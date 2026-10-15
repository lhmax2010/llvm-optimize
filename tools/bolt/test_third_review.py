"""PM review thirteen: independent closure, historical plan and scoped CMake links."""
from pathlib import Path
import json,lzma,unittest
import bolt_helper as h
from test_bolt_helper import Base

R=Path(__file__).parent/'results'
class ThirdPlanTests(unittest.TestCase):
    def test_independent_111_descriptions(self):
        descriptions=json.loads((R/'review-tool-descriptions-v2.json').read_text())
        self.assertEqual(len(descriptions),111);self.assertEqual(set(descriptions),h.BOLT_TASK_DESCRIPTIONS)
        old=json.loads((R/'review-tool-descriptions.json').read_text())
        self.assertEqual(set(descriptions)-set(old),{'Generating VCSVersion.inc'})
        self.assertEqual(set(old)-set(descriptions),set())
    def test_vcs_description_is_unique_in_closure(self):
        graph=json.loads(lzma.open(R/'review-closure-v2.json.xz','rt').read())
        matches=[row for row in graph['closure'] if row['description']=='Generating VCSVersion.inc']
        self.assertEqual(len(matches),1)
        self.assertEqual(matches[0]['outputs'],['tools/bolt/lib/Utils/VCSVersion.inc'])
        self.assertTrue(matches[0]['new'])
        self.assertEqual(len(graph['classification_changes']),1)
        self.assertFalse(graph['classification_changes'][0]['old_new'])
    def test_generated_counter(self):
        text='[1/2] Generating VCSVersion.inc\n[2/2] Linking CXX executable bin/llvm-bolt\n'
        self.assertEqual(h.tool_plan(text)['categories'],{'objects':0,'static_libraries':0,'executables':1,'generated':1})
    def test_historical_filtered_113(self):
        value=h.tool_plan((R/'review3-history-current-plan.txt').read_text())
        self.assertEqual(value['tasks'],113);self.assertEqual(value['configuration_refresh_tasks'],2)
        self.assertEqual(value['categories'],{'objects':102,'static_libraries':7,'executables':1,'generated':1})
    def test_all_historical_tasks_attributed(self):
        value=json.loads((R/'review3-history-reconciliation.json').read_text())
        self.assertEqual(len(value['rows']),126);self.assertEqual(value['unattributed'],0)
        self.assertEqual(value['counts'],{'TF':2,'disabled-runtime':8,'BOLT':111,'disabled-merge-fdata':2,'disabled-AArch64':3})
    def test_unknown_generated_still_rejected(self):
        with self.assertRaises(h.GateError):h.tool_plan('[1/2] Generating Unknown.inc\n[2/2] Linking CXX executable bin/llvm-bolt')
    def test_only_tf_file_refreshed(self):
        value=json.loads((R/'review3-external-input-audit.json').read_text())
        self.assertEqual([r['path'] for r in value['build_directory_external_inputs'] if r['rewritten_on_reconfigure']],['lib64/tf_runtime/tf_xla_runtime_dummy.c'])

class ThirdReverseTests(Base):
    def test_dangling_ordinary_link_allowed(self):
        (self.d/'ordinary').symlink_to('missing')
        self.assertTrue(h.no_bolt_products(self.d)['no_bolt_products'])
    def test_escaping_ordinary_link_allowed(self):
        (self.d/'ordinary').symlink_to('../../outside-root')
        self.assertTrue(h.no_bolt_products(self.d)['no_bolt_products'])
    def test_dangling_cmake_rejected(self):
        (self.d/'ordinary.cmake').symlink_to('missing')
        with self.assertRaisesRegex(h.GateError,'dangling CMake metadata'):h.no_bolt_products(self.d)
    def test_escaping_cmake_rejected(self):
        (self.d/'ordinary.cmake').symlink_to('../../outside-root')
        with self.assertRaisesRegex(h.GateError,'escapes buildroot'):h.no_bolt_products(self.d)
    def test_internal_cmake_link_checked(self):
        (self.d/'target').write_text('set(project baseline)')
        (self.d/'ordinary.cmake').symlink_to('/target')
        self.assertEqual(h.no_bolt_products(self.d)['cmake_files_checked'],1)
        (self.d/'target').write_text('set(libs LLVMBOLTCore)')
        with self.assertRaisesRegex(h.GateError,'LLVMBOLT'):h.no_bolt_products(self.d)

if __name__=='__main__':unittest.main()
