from pathlib import Path
import urllib.request,json,gzip,re,hashlib,datetime,xml.etree.ElementTree as ET
E=Path(__file__).resolve().parent;X=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/qb-1226850-1226851')
plans=[];results=[]
for bid,project,profile in [('1226850','Tizen-Base-Toolchain','tizen-base-toolchain_20261030.061318'),('1226851','Tizen-Base-Dev','tizen-base-dev_20261030.061217')]:
 text=(E/bid/'overview.txt').read_text()
 fields=dict(x.split('\t',1) for x in text.splitlines() if '\t' in x)
 assert fields['Build Package List']=='platform/upstream/llvm@fea0fe464d56e17f2c7588c557bfffd9f6ac352b'
 assert fields['Profile URL'].rstrip('/').endswith('/'+profile)
 base=fields['Download_URL'].replace('http://','https://').rstrip('/')+'/'
 snap=base.rstrip('/').rsplit('/',1)[-1]
 u=base+'builddata/manifest/'+snap+'_standard.xml'
 with urllib.request.urlopen(u,timeout=90) as resp:data=resp.read(2*1024*1024)
 (E/bid/'manifest.xml').write_bytes(data)
 rev=[p.attrib for p in ET.fromstring(data).findall('.//project') if p.get('name')=='platform/upstream/llvm']
 assert len(rev)==1 and rev[0]['revision']=='fea0fe464d56e17f2c7588c557bfffd9f6ac352b'
 for arch in ['x86_64','armv7l','aarch64']:
  u=base+'builddata/buildlogs/standard/'+arch+'/succeeded/llvm.buildlog.txt'
  p=E/bid/arch/'llvm.buildlog.txt.gz';p.parent.mkdir(exist_ok=True)
  h=hashlib.sha256();size=0
  with urllib.request.urlopen(u,timeout=90) as resp,p.open('xb') as raw,gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as out:
   for block in iter(lambda:resp.read(1048576),b''):out.write(block);h.update(block);size+=len(block)
  row={'build':bid,'project':project,'arch':arch,'profile':profile,'url':u,'raw_bytes':size,'raw_sha256':h.hexdigest(),'manifest_revision':rev[0]['revision'],'start':[],'end':[],'rpms':[]}
  with gzip.open(p,'rt',errors='replace') as f:
   for n,line in enumerate(f,1):
    line=line.rstrip('\n')
    for key,needle in [('start','started "build llvm.spec"'),('end','finished "build llvm.spec"')]:
     if needle in line:row[key].append({'line':n,'raw':line})
    if 'Wrote:' in line and line.endswith('.rpm'):
     name=line.rsplit('/',1)[-1];row['rpms'].append(name)
     if name.endswith('.src.rpm') and arch!='x86_64':continue
     sub='source' if name.endswith('.src.rpm') else 'debug' if '-debuginfo-' in name or '-debugsource-' in name else 'packages/'+arch
     plans.append({'build':bid,'project':project,'arch':arch,'name':name,'url':base+'repos/standard/'+sub+'/'+name,'path':str(X/bid/arch/'rpms'/name)})
  assert row['start'] and row['end'],row
  row['lines']=n;results.append(row)
  (E/'arch-status.json').write_text(json.dumps(results,indent=2)+'\n')
  print(bid,arch,'PASS',row['end'],len(row['rpms']),flush=True)
(E/'rpm-plan.json').write_text(json.dumps(plans,indent=2)+'\n')
end='ITEM1 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status=ok reason=identities_snapshots_and_three_arch_builds_verified'
(E/'item1-end.txt').write_text(end+'\n');print(end,flush=True)
