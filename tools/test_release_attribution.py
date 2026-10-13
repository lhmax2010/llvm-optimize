#!/usr/bin/env python3
import copy
import unittest
import check_release_attribution as gate
from test_release_debug_independence import fixture,section

class Parameters(unittest.TestCase):
    def pair(self):
        common=dict(compiler_sha256='fixed-compiler-sha',cwd='/fixed/cwd',environment_identity={'inherited_parent':'fixture'})
        return ({**common,'argv':['clang','-O3','-g','-gdwarf-4','-c','debug.bc','-o','debug.o'],'path_map':{'debug.bc':'<INPUT>','debug.o':'<OUTPUT>'}},
                {**common,'argv':['clang','-O3','-c','release.bc','-o','release.o'],'path_map':{'release.bc':'<INPUT>','release.o':'<OUTPUT>'}})
    def test_only_debug_options_pass(self):self.assertEqual(gate.parameter_gate(*self.pair())['status'],'PASS')
    def test_extra_non_debug_fails(self):
        d,r=self.pair();r['argv'].insert(1,'-fPIC');self.assertEqual(gate.parameter_gate(d,r)['status'],'FAIL')
    def test_missing_non_debug_fails(self):
        d,r=self.pair();r['argv'].remove('-O3');self.assertEqual(gate.parameter_gate(d,r)['status'],'FAIL')
    def test_changed_non_debug_fails(self):
        d,r=self.pair();r['argv'][1]='-O2';self.assertEqual(gate.parameter_gate(d,r)['status'],'FAIL')
    def test_non_debug_order_fails(self):
        d,r=self.pair();r['argv'][1:3]=r['argv'][1:3][::-1];self.assertEqual(gate.parameter_gate(d,r)['status'],'FAIL')
    def test_compiler_sha_fails(self):
        d,r=self.pair();r['compiler_sha256']='another';self.assertFalse(gate.parameter_gate(d,r)['checks']['compiler_sha'])
    def test_environment_fails(self):
        d,r=self.pair();r['environment_identity']={'changed':'yes'};self.assertFalse(gate.parameter_gate(d,r)['checks']['environment'])
    def test_cwd_fails(self):
        d,r=self.pair();r['cwd']='/different';self.assertFalse(gate.parameter_gate(d,r)['checks']['cwd'])
    def test_arbitrary_g_option_not_ignored(self):
        d,r=self.pair();d['argv'].insert(2,'-gline-tables-only');self.assertEqual(gate.parameter_gate(d,r)['status'],'FAIL')

class Attribution(unittest.TestCase):
    def pair(self):
        symbols=[dict(id='f',type=2,section='text',size=4),dict(id='map',name='$t',binding=0,section='text')]
        a=fixture([section('text','.text.f',b'ABCD',flags=6),section('data')],symbols)
        symbols[0]['size']=3
        b=fixture([section('text','.text.f',b'ABC',flags=6),section('data')],symbols)
        return a,b
    def test_input_stage_a_pass(self):self.assertEqual(gate.attribution_gate(*self.pair(),{'f'})['status'],'PASS_ATTRIBUTED')
    def test_backend_stage_b_pass(self):
        a,b=self.pair();self.assertEqual(gate.attribution_gate(a,b,set(),copy.deepcopy(b))['status'],'PASS_ATTRIBUTED')
    def test_outside_function_difference_fails(self):
        a,b=self.pair();b['alloc'][1]['content']=b'other';self.assertEqual(gate.attribution_gate(a,b,{'f'})['status'],'FAIL')
    def test_neither_a_nor_b_fails(self):
        a,b=self.pair();self.assertEqual(gate.attribution_gate(a,b,set(),a)['status'],'FAIL')
    def test_function_binding_change_fails(self):
        a,b=self.pair();b['symbols'][0]['binding']=2;self.assertEqual(gate.attribution_gate(a,b,{'f'})['status'],'FAIL')
    def test_mapping_in_other_section_fails(self):
        a,b=self.pair();b['symbols'].append(dict(name='$d',type=0,binding=0,visibility=0,section=['.data',1,'',None],value=1,size=0))
        self.assertEqual(gate.attribution_gate(a,b,{'f'})['status'],'FAIL')
    def test_llvm_diff_function_marker(self):
        self.assertTrue(gate.llvm_diff_changed_function('f',1,'in function f:\n > changed\n'))
        self.assertFalse(gate.llvm_diff_changed_function('f',0,''))
        with self.assertRaises(ValueError):gate.llvm_diff_changed_function('f',1,'error: invalid bitcode')
        with self.assertRaises(ValueError):gate.llvm_diff_changed_function('f',0,'No function named @f in either module')
        with self.assertRaises(ValueError):gate.llvm_diff_changed_function('f',1,'in function other:\n')

if __name__=='__main__':unittest.main(verbosity=2)
