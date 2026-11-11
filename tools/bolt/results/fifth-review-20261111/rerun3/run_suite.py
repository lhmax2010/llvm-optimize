from pathlib import Path
import sys,os,subprocess,json,datetime
E=Path(__file__).parent
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
X=W/'temp/fifth-review-20261111/rerun3';D=X/'environment'
inv=json.loads((E/'test-invocation.json').read_text())
name=sys.argv[1]
tests={'helper':['helper-suite/run_review_tests.py','--helper',str(W/'temp/rebase-359934-20261106/source/packaging/clang-bolt-helper.py')],'policy':['test_regressions.py'],'release':['test50.py'],'r2':['test_r2.py'],'cli':['test_cli_cancel.py'],'r3-r4-r5':['test_r3.py']}
args=tests[name];argv=[sys.executable,'-B',str(D/'run_preserved.py'),str(D/args[0]),*args[1:]]
environment=dict(os.environ,PATH=inv['PATH'],TEST_SCRATCH=str(X/(name+'-tests')))
with (E/(name+'-tests.log')).open('x') as log:
 result=subprocess.run(argv,env=environment,stdout=log,stderr=subprocess.STDOUT)
(E/(name+'-invocation.json')).write_text(json.dumps(dict(argv=argv,PATH=inv['PATH'],TEST_SCRATCH=environment['TEST_SCRATCH'],rc=result.returncode),indent=2)+'\n')
text=(E/(name+'-tests.log')).read_text()
print(text[-4000:])
sys.exit(result.returncode)
