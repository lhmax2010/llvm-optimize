"""v9 function comparison: ELF64 LE x86-64; relocation masking + separate tuples.
No final clang, no disassembly-text/address normalization. Unknown widths fail closed.
Zero-size symbol ranges are retained and separately reported (no inferred bytes).
"""
from pathlib import Path
import mmap,struct,hashlib,re,json,gzip,collections,bisect
WIDTH={0:0,1:8,2:4,3:4,4:4,5:0,6:8,7:8,8:8,9:4,10:4,11:4,12:2,13:2,14:1,15:1,
16:8,17:8,18:8,19:4,20:4,21:4,22:4,23:4,24:8,25:8,26:4,27:8,28:8,29:8,30:8,31:8,32:4,33:8,
34:4,35:0,36:16,37:8,38:8,41:4,42:4,43:4,44:4,45:4}
def normal(s): return re.sub(r'(?:\.llvm\.[0-9]+)+$','',s)
def sha(data):return hashlib.sha256(data).hexdigest()
class ELF:
 def __init__(self,path):
  self.path=str(path);self.f=open(path,'rb');self.m=mmap.mmap(self.f.fileno(),0,access=mmap.ACCESS_READ)
  m=self.m
  assert m[:6]==b'\x7fELF\x02\x01','ELF64 LE required'
  h=struct.unpack_from('<16sHHIQQQIHHHHHH',m,0)
  self.kind=h[1];assert h[2]==62
  off,ent,count,strings=h[6],h[11],h[12],h[13]
  assert ent==64 and count and strings<count
  self.sections=[]
  for i in range(count):
   a=struct.unpack_from('<IIQQQQIIQQ',m,off+i*ent)
   self.sections.append(dict(index=i,nameoff=a[0],type=a[1],flags=a[2],addr=a[3],offset=a[4],size=a[5],link=a[6],info=a[7],align=a[8],entsize=a[9]))
  st=self.sections[strings]
  for s in self.sections:s['name']=self.string(st,s['nameoff'])
  self.symtabs={}
  for s in self.sections:
   if s['type'] not in (2,11):continue
   assert s['entsize']==24 and s['size']%24==0
   names=self.sections[s['link']];syms=[]
   for pos in range(s['offset'],s['offset']+s['size'],24):
    n,info,other,idx,val,size=struct.unpack_from('<IBBHQQ',m,pos)
    syms.append(dict(name=self.string(names,n),type=info&15,bind=info>>4,other=other,section=idx,value=val,size=size))
   self.symtabs[s['index']]=syms
  tables=[s for s in self.sections if s['type']==2];assert len(tables)==1,'one static symbol table required'
  funcs=[]
  for k,sym in enumerate(self.symtabs[tables[0]['index']]):
   if sym['type'] not in (2,10) or not 0<sym['section']<len(self.sections):continue
   s=self.sections[sym['section']]
   if not s['flags']&4:continue
   start=sym['value'] if self.kind==1 else sym['value']-s['addr']
   assert 0<=start<=s['size'] and start+sym['size']<=s['size'],sym
   funcs.append(dict(sym,index=k,start=start,end=start+sym['size'],section_name=s['name'],normalized_name=normal(sym['name'])))
  self.functions=funcs
  self.relocs=collections.defaultdict(list);self.reloc_census=collections.Counter()
  for s in self.sections:
   if s['type'] not in (4,9) or not 0<s['info']<len(self.sections):continue
   target=self.sections[s['info']]
   if not target['flags']&4:continue
   ent=24 if s['type']==4 else 16
   assert s['entsize']==ent and s['size']%ent==0
   for pos in range(s['offset'],s['offset']+s['size'],ent):
    offset,info=struct.unpack_from('<QQ',m,pos);typ=info&0xffffffff;si=info>>32
    assert typ in WIDTH,('unknown width',typ)
    width=WIDTH[typ];relative=offset if self.kind==1 else offset-target['addr']
    assert 0<=relative<=target['size'] and relative+width<=target['size']
    symbol=self.symtabs[s['link']][si]
    symbol_name=symbol['name']
    if not symbol_name and symbol['type']==3:symbol_name='SECTION:'+self.sections[symbol['section']]['name']
    addend=struct.unpack_from('<q',m,pos+16)[0] if s['type']==4 else int.from_bytes(m[target['offset']+relative:target['offset']+relative+width],'little',signed=True)
    self.relocs[s['info']].append((relative,typ,normal(symbol_name),addend,width))
    self.reloc_census[str(typ)]+=1
  for rels in self.relocs.values():rels.sort()
  self.positions={k:[r[0] for r in rs] for k,rs in self.relocs.items()}
 def string(self,section,off):
  assert 0<=off<section['size']
  begin=section['offset']+off;end=self.m.find(b'\0',begin,section['offset']+section['size'])
  assert end>=begin
  return self.m[begin:end].decode('utf-8','surrogateescape')
 def records(self):
  groups=collections.defaultdict(list)
  for f in self.functions:groups[(f['normalized_name'],f['section_name'])].append(f)
  out={}
  for (name,section),fs in groups.items():
   for ordinal,f in enumerate(sorted(fs,key=lambda x:(x['start'],x['index']))):
    sec=self.sections[f['section']];data=bytearray(self.m[sec['offset']+f['start']:sec['offset']+f['end']])
    rels=self.relocs.get(f['section'],[]);positions=self.positions.get(f['section'],[])
    left=bisect.bisect_left(positions,f['start']);right=bisect.bisect_left(positions,f['end'])
    normalized=[]
    # No relocation field may straddle a function boundary.
    for rel in rels[max(0,left-1):right]:
     at,typ,symbol,addend,width=rel
     if at<f['start']:
      assert at+width<=f['start'],('crossing start',f,rel)
      continue
     assert at+width<=f['end'],('crossing end',f,rel)
     data[at-f['start']:at-f['start']+width]=b'\0'*width
     normalized.append((at-f['start'],typ,symbol,addend))
    out[(name,section,ordinal)]={'name':f['name'],'normalized_name':name,'section':section,'ordinal':ordinal,'address':f['value'],'size':f['size'],'symbol_index':f['index'],'symbol_type':f['type'],'raw_sha256':sha(self.m[sec['offset']+f['start']:sec['offset']+f['end']]),'masked_sha256':sha(data),'relocations':normalized}
  return out
 def close(self):self.m.close();self.f.close()
def compare(left,right,destination):
 a=ELF(left);b=ELF(right);ar=a.records();br=b.records()
 counts=collections.Counter();differences=[]
 for key in sorted(set(ar)|set(br)):
  x=ar.get(key);y=br.get(key)
  if x is None:cat='only_right'
  elif y is None:cat='only_left'
  elif x['size']!=y['size'] or x['masked_sha256']!=y['masked_sha256']:cat='machine_code_different'
  elif x['relocations']==y['relocations']:cat='identical'
  elif [(r[0],r[1]) for r in x['relocations']]==[(r[0],r[1]) for r in y['relocations']]:cat='relocation_target_or_addend_only'
  else:cat='relocation_structure_only'
  counts[cat]+=1
  if cat!='identical':differences.append({'key':key,'category':cat,'left':x,'right':y})
 result={'left':str(left),'right':str(right),'left_functions':len(ar),'right_functions':len(br),'counts':dict(counts),'left_zero_size':sum(r['size']==0 for r in ar.values()),'right_zero_size':sum(r['size']==0 for r in br.values()),'left_relocation_census':dict(a.reloc_census),'right_relocation_census':dict(b.reloc_census),'left_debug_sections':[s['name'] for s in a.sections if s['name'].startswith(('.debug','.zdebug'))],'right_debug_sections':[s['name'] for s in b.sections if s['name'].startswith(('.debug','.zdebug'))]}
 dest=Path(destination);dest.mkdir(exist_ok=False,parents=True)
 (dest/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
 with gzip.open(dest/'differences.json.gz','wt') as f:json.dump(differences,f)
 for label,recs in [('left',ar),('right',br)]:
  with gzip.open(dest/(label+'-functions.json.gz'),'wt') as f:json.dump(list(recs.values()),f)
 a.close();b.close();return result
if __name__=='__main__':
 import sys
 print(json.dumps(compare(*sys.argv[1:]),indent=2))
