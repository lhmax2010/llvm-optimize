from pathlib import Path
import subprocess as sp,hashlib,json,re,os,shlex,difflib
W=Path.cwd();E=W/'temp/hybrid-link-20261015';S=E/'source';R=W/'temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0'
base=(E/'base.txt').read_text().strip()
def run(args,**kw):return sp.check_output([str(x) for x in args],**kw)
files=run(['git','-C',W/'temp/llvm-hybrid-trial','diff','--name-only'],text=True).splitlines();files.remove('packaging/llvm.spec')
patch=run(['git','-C',W/'temp/llvm-hybrid-trial','diff','--',*files]);(E/'source-port.diff').write_bytes(patch)
sp.run(['git','-C',str(S),'apply','--check','-'],input=patch,check=True)
# Keep original source for the first configuration (b); apply later.
old=run(['git','-C',S,'show',base+':packaging/llvm.spec'],text=True);(E/'baseline.spec').write_text(old)
needle='%ifarch x86_64\n    -DLLVM_LINK_LLVM_DYLIB=OFF \\\n    -DCLANG_LINK_CLANG_DYLIB=OFF \\\n'
assert old.count(needle)==1
new=old.replace(needle,'%ifarch x86_64\n    -DLLVM_LINK_LLVM_DYLIB=ON \\\n    -DCLANG_LINK_CLANG_DYLIB=ON \\\n    -DTIZEN_HYBRID_LINK=ON \\\n    -DBUILD_SHARED_LIBS=OFF \\\n    -DLLVM_TOOL_LLVM_DRIVER_BUILD=OFF \\\n')
(E/'hybrid.spec').write_text(new);(S/'packaging/llvm.spec').write_text(new)
loader=[R/'lib64/ld-linux-x86-64.so.2','--library-path',str(R/'lib64')+':'+str(R/'usr/lib64'),R/'usr/bin/rpmspec']
summary=[]
for arch in ['x86_64','armv7l','aarch64']:
 M=R if arch=='x86_64' else Path('/home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS')/('scratch.'+arch+'.0')
 showfile=W/('temp/target-recipe-policy-check-20261009/root-showrc.stdout' if arch=='x86_64' else 'temp/arm-archive-feasibility-20261009/'+arch+'-native-showrc.stdout')
 paths=re.search(r'^Macro path: (.*)$',showfile.read_text(),re.M)[1].split(':')
 # Old ARM records may already include paths: relocate only root-relative RPM paths.
 paths=[str(M/'home/abuild/.rpmmacros') if p=='~/.rpmmacros' else str(M)+p if p.startswith(('/usr/','/etc/')) else p for p in paths]
 env=dict(os.environ,HOME=str(M/'home/abuild'),RPM_CONFIGDIR=str(M/'usr/lib/rpm'))
 args=loader+['--rcfile',str(M/'usr/lib/rpm/rpmrc')+':'+str(M/'home/abuild/.rpmrc'),'--macros',':'.join(paths),'--target='+arch,'--define','_smp_mflags -j4','--define','_srcdefattr (-,root,root)','--nosignature','--define','_build_create_debug 1','--define','_topdir /home/abuild/rpmbuild']
 (E/(arch+'-rpmspec-argv.json')).write_text(json.dumps([str(x) for x in args],indent=2))
 opt=run(args+['--eval','%{optflags}'],env=env,text=True).strip();(E/(arch+'-optflags.txt')).write_text(opt+'\n')
 stages={}
 for label in ['baseline','hybrid']:
  p=sp.run([str(x) for x in args+['--parse',E/(label+'.spec')]],env=env,text=True,capture_output=True)
  (E/(arch+'-'+label+'-parse.stderr')).write_text(p.stderr);p.check_returncode()
  (E/(arch+'-'+label+'-parsed.spec')).write_text(p.stdout)
  b=p.stdout.split('\n%build\n',1)[1].split('\n%install\n',1)[0];i=p.stdout.split('\n%install\n',1)[1].split('\n%files',1)[0]
  for st,txt in [('build',b),('install',i)]: (E/(arch+'-'+label+'-'+st+'.txt')).write_text(txt)
  stages[label]=(b,i)
  settings=b[b.index('OPTFLAGS_CFLAGS=' if arch=='x86_64' else 'MLGO_AOT_DIR='):b.index('mkdir -p build')]
  cmake=b[b.index('cmake \\\n'):].split('    ../llvm',1)[0]+'    ../llvm\n'
  capture='set -eu\nPWD=/tmp/hybrid52/source\nCFLAGS='+shlex.quote(opt)+'\nCXXFLAGS='+shlex.quote(opt)+'\n'+settings+cmake.replace('cmake \\\n',"printf '%s\\n' \\\n",1)
  (E/(arch+'-'+label+'-capture.sh')).write_text(capture)
  argv=run(['bash','--noprofile','--norc','-c',capture],text=True).splitlines()
  (E/(arch+'-'+label+'-cmake.json')).write_text(json.dumps(argv,indent=2)+'\n')
 for n,st in enumerate(['build','install']):
  a,b=stages['baseline'][n],stages['hybrid'][n];(E/(arch+'-'+st+'.diff')).write_text(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True))))
  summary.append(dict(arch=arch,stage=st,identical=a==b,baseline_sha256=hashlib.sha256(a.encode()).hexdigest(),hybrid_sha256=hashlib.sha256(b.encode()).hexdigest()))
  if arch!='x86_64' or st=='install':assert a==b
(E/'macro-comparison.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
