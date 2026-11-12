from pathlib import Path
import json,subprocess,shutil,hashlib,datetime,traceback
from compare_functions import compare,ELF,normal
E=Path(__file__).resolve().parent
cfg=json.loads((E/'platform-tools.json').read_text())
tools=cfg['tools'];prefix=[tools['loader']['path'],'--library-path',cfg['library_path']]
fixtures=E/'fixtures';fixtures.mkdir(exist_ok=False)
(fixtures/'tmp').mkdir()
scratch=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/td-function-diff-20261113');scratch.mkdir(exist_ok=False)
results={}
def run(tool,args,label):
 argv=prefix+[tools[tool]['path']]+list(map(str,args))
 with (E/'fixture-commands.jsonl').open('a') as f:f.write(json.dumps({'argv':argv,'cwd':str(fixtures)})+'\n')
 p=subprocess.run(argv,cwd=fixtures,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 (fixtures/(label+'.stdout')).write_bytes(p.stdout);(fixtures/(label+'.stderr')).write_bytes(p.stderr)
 assert p.returncode==0,(label,p.returncode,p.stderr.decode())
def checkpoint():
 (E/'known-answer-results.json').write_text(json.dumps(results,indent=2)+'\n')
try:
 inputs=json.loads((E/'inputs.json').read_text())
 T=Path(inputs['toolchain']['path']);copy=scratch/'toolchain-copy.elf'
 shutil.copyfile(T,copy)
 with copy.open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==inputs['toolchain']['sha256']
 a=compare(T,copy,E/'self-copy')
 assert a['counts'].get('identical',0)==a['left_functions']==a['right_functions'],a
 results['a']={'status':'PASS','result':a};checkpoint()
 print('a PASS',a['left_functions'],flush=True)
 # Single known function differs. Both functions stay exported and un-inlined.
 for variant,constant in [('before',7),('after',9)]:
  source=fixtures/('single-'+variant+'.c')
  source.write_text('__attribute__((noinline)) int changed(int x) { return x + '+str(constant)+'; }\n__attribute__((noinline)) int unchanged(int x) { return x * 3; }\nint entry(int x) { return changed(x) + unchanged(x); }\n')
  obj=fixtures/('single-'+variant+'.o');elf=fixtures/('single-'+variant+'.elf')
  run('clang',['-O2','-c',source,'-o',obj],'single-'+variant+'-compile')
  run('lld',['--emit-relocs','--export-dynamic','--entry=entry','--build-id=none','-o',elf,obj],'single-'+variant+'-link')
 b=compare(fixtures/'single-before.elf',fixtures/'single-after.elf',E/'single-function')
 import gzip
 with gzip.open(E/'single-function/differences.json.gz','rt') as f:d=json.load(f)
 assert len(d)==1 and d[0]['key'][0]=='changed' and d[0]['category']=='machine_code_different',d
 results['b']={'status':'PASS','result':b,'different_name':'changed'};checkpoint();print('b PASS',flush=True)
 (fixtures/'main.c').write_text('extern int bar(int); int entry(int x) { return bar(x) + 1; }\n')
 (fixtures/'lib.c').write_text('__attribute__((noinline)) static int local_fn(int x) { return x*3+5; }\nint bar(int x) { return local_fn(x); }\n')
 for variant,flags in [('nodebug',[]),('debug',['-g'])]:
  objs=[]
  for stem in ('main','lib'):
   obj=fixtures/(variant+'-'+stem+'.bc');objs.append(obj)
   run('clang',['-O2','-flto=thin',*flags,'-c',fixtures/(stem+'.c'),'-o',obj],variant+'-'+stem+'-compile')
  run('lld',['--emit-relocs','--export-dynamic','--entry=entry','--build-id=none','-o',fixtures/(variant+'.elf'),*objs],variant+'-link')
 c=compare(fixtures/'nodebug.elf',fixtures/'debug.elf',E/'module-hash')
 symbols=[]
 for name in ('nodebug','debug'):
  elf=ELF(fixtures/(name+'.elf'));symbols.append([r['name'] for r in elf.functions if normal(r['name'])!=r['name']]);elf.close()
 results['c']={'status':'PASS' if c['counts'].get('identical',0)==c['left_functions']==c['right_functions'] and symbols[0]!=symbols[1] and all(symbols) else 'FAIL','result':c,'promoted_symbols':symbols}
 checkpoint()
 assert results['c']['status']=='PASS',results['c']
 print('c PASS',symbols,flush=True)
except BaseException:
 (E/'known-answer-failure.txt').write_text(traceback.format_exc())
 checkpoint();print(traceback.format_exc(),flush=True);raise
finally:
 print('已结束',datetime.datetime.now().astimezone().isoformat(),'comparator-known-answers',flush=True)
