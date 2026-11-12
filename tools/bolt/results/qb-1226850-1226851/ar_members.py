import mmap,hashlib
def members(p):
 out=[];names=b'';index=0
 with p.open('rb') as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as mm:
  assert mm[:8]==b'!<arch>\n';at=8
  while at<len(mm):
   hd=mm[at:at+60];assert len(hd)==60 and hd[58:60]==bytes([96,10])
   size=int(hd[48:58]);start=at+60;end=start+size;assert end<=len(mm)
   raw=hd[:16].strip();name=raw.decode()
   if raw==b'//':names=mm[start:end]
   elif raw.startswith(b'/') and raw[1:].isdigit():
    no=int(raw[1:]);ne=names.find(b'/\n',no);assert ne>=no;name=names[no:ne].decode()
   elif raw.startswith(b'#1/'):
    nn=int(raw[3:]);name=mm[start:start+nn].rstrip(b'\0').decode();start+=nn
   elif raw not in (b'/',b'/SYM64/'):name=name.rstrip('/')
   h=hashlib.sha256()
   for pos in range(start,end,1024*1024):h.update(mm[pos:min(end,pos+1024*1024)])
   out.append(dict(index=index,name=name,bytes=end-start,sha256=h.hexdigest(),date=hd[16:28].decode().strip(),uid=hd[28:34].decode().strip(),gid=hd[34:40].decode().strip(),mode=hd[40:48].decode().strip()))
   index+=1;at=end+(size%2)
  assert at==len(mm)
 return out
