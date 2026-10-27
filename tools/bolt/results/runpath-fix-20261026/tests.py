from pathlib import Path
import importlib.util,sys,unittest
D=Path(__file__).resolve().parent;B=D.parents[1].parent/'llvm-optimize-bolt';T=B/'tools/bolt'
sys.path.insert(0,str(T))
spec=importlib.util.spec_from_file_location('bolt_helper',D/'source/packaging/clang-bolt-helper.py');h=importlib.util.module_from_spec(spec);sys.modules['bolt_helper']=h;spec.loader.exec_module(h)
suite=unittest.defaultTestLoader.discover(str(T),pattern='test_*.py')
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(not result.wasSuccessful())
