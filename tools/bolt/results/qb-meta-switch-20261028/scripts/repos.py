from pathlib import Path
import json,gzip,xml.etree.ElementTree as X,urllib.request,urllib.parse,hashlib,collections
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=Path(__file__).resolve().parent;E=B/'tools/bolt/results/qb-meta-switch-20261028';F=B/'tools/bolt/results/qb-meta-fix-and-snapshot-20261028/snapshots'
C='{http://linux.duke.edu/metadata/common}';R='{http://linux.duke.edu/metadata/rpm}';M='{http://linux.duke.edu/metadata/repo}'
def parse(data):
 out=[]
 for p in X.fromstring(gzip.decompress(data)):
  v=p.find(C+'version');fmt=p.find(C+'format');check=p.find(C+'checksum')
  row=dict(name=p.findtext(C+'name'),arch=p.findtext(C+'arch'),**v.attrib,location=p.find(C+'location').get('href'),checksum=check.text,checksum_type=check.get('type'),source=fmt.findtext(R+'sourcerpm'),size=int(p.find(C+'size').get('package')))
  for kind in ['provides','requires']:row[kind]=[dict(x.attrib) for x in fmt.findall(R+kind+'/'+R+'entry')]
  row['files']=[x.text for x in fmt.findall(C+'file')];out.append(row)
 return out
prov=[]
def get(url,p):
 p.parent.mkdir(parents=True,exist_ok=True)
 try:
  with urllib.request.urlopen(url,timeout=90) as r:data=r.read();status=r.status;final=r.url
  p.write_bytes(data);prov.append(dict(url=url,final_url=final,status=status,file=str(p.relative_to(E)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()));return data
 except Exception as ex:prov.append(dict(url=url,error=str(ex)));return None
for side in ['toolchain','base']:
 p=next((F/side).glob('*primary*'));data=p.read_bytes();rows=parse(data);d=E/'repos'/side;d.mkdir(parents=True,exist_ok=True);(d/'packages-all.json').write_text(json.dumps(rows,indent=2)+'\n');print(side,collections.Counter(r['arch'] for r in rows),flush=True)
urls={'unified':'https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified/tizen-unified_20261027.231956/','unified-toolchain':'https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20261016.052151/'}
for name,root in urls.items():
 d=E/'repos'/name
 get(root+'build.xml',d/'build.xml');get(root+'builddata/',d/'builddata-index.html');base=root+'repos/standard/packages/'
 data=get(base+'repodata/repomd.xml',d/'repomd.xml')
 if data:
  el=X.fromstring(data);primary=next(x for x in el if x.get('type')=='primary');loc=primary.find(M+'location').get('href');raw=get(urllib.parse.urljoin(base,loc),d/Path(loc).name)
  if raw:
   check=primary.find(M+'checksum');assert hashlib.new(check.get('type'),raw).hexdigest()==check.text
   rows=parse(raw);(d/'packages-all.json').write_text(json.dumps(rows,indent=2)+'\n');print(name,collections.Counter(r['arch'] for r in rows),flush=True)
 for arch in ['armv7l','aarch64','x86_64']:
  get(base+arch+'/',d/(arch+'-packages.html'));get(root+'repos/standard/debug/'+arch+'/',d/(arch+'-debug.html'))
(E/'repo-download-provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
