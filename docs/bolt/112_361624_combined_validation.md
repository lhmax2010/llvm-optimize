# 112：361624 综合候选验证（步骤4准备STOP）

**最终结论：步骤4 STOP（第二次准备错误），步骤5 SKIPPED。** 用户批准仅步骤4以 MemAvailable≥12GiB 准入后，完成输入归档、只读获取PS1、独立工作树应用建议补丁及两文件范围核对；随后读取错误的源码相对路径失败。没有实施 A1–A4/F6，没有生成综合候选 I，没有运行展开、解析或 CMake 配置，不把准备STOP表述为产品失败。

## 本次执行与停止

- 用户准入调整原文：**“仅步骤 4 改为至少 12 GiB”**。其余条件保持不变。准入时 MemAvailable=14,773,309,440B，/home可用113,994,158,080B，指定重进程0；非阻塞取得已有共享 `/home/linhao/Toolchain/development/heavy-stage.lock`。
- 服务 `task112-step4-20261116`：MemoryMax=4GiB、swap0、CPU200%、Nice19、IO idle；30秒看门狗，低于6GiB停止自己的服务。原24GiB等待服务已结束，未并行启动另一分析服务。
- 三份下载材料复制至 `W/temp/review-361624-final/` 并重新核对SHA；原件保留。证据仓库 `tools/bolt/results/review-361624/` 已归档终稿、补丁和说明信；旧版报告由Git历史保留。残留 `external-review.md` 与 Claude 原报告逐字节相同，未删除。
- PS1只读 fetch `refs/changes/24/361624/1` 成功，revision=`da885208aeb52f55c448ff46873d242346727522`。显式fetch使用完整SSH URL和BatchMode。
- 新独立游离工作树：`W/temp/combined-112-20261116/C1`。`git am`成功，得到仅应用建议补丁的提交 `61d821ab2a090d4d36995fd55a1631724fc29dae`，tree=`6f66f01452df352ab4711e7c22fb68edaecca4ae`。只改 `packaging/llvm-tools-subpkgs.spec` 和 `packaging/llvm.spec`，工作树干净。**这不是已完成的C1或I**。
- H2从114号本地对象库核对：`b06ee2ac62085748b1b137523582c989ac78184e`，tree=`02a7036249700830fe90fe24c66e07e08f18edb7`，父=`61ef5d31ca91025c414c748477bef0c64ddfa67c`。

### 两次准备问题（保留原文，不重跑）

第一次：误用旧源码对象库查询H2，触发隐式promisor fetch。只中止本任务自身的查询/fetch进程，改用114号本地对象库，并显式设置后续Git的BatchMode；使用本步骤一次准备修正机会。隐式fetch未显式带BatchMode，这一偏差如实记录；未交互输入或创建凭据。

```text
warning: filtering not recognized by server, ignoring
fatal: early EOF
```

第二次：检查脚本假定源码根目录直接包含 `bolt/CMakeLists.txt`，读取失败。按第二次准备错误停止，未修正路径重跑。

```text
FileNotFoundError: [Errno 2] No such file or directory: '/home/linhao/Toolchain/development/llvm-optimize/temp/combined-112-20261116/C1/bolt/CMakeLists.txt'
```

### 结果边界、资源与证据

| 子项 | 结论 |
|---|---|
| 4.1 输入归档/SHA、残留文件相等 | PASS |
| 4.2 PS1获取、git am、仅两spec改动 | PASS |
| 4.3 A1–A4/F6 | NOT RUN，准备STOP |
| 4.4 综合候选I/冲突解决 | NOT RUN |
| 4.5 展开/解析/三变体配置 | NOT RUN |
| 5 综合候选构建 | SKIPPED，步骤2没有新T产物且步骤4未通过 |

停止时服务采样 memory.peak=952,078,336B（约908MiB），memory.events的max/oom/oom_kill均为0；这是停止时采样，交付完成时另保存最终快照。等待与执行看门狗均未触发。没有运行BOLT、完整构建或QB；没有任何LLVM远端写入。

没有(ii)配置错误、(iii)链接行、runtime flags比较、build-id核对或bolt包结果。未生成完整 `combined/C1.diff`；只保存 `step4-patch-only.diff`，明确它仅代表建议补丁，不冒充A1–A4的综合候选。

已读：完整任务、授权回复、STATUS/工作区规则、三个输入、114号身份说明、本地提交对象、fetch/am范围核对。尚未读完HQ源码与各CMake修改位置，未读取新构建产物（本轮没有生成）。

[本轮证据索引](../../tools/bolt/results/night-102-112-20261116/RAW_LINKS.md)；[STOP原文](../../tools/bolt/results/night-102-112-20261116/STOP-step4.txt)；[授权](../../tools/bolt/results/night-102-112-20261116/step4-threshold-authorization.json)；[输入复制核对](../../tools/bolt/results/night-102-112-20261116/step4-input-copy.json)；[资源采样](../../tools/bolt/results/night-102-112-20261116/step4-resource-snapshot.json)。

## 历史等待记录（以下为当时状态，已由上文最终结论取代）

# 112：361624综合候选验证（等待资源，尚未执行）

当前结论：步骤4 WAITING，尚未获得资源准入，不是PASS或产品FAIL。步骤5 SKIPPED：102步骤2未执行，没有本任务要求的新T产物。

准入线：无gbs/rpmbuild/ninja/llvm-bolt进程，MemAvailable至少24GiB，共享锁可立即取得。每30分钟复查，截止2026-11-18 08:30 Asia/Shanghai。先检查资源，达标后才取共享锁；目前未取锁。

输入只读预检：/home/toolchain/Downloads不存在，使用/home/linhao/Downloads。三个文件均存在且SHA与任务指定值一致：

| 文件 | 字节 | SHA256 |
|---|---:|---|
| autofdo-bolt-agent-review.md | 36285 | 5e3b4ff68725d4a06408dd95b1447f07406866e9fdd0ff3998ff443f9dcc6a63 |
| 361624-suggested-fix-v3.patch | 9696 | 81f41716aa2fe1761d1a3f228c83ab86e6559e0f09c7c5defeac762afec5116b |
| attachment.txt | 5223 | 4b883b315e1c2781167adac21436e1ebef7b8ac3c03baff83fb24d25515306f2 |

没有复制、移动或覆盖这三个文件；没有fetch、git am、C1/I提交、cherry-pick、spec展开或cmake配置，因此没有(ii)错误原文、(iii)链接行、冲突清单或build-id/bolt包结果。不能引用其他轮次的通过结果代替本轮。

102步骤1的准备STOP原文在102报告。步骤4独立于步骤1，继续等待，不把步骤1的错误计入步骤4准备修正额度。步骤4准备修正使用0次。

资源等待服务task112-admission-20261116：4GiB、swap0、CPU200%、Nice19、IO idle；附属看门狗30秒一次，MemAvailable低于6GiB停止自己的服务。不操作另一项目目录/进程/锁。当前只有等待和证据记录，不启动构建。

[输入身份](../../tools/bolt/results/night-102-112-20261116/step4-input-preflight-sha.json)、[资源观察快照](../../tools/bolt/results/night-102-112-20261116/admission-snapshot.jsonl)、[看门狗快照](../../tools/bolt/results/night-102-112-20261116/watchdog-snapshot.jsonl)。

最近一次观察：2026-11-16T13:14:50.628431-08:00，MemAvailable=17197260800 B，/home可用=114082066432 B，指定重进程=0。


### 等待进度 2026-11-16T19:36:34.922566-08:00

累计17次准入观察，均未满足24GiB内存线；最近MemAvailable=16273952768 B，/home可用=114081792000 B，指定重进程=0。看门狗未触发。三个输入SHA已匹配，但未复制、fetch、应用补丁或配置。询问是否仅将轻量步骤4的内存准入线改为12GiB，尚未收到批准；继续按24GiB等待至原截止时间，不把沉默当成批准。

[准入观察](../../tools/bolt/results/night-102-112-20261116/admission-20261116T193634.json)；[看门狗观察](../../tools/bolt/results/night-102-112-20261116/watchdog-20261116T193634.json)。

最终交付采样 2026-11-16T21:18:02.827097-08:00：memory.peak=952078336B，memory.events原文见[交付资源记录](../../tools/bolt/results/night-102-112-20261116/step4-delivery-resource-snapshot.json)，OOM和看门狗触发均为0。此采样在最后记录提交及服务退出之前，不冒称覆盖退出后的数值。


## 133-D 续做 N3

**PARTIAL。** 候选 I 为 `a4d024f0f35630a743653af1542cb02e539fced6`，tree 为 `a982f88c18a6f73d97b2e861b74316d64214d9ae`。PS5 基线配置成功，按预期复现 Found erroneous configuration，I 的链接、镜像编译单元、runtime 图全部满足。主 spec 的默认三架构、八个开关组合和五个场景全部完成平台展开。追加的 rpmbuild `--nobuild` 门槛受工作树无源 tar 限制。

### 对象、提交和冲突

三个输入大小与 SHA256 全部符合。只读 fetch PS1 `da885208aeb52f55c448ff46873d242346727522`，`ls-tree` 找到 `bolt/CMakeLists.txt`，其源码根为独立工作树根目录。先 `git am` v3，验证只改动两个 spec。随后按 A1–A4 各建一提交，恢复 18 个 `DISABLE_LLVM_LINK_LLVM_DYLIB` 位置为变量，由 standalone 和共享 LLVM 条件控制；镜像实现和定义受同一条件控制。A5 删除了 spec 里重复的手工 merge-fdata 安装，保留 CMake 的 `add_bolt_tool` 安装和 RPM 文件清单。llvm-bat-dump 的手工安装保留。

将 PS1 及其后的 C1 提交依次拣选到 PS5。唯一冲突是 `packaging/llvm.spec` 安装入口。使用 HQ 的 `DESTDIR` 和 OpenMP 兼容链接清理，然后运行 PS5 原有 BOLT 安装后流程。清理位于 PS5 安装基线快照之前。其余冲突为零，保留开关、混合链接、BOLT 后处理、`debugfiles.list` 和原 helper。

[C1 diff](../../tools/bolt/results/review-361624/combined/C1.diff)、[C1 提交顺序](../../tools/bolt/results/task133-d/N3-C1-final.json)、[A2 的 18 个位置](../../tools/bolt/results/task133-d/N3-A2-locations.json)、[冲突原文](../../tools/bolt/results/task133-d/N3-install-conflict.diff)、[解决原文](../../tools/bolt/results/task133-d/N3-install-resolution.txt)、[PS5 到 I 的 diff](../../tools/bolt/results/task133-d/N3-I.diff)。

### spec 检查

16 组平台展开全通过，变更归类为三项 Obsoletes、MLGO 增量配置缺资产时的解包、显式 SHA1 build-id、DESTDIR 与 OpenMP 兼容链接、文件列表顺序。所有展开中 BOLT、混合链接和关键门禁标记的次数与 PS5 相同。

| llvm-tools-subpkgs | bolt_targets | 库后缀 | bolt Requires |
|---|---|---|---|
| x86_64 | X86;AArch64 | 64 | libllvm = 22.1.8 |
| aarch64 | AArch64 | 64 | libllvm = 22.1.8 |
| armv7l / i586 | ExclusiveArch 排除 | 不适用 | 不适用 |

x86_64 和 aarch64 的 BuildRequires 原文见证据。独立 `rpmbuild -bp --nobuild --nodeps` 确认 armv7l/i586 被拒绝。其余 12 次缺少导出的 `llvm-22.1.8.tar.gz`。原始展开和两种解析工具的范围分别记录。

[展开和 BuildRequires 原文](../../tools/bolt/results/task133-d/N3-spec.json)、[差异逐组归类](../../tools/bolt/results/task133-d/N3-expanded-classification.json)、[nobuild 的全部回执](../../tools/bolt/results/task133-d/N3-nobuild.json)。

### CMake 配置与 Ninja 图

| 变体 | 返回码 | 时长 | 结果 |
|---|---:|---:|---|
| (i) PS5 | 0 | 347.4s | PS5 基线配置成功 |
| (ii) PS5 + 361624 PS1 | 1 | 342.6s | 按预期复现 Found erroneous configuration |
| (iii) I | 0 | 343.1s | I 的链接、镜像编译单元、runtime 图全部满足 |

配置使用 x86_64 默认展开及 74 号实际编译参数，匹配的平台工具、sysroot 和 MLGO 资产，各变体加上 BOLT 项目，开启 runtime 以获得 ExternalProject 命令。安装与项目构建命令均未执行。CMake 自身执行了编译器探针。首次配置时私有 clang 的资源目录未随工具复制，导致缺少 `stddef.h`，外层误报 libstdc++ 版本过旧。修正一次，显式引用平台资源目录，重复执行三个配置。每个配置有 45 分钟上限。

(ii) 的错误原文

~~~text
-- Skipping FreeBSDKernel plugin due to missing libfbsdvmcore
-- Symbols (liblldb): exporting all symbols from the lldb namespace
-- Could NOT find Doxygen (missing: DOXYGEN_EXECUTABLE)
-- Targeting X86 in llvm-bolt
-- Building BOLT runtime libraries for unknown
CMake Error at cmake/modules/LLVMProcessSources.cmake:113 (message):
  Found erroneous configuration for source file X86BoltMnemonicTables.cpp

  LLVM's build system enforces that all source files are added to a build
  target, that exactly one build target exists in each directory, and that
  this target lists all files in that directory.  If you want multiple
  targets in the same directory, add PARTIAL_SOURCES_INTENDED to the target
  specification, though it is discouraged.

  Please update
  /home/linhao/Toolchain/development/llvm-optimize/temp/task133-d/src-raw/bolt/lib/Target/X86/CMakeLists.txt


Call Stack (most recent call first):
  cmake/modules/LLVMProcessSources.cmake:59 (llvm_check_source_file_list)
  cmake/modules/AddLLVM.cmake:519 (llvm_process_sources)
~~~

(iii) 链接行摘录

~~~text
lib64"  lib64/libLLVMX86CodeGen.a  lib64/libLLVMX86AsmParser.a  lib64/libLLVMX86Desc.a  lib64/libLLVMX86Disassembler.a  lib64/libLLV
~~~

I 的 llvm-bolt 组件库包含 `libLLVMX86Desc.a`，动态 `libLLVM.so` 匹配为 False。镜像编译单元命中 0 项。仅归一化两个工作区路径后，runtime ExternalProject 配置命令等同于 PS5：True；runtime 源码等同：True。未执行独立 runtime 子项目的生成或构建。

[首次配置故障原文](../../tools/bolt/results/task133-d/N3-cmake.json)、[修正后的命令和日志索引](../../tools/bolt/results/task133-d/N3-cmake2.json)、[链接与 runtime 图证据](../../tools/bolt/results/task133-d/N3-graph-summary.json)、[本地日志和大文件路径、字节与 SHA256](../../tools/bolt/results/task133-d/N3-local-artifacts.json)。


## N4：133-N 完整验证

**SKIPPED。**

| 步骤 | 结论 | 档位 | MemoryMax B | 开始 | 结束 | 等待 s | 执行 s | cgroup peak B | MemAvailable B | /home 可用 B | 依据 |
|---|---|---|---:|---|---|---:|---:|---:|---:|---:|---|
| N4 | SKIPPED | — | — | — | — | 1800.004 | — | UNKNOWN | 24288186368 | 385663987712 | MemAvailable minus 8 GiB below reduced MemoryMax |


## 留在本机的证据

| 步骤 | 文件 | 字节 | SHA256 |
|---|---|---:|---|

本地结果目录 /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118。全部步骤状态见[总 JSON](../../tools/bolt/results/task133-n/summary.json)。看门狗触发：否。


## N4：138-N 续跑

**SKIPPED。**

| 步骤 | 结论 | 档位 | MemoryMax GiB | 并行 | 开始 | 结束 | 等待秒 | 执行秒 | 内存峰值 B | 准入 MemAvailable GiB | 准入 /home GiB | 原因 |
|---|---|---|---:|---:|---|---|---:|---:|---:|---:|---:|---|
| N4 | SKIPPED | — | — | — | — | — | 1800.004 | — | — | 19.05 | 370.73 | MemAvailable minus 6 GiB below stage floor |

候选 I 产物核对

~~~json
{
  "audit_main": null,
  "audit_subpackages": null,
  "cleanup_main": null,
  "cleanup_subpackages": null
}
~~~



| 步骤 | 本地路径 | 字节 | SHA256 |
|---|---|---:|---|

单元 llvm-opt-138n-20261119.service，截止 2026-11-20T08:30:00+08:00。启动 MemAvailable 20.22 GiB，/home 可用 352.98 GiB。看门狗触发：否。[逐步 JSON](../../tools/bolt/results/task138-n-20261119/summary.json)
