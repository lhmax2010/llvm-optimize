from pathlib import Path
import os,sys,json,hashlib,subprocess,shutil,resource,signal,time,re,importlib.util,struct,lzma,traceback,shlex
W=Path('/home/linhao/Toolchain/development/llvm-optimize'); B=W.parent/'llvm-optimize-bolt'
D=Path(__file__).resolve().parent; E=B/'tools/bolt/results/crash-probe-20261028';E.mkdir(parents=True,exist_ok=True)
ROOT=W/'temp/oldtext-final-20261027/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
BUILD=ROOT/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build';WORK=BUILD/'clang-bolt';P=W/'temp/oldtext-final-20261027/products'
LOADER=[str(ROOT/'lib64/ld-linux-x86-64.so.2'),'--library-path',str(ROOT/'lib64')+':'+str(ROOT/'usr/lib64')]
CM=Path('/home/linhao/.local/state/security-remediation/2026-10-23/brotli-local-build/build-tools/lib/python3.12/site-packages/cmake/data/bin/cmake')
sp=importlib.util.spec_from_file_location('helper',W/'temp/oldtext-final-20261027/source/packaging/clang-bolt-helper.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(name,obj): (E/name).write_text(json.dumps(obj,indent=2)+'\n')
def limits():resource.setrlimit(resource.RLIMIT_CORE,(0,0))
def run(name,argv,env=None,stdin=None,timeout=180,check=True):
 start=time.monotonic()
 with (E/(name+'.stdout')).open('wb') as o,(E/(name+'.stderr')).open('wb') as e:
  p=subprocess.Popen(list(map(str,argv)),cwd=D,env=env,stdin=subprocess.PIPE if stdin is not None else subprocess.DEVNULL,stdout=o,stderr=e,start_new_session=True,preexec_fn=limits)
  try:p.communicate(stdin.encode() if stdin is not None else None,timeout=timeout)
  except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait();raise
 result={'argv':list(map(str,argv)),'rc':p.returncode,'seconds':time.monotonic()-start,'cwd':str(D)};save(name+'.json',result)
 if check and p.returncode:raise RuntimeError(name+' rc='+str(p.returncode))
 return result,(E/(name+'.stdout')).read_text(errors='replace'),(E/(name+'.stderr')).read_text(errors='replace')
def extract(rpm,target,out):
 p=subprocess.Popen(['rpm2cpio',str(rpm)],stdout=subprocess.PIPE,stderr=subprocess.PIPE);f=p.stdout;found=False
 def rd(n):
  b=b''
  while len(b)<n:
   z=f.read(n-len(b));assert z;b+=z
  return b
 while True:
  head=rd(110);assert head[:6] in (b'070701',b'070702');v=[int(head[6+8*i:14+8*i],16) for i in range(13)];n=rd(v[11]).rstrip(b'\0').decode();rd((-110-v[11])%4)
  if n=='TRAILER!!!':break
  selected=n.removeprefix('./')==target;remaining=v[6]
  dest=out.open('wb') if selected else None
  while remaining:
   block=rd(min(remaining,1024*1024));remaining-=len(block)
   if dest:dest.write(block)
  if dest:dest.close();found=True;out.chmod(0o755)
  rd((-v[6])%4)
 f.read();err=p.stderr.read();assert p.wait()==0,err;assert found

def prepare():
 rpms={'bolt':P/'RPMS/clang-debuginfo-22.1.8-1.x86_64.rpm'}
 candidates=sorted((W/'temp/hybrid-local-20261023').rglob('clang-debuginfo-22.1.8-1.x86_64.rpm'))
 if candidates:rpms['hybrid']=candidates[0]
 rows={}
 for name,p in rpms.items():
  _,out,_=run('debuginfo-'+name,['rpm','-qp','--qf','[%{FILENAMES}\t%{FILESIZES}\t%{FILEMODES}\n]',p]);files=[]
  for l in out.splitlines():
   path,size,mode=l.split('\t');files.append({'path':path,'bytes':int(size),'mode':mode})
  rows[name]={'rpm':str(p),'sha256':sha(p),'files':files,'clang_debug':[x for x in files if 'clang-22' in x['path']]}
 save('debuginfo.json',rows)
 final=D/'clang.final';extract(P/'RPMS/clang-22.1.8-1.x86_64.rpm','usr/bin/clang-22',final)
 assert sha(final)=='8c2429d870f421a29a9914458bc4d4ff2ce359a15e0bdd20f39bfb4580c40bdf'
 ordinary=D/'clang.ordinary';symbols=D/'clang.symbols';shutil.copyfile(WORK/'ordinary-clang-22',ordinary);ordinary.chmod(0o755);shutil.copyfile(WORK/'clang.bolt',symbols);symbols.chmod(0o755)
 assert sha(WORK/'clang.bolt')==json.loads((WORK/'identity.json').read_text())['before_sha256']
 ids={}
 for role,p in [('final',final),('ordinary',ordinary),('prestrip',WORK/'clang.bolt')]:
  _,out,_=run('build-id-'+role,['readelf','-nW',p]);ids[role]={'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p),'build_ids':re.findall(r'Build ID: (\S+)',out),'has_note_gnu_build_id':'.note.gnu.build-id' in out}
 save('build-ids.json',ids)
 run('strip-debug',[*LOADER,BUILD/'bin/llvm-strip','--strip-debug',symbols])
 old=h.security_properties(symbols)['DT_RUNPATH'];script=D/'symbols-rpath.cmake';script.write_text('file(RPATH_CHANGE FILE '+h.cmake_literal(str(symbols))+' OLD_RPATH '+h.cmake_literal(old)+' NEW_RPATH '+h.cmake_literal('$ORIGIN/../lib64')+')\n')
 run('symbols-rpath',[CM,'-P',script]);assert h.security_properties(symbols)['DT_RUNPATH']=='$ORIGIN/../lib64'
 run('only-keep-debug',[*LOADER,BUILD/'bin/llvm-objcopy','--only-keep-debug',symbols,D/'clang.symbols-only'])
 save('prepared.json',{r:{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for r,p in [('final',final),('ordinary',ordinary),('symbols',symbols),('symbols-only',D/'clang.symbols-only')]})

def crash():
 (D/'crash.c').write_text('#pragma clang __debug crash\n');(D/'empty-path').mkdir(exist_ok=True);(D/'symbolizer-path').mkdir(exist_ok=True)
 wrapper=D/'symbolizer-path/llvm-symbolizer';wrapper.write_text('#!/bin/sh\nexec '+shlex.join([*LOADER,str(BUILD/'bin/llvm-symbolizer')])+' "$@"\n');wrapper.chmod(0o755)
 summary=[]
 for role in ['ordinary','final','symbols']:
  for mode in ['absent','present']:
   env={**os.environ,'LC_ALL':'C','PATH':str(D/('empty-path' if mode=='absent' else 'symbolizer-path')),'TMPDIR':str(D)}
   env.pop('LLVM_SYMBOLIZER_PATH',None);env.pop('LLVM_DISABLE_SYMBOLIZATION',None)
   result,out,err=run('crash-'+role+'-'+mode,['/usr/bin/taskset','-c','2','/usr/bin/setarch','x86_64','-R',*LOADER,D/('clang.'+role),'--no-default-config','-resource-dir='+str(BUILD/'lib64/clang/22'),'-fno-crash-diagnostics','-fsyntax-only',D/'crash.c'],env=env,check=False)
   frames=[]
   for line in (out+'\n'+err).splitlines():
    m=re.match(r'\s*#(\d+)\s+(0x[0-9a-fA-F]+)\s*(.*)',line)
    if m:
     rest=m[3];named=bool(rest and not rest.startswith(('(','0x','??')));frames.append({'frame':int(m[1]),'ip':m[2],'text':rest,'named':named,'raw':line})
   summary.append({'role':role,'symbolizer':mode,'rc':result['rc'],'named_frames':sum(x['named'] for x in frames),'address_only_frames':sum(not x['named'] for x in frames),'frames':frames})
 save('crashes.json',summary)

def layout_offline():
 a=h.ELF(D/'clang.final');b=h.ELF(D/'clang.symbols');rows=[];diffs=[]
 for name,s in a.by_name.items():
  if s[2]&2 and s[1]!=8:
   t=b.by_name.get(name);equal=t is not None and s[3:6]==t[3:6] and a.mm[s[4]:s[4]+s[5]]==b.mm[t[4]:t[4]+t[5]]
   rows.append({'section':name,'address':s[3],'bytes':s[5],'equal':equal})
   if not equal:diffs.append(name)
 load_diffs=[]
 for p in a.loads:
  q=next((q for q in b.loads if q[3]==p[3]),None)
  if q and p==q:
   for off in range(p[2],p[2]+p[5]):
    if a.mm[off]!=b.mm[off]:load_diffs.append(off)
  else:load_diffs.append({'load_header_difference':p})
 save('layout.json',{'all_alloc_sections_equal':not diffs,'alloc_sections':rows,'program_headers_equal':a.phdrs==b.phdrs,'load_byte_differences':load_diffs,'elf_type':a.elf_type,'section_only_final':sorted(a.by_name.keys()-b.by_name.keys()),'section_only_symbols':sorted(b.by_name.keys()-a.by_name.keys())});a.close();b.close()
 data=json.loads((E/'crashes.json').read_text());frame_set=next(x for x in data if x['role']=='final' and x['symbolizer']=='absent')['frames'];addresses=[]
 for f in frame_set:
  m=re.search(re.escape(str(D/'clang.final'))+r'\+0x([0-9a-fA-F]+)',f['text'])
  if m:addresses.append({'frame':f['frame'],'runtime_ip':f['ip'],'module_offset':'0x'+m[1]})
 save('offline-addresses.json',addresses)
 for variant in ['symbols','symbols-only']:
  run('offline-'+variant,[*LOADER,BUILD/'bin/llvm-symbolizer','--obj='+str(D/('clang.'+variant)),'--inlining=false'],stdin='\n'.join(x['module_offset'] for x in addresses)+'\n')

def sizes():
 rows={}
 for role in ['final','symbols','symbols-only']:
  p=D/('clang.'+role);c=lzma.LZMACompressor(format=lzma.FORMAT_XZ,preset=5);n=0;start=time.monotonic()
  with p.open('rb') as f:
   while block:=f.read(1024*1024):n+=len(c.compress(block))
  n+=len(c.flush());rows[role]={'bytes':p.stat().st_size,'xz5_stream_bytes':n,'compression_seconds':time.monotonic()-start}
 save('sizes.json',{'method':'RPM payload uses xz 5T. Independently compress each ELF using single-stream xz preset5; difference estimates marginal clang payload, not a rebuilt RPM; cpio and cross-file compression not modeled.','files':rows,'estimated_rpm_delta_bytes':rows['symbols']['xz5_stream_bytes']-rows['final']['xz5_stream_bytes']})

def correctness():
 units=json.loads((W/'docs/53_hybrid_local_validation_evidence/tu-inputs.json').read_text());keys=list(dict.fromkeys(u['key'].rsplit('/',1)[0] for u in units))[:5];selected=[u for u in units if u['key'].rsplit('/',1)[0] in keys];assert len(selected)==15
 slot=D/'same-clang';slot.touch();inode=slot.stat().st_ino;result={}
 for role in ['final','symbols']:
  shutil.copyfile(D/('clang.'+role),slot);slot.chmod(0o755);assert slot.stat().st_ino==inode
  for u in selected:
   i=u['index'];out=D/('tu-'+str(i)+'.o');args=list(u['original_argv'][1:]);args.insert(0,'--no-default-config');args[args.index('-c')+1]=u['copy'];args[args.index('-o')+1]=str(out);args=[('-resource-dir='+str(BUILD/'lib64/clang/22') if x.startswith('-resource-dir=') else x) for x in args];assert sha(u['copy'])==u['sha256']
   run('tu-'+role+'-'+str(i),['taskset','-c','2',*LOADER,slot,*args],timeout=180)
   if role=='final':shutil.copyfile(out,D/('ref-'+str(i)+'.o'));result[i]={'key':u['key'],'target':u['target'],'final_sha':sha(out)}
   else:result[i].update(symbols_sha=sha(out),equal=out.read_bytes()==(D/('ref-'+str(i)+'.o')).read_bytes());assert result[i]['equal']
 save('correctness.json',{'PASS':True,'pairs':15,'same_inode':inode,'results':result})

if __name__=='__main__':
 status=[]
 for name,fn in [('prepare',prepare),('crash',crash),('layout_offline',layout_offline),('sizes',sizes),('correctness',correctness)]:
  try:fn();status.append({'step':name,'status':'completed'})
  except Exception:status.append({'step':name,'status':'partial','error':traceback.format_exc()})
  save('steps.json',status);print(json.dumps(status[-1]),flush=True)
