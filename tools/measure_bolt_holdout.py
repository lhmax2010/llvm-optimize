#!/usr/bin/env python3
"""Evaluate the frozen BOLT artifact on a locked holdout; never runs BOLT.

prepare -> verify -> calibrate -> measure -> summarize. Every benchmark round
interleaves RPM, stripped input, and BOLT, with RPM providing the common fixture.
Use --attempt to retain a failed calibration before a justified new attempt.
summarize-calibration emits explicitly unqualified diagnostics, never a formal result.
"""
import argparse
import json
import math
from pathlib import Path
import shlex
import subprocess
import sys
import time

import bench_toolchain as bench

W = bench.WORKSPACE
E = W/'temp/bolt-holdout-20260920'
D = W/'temp/bench_results/bolt-holdout-20260920'
TC = W/'temp/toolchain-baseline/usr'
INPUTS = bench.INPUTS/'holdout_tu'
OLD = W/'temp/bench_results/bolt-final-20260918/formal.json'
LOADER = Path('/lib64/ld-linux-x86-64.so.2')
RUNTIME = W/'temp/toolchain-runtime-baseline/libxml2/usr/lib64'
BINARIES = {
    'rpm-baseline': (TC/'bin/clang-22', '3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c'),
    'stripped-norelocs-bolt': (W/'temp/bolt-measurement-20260918/run/stripped/bin/clang-22', 'eccfb075bc3b2a6ca2bda5a2a6e68f6a29ba48b5586cb603f4b46080f656013e'),
    'bolted': (W/'temp/bolt-final-20260918/optimized/bin/clang-22', 'd6538b5ee1fdc429008b4481b651f994e354eabd55853666a0a9f0da03692e63'),
}


def read(path):
    return json.loads(path.read_text())


def require(path, status='PASS'):
    data = read(path)
    if data['status'] != status:
        raise RuntimeError(f'{path}: expected {status}, got {data["status"]}')
    return data


def protected():
    paths = [p for p,_ in BINARIES.values()]
    paths += [W/'temp/bolt-final-20260918/profile-work/merged.fdata',
              W/'llvm/packaging/llvm.spec', W/'gbs_llvm.conf', W/'tools/build_llvm_x86_64.py',
              W/'tools/llvm_baseline_capacity.json']
    # Existing training inputs must remain completely unchanged.
    paths += sorted(p for p in (bench.INPUTS/'real_tu').iterdir() if p.is_file())
    for sidecar in (bench.INPUTS/'real_tu').glob('*.flags.json'):
        data = read(sidecar)
        if 'input' in data: paths.append(Path(data['input']))
    for path, expected in BINARIES.values():
        if bench.digest(path) != expected: raise RuntimeError('artifact hash mismatch: '+str(path))
    return {str(p): bench.digest(p) for p in paths}


def host(path):
    with path.open('x') as log:
        log.write(time.strftime('%Y-%m-%dT%H:%M:%S%z')+'\n')
        for command in [['cat','/proc/meminfo'], ['free','-g'], ['nproc'],
                        ['cat','/proc/loadavg'], ['ps','-eo','pid,ppid,comm,rss,%cpu','--sort=-rss']]:
            log.write('$ '+shlex.join(command)+'\n'); log.flush()
            subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=True)


def common():
    old = read(OLD)['protocol']
    return ['--sysroot', old['sysroot'], '--resource-dir', old['resource_dir']]


def benchmark(prefix, calibrate=False):
    cmd = [sys.executable, str(W/'tools/bench_toolchain.py')]
    for label in BINARIES:
        cmd += ['--toolchain', label+'='+str(E/'toolchains'/label),
                '--loader', label+'='+str(LOADER), '--library-path', label+'='+str(RUNTIME)]
    cmd += common()+['--real-tu-dir', str(INPUTS), '--seed','20260920', '--scales','1','2','2',
                     '--runs','5','--cpus','2','--aslr','off','--load-threshold','10',
                     '--shards','64','--link-repeats','4096','--archive-repeats','1024',
                     '--work-dir','/dev/shm','--output',str(prefix)]
    if calibrate: cmd.append('--calibrate')
    return cmd


def summarize(directory, calibration_only=False):
    calibration = read(directory/'calibration.json') if calibration_only else require(directory/'calibration.json')
    runs = [read(directory/(name+'.json')) for name in ('calibration-run1','calibration-run2')]
    if not calibration_only:
        runs.append(require(directory/'formal.json', 'MEASURED'))
    if any(run['status'] not in ('MEASURED','MEASURED_WITH_WARNINGS') for run in runs):
        raise RuntimeError('cannot summarize an incomplete measurement')
    first = runs[0]
    for run in runs[1:]:
        for key in ('protocol_hash','fixture_hash','toolchains'):
            if run[key] != first[key]: raise RuntimeError('changed '+key)
    output = {'status':'UNCALIBRATED_DIAGNOSTIC' if calibration_only else 'PASS',
              'calibration_status':calibration['status'], 'formal_result':not calibration_only,
              'calibration_noise_pct':calibration['noise_floor_pct'], 'rounds':[]}
    for run in runs:
        rows = []
        for case in run['results']['rpm-baseline']:
            medians = {label: run['results'][label][case]['summary']['statistics']['wall_s']['median'] for label in BINARIES}
            r,s,b = [medians[k] for k in BINARIES]
            rows.append(dict(case=case, wall_medians=medians, bolt_over_stripped=b/s,
                             stripped_over_rpm=s/r, bolt_over_rpm=b/r))
        groups = {}
        for label, subset in [('compile',[r for r in rows if r['case'] not in ('ld.lld','llvm-ar')]),
                              ('real',[r for r in rows if r['case'].startswith('real_')]),
                              ('synthetic',[r for r in rows if r['case'] in 'ABC'])]:
            groups[label] = {key: math.exp(sum(math.log(r[key]) for r in subset)/len(subset))
                             for key in ('bolt_over_stripped','stripped_over_rpm','bolt_over_rpm')}
        output['rounds'].append(dict(start_time=run['start_time'], rows=rows, geometric_means=groups))
    stem = 'calibration-comparison' if calibration_only else 'comparison'
    bench.save(directory/(stem+'.json'), output)
    lines=[f"Status: {output['status']}; calibration: {calibration['status']}; formal: {output['formal_result']}", '',
           '| Case | RPM s | Stripped s | BOLT s | BOLT/stripped | Stripped/RPM | BOLT/RPM |',
           '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for r in output['rounds'][-1]['rows']:
        values=list(r['wall_medians'].values())+[r[k] for k in ('bolt_over_stripped','stripped_over_rpm','bolt_over_rpm')]
        lines.append('| '+r['case']+' | '+' | '.join(f'{v:.6f}' for v in values)+' |')
    for label, values in output['rounds'][-1]['geometric_means'].items():
        lines.append('| Geomean '+label+' | — | — | — | '+' | '.join(f'{v:.6f}' for v in values.values())+' |')
    (directory/(stem+'.md')).write_text('\n'.join(lines)+'\n')
    print(json.dumps(output['rounds'][-1]['geometric_means'],indent=2))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('phase',choices=['prepare','verify','calibrate','measure','summarize','summarize-calibration'])
    p.add_argument('--attempt',default='attempt1',help='new calibration directory, never overwrite a failed attempt')
    a=p.parse_args()
    if not a.attempt.replace('-','').isalnum(): p.error('invalid attempt name')
    E.mkdir(exist_ok=True); D.mkdir(parents=True,exist_ok=True)
    directory = D/a.attempt
    directory.mkdir(exist_ok=True)
    before = protected()
    if a.phase != 'prepare' and before != read(E/'protected-before.json'):
        raise RuntimeError('protected artifacts changed')
    if a.phase == 'prepare':
        if (E/'protected-before.json').exists(): raise RuntimeError('already prepared')
        require(E/'collection/collection.json')
        training = {read(p)['source'] for p in (bench.INPUTS/'real_tu').glob('*.flags.json')}
        holdout = {read(p)['source'] for p in INPUTS.glob('*.flags.json')}
        if len(holdout)!=10 or training & holdout: raise RuntimeError('invalid holdout')
        for label,(binary,_) in BINARIES.items():
            root=E/'toolchains'/label/'bin'; root.mkdir(parents=True,exist_ok=False)
            for alias in ('clang','clang++','clang-22'): (root/alias).symlink_to(binary)
            for alias in ('ld.lld','llvm-ar','llvm-ranlib'): (root/alias).symlink_to(TC/'bin'/alias)
        bench.save(E/'protected-before.json',before)
        host(E/'host-prepare.txt')
        return
    if a.phase in ('summarize', 'summarize-calibration'):
        summarize(directory, calibration_only=a.phase == 'summarize-calibration'); return
    logpath = directory/(a.phase+'-driver.log')
    host(directory/(a.phase+'-host-before.txt'))
    with logpath.open('x',buffering=1) as log:
        def run(cmd):
            cmd=list(map(str,cmd)); log.write('$ '+shlex.join(cmd)+'\n')
            subprocess.run(cmd,cwd=W,stdout=log,stderr=subprocess.STDOUT,check=True)
        if a.phase == 'verify':
            for label in ('stripped-norelocs-bolt','bolted'):
                run([sys.executable,W/'tools/verify_compiler_outputs.py',
                     '--baseline',BINARIES['rpm-baseline'][0],'--candidate',BINARIES[label][0],
                     '--loader',LOADER,'--library-path',RUNTIME,'--inputs',INPUTS,'--cpu','2',
                     '--output',E/('verify-'+label)]+common())
        elif a.phase == 'calibrate':
            for label in ('stripped-norelocs-bolt','bolted'): require(E/('verify-'+label)/'result.json')
            run(benchmark(directory/'calibration',True))
        else:
            require(directory/'calibration.json')
            run(benchmark(directory/'formal'))
    after = protected()
    bench.save(directory/(a.phase+'-protected-after.json'),after)
    if after != before: raise RuntimeError('protected artifact modified')


if __name__=='__main__':
    main()
