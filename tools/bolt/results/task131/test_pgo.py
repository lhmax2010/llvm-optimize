from pathlib import Path
import hashlib, importlib.util, json, lzma, os, shlex, subprocess, unittest
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
B=W.with_name('llvm-optimize-bolt'); T=W/'temp/task131/b-fixtures-final'; E=B/'tools/bolt/results/task131'
S=W/'temp/task131/pgo-dev/packaging'
def load(name):
    p=S/(name+'.py')
    spec=importlib.util.spec_from_file_location(name,p)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
H=load('clang-bolt-helper'); V=load('llvm-static-archives-native')
R=W/'temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
loader=[str(R/'lib64/ld-linux-x86-64.so.2'),'--library-path',':'.join(str(R/x) for x in ('usr/lib64','lib64'))]
clang=loader+[str(R/'usr/bin/clang-22')]
tool_log=[]
def command(args):
    proc=subprocess.run(args,cwd=T,text=True,capture_output=True,timeout=45)
    tool_log.append({'argv':args,'rc':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr})
    (E/'fixture-commands-final.json').write_text(json.dumps(tool_log,indent=2)+'\n')
    if proc.returncode:
        raise RuntimeError(f'{args[0]} returned {proc.returncode}:\n{proc.stderr}')
    return proc
def compile_c(src,out,opts):
    dry=command(clang+['-###','--no-default-config','--target=x86_64-tizen-linux-gnu',
                       '-resource-dir='+str(R/'usr/lib64/clang/22'),'-O3','-c',str(src),'-o',str(out),*opts])
    steps=[shlex.split(line) for line in dry.stderr.splitlines() if line.startswith(' ')]
    (cc1,)=[step[1:] for step in steps if len(step)>1 and step[1]=='-cc1']
    if '-record-command-line' in cc1:
        idx=cc1.index('-record-command-line')+1
        recorded=shlex.split(cc1[idx])
        assert Path(recorded[0]).name=='ld-linux-x86-64.so.2' and recorded[1]=='-###'
        recorded[:2]=[str(R/'usr/bin/clang-22')]
        cc1[idx]=shlex.join(recorded)
    command(clang+cc1)
def file_info(path,payload):
    data=lzma.compress(payload)
    path.write_bytes(data)
    sha=lambda b:hashlib.sha256(b).hexdigest()
    return dict(file=path.name,bytes=len(payload),sha256=sha(payload),xz_bytes=len(data),xz_sha256=sha(data))
class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.manifest=T/(self._testMethodName+'.json')
        self.data=T/(self._testMethodName+'.profdata.xz')
        self.bolt=T/(self._testMethodName+'.fdata.xz')
        self.p=file_info(self.data,b'profile-data')
        self.f=file_info(self.bolt,b'bolt-data')
        self.doc={'format':1,'status':'READY','llvm_version':'22.1.8','profiles':[
            {'project':'T','pgo':True,'bolt':True,'profdata':self.p,'bolt_profile':self.f},
            {'project':'T','pgo':True,'bolt':False,'profdata':self.p}]}
    def save(self):
        self.manifest.write_text(json.dumps(self.doc))
    def select(self,pr='T',pgo=True,bolt=True):
        self.save()
        return H.select_pgo_profile(self.manifest,pr,pgo,bolt)
    def test_prepare_and_correct_mapping(self):
        self.save()
        got=H.prepare_pgo(self.manifest,'T',T/'prepared',self.data,self.bolt)
        self.assertEqual(Path(got['profdata']['path']).read_bytes(),b'profile-data')
        self.assertEqual(Path(got['bolt']['path']).read_bytes(),b'bolt-data')
    def test_uncompressed_digest_mismatch(self):
        self.p['sha256']='0'*64
        self.save()
        with self.assertRaisesRegex(H.GateError,'uncompressed profile identity mismatch'):
            H.prepare_pgo(self.manifest,'T',T/'bad-digest',self.data)
    def test_compressed_digest_mismatch(self):
        self.p['xz_sha256']='0'*64
        self.save()
        with self.assertRaisesRegex(H.GateError,'compressed profile identity mismatch'):
            H.prepare_pgo(self.manifest,'T',T/'bad-xz-digest',self.data)
    def test_placeholder_manifest(self):
        with self.assertRaisesRegex(H.GateError,'PLACEHOLDER'):
            H.select_pgo_profile(S/'llvm-profiles.manifest','T',True,True)
    def test_placeholder_asset(self):
        self.doc['profiles'][1]['profdata']=file_info(self.data,b'PLACEHOLDER\n')
        self.save()
        with self.assertRaisesRegex(H.GateError,'placeholder profile payload'):
            H.prepare_pgo(self.manifest,'T',T/'bad-placeholder',self.data)
    def test_missing_mapping(self):
        with self.assertRaisesRegex(H.GateError,'missing profile mapping'):
            self.select('D')
    def test_duplicate_mapping(self):
        self.doc['profiles'].append(self.doc['profiles'][0])
        with self.assertRaisesRegex(H.GateError,'duplicate profile mapping'):
            self.select()
    def test_wrong_version(self):
        self.doc['llvm_version']='22.1.7'
        with self.assertRaisesRegex(H.GateError,'LLVM version'):
            self.select()
    def test_selection_by_bolt(self):
        self.assertIn('bolt_profile',self.select(bolt=True))
        self.assertNotIn('bolt_profile',self.select(bolt=False))
        self.assertTrue(H.select_pgo_profile(None,'T',False,True)['baseline'])
        self.assertIsNone(H.select_pgo_profile(None,'D',False,False))
class NinjaTests(unittest.TestCase):
    def rows(self,main,runtime):
        return [{'output':'lib/CMakeFiles/LLVM.dir/x.c.o','file':'x.c','command':'clang -c x.c '+main},
                {'output':'projects/compiler-rt/lib/asan/CMakeFiles/RTAsan.dir/y.c.o','file':'y.c','command':'clang -c y.c '+runtime}]
    def test_exact_scope(self):
        self.assertEqual(H.check_pgo_commands(self.rows('-fprofile-instr-use=/p',''),'/p')['profile_use'],1)
    def test_exclude_runtime(self):
        with self.assertRaisesRegex(H.GateError,'unexpected PGO option'):
            H.check_pgo_commands(self.rows('-fprofile-instr-use=/p','-fprofile-instr-use=/p'),'/p')
    def test_default_no_use(self):
        self.assertEqual(H.check_pgo_commands(self.rows('',''))['profile_use'],0)
        with self.assertRaisesRegex(H.GateError,'unexpected PGO option'):
            H.check_pgo_commands(self.rows('-fprofile-instr-use=/p',''))
    def test_wrong_file(self):
        with self.assertRaisesRegex(H.GateError,'wrong PGO option'):
            H.check_pgo_commands(self.rows('-fprofile-instr-use=/wrong',''),'/p')
class ArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        src=T/'probe.c'
        src.write_text('volatile int result;\nint counted(int x) { return x ? x + 1 : x; }\n')
        historical=W/'temp/pgo-profiles-keep-20261102/clang.profdata'
        cls.native=T/'profile-use-native.o'
        profile=['-fprofile-instr-use='+str(historical)]
        compile_c(src,cls.native,profile)
        cls.instrumented=T/'instrumented.o'
        compile_c(src,cls.instrumented,['-fprofile-generate='+str(T)])
        cls.bitcode=T/'profile-use-bitcode.o'
        compile_c(src,cls.bitcode,[*profile,'-frecord-gcc-switches','-flto=thin'])
        cls.ll=T/'profile-use.ll'
        command(loader+[str(R/'usr/bin/llvm-dis'),str(cls.bitcode),'-o',str(cls.ll)])
    def root(self,obj):
        root=T/self._testMethodName
        lib=root/'usr/lib64'
        lib.mkdir(parents=True)
        command(['/usr/bin/ar','rc',str(lib/'libprobe.a'),str(obj)])
        return root
    def test_instrumented_archive_rejected(self):
        with self.assertRaisesRegex(H.GateError,'PGO runtime dependency gate failed'):
            H.pgo_runtime_dependencies(self.root(self.instrumented),True)
    def test_profile_use_only_archive_accepted(self):
        report=H.pgo_runtime_dependencies(self.root(self.native),True)
        self.assertEqual((report['status'],report['archives']),('PASS',1))
    def test_disabled_instrumented_archive_logged(self):
        report=H.pgo_runtime_dependencies(self.root(self.instrumented),False)
        self.assertEqual(report['status'],'FAIL')
    def test_real_profile_use_bitcode_option(self):
        p=self.ll.read_text()
        self.assertIn('-fprofile-instr-use=',p)
        ir=V.ir_settings(p.splitlines(),debug_info='no')
        flags=[x for x in ir['policy']['tokens'] if x['token'].startswith('-fprofile-instr-use=')]
        self.assertEqual([x['category'] for x in flags],['ir'])
        self.assertFalse(any(x.startswith('-fprofile') for x in ir['flags']))
        output=T/'converted.o'
        compile_flags=[*ir['flags'],str(self.bitcode),'-o',str(output)]
        dry=command(clang+['-###',*compile_flags])
        steps=[shlex.split(line) for line in dry.stderr.splitlines() if line.startswith(' ')]
        (cc1,)=[step[1:] for step in steps if len(step)>1 and step[1]=='-cc1']
        command(clang+cc1)
        self.assertEqual(V.member_kind(output.read_bytes()),'machine')
    def test_generate_and_unknown_profile_options_rejected(self):
        for flag in ('-fprofile-generate','-fprofile-instr-generate','-fprofile-unknown','-fprofile-instr-use='):
            with self.subTest(flag=flag),self.assertRaisesRegex(ValueError,'uncertified profile option'):
                V.classify_options(['clang','-O3',flag])
T.mkdir(exist_ok=False)
unittest.main(verbosity=2)
