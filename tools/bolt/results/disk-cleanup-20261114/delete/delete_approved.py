#!/usr/bin/env python3
import pathlib,json,subprocess,datetime,os,hashlib,importlib.util
D=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location("preflight98",D/"preflight.py")
pf=importlib.util.module_from_spec(spec);spec.loader.exec_module(pf)
def now():return datetime.datetime.now().astimezone().isoformat()
def save(n,v):(D/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n")
def df():
 r=pf.run(["df","-B1","/home"])
 if r["rc"]==0:r["available_bytes"]=int(r["stdout"].splitlines()[1].split()[3])
 return r
approved=json.loads((D/"approved-paths.json").read_text())
checks=json.loads((D/"check02/preflight.json").read_text())
assert [x["path"] for x in checks]==[x["path"] for x in approved]
assert all(x["status"]=="READY" for x in checks)
assert json.loads((D/"check02/originals-before.json").read_text())["pass"]
out=[]
for r in checks:
 result={"number":r["number"],"path":r["path"],"allocated_bytes_before":r["actual_bytes"],"time_start":now()}
 p=pathlib.Path(r["path"]);reason=None
 if not p.is_dir() or p.is_symlink() or str(p.resolve())!=str(p):reason="STOP: path identity changed after preflight"
 else:
  st=p.lstat()
  if (st.st_dev,st.st_ino)!=(r["identity"]["device"],r["identity"]["inode"]):reason="STOP: inode changed after preflight"
 occ=pf.occupied([str(p)]);result["occupancy_immediate"]=occ
 if occ["rc"]!=0 or occ["hits"]:reason="SKIP: immediate occupancy check failed or process found"
 mrc,m=pf.mounts()
 if mrc!=0 or any(x["target"]==str(p) or x["target"].startswith(str(p)+"/") for x in m):reason="SKIP: mount detected or inspection failed"
 q=pf.run(["lslocks","--json","-o","PID,COMMAND,TYPE,MODE,PATH"])
 locks=json.loads(q["stdout"]).get("locks",[]) if q["rc"]==0 else []
 result["immediate_locks"]=[x for x in locks if str(x.get("path",""))==str(p) or str(x.get("path","")).startswith(str(p)+"/")]
 if q["rc"]!=0 or result["immediate_locks"]:reason="SKIP: lock query failed or lock present"
 listing=pathlib.Path(r["listing"]["path"])
 assert hashlib.sha256(listing.read_bytes()).hexdigest()==r["listing"]["sha256"]
 result["before_df"]=df()
 if reason:
  result.update(status="SKIPPED",reason=reason)
 else:
  cmd=["rm","-rf","--one-file-system","--",str(p)]
  result.update(status="DELETING",argv=cmd);save("item-%02d.json"%r["number"],result)
  print("ARGV",json.dumps(cmd),flush=True)
  q=subprocess.run(cmd,capture_output=True,text=True)
  result["rm"]={"rc":q.returncode,"stdout":q.stdout,"stderr":q.stderr}
  result["exists_after"]=p.exists() or p.is_symlink()
  result["status"]="DELETED" if q.returncode==0 and not result["exists_after"] else "STOP"
  result["reason"]="" if result["status"]=="DELETED" else "STOP: rm failed or path still exists; no retry"
 result["after_df"]=df();result["time_end"]=now()
 result["df_available_change"]=result["after_df"].get("available_bytes",0)-result["before_df"].get("available_bytes",0)
 save("item-%02d.json"%r["number"],result);out.append(result);save("deletion-results.json",out)
 print("98删除项",r["number"],"已结束",result["time_end"],result["status"],"df_delta",result["df_available_change"],result["reason"],flush=True)
print("98步骤2 已结束",now(),"status="+("PASS" if all(x["status"]=="DELETED" for x in out) else "PARTIAL"),flush=True)
