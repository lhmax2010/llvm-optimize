#!/usr/bin/env python3
"""Offline gate regression tests. Never starts GBS or compiles LLVM."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import build_llvm_x86_64 as b


class BuildGates(unittest.TestCase):
    def test_resource_thresholds(self):
        for memory, disk in ((16*b.GIB-1, 60*b.GIB), (16*b.GIB, 60*b.GIB-1)):
            with self.assertRaises(RuntimeError):
                b.resource_plan(memory, disk, 20)
        # The observed large link cannot be safely budgeted under the approved cap.
        for memory in (16, 17, 22, 23, 28, 30, 64):
            with self.assertRaisesRegex(RuntimeError, 'full build refused'):
                b.resource_plan(memory*b.GIB, 60*b.GIB, 20)
        # Exercise arithmetic for a hypothetical future approved capacity, without
        # raising the production cap or launching any process.
        with patch.object(b, 'MAX_BUILD_MEMORY_GIB', 32):
            plan = b.resource_plan(64*b.GIB, 60*b.GIB, 20)
        self.assertLess(plan['link_jobs'] * b.LINK_ESTIMATE_GIB, 64 * .6)
        self.assertLessEqual(plan['link_jobs']*b.LINK_ESTIMATE_GIB + plan['compile_jobs']*2 + 2,
                             plan['memory_max_gib'])
        self.assertEqual(plan['gbs_threads'], 1)

    def test_only_concurrency_edits(self):
        spec = (b.WORKSPACE/'llvm'/b.SPEC).read_text()
        changed = b.changed_concurrency(spec, dict(ninja_jobs=4, compile_jobs=4, link_jobs=1))
        self.assertTrue(b.only_concurrency_changed(spec, changed))
        self.assertFalse(b.only_concurrency_changed(spec, changed.replace('-O3', '-O2')))
        self.assertFalse(b.only_concurrency_changed(spec, changed + '\n%define _toolchain clang\n'))

    @staticmethod
    def cache():
        return ('CMAKE_BUILD_TYPE:STRING=Release\nLLVM_ENABLE_LTO:STRING=Thin\n'
                'LLVM_USE_LINKER:STRING=lld\nLLVM_ENABLE_ASSERTIONS:BOOL=NO\n'
                'LLVM_LINK_LLVM_DYLIB:BOOL=OFF\nCLANG_LINK_CLANG_DYLIB:BOOL=OFF\n'
                'CMAKE_CXX_FLAGS:STRING=-g -O3 -flto=thin\n'
                'LLVM_TARGETS_TO_BUILD:STRING=X86;ARM;AArch64;BPF\n')

    def test_cache_accepts_rpm_no_boolean(self):
        self.assertEqual(b.validate_cache(self.cache())[1], [])

    def test_each_required_cache_setting_is_enforced(self):
        for old, new in (('Release', 'MinSizeRel'), ('=Thin', '=OFF'), ('=lld', '=bfd'),
                         ('ASSERTIONS:BOOL=NO', 'ASSERTIONS:BOOL=ON'),
                         ('LLVM_DYLIB:BOOL=OFF', 'LLVM_DYLIB:BOOL=ON'),
                         ('CLANG_DYLIB:BOOL=OFF', 'CLANG_DYLIB:BOOL=ON'),
                         ('-O3', '-Os'), ('-O3', '-O3 -Os'), ('X86;ARM;', 'X86;')):
            with self.subTest(old=old):
                self.assertTrue(b.validate_cache(self.cache().replace(old, new))[1])
        self.assertTrue(b.validate_cache('')[1])

    def test_sampler_cleanup_with_harmless_processes(self):
        """Exercise actual threads/processes; replace GBS BEFORE subprocess launch."""
        real_popen = subprocess.Popen
        for scenario in ('pass', 'bad_cache', 'low_memory', 'child_failure', 'deadline', 'interrupted',
                         'masked_failure', 'missing_status', 'rewritten_cache', 'held_completion'):
            with self.subTest(scenario=scenario), tempfile.TemporaryDirectory(
                    prefix='build-guard-test-', dir=b.WORKSPACE/'temp') as tmp:
                directory = Path(tmp)
                args = SimpleNamespace(config=directory/'unused.conf', source=directory/'unused-source',
                                       buildroot=directory/'root')
                cache = args.buildroot/'local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/CMakeCache.txt'
                contents = self.cache() + 'LLVM_PARALLEL_COMPILE_JOBS:STRING=1\nLLVM_PARALLEL_LINK_JOBS:STRING=1\n'
                if scenario == 'bad_cache':
                    contents = contents.replace('Release', 'MinSizeRel')
                code = ('from pathlib import Path; import time; '
                        f'p=Path({str(cache)!r}); p.parent.mkdir(parents=True); '
                        f'p.write_text({contents!r}); time.sleep(3); '
                        f'raise SystemExit({7 if scenario == "child_failure" else 0})')
                completion = directory/'rpm.exit'
                release = directory/'rpm.release'
                if scenario == 'masked_failure':
                    code = f'from pathlib import Path; Path({str(completion)!r}).write_text("7"); ' + code
                if scenario == 'rewritten_cache':
                    code = code.replace('time.sleep(3);',
                        f'time.sleep(3); p.write_text({contents.replace("Release", "MinSizeRel")!r}); time.sleep(3);')
                if scenario == 'held_completion':
                    code = ('from pathlib import Path\nimport time\n'
                            f'p=Path({str(cache)!r}); p.parent.mkdir(parents=True); p.write_text({contents!r})\n'
                            f'Path({str(completion)!r}).write_text("0")\n'
                            'for _ in range(100):\n'
                            f' if Path({str(release)!r}).exists(): break\n'
                            ' time.sleep(.05)\n'
                            'else: raise SystemExit(8)\n')
                launched = []

                def harmless_popen(command, **kwargs):
                    if command[0] != '/usr/bin/time':
                        return real_popen(command, **kwargs)
                    self.assertIn('gbs', command)
                    # The real executable is Python, never GBS (and no compiler).
                    command = [sys.executable, '-c', code]
                    launched.append(command)
                    audit.log('SIMULATION actual executable: ' + repr(command))
                    child = real_popen(command, **kwargs)
                    if scenario == 'interrupted':
                        real_wait = child.wait
                        interrupted = False

                        def wait_once(*positional, **keywords):
                            nonlocal interrupted
                            if not interrupted:
                                interrupted = True
                                raise KeyboardInterrupt('simulated signal')
                            return real_wait(*positional, **keywords)

                        child.wait = wait_once
                    return child

                audit = b.Audit(directory/'audit')
                plan = dict(memory_max_gib=1, compile_jobs=1, link_jobs=1)
                try:
                    with patch.object(b.sp, 'Popen', harmless_popen), patch.object(
                            b, 'mem_available', return_value=(1 if scenario == 'low_memory' else 20)*b.GIB), patch.object(
                            b, 'CONFIG_GATE_SECONDS', 0 if scenario == 'deadline' else 900):
                        if scenario in ('pass','held_completion'):
                            b.build(audit, args, plan, directory/'unused-buildconf', 'prlimit',
                                    completion_file=completion if scenario == 'held_completion' else None,
                                    release_file=release if scenario == 'held_completion' else None)
                            if scenario == 'held_completion':
                                self.assertTrue(release.exists())
                                self.assertTrue((audit.directory/'scope-after-rpm.json').exists())
                        elif scenario == 'interrupted':
                            with self.assertRaises(KeyboardInterrupt):
                                b.build(audit, args, plan, directory/'unused-buildconf', 'prlimit')
                        else:
                            with self.assertRaises(RuntimeError):
                                b.build(audit, args, plan, directory/'unused-buildconf', 'prlimit',
                                        completion_file=completion if scenario in ('masked_failure','missing_status') else None)
                    self.assertEqual(len(launched), 1)
                    outcome = json.loads((audit.directory/'outcome.json').read_text())
                    audit.log('SIMULATION outcome: ' + json.dumps(outcome))
                    self.assertTrue(outcome['sampler_reaped'])
                    self.assertTrue(outcome['log_reader_reaped'])
                    self.assertFalse(any(t.name == 'build-sampler' for t in threading.enumerate()))
                finally:
                    audit.stream.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
