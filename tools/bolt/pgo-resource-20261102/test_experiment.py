import unittest,json,shlex,ast
from common import *
from monitor import phase_for
from unittest.mock import patch
from types import SimpleNamespace
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
  d=disk_budget();self.assertEqual(d['target_budget_bytes'],(24*70485561344+9)//10+20*1024**3);self.assertEqual(d['required_bytes'],2*70485561344+20*1024**3)
 def test_rehearsal_config_only(self):
  tree=ast.parse((T/'driver.py').read_text());self.assertTrue(any(isinstance(n,ast.If) and ast.unparse(n.test)=='not rehearsal' for n in ast.walk(tree)))
 def budget_at(self,free):
  with patch('common.os.statvfs',return_value=SimpleNamespace(f_bavail=free,f_frsize=1)):return disk_budget()
 def test_budget_above_target(self):
  target=disk_budget()['target_budget_bytes'];d=self.budget_at(target+1);self.assertTrue(d['PASS']);self.assertNotIn('BUDGET_MARGIN_WARNING',d);self.assertEqual(d['target_shortfall_bytes'],0)
 def test_budget_between_minimum_and_target(self):
  limits=disk_budget();free=(limits['minimum_start_bytes']+limits['target_budget_bytes'])//2;d=self.budget_at(free);self.assertTrue(d['PASS']);w=d['BUDGET_MARGIN_WARNING'];self.assertIn('available_bytes='+str(free),w);self.assertIn('target_budget_bytes='+str(limits['target_budget_bytes']),w);self.assertIn('shortfall_bytes='+str(limits['target_budget_bytes']-free),w)
 def test_budget_below_minimum(self):
  d=self.budget_at(disk_budget()['minimum_start_bytes']-1);self.assertFalse(d['PASS']);self.assertNotIn('BUDGET_MARGIN_WARNING',d)
if __name__=='__main__':unittest.main(verbosity=2)
