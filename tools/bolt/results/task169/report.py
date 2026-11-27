"""Archive the verified QB package evidence and authenticated overview receipts."""
from datetime import datetime, timezone
import gzip
import shlex
import shutil
import sys
from xml.etree import ElementTree
from zoneinfo import ZoneInfo

from audit import A, W, B, E, ARCH, PS7, PGO, read, save
sys.path.insert(0,str(W/"archive/task161"))
from coordination import publication
from review_packet import commit_push

OUT = B/"tools/bolt/results/task169"
DOC = B/"docs/bolt/169_qb_ps7_pgo_bolt.md"
L = "../../tools/bolt/results/task169/"
PS7_REV = "de305f2c4de2721c7aeb5a677cd0ee32c3be505c"
PGO_REV = "4080f55abfc7c48097c9bd7fdbf9334e37c661af"
PS7_BRANCH = "sandbox/lhmax2025/llvm-361624-ps7-20261126"
PGO_BRANCH = "sandbox/lhmax2025/llvm-pgo-bolt-20261125"
ZONE = ZoneInfo("America/Los_Angeles")
Q = chr(96)


def worker_time(records):
    (r,) = records
    s = r["text"].split(" at ",1)[1].removesuffix(".")
    return datetime.strptime(s,"%a %b %d %H:%M:%S UTC %Y").replace(tzinfo=timezone.utc).astimezone(ZONE).isoformat()


def cause():
    c=W/"archive/task160/candidates/B"
    expanded=next(x for x in (c/"test-x86_64.stdout.txt").read_text().splitlines()
                  if x.startswith("python3 ") and " pgo-prepare " in x)
    tokens=shlex.split(expanded)
    assert "--bolt-profile" not in tokens
    bad=next(x for x in tokens if x.endswith(".profdata.xz--bolt-profile"))
    m=read(c/"assets/llvm-profiles.manifest")
    keys=[[r["project"],r["pgo"],r["bolt"]] for r in m["profiles"]]
    spec=[{"line":i,"text":s} for i,s in enumerate((c/"assets/llvm.spec").read_text().splitlines(),1)
          if s.startswith("%define llvm_pgo_bolt_source") or s.startswith("python3 ") and " pgo-prepare " in s]
    older=B/"tools/bolt/results/task164/D-x86_64.buildlog.txt"
    previous=next(x for x in older.read_text().splitlines() if "missing profile mapping" in x)
    validation=W/"archive/task160/candidates/candidate.py"
    validators=[{"line":i,"text":s} for i,s in enumerate(validation.read_text().splitlines(),1)
                if 'argv+=["--bolt-profile",' in s or '"--bolt-profile" in prepare[0]' in s]
    save(E/"pgo-bolt-argument-audit.json",{"spec_lines":spec,"expanded_line":expanded,"shlex_argv":tokens,
         "fused_argument":bad,"1240310_error":previous,"manifest_status":m["status"],"manifest_keys":keys,
         "prior_static_validators":validators})
    shutil.copy2(c/"assets/llvm-profiles.manifest",E/"pgo-bolt-manifest.json")
    return previous


def records():
    remote={name:sha for sha,name in (s.split() for s in (E/"gerrit-refs.txt").read_text().splitlines())}
    builds={}
    for n in (*PS7,*PGO):
        rev,branch=(PS7_REV,PS7_BRANCH) if n in PS7 else (PGO_REV,PGO_BRANCH)
        project="Tizen-Base-Dev" if n in ("1241534","1241584") else "Tizen-Base-Toolchain"
        manifests=[p.get("revision") for p in ElementTree.parse(A/n/"standard-manifest.xml").iter("project")
                   if p.get("name")=="platform/upstream/llvm"]
        assert rev in manifests and remote["refs/heads/"+branch]==rev, (n,rev,manifests)
        loc=read(A/n/"public-log-locations.json")
        qb=read(E/n/"qb-identity.json") if (E/n/"qb-identity.json").exists() else None
        if qb:
            assert rev in (qb["build_package_list"] or "") and project in qb["title"], (n,qb)
            url=(qb["download"] or "invalid").replace("http:","https:",1).rstrip("/") + "/"
            assert all(loc[arch]["result"]["url"].startswith(url) for arch in ARCH),(n,url,loc)
        logs={}
        for arch in ARCH:
            d=read(E/n/(arch+"-log-audit.json"))
            assert any(project in line and f"arch '{arch}'" in line for line in d["project_and_arch"])
            logs[arch]={"status":"PASS" if d["publication_bucket"]=="succeeded" else "FAIL",
                        "start_pst":worker_time(d["worker_start"]),"end_pst":worker_time(d["worker_end"]),
                        "first_error":d["first_error"],"gate_lines":d["gate_lines"]}
        builds[n]={"project":project,"rev":rev,"branch":branch,"manifest_revisions":manifests,
                   "overview":qb,"architectures":logs,"log_urls":loc,"worker_span_pst": [
                       min(x["start_pst"] for x in logs.values()), max(x["end_pst"] for x in logs.values())]}
    save(E/"build-records.json",builds)
    return builds


def render(builds, audit, history):
    clock=lambda value: datetime.fromisoformat(value).strftime("%m-%d %H:%M:%S")
    s=["# 169 · PS7 与 PGO+BOLT 的 QB 核对","",
       "**PS7 两个项目的三架构 LLVM 包构建通过。PGO+BOLT 两个项目的 x86_64 均在 %build 参数解析处失败，"
       "其余两架构的 LLVM 包构建通过。**","",
       "| QB | 项目 | 候选 | x86_64 | aarch64 | armv7l | LLVM worker 区间（PST） | QB 概览状态和起止 |",
       "|---|---|---|---|---|---|---|---|"]
    for n,d in builds.items():
        qb=d["overview"]
        status=(f"{qb['status']} · {qb['start_qb_clock']} → {qb['end_qb_clock'] or '未完成'}（界面时钟）"
                if qb else "需登录")
        tag="PS7" if n in PS7 else "PGO+BOLT"
        arch=" | ".join(d["architectures"][a]["status"] for a in ARCH)
        span=" → ".join(map(clock,d["worker_span_pst"]))
        s.append(f"| [{n}](https://quickbuild.tizen.org/build/{n}) | {d['project']} | {tag} | {arch} | {span} | {status} |")
    s+=["", "LLVM worker 区间取三架构包日志最早的开始和最晚的结束。原始 worker 时钟为 UTC。"]
    if any(not r["overview"] for r in builds.values()):
        s+=["QB 概览需要登录，匿名 REST 只读请求返回 HTTP 401。表中标注了未核实的构建级起止与总体状态。"]
    s+=["",f"- PS7 {Q}{PS7_BRANCH}{Q} → {Q}{PS7_REV}{Q}。",
           f"- PGO+BOLT {Q}{PGO_BRANCH}{Q} → {Q}{PGO_REV}{Q}。","",
           f"四份发布 manifest 含对应提交，Gerrit 只读查询确认两个分支头。"
           f" [构建与逐架构时间]({L}build-records.json) · [Gerrit 原文]({L}gerrit-refs.txt)","",
           "## PS7 成品 RPM","",
           "| QB | 架构 | 目标归属 | RPM shebang | 日志后置检查 | 未打包错误 | clang Requires |",
           "|---|---|---|---:|---:|---|---|"]
    for n in PS7:
        for a,d in audit[n].items():
            assert all(p["vcs"]=="platform/upstream/llvm#"+PS7_REV for p in d["headers"].values())
            count=sum(len(row)==1 and row[0]["pass"] for row in d["shebangs"].values())
            checks=sum(x["matched"] for x in d["log"]["post_checks"].values())
            q=d["requires"]
            comparison= ("；无 154-B 同架构对照" if not q["same_arch_available"] else
                         "；仅 llvm release 变更" if not any(q["after_llvm_release_normalization"].values()) else
                         "；差异见审计")
            requirements=("发现 Python 条目" if q["python_entries"] else "无 Python 条目")+comparison
            owner=f"[{'PASS' if d['ownership_pass'] else 'FAIL'}]({L}{n}/{a}/audit.json)"
            unpackaged="有" if d["log"]["unpackaged"] else "无"
            s.append(f"| {n} | {a} | {owner} | {count}/6 | {checks}/6 | {unpackaged} | {requirements} |")
    s+=["", "18 个 RPM 的 VCS 字段均指向 PS7。scan-build 的资源和手册页在 clang，scan-view 的数据在 llvm。"
           "libscanbuild、libear 在 clang。llvm-devel 未保留这些条目。"
           "两个 x86_64 的 Requires 原始差异均为 llvm 从 22.1.8-1 锁定改成 22.1.8-2.1。"
           f" [六套审计]({L}ps7-audit.json) · [18 个 RPM 的下载地址和 SHA256]({L}ps7-downloads.json)","",
           "## PGO+BOLT x86_64 的共同失败","",
           "两个日志首先在 %build 的 pgo-prepare 参数解析处报错，CMake 尚未开始。spec 把可选宏紧贴"
           "带引号的 profdata 位置参数。RPM 展开和 shell 实际命令均将 .xz 和 --bolt-profile 合为一个参数，"
           "所以下一个 fdata 被 argparse 拒绝。166 的静态验收为 helper 单独构造了传参列表，而 spec 展开"
           "核对只检查子串出现，漏掉了 shell 实际分词。","",
           "1240310 在完成参数解析后报 D 映射缺失。本次 Base-Dev 在解析阶段已退出。"
           "新候选 manifest 的两个键仍只覆盖 T。1240310 的错误原文如下。","","> "+history,"",
           "Toolchain 未到 PGO Ninja、BOLT（含 -stale-threshold=5）、运行时依赖门禁或归档转换阶段。"
           "没有 ARCHIVE_MEMBER_RETRY 行。本次未产出 x86_64 成品，ELF、V3 身份比较和 V3q 补测均为 SKIPPED。",
           f" [spec、RPM 展开和实参分词]({L}pgo-bolt-argument-audit.json)",""]
    for n in PGO:
        d=builds[n]["architectures"]["x86_64"]["first_error"]
        f="x86_64-first-error-40x40.txt"
        s += [f"### {n} 首个实际错误原文","",
              f"第 {d['line']} 行。以下保留第 {d['from_line']}–{d['to_line']} 行，前 40 行及错误后至日志结束。","",
              Q*3+"text",(E/n/f).read_text().rstrip("\n"),Q*3,"",
              f"[上下文原文]({L}{n}/{f}) · [完整包日志]({L}{n}/x86_64.buildlog.txt.gz)",""]
    return "\n".join(s)


def archive():
    history=cause()
    builds=records()
    body=render(builds,read(E/"ps7-audit.json"),history)
    (A/"report.md").write_text(body)
    for n in (*PS7,*PGO):
        for f in ("standard-manifest.xml","public-log-locations.json"):
            shutil.copy2(A/n/f,E/n/f)
        for arch in ARCH:
            source=A/n/(arch+".buildlog.txt")
            target=E/n/(source.name+".gz")
            if not target.exists():
                with source.open("rb") as inc, target.open("wb") as out:
                    with gzip.GzipFile(filename="",fileobj=out,mode="wb",compresslevel=5,mtime=0) as z:
                        shutil.copyfileobj(inc,z)
    shutil.copy2(A/"ps7-downloads.json",E/"ps7-downloads.json")
    for f in ("report.py","collect_qb.py","audit.py","download_ps7.py"):
        shutil.copy2(A/f,E/f)
    with publication():
        for src in E.rglob("*"):
            if src.is_file():
                t=OUT/src.relative_to(E)
                t.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(src,t)
        DOC.write_text(body)
        sha=commit_push("docs: audit Quickbuild packaging and profile preparation",DOC,OUT)
    (A/"published.sha").write_text(sha+"\n")
    print(sha,flush=True)


if __name__=="__main__":
    archive()
