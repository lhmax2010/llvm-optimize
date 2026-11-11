"""Serial night coordinator. No full/night invocation is part of daytime prep."""
from pathlib import Path
import os,sys,json,time,subprocess,datetime,traceback
import launcher as L
from resource_report import critical_stop
N=L.W/'temp/night-20261103'

def ended(status,reason):
 print('NIGHT 已结束',datetime.datetime.now().astimezone().isoformat(),'status='+status,'reason='+reason,flush=True)

def run():
 status='failed';reason='unexpected-coordinator-error';results=[]
 try:
  L.check_source()
  for project in ('toolchain','basedev'):
   assert not (N/project).exists(),'fresh root required: '+str(N/project)
  for project in ('toolchain','basedev'):
   env=dict(os.environ,FINAL_PROJECT=project)
   p=subprocess.run([sys.executable,'-B',str(L.T/'launcher.py'),'full'],env=env,capture_output=True,text=True)
   print(p.stdout,p.stderr,flush=True)
   D=N/project;unit='night-'+project+'-full-controller-20261103.service'
   if p.returncode:raise RuntimeError('launch-failed '+project)
   heartbeat=0
   while True:
    state=subprocess.check_output(['systemctl','--user','show',unit,'-p','ActiveState','--value'],text=True).strip()
    if state in ('inactive','failed'):break
    if time.monotonic()-heartbeat>=60:
     heartbeat=time.monotonic();log=D/'evidence/rpm-build.log';tail=''
     if log.exists():
      with log.open('rb') as f:f.seek(max(0,log.stat().st_size-4096));tail=f.read().decode(errors='replace').splitlines()[-1:]
     print('NIGHT_PROGRESS',datetime.datetime.now().astimezone().isoformat(),project,'service='+state,'tail='+repr(tail),flush=True)
    time.sleep(5)
   result=L.json.loads((D/'evidence/result.json').read_text()) if (D/'evidence/result.json').exists() else {'status':'failed','reason':'controller-ended-without-result'}
   service=subprocess.check_output(['systemctl','--user','show',unit,'-p','Result'],text=True)
   if 'oom-kill' in service:result={'status':'stopped','reason':'memory-oom-stop'}
   print('NIGHT_PROJECT 已结束',datetime.datetime.now().astimezone().isoformat(),project,result,flush=True)
   results.append(dict(project=project,**result));L.save(N/'night-progress.json',results)
   critical=critical_stop(D,L.json.loads((D/'evidence/final-audit.json').read_text()) if (D/'evidence/final-audit.json').exists() else None)
   if critical or result['status']=='stopped' or not (D/'evidence/final-audit.json').exists():
    reason=critical or result['reason'];status='stopped';break
  else:
   status='ok' if all(r['status']=='ok' for r in results) else 'failed';reason='serial-builds-and-validation-finished'
 except BaseException:
  reason='coordinator-error-see-log';traceback.print_exc()
 finally:
  try:L.save(N/'night-result.json',dict(status=status,reason=reason,projects=results,time=datetime.datetime.now().astimezone().isoformat()))
  finally:ended(status,reason)
 return 0 if status=='ok' else 1

if __name__=='__main__':
 if sys.argv[1:]==['--worker']:sys.exit(run())
 assert not sys.argv[1:]
 L.check_source()
 for name in ['toolchain','basedev','night-result.json','night-progress.json','night.log']:
  assert not (N/name).exists(),'existing night output refused: '+name
 mem=int(next(l.split()[1] for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemTotal:')))*1024
 argv=['systemd-run','--user','--unit=llvm-night-20261103.service',*L.properties({'MemoryMax_bytes':mem-8*1024**3}),'-p','StandardOutput=append:'+str(N/'night.log'),'-p','StandardError=append:'+str(N/'night.log'),'--setenv=NIGHT_SOURCE_SHA='+L.COMMIT,sys.executable,'-B',str(Path(__file__).resolve()),'--worker']
 L.save(N/'night-command.json',argv);subprocess.run(argv,check=True)
 print('Night controller started; T then D, never parallel')
 print('tail -f '+str(N/'night.log'))
