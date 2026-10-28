import probe as p
import re,json
summary=[]
for role in ['ordinary','final','symbols']:
 for mode in ['absent','present']:
  text=(p.E/('crash-'+role+'-'+mode+'.stderr')).read_text();frames=[]
  for line in text.splitlines():
   m=re.match(r'\s*#(\d+)\s+(0x[0-9a-fA-F]+)\s*(.*)',line)
   if m:idx,ip,tail=int(m[1]),m[2],m[3];named=bool(tail and not tail.startswith(('(','??','0x')))
   else:
    m=re.match(r'\s*(\d+)\s+(\S+)\s+(0x[0-9a-fA-F]+)(?:\s+(.*))?$',line)
    if not m:continue
    idx,ip,tail=int(m[1]),m[3],m[4] or '';named=bool(tail)
   frames.append({'index':idx,'ip':ip,'named':named,'text':tail,'raw':line})
  result=json.loads((p.E/('crash-'+role+'-'+mode+'.json')).read_text())
  summary.append({'role':role,'symbolizer':mode,'rc':result['rc'],'total':len(frames),'named':sum(x['named'] for x in frames),'address_only':sum(not x['named'] for x in frames),'frames':frames})
p.save('crashes-corrected.json',{'parser_note':'LLVM uses two formats: absent tool uses numbered module/address rows; present tool uses #N rows. Original raw logs unchanged; both parsed here.','runs':summary})
frames=next(x for x in summary if x['role']=='final' and x['symbolizer']=='present')['frames'];addresses=[]
for f in frames:
 m=re.search(re.escape(str(p.D/'clang.final'))+r'\+0x([0-9a-fA-F]+)',f['text'])
 if m:addresses.append({'frame':f['index'],'runtime_ip':f['ip'],'module_offset':'0x'+m[1]})
p.save('offline-addresses-corrected.json',{'source':'final-present crash stack; PIE module offsets printed by LLVM; no guessing ASLR load base','addresses':addresses})
_,out,_=p.run('offline-symbols-corrected',[*p.LOADER,p.BUILD/'bin/llvm-symbolizer','--obj='+str(p.D/'clang.symbols'),'--inlining=false'],stdin='\n'.join(x['module_offset'] for x in addresses)+'\n')
blocks=[b for b in out.strip().split('\n\n') if b.strip()];assert len(blocks)==len(addresses),(len(blocks),len(addresses))
for a,b in zip(addresses,blocks):a['resolved']=b.splitlines()[0];a['location']=b.splitlines()[1:]
p.save('offline-resolution.json',{'resolved':sum(x['resolved']!='??' for x in addresses),'total':len(addresses),'results':addresses,'symbols_only':'NOT AVAILABLE: llvm-objcopy --only-keep-debug SIGSEGV, original log retained'})
print([(x['role'],x['symbolizer'],x['named'],x['address_only']) for x in summary]);print('offline',len(addresses),sum(x['resolved']!='??' for x in addresses))
