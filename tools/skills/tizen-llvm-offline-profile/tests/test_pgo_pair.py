import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
import manifest
import pgo_pair
from generate_synthetic import generate as synthetic


class PlanTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.output = self.root / "no-output"
        self.example = SKILL / "config.example.json"

    def plan(self, *args):
        result = subprocess.run([sys.executable, "-B", str(SKILL / "scripts/pgo_pair.py"),
                                 "--config", str(self.example), "--output", str(self.output),
                                 "--dry-run", *args], check=True, capture_output=True, text=True)
        self.assertFalse(self.output.exists())
        return json.loads(result.stdout)

    def test_full_dry_run_emits_commands_without_creating_outputs(self):
        data = self.plan()
        self.assertFalse(data["executes_builds"])
        self.assertEqual([s["stage"] for s in data["stages"]], list(pgo_pair.STAGES))
        self.assertEqual(len(data["training"]), 23)
        self.assertTrue(all(s["selected"] and s["commands"] for s in data["stages"]))
        self.assertEqual(len(data["stages"][1]["commands"]), 23)
        self.assertIn("-stale-threshold=5", data["stages"][6]["commands"][0]["argv"])
        self.assertEqual(data["historical_budget"]["peak_cgroup_bytes"], 21703991296)

    def test_dry_run_does_not_start_processes_or_read_host_resources(self):
        cfg = json.loads(self.example.read_text())
        rows = json.loads((SKILL / "references/training-set.json").read_text())
        with patch.object(pgo_pair.subprocess, "Popen") as command, patch.object(pgo_pair, "free_memory") as memory:
            plan = pgo_pair.Pipeline(cfg, self.output, rows).dry_run(["bolt-match"])
        command.assert_not_called()
        memory.assert_not_called()
        self.assertEqual([s["stage"] for s in plan["stages"] if s["selected"]], ["bolt-match"])

    def test_private_loader_environment_is_scoped_to_its_tool(self):
        cfg = json.loads(self.example.read_text())
        rows = json.loads((SKILL / "references/training-set.json").read_text())
        env = {"LD_LIBRARY_PATH": "/path/to/target-libs"}
        cfg["tool_environment"] = {
            "instrumented_clang": env, "readelf": env,
            "bolt-instrumented-clang": env,
        }
        pipeline = pgo_pair.Pipeline(cfg, self.output, rows)
        self.assertEqual(pipeline.tool_environment(pipeline.train("ir")[0]["argv"]), env)
        self.assertEqual(pipeline.tool_environment(pipeline.train("bolt")[0]["argv"]), env)
        self.assertEqual(pipeline.tool_environment(pipeline.plan()["pgo-build"][-1]["argv"]), env)
        self.assertEqual(pipeline.tool_environment(pipeline.tool("git", "status")), {})
        self.assertEqual(pipeline.tool_environment(pipeline.custom("pgo-build")[0]["argv"]), {})
        self.assertEqual(pipeline.tool_environment(pipeline.rewrite()["argv"]), {})

    def test_stage_selection_is_canonical_and_checked(self):
        self.assertEqual(pgo_pair.active_stages("bolt-match,ir-train"), ["ir-train", "bolt-match"])
        for value in ("unknown", "ir-train,ir-train"):
            with self.assertRaises(ValueError):
                pgo_pair.active_stages(value)

    def test_reduced_tier_changes_real_argv(self):
        cfg = json.loads(self.example.read_text())
        cfg["resources"]["tier"] = "reduced"
        rows = json.loads((SKILL / "references/training-set.json").read_text())
        plan = pgo_pair.Pipeline(cfg, self.output, rows).plan()
        argv = next(action["argv"] for action in plan["instrumented-build"]
                    if Path(action["argv"][0]).name == "gbs")
        self.assertEqual(argv[argv.index("--threads") + 1], "2")
        self.assertIn("mlgo_build_jobs 2", argv)
        self.assertIn("_buildshell /var/tmp/llvm-stage-jobs/build-shell", argv)

    def test_checked_normally_and_runtime_flags_rejected(self):
        main = {"command": "clang -c a.c -fprofile-instr-use=/profile", "output": "lib/code.o", "file": "a.c"}
        runtime = {"command": "clang -c b.c", "output": "projects/openmp/code.o", "file": "b.c"}
        self.assertEqual(pgo_pair.check_compile_db([main, runtime], "/profile"), {"main": 1, "runtime": 1})
        with self.assertRaisesRegex(RuntimeError, "runtime edge"):
            pgo_pair.check_compile_db([{**runtime, "command": runtime["command"] + " -fprofile-instr-use=/profile"}], "/profile")

    def test_historical_synthetic_input_identities(self):
        rows = {r["name"]: r for r in json.loads((SKILL / "references/training-set.json").read_text())}
        for name in ("A", "B", "C"):
            dest = self.root / name
            recipe = rows[name]["recipe"]
            synthetic(dest, recipe["scale"], recipe["seed"])
            self.assertEqual(manifest.file_identity(dest / (name + ".cpp")),
                             {key: rows[name][key] for key in ("bytes", "sha256")})

    def recovery_fixture(self):
        cfg = json.loads(self.example.read_text())
        rows = json.loads((SKILL / "references/training-set.json").read_text())
        source = self.root / "source"
        recipe = source / "packaging/llvm.spec"
        recipe.parent.mkdir(parents=True)
        recipe.write_bytes(b"recipe")
        conf = self.root / "gbs.conf"
        conf.write_bytes(b"configuration")
        cfg["paths"].update(llvm=str(source), gbs_config=str(conf))
        cfg["resources"]["lock_path"] = str(self.root / "lock")
        tools = {}
        for name in ("instrumented_clang", "llvm_profdata"):
            path = self.root / name
            path.write_bytes(name.encode())
            cfg["tools"][name] = str(path)
            tools[name] = {"path": str(path), "version": "22.1.8", **manifest.file_identity(path)}
        log = self.root / "build-0.txt"
        log.write_text("PGO_INSTRUMENTED_BUILD_PASS\n")
        identity = {"commit": cfg["source_commit"], "tree": "1" * 40,
                    "snapshot": cfg["snapshot"], "recipe": manifest.file_identity(recipe),
                    "gbs_config": manifest.file_identity(conf)}
        receipt = self.root / "recovery.json"
        receipt.write_text(json.dumps({"stage": "instrumented-build", "source_identity": identity,
                                       "tools": tools, "build_log": {"path": str(log), **manifest.file_identity(log)}}))
        return pgo_pair.Pipeline(cfg, self.output, rows), receipt, identity, tools

    def test_recovery_dry_run_verifies_and_does_not_write(self):
        pipeline, receipt, _, tools = self.recovery_fixture()
        result = pipeline.dry_run(["ir-train"], resume=True, recovery=receipt, available=24 * 2**30)
        self.assertEqual(result["recovery"]["status"], "VERIFIED_FOR_REUSE")
        self.assertEqual(result["recovery"]["next_stage"], "ir-train")
        self.assertFalse(self.output.exists())
        Path(tools["instrumented_clang"]["path"]).write_text("changed")
        with self.assertRaisesRegex(RuntimeError, "retained tool content mismatch"):
            pipeline.dry_run(["ir-train"], resume=True, recovery=receipt)

    def test_execute_recovers_g1_and_calls_only_g2(self):
        pipeline, receipt, identity, _ = self.recovery_fixture()
        artifact = self.root / "trained.profraw"
        artifact.write_bytes(b"profile")
        with patch.object(pipeline, "admit", return_value=True), \
             patch.object(pipeline, "verify_inputs"), \
             patch.object(pipeline, "source_identity", return_value=identity), \
             patch.object(pipeline, "watchdog"), \
             patch.object(pipeline, "stage", return_value=[artifact]) as stage:
            pipeline.execute(["ir-train"], True, receipt)
        self.assertEqual([call.args[0] for call in stage.call_args_list], ["ir-train"])
        self.assertTrue(pipeline.checkpoint("instrumented-build"))
        self.assertTrue(pipeline.checkpoint("ir-train"))

    def test_stage_admission_is_one_shot_with_matching_cgroup(self):
        cfg = json.loads(self.example.read_text())
        rows = json.loads((SKILL / "references/training-set.json").read_text())
        pipeline = pgo_pair.Pipeline(cfg, self.output, rows)
        stage = "pgo-build"
        memory = 22 * 2**30
        disk = {"/path/to/disk": 150 * 2**30}
        with patch.object(pipeline, "measure", return_value={"memory": memory, "disk": disk}) as measure, \
             patch.object(pipeline, "cgroup_memory_max", return_value=18 * 2**30), \
             patch.object(pgo_pair.time, "sleep") as sleep:
            self.assertTrue(pipeline.admit([stage]))
            self.assertEqual(pipeline.tier["jobs"], 4)
            self.assertEqual(measure.call_count, 1)
            sleep.assert_not_called()
        with patch.object(pipeline, "measure", return_value={"memory": memory, "disk": disk}), \
             patch.object(pipeline, "cgroup_memory_max", return_value=19 * 2**30):
            with self.assertRaisesRegex(RuntimeError, "outside its admitted"):
                pipeline.admit([stage])
        with patch.object(pipeline, "measure", return_value={"memory": 13 * 2**30, "disk": disk}), \
             patch.object(pipeline, "cgroup_memory_max") as cap:
            self.assertFalse(pipeline.admit([stage]))
            self.assertEqual(pipeline.status["status"], "SKIPPED")
            cap.assert_not_called()

    def test_dynamic_watchdog_legacy_config_and_boundary(self):
        cfg = json.loads(self.example.read_text())
        cfg["resources"]["stop_memory_bytes"] = 6 * 2**30
        rows = json.loads((SKILL / "references/training-set.json").read_text())
        pipeline = pgo_pair.Pipeline(cfg, self.output, rows)
        pipeline.end = float("inf")
        disk = {"/path/to/disk": 15*2**30}
        with patch.object(pipeline, "measure", return_value={"memory": 3*2**30, "disk": disk}):
            pipeline.watchdog()
        with patch.object(pipeline, "measure", return_value={"memory": 3*2**30-1, "disk": disk}):
            with self.assertRaisesRegex(RuntimeError, "crossed the memory or disk"):
                pipeline.watchdog()

    def test_launch_configuration_applies_to_training_and_version(self):
        cfg = json.loads(self.example.read_text())
        rows = json.loads((SKILL / "references/training-set.json").read_text())
        cfg["tool_launchers"] = {"instrumented_clang": {"loader": "/path/to/loader",
                                                       "library_path": ["/path/to/tizen/lib"]}}
        cfg["training_extra_args"] = {"ir": ["-fintegrated-cc1"]}
        pipeline = pgo_pair.Pipeline(cfg, self.output, rows)
        prefix = ["/path/to/loader", "--library-path", "/path/to/tizen/lib", str(pipeline.tools["instrumented_clang"])]
        self.assertEqual(pipeline.train("ir")[0]["argv"][:4], prefix)
        self.assertEqual(pipeline.train("ir")[0]["argv"][-1], "-fintegrated-cc1")
        self.assertEqual(pipeline.action(pipeline.tool("instrumented_clang", "--version"))["argv"], [*prefix, "--version"])
        self.assertEqual(pipeline.action(pipeline.tool("git", "status"))["argv"], pipeline.tool("git", "status"))

    def test_checkpoint_rejects_changed_artifacts(self):
        cfg = json.loads(self.example.read_text())
        rows = json.loads((SKILL / "references/training-set.json").read_text())
        pipeline = pgo_pair.Pipeline(cfg, self.output, rows)
        self.output.mkdir()
        artifact = self.output / "artifact"
        artifact.write_bytes(b"expected")
        name = "merge-profdata"
        pgo_pair.save(self.output / (name + ".done.json"),
                      {"stage": name, "identity": pipeline.state_digest,
                       "artifacts": [{"path": str(artifact), **manifest.file_identity(artifact)}]})
        self.assertTrue(pipeline.checkpoint(name))
        artifact.write_bytes(b"tampered")
        with self.assertRaisesRegex(RuntimeError, "artifact changed"):
            pipeline.checkpoint(name)
