"""Debug symbols must be opt-in for the debug RPM branch."""
import contextlib
from unittest.mock import patch
import bolt_helper as h
from test_bolt_helper import Base

class DebugModeTests(Base):
    def exercise(self, enabled):
        work=self.d/'work';work.mkdir()
        (work/'installed-baseline.json').write_text('{}')
        (work/'link.original').write_text('link')
        identity={'after_sha256':'test'}
        with contextlib.ExitStack() as stack:
            mocks={name:stack.enter_context(patch.object(h,name)) for name in
                ('replay_script','call','rewrite','tiny_gate','real_gate','separate_debug_symbols',
                 'strip_all','adjust_rpath','add_debuglink','security_compare')}
            mocks['replay_script'].return_value='script'
            mocks['rewrite'].return_value={}
            mocks['real_gate'].return_value={}
            mocks['security_compare'].return_value={}
            mocks['strip_all'].return_value=identity
            mocks['adjust_rpath'].return_value=identity
            mocks['add_debuglink'].return_value=identity
            mocks['separate_debug_symbols'].return_value={'symbols':True}
            args={'debug_symbols':True} if enabled else {}
            result=h.pipeline(self.d,work,'bolt',**args)
            self.assertEqual(mocks['separate_debug_symbols'].call_count,int(enabled))
            self.assertEqual(mocks['add_debuglink'].call_count,int(enabled))
            self.assertEqual(mocks['tiny_gate'].call_count,2)
            self.assertEqual(mocks['real_gate'].call_count,2)
            self.assertEqual(result['identity'],identity)
    def test_release_default_no_symbol_file_or_debuglink(self):self.exercise(False)
    def test_debug_extracts_and_adds_debuglink(self):self.exercise(True)
