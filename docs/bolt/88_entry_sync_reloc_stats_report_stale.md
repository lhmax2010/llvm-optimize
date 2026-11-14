# 88号：入口同步、2804 relocation 统计与 D report-stale

结论：**步骤1 PASS；步骤2 PASS；步骤3 STOP（未运行）**。W 执行入口与 B 已完全一致，两级清单通过，82号测试 **30/30**。T、D 各精确复现 **2804** 条不支持的重定位，组成相同。启动 D report-stale 前发现其他 GBS 重任务，未获取共享锁、未运行 BOLT。

## 1. 范围与资源

W=`/home/linhao/Toolchain/development/llvm-optimize`；B=`/home/linhao/Toolchain/development/llvm-optimize-bolt`。B 基点 `dc9a6ecbd2e31492ddf1d61275ced4d6b1fb6701`。全部操作串行运行于用户服务 `llvm-task88-preflight-20261114.service`，MemoryMax=4294967296、MemorySwapMax=0、Nice=19、IOSchedulingClass=3；分析后观测 MemoryPeak=688955392 B。没有为步骤3建立16GiB服务。时间采用运行环境 America/Los_Angeles（UTC−08:00）；此前报告的 +08:00 时间保留原样。

证据索引：[README](../../tools/bolt/results/night-88-20261114/README.md)。本轮不依赖 rg，不构建、不访问 QB/Gerrit、不改 LLVM、不删除文件。仅按授权同步 W 入口清单文件。87号因缺少 rg 的 STOP 属于准备错误，不是产品失败。

## 2. 步骤1：入口同步 PASS

完整目录比较只发现三处差异：`basedev/SHA256SUMS`、`basedev/provenance.json` 内容不同；顶层 `provenance.json` 在 W 缺失。没有清单外差异，没有 toolchain 差异，没有 W 独有文件。复制前对存在文件保存副本、大小和 SHA；缺失项明确记 null。

以 B 两级清单为准复制上述三项；逐文件 SHA 相同；同步后再次完整目录比较相同。W 顶层清单 **56 行 OK**，basedev 清单 **23 行 OK**。30项测试全部通过（3.146s）。dry-run PASS，只打印 argv/服务名/根目录，未启动构建；打印 `Linger=no` 警告符合入口行为。

证据：`entry/all-differences-before.json`、`entry/backup-manifest.json`、`entry/before/`、两级 `W-*-check.stdout`、`entry/30-tests.stderr`、`entry/dry-run.stdout`、`entry/result.json`。测试临时夹具原件保留本地，交付压缩副本 `entry/fixtures.tar.gz` 和逐文件清单。

```text
88步骤1 已结束 2026-11-14T01:46:23.352449-08:00 status=PASS
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
| toolchain | 19 R_X86_64_TLSGD | .rela.text | .text | 1536 |
| toolchain | 20 R_X86_64_TLSLD | .rela.text | .text | 415 |
| toolchain | 21 R_X86_64_DTPOFF32 | .rela.text | .text | 853 |
| basedev | 19 R_X86_64_TLSGD | .rela.text | .text | 1536 |
| basedev | 20 R_X86_64_TLSLD | .rela.text | .text | 415 |
| basedev | 21 R_X86_64_DTPOFF32 | .rela.text | .text | 853 |

两侧总数各 **2804，差值0**，无需调整筛选。全部位于 `.rela.text`→`.text`。名称虽包含 TLS，19/20/21 **不在 BOLT isTLSX86 的18/22/23跳过集合内**，也不在支持表内，因此到达 analyzeRelocation 返回 false 的分支。T成功通过支持类型筛选2101479条，D2101478条；两侧动态地址跳过各238377条，ALLOC重定位节跳过各238909条。两个 JSON 包含完整分组及每类前20个符号/偏移样例。

对重写的含义仅据源码：analyzeRelocation 在不支持类型时返回false（RewriteInstance.cpp:2479–2480），handleRelocation 增加 NumFailedRelocations 后返回（2911–2918），不继续该静态重定位的后续分析/注册逻辑。该事实不等于删除对应机器指令，也不能据此断言路径安全或告警“无害”。本步骤未运行BOLT、未生成重写产物。

```text
toolchain PASS 2804 [('R_X86_64_TLSLD', 415), ('R_X86_64_DTPOFF32', 853), ('R_X86_64_TLSGD', 1536)]
basedev PASS 2804 [('R_X86_64_TLSLD', 415), ('R_X86_64_DTPOFF32', 853), ('R_X86_64_TLSGD', 1536)]
88步骤2 已结束 2026-11-14T01:49:39.663503-08:00 status=PASS
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
STOP: other heavy tasks are running; D report-stale not started; shared lock not acquired.
88步骤3 已结束 2026-11-14T01:50:07.703364-08:00 status=STOP
```

下一最小动作：其他重任务结束后，重新执行身份/资源/输出目录/共享锁前置核对，再按已批准的87号计划和88号限制运行一次。本轮未自动重试。

## 5. 读过、未读与交付

已读：STATUS长期资源/共享锁规则；87号报告与保存的BOLT源码筛选链；87号report-stale计划；B/W入口完整目录和两级清单、82号测试；T/D输入ELF与其动态/静态重定位和符号字符串；/proc运行现场、systemd用户unit、df/meminfo；fea0fe46的ELF类型定义（只读Git对象）。

未读/未执行：QB/Gerrit网络、旧源码或构建树的编辑、任何完整构建、report-stale实际运行、新BOLT输出、此前2804逐条BOLT debug输出（不存在此次读取需求）。未把离线类型统计当作运行时stale分析。

一次只读查找误用了根目录 `STATUS.md`，原文 `grep: STATUS.md: No such file or directory`；随即改读实际 `docs/bolt/STATUS.md`。不涉及产品判定或统计脚本修改。统计一次完成，无反复调参；入口测试无重试。

步骤结束行原文如上。本报告于 2026-11-14T01:52:08.316832-08:00 整理；总体为 PARTIAL（步骤3 STOP），不是产品失败。
