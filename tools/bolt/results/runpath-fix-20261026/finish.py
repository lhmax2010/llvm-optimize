"""Sequential validation only after the one full build has passed."""
from pathlib import Path
import subprocess,json,time,datetime,traceback,sys
D=Path(__file__).resolve().parent;E=D.parent.parent.parent/'llvm-optimize-bolt/tools/bolt/results/runpath-fix-20261026';steps=[];status='failed';reason='controller exception'
def run(step,args):
 start=time.time_ns()
 with (E/(step+'.stdout')).open('wb') as o,(E/(step+'.stderr')).open('wb') as e:p=subprocess.run(['python3','-B',str(D/args[0]),*args[1:]],stdout=o,stderr=e)
 steps.append({'step':step,'args':args,'rc':p.returncode,'start_ns':start,'end_ns':time.time_ns()});(E/'validation-steps.json').write_text(json.dumps(steps,indent=2))
 assert p.returncode==0,step+' failed; no subsequent steps'
try:
 assert json.loads((E/'controller-result.json').read_text())['rc']==0,'full build failed'
 run('qualification',['qualify.py'])
 run('rpm-comparison',['compare-rpms.py'])
 run('objects-current',['objects.py','current'])
 run('oldtext',['oldtext.py'])
 run('objects-oldtext',['objects.py','oldtext'])
 run('threeway',['measure.py','threeway'])
 run('rss',['measure.py','rss'])
 run('collect',['collect.py'])
 status='ok';reason='all-build-gates-validation-and-measurements-pass'
except BaseException as e:
 reason=str(e);(E/'validation-failure.txt').write_text(traceback.format_exc());raise
finally:
 (E/'validation-result.json').write_text(json.dumps({'status':status,'reason':reason,'steps':steps},indent=2))
 with (E/'runpath-fix.log').open('a') as f:f.write('RUNPATH_FIX FINISHED '+datetime.datetime.now().astimezone().isoformat()+' status='+status+' reason='+reason.replace('\n',' ')+'\n')
