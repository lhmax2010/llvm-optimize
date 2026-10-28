from pathlib import Path
import urllib.request,urllib.parse,re,json,struct,gzip,lzma,bz2,hashlib,time,xml.etree.ElementTree as X
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';E=B/'tools/bolt/results/qb-fail-20261028/meta/buildconf';D=Path(__file__).resolve().parent
url='https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261013.024319/repos/standard/source/'
html=(E/'source-index-1.html').read_text();links=sorted(set(re.findall(r'href="([^"]+\.src\.rpm)"',html)))
(E/'srpm-list.txt').write_text('\n'.join(links)+'\n');print('SRPMs',len(links),flush=True)
class Count:
 def __init__(self,r):self.r=r;self.n=0;self.h=hashlib.sha256()
 def read(self,n=-1):
  b=self.r.read(n);self.n+=len(b);self.h.update(b);return b
 def seekable(self):return False
 def readable(self):return True
 def seek(self,*a):raise OSError('no seek')
def exact(f,n):
 out=bytearray()
 while len(out)<n:
  s=f.read(n-len(out))
  if not s:raise EOFError(f'expected {n}, got {len(out)}')
  out+=s
 return bytes(out)
def header(f):
 raw=exact(f,16);assert raw[:4]==b'\x8e\xad\xe8\x01'
 count,size=struct.unpack('>II',raw[8:]);idx=exact(f,count*16);data=exact(f,size);tags={}
 for i in range(count):
  tag,typ,off,n=struct.unpack_from('>IIII',idx,i*16)
  if typ in (6,8,9):tags[tag]=data[off:].split(b'\0',n)[:n]
 return tags,16+count*16+size
rows=[]
for ix,link in enumerate(links):
 dest=E/'specs'/link.removesuffix('.src.rpm');dest.mkdir(parents=True,exist_ok=True)
 cached=dest/'provenance.json'
 if cached.exists():rows.append(json.loads(cached.read_text()));continue
 row={'srpm':link,'url':urllib.parse.urljoin(url,link),'specs':[]}
 try:
  with urllib.request.urlopen(row['url'],timeout=90) as response:
   row['content_length']=response.headers.get('Content-Length');f=Count(response);assert exact(f,96)[:4]==b'\xed\xab\xee\xdb'
   _,n=header(f);exact(f,(-n)%8);tags,_=header(f)
   compressor=tags[1125][0].decode();files=tags.get(1117,[]);wanted=sum(x.endswith(b'.spec') for x in files);assert wanted>0
   row['compressor']=compressor;row['header_spec_names']=[x.decode() for x in files if x.endswith(b'.spec')]
   if compressor=='xz':stream=lzma.LZMAFile(f)
   elif compressor=='gzip':stream=gzip.GzipFile(fileobj=f)
   elif compressor=='bzip2':stream=bz2.BZ2File(f)
   else:raise ValueError('unsupported '+compressor)
   while len(row['specs'])<wanted:
    h=exact(stream,110);assert h[:6] in (b'070701',b'070702');v=[int(h[j:j+8],16) for j in range(6,110,8)];size,ns=v[6],v[11];name=exact(stream,ns).rstrip(b'\0').decode();exact(stream,(-(110+ns))%4)
    if name=='TRAILER!!!':break
    if name.endswith('.spec'):
     data=exact(stream,size);p=dest/Path(name).name;p.write_bytes(data);row['specs'].append({'file':str(p.relative_to(E)),'member':name,'bytes':size,'sha256':hashlib.sha256(data).hexdigest()})
    else:
     remaining=size
     while remaining:
      got=exact(stream,min(remaining,1048576));remaining-=len(got)
    exact(stream,(-size)%4)
   row.update(status='ok',bytes_received=f.n,download_prefix_sha256=f.h.hexdigest(),note='streamed SRPM payload until all .spec members; prefix SHA is NOT a full RPM SHA')
 except Exception as ex:row.update(status='error',error=repr(ex))
 cached.write_text(json.dumps(row,indent=2)+'\n');rows.append(row)
 (E/'spec-acquisition.json').write_text(json.dumps(rows,indent=2)+'\n')
 print(ix+1,link,row['status'],row.get('bytes_received'),row.get('error',''),flush=True)
print('DONE',len(rows),'errors',sum(x['status']!='ok' for x in rows),flush=True)
