#!/usr/bin/env python3
import os,stat,json,pathlib,time,datetime,collections
E=pathlib.Path(__file__).parent
parts=json.loads((E/"classification-plan.json").read_text())
start=time.monotonic()
allinodes={}; recs=[]; sensitive=[]
for r in parts:
 if r["category"]!="A" and not r["recommended_B"]:continue
 path=r["path"]; stats={"path":path,"category":r["category"],"files":0,"directories":0,"symlinks":0,"errors":[],"special_files":[],"allocated_bytes_per_name":0}
 stack=[path]
 while stack:
  if time.monotonic()-start>900:
   stats["errors"].append("inventory metadata scan exceeded 900s");break
  p=stack.pop()
  try:
   st=os.lstat(p); k=(st.st_dev,st.st_ino); b=st.st_blocks*512
   stats["allocated_bytes_per_name"]+=b
   if stat.S_ISDIR(st.st_mode):
    stats["directories"]+=1
    if pathlib.Path(p).name==".git":stats["special_files"].append(p)
    with os.scandir(p) as it:stack.extend(x.path for x in it)
   else:
    stats["files"]+=1
    if stat.S_ISLNK(st.st_mode):stats["symlinks"]+=1
    if pathlib.Path(p).suffix in [".fdata",".profdata",".profraw"] or pathlib.Path(p).name==".git":stats["special_files"].append(p)
   v=allinodes.setdefault(k,{"bytes":b,"links":st.st_nlink,"directory":stat.S_ISDIR(st.st_mode),"count_A":0,"count_AB":0,"path":p,"owners":[]})
   v["count_AB"]+=1
   if r["category"]=="A":v["count_A"]+=1
   if path not in v["owners"]:v["owners"].append(path)
  except OSError as ex:stats["errors"].append(str(ex))
 recs.append(stats);print("METADATA",path,stats["files"],"errors",len(stats["errors"]),flush=True)
def freed(v,which):
 count=v["count_"+which]
 return count>0 and (v["directory"] or count>=v["links"])
summary={}
for which in ["A","AB"]:
 selected=[v for v in allinodes.values() if v["count_"+which]]
 summary[which]={"all_observed_unique_bytes":sum(v["bytes"] for v in selected),"known_reclaimable_bytes":sum(v["bytes"] for v in selected if freed(v,which)),"external_link_bytes_excluded":sum(v["bytes"] for v in selected if not freed(v,which)),"inode_count":len(selected)}
result={"method":"lstat st_blocks*512, no symlink following; freeable only if every observed hardlink is inside selected set (directories counted separately); excludes filesystem metadata, snapshots/open handles beyond lsof visibility","elapsed_seconds":time.monotonic()-start,"summary":summary,"roots":recs,"external_link_samples":[v for v in allinodes.values() if not freed(v,"AB")][:100]}
(E/"reclaim-accounting.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(summary),flush=True)
print("97释放量核算 已结束",datetime.datetime.now().astimezone().isoformat(),"status=DONE",flush=True)
