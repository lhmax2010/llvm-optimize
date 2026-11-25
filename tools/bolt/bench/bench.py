#!/usr/bin/env python3
"""Measure isolated compiles of preprocessed Tizen translation units."""
import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
import filecmp
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import statistics
import subprocess
import sys
import tempfile
import time

GIB = 2**30
MIN_AVAILABLE = 6 * GIB
TASKSET = "/usr/bin/taskset"
TIME = "/usr/bin/time"
OBJCOPY = "/usr/bin/objcopy"
GENERIC_BUILD_COMM = {"gbs", "gbs-build", "rpmbuild", "ninja", "make", "llvm-bolt", "ld.lld"}

def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False) + "\n")

def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()

def available():
    with open("/proc/meminfo") as stream:
        return next(int(row.split()[1]) * 1024 for row in stream if row.startswith("MemAvailable:"))

def memory_guard():
    start = time.monotonic()
    while (measured := available()) < MIN_AVAILABLE:
        print(f"PAUSE: MemAvailable={measured} B", file=sys.stderr, flush=True)
        time.sleep(10)
    return time.monotonic() - start

def parse_cpus(text, allowed):
    cpus = set()
    for token in text.split(","):
        if not re.fullmatch(r"[0-9]+(?:-[0-9]+)?", token):
            raise ValueError("Invalid CPU list")
        ends = list(map(int, token.split("-")))
        if len(ends) == 2 and (ends[1] < ends[0] or ends[1] - ends[0] >= 4):
            raise ValueError("Invalid CPU range or more than four CPUs")
        cpus.update(range(ends[0], ends[-1] + 1))
    if len(cpus) > 4 or not cpus or not cpus <= allowed:
        raise ValueError("Select one to four available CPUs")
    return sorted(cpus)

def capture_environment(cpus, other_comm):
    governors = {}
    for cpu in cpus:
        path = Path(f"/sys/devices/system/cpu/cpu{cpu}/cpufreq/scaling_governor")
        try:
            governors[str(cpu)] = path.read_text().strip()
        except OSError:
            governors[str(cpu)] = None
    counts = Counter()
    names = GENERIC_BUILD_COMM | set(other_comm)
    for entry in Path("/proc").iterdir():
        if not entry.name.isdecimal():
            continue
        try:
            comm = (entry / "comm").read_text(errors="replace").strip()
        except OSError:
            continue
        if comm in names:
            counts[comm] += 1
    visible = any(counts[n] for n in other_comm)
    return {"at_unix": time.time(), "loadavg": list(os.getloadavg()),
            "governors": governors, "build_process_names": dict(counts),
            "other_project_build": ("OBSERVED" if visible else "NOT_OBSERVED") if other_comm else "UNKNOWN",
            "other_project_identity_comm": other_comm, "mem_available": available()}

def rotation(keys, round_index):
    offset = round_index % len(keys)
    return keys[offset:] + keys[:offset]

def quartiles(values):
    ordered = sorted(values)
    if not ordered:
        return None
    q1, _, q3 = statistics.quantiles(ordered, n=4, method="inclusive") if len(ordered) > 1 else [ordered[0]]*3
    return {"count": len(ordered), "min": ordered[0], "q1": q1, "median": statistics.median(ordered),
            "q3": q3, "max": ordered[-1], "iqr": q3-q1}

def argv_for(variant, input_row, output):
    return [variant["loader"], "--inhibit-cache", "--library-path", ":".join(variant["library_path"]),
            variant["clang"], "--no-default-config", "-fintegrated-cc1",
            *input_row["flags"], "-x", {"c":"cpp-output", "c++":"c++-cpp-output"}[input_row["language"]],
            "-c", input_row["path"], "-o", str(output)]

def variant_at(variant, alias):
    root = Path(variant["root"])
    if not root.is_absolute() or not root.is_dir():
        raise ValueError(f"Invalid private root {root}")

    def rebase(value):
        original = Path(value)
        original.resolve(strict=True).relative_to(root.resolve())
        return str(alias / original.relative_to(root))

    return {**variant, "loader": rebase(variant["loader"]), "clang": rebase(variant["clang"]),
            "library_path": [rebase(value) for value in variant["library_path"]]}

def use_variant(variant, alias):
    compiler = variant_at(variant, alias)
    temporary = alias.with_suffix(".next")
    temporary.symlink_to(variant["root"], target_is_directory=True)
    temporary.replace(alias)
    # The kernel resolves symlink targets for /proc/self/exe. The compiler
    # records that executable path, so the loader itself needs a stable file.
    loader = alias.parent / "loader"
    temporary = loader.with_suffix(".next")
    shutil.copy2(variant["loader"], temporary)
    temporary.replace(loader)
    compiler["loader"] = str(loader)
    return compiler

def terminate_child(process):
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait()

def measure(variant, tu, cpus, work, logs, objects, timeout):
    ident = tu["id"]
    path = work / (ident + ".o")
    logstem = logs / ident
    time_file = logstem.with_suffix(".time")
    stdout = logstem.with_suffix(".stdout")
    stderr = logstem.with_suffix(".stderr")
    done = objects / path.name
    command = [TIME, "-f", "%U\t%S\t%M", "-o", str(time_file),
               TASKSET, "--cpu-list", ",".join(map(str, cpus)), *argv_for(variant, tu, path)]
    attempts = []
    paused_seconds = 0
    path.unlink(missing_ok=True)
    while True:
        paused_seconds += memory_guard()
        start = time.perf_counter()
        interruption = None
        with stdout.open("wb") as out, stderr.open("wb") as err:
            process = subprocess.Popen(command, cwd=work, env={**os.environ, "LC_ALL":"C",
                   "LD_LIBRARY_PATH":"", "LD_PRELOAD":""}, start_new_session=True,
                   stdout=out, stderr=err)
            try:
                while process.poll() is None:
                    if available() < MIN_AVAILABLE:
                        interruption = "LOW_MEMORY"
                    elif time.perf_counter() - start > timeout:
                        interruption = "TIMEOUT"
                    if interruption:
                        terminate_child(process)
                        break
                    try:
                        process.wait(timeout=0.5)
                    except subprocess.TimeoutExpired:
                        pass
            finally:
                if process.poll() is None:
                    terminate_child(process)
        seconds = time.perf_counter() - start
        if interruption == "LOW_MEMORY":
            attempts.append({"state": interruption, "elapsed_seconds": seconds})
            for f in (stdout, stderr, time_file):
                if f.exists():
                    f.rename(f.with_name(f.name+f".paused-{len(attempts)}"))
            path.unlink(missing_ok=True)
            continue
        rc = process.returncode
        row = {"tu": ident, "package": tu["package"], "language": tu["language"],
               "wall_seconds": seconds, "rc": rc, "interruption": interruption,
               "stdout": str(stdout), "stderr": str(stderr), "command": command,
               "memory_interruptions": attempts, "memory_wait_seconds": paused_seconds}
        if time_file.exists():
            measured = time_file.read_text().splitlines()
            match = re.fullmatch(r"([0-9.]+)\s+([0-9.]+)\s+(\d+)", measured[-1]) if measured else None
            if match:
                user, sys_cpu, rss = match.groups()
                row.update(user_seconds=float(user), sys_seconds=float(sys_cpu),
                           cpu_seconds=float(user)+float(sys_cpu), max_rss_bytes=int(rss)*1024)
        success = rc == 0 and path.is_file() and path.stat().st_size and "cpu_seconds" in row
        row["status"] = "PASS" if success else "FAIL"
        if success:
            path.rename(done)
            row["object"] = {"path": str(done), "bytes": done.stat().st_size, "sha256": digest(done)}
        return row

def compare_objects(a, b):
    if not (a and b):
        return {"status": "UNVERIFIED"}
    if filecmp.cmp(a["path"], b["path"], shallow=False):
        return {"status": "IDENTICAL"}
    result = {"status": "DIFFERENT"}
    with tempfile.TemporaryDirectory(dir=Path(a["path"]).parent) as directory:
        dest = [Path(directory) / name for name in ("baseline.o", "candidate.o")]
        for original, target in zip((a, b), dest):
            try:
                p = subprocess.run([OBJCOPY, "--remove-section=.GCC.command.line", original["path"], target],
                                   capture_output=True, text=True, timeout=60)
            except (OSError, subprocess.TimeoutExpired) as error:
                result["without_command_line"] = "UNVERIFIED"
                result["objcopy_error"] = str(error)
                return result
            if p.returncode:
                result["without_command_line"] = "UNVERIFIED"
                result["objcopy_error"] = p.stderr
                return result
        result["without_command_line"] = "IDENTICAL" if filecmp.cmp(*dest, shallow=False) else "DIFFERENT"
    return result

def compare_round(round_data, baseline):
    by_variant = {n: {r["tu"]: r for r in x["measurements"]} for n,x in round_data["variants"].items()}
    comparisons = []
    for name, by_tu in by_variant.items():
        if name == baseline:
            continue
        for ident, ref in by_variant[baseline].items():
            row = by_tu[ident]
            a, b = ref.get("object"), row.get("object")
            comparisons.append({"variant":name, "tu":ident, "baseline":a, "candidate":b,
                                **compare_objects(a, b)})
    return comparisons

def anomalous(row):
    return (row["status"] == "PASS" and row["wall_seconds"] > 1.5 * row["cpu_seconds"]
            and row["wall_seconds"] - row["cpu_seconds"] > 1)

def batch_summary(measurements, retries, elapsed):
    return {"measurements":measurements, "anomaly_retries":retries, "elapsed_seconds":elapsed,
            "tu_wall_seconds_sum":sum(s["wall_seconds"] for s in measurements),
            "tu_cpu_seconds_sum":sum(s.get("cpu_seconds", 0) for s in measurements),
            "all_passed":all(s["status"]=="PASS" for s in measurements),
            "scored":all(s["status"]=="PASS" and not s["anomalous"] for s in measurements)}

def run_batch(compiler, inputs, cpus, work, root, timeout, jobs):
    logs, objects = root / "logs", root / "objects"
    logs.mkdir(parents=True)
    objects.mkdir()
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=jobs) as threads:
        initial = list(threads.map(lambda t: measure(compiler, t, cpus, work, logs, objects, timeout), inputs))
    for row in initial:
        row["anomalous"] = anomalous(row)
    return batch_summary(initial, [], time.perf_counter()-start)

def repeat_batch(batch, compiler, inputs, cpus, work, root, timeout):
    logs, objects = root / "retry-logs", root / "retry-objects"
    logs.mkdir()
    objects.mkdir()
    measurements, retries = [], []
    start = time.perf_counter()
    for row, tu in zip(batch["measurements"], inputs):
        selected = row
        if row["anomalous"]:
            selected = measure(compiler, tu, cpus, work, logs, objects, timeout)
            selected["anomalous"] = anomalous(selected)
            retries.append({"initial": row, "retry": selected,
                            "objects": compare_objects(row.get("object"), selected.get("object"))})
        measurements.append(selected)
    result = batch_summary(measurements, retries, batch["elapsed_seconds"])
    result["retry_elapsed_seconds"] = time.perf_counter()-start
    return result

def round_group(row):
    return "interference" if any(
        sample["build_process_names"] for sample in (row["environment_start"], row["environment_end"])
    ) else "quiet"

def summarize(rounds, variants, baseline, jobs):
    totals = defaultdict(list)
    successful_totals = defaultdict(list)
    cpu = defaultdict(list)
    ratios = defaultdict(lambda: defaultdict(list))
    for row in rounds:
        base = row["variants"][baseline]
        reference = {r["tu"]:r for r in base["measurements"]}
        for name, data in row["variants"].items():
            totals[name].append(data["tu_wall_seconds_sum"])
            if data.get("scored", data["all_passed"]):
                if jobs == 1 or not data.get("anomaly_retries"):
                    successful_totals[name].append(data["tu_wall_seconds_sum"] if jobs == 1 else data["elapsed_seconds"])
                cpu[name].append(data["tu_cpu_seconds_sum"])
            for r in data["measurements"]:
                prior = reference[r["tu"]]
                if (r["status"] == prior["status"] == "PASS" and r["cpu_seconds"] > 0
                        and not (r.get("anomalous") or prior.get("anomalous"))):
                    ratios[name][r["tu"]].append(prior["cpu_seconds"]/r["cpu_seconds"])
    baseline_stats = quartiles(cpu[baseline])
    result = {}
    for name in variants:
        primary = quartiles(cpu[name])
        speed = (baseline_stats["median"]/primary["median"] if primary and baseline_stats and primary["median"] else None)
        per_tu = {ident:statistics.median(vals) for ident,vals in ratios[name].items()}
        counts = Counter(c["status"] for rd in rounds for c in rd["comparisons"] if c["variant"]==name)
        result[name] = {"total_seconds":primary,"observed_tu_wall_seconds_sum":quartiles(totals[name]),
                        "total_cpu_seconds":primary,"total_wall_seconds":quartiles(successful_totals[name]),"speedup_vs_baseline":speed,
                        "per_tu_speedup":per_tu,"per_tu_distribution":quartiles(list(per_tu.values())),
                        "object_comparisons":dict(counts)}
    return result

def markdown(result):
    text = [f"# {result['label']}", "", f"Rounds {len(result['rounds'])}, jobs {result['jobs']}, CPUs {result['cpus']}.",
            "", "One warmup batch per variant is excluded. The primary metric is user + system CPU time.",
            "", "| Variant | Valid rounds | Median CPU (s) | CPU IQR (s) | Median wall (s) | Speedup vs V0 | Per-TU speedup Q1 / median / Q3 | Objects |",
            "|---|---:|---:|---:|---:|---:|---|---|"]
    for name,row in result["summary"].items():
        tot,dist = row["total_seconds"],row["per_tu_distribution"]
        numbers = " / ".join(f"{dist[k]:.3f}×" for k in ("q1","median","q3")) if dist else "—"
        speed = f"{row['speedup_vs_baseline']:.3f}×" if row["speedup_vs_baseline"] is not None else "—"
        count = row["object_comparisons"]
        wall = row["total_wall_seconds"]
        marker = "🔴 " if count.get("DIFFERENT") else ""
        text.append(f"| {name} | {tot['count'] if tot else 0} | "
                    f"{format(tot['median'],'.3f') if tot else '—'} | "
                    f"{format(tot['iqr'],'.3f') if tot else '—'} | {format(wall['median'],'.3f') if wall else '—'} | {speed} | {numbers} | "
                    f"{marker}{count.get('IDENTICAL',0)} same / {count.get('DIFFERENT',0)} different / "
                    f"{count.get('UNVERIFIED',0)} unverified |")
    text.extend(["","## Quiet and interference rounds","",
                 "Interference means that a sampled process name matched a build tool. Generic names cannot identify the owning project.",
                 "", "| Group | Variant | Valid rounds | Median CPU (s) | Median wall (s) |", "|---|---|---:|---:|---:|"])
    for group, summary in result["groups"].items():
        for name, row in summary.items():
            cpu, wall = row["total_cpu_seconds"], row["total_wall_seconds"]
            text.append(f"| {group} | {name} | {cpu['count'] if cpu else 0} | "
                        f"{format(cpu['median'],'.3f') if cpu else '—'} | {format(wall['median'],'.3f') if wall else '—'} |")
    text.extend(["","## Object differences, failures, and retries",""])
    for rd in result["rounds"]:
        for c in rd["comparisons"]:
            if c["status"] != "IDENTICAL":
                diagnostic = f" Without .GCC.command.line: {c['without_command_line']}." if "without_command_line" in c else ""
                text.append(f"- {'🔴 ' if c['status']=='DIFFERENT' else ''}Round {rd['round']} · {c['variant']} · {c['tu']} · {c['status']}.{diagnostic}")
        for name,d in rd["variants"].items():
            for retry in d["anomaly_retries"]:
                text.append(f"- Round {rd['round']} · {name} · {retry['initial']['tu']} · anomalous sample repeated once.")
            for r in d["measurements"]:
                if r["status"] == "FAIL":
                    text.append(f"- Round {rd['round']} · {name} · {r['tu']} · compile exit {r['rc']}.")
    return "\n".join(text)+"\n"

def run_bench(config, dest, *, rounds, jobs, cpus, variants, label, timeout, other_comm):
    dest.mkdir()
    inputs = config["inputs"]
    ids = [t["id"] for t in inputs]
    if not ids or len(set(ids)) != len(ids) or any(not re.fullmatch(r"[\w-]+",ident) for ident in ids):
        raise ValueError("Use unique nonempty TU IDs containing letters, digits, '_' or '-'")
    for t in inputs:
        memory_guard()
        if digest(Path(t["path"])) != t["sha256"] or "-O2" not in t["flags"]:
            raise ValueError(f"Input identity or -O2 check failed: {t['id']}")
    for name in variants:
        memory_guard()
        clang = config["variants"][name]
        if digest(Path(clang["clang"])) != clang["sha256"]:
            raise ValueError(f"Compiler identity failed: {name}")
    work = dest / "work"
    work.mkdir()
    alias = dest / "current-root"
    all_layouts = [variant_at(config["variants"][name], alias) for name in variants]
    if any(any(a[field] != all_layouts[0][field] for field in ("loader", "clang", "library_path"))
           for a in all_layouts[1:]):
        raise ValueError("All variants must provide identical relative loader, library, and compiler paths")
    warmup = {}
    for name in variants:
        compiler = use_variant(config["variants"][name], alias)
        warmup[name] = run_batch(compiler, inputs, cpus, work, dest / "warmup" / name,
                                 timeout, jobs)
    write_json(dest / "warmup.json", warmup)
    collected = []
    for i in range(rounds):
        order = rotation(variants,i)
        row = {"round":i+1,"order":order,"environment_start":capture_environment(cpus,other_comm),"variants":{}}
        for name in order:
            memory_guard()
            compiler = use_variant(config["variants"][name], alias)
            row["variants"][name] = run_batch(compiler, inputs, cpus, work, dest / f"round-{i+1:02}" / name,
                                              timeout, jobs)
        for name in order:
            batch = row["variants"][name]
            if any(s["anomalous"] for s in batch["measurements"]):
                compiler = use_variant(config["variants"][name], alias)
                row["variants"][name] = repeat_batch(batch, compiler, inputs, cpus, work,
                                                     dest / f"round-{i+1:02}" / name, timeout)
        row["comparisons"] = compare_round(row, "V0")
        row["environment_end"] = capture_environment(cpus,other_comm)
        row["group"] = round_group(row)
        collected.append(row)
        write_json(dest / f"round-{i+1:02}.json",row)
    result = {"label":label,"jobs":jobs,"cpus":cpus,"common_root":str(alias),"rounds":collected,
              "warmup":warmup,"summary":summarize(collected,variants,"V0",jobs),
              "groups":{group:summarize([row for row in collected if row["group"]==group],variants,"V0",jobs)
                        for group in ("quiet","interference")}}
    write_json(dest/"results.json",result)
    (dest/"results.md").write_text(markdown(result))
    return result

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("config",type=Path)
    p.add_argument("output",type=Path)
    p.add_argument("--rounds",type=int,default=5)
    p.add_argument("-j","--jobs",type=int,default=1)
    p.add_argument("--cpus")
    p.add_argument("--variants")
    p.add_argument("--timeout",type=float,default=600)
    p.add_argument("--label",default="Held-out compiler throughput")
    p.add_argument("--other-build-comm",action="append",default=[],
                   help="A caller-verified process name unique to the other project")
    opt = p.parse_args()
    cfg = json.loads(opt.config.read_text())
    chosen = opt.variants.split(",") if opt.variants else [n for n,v in cfg["variants"].items() if v.get("status")=="PASS"]
    if ("V0" not in chosen or len(chosen) != len(set(chosen)) or any(
            not re.fullmatch(r"V[0-3]",n) or cfg["variants"].get(n,{}).get("status")!="PASS" for n in chosen)):
        p.error("Select runnable, distinct variants including V0")
    allowed = os.sched_getaffinity(0)
    cpus = parse_cpus(opt.cpus or str(min(allowed)),allowed)
    if not (0 < opt.rounds and 0 < opt.jobs <= len(cpus) and 0 < opt.timeout):
        p.error("rounds and timeout must be positive; jobs must fit the selected CPUs")
    run_bench(cfg,opt.output.resolve(),rounds=opt.rounds,jobs=opt.jobs,cpus=cpus,variants=chosen,
              label=opt.label,timeout=opt.timeout,other_comm=opt.other_build_comm)

if __name__ == "__main__":
    main()
