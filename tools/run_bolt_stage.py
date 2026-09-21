#!/usr/bin/env python3
"""Run one authorized BOLT experiment stage with the baseline resource guard.

18 GiB cgroup by default (6 GiB for bounded pure rewriting), zero swap, nice 15, idle IO; 2s VmHWM and 30s free/load/RSS
samples, emergency stop below 2 GiB available, and sampler cleanup on exit.
The CMake gate is not applicable to arbitrary experiment commands. Full GBS
builds retain their normal gate. This script never runs gbs build or edits spec.
"""
import argparse
import json
from pathlib import Path
import shlex
import shutil
import signal
from types import SimpleNamespace
import uuid

import build_llvm_x86_64 as guard


def summarize(directory):
    """Summarize observed per-process VmHWM separately from aggregate scope peak."""
    peaks={}
    memory=directory/'process-memory.jsonl'
    if memory.exists():
        with memory.open() as stream:
            for line in stream:
                sample=json.loads(line)
                for row in sample['rows']:
                    argv=row['argv']
                    if not argv:continue
                    index=0
                    if 'ld-linux' in Path(argv[0]).name:
                        index=1
                        while index<len(argv) and argv[index].startswith('--'):
                            index+=2 if argv[index] in ['--library-path','--argv0','--preload'] else 1
                    executable=argv[index] if index<len(argv) else argv[0]
                    hwm=row['info'].get('VmHWM','').split()
                    if not hwm:continue
                    key=(row['pid'],executable);value=int(hwm[0])
                    if value>peaks.get(key,{}).get('vmhwm_kib',0):
                        peaks[key]=dict(pid=row['pid'],executable=executable,vmhwm_kib=value,
                                        timestamp=sample['timestamp'],threads=row['info'].get('Threads'))
    outcome=json.loads((directory/'outcome.json').read_text()) if (directory/'outcome.json').exists() else None
    scope=json.loads((directory/'scope-after-rpm.json').read_text()) if (directory/'scope-after-rpm.json').exists() else None
    samples=[]
    if (directory/'samples.jsonl').exists():
        with (directory/'samples.jsonl').open() as stream:samples=[json.loads(line) for line in stream]
    result=dict(outcome=outcome,scope=scope,process_peaks=sorted(peaks.values(),key=lambda x:x['vmhwm_kib'],reverse=True),
                minimum_available_bytes=min((s['available_bytes'] for s in samples),default=None),
                resource_sample_count=len(samples))
    (directory/'memory-summary.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--log-dir', type=Path, required=True, help='new directory under workspace temp/')
    p.add_argument('--root', type=Path, help='optional existing GBS chroot; run as abuild')
    p.add_argument('--cwd', required=True, help='working directory (root-relative absolute path in chroot mode)')
    p.add_argument('--memory-max-gib', type=int, choices=[6,18], default=18,
                   help='experiment-only cap; 6 for pure BOLT rewriting; does not change full-build policy')
    p.add_argument('--script', type=Path, help='host file containing the exact stage shell script')
    p.add_argument('command', nargs=argparse.REMAINDER, help='command after --; mutually exclusive with --script')
    a = p.parse_args()
    log = a.log_dir.resolve()
    if not log.is_relative_to(guard.WORKSPACE/'temp') or log.exists():
        p.error('new --log-dir under workspace temp/ required')
    command = a.command[1:] if a.command[:1]==['--'] else a.command
    if bool(command)==bool(a.script): p.error('choose exactly one command or --script')
    root = a.root.resolve() if a.root else None
    if root and not root.is_relative_to(guard.WORKSPACE/'temp'):
        p.error('--root must be an existing workspace temp/ root')
    audit = guard.Audit(log)
    try:
        for cmd in (['nproc'],['free','-g'],['df','-h',root or log]): audit.run(cmd)
        cpus = int(audit.run(['nproc']).stdout)
        guard.validate_resources(guard.mem_available(),shutil.disk_usage(root or log).free,cpus)
        audit.run(['systemd-run','--user','--scope','-p','MemoryMax=1G','-p','MemorySwapMax=0','/bin/true'])
        marker = Path('/home/abuild')/('bolt-stage-'+uuid.uuid4().hex) if root else log
        completion, release = marker/'command.exit', marker/'release'
        host_completion = root/str(completion).lstrip('/') if root else completion
        host_release = root/str(release).lstrip('/') if root else release
        trap = ('status=$?; printf "%s\\n" "$status" > '+shlex.quote(str(completion))+
                '; while [ ! -e '+shlex.quote(str(release))+' ]; do sleep .2; done; exit "$status"')
        body = a.script.read_text() if a.script else shlex.join(command)+'\n'
        # Host-side single-command stages get a second, command-specific time record.
        if not root and not a.script:
            body = shlex.join(['/usr/bin/time','-v','-o',str(log/'tool-time-v.txt')]+command)+'\n'
        script = ('set -eu\n'+('mkdir '+shlex.quote(str(marker))+'\n' if root else '')+
                  'trap '+shlex.quote(trap)+' EXIT\ncd '+shlex.quote(a.cwd)+'\n'+body)
        script_path = log/'stage.sh'; script_path.write_text(script)
        audit.json('stage.json',dict(root=str(root) if root else None,cwd=a.cwd,command=command,
                                    body=body,completion=str(host_completion),release=str(host_release)))
        if root:
            cmd = ['gbs','chroot','--root',str(root)]
            stdin = 'exec '+shlex.join(['su','-s','/bin/bash','-c',script,'-','abuild'])+'\n'
        else:
            cmd,stdin = ['/bin/bash',str(script_path)],None
        plan = dict(memory_max_gib=a.memory_max_gib,operation='AUTHORIZED_BOLT_EXPERIMENT',ninja_jobs=4,
                    compile_jobs=4,link_jobs=1)
        args = SimpleNamespace(buildroot=root.parents[2] if root else log)
        guard.build(audit,args,plan,None,'systemd',command=cmd,input_text=stdin,
                    completion_file=host_completion,release_file=host_release,cache_check=False)
        return 0
    except (Exception,KeyboardInterrupt) as error:
        audit.json('stopped.json',dict(reason=str(error),time=guard.stamp()))
        audit.log('STOPPED '+str(error));return 2
    finally:
        summarize(log)
        audit.stream.close()


if __name__=='__main__':
    def interrupted(signum, frame): raise KeyboardInterrupt(f'signal {signum}')
    for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP,signal.SIGQUIT):
        signal.signal(sig,interrupted)
    raise SystemExit(main())
