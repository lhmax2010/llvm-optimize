"""User-approved record-section exceptions, with strict structural/byte proofs.

No ALLOC content or symbol table is excluded. Files are mapped read-only and
large equal sections are compared in bounded chunks. This is local validation,
not release packaging policy.
"""
from pathlib import Path
import struct,hashlib,mmap,collections,re
RECORDS={'.GCC.command.line','.llvmcmd','.comment'}
def chunk_equal(a,b):
 if len(a)!=len(b):return False
 return all(bytes(a[i:i+1048576])==bytes(b[i:i+1048576]) for i in range(0,len(a),1048576))
def digest(a):
 h=hashlib.sha256()
 for i in range(0,len(a),1048576):h.update(a[i:i+1048576])
 return h.hexdigest()
def strings(a):
 raw=bytes(a);assert not raw or raw.endswith(b'\0'),'unterminated record strings'
 return collections.Counter(x.decode('utf-8',errors='strict') for x in raw.split(b'\0') if x)
def comment(a):
 c=strings(a);bad=[s for s in c if not any(re.fullmatch(p,s) for p in [r'clang version [^\r\n]+',r'(?:Apple |Ubuntu |Debian )?clang version [^\r\n]+',r'Linker: (?:LLD|GNU ld|GNU gold) [^\r\n]+',r'GCC: \([^\r\n]+\) [^\r\n]+'])]
 assert not bad,('non-identifier .comment strings',bad)
 return dict(c)
def layout(data):
 a=memoryview(data);assert bytes(a[:6]) in (b'\x7fELF\x02\x01',b'\x7fELF\x01\x01'),'ELF LE32/64 required'
 wide=a[4]==2;fmt='<HHIQQQIHHHHHH' if wide else '<HHIIIIIHHHHHH';h=struct.unpack_from(fmt,a,16)
 # type,machine,version,entry,phoff,shoff,flags,ehsize,phentsize,phnum,shentsize,shnum,shstrndx
 shfmt='<IIQQQQIIQQ' if wide else '<IIIIIIIIII';shlen=struct.calcsize(shfmt);assert h[10]==shlen and h[11]>0 and h[12]<h[11]
 assert h[5]+h[10]*h[11]<=len(a);ss=[struct.unpack_from(shfmt,a,h[5]+i*shlen) for i in range(h[11])];names=bytes(a[ss[h[12]][4]:ss[h[12]][4]+ss[h[12]][5]]);rows=[]
 for i,s in enumerate(ss):
  assert s[0]<len(names);end=names.find(b'\0',s[0]);assert end>=0
  name=names[s[0]:end].decode();assert s[1]==8 or s[4]+s[5]<=len(a)
  rows.append({'index':i,'name':name,'raw':s,'offset':s[4],'size':s[5],'type':s[1],'flags':s[2],'content':a[s[4]:s[4]+s[5]] if s[1]!=8 else a[0:0]})
 assert len({s['name'] for s in rows})==len(rows),'duplicate section names'
 return a,h,rows

def elf_proof(old,new):
 a,ha,sa=layout(old);b,hb,sb=layout(new);changes=[];proofs=[]
 assert bytes(a[:16])==bytes(b[:16]),'ELF identification changed'
 for i,(x,y) in enumerate(zip(ha,hb)):
  if x!=y:assert i==5,('ELF header changed',i,x,y);changes.append(dict(field='e_shoff',old=x,new=y))
 assert len(sa)==len(sb),'section count changed'
 assert chunk_equal(a[ha[4]:ha[4]+ha[8]*ha[9]],b[hb[4]:hb[4]+hb[8]*hb[9]]),'program headers changed'
 changed_records=[]
 for x,y in zip(sa,sb):
  assert x['name']==y['name'],('section name/order changed',x['name'],y['name'])
  name=x['name'];record=name in RECORDS
  assert all(u==v for i,(u,v) in enumerate(zip(x['raw'],y['raw'])) if i not in (4,5)),('section metadata changed',name)
  same=chunk_equal(x['content'],y['content'])
  if x['flags']&2:assert x['offset']==y['offset'] and x['size']==y['size'] and same,('ALLOC section changed',name)
  if not record:assert x['size']==y['size'] and same,('non-record section changed',name)
  if record:
   assert not x['flags']&2,('record section is ALLOC',name)
   row=dict(section=name,old_offset=x['offset'],new_offset=y['offset'],old_bytes=x['size'],new_bytes=y['size'],old_sha256=digest(x['content']),new_sha256=digest(y['content']),content_equal=same)
   if name=='.comment':row.update(old_strings=comment(x['content']),new_strings=comment(y['content']))
   if name=='.GCC.command.line':
    c,d=strings(x['content']),strings(y['content']);row.update(string_multisets_equal=c==d,old_unique=len(c),new_unique=len(d),old_total=sum(c.values()),new_total=sum(d.values()),order_only_difference=(not same and c==d),string_changes=[dict(string=s,old_count=c.get(s,0),new_count=d.get(s,0)) for s in sorted(c.keys()|d.keys()) if c.get(s,0)!=d.get(s,0)])
   proofs.append(row)
   if not same or x['size']!=y['size']:changed_records.append((x,y))
  if x['size']!=y['size']:assert record,('size changed outside records',name);changes.append(dict(section=name,field='sh_size',old=x['size'],new=y['size']))
 for x,y in zip(sa,sb):
  if x['offset']!=y['offset']:
   assert not x['flags']&2 and any(x['offset']>=u['offset']+u['size'] and y['offset']>=v['offset']+v['size'] for u,v in changed_records),('unexplained section relocation',x['name'])
   changes.append(dict(section=x['name'],field='sh_offset',old=x['offset'],new=y['offset']))
 if len(a)!=len(b):assert changed_records,'unexplained length';changes.append(dict(field='file_length',old=len(a),new=len(b)))
 if ha[5]!=hb[5]:assert any(ha[5]>=u['offset']+u['size'] and hb[5]>=v['offset']+v['size'] for u,v in changed_records),'unexplained section table relocation'
 # Check ALL bytes outside the ELF/program/section headers and section bodies.
 # Relocated alignment padding may change length only when a record resized,
 # and then must be all zero on both sides. Nonzero opaque gaps remain strict.
 def gaps(buf,h,ss):
  spans=[(0,h[7]),(h[4],h[4]+h[8]*h[9]),(h[5],h[5]+h[10]*h[11])]+[(s['offset'],s['offset']+s['size']) for s in ss if s['type']!=8 and s['size']]
  end=0;out=[]
  for lo,hi in sorted(spans):
   if lo>end:out.append((end,lo,buf[end:lo]))
   end=max(end,hi)
  if end<len(buf):out.append((end,len(buf),buf[end:]))
  return out
 ga,gb=gaps(a,ha,sa),gaps(b,hb,sb)
 na=[(lo,hi,v) for lo,hi,v in ga if any(v)];nb=[(lo,hi,v) for lo,hi,v in gb if any(v)]
 assert len(na)==len(nb) and all(chunk_equal(x[2],y[2]) for x,y in zip(na,nb)),'non-section bytes changed'
 if not changed_records:assert [(x,y) for x,y,_ in ga]==[(x,y) for x,y,_ in gb],'padding layout changed without record change'
 return dict(classification='identical' if chunk_equal(a,b) else 'command-record-sections-only',record_sections=proofs,structural_changes=changes,all_other_sections_equal=True,program_headers_equal=True,all_ALLOC_equal=True,padding=[{'old':[(lo,hi) for lo,hi,_ in ga],'new':[(lo,hi) for lo,hi,_ in gb],'nonzero_gaps_equal':True}])

def ar_members(data):
 a=memoryview(data);assert bytes(a[:8])==b'!<arch>\n';pos=8;names=b'';out=[]
 while pos<len(a):
  h=bytes(a[pos:pos+60]);assert len(h)==60 and h[-2:]==b'`\n';size=int(h[48:58]);body=a[pos+60:pos+60+size];assert len(body)==size
  raw=h[:16].decode().strip();name=raw
  if raw=='//':names=bytes(body)
  elif raw.startswith('/') and raw[1:].isdigit():at=int(raw[1:]);end=names.find(b'/\n',at);assert end>=at;name=names[at:end].decode()
  elif raw not in ('/','/SYM64/'):name=raw.rstrip('/')
  out.append(dict(name=name,offset=pos,size=size,header=h,body=body,pad=bytes(a[pos+60+size:pos+60+size+size%2])))
  pos+=60+size+size%2
 assert pos==len(a);return out

def archive_proof(a,b):
 aa,bb=ar_members(a),ar_members(b);assert [m['name'] for m in aa]==[m['name'] for m in bb],'archive member names/order changed'
 dates=[];sizes=[];proofs=[];hashes=[]
 for x,y in zip(aa,bb):
  assert x['header'][:16]==y['header'][:16] and x['header'][28:48]==y['header'][28:48] and x['header'][58:]==y['header'][58:],'non-date/size archive header changed'
  if x['header'][16:28]!=y['header'][16:28]:dates.append(dict(member=x['name'],old_offset=x['offset']+16,new_offset=y['offset']+16,old=x['header'][16:28].decode(),new=y['header'][16:28].decode()))
  if x['header'][48:58]!=y['header'][48:58]:sizes.append(dict(member=x['name'],field='ar_size',old=x['header'][48:58].decode(),new=y['header'][48:58].decode()))
  equal=chunk_equal(x['body'],y['body']);hashes.append(dict(name=x['name'],old_sha=digest(x['body']),new_sha=digest(y['body'])))
  if not equal:
   assert bytes(x['body'][:4])==b'\x7fELF',('non-ELF member changed (including archive index)',x['name'])
   proofs.append(dict(member=x['name'],old_member_offset=x['offset'],new_member_offset=y['offset'],**elf_proof(x['body'],y['body'])))
  else:assert x['size']==y['size']
  if x['pad']!=y['pad']:assert x['size']!=y['size'] and x['pad'] in (b'',b'\n') and y['pad'] in (b'',b'\n'),'archive padding changed'
 return dict(classification='ar-command-record-difference' if proofs else 'allowed-ar-date-difference' if dates else 'identical',member_order_equal=True,member_content_sha_equal=not proofs,all_non_date_bytes_equal=not proofs and not sizes,date_fields=dates,size_fields=sizes,command_byte_proofs=proofs,members=hashes)

def content_proof(a,b):
 if bytes(a[:8])==b'!<arch>\n':return archive_proof(a,b)
 if bytes(a[:4])==b'\x7fELF':return elf_proof(a,b)
 assert chunk_equal(a,b),'non-ELF file content changed';return dict(classification='identical')
def file_proof(a,b):
 with Path(a).open('rb') as x,Path(b).open('rb') as y:
  if not Path(a).stat().st_size or not Path(b).stat().st_size:return content_proof(x.read(),y.read())
  with mmap.mmap(x.fileno(),0,access=mmap.ACCESS_READ) as xx,mmap.mmap(y.fileno(),0,access=mmap.ACCESS_READ) as yy:
   error=None;kind=AssertionError
   try:answer=content_proof(xx,yy)
   except Exception as exc:error=str(exc);kind=type(exc);exc.__traceback__=None
  if error is not None:raise kind(error)
  return answer
