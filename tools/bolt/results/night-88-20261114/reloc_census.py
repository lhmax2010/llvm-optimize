import collections,datetime,hashlib,json,mmap,re,struct
from pathlib import Path
E=Path(__file__).resolve().parent
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
names={int(n):s for s,n in re.findall(r'ELF_RELOC\((\w+),\s*(\d+)\)',(E/'x86_64.def').read_text())}
supported={1,2,4,9,10,11,12,14,15,22,23,24,29,41,42}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def run(project,expected,size):
 p=W/'temp/local-full-r6-20261111-materials'/project/'reference-relocs-clang-22'
 digest=sha(p);assert digest==expected and p.stat().st_size==size,'input identity mismatch'
 with p.open('rb') as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as m:
  assert m[:6]==b'\x7fELF\x02\x01'
  h=struct.unpack_from('<HHIQQQIHHHHHH',m,16);assert h[1]==62 and h[0] in (2,3)
  off,ent,num,strings=h[5],h[10],h[11],h[12]
  secs=[dict(zip(('nameoff','type','flags','addr','offset','size','link','info','align','entsize'),struct.unpack_from('<IIQQQQIIQQ',m,off+i*ent))) for i in range(num)]
  def string(s,o):
   start=s['offset']+o;end=m.find(b'\0',start,s['offset']+s['size']);assert end>=start
   return m[start:end].decode('utf-8','replace')
  for s in secs:s['name']=string(secs[strings],s['nameoff'])
  def rels(s):
   assert s['entsize'] in (16,24) and s['size']%s['entsize']==0
   for o in range(s['offset'],s['offset']+s['size'],s['entsize']):
    a,i=struct.unpack_from('<QQ',m,o);yield a,i&0xffffffff,i>>32
  tags={}
  for s in secs:
   if s['type']==6:
    for o in range(s['offset'],s['offset']+s['size'],16):
     t,v=struct.unpack_from('<qQ',m,o)
     if t==0:break
     tags[t]=v
  dynamic=set();dynamic_sources=[]
  for tag,sizetag in ((7,8),(23,2)):
   if tags.get(sizetag,0):
    ds=next(s for s in secs if s['addr']==tags[tag]);assert ds['type'] in (4,9)
    assert tags[sizetag] in (ds['size'],ds['size']+tags.get(2,0))
    dynamic.update(a for a,t,_ in rels(ds) if t!=0);dynamic_sources.append(ds['name'])
  if not tags.get(8,0) and not tags:
   for s in secs:
    if s['name']=='.rela.dyn':dynamic.update(a for a,t,_ in rels(s) if t!=0);dynamic_sources.append(s['name'])
  if tags.get(35,0):
   ds=next(s for s in secs if s['addr']==tags[36]);assert ds['size']==tags[35] and tags[37]==8
   addr=0
   for o in range(ds['offset'],ds['offset']+ds['size'],8):
    v=struct.unpack_from('<Q',m,o)[0]
    if not v&1:dynamic.add(v);addr=v+8
    else:
     for bit in range(1,64):
      if v&(1<<bit):dynamic.add(addr+(bit-1)*8)
     addr+=63*8
   dynamic_sources.append(ds['name'])
  filters=collections.Counter();counts=collections.Counter();examples={}
  for s in secs:
   if s['type'] not in (4,9):continue
   n=s['size']//s['entsize']
   if s['flags']&2:filters['relocation_section_ALLOC']+=n;continue
   tsec=secs[s['info']]
   if not tsec['flags']&2:filters['target_nonALLOC']+=n;continue
   if tsec['name'] in ('.plt','.rela.plt','.got.plt','.eh_frame','.gcc_except_table'):filters['target_special']+=n;continue
   for a,typ,sym in rels(s):
    if typ==0:filters['NONE']+=1;continue
    if typ&128:filters['converted_bit_normalized']+=1;typ &= ~128
    if typ in (18,22,23):filters['TLS']+=1;continue
    if a in dynamic:filters['dynamic_address']+=1;continue
    if typ in supported:filters['supported']+=1;continue
    filters['unsupported']+=1;k=(typ,s['name'],tsec['name']);counts[k]+=1
    xs=examples.setdefault(k,[])
    if len(xs)<20:
     syms=secs[s['link']];assert sym*syms['entsize']<syms['size']
     no=struct.unpack_from('<I',m,syms['offset']+sym*syms['entsize'])[0]
     xs.append({'offset':hex(a),'symbol':string(secs[syms['link']],no),'symbol_index':sym})
  result={'project':project,'input':str(p),'sha256':digest,'bytes':size,'status':'PASS' if filters['unsupported']==2804 else 'STOP','unsupported_total':filters['unsupported'],'expected':2804,'delta':filters['unsupported']-2804,'filters':dict(filters),'dynamic_sources':dynamic_sources,'dynamic_addresses':len(dynamic),'groups':[{'type':k[0],'name':names.get(k[0],'UNKNOWN'),'relocation_section':k[1],'target_section':k[2],'count':v,'examples':examples[k]} for k,v in sorted(counts.items())],'uncertain_filters':[],'time':datetime.datetime.now().astimezone().isoformat()}
  (E/(project+'-reloc-census.json')).write_text(json.dumps(result,indent=2)+'\n')
  print(project,result['status'],result['unsupported_total'],[(names.get(k[0]),v) for k,v in counts.items()],flush=True)
  return result
results=[]
try:
 for args in [('toolchain','ae3d837d862673b03c3c4718f6746f6986d8abe2078bad426b97905258b91a5c',226816920),('basedev','bf15cf062439714651809cd3b5ca82619407081adca64ceb65699e6ccae50501',226782848)]:results.append(run(*args))
 status='PASS' if all(r['status']=='PASS' for r in results) else 'STOP'
except Exception as ex:
 status='STOP';print(repr(ex),flush=True);raise
finally:print('88步骤2 已结束',datetime.datetime.now().astimezone().isoformat(),'status='+status,flush=True)
