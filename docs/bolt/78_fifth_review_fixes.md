# 78. 第五轮评审修复：测试准备错误，按门禁停止

设计 v7 已入库，代码已通过 fixup/autosquash 归入第二、第三提交，混合链接提交未改。**测试未通过：helper 已运行 199 项，198 PASS、1 ERROR；计划总数 499，其余 300 项未运行。** 错误由我准备测试副本时改坏夹具路径引起，不是产品规则拒绝。已按门禁停止，没有修正后重跑、没有实物复扫或 sandbox 推送。

## 1. 起点与 v7

源码起点 60fabc723f30c5cc04146a9dd83487ebed63f259，工作树干净；已读 STATUS、75 号 §6、77 号。bolt-v4 起点 29be7b94a6506850f59dadeda45b16027c10d081。

[v7](design/tizen_llvm_speed_design_v7.md) 从 Downloads 移动到 W/docs/bolt/design/，再同步到 bolt-v4 工作树用于发布，旧版本不动。Downloads 原文件已不存在；移动前后均为 81285 字节，SHA256 为 11dc134f38945d3fe50ed3bd8a5cb73ef7bfbfdac49431001f3a0e863818d004。[移动记录](../../tools/bolt/results/fifth-review-20261111/design-move.json)。

## 2. 本地代码修改（尚未认证）

完整 [代码 diff](../../tools/bolt/results/fifth-review-20261111/changes-since-60fabc72.diff) 与 [提交说明/身份](../../tools/bolt/results/fifth-review-20261111/local-commits.json)。仍是原来的三个提交，基线 13c3e223 → cf4b6777，不新建分支。

| 标题 | SHA | tree |
|---|---|---|
| cmake: use hybrid LLVM linkage on x86_64 | 8a50d7122346258fd1171d270861a4ae28a8717c | 3d961cbb04f5446f84d2089b4f65f3178f2bd7fa |
| packaging: optimize x86_64 clang with BOLT | 1e415935a83a187aab7c41f9713115a0974a0365 | c23914776684bf94fdd5961f447f7c24e7bb79bc |
| packaging: fix x86 LLVM flags and archive mode | ae4487251aaa00c2ec4edf033cf8c9046d0d4b98 | bea0348f632ba68d995af66c53fe13b978852009 |

按用户本轮条目归属：

| 条目 | 实现 | 证据 |
|---|---|---|
| 1 | bolt_fail / bolt_checked 的两处诊断改为传递 bolt_status_exit | 完整 diff 的 llvm.spec |
| 2–3 | helper 保存结果/异常，恢复处理器后决定状态；取消打印 BOLT_CANCELLED 并返回 128+signal，未预期异常 traceback；保持原 SIG_IGN | 完整 diff 的 cli |
| 4–9 | 显式宽度表；拒绝动态/未知类型；非 NULL/NOBITS 节范围；压缩目标 ch_size；拒绝 CREL；符号表 sh_link；ar 纯数字长名 | 完整 diff 的转换器 |
| 10–11 | install_main 恢复处理器后决定状态；install_main / install / convert 保留 SIG_IGN；不改 SIGCHLD | 同上 |
| 12 | Commands.run 按指定说明进程组、subreaper、离组和不可中断睡眠边界 | 同上 |
| 13–14 | BOLT / 转换器说明替换指定句子、折行；Change-Id 保留 | 提交 JSON |

准备提交说明时有一次路径无关的断言失败：准备脚本要求段落以 “Check Python…” 开始，但原文该句位于 “Handle SIGTERM…” 段中；当时尚未生成 fixup，随后按原句匹配完成修改。这发生于测试前；本节不将它记为测试结果。

## 3. 重定位宽度表

类型来自保全的 LLVM 22.1.8 [x86_64.def](../../tools/bolt/results/fifth-review-20261111/x86_64.def)；字段来自 [psABI object-files.tex](https://gitlab.com/x86-psABIs/x86-64-ABI/-/blob/master/x86-64-ABI/object-files.tex) 的 Relocation Types / Large Model Relocation Types。[下载原文](../../tools/bolt/results/fifth-review-20261111/psabi-object-files.tex)。LP64 wordclass 为 8 B，COPY 无固定字段，TLSDESC_CALL 为零宽标记；LLVM 表外类型均拒绝。

这是**静态定义**：44 种中接受 37 种、拒绝 7 种动态链接专用类型；不能当成真实 census 或零拒绝证明。

| 编号 | 名字 | 字段字节数 | 策略 | 依据 |
|---:|---|---:|---|---|
| 0 | R_X86_64_NONE | 0 | 接受 | psABI Relocation Types: none (linker marker) |
| 1 | R_X86_64_64 | 8 | 接受 | psABI Relocation Types: word64 |
| 2 | R_X86_64_PC32 | 4 | 接受 | psABI Relocation Types: word32 |
| 3 | R_X86_64_GOT32 | 4 | 接受 | psABI Relocation Types: word32 |
| 4 | R_X86_64_PLT32 | 4 | 接受 | psABI Relocation Types: word32 |
| 5 | R_X86_64_COPY | 0 | 拒绝：动态链接专用 | psABI Relocation Types: none (COPY has no fixed field) |
| 6 | R_X86_64_GLOB_DAT | 8 | 拒绝：动态链接专用 | psABI Relocation Types: word64 |
| 7 | R_X86_64_JUMP_SLOT | 8 | 拒绝：动态链接专用 | psABI Relocation Types: word64 |
| 8 | R_X86_64_RELATIVE | 8 | 拒绝：动态链接专用 | psABI Relocation Types: word64 |
| 9 | R_X86_64_GOTPCREL | 4 | 接受 | psABI Relocation Types: word32 |
| 10 | R_X86_64_32 | 4 | 接受 | psABI Relocation Types: word32 |
| 11 | R_X86_64_32S | 4 | 接受 | psABI Relocation Types: word32 |
| 12 | R_X86_64_16 | 2 | 接受 | psABI Relocation Types: word16 |
| 13 | R_X86_64_PC16 | 2 | 接受 | psABI Relocation Types: word16 |
| 14 | R_X86_64_8 | 1 | 接受 | psABI Relocation Types: word8 |
| 15 | R_X86_64_PC8 | 1 | 接受 | psABI Relocation Types: word8 |
| 16 | R_X86_64_DTPMOD64 | 8 | 拒绝：动态链接专用 | psABI Relocation Types: word64 |
| 17 | R_X86_64_DTPOFF64 | 8 | 接受 | psABI Relocation Types: word64 |
| 18 | R_X86_64_TPOFF64 | 8 | 接受 | psABI Relocation Types: word64 |
| 19 | R_X86_64_TLSGD | 4 | 接受 | psABI Relocation Types: word32 |
| 20 | R_X86_64_TLSLD | 4 | 接受 | psABI Relocation Types: word32 |
| 21 | R_X86_64_DTPOFF32 | 4 | 接受 | psABI Relocation Types: word32 |
| 22 | R_X86_64_GOTTPOFF | 4 | 接受 | psABI Relocation Types: word32 |
| 23 | R_X86_64_TPOFF32 | 4 | 接受 | psABI Relocation Types: word32 |
| 24 | R_X86_64_PC64 | 8 | 接受 | psABI Relocation Types: word64 |
| 25 | R_X86_64_GOTOFF64 | 8 | 接受 | psABI Relocation Types: word64 |
| 26 | R_X86_64_GOTPC32 | 4 | 接受 | psABI Relocation Types: word32 |
| 27 | R_X86_64_GOT64 | 8 | 接受 | psABI Large Model Relocation Types: word64 |
| 28 | R_X86_64_GOTPCREL64 | 8 | 接受 | psABI Large Model Relocation Types: word64 |
| 29 | R_X86_64_GOTPC64 | 8 | 接受 | psABI Large Model Relocation Types: word64 |
| 30 | R_X86_64_GOTPLT64 | 8 | 接受 | psABI Large Model Relocation Types: word64 |
| 31 | R_X86_64_PLTOFF64 | 8 | 接受 | psABI Large Model Relocation Types: word64 |
| 32 | R_X86_64_SIZE32 | 4 | 接受 | psABI Relocation Types: word32 |
| 33 | R_X86_64_SIZE64 | 8 | 接受 | psABI Relocation Types: word64 |
| 34 | R_X86_64_GOTPC32_TLSDESC | 4 | 接受 | psABI Relocation Types: word32 |
| 35 | R_X86_64_TLSDESC_CALL | 0 | 接受 | psABI Relocation Types: none (linker marker) |
| 36 | R_X86_64_TLSDESC | 16 | 拒绝：动态链接专用 | psABI Relocation Types: word64 x 2 |
| 37 | R_X86_64_IRELATIVE | 8 | 拒绝：动态链接专用 | psABI Relocation Types: word64 |
| 41 | R_X86_64_GOTPCRELX | 4 | 接受 | psABI Relocation Types: word32 |
| 42 | R_X86_64_REX_GOTPCRELX | 4 | 接受 | psABI Relocation Types: word32 |
| 43 | R_X86_64_CODE_4_GOTPCRELX | 4 | 接受 | psABI Relocation Types: word32 |
| 44 | R_X86_64_CODE_4_GOTTPOFF | 4 | 接受 | psABI Relocation Types: word32 |
| 45 | R_X86_64_CODE_4_GOTPC32_TLSDESC | 4 | 接受 | psABI Relocation Types: word32 |
| 50 | R_X86_64_CODE_6_GOTTPOFF | 4 | 接受 | psABI Relocation Types: word32 |

## 4. 测试准备、结果与停止

独立 systemd 用户服务串行执行，MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、Nice=19、IOSchedulingClass=idle，无 OOM。scratch 为 W/temp/fifth-review-20261111/；测试清理动作转存到 retained-cleanup，历史目录只读、不删除文件。

本轮测试副本、修改 diff、输入及完整日志位于 [证据目录](../../tools/bolt/results/fifth-review-20261111/)。修改的预期仅有：helper 最后阶段取消输出改为 BOLT_CANCELLED: signal 15；PIC 宽度 (2,1) 改为 (2,4)。R5 新增 12 个 test 方法并入 test_r3.py，覆盖诊断矩阵、恢复窗口真实信号、继承忽略、重定位边界、payload/NOBITS、压缩、CREL、sh_link、ar 数字。其 subTest 不重复计数，均尚未运行。

显式展开平台 post 宏的准备输入已生成，5 个可选调用齐全；只完成首个 T debug-on 对照，不等于第三步 12/5 全量展开解析。

| 套件 | 计划 | 运行 | PASS | ERROR |
|---|---:|---:|---:|---:|
| helper | 393 | 199 | 198 | 1 |
| 参数/转换器 | 46 | 0 | 0 | 0 |
| release 专项 | 5 | 0 | 0 | 0 |
| 第二轮新增 | 12 | 0 | 0 | 0 |
| cli 异常取消 | 2 | 0 | 0 | 0 |
| R3/R4 + R5 | 29 + 12 | 0 | 0 | 0 |
| 合计 | 499 | 199 | 198 | 1 |

[helper-tests.log](../../tools/bolt/results/fifth-review-20261111/helper-tests.log)、[failure.txt](../../tools/bolt/results/fifth-review-20261111/failure.txt)、[计数 JSON](../../tools/bolt/results/fifth-review-20261111/test-summary.json)：

~~~text
ERROR: test_fourth_review (unittest.loader._FailedTest.test_fourth_review)
ImportError: Failed to import test module: test_fourth_review
FileNotFoundError: [Errno 2] No such file or directory: '/review-closure-v3.py'
Ran 199 tests in 15.863s
FAILED (errors=1)
已结束 2026-11-11T14:37:36+08:00 status=1 unit=llvm-review78-1111-025
~~~

原因：将测试副本的 results/review-closure-v3.py 改为历史只读证据绝对目录时，我错误保留了子路径开头的斜杠，Path 拼接因此丢弃父目录、改读根目录。原夹具实际存在；这是本轮测试准备错误。**按用户门禁停止，没有修改后重跑，也未放宽产品规则。**

## 5. 未运行项与后续

| 项目 | 状态 |
|---|---|
| 450 归档新旧检查、全部 ELF 成员及类型 census | NOT RUN，种类数 UNKNOWN |
| 至少 10 个真实 debug ThinLTO 库新旧转换和字节对照 | NOT RUN |
| .rela.debug_* 条数/类型 census、新检查零拒绝证明 | UNKNOWN，未执行 |
| 12 组完整展开、5 项 RPM 解析 | NOT RUN，仅测试输入准备完成 |
| 全部提交说明 72 列 / trailer 检查 | NOT RUN |
| r6 导出与校验 | NOT RUN，没有生成已认证评审包 |
| Gerrit 查询、sandbox 推送前后 ls-remote 与推送 | NOT RUN |

上一轮记录的 sandbox 为 60fabc723f30c5cc04146a9dd83487ebed63f259，本轮未读取远端，也未推送。没有完整构建、QB 操作、sudo 或 VS Code 修改。后续须先修正测试副本的路径准备，再从头重跑全部测试，不能沿用部分 PASS。

下一次 QB 的预定源码包白名单：llvm.spec、clang-bolt-helper.py、llvm-static-archives-native.py、VCS 行；0008 必须不变。这只是后续计划，本轮尚不能进入该验证阶段。

FIFTH_REVIEW 已结束 2026-11-11T14:42:18+08:00 status=stopped reason=test_fixture_import_error


## 6. 续跑（2026-11-11）：路径已修正，另一项输入遗漏后停止

本节是用户授权后的新一轮，第 1–5 节与第一次停止原文不改。源码 HEAD 为 ae4487251aaa00c2ec4edf033cf8c9046d0d4b98，tree 为 bea0348f632ba68d995af66c53fe13b978852009，工作树干净；三个提交与 §2 一致。**本轮未修改源码或提交说明，没有推送 sandbox。**

### 6.1 测试路径准备

将旧的字符串前缀替换改为捕获 results 后的相对子路径，再对它调用 lstrip('/') 后拼接。上一轮的测试副本和失败日志完整保留；新副本放在 tools/bolt/results/fifth-review-20261111/resume/，scratch 放在 W/temp/fifth-review-20261111/resume/。

修正前后原文（[prepare-paths.diff](../../tools/bolt/results/fifth-review-20261111/resume/prepare-paths.diff)）：

~~~diff
--- prepare-paths-before.py
+++ prepare-paths-after.py
@@ -1,3 +1,5 @@
 from pathlib import Path
+import re
 def rewrite(text, root):
-    return text.replace("Path(__file__).parent/'results", "Path("+repr(str(root))+")/'")
+    return re.sub(r"Path\(__file__\)\.parent/'results([^']*)'",
+                  lambda m: "Path("+repr(str(root))+")/"+repr(m.group(1).lstrip('/')), text)
~~~

[路径审计](../../tools/bolt/results/fifth-review-20261111/resume/path-audit.json)：相对上一轮已准备副本，只有 3 份 helper 文件的路径发生改变，非路径改动为 0；其 20 个历史/固定路径存在。其他测试脚本和旧版脚本原样复制，不改输入内容、断言或期望值。平台 post 宏展开输入重新生成，5 个可选调用仍齐全。

**该预检覆盖不完整。** 它检查了 helper 中已改写的显式路径，但没有检查参数/转换器套件通过 E/'debug-census.json' 动态取用的输入。复制脚本时遗漏该文件，导致下面的失败。这违反了本轮“全部输入先检查再运行”的要求，是我的准备遗漏，不能据 20 个路径存在宣称全量输入完整。

### 6.2 从头重跑结果

上一轮的 198 PASS 未沿用。所有命令串行置于独立 systemd 用户服务，MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、Nice=19、IOSchedulingClass=idle；没有 OOM，没有提高资源限制。测试内清理仍转存留存目录，没有删除文件。

| 套件 | 计划 | 已运行 | PASS | ERROR | 状态 |
|---|---:|---:|---:|---:|---|
| helper 全套 | 393 | 393 | 393 | 0 | PASS |
| 参数/转换器 | 46 | 27 | 26 | 1 | 输入缺失，failfast 停止 |
| 50 号 release | 5 | 0 | 0 | 0 | NOT RUN |
| 第二轮新增 | 12 | 0 | 0 | 0 | NOT RUN |
| cli 异常取消 | 2 | 0 | 0 | 0 | NOT RUN |
| R3/R4/R5 | 41 | 0 | 0 | 0 | NOT RUN |
| 合计 | 499 | 420 | 419 | 1 | 其余 79 项 NOT RUN |

[helper 全文](../../tools/bolt/results/fifth-review-20261111/resume/helper-tests.log)：

~~~text
Ran 393 tests in 26.630s
OK
已结束 2026-11-11T14:48:30+08:00 status=0 unit=llvm-review78-resume-1111-003
~~~

[参数/转换器全文](../../tools/bolt/results/fifth-review-20261111/resume/policy-tests.log)、[错误原文](../../tools/bolt/results/fifth-review-20261111/resume/failure.txt)：

~~~text
ERROR: test_debug_yes (__main__.Converter.test_debug_yes)
  File ".../resume/test_regressions.py", line 116, in real_command
    census=json.loads((E/'debug-census.json').read_text())
FileNotFoundError: [Errno 2] No such file or directory:
'/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/fifth-review-20261111/resume/debug-census.json'

Ran 27 tests in 17.632s
FAILED (errors=1)
已结束 2026-11-11T14:48:56+08:00 status=1 unit=llvm-review78-resume-1111-004
~~~

该错误发生在读取真实 recorded command 之前，未进入这个用例的转换器判定；不能归因为转换器拒绝。历史的 75 号 debug-census.json 和它指向的实际证据文件存在，记录见 [missing-input-diagnosis.json](../../tools/bolt/results/fifth-review-20261111/resume/missing-input-diagnosis.json)。停止后只读定位，没有补文件重跑，没有修改判定。

### 6.3 未运行项、推送与后续

- 450 归档新旧复扫及类型 census：NOT RUN；类型种类数、未知类型有无均 UNKNOWN。
- 至少 10 个 debug ThinLTO 库新旧转换、输出字节对照和 .rela.debug_* 条目/类型 census：NOT RUN。
- 第三步完整 12 组展开、5 项解析、全部提交说明检查：NOT RUN。测试准备只生成了 T debug-on 的展开输入，不能替代全量结果。
- r6 评审包、SHA256SUMS、Gerrit change 查询、sandbox 推送前后 ls-remote 与推送：NOT RUN。
- 本轮没有 sandbox 前后 SHA 的新观测；上一轮记录的远端仍为 60fabc72，本轮未访问 Gerrit，未执行推送。
- 不运行完整构建、不操作 QB、不执行 sudo、不修改 VS Code；历史构建根只读。

下一次 QB 源码包白名单保持：llvm.spec、clang-bolt-helper.py、llvm-static-archives-native.py、VCS 行；0008 必须不变。本轮测试门禁未通过，不能进入推送阶段。后续需要完整盘点测试套件的所有只读依赖，再从头运行，不沿用本轮部分 PASS。

FIFTH_REVIEW_RESUME 已结束 2026-11-11T14:50:27+08:00 status=stopped reason=missing_test_input_debug_census


## 7. 第二次续跑（2026-11-11）：产品取消路径 FAIL，停止

本节保留前两次停止的全部原文。**本次准备问题修正次数为 0；计划 499 项，实际运行 475 项，474 PASS、1 FAIL，余下 24 项未运行。** 失败属于产品实现错误，不能按用户允许的“准备问题最多修正两次”处理。没有修改源码或提交说明，没有修改预期或重试，没有推送 sandbox。

### 7.1 起点与测试环境

源码起点及结束时均为 ae4487251aaa00c2ec4edf033cf8c9046d0d4b98，tree bea0348f632ba68d995af66c53fe13b978852009，工作树干净；三个提交仍与 §2 完全一致。[身份记录](../../tools/bolt/results/fifth-review-20261111/rerun2/source-identity.json)。

按用户的新做法，完整复制 75 号 §6.2 的环境目录 tools/bolt/results/fourth-review-20261110/resume（282 个文件，8,102,162 B），到 W/temp/fifth-review-20261111/rerun2/environment。逐文件核对复制前后 SHA；旧环境及历史根只读。保留原输入目录所指向的历史证据；本轮输出、scratch 单独落到 rerun2。复制的历史结果只是环境留存，不计入本次 PASS。

[环境复制清单](../../tools/bolt/results/fifth-review-20261111/rerun2/environment-copy.json)、[完整调用环境](../../tools/bolt/results/fifth-review-20261111/rerun2/test-invocation.json)、[套件驱动](../../tools/bolt/results/fifth-review-20261111/rerun2/run_suite.py)。PATH、host-tools/cmake 版本和 SHA 与 75 号相同。被测文件显式指向当前源码目录的 llvm.spec、clang-bolt-helper.py 和 llvm-static-archives-native.py，未以旧副本代替产品。

加入的是第五轮已准备的新增用例；继承原先已经授权的 BOLT_CANCELLED 输出预期、PC32 宽度 (2,4) 及 R5 用例，未再调整测试数据或断言。补入完整环境本来具有的 debug-census.json，而不是生成新的输入。原输入指向的真实 recorded command 存在且 SHA 与记录相同。

### 7.2 输入预检

[预检 JSON](../../tools/bolt/results/fifth-review-20261111/rerun2/input-preflight.json)记录 361 个现有依赖，[读取表达式清单](../../tools/bolt/results/fifth-review-20261111/rerun2/read-expression-inventory.json)记录 187 处读取调用。检查范围包括：

- 所复制的完整环境、测试模块、三份当前产品、历史 helper 和转换器；
- helper 的 Path/results 组合、动态生成名字的 review4-macro 压缩展开、JSON 图与历史日志；所有压缩夹具已实际解压读取；
- debug-census.json 及其选中成员的 ir-settings.json，核对 SHA；
- Base-Dev 真实 release 成员来源 summary.json、选中的 ThinLTO 库、平台 clang/llvm-dis/llvm-nm/llvm-as、loader 和库目录；
- 环境变量 PATH 所用目录、TEST_SCRATCH 新根、Python、sh/dash/bash、prlimit 和 CMake；
- glob / proc / 临时文件读取分别记录：临时输入由未改动的 setUp/fixture 写入后读取，不能要求它们在 fixture 尚未生成前已经存在；/proc 进程状态在执行期间检查。

显式平台 post 宏重新展开，5 个可选调用齐全，[输入 SHA 与调用行](../../tools/bolt/results/fifth-review-20261111/rerun2/post-input.json)。本轮没有输入缺失、路径错误或 import 失败，故“准备问题修正后从头重跑”的次数为 **0/2**。之前两轮错误记录仍保留在 §4、§6，不算本轮的两次额度。

### 7.3 全部从头运行的实际结果

所有命令串行位于独立 systemd 用户服务，MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、Nice=19、IOSchedulingClass=idle。无 OOM、无提高上限。测试临时文件保留，原清理操作由既有留存运行器转存，没有删除文件。

| 套件 | 计划 | 已运行 | PASS | FAIL | 未运行 |
|---|---:|---:|---:|---:|---:|
| helper | 393 | 393 | 393 | 0 | 0 |
| policy | 46 | 46 | 46 | 0 | 0 |
| release | 5 | 5 | 5 | 0 | 0 |
| r2 | 12 | 12 | 12 | 0 | 0 |
| cli | 2 | 2 | 2 | 0 | 0 |
| r3-r4-r5 | 41 | 17 | 16 | 1 | 24 |
| 合计 | 499 | 475 | 474 | 1 | 24 |

[汇总 JSON](../../tools/bolt/results/fifth-review-20261111/rerun2/test-summary.json)。六份完整日志：
[helper](../../tools/bolt/results/fifth-review-20261111/rerun2/helper-tests.log)、
[参数/转换器](../../tools/bolt/results/fifth-review-20261111/rerun2/policy-tests.log)、
[release](../../tools/bolt/results/fifth-review-20261111/rerun2/release-tests.log)、
[R2](../../tools/bolt/results/fifth-review-20261111/rerun2/r2-tests.log)、
[cli](../../tools/bolt/results/fifth-review-20261111/rerun2/cli-tests.log)、
[R3/R4/R5](../../tools/bolt/results/fifth-review-20261111/rerun2/r3-r4-r5-tests.log)。

前五套全部通过。最后一套完成 14 个 R3、R4 的前 2 个方法，在第 17 个方法 test_cli_mid_conversion_signals 触发 FAIL；后续 R4 和全部 R5 未运行。subTest 不单独累计到 499。

### 7.4 产品 FAIL 的原文与原因

[完整 failure.txt](../../tools/bolt/results/fifth-review-20261111/rerun2/failure.txt)：

~~~text
FAIL: test_cli_mid_conversion_signals (__main__.R4.test_cli_mid_conversion_signals)
AssertionError: 1 != 143
RuntimeError: cancelled before process launch

During handling of the above exception, another exception occurred:

File ".../packaging/llvm-static-archives-native.py", line 1020, in install_main
    failure = sys.exc_info()
              ^^^
NameError: name 'sys' is not defined. Did you forget to import 'sys'?

Ran 17 tests in 18.700s
FAILED (failures=1)
已结束 2026-11-11T15:01:23+08:00 status=1 unit=llvm-review78-rerun2-1111-010
~~~

该用例使用真实 release bitcode 成员，在 disassemble 命令阶段发送真实 SIGTERM。产品先捕获了取消引起的 RuntimeError，但 install_main 新增的异常保存语句使用 sys.exc_info()，文件头却没有 import sys。因此它再次抛出 NameError，未走到最终的 128+SIGTERM=143，进程实际返回 1。

这是本轮第五轮代码实现的遗漏，不是 fixture 准备问题，也不是需要放宽断言的情况。按用户规则立即停止；没有补 import、没有 amend、没有重试。正常完成后取消的先前用例通过，不代表异常取消路径通过。

### 7.5 未运行检查与推送边界

- QB 1225393/1225395 的 450 归档实物新旧复扫、ELF 成员重定位 census：NOT RUN，类型种类数及表外类型有无为 UNKNOWN。
- 至少 10 个真实 debug ThinLTO 库的新旧转换、字节对照、.rela.debug_* 条数和类型 census：NOT RUN。单成员取消夹具不能替代该项。
- 完整 12 组 spec 展开、5 项 RPM 解析：NOT RUN；仅测试准备所需的首个 T debug-on 与 post 展开执行。
- 第三步独立提交说明检查：NOT RUN；既有 R3 的 test_messages 在本次测试中通过，但不冒充后续整项已执行。
- r6 包、SHA256SUMS、sandbox 推送前后 ls-remote、359934/357163 查询及推送：NOT RUN。
- 本次没有远端 SHA 新观测；上次记录的 sandbox 为 60fabc723f30c5cc04146a9dd83487ebed63f259，未声称本次已复查。
- 源码及说明保持原样，未运行完整构建、未操作 QB、未执行 sudo、未修改 VS Code 配置。

下一次 QB 源码包白名单仍为 llvm.spec、clang-bolt-helper.py、llvm-static-archives-native.py、VCS 行；0008 必须不变。当前产品门禁未通过，不能进入推送。

FIFTH_REVIEW_RERUN2 已结束 2026-11-11T15:03:47+08:00 status=stopped reason=converter_missing_sys_import


## 8. 第三次续跑（2026-11-11）：import sys 已修正，实物复核驱动断言停止

本节保留前三次停止记录原文。**499/499 项单元与回归测试全部通过；450 个 QB 归档的新旧复扫通过。** 随后的10个debug ThinLTO归档对照在第一个归档上停止：两版输出SHA相同，但我新增的复核驱动误把输出路径字段也纳入相等断言。这是复核驱动的错误，不是转换器新增拒绝。按“任何FAIL停止”的要求，没有修改断言后重跑，没有继续其余归档或推送sandbox。

### 8.1 唯一产品修正与源码身份

在转换器import列表增加import sys，用fixup/autosquash归入第三提交；Change-Id和提交说明不变。[唯一diff](../../tools/bolt/results/fifth-review-20261111/rerun3/import-sys.diff)、[三个提交全文](../../tools/bolt/results/fifth-review-20261111/rerun3/commits.json)。新HEAD相对ae448725仅这一行，工作树干净；前两个提交SHA/tree完全不变。

| 标题 | SHA | tree |
|---|---|---|
| cmake: use hybrid LLVM linkage on x86_64 | 8a50d7122346258fd1171d270861a4ae28a8717c | 3d961cbb04f5446f84d2089b4f65f3178f2bd7fa |
| packaging: optimize x86_64 clang with BOLT | 1e415935a83a187aab7c41f9713115a0974a0365 | c23914776684bf94fdd5961f447f7c24e7bb79bc |
| packaging: fix x86 LLVM flags and archive mode | fea0fe464d56e17f2c7588c557bfffd9f6ac352b | b2e8af2477cf623a945aa80bf8288a262dd4a5a9 |

[pyflakes记录](../../tools/bolt/results/fifth-review-20261111/rerun3/pyflakes.json)：系统没有pyflakes可执行文件或Python模块，按要求记 **NOT RUN**，没有联网安装；不能据此宣称未定义名字为0。上一轮漏import导致的取消错误由本轮实际测试覆盖。

### 8.2 测试环境与499项全量结果

沿用上次已通过输入预检、源自75号§6.2的环境，复制到W/temp/fifth-review-20261111/rerun3/environment。测试脚本、数据及断言不改；被测三个文件显式指向当前源码，转换器是修正后的版本。[环境来源](../../tools/bolt/results/fifth-review-20261111/rerun3/environment-provenance.json)、[361个依赖的预检](../../tools/bolt/results/fifth-review-20261111/rerun3/input-preflight.json)、[调用环境](../../tools/bolt/results/fifth-review-20261111/rerun3/test-invocation.json)。本轮测试准备问题修正次数 **0/2**；没有沿用之前的部分PASS。

| 套件 | 本次从头运行 | PASS |
|---|---:|---:|
| helper | 393 | 393 |
| 参数/转换器policy | 46 | 46 |
| release | 5 | 5 |
| R2 | 12 | 12 |
| cli | 2 | 2 |
| R3/R4/R5 | 41 | 41 |
| 合计 | 499 | 499 |

[汇总](../../tools/bolt/results/fifth-review-20261111/rerun3/test-summary.json)；完整日志：
[helper](../../tools/bolt/results/fifth-review-20261111/rerun3/helper-tests.log)、[policy](../../tools/bolt/results/fifth-review-20261111/rerun3/policy-tests.log)、
[release](../../tools/bolt/results/fifth-review-20261111/rerun3/release-tests.log)、[R2](../../tools/bolt/results/fifth-review-20261111/rerun3/r2-tests.log)、
[cli](../../tools/bolt/results/fifth-review-20261111/rerun3/cli-tests.log)、[R3/R4/R5](../../tools/bolt/results/fifth-review-20261111/rerun3/r3-r4-r5-tests.log)。

上次FAIL的test_cli_mid_conversion_signals本次 **PASS**；41项末套全文以Ran 41 tests / OK结束，包含这次此前未运行的全部新增测试。subTest不单独累计。

所有执行串行在独立systemd用户服务内，MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、Nice=19、IOSchedulingClass=idle；无OOM、无提高上限。测试和转换清理操作由既有留存运行器转存到本轮scratch，未删除文件。完整构建、QB、sudo均未执行。

499项结束后的一个只读代码查看探针，直接导入本地validate.py时因缺少其同目录import路径报ModuleNotFoundError: No module named 'checks'；随后仅用AST读取loader函数原文。该探针没有运行测试或转换，不计为测试准备修正，没有改任何测试输入或断言。[原文记录](../../tools/bolt/results/fifth-review-20261111/rerun3/inspection-import-error.txt)。

### 8.3 QB 450个归档复扫及第一组census

使用73/77号已经下载的QB1225393/1225395 llvm-static-devel RPM，解包到本轮新目录，不改历史根。每个完整归档SHA、大小核对77号manifest；每个ELF成员重新对照旧版60fabc72与当前版本的elf_details、pic_relocations，不能只以完整归档相同替代本轮检查。

[驱动](../../tools/bolt/results/fifth-review-20261111/rerun3/check_qb_archives.py)、[汇总](../../tools/bolt/results/fifth-review-20261111/rerun3/qb-archive-summary.json)、
[7728行成员原文](../../tools/bolt/results/fifth-review-20261111/rerun3/qb-archive-members.jsonl.gz)、[进度原文](../../tools/bolt/results/fifth-review-20261111/rerun3/qb-archive-check.stdout)、
[Toolchain RPM来源](../../tools/bolt/results/fifth-review-20261111/rerun3/toolchain-rpm-source.json)、[Base-Dev RPM来源](../../tools/bolt/results/fifth-review-20261111/rerun3/basedev-rpm-source.json)。

| 项目 | 归档 | ELF成员 | 转换 / 原生 | ALLOC目标受检重定位（新旧各） | census类型数 | .rela.debug_*条目 | 新拒绝 / 表外类型 |
|---|---:|---:|---:|---:|---:|---:|---|
| Toolchain 1225393 | 225 | 3864 | 3853 / 11 | 3763631 | 11 | 94400431 | 0 / 0 |
| Base-Dev 1225395 | 225 | 3864 | 3853 / 11 | 3763631 | 9 | 0 | 0 / 0 |
| 合计 | 450 | 7728 | 7706 / 22 | 7527262 | 11（并集） | 94400431 | 0 / 0 |

两个项目的新旧elf_details和pic_relocations全部一致，转换成员零拒绝；本次原生成员的禁止项也均为0。所有REL/RELA section的独立census共 **101927693** 条，区别于旧API只累计ALLOC目标的checked字段。调试节出现类型1、10、17，没有表外类型。

| 类型编号 | Toolchain全部 | Base-Dev全部 | Toolchain .rela.debug_* |
|---|---:|---:|---:|
| 1 | 27841359 | 413317 | 27428042 |
| 2 | 1331499 | 1331499 | 0 |
| 4 | 1915123 | 1915123 | 0 |
| 9 | 59 | 59 | 0 |
| 10 | 66972360 | 0 | 66972360 |
| 17 | 29 | 0 | 29 |
| 19 | 2145 | 2145 | 0 |
| 20 | 51 | 51 | 0 |
| 21 | 94 | 94 | 0 |
| 41 | 33 | 33 | 0 |
| 42 | 101310 | 101310 | 0 |

结束原文：

~~~text
已结束 2026-11-11T15:24:13+08:00 status=0 unit=llvm-review78-rerun3-1111-011
~~~

### 8.4 第二组debug ThinLTO实物验证：驱动断言失败，停止

从63号Toolchain构建树只读复制按大小排序的前10个归档，包含最大的libclangSema.a、libLLVMCodeGen.a、libclangCodeGen.a；原始/副本SHA逐个一致。[完整输入清单](../../tools/bolt/results/fifth-review-20261111/rerun3/debug-inputs.json)。没有在历史根内运行cmake/ninja/gbs。

采用75号§6.4同样的loader包装方式调用平台clang-22、llvm-dis、llvm-nm；三个版本均22.1.8，包装器同目录，完整argv和工具SHA在[单归档结果](../../tools/bolt/results/fifth-review-20261111/rerun3/debug-conversion-00.json)。新旧转换器同一工具、同一输入、debug_info=yes、jobs=1、进程地址空间上限4GiB，外层服务8GiB。

第一个libclangSema.a的两个实际转换都成功：输入348403542 B，86个bitcode成员；两边均converted=86、preserved=0、debug_members=86，输出401030038 B。**两边完整归档SHA都为8de79182e21d90c6351536f717b15ba0174cad1dc1a7798d630a16e1a082f3de。** 这一个归档的字节相同事实已成立，但不能代替10归档完整门禁通过。

随后我编写的[复核脚本](../../tools/bolt/results/fifth-review-20261111/rerun3/convert_debug_archive.py)第47行误用：

~~~python
a=new.inspect(outputs['old']);b=new.inspect(outputs['new']);assert a==b
~~~

inspect()含来源path，两次转换的输出目录本来不同。停止后的[只读定位](../../tools/bolt/results/fifth-review-20261111/rerun3/debug-conversion-failure-diagnosis.json)确认唯一不同字段是：

~~~text
old: .../rerun3/debug-conversion-00/old/archives/libclangSema.a
new: .../rerun3/debug-conversion-00/new/archives/libclangSema.a
~~~

该断言错误属于我的复核驱动，不是产品失败；它已进入实际结果判定，不能使用仅允许输入/路径/import准备ERROR修正的例外。没有修改测试预期或比较逻辑后重跑。[完整原文](../../tools/bolt/results/fifth-review-20261111/rerun3/debug-conversion-00.stdout)：

~~~text
a=new.inspect(outputs['old']);b=new.inspect(outputs['new']);assert a==b
AssertionError
DEBUG_CONVERSION 已结束 2026-11-11T15:33:39.766883+08:00 archive=libclangSema.a status=failed
已结束 2026-11-11T15:33:39+08:00 status=1 unit=llvm-review78-rerun3-1111-016
~~~

其余9个归档未转换；第二组独立.rela.debug_* census未执行，类型数、条数、表外类型有无均 **UNKNOWN**，不能借用§8.3的发货归档数据。两份输出及全部中间文件保留。

### 8.5 未运行项、推送及下一轮白名单

- 第三步完整12组spec展开、5项Tizen RPM解析：**NOT RUN**。499项测试所需的既有展开输入不能替代此整项重跑。
- 第三步独立提交说明72列/trailer检查：**NOT RUN**。回归套件里的提交说明测试已PASS，但不冒充独立检查。
- r6评审包、SHA256SUMS及其校验：**NOT RUN**，未生成未认证的评审包。
- sandbox推送前/后ls-remote、359934/357163查询、sandbox推送：**NOT RUN**。本轮没有远端SHA新观测；历史记录为60fabc723f30c5cc04146a9dd83487ebed63f259，不能声称本轮已复查。
- 没有运行完整构建，不操作QB，不执行sudo；历史输入只读，不删除文件，不改VS Code配置。
- 后续下一次QB源码包白名单仍为：llvm.spec、clang-bolt-helper.py、llvm-static-archives-native.py、VCS行；**0008必须不变**。
- 当前停点是复核驱动的路径字段断言；尚未满足进入评审包和sandbox推送的条件。

FIFTH_REVIEW_RERUN3 已结束 2026-11-11T15:39:20+08:00 status=stopped reason=verification_driver_compared_output_path


## 9. 第四次续跑（2026-11-11）：剩余验证通过，Gerrit状态变化停止推送

**10/10个debug ThinLTO归档新旧输出逐字节相同，12组展开、5项RPM解析及提交说明检查通过。** 推送前实时查询发现359934和357163已为MERGED，不满足用户指定的“仍为NEW”。因此未推送sandbox，未进入依赖推送后身份核对的完整构建入口准备与演练。原有四次停止记录全部保留，不以本节覆盖历史结果。

### 9.1 起点与核对脚本修正（1次）

源码HEAD仍为fea0fe464d56e17f2c7588c557bfffd9f6ac352b、tree b2e8af2477cf623a945aa80bf8288a262dd4a5a9，工作树干净。三个提交、提交说明及产品测试均未修改。[身份记录](../../tools/bolt/results/fifth-review-20261111/rerun4/source-identity.json)。

用户本次明确批准修正执行方核对脚本中按设计本来不同的字段；据此在新副本里仅从inspect()字典比较中排除来源path。**没有排除SHA、大小、成员、节、重定位结果或计数，也没有加入时间戳等其他例外。** [原始错误](../../tools/bolt/results/fifth-review-20261111/rerun4/previous-error.txt)、[单行修正diff](../../tools/bolt/results/fifth-review-20261111/rerun4/inspect-path-fix.diff)、[完整驱动](../../tools/bolt/results/fifth-review-20261111/rerun4/convert_debug_archive.py)。

~~~diff
- a=new.inspect(outputs['old']);b=new.inspect(outputs['new']);assert a==b
+ a=new.inspect(outputs['old']);b=new.inspect(outputs['new']);assert {k:v for k,v in a.items() if k!='path'}=={k:v for k,v in b.items() if k!='path'}
~~~

本轮允许修正额度使用 **1/2**，仅此一项；无产品FAIL、无测试数据或产品断言调整。libclangSema.a复用上次两份输出，通过[复核驱动](../../tools/bolt/results/fifth-review-20261111/rerun4/recheck_sema.py)重新计算SHA/大小，再执行相同的修正后比较和全成员检查。其余9个归档在新scratch中重新执行两版转换；历史根只读。

### 9.2 第二组实物验证和census

[输入来源/SHA](../../tools/bolt/results/fifth-review-20261111/rerun4/debug-inputs.json)、[完整汇总](../../tools/bolt/results/fifth-review-20261111/rerun4/debug-conversion-summary.json)。两版均debug_info=yes、jobs=1、进程地址空间4GiB，外层systemd用户服务MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、Nice=19、IOSchedulingClass=idle，所有服务串行。沿用75号loader调用方式，三个平台工具版本均22.1.8，来源SHA、argv和每次日志在debug-conversion-00至09的JSON及stdout中。无OOM、没有提高限制或重试；全部现场保留，没有删除文件。

|归档|成员|.rela.debug_*条目|两版相同的完整归档SHA256|
|---|---:|---:|---|
|libclangSema.a|86|5856488|8de79182e21d90c6351536f717b15ba0174cad1dc1a7798d630a16e1a082f3de|
|libclangTidyBugproneModule.a|105|3929302|4366135f08a01ec4d2133b5855deb994fa48c07b117615ef1e37321551719502|
|libLLVMCodeGen.a|238|4487133|e4894007eb23bba03b3d740606686ead1e3f48bde70fb796d22b39ccf240728c|
|libclangAST.a|114|4558219|4a05dc4113744f073479aa66e7c456f7c62faa5968167f091917b951ca3ee7dc|
|libclangCodeGen.a|101|3758699|d5183b82586383972b51157f129b276990667665abb788e47be21c4f3cbf35cd|
|libclangStaticAnalyzerCheckers.a|134|2845518|d2f9b766793549d6a6cde3cbad5a1ca6eaa00645ec73586605364243acf96d57|
|libclangDaemon.a|82|2953475|776525de05d2e5f7a74e18f3d6adc9ea1145d2fa21ed980d659e88a2aa162db3|
|libclangTidyModernizeModule.a|50|2490869|5df6d3df4a746e56591c96213b22c4f10bc50bdae60b1cfd8bd86a5302695f5a|
|libclangTidyReadabilityModule.a|59|2304671|c0849682a8884ce19ea2cc3a66ed21ce349bee1c8cc6da2d968d380811bd3401|
|libLLVMAnalysis.a|131|2376173|5f1993917095d04b80c2c51c794bae5a52ede9127ca5d572648dca99cdd404b6|

共 **1100个成员（1093转换、7原生）**，10/10完整归档大小/SHA一致，其余inspect字段一致，所有成员的elf_details和pic_relocations新旧一致；转换成员零拒绝。原生成员仍按原规则保留、比较旧新结果，不扩张其拦截规则。源输入是63号构建树按体积排序最大的10个ThinLTO库，包含libclangSema、libLLVMCodeGen、libclangCodeGen。

全部重定位共 **37005060** 条，7种类型；调试节共 **35560547** 条，2种类型（1、10）。表外类型为0。

|类型编号|全部重定位|.rela.debug_*|
|---|---:|---:|
|1|10640217|10486437|
|2|479877|0|
|4|780135|0|
|10|25074110|25074110|
|19|956|0|
|41|11|0|
|42|29754|0|

本项末尾原文：

~~~text
DEBUG_CONVERSION 已结束 2026-11-11T16:51:49.280209+08:00 archive=libLLVMAnalysis.a status=ok
ITEM1 已结束 2026-11-11T16:52:29.482766+08:00 status=ok
~~~

§8同一源码HEAD的499/499产品测试、450个QB归档复扫继续有效，本任务没有再次重复它们。第一组发货归档census为11种类型、94400431条调试节重定位，第二组是本节重新转换数据，不混用两组数字。pyflakes仍是上次“未安装、NOT RUN”，未联网安装。

### 9.3 展开、RPM解析和提交说明

[展开驱动](../../tools/bolt/results/fifth-review-20261111/rerun4/parse_checks.py)、[12组结果](../../tools/bolt/results/fifth-review-20261111/rerun4/parse/expansion-summary.json)、[5项解析结果](../../tools/bolt/results/fifth-review-20261111/rerun4/parse/five-summary.json)，逐次argv、stdout、stderr和完整diff均保存在parse/。

- 两配置分别覆盖x86 debug/release的BOLT开/关与ARM两架构，合计12组。
- ARM及BOLT关闭的8组与60fabc72逐字节相同。
- x86 BOLT开启的4组只允许两处disk-diagnose从“|| true”变为“|| bolt_status_exit $?”；逐处反向替换后与60fabc72全同，无其他差异。
- TizenRPM五项：x86开启、关闭、一行回退、armv7l、aarch64全部PASS；仅解析，没有构建。
- [独立说明检查](../../tools/bolt/results/fifth-review-20261111/rerun4/message-check.json)：三个说明最大行宽均72，最后一段只含可解析的Change-Id与Signed-off-by；混合链接SHA/tree仍8a50d7122346258fd1171d270861a4ae28a8717c / 3d961cbb04f5446f84d2089b4f65f3178f2bd7fa。

~~~text
EXPANSIONS_PASS 12 FIVE_PARSE_PASS 5
ITEM2 已结束 2026-11-11T16:52:56.152298+08:00 status=ok
~~~

### 9.4 r6材料及推送前停止

[r6评审包](../../patches/rebase-359934-20261111-r6/README.md)已生成：三个带PATCH 1/3–3/3编号的完整补丁、BOLT文本补丁、九份最终全文、对60fabc72完整diff、转换器对PS10 diff、provenance、README及SHA256SUMS；[最终17行校验全部OK](../../tools/bolt/results/fifth-review-20261111/rerun4/r6-sha256-final-check.txt)。README明确记录上轮测试抓到并修正的import sys，以及本轮核对脚本的路径修正。本包是已完成指定轻量/实物门禁的代码材料，不宣称完整构建或新QB已认证。

SSH一律BatchMode、使用完整URL。推送前ls-remote原文（[stdout](../../tools/bolt/results/fifth-review-20261111/rerun4/sandbox-before.stdout)、[命令](../../tools/bolt/results/fifth-review-20261111/rerun4/sandbox-before.command.json)）：

~~~text
60fabc723f30c5cc04146a9dd83487ebed63f259 refs/heads/sandbox/lhmax2025/bolt_pgo
~~~

实际输出在SHA与ref之间为TAB，以上为排版显示。随后查询359934即发现状态不符，未执行任何push；再仅补齐357163的已授权只读查询，未重试或更改推送方式。

|Change|实际状态|当前PS|revision|lastUpdated（+08:00）|
|---|---|---:|---|---|
|359934|MERGED|10|13c3e223d9e1b35e4affb55255c5042f8c940f35|2026-11-11T12:28:07+08:00|
|357163|MERGED|2|cf4b6777d056131e2534ecb460c5575327d99646|2026-11-11T12:28:07+08:00|

[359934完整原文](../../tools/bolt/results/fifth-review-20261111/rerun4/change-359934.stdout)、[357163完整原文](../../tools/bolt/results/fifth-review-20261111/rerun4/change-357163.stdout)、[前置判定](../../tools/bolt/results/fifth-review-20261111/rerun4/push-preflight.json)。revision虽未变，状态已经不满足本任务要求，不能自行豁免。**推送未执行，推后ls-remote NOT RUN；无推后SHA新观测。** 本地HEAD保持fea0fe46，最后一次实际读到的sandbox为60fabc72。

~~~text
ITEM3 已结束 2026-11-11T16:55:38.190457+08:00 status=stopped reason=change_status_not_NEW
~~~

### 9.5 未运行检查及后续边界

第四步要求源码副本核对时远端sandbox也为fea0fe46；该前置条件当前不成立，故没有创建新clone、新入口或夜间根。入口diff、自测、T/D演练、FLAGS/log-restarts/资源/残留审计和晚间磁盘预算均NOT RUN。[入口未运行记录](../../tools/bolt/results/fifth-review-20261111/rerun4/entry-not-run.json)，另见[74号追加节](74_local_full_build_fa4f9978.md)。不提供已可启动的晚间命令。

没有运行完整构建、操作QB、执行sudo、推refs/for、删除文件或修改VS Code配置。下一次QB源码包白名单仍为：llvm.spec、clang-bolt-helper.py、llvm-static-archives-native.py、VCS行；**0008必须不变**。待用户裁决MERGED状态是否满足推送前置条件后，才能继续sandbox和第四步入口准备。

FIFTH_REVIEW_RERUN4 已结束 2026-11-11T16:58:21+08:00 status=stopped reason=Gerrit_changes_MERGED_required_NEW


## 10. 第五次续跑（2026-11-11）：总部合入判定B，sandbox推送完成

按用户新的前提重新核对；前三个源码提交、说明、产品测试及r6材料均未修改。源码HEAD fea0fe464d56e17f2c7588c557bfffd9f6ac352b、tree b2e8af2477cf623a945aa80bf8288a262dd4a5a9，工作树干净。[身份](../../tools/bolt/results/fifth-review-20261111/rerun5/source-identity.json)、[r6的17项SHA校验全OK](../../tools/bolt/results/fifth-review-20261111/rerun5/r6-sha256-check.txt)。本轮准备/核对脚本修正次数0。

### 10.1 两个change的合入记录

[359934完整query](../../tools/bolt/results/fifth-review-20261111/rerun5/change-359934.stdout)、[357163完整query](../../tools/bolt/results/fifth-review-20261111/rerun5/change-357163.stdout)、[提取记录](../../tools/bolt/results/fifth-review-20261111/rerun5/merged-changes.json)。均使用SSH BatchMode，完整URL及实际argv另存于同目录command.json。

|Change|状态|PS|revision|SUBM记录、时间与提交者|
|---|---|---:|---|---|
|359934|MERGED|10|13c3e223d9e1b35e4affb55255c5042f8c940f35|SUBM +1；2026-11-11T12:28:07+08:00；Dongkyun Son / dkson95 / dongkyun.s@samsung.com|
|357163|MERGED|2|cf4b6777d056131e2534ecb460c5575327d99646|SUBM +1；2026-11-11T12:28:07+08:00；Dongkyun Son / dkson95 / dongkyun.s@samsung.com|

两份comments在该时刻均有原文“Change has been successfully merged”，与SUBM时间一致；不再把MERGED当成失败条件。

### 10.2 tizen_base判定及最新快照

**判定B**：远端tizen_base HEAD为 **61ef5d31ca91025c414c748477bef0c64ddfa67c**，13c3e223是其祖先；13c3e223之后仅1个合并提交，tree与13c3e223相同；完整diff及diff --stat均为空。因此不需要改接源码，本任务继续使用既有三提交链。

[ls-remote原文](../../tools/bolt/results/fifth-review-20261111/rerun5/tizen-base-remote.stdout)、[fetch原文](../../tools/bolt/results/fifth-review-20261111/rerun5/fetch-tizen-base.stderr)、[祖先检查](../../tools/bolt/results/fifth-review-20261111/rerun5/tizen-base-ancestor.command.json)、[父链](../../tools/bolt/results/fifth-review-20261111/rerun5/tizen-base-parent-list.stdout)、[完整diff](../../tools/bolt/results/fifth-review-20261111/rerun5/tizen-base-diff.stdout)、[stat](../../tools/bolt/results/fifth-review-20261111/rerun5/tizen-base-diff-stat.stdout)、[判定JSON](../../tools/bolt/results/fifth-review-20261111/rerun5/tizen-base-verdict.json)。

fetch仅写FETCH_HEAD和对象，不改本地分支；[分支前](../../tools/bolt/results/fifth-review-20261111/rerun5/local-branches-before.stdout)与[分支后](../../tools/bolt/results/fifth-review-20261111/rerun5/local-branches-after.stdout)逐字一致。HEAD的完整提交信息：

~~~text
commit 61ef5d31ca91025c414c748477bef0c64ddfa67c
Merge: cf4b6777d056 13c3e223d9e1
Author:     Dongkyun Son <dongkyun.s@samsung.com>
AuthorDate: Wed Nov 11 04:28:07 2026 +0000
Commit:     Gerrit Code Review <gerrit@localhost>
CommitDate: Wed Nov 11 04:28:07 2026 +0000

    Merge "packaging: classify -feliminate-unused-debug-types and mirror recorded backend policy" into tizen_base
~~~

[公开快照目录记录](../../tools/bolt/results/fifth-review-20261111/rerun5/latest-snapshots.json)：只列目录并按实际快照名时间戳排序，最新有名目录分别是：

|项目|最新快照名|
|---|---|
|Tizen-Base-Toolchain|tizen-base-toolchain_20261109.032334|
|Tizen-Base-Dev|tizen-base-dev_20261103.083743|

这只是只读盘点，**没有改变本轮比较基线或入口固定快照**：Toolchain仍tizen-base-toolchain_20261030.061318，Base-Dev仍tizen-base-dev_20261030.061217。

### 10.3 sandbox推送原文与核验

推送前：

~~~text
60fabc723f30c5cc04146a9dd83487ebed63f259	refs/heads/sandbox/lhmax2025/bolt_pgo
~~~

唯一推送命令：

~~~sh
git push --force-with-lease=refs/heads/sandbox/lhmax2025/bolt_pgo:60fabc723f30c5cc04146a9dd83487ebed63f259 ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm fea0fe464d56e17f2c7588c557bfffd9f6ac352b:refs/heads/sandbox/lhmax2025/bolt_pgo
~~~

原始输出：

~~~text
remote: 
remote: Processing changes: refs: 1        
remote: Processing changes: refs: 1, done            
To ssh://review.tizen.org:29418/platform/upstream/llvm
 + 60fabc723f30...fea0fe464d56 fea0fe464d56e17f2c7588c557bfffd9f6ac352b -> sandbox/lhmax2025/bolt_pgo (forced update)
~~~

推后ls-remote：

~~~text
fea0fe464d56e17f2c7588c557bfffd9f6ac352b	refs/heads/sandbox/lhmax2025/bolt_pgo
~~~

[push命令/返回码](../../tools/bolt/results/fifth-review-20261111/rerun5/sandbox-push.command.json)、[结果JSON](../../tools/bolt/results/fifth-review-20261111/rerun5/sandbox-result.json)。远端等于本地HEAD，父链如下；未推refs/for、未新建分支或操作QB：

~~~text
fea0fe464d56e17f2c7588c557bfffd9f6ac352b b2e8af2477cf623a945aa80bf8288a262dd4a5a9 packaging: fix x86 LLVM flags and archive mode
1e415935a83a187aab7c41f9713115a0974a0365 c23914776684bf94fdd5961f447f7c24e7bb79bc packaging: optimize x86_64 clang with BOLT
8a50d7122346258fd1171d270861a4ae28a8717c 3d961cbb04f5446f84d2089b4f65f3178f2bd7fa cmake: use hybrid LLVM linkage on x86_64
13c3e223d9e1b35e4affb55255c5042f8c940f35 087e06cf9c79c571c711af8a07057496940ae73d packaging: classify -feliminate-unused-debug-types and mirror recorded backend policy
cf4b6777d056131e2534ecb460c5575327d99646 7b49745738b5512fbbed890e67e6a3861e1e39a5 Revert "Revert clang bootstrap + ThinLTO, fall back to GCC"
~~~

此前499项产品测试、450个QB归档复扫、10个debug ThinLTO归档逐字节对照、12展开/5解析及r6校验结果不变。本步骤没有重跑测试、启动完整构建或演练。先将本节和STATUS推送GitHub，随后才开始用户第三步的源码副本/入口准备与演练，结果另记74号。下一次QB源码包白名单仍为llvm.spec、clang-bolt-helper.py、llvm-static-archives-native.py、VCS行；0008必须不变。

ITEM1 已结束 2026-11-11T17:15:51.383169+08:00 status=ok verdict=B

ITEM2 已结束 2026-11-11T17:16:44.572932+08:00 status=ok reason=sandbox_push_verified

R6_SANDBOX 已结束 2026-11-11T17:17:44+08:00 status=ok
