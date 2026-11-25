from collections import Counter
from pathlib import Path
import json, shutil, subprocess, tarfile

A=Path(__file__).resolve().parent
W=A.parents[1]
B=W.with_name(W.name+"-bolt")
E=A/"evidence"

def read(p):
    return json.loads(p.read_text())

def render():
    v=read(E/"variants.json")
    counts=read(E/"corpus-summary.json")
    audit=read(E/"input-eligibility.json")
    result=read(A/"pilot/results.json")
    one=result["rounds"][0]
    summary=result["summary"]
    diff=summary["V1"]["object_comparisons"]
    passed={name:sum(r["status"]=="PASS" for r in data["measurements"])
            for name,data in one["variants"].items()}
    reserve=sum(len(r["memory_interruptions"]) for data in one["variants"].values() for r in data["measurements"])
    measurements={name:{"completed":len(data["measurements"]),"pass":passed[name],
                   "max_rss_bytes":max(r.get("max_rss_bytes",0) for r in data["measurements"])}
                  for name,data in one["variants"].items()}
    text=["# 156 · 编译速度基准工具与试跑","",
          f"**试跑，非正式数据。** 同一核上完成 V0/V1 各 20 次编译，"
          f"成功 {passed['V0']}/20、{passed['V1']}/20。"
          f"逐字节比较 {diff.get('IDENTICAL',0)} 组相同、{diff.get('DIFFERENT',0)} 组不同、"
          f"{diff.get('UNVERIFIED',0)} 组未核对。151 的 G 链与试跑并行。","",
          "## 变体与私有运行环境","",
          "| 变体 | RPM | 私有 clang SHA256 | 版本 / 最小编译 | BOLT 节 |",
          "|---|---|---|---|---|"]
    for name in ("V0","V1"):
        x=v[name]
        text.append(f"| {name} | `{Path(x['source_rpm']['path']).name}` | `{x['sha256']}` | "
                    f"{x['version']['rc']} / {x['compile']['rc']} | "
                    f"{', '.join(x['bolt_sections']) or '无'} |")
    text.extend(["| V2 | 待仅 PGO 成品 | — | PENDING | — |",
                 "| V3 | 待 PGO+BOLT 成品 | — | PENDING | — |",""])
    for name in ("V0","V1"):
        x=v[name]
        text += [f"- {name} RPM `{x['source_rpm']['path']}`，SHA256 `{x['source_rpm']['sha256']}`。",
                 f"- {name} 私有 clang `{x['clang']}`，{x['clang_bytes']:,} B。"]
    text += ["","V0 使用留存的 149-run N2，无需回退到旧基线。它来自 PS5 并关闭 llvm_speedup。"
             "V1 采用同为 Toolchain 的 QB 1232863 x86_64。128 的回执登记的是 H4，其与 PS5 只差打包助手。"
             "QB 1232862 Base-Dev RPM 的身份也已核对。它不参与这轮。V1 的 PGO 关闭，混合链接和 BOLT 开启。",
             "",
             "两个私有根由同一个冻结 Tizen 快照的 glibc、libstdc++、libgcc、zlib RPM 提供运行库。"
             "加载器 --list 的各个真实文件都在对应根内。方法 A 使用显式加载器、--library-path 和 -fintegrated-cc1。"
             "同时禁用 clang 默认配置文件，由每个 TU 的清单传入目标与标志。",
             "[变体路径、哈希与烟测原文](../../tools/bolt/results/task156/variants.json) · "
             "[来源差异](../../tools/bolt/results/task156/variant-provenance.json)","",
             "## 留出语料","",
             f"共 {counts['inputs']} 个 x86_64 TU。zlib 为 20 个 C，LLVM 为 10 个 C++。"
             f"原始大小 {counts['size_min']:,}–{counts['size_max']:,} B。"
             f"小于 256 KiB {counts['size_bands'].get('small',0)} 个，256 KiB 至小于 8 MiB "
             f"{counts['size_bands'].get('medium',0)} 个，8 MiB 及以上 {counts['size_bands'].get('large',0)} 个。"
             "试跑取按字节大小分布选出的 10 个 C，另取全部 10 个 C++。",
             "",
             "server-kit、133-N 和 138-D 指向的 23 项训练记录按任务名、目标、字节、SHA256 核对一致。"
             "同时排除之前训练集中的相同源文件身份和不同预处理目标。"
             "C 使用已归档的 zlib O2 输入与命令，C++ 使用旧 holdout 收据和恢复的预处理文件。"
             "保留适用的 Tizen 编译标志，统一 -O2，并清除已用于预处理的目录路径及旧输出参数。",
             "",
             f"工作区受限扫描列出 {audit['discovered_candidates']} 个候选路径。"
             f"分类计数为 {json.dumps(audit['reasons'],ensure_ascii=False)}。"
             "同一 TU 的重复副本和其他架构预处理产物不增加独立样本数。"
             "无可验证包名、目标及编译参数的内容未纳入。因此可确认的语料未达到约 200 个、8 个包或完整语料 C/C++ 各半。",
             "",
             "[语料清单及标志](../../tools/bolt/results/task156/corpus.json) · "
             "[训练排除身份](../../tools/bolt/results/task156/training-overlap-policy.json) · "
             "[候选归类](../../tools/bolt/results/task156/input-eligibility.json)",
             "",
             "## 工具和试跑","",
             "正式默认 5 轮，轮换变体顺序。单线程按清单顺序编译，所有变体使用相同 taskset 掩码。"
             "-j N 提供最多四核的聚合模式。记录每 TU 墙钟、user + sys、峰值 RSS，并逐字节比较对象。"
             "8/8 单测通过，含轮换、并行、低内存等待、对象差异标红和统计。"
             f"本轮一个核，受控子单元 CPUQuota=100%、MemoryMax=2 GiB、swap0、Nice19、IO idle，"
             f"因低内存中断后重做的样本 {reserve}。"
             "MemAvailable 低于 6 GiB 时等待。若编译已启动，只停止本任务该子进程组并重新测量，保留中断日志。",
             "",
             "按进程名记录构建进程，另记 CPU 调节器与 loadavg。共享名称无法区分项目，"
             "另一项目是否构建记 UNKNOWN。单轮 IQR 为 0 只是定义值，试跑倍率不用于正式结论。",
             ""]
    text += (A/"pilot/results.md").read_text().splitlines()[4:]
    diagnostic=read(E/"pilot-object-attribution.json")
    first=one["variants"]["V1"]["measurements"][0]
    text += ["",f"只读诊断确认 {diagnostic['loader_path_only']}/{diagnostic['raw_different']} 组的唯一差异是 "
                 ".GCC.command.line 内记录的私有加载器路径。将该节里的 V0 路径替换为等长的 V1 路径后，"
                 "全文件其余字节一致。保留原始 DIFFERENT 标记与对象，诊断没有写回 .o。",
                 f"V1 首个样本墙钟 {first['wall_seconds']:.3f} s，user + sys {first['cpu_seconds']:.2f} s。"
                 "单轮的整体倍率受该样本影响。",
                 "[逐文件只读归因](../../tools/bolt/results/task156/pilot-object-attribution.json)"]
    text += ["","[JSON 原始测量与对象哈希](../../tools/bolt/results/task156/pilot-results.json) · "
                 "[试跑 Markdown](../../tools/bolt/results/task156/pilot-results.md) · "
                 "[试跑配置](../../tools/bolt/results/task156/pilot-config.json) · "
                 "[单测原文](../../tools/bolt/results/task156/tests.txt) · "
                 "[工具说明](../../tools/bolt/bench/README.md)",""]
    (A/"156_benchmark_harness.md").write_text("\n".join(text))
    (E/"pilot-summary.json").write_text(json.dumps({"observations":measurements,"ratios":summary,
       "memory_interrupted_samples":reserve,"correctness":diff},indent=2)+"\n")
    shutil.copyfile(A/"pilot/results.json",E/"pilot-results.json")
    shutil.copyfile(A/"pilot/results.md",E/"pilot-results.md")
    with tarfile.open(E/"pilot-compiler-logs.tar.gz","w:gz") as out:
        for p in sorted((A/"pilot/round-01").glob("*/logs/*")):
            if p.is_file():
                out.add(p,arcname=str(p.relative_to(A/"pilot")),recursive=False)
    for n in ("corpus.txt","corpus-retry.txt","discovery.txt","variants.txt","pilot.txt"):
        shutil.copyfile(A/n,E/n)
    print(passed,diff)

if __name__=="__main__":
    render()
