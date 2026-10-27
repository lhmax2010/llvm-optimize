#!/usr/bin/env python3
"""Fixture tests: no LLVM build, linker or BOLT execution."""
import hashlib
import json
import lzma
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import bolt_helper as h

EDGE = ': && /bin/clang++ driver.o -Xlinker --dependency-file=tools/clang/tools/driver/CMakeFiles/clang.dir/link.d -o bin/clang-22 -Wl,--thinlto-cache-dir=/original/cache -Wl,-rpath,"\\$ORIGIN/../lib64:" libLLVM.a && :'

def log(n=100, m=1000, s=None, u=None, q=None):
    v='BOLT-INFO: %s out of %s functions in the binary (10.0%%) have non-empty execution profile\n' % (n,m)
    if s is not None:v+='BOLT-WARNING: %s (5.0%% of all profiled) functions have invalid (possibly stale) profile. Use -report-stale to see the list.\n' % s
    if u is not None:v+='BOLT-INFO: profile for %s objects was ignored\n' % u
    if q is not None:v+='BOLT-INFO: %s functions with profile could not be optimized\n' % q
    return v

def elf(path, payload=b'\xc3', debug=False, bolt=True, symbols=None, reloc=False, stripped=None):
    stripped = Path(path).name == 'candidate' if stripped is None else stripped
    if stripped: bolt=False
    names=['','.shstrtab','.text'] + ([] if stripped else ['.strtab','.symtab']) + (['.rela.text'] if reloc else []) + (['.note.bolt_info'] if bolt else []) + (['.debug_info'] if debug else [])
    ns=b'\0'; nidx={}
    for n in names:nidx[n]=len(ns);ns+=n.encode()+b'\0'
    strings=b'\0probe\0';syms=symbols or [(0,0,0,0,0,0),(1,0x12,0,2,0x400100,len(payload))]
    symdata=b''.join(struct.pack('<IBBHQQ',*x) for x in syms)
    blobs={'.shstrtab':ns,'.text':payload,'.strtab':strings,'.symtab':symdata,
           '.rela.text':struct.pack('<QQq',0x400100,(1<<32)|1,7),'.note.bolt_info':b'BOLT', '.debug_info':b'old dwarf'}
    data=bytearray(256);headers=[(0,0,0,0,0,0,0,0,0,0)]
    for n in names[1:]:
        off=len(data);b=blobs[n];data.extend(b)
        typ=3 if n in ('.strtab','.shstrtab') else (2 if n=='.symtab' else (4 if n=='.rela.text' else (7 if n.startswith('.note') else 1)))
        headers.append((nidx[n],typ,6 if n=='.text' else 0,0x400100 if n=='.text' else 0,off,len(b),3 if n=='.symtab' else (4 if n=='.rela.text' else 0),1 if n=='.symtab' else (2 if n=='.rela.text' else 0),1,24 if n in ('.symtab','.rela.text') else 0))
    shoff=len(data)
    for x in headers:data.extend(struct.pack('<IIQQQQIIQQ',*x))
    ident=b'\x7fELF\x02\x01\x01'+b'\0'*9
    data[:64]=struct.pack('<16sHHIQQQIHHHHHH',ident,2,62,1,0x400100,64,shoff,0,64,56,1,64,len(headers),1)
    data[64:120]=struct.pack('<IIQQQQQQ',1,5,256,0x400100,0x400100,len(payload),len(payload),1)
    Path(path).write_bytes(data);Path(path).chmod(0o755)

class Base(unittest.TestCase):
    def setUp(self):self.temp=tempfile.TemporaryDirectory();self.d=Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()
    def identity(self):
        before=self.d/'before';elf(before)
        return {'before_path':str(before), 'before_sha256':h.digest(before), 'bolt_note_before':True, 'after_sha256':h.digest(self.d/'candidate')}

class ReplayTests(Base):
    def test_emit_relocs_and_literal_origin(self):
        s=h.replay_script(EDGE,self.d/'out with space',self.d/'dep',self.d/'cache');self.assertIn('\\$ORIGIN',s)
        self.assertTrue(s.endswith('-Wl,--emit-relocs\n'))
        self.assertEqual(subprocess.run(['/bin/dash','-n'],input=s,text=True).returncode,0)
    def test_reference_no_strip(self):self.assertNotIn('--strip-debug',h.replay_script(EDGE,'out','dep'))
    def test_missing_output(self):
        with self.assertRaises(h.GateError):h.replay_script(EDGE.replace('-o bin/clang-22 ','-o other '),'out','dep','cache')
    def test_multiline(self):
        with self.assertRaises(h.GateError):h.replay_script(EDGE+'\n'+EDGE,'out','dep','cache')
    def test_duplicate_output(self):
        with self.assertRaises(h.GateError):h.replay_script(EDGE.replace('driver.o','driver.o -o bin/clang-22 '),'out','dep','cache')
    def test_duplicate_dep(self):
        with self.assertRaises(h.GateError):h.replay_script(EDGE.replace('driver.o','driver.o '+EDGE.split('--dependency-file=')[1].split()[0]+' --dependency-file=tools/clang/tools/driver/CMakeFiles/clang.dir/link.d'),'out','dep','cache')
    def test_command_substitution(self):
        with self.assertRaises(h.GateError):h.replay_script(EDGE.replace('driver.o','$(touch x)'),'out','dep','cache')
    def test_semicolon(self):
        with self.assertRaises(h.GateError):h.replay_script(EDGE.replace('driver.o','driver.o; touch x'),'out','dep','cache')
    def test_unescaped_environment(self):
        with self.assertRaises(h.GateError):h.replay_script(EDGE.replace('\\$ORIGIN','$ORIGIN'),'out','dep','cache')
    def test_extra_output(self):
        with self.assertRaises(h.GateError):h.replay_script(EDGE.replace('driver.o','driver.o -Wl,-Map,foo'),'out','dep','cache')

class MatchingTests(unittest.TestCase):
    def parse(self,t,argv=()):return h.match_counts(t,argv,True,True)
    def test_zero_optional_lines(self):self.assertEqual(self.parse(log())['R'],0)
    def test_stale_exact_boundary(self):self.assertEqual(self.parse(log(s=5))['S_over_N'],.05)
    def test_unused_exact_boundary(self):self.assertEqual(self.parse(log(n=95,u=5))['R'],.05)
    def test_stale_over(self):
        with self.assertRaises(h.GateError):self.parse(log(s=6))
    def test_unused_over(self):
        with self.assertRaises(h.GateError):self.parse(log(n=95,u=6))
    def test_combined(self):
        with self.assertRaises(h.GateError):self.parse(log(s=3,u=3))
    def test_non_simple_not_stale(self):self.assertEqual(self.parse(log(q=383))['S'],0)
    def test_zero_n(self):
        with self.assertRaises(h.GateError):self.parse(log(n=0))
    def test_n_exceeds_m(self):
        with self.assertRaises(h.GateError):self.parse(log(n=100,m=10))
    def test_no_n(self):
        with self.assertRaises(h.GateError):self.parse('BOLT-INFO: profile for 1 objects was ignored\n')
    def test_duplicates(self):
        with self.assertRaises(h.GateError):self.parse(log()+log())
    def test_malformed_stale(self):
        with self.assertRaises(h.GateError):self.parse(log()+'BOLT-WARNING: -1 (5%) functions have invalid (possibly stale) profile.\n')
    def test_failed_tool(self):
        with self.assertRaises(h.GateError):h.match_counts(log(),[],False,True)
    def test_untrusted_tool(self):
        with self.assertRaises(h.GateError):h.match_counts(log(),[],True,False)
    def test_infer_disabled_spelling_forbidden(self):
        with self.assertRaises(h.GateError):self.parse(log(),['-infer-stale-profile=false'])

class ProfileTests(Base):
    def test_valid_sha(self):
        data=b'fixture profile';p=self.d/'profile.xz';p.write_bytes(lzma.compress(data))
        with patch.object(h,'PROFILE_SHA',hashlib.sha256(data).hexdigest()):h.profile_unpack(p,self.d/'out')
        self.assertEqual((self.d/'out').read_bytes(),data)
    def test_bad_sha_removes_output(self):
        p=self.d/'profile.xz';p.write_bytes(lzma.compress(b'bad'))
        with self.assertRaises(h.GateError):h.profile_unpack(p,self.d/'out')
        self.assertFalse((self.d/'out').exists())
    def test_corrupt_xz(self):
        p=self.d/'profile.xz';p.write_bytes(b'bad xz')
        with self.assertRaises(lzma.LZMAError):h.profile_unpack(p,self.d/'out')
    def test_existing_output(self):
        p=self.d/'out';p.write_bytes(b'keep')
        with self.assertRaises(h.GateError):h.profile_unpack('missing',p)
        self.assertEqual(p.read_bytes(),b'keep')

class ElfTests(Base):
    def test_debug_rejected(self):
        elf(self.d/'a',debug=True);e=h.ELF(self.d/'a')
        try:
            with self.assertRaises(h.GateError):e.audit()
        finally:e.close()
    def test_note_required(self):
        elf(self.d/'a',bolt=False);e=h.ELF(self.d/'a')
        try:
            with self.assertRaises(h.GateError):e.audit()
        finally:e.close()
    def test_entry_and_native(self):
        elf(self.d/'a');e=h.ELF(self.d/'a')
        try:self.assertEqual(len(e.audit()['loads']),1)
        finally:e.close()
    def test_invalid_range(self):
        (self.d/'a').write_bytes(b'\x7fELF\x02\x01')
        with self.assertRaises(h.GateError):h.ELF(self.d/'a')

class BuildrootUnchangedTests(Base):
    def setUp(self):
        super().setUp()
        self.root=self.d/'root';(self.root/'usr/share').mkdir(parents=True)
        self.file=self.root/'usr/share/probe';self.file.write_bytes(b'original')
        self.link=self.root/'usr/share/link';self.link.symlink_to('probe')
        self.before=h.root_snapshot(self.root)
    def compare(self):return h.compare_root(self.root,self.before,self.d/'after.json')
    def test_unchanged_passes(self):self.assertTrue(self.compare()['buildroot_unchanged'])
    def test_added_file_fails_with_path(self):
        (self.root/'usr/share/new').write_bytes(b'x')
        with self.assertRaisesRegex(h.GateError,'added: usr/share/new'):self.compare()
    def test_added_symlink_fails_with_path(self):
        (self.root/'usr/share/new').symlink_to('probe')
        with self.assertRaisesRegex(h.GateError,'added: usr/share/new'):self.compare()
    def test_removed_file_fails_with_path(self):
        self.file.unlink()
        with self.assertRaisesRegex(h.GateError,'removed: usr/share/probe'):self.compare()
    def test_content_change_fails_with_path(self):
        self.file.write_bytes(b'different')
        with self.assertRaisesRegex(h.GateError,'entry differs: usr/share/probe'):self.compare()
    def test_permission_change_fails_with_path(self):
        self.file.chmod(0o600)
        with self.assertRaisesRegex(h.GateError,'entry differs: usr/share/probe'):self.compare()
    def test_symlink_target_change_fails_with_path(self):
        self.link.unlink();self.link.symlink_to('different')
        with self.assertRaisesRegex(h.GateError,'entry differs: usr/share/link'):self.compare()
    def test_directory_permission_change_fails_with_path(self):
        (self.root/'usr/share').chmod(0o700)
        with self.assertRaisesRegex(h.GateError,'metadata differ: usr/share'):self.compare()

class InstallTests(Base):
    def root(self):
        r=self.d/'root';(r/'usr/bin').mkdir(parents=True);elf(r/'usr/bin/clang-22');return r
    def test_absolute_alias_resolves_inside_root(self):
        r=self.root();(r/'usr/bin/clang').symlink_to('/usr/bin/clang-22')
        self.assertEqual(h.rooted_resolve(r,r/'usr/bin/clang'),r/'usr/bin/clang-22')
    def test_hard_and_soft_aliases_normalized(self):
        r=self.root();os.link(r/'usr/bin/clang-22',r/'usr/bin/clang++');(r/'usr/bin/clang').symlink_to('/usr/bin/clang++')
        elf(self.d/'candidate');state=h.install_candidate(r,self.d/'candidate',self.d/'state.json',self.identity())
        for name in ['clang','clang++']:self.assertEqual(os.readlink(r/'usr/bin'/name),'clang-22')
        self.assertEqual(len(state['alias_changes']),2)
    def test_old_copy_alias_normalized(self):
        r=self.root();shutil=__import__('shutil');shutil.copyfile(r/'usr/bin/clang-22',r/'usr/bin/clang++');elf(self.d/'candidate')
        h.install_candidate(r,self.d/'candidate',self.d/'state.json',self.identity());self.assertTrue((r/'usr/bin/clang++').is_symlink())
    def test_cycle_stops(self):
        r=self.root();(r/'usr/bin/clang').symlink_to('clang++');(r/'usr/bin/clang++').symlink_to('clang')
        with self.assertRaises(h.GateError):h.alias_group(r)
    def test_escape_stops(self):
        r=self.root();(r/'usr/bin/clang').symlink_to('../../../outside')
        with self.assertRaises(h.GateError):h.alias_group(r)
    def test_different_clang_alias_stops(self):
        r=self.root();(r/'usr/bin/clang++').write_bytes(b'old')
        with self.assertRaises(h.GateError):h.alias_group(r)
    def test_debug_path_stops(self):
        r=self.d/'debug-root';(r/'usr/bin').mkdir(parents=True);elf(r/'usr/bin/clang-22');elf(self.d/'candidate')
        with self.assertRaises(h.GateError):h.install_candidate(r,self.d/'candidate',self.d/'state.json',self.identity())
    def test_post_sha_change_stops(self):
        r=self.root();elf(self.d/'candidate');state=h.install_candidate(r,self.d/'candidate',self.d/'state.json',self.identity());(r/'usr/bin/clang-22').write_bytes(b'changed')
        with self.assertRaises(h.GateError):h.post_gate(r,state,'unused',self.d/'gate')
    def test_post_stale_alias_stops(self):
        r=self.root();(r/'usr/bin/clang').symlink_to('clang-22');elf(self.d/'candidate');state=h.install_candidate(r,self.d/'candidate',self.d/'state.json',self.identity());(r/'usr/bin/clang').unlink();(r/'usr/bin/clang').symlink_to('/usr/bin/clang-22')
        with self.assertRaises(h.GateError):h.post_gate(r,state,'unused',self.d/'gate')
    def test_post_with_fixed_fixture_compiler(self):
        r=self.root();elf(self.d/'candidate');state=h.install_candidate(r,self.d/'candidate',self.d/'state.json',self.identity())
        h.installed_baseline(r,self.d/'installed-baseline.json')
        with patch.object(h,'tiny_gate',return_value=[{'byte_equal':True}]), patch.object(h,'real_gate',return_value={'real_pass':True}):
            result=h.post_gate(r,state,self.d/'before',self.d/'gate')
        self.assertTrue(result['strip_identity_pass'])
    def test_identity_wrong_final_sha(self):
        r=self.root();elf(self.d/'candidate');identity=self.identity();identity['after_sha256']='bad'
        with self.assertRaises(h.GateError):h.install_candidate(r,self.d/'candidate',self.d/'state.json',identity)
    def test_identity_unproven_note(self):
        r=self.root();elf(self.d/'candidate');identity=self.identity();identity['bolt_note_before']=False
        with self.assertRaises(h.GateError):h.install_candidate(r,self.d/'candidate',self.d/'state.json',identity)
    def test_identity_changed_prestrip(self):
        r=self.root();elf(self.d/'candidate');identity=self.identity();(self.d/'before').write_bytes(b'changed')
        with self.assertRaises(h.GateError):h.install_candidate(r,self.d/'candidate',self.d/'state.json',identity)

class TinyTests(Base):
    def compiler(self,name,mismatch=False):
        p=self.d/name;p.write_text('#!/usr/bin/env python3\nimport sys\nfrom pathlib import Path\nif "--version" in sys.argv: print("fixture clang");sys.exit(0)\ntriple=next(x for x in sys.argv if x.startswith("--target="))\nPath(sys.argv[sys.argv.index("-o")+1]).write_bytes((triple'+(' + "mismatch"' if mismatch else '')+').encode())\n');p.chmod(0o755);return str(p)
    def test_three_targets_complete_bytes(self):self.assertEqual(len(h.tiny_gate(self.compiler('a'),self.compiler('b'),self.d/'gate')),3)
    def test_difference_fails(self):
        with self.assertRaises(h.GateError):h.tiny_gate(self.compiler('a'),self.compiler('b',True),self.d/'gate')
    def test_missing_compiler_fails(self):
        with self.assertRaises(h.GateError):h.tiny_gate('missing','missing',self.d/'gate')

class ToolPlanTests(unittest.TestCase):
    def test_bolt_only(self):self.assertEqual(h.tool_plan('[1/2] '+next(x for x in h.BOLT_TASK_DESCRIPTIONS if x.startswith('Building '))+'\n[2/2] Linking CXX executable bin/llvm-bolt\n')['tasks'],2)
    def test_ordinary_compile_stops(self):
        with self.assertRaises(h.GateError):h.tool_plan('[1/1] Building CXX object lib/Support/a.o\n')
    def test_ordinary_link_stops(self):
        with self.assertRaises(h.GateError):h.tool_plan('[1/1] Linking CXX executable bin/clang-22\n')
    def test_empty_unrecognized_stops(self):
        with self.assertRaises(h.GateError):h.tool_plan('')
    def test_no_work(self):
        self.assertEqual(h.tool_plan('ninja: no work to do.\n')['tasks'],0)

class CacheTests(Base):
    def test_only_three_paths_and_flags_change(self):
        got=h.replay_script(EDGE,'out','dep','cache').splitlines()[-1]
        expected=EDGE[5:-5].replace('-o bin/clang-22 ',"-o 'out' ").replace('--dependency-file=tools/clang/tools/driver/CMakeFiles/clang.dir/link.d',"--dependency-file='dep'").replace('--thinlto-cache-dir=/original/cache',"--thinlto-cache-dir='cache'")+' -Wl,--emit-relocs'
        self.assertEqual(got,expected)
    def test_handed_off_cache_is_literal_and_only_two_paths_change(self):
        got=h.replay_script(EDGE,'out','dep').splitlines()[-1]
        expected=EDGE[5:-5].replace('-o bin/clang-22 ',"-o 'out' ").replace('--dependency-file=tools/clang/tools/driver/CMakeFiles/clang.dir/link.d',"--dependency-file='dep'")+' -Wl,--emit-relocs'
        self.assertEqual(got,expected)
    def test_large_cache_copy_not_refused_by_free_space(self):
        cache=self.d/'cache';cache.mkdir()
        fake={'files':[], 'count':47770, 'bytes':98248402280, 'samples':{}}
        with patch.object(h,'cache_manifest',return_value=fake),patch.object(h.shutil,'disk_usage',return_value=type('Disk',(),{'free':1})()),patch.object(h.shutil,'copytree') as copy:
            h.cache_copy('--thinlto-cache-dir='+str(cache),self.d/'copy',self.d/'state.json')
            copy.assert_called_once()
    def test_no_cache(self):
        with self.assertRaises(h.GateError):h.replay_script(EDGE.replace('--thinlto-cache-dir=/original/cache',''),'out','dep','cache')
    def test_duplicate_cache(self):
        with self.assertRaises(h.GateError):h.replay_script(EDGE.replace('driver.o','driver.o --thinlto-cache-dir=/another'),'out','dep','cache')
    def test_original_cache_forbidden(self):
        with self.assertRaises(h.GateError):h.replay_script(EDGE,'out','dep','/original/cache')
    def test_manifest_mutation(self):
        cache=self.d/'cache';cache.mkdir();(cache/'a').write_bytes(b'original');before=h.cache_manifest(cache)
        (cache/'a').write_bytes(b'changed')
        with self.assertRaises(h.GateError):h.cache_unchanged({'source':str(cache),'before':before})
    def test_copy_and_unchanged(self):
        cache=self.d/'cache';cache.mkdir();(cache/'a').write_bytes(b'original')
        with patch.object(h.shutil,'disk_usage',return_value=type('Disk',(),{'free':20*1024**3})()):
            state=h.cache_copy('--thinlto-cache-dir='+str(cache),self.d/'copy',self.d/'copy.json')
        self.assertEqual(state['before'],state['copied']);self.assertTrue(h.cache_unchanged(state))
    def test_cache_copy_has_no_disk_admission(self):
        cache=self.d/'cache';cache.mkdir()
        with patch.object(h.shutil,'disk_usage',return_value=type('Disk',(),{'free':1})()):
            self.assertEqual(h.cache_copy('--thinlto-cache-dir='+str(cache),self.d/'copy',self.d/'copy.json')['copied']['count'],0)

class StripTests(Base):
    def strip(self,argv,log,**kw):
        elf(argv[-1],stripped=True);return ''
    def test_strip_sha_chain(self):
        elf(self.d/'before');tool=self.d/'tool';tool.write_bytes(b'tool')
        with patch.object(h,'call',side_effect=self.strip):
            state=h.strip_all(tool,self.d/'before',self.d/'candidate',self.d/'identity.json')
        self.assertNotEqual(state['before_sha256'],state['after_sha256']);h.validate_identity(state,self.d/'candidate')
    def test_strip_did_not_strip(self):
        elf(self.d/'before');tool=self.d/'tool';tool.write_bytes(b'tool')
        with patch.object(h,'call',return_value=''):
            with self.assertRaises(h.GateError):h.strip_all(tool,self.d/'before',self.d/'candidate',self.d/'identity.json')
    def test_note_absent_before(self):
        elf(self.d/'before',bolt=False)
        with self.assertRaises(h.GateError):h.strip_all('tool',self.d/'before',self.d/'candidate',self.d/'identity.json')

class PackageTests(unittest.TestCase):
    def setup_payload(self):
        self.old={'files':{'main/usr/bin/clang-22':{'type':'file','mode':493,'bytes':3,'sha256':'old'},'main/usr/bin/lld':{'type':'file','mode':493,'bytes':3,'sha256':'lld'},'debuginfo/usr/lib/debug/clang-22.debug':{'type':'file','mode':420,'bytes':3,'sha256':'debug'},'debugsource/usr/src/debug/probe.cc':{'type':'file','mode':420,'bytes':3,'sha256':'source'}}}
        self.new=json.loads(json.dumps(self.old));self.new['files']['main/usr/bin/clang-22']['sha256']='new';self.proof={}
    def parse(self,mode='debug'):return h.package_compare(self.old,self.new,mode,self.proof)
    def remove_debug(self):
        self.proof={'removed':{}}
        for key in list(self.old['files']):
            if key.startswith(('debuginfo/','debugsource/')):
                del self.new['files'][key]
                self.proof['removed'][key]={'baseline':self.old['files'][key], 'kind':'clang_debug' if key.startswith('debuginfo/') else 'exclusive_source', 'evidence':{'owner':'usr/bin/clang-22','clang_debug_sha256':'fixture','dwarf_dump_sha256':'fixture','all_other_debug_manifest_sha256':'fixture','referenced_by':['usr/bin/clang-22'],'source_path':'probe.cc'}}
    def test_debug_content_only(self):self.setup_payload();self.assertTrue(self.parse()['pass'])
    def test_release_content_only(self):self.setup_payload();self.assertTrue(self.parse('release')['pass'])
    def test_debug_proven_omissions(self):self.setup_payload();self.remove_debug();self.assertEqual(len(self.parse()['removed']),2)
    def test_release_omissions_forbidden(self):
        self.setup_payload();self.remove_debug()
        with self.assertRaises(h.GateError):self.parse('release')
    def test_added_file_forbidden(self):
        self.setup_payload();self.new['files']['main/extra']={'type':'file'}
        with self.assertRaises(h.GateError):self.parse()
    def test_nonclang_bytes_forbidden(self):
        self.setup_payload();self.new['files']['main/usr/bin/lld']['sha256']='changed'
        with self.assertRaises(h.GateError):self.parse()
    def test_unproven_missing_forbidden(self):
        self.setup_payload();self.remove_debug();self.proof={}
        with self.assertRaises(h.GateError):self.parse()
    def test_shared_source_forbidden(self):
        self.setup_payload();self.remove_debug();self.proof['removed']['debugsource/usr/src/debug/probe.cc']['evidence']['referenced_by'].append('usr/bin/lld')
        with self.assertRaises(h.GateError):self.parse()
    def test_incomplete_proof_forbidden(self):
        self.setup_payload();self.remove_debug();self.proof['removed']['debuginfo/usr/lib/debug/clang-22.debug']['evidence'].pop('dwarf_dump_sha256')
        with self.assertRaises(h.GateError):self.parse()
    def test_wrong_debug_owner_forbidden(self):
        self.setup_payload();self.remove_debug();self.proof['removed']['debuginfo/usr/lib/debug/clang-22.debug']['evidence']['owner']='lld'
        with self.assertRaises(h.GateError):self.parse()
    def test_debug_buildid_exception(self):
        self.setup_payload();self.remove_debug();k='debuginfo/usr/lib/debug/.build-id/aa/bb.debug';v={'type':'symlink','target':'../../clang-22.debug'};self.old['files'][k]=v
        item=json.loads(json.dumps(self.proof['removed']['debuginfo/usr/lib/debug/clang-22.debug']));item.update(kind='clang_build_id',baseline=v);self.proof['removed'][k]=item
        self.assertTrue(self.parse()['pass'])
    def test_alias_exception(self):
        self.setup_payload();k='main/usr/bin/clang++';v=dict(self.old['files']['main/usr/bin/clang-22']);self.old['files'][k]=v;self.new['files'][k]={'type':'symlink','target':'clang-22'};self.proof={'aliases':[k],'alias_baseline':{k:v}}
        self.assertTrue(self.parse('release')['pass'])

class DiskTests(Base):
    def report(self,free=0,path=None):
        with patch.object(h.shutil,'disk_usage',return_value=type('Disk',(),{'free':free})()):
            return h.disk_report('begin',build=self.d,work=path or self.d/'work')
    def test_zero_free_does_not_reject(self):self.assertEqual(self.report()['free_bytes'],0)
    def test_one_free_does_not_reject(self):self.assertEqual(self.report(1)['free_bytes'],1)
    def test_large_free_records_exact_value(self):self.assertEqual(self.report(41*1024**3)['free_bytes'],41*1024**3)
    def test_no_disk_admission_symbol(self):self.assertFalse(hasattr(h,'disk_preflight'))
    def test_no_stage_budget_symbol(self):self.assertFalse(hasattr(h,'STAGE_WRITE_BUDGET'))
    def test_no_floor_symbol(self):self.assertFalse(hasattr(h,'DISK_FLOOR'))
    def test_records_are_written(self):self.report();self.assertTrue((self.d/'work/disk-begin.json').is_file())
    def test_nonexistent_destination(self):self.assertEqual(self.report(0,self.d/'new'/'work')['free_bytes'],0)

class PipelineTests(Base):
    def run_pipeline(self, failure=None, override=False):
        build=self.d/'build';(build/'bin').mkdir(parents=True)
        (build/'bin/llvm-strip').write_bytes(b'tool');work=self.d/'work';work.mkdir()
        (work/'link.original').write_text(EDGE)
        (work/'installed-baseline.json').write_text('{}')
        (work/'profile.fdata').write_bytes(b'profile');(work/'ordinary-clang-22').write_bytes(b'ordinary')
        events=[]
        def command(argv,log,**kw):
            if argv[0]=='/bin/sh':
                events.append('relink');script=Path(argv[1]).read_text()
                self.assertNotIn('--strip-debug',script);self.assertIn('--emit-relocs',script)
                self.assertIn("--thinlto-cache-dir='copied/cache'" if override else '--thinlto-cache-dir=/original/cache',script)
                elf(work/'reference-relocs-clang-22')
            elif '--strip-debug' in argv:events.append('strip-debug')
            elif '--strip-all' in argv:events.append('strip-all');elf(argv[-1],stripped=True)
            return ''
        def rewrite(tool,profile,input_elf,output,run):
            events.append('rewrite');self.assertEqual(events[:3],['relink','strip-debug','rewrite'])
            if failure=='rewrite':raise h.GateError('matching gate failed')
            elf(output);return {'counts':{'N':100}}
        def tiny(ordinary,candidate,gate,resource):
            label='prestrip' if Path(candidate).name=='clang.bolt' else 'final'
            events.append(label)
            if failure==label:raise h.GateError('tiny gate failed')
            return [{'byte_equal':True}]*3
        with patch.object(h,'call',side_effect=command),patch.object(h,'rewrite',side_effect=rewrite),patch.object(h,'tiny_gate',side_effect=tiny),patch.object(h,'cache_copy',side_effect=AssertionError('no automatic cache copy')),patch.object(h,'security_compare',side_effect=lambda *args,**kw: events.append('security') or {'security_preserved':True}),patch.object(h,'real_gate',side_effect=lambda *args: events.append('real') or {'real_pass':True}),patch.object(h,'adjust_rpath',side_effect=lambda *args: events.append('rpath') or args[-1]):
            if failure:
                with self.assertRaises(h.GateError):h.pipeline(build,work,'fixture-bolt','copied/cache' if override else None)
                if failure in ('rewrite','prestrip'):self.assertNotIn('strip-all',events)
                self.assertFalse((work/'pipeline-result.json').exists());return
            result=h.pipeline(build,work,'fixture-bolt','copied/cache' if override else None)
        self.assertEqual(events,['relink','strip-debug','rewrite','prestrip','real','strip-all','rpath','security','final','real'])
        self.assertEqual(result['identity']['after_sha256'],h.digest(work/'clang.candidate'))
        self.assertFalse((work/'lto-cache').exists());self.assertFalse((work/'strip-equivalence.json').exists())
        return result
    def test_pipeline_has_no_disk_admission(self):
        with patch.object(h.shutil,'disk_usage',return_value=type('Disk',(),{'free':0})()):
            self.assertEqual(self.run_pipeline()['cache_policy'],'original-in-place')
    def test_single_route_original_cache(self):self.assertEqual(self.run_pipeline()['cache_policy'],'original-in-place')
    def test_explicit_copy_override(self):self.assertEqual(self.run_pipeline(override=True)['cache_policy'],'explicit-copy')
    def test_matching_failure_stops(self):self.run_pipeline('rewrite')
    def test_prestrip_tiny_failure_stops(self):self.run_pipeline('prestrip')
    def test_final_tiny_failure_stops(self):self.run_pipeline('final')

if __name__=='__main__':unittest.main(verbosity=2)
