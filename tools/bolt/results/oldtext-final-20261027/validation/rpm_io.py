from common import *
import stat
def manifest(rpm):
    p=subprocess.Popen(['rpm2cpio',str(rpm)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    f=p.stdout;rows={};hard={};pending=[]
    def read(n):
        b=b''
        while len(b)<n:
            c=f.read(n-len(b));assert c,'short cpio read';b+=c
        return b
    while True:
        header=read(110);assert header[:6] in (b'070701',b'070702')
        v=[int(header[6+8*i:14+8*i],16) for i in range(13)]
        ino,mode,uid,gid,nlink,mtime,size,maj,min_,rmaj,rmin,namesize,check=v
        name=read(namesize).rstrip(b'\0').decode();read((-110-namesize)%4)
        if name=='TRAILER!!!':break
        hh=hashlib.sha256();remaining=size;link=b''
        while remaining:
            data=read(min(remaining,1024*1024));hh.update(data);remaining-=len(data)
            if stat.S_ISLNK(mode):link+=data
        read((-size)%4);name=name.removeprefix('./')
        row={'mode':mode,'uid':uid,'gid':gid,'bytes':size,'sha256':hh.hexdigest(),'mtime':mtime}
        if stat.S_ISLNK(mode):row['target']=link.decode()
        if stat.S_ISREG(mode) and nlink>1:
            key=(maj,min_,ino);pending.append((name,key))
            if size or key not in hard:hard[key]=(size,hh.hexdigest())
        rows[name]=row
    f.read();stderr=p.stderr.read();assert p.wait()==0,stderr
    for name,key in pending:rows[name]['bytes'],rows[name]['sha256']=hard[key]
    return rows
