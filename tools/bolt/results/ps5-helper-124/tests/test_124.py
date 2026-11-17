import importlib.util,os,types,unittest
from pathlib import Path
from unittest.mock import patch
H=Path(os.environ['PRODUCT_SOURCE'])/'packaging/clang-bolt-helper.py'
class Deadline124(unittest.TestCase):
 def setUp(self):
  spec=importlib.util.spec_from_file_location('h124',H);self.h=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.h)
 def test_scan_deadline_has_incomplete(self):
  h=self.h
  with patch.object(h.time,'monotonic',return_value=2):
   with self.assertRaises(h.SessionDeadlineError) as e:h.live_session_members(42,1)
  self.assertIn('session deadline expired; scan incomplete; last observed members:',str(e.exception));self.assertNotIn('while signalling',str(e.exception))
 def test_signalling_deadline_has_no_incomplete(self):
  h=self.h;clock=[0.];members=[(31,'S',1,'first'),(32,'S',2,'second')]
  def send(*args):clock[0]=2.
  with patch.object(h,'time',types.SimpleNamespace(monotonic=lambda:clock[0],sleep=lambda d:None)),patch.object(h,'live_session_members',return_value=members),patch.object(h,'kill_session_member',side_effect=send):
   with self.assertRaises(h.LiveDescendantsError) as e:h.wait_session_exit(42,1,kill=True)
  message=str(e.exception);self.assertIn('session deadline expired while signalling;',message);self.assertNotIn('scan incomplete',message);self.assertNotIn('final scan incomplete',message)
if __name__=='__main__':unittest.main(verbosity=2)
