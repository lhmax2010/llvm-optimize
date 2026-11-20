from pathlib import Path
import contextlib
import io
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_jobs import (COMPILE, LINK, LINK_FLAGS, initial_args, install, require_rpm_log,
                        schedule_flags, verify)


class BuildJobsTests(unittest.TestCase):
    def setUp(self):
        self.counts = (4, 4, 1)
        self.args = [
            "-G", "Ninja", "-DLLVM_ENABLE_LTO=Thin", "-DCMAKE_CXX_FLAGS=-flto=thin -O3",
            f"-D{COMPILE}=6", f"-D{LINK}=2",
            f"-D{LINK_FLAGS[0]}=-fuse-ld=lld -flto=thin -Wl,--gc-sections -Wl,--build-id=sha1",
            f"-D{LINK_FLAGS[1]}=-fuse-ld=lld -flto=thin", "../llvm",
        ]

    def test_initial_flags_kept_including_identity_flags(self):
        result = initial_args(self.args, self.counts, "-Wl,-z,relro,--as-needed")
        self.assertIn("-DCMAKE_CXX_FLAGS=-flto=thin -O3", result)
        self.assertIn(f"-D{COMPILE}=4", result)
        self.assertIn(f"-D{LINK}=1", result)
        self.assertIn(self.args[6] + " -Wl,--thinlto-jobs=4", result)
        self.assertIn(f"-D{LINK_FLAGS[2]}=-Wl,-z,relro,--as-needed -Wl,--thinlto-jobs=4", result)

    def test_install_and_other_cmake_modes_are_untouched(self):
        self.assertIsNone(initial_args(["-P", "cmake_install.cmake"], self.counts, ""))
        self.assertIsNone(initial_args(["--build", "."], self.counts, ""))

    def test_missing_and_conflicting_scheduling_flags(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            initial_args(self.args[:-2], self.counts, "")
        with self.assertRaisesRegex(ValueError, "conflicting"):
            schedule_flags("-Wl,-plugin-opt=jobs=14", 4)
        self.assertEqual(schedule_flags("-Wl,--thinlto-jobs=6 -O1", 4), "-Wl,--thinlto-jobs=4 -O1")

    def test_install_generates_shell_without_building(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "var/tmp").mkdir(parents=True)
            inner = install(root, self.counts)
            shell = root / inner.lstrip("/")
            self.assertTrue(os.access(shell.with_name("cmake"), os.X_OK))
            probe = root / "probe.sh"
            probe.write_text('printf "%s %s %s\n" "$PROFILE_JOBS" "$PROFILE_THINLTO_JOBS" "$PROFILE_LINK_JOBS"\n')
            result = subprocess.check_output([str(shell), str(probe)], text=True)
            self.assertEqual(result, "4 4 1\n")

    def test_install_rejects_symlink_outside_prepared_root(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            root = parent / "root"
            (root / "var").mkdir(parents=True)
            (root / "var/tmp").symlink_to(parent, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "escapes the prepared root"):
                install(root, self.counts)
            self.assertFalse((parent / "llvm-stage-jobs").exists())

    def test_result_log_requires_verified_cache_pools_and_ninja(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "CMakeFiles").mkdir()
            (root / "CMakeFiles/rules.ninja").write_text("pool compile_job_pool\n  depth = 4\npool link_job_pool\n  depth = 1\n")
            (root / "CMakeCache.txt").write_text(
                f"{COMPILE}:STRING=4\n{LINK}:STRING=1\n" +
                "".join(f"{key}:STRING=-Wl,--thinlto-jobs=4\n" for key in LINK_FLAGS)
            )
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                verify(root, self.counts, "configure")
            log = root / "rpm.log"
            log.write_text(output.getvalue() + "[ 15s] + ninja -d keeprsp -j 4\n")
            with contextlib.redirect_stdout(output):
                require_rpm_log(log, self.counts)
            with self.assertRaisesRegex(ValueError, "missing effective"):
                require_rpm_log(log, (2, 2, 1))
