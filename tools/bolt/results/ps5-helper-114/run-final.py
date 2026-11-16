from pathlib import Path
import os,sys,subprocess,json,re,runpy
E=Path(__file__).parent;T=E/'tests';D=T/'environment';B=E.parents[3]
S='/home/linhao/Toolchain/development/llvm-optimize/temp/ps5-helper-114/source'
inv=json.loads((B/'tools/bolt/results/fifth-review-20261111/rerun3/test-invocation.json').read_text())
# Already completed in this task: policy 46 + release 5. Failed r2 had 0.
rows=[{'suite':'policy','tests':46,'PASS':True,'log':'tests/policy.log'}, {'suite':'release','tests':5,'PASS':True,'log':'tests/release.log'}]
jobs=[('r2',[D/'test_r2.py'],12),('r3-r4-r5',[T/'selected_r3.py'],40),('hardening',[T/'test_hardening.py'],16),('review-r11',[T/'test_review_r11.py'],19),('helper',[T/'helper-suite/run_review_tests.py','--helper',S+'/packaging/clang-bolt-helper.py'],393),('targeted',[T/'test_hq_requests.py'],30),('N1',[T/'test_n1.py'],6),('regression109',[T/'test_109_regressions.py'],45),('sessions110',[T/'test_110_sessions.py'],35),('P1-P2-S2',[E/'test_p1p2.py'],14)]
for label,args,count in jobs:
 runpy.run_path(str(E/'test-admission.py'))['check']()
 env=dict(os.environ,PATH=inv['PATH'],PRODUCT_SOURCE=S,PYTHONDONTWRITEBYTECODE='1',TEST_SCRATCH=str(T/(label+'-114-final-scratch')),TEST_RESULT=str(E/(label+'-result.json')))
 cmd=[sys.executable,'-B',str(D/'run_preserved.py'),*map(str,args)]
 log=E/(label+'-114-final.log')
 with log.open('x') as f:r=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT)
 text=log.read_text();ns=re.findall(r'Ran (\d+) tests?',text);n=int(ns[-1]) if ns else 0
 row={'suite':label,'tests':n,'expected':count,'rc':r.returncode,'PASS':r.returncode==0 and n==count,'log':log.name};rows.append(row)
 (E/'final-results.json').write_text(json.dumps(rows,indent=2)+'\n');print(row,flush=True)
 if not row['PASS']:print(text[-8000:],flush=True);sys.exit(1)
print('PASS total=',sum(x['tests'] for x in rows),flush=True)
