from pathlib import Path
import urllib.request,hashlib,json,gzip,re,datetime,xml.etree.ElementTree as ET
E=Path(__file__).resolve().parent
X=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/qb-1221204-1221207')
ROWS=[('1221204','Tizen-Base-Toolchain','tizen-base-toolchain_20261106.102200','tizen-base-toolchain_20261030.061318'),('1221207','Tizen-Base-Dev','tizen-base-dev_20261106.102252','tizen-base-dev_20261030.061217')]
def save(rel,data,url):
 p=E/rel;p.parent.mkdir(parents=True,exist_ok=True)
 rawlen=len(data);rawsha=hashlib.sha256(data).hexdigest()
 if len(data)>1048576:p=p.with_name(p.name+'.gz');data=gzip.compress(data,mtime=0)
 p.write_bytes(data)
 with (E/'provenance.jsonl').open('a') as f:f.write(json.dumps(dict(file=str(p.relative_to(E)),url=url,raw_bytes=rawlen,raw_sha256=rawsha,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),time=datetime.datetime.now().astimezone().isoformat()))+'\n')
 return p
def get(url):
 with urllib.request.urlopen(url,timeout=120) as r:return r.read()
plans=[];status=[]
for bid,project,snap,profile in ROWS:
 base=f'https://download.tizen.org/RBS/TIZEN/Tizen/{project}/{snap}/'
 u=base+f'builddata/manifest/{snap}_standard.xml'
 data=get(u);save(f'{bid}/manifest.xml',data,u)
 rev=[p.attrib for p in ET.fromstring(data).findall('.//project') if p.get('name')=='platform/upstream/llvm'];print(bid,rev,flush=True)
 for arch in ['x86_64','armv7l','aarch64']:
  u=base+f'builddata/buildlogs/standard/{arch}/succeeded/llvm.buildlog.txt'
  data=get(u);save(f'{bid}/{arch}/llvm.buildlog.txt',data,u)
  lines=data.decode(errors='replace').splitlines()
  summary=dict(build=bid,arch=arch,manifest=rev,lines=len(lines),start=[dict(line=i,raw=l) for i,l in enumerate(lines,1) if 'started "build llvm.spec"' in l],end=[dict(line=i,raw=l) for i,l in enumerate(lines,1) if 'finished "build llvm.spec"' in l],rpms=[])
  for i,l in enumerate(lines,1):
   if 'Wrote:' in l and l.endswith('.rpm'):
    name=l.rsplit('/',1)[-1];summary['rpms'].append(dict(line=i,raw=l,name=name))
    if arch=='x86_64':
     sub='source' if name.endswith('.src.rpm') else 'debug' if '-debuginfo-' in name or '-debugsource-' in name else 'packages/x86_64'
     plans.append(dict(build=bid,name=name,url=base+f'repos/standard/{sub}/'+name,path=str(X/bid/'rpms'/name)))
  status.append(summary);print(bid,arch,len(data),len(lines),summary['end'],flush=True)
 for label,url in [('snapshot',f'https://download.tizen.org/snapshots/TIZEN/Tizen/{project}/{profile}/builddata/build.conf'),('rbs',base+'builddata/build.conf')]:
  try:
   data=get(url);save(f'{bid}/{label}-build.conf',data,url);print(bid,label,'buildconf',hashlib.sha256(data).hexdigest(),flush=True)
  except Exception as ex:save(f'{bid}/{label}-buildconf-error.txt',str(ex).encode(),url);print(url,str(ex),flush=True)
(E/'rpm-plan.json').write_text(json.dumps(plans,indent=2)+'\n')
(E/'arch-status.json').write_text(json.dumps(status,indent=2)+'\n')
