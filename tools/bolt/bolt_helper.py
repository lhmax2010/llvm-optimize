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
import stat
import struct
import subprocess
import sys
import tempfile

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

def call(argv, log, cwd=None, timeout=300):
    log = Path(log)
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.with_suffix(log.suffix + '.argv.json').open('w') as f:
        json.dump({'argv': list(map(str, argv)), 'cwd': str(cwd) if cwd else None}, f)
    with log.open('wb') as f:
        try:
            p = subprocess.run(list(map(str, argv)), cwd=cwd, stdout=f, stderr=subprocess.STDOUT,
                               timeout=timeout)
        except subprocess.TimeoutExpired as e:
            raise GateError('TIMEOUT: ' + str(argv[0])) from e
    require(p.returncode == 0, 'COMMAND_FAILED rc=%s: %s (see %s)' % (p.returncode, argv[0], log))
    return log.read_text(errors='replace')

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
        self.mm = mmap.mmap(self.f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            require(self.mm[:6] == b'\x7fELF\x02\x01', 'expected ELF64 little endian')
            h = self.unpack('<16sHHIQQQIHHHHHH', 0)
            self.machine = h[2]; self.entry = h[4]
            phoff, shoff, phentsize, phnum, shentsize, shnum, stridx = h[5], h[6], h[9], h[10], h[11], h[12], h[13]
            require(shentsize == 64 and shnum > 0 and stridx < shnum, 'unsupported section numbering')
            self.sections = [self.unpack('<IIQQQQIIQQ', shoff + i * 64) for i in range(shnum)]
            names = self.sections[stridx]
            self.names = [self.string(names[4], names[5], s[0]) for s in self.sections]
            self.by_name = dict(zip(self.names, self.sections))
            require(len(self.by_name) == len(self.names), 'duplicate section name')
            self.loads = []
            for i in range(phnum):
                require(phentsize == 56, 'unsupported program header')
                p = self.unpack('<IIQQQQQQ', phoff + i * phentsize)
                if p[0] == 1:
                    self.loads.append(p)
        except Exception:
            self.close(); raise
    def close(self):
        self.mm.close(); self.f.close()
    def unpack(self, fmt, pos):
        require(pos >= 0 and pos + struct.calcsize(fmt) <= len(self.mm), 'ELF range error')
        return struct.unpack_from(fmt, self.mm, pos)
    def string(self, offset, size, start):
        require(start < size, 'ELF string index error')
        end = self.mm.find(b'\0', offset + start, offset + size)
        require(end >= 0, 'unterminated ELF string')
        return self.mm[offset + start:end].decode('utf-8', errors='surrogateescape')
    def symbols(self, index):
        sec = self.sections[index]; require(sec[1] in (2, 11), 'not a symbol table')
        require(sec[9] == 24 and sec[5] % 24 == 0 and sec[6] < len(self.sections), 'bad symtab')
        strings = self.sections[sec[6]]; result = []
        for off in range(sec[4], sec[4] + sec[5], 24):
            name, info, other, shndx, value, size = self.unpack('<IBBHQQ', off)
            require(shndx != 65535, 'XINDEX not supported')
            target = self.names[shndx] if shndx < len(self.names) else 'RESERVED:%d' % shndx
            result.append((self.string(strings[4], strings[5], name), info, other, target, value, size))
        return result
    def audit(self, final=False):
        require(self.machine == 62 and self.loads, 'not executable native x86_64 ELF')
        require(any(p[1] & 1 and p[3] <= self.entry < p[3] + p[6] for p in self.loads),
                'entry not inside executable LOAD')
        require(not any('debug' in n.lower() for n in self.names), 'BOLT clang contains a debug section')
        require('.gdb_index' not in self.by_name, 'BOLT clang contains a debug index')
        if final:
            require('.symtab' not in self.by_name and '.note.bolt_info' not in self.by_name, 'candidate is not fully stripped')
        else:
            require('.note.bolt_info' in self.by_name, 'missing BOLT note')
        return {'entry': self.entry, 'loads': self.loads, 'bolt_sections': [n for n in self.names if '.bolt' in n]}

def tiny_gate(ordinary, candidate, work, resource_dir=None):
    work = Path(work); work.mkdir(parents=True, exist_ok=True)
    source = work/'tiny.c'; source.write_text(TINY); out = work/'same.o'; rows = []
    for label, cc in [('ordinary', ordinary), ('candidate', candidate)]:
        call([cc, '--version'], work/(label+'-version.log'), timeout=30)
    for triple in TRIPLES:
        row = {'target': triple, 'outputs': []}
        for label, cc in [('ordinary', ordinary), ('candidate', candidate)]:
            argv = [cc, '--target='+triple, '-c', '-O2', str(source), '-o', str(out)]
            if resource_dir:
                argv[1:1] = ['-resource-dir', resource_dir]
            call(argv, work/(triple+'-'+label+'.log'), cwd=work, timeout=60)
            dest = work/(triple+'.'+label+'.o'); shutil.copyfile(out, dest)
            row['outputs'].append({'path': str(dest), 'sha256': digest(dest), 'bytes': dest.stat().st_size})
        row['byte_equal'] = (work/(triple+'.ordinary.o')).read_bytes() == (work/(triple+'.candidate.o')).read_bytes()
        rows.append(row); save(work/'result.json', rows)
        require(row['byte_equal'], 'tiny object differs: '+triple)
    return rows

def inventory(root):
    root = Path(root).absolute(); files = {}
    for folder, dirs, names in os.walk(root, followlinks=False):
        for name in sorted(dirs + names):
            p = Path(folder)/name; key = p.relative_to(root).as_posix(); st = p.lstat()
            require(not (stat.S_ISLNK(st.st_mode) and p in [root]), 'symlink root')
            if stat.S_ISLNK(st.st_mode):
                files[key] = {'type': 'symlink', 'target': os.readlink(p)}
            elif stat.S_ISREG(st.st_mode):
                files[key] = {'type': 'file', 'mode': stat.S_IMODE(st.st_mode), 'bytes': st.st_size, 'sha256': digest(p)}
            elif stat.S_ISDIR(st.st_mode):
                files[key] = {'type': 'dir'}
            else:
                raise GateError('special file in buildroot: '+key)
    return {'root': str(root), 'files': files}

def prune_install(root, baseline, installed_paths):
    root = Path(root).absolute(); before = baseline['files']; after = inventory(root)['files']
    require(before.keys() <= after.keys(), 'ordinary install file removed before BOLT cleanup')
    added = set(after) - set(before)
    allowed = {Path(p).relative_to(root).as_posix() for p in installed_paths}
    for key in sorted(added, key=lambda x: (x.count('/'), x), reverse=True):
        path = root/key
        require(after[key]['type'] == 'dir' or key in allowed, 'unregistered install addition: '+key)
        if after[key]['type'] == 'dir':
            path.rmdir()
        else:
            path.unlink()
    now = inventory(root)['files']; require(now == before, 'install file list/type/mode differs after cleanup')
    return {'removed': sorted(added), 'file_list_equal': True}

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
        elif p.name in ['clang', 'clang++', 'clang++-22'] or p.name.endswith(('-clang','-clang++')):
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
    rows = tiny_gate(ordinary, str(entity), candidate_work, resource_dir)
    return {'sha_unchanged': True, 'aliases_pass': True, 'elf': elf, 'tiny': rows,
            'strip_identity_pass': True}

def rewrite(bolt, profile, input_elf, output, work):
    work = Path(work); work.mkdir(parents=True, exist_ok=True)
    require(digest(profile) == PROFILE_SHA, 'profile SHA mismatch')
    version = call([bolt, '--version'], work/'bolt-version.log')
    require('LLVM version 22.1.8' in version, 'uncertified BOLT tool version')
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

def tool_plan(text):
    rows = [l.strip() for l in text.splitlines() if re.match(r"^\[\d+/\d+\]", l)]
    for line in rows:
        body = re.sub(r"^\[\d+/\d+\]\s*", "", line)
        if any(x in body for x in ['Building ', 'Linking ']):
            require('tools/bolt/' in body or 'bin/llvm-bolt' in body,
                    'ordinary compile/link would run: '+body)
    require(bool(rows) or 'no work to do' in text, 'unrecognized ninja dry-run format')
    return {'tasks': len(rows), 'ordinary_compile_link_tasks': 0}

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
    tiny_gate(str(work/'ordinary-clang-22'),str(work/'clang.candidate'),work/'preinstall-gate',str(build/'lib64/clang/22'))
    result.update(identity=identity, input_policy='emit-relocs-then-strip-debug',
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
    s=sub.add_parser('prune');s.add_argument('root');s.add_argument('before');s.add_argument('install_manifest');s.add_argument('result')
    s=sub.add_parser('install');s.add_argument('root');s.add_argument('candidate');s.add_argument('state');s.add_argument('identity')
    s=sub.add_parser('post');s.add_argument('root');s.add_argument('state');s.add_argument('ordinary');s.add_argument('work');s.add_argument('--resource-dir')
    a=p.parse_args()
    if a.cmd=='tool-plan':result=tool_plan(Path(a.input).read_text())
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
    elif a.cmd=='snapshot':result=inventory(a.root);save(a.output,result)
    elif a.cmd=='prune':
        result=prune_install(a.root,json.loads(Path(a.before).read_text()),Path(a.install_manifest).read_text().splitlines());save(a.result,result)
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
