"""Resource admission watchdog independent of any potentially blocking du."""
import sys,time,json,subprocess
from pathlib import Path
D=Path(__file__).resolve().parent;label=sys.argv[1];unit='bolt-cache-'+label+'.service';E=D/label
cg=Path('/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice')/unit
deadline=time.monotonic()+30
while not cg.exists() and time.monotonic()<deadline:time.sleep(.2)
while cg.exists():
    now=time.time_ns();mem=int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))*1024
    row={'time_ns':now,'mem_available':mem}
    try:
        for name in ['memory.current','memory.peak','memory.events','cgroup.events']:row[name]=(cg/name).read_text().strip()
    except FileNotFoundError:break
    with (E/'independent-guard.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
    lease_expired=False
    try:
        leases=[json.loads(x) for x in (E/'leases.jsonl').read_text().splitlines()]
        last=[x for x in leases if x.get('acquired') or x.get('released')][-1]
        if last.get('acquired') and row.get('cgroup.events','').find('frozen 0')>=0:
            lease_expired=(now-last['time_ns'])/1e9>3500
    except (OSError,ValueError,IndexError):pass
    if lease_expired:
        (E/'independent-guard-stop.json').write_text(json.dumps(row))
        subprocess.run(['systemctl','--user','stop',unit]);break
    time.sleep(5)
