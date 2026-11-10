# 75. 第四轮评审修复：测试夹具失败，已停止

本轮未完成验证，不能交付为已认证的 r5。已有 472 项测试全部通过；新增测试已运行 11 项，10 项通过、1 项因我生成的 LLVM IR 夹具顺序错误而失败，另 3 项未运行。12 组 spec 展开和 5 项 RPM 解析通过；按“任何测试失败就停止”的要求，没有修正后重跑，没有继续 PIC 全量复扫、ARM 下载核验或完整构建，也没有推送 Gerrit/sandbox。

## 1. 用户裁决与设计版本

依据 [设计 v6.1 §7 第 15–17 条](design/tizen_llvm_speed_design_v6.1.md)，记录用户 2026-11-10 的三项裁决：

1. ARM 开发包中 AddLLVM.cmake、AddClang.cmake 的文本变化，作为行为不变的已知例外接受；AddLLD.cmake 是否安装仍待本轮实证核查，不能从提交说明推定已经核实。
2. 本地 T/D 完整构建用 fa4f9978（74 号）；最终 tree 以 QB 逐字节比较衔接。QB 比较出现任何发货内容差异时，这一衔接作废。本轮没有启动完整构建。
3. qemu-accel 取用 Toolchain 的 llvm，测速以 Toolchain 发货二进制为主结论，Base-Dev 为补充。

v6 与 v6.1 都已从 Downloads 移动到 W/docs/bolt/design/，并同步到 bolt-v4 工作树用于发布；v6.1 是当前有效版本，v6 保留为历史版本。移动前后大小和 SHA 相同，Downloads 原路径不存在。证据：[design-moves.json](../../tools/bolt/results/fourth-review-20261110/design-moves.json)。

| 设计 | 字节数 | 移动前后 SHA256 |
|---|---:|---|
| [v6](design/tizen_llvm_speed_design_v6.md) | 75520 | f25e89a2abb6f6c13e552f63c11cfd62d17e756c214970bbd06c515cc314d1af |
| [v6.1](design/tizen_llvm_speed_design_v6.1.md) | 76411 | 8e3025707693d1eae879a90f5ae491a329881d4d5541b1638b8836e4db66e7ee |

## 2. 本地提交与改动归属

起点 fa4f9978；用两个 fixup 归入 BOLT 与固定参数/转换器提交，再 autosquash 到 13c3e223。三个 Change-Id 保留，基线父链未变，没有新增分支。源码工作树干净；以下是本地未完整认证的提交，不是 sandbox 更新结果。

| 提交 | SHA | tree |
|---|---|---|
| cmake: use hybrid LLVM linkage on x86_64 | 8a50d7122346258fd1171d270861a4ae28a8717c | 3d961cbb04f5446f84d2089b4f65f3178f2bd7fa |
| packaging: optimize x86_64 clang with BOLT | 539e2a86532526b88912816c9af4ac9b20767e11 | 9e4948eba61ca48156f5b4534f49adaf0f47cab1 |
| packaging: fix x86 LLVM flags and archive mode | 80217ff8f1eacb78bb92d6ef7251bdb8c46da2ae | d386f458e9b6dd43ba7f54d988726e6f50f18413 |

提交说明全文见 [commits.json](../../tools/bolt/results/fourth-review-20261110/commits.json)，相对起点的完整代码差异见 [changes-since-fa4f9978.diff](../../tools/bolt/results/fourth-review-20261110/changes-since-fa4f9978.diff)。

- 混合链接：只按要求改提交说明，代码 tree 仍为 3d961cbb…。删去过时的 QB pending 说明，加入 ARM 安装模块文字。是否还要写 AddLLD，等待未运行的 ARM 实证。
- BOLT：只改 spec 中 printf 的 RPM 宏转义、bolt_status_exit 与直接 helper 调用的退出码传播；helper 文件未改。所用函数定义归在第二提交。
- 固定参数/转换器：PIC 节表、索引、目标范围检查及 8/16 位绝对重定位；elf_details 节名索引；ar 大小语法与长名边界；版本摘要与 NATIVE_ARCHIVES_TOOLS；取消 traceback/退出码和最后检查之后的取消；SIGCHLD 重置与进程回收保证注释。转换器调用的退出码传播归在第三提交。
- 转换器也在关闭 BOLT 时运行，而 bolt_status_exit 仅在开启 BOLT 时定义。因此在现有 x86_64 块内按 clang_bolt 条件选择新的退出函数或原来的 exit 1；这是保持 BOLT 关闭展开逐字相同所需的衔接。
- 提交说明按用户指定文本调整并折行；原 R3 消息测试验证三个说明每行不超过 72 列、trailer 可解析。本轮没有改 profile、helper、发布 OPTIONS 或白名单。

## 3. 测试结果与停止原文

所有执行串行位于独立 systemd 用户服务，MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、Nice=19、IOSchedulingClass=idle。服务结束行原文转录见 [service-endings.txt](../../tools/bolt/results/fourth-review-20261110/service-endings.txt)；各命令 stdout/stderr 保存于对应测试日志。使用 --pipe，journal 未必保存命令 stdout，[journal 查询结果](../../tools/bolt/results/fourth-review-20261110/service-journal.txt)原样保留。未发生 OOM。测试中原本清理的临时文件转存本轮 scratch 留存目录，历史根只读。

| 套件 | 已运行 | 通过 | 失败 | 原文 |
|---|---:|---:|---:|---|
| 显式 helper 既有套件 | 393 | 393 | 0 | [helper-tests.log](../../tools/bolt/results/fourth-review-20261110/helper-tests.log) |
| 参数/转换器回归 | 46 | 46 | 0 | [policy-tests.log](../../tools/bolt/results/fourth-review-20261110/policy-tests.log) |
| 50 号 release 专项 | 5 | 5 | 0 | [tests50.log](../../tools/bolt/results/fourth-review-20261110/tests50.log) |
| 第二轮新增 | 12 | 12 | 0 | [r2-tests.log](../../tools/bolt/results/fourth-review-20261110/r2-tests.log) |
| cli 异常取消 | 2 | 2 | 0 | [cli-tests.log](../../tools/bolt/results/fourth-review-20261110/cli-tests.log) |
| R3 既有 | 14 | 14 | 0 | [r3-r4-tests.log](../../tools/bolt/results/fourth-review-20261110/r3-r4-tests.log) |
| 本轮新增 | 11 | 10 | 1 | 同上，另 3 项 NOT RUN |
| 合计 | 483 | 482 | 1 | 计划总数 486，不记为全量 PASS |

新增用例已并入既有 test_r3.py；输入准备和 mock 的适配 diff 保存在结果目录。既有 validate_tools 返回值测试增加新字段的预期，mock 增加 tool_versions/tool_directory，以对应新增日志。ar 原有反例只要求 ValueError，未放宽为其他异常。运行器 failfast=True。

已通过的新增检查：ar 大小字段与长名边界；elf_details 节名索引；PIC 8/16 位绝对重定位及 SHN_ABS 例外；目标偏移与宽度；畸形节表/link/info；三种取消信号的中途与最后检查后状态；正常完成及清理后版本保留；run 返回时直接子进程已消失、组内无运行成员的状态记录；真实 release 成员和单成员完整归档的新旧转换字节相同。

失败原文：

~~~text
FAIL: test_real_module_asm_short_byte_rejected
File ".../test_r3.py", line 297, in test_real_module_asm_short_byte_rejected
    self.assertEqual(p.returncode,0,p.stderr)
AssertionError: 1 != 0 : .../usr/bin/llvm-as: .../real/short.ll:3:1: error: expected top-level entity
source_filename = "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/llvm/lib/Target/AArch64/AsmParser/AArch64AsmParser.cpp"
^

Ran 25 tests in 25.033s
FAILED (failures=1)
SERVICE 已结束 2026-11-10T21:58:04+08:00 status=1 unit=llvm-fourth-review-1110-026
~~~

[失败 IR 的开头](../../tools/bolt/results/fourth-review-20261110/failure-ir-header.txt) 是 module asm、ModuleID 注释、source_filename、target datalayout、target triple 的顺序。夹具错误由本轮生成方式造成，不是转换器拒绝了该重定位；llvm-as 还没生成 bitcode，.short 转换及 .byte 用例均未执行。没有修改这个夹具后重试，没有放宽规则。

尚未运行的三个新增 test 方法：shell_status_matrix、sigchld_ignore_exec_real_archive、version_mismatch_before_archive；不能以已有的其他相似测试代替。

## 4. 第三步各项结果

| 检查 | 结果 | 边界/证据 |
|---|---|---|
| 12 组展开 | PASS | [expansion-summary.json](../../tools/bolt/results/fourth-review-20261110/parse/expansion-summary.json)；T/D 的 ARM 与 BOLT 关闭均逐字节相同，x86 开启仅允许退出码传播差异，printf 展开仍是 %s |
| 5 项 Tizen RPM 解析 | PASS | [five-summary.json](../../tools/bolt/results/fourth-review-20261110/parse/five-summary.json)；未构建 |
| 显式平台 post 展开 | PASS | [optional-calls.json](../../tools/bolt/results/fourth-review-20261110/optional-calls.json)，5 个可选调用 |
| 450 归档全部成员 PIC/elf_details 新旧复扫 | NOT RUN | 测试失败后停止，没有沿用上轮结果 |
| 真实 release 成员及完整小归档转换输出 | PASS（单例） | 本轮新增测试已先运行；一个真实成员、一个单成员完整归档，不代表 7706 成员 |
| ARM 两项目两架构下载与模块对照 | NOT RUN | AddLLD.cmake 是否安装未核实；未搜索不含 0001 的同快照候选基线 |
| x86_64 lld 包安装及 ld.lld 归属日志 | NOT RUN | 未作本轮证据摘录 |
| 三个提交说明 72 列/trailer | PASS | 既有 test_messages 本轮已运行 |

新旧完整小归档 SHA256 同为 d4eaca298a50710aa8097dbcbbf7c28aab229f44899a2190fe67eae81fb940e9；1694822 B，1 个转换成员，无调试节。成员 SHA 与来源详见 [real-output-equality.json](../../tools/bolt/results/fourth-review-20261110/real-output-equality.json)。源码与平台工具身份均在测试输出/JSON 中记录；构建树没有执行 cmake/ninja/gbs。

## 5. 未完成交付与后续边界

触发停止条件后，72/73 文档修订、r4 README 与校验清单修订、r5 评审包导出均 NOT RUN；不发布“已通过”的 r5。仅发布设计原文、本停止报告、已生成测试证据和 STATUS。没有 sandbox/Gerrit 推送、QB 操作或完整构建。

后续必须先处理本轮夹具问题，完成剩余测试和实物检查，才能把 75 号标为完成并生成正式 r5。用户指定的下一阶段顺序保留：fa4f9978 夜间完整构建（74 号）、等待用户授权 sandbox 推送、QB 重跑、三家完整评审（设计 v6.1 + 完成认证后的 r5）；本轮不自行启动这些步骤。

下一次 QB 源码包的预定白名单：llvm.spec、llvm-static-archives-native.py、VCS 行，以及 0001 提交说明调整引入的 0008 补丁变化；此处是后续判定计划，不代表本轮已运行 QB。

FOURTH_REVIEW 已结束 2026-11-10T22:03:24+08:00 status=stopped reason=module_asm_fixture_parse_error

## 6. 续跑（2026-11-10）

本节是用户授权修正夹具后的新一轮，从头执行全部套件；第 1–5 节及第一次停止原文完整保留。**本次 487/487 测试通过，12 组展开、5 项解析、450 归档复扫与真实小归档转换比较通过；r5 已导出。** 这里的完成指本轮指定的轻量检查与证据交付，不是新提交已完整构建或发货认证。

### 6.1 起点、三处修正与最终提交

开始时源码 HEAD 为 80217ff8f1eacb78bb92d6ef7251bdb8c46da2ae，工作树干净。转换器修复通过 fixup/autosquash 归入第三提交；两个说明按用户指定句子重新折行并归入原提交，Change-Id 保持不变，没有新建分支。

1. test_real_module_asm_short_byte_rejected 的 module asm 追加在全部原有 IR 后面。只修夹具顺序，不改 .short/.byte 的拒绝预期或转换器规则。[夹具 diff](../../tools/bolt/results/fourth-review-20261110/resume/test_r3.py.resume.diff)。
2. pic_relocations 的偏移检查改为 kind != 0 才检查范围；R_X86_64_NONE 仍参与既有检查计数。新用例在节大小 8、r_offset=8 时，type 0 通过；type 1、10、12、14 均拒绝。[唯一代码修正](../../tools/bolt/results/fourth-review-20261110/resume/resume-code.diff)。
3. BOLT 说明删去“the native archive conversion”；第三提交在 late-cancel 句子后加入开启 BOLT 传递 129/130/143、关闭 BOLT 保持 exit 1/展开不变的说明。其余文字未改。[BOLT 说明 diff](../../tools/bolt/results/fourth-review-20261110/resume/539e2a86532526b88912816c9af4ac9b20767e11.message.diff)、[第三提交说明 diff](../../tools/bolt/results/fourth-review-20261110/resume/80217ff8f1eacb78bb92d6ef7251bdb8c46da2ae.message.diff)。

|提交标题|最终 SHA|tree|
|---|---|---|
|cmake: use hybrid LLVM linkage on x86_64|8a50d7122346258fd1171d270861a4ae28a8717c|3d961cbb04f5446f84d2089b4f65f3178f2bd7fa|
|packaging: optimize x86_64 clang with BOLT|358615447c2596c30aa6d064fc8c388292e443e4|9e4948eba61ca48156f5b4534f49adaf0f47cab1|
|packaging: fix x86 LLVM flags and archive mode|60fabc723f30c5cc04146a9dd83487ebed63f259|90fc87dde4d11c8c57f5d3de45a9995dcc35d5f9|

[完整说明及 trailer 解析](../../tools/bolt/results/fourth-review-20261110/resume/final-commits.json)：三份最大行宽均为 72，标题均小于 50，Change-Id/Signed-off-by 可解析，作者/提交者身份保持 Hao Lin。首提交代码 tree 仍为 3d961cbb04f5446f84d2089b4f65f3178f2bd7fa。ARM 未安装 AddLLD.cmake，故没有触发额外的首提交说明修改。

### 6.2 从头重跑的全部测试

所有命令串行位于独立 systemd 用户服务：MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、Nice=19、IOSchedulingClass=idle；未 OOM、未提高限制。测试使用显式源码文件，调用环境见 [test-invocation.json](../../tools/bolt/results/fourth-review-20261110/resume/test-invocation.json)。测试框架原本清理的临时文件保留到本轮 scratch；历史构建根只读。上一轮 PASS 不计入下表。

|套件|本次运行|PASS|原文|
|---|---:|---:|---|
|helper|393|393|[日志](../../tools/bolt/results/fourth-review-20261110/resume/helper-tests.log)|
|参数/转换器回归|46|46|[日志](../../tools/bolt/results/fourth-review-20261110/resume/policy-tests.log)|
|50 号 release 专项|5|5|[日志](../../tools/bolt/results/fourth-review-20261110/resume/tests50.log)|
|第二轮新增|12|12|[日志](../../tools/bolt/results/fourth-review-20261110/resume/r2-tests.log)|
|cli 异常取消|2|2|[日志](../../tools/bolt/results/fourth-review-20261110/resume/cli-tests.log)|
|R3 既有 + R4 新增|14 + 15|29|[日志](../../tools/bolt/results/fourth-review-20261110/resume/r3-r4-tests.log)|
|合计|487|487|[计数](../../tools/bolt/results/fourth-review-20261110/resume/test-summary.json)|

原始结束输出：

~~~text
helper-tests.log
Ran 393 tests in 26.096s

OK
CANCELLATION_PROBE {"signal": 2, "phase": "after", "rc": 130, "stderr": "BOLT_GATE_FAILED: CANCELLED: cancelled by signal 2 (see /home/linhao/Toolchain/development/llvm-optimize/temp/fourth-review-20261110/resume/helper-tests/tmpa_cs0lke/step.log)\n", "descendants": {"1826637": "gone", "1826638": "gone"}, "both_heartbeats_stopped": true}
CANCELLATION_PROBE {"signal": 2, "phase": "cleanup", "rc": 130, "stderr": "BOLT_GATE_FAILED: CANCELLED: cancelled by signal 2; while handling: COMMAND_ERROR: fixture cleanup trigger (see /home/linhao/Toolchain/development/llvm-optimize/temp/fourth-review-20261110/resume/helper-tests/tmpe1n6i_nw/step.log)\n", "descendants": {"1826640": "gone", "1826641": "gone"}, "both_heartbeats_stopped": true}
policy-tests.log

----------------------------------------------------------------------
Ran 46 tests in 17.763s

OK
tests50.log

----------------------------------------------------------------------
Ran 5 tests in 0.005s

OK
r2-tests.log

----------------------------------------------------------------------
Ran 12 tests in 1.401s

OK
cli-tests.log

----------------------------------------------------------------------
Ran 2 tests in 0.634s

OK
r3-r4-tests.log

----------------------------------------------------------------------
Ran 29 tests in 30.246s

OK
~~~

此前未运行的 shell_status_matrix、sigchld_ignore_exec_real_archive、version_mismatch_before_archive 本次均运行并通过。shell 矩阵包含三种 shell、三个函数、7 种模拟状态及 3 种真实信号，共 90 行；SIGCHLD 忽略后 exec 的真实归档运行成功并打印 NATIVE_ARCHIVES_SIGCHLD_RESET；工具版本不一致在 validate_archive 之前拒绝。新类型 0 用例、真实 module asm .short/.byte 拒绝、取消中途与最后检查后的六种状态、子进程回收全部通过。全部原文：[r3-observed.json](../../tools/bolt/results/fourth-review-20261110/resume/r3-observed.json)、[test_r3.py](../../tools/bolt/results/fourth-review-20261110/resume/test_r3.py)。

### 6.3 展开、解析与 450 归档复扫

[12 组完整展开](../../tools/bolt/results/fourth-review-20261110/resume/parse/expansion-summary.json) 与 [5 项 Tizen RPM 解析](../../tools/bolt/results/fourth-review-20261110/resume/parse/five-summary.json) 全部 PASS。T/D 各自 x86 debug/release 的 BOLT 关闭输出、armv7l/aarch64 输出与 fa4f9978 逐字节相同。x86 BOLT 开启只增加 bolt_status_exit 定义和规定调用的退出码传播；printf 的 %%s 在 RPM 展开后仍为 %s，没有额外差异。每一组完整 stdout、stderr、diff 都保存在 parse/。平台 post 显式展开后五个可选调用位于 481、513、516、524、826 行，见 [optional-calls.json](../../tools/bolt/results/fourth-review-20261110/resume/optional-calls.json)。

使用 QB 1223601/1223602 已下载的 llvm-static-devel 全部 ELF 成员，分别调用 fa4f9978 和本次转换器的 pic_relocations、elf_details。每个归档先对已有 QB 载荷清单核对 SHA；按保全 conversion summary 的成员序号/名字识别 converted/preserved。原生成员的禁止项只统计，不拦截。

|项目|归档|ELF 成员|转换成员|原生成员|旧/新各自受检重定位|新拒绝/异常|旧/新原生禁止项|
|---|---:|---:|---:|---:|---:|---:|---:|
|Toolchain / 1223601|225|3864|3853|11|3763631|0|0 / 0|
|Base-Dev / 1223602|225|3864|3853|11|3763631|0|0 / 0|
|合计|450|7728|7706|22|7527262|0|0 / 0|

转换成员零拒绝，所有成员的旧/新 PIC 结果（含禁止项）及 elf_details 结果逐项一致。不是重新转换 7706 成员，也不是重新计算新编译产物。证据：[脚本](../../tools/bolt/results/fourth-review-20261110/resume/check_qb_archives.py)、[完整运行原文](../../tools/bolt/results/fourth-review-20261110/resume/qb-archive-check.log)、[摘要](../../tools/bolt/results/fourth-review-20261110/resume/qb-archive-summary.json)、[逐成员原始结果](../../tools/bolt/results/fourth-review-20261110/resume/qb-archive-members.jsonl.gz)。

~~~text
ARCHIVE_CHECK 已结束 2026-11-10T22:20:09.182886+08:00 status=ok
SERVICE 已结束 2026-11-10T22:20:09+08:00 status=0 unit=llvm-fourth-review-resume-1110-012
~~~

### 6.4 本次重新执行的转换输出比较

test_old_new_real_conversion_bytes 从真实 release C-2 bitcode 成员生成一个完整小归档，旧 fa4f9978 与本次转换器各执行一次；两份成员和归档逐字节一致，没有沿用第一次结果。[完整记录](../../tools/bolt/results/fourth-review-20261110/resume/real-output-equality.json)：

- ELF 成员：1689400 B，SHA256 ec3c09329a17d0809ac8371d258bf8b9ae364b59b57c0e4f94d123f352696106，无调试节。
- 完整归档：1694822 B，SHA256 d4eaca298a50710aa8097dbcbbf7c28aab229f44899a2190fe67eae81fb940e9，converted=1、preserved=0。
- 同一成员注入 module asm .short/.byte 的两个负例生成了合法 bitcode，并被转换器 PIC 门禁拒绝；夹具修正没有改动门禁。

参数/门禁新旧一致、一个真实转换输出一致、整包一致是不同层次：本轮没有运行新版本整包构建或整包比较，不能由上述两项推出整包已认证。

### 6.5 ARM 安装文件与候选基线

从公开 RBS 地址下载了两个 QB × 两个架构的 llvm-devel、clang 共 8 个 RPM，所有包的 VCS 为 fa4f9978。来源 URL、大小、SHA、完整载荷清单见 [arm-downloads.json](../../tools/bolt/results/fourth-review-20261110/resume/arm-downloads.json) 与 [arm/](../../tools/bolt/results/fourth-review-20261110/resume/arm/)；原始 RPM 和解包副本保留在 W/temp/fourth-review-20261110/resume/arm/。

四组结果全部相同：

|检查|结果|
|---|---|
|AddLLVM.cmake 对 fa4f9978|逐字节相同，SHA256 02222783e87051da8b468a48e411e79a917ac194f4e50939d119f80a8bcfc7b1|
|AddClang.cmake 对 fa4f9978|逐字节相同，SHA256 cc505b09c2856008843c430269fb989648090bdcfd1048ab1c2ca16d2c499480|
|上述两文件对 PS10|完整 diff 正好等于混合链接提交改动|
|AddLLD.cmake|均未安装|
|LLD 开发配置|llvm-devel 提供 LLDConfig.cmake、LLDConfigVersion.cmake、LLDTargets.cmake 及架构对应的 targets 配置|

armv7l 使用 usr/lib/cmake，aarch64 使用 usr/lib64/cmake。无须另下载独立的 lld-devel 包；包目录及 llvm-devel 清单包含了 LLD 开发配置。原始结论：[arm-result.json](../../tools/bolt/results/fourth-review-20261110/resume/arm-result.json)、[运行输出](../../tools/bolt/results/fourth-review-20261110/resume/arm-check.log)。

找到一个**历史候选**：[QB 1214821](https://quickbuild.tizen.org/build/1214821)，Base-Dev 输入快照同为 tizen-base-dev_20261030.061217，Build Package List 明确请求 9b8d74af825d3caab67f8ff7cbc19fcda8a7ad64；49 号 B.1 已证明该 tree 等于 67619ec8，不含混合链接/BOLT。历史 ARM 日志记录 armv7l 成功 5105 秒、aarch64 成功 5940 秒。其公开产物链接为 [armv7l](https://download.tizen.org/RBS/TIZEN/Tizen/Tizen-Base-Dev/tizen-base-dev_20261102.005802/repos/standard/packages/armv7l/) 和 [aarch64](https://download.tizen.org/RBS/TIZEN/Tizen/Tizen-Base-Dev/tizen-base-dev_20261102.005802/repos/standard/packages/aarch64/)，本次访问均返回 **404**，不能称为已取得的 RPM 基线。

Toolchain 在已知 49/57/71/73 号记录中未找到不含混合链接、同快照的 ARM 基线；没有穷举私有 QB，也未启动 QB。[候选记录](../../tools/bolt/results/fourth-review-20261110/resume/arm-baseline-candidates.json)。首次只读候选查询误假定 manifest 只有一个 llvm 项目而退出 1；实际有两个条目，现均记录，以明确的 Build Package List 判定候选。这不是测试或复扫失败，没有更改规则或重复运行失败测试。

### 6.6 x86_64 的 lld 包与提交说明

两份初始化安装清单均**没有名称为 lld 的独立包**。日志有 llvm 包及构建输出 ld.lld 的记录：

~~~text
QB 1223601 L177: [    3s] [114/122] cumulate llvm-22.1.8-1.6
QB 1223601 L220: [    8s] llvm-22.1.8-1.6                       ########################################
QB 1223601 L11673: [ 4340s] -- Creating ld.lld
QB 1223602 L155: [    3s] [94/121] cumulate llvm-22.1.8-4.8
QB 1223602 L239: [   32s] llvm-22.1.8-4.8                       ########################################
QB 1223602 L11618: [ 3432s] -- Creating ld.lld
~~~

日志未打印 /usr/bin/ld.lld 的 rpm -qf/owned-by 归属查询原文，故该归属为 **NOT PRINTED**；不能把“Creating ld.lld”或 BUILDROOT 的符号链接当作依赖包归属记录。完整初始化摘录：[1223601](../../tools/bolt/results/fourth-review-20261110/resume/1223601-initial-packages.txt)、[1223602](../../tools/bolt/results/fourth-review-20261110/resume/1223602-initial-packages.txt)；[查询结果](../../tools/bolt/results/fourth-review-20261110/resume/lld-summary.json)。查找已完成，现有日志的证据缺口明确保留。

三个提交说明脚本检查通过：最大行宽均为 72，最后段只含 Signed-off-by/Change-Id，git interpret-trailers --parse 正确解析；[原文](../../tools/bolt/results/fourth-review-20261110/resume/final-commits.json)。

### 6.7 文档、评审包与未运行项

72 号旧表头已标明“第一次尝试时的边界（已被 §7.2 的全量重跑取代）”。73 号 §8 补充版本证据的间接满足与实际 ITEM2 结束时间，原 FAIL 不删。r4 README 仅修正指定两处表述，18 项 SHA256 校验通过。新 [r5 评审包](../../patches/rebase-359934-20261110-r5/README.md) 含三个带序号的补丁、BOLT 纯文本补丁、相对 fa4f9978/PS10 的完整 diff、九份文件全文、provenance 和校验清单；17 项 sha256sum -c 通过。[r4 校验原文](../../tools/bolt/results/fourth-review-20261110/resume/rebase-359934-20261109-r4-checksums.log)、[r5 校验原文](../../tools/bolt/results/fourth-review-20261110/resume/rebase-359934-20261110-r5-checksums.log)。

下一次 QB 源码包白名单：**llvm.spec、llvm-static-archives-native.py、VCS 行、第一个提交说明改动带来的 0008 补丁变化**。不能把 helper 或其他差异自动加进白名单。

本次没有运行：完整构建、启动演练、90 TU、7706 个成员重新转换、发货整包一致性比较、不可取得的旧 ARM RPM 比较；没有推送 sandbox/Gerrit、重新查询 change 状态或操作 QB。全部测试/本任务第三步指定的可执行检查已经完成；ARM 旧公开产物 404 和 ld.lld 归属日志缺失如上记录，不编造结论。

75 号本次轻量检查与交付完成。接下来依次为：夜间完整构建（fa4f9978，74 号）→等待用户授权推送 sandbox→QB 重跑→三家完整评审（设计 v6.1 + r5 代码）。

FOURTH_REVIEW_RESUME 已结束 2026-11-10T22:32:46+08:00 status=ok reason=487_tests_expansion_archives_and_review_bundle_pass
