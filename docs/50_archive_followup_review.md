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
