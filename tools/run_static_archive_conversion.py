#!/usr/bin/env python3
"""Offline archive conversion under a capped scope; never runs GBS or edits spec.

Uses the existing 30-second free/load/RSS and 2-second process monitors,
MemorySwapMax=0, nice 15, ionice idle, emergency stop below 2 GiB available,
and completion handshake to preserve final cgroup counters and reap samplers.
The offline cap is min(18 GiB, floor(MemAvailable/GiB)-4); full-build gates
are neither called nor changed by this offline admission policy.
"""
import argparse
import json
from pathlib import Path
import shlex
import shutil
import signal
import sys
from types import SimpleNamespace

import build_llvm_x86_64 as guard
from run_bolt_stage import summarize


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--log-dir', type=Path, required=True)
    p.add_argument('--loader', type=Path, required=True)
    p.add_argument('--library-path', required=True)
    a = p.parse_args()
    log = a.log_dir.resolve()
    if log.exists() or not log.is_relative_to(guard.WORKSPACE/'temp'):
        p.error('new --log-dir below workspace temp/ required')
    audit = guard.Audit(log)
    try:
        for cmd in (['nproc'], ['free', '-g'], ['df', '-h', log]):
            audit.run(cmd)
        available = guard.mem_available()
        cap = min(18, available//guard.GIB-4)
        if cap < 4 or shutil.disk_usage(log).free < 60*guard.GIB:
            raise RuntimeError('offline stage needs 4 GiB cap plus 4 GiB reserve and 60 GiB disk')
        audit.run(['systemd-run', '--user', '--scope', '-p', 'MemoryMax=1G', '-p', 'MemorySwapMax=0', '/bin/true'])
        root = a.root.resolve()
        cmd = [sys.executable, str(Path(__file__).with_name('convert_static_archives.py')),
               '--root', str(root), '--output', str(a.output.resolve()),
               '--clang', str(root/'usr/bin/clang-22'), '--llvm-dis', str(root/'usr/bin/llvm-dis'),
               '--loader', str(a.loader), '--library-path', a.library_path]
        completion, release = log/'conversion.exit', log/'release'
        trap = ('status=$?; printf "%s\\n" "$status" > '+shlex.quote(str(completion))+
                '; while [ ! -e '+shlex.quote(str(release))+' ]; do sleep .2; done; exit "$status"')
        script = log/'stage.sh'
        script.write_text('set -eu\ntrap '+shlex.quote(trap)+' EXIT\n'+shlex.join(cmd)+'\n')
        plan = dict(memory_max_gib=cap, operation='OFFLINE_STATIC_ARCHIVE_NATIVE_CONVERSION',
                    available_bytes=available, reserve_gib=4, workers=4, per_tool_as_bytes=4*guard.GIB,
                    full_build_policy_unchanged=True)
        audit.json('offline-plan.json', plan)
        guard.build(audit, SimpleNamespace(buildroot=log), plan, None, 'systemd',
                    command=['/bin/bash', str(script)], cache_check=False,
                    completion_file=completion, release_file=release)
        return 0
    except (Exception, KeyboardInterrupt) as error:
        audit.json('stopped.json', dict(reason=str(error), time=guard.stamp()))
        audit.log('STOPPED '+str(error))
        return 2
    finally:
        summarize(log)
        audit.stream.close()


if __name__ == '__main__':
    def interrupt(sig, frame):
        raise KeyboardInterrupt(f'signal {sig}')
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGQUIT):
        signal.signal(sig, interrupt)
    raise SystemExit(main())
