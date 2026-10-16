from pathlib import Path
import subprocess,os,json,time,sys,signal
E=Path(__file__).resolve().parent;cg=Path('/sys/fs/cgroup'+Path('/proc/self/cgroup').read_text().strip().split('::')[1]);env=dict(os.environ,SUDO_ASKPASS=str(E/'askpass.sh'))
avail=int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))*1024
assert avail>=6*1024**3
argv=['sudo','-A','/usr/bin/python3',str(E/'root_parse.py')];(E/'sudo-argv.json').write_text(json.dumps(argv,indent=2)+'\n')
with (E/'sudo.stdout').open('w') as out,(E/'sudo.stderr').open('w') as err:
 p=subprocess.Popen(argv,env=env,stdout=out,stderr=err,start_new_session=True);ts=time.monotonic()
 while p.poll() is None:
  if not (E/'root-entry.json').exists() and time.monotonic()-ts>600:
   os.killpg(p.pid,signal.SIGTERM);break
  time.sleep(.5)
 rc=p.wait()
(E/'sudo-result.json').write_text(json.dumps({'rc':rc,'seconds':time.monotonic()-ts},indent=2)+'\n')
data={}
for n in ['memory.max','memory.swap.max','memory.peak','memory.events']:
 try:data[n]=(cg/n).read_text()
 except OSError:pass
(E/'final-cgroup.json').write_text(json.dumps(data,indent=2)+'\n')
print('sudo rc',rc)
sys.exit(rc)
