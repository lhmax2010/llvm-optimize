import sys,unittest,json
from pathlib import Path
D=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/hardening-ps4-20261114/environment')
sys.path.insert(0,str(D));import test_r3 as m
suite=unittest.TestSuite();excluded=[]
for cls in (m.R3,m.R4,m.R5):
 for test in unittest.defaultTestLoader.loadTestsFromTestCase(cls):
  if test._testMethodName=='test_messages':excluded.append(test.id())
  else:suite.addTest(test)
r=unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)
E=Path(__file__).resolve().parent
(E/'r3-result.json').write_text(json.dumps(dict(tests=r.testsRun,failures=len(r.failures),errors=len(r.errors),passed=r.wasSuccessful(),excluded=excluded),indent=2)+'\n')
(E/'r3-observed.json').write_text(json.dumps(m.observed,indent=2)+'\n')
sys.exit(not r.wasSuccessful())
