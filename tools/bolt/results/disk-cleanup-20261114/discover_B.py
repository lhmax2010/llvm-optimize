#!/usr/bin/env python3
import json,pathlib,os,time,datetime
E=pathlib.Path(__file__).parent
plan=json.loads((E/"classification-plan.json").read_text())
found=[];errors=[];start=time.monotonic()
for r in plan:
 if r["category"]!="B":continue
 p=pathlib.Path(r["path"])
 if not p.is_dir() or p.is_symlink():continue
 def err(x):errors.append(str(x))
 for root,dirs,files in os.walk(p,onerror=err,followlinks=False):
  if time.monotonic()-start>900:
   errors.append("900s metadata inventory budget exhausted");break
  if ".git" in dirs or ".git" in files:found.append({"partition":str(p),"path":str(pathlib.Path(root)/".git"),"kind":"repository"})
  dirs[:]=[n for n in dirs if n!=".git" and not pathlib.Path(root,n).is_symlink()]
  for name in files:
   if name.endswith((".fdata",".profdata",".profraw")):
    q=pathlib.Path(root)/name
    try:st=q.stat();sz=st.st_size
    except OSError as x:err(x);sz=None
    found.append({"partition":str(p),"path":str(q),"kind":"profile_name","size":sz})
out={"found":found,"errors":errors,"elapsed_seconds":time.monotonic()-start,"meaning":"Names only. LLVM test fixtures or exported copies are not automatically training originals. No contents modified."}
(E/"B-profile-repository-discovery.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
print("B_PROFILE_DISCOVERY",len(found),"errors",len(errors),flush=True)
print("97保留边界复核 已结束",datetime.datetime.now().astimezone().isoformat(),"status=DONE",flush=True)
