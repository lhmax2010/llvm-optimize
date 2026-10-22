"""Local controller handoff; existing frozen build, new-build admission unchanged."""
import fcntl,json,subprocess,time,sys,shutil
from pathlib import Path
D=Path(__file__).resolve().parent;label=sys.argv[1];E=D/label
unit='bolt-cache-'+label+'.service';lock=open('/home/linhao/Toolchain/development/heavy-stage.lock','a+');held=False;started=None
G=1024**3

def event(v):
 with (E/'leases.jsonl').open('a') as f:f.write(json.dumps(dict(time_ns=time.time_ns(),controller='adopt-frozen',**v))+'\n')
def ctl(*args):
 p=subprocess.run(['systemctl','--user',*args],capture_output=True,text=True,timeout=60)
 if args[0]!='show':event({'control':args,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
 p.check_returncode();return p.stdout.strip()
def mem():return int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))*1024

def release():
 global held
 if held:event({'released':True,'held_seconds':time.monotonic()-started});fcntl.flock(lock,fcntl.LOCK_UN);held=False

def acquire_resume():
 global held,started
 assert ctl('show',unit,'-p','FreezerState','--value')=='frozen'
 t=time.monotonic();mw=None
 while True:
  m=mem()
  if m<3*G:
   if mw is None:mw=time.monotonic()
   if time.monotonic()-mw>=3600:raise RuntimeError('frozen resume memory wait timeout')
   event({'waiting':'memory','available':m,'minimum':3*G});time.sleep(5);continue
  try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError:
   if time.monotonic()-t>=7200:raise RuntimeError('shared lock timeout')
   time.sleep(5);continue
  held=True;started=time.monotonic()
  if mem()<3*G:release();continue
  free=shutil.disk_usage(D).free
  if free<30*G:raise RuntimeError('local disk floor unavailable')
  event({'acquired':True,'memory_available':mem(),'minimum':3*G,'disk_free':free,'resume_only':True});return

completed=False
try:
 acquire_resume();ctl('thaw',unit)
 while True:
  state=ctl('show',unit,'-p','ActiveState','--value')
  if state not in ('active','activating','deactivating'):break
  if time.monotonic()-started>=3200:
   ctl('freeze',unit)
   assert ctl('show',unit,'-p','FreezerState','--value')=='frozen'
   release();time.sleep(1);acquire_resume();ctl('thaw',unit)
  time.sleep(1)
 result=ctl('show',unit,'-p','Result','-p','ExecMainStatus','-p','ActiveState')
 (E/'adopt-controller-result.json').write_text(json.dumps({'time_ns':time.time_ns(),'result':result},indent=2)+'\n')
 completed=True
finally:
 if not completed:ctl('stop',unit)
 release();lock.close()
