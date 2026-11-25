from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import runtime_dep_check as r


class RuntimeGateTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.archive = self.root / "usr/lib64/libtest.a"
        self.archive.parent.mkdir(parents=True)
        # Mock readelf; the magic identifies the object routed to it.
        self.archive.write_bytes(r.ARCHIVE)
        self.reader = Path("/path/to/llvm-readelf")

    @staticmethod
    def tool(lines, code=0):
        child = MagicMock()
        child.__enter__.return_value = child
        child.stdout = iter(lines)
        child.wait.return_value = code
        return child

    def test_profile_sections_symbols_and_dependency(self):
        observed = [
            "File: libtest.a(a.o)",
            "  [8] __llvm_prf_cnts PROGBITS",
            "  4: 0000 4 NOTYPE GLOBAL DEFAULT UND __llvm_profile_register_function",
            "  0x0001 (NEEDED) Shared library: [libclang_rt.profile-x86_64.so]",
            "  0x0001 (NEEDED) Shared library: [libLLVM.so]",
        ]
        with patch.object(r.subprocess, "Popen", return_value=self.tool(observed)):
            result = r.audit(self.root, self.reader)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(len(result["findings"]), 3)

    def test_clean_member(self):
        with patch.object(r.subprocess, "Popen", return_value=self.tool(["File: libtest.a(a.o)", "  [1] .text PROGBITS"])) as run:
            result = r.audit(self.root, self.reader)
        self.assertEqual((result["status"], result["archives"]), ("PASS", 1))
        self.assertEqual(run.call_args.args[0][-1], str(self.archive))

    def test_reader_errors_fail_closed(self):
        with patch.object(r.subprocess, "Popen", return_value=self.tool(["error: invalid member"], code=1)):
            result = r.audit(self.root, self.reader)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(len(result["findings"]), 2)

    def test_thin_archive_rejected(self):
        self.archive.write_bytes(r.THIN)
        with patch.object(r.subprocess, "Popen") as run:
            result = r.audit(self.root, self.reader)
        run.assert_not_called()
        self.assertEqual(result["status"], "FAIL")

    def test_elf_exec_is_audited(self):
        self.archive.unlink()
        path = self.root / "clang"
        path.write_bytes(r.ELF + bytes([2, 1]) + b"\0" * 10 + b"\x03\0\0\0")
        with patch.object(r.subprocess, "Popen", return_value=self.tool(["  [1] .text PROGBITS"])):
            self.assertEqual(r.audit(self.root, self.reader)["elf"], 1)

    def test_resource_runtime_archive_is_not_a_static_devel_archive(self):
        resource = self.root / "usr/lib64/clang/22/lib/linux/libclang_rt.profile-x86_64.a"
        resource.parent.mkdir(parents=True)
        resource.write_bytes(r.ARCHIVE)
        with patch.object(r.subprocess, "Popen", return_value=self.tool(["  [1] .text PROGBITS"])) as run:
            result = r.audit(self.root, self.reader)
        self.assertEqual((result["status"], result["archives"]), ("PASS", 1))
        self.assertEqual(run.call_count, 1)
        self.assertEqual(run.call_args.args[0][-1], str(self.archive))
