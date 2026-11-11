from pathlib import Path
import os,sys,json,shutil,hashlib,importlib.util,shlex,time,datetime,traceback,threading,collections
from relocation_census import census
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.with_name('llvm-optimize-bolt');E=Path(__file__).parent;S=W/'temp/rebase-359934-20261106/source';X=Path(os.environ['TEST_SCRATCH'])
R=W/'temp/night-20261105/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';BUILD=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build'
index=int(sys.argv[1]);source=json.loads((E/'debug-inputs.json').read_text())[index];name=Path(source['copy']).name
def load(label,path):
 spec=importlib.util.spec_from_file_location(label,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def sha(path):
 with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
old=load('old',W/'temp/fifth-review-20261111/rerun3/environment/baseline-llvm-static-archives-native.py')
new=load('new',S/'packaging/llvm-static-archives-native.py')

result=json.loads((E.parent/'rerun3/debug-conversion-00.json').read_text())
result.pop('failure',None)
result['status']='failed'
outputs={k:Path(v['output']) for k,v in result['runs'].items()}
info=new.inspect(Path(source['copy']))
assert sha(Path(source['copy']))==source['sha256']
for label,path in outputs.items():
 assert sha(path)==result['runs'][label]['sha256']
 assert path.stat().st_size==result['runs'][label]['bytes']
start=time.monotonic()
try:
 stage='compare'
 assert result['runs']['old']['sha256']==result['runs']['new']['sha256'],result['runs']
 assert result['runs']['old']['bytes']==result['runs']['new']['bytes']
 a=new.inspect(outputs['old']);b=new.inspect(outputs['new']);assert {k:v for k,v in a.items() if k!='path'}=={k:v for k,v in b.items() if k!='path'}
 counts=collections.Counter();debug=collections.Counter();checked=0
 with outputs['new'].open('rb') as stream:
  for member in b['members']:
   stream.seek(member['offset']);data=stream.read(member['size'])
   assert old.elf_details(data)==new.elf_details(data)
   op=old.pic_relocations(data);np=new.pic_relocations(data);assert op==np
   if not any(m['ordinal']==member['ordinal'] and m['kind']=='machine' for m in info['members']):assert not np['forbidden']
   checked+=np['checked']
   c,d=census(data);counts.update(c);debug.update(d)
 unknown=set(counts)-set(new.X86_64_RELOCATION_WIDTHS);assert not unknown,unknown
 result.update(status='ok',byte_identical=True,members=b['member_count'],checked_relocations=checked,all_relocations=dict(counts),debug_relocations=dict(debug),unknown_types=sorted(unknown))

except BaseException:
 result['failure']=traceback.format_exc()
 raise
finally:
 result['reused_outputs']=True
 result['verification_seconds']=time.monotonic()-start
 (E/'debug-conversion-00.json').write_text(json.dumps(result,indent=2)+'\n')
 print('DEBUG_RECHECK 已结束',datetime.datetime.now().astimezone().isoformat(),'status='+result['status'],flush=True)
