# 12 编译器吞吐基准台

## 定位与基线

验证分两层。本基准台是本机的快速筛选层，用分钟级测量对 LLVM 变体排序；
最终验收是在专用构建服务器上测 Chromium 全量构建耗时，本机不进行该项验证。
后续必须把两层数据对照，检验筛选方向是否一致。通过噪声校准不等于已经证明
合成负载代表 Chromium，也不能将这里的比例直接解释为全平台 RPM 构建收益。

后续优化基线固定为工作区当前 spec（已有 `-O3`、ThinLTO、LLVM 库的静态链接配置等），
不回退到安装包配方。目标是其 x86_64 分支构建的原生 LLVM 工具，后续任务才运行
`gbs build -A x86_64`；本轮没有构建该基线。当前源码 HEAD 为
`f111162e94aa48ed367c9d2c039456c70e7160ae`。
本轮只用现成的 Chromium bundled clang 18 校准测量方法，不把它当成优化基线。

交付入口：[bench_toolchain.py](../tools/bench_toolchain.py)。仅依赖 Python 3 标准库、
Linux 的 `taskset`、`prlimit`、`setarch` 和 `stat`，不调用 GBS、RPM 构建、GN、Ninja 或 make。

## 输入、目标与工具身份

### 历史合成负载

生成器原文取自
`/home/linhao/Toolchain/plan_evaluation/analysis/bench_compiler.py:337–370`，
`generate()` 函数保持原样，固定种子 **73419**。来源哈希、函数哈希和历史输入清单见
[provenance.json](../tools/bench_inputs/provenance.json)，生成器见
[generate_synthetic.py](../tools/bench_inputs/generate_synthetic.py)。

| 类别 | 设计意图 | 历史 scale=1 | 当前默认 scale | 当前规模 |
| --- | --- | --- | --- | --- |
| A | 大量标准库头文件与重度模板实例化，偏前端 | 320 个实例 | 1 | 320 个实例 |
| B | 数百个独立中等复杂度函数，偏中端 | 400 个函数 | 2 | 800 个函数 |
| C | 单个超大函数，压优化管线对函数规模敏感的部分 | 3000 个条件块 | 2 | 6000 个条件块 |

三类均编译为 ARM ELF `.o`，采用 `-std=c++17 -O2`，不运行生成的程序。
“偏前端/中端”是设计意图，不是纯阶段计时：每次仍包含完整单文件编译过程。
`--scales 1 1 1` 会复现历史输入的三个 SHA256，已由自动检查确认。
当前 B/C 放大使用的是历史生成器原有 scale 能力；相同 scale 与种子才能比较历史
输入，**当前默认数据不能直接与历史 scale=1 的耗时相除**。此外本轮的原生启动方式、
亲和性、sysroot 路径和头文件版本也都进入协议记录，历史运行条件未必相同。

所有编译统一 `--target=armv7l-tizen-linux-gnueabi`；编译器本身是原生 x86_64，
生成 ARM 对象与通过 ARM/accel 运行编译器是不同的事情。脚本检查每个工具的 ELF
machine，拒绝非宿主架构的工具及 shell 包装器。

sysroot 必须通过 `--sysroot` 显式提供。本次使用上一轮报告 R：

```text
/home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0
```

同一次比较所有变体使用同一套 `--resource-dir` builtin headers，避免自动选择不同
头文件成为额外变量。sysroot 的 `usr/include`、`usr/lib/gcc` 及 resource headers
哈希在计时外记录。没有向工作区 LLVM 源码或 spec 写入任何内容。

### 真实翻译单元入口

本轮不填真实输入。[real_tu/README.md](../tools/bench_inputs/real_tu/README.md)
说明 `.ii` 与同名 `.flags.json`、固定 target、内容 SHA256、原始及预处理命令的格式。
扫描为空时 JSON/Markdown 明确标记 **REAL_TU_ABSENT**；缺少 sidecar、文件丢失、
target 不同、哈希不符或未允许的 flags 均会失败，不会静默跳过。
大于 10 MB 的 `.ii` 留在 `temp/`，通过 sidecar 的绝对 `input` 路径引用。
后续从 LLVM 自身编译采集输入后，必须重做校准；本轮没有采集或编译 Chromium TU。

### 链接与归档

先用列表中第一个工具链，在计时外把 B 的 800 个不同函数分成 64 个源文件编译，
每个函数仅出现一次；加上 A、C 的编译输出，共 **66 个 ARM 对象**。所有变体的
`ld.lld`、`llvm-ar` 都使用同一批对象，并记录逐文件 SHA256 与总清单哈希，
避免把不同编译器生成不同对象的影响混入链接器比较。

- 链接：`ld.lld -m armelf_linux_eabi -shared --threads=1 -o ... <66 objects>`。
  这是中等数量对象的 ELF shared-object 链接；不执行结果，不链接系统 C++ 运行库，
  允许外部符号未定义。未覆盖大型 executable、ThinLTO 链接或生产链接的完整特征。
- 归档：`llvm-ar rcsD ... <同一批对象>`，包含符号索引及确定性 archive 格式。
- 链接默认每个样本重复 4096 次，归档重复 1024 次，记录每次命令与输出；每次先删除前一产物，
  避免变成 archive 增量更新。按进程调用次数归一化 wall/user/sys；RSS 取峰值，
  **不除以重复次数**。批量只用于提高短任务测量稳定性，不是偷偷复制对象或符号。

## 资源上限与采样方法

- 默认亲和性是当前可用 `nproc` 的一半（向下取整，至少一核）；可用 `--cpus`
  选择更小的固定集合，超过半数则拒绝。所有工具经 `taskset -c` 启动，子进程继承
  affinity；采样器自身也固定在相同集合，整个基准串行运行，lld 固定 `--threads=1`。
  本次校准进一步固定到单核，具体核号见下表；没有修改宿主频率策略或其他进程。
- 默认 `--aslr off`，通过 `setarch <宿主架构> -R` 仅关闭本次工具子进程的地址随机化，
  固定另一个测量变量；不修改系统 sysctl。若环境不允许该 personality，启动即失败，
  可以显式 `--aslr on` 后重新校准，不能把两种状态的数据直接混用。
- 每个工具进程经 `prlimit --as=4294967296:4294967296`，虚拟地址空间硬上限为
  **4 GiB**。这也约束其线程与派生子进程；没有把 RSS 采样当作内存限制的替代。
  启动前和每次命令前检查 `MemAvailable`；能读取 cgroup v2 内存限额时同时取其
  剩余额度，低于 4 GiB 即拒绝。tmpfs/temp 另需至少 4 GiB 可用空间。
- 默认每个组合 **N=5**，第一次为预热且丢弃，其余四次计算中位数、最小值、
  样本标准差（`n-1`）、最大值和 CV。JSON 对 wall/user/sys/RSS 均保存这些统计，
  Markdown 提供 wall 分布、user/sys、峰值 RSS 和相对第一个工具链的时间比。
- 每次子进程前后记录三项 loadavg；1 分钟 loadavg 大于默认 `nproc/2` 时标记
  `suspect`。保留可疑样本，不择优删除；校准门禁不接受保留样本中的警告。
- wall 使用单调时钟和阻塞式 `wait4`，避免轮询间隔量化短任务；user/sys/max RSS
  使用该进程的 `wait4` rusage，Linux RSS
  单位为 KiB。编译器启动与进程退出包含在测量中，生成输入、制作公共对象、
  计算输入哈希不在样本中。完整基准耗时另外记录，包含准备工作。
  wall/RSS 包含 taskset、prlimit、setarch 和加载器启动的开销；特别是毫秒级链接/归档，
  不能把这一结果解释为链接器内部函数的纯处理时间。
- 多工具链在每类/每轮中交错测试，轮间逆转工具链顺序；不能同时跑两个基准进程。
  清除 CPATH、LD_PRELOAD 等可能改变输入/执行行为的继承变量，固定 `LC_ALL=C`。
- 默认临时产物位于 `/dev/shm/llvm-bench-*`，正常、异常和超时退出均清理；
  `--work-dir` 也可指定工作区 `temp/`。超时杀死当前工具进程组。原始 stdout/stderr、
  命令、资源数据与结果写到 `temp/bench_results/`，不会一起删除。

校准采用保守门禁：两次完整运行中，每一格 wall 中位数的绝对差都必须不超过 3%，
每格单轮 CV 也必须不超过 3%，且不得有保留的可疑负载样本。
噪声底定义为 `max(abs(median2 / median1 - 1)) × 100%`，不通过平均多格来掩盖
某个不稳定工具。两轮的协议、工具身份或公共对象哈希改变时直接拒绝比较。
退出码为 0（完成/校准通过）、1（执行或输入失败）、2（校准未合格；命令行参数格式
错误也由 argparse 返回 2）。
这是一项运行条件下的重复性门禁，不是对任意机器或长期 5% 差异的统计保证；
接近边界的候选应增加 N 并做交错复测，再由全量构建验收。

## 本机校准

### 降噪过程与全部完整尝试

| 尝试 | CPU | 链接/归档批次 | 跨轮最大差值 | 最大单轮 CV | 判定 |
| --- | --- | --- | --- | --- | --- |
| calibration-01 | 2 | 128 / 128 | 1.674% | 5.351%（归档） | 跨轮差值达标，但额外 CV 门禁未过 |
| calibration-02 | 2 | 1024 / 1024 | 1.565% | 3.409%（链接） | 跨轮差值达标，但额外 CV 门禁未过 |
| calibration-03 | 18 | 1024 / 1024 | 4.965% | 2.738%（A） | 跨轮差值未达标，不采用 |
| calibration-04 | 2；ASLR off | 4096 / 1024 | 0.220% | 0.902% | **PASS，最终协议** |

第一组保留全部原始数据和当时脚本快照。该版本以 1 ms 轮询等待子进程，短命令
容易受到计时量化影响；随后改成阻塞式 `wait4` 与 SIGALRM 超时保护，并把采样器
自身固定在工具使用的 CPU、把短任务批次从 128 增到 1024。第二组证明跨轮噪声
仍低于 3%，但单轮链接仍出现较大波动。两秒 `/proc/stat` 空闲采样后，第三组改用
CPU 18，保持输入、次数、批次和统计规则不变，重新进行两次完整校准，但跨轮差值
达到 4.965%，仍不合格。第四组回到 CPU 2，关闭基准子进程的 ASLR，将链接批次
延长到 4096，归档仍为 1024；其他输入和统计规则保持不变。
没有删除保留样本中的离群值，没有修改宿主 governor、关闭 turbo 或影响其他进程。
不同 CPU/计时版本/ASLR 状态之间的耗时变化不解释为工具链性能变化。

完整校准记录：

```text
/home/linhao/Toolchain/development/llvm-optimize/temp/bench_results/
  calibration-01.json / calibration-01-run{1,2}.json / calibration-01.console
  bench_toolchain.calibration-01.py
  calibration-02.json / calibration-02-run{1,2}.json / calibration-02.console
  calibration-03.json / calibration-03-run{1,2}.json / calibration-03.console
  bench_toolchain.calibration-02-03.py
  cpu-idle-survey.json
```

### 最终校准数据

**PASS：跨轮最大差值 0.220%，低于 3%；最大单轮 CV 0.902%。**

2026-09-16，CPU 2，nproc=20（默认最大允许 10 核，本次进一步收窄为 1 核），N=5，丢弃第一次；
ASLR 关闭，tmpfs，A/B/C scales=1/2/2，链接批次 4096、归档批次 1024。
这两轮由脚本连续、串行执行，全部保留样本的负载标记为正常。

宿主：`Intel(R) Core(TM) Ultra 7 265`；频率策略保持 `powersave / balance_performance`，
未改动 governor/turbo。两轮完整用时分别为 209.35 和 209.71 秒
（约 3.49、3.50 分钟，包含准备公共对象与保存日志）。

所有查询、准备及正式采样进程中的最高 RSS 为 **1,165,888 KiB（1.112 GiB）**，
小于 4 GiB 上限。两个工作目录都已删除；结果中的 `scratch_removed=true`。

| 项目 | 第一轮 wall 中位数（秒/次） | 第二轮 | 差值 | 第一轮 CV | 第二轮 CV |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | 10.100476 | 10.122722 | +0.220% | 0.504% | 0.290% |
| B | 2.581679 | 2.580747 | -0.036% | 0.386% | 0.110% |
| C | 5.607957 | 5.605654 | -0.041% | 0.257% | 0.090% |
| ld.lld | 0.004009 | 0.004012 | +0.078% | 0.198% | 0.173% |
| llvm-ar | 0.002275 | 0.002271 | -0.196% | 0.437% | 0.902% |

各轮详细统计（丢弃首轮后；链接/归档按单次调用归一化，RSS 列为保留样本的最大值）：

| 轮次 | 项目 | wall 最小值（秒） | wall 标准差（秒） | user 中位数（秒） | sys 中位数（秒） | 峰值 RSS（KiB） |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | A | 10.086458 | 0.051001 | 9.735398 | 0.353831 | 1165888 |
| 1 | B | 2.564638 | 0.009956 | 2.547575 | 0.029985 | 148752 |
| 1 | C | 5.593689 | 0.014404 | 5.551655 | 0.054488 | 198300 |
| 1 | ld.lld | 0.003995 | 0.000008 | 0.001215 | 0.002278 | 78284 |
| 1 | llvm-ar | 0.002266 | 0.000010 | 0.000649 | 0.001250 | 80524 |
| 2 | A | 10.066908 | 0.029351 | 9.737330 | 0.367375 | 1165888 |
| 2 | B | 2.576460 | 0.002837 | 2.546391 | 0.031481 | 505484 |
| 2 | C | 5.598116 | 0.005063 | 5.546480 | 0.054484 | 505484 |
| 2 | ld.lld | 0.004003 | 0.000007 | 0.001225 | 0.002266 | 505484 |
| 2 | llvm-ar | 0.002257 | 0.000021 | 0.000654 | 0.001245 | 505484 |

RSS 口径是 Linux `wait4` 返回的整个启动命令高水位，包含 fork/exec 前及包装进程的
记录；第二轮 B/C/链接/归档出现相同的 505484 KiB，不能解释为这些工具本体具有
相同内存需求。本轮没有单独采集 exec 后的工具稳态 RSS。资源上限由实际 prlimit
硬限制保证，不能只靠这列统计判断；全程最大值由 A 类编译产生。

工具身份（查询原文在 raw 日志）：

| 工具 | 版本摘录 | SHA256 |
| --- | --- | --- |
| clang++ | clang version 18.1.0rc; Target: x86_64-tizen-linux-gnu; Thread model: posix; InstalledDir: /home/linhao/Toolchain/plan_evaluation/chromium-efl/tizen_src/buildtools/llvm/bin | `2b6de207d210216f7a4251cfb244b8101d5d6d1f8542f0b690123b0c86141ee7` |
| ld.lld | LLD 18.1.0 (compatible with GNU linkers) | `2a9553f0bee743d90a33d2dd6aa6ff0e5f83dd221793076fc54b07cdc7d459a1` |
| llvm-ar | LLVM (http://llvm.org/):; LLVM version 18.1.0rc; Optimized build. | `c4099f6df3dbe30b98b4039de129f11c74578032a0ebd00a5b4fc7282f465fb4` |

66 个公共对象合计 535,980 字节。协议和对象清单在两轮完全相同：

```text
protocol_hash=2d6b568eb34b2def65ff0da8c0129446b79776dcb8d3d3c2d449e9ea6a27e768
fixture_hash=92ebc53a118692d51e2840c4c8034955eba05c1c1b69a3f9a38698cac736c3fb
```

最终证据位于以下工作区路径（JSON/Markdown/原始日志均不提交）：

```text
/home/linhao/Toolchain/development/llvm-optimize/temp/bench_results/calibration-04.json
/home/linhao/Toolchain/development/llvm-optimize/temp/bench_results/calibration-04.md
/home/linhao/Toolchain/development/llvm-optimize/temp/bench_results/calibration-04-run1.json
/home/linhao/Toolchain/development/llvm-optimize/temp/bench_results/calibration-04-run2.json
/home/linhao/Toolchain/development/llvm-optimize/temp/bench_results/calibration-04-run1-raw/commands.json
/home/linhao/Toolchain/development/llvm-optimize/temp/bench_results/calibration-04-run2-raw/commands.json
```

两份 commands.json 含大量重复 argv，均超过 10 MB，按规范只留在上述 temp 路径。
这次合格结论绑定上述协议；换 CPU、ASLR、批次、输入集、sysroot 或 resource headers 后必须重新校准。

### 验证与原始证据

`tools/test_bench_toolchain.py` 的 11 项检查通过，包含历史 A/B/C 哈希一致性、
丢弃预热及样本标准差、噪声/输入变化门禁、CPU 数上限、低内存拒绝、真实 TU 的
target/hash/危险 flags 拒绝，实际子进程 affinity/ASLR/prlimit 状态验证，
以及实际的超额内存分配、超时终止负对照。
原始输出为 `temp/bench_results/tests.txt`，最终复核输出为 `temp/bench_results/tests-final.txt`。

`multi-smoke` 使用同一 bundled 工具链的两个名称，实际走完多根目录交错测量、
链接、归档和对照表输出，验证入口；这是缩小输入的功能检查，不充当噪声合格证据。
`smoke.*`、`multi-smoke.*`、`help.txt`、`sizing.json`、`preprocess.stderr` 和
`direct-launch.json` 保存了功能试跑、初始规模评估及加载器/resource 路径诊断。
初始 sizing 留下的三个 `.o` 已删除；完整基准的工作目录均由脚本自动清理。
每次正式运行的 `*-raw/commands.json` 保存完整 argv、返回码、rusage、loadavg、
stdout/stderr 路径；具体 stdout/stderr 位于同一目录，所有原始证据都留在 temp。

## 用法

`python3 tools/bench_toolchain.py --help` 列出全部参数。

现成 bundled clang 的 ELF 解释器指向本机不存在的 `/emul/...` 路径，因此本次通过
宿主 `/lib64/ld-linux-x86-64.so.2` 直接加载原 x86_64 ELF；没有修改二进制、安装工具
或进入 chroot/accel。显式指定随 bundled 交付的 resource headers，避免加载器启动
使 clang 的自动 resource 路径落到宿主错误目录。这两个参数在结果中有记录。

```bash
python3 tools/bench_toolchain.py \
  --toolchain bundled=/home/linhao/Toolchain/plan_evaluation/chromium-efl/tizen_src/buildtools/llvm \
  --loader bundled=/lib64/ld-linux-x86-64.so.2 \
  --sysroot /home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0 \
  --resource-dir /home/linhao/Toolchain/plan_evaluation/chromium-efl/tizen_src/buildtools/llvm/lib64/clang/18 \
  --cpus 2 --calibrate \
  --output temp/bench_results/calibration-new
```

下一任务取得两个 x86_64 工具链后，可在相同输入、亲和性和校准条件下比较：

把保留的 baseline 放在第一个 `--toolchain`，与 candidate 在同一次运行中比较。
若分别单独运行 before 和 after，两次准备对象的编译器会变化；对象清单哈希不同的
链接/归档结果不能直接归因于链接器/归档器本身的变化。

```bash
python3 tools/bench_toolchain.py \
  --toolchain before=/实际路径/baseline/usr \
  --toolchain after=/实际路径/candidate/usr \
  --sysroot /实际路径/armv7l构建根 \
  --resource-dir /固定路径/clang/resource目录 \
  --cpus 2 --runs 5 \
  --output temp/bench_results/before-after
```

路径都是输入参数；上例两个待建工具链路径是占位符，不能当作已存在。
常规 ELF 解释器可直接执行时无需 `--loader`；如需指定加载器，每个 NAME 分别配置。
配套共享库需已能被该加载器找到，否则身份查询即失败，不回退到系统同名编译器。

## 提交前自检

1. 两次校准的差值与 3% 门禁：最大 **0.220%**，在 3% 以内；五项均通过，详细差值见上表。
2. 资源上限及实测峰值：半数 CPU 上限、串行工具、prlimit 4 GiB、启动/逐命令内存检查；实测最高 **1,165,888 KiB（1.112 GiB）**。
3. 是否构建 LLVM/Chromium，或执行 gbs build/rpmbuild：**否**，仅生成合成文件并编译、链接、归档；真实 TU 入口为空。
4. 是否向 Gerrit 推送：**否**，仅使用工作区 GitHub origin。
5. 完成回复是否列出所有产出的 raw 链接：交付时逐文件列出，包括配套 README、生成器来源清单和检查脚本。
