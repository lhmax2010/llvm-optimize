from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import hashlib,json,os,shutil,subprocess,time

A=Path("/home/linhao/Toolchain/development/llvm-optimize/archive/task153")
W=A.parents[1]
B=W.with_name(W.name+"-bolt")
E=A/"evidence"
Previous=W/"archive/task151"
DELIVERY=B/"tools/bolt/results/task153"
DOC=B/"docs/bolt/153_ps6_suggestions.md"
GIT=["/usr/bin/git","-C",str(B)]
SYSTEM=["/usr/bin/systemctl","--user"]
ENV={**os.environ,"GIT_TERMINAL_PROMPT":"0","LC_ALL":"C"}
ZONE=ZoneInfo("America/Los_Angeles")
DEADLINE=datetime(2026,11,26,20,tzinfo=ZONE)
GIB=2**30
DISK_PROXY=17_143_382_016
DISK_FLOOR=(23*DISK_PROXY+19)//20+15*GIB+30_000_000_000

def now():
    return datetime.now(ZONE)

def proc(argv,**kw):
    return subprocess.run(list(map(str,argv)),text=True,capture_output=True,env=ENV,**kw)

def save(p,body):
    t=p.with_suffix(p.suffix+".tmp")
    t.write_text(json.dumps(body,indent=2,ensure_ascii=False)+"\n")
    t.replace(p)

def measures():
    memory=next(int(l.split()[1])*1024 for l in Path("/proc/meminfo").read_text().splitlines() if l.startswith("MemAvailable:"))
    v=os.statvfs("/home")
    cap=max(0,min(memory-4*GIB,24*GIB))//os.sysconf("SC_PAGE_SIZE")*os.sysconf("SC_PAGE_SIZE")
    jobs=6 if cap>=20*GIB else 4 if cap>=14*GIB else 2
    return {"at":now().isoformat(),"mem_available":memory,"home_available":v.f_bavail*v.f_frsize,
            "memory_max":cap,"jobs":jobs,"thinlto_jobs":jobs,"link_jobs":1,
            "home_required":DISK_FLOOR,"memory_floor":10*GIB}

def proof():
    query=proc([*SYSTEM,"list-units","llvm-opt-151-g-chain*.service","--all","--plain","--no-legend","--no-pager"])
    if query.returncode:
        return None,"task 151 unit status unavailable"
    for row in query.stdout.splitlines():
        fields=row.split()
        if len(fields)>=4 and fields[2] not in ("inactive","failed"):
            return None,"active task 151 unit: "+row
    if not (Previous/"published-summary.sha").is_file() or not (Previous/"summary.json").is_file():
        return None,"task 151 summary not yet published"
    stamp=(Previous/"published-summary.sha").read_text().strip()
    p=proc([*GIT,"ls-remote","--exit-code","origin","refs/heads/bolt-v4"],timeout=25)
    if p.returncode or not p.stdout.strip():
        return None,"could not read bolt-v4 remote"
    head=p.stdout.split()[0]
    c=proc([*GIT,"merge-base","--is-ancestor",stamp,head])
    if c.returncode:
        return None,"task 151 summary not verified on remote branch"
    return {"after":str(Previous/"summary.json"),"task151_summary_commit":stamp,"remote_head":head},""

def run(key,path,args,cap,cpu):
    unit=f"llvm-opt-task153-{key}.service"
    log=A/(key+"-service.txt")
    argv=["/usr/bin/systemd-run","--user","--wait","--pipe","--unit="+unit,
         "-p","WorkingDirectory="+str(path),"-p","MemoryMax="+str(cap),
         "-p","MemorySwapMax=0","-p","Nice=19","-p","IOSchedulingClass=idle",
         "-p","OOMPolicy=stop","-p","KillMode=control-group","-p","CPUQuota="+str(cpu)+"%",
         *args]
    stamp=now().isoformat()
    reason=None
    with log.open("xb") as stream:
        p=subprocess.Popen(list(map(str,argv)),stdout=stream,stderr=subprocess.STDOUT,env=ENV)
        while p.poll() is None:
            m=measures()
            if now()>=DEADLINE or m["mem_available"]<3*GIB or m["home_available"]<15*GIB:
                reason={"why":"deadline" if now()>=DEADLINE else "resource watchdog",**m}
                stop=proc([*SYSTEM,"stop","--no-block",unit],timeout=30)
                reason.update(stop_rc=stop.returncode,stop_stderr=stop.stderr)
                if stop.returncode==0:
                    try:
                        p.wait(timeout=150)
                    except subprocess.TimeoutExpired:
                        proc([*SYSTEM,"stop",unit],timeout=140)
                    break
            try:
                p.wait(timeout=30)
            except subprocess.TimeoutExpired:
                pass
    return {"unit":unit,"start":stamp,"end":now().isoformat(),"rc":p.wait(),
            "interruption":reason,"status":"FAIL" if reason or p.returncode else "PASS","argv":list(map(str,argv))}

def package(root,source):
    if not source.is_file():
        return None
    size=source.stat().st_size
    with source.open("rb") as f: digest=hashlib.file_digest(f,"sha256").hexdigest()
    if size>10_000_000:
        return {"path":str(source),"bytes":size,"sha256":digest}
    target=DELIVERY/root/source.name
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,target)
    return None

def deliver(result):
    save(A/"final.json",result)
    extra=[]
    for p in (A/"final.json",A/"transactions-service.txt",A/"standalone-service.txt",A/"wait.jsonl"):
        maybe=package(Path(),p)
        if maybe: extra.append(maybe)
    for d in ("transactions","standalone"):
        where=A/d
        if not where.is_dir(): continue
        for p in sorted(where.glob("*.json")):
            maybe=package(Path(d),p)
            if maybe: extra.append(maybe)
        for p in sorted(where.glob("*.txt")):
            maybe=package(Path(d),p)
            if maybe: extra.append(maybe)
    for p in sorted((A/"standalone/evidence").glob("*")):
        maybe=package(Path("standalone/evidence"),p)
        if maybe: extra.append(maybe)
    if extra:
        save(DELIVERY/"local-logs.json",extra)
    raw=DOC.read_text()
    update="\n## 最终事务与构建结果\n\n"
    txn=result["transactions"]
    st=result["standalone"]
    update+=f"- RPM 哑包事务 {txn['status']}。"+(txn.get("reason",""))+"\n"
    if (A/"transactions/result.json").is_file():
        t=json.loads((A/"transactions/result.json").read_text())
        for row in t.get("cases",[]):
            update+="  - "+json.dumps(row,ensure_ascii=False)+"\n"
        update+="- libsolv "+t.get("testsolv",{}).get("state","SKIPPED")+"。\n"
        update+="[事务原文](../../tools/bolt/results/task153/transactions/commands.json)\n"
    update+=f"- 145 B2 同款 standalone {st['status']}。"+st.get("reason","")+"\n"
    if st['status']=="PASS" and (A/"standalone/result.json").is_file():
        build=json.loads((A/"standalone/result.json").read_text())
        audit=build["audit"]
        update+=f"- bolt RPM {audit['file_count']} 个路径与 145 B2 相同。llvm-bolt --version 通过，注册了 x86-64 和 aarch64。镜像编译单元有实测对象。\n"
    elif st['status']=="SKIPPED":
        update+="- 补丁 3 未经编译验证。\n"
    if result.get("prerequisite"):
        update+="- 已核对远端包含 151 汇总 "+result["prerequisite"]["task151_summary_commit"]+"。\n"
    update+="\n[最终状态及证据索引](../../tools/bolt/results/task153/final.json)\n"
    if "\n## 最终事务与构建结果\n" not in raw:
        DOC.write_text(raw.rstrip()+"\n"+update)
    for argv in (["branch","--show-current"],["diff","--cached","--name-only"]):
        q=proc([*GIT,*argv])
        if q.returncode or (q.stdout.strip()!="bolt-v4" if argv[0]=="branch" else bool(q.stdout.strip())):
            raise RuntimeError("evidence branch/index changed")
    for args in (["add","--",DOC,DELIVERY],["diff","--cached","--check","--",DOC],
                 ["-c","user.name=Hao Lin","-c","user.email=hao.lin@samsung.com","commit","-s","-m",
                  "docs: finalize task 153 transaction and standalone checks"],
                 ["push","origin","HEAD:refs/heads/bolt-v4"]):
        p=proc([*GIT,*args],timeout=180)
        print(p.stdout,p.stderr,flush=True)
        if p.returncode: raise RuntimeError("evidence git failed: "+str(args))
    p=proc([*GIT,"ls-remote","--exit-code","origin","refs/heads/bolt-v4"],timeout=30)
    rev=proc([*GIT,"rev-parse","HEAD"]).stdout.strip()
    assert p.returncode==0 and p.stdout.split()[0]==rev,p.stdout
    (A/"published-final.sha").write_text(rev+"\n")

def main():
    if not (A/"published-static.sha").is_file():
        raise RuntimeError("task 153 static evidence is not published")
    evidence={"not_before_task151":True,"standalone_deadline":DEADLINE.isoformat(),
              "disk":{"conservative_145_archive_allocation":DISK_PROXY,"floor":DISK_FLOOR}}
    tx=None
    st=None
    reason=""
    last=None
    prerequisite=None
    while now()<DEADLINE:
        last=measures()
        try:
            prerequisite, reason=proof()
        except (OSError,subprocess.TimeoutExpired) as ex:
            prerequisite=None
            reason=str(ex)
        if prerequisite:
            if tx is None and last["mem_available"]>=4*GIB:
                tx=run("transactions",A,["/usr/bin/python3","-B",A/"transactions.py"],1*GIB,100)
                if (A/"transactions/result.json").is_file():
                    tx["result"]=str(A/"transactions/result.json")
                last=measures()
            if tx and now()<DEADLINE and last["memory_max"]>=10*GIB and last["home_available"]>=DISK_FLOOR:
                check,_=proof()
                if not check:
                    continue
                d=A/"standalone"
                d.mkdir()
                st=run("standalone",d,["/usr/bin/python3","-B",A/"build_standalone.py",d,last["jobs"]],
                       last["memory_max"],last["jobs"]*100)
                st["admission"]=last
                if (d/"result.json").is_file():
                    body=json.loads((d/"result.json").read_text())
                    st["product"]=body
                    if body.get("error"):st["reason"]=body["error"]
                break
            reason="standalone disk or memory admission pending"
        with (A/"wait.jsonl").open("a") as f:
            f.write(json.dumps(dict(last,reason=reason,task151=prerequisite))+"\n")
        time.sleep(max(1,min(300,(DEADLINE-now()).total_seconds())))
    evidence.update(prerequisite=prerequisite,
             transactions=tx or {"status":"SKIPPED","reason":reason or "deadline"},
             standalone=st or {"status":"SKIPPED","reason":reason or "deadline","last_measurement":last},
             finished_at=now().isoformat())
    deliver(evidence)

if __name__=="__main__":main()
