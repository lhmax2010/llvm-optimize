import importlib.util,sys,unittest,subprocess,json,hashlib,shlex,tempfile
from pathlib import Path
from unittest import mock
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');S=B.parent/'llvm-optimize/temp/review-20261102/source';E=Path(__file__).parent
sys.path.insert(0,str(B/'tools'))
p=S/'packaging/llvm-static-archives-native.py';sp=importlib.util.spec_from_file_location('llvm_static_archives_source',p);a=importlib.util.module_from_spec(sp);sys.modules[sp.name]=a;sp.loader.exec_module(a)
print('CONVERTER_IMPORT',p,'SHA256',hashlib.sha256(p.read_bytes()).hexdigest(),flush=True)
import test_static_archives_source as old1,test_static_archives_source_v2 as old2
from test_inspect_llvm_archives import native,archive
inputs=json.loads((B/'tools/bolt/results/final-20261103/flags-inputs.json').read_text())
inputs['toolchain']['effective_notes']={'LDFLAGS':'日志中只有一次赋值，按原值推定'}
(E/'flags-inputs.json').write_text(json.dumps(inputs,ensure_ascii=False,indent=2)+'\n')
spec=(S/'packaging/llvm.spec').read_text();fragment=spec.split('# BEGIN TIZEN_LLVM_FIXED_FLAGS')[1].split('# END TIZEN_LLVM_FIXED_FLAGS')[0].replace('%%','%');function=fragment.split('tizen_llvm_flags CFLAGS')[0]
(E/'flags-fragment.sh').write_text(fragment);subprocess.run(['/bin/sh','-n',str(E/'flags-fragment.sh')],check=True)
observed=[]
def flags(shell,kind,text,release,ifs='default',extra=''):
    setup={'default':'IFS=" \\t\\n"','unset':'unset IFS','colon':"IFS=':'",'newline':"IFS='\n'"}[ifs]
    if ifs=='default':setup="IFS=' \t\n'"
    script=function+'\n'+extra+'\n'+setup+'''
before_set=${IFS+x};before_ifs=${IFS-};before_opts=$-
tizen_llvm_flags "$1" "$2" "$3" || exit 1
test "$before_set" = "${IFS+x}" && test "$before_ifs" = "${IFS-}" && test "$before_opts" = "$-" || exit 99
case $1 in CFLAGS) tizen_llvm_report_warnings \"$TIZEN_LLVM_UNREVIEWED\" '' '' ;; CXXFLAGS) tizen_llvm_report_warnings '' \"$TIZEN_LLVM_UNREVIEWED\" '' ;; LDFLAGS) tizen_llvm_report_warnings '' '' \"$TIZEN_LLVM_UNREVIEWED\" ;; esac
printf 'FLAGS_RESULT\\n%s\\0%s\\0%s' "$TIZEN_LLVM_RESULT" "$TIZEN_LLVM_NORMALIZED" "$TIZEN_LLVM_DROPPED"
'''
    r=subprocess.run([shell,'-c',script,'test',kind,text,str(release)],capture_output=True,text=True)
    observed.append({'shell':shell,'kind':kind,'input':text,'mode':release,'IFS':ifs,'extra':extra,'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    r.raw_stdout=r.stdout
    if 'FLAGS_RESULT\n' in r.stdout:r.stdout=r.stdout.split('FLAGS_RESULT\n',1)[1]
    return r
class Flags(unittest.TestCase):
    def test_certified_and_ifs(self):
        for shell in ('/bin/sh','/bin/dash'):
         for ifs in ('default','unset','colon','newline'):
          for kind in ('CFLAGS','CXXFLAGS','LDFLAGS'):
           r=flags(shell,kind,inputs['toolchain']['raw'][kind],0,ifs);self.assertEqual(r.returncode,0,r.stderr)
           out,norm,drop=r.stdout.split('\0');self.assertEqual(out,inputs['toolchain']['effective'][kind]);self.assertEqual(drop,'');self.assertNotIn('FLAGS_WARNING',r.raw_stdout+r.stderr)
    def test_basedev(self):
        for shell in ('/bin/sh','/bin/dash'):
         for kind in ('CFLAGS','CXXFLAGS','LDFLAGS'):
          r=flags(shell,kind,inputs['basedev']['raw'][kind],1);self.assertEqual(r.returncode,0,r.stderr)
          self.assertNotIn('FLAGS_WARNING',r.raw_stdout+r.stderr)
          out,norm,drop=r.stdout.split('\0');expected=inputs['toolchain']['effective'][kind]
          if kind!='LDFLAGS':expected=expected.replace('-g2 -gdwarf-4','').replace(' -g ','  ')
          self.assertEqual(out,expected);self.assertNotIn('-strong',out.split())
          self.assertEqual(drop,'' if kind=='LDFLAGS' else '-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4')
          self.assertEqual(norm,'' if kind=='LDFLAGS' else '-O2 -fstack-protector-strong -fno-omit-frame-pointer')
    def test_warning_tokens_and_native_rejection(self):
        for shell in ('/bin/sh','/bin/dash'):
         for kind,token in [('CFLAGS','-fcf-protection=full'),('LDFLAGS','-Wl,-z,now'),('CFLAGS','-mno-avx'),('CFLAGS','-march=native'),('CFLAGS','-mtune=native'),('CFLAGS','-gsplit-dwarf')]:
          r=flags(shell,kind,inputs['basedev']['raw'][kind]+' '+token,1)
          if token in ('-march=native','-mtune=native'):
           self.assertEqual(r.returncode,1);self.assertIn('TIZEN_LLVM_FIXED_FLAGS_FAILED',r.stderr)
          else:
           self.assertEqual(r.returncode,0);self.assertNotIn(token,r.stdout.split('\0')[0].split());self.assertIn('TIZEN_LLVM_FLAGS_WARNING',r.raw_stdout);self.assertIn('TIZEN_LLVM_FLAGS_WARNING',r.stderr)
          self.assertIn(token,r.stderr)
    def test_empty_allowlist(self):
        for shell in ('/bin/sh','/bin/dash'):
         r=flags(shell,'CFLAGS',inputs['basedev']['raw']['CFLAGS'],1,extra="TIZEN_LLVM_EXPECTED_DROPPED=''");self.assertEqual(r.returncode,0);self.assertIn('-fno-inline-functions',r.stderr);self.assertIn('TIZEN_LLVM_FLAGS_WARNING',r.raw_stdout)
    def test_debug_sequence(self):
        for shell in ('/bin/sh','/bin/dash'):
         for seq in ('-g2 -gdwarf-4','-g3 -gdwarf-5 -g'):
          for kind in ('CFLAGS','CXXFLAGS'):
           r=flags(shell,kind,seq,0);self.assertEqual(r.returncode,0);self.assertIn('TIZEN_LLVM_FLAGS_WARNING uncertified debug option sequence: ['+seq+']',r.stderr)
           r=flags(shell,kind,seq,1);self.assertEqual(r.returncode,0,r.stderr);self.assertNotIn('FLAGS_WARNING',r.raw_stdout+r.stderr)
    def test_aggregate_warning_once_per_stream(self):
        import os
        env=dict(os.environ,CFLAGS=inputs['basedev']['raw']['CFLAGS']+' -fcf-protection=full',CXXFLAGS=inputs['basedev']['raw']['CXXFLAGS']+' -mno-avx',LDFLAGS='-Wl,-z,now')
        for shell in ('/bin/sh','/bin/dash'):
         r=subprocess.run([shell,'-c','TIZEN_LLVM_RELEASE=1\n'+fragment],env=env,capture_output=True,text=True)
         self.assertEqual(r.returncode,0,r.stderr)
         expected='TIZEN_LLVM_FLAGS_WARNING unreviewed project options dropped: CFLAGS=[-fcf-protection=full] CXXFLAGS=[-mno-avx] LDFLAGS=[-Wl,-z,now] (manual review of the build log required)'
         self.assertEqual(r.stdout.count(expected),1);self.assertEqual(r.stderr.count(expected),1)
    def test_glob_option_restored(self):
        for shell in ('/bin/sh','/bin/dash'):
         for ifs in ('default','unset','colon','newline'):
          r=flags(shell,'CFLAGS',inputs['toolchain']['raw']['CFLAGS'],0,ifs,extra='set -f');self.assertEqual(r.returncode,0,r.stderr)
    def test_mode_invalid(self):
        for shell in ('/bin/sh','/bin/dash'):
         for mode in ('','2','yes'):
          r=flags(shell,'CFLAGS','',mode);self.assertEqual(r.returncode,1);self.assertIn('TIZEN_LLVM_RELEASE',r.stderr)
    def test_empty_and_duplicate_and_whitespace(self):
        for shell in ('/bin/sh','/bin/dash'):
         self.assertEqual(flags(shell,'CFLAGS','',1).returncode,0)
         r=flags(shell,'CFLAGS','-m64 -m64 -Os -Os -Wall -Wall',1);self.assertEqual(r.returncode,0);out,norm,drop=r.stdout.split('\0');self.assertEqual(out.split().count('-m64'),2);self.assertEqual(norm,'-Os -Os');self.assertEqual(drop,'')
         raw=inputs['toolchain']['raw']['CFLAGS'];r=flags(shell,'CFLAGS',' \t\n'.join(raw.split()),0);self.assertEqual(r.returncode,0);self.assertEqual(r.stdout.split('\0')[0],inputs['toolchain']['effective']['CFLAGS'])
class Converter(unittest.TestCase):
    def row(self,debug,flags=None):return a.ir_settings(old2.module(flags=flags),debug_info=debug)
    def real_command(self):
        census=json.loads((E/'debug-census.json').read_text());p=Path(census['source'])/census['rows'][0]['path']
        raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==census['rows'][0]['sha256']
        row=json.loads(raw);(E/'real-recorded-command.json').write_text(json.dumps({'source':str(p),'recorded_command':row['recorded_command']},indent=2)+'\n')
        return row['recorded_command']
    def test_debug_yes(self):
        row=self.row('yes',self.real_command());self.assertEqual(row['policy']['dwarf'],'-gdwarf-4');self.assertIn('-g',row['flags']);self.assertIn('-gdwarf-4',row['flags'])
    def test_release_no(self):
        r=self.row('no',[x for x in old2.FLAGS if not x.startswith('-g')]);self.assertIsNone(r['policy']['dwarf']);self.assertFalse(any(x.startswith('-g') for x in r['flags']))
    def test_expected_yes_found_no(self):
        with self.assertRaisesRegex(ValueError,'expected debug, found release'):self.row('yes',[x for x in self.real_command() if not x.startswith('-g')])
    def test_expected_no_found_yes(self):
        with self.assertRaisesRegex(ValueError,'expected=no found=yes'):self.row('no')
    def test_bad_debug_rule(self):
        for tail in (['-g'],['-g','-gdwarf-5']):
         with self.assertRaisesRegex(ValueError,'DWARF'):self.row('yes',[x for x in old2.FLAGS if not x.startswith('-g')]+tail)
    def test_unknown_and_qb_failure(self):
        for flags,token in [(old2.FLAGS+['-unknown-option'],'unknown-option'),(['clang',*shlex.split(inputs['basedev']['effective']['CFLAGS'])],'feliminate-unused-debug-types')]:
         with self.assertRaisesRegex(ValueError,token):a.classify_options(flags)
    def test_preserved_native_debug_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
         root=Path(tmp)/'root';root.mkdir();build=Path(tmp)/'build';build.mkdir()
         data=archive([('native.o',native())]);(root/'native.a').write_bytes(data)
         self.assertTrue(a.elf_details(native())[1])
         cmd=mock.Mock();cmd.signal_received=None
         with mock.patch.object(a,'validate_tools',return_value={}):
          result=a.convert(root,build/'evidence','cc','dis','nm',build,command=cmd,debug_info='no')
         self.assertEqual(result['native_members_preserved'],1);self.assertEqual(result['native_archives_skipped'],1)
         self.assertEqual((root/'native.a').read_bytes(),data);cmd.run.assert_not_called()
    def test_cli_mode_required(self):
        r=subprocess.run([sys.executable,'-B',str(p),'--root',str(E),'--build',str(E),'--evidence',str(E),'--arch','x86_64','--compiler','cc','--disassembler','dis','--nm','nm'],capture_output=True,text=True);self.assertEqual(r.returncode,2);self.assertIn('the following arguments are required: --debug-info',r.stderr)
    def test_release_debug_sections_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
         root=Path(tmp)/'root';root.mkdir();build=Path(tmp)/'build';build.mkdir();(root/'test.a').write_bytes(archive([('one.o',b'BC\xc0\xdeFAKE')]))
         cmd=mock.Mock();cmd.signal_received=None
         def run(argv,prefix,stdout=None):
          if str(prefix).endswith('disassemble'):stdout.write(''.join(old2.module(flags=[x for x in old2.FLAGS if not x.startswith('-g')])).encode())
          elif str(prefix).endswith('convert'):Path(argv[-1]).write_bytes(native())
          else:raise AssertionError(argv)
          return {'exit':0}
         cmd.run.side_effect=run
         with mock.patch.object(a,'validate_tools',return_value={}):
          with self.assertRaisesRegex(ValueError,'release conversion unexpectedly emitted debug sections'):a.convert(root,build/'evidence','cc','dis','nm',build,jobs=1,command=cmd,debug_info='no')
if __name__=='__main__':
 suite=unittest.TestSuite()
 for m in (old1,old2,sys.modules[__name__]):suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(m))
 r=unittest.TextTestRunner(verbosity=2).run(suite)
 (E/'policy-observed.json').write_text(json.dumps(observed,ensure_ascii=False,indent=2)+'\n');(E/'policy-result.json').write_text(json.dumps({'tests':r.testsRun,'failures':len(r.failures),'errors':len(r.errors)},indent=2)+'\n')
 sys.exit(not r.wasSuccessful())
