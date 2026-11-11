from pathlib import Path
import sys,subprocess,unittest,json,signal
E=Path(__file__).resolve().parent
S=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106/source')
observed=[]
class Tests(unittest.TestCase):
 def invoke(self,version,sig):
  helper=E/'old-helper.py' if version=='old' else S/'packaging/clang-bolt-helper.py'
  code="""import importlib.util,os,signal,sys
sp=importlib.util.spec_from_file_location('h',sys.argv[1]);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
def work():
 s=int(sys.argv[2])
 if s:os.kill(os.getpid(),s)
 raise KeyError('unexpected-after-work')
h.main=work
h.diagnose_safely=lambda *a,**kw: print('DIAGNOSE_CALLED',file=sys.stderr)
sys.exit(h.cli())
"""
  r=subprocess.run([sys.executable,'-B','-c',code,str(helper),str(sig)],text=True,capture_output=True,timeout=15)
  observed.append(dict(version=version,signal=sig,argv=[sys.executable,'-B','-c',code,str(helper),str(sig)],returncode=r.returncode,stdout=r.stdout,stderr=r.stderr))
  return r
 def test_recorded_cancel_unexpected_exception(self):
  for sig in [signal.SIGHUP,signal.SIGINT,signal.SIGTERM]:
   with self.subTest(signal=sig):
    old=self.invoke('old',sig);new=self.invoke('new',sig)
    self.assertEqual(old.returncode,1)
    self.assertEqual(new.returncode,128+sig)
    self.assertIn('Traceback (most recent call last):',new.stderr)
    self.assertIn("KeyError: 'unexpected-after-work'",new.stderr)
    self.assertIn('BOLT_GATE_FAILED: unexpected KeyError:',new.stderr)
    self.assertIn('DIAGNOSE_CALLED',new.stderr)
 def test_no_cancel_still_reraises(self):
  old=self.invoke('old',0);new=self.invoke('new',0)
  self.assertEqual(old.returncode,1);self.assertEqual(new.returncode,old.returncode)
  self.assertEqual(new.stdout,old.stdout)
  for text in ['Traceback (most recent call last):',"KeyError: 'unexpected-after-work'",'BOLT_GATE_FAILED: unexpected KeyError:','DIAGNOSE_CALLED']:
   self.assertIn(text,old.stderr);self.assertIn(text,new.stderr)
  # Traceback filenames and line offsets differ; control flow remains a re-raise.
  import ast
  for p in [E/'old-helper.py',S/'packaging/clang-bolt-helper.py']:
   tree=ast.parse(p.read_text());cli=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='cli')
   handler=next(h for n in ast.walk(cli) if isinstance(n,ast.Try) for h in n.handlers if isinstance(h.type,ast.Name) and h.type.id=='Exception')
   self.assertIsInstance(handler.body[-1],ast.Raise)
if __name__=='__main__':
 r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
 (E/'cli-cancel-observed.json').write_text(json.dumps(observed,indent=2)+'\n')
 (E/'cli-cancel-result.json').write_text(json.dumps(dict(tests=r.testsRun,failures=len(r.failures),errors=len(r.errors),PASS=r.wasSuccessful()))+'\n')
 sys.exit(not r.wasSuccessful())
