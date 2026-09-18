# 容量门禁重新标定与 BOLT 可行性实测

日期：2026-09-18。状态：**容量门禁修正完成；单目标重链成功；BOLT 实测被阻塞，未完成。**

同构基线现在允许在 18 GiB cap 下启动，异构配置仍拒绝。PGO 完整构建维持 **NO**，本次没有尝试。BOLT 的容量结论为 **有条件，实际内存需求 UNKNOWN**：本次只测到了带 relocations 的 clang 重链，尚未执行 `llvm-bolt`。不能把 lld 的内存数据当成 BOLT 的内存数据。

三个阻塞点分别是：22 个基线 RPM 和已检查的目录中没有 BOLT 工具；用户态 perf 采样权限不足；单 TU 的逐字节比较失败。最后一项已经定位到测试调用方式不一致造成的命令行记录差异，不能据此认定代码生成变化，但仍按任务红线停止，没有忽略该节区或将结果改记为 PASS。

## 1. 证据目录与既有事实

本文路径缩写均指本机绝对路径，`temp/` 不上传 GitHub：

```text
W  = /home/linhao/Toolchain/development/llvm-optimize
E  = W/temp/bolt-feasibility-20260918
L  = W/temp/baseline-build-20260917
J  = W/temp/baseline-resume-20260917
R1 = W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0
TC = W/temp/toolchain-baseline/usr
D  = W/temp/bench_results/baseline-20260917-rpm
S  = /home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0
```

直接沿用已确认事实：首轮 7634 个编译/链接任务在 18 GiB cap 内完成；失败发生在之后的 debuginfo `-j40`；改为 `-j4` 后完成 22 个 RPM。基线噪声底为 0.755%，正式数据及 clang 18 独立参考轮位于 D。本次没有重做这些历史测量。历史证据见 [固定提交的 docs/13](https://github.com/lhmax2010/llvm-optimize/blob/647e0d5dc0d85b35571871500b8e5fc9f80df881/docs/13_baseline_build.md)、`L/build.log`、`J/run/outcome.json` 和 `J/rpm-inventory.json`。

## 2. 容量门禁的新判据

旧模型把不同时刻的峰值相加，用于拒绝同一套已经完成编译/链接的配置，结论与实测矛盾。本次删除该加法预算及链接峰值占可用内存 60% 的旧准入条件。cgroup 上限用于限制整组进程的内存；准入表示有同构成功记录，**不承诺构建永不失败**。

`tools/build_llvm_x86_64.py:49` 起实现实际配置指纹，`:84` 的 `resource_plan()` 作精确比较。判据为：

```text
资源门槛通过
AND 实际配置指纹 == 已测基线配置指纹
AND systemd 聚合内存限制可用
=> MEASURED_BASELINE：MemoryMax=18G，MemorySwapMax=0
   GBS --threads=1，Ninja/compile/link=4/4/1，debuginfo -j4

任一配置指纹不同 => 拒绝；不能借用基线记录为 PGO 插桩等变体背书
```

资源门槛仍为 MemAvailable ≥16 GiB、磁盘剩余 ≥60 GiB；保留 nice 15、ionice idle、30 秒资源采样、2 秒进程内存采样、MemAvailable <2 GiB 中止和退出回收。实测准入要求 systemd cgroup：不能用每进程 `prlimit --as` 代替相同的聚合 18 GiB 条件。依据：`tools/build_llvm_x86_64.py:75`、`:509` 和本次 `E/relink/launch.json`。

配置清单提交于 [llvm_baseline_capacity.json](../tools/llvm_baseline_capacity.json)。它绑定实际输入，不接受仅声明“这是 baseline”的标签：

| 项目 | 固定值或检查方式 |
| --- | --- |
| LLVM 源码 HEAD | `f111162e94aa48ed367c9d2c039456c70e7160ae` |
| spec | 仅屏蔽三处并发数后计算 SHA256；其余配方逐字匹配 |
| 并发 | 三处数字另外解析，精确检查 4/4/1；GBS 1、debuginfo 4 |
| gbs 配置 SHA256 | `a3fea7732532db26c11b88407464e0274a6d8b4277623364fe16b6980181b03f` |
| build.conf SHA256 | `1e7610b6a922d27b80eb59c1c78bdf716f7de2e8e24700e0ee7c62522739ed52` |
| Base repomd SHA256 | `68b93454b4800a462e228260b11926a63ad8bba0589cc3f1a7dc4f0525bc2a74` |
| Unified repomd SHA256 | `e7af3f222f0ce958678d964589f2d156e8b47ba463ac0b3b0b96c74663382200` |
| 配置阶段 | 原关键门禁 + 基线 85 项 CMake 配置检查，15 分钟期限保持 |

85 项包含实际 CMake 显式参数、各类 C/C++/ASM 和链接 flags、PGO/coverage/sanitizer 等；完整值及来源随 JSON 提交。`LLVM_BUILD_INSTRUMENTED=OFF`、`LLVM_PROFDATA_FILE=`、`CLANG_BOLT=OFF`。编译器名允许原构建及续跑实际出现过的 bare name、`/bin/`、`/usr/bin/` 表示；其他参数严格比较。没有把整个含路径、内部探测变量的 CMakeCache 文件作为字节指纹。依据：`tools/build_llvm_x86_64.py:116`、清单 `cmake_parameters` / `evidence`。

异构拒绝表示**没有覆盖该配置的实测证据**，不表示已经证明它一定 OOM。PGO 继续 NO 是本任务确定的执行边界。

### 2.1 正负对照与实际预检

| 检查 | 结果 | 证据 |
| --- | --- | --- |
| 同构配置，可用内存 16/18/23/30/64 GiB | 均放行，cap 始终 18 GiB | `tools/test_build_llvm_x86_64.py:27` |
| 更改源码、配方、仓库、build.conf、架构、并发、debug -j40、加入 PGO 字段 | 即使可用 64 GiB 仍拒绝 | 同文件 `:35`、`:47` |
| 85 个 CMake 项逐一改变；PGO IR/profile/插桩 flags；BOLT ON | 均拒绝 | 同文件 `:57` |
| 资源阈值、原门禁和 10 种无害进程退出/采样器回收场景 | 通过 | 同文件 `:21`、`:75` 起 |
| 重链命令保真；模拟对象一致通过；首个不一致停止后续 TU | 通过 | `tools/test_bolt_preparation.py:18`、`:63`、`:64` |

原始测试摘要：

```text
E/capacity-tests-final.log:
Ran 9 tests in 21.814s
OK

E/preparation-tests.log:
Ran 3 tests in 0.020s
OK
```

上述测试不启动 GBS 构建、不编译 LLVM。对象测试模拟编译器输出并调用真实 `cmp`，只证明停止逻辑，不证明实际编译器等价。

实际运行了完整预检，**不带 `--run`**：

```bash
tools/build_llvm_x86_64.sh \
  --buildroot temp/gbs-root-capacity-check-final-20260918 \
  --log-dir temp/bolt-feasibility-20260918/preflight-final
```

`E/preflight-final/resource-plan.json` 记录 nproc=20、MemAvailable=23.019 GiB、磁盘可用=687.261 GiB。两个 repo HTTP 200，元数据哈希与清单一致；宏解析及最后输出如下（完整输出 `E/preflight-final/commands.log`）：

```text
2026-09-18T11:23:41+08:00 1|clang
[exit=0]
2026-09-18T11:23:41+08:00 CAPACITY ADMISSION MEASURED_BASELINE; 18 GiB cap, 4/4/1, debuginfo -j4
2026-09-18T11:23:41+08:00 MEMORY MECHANISM systemd
2026-09-18T11:23:41+08:00 PREFLIGHT PASS; no spec edit and no build. Use --run to proceed.
```

## 3. BOLT 工具与 perf 前提

使用 [probe_bolt_prerequisites.py](../tools/probe_bolt_prerequisites.py) 读取 `J/rpm-inventory.json`，对全部 22 个 RPM 执行 `rpm -qpl`；同时检查 TC/bin、R1 内 LLVM build/bin 和宿主 PATH。

| 工具 | 22 个 RPM 的文件清单 | TC/bin、R1 build/bin、PATH |
| --- | --- | --- |
| llvm-bolt | 未包含 | 未找到 |
| perf2bolt | 未包含 | 未找到 |
| merge-fdata | 未包含 | 未找到 |

依据：`E/prerequisites/result.json`（`rpm_count=22`、全部 `bolt_tools=[]`、`path_tools=null`），以及该目录全部 `rpm-files-*.log`。这不是对整台机器所有目录作不存在性证明；没有得到另一个可用工具目录。

`llvm/packaging/llvm.spec:260` 当前为：

```text
-DLLVM_ENABLE_PROJECTS="clang;lldb;clang-tools-extra;lld;compiler-rt;openmp"
```

没有 `bolt`。若以后让本配方产出工具，需要在项目中加入 bolt，并核对 RPM `%files` 对新工具、别名和 runtime 的归属。源码证据：`llvm/bolt/README.md:55`，`llvm/bolt/tools/driver/CMakeLists.txt:14` 定义 llvm-bolt、`:30` 定义 perf2bolt 别名，`llvm/bolt/tools/merge-fdata/CMakeLists.txt:3` 定义 merge-fdata；`llvm/bolt/cmake/modules/AddBOLT.cmake:15` 起为安装规则，`llvm/bolt/runtime/CMakeLists.txt:67` 起为 runtime。源码也提供 standalone 入口（`llvm/bolt/CMakeLists.txt:11` 起），但本次没有另行构建、下载或安装工具，没有改 spec。

perf 实测结果：

| 检查 | 原始结果 | 证据（E/prerequisites 下） |
| --- | --- | --- |
| 内核 | `6.17.0-1032-oem` | `kernel.log` |
| `/usr/bin/perf --version` | wrapper 缺少当前内核对应工具，exit 2 | `perf-wrapper-version.log` |
| 找到的独立 perf | `/usr/lib/linux-hwe-7.0-tools-7.0.0-31/perf`，`perf version 7.0.14` | `perf-actual-version.log` |
| perf_event_paranoid | `4` | `perf_event_paranoid.txt` |
| getcap | 无输出，exit 0 | `perf-capabilities.log` |
| 用户态 cycles:u，99 Hz | exit 255，无法打开事件 | `perf-user-cycles.log` |
| 用户态 cpu-clock:u，99 Hz | exit 255，无法打开事件 | `perf-user-cpu-clock.log` |
| sudo -n cycles:u | exit 1，`sudo: a password is required` | `perf-sudo-cycles.log` |

两个用户态事件均实际失败，不能只凭 paranoid 数字推断。原始错误摘录：

```text
Access to performance monitoring and observability operations is limited.
perf_event_paranoid setting is 4:
Failure to open any events for recording.
[exit=255]
```

独立 perf 还输出 `Missing support for build id in kernel mmap events.`；权限解除后仍需验证其与当前内核的配合，LBR 能力目前 UNKNOWN。99 Hz、0.2 秒 Python 忙循环仅用于低成本权限探测，**不是 clang profile 采集参数或训练结果**。本次没有修改 sysctl、授予 capability 或向宿主安装软件。继续采样需要可用的采样授权和通过实际探测的 perf。

## 4. 只重链 clang-22

执行 [relink_clang_for_bolt.py](../tools/relink_clang_for_bolt.py)。从 R1 的 Ninja 图用 `ninja -t commands -s bin/clang-22` 只取最终链接边，直接执行该命令。没有启动 Ninja 全图、CMake 配置或 RPM 构建。

保留原始 shell 转义（包括字面的 `$ORIGIN`）、全部输入对象/静态库/优化参数和 ThinLTO cache；只将 `-o` 与链接依赖文件指向独立目录，并追加 `-Wl,--emit-relocs`。`E/relink-command-validation.json` 验证还原这三项后 argv 与原始链接命令相同。完整命令保存在 `E/relink/original-link-command.txt`、`relocs-link-command.txt`，根内脚本为 `abuild-relink.sh`。

```bash
python3 tools/relink_clang_for_bolt.py \
  --root temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0 \
  --log-dir temp/bolt-feasibility-20260918/relink --run
```

脚本在 root 内以 abuild 用户、原构建目录执行。外层原始启动命令（`E/relink/time-v.txt`、`launch.json`）使用 `/usr/bin/time -v` 包裹：

```text
systemd-run --user --scope --unit=llvm-baseline-316e793fe71144eeabc8da0da49f2164.scope -p MemoryMax=18G -p MemorySwapMax=0 nice -n 15 ionice -c3 gbs chroot --root /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0
```

### 4.1 重链实测

| 指标 | 结果 | 原始证据 |
| --- | --- | --- |
| 链接退出码 / 外层退出码 | 0 / 0 | `E/relink/outcome.json` |
| wall | 227.655753 秒；time 显示 3:47.63 | 同上、`time-v.txt` |
| lld 自身采样 VmHWM | 10,235,012 KiB = **9.760868 GiB** | `process-memory.jsonl:113`，PID 2357535 |
| time -v maximum RSS | 10,239,884 KiB | `time-v.txt` |
| scope MemoryPeak | 11,222,044,672 B = **10.451344 GiB** | `scope-after-rpm.json`、`memory-summary.json` |
| MemoryMax | 19,327,352,832 B = 18 GiB | 同上 |
| memory.events max / oom / oom_kill | 0 / 0 / 0 | 同上 |
| 30 秒采样最低 MemAvailable | 23,617,146,880 B = 21.995 GiB | `memory-summary.json` |
| sampler / log reader 回收 | true / true | `outcome.json` |
| 记录过的残留 PID | `[]` | `memory-summary.json` |

这里的 VmHWM 是 2 秒采样观察到的单个 lld 高水位；time 和 cgroup 的统计口径分别保留，不混成一个值。文件名 `scope-after-rpm.json` 由复用的采样器生成，本次该文件对应**单目标重链**，没有执行 RPM 打包。

本次复用了 `build/lto.cache`，没有清缓存；命中率未采集。因此这不是冷缓存链接容量测量，也不能代替首轮 16.83 GiB 高水位或推导 BOLT 处理峰值。`cache-gate.json` 检查的是已有 CMakeCache：PASS，未重新配置。

新 ELF 绝对路径（超过 10 MB，仅留本机）：

```text
/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/bolt-relocs-6a5e8e81bccb/clang-22
```

大小 `3,560,474,952` 字节；SHA256 `6bfc85a8cce9952c4bcbea1a4ea169fb6199c379c18527df7d349f375e52caaf`。`readelf -SW` 包含 `.rela.text`、`.symtab`，版本为 clang 22.1.8。证据：`E/relink/output.json`、`elf-validation.log`。基线 build/bin/clang-22、RPM 解包 clang、build.ninja、CMakeCache 的前后哈希一致：`E/relink/preservation-check.json` 的 `equal=true`。基线工具链没有被覆盖。

### 4.2 单 TU 逐字节门禁：BLOCKER，测试调用不一致

使用 [verify_compiler_outputs.py](../tools/verify_compiler_outputs.py)，选 `real_llvm_sema_SemaStmt`。两次均使用 S、TC 的 clang 22 资源目录、同一个 `.ii`（SHA256 `6fb42a463b9cec5337665f495094cf29da94bad5fe63d966c165de62be393341`）、同一 sidecar flags、同一 cwd/输出 pathname、ARM triple、CPU 2、4 GiB AS 上限、ASLR off。证据：`E/relink-equality/result.json` 与 `raw/commands.json`。

**本次调用存在一个测试问题：基线传入 `TC/bin/clang++`，候选传入新 `clang-22`。** 两者都成功生成 ARM 对象，但 driver 名称不同；当前脚本没有自动规范化这个差异。该次运行因此不是严格单变量的等价性实验。

| 对象 | 字节数 | SHA256 |
| --- | --- | --- |
| baseline | 4,897,752 | `1267029569f99ed65e9014d2523969773eec017a4b54ab7651eca93383ec1030` |
| relocs candidate | 4,897,736 | `7ef94607b4933be00adf2755f1dd2a4eed1d043c0644ba87e955a0ea987017b4` |

实际执行 `cmp -- <baseline.o> <candidate.o>`，exit 1：

```text
...baseline.o ...candidate.o differ: char 33, line 1
```

完整原始输出在 `E/relink-equality/raw/00003-real_llvm_sema_SemaStmt-cmp.stdout`；门禁程序 exit 2、`result.json` 状态 **BLOCKER**。随后停止了编译/采样/重写/测量，仅做只读差异定位。

只读解析结果：两个文件各有 1408 个节区，唯一 payload 差异为 `.GCC.command.line`，721 对 703 字节，其余 1407 个节区 payload 相同。保留的 flags 包含 `-frecord-gcc-switches`，baseline 记录中多出 `--driver-mode=g++ `；从记录字符串中去掉这一项后，两个记录完全相同。对象本身没有被修改。这也解释了节区后续偏移/ELF header 的字节差异，不能把第一次差异在 header 当成机器码差异。

依据：`E/inspect_object_sections.py`、`E/section-inspection.log`、`E/relink-equality/section-differences.json`，以及 `baseline-recorded-command-payload.txt`、`candidate-recorded-command-payload.txt`。这证明了**本次对象差异的范围**，不替代用户要求的完整文件 `cmp` PASS。

后续复核需要统一两边 driver 调用模式/名称，保留原有 `-frecord-gcc-switches` 和其他 flags，重新做逐字节比较。本次按“不等价就停下报告”的红线没有再次编译，没有移除命令记录节区，也没有把等价性结果改成 PASS。

## 5. Profile、BOLT 重写、受控对照的执行状态

| 要求 | 本次结果 |
| --- | --- |
| A/B/C + 10 个真实 ARM TU 训练 profile | **NOT RUN**；只有第 3 节的权限探测 |
| 实际训练事件、频率、采样开销 | UNKNOWN；未采集训练数据 |
| perf2bolt 转换及 profile 大小 | **NOT RUN / UNKNOWN** |
| llvm-bolt 自身 VmHWM | **UNKNOWN，进程未启动** |
| llvm-bolt wall / OOM 情况 | **UNKNOWN，未做容量试验** |
| BOLT 工具链两轮校准（≤3%） | **NOT RUN** |
| 正式基准逐项比值 | **NOT RUN**，没有可以报告的比值 |
| BOLT 对全部 10 个真实 TU 的逐字节验证 | **NOT RUN** |

本次没有“实际使用”的 BOLT 优化选项。待前提具备时可评审工作区版本的上游说明 `llvm/bolt/README.md:212` 所列基本配置：`-reorder-blocks=ext-tsp -reorder-functions=cdsort -split-functions -split-all-cold -split-eh -dyno-stats`；本次未执行该命令。该源码文档 `:141` 给出用户态 cycles + 分支采样示例，`:197` 给出 perf2bolt 转换命令；也未执行训练或转换。

未来 BOLT 对照必须共享 clang 22 资源目录、全部 `.ii`/flags、夹具及测量协议，只改变待测二进制布局，并先解决 driver 记录差异。这与 docs/13 使用不同资源目录的 clang 18 量级参考有本质不同。旧 D 的数据不能充当本轮 BOLT 校准或单变量对照数据。

状态文件为 `W/temp/bench_results/bolt-20260918/status.json`，明确标记 `BLOCKED_NOT_BENCHMARKED`，测量字段为 null；它**不是基准结果 JSON**。

## 6. 容量结论与继续条件

| 问题 | 结论 |
| --- | --- |
| 同构完整基线可否按实测启动 | **YES**，4/4/1、debug -j4、18 GiB cap，预检通过；本次没启动完整构建 |
| 本机是否尝试 PGO 完整构建 | **NO**，维持既定决策 |
| 本次带 relocs 的单目标重链能否在 cap 内完成 | **YES**，227.656 秒，scope peak 10.451 GiB，受已有 ThinLTO cache 条件限制 |
| 本机做 BOLT 的容量结论 | **有条件；llvm-bolt 内存是否能装入 18 GiB 仍 UNKNOWN**，尚无实测支持 YES 或内存不足 NO |

继续所缺条件依次为：统一 driver 调用并通过对象逐字节门禁；获得可用的 llvm-bolt/perf2bolt/merge-fdata；获得实际可用的用户态采样权限。满足后仍需执行 18 GiB 限制下的 BOLT 重写，才能回答核心容量问题；若届时 OOM，应保存为有效容量结论。本报告没有以 ELF 文件大小或 lld 的内存用量猜测 BOLT 峰值。

## 7. 使用入口与原始记录

脚本均有 `--help`。以下是本次执行入口；E/R1/TC/S 按第 1 节展开。`relink` 的 `--run` 只执行单个已存在链接边，完整构建脚本本次只跑了不带 `--run` 的预检。

```bash
python3 tools/probe_bolt_prerequisites.py \
  --inventory temp/baseline-resume-20260917/rpm-inventory.json \
  --toolchain temp/toolchain-baseline/usr \
  --build-root temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0 \
  --output temp/bolt-feasibility-20260918/prerequisites

python3 tools/test_build_llvm_x86_64.py
python3 tools/test_bolt_preparation.py

# 以下为已失败的原始比较调用，保留用于审计，不应作为通过的调用示例：
python3 tools/verify_compiler_outputs.py \
  --baseline "$TC/bin/clang++" \
  --candidate "$R1/home/abuild/bolt-relocs-6a5e8e81bccb/clang-22" \
  --loader /lib64/ld-linux-x86-64.so.2 \
  --sysroot "$S" --resource-dir "$TC/lib64/clang/22" \
  --case real_llvm_sema_SemaStmt --cpu 2 \
  --output temp/bolt-feasibility-20260918/relink-equality
```

原始输出索引：

| E 下路径 | 内容 |
| --- | --- |
| `source-evidence.log` | 源码/spec/BOLT 文档带行号摘录、配置哈希、既有 spec diff |
| `capacity-tests-final.log`、`preparation-tests.log` | 测试全文，模拟场景明确标记 SIMULATION |
| `preflight-final/commands.log`、`resource-plan.json`、`repositories.json` | 完整预检、实际配置与资源、仓库证据 |
| `prerequisites/result.json`、该目录 `*.log` | 22 个 RPM 完整清单命令与输出，perf 版本/权限探测 |
| `relink/launch.json`、`commands.log`、`build.log` | 最终命令、时间戳与重链输出 |
| `relink/original-link-command.txt`、`relocs-link-command.txt` | 完整原链接/重链命令 |
| `relink/cache-gate.json`、`CMakeCache.txt` | 既有配置门禁证据 |
| `relink/time-v.txt`、`process-memory.jsonl`、`samples.jsonl` | time 全文、2 秒 VmHWM、30 秒 free/load/RSS |
| `relink/scope-after-rpm.json`、`memory-summary.json`、`outcome.json` | cgroup 峰值/事件、清理与退出状态 |
| `relink/output.json`、`elf-validation.log`、`preservation-check.json` | ELF 大小/哈希/节区、输入未覆盖证明 |
| `relink-equality/result.json`、`raw/commands.json`、`raw/*` | 两次 ARM 编译和 cmp 的完整参数/原始输出 |
| `inspect_object_sections.py`、`section-inspection.log` | 停止后的只读节区诊断 |
| `final-static-checks.json`、`final-preservation.log` | 脚本语法/help、两份历史 cache 的 85 项匹配、配置/spec 哈希和 scope inactive 证明 |
| `publication.log`、`publication-verification.json` | 本报告发布后写入的 Git 推送、远端与 raw 内容核对记录 |

## 8. 提交前自检

1. **容量门禁是否仍用独立峰值相加拒绝同构基线？否。** 新判据、同构正例、异构负例及真实预检均在第 2 节。
2. **是否完成 llvm-bolt 自身内存实测？否。** 工具缺失、perf 权限不足，且逐字节门禁因调用差异未通过；不得把重链 9.76 GiB 填入 BOLT 峰值。
3. **是否忽略对象差异继续？否。** cmp exit 1 后停止；只读定位到命令行记录差异，没有删除节区、放宽比较或继续跑其余 TU。
4. **是否改 spec 优化参数、gbs 配置或 LLVM 源码？否。** 三处 4/4/1 是此前已批准的现状，本次没有新 spec 修改。四个基线输入文件哈希保持一致。
5. **是否完整重建 LLVM、做 PGO、构建 Chromium 或向 Gerrit 推送？否。** 只执行一次 clang-22 重链、一个既有真实 TU 的两次对象比较编译，以及无害权限/回归探测。
6. **是否保留限流并回收采样器？是。** 重链使用 18 GiB cap、SwapMax=0、nice/ionice、资源监测；outcome 两项回收为 true，记录 PID 无残留。
7. **是否虚构 BOLT 噪声底、加速比或全 10 TU 一致性？否。** 全部标为 NOT RUN/UNKNOWN，旧基线数据保留。
8. **是否提交大文件或原始日志？否。** 新 ELF、对象、perf 探测输出与状态 JSON 全在 temp/；本次交付为本文、docs/13 的旧门禁失效提示以及 tools/ 脚本/清单/测试。完成回复列全部 raw 链接与钉到提交号的报告链接。
