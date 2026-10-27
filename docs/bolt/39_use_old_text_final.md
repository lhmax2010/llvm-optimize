# 39：发布参数采用 -use-old-text 的完整认证

完整构建、全部门禁、23包比较和90 TU均通过；许可之外的RPM内容差异为零。最终clang为152,532,296字节，比原布局缩小16.75%，RUNPATH为`$ORIGIN/../lib64`。运行时最大RSS相对ordinary的变化为-37.42%至-5.71%，下表按语言和目标分别列出。

## 1. 范围和源码身份

用户已决定采用 `-use-old-text`，该决策闭合；崩溃定位方案仍挂账。本轮在 detached HEAD 上 amend，没有创建分支。只在生产 helper 的 `OPTIONS` 末尾追加 `-use-old-text`，spec、Source1200、111+2 白名单、RUNPATH 修复、real 检查、工具并行和 cache-release 均保持不变。

| 项目 | 值 |
|---|---|
| 基线 BOLT | `ac112ebfd6e7983bdfd4c38dd156e6baba72731b` |
| 新 BOLT 提交 | `f308fe08eeaad4e219f8505449b88bd5f644ea8c` |
| tree | `214bd2ff9ec7680e045b36b5b8c7e873e953846d` |
| 不变的父提交 hybrid | `6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2` |
| BOLT Change-Id | `Ic98eab90cc017f127a66e1729b44fab8b8e8fb41` |
| 作者、提交者、Signed-off-by | `Hao Lin <hao.lin@samsung.com>` |

提交说明补充采用此参数及历史实验缩小约16.75%、目标文件不变的结论。没有修改全局 Git 配置。

证据目录：[oldtext-final-20261027](../../tools/bolt/results/oldtext-final-20261027/)。源码差异见 [source.patch](../../tools/bolt/results/oldtext-final-20261027/source.patch)，结构和常量检查见 [unchanged-production-constants.json](../../tools/bolt/results/oldtext-final-20261027/unchanged-production-constants.json)。

## 2. 前置认证和构建条件

- 318 项测试 PASS：既有317项加一个 OPTIONS 仅追加该参数的检查；其它生产函数 AST 与基线相同。
- gbs export PASS。Tizen RPM 4.14.1.1 对 x86 BOLT开、关、一行回退、armv7l、aarch64 五项解析 PASS。
- 关闭 BOLT 后，debug/release 两模式的展开结果分别与 ac112ebf 逐字节相同。
- 37号产品目录 SHA256SUMS 的35项全部通过，作为23包比较基线。

使用固定 `tizen-base-toolchain_20261013.024319` 的 packages/debug 两个仓库；build.conf SHA256 为 `e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945`。使用原配置 `temp/bolt-v4-20261021-disk-footprint/gbs_llvm_qb1202084.conf`，宏 `jobs 8`、`_smp_mflags -j8`、`_costomized_smp_mflags -j20`，外层 `--threads=30`。本地通过 GBS 构建，QB 使用 NGBS，该差异保留说明。spec 自身的 `mlgo_build_jobs` 默认值为6，因此普通Ninja和llvm-bolt实际均为 `-j6`；没有用外层jobs宏覆盖这个已有值。

新构建根位于 `/home/linhao/Toolchain/development/llvm-optimize/temp/oldtext-final-20261027/gbs-root`。systemd 用户 service 的 MemoryMax=24,482,967,552 B（本机 MemTotal减8GiB），swap=0、nice10、ionice2/7；不设内存准入或冻结，/home可用小于20GiB正常停止。资源规则只存在本地驱动，不进入发布代码。未在历史根执行 CMake/Ninja，未删除任何历史目录或构建根；仅发布流程按既定cache-release释放本轮缓存。

原文：[tests.stdout](../../tools/bolt/results/oldtext-final-20261027/tests.stdout)、[tests.stderr](../../tools/bolt/results/oldtext-final-20261027/tests.stderr)、[export-result.json](../../tools/bolt/results/oldtext-final-20261027/export-result.json)、[parse.stdout](../../tools/bolt/results/oldtext-final-20261027/parse.stdout)、[baseline-products-check.json](../../tools/bolt/results/oldtext-final-20261027/baseline-products-check.json)。

## 3. 完整构建和身份门禁

续跑的正常 `rpmbuild -ba --noprep` 返回0，产出22个二进制RPM和1个源码RPM。tool-plan、tool-verify均为113/113（111 BOLT+2 TF）；profile双门禁、BOLT标识节、strip、两次tiny、三处real、安全属性、RUNPATH/安装基线、compare-root、cache-release、最终post均PASS。三处real共24项，合计32.026258秒。Source1005转换225项PASS。

匹配统计精确为 N=23,592、M=144,032、S=0、U=1、Q=383；R=0.004238545331242318%，S/N=0，与37号一致。strip-all后、RUNPATH修改前SHA精确为`13a07cb7f84bd1ceda4d851c8bd71bddf7ef0c2d4864892eba64cbbb9a0350b8`，大小152,532,296 B。

最终candidate/安装实体SHA为`8c2429d870f421a29a9914458bc4d4ff2ce359a15e0bdd20f39bfb4580c40bdf`；ordinary SHA为`d5090159915657b235b96f1202c058e1efd1647d6a2225ac8fdb2906aeaa501d`，与37号ordinary相同。最终RUNPATH精确为`$ORIGIN/../lib64`，无RPATH、构建路径或空项。

缓存释放原文：

```text
BOLT_CACHE_RELEASE removed path=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache files=13163 allocated_bytes=21622669312 seconds=12.193443924000348
```

续跑cgroup峰值20GiB，oom/oom_kill均0；该值包含文件缓存，不能当作clang运行时RSS。资源受限引起的memory.events max计数不是OOM。证据：[qualification.json](../../tools/bolt/results/oldtext-final-20261027/qualification.json)、[build-result.json](../../tools/bolt/results/oldtext-final-20261027/build-result.json)、[完整合并日志](../../tools/bolt/results/oldtext-final-20261027/rpm-build.log)、[保全产品清单](../../tools/bolt/results/oldtext-final-20261027/preserved-products.json)。

## 4. 逐包比较、ELF和90 TU

23包全部PASS。比较脚本与37号第10.1节相同，两个自测也PASS：只有ar日期变化时单列通过；成员内容或其他字节变化必须失败。271个包内归档条目对应270个独立路径（libarcher_static.a重复出现在两个包）；不将它们计为“内容相同”。载荷mtime变化共2,471项，单独统计。原始RPM本身含构建元数据，不宣称RPM容器SHA相同。

| RPM | 允许内容变化 | 载荷mtime变化 | ar日期差异 | 许可外变化 |
|---|---:|---:|---:|---:|
| clang-22.1.8-1.x86_64.rpm | 1 | 66 | 0 | 0 |
| clang-debuginfo-22.1.8-1.x86_64.rpm | 0 | 27 | 0 | 0 |
| clang-devel-22.1.8-1.x86_64.rpm | 0 | 237 | 0 | 0 |
| clang-devel-debuginfo-22.1.8-1.x86_64.rpm | 0 | 4 | 0 | 0 |
| compiler-rt-22.1.8-1.x86_64.rpm | 0 | 105 | 45 | 0 |
| compiler-rt-debuginfo-22.1.8-1.x86_64.rpm | 0 | 17 | 0 | 0 |
| libllvm-22.1.8-1.x86_64.rpm | 0 | 3 | 0 | 0 |
| libllvm-debuginfo-22.1.8-1.x86_64.rpm | 0 | 4 | 0 | 0 |
| libomp-22.1.8-1.x86_64.rpm | 0 | 3 | 0 | 0 |
| libomp-debuginfo-22.1.8-1.x86_64.rpm | 0 | 6 | 0 | 0 |
| libomp-devel-22.1.8-1.x86_64.rpm | 0 | 1 | 1 | 0 |
| lldb-22.1.8-1.x86_64.rpm | 0 | 8 | 0 | 0 |
| lldb-debuginfo-22.1.8-1.x86_64.rpm | 0 | 16 | 0 | 0 |
| lldb-devel-22.1.8-1.x86_64.rpm | 0 | 34 | 0 | 0 |
| lldb-devel-debuginfo-22.1.8-1.x86_64.rpm | 0 | 7 | 0 | 0 |
| llvm-22.1.8-1.x86_64.rpm | 0 | 98 | 0 | 0 |
| llvm-debuginfo-22.1.8-1.x86_64.rpm | 0 | 85 | 0 | 0 |
| llvm-debugsource-22.1.8-1.x86_64.rpm | 0 | 1292 | 0 | 0 |
| llvm-devel-22.1.8-1.x86_64.rpm | 0 | 205 | 0 | 0 |
| llvm-devel-debuginfo-22.1.8-1.x86_64.rpm | 0 | 11 | 0 | 0 |
| llvm-static-devel-22.1.8-1.x86_64.rpm | 0 | 225 | 225 | 0 |
| python-clang-22.1.8-1.x86_64.rpm | 0 | 0 | 0 | 0 |
| llvm-22.1.8-1.src.rpm | 2 | 17 | 0 | 0 |

逐路径证据：[rpm-comparison/summary.json](../../tools/bolt/results/oldtext-final-20261027/validation/rpm-comparison/summary.json)及同目录逐包JSON。clang-debuginfo没有内容变化。唯一二进制内容变化是usr/bin/clang-22；源码包只有spec和helper。

直接ELF比较PASS：对照37号old-text实验的13a07cb7产物，最终版文件大小同为152,532,296 B，程序头和节头逐项相同；排除.dynstr/.dynamic后，147,614,253字节直接逐字节相同。原始.dynamic标签/数值没有变化，解码后的差异只有DT_RUNPATH字符串，最终为$ORIGIN/../lib64；不是重新布局或改写其它节。见[elf-literal-bytes.json](../../tools/bolt/results/oldtext-final-20261027/validation/elf-literal-bytes.json)、[elf-comparison.json](../../tools/bolt/results/oldtext-final-20261027/validation/elf-comparison.json)和两份readelf原文。

90 TU全部PASS：30个输入×3目标，ordinary和candidate依次占用同一路径/实体，完整.o逐字节相同，不移除.GCC.command.line。见[objects-current/result.json](../../tools/bolt/results/oldtext-final-20261027/validation/objects-current/result.json)。

## 5. 运行时内存和BOLT耗时

已完成1200次有效测量。C/C++各20文件×3目标，ordinary/candidate各5次，GNU `/usr/bin/time -v` 最大RSS，逐文件中位数后取几何平均。与37号第10.5节的现行参数结果并列。同实体路径、同resource-dir/loader、固定CPU2、关闭ASLR。

外部负载观察器每2秒检查本service外的进程；CPU至少0.5核或可读的进程I/O至少32MiB/s、持续10秒记为干扰。测量前等待12秒安静窗口；若干扰覆盖测量，则保留整批原始数据并重测完整五轮，不挑选样本。该观察有采样和/proc可读性边界，不等于证明全机绝对无干扰。


| 语言 | 目标 | 本轮old-text candidate/ordinary RSS | 变化 | 37号原布局比值 |
|---|---|---:|---:|---:|
| C | aarch64-tizen-linux-gnu | 0.637618431 | -36.24% | 0.639745763 |
| C | armv7l-tizen-linux-gnueabi | 0.625824558 | -37.42% | 0.630746944 |
| C | x86_64-tizen-linux-gnu | 0.721900655 | -27.81% | 0.732493770 |
| C++ | aarch64-tizen-linux-gnu | 0.921500512 | -7.85% | 0.922019580 |
| C++ | armv7l-tizen-linux-gnueabi | 0.921554156 | -7.84% | 0.922598366 |
| C++ | x86_64-tizen-linux-gnu | 0.942891443 | -5.71% | 0.946627699 |

接受的完整批次为`rss`；共执行1批，原始样本全部保留。逐文件5次中位数见[rss-medians.tsv](../../tools/bolt/results/oldtext-final-20261027/rss-medians.tsv)，汇总见[rss-comparison.json](../../tools/bolt/results/oldtext-final-20261027/rss-comparison.json)，负载判定见[rss-attempts.json](../../tools/bolt/results/oldtext-final-20261027/rss-attempts.json)。每次time -v、argv、load和频率记录在validation/rss/中。1200次测量的对象也全部通过逐字节检查。

| BOLT阶段 | 37号 | 本轮 | 差值 |
|---|---:|---:|---:|
| disk-report begin → compare-root | 883 s | 842 s | -41 s |
| llvm-bolt工具Ninja构建 | 108 s | 157 s | +49 s |

本轮重写进程的/proc观察窗口为44.045057秒，10ms采样的最大VmHWM为9,695,160 KiB；它是采样下界，不是wait4/GNU time的精确rusage。37号old-text实验为42.806872秒、GNU time最大RSS 9,686,616 KiB。37号原发布参数的重写没有同口径独立进程峰值记录，不能填充一个数值冒充对照；其bolt.log创建至最后写入约21.615秒，本轮对应41.878秒，仅作文件时间戳近似对照。资源限额与运行条件不同，不能把这些差值全部归因于参数。原始阶段行号和时间证据见[timing-comparison.json](../../tools/bolt/results/oldtext-final-20261027/timing-comparison.json)。

## 6. 操作记录、推送和保留

新根初始化、解析和构建按计划串行执行。准备期间只读查询发现当前sudo规则不允许`sudo -n true`，改为查询允许命令列表，确认既有build/chroot授权；未索要终端密码。查找工具验证JSON时先定位到实际文件`tool-build-verification.json`，在执行产品验证之前纠正名称，未改变产品门禁。

全部认证PASS后，以明确租约 `aa637c1b4a0f9ea9f6f0317cf035126eba85aeb7` 更新了唯一分支 `sandbox/lhmax2025/bolt_pgo`，推送返回0且无警告；推后ls-remote精确为`f308fe08eeaad4e219f8505449b88bd5f644ea8c`。未推refs/for、未创建分支、未操作QB。构建根和全部产物保留。


## 7. 主机重启后的续跑（2026-10-27）

首轮在普通构建期间被主机重启中断，最后保存的Ninja完成行为6,614/7,633；尚未进入BOLT或%install。用户报告系统崩溃并明确要求控制资源后继续，随后又授权适度放宽，但不占满CPU和内存。保存的内核日志未找到OOM kill原文，先前cgroup采样的oom/oom_kill为0，不能据此断言崩溃原因是OOM。现场、日志和全部已完成对象保留。

续跑使用同一新根里的正常`rpmbuild -ba --noprep`：仅跳过已经完成的%prep，沿用原始RPM环境、三个宏、spec和源码，不用short-circuit打包、不重新解包、不改发布代码。Tizen rpm的`--noprep`支持已核对。helper、profile和Source1005与源提交SHA重新核对一致，源码工作区clean。原日志见[pre-reboot](../../tools/bolt/results/oldtext-final-20261027/pre-reboot/)，续跑命令见[resume-command.json](../../tools/bolt/results/oldtext-final-20261027/resume-command.json)。

续跑初始CPUQuota=400%，用户随后要求适度放宽后改为1200%（本机nproc=20）；MemoryMax=20GiB、swap0、nice15、ionice idle，给系统保留约10.8GiB。初始的可选`io.stat`不存在使监控线程退出，原traceback保留；已启用独立低负载监控，允许可选统计项缺失，继续检查磁盘、OOM、profile精确统计和strip-all SHA，不重启构建。详见[resume-adjustments.json](../../tools/bolt/results/oldtext-final-20261027/resume-adjustments.json)。

首轮磁盘扫描曾多次超时，检查时只有一个du进程，未发现扫描累积。本地监控驱动优先级已在首轮下调；续跑不再周期性全树du，降低额外I/O。本任务不要求重新测量磁盘峰值，首轮采样原样保留，不由缺失样本推算峰值。续跑的各阶段耗时单独统计，包含中断和离线时间的日志累计秒数不能作为一次连续构建耗时。

构建结束后的普通 `/proc` 卸载返回32（`target is busy`），该挂载保留，未强制/懒卸载、未结束占用进程、未改VS Code配置。此后验证使用宿主loader访问本轮产物，不在历史根运行CMake/Ninja。构建根和全部产物均保留。


## 8. 最终推送和交付（2026-10-28）

推前工作区clean、detached HEAD、作者/提交者/Signed-off-by、Change-Id、tree和两级父提交均核对通过。远端推前精确为aa637c1，未使用其它强推方式。

```sh
git -c pack.threads=2 push --force-with-lease=refs/heads/sandbox/lhmax2025/bolt_pgo:aa637c1b4a0f9ea9f6f0317cf035126eba85aeb7 origin f308fe08eeaad4e219f8505449b88bd5f644ea8c:refs/heads/sandbox/lhmax2025/bolt_pgo
```

推送输出（CR进度换行及行尾空格仅为展示整理，原始字节保存在证据文件）：

```text
remote:
remote: Processing changes: refs: 1
remote: Processing changes: refs: 1, done
To ssh://review.tizen.org:29418/platform/upstream/llvm
 + aa637c1b4a0f...f308fe08eeaa f308fe08eeaad4e219f8505449b88bd5f644ea8c -> sandbox/lhmax2025/bolt_pgo (forced update)
```

推后远端原文：

```text
f308fe08eeaad4e219f8505449b88bd5f644ea8c	refs/heads/sandbox/lhmax2025/bolt_pgo
```

67619ec8之上的两个提交：

```text
6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2 67619ec8bbbac7238a6cfc33a481ccfbcd12206f cmake: use hybrid LLVM linkage on x86_64
f308fe08eeaad4e219f8505449b88bd5f644ea8c 6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2 packaging: optimize x86_64 clang with BOLT
```

推送前核对与原始输出：[push-preflight.json](../../tools/bolt/results/oldtext-final-20261027/push-preflight.json)、[sandbox-push-command.json](../../tools/bolt/results/oldtext-final-20261027/sandbox-push-command.json)、[sandbox-push.stderr](../../tools/bolt/results/oldtext-final-20261027/sandbox-push.stderr)、[sandbox-verified.json](../../tools/bolt/results/oldtext-final-20261027/sandbox-verified.json)。

QB软件包：`platform/upstream/llvm@f308fe08eeaad4e219f8505449b88bd5f644ea8c`。由用户启动，本会话未操作QB。

查找阶段曾按不存在的five-parse/result.json寻找解析汇总，随后定位到实际matrix.json/off-comparison.json；仅是读证据文件名更正，不涉及重跑或改变产品输入。318项测试原文摘要在tests.stderr（stdout是夹具输出），两者均保留。

**总结论：完整构建、精确身份、23包比较、90 TU和1200次RSS全部PASS；-use-old-text已采用，sandbox已更新为f308fe08，崩溃定位方案仍挂账，全部根和产物保留。**
