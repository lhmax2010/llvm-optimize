from pathlib import Path
import subprocess,hashlib,json,urllib.request,time,concurrent.futures
E=Path(__file__).resolve().parent;B=E.parents[2]/'llvm-optimize-bolt';pin=subprocess.check_output(['git','rev-parse','HEAD'],cwd=B,text=True).strip();old='478e3cde392dfa666975a635e2157f991fbd5916';paths=subprocess.check_output(['git','diff','--name-only',old,pin],cwd=B,text=True).splitlines();rows=[];base='https://raw.githubusercontent.com/lhmax2010/llvm-optimize/'
for f in paths:
 p=B/f;rows.append({'path':f,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'branch':base+'bolt-v4/'+f,'pinned':base+pin+'/'+f})
def check(task):
 row,kind=task;url=row[kind]
 for attempt in range(3):
  try:
   with urllib.request.urlopen(url,timeout=30) as response:data=response.read()
   return {'url':url,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'PASS':len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']}
  except Exception as error:
   if attempt==2:return {'url':url,'PASS':False,'error':str(error)}
   time.sleep(1)
t=time.monotonic()
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:checks=list(pool.map(check,[(r,k) for r in rows for k in ['branch','pinned']]))
v={'pin':pin,'files':rows,'URLs':len(checks),'PASS':all(x['PASS'] for x in checks),'seconds':time.monotonic()-t,'results':checks};(E/'closing-verification.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps({k:v[k] for k in ['pin','URLs','PASS','seconds']}));assert v['PASS']
