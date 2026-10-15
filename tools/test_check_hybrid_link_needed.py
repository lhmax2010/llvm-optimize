#!/usr/bin/env python3
"""Tests use synthetic headers/mocked readelf; no toolchain build or execution."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import check_hybrid_link_needed as c

D = Path(__file__).resolve().parents[1] / 'docs/52_hybrid_link_evidence'

class ExpectationsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.table = {'aliases': {'clang++': 'clang-22'}, 'targets': [
            {'build_output': 'bin/clang-22', 'category': c.CATEGORIES[0],
             'install_paths': ['/usr/bin/clang-22', '/usr/bin/clang++'],
             'expected_needed': {'libLLVM': False, 'libclang-cpp': False}},
            {'build_output': 'bin/clang-tidy', 'category': c.CATEGORIES[4],
             'install_paths': ['/usr/bin/clang-tidy'],
             'expected_needed': {'libLLVM': True, 'libclang-cpp': True}}]}

    def elf(self, name):
        p = self.root / name.lstrip('/')
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b'\x7fELFsynthetic')
        return p

    def test_all_188_graph_targets(self):
        table = json.loads((D / 'needed-expectations-v2.json').read_text())
        result = c.self_check(table, D/'a-all-link-targets.json', D/'aliases.json', D/'rpm-install-paths.txt')
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(sum(table['categories'].values()), 188)
        self.assertFalse(result['missing_targets'])

    def test_table_tampering_rejected(self):
        table = json.loads((D / 'needed-expectations-v2.json').read_text())
        table['targets'].pop()
        with self.assertRaisesRegex(ValueError, 'differs'):
            c.self_check(table, D/'a-all-link-targets.json', D/'aliases.json', D/'rpm-install-paths.txt')

    def test_sdk_copy_matches_install_glob(self):
        table = json.loads((D/'needed-expectations-v2.json').read_text())
        rows = {r['build_output']:r for r in table['targets']}
        self.assertIn('/home/owner/share/tmp/sdk_tools/lldb/lib64/liblldb.so.22.1.8',
                      rows['lib64/liblldb.so.22.1.8']['install_paths'])
        self.assertEqual(rows['lib64/liblldbIntelFeatures.so.22.1']['install_paths'],
                         ['/usr/lib64/liblldbIntelFeatures.so.22.1'])

    def test_five_categories(self):
        cases = [('bin/clang-22',False,False,0), ('bin/llvm-config',False,False,1),
                 ('bin/obj2yaml',False,False,2), ('bin/opt',True,False,3),
                 ('bin/clang-tidy',True,True,4)]
        for output, llvm, clang, index in cases:
            self.assertEqual(c.category(output, {'libLLVM':llvm, 'libclang-cpp':clang}), c.CATEGORIES[index])

    def test_graph_conflicts_rejected(self):
        with self.assertRaises(ValueError):
            c.category('bin/clang-22', {'libLLVM':True, 'libclang-cpp':False})
        with self.assertRaises(ValueError):
            c.category('bin/unexpected', {'libLLVM':False, 'libclang-cpp':True})

    def test_static_and_neither_accept_libc(self):
        self.assertEqual(c.needed_status({'libLLVM':False,'libclang-cpp':False}, ['libc.so.6'])['status'], 'PASS')

    def test_dynamic_exact_pass(self):
        self.assertEqual(c.needed_status({'libLLVM':True,'libclang-cpp':True},
            ['libLLVM.so.22.1','libclang-cpp.so.22.1'])['status'], 'PASS')

    def test_as_needed_is_pending_not_pass(self):
        r = c.needed_status({'libLLVM':True,'libclang-cpp':True}, ['libclang-cpp.so.22.1'])
        self.assertEqual(r['status'], 'ANALYSIS_PENDING')
        self.assertEqual(r['missing_expected_shared'], ['libLLVM'])

    def test_unexpected_shared_fails(self):
        self.assertEqual(c.needed_status({'libLLVM':False,'libclang-cpp':False}, ['libLLVM.so.22.1'])['status'], 'FAIL')

    def test_unrelated_library_name_is_not_libllvm(self):
        self.assertEqual(c.needed_status({'libLLVM':False,'libclang-cpp':False}, ['libLLVMSupport.so'])['status'], 'PASS')

    def test_absolute_alias_resolved_inside_root(self):
        p = self.elf('/usr/bin/clang-22')
        (p.parent/'clang++').symlink_to('/usr/bin/clang-22')
        self.assertEqual(c.rooted_path(self.root,'/usr/bin/clang++'), p)
        self.assertEqual(c.find_target(self.table, '/usr/bin/clang++', p)['build_output'], 'bin/clang-22')

    def test_accel_expanded_alias(self):
        p = self.elf('/emul/usr/bin/clang++')
        self.assertEqual(c.find_target(self.table, '/emul/usr/bin/clang++',p)['build_output'], 'bin/clang-22')

    def test_loop_and_escape_rejected(self):
        (self.root/'loop').symlink_to('loop')
        (self.root/'escape').symlink_to('../outside')
        for name in ['loop','escape']:
            with self.assertRaises(ValueError):
                c.rooted_path(self.root, name)

    def test_unknown_elf_error(self):
        self.elf('/usr/bin/new-tool')
        r = c.inspect_paths(self.table,self.root,['/usr/bin/new-tool'])
        self.assertEqual(r['exit_code'], 2)
        self.assertIn('unmapped',r['results'][0]['error'])

    def test_known_non_elf_and_missing_file_error(self):
        p = self.elf('/usr/bin/clang-22')
        p.write_text('unexpected script')
        r = c.inspect_paths(self.table,self.root,['/usr/bin/clang-22','/usr/bin/clang-tidy'])
        self.assertEqual(r['counts'], {'ERROR':2})

    def test_known_target_cannot_be_directory(self):
        (self.root/'usr/bin/clang-22').mkdir(parents=True)
        r = c.inspect_paths(self.table,self.root,['/usr/bin/clang-22'])
        self.assertEqual(r['exit_code'],2)

    def test_pending_exit_code_and_readelf_capture(self):
        self.elf('/usr/bin/clang-tidy')
        with patch.object(c.subprocess, 'run', return_value=subprocess.CompletedProcess([],0,
                   ' 0x (NEEDED) Shared library: [libclang-cpp.so.22.1]\n','')) as run:
            r = c.inspect_paths(self.table,self.root,['/usr/bin/clang-tidy'])
        self.assertEqual(r['exit_code'],3)
        self.assertEqual(run.call_args.args[0][1],'-dW')
        self.assertIn('stdout', r['results'][0])

    def test_readelf_failure_propagates(self):
        self.elf('/usr/bin/clang-22')
        with patch.object(c.subprocess,'run',return_value=subprocess.CompletedProcess([],1,'','invalid ELF')):
            r = c.inspect_paths(self.table,self.root,['/usr/bin/clang-22'])
        self.assertEqual(r['exit_code'],2)
        self.assertEqual(r['results'][0]['stderr'],'invalid ELF')

    def test_empty_run_cannot_pass(self):
        self.assertEqual(c.inspect_paths(self.table,self.root,[])['exit_code'],2)

    def test_missing_declared_paths_error(self):
        r = c.inspect_paths(self.table,self.root,[],require_declared=True)
        self.assertEqual(r['counts'], {'ERROR':3})
        self.assertTrue(all('missing from input path list' in row['error'] for row in r['results']))

    def test_alias_cycle_rejected(self):
        with self.assertRaisesRegex(ValueError,'cycle'):
            c.canonical_alias('a',{'a':'b','b':'a'})

if __name__ == '__main__':
    unittest.main(verbosity=2)
