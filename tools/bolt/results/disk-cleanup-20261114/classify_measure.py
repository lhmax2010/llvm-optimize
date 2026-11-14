#!/usr/bin/env python3
import json, pathlib, os, subprocess, time, selectors, datetime, stat
E=pathlib.Path(__file__).parent
W=pathlib.Path("/home/linhao/Toolchain/development/llvm-optimize")
B=pathlib.Path("/home/linhao/Toolchain/development/llvm-optimize-bolt")
T=W/"temp"
measure=[json.loads(x) for x in (E/"measurements.jsonl").read_text().splitlines()]
refs=json.loads((E/"reference-index.json").read_text())
def save(n,v): (E/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n")
over={}
def rule(p,c,why,doc,risk="",recommend=False):
 over[str(p)]={"category":c,"basis":why,"documents":doc,"risk":risk,"recommended_B":recommend}
for r in measure:
 p=pathlib.Path(r["path"])
 if not p.is_relative_to(T) and not str(p).startswith("/var/tmp"):
  rule(p,"C","W/B Git工作区本身；不作为清理候选","97")
for r in json.loads((E/"repositories-current.json").read_text()):
 p=pathlib.Path(r["path"])
 if p.is_relative_to(T):
  root=T/p.relative_to(T).parts[0]
  if root.name=="rebase-359934-20261111-r6":rule(p,"C","独立源码克隆，当前/历史已验证提交","74/85/96")
  else:rule(root,"C","包含LLVM/Git工作树或其公共对象库；保守保留整个上层目录，未发布性不改变保留结论","85/97")
for n,reason,doc in [
 ("deleted-repo-backup-20261105","源码保护备份，不可删除","64/85"),
 ("local-full-r6-20261111-materials","74 BOLT输入/最终ELF及后续83/87/88/93/94证据","74/83/97"),
 ("tu-inputs-restored-20261106","经SHA恢复的90 TU输入","67"),
 ("pgo-profiles-keep-20261102","原始PGO profile","61/64"),
 ("bolt-measurement-20260918","含Source1200合并前23份原始fdata；保留整组采集现场","16/65"),
 ("pgo-bolt-followup-20261105","含新采集profile原件、工具与实验唯一产物；保守整根保留","59/61"),
 ("gbs-root-x86_64-archivefix-v2","65需保留的工具、安装环境及原RPM未另保全","65/85"),
 ("gbs-root-x86_64-debuginfo-j4-v2","65需保留的工具、普通clang、RPM；不把整根认作可再生缓存","65/85"),
 ("crash-fix-probe-20261028","65确认原来源被删，工具矩阵/复现材料不能从剩余来源完整重建","65"),
 ("arm-archive-tls-thumb-20261010","65确认独有ARM实验输入/证据","65"),
 ("arm-archive-standard-build-20261010","65确认独有ARM基线输入","65"),
 ("night-20261103","原始转换命令/平台工具及后续重放输入；96准入前不得清理","55/78/96"),
 ("night-20261105","原ThinLTO库、loader/平台工具、264 DWARF原始输入与RPM；下周重放及A项再生依赖","63/67/78/96"),
 ("review-20261103","历史转换器测试工具/输入仍需保留，权限盲区下保守整根保留","53/78"),
 ("qb-1225393-1225395","78的450归档对应RPM；79 member-check旧端原件，保留各架构RPM","77/78/79"),
 ("qb-1216409-1216410","67的DWARF原输入及旧验证器依赖，作为A类再生依赖保留","57/67"),
 ("bench_results","历史性能原始数据，未证明有完整替代，保守保留","85"),
 ("deleted-roots-logs","已删根的唯一日志，不能重建原始测量","64")]:
 rule(T/n,"C",reason,doc)
rule(T/"qb-1226850-1226851","C","当前基线RPM及原始结果；仅明确解包副本另列A","79/97")
rule(T/"fifth-review-20261111","C","78/96重放输入和当前产物；仅可再生成员临时工作区另列A","78/96")
rule(T/"rebase-359934-20261111-r6","C","74现场的RPM、日志、采样、源码和配置；构建根另外列B","74")
for tag in ["toolchain","basedev"]:
 rule(T/"rebase-359934-20261111-r6"/tag/"gbs-root","B","当前74 r6完整构建根；丢失平台loader/tools及中间树，D report-stale仍依赖；需先完成诊断或保全可运行工具环境。RPM和日志保留不等于该待办已解除","74/87/92/97","高")
for n in ["qb-1221204-1221207","qb-1223601-1223602"]:
 rule(T/n,"B","旧QB下载/比较现场已由1226850/51取代，71/73结论已发布；本轮未联网确认能重新下载，故不列A。删除丢失旧RPM原件与复核便利；若URL仍可用可重下，否则需同提交快照重建，耗时/空间UNKNOWN","71/73/79","中",True)
for n in ["arm-archive-stage1-20261010","arm-source-root-probes-20261010","qb-meta-switch-20261028","bolt-v4-20261022-cache-release"]:
 rule(T/n,"B","65/85历史实验保留部分；已做过局部瘦身，不能把现存目录当旧缓存全删。丢失ARM/缓存释放/元数据对照材料；重建依赖原快照/工具/输入，成本UNKNOWN","65/66/85","中")
def arule(rel,reason,doc):
 p=T/rel
 assert p.exists(),p
 rule(p,"A",reason,doc,"低")
arule("dwarf-check-20261106","A2：由保留的264个.debug及平台llvm-dwarfdump导出的文本/规范化副本；输入及工具存在性和大小检查见dwarf-retained-inputs.json，脚本及结论已发布。重生成语义文本，不承诺gzip时间戳一致","67")
for rel in ["local-full-r6-20261111-compare/toolchain/payload","local-full-r6-20261111-compare/basedev/payload","qb79-local-resume-20261112/toolchain/payload","qb79-local-resume2-20261112/basedev/payload"]:
 arule(rel,"A2：RPM解包比较副本；74本地gbs-driver及对应QB RPM保留C，原始比较结论/清单在证据仓库。72个原RPM存在和大小检查见retained-rpm-sources.json","74/79")
arule("qb79-source-resume2-20261112","A2：R2源码比较/补丁应用展开副本；本地和QB源码RPM保留C，归类脚本与结论79已发布","79")
arule("qb-1226850-1226851/member-check","A2：新旧各架构静态归档解包成员；新基线及1225393/95原RPM全部保留C，可重新解包，成员比较结论79已发布","79")
arule("qb-1226850-1226851/source-audit","A2：当前基线source-audit展开副本，原源码RPM保留C，79结论已发布","79")
for p in sorted((T/"fifth-review-20261111").glob("rerun*/debug-conversion-*/retained-cleanup")):
 arule(str(p.relative_to(T)),"A2：转换器保留的临时input.bc/input.ll/成员.o；原bitcode输入及old/new最终归档全部保留C，78逐字节一致结论已发布；不包含需要保留的archives目录","78/96")
# Every path is covered by a conservative default; partitions split only at explicit overrides.
roots=[pathlib.Path(x["path"]) for x in measure]
extra=pathlib.Path("/home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM")
if extra.exists():
 roots.append(extra)
 rule(extra,"C","本项目17/20/28引用的共享ARM sysroot；可能与其他项目共用，不作为删除对象","17/20/28/31")
parts=[];containers=[]
def under(p,q):return p==q or p.startswith(q+"/")
def choose(p,inherited=None):
 p=str(p)
 if p in over:return dict(over[p])
 if inherited:return dict(inherited)
 return {"category":"B","basis":"历史实验/证据；未证明符合A条件，也未认定可丢弃。删除会失去本地输入/产物/原始日志；须按reference-index核对替代件后裁决；重建方法与成本UNKNOWN","documents":"85；reference-index.json","risk":"中","recommended_B":False}
def split(p,inherited=None):
 p=pathlib.Path(p); conf=choose(p,inherited)
 descendants=[k for k in over if k!=str(p) and under(k,str(p))]
 if descendants and p.is_dir() and not p.is_symlink():
  containers.append({"path":str(p),"category":conf["category"],"own_blocks_bytes":p.lstat().st_blocks*512})
  for child in sorted(p.iterdir()):split(child,conf)
 else:
  parts.append({"path":str(p),**conf,"filesystem":"home" if str(p).startswith("/home/") else "var_tmp"})
for p in roots:split(p)
assert len({p["path"] for p in parts})==len(parts)
for p in parts:
 assert not any(under(q["path"],p["path"]) and q!=p for q in parts)
save("classification-plan.json",parts)
save("partition-containers.json",containers)
print("partitions",len(parts),"containers",len(containers),flush=True)
# Single GNU du process across C,B,A counts each hardlink inode once. No symlink traversal.
ordered=sorted(parts,key=lambda r:("CBA".index(r["category"]),r["path"]))
(E/"partition-paths.nul").write_bytes(b"".join(os.fsencode(r["path"])+b"\0" for r in ordered))
start=time.monotonic()
cmd=["stdbuf","-o0","du","-x","-s","-B1","--null","--files0-from="+str(E/"partition-paths.nul")]
with (E/"partition-du.stderr").open("wb") as err:
 proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=err)
 sel=selectors.DefaultSelector();sel.register(proc.stdout,selectors.EVENT_READ)
 pending=b"";records=[];last=time.monotonic();timed_out=False
 while sel.get_map():
  if time.monotonic()-last>900 or time.monotonic()-start>6000:
   timed_out=True;proc.kill();break
  for key,_ in sel.select(5):
   data=os.read(key.fileobj.fileno(),65536)
   if not data:sel.unregister(key.fileobj);continue
   pending+=data
   while b"\0" in pending:
    line,pending=pending.split(b"\0",1)
    size,path=line.decode(errors="replace").split("\t",1)
    records.append({"path":path,"observed_deduplicated_bytes":int(size)})
    last=time.monotonic()
    if len(records)%20==0:print("DEDUP",len(records),path,flush=True)
 rc=proc.wait()
errors=(E/"partition-du.stderr").read_text()
for row in records:
 row["complete"]=not any(row["path"] in line for line in errors.splitlines())
 row["size_bytes"]=row["observed_deduplicated_bytes"] if row["complete"] else None
save("deduplicated-measurements.json",{"argv":cmd,"rc":rc,"timeout":timed_out,"elapsed_seconds":time.monotonic()-start,"records":records,"method":"C then B then A, GNU du default hardlink de-duplication; allocated bytes; permission failures remain UNKNOWN"})
print("97去重核算 已结束",datetime.datetime.now().astimezone().isoformat(),"status="+("UNKNOWN" if timed_out else "DONE"),flush=True)
