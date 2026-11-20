from datetime import datetime
from pathlib import Path
import json
import subprocess
import sys
import time

base = Path(__file__).resolve().parent
name, series, entry = sys.argv[1:]
gib = 2**30
sysctl = "/usr/bin/systemctl"
def now():
    return datetime.now().astimezone().isoformat(timespec="seconds")
def available():
    return next(int(line.split()[1])*1024 for line in Path("/proc/meminfo").read_text().splitlines()
                if line.startswith("MemAvailable:"))
def show(unit):
    p = subprocess.run([sysctl,"--user","show",unit,"-p","ActiveState,MemoryPeak,Result,ControlGroup"],
                       text=True,capture_output=True)
    return dict(l.split("=",1) for l in p.stdout.splitlines() if "=" in l)
def save(p, row):
    p.write_text(json.dumps(row,indent=2)+"\n")
attempts = []
ceiling = (12 if name == "b2" else 4) * gib
for attempt in range(1,4):
    mem = available()
    if mem < 2*gib:
        attempts.append({"status":"STOP","error":"launch below host MemAvailable protection line","mem_available":mem})
        break
    cap = max(512*2**20,min(ceiling,mem-(4*gib if name=="b2" else 3*gib)))//4096*4096
    jobs = 2 if name=="b2" and cap>=8*gib and attempt==1 else 1
    work = base/f"{name}-{series}-a{attempt}"
    work.mkdir()
    unit = f"llvm-opt-task145-{work.name}.service"
    argv = ["/usr/bin/systemd-run","--user","--wait","--pipe","--unit="+unit,
            "-p","WorkingDirectory="+str(work),"-p","MemoryMax="+str(cap),
            "-p","MemorySwapMax=0","-p","Nice=19","-p","IOSchedulingClass=idle","-p","OOMPolicy=stop",
            "-p","KillMode=control-group","-p","TimeoutStopSec=120",
            "/usr/bin/python3","-B",entry,str(work),str(jobs)]
    row = {"unit":unit,"at":now(),"mem_available":mem,"memory_max":cap,"jobs":jobs,"directory":str(work),"argv":argv}
    save(work/"resources.json",row)
    print(json.dumps(row),flush=True)
    minimum = mem
    interrupted = False
    t = time.monotonic()
    with (work/"service.txt").open("w") as log:
        proc = subprocess.Popen(argv,stdout=log,stderr=subprocess.STDOUT)
        while proc.poll() is None:
            m = available()
            minimum = min(minimum,m)
            if m < 2*gib:
                stop = subprocess.run([sysctl,"--user","stop",unit],capture_output=True,text=True,timeout=140)
                save(work/"watchdog-stop.json",{"at":now(),"mem_available":m,"threshold":2*gib,"unit":unit,
                     "rc":stop.returncode,"stdout":stop.stdout,"stderr":stop.stderr})
                proc.wait(timeout=140)
                interrupted = True
                break
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                pass
    result = work/"result.json"
    row.update(rc=proc.returncode,minimum=minimum,end=now(),seconds=round(time.monotonic()-t,2),systemd=show(unit),
               result=json.loads(result.read_text()) if result.exists() else None,
               status="INTERRUPTED" if interrupted else "PASS" if proc.returncode==0 else "STOP")
    save(work/"resources.json",row)
    attempts.append(row)
    if not interrupted:
        break
    ceiling = max(512*2**20,cap-(4 if name=="b2" else 1)*gib)
save(base/(name+"-"+series+"-sequence.json"),attempts)
sys.exit(attempts[-1]["status"]!="PASS")
