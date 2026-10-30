from common import *
from rpm_io import manifest
import struct,stat,unittest,io

def ar_members(b):
 assert b[:8]==b'!<arch>\n','not regular ar'
 at=8;out=[];names=b''
 while at<len(b):
  hd=b[at:at+60];assert len(hd)==60 and hd[58:]==b'`\n';sz=int(hd[48:58]);body=b[at+60:at+60+sz];assert len(body)==sz
  raw=hd[:16].decode().strip();name=raw
  if raw=='//':names=body
  elif raw.startswith('/') and raw[1:].isdigit():
   ix=int(raw[1:]);end=names.find(b'/\n',ix);assert end>=ix;name=names[ix:end].decode()
  elif raw not in ('/','/SYM64/'):name=raw.rstrip('/')
  out.append({'name':name,'raw_name':raw,'offset':at,'size':sz,'sha256':hashlib.sha256(body).hexdigest(),'body':body,'date':hd[16:28].decode()});at+=60+sz+(sz%2)
 assert at==len(b);return out

def date_difference(a,b):
 try:
  am,bm=ar_members(a),ar_members(b)
  order=[x['name'] for x in am]==[x['name'] for x in bm]
  contents=[x['sha256'] for x in am]==[x['sha256'] for x in bm]
  ranges=[(x['offset']+16,x['offset']+28) for x in am];br=[(x['offset']+16,x['offset']+28) for x in bm]
  aa,bb=bytearray(a),bytearray(b)
  for start,end in ranges:aa[start:end]=b' '*12
  for start,end in br:bb[start:end]=b' '*12
  outside=len(a)==len(b) and ranges==br and aa==bb
  return {'classification':'allowed-ar-date-difference' if a!=b and order and contents and outside else 'identical' if a==b else 'FAIL','member_order_equal':order,'member_content_sha_equal':contents,'all_other_bytes_equal':outside,'members':[{'name':x['name'],'sha256':x['sha256'],'header_offset':x['offset'],'old_date':x['date'],'new_date':y['date']} for x,y in zip(am,bm)]}
 except (AssertionError,ValueError,UnicodeError):return {'classification':'FAIL','reason':'invalid/different ar structure'}

def extract_selected(rpm,names,dest):
 dest.mkdir(parents=True,exist_ok=True);p=subprocess.Popen(['rpm2cpio',str(rpm)],stdout=subprocess.PIPE,stderr=subprocess.PIPE);f=p.stdout
 def read(n):
  b=b''
  while len(b)<n:
   x=f.read(n-len(b));assert x;b+=x
  return b
 found=set()
 while True:
  header=read(110);assert header[:6] in (b'070701',b'070702');v=[int(header[6+8*i:14+8*i],16) for i in range(13)];size=v[6];n=v[11];name=read(n).rstrip(b'\0').decode().removeprefix('./');read((-110-n)%4)
  if name=='TRAILER!!!':break
  out=None
  if name in names:
   target=dest/name;assert target.is_relative_to(dest);target.parent.mkdir(parents=True,exist_ok=True);out=target.open('wb');found.add(name)
  left=size
  while left:
   b=read(min(left,1024*1024));left-=len(b)
   if out:out.write(b)
  if out:out.close()
  read((-size)%4)
 f.read();err=p.stderr.read();assert p.wait()==0,err;assert found==names,(found,names)

def selftests():
 def arc(date=b'1',body=b'ABCD'):
  return b'!<arch>\n'+b'x.o/            '+date.ljust(12)+b'0     0     100644  '+str(len(body)).encode().ljust(10)+b'`\n'+body
 class Tests(unittest.TestCase):
  def test_only_date(self):self.assertEqual(date_difference(arc(),arc(b'2'))['classification'],'allowed-ar-date-difference')
  def test_body_or_other_byte(self):
   self.assertEqual(date_difference(arc(),arc(body=b'ABCE'))['classification'],'FAIL')
   x=bytearray(arc());x[40]=ord('1');self.assertEqual(date_difference(arc(),bytes(x))['classification'],'FAIL')
 out=io.StringIO();r=unittest.TextTestRunner(stream=out,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests));(E/'ar-selftests.txt').write_text(out.getvalue());assert r.wasSuccessful(),out.getvalue();print(out.getvalue(),flush=True)

def main():
 selftests();O=E/'rpm-comparison';O.mkdir();rows=[]
 newfiles=sorted((P/'RPMS').glob('*.rpm'))+sorted((P/'SRPMS').glob('*.rpm'));assert len(newfiles)==23
 for new in newfiles:
  free();old=OLD/('SRPMS' if new.name.endswith('.src.rpm') else 'RPMS')/new.name;a,b=manifest(old),manifest(new)
  added=set(b)-set(a);removed=set(a)-set(b)
  expected_add={'usr/lib/debug/usr/bin/clang-22.debug'} if new.name.startswith('clang-debuginfo-') else set()
  assert added==expected_add and not removed,(new.name,added,removed)
  added_rows=[{'path':n,'new':b[n]} for n in sorted(added)]
  if added:
   identity=json.loads((WORK/'identity.json').read_text())
   assert b[next(iter(added))]['sha256']==identity['debug_file']['sha256']
  changes=[];times=[]
  for name in sorted(a):
   x=dict(a[name]);y=dict(b[name]);tx=x.pop('mtime');ty=y.pop('mtime')
   if tx!=ty:times.append({'path':name,'old':tx,'new':ty})
   if x!=y:changes.append({'path':name,'old':x,'new':y})
  allowed={'llvm.spec','clang-bolt-helper.py'} if new.name.endswith('.src.rpm') else {'usr/bin/clang-22'} if new.name.startswith('clang-22.') else set()
  arnames={x['path'] for x in changes if x['path'].endswith('.a')};dest=X/'rpm-differences'/new.name
  if arnames:
   extract_selected(old,arnames,dest/'old');extract_selected(new,arnames,dest/'new')
  contents=[];dates=[];failed=[]
  for x in changes:
   name=x['path'];meta=all(x['old'].get(k)==x['new'].get(k) for k in ['mode','uid','gid','target'])
   if name in allowed and meta:contents.append(x)
   elif name in arnames and meta:
    proof=date_difference((dest/'old'/name).read_bytes(),(dest/'new'/name).read_bytes());x['proof']=proof
    if proof['classification']=='allowed-ar-date-difference':dates.append(x)
    else:failed.append(x)
   else:failed.append(x)
  row={'rpm':new.name,'paths':len(a),'old_sha256':sha(old),'new_sha256':sha(new),'content_changes':contents,'added_files':added_rows,'payload_mtime_changes':times,'ar_date_differences':dates,'unexpected_changes':failed,'PASS':not failed}
  save(O/(new.name+'.json'),{'result':row,'old_files':a,'new_files':b});rows.append(row);save(O/'summary.json',rows)
  print(new.name,'content',len(contents),'mtime',len(times),'ar_dates',len(dates),'unexpected',len(failed),flush=True);assert not failed,(new.name,'unexpected RPM content difference')
 print('RPM23_PASS',flush=True)
if __name__=='__main__':main()
