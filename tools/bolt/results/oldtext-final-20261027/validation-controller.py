from pathlib import Path
import fcntl,json,subprocess,time,datetime,shutil,traceback
D=Path(__file__).resolve().parent;W=D.parent.parent;E=W.parent/'llvm-optimize-bolt/tools/bolt/results/oldtext-final-20261027';plan=json.loads((D/'plan.json').read_text());unit='oldtext-final-validation-20261027';status='failed';reason='controller-unexpected';rc=1
lock=open('/home/linhao/Toolchain/development/heavy-stage.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX)
try:
 # The build controller writes its result immediately after releasing the lock.
 while not (E/'controller-result.json').exists():time.sleep(.2)
 build=json.loads((E/'controller-result.json').read_text());assert build['rc']==0 and build['reason'] is None,'build-stopped-or-failed'
 assert json.loads((E/'build-result.json').read_text())['exit_code']==0,'build-failed'
 argv=['systemd-run','--user','--wait','--pipe','--unit='+unit,'-p','MemoryMax='+str(plan['MemoryMax_bytes']),'-p','MemorySwapMax=0','-p','Nice=10','-p','IOSchedulingClass=best-effort','-p','IOSchedulingPriority=7','-p','OOMPolicy=stop','-p','KillMode=control-group','-p','TimeoutStopSec=120','--setenv=PYTHONDONTWRITEBYTECODE=1','python3','-B',str(D/'validate-runner.py')]
 (E/'validation-service-command.json').write_text(json.dumps(argv,indent=2)+'\n')
 with (E/'validation-service.stdout').open('wb') as o,(E/'validation-service.stderr').open('wb') as e:
  p=subprocess.Popen(argv,stdout=o,stderr=e)
  while p.poll() is None:
   row={'time_ns':time.time_ns(),'free_bytes':shutil.disk_usage('/home').free,'loadavg':Path('/proc/loadavg').read_text()};cg=subprocess.check_output(['systemctl','--user','show',unit,'-p','ControlGroup','--value'],text=True).strip()
   if cg:
    for n in ('memory.current','memory.peak','memory.events','memory.swap.current'):
     try:row[n]=(Path('/sys/fs/cgroup')/cg.lstrip('/')/n).read_text()
     except OSError:pass
   with (E/'validation-resources.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
   if row['free_bytes']<20*1024**3:
    reason='home-below-20GiB';subprocess.run(['systemctl','--user','stop',unit]);break
   time.sleep(2)
  rc=p.wait()
 result=json.loads((E/'validation-result.json').read_text()) if (E/'validation-result.json').exists() else {}
 status='ok' if rc==0 and result.get('status')=='ok' else 'stopped';reason=result.get('reason',reason if reason=='home-below-20GiB' else 'validation-service-failed')
except BaseException as error:
 status='stopped';reason=str(error).replace(' ','-');(E/'validation-controller-failure.txt').write_text(traceback.format_exc())
finally:
 fcntl.flock(lock,fcntl.LOCK_UN);lock.close();end=datetime.datetime.now().astimezone().isoformat()
 (E/'validation-controller-result.json').write_text(json.dumps({'status':status,'reason':reason,'rc':rc,'end':end},indent=2)+'\n')
 with (E/'oldtext-final.log').open('a') as f:f.write('OLDTEXT_FINAL FINISHED '+end+' status='+status+' reason='+reason+'\n')
print(status,reason,flush=True)
