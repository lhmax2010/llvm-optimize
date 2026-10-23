"""Best-effort cache release and observation after release."""
import contextlib, errno, io, json, stat, sys
from pathlib import Path
from unittest.mock import patch
import bolt_helper as h
from test_bolt_helper import Base, EDGE

class CacheReleaseTests(Base):
    def setUp(self):
        super().setUp()
        self.build=self.d/'build';self.work=self.build/'clang-bolt'
        self.work.mkdir(parents=True);self.cache=self.build/'lto.cache'
        self.cache.mkdir();(self.cache/'data').write_bytes(b'x'*8192)
        self.edge=__import__('re').sub(r'--thinlto-cache-dir=([^\s]+)', '--thinlto-cache-dir='+str(self.cache), EDGE)
        (self.work/'link.original').write_text(self.edge)
    def run_release(self):
        out=io.StringIO()
        with contextlib.redirect_stdout(out),patch.object(sys,'argv',['helper','cache-release',str(self.build),str(self.work)]):
            rc=h.cli()
        self.assertEqual(rc,0)
        return out.getvalue()
    def test_normal(self):
        expected=sum(x['allocated_bytes'] for x in h.disk_entries(self.cache).values())
        self.assertIn('removed path=',self.run_release());self.assertFalse(self.cache.exists())
        record=json.loads((self.work/'cache-release.json').read_text())
        self.assertEqual(record['files'],1);self.assertEqual(record['allocated_bytes'],expected)
    def test_redirect(self):
        other=self.d/'other';other.mkdir();(other/'keep').write_text('keep')
        (self.work/'link.original').write_text(self.edge.replace(str(self.cache),str(other)))
        self.assertIn('outside-build-cache',self.run_release());self.assertTrue((other/'keep').exists())
    def test_symlink(self):
        other=self.d/'other';self.cache.rename(other);self.cache.symlink_to(other)
        self.assertIn('symlink',self.run_release());self.assertTrue((other/'data').exists())
    def test_missing(self):
        h.shutil.rmtree(self.cache)
        self.assertIn('not-a-directory-or-missing',self.run_release())
    def test_partial(self):
        (self.cache/'second').write_text('remain')
        def failed(path):
            (path/'data').unlink();raise PermissionError('fixture denied')
        with patch.object(h.shutil,'rmtree',side_effect=failed):
            self.assertIn('partial error=fixture denied remaining_files=1',self.run_release())
        self.assertTrue((self.cache/'second').exists())
    def test_invalid_edge(self):
        (self.work/'link.original').write_text(self.edge.replace(' && :',' --thinlto-cache-dir=/elsewhere && :'))
        self.assertIn('skipped reason=',self.run_release());self.assertTrue(self.cache.exists())
    def test_index_error_is_skipped_and_recorded(self):
        with patch.object(h, 'replay_script', side_effect=IndexError('fixture empty paths')):
            output = self.run_release()
        self.assertIn('BOLT_CACHE_RELEASE skipped reason=fixture empty paths', output)
        record = json.loads((self.work/'cache-release.json').read_text())
        self.assertEqual(record['status'], 'skipped')
        self.assertEqual(record['reason'], 'fixture empty paths')
        self.assertTrue((self.cache/'data').exists())
    def test_missing_edge(self):
        (self.work/'link.original').unlink()
        self.assertIn('skipped reason=',self.run_release());self.assertTrue(self.cache.exists())
    def test_record_full(self):
        with patch.object(h,'save',side_effect=OSError(errno.ENOSPC,'No space left on device')):
            self.assertIn('record-unavailable',self.run_release())
        self.assertFalse(self.cache.exists())
    def test_usage(self):
        with patch.object(sys,'argv',['helper','cache-release']),contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as got:h.cli()
        self.assertEqual(got.exception.code,2)
    def test_report_and_diagnosis_after_release(self):
        with contextlib.redirect_stdout(io.StringIO()):before=h.disk_report('begin',self.build,self.work)
        allocated=sum(x['allocated_bytes'] for x in h.disk_entries(self.cache).values())
        self.run_release()
        log=self.work/'failure.log';log.write_text('fixture ordinary gate failure')
        with contextlib.redirect_stdout(io.StringIO()) as out:
            after=h.disk_report('post',self.build,self.work)
            h.disk_diagnose('post',log,build=self.build,work=self.work)
        self.assertTrue(after['recorded']);self.assertEqual(after['cache_delta_allocated_bytes'],0)
        self.assertEqual(after['cache_net_allocation_delta_bytes'],-allocated)
        self.assertIn('"cause": "not-disk"',out.getvalue())
        log.write_text('No space left on device')
        with contextlib.redirect_stdout(io.StringIO()) as out:
            h.disk_diagnose('post',log,build=self.build,work=self.work)
        self.assertIn('"cause": "disk"',out.getvalue());self.assertNotIn('diagnostic_error',out.getvalue())
