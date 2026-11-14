#!/usr/bin/env python3
import pathlib,json,subprocess,os,stat,time,datetime,gzip,hashlib
D=pathlib.Path(__file__).parent/"check02";D.mkdir(exist_ok=False);(D/"listings").mkdir();E=D.parent.parent;B=D.parents[5]
W=pathlib.Path("/home/linhao/Toolchain/development/llvm-optimize")
def save(n,v):(D/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n")
def now():return datetime.datetime.now().astimezone().isoformat()
def run(args,timeout=180):
 r=subprocess.run(args,capture_output=True,text=True,timeout=timeout)
 return {"argv":args,"rc":r.returncode,"stdout":r.stdout,"stderr":r.stderr}
def occupied(paths):
 q=run(["lsof","-nP","-Fpcfn"],120);hits=[];pid=cmd=None
 for line in q["stdout"].splitlines():
  if line.startswith("p"):pid=line[1:]
  elif line.startswith("c"):cmd=line[1:]
  elif line.startswith("n"):
   f=line[1:].removesuffix(" (deleted)")
   for p in paths:
    if f==p or f.startswith(p+"/"):hits.append({"path":p,"pid":pid,"command":cmd,"open_path":f})
 return {"time":now(),"rc":q["rc"],"stderr":q["stderr"],"hits":hits,"scope":"ordinary-user lsof including cwd/root/mmap; root process visibility can be restricted"}
def mounts():
 q=run(["findmnt","-J","-o","TARGET,SOURCE,FSTYPE"]);out=[]
 def visit(items):
  for x in items:
   out.append({k:v for k,v in x.items() if k!="children"});visit(x.get("children",[]))
 if q["rc"]==0:visit(json.loads(q["stdout"]).get("filesystems",[]))
 return q["rc"],out
def validate_originals():
 lookup={}
 for tag in ["toolchain","basedev"]:
  j=json.loads(pathlib.Path("tools/bolt/results/local-full-r6-20261111",tag,"comparison/rpm-identities.json").read_text())
  for pkg,v in j.items():
   for side in ["local","qb"]:
    lookup[v[side]["path"]]=v[side]["bytes"]
 for r in json.loads(pathlib.Path("tools/bolt/results/tu-dwarf-20261106/dwarf-pairs.json").read_text()):
  for side in ["old","new"]:lookup[r[side]]=r[side+"_bytes"]
 checks=[]
 reference=json.loads((E/"retained-rpm-sources.json").read_text())+json.loads((E/"dwarf-retained-inputs.json").read_text())["checks"]
 for r in reference:
  p=pathlib.Path(r["path"]);expected=lookup.get(str(p))
  exists=p.is_file();actual=p.stat().st_size if exists else None
  auxiliary=(str(p).endswith("/usr/bin/llvm-dwarfdump") or str(p).endswith("/lib64/ld-linux-x86-64.so.2")) and "expected_sha256" not in r
  checks.append({"path":str(p),"expected_bytes":expected,"actual_bytes":actual,"check":"existence-only auxiliary tool, no byte baseline in97" if auxiliary else "exact byte size against97 source manifest","ok":exists and (auxiliary or (expected is not None and actual==expected))})
 replay=json.loads((E/"replay-assets-current.json").read_text())
 for r in replay["debug_inputs"]["files"]+replay["outputs"]:
  p=pathlib.Path(r["path"]);actual=p.stat().st_size if p.is_file() else None
  checks.append({"path":str(p),"expected_bytes":r["size"],"actual_bytes":actual,"ok":actual==r["size"]})
 return {"checks":checks,"pass":all(x["ok"] for x in checks),"count":len(checks),"time":now(),"note":"97 stored size_match plus identity SHA; actual byte baselines recovered from the same 74/67 manifests used by97"}
def main():
 allowed=json.loads((D.parent/"approved-paths.json").read_text());paths=[r["path"] for r in allowed]
 originals=validate_originals();save("originals-before.json",originals)
 oc=occupied(paths);save("occupancy-before.json",oc)
 mrc,ms=mounts()
 locks=run(["lslocks","--json","-o","PID,COMMAND,TYPE,MODE,PATH"])
 ls=json.loads(locks["stdout"]).get("locks",[]) if locks["rc"]==0 else []
 save("project-locks-before.json",{"rc":locks["rc"],"stderr":locks["stderr"],"locks":[x for x in ls if any(str(x.get("path",""))==p or str(x.get("path","")).startswith(p+"/") for p in paths)]})
 save("df-before.json",run(["df","-B1","/home"]))
 parents={}
 for p in paths:
  par=pathlib.Path(p).parent
  if str(par) not in parents:
   parents[str(par)]=[{"path":str(c),"inode":c.lstat().st_ino,"type":"directory" if c.is_dir() else "file","size":c.lstat().st_size} for c in sorted(par.iterdir()) if str(c) not in paths]
 save("parent-siblings-before.json",parents)
 results=[]
 for row in allowed:
  r=dict(row);p=pathlib.Path(r["path"]);r["time"]=now();reasons=[]
  r["exists"]=p.exists();r["symlink"]=p.is_symlink();r["realpath"]=str(p.resolve())
  if not p.is_dir() or p.is_symlink() or str(p.resolve())!=str(p):reasons.append("STOP: directory missing, symlink, or canonical path mismatch")
  if not reasons:
   st=p.lstat();r["identity"]={"device":st.st_dev,"inode":st.st_ino,"uid":st.st_uid,"gid":st.st_gid}
   z=run(["du","-x","-s","-B1","--",str(p)],900);r["du"]=z
   if z["rc"]!=0:reasons.append("STOP: du did not complete")
   else:
    r["actual_bytes"]=int(z["stdout"].split()[0])
    r["relative_size_change"]=abs(r["actual_bytes"]-r["expected_bytes"])/max(1,r["expected_bytes"])
    if r["relative_size_change"]>0.05:reasons.append("STOP: size differs from97 by more than5%")
  if oc["rc"]!=0:reasons.append("SKIP: lsof query failed")
  r["occupancy"]=[x for x in oc["hits"] if x["path"]==str(p)]
  if r["occupancy"]:reasons.append("SKIP: process is using this directory")
  r["mountpoints"]=[x for x in ms if x["target"]==str(p) or x["target"].startswith(str(p)+"/")]
  if mrc!=0 or r["mountpoints"]:reasons.append("SKIP: mount inspection failed or mount present")
  r["held_locks"]=[x for x in ls if str(x.get("path",""))==str(p) or str(x.get("path","")).startswith(str(p)+"/")]
  if locks["rc"]!=0 or r["held_locks"]:reasons.append("SKIP: lock query failed or held lock")
  markers=[];errors=[]
  if not reasons:
   for root,dirs,files in os.walk(p,onerror=lambda x:errors.append(str(x)),followlinks=False):
    for n in dirs+files:
     if n in ("lock","lockfile",".lock",".git") or n.endswith((".lock",".lck")):markers.append(str(pathlib.Path(root)/n))
    dirs[:]=[n for n in dirs if not pathlib.Path(root,n).is_symlink()]
  r["lock_or_git_markers"]=markers;r["walk_errors"]=errors
  if markers or errors:reasons.append("SKIP: lock/Git marker or unreadable subtree")
  if r["category"]=="A" and not originals["pass"]:reasons.append("SKIP: preservation source missing or size changed")
  r["reasons"]=reasons;r["status"]="READY" if not reasons else ("STOP" if any(s.startswith("STOP") for s in reasons) else "SKIPPED")
  if r["status"]=="READY":
   fname=D/"listings"/(str(r["number"]).zfill(2)+"-"+p.name+".tsv.gz")
   # Requested find format; stream into gzip, do not buffer complete listing.
   with fname.open("xb") as out:
    find=subprocess.Popen(["find",str(p),"-printf","%P\t%s\t%T@\t%y\n"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    gz=subprocess.Popen(["gzip","-c"],stdin=find.stdout,stdout=out,stderr=subprocess.PIPE);find.stdout.close()
    _,gerr=gz.communicate(timeout=180)
    ferr=find.stderr.read();frc=find.wait(timeout=10)
   r["listing"]={"path":str(fname),"bytes":fname.stat().st_size,"sha256":hashlib.sha256(fname.read_bytes()).hexdigest(),"find_rc":frc,"gzip_rc":gz.returncode,"stderr":(ferr+gerr).decode(errors="replace"),"publish":fname.stat().st_size<=10000000}
   if frc or gz.returncode:r["status"]="STOP";r["reasons"].append("STOP: listing generation failed")
  results.append(r);save("preflight.json",results)
  print(r["number"],str(p),r["status"],r.get("relative_size_change"),r["reasons"],flush=True)
 print("98步骤1 已结束",now(),"status="+("PASS" if all(r["status"]=="READY" for r in results) else "PARTIAL"),flush=True)
if __name__=="__main__":main()
