import fcntl,json,shutil,subprocess,time
from pathlib import Path
from validate import D,E,save
assert json.loads((E/'build-result.json').read_text())['exit_code']==0
while not (E/'verification-controller-result.json').exists():time.sleep(5)
plan=json.loads((D/'plan.json').read_text());unit='hybrid-followup-20261023.service'
argv=['systemd-run','--user','--wait','--pipe','--unit='+unit,'-p','MemoryMax='+str(plan['MemoryMax_bytes']),'-p','MemorySwapMax=0','-p','Nice=10','-p','IOSchedulingClass=best-effort','-p','IOSchedulingPriority=7','-p','OOMPolicy=stop','-p','KillMode=control-group','-p','TimeoutStopSec=120','--setenv=PYTHONDONTWRITEBYTECODE=1','python3','-B',str(D/'followup-batch.py')]
save('followup-controller-service-command.json',argv)
lock=open('/home/linhao/Toolchain/development/heavy-stage.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX);start=time.time_ns();reason=None
try:
 with (E/'followup-controller-service.stdout').open('wb') as out,(E/'followup-controller-service.stderr').open('wb') as err:
  p=subprocess.Popen(argv,stdout=out,stderr=err)
  while p.poll() is None:
   free=shutil.disk_usage('/home').free
   r=subprocess.run(['systemctl','--user','show',unit,'--property=ControlGroup','--value'],capture_output=True,text=True);cg=r.stdout.strip();row={'time_ns':time.time_ns(),'home_available_bytes':free,'cgroup':cg}
   if cg:
    for n in ('memory.current','memory.peak','memory.events'):
     try:row[n]=(Path('/sys/fs/cgroup')/cg.lstrip('/')/n).read_text()
     except OSError as exc:row[n]=str(exc)
   with (E/'followup-controller-resources.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
   if free<20*1024**3 and reason is None:
    reason='home available below 20 GiB';save('followup-controller-disk-stop.json',row);subprocess.run(['systemctl','--user','stop',unit],capture_output=True,text=True)
   time.sleep(2)
  rc=p.returncode
finally:fcntl.flock(lock,fcntl.LOCK_UN);lock.close()
save('followup-controller-controller-result.json',{'rc':rc,'reason':reason,'start_ns':start,'end_ns':time.time_ns()})
print('VERIFICATION_EXIT',rc,'reason',reason,flush=True)
