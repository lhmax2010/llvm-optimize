#!/usr/bin/env python3
"""Measured offline commands: compile AS=4 GiB, links use the enclosing cgroup.

All commands must run inside the caller's capped scope. Samples are per process,
not summed virtual address spaces; short-lived processes may escape sampling.
"""
import json
from pathlib import Path
import resource
import subprocess
import threading
import time

from convert_static_archives import Commands


def bounded_argv(argv, timing, phase):
    if phase not in ('compile', 'link', 'run', 'query', 'strip'):
        raise ValueError('unknown command phase')
    bounds = ['--as=4294967296'] if phase == 'compile' else []
    return ['/usr/bin/time', '-f', '%e %U %S %M %x', '-o', str(timing),
            'prlimit', *bounds, '--core=0', '--', *map(str, argv)]


def process_tree(pid):
    pending, seen, rows = [pid], set(), []
    while pending:
        current = pending.pop()
        if current in seen:
            continue
        seen.add(current)
        root = Path('/proc')/str(current)
        try:
            fields = dict(line.split(':', 1) for line in (root/'status').read_text().splitlines())
            children = (root/'task'/str(current)/'children').read_text().split()
            pending.extend(map(int, children))
            row = dict(pid=current, name=fields['Name'].strip(),
                       argv=(root/'cmdline').read_bytes().replace(b'\0', b' ').decode(errors='replace'))
            for name in ('VmPeak', 'VmSize', 'VmHWM', 'VmRSS', 'Threads'):
                row[name] = int(fields.get(name, '0').split()[0])
            rows.append(row)
        except (OSError, ProcessLookupError):
            continue
    return rows


class MeasuredCommands(Commands):
    def run(self, argv, prefix, stdout=None, *, phase='query', expected_exit=0):
        prefix = Path(prefix)
        timing, log = prefix.with_suffix('.time'), prefix.with_suffix('.log')
        if phase == 'link' and resource.getrlimit(resource.RLIMIT_AS)[0] != resource.RLIM_INFINITY:
            raise RuntimeError('link parent already has an AS limit; refuse misleading measurement')
        command = bounded_argv(argv, timing, phase)
        start, done, samples, errors = time.monotonic(), threading.Event(), [], []
        def monitor(pid):
            try:
                with prefix.with_suffix('.memory.jsonl').open('w', buffering=1) as stream:
                    while not done.is_set():
                        row = dict(elapsed=time.monotonic()-start, processes=process_tree(pid))
                        samples.append(row)
                        stream.write(json.dumps(row)+'\n')
                        done.wait(0.05)
            except BaseException as error:
                errors.append(str(error))
        with log.open('wb') as err:
            with self.lock:
                if self.stop.is_set():
                    raise RuntimeError('cancelled after first failure')
                child = subprocess.Popen(command, stdout=stdout if stdout is not None else err,
                                         stderr=err, start_new_session=True)
                self.children.add(child)
            sampler = threading.Thread(target=monitor, args=(child.pid,))
            sampler.start()
            try:
                rc = child.wait()
            except BaseException:
                self.cancel()
                child.wait()
                raise
            finally:
                done.set()
                sampler.join()
                with self.lock:
                    self.children.discard(child)
        processes = [p for row in samples for p in row['processes']]
        record = dict(argv=list(map(str, argv)), bounded_argv=command, phase=phase,
                      as_bytes=4294967296 if phase == 'compile' else None,
                      elapsed_seconds=time.monotonic()-start, exit=rc, expected_exit=expected_exit,
                      sample_interval_seconds=0.05, sample_count=len(samples), sampler_reaped=True,
                      sample_errors=errors,
                      observed_max={k:max((p[k] for p in processes), default=0)
                                    for k in ('VmPeak','VmSize','VmHWM','VmRSS','Threads')})
        if timing.exists():
            record['time_raw'] = timing.read_text()
            line = record['time_raw'].splitlines()[-1].split()
            if len(line) == 5:
                record.update(wall=float(line[0]), user=float(line[1]), sys=float(line[2]), max_rss_kib=int(line[3]))
        prefix.with_suffix('.json').write_text(json.dumps(record, indent=2)+'\n')
        accepted = rc != 0 if expected_exit == 'nonzero' else rc == expected_exit
        if not accepted or errors:
            self.cancel()
            raise RuntimeError(f'command failed ({rc}): {argv}; see {log}; monitor errors={errors}')
        return record
