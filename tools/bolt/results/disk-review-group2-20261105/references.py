import subprocess,json,gzip
from pathlib import Path
E=Path(__file__).resolve().parent
W=Path('/home/linhao/Toolchain/development/llvm-optimize'); B=E.parents[3]
N=json.loads((E/'targets.json').read_text())
# Search docs, all scripts including historical results; skip data/huge generated logs in script pass.
for n in N:
 out=E/n;out.mkdir(exist_ok=True)
 sets=[('main-docs',W/'docs',[]),('bolt-docs',B/'docs',[]),('main-tools',W/'tools',['-g','*.py','-g','*.sh','-g','*.conf','-g','*.json']),('bolt-tools',B/'tools',['-g','*.py','-g','*.sh','-g','*.conf','-g','*.json'])]
 rows=[]
 for label,root,globs in sets:
  argv=['timeout','90','nice','-n','19','ionice','-c3','rg','-n','--no-heading','-F',n,str(root),'--glob','!disk-review-group2-20261105/**']+globs
  try:r=subprocess.run(argv,capture_output=True,text=True,timeout=100)
  except subprocess.TimeoutExpired: rows.append({'label':label,'status':'UNKNOWN timeout'});continue
  lines=[x for x in r.stdout.splitlines() if str(E) not in x]
  # JSON inventories may have long lines; retain full output in gzip.
  with gzip.open(out/(label+'-references.txt.gz'),'wt') as f:f.write('\n'.join(lines)+'\n')
  rows.append({'label':label,'argv':argv,'rc':r.returncode,'lines':len(lines),'stderr':r.stderr})
 (out/'references.json').write_text(json.dumps(rows,indent=2)+'\n')
 print(n,[(x['label'],x.get('lines')) for x in rows],flush=True)
