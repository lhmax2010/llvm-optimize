from common import *
import fcntl,time,datetime
unit='runpath-verify-quiet-20261027';lock=open('/home/linhao/Toolchain/development/heavy-stage.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX)
assert json.loads((E/'result.json').read_text())['status']=='ok', 'first sequence did not PASS; do not continue'
cap=int(next(l.split()[1] for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemTotal:')))*1024-8*1024**3
argv=['systemd-run','--user','--wait','--pipe','--unit='+unit,'-p','MemoryMax='+str(cap),'-p','MemorySwapMax=0','-p','Nice=10','-p','IOSchedulingClass=best-effort','-p','IOSchedulingPriority=7','-p','OOMPolicy=stop','-p','KillMode=control-group','-p','TimeoutStopSec=30','--setenv=PYTHONDONTWRITEBYTECODE=1','python3','-B',str(E/'quiet_runner.py')]
save(E/'quiet-service-command.json',argv);(E/'quiet-processes-before.txt').write_text(subprocess.check_output(['ps','-eo','pid,pcpu,comm,args','--sort=-pcpu'],text=True));reason=None;status='failed';start=time.time_ns()
try:
 with (E/'quiet-service.stdout').open('wb') as out,(E/'quiet-service.stderr').open('wb') as err:
  p=subprocess.Popen(argv,stdout=out,stderr=err)
  while p.poll() is None:
   row={'process_snapshot':subprocess.check_output(['ps','-eo','pid,ppid,pcpu,stat,comm','--sort=-pcpu'],text=True),'time_ns':time.time_ns(),'free':shutil.disk_usage('/home').free,'loadavg':Path('/proc/loadavg').read_text()}
   cg=subprocess.check_output(['systemctl','--user','show',unit,'-p','ControlGroup','--value'],text=True).strip()
   for n in ['memory.current','memory.peak','memory.events','memory.swap.current']:
    try:row[n]=(Path('/sys/fs/cgroup')/cg.lstrip('/')/n).read_text()
    except OSError:pass
   with (E/'quiet-resources.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
   if row['free']<20*1024**3:reason='home-space-below-20GiB';subprocess.run(['systemctl','--user','stop',unit]);break
   time.sleep(5)
  rc=p.wait()
 status='ok' if rc==0 else 'stopped';reason=reason or (json.loads((E/'quiet-result.json').read_text())['reason'] if (E/'quiet-result.json').exists() else 'service-exit-'+str(rc))
finally:
 fcntl.flock(lock,fcntl.LOCK_UN);lock.close();end=datetime.datetime.now().astimezone().isoformat();save(E/'quiet-controller-result.json',{'status':status,'reason':reason,'start_ns':start,'end':end,'MemoryMax':cap})
 with (E/'quiet-runpath-verify.log').open('a') as f:f.write('RUNPATH_VERIFY FINISHED '+end+' status='+status+' reason='+str(reason)+'\n')
 print(status,reason,flush=True)
