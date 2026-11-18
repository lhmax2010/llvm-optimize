from pathlib import Path
import hashlib,json,os,re,shlex,subprocess,time
w=Path('/home/linhao/Toolchain/development/llvm-optimize'); e=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')/'tools/bolt/results/task133-d'; t=w/'temp/task133-d'
r=w/'temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
h=w/'temp/rebase-359934-20261111-r6/toolchain/evidence/rpm-build.log'
tools=t/'tizen-tools/bin'; i=t/'I'
g='/usr/bin/git'
env=dict(os.environ,PATH=f'{tools}:/usr/bin:/bin',LC_ALL='C')
env.pop('LD_LIBRARY_PATH',None)
def git(path,*args):
 return subprocess.check_output([g,'-C',str(path),*args],stderr=subprocess.STDOUT).decode().strip()
def source(name,rev):
 path=t/f'src-{name}'
 if path.exists():
  assert git(path,'rev-parse','HEAD')==rev
  return path
 git(i,'worktree','add','--detach','--no-checkout',str(path),rev)
 git(path,'sparse-checkout','init','--no-cone')
 git(path,'sparse-checkout','set',*[f'/{d}/' for d in ('llvm','cmake','clang','lldb','clang-tools-extra','lld','compiler-rt','openmp','bolt','third-party')])
 git(path,'reset','--merge')
 return path
base='7b05a13744d1cf81a5e9cff22a27eb037bf1b6a8'
rev_raw=git(i,'rev-list','--reverse',base+'..HEAD').splitlines()[0]
with h.open(errors='replace') as f:
 for pos,line in enumerate(f,1):
  if '+ cmake -G Ninja -DTIZEN=1' in line:
   orig=shlex.split(line.split('+ cmake ',1)[1])[2:-1]; break
assert any(x=='-DLLVM_ENABLE_LTO=Thin' for x in orig)
rows=[]
for name,rev in [('ps5',base),('raw',rev_raw),('I',git(i,'rev-parse','HEAD'))]:
 try: src=source(name,rev)
 except subprocess.CalledProcessError as exc:
  print(exc.output.decode());raise
 build=t/f'cfg2-{name}'; log=t/f'N3-cmake2-{name}.log'; argv=[str(tools/'cmake'),'-G','Ninja','-S',str(src/'llvm'),'-B',str(build),'-DCMAKE_MAKE_PROGRAM='+str(tools/'ninja'),'-DCMAKE_SYSROOT='+str(r)]
 for a in orig:
  k,sep,v=a.partition('=')
  if k in ('-DCMAKE_C_COMPILER','-DCMAKE_CXX_COMPILER','-DCMAKE_AR','-DCMAKE_RANLIB'):
   v=str(tools/Path(v).name)
  elif k=='-DLLVM_ENABLE_PROJECTS':
   v+=';bolt'
  elif k=='-DLLVM_BINUTILS_INCDIR':
   v=str(r/v.removeprefix('/'))
  elif k in ('-DCMAKE_EXE_LINKER_FLAGS','-DCMAKE_SHARED_LINKER_FLAGS') and name!='ps5':
   v+=' -Wl,--build-id=sha1'
  if '/home/abuild/rpmbuild' in v:
   v=v.replace('/home/abuild/rpmbuild',str(r/'home/abuild/rpmbuild'))
  if k in ('-DCMAKE_C_FLAGS','-DCMAKE_CXX_FLAGS','-DCMAKE_ASM_FLAGS'):
   v+=' -resource-dir='+str(r/'usr/lib64/clang/22')
  argv.append(k+sep+v)
 argv+=['-DBOLT_BUILD_TOOLS=OFF','-DBOLT_ENABLE_RUNTIME=ON','-DBOLT_INCLUDE_TESTS=OFF','-DBOLT_TARGETS_TO_BUILD=X86']
 start=time.monotonic(); status='finished'
 with log.open('w') as f:
  try:
   run=subprocess.run(argv,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=2700)
   rc=run.returncode
  except subprocess.TimeoutExpired:
   rc=None;status='timeout 45 min'
 data=log.read_text(errors='replace')
 lines=data.splitlines()
 block=[]; linklines=[]; runtime=[]
 if (build/'build.ninja').exists():
  with (build/'build.ninja').open() as f:
   for line in f:
    if 'X86BoltMnemonicTables.cpp.' in line and 'LLVMBOLTTargetX86' in line:
     block.append(line.strip())
    if line.startswith('build bin/llvm-bolt:'):
     linklines=[next(f).strip() for _ in range(12)]
    if 'ExternalProject' in line: continue
    if ('bolt_rt' in line and ('-DCMAKE_C_FLAGS' in line or '-DCMAKE_CXX_FLAGS' in line)):
     runtime.append(line.strip())
 row=dict(variant=name,rev=rev,source=str(src),cwd=str(build),argc=len(argv),argv=argv,result=status,rc=rc,seconds=round(time.monotonic()-start,3),log=str(log),bytes=log.stat().st_size,sha256=hashlib.sha256(log.read_bytes()).hexdigest(),tail=lines[-35:],mirror=block,link=linklines,runtime=runtime)
 rows.append(row);(e/'N3-cmake2.json').write_text(json.dumps(dict(argv_source=str(h),argv_source_line=pos,configs=rows),indent=2)+'\n')
 print(name,rc,status,row['seconds'],flush=True)
 if rc!=0: print('\n'.join(lines[-18:]),flush=True)
