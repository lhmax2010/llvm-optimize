from pathlib import Path
import os,subprocess,sys,json,datetime
E=Path(__file__).parent;T=E/'tests';S='/home/linhao/Toolchain/development/llvm-optimize/temp/ps5-session-110-20261116/source'
rows=[]
for label,file in [('regression109','test_109_regressions.py'),('sessions110','test_110_sessions.py')]:
 env=dict(os.environ,PRODUCT_SOURCE=S,PYTHONDONTWRITEBYTECODE='1',TEST_SCRATCH=str(T/(label+'-scratch')),TEST_RESULT=str(E/(label+'-result.json')))
 argv=[sys.executable,'-B',str(T/'environment/run_preserved.py'),str(T/file)]
 (E/(label+'-invocation.json')).write_text(json.dumps({'argv':argv,**{k:env[k] for k in ('PRODUCT_SOURCE','TEST_SCRATCH','TEST_RESULT')}},indent=2))
 with (E/(label+'-output.txt')).open('x') as f:r=subprocess.run(argv,env=env,stdout=f,stderr=subprocess.STDOUT)
 row={'suite':label,'rc':r.returncode}
 if (E/(label+'-result.json')).exists():row.update(json.loads((E/(label+'-result.json')).read_text()))
 rows.append(row);(E/'extra-results.json').write_text(json.dumps(rows,indent=2));print(row,flush=True)
 if r.returncode:
  print((E/(label+'-output.txt')).read_text()[-10000:],flush=True);sys.exit(1)
print('110 新增与回归 已结束 '+datetime.datetime.now().astimezone().isoformat()+' PASS',flush=True)
