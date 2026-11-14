# 86：claims全路径、入口同步、BOLT告警与profile追溯

**结论：部分完成，需后续任务处理三个STOP。** 步骤1有效PIC条件复核通过并补句；步骤2只同步了获授权的5个文件，完整清单失败后停止，未测试；步骤3已统计日志并完成22组定向反汇编，源码归因遇到缺失旧提交后停止；步骤4完成830追溯，单条警告PID仍UNKNOWN；步骤5草案生成脚本断言失败，未修正重跑。没有构建、运行llvm-bolt或访问QB/Gerrit，没有修改LLVM提交/分支，没有删除文件。

PM已明确：85步骤5 STOP正确，原先要求整个类型条件相等是 **PM前提错误**；fea有意新增12/14。本次不计作准备错误，不覆盖85原始停止记录。

|步骤|结果|完成边界|
|---|---|---|
|1 claims|PASS|192个合法ELF组合及全部调用点；补充PS10对照|
|2 W入口|STOP|5文件SHA一致；完整SHA256SUMS失败；测试/dry-run NOT RUN|
|3 BOLT告警|STOP|日志、22组函数+后续符号反汇编完成；源码可达性/明细归因未完成|
|4 830追溯|PASS_WITH_UNKNOWN|A构建830、B训练0；合并23个输入均为B专用profile；单条PID未知|
|5 资源报备|STOP|生成脚本argv切片错误；未生成经核对的报备草案|
|6 交付|完成报告与证据发布|所有STOP原文保留，未把未完成项标PASS|

## 1. 读取范围与执行边界

B=/home/linhao/Toolchain/development/llvm-optimize-bolt（bolt-v4）；W=/home/linhao/Toolchain/development/llvm-optimize。本轮新增证据为[完整raw索引](../../tools/bolt/results/night-86-20261114/RAW_LINKS.md)。

已读：85停点/STATUS/82入口记录；PS10及fea转换器git对象；两版本全部pic_relocations、ir_settings及process调用；82对应5文件；74 T/D rewrite与主构建日志、79保存的QB1226850/1主构建日志、58/59的BOLT实验日志；74两份保全输入和59的PGO输入；58 A/B/C日志/命令/profile清单、相应历史脚本与保全profile。步骤5读74 D原始BOLT argv，未运行它。

未读/未完成：未访问QB网站或Gerrit；未重新比较RPM/执行归档转换；未跑真实入口/完整构建；未运行BOLT；未补采profile或重新合并。步骤3只成功保存了一份fea AArch64源码，旧3ee对象读取失败后停止，未完成源码路径证明；QB内部rewrite日志未在已保存材料中找到，不能用主日志0次命中代替内部日志无警告。

所有采集、分析、同步及交付命令均在串行用户服务下：MemoryMax=4G、MemorySwapMax=0、Nice=19、IOSchedulingClass=idle；工具使用74对应根的loader和运行库，无宿主反汇编器。未发生本轮OOM/超时。每条服务的结束行由退出trap输出。只写B及授权的W五文件；历史结果不覆盖。

## 2. claims全路径：有效PIC条件等价

[完整审计](../../tools/bolt/results/night-86-20261114/claims-path-review.md)；
[PS10全路径原文](../../tools/bolt/results/night-86-20261114/ps10-full-paths.txt)；
[fea全路径原文](../../tools/bolt/results/night-86-20261114/fea-full-paths.txt)；
[192组合JSON](../../tools/bolt/results/night-86-20261114/pic-path-matrix.json)。

|条件|PS10|fea0fe46|结论|
|---|---|---|---|
|REL/RELA|364–365|500–501|只遍历SHT_RELA=4、SHT_REL=9|
|目标SHF_ALLOC|366–368外层节循环|529–530逐记录|均排除非ALLOC目标；重定位节自身ALLOC/WRITE不作PIC过滤|
|SHN_ABS|376|533|符号绝对索引不进入forbidden|
|32/32S|376 kind10/11|533 kind10/11|ALLOC且非绝对符号即禁止，WRITE不豁免|
|64|376 kind1|533 kind1|还要求目标非WRITE|
|8/16新增|无|533 kind12/14|本系列新增，不称整条条件相同|
|PIC来源|324–326|354–356|PIC/PIE值0/1/2及组合检查|
|原生成员|652–658|850–856|记录forbidden，不因列表非空触发PIC门禁|
|转换成员|670–673|868–871|pic_level非零且forbidden非空，报non-PIC relocation|

用两版原函数对192个合法内存ELF组合逐个比较，checked/forbidden相同：kind∈{1,10,11} × 目标标志4种 × 重定位节标志4种 × 符号SHN_ABS/普通 × REL/RELA。调用点pic_level=0/1/2和原生分支也按原代码核对。未编译任何夹具。

**不能扩大成解析器整体等价。** fea495–496显式拒绝CREL，522–523拒绝宽度表外类型，表结构/索引/字段范围/压缩目标声明大小的检查在非ALLOC过滤之前。PS10对某些畸形或非ALLOC输入会跳过，而fea可能先报解析错误。对于合法输入的32/32S/64 PIC政策，有效条件等价；句4保留既有检查的描述准确。原生成员仍可能因解析错误拒绝，不能说原生成员“永不报错”。

已在[claims文档](../../tools/bolt/results/qb-1226850-1226851/commit-message-drafts/0003-claims-to-code.md)句4后加文末对照指引，并在历史对照末尾加用户规定段落；旧文字不改。PS10实际行号376。[新增diff](../../tools/bolt/results/night-86-20261114/claims-addition.diff)，[旧文副本](../../tools/bolt/results/night-86-20261114/claims-before.md)。因为PIC有效路径等价，本次没有触发“不等价时检索真实forbidden命中”的分支，也未重扫实物归档。

## 3. 入口同步：五文件完成，完整校验STOP

覆盖前备份及SHA在[entry-before-manifest.json](../../tools/bolt/results/night-86-20261114/entry-before-manifest.json)，原文件副本均保留在entry-before/。覆盖只涉及run-night.sh、test_serial.py、basedev/launcher.py、README.md、SHA256SUMS。

[结果JSON](../../tools/bolt/results/night-86-20261114/step2-result.json)中五个after SHA全部等于B；但运行W顶层sha256sum -c退出1：

    basedev/SHA256SUMS: FAILED
    basedev/provenance.json: FAILED
    provenance.json: FAILED open or read

[stdout原文](../../tools/bolt/results/night-86-20261114/entry-sha-check.stdout)；
[stderr原文](../../tools/bolt/results/night-86-20261114/entry-sha-check.stderr)。

这三项不在本任务授权W覆盖的五文件内。**保留现场，不回滚、不扩大同步范围、不重试。** 82的30项测试和dry-run本轮均NOT RUN，不能沿用B上次30/30称本轮通过。下一步需PM授权处理上述额外文件并重新验证；本轮没有写它们。

## 4. BOLT告警：产品与PGO必须分开

[逐文件SHA、行号、原文](../../tools/bolt/results/night-86-20261114/bolt-warning-lines.json)。

|来源|Failed to analyze行数/所报relocation数|jump past end行数|可见性|
|---|---|---:|---|
|74本地T rewrite|1 / 2804|10|原始内部日志|
|74本地D rewrite|1 / 2804|10|原始内部日志|
|74 T/D主构建日志|各0次命中|各0|内部rewrite未在主日志展开|
|QB1226850/1226851保存主日志|各0次命中|各0|内部BOLT日志UNKNOWN，不下“无告警”结论|
|58 PGO输入+旧profile rewrite|1 / 1551|2|原始实验日志|
|59 PGO插桩|1 / 1551|2|原始实验日志|
|59 PGO新profile优化|1 / 1551|2|原始实验日志|

1551/2804是单条汇总中的数量，不是读取到了1551/2804条明细。两处PGO警告确实也出现在已上传tree的本地T/D产品路径中，此外产品还有8个告警位置。本次不称其“无害”，也不把产品与PGO计数混合。

### 定向反汇编已完成的事实

[输入、工具SHA与完整argv](../../tools/bolt/results/night-86-20261114/disassembly-result.json)。T/D分别用74对应根的llvm-objdump及自身loader；PGO原D根已删除，对保全PGO输入使用74 T根平台llvm-objdump及其loader只读反汇编（不是原PGO构建工具身份认证）。每次只反汇编告警函数与其后一个函数符号，没有运行BOLT。

74输入大小/SHA与83一致：T226816920B / ae3d837d862673b03c3c4718f6746f6986d8abe2078bad426b97905258b91a5c；D226782848B / bf15cf062439714651809cd3b5ca82619407081adca64ceb65699e6ccae50501。三份输入均为保全的带重定位、无.debug/.zdebug的ELF；PGO本次身份在JSON中列出，旧身份未完成额外对照，不混作产品认证。

以下表仅复述已保存的反汇编和符号边界，源码可达性全部UNKNOWN（下述STOP发生在源码历史对照阶段）：
|输入|函数|告警指令地址|符号end|下一函数地址|可达性|
|---|---|---|---|---|---|
|toolchain|convertToThreeAddressWithLEA|0x27f0b69|0x27f2c7e|0x27f2c80|UNKNOWN|
|toolchain|convertToThreeAddress|0x27f3576|0x27f51c8|0x27f51d0|UNKNOWN|
|toolchain|LoadStoreMultipleOpti|0x2d00cbb|0x2d023a2|0x2d023b0|UNKNOWN|
|toolchain|isBranchOffsetInRange|0x2f1ea1e|0x2f1ea8b|0x2f1ea90|UNKNOWN|
|toolchain|getBranchDestBlock|0x2f1ead8|0x2f1eaf3|0x2f1eb00|UNKNOWN|
|toolchain|analyzeBranch|0x2f1f785|0x2f1f96c|0x2f1f970|UNKNOWN|
|toolchain|parseCondBranch|0x2f1fc15|0x2f2064e|0x2f20650|UNKNOWN|
|toolchain|runOnMachineFunction|0x3095780|0x30959ce|0x30959d0|UNKNOWN|
|toolchain|parsedAttrToRetainOwnershipKind|0x6cb9dc7|0x6cb9dca|0x6cb9dd0|UNKNOWN|
|toolchain|handleXReturnsXRetainedAttr|0x6cba1d6|0x6cbaeeb|0x6cbaef0|UNKNOWN|
|basedev|convertToThreeAddressWithLEA|0x27f0b69|0x27f2c7e|0x27f2c80|UNKNOWN|
|basedev|convertToThreeAddress|0x27f3576|0x27f51c8|0x27f51d0|UNKNOWN|
|basedev|LoadStoreMultipleOpti|0x2d00c5b|0x2d02342|0x2d02350|UNKNOWN|
|basedev|isBranchOffsetInRange|0x2f1e9be|0x2f1ea2b|0x2f1ea30|UNKNOWN|
|basedev|getBranchDestBlock|0x2f1ea78|0x2f1ea93|0x2f1eaa0|UNKNOWN|
|basedev|analyzeBranch|0x2f1f725|0x2f1f90c|0x2f1f910|UNKNOWN|
|basedev|parseCondBranch|0x2f1fbb5|0x2f205ee|0x2f205f0|UNKNOWN|
|basedev|runOnMachineFunction|0x3095740|0x309598e|0x3095990|UNKNOWN|
|basedev|parsedAttrToRetainOwnershipKind|0x6cb9d17|0x6cb9d1a|0x6cb9d20|UNKNOWN|
|basedev|handleXReturnsXRetainedAttr|0x6cba126|0x6cbae3b|0x6cbae40|UNKNOWN|
|pgo|getBranchDestBlock|0x3ee314a|0x3ee315a|0x3ee3160|UNKNOWN|
|pgo|convertToThreeAddressWithLEA|0x4a05080|0x4a0581a|0x4a05820|UNKNOWN|

例如PGO getBranchDestBlock：0x3ee314a的jae指向0x3ee315a，等于该函数符号end；PGO convertToThreeAddressWithLEA：0x4a05080的jae指向0x4a0581a，等于符号end。产品T对应目的地址是0x2f1eaf3和0x27f2c7e。原文含函数后padding和下一符号，不能仅由落在end就证明源码路径不可达。未完成llvm_unreachable与调用不变量证明，也未读取BOLT后最终指令作因果推断。

### 步骤3 STOP原文

    fatal: invalid object name '3ee2d847'.

读取命令：

    git -C /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106/source show 3ee2d847:llvm/lib/Target/AArch64/AArch64InstrInfo.cpp

返回128；脚本随后CalledProcessError。只保存了此前fea该源码文件；未fetch、未换仓库重试、未继续源码归因。其余source reachability与1551按类型/节/符号聚合NOT RUN，不能声称已证明缺少某个细节开关。后续需先只读定位可用旧源码对象，再核实BOLT诊断开关；可能需要额外-v/print诊断及约10GB进程预算，但本轮没有确认某开关必能给出所需明细。[STOP记录](../../tools/bolt/results/night-86-20261114/step3-result.json)。

## 5. 830追溯：合并输入明确，PID不完整

[步骤4结果](../../tools/bolt/results/night-86-20261114/step4-result.json)；
[830行原文](../../tools/bolt/results/night-86-20261114/counter-warning-lines.json)；
[84个连续告警段及Ninja上下文](../../tools/bolt/results/night-86-20261114/counter-warning-groups.json)；
[tblgen进程采样](../../tools/bolt/results/night-86-20261114/A-tblgen-process-records.json)。

- **已证明**：830条都在58号A构建stdout，首行为L1084；B训练另阶段独立记录，不是这830条的来源。A采样保存161条含tblgen的命令记录，告警附近Ninja目标是IntrinsicsNVPTX.h、ARM/AArch64/BPF生成表、Options.inc等。
- **UNKNOWN**：每条告警没有PID/命令标签，不能把邻近Ninja进度行武断对应成精确进程，也不能称830个独立进程。构建期生成工具的归属有上下文支持，但未完成逐警告PID证明。
- **已证明**：23次clang训练的stdout/stderr全部0条此告警，见[逐训练输出核对](../../tools/bolt/results/night-86-20261114/training-warning-audit.json)；这只覆盖本次训练，不保证其他负载不会耗尽。
- **已证明**：C显式合并的23个profraw都对应B的0–22号LLVM_PROFILE_FILE模式，大小/SHA与保存清单及现存保全文件逐一一致；合并结果52,528,216B，SHA256 8c60fb561f4a445d1456da90cf7552a79a31abcbf3aab44f28710ad66dee1805。
- A启动是env -i，未设置指向B目录的LLVM_PROFILE_FILE；B在A结束后通过profiles.mkdir()创建专用目录（不是exist_ok复用），每条训练独立设定i-%m-%p；C只合并该目录显式列表。因此A构建期产生的profraw未进入这一合并清单。**A各工具默认profile的实际路径/内容仍UNKNOWN**，未保存的旧A根不重建。
- driver.py、train.py、common.py的当前SHA与58号script-identities原记录全部相同，才能将这段流程作为历史证据；没有运行它们。

[23文件与合并命令身份链](../../tools/bolt/results/night-86-20261114/merge-input-trace.json)；
[带行号的目录隔离逻辑](../../tools/bolt/results/night-86-20261114/profile-path-separation.txt)。本轮没有重新采集或合并，不把“未进入当前profile”解释成耗尽告警无需调查。

## 6. 资源报备生成STOP

原始错误：

    File ".../night-86-20261114/step5.py", line 14, in <module>
        assert options[0].startswith('-data=')
    AssertionError

原因：准备脚本从保存argv的第5项开始截取，而-data=位于第4项。不是产品失败。按本任务“规定外STOP”保留脚本，不修正重跑。[完整STOP](../../tools/bolt/results/night-86-20261114/step5-result.json)。

report-stale身份读取在内存中进行，但尚未写成经核对的结果；命令草案、采集diff草案、本次df差额和清理候选表均未生成，**NOT RUN**。新目录里step5.py后部有未执行的候选文案，不作为已完成或已批准的报备稿。本任务没有运行report-stale，没有创建其输出目录，也未修改入口采集逻辑。85的历史目录大小仍可由85索引读取，但本报告不把旧df称为当前空间。

## 7. 交付、STOP与后续

1. 步骤2需新授权补齐清单涉及的额外入口元数据，再跑30项/dry-run；此时W保留5文件已同步的现场。
2. 步骤3需PM安排只读定位旧源码对象，继续可达性与relocation细分；已有日志和22组定向反汇编无需丢弃。
3. 步骤5需允许修正argv准备错误后生成报备草案；本轮不自行重跑。
4. claims补句完成；85原文和“PM前提错误”解释同时保留。第一批产品代码/提交、评审状态均未改变。

全部本次文件见[raw链接索引](../../tools/bolt/results/night-86-20261114/RAW_LINKS.md)。单文件≤10MB，报告≤30KB；已有证据不覆盖，W备份完整保留。

86步骤1 已结束 2026-11-14T15:18:52.130907+08:00 status=PASS

86步骤2 已结束 2026-11-14T15:19:17.797410+08:00 status=STOP

86步骤3 已结束 2026-11-14T15:22:22.918739+08:00 status=STOP

86步骤4 已结束 2026-11-14T15:23:57.001311+08:00 status=PASS_WITH_UNKNOWN

86步骤5 已结束 2026-11-14T15:29:20+08:00 status=STOP

