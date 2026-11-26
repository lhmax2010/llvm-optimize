import sys
import tempfile
import unittest
from pathlib import Path

A = Path(__file__).resolve().parent
sys.path.insert(0, str(A / "orchestration"))
from handoff import runtime_library


class LoaderListing(unittest.TestCase):
    def test_confines_the_loader_self_reference(self):
        with tempfile.TemporaryDirectory(dir=A) as name:
            parent = Path(name)
            root = parent / "root"
            root.mkdir()
            loader = root / "ld-linux-x86-64.so.2"
            library = root / "libc.so.6"
            outside = parent / loader.name
            for path in (loader, library, outside):
                path.touch()
            alias = "/lib64/ld-linux-x86-64.so.2"
            self.assertIsNone(runtime_library(f"\t{alias} => {loader} (0x0)", root, loader))
            self.assertEqual(runtime_library(f"\tlibc.so.6 => {library} (0x0)", root, loader),
                             ("libc.so.6", library))
            for label, path in ((alias, library), (alias, outside), ("/other/"+loader.name, loader)):
                with self.subTest(label=label, path=path), self.assertRaisesRegex(RuntimeError, "unexpected runtime"):
                    runtime_library(f"\t{label} => {path} (0x0)", root, loader)


if __name__ == "__main__":
    unittest.main()
