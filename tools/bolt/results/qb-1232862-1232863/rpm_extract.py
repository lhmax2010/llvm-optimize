"""Extract selected regular payloads into a NEW scratch tree; resolve cpio hardlinks."""
from pathlib import Path
import subprocess,hashlib,stat
import os,shutil

def extract_selected(rpm,names,dest):
 dest=Path(dest);dest.mkdir(parents=True,exist_ok=True);tmp=dest/('.cpio-'+hashlib.sha256(str(rpm).encode()).hexdigest()[:16]);tmp.mkdir(exist_ok=False)
 p=subprocess.Popen(['rpm2cpio',str(rpm)],stdout=subprocess.PIPE,stderr=subprocess.PIPE);f=p.stdout
 def read(n):
  b=b''
  while len(b)<n:
   x=f.read(n-len(b));assert x,'short cpio read';b+=x
  return b
 found=set();groups={};pending=[]
 while True:
  hd=read(110);assert hd[:6] in (b'070701',b'070702');v=[int(hd[6+8*i:14+8*i],16) for i in range(13)];ino,mode,uid,gid,nlink,mtime,size,maj,min_,rmaj,rmin,namesize,check=v
  name=read(namesize).rstrip(b'\0').decode().removeprefix('./');read((-110-namesize)%4)
  if name=='TRAILER!!!':break
  selected=name in names;target=dest/name;assert not Path(name).is_absolute() and '..' not in Path(name).parts
  key=(maj,min_,ino);out=None
  if stat.S_ISREG(mode) and nlink>1:
   if selected:pending.append((name,key));found.add(name)
   if size:
    body=tmp/('-'.join(map(str,key)));out=body.open('xb');groups[key]=body
  elif selected:
   assert stat.S_ISREG(mode),'selected payload is not a regular file';target.parent.mkdir(parents=True,exist_ok=True);out=target.open('xb');found.add(name)
  left=size
  while left:
   b=read(min(left,1024*1024));left-=len(b)
   if out:out.write(b)
  if out:out.close()
  read((-size)%4)
 f.read();err=p.stderr.read();assert p.wait()==0,err
 for name,key in pending:
  target=dest/name;target.parent.mkdir(parents=True,exist_ok=True)
  if key in groups:os.link(groups[key],target)
  else:target.touch(exist_ok=False)
 assert found==names,(found,names)
