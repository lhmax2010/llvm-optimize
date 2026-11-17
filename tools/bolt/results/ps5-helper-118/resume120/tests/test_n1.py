import unittest,signal,subprocess,sys,os,io,contextlib
from pathlib import Path
from unittest.mock import patch
from test_hq_requests import h,a
class N1(unittest.TestCase):
 def helper(self,fail):
  saved=signal.getsignal(signal.SIGCHLD)
  try:
   with patch.object(h.signal,'getsignal',return_value=None),patch.object(h.signal,'signal',wraps=signal.signal) as ss:
    if fail:
     original=OSError('N1 original spawn error')
     with patch.object(h.subprocess,'Popen',side_effect=original):
      with self.assertRaises(h.GateError) as caught:h.call(['fixture'],Path(os.environ['TEST_SCRATCH'])/'n1-fail.log')
     self.assertIs(caught.exception.__cause__,original)
    else:h.call([sys.executable,'-c','pass'],Path(os.environ['TEST_SCRATCH'])/'n1-ok.log')
    self.assertFalse(any(c.args==(signal.SIGCHLD,None) for c in ss.call_args_list))
  finally:signal.signal(signal.SIGCHLD,saved)
 def test_helper_none_success(self):self.helper(False)
 def test_helper_none_original_error(self):self.helper(True)
 def conv(self,error=None):
  saved=signal.getsignal(signal.SIGCHLD)
  try:
   with patch.object(a.signal,'getsignal',return_value=None),patch.object(a.signal,'signal',wraps=signal.signal) as ss,patch.object(a,'_install_main',side_effect=error,return_value=17),contextlib.redirect_stdout(io.StringIO()):
    if error is None:self.assertEqual(a.install_main(),17)
    else:
     with self.assertRaises(type(error)) as caught:a.install_main()
     self.assertIs(caught.exception,error)
    self.assertFalse(any(c.args==(signal.SIGCHLD,None) for c in ss.call_args_list))
  finally:signal.signal(signal.SIGCHLD,saved)
 def test_converter_none_success(self):self.conv()
 def test_converter_none_valueerror(self):self.conv(ValueError('original'))
 def test_converter_none_systemexit(self):self.conv(SystemExit(7))
 def test_converter_none_keyboardinterrupt(self):self.conv(KeyboardInterrupt())
if __name__=='__main__':unittest.main(verbosity=2)
