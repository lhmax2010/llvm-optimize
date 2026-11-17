import contextlib, errno, importlib.util, io, json, os, signal, subprocess, sys, tempfile, time, unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch, MagicMock
H = Path(os.environ['PRODUCT_SOURCE'])/'packaging/clang-bolt-helper.py'


def load():
    spec = importlib.util.spec_from_file_location('helper114', H)
    h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
    return h


class Hardening(unittest.TestCase):
    def setUp(self):
        self.h = load(); self.temp = tempfile.TemporaryDirectory()
        self.d = Path(self.temp.name); self.children = []

    def tearDown(self):
        for p in self.children:
            if p.poll() is None: p.kill()
            p.wait(timeout=3)
        self.temp.cleanup()

    def child(self):
        p = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'], start_new_session=True)
        self.children.append(p); return p

    def retirement(self, point):
        h = self.h; real = h.reap_child; calls = []
        def reap(p, *args):
            calls.append(p); self.assertIsNone(h._ACTIVE_SESSION)
            if point == 'before' and len(calls) == 1: raise OSError('before waitpid')
            rc = real(p, *args)
            if point == 'after': raise OSError('after actual reap')
            return rc
        save = h.save
        def save_fault(path, value):
            if point == 'metadata' and value.get('completed'): raise OSError('metadata after reap')
            return save(path, value)
        with patch.object(h, 'kill_session') as kill, patch.object(h, 'reap_child', side_effect=reap), patch.object(h, 'save', side_effect=save_fault):
            with self.assertRaises(h.GateError): h.call([sys.executable, '-c', 'pass'], self.d/'log')
            kill.assert_not_called()
        self.assertEqual(len(calls), 2 if point == 'before' else 1)
        self.assertEqual(calls[0].returncode, 0)
        with self.assertRaises(ChildProcessError): os.waitpid(calls[0].pid, os.WNOHANG)

    def test_retire_before_waitpid_fault(self): self.retirement('before')
    def test_retire_after_real_reap_fault(self): self.retirement('after')
    def test_retire_metadata_after_reap_fault(self): self.retirement('metadata')

    def test_cleanup_error_is_failure(self):
        h = self.h
        with patch.object(h, 'wait_session_exit', side_effect=h.GateError('denied fixture')):
            with self.assertRaisesRegex(h.GateError, 'cleanup error'):
                h.call([sys.executable, '-c', 'raise SystemExit(7)'], self.d/'log')

    def test_zero_systemexit_cannot_hide_cleanup_error(self):
        h=self.h
        with patch.object(h,'peek_child_exit',side_effect=SystemExit(0)),patch.object(h,'wait_session_exit',side_effect=h.GateError('cleanup denied')):
            with self.assertRaisesRegex(h.GateError,'cleanup error: cleanup denied'):
                h.call([sys.executable,'-c','import time;time.sleep(30)'],self.d/'log')

    def test_retire_after_waitpid_before_returncode_assignment(self):
        h=self.h;seen=[]
        def reap(p,*args):
            self.assertIsNone(h._ACTIVE_SESSION);seen.append(p.pid)
            os.waitpid(p.pid,0)
            raise OSError('fault before returncode assignment')
        with patch.object(h,'reap_child',side_effect=reap),patch.object(h,'kill_session') as kill:
            with self.assertRaisesRegex(h.GateError,'cleanup error'):
                h.call([sys.executable,'-c','pass'],self.d/'log')
        kill.assert_not_called();self.assertEqual(len(seen),2)
        with self.assertRaises(ChildProcessError):os.waitpid(seen[0],os.WNOHANG)

    def test_force_reentrant_mock_only_one_cleanup(self):
        h = self.h; h._CANCEL_SIGNAL = signal.SIGTERM; h._ACTIVE_SESSION = 99999999
        def nested(*args):
            h.record_cancel(signal.SIGHUP, None)
        with patch.object(h, 'kill_session', side_effect=nested) as cleanup, patch.object(h.signal, 'signal'), patch.object(h.os, 'kill') as terminate:
            h.record_cancel(signal.SIGTERM, None)
        cleanup.assert_called_once_with(99999999, 1)
        self.assertEqual([c.args[1] for c in terminate.call_args_list], [signal.SIGHUP, signal.SIGTERM])

    def test_force_exception_still_terminates(self):
        h=self.h; h._CANCEL_SIGNAL=signal.SIGTERM; h._ACTIVE_SESSION=99999999
        with patch.object(h,'kill_session',side_effect=RuntimeError('denied')),patch.object(h.signal,'signal') as restore,patch.object(h.os,'kill') as terminate:
            h.record_cancel(signal.SIGHUP,None)
        restore.assert_called_once_with(signal.SIGHUP,signal.SIG_DFL)
        terminate.assert_called_once_with(os.getpid(),signal.SIGHUP)

    def test_force_reentrant_real_short_timing(self):
        # Signal only our Popen child. Its emergency routine is deliberately slow
        # and records entries, without launching or signaling any descendants.
        code = '''import importlib.util,os,signal,sys,time
from pathlib import Path
s=importlib.util.spec_from_file_location('h',sys.argv[1]);h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
d=Path(sys.argv[2]);h._CANCEL_SIGNAL=signal.SIGTERM;h._ACTIVE_SESSION=99999999
def cleanup(*args):
 with (d/'entries').open('a') as f:f.write('entry\\n');f.flush()
 time.sleep(5)
h.kill_session=cleanup
for sig in (signal.SIGTERM,signal.SIGHUP):signal.signal(sig,h.record_cancel)
(d/'ready').write_text('ready')
while True:time.sleep(.01)
'''
        p=subprocess.Popen([sys.executable,'-c',code,str(H),str(self.d)]);self.children.append(p)
        end=time.monotonic()+3
        while not (self.d/'ready').exists() and time.monotonic()<end: time.sleep(.01)
        self.assertTrue((self.d/'ready').exists());p.send_signal(signal.SIGTERM)
        while not (self.d/'entries').exists() and time.monotonic()<end: time.sleep(.01)
        self.assertTrue((self.d/'entries').exists())
        start=time.monotonic();p.send_signal(signal.SIGHUP);self.assertEqual(p.wait(timeout=2),-signal.SIGHUP)
        self.assertLess(time.monotonic()-start,2);self.assertEqual((self.d/'entries').read_text().splitlines(),['entry'])

    def test_pidfd_stale_pid_in_other_owned_session_skipped(self):
        p=self.child();h=self.h;h._SESSION_KILL_MODE='pidfd'
        h.kill_session_member(os.getsid(0),p.pid,0)
        self.assertIsNone(p.poll())

    def test_pidfd_matching_owned_member_killed(self):
        p=self.child();h=self.h;h._SESSION_KILL_MODE='pidfd'
        h.kill_session_member(p.pid,p.pid,h.proc_stat('/proc/%d/stat'%p.pid)[5])
        self.assertEqual(p.wait(timeout=3),-signal.SIGKILL)

    def test_pidfd_closed_if_proc_disappears(self):
        h=self.h;h._SESSION_KILL_MODE='pidfd'
        with patch.object(h.os,'pidfd_open',return_value=71),patch.object(h.os,'close') as close,patch.object(h,'proc_stat',side_effect=FileNotFoundError()),patch.object(h.signal,'pidfd_send_signal') as send:
            with self.assertRaises(FileNotFoundError):h.kill_session_member(42,31,1)
        close.assert_called_once_with(71);send.assert_not_called()

    def test_pidfd_closed_on_signal_permission_error(self):
        h=self.h;h._SESSION_KILL_MODE='pidfd'
        with patch.object(h.os,'pidfd_open',return_value=71),patch.object(h.os,'close') as close,patch.object(h,'proc_stat',return_value=(31,'R',31,1,42,1)),patch.object(h.signal,'pidfd_send_signal',side_effect=PermissionError()):
            with self.assertRaises(PermissionError):h.kill_session_member(42,31,1)
        close.assert_called_once_with(71)

    def mode(self,error):
        h=self.h;output=io.StringIO()
        with patch.object(h.os,'pidfd_open',side_effect=error),contextlib.redirect_stderr(output):
            self.assertEqual(h.session_kill_mode(),'fallback-recheck');self.assertEqual(h.session_kill_mode(),'fallback-recheck')
        self.assertEqual(output.getvalue(),'SESSION_KILL_MODE=fallback-recheck'+(' errno='+errno.errorcode[error.errno] if isinstance(error,OSError) else '')+'\n')
    def test_pidfd_absent_logged_fallback(self):self.mode(AttributeError('missing'))
    def test_pidfd_enosys_logged_fallback(self):self.mode(OSError(errno.ENOSYS,'unsupported'))
    def test_pidfd_eperm_logged_fallback(self):self.mode(PermissionError(errno.EPERM,'denied'))

    def test_pidfd_send_api_missing_closes_probe_fd(self):
        h=self.h
        with patch.object(h.os,'pidfd_open',return_value=71),patch.object(h.os,'close') as close,patch.object(h.signal,'pidfd_send_signal',side_effect=AttributeError('missing')),contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(h.session_kill_mode(),'fallback-recheck')
        close.assert_called_once_with(71)

    def test_pidfd_other_failure_blocks_spawn(self):
        h=self.h
        with patch.object(h.os,'pidfd_open',side_effect=OSError(errno.EMFILE,'fd limit')),patch.object(h.subprocess,'Popen') as spawn:
            with self.assertRaisesRegex(h.GateError,'fd limit'):h.call(['unreachable'],self.d/'log')
        spawn.assert_not_called()

    def test_mode_logged_before_spawn(self):
        h=self.h;out=io.StringIO();real=h.subprocess.Popen
        def spawn(*a,**kw):
            self.assertEqual(out.getvalue(),'SESSION_KILL_MODE=pidfd\n');return real(*a,**kw)
        with contextlib.redirect_stderr(out),patch.object(h.subprocess,'Popen',side_effect=spawn):
            h.call([sys.executable,'-c','pass'],self.d/'log')

    def test_fallback_revalidates_sid_and_starttime(self):
        h=self.h;h._SESSION_KILL_MODE='fallback-recheck'
        with patch.object(h,'proc_stat',side_effect=[(31,'R',31,1,43,1),(31,'R',31,1,42,2),(31,'R',31,1,42,1)]),patch.object(h.os,'kill') as kill:
            for _ in range(3):h.kill_session_member(42,31,1)
        kill.assert_called_once_with(31,signal.SIGKILL)

    def test_fallback_stale_owned_session_safe(self):
        h=self.h;p=self.child();h._SESSION_KILL_MODE='fallback-recheck'
        h.kill_session_member(os.getsid(0),p.pid,0);self.assertIsNone(p.poll())

    def test_permission_member_does_not_stop_next(self):
        h=self.h
        with patch.object(h,'live_session_members',side_effect=[[(31,'R',1),(32,'S',2)],[(31,'R',1),(32,'S',2)],[]]),patch.object(h,'kill_session_member',side_effect=[PermissionError('denied 31'),None,None,None]) as kill:
            with self.assertRaisesRegex(h.GateError,'denied 31'):h.wait_session_exit(42,1,kill=True)
        self.assertEqual([c.args[1] for c in kill.call_args_list],[31,32,31,32])

    def test_missing_member_does_not_stop_next(self):
        h=self.h
        with patch.object(h,'live_session_members',side_effect=[[(31,'R',1),(32,'S',2)],[]]),patch.object(h,'kill_session_member',side_effect=[ProcessLookupError(),None]) as kill:
            h.wait_session_exit(42,1,kill=True)
        self.assertEqual(kill.call_count,2)

    def test_leader_permission_still_processes_members(self):
        h=self.h
        with patch.object(h.os,'killpg',side_effect=PermissionError('leader denied')),patch.object(h,'wait_session_exit') as wait:
            with self.assertRaisesRegex(h.GateError,'leader denied'):h.kill_session(42)
        self.assertTrue(wait.called)

    def scan_context(self,values):
        h=self.h; entries=MagicMock();entries.__enter__.return_value=iter([SimpleNamespace(name=str(p)) for p in values])
        def stat(path):
            if path=='/proc/self/stat':return os.getpid(),'R',0,1,0,1
            value=values[int(Path(path).parent.name)]
            if isinstance(value,BaseException):raise value
            return value
        return patch.object(h.os,'scandir',return_value=entries),patch.object(h,'proc_stat',side_effect=stat)

    def test_scan_permission_retains_other_members_and_fails(self):
        h=self.h;a,b=self.scan_context({31:PermissionError('scan denied'),32:(32,'R',32,1,42,2)})
        with a,b,self.assertRaises(h.SessionInspectionError) as caught:h.live_session_members(42)
        self.assertEqual(caught.exception.members,[(32,'R',2)])

    def test_partial_scan_still_kills_visible_member(self):
        h=self.h
        error=h.SessionInspectionError('scan incomplete: denied',[(32,'R',2)])
        with patch.object(h,'live_session_members',side_effect=error),patch.object(h,'kill_session_member') as kill:
            with self.assertRaisesRegex(h.GateError,'scan incomplete'):h.wait_session_exit(42,1,kill=True)
        self.assertEqual(kill.call_args.args[:3],(42,32,2))

    def test_scan_disappearing_entries_skipped(self):
        h=self.h;a,b=self.scan_context({31:FileNotFoundError(),32:ProcessLookupError()})
        with a,b:self.assertEqual(h.live_session_members(42),[])

    def test_deadline_partial_scan_never_empty_success(self):
        h=self.h; clock=[0]
        a,b=self.scan_context({31:(31,'R',31,1,42,1),32:(32,'R',32,1,42,2)})
        with a,b:
            original=h.proc_stat.side_effect
            def stat(path):
                result=original(path)
                if path=='/proc/31/stat':clock[0]=2
                return result
            h.proc_stat.side_effect=stat
            with patch.object(h.time,'monotonic',side_effect=lambda:clock[0]),self.assertRaisesRegex(h.SessionDeadlineError,'scan incomplete') as caught:
                h.live_session_members(42,1)
        self.assertEqual(caught.exception.members,[(31,'R',1)])


    def test_deadline_after_empty_scan_fails(self):
        h=self.h;clock=[0];a,b=self.scan_context({})
        def entries():
            clock[0]=2
            yield from ()
        with a,b,patch.object(h.time,'monotonic',side_effect=lambda:clock[0]):
            h.os.scandir.return_value.__enter__.return_value=entries()
            with self.assertRaisesRegex(h.GateError,'scan incomplete'):h.live_session_members(42,1)


    def test_deadline_checked_between_kills(self):
        h=self.h;clock=[0]
        def kill_one(*args):clock[0]=2
        with patch.object(h,'live_session_members',return_value=[(31,'R',1),(32,'R',2)]),patch.object(h.time,'monotonic',side_effect=lambda:clock[0]),patch.object(h,'kill_session_member',side_effect=kill_one) as kill:
            with self.assertRaisesRegex(h.GateError,'deadline'):h.wait_session_exit(42,1,kill=True)
        self.assertEqual(kill.call_count,1)


    def test_deadline_after_pidfd_read_no_signal(self):
        h=self.h;h._SESSION_KILL_MODE='pidfd';clock=[0]
        def stat(*args):clock[0]=2;return (31,'R',31,1,42,1)
        with patch.object(h.os,'pidfd_open',return_value=71),patch.object(h.os,'close') as close,patch.object(h,'proc_stat',side_effect=stat),patch.object(h.time,'monotonic',side_effect=lambda:clock[0]),patch.object(h.signal,'pidfd_send_signal') as send:
            with self.assertRaises(h.SessionDeadlineError):h.kill_session_member(42,31,1,1)
        send.assert_not_called();close.assert_called_once_with(71)


    def test_group_kill_and_wait_share_absolute_deadline(self):
        h=self.h
        with patch.object(h.time,'monotonic',return_value=10),patch.object(h.os,'killpg'),patch.object(h,'wait_session_exit') as wait:h.kill_session(42,1)
        self.assertEqual(wait.call_args.kwargs['deadline'],11)

    def test_old_group_apis_removed(self):
        for name in ('live_group_members','wait_group_exit','_ACTIVE_GROUP'):self.assertFalse(hasattr(self.h,name))
        self.assertIn('setsid()',H.read_text());self.assertIn('not cgroup containment',H.read_text())

    def test_setsid_escape_owned_process_outside_scan(self):
        # This directly owned child starts its own SID: the parent session scan
        # excludes it, and the test (not the helper) must clean it up.
        p=self.child();h=self.h
        self.assertNotEqual(os.getsid(p.pid),os.getsid(0))
        self.assertNotIn(p.pid,[m[0] for m in h.live_session_members(os.getsid(0),time.monotonic()+2)])
        self.assertIsNone(p.poll())


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2,failfast=True).run(unittest.defaultTestLoader.loadTestsFromTestCase(Hardening))
    Path(os.environ['TEST_RESULT']).write_text(json.dumps({'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'PASS':result.wasSuccessful()},indent=2)+'\n')
    sys.exit(not result.wasSuccessful())
