#!/usr/bin/env python3
"""Tizen clang BOLT draft. Every command fails closed; Python >= 3.9, POSIX sh."""
import argparse
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

PROFILE_SHA = 'd9b132f9430dfed32e080c65b4422bd76eba4a9c2101a2b18a7f66c94133b326'
OPTIONS = ['-reorder-blocks=ext-tsp', '-reorder-functions=cdsort', '-split-functions',
           '-split-all-cold', '-split-eh', '-dyno-stats', '--thread-count=1', '-stale-threshold=5']
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

def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.new')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    os.replace(tmp, path)

def live_group_members(group):
    members = []
    for path in Path('/proc').glob('[0-9]*/stat'):
        try:
            # comm may contain spaces and parentheses; the final ')' delimits it.
            fields = path.read_text().rsplit(')', 1)[1].split()
        except (FileNotFoundError, ProcessLookupError):
            continue
        except (OSError, IndexError) as error:
            raise GateError('cannot inspect process group member: '+str(path)) from error
        require(len(fields) >= 3, 'malformed process stat: '+str(path))
        if int(fields[2]) == group and fields[0] not in ('Z', 'X'):
            members.append((int(path.parent.name), fields[0]))
    return sorted(members)

def wait_group_exit(group, timeout=10):
    deadline = time.monotonic() + timeout
    while True:
        members = live_group_members(group)
        if not members:
            return
        require(time.monotonic() < deadline,
                'process group %d still alive after %s seconds: %s' %
                (group, timeout, ', '.join('%d:%s' % item for item in members)))
        time.sleep(0.02)

def call(argv, log, cwd=None, timeout=300):
    log = Path(log)
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.with_suffix(log.suffix + '.argv.json').open('w') as f:
        json.dump({'argv': list(map(str, argv)), 'cwd': str(cwd) if cwd else None}, f)
    process = None
    try:
        with log.open('wb') as f:
            process = subprocess.Popen(list(map(str, argv)), cwd=cwd, stdout=f,
                                       stderr=subprocess.STDOUT, start_new_session=True)
            rc = process.wait(timeout=timeout)
            require(rc == 0, 'COMMAND_FAILED rc=%s: %s' % (rc, argv[0]))
        return log.read_text(errors='replace')
    except BaseException as error:
        cleanup_error = None
        if process is not None:
            try:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                try:
                    process.wait()
                finally:
                    wait_group_exit(process.pid)
            except Exception as cleanup:
                cleanup_error = cleanup
        if cleanup_error is not None:
            raise GateError('%s; original error: %s (see %s)' %
                            (cleanup_error, error, log)) from error
        if isinstance(error, (KeyboardInterrupt, SystemExit)):
            raise
        raise GateError('%s: %s (see %s)' %
                        ('TIMEOUT' if isinstance(error, subprocess.TimeoutExpired) else 'COMMAND_ERROR',
                         error, log)) from error

def profile_unpack(source, output):
    output = Path(output)
    require(not output.exists(), 'profile output must be new')
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with lzma.open(source, 'rb') as src, output.open('xb') as dst:
            shutil.copyfileobj(src, dst, 1024 * 1024)
        require(digest(output) == PROFILE_SHA, 'profile uncompressed SHA mismatch')
    except Exception:
        if output.exists():
            output.unlink()
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
    require('&&' not in body and ';' not in body and '`' not in body and '$(' not in body,
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
    require(100 * (s + u) <= 5 * (n + u), 'profile R exceeds 5 percent')
    require(100 * s <= 5 * n, 'profile S/N exceeds 5 percent')
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
            require(shndx != 65535, 'XINDEX not supported')
            target = self.names[shndx] if shndx < len(self.names) else 'RESERVED:%d' % shndx
            result.append((self.string(strings[4], strings[5], name), info, other, target, value, size))
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
            return bytes(e.mm[section[4]:section[4]+section[5]])
        def headers(kind):
            return [p for p in e.phdrs if p[0] == kind]
        def header_values(kind, payload=False):
            values = []
            for p in headers(kind):
                value = {'flags': p[1]}
                if payload:
                    e.range(p[2], p[5])
                    value['content_hex'] = bytes(e.mm[p[2]:p[2]+p[5]]).hex()
                values.append(value)
            return values
        interp = [e.string(p[2], p[5], 0) for p in headers(3)]
        dynamic = e.by_name.get('.dynamic'); needed = []; flags = {}
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
        verneed = e.by_name.get('.gnu.version_r'); needs = []; version_names = {0: 'LOCAL', 1: 'GLOBAL'}
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
                    version_names[other & 0x7fff] = name
                    needs.append((filename, name, value_flags, value_hash))
                    if index+1 < count:
                        require(next_aux > 0, 'truncated vernaux chain')
                        position += next_aux
                if not following:
                    break
                cursor += following
        require(not version_values or len(version_values) == len(syms), 'versym/dynsym count mismatch')
        require(all((value & 0x7fff) in version_names for value in version_values), 'unknown symbol version')
        named_versions = sorted((syms[i][0], version_names[value & 0x7fff], bool(value & 0x8000))
                                for i, value in enumerate(version_values))
        return {'elf_type': e.elf_type, 'PT_INTERP': interp,
                'PT_GNU_RELRO': header_values(0x6474e552), 'PT_GNU_STACK': header_values(0x6474e551),
                'PT_GNU_PROPERTY': header_values(0x6474e553, True),
                '.note.gnu.property': content(e.by_name['.note.gnu.property']).hex() if '.note.gnu.property' in e.by_name else None,
                'DT_FLAGS_FLAGS1': flags, 'DT_NEEDED': needed,
                '.dynsym': sorted((s[0], s[1] >> 4, s[2] & 3) for s in syms),
                '.gnu.version': named_versions, '.gnu.version_r': sorted(needs)}
    finally:
        e.close()

def security_compare(ordinary, candidate):
    before, after = security_properties(ordinary), security_properties(candidate)
    differences = [key for key in before if before[key] != after[key]]
    require(not differences, 'ELF security attributes differ: '+', '.join(differences))
    heavy = ('.dynsym', '.gnu.version', '.gnu.version_r')
    return {'security_preserved': True,
            'ordinary_sha256': digest(ordinary), 'candidate_sha256': digest(candidate),
            'properties': {key: value for key, value in before.items() if key not in heavy},
            'symbol_version_evidence': {key: {'entries': len(before[key]),
                'sha256': hashlib.sha256(json.dumps(before[key], sort_keys=True).encode()).hexdigest()}
                for key in heavy}}

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

def inventory(root):
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
                files[key] = {'type': 'file', 'mode': stat.S_IMODE(st.st_mode), 'bytes': st.st_size, 'sha256': digest(p)}
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

def install_candidate(root, candidate, state, identity):
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
    st = entity.stat(); tmp = entity.with_name('.clang-bolt.new')
    disk_preflight(tmp.parent,Path(candidate).stat().st_size)
    shutil.copyfile(candidate, tmp); tmp.chmod(stat.S_IMODE(st.st_mode)); os.replace(tmp, entity)
    for p in aliases:
        tmp = p.with_name('.'+p.name+'.bolt-link'); require(not tmp.exists(), 'temporary alias exists')
        tmp.symlink_to('clang-22'); os.replace(tmp, p)
    result = {'installed_sha256': digest(entity), 'identity': identity, 'alias_changes': changed,
              'allowed_paths': ['usr/bin/clang-22'] + [p.relative_to(root).as_posix() for p in aliases], 'elf': elf}
    save(state, result); return result

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
    security = security_compare(ordinary, str(entity))
    rows = tiny_gate(ordinary, str(entity), candidate_work, resource_dir)
    return {'sha_unchanged': True, 'aliases_pass': True, 'elf': elf, 'tiny': rows,
            'strip_identity_pass': True, 'security': security}

def certified_version(text):
    lines = re.findall(r'^\s*(LLVM version[^\n]*)$', text, re.M)
    require(lines == ['LLVM version 22.1.8'], 'uncertified BOLT tool version')
    return lines[0]

def no_bolt_products(root):
    root = Path(root)
    for name in ('llvm-bolt', 'perf2bolt', 'llvm-boltdiff', 'merge-fdata'):
        p = root/'usr/bin'/name
        require(not p.exists() and not p.is_symlink(), 'BOLT tool in buildroot: '+str(p))
    require(not list((root/'usr/lib64').glob('libLLVMBOLT*.a')), 'BOLT static library in buildroot')
    # Inventory fails closed on traversal errors; inspect all installed CMake files,
    # a superset of exports including LLVMConfig.cmake and nested export metadata.
    for key, item in inventory(root)['files'].items():
        if key.lower().endswith('.cmake'):
            p = rooted_resolve(root, root/key)
            require(p.is_file(), 'unreadable CMake metadata: '+key)
            require(b'BOLT' not in p.read_bytes().upper(), 'BOLT CMake export: '+key)
    return {'no_bolt_products': True}

def rewrite(bolt, profile, input_elf, output, work):
    work = Path(work); work.mkdir(parents=True, exist_ok=True)
    require(digest(profile) == PROFILE_SHA, 'profile SHA mismatch')
    version = call([bolt, '--version'], work/'bolt-version.log')
    certified_version(version)
    disk_preflight(Path(output).parent,4*Path(input_elf).stat().st_size)
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

BOLT_TASK_DESCRIPTIONS = frozenset(('Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/AddressMap.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/BinaryBasicBlock.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/BinaryContext.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/BinaryData.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/BinaryEmitter.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/BinaryFunction.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/BinaryFunctionCallGraph.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/BinaryFunctionProfile.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/BinarySection.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/CallGraph.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/CallGraphWalker.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/DIEBuilder.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/DebugData.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/DebugNames.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/DynoStats.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/Exceptions.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/FunctionLayout.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/GDBIndex.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/HashUtilities.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/JumpTable.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/MCInstUtils.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/MCPlusBuilder.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/ParallelUtilities.cpp.o', 'Building CXX object tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir/Relocation.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/AArch64RelaxationPass.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/Aligner.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/AllocCombiner.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/AsmDump.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/BinaryPasses.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/CMOVConversion.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/CacheMetrics.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/DataflowAnalysis.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/DataflowInfoManager.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/FixRISCVCallsPass.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/FixRelaxationPass.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/FrameAnalysis.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/FrameOptimizer.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/HFSort.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/Hugify.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/IdenticalCodeFolding.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/IndirectCallPromotion.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/Inliner.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/Instrumentation.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/JTFootprintReduction.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/LivenessAnalysis.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/LongJmp.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/LoopInversionPass.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/MCF.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/PAuthGadgetScanner.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/PLTCall.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/PatchEntries.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/PettisAndHansen.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/PointerAuthCFIAnalyzer.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/PointerAuthCFIFixup.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/ProfileQualityStats.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/RegAnalysis.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/RegReAssign.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/ReorderAlgorithm.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/ReorderData.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/ReorderFunctions.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/RetpolineInsertion.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/ShrinkWrapping.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/SplitFunctions.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/StackAllocationAnalysis.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/StackAvailableExpressions.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/StackPointerTracking.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/StackReachingUses.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/StokeInfo.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/TailDuplication.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/ThreeWayBranch.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/ValidateInternalCalls.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/ValidateMemRefs.cpp.o', 'Building CXX object tools/bolt/lib/Passes/CMakeFiles/LLVMBOLTPasses.dir/VeneerElimination.cpp.o', 'Building CXX object tools/bolt/lib/Profile/CMakeFiles/LLVMBOLTProfile.dir/BoltAddressTranslation.cpp.o', 'Building CXX object tools/bolt/lib/Profile/CMakeFiles/LLVMBOLTProfile.dir/DataAggregator.cpp.o', 'Building CXX object tools/bolt/lib/Profile/CMakeFiles/LLVMBOLTProfile.dir/DataReader.cpp.o', 'Building CXX object tools/bolt/lib/Profile/CMakeFiles/LLVMBOLTProfile.dir/Heatmap.cpp.o', 'Building CXX object tools/bolt/lib/Profile/CMakeFiles/LLVMBOLTProfile.dir/StaleProfileMatching.cpp.o', 'Building CXX object tools/bolt/lib/Profile/CMakeFiles/LLVMBOLTProfile.dir/YAMLProfileReader.cpp.o', 'Building CXX object tools/bolt/lib/Profile/CMakeFiles/LLVMBOLTProfile.dir/YAMLProfileWriter.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/BinaryPassManager.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/BoltDiff.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/BuildIDRewriter.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/DWARFRewriter.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/ExecutableFileMemoryManager.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/GNUPropertyRewriter.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/JITLinkLinker.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/LinuxKernelRewriter.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/MachORewriteInstance.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/MetadataManager.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/PseudoProbeRewriter.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/RSeqRewriter.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/RewriteInstance.cpp.o', 'Building CXX object tools/bolt/lib/Rewrite/CMakeFiles/LLVMBOLTRewrite.dir/SDTRewriter.cpp.o', 'Building CXX object tools/bolt/lib/RuntimeLibs/CMakeFiles/LLVMBOLTRuntimeLibs.dir/HugifyRuntimeLibrary.cpp.o', 'Building CXX object tools/bolt/lib/RuntimeLibs/CMakeFiles/LLVMBOLTRuntimeLibs.dir/InstrumentationRuntimeLibrary.cpp.o', 'Building CXX object tools/bolt/lib/RuntimeLibs/CMakeFiles/LLVMBOLTRuntimeLibs.dir/RuntimeLibrary.cpp.o', 'Building CXX object tools/bolt/lib/Target/X86/CMakeFiles/LLVMBOLTTargetX86.dir/X86MCPlusBuilder.cpp.o', 'Building CXX object tools/bolt/lib/Target/X86/CMakeFiles/LLVMBOLTTargetX86.dir/X86MCSymbolizer.cpp.o', 'Building CXX object tools/bolt/lib/Utils/CMakeFiles/LLVMBOLTUtils.dir/CommandLineOpts.cpp.o', 'Building CXX object tools/bolt/lib/Utils/CMakeFiles/LLVMBOLTUtils.dir/Utils.cpp.o', 'Building CXX object tools/bolt/tools/driver/CMakeFiles/llvm-bolt.dir/llvm-bolt.cpp.o', 'Linking CXX executable bin/llvm-bolt', 'Linking CXX static library lib64/libLLVMBOLTCore.a', 'Linking CXX static library lib64/libLLVMBOLTPasses.a', 'Linking CXX static library lib64/libLLVMBOLTProfile.a', 'Linking CXX static library lib64/libLLVMBOLTRewrite.a', 'Linking CXX static library lib64/libLLVMBOLTRuntimeLibs.a', 'Linking CXX static library lib64/libLLVMBOLTTargetX86.a', 'Linking CXX static library lib64/libLLVMBOLTUtils.a'))

def tool_plan(text):
    counts = {'objects': 0, 'static_libraries': 0, 'executables': 0}
    lines = text.splitlines()
    require(bool(lines), 'empty BOLT tool plan')
    descriptions = []
    for line in lines:
        match = re.fullmatch(r'\[([0-9]+)/([0-9]+)\] (.+)', line)
        require(match is not None, 'non-progress line in BOLT tool plan: '+line)
        require(0 < int(match[1]) <= int(match[2]), 'invalid progress counters: '+line)
        body = match[3]
        require(body in BOLT_TASK_DESCRIPTIONS, 'unapproved BOLT task: '+body)
        descriptions.append(body)
        category = ('objects' if body.startswith('Building CXX object ') else
                    'static_libraries' if body.startswith('Linking CXX static library ') else 'executables')
        counts[category] += 1
    require('Linking CXX executable bin/llvm-bolt' in descriptions, 'missing llvm-bolt executable link')
    return {'tasks': len(lines), 'categories': counts, 'ordinary_compile_link_tasks': 0}

GIB = 1024**3
LARGE_WRITE = 10 * GIB
DISK_FLOOR = 30 * GIB
STAGE_WRITE_BUDGET = 16 * GIB

def disk_preflight(destination, planned_bytes, reserve_bytes=0):
    """Admission against a declared write upper bound on the destination filesystem.

    Include temporary outputs/cache growth in the caller's budget. Large writes
    must leave >=30 GiB after BOTH the write and any separately reserved space.
    The 16 GiB stage default is a conservative R1 estimate, not a cold-cache bound.
    """
    require(planned_bytes >= 0 and reserve_bytes >= 0, 'negative disk budget')
    destination = Path(destination).absolute()
    parent = destination
    while not parent.exists():
        parent = parent.parent
    require(parent.is_dir(), 'disk preflight requires a destination directory')
    free = shutil.disk_usage(parent).free
    floor = DISK_FLOOR if planned_bytes > LARGE_WRITE else 0
    value = {'destination':str(destination), 'filesystem_device':parent.stat().st_dev,
             'planned_write_bytes':planned_bytes, 'reserve_bytes':reserve_bytes,
             'free_before_bytes':free, 'projected_free_bytes':free-planned_bytes-reserve_bytes,
             'required_free_after_bytes':floor}
    require(value['projected_free_bytes'] >= floor,
            'SKIP_DISK: write/reserve would leave %d bytes; require %d bytes (planned %d)' %
            (value['projected_free_bytes'], floor, planned_bytes))
    return value

def pipeline(build, work, bolt, cache=None, planned_write_bytes=STAGE_WRITE_BUDGET):
    build, work = Path(build).absolute(), Path(work).absolute()
    edge = (work/'link.original').read_text()
    # Handed-off trees own their original cache; no copy, audit or path rewrite.
    # Protected trees must prepare a verified copy separately and pass --cache-dir.
    admission = disk_preflight(work, max(planned_write_bytes,
                                        4*(work/'ordinary-clang-22').stat().st_size))
    save(work/'disk-admission.json',admission)
    reference = work/'reference-relocs-clang-22'
    require(not reference.exists(), 'relink output must be new')
    script = work/'reference-relocs.sh'
    script.write_text(replay_script(edge,reference,work/'reference-relocs.d',cache))
    call(['/bin/sh',str(script)],work/'reference-relocs.log',cwd=build,timeout=1800)
    call([str(build/'bin/llvm-strip'),'--strip-debug',str(reference)],work/'reference-strip.log',timeout=600)
    result = rewrite(str(bolt),str(work/'profile.fdata'),str(reference),str(work/'clang.bolt'),work/'rewrite')
    tiny_gate(str(work/'ordinary-clang-22'),str(work/'clang.bolt'),work/'prestrip-gate',str(build/'lib64/clang/22'))
    identity = strip_all(str(build/'bin/llvm-strip'),work/'clang.bolt',work/'clang.candidate',work/'identity.json')
    security = security_compare(str(work/'ordinary-clang-22'), str(work/'clang.candidate'))
    tiny_gate(str(work/'ordinary-clang-22'),str(work/'clang.candidate'),work/'preinstall-gate',str(build/'lib64/clang/22'))
    result.update(identity=identity, security=security, input_policy='emit-relocs-then-strip-debug',
                  cache_policy='original-in-place' if cache is None else 'explicit-copy',
                  disk_admission=admission)
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
    admission = disk_preflight(destination.parent,before['bytes'],4*GIB)
    shutil.copytree(source, destination, copy_function=shutil.copy2)
    copied = cache_manifest(destination)
    require(before == copied, 'cache copy file count/size/mtime/sample SHA differs')
    require(cache_manifest(source) == before, 'original cache changed during copy')
    value = {'source': str(source), 'copy': str(destination), 'before': before, 'copied': copied, 'disk_admission':admission}
    save(result, value)
    print(json.dumps({'cache_copy': {'count': before['count'], 'bytes': before['bytes'], 'copy': str(destination)}}), flush=True)
    return value

def cache_unchanged(state):
    require(cache_manifest(state['source']) == state['before'], 'original ThinLTO cache changed')
    return True

def validate_identity(identity, candidate):
    require(identity.get('bolt_note_before') is True, 'unproven pre-strip BOLT identity')
    require(identity.get('before_sha256') == digest(identity['before_path']), 'pre-strip SHA changed')
    before = ELF(identity['before_path'])
    try:
        before.audit()
    finally:
        before.close()
    require(digest(candidate) == identity.get('after_sha256'), 'stripped candidate SHA mismatch')
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
    disk_preflight(after.parent,before.stat().st_size)
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
    s=sub.add_parser('security');s.add_argument('ordinary');s.add_argument('candidate')
    s=sub.add_parser('tool-plan');s.add_argument('input')
    s=sub.add_parser('pipeline');s.add_argument('build');s.add_argument('work');s.add_argument('tool');s.add_argument('--cache-dir');s.add_argument('--planned-write-bytes',type=int,default=STAGE_WRITE_BUDGET)
    s=sub.add_parser('disk-preflight');s.add_argument('destination');s.add_argument('planned_bytes',type=int);s.add_argument('--reserve-bytes',type=int,default=0)
    s=sub.add_parser('strip-all');s.add_argument('tool');s.add_argument('before');s.add_argument('after');s.add_argument('identity')
    s=sub.add_parser('cache-copy');s.add_argument('edge');s.add_argument('destination');s.add_argument('result')
    s=sub.add_parser('package-compare');s.add_argument('ordinary');s.add_argument('candidate');s.add_argument('mode',choices=['debug','release']);s.add_argument('proof');s.add_argument('result')
    s=sub.add_parser('unpack');s.add_argument('source');s.add_argument('output')
    s=sub.add_parser('replay');s.add_argument('edge');s.add_argument('output');s.add_argument('dependency');s.add_argument('script');s.add_argument('--cache-dir')
    s=sub.add_parser('rewrite');s.add_argument('tool');s.add_argument('profile');s.add_argument('input');s.add_argument('output');s.add_argument('work')
    s=sub.add_parser('tiny');s.add_argument('ordinary');s.add_argument('candidate');s.add_argument('work');s.add_argument('--resource-dir')
    s=sub.add_parser('snapshot');s.add_argument('root');s.add_argument('output')
    s=sub.add_parser('compare-root');s.add_argument('root');s.add_argument('baseline');s.add_argument('after')
    s=sub.add_parser('install');s.add_argument('root');s.add_argument('candidate');s.add_argument('state');s.add_argument('identity')
    s=sub.add_parser('post');s.add_argument('root');s.add_argument('state');s.add_argument('ordinary');s.add_argument('work');s.add_argument('--resource-dir')
    a=p.parse_args()
    if a.cmd=='security':result=security_compare(a.ordinary,a.candidate)
    elif a.cmd=='tool-plan':result=tool_plan(Path(a.input).read_text())
    elif a.cmd=='pipeline':result=pipeline(a.build,a.work,a.tool,a.cache_dir,a.planned_write_bytes)
    elif a.cmd=='disk-preflight':result=disk_preflight(a.destination,a.planned_bytes,a.reserve_bytes)
    elif a.cmd=='strip-all':result=strip_all(a.tool,a.before,a.after,a.identity)
    elif a.cmd=='cache-copy':result=cache_copy(Path(a.edge).read_text(),a.destination,a.result)
    elif a.cmd=='package-compare':
        result=package_compare(json.loads(Path(a.ordinary).read_text()),json.loads(Path(a.candidate).read_text()),a.mode,json.loads(Path(a.proof).read_text()));save(a.result,result)
    elif a.cmd=='unpack':result=profile_unpack(a.source,a.output)
    elif a.cmd=='replay':
        script=replay_script(Path(a.edge).read_text(),a.output,a.dependency,a.cache_dir)
        Path(a.script).write_text(script);Path(a.script).chmod(0o755);result={'script':a.script}
    elif a.cmd=='rewrite':result=rewrite(a.tool,a.profile,a.input,a.output,a.work)
    elif a.cmd=='tiny':result=tiny_gate(a.ordinary,a.candidate,a.work,a.resource_dir)
    elif a.cmd=='snapshot':result=root_snapshot(a.root);save(a.output,result)
    elif a.cmd=='compare-root':result=compare_root(a.root,json.loads(Path(a.baseline).read_text()),a.after)
    elif a.cmd=='install':result=install_candidate(a.root,a.candidate,a.state,json.loads(Path(a.identity).read_text()))
    elif a.cmd=='post':
        result=post_gate(a.root,json.loads(Path(a.state).read_text()),a.ordinary,a.work,
                         a.resource_dir);save(Path(a.work)/'post-result.json',result)
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':
    try:
        main()
    except (GateError, OSError, ValueError, lzma.LZMAError) as e:
        print('BOLT_GATE_FAILED: '+str(e),file=sys.stderr);sys.exit(1)
