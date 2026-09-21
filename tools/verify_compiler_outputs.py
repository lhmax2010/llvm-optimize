#!/usr/bin/env python3
"""Byte-compare target object output from two native compilers; stop at first mismatch.

Uses the benchmark's real TU sidecars, target, flags, and 4 GiB process limit.
Both compilations use the same cwd and output pathname to avoid debug-path drift.
Both explicitly select --driver-mode=g++; use clang-22 as both invocation names.
Default: every real TU. --case selects a named input for the relink prerequisite.
"""
import argparse
import json
from pathlib import Path
import shutil
import tempfile
from types import SimpleNamespace
import os

import bench_toolchain as bench


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--baseline', type=Path, required=True, help='baseline clang-22 ELF or symlink')
    p.add_argument('--candidate', type=Path, required=True, help='relocated/BOLT clang-22 ELF or symlink')
    p.add_argument('--loader', type=Path, required=True, help='same native ELF loader for both')
    p.add_argument('--library-path', type=Path, help='same optional independent runtime directory')
    p.add_argument('--sysroot', type=Path, required=True)
    p.add_argument('--resource-dir', type=Path, required=True)
    p.add_argument('--target', choices=[bench.TARGET, bench.AARCH64_TARGET], default=bench.TARGET)
    p.add_argument('--inputs', type=Path, default=bench.INPUTS/'real_tu')
    p.add_argument('--case', action='append', help='exact real_NAME; repeat, default all real inputs')
    p.add_argument('--cpu', type=int, default=min(os.sched_getaffinity(0)))
    p.add_argument('--output', type=Path, required=True, help='new evidence directory under workspace temp/')
    a = p.parse_args()
    for key in ('baseline','candidate','loader','sysroot','resource_dir','inputs'):
        setattr(a,key,getattr(a,key).absolute())
    a.output = a.output.resolve()
    if not a.output.is_relative_to(bench.WORKSPACE/'temp') or a.output.exists():
        p.error('--output must be a new directory under workspace temp/')
    if a.cpu not in os.sched_getaffinity(0): p.error('CPU outside inherited affinity')
    units = bench.real_inputs(a.inputs,a.target)
    if a.case:
        if set(a.case)-{u['name'] for u in units}: p.error('unknown real TU case')
        units = [u for u in units if u['name'] in a.case]
    if not units: p.error('no real translation units')
    for path in (a.baseline,a.candidate,a.loader): bench.native_elf(path)
    a.output.mkdir(parents=True)
    raw = a.output/'raw'; raw.mkdir()
    result = dict(status='RUNNING',target=a.target,baseline=str(a.baseline),candidate=str(a.candidate),
                  driver_mode='g++',
                  baseline_sha256=bench.digest(a.baseline),candidate_sha256=bench.digest(a.candidate),
                  sysroot=str(a.sysroot),resource_dir=str(a.resource_dir),units=[])
    def save(): bench.save(a.output/'result.json',result)
    args = SimpleNamespace(cpu_set=[a.cpu],load_threshold=len(os.sched_getaffinity(0))/2,
                           timeout=180,aslr='off')
    scratch_parent = Path('/dev/shm')
    if shutil.disk_usage(scratch_parent).free < bench.MEMORY_LIMIT:
        p.error('tmpfs requires 4 GiB free')
    runner = None
    try:
        with tempfile.TemporaryDirectory(prefix='clang-equality-',dir=scratch_parent) as scratch:
            cwd = Path(scratch)
            runner = bench.Runner(args,cwd,raw)
            prefix = [str(a.loader)]
            if a.library_path: prefix += ['--library-path',str(a.library_path.resolve())]
            for unit in units:
                files = []
                common = ['--driver-mode=g++']+bench.compiler_flags(a,a.resource_dir,a.target)+unit['flags']+[
                    '-x','c++-cpp-output','-c',str(unit['path']),'-o',str(cwd/'output.o')]
                row = dict(name=unit['name'],input_sha256=unit['sha256'],outputs=[])
                result['units'].append(row)
                for label,compiler in [('baseline',a.baseline),('candidate',a.candidate)]:
                    record = runner.command(prefix+[str(compiler)]+common,tag=unit['name']+'-'+label)
                    bench.verify_object(cwd/'output.o',a.target)
                    retained = a.output/(unit['name']+'.'+label+'.o')
                    shutil.copyfile(cwd/'output.o',retained)
                    files.append(retained)
                    row['outputs'].append(dict(label=label,path=str(retained),bytes=retained.stat().st_size,
                                               sha256=bench.digest(retained),measurement=record))
                # A byte comparison, not a disassembly/section or hash-only comparison.
                try:
                    runner.command(['cmp','--']+list(map(str,files)),tag=unit['name']+'-cmp')
                except bench.BenchError:
                    row['byte_equal']=False;result['status']='BLOCKER';save()
                    raise
                row['byte_equal']=True;save()
                print(unit['name'],'BYTE_IDENTICAL',flush=True)
        result.update(status='PASS',scratch_removed=not cwd.exists());save()
        return 0
    except Exception as error:
        result.update(status='BLOCKER' if result['status']=='BLOCKER' else 'FAILED',error=str(error))
        save();print(result['status'],error,flush=True);return 2
    finally:
        if runner: bench.save(raw/'commands.json',runner.commands)


if __name__ == '__main__':
    raise SystemExit(main())
