#!/usr/bin/env python3
"""Read-only BOLT/RPM and user-space perf probes; never builds or installs tools."""
import argparse
import datetime
import json
from pathlib import Path
import shlex
import shutil
import subprocess

NAMES = ('llvm-bolt', 'perf2bolt', 'merge-fdata')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--inventory', type=Path, required=True, help='baseline rpm-inventory.json')
    p.add_argument('--toolchain', type=Path, required=True, help='unpacked root containing bin/')
    p.add_argument('--build-root', type=Path, required=True, help='R1 scratch root (read only)')
    p.add_argument('--output', type=Path, required=True, help='new evidence directory under temp/')
    p.add_argument('--perf', type=Path, help='actual perf executable, bypassing a missing-kernel wrapper')
    a = p.parse_args()
    workspace = Path(__file__).resolve().parents[1]
    a.output = a.output.resolve()
    if not a.output.is_relative_to(workspace/'temp') or a.output.exists():
        p.error('--output must be a new directory under workspace temp/')
    a.output.mkdir(parents=True)
    rows = []

    def run(argv, name, timeout=60):
        result = subprocess.run(list(map(str, argv)), stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True, timeout=timeout)
        (a.output/(name+'.log')).write_text('$ '+shlex.join(map(str, argv))+'\n'+result.stdout+
                                           f'\n[exit={result.returncode}]\n')
        rows.append(dict(name=name, argv=list(map(str, argv)), exit_code=result.returncode,
                         output=str(a.output/(name+'.log'))))
        return result

    inventory = json.loads(a.inventory.read_text())
    packages = []
    for item in inventory:
        rpm = Path(item['path'])
        result = run(['rpm', '-qpl', rpm], 'rpm-files-'+item['name'])
        if result.returncode:
            raise RuntimeError('RPM file listing failed: '+str(rpm))
        hits = [line for line in result.stdout.splitlines() if Path(line).name in NAMES]
        packages.append(dict(rpm=str(rpm), bolt_tools=hits))
    buildbin = a.build_root/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin'
    locations = {name: {str(base/name): (base/name).exists()
                       for base in [a.toolchain/'bin', buildbin]} for name in NAMES}
    path_tools = {name: shutil.which(name) for name in NAMES}
    perf_candidates = sorted({str(q.resolve()) for base, pattern in [
        (Path('/usr/lib/linux-tools'), '*/perf'), (Path('/usr/lib'), 'linux-*/perf')]
        for q in base.glob(pattern) if q.is_file()})
    run(['uname', '-r'], 'kernel')
    run(['perf', '--version'], 'perf-wrapper-version')
    paranoid = Path('/proc/sys/kernel/perf_event_paranoid').read_text().strip()
    (a.output/'perf_event_paranoid.txt').write_text(paranoid+'\n')
    chosen = str(a.perf.resolve()) if a.perf else (perf_candidates[0] if len(perf_candidates)==1 else None)
    probes = []
    if chosen:
        run([chosen, '--version'], 'perf-actual-version')
        if shutil.which('getcap'):
            run(['getcap', chosen], 'perf-capabilities')
        workload = ['python3', '-c', 'import time; end=time.monotonic()+0.2\nwhile time.monotonic()<end: pass']
        for event in ['cycles:u', 'cpu-clock:u']:
            tag = event.split(':')[0]
            argv = [chosen, 'record', '-e', event, '-F', '99', '-o',
                    str(a.output/(tag+'.perf.data')), '--']+workload
            result = run(argv, 'perf-user-'+tag)
            probes.append(dict(event=event, privilege='user', exit_code=result.returncode))
        if not any(x['exit_code']==0 for x in probes):
            argv = ['sudo', '-n', chosen, 'record', '-e', 'cycles:u', '-F', '99', '-o',
                    str(a.output/'sudo-cycles.perf.data'), '--']+workload
            result = run(argv, 'perf-sudo-cycles')
            probes.append(dict(event='cycles:u', privilege='sudo-n', exit_code=result.returncode))
    status = dict(timestamp=datetime.datetime.now().astimezone().isoformat(),
                  rpm_count=len(packages), packages=packages, locations=locations, path_tools=path_tools,
                  perf_event_paranoid=paranoid, perf_candidates=perf_candidates, actual_perf=chosen,
                  sampling_probes=probes, commands=rows)
    (a.output/'result.json').write_text(json.dumps(status, indent=2)+'\n')
    print(json.dumps({k:v for k,v in status.items() if k not in ['commands','packages']}, indent=2))
    print('RPM tool hits:', sum(len(x['bolt_tools']) for x in packages))


if __name__ == '__main__':
    main()
