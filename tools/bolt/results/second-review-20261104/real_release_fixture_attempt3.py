"""C-2 #5/#6: synthetic bitcode made with this rehearsal's installed clang.
Not a real Base-Dev package member; replace with one after the full build.
"""
from pathlib import Path
import hashlib,importlib.util,json,os,re,shlex,shutil,subprocess,sys
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';E=Path(__file__).parent/'synthetic-retry03';E.mkdir()
R=W/'temp/second-review-20261104/toolchain-rehearsal/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
X=W/'temp/second-review-20261104/synthetic-release-retry03';X.mkdir()
S=W/'temp/review-20261102/source';sp=importlib.util.spec_from_file_location('converter',S/'packaging/llvm-static-archives-native.py');a=importlib.util.module_from_spec(sp);sp.loader.exec_module(a)
wr=X/'tools';wr.mkdir();tools={};records=[]
for name in ('clang-22','llvm-dis','llvm-as','llvm-nm'):
 p=R/'usr/bin'/name;assert p.is_file(),p
 q=wr/name;q.write_text('#!/bin/sh\nexec '+shlex.join([str(R/'usr/lib64/ld-linux-x86-64.so.2'),'--argv0',str(p),'--library-path',str(R/'usr/lib64'),str(p)])+' "$@"\n');q.chmod(0o755);tools[name]=str(q)
 records.append({'tool':name,'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'wrapper':q.read_text()})
def run(name,argv):
 p=subprocess.run(argv,cwd=X,capture_output=True,text=True)
 (E/(name+'.stdout')).write_text(p.stdout);(E/(name+'.stderr')).write_text(p.stderr);(E/(name+'.json')).write_text(json.dumps({'argv':argv,'rc':p.returncode},indent=2)+'\n')
 assert p.returncode==0,(name,p.stderr)
 return p.stdout
# Clang resolves /proc/self/exe when recording commands, so loader --argv0
# alone still records the loader. Execute a private copy directly with the
# same loader selected by its temporary PT_INTERP; no production file changes.
compiler=X/'compiler/clang-22';compiler.parent.mkdir();shutil.copyfile(R/'usr/bin/clang-22',compiler);compiler.chmod(0o755)
run('synthetic-compiler-interpreter',['patchelf','--set-interpreter',str(R/'usr/lib64/ld-linux-x86-64.so.2'),str(compiler)])
os.environ['LD_LIBRARY_PATH']=str(R/'usr/lib64')
tools['clang-22']=str(compiler)
records.append({'private_compiler':str(compiler),'sha256':hashlib.sha256(compiler.read_bytes()).hexdigest(),'modification':'PT_INTERP only, private fixture copy; same rehearsal tool code'})
source=X/'fixture.c';source.write_text('int synthetic_release_member(int x) { return x * 17 + 3; }\n')
rows=json.loads((E.parent/'policy-observed.json').read_text());row=next(r for r in rows if r['mode']==1 and r['kind']=='CFLAGS' and '-feliminate-unused-debug-types' in r['input'] and '-fcf-protection' not in r['input'] and r['rc']==0 and r['extra']=='')
fixed=row['stdout'].split('FLAGS_RESULT\n')[-1].split('\0')[0];flags=shlex.split(fixed);assert not any(x.startswith('-g') for x in flags)
base=[tools['clang-22'],'--target=x86_64-tizen-linux-gnu','-resource-dir',str(R/'usr/lib64/clang/22'),*flags,'-fPIC']
run('synthetic-release-compile',base+['-c',str(source),'-o',str(X/'release.bc')])
run('synthetic-debug-compile',base+['-g','-gdwarf-4','-c',str(source),'-o',str(X/'debug.bc')])
release=run('synthetic-release-dis',[tools['llvm-dis'],str(X/'release.bc'),'-o','-']);debug=run('synthetic-debug-dis',[tools['llvm-dis'],str(X/'debug.bc'),'-o','-'])
settings=a.ir_settings(release.splitlines(True),debug_info='no');assert not any(x.startswith('-g') for x in settings['flags'])
# Keep real debug metadata but remove only -g tokens from its recorded command;
# this models malformed release IR and must be rejected after backend emission.
assert '!llvm.dbg.cu' in debug
mid=re.search(r'!llvm.commandline = !\{!(\d+)\}',debug).group(1)
pattern=r'^!'+mid+r' = .*?$'
line=re.search(pattern,debug,re.M).group(0);new=line.replace(' -g -gdwarf-4','')
assert new!=line
bad=re.sub(pattern,lambda _:new,debug,flags=re.M);a.ir_settings(bad.splitlines(True),debug_info='no')
(X/'release-with-debug.ll').write_text(bad)
run('synthetic-negative-assemble',[tools['llvm-as'],str(X/'release-with-debug.ll'),'-o',str(X/'release-with-debug.bc')])
results=[]
for label,bc,expected in [('positive','release.bc','CONVERTED'),('negative','release-with-debug.bc','release conversion unexpectedly emitted debug sections')]:
 root=X/(label+'-root');root.mkdir();build=X/(label+'-build');build.mkdir();(build/'CMakeCache.txt').write_text('# Synthetic one-member fixture; no CMake invocation.\n')
 run('synthetic-'+label+'-archive',['/usr/bin/ar','qcDS',str(root/'fixture.a'),str(X/bc)])
 try:
  result=a.convert(root,build/'evidence',tools['clang-22'],tools['llvm-dis'],tools['llvm-nm'],build,jobs=1,debug_info='no')
 except ValueError as error:
  assert label=='negative' and str(error)==expected,str(error);results.append({'case':label,'PASS':True,'expected_error':str(error)})
 else:
  assert label=='positive' and result['status']==expected
  inspected=a.inspect(build/'evidence/archives/fixture.a');assert all(not m['debug_sections'] for m in inspected['members'])
  results.append({'case':label,'PASS':True,'status':result['status'],'debug_sections':[m['debug_sections'] for m in inspected['members']], 'result':result})
(E/'real-release-fixture.json').write_text(json.dumps({'synthetic':True,'not_full_release_build':True,'tools':records,'flags':flags,'recorded_command':settings['recorded_command'],'results':results},indent=2)+'\n')
print('CLAUDE_C2_SYNTHETIC_RELEASE_PASS 2/2')
