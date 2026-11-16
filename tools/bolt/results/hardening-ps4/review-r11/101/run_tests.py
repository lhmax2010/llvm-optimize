import os,sys,subprocess,json,re,datetime
from pathlib import Path
E=Path(__file__).resolve().parent;D=E/'environment'
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')
inv=json.loads((B/'tools/bolt/results/fifth-review-20261111/rerun3/test-invocation.json').read_text())
results=[]
for label,script,expected in [('policy',D/'test_regressions.py',46),('release',D/'test50.py',5),('r2',D/'test_r2.py',12),('r3-r4-r5',E/'selected_r3.py',40),('hardening',E/'test_hardening.py',16),('review-r11',E/'test_review_r11.py',19)]:
 argv=[sys.executable,'-B',str(D/'run_preserved.py'),str(script)];env=dict(os.environ,PATH=inv['PATH'],TEST_SCRATCH=str(E/(label+'-scratch')),PYTHONDONTWRITEBYTECODE='1')
 with (E/(label+'.log')).open('x') as log:p=subprocess.run(argv,env=env,stdout=log,stderr=subprocess.STDOUT)
 txt=(E/(label+'.log')).read_text();counts=re.findall(r'Ran (\d+) tests?',txt)
 n=json.loads((E/'r3-result.json').read_text())['tests'] if label=='r3-r4-r5' else (int(counts[-1]) if counts else 0)
 row=dict(suite=label,argv=argv,rc=p.returncode,tests=n,expected=expected,status='PASS' if p.returncode==0 and n==expected else 'STOP',time=datetime.datetime.now().astimezone().isoformat());results.append(row)
 (E/'test-results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(row),flush=True)
 if row['status']!='PASS':print(txt[-9000:],flush=True);sys.exit(1)
print('101测试 已结束',datetime.datetime.now().astimezone().isoformat(),'status=PASS',sum(r['tests'] for r in results),flush=True)
