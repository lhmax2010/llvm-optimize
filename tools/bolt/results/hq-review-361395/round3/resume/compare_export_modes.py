from pathlib import Path
import subprocess,json,tarfile,hashlib,gzip,re,os,datetime
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.with_name('llvm-optimize');E=Path(__file__).parent
S=W/'temp/hq-review-105-20261116/source';O=W/'temp/single-change-20261114/export-PS3';H=W/'temp/hq-review-104-20261116/exports/HQ'
P=W/'temp/hq-review-105-20261116/export-comparison-overlay';P.mkdir()
patches=sorted(O.glob('000*.patch'));assert len(patches)==8
affected=set()
for patch in patches:
 raw=subprocess.check_output(['git','apply','--numstat',str(patch)],text=True)
 for l in raw.splitlines():
  path=l.split('\t')[2];assert '..' not in Path(path).parts and not path.startswith('/')
  affected.add(path)
def sha(data):return hashlib.sha256(data).hexdigest()
def scan(tar,extract=False):
 result={};special={}
 with tarfile.open(tar,'r|gz') as tf:
  for m in tf:
   if m.isdir():continue
   path=m.name.split('/',1)[1]
   if path.split('/')[0] in ('packaging','.git'):continue
   if m.isfile():
    stream=tf.extractfile(m);h=hashlib.sha256();dest=None;buf=[]
    if extract and path in affected:
     dest=P/path;dest.parent.mkdir(parents=True,exist_ok=True);out=dest.open('xb')
    else:out=None
    try:
     for block in iter(lambda:stream.read(1024*1024),b''):
      h.update(block)
      if out:out.write(block)
      if path.endswith('.git_archival.txt'):buf.append(block)
    finally:
     if out:out.close();dest.chmod(m.mode)
    sig=('file',m.size,h.hexdigest())
    if buf:special[path]=b''.join(buf)
   elif m.issym():sig=('symlink',len(m.linkname),sha(m.linkname.encode()))
   else:raise ValueError(('unsupported tar member',path,m.type))
   assert path not in result,path
   result[path]=sig
 return result,special
old,oldspecial=scan(O/'llvm-22.1.8.tar.gz',True)
logs=[]
for i,patch in enumerate(patches):
 argv=['git','apply','--verbose',str(patch)]
 r=subprocess.run(argv,cwd=P,capture_output=True)
 (E/f'R3c-patch-{i+1:04d}.stdout').write_bytes(r.stdout);(E/f'R3c-patch-{i+1:04d}.stderr').write_bytes(r.stderr)
 logs.append(dict(patch=str(patch),rc=r.returncode,argv=argv))
 assert r.returncode==0,(patch,r.stderr)
for path in affected:
 f=P/path;data=f.read_bytes();old[path]=('file',len(data),sha(data))
new,newspecial=scan(H/'llvm-22.1.8.tar.gz')
keys=sorted(set(old)|set(new));diff=[];same=0
with gzip.open(E/'R3c-all-files.jsonl.gz','wt') as out:
 for path in keys:
  a=old.get(path);b=new.get(path)
  row=dict(path=path,old=a,new=b,identical=a==b);out.write(json.dumps(row)+chr(10))
  if a==b:same+=1
  else:diff.append(row)
allowed='clang/bindings/python/.git_archival.txt';exception=[]
for row in diff:
 path=row['path']
 assert path==allowed,('R3c unexpected difference',row)
 attrs=subprocess.check_output(['git','-C',str(S),'check-attr','--cached','export-subst','eol','text','--',path],text=True)
 (E/'R3c-archival.check-attr.txt').write_text(attrs)
 assert path+': export-subst: set' in attrs
 template=subprocess.check_output(['git','-C',str(S),'show','HEAD:'+path])
 identities={}
 for label,rev,actual in [('PS3-upstream','ca7933e47d3a3451d81e72ac174dcb5aa28b59d1',oldspecial[path]),('PS4-native','e9f16ee3c078f9a5ae563ee01e52ace27b28da4d',newspecial[path])]:
  values={}
  def expand(m):
   fmt=m.group(1).decode();v=subprocess.check_output(['git','-C',str(S),'show','-s','--format='+fmt,rev]).rstrip(b'\n');values[fmt]=v.decode();return v
  expected=re.sub(rb'\$Format:(.*?)\$',expand,template)
  (E/('R3c-'+label+'-archival.txt')).write_bytes(actual)
  assert actual==expected,(label,actual,expected)
  identities[label]=dict(revision=rev,values=values)
 exception.append(dict(path=path,category='E1',identities=identities))
report=dict(PASS=True,old_files=len(old),new_files=len(new),identical=same,exceptions=exception,patches=logs,affected_files=sorted(affected),git_only=sorted(set(old)-set(new)),tar_only=sorted(set(new)-set(old)))
(E/'R3c-result.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2),flush=True)
print('105续R3(c) 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status=PASS',flush=True)
