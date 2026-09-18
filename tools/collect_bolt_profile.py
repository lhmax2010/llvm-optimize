#!/usr/bin/env python3
"""Run the baseline's 13 compile workloads once with BOLT instrumentation.

Uses the unchanged historical generator, flags, real inputs, resource directory,
and ARM target. Each case also runs the baseline once to report instrumentation
overhead, not performance gains. The instrumented binary must already use a unique
--instrumentation-file prefix under --profile-dir and append PID to each file.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import time
from types import SimpleNamespace

import bench_toolchain as bench


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--compiler',type=Path,required=True,help='instrumented clang++ invocation')
    p.add_argument('--baseline',type=Path,required=True,help='baseline clang++ invocation')
    p.add_argument('--baseline-result',type=Path,required=True)
    p.add_argument('--loader',type=Path,required=True)
    p.add_argument('--library-path',type=Path,help='same independent runtime directory as the formal baseline')
    p.add_argument('--merge-fdata',type=Path,required=True)
    p.add_argument('--sysroot',type=Path,required=True)
    p.add_argument('--resource-dir',type=Path,required=True)
    p.add_argument('--profile-dir',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True,help='new temp/ evidence directory')
    p.add_argument('--cpu',type=int,default=2)
    a=p.parse_args()
    for k in ['compiler','baseline','baseline_result','loader','merge_fdata','sysroot','resource_dir','profile_dir','output']:
        setattr(a,k,getattr(a,k).absolute())
    if a.output.exists() or not a.output.is_relative_to(bench.WORKSPACE/'temp'):p.error('new temp/ output required')
    if a.cpu not in os.sched_getaffinity(0):p.error('CPU unavailable')
    baseline=json.loads(a.baseline_result.read_text());protocol=baseline['protocol']
    for k in ['sysroot','resource_dir']:
        if str(getattr(a,k))!=protocol[k]:p.error(k+' differs from baseline')
    if a.compiler.name!=a.baseline.name:p.error('both compilers must use identical invocation names')
    if list(a.profile_dir.glob('*')):p.error('profile directory must be empty before training')
    a.profile_dir.mkdir(parents=True,exist_ok=True);a.output.mkdir();raw=a.output/'raw';raw.mkdir()
    result=dict(status='RUNNING',baseline_protocol_hash=baseline['protocol_hash'],cases=[])
    args=SimpleNamespace(cpu_set=[a.cpu],load_threshold=protocol['load_threshold'],timeout=600,aslr=protocol['aslr'])
    runner=None;started=time.monotonic()
    try:
        with tempfile.TemporaryDirectory(prefix='bolt-profile-',dir='/dev/shm') as tmp:
            directory=Path(tmp);runner=bench.Runner(args,directory,raw)
            spec=importlib.util.spec_from_file_location('synthetic',bench.INPUTS/'generate_synthetic.py')
            generator=importlib.util.module_from_spec(spec);spec.loader.exec_module(generator)
            cases=[]
            for name,scale in zip('ABC',protocol['scales']):
                generated=directory/('generated-'+name);generator.generate(generated,scale)
                path=generated/(name+'.cpp')
                cases.append(dict(name=name,path=path,flags=['-std=c++17','-O2'],sha256=bench.digest(path)))
            cases+=bench.real_inputs(bench.INPUTS/'real_tu')
            prefix=[str(a.loader)]
            if a.library_path:prefix+=['--library-path',str(a.library_path.resolve())]
            expected={c['name']:(c['sha256'],c['flags']) for c in protocol['inputs']}
            actual={c['name']:(c['sha256'],c['flags']) for c in cases}
            if actual!=expected or len(cases)!=13:raise RuntimeError('training inputs/flags differ from formal baseline')
            result['inputs_equal_baseline']=True
            for case in cases:
                row=dict(name=case['name'],input_sha256=case['sha256'],flags=case['flags'])
                common=bench.compiler_flags(a,a.resource_dir)+case['flags']+(
                    ['-x','c++-cpp-output'] if case['name'].startswith('real_') else [])+[
                    '-c',str(case['path']),'-o',str(directory/'output.o')]
                previous=set(a.profile_dir.glob('*'))
                for label,compiler in [('baseline',a.baseline),('instrumented',a.compiler)]:
                    row[label]=runner.command(prefix+[str(compiler)]+common,tag=label+'-'+case['name'])
                    bench.verify_object(directory/'output.o');(directory/'output.o').unlink()
                created=set(a.profile_dir.glob('*'))-previous
                if not created or any(f.stat().st_size==0 for f in created):raise RuntimeError('missing/empty profile for '+case['name'])
                row['profiles']=[dict(path=str(f),bytes=f.stat().st_size,sha256=bench.digest(f)) for f in sorted(created)]
                row['instrumented_over_baseline_wall']=row['instrumented']['wall_s']/row['baseline']['wall_s']
                result['cases'].append(row);bench.save(a.output/'result.json',result)
                print(case['name'],'PROFILE_CREATED',len(created),flush=True)
            profiles=sorted(a.profile_dir.glob('*'));merged=a.output/'merged.fdata'
            result['merge']=runner.command(prefix+[str(a.merge_fdata),'-o',str(merged)]+list(map(str,profiles)),tag='merge-fdata')
            result['merged_profile']=dict(path=str(merged),bytes=merged.stat().st_size,sha256=bench.digest(merged))
            if not merged.stat().st_size:raise RuntimeError('empty merged profile')
        result.update(status='PASS',scratch_removed=not directory.exists(),
                      instrumented_compile_wall_s=sum(c['instrumented']['wall_s'] for c in result['cases']))
        return 0
    except Exception as error:
        result.update(status='FAILED',error=str(error));print('FAILED',error,flush=True);return 2
    finally:
        result['total_wall_s']=time.monotonic()-started;bench.save(a.output/'result.json',result)
        if runner:bench.save(raw/'commands.json',runner.commands)


if __name__=='__main__':raise SystemExit(main())
