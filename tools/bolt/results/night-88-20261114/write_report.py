import datetime,hashlib,json,tarfile
from pathlib import Path
B=Path.cwd();E=B/'tools/bolt/results/night-88-20261114';stamp=datetime.datetime.now().astimezone().isoformat()
# Preserve source excerpts with their original line numbers, no historical file edits.
source=B/'tools/bolt/results/night-87-20261114/source'
parts=[]
for fn,ranges in [('bolt_lib_Rewrite_RewriteInstance.cpp',[(2470,2485),(2659,2675),(2829,2919)]),('bolt_lib_Core_Relocation.cpp',[(33,54),(244,246),(573,583)])]:
 lines=(source/fn).read_text().splitlines();parts.append(fn)
 for a,z in ranges:parts += [f'{i}: {lines[i-1]}' for i in range(a,z+1)]
(E/'source-filter-excerpts.txt').write_text('\n'.join(parts)+'\n')
# Test fixtures remain on disk; archive a copy for a compact, complete delivery.
with tarfile.open(E/'entry/fixtures.tar.gz','w:gz') as tf:tf.add(E/'entry/fixtures',arcname='fixtures')
fixtures=[{'path':str(p.relative_to(E)), 'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((E/'entry/fixtures').rglob('*')) if p.is_file()]
(E/'entry/fixtures-manifest.json').write_text(json.dumps(fixtures,indent=2)+'\n')
rows=[]
for project in ('toolchain','basedev'):
 r=json.loads((E/(project+'-reloc-census.json')).read_text())
 for g in r['groups']:rows.append(f"| {project} | {g['type']} {g['name']} | {g['relocation_section']} | {g['target_section']} | {g['count']} |")
counts={x:len((E/f'entry/W-{x}-check.stdout').read_text().splitlines()) for x in ('top','basedev')}
report=f'''# 88号：入口同步、2804 relocation 统计与 D report-stale

结论：**步骤1 PASS；步骤2 PASS；步骤3 STOP（未运行）**。W 执行入口与 B 已完全一致，两级清单通过，82号测试 **30/30**。T、D 各精确复现 **2804** 条不支持的重定位，组成相同。启动 D report-stale 前发现其他 GBS 重任务，未获取共享锁、未运行 BOLT。

## 1. 范围与资源

W=`/home/linhao/Toolchain/development/llvm-optimize`；B=`/home/linhao/Toolchain/development/llvm-optimize-bolt`。B 基点 `dc9a6ecbd2e31492ddf1d61275ced4d6b1fb6701`。全部操作串行运行于用户服务 `llvm-task88-preflight-20261114.service`，MemoryMax=4294967296、MemorySwapMax=0、Nice=19、IOSchedulingClass=3；分析后观测 MemoryPeak=688955392 B。没有为步骤3建立16GiB服务。时间采用运行环境 America/Los_Angeles（UTC−08:00）；此前报告的 +08:00 时间保留原样。

证据索引：[README](../../tools/bolt/results/night-88-20261114/README.md)。本轮不依赖 rg，不构建、不访问 QB/Gerrit、不改 LLVM、不删除文件。仅按授权同步 W 入口清单文件。87号因缺少 rg 的 STOP 属于准备错误，不是产品失败。

## 2. 步骤1：入口同步 PASS

完整目录比较只发现三处差异：`basedev/SHA256SUMS`、`basedev/provenance.json` 内容不同；顶层 `provenance.json` 在 W 缺失。没有清单外差异，没有 toolchain 差异，没有 W 独有文件。复制前对存在文件保存副本、大小和 SHA；缺失项明确记 null。

以 B 两级清单为准复制上述三项；逐文件 SHA 相同；同步后再次完整目录比较相同。W 顶层清单 **{counts['top']} 行 OK**，basedev 清单 **{counts['basedev']} 行 OK**。30项测试全部通过（3.146s）。dry-run PASS，只打印 argv/服务名/根目录，未启动构建；打印 `Linger=no` 警告符合入口行为。

证据：`entry/all-differences-before.json`、`entry/backup-manifest.json`、`entry/before/`、两级 `W-*-check.stdout`、`entry/30-tests.stderr`、`entry/dry-run.stdout`、`entry/result.json`。测试临时夹具原件保留本地，交付压缩副本 `entry/fixtures.tar.gz` 和逐文件清单。

```text
{(E/'step1.stdout').read_text().splitlines()[-1]}
```

## 3. 步骤2：源码筛选链与 ELF 流式统计 PASS

输入身份已重算 SHA、检查大小：

| 项目 | 字节数 | SHA256 |
|---|---:|---|
| T | 226816920 | ae3d837d862673b03c3c4718f6746f6986d8abe2078bad426b97905258b91a5c |
| D | 226782848 | bf15cf062439714651809cd3b5ca82619407081adca64ceb65699e6ccae50501 |

输入均为 `W/temp/local-full-r6-20261111-materials/<toolchain或basedev>/reference-relocs-clang-22`，只读。脚本 `reloc_census.py` mmap读取 ELF64 LE x86_64，逐条解析 REL/RELA，仅保存计数和每组前20个样例，不生成完整重定位文本。

筛选依次为：重定位节非 ALLOC；目标节 ALLOC；排除源码指定的 `.plt/.rela.plt/.got.plt/.eh_frame/.gcc_except_table` 目标；跳过 NONE；清除 converted bit 0x80；按源码 isTLSX86 仅跳过 TPOFF32/TPOFF64/GOTTPOFF；排除已有动态重定位的地址；按 Relocation.cpp 的15项 x86支持表分类。动态地址按 ELF动态标记 DT_RELA/DT_JMPREL（以及解析器支持的 DT_RELR）取得。本次实际只使用 `.rela.dyn`、`.rela.plt`，两侧动态地址各238909个。源码和行号摘录见 `source-filter-excerpts.txt`；数值名称取同一 fea0fe46 Git对象中的 `x86_64.def`；converted常量来自 `bolt/include/bolt/Core/Relocation.h:32`。

| 项目 | 类型 | 重定位节 | 目标节 | 不支持计数 |
|---|---|---|---|---:|
{chr(10).join(rows)}

两侧总数各 **2804，差值0**，无需调整筛选。全部位于 `.rela.text`→`.text`。名称虽包含 TLS，19/20/21 **不在 BOLT isTLSX86 的18/22/23跳过集合内**，也不在支持表内，因此到达 analyzeRelocation 返回 false 的分支。T成功通过支持类型筛选2101479条，D2101478条；两侧动态地址跳过各238377条，ALLOC重定位节跳过各238909条。两个 JSON 包含完整分组及每类前20个符号/偏移样例。

对重写的含义仅据源码：analyzeRelocation 在不支持类型时返回false（RewriteInstance.cpp:2479–2480），handleRelocation 增加 NumFailedRelocations 后返回（2911–2918），不继续该静态重定位的后续分析/注册逻辑。该事实不等于删除对应机器指令，也不能据此断言路径安全或告警“无害”。本步骤未运行BOLT、未生成重写产物。

```text
{(E/'step2.stdout').read_text().strip()}
```

## 4. 步骤3：STOP，report-stale未运行

启动前检查发现其他重任务：

- scope：`profgen-release-build-20261114c.scope`；
- PID29234：gbs，另一工作区 `llvm_autofdo_bolt_agent` 的 release构建；
- PID34255：rpmbuild；PID41183：`ninja -j 4`；
- 同一现场还观察到平台 clang++ 编译 LLVM/lldb 对象。父链原文保存在 `heavy-process-parents.json`，各进程状态/cgroup在 `heavy-processes-preflight.json`。

预检的完整scope列表、df、MemAvailable均已保存。/home available以 `df-preflight.txt` 为准。共享锁长期路径 `/home/linhao/Toolchain/development/heavy-stage.lock` 已从01号和历史执行脚本核实；因“没有其他重任务”前提不满足，本轮没有获取锁、等待锁、释放锁或干预其他进程。

读取了87号 `report-stale-plan.json`（输入、tool、loader、profile、正式参数和-report-stale）；未执行其命令，也没有新建 `W/temp/report-stale-20261114`。未删任何输出。以下项目均 **NOT RUN**：stale函数名单、N/M/S/U/Q/R和S/N的新观测、与83号计数对照、16GiB服务memory.peak/events、BOLT VmHWM和耗时/输出大小。旧测量不能当作本次实测。

STOP原文：

```text
{(E/'step3.stdout').read_text().splitlines()[0]}
{(E/'step3.stdout').read_text().splitlines()[-1]}
```

下一最小动作：其他重任务结束后，重新执行身份/资源/输出目录/共享锁前置核对，再按已批准的87号计划和88号限制运行一次。本轮未自动重试。

## 5. 读过、未读与交付

已读：STATUS长期资源/共享锁规则；87号报告与保存的BOLT源码筛选链；87号report-stale计划；B/W入口完整目录和两级清单、82号测试；T/D输入ELF与其动态/静态重定位和符号字符串；/proc运行现场、systemd用户unit、df/meminfo；fea0fe46的ELF类型定义（只读Git对象）。

未读/未执行：QB/Gerrit网络、旧源码或构建树的编辑、任何完整构建、report-stale实际运行、新BOLT输出、此前2804逐条BOLT debug输出（不存在此次读取需求）。未把离线类型统计当作运行时stale分析。

一次只读查找误用了根目录 `STATUS.md`，原文 `grep: STATUS.md: No such file or directory`；随即改读实际 `docs/bolt/STATUS.md`。不涉及产品判定或统计脚本修改。统计一次完成，无反复调参；入口测试无重试。

步骤结束行原文如上。本报告于 {stamp} 整理；总体为 PARTIAL（步骤3 STOP），不是产品失败。
'''
p=B/'docs/bolt/88_entry_sync_reloc_stats_report_stale.md';assert not p.exists();p.write_text(report);assert p.stat().st_size<=30000
status=B/'docs/bolt/STATUS.md'
with status.open('a') as f:f.write(f'''\n\n## 2026-11-14：88号\n\n[88号](88_entry_sync_reloc_stats_report_stale.md)：入口同步 PASS；补齐 W 的 basedev/SHA256SUMS、basedev/provenance.json 和顶层 provenance.json（覆盖前备份），完整目录一致、两级清单 OK、82号30/30、dry-run PASS。87号缺rg为准备错误，不是产品失败。本轮不使用rg。\n\nT/D 只读ELF统计各复现2804条：TLSGD1536、TLSLD415、DTPOFF32 853，全部.rela.text→.text，差值0；每类20个符号/偏移样例已保全。源码含义是跳过对应静态重定位的后续分析，不作“无害”判断。\n\nD report-stale **STOP/NOT RUN**：`profgen-release-build-20261114c.scope` 内 gbs/rpmbuild/ninja 正在运行，不满足无其他重任务前提；未取共享锁、未运行BOLT、未新建输出根、未删除或干预任何进程。原文：`STOP: other heavy tasks are running; D report-stale not started; shared lock not acquired.` 其他重任务结束后可重新核对前提执行已批准计划。本轮全部操作为单一串行4GiB/swap0/nice19/IO-idle服务。\n''')
print('88文档整理 已结束',stamp,'status=PARTIAL')
