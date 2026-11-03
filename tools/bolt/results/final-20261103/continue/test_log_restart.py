from pathlib import Path
import ast,json,re,shutil,time
from unittest import mock
E=Path(__file__).parent
source=E/'launcher-syntax-probe/run.py'
node=next(n for n in ast.parse(source.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='logs')
root=E/'log-restart-fixture';root.mkdir();out=root/'evidence';out.mkdir()
old=b'PREP ONLY\n'*100
new=b'NEW LOG\n'*140+b'Executing(%prep)\nExecuting(%build)\n+ cmake -G Ninja ../llvm\n'
class Stop:
 def __init__(self):self.n=0
 def wait(self,seconds):
  self.n+=1
  if self.n>2:raise AssertionError('monitor did not stop')
  (root/'.build.log').write_bytes(old if self.n==1 else new)
  return False
rows=[]
sub=mock.Mock();sub.run.return_value=mock.Mock(returncode=0,stdout='',stderr='')
g={'R':root,'E':out,'plan':{'mode':'rehearsal'},'unit':'fixture-only.service','stop':Stop(),'reason':None,'re':re,'shutil':shutil,'time':time,'subprocess':sub,'append':lambda name,row:rows.append((name,row))}
exec(compile(ast.Module(body=[node],type_ignores=[]),str(source),'exec'),g)
g['logs']()
assert (out/'rpm-build-final.log').read_bytes()==new
assert g['reason']=='rehearsal-CMake-start'
assert sum(name=='log-restarts.jsonl' for name,_ in rows)==1
sub.run.assert_called_once_with(['systemctl','--user','stop','fixture-only.service'],capture_output=True,text=True)
(E/'log-restart-fixture.json').write_text(json.dumps({'PASS':True,'old_bytes':len(old),'new_bytes':len(new),'restart_events':rows,'subprocess':'mock only, no service executed'},indent=2)+'\n')
print('LOG_TRUNCATE_AND_REGROW_FIXTURE_PASS')
