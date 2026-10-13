#!/usr/bin/env python3
"""Release policy and POSIX native-launcher gates with literal expectations."""
import json
import os
from pathlib import Path
import signal
import tempfile
import unittest
from unittest import mock

import llvm_static_archives_source as production
import llvm_static_archives_arm_trial as trial
from test_static_archives_source_v2 import module
from test_archive_review_round3 import target_ir
from test_archive_review_round4 import native_header


def recorded(arch, debug):
    flags = ['clang', '-ffunction-sections', '-fdata-sections', '-flto=thin']
    if debug:
        flags += ['-g', '-gdwarf-4']
    if arch == 'x86_64':
        return flags + ['-O3']
    if arch == 'armv7l':
        return flags + ['--target=armv7l-tizen-linux-gnueabi', '-Os',
                        '-march=armv7-a', '-mthumb', '-mfpu=neon',
                        '-mfloat-abi=softfp', '-mlittle-endian']
    return flags + ['--target=aarch64-tizen-linux-gnu', '-O3',
                    '-march=armv8-a+fp+simd+crc+crypto', '-mtune=cortex-a53']


def text_ir(arch, flags, extra=''):
    if arch == 'x86_64':
        return module(extra, flags=flags)
    triple = 'thumbv7-tizen-linux-gnueabi' if arch == 'armv7l' else 'aarch64-tizen-linux-gnu'
    return ([f'target triple = "{triple}"', '!llvm.commandline = !{!9}',
             '!9 = !{!"'+' '.join(flags)+'"}'] + target_ir(arch) + extra.splitlines())


class ReleasePolicyTests(unittest.TestCase):
    def test_no_debug_all_architectures(self):
        for arch in ('x86_64', 'armv7l', 'aarch64'):
            modules = (production, trial) if arch == 'x86_64' else (trial,)
            for src in modules:
                with self.subTest(arch=arch, source=src.__name__):
                    row = (src.ir_settings(text_ir(arch, recorded(arch, False))) if arch == 'x86_64'
                           else src.arm_ir_settings(text_ir(arch, recorded(arch, False)), arch))
                    self.assertIsNone(row['policy']['dwarf'])
                    self.assertNotIn('-g', row['flags'])
                    self.assertNotIn('-gdwarf-4', row['flags'])
                    self.assertIn('-ffunction-sections', row['flags'])
                    self.assertIn('-fdata-sections', row['flags'])

    def test_no_debug_ir_cu_is_rejected(self):
        for arch in ('x86_64', 'armv7l', 'aarch64'):
            for src in ((production, trial) if arch == 'x86_64' else (trial,)):
                lines = text_ir(arch, recorded(arch, False), '!llvm.dbg.cu = !{!10}')
                with self.subTest(arch=arch), self.assertRaisesRegex(ValueError, 'no-debug command has !llvm.dbg.cu'):
                    src.ir_settings(lines) if arch == 'x86_64' else src.arm_ir_settings(lines, arch)

    def test_partial_or_uncertified_debug_is_rejected(self):
        for arch in ('x86_64', 'armv7l', 'aarch64'):
            for tokens in (['-g'], ['-g0'], ['-ggdb'], ['-gdwarf-5'], ['-g', '-gdwarf-5']):
                for src in ((production, trial) if arch == 'x86_64' else (trial,)):
                    with self.subTest(arch=arch, tokens=tokens), self.assertRaises(ValueError):
                        flags = recorded(arch, False) + tokens
                        src.classify_options(flags) if arch == 'x86_64' else src.arm_classify_options(flags, arch)

    def test_debug_backend_exact_literal(self):
        for arch, triple, opt, extra in (
            ('x86_64', 'x86_64-tizen-linux-gnu', '-O3', []),
            ('armv7l', 'thumbv7-tizen-linux-gnueabi', '-Os', ['-mfloat-abi=softfp', '-mlittle-endian', '-mthumb']),
            ('aarch64', 'aarch64-tizen-linux-gnu', '-O3', [])):
            want = ['--no-default-config', '--target='+triple, '-x', 'ir', opt,
                    '-ffunction-sections', '-fdata-sections', '-funique-section-names',
                    '-faddrsig', '-g', '-gdwarf-4', '-ffp-contract=on', '-c',
                    '-fno-pic', '-fno-pie'] + extra
            for src in ((production, trial) if arch == 'x86_64' else (trial,)):
                lines = text_ir(arch, recorded(arch, True))
                got = src.ir_settings(lines) if arch == 'x86_64' else src.arm_ir_settings(lines, arch)
                self.assertEqual(got['flags'], want)

    def test_debug_like_operand_is_not_a_debug_option(self):
        for src in (production, trial):
            row = src.classify_options(recorded('x86_64', False)+['-I', '/headers/-gdwarf-5'])
            self.assertIsNone(row['dwarf'])


def native_shells():
    if Path('/emul/usr/bin/sh').exists():
        # Root tests exercise every installed native implementation; no ARM shell
        # is substituted for a missing /emul implementation.
        return [Path('/emul/usr/bin')/name for name in ('bash', 'dash', 'sh')
                if (Path('/emul/usr/bin')/name).exists()]
    return [Path('/bin/bash'), Path('/bin/dash'), Path('/bin/sh')]


class PosixLauncherTests(unittest.TestCase):
    def test_three_shell_limits_core_and_identity(self):
        for shell in native_shells():
            with self.subTest(shell=shell), tempfile.TemporaryDirectory() as tmp:
                command = trial.ARMNativeLimitCommands(trial.Commands(), shell, [shell])
                row = trial.arm_address_space_probe(command, Path(tmp))
                self.assertEqual((row['soft'], row['hard']), ('4294967296', '4294967296'))
                self.assertRegex(row['raw'], r'Max core file size\s+0\s+0\s+bytes')
                self.assertEqual(command.shell_identity['program'], shell.resolve().name)
                self.assertEqual(command.shell_identity['sha256'], production.sha(shell.resolve()))

    def test_three_shell_quoted_argv_and_env_are_not_executed(self):
        for shell in native_shells():
            with self.subTest(shell=shell), tempfile.TemporaryDirectory() as tmp:
                p = Path(tmp); env = p/'env'; marker = p/'BAD'; out = p/'stdout'
                env.write_text('printf unsafe > "'+str(marker)+'"\n')
                command = trial.ARMNativeLimitCommands(trial.Commands(), shell, [shell])
                values = ['space here', 'single\'quote', 'double"quote', '$HOME', '$(false)', '']
                with mock.patch.dict(os.environ, {'BASH_ENV': str(env), 'ENV': str(env)}), out.open('wb') as stream:
                    row = command.run([shell, '-c', 'printf "<%s>\\n" "$@"', 'payload', *values], p/'argv', stdout=stream)
                self.assertFalse(marker.exists())
                self.assertEqual(out.read_text(), '<space here>\n<single\'quote>\n<double"quote>\n<$HOME>\n<$(false)>\n<>\n')
                self.assertEqual(row['argv'][:5], ['/usr/bin/env', '-u', 'BASH_ENV', '-u', 'ENV'])
                self.assertNotIn('--noprofile', row['argv'])
                self.assertNotIn('--norc', row['argv'])

    def test_three_shell_limit_failure_125(self):
        for shell in native_shells():
            with self.subTest(shell=shell), tempfile.TemporaryDirectory() as tmp:
                command = trial.ARMNativeLimitCommands(trial.Commands(), shell, [shell]); p = Path(tmp)
                script = 'ulimit -v 65536 || exit 99\n'+trial.ARM_NATIVE_LIMIT_EXEC
                with mock.patch.object(trial, 'ARM_NATIVE_LIMIT_EXEC', script), self.assertRaisesRegex(RuntimeError, r'\(125\)'):
                    command.run([shell, '-c', 'exit 0'], p/'fail')
                self.assertEqual(json.loads((p/'fail.json').read_text())['exit'], 125)

    def test_unsupported_ulimit_and_readback_mismatch_125(self):
        for shell in native_shells():
            for script in ('ulimit -! 1 || exit 125\n',
                           trial.ARM_NATIVE_LIMIT_EXEC.replace('hard=$(ulimit -H -v)', 'hard=1')):
                with self.subTest(shell=shell, script=script), tempfile.TemporaryDirectory() as tmp:
                    command = trial.ARMNativeLimitCommands(trial.Commands(), shell, [shell]); p = Path(tmp)
                    with mock.patch.object(trial, 'ARM_NATIVE_LIMIT_EXEC', script), self.assertRaisesRegex(RuntimeError, r'\(125\)'):
                        command.run([shell, '-c', 'exit 0'], p/'fail')
                    self.assertEqual(json.loads((p/'fail.json').read_text())['exit'], 125)

    def test_three_shell_timeout_sigkill_cleanup(self):
        for shell in native_shells():
            with self.subTest(shell=shell), tempfile.TemporaryDirectory() as tmp:
                p = Path(tmp); ready = p/'ready'
                command = trial.ARMNativeLimitCommands(trial.Commands(timeout=5), shell, [shell])
                with self.assertRaisesRegex(RuntimeError, 'timeout'):
                    command.run([shell, '-c', 'trap "" TERM; printf ready > "$1"; while :; do :; done', 'fixture', str(ready)], p/'timeout')
                self.assertTrue(ready.is_file())
                row = json.loads((p/'timeout.json').read_text())
                self.assertEqual(row['exit'], -signal.SIGKILL)
                self.assertGreaterEqual(row['wall'], 8)
                self.assertFalse(command.children)

    def test_missing_nonexecutable_and_wrong_arch_shell_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/'shell'; native = native_shells()[0]
            for blob, mode in ((None, None), (native_header(), 0o644), (native_header(183), 0o755)):
                if blob is not None:
                    p.write_bytes(blob); p.chmod(mode)
                with self.assertRaises(ValueError):
                    trial.ARMNativeLimitCommands(trial.Commands(), p, [native])


class MinorVersionTests(unittest.TestCase):
    def test_22_1_9_with_matching_tools_is_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp); (p/'CMakeCache.txt').touch()
            tools = [p/name for name in ('clang-22', 'llvm-dis', 'llvm-nm')]
            for tool in tools:
                tool.write_bytes(native_header()); tool.chmod(0o755)
            command = mock.Mock(); command.address_space_bytes = 4294967296
            def run(argv, prefix, stdout):
                if argv == ['/usr/bin/cat', '/proc/self/limits']:
                    stdout.write(b'Max address space 4294967296 4294967296 bytes   \n')
                else:
                    stdout.write(b'clang version 22.1.9\n' if argv[0] == tools[0] else b'LLVM version 22.1.9\n')
            command.run.side_effect = run
            row = trial.validate_arm_tools(p, *tools, command, p, 'aarch64')
            self.assertEqual(row['arm_full_version'], '22.1.9')
            self.assertEqual(row['tool_versions']['compiler']['resolved_path'], str(tools[0].resolve()))

    def test_feature_mismatch_names_recensus(self):
        for arch in ('armv7l', 'aarch64'):
            lines = [line.replace('target-features"="', 'target-features"="+uncertified,') for line in target_ir(arch)]
            with self.assertRaisesRegex(ValueError, '需按升级手册重做 docs/44 §2 普查'):
                trial.arm_function_targets(lines, arch)


if __name__ == '__main__':
    unittest.main(verbosity=2)
