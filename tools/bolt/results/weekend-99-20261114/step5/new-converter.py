#!/usr/bin/env python3
"""Convert installed ThinLTO archive members using a certified backend policy.

Requires Python >= 3.9 on Linux and LLVM major 22. Custom ar/ELF parsing retains
header-offset identities for duplicate member names, and verifies full indexes.
Text IR metadata/attribute parsing depends on LLVM 22 llvm-dis output syntax.
Four architecture-specific policy points are deliberately explicit: backend
options, recorded-command classification, relocation rules, and triple allowlist.
Failing closed when parameters change is intentional; recertify before use.
The HQ allowlist accepts -g0 and has_debug_options also counts it as debug.
Current recorded commands contain no -g0; recheck this on clang upgrades.
"""
import argparse
from collections import Counter
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
import hashlib
import json
import mmap
import os
from pathlib import Path
import re
import shlex
import shutil
import signal
import stat
import struct
import subprocess
import sys
import tempfile
import threading
import time
import traceback

_CANCEL_SIGNAL = None


def cstring(data, offset):
    if not 0 <= offset < len(data):
        raise ValueError('string offset outside table')
    end = data.find(b'\0', offset)
    if end < 0:
        raise ValueError('unterminated string')
    return data[offset:end].decode('utf-8', 'surrogateescape')


def member_kind(data):
    if data[:4] in (b'BC\xc0\xde', b'\xde\xc0\x17\x0b'):
        return 'bitcode'
    if (len(data) >= 20 and data[:4] == b'\x7fELF' and
            data[4] in (1, 2) and data[5] in (1, 2) and
            int.from_bytes(data[16:18], 'little' if data[5] == 1 else 'big') == 1):
        return 'machine'
    return 'other'


def elf_details(data):
    """Defined external symbols and debug sections in an ELF relocatable member."""
    if member_kind(data) != 'machine':
        raise ValueError('not a native ELF relocatable')
    bits, endian = data[4], '<' if data[5] == 1 else '>'
    if bits == 2:
        shoff = struct.unpack_from(endian+'Q', data, 40)[0]
        entsize, count, names_idx = struct.unpack_from(endian+'HHH', data, 58)
        fmt = endian+'IIQQQQIIQQ'; symfmt = endian+'IBBHQQ'
    else:
        shoff = struct.unpack_from(endian+'I', data, 32)[0]
        entsize, count, names_idx = struct.unpack_from(endian+'HHH', data, 46)
        fmt = endian+'IIIIIIIIII'; symfmt = endian+'IIIBBH'
    if not shoff:
        return [], []
    if entsize < struct.calcsize(fmt):
        raise ValueError('short ELF section header')
    zero = struct.unpack_from(fmt, data, shoff)
    if count == 0:
        count = zero[5]
    if names_idx == 0xffff:
        names_idx = zero[6]
    if names_idx >= count:
        raise ValueError('ELF section name index outside table')
    sections = [struct.unpack_from(fmt, data, shoff+i*entsize) for i in range(count)]
    def contents(section):
        start, size = section[4:6]
        if start+size > len(data):
            raise ValueError('ELF section outside member')
        return data[start:start+size]
    names = contents(sections[names_idx]) if names_idx else b'\0'
    debug = [cstring(names, s[0]) for s in sections
             if cstring(names, s[0]).startswith(('.debug', '.zdebug', '.rel.debug', '.rela.debug'))]
    symbols = []
    for s in sections:
        if s[1] != 2:  # SHT_SYMTAB, not dynamic symbols
            continue
        if s[6] >= count:
            raise ValueError("ELF symbol table link outside section table")
        strings = contents(sections[s[6]])
        table = contents(s); stride = s[9]
        if stride < struct.calcsize(symfmt) or len(table) % stride:
            raise ValueError('invalid ELF symbol table')
        for pos in range(0, len(table), stride):
            fields = struct.unpack_from(symfmt, table, pos)
            name, info, ndx = (fields[0], fields[1], fields[3]) if bits == 2 else (fields[0], fields[3], fields[5])
            if info >> 4 in (1, 2, 10) and ndx != 0 and name:
                symbols.append(cstring(strings, name))
    return symbols, debug


def ar_decimal(value):
    if re.fullmatch(r'[0-9]+', value) is None:
        raise ValueError('invalid ar long-name number: '+value)
    return int(value)


def inspect(path):
    path = Path(path)
    with path.open('rb') as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as data:
        magic = data[:8]
        if magic not in (b'!<arch>\n', b'!<thin>\n'):
            raise ValueError(f'not an archive: {path}')
        thin = magic == b'!<thin>\n'
        pos, longnames, raw_members, tables = 8, b'', [], []
        while pos < len(data):
            start = pos; header = data[pos:pos+60]
            if len(header) != 60 or header[58:60] != b'`\n':
                raise ValueError(f'invalid ar header at {pos}')
            if not re.fullmatch(rb'[0-9]+ *', header[48:58]):
                raise ValueError('invalid ar member size field')
            name = header[:16].decode('ascii').rstrip(); size = int(header[48:58]); pos += 60
            special = name in ('/', '//', '/SYM64/')
            stored_size = size if not thin or special else (ar_decimal(name[3:]) if name.startswith('#1/') else 0)
            if stored_size < 0 or stored_size > len(data)-pos:
                raise ValueError('ar member outside file')
            if name == '//':
                longnames = data[pos:pos+size]
            elif name in ('/', '/SYM64/'):
                tables.append((name, data[pos:pos+size]))
            else:
                raw_members.append(dict(header_offset=start, raw_name=name, offset=pos,
                                        size=size, mtime=header[16:28].decode().strip()))
            pos += stored_size + stored_size % 2
            if pos > len(data):
                raise ValueError('missing ar member alignment byte')
        members, offsets, native_map, occurrences = [], {}, [], Counter()
        for m in raw_members:
            name, off, size = m.pop('raw_name'), m['offset'], m['size']
            if name.startswith('#1/'):
                n = ar_decimal(name[3:])
                if not 0 <= n <= size:
                    raise ValueError('invalid BSD long name length')
                name = data[off:off+n].rstrip(b'\0').decode('utf-8', 'surrogateescape'); off += n; size -= n
            elif name.startswith('/'):
                n = ar_decimal(name[1:])
                if not 0 <= n < len(longnames):
                    raise ValueError('GNU long name offset outside table')
                if n and longnames[n-1:n] != b'\n':
                    raise ValueError('GNU long name offset inside entry')
                end = longnames.find(b'/\n', n)
                if end < 0:
                    raise ValueError('invalid GNU long name')
                name = longnames[n:end].decode('utf-8', 'surrogateescape')
            else:
                name = name.removesuffix('/')
            if name.startswith('__.SYMDEF'):
                raise ValueError('BSD ar symbol table unsupported; refuse silent index loss')
            ordinal = len(members); occurrences[name] += 1
            m.update(name=name, ordinal=ordinal, occurrence=occurrences[name], offset=off, size=size)
            payload = data[off:off+size] if not thin else b''
            m['magic_hex'] = payload[:4].hex() if not thin else None
            m['kind'] = member_kind(payload) if not thin else 'other'
            m['sha256'] = hashlib.sha256(payload).hexdigest() if not thin else None
            m['debug_sections'] = []
            if m['kind'] == 'machine':
                symbols, m['debug_sections'] = elf_details(payload)
                native_map += [[s, ordinal, name, occurrences[name]] for s in symbols]
            offsets[m['header_offset']] = m; members.append(m)
        index = []
        if len(tables) > 1:
            raise ValueError('multiple ar indexes not supported')
        for name, table in tables:
            width = 8 if name == '/SYM64/' else 4
            if len(table) < width:
                raise ValueError('short ar index')
            count = int.from_bytes(table[:width], 'big'); names_start = width*(1+count)
            if names_start > len(table):
                raise ValueError('ar index offset array truncated')
            string_pos = names_start
            for n in range(count):
                offset = int.from_bytes(table[width*(n+1):width*(n+2)], 'big')
                if offset not in offsets:
                    raise ValueError('ar index references a non-member header')
                symbol = cstring(table, string_pos); string_pos = table.index(b'\0', string_pos)+1
                m = offsets[offset]; index.append([symbol, m['ordinal'], m['name'], m['occurrence']])
        counts = Counter(m['kind'] for m in members)
        return dict(path=str(path), bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), thin=thin,
                    members=members, member_count=len(members), bitcode=counts['bitcode'],
                    machine=counts['machine'], other=counts['other'], index=index, index_entries=len(index),
                    index_equals_machine_symbols=Counter(map(tuple,index))==Counter(map(tuple,native_map)),
                    machine_symbol_entries=len(native_map))


CERTIFIED_LLVM_MAJOR = 22
CERTIFIED_OPTIMIZATION = {'x86_64': '-O3'}
CERTIFIED_TRIPLES = {'x86_64': {'x86_64-tizen-linux-gnu'}}
SWITCH_KEYS = ('function-sections', 'data-sections', 'unique-section-names', 'addrsig')
BACKEND_FLAGS = ['-ffunction-sections', '-fdata-sections',
                 '-funique-section-names', '-faddrsig']
# Replay mirrors the recorded command: section/symbol emission and debug emission
# follow the original backend policy (-f/-fno- per switch; -g -gdwarf-4 only when
# the original command recorded debug options).
# LLVM 22 clang/Driver/ToolChains/Clang.cpp:2797, 6228, 7992-7999.
DEFAULTS = {'unique-section-names': True, 'addrsig': True, 'fp-contract': 'on'}


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def classify_options(argv, arch='x86_64'):
    """Certified policy, not arbitrary compiler-option replay; consume operands."""
    if arch not in CERTIFIED_OPTIMIZATION:
        raise ValueError('uncertified architecture: '+arch)
    rows, optimizations, dwarfs, contractions = [], [], [], []
    switches = {key: [] for key in SWITCH_KEYS}
    operand_options = {'-D', '-I', '-isystem', '-resource-dir', '-o', '-MT', '-MF', '-x', '--param'}
    exact_ir = {'-fomit-frame-pointer', '-fno-omit-frame-pointer', '-fexceptions',
                '-fno-exceptions', '-fasynchronous-unwind-tables', '-funwind-tables',
                '-fno-asynchronous-unwind-tables', '-fno-unwind-tables', '-fno-common',
                '-ftrapping-math', '-m64', '-fPIC', '-fPIE', '-fpic', '-fpie',
                '-fno-pic', '-fno-pie', '-fno-semantic-interposition'}
    exact_ir.update({'-fvisibility-inlines-hidden', '-fno-visibility-inlines-hidden'})
    exact_ir.update({'-feliminate-unused-debug-types'})
    index = 0
    while index < len(argv):
        token = argv[index]
        category, reason = None, None
        if index == 0 and re.fullmatch(r'clang(?:\+\+)?(?:-22)?', Path(token).name):
            category, reason = 'irrelevant', 'original driver path'
        elif token in operand_options:
            if index+1 == len(argv) or argv[index+1].startswith('-'):
                raise ValueError('missing operand for '+token)
            if token == '--param' and not re.fullmatch(r'ssp-buffer-size=\d+', argv[index+1]):
                raise ValueError('unclassified --param value: '+argv[index+1])
            category, reason = 'irrelevant', 'preprocessing, driver resource, output or language operand'
            rows.append(dict(index=index, token=token, category=category, reason=reason))
            index += 1
            rows.append(dict(index=index, token=argv[index], category=category, reason='operand of '+token))
            index += 1
            continue
        elif re.fullmatch(r'-O(?:[0-3szg]|fast)', token):
            category, reason = 'ir', 'original IR pipeline; certified last optimization is also replayed'
            optimizations.append(token)
        elif re.fullmatch(r'-gdwarf-\d+', token):
            category, reason = 'restore', 'debug emission version'
            dwarfs.append(token)
        elif token.startswith('-ffp-contract='):
            category, reason = 'restore', 'backend FP fusion policy'
            contractions.append(token.split('=', 1)[1])
        elif any(token in ('-f'+key, '-fno-'+key) for key in switches):
            category, reason = 'restore', 'backend section/symbol emission policy'
            for key in switches:
                if token in ('-f'+key, '-fno-'+key):
                    switches[key].append(token == '-f'+key)
        elif (token in exact_ir or re.fullmatch(r'-fvisibility=(?:default|hidden|protected)', token)
              or re.fullmatch(r'-g(?:[0-3]|line-tables-only|line-directives-only)?', token)
              or re.fullmatch(r'-march=[A-Za-z0-9_.+-]+', token)
              or re.fullmatch(r'-m(?:sse|avx)[A-Za-z0-9_.-]*', token)
              or re.fullmatch(r'-mfpmath=(?:sse|387|sse,387|387,sse)', token)
              or token in ('-frecord-command-line', '-frecord-gcc-switches')
              or token.startswith('-std=')):
            category, reason = 'ir', 'function/module attributes, metadata or frontend semantics'
        elif token == '-flto=thin':
            category, reason = 'irrelevant', 'pre-link bitcode format already materialized; never replay LTO'
        elif re.fullmatch(r'--param=ssp-buffer-size=\d+', token):
            category, reason = 'ir', 'stack-protector-buffer-size function attribute already in the IR'
        elif token == '-Xassembler' or token.startswith('-Wa,'):
            raise ValueError('uncertified assembler option: '+token)
        elif (token.startswith(('-W', '-D', '-I', '--target=', '-fmessage-length=',
                               '-fdiagnostics-color=')) or token in
              ('-fdiagnostics-color', '-fcolor-diagnostics', '-fno-color-diagnostics',
               '-pedantic', '-pipe', '-c', '-MD', '--driver-mode=g++')):
            category, reason = 'irrelevant', 'diagnostics, preprocessing or driver action'
        elif not token.startswith('-') and re.search(r'\.(?:c|cc|cpp|cxx|C|ii|i|bc|ll|o|obj|s|S)$', token):
            category, reason = 'irrelevant', 'input/output path'
        if category is None:
            raise ValueError('unclassified original command token: '+token)
        rows.append(dict(index=index, token=token, category=category, reason=reason))
        index += 1
    if not optimizations or optimizations[-1] != CERTIFIED_OPTIMIZATION[arch]:
        raise ValueError('uncertified last optimization: '+str(optimizations[-1:] or 'missing'))
    has_debug_options = any(token.startswith('-g') for token in argv)
    if has_debug_options and (not dwarfs or dwarfs[-1] != '-gdwarf-4'):
        raise ValueError('uncertified last DWARF option: '+str(dwarfs[-1:] or 'missing'))
    effective = {}
    for key, values in switches.items():
        effective[key] = values[-1] if values else DEFAULTS.get(key, False)
    # Replay emits the original value explicitly; only the section-naming defaults
    # that the certified backend relies on must remain enabled.
    for key in ('unique-section-names', 'addrsig'):
        if not effective[key]:
            raise ValueError('original command does not enable '+key)
    contraction = contractions[-1] if contractions else DEFAULTS['fp-contract']
    if contraction not in ('on', 'off', 'fast'):
        raise ValueError('uncertified FP contraction value: '+contraction)
    return dict(tokens=rows, optimization=optimizations[-1], dwarf=dwarfs[-1] if dwarfs else None,
                switches=effective, fp_contract=contraction,
                fp_contract_source='last explicit option' if contractions else 'LLVM 22 non-CUDA/HIP default on')


def ir_settings(lines, require_recorded_options=True, arch='x86_64', debug_info=None):
    """Read LLVM 22 textual metadata/attributes without modifying input IR."""
    retained, metadata = [], {}
    triple, command_id = None, None
    levels, cpus, features = {}, set(), set()
    for line in lines:
        # Intrinsic references, not string literals in LLVM's own implementation.
        for intrinsic in ('llvm.type.test', 'llvm.public.type.test'):
            if re.search(r'@'+re.escape(intrinsic)+r'(?:\.|\s*\()', line):
                raise ValueError('unsupported type metadata/intrinsic: '+intrinsic)
        if re.search(r'!vcall_visibility\b', line):
            raise ValueError('unsupported type metadata: !vcall_visibility')
        if re.search(r'!"EnableSplitLTOUnit"\s*,\s*i32\s+1\b', line):
            raise ValueError('unsupported type metadata: EnableSplitLTOUnit=1')
        if line.startswith('!llvm.commandline = '):
            match = re.fullmatch(r'!llvm.commandline = !\{!(\d+)\}\s*', line)
            if not match or command_id is not None:
                raise ValueError('exactly one recorded command is required')
            command_id = match[1]
        match = re.fullmatch(r'!(\d+) = !\{!"(.*)"\}\s*', line)
        if match:
            metadata[match[1]] = match[2]
        if line.startswith('target triple = '):
            value = line.split('"')[1]
            if triple is not None:
                raise ValueError('multiple IR triples')
            triple = value; retained.append(line.rstrip())
        if line.startswith('attributes #'):
            retained.append(line.rstrip())
            cpus.update(re.findall(r'"target-cpu"="([^"]+)"', line))
            features.update(re.findall(r'"target-features"="([^"]+)"', line))
        if line.startswith('!') and any('"'+n+'"' in line for n in ('PIC Level', 'PIE Level', 'Code Model')):
            retained.append(line.rstrip())
            match = re.search(r'!"(PIC Level|PIE Level|Code Model)", i32 (\d+)', line)
            if not match:
                raise ValueError('unrecognized relocation flag: '+line.rstrip())
            key, value = match.groups()
            if key in levels and levels[key] != int(value):
                raise ValueError('conflicting relocation flags')
            levels[key] = int(value)
    if triple not in CERTIFIED_TRIPLES.get(arch, set()):
        raise ValueError('uncertified '+arch+' IR triple: '+str(triple))
    pic, pie = levels.get('PIC Level', 0), levels.get('PIE Level', 0)
    if pic not in (0, 1, 2) or pie not in (0, 1, 2) or (pie and pie != pic):
        raise ValueError('unsupported PIC/PIE flags')
    if 'Code Model' in levels:
        raise ValueError('explicit code model requires separate certification')
    if command_id not in metadata:
        raise ValueError('missing original command: backend policy cannot be certified')
    recorded_command = shlex.split(re.sub(r'\\([0-9A-Fa-f]{2})',
        lambda match: chr(int(match[1], 16)), metadata[command_id]))
    found_debug = 'yes' if any(token.startswith('-g') for token in recorded_command) else 'no'
    if debug_info is not None and debug_info != found_debug:
        raise ValueError('debug-info expected %s, found %s' %
                         ('debug' if debug_info == 'yes' else 'release',
                          'debug' if found_debug == 'yes' else 'release'))
    policy = classify_options(recorded_command, arch)
    flags = ['--no-default-config', '--target='+triple, '-x', 'ir', policy['optimization'],
             *(('-f'+key) if policy['switches'][key] else ('-fno-'+key)
               for key in SWITCH_KEYS)]
    if policy['dwarf']:
        flags += ['-g', policy['dwarf']]
    flags += ['-ffp-contract='+policy['fp_contract'], '-c']
    flags += ([{1: '-fpie', 2: '-fPIE'}[pie]] if pie else
              [{1: '-fpic', 2: '-fPIC'}[pic]] if pic else ['-fno-pic', '-fno-pie'])
    return dict(triple=triple, pic_level=pic, pie_level=pie, target_cpu=sorted(cpus),
                target_features=sorted(features), flags=flags, evidence=retained,
                recorded_command=recorded_command, policy=policy)


# LLVM 22.1.8 ELFRelocs/x86_64.def numbers; x86-64 psABI section 4.4,
# Relocation Types and Large Model Relocation Types (LP64 field bytes).
# Dynamic-loader-only relocations are deliberately absent from the accepted
# table. COPY has no fixed-size field; TLSDESC_CALL is a zero-width marker.
# 0 R_X86_64_NONE: 0 bytes; psABI Relocation Types: none (linker marker); accept.
# 1 R_X86_64_64: 8 bytes; psABI Relocation Types: word64; accept.
# 2 R_X86_64_PC32: 4 bytes; psABI Relocation Types: word32; accept.
# 3 R_X86_64_GOT32: 4 bytes; psABI Relocation Types: word32; accept.
# 4 R_X86_64_PLT32: 4 bytes; psABI Relocation Types: word32; accept.
# 5 R_X86_64_COPY: 0 bytes; psABI Relocation Types: none (COPY has no fixed field); reject dynamic-only.
# 6 R_X86_64_GLOB_DAT: 8 bytes; psABI Relocation Types: word64; reject dynamic-only.
# 7 R_X86_64_JUMP_SLOT: 8 bytes; psABI Relocation Types: word64; reject dynamic-only.
# 8 R_X86_64_RELATIVE: 8 bytes; psABI Relocation Types: word64; reject dynamic-only.
# 9 R_X86_64_GOTPCREL: 4 bytes; psABI Relocation Types: word32; accept.
# 10 R_X86_64_32: 4 bytes; psABI Relocation Types: word32; accept.
# 11 R_X86_64_32S: 4 bytes; psABI Relocation Types: word32; accept.
# 12 R_X86_64_16: 2 bytes; psABI Relocation Types: word16; accept.
# 13 R_X86_64_PC16: 2 bytes; psABI Relocation Types: word16; accept.
# 14 R_X86_64_8: 1 bytes; psABI Relocation Types: word8; accept.
# 15 R_X86_64_PC8: 1 bytes; psABI Relocation Types: word8; accept.
# 16 R_X86_64_DTPMOD64: 8 bytes; psABI Relocation Types: word64; reject dynamic-only.
# 17 R_X86_64_DTPOFF64: 8 bytes; psABI Relocation Types: word64; accept.
# 18 R_X86_64_TPOFF64: 8 bytes; psABI Relocation Types: word64; accept.
# 19 R_X86_64_TLSGD: 4 bytes; psABI Relocation Types: word32; accept.
# 20 R_X86_64_TLSLD: 4 bytes; psABI Relocation Types: word32; accept.
# 21 R_X86_64_DTPOFF32: 4 bytes; psABI Relocation Types: word32; accept.
# 22 R_X86_64_GOTTPOFF: 4 bytes; psABI Relocation Types: word32; accept.
# 23 R_X86_64_TPOFF32: 4 bytes; psABI Relocation Types: word32; accept.
# 24 R_X86_64_PC64: 8 bytes; psABI Relocation Types: word64; accept.
# 25 R_X86_64_GOTOFF64: 8 bytes; psABI Relocation Types: word64; accept.
# 26 R_X86_64_GOTPC32: 4 bytes; psABI Relocation Types: word32; accept.
# 27 R_X86_64_GOT64: 8 bytes; psABI Large Model Relocation Types: word64; accept.
# 28 R_X86_64_GOTPCREL64: 8 bytes; psABI Large Model Relocation Types: word64; accept.
# 29 R_X86_64_GOTPC64: 8 bytes; psABI Large Model Relocation Types: word64; accept.
# 30 R_X86_64_GOTPLT64: 8 bytes; psABI Large Model Relocation Types: word64; accept.
# 31 R_X86_64_PLTOFF64: 8 bytes; psABI Large Model Relocation Types: word64; accept.
# 32 R_X86_64_SIZE32: 4 bytes; psABI Relocation Types: word32; accept.
# 33 R_X86_64_SIZE64: 8 bytes; psABI Relocation Types: word64; accept.
# 34 R_X86_64_GOTPC32_TLSDESC: 4 bytes; psABI Relocation Types: word32; accept.
# 35 R_X86_64_TLSDESC_CALL: 0 bytes; psABI Relocation Types: none (linker marker); accept.
# 36 R_X86_64_TLSDESC: 16 bytes; psABI Relocation Types: word64 x 2; reject dynamic-only.
# 37 R_X86_64_IRELATIVE: 8 bytes; psABI Relocation Types: word64; reject dynamic-only.
# 41 R_X86_64_GOTPCRELX: 4 bytes; psABI Relocation Types: word32; accept.
# 42 R_X86_64_REX_GOTPCRELX: 4 bytes; psABI Relocation Types: word32; accept.
# 43 R_X86_64_CODE_4_GOTPCRELX: 4 bytes; psABI Relocation Types: word32; accept.
# 44 R_X86_64_CODE_4_GOTTPOFF: 4 bytes; psABI Relocation Types: word32; accept.
# 45 R_X86_64_CODE_4_GOTPC32_TLSDESC: 4 bytes; psABI Relocation Types: word32; accept.
# 50 R_X86_64_CODE_6_GOTTPOFF: 4 bytes; psABI Relocation Types: word32; accept.
X86_64_RELOCATION_WIDTHS = {
    0: 0,  # R_X86_64_NONE
    1: 8,  # R_X86_64_64
    2: 4,  # R_X86_64_PC32
    3: 4,  # R_X86_64_GOT32
    4: 4,  # R_X86_64_PLT32
    9: 4,  # R_X86_64_GOTPCREL
    10: 4,  # R_X86_64_32
    11: 4,  # R_X86_64_32S
    12: 2,  # R_X86_64_16
    13: 2,  # R_X86_64_PC16
    14: 1,  # R_X86_64_8
    15: 1,  # R_X86_64_PC8
    17: 8,  # R_X86_64_DTPOFF64
    18: 8,  # R_X86_64_TPOFF64
    19: 4,  # R_X86_64_TLSGD
    20: 4,  # R_X86_64_TLSLD
    21: 4,  # R_X86_64_DTPOFF32
    22: 4,  # R_X86_64_GOTTPOFF
    23: 4,  # R_X86_64_TPOFF32
    24: 8,  # R_X86_64_PC64
    25: 8,  # R_X86_64_GOTOFF64
    26: 4,  # R_X86_64_GOTPC32
    27: 8,  # R_X86_64_GOT64
    28: 8,  # R_X86_64_GOTPCREL64
    29: 8,  # R_X86_64_GOTPC64
    30: 8,  # R_X86_64_GOTPLT64
    31: 8,  # R_X86_64_PLTOFF64
    32: 4,  # R_X86_64_SIZE32
    33: 8,  # R_X86_64_SIZE64
    34: 4,  # R_X86_64_GOTPC32_TLSDESC
    35: 0,  # R_X86_64_TLSDESC_CALL
    41: 4,  # R_X86_64_GOTPCRELX
    42: 4,  # R_X86_64_REX_GOTPCRELX
    43: 4,  # R_X86_64_CODE_4_GOTPCRELX
    44: 4,  # R_X86_64_CODE_4_GOTTPOFF
    45: 4,  # R_X86_64_CODE_4_GOTPC32_TLSDESC
    50: 4,  # R_X86_64_CODE_6_GOTTPOFF
}


def pic_relocations(data):
    """Validate x86_64 ET_REL tables and reject non-PIC ALLOC relocations.

    Absolute 8-, 16- and 32-bit relocations against non-absolute symbols
    are forbidden in both writable and read-only ALLOC sections; 64-bit
    absolute relocations are forbidden in read-only ALLOC sections.
    SHN_ABS references remain allowed. Debug sections are excluded from
    the PIC policy, but all relocation indexes and target byte ranges are
    validated. PC-relative relocations may be legitimate (e.g. .eh_frame).
    """
    if (len(data) < 64 or member_kind(data) != 'machine' or
            data[4:6] != b'\x02\x01' or struct.unpack_from('<H', data, 18)[0] != 62):
        raise ValueError('not x86_64 ELF64 little-endian ET_REL')
    off = struct.unpack_from('<Q', data, 40)[0]
    stride, count = struct.unpack_from('<HH', data, 58)
    if not off or stride != 64 or off + 64 > len(data):
        raise ValueError('invalid ELF section table')
    if not count:
        count = struct.unpack_from('<IIQQQQIIQQ', data, off)[5]
    if not count or count > (len(data)-off) // stride:
        raise ValueError('ELF section table outside member')
    sections = [struct.unpack_from('<IIQQQQIIQQ', data, off+i*stride) for i in range(count)]
    checked, forbidden = 0, []
    for section in sections:
        if section[1] == 19:  # SHT_RELR is not supported in ET_REL members.
            raise ValueError('unsupported RELR relocation section')
        if section[1] == 0x40000014:
            raise ValueError('unsupported CREL relocation section')
        if section[1] not in (0, 8) and section[4] + section[5] > len(data):
            raise ValueError('ELF section outside member')
    for section in sections:
        if section[1] not in (4, 9):
            continue
        if section[6] >= count or section[7] >= count:
            raise ValueError('relocation link/info outside section table')
        target = sections[section[7]]
        limit = target[5]
        if target[2] & 0x800:  # SHF_COMPRESSED: offsets use uncompressed size.
            if target[5] < 24 or target[4] + 24 > len(data):
                raise ValueError('short compressed ELF section header')
            compression, reserved, limit, alignment = struct.unpack_from('<IIQQ', data, target[4])
            if compression not in (1, 2):  # ELFCOMPRESS_ZLIB / ELFCOMPRESS_ZSTD
                raise ValueError('unsupported ELF compression type: '+str(compression))
            if alignment and alignment & (alignment - 1):
                raise ValueError('invalid compressed ELF section alignment: '+str(alignment))
        symbols = sections[section[6]]
        if (symbols[1] != 2 or symbols[9] != 24 or symbols[5] % 24 or
                symbols[4] + symbols[5] > len(data)):
            raise ValueError('invalid relocation symbol table')
        relocation_stride = 24 if section[1] == 4 else 16
        if (section[9] != relocation_stride or section[5] % relocation_stride or
                section[4] + section[5] > len(data)):
            raise ValueError('invalid relocation table')
        symbol_count = symbols[5] // 24
        for pos in range(section[4], section[4]+section[5], section[9]):
            r_offset, info = struct.unpack_from('<QQ', data, pos)
            kind, symbol_index = info & 0xffffffff, info >> 32
            if kind not in X86_64_RELOCATION_WIDTHS:
                raise ValueError('uncertified x86_64 relocation type: '+str(kind))
            width = X86_64_RELOCATION_WIDTHS[kind]
            if kind != 0 and (r_offset + width > limit or (width == 0 and r_offset == limit)):
                raise ValueError('relocation offset outside target section')
            if symbol_index >= symbol_count:
                raise ValueError('relocation symbol index outside table')
            symbol = struct.unpack_from('<IBBHQQ', data, symbols[4]+symbol_index*symbols[9])
            if not target[2] & 2:
                continue
            checked += 1
            # SHN_ABS references do not need runtime relocation.
            if symbol[3] != 0xfff1 and (kind in (10, 11, 12, 14) or (kind == 1 and not target[2] & 1)):
                forbidden.append(dict(type=kind, target_section=section[7], symbol_index=symbol_index))
    return dict(checked=checked, forbidden=forbidden)



def atomic_json(path, value):
    path = Path(path)
    fd, name = tempfile.mkstemp(prefix='.'+path.name+'.', dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(value, stream, indent=2)
            stream.write('\n')
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


class Commands:
    def __init__(self, address_space_bytes=4*1024**3, timeout=600):
        self.stop = threading.Event()
        self.lock = threading.Lock()
        self.children = set()
        self.address_space_bytes = address_space_bytes
        self.timeout = timeout
        self.signal_received = None
        self.cancelled_at = None
        self.failure_reason = None

    def interrupted(self, sig, frame):
        # Python handlers run in the main thread: never acquire a worker lock here.
        global _CANCEL_SIGNAL
        _CANCEL_SIGNAL = sig
        self.signal_received = sig

    def cancel(self, reason=None):
        with self.lock:
            if reason is not None and self.failure_reason is None:
                self.failure_reason = reason
            if self.cancelled_at is None:
                self.cancelled_at = time.monotonic()
            self.stop.set()
            for child in self.children:
                try:
                    os.killpg(child.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass

    def check(self):
        if self.signal_received is not None:
            self.cancel()
            raise RuntimeError('cancelled by signal '+str(self.signal_received))
        if self.stop.is_set():
            raise RuntimeError('cancelled after: '+self.failure_reason if self.failure_reason else 'cancelled after command failure')

    def run(self, argv, prefix, stdout=None):
        # Reap the direct child and stop running members of its process group. Orphaned
        # grandchildren go to the nearest subreaper or PID 1; members that left the
        # process group are not signalled. SIGKILL is not awaited. Uninterruptible
        # kernel sleep can hold finally indefinitely; the outer timeout must handle that
        # case. This is not a subreaper.
        self.check()
        prefix = Path(prefix)
        timing, log = prefix.with_suffix('.time'), prefix.with_suffix('.log')
        command = ['/usr/bin/prlimit', '--as='+str(self.address_space_bytes), '--core=0',
                   '--', *map(str, argv)]
        start = time.monotonic()
        reason, status, usage, observed = None, None, None, False
        with log.open('wb') as err:
            with self.lock:
                if self.stop.is_set() or self.signal_received is not None:
                    raise RuntimeError('cancelled before process launch')
                child = subprocess.Popen(command, stdout=stdout if stdout is not None else err,
                                         stderr=err, start_new_session=True)
                self.children.add(child)
            try:
                while True:
                    now = time.monotonic()
                    if self.signal_received is not None:
                        reason = 'signal '+str(self.signal_received)
                        self.cancel(reason)
                    if now-start >= self.timeout and not observed:
                        reason = 'command timeout after '+str(self.timeout)+' s'
                        self.cancel(reason)
                    if self.stop.is_set():
                        reason = reason or 'cancelled after command failure'
                        if now-self.cancelled_at >= 3:
                            try:
                                os.killpg(child.pid, signal.SIGKILL)
                            except ProcessLookupError:
                                pass
                    if not observed:
                        info = os.waitid(os.P_PID, child.pid,
                                         os.WEXITED | os.WNOHANG | os.WNOWAIT)
                        if info is not None:
                            observed = True
                            if info.si_code != os.CLD_EXITED or info.si_status:
                                reason = reason or 'command failed'
                                self.cancel(reason)  # Includes descendants after the leader exits.
                    if observed and (not self.stop.is_set() or now-self.cancelled_at >= 3):
                        break
                    time.sleep(0.05)
            finally:
                if not observed:
                    self.cancel()
                    remaining = 3-(time.monotonic()-self.cancelled_at)
                    if remaining > 0:
                        time.sleep(remaining)
                # Keep the leader unreaped until the last group signal, including
                # after normal leader exit. No reused PID can receive that signal.
                try:
                    os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                os.waitid(os.P_PID, child.pid, os.WEXITED | os.WNOWAIT)
                with self.lock:
                    _, status, usage = os.wait4(child.pid, 0)
                    child.returncode = os.waitstatus_to_exitcode(status)
                    self.children.discard(child)
        elapsed, rc = time.monotonic()-start, child.returncode
        record = dict(argv=list(map(str, argv)), bounded_argv=command, pid=child.pid,
                      elapsed_seconds=elapsed, exit=rc, wall=elapsed,
                      user=usage.ru_utime, sys=usage.ru_stime, max_rss_kib=usage.ru_maxrss,
                      accounting='os.waitid(WNOWAIT), os.wait4; Linux ru_maxrss is KiB',
                      timeout_seconds=self.timeout, failure_reason=reason,
                      stderr=log.read_text(errors='replace'))
        record['time_raw'] = f"{elapsed:.9f} {usage.ru_utime:.9f} {usage.ru_stime:.9f} {usage.ru_maxrss} {rc}\n"
        timing.write_text(record['time_raw'])
        atomic_json(prefix.with_suffix('.json'), record)
        if rc or reason:
            self.cancel()
            raise RuntimeError(f'{reason or "command failed"} ({rc}): {argv}; see {log}')
        self.check()
        return record


def parse_nm(text):
    result = []
    for line in text.splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r'\s*(?:[0-9A-Fa-f-]+\s+)?([A-Za-z?])\s+(.+)', line)
        if not match:
            raise ValueError('unrecognized llvm-nm output: '+line)
        result.append((match[1], match[2]))
    return result


def compare_symbols(before, after):
    native_names = {name for kind, name in after}
    missing = [(kind, name) for kind, name in before if name not in native_names]
    strong_missing = [(kind, name) for kind, name in missing
                      if kind not in ('W', 'V', 'U', 'w', 'v', 'u') and not kind.islower()]
    return dict(before_count=len(before), after_count=len(after),
                missing_by_type=dict(Counter(kind for kind, name in missing)),
                missing=missing, strong_missing=strong_missing)


def check_symbols(nm, source, target, command):
    rows = []
    for label, path in [('bitcode', source), ('native', target)]:
        output = source.parent/(label+'-symbols.txt')
        with output.open('wb') as stream:
            command.run([nm, '--defined-only', '--extern-only', str(path)],
                        source.parent/(label+'-nm'), stdout=stream)
        rows.append(parse_nm(output.read_text()))
    result = compare_symbols(*rows)
    atomic_json(source.parent/'symbols.json', dict(result, bitcode_symbols=rows[0], native_symbols=rows[1]))
    if result['strong_missing']:
        raise ValueError('strong defined symbols missing after conversion: '+repr(result['strong_missing']))
    return result


def validate_archive(archive):
    if archive.is_symlink():
        raise ValueError('archive symlink not certified: '+str(archive))
    data = inspect(archive)
    if data['thin']:
        raise ValueError('thin archive is not supported: '+str(archive))
    if data['other']:
        raise ValueError('other-format archive members are not supported: '+str(archive))
    return data


def validate_tools(build, compiler, disassembler, nm, command, output):
    if not (build/'CMakeCache.txt').is_file():
        raise ValueError('missing CMakeCache.txt under --build: '+str(build))
    for label, tool in [('compiler', compiler), ('disassembler', disassembler), ('nm', nm)]:
        if not tool.is_file() or not os.access(tool, os.X_OK):
            raise ValueError('missing or non-executable --'+label+': '+str(tool))
    for label, tool in [('disassembler', disassembler), ('nm', nm)]:
        if tool.resolve().parent != compiler.resolve().parent:
            raise ValueError(label+' directory differs from compiler directory')
    version = output/'compiler-version.txt'
    with version.open('wb') as stream:
        command.run([compiler, '--version'], output/'compiler-version-command', stdout=stream)
    text = version.read_text()
    match = re.search(r'clang version (\d+)\.', text)
    if not match or int(match[1]) != CERTIFIED_LLVM_MAJOR:
        raise ValueError('uncertified compiler major (required 22): '+text.strip())
    full_version = re.search(r'clang version (\d+\.\d+\.\d+)\b', text)
    if not full_version:
        raise ValueError('missing complete clang version: '+text.strip())
    tool_versions = {'compiler': full_version[1]}
    version_texts = {'compiler': text}
    for label, tool in [('disassembler', disassembler), ('nm', nm)]:
        tool_version = output/(label+'-version.txt')
        with tool_version.open('wb') as stream:
            command.run([tool, '--version'], output/(label+'-version-command'), stdout=stream)
        tool_text = tool_version.read_text()
        match = re.search(r'LLVM version (\d+\.\d+\.\d+)\b', tool_text)
        if not match or match[1] != full_version[1]:
            raise ValueError('%s version mismatch: expected %s, found %s' %
                             (label, full_version[1], match[1] if match else tool_text.strip()))
        tool_versions[label] = match[1]
        version_texts[label] = tool_text
    return dict(compiler=str(compiler), version=text, compiler_sha256=sha(compiler),
                disassembler=str(disassembler), nm=str(nm),
                tool_versions=tool_versions, version_texts=version_texts,
                tool_directory=str(compiler.resolve().parent))


def reset_evidence(root, output, build):
    root, output, build = root.resolve(), output.resolve(), build.resolve()
    if (root == Path('/') or not root.is_dir() or not build.is_dir() or
            output == build or build.is_relative_to(output) or root.is_relative_to(output)
            or output.is_relative_to(root)):
        raise ValueError('unsafe or overlapping install/build/evidence directories')
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)


def atomic_install(candidate, destination, expected_sha):
    mode = stat.S_IMODE(destination.stat().st_mode)
    fd, name = tempfile.mkstemp(prefix='.'+destination.name+'.native-', dir=destination.parent)
    os.close(fd)
    try:
        shutil.copyfile(candidate, name)
        if sha(name) != expected_sha:
            raise ValueError('temporary archive copy SHA mismatch: '+str(destination))
        os.chmod(name, mode)
        os.replace(name, destination)
        if sha(destination) != expected_sha:
            raise ValueError('installed archive SHA mismatch: '+str(destination))
    finally:
        if os.path.exists(name):
            os.unlink(name)


def cleanup_evidence(output):
    archives = output/'archives'
    if archives.exists():
        shutil.rmtree(archives)
    # Keep JSON audit records, not bitcode/ELF/text-IR/nm/command-log payloads.
    for path in output.rglob('*'):
        if path.is_file() and path.suffix != '.json':
            path.unlink()

def convert(root, output, compiler, disassembler, nm, build, arch='x86_64', jobs=4,
            address_space_bytes=4*1024**3, command=None, debug_info=None):
    root, output, build = Path(root).resolve(), Path(output).resolve(), Path(build).resolve()
    if arch not in CERTIFIED_OPTIMIZATION or jobs < 1 or address_space_bytes < 1:
        raise ValueError('invalid architecture or resource parameters')
    if debug_info not in ('yes', 'no'):
        raise ValueError('debug-info expected=yes|no found='+str(debug_info))
    reset_evidence(root, output, build)
    command = command or Commands(address_space_bytes)
    summary = dict(started=time.time(), input_root=str(root), output_root=str(output),
                   arch=arch, workers=jobs, as_bytes=address_space_bytes, archives=[],
                   status='CONVERTING', debug_info=debug_info, missing_symbols_by_type={})
    def save():
        atomic_json(output/'summary.json', summary)
    save()
    old_handlers = {sig: signal.getsignal(sig) for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP)}
    for sig, handler in old_handlers.items():
        if handler != signal.SIG_IGN:
            signal.signal(sig, command.interrupted)
    try:
        summary['tools'] = validate_tools(build, Path(compiler), Path(disassembler), Path(nm), command, output)
        print('NATIVE_ARCHIVES_TOOLS', json.dumps({
            'tool_versions': summary['tools']['tool_versions'],
            'tool_directory': summary['tools']['tool_directory']}), flush=True)
        archives = [(archive, validate_archive(archive)) for archive in sorted(root.rglob('*.a'))]
        summary['scanned_archives'] = len(archives)
        summary['native_archives_skipped'] = sum(not data['bitcode'] for archive, data in archives)
        # Preserved native members retain their bytes, including any debug sections.
        summary['native_members_preserved'] = sum(data['machine'] for archive, data in archives)
        for archive, before in archives:
            command.check()
            if not before['bitcode']:
                continue
            rel = archive.relative_to(root)
            work = output/'members'/rel
            work.mkdir(parents=True)
            atomic_json(work/'before.json', before)
            paths = []
            with archive.open('rb') as stream:
                for member in before['members']:
                    if Path(member['name']).name != member['name'] or member['name'] in ('.', '..'):
                        raise ValueError('unsafe archive member name')
                    folder = work/f"{member['ordinal']:05d}"
                    folder.mkdir()
                    source = folder/'input.bc'
                    target = folder/member['name']
                    if target == source:
                        raise ValueError('reserved input name collision')
                    stream.seek(member['offset'])
                    payload = stream.read(member['size'])
                    if hashlib.sha256(payload).hexdigest() != member['sha256']:
                        raise ValueError('extracted member SHA mismatch')
                    (source if member['kind'] == 'bitcode' else target).write_bytes(payload)
                    paths.append((member, source, target))
            def process(item):
                member, source, target = item
                command.check()
                if member['kind'] == 'machine':
                    if sha(target) != member['sha256']:
                        raise ValueError('native member changed')
                    relocs = pic_relocations(target.read_bytes())
                    atomic_json(source.parent/'relocations.json', relocs)
                    return dict(ordinal=member['ordinal'], name=member['name'], preserved=True,
                                relocation_check=relocs)
                text_ir = source.with_suffix('.ll')
                with text_ir.open('wb') as out:
                    command.run([disassembler, str(source), '-o', '-'], source.parent/'disassemble', stdout=out)
                with text_ir.open() as lines:
                    settings = ir_settings(lines, arch=arch, debug_info=debug_info)
                atomic_json(source.parent/'ir-settings.json', settings)
                text_ir.unlink()
                record = command.run([compiler, *settings['flags'], str(source), '-o', str(target)], source.parent/'convert')
                data = target.read_bytes()
                if settings['policy']['dwarf'] is None and elf_details(data)[1]:
                    raise ValueError('release conversion unexpectedly emitted debug sections')
                relocs = pic_relocations(data)
                atomic_json(source.parent/'relocations.json', relocs)
                if settings['pic_level'] and relocs['forbidden']:
                    raise ValueError('non-PIC relocation in '+str(target))
                symbols = check_symbols(nm, source, target, command)
                return dict(ordinal=member['ordinal'], name=member['name'], preserved=False,
                            settings=settings, conversion=record, symbols=symbols, sha256=sha(target))
            results = []
            iterator = iter(paths)
            with ThreadPoolExecutor(max_workers=jobs) as pool:
                pending = {pool.submit(process, item) for item in list(next(iterator, None) for _ in range(jobs)) if item is not None}
                try:
                    while pending:
                        command.check()
                        done, pending = wait(pending, timeout=0.05, return_when=FIRST_COMPLETED)
                        for future in done:
                            results.append(future.result())
                        for _ in done:
                            item = next(iterator, None)
                            if item is not None:
                                pending.add(pool.submit(process, item))
                except BaseException:
                    command.cancel()
                    for future in pending:
                        future.cancel()
                    raise
            target_archive = output/'archives'/rel
            target_archive.parent.mkdir(parents=True, exist_ok=True)
            command.run(['/usr/bin/ar', 'qcDS', str(target_archive), *[str(t) for _, _, t in paths]], work/'pack')
            command.run(['/usr/bin/ar', 'sD', str(target_archive)], work/'index')
            after = inspect(target_archive)
            atomic_json(work/'after.json', after)
            if [(m['name'], m['occurrence']) for m in before['members']] != [(m['name'], m['occurrence']) for m in after['members']]:
                raise ValueError('member identity or order changed')
            if after['bitcode'] or after['other'] or not after['index_equals_machine_symbols']:
                raise ValueError('output format/index mismatch')
            for old, new in zip(before['members'], after['members']):
                if old['kind'] == 'machine' and old['sha256'] != new['sha256']:
                    raise ValueError('native member not preserved in archive')
            missing = Counter()
            for result in results:
                missing.update(result.get('symbols', {}).get('missing_by_type', {}))
            record = dict(path=str(rel), before_sha256=before['sha256'], after_sha256=after['sha256'],
                          before_bytes=before['bytes'], after_bytes=after['bytes'], members=before['member_count'],
                          converted=before['bitcode'], preserved=before['machine'], index_entries=after['index_entries'],
                          debug_members=sum(bool(m['debug_sections']) for m in after['members']),
                          missing_symbols_by_type=dict(missing), results=sorted(results, key=lambda x:x['ordinal']))
            summary['archives'].append(record)
            total_missing = Counter(summary['missing_symbols_by_type']); total_missing.update(missing)
            summary['missing_symbols_by_type'] = dict(total_missing)
            save()
            print(json.dumps({k:v for k,v in record.items() if k!='results'}), flush=True)
            for _, source, target in paths:
                if source.exists():
                    source.unlink()
                target.unlink()
        command.check()
        summary['status'] = 'CONVERTED'
        return summary
    except BaseException as error:
        command.cancel()
        summary.update(status='FAILED', reason=str(error))
        raise
    finally:
        try:
            summary['elapsed_seconds'] = time.time()-summary['started']
            cancelled = summary['status'] == 'CONVERTED' and command.signal_received is not None
            if cancelled:
                command.cancel()
                summary.update(status='FAILED', reason='signal '+str(command.signal_received))
            save()
            if cancelled:
                raise RuntimeError(summary['reason'])
        finally:
            for sig, handler in old_handlers.items():
                signal.signal(sig, handler)


def install(root, output, compiler, disassembler, nm, build, arch='x86_64', jobs=4,
            address_space_bytes=4*1024**3, debug_info=None):
    root, output = Path(root).resolve(), Path(output).resolve()
    command = Commands(address_space_bytes)
    old_handlers = {sig: signal.getsignal(sig) for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP)}
    for sig, handler in old_handlers.items():
        if handler != signal.SIG_IGN:
            signal.signal(sig, command.interrupted)
    result = None
    try:
        print('NATIVE_ARCHIVES_BEGIN', time.time(), flush=True)
        result = convert(root, output, compiler, disassembler, nm, build, arch, jobs, address_space_bytes, command, debug_info)
        command.check()
        result['status'] = 'INSTALLING'
        atomic_json(output/'summary.json', result)
        for record in result['archives']:
            command.check()
            destination, candidate = root/record['path'], output/'archives'/record['path']
            if sha(destination) != record['before_sha256'] or sha(candidate) != record['after_sha256']:
                raise ValueError('archive identity changed before atomic installation')
            atomic_install(candidate, destination, record['after_sha256'])
            record['installed'] = True
            atomic_json(output/'summary.json', result)
            print('NATIVE_ARCHIVE_INSTALLED', json.dumps({k:v for k,v in record.items() if k!='results'}), flush=True)
        command.check()
        cleanup_evidence(output)
        result.update(status='PASS', install_finished=time.time(), large_files_deleted=True)
        atomic_json(output/'summary.json', result)
        if not result['archives']:
            print('NATIVE_ARCHIVES_SKIP all archives already native', flush=True)
        command.check()
        print('NATIVE_ARCHIVES_END', time.time(), 'PASS', len(result['archives']), flush=True)
        return result
    except BaseException as error:
        command.cancel()
        if result is not None:
            result.update(status='INSTALL_FAILED', reason=str(error))
            atomic_json(output/'summary.json', result)
        raise
    finally:
        for sig, handler in old_handlers.items():
            signal.signal(sig, handler)


def log_startup_context():
    """Report exported target options and Python's inherited signal handlers."""
    architecture = {}
    for name in ('CFLAGS', 'CXXFLAGS'):
        try:
            tokens = shlex.split(os.environ.get(name, ''))
        except ValueError as error:
            # Diagnostics must not change conversion of already recorded IR.
            architecture[name] = {'parse_error': str(error)}
            continue
        # Same inherited architecture categories as the packaging flag policy.
        # Keep order and duplicates: the compiler applies last-option semantics.
        architecture[name] = [token for token in tokens if token == '-m64' or
                              token.startswith(('-march=', '-mtune=', '-msse', '-mfpmath='))]
    inherited = {}
    for name in ('SIGTERM', 'SIGINT', 'SIGHUP'):
        handler = signal.getsignal(getattr(signal, name))
        inherited[name] = ('ignored' if handler == signal.SIG_IGN else
                                             'default' if handler == signal.SIG_DFL else 'handler')
    print('NATIVE_ARCHIVES_STARTUP', json.dumps({
        'architecture_parameters': architecture, 'signals': inherited}), flush=True)


def install_main():
    global _CANCEL_SIGNAL
    _CANCEL_SIGNAL = None
    log_startup_context()
    if signal.getsignal(signal.SIGCHLD) != signal.SIG_DFL:
        signal.signal(signal.SIGCHLD, signal.SIG_DFL)
        print('NATIVE_ARCHIVES_SIGCHLD_RESET inherited handler -> SIG_DFL', flush=True)
    parser = argparse.ArgumentParser(description='Convert certified x86_64 ThinLTO archives before standard RPM stripping')
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--arch', choices=['x86_64'], required=True)
    parser.add_argument('--debug-info', choices=['yes', 'no'], required=True)
    parser.add_argument('--compiler', type=Path, required=True)
    parser.add_argument('--disassembler', type=Path, required=True)
    parser.add_argument('--nm', type=Path, required=True)
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--address-space-bytes', type=int, default=4*1024**3)
    args = parser.parse_args()
    def record_cancel(sig, frame):
        global _CANCEL_SIGNAL
        _CANCEL_SIGNAL = sig
    signals = (signal.SIGTERM, signal.SIGINT, signal.SIGHUP)
    old_handlers = {sig: signal.getsignal(sig) for sig in signals}
    for sig, handler in old_handlers.items():
        if handler != signal.SIG_IGN:
            signal.signal(sig, record_cancel)
    failure = None
    try:
        install(args.root, args.evidence, args.compiler.resolve(), args.disassembler.resolve(),
                args.nm.resolve(), args.build, args.arch, args.jobs, args.address_space_bytes, args.debug_info)
    except BaseException:
        failure = sys.exc_info()
    finally:
        for sig, handler in old_handlers.items():
            signal.signal(sig, handler)
    if _CANCEL_SIGNAL is not None:
        if failure is not None:
            traceback.print_exception(*failure)
        else:
            print('NATIVE_ARCHIVES_CANCELLED after completion', flush=True)
        return 128 + _CANCEL_SIGNAL
    if failure is not None:
        raise failure[1].with_traceback(failure[2])
    return 0


if __name__ == '__main__':
    raise SystemExit(install_main())
