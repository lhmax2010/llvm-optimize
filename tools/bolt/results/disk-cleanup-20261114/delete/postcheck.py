#!/usr/bin/env python3
import pathlib,json,subprocess,datetime,os
D=pathlib.Path(__file__).parent;E=D.parent
W=pathlib.Path("/home/linhao/Toolchain/development/llvm-optimize")
def save(n,v):(D/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n")
checks=json.loads((D/"check02/originals-before.json").read_text())["checks"]
for r in checks:
 p=pathlib.Path(r["path"]);actual=p.stat().st_size if p.is_file() else None
 r["after_bytes"]=actual
 r["after_ok"]=p.is_file() and (actual==r["expected_bytes"] if r["expected_bytes"] is not None else actual==r["actual_bytes"])
critical=["deleted-repo-backup-20261105","local-full-r6-20261111-materials","qb-1226850-1226851/1226850","qb-1226850-1226851/1226851","qb-1225393-1225395","night-20261103","night-20261105","fifth-review-20261111/rerun3/debug-inputs","tu-inputs-restored-20261106","pgo-profiles-keep-20261102"]
baselines={}
for line in (E/"measurements.jsonl").read_text().splitlines():
 r=json.loads(line)
 if r["size_bytes"] is not None:baselines[r["path"]]=r["size_bytes"]
 for x in r["children"]:baselines[x["path"]]=x["size_bytes"]
roots=[]
for rel in critical:
 p=W/"temp"/rel;r={"path":str(p),"exists":p.is_dir(),"same_realpath":str(p.resolve())==str(p)}
 if rel not in ["night-20261103","night-20261105"]:
  try:
   q=subprocess.run(["du","-x","-s","-B1","--",str(p)],capture_output=True,text=True,timeout=120)
   actual=int(q.stdout.split()[0]) if q.returncode==0 else None
   r.update(du_rc=q.returncode,du_stdout=q.stdout,du_stderr=q.stderr,expected_allocated_bytes=baselines.get(str(p)),actual_allocated_bytes=actual,size_match=actual==baselines.get(str(p)) and actual is not None)
  except subprocess.TimeoutExpired:r.update(du_status="UNKNOWN:120s timeout")
 else:r["size_sample"]="Verified original RPM/DWARF/tool files individually; full root du not repeated"
 roots.append(r);save("protected-roots-after.json",roots)
siblings=[]
for parent,rs in json.loads((D/"check02/parent-siblings-before.json").read_text()).items():
 for r in rs:
  p=pathlib.Path(r["path"]);exists=p.exists() or p.is_symlink()
  ok=exists and p.lstat().st_ino==r["inode"]
  if r["type"]!="directory":ok=ok and p.lstat().st_size==r["size"]
  siblings.append({**r,"preserved":ok})
missing=[r["path"] for r in json.loads((D/"approved-paths.json").read_text()) if pathlib.Path(r["path"]).exists()]
q=subprocess.run(["df","-B1","/home"],capture_output=True,text=True)
result={"time":datetime.datetime.now().astimezone().isoformat(),"originals":checks,"roots":roots,"siblings":siblings,"approved_paths_still_present":missing,"df":{"stdout":q.stdout,"stderr":q.stderr,"rc":q.returncode,"available_bytes":int(q.stdout.splitlines()[1].split()[3])},"pass":all(x["after_ok"] for x in checks) and all(x["exists"] and x["same_realpath"] and x.get("size_match",True) for x in roots) and all(x["preserved"] for x in siblings) and not missing}
save("postcheck.json",result)
print("ORIGINALS",sum(x["after_ok"] for x in checks),"/",len(checks),"SIBLINGS",sum(x["preserved"] for x in siblings),"/",len(siblings),flush=True)
print(q.stdout,flush=True)
print("98步骤3 已结束",result["time"],"status="+("PASS" if result["pass"] else "STOP"),flush=True)
