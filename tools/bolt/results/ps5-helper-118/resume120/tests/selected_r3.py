import os,sys,json,unittest,importlib.util
from pathlib import Path
E=Path(__file__).resolve().parent;D=E/'environment'
sys.path.insert(0,str(D))
import test_r3 as m
tests=[t for c in (m.R3,m.R4,m.R5) for t in unittest.defaultTestLoader.loadTestsFromTestCase(c) if t._testMethodName!='test_messages']
r=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(tests))
(E/'r3-result.json').write_text(json.dumps(dict(tests=r.testsRun,failures=len(r.failures),errors=len(r.errors)),indent=2))
sys.exit(not r.wasSuccessful())
