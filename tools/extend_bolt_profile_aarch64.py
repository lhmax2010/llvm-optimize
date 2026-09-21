#!/usr/bin/env python3
"""Train ten AArch64 inputs with an EXISTING instrumented clang and merge v2.

Never instruments or rewrites a binary. Retains the original 13 fdata files and
records their hashes before/after. The existing instrumented ELF embeds its
profile prefix, supplied here for auditing; PID-suffixed new files remain there.
Each compiler process has the harness's 4 GiB AS limit, one CPU and ASLR off.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import tempfile
import time
from types import SimpleNamespace

import bench_toolchain as bench


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for arg in ('compiler', 'baseline', 'loader', 'library-path', 'sysroot', 'resource-dir',
                'inputs', 'profile-dir', 'merge-fdata', 'output'):
        p.add_argument('--'+arg, type=Path, required=True)
    p.add_argument('--cpu', type=int, default=2)
    a = p.parse_args()
    for key,value in vars(a).items():
        if isinstance(value,Path):setattr(a,key,value.absolute())
    a.output = a.output.resolve()
    if not a.output.is_relative_to(bench.WORKSPACE/'temp') or a.output.exists():
        p.error('new output directory under workspace temp/ required')
    if a.cpu not in os.sched_getaffinity(0): p.error('CPU outside affinity')
    units = bench.real_inputs(a.inputs, bench.AARCH64_TARGET)
    if len(units) != 10: p.error('exactly ten AArch64 inputs required')
    # Absolute compiler paths, same invocation basename and explicit g++ mode.
    for key in ('compiler','baseline','loader','merge_fdata'):
        path=getattr(a,key).absolute(); setattr(a,key,path); bench.native_elf(path)
    if a.compiler.name != a.baseline.name: p.error('driver basenames must match')
    old = sorted(a.profile_dir.glob('clang.*.fdata'))
    if len(old) != 13: p.error('expected exactly 13 original profiles; refuse retry/ambiguous inventory')
    old_hashes={str(f.absolute()):bench.digest(f) for f in old}
    a.output.mkdir(parents=True); raw=a.output/'raw';raw.mkdir()
    result=dict(status='RUNNING',profile_version=2,target=bench.AARCH64_TARGET,
                instrumented_sha256=bench.digest(a.compiler),baseline_sha256=bench.digest(a.baseline),
                original_profiles=old_hashes,units=[],new_profiles=[])
    def save(): bench.save(a.output/'result.json',result)
    start=time.monotonic();runner=None
    try:
        args=SimpleNamespace(cpu_set=[a.cpu],load_threshold=len(os.sched_getaffinity(0))/2,
                             timeout=300,aslr='off')
        with tempfile.TemporaryDirectory(prefix='bolt-profile-v2-',dir='/dev/shm') as scratch:
            cwd=Path(scratch);runner=bench.Runner(args,cwd,raw)
            prefix=[str(a.loader),'--library-path',str(a.library_path.absolute())]
            for unit in units:
                before=set(a.profile_dir.glob('clang.*.fdata'))
                common=['--driver-mode=g++']+bench.compiler_flags(a,a.resource_dir,bench.AARCH64_TARGET)+unit['flags']+[
                    '-x','c++-cpp-output','-c',str(unit['path']),'-o',str(cwd/'output.o')]
                row=dict(name=unit['name'],input_sha256=unit['sha256'],flags=unit['flags'],measurements={})
                result['units'].append(row)
                for label,compiler in [('baseline',a.baseline),('instrumented',a.compiler)]:
                    rec=runner.command(prefix+[str(compiler)]+common,tag=label+'-'+unit['name'])
                    bench.verify_object(cwd/'output.o',bench.AARCH64_TARGET)
                    row['measurements'][label]=rec
                    (cwd/'output.o').unlink()
                created=set(a.profile_dir.glob('clang.*.fdata'))-before
                if len(created)!=1: raise RuntimeError('expected one PID profile per TU: '+repr(created))
                profile=created.pop()
                if not profile.stat().st_size: raise RuntimeError('empty profile')
                row['profile']=dict(path=str(profile.absolute()),sha256=bench.digest(profile),bytes=profile.stat().st_size)
                result['new_profiles'].append(row['profile'])
                row['instrumentation_wall_ratio']=row['measurements']['instrumented']['wall_s']/row['measurements']['baseline']['wall_s']
                save();print(unit['name'],'PROFILE_PASS',flush=True)
            result['collection_wall_s']=time.monotonic()-start
            if {str(f.absolute()):bench.digest(f) for f in old} != old_hashes:
                raise RuntimeError('original profiles changed')
            profiles=old+[Path(x['path']) for x in result['new_profiles']]
            if set(a.profile_dir.glob('clang.*.fdata'))!=set(profiles):
                raise RuntimeError('unexpected concurrent profile writer')
            merged=runner.command(prefix+[str(a.merge_fdata)]+list(map(str,profiles)),tag='merge-23-profiles')
            output=a.output/'merged-v2.fdata';shutil.copyfile(merged['stdout'],output)
            if not output.stat().st_size: raise RuntimeError('empty merged profile')
            result['merged_profile']=dict(path=str(output),sha256=bench.digest(output),bytes=output.stat().st_size,
                                          armv7l_profiles=13,aarch64_profiles=10,measurement=merged)
        result.update(status='PASS',original_profiles_unchanged=True,scratch_removed=not cwd.exists())
        return 0
    except Exception as error:
        result.update(status='FAILED',error=str(error));print('STOPPED',error,flush=True);return 2
    finally:
        result['wall_s']=time.monotonic()-start;save()
        if runner:bench.save(raw/'commands.json',runner.commands)


if __name__=='__main__':raise SystemExit(main())
