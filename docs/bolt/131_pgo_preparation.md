# 131 号：PGO 第二批准备与备份目录清理

**本地 pgo-dev 已提交原型，未通过认证。** 48 组平台 RPM 解析通过。初轮既有套件 719/743 通过，新增夹具最后一轮 17/18。A 归档清理在授权修正次数用完后停止，没有删除。D 匹配率保持 UNKNOWN。E dry-run 通过，资源准入及实际构建阶段输入尚未绑定。

| 部分 | 结论 |
|---|---|
| A | 26 个 bundle 保留，删除 0 项，释放 0 B。[清单和错误原文](131_backup_cleanup.md) |
| B | 原型提交在本地 pgo-dev。现有测试及实物转换夹具尚未放行。 |
| C | 旧构建的运行库确实使用过 profile。进度清单和采样证据分别列出。[盘点](131_pgo_scope.md) |
| D | 历史 profile 为 IR，夹具环境 STOP，计数 UNKNOWN。[方法](131_pgo_match_method.md) |
| E | 记录 23 项训练和两个 profile 的离线流程。只进行了 dry-run。 |
| F | [设计 v10](design/tizen_llvm_speed_design_v10.md) 记录总部、PM 和第二批裁决。 |

## B：本地 pgo-dev

基线 `7b05a13744d1cf81a5e9cff22a27eb037bf1b6a8`，tree `66aa08d9e6717b904a0eb390096d908fea1109c0`。候选 `cfcc4da0965449c08231a6e52691a57824e9330e`，tree `ef9c45fb4f6b01f7ac410271153ff7b08552985a`。

[提交列表](../../tools/bolt/results/task131/pgo-dev-commits.tsv)。[PS5 到候选的完整二进制 diff](../../tools/bolt/results/task131/ps5-to-pgo-dev.diff)。

| 项 | 当前结果 |
|---|---|
| B1 | clang_pgo 默认关闭，由 llvm_speedup 在 x86_64 控制。三个 PGO Source 有条件展开，保留 Source1200。占位清单和资产被拒绝。候选加入 CMake 前验证与解压、运行库子目录隔离与 Ninja 命令门禁。 |
| B2 | helper 的 RPM post 路径检查静态归档成员、发货 ELF 节和符号及 profile NEEDED。PGO 开启为硬门禁，关闭记录。真实插桩成员被拒绝，profile-use-only 成员通过。没有全发货集验证。 |
| B3 | 明确将非空 -fprofile-instr-use= 分类为 IR 已体现、后端不重放，拒绝其他 profile 选项。实际生成 Tizen 22.1.8 的 profile-use ThinLTO bitcode。夹具因记录了测试驱动的 --no-default-config，被现有白名单拒绝，未完成真实成员转换。 |
| B4 | 按 T/D × PGO × BOLT 选择唯一映射。PGO 关闭保留 Source1200 和历史 digest。映射夹具覆盖启用、禁用、SHA 不符、占位、缺失及重复。 |
| B5 | 诊断显示项分开提交，涵盖空观察、枚举结束时截止、错误列表、成功退出上下文、非 UTF-8 argv/cwd 和控制字符。保留 fail-closed。test_124 的旧元组夹具尚未维护。 |
| B6 | 平台 RPM 4.14.1 开关解析 48/48。首轮既有套件 719/743，新增最后一轮 17/18。候选未认证。 |

### 默认 spec 展开

三个架构均比 PS5 多出开头 14 个空行，全部来自 RPM 4.14.1 展开新增开关和派生宏定义。逐字节对照中没有其他位置的差异。中间版本在 Source 区域的 5 个空行已移除。默认输入、命令和 Source 选择维持 PS5。

[最终 48 组矩阵](../../tools/bolt/results/task131/spec-matrix-final.json)。[x86_64 默认展开差异](../../tools/bolt/results/task131/default-final-x86_64.diff)。[aarch64 默认展开差异](../../tools/bolt/results/task131/default-final-aarch64.diff)。[armv7l 默认展开差异](../../tools/bolt/results/task131/default-final-armv7l.diff)。

### 测试与停止记录

既有测试断言原样保留。初轮 114 套件有 1 个措辞断言失败，随后代码恢复兼容的 scan incomplete 字样，完整套件没有再认证。109 套件有 23 个失败。其探针仍以历史行号注入信号，本轮在 helper 中插入了代码，导致 hook 命中失效并返回超时等结果。没有把这次运行当作行为回归已排除的证据。

~~~text
AssertionError: "scan incomplete" does not match "session deadline expired after enumeration; verification incomplete; last observed members: "
AssertionError: 'RAISED GateError CANCELLED' not found in "RAISED GateError TIMEOUT: Command '1613122' timed out after 5 seconds (see /home/linhao/Toolchain/development/llvm-optimize/temp/task131/\n"
~~~

新增夹具首轮有 1 个测试使用了错误的返回字段，修正为从真实 bitcode 的记录参数进入转换器。最后一轮剩 1 个错误，编译时仍记录了仅用于夹具的开关，按原策略拒绝，未进一步修正。

~~~text
KeyError: 'options'
ValueError: unclassified original command token: --no-default-config
~~~

B 生成脚本第一次锚点未匹配且未写出 helper，修正其缩进锚点后继续。旧套件的行号注入仍需另外适配，未增加重试。[既有套件汇总](../../tools/bolt/results/task131/regression-results.json)。[24 条原始失败栈](../../tools/bolt/results/task131/regression-failures.json)。[新增夹具命令](../../tools/bolt/results/task131/fixture-commands-final.json)。

## E：离线配对入口与 dry-run

入口只运行 dry-run。20 个真实训练输入的大小和 SHA 与 59 号相同。A/B/C 原件未在旧构建路径，已从 58 号使用的生成配方识别生成器输入，分别用 scale 1/2/2、seed 73419，后续执行须生成并逐份核对历史 SHA。23 项保留完整编译参数。

| 顺序 | 步骤 | 历史耗时 s | 历史 cgroup 峰值 B | 来源 |
|---:|---|---:|---:|---|
| 1 | `instrumented-build` | 4068.547 | 7,227,248,640 | 58 §4 A |
| 2 | `ir-train` | 201.93 | 1,481,818,112 | 58 §4 B |
| 3 | `merge-profdata` | 3.278 | 1,824,751,616 | 58 §4 C |
| 4 | `pgo-build` | 6176 | 21,703,991,296 | 58 §4 D ordinary compile |
| 5 | `bolt-tools` | 418 | UNKNOWN | 58 §4 BOLT tools |
| 6 | `relink-strip-debug` | UNKNOWN | UNKNOWN | 58 §4 cannot separate from failed rewrite |
| 7 | `bolt-instrument` | 77.954 | 17,074,352,128 | 59 §7 |
| 8 | `bolt-train` | 379.427 | 3,890,348,032 | 59 §7 |
| 9 | `merge-fdata` | 3.396 | 1,585,553,408 | 59 §7 |
| 10 | `write-manifest` | UNKNOWN | UNKNOWN | no historical compressed-pair measurement |

已知步骤合计 11,328.532 s，约 3 小时 9 分钟。未包含重链、压缩、环境准备及未知阶段。历史 cgroup 峰值 20.213 GiB。58 号两根共存边界 85.007 GiB，59 号含 30 GiB 保留的已知部分规划值 125.626 GiB，连续峰值未知。

执行器要求提供实际的 127 N0 driver、计划、构建 argv、工具与 loader 身份和 T/D 输入身份。现有证据未找到可复用的 N0 实现，因此正常档、缩减档、看门狗和最多一次 30 分钟后复查尚未验证。入口将未验收的成对产物标为 UNQUALIFIED，产品门禁拒绝该状态。

[入口](../../tools/bolt/results/task131/pgo_pair.py)。[dry-run 输出、训练参数和预算](../../tools/bolt/results/task131/pgo-pair-dry-run.json)。

## 交付范围

没有执行完整构建，也未上传 PGO 候选。归档只推送证据仓库 bolt-v4。超过 10 MB 的文件和忽略的运行日志保留在本地，绝对路径、大小、SHA256 见清单。

[本地证据清单](../../tools/bolt/results/task131/local-artifacts.json)。

既有测试还写出了一个位于 126 号夹具目录的已跟踪诊断 JSON。此次生成副本保存在本地，原文件已按开始时的 HEAD 逐字节恢复，归档没有包含这项旧文件改动。


## 133-D B 续做

**PASS。** 既有 20 套件 743/743，131 新增 18/18，合计 **761/761**。同参数 ThinLTO 验证另作 1 项，compiler-rt/OpenMP CMake 块各复核 1 项。RPM 平台解析 48/48。

1. 将 23 项按行号触发的信号夹具改为查找唯一源码锚点。每个锚点与旧版的同一源码行及上下文逐字匹配，保留 `sys.settrace` 行事件与注入时机。遇到缺失或重复锚点直接失败。没有修改任何断言。
2. 旧诊断中的 `scan incomplete at verification` 已在 131 基底的对应路径保留，复跑通过，无需改文字。
3. `test_124` 的伪进程成员改用三元素 `_StatTuple` 与附加 `comm` 属性，断言不变。
4. Tizen Clang 22.1.8 用 58 号 D 构建采样第 1722 行的实际参数产生 profile-use ThinLTO。替换样例输入输出、include 目录的根路径和现存同一合并 profile 路径。转换器把该参数分类为 IR 已承载，后端命令省略它，生成机器码 ELF；未扩大选项白名单。样例函数并未作为历史训练函数计数。
5. `llvm.spec` 只在 PGO 开启时设置 `TIZEN_PGO_EXCLUDE_RUNTIMES`。compiler-rt/OpenMP 的 CMake 子目录只在该开关下删除继承的 PGO 参数并清空子目录的 `LLVM_PROFDATA_FILE`。核对了两段 CMake 对六类参数变量的处理以及 37 个历史运行库目标、157 个关联边。Ninja 检查要求运行库无 PGO 参数，主构建 C/C++ 只使用已核验路径。此次未运行 PGO 完整构建或独立 runtime Ninja 图。
6. 131 留下的 25 项失败全部清零。此轮完整运行没有失败，不需要第二次修改断言。
7. x86_64、armv7l、aarch64 默认展开各新增 14 个宏定义空行，去掉空行后逐字节等于 PS5。16 × 3 开关解析全部通过。
8. 本地候选 R 为 `2b9031dd9ab46e3fb142da13e64624de3896e8be`，tree 为 `ef9c45fb4f6b01f7ac410271153ff7b08552985a`。产品核对使用 `cfcc4da0` 的同一 tree；R 是通过后的登记提交，测试夹具改动在证据库。

| 测试 | 旧触发行 / 原 H5 源码行 | 唯一定位的原源码 | 现行 |
|---|---:|---|---:|
| `test_claude_h2_deferred_then_third_257` | 257 / 466 | `stderr=subprocess.STDOUT, start_new_session=True)` | 682 |
| `test_claude_h2_deferred_then_third_258` | 258 / 467 | `_ACTIVE_SESSION = process.pid` | 683 |
| `test_claude_h2_deferred_then_third_259` | 259 / 468 | `finally: / _SPAWNING = False` | 684 |
| `test_claude_h2_deferred_then_third_260` | 260 / 469 | `_SPAWNING = False` | 685 |
| `test_claude_h2_deferred_then_third_261` | 261 / 470 | `if _DEFERRED_SECOND_SIGNAL is not None:` | 686 |
| `test_claude_h2_deferred_then_third_262` | 262 / 471 | `pending = _DEFERRED_SECOND_SIGNAL` | 687 |
| `test_claude_h2_deferred_then_third_263` | 263 / 472 | `_DEFERRED_SECOND_SIGNAL = None` | 688 |
| `test_claude_h2_deferred_then_third_264` | 264 / 473 | `record_cancel(pending, None)` | 689 |
| `test_claude_h2_deferred_then_third_265` | 265 / 474 | `rc = peek_child_exit(process, timeout)` | 690 |
| `test_claude_h2_second_at_line_254` | 254 / 463 | `_SPAWNING = True` | 679 |
| `test_claude_h2_second_at_line_255` | 255 / 464 | `_SPAWNING = True / try:` | 680 |
| `test_claude_h2_second_at_line_256` | 256 / 465 | `process = subprocess.Popen(list(map(str, argv)), cwd=cwd, stdout=output,` | 681 |
| `test_claude_h2_second_at_line_257` | 257 / 466 | `stderr=subprocess.STDOUT, start_new_session=True)` | 682 |
| `test_claude_h2_second_at_line_258` | 258 / 467 | `_ACTIVE_SESSION = process.pid` | 683 |
| `test_claude_h2_second_at_line_259` | 259 / 468 | `finally: / _SPAWNING = False` | 684 |
| `test_claude_h2_second_at_line_260` | 260 / 469 | `_SPAWNING = False` | 685 |
| `test_claude_h2_second_at_line_261` | 261 / 470 | `if _DEFERRED_SECOND_SIGNAL is not None:` | 686 |
| `test_claude_h2_second_at_line_262` | 262 / 471 | `pending = _DEFERRED_SECOND_SIGNAL` | 687 |
| `test_claude_h2_second_at_line_263` | 263 / 472 | `_DEFERRED_SECOND_SIGNAL = None` | 688 |
| `test_claude_h2_second_at_line_264` | 264 / 473 | `record_cancel(pending, None)` | 689 |
| `test_claude_h2_second_at_line_265` | 265 / 474 | `rc = peek_child_exit(process, timeout)` | 690 |
| `test_claude_h2_two_real_at_line_258` | 258 / 467 | `_ACTIVE_SESSION = process.pid` | 683 |
| `test_claude_h2_two_real_at_line_265` | 265 / 474 | `rc = peek_child_exit(process, timeout)` | 690 |

[逐项锚点和时机依据](../../tools/bolt/results/task133-d/B-hook-locations.json)、[夹具 diff](../../tools/bolt/results/task133-d/B-legacy-fixtures.diff)、[测试计数、日志路径及 SHA](../../tools/bolt/results/task133-d/B-confirmation.json)、[运行库目标及 CMake 检查](../../tools/bolt/results/task133-d/B-runtime-scope.json)、[转换器实物夹具原始参数](../../tools/bolt/results/task133-d/B-historical-profile-commands.json)、[48 组解析及默认展开](../../tools/bolt/results/task133-d/spec-matrix.json)、[PS5 到 R 的 diff](../../tools/bolt/results/task133-d/B-R.diff)。
