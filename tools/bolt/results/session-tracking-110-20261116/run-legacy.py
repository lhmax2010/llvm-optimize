import os,sys,subprocess,json,re,datetime
from pathlib import Path
E=Path(__file__).parent;T=E/'tests';B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')
S='/home/linhao/Toolchain/development/llvm-optimize/temp/ps5-session-110-20261116/source'
inv=json.loads((B/'tools/bolt/results/fifth-review-20261111/rerun3/test-invocation.json').read_text())
env=dict(os.environ,PATH=inv['PATH'],PRODUCT_SOURCE=S,PYTHONDONTWRITEBYTECODE='1')
rows=[]
jobs=[('legacy-138',[sys.executable,'-B',str(T/'run.py')],138),
('helper',[sys.executable,'-B',str(T/'environment/run_preserved.py'),str(T/'helper-suite/run_review_tests.py'),'--helper',S+'/packaging/clang-bolt-helper.py'],393),
('targeted',[sys.executable,'-B',str(T/'environment/run_preserved.py'),str(T/'test_hq_requests.py')],30),
('N1',[sys.executable,'-B',str(T/'environment/run_preserved.py'),str(T/'test_n1.py')],6)]
for label,argv,count in jobs:
 env.update(TEST_SCRATCH=str(T/(label+'-scratch')),TEST_RESULT=str(T/(label+'-result.json')))
 with (T/(label+'-all.log')).open('x') as f:r=subprocess.run(argv,env=env,stdout=f,stderr=subprocess.STDOUT)
 text=(T/(label+'-all.log')).read_text()
 if label=='legacy-138':
  legacy=json.loads((T/'test-results.json').read_text());n=sum(x['tests'] for x in legacy);ok=r.returncode==0 and all(x['rc']==0 for x in legacy)
 else:
  ns=re.findall(r'Ran (\d+) tests?',text);n=int(ns[-1]) if ns else 0;ok=r.returncode==0
 row=dict(suite=label,rc=r.returncode,count=n,expected=count,PASS=ok and n==count);rows.append(row)
 (E/'test-results.json').write_text(json.dumps(rows,indent=2));print(row,flush=True)
 if not row['PASS']:
  print(text[-9000:],flush=True);sys.exit(1)
print('已结束 '+datetime.datetime.now().astimezone().isoformat()+' tests=PASS total='+str(sum(r['count'] for r in rows)),flush=True)
