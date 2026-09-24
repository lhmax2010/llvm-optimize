#!/usr/bin/env python3
"""Regression checks for structural option comparison (no LLVM build)."""
import subprocess
import tempfile
import unittest
from pathlib import Path
from compare_native_conversion_options import BACKEND_FLAGS, describe, differences


class StructuralComparisonTests(unittest.TestCase):
    def test_sections_symbols_visibility_and_relocations(self):
        with tempfile.TemporaryDirectory() as name:
            root=Path(name)
            src=root/'probe.s'; obj=root/'probe.o'
            src.write_text('.section .text.probe,"ax",@progbits\n'
                           '.global probe\n.hidden probe\n.type probe,@function\n'
                           'probe: call external\nret\n.size probe,.-probe\n'
                           '.section .data.item,"aw",@progbits\n'
                           '.global item\n.type item,@object\nitem: .quad 1\n')
            subprocess.run(['as','--64',str(src),'-o',str(obj)],check=True,capture_output=True)
            found=describe(obj,root)
            self.assertEqual(found['text_function_sections'],1)
            self.assertEqual(found['sections']['.data.item'],1)
            self.assertIn(('probe','FUNC','GLOBAL','HIDDEN'),found['defined_symbols'])
            self.assertNotIn('external',[s[0] for s in found['defined_symbols']])
            self.assertEqual(found['relocations']['R_X86_64_PLT32'],1)
            self.assertFalse(any(x['only_native'] or x['only_ir_native'] for x in differences(found,found).values()))

    def test_equal_counts_do_not_hide_wrong_sections_or_visibility(self):
        a=dict(sections={'.text.a':1},relocations={'R_X86_64_PLT32':1},defined_symbols=[('a','FUNC','GLOBAL','HIDDEN')])
        b=dict(sections={'.text.b':1},relocations={'R_X86_64_PC32':1},defined_symbols=[('a','FUNC','GLOBAL','DEFAULT')])
        self.assertTrue(all(v['only_native'] and v['only_ir_native'] for v in differences(a,b).values()))

    def test_duplicate_sections_are_counted(self):
        a=dict(sections={'.group':2},relocations={},defined_symbols=[])
        b=dict(sections={'.group':1},relocations={},defined_symbols=[])
        self.assertEqual(differences(a,b)['sections']['only_native'],[('.group',1)])

    def test_backend_flags_include_sections_and_exclude_lto(self):
        self.assertIn('-ffunction-sections',BACKEND_FLAGS)
        self.assertIn('-fdata-sections',BACKEND_FLAGS)
        self.assertFalse(any('lto' in f for f in BACKEND_FLAGS))


if __name__=='__main__':unittest.main(verbosity=2)
