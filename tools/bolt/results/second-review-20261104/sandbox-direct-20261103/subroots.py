from pathlib import Path
import subprocess,time,json
E=Path(__file__).parent;assets=json.loads((E/'local-assets-shallow.json').read_text());rows=[]
for a in assets:
 if Path(a['path']).name not in ('final-20261103','second-review-20261104'):continue
 for m in a['markers']:
  if m['kind']!='gbs-root':continue
  path=m['path'];cmd=['nice','-n','19','ionice','-c3','du','-sx','-B1','--time','--time-style=full-iso',path];start=time.monotonic()
  try:
   p=subprocess.run(cmd,capture_output=True,text=True,timeout=30);rc=p.returncode;out=p.stdout;err=p.stderr
  except subprocess.TimeoutExpired as x:rc=124;out=(x.stdout or b'').decode(errors='replace');err=(x.stderr or b'').decode(errors='replace')
  n=int(out.split()[0]) if out.strip() and rc!=124 else None
  row={'path':path,'argv':cmd,'rc':rc,'stdout':out,'stderr':err,'bytes':n,'seconds':time.monotonic()-start,'status':'UNKNOWN' if n is None else 'lower-bound' if rc else 'OK'};rows.append(row)
  (E/'rebuildable-subroots.json').write_text(json.dumps(rows,indent=2)+'\n');print(path,n,flush=True)
