from datetime import datetime
from pathlib import Path
import json, os, shutil, subprocess, sys, time
import candidate as c

A,B,E,OLD=c.A,c.B,c.E,c.OLD
DEST=B/"tools/bolt/results/task157"
DOC=B/"docs/bolt/157_qb_candidates.md"
BGIT=["/usr/bin/git","-C",str(B)]
SYSTEM=["/usr/bin/systemctl","--user"]
WATCH=A/"progress.json"
STATE=("PASS","FAIL","SKIPPED","INTERRUPTED","STOP")

def observed():
    return {n:c.read(OLD/(n+".json")) for n in ("G4","G5","G6","G7","G8") if (OLD/(n+".json")).is_file()}

def progress(phases,status):
    c.save(WATCH,{"at":datetime.now(c.TIMEZONE).isoformat(),"state":status,
                 "stages":{n:r.get("status") for n,r in observed().items()},"candidates":phases})

def live():
    r=c.command([*SYSTEM,"show","llvm-opt-151-g-chain.service","-p","ActiveState","--value"],
                check=False,timeout=20)
    return r.stdout.strip() in ("active","activating","reloading","deactivating")

def blocker(kind,reason,stages):
    d=A/kind
    d.mkdir(exist_ok=True)
    (d/"STOP.txt").write_text(reason+"\n")
    c.save(d/"151-stage-receipts.json",stages)
    result={"kind":kind,"status":"STOP","error":reason,
            "prerequisites":{n:r.get("status") for n,r in stages.items()}}
    if kind=="B" and "G6" in stages:
        g=stages["G6"]
        result["last_g6_admission"]=next(iter(reversed(g.get("admission",[]))),None)
        result["g6_reason"]=g.get("reason")
    if kind=="B":
        raw=c.PROFILES/"bolt-match.json"
        if raw.is_file():
            shutil.copyfile(raw,d/"G7-match.json")
        logs={}
        for attempt in c.PROFILES.glob("bolt-match-*"):
            for path in attempt.glob("rewrite*"):
                if not path.is_file():
                    continue
                digest=c.receipt(path)
                if digest["bytes"]<10_000_000:
                    shutil.copyfile(path,d/(attempt.name+"-"+path.name+".txt"))
                logs[str(path)]=digest
        if logs:
            c.save(d/"G7-raw-log-receipts.json",logs)
    c.save(d/"result.json",result)
    return result

def delivery_sources(kind):
    d=A/kind
    items=[p for p in d.iterdir() if p.is_file() and p.suffix in (".txt",".json",".cmake")
           and p.stat().st_size<=10_000_000]
    for dirname in ("patches","messages"):
        if (d/dirname).is_dir():
            items+=sorted((d/dirname).iterdir())
    m=d/"assets/llvm-profiles.manifest"
    if m.is_file():
        items.append(m)
    return items

def publish(kind,results):
    # Commit only named files. If a predecessor is committing evidence at the
    # same time, let its index become idle before staging.
    deadline=time.monotonic()+180
    while True:
        staged=c.command([*BGIT,"diff","--cached","--name-only"]).stdout
        if not staged:
            break
        c.require(time.monotonic()<deadline,"evidence branch has another staged change")
        time.sleep(3)
    def git(*args):
        return c.command([*BGIT,*args],timeout=180).stdout
    c.require(git("branch","--show-current").strip()=="bolt-v4","evidence checkout is on another branch")
    before=git("rev-parse","HEAD").strip()
    remote=git("ls-remote","--exit-code","origin","refs/heads/bolt-v4").split()[0]
    c.command([*BGIT,"merge-base","--is-ancestor",remote,before],timeout=20)
    payload=[]
    for source in [E/"baseline.json",A/"candidate.py",A/"watch.py",A/"hooks/pre-push"]:
        dest=DEST/source.name
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,dest)
        payload.append(dest)
    for source in delivery_sources(kind):
        dest=DEST/kind/source.relative_to(A/kind)
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,dest)
        payload.append(dest)
    base=c.read(E/"baseline.json")
    lines=["# 157 · QB PGO 候选","",
           f"固定配方 `{base['recipe']}`，tree `{base['tree']}`，直接父提交 `{base['immediate_parent']}`。"
           f"PS5 `{base['ps5']}` 是祖先。","",
           "候选面向 Toolchain 项目 T，当前 profile 只含 T 的映射。"
           "x86_64 的 RPM 展开使用 LLVM_PROFDATA_FILE，CMake 源码将它转换为 -fprofile-instr-use。"
           "验证通过脚本模式执行对应 CMake 片段，不配置或编译 LLVM。ARM 展开与集成提交逐字节比较。",
           "",
           "| 候选 | 结论 | 集成提交 | QB 测试提交 | 远端分支或停止原因 |",
           "|---|---|---|---|---|"]
    for n in ("A","B"):
        r=results.get(n,{"status":"PENDING"})
        outcome=(r.get("branch") or r.get("error","等待阶段回执")).replace("\n"," ").replace("|","\\|")
        lines.append(f"| {n} | {r['status']} | {r.get('integration','—')} | {r.get('test','—')} | {outcome} |")
    lines+=["","远端 refs/heads 创建使用普通 push。pre-push 门禁要求 Gerrit 通告该引用的旧 SHA 全零，"
             "避免并发更新已存在分支。",""]
    for n,r in results.items():
        lines.extend([f"[{n} 状态和阶段原文](../../tools/bolt/results/task157/{n}/result.json)"])
        if r.get("status")=="PASS":
            lines.extend([f"[{n} 推送原文](../../tools/bolt/results/task157/{n}/sandbox-push.stdout.txt) · "
                          f"[{n} 远端头](../../tools/bolt/results/task157/{n}/sandbox-after.stdout.txt)"])
    DOC.write_text("\n".join(lines)+"\n")
    git("add","--",DOC,*payload)
    git("diff","--cached","--check","--",DOC)
    c.require(git("diff","--cached","--name-only").strip(),"no new task157 evidence to commit")
    git("-c","user.name=Hao Lin","-c","user.email=hao.lin@samsung.com","commit","-s","-m",
        "docs: record PGO build verification candidate "+kind,"--",DOC,*payload)
    pushed=c.command([*BGIT,"push","origin","HEAD:refs/heads/bolt-v4"],timeout=180)
    head=git("rev-parse","HEAD").strip()
    c.require(git("ls-remote","--exit-code","origin","refs/heads/bolt-v4").split()[0]==head,"bolt-v4 did not match")
    c.save(A/(kind+"-published.json"),{"commit":head,"push_stdout":pushed.stdout,"push_stderr":pushed.stderr})
    return head

def commit_evidence(kind,results):
    try:
        results[kind]["evidence_commit"]=publish(kind,results)
    except Exception as error:
        results[kind]["evidence_error"]=str(error)
        (A/(kind+"-evidence-error.txt")).write_text(str(error)+"\n")
    progress(results,"WAITING" if kind=="A" and results[kind]["status"]=="PASS" else "DONE")
    print(json.dumps(results[kind],ensure_ascii=False),flush=True)

def main():
    c.preflight()
    results={}
    while True:
        stages=observed()
        g4=stages.get("G4",{}).get("status")
        if g4 in STATE:
            break
        if not live():
            results["A"]=blocker("A","151 stopped without a terminal G4 receipt",stages)
            break
        progress(results,"WAITING_FOR_G4")
        time.sleep(30)
    if "A" not in results:
        if g4=="PASS":
            results["A"]=c.finalize("A")
            c.save(A/"A/151-stage-receipts.json",{"G4":stages["G4"]})
            progress(results,"A_COMPLETE")
        else:
            results["A"]=blocker("A",f"G4 {g4}: "+stages["G4"].get("reason",""),stages)
    commit_evidence("A",results)
    if results["A"]["status"]!="PASS":
        results["B"]=blocker("B","A prerequisites did not pass",observed())
    else:
        while True:
            stages=observed()
            bad=next((n for n in ("G6","G7","G8")
                      if n in stages and stages[n]["status"] in STATE and stages[n]["status"]!="PASS"),None)
            if bad:
                state=stages[bad]
                results["B"]=blocker("B",f"{bad} {state['status']}: "+state.get("reason",""),stages)
                break
            if all(stages.get(n,{}).get("status")=="PASS" for n in ("G6","G7","G8")):
                results["B"]=c.finalize("B",results["A"])
                c.save(A/"B/151-stage-receipts.json",stages)
                break
            if not live():
                results["B"]=blocker("B","151 stopped before G6, G7 and G8 all passed",stages)
                break
            progress(results,"WAITING_FOR_G6_TO_G8")
            time.sleep(45)
    commit_evidence("B",results)
    c.save(A/"final.json",results)

if __name__=="__main__":
    main()
