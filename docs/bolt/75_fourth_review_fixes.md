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
