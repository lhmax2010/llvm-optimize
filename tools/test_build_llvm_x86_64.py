#!/usr/bin/env python3
"""Offline gate regression tests. Never starts GBS or compiles LLVM."""
import json
import copy
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
    @staticmethod
    def profile():
        return json.loads(b.BASELINE_PROFILE.read_text())

    def test_resource_thresholds(self):
        configuration = self.profile()['configuration']
        for memory, disk in ((16*b.GIB-1, 60*b.GIB), (16*b.GIB, 60*b.GIB-1)):
            with self.assertRaises(RuntimeError):
                b.resource_plan(memory, disk, 20, configuration)

    def test_measured_configuration_is_admitted_without_summing_peaks(self):
        for available in (16, 18, 23, 30, 64):
            plan = b.resource_plan(available*b.GIB, 60*b.GIB, 20, self.profile()['configuration'])
            self.assertEqual(plan['admission'], 'MEASURED_BASELINE')
            self.assertEqual(plan['memory_max_gib'], 18)
            self.assertEqual([plan[k] for k in ('gbs_threads','ninja_jobs','compile_jobs','link_jobs','debuginfo_jobs')],
                             [1,4,4,1,4])

    def test_heterogeneous_configuration_is_refused(self):
        for key, value in [('source_head','another-commit'), ('normalized_spec_sha256','instrumented-recipe'),
                           ('gbs_config_sha256','different-repositories'), ('buildconf_sha256','different-macros'),
                           ('repository_metadata',{'repo.base-standard':'changed-package-set'}),
                           ('arch','aarch64'), ('ninja_jobs',8), ('compile_jobs',8), ('link_jobs',2),
                           ('gbs_threads',2), ('debuginfo_jobs',40), ('LLVM_BUILD_INSTRUMENTED','IR')]:
            with self.subTest(key=key):
                candidate = copy.deepcopy(self.profile()['configuration'])
                candidate[key] = value
                with self.assertRaisesRegex(RuntimeError, 'capacity evidence does not cover'):
                    b.resource_plan(64*b.GIB, 100*b.GIB, 20, candidate)

    def test_recipe_identity_detects_pgo_and_configuration_changes(self):
        spec = (b.WORKSPACE/'llvm'/b.SPEC).read_text()
        def identity(s): return b.configuration_identity(b.EXPECTED_HEAD, s, b'config', b'buildconf')
        baseline = identity(spec)
        instrumented = identity(spec+'\n# hypothetical variant\n%define pgo -DLLVM_BUILD_INSTRUMENTED=IR\n')
        self.assertNotEqual(baseline['normalized_spec_sha256'],instrumented['normalized_spec_sha256'])
        changed = b.changed_concurrency(spec, dict(ninja_jobs=8,compile_jobs=8,link_jobs=2))
        self.assertEqual(baseline['normalized_spec_sha256'],identity(changed)['normalized_spec_sha256'])
        self.assertEqual([identity(changed)[k] for k in ('ninja_jobs','compile_jobs','link_jobs')],[8,8,2])

    def test_entire_cmake_contract_including_pgo_is_checked(self):
        parameters = self.profile()['cmake_parameters']
        def cache(values): return ''.join(f'{k}:STRING={v}\n' for k,v in values.items())
        self.assertEqual(b.validate_cache(cache(parameters), parameters)[1], [])
        for key in parameters:
            changed = dict(parameters)
            changed[key] += '-DIFFERENT'
            with self.subTest(key=key):
                self.assertTrue(b.validate_cache(cache(changed), parameters)[1])
        for key, value in [('LLVM_BUILD_INSTRUMENTED','IR'),('LLVM_PROFDATA_FILE','/tmp/new.profdata'),
                           ('LLVM_ENABLE_BOLT','ON'),('CMAKE_CXX_FLAGS','-O3 -fprofile-instr-generate')]:
            changed = dict(parameters); changed[key] = value
            self.assertTrue(b.validate_cache(cache(changed), parameters)[1])
        changed = dict(parameters)
        for key in ('CMAKE_C_COMPILER','CMAKE_CXX_COMPILER'):
            changed[key] = '/bin/'+changed[key]
        self.assertEqual(b.validate_cache(cache(changed), parameters)[1], [])

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
