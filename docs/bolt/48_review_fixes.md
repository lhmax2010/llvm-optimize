# 48 外部评审修订与轻量认证

本轮**未达到全部上传前门禁**：375 项夹具、GBS 导出、Tizen RPM 五项解析、真实 RUNPATH 和 debugfiles 清单检查通过，但严格的 strip-all LOAD 字节门禁拒绝了历史认证产物。原因已定位：移除非加载符号表会改变落在首个 LOAD 内的三个 ELF 节表定位字段，共 6 个字节；没有自行加入例外。两个本地提交及评审包已保留，**当前 BOLT 提交不能用于夜间完整构建或上传 Gerrit**，等待用户决定是否仅归一化这三个字段。

执行日期：2026-11-02（目录按任务要求命名 20261103）。方案来源均为本轮外部评审及用户逐项要求；实现、测试和下述边界分析由本次执行完成。不把历史验证算作本 revision 的完整构建验证。

证据目录：[review-fixes-20261103](../../tools/bolt/results/review-fixes-20261103/)。源码工作目录为 `W/temp/review-20261102/source`，detached HEAD；新的配置根和临时产物均在 `W/temp/review-20261103/`。没有进入或改变 PGO 源码工作区及其试验目录，没有在历史根运行 CMake/Ninja，没有运行完整构建，没有推送 Gerrit/sandbox，也没有操作 QB。

## 1. 三个驱动的 NEEDED 断言

在 x86_64 普通 ninja 条件分支全部结束之后检查 `bin/clang-22`、`bin/lld`、`bin/llvm-ar`。每个必须是存在的文件，`readelf -dW` 必须成功；NEEDED 命中 `libLLVM*.so` 或 `libclang-cpp*.so` 即退出 1。通过打印 `TIZEN_HYBRID_LINK_OK`。不依赖 BOLT 开关。

夹具覆盖缺少文件、LLVM 共享库依赖、Clang 共享库依赖及正常组件链接。新增断言是本轮对普通 %build 的明确授权改动；没有包装普通 ninja 或改变输出方式。完整 diff：[hybrid-new-diff.txt](../../tools/bolt/results/review-fixes-20261103/hybrid-new-diff.txt)。

## 2. 空组件探测和 FATAL_ERROR

**探测结论：96 个被改写的静态库接口，空组件列表为 0。**

先以原 hybrid 6e9d4f2 完成新根的 `%prep`，没有编译 LLVM。把 full-20261030 保存的完整 CMake argv 和 RPM 环境用于新目录；临时探针只加在新根源码副本中 `llvm_map_components_to_libnames` 后。生产 CMake 当时未改。探针记录所有已通过“STATIC_LIBRARY、interface 包含 LLVM”条件的目标及其实际组件值，不用预设库名筛选。

原文：

```json
{"rewritten": 96, "empty_count": 0, "empty_targets": []}
```

来源：[hybrid-component-probe.tsv](../../tools/bolt/results/review-fixes-20261103/hybrid-component-probe.tsv)、[temporary-config-probe.diff](../../tools/bolt/results/review-fixes-20261103/temporary-config-probe.diff)、[config-hybrid.argv.json](../../tools/bolt/results/review-fixes-20261103/config-hybrid.argv.json)、[config-hybrid.sh](../../tools/bolt/results/review-fixes-20261103/config-hybrid.sh)、[配置原文](../../tools/bolt/results/review-fixes-20261103/config-hybrid.stdout)。

据此在 AddLLVM.cmake 加入 `if(NOT components) message(FATAL_ERROR ...)`，信息含库名及 `declare LINK_COMPONENTS or disable TIZEN_HYBRID_LINK`。随后把生产 CMake 放入同一个新根、另一个新构建目录再次配置，成功：

```text
-- Configuring done (28.4s)
-- Generating done (2.3s)
-- Build files have been written to: /home/abuild/rpmbuild/BUILD/llvm-22.1.8/review-config-guard
```

见 [config-guard.stdout](../../tools/bolt/results/review-fixes-20261103/config-guard.stdout)。另有空组件负例配置夹具，确认出现目标名和 remedy。新配置过程用独立 user systemd 服务限制 4 GiB、swap 0、CPU 200%、nice 19、idle I/O，仅用于本次轻量检查，不进入发布代码。新根无残留挂载，见 [new-root-mount-check.txt](../../tools/bolt/results/review-fixes-20261103/new-root-mount-check.txt)。

## 3. USE_SHARED 注释

clang driver、lld driver、llvm-ar 的 `set(USE_SHARED "")` 上各加一行：

```cmake
# add_llvm_executable is a macro and never clears USE_SHARED; reset it here.
```

没有改变它们的值或执行条件。

## 4. hybrid 提交说明与历史证据

新说明引用 [main/docs/53](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/main/docs/53_hybrid_local_validation.md) 的实际结果：22 个二进制 RPM + 1 个 SRPM；188 项中 183 PASS、4 个非默认目标未产出、AnnotateFunctions.so 的一个 `--as-needed` 例外经 PM 接受；225/225 原生归档、90 个完整对象相同。本 revision 的 QB 验证待完成。`static-devel packaging` 改为 `the static-devel %files rules`。

五个点名工具 `llvm-tblgen`、`clang-tblgen`、`lldb-tblgen`、`llvm-config`、`llvm-exegesis` 均逐项核查 docs/53 的 NEEDED 原始行：PASS，实际无 libLLVM/libclang-cpp 共享依赖，所以保留原说明。原文：[five-static-tools.json](../../tools/bolt/results/review-fixes-20261103/five-static-tools.json)。说明差异：[hybrid-message.diff](../../tools/bolt/results/review-fixes-20261103/hybrid-message.diff)。

## 5. SIGTERM/SIGHUP 取消处理

处理器只记录信号号；Popen 前和 `peek_child_exit` 每次轮询检查，抛 GateError，复用现有 killpg、等整个进程组退出、回收 leader 的路径。CLI finally 恢复原 SIGTERM/SIGHUP 处理器。

六个真实 CLI 探针覆盖两个信号 × 创建前/创建后/清理期间。子进程和孙进程分别写心跳；只给 helper 发信号。创建后及清理期间的探针确认两代进程均消失，两个心跳在至少两个周期后不再增长。示例原文：

```text
BOLT_GATE_FAILED: COMMAND_ERROR: cancelled by signal 15 (see /tmp/tmpbuto5xp7/step.log)
```

完整六行含 PID 状态、退出码和 stderr，见 [tests-final-complete.stdout](../../tools/bolt/results/review-fixes-20261103/tests-final-complete.stdout) 的 `CANCELLATION_PROBE`。测试仅在探针 wrapper 内加入定时等待以命中竞态窗口，不在生产 helper 加测试开关。

## 6. RUNPATH 精确字节门禁

可变范围只从改写前的 DT_RPATH/DT_RUNPATH 字符串计算（含 NUL），并带入改写后比较；不再放过整个 `.dynamic`、`.dynstr`。所有其他文件字节、程序头和节头冻结。DT_FINI、DT_RELA、非路径 dynstr 字节负例失败；缩短路径、去尾部空项、原路径相同通过。

真实离线检查 PASS。full-20261030 的 `clang.bolt` 仍在；其原始 strip-all 中间文件已在后续原地 RUNPATH/debuglink 操作中改变，因此没有把最终 4f08 文件冒充中间文件。本轮只复制 `clang.bolt` 到新临时目录，使用同一 llvm-strip、同一 `--strip-all` 重现：

| 角色 | SHA256 |
|---|---|
| full-20261030 clang.bolt | `de2ae6e3ed1040505151c9b88b66ef1b6383f51058e6535d0a107287a1658e9d` |
| 重现的 strip-all 输出 | `13a07cb7f84bd1ceda4d851c8bd71bddf7ef0c2d4864892eba64cbbb9a0350b8` |
| 保全的 39 号 RUNPATH 输出 | `8c2429d870f421a29a9914458bc4d4ff2ce359a15e0bdd20f39bfb4580c40bdf` |

后两者均逐项对上 full-20261030 的 identity 记录。唯一允许的字节区间是 `[7070519,7070589)`，新门禁返回 `rpath_gate_pass: true`。完整路径、实际 argv、工具 SHA 和结果：[real-offline-gates.json](../../tools/bolt/results/review-fixes-20261103/real-offline-gates.json)。没有重新链接、运行 BOLT 或修改历史文件。

## 7. strip-all 布局门禁：阻断，待裁决

按要求在 pipeline 的 strip-all 之后、RUNPATH 之前加入程序头和 LOAD 全部字节的比较；包含偏移。夹具覆盖 LOAD 地址变化、内容变化拒绝，以及只移除非加载符号表通过。

**真实产物不能通过“所有 LOAD 原始字节 SHA 相同”的原要求。** 原文：

```text
strip-all changed program headers or LOAD content
```

程序头完整相同，五个 LOAD 的地址、文件偏移、filesz/memsz、flags、alignment 全部相同。4 个 LOAD 原始 SHA 完全相同；首个 LOAD 从文件偏移 0 开始，包含 ELF header，只有以下三项改变：

| ELF 字段 | 字段范围 | strip 前 | strip 后 | 实际变化字节 |
|---|---|---:|---:|---|
| e_shoff | [40,48) | 185673536 | 152529864 | 40、41、42、43 |
| e_shnum | [60,62) | 43 | 38 | 60 |
| e_shstrndx | [62,64) | 40 | 37 | 62 |

首个 LOAD 原始 SHA：`8bfb86945911e34977fdc0c10668a6d9a8d4643569c99b7299fa50ea0b6efd1c` → `b4c6f8f54e5ab4b4c848b9310328d00e4171cde32aefc2be6827942b72b9b410`。这不是代码地址或指令改变，而是非加载符号/节移除后更新 ELF 节表索引信息。

证据：[strip-layout-initial.json](../../tools/bolt/results/review-fixes-20261103/strip-layout-initial.json)、[strip-real-gate.json](../../tools/bolt/results/review-fixes-20261103/strip-real-gate.json)。分析脚本仅在内存中归一化这三个字段后，五个 LOAD SHA 全部相同，见 [strip-header-diagnosis.json](../../tools/bolt/results/review-fixes-20261103/strip-header-diagnosis.json)。**这只是建议的依据，没有将例外写进 helper。** 已向用户询问是否允许仅这三个字段归一化；未收到裁决，不把这一项改判 PASS。当前本地提交保留严格门禁，不能用于后续完整构建。

## 8. debugfiles 清单进包检查

平台实际使用唯一清单为 RPM BUILD 源目录下的 `debugfiles.list`，即 `Path(ordinary).parent.parent.parent / 'debugfiles.list'`；不搜索或接受其他同名清单。

full-20261030 `evidence/rpm-build.log:24230` 原文：

```text
[ 7350s] + /usr/lib/rpm/find-debuginfo.sh -j8 --build-id-seed 22.1.8-1 --unique-debug-src-base llvm-22.1.8-1.x86_64 -S debugsourcefiles.list /home/abuild/rpmbuild/BUILD/llvm-22.1.8
```

平台脚本 `find-debuginfo.sh:116` 默认 `out=debugfiles.list`；真实清单第 36 行为 `/usr/lib/debug/usr/bin/clang-22.debug`。清单 SHA `c2bd719f9ca31f97dce92477277060f19f04c24d08b4988b26067c9d69c6c5f0`。

post 在 debug identity 下要求该文件存在并有精确路径（可为 `./usr/lib/debug/usr/bin/clang-22.debug`）；release 不检查。真实清单 PASS，五个夹具分别覆盖普通路径、./ 前缀、缺条目、缺清单、release 跳过。证据：[完整清单](../../tools/bolt/results/review-fixes-20261103/full-20261030-debugfiles.list)、[日志摘录](../../tools/bolt/results/review-fixes-20261103/debugfiles-log-excerpts.txt)、[real-offline-gates.json](../../tools/bolt/results/review-fixes-20261103/real-offline-gates.json)。

## 9. run_step 超时

按用户的暂定授权，固定 `14400` 秒，无环境开关。超时沿用 call 的进程组清理，错误补充 `step=<name> elapsed_seconds=<实测>`。短超时夹具只在测试中把传入的 14400 映射为 0.1 秒，并断言生产值确为 14400；sleep 子组被清理。正常步骤通过。

## 10. 未预期异常

保留原有 except，再加 `except Exception`：先 diagnose_safely，输出 `BOLT_GATE_FAILED: unexpected <类型>: <信息>`，然后 raise 保留 traceback。post 的缺键 state JSON 真实 CLI 夹具确认非零、KeyError 前缀和 traceback 均存在。没有把未知异常转为成功。

## 11. 磁盘标签

`not-disk` 改为 `unconfirmed`，不再把“可读日志没有命中写满文本”说成已排除磁盘原因。`disk`、`unknown` 判据和实测推算公式不改，夹具断言同步。

## 12. spec 小改

四个 disk-report、一个 cache-release 均加 `|| true`。两个实际 Ninja 子命令改为 `-- env LC_ALL=C NINJA_STATUS='[%%f/%%t] ' ninja ...`，不依赖 shell 函数临时变量导出。子进程环境夹具确认展开后收到 `LC_ALL=C` 和 `NINJA_STATUS=[%f/%t] `（末尾空格保留）。debug 路径拒绝处增加平台 debug-path 策略说明，不改变原检查。

普通 ninja、普通安装、Source1005、平台后处理执行方式未包装；只有第 1 项授权的独立 hybrid NEEDED 断言新增在普通构建之后。完整源码差异：[source-diff.txt](../../tools/bolt/results/review-fixes-20261103/source-diff.txt)。

## 13. BOLT 提交说明

按代码实际顺序重写流程，明确 compare-root 后才允许 BOLT 改 buildroot。区分候选准备失败、安装/后处理失败，说明后者中止 RPM 但不整体回滚 BUILDROOT；磁盘结论为证据和实测推算。

历史性能明确不是最终 debuglink 重新测量。x86 独立20/留出10数据可从既有 validation-performance.json 逐条得到：`0.8543989745506342 / 0.8588801173123148`，保存计算输入与分组于 [x86-historical-cohorts.json](../../tools/bolt/results/review-fixes-20261103/x86-historical-cohorts.json)，因此补入说明，未发起新性能测试。ARM/AArch64 历史值保持。

核对 37 号 §10：同轮 `183,224,160 → 152,532,296`，缩小 16.75%，说明明确比较 previous appended-text layout；42 号工具矩阵记载 only-keep-debug 为 SIGSEGV (-11)，不是 clang 的 pragma crash 所用 SIGILL。新增五道门禁各用一句描述，保留 `pending Quickbuild verification`。说明折行不超过 72 列。完整差异：[bolt-message.diff](../../tools/bolt/results/review-fixes-20261103/bolt-message.diff)。

## 14. 显式 helper 的测试入口

新增 [run_review_tests.py](../../tools/bolt/run_review_tests.py)，`--helper` 必填，先打印绝对路径和 SHA，再发现全部 `test_*.py`。本轮最终结果：

```text
Ran 375 tests in 7.790s
OK
```

旧 f308fe08 helper 的 debuglink 负控制：30 项、29 个错误、退出 1，证明旧实现不会假通过。见 [old-helper-negative.stderr](../../tools/bolt/results/review-fixes-20261103/old-helper-negative.stderr)。本轮保留原 347 个文件内测试，新增 28 个；历史 348 数包含旧临时 runner 额外注入的 OPTIONS 检查，本轮将参数/白名单不变检查纳入正式 test 文件，而非继续依赖临时 runner。

旧夹具改动的原因：磁盘枚举名变更；磁盘子进程必须加载同一个显式 helper，不能偷偷 import 工具目录的旧镜像；debug post 准备真实格式的清单；模式测试 mock 新 strip 门禁并断言调用一次；RUNPATH mock 提供新接口的原始可变范围。没有删除失败条件。新增测试包含 hybrid shell/configuration 负例。

首轮测试缺宿主 cmake；使用本轮新根的 CMake 和 loader，在临时宿主探针目录执行，不进历史根。随后修正测试子进程 sys.path 和新门禁 mock。每轮失败输出保留，不混称产品失败。最终 stdout/stderr：[tests-final-complete.stdout](../../tools/bolt/results/review-fixes-20261103/tests-final-complete.stdout)、[tests-final-complete.stderr](../../tools/bolt/results/review-fixes-20261103/tests-final-complete.stderr)。

## 15. OFF 展开：完整原文，不隐藏空行

Tizen RPM debug/release 两模式均保存完整 `rpmspec -P` 原文和 unified diff，无空白归一化。比较对象是本轮新 BOLT 与其新 hybrid 父提交；另一组为新 BOLT 与 3ee2d847，均关闭 BOLT。

| 比较 | debug | release | 原因 |
|---|---|---|---|
| 新 BOLT vs 新 hybrid | 2 个 Source + 14 个空行 | 同左 | Source1200/1201 无条件声明；既有 BOLT 宏条件块留下空行 |
| 新 BOLT OFF vs 3ee2d847 OFF | 仅本轮 hybrid NEEDED 断言 | 同左 | %build 的明确新增检查；无 BOLT 流水线泄漏 |

14 个空行逐块：开头 BOLT bcond/架构块 7 行；Source 后 util-linux 架构块的额外结束/间隔 1 行；BOLT BuildRequires 条件块 6 行。这些格式差异在本轮前已存在，未借此次任务改写旧宏布局。因而“预期只有两个 Source”在**非空行**成立，在**原始全文**不成立；这里不声称逐字节相同。

完整差异：[debug vs hybrid](../../tools/bolt/results/review-fixes-20261103/parse-bc0d58ffaab3-retry1/off-debug-vs-hybrid.diff)、[release vs hybrid](../../tools/bolt/results/review-fixes-20261103/parse-bc0d58ffaab3-retry1/off-release-vs-hybrid.diff)、[debug vs 3ee](../../tools/bolt/results/review-fixes-20261103/parse-bc0d58ffaab3-retry1/off-debug-vs-previous.diff)、[release vs 3ee](../../tools/bolt/results/review-fixes-20261103/parse-bc0d58ffaab3-retry1/off-release-vs-previous.diff)。辅助分类 JSON 不替代这些原文。

## 16. 静态包基线和四个非默认目标

**未找到能确证为精确 67619ec8 完整构建的保全产物；本轮不冒用其他版本逐包比较。** 已保全 baseline-products 的 SRPM VCS 是 `platform/upstream/llvm#9e5675f57d122549997caffa39b655dfefc46fee`，该轮开启 BOLT；rpms-docs35 的 SRPM VCS 是 `platform/upstream/llvm#f111162e94aa48ed367c9d2c039456c70e7160ae-dirty`。docs/38 还明确为单独 llvm-strip 改动的续跑，不是可直接等同本次要求的纯 67619ec8 完整构建。

两份 SRPM 的实际路径、大小、SHA 和查询原文：[baseline-artifact-search.json](../../tools/bolt/results/review-fixes-20261103/baseline-artifact-search.json)。没有进行归档成员/逐包比较，不由“归档转换器相同”推导产物相同；列为材料缺口。

新目录分别用 67619ec8 和 hybrid 完整配方配置（不运行 Ninja），解析保存的 Ninja 文本图，沿默认 `all` 的显式/隐式/order-only 输入递归计算闭包。四项在两份图中都有构建边，但均不在默认闭包：

- `lib64/libomp_testing.so`
- `projects/openmp/runtime/unittests/String/StringTests`
- `bin/clang-fuzzer`
- `bin/clang-objc-fuzzer`

结果含原始边：[nondefault-four-targets.json](../../tools/bolt/results/review-fixes-20261103/nondefault-four-targets.json)；完整两份 build.ninja、rules.ninja、CMakeCache 以 xz 保存于同目录。默认闭包结论是静态图证据，不宣称重新构建过这些目标。

## 17. 新评审包和验收界线

[review-20261103/README.md](../../patches/review-20261103/README.md) 含两个完整 format-patch、BOLT 纯文本 diff、8 个完整文本文件、提交说明、blob SHA、最终完整递归 ls-tree（xz），并明确标为**第 7 项阻断，不能上传/完整构建**。源码包加入 profile/helper，OFF 的二进制设计契约与同一 hybrid 基线一致；本轮未做新的 RPM 全量实物验证。

上传前和发布前验收分栏；release 完整构建、当前 revision QB、正常依赖装包、Clang/LLD 组件消费者、accel/worker、ARM 根、BOLT/重链资源实测都未标 PASS。旧 review-20261102 包未修改。

## 18. 最终轻量检查与提交身份

| 项目 | 结果 |
|---|---|
| 新 hybrid guard 配置与空组件负例 | PASS |
| 全部显式 helper 测试 | 375/375 PASS |
| GBS export | PASS，退出 0 |
| Tizen RPM x86 ON/OFF/一行回退/armv7l/aarch64 | 5/5 PASS；8 个生成 Patch |
| 真实 RUNPATH / debugfiles | PASS / PASS |
| 真实 strip LOAD 门禁 | **BLOCKED**（第 7 节） |
| profile、Source1005、OPTIONS、111+2 白名单 | 不变 |
| 两份 format-patch 顺序应用 | PASS，得到相同最终 tree |
| 完整构建、实物 RPM 新验证、Gerrit/sandbox | NOT RUN / 未推送 |

RPM 首次版本探针误把 `rpm --version` 的显示值 `4.14.1` 当作发行包版本；其安装包查询为 **4.14.1.1**，改用 `rpm -q --qf` 后重做解析。首轮原文保留，没有换工具、放宽解析或执行 `%prep/%build`。最终五项原文：[five-parse.json](../../tools/bolt/results/review-fixes-20261103/parse-bc0d58ffaab3-retry1/five-parse.json)。

| 提交 | SHA / tree / parent |
|---|---|
| hybrid | `38477c9b6e1401e5e1fe01fafa282ab92cf53887` / `0ce98bed0e7e92780ca6d9f8d316d1ee422fb8d6` / `67619ec8bbbac7238a6cfc33a481ccfbcd12206f` |
| BOLT（阻断稿） | `bc0d58ffaab37dbcd88098ccb4c3734570345593` / `d2a5e457ecd5d439a9dd50b67fb561a5f0d67eb3` / `38477c9b6e1401e5e1fe01fafa282ab92cf53887` |

作者/提交者/Signed-off-by 均 Hao Lin <hao.lin@samsung.com>，两个 Change-Id 原样保留。源码工作区干净，detached HEAD；hybrid 与 BOLT 的 %build 冲突仅在 ninja 条件结束处，保留双方逻辑并将 NEEDED 检查放到整个条件之后。证据：[commit-identities.json](../../tools/bolt/results/review-fixes-20261103/commit-identities.json)、[cherry-pick-conflict-resolution.txt](../../tools/bolt/results/review-fixes-20261103/cherry-pick-conflict-resolution.txt)、[patch-apply-check.json](../../tools/bolt/results/review-fixes-20261103/patch-apply-check.json)。

## 19. 交付与下一步

本轮仅向 GitHub bolt-v4 提交代码审查材料、测试及文档。第 7 项应先由用户裁决：是否允许仅归一化 ELF header 的 e_shoff/e_shnum/e_shstrndx，仍冻结所有程序头、所有 LOAD 的地址/偏移/大小/标志和其余每个字节；或坚持原始 LOAD SHA 相同并保持阻断。**未得到裁决前，不应以此 BOLT 提交启动完整构建。**
