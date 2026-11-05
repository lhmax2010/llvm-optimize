import os,json,hashlib,subprocess,gzip
from pathlib import Path
E=Path(__file__).resolve().parent;B=E.parents[3];W=Path('/home/linhao/Toolchain/development/llvm-optimize')
# Compare key small local records against tracked evidence, retaining local-only items explicitly.
tracked={}
for repo in [B,W]:
 r=subprocess.run(['git','-C',str(repo),'ls-files','-z','docs','tools'],capture_output=True)
 for rel in r.stdout.decode().split('\0'):
  if not rel:continue
  p=repo/rel
  try:
   st=p.stat()
   if st.st_size<=2*1024*1024:tracked.setdefault((p.name,st.st_size),[]).append(p)
  except OSError:pass
cache={}
def sha(p):
 s=p.stat();k=(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns)
 if k not in cache:
  r=subprocess.run(['timeout','30','nice','-n','19','ionice','-c3','sha256sum','--',str(p)],capture_output=True,text=True);cache[k]=r.stdout.split()[0] if r.returncode==0 else None
 return cache[k]
for n in json.loads((E/'targets.json').read_text()):
 inv=json.loads((E/n/'inventory.json').read_text());rows=[]
 for x in inv['top']:
  p=Path(x['path'])
  if 'du' in x or x['mode'][0]!='-' or x['size']>2*1024*1024:continue
  if p.suffix not in ('.json','.jsonl','.txt','.log','.py','.sh','.md','.conf','.patch','.diff'):continue
  h=sha(p);same=[str(q) for q in tracked.get((p.name,x['size']),[]) if h and sha(q)==h]
  rows.append({'path':str(p),'bytes':x['size'],'sha256':h,'tracked_same_name_same_sha':same,'status':'tracked duplicate' if same else 'not proven archived; keep local'})
 (E/n/'small-evidence.json').write_text(json.dumps(rows,indent=2))
 print(n,len(rows),sum(bool(x['tracked_same_name_same_sha']) for x in rows),flush=True)
