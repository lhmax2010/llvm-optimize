from pathlib import Path
import importlib.util,sys,unittest
D=Path(__file__).resolve().parent;B=D.parents[1].parent/'llvm-optimize-bolt';T=B/'tools/bolt'
sys.path.insert(0,str(T))
spec=importlib.util.spec_from_file_location('bolt_helper',D/'source/packaging/clang-bolt-helper.py');h=importlib.util.module_from_spec(spec);sys.modules['bolt_helper']=h;spec.loader.exec_module(h)
suite=unittest.defaultTestLoader.discover(str(T),pattern='test_*.py')
class OldTextOptions(unittest.TestCase):
    def test_only_append_old_text(self):
        import ast,subprocess
        old=ast.parse(subprocess.check_output(['git','-C',str(D/'source'),'show','ac112ebfd6e7983bdfd4c38dd156e6baba72731b:packaging/clang-bolt-helper.py'],text=True))
        node=next(n for n in old.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='OPTIONS')
        self.assertEqual(h.OPTIONS,ast.literal_eval(node.value)+['-use-old-text'])
suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(OldTextOptions))
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(not result.wasSuccessful())
