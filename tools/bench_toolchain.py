#!/usr/bin/env python3
"""Native LLVM throughput screening, without building LLVM or Chromium.

Requires Linux, Python 3, taskset, prlimit and setarch. Toolchain roots contain bin/clang,
bin/clang++, bin/ld.lld and bin/llvm-ar. Target is always ARMv7 Tizen; compiler
executables must be native host ELF files. Sequential jobs, bounded affinity,
4 GiB RLIMIT_AS per process, and at least 4 GiB available memory are enforced.
"""

import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import platform
import re
import shutil
import signal
import statistics
import struct
import subprocess
import sys
import tempfile
import time

WORKSPACE = Path(__file__).resolve().parents[1]
INPUTS = Path(__file__).resolve().parent / "bench_inputs"
TARGET = "armv7l-tizen-linux-gnueabi"
MEMORY_LIMIT = 4 * 1024 ** 3
SCHEMA = 1
sys.dont_write_bytecode = True


class BenchError(Exception):
    pass


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def json_digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    staged = path.with_suffix(path.suffix + ".tmp")
    staged.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    staged.replace(path)


def available_memory():
    fields = dict(line.split(":", 1) for line in Path("/proc/meminfo").read_text().splitlines())
    available = int(fields["MemAvailable"].split()[0]) * 1024
    # Respect a unified cgroup ceiling too, when present and readable.
    for line in Path("/proc/self/cgroup").read_text().splitlines():
        if line.startswith("0::"):
            base = Path("/sys/fs/cgroup") / line[3:].lstrip("/")
            try:
                ceiling = (base / "memory.max").read_text().strip()
                if ceiling != "max":
                    available = min(available, int(ceiling) - int((base / "memory.current").read_text()))
            except OSError:
                pass
    return available


def memory_guard():
    available = available_memory()
    if available < MEMORY_LIMIT:
        raise BenchError(f"LOW_MEMORY: {available} bytes available; need {MEMORY_LIMIT}")
    return available


def parse_cpus(text, allowed):
    if not text:
        return sorted(allowed)[:max(1, len(allowed) // 2)]
    chosen = set()
    for part in text.split(","):
        if re.fullmatch(r"\d+-\d+", part):
            low, high = map(int, part.split("-"))
            chosen.update(range(low, high + 1))
        elif part.isdecimal():
            chosen.add(int(part))
        else:
            raise BenchError("Invalid CPU list")
    if not chosen or not chosen <= allowed:
        raise BenchError("CPU list must be a nonempty subset of the current affinity")
    if len(chosen) > max(1, len(allowed) // 2):
        raise BenchError("CPU count exceeds the half-nproc ceiling")
    return sorted(chosen)


def named_paths(items):
    result = {}
    for item in items:
        if "=" not in item:
            raise BenchError("Use NAME=/absolute/path")
        name, value = item.split("=", 1)
        if not re.fullmatch(r"[A-Za-z0-9_-]+", name) or name in result:
            raise BenchError("Names must be unique and use letters, digits, '-' or '_'")
        result[name] = Path(value).resolve(strict=True)
    return result


def native_elf(path):
    with Path(path).open("rb") as stream:
        head = stream.read(20)
    expected = {"x86_64": 62, "aarch64": 183}.get(platform.machine())
    if len(head) < 20 or head[:4] != b"\x7fELF" or head[5] not in (1, 2):
        raise BenchError(f"Tool must be a native ELF, not a wrapper: {path}")
    machine = struct.unpack("<H" if head[5] == 1 else ">H", head[18:20])[0]
    if not expected or machine != expected:
        raise BenchError(f"Non-native tool refused: {path}, ELF machine {machine}")
    return machine


def summarize(samples):
    retained = samples[1:]
    if len(retained) < 2:
        raise BenchError("Need at least three runs: discard one, retain at least two")
    stats = {}
    for field in ("wall_s", "user_s", "sys_s", "max_rss_kib"):
        values = [s[field] for s in retained]
        mean = statistics.mean(values)
        stats[field] = {"median": statistics.median(values), "min": min(values),
                        "stddev": statistics.stdev(values), "max": max(values)}
        stats[field]["cv_pct"] = 100 * stats[field]["stddev"] / mean if mean else 0
    return {"discarded": 1, "retained": len(retained), "statistics": stats,
            "suspect_retained": sum(s["suspect"] for s in retained)}


def real_inputs(directory):
    units = []
    directory = Path(directory)
    if not directory.is_dir():
        raise BenchError(f"Missing real-TU directory: {directory}")
    for path in directory.glob("*.ii"):
        if not path.with_suffix(".flags.json").is_file():
            raise BenchError(f"Missing flags sidecar: {path}")
    # A strict whitelist prevents flags from silently reading files or loading code.
    flag_pattern = re.compile(
        r"(?:-std=(?:c\+\+|gnu\+\+)(?:11|14|17|20|23)|-O[0123sz]|"
        r"-g(?:0|1|2|3|line-tables-only)?|-f(?:no-)?(?:exceptions|rtti|"
        r"omit-frame-pointer|strict-aliasing|signed-char|unsigned-char|"
        r"unwind-tables|asynchronous-unwind-tables|function-sections|data-sections)|"
        r"-fPIC|-fno-semantic-interposition|-fvisibility-inlines-hidden|-fno-common|"
        r"-gdwarf-4|-frecord-gcc-switches|"
        r"-fvisibility=(?:hidden|default)|-m(?:cpu|arch|fpu)=[A-Za-z0-9_.+-]+|"
        r"-mfloat-abi=(?:soft|softfp|hard)|-m(?:thumb|arm)|-pthread)\Z")
    for sidecar in sorted(directory.glob("*.flags.json")):
        name = sidecar.name.removesuffix(".flags.json")
        if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
            raise BenchError(f"Invalid real-TU name: {name}")
        data = json.loads(sidecar.read_text())
        if data.get("target") != TARGET:
            raise BenchError(f"Target mismatch: {sidecar}")
        path = Path(data.get("input", directory / (name + ".ii"))).resolve(strict=True)
        if path.suffix != ".ii" or digest(path) != data.get("sha256"):
            raise BenchError(f"Real-TU input/hash mismatch: {sidecar}")
        flags = data.get("flags")
        if not isinstance(flags, list) or not flags or any(
                not isinstance(f, str) or not flag_pattern.fullmatch(f) for f in flags):
            raise BenchError(f"Unsupported real-TU flags: {sidecar}")
        for field in ("source", "original_command", "preprocess_command"):
            if not data.get(field):
                raise BenchError(f"Missing provenance {field}: {sidecar}")
        units.append({"name": "real_" + name, "path": path, "flags": flags,
                      "sha256": data["sha256"], "provenance": data})
    return units


class Runner:
    def __init__(self, args, directory, evidence):
        self.args, self.directory, self.evidence = args, directory, evidence
        self.serial = 0
        self.commands = []
        self.env = dict(os.environ)
        for key in ("CPATH", "CPLUS_INCLUDE_PATH", "C_INCLUDE_PATH", "LIBRARY_PATH",
                    "GCC_EXEC_PREFIX", "COMPILER_PATH", "LD_PRELOAD", "LD_LIBRARY_PATH"):
            self.env.pop(key, None)
        self.env.update(LC_ALL="C", LANG="C", TMPDIR=str(directory),
                        LLVM_PROFILE_FILE=str(directory / "profile-%p.profraw"),
                        OMP_NUM_THREADS="1")

    def command(self, command, *, tag, timeout=None):
        memory_guard()
        self.serial += 1
        stem = self.evidence / f"{self.serial:05d}-{tag}"
        wrapped = ["taskset", "-c", ",".join(map(str, self.args.cpu_set)),
                   "prlimit", f"--as={MEMORY_LIMIT}:{MEMORY_LIMIT}", "--"]
        if getattr(self.args, "aslr", "off") == "off":
            wrapped += ["setarch", platform.machine(), "-R"]
        wrapped += list(map(str, command))
        before = list(os.getloadavg())
        killed = False
        with stem.with_suffix(".stdout").open("wb") as stdout, stem.with_suffix(".stderr").open("wb") as stderr:
            start = time.perf_counter()
            process = subprocess.Popen(wrapped, cwd=self.directory, env=self.env,
                                       stdout=stdout, stderr=stderr, start_new_session=True)

            def expire(signum, frame):
                nonlocal killed
                killed = True
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass

            old_handler = signal.signal(signal.SIGALRM, expire)
            signal.setitimer(signal.ITIMER_REAL, timeout or self.args.timeout)
            try:
                _, status, usage = os.wait4(process.pid, 0)
                elapsed = time.perf_counter() - start
                process.returncode = os.waitstatus_to_exitcode(status)
            except BaseException:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                _, status, _ = os.wait4(process.pid, 0)
                process.returncode = os.waitstatus_to_exitcode(status)
                raise
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)
                signal.signal(signal.SIGALRM, old_handler)
        after = list(os.getloadavg())
        record = {"argv": wrapped, "cwd": str(self.directory), "returncode": process.returncode,
                  "timed_out": killed, "wall_s": elapsed,
                  "user_s": usage.ru_utime, "sys_s": usage.ru_stime,
                  "max_rss_kib": usage.ru_maxrss, "load_before": before, "load_after": after,
                  "suspect": max(before[0], after[0]) > self.args.load_threshold,
                  "stdout": str(stem.with_suffix(".stdout")), "stderr": str(stem.with_suffix(".stderr"))}
        self.commands.append(record)
        # Persist failures immediately; successful metadata is also saved at run end.
        if process.returncode:
            save(self.evidence / "commands.json", self.commands)
            raise BenchError(f"Command failed ({process.returncode}, timeout={killed}): "
                             f"{command}; stderr={record['stderr']}")
        return record

    def measure(self, command, output, tag, repetitions):
        records = []
        for _ in range(repetitions):
            output.unlink(missing_ok=True)
            records.append(self.command(command, tag=tag))
            if not output.is_file() or output.stat().st_size == 0:
                raise BenchError(f"Missing/empty output: {output}")
        result = {key: sum(r[key] for r in records) / repetitions
                  for key in ("wall_s", "user_s", "sys_s")}
        result.update(max_rss_kib=max(r["max_rss_kib"] for r in records),
                      repetitions=repetitions, batch_wall_s=sum(r["wall_s"] for r in records),
                      load_before=records[0]["load_before"], load_after=records[-1]["load_after"],
                      suspect=any(r["suspect"] for r in records),
                      command_first=len(self.commands) - repetitions,
                      command_last=len(self.commands) - 1)
        return result


def compiler_flags(args, resource):
    return ["--target=" + TARGET, "--sysroot=" + str(args.sysroot),
            "-resource-dir=" + str(resource)]


def verify_object(path):
    with path.open("rb") as stream:
        head = stream.read(20)
    if head[:4] != b"\x7fELF" or head[4:6] != b"\x01\x01" or struct.unpack("<HH", head[16:20]) != (1, 40):
        raise BenchError(f"Expected ARM ELF relocatable object: {path}")


def toolchains(args, runner):
    result = {}
    for name, root in args.roots.items():
        tools = {}
        loader = args.loaders.get(name)
        library_path = args.library_paths.get(name)
        if loader:
            native_elf(loader)
        for tool in ("clang", "clang++", "ld.lld", "llvm-ar"):
            path = root / "bin" / tool
            machine = native_elf(path)
            prefix = ([str(loader)] if loader else [])
            if library_path:
                prefix += ["--library-path", str(library_path)]
            prefix += [str(path)]
            rec = runner.command(prefix + ["--version"], tag=name + "-identity")
            tools[tool] = {"path": str(path), "sha256": digest(path), "machine": machine,
                           "prefix": prefix, "version": Path(rec["stdout"]).read_text()}
        result[name] = {"root": str(root), "loader": str(loader) if loader else None, "tools": tools}
        if library_path:
            result[name]["library_path"] = str(library_path)
            result[name]["runtime_sha256"] = {p.name: digest(p) for p in sorted(library_path.iterdir()) if p.is_file()}
            result[name]["loader_sha256"] = digest(loader)
    return result


def markdown(result):
    lines = ["# LLVM throughput screening", "", f"Status: {result['status']}; real TU: {result['real_tu_status']}",
             f"CPU affinity: {result['protocol']['cpus']}; target: {TARGET}; first run discarded.", "",
             "| Toolchain | Case | Wall median (s/op) | Min | SD | CV % | User | Sys | Peak RSS KiB | Suspect | Ratio to first |",
             "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    baseline = {}
    for name, cases in result["results"].items():
        for case, value in cases.items():
            st = value["summary"]["statistics"]
            wall = st["wall_s"]
            baseline.setdefault(case, wall["median"])
            lines.append(f"| {name} | {case} | {wall['median']:.6f} | {wall['min']:.6f} | "
                         f"{wall['stddev']:.6f} | {wall['cv_pct']:.2f} | {st['user_s']['median']:.6f} | "
                         f"{st['sys_s']['median']:.6f} | {st['max_rss_kib']['max']:.0f} | "
                         f"{value['summary']['suspect_retained']} | {wall['median']/baseline[case]:.4f} |")
    lines += ["", "Lower time is better. Link/archive times are normalized per invocation; batching reduces timer noise.",
              "Peak RSS is the maximum retained process RSS, not divided by batch repetitions.",
              "A ranking here is not a prediction of full Chromium build speedup.", ""]
    return "\n".join(lines)


def single_run(args, prefix):
    started = time.monotonic()
    evidence = prefix.parent / (prefix.name + "-raw")
    if evidence.exists() or prefix.with_suffix(".json").exists():
        raise BenchError(f"Output already exists: {prefix}")
    evidence.mkdir(parents=True)
    result = {"schema": SCHEMA, "status": "RUNNING", "real_tu_status": "REAL_TU_ABSENT", "invocation": sys.argv,
              "results": {}, "start_time": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
    with tempfile.TemporaryDirectory(prefix="llvm-bench-", dir=args.work_dir) as scratch:
        directory = Path(scratch)
        runner = Runner(args, directory, evidence)
        try:
            memory_guard()
            spec = importlib.util.spec_from_file_location("synthetic", INPUTS / "generate_synthetic.py")
            generator = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(generator)
            cases = []
            for case, scale in zip("ABC", args.scales):
                generated = directory / ("generated-" + case)
                generator.generate(generated, scale, args.seed)
                cases.append({"name": case, "path": generated / (case + ".cpp"),
                              "flags": ["-std=c++17", "-O2"], "scale": scale,
                              "sha256": digest(generated / (case + ".cpp"))})
            real = real_inputs(args.real_tu_dir)
            if real:
                result["real_tu_status"] = "REAL_TU_PRESENT"
            cases += real
            identities = toolchains(args, runner)
            result["toolchains"] = identities
            inputs = [{k: str(v) if isinstance(v, Path) else v for k, v in c.items() if k != "path"} for c in cases]
            # Fix the resource headers for all variants, so compiler selection does not change inputs.
            result["protocol"] = {"target": TARGET, "sysroot": str(args.sysroot),
                "resource_dir": str(args.resource_dir), "resource_header_hash": args.resource_hash,
                "sysroot_header_hash": args.sysroot_hash, "cpus": args.cpu_set, "nproc": args.nproc,
                "runs": args.runs, "scales": args.scales, "seed": args.seed,
                "memory_limit_bytes": MEMORY_LIMIT, "load_threshold": args.load_threshold,
                "aslr": args.aslr,
                "link_repeats": args.link_repeats, "archive_repeats": args.archive_repeats,
                "link_threads": 1, "object_shards": args.shards, "inputs": inputs,
                "fixture_toolchain": next(iter(identities)),
                "fixture_compiler_hash": next(iter(identities.values()))["tools"]["clang++"]["sha256"],
                "generator_hash": digest(INPUTS / "generate_synthetic.py"),
                "harness_hash": digest(__file__), "work_filesystem": args.work_filesystem}
            result["protocol_hash"] = json_digest(result["protocol"])
            result["host"] = {"uname": list(platform.uname()), "mem_available_start": memory_guard(),
                              "inherited_affinity": args.inherited_affinity,
                              "cpu_model": next((l.split(":", 1)[1].strip() for l in Path("/proc/cpuinfo").read_text().splitlines() if l.startswith("model name")), "UNKNOWN"),
                              "cpu_frequency_policy": {str(c): {p: (Path(f"/sys/devices/system/cpu/cpu{c}/cpufreq") / p).read_text().strip() for p in ("scaling_governor", "energy_performance_preference", "scaling_max_freq") if (Path(f"/sys/devices/system/cpu/cpu{c}/cpufreq") / p).is_file()} for c in args.cpu_set}}
            base = compiler_flags(args, args.resource_dir)
            fixtures = directory / "fixtures"
            fixtures.mkdir()
            # Compile each unique B function exactly once, partitioned into many objects.
            body = cases[1]["path"].read_text()
            functions = body.split('extern "C"')[1:]
            fixture_tool = next(iter(identities.values()))["tools"]["clang++"]["prefix"]
            objects = []
            for index in range(args.shards):
                source = fixtures / f"part-{index:03}.cpp"
                source.write_text("".join('extern "C"' + f for f in functions[index::args.shards]))
                obj = source.with_suffix(".o")
                runner.command(fixture_tool + base + ["-std=c++17", "-O2", "-c", source, "-o", obj], tag="fixture")
                verify_object(obj)
                objects.append(obj)
            # Use A/C compiler outputs too; all variants then link/archive these identical objects.
            for case in (cases[0], cases[2]):
                obj = fixtures / (case["name"] + ".o")
                runner.command(fixture_tool + base + case["flags"] + ["-c", case["path"], "-o", obj], tag="fixture")
                verify_object(obj)
                objects.append(obj)
            result["fixture_objects"] = [{"name": p.name, "bytes": p.stat().st_size, "sha256": digest(p)} for p in objects]
            result["fixture_hash"] = json_digest(result["fixture_objects"])
            for name in identities:
                result["results"][name] = {c["name"]: {"samples": []} for c in cases}
                result["results"][name].update({"ld.lld": {"samples": []}, "llvm-ar": {"samples": []}})
            # Interleave variants per case/round, alternating order to reduce position bias.
            for iteration in range(args.runs):
                labels = list(identities)
                if iteration % 2:
                    labels.reverse()
                for case in cases + [{"name": "ld.lld"}, {"name": "llvm-ar"}]:
                    for name in labels:
                        output = directory / "measured-output"
                        tools = identities[name]["tools"]
                        key = case["name"]
                        repeats = 1
                        if key == "ld.lld":
                            command = tools[key]["prefix"] + ["-m", "armelf_linux_eabi", "-shared", "--threads=1", "-o", output] + objects
                            repeats = args.link_repeats
                        elif key == "llvm-ar":
                            command = tools[key]["prefix"] + ["rcsD", output] + objects
                            repeats = args.archive_repeats
                        else:
                            language = ["-x", "c++-cpp-output"] if key.startswith("real_") else []
                            command = tools["clang++"]["prefix"] + base + case["flags"] + language + ["-c", case["path"], "-o", output]
                        print(f"{prefix.name} {iteration+1}/{args.runs} {name} {key} x{repeats}", flush=True)
                        sample = runner.measure(command, output, name + "-" + key, repeats)
                        if key not in ("ld.lld", "llvm-ar"):
                            verify_object(output)
                        else:
                            with output.open("rb") as stream:
                                magic = stream.read(8)
                            if (key == "ld.lld" and magic[:4] != b"\x7fELF") or (key == "llvm-ar" and magic != b"!<arch>\n"):
                                raise BenchError(f"Unexpected {key} output format")
                        sample["iteration"] = iteration
                        sample["discarded"] = iteration == 0
                        result["results"][name][key]["samples"].append(sample)
                        output.unlink()
            for values in result["results"].values():
                for value in values.values():
                    value["summary"] = summarize(value["samples"])
            result["status"] = "MEASURED_WITH_WARNINGS" if any(v["summary"]["suspect_retained"] for values in result["results"].values() for v in values.values()) else "MEASURED"
        except BaseException as exc:
            result["status"] = "FAILED"
            result["error"] = str(exc)
            raise
        finally:
            result["duration_s"] = time.monotonic() - started
            result["peak_rss_kib_all_commands"] = max((c["max_rss_kib"] for c in runner.commands), default=0)
            result["scratch_directory"] = str(directory)
            save(evidence / "commands.json", runner.commands)
            save(prefix.with_suffix(".json"), result)
    result["scratch_removed"] = not directory.exists()
    save(prefix.with_suffix(".json"), result)
    prefix.with_suffix(".md").write_text(markdown(result))
    return result


def calibration(first, second, limit=3.0):
    if first["protocol_hash"] != second["protocol_hash"] or first["fixture_hash"] != second["fixture_hash"] or first["toolchains"] != second["toolchains"]:
        raise BenchError("Calibration inputs/protocol/tool identities changed")
    rows = []
    for name, cases in first["results"].items():
        for case, a in cases.items():
            b = second["results"][name][case]
            one = a["summary"]["statistics"]["wall_s"]
            two = b["summary"]["statistics"]["wall_s"]
            change = 100 * (two["median"] / one["median"] - 1)
            suspicious = a["summary"]["suspect_retained"] + b["summary"]["suspect_retained"]
            rows.append({"toolchain": name, "case": case, "run1_s": one["median"], "run2_s": two["median"],
                         "change_pct": change, "absolute_change_pct": abs(change),
                         "run1_cv_pct": one["cv_pct"], "run2_cv_pct": two["cv_pct"],
                         "suspect_retained": suspicious,
                         "pass": abs(change) <= limit and max(one["cv_pct"], two["cv_pct"]) <= limit and not suspicious})
    return {"schema": SCHEMA, "status": "PASS" if all(r["pass"] for r in rows) else "FAIL",
            "noise_floor_pct": max(r["absolute_change_pct"] for r in rows), "threshold_pct": limit,
            "protocol_hash": first["protocol_hash"], "rows": rows,
            "definition": "max absolute difference of corresponding wall medians; also require per-run CV <= threshold and no suspect retained samples"}


def header_tree_hash(root):
    # Hash the complete header input tree once, outside timing (follow file symlinks).
    h = hashlib.sha256()
    for base, dirs, files in os.walk(root):
        dirs.sort()
        for name in sorted(files):
            path = Path(base) / name
            if path.is_file():
                h.update(str(path.relative_to(root)).encode() + b"\0")
                h.update(digest(path).encode())
    return h.hexdigest()


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--toolchain", action="append", required=True, metavar="NAME=ROOT", help="repeat for multiple native toolchain roots; first supplies common link/archive objects")
    p.add_argument("--sysroot", type=Path, required=True, help="existing ARMv7 GBS root; never modified")
    p.add_argument("--resource-dir", type=Path, required=True, help="one fixed Clang resource directory (contains include/) for all compared variants")
    p.add_argument("--loader", action="append", default=[], metavar="NAME=ELF_LOADER", help="optional native dynamic loader; no chroot/accel, tool binaries unchanged")
    p.add_argument("--library-path", action="append", default=[], metavar="NAME=DIR", help="independent extracted runtime library directory; requires matching --loader, recorded with library hashes")
    p.add_argument("--cpus", help="taskset list; default first half of inherited CPU affinity, cannot exceed half")
    p.add_argument("--runs", type=int, default=5, help="total runs per case, including one discarded warmup (default 5)")
    p.add_argument("--scales", type=float, nargs=3, default=[1, 2, 2], metavar=("A", "B", "C"), help="historical generator scales (default 1 2 2); use 1 1 1 for historical input hashes")
    p.add_argument("--seed", type=int, default=73419, help="synthetic seed (default historical 73419); non-default seeds change all A/B/C")
    p.add_argument("--shards", type=int, default=64, help="split B into this many unique objects; add A/C (default total 66)")
    p.add_argument("--link-repeats", type=int, default=4096, help="links per sample to amortize short-command noise (default 4096)")
    p.add_argument("--archive-repeats", type=int, default=1024, help="archives per sample; fresh output each time (default 1024)")
    p.add_argument("--aslr", choices=("off", "on"), default="off", help="default off uses setarch -R only for benchmark child processes; on requires recalibration")
    p.add_argument("--real-tu-dir", type=Path, default=INPUTS / "real_tu", help="optional .ii + .flags.json directory; empty -> REAL_TU_ABSENT")
    p.add_argument("--timeout", type=float, default=180, help="seconds per subprocess before killing its process group")
    p.add_argument("--load-threshold", type=float, help="one-minute loadavg suspect threshold (default nproc/2)")
    p.add_argument("--work-dir", type=Path, default=Path("/dev/shm") if Path("/dev/shm").is_dir() else WORKSPACE / "temp", help="scratch parent on tmpfs or workspace temp; removed on success/failure")
    p.add_argument("--output", type=Path, default=WORKSPACE / "temp/bench_results" / time.strftime("bench-%Y%m%d-%H%M%S"), help="output prefix for JSON, markdown and raw logs")
    p.add_argument("--calibrate", action="store_true", help="two consecutive complete runs; exit 2 unless every case differs <=3%%, CV<=3%%, and no retained load warnings")
    args = p.parse_args(argv)
    try:
        memory_guard()
        for command in ("taskset", "prlimit") + (("setarch",) if args.aslr == "off" else ()):
            if not shutil.which(command):
                raise BenchError(f"Required program missing: {command}")
        args.roots, args.loaders = named_paths(args.toolchain), named_paths(args.loader)
        args.library_paths = named_paths(args.library_path)
        if args.loaders.keys() - args.roots.keys():
            raise BenchError("Loader name has no matching toolchain")
        if args.library_paths.keys() - args.loaders.keys():
            raise BenchError("Library path requires a matching --loader")
        if any(not path.is_dir() for path in args.library_paths.values()):
            raise BenchError("Library path must be a directory")
        allowed = os.sched_getaffinity(0)
        args.inherited_affinity = sorted(allowed)
        args.nproc = len(allowed)
        args.cpu_set = parse_cpus(args.cpus, allowed)
        # Keep the sampler on the same cores too: no variable cross-core wakeups.
        os.sched_setaffinity(0, args.cpu_set)
        if args.load_threshold is None:
            args.load_threshold = args.nproc / 2
        if args.runs < 3 or min(args.scales) <= 0 or not all(math.isfinite(x) for x in args.scales):
            raise BenchError("runs >=3 and positive finite scales required")
        if not 32 <= args.shards <= 256 or args.shards > round(400 * args.scales[1]):
            raise BenchError("shards must be 32..256 and not exceed the generated B function count")
        if min(args.link_repeats, args.archive_repeats) < 1 or args.timeout <= 0 or args.load_threshold <= 0:
            raise BenchError("Repetitions, timeout and load threshold must be positive")
        args.sysroot = args.sysroot.resolve(strict=True)
        args.resource_dir = args.resource_dir.resolve(strict=True)
        if not (args.sysroot / "usr/include/stdlib.h").is_file() or not (args.resource_dir / "include/stddef.h").is_file():
            raise BenchError("Missing sysroot C headers or resource builtin headers")
        args.work_dir = args.work_dir.resolve(strict=True)
        args.work_filesystem = subprocess.check_output(["stat", "-f", "-c", "%T", str(args.work_dir)], text=True).strip()
        if args.work_filesystem != "tmpfs" and not args.work_dir.is_relative_to(WORKSPACE / "temp"):
            raise BenchError("Scratch must be on tmpfs or within workspace temp/")
        if shutil.disk_usage(args.work_dir).free < MEMORY_LIMIT:
            raise BenchError("Scratch filesystem needs at least 4 GiB free")
        args.output = args.output.resolve()
        if args.output.suffix:
            raise BenchError("--output is a filename prefix without an extension")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        print("Hashing fixed header inputs (outside measurement)...", flush=True)
        args.resource_hash = header_tree_hash(args.resource_dir / "include")
        args.sysroot_hash = json_digest({"usr/include": header_tree_hash(args.sysroot / "usr/include"),
                                        "gcc": header_tree_hash(args.sysroot / "usr/lib/gcc")})
        if args.calibrate:
            one = single_run(args, args.output.with_name(args.output.name + "-run1"))
            two = single_run(args, args.output.with_name(args.output.name + "-run2"))
            result = calibration(one, two)
            save(args.output.with_suffix(".json"), result)
            lines = ["# Noise calibration", "", f"{result['status']}: noise floor {result['noise_floor_pct']:.3f}%", "",
                     "| Case | Run 1 s/op | Run 2 s/op | Difference % | CV 1 % | CV 2 % | Pass |",
                     "| --- | ---: | ---: | ---: | ---: | ---: | --- |"]
            for row in result["rows"]:
                lines.append(f"| {row['toolchain']}/{row['case']} | {row['run1_s']:.6f} | {row['run2_s']:.6f} | {row['change_pct']:.3f} | {row['run1_cv_pct']:.3f} | {row['run2_cv_pct']:.3f} | {row['pass']} |")
            args.output.with_suffix(".md").write_text("\n".join(lines) + "\n")
            print("\n".join(lines), flush=True)
            return 0 if result["status"] == "PASS" else 2
        single_run(args, args.output)
        print(args.output.with_suffix(".md"), flush=True)
        return 0
    except (BenchError, OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
