import subprocess,os,json,re
from pathlib import Path
E=Path(__file__).resolve().parent;B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');R=B.parent/'llvm-optimize/temp/hq-review-104-20261116'
inv=json.loads((B/'tools/bolt/results/fifth-review-20261111/rerun3/test-invocation.json').read_text())
rows=[]
for label,source in [('hq','361395-ps4'),('candidate','candidate')]:
 T=E/(label+'-tests')
 argv=['python3','-B',str(T/'environment/run_preserved.py'),str(T/'helper-suite/run_review_tests.py'),'--helper',str(R/source/'packaging/clang-bolt-helper.py')]
 env=dict(os.environ,PATH=inv['PATH'],TEST_SCRATCH=str(T/'helper-scratch'),PYTHONDONTWRITEBYTECODE='1')
 with (T/'helper.log').open('x') as f:r=subprocess.run(argv,env=env,stdout=f,stderr=subprocess.STDOUT)
 s=(T/'helper.log').read_text();n=re.findall(r'Ran (\d+) tests?',s)
 row={'label':label,'rc':r.returncode,'tests':int(n[-1]) if n else 0}
 rows.append(row);(E/'helper-results.json').write_text(json.dumps(rows,indent=2))
 print(row,flush=True)
 if r.returncode:print(s[-7000:],flush=True)
