"""Second review: independent Ninja evidence and fail-closed negative cases."""
import json,os,shutil,signal,struct,subprocess,sys,time,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import bolt_helper as h
from test_bolt_helper import Base,EDGE
from test_security_properties import security_elf

RESULTS=Path(__file__).parent/'results'
DESCRIPTIONS=json.loads((RESULTS/'review-tool-descriptions.json').read_text())
LINK='Linking CXX executable bin/llvm-bolt'
TF=['Building C object lib64/tf_runtime/CMakeFiles/tf_xla_runtime.dir/tf_xla_runtime_dummy.c.o',
    'Linking C static library lib64/libtf_xla_runtime.a']
def plan_text(rows):return '\n'.join('[%d/%d] %s'%(i+1,len(rows),s) for i,s in enumerate(rows))

class SecondPlanTests(unittest.TestCase):
    def rejected(self,text):
        with self.assertRaises(h.GateError):h.tool_plan(text)
    def test_up_to_date(self):self.assertEqual(h.tool_plan('ninja: no work to do.')['plan_type'],'up-to-date')
    def test_trailing_blank(self):self.assertEqual(h.tool_plan('ninja: no work to do.\n\n  \n')['tasks'],0)
    def test_up_to_date_mixed(self):self.rejected('ninja: no work to do.\n[1/1] '+LINK)
    def test_other_ninja_message(self):self.rejected('ninja: interrupted by user.')
    def test_regeneration_specific(self):
        for f in (0,1):
            with self.subTest(f=f),self.assertRaisesRegex(h.GateError,'build.ninja still needs regeneration'):
                h.tool_plan('[%d/1] Re-running CMake...'%f)
    def test_truncated(self):self.rejected('[1/2] '+LINK)
    def test_skip(self):self.rejected('[2/1] '+LINK)
    def test_wrong_total(self):self.rejected('[1/9] '+LINK)
    def test_duplicate(self):self.rejected(plan_text([LINK,LINK]))
    def test_stderr_warning(self):self.assertEqual(h.tool_plan('ninja: warning: bad\n[1/1] '+LINK)['ninja_diagnostics'], ['ninja: warning: bad'])
    def test_leading_blank(self):self.rejected('\n[1/1] '+LINK)
    def test_tf_pair(self):
        p=h.tool_plan(plan_text(TF+DESCRIPTIONS))
        self.assertEqual(p['tasks'],112);self.assertEqual(p['configuration_refresh_tasks'],2)
        self.assertEqual(sum(p['categories'].values())+2,112)
        self.assertNotIn('ordinary_compile_link_tasks',p)
    def test_tf_single(self):
        for row in TF:self.rejected(plan_text([row,LINK]))
    def test_ordinary_consistent_count(self):self.rejected(plan_text(['Building CXX object lib/Support/a.o',LINK]))
    def test_historical_raw_rejected(self):
        # Historical collector prefixes and runtime/merge-fdata options differ.
        raw=(RESULTS/'review2-historical-dry-run.txt').read_text()
        self.rejected(raw)
        normalized='\n'.join(s.split(' ',1)[1] for s in raw.splitlines() if ' [' in s)
        self.rejected(normalized)
    def test_real_toy_fixtures(self):
        self.assertEqual(h.tool_plan((RESULTS/'review2-toy-up-to-date.combined.txt').read_text())['tasks'],0)
        with self.assertRaisesRegex(h.GateError,'build.ninja still needs regeneration'):
            h.tool_plan((RESULTS/'review2-toy-rerun.combined.txt').read_text())
        self.rejected((RESULTS/'review2-toy-write-rerun.combined.txt').read_text())

class SecondBuildTests(Base):
    def setup_build(self,tf=False):
        (self.d/'bin').mkdir();p=self.d/'bin/llvm-bolt';p.write_text('tool');p.chmod(0o755)
        (self.d/'lib64').mkdir();(self.d/'lib64/libtf_xla_runtime.a').write_bytes(b'archive')
        source=self.d/'libtf_xla_runtime_prebuilt.a';source.write_bytes(b'archive')
        (self.d/'build.ninja').write_text('build lib64/libtf_xla_runtime.a: C_STATIC_LIBRARY_LINKER a.o\n  POST_BUILD = cp '+str(source)+' lib64/libtf_xla_runtime.a\n')
        p=h.tool_plan(plan_text((TF if tf else [])+[LINK]));s=h.tool_prepare(self.d,p,self.d/'before.json')
        return p,s
    def test_warnings_and_restat(self):
        p,s=self.setup_build(True)
        text='[1/5] '+TF[0]+'\ncompiler: warning: fixture\n[2/3] '+TF[1]+'\n[3/3] '+LINK
        self.assertEqual(h.tool_verify(self.d,p,text+'\n'+h.BUILD_SUCCESS,s)['tasks'],3)
        self.assertTrue(s['prebuilt_evidence']['archive_equal'])
    def test_task_outside_plan(self):
        p,s=self.setup_build()
        with self.assertRaises(h.GateError):h.tool_verify(self.d,p,'[1/1] '+TF[0]+'\n'+h.BUILD_SUCCESS,s)
    def test_duplicate(self):
        p,s=self.setup_build()
        with self.assertRaises(h.GateError):h.tool_verify(self.d,p,plan_text([LINK,LINK])+'\n'+h.BUILD_SUCCESS,s)
    def test_up_to_date_progress(self):
        p,s=self.setup_build();p=h.tool_plan('ninja: no work to do.')
        with self.assertRaises(h.GateError):h.tool_verify(self.d,p,'[1/1] '+LINK+'\n'+h.BUILD_SUCCESS,s)
    def test_archive_changed(self):
        p,s=self.setup_build(True);(self.d/'lib64/libtf_xla_runtime.a').write_bytes(b'changed')
        with self.assertRaisesRegex(h.GateError,'TF archive SHA changed'):h.tool_verify(self.d,p,plan_text(TF+[LINK])+'\n'+h.BUILD_SUCCESS,s)
    def test_archive_missing(self):
        p,s=self.setup_build(True);(self.d/'lib64/libtf_xla_runtime.a').unlink()
        with self.assertRaises(h.GateError):h.tool_verify(self.d,p,plan_text(TF+[LINK])+'\n'+h.BUILD_SUCCESS,s)
    def test_executable_symlink(self):
        p,s=self.setup_build();exe=self.d/'bin/llvm-bolt';exe.rename(exe.with_name('other'));exe.symlink_to('other')
        with self.assertRaises(h.GateError):h.tool_verify(self.d,p,'[1/1] '+LINK+'\n'+h.BUILD_SUCCESS,s)
    def test_discontinuous_progress(self):
        p,s=self.setup_build()
        with self.assertRaises(h.GateError):h.tool_verify(self.d,p,'[2/2] '+LINK+'\n'+h.BUILD_SUCCESS,s)

class SecondProcessTests(Base):
    def test_wait_deadline_stubborn(self):
        with patch.object(h,'live_group_members',return_value=[(424242,'R')]),patch.object(h.time,'monotonic',side_effect=[0,11]):
            with self.assertRaisesRegex(h.GateError,'424242:R'):h.wait_group_exit(42)
    def test_reap_deadline_stubborn(self):
        with patch.object(os,'waitpid',return_value=(0,0)),patch.object(h.time,'monotonic',side_effect=[0,2]):
            with self.assertRaisesRegex(h.GateError,'leader 424242'):h.reap_child(SimpleNamespace(pid=424242))
    def test_nonzero_live_grandchild(self):
        pidfile=self.d/'pid'
        code='import os,subprocess,sys\np=subprocess.Popen([sys.executable,"-c","import time;time.sleep(60)"])\nopen('+repr(str(pidfile))+',"w").write(str(p.pid))\nsys.exit(7)'
        with self.assertRaisesRegex(h.GateError,'^COMMAND_FAILED rc=7:'):
            h.call([sys.executable,'-c',code],self.d/'nonzero.log')
        pid=int(pidfile.read_text())
        try:self.assertIn(h.proc_stat('/proc/%d/stat'%pid)[1],('Z','X'))
        except FileNotFoundError:pass
    def test_success_log_read_failure_does_not_kill(self):
        real=Path.read_text
        def read(p,*a,**kw):
            if p==self.d/'log':raise OSError('read failure')
            return real(p,*a,**kw)
        with patch.object(Path,'read_text',read),patch.object(os,'killpg') as kill,self.assertRaisesRegex(h.GateError,'^COMMAND_ERROR.*read failure'):
            try:h.call(['/bin/sh','-c','exit 0'],self.d/'log')
            finally:kill.assert_not_called()
    def test_proc_enumeration_error(self):
        with patch.object(os,'scandir',side_effect=PermissionError('denied')),self.assertRaisesRegex(h.GateError,'cannot enumerate/read'):h.live_group_members(42)
    def test_self_pid_mismatch(self):
        with patch.object(h,'proc_stat',return_value=(os.getpid()+1,'R',42,1)),self.assertRaisesRegex(h.GateError,'PID namespace mismatch'):h.live_group_members(42)
    def scan(self,state,threads,error=None):
        real=h.proc_stat
        def stat(p):
            if p=='/proc/self/stat':return real(p)
            if error:raise error
            return 424242,state,42,threads
        entries=unittest.mock.MagicMock();entries.__enter__.return_value=iter([SimpleNamespace(name='424242')])
        with patch.object(os,'scandir',return_value=entries),patch.object(h,'proc_stat',stat):return h.live_group_members(42)
    def test_disappeared_process(self):self.assertEqual(self.scan('R',1,FileNotFoundError()),[])
    def test_process_permission_error(self):
        with self.assertRaises(h.GateError):self.scan('R',1,PermissionError('denied'))
    def test_zombie_threads(self):self.assertEqual(self.scan('Z',2),[(424242,'Z')])
    def test_single_zombie(self):self.assertEqual(self.scan('Z',1),[])
    def test_sigchld_ignored(self):
        previous=signal.getsignal(signal.SIGCHLD)
        try:
            signal.signal(signal.SIGCHLD,signal.SIG_IGN)
            with self.assertRaisesRegex(h.GateError,'^COMMAND_FAILED rc=7:'):h.call(['/bin/sh','-c','exit 7'],self.d/'ignored.log')
            self.assertEqual(signal.getsignal(signal.SIGCHLD),signal.SIG_DFL)
            self.assertTrue(json.loads((self.d/'ignored.log.argv.json').read_text())['SIGCHLD_reset_to_default'])
        finally:signal.signal(signal.SIGCHLD,previous)
    def test_original_error_before_cleanup(self):
        with patch.object(h,'peek_child_exit',side_effect=OSError('ORIGINAL')),patch.object(h,'wait_group_exit',side_effect=h.GateError('CLEANUP')):
            with self.assertRaisesRegex(h.GateError,'^COMMAND_ERROR: ORIGINAL.*cleanup error: CLEANUP'):h.call(['/bin/sh','-c','sleep 60'],self.d/'order.log')
    def test_base_exceptions_preserved(self):
        for error in (KeyboardInterrupt(),SystemExit(31)):
            with self.subTest(error=type(error).__name__),patch.object(h,'peek_child_exit',side_effect=error),self.assertRaises(type(error)) as caught:
                h.call(['/bin/sh','-c','sleep 60'],self.d/'base.log')
            self.assertIs(caught.exception,error)

class SecondSecurityTests(Base):
    def pair(self):
        a=self.d/'a';b=self.d/'b';security_elf(a);shutil.copyfile(a,b);return a,b
    def edit_symbol(self,offset,fmt,value):
        a,b=self.pair();e=h.ELF(b)
        try:pos=e.by_name['.dynsym'][4]+24+offset
        finally:e.close()
        data=bytearray(b.read_bytes());struct.pack_into(fmt,data,pos,value);b.write_bytes(data)
        return a,b
    def test_undefined_only(self):
        with self.assertRaisesRegex(h.GateError,'dynsym'):h.security_compare(*self.edit_symbol(6,'<H',0))
    def test_type_only(self):
        with self.assertRaisesRegex(h.GateError,'dynsym'):h.security_compare(*self.edit_symbol(4,'<B',0x11))
    def test_symbol_addresses_ignored(self):self.assertTrue(h.security_compare(*self.edit_symbol(8,'<Q',0x777777))['security_preserved'])
    def test_code_section_name_ignored(self):
        a,b=self.pair();data=b.read_bytes().replace(b'.text\0',b'.code\0');b.write_bytes(data)
        self.assertTrue(h.security_compare(a,b)['security_preserved'])
    def test_wx_load(self):
        a,b=self.pair();data=bytearray(b.read_bytes());struct.pack_into('<I',data,68,7);b.write_bytes(data)
        with self.assertRaisesRegex(h.GateError,'W_X_LOAD'):h.security_compare(a,b)
    def test_bind_now_removed(self):
        a,b=self.pair();e=h.ELF(a)
        try:pos=e.by_name['.dynamic'][4]
        finally:e.close()
        data=bytearray(a.read_bytes());struct.pack_into('<qQ',data,pos+16,24,0);a.write_bytes(data)
        data=bytearray(data);struct.pack_into('<qQ',data,pos+16,21,0);b.write_bytes(data)
        with self.assertRaisesRegex(h.GateError,'DT_BIND_NOW'):h.security_compare(a,b)
    def test_nobits_metadata(self):
        a,b=self.pair();e=h.ELF(b)
        try:index=e.names.index('.note.gnu.property')
        finally:e.close()
        data=bytearray(b.read_bytes());sh=struct.unpack_from('<Q',data,40)[0];struct.pack_into('<I',data,sh+index*64+4,8);b.write_bytes(data)
        with self.assertRaisesRegex(h.GateError,'NOBITS'):h.security_properties(b)
    def test_same_version_name_different_provider(self):
        a,b=self.pair();e=h.ELF(a)
        try:
            headers=list(e.sections);names=list(e.names)
            sec=e.by_name['.dynstr'];strings=bytes(e.mm[sec[4]:sec[4]+sec[5]])
            sec=e.by_name['.dynsym'];symbols=bytes(e.mm[sec[4]:sec[4]+sec[5]])
        finally:e.close()
        provider=len(strings);strings+=b'libother.so\0';symname=len(strings);strings+=b'other_symbol\0'
        symbols+=struct.pack('<IBBHQQ',symname,0x12,0,2,0x400100,1)
        version=strings.index(b'GLIBC');libc=strings.index(b'libc')
        needs=(struct.pack('<HHIII',1,1,libc,16,32)+struct.pack('<IHHII',0,0,2,version,0)+
               struct.pack('<HHIII',1,1,provider,16,0)+struct.pack('<IHHII',0,0,3,version,0))
        data=bytearray(a.read_bytes())
        for name,blob in [('.dynstr',strings),('.dynsym',symbols),('.gnu.version',struct.pack('<HHH',0,2,3)),('.gnu.version_r',needs)]:
            i=names.index(name);row=list(headers[i]);row[4]=len(data);row[5]=len(blob);headers[i]=tuple(row);data.extend(blob)
        shoff=len(data)
        for row in headers:data.extend(struct.pack('<IIQQQQIIQQ',*row))
        struct.pack_into('<Q',data,40,shoff);a.write_bytes(data)
        vers=headers[names.index('.gnu.version')][4];struct.pack_into('<HH',data,vers+2,3,2);b.write_bytes(data)
        self.assertEqual(h.security_properties(a)['.gnu.version_r'],h.security_properties(b)['.gnu.version_r'])
        with self.assertRaisesRegex(h.GateError,'gnu.version'):h.security_compare(a,b)
    def relro(self,field,value):
        source=self.d/'relro.c';source.write_text('int exported=1; int main(void){return exported;}\n')
        a=self.d/'ordinary';b=self.d/'mutated'
        subprocess.run(['/usr/bin/cc','-Wl,-z,relro,-z,now',str(source),'-o',str(a)],check=True,capture_output=True)
        data=bytearray(a.read_bytes());off=struct.unpack_from('<Q',data,32)[0];n=struct.unpack_from('<H',data,56)[0]
        pos=next(off+i*56 for i in range(n) if struct.unpack_from('<I',data,off+i*56)[0]==0x6474e552)
        old=struct.unpack_from('<Q',data,pos+field)[0];struct.pack_into('<Q',data,pos+field,value(old));b.write_bytes(data)
        with self.assertRaisesRegex(h.GateError,'RELRO'):h.security_compare(a,b)
    def test_relro_moved(self):self.relro(16,lambda x:x+8)
    def test_relro_shrunk(self):self.relro(32,lambda x:x-8)
    def test_relro_zeroed(self):self.relro(32,lambda x:0)
    def test_relro_invalid_size(self):self.relro(40,lambda x:0)

class SecondReverseTests(Base):
    def test_unrelated_bolt_word_and_path(self):
        p=self.d/'bolt/C.cmake';p.parent.mkdir();p.write_text('set(project Thunderbolt) # bolt BOLT')
        with patch.object(h,'digest',side_effect=AssertionError('no hashes in reverse check')):self.assertTrue(h.no_bolt_products(self.d)['no_bolt_products'])
    def test_tokens_reported(self):
        p=self.d/'a.cmake'
        for token in ('LLVMBOLTCore','perf2bolt'):
            p.write_text(token)
            with self.subTest(token=token),self.assertRaisesRegex(h.GateError,'a.cmake matched '+('LLVMBOLT' if token=='LLVMBOLTCore' else token)):h.no_bolt_products(self.d)
    def test_rooted_absolute_link(self):
        (self.d/'target').write_text('ok');(self.d/'link').symlink_to('/target')
        self.assertTrue(h.no_bolt_products(self.d)['no_bolt_products'])
    def test_dangling(self):
        (self.d/'link.cmake').symlink_to('missing')
        with self.assertRaisesRegex(h.GateError,'dangling'):h.no_bolt_products(self.d)
    def test_permission_error(self):
        with patch.object(os,'scandir',side_effect=PermissionError('forced')),self.assertRaisesRegex(h.GateError,'inventory traversal failed'):h.no_bolt_products(self.d)
    def test_special_file(self):
        os.mkfifo(self.d/'fifo')
        with self.assertRaisesRegex(h.GateError,'special file'):h.no_bolt_products(self.d)
    def test_response_file_rejected(self):
        edge=EDGE.replace('driver.o','@driver.rsp')
        with self.assertRaisesRegex(h.GateError,'link edge uses a response file; rsp auditing is not implemented'):h.replay_script(edge,'out','dep')

if __name__=='__main__':unittest.main()
