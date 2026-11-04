# 47：PGO 资源测量试验（2026-11-02）

本轮只准备测量试验，尚未运行插桩版 clang 的完整编译、训练或 PGO 完整打包。发布源码、spec、helper 和 Source 文件保持不变；试验副本只在原 CMake 参数上增加 PGO 参数。白天检查与最终演练结果见第 6 节，夜间入口见第 8 节；本轮不推送 Gerrit、sandbox，也不操作 QB。

## 1. 基线与范围

- 发布源码：`3ee2d84719e4bd358c0b2366161f70f2eb788313`，tree `43d60f7523439fa0ccf4a61f668dd60622554606`；原工作区干净。
- 完整构建参考：`temp/debuglink-20261028/full-20261030/`，43 号第 9.7 节。该次 BOLT 已测，不为补基线重复运行；本次阶段 D 的 BOLT 输入因 PGO 改变，属于新试验。
- 固定快照：`tizen-base-toolchain_20261013.024319`，只启用 standard/packages、standard/debug。
- 配置：`temp/bolt-v4-20261021-disk-footprint/gbs_llvm_qb1202084.conf`；build.conf SHA256：`e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945`。
- 试验根：`W/temp/pgo-resource-20261102/`，W=`/home/linhao/Toolchain/development/llvm-optimize`。
- 代码：`tools/bolt/pgo-resource-20261102/`；证据：`tools/bolt/results/pgo-resource-20261102/`。下文证据相对路径以此结果目录为根。

没有修改原源码，也没有对历史构建根执行 CMake/Ninja。本次只在新演练根配置；CMake 自身的微型编译器探测属于配置过程，没有启动 LLVM Ninja 目标编译。全部新目录保留，没有删除历史目录。

## 2. 阶段与目录

沿用 dca920a8 的物理根与 gbs-driver 布局：每个新根的 `gbs-driver/local/BUILD-ROOTS` 链接到同级 `gbs-root/local/BUILD-ROOTS`；导出文件同时放入 driver 的标准 sources 位置。没有把 driver 的 BUILD-ROOTS 误指向另一棵树。

| 阶段 | 夜间动作 | 输入与输出 | 停止判据 |
|---|---|---|---|
| A | 新根 `%prep`；原 RPM 环境下 CMake；`ninja -j6 clang_rt.profile-x86_64`，再 `ninja -j6 clang` | `full/stage-A/gbs-root/`；插桩 `build/bin/clang-22` | 命令失败、OOM、磁盘底线触发 |
| B | 逐个编译同一套 23 份训练输入，单并发 | A 的 clang，`full/stage-A/objects/` 和 `profiles/*.profraw` | 输入 SHA 不符、编译失败、没有 profraw |
| C | 现有同源码构建树的 llvm-profdata merge | A 的 profraw → `profiles/clang.profdata`；记录数量、字节、SHA、工具 SHA | merge 失败或输出为空 |
| D | 另一个新根，PGO spec 副本正常 GBS 完整构建，默认开启 BOLT | `full/stage-D/gbs-root/`；ThinLTO、正常安装、BOLT、后处理和 RPM | 原有任何门禁失败即停止，不绕过、不降级 |

A/B/C/D 分别是独立 systemd 服务；A、D 的根准备另有 prepare 服务，准备开销单列，不能算成 clang 编译。A 根保留至 D 结束，不为省空间提前删除插桩现场。阶段 D 的 profile 放进新 chroot 的 `/home/abuild/pgo-resource/clang.profdata`，不依赖外部 bind mount。

### 2.1 CMake 参数与环境

原文来自 `full-20261030/evidence/rpm-build.log` **L657**。保存原始整行 `preflight/configure-original.txt`，以及经过 shell 解码的 `cmake-base.json`；不是凭记忆拼参数。

完整可执行命令：`preflight/cmake-A.txt`、`preflight/cmake-D.txt`；逐参数比较：`preflight/cmake-differences.json`。

| 比较 | 唯一新增参数 | 其他 argv |
|---|---|---|
| A / full-20261030 | `-DLLVM_BUILD_INSTRUMENTED=IR` | 全部逐字相同，包括编译器、C/C++/ASM flags、ThinLTO、hybrid、MLGO、项目列表、链接池 |
| D / full-20261030 | `-DLLVM_PROFDATA_FILE=/home/abuild/pgo-resource/clang.profdata` | 全部逐字相同 |

相对发布 spec，副本只有这一行增加：

```diff
+    -DLLVM_PROFDATA_FILE=/home/abuild/pgo-resource/clang.profdata \
     ../llvm
```

`preflight/spec-PGO.diff` 是全文 diff；GBS 两次导出间另有自动 VCS 字段变化，见 `export-spec.diff`。副本位于 `source-D/` 的 detached HEAD，本地试验提交 `4ff8ceb44b04b48f6299b6ddf7c5b147ad788b54`，不用于发布、不推送。原 profile、helper、Source1005 的 SHA 都未变。

原 RPM PATH 为 `/usr/local/bin:/bin:/usr/bin:/usr/local/sbin`，CFLAGS/CXXFLAGS 从同一条配置日志逐字提取，LDFLAGS 为 `-Wl,-z,relro,--as-needed`，AR/RANLIB 为 llvm-ar/llvm-ranlib；完整记录 `rpm-environment.json`。新根与历史根 clang、clang++、lld、llvm-ar、llvm-ranlib、cmake、ninja 共 **7/7** 实体 SHA 相同，见 `compiler-tool-identities.json`。这样避免历史上 `/usr/bin` 与 `/bin` 的相对编译器解析差异。

**profile runtime 的引导条件：**固定快照安装的编译器缺少 `libclang_rt.profile-x86_64.a`。仅在新试验根的编译器 resource-dir 中补入 full-20261030 已构建的同版本 runtime，来源/大小身份见各次 `stage-A/evidence/bootstrap-runtime.json`。原构建根只读。夜间仍先构建 A 自己的 profile runtime 目标，再构建插桩 clang。不能把这个额外引导条件隐去，亦不为它改发布 BuildRequires 或 Source。

阶段 C 的 llvm-profdata 使用 full-20261030 的 `build/bin/llvm-profdata`，源码也是 3ee2d847；用该根的 loader 和运行库启动，只读使用，不另建 LLVM 工具目标。阶段 C 的结果记录完整路径与 SHA。

### 2.2 训练输入

依据 `temp/bolt-aarch64-v2-20260921/profile-v2-manifest.json`：ARM 13 份（3 个 synthetic A/B/C，加 10 个真实 `.ii`），AArch64 10 个真实 `.ii`。不是把 30 TU 验证资产当作训练集。

23 份输入全部存在且与原清单 SHA 一致。A/B/C 原临时路径已不在，使用原生成器、seed 73419、scale 1/2/2，在**本次** `inputs/` 重建；重建字节 SHA 与原训练清单一致。完整路径、目标、CPU/优化选项、sysroot、resource-dir、字节数和 SHA 见 `preflight/training.json`；原清单与生成器 SHA 见 `training-provenance.json`。

B 使用 A 的插桩 clang，保持训练清单的目标和参数，`LLVM_PROFILE_FILE=<case>-%m-%p.profraw` 避免不同用例覆盖。每份编译的 argv、stdout/stderr、退出码均保存；B 结束记录 profraw 文件数/总字节及逐文件 SHA。C 合并后记录 profdata 字节和 SHA。此处只制定并检查入口，白天没有执行训练。

### 2.3 PGO 对 BOLT 的影响

不改 BOLT OPTIONS、profile、111+2 白名单、5% 双门禁或其余门禁。PGO 可能改变地址、控制流和布局，旧 BOLT profile 的匹配统计可能变化；D 中失败就保留日志的 N/M/S/U/Q、R、S/N 和失败点，到此为止，后处理/打包标为 NOT RUN。不要求 PGO 产物复现无 PGO 的 clang SHA，也不把门禁失败解释成测量脚本必须绕过的问题。

## 3. 资源测量方法与限度

每个阶段服务独立读取自身 `memory.peak`，包含页缓存。上限为 MemTotal−8GiB，MemorySwapMax=0，CPUQuota=1200%，nice10，ionice best-effort/7；正常 Ninja 实际 `-j6`、链接池2。GBS 外层 threads30，宏仍为 jobs8、_smp_mflags -j8、_costomized_smp_mflags -j20。限制只存在试验脚本，没有写进发布代码。

- 每 2 秒递归枚举阶段 cgroup 及其子 cgroup 的全部 PID，读 `/proc/PID/status` 的 VmHWM/VmRSS、进程名、完整命令、starttime。PID 加 starttime 防止复用混淆。原始 `processes.jsonl`，每 PID 最大值 `process-maxima.json`。短于采样周期的进程可能漏掉，不能声称这是内核级的所有短命进程最大值。
- 每 5 秒 statvfs `/home`，记录设备号、可用字节与纳秒时间，输出 `filesystem.jsonl`。这是整块文件系统的可用空间，其他写入也会影响它；不是仅本试验的耗用。
- du 只在服务或日志阶段边界执行；逐次保存开始/结束时间、退出码、stderr，超时为 UNKNOWN，不补造。**只有边界观测最大值，真实瞬时磁盘峰值仍 UNKNOWN**。这是用户要求的低频 du 方法固有的限制，不能把边界值标成连续峰值。
- 阶段 D 按下表的日志锚点转段。独立服务给出 D 总峰值；D 子阶段则保持同一个打开的 `memory.peak` 文件描述符，边界读值后写 0 清零，得到各观察区间的内核峰值。该接口的重置仅作用于这个 FD，不破坏服务总峰值。采样器在服务退出前握手完成最终读取，避免 cgroup 消失。
- 日志锚点有最多约 1 秒观察延迟。跨阶段进程的 VmHWM 是该进程生存期高水位，不可清零；子阶段表明确标作该区间观察到的 lifetime HWM，不伪装成区间 RSS 峰值。
- `service-result.json` 记录命令开始/结束纳秒、memory.events 和上限；`resources-summary.json` 汇总数值、进程名/命令、时间；缺采样写 UNKNOWN。

| D 子阶段 | 起点锚点 | 下一个锚点为终点 |
|---|---|---|
| 普通编译 | `Executing(%build)` | `%install` |
| 普通安装 | `Executing(%install)` | `BOLT_DISK_REPORT` 的 begin |
| BOLT | disk-report begin | `BOLT_COMPARE_ROOT_PASS` |
| 缓存释放 | `BOLT_COMPARE_ROOT_PASS` | `BOLT_CACHE_RELEASE` |
| 归档转换安装 | `BOLT_CACHE_RELEASE` | find-debuginfo |
| 平台后处理 | `/usr/lib/rpm/find-debuginfo.sh` | `Processing files:` |
| 打包 | `Processing files:` | D 命令结束 |

边界采样正在扫描时，不保证磁盘树不变，扫描开始/结束时刻一并保留。profraw、profdata、训练对象在 A 根旁的目录，夜间分析要单列它们，不能拿 root du 充当整个试验目录用量。A/D 根并存的总占用也不能用两个不同时刻的峰值简单相加。

共享重任务锁在试验控制器中独占；低于 20GiB 的 `/home` 剩余空间时正常停止当前服务。OOM/命令失败不自动重跑；即使阶段失败，也尝试正常卸载本次新根挂载，记录残留，保留现场。

## 4. 磁盘预估

full-20261030 的历史**采样下界**为 68,252,237,824B（63.565GiB），不是完整连续高水位。预检采用：

```text
2 个根 × 历史采样峰值 × 1.5 预留系数 + 20GiB 剩余
= 226,231,549,952B（210.695GiB）
```

1.5 是本次规划余量，不是实测 PGO 增长率；A 的插桩/带调试 ThinLTO 和 B 的 profraw 尚无测量，不能保证不会超出。启动时重新检查预算，运行中保留20GiB停止条件，全部只是本地试验规则。

初始可用261,475,123,200B，预算通过（`preflight/disk-budget.json`）。最终演练结束后的实际可用空间和余量见第6节及 `disk-budget-final.json`。只统计 `/home`，不与 `/var/tmp` 相加。本轮多次演练根和导出副本占用已包含在最终可用空间中，没有为了过预算删除目录。

### 4.1 2026-11-04 用户批准的预算调整

保留上述11月2日原预检记录。今晚采用43号的68,252,237,824 B与54号夜间T的
70,485,561,344 B中较大者，即70,485,561,344 B（65.644794 GiB），规划系数从1.5改为1.2：

```text
修改前：2 × 68,252,237,824 × 1.5 + 20 GiB = 226,231,549,952 B（210.695 GiB）
修改后：2 × 70,485,561,344 × 1.2 + 20 GiB = 190,640,183,706 B（177.548 GiB，向上取整字节；启动分档约177.6 GiB）
无余量预算：2 × 70,485,561,344 + 20 GiB = 162,445,959,168 B（151.290 GiB，启动分档约151.3 GiB）
```

原因是使用最近实测的较大采样下界，并按用户批准降低本地实验余量；这不是PGO增长率的实测。
运行中低于20 GiB正常停止的规则未变，未改任何发布spec/helper/Source。
仅改common.py预算常量/公式和相应测试预期后，`test_experiment.py` **12/12 PASS**，
原文见 `tools/bolt/results/pgo-resource-full-20261104/tests.stderr`。
用户随后明确裁决：目标预算只记录，最低启动预算才作为PASS门槛；介于两者之间时，
预算JSON和controller.stdout首行都写BUDGET_MARGIN_WARNING（可用、目标、差额）。
低于最低预算仍拒绝，其他流程不变。原12项加高于目标/介于两者/低于最低3个边界夹具，
**15/15 PASS**，见tests-approved.stderr。入口内部已演练的免密sudo -n获用户明确允许，
不新增提权方式、不弹窗，认证失败就按原入口停止，不重试。

本次启动可用183,273,168,896B（170.686GiB），
比目标少7,367,014,810B（6.861GiB），
但高于最低启动预算，按裁决PASS。唯一指定launch.sh full已于2026-11-04执行一次。
启动、清理和最终测量结果见58号文档。

## 5. 与 QB 的差别及可外推范围

本机 Intel Core Ultra 7 265、20 logical CPU；内核与完整 lscpu 原文在 `preflight/host.txt`。本地 GBS 与 QB NGBS 不同；QB 1202084 日志有 JOBS_N=12、WORKER_N=28，且曾三架构同 worker 并行。本试验串行 A→B→C→D、限12核配额，只做 x86_64 构建和交叉目标训练；不能把本地耗时、页缓存峰值或文件系统最低余量直接当作 QB 机器需求。

可直接复用的是固定快照/build.conf 身份、编译器版本与参数、输入 profile 的字节身份、最终文件实际大小和流程顺序。工具链相同不代表机器负载/压缩/缓存淘汰相同。特别是 A 只构建 clang 与 runtime，并非又完整生产一套22包；“两次完整构建”的磁盘预算是对两个同时保留根的保守规划，不代表 A 真会执行全量包目标。

## 6. 白天检查与演练

### 6.1 前置检查

| 检查 | 结果 | 原始证据 |
|---|---|---|
| 原源码 HEAD/tree/干净工作区 | PASS，发布代码未变 | preflight/source-final-audit.json |
| 既有测试 | **348/348 PASS** | preflight/existing-tests-retry.stdout.stderr，L352–354 |
| 试验附加检查 | **12/12 PASS** | preflight/experiment-tests-final2.stderr |
| gbs export 原版与副本 | 两次退出0 | preflight/export-baseline.stdout、export-PGO.stdout 及 result.json |
| spec 副本唯一增加 PGO 行 | PASS | preflight/spec-PGO.diff |
| Tizen RPM 五项 | **5/5 PASS**，x86开/关/单行回退、armv7l、aarch64 | preflight/five-parse/matrix.json 及各 case stdout/stderr |
| 训练输入 | **23/23 SHA PASS**，13 ARM +10 AArch64 | preflight/training.json |
| A/D 配置 argv | 除各自一个 PGO 参数外逐字相同 | preflight/cmake-differences.json、cmake-{base,A,D}.json |
| 编译器/工具身份 | 7/7 与 full-20261030 同 SHA | preflight/compiler-tool-identities.json |
| IR 配置与目标存在 | PASS，clang/profile runtime 两目标存在，仅文本检查 | rehearsal-03/stage-A/evidence/configure-proof.json、preflight/configured-targets.json |
| 语法 | Python 源码 compile()、POSIX sh -n PASS | launch.sh 及脚本身份见 preflight/ready.json |
| 阶段峰值重置 | PASS，先分配80MiB再释放，两个区间94609408B /10207232B | preflight/sampler-selftest.json、sampler-test/ |
| 最终服务/进程/挂载 | 无残留 | preflight/final-audit.json、all-pgo-units-final.json、all-pgo-processes-final.json |

RPM解析使用本次新根的 RPM 4.14.1.1（库包版本；`rpm --version` 显示4.14.1），采用 `rpmbuild -bp --nodeps --nobuild` 和 `rpmspec -P`；没有运行 `%build`。五份导出都具有8个补丁声明，具体 argv 和展开全文逐项保存。A 配置是实际运行结果；D 配置 argv 是从待运行 spec 展开得到的静态比较，白天没有配置/编译 D。

### 6.2 失败记录、修复及复演

1. 首次既有测试缺少宿主 PATH 中的 cmake，348项中的8项报 `FileNotFoundError: [Errno 2] No such file or directory: 'cmake'`；原文 `existing-tests.stdout.stderr` L367起，L496为 `FAILED (errors=8)`。沿用43号已记录的本机 CMake 目录，在测试服务环境中追加该目录，未安装软件、未修改测试判据；重跑348/348 PASS。实际参数在 `existing-tests-retry.stdout.argv.json`。
2. **rehearsal-01 的 CMake 成功，但测量收尾失败**：`OSError: [Errno 19] No such device`，读/关闭已消失 cgroup 的 memory.peak FD。早期控制器虽写 status=ok，本轮明确不接受它作为演练通过，原日志不改。试验采样器改为阶段命令完成后等待采样器读取结束，随后释放服务；线程异常传播到控制器，不再静默忽略。
3. 独立80MiB轻量自测证明同FD区间峰值重置有效。rehearsal-02 重新建立全新根，配置、采样与收尾通过。
4. 补齐日志尾部读取、保留A/B/C阶段标签和报告区间耗时之后，再用同一个 `launch.sh rehearsal` 入口启动 **rehearsal-03**，最终版本通过。所有尝试的根和失败原文保留，没有删除或复用失败根。

最终原文（`rehearsal-03/stage-A/evidence/A/stdout`）：

```text
-- Configuring done (35.7s)
-- Generating done (2.2s)
-- Build files have been written to: /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build
PGO_A_CONFIGURE_PASS
PGO_STAGE 已结束 2026-11-02T15:32:00.625092+08:00 status=ok
```

控制器末行：

```text
PGO_RESOURCE 已结束 2026-11-02T15:32:00.700476+08:00 status=ok reason=configure-only-no-ninja
```

新根的顶层 `.ninja_log` 不存在，未执行 LLVM 目标编译；`build.ninja` 的 clang/profile runtime 目标检查是读文本，没有调用 Ninja。完整构建目录 `full/` 尚不存在。

### 6.3 本次最终演练资源（不是 PGO 完整构建结果）

| 步骤 | 命令耗时秒 | cgroup memory.peak 字节（含缓存） | 最大采样 VmHWM 字节 /进程 | 边界 du 最大字节 | statvfs 最低可用字节 |
|---|---:|---:|---|---:|---:|
| stage-A/prepare | 84.148 | 6076051456 | 20492288 / rpm | 7022088192 | 235216105472 |
| stage-A/A | 38.301 | 560349184 | 318214144 / cmake | 7088418816 | 234431844352 |

每个最大值的 PID、完整命令与纳秒时间都在 `rehearsal-03/resources-summary.json` 和原始 jsonl；本表没有以主进程替代全阶段进程扫描。准备阶段主要页缓存计入cgroup；A行仅CMake配置，不可用于估算真正插桩编译的内存峰值。

独立收尾审计原文（`preflight/final-audit.json`，命令也在其中）：

```text
$ systemctl --user show pgo-controller-rehearsal-03-20261102.service pgo-rehearsal-03-stage-A-prepare-20261102.service pgo-rehearsal-03-stage-A-A-20261102.service -p Id -p ActiveState -p SubState -p MainPID
MainPID=0
Id=pgo-controller-rehearsal-03-20261102.service
ActiveState=inactive
SubState=dead

MainPID=0
Id=pgo-rehearsal-03-stage-A-prepare-20261102.service
ActiveState=inactive
SubState=dead

MainPID=0
Id=pgo-rehearsal-03-stage-A-A-20261102.service
ActiveState=inactive
SubState=dead
```

所有 pgo-*20261102 服务的 running/activating/deactivating 清单为空；扫描阶段 cgroup 的 `/proc` 成员为空；本次试验路径的 mountinfo 引用为空。没有结束其他进程，没有强制或懒卸载。原源码再次核对仍为3ee2d847且干净。

最终预算：可用 **234,376,544,256B（218.280GiB）**，要求 **226,231,549,952B（210.695GiB）**，超出预算约 7.586GiB，PASS。不是把规划余量认作真正 PGO 的实测剩余；今晚入口会再检查。


## 7. 证据与复核入口

- `preflight/`：原 configure 行、三套 argv、spec diff、原/source副本身份、export 原文、五项 parse、训练 SHA、测试原文、磁盘预算。
- `rehearsal-01/`、`rehearsal-02/`、`rehearsal-03/`：逐次原始日志、资源数据、结果和清理检查；第一次失败不隐藏。
- `sampler-test/`：80MiB 分配/释放的独立区间峰值自测；无需 LLVM 编译。
- 脚本角色：`prepare.py` 一次性建立副本，`parse.py` 五项解析，`driver.py` 服务/阶段串接，`monitor.py` 只读采样，`service.py` 执行与收尾握手，`train.py` 训练，`report.py` 汇总，`test_experiment.py` 本试验检查。

`prepare.py` 不可覆盖重跑；新入口 `launch.sh rehearsal` 总是选择新的 rehearsal-NN，`launch.sh full` 要求 ready.json 且 full/ 不存在，防止误覆盖。既有验证目录没有原地运行或写入。

## 8. 晚上启动（本轮未执行）

```sh
/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/pgo-resource-20261102/launch.sh full
```

入口建立 `temp/pgo-resource-20261102/full/`；前台最后一行单独打印：

```sh
tail -f /home/linhao/Toolchain/development/llvm-optimize/temp/pgo-resource-20261102/full/controller.stdout
```

控制器日志给出最终状态；命令的实时原文在 `full/stage-A/evidence/A/stdout`、`.../B/stdout`、`.../C/stdout`、`full/stage-D/evidence/D/stdout`，失败原文还有对应 stderr 和 `full/failure.txt`。最终行形如：

```text
PGO_RESOURCE 已结束 <ISO时间> status=ok|failed reason=<原因>
```

失败状态同样结束并保留现场，不能把没有结束行的文件误认为成功。所有阶段结束后汇总（纯读取原始记录并写新报告）：

```sh
python3 -B /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/pgo-resource-20261102/report.py /home/linhao/Toolchain/development/llvm-optimize/temp/pgo-resource-20261102/full
```

总结论：白天检查及最终配置演练全部通过，晚上可以启动；本轮未运行完整构建。


## 11. 2026-11-04 完整实验结束（58号）

按用户批准的目标/最低双预算启动一次：可用183,273,168,896B（170.686GiB），比目标少7,367,014,810B（6.861GiB），高于最低启动预算；budget JSON和controller首行均有BUDGET_MARGIN_WARNING。原12项及新增3项预算边界检查共15/15 PASS。

A/B/C完成，23份profraw共746,313,472B，合并profdata 52,528,216B。D普通编译/安装及BOLT工具构建完成，llvm-bolt在85.3%陈旧函数profile处按原5%门槛失败；没有打包成功、没有重试。结束行：`PGO_RESOURCE 已结束 2026-11-04T23:47:45.378355+08:00 status=failed reason=D: rc=1 reason=None; see /home/linhao/Toolchain/development/llvm-optimize/temp/pgo-resource-20261102/full/stage-D/evidence/D`。

各阶段独立memory.peak、进程VmHWM、边界磁盘和profile统计见[58号结果](58_pgo_resource_results.md)；原report.py已执行exit0。所有根与产物保留，未额外提权、未改发布代码或启动其他构建。
