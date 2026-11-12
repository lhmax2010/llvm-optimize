from pathlib import Path
from unittest.mock import patch
import os,sys,json,unittest
os.environ['NIGHT_SOURCE_SHA']='9e39fa8a61392652bb28b75fc26216675bcad1d5'
import launcher as L
class Startup(unittest.TestCase):
 def call(self,head,status):
  calls=[]
  def fake(argv,**kwargs):
   calls.append(argv)
   return head+'\nTREE\n' if 'rev-parse' in argv else status
  with patch.object(L.subprocess,'check_output',fake):r=L.check_source()
  self.assertIn('--untracked-files=no',calls[1]);return r
 def test_clean(self):self.assertEqual(self.call(L.COMMIT,'')['commit'],L.COMMIT)
 def test_wrong_sha(self):
  with self.assertRaises(AssertionError):self.call('0'*40,'')
 def test_tracked_modification(self):
  with self.assertRaises(AssertionError):self.call(L.COMMIT,' M packaging/llvm.spec\n')
 def test_staged_modification(self):
  with self.assertRaises(AssertionError):self.call(L.COMMIT,'M  packaging/llvm.spec\n')
 def test_untracked_query_ignored(self):self.call(L.COMMIT,'')
if __name__=='__main__':unittest.main(verbosity=2)
