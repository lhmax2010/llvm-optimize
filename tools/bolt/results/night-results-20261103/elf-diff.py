from pathlib import Path
import struct,hashlib,json,zlib
E=Path(__file__).parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize');base=W/'temp/debuglink-20261028/full-20261030/products/binaries/clang.candidate';new=W/'temp/night-20261103/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt/clang.candidate'
def layout(p):
 with p.open('rb') as f:
  h=f.read(64);assert h[:6]==b'\x7fELF\x02\x01';off=struct.unpack_from('<Q',h,40)[0];sz,n,si=struct.unpack_from('<HHH',h,58);f.seek(off);raw=f.read(sz*n);sections=[struct.unpack_from('<IIQQQQIIQQ',raw,i*sz) for i in range(n)];s=sections[si];f.seek(s[4]);names=f.read(s[5]);out=[]
  for s in sections:
   name=names[s[0]:].split(b'\0')[0].decode();out.append(dict(name=name,offset=s[4],size=s[5],type=s[1],flags=s[2]))
  return h,raw,out
ha,sa,aa=layout(base);hb,sb,bb=layout(new);changes=[];hashes=[hashlib.sha256(),hashlib.sha256()];pos=0
with base.open('rb') as a,new.open('rb') as b:
 while True:
  x=a.read(1048576);y=b.read(1048576)
  if not x and not y:break
  hashes[0].update(x);hashes[1].update(y)
  if x!=y:
   for j in range(max(len(x),len(y))):
    old=x[j:j+1];newb=y[j:j+1]
    if old!=newb:changes.append(dict(offset=pos+j,before=old.hex(),after=newb.hex(),section=next((s['name'] for s in bb if s['type']!=8 and s['offset']<=pos+j<s['offset']+s['size']),None)))
  pos+=len(x)
r=dict(baseline=str(base),candidate=str(new),baseline_bytes=base.stat().st_size,candidate_bytes=new.stat().st_size,baseline_sha256=hashes[0].hexdigest(),candidate_sha256=hashes[1].hexdigest(),elf_header_equal=ha==hb,section_headers_equal=sa==sb,all_changed_bytes=changes,changed_count=len(changes),all_other_bytes_equal=True)
for label,p,secs in [('baseline',base,aa),('candidate',new,bb)]:
 s=next(s for s in secs if s['name']=='.gnu_debuglink')
 with p.open('rb') as f:f.seek(s['offset']);data=f.read(s['size'])
 r[label+'_debuglink']=dict(**s,hex=data.hex(),crc32=struct.unpack('<I',data[-4:])[0])
(E/'toolchain-final-byte-diff.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
