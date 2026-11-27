"""Publish the requested evidence, restricted to the evidence branch."""
import gzip
from pathlib import Path
import re
import shutil
import sys

from collect import A,W,B,E,BUILD,BRANCH,REV,PROJECT,BASE,ARCHES,read,save,STAMP

sys.path.insert(0,str(W/"archive/task161"))
from coordination import publication
from review_packet import commit_push

DOC=B/"docs/bolt/171_qb_pgo_bolt.md"
DEST=B/"tools/bolt/results/task171"
BENCH=A/"benchmark"
LINK="../../tools/bolt/results/task171/"
Q=chr(96)


def gate_rows(x):
    bodies=[STAMP.sub("",row["text"]) for row in x["gates"]]
    def body(marker):
        return [l for l in bodies if l.startswith(marker)]
    counts=[]
    for r in x["bolt_counts"]:
        if r["counts"] not in counts:
            counts.append(r["counts"])
    summaries={m:body(m) for m in ("PGO_NINJA_CHECK","PGO_MATCH","PGO_RUNTIME_CHECK",
                                  "BOLT_PIPELINE_PASS","BOLT_REAL_GATE_PASS","BOLT_POST_GATE_PASS")}
    return {"markers":summaries,"counts":counts,"threshold":x["observed_threshold_options"],
            "retry":x["archive_member_retry"]}


def cause(error):
    message=error["text"].lower()
    for patt, hint in [
        (r"unrecognized arguments|missing profile mapping","PGO 参数或映射校验失败。"),
        (r"pgo ninja check|profile.use|profile-mismatch","PGO Ninja 或 profile-use 门禁失败。"),
        (r"profile sha|profile identity","BOLT profile 文件身份校验失败。"),
        (r"profile r actual|profile s/n actual|possibly stale|stale-threshold","BOLT profile 匹配门禁失败。"),
        (r"out of memory|oom.kill|cannot allocate memory","日志显示内存分配失败。"),
        (r"no space left|disk quota","日志显示磁盘耗尽或配额限制。"),
        (r"missing debug|required debug|debug_id|debuglink","BOLT 调试信息门禁失败。"),
        (r"bad exit status","日志中的 RPM scriptlet 退出为封装层错误，根因未从包日志确认。"),
        (r"failed:|ninja: error|fatal error|ld.lld: error|cmake error","编译、配置或链接报错，原始命令和诊断见上下文。"),
    ]:
        if re.search(patt,message):
            return hint
    return "构建在此诊断处失败，原因以原文为准。"


def render(meta, audit=None):
    s=["# 171 · PGO+BOLT Toolchain QB 核对","",
           f"[QB {BUILD}](https://quickbuild.tizen.org/build/{BUILD}) · {PROJECT} · {Q}{BRANCH}{Q} · {Q}{REV}{Q}。"
           f" [分支头原文]({LINK}gerrit-ref.txt)","",
           f"QB 概览状态为 **{meta['overall']}**，界面开始时间 {meta['started_qb_clock']}，"
           f"最近一次界面时长 {meta['duration']}。",
           f" [构建身份]({LINK}build.json) · [QB 概览快照]({LINK}qb-overview.json)",""]
    if meta.get("qb_overview_read_error"):
        s.extend(["最后回读 QB 概览时遇到连接或授权阻塞，终态以发布的逐架构包日志核对。",""])
    if meta.get("local_audit_error"):
        s.extend([f"本地核对停止。{meta['local_audit_error']} [原文]({LINK}audit-error.txt)",""])
    if not audit:
        s.extend(["**构建结果待发布。**", "",
                  "已核实构建页和 Gerrit 分支头。三架构结论、包日志门禁、成品身份及条件补测待产物发布。",""])
        return "\n".join(s)
    s.extend(["| 架构 | LLVM 包结论 | 开始（worker 原文） | 结束（worker 原文） | 日志 |","|---|---|---|---|---|"])
    for arch in ARCHES:
        d=audit[arch]
        start=" / ".join(t.split(" at ",1)[-1] for t in d["start"]) or "无"
        end=" / ".join(t.split(" at ",1)[-1] for t in d["end"]) or "无"
        s.append(f"| {arch} | {d['status']} | {start} | {end} | [原文]({LINK}{arch}.buildlog.txt.gz) |")
    s+=["",f"[发布源码清单]({LINK}standard-manifest.xml) · [逐架构日志回执]({LINK}package-log-audit.json)",""]
    for arch in ARCHES:
        d=audit[arch]
        if d["status"]=="PASS":
            continue
        s+= [f"## {arch} 首个实际错误",""]
        err=d["error"]
        if err:
            p=E/(arch+"-first-error-40x40.txt")
            s += [f"第 {err['line']} 行，阶段 {err['phase']}，{cause(err)}"
                  f" 原文第 {err['first_context_line']}–{err['last_context_line']} 行。"
                  f" [上下文]({LINK}{p.name})","",
                  Q*3+"text",p.read_text(errors="replace").rstrip(),Q*3,""]
        else:
            s+=["包日志中没有识别到明确的首错，见完整日志。",""]
    x=audit["x86_64"]
    g=gate_rows(x)
    s+=["## x86_64 门禁","",f"[日志门禁行原文]({LINK}x86_64-gates.txt)",""]
    for key, rows in g["markers"].items():
        # These markers carry short, structured product gate receipts.
        if len(rows)>0:
            for r in rows:
                s.append(f"- {q(r)}")
        else:
            s.append(f"- {q(key)} 未在日志出现。")
    s+=["",f"- BOLT 日志中的阈值参数 {g['threshold'] or '未记录'}。"]
    for counts in g["counts"]:
        s.append(f"- N/M/S/U/Q 为 {counts['N']} / {counts['M']} / {counts['S']} / {counts['U']} / {counts['Q']}，"
                 f"R 为 {counts['R']:.6%}，S/N 为 {counts['S_over_N']:.6%}。")
    s.append(f"- ARCHIVE_MEMBER_RETRY 共 {len(g['retry'])} 行。")
    s.extend(f"  - {q(r['text'])}" for r in g["retry"])
    s.append("")
    if x["status"]!="PASS":
        s+=["没有本次 x86_64 成品，ELF、clang 身份比较和 V3q 补测均跳过。",""]
        return "\n".join(s)
    if not (E/"clang-comparison.json").is_file():
        s += ["本次 x86_64 已成功，RPM 核验或基准正在进行。",""]
        return "\n".join(s)
    elf=read(E/"runtime-elf-audit.json")
    data=read(E/"clang-comparison.json")
    s+=["## x86_64 成品与 V3","",
        f"独立 RPM 载荷检查 **{elf['status']}**，覆盖 {elf['elf']} 个 ELF 与 {elf['archives']} 个归档，"
        f"{len(elf['findings'])} 项发现。核对 profile 节、符号和动态依赖。"
        f" [ELF 审计]({LINK}runtime-elf-audit.json) · [RPM 下载及 SHA256]({LINK}rpm-downloads.json)","",
        "| 身份 | SHA256 | 文件大小（B） |","|---|---|---:|"]
    for name in ("V3","V3q"):
        r=data[name]
        s.append(f"| {name} | {q(r['sha256'])} | {r['bytes']:,} |")
    s+=["",f"SHA256 **{'相同' if data['same_sha256'] else '不同'}**。 [身份与原始节表]({LINK}clang-comparison.json)","",
        "| ELF 节 | V3（B） | V3q（B） |","|---|---:|---:|"]
    for sec in sorted(data["V3"]["sections"].keys() | data["V3q"]["sections"].keys()):
        s.append(f"| {q(sec)} | {data['V3']['sections'].get(sec,'无')} | {data['V3q']['sections'].get(sec,'无')} |")
    s.append("")
    benchmark=BENCH/"result.json"
    if data["same_sha256"]:
        s.extend(["V3q 补测条件未满足。",""])
    elif benchmark.is_file():
        r=read(benchmark)
        s+=["## V3q 单线程补测","",
            f"状态 **{r['status']}**。使用 168 的 30 项语料、性能核 CPU {r['cpu']}、"
            "一轮预热和五轮正式，三个变体逐轮轮换，按 TU 配对统计 CPU 时间比。","",
            "| CPU 时间比 | 有效 TU | 几何平均比 [95% CI] | 双侧 Wilcoxon p |","|---|---:|---:|---:|"]
        for pair,val in r["paired"]["pairs"].items():
            o=val["groups"]["all"]
            ci=o["ci"]
            if ci:
                s.append(f"| {pair} | {o['tus']} | {o['ratio']:.4f} [{ci[0]:.4f}, {ci[1]:.4f}] | {o['p']:.4g} |")
            else:
                s.append(f"| {pair} | {o['tus']} | — | — |")
        s+=["",f"正式对象比较 {r['formal_objects']}，预热比较 {r['warmup_objects']}。"
                f" [逐 TU 与逐字节结果]({LINK}benchmark/result.json)",""]
        for diff in r["differences"]:
            s.append(f"- 🔴 第 {diff['round']} 轮 {diff['tu']} {diff['left']} / {diff['right']} {diff['status']}。")
        for diff in r["retries"]:
            if diff["objects"]["status"]!="IDENTICAL":
                s.append(f"- 🔴 第 {diff['round']} 轮 {diff['variant']} {diff['tu']} 复跑 {diff['objects']['status']}。")
    return "\n".join(s)


def q(text):
    return Q+text+Q


def compress_logs():
    idx=E/"package-log-identities.json"
    if idx.exists():
        for arch,row in read(idx).items():
            path=Path(row["artifact"]["path"])
            dst=E/(arch+".buildlog.txt.gz")
            if not dst.exists():
                with path.open("rb") as src, dst.open("wb") as out:
                    with gzip.GzipFile(filename="",fileobj=out,mode="wb",compresslevel=5,mtime=0) as enc:
                        shutil.copyfileobj(src,enc)


def publish(meta,audit=None):
    save(E/"build.json",meta)
    sources=[A/"gerrit-ref.txt",A/"collect.py",A/"watch.py",A/"v3q.py",A/"report.py"]
    overview=A/"qb-current.json"
    if overview.is_file():
        shutil.copyfile(overview,E/"qb-overview.json")
    else:
        shutil.copyfile(A/"1242771-overview-initial.json",E/"qb-overview.json")
    for p in sources:
        shutil.copyfile(p,E/p.name)
    compress_logs()
    if (A/"1242774-child.json").is_file():
        shutil.copyfile(A/"1242774-child.json",E/"qb-child-initial.json")
    if (BENCH/"result.json").is_file():
        out=E/"benchmark"
        out.mkdir(exist_ok=True)
        if (A/"benchmark-run.txt").is_file():
            shutil.copyfile(A/"benchmark-run.txt",out/"benchmark-run.txt")
        for p in BENCH.iterdir():
            if p.is_file() and p.suffix in (".json",".csv"):
                shutil.copyfile(p,out/p.name)
    with publication():
        for src in E.rglob("*"):
            if src.is_file():
                d=DEST/src.relative_to(E)
                d.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(src,d)
        DOC.write_text(render(meta,audit))
        rev=commit_push("docs: verify the Toolchain PGO and BOLT Quickbuild",DOC,DEST)
    (A/"published.sha").write_text(rev+"\n")
    print("PUBLISHED",rev,flush=True)
    return rev
