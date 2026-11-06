import ast,hashlib,json,unittest
from pathlib import Path
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';E=Path(__file__).resolve().parent
FILES=[B/'tools/bolt/night-launch-20261105/validation_common.py',B/'tools/bolt/night-launch-20261103/validate.py']
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def statements(p):
 fn=next(x for x in ast.parse(p.read_text()).body if isinstance(x,ast.FunctionDef) and x.name=='objects')
 load=next(x for x in fn.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='units' for t in x.targets))
 guard=next(x for x in ast.walk(fn) if isinstance(x,ast.Assert) and "u['copy']" in ast.unparse(x.test))
 return load,guard
class Restored(unittest.TestCase):
 def test_actual_entry_manifest(self):
  expected=json.loads((E/'original-tu-inputs.json').read_text())
  for p in FILES:
   load,_=statements(p);ns={'W':W,'json':json};exec(compile(ast.Module(body=[load],type_ignores=[]),str(p),'exec'),ns);actual=ns['units']
   self.assertEqual(len(actual),90)
   for x,y in zip(expected,actual):
    for k in ['index','key','target','sha256','bytes','original_argv','provenance']:self.assertEqual(x[k],y[k])
    self.assertEqual(Path(y['copy']).parent,W/'temp/tu-inputs-restored-20261106')
 def test_all_90_file_sha(self):
  a=json.loads((W/'temp/tu-inputs-restored-20261106/tu-inputs.json').read_text())
  for u in a:self.assertEqual(sha(u['copy']),u['sha256'])
 def test_actual_guard_rejects_changed_bytes(self):
  d=E/'guard-fixture';d.mkdir(exist_ok=True);good=d/'good.ii';bad=d/'bad.ii';good.write_bytes(b'int x;\n');bad.write_bytes(b'int y;\n')
  for p in FILES:
   _,guard=statements(p);c=compile(ast.Module(body=[guard],type_ignores=[]),str(p),'exec')
   exec(c,{'sha':sha,'u':{'copy':str(good),'sha256':sha(good)}})
   with self.assertRaises(AssertionError):exec(c,{'sha':sha,'u':{'copy':str(bad),'sha256':sha(good)}})
 def test_no_old_manifest_in_active_entries(self):
  for p in FILES:self.assertNotIn('docs/53_hybrid_local_validation_evidence/tu-inputs.json',p.read_text())
if __name__=='__main__':unittest.main(verbosity=2)
