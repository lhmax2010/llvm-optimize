from datetime import datetime
from pathlib import Path
import hashlib, json, os, shlex, shutil, subprocess, sys, time, traceback

A=Path(__file__).resolve().parent
W=A.parents[1]
B=W.with_name(W.name+"-bolt")
GIT=["/usr/bin/git","-C",str(B)]
SYS=["/usr/bin/systemctl","--user"]
ORCH=W/"archive/task151/orchestration"
sys.path.insert(0,str(ORCH))
from policy import GIB, PAGE, ZONE, admit, floor_disk, stop_line
from handoff import confined, prune
from corpus_gate import corpus_terminal
DEADLINE=datetime(2026,11,27,20,tzinfo=ZONE)
GROWTH=222_650_722_030
DISK=floor_disk(GROWTH,True)
R=B/"tools/bolt/results/task154"
DOC=B/"docs/bolt/154_ps6_fixes.md"
ENV={**os.environ,"GIT_TERMINAL_PROMPT":"0","LC_ALL":"C"}
UNIT="llvm-opt-task154-full-build"
CHECKPOINTS={
    "151":(W/"archive/task151/published-summary.sha","tools/bolt/results/task151/summary.json"),
    "153":(W/"archive/task153/published-final.sha","tools/bolt/results/task153/final.json"),
}

def now():
    return datetime.now(ZONE)
def json_out(f,data):
    tmp=f.with_suffix(f.suffix+".tmp")
    tmp.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n")
    tmp.replace(f)
def run(args,**changes):
    return subprocess.run(list(map(str,args)),text=True,capture_output=True,env=ENV,**changes)
def observe():
    lines=Path("/proc/meminfo").read_text().splitlines()
    mem=next(int(v.split()[1])*1024 for v in lines if v.startswith("MemAvailable:"))
    disk=os.statvfs("/home")
    return {"at":now().isoformat(),"mem_available":mem,"home_available":disk.f_bavail*disk.f_frsize}
def check_predecessors():
    p=run([*SYS,"list-units","llvm-opt-151-g-chain*.service","llvm-opt-task153-*.service",
           "--all","--plain","--no-legend","--no-pager"],timeout=20)
    if p.returncode:
        return None,"unit state query failed: "+p.stderr.strip()
    active=[line for line in p.stdout.splitlines() if len(line.split())>=4
            and line.split()[2] not in ("inactive","failed")]
    if active:
        return None,"prerequisite units active: "+", ".join(line.split()[0] for line in active)
    ids={}
    for n,(stamp,path) in CHECKPOINTS.items():
        if not stamp.is_file():
            return None,f"task {n} has not published its final checkpoint"
        rev=stamp.read_text().strip()
        if run([*GIT,"cat-file","-e",f"{rev}:{path}"],timeout=20).returncode:
            return None,f"task {n} published checkpoint has no final receipt"
        ids[n]=rev
    p=run([*GIT,"ls-remote","--exit-code","origin","refs/heads/bolt-v4"],timeout=30)
    if p.returncode:
        return None,"bolt-v4 verification failed: "+p.stderr.strip()
    head=p.stdout.split()[0]
    if run([*GIT,"cat-file","-e",head+"^{commit}"],timeout=20).returncode:
        fetch=run([*GIT,"fetch","--no-tags","--no-write-fetch-head","origin","refs/heads/bolt-v4"],timeout=80)
        if fetch.returncode:
            return None,"bolt-v4 object fetch failed: "+fetch.stderr.strip()
    if any(run([*GIT,"merge-base","--is-ancestor",rev,head],timeout=20).returncode for rev in ids.values()):
        return None,"final receipts are not ancestors of the remote bolt-v4"
    corpus,reason=corpus_terminal(W/"archive/task158/corpus-state.json")
    if corpus is None:
        return None,reason
    return {**ids,"remote_head":head,"158_corpus":corpus},""
def select(last,retry=False):
    plan=admit("N2",last["mem_available"])
    if retry and plan["admitted"]:
        # Lower one 139-D tier after resource failure. With no lower admitted
        # tier, keep the floor and wait for recovery.
        if plan["memory_max"]>=20*GIB:
            plan.update(memory_max=(20*GIB-PAGE),jobs=4,thinlto_jobs=4)
        elif plan["memory_max"]>=14*GIB:
            plan.update(memory_max=(14*GIB-PAGE),jobs=2,thinlto_jobs=2)
    return plan
def record(file,data):
    with file.open("a") as out:
        out.write(json.dumps(data,ensure_ascii=False)+"\n")

def cleanup(d):
    from buildsteps import settle_root
    paths=[d/"gbs-root/local/BUILD-ROOTS/scratch.x86_64.0", d/"runtime-root", d/"tmp"]
    before=observe()
    rows=[]
    for root in paths:
        if not root.exists():
            continue
        try:
            if root.name!="tmp":
                settle_root(root)
            rows.append(prune(root,A))
        except (OSError,ValueError,AssertionError,RuntimeError) as error:
            rows.append({"path":str(root),"remaining":root.exists(),"reason":str(error)})
    after=observe()
    return {"before":before,"after":after,"df_delta":after["home_available"]-before["home_available"],"rows":rows}

def attempt(no,plan,pre,last):
    d=A/f"attempt-{no}"
    d.mkdir()
    unit=UNIT+f"-{no}.service"
    worker_log=d/"service.txt"
    cap,jobs=plan["memory_max"],plan["jobs"]
    stopfile=d/"stop-cgroup.json"
    argv=["/usr/bin/systemd-run","--user","--wait","--pipe","--unit="+unit,
          "--expand-environment=no","-p",f"MemoryMax={cap}","-p","MemorySwapMax=0",
          "-p",f"CPUQuota={jobs*100}%","-p","Nice=19","-p","IOSchedulingClass=idle",
          "-p","OOMPolicy=stop","-p","KillMode=control-group","-p","TimeoutStopSec=120",
          "-p","WorkingDirectory="+str(d),
          "-p",f"ExecStopPost=/usr/bin/python3 -B {ORCH/'capture_stop.py'} {stopfile}",
          "/usr/bin/python3","-B",A/"build.py",d,str(jobs)]
    row={"unit":unit,"prerequisites":pre,"admission":last,"plan":plan,
         "argv":list(map(str,argv)),"start":now().isoformat()}
    json_out(d/"started.json",row)
    t0=time.monotonic()
    watch=None
    with worker_log.open("xb") as f:
        process=subprocess.Popen(list(map(str,argv)),stdout=f,stderr=subprocess.STDOUT,env=ENV)
        while process.poll() is None:
            snapshot=observe()
            record(d/"resources.jsonl",snapshot)
            if watch is None and (stop_line(snapshot) or now()>=DEADLINE):
                state=run([*SYS,"show",unit,"-p","ActiveState","--value"],timeout=15)
                if state.stdout.strip() in ("activating","active","reloading"):
                    stop=run([*SYS,"stop","--no-block",unit],timeout=15)
                    watch={"measurement":snapshot,"deadline":now()>=DEADLINE,
                           "stop":{"rc":stop.returncode,"stdout":stop.stdout,"stderr":stop.stderr}}
            try:
                process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                pass
    stop_data=json.loads(stopfile.read_text()) if stopfile.exists() else {}
    worker=json.loads((d/"worker.json").read_text()) if (d/"worker.json").is_file() else {}
    state=run([*SYS,"show",unit,"-p","Result,MemoryPeak,ActiveState"],timeout=20).stdout
    oom="Result=oom-kill" in state or any(line.split()==["oom_kill", value] and int(value)>0
                                         for line in str(stop_data.get("memory.events","")).splitlines()
                                         for value in line.split()[-1:])
    row.update(end=now().isoformat(),elapsed=round(time.monotonic()-t0,2),rc=process.returncode,
               worker=worker,watchdog=watch,oom=oom,cgroup=stop_data,systemd=state)
    row["status"]="INTERRUPTED" if watch else worker.get("status","FAIL")
    if process.returncode and row["status"] in ("PASS","PARTIAL"):
        row["status"]="FAIL"
    row["cleanup"]=cleanup(d)
    json_out(d/"result.json",row)
    return row

def residual_script(result):
    paths={Path(c["path"]) for row in result["attempts"] for c in row["cleanup"]["rows"]
           if c["remaining"] and Path(c["path"]).exists()}
    if not paths:
        return None
    script=A/"sudo-clean.sh"
    guard=B/"tools/skills/tizen-llvm-offline-profile/scripts/build_cleanup.py"
    fixed=A/"guarded_cleanup.py"
    shutil.copyfile(guard,fixed)
    lines=["#!/bin/sh","set -eu"]
    for p in sorted(paths):
        try:
            confined(p,A)
        except (ValueError,OSError):
            lines.append("# Manual review required for "+str(p))
            continue
        lines.append(shlex.join(["/usr/bin/sudo","/usr/bin/python3","-B",str(fixed),str(A),str(p)]))
    script.write_text("\n".join(lines)+"\n")
    script.chmod(0o755)
    return {"path":str(script),"paths":list(map(str,sorted(paths))),"commands":lines}

def publish(result):
    json_out(A/"final.json",result)
    files=[A/"final.json"]
    if (A/"wait.jsonl").is_file():
        files.append(A/"wait.jsonl")
    if result.get("sudo_cleanup"):
        files.extend((A/"sudo-clean.sh",A/"guarded_cleanup.py"))
    for i,row in enumerate(result["attempts"],1):
        base=A/f"attempt-{i}"
        for p in base.glob("*"):
            if p.is_file():
                files.append(p)
        if (base/"evidence").is_dir():
            files.extend(p for p in (base/"evidence").rglob("*") if p.is_file())
    local=[]
    for p in sorted(set(files)):
        if p.is_symlink():
            continue
        size=p.stat().st_size
        if size>10_000_000:
            with p.open("rb") as f:
                local.append({"path":str(p),"bytes":size,"sha256":hashlib.file_digest(f,"sha256").hexdigest()})
            continue
        dest=R/p.relative_to(A)
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(p,dest)
    json_out(R/"local-files.json",local)
    text=["## B · 完整构建验证","",f"**{result['status']}**。{result.get('reason','')}",""]
    for no,row in enumerate(result["attempts"],1):
        worker=row["worker"]
        text.extend([f"- 第 {no} 轮 {row['start']} → {row['end']}，{row['elapsed']} 秒，"
                     f"档位 {row['plan']['jobs']}/{row['plan']['thinlto_jobs']}/1，"
                     f"MemoryMax {row['plan']['memory_max']:,} B。"
                     f"GBS {worker.get('build','未完成')}，"
                     f"RPM 文件比较 {worker.get('file_comparison','未完成')}。"
                     f"清理前后可用空间差 {row['cleanup']['df_delta']:,} B。",
                     f"- 功能结果 {json.dumps(worker.get('functional',{}),ensure_ascii=False)}。",
                     f"- clang Python 检查 {json.dumps(worker.get('clang_python_checks',{}),ensure_ascii=False)}。",
                     f"- 第 {no} 轮看门狗 {'触发' if row['watchdog'] else '未触发'}。"
                     f"详细原文见 [第 {no} 轮证据](../../tools/bolt/results/task154/attempt-{no}/evidence/)。"])
        for tool in ("analyze-build","intercept-build","scan-build-py"):
            entry=worker.get("functional",{}).get(tool)
            if entry:
                detail=f"；[原文](../../tools/bolt/results/task154/attempt-{no}/evidence/{entry['output']})" if "output" in entry else ""
                text.append(f"- 第 {no} 轮 `{tool} --help` · {entry['status']}{detail}。")
    if result.get("sudo_cleanup"):
        text.append("- 残留由 [sudo 清理脚本](../../tools/bolt/results/task154/sudo-clean.sh) 登记。")
    text.append("[最终回执](../../tools/bolt/results/task154/final.json) · [本地大文件清单](../../tools/bolt/results/task154/local-files.json)")
    src=DOC.read_text()
    if "## B · 完整构建验证" not in src:
        DOC.write_text(src.rstrip()+"\n\n"+"\n".join(text)+"\n")
    def git(*args):
        p=run([*GIT,*args],timeout=240)
        print(p.stdout,p.stderr,flush=True)
        p.check_returncode()
        return p.stdout
    assert git("branch","--show-current").strip()=="bolt-v4"
    assert not git("diff","--cached","--name-only").strip()
    git("add","--",DOC,R)
    git("diff","--cached","--check","--",DOC)
    git("-c","user.name=Hao Lin","-c","user.email=hao.lin@samsung.com","commit","-s","-m",
        "docs: record task 154 full-build and analyzer smoke results")
    git("push","origin","HEAD:refs/heads/bolt-v4")
    rev=git("rev-parse","HEAD").strip()
    assert git("ls-remote","--exit-code","origin","refs/heads/bolt-v4").split()[0]==rev
    (A/"published-final.sha").write_text(rev+"\n")

def main():
    if not (A/"published-static.sha").is_file():
        raise RuntimeError("task 154 static results must be published first")
    result={"status":"SKIPPED","deadline":DEADLINE.isoformat(),"disk_required":DISK,"attempts":[]}
    reason="deadline"
    while now()<DEADLINE:
        last=observe()
        plan=select(last,bool(result["attempts"]))
        try:
            pre,reason=check_predecessors()
        except (OSError,subprocess.SubprocessError,IndexError) as exc:
            pre,reason=None,str(exc)
        if pre and plan["admitted"] and last["home_available"]>=DISK:
            row=attempt(len(result["attempts"])+1,plan,pre,last)
            result["attempts"].append(row)
            result["status"]=row["status"]
            if (len(result["attempts"])==1 and (row["watchdog"] or row["oom"]) and
                    not (row["watchdog"] and row["watchdog"]["deadline"])):
                reason="resource failure; one retry after cleanup and fresh admission"
            else:
                reason=row["worker"].get("error","")
                break
        elif pre:
            reason="waiting for 139-D memory floor or build disk allowance"
        record(A/"wait.jsonl",{**last,"disk_required":DISK,"plan":plan,"reason":reason})
        if now()<DEADLINE:
            time.sleep(max(1,min(300,(DEADLINE-now()).total_seconds())))
    result.update(reason=reason,ended_at=now().isoformat(),sudo_cleanup=residual_script(result))
    publish(result)

if __name__=="__main__":
    main()
