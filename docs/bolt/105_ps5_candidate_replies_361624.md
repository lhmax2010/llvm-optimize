# 105：PS5 候选、导出核对与停止记录

> **105续三最新状态：sandbox 已为 a061f4e415a895412516ffe076084f407f2d70a8。R3(a–e)通过（c由PM裁决）；567/567沿用；FINAL回复已生成、未发布。361624试合并的树内CMake配置失败，按规则STOP；未完成项目见§8.4。下方§1–7为原停止记录，全部保留。**

> 105号续二最新状态：R3(b)已按PM裁决通过；R3(c)的8个补丁实际应用及反向dry-run全部通过，但新的清单脚本漏记目录符号链接，按“再有准备错误即STOP”停止，未推sandbox。见文末§7，历史STOP原文保留。

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

## 7. 105号续二：实际应用补丁通过，清单准备 STOP

结论：**STOP，未推 sandbox。** 用户授权修正外层Git仓库发现问题后，已在/var/tmp的新临时目录完整解包上游tar，8个补丁应用、修改文件数核对和8次反向dry-run全部通过。但后续os.walk清单遗漏一个指向目录的符号链接；这是新准备错误，不能判产品失败，也未继续修改或重跑。

### 7.1 授权修正和防静默跳过

解包根目录：/var/tmp/task105-r3c-sf_6b3k0/llvm-22.1.8。
解包前后git rev-parse --show-toplevel均失败，确认没有外层Git仓库。[原文](../../tools/bolt/results/hq-review-361395/round3/resume2/outside-git.stderr)。
使用GNU patch 2.7.6，实际命令：
patch -p1 --forward --batch --no-backup-if-mismatch -i <补丁>。
每次要求rc=0，stdout中的patching file列表与git apply --numstat所列路径逐项一致，且不能包含Skipped、FAILED、Reversed。
8个补丁全部应用后，在最终树上逐个运行patch -p1 --reverse --dry-run --batch -i <补丁>，均rc=0，checking file列表也与diffstat一致。没有实际反向修改树。
[脚本](../../tools/bolt/results/hq-review-361395/round3/resume2/compare_export_modes.py)、[相对前次修正diff](../../tools/bolt/results/hq-review-361395/round3/resume2/preparation-fix.diff)、[应用/反向完整JSON](../../tools/bolt/results/hq-review-361395/round3/resume2/patch-application.json)。

| 补丁 | diffstat文件数 | 实际修改文件数 | 反向dry-run | 原文 |
|---|---:|---:|---|---|
| 0001 | 6 | 6 | PASS | [应用](../../tools/bolt/results/hq-review-361395/round3/resume2/patch-0001.stdout) / [反向](../../tools/bolt/results/hq-review-361395/round3/resume2/reverse-0001.stdout) |
| 0002 | 1 | 1 | PASS | [应用](../../tools/bolt/results/hq-review-361395/round3/resume2/patch-0002.stdout) / [反向](../../tools/bolt/results/hq-review-361395/round3/resume2/reverse-0002.stdout) |
| 0003 | 1 | 1 | PASS | [应用](../../tools/bolt/results/hq-review-361395/round3/resume2/patch-0003.stdout) / [反向](../../tools/bolt/results/hq-review-361395/round3/resume2/reverse-0003.stdout) |
| 0004 | 3 | 3 | PASS | [应用](../../tools/bolt/results/hq-review-361395/round3/resume2/patch-0004.stdout) / [反向](../../tools/bolt/results/hq-review-361395/round3/resume2/reverse-0004.stdout) |
| 0005 | 2 | 2 | PASS | [应用](../../tools/bolt/results/hq-review-361395/round3/resume2/patch-0005.stdout) / [反向](../../tools/bolt/results/hq-review-361395/round3/resume2/reverse-0005.stdout) |
| 0006 | 1 | 1 | PASS | [应用](../../tools/bolt/results/hq-review-361395/round3/resume2/patch-0006.stdout) / [反向](../../tools/bolt/results/hq-review-361395/round3/resume2/reverse-0006.stdout) |
| 0007 | 9 | 9 | PASS | [应用](../../tools/bolt/results/hq-review-361395/round3/resume2/patch-0007.stdout) / [反向](../../tools/bolt/results/hq-review-361395/round3/resume2/reverse-0007.stdout) |
| 0008 | 6 | 6 | PASS | [应用](../../tools/bolt/results/hq-review-361395/round3/resume2/patch-0008.stdout) / [反向](../../tools/bolt/results/hq-review-361395/round3/resume2/reverse-0008.stdout) |

共29次文件修改记录；重复路径按各补丁分别计数，不把事件总数冒称独立文件数。

### 7.2 新准备错误

PS3解包树清单使用os.walk遍历时只处理files，没有把dirs中的符号链接纳入清单。实际存在的链接因此被记录为old=None：

    lldb/test/API/functionalities/breakpoint/breakpoint_with_realpath_and_source_map/symlink2

只读lstat/readlink核实：该项存在，是指向目录的符号链接，目标字符串为real（4字节），SHA256为aa33996d60e89311b4d1a920dae03c6d7fa3ae1956c52662e273aad4683e577f，与PS4 native tar记录完全相同。
[原始比较差异](../../tools/bolt/results/hq-review-361395/round3/resume2/R3c-raw-differences.json)、[实际链接证据](../../tools/bolt/results/hq-review-361395/round3/resume2/symlink-inventory-error.json)、[完整首次traceback](../../tools/bolt/results/hq-review-361395/round3/resume2/first-error.txt)。
原始比较仅列出.git_archival.txt和该链接两项；本次没有修改清单、重新执行比较或把无效比较标为PASS。

原始断言：

    AssertionError: ('new unexpected difference', {'path': 'lldb/test/API/functionalities/breakpoint/breakpoint_with_realpath_and_source_map/symlink2', 'old': None, 'new': ('symlink', 4, 'aa33996d60e89311b4d1a920dae03c6d7fa3ae1956c52662e273aad4683e577f'), 'identical': False})

STOP原文：

    STOP R3(c) preparation: the os.walk manifest loop omitted symlinks to directories from the extracted PS3 tree. All eight patches were applied and passed reverse dry-run, but the manifest comparison is invalid. No further preparation correction or retry was made; sandbox push and later steps were not run.

105续二R3(c) 已结束 2026-11-16T06:41:16.671507-08:00 status=STOP。

### 7.3 范围与剩余工作

候选仍为a061f4e415a895412516ffe076084f407f2d70a8，tree 8d08d49a1c70ebb06118d8d84734c695e24e6d32，工作树干净。[复核](../../tools/bolt/results/hq-review-361395/round3/resume2/candidate-recheck.json)。
按授权沿用567/567测试结果，不重新生成候选。R3(b)的E1/E2通过结论保留。
R3(d)、R3(e)、sandbox推送、FINAL回复/中文说明、361624后续评审未运行；105没有完成，因此没有进入用户要求“完成后”执行的107。
本次没有查询或写入Gerrit、推LLVM分支、访问QB或构建，也没有改历史目录。新解包目录与全部日志保留。

已读：PS3历史导出tar、0001–0008、PS4 native tar、候选Git对象、补丁应用与反向诊断、目录链接原始元数据。
未执行：重新跑567测试、后续五项解析、361624配置/试合并/nm、对外回复发布。
[资源](../../tools/bolt/results/hq-review-361395/round3/resume2/resources.json)、[看门狗采样](../../tools/bolt/results/hq-review-361395/round3/resume2/watchdog-observed.txt)：4GiB/swap0/CPU200%/Nice19/idle，OOM0，看门狗未触发，没有提高资源上限。

105续二 已结束 2026-11-16T06:42:24-08:00 status=STOP


## 8. 105号续三：导出通过、sandbox已推；361624配置STOP

### 8.1 R3(c) PM裁决（原文）

PM 已核对 resume2 的证据（R3c-raw-differences.json、symlink-inventory-error.json、两份 archival 原文）：
- 169,029 个路径中只有2处原始差异；
- clang/bindings/python/.git_archival.txt：属于 E1，两侧分别是对各自归档提交（ca7933e4 与 e9f16ee3）展开的结果；
- lldb/.../symlink2：PS3 树中确实存在该目录符号链接（lexists=true、is_symlink=true），只是清单脚本没有记录；native 侧为同一个指向 real 的链接。
- 8个补丁全部实际应用，并通过反向 dry-run。
结论：R3(c) PASS（PM 裁决，依据上述证据）。不需要修改或重跑清单脚本；在报告中照录本裁决。

没有修改或重跑resume2清单脚本。候选仍为a061f4e415a895412516ffe076084f407f2d70a8，
tree为8d08d49a1c70ebb06118d8d84734c695e24e6d32，父61ef5d31；工作树干净，
沿用已完成的567/567，不再生成提交。

### 8.2 R3(d)/(e)与推送

| 项目 | 当前结论 |
|---|---|
| R3(a) | PASS，先前GBS原文说明native模式，未重导出 |
| R3(b) | PASS，先前7文件逐项E1/E2证据沿用 |
| R3(c) | PASS，以上PM裁决，原始2差异与原STOP保留 |
| R3(d) | PASS，完整spec差异保存；PS3→PS4为VCS及生成Patch/%patch删除；PS4→候选为VCS及批准的H3显式debugfiles.list参数 |
| R3(e) | PASS，x86_64开/关、armv7l、aarch64、一行bcond回退，5/5 |
| sandbox | PASS，121b4c23→a061f4e4，带准确lease且ls-remote核对 |
| FINAL回复 | PASS，5条inline+Q1–Q6，英文门禁通过，未发布 |
| 361624 | PARTIAL/STOP，spec冲突保留，树内配置出现source-list错误 |
| 107 | 未开始，用户称材料尚未就绪，等通知 |

native模式5项均Patch count=0，无残留%patch，Source全部存在。
平台rpmbuild -bp --nodeps --nobuild及rpmspec解析均rc=0，只有x86-on启用BOLT；
没有运行RPM构建。原文与展开见[五项结果](../../tools/bolt/results/hq-review-361395/round3/resume3/five-parse-result.json)，
4份完整spec diff见[证据索引](../../tools/bolt/results/hq-review-361395/round3/resume3/RAW_LINKS.md)。

推送命令：

```sh
git push --force-with-lease=refs/heads/sandbox/lhmax2025/bolt_pgo:121b4c23bcd6a9a30b0e277c30e5dc17af3e8521 ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm a061f4e415a895412516ffe076084f407f2d70a8:refs/heads/sandbox/lhmax2025/bolt_pgo
```

SSH BatchMode，推送前tizen_base仍61ef5d31。远端返回rc=0，仅提示标题超过50字符，
不是拒绝；不改用户固定的提交。推送后远端为a061f4e415a895412516ffe076084f407f2d70a8。
[命令与原文](../../tools/bolt/results/hq-review-361395/round3/resume3/sandbox-push.stderr)、
[前后SHA](../../tools/bolt/results/hq-review-361395/round3/resume3/sandbox-result.json)。
没有推refs/for、回复、评论、投票；未访问QB。

### 8.3 用户回复文件

- [FINAL-replies-for-user.md](../../tools/bolt/results/hq-review-361395/round2/replies/FINAL-replies-for-user.md)：先5条PS3行内位置及原文第一句，再Q1–Q6；next patch set明确指PS5。
- [中文代码对照](../../tools/bolt/results/hq-review-361395/round2/replies/FINAL-replies-code-map-zh.md)：a061f4e4具体位置，供用户追问时核对。
- H2说明暂存第二次信号及未采用pthread_sigmask的原因；H1/H5含N1；Q2按5A/5B、不称全部无害；Q3另change；Q5最小插件验证。
- [门禁](../../tools/bolt/results/hq-review-361395/round3/resume3/final-replies-gate.json)通过。只是文件，所有发布由用户本人执行。

### 8.4 361624：已证明的停止点

完整父提交/diff、HQ合入后改接评论、影响表、配置限制与未运行项见
[部分评审](../../tools/bolt/results/hq-review-361395/round3/resume3/361624-review-partial.md)。
试cherry-pick到独立游离工作树，只有packaging/llvm.spec冲突；未解决、未提交。
未叠加侧CMake成功、ninja查询一条最终链接命令且不含libLLVM.so；
叠加侧配置失败，原文：

```text
CMake Error at cmake/modules/LLVMProcessSources.cmake:113 (message):
  Found erroneous configuration for source file X86BoltMnemonicTables.cpp

  LLVM's build system enforces that all source files are added to a build
  target, that exactly one build target exists in each directory, and that
  this target lists all files in that directory.  If you want multiple
  targets in the same directory, add PARTIAL_SOURCES_INTENDED to the target
  specification, though it is discouraged.

  Please update
  /home/linhao/Toolchain/development/llvm-optimize/temp/hq-review-105-20261116/trial-361624/bolt/lib/Target/X86/CMakeLists.txt


Call Stack (most recent call first):
  cmake/modules/LLVMProcessSources.cmake:59 (llvm_check_source_file_list)
  cmake/modules/AddLLVM.cmake:519 (llvm_process_sources)
  cmake/modules/AddLLVM.cmake:925 (llvm_add_library)
  /home/linhao/Toolchain/development/llvm-optimize/temp/hq-review-105-20261116/trial-361624/bolt/lib/Target/X86/CMakeLists.txt:31 (add_llvm_library)


```

新cpp只在BOLT_BUILT_STANDALONE时加入目标，未列LLVM_OPTIONAL_SOURCES，
触发LLVMProcessSources完整性检查。未修补HQ代码或重试；不能声称已证明最终共享链接命令。
原日志还含平台cmake子进程OPENSSL_3.2.0装载报错，一并保留。
后续tool-plan执行、find-debuginfo/build-id详细核实、nm-D导出符号核实均NOT RUN；
不会把这些缺口写成通过。[STOP原文](../../tools/bolt/results/hq-review-361395/round3/resume3/step5-STOP.txt)。
[英文部分草稿](../../tools/bolt/results/hq-review-361395/round3/resume3/361624-review-for-user.partial.md)未发布。

本次读取旧导出/测试/PM证据、PS5源码、361624完整diff、HQ既存评论、试合并与配置输出；
没有重跑567测试、R3(c)清单或实际构建；未读取新的QB数据，未触碰其他项目。
停止报告生成时JS模板中的未转义反引号触发SyntaxError，命令尚未执行；
使用本次一次准备修正，仅修交付脚本引用方式，不重跑配置。原文和修正说明见
delivery-preparation-error.txt、delivery-preparation-fix.diff（编排层差异，不冒称磁盘旧脚本）。
资源4GiB/swap0/CPU200%/Nice19/idle串行，峰值2,220,883,968 B，
max/OOM/oom_kill均0；看门狗快照无低于6GiB样本。

交付补记：新增的ASCII断言把英文标题的U+2014破折号拒绝，发生第二次准备错误；未修改草稿、未修断言、未重跑。原英文/禁止引用门禁结果保留，新检查不能称通过。只保全现有证据并提交停止报告。原文见[delivery-second-STOP.txt](../../tools/bolt/results/hq-review-361395/round3/resume3/delivery-second-STOP.txt)。
