import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import unittest
from unittest.mock import patch

WORK = Path(__file__).resolve().parents[3]
EVIDENCE = WORK.with_name(WORK.name + "-bolt")
sys.path.insert(0, str(EVIDENCE / "tools/skills/tizen-llvm-offline-profile/scripts"))
from pgo_pair import check_compile_db
from pgo_pair import scan_pgo_commands as skill_scan

helper = WORK / "temp/task131/pgo-dev/packaging/clang-bolt-helper.py"
spec = importlib.util.spec_from_file_location("recipe_helper", helper)
recipe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recipe)

PROFILE = "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/pgo-profiles/clang.profdata"
FLAG = "-fprofile-instr-use=" + PROFILE


def compile_edge(output, *flags, source="llvm.cpp", directory="/build"):
    return {"file": source, "output": output, "directory": directory,
            "command": " ".join(["clang++", "-c", source, "-o", output, *flags])}


class PgoGateTests(unittest.TestCase):
    def both(self, rows, expected=PROFILE):
        product = recipe.scan_pgo_commands(rows, expected)
        skill = skill_scan(rows, expected)
        self.assertEqual(product, skill)
        return product

    def test_historical_duplicate_link_and_startup_object(self):
        evidence = EVIDENCE / "tools/bolt/results/task149-run"
        first = (evidence / "first-attempt/G4-rpm-build.txt").read_text()
        second = (evidence / "g4-retry/rpm-build.txt").read_text()
        self.assertIn(f"wrong PGO option for bin/llvm-min-tblgen: {str([FLAG, FLAG])}", first)
        output = "lib64/clang/22/lib/linux/clang_rt.crtbegin-x86_64.o"
        self.assertIn(f"wrong PGO option for {output}: []", second)
        report = self.both([{"file": "tblgen.o", "output": "bin/llvm-min-tblgen",
                             "command": f"clang++ {FLAG} tblgen.o -o bin/llvm-min-tblgen {FLAG}"},
                            compile_edge(output), compile_edge("tblgen.o", FLAG)])
        self.assertEqual(report["violation_count"], 0)
        self.assertEqual(report["runtime_compile"], 1)
        self.assertEqual(report["profile_use"], 1)

    def test_runtime_directories_basename_and_subbuild_cases(self):
        for row in (compile_edge("lib/clang/22.1.8/lib/linux/foreign-startup.o"),
                    compile_edge("objects/clang_rt.crtend-x86_64.o"),
                    compile_edge("out/libclang_rt.profile-x86_64.a"),
                    compile_edge("out/init.o", source="../compiler-rt/lib/x.c"),
                    compile_edge("out/init.o", directory="/build/openmp"),
                    compile_edge("out/init.o", source="../openmp/runtime/src/runtime.cpp"),
                    {"output": "runtime-stamp", "command": "cmake --build=/build/openmp"}):
            with self.subTest(row=row):
                self.assertEqual(self.both([row])["violation_count"], 0)
                flagged = {**row, "command": row["command"] + " " + FLAG}
                self.assertEqual(self.both([flagged])["violations"][0]["category"], "runtime")

    def test_all_main_compile_violations_and_runtime_flags_are_reported(self):
        rows = [compile_edge("missing.o"), compile_edge("wrong.o", "-fprofile-instr-use=/wrong"),
                compile_edge("extra.o", FLAG, FLAG),
                compile_edge("compiler-rt/out.o", "-fprofile-instr-generate")]
        report = self.both(rows)
        self.assertEqual(report["violation_count"], 4)
        self.assertEqual([item["edge"] for item in report["violations"]], [1, 2, 3, 4])
        self.assertEqual([item["category"] for item in report["violations"]],
                         ["main_compile", "main_compile", "main_compile", "runtime"])
        self.assertEqual([item["options"] for item in report["violations"]],
                         [[], ["-fprofile-instr-use=/wrong"], [FLAG, FLAG], ["-fprofile-instr-generate"]])
        with patch("builtins.print") as printed, self.assertRaises(recipe.GateError):
            recipe.check_pgo_commands(rows, PROFILE)
        self.assertEqual(json.loads(printed.call_args.args[1]), report)
        with self.assertRaises(RuntimeError):
            check_compile_db(rows, PROFILE)
        self.assertEqual(check_compile_db(rows, PROFILE, report=True), report)

    def test_link_only_and_identical_paths_only(self):
        for command in (f"clang++ {FLAG} {FLAG} {FLAG} -o x x.o",
                        f"clang++ {FLAG} -fprofile-instr-use=/wrong -o x x.o",
                        f"clang++ -S {FLAG} {FLAG} -o x x.cpp"):
            with self.subTest(command=command):
                self.assertEqual(self.both([{"output": "x", "command": command}])["violation_count"], 1)
        self.assertEqual(self.both([compile_edge("x.o", FLAG)], None)["violations"][0]["category"], "disabled")

    def test_a_bad_shell_token_does_not_stop_the_scan(self):
        report = self.both([{"output": "x", "command": "clang++ '"}, compile_edge("next.o")])
        self.assertEqual([item["category"] for item in report["violations"]], ["parse", "main_compile"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
