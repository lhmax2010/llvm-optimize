#!/usr/bin/env python3
"""Continue the successful final BOLT attempt, one prerequisite-checked phase.

collect -> optimize -> verify -> calibrate -> measure. Never reinstruments.
Only the fixed BOLT optimization command uses 22 GiB and one worker. Compiler
workloads retain the unchanged benchmark limits, inputs and baseline fixture.
All outputs use new paths under temp/; no baseline artifact is overwritten.
"""
import argparse
import json
from pathlib import Path
import shlex
import signal
import subprocess
import sys
import threading
import time
from types import SimpleNamespace

import bench_toolchain as bench
import bolt_final_attempt as final
import build_llvm_x86_64 as guard

W = guard.WORKSPACE
E = W/'temp/bolt-final-20260918'
D = W/'temp/bench_results/bolt-final-20260918'
TC = W/'temp/toolchain-baseline/usr'
REFERENCE = W/'temp/bench_results/baseline-20260917-rpm/formal-baseline.json'


def require(path):
    result = json.loads(path.read_text())
    if result.get('status') != 'PASS':
        raise RuntimeError('prerequisite not PASS: '+str(path))
    return result


def rewrite_plan():
    return dict(memory_max_gib=final.FINAL_BOLT_MEMORY_GIB,
                memory_swap_max_bytes=0, operation='FINAL_BOLT_OPTIMIZATION_ONLY', bolt_workers=1)


def rewrite(command):
    """Fixed BOLT-only path; never used by a GBS or Ninja entry point."""
    directory = E/'optimize'
    audit = guard.Audit(directory)
    stop = threading.Event()
    observer = None
    try:
        audit.run(['free', '-g'])
        audit.run(['cat', '/proc/meminfo'])
        completion, release = directory/'command.exit', directory/'release'
        trap = ('status=$?; printf "%s\\n" "$status" > '+shlex.quote(str(completion))+
                '; while [ ! -e '+shlex.quote(str(release))+' ]; do sleep .2; done; exit "$status"')
        body = shlex.join(['/usr/bin/time','-v','-o',str(directory/'tool-time-v.txt')]+command)+'\n'
        script = directory/'stage.sh'
        script.write_text('set -eu\ntrap '+shlex.quote(trap)+' EXIT\ncd '+shlex.quote(str(W))+'\n'+body)
        audit.json('stage.json', dict(command=command, cwd=str(W), completion=str(completion), release=str(release)))

        def sample():
            with (directory/'host-memory-2s.jsonl').open('w', buffering=1) as stream:
                start = time.monotonic()
                while True:
                    stream.write(json.dumps(dict(timestamp=guard.stamp(),elapsed=time.monotonic()-start,
                                                 available_bytes=guard.mem_available()))+'\n')
                    if stop.wait(2): break

        observer = threading.Thread(target=sample, name='bolt-host-memory', daemon=False)
        observer.start()
        guard.build(audit, SimpleNamespace(buildroot=directory), rewrite_plan(), None, 'systemd',
                    command=['/bin/bash',str(script)], completion_file=completion, release_file=release,
                    cache_check=False)
        audit.json('success.json', dict(status='PASS'))
    finally:
        stop.set()
        if observer is not None:
            observer.join()
            final.detailed_summary(directory)
        audit.stream.close()


def aliases(binary):
    for name in ['clang', 'clang++']:
        alias = binary.parent/name
        if alias.is_symlink() and alias.readlink() == Path(binary.name): continue
        alias.symlink_to(binary.name)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('phase',choices=['collect','optimize','verify','calibrate','measure'])
    a = p.parse_args()
    success = require(final.EVIDENCE/'success.json')
    outcome = json.loads(Path(success['outcome']).read_text())
    if outcome['exit_code'] or outcome['problems']: raise RuntimeError('instrumentation failed')
    instrumented = Path(success['compiler'])
    optimized = E/'optimized/bin/clang-22'
    baseline = json.loads(REFERENCE.read_text())
    sysroot, resource = [baseline['protocol'][k] for k in ['sysroot','resource_dir']]
    _, original = final.load_command()
    prefix, bolt = original[:3], Path(original[3])
    loader, runtime = prefix[0], prefix[2]
    log_path = E/(a.phase+'-driver.log')
    if log_path.exists(): raise RuntimeError('phase already attempted; do not overwrite evidence')
    with log_path.open('x', buffering=1) as log:
        def run(cmd):
            cmd = list(map(str,cmd));log.write('$ '+shlex.join(cmd)+'\n')
            subprocess.run(cmd,cwd=W,stdout=log,stderr=subprocess.STDOUT,check=True)
        if a.phase == 'collect':
            aliases(instrumented)
            run([sys.executable,W/'tools/run_bolt_stage.py','--log-dir',E/'profile-collection','--cwd',W,'--',
                 sys.executable,W/'tools/collect_bolt_profile.py','--compiler',instrumented.parent/'clang++',
                 '--baseline',TC/'bin/clang++','--baseline-result',REFERENCE,'--loader',loader,
                 '--library-path',runtime,'--merge-fdata',bolt.parent/'merge-fdata',
                 '--sysroot',sysroot,'--resource-dir',resource,'--profile-dir',success['profiles'],
                 '--output',E/'profile-work','--cpu','2'])
        elif a.phase == 'optimize':
            profile = require(E/'profile-work/result.json')['merged_profile']['path']
            optimized.parent.mkdir(parents=True,exist_ok=False)
            command = prefix+[str(bolt),success['input'],'-o',str(optimized),'-data='+profile,
                              '-reorder-blocks=ext-tsp','-reorder-functions=cdsort','-split-functions',
                              '-split-all-cold','-split-eh','-dyno-stats','--thread-count=1']
            log.write('$ '+shlex.join(command)+'\n')
            rewrite(command)
            aliases(optimized)
            for name in ['ld.lld','llvm-ar','llvm-ranlib']:
                (optimized.parent/name).symlink_to(TC/'bin'/name)
        elif a.phase == 'verify':
            require(E/'optimize/success.json')
            run([sys.executable,W/'tools/verify_compiler_outputs.py','--baseline',TC/'bin/clang-22',
                 '--candidate',optimized,'--loader',loader,'--library-path',runtime,'--sysroot',sysroot,
                 '--resource-dir',resource,'--cpu','2','--output',E/'optimized-equality'])
        else:
            verified = require(E/'optimized-equality/result.json')
            if len(verified['units']) != 10 or not all(x['byte_equal'] for x in verified['units']):
                raise RuntimeError('all 10 byte comparisons must PASS')
            if a.phase == 'measure': require(D/'calibration.json')
            D.mkdir(exist_ok=True,parents=True)
            cmd = [sys.executable,W/'tools/bench_toolchain.py','--toolchain','baseline='+str(TC),
                   '--toolchain','bolt='+str(optimized.parents[1]),'--loader','baseline='+loader,
                   '--loader','bolt='+loader,'--library-path','baseline='+runtime,'--library-path','bolt='+runtime,
                   '--sysroot',sysroot,'--resource-dir',resource,'--cpus','2',
                   '--output',D/('calibration' if a.phase == 'calibrate' else 'formal')]
            if a.phase == 'calibrate': cmd += ['--calibrate']
            run(cmd)
    print(a.phase.upper()+'_PASS',flush=True)


if __name__ == '__main__':
    def interrupted(signum,frame): raise KeyboardInterrupt(f'signal {signum}')
    for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP,signal.SIGQUIT):signal.signal(sig,interrupted)
    main()
