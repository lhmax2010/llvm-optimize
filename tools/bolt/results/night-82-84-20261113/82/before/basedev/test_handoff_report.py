"""Retained fixtures for the prep/build handoff and rehearsal report contract."""
from pathlib import Path
import ast
import json
import os
import re
import shutil
import time
import unittest

os.environ.setdefault('NIGHT_SOURCE_SHA', '7d5e28ca89ed68e3360765bc4e42234eaaabae27')
os.environ.setdefault('FINAL_PROJECT', 'basedev')
import launcher
from resource_report import report

class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(os.environ['REBASE_TEST_ROOT'])
        cls.root.mkdir(exist_ok=False)

    def test_prep_to_build_epoch_is_not_restart(self):
        for replace_inode in (False, True):
            with self.subTest(replace_inode=replace_inode):
                d = self.root / ('handoff-' + str(replace_inode))
                e = d / 'evidence'
                e.mkdir(parents=True)
                r = d / 'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
                r.mkdir(parents=True)
                p = r / '.build.log'
                old = b'PREP-ONLY\n' * 2200 + b'PREP-TAIL'
                p.write_bytes(old)
                launcher.materialize(d, dict(prep_unit='test-prep', build_unit='test-build', mode='full'))
                tree = ast.parse((d / 'run.py').read_text())
                funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ('log_epoch', 'logs')]
                self.assertEqual(len(funcs), 2)
                events = []
                chunks = [b'[ 0s] NEW BUILD\n', b'[ 1s] Executing(%build)\n', b'[ 2s] extra\n']
                copied = e / 'rpm-build.log'
                outer = self
                class Clock:
                    i = 0
                    def wait(self, delay):
                        self.i += 1
                        if self.i in (1, 2):
                            outer.assertFalse(copied.exists(), 'prep bytes copied')
                            return False
                        if self.i == 3:
                            outer.assertFalse(copied.exists(), 'prep bytes copied')
                            if replace_inode:
                                p.rename(r / 'prep-retained.log')
                            p.write_bytes(chunks[0])
                            return False
                        if self.i in (4, 5):
                            with p.open('ab') as f:
                                f.write(chunks[self.i - 3])
                            return False
                        outer.assertEqual(copied.read_bytes(), b''.join(chunks))
                        return True
                env = dict(R=r, E=e, stop=Clock(), reason=None, plan={'mode':'full'},
                           time=time, re=re, shutil=shutil,
                           append=lambda name,row: events.append((name,row)))
                exec(compile(ast.Module(body=funcs, type_ignores=[]), 'generated-run-functions', 'exec'), env)
                env['prep_log_epoch'] = env['log_epoch'](p)
                env['logs']()
                self.assertEqual([x for x in events if x[0]=='log-restarts.jsonl'], [])
                self.assertEqual(len([x for x in events if x[0]=='log-source-handoff.jsonl']), 1)
                self.assertEqual(copied.read_bytes(), p.read_bytes())
                (d / 'result.json').write_text(json.dumps(dict(
                    old_prep_bytes_copied=0, log_restarts=0,
                    copied_bytes=len(copied.read_bytes()), equals_original=True,
                    events=events), indent=2)+'\n')

    def test_rehearsal_report_only_uses_own_original_log(self):
        d = self.root / 'report'
        e = d / 'evidence'
        e.mkdir(parents=True)
        original = d / 'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/.build.log'
        original.parent.mkdir(parents=True)
        text = ('[ 0s] host started "build llvm.spec" at Fri Nov  6 07:10:50 UTC 2026.\n'
                '[ 2s] Executing(%build): /bin/sh\n'
                '[ 3s] + cmake -G Ninja test\n')
        original.write_text(text)
        (d / 'plan.json').write_text(json.dumps({'mode':'rehearsal'}))
        result = report(d)
        self.assertEqual(result['log_source']['path'], str(original))
        self.assertTrue((e / 'resource-table.md').exists())
        (d / 'plan.json').write_text(json.dumps({'mode':'full'}))
        with self.assertRaisesRegex(AssertionError, 'exactly one original successful GBS log required'):
            report(d)
        success = d / 'gbs-driver/local/repos/test/x86_64/logs/success/llvm-22.1.8/log.txt'
        success.parent.mkdir(parents=True)
        success.write_text(text)
        result = report(d)
        self.assertEqual(result['log_source']['path'], str(success))

if __name__ == '__main__':
    unittest.main(verbosity=2)
