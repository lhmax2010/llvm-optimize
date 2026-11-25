import json, os, subprocess, sys, time
from datetime import datetime
from pathlib import Path

from handoff import cleanup, preserve_clang, save
from policy import DEADLINE, G6_DEADLINE, GIB, ZONE, STEPS, admit, blocked, disk_limits, expired, oom_killed, stop_line, terminal

W,B,A=map(Path,sys.argv[1:4])
SCRIPTS=Path(__file__).resolve().parent
UNIT="llvm-opt-task160-g-chain"
SYS="/usr/bin/systemctl"
RUN="/usr/bin/systemd-run"
GIT="/usr/bin/git"

def stamp():
    return datetime.now(ZONE).isoformat(timespec="seconds")

def read_json(path):
    return json.loads(path.read_text())

def write(path,value):
    tmp=path.with_suffix(path.suffix+".tmp")
    save(tmp,value)
    tmp.replace(path)

def resources():
    mem=next(int(l.split()[1])*1024 for l in Path("/proc/meminfo").read_text().splitlines() if l.startswith("MemAvailable:"))
    v=os.statvfs("/home")
    return {"time":stamp(),"mem_available":mem,"home_available":v.f_bavail*v.f_frsize}

def command(argv,**kwargs):
    return subprocess.run(argv,text=True,capture_output=True,**kwargs)

def append(path,obj):
    with path.open("a") as f:
        f.write(json.dumps(obj,ensure_ascii=False)+"\n")

def cgroup_data(unit):
 prop=command([SYS,"--user","show",unit,"-p","ControlGroup","--value"]).stdout.strip()
 if not prop.startswith("/"):
  return {}
 p=Path("/sys/fs/cgroup")/prop.lstrip("/")
 d={}
 for n in ("memory.peak","memory.max","memory.events","memory.swap.peak","memory.stat"):
  try:
   text=(p/n).read_text()
   if n=="memory.stat": text="\n".join(l for l in text.splitlines() if l.split()[0] in ("anon","file"))
   d[n]=text.strip()
  except OSError: pass
 try:
  local_max={"bytes":0}
  for group in p.rglob("cgroup.procs"):
   for pid in group.read_text().split():
    try:
     proc=Path("/proc")/pid
     st=(proc/"status").read_text()
     n=next((int(l.split()[1])*1024 for l in st.splitlines() if l.startswith("VmHWM:")),0)
     if n>local_max["bytes"]:
      local_max={"bytes":n,"pid":int(pid),"argv":os.fsdecode((proc/"cmdline").read_bytes()).replace("\x00"," ").strip()}
    except OSError: continue
  if local_max["bytes"]: d["VmHWM_sample"]=local_max
 except OSError: pass
 return d

STAGES={"G4":"pgo-build","G5":"bolt-tools-relink","G6":"bolt-instrument-train-merge",
        "G7":"bolt-match","G8":"write-manifest","N2":"full-build"}
ESTIMATES={"G4":"5.5–6.5 hours based on G4 and N2 measurements",
           "G5":"7–11 min for tools plus unmeasured relink",
           "G6":"7m41s historical; admission wait up to 06:00 PST",
           "G7":"minutes for rewrite, plus runtime scan",
           "G8":"no comparable compression measurement"}

def admission_timeout(step):
    return 10800 if step=="G4" else float("inf") if step=="G6" else 3600

def select(step, disk):
    started=time.monotonic()
    checks=[]
    timeout=admission_timeout(step)
    until=G6_DEADLINE if step=="G6" else DEADLINE
    while True:
        observed=resources()
        limit=admit(step,observed["mem_available"])
        observed.update(memory_plan=limit,disk_required=disk,step=step)
        checks.append(observed)
        spent=time.monotonic()-started
        remaining=min(timeout-spent,(until-datetime.now(ZONE)).total_seconds())
        if expired(step,datetime.now(ZONE)):
            return None,"admission deadline reached",checks,spent
        if limit["admitted"] and observed["home_available"]>=disk:
            return limit,"",checks,spent
        reason=", ".join(label for condition,label in (
            (not limit["admitted"],"memory below floor"),(observed["home_available"]<disk,"disk below floor")) if condition)
        if remaining<=0:
            return None,reason,checks,spent
        append(A/"admission-live.jsonl",observed)
        print("WAIT",step,reason,observed,flush=True)
        time.sleep(min(600,remaining))

def merge_stats(stats,fresh):
    for key,value in fresh.items():
        if key=="memory.peak" and int(value)<int(stats.get(key,0)):
            continue
        if key=="VmHWM_sample" and value["bytes"]<stats.get(key,{}).get("bytes",0):
            continue
        if key=="memory.events" and oom_killed(stats,"") and not oom_killed({key:value},""):
            continue
        stats[key]=value

def execute(step,selected,checks,wait,attempt):
    path=A/step
    path.mkdir(exist_ok=True)
    unit=UNIT+"-"+step.lower()+f"-{attempt}.service"
    mem,jobs,tier=(selected[x] for x in ("memory_max","jobs","tier"))
    cpu=jobs*100 if jobs>1 else 200
    stop_snapshot=path/f"cgroup-stop-{attempt}.json"
    argv=[RUN,"--user","--wait","--pipe","--unit="+unit,"--expand-environment=no",
          "-p","MemoryMax="+str(mem),"-p","MemorySwapMax=0","-p","CPUQuota="+str(cpu)+"%",
          "-p","Nice=19","-p","IOSchedulingClass=idle","-p","OOMPolicy=stop","-p","KillMode=control-group",
          "-p","TimeoutStopSec=120","-p","WorkingDirectory="+str(path),
          "-p",f"ExecStopPost=/usr/bin/python3 -B {SCRIPTS/'capture_stop.py'} {stop_snapshot}",
          "--setenv=TZ=America/Los_Angeles","--setenv=TASK133_WORKSPACE="+str(W),
          "--setenv=TASK138_UNIT="+unit.removesuffix(".service"),
          "--setenv=TASK133_ADMISSION_MEMORY="+str(checks[-1]["mem_available"]),
          "/usr/bin/python3","-B",str(SCRIPTS/"worker.py"),str(A),step,tier,str(jobs),str(mem),str(cpu)]
    row={"step":step,"attempt":attempt,"started_at":stamp(),**selected,"cpu_percent":cpu,
         "admission":checks,"admission_wait_seconds":round(wait,3),"unit":unit,"argv":argv}
    write(path/"started.json",row)
    print("START",step,tier,checks[-1],flush=True)
    t0=time.monotonic()
    stats={}
    watchdog=None
    next_watchdog=t0
    deadline_stop=None
    logpath=path/("service.log" if attempt==1 else f"service-{attempt}.log")
    with logpath.open("xb") as f:
        process=subprocess.Popen(argv,stdout=f,stderr=subprocess.STDOUT)
        while True:
            snapshot=resources()
            readings=cgroup_data(unit)
            merge_stats(stats,readings)
            snapshot.update(readings)
            if time.monotonic()>=next_watchdog or process.poll() is not None:
                append(path/"resources.jsonl",snapshot)
            if process.poll() is not None:
                break
            now=time.monotonic()
            if now>=next_watchdog:
                next_watchdog=now+30
                # systemd-run starts asynchronously. Only issue stop after this child exists.
                if readings and datetime.now(ZONE)>=DEADLINE and deadline_stop is None:
                    deadline_stop=snapshot
                    command([SYS,"--user","stop","--no-block",unit],timeout=15)
                if readings and stop_line(snapshot) and watchdog is None:
                    watchdog=snapshot
                    stop=command([SYS,"--user","stop","--no-block",unit],timeout=15)
                    row["stop_command"]={"rc":stop.returncode,"stdout":stop.stdout,"stderr":stop.stderr}
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                pass
    rc=process.returncode
    systemd=command([SYS,"--user","show",unit,"-p","Result,MemoryPeak,CPUUsageNSec,ActiveState,InvocationID"],timeout=15).stdout
    if stop_snapshot.is_file():
        merge_stats(stats,json.loads(stop_snapshot.read_text()))
    identity=path/"worker.json"
    worker=json.loads(identity.read_text()) if identity.is_file() else {}
    merge_stats(stats,worker.get("cgroup_end",{}))
    watchdog=watchdog or worker.get("details",{}).get("watchdog")
    outcome=worker.get("status","FAIL")
    if (outcome=="STOP" and not worker.get("pgo_ninja_violations")) or (rc and outcome=="PASS"):
        outcome="FAIL"
    killed=oom_killed(stats,systemd)
    outcome,reason=terminal(step,tier,outcome,watchdog,killed)
    if deadline_stop is not None and watchdog is None:
        outcome,reason="INTERRUPTED","overall deadline reached during this step"
    if deadline_stop is not None:
        row["deadline_stop"]=deadline_stop
    with logpath.open("rb") as stream:
        stream.seek(max(0,logpath.stat().st_size-16000))
        tail=stream.read().decode(errors="replace")
    row.update(status=outcome,reason=reason or worker.get("reason","") or
               (f"child exited {rc} ({systemd.splitlines()[0] if systemd else 'no systemd result'})" if rc else ""),
               rc=rc,ended_at=stamp(),seconds=round(time.monotonic()-t0,3),resources=stats,
               systemd=systemd,worker=worker,watchdog=watchdog,oom_killed=killed,
               log_path=str(logpath),log_tail=tail,end_measurement=resources())
    return row

def finish_stage(row):
    step=row["step"]
    path=A/step
    if not path.exists():
        return
    begin=resources()
    result=[]
    try:
        if step=="G4" and row["status"]=="PASS":
            row["retained_clang"]=preserve_clang(A)
            item=path/"BUILDROOT-cleanup.json"
            if item.exists():
                result.append(json.loads(item.read_text()))
        # G4's scratch name is absent after the verified handoff. Only G5 owns
        # the moved scratch. Later stages consume copied tools and libraries.
        result.extend(cleanup(path,A))
    except Exception as exc:
        row["cleanup_error"]=f"{type(exc).__name__}: {exc}"
        if row["status"]=="PASS":
            row.update(status="FAIL",reason=row["cleanup_error"])
    after=resources()
    row["cleanup"]={"roots":result,"before":begin,"after":after,"df_delta":after["home_available"]-begin["home_available"],
                    "estimated_allocated_bytes_removed":sum(x["estimated_allocated_bytes_removed"] for x in result)}

def main():
    peak=222650722030
    previous=B/"tools/bolt/results/task150"
    recipe=(A/"recipe.sha").read_text().strip()
    preview=read_json(previous/"preview-summary.json")["second"]
    original=(previous/"recipe-final.sha").read_text().strip()
    gate=read_json(A/"154-gate.json")
    delta=command([GIT,"-C",str(W/"temp/task131/pgo-dev"),"diff","--name-only",original,recipe],check=True).stdout.splitlines()
    patch=command([GIT,"-C",str(W/"temp/task131/pgo-dev"),"diff","--unified=0",original,recipe,"--","packaging/llvm.spec"],check=True).stdout
    if (preview["violation_count"]!=0 or
        delta!=["packaging/llvm-static-archives-native.py","packaging/llvm.spec"] or
        len([line for line in patch.splitlines() if line.startswith("+    --jobs 4 --address-space-bytes 4294967296 --retry-address-space-bytes 8589934592")])!=2):
        raise RuntimeError("the converter-only recipe delta no longer matches the earlier configure validation")
    disks=disk_limits(peak)
    init=resources()
    startup={"unit":UNIT+".service","startup":init,"peak_growth":peak,"disks":disks,
             "deadline":DEADLINE.isoformat(),"g6_deadline":G6_DEADLINE.isoformat(),"estimates":ESTIMATES,
             "recipe":recipe,"reused_preview":preview,"154_gate":gate,
             "projected":{step:admit(step,init["mem_available"]) for step in STEPS}}
    write(A/"startup.json",startup)
    from delivery import publish
    statuses=[]
    g_failed=False
    for step in STEPS:
        if not gate["admitted"]:
            row={"step":step,"status":"SKIPPED","reason":gate["reason"],
                 "admission":[resources()],"admission_wait_seconds":0,"ended_at":stamp()}
        elif blocked(step,g_failed):
            row={"step":step,"status":"SKIPPED","reason":"G chain prerequisite did not pass",
                 "admission":[resources()],"admission_wait_seconds":0,"ended_at":stamp()}
        else:
            plan,reason,checks,wait=select(step,disks[step])
            if plan is None:
                row={"step":step,"status":"SKIPPED","reason":reason,
                     "admission":checks,"admission_wait_seconds":round(wait,3),"ended_at":stamp()}
            else:
                try:
                    row=execute(step,plan,checks,wait,1)
                except Exception as exc:
                    row={"step":step,"status":"FAIL","reason":f"{type(exc).__name__}: {exc}",
                         "admission":checks,"admission_wait_seconds":round(wait,3),"ended_at":stamp()}
                    own_unit=UNIT+"-"+step.lower()+"-1.service"
                    command([SYS,"--user","stop",own_unit],timeout=140)
                if step=="G4":
                    scope=A/step
                    scratch=scope/"gbs-root/local/BUILD-ROOTS/scratch.x86_64.0"
                    # After a watchdog stop the worker may not have copied
                    # the RPM log yet. The chroot log is still retained.
                    paths=(scope/"rpm-build.log",scratch/".build.log")
                    lines=[]
                    for log in paths:
                        if log.is_file():
                            with log.open(errors="replace") as stream:
                                lines.extend(line.rstrip("\n") for line in stream
                                             if "ARCHIVE_MEMBER_RETRY " in line and "echo " not in line)
                    lines=list(dict.fromkeys(lines))
                    (scope/"member-retries.log").write_text("".join(line+"\n" for line in lines))
                    row["archive_member_retries"]=lines
                    native=scratch/"home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/native-archive-conversion"
                    receipts=[]
                    for archive in sorted({line.split("ARCHIVE_MEMBER_RETRY ",1)[1].split()[0] for line in lines}):
                        rel=Path(archive)
                        if rel.is_absolute() or ".." in rel.parts:
                            continue
                        for receipt in sorted((native/"members"/rel).glob("*/convert-retry.json")):
                            result=read_json(receipt)
                            receipts.append({"archive":archive,"member":Path(result["argv"][-1]).name,
                                             "record_path":str(receipt),"record":result})
                    if receipts:
                        write(scope/"member-retry-receipts.json",receipts)
                finish_stage(row)
        if row["status"]!="PASS":
            g_failed=True
        statuses.append(row)
        write(A/(step+".json"),row)
        print("FINISH",step,row["status"],row.get("reason",""),flush=True)
        publish(W,B,A,step,statuses)
    write(A/"summary.json",{"startup":startup,"rows":statuses,"end":resources(),
                            "watchdog_triggered":any(r.get("watchdog") for r in statuses)})
    publish(W,B,A,"summary",statuses)

if __name__=="__main__":
    main()

