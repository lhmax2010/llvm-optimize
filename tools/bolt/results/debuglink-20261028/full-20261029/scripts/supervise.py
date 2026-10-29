from pathlib import Path
import subprocess,datetime,json,traceback
D=Path(__file__).resolve().parent
E=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/debuglink-20261028/full-20261029')
status='failed';reason='controller-exception'
try:
 r=subprocess.run(['python3','-B',str(D/'run.py')])
 data=json.loads((E/'controller-result.json').read_text()) if (E/'controller-result.json').exists() else {}
 status='ok' if r.returncode==0 and data.get('rc')==0 and not data.get('reason') else 'stopped' if data.get('reason') else 'failed'
 reason=data.get('reason') or ('build-complete-validation-pending' if status=='ok' else 'build-failed')
except BaseException:
 (E/'supervisor-error.txt').write_text(traceback.format_exc())
finally:
 line='DEBUGLINK FINISHED '+datetime.datetime.now().astimezone().isoformat()+' status='+status+' reason='+str(reason).replace(' ','_')+'\n'
 with (E/'debuglink.log').open('a') as f:f.write(line)
 print(line,end='',flush=True)
