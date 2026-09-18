#!/usr/bin/env python3
"""Execute one auditable BOLT phase; existing outputs are never overwritten.

Order: inventory, strip, instrument, collect, optimize, verify, calibrate, measure.
Each phase verifies its prerequisites. BOLT/objcopy run under the shared 18 GiB
scope; compiler workloads retain the baseline harness's 4 GiB process limit.
No source/spec edits, software installation, perf, PGO or complete LLVM rebuild.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import sys

import bench_toolchain as bench


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('phase',choices=['inventory','strip','instrument','collect','optimize','verify','calibrate','measure'])
    p.add_argument('--bolt-bin',type=Path,required=True)
    p.add_argument('--relocs',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True,help='experiment evidence directory')
    p.add_argument('--bench-output',type=Path,required=True)
    p.add_argument('--sysroot',type=Path,required=True)
    p.add_argument('--baseline',type=Path,default=bench.WORKSPACE/'temp/toolchain-baseline/usr')
    p.add_argument('--baseline-result',type=Path,default=bench.WORKSPACE/'temp/bench_results/baseline-20260917-rpm/formal-baseline.json')
    p.add_argument('--runtime',type=Path,default=bench.WORKSPACE/'temp/toolchain-runtime-baseline/libxml2/usr/lib64')
    p.add_argument('--attempt',default='',help='unique retry log suffix; candidate output must still be absent')
    p.add_argument('--instrument-original',action='store_true',help='authorized fallback: instrument the retained unstripped relocs ELF')
    a=p.parse_args();w=bench.WORKSPACE
    for k in ['bolt_bin','relocs','output','bench_output','sysroot','baseline','baseline_result','runtime']:
        setattr(a,k,getattr(a,k).absolute())
    if not a.output.is_relative_to(w/'temp') or not a.bench_output.is_relative_to(w/'temp'):
        p.error('all evidence/results must be under workspace temp/')
    a.output.mkdir(parents=True,exist_ok=True);a.bench_output.mkdir(parents=True,exist_ok=True)
    if a.attempt and (not a.attempt.isalnum()):p.error('attempt must be alphanumeric')
    suffix='-'+a.attempt if a.attempt else ''
    phase_log=a.output/(a.phase+suffix+'-driver.log')
    if phase_log.exists():p.error('phase already attempted; preserve evidence and use an explicit new experiment')
    loader=Path('/lib64/ld-linux-x86-64.so.2')
    prefix=[str(loader),'--library-path',str(a.runtime)]
    resource=a.baseline/'lib64/clang/22'
    stripped=a.output/'stripped/bin/clang-22';instrumented=a.output/'instrumented/bin/clang-22'
    optimized=a.output/'optimized/bin/clang-22';profiles=a.output/'profiles'
    if a.instrument_original:
        if a.phase!='instrument' or not a.attempt:p.error('original fallback requires instrument phase and unique --attempt')
        instrumented=a.output/'instrumented-original/bin/clang-22';profiles=a.output/'profiles-original'
    bolt=a.bolt_bin/'llvm-bolt'
    def require(path,status='PASS'):
        data=json.loads(path.read_text())
        if data.get('status')!=status:raise RuntimeError('prerequisite not '+status+': '+str(path))
        return data
    with phase_log.open('w',buffering=1) as log:
        def run(cmd):
            cmd=list(map(str,cmd));log.write('$ '+shlex.join(cmd)+'\n');log.flush()
            subprocess.run(cmd,cwd=w,stdout=log,stderr=subprocess.STDOUT,check=True)
        def bounded(label,cmd):
            run([sys.executable,w/'tools/run_bolt_stage.py','--log-dir',a.output/(label+suffix),
                 '--cwd',w,'--']+cmd)
        def aliases(binary):
            for name in ['clang','clang++']:(binary.parent/name).symlink_to(binary.name)
        if a.phase=='inventory':
            rows=[]
            for name in ['llvm-bolt','perf2bolt','merge-fdata']:
                path=a.bolt_bin/name
                run(['ls','-la',path]);run(['readelf','-d',path]);run(prefix+[path,'--version'])
                rows.append(dict(name=name,path=str(path),bytes=path.stat().st_size,sha256=bench.digest(path)))
            bench.save(a.output/'bolt-tools.json',rows)
            run(prefix+[bolt,'--help'])
        elif a.phase=='strip':
            stripped.parent.mkdir(parents=True)
            bounded('strip',prefix+[a.baseline/'bin/llvm-objcopy','--strip-debug',a.relocs,stripped])
            bounded('strip-check',[sys.executable,w/'tools/check_bolt_elf.py','--before',a.relocs,'--after',stripped,
                 '--output',a.output/'strip-audit'])
        elif a.phase=='instrument':
            require(a.output/'strip-audit/result.json')
            if instrumented.exists() or list(profiles.glob('*')):raise RuntimeError('refuse to overwrite binary/profiles')
            instrumented.parent.mkdir(parents=True,exist_ok=True);profiles.mkdir(exist_ok=True)
            instrument_input=a.relocs if a.instrument_original else stripped
            bounded('instrument',prefix+[bolt,instrument_input,'-instrument','--thread-count=4',
                '-runtime-instrumentation-lib='+str(a.bolt_bin.parent/'lib64/libbolt_rt_instr.a'),
                '-instrumentation-file='+str(profiles/'clang'),'-instrumentation-file-append-pid',
                '-instrumentation-binpath='+str(instrumented),'-o',instrumented])
            aliases(instrumented)
            bench.save(a.output/'instrument-success.json',dict(status='PASS',input=str(instrument_input),compiler=str(instrumented),
                       profiles=str(profiles),outcome=str(a.output/('instrument'+suffix)/'outcome.json')))
        elif a.phase=='collect':
            success=require(a.output/'instrument-success.json')
            instrumented=Path(success['compiler']);profiles=Path(success['profiles'])
            outcome=json.loads(Path(success['outcome']).read_text())
            if outcome['command_exit_code']!=0 or outcome['problems']:raise RuntimeError('instrumentation did not succeed')
            bounded('profile-collection',[sys.executable,w/'tools/collect_bolt_profile.py',
                '--compiler',instrumented.parent/'clang++','--baseline',a.baseline/'bin/clang++',
                '--baseline-result',a.baseline_result,'--loader',loader,'--library-path',a.runtime,
                '--merge-fdata',a.bolt_bin/'merge-fdata','--sysroot',a.sysroot,
                '--resource-dir',resource,'--profile-dir',profiles,'--output',a.output/'profile-work','--cpu','2'])
        elif a.phase=='optimize':
            result=require(a.output/'profile-work/result.json');optimized.parent.mkdir(parents=True)
            instrument_input=Path(require(a.output/'instrument-success.json')['input'])
            bounded('optimize',prefix+[bolt,instrument_input,'-o',optimized,'-data='+result['merged_profile']['path'],
                '-reorder-blocks=ext-tsp','-reorder-functions=cdsort','-split-functions','-split-all-cold',
                '-split-eh','-dyno-stats','--thread-count=4'])
            aliases(optimized)
            for name in ['ld.lld','llvm-ar','llvm-ranlib']:(optimized.parent/name).symlink_to(a.baseline/'bin'/name)
        elif a.phase=='verify':
            run([sys.executable,w/'tools/verify_compiler_outputs.py','--baseline',a.baseline/'bin/clang-22',
                '--candidate',optimized,'--loader',loader,'--library-path',a.runtime,'--sysroot',a.sysroot,
                '--resource-dir',resource,'--cpu','2','--output',a.output/'optimized-equality'])
        elif a.phase in ['calibrate','measure']:
            verified=require(a.output/'optimized-equality/result.json')
            if len(verified['units'])!=10:raise RuntimeError('all 10 TUs required')
            if a.phase=='measure':require(a.bench_output/'calibration.json')
            cmd=[sys.executable,w/'tools/bench_toolchain.py',
                 '--toolchain','baseline='+str(a.baseline),'--toolchain','bolt='+str(optimized.parents[1]),
                 '--loader','baseline='+str(loader),'--loader','bolt='+str(loader),
                 '--library-path','baseline='+str(a.runtime),'--library-path','bolt='+str(a.runtime),
                 '--sysroot',a.sysroot,'--resource-dir',resource,'--cpus','2',
                 '--output',a.bench_output/('calibration' if a.phase=='calibrate' else 'formal')]
            if a.phase=='calibrate':cmd+=['--calibrate']
            run(cmd)
    print(a.phase.upper()+'_PASS',flush=True)
    return 0


if __name__=='__main__':raise SystemExit(main())
