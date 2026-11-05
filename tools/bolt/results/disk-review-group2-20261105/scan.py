import os,sys,json,subprocess,time,gzip,stat,datetime
from pathlib import Path
E=Path(__file__).resolve().parent
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
N=json.loads((E/'targets.json').read_text())
def cmd(argv,seconds=90):
 t=time.monotonic()
 try:
  r=subprocess.run(['timeout',str(seconds),'nice','-n','19','ionice','-c3']+argv,capture_output=True,text=True)
  return {'argv':argv,'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'seconds':time.monotonic()-t,'status':'UNKNOWN' if r.returncode else 'OK'}
 except Exception as x:return {'argv':argv,'status':'UNKNOWN','error':str(x)}
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
for n in N:
 root=W/'temp'/n; out=E/n;out.mkdir(exist_ok=True)
 print(datetime.datetime.now().astimezone().isoformat(),'START',n,flush=True)
 info={'path':str(root),'exists':root.exists(),'symlink':root.is_symlink(),'realpath':str(root.resolve()),'errors':[],'repositories':[],'special':[],'rpms':[],'top':[]}
 if not root.exists():save(out/'inventory.json',info);continue
 info['du']=cmd(['du','-sx','-B1','--',str(root)],180)
 for p in sorted(root.iterdir()):
  st=p.lstat(); entry={'path':str(p),'name':p.name,'mode':stat.filemode(st.st_mode),'size':st.st_size,'uid':st.st_uid,'mtime':st.st_mtime}
  if p.is_dir() and not p.is_symlink():entry['du']=cmd(['du','-sx','-B1','--',str(p)],90)
  info['top'].append(entry)
 start=time.monotonic(); count=0
 with gzip.open(out/'files.jsonl.gz','wt') as log:
  for base,ds,fs in os.walk(root,followlinks=False,onerror=lambda x:info['errors'].append(str(x))):
   if time.monotonic()-start>240:info['errors'].append('walk timeout 240s; incomplete UNKNOWN');break
   p=Path(base)
   if '.git' in ds or '.git' in fs:info['repositories'].append(str(p))
   if 'HEAD' in fs and 'objects' in ds and 'refs' in ds:info['repositories'].append(str(p));ds[:]=[];continue
   if '.git' in ds:ds.remove('.git')
   for f in fs:
    q=p/f
    try:
     s=q.lstat(); rec={'path':str(q),'size':s.st_size,'allocated':s.st_blocks*512,'mode':stat.filemode(s.st_mode),'uid':s.st_uid,'mtime':s.st_mtime,'dev':s.st_dev,'ino':s.st_ino,'nlink':s.st_nlink}
     if stat.S_ISLNK(s.st_mode):rec['link']=os.readlink(q)
     log.write(json.dumps(rec,ensure_ascii=False)+'\n');count+=1
     if f.endswith('.rpm'):info['rpms'].append(rec)
     if f in ('merge-fdata','libbolt_rt_instr.a','perf2bolt','llvm-bolt','clang-22','clang','clang++','clang.bolt','clang-22.debug','llvm-strip','llvm-symbolizer','identity.json','build.conf','CMakeCache.txt','build.ninja') or f.endswith(('.fdata','.profraw','.profdata','.fdata.xz')) or 'products' in q.parts or 'binaries' in q.parts:info['special'].append(rec)
    except OSError as x:info['errors'].append(str(x))
 info['file_count']=count
 save(out/'inventory.json',info)
 print('DONE',n,'files',count,'rpm',len(info['rpms']),'repos',len(info['repositories']),'errors',len(info['errors']),flush=True)
