
import ctypes,importlib.util,json,os,signal,subprocess,sys,tempfile,time,unittest,shutil,re
from pathlib import Path
from unittest import mock
S=Path(os.environ['PRODUCT_SOURCE'])
H=S/'packaging/clang-bolt-helper.py'
C=S/'packaging/llvm-static-archives-native.py'
HERE=Path(__file__).parent
AD=HERE/'external/adapted'
M={int(k):v for k,v in json.loads((HERE/'external/line-map.json').read_text()).items()}
OBS=[]
if ctypes.CDLL(None).prctl(36,1,0,0,0)!=0:raise RuntimeError('test subreaper unavailable')
def load():
 spec=importlib.util.spec_from_file_location('h109',H);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h);return h
def alive(pid):
 try:return Path('/proc/%d/stat'%pid).read_text().rsplit(')',1)[1].split()[0] not in ('Z','X')
 except (FileNotFoundError,ProcessLookupError):return False
def reap_adopted():
 while True:
  try:
   pid,status=os.waitpid(-1,os.WNOHANG)
   if pid==0:return
  except ChildProcessError:return
class R1(unittest.TestCase):
 def setUp(self):
  self.h=load();self.d=Path(tempfile.mkdtemp());self.old=signal.getsignal(signal.SIGCHLD)
 def tearDown(self):
  signal.signal(signal.SIGCHLD,self.old);reap_adopted()
 def descendant(self,seconds):
  return [sys.executable,'-c','import os,time\np=os.fork()\nif p: print(p,flush=True);os._exit(0)\ntime.sleep('+str(seconds)+')\n']
 def test_success_with_live_descendant_fails_and_cleans(self):
  log=self.d/'live.log';begin=time.monotonic()
  with self.assertRaisesRegex(self.h.GateError,'COMMAND_ERROR: command exited successfully with live descendants'):
   self.h.call(self.descendant(60),log)
  pid=int(log.read_text().strip());self.assertFalse(alive(pid))
  _,status=os.waitpid(pid,0);self.assertEqual(os.waitstatus_to_exitcode(status),-signal.SIGKILL)
  self.assertIsNone(self.h._ACTIVE_SESSION)
  OBS.append(dict(test=self.id(),elapsed=time.monotonic()-begin,descendant_status=os.waitstatus_to_exitcode(status)))
 def test_short_lived_descendant_succeeds(self):
  log=self.d/'short.log';begin=time.monotonic()
  self.h.call(self.descendant(2),log)
  pid=int(log.read_text().strip());self.assertFalse(alive(pid))
  _,status=os.waitpid(pid,0);self.assertEqual(os.waitstatus_to_exitcode(status),0)
  self.assertGreaterEqual(time.monotonic()-begin,1.8)
  OBS.append(dict(test=self.id(),elapsed=time.monotonic()-begin))
 def test_ordinary_success_clears_pgid_before_reap(self):
  seen=[];real=self.h.reap_child
  def reap(*args,**kwargs):
   seen.append(self.h._ACTIVE_SESSION);return real(*args,**kwargs)
  with mock.patch.object(self.h,'reap_child',side_effect=reap):
   out=self.h.call([sys.executable,'-c','print("ordinary")'],self.d/'ordinary.log')
  self.assertEqual(out.strip(),'ordinary');self.assertEqual(seen,[None])
 def test_proc_read_failure_keeps_error_and_cleans(self):
  children=[];real=self.h.subprocess.Popen
  def spawn(*a,**kw):
   p=real(*a,**kw);children.append(p.pid);return p
  with mock.patch.object(self.h.subprocess,'Popen',side_effect=spawn),mock.patch.object(self.h.os,'scandir',side_effect=PermissionError('109 proc denied')):
   with self.assertRaisesRegex(self.h.GateError,'cannot enumerate/read process session; scan incomplete: 109 proc denied') as caught:
    self.h.call([sys.executable,'-c','pass'],self.d/'proc.log')
  self.assertNotIn('successfully with live descendants',str(caught.exception))
  for pid in children:
   with self.assertRaises(ChildProcessError):os.waitpid(pid,os.WNOHANG)
class Regression(unittest.TestCase):
 def setUp(self):self.d=Path(tempfile.mkdtemp())
 def tearDown(self):reap_adopted()
 def run_probe(self,name,args=(),code=None,env=None,timeout=30):
  argv=[sys.executable,'-B',str(AD/name),*map(str,args)] if code is None else [sys.executable,'-B','-c',code,*map(str,args)]
  p=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=env,timeout=timeout)
  (self.d/'stdout.txt').write_text(p.stdout);(self.d/'stderr.txt').write_text(p.stderr)
  OBS.append(dict(test=self.id(),argv=argv,rc=p.returncode,stdout=p.stdout,stderr=p.stderr))
  return p
 def claude_h2(self,mode,oldline):
  new_line=M.get(oldline,oldline)
  p=self.run_probe('h2.py',[H,mode,new_line,self.d,M[254]],timeout=20)
  if p.returncode==0:
   self.assertIn('RAISED GateError CANCELLED',p.stdout)
  else:self.assertIn(p.returncode,[-signal.SIGTERM,-signal.SIGHUP])
  f=self.d/'popen.pid'
  if f.exists():
   pid=int(f.read_text());deadline=time.monotonic()+3
   while alive(pid) and time.monotonic()<deadline:time.sleep(.01)
   live=alive(pid)
   if live:os.killpg(pid,signal.SIGKILL)
   self.assertFalse(live,'test harness had to kill surviving child')
   try:os.waitpid(pid,0)
   except ChildProcessError:pass
 def claude_h1(self,mode):
  p=self.run_probe('h1.py',[H,mode,self.d/'h1.log'])
  self.assertEqual(p.returncode,0,p.stderr)
  self.assertIn('SIGCHLD_after=1',p.stdout)
  self.assertIn("('restore', False)",p.stdout)
  expected={'ok':'returned','fail':'GateError','timeout':'GateError','cancel':'GateError','sysexit':'SystemExit','kbint':'KeyboardInterrupt'}[mode]
  self.assertIn(expected,p.stdout)
 def test_claude_n1(self):
  p=self.run_probe('n1.py',[H,self.d/'n1.log']);self.assertEqual(p.returncode,0,p.stderr);self.assertIn('returned;',p.stdout);self.assertNotIn('raised',p.stdout)
 def child_mask(self,ignore_int):
  code='import signal,sys,runpy\nsignal.signal(signal.SIGCHLD,signal.SIG_IGN)\n'
  if ignore_int:code+='signal.signal(signal.SIGINT,signal.SIG_IGN)\n'
  code+='sys.argv=sys.argv[1:]\nrunpy.run_path(sys.argv[0],run_name="__main__")\n'
  p=self.run_probe('',[AD/'mask.py',H,self.d/'mask.log'],code=code)
  self.assertEqual(p.returncode,0,p.stderr)
  child=next(x for x in p.stdout.splitlines() if x.startswith('child:'))
  self.assertEqual(int(re.search(r'SigBlk:\s*([0-9a-fA-F]+)',child).group(1),16),0)
  ignored=int(re.search(r'SigIgn:\s*([0-9a-fA-F]+)',child).group(1),16)
  self.assertEqual(bool(ignored&(1<<(signal.SIGINT-1))),ignore_int)
  self.assertFalse(ignored&(1<<(signal.SIGCHLD-1)))
 def test_child_mask_chld_ignored(self):self.child_mask(False)
 def test_child_mask_chld_int_ignored(self):self.child_mask(True)
 def disposition(self,kind):
  h=load();saved=signal.getsignal(signal.SIGCHLD)
  value={'default':signal.SIG_DFL,'ignored':signal.SIG_IGN,'custom':lambda s,f:None,'none':None}[kind]
  try:
   if value is not None:signal.signal(signal.SIGCHLD,value)
   realget=signal.getsignal
   def get(sig):return None if sig==signal.SIGCHLD and value is None else realget(sig)
   with mock.patch.object(h.signal,'getsignal',side_effect=get):
    self.assertEqual(h.call([sys.executable,'-c','print("ok")'],self.d/'disp.log').strip(),'ok')
    with self.assertRaisesRegex(h.GateError,'COMMAND_FAILED rc=7'):
     h.call([sys.executable,'-c','raise SystemExit(7)'],self.d/'disp-fail.log')
   self.assertIs(realget(signal.SIGCHLD),signal.SIG_DFL if value is None else value)
  finally:signal.signal(signal.SIGCHLD,saved)
 def test_popen_failure_without_deferred_signal(self):
  h=load();error=FileNotFoundError('109 spawn failure')
  with mock.patch.object(h.subprocess,'Popen',side_effect=error):
   with self.assertRaises(h.GateError) as caught:h.call(['fixture'],self.d/'spawn.log')
  self.assertIs(caught.exception.__cause__,error);self.assertFalse(h._SPAWNING);self.assertIsNone(h._ACTIVE_SESSION)
 def test_claude_archive_probe(self):
  def member(name,data,size=None):
   n=len(data) if size is None else size
   header=(f'{name:<16}{0:<12}{0:<6}{0:<6}{644:<8}{n:<10}'+chr(96)+chr(10)).encode()
   return header+data+(bytes([10]) if len(data)%2 else b'')
  table=b'a_very_long_name.o/\nanother_long_name.o/\n';offset=len(b'a_very_long_name.o/\n')
  for thin in [False,True]:
   data=(b'!<thin>\n' if thin else b'!<arch>\n')+member('//',table)
   for index in [0,offset]:data+=member('/'+str(index),b'' if thin else b'BC\xc0\xde',size=4)
   (self.d/('thin.a' if thin else 'normal.a')).write_bytes(data)
  (self.d/'short.a').write_bytes(b'!<arch>\n'+member('short.o/',b'BC\xc0\xde'))
  p=self.run_probe('h4b.py',[C,self.d])
  self.assertEqual(p.returncode,0,p.stderr)
  lines=p.stdout.splitlines();self.assertEqual(len(lines),8)
  self.assertEqual(sum(' ACCEPT ' in x for x in lines),4)
  self.assertEqual(sum(' REJECT ValueError: duplicate GNU ar long-name table' in x for x in lines),4)
 def test_codex_review_probe(self):
  shutil.copyfile(H,self.d/'clang-bolt-helper.py');shutil.copyfile(C,self.d/'llvm-static-archives-native.py')
  env=dict(os.environ,CODEX_SCRATCH=str(self.d))
  p=self.run_probe('codex_check_review.py',env=env,timeout=40)
  self.assertEqual(p.returncode,0,p.stderr)
  rows=json.loads((self.d/'test-results.json').read_text())
  self.assertEqual(len(rows),28)
  for r in rows:
   k=r['test']
   if k.startswith('H2_'):
    self.assertIn(r['helper_rc'],[143,-signal.SIGTERM,-signal.SIGHUP])
    self.assertNotEqual(r['child_status'],'survived; cleaned by test')
   elif k.startswith('H1_'):
    self.assertTrue(r['restored_IGN']);self.assertTrue(r['direct_children_reaped'])
   elif k.startswith('H5_'):self.assertTrue(r['restored_IGN'])
   elif k.startswith('N1_'):self.assertTrue(r['passed'])
   elif k=='H4_duplicate':self.assertEqual(r['verdict'],'duplicate GNU ar long-name table')
   elif k=='H4_valid':self.assertIn(r['members'],[0,1])
   elif k=='H3_release':self.assertEqual(r['value'],{'required':False})
   elif k=='H3_debug':self.assertTrue(r['required'])
   elif k=='successful_leader_descendant':self.assertTrue(r['call_rejected']);self.assertEqual(r['descendant_status'],-signal.SIGKILL)
  OBS.append({'test':self.id(),'codex_rows':rows})
def h2case(mode,line):
 def test(self):self.claude_h2(mode,line)
 return test
for mode,line in ([('second-at-line',i) for i in range(254,266)]+[('two-real-at-line',258),('two-real-at-line',265),('popen-ok',0),('popen-fail',0)]+[('deferred-then-third',i) for i in range(257,266)]):
 setattr(Regression,'test_claude_h2_'+mode.replace('-','_')+'_'+str(line),h2case(mode,line))
def h1case(mode):
 def test(self):self.claude_h1(mode)
 return test
for mode in ['ok','fail','timeout','cancel','sysexit','kbint']:setattr(Regression,'test_claude_h1_'+mode,h1case(mode))
def statecase(kind):
 def test(self):self.disposition(kind)
 return test
for kind in ['default','ignored','custom','none']:setattr(Regression,'test_sigchld_'+kind,statecase(kind))
if __name__=='__main__':
 try:
  suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(R1),unittest.defaultTestLoader.loadTestsFromTestCase(Regression)])
  result=unittest.TextTestRunner(verbosity=2).run(suite)
  Path(os.environ['TEST_RESULT']).write_text(json.dumps({'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'PASS':result.wasSuccessful()},indent=2))
 finally:
  (Path(os.environ['TEST_SCRATCH'])/'observed.json').write_text(json.dumps(OBS,indent=2))
  reap_adopted()
 sys.exit(not result.wasSuccessful())
