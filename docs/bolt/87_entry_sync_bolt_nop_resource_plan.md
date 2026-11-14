# 87：入口同步、产品路径BOLT告警与资源报备草案

**结论：步骤1 STOP；步骤2完成只读分析（2处A级、8处B级，不能称全部逐条证明）；步骤3草案完成，但现有BOLT工具无法输出逐条重定位诊断。未构建、未运行llvm-bolt、未访问QB/Gerrit、未改LLVM、未删除文件。**

PM定性：86号三个STOP都是准备或清单问题，不是产品失败。86步骤3、5的获批修正不计准备错误次数。本次步骤1另遇受限服务缺少rg，按“任何失败即STOP”停止，未作同步或测试。旧证据全部保留。

## 1. 入口步骤STOP（W未写入）

第一次只读准备命令在读取入口差异前退出：

    /bin/sh: 7: rg: not found
    已结束 2026-11-14T16:00:28+08:00 status=127 unit=llvm-audit87-20261114-001

原文：[step1-stop.txt](../../tools/bolt/results/night-87-20261114/step1-stop.txt)。未完成W/B完整diff、未备份/复制新增清单文件、未运行两级sha256sum -c、30项测试及dry-run。没有回滚86已同步的五文件。82在B的30/30历史结果不能代替W本次测试。
PM说明的三个漏项（basedev/SHA256SUMS、basedev/provenance.json、顶层provenance.json）作为本次授权依据记录，未冒充本轮已复核或已同步。入口仍不能宣称完成部署。

## 2. BOLT源码：触发条件和替换行为

只读git对象fea0fe464d56e17f2c7588c557bfffd9f6ac352b。未读取3ee2d847，也未fetch。完整源码保存于source/，行号对应原文件，不是文档行号。

### 2.1 jump-past-end

[BinaryFunction.cpp](../../tools/bolt/results/night-87-20261114/source/bolt_lib_Core_BinaryFunction.cpp) L1391–1431：

- 已反汇编指令被识别为branch或call，并且evaluateBranch能解析目标。
- 递归调用到函数入口有单独路径；本告警位于目标不在containsAddress范围内的外部目标分支。
- TargetAddress恰等于getAddress()+getSize()，且小于getAddress()+getMaxSize()。
- 排除AArch64 veneer匹配；本次输入ELF为x86_64，函数名称中AArch64不改变ELF架构。
- 源码注释是“Result of __builtin_unreachable().”；随后createNoop替换MC指令。
- 若原指令为条件跳转，将(Offset, Offset+Size)加入IgnoredBranches，用于profile validation；无条件跳转不加入此表。
- goto add_instruction跳过后续外部引用处理/TakenBranches登记及replaceBranchTarget。源码注释不等于任意输入的可达性证明。

关键原文：

~~~cpp
if (TargetAddress == getAddress() + getSize() &&
    TargetAddress < getAddress() + getMaxSize() &&
    !(BC.isAArch64() &&
      BC.handleAArch64Veneer(TargetAddress, /*MatchOnly*/ true))) {
  // Result of __builtin_unreachable().
  errs() << "BOLT-WARNING: jump past end detected at 0x"
         << Twine::utohexstr(AbsoluteInstrAddr) << " in function "
         << *this << " : replacing with nop.\n";
  BC.MIB->createNoop(Instruction);
  if (IsCondBranch) {
    // Register branch offset for profile validation.
    IgnoredBranches.emplace_back(Offset, Offset + Size);
  }
  goto add_instruction;
}
~~~

### 2.2 relocation计数与开关

[RewriteInstance.cpp](../../tools/bolt/results/night-87-20261114/source/bolt_lib_Rewrite_RewriteInstance.cpp)：
L2659–2675输出NumFailedRelocations汇总；L2911–2918仅在analyzeRelocation返回false时递增。
该函数L2479–2480唯一false路径是!Relocation::isSupported(RType)。其余支持类型的值一致性有assert，不计为这里的false。
[Relocation.cpp](../../tools/bolt/results/night-87-20261114/source/bolt_lib_Core_Relocation.cpp) L33–54列x86支持类型，L719–729按架构分派。

筛选链完整原文在RewriteInstance.cpp L2829–2903：重定位节自身非ALLOC；目标节ALLOC；排除.plt/.rela.plt/.got.plt/.eh_frame/.gcc_except_table；skipRelocationType；x86 converted-bit归一化；x86 TLS跳过；已有动态重定位地址跳过。2804是经这些筛选后不支持的记录数，不是全部ELF重定位数，也不能凭汇总定位具体类型或符号。

L2913–2916逐条offset/type-name输出包在LLVM_DEBUG中，L2830–2845可打印重定位节和目标节上下文；DEBUG_TYPE为L69的“bolt”。对应开关为-debug-only=bolt，**前提是工具编入LLVM_DEBUG支持**。失败分支尚未取得SymbolName，符号归属仍需原ELF交叉映射。

[Debug.h](../../tools/bolt/results/night-87-20261114/source/llvm_include_llvm_Support_Debug.h) L37及NDEBUG分支、[Debug.cpp](../../tools/bolt/results/night-87-20261114/source/llvm_lib_Support_Debug.cpp) L120之后表明NDEBUG会去掉这些功能。74 T/D实际RewriteInstance.cpp编译参数都有-DNDEBUG：
[toolchain-exact-bolt-flags.txt](../../tools/bolt/results/night-87-20261114/toolchain-exact-bolt-flags.txt)；[basedev-exact-bolt-flags.txt](../../tools/bolt/results/night-87-20261114/basedev-exact-bolt-flags.txt)。
因此不能把-v=1或-print-*当成既有工具的替代开关，也不能承诺现有工具加-debug-only就有明细。本轮未运行--help或BOLT。

## 3. 产品10处逐项归因

复用86已保存的完整函数及后续符号反汇编（本次没有新运行平台工具），核对其输入SHA与74记录：T ae3d837d862673b03c3c4718f6746f6986d8abe2078bad426b97905258b91a5c；D bf15cf062439714651809cd3b5ca82619407081adca64ceb65699e6ccae50501。

T/D各10处：去ThinLTO数字后缀后函数名一一对应，告警种类、相对函数起点的跳转偏移相同，目标均等于函数end。不是所有原始名字完全相同：AArch64CondBrTuning的.llvm数字后缀不同。前两处甚至绝对地址也相同，其余有位移。完整记录：[function-attribution.json](../../tools/bolt/results/night-87-20261114/function-attribution.json)；源码摘录：[function-source-excerpts.txt](../../tools/bolt/results/night-87-20261114/function-source-excerpts.txt)。

A＝源码、指令及生成枚举可逐项对应；该跳转只有违反unreachable前提才会执行。B＝结构相符，但未逐条映射；不能写成已经证明不可达。UNKNOWN＝无法对应。本轮A2、B8、UNKNOWN0；B保留不确定性。

|序号/函数|T跳转→end|D跳转→end|级别|源码结构与局限|
|---|---|---|---|---|
|1 X86 convertToThreeAddressWithLEA|0x27f0b69→0x27f2c7e|0x27f0b69→0x27f2c7e|B|MIOpc穷举switch，default为llvm_unreachable；告警前bit-test失败后jae到函数end。未把全部opcode编号/优化分支逐一复原。（llvm_lib_Target_X86_X86InstrInfo.cpp L1219–1337）|
|2 X86 convertToThreeAddress|0x27f3576→0x27f51c8|0x27f3576→0x27f51c8|B|convertToThreeAddress主switch default为llvm_unreachable；bit-test的jb未取后无条件jmp到end。多个内联/子switch共享末尾，尚未完成逐条映射。（llvm_lib_Target_X86_X86InstrInfo.cpp L1409–1670）|
|3 ARM LoadStoreMultipleOpti|0x2d00cbb→0x2d023a2|0x2d00c5b→0x2d02342|B|候选内联getUpdatingLSMultipleOpcode的opcode/default不可达；0x7d7=STMDA，0x55选中STMDA/STMDB/STMIA/STMIB。Mode随后表查，结构相符；内联调用链未完整逐条证明。（llvm_lib_Target_ARM_ARMLoadStoreOptimizer.cpp L1118–1183）|
|4 AArch64 isBranchOffsetInRange|0x2f1ea1e→0x2f1ea8b|0x2f1e9be→0x2f1ea2b|A|getBranchDisplacementBits内联：488..493、2180..2183、B=1887、Bcc=2107已分流；7881/7882/7899/7900由0xc0003位图识别。告警jae只在不属于该TBZ/TBNZ集合时取，合法枚举路径不会取。（llvm_lib_Target_AArch64_AArch64InstrInfo.cpp L270–304）|
|5 AArch64 getBranchDestBlock|0x2f1ead8→0x2f1eaf3|0x2f1ea78→0x2f1ea93|A|同一opcode分流：488..493取operand3，2180..2183取operand1；B取operand0，Bcc取operand1；TBZ/TBNZ位图成功取operand2。失败jae跳end对应default llvm_unreachable。（llvm_lib_Target_AArch64_AArch64InstrInfo.cpp L306–332）|
|6 AArch64 analyzeBranch|0x2f1f785→0x2f1f96c|0x2f1f725→0x2f1f90c|B|analyzeBranch中含parseCondBranch及getBranchDestBlock调用；0xc0003与7881偏移对应TBZ/TBNZ分类，失败跳end。无法在无DWARF的内联体中唯一定位是哪一次调用。（llvm_lib_Target_AArch64_AArch64InstrInfo.cpp L406–500）|
|7 parseCondBranch|0x2f1fc15→0x2f2064e|0x2f1fbb5→0x2f205ee|B|parseCondBranch default llvm_unreachable；同一TBZ/TBNZ位图，成功后读取operand2，失败跳end。未逐个复原全部入口分支。（llvm_lib_Target_AArch64_AArch64InstrInfo.cpp L216–268）|
|8 AArch64CondBrTuning runOnMachineFunction|0x3095780→0x30959ce|0x3095740→0x309598e|B|runOnMachineFunction→tryToTuneBranch→convertToCondBr，含getBranchDestBlock和Unexpected opcode default；告警前同一TBZ/TBNZ位图。ThinLTO内联来源结构相符，未唯一逐条定位。（llvm_lib_Target_AArch64_AArch64CondBrTuning.cpp L115–145）|
|9 SemaObjC parsedAttrToRetainOwnershipKind|0x6cb9dc7→0x6cb9dca|0x6cb9d17→0x6cb9d1a|B|parsedAttrToRetainOwnershipKind枚举switch default为Wrong argument supplied/llvm_unreachable；位图0x61在kind-0x3c上失败后jae到end。未读取生成的ParsedAttr枚举数值，故不升级A。（clang_lib_Sema_SemaObjC.cpp L1771–1794）|
|10 SemaObjC handleXReturnsXRetainedAttr|0x6cba1d6→0x6cbaeeb|0x6cba126→0x6cbae3b|B|handleXReturnsXRetainedAttr开头调用parsedAttrToRetainOwnershipKind；内联后同一0x61位图失败jae到end，结构相符但未逐一对应所有属性枚举。（clang_lib_Sema_SemaObjC.cpp L1771–1820）|

A级两处的生成枚举依据：[aarch64-enum.txt](../../tools/bolt/results/night-87-20261114/aarch64-enum.txt)。488..493对应新比较分支，2180..2183对应CBZ/CBNZ；1887为B、2107为Bcc；7881、7882、7899、7900对应TBNZW/TBNZX/TBZW/TBZX，减7881后为0、1、18、19，正好是0xc0003位图。逐分流对照可解释最后jae到end。不能把这个证明推广到整个编译器所有动态输入或全部8个B级点。

ARM候选内联函数的STMDA/STMDB/STMIA/STMIB编号为2007/2009/2011/2013，减2007后为0/2/4/6，匹配0x55；生成枚举原文：[arm-enum.txt](../../tools/bolt/results/night-87-20261114/arm-enum.txt)。但本轮未把全部内联调用链证明到唯一位置，因此仍为B。

源码llvm_unreachable语义见[ErrorHandling.h](../../tools/bolt/results/night-87-20261114/source/llvm_include_llvm_Support_ErrorHandling.h) L145–175：NDEBUG与LLVM_UNREACHABLE_OPTIMIZE等配置决定优化提示或trap；不能仅凭宏名断言真实业务永远不触及该前提。10处均符合BOLT检测的“跳到函数末尾”形态，源结构也都有unreachable候选；**只有2处达到A，不能回答10处已全部严格证明属于注释所说的源码原因**。不使用“无害”结论。

PGO两处名称对应本表1、5；86记录的地址及1551汇总与产品2804分开。未追查PGO旧3ee2d847源码，PGO源码对应关系UNKNOWN，不把fea源码证据移用为旧PGO证明。

## 4. 只读引用74/79最终产物

[final-sha-summary.json](../../tools/bolt/results/night-87-20261114/final-sha-summary.json)引用74本地audit.json的post记录及79已存log-supplement-v2.json.gz中新QB stages：
- T本地与QB1226850最终SHA均为e08724d81231d8675c51d4908f4ff0e8d233ef3740c878da1c7eda42dd3532f5。
- D本地与QB1226851最终SHA均为1664b9d2d70d0cbbbde31f51bf26593c4eed05e776489768dac09aa7234b3362。

**QB内部BOLT日志未保存，按最终产物相同推断告警集合相同，未直接证明。** 最终SHA一致本身不逻辑保证日志集合一致；这里按PM要求记录为推断，不作为直接日志证据。本轮未下载QB数据、未重算最终ELF、未重跑包比较。

## 5. 资源报备草案（只写，未执行）

### 5.1 获批的argv准备修正
[step5-index-fix.diff](../../tools/bolt/results/night-87-20261114/step5-index-fix.diff)只有['argv'][5:]→['argv'][4:]一处。86旧脚本/输出不覆盖，新副本[step5.py](../../tools/bolt/results/night-87-20261114/step5.py)其余逻辑和文字未改。重跑stdout/stderr和返回码：[step3-rerun.stdout](../../tools/bolt/results/night-87-20261114/step3-rerun.stdout)、[step3-rerun.stderr](../../tools/bolt/results/night-87-20261114/step3-rerun.stderr)、[step3-rerun-result.json](../../tools/bolt/results/night-87-20261114/step3-rerun-result.json)。返回0；输入/工具/loader/profile均存在，工具SHA与74原记录一致。继承的stdout仍写86步骤5，只代表新副本重跑，非篡改历史时间。

[原脚本生成草案](../../tools/bolt/results/night-87-20261114/resource-proposal.md)；[87源码核对补充](../../tools/bolt/results/night-87-20261114/resource-supplement.md)；[完整命令/身份JSON](../../tools/bolt/results/night-87-20261114/report-stale-plan.json)。

D输入226,782,848B；工具47,280,568B/SHA12778b710b1f163a83fdd68e7ecb96bc9f70849fac1d86e5131dbcac3d819642；
profile171,232,190B/SHAd9b132f9430dfed32e080c65b4422bd76eba4a9c2101a2b18a7f66c94133b326。
命令通过D自己的loader，保留正式参数与5%门槛，仅加-report-stale。输出拟为W/temp/report-stale-proposal-20261116（未创建）。

申请建议：单进程约10GB（83依据），cgroup16GiB含文件缓存、swap0、CPU400%、nice19/idle；这不是批准也不是新的实测峰值。时长UNKNOWN，拟60分钟上限；磁盘暂申请5GiB，/home<30GiB或新目录>5GiB、OOM/超时停止不重试。正常取消/超时信号需随执行授权。

### 5.2 2804定向诊断
[relocation-diagnostic-plan.json](../../tools/bolt/results/night-87-20261114/relocation-diagnostic-plan.json)给出条件argv、工具身份、开关与停止线。**既有74工具的LLVM_DEBUG已被编译掉，现有工具取得逐条明细这项BLOCKED**。需PM另批同源非NDEBUG诊断工具，或另批只读ELF筛选器；都不在本轮执行范围。条件argv只是开关位置说明，不是可执行的既有工具方案，不能覆盖历史工具。

若未来有获批诊断工具，可将-report-stale与-debug-only=bolt放入同一次运行；需记录新SHA、复现2804及profile计数。风险：工具身份/性能变化、debug日志体积及缓存增加，5GiB/60分钟停止线可能导致报告未完成；精确新增内存/时长/磁盘UNKNOWN。不能为了明细擅自重建BOLT或提高本轮4GiB限制。

### 5.3 下次计划内构建采集
[collection-draft.diff.txt](../../tools/bolt/results/night-87-20261114/collection-draft.diff.txt)是语义伪diff，不可直接应用，未改入口。涉及两侧launcher.py的stage/materialize/worker、resource_report.py、拟新增collector/tests，以及run-night参数传递和说明/清单。
- 命令边界同时记录wall与monotonic起止；精确子步骤须exec/exit证据，不能用相邻日志猜。
- 2秒memory.current/peak/events/stat anon/file，服务回收前保全；短进程VmHWM需进程事件或可审计wait4/rusage，chroot/孙进程盲区明确UNKNOWN。
- 文件系统用量10秒；分层du5分钟、每次50秒、串行，记录超时与权限问题，父子目录不相加。
- 不改变产品helper/spec；无法无侵入得到BOLT内部步骤精确时间时保留UNKNOWN。测试覆盖时钟回拨、短进程、cgroup消失、du失败/超时、日志交接及截断峰值。所有限时终止需新执行任务授权。

### 5.4 本次df与磁盘差额
采样时间：2026-11-14T16:04:50.021193+08:00；原文：[current-df.txt](../../tools/bolt/results/night-87-20261114/current-df.txt)；计算：[resource-budget.json](../../tools/bolt/results/night-87-20261114/resource-budget.json)。

|量|字节|GiB|
|---|---:|---:|
|当前可用|69,928,734,720|65.126|
|历史双根最低预算|162,445,959,168|151.290|
|含20%根余量目标|190,640,183,706|177.548|
|最低预算缺口|92,517,224,448|86.163|
|目标预算缺口|120,711,448,986|112.421|

最低公式2×70,485,561,344B+20GiB；目标公式ceil(2×70,485,561,344B×1.2)+20GiB。它们是历史预算，不保证下一轮采集、版本或比较副本开销。report-stale临时空间另计。没有重新du；下表大小沿用85原采样，不等于承诺释放量。

|候选目录（W/temp下）|85 du GiB|用途文档|替代/发布证据与风险|
|---|---:|---|---|
|local-full-r6-20261111-compare|26.468|74/79|从RPM解包的比较副本；已发布比较报告，保留RPM可重解；本次未逐文件验证可重建；中：先分离日志/唯一证据，不能整目录自动删|
|qb79-local-resume-20261112|24.898|79|源码tar/比较工作副本；报告与分类证据已发布，RPM在QB下载目录；唯一性需清单审核；中|
|dwarf-check-20261106|29.886|67|DWARF展开文本和副本；分类结论已发布，132对原.debug需保留；文本可否完全重生未复核；中|
|qb-1221204-1221207|16.089|71|旧QB下载；71结果已发布，不能保证公开下载长期可用；后续基线现为1226850/1；中高：旧回归追溯基线|
|qb-1223601-1223602|16.090|73/75|旧QB下载及ARM检查源；77/79新基线可覆盖部分，不替代全部历史输入；高|
|deleted-repo-backup-20261105|91.294|64/66|源码保护bundle/补丁；GitHub未包含全部仓库副本，85扩展盘点OOM；极高：不建议清理，需先独立源码完整性审计|

完整路径、原采样时间、风险见[cleanup-candidates.json](../../tools/bolt/results/night-87-20261114/cleanup-candidates.json)。这里只列待审核候选，不授权删除；源码保护备份明确不建议删，不能因摘要已发布就认为大型原始输入已发布。

## 6. 读取范围、边界与结束行

已读：STATUS和86停点；fea源码中BOLT完整BinaryFunction/RewriteInstance/Relocation、Debug/ErrorHandling及相关LLVM/Clang函数；86保存的反汇编和警告JSON；74构建生成的AArch64/ARM枚举与BOLT编译参数；74/79本地证据；85目录清单；86草案脚本；B入口采集相关代码。源码读取仅git show/grep，没有改LLVM工作树/分支。

未读/未做：QB/Gerrit网络、PGO旧源码、入口W差异全表/同步/30测试/dry-run、BOLT执行、构建、清理、性能实验、新relocation逐条运行、运行中的动态路径验证。已有86证据未修改。没有OOM或超时。
执行组织偏差：命令按多个小段串行用户服务运行，而非每个步骤仅一个服务；所有服务均指定4GiB/swap0/Nice19/idle，未并行。此处如实记录，不把它描述为严格满足“每步骤一个服务”。

结束行：
- 87步骤1 已结束 2026-11-14T16:00:28+08:00 status=STOP reason=rg-not-found
- 87步骤2 已结束 2026-11-14T16:04:31.266254+08:00 status=PASS_WITH_LIMITATIONS
- 87步骤3 已结束 2026-11-14T16:06:58.468087+08:00 status=DRAFT_WITH_BLOCKED_DIAGNOSTIC

所有交付文件见[raw链接索引](../../tools/bolt/results/night-87-20261114/RAW_LINKS.md)。唯一运行错误STOP原文在步骤1；NDEBUG诊断限制是只读源码结论，不是执行BOLT失败。下一次使用入口前仍需完成未运行的同步/测试；本报告不放行构建。
