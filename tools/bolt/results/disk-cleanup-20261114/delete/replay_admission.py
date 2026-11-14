#!/usr/bin/env python3
import pathlib,json,re,subprocess,datetime,shutil
D=pathlib.Path(__file__).parent
post=json.loads((D/"postcheck.json").read_text())
assert post["pass"],"STOP: post-cleanup preservation checks failed"
rows=[];blind=[]
for p in pathlib.Path("/proc").iterdir():
 if not p.name.isdigit():continue
 try:
  comm=(p/"comm").read_text().strip()
  if comm not in ("gbs","rpmbuild","ninja","llvm-bolt"):continue
  rows.append({"pid":int(p.name),"comm":comm,"cmdline":(p/"cmdline").read_bytes().replace(b"\0",b" ").decode(errors="replace"),"cgroup":(p/"cgroup").read_text()})
 except PermissionError:blind.append(p.name)
 except FileNotFoundError:pass
mem=pathlib.Path("/proc/meminfo").read_text()
avail=int(re.search(r"^MemAvailable:\s+(\d+)",mem,re.M)[1])*1024
free=shutil.disk_usage("/home").free
reasons=[]
if rows:reasons.append("other gbs/rpmbuild/ninja/llvm-bolt heavy processes are running")
if avail<20*1024**3:reasons.append("MemAvailable below20GiB")
if free<30*1024**3:reasons.append("/home available below30GiB")
out={"time":datetime.datetime.now().astimezone().isoformat(),"status":"SKIPPED" if reasons else "READY_FOR_LOCK_CHECK","reasons":reasons,"heavy_processes":rows,"permission_blind_spots":blind,"MemAvailable_bytes":avail,"home_available_bytes":free,"shared_lock":"NOT ATTEMPTED: other precondition failed" if reasons else "NOT YET CHECKED; must acquire immediately within replay service before running","replay_executed":False}
(D/"replay-admission.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
(D/"admission-meminfo.txt").write_text(mem)
print(json.dumps(out,ensure_ascii=False,indent=2),flush=True)
print("98步骤4准入 已结束",out["time"],"status="+out["status"],flush=True)
