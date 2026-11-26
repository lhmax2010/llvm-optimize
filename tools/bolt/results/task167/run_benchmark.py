"""Run the four verified compiler roots with one worker per physical core."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from itertools import combinations
import json
import os
from pathlib import Path
from queue import SimpleQueue
import subprocess
import sys
import time
from zoneinfo import ZoneInfo

A = Path(__file__).resolve().parent
W = A.parents[1]
B = W.with_name(W.name + "-bolt")
OUT = A / "run"
CHECKED = W / "archive/task166/C"
DOC166 = B / "tools/bolt/results/task166/C/variants.json"
CORPUS = B / "tools/bolt/results/task158/corpus-config.json"
NAMES = ("V0", "V1", "V2", "V3")
ZONE = ZoneInfo("America/Los_Angeles")

sys.path.insert(0, str(B / "tools/bolt/bench"))
import bench


def now():
    return datetime.now(ZONE).isoformat()


def read(path):
    return json.loads(path.read_text())


def record(path, data):
    tmp = path.with_suffix(".tmp")
    bench.write_json(tmp, data)
    tmp.replace(path)


def topology():
    raw = subprocess.check_output(
        ["/usr/bin/lscpu", "-p=CPU,CORE,SOCKET,NODE,ONLINE"], text=True)
    allowed = os.sched_getaffinity(0)
    online = []
    cores = {}
    for line in raw.splitlines():
        if line.startswith("#"):
            continue
        cpu, core, socket, _, status = line.split(",")
        if status == "Y":
            online.append((int(cpu), int(socket), int(core)))
            if int(cpu) in allowed:
                cores.setdefault((int(socket), int(core)), int(cpu))
    if len(cores) != len({(socket, core) for _, socket, core in online}) or len(cores) < 3:
        raise RuntimeError("host physical cores are not all available to this task")
    ordered = sorted(cores.values())
    return raw, ordered[2:], ordered[:2], sorted(allowed)


def temperature():
    values = {}
    for zone in sorted(Path("/sys/class/thermal").glob("thermal_zone*")):
        try:
            label = (zone / "type").read_text().strip()
            value = int((zone / "temp").read_text()) / 1000
        except (OSError, ValueError):
            continue
        if -40 <= value <= 150:
            values[f"{zone.name}:{label}"] = value
    return values


def environment(cpus):
    sample = bench.capture_environment(
        cpus, ["build", "cmake", "clang", "clang-22", "clang++", "gcc", "g++", "cc1", "cc1plus"])
    sample.update(at=now(), temperature_c=temperature(),
                  other_build_processes_sampled=bool(sample["build_process_names"]))
    sample.pop("other_project_build")
    sample.pop("other_project_identity_comm")
    return sample


def batch(compiler, inputs, cpus, work, dest):
    logs = dest / "logs"
    objects = dest / "objects"
    logs.mkdir(parents=True)
    objects.mkdir()
    slots = SimpleQueue()
    for cpu in cpus:
        slots.put(cpu)

    def worker_init():
        os.sched_setaffinity(0, {slots.get()})

    def measure(tu):
        affinity = sorted(os.sched_getaffinity(0))
        if len(affinity) != 1 or affinity[0] not in cpus:
            raise RuntimeError(f"invalid worker affinity: {affinity}")
        row = bench.measure(compiler, tu, affinity, work, logs, objects, float("inf"))
        row["cpu"] = affinity[0]
        row["anomalous"] = bench.anomalous(row)
        return row

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=len(cpus), initializer=worker_init) as pool:
        rows = list(pool.map(measure, inputs))
    return bench.batch_summary(rows, [], time.perf_counter() - start)


def compare_round(batches, inputs):
    by_variant = {name: {r["tu"]: r for r in batches[name]["measurements"]} for name in NAMES}
    comparisons = []
    for tu in inputs:
        for left, right in combinations(NAMES, 2):
            a = by_variant[left][tu["id"]].get("object")
            b = by_variant[right][tu["id"]].get("object")
            comparisons.append({"tu": tu["id"], "left": left, "right": right,
                                **bench.compare_objects(a, b)})
    return comparisons


def run():
    config = read(CORPUS)
    inputs = config["inputs"]
    variants = read(CHECKED / "variants.json")
    if variants != read(DOC166) or len(inputs) != 177 or len({tu["id"] for tu in inputs}) != 177:
        raise RuntimeError("unexpected variant receipt or corpus size")
    for tu in inputs:
        path = Path(tu["path"])
        if (tu["training_source_overlap"] or tu["training_sha256_overlap"] or "-O2" not in tu["flags"]
                or path.stat().st_size != tu["bytes"] or bench.digest(path) != tu["sha256"]):
            raise RuntimeError(f"TU identity or held-out check failed: {tu['id']}")
    alias = CHECKED / "fixed/root"
    layouts = []
    for name in NAMES:
        variant = variants[name]
        if (variant["status"] != "PASS" or bench.digest(Path(variant["clang"])) != variant["sha256"]
                or bench.digest(Path(variant["loader"])) != variant["loader_sha256"]):
            raise RuntimeError(f"compiler or loader identity check failed: {name}")
        rebased = bench.variant_at(variant, alias)
        layouts.append([rebased["clang"], rebased["loader"], rebased["library_path"]])
    if any(row != layouts[0] for row in layouts[1:]):
        raise RuntimeError("private roots have inconsistent relative runtime layouts")
    raw, cpus, reserved, allowed = topology()
    OUT.mkdir()
    work = OUT / "work"
    work.mkdir()
    (OUT / "cpu-topology.csv").write_text(raw)
    record(OUT / "manifest.json", {"started_at": now(), "jobs": len(cpus), "cpus": cpus, "reserved": reserved,
           "allowed": allowed, "variants": variants, "corpus": str(CORPUS), "corpus_sha256": bench.digest(CORPUS),
           "inputs": inputs, "fixed_root": str(alias), "fixed_work": str(work), "rounds": 5})
    print(f"START {now()} concurrent={len(cpus)} cpus={cpus} tus={len(inputs)}", flush=True)
    # This task has no MemAvailable floor. The original harness retains its
    # default for other callers.
    bench.MIN_AVAILABLE = 0
    original_root = alias.resolve(strict=True)

    try:
        for index in range(6):
            phase = "warmup" if index == 0 else f"round-{index:02}"
            order = bench.rotation(NAMES, max(0, index - 1))
            row = {"round": index, "order": order, "environment_start": environment(cpus), "variants": {}}
            batches = row["variants"]
            for name in order:
                print(f"BEGIN {now()} {phase} {name}", flush=True)
                compiler = bench.use_variant(variants[name], alias)
                metrics = batch(compiler, inputs, cpus, work, OUT / phase / name)
                batches[name] = metrics
                print(f"END {now()} {phase} {name} cpu={metrics['tu_cpu_seconds_sum']:.3f} "
                      f"wall={metrics['elapsed_seconds']:.3f} pass={metrics['all_passed']}", flush=True)
            if index:
                for name in order:
                    initial = batches[name]
                    if any(s["anomalous"] for s in initial["measurements"]):
                        compiler = bench.use_variant(variants[name], alias)
                        repeat = bench.repeat_batch(initial, compiler, inputs, [cpus[0]], work,
                                                   OUT / phase / name, float("inf"))
                        initial["anomaly_retries"] = repeat["anomaly_retries"]
                        initial["retry_elapsed_seconds"] = repeat["retry_elapsed_seconds"]
            row["comparisons"] = compare_round(batches, inputs)
            row["environment_end"] = environment(cpus)
            row["group"] = "interference" if any(
                row[key]["other_build_processes_sampled"] for key in ("environment_start", "environment_end")
            ) else "quiet"
            record(OUT / (phase + ".json"), row)
            print(f"RECORDED {now()} {phase} {row['group']}", flush=True)
    finally:
        original = next(v for v in variants.values() if Path(v["root"]).resolve() == original_root)
        bench.use_variant(original, alias)
    record(OUT / "complete.json", {"ended_at": now(), "formal_rounds": 5})
    print(f"COMPLETE {now()}", flush=True)


if __name__ == "__main__":
    run()
