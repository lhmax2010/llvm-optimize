from pathlib import Path
import subprocess, json, time, fcntl, shutil
D=Path(__file__).resolve().parent;E=D.parents[2]/'llvm-optimize-bolt/tools/bolt/results/bolt-on-hybrid-20261024'
assert E.is_dir(),E
assert json.loads((E/'build-result.json').read_text())['exit_code']==0
unit='bolt-hybrid-verify-20261024.service'
plan=json.loads((D/'plan.json').read_text());lock=open('/home/linhao/Toolchain/development/heavy-stage.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX)
argv=['systemd-run','--user','--wait','--pipe','--unit='+unit,'-p','MemoryMax='+str(plan['MemoryMax_bytes']),'-p','MemorySwapMax=0','-p','Nice=10','-p','IOSchedulingClass=best-effort','-p','IOSchedulingPriority=7','-p','OOMPolicy=stop','-p','KillMode=control-group','-p','TimeoutStopSec=120','python3','-B',str(D/'validate-products.py')]
start=time.time_ns();reason=None
with (E/'validation.stdout').open('wb') as out,(E/'validation.stderr').open('wb') as err:
 p=subprocess.Popen(argv,stdout=out,stderr=err)
 while p.poll() is None:
  free=shutil.disk_usage('/home').free;cg=subprocess.run(['systemctl','--user','show',unit,'-p','ControlGroup','--value'],capture_output=True,text=True).stdout.strip();row={'time_ns':time.time_ns(),'free_bytes':free}
  if cg:
   for n in ['memory.current','memory.peak','memory.events']:
    try:row[n]=(Path('/sys/fs/cgroup')/cg.lstrip('/')/n).read_text()
    except OSError:pass
  with (E/'validation-resources.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
  if free<20*1024**3:
   reason='home available below 20 GiB';subprocess.run(['systemctl','--user','stop',unit]);break
  time.sleep(5)
 rc=p.wait()
fcntl.flock(lock,fcntl.LOCK_UN);lock.close()
(E/'validation-controller.json').write_text(json.dumps({'argv':argv,'start_ns':start,'end_ns':time.time_ns(),'rc':rc,'reason':reason},indent=2)+'\n')
raise SystemExit(rc)
