import copy
import importlib.util
import lzma
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "task157/candidate.py"
spec = importlib.util.spec_from_file_location("candidate", SOURCE)
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)


class TestStatus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = candidate.show(candidate.RECIPE, candidate.HELPER)
        cls.verification = candidate.verification_helper(cls.original)

    def setUp(self):
        directory = tempfile.TemporaryDirectory(dir=HERE)
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.manifest = self.root / "manifest.json"
        self.helper = self.root / "helper.py"
        self.counter = 0
        self.profile, info = self.asset("clang.profdata", b"profile test bytes")
        self.bolt, bolt_info = self.asset("clang.fdata", b"paired fdata")
        pair = {"project": "T", "pgo": True, "bolt": False, "profdata": info}
        self.doc = {"format": 1, "llvm_version": "22.1.8", "status": "UNQUALIFIED",
                    "profiles": [pair, dict(pair, bolt=True, bolt_profile=bolt_info)]}

    def asset(self, name, data):
        plain = self.root / name
        plain.write_bytes(data)
        packed = plain.with_suffix(plain.suffix + ".xz")
        return packed, candidate.pack(plain, packed)

    def invoke(self, doc, *, original=False, project="T", bolt=False):
        self.counter += 1
        self.helper.write_text(self.original if original else self.verification)
        self.manifest.write_text(doc if isinstance(doc, str) else json.dumps(doc))
        cmd = [sys.executable, "-B", self.helper, "pgo-prepare", self.manifest,
               project, self.root / ("result-" + str(self.counter)), self.profile]
        if bolt:
            cmd += ["--bolt-profile", self.bolt]
        return subprocess.run(cmd, text=True, capture_output=True, timeout=20)

    def reject(self, doc, message, **kwargs):
        p = self.invoke(doc, **kwargs)
        self.assertEqual(p.returncode, 1, p.stdout + p.stderr)
        self.assertIn(message, p.stdout + p.stderr)

    def test_integration_rejects_unqualified_for_both_mappings(self):
        for bolt in (False, True):
            self.reject(self.doc, "profile manifest is not READY", original=True, bolt=bolt)

    def test_verification_accepts_unqualified_for_both_mappings(self):
        for bolt in (False, True):
            p = self.invoke(self.doc, bolt=bolt)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertEqual((self.root / f"result-{self.counter}/clang.profdata").read_bytes(), b"profile test bytes")
            if bolt:
                self.assertEqual((self.root / f"result-{self.counter}/clang.fdata").read_bytes(), b"paired fdata")

    def test_production_ready_still_works(self):
        p = self.invoke(dict(self.doc, status="READY"), original=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_placeholder_status_rejected(self):
        self.reject(dict(self.doc, status="PLACEHOLDER"), "profile manifest is not READY")

    def test_unknown_status_rejected(self):
        self.reject(dict(self.doc, status="QUALIFIED"), "profile manifest is not READY")

    def test_placeholder_bytes_rejected(self):
        payload = b"PLACEHOLDER content"
        self.profile = self.root / "placeholder.profdata.xz"
        self.profile.write_bytes(lzma.compress(payload))
        info = dict(self.doc["profiles"][0]["profdata"], file=self.profile.name,
                    sha256=candidate.hashlib.sha256(payload).hexdigest(), bytes=len(payload),
                    xz_sha256=candidate.file_identity(self.profile)["sha256"],
                    xz_bytes=self.profile.stat().st_size)
        self.doc["profiles"][0]["profdata"] = info
        self.reject(self.doc, "placeholder profile payload")

    def test_all_asset_identities_checked(self):
        for key, value, diagnostic in (
            ("sha256", "0" * 64, "uncompressed profile identity mismatch"),
            ("xz_sha256", "0" * 64, "compressed profile identity mismatch"),
            ("bytes", 100, "uncompressed profile identity mismatch"),
            ("xz_bytes", 100, "compressed profile identity mismatch"),
        ):
            for bolt in (False, True):
                with self.subTest(key=key, bolt=bolt):
                    doc = copy.deepcopy(self.doc)
                    item = doc["profiles"][int(bolt)]
                    item["bolt_profile" if bolt else "profdata"][key] = value
                    self.reject(doc, diagnostic, bolt=bolt)

    def test_project_and_switch_mapping_enforced(self):
        self.reject(self.doc, "missing profile mapping", project="D")
        invalid_project = self.invoke(self.doc, project="X")
        self.assertEqual(invalid_project.returncode, 2)
        self.assertIn("invalid choice", invalid_project.stderr)
        self.reject(dict(self.doc, profiles=self.doc["profiles"][:1]), "missing profile mapping", bolt=True)
        invalid = dict(self.doc["profiles"][0], pgo=False)
        self.reject(dict(self.doc, profiles=[invalid]), "invalid profile mapping key")

    def test_duplicate_mapping_rejected(self):
        self.reject(dict(self.doc, profiles=self.doc["profiles"] * 2), "duplicate profile mapping")

    def test_duplicate_json_fields_rejected(self):
        self.reject(json.dumps(self.doc).replace('{"format": 1,', '{"format": 1, "format": 1,'), "duplicate")


if __name__ == "__main__":
    unittest.main()
