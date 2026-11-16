import os,sys,subprocess,json,re,datetime
from pathlib import Path
E=Path(__file__).resolve().parent;D=E/'environment'
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')
inv=json.loads((B/'tools/bolt/results/fifth-review-20261111/rerun3/test-invocation.json').read_text())
rows=[]
for label,file,n in [('policy',D/'test_regressions.py',46),('release',D/'test50.py',5),('r2',D/'test_r2.py',12),('r3-r4-r5',E/'selected_r3.py',40),('hardening',E/'test_hardening.py',16),('review-r11',E/'test_review_r11.py',19)]:
 env=dict(os.environ,PATH=inv['PATH'],TEST_SCRATCH=str(E/(label+'-scratch')),PYTHONDONTWRITEBYTECODE='1')
 with (E/(label+'.log')).open('x') as log:
  p=subprocess.run([sys.executable,'-B',str(D/'run_preserved.py'),str(file)],stdout=log,stderr=subprocess.STDOUT,env=env)
 txt=(E/(label+'.log')).read_text();counts=re.findall(r'Ran (\d+) tests?',txt)
 row=dict(suite=label,rc=p.returncode,tests=int(counts[-1]) if counts else 0,expected=n)
 rows.append(row);(E/'test-results.json').write_text(json.dumps(rows,indent=2))
 print(row,flush=True)
 if p.returncode:print(txt[-5000:],flush=True);sys.exit(1)
