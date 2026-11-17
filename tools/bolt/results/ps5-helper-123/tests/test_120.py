import importlib.util,os,types,unittest
from pathlib import Path
from unittest.mock import patch
H=Path(os.environ['PRODUCT_SOURCE'])/'packaging/clang-bolt-helper.py'
class Diagnostic120(unittest.TestCase):
 def exercise(self,partial):
  spec=importlib.util.spec_from_file_location('helper120',H);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
  clock=[0.];calls=[0];members=[(99999999,'S',1)]
  def scan(*args):
   calls[0]+=1
   if calls[0]==1:return members
   clock[0]=2.
   raise h.SessionDeadlineError('deadline during scan',[])
  def sleep(delay):clock[0]=.1 if partial else 2.
  with patch.object(h,'time',types.SimpleNamespace(monotonic=lambda:clock[0],sleep=sleep)),patch.object(h,'live_session_members',side_effect=scan),patch.object(h,'session_snapshot',return_value='99999999:worker (S)'):
   with self.assertRaises(h.LiveDescendantsError) as caught:h.wait_session_exit(42,1)
  message=str(caught.exception)
  self.assertIn('last observed members (last complete scan): 99999999:worker (S)',message)
  self.assertEqual('final scan incomplete' in message,partial)
  self.assertEqual(calls[0],2 if partial else 1)
 def test_deadline_between_scans_is_not_incomplete(self):self.exercise(False)
 def test_deadline_inside_scan_is_incomplete(self):self.exercise(True)
if __name__=='__main__':unittest.main(verbosity=2,failfast=True)
