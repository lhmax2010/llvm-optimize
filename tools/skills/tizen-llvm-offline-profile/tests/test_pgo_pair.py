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
        argv = plan["instrumented-build"][0]["argv"]
        self.assertEqual(argv[argv.index("--threads") + 1], "2")

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
