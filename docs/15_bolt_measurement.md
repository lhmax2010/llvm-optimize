# BOLT 插桩与吞吐实测

日期：2026-09-18。**容量结论：NO——本轮 18 GiB cap、4 个 BOLT 工作线程下，
本机插桩并自行采集 profile 的完整流程无法完成。** 剥离版及原始 ELF 均在
`llvm-bolt -instrument` 阶段触发 cgroup OOM，没有生成插桩二进制。

已完成全 10 TU 重测、BOLT 工具增量构建和调试信息剥离检查。由于插桩失败，
profile、优化重写、BOLT 后一致性验证、校准和正式基准均 **NOT RUN**。
这不等于已证明“拿到外部 profile 后，纯 BOLT 优化重写也一定超过 18 GiB”；
该阶段内存仍 UNKNOWN。本报告不把插桩峰值冒充优化重写峰值。

## 1. 范围与固定输入

直接沿用 [docs/14](14_bolt_feasibility.md) 已确认事实：带 `--emit-relocs` 的
clang-22 重链成功，wall 227.656 秒，lld VmHWM 9.760868 GiB，scope peak
10.451344 GiB，复用了热 ThinLTO cache。新 ELF 为 3,560,474,952 字节，SHA256
`6bfc85a8cce9952c4bcbea1a4ea169fb6199c379c18527df7d349f375e52caaf`。
本次不重复该重链。

路径缩写均为本机路径，原始材料不提交：

```text
W  = /home/linhao/Toolchain/development/llvm-optimize
E  = W/temp/bolt-measurement-20260918
R1 = W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0
B  = R1/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build
TC = W/temp/toolchain-baseline/usr
S  = /home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0
D  = W/temp/bench_results/baseline-20260917-rpm
原始 relocs ELF = R1/home/abuild/bolt-relocs-6a5e8e81bccb/clang-22
```

源码与 spec 不修改；R1 现在明确作为实验构建目录使用。原 RPM、TC、原始 relocs
ELF 独立保留，历史 CMakeCache、Ninja 图和关键 ELF 哈希先归档，再重新配置。
不做 PGO、完整 LLVM 重建、Chromium 构建或 Gerrit 推送。不修改 sysctl、capability，
不向宿主安装软件，本轮不执行 perf 采样。

## 2. 全 10 TU 逐字节门禁重测

上次差异已定性为测试调用问题。本次两边都以 `clang-22` 调用，并在共同参数前显式
加入 `--driver-mode=g++`。`-frecord-gcc-switches` 保留，使用完整对象文件 `cmp`，
没有排除 `.GCC.command.line` 或其他节区。

结果：**全部 10 个真实 ARM TU PASS**。证据：`E/relink-equality/result.json`、
`E/relink-equality/raw/commands.json`、`E/relink-equality-summary.json`。
每行保留两个对象的大小、SHA256 和实际 cmp 返回码；运行参数为同一个 S、TC clang 22
资源目录、原 `.ii`/sidecar flags、CPU 2、ASLR off、4 GiB 进程 AS 上限。两次编译
使用同一个临时 cwd 和输出路径，退出时删除临时目录。

| TU | 原始 relocs clang 对 RPM 基线 |
| --- | --- |
| llvm_arm_ARMISelLowering | BYTE_IDENTICAL |
| llvm_arm_ARMTargetTransformInfo | BYTE_IDENTICAL |
| llvm_codegen_MachinePipeliner | BYTE_IDENTICAL |
| llvm_codegen_SelectionDAG | BYTE_IDENTICAL |
| llvm_mc_AsmParser | BYTE_IDENTICAL |
| llvm_mc_MasmParser | BYTE_IDENTICAL |
| llvm_sema_SemaExprCXX | BYTE_IDENTICAL |
| llvm_sema_SemaStmt | BYTE_IDENTICAL |
| llvm_transforms_Attributor | BYTE_IDENTICAL |
| llvm_transforms_WholeProgramDevirt | BYTE_IDENTICAL |

## 3. BOLT 工具增量构建

改动前的 CMakeCache SHA256：
`e730feac1d721f5485c7ac3e981f3537110af5da1a4416c077e292e05b576a8b`。
改动后：`23848f0d9a5b46a83c8d2ed7b099d2e6e1d6e9935a4632fb7ba8ba2c8d1f0d55`。
原件与新件分别存 `E/incremental/before/`、`after-configure/`。

在原 build 目录内执行：

```bash
cmake -S /home/abuild/rpmbuild/BUILD/llvm-22.1.8/llvm -B . \
  '-DLLVM_ENABLE_PROJECTS=clang;lldb;clang-tools-extra;lld;compiler-rt;openmp;bolt'
```

原有 85 项配置仅项目列表按授权改变，其余逐项匹配。总计 12 项 cache 值变化，
包括新增 BOLT 配置与 CMake 内部文件计数，完整 before/after 为
`E/incremental/cache-changes.json`；验证结果为 `configuration-check.json`。
重新配置后关键 ELF 哈希未变。

缓存变化清单（`∅` 为原来没有该条目）：

| CMake 项 | 原值 | 新值 |
| --- | --- | --- |
| LLVM_ENABLE_PROJECTS | clang;lldb;clang-tools-extra;lld;compiler-rt;openmp | 原列表追加 ;bolt |
| LLVM_EXTERNAL_BOLT_SOURCE_DIR | 空 | /home/abuild/rpmbuild/BUILD/llvm-22.1.8/llvm/../bolt |
| LLVM_TOOL_BOLT_BUILD | FALSE | TRUE |
| BOLT_BUILD_TOOLS | ∅ | ON |
| BOLT_ENABLE_RUNTIME | ∅ | ON |
| BOLT_TARGETS_TO_BUILD | ∅ | AArch64;X86 |
| BOLT_INCLUDE_DOCS | ∅ | OFF |
| BOLT_CLANG_EXE / BOLT_LLD_EXE | ∅ / ∅ | 空 / 空 |
| BOLT_TOOLS_INSTALL_DIR | ∅ | bin |
| BOLT_TOOLS_INSTALL_DIR-ADVANCED | ∅ | 1 |
| CMAKE_NUMBER_OF_MAKEFILES | 667 | 685 |

该版本的 `perf2bolt` 不是单独 Ninja 目标，而是 `llvm-bolt` 的 POST_BUILD 符号链接：
`llvm/bolt/tools/driver/CMakeLists.txt:30`，以及 B/build.ninja 的 POST_BUILD 行。
实际请求目标为 `ninja -j4 llvm-bolt merge-fdata`，由该规则同时生成 perf2bolt。
初次按名称请求 perf2bolt 的命令在任何编译开始前以 unknown target 退出，现场保留在
`E/incremental/build/`。后续 dry-run 在 chroot 内完成，避免根内绝对路径在宿主
只触发 CMake 再生成而没有检查到实际目标图的问题。

dry-run 为 126 项。除 BOLT 依赖外，还包含生成的 TF runtime 锚点对象及归档两个
依赖边。其来源为 `B/../mlgo_verify_assets/mlgo_sysroot/xla_aot_runtime_src/CMakeLists.txt:6`：
configure 写入 45 字节的 `int __tf_xla_runtime_anchor(void){return 0;}`；`:12` 起
POST_BUILD 复制同一预编译 PIC 归档并执行 compare_files。构建前已经确认现有归档
与预编译输入哈希相同，归档备份与前后核对写入 `E/incremental-final/tf-runtime-proof.json`。
没有为此改源码、spec 或优化参数。

各阶段使用 `tools/run_bolt_stage.py`：18 GiB 聚合 cgroup、SwapMax=0、nice 15、
ionice idle、2 秒进程 VmHWM 和 30 秒 free/load/RSS 采样、MemAvailable <2 GiB
中止、退出回收。构建前仍检查可用内存 ≥16 GiB、磁盘 ≥60 GiB。
Ninja/compile/link 并发保持 4/4/1。实验命令不套用完整基线的项目列表门禁，
而是在重新配置后单独验证授权差异；完整 GBS 构建的默认门禁保持。

增量构建启动前原始输出（`E/incremental-final/build/commands.log`）：

```text
nproc: 20
               total        used        free      shared  buff/cache   available
Mem:              30           9           1           0          21          21
Swap:              3           2           1
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       1.8T  1.1T  682G  61% /home
```

free -g 是整数展示；脚本以 `/proc/meminfo` 和磁盘实际字节数执行阈值检查。

### 3.1 构建实测与产物

| 阶段 | scope wall 秒 | scope MemoryPeak | 结果 |
| --- | ---: | ---: | --- |
| 重新 configure | 26.426 | 627,392,512 B | PASS |
| 126 项增量构建 | 545.525 | 4,907,880,448 B（4.570820 GiB） | PASS |

增量构建的 lld 采样 VmHWM 为 3,598,268 KiB；外层 `/usr/bin/time -v` 为
wall 9:05.51、maximum RSS 4,465,844 KiB、exit 0。两者统计对象不同，不合并。
依据：`E/incremental/configure/` 与 `E/incremental-final/build/` 中的
`outcome.json`、`memory-summary.json`、`scope-after-rpm.json`、`time-v.txt`。
采样器、日志线程均回收。
`scope-after-rpm.json` 的文件名沿用公共采样器，本轮对应实验阶段，并未运行 RPM 打包。

工具路径均为 **B/bin/**，未安装到宿主，属于实验构建产物，不是新 RPM：

| 工具 | 字节数（跟随符号链接） | SHA256 |
| --- | ---: | --- |
| llvm-bolt | 648,678,768 | `1da7bb735f7bc1afab9a863154260699b0b0f88c6fd05b99231dd21ef653fd5a` |
| perf2bolt → llvm-bolt | 648,678,768 | `1da7bb735f7bc1afab9a863154260699b0b0f88c6fd05b99231dd21ef653fd5a` |
| merge-fdata | 11,891,568 | `9a725e368f39cc9fbaaf32fe8698ea3e1d120fee7de565373e376e3fc759a6a7` |

三个 `--version` 均报告 LLVM 22.1.8；llvm-bolt/perf2bolt 另报告
`BOLT revision <unknown>`，不能把它写成工具自身提供了 Git revision。
完整版本、NEEDED、`ls -la` 与帮助输出：`E/run/inventory-driver.log`；路径与哈希：
`E/run/bolt-tools.json`。CMake 同时自动生成 llvm-boltdiff 别名，没有为它单独编译可执行文件。

### 3.2 基线证据保留

R1 的 build 目录已按授权重新配置，不能再把它的当前 cache 当成原始基线 cache。
改动前 cache、Ninja 图、生成配置头及关键 ELF 哈希在 `E/incremental/before/`；
原 RPM 和 TC 没有被覆盖。构建后的 `E/incremental-final/preservation-check.json`
及全部实验结束后的 `E/final-preservation.json` 均检查相同基线文件。

关键 ELF 的改前/改后哈希相同，摘录如下；clang++、llvm-ranlib 等别名也在 JSON 中逐项记录：

| 文件 | 字节数 | 改前 = 改后 SHA256 |
| --- | ---: | --- |
| B/bin/clang-22 | 1,793,477,048 | `d25e99607c9ea23bf2e50da5075c21f0145f6da24a39a4228d2fd8026ead70cf` |
| B/bin/ld.lld | 1,079,523,024 | `9895d67f7020ac1ca573ac7d40b1cda93ace9aa504c17cfed358211bd1554f47` |
| B/bin/llvm-ar | 121,868,264 | `3d8ed30f0cfb0ce3bf1dc096b7b3cb840291ff0e49f3aaa26975ad3a2a681d8f` |
| TC/bin/clang-22 | 139,929,464 | `3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c` |
| 原始 relocs ELF | 3,560,474,952 | `6bfc85a8cce9952c4bcbea1a4ea169fb6199c379c18527df7d349f375e52caaf` |

## 4. 剥离、插桩、profile 与重写

### 4.1 剥离结果

用 TC/bin/llvm-objcopy，经宿主 ELF loader 执行 `--strip-debug <原始 ELF> <独立输出>`，
没有覆盖原件。精简版绝对路径：

```text
/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-measurement-20260918/run/stripped/bin/clang-22
```

| 项目 | 原始 ELF | 剥离版 |
| --- | ---: | ---: |
| 文件字节数 | 3,560,474,952 | 226,730,672 |
| .text 字节数 | 95,419,023 | 95,419,023 |
| .rela.text 字节数 | 36,376,776 | 36,376,776 |
| .symtab 字节数 | 6,850,080 | 6,793,656 |

剥离版 SHA256：`eccfb075bc3b2a6ca2bda5a2a6e68f6a29ba48b5586cb603f4b46080f656013e`。
所有 SHF_ALLOC 节区的地址、类型、大小及 payload 哈希均保持一致，包含完整 `.text`。
`.symtab` 保留且非空；所有指向非调试节区的 RELA/REL 节区保留，目标与大小不变。
符号编号可能因删除调试符号而重排，所以没有错误地要求 `.symtab` 或 `.rela.text`
的原始字节哈希不变。

删除的重定位节区仅为 `.rela.debug_aranges`、`.rela.debug_info`、`.rela.debug_line`、
`.rela.debug_loc`、`.rela.debug_ranges`，对应的调试段一起删除；代码/数据重定位未删。
依据：`E/run/strip-audit/result.json`、`before-sections.txt`、`after-sections.txt`。
检查工具为 `tools/check_bolt_elf.py`，只读解析完整 ELF64，未修改 ELF。
objcopy 阶段 wall 4.167 秒、scope peak 2,921,844,736 B；剥离审计也单独受 18 GiB 限制。

### 4.2 插桩命令与实测 OOM

本轮使用源码 README 的插桩流程（`llvm/bolt/README.md:172` 起），不使用 perf。
最终有效命令的参数如下；实际绝对路径、loader/library-path、nice/ionice 和 scope
外层命令完整保存在两次尝试的 `launch.json`、`stage.json`、`commands.log`：

```text
llvm-bolt <input> -instrument --thread-count=4
  -runtime-instrumentation-lib=<B>/lib64/libbolt_rt_instr.a
  -instrumentation-file=<独立 profiles 目录>/clang
  -instrumentation-file-append-pid
  -instrumentation-binpath=<对应独立输出>/bin/clang-22
  -o <对应独立输出>/bin/clang-22
```

线程参数的实际定义为 `llvm/bolt/lib/Core/ParallelUtilities.cpp:27` 的
`thread-count`，4 个工作线程加主线程，采样观察为 5 个线程。曾有一次 `--threads=4`
拼写被 CLI 拒绝，未处理 ELF；该记录保存在 `E/run/instrument/`，不纳入容量试验。
修正后以下两次是真正进入插桩的运行。

指定 runtime archive 是为了使用本次构建的插桩 runtime；指定 instrumentation-binpath
用于明确被插桩 ELF 路径，避免显式 loader 启动时 `/proc/self/exe` 指向 loader。
PID 后缀用于防止多个编译进程覆盖 profile。相关选项定义见
`llvm/bolt/lib/Passes/Instrumentation.cpp:32`、`:38`、`:44` 和
`llvm/bolt/lib/RuntimeLibs/InstrumentationRuntimeLibrary.cpp:28`。

**核心实测：这是 llvm-bolt 进程自身的 VmHWM，不是 lld，也不是整个 scope 的 RSS。**
进程虽然由 ELF loader 启动、`/proc/PID/status` 的 Name 显示 ld-linux-x86-64，
但采样的完整 argv 明确执行 B/bin/llvm-bolt；汇总按该实际程序路径识别。

| 输入 | llvm-bolt PID | 自身采样 VmHWM | scope peak | 阶段 wall（秒） | 自身存活时间界限（秒） | 结果 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 226,730,672 B 剥离版 | 2413516 | 18,838,684 KiB = **17.965969 GiB** | **18 GiB** | 124.145 | 119.819–123.859 | OOM |
| 3,560,474,952 B 原始版 | 2413950 | 18,839,048 KiB = **17.966316 GiB** | **18 GiB** | 44.385 | 40.255–44.293 | OOM |

wall 是外层阶段从启动到退出的实测值，包含短暂启动/收尾。两次同组 `/usr/bin/time`
也被 OOM 后的 scope 清理终止，`tool-time-v.txt` 未写出有效自身耗时；不能把外层
time 的少量 RSS 误填成 llvm-bolt 的峰值。自身存活时间界限根据相邻 2 秒进程采样
的出现/消失区间计算，不能提供比该区间更精确的进程自身 wall。

两个峰值均受 cap 截断，不能据此推算无上限时的真实峰值，也不能把停止时间差解释
为剥离版的性能收益。剥离大幅减少了输入文件大小，但未让本次插桩装入 18 GiB。
依据：`E/oom-summary.json`，以及 `E/run/instrument-02/`、`instrument-original/`
内 `process-memory.jsonl`、`memory-summary.json`、`scope-after-rpm.json`。

原始 cgroup 证据：

```text
剥离版：
Result=oom-kill
MemoryPeak=19327352832
MemoryMax=19327352832
MemorySwapMax=0
memory.events: max 337097, oom 1, oom_kill 1

原始版：
Result=oom-kill
MemoryPeak=19327352832
MemoryMax=19327352832
MemorySwapMax=0
memory.events: max 41464, oom 1, oom_kill 1
```

两次 outer exit 均为 143，scope 明确记录 oom-kill；shell 的完成标记却为 0，不能
单凭该标记判断成功。实际执行器已因 outer exit 非零拒绝继续。随后还加强了共享
guard：只要 cgroup 累计 `oom_kill>0`，即使 shell 标记为 0 也必须失败，测试覆盖
“只有回收压力 max 增长”和“确有 OOM kill”的区别。

两次最低采样 MemAvailable 分别为 5.304 GiB、5.194 GiB，没有触发宿主 <2 GiB
紧急停止；失败是 cgroup OOM。`sampler_reaped=true`、`log_reader_reaped=true`，
最终 scope 保留 failed/oom-kill 状态，记录过的进程均已退出。原始和剥离版 ELF 都保留，
没有生成可用插桩输出。

BOLT 在失败前还记录了 split function、2804 个 relocation 分析失败、jump past end
替换 nop 等警告，完整文本在两份 `build.log`。没有可运行产物，不能将这些警告
判为无害，也不能将它们当成已证实的 codegen 差异；本轮确定的终止原因是 OOM。

### 4.3 下游步骤状态

| 步骤 | 本次结果 |
| --- | --- |
| 插桩 clang 跑 10 TU + A/B/C | **NOT RUN**，插桩二进制未生成 |
| profile 采集耗时、大小、插桩运行开销 | **UNKNOWN**，不能把 OOM 时间当训练耗时 |
| merge-fdata 合并 | **NOT RUN**；仅完成工具版本查询 |
| 基本配置优化重写 | **NOT RUN**，没有可用 profile |
| 优化重写的 llvm-bolt VmHWM / wall | **UNKNOWN**，不能复用上表的插桩数据 |
| -dyno-stats | **NOT RUN**，无优化重写输出 |

已准备的优化命令选项仍是 README:212 那组：
`-reorder-blocks=ext-tsp -reorder-functions=cdsort -split-functions -split-all-cold -split-eh -dyno-stats`。
它们只存在于执行脚本的后续分支，**本轮没有执行**。

## 5. BOLT 后对象一致性与受控基准

全部 **NOT RUN**：没有 BOLT 优化后的 clang，因而没有第二次 10 TU 验证、两轮校准、
正式轮或逐项比值。第 2 节的 10/10 PASS 只验证原始 relocs clang，不能冒充 BOLT
产物的 10/10 PASS。

后续脚本按 TC clang 22 同一资源目录、同一 `.ii`/flags、固定种子 73419 的 A/B/C
（scale 1/2/2）、同一链接夹具和原有测量协议准备；同轮基线/BOLT 按原基准台交错运行。
该设计目的是得到只改变二进制布局的单变量对照，与 docs/13 的 clang 18 不同资源目录
参考轮不同。**本轮没有取得这种受控对照结果**，也没有复用旧基线噪声底当作 BOLT 校准。

结果目录：`W/temp/bench_results/bolt-20260918-instrumented/status.json`，状态为
`INSTRUMENTATION_OOM_NOT_BENCHMARKED`，包含两次 OOM 数据；profile、优化重写、
校准、基准与最终对象验证字段均为 null。这个文件是失败状态记录，不是基准数据。

## 6. 容量结论、原始输出与自检

### 6.1 结论边界

**NO：已测试的本机插桩流程，在 18 GiB cap、4 个工作线程配置下无法完成。**
两次实际运行的 cgroup OOM 已提供容量失败证据，不能再以“3.56 GB 主要是调试信息，
剥离后就应该够用”作为放行依据。没有提高 cap、关闭限制或改用更少覆盖面的插桩。

未测项目仍 UNKNOWN：无 cap 时需要多少内存、其他线程数是否能完成、外部提供 profile
后的纯优化重写是否能在 18 GiB 内完成。不能从两次 cap 截断的峰值给出更大内存机器的
精确最低配置。本轮也没有性能收益结论。PGO 完整构建维持此前 NO 决策。

### 6.2 脚本与原始输出

| 交付脚本 | 职责及本次验证程度 |
| --- | --- |
| tools/verify_compiler_outputs.py | 两边显式 g++ driver 模式、完整对象 cmp；本次 10 TU 实测 PASS |
| tools/build_bolt_incremental.py | 归档配置/哈希、授权重新 configure、审查 dry-run、增量构建及哈希复核；实测 PASS |
| tools/run_bolt_stage.py | 复用资源限制与采样器；支持命令自身 time-v 和独立 VmHWM 汇总；成功及 OOM 路径实测 |
| tools/check_bolt_elf.py | 剥离前后可加载节区、代码/数据重定位及符号表审计；实测 PASS |
| tools/collect_bolt_profile.py | 校验基线输入与 flags、采集 13 项负载及合并；仅语法/help 检查，因 OOM 未执行训练 |
| tools/measure_bolt.py | 按阶段执行并检查前置结果，保留失败/回退日志；inventory/strip/instrument 分支实测，后续未执行 |
| tools/build_llvm_x86_64.py | 保留完整构建门禁；为显式实验命令提供采样复用；新增 OOM 计数检查 |
| tools/test_bolt_preparation.py | 重链参数保真、driver 模式、cmp 停止逻辑、默认门禁不能关闭、OOM 计数测试 |

主要执行入口示例（每个目录必须是新的，完整参数以原始日志为准）：

```bash
python3 tools/build_bolt_incremental.py --help
python3 tools/measure_bolt.py --help
python3 tools/verify_compiler_outputs.py --help
python3 tools/test_build_llvm_x86_64.py
python3 tools/test_bolt_preparation.py
```

实际分阶段调用保存在 `E/run_phase.py`、`E/run/*-driver.log`；两次有效插桩命令
分别在 `E/run/instrument-02/stage.json` 和 `instrument-original/stage.json`。
本轮没有解除失败门禁继续到 collect/optimize/measure。

原始输出索引：

| E 下路径 | 内容 |
| --- | --- |
| relink-equality/、relink-equality-summary.json | 10 TU 完整调用、对象 SHA、cmp 原始输出 |
| incremental/before/、after-configure/、cache-changes.json | CMakeCache、Ninja 图、配置头与改前改后差异 |
| incremental/configure/ | configure 限流、采样、time 和退出状态 |
| incremental-targets/ | 首次完整 dry-run 与生成 TF 依赖边的审查记录 |
| incremental-final/ | 最终 dry-run、126 项增量构建、工具身份、TF 归档及基线哈希复核 |
| run/inventory-driver.log、bolt-tools.json | 三工具路径、体积、哈希、版本、NEEDED、帮助 |
| run/strip/、strip-check/、strip-audit/ | objcopy 命令、限流、剥离前后完整节区与哈希审计 |
| run/instrument-02/、instrument-original/ | 两次 BOLT 插桩完整命令、警告、2 秒 VmHWM、30 秒资源、OOM 现场 |
| oom-summary.json | BOLT 自身峰值、进程存活时间界限与 cgroup 计数汇总 |
| final-preservation.json | 实验结束后基线 ELF/spec/config 哈希、scope 失败状态与无残留进程核对 |
| build-guard-tests-final.log、preparation-tests-final.log | 9 项 + 5 项回归测试原始输出 |
| publication.log、publication-verification.json | 提交推送后写入的远端提交与 raw 内容核对 |

### 6.3 自检

1. **前置全部 10 TU 是否逐字节通过？是。** 两边均为 clang-22 + `--driver-mode=g++`，保留完整节区比较。
2. **是否先归档再 configure，记录 cache 与关键 ELF 哈希？是。** R1 变为实验目录，原 RPM、TC、原始 relocs ELF 保留；哈希核对通过。
3. **是否补齐三个工具？是。** LLVM 22.1.8；perf2bolt 是 llvm-bolt 的构建后别名，不是独立编译目标。
4. **剥离是否保留 BOLT 所需重定位和符号表？是。** 非调试目标的 RELA/REL 与 `.symtab` 保留，所有可加载节区 payload 不变。
5. **llvm-bolt 自身峰值与耗时是否实测？是，限于插桩。** 上表给出自身 VmHWM、阶段 wall 和进程自身时间界限；优化重写尚未运行。
6. **OOM 后是否继续基准或伪造结果？否。** 仅按授权用原始 ELF 回退一次，仍 OOM 后停止；下游均 NOT RUN。
7. **资源限制与采样器回收是否保持？是。** 两次有效插桩 cap 均为 18 GiB，swap=0，OOM 计数为 1，采样和日志线程均回收。
8. **是否改 spec/LLVM 源码、做 PGO/完整 LLVM 重建/Chromium/Gerrit？否。** 本次执行了 TU 比较编译、实验 configure、目标增量构建、剥离及 BOLT 插桩尝试。
9. **是否修改宿主 sysctl/capability 或安装软件？否。** 本轮不用 perf，工具保留在 R1 和 temp/。
10. **是否提交原始大文件？否。** 全部大文件与日志保存在本文指明的 temp/ 路径。完成回复列全部 raw 链接和固定提交的报告链接。
