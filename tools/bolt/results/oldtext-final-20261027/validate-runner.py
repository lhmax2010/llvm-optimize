from pathlib import Path
import json,subprocess,time,traceback,datetime,sys,hashlib,os
from external_load import Observer
D=Path(__file__).resolve().parent;W=D.parent.parent;E=W.parent/'llvm-optimize-bolt/tools/bolt/results/oldtext-final-20261027';V=E/'validation';steps=[];status='failed';reason='unexpected-validation-error'
def step(name,argv):
 start=time.time_ns()
 with (E/(name+'.stdout')).open('wb') as o,(E/(name+'.stderr')).open('wb') as e:r=subprocess.run(argv,stdout=o,stderr=e)
 steps.append({'step':name,'argv':argv,'rc':r.returncode,'start_ns':start,'end_ns':time.time_ns()});(E/'validation-steps.json').write_text(json.dumps(steps,indent=2)+'\n')
 if r.returncode:raise RuntimeError(name+'-failed')
try:
 assert json.loads((E/'controller-result.json').read_text())['rc']==0
 assert json.loads((E/'build-result.json').read_text())['exit_code']==0
 step('qualification',['python3','-B',str(D/'qualify.py')])
 step('collect',['python3','-B',str(D/'collect.py')])
 step('rpm23',['python3','-B',str(V/'compare.py')])
 clang=json.loads((V/'rpm-comparison/clang-22.1.8-1.x86_64.rpm.json').read_text())['new_files']['usr/bin/clang-22']['sha256'];q=json.loads((E/'qualification.json').read_text());assert clang==q['candidate_sha256']
 (V/'installed-rpm-identity.json').write_text(json.dumps({'PASS':True,'candidate_and_rpm_sha256':clang},indent=2)+'\n')
 step('elf',['python3','-B',str(V/'elf_compare.py')])
 step('objects-current',['python3','-B',str(V/'objects.py'),'current'])
 # Performance starts only after these correctness and package gates pass.
 observer=Observer(E/'external-load.jsonl');attempts=[]
 try:
  for attempt in range(1000000):
   observer.quiet();label='rss' if attempt==0 else 'rss-repeat-'+str(attempt);os.environ['MEASUREMENT_LABEL']=label
   begin=time.time_ns();step(label,['python3','-B',str(V/'measure.py'),'rss']);end=time.time_ns();interference=observer.overlapping(begin,end)
   attempts.append({'label':label,'start_ns':begin,'end_ns':end,'interference':interference,'accepted':not interference})
   (E/'rss-attempts.json').write_text(json.dumps(attempts,indent=2)+'\n')
   if not interference:
    (E/'rss-accepted.json').write_text(json.dumps({'label':label,'method':'5 complete rounds; repeat the whole five-round batch if sustained external load overlaps; retain every original sample','cpu_threshold_cores':.5,'io_threshold_Bps':32*1024**2,'sustained_seconds':10,'quiet_seconds':12},indent=2)+'\n');break
  else:raise RuntimeError('no-quiet-RSS-run')
 finally:observer.close()
 status='ok';reason='build-package-identity-objects-rss-complete'
except BaseException as ex:
 status='stopped';reason=str(ex).replace(' ','-');(E/'validation-failure.txt').write_text(traceback.format_exc())
finally:
 (E/'validation-result.json').write_text(json.dumps({'status':status,'reason':reason,'steps':steps},indent=2)+'\n')
 print('OLDTEXT_FINAL FINISHED '+datetime.datetime.now().astimezone().isoformat()+' status='+status+' reason='+reason,flush=True)
sys.exit(0 if status=='ok' else 1)
