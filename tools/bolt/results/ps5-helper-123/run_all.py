from pathlib import Path
import os,sys,subprocess,json,re,datetime,ast,hashlib
E=Path(__file__).parent;T=E/'tests';D=T/'environment';B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');S='/home/linhao/Toolchain/development/llvm-optimize/temp/ps5-helper-122/source'
inv=json.loads((B/'tools/bolt/results/fifth-review-20261111/rerun3/test-invocation.json').read_text())
jobs=[('review122-retained',[T/'test_122.py'],11),('review120',[T/'test_120.py'],2),('review119',[T/'test_119.py'],6),('review118',[T/'test_118.py'],19),('review114',[T/'test_114.py'],34),('policy',[D/'test_regressions.py'],46),('release',[D/'test50.py'],5),('r2',[D/'test_r2.py'],12),('r3-r4-r5',[T/'selected_r3.py'],40),('hardening',[T/'test_hardening.py'],16),('review-r11',[T/'test_review_r11.py'],19),('helper',[T/'helper-suite/run_review_tests.py','--helper',S+'/packaging/clang-bolt-helper.py'],393),('targeted',[T/'test_hq_requests.py'],30),('N1',[T/'test_n1.py'],6),('regression109',[T/'test_109_regressions.py'],45),('sessions110',[T/'test_110_sessions.py'],35),('P1-P2-S2',[E/'test_p1p2.py'],14)]
rows=[]
(E/'test-invocation.json').write_text(json.dumps({'product':S,'PATH':inv['PATH'],'suites':[(a,list(map(str,b)),c) for a,b,c in jobs],'prior_passes_reused':False},indent=2))
for label,args,count in jobs:
 env=dict(os.environ,PATH=inv['PATH'],PRODUCT_SOURCE=S,PYTHONDONTWRITEBYTECODE='1',TEST_SCRATCH=str(T/(label+'-123-scratch')),TEST_RESULT=str(E/(label+'-result.json')))
 cmd=[sys.executable,'-B',str(D/'run_preserved.py'),*map(str,args)]
 log=E/(label+'-123.log')
 with log.open('x') as f:r=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT)
 text=log.read_text();ns=re.findall(r'Ran (\d+) tests?',text);n=int(ns[-1]) if ns else 0
 row={'suite':label,'tests':n,'expected':count,'rc':r.returncode,'PASS':r.returncode==0 and n==count,'log':log.name};rows.append(row)
 (E/'test-results.json').write_text(json.dumps(rows,indent=2)+'\n');print(row,flush=True)
 if not row['PASS']:
  print(text[-10000:],flush=True)
  print('已结束 '+datetime.datetime.now().astimezone().isoformat()+' D tests STOP',flush=True)
  sys.exit(1)
print('已结束 '+datetime.datetime.now().astimezone().isoformat()+' D tests PASS total='+str(sum(x['tests'] for x in rows)),flush=True)
