import pathlib,json,mmap,struct,hashlib,re,subprocess,datetime
E=pathlib.Path(__file__).resolve().parent;B=E.parents[3];W=pathlib.Path('/home/linhao/Toolchain/development/llvm-optimize')
logs=json.loads((E/'bolt-warning-lines.json').read_text());inputs=json.loads((B/'tools/bolt/results/night-82-84-20261113/83/inputs.json').read_text())
pgoinfo=json.loads((B/'tools/bolt/results/pgo-bolt-followup-20261105/identities.json').read_text())
(E/'pgo-identity-record.json').write_text(json.dumps(pgoinfo,indent=2)+'\n')
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
 return h.hexdigest()
def symbols(p):
 with open(p,'rb') as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as m:
  h=struct.unpack_from('<16sHHIQQQIHHHHHH',m,0);ss=[struct.unpack_from('<IIQQQQIIQQ',m,h[6]+i*h[11]) for i in range(h[12])]
  sn=ss[h[13]]
  def string(s,o):
   start=s[4]+o;end=m.find(b'\0',start,s[4]+s[5]);assert end>=0
   return m[start:end].decode(errors='replace')
  names=[string(sn,s[0]) for s in ss];out=[]
  for s in ss:
   if s[1]!=2:continue
   for pos in range(s[4],s[4]+s[5],24):
    n,inf,oth,idx,val,size=struct.unpack_from('<IBBHQQ',m,pos)
    if 0<idx<len(ss) and ss[idx][2]&4 and n:
     out.append(dict(name=string(ss[s[6]],n),type=inf&15,section=idx,address=val,size=size))
  return sorted(out,key=lambda d:(d['address'],d['name'])),names
results=[]
for proj,logid,p in [('toolchain','74-toolchain',pathlib.Path(inputs['toolchain']['path'])),('basedev','74-basedev',pathlib.Path(inputs['basedev']['path'])),('pgo','59-optimize',W/'temp/pgo-bolt-followup-20261105/reference-relocs-clang-22')]:
 expected=inputs.get(proj);ident=dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p))
 if expected:assert ident['bytes']==expected['size'] and ident['sha256']==expected['sha256']
 # Use tools from the 74 matching project root; PGO's original D root was removed,
 # so its read-only disassembly uses 74 Toolchain's own objdump+loader.
 toolproj=proj if proj in inputs else 'toolchain'
 root=W/'temp/rebase-359934-20261111-r6'/toolproj/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
 loader=root/'lib64/ld-linux-x86-64.so.2';tool=root/'usr/bin/llvm-objdump'
 if not tool.is_file():tool=root/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-objdump'
 assert loader.is_file() and tool.is_file(),(loader,tool)
 lib=':'.join(str(root/x) for x in ['home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64','lib64','usr/lib64'])
 prefix=[str(loader),'--library-path',lib,str(tool)]
 version=subprocess.run(prefix+['--version'],capture_output=True,text=True)
 assert version.returncode==0
 syms,sections=symbols(p);folder=E/'disassembly'/proj;folder.mkdir(parents=True)
 rr=dict(project=proj,input=ident,loader=str(loader),tool=str(tool),tool_sha256=sha(tool),version=version.stdout,debug_sections=[n for n in sections if n.startswith(('.debug','.zdebug'))],relocation_sections=[n for n in sections if n.startswith(('.rela','.rel'))],functions=[])
 for j,entry in enumerate(next(d for d in logs if d['id']==logid)['matches']):
  if entry['kind']!='nop':continue
  m=re.search(r'at (0x[0-9a-f]+) in function (\S+) :',entry['text']);assert m,entry
  at=int(m[1],16);name=re.sub(r'/\d+$','',m[2])
  candidates=[s for s in syms if s['name']==name]
  assert candidates,(proj,name)
  hit=next((s for s in candidates if s['address']<=at<s['address']+s['size']),candidates[0])
  nxt=next(s for s in syms if s['section']==hit['section'] and s['address']>hit['address'] and s['type'] in (2,10))
  cmd=prefix+['-d','--disassemble-symbols='+hit['name']+','+nxt['name'],str(p)]
  out=folder/(str(j).zfill(2)+'.txt');err=folder/(str(j).zfill(2)+'.stderr')
  with out.open('w') as fo,err.open('w') as fe:
   proc=subprocess.run(cmd,stdout=fo,stderr=fe,timeout=180)
  assert proc.returncode==0,(cmd,proc.returncode)
  lines=out.read_text().splitlines();near=[]
  for i,line in enumerate(lines):
   if re.match(r'\s*'+format(at,'x')+r':',line):near=lines[max(0,i-3):i+6]
  row=dict(warning=entry,symbol=hit,next_symbol=nxt,jump_address=at,function_end=hit['address']+hit['size'],argv=cmd,rc=proc.returncode,output=str(out.relative_to(B)),near_warning=near)
  rr['functions'].append(row)
  print(proj,name,'at',hex(at),'end',hex(row['function_end']),'next',nxt['name'],flush=True)
  print('\n'.join(near),flush=True)
 results.append(rr)
 (E/'disassembly-progress.json').write_text(json.dumps(results,indent=2)+'\n')
(E/'disassembly-result.json').write_text(json.dumps(results,indent=2)+'\n')
print('disassembly done',datetime.datetime.now().astimezone().isoformat())
