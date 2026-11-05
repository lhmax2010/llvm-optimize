from pathlib import Path
import os,json,stat,hashlib,time
from checks import identity,process_snapshot,mount_snapshot,user_services,command,parent_snapshot,stamp
E=Path(__file__).parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize')
rows=[dict(number=n,path=p if p.startswith('/') else str(W/'temp'/p)) for n,p in json.loads((E/'targets.json').read_text())]
def save(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
paths=[r['path'] for r in rows];save('df-before.json',command(['df','-B1','/home']));save('processes-before.json',process_snapshot(paths));save('mounts-before.json',mount_snapshot(paths));save('services-before.json',user_services());save('parents-before.json',parent_snapshot(paths[:3]))
protected=['night-20261105','night-20261103','qb-1216409-1216410','review-20261102','hq-463c9a13','debuglink-20261028/full-20261030/products','runpath-fix-20261026/products','oldtext-final-20261027/products','bolt-on-hybrid-20261024','bench_results','pgo-bolt-followup-20261105','debuglink-tb20261026'];save('protected-before.json',[dict(path=str(W/'temp'/p),identity=identity(W/'temp'/p)) for p in protected])
for r in rows:
 t=time.monotonic();p=Path(r['path']);r['identity']=identity(p);r['errors']=[];r['repos']=[];r['rpms']=[];r['nonuser_entries']=0;r['not_user_writable_dirs']=0;r['top']=[]
 print(stamp(),'SCAN_START',r['number'],p,flush=True)
 if r['identity'].get('directory') and not r['identity']['symlink'] and r['identity']['realpath']==str(p):
  try:
   for q in sorted(p.iterdir()):
    s=q.lstat();r['top'].append(dict(name=q.name,mode=oct(s.st_mode),uid=s.st_uid,gid=s.st_gid,bytes=s.st_size,mtime_ns=s.st_mtime_ns,link=os.readlink(q) if q.is_symlink() else None))
  except OSError as ex:r['errors'].append(str(ex))
  mounts=json.loads((E/'mounts-before.json').read_text());hits=[x for x in mounts['matches'] if x['target']==str(p)];r['mount_hits']=hits
  if not hits:
   def err(e):r['errors'].append(str(e))
   for d,ds,fs in os.walk(p,followlinks=False,onerror=err):
    try:
     sd=os.lstat(d)
     if sd.st_uid!=os.getuid():r['nonuser_entries']+=1
     if not os.access(d,os.W_OK|os.X_OK):r['not_user_writable_dirs']+=1
     if '.git' in ds or '.git' in fs:r['repos'].append(d)
     if 'HEAD' in fs and 'objects' in ds and 'refs' in ds:r['repos'].append(d)
     ds[:]=[x for x in ds if x!='.git' and not os.path.islink(os.path.join(d,x))]
     for f in fs:
      q=Path(d)/f
      if q.suffix=='.rpm' and not q.is_symlink():
       with q.open('rb') as stream:h=hashlib.file_digest(stream,'sha256').hexdigest()
       r['rpms'].append(dict(path=str(q.relative_to(p)),bytes=q.stat().st_size,sha256=h))
    except (OSError,ValueError) as ex:r['errors'].append(str(ex))
   r['du']=command(['nice','-n','19','ionice','-c3','du','-sx','-B1',str(p)],180)
  else:r['scan_skipped']='mount reference; no recursive scan'
 r['seconds']=time.monotonic()-t;save('path-%02d.json'%r['number'],r);save('inventory.json',rows);print(stamp(),'SCAN_END',r['number'],'repos',len(r['repos']),'rpms',len(r['rpms']),'errors',len(r['errors']),flush=True)
print('INVENTORY 已结束',stamp(),'status=ok',flush=True)
