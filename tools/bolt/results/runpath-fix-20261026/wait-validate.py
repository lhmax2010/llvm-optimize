from pathlib import Path
import time,json,subprocess,fcntl,datetime,sys,traceback
D=Path(__file__).resolve().parent;E=D.parent.parent.parent/'llvm-optimize-bolt/tools/bolt/results/runpath-fix-20261026';result=E/'controller-result.json';plan=json.loads((D/'plan.json').read_text());status='failed';reason='validation launcher exception'
try:
 while not result.exists():time.sleep(5)
 build=json.loads(result.read_text())
 if build['rc']!=0 or build.get('reason'):
  status='stopped';reason='full-build-not-pass; validation and measurements NOT RUN'
 else:
  lock=open('/home/linhao/Toolchain/development/heavy-stage.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX)
  argv=['systemd-run','--user','--wait','--pipe','--unit=runpath-fix-validation-resume-20261026','-p','MemoryMax='+str(plan['MemoryMax_bytes']),'-p','MemorySwapMax=0','-p','Nice=10','-p','IOSchedulingClass=best-effort','-p','IOSchedulingPriority=7','-p','OOMPolicy=stop','-p','KillMode=control-group','-p','TimeoutStopSec=120','--setenv=PYTHONDONTWRITEBYTECODE=1','python3','-B',str(D/'finish.py')]
  (E/'validation-service-command.json').write_text(json.dumps(argv,indent=2))
  with (E/'validation-service.stdout').open('wb') as out,(E/'validation-service.stderr').open('wb') as err:p=subprocess.run(argv,stdout=out,stderr=err)
  fcntl.flock(lock,fcntl.LOCK_UN);lock.close()
  status='ok' if p.returncode==0 else 'failed';reason='validation-service-exit-'+str(p.returncode)
  (E/'validation-service-result.json').write_text(json.dumps({'rc':p.returncode,'status':status},indent=2))
except BaseException as e:
 reason=str(e);(E/'validation-launch-failure.txt').write_text(traceback.format_exc());raise
finally:
 (E/'task-result.json').write_text(json.dumps({'status':status,'reason':reason,'time':datetime.datetime.now().astimezone().isoformat()},indent=2))
 with (E/'runpath-fix.log').open('a') as f:f.write('RUNPATH_FIX FINISHED '+datetime.datetime.now().astimezone().isoformat()+' status='+status+' reason='+reason+'\n')
 print('RUNPATH_FIX',status,reason,flush=True)
