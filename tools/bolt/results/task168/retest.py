"""Controlled compiler-only retest on separately identified performance cores."""
from collections import Counter, defaultdict
import os
from pathlib import Path
import statistics
import subprocess
import sys
from threading import Event, Thread
import time

from paired import A, W, OLD, read, rounds_in, stored_time

sys.path.insert(0, str(W/"archive/task167"))
import run_benchmark as prior

BENCH = prior.bench
OUT = A/"run"


def cpulist(text):
    cpus = set()
    for item in text.split(","):
        bounds = list(map(int, item.split("-")))
        cpus.update(range(bounds[0], bounds[-1]+1))
    return cpus


def find_cores():
    argv = ["/usr/bin/lscpu", "-p=CPU,CORE,SOCKET,NODE,ONLINE,MAXMHZ"]
    raw = subprocess.check_output(argv, text=True)
    rows = {}
    for line in raw.splitlines():
        if not line.startswith("#"):
            cpu, core, socket, _, online, maxmhz = line.split(",")
            if online == "Y":
                rows[int(cpu)] = {"core": (int(socket), int(core)), "max_mhz": float(maxmhz)}
    usable = set(rows) & os.sched_getaffinity(0)
    sysfs = {}
    for kind in ("core", "atom"):
        file = Path(f"/sys/devices/cpu_{kind}/cpus")
        if file.is_file():
            sysfs[str(file)] = file.read_text().strip()
    if len(sysfs) == 2:
        p, e = (cpulist(spec) for spec in sysfs.values())
        if p & e or not usable <= p | e:
            raise RuntimeError("kernel core classifications do not cover the usable CPU set")
        source = "kernel cpu_core/cpus and cpu_atom/cpus"
    else:
        maximum = max(rows[cpu]["max_mhz"] for cpu in usable)
        p = {cpu for cpu in usable if rows[cpu]["max_mhz"] == maximum}
        e = usable-p
        source = "lscpu MAXMHZ tiers"
    one_per_core = {}
    for cpu in sorted(p & usable):
        one_per_core.setdefault(rows[cpu]["core"], cpu)
    representatives = sorted(one_per_core.values())
    if len(representatives) < 2:
        raise RuntimeError("need at least two available performance cores")
    return raw, {"source": source, "sysfs_cpu_lists": sysfs, "online_cpus": rows, "allowed_cpus": sorted(usable),
                 "p_cpu_ids": sorted(p & usable), "e_cpu_ids": sorted(e & usable),
                 "reserved_p_cpu": representatives[0], "multi_cpus": representatives[1:],
                 "single_cpu": representatives[1]}


def frequency(cpus):
    values = {}
    for cpu in cpus:
        p = Path(f"/sys/devices/system/cpu/cpu{cpu}/cpufreq/scaling_cur_freq")
        try:
            values[str(cpu)] = int(p.read_text())
        except (OSError, ValueError):
            values[str(cpu)] = None
    return {"at": prior.now(), "frequency_khz": values, "temperature_c": prior.temperature()}


def environment(cpus):
    return {**prior.environment(cpus), **frequency(cpus)}


def measure(variant, tu, cpus, work, logs, objects, timeout):
    """Measure the integrated cc1 compile with microsecond wait4 accounting."""
    stem = tu["id"]
    obj = work/(stem+".o")
    dest = objects/obj.name
    stdout, stderr = (logs/(stem+suffix) for suffix in (".stdout", ".stderr"))
    argv = [BENCH.TASKSET, "--cpu-list", str(cpus[0]), *BENCH.argv_for(variant, tu, obj)]
    start = time.perf_counter_ns()
    with stdout.open("xb") as out, stderr.open("xb") as err:
        p = subprocess.Popen(argv, cwd=work, env={**os.environ, "LC_ALL":"C",
                             "LD_LIBRARY_PATH":"", "LD_PRELOAD":""}, stdout=out, stderr=err)
        _, status, usage = os.wait4(p.pid, 0)
        p.returncode = os.waitstatus_to_exitcode(status)
    elapsed = (time.perf_counter_ns()-start)/1_000_000_000
    user, system = (round(x*1_000_000) for x in (usage.ru_utime, usage.ru_stime))
    cpu = user+system
    success = p.returncode == 0 and obj.is_file() and obj.stat().st_size > 0 and cpu > 0
    row = {"tu": stem, "package": tu["package"], "language": tu["language"],
           "command": argv, "stdout": str(stdout), "stderr": str(stderr), "rc": p.returncode,
           "user_usec": user, "sys_usec": system, "cpu_usec": cpu, "status": "PASS" if success else "FAIL",
           "cpu_seconds": cpu/1_000_000, "wall_seconds": elapsed, "max_rss_bytes": usage.ru_maxrss*1024}
    if obj.is_file():
        obj.rename(dest)
        if success:
            row["object"] = {"path": str(dest), "bytes": dest.stat().st_size, "sha256": BENCH.digest(dest)}
    return row


def batch_with_environment(compiler, rows, cpus, work, out):
    stop = Event()
    samples = []

    def collect():
        while not stop.is_set():
            samples.append(frequency(cpus))
            stop.wait(3)

    thread = Thread(target=collect, name="clock-sampler")
    thread.start()
    try:
        result = prior.batch(compiler, rows, cpus, work, out)
    finally:
        stop.set()
        thread.join()
    result["clock_samples"] = samples
    return result


def order_top30(inputs):
    workloads = defaultdict(list)
    for row in rounds_in(OLD):
        for sample in row["variants"]["V0"]["measurements"]:
            workloads[sample["tu"]].append(stored_time(sample, "167"))
    ranking = sorted(inputs, key=lambda t: (-statistics.median(workloads[t["id"]]), t["id"]))
    return [{**t, "v0_task167_cpu_median_seconds": statistics.median(workloads[t["id"]])/200}
            for t in ranking[:30]]


def run_mode(mode, inputs, count, cpus, all_cpus, variants, alias, work):
    mode_dir = OUT/mode
    mode_dir.mkdir()
    for index in range(count+1):
        phase = f"round-{index:02}" if index else "warmup"
        order = prior.bench.rotation(prior.NAMES, max(index-1, 0))
        row = {"round": index, "order": order, "environment_start": environment(all_cpus), "variants": {}}
        for name in order:
            print(f"BEGIN {prior.now()} {mode} {phase} {name}", flush=True)
            compiler = BENCH.use_variant(variants[name], alias)
            data = batch_with_environment(compiler, inputs, cpus, work, mode_dir/phase/name)
            row["variants"][name] = data
            if {r["cpu"] for r in data["measurements"]} != set(cpus):
                raise RuntimeError(f"{mode} did not use every selected core")
            print(f"END {prior.now()} {mode} {phase} {name} cpu={data['tu_cpu_seconds_sum']:.3f} "
                  f"wall={data['elapsed_seconds']:.3f} ok={data['all_passed']}", flush=True)
        if index:
            for name in order:
                initial = row["variants"][name]
                if any(sample["anomalous"] for sample in initial["measurements"]):
                    compiler = BENCH.use_variant(variants[name], alias)
                    repeated = BENCH.repeat_batch(initial, compiler, inputs, [cpus[0]], work, mode_dir/phase/name, 0)
                    initial.update(anomaly_retries=repeated["anomaly_retries"],
                                   retry_elapsed_seconds=repeated["retry_elapsed_seconds"])
        row["comparisons"] = prior.compare_round(row["variants"], inputs)
        row["environment_end"] = environment(all_cpus)
        row["group"] = ("interference" if row["environment_start"]["build_process_names"] or
                        row["environment_end"]["build_process_names"] else "quiet")
        prior.record(mode_dir/(phase+".json"), row)
        print(f"RECORDED {prior.now()} {mode} {phase} {row['group']} "
              f"objects={dict(Counter(x['status'] for x in row['comparisons']))}", flush=True)
    prior.record(mode_dir/"complete.json", {"ended_at": prior.now(), "formal_rounds": count})


def main():
    # A must be archived locally before the retest starts.
    if not (A/"A-paired.json").is_file():
        raise RuntimeError("task 167 pair analysis is missing")
    inputs = read(OLD/"manifest.json")["inputs"]
    variants = read(prior.CHECKED/"variants.json")
    if variants != read(prior.DOC166) or variants != read(OLD/"manifest.json")["variants"] or len(inputs) != 177:
        raise RuntimeError("historical identities disagree")
    for path, digest in [(Path(t["path"]), t["sha256"]) for t in inputs] + [
            (Path(v[key]), v[field]) for v in variants.values()
            for key, field in (("clang","sha256"),("loader","loader_sha256"))]:
        if BENCH.digest(path) != digest:
            raise RuntimeError(f"input SHA256 changed: {path}")
    alias = prior.CHECKED/"fixed/root"
    original_root = alias.resolve(strict=True)
    raw, topology = find_cores()
    all_cpus = topology["allowed_cpus"]
    before = environment(all_cpus)
    OUT.mkdir()
    work = OUT/"work"
    work.mkdir()
    (OUT/"cpu-topology.csv").write_text(raw)
    top30 = order_top30(inputs)
    prior.record(OUT/"manifest.json", {"started_at": prior.now(), "topology": topology, "initial_environment": before,
                 "variants": variants, "inputs": inputs, "single_inputs": top30, "fixed_root": str(alias),
                 "fixed_work": str(work), "multi_rounds": 10, "single_rounds": 5})
    print(f"START {prior.now()} multi={topology['multi_cpus']} single={topology['single_cpu']} "
          f"governors={dict(Counter(before['governors'].values()))}", flush=True)
    os.sched_setaffinity(0, {topology["reserved_p_cpu"]})
    BENCH.measure = measure
    try:
        run_mode("multi", inputs, 10, topology["multi_cpus"], all_cpus, variants, alias, work)
        run_mode("single", top30, 5, [topology["single_cpu"]], all_cpus, variants, alias, work)
    finally:
        original = next(v for v in variants.values() if Path(v["root"]).resolve() == original_root)
        BENCH.use_variant(original, alias)
    prior.record(OUT/"complete.json", {"ended_at": prior.now()})
    print("COMPLETE", prior.now(), flush=True)


if __name__ == "__main__":
    main()
