#!/usr/bin/env python3
"""One final BOLT instrumentation attempt: 22 GiB, no swap, one worker.

Without --run, print the exact authorized command and policy. With --run, use
the existing stripped ELF and docs/15 command (only thread-count changes).
The fixed evidence directory is an exclusive attempt marker: no retries.
This entry point cannot run a build, accept another command, or change a cap.
Full LLVM builds and run_bolt_stage.py continue to use their 18 GiB policies.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shlex
import signal
import threading
import time
from types import SimpleNamespace

import build_llvm_x86_64 as guard
from run_bolt_stage import summarize

W = guard.WORKSPACE
PREVIOUS = W/'temp/bolt-measurement-20260918/run/instrument-02/stage.json'
PREVIOUS_SHA256 = '615a52272eaa6515ad81c8e21c480872684261f4a698bed3d41749d281f28e2a'
INPUT_SHA256 = 'eccfb075bc3b2a6ca2bda5a2a6e68f6a29ba48b5586cb603f4b46080f656013e'
EVIDENCE = W/'temp/bolt-final-20260918/instrument'
FINAL_BOLT_MEMORY_GIB = 22


def final_plan():
    # Local experiment policy, never assign guard.MAX_BUILD_MEMORY_GIB.
    return dict(memory_max_gib=FINAL_BOLT_MEMORY_GIB, memory_swap_max_bytes=0,
                operation='FINAL_BOLT_INSTRUMENTATION_ONLY', bolt_workers=1)


def single_thread_command(previous):
    """Preserve every argv element except the one authorized replacement."""
    if (len(previous) != 13 or Path(previous[3]).name != 'llvm-bolt'
            or previous[5:7] != ['-instrument', '--thread-count=4']
            or previous[11] != '-o'):
        raise ValueError('not the expected docs/15 instrumentation command')
    result = list(previous)
    result[6] = '--thread-count=1'
    return result


def load_command():
    raw = PREVIOUS.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PREVIOUS_SHA256:
        raise RuntimeError('docs/15 command evidence changed')
    old = json.loads(raw)
    return old, single_thread_command(old['command'])


def meminfo_bytes(text):
    values = {}
    for line in text.splitlines():
        key, rest = line.split(':', 1)
        fields = rest.split()
        values[key] = int(fields[0]) * (1024 if fields[1:] == ['kB'] else 1)
    return values


def detailed_summary(log):
    result = summarize(log)
    points = [json.loads(line) for line in (log/'host-memory-2s.jsonl').read_text().splitlines()]
    result['host_min_available_bytes_2s'] = min((p['available_bytes'] for p in points), default=None)
    result['host_observer_reaped'] = not any(t.name == 'bolt-host-memory' for t in threading.enumerate())
    timeline = ([json.loads(line) for line in (log/'process-memory.jsonl').read_text().splitlines()]
                if (log/'process-memory.jsonl').exists() else [])
    for process in result['process_peaks']:
        if Path(process['executable']).name != 'llvm-bolt':
            continue
        indices = [i for i, sample in enumerate(timeline)
                   if any(row['pid'] == process['pid'] for row in sample['rows'])]
        first, last = indices[0], indices[-1]
        lower = timeline[last]['elapsed'] - timeline[first]['elapsed']
        birth_lower = timeline[first-1]['elapsed'] if first else 0
        death_upper = (timeline[last+1]['elapsed'] if last+1 < len(timeline)
                       else result['outcome']['elapsed_seconds'])
        process['lifetime_bounds_seconds'] = [lower, death_upper-birth_lower]
    scope = result.get('scope') or {}
    peak, maximum = scope.get('MemoryPeak'), scope.get('MemoryMax')
    result['cap_truncated'] = bool(guard.oom_kills(scope) and peak == maximum)
    (log/'final-summary.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run', action='store_true', help='perform the single authorized attempt; never retries')
    return p


def main():
    args = parser().parse_args()
    old, command = load_command()
    print(json.dumps(dict(policy=final_plan(), command=command, evidence=str(EVIDENCE)), indent=2), flush=True)
    if not args.run:
        return 0
    # Audit.mkdir(exist_ok=False) is also the permanent one-attempt interlock.
    audit = guard.Audit(EVIDENCE)
    stop = threading.Event()
    observer = None
    try:
        audit.json('command-diff.json', dict(previous=str(PREVIOUS), previous_sha256=PREVIOUS_SHA256,
                   changed=[dict(index=i, before=x, after=y) for i, (x, y) in
                            enumerate(zip(old['command'], command)) if x != y]))
        source, output = Path(command[4]), Path(command[-1])
        profile = Path(command[8].split('=', 1)[1]).parent
        if output.exists() or list(profile.iterdir()):
            raise RuntimeError('refuse to overwrite any instrumented binary or profile')
        with source.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        if digest != INPUT_SHA256:
            raise RuntimeError('stripped input identity changed')
        audit.json('input.json', dict(path=str(source), bytes=source.stat().st_size, sha256=digest))
        raw = audit.run(['cat', '/proc/meminfo']).stdout
        (EVIDENCE/'meminfo-before.txt').write_text(raw)
        memory = meminfo_bytes(raw)
        audit.json('meminfo-before-bytes.json', memory)
        audit.run(['free', '-g'])
        processes = audit.run(['ps', '-eo', 'pid,ppid,user,rss,vsz,comm', '--sort=-rss']).stdout
        (EVIDENCE/'major-memory-processes.txt').write_text('\n'.join(processes.splitlines()[:21])+'\n')
        audit.run(['nproc'])
        audit.run(['df', '-h', EVIDENCE])
        available = memory['MemAvailable']
        audit.json('startup-policy.json', dict(available_bytes=available,
                   cap_bytes=22*guard.GIB, available_minus_cap_bytes=available-22*guard.GIB,
                   below_24_gib=available < 24*guard.GIB, admission='CONTINUE_AS_AUTHORIZED',
                   emergency_stop_below_bytes=2*guard.GIB, **final_plan()))
        # Below 24 GiB is informational, not a start veto in this final experiment.
        audit.run(['systemd-run', '--user', '--scope', '-p', 'MemoryMax=1G',
                   '-p', 'MemorySwapMax=0', '/bin/true'])
        completion, release = EVIDENCE/'command.exit', EVIDENCE/'release'
        trap = ('status=$?; printf "%s\\n" "$status" > '+shlex.quote(str(completion))+
                '; while [ ! -e '+shlex.quote(str(release))+' ]; do sleep .2; done; exit "$status"')
        body = shlex.join(['/usr/bin/time', '-v', '-o', str(EVIDENCE/'tool-time-v.txt')]+command)+'\n'
        script = 'set -eu\ntrap '+shlex.quote(trap)+' EXIT\ncd '+shlex.quote(old['cwd'])+'\n'+body
        stage = EVIDENCE/'stage.sh'
        stage.write_text(script)
        audit.json('stage.json', dict(root=None, cwd=old['cwd'], command=command, body=body,
                   completion=str(completion), release=str(release)))

        def host_samples():
            # Supplement the unchanged shared 30s free/load/tree sampler.
            with (EVIDENCE/'host-memory-2s.jsonl').open('w', buffering=1) as stream:
                start = time.monotonic()
                while True:
                    stream.write(json.dumps(dict(timestamp=guard.stamp(), elapsed=time.monotonic()-start,
                                                 available_bytes=guard.mem_available()))+'\n')
                    if stop.wait(2):
                        break

        observer = threading.Thread(target=host_samples, name='bolt-host-memory', daemon=False)
        observer.start()
        guard.build(audit, SimpleNamespace(buildroot=EVIDENCE), final_plan(), None, 'systemd',
                    command=['/bin/bash', str(stage)], completion_file=completion,
                    release_file=release, cache_check=False)
        if not output.is_file() or not output.stat().st_size:
            raise RuntimeError('no instrumented output despite successful exit')
        audit.json('success.json', dict(status='PASS', compiler=str(output), input=str(source),
                   profiles=str(profile), outcome=str(EVIDENCE/'outcome.json')))
        return 0
    except (Exception, KeyboardInterrupt) as error:
        audit.json('stopped.json', dict(reason=str(error), time=guard.stamp(), retry_allowed=False))
        audit.log('FINAL ATTEMPT STOPPED; NO RETRY: '+str(error))
        return 2
    finally:
        stop.set()
        if observer is not None:
            observer.join()
            detailed_summary(EVIDENCE)
        audit.stream.close()


if __name__ == '__main__':
    def interrupted(signum, frame):
        raise KeyboardInterrupt(f'signal {signum}')
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGQUIT):
        signal.signal(sig, interrupted)
    raise SystemExit(main())
