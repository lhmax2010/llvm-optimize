"""Read-only failure diagnosis, not a continuation or relaxation of RPM gate."""
from pathlib import Path
import json,subprocess,hashlib,datetime
D=Path(__file__).resolve().parent;W=D.parent.parent;E=W.parent/'llvm-optimize-bolt/tools/bolt/results/runpath-fix-20261026'
result=json.loads((E/'rpm-comparison/compiler-rt-22.1.8-1.x86_64.rpm.json').read_text())['result'];wanted={x['path'] for x in result['changed']}
paths={'old':W/'temp/bolt-on-hybrid-20261024/products/RPMS/compiler-rt-22.1.8-1.x86_64.rpm','new':D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/RPMS/x86_64/compiler-rt-22.1.8-1.x86_64.rpm'}
def read_payload(p):
 child=subprocess.Popen(['rpm2cpio',str(p)],stdout=subprocess.PIPE,stderr=subprocess.PIPE);f=child.stdout;data={}
 def read(n):
  b=b''
  while len(b)<n:
   c=f.read(n-len(b));assert c,'short cpio';b+=c
  return b
 while True:
  h=read(110);assert h[:6] in (b'070701',b'070702');v=[int(h[6+8*i:14+8*i],16) for i in range(13)];size=v[6];ns=v[11]
  name=read(ns).rstrip(b'\0').decode().removeprefix('./');read((-110-ns)%4)
  if name=='TRAILER!!!':break
  b=read(size);read((-size)%4)
  if name in wanted:data[name]=b
 f.read();err=child.stderr.read();assert child.wait()==0,err;assert set(data)==wanted;return data
payload={k:read_payload(p) for k,p in paths.items()}
def ar(b):
 assert b.startswith(b'!<arch>\n');at=8;members=[];ranges=[]
 while at<len(b):
  h=b[at:at+60];assert len(h)==60 and h[-2:]==b'`\n';sz=int(h[48:58]);name=h[:16].decode().strip();body=b[at+60:at+60+sz]
  members.append({'name':name,'header_offset':at,'date':h[16:28].decode(),'size':sz,'content_sha256':hashlib.sha256(body).hexdigest(),'header_except_date_sha256':hashlib.sha256(h[:16]+h[28:]).hexdigest()});ranges.append((at+16,at+28));at+=60+sz+(sz%2)
 assert at==len(b);return members,ranges
rows=[]
for name in sorted(wanted):
 a,b=payload['old'][name],payload['new'][name];am,aranges=ar(a);bm,branges=ar(b);assert len(am)==len(bm)
 changes=[{'member':x['name'],'header_offset':x['header_offset'],'old_date':x['date'],'new_date':y['date']} for x,y in zip(am,bm) if x['date']!=y['date']]
 normalized_a=bytearray(a);normalized_b=bytearray(b)
 for start,end in aranges:normalized_a[start:end]=b' '*12
 for start,end in branges:normalized_b[start:end]=b' '*12
 rows.append({'path':name,'bytes':len(a),'members':len(am),'old_sha256':hashlib.sha256(a).hexdigest(),'new_sha256':hashlib.sha256(b).hexdigest(),'changed_dates':changes,'ar_date_ranges_equal':aranges==branges,'all_bytes_except_ar_dates_equal':normalized_a==normalized_b,'members_content_equal':[x['content_sha256'] for x in am]==[x['content_sha256'] for x in bm]})
summary={'purpose':'failure diagnosis only; original complete-file SHA gate remains FAILED; no normalization adopted','rpm':result['rpm'],'files':len(rows),'all_differences_only_ar_date_fields':all(x['all_bytes_except_ar_dates_equal'] for x in rows),'member_contents_all_equal':all(x['members_content_equal'] for x in rows),'rows':rows}
(E/'rpm-comparison/compiler-rt-ar-diagnosis.json').write_text(json.dumps(summary,indent=2)+'\n');print({k:v for k,v in summary.items() if k!='rows'});print(rows[0])
