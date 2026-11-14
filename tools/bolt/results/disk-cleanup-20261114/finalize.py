#!/usr/bin/env python3
import json,pathlib,subprocess,datetime
E=pathlib.Path(__file__).parent
B=pathlib.Path("/home/linhao/Toolchain/development/llvm-optimize-bolt")
W=B.parent/"llvm-optimize";T=W/"temp";G=1024**3
def read(n):return json.loads((E/n).read_text())
def save(n,v):(E/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n")
def gi(n):return f"{n/G:.3f}"
plans=read("classification-plan.json")
dedup=read("deduplicated-measurements.json")
reclaim=read("reclaim-accounting.json")
assert not dedup["timeout"],"STOP: du timeout requires UNKNOWN/fallback handling"
ds={x["path"]:x for x in dedup["records"]}
assert len(ds)==len(plans)
assert all(not r["errors"] for r in reclaim["roots"]),"STOP: candidate stat scan errors"
refs=read("reference-index.json")
adjustments={r["path"]:r for r in read("post-discovery-classification.json")}
rows=[]
for r in plans:
 q={**r,**ds[r["path"]],"kind":"partition","included_in_total":True}
 q.update(adjustments.get(q["path"],{}))
 p=pathlib.Path(q["path"]);key=p.relative_to(T).parts[0] if p.is_relative_to(T) else None
 q["references"]=refs.get(key,[])[:8]
 if q["category"]=="B":
  q["loss_if_deleted"]=q["basis"]
  q["recreation"]= "若原公开RPM仍可下载则重新下载；否则需原提交、快照重建，不能保证旧环境再现" if q["recommended_B"] else "按引用文档重做实验/构建并保全输入；原始运行日志和采样不能重建"
  q["cost"]="UNKNOWN（未重下载、重建或估算）"
  if key=="rebase-359934-20261111-r6":q["cost"]="74实测参考：T 7875.23s、D 3900.703s；两根启动预算151.3GiB。这是历史观测，不是未来重建预测；原日志/测量无法重建"
  q["recommendation"]="有条件建议：用户接受失去旧RPM即时复核能力后，可在A之后清理；下载可用性未核实，删除前再查占用" if q["recommended_B"] else "暂保留，待PM核对输入、替代件及待办后决定"
  if key=="qb-1223601-1223602":q["risk"]="高"
 rows.append(q)
for r in read("partition-containers.json"):
 rows.append({**r,"kind":"container_inode_only","included_in_total":True,"filesystem":"home","size_bytes":r["own_blocks_bytes"],"observed_deduplicated_bytes":r["own_blocks_bytes"],"complete":True,"basis":"仅父目录自身块；子项已单列，本行不是整个目录的删除候选"})
initial=[json.loads(x) for x in (E/"measurements.jsonl").read_text().splitlines()]
top=[]
for r in initial:
 p=pathlib.Path(r["path"]);lower=r["size_bytes"] if r["size_bytes"] is not None else next((x["size_bytes"] for x in r["children"] if x["path"]==r["path"]),0)
 subs=[q for q in rows if q["path"]==r["path"] or q["path"].startswith(r["path"]+"/")]
 cats={q["category"] for q in subs};cat="C" if "C" in cats else "B" if "B" in cats else "A"
 top.append({"path":r["path"],"kind":"top_scope","category":cat,"child_categories":sorted(cats),"included_in_total":False,"size_bytes":r["size_bytes"],"observed_independent_du_bytes":lower,"complete":r["size_bytes"] is not None,"basis":"顶层含C不得整体删除；合计仅用partition及父目录自身块，避免重复","references":refs.get(p.name,[])[:8]})
rows.extend(top)
(E/"inventory.jsonl").write_text("".join(json.dumps(q,ensure_ascii=False)+"\n" for q in rows))
now=datetime.datetime.now().astimezone().isoformat()
df=subprocess.run(["df","-B1","/home","/var/tmp"],capture_output=True,text=True)
save("df-final.json",{"time":now,"argv":df.args,"rc":df.returncode,"stdout":df.stdout,"stderr":df.stderr})
available=int(df.stdout.splitlines()[1].split()[3])
add=[r for r in rows if r["included_in_total"]]
shared="/home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM"
summ={}
for area in ["home_project","home_shared_input","var_tmp"]:
 rs=[r for r in add if (area=="home_project" and r["filesystem"]=="home" and r["path"]!=shared) or (area=="home_shared_input" and r["path"]==shared) or (area=="var_tmp" and r["filesystem"]=="var_tmp")]
 summ[area]={}
 for c in "ABC":
  rr=[r for r in rs if r["category"]==c]
  summ[area][c]={"observed_bytes":sum(r["observed_deduplicated_bytes"] for r in rr),"complete":all(r["complete"] for r in rr),"unknown_partitions":sum(not r["complete"] for r in rr),"partitions":len(rr)}
pred={"available_bytes":available,"need_bytes":186*G}
for c,k in [("A","only_A"),("AB","A_plus_recommended_B")]:
 v=reclaim["summary"][c]["known_reclaimable_bytes"]
 pred[k]={"reclaimable_bytes":v,"available_after_bytes":available+v,"gap_bytes":max(0,186*G-available-v),"surplus_bytes":max(0,available+v-186*G)}
save("summary.json",{"time":now,"totals":summ,"forecasts":pred,"initial_home_available_bytes":30505807872,"initial_independent_home_observation_bytes":sum(q["observed_independent_du_bytes"] for q in top if q["path"].startswith("/home/")),"initial_measurement_seconds":read("measurement-summary.json")["elapsed_seconds"],"deduplicated_measurement_seconds":dedup["elapsed_seconds"]})
def size(r):return ("≥"+gi(r["observed_deduplicated_bytes"])+"（完整UNKNOWN）") if not r["complete"] else gi(r["observed_deduplicated_bytes"])
def short(p):return "W/temp/"+p[len(str(T))+1:] if p.startswith(str(T)+"/") else p
base="https://github.com/lhmax2010/llvm-optimize/blob/bolt-v4/"
for c in "ABC":
 rs=sorted([r for r in rows if r["kind"]=="partition" and r["category"]==c],key=lambda r:r["observed_deduplicated_bytes"],reverse=True)
 out=[f"# {c} 类完整清单\n","GiB为跨目录硬链接去重后的分摊占用（C→B→A顺序）；独立du另见top-level-list.md。仅分类，不构成删除授权。\n"]
 if c=="B":out+=["有条件建议仅两组旧QB目录；可重下载未核实，删除会影响历史复核。其他B项建议暂保留。\n"]
 out+=["| 路径 | 分摊GiB | 依据／损失与重建 | 文档 | 风险／建议 |","|---|---:|---|---|---|"]
 for q in rs:
  documents=q["documents"]
  found=list(dict.fromkeys(x["file"] for x in q["references"]))[:3]
  documents+="; "+" ".join("["+pathlib.Path(f).name+"]("+base+f+")" for f in found)
  reason=q["basis"]
  if c=="B":reason+=" "+q["recreation"]+"；成本："+q["cost"]
  out.append("| "+short(q["path"])+" | "+size(q)+" | "+reason.replace("|","/").replace("\n"," ")+" | "+documents+" | "+q.get("risk","")+" "+q.get("recommendation","")+" |")
 (E/f"{c}-list.md").write_text("\n".join(out)+"\n")
out=["# 范围总表（不与分类分区相加）","","| 路径 | 独立du GiB | 整目录类别 | 子类 |","|---|---:|---|---|"]
for r in top:
 v=("≥"+gi(r["observed_independent_du_bytes"])+" / UNKNOWN") if not r["complete"] else gi(r["size_bytes"])
 out.append(f"| {short(r['path'])} | {v} | {r['category']} | {','.join(r['child_categories'])} |")
(E/"top-level-list.md").write_text("\n".join(out)+"\n")
print("97分类 已结束",now,"status=PARTIAL")
print(json.dumps({"totals":summ,"forecasts":pred},ensure_ascii=False,indent=2))
