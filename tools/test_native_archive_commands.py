#!/usr/bin/env python3
import json
from pathlib import Path
import sys
import tempfile
import unittest
from native_archive_commands import bounded_argv, MeasuredCommands


class ResourcePolicyTests(unittest.TestCase):
    def test_compile_limit_does_not_leak_to_link(self):
        self.assertIn('--as=4294967296', bounded_argv(['clang','-c','x.cpp'],'t','compile'))
        self.assertFalse(any(x.startswith('--as') for x in bounded_argv(['ld.lld','x.o'],'t','link')))
        self.assertIn('--core=0', bounded_argv(['ld.lld','x.o'],'t','link'))
        with self.assertRaises(ValueError):
            bounded_argv(['true'],'t','unknown')

    def test_actual_limits_and_monitor_cleanup(self):
        with tempfile.TemporaryDirectory() as name:
            root=Path(name)
            for phase,expected in [('compile',4294967296),('link',-1)]:
                out=root/(phase+'.txt')
                with out.open('wb') as stream:
                    record=MeasuredCommands().run([sys.executable,'-c',
                        'import resource,time; print(resource.getrlimit(resource.RLIMIT_AS)[0]); time.sleep(.12)'],
                        root/phase,stdout=stream,phase=phase)
                self.assertEqual(int(out.read_text()),expected)
                self.assertTrue(record['sampler_reaped'])
                self.assertGreater(record['sample_count'],0)
                self.assertFalse(record['sample_errors'])

    def test_failure_stops_following_commands(self):
        with tempfile.TemporaryDirectory() as name:
            runner=MeasuredCommands()
            with self.assertRaises(RuntimeError):
                runner.run(['/bin/false'],Path(name)/'fail',phase='run')
            with self.assertRaises(RuntimeError):
                runner.run(['/bin/true'],Path(name)/'later',phase='run')
            self.assertTrue(json.loads((Path(name)/'fail.json').read_text())['sampler_reaped'])


if __name__=='__main__':unittest.main(verbosity=2)
