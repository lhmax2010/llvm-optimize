#!/usr/bin/env python3
"""Packaged Source resource accounting and limit tests; no LLVM build."""
import concurrent.futures
import json
from pathlib import Path
import sys
import tempfile
import unittest

import llvm_static_archives_source as source


class SourceCommandsTests(unittest.TestCase):
    def test_limits_accounting_and_no_external_time(self):
        with tempfile.TemporaryDirectory() as tmp:
            prefix = Path(tmp)/'limits'
            output = Path(tmp)/'stdout'
            with output.open('wb') as out:
                row = source.Commands().run([sys.executable, '-c',
                    'import resource,json; print(json.dumps([resource.getrlimit(resource.RLIMIT_AS),'
                    'resource.getrlimit(resource.RLIMIT_CORE)]))'], prefix, stdout=out)
            self.assertEqual(json.loads(output.read_text()), [[4*1024**3]*2, [0, 0]])
            self.assertNotIn('/usr/bin/time', row['bounded_argv'])
            self.assertGreater(row['max_rss_kib'], 0)
            self.assertGreater(row['wall'], 0)
            self.assertEqual(row['exit'], 0)

    def test_first_failure_cancels_and_reaps(self):
        with tempfile.TemporaryDirectory() as tmp:
            command = source.Commands()
            with self.assertRaises(RuntimeError):
                command.run([sys.executable, '-c', 'raise SystemExit(7)'], Path(tmp)/'fail')
            self.assertFalse(command.children)
            self.assertEqual(json.loads((Path(tmp)/'fail.json').read_text())['exit'], 7)
            with self.assertRaisesRegex(RuntimeError, 'cancelled'):
                command.run([sys.executable, '-c', 'pass'], Path(tmp)/'next')

    def test_wait4_is_per_child_under_four_workers(self):
        with tempfile.TemporaryDirectory() as tmp:
            command = source.Commands()
            def run(i):
                return command.run([sys.executable, '-c',
                    f'x=bytearray({(i+1)*16}*1024**2); sum(x)'], Path(tmp)/str(i))
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
                rows = list(pool.map(run, range(4)))
            self.assertTrue(all(row['exit'] == 0 for row in rows))
            self.assertGreater(rows[-1]['max_rss_kib'], rows[0]['max_rss_kib']+24*1024)
            self.assertFalse(command.children)


if __name__ == '__main__':
    unittest.main(verbosity=2)
