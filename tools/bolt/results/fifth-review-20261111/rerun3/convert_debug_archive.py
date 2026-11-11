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
log=(E/('debug-conversion-%02d.stdout'%index)).open('w')
class Tee:
 def write(self,s):sys.__stdout__.write(s);log.write(s);log.flush()
 def flush(self):sys.__stdout__.flush();log.flush()
sys.stdout=Tee()
stage='prepare';done=threading.Event()
def monitor():
 while not done.wait(30):
  print('CONVERSION_PROGRESS',datetime.datetime.now().astimezone().isoformat(),name,stage,'free_bytes='+str(shutil.disk_usage(X).free),flush=True)
thread=threading.Thread(target=monitor,daemon=True);thread.start()
result=dict(archive=name,input=source,debug_info='yes',jobs=1,status='failed',runs={},all_relocations={},debug_relocations={},unknown_types=[])
start=time.monotonic()
try:
 root=X/'input';root.mkdir();shutil.copy2(source['copy'],root/name);assert sha(root/name)==source['sha256']
 info=new.inspect(root/name);assert info['bitcode']>0 and not info['thin'];result['input_members']=info['member_count'];result['input_bitcode']=info['bitcode']
 build=X/'build';build.mkdir();shutil.copy2(BUILD/'CMakeCache.txt',build/'CMakeCache.txt')
 tools=X/'tools';tools.mkdir()
 paths={}
 for filename in ('clang-22','llvm-dis','llvm-nm'):
  binary=R/'usr/bin'/filename;assert binary.is_file()
  argv=[str(R/'lib64/ld-linux-x86-64.so.2'),'--library-path',str(R/'lib64')+':'+str(R/'usr/lib64'),str(binary)]
  wrapper=tools/filename;wrapper.write_text('#!/bin/sh\nexec '+shlex.join(argv)+' "$@"\n');wrapper.chmod(0o755);paths[filename]=wrapper
  result.setdefault('tools',{})[filename]=dict(source=str(binary),source_sha256=sha(binary),wrapper=str(wrapper),wrapper_sha256=sha(wrapper),argv=argv)
 outputs={}
 for label,mod in [('old',old),('new',new)]:
  stage=label;tick=time.monotonic();out=X/label
  print('CONVERSION_START',name,label,datetime.datetime.now().astimezone().isoformat(),flush=True)
  summary=mod.convert(root,out,paths['clang-22'],paths['llvm-dis'],paths['llvm-nm'],build,jobs=1,debug_info='yes')
  assert summary['status']=='CONVERTED'
  target=out/'archives'/name;outputs[label]=target
  result['runs'][label]=dict(sha256=sha(target),bytes=target.stat().st_size,seconds=time.monotonic()-tick,output=str(target),summary=str(out/'summary.json'),converted=summary['archives'][0]['converted'],preserved=summary['archives'][0]['preserved'])
 stage='compare'
 assert result['runs']['old']['sha256']==result['runs']['new']['sha256'],result['runs']
 assert result['runs']['old']['bytes']==result['runs']['new']['bytes']
 a=new.inspect(outputs['old']);b=new.inspect(outputs['new']);assert a==b
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
 result['failure']=traceback.format_exc();print(result['failure'],flush=True);raise
finally:
 done.set();thread.join();result['seconds']=time.monotonic()-start
 (E/('debug-conversion-%02d.json'%index)).write_text(json.dumps(result,indent=2)+'\n')
 print('DEBUG_CONVERSION 已结束',datetime.datetime.now().astimezone().isoformat(),'archive='+name,'status='+result['status'],flush=True)
