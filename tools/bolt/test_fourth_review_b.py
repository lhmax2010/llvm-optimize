"""Fourteen B: embedded maintenance and the final diagnostic refinements."""
import ast
from pathlib import Path
import unittest
import bolt_helper as h

LINK = 'Linking CXX executable bin/llvm-bolt'

class FourthReviewBTests(unittest.TestCase):
    def test_maintenance_header_covers_remedies_and_recertification(self):
        doc=h.__doc__
        for token in ('Tool-version remedy:', 'Profile-SHA remedy:', 'Unapproved-task remedy:',
                      'Matching remedy:', 'CERTIFIED.llvm_version', 'tf_refresh_task_count',
                      '%bcond_with clang_bolt', 'accel/worker', '13 ARM workloads',
                      'merge-fdata', 'exclude holdouts', 'RPM/DWARF', 'Build-ID'):
            with self.subTest(token=token):self.assertIn(token,doc)
    def test_only_helper_docstring_changed_from_previous_squash(self):
        previous=Path(__file__).parent/'results/review4-rebased-helper.py'
        def program(text):
            module=ast.parse(text)
            self.assertIsInstance(module.body[0],ast.Expr)
            self.assertIsInstance(module.body[0].value,ast.Constant)
            module.body=module.body[1:]
            return ast.dump(module,include_attributes=False)
        self.assertEqual(program(previous.read_text()),program(Path(h.__file__).read_text()))
    def test_diagnostics_count_matches_preserved_warning_lines(self):
        warnings=['ninja: warning: first','ninja: warning: second']
        for body in ('ninja: no work to do.','[1/1] '+LINK):
            with self.subTest(body=body):
                value=h.tool_plan('\n'.join(warnings+[body]))
                self.assertEqual(value['ninja_diagnostics'],warnings)
                self.assertEqual(value['ninja_diagnostics_count'],2)
    def test_regeneration_in_warning_is_rejected_before_filtering(self):
        for body in ('ninja: no work to do.','[1/1] '+LINK):
            with self.subTest(body=body),self.assertRaisesRegex(h.GateError,'real plan is not visible'):
                h.tool_plan('ninja: warning: Re-running CMake...\n'+body)

if __name__=='__main__':unittest.main()
