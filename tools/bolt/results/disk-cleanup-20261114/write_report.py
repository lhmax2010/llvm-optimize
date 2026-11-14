#!/usr/bin/env python3
import json,pathlib,datetime,subprocess
B=pathlib.Path("/home/linhao/Toolchain/development/llvm-optimize-bolt")
E=pathlib.Path(__file__).parent
W=B.parent/"llvm-optimize";T=W/"temp";G=1024**3
def read(n):return json.loads((E/n).read_text())
def gi(n):return f"{n/G:.3f}"
s=read("summary.json");tot=s["totals"];pred=s["forecasts"];a=pred["only_A"];ab=pred["A_plus_recommended_B"];now=s["time"]
rows=[json.loads(x) for x in (E/"inventory.jsonl").read_text().splitlines()]
parts=[r for r in rows if r["kind"]=="partition"]
def short(p):return "W/temp/"+p[len(str(T))+1:] if p.startswith(str(T)+"/") else p
catrows=[]
for c in "ABC":
 v=tot["home_project"][c]
 catrows.append(f"| {c} | {'≥' if not v['complete'] else ''}{gi(v['observed_bytes'])} | {'UNKNOWN；'+str(v['unknown_partitions'])+'个分区有权限盲区' if not v['complete'] else '本次测量完整'} |")
atables="\n".join("| "+short(r["path"])+" | "+gi(r["observed_deduplicated_bytes"])+" | "+r["documents"]+" |" for r in sorted([r for r in parts if r["category"]=="A"],key=lambda r:r["observed_deduplicated_bytes"],reverse=True))
btable="\n".join("| "+short(r["path"])+" | "+gi(r["observed_deduplicated_bytes"])+" | "+r["risk"]+" |" for r in parts if r["recommended_B"])
home=sum(v["observed_bytes"] for v in tot["home_project"].values());shared=sum(v["observed_bytes"] for v in tot["home_shared_input"].values());var=sum(v["observed_bytes"] for v in tot["var_tmp"].values())
vars_table="\n".join(f"| {c} | {'≥' if not tot['var_tmp'][c]['complete'] else ''}{gi(tot['var_tmp'][c]['observed_bytes'])} |" for c in "ABC")
df=read("df-final.json")["stdout"]
doc=f"""# 97号：llvm-optimize 磁盘清理盘点（不删除）

**结论：只读盘点和分类完成，没有删除、移动、压缩原件或修改锁。** /home可用 **{gi(pred['available_bytes'])} GiB**。只删A预计释放 **{gi(a['reclaimable_bytes'])} GiB**，可用为 **{gi(a['available_after_bytes'])} GiB**，距下周 **186 GiB** 需求缺 **{gi(a['gap_bytes'])} GiB**；A加下述两组有条件建议B后，可用为 **{gi(ab['available_after_bytes'])} GiB**，富余 **{gi(ab['surplus_bytes'])} GiB**、缺口 **{gi(ab['gap_bytes'])} GiB**。这是其他写入不变时的规划，不是已经释放，也不是删除授权。

| /home项目类别 | 已读、跨目录去重占用GiB | 完整合计 |
|---|---:|---|
{chr(10).join(catrows)}

B/C完整合计为UNKNOWN；“≥”仅加总读到的块，不推算权限盲区。共享ARM输入根另列C **≥{gi(shared)} GiB**，不冒充项目独占；将它计入相关位置时，C下界为 **{gi(tot['home_project']['C']['observed_bytes']+shared)} GiB**。/var/tmp另盘，不计入/home释放预测。

完整清单：[A，按大小排序](../../tools/bolt/results/disk-cleanup-20261114/A-list.md)、[B，风险与重建](../../tools/bolt/results/disk-cleanup-20261114/B-list.md)、[C](../../tools/bolt/results/disk-cleanup-20261114/C-list.md)、[顶层范围](../../tools/bolt/results/disk-cleanup-20261114/top-level-list.md)、[inventory.jsonl](../../tools/bolt/results/disk-cleanup-20261114/inventory.jsonl)、[数字JSON](../../tools/bolt/results/disk-cleanup-20261114/summary.json)。[证据文件索引](../../tools/bolt/results/disk-cleanup-20261114/RAW_LINKS.md)。

## 1. 范围、测量与“约1TB”

W={W}；B={B}。范围包括W所有非temp直接子项、W/temp全部152个一级目录及直接文件、B、8个/var/tmp项目位置，以及共享ARM输入根。85号32个历史仓库位置全部在W/temp，不再叠加；先核对34处HEAD，后续又发现single-change-20261114/source（ecb2dec7），合计35处；见repositories-current.json和additional-repository.json。/home/abuild宿主目录不存在（scope.json），不能再把每个构建根内的home/abuild计成宿主独立根。

首轮逐根du在/home已读 **1051.218 GiB，约1.027 TiB**，对应“接近1TB”，但有跨目录硬链接重复和权限缺口。第二轮同一GNU du进程按C→B→A对互不重叠分区计数，/home项目已读 **{gi(home)} GiB**。父目录不与子目录叠加；拆分父目录只另计自身块。独立目录大小与去重分摊值可能不同，前者保留在top_scope记录。后续文件名复核把4个位置从B保守上调C（新增源码工作树及profile），沿用原去重块分摊，不重复测量或加计；见post-discovery-classification.json。独立测量数不是精确占用总量；去重后仍有不可读内容，完整总量仍UNKNOWN。

/home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM在17/20/28号被引用为ARM sysroot，保守C、共享输入单列。其他名称相似的MLGO/GCC/C99目录、llvm_autofdo_bolt_agent等不进入：仅浅层列名、读本项目文档确认归属，未遍历其内容。外部归属未确认项见external-root-attribution.json；不把同名LLVM工具链一概算成本项目。

/var/tmp已读合计 **≥{gi(var)} GiB**：
| 类别 | 已读去重GiB |
|---|---:|
{vars_table}

该盘释放不能增加/home可用量。原件/日志替代性未完整证明的旧构建根保守B。

首轮207项du耗时{s['initial_measurement_seconds']:.1f}s，第二轮{s['deduplicated_measurement_seconds']:.1f}s，合计{(s['initial_measurement_seconds']+s['deduplicated_measurement_seconds'])/60:.1f}分钟，低于2小时；每个根/根输出等待上限900s，未出现超时，因此未触发最多两级超时下钻。首轮已记录max-depth=3的子目录分布。UNKNOWN是权限拒绝，不是超时；不用sudo、不外推隐藏内容。

全部分析在同一4GiB、swap0、nice19、IO idle用户服务内。du原文在du-*.txt，首次明细measurements.jsonl，去重结果deduplicated-measurements.json、权限原文partition-du.stderr。reclaim-accounting.json按lstat块数核算：只有全部硬链接都在假设清理集合内才计可释放；集合外硬链接排除。没有执行删除，也不承诺文件系统元数据、不可见打开句柄或后续写入的收益。

## 2. A类：已保留原件的解包、展开副本

A采用“保留RPM/归档可再生”的条款。本轮未使用“旧QB能重新下载”条款，也没有冒充完成未运行的重复副本抽样SHA证明。

| 路径 | 去重分摊GiB | 文档 |
|---|---:|---|
{atables}

- 78号只把retained-cleanup里的input.bc/input.ll/.o临时工作区列A；old/new/archives及rerun3/debug-inputs仍C。
- dwarf-check由保留的264个.debug及原平台llvm-dwarfdump展开。输入存在性、历史清单大小、工具路径核对见dwarf-retained-inputs.json；67号脚本/结论在B。此次不重新导出DWARF，不声称gzip封套时间字节可重现。
- 74/79 payload原RPM仍在本地gbs-driver和QB目录，72个原RPM存在/大小检查见retained-rpm-sources.json。父目录dwarf-proofs和已发布结果不随payload列A。
- 当前QB仅member-check/source-audit为展开副本；原RPM目录全部保留。

## 3. B类：需用户决定

有条件建议优先审议以下两组。**只有用户接受失去历史RPM即时复核能力，才能考虑清理。** 71/73结论已发布，当前基线1226850/51及78依赖的1225393/95原件保留C；然而旧脚本仍有路径引用（recommended-B-script-references.json），不是“无引用”。本轮未访问QB或公开下载URL，**可重新下载未核实**，故不能列A。URL仍可用时可重下载；失效则要原提交/快照重建，原环境能否再现、所需时间/磁盘均UNKNOWN。

| 有条件建议B | 去重分摊GiB | 风险 |
|---|---:|---|
{btable}

其他B建议暂保留，完整逐项损失、重建方法、成本UNKNOWN见B-list.md，尤其：
- 当前74 r6的toolchain/basedev gbs-root：B、高风险，D report-stale仍需其中loader/工具；删除会丢失原构建中间树和可运行诊断环境。它们不计入建议B释放量。74号L424/L453历史耗时T 7875.23s、D 3900.703s，入口两根预算151.3GiB；仅作代价参考，不预测下次时间。下周会重建不等于允许现在删。
- 历史ARM、缓存释放、安装及性能现场：无法证明原件/日志完整替代的部分B。65/85明确唯一输入、源码或profile原件的部分C。64/66已做过局部清理，不根据目录名把现在剩下的内容认作全部可再生。
- 重建只能恢复新的运行，不能恢复原始时间、资源采样或失败现场；成本无法从现有证据确定的明确UNKNOWN。

## 4. C类与96号真实重放的实际路径

deleted-repo-backup-20261105独立du91.294GiB，源码保护备份严格C。W/B工作区、PS1/PS2/PS3相关工作树、b0c1732c所在hardening-ps4源码根全C；本轮不fetch、不改分支，不以“可能已发布”为由放行源码删除。

91项关键路径存在性记录见protected-assets.json。已确认的关键输入：
- 74材料：W/temp/local-full-r6-20261111-materials/，83/87/88/93/94使用的BOLT输入与最终ELF。
- TU：W/temp/tu-inputs-restored-20261106/。
- PGO：W/temp/pgo-profiles-keep-20261102/，以及pgo-bolt-followup-20261105采集现场整体C。
- Source1200合并前23份fdata：W/temp/bolt-measurement-20260918/run/profiles/；源码测试夹具中的.profraw不当作训练原件。
- 450发货归档：W/temp/fifth-review-20261111/rerun3/qb-payload/toolchain及basedev，各225个。原RPM在W/temp/qb-1225393-1225395/1225393及1225395/x86_64/rpms/。
- 十个调试ThinLTO副本：W/temp/fifth-review-20261111/rerun3/debug-inputs/*.a；原件在night-20261105/toolchain/gbs-root中LLVM build/lib64，连同loader/工具保留。
- 96需比较的“当前产物”：Sema位于rerun3/debug-conversion-00/old及new/archives/libclangSema.a；其余九库位于rerun4/debug-conversion-01..09/old及new/archives/*.a。全部C。
- 十库覆盖78实测1093个转换成员、7个原生成员，**不是全部3853**；night-20261103完整原命令/输入及night-20261105原树也保留，避免丢失未来全量重放的材料。
- 当前基线RPM：W/temp/qb-1226850-1226851/1226850及1226851，全部架构C。
- 74本地RPM/源码包：W/temp/rebase-359934-20261111-r6/toolchain及basedev/gbs-driver/，evidence中的日志/采样同时保留C。

72原RPM和264个.debug输入本轮只核对存在性及历史大小；JSON中的SHA是历史身份索引，未重新哈希全部大文件。旧78/79通过结果不是97的新转换测试。96重放仍SKIPPED，PASS之前不得触发QB。B类另做profile/Git标记搜索：473条记录、55处权限拒绝；LLVM测试数据及7字节模拟profile不当训练原件。74和历史中间树的4份171232190字节profile副本经流式SHA与保留Source1200解压内容相同（profile-copy-proof.json），原件已在C。历史两份merged profile与新增PS工作树上调C。

普通用户lsof快照仅见其他进程占用W/B根cwd，未见A/B候选子树打开文件；自己的du/读文件句柄另列排除。lslocks未见项目路径锁，findmnt未见项目内部挂载。**root权限盲区仍在；任何实际被占用目录必须C，删除前要重新完整核对进程、锁和挂载**。本轮快照不是删除放行。W/B本身已C。

## 5. 可用空间预测

需求按本任务151+5+30=**186GiB**，不混用旧入口151.3GiB启动门槛。
| 假设 | 预计释放GiB | /home可用GiB | 距186GiB缺口 | 富余 |
|---|---:|---:|---:|---:|
| 不删 | 0 | {gi(pred['available_bytes'])} | {gi(max(0,186*G-pred['available_bytes']))} | 0 |
| 只删A | {gi(a['reclaimable_bytes'])} | {gi(a['available_after_bytes'])} | {gi(a['gap_bytes'])} | {gi(a['surplus_bytes'])} |
| A+建议B | {gi(ab['reclaimable_bytes'])} | {gi(ab['available_after_bytes'])} | {gi(ab['gap_bytes'])} | {gi(ab['surplus_bytes'])} |

df（{now}）：
~~~text
{df.rstrip()}
~~~
开工/home可用30,505,807,872B。后续df变化来自新增小型证据及其他写入，不是本任务清理收益。

## 6. 读了什么、没读什么与停止记录

已读：STATUS保留规则，65/74/78/79/85/87/96相关文档与输入清单，207处du及子目录，85的32个仓库位置与当前35处HEAD，解包/重放脚本引用，df/findmnt/lslocks/lsof，候选A和建议B逐文件inode/硬链接。reference-index.json给出文档行号，inventory.jsonl给出分类依据。

未读/未做：其他项目内部、QB/Gerrit与下载可用性、全部大RPM内容复核、全部源码未发布性重审（都保留）、不可读root目录内容；没有构建、转换、重新导出DWARF、删除、移动、压缩或锁操作。不能证明的大小与重建代价为UNKNOWN，不估算。

准备记录：生成报告程序的工具调用曾因JavaScript字符串引号产生SyntaxError；调用未执行、未写文件，修正一次后继续，原文见preparation-error.json。不涉及产品或分类判据修改。STOP无。权限UNKNOWN不是产品失败，也不产生删除许可。

97盘点 已结束 {now} status=PARTIAL（分类完成；权限盲区完整大小UNKNOWN）
"""
(B/"docs/bolt/97_disk_cleanup_inventory.md").write_text(doc)
status=B/"docs/bolt/STATUS.md"
heading="## 2026-11-14：97号磁盘清理盘点（不删除）"
assert heading not in status.read_text(),"STATUS heading already exists; do not append twice"
with status.open("a") as f:
 f.write(f"""
\n{heading}

见[97号](97_disk_cleanup_inventory.md)。只读盘点完成；权限盲区完整大小UNKNOWN，没有删除/移动/压缩或锁变更。/home项目A {gi(tot['home_project']['A']['observed_bytes'])}GiB、B ≥{gi(tot['home_project']['B']['observed_bytes'])}GiB、C ≥{gi(tot['home_project']['C']['observed_bytes'])}GiB（跨目录去重；共享ARM输入另列C ≥{gi(shared)}GiB，/var/tmp另盘）。只删A预计释放{gi(a['reclaimable_bytes'])}GiB、可用{gi(a['available_after_bytes'])}GiB，距186GiB缺{gi(a['gap_bytes'])}GiB；加两组有条件建议B后可用{gi(ab['available_after_bytes'])}GiB、富余{gi(ab['surplus_bytes'])}GiB。旧QB下载可用性未核实，仍B；当前74 gbs-root仍B，D report-stale依赖未解除，不计入建议释放。源码链/b0c1732c、源码保护备份、74材料、450归档及10调试输入/old-new产物、TU、profile原件、当前QB RPM全C。清理需另行批准，删除前重查完整占用/锁/挂载。96全量重放仍SKIPPED、PASS前不得触发QB。STOP无；工具调用准备语法错误一次已记录，不涉及产品判定。
""")
print("97文档 已结束",datetime.datetime.now().astimezone().isoformat(),"status=PARTIAL")
