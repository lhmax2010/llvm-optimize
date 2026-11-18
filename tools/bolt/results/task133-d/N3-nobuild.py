from pathlib import Path
import difflib,itertools,json,os,re,shlex,subprocess,time
w=Path('/home/linhao/Toolchain/development/llvm-optimize'); e=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')/'tools/bolt/results/task133-d'; t=w/'temp/task133-d'; i=t/'I'; rv=t/'parse-n3'
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
old=rv/'PS5.spec'
new=i/'packaging/llvm.spec'
sub=i/'packaging/llvm-tools-subpkgs.spec'
def run(spec,arch,opts=(),phase='-P'):
 mk='toolchain-'+('x86-debug' if arch in ('x86_64','i586') else arch)
 # Keep the same macro and Source path for both specs.
 args=[*cmd,phase,'--define','_topdir '+str(rv/'rpm'),'--define','_builddir '+str(rv/'rpm/BUILD'),'--macros',ma+':'+str(m/(mk+'.macros')),
       '--target',arch+'-tizen-linux','--define','_sourcedir '+str(i/'packaging'),'--define','_toolchain clang',*opts,str(spec)]
 if phase=='-bp':
  args[3]=str(r/'usr/bin/rpmbuild')
  args[5:5]=['--nodeps','--nobuild']
  (rv/'rpm').mkdir(exist_ok=True)
 return subprocess.run(args,env=env,text=True,capture_output=True)

rows=[]
for case,arch,opts,on in (
 ('on','x86_64',(),True),('off','x86_64',('--without','clang_bolt'),False),
 ('armv7l','armv7l',(),False),('aarch64','aarch64',(),False),('rollback','x86_64',(),False)):
 for side,file in [('PS5',old),('I',new)]:
  if case=='rollback': file=rv/(('ps5' if side=='PS5' else 'I')+'-rollback.spec')
  result=run(file,arch,opts,'-bp')
  x=run(file,arch,opts)
  got='BOLT_PROFILE_SOURCE=' in x.stdout
  rows.append(dict(case=case,side=side,arch=arch,rc=result.returncode,stdout=result.stdout,stderr=result.stderr,expanded_rc=x.returncode,expected_bolt=on,actual_bolt=got,pass_=result.returncode==x.returncode==0 and got==on))
for arch in ('x86_64','aarch64','armv7l','i586'):
 result=run(sub,arch,(),'-bp')
 expect_excluded=arch not in ('x86_64','aarch64')
 rows.append(dict(case='subpkg-arch-gate',arch=arch,rc=result.returncode,stdout=result.stdout,stderr=result.stderr,excluded=expect_excluded,pass_=bool(result.returncode and re.search('not included|not allowed',result.stderr,re.I)) if expect_excluded else result.returncode==0))
(e/'N3-nobuild.json').write_text(json.dumps(rows,indent=2)+'\n')
print([(x['case'],x.get('side',x['arch']),x['rc'],x['pass_'],x['stderr']) for x in rows])
exit(0 if all(x['pass_'] for x in rows) else 1)
