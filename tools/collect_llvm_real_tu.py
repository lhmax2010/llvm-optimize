#!/usr/bin/env python3
"""Collect genuine target-preprocessed LLVM TUs without editing sources/configuration.

Candidates are the audited JSON list documented in docs/13. Their object names
are resolved again against the supplied build.ninja using ninja -t compdb.
All .ii files initially stay in a new temp directory. Nothing is published to
bench_inputs until every preprocessing command succeeds.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import signal
import subprocess as sp
import sys

import bench_toolchain as bench


def translate(row, root, toolchain, sysroot, output, resource=None, loader=None, target=bench.TARGET):
    original = shlex.split(row['command'])
    flags, semantic, changes = [], [], []
    index = 1
    while index < len(original):
        arg = original[index]
        if arg in ('-o', '-MF', '-MT', '-MQ'):
            changes.append(original[index:index+2]); index += 2; continue
        if arg in ('-c', '-MD', '-MMD', '-MP') or arg == row['file']:
            changes.append([arg]); index += 1; continue
        if arg in ('-m64', '-msse4.2', '-mfpmath=sse', '-march=nehalem') or arg.startswith('-flto'):
            changes.append([arg]); index += 1; continue
        if arg.startswith('-I/'):
            arg = '-I' + str(root / arg[3:])
        elif arg in ('-I', '-isystem', '-iquote'):
            value = original[index+1]
            flags += [arg, str(root/value.lstrip('/')) if value.startswith('/') else value]
            index += 2; continue
        elif arg.startswith('@'):
            raise RuntimeError('unexpanded response file: '+arg)
        flags.append(arg)
        if (arg.startswith(('-std=', '-O', '-g')) or arg == '-pthread'
                or (arg.startswith('-f') and not arg.startswith(('-fdiagnostics', '-fmessage')))):
            semantic.append(arg)
        index += 1
    source = root / row['file'].lstrip('/')
    resource = resource or toolchain/'lib64/clang/22'
    command = ([str(loader)] if loader else []) + [str(toolchain/'bin/clang++'), '--target='+target,
               '--sysroot='+str(sysroot), '-resource-dir='+str(resource)]
    command += flags + ['-E', str(source), '-o', str(output)]
    return command, semantic, changes


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--toolchain', type=Path, required=True, help='native toolchain directory containing bin/')
    p.add_argument('--resource-dir', type=Path, help='compiler-owned resource directory; default TOOLCHAIN/lib64/clang/22')
    p.add_argument('--loader', type=Path, help='explicit native ELF loader for a non-host PT_INTERP; no binary changes')
    p.add_argument('--build-root', type=Path, required=True, help='scratch.x86_64.N chroot with completed BUILD tree')
    p.add_argument('--sysroot', type=Path, required=True, help='existing target GBS root')
    p.add_argument('--target', choices=[bench.TARGET, bench.AARCH64_TARGET], default=bench.TARGET)
    p.add_argument('--candidates', type=Path, required=True, help='audited ten-entry TU candidate JSON')
    p.add_argument('--output-dir', type=Path, required=True, help='new evidence/large-input directory under workspace temp/')
    p.add_argument('--publish-dir', type=Path, default=bench.INPUTS/'real_tu')
    p.add_argument('--cpu', type=int, default=min(os.sched_getaffinity(0)), help='one allowed CPU for sequential preprocessing')
    p.add_argument('--dry-run', action='store_true', help='extract commands and emit plan; do not preprocess or publish')
    a = p.parse_args()
    for name in ('toolchain', 'build_root', 'sysroot', 'candidates', 'output_dir', 'publish_dir'):
        setattr(a,name,getattr(a,name).resolve())
    a.resource_dir = (a.resource_dir or a.toolchain/'lib64/clang/22').resolve()
    if a.loader:
        a.loader = a.loader.resolve(strict=True)
        bench.native_elf(a.loader)
    if not a.output_dir.is_relative_to(bench.WORKSPACE/'temp') or a.output_dir.exists():
        p.error('--output-dir must be a new directory inside workspace temp/')
    if a.cpu not in os.sched_getaffinity(0): p.error('CPU outside inherited affinity')
    a.output_dir.mkdir(parents=True)
    build = a.build_root/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build'
    log=(a.output_dir/'commands.log').open('w',buffering=1)
    result=dict(status='IN_PROGRESS', target=a.target, build_root=str(a.build_root),
                toolchain=str(a.toolchain), resource_dir=str(a.resource_dir),
                loader=str(a.loader) if a.loader else None, units=[])
    environment=dict(os.environ)
    for key in ('CPATH','CPLUS_INCLUDE_PATH','C_INCLUDE_PATH','LIBRARY_PATH',
                'GCC_EXEC_PREFIX','COMPILER_PATH','LD_PRELOAD','LD_LIBRARY_PATH'):
        environment.pop(key,None)
    environment.update(LC_ALL='C',LANG='C',TMPDIR=str(a.output_dir))
    def save():
        (a.output_dir/'collection.json').write_text(json.dumps(result,indent=2)+'\n')
    def run(command, *, capture=False):
        log.write('$ '+shlex.join(command)+'\n')
        process=sp.Popen(command,cwd=build,text=True,stdout=sp.PIPE if capture else log,
                         stderr=log,env=environment,start_new_session=True)
        try:
            stdout,_=process.communicate(timeout=180)
        except BaseException:
            os.killpg(process.pid,signal.SIGKILL)
            process.wait()
            raise
        log.write(f'[exit={process.returncode}]\n')
        if process.returncode: raise RuntimeError('command failed: '+shlex.join(command))
        return stdout
    try:
        bench.memory_guard()
        candidates=json.loads(a.candidates.read_text())
        if len(candidates)!=10: raise RuntimeError('expected exactly ten audited candidates')
        ninja=[str(a.build_root/'usr/lib64/ld-linux-x86-64.so.2'),'--library-path',
               str(a.build_root/'usr/lib64'),str(a.build_root/'usr/bin/ninja'),'-t','compdb-targets']
        raw_database=run(ninja+[row['object'] for row in candidates],capture=True)
        (a.output_dir/'compdb.json').write_text(raw_database)
        database=json.loads(raw_database)
        by_output={row.get('output'):row for row in database}
        for candidate in candidates:
            row=by_output[candidate['object']]
            name='llvm_'+candidate['group']+'_'+Path(row['file']).stem
            if not re.fullmatch(r'[A-Za-z0-9_-]+',name): raise RuntimeError('invalid input name')
            output=a.output_dir/(name+'.ii')
            command,flags,changes=translate(row,a.build_root,a.toolchain,a.sysroot,output,a.resource_dir,a.loader,a.target)
            result['units'].append(dict(name=name,source=row['file'],original_command=shlex.split(row['command']),
                preprocess_command=command, flags=flags, input=str(output),
                removed_for_target_elf_input=changes, historical_x86_compile_wall_s=candidate['build_wall_s']))
        save()
        if a.dry_run:
            result['status']='PLAN_ONLY';save();return 0
        bench.native_elf(a.toolchain/'bin/clang++')
        if not (a.resource_dir/'include/stddef.h').is_file():
            raise RuntimeError('missing compiler resource headers')
        query=([str(a.loader)] if a.loader else [])+[str(a.toolchain/'bin/clang++'),
               '--target='+a.target,'--sysroot='+str(a.sysroot),
               '-resource-dir='+str(a.resource_dir),'-dM','-E','-x','c++','/dev/null']
        macros=run(['taskset','-c',str(a.cpu),'prlimit',f'--as={bench.MEMORY_LIMIT}:{bench.MEMORY_LIMIT}','--']+query,capture=True)
        (a.output_dir/'target-predefined-macros.txt').write_text(macros)
        expected, forbidden = ('__arm__', '__aarch64__') if a.target == bench.TARGET else ('__aarch64__', '__arm__')
        if '#define '+expected+' 1' not in macros or '#define '+forbidden+' ' in macros or '#define __x86_64__' in macros:
            raise RuntimeError('preprocessor is not targeting '+a.target)
        for unit in result['units']:
            bench.memory_guard()
            command=['/usr/bin/time','-v','-o',str(a.output_dir/(unit['name']+'.time.txt')),
                     'nice','-n','15','ionice','-c3','taskset','-c',str(a.cpu),
                     'prlimit',f'--as={bench.MEMORY_LIMIT}:{bench.MEMORY_LIMIT}','--']+unit['preprocess_command']
            run(command)
            output=Path(unit['input'])
            unit.update(sha256=bench.digest(output),bytes=output.stat().st_size,status='PREPROCESSED',target=a.target)
            save();print(unit['name'],unit['bytes'],'bytes',flush=True)
        # Validate all proposed sidecars before publishing any input into the harness.
        proposed=a.output_dir/'sidecars';proposed.mkdir()
        for unit in result['units']:
            sidecar=dict(target=a.target,sha256=unit['sha256'],flags=unit['flags'],
                         source=unit['source']+' @ f111162e94aa48ed367c9d2c039456c70e7160ae',
                         original_command=unit['original_command'],preprocess_command=unit['preprocess_command'],
                         input=unit['input'])
            (proposed/(unit['name']+'.flags.json')).write_text(json.dumps(sidecar,indent=2)+'\n')
        bench.real_inputs(proposed,a.target)
        a.publish_dir.mkdir(parents=True,exist_ok=True)
        for unit in result['units']:
            destination=a.publish_dir/(unit['name']+'.flags.json')
            if destination.exists() or (a.publish_dir/(unit['name']+'.ii')).exists():
                raise RuntimeError('refusing to overwrite existing input: '+str(destination))
        for unit in result['units']:
            sidecar=json.loads((proposed/(unit['name']+'.flags.json')).read_text())
            if unit['bytes']<=10_000_000:
                shutil.copy2(unit['input'],a.publish_dir/(unit['name']+'.ii'))
                sidecar.pop('input')
            (a.publish_dir/(unit['name']+'.flags.json')).write_text(json.dumps(sidecar,indent=2)+'\n')
        result['status']='PASS';save();return 0
    except Exception as error:
        result.update(status='FAILED',error=str(error));save()
        log.write('STOPPED '+str(error)+'\n')
        print('STOPPED:',error,file=sys.stderr);return 2
    finally:
        log.close()


if __name__=='__main__':
    sys.exit(main())
