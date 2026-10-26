from pathlib import Path
import os,stat,json,time,collections
E=Path(__file__).resolve().parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize')
tops=[p for p in (W/'temp').iterdir() if p.is_dir() and not p.is_symlink()]+[p for p in Path('/var/tmp').iterdir() if p.is_dir() and any(x in p.name for x in ['llvm','gbs','hybrid','bolt'])]
results=[];hard={};assets=[];scripts=[];special=[];links=[]
for top in tops:
 dev=top.stat().st_dev;meta=dict(path=str(top),files=0,root_owned=0,root_owned_dirs=0,not_writable_dirs=0,newest_file_ns=0,newest_file=None,errors=[],git_roots=[],bytes_counting_links=0)
 def walk(p):
  try:entries=list(os.scandir(p))
  except OSError as e:meta['errors'].append(dict(path=str(p),error=str(e)));return
  for e in entries:
   try:s=e.stat(follow_symlinks=False)
   except OSError as x:meta['errors'].append(dict(path=e.path,error=str(x)));continue
   if s.st_dev!=dev:continue
   if stat.S_ISDIR(s.st_mode):
    if s.st_uid==0:meta['root_owned_dirs']+=1
    if not os.access(e.path,os.W_OK|os.X_OK):meta['not_writable_dirs']+=1
    if e.name=='.git':meta['git_roots'].append(str(Path(e.path).parent))
    if e.name in ['lto.cache','BUILD','BUILDROOT','RPMS','SRPMS','upper','lower','work','products','baseline-products','revised-products','build','payload-merged','baseline-extract','independent-install'] or e.name.startswith('scratch.'):
     special.append(dict(path=e.path,top=str(top),name=e.name))
    walk(e.path)
   elif stat.S_ISREG(s.st_mode):
    meta['files']+=1;meta['root_owned']+=s.st_uid==0;meta['bytes_counting_links']+=s.st_blocks*512
    if s.st_mtime_ns>meta['newest_file_ns']:meta['newest_file_ns']=s.st_mtime_ns;meta['newest_file']=e.path
    if s.st_nlink>1:
     key=f'{s.st_dev}:{s.st_ino}';h=hard.setdefault(key,dict(nlink=s.st_nlink,allocated=s.st_blocks*512,size=s.st_size,paths=[]));h['paths'].append(e.path)
    if e.name=='.git':meta['git_roots'].append(str(Path(e.path).parent))
    if e.name in ['clang-22','ordinary-clang-22','candidate-clang-22','llvm-bolt','clang.bolt','clang.stripped','profile.fdata','clang-bolt-v2.fdata.xz','identity.json','preserved.json','build.conf','gbs_llvm_qb1202084.conf'] or e.name.endswith('.rpm') or (e.name.endswith('.fdata') and s.st_size>0):
     assets.append(dict(path=e.path,top=str(top),bytes=s.st_size,allocated=s.st_blocks*512,uid=s.st_uid,dev=s.st_dev,ino=s.st_ino,mtime_ns=s.st_mtime_ns))
    rel=Path(e.path).relative_to(top)
    if e.name.endswith(('.py','.sh')) and len(rel.parts)<=4 and not any(x in rel.parts for x in ['.git','source','llvm','BUILD-ROOTS','sources']):scripts.append(e.path)
   elif stat.S_ISLNK(s.st_mode) and len(Path(e.path).relative_to(top).parts)<=4:
    try:links.append(dict(path=e.path,target=os.readlink(e.path)))
    except OSError:pass
 walk(top);results.append(meta)
 for name,data in [('metadata',results),('hardlinks',hard),('assets-found',assets),('scripts',scripts),('special-directories',special),('top-symlinks',links)]:
  (E/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')
 print(top.name,meta['files'],'errors',len(meta['errors']),flush=True)
(E/'metadata-complete.json').write_text(json.dumps(dict(time=time.time(),tops=len(results)))+'\n')
