import ast,collections,datetime,gzip,hashlib,json,mmap,re,struct,subprocess
from pathlib import Path
E=Path(__file__).resolve().parent;B=E.parents[3]
# Reuse only the readonly ELF parser class, not task92's executable main.
parser=B/'tools/bolt/results/night-92-20261114/tls_forms.py'
node=next(n for n in ast.parse(parser.read_text()).body if isinstance(n,ast.ClassDef) and n.name=='ELF')
exec(compile(ast.Module(body=[node],type_ignores=[]),str(parser),'exec'))
identities=json.loads((E/'identities.json').read_text())
def save(name,value): (E/name).write_text(json.dumps(value,indent=2)+'\n')
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 return h.hexdigest()
def dynamic(elf):
 rows=[];needed=[]
 for s in elf.s:
  if s['name']=='.rela.dyn':
   for o in range(s['offset'],s['offset']+s['size'],s['entsize']):
    addr,info,addend=struct.unpack_from('<QQq',elf.m,o)
    if info&0xffffffff==18:rows.append({'address':addr,'symbol':elf.sym(s,info>>32),'addend':addend})
  if s['type']==6:
   for o in range(s['offset'],s['offset']+s['size'],s['entsize']):
    tag,val=struct.unpack_from('<qQ',elf.m,o)
    if tag==1:needed.append(elf.string(elf.s[s['link']],val))
 return {'TPOFF64':rows,'NEEDED':needed}
def key(row):return (row['address'],row['symbol']['name'],row['addend'])
def raw_ld(elf):
 # Fixed prefix including mov's absolute fs:disp32 addressing; all nonzero variations too.
 prefix=bytes.fromhex('66666664488b0425');rows=[]
 for s in elf.s:
  if not s['flags']&4 or s['type']==8:continue
  start=s['offset'];end=start+s['size'];pos=start
  while True:
   pos=elf.m.find(prefix,pos,end)
   if pos<0:break
   assert pos+12<=end
   disp=struct.unpack_from('<I',elf.m,pos+8)[0]
   rows.append({'section':s['name'],'address':s['addr']+pos-start,'fs_displacement':disp,'bytes':elf.m[pos:pos+12].hex(),'disassembly':None});pos+=1
 return rows
insn_re=re.compile(r'^\s*([0-9a-f]+):\s+((?:[0-9a-f]{2} )*[0-9a-f]{2})\s+(.+)$')
fs_re=re.compile(r'^movq\s+%fs:(?:0x0|0),\s*(%[a-z0-9]+)$')
add_re=re.compile(r'^addq\s+(-?(?:0x)?[0-9a-f]+)\(%rip\),\s*(%[a-z0-9]+)$')
copy_re=re.compile(r'^movq\s+(%[a-z0-9]+),\s*(%[a-z0-9]+)$')
def register_family(reg):
 for r,aliases in {'rax':['eax','ax','al','ah'],'rbx':['ebx','bx','bl','bh'],'rcx':['ecx','cx','cl','ch'],'rdx':['edx','dx','dl','dh'],'rsi':['esi','si','sil'],'rdi':['edi','di','dil'],'rbp':['ebp','bp','bpl'],'rsp':['esp','sp','spl']}.items():
  if reg.lstrip('%') in [r]+aliases:return '%'+r
 return re.sub(r'^(%r\d+)[dwb]$',r'\1',reg)
def disassemble(project,path,elf,G,ld):
 cfg=json.loads((B/'tools/bolt/results/night-92-20261114'/f'{project}-disassembly-command.json').read_text());base=cfg['argv'][:4]
 assert sha(base[0])==cfg['loader_sha256'] and sha(base[3])==cfg['tool_sha256']
 argv=base+['-d','--disassemble-zeroes',path]
 save(project+'-output-command.json',{'argv':argv,'loader_sha256':cfg['loader_sha256'],'tool_sha256':cfg['tool_sha256']})
 matches=[];variants=[];fs_total=0;pending={};serial=0;history=collections.deque(maxlen=33);section='';function='';coverage=collections.Counter();ldmap={r['address']:r for r in ld};previous=None
 with (E/(project+'-objdump.stderr')).open('w') as error:
  proc=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=error,text=True)
  for line in proc.stdout:
   if line.startswith('Disassembly of section '):section=line.strip().split('section ',1)[1].rstrip(':');pending.clear();history.clear();previous=None
   if line.strip().endswith('>:'):function=line.strip()
   m=insn_re.match(line)
   if not m:continue
   addr=int(m[1],16);bs=bytes.fromhex(m[2]);asm=m[3].split('#',1)[0].strip();serial+=1;coverage[section]+=1
   item={'section':section,'address':addr,'bytes':bs.hex(),'asm':asm,'raw':line.rstrip(),'function':function,'serial':serial}
   if addr in ldmap:ldmap[addr]['disassembly']=item
   if previous and addr!=previous['address']+len(bytes.fromhex(previous['bytes'])):pending.clear()
   for reg in list(pending):
    if serial-pending[reg]['serial']>32:del pending[reg]
   fm=fs_re.match(asm);am=add_re.match(asm);cm=copy_re.match(asm)
   if am:
    dest=am[2];origin=pending.get(dest)
    if origin is None and previous and fs_re.match(previous['asm']):origin=previous
    if origin:
     disp=int(am[1],16);target=addr+len(bs)+disp
     variant='adjacent_same_register' if serial==origin['serial']+1 and fs_re.match(origin['asm'])[1]==dest else 'intervening_or_different_register'
     row={'section':section,'fs_load':origin,'add':item,'target':target,'in_G_out':target in G,'variant':variant,'between':[x for x in history if x['serial']>origin['serial']]}
     matches.append(row)
     if variant!='adjacent_same_register':variants.append(row)
   if fm:
    fs_total+=1;pending[fm[1]]=item
   else:
    # Retain aliases across register copies; unrelated instructions are kept.
    alias=pending.get(cm[1]) if cm else None
    mnemonic=asm.split()[0] if asm else ''
    dest=re.search(r'(?:^|,)\s*(%[a-z0-9]+)$',asm)
    if mnemonic.startswith(('call','ret','jmp','j')):pending.clear()
    elif mnemonic.startswith(('mov','lea','add','sub','xor','and','or','inc','dec','pop','imul','mul','div','neg','not','sh','sa','cmov','set')) and dest:pending.pop(register_family(dest[1]),None)
    if cm and alias:pending[cm[2]]=alias
   history.append(item);previous=item
  rc=proc.wait();assert rc==0,('objdump',rc)
 executable=[s['name'] for s in elf.s if s['flags']&4 and s['size'] and s['type']!=8]
 assert set(executable)<=set(coverage),('unscanned executable sections',set(executable)-set(coverage))
 assert all(r['disassembly'] is not None for r in ld),'raw LD pattern was not aligned to a decoded instruction'
 return {'matches':matches,'variants':variants,'fs0_load_count':fs_total,'executable_sections':executable,'decoded_instructions_by_section':dict(coverage)}
results=[]
for project in ('toolchain','basedev'):
 identities_project={r['role']:r for r in identities if r['project']==project}
 ip=identities_project['input'];op=identities_project['final_rpm']
 assert sha(ip['path'])==ip['sha256'] and sha(op['path'])==op['sha256']
 inp=ELF(ip['path']);out=ELF(op['path']);din=dynamic(inp);dout=dynamic(out)
 gin={key(r) for r in din['TPOFF64']};gout={key(r) for r in dout['TPOFF64']};addresses={r['address'] for r in dout['TPOFF64']}
 save(project+'-dynamic.json',{'input':din,'output':dout,'equal':gin==gout,'only_in_input':sorted(gin-gout),'only_in_output':sorted(gout-gin)})
 ld_in=raw_ld(inp);ld_out=raw_ld(out)
 result=disassemble(project,op['path'],out,addresses,ld_out)
 # Derive all input GD-to-IE references from actual bytes at original TLSGD records.
 input_ie=[]
 for s in inp.s:
  if s['type'] not in (4,9):continue
  for a,t,idx in inp.rels(s):
   if t!=19:continue
   start=a-4;seq=inp.bytes(start,16)
   assert seq[:12]==bytes.fromhex('64488b042500000000480305'),('unexpected input TLSGD form',hex(a))
   target=start+16+struct.unpack_from('<i',seq,12)[0];input_ie.append({'address':start,'target':target,'bytes':seq.hex(),'symbol':inp.sym(s,idx)})
 ci=collections.Counter(r['target'] for r in input_ie);co=collections.Counter(r['target'] for r in result['matches']);bad=[r for r in result['matches'] if not r['in_G_out']]
 result.update(input_ie=input_ie,ld_input=ld_in,ld_output=ld_out)
 with gzip.open(E/(project+'-full-static-check.json.gz'),'wt') as f:json.dump(result,f,indent=2)
 summary={'project':project,'G_equal':gin==gout,'G_count':len(gout),'input_IE':len(input_ie),'output_IE':len(result['matches']),'IE_variants':len(result['variants']),'outside_G':len(bad),'references_by_slot':[{'address':hex(a),'symbol':next((r['symbol']['name'] for r in dout['TPOFF64'] if r['address']==a),'NOT_IN_G'),'input':ci[a],'output':co[a]} for a in sorted(set(ci)|set(co))],'input_LD_zero':sum(r['fs_displacement']==0 for r in ld_in),'output_LD_zero':sum(r['fs_displacement']==0 for r in ld_out),'output_LD_nonzero':sum(r['fs_displacement']!=0 for r in ld_out),'executable_sections':result['executable_sections'],'decoded_instructions_by_section':result['decoded_instructions_by_section'],'fs0_load_count':result['fs0_load_count'],'time':datetime.datetime.now().astimezone().isoformat()}
 summary['status']='PASS' if gin==gout and len(input_ie)==len(result['matches'])==1536 and ci==co and not bad and summary['input_LD_zero']==summary['output_LD_zero']==415 and summary['output_LD_nonzero']==0 else 'FAIL'
 save(project+'-summary.json',summary)
 examples=[]
 for row in result['matches'][:5]+result['variants']+bad:
  examples.append(json.dumps({k:v for k,v in row.items() if k not in ('fs_load','add','between')}));examples.append(row['fs_load']['raw']);examples.extend(i['raw'] for i in row['between']);examples.append(row['add']['raw'])
 for row in [r for r in ld_out if r['fs_displacement']!=0] or ld_out[:5]:examples.append(row['disassembly']['raw'])
 (E/(project+'-examples-and-all-bad.txt')).write_text('\n'.join(examples)+'\n')
 print(json.dumps(summary),flush=True);print('93静态核对 已结束',summary['time'],project,'status='+summary['status'],flush=True)
 results.append(summary)
 if summary['status']=='FAIL':print('STOP: final clang TLS static-check mismatch; no rule changes or retries.',flush=True);break
save('overall-result.json',{'results':results,'status':'PASS' if len(results)==2 and all(r['status']=='PASS' for r in results) else 'FAIL'})
