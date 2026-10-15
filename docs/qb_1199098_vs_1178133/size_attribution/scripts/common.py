"""Read-only evidence helpers. Run from any working directory."""
from pathlib import Path
import datetime,hashlib,json,requests
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parents[1]
RAW=OUT/'raw'
TEMP=ROOT/'temp/qb_size'
SNAPSHOTS={'old':'20260914.073422','new':'20261015.022255'}
def now():return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  while b:=f.read(1024*1024):h.update(b)
 return h.hexdigest()
def fetch(url,path,session=None):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 s=session or requests.Session();r=s.get(url,stream=True,timeout=(20,180));h=hashlib.sha256();n=0
 with path.open('wb') as f:
  for b in r.iter_content(256*1024):f.write(b);h.update(b);n+=len(b)
 meta={'time':now(),'url':url,'final_url':r.url,'status':r.status_code,'content_type':r.headers.get('Content-Type'),'bytes':n,'sha256':h.hexdigest(),'file':str(path.relative_to(ROOT))}
 with (RAW/'fetch_manifest.jsonl').open('a') as f:f.write(json.dumps(meta,ensure_ascii=False)+'\n')
 print(json.dumps(meta,ensure_ascii=False),flush=True)
 return meta
