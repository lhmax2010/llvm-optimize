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

EDGE = ': && /bin/clang++ driver.o -Xlinker --dependency-file=tools/clang/tools/driver/CMakeFiles/clang.dir/link.d -o bin/clang-22 -Wl,-rpath,"\\$ORIGIN/../lib64:" libLLVM.a && :'

def log(n=100, m=1000, s=None, u=None, q=None):
    v='BOLT-INFO: %s out of %s functions in the binary (10.0%%) have non-empty execution profile\n' % (n,m)
    if s is not None:v+='BOLT-WARNING: %s (5.0%% of all profiled) functions have invalid (possibly stale) profile. Use -report-stale to see the list.\n' % s
    if u is not None:v+='BOLT-INFO: profile for %s objects was ignored\n' % u
    if q is not None:v+='BOLT-INFO: %s functions with profile could not be optimized\n' % q
    return v

def elf(path, payload=b'\xc3', debug=False, bolt=True, symbols=None, reloc=False):
    names=['','.shstrtab','.text','.strtab','.symtab'] + (['.rela.text'] if reloc else []) + (['.note.bolt_info'] if bolt else []) + (['.debug_info'] if debug else [])
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

class ReplayTests(Base):
    def test_two_flags_and_literal_origin(self):
        s=h.replay_script(EDGE,self.d/'out with space',self.d/'dep');self.assertIn('\\$ORIGIN',s)
        self.assertTrue(s.endswith('-Wl,--emit-relocs -Wl,--strip-debug\n'))
        self.assertEqual(subprocess.run(['/bin/dash','-n'],input=s,text=True).returncode,0)
    def test_reference_no_strip(self):self.assertNotIn('--strip-debug',h.replay_script(EDGE,'out','dep',False))
    def test_missing_output(self):
        with self.assertRaises(h.GateError):h.replay_script(EDGE.replace('-o bin/clang-22 ','-o other '),'out','dep')
    def test_multiline(self):
        with self.assertRaises(h.GateError):h.replay_script(EDGE+'\n'+EDGE,'out','dep')
    def test_duplicate_output(self):
        with self.assertRaises(h.GateError):h.replay_script(EDGE.replace('driver.o','driver.o -o bin/clang-22 '),'out','dep')
    def test_duplicate_dep(self):
        with self.assertRaises(h.GateError):h.replay_script(EDGE.replace('driver.o','driver.o '+EDGE.split('--dependency-file=')[1].split()[0]+' --dependency-file=tools/clang/tools/driver/CMakeFiles/clang.dir/link.d'),'out','dep')
    def test_command_substitution(self):
        with self.assertRaises(h.GateError):h.replay_script(EDGE.replace('driver.o','$(touch x)'),'out','dep')
    def test_semicolon(self):
        with self.assertRaises(h.GateError):h.replay_script(EDGE.replace('driver.o','driver.o; touch x'),'out','dep')
    def test_unescaped_environment(self):
        with self.assertRaises(h.GateError):h.replay_script(EDGE.replace('\\$ORIGIN','$ORIGIN'),'out','dep')
    def test_extra_output(self):
        with self.assertRaises(h.GateError):h.replay_script(EDGE.replace('driver.o','driver.o -Wl,-Map,foo'),'out','dep')

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
    def test_identical_records(self):
        elf(self.d/'a',reloc=True);elf(self.d/'b',reloc=True);self.assertTrue(h.compare_elf(self.d/'a',self.d/'b')['equal'])
    def test_code_difference(self):
        elf(self.d/'a');elf(self.d/'b',payload=b'\x90\xc3');self.assertFalse(h.compare_elf(self.d/'a',self.d/'b')['allocated_equal'])
    def test_symbol_difference(self):
        elf(self.d/'a');elf(self.d/'b',symbols=[(0,0,0,0,0,0),(1,0x12,0,2,0x400101,1)])
        self.assertFalse(h.compare_elf(self.d/'a',self.d/'b')['symbols_equal'])
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

class InstallTests(Base):
    def root(self):
        r=self.d/'root';(r/'usr/bin').mkdir(parents=True);elf(r/'usr/bin/clang-22');return r
    def test_manifest_delta_deletes_every_registered_addition(self):
        r=self.root();before=h.inventory(r);(r/'usr/lib').mkdir();(r/'usr/lib/first.a').write_bytes(b'a');(r/'usr/lib/new-tool').symlink_to('../bin/clang-22')
        result=h.prune_install(r,before,[r/'usr/lib/first.a',r/'usr/lib/new-tool']);self.assertTrue(result['file_list_equal'])
    def test_unknown_addition_stops(self):
        r=self.root();before=h.inventory(r);(r/'usr/bin/unknown').write_bytes(b'x')
        with self.assertRaises(h.GateError):h.prune_install(r,before,[])
    def test_removed_ordinary_file_stops(self):
        r=self.root();before=h.inventory(r);(r/'usr/bin/clang-22').unlink()
        with self.assertRaises(h.GateError):h.prune_install(r,before,[])
    def test_absolute_alias_resolves_inside_root(self):
        r=self.root();(r/'usr/bin/clang').symlink_to('/usr/bin/clang-22')
        self.assertEqual(h.rooted_resolve(r,r/'usr/bin/clang'),r/'usr/bin/clang-22')
    def test_hard_and_soft_aliases_normalized(self):
        r=self.root();os.link(r/'usr/bin/clang-22',r/'usr/bin/clang++');(r/'usr/bin/clang').symlink_to('/usr/bin/clang++')
        elf(self.d/'candidate');state=h.install_candidate(r,self.d/'candidate',self.d/'state.json')
        for name in ['clang','clang++']:self.assertEqual(os.readlink(r/'usr/bin'/name),'clang-22')
        self.assertEqual(len(state['alias_changes']),2)
    def test_old_copy_alias_normalized(self):
        r=self.root();shutil=__import__('shutil');shutil.copyfile(r/'usr/bin/clang-22',r/'usr/bin/clang++');elf(self.d/'candidate')
        h.install_candidate(r,self.d/'candidate',self.d/'state.json');self.assertTrue((r/'usr/bin/clang++').is_symlink())
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
        with self.assertRaises(h.GateError):h.install_candidate(r,self.d/'candidate',self.d/'state.json')
    def test_post_sha_change_stops(self):
        r=self.root();elf(self.d/'candidate');state=h.install_candidate(r,self.d/'candidate',self.d/'state.json');(r/'usr/bin/clang-22').write_bytes(b'changed')
        with self.assertRaises(h.GateError):h.post_gate(r,state,'unused',self.d/'gate')
    def test_post_stale_alias_stops(self):
        r=self.root();(r/'usr/bin/clang').symlink_to('clang-22');elf(self.d/'candidate');state=h.install_candidate(r,self.d/'candidate',self.d/'state.json');(r/'usr/bin/clang').unlink();(r/'usr/bin/clang').symlink_to('/usr/bin/clang-22')
        with self.assertRaises(h.GateError):h.post_gate(r,state,'unused',self.d/'gate')
    def test_final_manifest_cannot_hide_debug_file_difference(self):
        r=self.root();before=h.inventory(r);(r/'usr/lib').mkdir();(r/'usr/lib/clang.debug').write_bytes(b'bad')
        elf(self.d/'candidate');state=h.install_candidate(r,self.d/'candidate',self.d/'state.json')
        with self.assertRaises(h.GateError):h.post_gate(r,state,'unused',self.d/'gate',before)
    def test_post_with_fixed_fixture_compiler(self):
        r=self.root();before=h.inventory(r);elf(self.d/'candidate');state=h.install_candidate(r,self.d/'candidate',self.d/'state.json')
        with patch.object(h,'tiny_gate',return_value=[{'byte_equal':True}]):
            result=h.post_gate(r,state,'fixture',self.d/'gate',before)
        self.assertTrue(result['ordinary_manifest_checked'])

class TinyTests(Base):
    def compiler(self,name,mismatch=False):
        p=self.d/name;p.write_text('#!/usr/bin/env python3\nimport sys\nfrom pathlib import Path\nif "--version" in sys.argv: print("fixture clang");sys.exit(0)\ntriple=next(x for x in sys.argv if x.startswith("--target="))\nPath(sys.argv[sys.argv.index("-o")+1]).write_bytes((triple'+(' + "mismatch"' if mismatch else '')+').encode())\n');p.chmod(0o755);return str(p)
    def test_three_targets_complete_bytes(self):self.assertEqual(len(h.tiny_gate(self.compiler('a'),self.compiler('b'),self.d/'gate')),3)
    def test_difference_fails(self):
        with self.assertRaises(h.GateError):h.tiny_gate(self.compiler('a'),self.compiler('b',True),self.d/'gate')
    def test_missing_compiler_fails(self):
        with self.assertRaises(OSError):h.tiny_gate('missing','missing',self.d/'gate')

class ToolPlanTests(unittest.TestCase):
    def test_bolt_only(self):self.assertEqual(h.tool_plan('[1/2] Building CXX object tools/bolt/Core/a.o\n[2/2] Linking CXX executable bin/llvm-bolt\n')['tasks'],2)
    def test_ordinary_compile_stops(self):
        with self.assertRaises(h.GateError):h.tool_plan('[1/1] Building CXX object lib/Support/a.o\n')
    def test_ordinary_link_stops(self):
        with self.assertRaises(h.GateError):h.tool_plan('[1/1] Linking CXX executable bin/clang-22\n')
    def test_empty_unrecognized_stops(self):
        with self.assertRaises(h.GateError):h.tool_plan('')
    def test_no_work(self):self.assertEqual(h.tool_plan('ninja: no work to do.\n')['tasks'],0)

class DebugOwnershipTests(Base):
    def test_remove_owned_debug_only(self):
        r=self.d/'root';d=r/'usr/lib/debug/usr/bin';d.mkdir(parents=True)
        (d/'clang-22.debug').write_bytes(b'old');(d/'lld.debug').write_bytes(b'keep')
        state={'allowed_paths':['usr/bin/clang-22']}
        h.remove_clang_debug(r,state);self.assertFalse((d/'clang-22.debug').exists());self.assertTrue((d/'lld.debug').exists())

if __name__=='__main__':unittest.main(verbosity=2)
