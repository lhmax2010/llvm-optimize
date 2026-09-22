#!/usr/bin/env python3
"""Small regression checks for measurement validity and resource enforcement."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import bench_toolchain as bench


class HarnessChecks(unittest.TestCase):
    def test_loader_library_path_is_explicit_and_fingerprinted(self):
        root = self.temporary()
        (root / 'bin').mkdir()
        library = root / 'runtime'
        library.mkdir()
        (library / 'libexample.so.1').write_bytes(b'runtime-v1')
        for name in ('clang', 'clang++', 'ld.lld', 'llvm-ar'):
            (root / 'bin' / name).symlink_to('/usr/bin/true')
        stdout = root / 'version.txt'
        stdout.write_text('fixture version\n')
        seen = []
        class FakeRunner:
            def command(self, argv, **kwargs):
                seen.append(argv)
                return {'stdout': str(stdout)}
        args = SimpleNamespace(roots={'test': root}, loaders={'test': Path('/usr/bin/true')},
                               library_paths={'test': library})
        first = bench.toolchains(args, FakeRunner())
        self.assertTrue(all(argv[:3] == ['/usr/bin/true', '--library-path', str(library)] for argv in seen))
        (library / 'libexample.so.1').write_bytes(b'runtime-v2')
        second = bench.toolchains(args, FakeRunner())
        self.assertNotEqual(first['test']['runtime_sha256'], second['test']['runtime_sha256'])

    def temporary(self):
        temp = tempfile.TemporaryDirectory(dir=bench.WORKSPACE / "temp")
        self.addCleanup(temp.cleanup)
        return Path(temp.name)

    def sample(self, wall, suspect=False):
        return dict(wall_s=wall, user_s=wall / 2, sys_s=wall / 4,
                    max_rss_kib=1234, suspect=suspect)

    def result(self):
        samples = [dict(self.sample(v), iteration=i, discarded=i == 0)
                   for i, v in enumerate((100, 10, 10, 10, 10))]
        protocol = {"calibration_policy": bench.CALIBRATION_POLICY, "runs": 5,
                    "inputs": [{"name": "A", "sha256": "a"*64}]}
        fixture = [{"name": "part-0.o", "bytes": 1, "sha256": "b"*64}]
        value = {"samples": samples, "summary": bench.summarize(samples)}
        return dict(schema=bench.SCHEMA, status="MEASURED",
                    protocol_hash=bench.json_digest(protocol), fixture_hash=bench.json_digest(fixture),
                    fixture_objects=fixture, toolchains={"a": "same"}, protocol=protocol,
                    results={"a": {k: copy.deepcopy(value) for k in ("A", "ld.lld", "llvm-ar")}})

    def change_case(self, result, case, factor=1, suspect=False, uneven=False):
        value = result["results"]["a"][case]
        for sample in value["samples"]:
            sample["wall_s"] *= factor
        if suspect: value["samples"][1]["suspect"] = True
        if uneven: value["samples"][1]["wall_s"] *= 1.5
        value["summary"] = bench.summarize(value["samples"])
        if suspect: result["status"] = "MEASURED_WITH_WARNINGS"

    def test_discard_warmup_and_sample_standard_deviation(self):
        values = [self.sample(v) for v in (1000, 1, 2, 3, 4)]
        result = bench.summarize(values)
        self.assertEqual(result["statistics"]["wall_s"]["median"], 2.5)
        self.assertEqual(result["statistics"]["wall_s"]["min"], 1)
        self.assertAlmostEqual(result["statistics"]["wall_s"]["stddev"], (5 / 3) ** .5)

    def test_bad_warmup_does_not_taint_retained_samples(self):
        samples = [self.sample(100, True)] + [self.sample(10) for _ in range(4)]
        self.assertEqual(bench.summarize(samples)["suspect_retained"], 0)

    def test_noise_gate(self):
        first = self.result(); second = copy.deepcopy(first)
        self.change_case(second, "A", factor=1.05)
        self.assertEqual(bench.calibration(first, second)["status"], "FAIL")
        second = copy.deepcopy(first); self.change_case(second, "A", suspect=True)
        self.assertEqual(bench.calibration(first, second)["status"], "FAIL")
        self.assertEqual(bench.calibration(first, first)["status"], "PASS")

    def test_noise_gate_refuses_changed_fixture_or_protocol(self):
        for key in ("fixture_hash", "protocol_hash", "toolchains"):
            first, second = self.result(), self.result(); second[key] = "changed"
            with self.assertRaises(bench.BenchError): bench.calibration(first, second)

    def test_link_archive_timing_only_cannot_fail_compilation_gate(self):
        first = self.result(); second = copy.deepcopy(first)
        for case in ('ld.lld','llvm-ar'): self.change_case(second,case,1.2,uneven=True)
        result=bench.calibration(first,second)
        self.assertEqual(result['status'],'PASS'); self.assertEqual(result['noise_floor_pct'],0)
        self.assertEqual(result['calibration_policy'],'compile-only-v3')
        self.assertEqual([r['diagnostic_only'] for r in result['rows']],[False,True,True])
        self.change_case(second,'A',1.04)
        self.assertEqual(bench.calibration(first,second)['status'],'FAIL')

    def test_lld_suspect_is_environment_failure(self):
        first=self.result();second=copy.deepcopy(first)
        self.change_case(second,'ld.lld',suspect=True)
        result=bench.calibration(first,second)
        self.assertEqual(result['status'],'FAIL')
        self.assertTrue(result['suspect_any_row']);self.assertTrue(result['suspect_diagnostic_only'])
        self.assertEqual(result['noise_floor_pct'],0)

    def test_symmetric_deletion_and_forgery_rejected(self):
        mutations=[
            lambda r:r['results']['a'].pop('A'),
            lambda r:r['results']['a'].pop('ld.lld'),
            lambda r:r.update(protocol_hash='f'*64),
            lambda r:r['protocol'].update(runs=6),
            lambda r:r['results']['a']['A']['samples'].pop(),
            lambda r:r.update(status='FAILED'),
            lambda r:r['results']['a']['A']['summary']['statistics']['wall_s'].update(median=1),
            lambda r:r['results']['a']['A']['summary'].pop('retained'),
            lambda r:r['results']['a']['A']['samples'][1].update(discarded=True),
            lambda r:r['results']['a']['A']['samples'][1].update(wall_s=float('nan')),
            lambda r:r.update(fixture_hash='forged'),
            lambda r:r['results'].update(extra=copy.deepcopy(r['results']['a'])),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                r=self.result();mutation(r)
                with self.assertRaises(bench.BenchError):bench.calibration(r,copy.deepcopy(r))

    def test_historical_policy_cannot_be_reinterpreted(self):
        old=self.result();old['protocol']['calibration_policy']='compile-only-v2'
        with self.assertRaisesRegex(bench.BenchError,'Historical'):bench.calibration(old,old)

    def test_aarch64_input_flags_and_output_machine_are_checked(self):
        root = self.temporary()
        source = root / 'demo.ii'
        source.write_text('int f() { return 0; }\n')
        bench.save(root/'demo.flags.json', dict(target=bench.AARCH64_TARGET,
            sha256=bench.digest(source),flags=['-O2'],source='fixture',
            original_command=['clang++'],preprocess_command=['clang++','-E']))
        with self.assertRaises(bench.BenchError): bench.real_inputs(root)
        self.assertEqual(len(bench.real_inputs(root,bench.AARCH64_TARGET)),1)
        args = SimpleNamespace(sysroot=Path('/arm'))
        flags = bench.compiler_flags(args,Path('/resource'),bench.AARCH64_TARGET,Path('/aarch64'))
        self.assertEqual(flags[:2],['--target=aarch64-tizen-linux-gnu','--sysroot=/aarch64'])
        obj=root/'test.o'
        import struct
        obj.write_bytes(b'\x7fELF\x02\x01'+b'\0'*10+struct.pack('<HH',1,183))
        bench.verify_object(obj,bench.AARCH64_TARGET)
        with self.assertRaises(bench.BenchError): bench.verify_object(obj)

    def test_target_split_selects_13_or_10_without_mutating_fixture_inputs(self):
        arm = [dict(name=str(i), target=bench.TARGET) for i in range(13)]
        a64 = [dict(name=str(i), target=bench.AARCH64_TARGET) for i in range(10)]
        cases = arm + a64
        original = copy.deepcopy(cases)
        self.assertEqual(bench.select_compile_cases(cases, 'armv7l'), arm)
        self.assertEqual(bench.select_compile_cases(cases, 'aarch64'), a64)
        self.assertEqual(bench.select_compile_cases(cases, 'all'), original)
        self.assertEqual(cases, original)
        with self.assertRaises(bench.BenchError):
            bench.select_compile_cases(arm, 'aarch64')

    def test_memory_preflight(self):
        with patch.object(bench, "available_memory", return_value=bench.MEMORY_LIMIT - 1):
            with self.assertRaisesRegex(bench.BenchError, "LOW_MEMORY"):
                bench.memory_guard()

    def test_affinity_limit(self):
        allowed = {2, 3, 6, 7}
        self.assertEqual(bench.parse_cpus(None, allowed), [2, 3])
        self.assertEqual(bench.parse_cpus("6-7", allowed), [6, 7])
        for value in ("2,3,6", "99", "7-6", "invalid"):
            with self.assertRaises(bench.BenchError):
                bench.parse_cpus(value, allowed)

    def test_real_tu_empty_target_hash_and_unsafe_flags(self):
        root = self.temporary()
        self.assertEqual(bench.real_inputs(root), [])
        source = root / "demo.ii"
        source.write_text("int f() { return 0; }\n")
        sidecar = root / "demo.flags.json"
        data = dict(target=bench.TARGET, sha256=bench.digest(source), flags=["-O2"],
                    source="fixture", original_command=["clang++"], preprocess_command=["clang++", "-E"])
        bench.save(sidecar, data)
        self.assertEqual(len(bench.real_inputs(root)), 1)
        for key, value in (("target", "x86_64-linux-gnu"), ("sha256", "wrong"),
                           ("flags", ["-Xclang", "-load", "plugin.so"]),
                           ("flags", ["--sysroot=/other"]), ("flags", ["-flto=thin"])):
            changed = dict(data, **{key: value})
            bench.save(sidecar, changed)
            with self.assertRaises(bench.BenchError):
                bench.real_inputs(root)

    def test_historical_generator_hashes(self):
        path = bench.INPUTS / "generate_synthetic.py"
        spec = importlib.util.spec_from_file_location("generator_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        output = self.temporary()
        actual = module.generate(output, 1)
        expected = json.loads((bench.INPUTS / "provenance.json").read_text())["historical_manifest"]["sources"]
        self.assertEqual(actual, expected)

    def test_actual_address_space_limit(self):
        root = self.temporary()
        args = SimpleNamespace(cpu_set=[min(bench.os.sched_getaffinity(0))], timeout=10, load_threshold=1e9)
        runner = bench.Runner(args, root, root)
        # prlimit must prevent allocation before the host can allocate 5 GiB.
        with self.assertRaises(bench.BenchError):
            runner.command([sys.executable, "-c", "bytearray(5 * 1024**3)"], tag="memory-negative")
        self.assertIn("MemoryError", Path(runner.commands[-1]["stderr"]).read_text())

    def test_holdout_seed_changes_all_classes_without_changing_scale(self):
        import re
        spec = importlib.util.spec_from_file_location("seed_test", bench.INPUTS / "generate_synthetic.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        root = self.temporary()
        for scale in (1, 2):
            old, new, repeat = [root / f"{scale}-{x}" for x in ("old", "new", "repeat")]
            training = module.generate(old, scale)
            holdout = module.generate(new, scale, 20260920)
            self.assertEqual(holdout, module.generate(repeat, scale, 20260920))
            self.assertTrue(all(training[c]['sha256'] != holdout[c]['sha256'] for c in 'ABC'))
            counts = lambda p: json.loads((p / 'generator.json').read_text())['counts']
            self.assertEqual(counts(old), counts(new))
            ids = lambda p: set(re.findall(r'sizeof\(Front<(\d+)>', (p/'A.cpp').read_text()))
            self.assertFalse(ids(old) & ids(new))
            self.assertEqual(len(ids(old)), len(ids(new)))

    def test_actual_timeout_is_failure(self):
        root = self.temporary()
        args = SimpleNamespace(cpu_set=[min(bench.os.sched_getaffinity(0))], timeout=.05, load_threshold=1e9)
        runner = bench.Runner(args, root, root)
        with self.assertRaises(bench.BenchError):
            runner.command([sys.executable, "-c", "import time; time.sleep(5)"], tag="timeout-negative")
        self.assertTrue(runner.commands[-1]["timed_out"])
        self.assertLess(runner.commands[-1]["wall_s"], 1)

    def test_actual_affinity_limit_and_aslr_personality(self):
        root = self.temporary()
        cpu = min(bench.os.sched_getaffinity(0))
        args = SimpleNamespace(cpu_set=[cpu], timeout=10, load_threshold=1e9, aslr="off")
        runner = bench.Runner(args, root, root)
        record = runner.command([sys.executable, "-c",
            "import json,os,resource; print(json.dumps([sorted(os.sched_getaffinity(0)),"
            "resource.getrlimit(resource.RLIMIT_AS),int(open('/proc/self/personality').read(),16)]))"],
            tag="resource-positive")
        affinity, limits, personality = json.loads(Path(record["stdout"]).read_text())
        self.assertEqual(affinity, [cpu])
        self.assertEqual(limits, [bench.MEMORY_LIMIT, bench.MEMORY_LIMIT])
        self.assertTrue(personality & 0x40000)


if __name__ == "__main__":
    unittest.main()
