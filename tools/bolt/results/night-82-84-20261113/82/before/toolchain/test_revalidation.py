"""No cleanup: all new fixture files remain available for review."""
from pathlib import Path
import unittest,os,json,struct,shutil,ast
from unittest.mock import patch
os.environ['NIGHT_SOURCE_SHA']='9e39fa8a61392652bb28b75fc26216675bcad1d5'
import launcher as L
from checks import *
from section_compare import layout
from resource_report import critical_stop
from log_support import canonical_log,log_summary,audit_log_copy
from validate import packages
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';X=Path(os.environ.get('NIGHT_TEST_ROOT',str(W/'temp/night-revalidation-20261104-tests-03')));X.mkdir(exist_ok=False)
class Tests(unittest.TestCase):
 def test_memory_error_stops_queue(self):
  d=X/'memory';(d/'validation').mkdir(parents=True);(d/'validation/failure.txt').write_text('Traceback\nMemoryError\n');self.assertEqual(critical_stop(d),'memory-oom-stop')
 def test_validation_oom_stops_queue(self):
  d=X/'oom';(d/'validation-02').mkdir(parents=True);save(d/'validation-02/service-result.json',{'Result':'oom-kill'});self.assertEqual(critical_stop(d),'memory-oom-stop')
 def test_memory_error_main_result(self):
  import validate,argparse
  d=X/'memory-main';d.mkdir();args=argparse.Namespace(root=d,output=d/'validation',project='toolchain',peer=None,certified_selftest=False)
  with patch.object(validate,'canonical_log',side_effect=MemoryError('fixture')):self.assertEqual(validate.main(args),1)
  r=json.loads((d/'validation/result.json').read_text());self.assertEqual(r['reason'],'memory-stop');self.assertEqual(critical_stop(d),'memory-oom-stop')
 def queue_fixture(self,kind):
  import night,subprocess
  n=X/('queue-'+kind);n.mkdir();launched=[]
  def launch(argv,**kwargs):
   project=kwargs['env']['FINAL_PROJECT'];launched.append(project);d=n/project;(d/'evidence').mkdir(parents=True)
   save(d/'evidence/result.json',dict(status='failed',reason='fixture'))
   save(d/'evidence/final-audit.json',dict(mounts={'stdout':''},remaining_build_processes=[]))
   if kind=='MemoryError':(d/'validation').mkdir();(d/'validation/failure.txt').write_text('MemoryError: fixture')
   return subprocess.CompletedProcess(argv,0,'fixture launch','')
  def show(argv,**kwargs):return 'inactive\n' if 'ActiveState' in argv else 'Result=oom-kill\n' if kind=='OOM' else 'Result=exit-code\n'
  with patch.object(night,'N',n),patch.object(night.L,'check_source',lambda:None),patch.object(night.subprocess,'run',launch),patch.object(night.subprocess,'check_output',show):
   self.assertEqual(night.run(),1)
  self.assertEqual(launched,['toolchain']);self.assertFalse((n/'basedev').exists());self.assertEqual(json.loads((n/'night-result.json').read_text())['status'],'stopped')
 @unittest.skip('single Toolchain project; no serial Base-Dev queue')
 def test_actual_queue_memory_error(self):self.queue_fixture('MemoryError')
 @unittest.skip('single Toolchain project; no serial Base-Dev queue')
 def test_actual_queue_service_oom(self):self.queue_fixture('OOM')
 def test_packages_only_driver(self):
  d=X/'packages';(d/'gbs-root/local/repos').mkdir(parents=True);(d/'gbs-root/local/repos/wrong.rpm').touch()
  with self.assertRaisesRegex(AssertionError,'required location'):packages(d)
  p=d/'gbs-driver/local/repos/test/RPMS';p.mkdir(parents=True);(p/'right.rpm').touch()
  with patch('validate.subprocess.run',return_value=type('R',(),dict(returncode=0,stdout='clang\tx86_64',stderr=''))):self.assertEqual(list(packages(d)),['clang\tx86_64'])
 def test_log_size_guard(self):
  p=X/'large.log'
  with p.open('wb') as f:f.truncate(1024**3+1)
  with self.assertRaisesRegex(AssertionError,'1 GiB'):log_summary(p)
 def test_real_record_resize_and_negatives(self):
  original=W/'temp/night-20261103/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt/clang-22.debug'
  a=original.read_bytes();view,h,ss=layout(a);s=next(s for s in ss if s['name']=='.comment');at=s['offset']+s['size'];addition=b'Linker: LLD abc\0';assert len(addition)==16
  b=bytearray(a[:at]+addition+a[at:]);struct.pack_into('<Q',b,40,h[5]+16)
  for sec in ss:
   off=h[5]+16+sec['index']*64
   if sec['offset']>=at:struct.pack_into('<Q',b,off+24,sec['offset']+16)
   if sec['name']=='.comment':struct.pack_into('<Q',b,off+32,sec['size']+16)
  p=X/'record-resized.debug';p.write_bytes(b);proof=file_proof(original,p);save(X/'record-resize-proof.json',proof);self.assertEqual(proof['classification'],'command-record-sections-only')
  for name in ['.symtab']:
   bad=bytearray(a);off=next(s for s in ss if s['name']==name)['offset']+1;bad[off]^=1;p=X/(name[1:]+'-bad.debug');p.write_bytes(bad)
   with self.assertRaisesRegex(AssertionError,name):file_proof(original,p)
  bad=bytearray(b);bad[s['offset']:s['offset']+10]=b'NOT_IDENT!';p=X/'comment-bad.debug';p.write_bytes(bad)
  with self.assertRaisesRegex(AssertionError,'non-identifier'):file_proof(original,p)
  src=original.parent/'clang.candidate';p=X/'text-bad.clang';shutil.copyfile(src,p);off=sections(src.read_bytes())['.text']['offset']+17
  with p.open('r+b') as f:f.seek(off);x=f.read(1);f.seek(off);f.write(bytes([x[0]^1]))
  with self.assertRaisesRegex(AssertionError,'ALLOC'):file_proof(src,p)
 def test_generated_poll_no_restarts(self):
  d=X/'poll';(d/'evidence').mkdir(parents=True);L.materialize(d,{'prep_unit':'fixture-prep','build_unit':'fixture-build','mode':'full'})
  source=(d/'run.py').read_text();self.assertIn("shutil.copyfile(p,E/'rpm-build.log')",source);start=source.index('    src.seek(max(0,position-len(anchor)))');end=source.index('\n',source.index('anchor=src.read(min(position,128))',start))
  readblock='\n'.join(l[4:] for l in source[start:end].splitlines());ast.parse(readblock)
  start=source.index("    for ln in b.decode");end=source.index("    if plan['mode']=='rehearsal'",start)
  phaseblock='\n'.join(l[4:] for l in source[start:end].splitlines());ast.parse(phaseblock)
  original=d/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/.build.log';original.parent.mkdir(parents=True);original.touch();copied=d/'evidence/rpm-build.log';events=[];env={'position':0,'anchor':b'','p':original,'time':__import__('time'),'append':lambda name,row:events.append((name,row))}
  for chunk in [b'[ 1s] Executing(%build)\n',b'[ 2s] BOLT_DISK_REPORT begin\n',b'[ 3s] BOLT_COMPARE_ROOT_PASS\n',b'',b'[ 4s] Processing files: clang\n']:
   with original.open('ab') as f:f.write(chunk)
   with original.open('rb') as src:env['src']=src;exec(readblock,env)
   with copied.open('ab') as out:out.write(env['b'])
   exec(phaseblock,env)
  self.assertEqual([e for e in events if e[0]=='log-restarts.jsonl'],[]);self.assertEqual(original.read_bytes(),copied.read_bytes());save(X/'poll-audit.json',audit_log_copy(d))
if __name__=='__main__':unittest.main(verbosity=2)
