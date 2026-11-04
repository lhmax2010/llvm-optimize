from common import *
import struct,zlib,subprocess
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for data in iter(lambda:f.read(1048576),b''):h.update(data)
 return h.hexdigest()
def layout(p):
 with p.open('rb') as f:
  h=f.read(64);assert h[:6]==b'\x7fELF\x02\x01';po=struct.unpack_from('<Q',h,32)[0];ps,pn=struct.unpack_from('<HH',h,54);f.seek(po);ph=f.read(ps*pn)
  off=struct.unpack_from('<Q',h,40)[0];sz,n,si=struct.unpack_from('<HHH',h,58);f.seek(off);raw=f.read(sz*n);ss=[struct.unpack_from('<IIQQQQIIQQ',raw,i*sz) for i in range(n)];s=ss[si];f.seek(s[4]);names=f.read(s[5]);out=[]
  for s in ss:out.append(dict(name=names[s[0]:].split(b'\0')[0].decode(),offset=s[4],size=s[5],type=s[1],flags=s[2]))
 return h,ph,raw,out
res={}
for bid,proj in [(1216409,'toolchain'),(1216410,'basedev')]:
 work=W/f'temp/night-20261103/{proj}/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt'
 for name,rel in [('clang.candidate','usr/bin/clang-22')]+([('clang-22.debug','usr/lib/debug/usr/bin/clang-22.debug')] if proj=='toolchain' else []):
  local=work/name;qb=D/str(bid)/'extracted'/rel
  lh,lp,ls,lt=layout(local);qh,qp,qs,qt=layout(qb);r={'local_path':str(local),'qb_path':str(qb),'local_bytes':local.stat().st_size,'qb_bytes':qb.stat().st_size,'local_sha256':sha(local),'qb_sha256':sha(qb),'elf_header_equal':lh==qh,'program_headers_equal':lp==qp,'section_headers_equal':ls==qs,'changed_bytes':0,'ranges':[]}
  def section(off,table):return next((s['name'] for s in table if s['type']!=8 and s['offset']<=off<s['offset']+s['size']),'ELF headers/padding/outside sections')
  active=None;pos=0
  with local.open('rb') as a,qb.open('rb') as b:
   while True:
    x=a.read(1048576);y=b.read(1048576)
    if not x and not y:break
    if x!=y:
     for i in range(max(len(x),len(y))):
      if x[i:i+1]==y[i:i+1]:continue
      off=pos+i;label=section(off,qt);r['changed_bytes']+=1
      if active is None or active['end_inclusive']+1!=off or active['qb_section']!=label:
       active={'start':off,'end_inclusive':off,'local_section':section(off,lt),'qb_section':label,'local_hex':'','qb_hex':''};r['ranges'].append(active)
      active['end_inclusive']=off;active['local_hex']+=x[i:i+1].hex();active['qb_hex']+=y[i:i+1].hex()
    pos+=max(len(x),len(y))
  r['all_other_bytes_equal']=True
  # ELF dynamic/RUNPATH/debuglink originals are saved.
  for side,p in [('local',local),('qb',qb)]:
   for flag in ['-SW','-dW']:
    z=subprocess.run(['readelf',flag,str(p)],capture_output=True);save(f'{bid}/{name}-{side}-{flag[1:]}.txt',z.stdout+z.stderr)
  if name=='clang.candidate':
   s=next((s for s in qt if s['name']=='.gnu_debuglink'),None)
   if s:
    with qb.open('rb') as f:f.seek(s['offset']);data=f.read(s['size'])
    crc=struct.unpack('<I',data[-4:])[0];debug=D/str(bid)/'extracted/usr/lib/debug/usr/bin/clang-22.debug';actual=0
    with debug.open('rb') as f:
     for b in iter(lambda:f.read(1048576),b''):actual=zlib.crc32(b,actual)
    r['debuglink']={'name':data.split(b'\0')[0].decode(),'crc32':crc,'debug_file_crc32':actual,'crc_equal':crc==actual}
   else:r['debuglink']=None
  res[f'{bid}/{name}']=r;save(f'{bid}/{name}-byte-diff.json',json.dumps(r,indent=2)+'\n');print(bid,name,{k:r[k] for k in ['local_sha256','qb_sha256','changed_bytes']},'ranges',len(r['ranges']),flush=True)
(E/'binary-comparison.json').write_text(json.dumps(res,indent=2)+'\n')
