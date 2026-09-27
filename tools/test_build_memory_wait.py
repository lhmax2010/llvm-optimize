#!/usr/bin/env python3
"""Frozen memory policy tests, fake time, never starts a build."""
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
import build_llvm_x86_64 as b


class MemoryWaitTests(unittest.TestCase):
    def run_policy(self, readings, limit=21600):
        state = {'now': 0, 'sleeps': [], 'messages': []}
        values = iter(readings)
        def sleep(n):
            state['sleeps'].append(n)
            state['now'] += n
        with tempfile.TemporaryDirectory() as tmp:
            audit = SimpleNamespace(directory=Path(tmp), log=state['messages'].append)
            try:
                state['result'] = b.wait_for_build_memory(audit, limit,
                    read=lambda: next(values), clock=lambda: state['now'], sleep=sleep)
            except RuntimeError as error:
                state['error'] = str(error)
            state['rows'] = [json.loads(x) for x in (Path(tmp)/'memory-admission.jsonl').read_text().splitlines()]
        return state

    def test_exact_threshold_immediate(self):
        s = self.run_policy([16*b.GIB])
        self.assertEqual(s['result'], 16*b.GIB)
        self.assertEqual(s['sleeps'], [])

    def test_poll_every_five_minutes_until_admitted(self):
        s = self.run_policy([16*b.GIB-1, 15*b.GIB, 17*b.GIB])
        self.assertEqual(s['sleeps'], [300, 300])
        self.assertEqual(s['result'], 17*b.GIB)
        self.assertEqual([r['admitted'] for r in s['rows']], [False, False, True])

    def test_six_hours_timeout_no_retry(self):
        s = self.run_policy([15*b.GIB]*73)
        self.assertEqual(sum(s['sleeps']), 21600)
        self.assertEqual(len(s['rows']), 73)
        self.assertIn('expired', s['error'])
        self.assertNotIn('result', s)


if __name__ == '__main__':
    unittest.main(verbosity=2)
