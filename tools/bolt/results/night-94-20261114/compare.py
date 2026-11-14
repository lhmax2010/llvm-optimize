from common import *
import bisect,collections,datetime,gzip,re,subprocess
STAMP=lambda:datetime.datetime.now().astimezone().isoformat()
rx=re.compile(r'^\s*([0-9a-f]+):\s+((?:[0-9a-f]{2} )*[0-9a-f]{2})\s+(.+)$')
fs=re.compile(r'^movq %fs:(?:0x0|0), (%[a-z0-9]+)$')
add=re.compile(r'^addq (-?(?:0x)?[0-9a-f]+)\(%rip\), (%[a-z0-9]+)$')
def norm(s):
 s=s.split('#',1)[0].strip()
 s=re.sub(r'^(?:(?:data16|data32|addr32)\s+)+','',s)
 return re.sub(r'\s+',' ',s)
def family(r):
 for main,aliases in {'rax':['eax','ax','al','ah'],'rbx':['ebx','bx','bl','bh'],'rcx':['ecx','cx','cl','ch'],'rdx':['edx','dx','dl','dh'],'rsi':['esi','si','sil'],'rdi':['edi','di','dil'],'rbp':['ebp','bp','bpl'],'rsp':['esp','sp','spl']}.items():
  if r.lstrip('%') in [main]+aliases:return '%'+main
 return re.sub(r'^(%r\d+)[dwb]$',r'\1',r)
def dyn(e):
 out=[]
 for s in e.s:
  if s['name']!='.rela.dyn':continue
  for o in range(s['offset'],s['offset']+s['size'],s['entsize']):
   a,i,d=struct.unpack_from('<QQq',e.m,o)
   if i&0xffffffff==18:out.append([a,e.sym(s,i>>32)['name'],d])
 return sorted(out)
def table(e,input_names):
 groups=collections.defaultdict(list)
 for s in symbols(e):groups[(s['section'],s['address'])].append(s)
 out=collections.defaultdict(list)
 for (sec,a),ss in groups.items():
  names=[]
  for s in ss:
   n=s['name'];base=re.sub(r'\.cold(?:\.\d+)?$','',n)
   names.append(base if base in input_names else n)
  candidates=sorted(set(names)&input_names) or sorted(set(names))
  out[sec].append(dict(address=a,end=max(a+s['size'] for s in ss),name=candidates[0],aliases=[s['name'] for s in ss]))
 for sec in out:out[sec].sort(key=lambda s:s['address'])
 return out

def scan(project,role,path,e,tab,oldtab):
 cfg=json.loads((B/'tools/bolt/results/night-92-20261114'/f'{project}-disassembly-command.json').read_text());base=cfg['argv'][:4]
 assert sha(base[0])==cfg['loader_sha256'] and sha(base[3])==cfg['tool_sha256']
 argv=base+['-d','--disassemble-zeroes',path];save(project+'-'+role+'-command.json',dict(argv=argv,tool_sha=cfg['tool_sha256'],loader_sha=cfg['loader_sha256']))
 records=[];segment=[];active={};pending=None;serial=0;section='';coverage=collections.Counter();orphan=[];funcs=collections.defaultdict(lambda:dict(fs=[],IE=[],LD=[],ops=[]));previous_end=None;current=None
 def owner(addr):
  nonlocal current
  ts=oldtab.get('.text',[]) if section=='.bolt.org.text' else tab.get(section,[])
  if not current or not current['address']<=addr<current['end']:
   ix=bisect.bisect_right(starts.get(section,[]),addr)-1
   current=ts[ix] if ix>=0 else None
  if current and current['address']<=addr<current['end']:return ('OLD:' if section=='.bolt.org.text' else '')+current['name']
  return 'UNMAPPED:'+section+':'+hex(addr)
 starts={sec:[s['address'] for s in ts] for sec,ts in tab.items()};starts['.bolt.org.text']=[s['address'] for s in oldtab.get('.text',[])]
 def finish_pending(am,item):
  nonlocal pending
  if pending is None:return
  r=pending;pending=None
  if am and am[2]==r['register'] and item['address']==r['address']+len(bytes.fromhex(r['bytes'])):
   r['kind']='IE';r['add']=item;r['GOT']=item['address']+len(bytes.fromhex(item['bytes']))+int(am[1],16);funcs[r['function']]['IE'].append(r);active.pop(r['register'],None)
  else:r['kind']='LD';funcs[r['function']]['LD'].append(r)
 with (E/(project+'-'+role+'-objdump.stderr')).open('w') as err:
  p=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=err,text=True)
  for line in p.stdout:
   if line.startswith('Disassembly of section '):
    finish_pending(None,None);section=line.strip().split('section ',1)[1][:-1];active.clear();current=None;previous_end=None;continue
   m=rx.match(line)
   if not m:continue
   a=int(m[1],16);rawbytes=m[2].replace(' ','');asm=norm(m[3]);coverage[section]+=1;serial+=1
   fm=fs.match(asm);am=add.match(asm)
   # Keep only TLS evidence; all instructions still advance lifetime and coverage.
   item=None
   if pending or active or '%fs:' in asm:
    item=dict(address=a,bytes=rawbytes,asm=asm,raw=line.rstrip(),section=section,function=owner(a))
   finish_pending(am,item)
   if previous_end!=a:active.clear()
   previous_end=a+len(rawbytes)//2
   if '%fs:' in asm:
    funcs[item['function']]['fs'].append(item)
    if item['function'].startswith('UNMAPPED:'):orphan.append(item)
   if fm:
    r=dict(item,register=fm[1],kind=None,operations=[]);records.append(r);active[fm[1]]=r;pending=r
   else:
    for reg,r in list(active.items()):
     if item['function']!=r['function']:active.pop(reg,None);continue
     # A TLS-relative memory operand whose base is this loaded register.
     if re.search(r'\('+re.escape(reg)+r'(?:,|\))',asm):
      r['operations'].append(item);funcs[r['function']]['ops'].append(item)
    mn=asm.split(' ',1)[0]
    if mn.startswith(('j','call','ret','loop')) or mn in ('ud2','int3','syscall'):active.clear()
    else:
     dest=re.search(r'(?:^|,)\s*(%[a-z0-9]+)$',asm)
     if dest and not mn.startswith(('cmp','test','push','bt','prefetch')):active.pop(family(dest[1]),None)
  finish_pending(None,None)
  assert p.wait()==0,'objdump failed'
 assert set(s['name'] for s in e.s if s['flags']&4 and s['size'])<=set(coverage)
 result=dict(functions=dict(funcs),sequences=records,coverage=dict(coverage),unmapped=orphan)
 with gzip.open(E/(project+'-'+role+'-tls.json.gz'),'wt') as f:json.dump(result,f)
 print(project,role,'scanned',sum(coverage.values()),'instructions',len(records),'fs0 sequences',STAMP(),flush=True)
 return result

def summary_stats(r):
 f=r['functions'];return dict(functions=len(f),fs=sum(len(x['fs']) for x in f.values()),IE=sum(len(x['IE']) for x in f.values()),LD=sum(len(x['LD']) for x in f.values()),ops=sum(len(x['ops']) for x in f.values()),unmapped=len(r['unmapped']))
def compare(project):
 rr={r['role']:r for r in ids if r['project']==project};inp=ELF(rr['input']['path']);out=ELF(rr['auxiliary_bolt_before_strip']['path']);final=ELF(rr['final_rpm']['path'])
 names={s['name'] for s in symbols(inp)};ti=table(inp,names);to=table(out,names)
 gi=dyn(inp);go=dyn(final);save(project+'-GOT.json',dict(input=gi,output=go,equal=gi==go))
 i=scan(project,'input',rr['input']['path'],inp,ti,ti);o=scan(project,'output',rr['auxiliary_bolt_before_strip']['path'],out,to,ti)
 empty=dict(fs=[],IE=[],LD=[],ops=[]);bad=[];equal=0
 for name in sorted(set(i['functions'])|{n for n in o['functions'] if not n.startswith('OLD:')}):
  a=i['functions'].get(name,empty);b=o['functions'].get(name,empty);diff={}
  for field in ('fs','IE','LD','ops'):
   x=collections.Counter(z['asm'] for z in a[field]) if field in ('fs','ops') else collections.Counter({'count':len(a[field])})
   y=collections.Counter(z['asm'] for z in b[field]) if field in ('fs','ops') else collections.Counter({'count':len(b[field])})
   if x!=y:diff[field]=dict(input=dict(x),output=dict(y))
  if diff:bad.append(dict(function=name,differences=diff,input=a,output=b))
  else:equal+=1
 ie=[r for r in o['sequences'] if r['kind']=='IE'];outside=[r for r in ie if r['GOT'] not in {x[0] for x in go}]
 old=[r for r in o['sequences'] if r['function'].startswith('OLD:')];oldproof=[]
 imap={r['address']:r for r in i['sequences']}
 for r in old:
  a=imap.get(r['address']);oldproof.append(dict(output=r,input=a,same=bool(a and a['bytes']==r['bytes'] and a['kind']==r['kind'])))
 ld=[r for r in o['sequences'] if r['kind']=='LD' and not r['function'].startswith('OLD:')]
 s=dict(project=project,input=summary_stats(i),output=summary_stats(o),compared_functions=equal+len(bad),equal_functions=equal,different_functions=len(bad),G_equal=gi==go,IE_outside_G=len(outside),old_sequences=len(old),old_identical=sum(r['same'] for r in oldproof),LD_main=len(ld),LD_main_without_data16=sum(not r['bytes'].startswith('66') for r in ld),LD_main_with_data16=sum(r['bytes'].startswith('66') for r in ld),old_LD=sum(r['kind']=='LD' for r in old),time=STAMP())
 s['status']='PASS' if not bad and not outside and gi==go and not i['unmapped'] and not o['unmapped'] and all(r['same'] for r in oldproof) else 'FAIL'
 with gzip.open(E/(project+'-differences.json.gz'),'wt') as f:json.dump(bad,f,indent=2)
 save(project+'-old-copies.json',oldproof);save(project+'-summary.json',s);save(project+'-outside-G.json',outside)
 print(json.dumps(s),flush=True);print('94逐函数核对 已结束',STAMP(),project,'status='+s['status'],flush=True)
 return s
if __name__=='__main__':
 results=[]
 for project in ('toolchain','basedev'):
  s=compare(project);results.append(s)
  if s['status']!='PASS':print('STOP: per-function TLS comparison has unmatched or different items; no rules changed.',flush=True);break
 save('overall.json',dict(results=results,status='PASS' if len(results)==2 and all(s['status']=='PASS' for s in results) else 'FAIL'))
