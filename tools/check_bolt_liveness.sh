#!/usr/bin/env bash
# Functional smoke check, not a benchmark. Never strips or modifies the input ELF.
set -euo pipefail
exec python3 - "$@" <<'PY'
import argparse, hashlib, json, os, platform, re, shutil, signal, subprocess, sys
from pathlib import Path

p = argparse.ArgumentParser(description='Check native clang LOAD segments, entry, version and a minimal TU. '
    'Requires Python3, readelf, taskset, prlimit, nice, ionice. Each query has a 30s timeout, '
    '4 GiB AS, one CPU and no core dumps. No system installation; evidence directory must be new.')
p.add_argument('clang', type=Path)
p.add_argument('--output', required=True, type=Path)
p.add_argument('--loader', type=Path)
p.add_argument('--library-path')
p.add_argument('--target', default='armv7l-tizen-linux-gnueabi')
p.add_argument('--expected-load-count', type=int, help='Optional count from certified input at this layer')
a = p.parse_args()
if a.library_path and not a.loader: p.error('--library-path requires --loader')
for name in ('readelf', 'taskset', 'prlimit', 'nice', 'ionice'):
    if not shutil.which(name): p.error('missing '+name)
if not a.clang.is_file() or not os.access(a.clang, os.X_OK): p.error('input must be an executable regular ELF')
a.clang = a.clang.resolve()
try: a.output.mkdir(parents=True, exist_ok=False)
except FileExistsError: p.error('evidence directory already exists')
records = []
def run(argv, tag, bounded=False):
    argv = [str(x) for x in argv]
    if bounded:
        argv = ['nice','-n','15','ionice','-c3','taskset','-c',str(min(os.sched_getaffinity(0))),
                'prlimit','--as=4294967296','--core=0','--'] + argv
    with subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          start_new_session=True) as process:
        try:
            out, err = process.communicate(timeout=30)
            rc = process.returncode
        except subprocess.TimeoutExpired:
            # clang may spawn cc1. Reap the complete query group on timeout.
            try: os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError: pass
            out, err = process.communicate()
            rc = 124
        except BaseException:
            try: os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError: pass
            process.communicate()
            raise
    (a.output/(tag+'.stdout')).write_bytes(out)
    (a.output/(tag+'.stderr')).write_bytes(err)
    records.append(dict(argv=argv, tag=tag, returncode=rc))
    return rc, out.decode(errors='replace')
def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()
result = dict(input=str(a.clang), sha256=sha(a.clang), target=a.target)
try:
    rc, header = run(['readelf','-hW',a.clang], 'header')
    if rc: raise ValueError('readelf header failed')
    machine = re.search(r'^\s*Machine:\s*(.+)$', header, re.M).group(1)
    host = platform.machine()
    native = {'x86_64':'Advanced Micro Devices X86-64', 'aarch64':'AArch64'}
    if native.get(host) != machine: raise ValueError('native ELF required; use identity checker for foreign ELF')
    rc, ph = run(['readelf','-lW',a.clang], 'program-headers')
    if rc: raise ValueError('readelf program headers failed')
    entry = int(re.search(r'Entry point address:\s*(0x[0-9a-fA-F]+)', header).group(1),16)
    loads = []
    for line in ph.splitlines():
        fields = line.split()
        if fields and fields[0] == 'LOAD':
            loads.append(dict(offset=int(fields[1],16),vaddr=int(fields[2],16),
                filesz=int(fields[4],16),memsz=int(fields[5],16),flags=''.join(fields[6:-1])))
    inside = any(x['vaddr'] <= entry < x['vaddr']+x['memsz'] and 'E' in x['flags'] for x in loads)
    result.update(load_count=len(loads),entry=hex(entry),entry_in_executable_load=inside,loads=loads)
    prefix = ([str(a.loader)] + (['--library-path',a.library_path] if a.library_path else [])) if a.loader else []
    prefix += [str(a.clang)]
    vr, _ = run(prefix+['--version'], 'version', True)
    source = a.output/'minimal.cpp'; source.write_text('int bolt_liveness(int x) { return x + 1; }\n')
    obj = a.output/'minimal.o'
    cr, _ = run(prefix+['--driver-mode=g++','--target='+a.target,'-nostdinc','-x','c++','-O2','-c',source,'-o',obj], 'compile', True)
    object_ok = cr == 0 and obj.is_file() and obj.read_bytes()[:4] == b'\x7fELF'
    count_ok = a.expected_load_count is None or len(loads) == a.expected_load_count
    passed = bool(loads) and inside and vr == 0 and object_ok and count_ok
    result.update(version_exit=vr,compile_exit=cr,object_elf=object_ok,load_count_matches=count_ok,
                  status='PASS' if passed else 'FAIL')
    code = 0 if passed else 1
except (OSError, ValueError, AttributeError, IndexError) as e:
    result.update(status='ERROR',error=str(e));code=2
result['input_unchanged'] = sha(a.clang) == result['sha256']
if not result['input_unchanged']: result['status']='ERROR';code=2
result['commands'] = records
(a.output/'result.json').write_text(json.dumps(result,indent=2)+'\n')
for key in ('status','load_count','entry_in_executable_load','version_exit','compile_exit','input_unchanged'):
    print(key.upper()+'='+str(result.get(key,'UNKNOWN')))
sys.exit(code)
PY
