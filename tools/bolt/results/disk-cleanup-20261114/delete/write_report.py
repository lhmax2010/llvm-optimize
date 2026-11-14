#!/usr/bin/env python3
import pathlib,json,subprocess,datetime,urllib.parse
D=pathlib.Path(__file__).parent;B=pathlib.Path.cwd()
def read(n):return json.loads((D/n).read_text())
def gi(n):return f"{n/1024**3:.3f}"
rs=read("deletion-results.json");post=read("postcheck.json");adm=read("replay-admission.json")
assert len(rs)==20 and all(r["status"]=="DELETED" for r in rs)
assert post["pass"] and all(r["pass"] for r in read("night-root-samples-after.json"))
assert adm["status"]=="SKIPPED"
q=subprocess.run(["df","-B1","/home"],capture_output=True,text=True,check=True)
now=datetime.datetime.now().astimezone().isoformat();available=int(q.stdout.splitlines()[1].split()[3])
(D/"df-final.json").write_text(json.dumps({"time":now,"argv":q.args,"stdout":q.stdout,"stderr":q.stderr,"available_bytes":available},ensure_ascii=False,indent=2)+"\n")
cg=subprocess.check_output(["systemctl","--user","show","llvm-task98-cleanup-20261114.service","-p","ControlGroup","--value"],text=True).strip()
cp=pathlib.Path("/sys/fs/cgroup")/cg.lstrip("/")
resource={"unit":"llvm-task98-cleanup-20261114.service","properties":subprocess.check_output(["systemctl","--user","show","llvm-task98-cleanup-20261114.service","-p","MemoryMax","-p","MemorySwapMax","-p","CPUQuotaPerSecUSec","-p","Nice","-p","IOSchedulingClass"],text=True),"memory.events":(cp/"memory.events").read_text(),"memory.peak":(cp/"memory.peak").read_text()}
assert "oom_kill 0" in resource["memory.events"]
(D/"resource-final.json").write_text(json.dumps(resource,ensure_ascii=False,indent=2)+"\n")
allocated=sum(r["allocated_bytes_before"] for r in rs);net=rs[-1]["after_df"]["available_bytes"]-rs[0]["before_df"]["available_bytes"];steps=sum(r["df_available_change"] for r in rs)
W="/home/linhao/Toolchain/development/llvm-optimize"
table="\n".join(f"| {r['number']} | {r['path'].removeprefix(W+'/temp/')} | {gi(r['allocated_bytes_before'])} | {gi(r['df_available_change'])} | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-{r['number']:02d}.json) |" for r in rs)
root_table="\n".join(f"| {r['path'].removeprefix(W+'/temp/')} | 存在 | "+(gi(r["actual_allocated_bytes"])+"；与97相同" if r.get("size_match") else r.get("size_sample",r.get("du_status","UNKNOWN")))+" |" for r in post["roots"])
cmd="\n".join(" ".join(r["argv"]) for r in rs)
times=[f"98步骤1 已结束 {read('check02/preflight.json')[-1]['time']} status=PASS（逐项记录时间；实际完成行05:28:49.883519-08:00）",
"98步骤1 已结束 2026-11-14T05:28:49.883519-08:00 status=PASS",
"98步骤2 已结束 2026-11-14T05:33:40.420436-08:00 status=PASS",
f"98步骤3 已结束 {post['time']} status=PASS",
f"98步骤4准入 已结束 {adm['time']} status=SKIPPED"]
summary={"cleanup":"PASS","deleted":20,"skipped":0,"allocated_bytes_removed":allocated,"per_item_df_increase_sum":steps,"first_to_last_delete_df_net_increase":net,"post_cleanup_available_bytes":post["df"]["available_bytes"],"final_available_bytes":available,"final_time":now,"replay":"SKIPPED","reasons":adm["reasons"],"preparation_corrections":1,"new_STOPs":[],"end_lines":times[1:]}
(D/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
doc=f"""# 98号：批准目录清理与96号重放准入

**清理PASS：批准的20项全部删除，0项跳过。96号真实输入重放SKIPPED：存在另一项目GBS重构建，且MemAvailable低于20GiB；未取锁、不等待、不重试、未运行重放、未回退sandbox。**

删除前占块合计 **{gi(allocated)} GiB**；从第一项删除前到最后一项删除后，df可用净增 **{gi(net)} GiB**。清理完成核对时可用 **{gi(post['df']['available_bytes'])} GiB**；最终记录 **{gi(available)} GiB**（{now}）。共享文件系统期间仍有其他写入，df变化不等于目录占块，具体差额没有逐项归因。97号“约199GiB”是按当时df的预测，不是本轮保证值。

| 步骤 | 结论 |
|---|---|
|批准清单与97核对|18个A＋2个指定B，20/20完全相符|
|删除前检查|20项大小与97逐字节数相等，偏差0%；无可见打开句柄/锁文件/内部挂载|
|删除|20/20成功，普通用户、nice19、IO idle；无通配符|
|原件与父目录核对|368项原件/工具检查通过，250个保留兄弟条目通过|
|96重放|SKIPPED；无产品实物PASS/FAIL结果，未触发回退条件|

[全部证据raw索引](../../tools/bolt/results/disk-cleanup-20261114/delete/RAW_LINKS.md)、[汇总JSON](../../tools/bolt/results/disk-cleanup-20261114/delete/summary.json)。

## 1. 授权、预检与一次准备修正

按2026-11-14授权，只处理97号A-list的18项和B-list中的qb-1221204-1221207、qb-1223601-1223602。98清单与97表格、inventory分区逐项集合核对；路径没有增减、没有用通配符展开删除目标。[批准清单](../../tools/bolt/results/disk-cleanup-20261114/delete/approved-paths.json)。

每项核对：真实目录、非软链接、realpath精确匹配、du占块与97相差不超过5%，并记录设备/inode；检查lsof（含cwd/root/mmap）、锁文件名称、lslocks、findmnt。所有偏差实为0。删除前再次检查inode、占用、持锁和挂载；所有查询成功。普通用户视图有权限边界，没有宣称完成root不可见进程的特权审计，也没有使用sudo。

原件检查使用97号retained-rpm-sources.json和dwarf-retained-inputs.json列出的路径，历史字节大小来自97使用的74/67原身份清单；包括72个RPM、264个.debug原件。十个调试输入和二十个old/new归档按97 replay-assets-current.json核对大小。两个平台工具另核对存在性；97对它们没有登记历史字节大小，本轮记录181072和251728字节，前后相同，不冒充已经与97未记录的大小比较。

首次准备脚本错误假定全部368项都有历史大小，在两个辅助工具处expected_bytes=None，误把18个A标SKIPPED；336个RPM/DWARF和30个重放输入/产物实际全部通过。**首次未执行删除**。按长期准备错误可修正一次规则，辅助工具沿用97的存在性判定，所有原始数据文件仍严格比较历史大小；重新完整预检20项通过。不改历史97结果，也未放宽任何真实原件大小差异。[原始误判](../../tools/bolt/results/disk-cleanup-20261114/delete/originals-before.json)、[修正说明](../../tools/bolt/results/disk-cleanup-20261114/delete/preparation-error.json)、[diff](../../tools/bolt/results/disk-cleanup-20261114/delete/preflight-preparation-fix.diff)、[最终预检](../../tools/bolt/results/disk-cleanup-20261114/delete/check02/preflight.json)。

删除前find逐项生成相对路径、大小、mtime和类型的gzip清单，20份均小于10MB，全部提交；没有只留本地的大清单。[清单索引及SHA](../../tools/bolt/results/disk-cleanup-20261114/delete/listings-index.json)。check02保留重跑记录；顶层listings是正式20份，原先19/20清单逐SHA相同才复用，没有覆盖不同结果。

## 2. 逐项结果

路径均相对W/temp。占块是被删目录的测量量；df增加是该项执行前后的实际观测，可能受其他写入影响，不能混同。

|序号|路径|删除前占块GiB|该项df增加GiB|结果|证据|
|---|---|---:|---:|---|---|
{table}

每项均使用普通用户执行下列明确argv，额外使用one-file-system保护；没有删除父目录，没有重试rm：
~~~sh
{cmd}
~~~

每项原始df、rm返回码/stdout/stderr、即时占用核对、inode检查及结束时间都在item-01至item-20.json。保留了local-full-r6-20261111-compare/toolchain/dwarf-proofs、各父目录的已发布结果、fifth-review的old/new/archives。B其他项和C保留范围未列入任何删除命令。

## 3. 删除后保护检查

20个批准路径全部不存在。368项检查全部通过：336个RPM/DWARF原件和30个重放输入/产物仍符合97所用大小；2工具前后大小相同。父目录中的250个非目标兄弟条目仍存在、inode一致；文件大小也一致，目录不把内部内容大小当成单文件大小。[完整postcheck](../../tools/bolt/results/disk-cleanup-20261114/delete/postcheck.json)。

|关键保留位置|存在性|大小核对GiB／抽查|
|---|---|---|
{root_table}

night-20261103的T/D evidence分别34537472/12144640 B，night-20261105/toolchain/evidence为31604736 B，均与97相同；未重新扫描巨大构建根全量大小。[补充抽查](../../tools/bolt/results/disk-cleanup-20261114/delete/night-root-samples-after.json)。保留原件没有重新全量哈希；本任务要求的是存在性与大小抽查，不冒充内容重新认证。

清理完成df：
~~~text
{post['df']['stdout'].rstrip()}
~~~

最终df（{now}）：
~~~text
{q.stdout.rstrip()}
~~~

## 4. 96号重放：SKIPPED

准入时间：{adm['time']}；仅检查一次，不等待、不重试。

|条件|观测|结果|
|---|---|---|
|无其他gbs/rpmbuild/ninja/llvm-bolt|gbs PID {adm['heavy_processes'][0]['pid']}，m1-ffmpeg-a32-20261114-fix1.scope|不满足|
|/home≥30GiB|{adm['home_available_bytes']} B（{gi(adm['home_available_bytes'])} GiB）|满足|
|MemAvailable≥20GiB|{adm['MemAvailable_bytes']} B（{gi(adm['MemAvailable_bytes'])} GiB）；阈值21474836480 B|不满足|
|共享锁立即可得|其他条件已失败，未尝试|NOT ATTEMPTED|

[准入原文](../../tools/bolt/results/disk-cleanup-20261114/delete/replay-admission.json)。进程属于另一项目llvm_autofdo_bolt_agent；只读取准入所需/proc信息，没有进入它的构建目录、发信号或干预。未启动16GiB重放服务，也未执行450归档、10调试归档或3853成员转换比较。此前119/119测试不能替代本次未运行的真实重放。

本次没有实物差异或新增拒绝，没有触发“b0c1732c用lease退回ecb2dec7”的条件；**未访问或修改sandbox/Gerrit/QB**。按96已记录状态，sandbox仍领先PS3一个提交，本任务没有新的远端SHA观测。真实输入重放PASS之前不得触发QB。

## 5. 资源、阅读范围和结束记录

清理、检查和交付串行使用llvm-task98-cleanup-20261114用户服务：MemoryMax4GiB、swap0、CPU400%、Nice19、IO idle。未OOM。16GiB/90分钟重放资源未使用。[资源记录](../../tools/bolt/results/disk-cleanup-20261114/delete/resource-final.json)。

读过：97分类、分区和原件清单；96续二及STATUS长期规则；74/67原身份大小记录；78驱动和census脚本（只读，为可能的重放准备）；批准路径的元数据与删除清单；进程、锁、挂载、df及meminfo。未运行产品转换、BOLT或构建；没有QB/Gerrit查询；未读取另一项目目录内容；未修改LLVM代码或分支；没有删除批准清单以外的历史路径。

本轮实际STOP：无。首次原件检查的脚本误标SKIPPED及全部原文保留，已通过一次准备修正闭合；重放SKIPPED是准入结果，不是产品FAIL。

~~~text
{chr(10).join(times[1:])}
~~~

98 已结束 {now} status=PASS cleanup=20/20 replay=SKIPPED
"""
(B/"docs/bolt/98_disk_cleanup_and_replay.md").write_text(doc)
status=B/"docs/bolt/STATUS.md";heading="## 2026-11-14：98号批准清理与重放准入"
assert heading not in status.read_text()
with status.open("a") as f:f.write(f"""
\n{heading}

[98号](98_disk_cleanup_and_replay.md)：清理PASS，97号18个A及两组批准B共20/20删除，0跳过；占块合计{gi(allocated)}GiB，首项删除前至末项后df可用净增{gi(net)}GiB。清理完成可用{gi(post['df']['available_bytes'])}GiB，最终记录{gi(available)}GiB（{now}，共享文件系统仍有其他写入）。368项原件/工具检查、250个保留兄弟条目及关键C目录抽查通过；没有删除父目录、其他B或C。336原RPM/DWARF+30重放输入/产物严格比较历史大小，2辅助工具97仅登记存在性；首次脚本混淆记录类型的误判已保留并修正一次，无真实原件变化。

96真实重放SKIPPED：{adm['time']}另一项目gbs PID {adm['heavy_processes'][0]['pid']}运行，MemAvailable {gi(adm['MemAvailable_bytes'])}GiB<20GiB；空间{gi(adm['home_available_bytes'])}GiB满足。未取共享锁、不等待/不重试、未启动重放；无sandbox回退、无LLVM/Gerrit/QB操作。b0c1732c全量实物不变证明仍未完成，PASS前不得触发QB。今后复跑依赖已清理展开副本的旧脚本，须从97列出的C原件重新生成副本，不能把路径已删除视为产品错误。全部STOP：无。
""")
print(json.dumps(summary,ensure_ascii=False,indent=2))
