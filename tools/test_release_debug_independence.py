#!/usr/bin/env python3
"""Fixed ELF32/ELF64 positive and negative controls for the release gate."""
import copy
from pathlib import Path
import subprocess
import tempfile
import unittest
import check_release_debug_independence as gate


class ReleaseGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory(prefix='release-gate-')
        root = Path(cls.directory.name)
        source = root/'fixture.s'
        source.write_text('.text\n.globl test_entry\n.type test_entry,@function\n'
                          'test_entry:\ncall external_function\nret\n'
                          '.size test_entry,.-test_entry\n.data\n.long 17\n.long .text\n')
        cls.pairs = {}
        for bits in (32, 64):
            items = []
            for debug in (True, False):
                target = root/('%d-%s.o' % (bits, debug))
                subprocess.run(['as', '--'+str(bits), *(['-g'] if debug else []),
                                str(source), '-o', str(target)], check=True, capture_output=True)
                items.append(gate.parse(target.read_bytes()))
            cls.pairs[bits] = items

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def test_actual_elf32_rel_and_debug_filter(self):
        a,b = self.pairs[32]
        self.assertTrue(a['debug_sections']); self.assertFalse(b['debug_sections'])
        self.assertEqual(a['relocations'][0]['type'], 2)
        self.assertEqual(a['relocations'][0]['format'], 'REL')
        self.assertEqual(gate.compare(a,b)['status'], 'PASS')

    def test_actual_elf64_rela_and_debug_filter(self):
        a,b = self.pairs[64]
        self.assertEqual(a['relocations'][0]['type'], 4)
        self.assertEqual(a['relocations'][0]['addend'], -4)
        self.assertEqual(gate.compare(a,b)['status'], 'PASS')

    def rejected(self, change, category):
        a,b = copy.deepcopy(self.pairs[64]); change(b)
        result = gate.compare(a,b)
        self.assertEqual(result['status'], 'FAIL')
        self.assertFalse(result['checks'][category])
        self.assertIn(category, result['differences'])

    def test_alloc_contents(self):
        self.rejected(lambda b:b['alloc'][0].update(content=b'changed'), 'alloc')

    def test_alloc_flags(self):
        self.rejected(lambda b:b['alloc'][0].update(flags=3), 'alloc')

    def test_alloc_size(self):
        self.rejected(lambda b:b['alloc'][0].update(size=7), 'alloc')

    def test_alloc_name(self):
        self.rejected(lambda b:b['alloc'][0].update(section=['.different',0]), 'alloc')

    def test_relocation_fields(self):
        for field, value in [('offset',3),('type',2),('symbol','other'),('addend',-8)]:
            with self.subTest(field=field):
                self.rejected(lambda b:b['relocations'][0].update({field:value}), 'relocations')

    def test_symbol_fields(self):
        for field, value in [('name','other'),('type',1),('binding',2),('visibility',2),
                             ('section',['.data',0]),('value',3),('size',27)]:
            with self.subTest(field=field):
                def change(b):
                    s = next(s for s in b['symbols'] if s['name']=='test_entry')
                    s[field] = value
                self.rejected(change,'symbols')

    def test_additional_non_debug_section_symbol_rejected(self):
        self.rejected(lambda b:b['symbols'].append(dict(name='',type=3,binding=0,
                      visibility=0,section=['.other',0],value=0,size=0)), 'symbols')

    def test_release_debug_sections_rejected(self):
        self.rejected(lambda b:b['debug_sections'].append('.debug_info'), 'release_no_debug')

    def test_rel_implicit_addend_bytes(self):
        a,b = copy.deepcopy(self.pairs[32]); b['alloc'][0]['content'] = b'changed'
        self.assertFalse(gate.compare(a,b)['checks']['alloc'])

    def test_truncated_elf_rejected(self):
        with self.assertRaises(ValueError): gate.parse(b'\x7fELF')


if __name__ == '__main__':
    unittest.main(verbosity=2)
