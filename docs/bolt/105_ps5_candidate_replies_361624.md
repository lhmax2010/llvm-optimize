# 105：PS5 候选、导出核对与停止记录

> 105号续最新状态：PM E1/E2 裁决后，R3(b) 的7项已全部通过。R3(c) 因本次补丁应用准备脚本错误停止，未推 sandbox；详见文末“6. 105号续”。下文原始 STOP 保留。

结论：**STOP，未推 sandbox，未做任何 Gerrit 写操作。** R1 通过，N1 两处修正完成，全部 567/567 测试通过。R3(b) 全量比较发现 7 个 native tarball 文件与候选 Git blob 内容不同；其余 169,022 个相同。没有自行豁免 export-subst 或换行差异。R3(c)–(e)、回复文件和 361624 后续评审均未运行。

| 项目 | 结果 |
|---|---|
| R1 远端与 tree 核对 | PASS |
| 步骤1 N1、单个累积提交、全部测试 | PASS，567/567 |
| R3(a) native 原因与 GBS 原文 | 已记录；GBS rc=0 |
| R3(b) tarball / Git tree 内容 | STOP：7/169,029 不同 |
| R3(c) PS3 补丁应用后 / PS4 native | NOT RUN |
| R3(d) 两种模式 spec 原文差异 | NOT RUN |
| R3(e) 五项解析 | NOT RUN |
| 步骤3 sandbox 推送 | NOT RUN；最后只读观测仍为 121b4c23 |
| 步骤4 FINAL 回复文件 | NOT RUN，不把104草稿冒称本次最终回复 |
| 步骤5 361624 评审/试合并/配置/nm | NOT RUN |
| 步骤6 | 本停止报告、原始证据与 STATUS 提交至 bolt-v4 |

## 1. R1 与候选

[R1 原始结果](../../tools/bolt/results/hq-review-361395/round3/R1.json)、[ls-remote 原文](../../tools/bolt/results/hq-review-361395/round3/preflight-ls-remote.stdout)。

- 远端 tizen_base：61ef5d31ca91025c414c748477bef0c64ddfa67c。
- 61ef5d31 与 13c3e223 的 tree 均为 087e06cf9c79c571c711af8a07057496940ae73d。
- Gerrit PS4 e9f16ee3 与 PS3 ecb2dec7 的 tree 均为 b2e8af2477cf623a945aa80bf8288a262dd4a5a9。
- 按 PM R1 接受 PS4 基底；PS3 tree 的既有验证适用于该相同 tree，不冒称包含新修复的候选已获 QB 验证。

新独立游离工作树：/home/linhao/Toolchain/development/llvm-optimize/temp/hq-review-105-20261116/source。
候选：a061f4e415a895412516ffe076084f407f2d70a8；tree：8d08d49a1c70ebb06118d8d84734c695e24e6d32；父：61ef5d31ca91025c414c748477bef0c64ddfa67c。
以104候选3a1b0e29为内容基底，只改 helper call()、converter install_main() 两处 finally 恢复条件：
previous is not None and previous != signal.SIG_DFL。
初始 SIGCHLD 重置分支不变，H2 不使用 pthread_sigmask，提交说明沿用104版本。
[两行代码 diff](../../tools/bolt/results/hq-review-361395/round3/N1.diff)、[候选身份](../../tools/bolt/results/hq-review-361395/round3/candidate.json)、[完整说明](../../tools/bolt/results/hq-review-361395/round3/candidate-message.txt)。
候选工作树干净；旧工作树及分支未改。

## 2. 全量测试

[汇总 JSON](../../tools/bolt/results/hq-review-361395/round3/test-results.json)、[运行脚本](../../tools/bolt/results/hq-review-361395/round3/run-tests.py)。
既有测试只替换被测源码路径，断言不变；测试临时文件由既有保留式驱动保存，未删除历史证据。

| 套件 | 通过 / 总数 |
|---|---|
| policy | 46/46 |
| release | 5/5 |
| r2 | 12/12 |
| r3/r4/r5 | 40/40 |
| hardening | 16/16 |
| review-r11 | 19/19 |
| helper | 393/393 |
| H1–H5 定向 | 30/30 |
| 新 N1 | 6/6 |
| **总计** | **567/567** |

[N1 测试](../../tools/bolt/results/hq-review-361395/round3/tests/test_n1.py)模拟 getsignal 返回 None，覆盖 helper 正常返回和 Popen 原始 OSError（GateError 的 cause 必须是原对象）；converter 正常返回、ValueError、SystemExit、KeyboardInterrupt（原异常对象原样传出）。同时确认未调用 signal.signal(SIGCHLD, None)。
[138项日志](../../tools/bolt/results/hq-review-361395/round3/tests/legacy-138-all.log)、[helper日志](../../tools/bolt/results/hq-review-361395/round3/tests/helper-all.log)、[定向日志](../../tools/bolt/results/hq-review-361395/round3/tests/targeted-all.log)、[N1日志](../../tools/bolt/results/hq-review-361395/round3/tests/N1-all.log)。

原结束行：105步骤1 已结束 2026-11-16T05:52:15.193631-08:00 tests=PASS total=567。

## 3. Native 导出及 R3(b) STOP

[GBS argv](../../tools/bolt/results/hq-review-361395/round3/candidate-export.json)、[stdout](../../tools/bolt/results/hq-review-361395/round3/candidate-export.stdout)、[stderr](../../tools/bolt/results/hq-review-361395/round3/candidate-export.stderr)。
原文：Creating (native) source archive llvm-22.1.8.tar.gz from 'a061f4e415a895412516ffe076084f407f2d70a8'。

原因依据：本机 gbp/scripts/buildpackage_rpm.py 288–302 的 is_native() 在 auto 模式下检查 upstream 分支及同名远端分支；都没有时返回 True。默认 upstream-branch 为 upstream、native 为 auto。本独立 clone 只有 origin/bolt-on-359934、origin/hq-463c9a13-probe、origin/tizen_base，没有 upstream。626行执行 native archive 路径；上述源码与本次实际 native 输出吻合。这是导出环境的模式选择，不是产品代码修改。
[检测源码](../../tools/bolt/results/hq-review-361395/round3/native-detection-source.txt)、[默认配置](../../tools/bolt/results/hq-review-361395/round3/native-config-defaults.txt)、[本地 refs](../../tools/bolt/results/hq-review-361395/round3/native-local-refs.txt)。

流式读取 tarball，逐文件计算 Git blob SHA-1（含正确 NUL 分隔的 blob 头），与 git ls-tree 中对象 ID 比较，同时保存 SHA256；软链接按链接目标比较。排除12个 packaging条目，未发现 .git 文件。169,029 个文件全部处理；Git-only 为0。没有做换行或身份归一化后判 PASS。
[比较器](../../tools/bolt/results/hq-review-361395/round3/native_tree_check-v2.py)、[全量结果](../../tools/bolt/results/hq-review-361395/round3/native-git-result-v2.json)、[逐文件清单索引](../../tools/bolt/results/hq-review-361395/round3/RAW_LINKS.md)、[差异元数据](../../tools/bolt/results/hq-review-361395/round3/export-mismatch-details.json)。

| 文件 | Git / tar 字节数 | 事实 | 原文 |
|---|---:|---|---|
| clang/bindings/python/.git_archival.txt | 110 / 136 | export-subst 提交信息展开 | [原文 diff](../../tools/bolt/results/hq-review-361395/round3/export-mismatch-originals/01-.git_archival.txt.diff) |
| lld/test/wasm/Inputs/libstub.so | 104 / 110 | LF→CRLF；规范化后相同，但未豁免 | [原文 diff](../../tools/bolt/results/hq-review-361395/round3/export-mismatch-originals/02-libstub.so.diff) |
| llvm/test/MC/AsmParser/preserve-comments-crlf.s | 295 / 308 | LF→CRLF；规范化后相同，但未豁免 | [原文 diff](../../tools/bolt/results/hq-review-361395/round3/export-mismatch-originals/03-preserve-comments-crlf.s.diff) |
| llvm/test/tools/llvm-mca/X86/directives-handle-crlf.s | 116 / 120 | LF→CRLF；规范化后相同，但未豁免 | [原文 diff](../../tools/bolt/results/hq-review-361395/round3/export-mismatch-originals/04-directives-handle-crlf.s.diff) |
| llvm/test/tools/split-file/Inputs/basic-aa.crlf | 4 / 6 | LF→CRLF；规范化后相同，但未豁免 | [原文 diff](../../tools/bolt/results/hq-review-361395/round3/export-mismatch-originals/05-basic-aa.crlf.diff) |
| llvm/test/tools/split-file/Inputs/basic-bb.crlf | 6 / 10 | LF→CRLF；规范化后相同，但未豁免 | [原文 diff](../../tools/bolt/results/hq-review-361395/round3/export-mismatch-originals/06-basic-bb.crlf.diff) |
| llvm/test/tools/split-file/basic.crlf.test | 173 / 183 | LF→CRLF；规范化后相同，但未豁免 | [原文 diff](../../tools/bolt/results/hq-review-361395/round3/export-mismatch-originals/07-basic.crlf.test.diff) |

.git_archival.txt 的三行从 $Format 占位符变为候选提交号、提交者时间和 describe-name；根 .gitattributes 含 export-subst。
其余六个文件的唯一内容差异为LF/CRLF；CRLF数量依次为6、13、4、2、4、10。该观察仅用于解释差异，不改变严格比较结论。
[Git attributes 原文](../../tools/bolt/results/hq-review-361395/round3/git-attributes.txt)。

STOP 原文：

    STOP R3(b): candidate native tarball differs from candidate Git blobs in 7 of 169029 files; 169022 identical, 12 packaging entries excluded, no Git-only files. No comparison exceptions applied. Sandbox push and steps R3(c)-R3(e), 3-5 NOT RUN.

原结束行：105步骤2 已结束 2026-11-16T05:59:46.681496-08:00 status=STOP。

## 4. 准备错误与保留现场

本次使用一次准备错误修正机会：初版比较器代码生成转义错误，Git blob 头写入字面量反斜杠零而非NUL，并将JSONL换行写为字面量反斜杠n。导致第一次169,029项误报。首个文件直接读取Git原文与tar字节相同，使用正确NUL所得对象ID与Git一致；错误算法恰好复现首次错误哈希。未修改产品、测试断言或比较条件。
[首次错误证明](../../tools/bolt/results/hq-review-361395/round3/preparation-error-1.json)、[原脚本](../../tools/bolt/results/hq-review-361395/round3/native_tree_check.py)、[修正 diff](../../tools/bolt/results/hq-review-361395/round3/preparation-error-1.diff)。
重跑后缩小为上述7项真实字节差异，按门禁停止，未再修正或豁免。

STOP后只读交付清单脚本另遇路径错误（没有重新跑任何门禁）：

    FileNotFoundError: [Errno 2] No such file or directory: '/home/linhao/Toolchain/development/llvm-optimize-bolt/README.md'

[原文](../../tools/bolt/results/hq-review-361395/round3/delivery-read-error.txt)。没有把该错误当成新的修正机会继续任务。实际STATUS在docs/bolt/STATUS.md，本节只做停止交付记录。
超过10MiB的首次错误结果与完整未分片清单保留原路径，不提交；路径、大小和SHA见[本地大文件登记](../../tools/bolt/results/hq-review-361395/round3/large-local-files.json)。正确清单另分17个gzip文件入库，原文件不动。

## 5. 资源与读取边界

同一串行用户服务 task105-light-20261116.service，MemoryMax=4GiB、swap0、CPU200%、Nice19、IO idle；每30秒检查MemAvailable，低于6GiB停止自身服务。
[资源原文](../../tools/bolt/results/hq-review-361395/round3/resources.json)、[看门狗可见采样](../../tools/bolt/results/hq-review-361395/round3/watchdog-observed.txt)。已采集memory.peak=4,294,967,296B，memory.events max=1166，oom/oom_kill=0；未调高限制，看门狗未触发。峰值包含文件缓存，不等同匿名内存。

已读：STATUS/104记录，104候选与测试、现有H1–H5夹具，R1所需Git对象和远端refs，当前候选全部非packaging Git文件清单与native tar内容，gbp native检测源码及Git attributes。
未读/未执行：新QB、构建、真实输入重放、Gerrit评论写入/refs-for，PS3补丁重新应用及R3(c)比较、两种spec差异与五项解析、361624试合并/CMake/nm、FINAL回复文件。没有干预另一项目。

105 已结束 2026-11-16T06:02:48-08:00 status=STOP

## 6. 105号续：E1/E2 放行与 R3(c) 准备 STOP

本次结论：**R3(b) PASS；R3(c) STOP（准备脚本错误），不判产品失败。** 本地候选仍为 a061f4e415a895412516ffe076084f407f2d70a8，工作树干净；567/567 原测试结果按用户授权沿用，未重新生成候选或重复测试。没有推 sandbox、refs/for 或 Gerrit 文本。

### 6.1 PM 裁决与重新判定

原 R3(b) 的7个差异仅允许两类：
- E1：git check-attr export-subst 为set，且$Format占位符展开能逐字对应导出提交的信息。
- E2：git check-attr eol/text表明应导出CRLF，去掉CR后与Git blob逐字相同。
除此7项再有差异仍STOP。原 README.md 交付路径错误按PM裁定为准备错误，已澄清，不再作为STOP理由；原记录不删。

使用 git check-attr --cached，读取候选索引内的属性，避免 sparse checkout 缺少目录内.gitattributes 影响检查；候选HEAD和干净状态独立复核。
[重新判定JSON](../../tools/bolt/results/hq-review-361395/round3/resume/R3b-reclassification.json)、[候选复核](../../tools/bolt/results/hq-review-361395/round3/resume/candidate-recheck.json)。

| 文件 | 类别 | 核对 | 证据 |
|---|---|---|---|
| clang/bindings/python/.git_archival.txt | E1 | export-subst=set；三个展开值逐字吻合 | [check-attr 原文](../../tools/bolt/results/hq-review-361395/round3/resume/01-.git_archival.txt.check-attr.txt) |
| lld/test/wasm/Inputs/libstub.so | E2 | eol=crlf；去掉CR后逐字吻合 | [check-attr 原文](../../tools/bolt/results/hq-review-361395/round3/resume/02-libstub.so.check-attr.txt) |
| llvm/test/MC/AsmParser/preserve-comments-crlf.s | E2 | eol=crlf；去掉CR后逐字吻合 | [check-attr 原文](../../tools/bolt/results/hq-review-361395/round3/resume/03-preserve-comments-crlf.s.check-attr.txt) |
| llvm/test/tools/llvm-mca/X86/directives-handle-crlf.s | E2 | eol=crlf；去掉CR后逐字吻合 | [check-attr 原文](../../tools/bolt/results/hq-review-361395/round3/resume/04-directives-handle-crlf.s.check-attr.txt) |
| llvm/test/tools/split-file/Inputs/basic-aa.crlf | E2 | eol=crlf；去掉CR后逐字吻合 | [check-attr 原文](../../tools/bolt/results/hq-review-361395/round3/resume/05-basic-aa.crlf.check-attr.txt) |
| llvm/test/tools/split-file/Inputs/basic-bb.crlf | E2 | eol=crlf；去掉CR后逐字吻合 | [check-attr 原文](../../tools/bolt/results/hq-review-361395/round3/resume/06-basic-bb.crlf.check-attr.txt) |
| llvm/test/tools/split-file/basic.crlf.test | E2 | eol=crlf；去掉CR后逐字吻合 | [check-attr 原文](../../tools/bolt/results/hq-review-361395/round3/resume/07-basic.crlf.test.check-attr.txt) |

E1三个值：%H=a061f4e415a895412516ffe076084f407f2d70a8；%cI=2026-11-16T05:49:18-08:00；describe-name=llvmorg-14-init-170502-ga061f4e415a8。将这些值代入Git blob中的$Format占位符后，与tar内容逐字相同。没有放宽到任意身份替换。
其余169022个文件沿用上次完整逐文件比较的相同结论，没有新例外。

105续R3(b) 已结束 2026-11-16T06:20:24.659929-08:00 status=PASS。

### 6.2 R3(c) 首次准备错误与停止

新脚本[compare_export_modes.py](../../tools/bolt/results/hq-review-361395/round3/resume/compare_export_modes.py)从89号保留的PS3上游tar流式读入全部文件，仅把8个补丁涉及的源文件复制到新的overlay目录，计划应用补丁后与104号PS4 native tar逐文件比较。
但overlay位于W/temp下。git apply向上发现了W的证据仓库，以子目录过滤规则跳过补丁；每次仍返回0。本脚本只检查返回码，没有检查Skipped诊断，随后对未打补丁的内容做了比较，这是我的准备错误。
[发现的外层仓库](../../tools/bolt/results/hq-review-361395/round3/resume/R3c-discovered-repository.txt)、[八次诊断与无效比较记录](../../tools/bolt/results/hq-review-361395/round3/resume/R3c-invalid-comparison.json)。

8个补丁的stderr共29行Skipped patch。首条与最后一组示例原文：

    Skipped patch 'clang/include/clang/Config/config.h.cmake'.
    Skipped patch 'clang/cmake/modules/AddClang.cmake'.
    Skipped patch 'clang/tools/driver/CMakeLists.txt'.
    Skipped patch 'lld/cmake/modules/AddLLD.cmake'.
    Skipped patch 'lld/tools/lld/CMakeLists.txt'.
    Skipped patch 'llvm/cmake/modules/AddLLVM.cmake'.
    Skipped patch 'llvm/tools/llvm-ar/CMakeLists.txt'.

随后首个断言：

    AssertionError: ('R3c unexpected difference', {'path': 'clang/cmake/modules/AddClang.cmake', 'old': ('file', 7989, 'ce8e9a0d4ed08c4ffc57195c5eab04b3510e65143ea17f32c1d44173fbceed87'), 'new': ('file', 8036, 'cc505b09c2856008843c430269fb989648090bdcfd1048ab1c2ca16d2c499480'), 'identical': False})

[完整 traceback](../../tools/bolt/results/hq-review-361395/round3/resume/R3c-first-error.txt)。无效输入比较的28项差异不能作为产品差异，也不能作为R3(c)通过的证据。没有把错误结果按E1/E2豁免。

105号前次已使用一次NUL转义准备修正机会；此次续跑未明确重置次数，因此不自行再次改脚本、重新应用或重跑。保留原始脚本、stderr、结果和现场。完整无效清单压缩后9485080字节，已入库；另登记[路径/大小/SHA](../../tools/bolt/results/hq-review-361395/round3/resume/R3c-local-manifest.json)，小型差异和全部诊断已入库。

STOP原文：

    STOP R3(c) preparation: git apply discovered the outer llvm-optimize repository and skipped all eight patches with exit code 0. The comparison input was not patched. The prior 105 preparation-correction allowance was already used; no correction or retry performed. No sandbox push.

105续R3(c) 已结束 2026-11-16T06:23:50.299018-08:00 status=STOP。

### 6.3 后续状态与资源

R3(d)、R3(e)、sandbox推送、FINAL-replies-for-user.md与中文对照、361624试合并/配置/nm/评审均NOT RUN。本次未重新查询sandbox；上次只读观测为121b4c23，无本任务写操作。

已读：前次105候选/完整清单/7处原文，候选索引属性和提交元数据，PS3的8个补丁与上游tar、PS4 native tar，补丁stderr和Git仓库发现结果。
未读/未执行：QB/Gerrit、本次五项spec解析、361624后续核实；未构建。

受限串行服务MemoryMax4GiB、swap0、CPU200%、Nice19、IOidle。首次非交互bootstrap服务立即正常退出、没有运行分析；随后交互服务运行分析与持续30秒看门狗。[资源原文](../../tools/bolt/results/hq-review-361395/round3/resume/resources.json)、[看门狗](../../tools/bolt/results/hq-review-361395/round3/resume/watchdog-observed.txt)。OOM0，看门狗未触发，未调高限制或干预其他项目。

105续 已结束 2026-11-16T06:25:06-08:00 status=STOP
