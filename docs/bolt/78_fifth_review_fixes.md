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
