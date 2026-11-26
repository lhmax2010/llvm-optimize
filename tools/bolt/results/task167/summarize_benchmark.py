"""Summarize and archive the task 167 benchmark without altering the samples."""
from base64 import b64encode
from collections import Counter
import gzip
import json
import math
from pathlib import Path
import random
import shutil
import statistics
import sys

from run_benchmark import A, B, NAMES, OUT, W, bench, read, record

sys.path.insert(0, str(W / "archive/task161"))
from coordination import publication
from review_packet import commit_push

E = B / "tools/bolt/results/task167"
DOC = B / "docs/bolt/167_benchmark.md"
DRAWS = 20_000
SEED = 167


def statistics_for(samples):
    counts = {len(values) for values in samples.values()}
    if len(counts) != 1 or not counts or not next(iter(counts)):
        return {}
    count = len(samples["V0"])
    randomizer = random.Random(SEED)
    simulated = {name: [] for name in NAMES}
    for _ in range(DRAWS):
        indices = randomizer.choices(range(count), k=count)
        base = statistics.median(samples["V0"][i] for i in indices)
        for name in NAMES:
            value = statistics.median(samples[name][i] for i in indices)
            if value > 0:
                simulated[name].append(base / value)
    base = statistics.median(samples["V0"])
    ratios = {}
    for name in NAMES:
        timings = bench.quartiles(samples[name])
        values = sorted(simulated[name])
        if not values or not timings["median"]:
            raise ValueError("zero timing prevents a paired bootstrap calculation")
        quant = lambda p: values[math.floor(p*(len(values)-1))]
        ratios[name] = {"total": timings, "ratio": base / timings["median"],
                        "95pct_interval": [quant(0.025), quant(0.975)]}
    return ratios


def included(row, ids):
    by_variant = {}
    for name, data in row["variants"].items():
        samples = [r for r in data["measurements"] if r["tu"] in ids]
        if len(samples) != len(ids) or any(r["status"] != "PASS" for r in samples):
            return None
        by_variant[name] = samples
    return by_variant


def scores(rounds, ids, *, wall=False):
    values = {name: [] for name in NAMES}
    for row in rounds:
        samples = included(row, ids)
        if samples is None:
            continue
        for name, measurements in samples.items():
            value = row["variants"][name]["elapsed_seconds"] if wall else sum(
                item["cpu_seconds"] for item in measurements)
            values[name].append(value)
    return statistics_for(values)


def retry_checked(rounds, ids):
    adjusted = {name: [] for name in NAMES}
    for row in rounds:
        chosen = {}
        for name, data in row["variants"].items():
            retries = {x["initial"]["tu"]: x["retry"] for x in data["anomaly_retries"]}
            selected = [retries.get(r["tu"], r) for r in data["measurements"]]
            if len(selected) != len(ids) or any(r["status"] != "PASS" or r["anomalous"] for r in selected):
                break
            chosen[name] = sum(r["cpu_seconds"] for r in selected)
        else:
            for name, value in chosen.items():
                adjusted[name].append(value)
    return statistics_for(adjusted)


def collect_summary(manifest, warmup, rows):
    inputs = manifest["inputs"]
    ids = {x["id"] for x in inputs}
    cpus = set(manifest["cpus"])
    seen = []
    for r in [warmup, *rows]:
        assert list(r["variants"]) == r["order"] and len(r["variants"]) == 4
        assert len(r["comparisons"]) == len(ids)*6
        for name in NAMES:
            data = r["variants"][name]
            assert {x["tu"] for x in data["measurements"]} == ids
            assert len(data["measurements"]) == len(ids)
            actual = {int(x["command"][7]) for x in data["measurements"]}
            assert actual == cpus, (r["round"], name, actual)
            assert all(x["cpu"] == int(x["command"][7]) for x in data["measurements"])
            seen.append({"round": r["round"], "variant": name, "pinned_cpus": sorted(actual)})
    output = {"paired_rounds": len(rows), "bootstrap_draws": DRAWS, "bootstrap_seed": SEED,
              "pin_checks": seen, "score_cpu": scores(rows, ids), "score_wall": scores(rows, ids, wall=True),
              "retry_sensitivity_cpu": retry_checked(rows, ids), "groups": {},
              "interference_groups": {}, "samples": {}, "objects": {}, "differences": [], "failed": []}
    for key, values in (("size_band", ("small", "medium", "large")), ("language", ("c", "c++"))):
        for group in values:
            picked = [tu["id"] for tu in inputs if tu[key] == group]
            output["groups"][group] = {"count": len(picked), "score": scores(rows, set(picked)),
                                        **({"tu_ids": picked} if group == "large" else {})}
    for group in ("quiet", "interference"):
        subset = [r for r in rows if r["group"] == group]
        output["interference_groups"][group] = {"rounds": [r["round"] for r in subset],
                                               "cpu": scores(subset, ids),
                                               "wall": scores(subset, ids, wall=True)}
    output["all_pair_checks"] = dict(Counter(
        c["status"] for r in rows for c in r["comparisons"]))
    output["warmup_pair_checks"] = dict(Counter(c["status"] for c in warmup["comparisons"]))
    for name in NAMES:
        batches = [r["variants"][name] for r in rows]
        attempts = [x for batch in batches for x in batch["measurements"]]
        retries = [x for batch in batches for x in batch["anomaly_retries"]]
        output["samples"][name] = {
            "formal_compiles": len(attempts), "retry_count": len(retries),
            "still_anomalous": sum(x["retry"]["anomalous"] for x in retries),
            "retry_object_checks": dict(Counter(x["objects"]["status"] for x in retries)),
            "max_rss_bytes": max(x.get("max_rss_bytes", 0) for x in attempts+[r["retry"] for r in retries]),
        }
        refs = [x for row in rows for x in row["comparisons"] if name in (x["left"], x["right"])]
        bad = {x["tu"] for x in refs if x["status"] != "IDENTICAL"}
        output["objects"][name] = {"identical_tus": len(ids-bad), "total_tus": len(ids),
                                   "pair_status": dict(Counter(x["status"] for x in refs))}
    for row in [warmup, *rows]:
        for comp in row["comparisons"]:
            if comp["status"] != "IDENTICAL":
                output["differences"].append({"round": row["round"], **comp})
        for name, batch in row["variants"].items():
            for item in batch["measurements"]:
                if item["status"] != "PASS":
                    output["failed"].append({"round": row["round"], "variant": name, **item})
            for retry in batch["anomaly_retries"]:
                if retry["objects"]["status"] != "IDENTICAL":
                    output["differences"].append({"round": row["round"], "tu": retry["initial"]["tu"],
                                                 "left": name, "right": name+" (retry)", **retry["objects"]})
                if retry["retry"]["status"] != "PASS":
                    output["failed"].append({"round": row["round"], "variant": name,
                                             "retry": True, **retry["retry"]})
    return output


def ratio_text(score):
    lower, upper = score["95pct_interval"]
    return f"{score['ratio']:.4f}× [{lower:.4f}, {upper:.4f}]"


def result_table(report):
    lines = ["| 变体 | CPU 中位数 / IQR (s) | 墙钟中位数 / IQR (s) | 相对 V0 CPU 加速比 [95% CI] | 原始 .o 一致 |",
             "|---|---:|---:|---:|---:|"]
    for name in NAMES:
        cpu = report["score_cpu"].get(name)
        wall = report["score_wall"].get(name)
        fmt = lambda row: f"{row['total']['median']:.2f} / {row['total']['iqr']:.2f}" if row else "—"
        obj = report["objects"][name]
        object_text = f"{obj['identical_tus']}/{obj['total_tus']}"
        if obj['identical_tus'] != obj['total_tus']:
            object_text = "🔴 " + object_text
        lines.append(f"| {name} | {fmt(cpu)} | {fmt(wall)} | {ratio_text(cpu) if cpu else '—'} | {object_text} |")
    return lines


def report_text(report, manifest, warmup, rows, end):
    links = "../../tools/bolt/results/task167/"
    result = ["# 167 · 四变体正式编译速度基准", "", *result_table(report), "",
              "CPU 时间为主指标。每轮对同一变体的 177 个 TU 汇总 user + sys 时间，"
              "墙钟为同一次并行批次从提交任务到收集全部产物的时间。预热和复跑时间另存。"
              "主表使用五轮原始完成样本，含采样期间出现干扰的轮次。"
              "加速比为 V0 与相应变体的轮次总量中位数之比，置信区间为整轮配对重采样"
              f" {DRAWS:,} 次得到的 95% 百分位区间。IQR 使用 inclusive 四分位，"
              "五轮的区间应结合原始轮次波动解读。", "",
              f"运行时段 {manifest['started_at']} 至 {end['ended_at']}。"
              "20 个物理核，每核一个可用逻辑 CPU。18 个 worker 分别固定到 CPU 2–19，"
              "CPU 0–1 留出。每个变体一轮预热、五轮正式，正式执行顺序逐轮循环左移。"
              "clang、loader 的 SHA256 均与 166-C 收据一致，固定启动路径沿用 166-C。"
              "177 个 TU 来自 9 个包，87 个 C、90 个 C++，每个输入的源身份及 SHA256 均与训练集无交集。", "",
              "V0 为 149-run N2 关闭优化的成品，V1 为 QB 1232863 的仅 BOLT 成品，"
              "V2 为 QB 1240309 的仅 PGO 成品，V3 为本地 G7 的 PGO+BOLT 产物。"
              "本轮的 V3 来自 G7 重写流程，测试结论适用于这些具体二进制。", "",
              f"[原始逐 TU 数据、环境、命令与脚本]({links}) · [输入与变体身份]({links}manifest.json)", "",
              "## 墙钟加速比", "",
              "| 变体 | 相对 V0 墙钟加速比 [95% CI] |", "|---|---:|"]
    for name in NAMES:
        if name in report["score_wall"]:
            result.append(f"| {name} | {ratio_text(report['score_wall'][name])} |")
    result += ["", "## 按 TU 大小和语言", "",
              "| 分组 | TU 数 | V0 | V1 | V2 | V3 |", "|---|---:|---:|---:|---:|---:|"]
    labels = {"small":"小", "medium":"中", "large":"大", "c":"C", "c++":"C++"}
    for key, group in report["groups"].items():
        result.append(f"| {labels[key]} | {group['count']} | "+
                      " | ".join(ratio_text(group["score"][n]) if n in group["score"] else "—" for n in NAMES)+" |")
    result += ["", "大 TU 只有 5 个，名单为 " + "、".join(f"`{name}`" for name in report["groups"]["large"]["tu_ids"]) + "。"
               "各分组先在每轮汇总组内 CPU 时间，再按主表方法计算加速比和区间。", "",
               "## 资源、复跑与正确性", "",
               "| 变体 | 最大 RSS (MiB) | 正式编译 | 异常复跑 | 复跑仍异常 |",
               "|---|---:|---:|---:|---:|"]
    for name, sample in report["samples"].items():
        result.append(f"| {name} | {sample['max_rss_bytes']/1024**2:.2f} | {sample['formal_compiles']} | "
                      f"{sample['retry_count']} | {sample['still_anomalous']} |")
    result.extend(["", "最大 RSS 取正式批次中的单次编译峰值，含复跑。"
                   "沿用 158 的异常规则，单个 TU 墙钟超过 CPU 时间的 1.5 倍且多于 1 秒，"
                   "在本轮末尾复跑一次。原始和复跑数据全部保留。"
                   f" [复跑敏感性与原始比较计数]({links}summary.json)", "",
                   "正式对象比较计数 " + "，".join(f"{k} {v:,}" for k,v in report['all_pair_checks'].items()) + "。"
                   "预热对象比较计数 " + "，".join(f"{k} {v:,}" for k,v in report['warmup_pair_checks'].items()) + "。"
                   "主表按 TU 统计，每个变体与其余三个变体在全部正式轮次逐字节核对。", ""])
    if report["differences"]:
        result += ["| 轮次 | TU | 变体 | 结果 | 去掉 .GCC.command.line |", "|---|---|---|---|---|"]
        for row in report["differences"]:
            mark = "🔴 " if row["status"] == "DIFFERENT" else ""
            result.append(f"| {row['round']} | {row['tu']} | {row['left']} / {row['right']} | {mark}{row['status']} | "
                          f"{row.get('without_command_line', '—')} |")
        result.append("")
    if report["failed"]:
        result += ["| 轮次 | 变体 | TU | 退出码 |", "|---|---|---|---:|"]
        for row in report["failed"]:
            result.append(f"| {row['round']} | {row['variant']} | {row['tu']} | {row['rc']} |")
        result.append("")
    result += ["## 轮次环境", "",
               "每轮起止采样 loadavg、CPU 频率调节器、可读温度和构建进程名。"
               "构建进程采样只看名称，无法据此确定归属。", "",
               "| 轮次 | 顺序 | loadavg 1m 起 → 止 | CPU 温度 °C 起 → 止 | 调节器 | 构建进程名 |",
               "|---|---|---|---|---|---|"]
    cpu_temp = lambda e: next((v for k,v in e['temperature_c'].items() if k.endswith(':x86_pkg_temp')), '—')
    for row in [warmup, *rows]:
        low, high = row["environment_start"], row["environment_end"]
        names = sorted(set(low["build_process_names"]) | set(high["build_process_names"]))
        gov = sorted({g for env in (low, high) for g in env["governors"].values() if g})
        result.append(f"| {row['round'] or '预热'} | {' → '.join(row['order'])} | {low['loadavg'][0]:.2f} → "
                      f"{high['loadavg'][0]:.2f} | {cpu_temp(low)} → {cpu_temp(high)} | "
                      f"{', '.join(gov) or '不可读'} | {', '.join(names) or '未观察到'} |")
    result += ["", "| 环境 | 正式轮次 | 变体 | CPU 中位数 (s) | 墙钟中位数 (s) |",
               "|---|---|---|---:|---:|"]
    for group, values in report["interference_groups"].items():
        label = {"quiet":"安静", "interference":"有干扰"}[group]
        rounds = ", ".join(map(str, values["rounds"])) or "—"
        for name in NAMES:
            if name in values["cpu"]:
                result.append(f"| {label} | {rounds} | {name} | {values['cpu'][name]['total']['median']:.2f} | "
                              f"{values['wall'][name]['total']['median']:.2f} |")
        if not values["cpu"]:
            result.append(f"| {label} | {rounds} | — | — | — |")
    return "\n".join(result) + "\n"


def pack_compiler_logs(phases):
    target = A / "compiler-logs.jsonl.gz"
    with gzip.open(target, "wt", encoding="utf-8") as archive:
        for phase in phases:
            for path in sorted(phase.glob("*/**/*")):
                if path.suffix in (".time", ".stdout", ".stderr") and path.is_file() and path.stat().st_size:
                    entry = {"path": str(path.relative_to(OUT)),
                             "base64": b64encode(path.read_bytes()).decode("ascii")}
                    archive.write(json.dumps(entry) + "\n")
    return target


def main():
    manifest, end = read(OUT/"manifest.json"), read(OUT/"complete.json")
    warmup = read(OUT/"warmup.json")
    phases = [OUT / f"round-{i:02}.json" for i in range(1, 6)]
    rows = [read(path) for path in phases]
    summary = collect_summary(manifest, warmup, rows)
    output = [*phases, OUT/"manifest.json", OUT/"complete.json", OUT/"warmup.json", OUT/"cpu-topology.csv",
              A/"run_benchmark.py", Path(__file__).resolve(), A/"run-journal.txt", A/"service-resources.txt",
              A/"harness-sha256.txt", pack_compiler_logs([OUT/"warmup", *(path.with_suffix("") for path in phases)])]
    body = report_text(summary, manifest, warmup, rows, end)
    record(A/"summary.json", summary)
    (A/"report.md").write_text(body)
    with publication():
        E.mkdir(exist_ok=True)
        for path in [*output, A/"summary.json"]:
            if path.stat().st_size > 10_000_000:
                raise RuntimeError(f"evidence file exceeds 10 MB: {path}")
            shutil.copy2(path, E / path.name)
        DOC.write_text(body)
        sha = commit_push("docs: record the four-variant compiler benchmark", DOC, E)
    (A/"published.sha").write_text(sha+"\n")
    print(sha, flush=True)


if __name__ == "__main__":
    main()
