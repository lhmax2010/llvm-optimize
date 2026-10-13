#!/usr/bin/env python3
"""Offline tests; no GBS, filesystem cleanup, or shared-lock acquisition."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import run_certified_x86_release_build as trial


class RegisteredBuild(unittest.TestCase):
    def test_disk_rules(self):
        trial.disk_admission(trial.ADMISSION)
        for free in (trial.ADMISSION-1, trial.BUDGET+trial.FLOOR-1):
            with self.assertRaisesRegex(RuntimeError,'disk admission'):
                trial.disk_admission(free)

    def test_round2_exception_is_scoped_and_bounded(self):
        allowed = trial.ADMISSION-1
        self.assertTrue(trial.disk_admission(allowed,2)['pm_exception_used'])
        self.assertFalse(trial.disk_admission(trial.ADMISSION,2)['pm_exception_used'])
        self.assertTrue(trial.disk_admission(trial.ADMISSION-trial.guard.GIB,2)['pm_exception_used'])
        for round_number, free in [(1,allowed),(2,trial.ADMISSION-trial.guard.GIB-1),
                                    (2,trial.BUDGET+40*trial.guard.GIB-1)]:
            with self.assertRaisesRegex(RuntimeError,'disk admission'):
                trial.disk_admission(free,round_number)
        # Exercise independent 40 GiB floor even with a relaxed mock admission.
        with patch.object(trial,'ADMISSION',trial.BUDGET+40*trial.guard.GIB):
            with self.assertRaisesRegex(RuntimeError,'disk admission'):
                trial.disk_admission(trial.ADMISSION-1,2)

    def test_round2_marker_and_evidence_are_separate(self):
        first, first_marker=trial.run_paths(1)
        second, second_marker=trial.run_paths(2)
        self.assertNotEqual(first,second)
        self.assertNotEqual(first_marker,second_marker)
        self.assertEqual(first,trial.E)
        with self.assertRaises(ValueError):trial.run_paths(3)

    def test_exact_identity_and_fresh_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            w=Path(tmp); e=w/'e'; e.mkdir(); source=w/'source'; source.mkdir()
            (e/'repository-preflight').mkdir()
            (e/'repository-preflight/result.json').write_text('{"status":"PASS"}')
            for name in ('temp/.llvm-optimize-exclusive.lock',
                         'temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock'):
                p=w/name; p.parent.mkdir(parents=True,exist_ok=True)
                p.write_text(json.dumps(dict(session='release-x86-latest-base-20261013',pid=os.getpid())))
            file=source/'spec'; file.write_text('certified')
            with patch.multiple(trial,W=w,E=e,SOURCE=source,ROOT=w/'newroot',
                                HASHES={file:hashlib.sha256(b'certified').hexdigest()}), \
                 patch.object(trial.subprocess,'check_output',side_effect=lambda args,**kw: trial.HEAD if args[3]=='rev-parse' else ''):
                self.assertEqual(len(trial.verify_inputs()),1)
                file.write_text('changed')
                with self.assertRaisesRegex(RuntimeError,'unregistered input'):trial.verify_inputs()
                file.write_text('certified')
                with patch.object(trial.subprocess,'check_output',return_value='wrong'):
                    with self.assertRaisesRegex(RuntimeError,'HEAD/status'):trial.verify_inputs()
                (w/'newroot').mkdir()
                with self.assertRaisesRegex(RuntimeError,'fresh root'):trial.verify_inputs()


if __name__=='__main__':unittest.main()
