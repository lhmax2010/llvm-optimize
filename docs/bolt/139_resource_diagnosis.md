# 139-D 本机资源诊断与低内存构建档位

**结论：N2、G4、G5、N4 在实测约 19 GiB MemAvailable 时可按 15 GiB 限额、编译 4 / ThinLTO 4 / 链接 1 准入。G6 需要主机当时至少有 22 GiB MemAvailable。** 133-N 曾达到 22.70 GiB，138-N 最高为 20.22 GiB。两段记录均无法证明另一项目是内存下降的原因。

编排和离线 profile 技能已更新。59 项单测全通过，Tizen RPM 4.14.1 对 PS5、R、I 的三组展开及 CMake 参数核对通过，技能目录扫描零命中。本次没有配置或构建 LLVM，低内存档位尚无实测耗时或产物 SHA 对照。

## 1. 本机一次性采样

2026-11-19 20:01:51 PST（UTC−08:00）。Intel Core Ultra 7 265，系统可见 20 个物理核和 20 个逻辑 CPU，每核 1 线程。任务单元 CPUQuota 100%。交换来自 `/swap.img`，任务服务禁用 swap。[快照](../../tools/bolt/results/task139-d/snapshot.json)

|字段|字节|GiB|
|---|---:|---:|
|MemTotal|33,072,918,528|30.80|
|MemAvailable|13,647,409,152|12.71|
|Cached|3,783,852,032|3.52|
|Shmem|1,031,651,328|0.96|
|SReclaimable|5,650,743,296|5.26|
|AnonPages|16,009,527,296|14.91|
|SwapTotal|4,294,963,200|4.00|
|SwapUsed|3,293,339,648|3.07|

tmpfs 以 `df -B1 -t tmpfs` 采样。`/dev/shm` 使用 81,514,496 B，`/run` 使用 2,928,640 B，`/run/lock` 使用 8,192 B，`/run/user/1000` 使用 319,488 B。`df` 和 `/proc/meminfo` 的 `Shmem` 统计范围不同。

进程归属按 `/proc/<pid>/cwd` 落点判断，RSS 可能重复计算共享页。PID 2407 和部分 `code-insiders` 的 cwd 不可读。采样未见 `gbs`、`rpmbuild`、`ninja`、`llvm-bolt` 或 `ld.lld` 进程名。[含 cwd 的原始快照](../../tools/bolt/results/task139-d/snapshot.json)

|序|PID|用户|命令名|RSS B|RSS GiB|按 cwd 归属|
|---:|---:|---|---|---:|---:|---|
|1|10039|linhao|`code-insiders`|5,535,645,696|5.16|其他|
|2|2407|root|`epp-client-daem`|2,445,803,520|2.28|UNKNOWN（cwd 不可读）|
|3|1705805|linhao|`code-insiders`|662,454,272|0.62|UNKNOWN（cwd 不可读）|
|4|1760284|linhao|`code-insiders`|637,898,752|0.59|UNKNOWN（cwd 不可读）|
|5|2357228|linhao|`code-insiders`|637,546,496|0.59|UNKNOWN（cwd 不可读）|
|6|2370200|linhao|`chrome`|634,953,728|0.59|其他|
|7|2369040|linhao|`chrome`|542,400,512|0.51|其他|
|8|2359070|linhao|`chrome`|524,316,672|0.49|其他|
|9|2358593|linhao|`chrome`|463,462,400|0.43|其他|
|10|2357007|linhao|`code-insiders`|369,012,736|0.34|UNKNOWN（cwd 不可读）|
|11|2355493|linhao|`chrome`|367,681,536|0.34|其他|
|12|2357813|linhao|`code-insiders`|338,259,968|0.32|UNKNOWN（cwd 不可读）|
|13|2355030|linhao|`code-insiders`|311,300,096|0.29|UNKNOWN（cwd 不可读）|
|14|5678|linhao|`code-insiders`|257,019,904|0.24|UNKNOWN（cwd 不可读）|
|15|9812|linhao|`code-insiders`|250,486,784|0.23|UNKNOWN（cwd 不可读）|
|16|2357205|linhao|`code-insiders`|248,975,360|0.23|其他|
|17|2358012|linhao|`code-insiders`|240,578,560|0.22|其他|
|18|1705720|linhao|`code-insiders`|238,469,120|0.22|其他|
|19|2355230|linhao|`code-insiders`|232,964,096|0.22|其他|
|20|2370258|linhao|`chrome`|231,284,736|0.22|其他|

## 2. 夜间内存与另一项目活动

[完整采样 TSV](../../tools/bolt/results/task139-d/memavailable.tsv) 保留原时区、每次检查时间、阶段、采样类型和整数 B 值。读取两次编排的 `startup.json`、阶段状态 JSON 的 `admission`/`end_measurement`、`resources.jsonl` 及最终 `summary.json`，保留不同来源的同秒记录。[133-N](133_night_validation.md) · [138-N](138_night_validation.md)

|记录|样本数|MemAvailable（GiB）变化|
|---|---:|---|
|133-N，11 月 18 日 PST|235|07:39:59 启动 19.32，07:44:59 重查 21.72，08:25:06 到 22.58，08:30:06 最高 22.70，09:57:12 G6 依赖跳过时为 22.58，10:27:19 N4 最后重查为 22.62。|
|138-N，11 月 19 日 PST|160|00:24:02 启动 20.22，00:34:02 为 19.39，00:49:02 为 18.88，00:58:19 G3 采样最低 17.22，00:58:24 G4 准入为 18.78，01:28:30 G6 依赖跳过时为 18.95，01:58:37 最后重查为 19.05。|

133-N 启动前的即时检查见到 `gbs`、`rpmbuild` 进程名，记录不足以判定归属。138-N 阶段的进程采样覆盖本项目子单元。用户单元的 `WorkingDirectory` 或 `ExecStart` 能判定下表驱动属于另一项目。两次曲线期间是否有该项目的 `gbs`、`rpmbuild`、`ninja` 子进程仍是 **UNKNOWN**，用户 journal 无法覆盖每个未受 systemd 管理的进程。[用户单元、timer](../../tools/bolt/results/task139-d/units.json) · [journal 摘录](../../tools/bolt/results/task139-d/journal.json)

|单元|采样时状态|历史开始（PST）|历史结束（PST）|TriggeredBy|
|---|---|---|---|---|
|afdo-m1-attempt04-driver.service|failed/failed|Mon 2026-11-16 23:35:56 PST|Mon 2026-11-16 23:39:03 PST|—|
|afdo-m1-attempt04-repair1.service|failed/failed|Mon 2026-11-16 23:42:19 PST|Mon 2026-11-16 23:52:11 PST|—|
|afdo-m1-attempt05-driver.service|failed/failed|Tue 2026-11-17 00:41:21 PST|Tue 2026-11-17 00:46:44 PST|—|
|afdo-m1-attempt05-repair12.service|failed/failed|Tue 2026-11-17 00:49:14 PST|Tue 2026-11-17 01:06:17 PST|—|
|afdo-m1-attempt06-driver.service|failed/failed|Tue 2026-11-17 01:41:39 PST|Tue 2026-11-17 01:58:36 PST|—|
|afdo-m1-attempt07-driver.service|failed/failed|Tue 2026-11-17 02:54:21 PST|Tue 2026-11-17 03:28:28 PST|—|
|afdo-m1-attempt08-driver.service|failed/failed|Tue 2026-11-17 03:33:06 PST|Tue 2026-11-17 05:52:14 PST|—|
|afdo-m1-attempt09-driver.service|failed/failed|Tue 2026-11-17 07:37:45 PST|Tue 2026-11-17 08:19:12 PST|—|
|afdo-m1-attempt10-driver.service|failed/failed|Tue 2026-11-17 09:41:10 PST|Tue 2026-11-17 10:24:44 PST|—|
|kernel-k1a-base-0fac5de6-02.service|failed/failed|Tue 2026-11-17 19:43:30 PST|Tue 2026-11-17 19:43:30 PST|—|
|kernel-k1a-base-0fac5de6-03.service|failed/failed|Tue 2026-11-17 19:43:54 PST|Tue 2026-11-17 19:59:31 PST|—|
|kernel-k1c-kbase-01.service|failed/failed|Wed 2026-11-18 06:18:25 PST|Wed 2026-11-18 06:18:25 PST|—|

`launchpadlib-cache-clean.timer` 下次触发为 11 月 19 日 20:31:57 PST，`snap.firmware-updater.firmware-notifier.timer` 为 21:00:00 PST，均与另一项目无关。未找到该项目的用户 timer 或下次触发时间。记录显示 11 月 16 日 23:35 至 17 日 10:24 有 AutoFDO 多次尝试，17 日 19:43–19:59 及 18 日 06:18 有 kernel 驱动记录，无法确认固定的每晚构建或时段。

## 3. 并行参数及其作用

按 PS5 `7b05a137`、R `2b9031dd`、I `a4d024f0` 的 Git 对象只读核对 Toolchain x86_64 路径。[RPM 展开及 argv 差异](../../tools/bolt/results/task139-d/static-probes.json)

|参数|当前值和来源|不改产品源码的设置途径|
|---|---|---|
|GBS `--threads`、RPM `jobs`、`_smp_mflags`、`_costomized_smp_mflags`|138-N 按档位传给 GBS 和通用 RPM 宏。|沿用 `--threads`、`gbs --define`。|
|Ninja `-j`|PS5 `llvm.spec:75,542,544,547,666` 的 `mlgo_build_jobs` 默认 6，普通构建和 Part 2 工具均使用。R、I 同值。|`gbs --define 'mlgo_build_jobs N'`，离线 G5 直接传给 Ninja。|
|LLVM 编译池、链接池|PS5 `llvm.spec:451–452` 的 `LLVM_PARALLEL_COMPILE_JOBS=6`、`LLVM_PARALLEL_LINK_JOBS=2`，R、I 同值。LLVM `HandleLLVMOptions.cmake:39–86` 转为 Ninja 编译和链接池。|spec 显式给值，同名环境变量或 RPM 通用宏不能覆盖。启动脚本用 `_buildshell` 安装到本任务准备的 RPM 根，包装 LLVM 的 CMake 配置；离线重配置显式传参。|
|每个 lld 的 ThinLTO 线程|三份 spec 都没有显式指定。exe/shared flags 写在 spec，module 由规范化 `LDFLAGS` 初始化。`lld/ELF/Driver.cpp:1843–1865` 规定 `--threads=N` 同时提供非 LTO 线程和 ThinLTO 默认值，再由 `--thinlto-jobs=N` 覆盖后者。|包装层在 exe/shared/module 的 CMake linker flags 中注入 `-Wl,--thinlto-jobs=N`。现有 lld 通用线程设置不变。|
|TableGen、运行库和子构建|LLVM `HandleLLVMOptions.cmake:91–114` 支持 `LLVM_PARALLEL_TABLEGEN_JOBS` 及 `LLVM_RAM_PER_{COMPILE,LINK,TABLEGEN}_JOB`。三份 recipe 未设置，无证据表明所有独立 runtime/MLGO 子构建均受主链接池限制。|直接 CMake 配置可传这些设置。本次维持原样。`CMAKE_BUILD_PARALLEL_LEVEL` 只作用于 `cmake --build`。|
|BOLT 工具、改写和训练|工具构建受上述 Ninja 档位限制。PS5 `clang-bolt-helper.py:104` 的改写和技能中 G6/G7 均为 `--thread-count=1`，训练逐项执行。N4.2 独立工具子包保留 jobs 2。|工具可通过 Ninja 参数设置。既有产品 helper 的改写线程没有独立的 RPM 宏。本次保持。|
|归档转换|PS5 `llvm.spec:721,737,739` 在编译及 BOLT 后运行 `--jobs 4 --address-space-bytes 4294967296`。转换器 `llvm-static-archives-native.py:888,1044–1045` 使用线程池。|直接调用可传这两个参数，spec 当前没有独立的 RPM 宏。本次保持。|

包装器核实 `CMakeCache.txt` 和 `CMakeFiles/rules.ninja` 后写 `LLVM_BUILD_JOBS`，编排检查 RPM 日志中生效的 Ninja `-j`。G5 在重配置后提取 relink 命令。静态展开确认调度以外的 CMake 参数逐 token 相同，包括 I 的 `--build-id=sha1`、N2 的关闭开关和 G4 的 profile 参数。三个参数的代码语义只涉及并发，产物逐字节一致性仍需构建对照。74 号曾观察到单个 lld 约 13.3×10^9 B，10 GiB 的准入档低于该历史值，链接并发为 1 也不能保证构建通过。

## 4. 新档位和耗时估算

重步骤按 `min(MemAvailable − 4 GiB, 24 GiB)` 分配，向下按内存页对齐。N2、G4、N4 下限 10 GiB，G5 保留 15 GiB，G6 下限 18 GiB。G1 保留约 8.08 GiB 下限，轻阶段保留历史预算。MemoryMax 至少 20 GiB 时为 `6 / 6 / 1`，至少 14 且低于 20 时为 `4 / 4 / 1`，至少 10 且低于 14 时为 `2 / 2 / 1`。看门狗在 MemAvailable < 3 GiB 或 /home 可用 < 15 GiB 时只停止本任务当前子单元，后续重步骤跳过。[编排补丁](../../tools/bolt/results/task139-d/orchestration.patch) · [技能 dry-run](../../tools/bolt/results/task139-d/dry-run-19gib.json)

|步骤|主机 19 GiB 时 MemoryMax|下限|编译 / ThinLTO / 链接|时长估算|
|---|---:|---:|---|---|
|N2 PS5 关闭优化全构建|15 GiB|10 GiB|4 / 4 / 1|约 1:56–2:28，74 T 去掉 BOLT。|
|G4 PGO 正式构建|15 GiB|10 GiB|4 / 4 / 1|约 2:35–3:27，取历史 PGO 编译 6,176 s、安装 328 s，其余非 BOLT 阶段用 74 T 作代理。|
|G5 BOLT 工具与重链|15 GiB|15 GiB|4 / 4 / 1|工具约 7–11 分钟，另加重链接及 strip（UNKNOWN）。74 T 整个 BOLT 阶段 749 s，含其他步骤。|
|G6 BOLT 插桩、训练、merge-fdata|15 GiB，SKIPPED|18 GiB|准入后保持 BOLT 1 线程，逐项训练|本场景不启动。准入时历史三阶段共约 7 分 41 秒。|
|N4 综合候选完整构建|15 GiB|10 GiB|4 / 4 / 1|主包 4.1 约 2:08–2:41；4.2 子包 UNKNOWN。|

区间下端以历史耗时估算，上端仅将普通构建/工具生成按 `6/4` 乘数估算。133-N 的 G1 用 8.08 GiB 限额耗时 61 分 47 秒，按同一比例为约 93 分钟，仅指插桩 clang 和运行时的目标量级。74 T 普通构建的 3,940 s 含配置、编译和链接，单链接池排队、页缓存回收和实际配置差异可能让耗时超出区间。74 T 的归档转换采样峰值为 15,945,318,400 B（14.85 GiB，含缓存），已接近中档限额。[74 号资源数据](74_local_full_build_fa4f9978.md) · [133-N G1](133_night_validation.md) · [历史 PGO/BOLT 分项](../../tools/bolt/results/task131/pgo-pair-dry-run.json)

## 5. G6 可行性

18 GiB 子单元下限需要主机当时至少 **22 GiB** MemAvailable（23,622,320,128 B），还要通过 G6 磁盘准入。138-N 的最高可用内存距此少 1.78 GiB，典型 19 GiB 时少约 3 GiB。133-N 09:57:12 曾达到 22.58 GiB，当时 G6 因依赖被跳过。此次 12.71 GiB 的单次采样只够分配约 8.71 GiB，表中五步均低于下限。

无法从现有记录估计另一项目某晚空闲可释放多少内存。G6 应安排在该项目未运行、实测达到 22 GiB 且磁盘通过的时段，或在满足同等环境与资源的机器执行。历史 BOLT 插桩的 17,074,352,128 B 是阶段 cgroup 峰值，含文件缓存。对应单进程峰值尚未从该记录单独取证。

## 6. 核对与准备错误

- 59/59 单测通过，覆盖调度边界、G6 准入、3 GiB 看门狗、shell 传参、CMake cache 和 Ninja 池、原链接选项及冲突拒绝。技能格式校验通过。[单测原文](../../tools/bolt/results/task139-d/tests-final.txt)
- Tizen RPM 4.14.1 展开的 N2、G4、N4 均含 `ninja -j 4`。`%{__spec_build_cmd}` 展开到构建根内包装 shell。GBS 有 `--noinit`。在外层 Git 之外重新应用编排补丁，六个文件与实际副本逐字节一致。改后副本位于 `/home/linhao/Toolchain/development/llvm-optimize/archive/task139-d/orchestration`。[命令原文](../../tools/bolt/results/task139-d/integration.txt) · [静态核对](../../tools/bolt/results/task139-d/static-probes.json) · [补丁核对](../../tools/bolt/results/task139-d/orchestration-check.json)
- 用 134 号原正则不区分大小写扫描技能目录全部 23 个文件，零命中。[扫描规则和结果](../../tools/bolt/results/task139-d/skill-scan.json)
- 首次采集报 `FileNotFoundError: [Errno 2] No such file or directory: '/usr/bin/swapon'`。改读 `/proc/swaps` 后保存一次成功快照。[原文](../../tools/bolt/results/task139-d/prep-errors.txt)
- 加入安装包装器后，管道计划测试仍按首条命令找 GBS，报 `ValueError: '--threads' is not in list`。夹具改为按 GBS 可执行文件定位，保留 `--threads` 值断言并补 RPM 宏断言。重跑全部通过。[初次失败原文](../../tools/bolt/results/task139-d/tests-before-fixture-adjustment.txt)

读取了本机 `/proc`、`df`、用户单元及 journal、两次编排记录、74 号资源数据、131 号 dry-run、三份产品 spec 与相关 helper/转换器及 LLVM/lld 实现。另一项目目录和锁未访问。没有运行 LLVM 配置、编译、链接、BOLT 或任何远端构建。任务使用 2 GiB、swap 0、CPUQuota 100%、Nice 19、IO idle。无未解除 STOP。
