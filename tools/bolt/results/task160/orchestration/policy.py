from datetime import datetime
from zoneinfo import ZoneInfo
import os

GIB = 2**30
PAGE = os.sysconf("SC_PAGE_SIZE")
RESERVE = 15*GIB + 30_000_000_000
ZONE = ZoneInfo("America/Los_Angeles")
DEADLINE = datetime(2026,11,27,20,tzinfo=ZONE)
G6_DEADLINE = datetime(2026,11,27,6,tzinfo=ZONE)
STEPS = ("G4","G5","G6","G7","G8")
FLOORS = {"G4":10*GIB, "G5":15*GIB, "N2":10*GIB, "G7":9*GIB, "G8":GIB}
STAGE_PEAK = {"G5":30*GIB, "G6":4_948_119_552, "G7":6*GIB, "G8":2*GIB}

def floor_disk(growth, margin=False):
    return ((23*growth+19)//20 if margin else growth)+RESERVE

def disk_limits(peak):
    return {step:floor_disk(peak,True) if step in ("G4","N2") else floor_disk(STAGE_PEAK[step])
            for step in STEPS}

def admit(step, available):
    cap=max(0,min(available-4*GIB,24*GIB))//PAGE*PAGE
    tier="dynamic"
    if step=="G6":
        if available>=22*GIB:
            tier="preferred"
            minimum=18*GIB
        else:
            tier="fallback"
            minimum=16*GIB
            cap=max(0,available-7*GIB//2)//PAGE*PAGE
    else:
        minimum=FLOORS[step]
    jobs=(6 if cap>=20*GIB else 4 if cap>=14*GIB else 2) if step in ("G4","G5","N2") else 1
    return dict(memory_max=cap, floor=minimum, admitted=cap>=minimum, tier=tier, jobs=jobs,
                thinlto_jobs=jobs if step in ("G4","G5","N2") else None,
                link_jobs=1 if step in ("G4","G5","N2") else None)

def expired(step, now):
    return now >= (G6_DEADLINE if step=="G6" else DEADLINE)

def stop_line(snapshot):
    return snapshot["mem_available"]<3*GIB or snapshot["home_available"]<15*GIB

def oom_killed(stats,systemd):
    return ("Result=oom-kill" in systemd or
            any(line.split()[0]=="oom_kill" and int(line.split()[1])>0
                for line in stats.get("memory.events","").splitlines() if line.split()))

def terminal(step, tier, status, watchdog, oom):
    if step=="G6" and tier=="fallback" and oom:
        return "FAIL","fallback cgroup OOM; no retry"
    if watchdog:
        return "INTERRUPTED","watchdog stopped only this step"
    return status, ""

def blocked(step, g_failed):
    return g_failed

