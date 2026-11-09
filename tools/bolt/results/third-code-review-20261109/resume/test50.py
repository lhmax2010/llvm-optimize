#!/usr/bin/env python3
import hashlib, importlib.util, json, os, shlex, subprocess, sys, tempfile, unittest
from pathlib import Path
from unittest import mock
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')
S=W/'temp/rebase-359934-20261106/source'; E=Path(__file__).parent
sys.path.insert(0,str(B/'tools'))
p=S/'packaging/llvm-static-archives-native.py'
spec=importlib.util.spec_from_file_location('llvm_static_archives_source',p)
a=importlib.util.module_from_spec(spec);sys.modules[spec.name]=a;spec.loader.exec_module(a)
print('CONVERTER_IMPORT',p,'SHA256',hashlib.sha256(p.read_bytes()).hexdigest(),flush=True)
import test_static_archives_source as old1, test_static_archives_source_v2 as old2
from test_inspect_llvm_archives import native, archive
inputs=json.loads((B/'tools/bolt/results/final-20261103/flags-inputs.json').read_text())
spec_text=(S/'packaging/llvm.spec').read_text()
fragment=spec_text.split('# BEGIN TIZEN_LLVM_FIXED_FLAGS',1)[1].split('# END TIZEN_LLVM_FIXED_FLAGS',1)[0].replace('%%','%')
function=fragment.split('tizen_llvm_flags CFLAGS',1)[0]
(E/'actual-flags-fragment.sh').write_text(fragment)
subprocess.run(['/bin/sh','-n',str(E/'actual-flags-fragment.sh')],check=True)
observed=[]
def flags(kind,text,release):
    script=function+'\ntizen_llvm_flags "$1" "$2" "$3"\nprintf "%s\\0%s\\0%s" "$TIZEN_LLVM_RESULT" "$TIZEN_LLVM_NORMALIZED" "$TIZEN_LLVM_DROPPED"\n'
    run=subprocess.run(['/bin/sh','-c',script,'fixture',kind,text,str(release)],capture_output=True,check=True)
    row=run.stdout.decode().split('\0');observed.append(dict(kind=kind,input=text,release=release,result=row));return row
class FlagTests(unittest.TestCase):
    def test_toolchain_exact_three_strings(self):
        for kind in ('CFLAGS','CXXFLAGS','LDFLAGS'):
            with self.subTest(kind=kind):
                result,norm,drop=flags(kind,inputs['toolchain']['raw'][kind],0)
                self.assertEqual(result,inputs['toolchain']['effective'][kind]);self.assertEqual(drop,'')
                self.assertEqual(norm,'' if kind=='LDFLAGS' else '-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer')
    def test_basedev_fixed_and_arch_and_lists(self):
        for kind in ('CFLAGS','CXXFLAGS','LDFLAGS'):
            with self.subTest(kind=kind):
                result,norm,drop=flags(kind,inputs['basedev']['raw'][kind],1)
                expected=inputs['toolchain']['effective'][kind]
                if kind!='LDFLAGS':expected=expected.replace('-g2 -gdwarf-4','').replace(' -g ','  ')
                self.assertEqual(result,expected)
                self.assertEqual(norm,'' if kind=='LDFLAGS' else '-O2 -fstack-protector-strong -fno-omit-frame-pointer')
                self.assertEqual(drop,'' if kind=='LDFLAGS' else '-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4')
                self.assertNotIn('-strong',shlex.split(result))
    def test_strong_is_whole_token(self):
        result,norm,drop=flags('CFLAGS','-fstack-protector-strong -m64',1)
        self.assertEqual(norm,'-fstack-protector-strong');self.assertEqual(drop,'')
        self.assertNotIn('-strong',result);self.assertIn('-m64',result.split())
    def test_empty(self):
        for kind in ('CFLAGS','CXXFLAGS','LDFLAGS'):
            result,norm,drop=flags(kind,'',1);self.assertEqual(norm,'');self.assertEqual(drop,'')
            self.assertTrue(result);self.assertNotIn('-g',result.split())
    def test_repeated_tokens_preserve_arch_and_audit(self):
        result,norm,drop=flags('CFLAGS','-m64 -m64 -Os -Os -Wall -Wall -unknown -unknown',1)
        self.assertEqual(result.split().count('-m64'),2);self.assertEqual(result.split().count('-Wall'),1)
        self.assertEqual(norm,'-Os -Os');self.assertEqual(drop,'-unknown -unknown')
    def test_whitespace(self):
        raw=inputs['toolchain']['raw']['CFLAGS']; altered=' \t '+ '   \t\n'.join(raw.split())+'  '
        self.assertEqual(flags('CFLAGS',raw,0),flags('CFLAGS',altered,0))
class ReleaseTests(unittest.TestCase):
    def test_release_no_dwarf(self):
        f=[x for x in old2.FLAGS if not x.startswith('-g')]
        row=a.ir_settings(old2.module(flags=f));self.assertIsNone(row['policy']['dwarf'])
        self.assertFalse(any(x.startswith('-g') for x in row['flags']))
    def test_debug_old_rule(self):
        f=[x for x in old2.FLAGS if not x.startswith('-g')]
        for tail in (['-g'],['-g','-gdwarf-5']):
            with self.assertRaisesRegex(ValueError,'DWARF'):a.classify_options(f+tail)
        self.assertEqual(a.classify_options(f+['-g','-gdwarf-4'])['dwarf'],'-gdwarf-4')
    def test_unknown(self):
        with self.assertRaises(ValueError):a.classify_options(old2.FLAGS+['-unknown-new-flag'])
    def test_qb_failed_real_flags(self):
        # QB printed CFLAGS, not a complete per-object compile command; preserve exact observed flags.
        raw=inputs['basedev']['effective']['CFLAGS'];self.assertIn('-feliminate-unused-debug-types',raw)
        a.classify_options(['clang',*shlex.split(raw)])
    def test_release_debug_elf_rejected_in_convert(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'root';root.mkdir();build=Path(temp)/'build';build.mkdir()
            (root/'test.a').write_bytes(archive([('one.o',b'BC\xc0\xdeFAKE')]))
            cmd=mock.Mock();cmd.signal_received=None
            def run(argv,prefix,stdout=None):
                if str(prefix).endswith('disassemble'):
                    f=[x for x in old2.FLAGS if not x.startswith('-g')]
                    stdout.write(''.join(old2.module(flags=f)).encode())
                elif str(prefix).endswith('convert'):Path(argv[-1]).write_bytes(native())
                else:raise AssertionError('unexpected mocked command '+repr(argv))
                return {'exit':0}
            cmd.run.side_effect=run
            with mock.patch.object(a,'validate_tools',return_value={}):
                with self.assertRaisesRegex(ValueError,'release conversion unexpectedly emitted debug sections'):
                    a.convert(root,build/'evidence','cc','dis','nm',build,jobs=1,command=cmd,debug_info='no')

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ReleaseTests))
 (E/'tests50-result.json').write_text(json.dumps({'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors)})+'\n')
 sys.exit(not result.wasSuccessful())
