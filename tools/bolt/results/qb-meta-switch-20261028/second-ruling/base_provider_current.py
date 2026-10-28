from pathlib import Path
import json,gzip,xml.etree.ElementTree as X,urllib.request,urllib.parse,hashlib
E=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028/second-ruling');D=E/'base-current';D.mkdir(exist_ok=True)
base='https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261013.140248/repos/standard/packages/'
prov=[]
def get(u,n):
 with urllib.request.urlopen(u,timeout=60) as r:b=r.read();prov.append(dict(url=u,status=r.status,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),file=n))
 (D/n).write_bytes(b);return b
M='{http://linux.duke.edu/metadata/repo}';C='{http://linux.duke.edu/metadata/common}';R='{http://linux.duke.edu/metadata/rpm}'
a=X.fromstring(get(base+'repodata/repomd.xml','repomd.xml'));p=next(x for x in a if x.get('type')=='primary');loc=p.find(M+'location').get('href');b=get(urllib.parse.urljoin(base,loc),Path(loc).name);assert hashlib.new(p.find(M+'checksum').get('type'),b).hexdigest()==p.find(M+'checksum').text
out=[]
for p in X.fromstring(gzip.decompress(b)):
 v=p.find(C+'version');fmt=p.find(C+'format');row=dict(name=p.findtext(C+'name'),arch=p.findtext(C+'arch'),**v.attrib)
 for k in ['provides','requires']:row[k]=[dict(x.attrib) for x in fmt.findall(R+k+'/'+R+'entry')]
 row['files']=[x.text for x in fmt.findall(C+'file')];out.append(row)
(D/'packages-all.json').write_text(json.dumps(out,indent=2)+'\n');(D/'provenance.json').write_text(json.dumps(prov,indent=2)+'\n');print('packages',len(out))
