from pathlib import Path
import gzip,importlib.util,json,os,shlex,subprocess
w=Path('/home/linhao/Toolchain/development/llvm-optimize'); b=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt'); t=w/'temp/task133-d'; e=b/'tools/bolt/results/task133-d'; q=t/'B-historical-fixture';q.mkdir()
p=b/'tools/bolt/results/pgo-resource-full-20261104/full/stage-D/evidence/D/processes.jsonl.gz'
r=w/'temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
tools=t/'tizen-tools/bin'; env=dict(os.environ,LD_LIBRARY_PATH=f'{r}/usr/lib64:{r}/lib64')
with gzip.open(p,'rt') as f:
 for n,line in enumerate(f,1):
  if '-fprofile-instr-use' in line and '/llvm/lib/Support/' in line:
   origin=json.loads(line)['cmdline']; break
raw=shlex.split(origin)
profile=w/'temp/pgo-profiles-keep-20261102/clang.profdata'
src=q/'fixture.cpp'; obj=q/'fixture.o'; ll=q/'fixture.ll'; converted=q/'converted.o'
src.write_text('extern "C" int counted(int x) { return x ? x+1 : x+2; }\n')
args=[]
for a in raw[1:]:
 if a.startswith('-fprofile-instr-use='): a='-fprofile-instr-use='+str(profile)
 elif a.startswith('-I/home/abuild/'): a='-I'+str(r/a[3:])
 elif a.endswith('BinaryStreamWriter.cpp.o'): a=str(obj)
 elif a.endswith('BinaryStreamWriter.cpp.o.d'): a=str(q/'fixture.d')
 elif a.endswith('/BinaryStreamWriter.cpp'): a=str(src)
 args.append(a)
rec=[]
def run(tool,*argv):
 cmd=[str(tools/tool),*map(str,argv)]
 result=subprocess.run(cmd,cwd=q,env=env,capture_output=True,text=True)
 rec.append(dict(argv=cmd,rc=result.returncode,stdout=result.stdout,stderr=result.stderr))
 (e/'B-historical-profile-commands.json').write_text(json.dumps(dict(log=str(p),line=n,original=origin,calls=rec),indent=2)+'\n')
 if result.returncode: raise RuntimeError(result.stderr)
run('clang++',*args)
run('llvm-dis',obj,'-o',ll)
file=w/'temp/task131/pgo-dev/packaging/llvm-static-archives-native.py'
module_spec=importlib.util.spec_from_file_location('converter',file)
mod=importlib.util.module_from_spec(module_spec); module_spec.loader.exec_module(mod)
ir=mod.ir_settings(ll.read_text().splitlines(),debug_info='yes')
assert [x['category'] for x in ir['policy']['tokens'] if x['token'].startswith('-fprofile-instr-use=')]==['ir']
assert not any(x.startswith('-fprofile') for x in ir['flags'])
run('clang-22',*ir['flags'],obj,'-o',converted)
assert mod.member_kind(converted.read_bytes())=='machine'
print('PASS historical ThinLTO converter fixture',p,n)
