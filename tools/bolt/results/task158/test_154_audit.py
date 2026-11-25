from pathlib import Path
import json
import tempfile
import unittest

from corpus_gate import corpus_terminal
from rpm_python_audit import bytecode_audit, dependency_diff


class RpmAuditTests(unittest.TestCase):
    def test_python_and_abi_and_tools_are_detected(self):
        result = dependency_diff(
            "python3\nlibc.so\n",
            "python3\nlibc.so\npython(abi) = 3.12\n/usr/bin/python3\npython3dist(foo)\nlibpython3.12.so\nlibssl",
        )
        self.assertEqual(result["added_python"],
                         ["/usr/bin/python3", "libpython3.12.so", "python(abi) = 3.12", "python3dist(foo)"])
        self.assertIn("libssl", result["added"])

    def test_existing_python_is_not_new(self):
        self.assertEqual(dependency_diff("python3\n", "python3\nq\n")["added_python"], [])

    def test_no_bytecode(self):
        result = bytecode_audit(["/usr/lib/libscanbuild/a.py", "/usr/lib/libear/x.py"])
        self.assertEqual((result["status"], result["bytecode"]), ("PASS", "ABSENT"))

    def test_all_sources_have_bytecode(self):
        roots = ["/usr/lib/libscanbuild", "/usr/lib/libear"]
        paths = [roots[0] + name for name in ("/a.py", "/__pycache__", "/__pycache__/a.cpython-312.opt-1.pyc")]
        paths.extend([roots[1] + "/b.py", roots[1] + "/b.pyc"])
        self.assertEqual(bytecode_audit(paths)["status"], "PASS")

    def test_partial_or_orphan_bytecode(self):
        result = bytecode_audit(["/usr/lib/libscanbuild/a.py", "/usr/lib/libear/b.pyc",
                                 "/usr/lib/libscanbuild/__pycache__"])
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["missing_bytecode"], ["/usr/lib/libscanbuild/a.py"])
        self.assertEqual(result["orphans"], ["/usr/lib/libear/b.pyc", "/usr/lib/libscanbuild/__pycache__"])

    def test_other_directories_excluded(self):
        result = bytecode_audit(["/usr/lib/libear-unrelated/a.pyc", "/usr/lib/libear/a.py"])
        self.assertEqual(result["files"], ["/usr/lib/libear/a.py"])

    def test_gate_waits_for_terminal_status_and_no_active_child(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "receipt.json"
            self.assertIsNone(corpus_terminal(path)[0])
            path.write_text("{")
            self.assertIsNone(corpus_terminal(path)[0])
            for status, active, admitted in (("RUNNING", False, False), ("BUDGET_EXPIRED", True, False),
                                             ("BUDGET_EXPIRED", False, True), ("PARTIAL", False, True)):
                path.write_text(json.dumps(dict(status=status, package_build_active=active)))
                self.assertEqual(corpus_terminal(path)[0] is not None, admitted)


if __name__ == "__main__":
    unittest.main()
