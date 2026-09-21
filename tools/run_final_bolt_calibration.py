#!/usr/bin/env python3
"""One preregistered, split-target calibration attempt; never build or rewrite.

Default prints the frozen commands without executing any compiler. After the
user confirms the quiet window, supply --run --quiet-window-confirmed and the
published --preregistered-commit. The evidence directory cannot be reused.
"""
import argparse
import datetime
import json
import math
import os
from pathlib import Path
import re
import signal
import subprocess as sp
import sys
import threading
import time

import bench_toolchain as bench

PLAN = Path(__file__).with_name('final_bolt_calibration_plan.json')


def timestamp():
    return datetime.datetime.now().astimezone().isoformat()


def commands(plan, target, formal=False):
    command = list(plan['command_template'])
    command.remove('--calibrate')
    command[command.index('--output') + 1] = str(
        Path(plan['output']) / target / ('formal' if formal else 'calibration'))
    command += ['--compile-target', target]
    if not formal:
        command.append('--calibrate')
    return ['nice', '-n', '15', 'ionice', '-c3'] + command


def load_sample():
    raw = Path('/proc/loadavg').read_text().strip()
    return dict(timestamp=timestamp(), monotonic_s=time.monotonic(),
                loadavg_raw=raw, load1=float(raw.split()[0]))


def require_quiet(sample):
    if not math.isfinite(sample['load1']) or sample['load1'] > 3:
        raise RuntimeError('REFUSED_LOAD: one-minute loadavg > 3; no waiting or retry')


def load_summary(samples):
    periods = []
    for index, sample in enumerate(samples):
        if sample['load1'] <= 10:
            continue
        if index == 0 or samples[index - 1]['load1'] <= 10:
            periods.append(dict(first_observed=sample['timestamp'], last_observed=sample['timestamp'],
                                prior_observation=samples[index-1]['timestamp'] if index else None,
                                next_observation=None))
        periods[-1]['last_observed'] = sample['timestamp']
        if index+1 < len(samples) and samples[index+1]['load1'] <= 10:
            periods[-1]['next_observation'] = samples[index+1]['timestamp']
    return dict(max_load1=max(s['load1'] for s in samples), interval_s=30,
                above_10_samples=[s for s in samples if s['load1'] > 10],
                above_10_observed_periods=periods,
                interpretation='30s observations, not continuous peaks; timestamps identify observed high-load periods')


class LoadMonitor:
    def __init__(self, directory):
        self.path = directory / 'loadavg.jsonl'
        self.samples = []
        self.error = None
        self.stop = threading.Event()
        self.thread = threading.Thread(target=self.loop, name='final-bolt-loadavg')

    def sample(self):
        row = load_sample()
        with self.path.open('a') as stream:
            stream.write(json.dumps(row) + '\n')
        self.samples.append(row)

    def loop(self):
        try:
            while not self.stop.wait(30):
                self.sample()
        except Exception as error:
            self.error = error

    def __enter__(self):
        self.sample()
        self.thread.start()
        return self

    def __exit__(self, *_):
        self.stop.set()
        self.thread.join()
        self.sample()
        summary = load_summary(self.samples)
        summary.update(sampler_reaped=not self.thread.is_alive(), error=str(self.error) if self.error else None)
        bench.save(self.path.with_name('loadavg-summary.json'), summary)


def execute(command, directory, monitor):
    bench.save(directory.with_suffix('.command.json'), command)
    child = None
    with directory.with_suffix('.log').open('x') as log:
        try:
            child = sp.Popen(command, cwd=bench.WORKSPACE, stdout=log, stderr=sp.STDOUT,
                             start_new_session=True)
            while child.poll() is None:
                if monitor.error:
                    raise RuntimeError('Load sampler failed: ' + str(monitor.error))
                time.sleep(.25)
            return child.returncode
        finally:
            if child and child.poll() is None:
                os.killpg(child.pid, signal.SIGTERM)
                try:
                    child.wait(timeout=10)
                except sp.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL)
                    child.wait()


def validate_run(result, plan, target):
    if result['status'] not in ('MEASURED', 'MEASURED_WITH_WARNINGS'):
        raise RuntimeError('Incomplete run')
    if result['toolchains'] != plan['reference_toolchains'] or result['fixture_hash'] != plan['fixture_hash']:
        raise RuntimeError('Toolchain or shared fixture differs from frozen baseline')
    actual = dict(result['protocol'])
    if actual.pop('compile_target_filter') != target or actual.pop('fixture_target') != bench.TARGET:
        raise RuntimeError('Wrong target selection/fixture')
    if actual.pop('harness_hash') != bench.digest(bench.__file__):
        raise RuntimeError('Harness changed during run')
    expected = dict(plan['reference_protocol'])
    expected.pop('harness_hash')
    for case in actual['inputs']:
        case.pop('provenance', None)
    expected['inputs'] = bench.select_compile_cases(expected['inputs'], target)
    if actual != expected or len(actual['inputs']) != plan['compile_cases'][target]:
        raise RuntimeError('Protocol or inputs differ from preregistration')


def validate_calibration(directory, plan, target, returncode):
    first = json.loads((directory / 'calibration-run1.json').read_text())
    second = json.loads((directory / 'calibration-run2.json').read_text())
    # validate_run copies/mutates nested input metadata; preserve originals for comparisons.
    for result in (first, second):
        validate_run(json.loads(json.dumps(result)), plan, target)
    recalculated = bench.calibration(first, second)
    recorded = json.loads((directory / 'calibration.json').read_text())
    if recalculated != recorded or returncode != (0 if recorded['status'] == 'PASS' else 2):
        raise RuntimeError('Calibration output/exit code inconsistent')
    return recorded


def verify_git(commit):
    if not re.fullmatch('[0-9a-f]{40}', commit or ''):
        raise RuntimeError('Full preregistered commit SHA required')
    head = sp.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    if head != commit or sp.check_output(['git', 'status', '--porcelain'], text=True).strip():
        raise RuntimeError('Require clean checkout of the exact preregistered commit')
    remote = sp.check_output(['git', 'ls-remote', 'origin', 'refs/heads/main'], text=True).split()[0]
    if remote != commit:
        raise RuntimeError('Preregistration must already be pushed to origin/main')
    return sp.check_output(['git', 'show', '-s', '--format=fuller', commit], text=True)


def verify_inputs(plan):
    """Reject changed binaries, flags or header trees before any compiler starts."""
    verified = {}
    def check(path, expected):
        path = str(Path(path).resolve())
        if path not in verified:
            verified[path] = bench.digest(path)
        if verified[path] != expected:
            raise RuntimeError('Frozen input changed: '+path)
    for toolchain in plan['reference_toolchains'].values():
        for tool in toolchain['tools'].values():
            check(tool['path'], tool['sha256'])
        check(toolchain['loader'], toolchain['loader_sha256'])
        for name, sha in toolchain['runtime_sha256'].items():
            check(Path(toolchain['library_path'])/name, sha)
    protocol = plan['reference_protocol']
    check(bench.INPUTS/'generate_synthetic.py', protocol['generator_hash'])
    if bench.header_tree_hash(Path(protocol['resource_dir'])/'include') != protocol['resource_header_hash']:
        raise RuntimeError('Resource headers changed')
    for source in (protocol, protocol['additional_target']):
        root=Path(source['sysroot'])
        sha=bench.json_digest({'usr/include':bench.header_tree_hash(root/'usr/include'),
                               'gcc':bench.header_tree_hash(root/'usr/lib/gcc')})
        if sha != source['sysroot_header_hash']:raise RuntimeError('Sysroot headers changed')
    current=[]
    for target,folder in ((bench.TARGET,'real_tu'),(bench.AARCH64_TARGET,'real_tu_aarch64')):
        for case in bench.real_inputs(bench.INPUTS/folder,target):
            name=case['name'] if target==bench.TARGET else 'real_aarch64_'+case['name'][5:]
            current.append(dict(name=name,target=target,sha256=case['sha256'],flags=case['flags']))
    keys=('name','target','sha256','flags')
    expected=[{k:case[k] for k in keys} for case in protocol['inputs'] if case['name'].startswith('real_')]
    if current != expected:raise RuntimeError('Frozen real TU inputs/flags changed')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true', help='actually launch this single registered attempt')
    parser.add_argument('--quiet-window-confirmed', action='store_true', help='only after user confirms desktop applications closed')
    parser.add_argument('--preregistered-commit', help='full SHA of the already pushed preregistration commit')
    args = parser.parse_args(argv)
    plan = json.loads(PLAN.read_text())
    if not args.run:
        print(json.dumps({t:dict(calibration=commands(plan,t),formal_if_pass=commands(plan,t,True))
                          for t in plan['order']}, indent=2))
        return 0
    if not args.quiet_window_confirmed:
        parser.error('WAITING_USER_CONFIRMATION: no compiler started')
    git_evidence = verify_git(args.preregistered_commit)
    output = Path(plan['output'])
    output.mkdir(parents=True, exist_ok=False)  # A refusal/failure also leaves an immutable attempt record.
    state = dict(status='STARTING', started=timestamp(), preregistered_commit=args.preregistered_commit,
                 plan_sha256=bench.digest(PLAN), user_quiet_confirmation=True, targets={})
    def save():
        bench.save(output/'attempt.json', state)
    try:
        (output/'preregistration-git.txt').write_text(git_evidence)
        before = load_sample()
        before['meminfo_raw'] = Path('/proc/meminfo').read_text()
        before['mem_available_bytes'] = int(next(l.split()[1] for l in before['meminfo_raw'].splitlines()
                                                if l.startswith('MemAvailable:'))) * 1024
        before['top20_rss'] = sp.check_output(['ps','-eo','pid,comm,rss','--sort=-rss'],text=True).splitlines()[:21]
        bench.save(output/'host-before.json', before)
        save()
        require_quiet(before)
        verify_inputs(plan)
        bench.memory_guard()
        state['status'] = 'RUNNING'
        with LoadMonitor(output) as monitor:
            for target in plan['order']:
                directory = output/target
                directory.mkdir()
                row = dict(started=timestamp(),status='CALIBRATING')
                state['targets'][target] = row
                save()
                rc = execute(commands(plan,target), directory/'calibration-process', monitor)
                cal = validate_calibration(directory, plan, target, rc)
                row.update(calibration_status=cal['status'],noise_floor_pct=cal['noise_floor_pct'],formal_ran=False)
                if cal['status'] == 'PASS':
                    row['status'] = 'FORMAL_RUNNING';save()
                    if execute(commands(plan,target,True), directory/'formal-process', monitor) != 0:
                        raise RuntimeError('Formal run failed: '+target)
                    result=json.loads((directory/'formal.json').read_text())
                    validate_run(json.loads(json.dumps(result)),plan,target)
                    first=json.loads((directory/'calibration-run1.json').read_text())
                    for key in ('protocol_hash','fixture_hash','toolchains'):
                        if result[key] != first[key]:raise RuntimeError('Formal differs from calibration: '+key)
                    row.update(formal_ran=True,formal_status=result['status'])
                row.update(status='COMPLETE',ended=timestamp());save()
        if monitor.error:
            raise RuntimeError('Load sampler failed: '+str(monitor.error))
        for row in state['targets'].values():
            samples = [s for s in monitor.samples if row['started'] <= s['timestamp'] <= row['ended']]
            row['loadavg_observations'] = load_summary(samples) if samples else None
        state['status']='COMPLETE_NO_MORE_LOCAL_ATTEMPTS'
        state['next']='Three reviews and Quickbuild; no local retries regardless of outcome'
        return 0 if all(r['calibration_status']=='PASS' for r in state['targets'].values()) else 2
    except BaseException as error:
        state.update(status='REFUSED' if str(error).startswith('REFUSED_LOAD') else 'STOPPED',error=str(error))
        print(state['status'],str(error),file=sys.stderr)
        return 2
    finally:
        state['ended']=timestamp();save()


if __name__=='__main__':
    def interrupted(signum, _frame):
        raise KeyboardInterrupt('signal '+str(signum))
    signal.signal(signal.SIGTERM,interrupted)
    signal.signal(signal.SIGINT,interrupted)
    raise SystemExit(main())
