from pathlib import Path
import subprocess,time,json,datetime,sys
E=Path(__file__).resolve().parent;B=E.parents[5]
# B is passed explicitly to avoid dependence on caller cwd.
runner=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/overnight-20261105/run_service.py')
def now():return datetime.datetime.now().astimezone().isoformat()
status='failed';reason='not-completed'
try:
 while not (E/'train-service/result.json').exists():time.sleep(5)
 r=json.loads((E/'train-service/result.json').read_text());assert r['status']=='ok',r
 for phase in ('merge','optimize','speed'):
  print('START',phase,now(),flush=True)
  p=subprocess.run(['/usr/bin/python3','-B',str(runner),str(E/(phase+'-service')),'pgo-bolt-'+phase+'-20261105','/usr/bin/python3','-B',str(E/'experiment.py'),phase])
  if p.returncode:raise RuntimeError(phase+' failed rc='+str(p.returncode))
 status='ok';reason='completed'
except BaseException as e:
 reason=repr(e)
finally:
 line='PGO_BOLT_FOLLOWUP 已结束 '+now()+' status='+status+' reason='+reason
 (E/'end.txt').write_text(line+'\n');print(line,flush=True)
sys.exit(0 if status=='ok' else 1)
