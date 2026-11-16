from pathlib import Path
import subprocess,json,tarfile,hashlib,gzip,re,os,datetime,tempfile
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.with_name('llvm-optimize');E=Path(__file__).parent
S=W/'temp/hq-review-105-20261116/source';O=W/'temp/single-change-20261114/export-PS3';H=W/'temp/hq-review-104-20261116/exports/HQ'
P=Path(tempfile.mkdtemp(prefix='task105-r3c-',dir='/var/tmp'));(E/'workspace.txt').write_text(str(P))
r=subprocess.run(['git','rev-parse','--show-toplevel'],cwd=P,capture_output=True)
(E/'outside-git.stdout').write_bytes(r.stdout);(E/'outside-git.stderr').write_bytes(r.stderr)
assert r.returncode!=0,('unexpected Git repository',r.stdout)
argv=['tar','--extract','--gzip','--file',str(O/'llvm-22.1.8.tar.gz'),'--directory',str(P),'--no-same-owner']
r=subprocess.run(argv,capture_output=True);(E/'extract.stderr').write_bytes(r.stderr);assert r.returncode==0,r.stderr
dirs=[p for p in P.iterdir()];assert len(dirs)==1 and dirs[0].is_dir(),dirs
P=dirs[0];(E/'source-root.txt').write_text(str(P))
r=subprocess.run(['git','rev-parse','--show-toplevel'],cwd=P,capture_output=True);assert r.returncode!=0,r.stdout
patches=sorted(O.glob('000*.patch'));assert len(patches)==8
logs=[]
for i,p in enumerate(patches,1):
 stat=subprocess.check_output(['git','apply','--numstat',str(p)],text=True)
 expected=[l.split('\t')[2] for l in stat.splitlines()]
 argv=['patch','-p1','--forward','--batch','--no-backup-if-mismatch','-i',str(p)]
 r=subprocess.run(argv,cwd=P,capture_output=True,text=True)
 (E/f'patch-{i:04d}.stdout').write_text(r.stdout);(E/f'patch-{i:04d}.stderr').write_text(r.stderr);(E/f'patch-{i:04d}.numstat').write_text(stat)
 actual=re.findall(r'^patching file (.+)$',r.stdout,re.M)
 row=dict(patch=p.name,argv=argv,rc=r.returncode,expected=expected,actual=actual)
 logs.append(row);(E/'patch-application.json').write_text(json.dumps(logs,indent=2))
 assert r.returncode==0 and sorted(expected)==sorted(actual),row
 assert not re.search(r'Skipped|FAILED|Reversed',r.stdout+r.stderr),row
 print('applied',p.name,len(actual),flush=True)
for i,p in reversed(list(enumerate(patches,1))):
 argv=['patch','-p1','--reverse','--dry-run','--batch','-i',str(p)]
 r=subprocess.run(argv,cwd=P,capture_output=True,text=True)
 (E/f'reverse-{i:04d}.stdout').write_text(r.stdout);(E/f'reverse-{i:04d}.stderr').write_text(r.stderr)
 assert r.returncode==0,(p.name,r.stdout,r.stderr)
 actual=re.findall(r'^checking file (.+)$',r.stdout,re.M)
 assert sorted(actual)==sorted(logs[i-1]['expected']),(p.name,actual)
 logs[i-1]['reverse_dry_run']=dict(argv=argv,rc=0,actual=actual)
(E/'patch-application.json').write_text(json.dumps(logs,indent=2))
print('all reverse dry-run checks PASS',flush=True)
def digest_stream(f):
 h=hashlib.sha256()
 for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
old={};special={}
for root,dirs,files in os.walk(P):
 dirs[:]=[d for d in dirs if (Path(root)/d).relative_to(P).parts[0] not in ('packaging','.git')]
 for name in files:
  f=Path(root)/name;path=f.relative_to(P).as_posix()
  if path.split('/')[0] in ('packaging','.git'):continue
  if f.is_symlink():data=os.readlink(f).encode();sig=('symlink',len(data),hashlib.sha256(data).hexdigest())
  else:
   with f.open('rb') as stream:sig=('file',f.stat().st_size,digest_stream(stream))
  old[path]=sig
  if path.endswith('.git_archival.txt'):special[path]=f.read_bytes()
new={};newspecial={}
with tarfile.open(H/'llvm-22.1.8.tar.gz','r|gz') as tf:
 for m in tf:
  if m.isdir():continue
  path=m.name.split('/',1)[1]
  if path.split('/')[0] in ('packaging','.git'):continue
  if m.isfile():
   f=tf.extractfile(m)
   if path.endswith('.git_archival.txt'):
    data=f.read();newspecial[path]=data;sig=('file',len(data),hashlib.sha256(data).hexdigest())
   else:sig=('file',m.size,digest_stream(f))
  elif m.issym():
   data=m.linkname.encode();sig=('symlink',len(data),hashlib.sha256(data).hexdigest())
  else:raise ValueError((path,m.type))
  assert path not in new,path
  new[path]=sig
same=0;diff=[]
with gzip.open(E/'R3c-files.jsonl.gz','wt') as out:
 for path in sorted(set(old)|set(new)):
  row=dict(path=path,old=old.get(path),new=new.get(path),identical=old.get(path)==new.get(path));out.write(json.dumps(row)+chr(10))
  if row['identical']:same+=1
  else:diff.append(row)
(E/'R3c-raw-differences.json').write_text(json.dumps(diff,indent=2))
allowed=json.loads((E.parent/'export-mismatch-details.json').read_text())
exceptions=[]
for row in diff:
 path=row['path'];assert path in allowed,('new unexpected difference',row)
 attrs=subprocess.check_output(['git','-C',str(S),'check-attr','--cached','export-subst','eol','text','--',path],text=True)
 (E/(allowed[path]['evidence']+'.check-attr.txt')).write_text(attrs)
 if path.endswith('.git_archival.txt'):
  assert path+': export-subst: set' in attrs
  template=subprocess.check_output(['git','-C',str(S),'show','HEAD:'+path]);identities={}
  for label,rev,actual in [('PS3-upstream','ca7933e47d3a3451d81e72ac174dcb5aa28b59d1',special[path]),('PS4-native','e9f16ee3c078f9a5ae563ee01e52ace27b28da4d',newspecial[path])]:
   values={}
   def expand(m):
    fmt=m.group(1).decode();val=subprocess.check_output(['git','-C',str(S),'show','-s','--format='+fmt,rev]).rstrip(b'\n');values[fmt]=val.decode();return val
   expected=re.sub(rb'\$Format:(.*?)\$',expand,template)
   (E/(label+'-archival.txt')).write_bytes(actual)
   assert actual==expected,(label,actual,expected)
   identities[label]=dict(revision=rev,values=values)
  exceptions.append(dict(path=path,category='E1',identities=identities))
 else:
  raise AssertionError(('CRLF files expected already identical in both exports',row))
report=dict(PASS=True,files=len(old),new_files=len(new),identical=same,exceptions=exceptions,patches=logs,source_root=str(P),CRLF_files_identical=[x for x in allowed if x!= 'clang/bindings/python/.git_archival.txt' and old.get(x)==new.get(x)])
(E/'R3c-result.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='patches'},indent=2),flush=True)
print('105续二R3(c) 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status=PASS',flush=True)
