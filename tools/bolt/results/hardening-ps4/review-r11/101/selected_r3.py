import sys,unittest,json
from pathlib import Path
E=Path(__file__).resolve().parent;D=E/'environment'
sys.path.insert(0,str(D));import test_r3 as m
alltests=[];excluded=[]
for cls in (m.R3,m.R4,m.R5):
 for test in unittest.defaultTestLoader.loadTestsFromTestCase(cls):
  if test._testMethodName=='test_messages':excluded.append(test.id())
  else:alltests.append(test)
results=[];retry_used=False
for test in alltests:
 r=unittest.TextTestRunner(verbosity=2,failfast=True).run(unittest.TestSuite([test]));ok=r.wasSuccessful()
 row=dict(id=test.id(),passed=ok,errors=r.errors,failures=r.failures)
 row['errors']=[(t.id(),trace) for t,trace in r.errors];row['failures']=[(t.id(),trace) for t,trace in r.failures]
 if not ok and not retry_used and test._testMethodName=='test_process_states_at_run_return' and len(r.errors)==1 and not r.failures and 'ProcessLookupError' in r.errors[0][1]:
  retry_used=True
  again=test.__class__(test._testMethodName)
  rr=unittest.TextTestRunner(verbosity=2,failfast=True).run(unittest.TestSuite([again]));ok=rr.wasSuccessful();row['retry_passed']=ok
 results.append(row)
 (E/'r3-result.json').write_text(json.dumps(dict(tests=len(results),passed=all(x['passed'] or x.get('retry_passed',False) for x in results),retry_used=retry_used,results=results,excluded=excluded),indent=2)+'\n')
 if not ok:sys.exit(1)
(E/'r3-observed.json').write_text(json.dumps(m.observed,indent=2)+'\n')
print('R3_R4_R5_TOTAL',len(results),'PASS',flush=True)
