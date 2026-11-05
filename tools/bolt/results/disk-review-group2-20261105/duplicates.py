import os,time,json,subprocess,stat
from pathlib import Path
E=Path(__file__).resolve().parent; W=Path('/home/linhao/Toolchain/development/llvm-optimize');N=json.loads((E/'targets.json').read_text())
index={};errors=[];start=time.monotonic();wanted={'merge-fdata','libbolt_rt_instr.a','perf2bolt','llvm-bolt','clang-22','clang-22.debug'}
for base,ds,fs in os.walk(W/'temp',followlinks=False,onerror=lambda x:errors.append(str(x))):
 if time.monotonic()-start>480:errors.append('metadata index timeout 480s UNKNOWN');break
 ds[:]=[x for x in ds if x not in ('.git','proc','sys','dev')]
 for n in fs:
  if not (n.endswith(('.rpm','.fdata','.profraw','.profdata','.fdata.xz')) or n in wanted):continue
  p=Path(base)/n
  try:
   s=p.lstat()
   if stat.S_ISREG(s.st_mode):index.setdefault(str(s.st_size),[]).append({'path':str(p),'size':s.st_size,'dev':s.st_dev,'ino':s.st_ino,'mtime_ns':s.st_mtime_ns})
  except OSError as x:errors.append(str(x))
(E/'duplicate-candidate-index.json').write_text(json.dumps({'seconds':time.monotonic()-start,'errors':errors,'by_size':index},indent=2))
print('index ready',sum(map(len,index.values())),'errors',len(errors),flush=True)
cache={}
def sha(p):
 try:s=os.stat(p); key=(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns)
 except OSError as x:return {'status':'UNKNOWN','error':str(x)}
 if key in cache:return dict(cache[key],cache_inode=True)
 r=subprocess.run(['timeout','120','nice','-n','19','ionice','-c3','sha256sum','--',str(p)],capture_output=True,text=True)
 v={'status':'OK' if r.returncode==0 else 'UNKNOWN','rc':r.returncode,'sha256':r.stdout.split()[0] if r.returncode==0 else None,'stderr':r.stderr}
 cache[key]=v;return v
for name in N:
 out=E/name
 while not (out/'inventory.json').exists():time.sleep(2)
 inv=json.loads((out/'inventory.json').read_text()); records={}
 targets=inv.get('rpms',[])+[x for x in inv.get('special',[]) if not x.get('link') and (Path(x['path']).name in wanted or x['path'].endswith(('.fdata','.profdata','.profraw','.fdata.xz')) or ('products' in Path(x['path']).parts or 'binaries' in Path(x['path']).parts) and x['size']>1024*1024)]
 for x in targets:
  if x['path'] in records:continue
  row=dict(x,hash=sha(x['path']),duplicates=[]);records[x['path']]=row
  if row['hash']['status']!='OK':continue
  for c in index.get(str(x['size']),[]):
   if c['path']==x['path'] or c['path'].startswith(inv['path']+'/'):continue
   h=sha(c['path'])
   if h.get('sha256')==row['hash']['sha256']:row['duplicates'].append(dict(c,sha256=h['sha256']))
  (out/'hashes.json').write_text(json.dumps(list(records.values()),indent=2))
 print('HASHED',name,len(records),flush=True)
(E/'hash-cache-count.json').write_text(json.dumps({'unique_inodes':len(cache),'errors':sum(x['status']!='OK' for x in cache.values())}))
