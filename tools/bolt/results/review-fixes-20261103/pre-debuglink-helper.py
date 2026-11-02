#!/usr/bin/env python3
"""Tizen clang BOLT gates. Python >= 3.9; shell commands use POSIX sh.

Maintenance notes (fail closed; preserve actual/expected values and logs):
- No disk-space admission thresholds: profile, BOLT and clang sizes change,
  so fixed budgets become stale. Record actual allocation/free space only;
  diagnose a failed step from its errno/log and estimate from this build.
  disk-report is best effort; disk-diagnose is read-only. Neither is a gate.
- Tool-version remedy: verify provenance; for an intended LLVM upgrade update
  CERTIFIED and recertify, otherwise disable BOLT. Do not use substring matches.
- Profile-SHA remedy: verify the binary Source and decompressed SHA first;
  a SHA mismatch alone does not establish that the profile is stale.
- Unapproved-task remedy: inspect configuration and dirty causes. Review the
  saved Ninja closure, regenerate the independent description JSON and exact
  whitelist only after review, then recertify. Never expand it automatically.
- Matching remedy: verify input ELF/tool/profile identity; retrain the profile
  or disable BOLT when R or S/N exceeds 5%. Never raise the threshold or enable
  infer-stale to pass a failing gate.

LLVM upgrade: review CERTIFIED.llvm_version, bolt_version, profile_sha256,
bolt_task_count and tf_refresh_task_count (PROFILE_SHA is an alias), OPTIONS,
and both task-description sets. Recertify fixtures, static graph plus actual
Ninja plans/build logs and TF archive SHA, ON/OFF debug/release macro and post
chains, install ordering/root identity, ELF security, tiny targets, full object
comparisons, RPM/DWARF payload differences and three-target/holdout performance.
Static graphs do not load .ninja_deps/depfiles or establish full dirty state.

Rollback: --without clang_bolt locally; where build arguments cannot change,
change the x86_64 %bcond_without clang_bolt to %bcond_with clang_bolt in a new
spec commit. BOLT Sources/BuildRequires then disable together. Also restore
matching accel/worker binaries and repository snapshots; verify their hashes.

Profile retraining is offline, never part of an RPM build: preserve a relinked
emit-relocs/strip-debug input and matching BOLT/runtime identities, instrument
with one BOLT thread and a fresh PID-suffixed profile prefix. Reuse the recorded
13 ARM workloads (A/B/C generator plus ten real TUs) and ten AArch64 TUs, their
exact flags/sysroots/resource directory and input hashes; exclude holdouts.
The existing collect_bolt_profile.py and extend_bolt_profile_aarch64.py scripts
collect these 13+10 profiles and merge explicit paths with merge-fdata. Compress
the new profile Source, update its SHA, then repeat matching, object, security,
package and performance gates. Historical instrumentation requires
resource planning outside package builds; local resource/lock rules never
enter this release helper.
Retain ordinary/pre-strip BOLT ELFs, rewrite/identity records, final RPM/accel
SHA and Build-ID for crash localization; the shipped clang is fully stripped.
"""
import argparse
import collections
import shlex
import hashlib
import json
import lzma
import mmap
import os
from pathlib import Path
import re
import shutil
import signal
import stat
import struct
import subprocess
import sys
import tempfile
import time

CERTIFIED = {'llvm_version': '22.1.8', 'bolt_version': 'LLVM version 22.1.8',
             'profile_sha256': 'd9b132f9430dfed32e080c65b4422bd76eba4a9c2101a2b18a7f66c94133b326',
             'bolt_task_count': 111, 'tf_refresh_task_count': 2}
PROFILE_SHA = CERTIFIED['profile_sha256']
BUILD_SUCCESS = 'BOLT_NINJA_EXIT_0'
REGEN_ERROR = ('dry-run shows "Re-running CMake..."; build.ninja still needs regeneration '
               'after the BOLT configure, so the real plan is not visible')


def preflight():
    require(sys.version_info >= (3, 9), 'Python actual=%s expected=>=3.9' % (tuple(sys.version_info[:3]),))
    required = ('waitid', 'waitstatus_to_exitcode', 'P_PID', 'WEXITED', 'WNOHANG', 'WNOWAIT', 'CLD_EXITED')
    missing = [name for name in required if not hasattr(os, name)]
    require(not missing, 'Python os interfaces actual=missing %s expected=%s' % (missing, required))
    return {'preflight_pass': True, 'python': list(sys.version_info[:3]), 'os_interfaces': list(required)}


def certified():
    return {**CERTIFIED, 'whitelist_counts': {'bolt': len(BOLT_TASK_DESCRIPTIONS),
                                             'tf_refresh': len(TF_REFRESH_DESCRIPTIONS)}}


def profile_identity(path):
    actual = digest(path)
    require(actual == PROFILE_SHA, 'profile SHA actual=%s expected=%s; remedy: first verify the Source identity; '
            'do not assume the profile is stale' % (actual, PROFILE_SHA))

OPTIONS = ['-reorder-blocks=ext-tsp', '-reorder-functions=cdsort', '-split-functions',
           '-split-all-cold', '-split-eh', '-dyno-stats', '--thread-count=1', '-stale-threshold=5', '-use-old-text']
TRIPLES = ['armv7l-tizen-linux-gnueabi', 'aarch64-tizen-linux-gnu', 'x86_64-tizen-linux-gnu']
TINY = ('unsigned bolt_probe(unsigned x, unsigned y) { return (x * 33u) ^ (y + (x >> 3)); }\n'
        'int bolt_branch(int x) { return x < 0 ? -x : x * 7 + 1; }\n')

class GateError(RuntimeError):
    pass

def require(ok, message):
    if not ok:
        raise GateError(message)

def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

def atomic_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name+'.new')
    try:
        with tmp.open('w',encoding='utf-8') as stream:
            require(stream.write(text) == len(text), 'short text write: '+str(tmp))
            stream.flush(); os.fsync(stream.fileno())
        os.replace(tmp,path)
    except BaseException as error:
        try:
            error.bolt_write_bytes=len(text.encode('utf-8'));error.bolt_write_path=str(path)
        except Exception:pass
        try: tmp.unlink()
        except OSError: pass
        raise


def save(path, value):
    atomic_text(path, json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def proc_stat(path):
    text = Path(path).read_text()
    try:
        pid = int(text.split(' ', 1)[0])
        fields = text.rsplit(')', 1)[1].split()
        require(len(fields) >= 18, 'short process stat: '+str(path))
        return pid, fields[0], int(fields[2]), int(fields[17])
    except (ValueError, IndexError) as error:
        raise GateError('malformed process stat: '+str(path)) from error

def live_group_members(group):
    require(proc_stat('/proc/self/stat')[0] == os.getpid(), 'PID namespace mismatch in /proc/self/stat')
    members = []
    try:
        with os.scandir('/proc') as entries:
            for entry in entries:
                if not entry.name.isdecimal():
                    continue
                try:
                    pid, state, pgrp, threads = proc_stat('/proc/'+entry.name+'/stat')
                except (FileNotFoundError, ProcessLookupError):
                    continue
                if pgrp == group and (state not in ('Z', 'X') or threads > 1):
                    members.append((pid, state))
    except OSError as error:
        raise GateError('cannot enumerate/read process group: '+str(error)) from error
    return sorted(members)

def wait_group_exit(group, timeout=10):
    deadline = time.monotonic()+timeout
    while True:
        members = live_group_members(group)
        if not members:
            return
        require(time.monotonic() < deadline, 'process group %d still alive: %s' %
                (group, ', '.join('%d:%s' % item for item in members)))
        time.sleep(.02)

def peek_child_exit(process, timeout):
    deadline = time.monotonic()+timeout if timeout is not None else None
    while True:
        status = os.waitid(os.P_PID, process.pid, os.WEXITED | os.WNOHANG | os.WNOWAIT)
        if status is not None:
            return status.si_status if status.si_code == os.CLD_EXITED else -status.si_status
        if deadline is not None and time.monotonic() >= deadline:
            raise subprocess.TimeoutExpired(str(process.pid), timeout)
        time.sleep(.01)

def reap_child(process, timeout=1):
    deadline = time.monotonic()+timeout
    while True:
        pid, status = os.waitpid(process.pid, os.WNOHANG)
        if pid:
            process.returncode = os.waitstatus_to_exitcode(status)
            return process.returncode
        require(time.monotonic() < deadline, 'leader %d was not reaped before deadline' % process.pid)
        time.sleep(.01)

def call(argv, log, cwd=None, timeout=300):
    log = Path(log); log.parent.mkdir(parents=True, exist_ok=True)
    process = None; reaped = False; primary = None
    try:
        previous = signal.getsignal(signal.SIGCHLD)
        if previous != signal.SIG_DFL:
            signal.signal(signal.SIGCHLD, signal.SIG_DFL)
        save(log.with_suffix(log.suffix+'.argv.json'),
             {'argv': list(map(str, argv)), 'cwd': str(cwd) if cwd else None,
              'SIGCHLD_original': str(previous), 'SIGCHLD_reset_to_default': previous != signal.SIG_DFL})
        with log.open('wb') as output:
            process = subprocess.Popen(list(map(str, argv)), cwd=cwd, stdout=output,
                                       stderr=subprocess.STDOUT, start_new_session=True)
            rc = peek_child_exit(process, timeout)
            if rc != 0:
                primary = 'COMMAND_FAILED rc=%d: %s' % (rc, argv[0])
                raise GateError(primary)
            require(reap_child(process) == rc, 'child exit status changed while reaping')
            reaped = True
        text = log.read_text(errors='replace')
        metadata = log.with_suffix(log.suffix+'.argv.json')
        invocation = json.loads(metadata.read_text())
        save(metadata, dict(invocation,completed=True,rc=0))
        return text
    except BaseException as error:
        if primary is None:
            primary = ('TIMEOUT: ' if isinstance(error, subprocess.TimeoutExpired) else 'COMMAND_ERROR: ')+str(error)
        cleanup = []
        if process is not None and not reaped:
            # Keep the un-reaped leader as a PGID anchor until group cleanup ends.
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            except Exception as failure:
                cleanup.append(str(failure))
            try:
                wait_group_exit(process.pid, 10)
            except Exception as failure:
                cleanup.append(str(failure))
            try:
                reap_child(process, 1)
            except Exception as failure:
                cleanup.append(str(failure))
        if isinstance(error, (KeyboardInterrupt, SystemExit)):
            raise
        message = primary+' (see '+str(log)+')'
        if cleanup:
            message += '; cleanup error: '+'; '.join(cleanup)
        failure = GateError(message)
        failure.bolt_log = str(log)
        raise failure from error

def profile_unpack(source, output):
    output = Path(output)
    require(not output.exists(), 'profile output must be new')
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with lzma.open(source, 'rb') as src, output.open('xb') as dst:
            shutil.copyfileobj(src, dst, 1024 * 1024)
        profile_identity(output)
    except Exception:
        if output.exists():
            try: output.unlink()
            except OSError: pass
        raise
    return {'sha256': PROFILE_SHA, 'bytes': output.stat().st_size,
            'compressed_sha256': digest(source)}

def quote(value):
    return "'" + str(value).replace("'", "'\\''") + "'"

def replay_script(original, output, dependency, cache=None):
    original = original.strip()
    require('\n' not in original and original.startswith(': && ') and original.endswith(' && :'),
            'unexpected link edge framing')
    body = original[5:-5]
    args = shlex.split(body)
    require(not any(arg.startswith('@') or (arg.startswith('-Wl,') and any(part.startswith('@') for part in arg[4:].split(','))) for arg in args),
            'link edge uses a response file; rsp auditing is not implemented')
    require(not any(c in body for c in ';`|&<>') and '$(' not in body,
            'unsupported shell syntax in link edge')
    require(not re.search(r'(?<!\\)\$', body), 'unknown shell substitution')
    require('--emit-relocs' not in body and '--strip-debug' not in body, 'edge already has BOLT flags')
    old_out = '-o bin/clang-22 '
    old_dep = '--dependency-file=tools/clang/tools/driver/CMakeFiles/clang.dir/link.d'
    require(body.count(old_out) == 1 and body.count(old_dep) == 1, 'non-unique clang output/depfile')
    require(not any(x in body for x in ['--Map', '-Map', '--save-temps', '--time-trace']),
            'unregistered additional linker output')
    caches = re.findall(r'--thinlto-cache-dir=([^\s]+)', body)
    require(len(caches) == 1 and caches[0].startswith('/') and not any(c in caches[0] for c in '\"\'`$'), 'non-unique or unsupported ThinLTO cache')
    if cache is not None:
        require(str(cache) != caches[0], 'explicit cache override must be isolated')
        body = body.replace('--thinlto-cache-dir='+caches[0], '--thinlto-cache-dir='+quote(cache), 1)
    body = body.replace(old_out, '-o ' + quote(output) + ' ', 1)
    body = body.replace(old_dep, '--dependency-file=' + quote(dependency), 1)
    flags = ' -Wl,--emit-relocs'
    return '#!/bin/sh\nset -eu\n' + body + flags + '\n'

def match_counts(text, argv, successful, trusted_tool):
    require(successful and trusted_tool, 'untrusted tool or incomplete/failed rewrite log')
    require(not any('infer-stale' in str(x) for x in argv), 'infer-stale forbidden')
    nrows = re.findall(r'^BOLT-INFO: (\d+) out of (\d+) functions in the binary .*have non-empty execution profile$', text, re.M)
    srows = re.findall(r'^BOLT-(?:WARNING|ERROR): (\d+) \([^\n]*\) functions? have invalid \(possibly stale\) profile\.', text, re.M)
    urows = re.findall(r'^BOLT-INFO: profile for (\d+) objects was ignored$', text, re.M)
    qrows = re.findall(r'^BOLT-INFO: (\d+) functions? with profile could not be optimized$', text, re.M)
    require('invalid (possibly stale) profile' not in text or bool(srows), 'malformed stale counter')
    require('objects was ignored' not in text or bool(urows), 'malformed unused counter')
    require('with profile could not be optimized' not in text or bool(qrows), 'malformed non-simple counter')
    require(len(nrows) == 1 and len(srows) <= 1 and len(urows) <= 1 and len(qrows) <= 1,
            'missing/duplicate profile counters')
    n, m = map(int, nrows[0]); s = int(srows[0]) if srows else 0
    u = int(urows[0]) if urows else 0; q = int(qrows[0]) if qrows else 0
    require(n > 0 and m >= n and s <= n, 'invalid N/M/S')
    # Absent optional zero-counter lines are allowed only for this authenticated success format.
    require(100 * (s + u) <= 5 * (n + u), 'profile R actual=%s expected=<=0.05; remedy: verify input identity, then retrain the profile or disable BOLT; never raise the threshold' % ((s+u)/(n+u)))
    require(100 * s <= 5 * n, 'profile S/N actual=%s expected=<=0.05; remedy: verify input identity, then retrain the profile or disable BOLT; never raise the threshold' % (s/n))
    return {'N': n, 'M': m, 'S': s, 'U': u, 'Q': q,
            'R': (s + u) / (n + u), 'S_over_N': s / n}

class ELF:
    """ELF64 little-endian reader. No whole-file loads; semantic symbol/relocation records."""
    def __init__(self, path):
        self.path = Path(path); self.f = self.path.open('rb')
        if os.fstat(self.f.fileno()).st_size < 64:
            self.f.close(); raise GateError('truncated ELF header')
        self.mm = mmap.mmap(self.f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            require(self.mm[:6] == b'\x7fELF\x02\x01', 'expected ELF64 little endian')
            h = self.unpack('<16sHHIQQQIHHHHHH', 0)
            require(h[0][6] == 1 and h[3] == 1 and h[8] == 64, 'invalid ELF header version/size')
            require(h[1] in (2, 3), 'expected executable or shared ELF type')
            self.elf_type = h[1]; self.machine = h[2]; self.entry = h[4]
            phoff, shoff, phentsize, phnum, shentsize, shnum, stridx = h[5], h[6], h[9], h[10], h[11], h[12], h[13]
            require(shentsize == 64 and shnum > 0 and stridx < shnum, 'unsupported section numbering')
            self.sections = [self.unpack('<IIQQQQIIQQ', shoff + i * 64) for i in range(shnum)]
            for section in self.sections:
                if section[1] != 8:
                    self.range(section[4], section[5])
            names = self.sections[stridx]
            require(names[1] == 3, 'section name table is not STRTAB')
            self.names = [self.string(names[4], names[5], s[0]) for s in self.sections]
            self.by_name = dict(zip(self.names, self.sections))
            require(len(self.by_name) == len(self.names), 'duplicate section name')
            self.loads = []; self.phdrs = []
            for i in range(phnum):
                require(phentsize == 56, 'unsupported program header')
                p = self.unpack('<IIQQQQQQ', phoff + i * phentsize)
                self.phdrs.append(p)
                if p[0] == 1:
                    require(p[5] <= p[6], 'LOAD filesz exceeds memsz')
                    self.range(p[2], p[5])
                    self.loads.append(p)
        except Exception:
            self.close(); raise
    def close(self):
        self.mm.close(); self.f.close()
    def unpack(self, fmt, pos):
        require(pos >= 0 and pos + struct.calcsize(fmt) <= len(self.mm), 'ELF range error')
        return struct.unpack_from(fmt, self.mm, pos)
    def range(self, offset, size):
        require(0 <= offset <= len(self.mm) and 0 <= size <= len(self.mm)-offset, 'ELF content range error')
    def string(self, offset, size, start):
        self.range(offset, size)
        require(0 <= start < size, 'ELF string index error')
        end = self.mm.find(b'\0', offset + start, offset + size)
        require(end >= 0, 'unterminated ELF string')
        return self.mm[offset + start:end].decode('utf-8', errors='surrogateescape')
    def symbols(self, index):
        sec = self.sections[index]; require(sec[1] in (2, 11), 'not a symbol table')
        require(sec[9] == 24 and sec[5] % 24 == 0 and sec[6] < len(self.sections), 'bad symtab')
        strings = self.sections[sec[6]]; require(strings[1] == 3, 'symbol names are not STRTAB'); result = []
        for off in range(sec[4], sec[4] + sec[5], 24):
            name, info, other, shndx, value, size = self.unpack('<IBBHQQ', off)
            require(shndx < len(self.sections) or shndx in (0xfff1, 0xfff2), 'invalid symbol shndx: actual=%d expected=section index, SHN_ABS or SHN_COMMON' % shndx)
            target = self.names[shndx] if shndx < len(self.names) else 'RESERVED:%d' % shndx
            result.append((self.string(strings[4], strings[5], name), info, other, target, value, size, shndx))
        return result
    def audit(self, final=False):
        require(self.machine == 62 and self.loads, 'not executable native x86_64 ELF')
        require(any(p[1] & 1 and p[3] <= self.entry < p[3] + p[5] for p in self.loads),
                'entry not inside executable LOAD')
        require(not any('debug' in n.lower() for n in self.names), 'BOLT clang contains a debug section')
        require('.gdb_index' not in self.by_name, 'BOLT clang contains a debug index')
        if final:
            require('.symtab' not in self.by_name and '.note.bolt_info' not in self.by_name, 'candidate is not fully stripped')
        else:
            require('.note.bolt_info' in self.by_name, 'missing BOLT note')
        return {'entry': self.entry, 'loads': self.loads, 'bolt_sections': [n for n in self.names if '.bolt' in n]}

def security_properties(path):
    e = ELF(path)
    try:
        def content(section):
            require(section[1] != 8, 'NOBITS section cannot contain security metadata')
            return bytes(e.mm[section[4]:section[4]+section[5]])
        def headers(kind):
            return [p for p in e.phdrs if p[0] == kind]
        def header_values(kind, payload=False):
            values = []
            for p in headers(kind):
                value = {'flags': p[1]}
                if kind == 0x6474e552:
                    require(p[5] <= p[6], 'RELRO filesz exceeds memsz');e.range(p[2], p[5])
                    value.update(vaddr=p[3], filesz=p[5], memsz=p[6])
                if payload:
                    e.range(p[2], p[5])
                    value['content_hex'] = bytes(e.mm[p[2]:p[2]+p[5]]).hex()
                values.append(value)
            return values
        interp = [e.string(p[2], p[5], 0) for p in headers(3)]
        dynamic = e.by_name.get('.dynamic'); needed = []; flags = {}; bind_now = False; search_paths = {}
        if dynamic:
            require(dynamic[1] == 6 and dynamic[9] == 16 and dynamic[5] % 16 == 0 and dynamic[6] < len(e.sections), 'invalid dynamic table')
            strings = e.sections[dynamic[6]]
            require(strings[1] == 3, 'dynamic strings are not STRTAB')
            terminated = False
            for offset in range(dynamic[4], dynamic[4]+dynamic[5], 16):
                tag, value = e.unpack('<qQ', offset)
                if tag == 0:
                    terminated = True
                    break
                if tag in (15, 29):
                    key = 'DT_RPATH' if tag == 15 else 'DT_RUNPATH'
                    require(key not in search_paths, 'duplicate dynamic search path tag: '+key)
                    search_paths[key] = e.string(strings[4], strings[5], value)
                if tag == 24:
                    bind_now = True
                if tag == 1:
                    needed.append(e.string(strings[4], strings[5], value))
                if tag in (30, 0x6ffffffb):
                    require(str(tag) not in flags, 'duplicate dynamic flags')
                    flags[str(tag)] = value
            require(terminated, 'unterminated dynamic table')
        syms = e.symbols(e.names.index('.dynsym')) if '.dynsym' in e.names else []
        vers = e.by_name.get('.gnu.version')
        require(not vers or (vers[1] == 0x6fffffff and vers[5] % 2 == 0), 'invalid versym table')
        version_values = list(struct.unpack('<'+'H'*(vers[5]//2), content(vers))) if vers else []
        verneed = e.by_name.get('.gnu.version_r'); needs = []; version_names = {0: ('', 'LOCAL'), 1: ('', 'GLOBAL')}
        if verneed:
            require(verneed[1] == 0x6ffffffe and verneed[6] < len(e.sections), 'invalid verneed table')
            strings = e.sections[verneed[6]]
            require(strings[1] == 3, 'verneed names are not STRTAB')
            cursor = 0; seen = set()
            while True:
                require(cursor not in seen and 0 <= cursor <= verneed[5]-16, 'bad verneed record')
                seen.add(cursor)
                version, count, filename, auxiliary, following = e.unpack('<HHIII', verneed[4]+cursor)
                require(version == 1, 'unsupported verneed version')
                filename = e.string(strings[4], strings[5], filename)
                position = cursor+auxiliary
                for index in range(count):
                    require(0 <= position <= verneed[5]-16, 'bad vernaux record')
                    value_hash, value_flags, other, name, next_aux = e.unpack('<IHHII', verneed[4]+position)
                    name = e.string(strings[4], strings[5], name)
                    version_names[other & 0x7fff] = (filename, name)
                    needs.append((filename, name, value_flags, value_hash))
                    if index+1 < count:
                        require(next_aux > 0, 'truncated vernaux chain')
                        position += next_aux
                if not following:
                    break
                cursor += following
        require(not version_values or len(version_values) == len(syms), 'versym/dynsym count mismatch')
        require(all((value & 0x7fff) in version_names for value in version_values), 'unknown symbol version')
        def interface(symbol):
            shndx = symbol[6]
            definition = 'UND' if shndx == 0 else 'ABS' if shndx == 0xfff1 else 'COMMON' if shndx == 0xfff2 else 'DEF'
            return symbol[0], symbol[1] >> 4, symbol[1] & 15, symbol[2] & 3, definition
        named_versions = sorted((interface(syms[i]), version_names[value & 0x7fff], bool(value & 0x8000))
                                for i, value in enumerate(version_values))
        return {'elf_type': e.elf_type, 'PT_INTERP': interp,
                'PT_GNU_RELRO': header_values(0x6474e552), 'PT_GNU_STACK': header_values(0x6474e551),
                'PT_GNU_PROPERTY': header_values(0x6474e553, True),
                '.note.gnu.property': content(e.by_name['.note.gnu.property']).hex() if '.note.gnu.property' in e.by_name else None,
                'DT_RPATH': search_paths.get('DT_RPATH'), 'DT_RUNPATH': search_paths.get('DT_RUNPATH'),
                'DT_FLAGS_FLAGS1': flags, 'DT_BIND_NOW': bind_now, 'W_X_LOAD': any(p[1] & 3 == 3 for p in e.loads), 'DT_NEEDED': needed,
                '.dynsym': sorted(interface(symbol) for symbol in syms),
                '.gnu.version': named_versions, '.gnu.version_r': sorted(needs)}
    finally:
        e.close()

def security_compare(ordinary, candidate, ignore_paths=False):
    before, after = security_properties(ordinary), security_properties(candidate)
    differences = [key for key in before if before[key] != after[key] and
                   not (ignore_paths and key in ('DT_RPATH', 'DT_RUNPATH'))]
    if differences:
        details = []
        for key in differences:
            if key in ('.dynsym', '.gnu.version', '.gnu.version_r'):
                old = collections.Counter(json.dumps(row, sort_keys=True) for row in before[key])
                new = collections.Counter(json.dumps(row, sort_keys=True) for row in after[key])
                details.append('%s before_count=%d after_count=%d first_removed=%r first_added=%r' %
                               (key, len(before[key]), len(after[key]), list((old-new).elements())[:5], list((new-old).elements())[:5]))
            else:
                details.append('%s before=%r after=%r' % (key, before[key], after[key]))
        raise GateError('ELF security attributes differ: '+'; '.join(details))
    heavy = ('.dynsym', '.gnu.version', '.gnu.version_r')
    return {'security_preserved': True,
            'ordinary_sha256': digest(ordinary), 'candidate_sha256': digest(candidate),
            'properties': {key: value for key, value in before.items() if key not in heavy},
            'symbol_version_evidence': {key: {'entries': len(before[key]),
                'sha256': hashlib.sha256(json.dumps(before[key], sort_keys=True).encode()).hexdigest()}
                for key in heavy}}

def installed_baseline(root, output):
    entity = Path(root)/'usr/bin/clang-22'
    properties = security_properties(entity)
    result = {'path': str(entity), 'sha256': digest(entity),
              'DT_RPATH': properties['DT_RPATH'], 'DT_RUNPATH': properties['DT_RUNPATH'],
              'security_properties': properties}
    save(output, result)
    return result


def installed_security(baseline, candidate):
    require(Path(baseline).is_file(), 'installed-baseline missing: '+str(baseline))
    before = json.loads(Path(baseline).read_text())['security_properties']
    after = json.loads(json.dumps(security_properties(candidate)))
    differences = {k: {'installed_baseline': before.get(k), 'candidate': after.get(k)}
                   for k in before.keys() | after.keys() if before.get(k) != after.get(k)}
    require(not differences, 'installed-baseline security attributes differ: '+json.dumps(differences))
    return {'installed_security_preserved': True, 'baseline_sha256': digest(baseline),
            'candidate_sha256': digest(candidate)}


def rpath_layout(path):
    """Freeze headers and every file byte except the two permitted sections."""
    elf = ELF(path)
    try:
        allowed = sorted((s[4], s[4]+s[5]) for name, s in elf.by_name.items()
                         if name in ('.dynamic', '.dynstr'))
        cursor = 0; frozen = hashlib.sha256()
        for start, end in allowed:
            require(start >= cursor, 'overlapping RPATH sections')
            frozen.update(elf.mm[cursor:start]); cursor = end
        frozen.update(elf.mm[cursor:])
        dynamic = elf.by_name.get('.dynamic')
        tags = [struct.unpack_from('<qQ', elf.mm, i)[0]
                for i in range(dynamic[4], dynamic[4]+dynamic[5], 16)] if dynamic else []
        return {'file_bytes': len(elf.mm), 'program_headers': elf.phdrs,
                'section_headers': elf.sections, 'dynamic_tags': tags,
                'unchanged_bytes_sha256': frozen.hexdigest(),
                'code_sections': {name: hashlib.sha256(elf.mm[s[4]:s[4]+s[5]]).hexdigest()
                                  for name, s in elf.by_name.items() if s[2] & 4 and s[1] != 8}}
    finally:
        elf.close()


def cmake_literal(value):
    require('\x00' not in value, 'NUL in CMake argument')
    delimiter = '='
    while ']'+delimiter+']' in value:
        delimiter += '='
    return '['+delimiter+'['+value+']'+delimiter+']'


def adjust_rpath(candidate, baseline, work, identity):
    candidate, work = Path(candidate), Path(work)
    require(Path(baseline).is_file(), 'installed-baseline missing: '+str(baseline))
    expected = json.loads(Path(baseline).read_text())
    props = security_properties(candidate)
    keys = ('DT_RPATH', 'DT_RUNPATH')
    old, new = {k: props[k] for k in keys}, {k: expected[k] for k in keys}
    require([k for k in keys if old[k] is not None] == [k for k in keys if new[k] is not None],
            'RPATH tag types differ from installed-baseline')
    require(sum(old[k] is not None for k in keys) <= 1, 'multiple RPATH tags unsupported')
    layout = rpath_layout(candidate); stripped_sha = digest(candidate)
    if old != new:
        key = next(k for k in keys if old[k] is not None)
        script = work/'candidate-rpath.cmake'
        atomic_text(script, 'file(RPATH_CHANGE FILE '+cmake_literal(str(candidate))+
                    ' OLD_RPATH '+cmake_literal(old[key])+' NEW_RPATH '+cmake_literal(new[key])+')\n')
        call(['cmake', '-P', str(script)], work/'candidate-rpath.log', timeout=60)
    require(rpath_layout(candidate) == layout, 'RPATH_CHANGE changed ELF layout or non-path content')
    actual = security_properties(candidate)
    require({k: actual[k] for k in keys} == new, 'ELF RPATH differs from installed-baseline')
    log = work/'candidate-readelf.log'
    call(['readelf', '-dW', str(candidate)], log, timeout=60)
    text = log.read_text(); readelf_paths = {}
    for key in keys:
        matches = re.findall(r'\('+key[3:]+r'\)[^\n]*\[([^\n]*)\]', text)
        require(len(matches) <= 1, 'duplicate readelf path tag: '+key)
        readelf_paths[key] = matches[0] if matches else None
    require(readelf_paths == new, 'readelf RPATH differs from installed-baseline')
    checked = installed_security(baseline, candidate)
    identity.update(strip_all_sha256=stripped_sha, rpath_adjusted_sha256=digest(candidate),
                    after_sha256=digest(candidate), installed_baseline_sha256=digest(baseline),
                    installed_baseline_path=str(baseline),
                    rpath={'before': old, 'after': new, 'layout': layout, 'readelf': readelf_paths,
                           'security': checked})
    validate_identity(identity, candidate)
    save(work/'identity.json', identity)
    return identity


# Real implementation files, not synthetic tiny probes. C uses compiler resource
# headers only; freestanding + nostdinc prevents accidental cross-target sysroots.
REAL_C_SOURCES = ('compiler-rt/lib/builtins/bswapsi2.c', 'compiler-rt/lib/builtins/bswapdi2.c')
REAL_CXX_SOURCES = ('llvm/lib/Support/SmallVector.cpp', 'llvm/lib/Support/StringRef.cpp')


def real_commands(build, resource_dir):
    build = Path(build).absolute(); source = build.parent
    cases = []
    for relative in REAL_C_SOURCES:
        for target in TRIPLES:
            cases.append((relative, target, ['--no-default-config', '--target='+target,
                          '-resource-dir='+str(resource_dir), '-ffreestanding', '-nostdinc',
                          '-isystem', str(Path(resource_dir)/'include'), '-O2', '-g', '-c',
                          str(source/relative)]))
    for relative in REAL_CXX_SOURCES:
        cases.append((relative, 'x86_64-tizen-linux-gnu', ['--no-default-config',
                      '--target=x86_64-tizen-linux-gnu', '-resource-dir='+str(resource_dir),
                      '-O2', '-g', '-std=c++17', '-I'+str(source/'llvm/include'),
                      '-I'+str(build/'include'), '-c', str(source/relative)]))
    return cases


def real_gate(ordinary, candidate, build, work, resource_dir):
    started = time.monotonic(); work = Path(work); work.mkdir(parents=True, exist_ok=True)
    # Both roles use the same physical compiler/output paths, including strings
    # emitted into .GCC.command.line. No stripping or object normalization.
    compiler = work/'same-clang'; output = work/'same.o'; rows = []
    cases = real_commands(build, resource_dir)
    for role, executable in (('ordinary', ordinary), ('candidate', candidate)):
        shutil.copyfile(executable, compiler); compiler.chmod(0o755)
        for index, (relative, target, args) in enumerate(cases):
            output.unlink(missing_ok=True)
            start = time.monotonic()
            call([str(compiler), *args, '-o', str(output)], work/('%s-%02d.log' % (role,index)), timeout=120)
            require(output.is_file() and not output.is_symlink() and output.stat().st_size > 0,
                    'real compile did not produce a nonempty regular object: '+relative)
            sha = digest(output)
            if role == 'ordinary':
                rows.append({'source': relative, 'target': target, 'ordinary_sha256': sha,
                             'ordinary_seconds': time.monotonic()-start})
            else:
                rows[index].update(candidate_sha256=sha, candidate_seconds=time.monotonic()-start)
                require(sha == rows[index]['ordinary_sha256'], 'real object bytes differ: '+relative+' '+target)
                rows[index]['byte_equal'] = True
    result = {'real_pass': True, 'seconds': time.monotonic()-started, 'cases': rows}
    save(work/'real-result.json', result)
    print('BOLT_REAL_GATE_PASS '+json.dumps({'work': str(work), 'cases': len(rows), 'seconds': result['seconds']}), flush=True)
    return result


def tiny_gate(ordinary, candidate, work, resource_dir=None):
    work = Path(work); work.mkdir(parents=True, exist_ok=True)
    source = work/'tiny.c'; source.write_text(TINY); out = work/'same.o'; rows = []
    for label, cc in [('ordinary', ordinary), ('candidate', candidate)]:
        call([cc, '--version'], work/(label+'-version.log'), timeout=30)
    for triple in TRIPLES:
        row = {'target': triple, 'outputs': []}
        for label, cc in [('ordinary', ordinary), ('candidate', candidate)]:
            argv = [cc, '--no-default-config', '--target='+triple, '-c', '-O2', str(source), '-o', str(out)]
            if resource_dir:
                argv[1:1] = ['-resource-dir', resource_dir]
            if out.exists() or out.is_symlink():
                out.unlink()
            call(argv, work/(triple+'-'+label+'.log'), cwd=work, timeout=60)
            require(out.is_file() and not out.is_symlink() and out.stat().st_size > 0,
                    'tiny compiler did not produce a nonempty regular file: '+label+' '+triple)
            dest = work/(triple+'.'+label+'.o'); shutil.copyfile(out, dest)
            row['outputs'].append({'path': str(dest), 'sha256': digest(dest), 'bytes': dest.stat().st_size})
        row['byte_equal'] = (work/(triple+'.ordinary.o')).read_bytes() == (work/(triple+'.candidate.o')).read_bytes()
        rows.append(row); save(work/'result.json', rows)
        require(row['byte_equal'], 'tiny object differs: '+triple)
    return rows

def inventory(root, hash_files=True):
    root = Path(root).absolute(); files = {}
    require(root.is_dir() and not root.is_symlink(), 'inventory root must be a non-symlink directory: '+str(root))
    def traversal_error(error):
        raise GateError('inventory traversal failed: '+str(error)) from error
    for folder, dirs, names in os.walk(root, followlinks=False, onerror=traversal_error):
        for name in sorted(dirs + names):
            p = Path(folder)/name; key = p.relative_to(root).as_posix(); st = p.lstat()
            if stat.S_ISLNK(st.st_mode):
                files[key] = {'type': 'symlink', 'target': os.readlink(p)}
            elif stat.S_ISREG(st.st_mode):
                files[key] = {'type': 'file', 'mode': stat.S_IMODE(st.st_mode), 'bytes': st.st_size, **({'sha256': digest(p)} if hash_files else {})}
            elif stat.S_ISDIR(st.st_mode):
                files[key] = {'type': 'dir'}
            else:
                raise GateError('special file in buildroot: '+key)
    return {'root': str(root), 'files': files}

def root_snapshot(root):
    """Packaging baseline, including directory and symlink permissions."""
    root = Path(root).absolute()
    result = inventory(root)
    result['metadata'] = {}
    for key in [''] + sorted(result['files']):
        path = root/key
        st = path.lstat()
        item = {'mode': stat.S_IMODE(st.st_mode)}
        if stat.S_ISLNK(st.st_mode):
            item['bytes'] = st.st_size
        result['metadata'][key] = item
    return result

def compare_root(root, baseline, after_path):
    """Reject any buildroot side effect before installing the candidate."""
    current = root_snapshot(root)
    save(after_path, current)
    require(baseline.get('root') == current['root'], 'buildroot baseline belongs to a different root')
    require('metadata' in baseline, 'buildroot baseline lacks complete permission metadata')
    old, new = baseline['files'], current['files']
    for key in sorted(old.keys() | new.keys()):
        require(key in old, 'buildroot added: '+key)
        require(key in new, 'buildroot removed: '+key)
        require(old[key] == new[key], 'buildroot entry differs: '+key)
        require(baseline['metadata'].get(key) == current['metadata'][key],
                'buildroot permissions/metadata differ: '+key)
    require(baseline['metadata'].get('') == current['metadata'][''],
            'buildroot permissions/metadata differ: .')
    return {'buildroot_unchanged': True, 'entries': len(new)}

def rooted_resolve(root, path):
    root = Path(root).absolute(); rel = Path(path).relative_to(root); todo = list(rel.parts)
    done = []; seen = set()
    while todo:
        part = todo.pop(0)
        if part in ('', '.'):
            continue
        if part == '..':
            require(bool(done), 'alias escapes buildroot'); done.pop(); continue
        probe = root.joinpath(*done, part)
        if probe.is_symlink():
            identity = probe.relative_to(root).as_posix()
            require(identity not in seen, 'alias cycle'); seen.add(identity)
            target = os.readlink(probe)
            if target.startswith('/'):
                done = []
            todo = list(Path(target).parts[1:] if target.startswith('/') else Path(target).parts) + todo
        else:
            done.append(part)
    return root.joinpath(*done)

def alias_group(root):
    root = Path(root).absolute(); entity = root/'usr/bin/clang-22'
    require(entity.is_file() and not entity.is_symlink(), 'missing clang-22 installed entity')
    base = entity.stat(); aliases = []
    for p in sorted((root/'usr/bin').iterdir()):
        if p == entity:
            continue
        resolved = rooted_resolve(root, p)
        if resolved.exists() and (resolved.stat().st_dev, resolved.stat().st_ino) == (base.st_dev, base.st_ino):
            aliases.append(p)
        elif p.is_file() and not p.is_symlink() and p.stat().st_size == base.st_size and digest(p) == digest(entity):
            aliases.append(p)
        elif p.name in ['clang', 'clang++', 'clang++-22', 'clang-cl', 'clang-cpp'] or p.name.endswith(('-clang','-clang++')):
            raise GateError('clang family alias points to different content: '+str(p))
    return entity, aliases

def install_candidate(root, candidate, state, identity, announce=False, identity_path=None):
    root = Path(root).absolute(); require('debug' not in str(root).lower(), 'buildroot absolute path contains debug')
    e = ELF(candidate)
    try:
        elf = e.audit(final=True)
    finally:
        e.close()
    validate_identity(identity, candidate)
    entity, aliases = alias_group(root); changed = []
    for p in aliases:
        changed.append({'path': p.relative_to(root).as_posix(), 'old_type': 'symlink' if p.is_symlink() else 'file',
                        'old_target': os.readlink(p) if p.is_symlink() else None})
    st = entity.stat(); tmp = entity.with_name('.clang-bolt.new'); staged = []
    require(not tmp.exists() and not tmp.is_symlink(), 'temporary candidate exists')
    try:
        shutil.copyfile(candidate,tmp)
        tmp.chmod(stat.S_IMODE(st.st_mode))
        with tmp.open('rb') as stream: os.fsync(stream.fileno())
        actual = digest(tmp)
        require(actual == identity['after_sha256'], 'temporary candidate SHA differs')
        require(tmp.stat().st_size == Path(candidate).stat().st_size, 'temporary candidate size differs')
        for path in aliases:
            link = path.with_name('.'+path.name+'.bolt-link')
            require(not link.exists() and not link.is_symlink(), 'temporary alias exists')
            link.symlink_to('clang-22'); staged.append((link,path))
        identity = dict(identity, installed_sha256=actual)
        result = {'installed_sha256':actual, 'identity':identity, 'alias_changes':changed,
                  'allowed_paths':['usr/bin/clang-22']+[p.relative_to(root).as_posix() for p in aliases], 'elf':elf}
        # All file writes, state and output publication precede the final commit.
        save(state,result)
        if identity_path is not None:
            save(identity_path, identity)
        if announce: print(json.dumps(result,ensure_ascii=False),flush=True)
        for link,path in staged: os.replace(link,path)
        os.replace(tmp,entity)
        return result
    except BaseException:
        for path in [tmp]+[link for link,_ in staged]:
            try: path.unlink()
            except OSError: pass
        raise

def post_gate(root, state, ordinary, candidate_work, resource_dir=None):
    root = Path(root).absolute(); require('debug' not in str(root).lower(), 'buildroot absolute path contains debug')
    entity = root/'usr/bin/clang-22'; require(digest(entity) == state['installed_sha256'], 'clang changed during RPM post-processing')
    for change in state['alias_changes']:
        p = root/change['path']
        require(p.is_symlink() and os.readlink(p) == 'clang-22' and rooted_resolve(root,p) == entity,
                'alias stale or not normalized: '+str(p))
    e = ELF(entity)
    try:
        elf = e.audit(final=True)
    finally:
        e.close()
    require(digest(entity) == state['identity']['after_sha256'], 'final installed SHA differs from stripped candidate')
    no_bolt_products(root)
    security = security_compare(ordinary, str(entity), ignore_paths=True)
    baseline = Path(ordinary).parent/'installed-baseline.json'
    if 'installed_baseline_sha256' in state['identity']:
        require(digest(baseline) == state['identity']['installed_baseline_sha256'], 'installed-baseline SHA changed')
    installed = installed_security(baseline, entity)
    rows = tiny_gate(ordinary, str(entity), candidate_work, resource_dir)
    real = real_gate(ordinary, str(entity), Path(ordinary).parent.parent,
                     Path(candidate_work)/'real', resource_dir)
    return {'sha_unchanged': True, 'aliases_pass': True, 'elf': elf, 'tiny': rows,
            'strip_identity_pass': True, 'security': security, 'installed_security': installed, 'real': real}

def certified_version(text):
    lines = re.findall(r'^\s*(LLVM version[^\n]*)$', text, re.M)
    require(lines == [CERTIFIED['bolt_version']], 'uncertified BOLT tool version actual=%s expected=%s; remedy: update certified constants and recertify, or disable with --without clang_bolt / bcond_with' % (lines, CERTIFIED['bolt_version']))
    return lines[0]

def no_bolt_products(root):
    root = Path(root).absolute()
    for name in ('llvm-bolt', 'perf2bolt', 'llvm-boltdiff', 'merge-fdata'):
        path = root/'usr/bin'/name
        require(not path.exists() and not path.is_symlink(), 'BOLT tool in buildroot: '+str(path))
    tokens = (b'LLVMBOLT', b'llvm-bolt', b'perf2bolt', b'llvm-boltdiff', b'merge-fdata')
    # Reuse fail-closed inventory traversal without hashing package payloads.
    files = inventory(root, hash_files=False)['files']
    cmake_count = 0
    for key, item in files.items():
        path = root/key
        require(not (key.startswith('usr/lib64/libLLVMBOLT') and key.endswith('.a')),
                'BOLT static library in buildroot: '+key)
        if key.lower().endswith('.cmake'):
            path = rooted_resolve(root, path)
            require(path.exists(), 'dangling CMake metadata: '+key)
            cmake_count += 1
            require(path.is_file(), 'unreadable CMake metadata: '+key)
            content = path.read_bytes()
            for token in tokens:
                require(token not in content, 'BOLT CMake export: '+key+' matched '+token.decode())
    return {'no_bolt_products': True, 'paths_checked': len(files), 'cmake_files_checked': cmake_count, 'cmake_tokens': [v.decode() for v in tokens]}

def rewrite(bolt, profile, input_elf, output, work):
    work = Path(work); work.mkdir(parents=True, exist_ok=True)
    profile_identity(profile)
    version = call([bolt, '--version'], work/'bolt-version.log')
    certified_version(version)
    argv = [bolt, input_elf, '-o', output, '-data='+str(profile)] + OPTIONS
    text = call(argv, work/'bolt.log', timeout=1800)
    counters = match_counts(text, argv, True, True)
    e = ELF(output)
    try:
        elf = e.audit()
    finally:
        e.close()
    result = {'tool_sha256': digest(bolt), 'profile_sha256': PROFILE_SHA,
              'input_sha256': digest(input_elf), 'output_sha256': digest(output), 'argv': argv,
              'counts': counters, 'elf': elf}
    save(work/'rewrite-result.json', result); return result

BOLT_TASK_DESCRIPTIONS = frozenset(('Generating VCSVersion.inc', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/AddressMap.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/BinaryBasicBlock.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/BinaryContext.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/BinaryData.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/BinaryEmitter.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/BinaryFunction.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/BinaryFunctionCallGraph.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/BinaryFunctionProfile.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/BinarySection.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/CallGraph.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/CallGraphWalker.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/DIEBuilder.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/DebugData.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/DebugNames.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/DynoStats.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/Exceptions.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/FunctionLayout.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/GDBIndex.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/HashUtilities.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/JumpTable.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/MCInstUtils.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/MCPlusBuilder.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/ParallelUtilities.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/Relocation.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/AArch64RelaxationPass.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/Aligner.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/AllocCombiner.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/AsmDump.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/BinaryPasses.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/CMOVConversion.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/CacheMetrics.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/DataflowAnalysis.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/DataflowInfoManager.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/FixRISCVCallsPass.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/FixRelaxationPass.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/FrameAnalysis.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/FrameOptimizer.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/HFSort.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/Hugify.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/IdenticalCodeFolding.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/IndirectCallPromotion.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/Inliner.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/Instrumentation.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/JTFootprintReduction.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/LivenessAnalysis.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/LongJmp.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/LoopInversionPass.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/MCF.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/PAuthGadgetScanner.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/PLTCall.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/PatchEntries.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/PettisAndHansen.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/PointerAuthCFIAnalyzer.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/PointerAuthCFIFixup.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/ProfileQualityStats.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/RegAnalysis.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/RegReAssign.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/ReorderAlgorithm.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/ReorderData.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/ReorderFunctions.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/RetpolineInsertion.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/ShrinkWrapping.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/SplitFunctions.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/StackAllocationAnalysis.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/StackAvailableExpressions.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/StackPointerTracking.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/StackReachingUses.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/StokeInfo.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/TailDuplication.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/ThreeWayBranch.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/ValidateInternalCalls.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/ValidateMemRefs.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/VeneerElimination.cpp.o', 'Building CXX object tools/bolt/lib/Profile/CMakeFiles/LLVMBOLTProfile.dir/BoltAddressTranslation.cpp.o', 'Building CXX object tools/bolt/lib/Profile/CMakeFiles/LLVMBOLTProfile.dir/DataAggregator.cpp.o', 'Building CXX object tools/bolt/lib/Profile/CMakeFiles/LLVMBOLTProfile.dir/DataReader.cpp.o', 'Building CXX object tools/bolt/lib/Profile/CMakeFiles/LLVMBOLTProfile.dir/Heatmap.cpp.o', 'Building CXX object tools/bolt/lib/Profile/CMakeFiles/LLVMBOLTProfile.dir/StaleProfileMatching.cpp.o', 'Building CXX object tools/bolt/lib/Profile/CMakeFiles/LLVMBOLTProfile.dir/YAMLProfileReader.cpp.o', 'Building CXX object tools/bolt/lib/Profile/CMakeFiles/LLVMBOLTProfile.dir/YAMLProfileWriter.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/BinaryPassManager.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/BoltDiff.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/BuildIDRewriter.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/DWARFRewriter.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/ExecutableFileMemoryManager.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/GNUPropertyRewriter.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/JITLinkLinker.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/LinuxKernelRewriter.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/MachORewriteInstance.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/MetadataManager.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/PseudoProbeRewriter.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/RSeqRewriter.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/RewriteInstance.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/SDTRewriter.cpp.o', 'Building CXX object tools/bolt/lib/RuntimeLibs/CMakeFiles/LLVMBOLTRuntimeLibs.dir/HugifyRuntimeLibrary.cpp.o', 'Building CXX object tools/bolt/lib/RuntimeLibs/CMakeFiles/LLVMBOLTRuntimeLibs.dir/InstrumentationRuntimeLibrary.cpp.o', 'Building CXX object tools/bolt/lib/RuntimeLibs/CMakeFiles/LLVMBOLTRuntimeLibs.dir/RuntimeLibrary.cpp.o', 'Building CXX object tools/bolt/lib/Target/X86/CMakeFiles/LLVMBOLTTargetX86.dir/X86MCPlusBuilder.cpp.o', 'Building CXX object tools/bolt/lib/Target/X86/CMakeFiles/LLVMBOLTTargetX86.dir/X86MCSymbolizer.cpp.o', 'Building CXX object tools/bolt/lib/Utils/CMakeFiles/LLVMBOLTUtils.dir/CommandLineOpts.cpp.o', 'Building CXX object tools/bolt/lib/Utils/CMakeFiles/LLVMBOLTUtils.dir/Utils.cpp.o', 'Building CXX object tools/bolt/tools/driver/CMakeFiles/llvm-bolt.dir/llvm-bolt.cpp.o', 'Linking CXX executable bin/llvm-bolt', 'Linking CXX static library lib64/libLLVMBOLTCore.a', 'Linking CXX static library lib64/libLLVMBOLTPasses.a', 'Linking CXX static library lib64/libLLVMBOLTProfile.a', 'Linking CXX static library lib64/libLLVMBOLTRewrite.a', 'Linking CXX static library lib64/libLLVMBOLTRuntimeLibs.a', 'Linking CXX static library lib64/libLLVMBOLTTargetX86.a', 'Linking CXX static library lib64/libLLVMBOLTUtils.a'))

TF_REFRESH_DESCRIPTIONS = frozenset((
    'Building C object lib64/tf_runtime/CMakeFiles/tf_xla_runtime.dir/tf_xla_runtime_dummy.c.o',
    'Linking C static library lib64/libtf_xla_runtime.a'))

def tool_plan(text):
    lines = text.splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    require(not any('Re-running CMake...' in line for line in lines), REGEN_ERROR)
    diagnostics = [line for line in lines if line.startswith('ninja: warning:')]
    lines = [line for line in lines if not line.startswith('ninja: warning:')]
    require(not any('Re-running CMake...' in line for line in lines), REGEN_ERROR)
    counts = {'objects': 0, 'static_libraries': 0, 'executables': 0, 'generated': 0}
    if lines == ['ninja: no work to do.']:
        return {'plan_type': 'up-to-date', 'tasks': 0, 'categories': counts,
                'configuration_refresh_tasks': 0, 'descriptions': [], 'ninja_diagnostics': diagnostics, 'ninja_diagnostics_count': len(diagnostics)}
    require(bool(lines), 'empty BOLT tool plan')
    descriptions = []; completed = set()
    for line in lines:
        match = re.fullmatch(r'\[([0-9]+)/([0-9]+)\] (.+)', line)
        require(match is not None, 'non-progress line in BOLT tool plan: '+line)
        require(1 <= int(match[1]) <= len(lines) and int(match[2]) == len(lines) and
                int(match[1]) not in completed, 'invalid or truncated BOLT plan: '+line)
        completed.add(int(match[1]))
        body = match[3]
        require(body not in descriptions, 'duplicate BOLT task: '+body)
        require(body in BOLT_TASK_DESCRIPTIONS or body in TF_REFRESH_DESCRIPTIONS, 'unapproved BOLT task: actual=%s expected=certified BOLT/TF tasks; remedy: inspect configuration and dirty causes, regenerate the certified whitelist and recertify if needed; never expand it automatically' % body)
        descriptions.append(body)
        if body in BOLT_TASK_DESCRIPTIONS:
            category = ('generated' if body == 'Generating VCSVersion.inc' else
                        'objects' if body.startswith('Building CXX object ') else
                        'static_libraries' if body.startswith('Linking CXX static library ') else 'executables')
            counts[category] += 1
    tf = set(descriptions) & TF_REFRESH_DESCRIPTIONS
    require(not tf or tf == TF_REFRESH_DESCRIPTIONS, 'TF configuration refresh tasks must appear together')
    require('Linking CXX executable bin/llvm-bolt' in descriptions, 'missing llvm-bolt executable link')
    return {'plan_type': 'build', 'tasks': len(lines), 'categories': counts,
            'configuration_refresh_tasks': len(tf), 'descriptions': descriptions, 'ninja_diagnostics': diagnostics, 'ninja_diagnostics_count': len(diagnostics)}

def tool_prepare(build, plan, state_path):
    build = Path(build)
    executable = build/'bin/llvm-bolt'
    exists = executable.exists()
    value = {'configuration_refresh_tasks': plan['configuration_refresh_tasks'],
             'executable_before': {'exists': exists, 'sha256': digest(executable) if exists and executable.is_file() else None}}
    if value['configuration_refresh_tasks']:
        archive = build/'lib64/libtf_xla_runtime.a'
        require(archive.is_file(), 'missing TF archive before build')
        value['archive_path'] = str(archive); value['before_sha256'] = digest(archive)
        # Only evidence: do not turn an optional graph inference into a gate.
        graph = (build/'build.ninja').read_text()
        match = re.search(r'^build lib64/libtf_xla_runtime\.a:[^\n]*(?:\n  [^\n]*)*', graph, re.M)
        paths = set(re.findall(r'/[^\s\"\';]+/libtf_xla_runtime_prebuilt\.a', match[0] if match else ''))
        value['prebuilt_evidence'] = {'inferred_paths': sorted(paths)}
        if len(paths) == 1:
            source = Path(next(iter(paths)))
            if source.is_file():
                sha = digest(source)
                value['prebuilt_evidence'].update(sha256=sha, archive_equal=sha == value['before_sha256'])
    save(state_path, value)
    return value

def tool_verify(build, plan, text, state):
    lines = text.splitlines()
    require(bool(lines) and lines[-1] == BUILD_SUCCESS and lines.count(BUILD_SUCCESS) == 1,
            'missing, duplicate or non-final '+BUILD_SUCCESS)
    descriptions = []; counters = []
    for line in lines[:-1]:
        match = re.fullmatch(r'\[(\d+)/(\d+)\] (.+)', line)
        if match is None:
            require(not re.match(r'\[\d', line), 'malformed real build progress: '+line)
            continue
        f, t, body = int(match[1]), int(match[2]), match[3]
        require(1 <= f <= t and f not in [c[0] for c in counters],
                'invalid real build progress: '+line)
        require(body in plan['descriptions'], 'real build task outside approved plan: '+body)
        require(body not in descriptions, 'duplicate real build task: '+body)
        descriptions.append(body); counters.append([f, t])
    require(plan['plan_type'] != 'up-to-date' or not descriptions, 'up-to-date build unexpectedly ran tasks')
    require(plan['plan_type'] != 'build' or bool(descriptions), 'build plan executed no tasks')
    require({c[0] for c in counters} == set(range(1, len(descriptions)+1)), 'real build counter set incomplete')
    require(set(descriptions) == set(plan['descriptions']) and len(descriptions) == plan['tasks'],
            'executed task set/count differs from approved plan')
    executable = Path(build)/'bin/llvm-bolt'
    require(executable.is_file() and not executable.is_symlink() and os.access(executable, os.X_OK),
            'llvm-bolt is not a regular executable')
    require(state['configuration_refresh_tasks'] == plan['configuration_refresh_tasks'], 'TF snapshot does not match plan')
    tf = dict(state)
    if plan['configuration_refresh_tasks']:
        archive = Path(build)/'lib64/libtf_xla_runtime.a'
        require(archive.is_file(), 'missing TF archive after build')
        tf['after_sha256'] = digest(archive)
        require(tf['after_sha256'] == state['before_sha256'], 'TF archive SHA changed during build')
    after_sha = digest(executable)
    before = state['executable_before']
    return {'planned_tasks': plan['tasks'], 'executed_tasks': len(descriptions),
            'executable_before': before['exists'], 'executable_before_sha256': before['sha256'],
            'executable_after_sha256': after_sha,
            'executable_produced_by_this_build': 'Linking CXX executable bin/llvm-bolt' in descriptions,
            'tool_build_verified': True, 'tasks': len(descriptions), 'descriptions': descriptions,
            'progress_counters': counters, 'TF_archive': tf, 'executable': str(executable)}


# These are package-owned measurement scopes, not admission limits.
BOLT_OWNED_PATHS = ('clang-bolt/**', 'tools/bolt/**', 'lib64/libLLVMBOLT*.a',
                    'bin/llvm-bolt', 'ThinLTO cache positive allocation delta')
DISK_LOG_MATCHES = (r'No space left on device', r'Disk quota exceeded',
                    r'\bENOSPC\b', r'\bEDQUOT\b')
_DISK_CONTEXT = {}


def disk_context(build=None, work=None, root=None):
    build = Path(build or _DISK_CONTEXT.get('build') or os.environ.get('BOLT_BUILD') or Path.cwd()).absolute()
    work = Path(work or _DISK_CONTEXT.get('work') or os.environ.get('BOLT_WORK') or build/'clang-bolt').absolute()
    root = root or _DISK_CONTEXT.get('root') or os.environ.get('BOLT_INSTALL_ROOT')
    return build, work, Path(root).absolute() if root else None


def filesystem(path):
    path = Path(path).absolute()
    while not path.exists():
        path = path.parent
    if not path.is_dir():
        path = path.parent
    return {'path': str(path), 'device': path.stat().st_dev,
            'free_bytes': shutil.disk_usage(path).free, 'time_ns': time.time_ns()}


def disk_entries(root):
    """lstat allocation, including directories; never follow symlinks."""
    root = Path(root)
    if not root.exists() and not root.is_symlink():
        return {}
    result = {}
    def add(path):
        s = path.lstat()
        result[path.relative_to(root).as_posix()] = {
            'device': s.st_dev, 'inode': s.st_ino, 'bytes': s.st_size,
            'allocated_bytes': s.st_blocks*512, 'mode': s.st_mode}
    add(root)
    if root.is_dir() and not root.is_symlink():
        def failed(error): raise error
        for directory, dirs, files in os.walk(root, followlinks=False, onerror=failed):
            for name in dirs+files:
                add(Path(directory)/name)
    return result


def cache_release(build, work):
    """Best-effort release of the certified in-tree cache after compare-root."""
    build, work = Path(build), Path(work)
    path = build/'lto.cache'
    started = time.monotonic()
    result = {'status': 'skipped', 'path': str(path)}
    def emit(message):
        try: print('BOLT_CACHE_RELEASE '+message, flush=True)
        except OSError: pass
    try:
        original = (work/'link.original').read_text()
        # Validate the original edge with the exact replay syntax/cache rules.
        replay_script(original, work/'unused-output', work/'unused-dependency')
        # Remove CMake Ninja ': && ' and ' && :' wrappers, as in replay_script.
        paths = re.findall(r'--thinlto-cache-dir=([^\s]+)', original.strip()[5:-5])
        path = Path(paths[0])
        result['path'] = str(path)
        if path.is_symlink():
            reason = 'symlink'
        elif path.resolve() != (build/'lto.cache').resolve():
            reason = 'outside-build-cache'
        elif not path.is_dir():
            reason = 'not-a-directory-or-missing'
        else:
            entries = disk_entries(path)
            result.update(files=sum(stat.S_ISREG(x['mode']) for x in entries.values()),
                          allocated_bytes=sum(x['allocated_bytes'] for x in entries.values()))
            try:
                shutil.rmtree(path)
            except OSError as error:
                try:
                    remaining = sum(stat.S_ISREG(x['mode']) for x in disk_entries(path).values())
                except OSError:
                    remaining = 'unknown'
                result.update(status='partial', error=str(error), remaining_files=remaining)
                emit('partial error='+str(error)+' remaining_files='+str(remaining))
            else:
                result.update(status='removed', seconds=time.monotonic()-started)
                emit('removed path='+str(path)+' files='+str(result['files'])+
                     ' allocated_bytes='+str(result['allocated_bytes'])+
                     ' seconds='+str(result['seconds']))
            reason = None
        if reason:
            result['reason'] = reason
            emit('skipped reason='+reason+' path='+str(path))
    except Exception as error:
        result['reason'] = str(error)
        emit('skipped reason='+str(error)+' path='+str(path))
    try:
        save(work/'cache-release.json', result)
    except (OSError, ValueError) as error:
        emit('record-unavailable error='+str(error)+' path='+str(work/'cache-release.json'))
    return result


def disk_cache(build, work):
    edge = work/'link.original'
    if edge.is_file():
        matches = re.findall(r'--thinlto-cache-dir=([^\s]+)', edge.read_text())
        if len(matches) == 1:
            return Path(matches[0].strip("'\""))
    return build/'lto.cache'


def disk_measure(build, work, baseline=None):
    scopes = [('work', work), ('tool_objects', build/'tools/bolt'),
              ('tool_executable', build/'bin/llvm-bolt')]
    scopes += [('tool_library', p) for p in sorted((build/'lib64').glob('libLLVMBOLT*.a'))]
    owned = {}; groups = []; seen = set()
    for category, path in scopes:
        entries = disk_entries(path); allocated = logical = 0
        for rel, item in entries.items():
            key = (item['device'], item['inode'])
            if key in seen: continue
            seen.add(key); allocated += item['allocated_bytes']
            if stat.S_ISREG(item['mode']): logical += item['bytes']
            owned[str(path/rel)] = item
        groups.append({'category': category, 'path': str(path),
                       'allocated_bytes': allocated, 'logical_file_bytes': logical})
    cache = disk_cache(build, work); current = disk_entries(cache)
    old = (baseline or {}).get('cache_entries', {})
    same_cache = baseline is not None and baseline.get('cache_path') == str(cache)
    cache_delta = cache_logical = 0
    if same_cache:
        for rel, item in current.items():
            previous = old.get(rel)
            delta = item['allocated_bytes'] if previous is None else max(0, item['allocated_bytes']-previous['allocated_bytes'])
            logical = item['bytes'] if previous is None else max(0, item['bytes']-previous['bytes'])
            cache_delta += delta
            if stat.S_ISREG(item['mode']): cache_logical += logical
    per_device = collections.defaultdict(int)
    for item in owned.values(): per_device[item['device']] += item['allocated_bytes']
    if same_cache:
        for rel, item in current.items():
            previous = old.get(rel)
            per_device[item['device']] += item['allocated_bytes'] if previous is None else max(0, item['allocated_bytes']-previous['allocated_bytes'])
    return {'owned_paths': groups, 'owned_filesystem_bytes': dict(per_device),
            'used_bytes': sum(per_device.values()), 'cache_path': str(cache),
            'cache_entries': current, 'cache_delta_known': same_cache,
            'cache_delta_allocated_bytes': cache_delta, 'cache_delta_logical_bytes': cache_logical,
            'cache_net_allocation_delta_bytes': sum(x['allocated_bytes'] for x in current.values())-sum(x['allocated_bytes'] for x in old.values()) if same_cache else None}


def disk_report(stage, build=None, work=None, root=None):
    """Best effort only: no space-based decisions, and no propagated exception."""
    value = {'stage': stage, 'time_ns': time.time_ns(), 'recorded': False}
    try:
        build, work, root = disk_context(build, work, root)
        baseline_path = work/'disk-baseline.json'
        baseline = None
        if stage != 'begin' and baseline_path.is_file():
            baseline = json.loads(baseline_path.read_text())
        measured = disk_measure(build, work, baseline)
        value.update(filesystem(work), build=str(build), work=str(work),
                     root=str(root) if root else None, scopes=list(BOLT_OWNED_PATHS), **measured)
        value['filesystem_device']=value['device']
        if stage == 'begin':
            baseline = {'time_ns': value['time_ns'], 'cache_path': measured['cache_path'],
                        'cache_entries': measured['cache_entries']}
            save(baseline_path, baseline)
        record = dict(value); record.pop('cache_entries', None); record['recorded'] = True
        save(work/('disk-'+stage+'.json'), record)
        value = record
    except Exception as error:
        value['report_error'] = str(error)
    value.pop('cache_entries',None)
    try: print('BOLT_DISK_REPORT '+json.dumps(value, ensure_ascii=False), flush=True)
    except Exception: pass
    return value


def disk_failure_log(log):
    try:
        text = Path(log).read_text(errors='replace') if log and str(log) != '-' else ''
        return text, bool(text.strip())
    except (OSError, ValueError):
        return '', False


def disk_evidence(log, error=None, log_text=None):
    evidence = []; seen = set()
    while error is not None and id(error) not in seen:
        seen.add(id(error))
        if isinstance(error, OSError) and error.errno in (28, 122):
            evidence.append('errno='+str(error.errno))
        # copytree preserves per-file failures as structured triples, not errno.
        if isinstance(error, shutil.Error) and error.args and isinstance(error.args[0], list):
            messages='\n'.join(str(row[2]) for row in error.args[0] if isinstance(row, (list,tuple)) and len(row)==3)
            evidence += ['copytree:'+pattern for pattern in DISK_LOG_MATCHES if re.search(pattern,messages,re.I)]
        error = error.__cause__ or error.__context__
    text = disk_failure_log(log)[0] if log_text is None else log_text
    evidence += [pattern for pattern in DISK_LOG_MATCHES if re.search(pattern, text, re.I)]
    return evidence


def task_output(build, description):
    for prefix in ('Building CXX object ', 'Building C object ', 'Linking CXX static library ', 'Linking C static library ', 'Linking CXX executable '):
        if description.startswith(prefix): return build/description[len(prefix):]
    if description == 'Generating VCSVersion.inc': return build/'tools/bolt/lib/Utils/VCSVersion.inc'
    if description.startswith('Building CXX object '): return build/description.split('Building CXX object ', 1)[1]
    return None


def disk_prediction(build, work, root, measured, baseline, device):
    formulas = []; unknown = []; growth = peak = 0
    def file_size(path): return path.stat().st_size if path.is_file() else 0
    def allocation(path): return path.stat().st_blocks*512 if path.is_file() else 0
    def completed(log):
        path = log.with_suffix(log.suffix+'.argv.json')
        try:
            value = json.loads(path.read_text())
            return value.get('completed') is True and path.stat().st_mtime_ns >= baseline['time_ns']
        except (OSError, ValueError): return False
    def add(name, expected, present, destination, temporary=False):
        nonlocal growth, peak
        need = max(0, expected-present)
        relevant = filesystem(destination)['device'] == device
        formulas.append({'item': name, 'formula': 'max(expected_output_bytes - present_allocated_bytes, 0)',
                         'expected_output_bytes': expected, 'present_allocated_bytes': present,
                         'additional_bytes': need, 'temporary': temporary,
                         'filesystem_device': filesystem(destination)['device']})
        if relevant:
            if temporary: peak = max(peak, growth+need)
            else: growth += need; peak = max(peak, growth)
    copy_source=_DISK_CONTEXT.get('copy_source');copy_destination=_DISK_CONTEXT.get('copy_destination')
    if copy_source and copy_destination:
        entries=disk_entries(copy_source);current=disk_entries(copy_destination)
        expected=sum(v['bytes'] for v in entries.values() if stat.S_ISREG(v['mode']))
        present=sum(v['allocated_bytes'] for v in current.values() if stat.S_ISREG(v['mode']))
        formulas.append({'item':'cache-copy size','formula':'sum(actual source file sizes)', 'source_bytes':expected})
        add('cache-copy remaining',expected,present,copy_destination)
    plan_path = work/'tool-plan.json'; tool_log = work/'tool-build.txt'
    try:
        plan = json.loads(plan_path.read_text()); descriptions = plan['descriptions']
        done = []; previous = None
        for line in tool_log.read_text(errors='replace').splitlines() if tool_log.is_file() else []:
            match = re.fullmatch(r'\[\d+/\d+\] (.+)', line)
            if match:
                previous = match[1]
                if previous in descriptions and previous not in done: done.append(previous)
            elif line.startswith('FAILED:') and previous in done: done.remove(previous)
        outputs = [task_output(build, d) for d in done]
        if any(p is None or not p.is_file() for p in outputs):
            unknown.append('some completed tool tasks have no measurable output')
        elif done:
            total = sum(file_size(p) for p in set(outputs)); remaining = len(descriptions)-len(done)
            predicted = (total*remaining+len(done)-1)//len(done)
            partial = sum(allocation(p) for d in descriptions if d not in done for p in [task_output(build,d)] if p is not None)
            formulas.append({'item': 'tool-build', 'formula': 'ceil(completed_output_bytes / completed_tasks * remaining_tasks)',
                             'completed_output_bytes': total, 'completed_tasks': len(done),
                             'remaining_tasks': remaining, 'predicted_output_bytes': predicted})
            add('tool-build remaining', predicted, partial, build)
        elif descriptions: unknown.append('tool completed_tasks=0: no measured per-task size; cannot divide by zero')
    except (OSError, ValueError, KeyError, TypeError): unknown.append('tool plan unavailable; no fabricated tool budget')
    ordinary = work/'ordinary-clang-22'; source = build/'bin/clang-22'
    ordinary_size = file_size(source) or file_size(ordinary)
    if not ordinary_size: unknown.append('ordinary-clang-22 size unavailable')
    formulas.append({'item': 'ordinary-input', 'formula': 'actual ordinary clang file size',
                     'build_clang_bytes': file_size(source), 'saved_ordinary_bytes': file_size(ordinary)})
    add('ordinary-copy', ordinary_size, allocation(ordinary), work)
    profile = work/'profile.fdata'
    if not completed(work/'unpack.log'):
        source_name = os.environ.get('BOLT_PROFILE_SOURCE')
        if source_name:
            try:
                profile_bytes = 0
                with lzma.open(source_name,'rb') as stream:
                    for chunk in iter(lambda: stream.read(1024*1024),b''): profile_bytes += len(chunk)
                formulas.append({'item':'profile-size','formula':'stream-count actual decompressed Source bytes without writing a file',
                                 'source':source_name,'decompressed_bytes':profile_bytes})
                add('profile unpack',profile_bytes,allocation(profile),work)
            except (OSError,lzma.LZMAError): unknown.append('profile Source cannot be measured')
        elif not profile.is_file(): unknown.append('profile Source size unavailable')
    reference = work/'reference-relocs-clang-22'; rewritten = work/'clang.bolt'; candidate = work/'clang.candidate'
    relink_size = max(ordinary_size, file_size(reference))
    if not completed(work/'reference-relocs.log'):
        formulas.append({'item':'relink-size', 'formula':'max(ordinary_bytes, observed_reference_bytes)',
                         'ordinary_bytes':ordinary_size, 'observed_reference_bytes':file_size(reference)})
        add('relink', relink_size, allocation(reference), work)
    reference_size = (file_size(reference) or relink_size) if completed(work/'reference-relocs.log') else relink_size
    if not completed(work/'reference-strip.log'):
        add('strip-debug temporary', reference_size, 0, work, temporary=True)
    rewrite_size = file_size(rewritten) if completed(work/'rewrite/bolt.log') else max(reference_size, file_size(rewritten))
    if not completed(work/'rewrite/bolt.log'):
        formulas.append({'item':'rewrite-size', 'formula':'max(observed_input_bytes, observed_partial_output_bytes)',
                         'observed_input_bytes':reference_size, 'observed_partial_output_bytes':file_size(rewritten)})
        add('BOLT rewrite', rewrite_size, allocation(rewritten), work)
    if not completed(work/'identity.strip.log'):
        predicted_candidate = max(rewrite_size, file_size(candidate))
        add('strip-all candidate copy', predicted_candidate, allocation(candidate), work)
        add('strip-all temporary', predicted_candidate, 0, work, temporary=True)
    install_size = file_size(candidate) or rewrite_size
    if root:
        entity = root/'usr/bin/clang-22'
        try: installed = file_size(candidate)>0 and digest(entity)==digest(candidate)
        except OSError: installed=False
        if not installed:
            add('atomic install temporary', install_size, allocation(entity.with_name('.clang-bolt.new')), entity.parent, temporary=True)
    cache_delta = measured['cache_delta_allocated_bytes']
    formulas.append({'item':'ThinLTO observed cache allocation', 'formula':'sum(max(current_allocation - baseline_allocation, 0)) per retained cache entry; new entries use current allocation',
                     'observed_bytes':cache_delta, 'already_in_used_bytes':True,
                     'additional_prediction_bytes':0, 'note':'Observed growth is retained once; future unobserved cache growth cannot be predicted from file sizes.'})
    if not measured['cache_delta_known']: unknown.append('cache baseline path mismatch')
    if not completed(work/'reference-relocs.log'):
        unknown.append('future ThinLTO growth is unobserved; measured retained cache delta is included once in used bytes')
    return {'estimated_remaining_bytes':peak, 'estimated_total_bytes':measured['owned_filesystem_bytes'].get(device,0)+peak,
            'formulas':formulas, 'incomplete_estimate':bool(unknown), 'unknown_components':unknown,
            'requirement_scope':'failure filesystem, retained outputs plus peak temporary allocation; lower bound when components are unknown'}


def disk_diagnose(step, log, error=None, build=None, work=None, root=None):
    """Read-only, failure evidence only; failures here never replace the error."""
    text, available = disk_failure_log(log)
    evidence = disk_evidence(log,error,log_text=text)
    cause = 'disk' if evidence else ('not-disk' if available else 'unknown')
    value = {'cause': cause, 'step': step, 'free_bytes': None}
    if cause == 'unknown':
        value.update(used_bytes=None,reason='日志不可用，无法判定原因')
    try:
        build, work, root = disk_context(build, work, root)
        target = root/'usr/bin' if root and step == 'install' else work
        value.update(free_bytes=filesystem(target)['free_bytes'])
        if cause in ('disk','unknown'):
            device=filesystem(target)['device']
            if cause == 'disk':
                value.update(filesystem_device=device, evidence=evidence,
                             estimate_note='估计值，依据本次构建实际文件大小',
                             errno_messages=[os.strerror(int(item.split('=')[1])) for item in evidence if item.startswith('errno=')])
            baseline = None
            try:
                baseline=json.loads((work/'disk-baseline.json').read_text())
                if not (isinstance(baseline,dict) and isinstance(baseline.get('time_ns'),int)
                        and isinstance(baseline.get('cache_entries'),dict)
                        and all(isinstance(x,dict) and isinstance(x.get('allocated_bytes'),int)
                                and isinstance(x.get('bytes'),int) for x in baseline['cache_entries'].values())):
                    baseline=None
            except (OSError, ValueError): pass
            measured = disk_measure(build,work,baseline)
            value['used_bytes']=measured['owned_filesystem_bytes'].get(device,0)
            if cause == 'disk': value['cache_delta_known']=measured['cache_delta_known']
            if cause == 'unknown':
                pass
            elif baseline is None:
                value.update(degraded='records unavailable: only current free and owned allocation are reliable')
            else:
                value.update(disk_prediction(build,work,root,measured,baseline,device))
                current=error;seen=set()
                while current is not None and id(current) not in seen:
                    seen.add(id(current))
                    if hasattr(current,'bolt_write_bytes') and filesystem(current.bolt_write_path)['device']==device:
                        count=current.bolt_write_bytes
                        value['formulas'].append({'item':'failed atomic text/JSON output','formula':'actual UTF-8 serialization length; failed temporary removed',
                                                  'path':current.bolt_write_path,'expected_output_bytes':count})
                        value['estimated_remaining_bytes']+=count;value['estimated_total_bytes']+=count
                        break
                    current=current.__cause__ or current.__context__
                value['shortfall_bytes']=max(0,value['estimated_remaining_bytes']-value['free_bytes'])
                value['total_formula']='used_bytes + estimated_remaining_bytes'
                value['shortfall_formula']='max(estimated_remaining_bytes - free_bytes, 0)'
                if any('122' in item or 'quota' in item.lower() for item in value['evidence']):
                    value['quota_headroom_unknown']=True
    except Exception as failure:
        if cause in ('disk','unknown'):
            value['degraded']=str(failure)
    try: print('BOLT_DISK_DIAGNOSIS '+json.dumps(value,ensure_ascii=False),flush=True)
    except Exception: pass
    return value


def diagnose_safely(step, log, error=None):
    try: return disk_diagnose(step,log,error)
    except Exception: return None


def run_step(step, log, argv, output=None, success_marker=None):
    os.environ['BOLT_STEP_LOG'] = str(log)
    try:
        text = call(argv,log,timeout=None)
        if success_marker:
            with Path(log).open('a') as stream:
                require(stream.write(success_marker+'\n')==len(success_marker)+1,'short build-success marker write');stream.flush();os.fsync(stream.fileno())
            text += success_marker+'\n'
        if output: atomic_text(output,text)
        print(text,end='',flush=True)
        return {'step':step,'log':str(log),'output':str(output) if output else None}
    except BaseException as error:
        # Preserve the failed command's actual output even when its exit is nonzero.
        try: print(Path(log).read_text(errors='replace'),end='',flush=True)
        except Exception: pass
        raise


def pipeline(build, work, bolt, cache=None):
    build, work = Path(build).absolute(), Path(work).absolute()
    baseline = work/'installed-baseline.json'
    require(baseline.is_file(), 'installed-baseline missing: '+str(baseline))
    edge = (work/'link.original').read_text()
    reference = work/'reference-relocs-clang-22'
    require(not reference.exists(), 'relink output must be new')
    script = work/'reference-relocs.sh'
    atomic_text(script,replay_script(edge,reference,work/'reference-relocs.d',cache))
    call(['/bin/sh',str(script)],work/'reference-relocs.log',cwd=build,timeout=1800)
    call([str(build/'bin/llvm-strip'),'--strip-debug',str(reference)],work/'reference-strip.log',timeout=600)
    result = rewrite(str(bolt),str(work/'profile.fdata'),str(reference),str(work/'clang.bolt'),work/'rewrite')
    tiny_gate(str(work/'ordinary-clang-22'),str(work/'clang.bolt'),work/'prestrip-gate',str(build/'lib64/clang/22'))
    real_prestrip = real_gate(work/'ordinary-clang-22',work/'clang.bolt',build,work/'prestrip-real',build/'lib64/clang/22')
    identity = strip_all(str(build/'bin/llvm-strip'),work/'clang.bolt',work/'clang.candidate',work/'identity.json')
    identity = adjust_rpath(work/'clang.candidate',baseline,work,identity)
    security = security_compare(str(work/'ordinary-clang-22'), str(work/'clang.candidate'), ignore_paths=True)
    tiny_gate(str(work/'ordinary-clang-22'),str(work/'clang.candidate'),work/'preinstall-gate',str(build/'lib64/clang/22'))
    real_final = real_gate(work/'ordinary-clang-22',work/'clang.candidate',build,work/'preinstall-real',build/'lib64/clang/22')
    result.update(real_prestrip=real_prestrip, real_final=real_final, identity=identity, security=security, input_policy='emit-relocs-then-strip-debug',
                  cache_policy='original-in-place' if cache is None else 'explicit-copy')
    save(work/'pipeline-result.json',result)
    return result

def cache_manifest(root):
    root = Path(root)
    require(root.is_dir(), 'ThinLTO cache directory missing')
    rows = []
    for p in sorted(root.rglob('*')):
        require(not p.is_symlink(), 'cache symlink is unsupported')
        if p.is_file():
            st = p.stat()
            rows.append({'path': p.relative_to(root).as_posix(), 'bytes': st.st_size,
                         'mtime_ns': st.st_mtime_ns})
        else:
            require(p.is_dir(), 'cache contains a special file')
    # Deterministic samples spanning the full sorted file list; timestamps are also frozen.
    indices = sorted(set([0, len(rows)-1] + list(range(0, len(rows), max(1,len(rows)//32))))) if rows else []
    samples = {rows[i]['path']: digest(root/rows[i]['path']) for i in indices}
    return {'files': rows, 'count': len(rows), 'bytes': sum(r['bytes'] for r in rows), 'samples': samples}

def cache_copy(edge, destination, result):
    matches = re.findall(r'--thinlto-cache-dir=([^\s]+)', edge)
    require(len(matches) == 1, 'cache path is not unique')
    source, destination = Path(matches[0]), Path(destination).absolute()
    require(source.is_absolute() and source != destination and not destination.exists(), 'unsafe cache destination')
    before = cache_manifest(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination, copy_function=shutil.copy2)
    copied = cache_manifest(destination)
    require(before == copied, 'cache copy file count/size/mtime/sample SHA differs')
    require(cache_manifest(source) == before, 'original cache changed during copy')
    value = {'source': str(source), 'copy': str(destination), 'before': before, 'copied': copied}
    save(result, value)
    print(json.dumps({'cache_copy': {'count': before['count'], 'bytes': before['bytes'], 'copy': str(destination)}}), flush=True)
    return value

def cache_unchanged(state):
    require(cache_manifest(state['source']) == state['before'], 'original ThinLTO cache changed')
    return True

def validate_identity(identity, candidate):
    if 'rpath_adjusted_sha256' in identity:
        require(identity['after_sha256'] == identity['rpath_adjusted_sha256'], 'RPATH identity SHA inconsistent')
        require(digest(identity['installed_baseline_path']) == identity['installed_baseline_sha256'],
                'installed-baseline SHA changed')
    require(identity.get('bolt_note_before') is True, 'unproven pre-strip BOLT identity')
    require(identity.get('before_sha256') == digest(identity['before_path']), 'pre-strip SHA changed')
    before = ELF(identity['before_path'])
    try:
        before.audit()
    finally:
        before.close()
    require(digest(candidate) == identity.get('rpath_adjusted_sha256', identity.get('after_sha256')), 'stripped candidate SHA mismatch')
    final = ELF(candidate)
    try:
        final.audit(final=True)
    finally:
        final.close()

def strip_all(tool, before, after, result):
    before, after = Path(before).absolute(), Path(after).absolute()
    require(not after.exists() and before != after, 'strip-all output must be new')
    e = ELF(before)
    try:
        audit = e.audit()
    finally:
        e.close()
    before_sha = digest(before)
    shutil.copy2(before, after)
    call([str(tool), '--strip-all', str(after)], Path(result).with_suffix('.strip.log'), timeout=600)
    identity = {'before_path': str(before), 'before_sha256': before_sha, 'bolt_note_before': True,
                'bolt_sections_before': audit['bolt_sections'], 'after_path': str(after),
                'after_sha256': digest(after), 'strip_tool_sha256': digest(tool)}
    validate_identity(identity, after)
    save(result, identity)
    print(json.dumps({'BOLT_STRIP_IDENTITY': identity}), flush=True)
    return identity

def package_compare(ordinary, candidate, mode, proof):
    """Local RPM payload comparison. Proof binds per-path DWARF provenance to baseline.

    The proof must be generated/reviewed from ordinary DWARF and ALL other debuginfo
    (see design). Missing evidence fails; a path pattern alone is never proof.
    Root entries are package-qualified: main/, debuginfo/, debugsource/.
    """
    require(mode in ('debug','release'), 'unknown package mode')
    old, new = ordinary['files'], candidate['files']
    require(new.keys() <= old.keys(), 'RPM added a file')
    entity = 'main/usr/bin/clang-22'
    require(entity in old and entity in new, 'RPM lost clang-22')
    require(old[entity]['type'] == new[entity]['type'] == 'file' and
            old[entity]['mode'] == new[entity]['mode'], 'clang entity type/mode changed')
    aliases = set(proof.get('aliases', []))
    for key in aliases:
        require(key.startswith('main/usr/bin/') and key != entity and key in old,
                'invalid baseline alias')
        # Alias evidence is produced by alias_group on the ordinary extraction root.
        require(proof.get('alias_baseline', {}).get(key) == old[key], 'unproven clang alias')
    removed = sorted(old.keys()-new.keys()); changed = []
    for key in sorted(new):
        if old[key] == new[key]:
            continue
        if key == entity:
            changed.append(key);continue
        if key in aliases:
            require(new[key] == {'type':'symlink','target':'clang-22'}, 'alias is not normalized')
            changed.append(key);continue
        raise GateError('non-clang RPM file changed: '+key)
    for key in removed:
        require(mode == 'debug', 'release RPM lost a file: '+key)
        item = proof.get('removed', {}).get(key)
        require(item is not None and item.get('baseline') == old[key], 'missing or mismatched DWARF provenance: '+key)
        evidence = item.get('evidence', {})
        require(evidence.get('clang_debug_sha256') and evidence.get('dwarf_dump_sha256') and
                evidence.get('all_other_debug_manifest_sha256'), 'incomplete DWARF evidence: '+key)
        if key.startswith('debuginfo/'):
            require(item.get('kind') in ('clang_debug','clang_build_id') and
                    evidence.get('owner') == 'usr/bin/clang-22', 'debug file not owned by clang-22')
        elif key.startswith('debugsource/'):
            require(item.get('kind') == 'exclusive_source' and evidence.get('referenced_by') == ['usr/bin/clang-22'] and
                    evidence.get('source_path'), 'source not proven exclusive to clang-22')
        else:
            raise GateError('unexpected missing file: '+key)
    return {'mode':mode, 'pass':True, 'changed':changed, 'removed':removed,
            'proof_sha256':hashlib.sha256(json.dumps(proof,sort_keys=True).encode()).hexdigest()}

def main():
    p = argparse.ArgumentParser(description=__doc__); sub = p.add_subparsers(dest='cmd',required=True)
    sub.add_parser('preflight'); sub.add_parser('certified')
    s=sub.add_parser('security');s.add_argument('ordinary');s.add_argument('candidate')
    s=sub.add_parser('tool-prepare');s.add_argument('build');s.add_argument('plan');s.add_argument('state')
    s=sub.add_parser('tool-verify');s.add_argument('build');s.add_argument('plan');s.add_argument('log');s.add_argument('state');s.add_argument('result')
    s=sub.add_parser('tool-plan');s.add_argument('input')
    s=sub.add_parser('pipeline');s.add_argument('build');s.add_argument('work');s.add_argument('tool');s.add_argument('--cache-dir')
    s=sub.add_parser('strip-all');s.add_argument('tool');s.add_argument('before');s.add_argument('after');s.add_argument('identity')
    s=sub.add_parser('cache-release');s.add_argument('build');s.add_argument('work')
    s=sub.add_parser('cache-copy');s.add_argument('edge');s.add_argument('destination');s.add_argument('result')
    s=sub.add_parser('package-compare');s.add_argument('ordinary');s.add_argument('candidate');s.add_argument('mode',choices=['debug','release']);s.add_argument('proof');s.add_argument('result')
    s=sub.add_parser('unpack');s.add_argument('source');s.add_argument('output')
    s=sub.add_parser('replay');s.add_argument('edge');s.add_argument('output');s.add_argument('dependency');s.add_argument('script');s.add_argument('--cache-dir')
    s=sub.add_parser('rewrite');s.add_argument('tool');s.add_argument('profile');s.add_argument('input');s.add_argument('output');s.add_argument('work')
    s=sub.add_parser('tiny');s.add_argument('ordinary');s.add_argument('candidate');s.add_argument('work');s.add_argument('--resource-dir')
    s=sub.add_parser('installed-baseline');s.add_argument('root');s.add_argument('output')
    s=sub.add_parser('snapshot');s.add_argument('root');s.add_argument('output')
    s=sub.add_parser('compare-root');s.add_argument('root');s.add_argument('baseline');s.add_argument('after')
    s=sub.add_parser('install');s.add_argument('root');s.add_argument('candidate');s.add_argument('state');s.add_argument('identity')
    s=sub.add_parser('post');s.add_argument('root');s.add_argument('state');s.add_argument('ordinary');s.add_argument('work');s.add_argument('--resource-dir')
    s=sub.add_parser('disk-report');s.add_argument('stage',choices=['begin','tool-built','pipeline','post']);s.add_argument('--build');s.add_argument('--work');s.add_argument('--root')
    s=sub.add_parser('disk-diagnose');s.add_argument('step');s.add_argument('log');s.add_argument('--build');s.add_argument('--work');s.add_argument('--root')
    s=sub.add_parser('run-step');s.add_argument('step');s.add_argument('log');s.add_argument('--output');s.add_argument('--success-marker');s.add_argument('argv',nargs=argparse.REMAINDER)
    a=p.parse_args()
    _DISK_CONTEXT.clear()
    _DISK_CONTEXT['step']=getattr(a,'step',a.cmd)
    if a.cmd=='pipeline': _DISK_CONTEXT.update(build=a.build,work=a.work)
    elif a.cmd=='install': _DISK_CONTEXT.update(root=a.root)
    elif a.cmd=='cache-copy':
        try:
            cache_paths=re.findall(r'--thinlto-cache-dir=([^\s]+)',Path(a.edge).read_text())
            if len(cache_paths)==1:_DISK_CONTEXT.update(copy_source=cache_paths[0],copy_destination=a.destination)
        except OSError:pass
    if a.cmd=='cache-release':
        cache_release(a.build,a.work);return
    if a.cmd in ('disk-report','disk-diagnose'):
        try:
            if a.cmd=='disk-report':disk_report(a.stage,a.build,a.work,a.root)
            else:disk_diagnose(a.step,a.log,build=a.build,work=a.work,root=a.root)
        except Exception:pass
        return
    if a.cmd=='run-step':
        # REMAINDER begins after step/log: parse optional output flags explicitly.
        args=list(a.argv);output=a.output;marker=a.success_marker
        while args and args[0].startswith('--') and args[0]!='--':
            flag=args.pop(0)
            require(flag in ('--output','--success-marker') and args, 'invalid run-step option')
            value=args.pop(0)
            if flag=='--output':output=value
            else:marker=value
        if args and args[0]=='--':args.pop(0)
        require(args, 'run-step requires -- command')
        run_step(a.step,a.log,args,output,marker);return
    if a.cmd=='preflight':result=preflight()
    elif a.cmd=='certified':result=certified()
    elif a.cmd=='security':result=security_compare(a.ordinary,a.candidate)
    elif a.cmd=='tool-prepare':result=tool_prepare(a.build,json.loads(Path(a.plan).read_text()),a.state)
    elif a.cmd=='tool-verify':
        result=tool_verify(a.build,json.loads(Path(a.plan).read_text()),Path(a.log).read_text(),json.loads(Path(a.state).read_text()));save(a.result,result)
    elif a.cmd=='tool-plan':result=tool_plan(Path(a.input).read_text())
    elif a.cmd=='pipeline':result=pipeline(a.build,a.work,a.tool,a.cache_dir)
    elif a.cmd=='strip-all':result=strip_all(a.tool,a.before,a.after,a.identity)
    elif a.cmd=='cache-copy':result=cache_copy(Path(a.edge).read_text(),a.destination,a.result)
    elif a.cmd=='package-compare':
        result=package_compare(json.loads(Path(a.ordinary).read_text()),json.loads(Path(a.candidate).read_text()),a.mode,json.loads(Path(a.proof).read_text()));save(a.result,result)
    elif a.cmd=='unpack':result=profile_unpack(a.source,a.output)
    elif a.cmd=='replay':
        script=replay_script(Path(a.edge).read_text(),a.output,a.dependency,a.cache_dir)
        atomic_text(a.script,script);Path(a.script).chmod(0o755);result={'script':a.script}
    elif a.cmd=='rewrite':result=rewrite(a.tool,a.profile,a.input,a.output,a.work)
    elif a.cmd=='tiny':result=tiny_gate(a.ordinary,a.candidate,a.work,a.resource_dir)
    elif a.cmd=='installed-baseline':result=installed_baseline(a.root,a.output)
    elif a.cmd=='snapshot':result=root_snapshot(a.root);save(a.output,result)
    elif a.cmd=='compare-root':result=compare_root(a.root,json.loads(Path(a.baseline).read_text()),a.after)
    elif a.cmd=='install':
        install_candidate(a.root,a.candidate,a.state,json.loads(Path(a.identity).read_text()),announce=True,identity_path=a.identity);return
    elif a.cmd=='post':
        result=post_gate(a.root,json.loads(Path(a.state).read_text()),a.ordinary,a.work,
                         a.resource_dir);save(Path(a.work)/'post-result.json',result)
    print(json.dumps(result,ensure_ascii=False),flush=True)

def cli():
    try:
        main()
        return 0
    except (GateError, OSError, ValueError, lzma.LZMAError) as error:
        step = _DISK_CONTEXT.get('step') or (sys.argv[1] if len(sys.argv)>1 else 'helper')
        log = getattr(error,'bolt_log',None) or os.environ.get('BOLT_STEP_LOG','-')
        diagnose_safely(step,log,error)
        print('BOLT_GATE_FAILED: '+str(error),file=sys.stderr)
        return 1


if __name__=='__main__':
    sys.exit(cli())
