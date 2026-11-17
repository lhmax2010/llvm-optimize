import ctypes,importlib.util,json,os,signal,subprocess,sys,tempfile,time,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch,MagicMock,call
S=Path(os.environ['PRODUCT_SOURCE']);H=S/'packaging/clang-bolt-helper.py';E=Path(__file__).parent.parent
sys.path.insert(0,str(E))
from post_macro_gate import check_post
OBS=[]
if ctypes.CDLL(None).prctl(36,1,0,0,0)!=0:raise RuntimeError('test subreaper unavailable')
TREE="""
import os,sys,time,json
from pathlib import Path
d=Path(sys.argv[1]);mode=sys.argv[2];duration=float(sys.argv[3])
def record(role):
 data=(json.dumps(dict(pid=os.getpid(),pgid=os.getpgrp(),sid=os.getsid(0),role=role))+chr(10)).encode()
 fd=os.open(str(d/'pids'),os.O_WRONLY|os.O_CREAT|os.O_APPEND,0o600);os.write(fd,data);os.close(fd)
record('leader')
for i in range(2):
 if os.fork()==0:
  os.setpgid(0,0);record('job')
  if os.fork()==0:record('grandchild')
  time.sleep(duration);os._exit(0)
end=time.monotonic()+3
while len((d/'pids').read_text().splitlines())<5:
 if time.monotonic()>end:raise RuntimeError('fixture not ready')
 time.sleep(.01)
(d/'ready').write_text('ready')
if mode=='exit':sys.exit(0)
if mode=='fail':sys.exit(7)
time.sleep(60)
"""
def load():
 sp=importlib.util.spec_from_file_location('h110',H);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);return h
def alive(pid):
 try:
  f=Path('/proc/%d/stat'%pid).read_text().rsplit(')',1)[1].split()
  return f[0] not in ('Z','X') or int(f[17])>1
 except (FileNotFoundError,ProcessLookupError):return False
def reap():
 while True:
  try:
   pid,status=os.waitpid(-1,os.WNOHANG)
   if not pid:return
  except ChildProcessError:return
class SessionTests(unittest.TestCase):
 def setUp(self):self.h=load();self.d=Path(tempfile.mkdtemp());self.spawned=[]
 def tearDown(self):
  if (self.d/'pids').exists():
   for row in self.rows():
    if alive(row['pid']):
     try:os.kill(row['pid'],signal.SIGKILL)
     except ProcessLookupError:pass
  for p in self.spawned:
   if p.poll() is None:p.kill();p.wait()
  reap()
 def rows(self):return [json.loads(l) for l in (self.d/'pids').read_text().splitlines()]
 def argv(self,mode='hang',duration=60):
  p=self.d/'tree.py';p.write_text(TREE)
  return [sys.executable,'-B',str(p),str(self.d),mode,str(duration)]
 def checked_empty(self):
  rows=self.rows();self.assertEqual(len(rows),5)
  self.assertEqual(len({r['sid'] for r in rows}),1);self.assertEqual(len({r['pgid'] for r in rows}),3)
  self.assertTrue(all(not alive(r['pid']) for r in rows),rows)
  OBS.append({'test':self.id(),'processes':rows,'all_not_live':True})
 def waitfile(self,path,p,timeout=6):
  end=time.monotonic()+timeout
  while not path.exists() and p.poll() is None and time.monotonic()<end:time.sleep(.01)
  self.assertTrue(path.exists(),str(path))
 def test_timeout_cross_groups(self):
  with self.assertRaisesRegex(self.h.GateError,'TIMEOUT:'):self.h.call(self.argv(),self.d/'log',timeout=1)
  self.checked_empty()
 def test_failure_cross_groups(self):
  with self.assertRaisesRegex(self.h.GateError,'COMMAND_FAILED rc=7'):self.h.call(self.argv('fail'),self.d/'log')
  self.checked_empty()
 def test_success_cross_groups_persistent_fails(self):
  start=time.monotonic()
  with self.assertRaisesRegex(self.h.GateError,'command exited successfully with live descendants'):
   self.h.call(self.argv('exit'),self.d/'log')
  self.assertGreaterEqual(time.monotonic()-start,10);self.checked_empty()
 def test_success_cross_groups_short_lived(self):
  start=time.monotonic();self.h.call(self.argv('exit',2),self.d/'log')
  self.assertGreaterEqual(time.monotonic()-start,1.8);self.checked_empty()
 def signal_case(self,sig,second):
  argv=self.argv();wrapper=self.d/'wrapper.py'
  wrapper.write_text("""
import importlib.util,sys,json,time
from pathlib import Path
sp=importlib.util.spec_from_file_location('helper',sys.argv[1]);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
d=Path(sys.argv[2]);original=h.wait_session_exit;entered=False
def drain(*a,**kw):
 global entered
 if sys.argv[3]=='second' and kw.get('kill') and not entered:
  entered=True;(d/'cleanup-ready').write_text('ready');time.sleep(5)
 return original(*a,**kw)
h.wait_session_exit=drain
h.main=lambda:h.call(json.loads(sys.argv[4]),d/'log',timeout=20)
sys.exit(h.cli())
""")
  p=subprocess.Popen([sys.executable,'-B',str(wrapper),str(H),str(self.d),'second' if second else 'first',json.dumps(argv)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);self.spawned.append(p)
  self.waitfile(self.d/'ready',p);p.send_signal(sig)
  if second:self.waitfile(self.d/'cleanup-ready',p);p.send_signal(sig)
  out,err=p.communicate(timeout=8);(self.d/'stdout').write_text(out);(self.d/'stderr').write_text(err)
  self.assertEqual(p.returncode,-sig if second else 128+sig,err);self.checked_empty()
  OBS.append({'test':self.id(),'rc':p.returncode,'stderr':err})
 def clear_before_reap(self,fail):
  real=self.h.reap_child;seen=[]
  def r(*a,**kw):seen.append(self.h._ACTIVE_SESSION);return real(*a,**kw)
  with patch.object(self.h,'reap_child',side_effect=r):
   if fail:
    with self.assertRaises(self.h.GateError):self.h.call([sys.executable,'-c','raise SystemExit(7)'],self.d/'log')
   else:self.h.call([sys.executable,'-c','pass'],self.d/'log')
  self.assertEqual(seen,[None])
 def test_failure_clears_before_reap(self):self.clear_before_reap(True)
 def test_success_clears_before_reap(self):self.clear_before_reap(False)
 def typed(self,error,classified):
  real=self.h.wait_session_exit
  def drain(*a,**kw):
   if kw.get('kill'):return real(*a,**kw)
   raise error
  with patch.object(self.h,'wait_session_exit',side_effect=drain),self.assertRaises(self.h.GateError) as caught:
   self.h.call([sys.executable,'-c','pass'],self.d/'log')
  self.assertEqual('command exited successfully with live descendants' in str(caught.exception),classified)
  self.assertIn(str(error),str(caught.exception))
 def test_typed_timeout_independent_of_text(self):self.typed(self.h.LiveDescendantsError('different wording'),True)
 def test_generic_error_not_classified_by_text(self):self.typed(self.h.GateError('process session 42 still alive: 43:R'),False)
 def test_oserror_not_live_descendants(self):self.typed(OSError('inspection error'),False)
 def test_kill_rescans_new_members(self):
  with patch.object(self.h,'live_session_members',side_effect=[[(600001,'R',1)],[(600002,'S',1)],[]]),patch.object(self.h,'kill_session_member') as kill:
   self.h.wait_session_exit(42,1,kill=True)
  self.assertEqual([c.args[:3] for c in kill.call_args_list],[(42,600001,1),(42,600002,1)])
 def test_session_timeout_is_typed(self):
  with patch.object(self.h,'live_session_members',return_value=[(600001,'R',1)]),patch.object(self.h.time,'monotonic',side_effect=[0,11]),self.assertRaises(self.h.LiveDescendantsError):
   self.h.wait_session_exit(42)
 def test_proc_stat_session_field(self):
  v=self.h.proc_stat('/proc/self/stat');self.assertEqual(v,(os.getpid(),v[1],os.getpgrp(),v[3],os.getsid(0),v[5]))
 def scan(self,state,threads,sid=42,error=None):
  real=self.h.proc_stat
  def stat(p):
   if p=='/proc/self/stat':return real(p)
   if error:raise error
   return 600001,state,777,threads,sid,1
  entries=MagicMock();entries.__enter__.return_value=iter([SimpleNamespace(name='600001')])
  with patch.object(self.h.os,'scandir',return_value=entries),patch.object(self.h,'proc_stat',side_effect=stat):return self.h.live_session_members(42)
 def test_session_matches_different_group(self):self.assertEqual(self.scan('S',1),[(600001,'S',1)])
 def test_foreign_session_excluded(self):self.assertEqual(self.scan('S',1,43),[])
 def test_session_zombie_excluded(self):self.assertEqual(self.scan('Z',1),[])
 def test_session_dead_excluded(self):self.assertEqual(self.scan('X',1),[])
 def test_zombie_leader_live_threads_included(self):self.assertEqual(self.scan('Z',2),[(600001,'Z',1)])
 def test_disappearing_member(self):self.assertEqual(self.scan('S',1,error=ProcessLookupError()),[])
 def test_scan_error_fail_closed(self):
  with self.assertRaisesRegex(self.h.GateError,'scan incomplete'):self.scan('S',1,error=PermissionError('denied'))
 def test_setsid_escape_is_documented_limit(self):
  code="""import os,time,json,sys
from pathlib import Path
d=Path(sys.argv[1]);leader=os.getpid()
if os.fork()==0:
 os.setsid();(d/'escape').write_text(json.dumps({'pid':os.getpid(),'sid':os.getsid(0),'leader':leader}));time.sleep(60);os._exit(0)
while not (d/'escape').exists():time.sleep(.01)
"""
  try:
   self.h.call([sys.executable,'-c',code,str(self.d)],self.d/'log')
   row=json.loads((self.d/'escape').read_text());self.assertNotEqual(row['sid'],row['leader']);self.assertTrue(alive(row['pid']))
   OBS.append({'test':self.id(),'known_limit':row,'escaped_alive':True})
  finally:
   if (self.d/'escape').exists():
    pid=json.loads((self.d/'escape').read_text())['pid']
    try:os.kill(pid,signal.SIGKILL)
    except ProcessLookupError:pass
    try:os.waitpid(pid,0)
    except ChildProcessError:pass
 # Repeat the r14 scenarios using the owned-process fixture above. The old
 # scripts use global pgrep/raw PID cleanup, so they are not executed here.
 def test_r14_short(self):
  self.h.call(self.argv('exit',3),self.d/'r14-short');self.checked_empty()
 def test_r14_long(self):
  with self.assertRaisesRegex(self.h.GateError,'command exited successfully'):
   self.h.call(self.argv('exit',60),self.d/'r14-long')
  self.checked_empty()
 def test_r14_second_signal(self):self.signal_case(signal.SIGTERM,True)
class PostMacroTests(unittest.TestCase):
 body='clang-bolt-helper.py post root\necho BOLT_POST_GATE_PASS\ndisk-report post\n'
 def test_enabled_requires_all_three(self):self.assertEqual(len(check_post(self.body,True)),3)
 def test_disabled_empty(self):check_post('ordinary rpm hook',False)
 def test_disabled_rejects_hidden_post(self):
  with self.assertRaises(AssertionError):check_post('clang-bolt-helper.py post root',False)
 def test_enabled_rejects_missing_macro(self):
  with self.assertRaises(AssertionError):check_post('',True)
 def test_enabled_rejects_missing_disk(self):
  with self.assertRaises(AssertionError):check_post(self.body.replace('disk-report post',''),True)
 def test_enabled_rejects_duplicates(self):
  with self.assertRaises(AssertionError):check_post(self.body*2,True)
def signal_test(sig,second):
 def test(self):self.signal_case(sig,second)
 return test
for sig in (signal.SIGTERM,signal.SIGHUP,signal.SIGINT):
 for second in (False,True):setattr(SessionTests,'test_signal_'+str(sig)+'_'+str(second),signal_test(sig,second))
if __name__=='__main__':
 suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(SessionTests),unittest.defaultTestLoader.loadTestsFromTestCase(PostMacroTests)])
 try:
  result=unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)
  Path(os.environ['TEST_RESULT']).write_text(json.dumps({'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'PASS':result.wasSuccessful()},indent=2))
 finally:
  (Path(os.environ['TEST_SCRATCH'])/'observed.json').write_text(json.dumps(OBS,indent=2));reap()
 sys.exit(not result.wasSuccessful())
