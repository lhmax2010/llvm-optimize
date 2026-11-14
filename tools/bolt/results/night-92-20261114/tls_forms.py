import bisect,collections,datetime,gzip,hashlib,json,mmap,re,struct,subprocess
from pathlib import Path
E=Path(__file__).resolve().parent; B=E.parents[3]
OLD=B/'tools/bolt/results/night-88-20261114';plan=json.loads((B/'tools/bolt/results/night-87-20261114/report-stale-plan.json').read_text())
class ELF:
 def __init__(self,path):
  self.f=open(path,'rb');self.m=mmap.mmap(self.f.fileno(),0,access=mmap.ACCESS_READ);m=self.m
  assert m[:6]==b'\x7fELF\x02\x01';h=struct.unpack_from('<HHIQQQIHHHHHH',m,16);assert h[1]==62
  self.etype=h[0];self.ph=[dict(zip(('type','flags','offset','vaddr','paddr','filesz','memsz','align'),struct.unpack_from('<IIQQQQQQ',m,h[4]+i*h[8]))) for i in range(h[9])]
  self.s=[dict(zip(('nameoff','type','flags','addr','offset','size','link','info','align','entsize'),struct.unpack_from('<IIQQQQIIQQ',m,h[5]+i*h[10]))) for i in range(h[11])]
  for s in self.s:s['name']=self.string(self.s[h[12]],s['nameoff'])
 def string(self,s,o):
  a=s['offset']+o;z=self.m.find(b'\0',a,s['offset']+s['size']);assert z>=a;return self.m[a:z].decode(errors='replace')
 def sym(self,s,idx):
  sy=self.s[s['link']];name,info,other,ndx,value,size=struct.unpack_from('<IBBHQQ',self.m,sy['offset']+idx*sy['entsize']);return {'name':self.string(self.s[sy['link']],name),'info':info,'section':ndx,'value':value,'size':size}
 def rels(self,s):
  for o in range(s['offset'],s['offset']+s['size'],s['entsize']):
   a,i=struct.unpack_from('<QQ',self.m,o);yield a,i&0xffffffff,i>>32
 def bytes(self,a,n):
  s=next(s for s in self.s if s['addr']<=a and a+n<=s['addr']+s['size'] and s['type']!=8);o=s['offset']+a-s['addr'];return self.m[o:o+n]
def digest(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def analyze(project,sample=False):
 previous=json.loads((OLD/(project+'-reloc-census.json')).read_text());p=previous['input'];assert digest(p)==previous['sha256'];elf=ELF(p)
 rels=[];dynamic=set()
 for s in elf.s:
  if s['type'] in (4,9) and s['flags']&2:dynamic.update(a for a,t,_ in elf.rels(s) if t)
 for s in elf.s:
  if s['type'] not in (4,9) or s['flags']&2:continue
  target=elf.s[s['info']]
  if not target['flags']&2 or target['name'] in ('.plt','.rela.plt','.got.plt','.eh_frame','.gcc_except_table'):continue
  for a,t,i in elf.rels(s):
   if t in (19,20,21) and a not in dynamic:rels.append({'offset':a,'type':t,'relocation_section':s['name'],'symbol':elf.sym(s,i),'instructions':[]})
 assert len(rels)==2804
 if sample:rels=[r for t in (19,20,21) for r in sorted([r for r in rels if r['type']==t],key=lambda r:r['offset'])[:5]]
 rels.sort(key=lambda r:r['offset']); offsets=[r['offset'] for r in rels]
 # Collect every supported relocation within 24 bytes, without retaining all ELF relocations.
 supported={1,2,4,9,10,11,12,14,15,22,23,24,29,41,42}
 for r in rels:r['nearby_supported']=[]
 for s in elf.s:
  if s['type'] not in (4,9) or s['flags']&2:continue
  target=elf.s[s['info']]
  if not target['flags']&2 or target['name'] in ('.plt','.rela.plt','.got.plt','.eh_frame','.gcc_except_table'):continue
  for a,t,i in elf.rels(s):
   nt=t&~128
   if t==0 or nt in (18,22,23) or a in dynamic or nt not in supported:continue
   lo=bisect.bisect_left(offsets,a-24);hi=bisect.bisect_right(offsets,a+24)
   if lo==hi:continue
   row={'offset':a,'type':nt,'raw_type':t,'symbol':elf.sym(s,i)}
   for r in rels[lo:hi]:r['nearby_supported'].append(row)
 base=[s.replace('/basedev/','/'+project+'/') for s in plan['argv'][:3]]
 tool=plan['argv'][3].replace('/basedev/','/'+project+'/').replace('/llvm-bolt','/llvm-objdump')
 argv=base+[tool,'-d','--section=.text',p]
 if sample:
  # One bounded span covers the first five of each type for the D sample.
  argv+=['--start-address='+str(offsets[0]-32),'--stop-address='+str(offsets[-1]+40)]
 (E/(project+'-disassembly-command.json')).write_text(json.dumps({'argv':argv,'tool_sha256':digest(tool),'loader_sha256':digest(base[0])},indent=2)+'\n')
 insn=re.compile(r'^\s*([0-9a-f]+):\s+((?:[0-9a-f]{2} )*[0-9a-f]{2})\s+(.+)$')
 current='';num=0
 with (E/(project+'-objdump.stderr')).open('w') as err:
  proc=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=err,text=True)
  for line in proc.stdout:
   if line.rstrip().endswith('>:'):current=line.strip()
   mat=insn.match(line)
   if not mat:continue
   a=int(mat[1],16);bs=bytes.fromhex(mat[2]);num+=1
   lo=bisect.bisect_left(offsets,a-32);hi=bisect.bisect_right(offsets,a+32)
   for r in rels[lo:hi]:r['instructions'].append({'address':a,'size':len(bs),'bytes':bs.hex(),'asm':mat[3],'raw':line.rstrip(),'function':current})
  assert proc.wait()==0,'objdump failed'
 counts=collections.Counter();supportedseq={}
 for r in rels:
  a=r['offset'];ins=r['instructions'];cont=[i for i in ins if i['address']<=a<i['address']+i['size']];assert len(cont)==1,hex(a)
  r['containing_instruction']=cont[0];r['category']='other';r['form']='unclassified';r['sequence_range']=None
  if r['type'] in (19,20):
   # Fixed ABI linker relaxation windows (start relative to original relocation).
   starts=(a-4,a-3)
   for start in starts:
    seq=elf.bytes(start,24)
    if seq.startswith(bytes.fromhex('64488b042500000000')):
     tail=seq[9:];r['sequence_range']=[start,start+16]
     if tail[:3] in (bytes.fromhex('488d80'),bytes.fromhex('4805')) or tail[:2]==bytes.fromhex('4805'):
      r['category']='LE';r['form']='GD-to-LE fs:0 plus immediate'
     elif tail[:3]==bytes.fromhex('480305'):
      r['category']='IE';r['form']='GD-to-IE fs:0 plus RIP-relative GOT memory'
     break
    if seq.startswith(bytes.fromhex('66666664488b042500000000')):
     r['sequence_range']=[start,start+12];r['category']='LE';r['form']='LD-to-LE data16 padding plus fs:0';break
   if r['category']=='other' and any('call' in i['asm'] and '__tls_get_addr' in i['asm'] and a<=i['address']<=a+12 for i in ins):r['category']='unrelaxed';r['form']='call __tls_get_addr'
  else:
   i=cont[0]
   # DTPOFF32 is an immediate/disp32 data field. Require no RIP-relative access and TLS symbol.
   if '%rip' not in i['asm'] and 'call' not in i['asm'] and r['symbol']['info']&15==6 and a+4==i['address']+i['size']:
    r['category']='LE';r['form']='DTPOFF32 fixed displacement/immediate';r['sequence_range']=[i['address'],i['address']+i['size']]
  counts[(r['type'],r['category'],r['form'])]+=1
  interval=r['sequence_range']
  r['same_sequence_supported']=[x for x in r['nearby_supported'] if interval and interval[0]<=x['offset']<interval[1]]
  for x in r['same_sequence_supported']:supportedseq[x['offset']]=x
 result={'project':project,'sample':sample,'sha256':previous['sha256'],'elf_type':elf.etype,'program_headers':elf.ph,'PT_TLS':[h for h in elf.ph if h['type']==7],'counts':[{'type':k[0],'category':k[1],'form':k[2],'count':v} for k,v in sorted(counts.items())],'analyzed':len(rels),'decoded_instructions':num,'same_sequence_supported_unique':len(supportedseq),'same_sequence_supported':list(supportedseq.values()),'status':'待验证' if any(k[1]!='LE' for k in counts) or supportedseq else 'PASS'}
 (E/(project+'-forms-summary.json')).write_text(json.dumps(result,indent=2)+'\n')
 with gzip.open(E/(project+'-forms-full.json.gz'),'wt') as f:json.dump(rels,f,indent=2)
 ex=[]
 for k in counts:
  ex.append(str(k))
  for r in [r for r in rels if (r['type'],r['category'],r['form'])==k][:5]:
   ex.append(f"reloc {hex(r['offset'])} {r['symbol']['name']} {r['category']}")
   ex += [i['raw'] for i in r['instructions']]
 (E/(project+'-examples.txt')).write_text('\n'.join(ex)+'\n')
 print(project,json.dumps(result['counts']), 'residual',len(supportedseq),flush=True)
for p,s in [('toolchain',False),('basedev',True)]:analyze(p,s)
print('92步骤1 已结束',datetime.datetime.now().astimezone().isoformat(),'status=COMPLETED',flush=True)
