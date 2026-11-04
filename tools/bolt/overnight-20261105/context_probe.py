from pathlib import Path
import sys,json,subprocess,hashlib,shlex,re,datetime,difflib,os
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize';E=B/'tools/bolt/results/baseline-attribution-20261105';O=W/'temp/attribution-20261105/probe';O.mkdir(parents=True,exist_ok=False)
ROOTS={'old':W/'temp/debuglink-20261028/full-20261030','new':W/'temp/night-20261103/toolchain'}
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
result={};configs={};rootmap={};contexts={}
try:
 for side,top in ROOTS.items():
  r=top/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';src=r/'home/abuild/rpmbuild/BUILD/llvm-22.1.8';b=src/'build';rootmap[side]=(r,src,b)
  cache={}
  for i,l in enumerate((b/'CMakeCache.txt').read_text().splitlines(),1):
   if l.startswith(('CMAKE_C_FLAGS:','CMAKE_CXX_FLAGS:','CMAKE_MODULE_LINKER_FLAGS:','CMAKE_EXE_LINKER_FLAGS:','CMAKE_SHARED_LINKER_FLAGS:')):cache[l.split(':')[0]]=l.split('=',1)[1]
  configs[side]=cache;anchors=[]
  logs=list((top/'gbs-driver/local/repos').glob('**/logs/success/**/log.txt'))
  if not logs and (top/'rpm-build.log').is_file():logs=[top/'rpm-build.log']
  for log in logs:
   with log.open(errors='replace') as f:
    for i,l in enumerate(f,1):
     if '+ cmake -G Ninja' in l and '-DCMAKE_C_FLAGS=' in l:anchors.append({'file':str(log),'line':i,'text':l.rstrip()})
  ninja=(b/'build.ninja').read_text();lines=ninja.splitlines();blocks=[]
  for i,l in enumerate(lines):
   if l.startswith('build ') and ('ompdModule.so' in l or ('builtins' in l and 'absvdi2.c.o:' in l) or 'blake3_portable.c.o:' in l):
    j=i+1
    while j<len(lines) and lines[j]:j+=1
    blocks.append({'file':str(b/'build.ninja'),'line':i+1,'text':'\n'.join(lines[i:j])})
  probe_block=next(z['text'] for z in blocks if 'blake3_portable.c.o:' in z['text'])
  configs[side]['probe_FLAGS']=next(l.split(' = ',1)[1] for l in probe_block.splitlines() if l.startswith('  FLAGS = '))
  configs[side]['probe_DEFINES']=next(l.split(' = ',1)[1] for l in probe_block.splitlines() if l.startswith('  DEFINES = '))
  configs[side]['probe_INCLUDES']=next(l.split(' = ',1)[1] for l in probe_block.splitlines() if l.startswith('  INCLUDES = '))
  add=src/'llvm/cmake/modules/AddLLVM.cmake';(E/(side+'-AddLLVM-source.cmake')).write_bytes(add.read_bytes())
  contexts[side]={'cache_path':str(b/'CMakeCache.txt'),'cache_sha':sha(b/'CMakeCache.txt'),'flags':cache,'configure_log':anchors,'ninja_blocks':blocks,'AddLLVM_source':str(add),'AddLLVM_sha':sha(add)}
 save(E/'configuration-evidence.json',contexts)
 repo=W/'temp/review-20261102/source'
 gp=subprocess.run(['git','-C',str(repo),'diff','6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2','d4d6ca16b55a9afcb64a30ebf634f340f968267b','--','llvm/cmake/modules/AddLLVM.cmake'],capture_output=True)
 (E/'AddLLVM-hybrid-commit.diff').write_bytes(gp.stdout);(E/'AddLLVM-hybrid-commit.stderr').write_bytes(gp.stderr)
 result['git_diff_rc']=gp.returncode
 (E/'AddLLVM-source.diff').write_text(''.join(difflib.unified_diff((E/'old-AddLLVM-source.cmake').read_text().splitlines(True),(E/'new-AddLLVM-source.cmake').read_text().splitlines(True),fromfile=contexts['old']['AddLLVM_source'],tofile=contexts['new']['AddLLVM_source'])))
 r,src,b=rootmap['new'];source=src/'llvm/lib/Support/BLAKE3/blake3_portable.c';oldsource=rootmap['old'][1]/'llvm/lib/Support/BLAKE3/blake3_portable.c';assert sha(source)==sha(oldsource)
 loader=r/'lib64/ld-linux-x86-64.so.2';lib=str(r/'usr/lib64')+':'+str(r/'lib64');clang=r/'usr/bin/clang-22';analyzer=r/'usr/bin/llvm-bcanalyzer';prefix=[str(loader),'--library-path',lib]
 result['tools']=[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in (loader,clang,analyzer,source)]
 result['source_same_sha']=sha(source);runs=[]
 for label,flags in [('old',configs['old']['probe_FLAGS']),('new',configs['new']['probe_FLAGS']),('repeat',configs['new']['probe_FLAGS'])]:
  argv=prefix+[str(clang),'--sysroot='+str(r),'-resource-dir='+str(r/'usr/lib64/clang/22'),*shlex.split(flags),*shlex.split(configs['new']['probe_DEFINES']),*[v.replace('/home/abuild/',str(r)+'/home/abuild/') for v in shlex.split(configs['new']['probe_INCLUDES'])],'-c',str(source),'-o','-'];out=O/(label+'.bc');err=O/(label+'.stderr');env=dict(os.environ,TMPDIR=str(O));start=datetime.datetime.now().astimezone().isoformat()
  with out.open('xb') as so,err.open('xb') as se:p=subprocess.run(argv,stdout=so,stderr=se,cwd=O,env=env)
  row={'label':label,'argv':argv,'rc':p.returncode,'start':start,'end':datetime.datetime.now().astimezone().isoformat(),'output':str(out),'bytes':out.stat().st_size,'sha256':sha(out),'stderr':err.read_text(errors='replace')};runs.append(row)
  if p.returncode:result['status']='partial';result['reason']='single-file-compile-failed';break
  aa=prefix+[str(analyzer),'-dump',str(out)];ar=subprocess.run(aa,capture_output=True,cwd=O);(O/(label+'-bcanalyzer.stdout')).write_bytes(ar.stdout);(O/(label+'-bcanalyzer.stderr')).write_bytes(ar.stderr);row['analyzer_argv']=aa;row['analyzer_rc']=ar.returncode;row['module_hash_lines']=[l for l in ar.stdout.decode(errors='replace').splitlines() if re.search(r'<HASH\b',l)]
  if ar.returncode:result['status']='partial';result['reason']='analyzer-failed';break
 result['runs']=runs
 if len(runs)==3 and all(x['rc']==0 and x.get('analyzer_rc')==0 for x in runs):
  result.update(status='ok',old_new_module_hash_equal=runs[0]['module_hash_lines']==runs[1]['module_hash_lines'],same_flags_module_hash_equal=runs[1]['module_hash_lines']==runs[2]['module_hash_lines'],same_flags_bitcode_sha_equal=runs[1]['sha256']==runs[2]['sha256'])
except BaseException as ex:result.update(status='stopped',reason=str(ex))
finally:
 save(E/'thinlto-probe.json',result);line='THINLTO_PROBE 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status='+result.get('status','stopped')+' reason='+result.get('reason','complete');(E/'thinlto-probe-end.txt').write_text(line+'\n');print(line,flush=True)
