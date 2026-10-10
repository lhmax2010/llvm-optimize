#!/usr/bin/env python3
"""Convert installed ThinLTO archive members using a certified backend policy.

Requires Python >= 3.9 on Linux and LLVM major 22. Custom ar/ELF parsing retains
header-offset identities for duplicate member names, and verifies full indexes.
Text IR metadata/attribute parsing depends on LLVM 22 llvm-dis output syntax.
Four architecture-specific policy points are deliberately explicit: backend
options, recorded-command classification, relocation rules, and triple allowlist.
Failing closed when parameters change is intentional; recertify before use.
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
import tempfile
import threading
import time


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
            name = header[:16].decode('ascii').rstrip(); size = int(header[48:58]); pos += 60
            special = name in ('/', '//', '/SYM64/')
            stored_size = size if not thin or special else (int(name[3:]) if name.startswith('#1/') else 0)
            if pos+stored_size > len(data):
                raise ValueError('ar member outside file')
            if name == '//':
                longnames = data[pos:pos+size]
            elif name in ('/', '/SYM64/'):
                tables.append((name, data[pos:pos+size]))
            else:
                raw_members.append(dict(header_offset=start, raw_name=name, offset=pos,
                                        size=size, mtime=header[16:28].decode().strip()))
            pos += stored_size + stored_size % 2
        members, offsets, native_map, occurrences = [], {}, [], Counter()
        for m in raw_members:
            name, off, size = m.pop('raw_name'), m['offset'], m['size']
            if name.startswith('#1/'):
                n = int(name[3:]); name = data[off:off+n].rstrip(b'\0').decode('utf-8', 'surrogateescape'); off += n; size -= n
            elif name.startswith('/'):
                n = int(name[1:]); end = longnames.find(b'/\n', n)
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
BACKEND_FLAGS = ['-ffunction-sections', '-fdata-sections',
                 '-funique-section-names', '-faddrsig', '-g', '-gdwarf-4']
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
    switches = {key: [] for key in ('function-sections', 'data-sections',
                                  'unique-section-names', 'addrsig')}
    operand_options = {'-D', '-I', '-isystem', '-resource-dir', '-o', '-MT', '-MF', '-x'}
    exact_ir = {'-fomit-frame-pointer', '-fno-omit-frame-pointer', '-fexceptions',
                '-fno-exceptions', '-fasynchronous-unwind-tables', '-funwind-tables',
                '-fno-asynchronous-unwind-tables', '-fno-unwind-tables', '-fno-common',
                '-ftrapping-math', '-m64', '-fPIC', '-fPIE', '-fpic', '-fpie',
                '-fno-pic', '-fno-pie', '-fno-semantic-interposition'}
    exact_ir.update({'-fvisibility-inlines-hidden', '-fno-visibility-inlines-hidden'})
    index = 0
    while index < len(argv):
        token = argv[index]
        category, reason = None, None
        if index == 0 and re.fullmatch(r'clang(?:\+\+)?(?:-22)?', Path(token).name):
            category, reason = 'irrelevant', 'original driver path'
        elif token in operand_options:
            if index+1 == len(argv) or argv[index+1].startswith('-'):
                raise ValueError('missing operand for '+token)
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
    if not dwarfs or dwarfs[-1] != '-gdwarf-4':
        raise ValueError('uncertified last DWARF option: '+str(dwarfs[-1:] or 'missing'))
    effective = {}
    for key, values in switches.items():
        effective[key] = values[-1] if values else DEFAULTS.get(key, False)
        if not effective[key]:
            raise ValueError('original command does not enable '+key)
    contraction = contractions[-1] if contractions else DEFAULTS['fp-contract']
    if contraction not in ('on', 'off', 'fast'):
        raise ValueError('uncertified FP contraction value: '+contraction)
    return dict(tokens=rows, optimization=optimizations[-1], dwarf=dwarfs[-1],
                switches=effective, fp_contract=contraction,
                fp_contract_source='last explicit option' if contractions else 'LLVM 22 non-CUDA/HIP default on')


def ir_settings(lines, require_recorded_options=True, arch='x86_64'):
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
    policy = classify_options(recorded_command, arch)
    flags = ['--no-default-config', '--target='+triple, '-x', 'ir', policy['optimization'],
             *BACKEND_FLAGS, '-ffp-contract='+policy['fp_contract'], '-c']
    flags += ([{1: '-fpie', 2: '-fPIE'}[pie]] if pie else
              [{1: '-fpic', 2: '-fPIC'}[pic]] if pic else ['-fno-pic', '-fno-pie'])
    return dict(triple=triple, pic_level=pic, pie_level=pie, target_cpu=sorted(cpus),
                target_features=sorted(features), flags=flags, evidence=retained,
                recorded_command=recorded_command, policy=policy)


def pic_relocations(data):
    """Reject absolute relocations in read-only allocated x86_64 sections.

    Debug relocations are excluded. Absolute 32-bit relocations against
    non-absolute symbols are also rejected in writable allocated sections.
    PC-relative relocations are not all forbidden: e.g. hidden symbols and
    .eh_frame legitimately use them. A consumer GNU ld -shared check follows.
    """
    if member_kind(data) != 'machine' or data[4:6] != b'\x02\x01' or struct.unpack_from('<H', data, 18)[0] != 62:
        raise ValueError('not x86_64 ELF64 little-endian ET_REL')
    off = struct.unpack_from('<Q', data, 40)[0]
    stride, count = struct.unpack_from('<HH', data, 58)
    if not count:
        count = struct.unpack_from('<IIQQQQIIQQ', data, off)[5]
    sections = [struct.unpack_from('<IIQQQQIIQQ', data, off+i*stride) for i in range(count)]
    checked, forbidden = 0, []
    for section in sections:
        if section[1] not in (4, 9):
            continue
        target = sections[section[7]]
        if not target[2] & 2:  # SHF_ALLOC; excludes all debug sections
            continue
        symbols = sections[section[6]]
        for pos in range(section[4], section[4]+section[5], section[9]):
            _, info = struct.unpack_from('<QQ', data, pos)
            kind, symbol_index = info & 0xffffffff, info >> 32
            symbol = struct.unpack_from('<IBBHQQ', data, symbols[4]+symbol_index*symbols[9])
            checked += 1
            # SHN_ABS references do not need runtime relocation.
            if symbol[3] != 0xfff1 and (kind in (10, 11) or (kind == 1 and not target[2] & 1)):
                forbidden.append(dict(type=kind, target_section=section[7], symbol_index=symbol_index))
    return dict(checked=checked, forbidden=forbidden)



# Experimental ARM tables: recipe-derived until the full per-architecture census
# and consumer gates complete. Never change the certified x86_64 tables above.
# Evidence: Clang Arch/ARM.cpp 275-353, 660-679; AArch64.cpp 200-266;
# BackendUtil.cpp 383-405; CodeGenModule.cpp 2729-2740, 2929-2992.
ARM_OPTIMIZATION = {'armv7l': '-Os', 'aarch64': '-O3'}
ARM_IR_TRIPLES = {'armv7l': {'thumbv7-tizen-linux-gnueabi'},
                  'aarch64': {'aarch64-tizen-linux-gnu'}}
ARM_DRIVER_TRIPLES = {'armv7l': {'armv7l-tizen-linux-gnueabi', 'thumbv7-tizen-linux-gnueabi'},
                      'aarch64': {'aarch64-tizen-linux-gnu'}}
ARM_EXACT_TOKENS = {
    'armv7l': {
        '-march=armv7-a': ('ir', 'triple/CPU/features'),
        '-mthumb': ('restore', 'driver effective triple and file-scope Thumb mode'),
        '-mfpu=neon': ('ir', 'FPU target features'),
        '-mfloat-abi=softfp': ('restore', 'calling convention and backend FloatABI'),
        '-mlittle-endian': ('restore', 'driver endianness cross-check'),
        '-mtune=cortex-a8': ('irrelevant', 'LLVM 22 ARM driver ignores mtune'),
    },
    'aarch64': {
        '-march=armv8-a+fp+simd+crc+crypto': ('ir', 'CPU target features'),
        '-mtune=cortex-a53': ('ir', 'tune-cpu attribute'),
    },
}
ARM_REQUIRED_TOKENS = {
    'armv7l': {'-march=armv7-a', '-mthumb', '-mfpu=neon', '-mfloat-abi=softfp', '-mlittle-endian'},
    'aarch64': {'-march=armv8-a+fp+simd+crc+crypto', '-mtune=cortex-a53'},
}


def arm_classify_options(argv, arch):
    """Certified policy, not arbitrary compiler-option replay; consume operands."""
    if arch not in ARM_OPTIMIZATION:
        raise ValueError('uncertified architecture: '+arch)
    rows, optimizations, dwarfs, contractions = [], [], [], []
    switches = {key: [] for key in ('function-sections', 'data-sections',
                                  'unique-section-names', 'addrsig')}
    operand_options = {'-D', '-I', '-isystem', '-resource-dir', '-o', '-MT', '-MF', '-x'}
    exact_ir = {'-fomit-frame-pointer', '-fno-omit-frame-pointer', '-fexceptions',
                '-fno-exceptions', '-fasynchronous-unwind-tables', '-funwind-tables',
                '-fno-asynchronous-unwind-tables', '-fno-unwind-tables', '-fno-common',
                '-ftrapping-math', '-fstack-protector', '-fPIC', '-fPIE', '-fpic', '-fpie',
                '-fno-pic', '-fno-pie', '-fno-semantic-interposition'}
    exact_ir.update({'-fvisibility-inlines-hidden', '-fno-visibility-inlines-hidden'})
    index = 0
    while index < len(argv):
        token = argv[index]
        category, reason = None, None
        if index == 0 and re.fullmatch(r'(?:(?:armv7l-tizen-linux-gnueabi|aarch64-tizen-linux-gnu)-)?clang(?:\+\+)?(?:-22)?', Path(token).name):
            category, reason = 'irrelevant', 'original driver path'
        elif token in ARM_EXACT_TOKENS[arch]:
            category, reason = ARM_EXACT_TOKENS[arch][token]
        elif token.startswith('--target='):
            if token.split('=', 1)[1] not in ARM_DRIVER_TRIPLES[arch]:
                raise ValueError('uncertified ARM driver target: '+token)
            category, reason = 'irrelevant', 'target cross-checked against architecture policy'
        elif token.startswith('-m'):
            raise ValueError('unclassified original command token: '+token)
        elif token in operand_options:
            if index+1 == len(argv) or argv[index+1].startswith('-'):
                raise ValueError('missing operand for '+token)
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
              or token in ('-frecord-command-line', '-frecord-gcc-switches')
              or token.startswith('-std=')):
            category, reason = 'ir', 'function/module attributes, metadata or frontend semantics'
        elif token == '-flto=thin':
            category, reason = 'irrelevant', 'pre-link bitcode format already materialized; never replay LTO'
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
    if not optimizations or optimizations[-1] != ARM_OPTIMIZATION[arch]:
        raise ValueError('uncertified last optimization: '+str(optimizations[-1:] or 'missing'))
    if not dwarfs or dwarfs[-1] != '-gdwarf-4':
        raise ValueError('uncertified last DWARF option: '+str(dwarfs[-1:] or 'missing'))
    effective = {}
    for key, values in switches.items():
        effective[key] = values[-1] if values else DEFAULTS.get(key, False)
        if not effective[key]:
            raise ValueError('original command does not enable '+key)
    contraction = contractions[-1] if contractions else DEFAULTS['fp-contract']
    if contraction not in ('on', 'off', 'fast'):
        raise ValueError('uncertified FP contraction value: '+contraction)
    missing = set(ARM_REQUIRED_TOKENS[arch]) - set(argv)
    if missing:
        raise ValueError('uncertified ARM command missing: '+repr(sorted(missing)))
    return dict(tokens=rows, optimization=optimizations[-1], dwarf=dwarfs[-1],
                switches=effective, fp_contract=contraction,
                fp_contract_source='last explicit option' if contractions else 'LLVM 22 non-CUDA/HIP default on')



def arm_ir_settings(lines, arch):
    """Read LLVM 22 textual metadata/attributes without modifying input IR."""
    lines = list(lines)
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
    if triple not in ARM_IR_TRIPLES.get(arch, set()):
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
    policy = arm_classify_options(recorded_command, arch)
    flags = ['--no-default-config', '--target='+triple, '-x', 'ir', policy['optimization'],
             *BACKEND_FLAGS, '-ffp-contract='+policy['fp_contract'], '-c']
    flags += ([{1: '-fpie', 2: '-fPIE'}[pie]] if pie else
              [{1: '-fpic', 2: '-fPIC'}[pic]] if pic else ['-fno-pic', '-fno-pie'])
    if arch == 'armv7l':
        if any('-thumb-mode' in f.split(',') or '-neon' in f.split(',') for f in features):
            raise ValueError('ARM IR features contradict certified Thumb/NEON policy')
        # Clang BackendUtil FloatABI and driver endianness are not inferred here.
        flags += ['-mfloat-abi=softfp', '-mlittle-endian', '-mthumb']
    elif arch == 'aarch64':
        tunes = set(re.findall(r'"tune-cpu"="([^"]+)"', ''.join(lines)))
        if tunes and tunes != {'cortex-a53'}:
            raise ValueError('uncertified AArch64 tune-cpu: '+repr(sorted(tunes)))
    return dict(triple=triple, pic_level=pic, pie_level=pie, target_cpu=sorted(cpus),
                target_features=sorted(features), flags=flags, evidence=retained,
                recorded_command=recorded_command, policy=policy,
                module_asm_sections=arm_module_asm_sections(lines) if arch == 'armv7l' else [])



# ELFRelocs/ARM.def:111-117; ARM getRelExpr:147-152 (GD/LD).
# AArch64.def:67-131; AArch64 getRelExpr:174-182 (TLSDESC), 184-196
# (LE), 222-234 (IE). Legacy GD/LD are ABI-defined but not implemented by
# this lld getRelExpr; permitting the object is not proof that lld can link it.
ARM_TLS_ALLOWED = {
    'armv7l': {104, 105, 106},
    'aarch64': set(range(0x200, 0x21b)) | set(range(0x230, 0x23a)) | {0x23c, 0x23d},
}
ARM_TLS_LOCAL_EXEC = {
    'armv7l': {108, 110},
    'aarch64': set(range(0x220, 0x230)) | {0x23a, 0x23b},
}
ARM_TLS_PENDING = {
    'armv7l': {90, 91, 92, 93, 107, 111, 129, 130},
    'aarch64': set(range(0x21b, 0x220)),
}


def arm_reject_triple_override(record):
    stderr = record.get('stderr', '')
    if '-Woverride-module' in stderr or 'overriding the module target triple' in stderr:
        raise ValueError('ARM conversion changed module target triple: '+stderr.strip())


def arm_module_asm_sections(lines):
    """Sections explicitly used by LLVM module-level assembler, including default .text."""
    sections, current, previous, stack = set(), '.text', None, []
    for line in lines:
        if not line.startswith('module asm '):
            continue
        match = re.fullmatch(r'module asm "(.*)"\s*', line)
        if not match:
            raise ValueError('unrecognized ARM module asm encoding')
        asm = re.sub(r'\\([0-9A-Fa-f]{2})', lambda m: chr(int(m[1], 16)), match[1])
        for statement in asm.splitlines():
            statement = statement.strip()
            m = re.match(r'\.(pushsection|section)\s+("[^"]+"|[^,\s]+)', statement)
            if m:
                if m[1] == 'pushsection':
                    stack.append(current)
                previous, current = current, m[2].strip('"')
            elif re.match(r'\.popsection\b', statement):
                if not stack:
                    raise ValueError('unbalanced ARM module asm popsection')
                previous, current = current, stack.pop()
            elif statement == '.previous':
                if previous is None:
                    raise ValueError('ARM module asm previous has no section')
                current, previous = previous, current
            elif re.match(r'\.(text|data|bss)\b', statement):
                previous, current = current, statement.split()[0]
            if statement and not statement.startswith(('#', '@', '//')):
                sections.add(current)
    if stack:
        raise ValueError('unbalanced ARM module asm pushsection')
    return sorted(sections)


def arm_reference_flags(settings):
    """Same IR through original driver flags; remove only LTO/action/input/dependency paths."""
    argv = settings['recorded_command'][1:]
    kept, i = [], 0
    paired = {'-D', '-I', '-isystem', '-resource-dir'}
    removed = {'-o', '-MT', '-MF', '-x'}
    while i < len(argv):
        token = argv[i]
        if token in paired:
            kept.extend(argv[i:i+2]); i += 2
        elif token in removed:
            i += 2
        elif token in ('-c', '-MD', '-flto=thin'):
            i += 1
        elif not token.startswith('-') and re.search(r'\.(?:c|cc|cpp|cxx|C|ii|i|bc|ll|o|obj|s|S)$', token):
            i += 1
        else:
            kept.append(token); i += 1
    if '-mthumb' not in kept or any(x.startswith('-flto') for x in kept):
        raise ValueError('uncertified ARM reference driver flags')
    return ['--no-default-config', *kept, '-x', 'ir', '-c']


def arm_mapping_modes(data, selected):
    """ELF mapping symbols give ARM/Thumb/data transitions in module-asm sections."""
    if member_kind(data) != 'machine' or data[4:6] != b'\x01\x01' or struct.unpack_from('<H', data, 18)[0] != 40:
        raise ValueError('ARM mapping gate requires little-endian ELF32 ET_REL')
    off = struct.unpack_from('<I', data, 32)[0]
    stride, count, names = struct.unpack_from('<HHH', data, 46)
    if not count:
        count = struct.unpack_from('<IIIIIIIIII', data, off)[5]
    sections = [struct.unpack_from('<IIIIIIIIII', data, off+i*stride) for i in range(count)]
    if names == 65535:
        names = sections[0][6]
    strings = sections[names]; names_data = data[strings[4]:strings[4]+strings[5]]
    found = {i: cstring(names_data, s[0]) for i, s in enumerate(sections)
             if cstring(names_data, s[0]) in selected and s[2] & 4 and s[5]}
    maps = {i: [] for i in found}
    for section in sections:
        if section[1] != 2:
            continue
        string_sec = sections[section[6]]; strings = data[string_sec[4]:string_sec[4]+string_sec[5]]
        for pos in range(section[4], section[4]+section[5], section[9]):
            name, value, size, info, other, shndx = struct.unpack_from('<IIIBBH', data, pos)
            text = cstring(strings, name)
            if shndx in maps and re.fullmatch(r'\$[atd](?:\..*)?', text):
                maps[shndx].append((value, text[1]))
    result = {}
    for index, name in found.items():
        modes = []
        for _, mode in sorted(maps[index]):
            if not modes or modes[-1] != mode:
                modes.append(mode)
        if not modes:
            raise ValueError('ARM module asm section lacks mapping symbols: '+name)
        result[name] = modes
    return result


def arm_thumb_gate(compiler, source, target, settings, command):
    """ARM32-only reference compile; x86 never executes this extra command."""
    reference = source.parent/'thumb-reference.o'
    record = command.run([compiler, *arm_reference_flags(settings), str(source), '-o', str(reference)],
                         source.parent/'thumb-reference')
    arm_reject_triple_override(record)
    def signature(path, label):
        output = source.parent/(label+'.attributes.txt')
        with output.open('wb') as stream:
            command.run(['readelf', '-AW', str(path)], source.parent/(label+'-readelf'), stdout=stream)
        text = output.read_text()
        attributes = {}
        for key in ('Tag_ARM_ISA_use', 'Tag_THUMB_ISA_use', 'Tag_ABI_VFP_args'):
            values = re.findall(r'^\s*'+key+r': (.*)$', text, re.M)
            if len(values) > 1:
                raise ValueError('multiple ARM attribute values: '+key)
            attributes[key] = values[0] if values else 'default(0)'
        return dict(attributes=attributes, module_asm_modes=arm_mapping_modes(path.read_bytes(), settings['module_asm_sections']))
    actual = signature(target, 'converted'); expected = signature(reference, 'reference')
    result = dict(actual=actual, expected=expected, equal=actual == expected,
                  no_function_attributes=not settings['target_cpu'] and not settings['target_features'],
                  reference_sha256=sha(reference), reference_command=record)
    atomic_json(source.parent/'thumb-gate.json', result)
    if not result['equal']:
        raise ValueError('ARM Thumb/ABI/module-asm mode differs from original-flags IR reference: '+str(target))
    reference.unlink()
    return result


def arm_pic_relocations(data, arch):
    """Experimental, fail-closed ARM PIC policy for REL/RELA input sections.

    LLVM ELFRelocs/{ARM,AArch64}.def and lld/ELF/Arch/{ARM,AArch64}.cpp
    define the numbers and expressions. Unknown/TLS/platform policies require
    separate certification. Low-12 address fragments are not full addresses.
    """
    bits, machine = (1, 40) if arch == 'armv7l' else (2, 183)
    if (arch not in ARM_OPTIMIZATION or member_kind(data) != 'machine' or
            data[4:6] != bytes([bits, 1]) or struct.unpack_from('<H', data, 18)[0] != machine):
        raise ValueError('not certified '+arch+' little-endian ET_REL')
    if bits == 1:
        off = struct.unpack_from('<I', data, 32)[0]
        stride, count = struct.unpack_from('<HH', data, 46)
        sfmt, symfmt = '<IIIIIIIIII', '<IIIBBH'
    else:
        off = struct.unpack_from('<Q', data, 40)[0]
        stride, count = struct.unpack_from('<HH', data, 58)
        sfmt, symfmt = '<IIQQQQIIQQ', '<IBBHQQ'
    if stride < struct.calcsize(sfmt) or not off:
        raise ValueError('invalid ARM ELF section header')
    if not count:
        count = struct.unpack_from(sfmt, data, off)[5]
    sections = [struct.unpack_from(sfmt, data, off+i*stride) for i in range(count)]
    if arch == 'armv7l':
        absolute = {2,5,6,7,8,38,43,44,47,48,55,132,133,134,135}
        narrow = {5,6,7,8}
        # NONE, relative code/data, GOT/PLT and EHABI PREL31. TARGET2/BASE_ABS
        # remain uncertified; the separate TLS tables are explicit and bounded.
        allowed = {0,1,3,4,10,11,24,25,26,27,28,29,30,40,42,45,46,49,50,
                   51,52,53,54,56,57,58,59,60,61,62,63,64,65,66,67,68,69,
                   96,97,98,102,103}
    else:
        absolute = {0x101,0x102,0x103,0x13d,0x244} | set(range(0x107,0x111))
        narrow = {0x102,0x103}
        # ADRP+LO12, PREL, branches and GOT fragments; no TLS/PAuth default.
        allowed = {0,0x100,0x104,0x105,0x106,0x111,0x112,0x113,0x114,
                   0x115,0x116,0x117,0x118,0x11a,0x11b,0x11c,0x11d,0x11e,
                   0x11f,0x120,0x121,0x122,0x123,0x124,0x125,0x12b,
                   0x12c,0x12d,0x12e,0x12f,0x130,0x131,0x132,0x133,
                   0x134,0x135,0x136,0x137,0x138,0x139,0x13a,0x13b}
    tls_allowed = ARM_TLS_ALLOWED[arch]
    tls_forbidden = ARM_TLS_LOCAL_EXEC[arch]
    checked, forbidden, types = 0, [], Counter()
    for section in sections:
        if section[1] not in (4, 9):
            continue
        target = sections[section[7]]
        symidx = section[6]; symbols = sections[symidx]
        if symbols[1] != 2 or symbols[9] < struct.calcsize(symfmt):
            raise ValueError('invalid ARM relocation symbol table')
        xindex = [s for s in sections if s[1] == 18 and s[6] == symidx]
        rfmt = ('<IIi' if section[1] == 4 else '<II') if bits == 1 else ('<QQq' if section[1] == 4 else '<QQ')
        if section[9] < struct.calcsize(rfmt) or section[5] % section[9]:
            raise ValueError('invalid ARM relocation stride')
        for pos in range(section[4], section[4]+section[5], section[9]):
            rel = struct.unpack_from(rfmt, data, pos); info = rel[1]
            kind, si = (info & 255, info >> 8) if bits == 1 else (info & 0xffffffff, info >> 32)
            if si*symbols[9] >= symbols[5]:
                raise ValueError('ARM relocation symbol index outside table')
            sym = struct.unpack_from(symfmt, data, symbols[4]+si*symbols[9])
            ndx = sym[5] if bits == 1 else sym[3]
            if ndx == 0xffff:
                if len(xindex) != 1 or si*4 >= xindex[0][5]:
                    raise ValueError('missing extended ARM symbol section index')
                ndx = struct.unpack_from('<I', data, xindex[0][4]+4*si)[0]
            if kind in tls_forbidden:
                # Reject here, independently of the caller's PIC Level check.
                raise ValueError('forbidden '+arch+' TLS local-exec relocation '+str(kind)+' at section '+str(section[7]))
            if kind in ARM_TLS_PENDING[arch]:
                raise ValueError('uncertified '+arch+' TLS relocation '+str(kind)+' at section '+str(section[7]))
            if not target[2] & 2:
                continue
            checked += 1; types[kind] += 1
            if kind not in absolute | allowed | tls_allowed:
                raise ValueError('uncertified '+arch+' relocation '+str(kind)+' at section '+str(section[7]))
            if ndx != 0xfff1 and (kind in narrow or kind in absolute and not target[2] & 1):
                forbidden.append(dict(type=kind, target_section=section[7], symbol_index=si))
    return dict(checked=checked, forbidden=forbidden, types=dict(types))


def policy_for_arch(arch):
    if arch == 'x86_64':
        # These are the original functions; the ARM branches are unreachable.
        return dict(settings=lambda lines: ir_settings(lines, arch=arch), relocations=pic_relocations)
    if arch in ARM_OPTIMIZATION:
        return dict(settings=lambda lines: arm_ir_settings(lines, arch),
                    relocations=lambda data: arm_pic_relocations(data, arch))
    raise ValueError('uncertified architecture: '+arch)


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
        self.check()
        prefix = Path(prefix)
        timing, log = prefix.with_suffix('.time'), prefix.with_suffix('.log')
        command = ['/usr/bin/prlimit', '--as='+str(self.address_space_bytes), '--core=0',
                   '--', *map(str, argv)]
        start = time.monotonic()
        reason, status, usage, reaped = None, None, None, False
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
                    if now-start >= self.timeout and not reaped:
                        reason = 'command timeout after '+str(self.timeout)+' s'
                        self.cancel(reason)
                    if self.stop.is_set():
                        reason = reason or 'cancelled after command failure'
                        if now-self.cancelled_at >= 3:
                            try:
                                os.killpg(child.pid, signal.SIGKILL)
                            except ProcessLookupError:
                                pass
                    if not reaped:
                        pid, child_status, child_usage = os.wait4(child.pid, os.WNOHANG)
                        if pid:
                            status, usage, reaped = child_status, child_usage, True
                            child.returncode = os.waitstatus_to_exitcode(status)
                            if child.returncode:
                                reason = reason or 'command failed'
                                self.cancel(reason)  # Includes descendants after the leader exits.
                    if reaped and (not self.stop.is_set() or now-self.cancelled_at >= 3):
                        break
                    time.sleep(0.05)
            finally:
                if not reaped:
                    self.cancel()
                    remaining = 3-(time.monotonic()-self.cancelled_at)
                    if remaining > 0:
                        time.sleep(remaining)
                    try:
                        os.killpg(child.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    _, status, usage = os.wait4(child.pid, 0)
                    child.returncode = os.waitstatus_to_exitcode(status)
                with self.lock:
                    self.children.discard(child)
        elapsed, rc = time.monotonic()-start, child.returncode
        record = dict(argv=list(map(str, argv)), bounded_argv=command, pid=child.pid,
                      elapsed_seconds=elapsed, exit=rc, wall=elapsed,
                      user=usage.ru_utime, sys=usage.ru_stime, max_rss_kib=usage.ru_maxrss,
                      accounting='os.wait4(WNOHANG); Linux ru_maxrss is KiB',
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
    version = output/'compiler-version.txt'
    with version.open('wb') as stream:
        command.run([compiler, '--version'], output/'compiler-version-command', stdout=stream)
    text = version.read_text()
    match = re.search(r'clang version (\d+)\.', text)
    if not match or int(match[1]) != CERTIFIED_LLVM_MAJOR:
        raise ValueError('uncertified compiler major (required 22): '+text.strip())
    return dict(compiler=str(compiler), version=text, compiler_sha256=sha(compiler),
                disassembler=str(disassembler), nm=str(nm))


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
            address_space_bytes=4*1024**3, command=None):
    root, output, build = Path(root).resolve(), Path(output).resolve(), Path(build).resolve()
    policy = policy_for_arch(arch)
    if jobs < 1 or address_space_bytes < 1:
        raise ValueError('invalid architecture or resource parameters')
    reset_evidence(root, output, build)
    command = command or Commands(address_space_bytes)
    summary = dict(started=time.time(), input_root=str(root), output_root=str(output),
                   arch=arch, workers=jobs, as_bytes=address_space_bytes, archives=[],
                   status='CONVERTING', missing_symbols_by_type={})
    def save():
        atomic_json(output/'summary.json', summary)
    save()
    old_handlers = {sig: signal.signal(sig, command.interrupted) for sig in (signal.SIGTERM, signal.SIGINT)}
    try:
        summary['tools'] = validate_tools(build, Path(compiler), Path(disassembler), Path(nm), command, output)
        archives = [(archive, validate_archive(archive)) for archive in sorted(root.rglob('*.a'))]
        summary['scanned_archives'] = len(archives)
        summary['native_archives_skipped'] = sum(not data['bitcode'] for archive, data in archives)
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
                    relocs = policy['relocations'](target.read_bytes())
                    if arch != 'x86_64' and relocs['forbidden']:
                        raise ValueError('non-PIC original ARM member: '+str(target))
                    atomic_json(source.parent/'relocations.json', relocs)
                    return dict(ordinal=member['ordinal'], name=member['name'], preserved=True,
                                relocation_check=relocs)
                text_ir = source.with_suffix('.ll')
                with text_ir.open('wb') as out:
                    command.run([disassembler, str(source), '-o', '-'], source.parent/'disassemble', stdout=out)
                with text_ir.open() as lines:
                    settings = policy['settings'](lines)
                atomic_json(source.parent/'ir-settings.json', settings)
                text_ir.unlink()
                record = command.run([compiler, *settings['flags'], str(source), '-o', str(target)], source.parent/'convert')
                if arch in ARM_OPTIMIZATION:
                    arm_reject_triple_override(record)
                if arch == 'armv7l':
                    record['arm_thumb_gate'] = arm_thumb_gate(compiler, source, target, settings, command)
                data = target.read_bytes()
                relocs = policy['relocations'](data)
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
            address_space_bytes=4*1024**3):
    root, output = Path(root).resolve(), Path(output).resolve()
    command = Commands(address_space_bytes)
    old_handlers = {sig: signal.signal(sig, command.interrupted) for sig in (signal.SIGTERM, signal.SIGINT)}
    result = None
    try:
        print('NATIVE_ARCHIVES_BEGIN', time.time(), flush=True)
        result = convert(root, output, compiler, disassembler, nm, build, arch, jobs, address_space_bytes, command)
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


def install_main():
    parser = argparse.ArgumentParser(description='Experimental ARM policy dispatch; x86_64 policy preserved')
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--arch', choices=['x86_64', 'armv7l', 'aarch64'], required=True)
    parser.add_argument('--compiler', type=Path, required=True)
    parser.add_argument('--disassembler', type=Path, required=True)
    parser.add_argument('--nm', type=Path, required=True)
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--address-space-bytes', type=int, default=4*1024**3)
    args = parser.parse_args()
    install(args.root, args.evidence, args.compiler.resolve(), args.disassembler.resolve(),
            args.nm.resolve(), args.build, args.arch, args.jobs, args.address_space_bytes)


if __name__ == '__main__':
    install_main()
