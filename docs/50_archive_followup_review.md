# 50 x86_64静态归档后续增量评审与升级调查

当前阶段：新评审356949已上传并远端回读核对PASS；继续官方快照与bash/LLVM23调查。日期2026-10-14，时间均为北京时间。

证据E=`temp/archive-followup-review-20261014`；已验收最终树为`4c36e899dffee2869af9afd174346e3eb9a7d7ca`，生产Source SHA `c43523c0ce04fc3310e670ff97823db8260c21250dc3172575a18db56500082e`。既有Source、冻结候选补丁、W/gbs配置和已交接x86构建树不修改。本轮不处理ARM根内执行环境。

## 1. tizen_base合入核查

无交互fetch后最新HEAD=`67619ec8bbbac7238a6cfc33a481ccfbcd12206f`，父提交=`cb67996861d070d68fec2b4c623eed7d20ba2e23`。Gerrit查询356627为MERGED、currentPatchSet=2且revision精确等于该HEAD；356639为NEW，patchset1=`b0465d099164a8f8c1ddd406e6f74c2ada8f9f9f`，未合入。

从cb679968之后全部提交只有以下一条，未发现其他提交修改spec或Source：

|提交|作者时间|标题|文件|
|---|---|---|---|
|67619ec8bbbac7238a6cfc33a481ccfbcd12206f|2026-10-09T16:58:36+08:00|packaging: fix llvm-static-devel with ThinLTO|新增packaging/llvm-static-archives-native.py；修改packaging/llvm.spec|

作者时间不是合入时间。上传PS2与合入commit完全相同，逐文件SHA：spec `d93a549206434c4512c60d5a96bfeb133b7aaf6ea13b8cd0302e06c1cb99b1c9`；Source `6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557`。证据merge-check.json、gerrit-status.jsonl、target-commits-since-base.txt、fetch-tizen-base.*。

已验收候选commit保存在此前隔离仓库`temp/release-attribution-20261013/patch-work`。初次只读git diff在W/llvm查询该本地commit得到bad object；随后核实原候选仓库HEAD精确为4c36e899，未更改输入、门禁或任何Source。证据candidate-location.json。合入版到候选的完整二进制diff存E/merged-to-validated.diff，只涉及spec与Source（116插入/17删除）。

## 2. 本轮用户裁决与执行边界

- 新建独立Gerrit change，父为最新tizen_base，将已验收PS3相对合入版的增量与PS2静态库llvm-strip合为一条提交；两份旧候选文件保持冻结。
- 作者FatTank <hao.lin@samsung.com>，只推refs/for/tizen_base，不直推分支、不推sandbox。356639由用户在新change上传后Abandon，本会话不代办。
- 最终packaging内容须与4c36e899同字节，必须完成干净apply检查、实际apply、整树比较、debug/发布两模式rpmspec parse后才能上传。
- 发布完整构建、同环境未打补丁非归档对照仍不能宣称完成；新快照若可用按本轮条件核对。ARM根内小试/64MiB暂停至下周，宿主不修改。
- 资源、项目锁与共享重任务锁、1.2倍/30GiB磁盘规则沿用。开场轻任务内存准入通过，用户gbs配置改动SHA与登记一致。

## 3. 新单提交、应用与宏展开

新提交 `d4dd40da3b6ab28925b57d24d66bd992b4ad798c`，父提交 `67619ec8bbbac7238a6cfc33a481ccfbcd12206f`，作者/提交者FatTank <hao.lin@samsung.com>；新Change-Id `I9a815cad07c9bd5ae1e3068fe5b13a339e2ea3ce`。隔离仓库E/submit-work，不修改W/llvm。完整树OID `480be0836bc470dd027f73882b4082d0ce0e5000` 与已验收4c36e899完全相同；仅spec/Source两文件变化。新提交相对父的full-index binary diff与“合入版→已验收候选”diff逐字节相同，SHA `4cc17eaf866d6a9e4152ba47767d094b29aff6caf2503611f9359cd01ff8ea72`。干净副本E/apply-check依次apply --check、实际apply、write-tree，完整树亦完全相同（E/generation-result.json、generation-commands.json）。

|文件|字节|SHA256|
|---|---:|---|
|packaging/llvm.spec|22505|e88ef4cb4cfc4010bceb62a94389f517aedff0b2c2df819ba64dd988d9910426|
|packaging/llvm-static-archives-native.py|45786|c43523c0ce04fc3310e670ff97823db8260c21250dc3172575a18db56500082e|
|新format-patch|见generation-result.json及仓库文件|437f128a668b6e38cfed582c44e8ec48dec52144f68b1aa4126f496f384087ff|

新增补丁与完整英文说明分别为[format-patch](../patches/archive-index-fix/followup/0001-packaging-refine-x86_64-static-archive-handling.patch)、[commit-message](../patches/archive-index-fix/followup/commit-message.txt)。旧PS3/PS2冻结文件保留不覆盖。

两种模式rpmspec --parse均exit0，且分支断言通过：debug不含RELCFLAGS去debug段，release包含该段；两者转换器均展开为build/bin/clang。使用旧x86 archivefix-v2根的RPM及库经显式loader只读运行，未进入已交接构建树、没有执行%build/%install。发布环境是历史abuild/.rpmmacros的证据副本，**仅去掉%_toolchain定义一行**；其他宏相同，解析的候选spec本体不改。完整argv/输出/宏diff见E/rpmspec-final-result.json、debug-rpmspec.stdout、release-isolated-rpmspec.stdout、release-macro-environment.diff。

辅助环境检查曾两次拒绝错误的“发布”输入：CLI --undefine，以及临时输入前缀单次%undefine，均parse exit0却仍含debug分支，不能当作发布PASS。根宏文件home/abuild/.rpmmacros:63确实定义_toolchain；改以隔离宏文件去掉该定义后，未修改候选spec，真实发布分支通过。原始输出及两个尝试保留；这是解析环境构造问题，不是配方或Source失败，也未放宽发布分支断言。

## 4. Gerrit上传与远端回读

2026-10-14 15:58:18，新评审 **[356949](https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/356949)**，patchset1，状态NEW。唯一push目标`HEAD:refs/for/tizen_base`；上传前ls-remote复核父HEAD仍为67619ec8。没有直推tizen_base/sandbox，没有操作356639状态。

- commit：`d4dd40da3b6ab28925b57d24d66bd992b4ad798c`
- parent：`67619ec8bbbac7238a6cfc33a481ccfbcd12206f`
- Change-Id：`I9a815cad07c9bd5ae1e3068fe5b13a339e2ea3ce`
- ref：`refs/changes/49/356949/1`

上传后SSH query及fetch上述ref，FETCH_HEAD的commit与完整tree均精确等于本地；这是远端实际回读，不只依赖push成功信息。证据E/gerrit-push.*、new-change-query.stdout、fetch-uploaded-change.*、uploaded-review.json。356639由用户Abandon。

## 5. 合入后官方快照：条件尚未满足

2026-10-14 15:59直取下载站[Base快照目录](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/)，HTTP200，原文SHA `93dd5db3a111998f83f2e5c668018788c0d91fdb3dca55e63fb840d34d8d0281`。目录列出20260914.073422、20260924.094908、20261010.120615、20261013.024319、**20261013.140248**；最新仍为10月13日。Gerrit SUBM时间为2026-10-14 14:48:39+08，未见合入后的快照目录，故本轮不启动两快照RPM下载/比较，登记待办、不等待。不是以作者日期10月9日推断已发快照，也未声称任一历史快照静态库或非归档文件对照通过。证据E/base-list.body、official-release-check.json、post-merge-snapshot-result.json与gerrit-status.jsonl。

## 6. bash依赖清单

本轮对git跟踪的tools/*.py、*.sh逐文件扫描，并人工核对命中类别。两份Source AST均只有一处外部启动：生产Source:480/488、ARM候选:1208/1216先构造`['/usr/bin/prlimit', ..., *map(str, argv)]`再`subprocess.Popen(command, ...)`；没有shell=True、os.system/os.popen或直接bash调用。ARM:747–789显式选择参数传入的原生shell，借`/usr/bin/env -u BASH_ENV -u ENV`隔离环境，再执行POSIX sh片段和`exec "$@"`；可以指向bash，但不依赖bash命令名称/专有语法（本次Source SHA仍c43523c0/1bac8db6）。

宿主本轮实际运行`python3 -m unittest -v test_archive_review_round4_continue.PosixLauncherTests`：**6/6 PASS，52.156秒**。逐项：shell不存在/不可执行/错误架构拒绝；限制设置失败exit125；bash/dash/sh三者AS软硬4GiB与core0读回/身份；引号参数与BASH_ENV/ENV不执行；三者超时SIGKILL与子进程回收；不支持ulimit与读回错值exit125。/bin/sh实际指向dash；三路径resolved/SHA与完整输出存E/bash-audit/launcher-tests.*。这不是ARM根内实测，本轮按决定不挂载/proc、不恢复binfmt。

下列14个文件保留为仓库辅助驱动/测试的bash债务，**没有修改它们**。测试中的bash字面量可能只是覆盖多shell/拒绝参数的夹具，不代表转换生产依赖；Python局部变量名bash与注释亦不算外部调用。完整行原文、文件SHA、AST审计见E/bash-audit/result.json。该扫描不等同任意动态生成shell内容的形式化证明；LLVM源码自身bash审计仍留待总部dash切换时另做。

|文件|类别|行号|
|---|---|---|
|tools/bolt_final_attempt.py|explicit bash argv/string|159|
|tools/build_llvm_x86_64.sh|bash shebang (possibly generated fixture)；bash-specific shell option/builtin|1, 3|
|tools/check_bolt_liveness.sh|bash shebang (possibly generated fixture)；bash-specific shell option/builtin|1, 3|
|tools/finish_bolt_final.py|explicit bash argv/string|71|
|tools/relink_clang_for_bolt.py|explicit bash argv/string|90|
|tools/resume_llvm_x86_64.py|explicit bash argv/string|109|
|tools/run_bolt_stage.py|explicit bash argv/string|97, 99|
|tools/run_static_archive_conversion.py|explicit bash argv/string|58|
|tools/test_archive_review_round4.py|测试/夹具；explicit bash argv/string|170|
|tools/test_archive_review_round4_continue.py|测试/夹具；explicit bash argv/string|93, 95|
|tools/test_check_bolt_liveness.sh|测试/夹具；bash shebang (possibly generated fixture)；bash syntax (manual review required)；bash-specific shell option/builtin|1, 3, 16, 21|
|tools/test_verify_toolchain_identity.sh|测试/夹具；bash shebang (possibly generated fixture)；bash syntax (manual review required)；bash-specific shell option/builtin|1, 3, 35, 37, 52, 53, 56, 57, 61, 62, 68, 69, 70, 71, 75, 81, 88, 89, 94, 110, 121, 132, 178, 191, 224|
|tools/verify_toolchain.sh|bash shebang (possibly generated fixture)；bash-specific shell option/builtin|1, 3|
|tools/verify_toolchain_identity.sh|bash shebang (possibly generated fixture)；bash syntax (manual review required)；bash-specific shell option/builtin|1, 3, 74, 76, 79, 80, 84, 88, 89, 92, 94, 98, 100, 102, 103, 104, 106, 112, 117, 119, 120, 124, 126, 127, 130, 154, 157, 164, 173, 175, 177, 182, 194, 195, 197, 199, 205, 207, 208, 209, 212, 215, 216, 220, 231, 232, 235, 239, 242, 251, 252, 268, 276, 281, 282, 300, 301, 302, 313, 317|
