import json,os,signal,struct,subprocess,sys,time,unittest
from pathlib import Path
from unittest.mock import patch
import bolt_helper as h
from test_bolt_helper import Base,elf

class ProcessGroupTests(Base):
    def test_timeout_kills_descendants_and_heartbeat(self):
        heartbeat=self.d/'heartbeat';pids=self.d/'pids'
        grand=self.d/'grand.py';grand.write_text('import os,time\nfrom pathlib import Path\np=Path('+repr(str(pids))+')\np.open("a").write(str(os.getpid())+"\\n")\nwhile True:\n Path('+repr(str(heartbeat))+').open("a").write("beat\\n")\n time.sleep(.03)\n')
        child=self.d/'child.py';child.write_text('import os,subprocess,sys\nfrom pathlib import Path\nPath('+repr(str(pids))+').open("a").write(str(os.getpid())+"\\n")\nsubprocess.run([sys.executable,'+repr(str(grand))+'])\n')
        script=self.d/'start.sh';script.write_text('echo $$ >> '+h.quote(pids)+'\n'+h.quote(sys.executable)+' '+h.quote(child)+'\n')
        with self.assertRaisesRegex(h.GateError,'TIMEOUT.*see'):
            h.call(['/bin/sh',str(script)],self.d/'timeout.log',timeout=1)
        ids=list(map(int,pids.read_text().split()));self.assertEqual(len(ids),3)
        deadline=time.monotonic()+10
        while True:
            live=[]
            for pid in ids:
                status=Path('/proc')/str(pid)/'stat'
                try:state=status.read_text().rsplit(')',1)[1].split()[0]
                except FileNotFoundError:state=None
                if state not in (None,'Z','X'):live.append((pid,state))
            if not live:break
            self.assertLess(time.monotonic(),deadline,str(live));time.sleep(.02)
        size=heartbeat.stat().st_size;time.sleep(.15);self.assertEqual(heartbeat.stat().st_size,size)
    def test_stubborn_member_reports_pid_and_original_error(self):
        with patch.object(h,'live_group_members',return_value=[(424242,'R')]),patch.object(h.time,'monotonic',side_effect=[0,11]):
            with self.assertRaisesRegex(h.GateError,r'424242:R.*original error.*see'):
                h.call(['/bin/sh','-c','exit 7'],self.d/'stubborn.log')
    def test_zombie_and_absent_group_exit(self):
        with patch.object(h,'live_group_members',return_value=[]):h.wait_group_exit(424242)
    def test_exception_kills_group_and_reports_log(self):
        real_wait=subprocess.Popen.wait;calls=[]
        def wait(p,*a,**kw):
            if not calls:calls.append(1);raise OSError('injected wait error')
            return real_wait(p,*a,**kw)
        with patch.object(subprocess.Popen,'wait',wait),self.assertRaisesRegex(h.GateError,'injected wait error.*see'):
            h.call(['/bin/sh','-c','sleep 60'],self.d/'exception.log')

class ReviewTinyTests(Base):
    def compiler(self,name,behavior):
        p=self.d/name;p.write_text('#!'+sys.executable+'\nimport sys\nfrom pathlib import Path\nif "--version" in sys.argv:sys.exit(0)\nassert "--no-default-config" in sys.argv\np=Path(sys.argv[sys.argv.index("-o")+1])\n'+behavior+'\n');p.chmod(0o755);return str(p)
    def check_bad(self,behavior):
        work=self.d/'gate';work.mkdir();(work/'same.o').write_bytes(b'stale')
        ordinary=self.compiler('ordinary','p.write_bytes(b"object")')
        candidate=self.compiler('candidate',behavior)
        with self.assertRaisesRegex(h.GateError,'nonempty regular'):h.tiny_gate(ordinary,candidate,work)
    def test_zero_without_output(self):self.check_bad('pass')
    def test_empty_output(self):self.check_bad('p.touch()')
    def test_symlink_output(self):self.check_bad('p.symlink_to("tiny.c")')
    def test_config_disabled_both(self):
        self.assertEqual(len(h.tiny_gate(self.compiler('o','p.write_bytes(b"o")'),self.compiler('c','p.write_bytes(b"o")'),self.d/'gate')),3)

class ReviewInventoryTests(Base):
    def test_missing_root(self):
        with self.assertRaises(h.GateError):h.inventory(self.d/'missing')
    def test_symlink_root(self):
        (self.d/'link').symlink_to(self.d,target_is_directory=True)
        with self.assertRaises(h.GateError):h.inventory(self.d/'link')
    def test_scandir_permission_error_even_as_root(self):
        child=self.d/'child';child.mkdir();real=os.scandir
        def scandir(path):
            if Path(path)==child:raise PermissionError(13,'fixture forced unreadable directory',str(child))
            return real(path)
        with patch.object(os,'scandir',scandir),self.assertRaisesRegex(h.GateError,'inventory traversal failed.*child'):h.inventory(self.d)

class ReviewElfTests(Base):
    def mutate(self,offset,fmt,value):
        p=self.d/'elf';elf(p);data=bytearray(p.read_bytes());struct.pack_into(fmt,data,offset,value);p.write_bytes(data);return p
    def rejected(self,p,audit=False):
        with self.assertRaises(h.GateError):
            e=h.ELF(p)
            try:
                if audit:e.audit()
            finally:e.close()
    def test_type(self):self.rejected(self.mutate(16,'<H',1))
    def test_ident_version(self):self.rejected(self.mutate(6,'<B',0))
    def test_header_version(self):self.rejected(self.mutate(20,'<I',0))
    def test_header_size(self):self.rejected(self.mutate(52,'<H',63))
    def test_section_content_outside_file(self):
        p=self.d/'elf';elf(p);data=bytearray(p.read_bytes());sh=struct.unpack_from('<Q',data,40)[0];struct.pack_into('<Q',data,sh+64+32,len(data)+1);p.write_bytes(data);self.rejected(p)
    def test_section_names_not_strtab(self):
        p=self.d/'elf';elf(p);data=bytearray(p.read_bytes());sh=struct.unpack_from('<Q',data,40)[0];struct.pack_into('<I',data,sh+64+4,1);p.write_bytes(data);self.rejected(p)
    def test_load_filesz_exceeds_memsz(self):self.rejected(self.mutate(64+32,'<Q',2))
    def test_load_file_range(self):self.rejected(self.mutate(64+8,'<Q',1<<40))
    def test_entry_in_bss_rejected(self):
        p=self.mutate(64+40,'<Q',100);data=bytearray(p.read_bytes());struct.pack_into('<Q',data,24,0x400101);p.write_bytes(data);self.rejected(p,True)
    def test_string_range(self):
        p=self.d/'elf';elf(p);e=h.ELF(p)
        try:
            for offset,size,start in [(len(e.mm),10,0),(0,1,-1),(0,1,1)]:
                with self.subTest(values=(offset,size,start)),self.assertRaises(h.GateError):e.string(offset,size,start)
        finally:e.close()
    def test_nobits_allowed_outside_file(self):
        p=self.d/'elf';elf(p);data=bytearray(p.read_bytes());sh=struct.unpack_from('<Q',data,40)[0];struct.pack_into('<I',data,sh+2*64+4,8);struct.pack_into('<Q',data,sh+2*64+24,1<<40);p.write_bytes(data);e=h.ELF(p);e.close()

class ReviewAliasTests(Base):
    def root(self):
        root=self.d/'root';(root/'usr/bin').mkdir(parents=True);(root/'usr/bin/clang-22').write_bytes(b'new');return root
    def test_old_symlink(self):
        for alias in ('clang-cl','clang-cpp'):
            with self.subTest(alias=alias):
                root=self.root() if not (self.d/'root').exists() else self.d/'root';p=root/'usr/bin'/alias;(root/'usr/bin/old').write_bytes(b'old');p.symlink_to('old')
                with self.assertRaises(h.GateError):h.alias_group(root)
                p.unlink()
    def test_wrong_regular(self):
        root=self.root()
        for alias in ('clang-cl','clang-cpp'):
            p=root/'usr/bin'/alias;p.write_bytes(b'old')
            with self.assertRaises(h.GateError):h.alias_group(root)
            p.unlink()
    def test_normal(self):
        root=self.root();(root/'usr/bin/clang-cl').symlink_to('clang-22');(root/'usr/bin/clang-cpp').write_bytes(b'new');self.assertEqual(len(h.alias_group(root)[1]),2)

class ReviewVersionTests(unittest.TestCase):
    def test_exact_line(self):self.assertEqual(h.certified_version('LLVM\n  LLVM version 22.1.8\nOptimized build.\n'),'LLVM version 22.1.8')
    def test_substring_or_different_version(self):
        for text in ['LLVM version 22.1.80','LLVM version 22.1.8git','prefix LLVM version 22.1.8','LLVM version 22.1.8\nLLVM version 22.1.8']:
            with self.subTest(text=text),self.assertRaises(h.GateError):h.certified_version(text)

class ReviewReverseTests(Base):
    def test_clean(self):self.assertTrue(h.no_bolt_products(self.d)['no_bolt_products'])
    def test_tools(self):
        (self.d/'usr/bin').mkdir(parents=True)
        for name in ('llvm-bolt','perf2bolt','llvm-boltdiff','merge-fdata'):
            p=self.d/'usr/bin'/name;p.symlink_to('absent')
            with self.subTest(name=name),self.assertRaises(h.GateError):h.no_bolt_products(self.d)
            p.unlink()
    def test_static_library(self):
        (self.d/'usr/lib64').mkdir(parents=True);(self.d/'usr/lib64/libLLVMBOLTCore.a').write_bytes(b'a')
        with self.assertRaises(h.GateError):h.no_bolt_products(self.d)
    def test_cmake_export(self):
        (self.d/'usr/lib64/cmake/llvm').mkdir(parents=True);(self.d/'usr/lib64/cmake/llvm/LLVMConfig.cmake').write_text('set(libs LLVMBOLTCore)')
        with self.assertRaisesRegex(h.GateError,'BOLT CMake export'):h.no_bolt_products(self.d)

if __name__=='__main__':unittest.main()
