import contextlib,ctypes,importlib.util,io,json,os,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
H=Path(os.environ['PRODUCT_SOURCE'])/'packaging/clang-bolt-helper.py'
CODE="import ctypes,time; assert ctypes.CDLL(None).prctl(15,b'\\xff\\xfe',0,0,0)==0; print('ready',flush=True); time.sleep(40)"
class Utf8126(unittest.TestCase):
 def setUp(self):
  spec=importlib.util.spec_from_file_location('h126',H);self.h=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.h)
 @contextlib.contextmanager
 def child(self):
  p=subprocess.Popen([sys.executable,'-u','-c',CODE],start_new_session=True,stdout=subprocess.PIPE,text=True)
  try:
   self.assertEqual(p.stdout.readline().strip(),'ready');yield p
  finally:
   if p.poll() is None:p.kill()
   p.wait(timeout=5);p.stdout.close()
 def test_real_non_utf8_stat_shape_and_attribute(self):
  with self.child() as p:
   st=self.h.proc_stat('/proc/%d/stat'%p.pid);pid,state,pgrp,threads,sid,start=st
   self.assertEqual(len(st),6);self.assertEqual(st,(pid,state,pgrp,threads,sid,start));self.assertEqual(pid,p.pid);self.assertEqual(sid,p.pid);self.assertEqual(pgrp,p.pid)
   self.assertEqual(st.comm.encode('utf-8','surrogateescape'),b'\xff\xfe')
 def test_foreign_non_utf8_process_does_not_fail_step(self):
  with self.child() as p,tempfile.TemporaryDirectory() as tmp:
   self.assertNotEqual(os.getsid(p.pid),os.getsid(0));self.h.live_session_members(os.getsid(0))
   self.assertEqual(self.h.call(['/bin/sh','-c','exit 0'],Path(tmp)/'foreign.log'),'');self.assertIsNone(p.poll())
 def test_non_utf8_member_own_group_timeout_cleans(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=subprocess.Popen([sys.executable,'-B',str(Path(__file__).with_name('owned_utf8_scenario.py')),str(H),tmp],start_new_session=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
   try:out,err=p.communicate(timeout=30)
   finally:
    if p.poll() is None:p.kill();p.wait(timeout=5)
   self.assertEqual(p.returncode,0,err);r=json.loads(out);self.assertIn('TIMEOUT',r['error']);self.assertNotIn('cleanup error',r['error']);self.assertNotIn('codec',r['error'])
   ident=r['identity'];self.assertEqual(ident['sid'],ident['leader']);self.assertEqual(ident['pgrp'],ident['pid']);self.assertNotEqual(ident['pid'],ident['leader']);self.assertTrue(r['member_dead']);self.assertEqual(r['remaining_owned'],[])
   self.assertTrue(any('\ufffd\ufffd' in x for x in r['snapshots']),r)
 def test_snapshot_replacement_encodes_strict_utf8_without_io(self):
  m=self.h._StatTuple((31,'S',2));m.comm=b'\xff\xfe'.decode('utf-8','surrogateescape')
  with patch.object(Path,'read_bytes',side_effect=AssertionError('diagnostic I/O')),patch.object(Path,'read_text',side_effect=AssertionError('diagnostic I/O')):
   text=self.h.session_snapshot([m]);self.assertEqual(text,'31:\ufffd\ufffd (S)');self.assertEqual(text.encode('utf-8').decode('utf-8'),text)
if __name__=='__main__':unittest.main(verbosity=2)
