#!/usr/bin/env python3
"""Exact archive-fix admission and bundled Source tests; never runs GBS."""
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_llvm_x86_64 as b
import convert_static_archives as original
import llvm_static_archives_source as source


class ArchiveTrialTests(unittest.TestCase):
    def test_exact_opt_in_and_no_leak_to_other_configurations(self):
        config=json.loads(b.ARCHIVE_PROFILE.read_text())['configuration']
        plan=b.resource_plan(24*b.GIB,100*b.GIB,20,config,certify_fingerprint='archive-fix-trial')
        self.assertEqual(plan['memory_max_gib'],18)
        self.assertEqual(plan['admission'],'CERTIFICATION_ARCHIVE_FIX_TRIAL')
        with self.assertRaises(RuntimeError):b.resource_plan(24*b.GIB,100*b.GIB,20,config)
        with self.assertRaises(RuntimeError):b.resource_plan(24*b.GIB,100*b.GIB,20,config,certify_fingerprint='hybrid-trial')
        for key in config:
            changed=copy.deepcopy(config);changed[key]='different'
            with self.subTest(key=key),self.assertRaises(RuntimeError):
                b.resource_plan(24*b.GIB,100*b.GIB,20,changed,certify_fingerprint='archive-fix-trial')
        with self.assertRaises(RuntimeError):
            b.resource_plan(15*b.GIB,100*b.GIB,20,config,certify_fingerprint='archive-fix-trial')

    def test_cmake_contract_is_exact_baseline(self):
        profile=json.loads(b.ARCHIVE_PROFILE.read_text())
        baseline=json.loads(b.BASELINE_PROFILE.read_text())
        self.assertEqual(profile['cmake_parameters'],baseline['cmake_parameters'])
        for key,value in baseline['configuration'].items():
            if key!='normalized_spec_sha256':self.assertEqual(profile['configuration'][key],value)
        parameters=profile['cmake_parameters']
        cache=lambda p: ''.join(f'{k}:STRING={v}\n' for k,v in p.items())
        self.assertFalse(b.validate_cache(cache(parameters),parameters,certify_fingerprint='archive-fix-trial')[1])
        for key in parameters:
            wrong=dict(parameters);wrong[key]+='-wrong'
            with self.subTest(key=key):
                self.assertTrue(b.validate_cache(cache(wrong),parameters,certify_fingerprint='archive-fix-trial')[1])

    def test_real_trial_and_wrong_path(self):
        found=b.archive_trial_source_identity(b.WORKSPACE/'temp/llvm-archivefix-trial')
        self.assertEqual(found['trial'],'archive-fix-trial')
        with self.assertRaises(RuntimeError):b.archive_trial_source_identity(b.WORKSPACE/'llvm')

    def test_wrong_head_branch_inventory_and_diff(self):
        path=b.WORKSPACE/'temp/llvm-archivefix-trial'
        expected=json.loads(b.ARCHIVE_PROFILE.read_text())['configuration']
        status=b' M packaging/llvm.spec\n A packaging/llvm-static-archives-native.py\n'
        cases=[[b'wrong\n'],[b.EXPECTED_HEAD.encode(),b'main\n'],
               [b.EXPECTED_HEAD.encode(),b'archive-fix-trial\n',b' M unrelated.cpp\n'],
               [b.EXPECTED_HEAD.encode(),b'archive-fix-trial\n',status,b'wrong diff']]
        for outputs in cases:
            with self.subTest(outputs=outputs),patch.object(b.sp,'check_output',side_effect=outputs),self.assertRaises(RuntimeError):
                b.archive_trial_source_identity(path)

    def test_spec_and_source_hash_changes_rejected(self):
        read=Path.read_bytes
        for name in ('llvm.spec','llvm-static-archives-native.py'):
            def altered(path):return b'changed' if path.name==name else read(path)
            with self.subTest(name=name),patch.object(Path,'read_bytes',altered),self.assertRaises(RuntimeError):
                b.archive_trial_source_identity(b.WORKSPACE/'temp/llvm-archivefix-trial')

    def test_root_lock_is_only_existing_entry(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,'WORKSPACE',Path(tmp)):
            root=Path(tmp)/'temp/gbs-root-x86_64-archivefix';root.mkdir(parents=True)
            lock=root/'.llvm-optimize-exclusive.lock'
            data=dict(session='test-session',pid=os.getpid(),root=str(root))
            lock.write_text(json.dumps(data))
            self.assertEqual(b.archive_trial_root(root,'test-session'),data)
            with self.assertRaises(RuntimeError):b.archive_trial_root(root,'other')
            (root/'foreign').touch()
            with self.assertRaises(RuntimeError):b.archive_trial_root(root,'test-session')

    def test_source_embeds_the_same_certified_conversion_logic(self):
        self.assertEqual(source.BACKEND_FLAGS,original.BACKEND_FLAGS)
        def definitions(path):
            return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(Path(path).read_text()).body
                    if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
        src=definitions(source.__file__);orig=definitions(original.__file__)
        for name in ('sha','ir_settings','pic_relocations','Commands','convert'):
            self.assertEqual(src[name],orig[name],name)
        trial=b.WORKSPACE/'temp/llvm-archivefix-trial/packaging/llvm-static-archives-native.py'
        self.assertEqual(Path(source.__file__).read_bytes(),trial.read_bytes())


if __name__=='__main__':unittest.main(verbosity=2)
