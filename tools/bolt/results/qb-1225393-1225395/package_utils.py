from pathlib import Path
import json,hashlib,urllib.request,subprocess,gzip,datetime
from rpm_io import manifest
E=Path(__file__).resolve().parent
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
X=W/'temp/qb-1225393-1225395'
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')

def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def now():return datetime.datetime.now().astimezone().isoformat()

def fetch(row):
 p=Path(row['path']);p.parent.mkdir(parents=True,exist_ok=True)
 receipt=E/'downloads'/row['build']/row['arch']/(row['name']+'.json')
 if p.exists():
  digest=sha(p)
  expected=row.get('sha256')
  if receipt.exists():expected=json.loads(receipt.read_text())['sha256']
  assert expected and digest==expected,('existing file has no verified receipt or SHA differs',str(p))
 else:
  h=hashlib.sha256()
  with urllib.request.urlopen(row['url'],timeout=120) as src,p.open('xb') as out:
   while b:=src.read(1024*1024):out.write(b);h.update(b)
  digest=h.hexdigest()
 q=subprocess.run(['rpm','-qp','--qf','%{NAME}\t%{VERSION}\t%{RELEASE}\t%{ARCH}\t%{VCS}\n',str(p)],capture_output=True,text=True)
 assert q.returncode==0,q.stderr
 rec={**row,'sha256':digest,'bytes':p.stat().st_size,'rpm_query':q.stdout,'rpm_stderr':q.stderr,'time':now()}
 save(receipt,rec)
 return rec

def getman(p,bid,arch,name):
 out=E/'manifests'/bid/arch/(name+'.json.gz');out.parent.mkdir(parents=True,exist_ok=True)
 m=manifest(p)
 with gzip.open(out,'wt') as f:json.dump(m,f,sort_keys=True)
 return m
