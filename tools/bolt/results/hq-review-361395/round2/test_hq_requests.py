import unittest, importlib.util, os, sys, signal, subprocess, tempfile, json, contextlib, io, re
from pathlib import Path
from unittest.mock import patch, Mock
S=Path(os.environ['PRODUCT_SOURCE'])
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
h=load('helper104',S/'packaging/clang-bolt-helper.py')
a=load('converter104',S/'packaging/llvm-static-archives-native.py')
class Requests(unittest.TestCase):
 def setUp(self):
  self.root=Path(tempfile.mkdtemp())
  self.saved={s:signal.getsignal(s) for s in (signal.SIGCHLD,signal.SIGINT,signal.SIGTERM,signal.SIGHUP)}
  h._CANCEL_SIGNAL=None;h._ACTIVE_GROUP=None
  if hasattr(h,'_SPAWNING'):h._SPAWNING=False;h._DEFERRED_SECOND_SIGNAL=None
 def tearDown(self):
  for s,v in self.saved.items():signal.signal(s,v)
  h._CANCEL_SIGNAL=None;h._ACTIVE_GROUP=None
 def helper_restore(self,mode,previous=signal.SIG_IGN):
  signal.signal(signal.SIGCHLD,previous)
  argv=[sys.executable,'-c','pass' if mode=='success' else 'import time;time.sleep(10)']
  if mode=='failure':argv=[sys.executable,'-c','raise SystemExit(7)']
  original=h.reap_child;reaped=[]
  def reap(*args,**kw):
   self.assertEqual(signal.getsignal(signal.SIGCHLD),signal.SIG_DFL)
   rc=original(*args,**kw);reaped.append(args[0].pid);return rc
  with patch.object(h,'reap_child',side_effect=reap):
   if mode in ('systemexit','keyboard','cancel'):
    error={'systemexit':SystemExit(3),'keyboard':KeyboardInterrupt(),'cancel':h.GateError('cancel fixture',cancel_originated=True)}[mode]
    with patch.object(h,'peek_child_exit',side_effect=error),self.assertRaises(BaseException):
     h.call(argv,self.root/'log')
   elif mode in ('failure','timeout'):
    with self.assertRaises(h.GateError):h.call(argv,self.root/'log',timeout=.03 if mode=='timeout' else 10)
   else:h.call(argv,self.root/'log')
  self.assertTrue(reaped)
  for pid in reaped:
   with self.assertRaises(ChildProcessError):os.waitpid(pid,os.WNOHANG)
  self.assertEqual(signal.getsignal(signal.SIGCHLD),previous)
 def test_H1_success_ignored(self):self.helper_restore('success')
 def test_H1_success_handler(self):self.helper_restore('success',lambda *_:None)
 def test_H1_command_failure(self):self.helper_restore('failure')
 def test_H1_timeout(self):self.helper_restore('timeout')
 def test_H1_cancel(self):self.helper_restore('cancel')
 def test_H1_systemexit(self):self.helper_restore('systemexit')
 def test_H1_keyboardinterrupt(self):self.helper_restore('keyboard')
 def test_H1_popen_failure(self):
  signal.signal(signal.SIGCHLD,signal.SIG_IGN)
  with patch.object(h.subprocess,'Popen',side_effect=OSError('fixture')),self.assertRaises(h.GateError):h.call(['missing'],self.root/'log')
  self.assertEqual(signal.getsignal(signal.SIGCHLD),signal.SIG_IGN)
 def spawn_case(self,failed=False,second=True):
  events=[];proc=Mock(pid=987654321);proc.returncode=None
  def popen(*args,**kw):
   self.assertNotIn('preexec_fn',kw)
   events.append('inside')
   h.record_cancel(signal.SIGTERM,None)
   if second:h.record_cancel(signal.SIGINT,None)
   events.append('after-signals')
   if failed:raise OSError('spawn failed')
   return proc
  def terminate(pid,sig):
   events.append(('terminate',pid,sig))
   raise SystemExit(128+sig)
  with patch.object(h.subprocess,'Popen',side_effect=popen),patch.object(h.os,'kill',side_effect=terminate),patch.object(h.os,'killpg',side_effect=lambda p,s:events.append(('killpg',p,s))),patch.object(h,'wait_group_exit'),patch.object(h,'reap_child',return_value=-9),patch.object(h,'peek_child_exit',side_effect=lambda *args:h.check_cancel()):
   with self.assertRaises(BaseException):h.call(['fixture'],self.root/'log')
  self.assertIn('after-signals',events)
  if second:self.assertTrue(any(isinstance(e,tuple) and e[0]=='terminate' for e in events))
  if not failed:self.assertTrue(any(isinstance(e,tuple) and e[0]=='killpg' and e[1]==proc.pid for e in events))
  else:self.assertFalse(any(isinstance(e,tuple) and e[0]=='killpg' for e in events))
  self.assertFalse(getattr(h,'_SPAWNING',False))
  self.assertIsNone(getattr(h,'_DEFERRED_SECOND_SIGNAL',None))
 def test_H2_second_signal_spawn_success(self):self.spawn_case()
 def test_H2_second_signal_spawn_failure(self):self.spawn_case(failed=True)
 def test_H2_first_signal_spawn_success(self):self.spawn_case(second=False)
 def test_H2_child_signal_mask_unchanged(self):
  wanted={int(x) for x in signal.pthread_sigmask(signal.SIG_BLOCK,[])}
  text=h.call([sys.executable,'-c','import signal,json;print(json.dumps(sorted(int(s) for s in signal.pthread_sigmask(signal.SIG_BLOCK,[]))))'],self.root/'log')
  self.assertEqual(set(json.loads(text)),wanted)
  self.assertEqual({int(x) for x in signal.pthread_sigmask(signal.SIG_BLOCK,[])},wanted)
 def test_H3_explicit_list_nonstandard_layout(self):
  p=self.root/'arbitrary-list';p.write_text('/'+h.DEBUG_INSTALL_PATH+'\n'.replace('\\n','\n'))
  # Write a real newline, not a shell escape.
  p.write_text('/'+h.DEBUG_INSTALL_PATH+chr(10))
  r=h.debugfiles_gate(str(p),{'debug_file':{}})
  self.assertTrue(r['required']);self.assertEqual(r['path'],str(p));self.assertEqual(r['sha256'],h.digest(p))
 def test_H3_missing_list(self):
  with self.assertRaises(h.GateError):h.debugfiles_gate(str(self.root/'missing'),{'debug_file':{}})
 def test_H3_wrong_member(self):
  p=self.root/'list';p.write_text('/usr/lib/debug/wrong.debug\n')
  with self.assertRaises(h.GateError):h.debugfiles_gate(str(p),{'debug_file':{}})
 def test_H3_release_no_list_required_by_gate(self):
  self.assertEqual(h.debugfiles_gate(None,{}),{'required':False})
 def test_H3_spec_explicit_list(self):
  spec=(S/'packaging/llvm.spec').read_text()
  line=next(l for l in spec.splitlines() if '%{SOURCE1201} post ' in l)
  self.assertIn('--debugfiles-list "%{_builddir}/%{buildsubdir}/debugfiles.list"',line)
 def ar_header(self,name,data):
  return f'{name:<16}{0:<12}{0:<6}{0:<6}{100644:<8}{len(data):<10}'.encode()+bytes([96,10])+data+(bytes([10]) if len(data)%2 else b'')
 def test_H4_second_nonempty_table_rejected(self):
  for magic in (b'!<arch>'+bytes([10]),b'!<thin>'+bytes([10])):
   p=self.root/('normal' if magic.startswith(b'!<arch>') else 'thin')
   p.write_bytes(magic+self.ar_header('//',b'a/'+bytes([10]))+self.ar_header('//',b'b/'+bytes([10])))
   with self.assertRaisesRegex(ValueError,'duplicate.*long-name'):a.inspect(p)
 def test_H4_empty_first_table_rejected(self):
  for magic in (b'!<arch>'+bytes([10]),b'!<thin>'+bytes([10])):
   p=self.root/('normal' if magic.startswith(b'!<arch>') else 'thin')
   p.write_bytes(magic+self.ar_header('//',b'')+self.ar_header('//',b'b/'+bytes([10])))
   with self.assertRaisesRegex(ValueError,'duplicate.*long-name'):a.inspect(p)
 def test_H4_single_empty_table_accepted(self):
  for magic in (b'!<arch>'+bytes([10]),b'!<thin>'+bytes([10])):
   p=self.root/('normal' if magic.startswith(b'!<arch>') else 'thin');p.write_bytes(magic+self.ar_header('//',b''))
   self.assertEqual(a.inspect(p)['members'],[])
 def test_H4_valid_longname_resolves(self):
  p=self.root/'valid.a';p.write_bytes(b'!<arch>'+bytes([10])+self.ar_header('//',b'long-member.o/'+bytes([10]))+self.ar_header('/0',bytes.fromhex('4243c0de')))
  self.assertEqual(a.inspect(p)['members'][0]['name'],'long-member.o')
 def converter_restore(self,mode,previous=signal.SIG_IGN):
  signal.signal(signal.SIGCHLD,previous)
  argv=['converter','--root','r','--build','b','--evidence','e','--arch','x86_64','--debug-info','yes','--compiler','c','--disassembler','d','--nm','n']
  if mode=='help':argv=['converter','--help']
  if mode=='parse':argv=['converter','--unknown']
  events=[]
  def install(*args):
   self.assertEqual(signal.getsignal(signal.SIGCHLD),signal.SIG_DFL);events.append('install')
   if mode=='failure':raise ValueError('fixture failure')
   if mode=='timeout':raise subprocess.TimeoutExpired('fixture',1)
   if mode=='systemexit':raise SystemExit(7)
   if mode=='keyboard':raise KeyboardInterrupt()
   if mode=='cancel':a._CANCEL_SIGNAL=signal.SIGTERM
   events.append('finished')
  with patch.object(sys,'argv',argv),patch.object(a,'install',side_effect=install),contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
   if mode in ('help','parse','failure','timeout','systemexit','keyboard'):
    with self.assertRaises(BaseException):a.install_main()
   else:self.assertEqual(a.install_main(),143 if mode=='cancel' else 0)
  self.assertEqual(signal.getsignal(signal.SIGCHLD),previous)
 def test_H5_success(self):self.converter_restore('success')
 def test_H5_handler(self):self.converter_restore('success',lambda *_:None)
 def test_H5_help(self):self.converter_restore('help')
 def test_H5_parse_error(self):self.converter_restore('parse')
 def test_H5_failure(self):self.converter_restore('failure')
 def test_H5_timeout(self):self.converter_restore('timeout')
 def test_H5_systemexit(self):self.converter_restore('systemexit')
 def test_H5_keyboardinterrupt(self):self.converter_restore('keyboard')
 def test_H5_cancel(self):self.converter_restore('cancel')
if __name__=='__main__':
 r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Requests))
 Path(os.environ['TEST_RESULT']).write_text(json.dumps({'tests':r.testsRun,'failures':[(t.id(),s) for t,s in r.failures],'errors':[(t.id(),s) for t,s in r.errors],'success':r.wasSuccessful()},indent=2))
 sys.exit(not r.wasSuccessful())
