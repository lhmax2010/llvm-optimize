from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
import build_cleanup
from stage_resources import GIB, admission, budget


class BuildCleanupTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.tree = self.root / "build"
        self.tree.mkdir()
        (self.tree / "first").write_text("keep until the preflight passes")
        (self.tree / "nested").mkdir()
        (self.tree / "nested" / "artifact").touch()

    def test_normal_tree(self):
        build_cleanup.remove_tree(self.root, self.tree)
        self.assertFalse(self.tree.exists())
        self.assertTrue(self.root.is_dir())

    def test_nested_symlinks_are_unlinked_without_following(self):
        external = self.root / "retain"
        external.mkdir()
        data = external / "data"
        data.write_bytes(b"preserve me")
        (self.tree / "alias").symlink_to(external, target_is_directory=True)
        (self.tree / "broken-link").symlink_to(external / "missing")
        build_cleanup.remove_tree(self.root, self.tree)
        self.assertEqual(data.read_bytes(), b"preserve me")

    def test_different_device_refuses_before_deletion(self):
        original = os.stat

        def foreign(path, *args, **kwargs):
            result = original(path, *args, **kwargs)
            if path == "nested" and kwargs.get("dir_fd") is not None:
                return SimpleNamespace(st_dev=result.st_dev + 1)
            return result

        with patch.object(build_cleanup.os, "stat", side_effect=foreign):
            with self.assertRaisesRegex(ValueError, "different st_dev"):
                build_cleanup.remove_tree(self.root, self.tree)
        self.assertTrue((self.tree / "first").is_file())
        self.assertTrue((self.tree / "nested" / "artifact").is_file())

    def test_same_device_mount_refuses_before_deletion(self):
        with patch.object(build_cleanup, "mount_points", return_value={self.tree / "nested"}):
            with self.assertRaisesRegex(ValueError, "mount"):
                build_cleanup.remove_tree(self.root, self.tree)
        self.assertTrue((self.tree / "first").is_file())

    def test_outside_path_and_anchor_are_refused(self):
        other = self.root / "other"
        other.mkdir()
        for rejected in (other, self.tree):
            with self.assertRaisesRegex(ValueError, "outside"):
                build_cleanup.remove_tree(self.tree, rejected)
        alias = self.root / "alias"
        alias.symlink_to(self.tree)
        with self.assertRaisesRegex(ValueError, "symlink-free"):
            build_cleanup.remove_tree(self.root, alias)


class StageResourcesTests(unittest.TestCase):
    def test_full_build_tier_boundaries(self):
        for available, jobs in ((14*GIB, 2), (18*GIB-1, 2), (18*GIB, 4),
                                (24*GIB-1, 4), (24*GIB, 6), (40*GIB, 6)):
            with self.subTest(available=available):
                plan = admission("full-build", available)
                self.assertEqual(plan["jobs"], jobs)
                self.assertEqual(plan["thinlto_jobs"], jobs)
                self.assertEqual(plan["link_jobs"], 1)
                self.assertTrue(plan["admitted"])
        self.assertEqual(admission("full-build", 40*GIB)["memory_max"], 24*GIB)

    def test_floors_and_historical_evening(self):
        for stage in ("full-build", "pgo-build", "bolt-tools-relink"):
            floor = budget(stage)[1]
            self.assertTrue(admission(stage, floor+4*GIB)["admitted"])
            self.assertFalse(admission(stage, floor+4*GIB-1)["admitted"])
            plan = admission(stage, 19*GIB)
            self.assertEqual((plan["memory_max"], plan["jobs"]), (15*GIB, 4))
        stage = "bolt-instrument-train-merge"
        self.assertFalse(admission(stage, 19*GIB)["admitted"])
        self.assertFalse(admission(stage, 22*GIB-1)["admitted"])
        plan = admission(stage, 22*GIB)
        self.assertTrue(plan["admitted"])
        self.assertEqual((plan["memory_max"], plan["jobs"], plan["thinlto_jobs"]), (18*GIB, 1, None))

    def test_watchdog_limits(self):
        from stage_resources import WATCHDOG_DISK, WATCHDOG_MEMORY
        self.assertEqual((WATCHDOG_MEMORY, WATCHDOG_DISK), (3*GIB, 15*GIB))
