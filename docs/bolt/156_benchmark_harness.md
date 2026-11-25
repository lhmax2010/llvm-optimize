# 156 · 编译速度基准工具与试跑

**试跑，非正式数据。** 同一核上完成 V0/V1 各 20 次编译，成功 20/20、20/20。逐字节比较 0 组相同、20 组不同、0 组未核对。151 的 G 链与试跑并行。

## 变体与私有运行环境

| 变体 | RPM | 私有 clang SHA256 | 版本 / 最小编译 | BOLT 节 |
|---|---|---|---|---|
| V0 | `clang-22.1.8-1.x86_64.rpm` | `fc12684ac40c4d44e791df22ff1510943e70d37828dffc08a42c3f3f1d187ff0` | 0 / 0 | 无 |
| V1 | `clang-22.1.8-2.1.x86_64.rpm` | `e08724d81231d8675c51d4908f4ff0e8d233ef3740c878da1c7eda42dd3532f5` | 0 / 0 | .bolt.org.rodata, .bolt.org.eh_frame, .bolt.org.gcc_except_table, .bolt.org.eh_frame_hdr, .bolt.org.text |
| V2 | 待仅 PGO 成品 | — | PENDING | — |
| V3 | 待 PGO+BOLT 成品 | — | PENDING | — |

- V0 RPM `/home/linhao/Toolchain/development/llvm-optimize/archive/task149-run/resume/N2/gbs-driver/local/repos/tizen_base_toolchain_standard/x86_64/RPMS/clang-22.1.8-1.x86_64.rpm`，SHA256 `c782f9c2aeccc6b78dc24015d8efc1383f659d44248fd479ba31b88131c3b5a7`。
- V0 私有 clang `/home/linhao/Toolchain/development/llvm-optimize/archive/task156/private/V0/usr/bin/clang-22`，139,929,464 B。
- V1 RPM `/home/linhao/Toolchain/development/llvm-optimize/temp/keep-baselines/qb-1232862-1232863/1232863/x86_64/rpms/clang-22.1.8-2.1.x86_64.rpm`，SHA256 `fab9fa0c7d317beaab81999f52002b94d7b216913e46e31bd209f1588de4cadd`。
- V1 私有 clang `/home/linhao/Toolchain/development/llvm-optimize/archive/task156/private/V1/usr/bin/clang-22`，152,532,400 B。

V0 使用留存的 149-run N2，无需回退到旧基线。它来自 PS5 并关闭 llvm_speedup。V1 采用同为 Toolchain 的 QB 1232863 x86_64。128 的回执登记的是 H4，其与 PS5 只差打包助手。QB 1232862 Base-Dev RPM 的身份也已核对。它不参与这轮。V1 的 PGO 关闭，混合链接和 BOLT 开启。

两个私有根由同一个冻结 Tizen 快照的 glibc、libstdc++、libgcc、zlib RPM 提供运行库。加载器 --list 的各个真实文件都在对应根内。方法 A 使用显式加载器、--library-path 和 -fintegrated-cc1。同时禁用 clang 默认配置文件，由每个 TU 的清单传入目标与标志。
[变体路径、哈希与烟测原文](../../tools/bolt/results/task156/variants.json) · [来源差异](../../tools/bolt/results/task156/variant-provenance.json)

## 留出语料

共 30 个 x86_64 TU。zlib 为 20 个 C，LLVM 为 10 个 C++。原始大小 87,542–19,739,071 B。小于 256 KiB 20 个，256 KiB 至小于 8 MiB 5 个，8 MiB 及以上 5 个。试跑取按字节大小分布选出的 10 个 C，另取全部 10 个 C++。

server-kit、133-N 和 138-D 指向的 23 项训练记录按任务名、目标、字节、SHA256 核对一致。同时排除之前训练集中的相同源文件身份和不同预处理目标。C 使用已归档的 zlib O2 输入与命令，C++ 使用旧 holdout 收据和恢复的预处理文件。保留适用的 Tizen 编译标志，统一 -O2，并清除已用于预处理的目录路径及旧输出参数。

工作区受限扫描列出 156 个候选路径。分类计数为 {"training source identity": 119, "duplicate source identity or other preprocessing target": 27, "selected input in corpus.json": 10}。同一 TU 的重复副本和其他架构预处理产物不增加独立样本数。无可验证包名、目标及编译参数的内容未纳入。因此可确认的语料未达到约 200 个、8 个包或完整语料 C/C++ 各半。

[语料清单及标志](../../tools/bolt/results/task156/corpus.json) · [训练排除身份](../../tools/bolt/results/task156/training-overlap-policy.json) · [候选归类](../../tools/bolt/results/task156/input-eligibility.json)

## 工具和试跑

正式默认 5 轮，轮换变体顺序。单线程按清单顺序编译，所有变体使用相同 taskset 掩码。-j N 提供最多四核的聚合模式。记录每 TU 墙钟、user + sys、峰值 RSS，并逐字节比较对象。8/8 单测通过，含轮换、并行、低内存等待、对象差异标红和统计。本轮一个核，受控子单元 CPUQuota=100%、MemoryMax=2 GiB、swap0、Nice19、IO idle，因低内存中断后重做的样本 0。MemAvailable 低于 6 GiB 时等待。若编译已启动，只停止本任务该子进程组并重新测量，保留中断日志。

按进程名记录构建进程，另记 CPU 调节器与 loadavg。共享名称无法区分项目，另一项目是否构建记 UNKNOWN。单轮 IQR 为 0 只是定义值，试跑倍率不用于正式结论。

| Variant | Valid rounds | Median total wall (s) | IQR (s) | Speedup vs V0 | Per-TU speedup Q1 / median / Q3 | Objects |
|---|---:|---:|---:|---:|---|---|
| V0 | 1 | 195.799 | 0.000 | 1.000× | 1.000× / 1.000× / 1.000× | 0 same / 0 different / 0 unverified |
| V1 | 1 | 281.435 | 0.000 | 0.696× | 1.253× / 2.194× / 4.475× | 🔴 0 same / 20 different / 0 unverified |

## Object differences and failures

- 🔴 Round 1 · V1 · zlib-compress · DIFFERENT.
- 🔴 Round 1 · V1 · llvm-ELF · DIFFERENT.
- 🔴 Round 1 · V1 · zlib-adler32 · DIFFERENT.
- 🔴 Round 1 · V1 · llvm-Metadata · DIFFERENT.
- 🔴 Round 1 · V1 · zlib-inffast · DIFFERENT.
- 🔴 Round 1 · V1 · llvm-Driver · DIFFERENT.
- 🔴 Round 1 · V1 · zlib-infback · DIFFERENT.
- 🔴 Round 1 · V1 · llvm-InstrProfReader · DIFFERENT.
- 🔴 Round 1 · V1 · zlib-gzclose · DIFFERENT.
- 🔴 Round 1 · V1 · llvm-ScalarEvolution · DIFFERENT.
- 🔴 Round 1 · V1 · zlib-inflate · DIFFERENT.
- 🔴 Round 1 · V1 · llvm-ParentMapContext · DIFFERENT.
- 🔴 Round 1 · V1 · zlib-gzwrite · DIFFERENT.
- 🔴 Round 1 · V1 · llvm-ParseDecl · DIFFERENT.
- 🔴 Round 1 · V1 · zlib-deflate · DIFFERENT.
- 🔴 Round 1 · V1 · llvm-CoverageMappingGen · DIFFERENT.
- 🔴 Round 1 · V1 · zlib-unzip · DIFFERENT.
- 🔴 Round 1 · V1 · llvm-AArch64InstructionSelector · DIFFERENT.
- 🔴 Round 1 · V1 · zlib-zip · DIFFERENT.
- 🔴 Round 1 · V1 · llvm-X86ISelDAGToDAG · DIFFERENT.

只读诊断确认 20/20 组的唯一差异是 .GCC.command.line 内记录的私有加载器路径。将该节里的 V0 路径替换为等长的 V1 路径后，全文件其余字节一致。保留原始 DIFFERENT 标记与对象，诊断没有写回 .o。
V1 首个样本墙钟 188.400 s，user + sys 0.08 s。单轮的整体倍率受该样本影响。
[逐文件只读归因](../../tools/bolt/results/task156/pilot-object-attribution.json)

[JSON 原始测量与对象哈希](../../tools/bolt/results/task156/pilot-results.json) · [试跑 Markdown](../../tools/bolt/results/task156/pilot-results.md) · [试跑配置](../../tools/bolt/results/task156/pilot-config.json) · [编译日志文本](../../tools/bolt/results/task156/pilot-compiler-logs.txt) · [单测原文](../../tools/bolt/results/task156/tests.txt) · [工具说明](../../tools/bolt/bench/README.md)
