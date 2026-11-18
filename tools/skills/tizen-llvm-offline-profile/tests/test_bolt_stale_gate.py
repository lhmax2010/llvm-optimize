import sys
from pathlib import Path
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import bolt_stale_gate as h


def log(n=100, m=1000, s=None, u=None, q=None):
    v='BOLT-INFO: %s out of %s functions in the binary (10.0%%) have non-empty execution profile\n' % (n,m)
    if s is not None:v+='BOLT-WARNING: %s (5.0%% of all profiled) functions have invalid (possibly stale) profile. Use -report-stale to see the list.\n' % s
    if u is not None:v+='BOLT-INFO: profile for %s objects was ignored\n' % u
    if q is not None:v+='BOLT-INFO: %s functions with profile could not be optimized\n' % q
    return v


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


class TransportTests(unittest.TestCase):
    def test_truncated_transport(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rewrite.txt"
            path.write_text(log().rstrip("\n"))
            with self.assertRaisesRegex(h.GateError, "truncated"):
                h.audit_log(path, ["-stale-threshold=5"], True, True)

    def test_literal_threshold_required(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rewrite.txt"
            path.write_text(log())
            for argv in ([], ["-stale-threshold=6"], ["-stale-threshold=5"] * 2):
                with self.subTest(argv=argv), self.assertRaisesRegex(h.GateError, "exactly one"):
                    h.audit_log(path, argv, True, True)
            self.assertEqual(h.audit_log(path, ["-stale-threshold=5"], True, True)["N"], 100)

    def test_extra_malformed_counter_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rewrite.txt"
            path.write_text(log(s=1) + "BOLT-WARNING: -1 (5%) functions have invalid (possibly stale) profile.\n")
            with self.assertRaisesRegex(h.GateError, "malformed"):
                h.audit_log(path, ["-stale-threshold=5"], True, True)
