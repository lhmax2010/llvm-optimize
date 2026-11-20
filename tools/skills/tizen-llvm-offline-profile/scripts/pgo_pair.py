#!/usr/bin/env python3
"""Generate a local paired profile, or print an eight-stage plan without executing it."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import signal
import subprocess
import sys
import time

from bolt_stale_gate import GateError, audit_log
from build_cleanup import remove_tree
from stage_resources import WATCHDOG_DISK, WATCHDOG_MEMORY, admission as stage_admission, parallelism
from manifest import file_identity, generate

STAGES = (
    "instrumented-build", "ir-train", "merge-profdata", "pgo-build",
    "bolt-tools-relink", "bolt-instrument-train-merge", "bolt-match", "write-manifest",
)
# Historical elapsed seconds and peak cgroup bytes for observed substeps.
MEASUREMENTS = {
    "instrumented-build": [(4068.547, 7227248640)],
    "ir-train": [(201.930, 1481818112)],
    "merge-profdata": [(3.278, 1824751616)],
    "pgo-build": [(6176, 21703991296)],
    "bolt-tools-relink": [(418, None), (None, None)],
    "bolt-instrument-train-merge": [(77.954, 17074352128), (379.427, 3890348032), (3.396, 1585553408)],
    "bolt-match": [(44.984, 8712601600)],
    "write-manifest": [(None, None)],
}
BOLT_OPTIONS = [
    "-reorder-blocks=ext-tsp", "-reorder-functions=cdsort", "-split-functions",
    "-split-all-cold", "-split-eh", "-dyno-stats", "--thread-count=1",
    "-stale-threshold=5", "-use-old-text",
]


def timestamp():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def absolute(value):
    path = Path(value)
    if not path.is_absolute():
        raise ValueError(f"expected an absolute path: {value}")
    return path


def save(path, data, replace=False):
    dest = path.with_name(path.name + ".tmp") if replace else path
    with dest.open("x", encoding="utf-8") as stream:
        json.dump(data, stream, indent=2)
        stream.write("\n")
    if replace:
        dest.replace(path)


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def targets(rows, variables):
    if len(rows) != 23 or len({r["name"] for r in rows}) != 23:
        raise ValueError("training list must contain 23 uniquely named entries")
    result = []
    for row in rows:
        source = absolute(row["file"].format_map(variables))
        flags = [arg.format_map(variables) for arg in row["compiler_args"]]
        if (not re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) or
                type(row["bytes"]) is not int or row["bytes"] <= 0 or
                "--target=" + row["target"] not in flags):
            raise ValueError(f"invalid training row: {row['name']}")
        result.append({**row, "file": str(source), "compiler_args": flags})
    return result


def active_stages(value):
    names = value.split(",") if value else list(STAGES)
    if len(set(names)) != len(names) or set(names) - set(STAGES):
        raise ValueError("--stages must name distinct stages from the plan")
    return [name for name in STAGES if name in names]


def free_memory():
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) * 1024
    raise RuntimeError("MemAvailable unavailable")


@contextmanager
def owned_lock(path):
    with path.open("a") as stream:
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise RuntimeError(f"cooperative build lock is busy: {path}") from error
        yield


def runtime_target(output):
    path = Path(output)
    return (bool({"compiler-rt", "openmp", "runtimes", "offload"} & set(path.parts))
            or path.name.startswith(("libclang_rt.", "libomp.", "libompd.", "libarcher.", "libomptarget.")))


def check_compile_db(rows, profile, runtime_only=False):
    counts = {"main": 0, "runtime": 0}
    for row in rows:
        argv = shlex.split(row["command"])
        flags = [arg for arg in argv if re.match(r"-f(?:no-)?(?:cs-)?(?:profile|auto-profile)", arg)]
        runtime = runtime_only or runtime_target(row["output"])
        compiles = "-c" in argv and Path(row["file"]).suffix in (".c", ".cc", ".cpp", ".cxx", ".m", ".mm", ".C")
        if compiles:
            counts["runtime" if runtime else "main"] += 1
        if runtime:
            if flags:
                raise RuntimeError(f"profile options found in a runtime edge: {row['output']}")
        elif compiles or flags:
            if flags != ["-fprofile-instr-use=" + profile]:
                raise RuntimeError(f"unexpected profile options in a main edge: {row['output']}")
    return counts


class Pipeline:
    def __init__(self, cfg, output, rows):
        self.cfg, self.root = cfg, absolute(output)
        self.paths = {key: str(absolute(value)) for key, value in cfg["paths"].items()}
        self.paths["output"] = str(self.root)
        self.paths["profdata"] = str(self.root / "clang.profdata")
        self.rows = targets(rows, self.paths)
        self.resources = cfg["resources"]
        limits = self.resources["tiers"][self.resources["tier"]]
        self.set_parallelism({"jobs": limits["jobs"], "thinlto_jobs": limits["jobs"], "link_jobs": 1})
        self.dynamic_admission = self.resources.get("stage_admission", False)
        self.stop_memory = WATCHDOG_MEMORY if self.dynamic_admission else self.resources["stop_memory_bytes"]
        self.stop_disk = WATCHDOG_DISK if self.dynamic_admission else self.resources["stop_disk_bytes"]
        # Accept archived configurations with the previous memory threshold so
        # their immutable stage checkpoint fingerprints still validate.
        if self.dynamic_admission and (self.resources["stop_memory_bytes"] not in (WATCHDOG_MEMORY, 6 * 2**30)
                                       or self.resources["stop_disk_bytes"] != WATCHDOG_DISK):
            raise ValueError("stage admission requires the 3 GiB memory and 15 GiB disk stop lines")
        if (type(limits["jobs"]) is not int or limits["jobs"] <= 0 or
                not 0 < self.resources["watchdog_seconds"] <= 30 or
                self.resources["max_seconds"] <= 0 or
                not 0 <= self.resources["defer_seconds"] <= 1800 or
                limits["admission_memory_bytes"] <= self.resources["stop_memory_bytes"] or
                limits["admission_disk_bytes"] <= self.resources["stop_disk_bytes"]):
            raise ValueError("invalid resource limits")
        self.profile = self.expand(cfg["profile_path_in_build"])
        absolute(self.profile)
        self.ninja_roots = [absolute(self.expand(path)) for path in cfg["ninja_roots"]]
        if not self.ninja_roots:
            raise ValueError("at least the main Ninja root is required")
        if cfg["project"] not in ("T", "D") or not re.fullmatch(r"\d+\.\d+\.\d+", cfg["llvm_version"]):
            raise ValueError("invalid project or LLVM version")
        if not re.fullmatch(r"[0-9a-f]{40}", cfg["source_commit"]):
            raise ValueError("source_commit must be a full lowercase commit ID")
        self.command_config = cfg["commands"]
        self.tools = {name: absolute(self.expand(path)) for name, path in cfg["tools"].items()}
        self.launchers = {}
        for name, launch in cfg.get("tool_launchers", {}).items():
            if name not in self.tools and name != "bolt-instrumented-clang":
                raise ValueError(f"unknown launcher tool: {name}")
            loader = absolute(self.expand(launch["loader"]))
            libraries = [str(absolute(self.expand(path))) for path in launch["library_path"]]
            if not libraries:
                raise ValueError(f"empty loader library path: {name}")
            self.launchers[name] = [str(loader), "--library-path", ":".join(libraries)]
        self.bolt_input = absolute(self.expand(cfg["bolt_input"]))
        self.bolt_runtime = absolute(self.expand(cfg["bolt_runtime"]))
        self.executable = self.root / "clang-bolt-instrumented"
        self.profdata = Path(self.paths["profdata"])
        self.fdata = self.root / "clang.fdata"
        self.status = {"status": "STOP", "project": cfg["project"], "stages": []}
        self.state_digest = hashlib.sha256(json.dumps([cfg, str(self.root), rows], sort_keys=True).encode()).hexdigest()
        self.tier = None
        self.end = None

    def set_parallelism(self, counts):
        for name, value in counts.items():
            self.paths[name] = "" if value is None else str(value)

    def expand(self, value):
        return value.format_map(self.paths)

    def tool(self, name, *args):
        return [str(self.tools[name]), *map(str, args)]

    def custom(self, name):
        specs = self.command_config[name]
        if not specs:
            raise ValueError(f"missing commands for {name}")
        result = []
        for step in specs:
            argv = [self.expand(arg) for arg in step["argv"]]
            if not argv:
                raise ValueError(f"empty command for {name}")
            capture = absolute(self.expand(step["stdout"])) if step.get("stdout") else None
            result.append(self.action(argv, absolute(self.expand(step["cwd"])), stdout=capture))
        return result

    def action(self, argv, cwd=None, extra_env=None, stdout=None):
        absolute(argv[0])
        name = self.tool_name(argv)
        launcher = self.launchers.get(name, [])
        return {"argv": launcher + argv, "cwd": str(self.root if cwd is None else cwd),
                "extra_env": extra_env or {}, "stdout": str(stdout) if stdout else None}

    def train(self, mode):
        if mode == "ir":
            program = self.tools["instrumented_clang"]
        else:
            program = self.executable
        actions = []
        for index, row in enumerate(self.rows):
            tree = self.root / mode / f"{index:02d}"
            env = {"LLVM_PROFILE_FILE": str(tree / "%m-%p.profraw")} if mode == "ir" else {}
            extra = self.cfg.get("training_extra_args", {}).get(mode, [])
            argv = [str(program), *row["compiler_args"], "-c", row["file"], "-o", str(tree / "input.o"), *extra]
            actions.append(self.action(argv, tree, env))
        return actions

    def instrument(self):
        return self.action(self.tool(
            "llvm_bolt", self.bolt_input, "-instrument", "--thread-count=1",
            "-runtime-instrumentation-lib=" + str(self.bolt_runtime),
            "-instrumentation-file=" + str(self.root / "bolt" / "clang"),
            "-instrumentation-file-append-pid", "-instrumentation-binpath=" + str(self.executable),
            "-o", self.executable))

    def rewrite(self):
        return self.action(self.tool("llvm_bolt", self.bolt_input, "-data=" + str(self.fdata),
                                     *BOLT_OPTIONS, "-o", self.root / "clang-bolt-qualified"))

    def plan(self):
        raw_paths = [str(self.root / "ir" / f"{i:02d}" / "*.profraw") for i in range(23)]
        mapping = {
            "instrumented-build": self.custom("instrumented-build"),
            "ir-train": self.train("ir"),
            "merge-profdata": [self.action(self.tool("llvm_profdata", "merge", "-o", self.profdata, *raw_paths))],
            "pgo-build": self.custom("pgo-build") +
            [self.action(self.tool("ninja", "-t", "compdb"), cwd=root) for root in self.ninja_roots] +
            [self.action([sys.executable, str(Path(__file__).with_name("runtime_dep_check.py")),
                          "--root", self.paths["package_root"], "--readelf", str(self.tools["readelf"])])],
            "bolt-tools-relink": self.custom("bolt-tools") + self.custom("relink-strip-debug") +
            [self.action(self.tool("readelf", "--wide", "--section-headers", self.bolt_input))],
            "bolt-instrument-train-merge": [self.instrument(), *self.train("bolt"),
                                           self.action(self.tool("merge_fdata", self.root / "bolt" / "clang*.fdata"),
                                                       stdout=self.fdata)],
            "bolt-match": [self.rewrite()],
            "write-manifest": [self.action([sys.executable, str(Path(__file__).with_name("manifest.py")), "generate",
                                          "--output", str(self.root), "--project", self.cfg["project"],
                                          "--llvm-version", self.cfg["llvm_version"], "--profdata", str(self.profdata),
                                          "--fdata", str(self.fdata), "--provenance", str(self.root / "provenance.json")])],
        }
        return mapping

    def dry_run(self, selected, resume=False, recovery=None, available=None):
        recovery_plan = None
        if recovery:
            receipt = self.recovery_receipt(recovery)
            recovery_plan = {"stage": "instrumented-build", "status": "VERIFIED_FOR_REUSE",
                             "artifacts": receipt["tools"], "next_stage": "ir-train"}
        mapping = {}
        for name in selected:
            if available is not None and self.dynamic_admission:
                limit = stage_admission(name, available)
                self.set_parallelism({key: limit[key] for key in ("jobs", "thinlto_jobs", "link_jobs")})
            mapping[name] = self.plan()[name]
        defaults = self.cfg["resources"]["tiers"][self.resources["tier"]]["jobs"]
        self.set_parallelism({"jobs": defaults, "thinlto_jobs": defaults, "link_jobs": 1})
        for name, commands in self.plan().items():
            mapping.setdefault(name, commands)
        return {"mode": "dry-run", "resume": resume, "recovery": recovery_plan,
                "stage_admission": ([stage_admission(name, available) for name in selected]
                                    if available is not None else []), "executes_builds": False, "project": self.cfg["project"],
                "stages": [{"stage": name, "selected": name in selected, "commands": mapping[name],
                            "historical_substeps": [{"seconds": seconds, "peak_cgroup_bytes": memory}
                                                    for seconds, memory in MEASUREMENTS[name]]}
                           for name in STAGES],
                "training": self.rows, "resources": self.resources,
                "historical_budget": {"peak_cgroup_bytes": 21703991296,
                                      "observed_root_boundary_bytes": 91275411456,
                                      "planning_lower_bound_gib_including_reserve": 125.626},
                "notes": ["Pattern operands describe inventoried files and are never passed to a shell.",
                          "Stage checkpoints are validated by content identity before reuse.",
                          "PGO match remains UNKNOWN. Final package qualification is separate."]}

    def admit(self, selected=(), available=None):
        start = time.monotonic()
        if self.dynamic_admission:
            if len(selected) != 1:
                raise ValueError("select one stage per resource-limited invocation")
            self.end = start + self.resources["max_seconds"]
            measurement = self.measure()
            available = measurement["memory"] if available is None else available
            limit = stage_admission(selected[0], available)
            self.status["admission"] = [{**measurement, "admission_memory": available, **limit}]
            if not limit["admitted"] or min(measurement["disk"].values()) < self.resources["tiers"][self.resources["tier"]]["admission_disk_bytes"]:
                self.status["status"] = "SKIPPED"
                self.status["reason"] = "stage memory or disk below admission floor"
                return False
            cap = self.cgroup_memory_max()
            if not limit["floor"] <= cap <= limit["memory_max"]:
                raise RuntimeError("stage cgroup MemoryMax is outside its admitted memory budget")
            self.tier = parallelism(selected[0], cap)
            self.set_parallelism(self.tier)
            self.status["admission"][-1].update(self.tier, actual_memory_max=cap)
            return True

        self.end = start + self.resources["max_seconds"]
        retry = self.resources["defer_seconds"]
        if not 0 <= retry <= 1800:
            raise ValueError("defer_seconds must be between 0 and 1800")
        for attempt in range(2):
            measurement = self.measure()
            self.status.setdefault("admission", []).append(measurement)
            for name, tier in self.resources["tiers"].items():
                if (name == self.resources["tier"] and
                        measurement["memory"] >= tier["admission_memory_bytes"] and
                        min(measurement["disk"].values()) >= tier["admission_disk_bytes"]):
                    self.tier = tier
                    self.status["tier"] = name
                    return True
            if attempt or not retry or time.monotonic() + retry >= self.end:
                break
            time.sleep(retry)
        raise RuntimeError("resource admission failed for the selected tier; see summary")

    def cgroup_memory_max(self):
        relative = next(line[3:] for line in Path("/proc/self/cgroup").read_text().splitlines()
                        if line.startswith("0::"))
        root = Path("/sys/fs/cgroup")
        group = root / relative.lstrip("/")
        limits = []
        for path in (group, *group.parents):
            if not path.is_relative_to(root):
                break
            try:
                value = (path / "memory.max").read_text().strip()
            except FileNotFoundError:
                continue
            if value != "max":
                limits.append(int(value))
        if not limits:
            raise RuntimeError("stage requires a finite cgroup MemoryMax")
        return min(limits)

    def measure(self):
        mounts = {str(self.root), *self.resources["disk_paths"]}
        return {"at": timestamp(), "memory": free_memory(),
                "disk": {path: shutil.disk_usage(absolute(path)).free for path in sorted(mounts)}}

    def watchdog(self):
        if time.monotonic() >= self.end:
            raise RuntimeError("job deadline reached")
        data = self.measure()
        if data["memory"] < self.stop_memory or min(data["disk"].values()) < self.stop_disk:
            self.status["watchdog"] = data
            raise RuntimeError("job crossed the memory or disk stop line")

    def tool_name(self, argv):
        tools = {**self.tools, "bolt-instrumented-clang": self.executable}
        for name, path in tools.items():
            prefix = self.launchers.get(name, [])
            if argv[0] == str(path) or (prefix and argv[:len(prefix)+1] == [*prefix, str(path)]):
                return name
        return None

    def tool_environment(self, argv):
        by_tool = self.cfg.get("tool_environment", {})
        name = self.tool_name(argv)
        if name in self.launchers:
            return {key: val for key, val in by_tool.get(name, {}).items() if key != "LD_LIBRARY_PATH"}
        if name:
            return by_tool.get(name, {})
        if (len(argv) > 1 and any(Path(arg).name == "runtime_dep_check.py" for arg in argv[:3])
                and str(self.tools["readelf"]) in argv):
            return by_tool.get("readelf", {})
        return {}

    def run(self, attempt, label, action):
        self.watchdog()
        argv = action["argv"]
        log = attempt / (label + ".txt")
        env = {**os.environ, **self.cfg.get("environment", {}), **self.tool_environment(argv), "LC_ALL": "C",
               **action["extra_env"]}
        for key in ("jobs", "thinlto_jobs", "link_jobs"):
            env["PROFILE_" + key.upper()] = self.paths[key]
        if self.tool_name(argv) in self.launchers:
            env.pop("LD_LIBRARY_PATH", None)
        with log.open("xb") as stream:
            output_path = Path(action["stdout"]) if action["stdout"] else None
            output = output_path.open("xb") if output_path else stream
            started = time.monotonic()
            try:
                with subprocess.Popen(argv, cwd=action["cwd"], env=env, stdout=output,
                                      stderr=stream if output_path else subprocess.STDOUT,
                                      start_new_session=True) as process:
                    try:
                        while True:
                            try:
                                code = process.wait(timeout=min(self.resources["watchdog_seconds"],
                                                                max(0.01, self.end - time.monotonic())))
                                break
                            except subprocess.TimeoutExpired:
                                self.watchdog()
                    except BaseException:
                        try:
                            os.killpg(process.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                        process.wait()
                        raise
            finally:
                if output is not stream:
                    output.close()
            receipt = {"argv": argv, "cwd": action["cwd"], "exit_code": code,
                       "seconds": round(time.monotonic() - started, 3), "log": str(log)}
            if action.get("trusted_tool") is True:
                receipt.update(trusted_tool=True, log_identity=file_identity(log))
            save(attempt / (label + ".json"), receipt)
        if code:
            raise RuntimeError(f"command failed ({code}); see {log}")
        return log

    def verify_inputs(self):
        for row in self.rows:
            inventories = file_identity(row["file"])
            if inventories != {key: row[key] for key in ("bytes", "sha256")}:
                raise RuntimeError(f"training input identity mismatch: {row['name']}")
            for arg in row["compiler_args"]:
                if arg.startswith(("--sysroot=", "-resource-dir=")) and not Path(arg.split("=", 1)[1]).is_dir():
                    raise RuntimeError(f"missing training directory: {arg}")

    def source_identity(self, attempt):
        src = self.paths["llvm"]
        def query(label, *argv):
            return self.run(attempt, label, self.action(self.tool("git", "-C", src, *argv))).read_text().strip()
        commit = query("source-commit", "rev-parse", "HEAD")
        if commit != self.cfg["source_commit"] or query("source-status", "status", "--porcelain", "--untracked-files=no"):
            raise RuntimeError("source revision or tracked worktree differs from the configured input")
        tree = query("source-tree", "rev-parse", "HEAD^{tree}")
        return {"commit": commit, "tree": tree, "snapshot": self.cfg["snapshot"],
                "recipe": file_identity(Path(src) / "packaging" / "llvm.spec"),
                "gbs_config": file_identity(self.paths["gbs_config"])}

    def train_profiles(self, mode, attempt):
        raw = []
        for index, action in enumerate(self.train(mode)):
            work = Path(action["cwd"])
            work.mkdir(parents=True, exist_ok=False)
            profile_dir = work if mode == "ir" else self.root / "bolt"
            pattern = "*.profraw" if mode == "ir" else "clang*.fdata"
            before = set(profile_dir.glob(pattern))
            self.run(attempt, f"{mode}-{index:02d}", action)
            after = set(profile_dir.glob(pattern))
            new = after - before
            if not before <= after or len(new) != 1 or next(iter(new)).stat().st_size == 0:
                raise RuntimeError(f"expected exactly one fresh nonempty training profile for {index}")
            raw.extend(new)
        return raw

    def record_tools(self, attempt, names):
        result = {}
        for name in names:
            env = {"LLVM_PROFILE_FILE": str(attempt / "version-%p.profraw")} if name == "instrumented_clang" else {}
            path = self.tools[name]
            version = self.run(attempt, name + "-version", self.action(self.tool(name, "--version"),
                                                                      extra_env=env))
            result[name] = {"path": str(path), **file_identity(path),
                            "version": version.read_text(errors="replace").strip()}
        return result

    def stage(self, name, attempt):
        if name == "instrumented-build":
            identity = self.current_identity
            if Path(self.paths["instrumented_root"]).exists():
                raise RuntimeError("instrumented build root already exists")
            for index, action in enumerate(self.custom(name)):
                self.run(attempt, f"build-{index}", action)
            tool_data = self.record_tools(attempt, ("instrumented_clang", "llvm_profdata"))
            source_record = self.root / "source-identity.json"
            tool_record = self.root / "ir-tools.json"
            save(source_record, identity)
            save(tool_record, tool_data)
            return [source_record, tool_record, self.tools["instrumented_clang"], self.tools["llvm_profdata"]]
        if name == "ir-train":
            return self.train_profiles("ir", attempt)
        if name == "merge-profdata":
            profiles = sorted((self.root / "ir").glob("*/*.profraw"))
            if len(profiles) != 23 or self.profdata.exists():
                raise RuntimeError("merge requires exactly 23 raw profiles and a fresh output")
            self.run(attempt, "merge", self.action(self.tool("llvm_profdata", "merge", "-o", self.profdata, *profiles)))
            return [self.profdata]
        if name == "pgo-build":
            if Path(self.paths["pgo_root"]).exists():
                raise RuntimeError("PGO build root already exists")
            for index, action in enumerate(self.custom(name)):
                self.run(attempt, f"build-{index}", action)
            total = {"main": 0, "runtime": 0}
            graphs = []
            for index, cwd in enumerate(self.ninja_roots):
                ninja = cwd / "build.ninja"
                if not ninja.is_file():
                    raise RuntimeError(f"missing Ninja graph: {ninja}")
                compdb = self.run(attempt, f"compdb-{index}", self.action(self.tool("ninja", "-t", "compdb"), cwd))
                result = check_compile_db(read(compdb), self.profile, runtime_only=index != 0)
                save(attempt / f"ninja-{index}.json", {"graph": str(ninja), **file_identity(ninja)})
                graphs.extend([compdb, attempt / f"ninja-{index}.json"])
                for key in total:
                    total[key] += result[key]
            if not all(total.values()):
                raise RuntimeError("Ninja check missed main or runtime compilation edges")
            save(attempt / "ninja-gate.json", {**total, "pgo_match": "UNKNOWN"})
            runtime = self.plan()[name][-1]
            log = self.run(attempt, "runtime-dependency-gate", runtime)
            return [*graphs, log, attempt / "ninja-gate.json"]
        if name == "bolt-tools-relink":
            for index, action in enumerate(self.custom("bolt-tools") + self.custom("relink-strip-debug")):
                self.run(attempt, f"build-{index}", action)
            sections = self.run(attempt, "bolt-input-sections",
                                self.action(self.tool("readelf", "--wide", "--section-headers", self.bolt_input)))
            text = sections.read_text()
            if not re.search(r"(?<!\S)\.rela?\.text(?:[.\s])", text) or re.search(r"\.(?:z?debug)_", text):
                raise RuntimeError("expected an emit-relocs BOLT input with debug sections stripped")
            record = self.root / "bolt-tools.json"
            save(record, self.record_tools(attempt, ("llvm_bolt", "merge_fdata")))
            return [record, self.tools["llvm_bolt"], self.tools["merge_fdata"], self.bolt_input, self.bolt_runtime]
        if name == "bolt-instrument-train-merge":
            (self.root / "bolt").mkdir(exist_ok=False)
            self.run(attempt, "instrument", self.instrument())
            profiles = self.train_profiles("bolt", attempt)
            self.run(attempt, "merge", self.action(self.tool("merge_fdata", *profiles), stdout=self.fdata))
            return [self.executable, *profiles, self.fdata]
        if name == "bolt-match":
            action = self.rewrite()
            product = Path(action["argv"][-1])
            if product.exists():
                raise RuntimeError("BOLT check output already exists")
            tool = read(self.root / "bolt-tools.json")["llvm_bolt"]
            trusted = file_identity(self.tools["llvm_bolt"]) == {key: tool[key] for key in ("bytes", "sha256")}
            if not trusted:
                raise RuntimeError("BOLT executable identity changed")
            action["trusted_tool"] = trusted
            log = self.run(attempt, "rewrite", action)
            gate = self.root / "bolt-match.json"
            save(gate, audit_log(log, action["argv"], True, trusted))
            return [product, log, gate]
        warnings = self.warnings()
        provenance = {"source_identity": read(self.root / "source-identity.json"), "training": self.rows,
                      "tools": {**read(self.root / "ir-tools.json"), **read(self.root / "bolt-tools.json")},
                      "bolt_input": file_identity(self.bolt_input), "bolt_runtime": file_identity(self.bolt_runtime),
                      "bolt_match": read(self.root / "bolt-match.json"), "pgo_match": "UNKNOWN",
                      "instrumentation_warnings": warnings}
        save(self.root / "provenance.json", provenance)
        manifest = generate(self.root, self.cfg["project"], self.cfg["llvm_version"], self.profdata, self.fdata, provenance)
        return [self.root / "llvm-profiles.manifest", self.root / "provenance.json",
                self.root / manifest["profiles"][1]["bolt_profile"]["file"],
                self.root / manifest["profiles"][1]["profdata"]["file"]]

    def warnings(self):
        report = {"count": 0, "first": None, "by_stage": {}}
        for stage in ("instrumented-build", "ir-train"):
            checkpoint = read(self.root / (stage + ".done.json"))
            count = 0
            for log in sorted(Path(checkpoint["attempt"]).glob("*.txt")):
                with log.open(errors="replace") as stream:
                    for line in stream:
                        if "LLVM Profile Warning" in line:
                            count += 1
                            if report["first"] is None:
                                report["first"] = {"log": str(log), "line": line.rstrip("\n")}
            report["by_stage"][stage] = count
            report["count"] += count
        return report

    def checkpoint(self, name):
        path = self.root / (name + ".done.json")
        if not path.exists():
            return False
        row = read(path)
        if row["identity"] != self.state_digest or row["stage"] != name:
            raise RuntimeError(f"checkpoint configuration or stage mismatch: {name}")
        for record in row["artifacts"]:
            if file_identity(record["path"]) != {key: record[key] for key in ("sha256", "bytes")}:
                raise RuntimeError(f"checkpoint artifact changed: {record['path']}")
        return True

    def recovery_receipt(self, path):
        receipt = read(absolute(path))
        if receipt["stage"] != "instrumented-build":
            raise RuntimeError("receipt must describe the instrumented build")
        for key, value in (("commit", self.cfg["source_commit"]), ("snapshot", self.cfg["snapshot"]),
                           ("recipe", file_identity(Path(self.paths["llvm"]) / "packaging/llvm.spec")),
                           ("gbs_config", file_identity(self.paths["gbs_config"]))):
            if receipt["source_identity"][key] != value:
                raise RuntimeError(f"retained build identity mismatch: {key}")
        if set(receipt["tools"]) != {"instrumented_clang", "llvm_profdata"}:
            raise RuntimeError("retained build receipt requires both IR tools")
        for name, record in receipt["tools"].items():
            if absolute(record["path"]) != self.tools[name] or not record["version"]:
                raise RuntimeError(f"retained tool path or version mismatch: {name}")
            if file_identity(self.tools[name]) != {k: record[k] for k in ("bytes", "sha256")}:
                raise RuntimeError(f"retained tool content mismatch: {name}")
        log = receipt["build_log"]
        path = absolute(log["path"])
        if file_identity(path) != {k: log[k] for k in ("bytes", "sha256")}:
            raise RuntimeError("retained build log content mismatch")
        with path.open(errors="replace") as stream:
            if not any(line.rstrip() == "PGO_INSTRUMENTED_BUILD_PASS" for line in stream):
                raise RuntimeError("retained build log has no instrumented build completion marker")
        return receipt

    def adopt_instrumented(self, receipt):
        if receipt["source_identity"] != self.current_identity:
            raise RuntimeError("retained build source identity does not match the current source")
        ir = self.root / "ir-tools.json"
        origin = self.root / "source-identity.json"
        log = receipt["build_log"]
        save(ir, receipt["tools"])
        save(origin, self.current_identity)
        files = [ir, origin, *map(Path, (row["path"] for row in receipt["tools"].values())), Path(log["path"])]
        save(self.root / "instrumented-build.done.json", {
            "stage": "instrumented-build", "identity": self.state_digest,
            "attempt": str(Path(log["path"]).parent),
            "artifacts": [{"path": str(p), **file_identity(p)} for p in files],
        })

    def execute(self, selected, resume, recovery=None, available=None):
        lock = absolute(self.resources["lock_path"])
        if self.root.is_symlink():
            raise ValueError("output root must not be a symbolic link")
        with owned_lock(lock):
            self.root.mkdir(exist_ok=resume)
            self.status["started_at"] = timestamp()
            try:
                if not self.admit(selected, available):
                    return
                self.verify_inputs()
                audit = self.root / ("inputs-" + str(time.time_ns()))
                audit.mkdir()
                self.current_identity = self.source_identity(audit)
                old_identity = self.root / "source-identity.json"
                if old_identity.exists() and read(old_identity) != self.current_identity:
                    raise RuntimeError("source, recipe, snapshot or build configuration changed")
                existing = [self.checkpoint(name) for name in STAGES]
                if recovery and not existing[0]:
                    self.adopt_instrumented(self.recovery_receipt(recovery))
                    existing[0] = self.checkpoint(STAGES[0])
                    if STAGES[0] not in selected:
                        self.status["stages"].append({"name": STAGES[0], "status": "REUSED"})
                planned = set(selected)
                for index, name in enumerate(STAGES):
                    if name in planned and not all(existing[j] or STAGES[j] in planned for j in range(index)):
                        raise RuntimeError(f"missing completed prerequisite for {name}")
                for index, name in enumerate(STAGES):
                    if name not in planned:
                        continue
                    if existing[index]:
                        self.status["stages"].append({"name": name, "status": "REUSED"})
                        continue
                    self.watchdog()
                    attempt = self.root / (name + "-" + str(time.time_ns()))
                    attempt.mkdir()
                    row = {"name": name, "status": "STOP", "attempt": str(attempt)}
                    self.status["stages"].append(row)
                    outputs = self.stage(name, attempt)
                    artifacts = [{"path": str(path), **file_identity(path)} for path in outputs]
                    if not all(x["bytes"] > 0 for x in artifacts):
                        raise RuntimeError(f"empty stage output: {name}")
                    cleanup = self.cfg.get("build_tree_cleanup", {}).get(name)
                    if cleanup:
                        project = self.expand(cleanup["project_root"])
                        tree = self.expand(cleanup["path"])
                        if any(Path(record["path"]).resolve().is_relative_to(Path(tree)) for record in artifacts):
                            raise RuntimeError("a checkpoint artifact still resides in the intermediate build tree")
                        save(attempt / "cleanup-intent.json", {"path": tree, "retained": artifacts})
                        remove_tree(project, tree)
                    save(self.root / (name + ".done.json"), {"stage": name, "identity": self.state_digest,
                                                             "attempt": str(attempt), "artifacts": artifacts})
                    row["status"] = "PASS"
                all_complete = all(self.checkpoint(name) for name in STAGES)
                self.status["status"] = "UNQUALIFIED" if all_complete else "PARTIAL"
            except (RuntimeError, OSError, TypeError, ValueError, KeyError, KeyboardInterrupt) as error:
                self.status["reason"] = str(error) or type(error).__name__
                if "watchdog" in self.status:
                    self.status["status"] = "INTERRUPTED"
                    if self.status["stages"] and self.status["stages"][-1]["status"] == "STOP":
                        self.status["stages"][-1]["status"] = "INTERRUPTED"
                raise
            finally:
                self.status["ended_at"] = timestamp()
                save(self.root / "summary.json", self.status, replace=True)
                print(json.dumps(self.status, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--recover-instrumented", type=Path)
    parser.add_argument("--memory-available-bytes", type=int,
                        help="admission snapshot from the enclosing stage launcher")
    parser.add_argument("--stages", help="comma-separated stage names")
    args = parser.parse_args()
    try:
        cfg = read(absolute(args.config))
        if cfg["training"] == "bundled":
            training = Path(__file__).resolve().parents[1] / "references" / "training-set.json"
        else:
            training = absolute(cfg["training"])
        pipeline = Pipeline(cfg, args.output, read(training))
        selected = active_stages(args.stages)
        if args.recover_instrumented and not args.resume:
            raise ValueError("a retained instrumented build receipt requires --resume")
        if args.memory_available_bytes is not None and args.memory_available_bytes <= 0:
            raise ValueError("memory snapshot must be positive")
        if args.dry_run:
            print(json.dumps(pipeline.dry_run(selected, args.resume, args.recover_instrumented,
                                              args.memory_available_bytes), indent=2))
        else:
            def interrupt(signum, frame):
                raise KeyboardInterrupt(f"received signal {signum}")

            for signum in (signal.SIGTERM, signal.SIGHUP):
                signal.signal(signum, interrupt)
            pipeline.execute(selected, args.resume, args.recover_instrumented, args.memory_available_bytes)
    except (GateError, RuntimeError, OSError, KeyError, TypeError, ValueError, KeyboardInterrupt) as error:
        parser.exit(1, f"STOP: {error or type(error).__name__}\n")


if __name__ == "__main__":
    main()
