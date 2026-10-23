"""Extract only differing retained RPM members, compare ar metadata/content read-only."""
import hashlib,json,stat,subprocess,time
from pathlib import Path
from rpm_inventory import exact
D=Path(__file__).resolve().parent; out=D/'rpm-difference-analysis';out.mkdir(exist_ok=True)
rows=json.loads((D/'rpm-comparison.json').read_text()); result=[]
def extract(rpm,wanted,dest):
 p=subprocess.Popen(['rpm2cpio',str(rpm)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 try:
  while True:
   h=exact(p.stdout,110);assert h[:6] in (b'070701',b'070702');v=[int(h[6+i*8:14+i*8],16) for i in range(13)];size,ns=v[6],v[11]
   name=exact(p.stdout,ns)[:-1].decode();exact(p.stdout,(-110-ns)%4);name=name.removeprefix('./')
   if name=='TRAILER!!!':break
   f=None
   if name in wanted:
    target=dest/name;target.parent.mkdir(parents=True,exist_ok=True);f=target.open('wb')
   left=size
   while left:
    b=exact(p.stdout,min(left,1048576));left-=len(b)
    if f:f.write(b)
   if f:f.close()
   exact(p.stdout,(-size)%4)
  while p.stdout.read(1048576):pass
  err=p.stderr.read();assert p.wait()==0,err
 finally:
  if p.poll() is None:p.kill();p.wait()
def ar(p):
 b=p.read_bytes();assert b[:8]==b'!<arch>\n';pos=8;members=[];norm=bytearray(b)
 while pos<len(b):
  h=b[pos:pos+60];assert len(h)==60 and h[-2:]==b'`\n';n=int(h[48:58]);data=b[pos+60:pos+60+n];assert len(data)==n
  members.append({'offset':pos,'name':h[:16].decode(),'timestamp':h[16:28].decode(),'uid':h[28:34].decode(),'gid':h[34:40].decode(),'mode':h[40:48].decode(),'size':n,'sha256':hashlib.sha256(data).hexdigest()})
  norm[pos+16:pos+28]=b'0           ';pos+=60+n+n%2
 assert pos==len(b)
 return members,hashlib.sha256(norm).hexdigest()
for row in rows:
 if row['rpm'].endswith('.src.rpm.json') or not row['changes']:continue
 name=row['rpm'].removesuffix('.json');wanted={r['path'] for r in row['changes']};assert all(p.endswith('.a') for p in wanted),wanted
 for label in ('baseline','revised'):
  rpms=list((D/(label+'-products')/'RPMS').rglob(name));assert len(rpms)==1
  extract(rpms[0],wanted,out/label)
 for path in sorted(wanted):
  a,ah=ar(out/'baseline'/path);b,bh=ar(out/'revised'/path)
  changes=[]
  assert len(a)==len(b)
  for x,y in zip(a,b):
   delta={k:{'before':x[k],'after':y[k]} for k in x if x[k]!=y[k]}
   if delta:changes.append({'member':x['name'],'offset':x['offset'],'changes':delta})
  result.append({'rpm':name,'path':path,'members':len(a),'equal_after_only_ar_timestamp_normalization':ah==bh,'normalized_sha256_before':ah,'normalized_sha256_after':bh,'member_changes':changes})
(out/'archive-differences.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'archives':len(result),'only_ar_timestamps':sum(r['equal_after_only_ar_timestamp_normalization'] for r in result)},indent=2))
