from pathlib import Path
import json,urllib.request,hashlib,gzip,datetime
D=Path(__file__).resolve().parent
E=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-1215801-1215600')
def req(action,**kw):
 q=urllib.request.Request('http://127.0.0.1:18757',data=json.dumps(dict(action=action,**kw)).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(q,timeout=150) as r:return json.load(r)
def save(path,data,url=None):
 path=E/path;path.parent.mkdir(parents=True,exist_ok=True)
 if isinstance(data,str):data=data.encode()
 rawsha=hashlib.sha256(data).hexdigest();rawlen=len(data)
 if len(data)>1048576 and path.suffix in ['.txt','.html','.xml','.log','.diff']:path=path.with_name(path.name+'.gz');data=gzip.compress(data,mtime=0)
 path.write_bytes(data)
 row={'file':str(path.relative_to(E)),'url':url,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'raw_bytes':rawlen,'raw_sha256':rawsha,'time':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 with (E/'provenance.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
 return row
def get(url):
 with urllib.request.urlopen(url,timeout=90) as r:return r.read()
