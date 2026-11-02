"""Child holds its own cgroup alive until the final kernel memory.peak is read."""
from common import *
import sys,datetime,traceback
out=Path(sys.argv[1]);argv=json.loads(Path(sys.argv[2]).read_text());start=time.time_ns();rc=1
try:rc=subprocess.run(argv).returncode
except BaseException:traceback.print_exc()
finally:
 cg=Path('/sys/fs/cgroup')/next(l.split(':',2)[2] for l in Path('/proc/self/cgroup').read_text().splitlines() if l.startswith('0::')).lstrip('/')
 stats={}
 for n in ['memory.peak','memory.events','memory.swap.peak','memory.max','memory.swap.max','cpu.max']:
  try:stats[n]=(cg/n).read_text()
  except OSError as e:stats[n]='UNKNOWN '+str(e)
 save(out/'service-result.json',{'rc':rc,'start_ns':start,'end_ns':time.time_ns(),'stats':stats})
 # Keep the empty cgroup alive until the monitor has read/reset its peak FD.
 deadline=time.monotonic()+180
 while not (out/'monitor-release').exists() and time.monotonic()<deadline:time.sleep(.2)
 if not (out/'monitor-release').exists():rc=1
 print('PGO_STAGE 已结束',datetime.datetime.now().astimezone().isoformat(),'status='+('ok' if rc==0 else 'failed'),flush=True)
sys.exit(rc)
