# 58：PGO 资源测量结果

**启动时余量不足：可用 170.686 GiB，低于目标 177.548 GiB，差 6.861 GiB，可能触发运行中 20 GiB 停止线。** 用户已批准高于最低预算时启动。A/B/C已完成；D在原BOLT陈旧profile门禁失败（85.3% > 5%），未完成打包。没有OOM或磁盘不足，没有重试。

## 1. 本地预算调整与启动

沿用47号源码3ee2d847和固定Toolchain快照20261013.024319，未修改发布源码/spec/helper/Source。只修改本地budget常量/公式及警告记录：旧210.695GiB硬预算改为177.548GiB目标（仅记录）和151.290GiB最低启动预算（硬门槛），均由原始70,485,561,344B采样值计算，未使用四舍五入值反算。原12项加3项边界测试共15项通过。

预算 JSON 与controller首行原文：

```text
BUDGET_MARGIN_WARNING available_bytes=183273168896 target_budget_bytes=190640183706 shortfall_bytes=7367014810; possible 20GiB runtime stop
```

启动前无GBS/rpmbuild，full目录不存在；只执行以下指定命令一次，没有重试：

```sh
/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/pgo-resource-20261102/launch.sh full
```

服务 `pgo-controller-full-20261102.service` 启动后为active/running，初始MainPID=2328504。仅使用入口原有且已演练的免密sudo -n，用户已明确授权；没有另行手动提权或弹窗。观察脚本每30分钟只读进度与原始采样；服务结束时补读一次，不干预。

## 2. 获批临时副本清理

先限时低优先级du、lsof +D和可读/proc打开文件检查，再普通用户rm精确文件清单。所有json/txt/log/stdout/stderr、RPM、TU输入副本、脚本和旧validation保留；没有删除任何目录、构建根或原始产物。保留文件的inode/大小/mtime/SHA逐项复核通过。proc权限盲区数量如实记入cleanup-result.json，不提权。

|路径（W/temp/下）|删除前du B|删除副本数|df释放 B|结果|
|---|---:|---:|---:|---|
|night-20261103/toolchain/validation-02/rpm-bytes|14167117824|1088|14165794816|deleted-copies-reports-preserved|
|night-20261103/toolchain/validation-02/objects|2012569600|181|1318715392|deleted-copies-reports-preserved|
|night-20261103/basedev/validation-02/payload|350355456|1691|349851648|deleted-copies-reports-preserved|
|night-20261103/basedev/validation-02/objects|2012573696|181|1318801408|deleted-copies-reports-preserved|
|night-20261103/basedev/validation-02/release-check-resume/payload|1238134784|5073|1236660224|deleted-copies-reports-preserved|
|night-revalidation-20261104-tests-05|258723840|4|258510848|deleted-copies-reports-preserved|

按每组df差值合计 18,648,334,336 B；df包含同期其他写入，精确文件大小及完整命令另见清单。

## 3. 最终结果与失败原文

A 插桩 clang、B 的23份训练、C 的 profdata 合并通过。D 普通编译、普通安装、BOLT工具113项构建完成，随后 llvm-bolt 因陈旧 profile 超过5%主动返回1，%install失败。没有重试、手动续跑、改发布参数或放宽门禁；不是磁盘不足或OOM。本轮没有完成PGO+BOLT打包，不能作为完整构建通过的认证。

总结束行（controller.stdout:L2）：

```text
PGO_RESOURCE 已结束 2026-11-04T23:47:45.378355+08:00 status=failed reason=D: rc=1 reason=None; see /home/linhao/Toolchain/development/llvm-optimize/temp/pgo-resource-20261102/full/stage-D/evidence/D
```

GBS 原始失败日志 `full/stage-D/gbs-driver/local/repos/tizen_base_toolchain_standard/x86_64/logs/fail/llvm-22.1.8-1/log.txt.gz`：

```text
L23684 [ 7190s] + python3 -B /home/abuild/rpmbuild/SOURCES/clang-bolt-helper.py pipeline /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-bolt --debug-symbols
L23685 [ 7463s] BOLT_DISK_DIAGNOSIS {"cause": "not-disk", "step": "pipeline", "free_bytes": 86711771136}
L23686 [ 7463s] BOLT_GATE_FAILED: COMMAND_FAILED rc=1: /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-bolt (see /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt/rewrite/bolt.log)
L23688 [ 7463s] error: Bad exit status from /var/tmp/rpm-tmp.ZCXagu (%install)
```

根因日志 rewrite/bolt.log 全文如下（原件含行号摘录见 `failure-and-anchors.txt`）：

```text
L1 BOLT-INFO: shared object or position-independent executable detected
L2 BOLT-INFO: Target architecture: x86_64
L3 BOLT-INFO: BOLT version: <unknown>
L4 BOLT-INFO: first alloc address is 0x0
L5 BOLT-INFO: creating new program header table at address 0x7a00000, offset 0x7a00000
L6 BOLT-INFO: enabling relocation mode
L7 BOLT-WARNING: split function detected on input : _ZN10tensorflow22XlaCompiledCpuFunctionC2ERKNS0_10StaticDataENS0_9AllocModeE.cold. The support is limited in relocation mode
L8 BOLT-WARNING: Failed to analyze 1551 relocations
L9 BOLT-INFO: pre-processing profile using branch profile reader
L10 BOLT-WARNING: jump past end detected at 0x3ee314a in function _ZNK4llvm16AArch64InstrInfo18getBranchDestBlockERKNS_12MachineInstrE/1 : replacing with nop.
L11 BOLT-WARNING: jump past end detected at 0x4a05080 in function _ZNK4llvm12X86InstrInfo28convertToThreeAddressWithLEAEjRNS_12MachineInstrEPNS_13LiveVariablesEPNS_13LiveIntervalsEb/1 : replacing with nop.
L12 BOLT-INFO: forcing -jump-tables=move as PIC jump table was detected in function _ZN5clang4Sema25CheckTemplateArgumentListEPNS_12TemplateDeclENS_14SourceLocationERNS_24TemplateArgumentListInfoERKNS_16DefaultArgumentsEbRNS0_25CheckTemplateArgumentInfoEbPb
L13 Warning: request a ThreadPool with 20 threads, but LLVM_ENABLE_THREADS has been turned off
L14 BOLT-WARNING: 9 collisions detected while hashing binary objects. Use -v=1 to see the list.
L15 BOLT-INFO: 18343 out of 164430 functions in the binary (11.2%) have non-empty execution profile
L16 BOLT-INFO: 603 functions with profile could not be optimized
L17 BOLT-ERROR: 15638 (85.3% of all profiled) functions have invalid (possibly stale) profile. Use -report-stale to see the list.
L18 BOLT-ERROR: 99669657832 out of 101121718769 samples in the binary (98.6%) belong to functions with invalid (possibly stale) profile.
L19 FATAL BOLT-ERROR: stale functions exceed specified threshold of 5%. Exiting.
L20
```

工具返回1，helper没有执行成功日志的match_counts，也没有生成pipeline-result.json。日志直接给出N=18343、M=164430、S=15638、Q=603；没有U行，**U及正式R均UNKNOWN，不能把失败日志中缺失的可选计数当零**。S/N可直接由已打印数字计算，85.25323012%，与日志85.3%一致，远超原5%门槛。失效样本比例为98.6%，这是样本权重口径，不与函数数比例混用。

|同口径统计|43号非PGO Toolchain debug|54号T非PGO Toolchain debug|本轮PGO D Toolchain debug（失败日志）|
|---|---:|---:|---:|
|N（带profile函数）|23592|23592|18343|
|M（总函数）|144032|144032|164430|
|S（陈旧函数）|0|0|15638|
|U（忽略profile对象）|1|1|UNKNOWN|
|Q（不能优化函数）|383|383|603|
|R=(S+U)/(N+U)，百分比|0.004238545331%|0.004238545331%|UNKNOWN（成功解析未运行）|
|S/N，百分比|0%|0%|85.25323012%|

基线来自两次保全的pipeline-result.json原件，路径、SHA和原始计数见 `non-PGO-baseline-counts.json`，不是摘要估算。43号与本实验同为3ee2d847基线；54号T为9e39fa8a，存在固定参数/记录变化，因此用作同模式对照而非相同输入认证。Source1200和5%门槛未改：现有非PGO训练profile不适用于本次PGO输入，后续若继续需单独设计重新采样；本轮不实施。

## 4. A/B/C/D资源与耗时

已在总结束后执行47号原始 `report.py` 一次，exit0；完整输出 `report.stdout`、结构化结果 `full/resources-summary.json`，命令见 `report-command.json`。下列cgroup值来自每个独立服务结束前的内核memory.peak，**包含文件缓存**；进程VmHWM来自2秒抽样的所有可读PID，短进程或不可读进程可能漏采，不能冒充完整进程记账。通过loader启动时进程名为ld-linux-x86-64，真实工具见完整cmdline。

|阶段|状态|服务实测耗时s|cgroup峰值|最大进程VmHWM|进程/命令摘要|构建根边界du最大值|/home最小可用|
|---|---|---:|---|---|---|---|---|
|A|PASS|4068.547|7,227,248,640 B (6.731 GiB)|5,930,262,528 B (5.523 GiB)|ld.lld；ld.lld … -o bin/clang-22|26,444,713,984 B (24.629 GiB)|156,150,726,656 B (145.427 GiB)|
|B|PASS|201.930|1,481,818,112 B (1.380 GiB)|1,046,290,432 B (0.974 GiB)|ld-linux-x86-64；loader … 插桩clang-22，训练0|26,444,713,984 B (24.629 GiB)|155,218,534,400 B (144.559 GiB)|
|C|PASS|3.278|1,824,751,616 B (1.699 GiB)|1,976,971,264 B (1.841 GiB)|ld-linux-x86-64；loader … llvm-profdata merge|26,444,713,984 B (24.629 GiB)|155,177,299,968 B (144.520 GiB)|
|D|FAIL：BOLT stale profile|7472.449|21,703,991,296 B (20.213 GiB)|13,305,700,352 B (12.392 GiB)|ld.lld；ld.lld … -o bin/clang-22（普通编译）|64,830,697,472 B (60.378 GiB)|83,763,408,896 B (78.011 GiB)|

完整VmHWM的PID、进程名、命令原文和采样时间见 `process-peak-identities.json`；不是仅采llvm-bolt。服务起止时间见 `stage-times.json`。A耗时包含CMake配置和profile运行库/clang构建；B/C不包含前后记录SHA的时间；prepare服务另列，不混入A/D。

- stage-A/prepare：117.427s，cgroup峰值5,694,087,168 B (5.303 GiB)，结束根du7,022,018,560 B (6.540 GiB)。
- stage-D/prepare：124.614s，cgroup峰值5,790,814,208 B (5.393 GiB)，结束根du7,022,112,768 B (6.540 GiB)。

D子阶段：耗时同时列日志秒数差和采样器观察时间（服务开始/结束还包括GBS收尾），两者不混用。磁盘只是边界扫描，**所有真实连续峰值UNKNOWN**；普通编译退出/安装入口的扫描90秒超时，7,074,676,736B只是普通编译入口观测，不能据此说编译峰值只有6.59GiB。

|D子阶段|GBS日志区间/差值s|采样观察耗时s|阶段cgroup峰值|最大进程VmHWM|边界du观测|/home最小可用|
|---|---|---:|---|---|---|---|
|setup|开始→[268s]|276.447|4,478,197,760 B (4.171 GiB)|65,052,672 B (0.061 GiB) / gbs|7,074,676,736 B (6.589 GiB)|146,420,011,008 B (136.364 GiB)|
|ordinary-compile|[268s]→[6444s] / 6176|6176.712|21,703,991,296 B (20.213 GiB)|13,305,700,352 B (12.392 GiB) / ld.lld|UNKNOWN（出口扫描超时；入口6.589GiB）|104,091,758,592 B (96.943 GiB)|
|ordinary-install|[6444s]→[6772s] / 328|327.407|11,565,408,256 B (10.771 GiB)|65,052,672 B (0.061 GiB) / gbs|60,700,127,232 B (56.531 GiB)|90,878,791,680 B (84.637 GiB)|
|BOLT|[6772s]→失败[7463s] / 691|692.108|14,664,306,688 B (13.657 GiB)|9,267,929,088 B (8.631 GiB) / ld.lld|64,830,697,472 B (60.378 GiB)|83,763,408,896 B (78.011 GiB)|
|cache-release / archive-install / platform-post / packaging|NOT RUN|NOT RUN|UNKNOWN|UNKNOWN|UNKNOWN|UNKNOWN|

锚点：GBS:L345 %build=268s，L10888 %install=6444s，L16467 disk-report begin=6772s，L23683 tool-built=7190s，L23686失败=7463s。工具构建BOLT_NINJA_EXIT_0见L23081；tool-verify报告113/113。pipeline失败早于compare-root、cache-release、静态库转换、平台后处理、打包，不能用此前构建补全后续资源。

本地资源限制：MemoryMax=24,482,979,840B（MemTotal减8GiB），MemorySwapMax=0，CPUQuota=1200%，nice10，ionice best-effort/7；Ninja -j6，GBS外层threads30，三个宏仍为jobs8、_smp_mflags -j8、_costomized_smp_mflags -j20。每阶段systemd-command.json、command.json、service-result.json保存实际值，所有已运行阶段oom/oom_kill为0。systemd-run打印的Memory peak与内核采样值不是同一记录来源，表中统一使用内核memory.peak，不采用其14.4M/512K等尾行值。

C阶段进程VmHWM可大于cgroup记账峰值：两个量分别是进程驻留高水位和cgroup计费，不作加减或相等推断。VmHWM为PID生命周期高水位，阶段内采样不能消去它此前的驻留峰值。

## 5. 训练与profile磁盘数据

23/23训练PASS（13 ARM、10 AArch64），生成profraw **23份，共746,313,472 B (0.695 GiB)**。合并profdata **52,528,216 B (0.049 GiB)**，SHA256 `8c60fb561f4a445d1456da90cf7552a79a31abcbf3aab44f28710ad66dee1805`。两者在阶段A根外的profiles目录，单独列出，不混入根du。profdata另复制一份到D根内，该副本已计入D根占用，汇总时不再重复相加。

profraw阶段末保留量即已观察最大保留量；写入过程没有profile目录连续大小采样，因此瞬时峰值UNKNOWN。profdata亦只记录完成大小，合并过程中临时输出峰值UNKNOWN。完整每文件SHA/逻辑大小/分配大小见 `profile-final-inventory.json`，训练argv和每条结束标记见stage-A证据。工具llvm-profdata使用同源码的full-20261030已有版本，未额外编译目标，身份见profdata.json。

附带观察：A构建stdout:L1084起有830条 `LLVM Profile Warning: Unable to track new values: Running out of static counters.  Consider using option -mllvm -vp-counters-per-site=<n> to allocate more value profile counters at compile time.`，是A构建期间执行工具的警告。B的23条训练stdout/stderr未出现该警告，C合并成功。计数和首行见 `profile-runtime-warnings.json`；没有因此修改插桩参数、补采或重跑，也不把该警告直接认定为BOLT陈旧profile的原因。

## 6. 两根共存、磁盘下界与清理状态

A在B/C边界均为26,444,713,984B，D退出边界为64,830,697,472B。D运行期间A不再构建/写入，按这一不变前提组合的**边界记录最大共存根占用为91,275,411,456 B (85.007 GiB)**；这不是同时连续扫描的精确峰值，真实共存峰值仍UNKNOWN。没有把两个历史独立峰值直接当作同一时刻实测值。普通用户结束后du对两个根分别可见26,444,709,888B和64,830,693,376B，均exit1、有root属主目录权限盲区，只作下界；完整full目录可见94,775,939,072B，也有同样盲区。没有为补测另行sudo。

全过程/home最低可用 **83,763,408,896 B (78.011 GiB)**，时间 **2026-11-04T23:46:58.438352+08:00**，D/BOLT阶段，距20GiB停止线仍58.011GiB。结束后的df原文：

```text
Filesystem         1B-blocks          Used   Available Use% Mounted on
/dev/sda1      1967844950016 1781133635584 86674702336  96% /home
```

所有原始根、profraw/profdata和失败现场保留。原入口完成正常清理；audit.json中的mounts和remaining_stage_processes均为空。控制器最终failed是D的rc1，不是残留资源或OOM。没有重试、手动启动后续阶段、懒卸载或杀外部进程。

## 7. 证据与外推范围

证据根：`tools/bolt/results/pgo-resource-full-20261104/`。`full-provenance.json`记录所有已归档原件/副本大小、SHA256和gzip状态；大于1MiB文本压缩保存，原始现场不删。`SHA256SUMS`校验本目录交付文件。15项测试原文、预算警告、获批清理的文件清单/检查/df、启动前检查和一次启动命令均在同目录。日志未包含成功的pipeline报告时，明确记录缺失，不制造N/M/S/U/Q认证结果。

这些数值仅代表本机、固定Toolchain快照、3ee2d847及23份训练输入的这一次试验；源码A只构建插桩clang与profile运行库，不能视为一次完整插桩软件包构建。PGO输出大小、profile不兼容事实可用于后续设计；cgroup内存（含缓存）、耗时和磁盘边界下界受并发、内核和机器影响，不能直接当作QB三架构共享磁盘的容量上限。BOLT失败后的缓存释放/转换/打包资源尚无PGO数据。

结论：PGO A/B/C完成；D在原BOLT 5%陈旧profile门禁停止，整套PGO+BOLT构建未通过，保留现场等待用户决定。
