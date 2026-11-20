from pathlib import Path
import hashlib,json,sys

w=Path("/home/linhao/Toolchain/development/llvm-optimize")
b=w.with_name(w.name+"-bolt")
a=w/"archive/task144"
d=Path(sys.argv[1])
sys.path.insert(0,str(b/"tools/bolt/rebase-launch-20261111-r6/toolchain"))
from rpm_io import manifest

def sha(p):
    with p.open("rb") as f:
        return hashlib.file_digest(f,"sha256").hexdigest()

current=json.loads((a/"b1-a1/evidence/rpms.json").read_text())
qb=b/"tools/bolt/results/qb-1232862-1232863"
plan=json.loads((qb/"rpm-plan.json").read_text())
o,=[row for row in plan if row["build"]=="1232863" and row["arch"]=="x86_64" and row["name"].startswith("llvm-debugsource-")]
n,=[row for row in current if Path(row["path"]).name.startswith("llvm-debugsource-")]
p=Path(o["path"])
if not p.is_file():
    p=w/"temp/keep-baselines/qb-1232862-1232863/1232863/x86_64/rpms"/o["name"]
q=Path(n["path"])
expect=json.loads((qb/"downloads/1232863/x86_64"/(o["name"]+".json")).read_text())["sha256"]
assert sha(p)==expect and sha(q)==n["sha256"]
def read(r,rel):
    prefix=f"usr/src/debug/llvm-22.1.8-{rel}.x86_64"
    outside={}
    inside={}
    for path,row in manifest(r).items():
        row={n:row[n] for n in ("mode","uid","gid","bytes","sha256","target") if n in row}
        if path==prefix or path.startswith(prefix+"/"):
            inside[path[len(prefix):]]=row
        else:
            outside[path]=row
    return inside,outside
lo,lx=read(p,"2.1")
hi,hx=read(q,"1")
delta=[{"name":key,"old":lo.get(key),"new":hi.get(key)} for key in sorted(lo.keys()|hi.keys()) if lo.get(key)!=hi.get(key)]
outside=[{"name":key,"old":lx.get(key),"new":hx.get(key)} for key in sorted(lx.keys()|hx.keys()) if lx.get(key)!=hx.get(key)]
r={"status":"PASS" if not delta and not outside else "STOP","rpm_old":str(p),"rpm_old_sha256":expect,
   "rpm_new":str(q),"rpm_new_sha256":n["sha256"],"old_paths":len(lo),"new_paths":len(hi),
   "unmodified_raw_link_targets_checked":sum("target" in row for row in lo.values()),
   "compared_fields":["relative path","mode","uid","gid","bytes","sha256","raw link target"],
   "prefix_differences":delta,"other_differences":outside}
(d/"result.json").write_text(json.dumps(r,indent=2)+"\n")
print(r,flush=True)
sys.exit(r["status"]!="PASS")
