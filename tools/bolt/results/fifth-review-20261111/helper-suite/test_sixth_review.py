"""Second external review: fail-closed shell gate and cancellation contracts."""
import contextlib,io,os,signal,subprocess,sys,time
from pathlib import Path
from unittest.mock import patch
import bolt_helper as h
from test_bolt_helper import Base
import test_hybrid_review as hybrid
import test_fifth_review as fifth

class HybridFailureTests(Base):
    def setUp(self):
        super().setUp()
        spec=(Path(h.__file__).parent/"llvm.spec").read_text()
        a=spec.index("for hybrid_tool in ");b=spec.index("echo TIZEN_HYBRID_LINK_OK",a)
        self.gate=spec[a:b]+"echo TIZEN_HYBRID_LINK_OK\n"
        (self.d/"bin").mkdir();(self.d/"mock").mkdir()
        for n in ("clang-22","lld","llvm-ar"):(self.d/"bin"/n).write_text("fixture")
    def mock_gate(self,readelf='exit 0',grep=None,optional=None):
        for name,body in [('readelf',readelf),('grep',grep)]:
            if body is not None:
                p=self.d/'mock'/name;p.write_text('#!/bin/sh\n'+body+'\n');p.chmod(0o755)
        if optional:(self.d/'bin'/optional).write_text('fixture')
        p=subprocess.run(['/bin/sh','-e','-c',self.gate],cwd=self.d,env=dict(os.environ,PATH=str(self.d/'mock')+':'+os.environ['PATH']),capture_output=True,text=True)
        return p
    def reject(self,**kw):
        p=self.mock_gate(**kw);self.assertNotEqual(p.returncode,0);self.assertIn('TIZEN_HYBRID_LINK_FAILED',p.stderr);self.assertNotIn('TIZEN_HYBRID_LINK_OK',p.stdout)
    def test_grep_2(self):self.reject(grep='exit 2')
    def test_grep_127(self):self.reject(grep='exit 127')
    def test_readelf_failure(self):self.reject(readelf='exit 7')
    def test_optional_shared(self):self.reject(optional='llvm-config',readelf='case "$2" in bin/llvm-config) echo "(NEEDED) [libLLVM.so]";; esac')
    def test_optional_absent(self):
        p=self.mock_gate();self.assertEqual(p.returncode,0)
        for name in ('llvm-tblgen','clang-tblgen','lldb-tblgen','llvm-config','llvm-exegesis'):self.assertIn('TIZEN_HYBRID_LINK_SKIP bin/'+name,p.stdout)

class CancelTests(Base):
    def tearDown(self):h._CANCEL_SIGNAL=None;super().tearDown()
    def test_after_main(self):
        def work():h.record_cancel(signal.SIGTERM,None)
        with patch.object(h,'main',side_effect=work),patch.object(h,'disk_diagnose') as disk,contextlib.redirect_stderr(io.StringIO()) as out:
            self.assertEqual(h.cli(),143);self.assertIn('BOLT_CANCELLED: signal 15',out.getvalue());disk.assert_not_called()
    def test_after_last_child_no_marker(self):
        log=self.d/'step.log'
        def call(*a,**kw):log.write_text('child completed\n');h.record_cancel(signal.SIGTERM,None);return 'child completed\n'
        with patch.object(h,'call',side_effect=call),self.assertRaisesRegex(h.GateError,'^CANCELLED:'):
            h.run_step('late',log,['fixture'],success_marker='SUCCESS')
        self.assertNotIn('SUCCESS',log.read_text())
    def test_digest_cancel(self):
        p=self.d/'file';p.write_bytes(b'a');h.record_cancel(signal.SIGTERM,None)
        with self.assertRaisesRegex(h.GateError,'^CANCELLED:'):h.digest(p)
    def test_inventory_cancel(self):
        h.record_cancel(signal.SIGTERM,None)
        with self.assertRaisesRegex(h.GateError,'^CANCELLED:'):h.inventory(self.d)
    def test_profile_cancel(self):
        import lzma
        p=self.d/'profile.xz';p.write_bytes(lzma.compress(b'abc'));h.record_cancel(signal.SIGTERM,None)
        with self.assertRaisesRegex(h.GateError,'^CANCELLED:'):h.profile_unpack(p,self.d/'out')
    def test_prefixes(self):
        for argv,timeout,prefix in [(['/bin/sh','-c','exit 2'],1,'COMMAND_ERROR:'),(['/bin/sh','-c','sleep 2'],.02,'TIMEOUT:')]:
            with self.assertRaises(h.GateError) as e:h.call(argv,self.d/'log',timeout=timeout)
            self.assertTrue(str(e.exception).startswith(prefix));self.assertNotIn('CANCELLED:',str(e.exception))
    def test_pure_python_sigterm(self):
        code="import importlib.util,sys; from pathlib import Path; s=importlib.util.spec_from_file_location('h',sys.argv[1]);h=importlib.util.module_from_spec(s);s.loader.exec_module(h); p=Path(sys.argv[2]); p.write_bytes(b'a'*1024); h.main=lambda:exec('while True: h.digest(p)',globals()); sys.exit(h.cli())"
        p=subprocess.Popen([sys.executable,'-B','-c',code,h.__file__,str(self.d/'ready')],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        try:
            for _ in range(500):
                if (self.d/'ready').exists():break
                time.sleep(.01)
            time.sleep(.05);p.send_signal(signal.SIGTERM);o,e=p.communicate(timeout=5)
            self.assertEqual(p.returncode,143);self.assertIn('CANCELLED:',e)
        finally:
            if p.poll() is None:p.kill();p.wait()
    def test_double_term(self):
        code="""import importlib.util,sys,signal,time
from pathlib import Path
s=importlib.util.spec_from_file_location('h',sys.argv[1]);h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
ready=Path(sys.argv[2]);log=ready.with_suffix('.log')
original=h.wait_group_exit
def cleanup(*a,**kw):
 ready.write_text(str(a[0]));time.sleep(3);return original(*a,**kw)
h.wait_group_exit=cleanup
h.main=lambda:h.call(['/bin/sh','-c','sleep 30 & wait'],log)
sys.exit(h.cli())
"""
        ready=self.d/'ready';p=subprocess.Popen([sys.executable,'-B','-c',code,h.__file__,str(ready)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            for _ in range(500):
                if ready.with_suffix('.log').exists():break
                time.sleep(.01)
            time.sleep(.1);p.send_signal(signal.SIGTERM)
            for _ in range(500):
                if ready.exists():break
                time.sleep(.01)
            self.assertTrue(ready.exists());group=int(ready.read_text());p.send_signal(signal.SIGTERM);p.communicate(timeout=5)
            self.assertEqual(p.returncode,-signal.SIGTERM);h.wait_group_exit(group,3)
        finally:
            if p.poll() is None:p.kill();p.wait()

class IntCancellationTests(Base):
    probe=fifth.CancellationTests.probe
    def test_int_after(self):self.probe(signal.SIGINT,'after')
    def test_int_cleanup(self):self.probe(signal.SIGINT,'cleanup')
