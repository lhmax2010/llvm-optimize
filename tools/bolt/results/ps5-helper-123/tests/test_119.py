import importlib.util,json,os,subprocess,sys,types,unittest,errno
from pathlib import Path
from unittest.mock import patch
H=Path(os.environ['PRODUCT_SOURCE'])/'packaging/clang-bolt-helper.py'
OBS=[]
class Diagnostic119(unittest.TestCase):
 def setUp(self):
  spec=importlib.util.spec_from_file_location('helper119',H);self.h=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.h)
 def exercise(self,case):
  h=self.h;clock=[0.0];calls=[0];p=None
  if case!='first_empty':
   p=subprocess.Popen([sys.executable,'-u','-c','import time;print("ready",flush=True);time.sleep(30)'],start_new_session=True,stdout=subprocess.PIPE,text=True)
   self.assertEqual(p.stdout.readline().strip(),'ready')
  try:
   sid=p.pid if p else 99999999
   real_scan=h.live_session_members
   owned=real_scan(sid) if p else []
   if p:self.assertEqual([x[0] for x in owned],[p.pid])
   def scan(*args):
    calls[0]+=1
    if case in ('first_member','first_empty') or (calls[0]>1 and case in ('complete_partial','kill_wrapper')):
     clock[0]=2.0
     raise h.SessionDeadlineError('deadline during scan',owned if case=='first_member' else [])
    return real_scan(sid)
   def sleep(delay):clock[0]=2.0 if case=='complete_next' else clock[0]+delay
   def denied(*args):clock[0]=2.0;raise OSError(errno.EMFILE,'member injected')
   timer=types.SimpleNamespace(monotonic=lambda:clock[0],sleep=sleep)
   with patch.object(h,'time',timer),patch.object(h,'live_session_members',side_effect=scan):
    with self.assertRaises(h.GateError) as caught:
     if case=='member_error':
      with patch.object(h,'kill_session_member',side_effect=denied):h.wait_session_exit(sid,1,kill=True)
     elif case=='kill_wrapper':
      # Keep the known child alive for a controlled incomplete cleanup scan.
      with patch.object(h.os,'killpg'),patch.object(h,'kill_session_member'):h.kill_session(sid,1)
     else:h.wait_session_exit(sid,1)
   e=caught.exception;message=str(e)
   if case in ('first_member','first_empty'):
    self.assertIsInstance(e,h.SessionInspectionError);self.assertIn('could not verify that the session is empty',message);self.assertIn('partial observations: ',message)
    self.assertNotIn('last complete scan',message)
   else:
    self.assertIsInstance(e,h.LiveDescendantsError);self.assertIn('last observed members (last complete scan): ',message)
   if p:self.assertIn(str(p.pid)+':python',message)
   else:self.assertNotIn('99999999:',message)
   if case in ('complete_partial','kill_wrapper'):self.assertIn('final scan incomplete',message)
   if case=='member_error':self.assertIn('errors: PID '+str(p.pid)+' errno=EMFILE',message)
   OBS.append({'case':case,'kind':'mock' if case=='first_empty' else 'mixed-real-process-controlled-scan','message':message,'scans':calls[0],'owned_pid':p.pid if p else None})
  finally:
   if p:
    # Only the test-owned Popen, never a name or unowned numeric PID.
    if p.poll() is None:p.kill()
    p.wait(timeout=5);p.stdout.close()
 def test_complete_then_next_scan_deadline(self):self.exercise('complete_next')
 def test_complete_then_partial_empty_deadline(self):self.exercise('complete_partial')
 def test_first_partial_with_actual_member(self):self.exercise('first_member')
 def test_first_partial_empty(self):self.exercise('first_empty')
 def test_member_error_details(self):self.exercise('member_error')
 def test_kill_session_uses_same_diagnostic(self):self.exercise('kill_wrapper')
if __name__=='__main__':
 r=unittest.TextTestRunner(verbosity=2,failfast=True).run(unittest.defaultTestLoader.loadTestsFromTestCase(Diagnostic119))
 Path(os.environ['TEST_RESULT']).write_text(json.dumps({'tests':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'PASS':r.wasSuccessful(),'observations':OBS},indent=2)+'\n')
 sys.exit(not r.wasSuccessful())
