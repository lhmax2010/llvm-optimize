import importlib.util,os,subprocess,sys,unittest
from pathlib import Path
from unittest.mock import patch
H=Path(os.environ['PRODUCT_SOURCE'])/'packaging/clang-bolt-helper.py'
class Tuple125(unittest.TestCase):
 def setUp(self):
  spec=importlib.util.spec_from_file_location('h125',H);self.h=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.h)
 def test_real_stat_six_fields_and_comm(self):
  st=self.h.proc_stat('/proc/self/stat');pid,state,pgrp,threads,sid,start=st
  self.assertEqual(len(st),6);self.assertEqual(st,(pid,state,pgrp,threads,sid,start));self.assertEqual(pid,os.getpid());self.assertTrue(st.comm.startswith('python'));self.assertFalse(hasattr(type(st),'__slots__'))
 def test_real_member_three_fields_name_after_exit_no_io(self):
  p=subprocess.Popen([sys.executable,'-u','-c','import time;print("ready",flush=True);time.sleep(30)'],start_new_session=True,stdout=subprocess.PIPE,text=True)
  try:
   self.assertEqual(p.stdout.readline().strip(),'ready');real=Path.read_text
   def read(path,*a,**kw):
    self.assertFalse(str(path).endswith('/comm'));return real(path,*a,**kw)
   with patch.object(Path,'read_text',read):members=self.h.live_session_members(p.pid)
   self.assertEqual(len(members),1);m=members[0];pid,state,start=m;self.assertEqual(len(m),3);self.assertEqual(m,(pid,state,start));self.assertTrue(m.comm.startswith('python'))
   name=m.comm;p.kill();p.wait(timeout=5)
   with patch.object(Path,'read_text',side_effect=AssertionError('diagnostic I/O')):text=self.h.session_snapshot(members)
   self.assertIn(str(p.pid)+':'+name,text)
  finally:
   if p.poll() is None:p.kill()
   p.wait(timeout=5);p.stdout.close()
 def test_plain_tuple_snapshot_unknown_without_io(self):
  with patch.object(Path,'read_text',side_effect=AssertionError('diagnostic I/O')):
   self.assertEqual(self.h.session_snapshot([(31,'S',1)]),'31:? (S)')
 def test_sort_and_equality_ignore_comm(self):
  a=self.h._StatTuple((32,'S',2));a.comm='z';b=self.h._StatTuple((31,'S',1));b.comm='a'
  self.assertEqual(sorted([a,b]),[(31,'S',1),(32,'S',2)]);self.assertEqual(a,(32,'S',2));self.assertEqual(hash(a),hash((32,'S',2)))
if __name__=='__main__':unittest.main(verbosity=2)
