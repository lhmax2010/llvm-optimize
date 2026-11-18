import copy
import lzma
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from manifest import file_identity, generate, validate


class ManifestTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.raw = self.root / "raw.profdata"
        self.fdata = self.root / "raw.fdata"
        self.raw.write_bytes(b"profile")
        self.fdata.write_bytes(b"bolt profile")
        self.doc = generate(self.root, "T", "22.1.8", self.raw, self.fdata, {"test": True})

    def ready(self):
        self.doc["status"] = "READY"

    def test_generate_and_select_two_switch_modes(self):
        self.assertEqual(self.doc["status"], "UNQUALIFIED")
        self.ready()
        self.assertIn("bolt_profile", validate(self.doc, self.root, "T", True, True))
        self.assertNotIn("bolt_profile", validate(self.doc, self.root, "T", True, False))

    def test_disabled_fallback(self):
        self.ready()
        self.assertEqual(validate(self.doc, self.root, "D", False, True), {"baseline": True})
        self.assertIsNone(validate(self.doc, self.root, "D", False, False))

    def test_unqualified_requires_opt_in(self):
        with self.assertRaisesRegex(ValueError, "unqualified"):
            validate(self.doc, self.root, "T", True, True)
        self.assertIn("bolt_profile", validate(self.doc, self.root, "T", True, True, allow_unqualified=True))

    def test_placeholder_status_rejected_even_with_opt_in(self):
        self.doc["status"] = "PLACEHOLDER"
        with self.assertRaisesRegex(ValueError, "PLACEHOLDER"):
            validate(self.doc, self.root, "T", True, True, allow_unqualified=True)

    def test_placeholder_asset_with_correct_hashes_rejected(self):
        self.ready()
        row = self.doc["profiles"][1]["profdata"]
        self.raw.write_bytes(b"PLACEHOLDER\n")
        asset = self.root / row["file"]
        asset.write_bytes(lzma.compress(self.raw.read_bytes()))
        compressed = file_identity(asset)
        row.update(file_identity(self.raw), xz_sha256=compressed["sha256"], xz_bytes=compressed["bytes"])
        with self.assertRaisesRegex(ValueError, "placeholder profile"):
            validate(self.doc, self.root, "T", True, True)

    def test_compressed_digest_rejected(self):
        self.ready()
        self.doc["profiles"][1]["profdata"]["xz_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "compressed profile identity"):
            validate(self.doc, self.root, "T", True, True)

    def test_uncompressed_digest_rejected(self):
        self.ready()
        self.doc["profiles"][1]["profdata"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "uncompressed profile identity"):
            validate(self.doc, self.root, "T", True, True)

    def test_missing_and_duplicate_mappings(self):
        self.ready()
        with self.assertRaisesRegex(ValueError, "missing"):
            validate(self.doc, self.root, "D", True, True)
        self.doc["profiles"].append(copy.deepcopy(self.doc["profiles"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            validate(self.doc, self.root, "T", True, True)

    def test_path_traversal_rejected(self):
        self.ready()
        self.doc["profiles"][1]["profdata"]["file"] = "../unexpected.xz"
        with self.assertRaisesRegex(ValueError, "basename"):
            validate(self.doc, self.root, "T", True, True)
