import os,sys,subprocess,json,re,datetime
from pathlib import Path
E=Path(__file__).resolve().parent;X=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/hardening-ps4-20261114');D=X/'environment'
inv=json.loads((E.parents[1]/'fifth-review-20261111/rerun3/test-invocation.json').read_text()) if False else json.loads(Path('/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/fifth-review-20261111/rerun3/test-invocation.json').read_text())
results=[]
for label,script in [('policy',D/'test_regressions.py'),('release',D/'test50.py'),('r2',D/'test_r2.py'),('r3-r4-r5',E/'selected_r3.py')]:
 argv=[sys.executable,'-B',str(D/'run_preserved.py'),str(script)];env=dict(os.environ,PATH=inv['PATH'],TEST_SCRATCH=str(X/(label+'-tests')))
 with (E/(label+'.log')).open('x') as log:p=subprocess.run(argv,env=env,stdout=log,stderr=subprocess.STDOUT)
 text=(E/(label+'.log')).read_text();counts=re.findall(r'Ran (\d+) tests?',text)
 row=dict(suite=label,argv=argv,rc=p.returncode,tests=int(counts[-1]) if counts else None,status='PASS' if p.returncode==0 else 'STOP',time=datetime.datetime.now().astimezone().isoformat());results.append(row)
 (E/'existing-tests.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(row),flush=True)
 if p.returncode:print(text[-6500:],flush=True);sys.exit(p.returncode)
print('96既有测试 已结束',datetime.datetime.now().astimezone().isoformat(),'status=PASS',sum(r['tests'] for r in results),flush=True)
