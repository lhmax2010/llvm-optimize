from common import *
import time,datetime,traceback
steps=[];status='failed';reason='unexpected runner exception'
try:
 for step,args in [('preflight',['preflight.py']),('rpm23',['compare.py']),('elf',['elf_compare.py']),('objects-current',['objects.py','current']),('oldtext',['oldtext.py']),('objects-oldtext',['objects.py','oldtext']),('threeway',['measure.py','threeway']),('rss',['measure.py','rss']),('native-audit',['native_audit.py'])]:
  free();start=time.time_ns()
  with (E/(step+'.stdout')).open('wb') as out,(E/(step+'.stderr')).open('wb') as err:p=subprocess.run(['python3','-B',str(E/args[0]),*args[1:]],stdout=out,stderr=err)
  steps.append({'step':step,'rc':p.returncode,'start_ns':start,'end_ns':time.time_ns()});save(E/'steps.json',steps)
  if p.returncode:status='stopped';reason=step+'-failed';raise RuntimeError(reason)
 status='ok';reason='all-requested-checks-and-measurements-pass'
except BaseException:
 (E/'failure.txt').write_text(traceback.format_exc())
finally:
 save(E/'result.json',{'status':status,'reason':reason,'steps':steps})
 print('RUNPATH_VERIFY FINISHED '+datetime.datetime.now().astimezone().isoformat()+' status='+status+' reason='+reason,flush=True)
 if status!='ok':raise SystemExit(1)
