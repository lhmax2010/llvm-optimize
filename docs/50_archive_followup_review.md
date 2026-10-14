# 50 x86_64静态归档后续增量评审与升级调查

最终状态：新评审356949已上传并远端回读核对PASS；bash清单与LLVM23探测完成（发现升级解析边界）；官方快照对照待新快照，ARM根内按用户决定暂停。日期2026-10-14，时间均为北京时间。

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
|新format-patch|17916|437f128a668b6e38cfed582c44e8ec48dec52144f68b1aa4126f496f384087ff|

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
|tools/test_check_bolt_liveness.sh|测试/夹具；bash shebang、pipefail、BASH_SOURCE数组、bash语法|1, 3, 8, 16, 21|
|tools/test_verify_toolchain_identity.sh|测试/夹具；bash shebang (possibly generated fixture)；bash syntax (manual review required)；bash-specific shell option/builtin|1, 3, 4, 35, 37, 41, 52, 53, 56, 57, 61, 62, 68, 69, 70, 71, 75, 81, 88, 89, 94, 110, 121, 132, 178, 191, 224|
|tools/verify_toolchain.sh|bash shebang (possibly generated fixture)；bash-specific shell option/builtin|1, 3|
|tools/verify_toolchain_identity.sh|bash shebang (possibly generated fixture)；bash syntax (manual review required)；bash-specific shell option/builtin|1, 3, 74, 76, 79, 80, 84, 88, 89, 92, 94, 98, 100, 102, 103, 104, 106, 112, 117, 119, 120, 124, 126, 127, 130, 154, 157, 164, 173, 175, 177, 182, 194, 195, 197, 199, 205, 207, 208, 209, 212, 215, 216, 220, 231, 232, 235, 239, 242, 251, 252, 268, 276, 281, 282, 300, 301, 302, 313, 317|

## 7. LLVM23前向读取探测（方法与工具）

从[LLVM官方发布页23.1.3](https://github.com/llvm/llvm-project/releases/tag/llvmorg-23.1.3)选择当时最新非预发布23.x版本。GitHub官方releases API前100项原文HTTP200、SHA `3362d46f9ae9b34ab037cb8ac07f3f337c6a67911f18a9f7fc6c1824f02850cb`；选取Linux-X64 `.tar.zst`，1,188,398,549B，下载SHA与官方asset digest相同：`14d2f701eb68fb799001bdea6231048f3990690fa2f406d563555ff8f744daba`。只解包clang、llvm-dis及同包顶层共享库到本轮证据目录，不安装宿主软件、不使用已交接的x86构建树。

第一次辅助解包未产出工具：zstd默认解码窗口上限128MiB，官方文件声明1GiB窗口；只读`zstd -lv`与`zstd -t`明确报`1073741824 > 134217728`并建议`--memory=1024MB`。按提示修辅助解包命令一次，保持18GiB/swap0、共享锁及内存/磁盘底线，新输出目录保留首次记录。第二次解包成功，wall10.975秒、scope峰2,320,326,656B、OOM0；没有修改Source/命令策略或升级版本门禁。证据llvm23-probe/extraction-helper-diagnosis.json、zstd-default-test.stderr、E/llvm23-extract-helper-fix.diff、两次extraction-scope。

工具身份：

|工具|实际版本|SHA256|
|---|---|---|
|新包bin/llvm-dis|23.1.3|52a2775dd1e203a83420ea879111222f3aa6162c100e2039729c73b7d8f662a5|
|新包bin/clang→clang-23|23.1.3|913453afb492abab17025139852413ba7fd7a52b4fb75fcce58ff3fe399d0a9e|
|旧x86 archivefix-v2 build/bin/llvm-dis|22.1.8|9416f931e11ca81259c02fb53f103125771cb8fa3a534a1bf4c7daf2df9a34c7|

clang --version原文首三行（InstalledDir完整路径见E/llvm23-probe/clang-23-version.stdout）：

```text
clang version 23.1.3 (https://github.com/llvm/llvm-project 0d261d1ca552c95a8f007e061c787ac7132fbcbc)
Target: x86_64-unknown-linux-gnu
Thread model: posix
```

选样先纳入此前全量普查的全部module asm成员（x863、ARM322、AArch643），再按已保存归档路径排序等距选档、每档选首个bitcode成员，确定性补到每架构200个不同成员。没有根据新解析结果挑选样本。逐档核对旧summary的before SHA，按ordinal/名称/同名序号提取且核对成员SHA；输入分别为E5/x86-input、E11原armv7l-input和E12原aarch64-input，均为已有22.1.8 bitcode。选样清单及引用summary SHA见E/llvm23-probe/selection-members.json。

每成员执行22.1.8与23.1.3的`llvm-dis input.bc -o {22,23}.ll`，均经`prlimit --as=4294967296 --core=0`；使用当前未改Source的ir_settings/arm_ir_settings直接解析文本，比对**所有返回字段**，保留两份文本、参数、stderr、IR SHA、完整解析结果及unified diff。不调用clang做代码生成/转换，不绕过生产validate_tools门禁。x86旧读取器取自历史archivefix-v2根，和已交接给BOLT的20261013新根不是同一棵树。

### 7.1 600个样本的结果与全部解析差异

|架构|样本|两版llvm-dis成功/当前解析异常|返回字段完全相同|evidence字段不同|module_asm漏读|module_asm_sections漏读|
|---|---:|---|---:|---:|---:|---:|
|x86_64|200|200 / 0|18|182|3|不适用|
|armv7l|200|200 / 0|21|179|2|2|
|aarch64|200|200 / 0|14|186|3|不适用|

600个样本的flags、原命令、policy、triple、PIC/PIE、CPU/features（以及ARM函数认证返回值）在两版输出中均相同。但这不表示解析结果全部正确：**LLVM23将module asm改为两行，现解析器静默漏读全部8个已有声明。** 例如x86 libLLVMAnalysis.a/MLInlineAdvisor.cpp.o ordinal80（同名序号1），LLVM22与LLVM23原文分别为：

```llvm
; LLVM22，第6行
module asm ".globl _ZSt21ios_base_library_initv"
; LLVM23，第6–7行
module asm
    ".globl _ZSt21ios_base_library_initv"
```

生产ir_settings在tools/llvm_static_archives_source.py:309按`line.startswith('module asm ')`收集；白名单在:281起同样依赖单行。ARM白名单在tools/llvm_static_archives_arm_trial.py:573起同一假设，ARM32节跟踪也因此漏记。**声明仍存在于23的IR文本，是解析器漏读，不是llvm-dis删除声明。** 当前生产入口的validate_tools仍在生产:629、ARM:1357硬拒绝LLVM主版本非22，本轮不改任何版本/解析门禁。将来不能只把主版本常量改成23；须先认证多行IR语法并重新检查全部asm白名单/输出符号门禁。本次仅探测，不将LLVM23标为兼容认证。

8个必选成员如下，ordinal为0起、同名序号均1：

|架构|归档|成员|ordinal|
|---|---|---|---:|
|x86_64|libLLVMAnalysis.a|MLInlineAdvisor.cpp.o|80|
|x86_64|libLLVMCodeGen.a|MLRegAllocEvictAdvisor.cpp.o|137|
|x86_64|libarcher_static.a|ompt-tsan.cpp.o|0|
|armv7l|libLLVMAnalysis.a|MLInlineAdvisor.cpp.o|80|
|armv7l|libLLVMCodeGen.a|MLRegAllocEvictAdvisor.cpp.o|137|
|aarch64|libLLVMAnalysis.a|MLInlineAdvisor.cpp.o|80|
|aarch64|libLLVMCodeGen.a|MLRegAllocEvictAdvisor.cpp.o|137|
|aarch64|libarcher_static.a|ompt-tsan.cpp.o|0|

`evidence`是Source保留的原始属性组/模块标志文本。去掉属性组/元数据编号、忽略列表次序后，ARM32与AArch64各1个仅编号/顺序不同；其余x86182、ARM32178、AArch64185个仍有属性内容或数量差异（如内存内建声明的nosync属性变化、属性组数量变化）。不把这些差异隐去，也不声称代码生成等价。**每一个差异字段的两版完整值**以及600项成员身份、输入/IR SHA、错误、必选asm原文已公开到[解析差异JSON](50_llvm23_probe_results.json)，字段差异按SHA去重引用difference_catalogue；这只是存储去重，不丢差异。全量原始.ll、命令、stderr、unified diff仍保留E/llvm23-probe/samples。

公开JSON 6,290,224B，SHA `c026254166a59dc83c538d8c7a2b1d214522f4f820a2d02d67bbb3aa7239cb6b`。本次读取探测wall 564.164s，scope峰 11,494,162,432B（含页缓存，非单个llvm-dis自身RSS），最大采样进程树RSS 614,035,456B；宿主可用最低采样 17,259,884,544B、/home可用最低采样 333,983,961,088B。scope18GiB/swap0，无OOM/max事件；每2秒保护、30秒持久采样，共享锁在读取前取得、完成后释放，采样器/reader已回收。资源原文E/probe-resource-summary.json与llvm23-probe-scope。未做任何LLVM构建、归档转换或新性能结论。

## 8. 最终范围与后续

|项目|本轮状态|
|---|---|
|tizen_base与356627/356639状态|PASS，67619ec8为父，只有356627改动；356639未合入|
|新提交、最终内容/整树、apply、双模式parse|PASS，新commit d4dd40da3b6a，完整树等于已验收4c36e899|
|Gerrit上传与回读|PASS，新356949 PS1；用户随后Abandon356639|
|官方快照非归档/归档对照|PENDING：目录未出现合入后的新快照；没有下载两套RPM或宣称比较PASS|
|bash依赖扫描及三shell测试|完成：14辅助脚本登记债务，6专项PASS；两Source无直接bash或shell=True|
|LLVM23探测|完成600样本，0读取/解析异常但8个asm静默漏读；未认证23、未改Source|
|ARM根内小试/64MiB负例|按用户决定暂停至下周，本轮不处理binfmt、不挂载/proc|
|发布模式完整构建|仍待PM；已有60对样本认证不能代替完整发布构建|

## 9. 本次提交说明全文

以下与上传commit message逐字相同（独立文件见§3）：

```text
packaging: refine x86_64 static archive handling

Background:
Change 356627 converts ThinLTO bitcode members in installed x86_64 static
archives to native objects and rebuilds their indexes. This avoids index
damage from GNU strip and makes the archives usable by GNU ld without
LTO or an LLVM plugin.

Changes:
- Support release builds without _toolchain. When the recorded command
  has no debug options, do not add -g or -gdwarf-4 during conversion.
  The merged version rejects this case because it requires -gdwarf-4.
  Reject no-debug commands whose IR still contains a debug compile unit.
- Reject unsupported assembler options (-Wa, and -Xassembler), require
  clang, llvm-dis and llvm-nm to have the same full LLVM 22 version, and
  check ELF section, symbol and relocation table bounds and strides.
  Allow only the certified iostream module-assembly declaration and
  verify that its undefined symbol is preserved after conversion.
- Use the build/bin/clang alias instead of a hard-coded clang-22 path.
- Use llvm-strip for static archive post-processing, following the
  platform's move to LLVM. Override only the archive-strip argument in
  __strip_install_post; ordinary executable stripping keeps the platform
  default. Find-debuginfo and other enabled post-processing remain intact.
  The override copies tizen_macros:34-38 from rpm-build-4.14.1.1-1.4 and
  must be synchronized when the platform changes that macro. It covers
  all static archives in this package's buildroot, including compiler-rt.

Scope:
Only x86_64 is affected. The conversion also includes libarcher_static.a.
armv7l and aarch64 packaging are unchanged; ARM support will be submitted
separately. Final static archives contain no DWARF after stripping.

Testing:
A full x86_64 build completed with one serial continuation in the
Tizen-Base-Toolchain tizen-base-toolchain_20261010.120615 environment.
All 225 development archives (3,864 ordered members) contain native
objects and complete indexes. Checks passed for all 45 compiler-rt
archives, including allocated section contents and symbol-to-member
mappings. Host and Tizen GNU ld (without LTO or plugins) and lld consumers
linked and ran successfully, including sanitizer, profile and builtins
probes. Independent reinstallation reproduced the converted archives;
a repeated converter invocation skipped the already-native archives.

Across 60 paired x86_64, armv7l and aarch64 source samples, release/debug
conversion arguments differed only by the debug options. Differences in
object output were attributed to compiler debug-information handling.
A complete release-mode package build is still pending.

The non-archive file comparison against an unpatched build in the same
environment has not yet been run; it will be checked using the next
official snapshot.

Supersedes Change 356639.

Signed-off-by: FatTank <hao.lin@samsung.com>
Change-Id: I9a815cad07c9bd5ae1e3068fe5b13a339e2ea3ce
```

## 10. 收尾与完整性

2026-10-14T16:18:28.485266+08:00终检PASS：开场冻结的两Source、两候选补丁与W/gbs配置SHA全部一致，W/llvm HEAD、工作树状态与本机spec diff保持原样；新公开补丁SHA和上传commit一致。3个scope均结束，采样器与reader回收，本任务进程0、临时挂载0，两项目锁已释放，共享重任务锁按阶段finally释放。没有进入已交接x86树/BOLT工作树，没有修改宿主配置、旧Source/Commands/候选补丁或重新构建/打包；用户既有gbs配置改动保留不提交。证据E/final-audit.json、lock-released.json与各scope outcome/shared-lock-released。

本轮GitHub进度：e289e66（合入核对）、b940a01（新提交/apply/parse）、3b53b98（Gerrit上传回读）、813813b（快照/bash）；最终探测与本节同STATUS提交。Gerrit只有新评审356949，未执行356639 Abandon。

## 11. PS2 提交说明修订

2026-10-14，本节是本轮结果；§1–§10 保留 PS1 历史。只用 `git commit --amend` 修改 Gerrit PS1 的说明，未改代码、spec 或 Source，未构建、未转换，也未取得 heavy-stage 锁。唯一 Gerrit push 为 `HEAD:refs/for/tizen_base`，未提交合入、未打分、未操作其他 change。
证据 P=`temp/followup-356949-ps2-message-20261014`；34 组带原文件 SHA 和行号的原文见 `P/fact-excerpts.json`，结论见 `P/facts-summary.json`。未进入 BOLT 资产或已交接 x86 构建树。

### 11.1 前置检查与实际底稿

| 项目 | Gerrit PS1 实读 | 结果 |
|---|---|---|
| 状态/数量 | `NEW`；只有 patchset 1 | PASS |
| commit | `d4dd40da3b6ab28925b57d24d66bd992b4ad798c` | PASS |
| tree | `480be0836bc470dd027f73882b4082d0ce0e5000` | PASS |
| parent | `67619ec8bbbac7238a6cfc33a481ccfbcd12206f` | PASS |
| Change-Id | `I9a815cad07c9bd5ae1e3068fe5b13a339e2ea3ce` | PASS |

SSH 查询原文 `P/gerrit-before.jsonl`；从 Gerrit fetch PS1 到 P/review-work 后读取 commit object，而非假定本地说明就是远端。实际说明与原 `patches/archive-index-fix/followup/commit-message.txt` 同字节，保留段没有内容偏差。上传前又查询一次，仍为 NEW/仅 PS1。用户已有 `gbs_llvm.conf` 改动保留、不提交。

### 11.2 只读事实 1a–1f

**1a：发布 sed 的原文。** 以下行号以远端 PS1 `packaging/llvm.spec` 为准（P/ps1-llvm.spec 同字节）：

```text
192: %if 0%{llvm_release_build}
194: RELCFLAGS=$(echo $CFLAGS | sed -e 's*\(^\|[[:space:]]\)-g\([[:digit:]]\+\|gdb\|dwarf-[[:digit:]]\)\?* *g')
195: export CFLAGS=${RELCFLAGS}
196: RELCXXFLAGS=$(echo $CXXFLAGS | sed -e 's*\(^\|[[:space:]]\)-g\([[:digit:]]\+\|gdb\|dwarf-[[:digit:]]\)\?* *g')
197: export CXXFLAGS=${RELCXXFLAGS}
```

确认删除 `-g`、`-gN`、`-ggdb`、`-gdwarf-N`（此正则的 DWARF 版本只匹配一位数字，现值为 4）。它**没有尾部词边界**，不能泛化为安全删除任意 `-g*`：`-gline-tables-only` / `-grecord-gcc-switches` 会留下 `line-tables-only` / `record-gcc-switches`。本轮不改 sed。

**1b：结论①，当前认证配方的发布记录命令应为零 `-g`，未找到额外来源。** 此为指定配方/宏/工具的事实，不承诺未来任意 optflags，也不是发布模式完整构建认证。

| 核对项 | 原文及 file:line | 判定 |
|---|---|---|
| 分支 | PS1 spec:20–24：`%if %{defined _toolchain}` / `%define llvm_release_build 0`，else 为 `1` | 未定义时走去调试分支 |
| 构建类型 | PS1 spec:270/274/279：`-DCMAKE_BUILD_TYPE=Release` / `MinSizeRel` / `Release` | 三架构都不是 Debug/RelWithDebInfo |
| C/CXX/ASM 公共 flags | PS1 spec:256–258：`-DCMAKE_ASM_FLAGS="$CFLAGS"`、`-DCMAKE_C_FLAGS="$CFLAGS"`、`-DCMAKE_CXX_FLAGS="$CXXFLAGS"` | 取 sed 后变量；229–230 的 x86 追加项无 `-g` |
| 构建类型追加项 | 旧 archivefix-v2 的 build/CMakeCache.txt:394/430：`CMAKE_CXX_FLAGS_RELEASE:STRING=-O3 -DNDEBUG` / `CMAKE_C_FLAGS_RELEASE:STRING=-O3 -DNDEBUG`；391/427 为 `-Os -DNDEBUG` | 无 `-g`；Debug/RelWithDebInfo 的默认 flags 未被选择 |
| LLVM 选项 | 同 Cache:1288 `LLVM_ENABLE_ASSERTIONS:BOOL=No`；1384 `LLVM_ENABLE_MODULES:BOOL=OFF`；2148 `LLVM_USE_SANITIZER:STRING=`；2151 `LLVM_USE_SPLIT_DWARF:BOOL=OFF` | 未启用追加调试选项的条件 |
| LLVM 追加逻辑 | `llvm/llvm/cmake/modules/HandleLLVMOptions.cmake:719–722` 的 `-gmodules` 只在模块+Debug/RelWithDebInfo；965–974/997 的 `-gline-tables-only` 属 sanitizer 条件；1110–1116 的 `-gsplit-dwarf` 亦受构建类型约束 | 当前值不触发；完整 spec 无其他显式新增 `-g` |
| 原 optflags | `docs/37_target_recipe_policy_check.md:212`、保存的 `temp/release-x86-full-build-20261013/round2-resume-serial/original-rpm-build.sh:29–31`：`... -g2 -gdwarf-4 ... -frecord-gcc-switches ... -g` | 只有 `-g2/-gdwarf-4/-g`；`-frecord-` 不是 `-grecord-`；无上述 sed 残片形式 |
| clang 默认 | `docs/37_target_recipe_policy_check.md:299–301`：`clang.cfg` 只有 `-target x86_64-tizen-linux-gnu`、`-resource-dir /usr/lib64/clang/22`；`llvm/clang/lib/Driver/ToolChains/Clang.cpp:6076–6079`：`DebugInfoKind = ... NoDebugInfo`，4400–4406 根据 g_Group 修改 | 未发现 cfg 或 driver 默认加 `-g` |
| 已记录命令 | 各 `*-release-before.txt` 的调试 token 全集均为 `['-g', '-g2', '-gdwarf-4']`；`*-release-after.txt` 全集均 `[]` | 11,235 条零残留，不只是几个夹具 |

Cache 来自 docs/35 的旧 archivefix-v2 根（完整路径在 P/fact-excerpts.json），不是交接树。真实发布宏展开 `temp/archive-followup-review-20261014/release-isolated-rpmspec.stdout:183–187` 包含上述 sed；完整记录命令已覆盖 CMake 附加项。

**1c：11,235 是三架构已有 debug bitcode 的记录命令，不是发布模式新完整构建。** 原文 `docs/49_round4_revision_and_x86_build.md:58–64`：

```text
| x86_64 | 3,853 | 3,853 | 0 | dwarf=None，无调试选项 |
| armv7l | 3,683 | 3,683 | 0 | dwarf=None，无调试选项 |
| aarch64 | 3,699 | 3,699 | 0 | dwarf=None，无调试选项 |
合计11,235条；分类脚本 wall 9.669秒。**这只证明策略覆盖记录命令，不证明对应实物与直接编译等价。**
```

| 架构 | 原始构建范围 | 记录来源与追溯 |
|---|---|---|
| x86_64 | docs/35 构建原始 225 档中的 3,853 个 bitcode 成员 | E5/x86-input；`temp/arm-archive-stage1-20261010/anchor-metadata.json:2` 指向 docs/35 summary；后续 `temp/review-round3-continue-20261012/x86-production-conversion/members/**/ir-settings.json` 只重新读取这些记录，不是新编译 |
| armv7l | docs/40 §11 标准完整 `%build` 的 210 档，3,683 个 bitcode 成员 | `temp/arm-archive-standard-build-20261010/armv7l-ir-census/**` |
| aarch64 | docs/40 §12 标准完整 `%build` 的 212 档，3,699 个 bitcode 成员 | `temp/arm-archive-tls-thumb-20261010/aarch64-ir-census/**` |

三个 `temp/review-round4-continue-20261013/*-release-classified.json:3` 的 `evidence` 字段分别钉住上述来源；同目录 `release_static.py:9–27` 保存先精确 sed 再拆 token 的方法。原命令静态分类与下面“转换所生成的参数”不是一回事。

60 对每架构各 20（`docs/49_release_attribution.md:106–131` 的逐文件三列）。结果原文 :106 为 `{'PASS_ATTRIBUTED': 7, 'PASS_IDENTICAL': 53}`；:46 为“两路仅差 `-g -gdwarf-4`，其余参数及次序一致，clang实体SHA一致”。
归因原文 :48：“去debug后的debug bitcode按原发布命令（仅换输入/输出）再转换exit0……与发布产物对应函数节、节内重定位、函数及映射符号完全一致”；:162：“AArch64有6文件、19函数……均由后端路径(b)归因”。合计 ARM32 一个文件一个函数 + AArch64 六个文件十九函数。

**措辞收窄**：`PASS_IDENTICAL` 是十项 ELF 比较规则 PASS，不能写整个 `.o` 字节相同。`tools/check_release_debug_independence.py:119–145` 排除调试专用符号，:167–179 规范化节身份，:186–196 比较 header/alloc/重定位/符号/组/addrsig 而不比较 debug 路的 DWARF。PS2 改成“53 pairs matched under the ELF comparison rules, which exclude debug-only metadata and normalize section identities”。计数及归因不变。

**1d：工具版本比较是数字三元组。** 远端 PS1 Source、main 的 `tools/llvm_static_archives_source.py` 与 `6972188d` 中同名 tools Source 同字节，SHA `c43523c0ce04fc3310e670ff97823db8260c21250dc3172575a18db56500082e`。原文 :626–633：

```python
pattern = r'clang version (\d+\.\d+\.\d+)\b' if label == 'compiler' else r'LLVM version (\d+\.\d+\.\d+)\b'
match = re.search(pattern, text)
if label == 'compiler':
    if not match or int(match[1].split('.')[0]) != CERTIFIED_LLVM_MAJOR:
        raise ValueError('uncertified compiler major/full version (required 22): '+text.strip())
elif not match or match[1] != versions['compiler']['version']:
    raise ValueError(label+' version differs from clang '+versions['compiler']['version']+': '+text.strip())
```

clang 须可解析三段数字且主版本 22；llvm-dis/llvm-nm 须等于解析出的 `major.minor.patch`，不比较完整 raw/version/vendor 文本。使用用户提供的三元组措辞。

**1e：Known limitation 逐句核对；缺证据的绝对说法已收窄。**

| 句意 | 原文/证据与行号 | PS2 处置 |
|---|---|---|
| 两种 strip 均 sh_link=0 | docs/51:142 `5,799`；:195–196 “其同一5,799个表也全部sh_link=0”；:150–153 `before ... E 1004` → `after ... E 0` | 采纳为本次包内实测，不外推所有 strip 版本 |
| FILE 删除、重编号 | docs/51:144 “payload SHA全部未变，符号表已重新编号”；`llvm/llvm/lib/ObjCopy/ELF/ELFObjcopy.cpp:384–385`：`if (Config.StripDebug && Sym.Type == STT_FILE) return true;` | 保留删除/重编号与实测 payload 事实 |
| “strip不更新sh_link” | docs/51:206–207；`ELFObject.cpp:2591–2595` 原文 `If the .symtab indices have not been changed, restore the sh_link`，条件 `!Obj.SymbolTable->indicesChanged()`；:1133–1153 清开 symtab 链接 | 原提法易误读为保持旧有效链接；改成实测 `leave .llvm_addrsig with sh_link=0 and unchanged payload bytes`，不把 LLVM 源码机制冒充 GNU strip 源码证明 |
| compiler-rt 旧基线也如此 | docs/51:213 “compiler-rt的成员与docs/13基线同字节，故其中的失效也存在于旧基线” | 采纳；未转换运行库为既有证据 |
| GNU ld 不使用此节 | docs/51 没有 GNU ld 实现级原文；:168–172 有 GNU ld A/B/shared/GC 正确输出 | 删除“不使用”的普遍断言，改为 `The tested GNU ld links produce correct output.` |
| lld 忽略、保守标地址显著 | docs/51:204–205；`llvm/lld/ELF/InputFiles.cpp:791–804` 无有效 sh_link 时忽略；`Driver.cpp:2587–2611` 无 addrsig 时标记全部符号 | 采纳 |
| 普通测试输出正确 | docs/51:168 “O2输出与基线opt完全一致”；:169 “退出37”；:170–171 shared/GC 正确 | 保留限定 `tested` |
| safe ICF 警告、fatal 失败 | docs/51:183–185：GNU strip safe exit0/1057警告；两种 strip safe+fatal 均 exit1；:190–191 警告/错误原文 | 采纳；不称所有 lld 链接失败 |
| 换 llvm-strip 既非原因也非修复 | docs/51:196/213/215 支持问题此前已存在且该切换不修复；不证明任意环境中“绝非原因” | 标题仍为 not introduced；末句收窄成 `Switching to llvm-strip does not fix this`；后续独立 change |

LLVM 原文/SHA 见 docs/51 的 `*.source.txt`/`source-provenance.json`（f111162e），本轮未重做实验。

**1f：该全量构建用了带版本号的入口。** 不读取交接树，读取构建时已保存的证据副本：
`temp/release-x86-full-build-20261013/round2-eight-output-proof/ba-install-conversion-evidence/summary.json:3198216–3198223` 的 `tools.tool_versions.compiler`：

```json
"path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/clang-22",
"resolved_path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/clang-22",
"sha256": "7df0ff90dbca7f99ed6a642546281584dbfaab1528a94abf7a1bb524ca371b2c",
"version": "22.1.8"
```

因此按裁决在 Testing 第一段末追加规定的 alias 覆盖句。别名依据为 `docs/49_release_attribution.md:655` 的 `samefile=true`、`clang-alias.json` 的同 inode，以及 :643–648 两次全量转换输出相等；不冒充该完整构建实用无版本别名。debug 下 brp-strip 未执行的原文为 `docs/49_x86_build_resume_result.md:138`：“debug配置下brp-strip为0”；与 PS1 spec:6 `%{!?__debug_package:...}` 对应。

### 11.3 最终英文说明

保留的 Background、llvm-strip 条、Scope、原 Testing 第一段、Supersedes、Signed-off-by、Change-Id 逐词相同；只重新折行≤72字符，Testing 末尾加上述授权句。PS1 原有 73–74 字符行重新折行；1c/1e 收窄如上。

```text
packaging: refine x86_64 static archive handling

Background:
Change 356627 converts ThinLTO bitcode members in installed x86_64
static archives to native objects and rebuilds their indexes. This
avoids index damage from GNU strip and makes the archives usable by GNU
ld without LTO or an LLVM plugin.

Changes:
- Support release builds without _toolchain for recorded commands that
  carry no -g option. The release branch of this spec removes -g, -gN,
  -ggdb and -gdwarf-N from CFLAGS and CXXFLAGS to produce this form. For
  such commands, do not add -g or -gdwarf-4 during conversion; the
  merged version rejects them because it requires -gdwarf-4. Commands
  with other -g options must still have -gdwarf-4 as their last DWARF
  version option, as in the certified debug build, or they are rejected.
  Reject no-debug commands whose IR still contains a debug compile unit.
- Reject unsupported assembler options (-Wa, and -Xassembler), require
  the compiler to be LLVM 22 and llvm-dis and llvm-nm to report the same
  major.minor.patch version as the compiler, and check ELF section,
  symbol and relocation table bounds and strides. Allow only the
  certified iostream module-assembly declaration and verify that its
  undefined symbol is preserved after conversion. The recognizer handles
  the single-line module asm form printed by LLVM 22 llvm-dis, which the
  version check guarantees; it must also handle the multi-line form
  before that check allows a later LLVM version.
- Use the build/bin/clang alias instead of a hard-coded clang-22 path.
- Use llvm-strip for static archive post-processing, following the
  platform's move to LLVM. Override only the archive-strip argument in
  __strip_install_post; ordinary executable stripping keeps the platform
  default. Find-debuginfo and other enabled post-processing remain
  intact. The override copies tizen_macros:34-38 from
  rpm-build-4.14.1.1-1.4 and must be synchronized when the platform
  changes that macro. It covers all static archives in this package's
  buildroot, including compiler-rt.

Scope:
Only x86_64 is affected. The conversion also includes
libarcher_static.a. armv7l and aarch64 packaging are unchanged; ARM
support will be submitted separately. Final static archives contain no
DWARF after stripping.

Testing:
A full x86_64 build completed with one serial continuation in the
Tizen-Base-Toolchain tizen-base-toolchain_20261010.120615 environment.
All 225 development archives (3,864 ordered members) contain native
objects and complete indexes. Checks passed for all 45 compiler-rt
archives, including allocated section contents and symbol-to-member
mappings. Host and Tizen GNU ld (without LTO or plugins) and lld
consumers linked and ran successfully, including sanitizer, profile and
builtins probes. Independent reinstallation reproduced the converted
archives; a repeated converter invocation skipped the already-native
archives. The clang alias was verified by inode identity and
conversion-output equality rather than by that build, which still used
the versioned path.

Across 60 paired source samples (20 each for x86_64, armv7l and
aarch64), the generated release and debug conversion arguments differed
only by -g and -gdwarf-4. 53 pairs matched under the ELF comparison
rules, which exclude debug-only metadata and normalize section
identities. The other 7 were attributed to the backend's handling of
debug information by converting the debug bitcode again after removing
its debug information. This compares generated conversion arguments, not
recorded commands. Applying this spec's release flag substitution to the
11,235 commands recorded in the debug builds left no -g option in any of
them. A complete release-mode package build has not yet been run. The
tested build used the debug configuration, where __debug_package
suppresses the brp-strip line of the override, so that line has not been
executed.

The non-archive file comparison against an unpatched build in the same
environment has not yet been run. A comparison with the next official
snapshot is planned, with differences between the build environments
recorded; that comparison alone does not establish same-environment
equivalence.

Known limitation (not introduced by this change):
Stripping debug information from archive members removes STT_FILE
symbols and renumbers the symbol table. In the tested packaged archives,
both GNU strip and llvm-strip leave .llvm_addrsig with sh_link=0 and
unchanged payload bytes; compiler-rt archives, which are not converted,
have the same state in builds without these changes. The tested GNU ld
links produce correct output. lld ignores these sections and treats all
symbols as address-significant, so the tested lld links also produce
correct output. lld links using --icf=safe print warnings, and adding
--fatal-warnings makes them fail. Switching to llvm-strip does not fix
this; it will be addressed in a separate change.

Supersedes Change 356639.

Signed-off-by: FatTank <hao.lin@samsung.com>
Change-Id: I9a815cad07c9bd5ae1e3068fe5b13a339e2ea3ce
```

### 11.4 PS1→PS2 说明完整 diff

```diff
--- 356949-PS1/commit-message
+++ 356949-PS2/commit-message
@@ -1,34 +1,44 @@
 packaging: refine x86_64 static archive handling
 
 Background:
-Change 356627 converts ThinLTO bitcode members in installed x86_64 static
-archives to native objects and rebuilds their indexes. This avoids index
-damage from GNU strip and makes the archives usable by GNU ld without
-LTO or an LLVM plugin.
+Change 356627 converts ThinLTO bitcode members in installed x86_64
+static archives to native objects and rebuilds their indexes. This
+avoids index damage from GNU strip and makes the archives usable by GNU
+ld without LTO or an LLVM plugin.
 
 Changes:
-- Support release builds without _toolchain. When the recorded command
-  has no debug options, do not add -g or -gdwarf-4 during conversion.
-  The merged version rejects this case because it requires -gdwarf-4.
+- Support release builds without _toolchain for recorded commands that
+  carry no -g option. The release branch of this spec removes -g, -gN,
+  -ggdb and -gdwarf-N from CFLAGS and CXXFLAGS to produce this form. For
+  such commands, do not add -g or -gdwarf-4 during conversion; the
+  merged version rejects them because it requires -gdwarf-4. Commands
+  with other -g options must still have -gdwarf-4 as their last DWARF
+  version option, as in the certified debug build, or they are rejected.
   Reject no-debug commands whose IR still contains a debug compile unit.
 - Reject unsupported assembler options (-Wa, and -Xassembler), require
-  clang, llvm-dis and llvm-nm to have the same full LLVM 22 version, and
-  check ELF section, symbol and relocation table bounds and strides.
-  Allow only the certified iostream module-assembly declaration and
-  verify that its undefined symbol is preserved after conversion.
+  the compiler to be LLVM 22 and llvm-dis and llvm-nm to report the same
+  major.minor.patch version as the compiler, and check ELF section,
+  symbol and relocation table bounds and strides. Allow only the
+  certified iostream module-assembly declaration and verify that its
+  undefined symbol is preserved after conversion. The recognizer handles
+  the single-line module asm form printed by LLVM 22 llvm-dis, which the
+  version check guarantees; it must also handle the multi-line form
+  before that check allows a later LLVM version.
 - Use the build/bin/clang alias instead of a hard-coded clang-22 path.
 - Use llvm-strip for static archive post-processing, following the
   platform's move to LLVM. Override only the archive-strip argument in
   __strip_install_post; ordinary executable stripping keeps the platform
-  default. Find-debuginfo and other enabled post-processing remain intact.
-  The override copies tizen_macros:34-38 from rpm-build-4.14.1.1-1.4 and
-  must be synchronized when the platform changes that macro. It covers
-  all static archives in this package's buildroot, including compiler-rt.
+  default. Find-debuginfo and other enabled post-processing remain
+  intact. The override copies tizen_macros:34-38 from
+  rpm-build-4.14.1.1-1.4 and must be synchronized when the platform
+  changes that macro. It covers all static archives in this package's
+  buildroot, including compiler-rt.
 
 Scope:
-Only x86_64 is affected. The conversion also includes libarcher_static.a.
-armv7l and aarch64 packaging are unchanged; ARM support will be submitted
-separately. Final static archives contain no DWARF after stripping.
+Only x86_64 is affected. The conversion also includes
+libarcher_static.a. armv7l and aarch64 packaging are unchanged; ARM
+support will be submitted separately. Final static archives contain no
+DWARF after stripping.
 
 Testing:
 A full x86_64 build completed with one serial continuation in the
@@ -36,19 +46,45 @@
 All 225 development archives (3,864 ordered members) contain native
 objects and complete indexes. Checks passed for all 45 compiler-rt
 archives, including allocated section contents and symbol-to-member
-mappings. Host and Tizen GNU ld (without LTO or plugins) and lld consumers
-linked and ran successfully, including sanitizer, profile and builtins
-probes. Independent reinstallation reproduced the converted archives;
-a repeated converter invocation skipped the already-native archives.
+mappings. Host and Tizen GNU ld (without LTO or plugins) and lld
+consumers linked and ran successfully, including sanitizer, profile and
+builtins probes. Independent reinstallation reproduced the converted
+archives; a repeated converter invocation skipped the already-native
+archives. The clang alias was verified by inode identity and
+conversion-output equality rather than by that build, which still used
+the versioned path.
 
-Across 60 paired x86_64, armv7l and aarch64 source samples, release/debug
-conversion arguments differed only by the debug options. Differences in
-object output were attributed to compiler debug-information handling.
-A complete release-mode package build is still pending.
+Across 60 paired source samples (20 each for x86_64, armv7l and
+aarch64), the generated release and debug conversion arguments differed
+only by -g and -gdwarf-4. 53 pairs matched under the ELF comparison
+rules, which exclude debug-only metadata and normalize section
+identities. The other 7 were attributed to the backend's handling of
+debug information by converting the debug bitcode again after removing
+its debug information. This compares generated conversion arguments, not
+recorded commands. Applying this spec's release flag substitution to the
+11,235 commands recorded in the debug builds left no -g option in any of
+them. A complete release-mode package build has not yet been run. The
+tested build used the debug configuration, where __debug_package
+suppresses the brp-strip line of the override, so that line has not been
+executed.
 
 The non-archive file comparison against an unpatched build in the same
-environment has not yet been run; it will be checked using the next
-official snapshot.
+environment has not yet been run. A comparison with the next official
+snapshot is planned, with differences between the build environments
+recorded; that comparison alone does not establish same-environment
+equivalence.
+
+Known limitation (not introduced by this change):
+Stripping debug information from archive members removes STT_FILE
+symbols and renumbers the symbol table. In the tested packaged archives,
+both GNU strip and llvm-strip leave .llvm_addrsig with sh_link=0 and
+unchanged payload bytes; compiler-rt archives, which are not converted,
+have the same state in builds without these changes. The tested GNU ld
+links produce correct output. lld ignores these sections and treats all
+symbols as address-significant, so the tested lld links also produce
+correct output. lld links using --icf=safe print warnings, and adding
+--fatal-warnings makes them fail. Switching to llvm-strip does not fix
+this; it will be addressed in a separate change.
 
 Supersedes Change 356639.
 
```

### 11.5 远端回读与补丁正文

| 项目 | 结果 |
|---|---|
| PS2 commit | `a18ce53708d3b6ef596dcd27d0b51e18ce1db282` |
| tree / parent | `480be0836bc470dd027f73882b4082d0ce0e5000` / `67619ec8bbbac7238a6cfc33a481ccfbcd12206f`，均与 PS1 相同 |
| Change-Id | `I9a815cad07c9bd5ae1e3068fe5b13a339e2ea3ce`，不变 |
| Gerrit | [356949 PS2](https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/356949/2)，`NEW`，`kind=NO_CODE_CHANGE` |
| fetch | `refs/changes/49/356949/2`，commit/tree/parent/Change-Id 与本地相同，message 同字节 |
| 唯一 push | 1 次，用户授权的 `HEAD:refs/for/tizen_base`；回读时间 `2026-10-14T20:15:11.283881+08:00` |
| 说明 SHA256 | `e452b9ff4ed02254fc2eb813e3b05251c539fbb90bc4fffd18fe8d5fd6887157` |
| PS1 patch SHA256（历史保留） | `437f128a668b6e38cfed582c44e8ec48dec52144f68b1aa4126f496f384087ff` |
| PS2 patch SHA256 | `23a4cfa1eb1e602459f3b3ae39096ec2cc2458679164c23407e0dc394ee23d76` |
| diff 正文 SHA256 | `f5310a84d19a84b878cedfb805177c9c121688dac973222e8669f9661e239011`，新旧同字节 |

`P/amend-check.json`、`P/upload-result.json`、`P/post-push-query.stdout` 与 `P/fetch-ps2.*` 保存原始检查。新旧 format-patch 从 `diff --git` 至结尾完全相同；从说明结束的 `---` 起（diffstat/正文/Git版本尾注）也完全相同。封装的 `From <commit>` 随 amend 更新，作者/作者时间/标题相同，除提交说明及 commit 身份封装外无差异。`git diff PS1 PS2` 为空，Source/spec 的树内容不变。

### 11.6 评审采纳表

| 意见/来源 | 最终处置 |
|---|---|
| addrsig 已知限制（三家） | 采纳；加入实测边界、两 strip 均失败的 ICF 条件；机制/GNU ld 普遍断言按证据收窄 |
| 发布支持收窄（Claude Code P5-1、Codex R1） | 采纳；限定零-g，说明现 sed 与其他-g仍要求末项DWARF4，no-debug/IR矛盾拒绝 |
| brp-strip 行未执行（Claude Code P5-7） | 采纳；不以 debug 构建证明该行执行 |
| 快照口径（Codex R4） | 采纳；未来官方跨环境对照不等于同环境未打补丁对照 |
| 版本门禁（Claude Code P5-2） | 采纳；解析的 major.minor.patch，不是 raw 字符串 |
| 60对（Claude Code P5-6） | 采纳；每架构20，53为规定ELF比较同等，7为后端归因；生成参数与记录命令区分 |
| module asm 单行（Claude Code P5-3） | 采纳；LLVM22打印格式与版本门禁边界；放行新主版本前先支持多行 |
| alias 覆盖（Claude Code P3-6/P5-5） | 采纳；全量构建 clang-22，明确别名仅同inode/输出相等证据 |

### 11.7 代码边界与推迟项（本次不改）

已记录的真实命令只有 `-g/-g2/-gdwarf-4`，未触发以下两种调试开关边界。Source:258–270 按是否出现调试 token 与末个 DWARF 选项判定，:358–361 由 dwarf 是否为 None 选择后端参数。重定位 Source:397–411 **已检查 sh_link/sh_info 索引范围**，但未校验 sh_link 指向节的类型及 sh_info 的完整语义；不能写成“完全不检查 sh_info”。

| 推迟项 | 现状与后续归属 |
|---|---|
| `-gdwarf-4` 后出现 `-g0` | 仍按调试处理；ARM 补丁处理并带 x86 回归 |
| 只有 `-gdwarf-4` 没有 `-g` | 当前仍补 `-g`；ARM 补丁处理并带 x86 回归 |
| relocation sh_link 类型/sh_info 语义 | 上述范围检查之外的加固；ARM 补丁并带 x86 回归 |
| dbg.cu 对称门禁 | no-debug命令含debug CU的现有拒绝已在Source；更完整对称策略去ARM补丁并带x86回归 |
| BACKEND_FLAGS 元组、错误信息、符号从白名单派生 | ARM补丁并带x86回归 |
| tizen_macros 漂移检查 | ARM补丁并带x86回归；此次保留同步平台宏的说明 |
| 多行 module asm 解析 | ARM补丁并带x86回归；升级LLVM主版本闸门前完成 |
| addrsig 修复 | 独立change；先做 `llvm-strip -g --keep-file-symbols` 探针，备选strip后删除该节；扫描Tizen中`--icf=safe --fatal-warnings`使用，新增sh_link状态回归测试；本轮未运行/未许诺探针必有效 |
| 发布模式完整打包 | 正式启用发布模式前完成；60对认证不能代替 |

无产品门禁停止点。主库只更新本节、STATUS、followup说明/封装；Source/spec/冻结补丁不改，用户gbs修改保留；无构建/采样器/挂载/heavy锁。
