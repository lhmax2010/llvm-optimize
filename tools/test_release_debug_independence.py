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
        cls.root = root
        cls.sequence = 0
        source = root/'fixture.s'
        source.write_text('.text\n.globl test_entry\n.type test_entry,@function\n'
                          'test_entry:\ncall external_function\nret\n'
                          '.size test_entry,.-test_entry\n.data\n.long 17\n.long .text\n')
        cls.assembly = source.read_text()
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
        self.rejected(lambda b:b['alloc'][0].update(section='.different'), 'alloc')

    def test_alloc_type_alignment_entsize(self):
        for field,value in [('type',7),('alignment',64),('entsize',16)]:
            with self.subTest(field=field):
                self.rejected(lambda b:b['alloc'][0].update({field:value}), 'alloc')

    def test_alloc_order(self):
        self.rejected(lambda b:b['alloc'].reverse(), 'alloc')

    def test_relocation_fields(self):
        for field, value in [('offset',3),('type',2),('symbol','other'),('addend',-8)]:
            with self.subTest(field=field):
                self.rejected(lambda b:b['relocations'][0].update({field:value}), 'relocations')

    def test_symbol_fields(self):
        for field, value in [('name','other'),('type',1),('binding',2),('visibility',2),
                             ('section','.data'),('value',3),('size',27)]:
            with self.subTest(field=field):
                def change(b):
                    s = next(s for s in b['symbols'] if s['name']=='test_entry')
                    s[field] = value
                self.rejected(change,'symbols')

    @classmethod
    def assemble(cls, extra='', bits=64):
        cls.sequence += 1
        source = cls.root/('extra-%d.s' % cls.sequence)
        target = source.with_suffix('.o')
        source.write_text(cls.assembly+extra)
        subprocess.run(['as','--'+str(bits),'-L',str(source),'-o',str(target)],
                       check=True,capture_output=True)
        return gate.parse(target.read_bytes())

    def test_additional_section_symbol_passes(self):
        a=self.assemble('.section .debug_probe,"",@progbits\n.quad .data\n')
        b=self.assemble()
        self.assertEqual(sum(s['type']==3 for s in a['excluded_symbols']),
                         sum(s['type']==3 for s in b['excluded_symbols'])+1)
        self.assertEqual(gate.compare(a,b)['status'],'PASS')

    def test_unreferenced_dot_l_local_passes(self):
        a=self.assemble('.local .Lunused\n.set .Lunused,19\n');b=self.assemble()
        self.assertTrue(any(s['name']=='.Lunused' for s in a['excluded_symbols']))
        self.assertEqual(gate.compare(a,b)['status'],'PASS')

    def test_named_local_difference_fails(self):
        a=self.assemble('.local bookkeeping\n.set bookkeeping,19\n');b=self.assemble()
        self.assertFalse(gate.compare(a,b)['checks']['symbols'])

    def test_dot_l_global_is_compared(self):
        a=self.assemble('.globl .Lpublic\n.set .Lpublic,19\n');b=self.assemble()
        self.assertFalse(gate.compare(a,b)['checks']['symbols'])

    def test_symbol_order_ignored(self):
        a,b=copy.deepcopy(self.pairs[64]);b['symbols'].reverse()
        self.assertEqual(gate.compare(a,b)['status'],'PASS')

    def test_symbol_multiplicity_checked(self):
        self.rejected(lambda b:b['symbols'].append(copy.deepcopy(b['symbols'][0])), 'symbols')

    def test_section_relocation_target_canonical_name(self):
        for bits in (32,64):
            a=self.assemble(bits=bits)
            r=next(r for r in a['relocations'] if r['target'][0]=='.data')
            self.assertEqual(r['symbol'],'.text')
            b=copy.deepcopy(a)
            next(r for r in b['relocations'] if r['target'][0]=='.data')['symbol']='.bss'
            self.assertFalse(gate.compare(a,b)['checks']['relocations'])

    def group_pair(self):
        common=('.section .text.group,"axG",@progbits,group_signature,comdat\n'
                '.globl grouped_function\n.type grouped_function,@function\n'
                'grouped_function: ret\n.size grouped_function,.-grouped_function\n')
        a=self.assemble(common+'.section .debug_group,"G",@progbits,group_signature,comdat\n.long .text.group\n')
        b=self.assemble(common)
        return a,b

    def test_comdat_debug_only_member_difference_passes(self):
        a,b=self.group_pair()
        self.assertEqual(a['groups'],[dict(signature='group_signature',flags=1,members=['.text.group'])])
        self.assertEqual(gate.compare(a,b)['status'],'PASS')

    def test_comdat_member_difference_fails(self):
        a,b=self.group_pair();b['groups'][0]['members'].append('.data')
        self.assertFalse(gate.compare(a,b)['checks']['groups'])

    def test_comdat_signature_flags_and_member_order(self):
        for field,value in [('signature','other'),('flags',0),('members',['.other','.text.group'])]:
            with self.subTest(field=field):
                a,b=self.group_pair();b['groups'][0][field]=value
                self.assertFalse(gate.compare(a,b)['checks']['groups'])
        a,b=self.group_pair()
        a['groups'][0]['members']=['.one','.two'];b['groups'][0]['members']=['.two','.one']
        self.assertFalse(gate.compare(a,b)['checks']['groups'])

    def test_comdat_multiset(self):
        a,b=self.group_pair();other=dict(signature='other',flags=1,members=['.data'])
        a['groups'].append(other);b['groups'].insert(0,other)
        self.assertEqual(gate.compare(a,b)['status'],'PASS')
        b['groups'].append(copy.deepcopy(other))
        self.assertFalse(gate.compare(a,b)['checks']['groups'])

    def test_actual_release_debug_section_fails(self):
        a=self.assemble();b=self.assemble('.section .debug_unexpected,"",@progbits\n.byte 0\n')
        self.assertFalse(gate.compare(a,b)['checks']['release_no_debug'])

    def test_release_debug_sections_rejected(self):
        self.rejected(lambda b:b['debug_sections'].append('.debug_info'), 'release_no_debug')

    def test_rel_implicit_addend_bytes(self):
        a,b = copy.deepcopy(self.pairs[32]); b['alloc'][0]['content'] = b'changed'
        self.assertFalse(gate.compare(a,b)['checks']['alloc'])

    def test_truncated_elf_rejected(self):
        with self.assertRaises(ValueError): gate.parse(b'\x7fELF')


if __name__ == '__main__':
    unittest.main(verbosity=2)
