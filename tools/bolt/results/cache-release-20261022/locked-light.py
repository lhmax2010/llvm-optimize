"""Local I/O work: shared lease <=3300 seconds; never alters product code."""
import fcntl,json,os,signal,subprocess,sys,time
from pathlib import Path
D=Path(__file__).resolve().parent;label=sys.argv[1];argv=sys.argv[2:];E=D/label;E.mkdir(exist_ok=False)
lock=open('/home/linhao/Toolchain/development/heavy-stage.lock','a+');wait=time.monotonic()
while True:
 try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);break
 except BlockingIOError:
  if time.monotonic()-wait>=7200:raise RuntimeError('shared lock timeout')
  time.sleep(5)
start=time.monotonic();p=None
(E/'start.json').write_text(json.dumps({'time_ns':time.time_ns(),'argv':argv,'wait_seconds':start-wait,'lock_seconds_limit':3300},indent=2)+'\n')
try:
 with (E/'stdout').open('wb') as out,(E/'stderr').open('wb') as err:
  p=subprocess.Popen(argv,stdout=out,stderr=err,start_new_session=True)
  try:rc=p.wait(timeout=3300)
  except BaseException:
   os.killpg(p.pid,signal.SIGKILL);p.wait();raise
 (E/'result.json').write_text(json.dumps({'rc':rc,'time_ns':time.time_ns(),'held_seconds':time.monotonic()-start},indent=2)+'\n')
finally:
 fcntl.flock(lock,fcntl.LOCK_UN);lock.close()
sys.exit(rc)
