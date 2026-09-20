# BOLT 最后一次容量尝试与受控对照

日期：2026-09-18。**22 GiB cap、单线程插桩成功；纯优化重写也成功。**
插桩的 llvm-bolt 自身峰值为 **19.722076 GiB**，优化重写自身峰值为
**3.481499 GiB**；两者不能混用。BOLT 后 clang 已通过全部 10 个真实 ARM TU
的完整对象文件逐字节比较。

**本机 BOLT 容量最终结论：YES（本次输入与协议）。** 两轮完整校准噪声底
**1.595225% <3%**；正式轮 13 个编译项的 BOLT/交错基线等权几何平均比值
**0.846042**，即 wall 减少 **15.396%**。优化重写阶段的生产资源评估应使用
约 **3.5 GiB** 的自身实测峰值，不能用插桩的约 19.7 GiB 替代。详见第 8、9 节。

## 1. 范围、既有事实与路径

直接沿用 [docs/15](15_bolt_measurement.md) 的已确认事实，不重复构建或论证：
原始 relocs clang 与基线的 10 TU 逐字节门禁通过；三个 BOLT 工具已在 B/bin
增量构建完成；剥离版为 226,730,672 字节，`.text`、`.rela.text`、`.symtab`
保留，SHA256 为
`eccfb075bc3b2a6ca2bda5a2a6e68f6a29ba48b5586cb603f4b46080f656013e`。

前两次 4 线程插桩在 18 GiB cap 下 OOM，自身 VmHWM 为 17.965969 / 17.966316 GiB；
MemoryPeak 与 MemoryMax 均为 19,327,352,832 字节，宿主仍有 5.304 / 5.194 GiB
MemAvailable。这些是受 cap 截断的值，不是自然峰值。本次没有据此重新推算自然峰值。

本报告路径缩写如下，均为本机绝对路径；原始输出、大文件不提交：

```text
W  = /home/linhao/Toolchain/development/llvm-optimize
E  = W/temp/bolt-final-20260918
D  = W/temp/bench_results/bolt-final-20260918
D0 = W/temp/bench_results/baseline-20260917-rpm
Q  = W/temp/bolt-measurement-20260918/run
R1 = W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0
B  = R1/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build
TC = W/temp/toolchain-baseline/usr
S  = /home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0
资源目录 = TC/lib64/clang/22
独立运行库目录 = W/temp/toolchain-runtime-baseline/libxml2/usr/lib64
输入 = Q/stripped/bin/clang-22
插桩输出 = Q/instrumented/bin/clang-22
原始 profile = Q/profiles/clang.<PID>.fdata
合并 profile = E/profile-work/merged.fdata
优化输出 = E/optimized/bin/clang-22
```

## 2. 两项调整与完整构建门禁隔离

本次只对 BOLT 插桩和优化重写使用 **MemoryMax=22G、MemorySwapMax=0、
--thread-count=1**。22 GiB 来自本轮授权的主机预算，单线程用于降低并行处理开销。
这是一次调整组合的实测，不将前次截断峰值与本次自然峰值做线程扩展比例推算。

完整 LLVM 构建入口 `tools/build_llvm_x86_64.py` 及
`tools/llvm_baseline_capacity.json` **字节未改**。完整构建仍是 18 GiB、
Ninja/compile/link 为 4/4/1、debuginfo 为 -j4，同构放行，PGO 等异构配置拒绝。
`tools/run_bolt_stage.py` 的原有 18 GiB 路径也未改。本次 profile 编译工作负载
沿用该路径，单个编译进程继续受 4 GiB AS 限制。

独立入口 `tools/bolt_final_attempt.py:28` 定义本轮 BOLT 的 22 GiB，
`:37` 只替换原命令的线程参数，`:102` 用固定日志目录的排他创建防止重试。
它不接受任意命令、构建根或 cap 覆盖。`tools/finish_bolt_final.py:38` 是独立
优化重写路径，`:120` 固定构造 BOLT 命令。二者不赋值或覆盖完整构建的
`MAX_BUILD_MEMORY_GIB`。

负对照 `tools/test_bolt_final.py` 验证：

1. 调用两个 22 GiB BOLT 策略前后，完整同构构建仍返回 **18 GiB、4/4/1/-j4**。
2. 即使宿主可用内存 64 GiB，PGO、compile=8、debuginfo=40 仍被完整构建门禁拒绝。
3. BOLT 入口拒绝 `gbs build`、任意 cap、`--root`；旧 argv 仅线程值有一处差异。

实测新负对照 **3/3 PASS**，原构建门禁测试 **9/9 PASS**（含异常退出与采样器回收）。
测试只使用模拟子进程，没有启动 GBS。证据：`E/policy-tests-final.log`、
`E/build-guard-tests.log`、`E/protected-before.sha256`、`E/protected-after-instrument.log`。

两条 BOLT 路径均沿用 nice 15、ionice idle、聚合 cgroup、零 swap、每 30 秒
free/loadavg/进程树 RSS、每 2 秒进程 VmHWM、MemAvailable <2 GiB 紧急中止。
额外每 2 秒记录宿主 MemAvailable；退出时回收该观察线程以及原采样器、日志线程。
没有改变宿主 sysctl、capability 或安装软件。

## 3. 启动前资源

`E/instrument/meminfo-before.txt` 保存 `/proc/meminfo` 原文，
`meminfo-before-bytes.json` 将所有 kB 字段乘 1024 转为字节（无单位计数仍是计数）。

| 项目 | 字节 | GiB |
| --- | ---: | ---: |
| MemTotal | 33,072,918,528 | 30.801556 |
| MemFree | 12,175,343,616 | 11.339172 |
| MemAvailable | 27,097,939,968 | 25.236923 |
| 本轮 cap | 23,622,320,128 | 22 |
| available − cap | 3,475,619,840 | 3.236923 |

启动时 available 高于 24 GiB。本轮入口将低于 24 GiB 记为信息，不拒绝启动；
运行中的 <2 GiB 紧急保护保持不变。实际判定保存在 `startup-policy.json`。

`free -g` 原始输出（整数显示），完整输出见 `E/instrument/commands.log`：

```text
               total        used        free      shared  buff/cache   available
Mem:              30           5          11           0          14          25
Swap:              3           1           2
```

启动前 RSS 最高的进程摘录（KiB），完整前 20 项在 `major-memory-processes.txt`：

```text
    PID    PPID USER       RSS    VSZ COMMAND
1819125 1818171 linhao   1478076 3201320 xdg-desktop-por
   2423       1 root     994384 3286880 epp-client-daem
1835069 1834542 linhao   528324 1518759036 code
1834788 1834539 linhao   261104 1518400136 code
1834656 1834542 linhao   229984 1522703760 code
```

## 4. 唯一一次插桩

实际入口：`python3 tools/bolt_final_attempt.py --run`。读取并钉住上一轮
`Q/instrument-02/stage.json` 的 SHA256：
`615a52272eaa6515ad81c8e21c480872684261f4a698bed3d41749d281f28e2a`。
argv 逐项对照只改变 index 6：`--thread-count=4` → `--thread-count=1`。
原输出目录为空，因此本轮保留全部原路径；旧尝试的日志、输入均未覆盖。
证据：`E/instrument/command-diff.json`、`input.json`、`stage.json`。

以下命令中的 W/B/Q 按第 1 节展开；完整绝对路径 argv 在 `stage.json`：

```bash
/lib64/ld-linux-x86-64.so.2 \
  --library-path "$W/temp/toolchain-runtime-baseline/libxml2/usr/lib64" \
  "$B/bin/llvm-bolt" "$Q/stripped/bin/clang-22" \
  -instrument --thread-count=1 \
  -runtime-instrumentation-lib="$B/lib64/libbolt_rt_instr.a" \
  -instrumentation-file="$Q/profiles/clang" \
  -instrumentation-file-append-pid \
  -instrumentation-binpath="$Q/instrumented/bin/clang-22" \
  -o "$Q/instrumented/bin/clang-22"
```

外层为 `/usr/bin/time -v` → `systemd-run --user --scope -p MemoryMax=22G
-p MemorySwapMax=0` → `nice -n 15 ionice -c3` → 阶段脚本；内部再用
`/usr/bin/time -v` 记录 BOLT 命令自身。原始封装命令见 `launch.json` 和 `commands.log`。
只有一次实际插桩，没有重试、换输入或新参数组合。

## 5. 插桩与优化重写的内存画像

以下是 **llvm-bolt 自身**，不是 clang 训练进程或历史 lld。进程经 loader 启动，
采样依据完整 argv 识别 B/bin/llvm-bolt，不能只看 `/proc` 的 Name。

| 项目 | 插桩 | 优化重写 |
| --- | ---: | ---: |
| BOLT PID | 3661335 | 3662653 |
| 自身 VmHWM，KiB | 20,680,096 | 3,650,616 |
| 自身 VmHWM，GiB | 19.722076 | 3.481499 |
| 自身 time -v maximum RSS，KiB | 20,680,096 | 3,650,616 |
| 自身 time -v wall，秒 | 66.00 | 21.83 |
| 2 秒采样推得的自身存活界限，秒 | 62.418–66.454 | 18.105–22.138 |
| 阶段 wall，秒（含启动/收尾） | 66.718639 | 22.271900 |
| cgroup MemoryPeak，字节 | 21,006,602,240 | 3,668,492,288 |
| cgroup MemoryPeak，GiB | 19.563923 | 3.416550 |
| cgroup MemoryMax，字节 | 23,622,320,128 | 23,622,320,128 |
| 最低采样宿主 MemAvailable，字节 | 7,161,487,360 | 24,259,383,296 |
| 最低采样宿主 MemAvailable，GiB | 6.669655 | 22.593311 |
| MemorySwapMax | 0 | 0 |
| 结果 | exit 0 | exit 0 |

自身 RSS 与 cgroup MemoryPeak 是不同统计口径，分别保留，不相加。
最低宿主 available 是每 2 秒采样观察值；存活界限来自相邻采样中 PID 的出现/消失，
不将离散采样伪装成更精确的连续测量。两次自身 time -v 都正常写出，maximum RSS
恰与采样 VmHWM 一致；两次均观察到 1 个线程。

两阶段 `memory.events` 原文相同：

```text
low 0
high 0
max 0
oom 0
oom_kill 0
oom_group_kill 0
```

**本次两阶段均不是 cap 截断值。** 两次 exit 0、max/oom/oom_kill 全为 0，
MemoryPeak 小于 MemoryMax；插桩 scope 仍距 cap 2.436077 GiB。
没有触发宿主 <2 GiB 保护。采样器、日志线程和额外宿主观察线程均已回收。

证据：`E/stage-summary.json`；`E/instrument/` 和 `E/optimize/` 内的
`process-memory.jsonl`、`host-memory-2s.jsonl`、`samples.jsonl`、`tool-time-v.txt`、
`outcome.json`、`scope-after-rpm.json`、`scope-after-rpm.log`、`final-summary.json`。
`scope-after-rpm` 是公共采样器沿用的文件名，本任务未运行 RPM 构建。
同样，日志中的 `BUILD COMMAND` 是公共执行器的历史标签；实际 argv 见
`launch.json`，本轮执行的是 BOLT 或训练脚本，没有调用 `gbs build`。

## 6. 训练 profile 与优化重写

训练使用与 D0/formal-baseline.json 完全相同的 13 组输入及 flags：历史生成器
A/B/C，seed 73419、scale 1/2/2，加 10 个真实 ARM TU。目标为
`armv7l-tizen-linux-gnueabi`；S、TC clang 22 资源目录、CPU 2、ASLR off 保持一致。
每组先跑基线，再跑插桩版本一次，验证输出为 ARM ELF 对象后删除临时产物。
两边均通过同一个 loader/library-path，以 `clang++` 名义调用。

13/13 组生成非空 PID profile。原始 profile 合计 **1,373,677,101 字节**；
`merge-fdata -o E/profile-work/merged.fdata <13 个 profile>` 合并成功，耗时
**2.751942 秒**，自身 maximum RSS 372,124 KiB。合并文件 **153,887,224 字节**，
SHA256：`d8b6c9146822fbe19ce0c3646d57d17e797d865100a7b0193562db6ea371c24d`。

采集流程总 wall **366.800154 秒**，含成对基线编译及合并；其中基线编译合计
**72.818840 秒**，插桩编译合计 **290.013137 秒**，比值 **3.982666**。
这是一次训练的插桩开销，不是优化收益或重复测量后的性能结论。

| 负载 | 基线秒 | 插桩秒 | 插桩/基线 |
| --- | ---: | ---: | ---: |
| A | 9.221660 | 32.775390 | 3.5542 |
| B | 2.218518 | 12.635126 | 5.6953 |
| C | 5.911112 | 27.507570 | 4.6535 |
| real_llvm_arm_ARMISelLowering | 8.261556 | 32.153594 | 3.8920 |
| real_llvm_arm_ARMTargetTransformInfo | 4.683543 | 19.215296 | 4.1027 |
| real_llvm_codegen_MachinePipeliner | 6.101803 | 23.289207 | 3.8168 |
| real_llvm_codegen_SelectionDAG | 6.762477 | 25.990604 | 3.8434 |
| real_llvm_mc_AsmParser | 2.636557 | 11.945699 | 4.5308 |
| real_llvm_mc_MasmParser | 3.296659 | 13.957690 | 4.2339 |
| real_llvm_sema_SemaExprCXX | 5.999005 | 23.573910 | 3.9296 |
| real_llvm_sema_SemaStmt | 5.756103 | 22.553400 | 3.9182 |
| real_llvm_transforms_Attributor | 6.242867 | 23.063442 | 3.6944 |
| real_llvm_transforms_WholeProgramDevirt | 5.726978 | 21.352210 | 3.7284 |

完整输入哈希、flags、命令、每次 wall/user/sys/RSS 和每个 profile 的大小/哈希，见
`E/profile-work/result.json`、`raw/commands.json`。`inputs_equal_baseline=true`，
训练临时目录已删除。

优化重写使用**原剥离版**加合并 profile，不以插桩 ELF 作为优化输入：

```bash
/lib64/ld-linux-x86-64.so.2 \
  --library-path "$W/temp/toolchain-runtime-baseline/libxml2/usr/lib64" \
  "$B/bin/llvm-bolt" "$Q/stripped/bin/clang-22" \
  -o "$E/optimized/bin/clang-22" -data="$E/profile-work/merged.fdata" \
  -reorder-blocks=ext-tsp -reorder-functions=cdsort \
  -split-functions -split-all-cold -split-eh -dyno-stats --thread-count=1
```

配置直接采用 `llvm/bolt/README.md:212` 的基本组：重排基本块、按 profile 排列函数，
分离冷代码和 EH，输出 dyno-stats。线程数与本轮决定一致；没有加入其他优化旋钮。
优化输出 SHA256：
`d6538b5ee1fdc429008b4481b651f994e354eabd55853666a0a9f0da03692e63`。

原始 `-dyno-stats` 完整保存在 `E/optimize/build.log`。关键输出：

```text
21802 out of 144032 functions in the binary (15.1%) have non-empty execution profile
378 functions with profile could not be optimized
profile for 1 objects was ignored
basic block reordering modified layout of 17447 functions (80.02% of profiled, 12.08% of total)
splitting separates 10703126 hot bytes from 12304877 cold bytes
456997977916 : executed instructions (-1.5%)
62626280077 : total branches (-6.6%)
11664984251 : taken branches (-65.7%)
```

这些是 BOLT 按 profile 计算的动态统计，不是硬件计数器实测，也不能直接换算成 wall
收益。日志仍有 split function、2804 个 relocation 分析失败及 jump past end 警告；
没有隐藏它们。后续一致性门禁检验本轮 10 TU，不据此声称覆盖全部编译器功能。

## 7. 完整对象文件一致性

两边共同使用 `clang-22 --driver-mode=g++`，原 sidecar flags、`-frecord-gcc-switches`
保留。每对编译使用同一 cwd、输出路径、资源目录和 sysroot，之后执行完整文件
`cmp -- baseline.o candidate.o`，不跳过 `.GCC.command.line` 或任何节区。
**10/10 PASS**；对象和原始命令保存在 `E/optimized-equality/`，
`result.json` 逐项记录字节数、两个 SHA256 和 `byte_equal=true`。

| TU | 每个对象字节数 | 完整 cmp |
| --- | ---: | --- |
| real_llvm_arm_ARMISelLowering | 6,957,056 | PASS |
| real_llvm_arm_ARMTargetTransformInfo | 3,220,172 | PASS |
| real_llvm_codegen_MachinePipeliner | 5,462,140 | PASS |
| real_llvm_codegen_SelectionDAG | 6,120,924 | PASS |
| real_llvm_mc_AsmParser | 2,628,704 | PASS |
| real_llvm_mc_MasmParser | 3,113,328 | PASS |
| real_llvm_sema_SemaExprCXX | 4,828,336 | PASS |
| real_llvm_sema_SemaStmt | 4,897,752 | PASS |
| real_llvm_transforms_Attributor | 6,661,176 | PASS |
| real_llvm_transforms_WholeProgramDevirt | 6,045,332 | PASS |

## 8. 受控校准与正式基准

两轮完整校准 **PASS**，全 30 个工具链/负载组合的最大绝对差值（噪声底）为 **1.595225%**，低于 3%。
两轮所有项的最大 CV 为 **1.178783%**，保留的可疑负载样本数为 0。
没有改协议、放宽阈值或挑选/删除保留样本。

| 负载 | 基线校准 1 秒 | 基线校准 2 秒 | 差值 % | BOLT 校准 1 秒 | BOLT 校准 2 秒 | 差值 % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 8.242563 | 8.351023 | +1.316 | 7.355681 | 7.351180 | -0.061 |
| B | 2.209753 | 2.204140 | -0.254 | 1.680706 | 1.678758 | -0.116 |
| C | 5.936957 | 5.904861 | -0.541 | 5.690035 | 5.699053 | +0.158 |
| real_llvm_arm_ARMISelLowering | 8.204240 | 8.234314 | +0.367 | 7.050285 | 7.055233 | +0.070 |
| real_llvm_arm_ARMTargetTransformInfo | 4.719137 | 4.725220 | +0.129 | 3.916223 | 3.891689 | -0.626 |
| real_llvm_codegen_MachinePipeliner | 6.113601 | 6.087033 | -0.435 | 5.189931 | 5.167130 | -0.439 |
| real_llvm_codegen_SelectionDAG | 6.743226 | 6.739454 | -0.056 | 5.759144 | 5.721771 | -0.649 |
| real_llvm_mc_AsmParser | 2.647500 | 2.622445 | -0.946 | 2.213614 | 2.224759 | +0.503 |
| real_llvm_mc_MasmParser | 3.286733 | 3.276800 | -0.302 | 2.804326 | 2.785632 | -0.667 |
| real_llvm_sema_SemaExprCXX | 5.985967 | 5.971879 | -0.235 | 4.942085 | 4.938547 | -0.072 |
| real_llvm_sema_SemaStmt | 5.756889 | 5.744456 | -0.216 | 4.781609 | 4.786183 | +0.096 |
| real_llvm_transforms_Attributor | 6.204785 | 6.184744 | -0.323 | 5.208712 | 5.226101 | +0.334 |
| real_llvm_transforms_WholeProgramDevirt | 5.700814 | 5.657719 | -0.756 | 4.791706 | 4.775080 | -0.347 |
| ld.lld | 0.004540 | 0.004553 | +0.297 | 0.004541 | 0.004532 | -0.198 |
| llvm-ar | 0.002328 | 0.002301 | -1.178 | 0.002335 | 0.002297 | -1.595 |

下表为正式轮 wall 中位数（秒/操作）；比值越低越快。D0 列来自 docs/13 的历史正式轮，
“本次基线”与 BOLT 在同一轮中交错测量；性能判断以该受控对照为主。

| 负载 | docs/13 基线秒 | 本次基线秒 | BOLT 秒 | BOLT/本次基线 | BOLT/docs13 | 基线 CV % | BOLT CV % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 8.399582 | 8.297694 | 7.332046 | 0.8836 | 0.8729 | 0.369 | 0.822 |
| B | 2.214020 | 2.201669 | 1.681161 | 0.7636 | 0.7593 | 0.714 | 0.108 |
| C | 5.921623 | 5.901407 | 5.679014 | 0.9623 | 0.9590 | 0.166 | 0.451 |
| real_llvm_arm_ARMISelLowering | 8.238827 | 8.191364 | 7.029427 | 0.8582 | 0.8532 | 0.299 | 0.264 |
| real_llvm_arm_ARMTargetTransformInfo | 4.726586 | 4.712997 | 3.891380 | 0.8257 | 0.8233 | 0.337 | 0.911 |
| real_llvm_codegen_MachinePipeliner | 6.132139 | 6.088252 | 5.151281 | 0.8461 | 0.8400 | 0.831 | 0.429 |
| real_llvm_codegen_SelectionDAG | 6.744573 | 6.723241 | 5.665625 | 0.8427 | 0.8400 | 0.676 | 0.772 |
| real_llvm_mc_AsmParser | 2.661888 | 2.628101 | 2.225143 | 0.8467 | 0.8359 | 0.282 | 0.503 |
| real_llvm_mc_MasmParser | 3.298552 | 3.285442 | 2.793099 | 0.8501 | 0.8468 | 0.932 | 0.926 |
| real_llvm_sema_SemaExprCXX | 6.013191 | 5.991850 | 4.921860 | 0.8214 | 0.8185 | 0.224 | 0.705 |
| real_llvm_sema_SemaStmt | 5.754308 | 5.756282 | 4.753100 | 0.8257 | 0.8260 | 0.598 | 0.689 |
| real_llvm_transforms_Attributor | 6.269321 | 6.180938 | 5.213783 | 0.8435 | 0.8316 | 0.316 | 0.596 |
| real_llvm_transforms_WholeProgramDevirt | 5.718177 | 5.685439 | 4.789024 | 0.8423 | 0.8375 | 0.359 | 0.482 |
| ld.lld | 0.004918 | 0.004538 | 0.004550 | 1.0024 | 0.9251 | 0.142 | 0.254 |
| llvm-ar | 0.002360 | 0.002330 | 0.002352 | 1.0097 | 0.9969 | 0.289 | 1.445 |

13 个编译项的 BOLT/本次基线比值范围 **0.7636–0.9623**；
等权几何平均比值 **0.846042**（wall 减少 **15.396%**），
13 项中位数之和的比值 **0.853182**（减少 **14.682%**）。
几何平均与求和采用不同权重，均只总结这 13 项，不代表全平台包构建加速比例。
正式轮全部命令最大 RSS 为 **1,188,748 KiB**，每个进程仍有 4 GiB AS 上限。

lld/ar 二进制未被 BOLT 修改，两个工具链入口指向同一基线文件；它们的比值是环境/测量对照，不是 BOLT 对链接或归档的优化收益。

**口径更正（2026-09-20）：**本次保持同一个 clang 22 资源目录、sysroot、13 个输入及 flags、同一夹具、同一协议，
但 RPM 基线到 BOLT 产物之间同时包含重链/剥离与 BOLT 重写，不能称作 BOLT 的单变量对照。
[docs/17](17_bolt_holdout.md) 增加 BOLT 实际输入的剥离版作为中间对照，并使用独立留出集测量净收益。
该轮校准未通过噪声门禁，尚不能将其诊断数据作为已验证的留出收益。
与 docs/13 的 clang 18 参考轮仍有区别：后者还使用了不同资源目录。
训练和评估使用同一批输入，收益不能直接外推到未见负载。本基准台是快速筛选层，最终 Chromium 全量时长仍需在专用构建服务器验收，本机未做。

协议：ARMv7 Tizen target；CPU 2、ASLR off；N=5 丢首次；scale 1/2/2、seed 73419；
66 个基线夹具对象，lld 每样本 4096 次、ar 1024 次，链接线程 1；loadavg 阈值 10。
协议 hash：`4f8b71e0547b3c7e72deac4141ce5dec4fee1f43af6a9b8f19b4fc91bd4637e5`。
夹具 hash：`30acab6c36503bcf53f5ad6467d17a58ede7f0205f95f68dedd1125494a9096a`。
两轮校准、正式轮与 D0 的协议、夹具和基线工具身份逐项一致，校验结果及比值在 D/controlled-comparison.json。

原始数据：D/calibration-run1.json、calibration-run2.json、calibration.json、formal.json；
各同名 .md 为人读表；*-raw/ 保存实际命令和 stdout/stderr。JSON 同时包含 wall/user/sys、最小值、标准差、RSS、前后负载与样本标记。

两轮完整校准分别耗时 904.646 秒、902.870 秒，正式轮耗时 902.031 秒；正式轮最大
CV 为 1.445361%，保留的可疑样本为 0，三个测量临时目录均已删除。证据为各轮 JSON。

历史对照需注意：lld 的 BOLT/docs13 比值 0.9251，不能解读为 BOLT 让 lld 加速约
7.5%。它的二进制没有变化，本次同轮 BOLT/基线比值为 1.0024；跨次差异的成因未在
本任务中调查。这也是同时提供本次交错基线和历史列的原因。

## 9. 容量结论与资源规划

**本机容量结论：YES，限定本次 ELF、profile、单线程和已验证的协议。**
22 GiB/零 swap 下唯一一次插桩成功，完整训练和优化重写成功，且 10 TU 逐字节门禁通过。
前次 18 GiB OOM 不能推广为本机无法运行任何 BOLT 流程。

可直接用于资源规划的两种流程：

| 流程 | 本次实测 BOLT 自身峰值 | 聚合 scope peak | 资源依据 |
| --- | ---: | ---: | --- |
| 本机插桩并采集 profile | 19.722076 GiB | 19.563923 GiB | 已验证 22 GiB cap、零 swap；启动 available 25.236923 GiB，最低采样仍有 6.669655 GiB |
| 已有 profile，纯优化重写 | 3.481499 GiB | 3.416550 GiB | 21.83 秒自身 wall、22.272 秒阶段 wall，远离本轮 22 GiB cap，无触限事件 |

完整插桩路线的宿主空闲资源可按本轮授权预算 **22 + 2 = 24 GiB** 做规划，
本次实测启动值高于该预算。纯优化重写对这个输入的实测需求约 **3.5 GiB**，
生产配置应再留宿主与输入规模增长余量；本轮没有降低 cap 寻找“最小可运行上限”，
不能把 3.5 GiB 宣称为保证成功的 cap，也不能推广到其他 LLVM 版本或更大的 profile。
纯优化重写的数据已直接测得，无需用 19.7 GiB 插桩峰值代替它。

本轮不需要 perf 权限就完成插桩 profile 路线；没有修改 perf 权限、sysctl 或 capability。
将来如采用 perf profile，应另做采样质量和性能对照。本报告不推测该对照的结果。
完整 LLVM 构建继续维持独立的 **18 GiB** 门禁；本机 PGO 完整构建仍按既定决策为 NO，
本任务没有尝试 PGO。

## 10. 复现入口、原始材料与自检

本次实际执行顺序如下。脚本拒绝覆盖现有阶段日志；首条是已完成的唯一一次尝试，
不能在原证据目录上重复执行。

```bash
python3 tools/bolt_final_attempt.py --run
python3 tools/finish_bolt_final.py collect
python3 tools/finish_bolt_final.py optimize
python3 tools/finish_bolt_final.py verify
python3 tools/finish_bolt_final.py calibrate
python3 tools/finish_bolt_final.py measure
```

原始材料索引（第 1 节已给出 W/E/D/Q 的完整绝对路径）：

| 路径 | 内容 |
| --- | --- |
| E/instrument/ | 启动 meminfo/free/ps、完整 argv/命令差异、time、2 秒/30 秒采样、cgroup counters、退出与回收 |
| E/profile-work/ | 13 组训练原始命令/输出、单次开销、profile 元数据、合并 fdata |
| Q/profiles/ | 13 个带 PID 的原始 fdata，大文件保留本机 |
| E/profile-collection/ | 训练阶段的资源采样与回收记录 |
| E/optimize/ | 独立优化重写命令、完整 dyno-stats、time/VmHWM/cgroup/宿主采样 |
| E/optimized-equality/ | 10 对对象文件、完整 cmp、两边 SHA256、命令与 stdout/stderr |
| D/ | 两轮校准、正式轮、各 JSON/Markdown 和原始输出；controlled-comparison.json 为比值与身份校验 |
| E/stage-summary.json | 两个 BOLT 阶段的统一内存/时间摘要 |
| E/final-preservation.json | 受保护文件 SHA256、源码/spec 状态、输出身份、各阶段 PID 已退出证据 |
| E/publication.log、publication-verification.json | Git 提交/推送、remote HEAD 与 raw 内容 SHA256 校验记录 |

本轮二进制均不提交，身份如下：

| 文件 | 字节数 | SHA256 |
| --- | ---: | --- |
| Q/instrumented/bin/clang-22 | 674,766,880 | `685b2f3706a427c674d633602cc6309c5d45aad2c31723ca6d0cdaaac74d2ea1` |
| E/optimized/bin/clang-22 | 215,899,856 | `d6538b5ee1fdc429008b4481b651f994e354eabd55853666a0a9f0da03692e63` |

提交前自检：

1. **是否只执行一次本轮插桩？是。** 只使用剥离输入，22 GiB、thread-count=1；
   与 docs/15 有效 argv 的唯一差异是线程参数。没有更高 cap、换输入或重试。
2. **完整构建的 18 GiB 门禁是否保持？是。** 原脚本与容量配置 SHA256 未变，
   3 个新负对照及 9 个原门禁测试通过，22 GiB 只存在于本轮 BOLT 入口。
3. **MemorySwapMax 是否仍为 0？是。是否仍为截断峰值？否。** 两阶段正常退出，
   max/oom/oom_kill 均为 0，scope peak 低于 cap。
4. **采样器是否回收？是。** 插桩、训练、重写阶段的采样器和日志线程均已回收；
   两个额外宿主观察线程已回收，记录过的阶段 PID 均已退出。
5. **全部 10 TU 是否完整逐字节一致？是。** 同一 driver 模式，未删除
   `-frecord-gcc-switches`，未跳过任何节区。
6. **校准是否通过？是。** 两轮完整测量最大差值 1.595225%，最大 CV 1.178783%，
   可疑保留样本为 0；之后才执行正式轮。
7. **是否改 spec/LLVM 源码或覆盖基线？否。** source HEAD 仍为
   `f111162e94aa48ed367c9d2c039456c70e7160ae`。spec SHA256 仍为
   `95887b2d060b38d5ef8f56936f7481a03d131f9d26432180a68e02ec95f0dda5`；
   Git 中已有的三处并发差异原样保留，本轮未增加变化。剥离输入、TC 基线、GBS 配置
   与完整构建门禁文件哈希均保持。证据为 E/final-preservation.json。
8. **是否做 PGO、完整 LLVM 重建、Chromium 构建或 Gerrit 推送？否。**
   没有改宿主 sysctl/capability、安装软件；本轮只新增本报告和三个 tools/ 脚本。
9. **大文件是否留在 temp/？是。** 仅指定提交 docs/16 和三个脚本，并在提交前
   检查每个文件 <10,000,000 字节。原始输入、ELF、profile、对象和 JSON/日志留本机。
10. **发布校验如何完成？** 提交推送到 GitHub main 后核对 remote HEAD，并逐一下载
    四个 main raw 文件及固定提交报告，验证 SHA256 与本地一致；完成回复列出全部
    raw 链接及钉到本次提交号的报告链接。原始记录保存在 E/publication*。
