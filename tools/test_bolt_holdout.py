#!/usr/bin/env python3
"""Keep failed calibration diagnostics separate from qualified formal results."""
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest

import measure_bolt_holdout as holdout


class HoldoutChecks(unittest.TestCase):
    def fixture(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        directory = Path(temporary.name)
        result = dict(status='MEASURED', protocol_hash='fixed', fixture_hash='fixed',
                      toolchains={'fixed':'identities'}, start_time='fixture', results={})
        # Known decomposition: stripped/RPM=0.5; BOLT/stripped=0.5; total=0.25.
        for name, value in zip(holdout.BINARIES, [4, 2, 1]):
            result['results'][name] = {case: dict(summary=dict(statistics=dict(wall_s=dict(median=value))))
                                       for case in ('A','real_example','ld.lld','llvm-ar')}
        holdout.bench.save(directory/'calibration.json', dict(status='FAIL',noise_floor_pct=5))
        for number in (1,2):
            holdout.bench.save(directory/f'calibration-run{number}.json', result)
        return directory, result

    def test_failed_calibration_cannot_produce_formal_summary(self):
        directory, _ = self.fixture()
        with self.assertRaises(RuntimeError):
            holdout.summarize(directory)
        self.assertFalse((directory/'comparison.json').exists())

    def test_diagnostics_remain_unqualified_and_decompose_correctly(self):
        directory, _ = self.fixture()
        with contextlib.redirect_stdout(io.StringIO()):
            holdout.summarize(directory, calibration_only=True)
        result = json.loads((directory/'calibration-comparison.json').read_text())
        self.assertEqual(result['status'],'UNCALIBRATED_DIAGNOSTIC')
        self.assertEqual(result['calibration_status'],'FAIL')
        self.assertFalse(result['formal_result'])
        for row in result['rounds']:
            self.assertEqual(row['geometric_means']['compile'],dict(
                bolt_over_stripped=.5,stripped_over_rpm=.5,bolt_over_rpm=.25))
        self.assertFalse((directory/'formal.json').exists())

    def test_incomplete_or_changed_inputs_are_refused_even_for_diagnostics(self):
        directory, original = self.fixture()
        for change in (dict(status='RUNNING'),dict(fixture_hash='changed')):
            result = copy.deepcopy(original);result.update(change)
            holdout.bench.save(directory/'calibration-run2.json',result)
            with self.assertRaises(RuntimeError):
                holdout.summarize(directory,calibration_only=True)


if __name__ == '__main__':
    unittest.main()
