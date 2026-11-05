from pathlib import Path
import sys,json,unittest
T=Path(__file__).resolve().parents[3]/'night-launch-20261105'
sys.path.insert(0,str(T))
from validate import flags
class Tests(unittest.TestCase):
 def test_flags(self):
  q=json.loads((T/'qb-reference.json').read_text());s=[r['text'] for r in q['flags']];self.assertEqual(flags(['[ 123s] '+x for x in s]),s);self.assertEqual(flags(['[ 1s] + printf TIZEN_LLVM_FLAGS_WARNING x']),[])
 def test_warning_not_ignored(self):self.assertEqual(flags(['[ 2s] TIZEN_LLVM_FLAGS_WARNING x']),['TIZEN_LLVM_FLAGS_WARNING x'])
 def test_single_project(self):
  text=(T/'launch.sh').read_text();self.assertNotIn('night.py',text);self.assertIn('FINAL_PROJECT=toolchain',text);self.assertIn("assert PROJECT == 'toolchain'",(T/'launcher.py').read_text())
 def test_source_and_snapshot(self):
  q=json.loads((T/'qb-reference.json').read_text());self.assertEqual(q['commit'],'9e39fa8a61392652bb28b75fc26216675bcad1d5');self.assertEqual(q['snapshot'],'tizen-base-toolchain_20261030.061318');self.assertEqual(q['identity']['after_sha256'],'e08724d81231d8675c51d4908f4ff0e8d233ef3740c878da1c7eda42dd3532f5')
if __name__=='__main__':unittest.main()
