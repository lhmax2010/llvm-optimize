import contextlib,errno,importlib.util,io,json,os,signal,subprocess,sys,time,types,unittest
from pathlib import Path
from unittest.mock import patch
H=Path(os.environ['PRODUCT_SOURCE'])/'packaging/clang-bolt-helper.py'
T=Path(__file__).parent
def load():
 s=importlib.util.spec_from_file_location('h118',H);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def kind(k):
 def deco(f):f.evidence_kind=k;return f
 return deco
class Review118(unittest.TestCase):
 def setUp(self):
  self.h=load();self.d=Path(os.environ['TEST_SCRATCH'])/self._testMethodName;self.d.mkdir()
 def scenario(self,name):
  r=subprocess.run([sys.executable,'-B',str(T/'owned_scenario.py'),str(H),str(self.d/'owned'),name],capture_output=True,text=True,timeout=20)
  (self.d/'result.json').write_text(json.dumps({'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr},indent=2))
  self.assertEqual(r.returncode,0,r.stderr+r.stdout);v=json.loads(r.stdout);self.assertTrue(v['PASS'])
 @kind('mixed')
 def test_R1_permission_rescan_fork_real(self):self.scenario('permission')
 @kind('mixed')
 def test_R2_emfile_rescan_real(self):self.scenario('emfile')
 @kind('mixed')
 def test_R2_enomem_rescan_real(self):self.scenario('enomem')
 @kind('mixed')
 def test_ESRCH_after_real_pidfd_open(self):self.scenario('esrch')
 def seccomp(self,code):
  r=subprocess.run([sys.executable,'-B',str(T/'seccomp_scenario.py'),str(H),code,str(self.d)],capture_output=True,text=True,timeout=10)
  (self.d/'seccomp.json').write_text(json.dumps({'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr},indent=2))
  self.assertEqual(r.returncode,0,r.stderr+r.stdout)
  if code=='EINVAL':self.assertNotIn('SESSION_KILL_MODE',r.stderr)
  else:self.assertIn('SESSION_KILL_MODE=fallback-recheck errno='+code,r.stderr)
 @kind('real')
 def test_seccomp_enosys(self):self.seccomp('ENOSYS')
 @kind('real')
 def test_seccomp_eperm(self):self.seccomp('EPERM')
 @kind('real')
 def test_seccomp_eacces(self):self.seccomp('EACCES')
 @kind('real')
 def test_seccomp_einval_before_spawn(self):self.seccomp('EINVAL')
 @kind('mock')
 def test_eacces_send_probe_closes_fd(self):
  h=self.h;o=io.StringIO()
  with patch.object(h.os,'pidfd_open',return_value=71),patch.object(h.os,'close') as close,patch.object(h.signal,'pidfd_send_signal',side_effect=PermissionError(errno.EACCES,'denied')),contextlib.redirect_stderr(o):
   self.assertEqual(h.session_kill_mode(),'fallback-recheck')
  close.assert_called_once_with(71);self.assertEqual(o.getvalue(),'SESSION_KILL_MODE=fallback-recheck errno=EACCES\n')
 def diagnostic(self,scenario):
  h=self.h;clock=[0];calls=[0];members=[(99999999,'S',1)]
  def scan(*args):
   calls[0]+=1
   if scenario=='complete':return members
   if calls[0]==1 and scenario in ('partial_after_complete','timeout_after_complete'):return members
   clock[0]=2
   if scenario=='timeout_after_complete':raise h.SessionDeadlineError('scan incomplete',[])
   raise h.SessionInspectionError('scan incomplete',[])
  timer=types.SimpleNamespace(monotonic=lambda:clock[0],sleep=lambda n:clock.__setitem__(0,clock[0]+n))
  with patch.object(h,'time',timer),patch.object(h,'live_session_members',side_effect=scan),patch.object(h,'session_snapshot',return_value='99999999:worker (S)'):
   with self.assertRaises(h.GateError) as err:h.wait_session_exit(42,.05)
  return err.exception
 @kind('mock')
 def test_R3_complete_snapshot_has_pid_comm(self):
  e=self.diagnostic('complete');self.assertIsInstance(e,self.h.LiveDescendantsError);self.assertIn('99999999:worker',str(e));self.assertNotIn('scan incomplete',str(e))
 @kind('mock')
 def test_L2_incomplete_empty_keeps_previous(self):
  e=self.diagnostic('partial_after_complete');self.assertIsInstance(e,self.h.LiveDescendantsError);self.assertIn('last observed members (last complete scan): 99999999:worker',str(e));self.assertIn('final scan incomplete',str(e))
 @kind('mock')
 def test_L2_timed_out_empty_keeps_previous(self):
  e=self.diagnostic('timeout_after_complete');self.assertIsInstance(e,self.h.LiveDescendantsError);self.assertIn('last observed members (last complete scan): 99999999:worker',str(e));self.assertIn('final scan incomplete',str(e))
 @kind('mock')
 def test_R3_never_observed_no_invented_member(self):
  e=self.diagnostic('never');self.assertIn('partial observations: ;',str(e));self.assertNotIn('99999999',str(e))
 @kind('mixed')
 def test_call_unverified_not_labelled_live(self):
  h=self.h;real=h.wait_session_exit
  def wait(sid,*a,**kw):
   if kw.get('kill'):return real(sid,*a,**kw)
   raise h.SessionInspectionError('could not verify that the session is empty; last observed snapshot: ',[])
  with patch.object(h,'wait_session_exit',side_effect=wait),self.assertRaises(h.GateError) as e:
   h.call([sys.executable,'-c','pass'],self.d/'log')
  self.assertIn('could not verify',str(e.exception));self.assertNotIn('with live descendants',str(e.exception))
 def retirement(self,rc):
  h=self.h;seen=[];lines=H.read_text().splitlines()
  def trace(frame,event,arg):
   if event=='line' and frame.f_code.co_filename==str(H) and frame.f_code.co_name=='call' and lines[frame.f_lineno-1].strip()=='session_retired = True':
    self.assertIsNone(h._ACTIVE_SESSION);seen.append(frame.f_lineno)
   return trace
  old=sys.gettrace();sys.settrace(trace)
  try:
   if rc:
    with self.assertRaises(h.GateError):h.call([sys.executable,'-c','raise SystemExit(7)'],self.d/'log')
   else:h.call([sys.executable,'-c','pass'],self.d/'log')
  finally:sys.settrace(old)
  self.assertEqual(len(seen),1)
 @kind('mixed')
 def test_L1_success_before_retirement_store(self):self.retirement(0)
 @kind('mixed')
 def test_L1_failure_before_retirement_store(self):self.retirement(7)
 @kind('mock')
 def test_member_runtime_errno_matrix_no_fallback(self):
  for code in [errno.ENFILE,errno.ENOSYS,errno.EACCES,errno.EPERM,errno.EINVAL]:
   h=load();h._SESSION_KILL_MODE='pidfd'
   with patch.object(h,'live_session_members',side_effect=[[(31,'S',1),(32,'S',2)],[(31,'S',1)],[]]),patch.object(h,'kill_session_member',side_effect=[OSError(code,'member failure'),None,None]) as kill:
    with self.assertRaisesRegex(h.GateError,errno.errorcode[code]):h.wait_session_exit(42,1,kill=True)
   self.assertEqual([x.args[1] for x in kill.call_args_list],[31,32,31]);self.assertEqual(h._SESSION_KILL_MODE,'pidfd')
 @kind('mock')
 def test_malformed_member_stat_does_not_abort_pass(self):
  h=self.h
  with patch.object(h,'live_session_members',side_effect=[[(31,'S',1),(32,'S',2)],[]]),patch.object(h,'kill_session_member',side_effect=[h.GateError('malformed process stat'),None]) as kill:
   with self.assertRaisesRegex(h.GateError,'malformed'):h.wait_session_exit(42,1,kill=True)
  self.assertEqual(kill.call_count,2)
 @kind('real')
 def test_local_pidfd_mode_real(self):
  h=self.h;o=io.StringIO()
  with contextlib.redirect_stderr(o):self.assertEqual(h.session_kill_mode(),'pidfd')
  self.assertEqual(o.getvalue(),'SESSION_KILL_MODE=pidfd\n')
if __name__=='__main__':
 kinds={name:getattr(getattr(Review118,name),'evidence_kind') for name in dir(Review118) if name.startswith('test_')}
 (T/'test-118-kinds.json').write_text(json.dumps(kinds,indent=2))
 r=unittest.TextTestRunner(verbosity=2,failfast=True).run(unittest.defaultTestLoader.loadTestsFromTestCase(Review118))
 Path(os.environ['TEST_RESULT']).write_text(json.dumps({'tests':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'PASS':r.wasSuccessful()},indent=2))
 sys.exit(not r.wasSuccessful())
