"""Render paired and aggregate compiler benchmark evidence and publish it."""
from base64 import b64encode
from collections import Counter
import gzip
import json
from pathlib import Path
import shutil
import statistics
import subprocess
import sys
import time

from paired import A, B, W, GROUPS, PAIRS, analyze, read, rounds_in, row_text, save

OUT = A/"run"
LAYOUT = B/"tools/bolt/results/task168"
DOC = B/"docs/bolt/168_benchmark_controlled.md"
NAMES = ("V0","V1","V2","V3")
LABELS = {"all":"全部","small":"小","medium":"中","large":"大","c":"C","c++":"C++"}

sys.path[:0] = [str(W/"archive/task167"),str(W/"archive/task161")]
from summarize_benchmark import statistics_for
from coordination import publication
from review_packet import commit_push


def checked_rounds(mode, count, cpus, inputs):
    directory = OUT/mode
    rounds = rounds_in(directory)
    warmup = read(directory/"warmup.json")
    ids = {i["id"] for i in inputs}
    assert [r["round"] for r in rounds] == list(range(1,count+1))
    for row in [warmup, *rounds]:
        assert list(row["variants"]) == row["order"]
        assert len(row["comparisons"]) == 6*len(ids)
        for variant in row["variants"].values():
            passes = variant["measurements"]
            assert len(passes) == len(ids) and {x["tu"] for x in passes} == ids
            assert {x["cpu"] for x in passes} == set(cpus)
            for x in passes:
                assert int(x["command"][2]) == x["cpu"]
    return warmup, rounds


def summarize_mode(warmup, rows):
    result = {"formal_pairs": dict(Counter(c["status"] for r in rows for c in r["comparisons"])),
              "warmup_pairs": dict(Counter(c["status"] for c in warmup["comparisons"])),
              "differences": [], "failures": [], "max_rss": {}, "retries": {}, "clocks": {}}
    matched = [r for r in rows if all(r["variants"][n]["all_passed"] for n in NAMES)]
    result["aggregate_rounds"] = [r["round"] for r in matched]
    for metric, key in (("cpu","tu_cpu_seconds_sum"),("wall","elapsed_seconds")):
        result[metric] = statistics_for({n: [r["variants"][n][key] for r in matched] for n in NAMES})
    for n in NAMES:
        batch = [r["variants"][n] for r in rows]
        retries = [x for r in batch for x in r["anomaly_retries"]]
        result["retries"][n] = len(retries)
        rss = [x["max_rss_bytes"] for r in batch for x in r["measurements"]] + [
               x["retry"]["max_rss_bytes"] for x in retries]
        result["max_rss"][n] = max(rss)
        samples = [s for r in batch for s in r["clock_samples"]]
        freq = [v/1000 for s in samples for v in s["frequency_khz"].values() if v is not None]
        temp = [v for s in samples for k,v in s["temperature_c"].items() if k.endswith(":x86_pkg_temp")]
        result["clocks"][n] = {
            "frequency_mhz_min_median_max": [min(freq), statistics.median(freq), max(freq)] if freq else None,
            "pkg_temp_c_min_median_max": [min(temp), statistics.median(temp), max(temp)] if temp else None,
            "samples": len(samples)}
    for r in [warmup,*rows]:
        for item in r["comparisons"]:
            if item["status"] != "IDENTICAL":
                result["differences"].append({"round":r["round"],**item})
        for n,batch in r["variants"].items():
            for sample in batch["measurements"]:
                if sample["status"] != "PASS":
                    result["failures"].append({"round":r["round"],"variant":n,**sample})
            for item in batch["anomaly_retries"]:
                if item["retry"]["status"] != "PASS":
                    result["failures"].append({"round":r["round"],"variant":n,"retry":True,**item["retry"]})
                if item["objects"]["status"] != "IDENTICAL":
                    result["differences"].append({"round":r["round"],"tu":item["initial"]["tu"],
                        "left":n,"right":n+" (retry)",**item["objects"]})
    result["rounds_with_build_processes"] = [r["round"] for r in rows if r["group"]!="quiet"]
    return result


def pair_table(paired, *, old=False, overall=False):
    head = "| CPU 时间比 | 分组 | TU（可用/总数） | 比值 [95% CI] | Wilcoxon p |"
    fmt = "|---|---|---:|---:|---:|"
    if old:
        head += " 5 轮均可直接计算 | 0.005s 填补敏感性 [95% CI] | 填补后 p |"
        fmt += "---:|---:|---:|"
    table = [head, fmt]
    for pair, item in paired["pairs"].items():
        for group, stat in item["groups"].items():
            if overall and group != "all":
                continue
            ratio, p = row_text(stat)
            line = f"| {pair} | {LABELS[group]} | {stat['tus']}/{stat['available_tus']} | {ratio} | {p} |"
            if old:
                sensitivity, p_alt = row_text(stat["zero_bin_midpoint"])
                line += f" {stat['all_rounds_positive']} | {sensitivity} | {p_alt} |"
            table.append(line)
    return table


def ms_text(row):
    return "—" if row is None else f"{row['total']['median']:.3f} / {row['total']['iqr']:.3f}"


def speed_text(row):
    if row is None:
        return "—"
    low, high = row["95pct_interval"]
    return f"{row['ratio']:.4f}× [{low:.4f}, {high:.4f}]"


def aggregate_table(mode):
    table = ["| 变体 | CPU 中位数 / IQR (s) | 墙钟中位数 / IQR (s) | CPU 加速比 vs V0 [95% CI] | 墙钟加速比 vs V0 [95% CI] | 最大 RSS (MiB) |",
             "|---|---:|---:|---:|---:|---:|"]
    for name in NAMES:
        c,w = mode["cpu"].get(name),mode["wall"].get(name)
        table.append(f"| {name} | {ms_text(c)} | {ms_text(w)} | {speed_text(c)} | "
                     f"{speed_text(w)} | {mode['max_rss'][name]/2**20:.2f} |")
    return table


def significance(data):
    for mode, paired in data.items():
        ratio = paired["pairs"]["V3/V1"]["groups"]["all"]
        estimator,p = row_text(ratio)
        if ratio["p"] is None:
            result = "缺少可分析样本"
        elif ratio["p"] >= .05:
            result = "未检出显著差异"
        elif ratio["ratio"] < 1:
            result = "V3 显著降低 CPU 时间"
        else:
            result = "V3 显著增加 CPU 时间"
        yield f"| {mode} | {estimator} | {p} | {result} |"


def render(manifest, historical, decisions, aggregates, paired):
    initial = manifest["initial_environment"]
    topology = manifest["topology"]
    governor_counts = dict(Counter(initial["governors"].values()))
    link = "../../tools/bolt/results/task168/"
    text = ["# 168 · 编译器基准配对复核与受控重测", "",
            "| V3/V1 | CPU 时间比 [95% CI] | Wilcoxon p | 结论（α=0.05） |",
            "|---|---:|---:|---|",
            *significance({"167 复核":historical,"受控多线程":paired["multi"],"受控单线程":paired["single"]}), "",
            "时间比为左侧变体除以右侧，低于 1 表示左侧较快。"
            "每个 TU 先取同轮 CPU 比值的中位数，再赋予所有 TU 相同权重计算几何平均。"
            "95% 区间按 TU 有放回抽样 10,000 次。Wilcoxon 使用 TU 中位比值的对数，"
            "采用双侧符号秩检验，平秩取平均，精确计算条件符号分布，零差排除。"
            "p 值未做多重比较校正，分组为探索性。", "",
            "## A · 现有 167 数据", "",
            "167 用 GNU time 分别以 0.01 s 显示 user 和 sys。0.00 s 记录无法直接取有限正比值。"
            "主分析使用同轮双方均为正值的比值，无正值配对的 TU 保留缺测标记。"
            "敏感性列对每个记录为零的合计时间填入半个显示刻度 0.005 s，从而覆盖所有 TU 的五轮。"
            "填补结果受该假设影响。167 主表按每轮汇总的总 CPU 时间比较，长 TU 权重自然更大。"
            "V3 的总 CPU 中位数为 113.39 s、V1 为 114.74 s，V3/V1 为 0.9882。"
            "TU 等权后 V3/V1 的两种 167 口径均未检出显著差异。"
            "V1、V2、V3 相对 V0 的整体方向与主表一致。"
            f" [167 报告](167_benchmark.md) · [逐 TU 配对和零值计数]({link}A-paired.json)", "",
            *pair_table(historical, old=True), "",
            "## B · 受控重测", "",
            f"内核与 lscpu 一致识别性能核 {topology['p_cpu_ids']}、能效核 {topology['e_cpu_ids']}。"
            f"启动时调节器计数为 {governor_counts}。多线程使用 CPU {topology['multi_cpus']}，"
            f"留出性能核 CPU {topology['reserved_p_cpu']}，单线程固定 CPU {topology['single_cpu']}。"
            "每个 worker 程序级固定在一个独立物理核。两个模式都先预热，正式轮次循环改变变体顺序。"
            "每轮起止采样全体 CPU 的环境，批次执行中每三秒采样所用核的频率和可读温度。"
            "B 使用 wait4 的 user+sys 微秒计时，继续使用同一编译器、加载器、参数和固定启动路径。"
            "主统计使用原始正式量测，异常复跑及对象原文另存。"
            "总体加速比为 V0 与变体各自轮次总量中位数之比，95% 区间按配对轮次重抽样。"
            f" [拓扑、输入与运行环境]({link}manifest.json)", "",
            "单线程的 30 个 TU 按 167 的 V0 五轮 CPU 时间中位数从长到短选取，同分按 TU ID 排序。"
            "名单、时长、源与原始参数保存在清单中；单线程结果只代表该子集。", ""]
    for mode, title in (("multi","多线程 · 177 TU · 10 轮"),("single","单线程 · 30 TU · 5 轮")):
        d = aggregates[mode]
        text += [f"### {title}", "",
                 f"完整总量轮次 {len(d['aggregate_rounds'])}。执行期频率和封装温度为读到的样本，"
                 "包含 worker 完成前后频率变化。", "",
                 *aggregate_table(d), "", *pair_table(paired[mode]), "",
                 "| 变体 | 频率 min / 中位数 / max (MHz) | 封装温度 min / 中位数 / max (°C) | 采样数 |",
                 "|---|---:|---:|---:|"]
        for n, c in d["clocks"].items():
            fmt = lambda x: " / ".join(f"{i:.1f}" for i in x) if x else "不可读"
            text.append(f"| {n} | {fmt(c['frequency_mhz_min_median_max'])} | "
                        f"{fmt(c['pkg_temp_c_min_median_max'])} | {c['samples']} |")
        text += ["", f"正式对象比较 {d['formal_pairs']}，预热比较 {d['warmup_pairs']}。"
                 f"观察到构建进程名的正式轮次 {d['rounds_with_build_processes'] or '无'}。"
                 f"按变体复跑计数 {d['retries']}。"
                 f" [逐 TU 原始数据与各轮频温采样]({link}{mode}/)", ""]
        for item in d["differences"]:
            tag = "🔴 " if item["status"] == "DIFFERENT" else ""
            text.append(f"- {tag}第 {item['round']} 轮 · {item['tu']} · {item['left']} / {item['right']} · "
                        f"{item['status']} · 移除 .GCC.command.line 后 {item.get('without_command_line','—')}。")
        for item in d["failures"]:
            text.append(f"- 第 {item['round']} 轮 · {item['tu']} · {item['variant']} · 编译退出 {item['rc']}。")
        if d["differences"] or d["failures"]:
            text.append("")
    text += [f"运行时段 {manifest['started_at']} 至 {decisions['ended_at']}。"
             f" [汇总数据]({link}aggregate.json) · [单元日志]({link}run-journal.txt)", ""]
    return "\n".join(text)


def save_logs(mode):
    path = A/f"{mode}-compiler-logs.jsonl.gz"
    with gzip.open(path,"wt",encoding="utf-8") as out:
        for entry in sorted((OUT/mode).glob("*/*/*/*")):
            if entry.suffix in (".stdout",".stderr") and entry.is_file() and entry.stat().st_size:
                row = {"path":str(entry.relative_to(OUT)),"base64":b64encode(entry.read_bytes()).decode("ascii")}
                out.write(json.dumps(row)+"\n")
    return path


def finish():
    m = read(OUT/"manifest.json")
    decisions = read(OUT/"complete.json")
    historical = read(A/"A-paired.json")
    aggregates, paired = {}, {}
    for mode in ("multi","single"):
        inputs = m["inputs"] if mode=="multi" else m["single_inputs"]
        cpus = m["topology"]["multi_cpus"] if mode=="multi" else [m["topology"]["single_cpu"]]
        warmup, rows = checked_rounds(mode,m[mode+"_rounds"],cpus,inputs)
        aggregates[mode] = summarize_mode(warmup,rows)
        paired[mode] = analyze(rows,inputs,"168")
        save(A/(mode+"-paired.json"),paired[mode])
    save(A/"aggregate.json",aggregates)
    body = render(m,historical,decisions,aggregates,paired)
    (A/"report.md").write_text(body)
    journal = A/"run-journal.txt"
    with journal.open("w") as out:
        subprocess.run(["/usr/bin/journalctl","--user","-u","llvm-opt-task168-controlled.service",
                        "--no-pager","-o","cat"],stdout=out,check=True)
    artifacts = [(src,Path(src.name)) for src in [
        OUT/"manifest.json",OUT/"cpu-topology.csv",OUT/"complete.json",A/"A-paired.json",
        A/"aggregate.json",A/"paired.py",A/"retest.py",Path(__file__).resolve(),journal]]
    for mode in ("multi","single"):
        artifacts.extend((source,Path(mode)/source.name) for source in [
            *sorted((OUT/mode).glob("*.json")), A/(mode+"-paired.json"), save_logs(mode)])
    with publication():
        for src, dest in artifacts:
            target = LAYOUT/dest
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(src,target)
        DOC.write_text(body)
        rev = commit_push("docs: verify compiler benchmark on performance cores",DOC,LAYOUT)
    (A/"published.sha").write_text(rev+"\n")
    print(rev,flush=True)


def main():
    while not (OUT/"complete.json").is_file():
        unit = subprocess.check_output(["/usr/bin/systemctl","--user","show","llvm-opt-task168-controlled.service",
                                        "-p","ActiveState","--value"],text=True)
        if unit.strip() in {"failed","inactive"}:
            raise RuntimeError("retest ended without a final checkpoint")
        time.sleep(25)
    finish()


if __name__ == "__main__":
    main()
