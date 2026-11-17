import unittest,io,contextlib,signal,os,json,struct
from unittest.mock import patch
from test_hardening import a,old,fixture
class ReviewR11(unittest.TestCase):
 def test_compression_1_2_alignment_0_1_8(self):
  for typ in (1,2):
   for align in (0,1,8):
    with self.subTest(typ=typ,align=align): self.assertEqual(a.pic_relocations(fixture(compressed=True,typ=typ,alignment=align)),old.pic_relocations(fixture(compressed=True,typ=typ,alignment=align)))
 def test_compression_unknown_rejected(self):
  with self.assertRaisesRegex(ValueError,'unsupported ELF compression type'):a.pic_relocations(fixture(compressed=True,typ=3))
 def test_alignment_three_rejected(self):
  with self.assertRaisesRegex(ValueError,'invalid compressed ELF section alignment'):a.pic_relocations(fixture(compressed=True,alignment=3))
 def test_truncated_header_rejected(self):
  with self.assertRaisesRegex(ValueError,'short compressed'):a.pic_relocations(fixture(compressed=True,size=23))
 def test_tlsdesc_two_byte_call_at_limit_minus_two(self):
  b=fixture(35,6);b[326:328]=bytes.fromhex('ff10')
  self.assertEqual(a.pic_relocations(b),old.pic_relocations(b))
 def test_marker_limit_and_beyond_rejected(self):
  for off in (8,9):
   with self.subTest(offset=off),self.assertRaisesRegex(ValueError,'offset outside'):a.pic_relocations(fixture(35,off))
 def test_marker_empty_section_rejected(self):
  b=fixture(35,0);struct.pack_into('<Q',b,128+32,0)
  with self.assertRaisesRegex(ValueError,'offset outside'):a.pic_relocations(b)
 def test_none_exemption_empty_and_end(self):
  for off in (0,8,9):
   b=fixture(0,off);struct.pack_into('<Q',b,128+32,0)
   self.assertEqual(a.pic_relocations(b),old.pic_relocations(b))
 def test_nonzero_exact_end_accepted(self):
  self.assertEqual(a.pic_relocations(fixture(2,4)),old.pic_relocations(fixture(2,4)))
 def test_nonzero_one_byte_overrun_rejected(self):
  with self.assertRaisesRegex(ValueError,'offset outside'):a.pic_relocations(fixture(2,5))
 def test_empty_relr_rejected(self):
  b=fixture();struct.pack_into('<I',b,64+4,19)
  with self.assertRaisesRegex(ValueError,'unsupported RELR'):a.pic_relocations(b)
 def capture(self,env):
  out=io.StringIO()
  with patch.dict(os.environ,env,clear=True),contextlib.redirect_stdout(out):a.log_startup_context()
  return json.loads(out.getvalue().split(' ',1)[1])
 def test_normal_sigint_default(self):
  self.assertIs(signal.getsignal(signal.SIGINT),signal.default_int_handler)
  self.assertEqual(self.capture({})['signals']['SIGINT'],'default')
 def test_ignored(self):
  with patch.object(a.signal,'getsignal',return_value=signal.SIG_IGN):self.assertEqual(set(self.capture({})['signals'].values()),{'ignored'})
 def test_non_python(self):
  with patch.object(a.signal,'getsignal',return_value=None):self.assertEqual(set(self.capture({})['signals'].values()),{'non-python'})
 def test_unset_null_and_set_empty_list(self):
  self.assertEqual(self.capture({})['architecture_parameters'],{'CFLAGS':None,'CXXFLAGS':None})
  self.assertEqual(self.capture({'CFLAGS':'','CXXFLAGS':'-O2'})['architecture_parameters'],{'CFLAGS':[],'CXXFLAGS':[]})
 def test_write_error_nonfatal(self):
  class Bad:
   def write(self,*args):raise BrokenPipeError('write failure')
   def flush(self):pass
  with contextlib.redirect_stdout(Bad()):a.log_startup_context()
 def test_flush_error_nonfatal(self):
  class Bad(io.StringIO):
   def flush(self):raise OSError('flush failure')
  with contextlib.redirect_stdout(Bad()):a.log_startup_context()
 def test_closed_stream_nonfatal(self):
  out=io.StringIO();out.close()
  with contextlib.redirect_stdout(out):a.log_startup_context()
 def test_keyboard_interrupt_propagates(self):
  class Bad:
   def write(self,*args):raise KeyboardInterrupt()
   def flush(self):pass
  with self.assertRaises(KeyboardInterrupt),contextlib.redirect_stdout(Bad()):a.log_startup_context()
if __name__=='__main__':unittest.main(verbosity=2,failfast=True)
