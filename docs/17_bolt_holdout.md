# BOLT 收益的留出集验证与中间对照

日期：2026-09-20。本轮只评估已经冻结的三个 clang；不再采集 profile、不再运行
BOLT、不改变优化参数。docs/16 的容量和训练集测量事实直接沿用。

**状态：BLOCKED_BY_NOISE，正式收益验证尚未完成。** 两对完整、同轮三工具链校准均
未通过原 3% 门禁：首次噪声底 **4.345326%**，暂停额外工作后的
重跑噪声底 **6.609160%**。没有运行正式轮，**目前没有合格的可对外汇报收益区间**。

已完成独立的 10 个 ARM 留出 TU、新 seed 20260920 的 A/B/C、三方交错测量与
20/20 配对对象逐字节检查。下文完整披露校准期诊断比值及其分解，**不把这些未通过
门禁的数据称为正式收益或已证实的泛化效果**。原 profile 和三个二进制均未改变。
证据：D1/calibration.json、D/calibration.json、E/formal-gate-negative.log。

## 1. 路径、产物与本次对照的含义

以下缩写均指本机已有路径；JSON、原始输出和大文件只保留在 `temp/`。

```text
W   = /home/linhao/Toolchain/development/llvm-optimize
E   = W/temp/bolt-holdout-20260920
D1  = W/temp/bench_results/bolt-holdout-20260920/attempt1（失败校准）
D   = W/temp/bench_results/bolt-holdout-20260920/attempt2
TC  = W/temp/toolchain-baseline/usr
Q   = W/temp/bolt-measurement-20260918/run
E16 = W/temp/bolt-final-20260918
R1  = W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0
B   = R1/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build
S   = /home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0
H   = W/tools/bench_inputs/holdout_tu
```

| 测量名称 | clang 文件 | SHA256 |
| --- | --- | --- |
| rpm-baseline | `TC/bin/clang-22` | `3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c` |
| stripped-norelocs-bolt | `Q/stripped/bin/clang-22` | `eccfb075bc3b2a6ca2bda5a2a6e68f6a29ba48b5586cb603f4b46080f656013e` |
| bolted | `E16/optimized/bin/clang-22` | `d6538b5ee1fdc429008b4481b651f994e354eabd55853666a0a9f0da03692e63` |

`stripped-norelocs-bolt` 按任务指定名称记录；**该文件实际保留重定位，并且未经
BOLT**，名称中的 `norelocs` 不描述文件属性。它正是本次已冻结 BOLT 产物的实际输入。
三组入口是 `E/toolchains/<名称>/bin/` 中的符号链接；全部以 `clang++` 名义测量。
`ld.lld`、`llvm-ar`、`llvm-ranlib` 都指向同一套 RPM 基线文件。

本轮将差异分解为：BOLT/剥离版 = 固定实际输入后的 BOLT 净收益；
剥离版/RPM = 重链及剥离路径的合并影响（不能再拆成各自贡献）；
BOLT/RPM = 从 RPM 起点出发的总影响。docs/16 把最后一项称作单变量对照不够严谨，
本报告修正这一解释；产物 `.o` 逐字节相同证明 codegen 一致，不证明编译器运行速度相同。

证据：`E/protected-before.json`、各阶段 `D/*-protected-after.json`、各轮 JSON 的
`toolchains`。原 profile `E16/profile-work/merged.fdata` 也在前后 SHA256 检查范围内。

## 2. 留出集构造与预处理

先按子系统锁定十个名额：AST、Parse、Driver、前端 CodeGen、IR、Analysis、
AArch64、X86、Object、ProfileData。前端 CodeGen 排除 `TargetBuiltins/`，覆盖 ARM
后端之外的前端工作。每组从 B/.ninja_log 的已有 x86 编译记录中取最后一次记录，
仅保留 2–12 秒的目标，选最接近 6 秒者，以对象路径打破同值。该范围覆盖原训练集
约 2.4–6.9 秒的历史记录，并容纳另一个子系统的较重文件。

选择器 `tools/select_llvm_holdout.py` 不运行候选编译器。选择时全部训练源码均被
排除；最终源文件集合与原训练十个文件的交集为空。完整候选池（包括未选中的目标）
与排序方法保存在 `E/selection/selection-evidence.json`，原始 `.ninja_log` 副本
在同目录 `ninja-log.txt`。固定清单 `H/selection.json` 的 SHA256：
`27c89a0dd45fb78cdf5879ba95e4d7eb8613dd5fb0eedab301bb74c67bf77e23`。
清单在首次候选性能检查前写定，后续没有替换文件。

| 分组 | 源文件（相对 llvm-22.1.8） | 历史 x86 编译秒 | RPM ARM 编译秒（单次检查） | .ii 字节 | 存储 |
| --- | --- | ---: | ---: | ---: | --- |
| ast | `clang/lib/AST/ParentMapContext.cpp` | 5.461 | 5.573 | 8411396 | 独立 holdout_tu 目录 |
| parse | `clang/lib/Parse/ParseDecl.cpp` | 4.958 | 4.756 | 9076128 | 独立 holdout_tu 目录 |
| driver | `clang/lib/Driver/Driver.cpp` | 4.482 | 5.082 | 4390703 | 独立 holdout_tu 目录 |
| frontend_codegen | `clang/lib/CodeGen/CoverageMappingGen.cpp` | 6.062 | 5.338 | 10722459 | E/collection |
| ir | `llvm/lib/IR/Metadata.cpp` | 4.742 | 5.250 | 4187255 | 独立 holdout_tu 目录 |
| analysis | `llvm/lib/Analysis/ScalarEvolution.cpp` | 7.349 | 9.361 | 5491931 | 独立 holdout_tu 目录 |
| aarch64 | `llvm/lib/Target/AArch64/GISel/AArch64InstructionSelector.cpp` | 5.713 | 5.361 | 18902822 | E/collection |
| x86 | `llvm/lib/Target/X86/X86ISelDAGToDAG.cpp` | 5.346 | 4.646 | 19611787 | E/collection |
| object | `llvm/lib/Object/ELF.cpp` | 4.663 | 5.598 | 2839857 | 独立 holdout_tu 目录 |
| profiledata | `llvm/lib/ProfileData/InstrProfReader.cpp` | 4.038 | 4.364 | 5113537 | 独立 holdout_tu 目录 |

表中 RPM ARM 秒数来自固定清单的产物一致性检查，用于确认工作量可比；是单次检查，
不是正式性能结果。十个文件约 4.36–9.36 秒，因此均保留。检查证据：
`E/verify-stripped-norelocs-bolt/result.json`。

所有源码来自 `f111162e94aa48ed367c9d2c039456c70e7160ae`。已有
`collect_llvm_real_tu.py` 通过只读 `ninja -t compdb-targets` 提取命令；由 **RPM 基线**
clang++ 实际执行 `-E`，使用 ARM triple、S sysroot 与 `TC/lib64/clang/22`。
移除原 x86 专属选项、LTO 与生成对象/依赖文件的选项，重定位根内 include 路径，
保留宏定义及语义 flags；没有修改 LLVM 源码或生成配置头。
`E/collection/arm-predefined-macros.txt` 验证 `__arm__=1` 且没有 `__x86_64__`。
全部实际 argv、原始 argv、移除项、input SHA256 见 `E/collection/collection.json`，
也逐个写入 `H/*.flags.json`；十个预处理均成功。

H 是独立留出目录，没有写入训练用 `tools/bench_inputs/real_tu/`。
七个 `.ii` 各小于 10 MB，提交在 H；另外三个超过 10 MB，绝对路径为：

```text
/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-holdout-20260920/collection/llvm_frontend_codegen_CoverageMappingGen.ii
/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-holdout-20260920/collection/llvm_aarch64_AArch64InstructionSelector.ii
/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-holdout-20260920/collection/llvm_x86_X86ISelDAGToDAG.ii
```

对应 sidecar 用绝对 `input` 引用。迁移机器需要复制这三个输入并验证 SHA256。

合成负载固定新 seed **20260920**，scale **1/2/2**：A 为 320 个标准库模板实例，
B 为 800 个中等函数，C 为含 6000 个块的单函数。设计结构沿用历史生成器。
原生成器只有 B/C 消耗随机数，A 使用顺序模板 ID；因此为非默认 seed 给 A 增加
独立随机流，选择与训练 A 不相交的模板 ID。数量、头文件和模板结构不变，B/C 的
随机数流不受 A 影响。原 seed **73419** 在 scale 1/2 的输出与修改前生成器逐字节相同；
本轮 A/B/C 三个输入 SHA256 均与训练不同。证据：`E/synthetic-audit.json`、
`E/harness-tests.log`（13 项检查 PASS，含默认兼容、新种子确定性、三类均变化与 A ID 不重合）。

## 3. 同轮交错协议与正确性检查

每轮是 `bench_toolchain.py` 的**一次三工具链调用**，不是分开运行后拼表：
rpm-baseline 第一个、stripped-norelocs-bolt 第二个、bolted 第三个。
每个迭代、每个负载内依次测三者，下一迭代反向排序。RPM 基线为三者生成同一组
66 个夹具对象（B 的 64 片及 A/C 各一），所有轮次检查夹具内容 SHA256 相同。
新种子产生新夹具，与训练轮夹具不同；本轮三工具链及四个校准轮之间完全共享；正式轮尚未运行。

| 项目 | 固定值 |
| --- | --- |
| target / sysroot | `armv7l-tizen-linux-gnueabi` / S |
| 资源目录 | `TC/lib64/clang/22`，三个 clang 完全相同 |
| 动态 loader | `/lib64/ld-linux-x86-64.so.2` |
| library-path | `W/temp/toolchain-runtime-baseline/libxml2/usr/lib64`，独立解包库，不安装宿主 |
| CPU / ASLR | CPU 2；子进程 `setarch x86_64 -R` |
| 采样 | N=5，丢首次，4 个保留样本取 wall 中位数；同时记录 user/sys、min、SD、RSS |
| 内存 | 单进程 `prlimit --as=4294967296:4294967296`；可用内存不足 4 GiB 拒绝启动 |
| loadavg | 每次命令前后采集，阈值 10（nproc=20 的 50%） |
| lld / ar | 每样本 4096 / 1024 次，归一化每操作时间；lld `--threads=1` |
| 临时产物 | `/dev/shm`，每轮退出清理 |
| 校准门禁 | 45 个组合逐项两轮 wall 中位数差绝对值 ≤3%，各轮 CV ≤3%，保留样本无负载告警 |

测量方法与 docs/16 相同，未放宽阈值。输入、seed 及支持 seed 参数的代码发生变化，
故整个协议 hash 与历史不同，这是本轮留出评估的预期变化；本轮四次校准运行的协议、
工具身份、资源/系统头文件 hash 与夹具 hash 必须一致。所有比值分母均来自**同轮**。
历史 0.846042 只用于按任务要求讨论训练/留出差距，不用作本次计时分母。

在校准前，另用 `verify_compiler_outputs.py` 将每个留出 TU 分别编译为 ARM ELF
对象，比较 RPM/剥离版与 RPM/BOLT 两组，每组 **10/10 全文件逐字节 PASS**。
两边统一 `clang-22 --driver-mode=g++`，保持 `-frecord-gcc-switches`，不排除任何节区。
证据：`E/verify-stripped-norelocs-bolt/result.json`、`E/verify-bolted/result.json` 及
各自 `raw/commands.json`、`cmp` 原始输出。

测量前宿主原始内存、nproc、loadavg、按 RSS 排序的进程清单保存在
`D1/calibrate-host-before.txt` 与 `D/calibrate-host-before.txt`；准备阶段另有
`E/host-prepare.txt`。完整构建的 18 GiB 容量门禁没有修改，本轮也没有启动构建。

## 4. 校准失败、降噪尝试与资源记录

每轮 45 个组合（三工具链 × 13 个编译项及 lld/ar），每组合 N=5 丢首次。以下两对都完整结束，没有提前裁掉异常样本。

| 校准对 | 两轮最大中位数差 % | 第1轮最大 CV % | 第2轮最大 CV % | 失败组合/45 | 结果 |
| --- | ---: | ---: | ---: | ---: | --- |
| attempt1 | 4.345326 | 12.748469 | 3.423937 | 16 | FAIL |
| attempt2 | 6.609160 | 5.089892 | 4.236809 | 18 | FAIL |

第一对的 BOLT/AST 某个保留样本 wall 为 6.0799 秒，user+sys 为约 5.0183 秒，存在约 1.0616 秒未计入 CPU 的时间；A 的三组 CPU 时间也随迭代共同漂移。wall/CPU 缺口可由调度等待、I/O 等因素造成，**没有同步的调度/硬件计数证据，具体外部进程与根因 UNKNOWN**。
第一次失败后，将额外的文档生成、文件核对等本任务工作与测量分开，仅保留简短日志读取，在新目录 attempt2 重新跑完整两轮。没有增加 N、变更 CPU/ASLR、阈值、输入、flags 或抽取较好样本；没有停止其他应用或修改宿主配置。第二对仍失败，因此停止继续重复尝试，没有按收益高低挑选通过窗口。
第二对中，**同一个未被修改的 RPM llvm-ar**，rpm-baseline 入口的跨轮中位数变化最大。其两轮中位数和差值见下表。这不是 BOLT 对 llvm-ar 的收益，直接说明当前测量环境仍存在漂移。

| 诊断项 | 第一轮秒/操作 | 第二轮秒/操作 | 变化 % |
| --- | ---: | ---: | ---: |
| rpm-baseline/llvm-ar | 0.002324364 | 0.002477984 | +6.609160 |

门禁没有新增额外条件：`tools/bench_toolchain.py` 的 `calibration()` 与任务前提交 `6b69661be244776cadb2d6236445739ab510f151` 中的函数逐字节相同，证明见 E/gate-unchanged.json。条件仍为跨轮中位数差 ≤3%、各轮 CV ≤3%、保留样本无负载告警。两对不仅有 CV 超限，跨轮差本身也超过 3%。
E/attempt1-noise-diagnosis.json、E/retry-plan.json 保存异常样本与重跑依据；两对 calibration.json/.md 列出全部 45 个组合的门禁结果。实际执行 `measure --attempt attempt2` 的负对照被 `expected PASS, got FAIL` 拒绝，未调用基准台，未生成 formal.json，见 E/formal-gate-negative.log。

| 校准对/轮次 | 开始时间 | wall 秒 | 最大 CV % | 保留可疑样本 | 峰值 RSS KiB | scratch 已清理 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 1/1 | 2026-09-20T13:56:55+0800 | 1415.226 | 12.748469 | 0 | 1189516 | True |
| 1/2 | 2026-09-20T14:20:32+0800 | 1397.677 | 3.423937 | 0 | 1524048 | True |
| 2/1 | 2026-09-20T14:44:33+0800 | 1404.220 | 5.089892 | 0 | 1189516 | True |
| 2/2 | 2026-09-20T15:07:59+0800 | 1413.454 | 4.236809 | 0 | 1523448 | True |

四轮全部命令峰值 RSS **1,524,048 KiB（1.453445 GiB）**，单进程 AS 上限始终为 4 GiB。
保留样本的 loadavg 未触发阈值 10，仍未满足稳定性门禁；loadavg 检查不能替代实际校准。
本机 CPU：**Intel(R) Core(TM) Ultra 7 265**。CPU 2 的记录策略为 `{"scaling_governor": "powersave", "energy_performance_preference": "balance_performance", "scaling_max_freq": "5300000"}`。这是配置记录，不足以将漂移归因于具体频率或温度变化。

| 轮次 | 基准台开始时 MemAvailable GiB |
| --- | ---: |
| 1/1 | 21.300522 |
| 1/2 | 21.370472 |
| 2/1 | 21.676712 |
| 2/2 | 21.157120 |

两次启动前完整 `/proc/meminfo`、`free -g`、nproc、loadavg 和按 RSS 排序的进程清单见 D1/calibrate-host-before.txt、D/calibrate-host-before.txt。快照包括桌面门户、终端安全进程、Chrome、Code 等常驻进程；没有将其中某个进程定性为噪声来源。
四轮协议 hash：`7538a88f10d2888ba7fb9d94e357b29ec9fbedbbc7a8644ce7ee9b815a324e19`。
四轮夹具 hash：`6c527f46fd91cccbbfd590bb81b8bde9cbe13e9a8ee5269fa21c0f180c1dd5dc`。
四轮的 protocol、fixture、toolchains 均一致。与 docs/16 比较，排除输入/seed、生成器和基准台代码身份、夹具工具链标签后，其余 18 个协议字段全部相同，见 E/protocol-audit.json。

## 5. 三方逐项诊断比值与几何平均（不是正式收益）

**正式轮：NOT_RUN。** 下列是重跑校准的两个完整轮次，逐个比值均以同轮中位数为分母，没有使用历史绝对耗时。BOLT/剥离版对应净变化的定义，但这些估计尚未通过质量门禁，不能作已验证收益。
lld/ar 三组入口为相同二进制，仅作环境对照；不计入编译几何平均。

### 重跑校准 1（FAIL 对中的观测值）

| 负载 | RPM 秒 | 剥离版秒 | BOLT 秒 | BOLT/剥离版 | 剥离版/RPM | BOLT/RPM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 8.348138 | 8.301740 | 7.376104 | 0.888501 | 0.994442 | 0.883563 |
| B | 2.209678 | 2.204534 | 1.701233 | 0.771697 | 0.997672 | 0.769901 |
| C | 6.001517 | 6.012354 | 5.727088 | 0.952553 | 1.001806 | 0.954273 |
| real_llvm_aarch64_AArch64InstructionSelector | 5.426455 | 5.466525 | 4.666273 | 0.853609 | 1.007384 | 0.859912 |
| real_llvm_analysis_ScalarEvolution | 9.472836 | 9.490720 | 8.244317 | 0.868671 | 1.001888 | 0.870311 |
| real_llvm_ast_ParentMapContext | 5.697715 | 5.698613 | 4.823052 | 0.846355 | 1.000158 | 0.846489 |
| real_llvm_driver_Driver | 5.188386 | 5.195252 | 4.507151 | 0.867552 | 1.001323 | 0.868700 |
| real_llvm_frontend_codegen_CoverageMappingGen | 5.524407 | 5.559206 | 4.574933 | 0.822947 | 1.006299 | 0.828131 |
| real_llvm_ir_Metadata | 5.413933 | 5.379419 | 4.639625 | 0.862477 | 0.993625 | 0.856979 |
| real_llvm_object_ELF | 5.570786 | 5.576036 | 4.923550 | 0.882984 | 1.000942 | 0.883816 |
| real_llvm_parse_ParseDecl | 4.868306 | 4.871034 | 4.102854 | 0.842296 | 1.000560 | 0.842768 |
| real_llvm_profiledata_InstrProfReader | 4.446986 | 4.462988 | 3.780046 | 0.846976 | 1.003598 | 0.850024 |
| real_llvm_x86_X86ISelDAGToDAG | 4.786480 | 4.794787 | 4.078677 | 0.850648 | 1.001735 | 0.852125 |
| ld.lld | 0.004634 | 0.004654 | 0.004593 | 0.986799 | 1.004346 | 0.991088 |
| llvm-ar | 0.002324 | 0.002348 | 0.002318 | 0.986883 | 1.010329 | 0.997076 |

### 重跑校准 2（FAIL 对中的观测值）

| 负载 | RPM 秒 | 剥离版秒 | BOLT 秒 | BOLT/剥离版 | 剥离版/RPM | BOLT/RPM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 8.643983 | 8.684870 | 7.760271 | 0.893539 | 1.004730 | 0.897766 |
| B | 2.251198 | 2.250721 | 1.734794 | 0.770773 | 0.999788 | 0.770609 |
| C | 6.144997 | 6.133530 | 5.828183 | 0.950217 | 0.998134 | 0.948444 |
| real_llvm_aarch64_AArch64InstructionSelector | 5.479631 | 5.546422 | 4.716091 | 0.850294 | 1.012189 | 0.860659 |
| real_llvm_analysis_ScalarEvolution | 9.430742 | 9.472069 | 8.234614 | 0.869357 | 1.004382 | 0.873167 |
| real_llvm_ast_ParentMapContext | 5.752664 | 5.716947 | 4.760141 | 0.832637 | 0.993791 | 0.827467 |
| real_llvm_driver_Driver | 5.165703 | 5.176882 | 4.490784 | 0.867469 | 1.002164 | 0.869346 |
| real_llvm_frontend_codegen_CoverageMappingGen | 5.488669 | 5.483603 | 4.475809 | 0.816217 | 0.999077 | 0.815464 |
| real_llvm_ir_Metadata | 5.336739 | 5.462958 | 4.551593 | 0.833174 | 1.023651 | 0.852879 |
| real_llvm_object_ELF | 5.523411 | 5.505227 | 4.948879 | 0.898942 | 0.996708 | 0.895982 |
| real_llvm_parse_ParseDecl | 4.941392 | 4.903267 | 4.106368 | 0.837476 | 0.992284 | 0.831014 |
| real_llvm_profiledata_InstrProfReader | 4.483646 | 4.398530 | 3.695596 | 0.840189 | 0.981016 | 0.824239 |
| real_llvm_x86_X86ISelDAGToDAG | 4.720925 | 4.704805 | 4.022411 | 0.854958 | 0.996585 | 0.852039 |
| ld.lld | 0.004613 | 0.004609 | 0.004671 | 1.013602 | 0.999027 | 1.012615 |
| llvm-ar | 0.002478 | 0.002440 | 0.002400 | 0.983645 | 0.984494 | 0.968393 |

### 所有四轮的等权几何平均

同时列出首次失败校准，避免选择较好看的轮次。compile=13 个编译项，real=10 个真实 TU，synthetic=A/B/C。

| 校准对/轮次 | 集合 | BOLT/剥离版 | 剥离版/RPM | BOLT/RPM |
| --- | --- | ---: | ---: | ---: |
| 1/1 | compile | 0.856792 | 1.002070 | 0.858566 |
| 1/1 | real | 0.853397 | 1.001647 | 0.854802 |
| 1/1 | synthetic | 0.868205 | 1.003484 | 0.871230 |
| 1/2 | compile | 0.856983 | 1.000791 | 0.857661 |
| 1/2 | real | 0.851160 | 1.001312 | 0.852277 |
| 1/2 | synthetic | 0.876683 | 0.999058 | 0.875857 |
| 2/1 | compile | 0.857359 | 1.000872 | 0.858107 |
| 2/1 | real | 0.854303 | 1.001745 | 0.855794 |
| 2/1 | synthetic | 0.867624 | 0.997969 | 0.865861 |
| 2/2 | compile | 0.853993 | 1.000299 | 0.854248 |
| 2/2 | real | 0.849776 | 1.000124 | 0.849882 |
| 2/2 | synthetic | 0.868202 | 1.000880 | 0.868966 |

所有轮次的全部逐项比值在各自 calibration-comparison.json，首次两轮的逐项表也列在文末。诊断 JSON 明确标为 `UNCALIBRATED_DIAGNOSTIC`、`formal_result=false`，不会生成或冒充 formal.json。

## 6. 八个核心问题的回答与恢复条件

1. **留出清单与 seed：**第 2 节的十个新文件，与训练集合不重合；seed=20260920，scale=1/2/2。没有按候选收益换文件。
2. **噪声底：**两对分别 4.345326%、6.609160%，均不合格；第 4 节同时列 CV 与各轮资源记录。
3. **三种比值：**第 5 节已给出同轮三方诊断数据；正式比值 **UNKNOWN**，因为门禁拒绝正式轮。
4. **几何平均：**第 5 节列全部四轮、三个集合的诊断几何平均；不是合格的性能结论。
5. **与训练集 0.846042 的差距：**下表只是诊断值的算术差，不是过拟合比例，也不是显著性判断。旧训练数的分母是 RPM，本轮净比值分母是剥离版；另有负载分布变化与未达标的噪声，不能把差全部归因为训练集重合。

| 重跑轮次 | 留出 BOLT/剥离版（13 项诊断值） | 减去训练 0.846042 | wall 减少量比旧 15.3958% 少的百分点 |
| --- | ---: | ---: | ---: |
| 1 | 0.857359 | +0.011317 | +1.132 |
| 2 | 0.853993 | +0.007951 | +0.795 |

6. **非 BOLT 成分：**重跑两轮中间环的观测值如下，可以做乘法分解，但不足以证明它显著偏离 1.0，或认定精确影响为零。不能据此倒算 docs/16 当时的准确非 BOLT 贡献。旧 15.396% 按定义包含重链/剥离与 BOLT，不能直接称作已验证的纯 BOLT 收益。

| 重跑轮次 | 净比值 × 中间环比值 = 总比值（13 项） | 中间环观测 wall 变化 % |
| --- | --- | ---: |
| 1 | 0.857358997 × 1.000872322 = 0.858106889 | +0.087 |
| 2 | 0.853993066 × 1.000298789 = 0.854248230 | +0.030 |

7. **可对外汇报收益区间：UNKNOWN，当前不能给出合格区间。** 不能把两轮诊断数的跨度改称收益区间或置信区间。即使后续通过门禁，适用域也仅为本机、这些 LLVM 自身源码 ARM 编译 TU 与新种子合成负载，不等于 Chromium 或 Tizen 全平台包构建收益；全量验收仍需专用构建服务器。
8. **profile 泛化性：UNKNOWN（尚未完成合格验证）。** 诊断比值与训练数方向接近，但噪声门禁没有通过；不能据此宣布泛化良好或定量过拟合。同域未见文件也共享 LLVM/标准库头文件与编译器路径，不能等同于跨工程泛化。

**恢复条件：**先定位并消除残余漂移（具体来自执行环境还是测量链路仍 UNKNOWN；仅保持空闲未必足够）。在可验证稳定、无其他重负载/持续桌面活动的测量窗口中，保持同样 CPU 2、ASLR off、N=5、资源目录、sysroot 和夹具协议下重新跑完整两轮，逐项通过现有 3% 门禁后再启动正式轮。按本轮约 23 分钟/完整轮计，预留约 75 分钟完成两轮校准与正式轮。具体干扰进程 UNKNOWN；本轮没有停止其他应用，也没有改电源策略、sysctl 或系统配置。
当前没有合格正式数据，不能用历史耗时代替分母，也不能删除 lld/ar、改 CPU、增加 N 或更换留出文件来把当前结果包装为通过。当前未取得更稳定的运行条件，因此停止继续试跑。
保持现有 frozen artifact 和输入时，可用 `python3 tools/measure_bolt_holdout.py calibrate --attempt attempt3` 在新目录恢复。只有 PASS 后再执行同 attempt 的 `measure` 和 `summarize`。这两步的正式门禁保持原样。


## 7. 复现、证据与边界检查

从 W 运行，以下命令对应实际执行步骤。输出目录需要是新目录；已存在的证据不会覆盖。
`measure_bolt_holdout.py` 固定到本轮三件产物，首先校验给定 SHA256，不会调用 BOLT。

```bash
python3 tools/select_llvm_holdout.py \
  --build-root temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0 \
  --training tools/bench_inputs/real_tu/selection.json \
  --output temp/bolt-holdout-20260920/selection
python3 tools/collect_llvm_real_tu.py \
  --toolchain temp/toolchain-baseline/usr --loader /lib64/ld-linux-x86-64.so.2 \
  --build-root temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0 \
  --sysroot /home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0 \
  --candidates temp/bolt-holdout-20260920/selection/selection.json \
  --output-dir temp/bolt-holdout-20260920/collection \
  --publish-dir tools/bench_inputs/holdout_tu --cpu 2
python3 tools/measure_bolt_holdout.py prepare
python3 tools/measure_bolt_holdout.py verify
python3 tools/measure_bolt_holdout.py calibrate
python3 tools/measure_bolt_holdout.py calibrate --attempt attempt2
# 负对照：以下命令按预期被失败校准拒绝，没有启动正式轮
python3 tools/measure_bolt_holdout.py measure --attempt attempt2
python3 tools/measure_bolt_holdout.py summarize-calibration --attempt attempt1
python3 tools/measure_bolt_holdout.py summarize-calibration --attempt attempt2
```

`D1/calibrate-driver.log` 和 `D/calibrate-driver.log` 首行给出展开后的完整基准台命令；
每个目录都保存 `calibration-run1.json`、`calibration-run2.json`、`calibration.json`
及同名 Markdown 表。没有 formal.json。每轮 `*-raw/commands.json` 收录完整封装 argv、
原始 stdout/stderr 文件位置、wall/user/sys、RSS、前后 loadavg；`calibration-comparison.json/.md`
保留明确标记为未合格诊断的三方比值及等权几何平均。

## 8. 提交前自检

1. 留出集是否与训练文件重复？**否**，十个 source 交集为空；新 seed 使 A/B/C 三个内容 hash 都不同，默认 73419 历史输出不变。
2. 是否同轮交错三工具链、RPM 第一个提供夹具？**是**；四轮 invocation、toolchains、fixture_objects 和 commands.json 均可核对。
3. 两轮校准是否通过？**否**，两对都 FAIL；正式轮没有运行，可对外收益区间 UNKNOWN。
4. 是否用历史绝对耗时作本次分母，或筛掉异常样本？**否**。旧训练比值仅用于注明口径差异的诊断讨论；N=5 均只按原协议丢首次。
5. 是否重新采 profile、运行 BOLT、改 BOLT 参数、做 PGO 或完整重建？**否**；本轮只预处理/编译基准 TU、运行已有 lld/ar。
6. 是否改 spec、LLVM 源码、宿主配置或完整构建 18 GiB 门禁？**否**；E/protected-before.json 与 protected-final.json 完全一致，原有 spec 三处并发 diff 保持不变，见 E/initial-state.log、E/final-source-state.log。
7. 是否构建 Chromium 或向 Gerrit 推送？**否**，发布只到指定 GitHub origin/main。
8. 产物正确性与检查结果？**20/20 配对全文件逐字节 PASS**，两边统一 driver，不跳过节区；原基准台与新 seed 检查 13 项、新诊断/失败门禁检查 3 项，共 16 项 PASS。实际失败校准启动正式轮的负对照也 PASS（按预期拒绝），见 E/*tests.log、E/formal-gate-negative.log。
9. 发布证据？提交、git push、远端 HEAD、全部 main raw 内容与钉到提交号的报告的 SHA256 核对见 E/publication.log、E/publication-verification.json；完成回复列全部 raw 链接。

## 附录：首次失败校准的逐项诊断数据

以下同样未通过门禁，保留以避免只展示重跑数据；完整原始样本在 D1。

### 首次校准 1

| 负载 | RPM 秒 | 剥离版秒 | BOLT 秒 | BOLT/剥离版 | 剥离版/RPM | BOLT/RPM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 8.446301 | 8.560535 | 7.563937 | 0.883582 | 1.013525 | 0.895533 |
| B | 2.222621 | 2.219369 | 1.701691 | 0.766745 | 0.998537 | 0.765624 |
| C | 5.998441 | 5.989227 | 5.785488 | 0.965982 | 0.998464 | 0.964499 |
| real_llvm_aarch64_AArch64InstructionSelector | 5.484719 | 5.476539 | 4.634297 | 0.846209 | 0.998509 | 0.844947 |
| real_llvm_analysis_ScalarEvolution | 9.523719 | 9.567687 | 8.328834 | 0.870517 | 1.004617 | 0.874536 |
| real_llvm_ast_ParentMapContext | 5.718898 | 5.717092 | 4.844987 | 0.847456 | 0.999684 | 0.847189 |
| real_llvm_driver_Driver | 5.191127 | 5.191183 | 4.529269 | 0.872493 | 1.000011 | 0.872502 |
| real_llvm_frontend_codegen_CoverageMappingGen | 5.511428 | 5.534613 | 4.556195 | 0.823218 | 1.004207 | 0.826681 |
| real_llvm_ir_Metadata | 5.488962 | 5.453652 | 4.623967 | 0.847866 | 0.993567 | 0.842412 |
| real_llvm_object_ELF | 5.635809 | 5.637352 | 4.985311 | 0.884336 | 1.000274 | 0.884578 |
| real_llvm_parse_ParseDecl | 4.888768 | 5.002292 | 4.179035 | 0.835424 | 1.023221 | 0.854824 |
| real_llvm_profiledata_InstrProfReader | 4.515303 | 4.541313 | 3.845400 | 0.846759 | 1.005760 | 0.851637 |
| real_llvm_x86_X86ISelDAGToDAG | 4.848496 | 4.785525 | 4.122682 | 0.861490 | 0.987012 | 0.850301 |
| ld.lld | 0.004636 | 0.004610 | 0.004615 | 1.001113 | 0.994305 | 0.995411 |
| llvm-ar | 0.002364 | 0.002333 | 0.002355 | 1.009207 | 0.987045 | 0.996132 |

### 首次校准 2

| 负载 | RPM 秒 | 剥离版秒 | BOLT 秒 | BOLT/剥离版 | 剥离版/RPM | BOLT/RPM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 8.234413 | 8.210301 | 7.458491 | 0.908431 | 0.997072 | 0.905771 |
| B | 2.195345 | 2.190776 | 1.686977 | 0.770036 | 0.997919 | 0.768434 |
| C | 5.883000 | 5.895884 | 5.679024 | 0.963218 | 1.002190 | 0.965328 |
| real_llvm_aarch64_AArch64InstructionSelector | 5.382630 | 5.394698 | 4.574884 | 0.848033 | 1.002242 | 0.849935 |
| real_llvm_analysis_ScalarEvolution | 9.381719 | 9.389406 | 8.186834 | 0.871923 | 1.000819 | 0.872637 |
| real_llvm_ast_ParentMapContext | 5.612184 | 5.605170 | 4.747120 | 0.846918 | 0.998750 | 0.845860 |
| real_llvm_driver_Driver | 5.102702 | 5.100552 | 4.430191 | 0.868571 | 0.999579 | 0.868205 |
| real_llvm_frontend_codegen_CoverageMappingGen | 5.396296 | 5.411426 | 4.421580 | 0.817082 | 1.002804 | 0.819373 |
| real_llvm_ir_Metadata | 5.326781 | 5.326207 | 4.493430 | 0.843645 | 0.999892 | 0.843554 |
| real_llvm_object_ELF | 5.445087 | 5.466474 | 4.823411 | 0.882362 | 1.003928 | 0.885828 |
| real_llvm_parse_ParseDecl | 4.766994 | 4.795427 | 3.997442 | 0.833595 | 1.005965 | 0.838567 |
| real_llvm_profiledata_InstrProfReader | 4.380366 | 4.373991 | 3.707437 | 0.847610 | 0.998545 | 0.846376 |
| real_llvm_x86_X86ISelDAGToDAG | 4.706525 | 4.709440 | 4.020882 | 0.853792 | 1.000619 | 0.854321 |
| ld.lld | 0.004545 | 0.004545 | 0.004540 | 0.998728 | 1.000179 | 0.998907 |
| llvm-ar | 0.002321 | 0.002309 | 0.002345 | 1.015706 | 0.994692 | 1.010315 |
