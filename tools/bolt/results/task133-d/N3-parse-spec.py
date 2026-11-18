from pathlib import Path
import difflib,itertools,json,os,re,shlex,subprocess,time
w=Path('/home/linhao/Toolchain/development/llvm-optimize'); e=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')/'tools/bolt/results/task133-d'; t=w/'temp/task133-d'; i=t/'I'; rv=t/'parse-n3'; rv.mkdir()
G='/usr/bin/git'; ps5='7b05a13744d1cf81a5e9cff22a27eb037bf1b6a8'
def git(repo,*args):
 return subprocess.check_output([G,'-C',str(repo),*args])
r=w/'temp/review-20261103/config-root/local/BUILD-ROOTS/scratch.x86_64.0'
m=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')/'tools/bolt/results/fifth-review-20261111/rerun4/parse'
cmd=[str(r/'usr/lib64/ld-linux-x86-64.so.2'),'--library-path',str(r/'usr/lib64'),str(r/'usr/bin/rpmspec')]
env=dict(os.environ,RPM_CONFIGDIR=str(r/'usr/lib/rpm'),LC_ALL='C')
show=subprocess.check_output([*cmd,'--showrc'],env=env,text=True)
ma=next(line.split(': ',1)[1] for line in show.splitlines() if line.startswith('Macro path:'))
ma=':'.join(x for x in ma.split(':') if x.startswith(str(r)))
old=rv/'PS5.spec'; old.write_bytes(git(i,'show',ps5+':packaging/llvm.spec'))
new=i/'packaging/llvm.spec'
sub=i/'packaging/llvm-tools-subpkgs.spec'
def run(spec,arch,opts=(),phase='-P'):
 mk='toolchain-'+('x86-debug' if arch in ('x86_64','i586') else arch)
 # Keep the same macro and Source path for both specs.
 args=[*cmd,phase,'--define','_topdir '+str(rv/'rpm'),'--define','_builddir '+str(rv/'rpm/BUILD'),'--macros',ma+':'+str(m/(mk+'.macros')),
       '--target',arch+'-tizen-linux','--define','_sourcedir '+str(i/'packaging'),'--define','_toolchain clang',*opts,str(spec)]
 return subprocess.run(args,env=env,text=True,capture_output=True)
checks=[]
def compare(tag,arch,a,b,opts=(),phase='-P'):
 l=run(a,arch,opts,phase); r=run(b,arch,opts,phase)
 (rv/(tag+'-ps5.txt')).write_text(l.stdout); (rv/(tag+'-I.txt')).write_text(r.stdout)
 diff=''.join(difflib.unified_diff(l.stdout.splitlines(True),r.stdout.splitlines(True),'PS5','I'))
 (rv/(tag+'.diff')).write_text(diff)
 checks.append(dict(tag=tag,arch=arch,rc=[l.returncode,r.returncode],stderr=[l.stderr,r.stderr],delta=diff))
for arch in ('x86_64','aarch64','armv7l'):
 compare(f'default-{arch}',arch,old,new)
for bits in itertools.product((0,1),repeat=3):
 args=[]
 for macro,bit in zip(('llvm_speedup','hybrid_link','clang_bolt'),bits):
  args+=['--define',f'_{("with" if bit else "without")}_{macro} 1']
 compare('switch-'+''.join(map(str,bits)),'x86_64',old,new,args)
roll=[]
for name,spec in (('ps5',old),('I',new)):
 f=rv/(name+'-rollback.spec'); txt=spec.read_text(); assert txt.count('%bcond_without clang_bolt')==1
 f.write_text(txt.replace('%bcond_without clang_bolt','%bcond_with clang_bolt')); roll.append(f)
for tag,arch,a,b,args in (
 ('five-on','x86_64',old,new,()),('five-off','x86_64',old,new,('--define','_without_clang_bolt 1')),
 ('five-armv7l','armv7l',old,new,()),('five-aarch64','aarch64',old,new,()),('five-rollback','x86_64',*roll,())):
 compare(tag,arch,a,b,args,phase='-P')
subrows=[]
for arch in ('x86_64','aarch64','armv7l','i586'):
 r=run(sub,arch)
 lines=[x for x in r.stdout.splitlines() if re.search(r'^BuildRequires|^Requires|^ExclusiveArch|BOLT_TARGETS_TO_BUILD|LLVM_LIBDIR_SUFFIX|_libdir',x)]
 if r.stdout: (rv/f'subpkg-{arch}.stdout').write_text(r.stdout)
 subrows.append(dict(arch=arch,rc=r.returncode,stderr=r.stderr,lines=lines))
 if arch in ('armv7l','i586'):
  # rpmspec -P can still print an architecture-excluded spec.
  query=run(sub,arch,('--qf','%{name}\n'),phase='-q')
  subrows[-1]['query']={'rc':query.returncode,'stdout':query.stdout,'stderr':query.stderr}
(e/'N3-spec.json').write_text(json.dumps(dict(main=checks,subpackages=subrows),indent=2)+'\n')
print('parsed',len(checks),[x['tag'] for x in checks if any(x['rc'])]); print(json.dumps(subrows,indent=2))
