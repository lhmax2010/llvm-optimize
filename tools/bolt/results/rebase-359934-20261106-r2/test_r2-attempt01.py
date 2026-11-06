from pathlib import Path
import importlib.util,sys,os,subprocess,unittest,json,signal,time,shlex
E=Path(__file__).parent
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
B=W.parent/'llvm-optimize-bolt';S=W/'temp/rebase-359934-20261106/source'
X=W/'temp/rebase-359934-20261106-r2/new-tests';X.mkdir(exist_ok=False)
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
h=load('h',S/'packaging/clang-bolt-helper.py')
a=load('a',S/'packaging/llvm-static-archives-native.py')
sys.path.insert(0,str(B/'tools'))
import test_static_archives_source_v2 as old
spec=(E/'parse-03/toolchain-x86-debug-on-new.stdout').read_text()
optional=spec[spec.index('bolt_optional() {'):spec.index('bolt_step() {')]
calls=[l.strip() for l in spec.splitlines() if l.strip().startswith('bolt_optional python3 -B ')]
assert len(calls)==5,calls
inputs=json.loads((B/'tools/bolt/results/final-20261103/flags-inputs.json').read_text())
rawspec=(S/'packaging/llvm.spec').read_text()
fragment=rawspec.split('# BEGIN TIZEN_LLVM_FIXED_FLAGS')[1].split('# END TIZEN_LLVM_FIXED_FLAGS')[0].replace('%%','%')
observed=[]
def wait_ready(p,path):
 end=time.monotonic()+10
 while not path.exists() and p.poll() is None and time.monotonic()<end:time.sleep(.01)
 assert path.exists(),('not ready',p.poll())
class Tests(unittest.TestCase):
 def test_assembler_rejected_warnings_kept(self):
  for token in ['-Wa,--noexecstack','-Wa,a,b','-Xassembler']:
   with self.assertRaisesRegex(ValueError,'uncertified assembler option: '+token):a.classify_options(old.FLAGS+[token])
  for token in ['-Wall','-Wno-unused']:a.classify_options(old.FLAGS+[token])
 def versions(self,dis='22.1.8',nm='22.1.8',cc='22.1.8',tag='ok'):
  d=X/('versions-'+tag);d.mkdir();(d/'CMakeCache.txt').write_text('fixture')
  tools=[]
  for name in ['clang','llvm-dis','llvm-nm']:
   p=d/name;p.write_text('fixture');p.chmod(0o755);tools.append(p)
  class Command:
   def run(self,argv,prefix,stdout):
    version={'clang':'clang version '+cc,'llvm-dis':'LLVM version '+dis,'llvm-nm':'LLVM version '+nm}[Path(argv[0]).name]
    stdout.write((version+'\n').encode())
  return a.validate_tools(d,*tools,Command(),d)
 def test_tool_versions_equal(self):
  r=self.versions();self.assertEqual(set(r),{'compiler','version','compiler_sha256','disassembler','nm'})
 def test_dis_version_mismatch(self):
  with self.assertRaisesRegex(ValueError,'disassembler version mismatch: expected 22.1.8, found 22.1.7'):self.versions(dis='22.1.7',tag='dis-bad')
 def test_nm_version_mismatch(self):
  with self.assertRaisesRegex(ValueError,'nm version mismatch'):self.versions(nm='22.0.0',tag='nm-bad')
 def test_major_still_rejected(self):
  with self.assertRaisesRegex(ValueError,'compiler major'):self.versions(cc='21.1.8',tag='cc-bad')
 def test_debug_error_not_repeated(self):
  with self.assertRaises(ValueError) as exc:a.ir_settings(old.module(flags=old.FLAGS),debug_info='no')
  self.assertEqual(str(exc.exception),'debug-info expected release, found debug')
 def test_rpath_doc_restored(self):self.assertIn('Freeze all bytes',h.rpath_layout.__doc__)
 def test_diagnostics_uses_origin_attribute(self):
  from unittest.mock import patch
  with patch.object(h,'disk_diagnose') as disk:
   h.diagnose_safely('x','-',h.GateError('CANCELLED: fake text'));disk.assert_called_once()
  with patch.object(h,'disk_diagnose') as disk:
   h.diagnose_safely('x','-',h.GateError('anything',cancel_originated=True));disk.assert_not_called()
 def test_environment_cannot_override_literal(self):
  for shell in ['/bin/sh','/bin/dash']:
   for project,mode in [('toolchain','0'),('basedev','1')]:
    env=dict(os.environ,**inputs[project]['raw'],TIZEN_LLVM_RELEASE=mode)
    env.pop('TIZEN_LLVM_EXPECTED_DROPPED',None)
    argv=[shell,'-e','-c',fragment+'\nprintf "VALUES:%s|%s|%s\n" "$CFLAGS" "$CXXFLAGS" "$LDFLAGS"']
    baseline=subprocess.run(argv,env=env,capture_output=True,text=True)
    self.assertEqual(baseline.returncode,0,baseline.stderr)
    for value in ['', '-fcf-protection=full','arbitrary']:
     r=subprocess.run(argv,env=dict(env,TIZEN_LLVM_EXPECTED_DROPPED=value),capture_output=True,text=True)
     self.assertEqual((r.returncode,r.stdout,r.stderr),(baseline.returncode,baseline.stdout,baseline.stderr))
 def test_no_debug_description(self):
  fn=fragment.split('tizen_llvm_flags CFLAGS')[0]
  for shell in ['/bin/sh','/bin/dash']:
   for kind in ['CFLAGS','CXXFLAGS']:
    r=subprocess.run([shell,'-e','-c',fn+'\ntizen_llvm_flags '+kind+' "" 0'],capture_output=True,text=True)
    self.assertEqual(r.returncode,0)
    for output in (r.stdout,r.stderr):
     self.assertIn('uncertified debug option sequence: no debug options',output)
     self.assertNotIn('uncertified debug option sequence: []',output)
 def test_five_optional_calls_cancel_and_ordinary_failure(self):
  for i,call in enumerate(calls):
   for sig in [signal.SIGTERM,signal.SIGHUP,signal.SIGINT,None]:
    d=X/('optional-'+str(i)+'-'+str(sig));d.mkdir()
    ready=d/'ready';marker=d/'after';wrapper=d/'helper.py'
    wrapper.write_text("""from pathlib import Path
import importlib.util,sys,os,time
sp=importlib.util.spec_from_file_location('h',sys.argv[1]);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
sys.argv=sys.argv[1:]
def probe(*a,**kw):
 Path(READY).write_text(str(os.getpid()))
 if NORMAL:raise h.GateError('ordinary diagnostic failure')
 while True:h.check_cancel();time.sleep(.01)
h.disk_report=probe;h.cache_release=probe
h.disk_diagnose=lambda *a,**kw: None
sys.exit(h.cli())
""".replace('READY',repr(str(ready))).replace('NORMAL',repr(sig is None)))
    import re
    line=re.sub(r'python3 -B \S+',shlex.join([sys.executable,'-B',str(wrapper),str(S/'packaging/clang-bolt-helper.py')]),call)
    script=d/'install.sh';script.write_text('BOLT_WORK='+shlex.quote(str(d))+'\n'+optional+line+'\nprintf after > '+shlex.quote(str(marker))+'\n')
    p=subprocess.Popen(['/bin/sh','-e',str(script)],cwd=d,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    try:
     wait_ready(p,ready)
     if sig is not None:os.kill(int(ready.read_text()),sig)
     out,err=p.communicate(timeout=10)
     self.assertEqual(p.returncode,128+sig if sig else 0,(i,sig,out,err))
     self.assertEqual(marker.exists(),sig is None)
     observed.append(dict(call=call,signal=int(sig) if sig else None,rc=p.returncode,marker=marker.exists(),stdout=out,stderr=err))
    finally:
     if p.poll() is None:p.kill();p.wait()
 def test_failure_then_cancel_preserves_diagnosis(self):
  d=X/'concurrent';d.mkdir();ready=d/'ready';script=d/'probe.py'
  script.write_text("""from pathlib import Path
import importlib.util,sys,time
sp=importlib.util.spec_from_file_location('h',HELPER);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
original=h.wait_group_exit
def cleanup(*args,**kw):
 Path(READY).write_text('ready')
 while h._CANCEL_SIGNAL is None:time.sleep(.01)
 return original(*args,**kw)
h.wait_group_exit=cleanup
def diagnose(*args,**kw):print('DISK_DIAGNOSE_CALLED',file=sys.stderr)
h.disk_diagnose=diagnose
h.main=lambda:h.call(['/bin/sh','-c','exit 1'],LOG)
sys.exit(h.cli())
""".replace('HELPER',repr(str(S/'packaging/clang-bolt-helper.py'))).replace('READY',repr(str(ready))).replace('LOG',repr(str(d/'call.log'))))
  p=subprocess.Popen([sys.executable,'-B',str(script)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
  try:
   wait_ready(p,ready);p.send_signal(signal.SIGTERM);out,err=p.communicate(timeout=10)
   self.assertEqual(p.returncode,143);self.assertIn('COMMAND_FAILED rc=1',err);self.assertIn('CANCELLED:',err);self.assertIn('DISK_DIAGNOSE_CALLED',err)
   observed.append(dict(case='command-failed-then-cancel',rc=p.returncode,stdout=out,stderr=err))
  finally:
   if p.poll() is None:p.kill();p.wait()
if __name__=='__main__':
 r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
 (E/'new-tests-observed.json').write_text(json.dumps(observed,indent=2)+'\n')
 (E/'new-tests-result.json').write_text(json.dumps(dict(tests=r.testsRun,failures=len(r.failures),errors=len(r.errors)))+'\n')
 sys.exit(not r.wasSuccessful())
