import unittest,json,shlex,ast
from common import *
from monitor import phase_for
class Tests(unittest.TestCase):
 def test_training_count(self):
  rows=json.loads((E/'training.json').read_text());self.assertEqual(len(rows),23);self.assertEqual(sum(r['target'].startswith('armv7l') for r in rows),13)
 def test_training_hashes(self):
  for r in json.loads((E/'training.json').read_text()):self.assertEqual(sha(r['path']),r['sha256'])
 def test_A_only_IR(self):
  a=json.loads((E/'cmake-A.json').read_text());self.assertEqual(a[-2],'-DLLVM_BUILD_INSTRUMENTED=IR');self.assertEqual(a[:-2]+a[-1:],json.loads((E/'cmake-base.json').read_text()))
 def test_D_only_profile(self):
  a=json.loads((E/'cmake-D.json').read_text());self.assertEqual(a[-2],'-DLLVM_PROFDATA_FILE='+PROFDATA);self.assertEqual(a[:-2]+a[-1:],json.loads((E/'cmake-base.json').read_text()))
 def test_spec_one_line(self):
  original=(S/'packaging/llvm.spec').read_text();copy=(P/'source-D/packaging/llvm.spec').read_text();self.assertEqual(copy.replace('    -DLLVM_PROFDATA_FILE='+PROFDATA+' \\\n',''),original)
 def test_resources(self):
  p=props();self.assertIn('CPUQuota=1200%',p);self.assertIn('MemorySwapMax=0',p);self.assertIn('Nice=10',p)
 def test_no_modified_source_files(self):
  for name in ['clang-bolt-helper.py','clang-bolt-v2.fdata.xz','llvm-static-archives-native.py']:
   self.assertEqual(sha(S/'packaging'/name),sha(P/'source-D/packaging'/name))
 def test_phase_begin(self):self.assertEqual(phase_for('BOLT_DISK_REPORT {"stage": "begin"}','ordinary-install'),'BOLT')
 def test_phase_post_keeps(self):self.assertEqual(phase_for('BOLT_DISK_REPORT {"stage": "post"}','platform-post'),'platform-post')
 def test_phases(self):
  for text,phase in [('Executing(%build)','ordinary-compile'),('Executing(%install)','ordinary-install'),('BOLT_COMPARE_ROOT_PASS','cache-release'),('BOLT_CACHE_RELEASE removed','archive-install'),('/usr/lib/rpm/find-debuginfo.sh','platform-post'),('Processing files: llvm','packaging')]:self.assertEqual(phase_for(text,'prior'),phase)
 def test_disk_budget_known_formula(self):
  d=disk_budget();self.assertEqual(d['required_bytes'],3*68252237824+20*1024**3)
 def test_rehearsal_config_only(self):
  tree=ast.parse((T/'driver.py').read_text());self.assertTrue(any(isinstance(n,ast.If) and ast.unparse(n.test)=='not rehearsal' for n in ast.walk(tree)))
if __name__=='__main__':unittest.main(verbosity=2)
