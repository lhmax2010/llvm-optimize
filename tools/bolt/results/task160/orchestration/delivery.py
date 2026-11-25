from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess

from handoff import SUFFIX, confined
from policy import STEPS

def table(rows):
    lines=["|步骤|结论|档位|MemoryMax B|编译/ThinLTO/链接|起止 PST|等待 s|执行 s|cgroup 峰值 B|准入内存 B|准入磁盘 B|清理 df 差值 B|原因|",
           "|---|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|---|"]
    for step in STEPS:
        r=next((row for row in rows if row["step"]==step),{})
        m=(r.get("admission") or [{}])[-1]
        jobs="/".join(str(r.get(k) or "—") for k in ("jobs","thinlto_jobs","link_jobs"))
        why=str(r.get("reason") or "—").splitlines()[0].replace("|","\\|")
        cols=(step,r.get("status","PENDING"),r.get("tier","—"),r.get("memory_max","—"),jobs,
              r.get("started_at","—")+" → "+r.get("ended_at","—"),r.get("admission_wait_seconds","—"),
              r.get("seconds","—"),r.get("resources",{}).get("memory.peak","—"),m.get("mem_available","—"),
              m.get("home_available","—"),r.get("cleanup",{}).get("df_delta","—"),why)
        lines.append("| "+" | ".join(map(str,cols))+" |")
    return lines

def remaining(archive):
    out=[]
    for step in ("G4","G5", *(p.name for p in sorted(archive.glob("preview-*")) if p.is_dir())):
        for p in (archive/step/SUFFIX,archive/step/"tmp"):
            if p.is_dir():
                try:
                    confined(p,archive)
                    info=p.lstat()
                    out.append({"path":str(p),"inode":info.st_ino,"device":info.st_dev})
                except ValueError as exc:
                    out.append({"path":str(p),"refused":str(exc)})
    return out

def publish(work,b,archive,key,rows):
    results=[]
    evidence=b/"tools/bolt/results/task160/g-chain"
    doc=b/"docs/bolt/160_g_chain.md"
    try:
        startup=json.loads((archive/"startup.json").read_text())
        evidence.mkdir(parents=True,exist_ok=True)
        artifacts=[]
        files=[]
        def retain(p,name):
            if not p.is_file():
                return
            size=p.stat().st_size
            if size<=2**20:
                target=evidence/name
                shutil.copyfile(p,target)
                files.append(target)
            else:
                with p.open("rb") as stream:
                    artifacts.append({"path":str(p),"bytes":size,"sha256":hashlib.file_digest(stream,"sha256").hexdigest()})
        retain(archive/(key+".json"),key+".json")
        retain(archive/"startup.json","startup.json")
        retain(archive/"sudo-recheck.json","sudo-recheck.json")
        retain(archive/"tests.txt","tests.txt")
        if key=="summary":
            for name in ("admission-live.jsonl","tests.txt","skill-tests.txt","gate-tests.txt","sudo-recheck.json"):
                retain(archive/name,name)
            retain(archive/"G-config/recover-g3.json","G3-reused.json")
            for path in sorted((archive/"G-evidence").glob("sudo-*-output.txt")):
                retain(path,path.name)
            residual=remaining(archive)
            if residual:
                p=evidence/"sudo-residuals.json"
                p.write_text(json.dumps(residual,indent=2,ensure_ascii=False)+"\n")
                files.append(p)
                from sudo_script import write_script
                write_script(archive,residual)
        else:
            if key == "G4":
                for attempt in sorted((archive/"G-profiles").glob("pgo-build-*")):
                    for name in ("build-0.txt","build-0.json","ninja-gate.json","runtime-dependency-gate.txt"):
                        retain(attempt/name,key+"-"+attempt.name+"-"+name)
            for name in ("service.log","gbs.log","prep.log","rpm-build.log","worker.json","rpm-identities.json",
                         "dry-run.json","validation.json","pgo-ninja-violations.json","pgo-configure-gate.json","pgo-shipped-libraries.json","pgo-evidence.json","key-lines.json","needed.json",
                         "needed-comparison.json","relink-artifacts.json","runtime-artifacts.json",
                         "runtime-dependency-gate.json","runtime-dependency-gate.txt","profile-input.json","member-retries.log","member-retry-receipts.json","pgo-clang.json","g5-handoff.json","started.json","cgroup-stop-1.json",
                         "resources.jsonl","bolt-tools.log","bolt-configure.log","relink.log"):
                retain(archive/key/name,key+"-"+name.replace(".log",".txt"))
        if artifacts:
            p=evidence/(key+"-local-files.json")
            p.write_text(json.dumps(artifacts,indent=2)+"\n")
            files.append(p)
        text=["# 160 · PGO/BOLT profile 重跑","",
              "**"+("最终" if key=="summary" else "进行中")+"**","",*table(rows),"",
              f"本地配方 {startup['recipe']}。转换器重试修复未触及 PGO Ninja 门禁，沿用 150 的预演。"
              "G4 的配方在 CMake 后、编译前执行完整 Ninja 门禁。N2 已由 149-run 完成。",
              "",
              f"峰值增长 P 为 {startup['peak_growth']:,} B。G4 准入包含 15% 系数、"
              "15 GiB 安全线和另一项目的 30 GB 磁盘预留。",
              "",
              f"启动时 {startup['startup']['time']}，MemAvailable {startup['startup']['mem_available']:,} B，"
              f"/home 可用 {startup['startup']['home_available']:,} B。",
              f"G6 等待截止 {startup['g6_deadline']}。整体截止 {startup['deadline']}。",
              ""]
        text.extend(f"- {step} 磁盘准入 {startup['disks'][step]:,} B" for step in STEPS)
        text.extend(["", "若 G4 通过，先保留经过 SHA256 核对的 clang 和成品清单。G5 复用 G4 的对象和 Ninja 图重链，"
                     "核对导出的 ELF、BOLT 工具和匹配运行库后清理交接根。"
                     "G3 检查点按内容核对，IR 源提交与新的 PGO 源提交分别登记。",
                     "", "看门狗只停止本任务当前子单元。清理之后按依赖关系和准入规则继续。",
                     "", "[150 的配方和预演](150_g_chain.md) · "
                     "[修复和候选报告](160_converter_retry.md) · "
                     "[160 编排单测](../../tools/bolt/results/task160/g-chain/tests.txt)",
                     "", "## 日志与结果", ""])
        if key=="summary":
            end=json.loads((archive/"summary.json").read_text())
            text.extend([f"看门狗触发 {end['watchdog_triggered']}，结束时 /home 可用 {end['end']['home_available']:,} B。",
                         f"需要 sudo 复核的残留 {len(residual)} 项。脚本仅保留在本地。",
                         "[最终汇总 JSON](../../tools/bolt/results/task160/g-chain/summary.json)", ""])
        for row in rows:
            step=row["step"]
            details=row.get("worker",{}).get("details",{})
            output={k:details[k] for k in ("dry_run","pgo_clang","merged_profdata","bolt_match","runtime_dependency_gate","validation")
                    if details.get(k) is not None}
            if step=="G4":
                output["archive_member_retries"]=row.get("archive_member_retries",[])
            if "retained_clang" in row:
                output["retained_clang"]=row["retained_clang"]
            if step in ("G5","G6","G8"):
                output["artifacts"]=[x for x in details.get("artifacts",[]) if not x["path"].endswith("/input.o")]
            if step=="G6":
                output["VmHWM_sample"]=row.get("resources",{}).get("VmHWM_sample")
            text.extend([f"### {step}","",f"[{step} JSON 与日志索引](../../tools/bolt/results/task160/g-chain/{step}.json)",""])
            if output:
                text.extend(["~~~json",json.dumps(output,indent=2,ensure_ascii=False),"~~~",""])
        doc.write_text("\n".join(text).rstrip()+"\n")
        files.append(doc)
        def git(*args):
            r=subprocess.run(["/usr/bin/git","-C",str(b),*map(str,args)],text=True,capture_output=True,
                             timeout=100,env=dict(os.environ,GIT_TERMINAL_PROMPT="0"))
            results.append(dict(argv=args,rc=r.returncode,stdout=r.stdout,stderr=r.stderr))
            if r.returncode:
                raise RuntimeError(f"git {args[0]} exited {r.returncode}")
            return r.stdout
        if git("branch","--show-current").strip()!="bolt-v4" or git("diff","--cached","--name-only").strip():
            raise RuntimeError("evidence branch or index changed")
        git("add","--",*[str(p) for p in files])
        git("diff","--cached","--check","--",str(doc))
        git("-c","user.name=Hao Lin","-c","user.email=hao.lin@samsung.com","commit","-s",
            "-m","docs: record task 160 profile generation "+key)
        git("push","origin","HEAD:refs/heads/bolt-v4")
        rev=git("rev-parse","HEAD").strip()
        assert git("ls-remote","--exit-code","origin","refs/heads/bolt-v4").split()[0]==rev
        (archive/("published-"+key+".sha")).write_text(rev+"\n")
    except Exception as error:
        results.append({"error":str(error)})
        print("EVIDENCE",key,str(error),flush=True)
    (archive/("publish-"+key+".json")).write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n")

