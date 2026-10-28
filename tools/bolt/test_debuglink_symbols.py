"""Function-symbol packaging gates, using synthetic ELFs and real objcopy I/O."""
import copy
import json
import shutil
import struct
import subprocess
from pathlib import Path
from unittest.mock import patch
import bolt_helper as h
from test_bolt_helper import Base, elf

class DebuglinkTests(Base):
    def setup_link(self):
        self.before=self.d/'before';src=self.d/'probe.c';src.write_text('int main(void) { return 0; }\n')
        self.objcopy=shutil.which('objcopy');self.assertIsNotNone(self.objcopy)
        subprocess.run(['cc',str(src),'-o',str(self.before)],check=True,capture_output=True)
        note=self.d/'bolt-note';note.write_bytes(b'BOLT')
        subprocess.run([self.objcopy,'--add-section=.note.bolt_info='+str(note),str(self.before)],check=True,capture_output=True)
        self.debug=self.d/'clang-22.debug';shutil.copyfile(self.before,self.debug)
        self.candidate=self.d/'candidate';shutil.copyfile(self.before,self.candidate)
        subprocess.run([self.objcopy,'--strip-all','--remove-section=.note.bolt_info',str(self.candidate)],check=True,capture_output=True)
        self.objcopy=shutil.which('objcopy');self.assertIsNotNone(self.objcopy)
        self.layout=h.debuglink_layout(self.candidate)
        subprocess.run([self.objcopy,'--add-gnu-debuglink='+str(self.debug),str(self.candidate)],check=True,capture_output=True)
        self.identity={'before_path':str(self.before),'before_sha256':h.digest(self.before),'bolt_note_before':True,
                       'after_sha256':h.digest(self.candidate),'debuglink_sha256':h.digest(self.candidate),
                       'debug_file':{'path':str(self.debug),'sha256':h.digest(self.debug),'bytes':self.debug.stat().st_size,'crc32':h.debug_crc(self.debug)},
                       'debuglink':{'filename':'clang-22.debug','crc32':h.debug_crc(self.debug)}}
    def test_debuglink_and_final_identity(self):
        self.setup_link();h.validate_identity(self.identity,self.candidate)
        self.assertEqual(h.verify_debuglink(self.candidate,self.debug,h.debug_crc(self.debug))['filename'],'clang-22.debug')
    def test_missing_debug(self):
        self.setup_link();self.debug.unlink()
        with self.assertRaisesRegex(h.GateError,'missing'):h.validate_identity(self.identity,self.candidate)
    def test_changed_debug(self):
        self.setup_link();self.debug.write_bytes(self.debug.read_bytes()+b'x')
        with self.assertRaisesRegex(h.GateError,'SHA/size'):h.validate_identity(self.identity,self.candidate)
    def test_wrong_crc(self):
        self.setup_link()
        with self.assertRaisesRegex(h.GateError,'CRC'):h.verify_debuglink(self.candidate,self.debug,h.debug_crc(self.debug)^1)
    def test_wrong_basename(self):
        self.setup_link();p=self.d/'other.debug';shutil.copyfile(self.debug,p)
        subprocess.run([self.objcopy,'--remove-section=.gnu_debuglink','--add-gnu-debuglink='+str(p),str(self.candidate)],check=True,capture_output=True)
        with self.assertRaisesRegex(h.GateError,'basename'):h.verify_debuglink(self.candidate,self.debug,h.debug_crc(self.debug))
    def test_missing_link(self):
        self.setup_link();elf(self.candidate,stripped=True)
        with self.assertRaisesRegex(h.GateError,'missing'):h.verify_debuglink(self.candidate,self.debug,h.debug_crc(self.debug))
    def test_unproven_link(self):
        self.setup_link();del self.identity['debug_file']
        with self.assertRaisesRegex(h.GateError,'unproven'):h.validate_identity(self.identity,self.candidate)
    def test_debug_elf_sections_only(self):
        self.before=self.d/'before';elf(self.before)
        data=bytearray(self.before.read_bytes());struct.pack_into('<Q',data,64+8,len(data)+4096);self.before.write_bytes(data)
        with self.assertRaises(h.GateError):h.ELF(self.before)
        self.assertEqual(len(h.symbol_records(self.before)),2)
    def test_missing_symtab(self):
        p=self.d/'stripped';elf(p,stripped=True)
        with self.assertRaisesRegex(h.GateError,'symtab'):h.symbol_records(p)
    def test_symtab_mismatch(self):
        a=self.d/'a';b=self.d/'b';elf(a);elf(b,payload=b'abc')
        with self.assertRaisesRegex(h.GateError,'symtab count'):h.verify_debug_symbols(a,b,'symbolizer',self.d)
    def functions(self):
        return [('main',18,0,'.text',0x1000,10)]+[(f'fn{i}.cold.1' if i<5 else f'fn{i}',18,0,'.text',0x2000+16*i,10) for i in range(24)]
    def symbols(self,broken=False):
        rows=self.functions()
        def call(argv,log,**kw):
            names={hex(row[4]):row[0] for row in rows}
            Path(log).write_text(''.join(('??' if broken else names[x])+'\n??:0:0\n\n' for x in argv[4:]))
        with patch.object(h,'symbol_records',return_value=rows),patch.object(h,'call',side_effect=call):
            return h.verify_debug_symbols('before','debug','symbolizer',self.d)
    def test_24_symbols_main_and_cold(self):
        result=self.symbols();self.assertEqual(len(result['samples']),24)
        self.assertEqual(result['samples'][0]['resolved_name'],'main');self.assertGreaterEqual(result['cold_function_count'],3)
    def test_symbolizer_failure(self):
        with self.assertRaisesRegex(h.GateError,'lookup failed'):self.symbols(True)
    def test_incomplete_symbolizer_output(self):
        def call(args,log,**kw):Path(log).write_text('main\n??:0\n\n')
        with patch.object(h,'symbol_records',return_value=self.functions()),patch.object(h,'call',side_effect=call),self.assertRaisesRegex(h.GateError,'every debug address'):
            h.verify_debug_symbols('before','debug','symbolizer',self.d)
    def test_loaded_content_change_detected(self):
        self.setup_link();before=h.debuglink_layout(self.candidate)
        e=h.ELF(self.candidate);off=e.by_name['.text'][4];e.close()
        data=bytearray(self.candidate.read_bytes());data[off]^=1;self.candidate.write_bytes(data)
        self.assertNotEqual(h.debuglink_layout(self.candidate),before)
    def test_add_debuglink_rejects_layout_change(self):
        self.setup_link();work=self.d/'work';work.mkdir();shutil.copyfile(self.candidate,work/'clang.candidate');shutil.copyfile(self.debug,work/'clang-22.debug')
        # Candidate must start without the link; injected layout difference
        # models an objcopy modifying program headers or loaded section content.
        elf(work/'clang.candidate',stripped=True)
        with patch.object(h,'debuglink_layout',side_effect=[{'loaded':1},{'loaded':2}]),patch.object(h,'call'),self.assertRaisesRegex(h.GateError,'program headers'):
            h.add_debuglink(self.d,work,self.identity,self.identity['debug_file'])
    def installed(self):
        self.setup_link();root=self.d/'root';(root/'usr/bin').mkdir(parents=True);elf(root/'usr/bin/clang-22',bolt=False)
        state=h.install_candidate(root,self.candidate,self.d/'state.json',self.identity)
        self.assertEqual((root/h.DEBUG_INSTALL_PATH).stat().st_mode&0o777,0o644)
        self.assertEqual(h.digest(root/h.DEBUG_INSTALL_PATH),h.digest(self.debug))
        self.assertIn(h.DEBUG_INSTALL_PATH,state['allowed_paths'])
        return root,state
    def test_atomic_install_symbols(self):self.installed()
    def test_install_write_failure_keeps_clang(self):
        self.setup_link();root=self.d/'root';(root/'usr/bin').mkdir(parents=True);entity=root/'usr/bin/clang-22';elf(entity,bolt=False);old=h.digest(entity);real=h.shutil.copyfile
        def copy(src,dst):
            if str(dst).endswith('.debug.bolt-new'):raise OSError(28,'No space left on device')
            return real(src,dst)
        with patch.object(h.shutil,'copyfile',side_effect=copy),self.assertRaises(OSError):h.install_candidate(root,self.candidate,self.d/'state.json',self.identity)
        self.assertEqual(h.digest(entity),old)
    def post(self,root,state):
        with patch.object(h,'security_compare',return_value={}),patch.object(h,'installed_security',return_value={}),patch.object(h,'tiny_gate',return_value=[]),patch.object(h,'real_gate',return_value={}):
            return h.post_gate(root,state,self.d/'ordinary',self.d/'post')
    def test_post_debug_identity(self):
        root,state=self.installed();r=self.post(root,state);self.assertIn('SHAs unchanged',r['debug']['find_debuginfo_skip_basis'])
    def test_post_missing_debug(self):
        root,state=self.installed();(root/h.DEBUG_INSTALL_PATH).unlink()
        with self.assertRaisesRegex(h.GateError,'missing'):self.post(root,state)
    def test_post_changed_debug(self):
        root,state=self.installed();(root/h.DEBUG_INSTALL_PATH).write_bytes(b'changed')
        with self.assertRaisesRegex(h.GateError,'SHA/size'):self.post(root,state)
    def test_post_wrong_debug_mode(self):
        root,state=self.installed();(root/h.DEBUG_INSTALL_PATH).chmod(0o755)
        with self.assertRaisesRegex(h.GateError,'mode'):self.post(root,state)
    def test_install_existing_debug_rejected(self):
        root,state=self.installed()
        with self.assertRaisesRegex(h.GateError,'already exists'):h.install_candidate(root,self.candidate,self.d/'state2.json',self.identity)
    def test_compare_root_still_rejects_early_debug_install(self):
        root=self.d/'root';root.mkdir();snap=h.root_snapshot(root);(root/'unexpected').write_text('symbols')
        with self.assertRaisesRegex(h.GateError,'added'):h.compare_root(root,snap,self.d/'after.json')

class DebugPackageTests(Base):
    def setup_package(self):
        entity={'type':'file','mode':0o755,'bytes':5,'sha256':'clang'}
        self.old={'files':{'main/usr/bin/clang-22':entity}}
        self.new=copy.deepcopy(self.old);key='debuginfo/'+h.DEBUG_INSTALL_PATH
        self.new['files'][key]={'type':'file','mode':0o644,'bytes':10,'sha256':'symbols'}
        self.proof={'debug_file':{'candidate_sha256':'clang','bytes':10,'sha256':'symbols','crc32':1234}}
    def test_only_standard_debug_file_allowed(self):
        self.setup_package();self.assertTrue(h.package_compare(self.old,self.new,'debug',self.proof)['pass'])
    def test_unproven_debug_file(self):
        self.setup_package()
        with self.assertRaisesRegex(h.GateError,'added'):h.package_compare(self.old,self.new,'debug',{})
    def test_wrong_debug_sha(self):
        self.setup_package();self.proof['debug_file']['sha256']='wrong'
        with self.assertRaisesRegex(h.GateError,'bound'):h.package_compare(self.old,self.new,'debug',self.proof)
    def test_other_new_file_rejected(self):
        self.setup_package();self.new['files']['debuginfo/extra']={'type':'file'}
        with self.assertRaisesRegex(h.GateError,'added'):h.package_compare(self.old,self.new,'debug',self.proof)
    def test_release_does_not_allow_debugfile(self):
        self.setup_package()
        with self.assertRaisesRegex(h.GateError,'debug package mode'):h.package_compare(self.old,self.new,'release',self.proof)
