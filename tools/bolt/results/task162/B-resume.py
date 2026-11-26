"""Resume the existing profile generation at the G5 in-place handoff."""
from hashlib import file_digest
from pathlib import Path
import json
import shutil
import subprocess
import sys
import traceback

A = Path(__file__).resolve().parent
W = A.parents[1]
B = W.with_name(W.name + "-bolt")
RUN = W / "archive/task160/run"
STAGES = A / "stages"
E = B / "tools/bolt/results/task162"
DOC = B / "docs/bolt/162_g_chain.md"
sys.path.insert(0,str(W/"archive/task161"))
from coordination import publication, save
from review_packet import commit_push

sys.path.insert(0,str(RUN/"orchestration"))
sys.argv[1:4] = [str(W),str(B),str(RUN)]
import dispatch
from handoff import attach_g4, g4_scratch, receipt

dispatch.UNIT = "llvm-opt-task162-g-chain"
STEPS = ("G5", "G6", "G7", "G8")
LIMIT = 10_000_000


def read(path):
    return json.loads(path.read_text())


def state(value):
    save(A/"live.json", value)
    print(json.dumps(value,ensure_ascii=False),flush=True)


def collect(source, destination, local):
    if not source.is_file() or source.is_symlink():
        return
    if source.stat().st_size > LIMIT:
        local.append(receipt(source))
    else:
        destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,destination)


def render(rows, candidate):
    clean=lambda v:str(v or "—").splitlines()[0].replace("|", "\\|")
    lines=["# 162 · 从 G5 原地接续", "",
           "160 的 G4 构建和 PGO/Ninja 门禁已完成。旧交接在重命名 root 所有的构建根时失败。"
           "G5 使用原 G4 构建目录，通过当前 UID 的非特权命名空间调用原构建工具。",
           "G4 的 clang-22、Ninja 输入和 23 个成品 RPM 已逐项核对。RPM 原位置作为 V2 来源保留。",
           "", "[功能复测](161_ps6_review_packet.md) · "
           "[全部输入](../../tools/bolt/results/task162/G4-input-inventory.json) · "
           "[G4 RPM](../../tools/bolt/results/task162/G4-rpm-check.json) · "
           "[编排差异](../../tools/bolt/results/task162/B-orchestration.diff)", "",
           "| 步骤 | 状态 | 档位 | MemoryMax B | MemAvailable B | /home 可用 B | 用时 s | 原因 |",
           "|---|---|---|---:|---:|---:|---:|---|"]
    by_stage={row["step"]:row for row in rows}
    for step in STEPS:
        row=by_stage.get(step,{})
        last=(row.get("admission") or [{}])[-1]
        data=(step,row.get("status","PENDING"),row.get("tier","—"),row.get("memory_max","—"),
              last.get("mem_available","—"),last.get("home_available","—"),row.get("seconds","—"),
              clean(row.get("reason")))
        lines.append("| "+" | ".join(map(str,data))+" |")
    for row in rows:
        step=row["step"]
        lines.append("")
        lines.append(f"[{step} 回执](../../tools/bolt/results/task162/{step}/result.json)")
    if candidate:
        lines.extend(["",f"157-B 状态为 **{candidate['status']}**。"+clean(candidate.get("error") or candidate.get("reason")),
                      "[候选回执](../../tools/bolt/results/task162/paired-candidate.json)"])
        if candidate["status"]=="PASS":
            lines.append(f"分支为 {candidate['branch']}，集成提交 {candidate['integration']}，测试提交 {candidate['test']}。")
    return "\n".join(lines)+"\n"


def publish(rows, key, candidate=None):
    local=[]
    with publication():
        E.mkdir(parents=True,exist_ok=True)
        for source in (A/"evidence").iterdir():
            if source.name.startswith(("G4-","B-")):
                collect(source,E/source.name,local)
        for row in rows:
            step=row["step"]
            source=RUN/step
            dest=E/step
            collect(STAGES/(step+".json"),dest/"result.json",local)
            for path in source.iterdir() if source.exists() else []:
                if path.suffix in (".txt",".json",".log",".jsonl",".original"):
                    collect(path,dest/path.name,local)
            details=row.get("worker",{}).get("details",{})
            for entry in details.get("artifacts",[]):
                path=Path(entry["path"])
                if path.suffix in (".txt",".json",".manifest",".log"):
                    collect(path,dest/path.name,local)
        if candidate:
            save(E/"paired-candidate.json",candidate)
            root=RUN.parent/"candidates/B"
            for path in root.rglob("*") if root.exists() else []:
                if path.suffix in (".txt",".json",".manifest",".patch",".cmake"):
                    collect(path,E/"candidate-b"/path.relative_to(root),local)
        save(E/"B-local-files.json",local)
        DOC.write_text(render(rows,candidate))
        sha=commit_push("docs: record the in-place profile generation "+key,DOC,E)
    (A/("published-"+key+".sha")).write_text(sha+"\n")
    return sha


def prepare():
    g4=read(RUN/"G4.json")
    inventory=read(A/"evidence/G4-input-inventory.json")
    rpms=read(A/"evidence/G4-rpm-check.json")
    clang=read(A/"evidence/G4-clang-check.json")
    if (g4["worker"]["status"]!="PASS" or inventory["missing"] or
        rpms["status"]!="PASS" or clang[0]!=g4["worker"]["details"]["pgo_clang"]):
        raise ValueError("task 160 G4 checkpoint is not complete")
    old=read(RUN/"G4/clang-handoff.json")
    if old!=clang[1]:
        raise ValueError("preserved G4 compiler differs from the recorded handoff")
    attach_g4(RUN,old)
    state({"step":"G5","state":"READY","g4_build":str(g4_scratch(RUN)),
           "original_g4_handoff_error":g4["reason"],**dispatch.resources()})
    publish([], "preflight")


def run_step(step):
    disk=dispatch.disk_limits(222650722030)[step]
    def waiting(measurement, reason):
        state({"step":step,"state":"WAITING","reason":reason,**measurement})
    plan,reason,checks,wait=dispatch.select(step,disk,waiting)
    if plan is None:
        return {"step":step,"status":"SKIPPED","reason":reason,"admission":checks,
                "admission_wait_seconds":round(wait,3),"ended_at":dispatch.stamp()}
    state({"step":step,"state":"RUNNING",**checks[-1],**plan})
    try:
        row=dispatch.execute(step,plan,checks,wait,1)
        dispatch.finish_stage(row)
        return row
    except Exception:
        raw=traceback.format_exc()
        print(raw,flush=True)
        dispatch.command(["/usr/bin/systemctl","--user","stop",dispatch.UNIT+"-"+step.lower()+"-1.service"],
                         timeout=140)
        return {"step":step,"status":"STOP","reason":raw.splitlines()[-1],
                "error":raw,"admission":checks,"ended_at":dispatch.stamp()}


def paired(rows):
    lookup={row["step"]:row["status"] for row in rows}
    if any(lookup.get(n)!="PASS" for n in ("G6","G7","G8")):
        return {"status":"SKIPPED","reason":"G6, G7 and G8 must pass"}
    for name in ("G6","G7","G8"):
        if not (A/("published-"+name+".sha")).is_file():
            return {"status":"STOP","error":"missing published checkpoint for "+name}
    sys.path.insert(0,str(RUN.parent/"candidates"))
    import candidate
    candidate.OLD=STAGES
    previous=read(RUN.parent/"candidates/A/result.json")
    if previous["status"]!="PASS":
        return {"status":"STOP","error":"candidate A is unavailable"}
    return candidate.finalize("B",previous)


def main():
    STAGES.mkdir(exist_ok=True)
    prepare()
    rows=[]
    for step in STEPS:
        if rows and rows[-1]["status"]!="PASS":
            row={"step":step,"status":"SKIPPED","reason":"preceding stage did not pass",
                 "admission":[dispatch.resources()],"ended_at":dispatch.stamp()}
        else:
            row=run_step(step)
        save(STAGES/(step+".json"),row)
        rows.append(row)
        publish(rows,step)
    try:
        candidate=paired(rows)
    except Exception:
        candidate={"status":"STOP","error":traceback.format_exc()}
    save(A/"paired-candidate.json",candidate)
    sha=publish(rows,"B",candidate)
    save(A/"B-terminal.json",{"rows":rows,"candidate":candidate,"published":sha})
    state({"step":"B","state":"TERMINAL","candidate":candidate,"published":sha})


if __name__=="__main__":
    main()
