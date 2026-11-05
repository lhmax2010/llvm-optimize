"""Read completed build outputs; publish text evidence only, retain every original."""
from pathlib import Path
import datetime,gzip,hashlib,json,os,shutil,subprocess
E=Path(__file__).resolve().parent
D=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain')
assert 'NIGHT_PROJECT 已结束' in (D/'controller.stdout').read_text(), 'wait for automatic build and validation completion'
records=[]
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def copy(p,relative):
 target=E/relative; target.parent.mkdir(parents=True,exist_ok=True)
 compressed=p.stat().st_size>1024*1024
 if compressed:target=target.with_name(target.name+'.gz')
 assert not target.exists(),str(target)
 if compressed:
  with p.open('rb') as f,target.open('wb') as dst,gzip.GzipFile(filename='',mode='wb',fileobj=dst,mtime=0) as out:shutil.copyfileobj(f,out,1024*1024)
 else:shutil.copyfile(p,target)
 records.append(dict(source=str(p),bytes=p.stat().st_size,sha256=digest(p),saved=str(target.relative_to(E)),saved_bytes=target.stat().st_size,saved_sha256=digest(target)))
for name in ['controller.stdout','controller.stderr','plan.json']:
 p=D/name
 if p.is_file():copy(p,'completed/'+name)
for directory in ['evidence','validation']:
 base=D/directory
 if not base.exists():continue
 for p in sorted(base.iterdir()):
  if p.is_file() and p.suffix in ('.json','.jsonl','.txt','.stdout','.stderr','.md','.log') and p.name!='rpm-build.log':copy(p,'completed/'+directory+'/'+p.name)
 # Per-package manifests are text evidence, never copy unpacked payloads.
 if directory=='validation' and (base/'manifests').exists():
  for p in sorted((base/'manifests').rglob('*.json')):copy(p,'completed/validation/'+str(p.relative_to(base)))
logs=sorted((D/'gbs-driver/local/repos').glob('*/x86_64/logs/*/llvm-*/log.txt'))
for i,p in enumerate(logs):copy(p,'completed/gbs-original-'+str(i)+'.log')
(E/'provenance.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
(E/'df-final.txt').write_text(subprocess.check_output(['df','-B1','/home'],text=True))
s=os.statvfs('/home');(E/'completion-space.json').write_text(json.dumps(dict(time=datetime.datetime.now().astimezone().isoformat(),available_bytes=s.f_bavail*s.f_frsize),indent=2)+'\n')
print('COLLECTED',len(records),'files; originals unchanged')
