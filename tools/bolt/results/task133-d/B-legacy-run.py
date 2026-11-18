from pathlib import Path
import json,os,re,shutil,subprocess
W=Path('/home/linhao/Toolchain/development/llvm-optimize'); B=W.with_name('llvm-optimize-bolt')
S=W/'temp/task131/pgo-dev'; T=W/'temp/task133-d'; E=B/'tools/bolt/results/task133-d'
O=B/'tools/bolt/results/ps5-helper-126/run2'
D=T/'B-suite'
cfg=json.loads((O/'test-invocation.json').read_text())
results=[]
failures=[]
for label,args,count in cfg['suites']:
    argv=[str(D/'tests/environment/run_preserved.py'),*args]
    if label=='P1-P2-S2':argv[1]=str(D/'test_p1p2.py')
    argv=[p.replace(str(O),str(D)).replace(cfg['product'],str(S)) for p in argv]
    env={**os.environ,'PATH':cfg['PATH'],'PRODUCT_SOURCE':str(S),'PYTHONDONTWRITEBYTECODE':'1',
         'TEST_SCRATCH':str(D/(label+'-scratch')),'TEST_RESULT':str(D/(label+'-result.json')),
         'TEST_DETAILS':str(D/(label+'-details.json'))}
    log=D/(label+'.log')
    with log.open('x') as stream:
        result=subprocess.run(['/usr/bin/python3','-B',*argv],env=env,stdout=stream,stderr=subprocess.STDOUT)
    raw=log.read_text(errors='replace')
    totals=re.findall(r'Ran (\d+) tests?',raw)
    n=int(totals[-1]) if totals else 0
    row={'suite':label,'tests':n,'expected':count,'rc':result.returncode,'pass':n==count and result.returncode==0,'log':str(log)}
    detail=D/(label+'-details.json')
    if detail.exists():
        report=json.loads(detail.read_text())
        for k in ('failures','errors','skipped'):
            for item in report.get(k,[]):failures.append({'suite':label,'kind':k,'detail':item})
    elif not row['pass']:
        failures.append({'suite':label,'kind':'setup','detail':raw[-12000:]})
    results.append(row)
    (E/'B-legacy-results.json').write_text(json.dumps(results,indent=2)+'\n')
    (E/'B-legacy-failures.json').write_text(json.dumps(failures,indent=2)+'\n')
    print(label,n,result.returncode,flush=True)
    if not row['pass']:print(raw[-4000:],flush=True)
print('legacy complete',sum(r['tests'] for r in results),len(failures),flush=True)
raise SystemExit(0 if all(r['pass'] for r in results) else 1)
