"""Hash each RPM payload entry by streaming newc; no unpacked tree is written."""
import hashlib,json,stat,subprocess,sys
from pathlib import Path

def exact(f,n):
    out=bytearray()
    while len(out)<n:
        data=f.read(n-len(out))
        if not data:raise ValueError('truncated cpio payload')
        out.extend(data)
    return bytes(out)

def inventory(path):
    p=subprocess.Popen(['rpm2cpio',str(path)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    rows=[];groups={}
    try:
        while True:
            h=exact(p.stdout,110)
            if h[:6] not in (b'070701',b'070702'):raise ValueError('unknown cpio format')
            v=[int(h[6+i*8:14+i*8],16) for i in range(13)]
            ino,mode,uid,gid,links,mtime,size,major,minor,rmaj,rmin,ns,crc=v
            name=exact(p.stdout,ns)[:-1].decode('utf-8');exact(p.stdout,(-110-ns)%4)
            if name=='TRAILER!!!':break
            left=size;sha=hashlib.sha256();target=bytearray()
            while left:
                data=exact(p.stdout,min(left,1024*1024));sha.update(data);left-=len(data)
                if stat.S_ISLNK(mode):target.extend(data)
            exact(p.stdout,(-size)%4)
            key=(major,minor,ino)
            row={'path':name[2:] if name.startswith('./') else name,'mode':mode,'uid':uid,'gid':gid,'mtime':mtime,'size':size,'nlink':links,'sha256':sha.hexdigest() if stat.S_ISREG(mode) else None}
            if stat.S_ISLNK(mode):row['target']=target.decode('utf-8')
            if stat.S_ISREG(mode) and links>1:
                groups.setdefault(key,[]).append(row)
            rows.append(row)
        # Drain padding before waiting, so a full stdout pipe cannot deadlock.
        while p.stdout.read(1024*1024):pass
        err=p.stderr.read().decode();rc=p.wait()
        if rc:raise RuntimeError('rpm2cpio rc='+str(rc)+' '+err)
        for members in groups.values():
            populated=[x for x in members if x['size']>0]
            if populated:
                content=populated[0]
                assert all(x['sha256']==content['sha256'] and x['size']==content['size'] for x in populated)
                for row in members:row.update(size=content['size'],sha256=content['sha256'])
        return sorted(rows,key=lambda x:x['path'])
    finally:
        if p.poll() is None:p.kill();p.wait()

if __name__=='__main__':
    root=Path(sys.argv[1]);output=Path(sys.argv[2]);output.mkdir(parents=True,exist_ok=True)
    for rpm in sorted(root.rglob('*.rpm')):
        print(str(rpm),flush=True)
        rows=inventory(rpm);(output/(rpm.name+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
