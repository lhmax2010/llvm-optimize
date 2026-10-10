#!/usr/bin/env python3
"""Review A-I regression tests, plus parameter/cleanup and Python 3.9 checks."""
import ast
import contextlib
import io
import json
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock

import llvm_static_archives_source as source
from test_inspect_llvm_archives import native

FLAGS = ['clang', '-O3', '-flto=thin', '-gdwarf-4', '-ffunction-sections', '-fdata-sections']


def module(extra='', flags=None):
    argv = FLAGS if flags is None else flags
    return ('target triple = "x86_64-tizen-linux-gnu"\n'
            '!llvm.commandline = !{!9}\n!9 = !{!"'+ ' '.join(argv)+'"}\n'+extra).splitlines(True)


class PolicyTests(unittest.TestCase):
    def test_a_classifies_operands_without_replaying_lto(self):
        flags = FLAGS+['-I', '/a', '-D', 'KEY=1', '-MT', 'out', '-MF', 'deps', '-o', 'x.o', '-c', '/a/a.cpp']
        row = source.classify_options(flags)
        self.assertEqual(len(row['tokens']), len(flags))
        self.assertEqual({x['category'] for x in row['tokens']}, {'ir','irrelevant','restore'})
        self.assertNotIn('-flto=thin', source.ir_settings(module(flags=flags))['flags'])

    def test_a_unknown_and_missing_operands_fail(self):
        for token in ('-mllvm', '-foo', '-fno-unroll-loops', '-march-native'):
            with self.subTest(token=token), self.assertRaisesRegex(ValueError, token):
                source.classify_options(FLAGS+[token])
        with self.assertRaisesRegex(ValueError, 'missing operand'):
            source.classify_options(FLAGS+['-I'])

    def test_b_last_values_and_defaults(self):
        row = source.classify_options(['clang','-O2','-gdwarf-5','-fno-function-sections', *FLAGS[1:],
                                      '-ffp-contract=off','-ffp-contract=on'])
        self.assertEqual(row['optimization'], '-O3')
        self.assertEqual(row['dwarf'], '-gdwarf-4')
        self.assertEqual(row['fp_contract'], 'on')
        self.assertTrue(row['switches']['unique-section-names'])
        self.assertTrue(row['switches']['addrsig'])
        self.assertNotIn('-O3', source.BACKEND_FLAGS)
        self.assertFalse(any(x.startswith('-ffp-contract=') for x in source.BACKEND_FLAGS))
        self.assertIn('-ffp-contract=off', source.ir_settings(module(flags=FLAGS+['-ffp-contract=off']))['flags'])

    def test_b_uncertified_last_values_fail(self):
        for token in ('-O2','-gdwarf-5','-fno-function-sections','-fno-data-sections',
                      '-fno-unique-section-names','-fno-addrsig','-ffp-contract=invalid'):
            with self.subTest(token=token), self.assertRaises(ValueError):
                source.classify_options(FLAGS+[token])

    def test_c_normal_ir_and_zero_split_lto_pass(self):
        source.ir_settings(module('!10 = !{i32 1, !"EnableSplitLTOUnit", i32 0}\n'))
        source.ir_settings(module('@message = constant [15 x i8] c"llvm.type.test\\00"\n'))

    def test_c_four_type_features_fail(self):
        for marker in ('declare i1 @llvm.type.test(ptr, metadata)',
                       'declare i1 @llvm.public.type.test(ptr, metadata)',
                       '@v = global ptr null, !vcall_visibility !11',
                       '!10 = !{i32 1, !"EnableSplitLTOUnit", i32 1}'):
            with self.subTest(marker=marker), self.assertRaisesRegex(ValueError, 'type metadata'):
                source.ir_settings(module(marker))

    def test_i_strong_preserved_weak_missing_recorded(self):
        result = source.compare_symbols([('T','code'),('D','data'),('W','weak'),('V','object')],
                                        [('T','code'),('D','data')])
        self.assertFalse(result['strong_missing'])
        self.assertEqual(result['missing_by_type'], {'W':1,'V':1})
        self.assertEqual(source.parse_nm('---------------- T code\n00000000 W weak\n'), [('T','code'),('W','weak')])

    def test_i_missing_strong_fails_check(self):
        result = source.compare_symbols([('T','code'),('B','data'),('A','absolute')], [('T','code')])
        self.assertEqual(result['strong_missing'], [('B','data'),('A','absolute')])
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);command=mock.Mock()
            def run(argv,prefix,stdout=None):
                stdout.write(b'---------------- T gone\n' if str(argv[-1]).endswith('.bc') else b'')
            command.run.side_effect=run
            with self.assertRaisesRegex(ValueError,'strong defined symbols missing'):
                source.check_symbols('nm',p/'input.bc',p/'obj.o',command)

    def test_j_triple_mismatch(self):
        with self.assertRaisesRegex(ValueError, 'uncertified'):
            source.ir_settings([x.replace('x86_64-tizen-linux-gnu','aarch64-tizen-linux-gnu') for x in module()])
        with self.assertRaisesRegex(ValueError,'uncertified architecture'):
            source.classify_options(FLAGS,'aarch64')

    def test_k_python39_and_chunk_digest(self):
        text=Path(source.__file__).read_text()
        ast.parse(text,feature_version=(3,9))
        self.assertNotIn('hashlib.file_digest',text)
        self.assertEqual(text.count('#!/usr/bin/env python3'),1)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'data';p.write_bytes(b'a'*(2*1024*1024+13))
            import hashlib
            self.assertEqual(source.sha(p),hashlib.sha256(p.read_bytes()).hexdigest())


class FilesystemTests(unittest.TestCase):
    def test_d_native_pass_thin_and_other_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);obj=root/'x.o';obj.write_bytes(native())
            for mode,name in [('qcD','native.a'),('qcDT','thin.a')]:
                subprocess.run(['ar',mode,str(root/name),str(obj)],check=True,capture_output=True)
            self.assertEqual(source.validate_archive(root/'native.a')['bitcode'],0)
            with self.assertRaisesRegex(ValueError,'thin archive'):
                source.validate_archive(root/'thin.a')
            text=root/'x.txt';text.write_text('unsupported')
            subprocess.run(['ar','qcD',str(root/'other.a'),str(text)],check=True,capture_output=True)
            with self.assertRaisesRegex(ValueError,'other-format'):
                source.validate_archive(root/'other.a')

    def test_e_evidence_reset_and_unsafe_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'root';root.mkdir();build=Path(tmp)/'build';build.mkdir()
            out=build/'evidence';out.mkdir();(out/'stale').write_text('x')
            source.reset_evidence(root,out,build)
            self.assertEqual(list(out.iterdir()),[])
            with self.assertRaisesRegex(ValueError,'unsafe'):
                source.reset_evidence(root,build,build)

    def test_e_native_install_skip_and_cleanup(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'root';root.mkdir();out=Path(tmp)/'output';out.mkdir()
            result={'archives':[],'status':'CONVERTED'}
            with mock.patch.object(source,'convert',return_value=result), contextlib.redirect_stdout(io.StringIO()) as log:
                source.install(root,out,'cc','dis','nm',Path(tmp))
            self.assertIn('NATIVE_ARCHIVES_SKIP',log.getvalue())
            self.assertEqual(json.loads((out/'summary.json').read_text())['status'],'PASS')

    def test_f_atomic_copy_preserves_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);dest=p/'archive.a';dest.write_bytes(b'old');dest.chmod(0o640)
            candidate=p/'new.a';candidate.write_bytes(b'new')
            source.atomic_install(candidate,dest,source.sha(candidate))
            self.assertEqual(dest.read_bytes(),b'new')
            self.assertEqual(stat.S_IMODE(dest.stat().st_mode),0o640)
            self.assertFalse(list(p.glob('.archive.a.native-*')))

    def test_f_failed_copy_preserves_original_and_records_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);root=p/'root';root.mkdir();out=p/'out';(out/'archives').mkdir(parents=True)
            dest=root/'a.a';dest.write_bytes(b'old');candidate=out/'archives/a.a';candidate.write_bytes(b'new')
            result={'status':'CONVERTED','archives':[{'path':'a.a','before_sha256':source.sha(dest),'after_sha256':source.sha(candidate)}]}
            def fail(src,dst):
                Path(dst).write_bytes(b'partial');raise OSError('injected copy failure')
            with mock.patch.object(source,'convert',return_value=result),mock.patch.object(source.shutil,'copyfile',side_effect=fail):
                with self.assertRaisesRegex(OSError,'injected copy failure'):
                    source.install(root,out,'cc','dis','nm',p)
            self.assertEqual(dest.read_bytes(),b'old')
            self.assertEqual(json.loads((out/'summary.json').read_text())['status'],'INSTALL_FAILED')
            self.assertFalse(list(root.glob('.a.a.native-*')))

    def test_h_tools_version_and_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'CMakeCache.txt').touch();tool=p/'cc';tool.write_text('fake');tool.chmod(0o755)
            command=mock.Mock()
            command.run.side_effect=lambda argv,prefix,stdout:stdout.write(b'clang version 22.1.8\n')
            source.validate_tools(p,tool,tool,tool,command,p)
            command.run.side_effect=lambda argv,prefix,stdout:stdout.write(b'clang version 23.0.0\n')
            with self.assertRaisesRegex(ValueError,'compiler major'):
                source.validate_tools(p,tool,tool,tool,command,p)
            tool.chmod(0o644)
            with self.assertRaisesRegex(ValueError,'non-executable'):
                source.validate_tools(p,tool,tool,tool,command,p)
            (p/'CMakeCache.txt').unlink()
            with self.assertRaisesRegex(ValueError,'CMakeCache'):
                source.validate_tools(p,tool,tool,tool,command,p)

    def test_l_cleanup_keeps_json_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'archives').mkdir();(p/'archives/a.a').write_text('large')
            (p/'members').mkdir();(p/'members/data.bc').write_text('large')
            (p/'members/ir-settings.json').write_text('{}')
            source.cleanup_evidence(p)
            self.assertFalse((p/'archives').exists())
            self.assertEqual([x.name for x in (p/'members').iterdir()],['ir-settings.json'])


class CancellationTests(unittest.TestCase):
    def test_g_handler_only_records_signal(self):
        command=source.Commands()
        with command.lock:
            command.interrupted(signal.SIGTERM,None)
        self.assertFalse(command.stop.is_set())
        with self.assertRaisesRegex(RuntimeError,'signal'):
            command.check()

    def test_g_success_and_timeout_reaped(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);ready=p/'ready';timeout=5
            command=source.Commands(timeout=timeout)
            child=("import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); "
                   "open("+repr(str(ready))+",'w').write('ready'); time.sleep(30)")
            with self.assertRaisesRegex(RuntimeError,'timeout'):
                command.run([sys.executable,'-c',child],p/'hang')
            self.assertTrue(ready.is_file(), '环境未建立测试前提: SIGTERM ignore handler not ready')
            self.assertFalse(command.children)
            row=json.loads((p/'hang.json').read_text())
            self.assertEqual(row['exit'],-signal.SIGKILL)
            self.assertGreaterEqual(row['wall'],timeout+3)

    def test_g_failed_leader_descendants_are_killed(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);pidfile=p/'descendant.pid'
            child="import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(30)"
            script=("import subprocess,sys,pathlib,time; "
                    "p=subprocess.Popen([sys.executable,'-c',"+repr(child)+"]); "
                    "pathlib.Path("+repr(str(pidfile))+").write_text(str(p.pid));time.sleep(.1);sys.exit(7)")
            with self.assertRaisesRegex(RuntimeError,'command failed'):
                source.Commands().run([sys.executable,'-c',script],p/'failed-leader')
            returned = time.monotonic()
            status=Path('/proc')/pidfile.read_text()/'status'
            def snapshot():
                try:
                    fields = dict(line.split(':', 1) for line in status.read_text().splitlines())
                except (FileNotFoundError, ProcessLookupError):
                    return None
                return {key: fields[key].strip() for key in ('State', 'SigPnd', 'ShdPnd')}
            first = snapshot()
            self.assertTrue(first is None or 'Z' in first['State'] or
                            (int(first['SigPnd'], 16) | int(first['ShdPnd'], 16)) & 0x100,
                            'live descendant without pending SIGKILL: '+repr(first))
            last = first
            while last is not None and 'Z' not in last['State'] and time.monotonic()-returned < 3:
                time.sleep(.005)
                last = snapshot()
            self.assertTrue(last is None or 'Z' in last['State'],
                            'descendant did not terminate within 3 seconds: '+repr((first, last)))
            self.assertLessEqual(time.monotonic()-returned, 3)

    def test_g_signal_on_success_cannot_return_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            command=source.Commands();p=Path(tmp)
            timer=threading.Timer(.08,lambda:command.interrupted(signal.SIGINT,None));timer.start()
            try:
                with self.assertRaisesRegex(RuntimeError,'signal'):
                    command.run([sys.executable,'-c','import time;time.sleep(.2)'],p/'signal')
            finally:timer.join()
            self.assertFalse(command.children)


if __name__ == '__main__':
    unittest.main(verbosity=2)
