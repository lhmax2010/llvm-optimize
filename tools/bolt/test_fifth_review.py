"""External review: exact paths, cancellation, timeout and packaging checks."""
import json
import os
from pathlib import Path
import signal
import struct
import subprocess
import sys
import time
import unittest
from unittest.mock import patch
import bolt_helper as h
from test_bolt_helper import Base
import test_runpath_improvements as runpath


class FrozenRunpathTests(Base):
    setup_elf = runpath.RunpathTests.setup_elf
    adjust = runpath.RunpathTests.adjust
    def corrupt(self, what):
        self.setup_elf('$ORIGIN/../lib64:/build/lib64:')
        original=h.call
        def call(argv,*a,**kw):
            result=original(argv,*a,**kw)
            if argv[0]=='cmake':
                e=h.ELF(self.candidate)
                try:
                    if what=='string':
                        s=e.by_name['.dynstr'];pos=s[4]+1
                    else:
                        s=e.by_name['.dynamic'];pos=next(i+8 for i in range(s[4],s[4]+s[5],16) if e.unpack('<qQ',i)[0]==what)
                finally:e.close()
                data=bytearray(self.candidate.read_bytes());data[pos]^=1;self.candidate.write_bytes(data)
            return result
        with patch.object(h,'call',side_effect=call),self.assertRaisesRegex(h.GateError,'non-path content'):
            self.adjust()
    def test_fini_value_rejected(self):self.corrupt(13)
    def test_rela_value_rejected(self):self.corrupt(7)
    def test_non_path_dynstr_rejected(self):self.corrupt('string')


class DebugListTests(Base):
    def setUp(self):
        super().setUp();self.ordinary=self.d/'build/clang-bolt/ordinary';self.list=self.d/'debugfiles.list'
    def test_present(self):
        self.list.write_text('/'+h.DEBUG_INSTALL_PATH+'\n');self.assertTrue(h.debugfiles_gate(self.ordinary,{'debug_file':{}})['required'])
    def test_dot_prefix(self):
        self.list.write_text('./'+h.DEBUG_INSTALL_PATH+'\n');self.assertTrue(h.debugfiles_gate(self.ordinary,{'debug_file':{}})['required'])
    def test_absent_entry(self):
        self.list.write_text('/usr/lib/debug/other\n')
        with self.assertRaisesRegex(h.GateError,'omits'):h.debugfiles_gate(self.ordinary,{'debug_file':{}})
    def test_missing_list(self):
        with self.assertRaisesRegex(h.GateError,'missing'):h.debugfiles_gate(self.ordinary,{'debug_file':{}})
    def test_release_skip(self):self.assertFalse(h.debugfiles_gate(self.ordinary,{})['required'])


class CliReviewTests(Base):
    def test_unexpected_post_key(self):
        root=self.d/'root';(root/'usr/bin').mkdir(parents=True);(root/'usr/bin/clang-22').write_bytes(b'fixture')
        state=self.d/'state.json';state.write_text('{}')
        p=subprocess.run([sys.executable,'-B',h.__file__,'post',str(root),str(state),'ordinary',str(self.d/'post')],capture_output=True,text=True)
        self.assertNotEqual(p.returncode,0);self.assertIn('BOLT_GATE_FAILED: unexpected KeyError:',p.stderr);self.assertIn('Traceback',p.stderr)
    def test_restore_handlers(self):
        old={s:signal.getsignal(s) for s in (signal.SIGTERM,signal.SIGHUP)}
        with patch.object(h,'main'):self.assertEqual(h.cli(),0)
        self.assertEqual(old,{s:signal.getsignal(s) for s in old})
    def test_short_timeout(self):
        log=self.d/'timeout.log';real=h.call
        def short(argv,log,**kw):
            self.assertEqual(kw['timeout'],14400)
            return real(argv,log,timeout=.1)
        with patch.object(h,'call',side_effect=short),self.assertRaisesRegex(h.GateError,r'TIMEOUT: step=fixture elapsed_seconds='):
            h.run_step('fixture',log,['/bin/sh','-c','sleep 20 & wait'])
    def test_normal_step(self):
        r=h.run_step('normal',self.d/'ok.log',['/bin/sh','-c','printf normal'])
        self.assertEqual(r['step'],'normal')


class CancellationTests(Base):
    def probe(self,sig,phase):
        heartbeat=self.d/'heartbeat';ready=self.d/'ready';log=self.d/'step.log'
        child_heartbeat=Path(str(heartbeat)+'.child')
        grandchild_code="import time,sys,os; f=open(sys.argv[1],'a',buffering=1); exec('while True: f.write(str(os.getpid())+chr(32)+str(time.time())+chr(10)); time.sleep(.03)')"
        child_code="import subprocess,sys,time,os; p=subprocess.Popen([sys.executable,'-c',"+repr(grandchild_code)+",sys.argv[1]]); f=open(sys.argv[1]+'.child','a',buffering=1); exec('while True: f.write(str(os.getpid())+chr(32)+str(time.time())+chr(10)); time.sleep(.03)')"
        # Instrument timing only, then execute the real CLI and real process tree.
        wrapper=self.d/'invoke.py'
        wrapper.write_text('''import importlib.util,sys,os,time,signal
from pathlib import Path
s=importlib.util.spec_from_file_location('h',sys.argv[1]);h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
phase=sys.argv[2];ready=Path(sys.argv[3]);sig=int(sys.argv[4]);heartbeat=sys.argv[5];log=sys.argv[6]
if phase=='before':
 original=h.check_cancel
 def check():
  ready.write_text('before')
  time.sleep(.3)
  original()
 h.check_cancel=check
elif phase=='cleanup':
 original=h.wait_group_exit
 def cleanup(*a,**kw):
  ready.write_text('cleanup')
  time.sleep(.3)
  return original(*a,**kw)
 h.wait_group_exit=cleanup
code=CODE_TOKEN
sys.argv=['helper','run-step','cancel',log,'--','/bin/sh','-c','exec '+h.quote(sys.executable)+' -c '+h.quote(code)+' '+h.quote(heartbeat)]
sys.exit(h.cli())
'''.replace('CODE_TOKEN',repr(child_code)))
        p=subprocess.Popen([sys.executable,'-B',str(wrapper),h.__file__,phase,str(ready),str(sig),str(heartbeat),str(log)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        try:
            end=time.monotonic()+5
            targets=[ready] if phase=='before' else [heartbeat,child_heartbeat]
            while not all(x.exists() and x.stat().st_size for x in targets) and p.poll() is None and time.monotonic()<end:time.sleep(.01)
            self.assertTrue(all(x.exists() and x.stat().st_size for x in targets),'probe did not become ready')
            descendants=[] if phase=='before' else [int(x.read_text().split()[0]) for x in [child_heartbeat,heartbeat]]
            os.kill(p.pid,sig)
            if phase=='cleanup':
                while not ready.exists() and p.poll() is None and time.monotonic()<end:time.sleep(.01)
                self.assertTrue(ready.exists());os.kill(p.pid,sig)
            out,err=p.communicate(timeout=12)
            self.assertNotEqual(p.returncode,0);self.assertIn('signal '+str(sig),err)
            sizes=[x.stat().st_size if x.exists() else 0 for x in [heartbeat,child_heartbeat]];time.sleep(.15)
            self.assertEqual(sizes,[x.stat().st_size if x.exists() else 0 for x in [heartbeat,child_heartbeat]])
            states={}
            for pid in descendants:
                try:state=h.proc_stat('/proc/%d/stat'%pid)[1]
                except FileNotFoundError:state='gone'
                self.assertIn(state,('gone','Z','X'));states[pid]=state
            print('CANCELLATION_PROBE '+json.dumps({'signal':int(sig),'phase':phase,'rc':p.returncode,'stderr':err,'descendants':states,'both_heartbeats_stopped':True}))
        finally:
            if p.poll() is None:p.kill();p.wait()
    def test_term_before(self):self.probe(signal.SIGTERM,'before')
    def test_hup_before(self):self.probe(signal.SIGHUP,'before')
    def test_term_after(self):self.probe(signal.SIGTERM,'after')
    def test_hup_after(self):self.probe(signal.SIGHUP,'after')
    def test_term_cleanup(self):self.probe(signal.SIGTERM,'cleanup')
    def test_hup_cleanup(self):self.probe(signal.SIGHUP,'cleanup')


class StripLayoutTests(Base):
    def setup_elf(self):
        # The test ELF's sole LOAD contains one text byte, not section metadata.
        from test_bolt_helper import elf
        self.a=self.d/'a';self.b=self.d/'b';elf(self.a)
        e=h.ELF(self.a)
        try:offset=e.by_name['.text'][4]
        finally:e.close()
        data=bytearray(self.a.read_bytes());struct.pack_into('<Q',data,64+8,offset);self.a.write_bytes(data);self.b.write_bytes(data)
    def test_symbol_table_removed(self):
        self.setup_elf()
        # Remove nonloaded symbol-table section headers; loaded bytes stay put.
        original=self.a.read_bytes();shoff=struct.unpack_from('<Q',original,40)[0]
        e=h.ELF(self.a)
        try:headers=[original[shoff+i*64:shoff+(i+1)*64] for i,n in enumerate(e.names) if n not in ('.symtab','.strtab')]
        finally:e.close()
        data=bytearray(original[:shoff]+b''.join(headers));struct.pack_into('<H',data,60,len(headers));self.b.write_bytes(data)
        self.assertTrue(h.verify_strip_layout(self.a,self.b)['preserved'])
    def test_load_address_changed(self):
        self.setup_elf();data=bytearray(self.b.read_bytes());struct.pack_into('<Q',data,64+16,0x500100);self.b.write_bytes(data)
        with self.assertRaisesRegex(h.GateError,'LOAD'):h.verify_strip_layout(self.a,self.b)
    def test_load_content_changed(self):
        self.setup_elf();e=h.ELF(self.b)
        try:offset=e.loads[0][2]
        finally:e.close()
        data=bytearray(self.b.read_bytes());data[offset]^=1;self.b.write_bytes(data)
        with self.assertRaisesRegex(h.GateError,'LOAD'):h.verify_strip_layout(self.a,self.b)


class ProductionConstantsTests(Base):
    def test_profile_options_and_whitelist_unchanged(self):
        import ast
        old=Path(__file__).parents[2]/'patches/review-20261102/files/packaging/clang-bolt-helper.py'
        def constants(path):
            result={}
            for node in ast.parse(path.read_text()).body:
                if isinstance(node,ast.Assign):
                    for target in node.targets:
                        if isinstance(target,ast.Name):result[target.id]=ast.dump(node.value,include_attributes=False)
            return result
        before,after=constants(old),constants(Path(h.__file__))
        for name in ('OPTIONS','PROFILE_SHA','CERTIFIED','BOLT_TASK_DESCRIPTIONS','TF_REFRESH_DESCRIPTIONS'):
            with self.subTest(name=name):self.assertEqual(before[name],after[name])
    def test_child_ninja_environment(self):
        spec=(Path(h.__file__).parent/'llvm.spec').read_text()
        self.assertEqual(spec.count("-- env LC_ALL=C NINJA_STATUS='[%%f/%%t] ' ninja"),2)
        p=subprocess.run([sys.executable,'-B',h.__file__,'run-step','environment',str(self.d/'env.log'),'--','env','LC_ALL=C','NINJA_STATUS=[%f/%t] ',sys.executable,'-c',"import os,json; print(json.dumps({k:os.environ[k] for k in ('LC_ALL','NINJA_STATUS')}))"],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(json.loads((self.d/'env.log').read_text()),{'LC_ALL':'C','NINJA_STATUS':'[%f/%t] '})
