#!/usr/bin/env python3
"""One v2 rewrite, 30-TU byte gate, then interleaved two-target comparison.

No instrumentation, relinking, source edits or rebuilding. Rewrite has a 6 GiB
zero-swap cgroup; compilers retain the harness's 4 GiB limit. Each phase is tried
once per evidence directory. Failed calibration never launches a formal run.
"""
import argparse
import json
from pathlib import Path
import shlex
import subprocess as sp
import sys

import bench_toolchain as bench


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('phase',choices=['rewrite','verify','calibrate','measure'])
    for key in ('experiment','results','baseline','bolt-v1','stripped','bolt-bin','sysroot','aarch64-sysroot','runtime'):
        p.add_argument('--'+key,type=Path,required=True)
    a=p.parse_args();w=bench.WORKSPACE
    for key,value in vars(a).items():
        if isinstance(value,Path):setattr(a,key,value.absolute())
    if not all(x.is_relative_to(w/'temp') for x in [a.experiment,a.results]):p.error('evidence must stay under temp/')
    a.results.mkdir(parents=True,exist_ok=True)
    if not a.experiment.is_dir():p.error('existing profile collection experiment required')
    logpath=a.experiment/(a.phase+'-driver.log')
    if logpath.exists():p.error('phase already attempted; preserve it, do not silently retry')
    loader=Path('/lib64/ld-linux-x86-64.so.2');prefix=[loader,'--library-path',a.runtime]
    candidate=a.experiment/'optimized-v2/bin/clang-22';resource=a.baseline/'lib64/clang/22'
    def require(path):
        data=json.loads(path.read_text())
        if data.get('status')!='PASS':raise RuntimeError('prerequisite not PASS: '+str(path))
        return data
    with logpath.open('x',buffering=1) as log:
        def run(cmd):
            cmd=list(map(str,cmd));log.write('$ '+shlex.join(cmd)+'\n')
            sp.run(cmd,cwd=w,stdout=log,stderr=sp.STDOUT,check=True)
        try:
            if a.phase=='rewrite':
                profile=require(a.experiment/'profile-work/result.json')
                if len(profile['new_profiles'])!=10 or len(profile['original_profiles'])!=13:
                    raise RuntimeError('23 training profiles required')
                merged=Path(profile['merged_profile']['path'])
                if bench.digest(merged)!=profile['merged_profile']['sha256']:raise RuntimeError('profile identity changed')
                if bench.digest(a.stripped)!='eccfb075bc3b2a6ca2bda5a2a6e68f6a29ba48b5586cb603f4b46080f656013e':
                    raise RuntimeError('wrong stripped input')
                candidate.parent.mkdir(parents=True)
                command=prefix+[a.bolt_bin/'llvm-bolt',a.stripped,'-o',candidate,'-data='+str(merged),
                    '-reorder-blocks=ext-tsp','-reorder-functions=cdsort','-split-functions','-split-all-cold',
                    '-split-eh','-dyno-stats','--thread-count=1','-stale-threshold=5']
                run([sys.executable,w/'tools/run_bolt_stage.py','--memory-max-gib','6',
                    '--log-dir',a.experiment/'rewrite-scope','--cwd',w,'--']+command)
                outcome=json.loads((a.experiment/'rewrite-scope/outcome.json').read_text())
                if outcome['command_exit_code']!=0 or outcome['problems']:raise RuntimeError('rewrite failed')
                for alias in ('clang','clang++'):(candidate.parent/alias).symlink_to(candidate.name)
                for tool in ('ld.lld','llvm-ar','llvm-ranlib'):(candidate.parent/tool).symlink_to(a.baseline/'bin'/tool)
                bench.save(a.experiment/'profile-v2-manifest.json',dict(profile_schema=2,profile_version='v2',
                    status='REWRITTEN_NOT_YET_CERTIFIED',stripped_sha256=bench.digest(a.stripped),
                    instrumented_sha256=profile['instrumented_sha256'],profile=profile['merged_profile'],
                    candidate_sha256=bench.digest(candidate),candidate_bytes=candidate.stat().st_size,
                    source_profile_v1=profile['original_profiles'],rewrite_command=list(map(str,command)),
                    corpora=[dict(target=bench.TARGET,count=13,seed=73419,scales=[1,2,2],
                                 real_inputs=[{k:str(v) if isinstance(v,Path) else v for k,v in u.items()} for u in bench.real_inputs(bench.INPUTS/'real_tu')]),
                             dict(target=bench.AARCH64_TARGET,count=10,sysroot=str(a.aarch64_sysroot),
                                 real_inputs=[{k:str(v) if isinstance(v,Path) else v for k,v in u.items()} for u in bench.real_inputs(bench.INPUTS/'real_tu_aarch64',bench.AARCH64_TARGET)])]))
            elif a.phase=='verify':
                sets=[('arm-training',bench.TARGET,a.sysroot,'real_tu'),
                      ('arm-holdout',bench.TARGET,a.sysroot,'holdout_tu'),
                      ('aarch64',bench.AARCH64_TARGET,a.aarch64_sysroot,'real_tu_aarch64')]
                rows=[]
                for name,target,sysroot,inputs in sets:
                    output=a.experiment/('equality-'+name)
                    run([sys.executable,w/'tools/verify_compiler_outputs.py','--baseline',a.baseline/'bin/clang-22',
                         '--candidate',candidate,'--loader',loader,'--library-path',a.runtime,'--sysroot',sysroot,
                         '--resource-dir',resource,'--target',target,'--inputs',bench.INPUTS/inputs,
                         '--cpu','2','--output',output])
                    result=require(output/'result.json')
                    if len(result['units'])!=10:raise RuntimeError('expected ten TUs per corpus')
                    rows.append(dict(corpus=name,target=target,result=str(output/'result.json'),count=10))
                bench.save(a.experiment/'correctness-30.json',dict(status='PASS',corpora=rows,count=30,
                    baseline_sha256=bench.digest(a.baseline/'bin/clang-22'),candidate_sha256=bench.digest(candidate)))
            else:
                checked=require(a.experiment/'correctness-30.json')
                if checked['candidate_sha256']!=bench.digest(candidate):raise RuntimeError('candidate changed after byte gate')
                if checked['baseline_sha256']!=bench.digest(a.baseline/'bin/clang-22'):
                    raise RuntimeError('baseline changed after byte gate')
                if a.phase=='measure':require(a.results/'calibration.json')
                out=a.results/('calibration' if a.phase=='calibrate' else 'formal')
                cmd=[sys.executable,w/'tools/bench_toolchain.py']
                for name,root in [('rpm-baseline',a.baseline),('bolt-v1',a.bolt_v1),('bolt-v2',candidate.parents[1])]:
                    cmd+=['--toolchain',name+'='+str(root),'--loader',name+'='+str(loader),
                          '--library-path',name+'='+str(a.runtime)]
                cmd+=['--sysroot',a.sysroot,'--aarch64-sysroot',a.aarch64_sysroot,
                      '--aarch64-real-tu-dir',bench.INPUTS/'real_tu_aarch64','--real-tu-dir',bench.INPUTS/'real_tu',
                      '--resource-dir',resource,'--cpus','2','--runs','5','--seed','73419','--scales','1','2','2',
                      '--aslr','off','--load-threshold','10','--shards','64','--link-repeats','4096',
                      '--archive-repeats','1024','--work-dir','/dev/shm','--output',out]
                if a.phase=='calibrate':cmd+=['--calibrate']
                with (a.results/(a.phase+'-host-before.txt')).open('w') as host:
                    for c in [['date','-Is'],['free','-b'],['cat','/proc/meminfo'],['ps','-eo','pid,comm,rss','--sort=-rss']]:
                        host.write('$ '+shlex.join(c)+'\n');host.flush();sp.run(c,stdout=host,check=True)
                bench.save(a.results/(a.phase+'-launch.json'),list(map(str,cmd)))
                run(['nice','-n','15','ionice','-c3']+cmd)
                if a.phase=='measure':
                    reference=json.loads((a.results/'calibration-run1.json').read_text())
                    measured=json.loads(out.with_suffix('.json').read_text())
                    for key in ('protocol_hash','fixture_hash','toolchains'):
                        if measured[key]!=reference[key]:
                            raise RuntimeError('formal run no longer matches calibration: '+key)
            print(a.phase.upper()+'_PASS',flush=True);return 0
        except Exception as error:
            log.write('STOPPED '+str(error)+'\n');print('STOPPED',error,flush=True);return 2


if __name__=='__main__':raise SystemExit(main())
