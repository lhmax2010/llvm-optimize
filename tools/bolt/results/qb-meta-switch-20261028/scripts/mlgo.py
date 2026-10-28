from pathlib import Path
import json,urllib.request,hashlib,subprocess,os,time,re,resource
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=Path(__file__).resolve().parent;E=B/'tools/bolt/results/qb-meta-switch-20261028';out=E/'mlgo';out.mkdir(exist_ok=True)
source=D/'mlgo.c';source.write_text('static int twice(int x) { return x * 2; }\nint probe(int *p, int n) { int s=0; for (int i=0;i<n;++i) s += twice(p[i]) + i; return s; }\n');(out/'mlgo.c').write_bytes(source.read_bytes())
urls={'base':'https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base/tizen-base_20261026.005418/repos/standard/packages/','toolchain':'https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261013.024319/repos/standard/packages/'}
records=[];tests=[]
def save():
 (out/'downloads.json').write_text(json.dumps(records,indent=2)+'\n');(out/'tests.json').write_text(json.dumps(tests,indent=2)+'\n')
def limits():
 resource.setrlimit(resource.RLIMIT_CORE,(0,0));resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,4*1024**3))
for side in ['base','toolchain']:
 rows=json.loads((E/'repos'/side/'packages-all.json').read_text());root=D/'mlgo'/side/'root';root.mkdir(parents=True,exist_ok=True);rpmdir=root.parent/'rpms';rpmdir.mkdir(exist_ok=True)
 # Shared libraries actually required by these clang RPMs; no RPM scripts or installation.
 for name in ['clang','glibc','libgcc','libstdc++','zlib']:
  candidates=[r for r in rows if r['name']==name and r['arch']=='x86_64'];assert len(candidates)==1,(side,name,len(candidates));r=candidates[0];url=urls[side]+r['location'];p=rpmdir/Path(r['location']).name;t=time.monotonic()
  if not p.exists():
   with urllib.request.urlopen(url,timeout=120) as response,p.open('wb') as f:
    while True:
     chunk=response.read(1024*1024)
     if not chunk:break
     f.write(chunk)
  h=hashlib.sha256()
  with p.open('rb') as f:
   for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
  assert r['checksum_type']=='sha256' and h.hexdigest()==r['checksum']
  rec=dict(side=side,package=name,url=url,bytes=p.stat().st_size,sha256=h.hexdigest(),download_seconds=time.monotonic()-t);records.append(rec);save();print(side,name,'downloaded',p.stat().st_size,flush=True)
  # cpio does not run package scripts. Preserve stderr and check both pipeline exits.
  with (out/(side+'-'+name+'-unpack.txt')).open('w') as log:
   producer=subprocess.Popen(['rpm2cpio',str(p)],stdout=subprocess.PIPE,stderr=log)
   consumer=subprocess.Popen(['cpio','-idm','--quiet','--no-absolute-filenames'],cwd=root,stdin=producer.stdout,stdout=log,stderr=log)
   producer.stdout.close();c=consumer.wait();a=producer.wait();assert (a,c)==(0,0),(side,name,a,c)
  rec['unpack_rc']=[a,c];save()
 clang=root/'usr/bin/clang-22';assert clang.is_file()
 loaders=list(root.glob('lib64/ld-linux-x86-64.so.2'))+list(root.glob('usr/lib64/ld-linux-x86-64.so.2'));assert loaders
 loader=loaders[0];libpath=':'.join(str(root/x) for x in ['lib64','usr/lib64']);prefix=[str(loader),'--library-path',libpath,str(clang),'--no-default-config']
 for label,args in [('version',['--version']),('loader-list',[])]:
  cmd=prefix+args if label=='version' else [str(loader),'--library-path',libpath,'--list',str(clang)]
  q=subprocess.run(cmd,capture_output=True,text=True,timeout=30,preexec_fn=limits);(out/(side+'-'+label+'.txt')).write_text(q.stdout+q.stderr);assert q.returncode==0,(side,label,q.stderr)
 for target in ['armv7l-tizen-linux-gnueabi','aarch64-tizen-linux-gnu']:
  obj=root.parent/(target+'.o');cmd=prefix+['--target='+target,'-O2','-mllvm=-regalloc-enable-advisor=release','-mllvm=-enable-ml-inliner=release','-c',str(source),'-o',str(obj)]
  t=time.monotonic();q=subprocess.run(cmd,capture_output=True,text=True,timeout=90,preexec_fn=limits);stem=side+'-'+target;(out/(stem+'.stdout')).write_text(q.stdout);(out/(stem+'.stderr')).write_text(q.stderr)
  row=dict(side=side,target=target,argv=cmd,rc=q.returncode,seconds=time.monotonic()-t,stdout=stem+'.stdout',stderr=stem+'.stderr',object_exists=obj.exists(),object_bytes=obj.stat().st_size if obj.exists() else 0)
  if obj.exists():row['object_sha256']=hashlib.sha256(obj.read_bytes()).hexdigest()
  tests.append(row);save();print(side,target,'rc',q.returncode,q.stderr[:240],flush=True)
