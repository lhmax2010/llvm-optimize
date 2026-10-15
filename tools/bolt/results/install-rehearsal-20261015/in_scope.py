import subprocess,os,json,time,sys,signal
from pathlib import Path
E=Path(__file__).resolve().parent
cg=Path('/sys/fs/cgroup'+Path('/proc/self/cgroup').read_text().strip().split('::')[1]);env=dict(os.environ,SUDO_ASKPASS=str(E/'askpass.sh'))
argv=['sudo','-A','-k','/usr/bin/python3',str(E/'root_wrapper.py')]
(E/'sudo-argv.json').write_text(json.dumps(argv,indent=2)+'\n')
with (E/'sudo.stdout').open('w') as out,(E/'sudo.stderr').open('w') as err:
 p=subprocess.Popen(argv,env=env,stdout=out,stderr=err,start_new_session=True)
 started=time.monotonic();cancelled=False
 while p.poll() is None:
  if not (E/'root-entry.json').exists() and time.monotonic()-started>600:
   os.killpg(p.pid,signal.SIGTERM);cancelled=True;break
  time.sleep(.5)
 rc=p.wait()
(E/'sudo-result.json').write_text(json.dumps({'rc':rc,'wall':time.monotonic()-started,'graphical_prompt_timeout':cancelled},indent=2)+'\n')
if not (E/'rehearsal-result.json').exists():
 (E/'rehearsal-result.json').write_text(json.dumps({'status':'NOT RUN','reason':'single graphical sudo invocation failed/cancelled/timed out; no retry','sudo_rc':rc},indent=2)+'\n')
final={}
for k in ['memory.max','memory.swap.max','memory.peak','memory.events','cgroup.procs']:
 try:final[k]=(cg/k).read_text()
 except OSError:pass
(E/'final-cgroup.json').write_text(json.dumps(final,indent=2)+'\n')
sys.exit(rc)
