# 99号：周末低资源任务

**五步已结束：1 STOP，2–5 PASS。** 步骤1既有测试出现进程读取竞态，未创建新产品提交或推送sandbox。步骤5使用已提交b0c1732c，完成450发货归档复核，以及225个原始归档的3853个转换成员重新生成/字节比较，全部一致。看门狗未触发，无OOM。

步骤1–4和收尾服务4GiB/swap0/CPU200%/Nice19/IO idle；步骤5准备4GiB，实际重放按授权12GiB/CPU400%、jobs=2，每进程地址空间4GiB。所有服务串行，重放含准备总限120分钟，每30秒检查MemAvailable<6GiB即停止自己的服务。首次准入全部满足，没有进入30分钟等待。未进入另一项目目录、未操作其锁或进程。

|步骤|状态|结果|
|---|---|---|
|1|STOP|103项已运行：102通过、1ERROR，16未运行；sandbox未推送|
|2|PASS|8处B完成复核，3升A、5仍B；连同87号现为5A/5B|
|3|PASS|68函数逐对指令diff；28算术序列、35 LEA/复制形式、5混合|
|4|PASS|设计6项事实资料包；无推荐/裁决|
|5|PASS|450发货归档/7728 ELF成员新旧检查一致；225 T原始归档重新转换3853成员、保留11成员，归档和逐成员SHA与发货T一致|

[raw链接索引](../../tools/bolt/results/weekend-99-20261114/RAW_LINKS.md)。

## 步骤1：STOP（既有测试出现进程读取竞态）

只改log_startup_context中一个续行的前导空白，AST逐节点完全相同；未改测试预期。原独立工作树HEAD仍b0c1732c，保留这处未提交空白改动，没有重建产品提交，没有sandbox查询或推送。后续实物重放将使用git对象b0c1732c，而非这份脏工作树文件。

|套件|运行|通过|错误|未运行|
|---|---:|---:|---:|---:|
|加固|16|16|0|0|
|policy|46|46|0|0|
|release|5|5|0|0|
|r2|12|12|0|0|
|R3/R4/R5|24|23|1|16|
|合计|103|102|1|16|

原40项范围仍排除已在96号声明不适用的旧三提交身份测试，不改本轮范围。复制测试环境，仅修改新输出目录路径。未把测试运行中的ERROR解释为准备错误，没有修测试/重试。

~~~text
ERROR: test_process_states_at_run_return (test_r3.R4.test_process_states_at_run_return)
File "test_r3.py", line 427, in state
    fields=Path('/proc',str(pid),'stat').read_text().split(') ',1)[1].split()
ProcessLookupError: [Errno 3] No such process
~~~

[完整测试日志](../../tools/bolt/results/weekend-99-20261114/step1/r3-r4-r5.log)、[空白diff](../../tools/bolt/results/weekend-99-20261114/step1/whitespace.diff)、[步骤结果](../../tools/bolt/results/weekend-99-20261114/step1/result.json)。失败只停止本步骤；不触发sandbox回退。

99步骤1 已结束 2026-11-14T06:22:02.651260-08:00 status=STOP

## 进度

五步均已结束；各步原始记录如下。

## 步骤2：PASS（8处完成复核，3处升A、5处仍B）

读取74号T构建的X86/ARM/AArch64生成opcode表、AttrParsedAttrList.inc及AttributeCommonInfo.h，复用87号同源源码和86号完整反汇编；不编译、不运行BOLT，不用PGO旧源码。A只表示该处与unreachable前提逐项对上，不是所有运行输入正确性的证明。

|87序号|等级|依据和未闭合部分|
|---|---|---|
|1|B|0x900000009对应INC16r/INC16r_NF/INC8r/INC8r_NF（1891,1894,1923,1926）；对应源码CASE_NF(INC8r/INC16r)。其他SHL/ADD/DEC先分流；尚未解码全跳表及所有入口到末尾bit-test的控制流，不升级。|
|2|B|0x4104041+5663对应5个VBROADCAST浮点rmk，0x2082000001041+15066对应6个VPBROADCAST整数rmk。已映射末端拒绝前11种枚举，但主switch还有大量分支/跳表，不能用最后一个位图证明整个default路径。|
|3|B|0x55+2007为STMDA/STMDB/STMIA/STMIB，0x55+938为LDMDA/LDMDB/LDMIA/LDMIB；对应getUpdatingLSMultipleOpcode L1122–1142。源码尚有t2/VFP及Mode分支；没有完整复原内联调用链和Mode表，所以保持B。|
|6|B|7881+0xc0003为TBNZW/TBNZX/TBZW/TBZX，成功选operand2（0x50），随后比较MBB successor，与getBranchDestBlock调用相符。尚未唯一定位所有内联入口，保持B。|
|7|A|函数入口直接读取opcode；2180..2183先取operand1；另侧2107及488..493分流；余下7881+0xc0003匹配TBNZW/TBNZX/TBZW/TBZX，成功取operand2。该集合精确对应parseCondBranch L235–243，失败jae到end为L220–221 default。合法case全部绕开该末尾拒绝分支。|
|8|B|生成枚举将同一0xc0003准确映射到四种TBZ/TBNZ，operand2读取与convertToCondBr→getBranchDestBlock相符；同一内联范围还混有cond-code选择，未逐一复原全部入口路径，不升级。|
|9|A|ParsedAttr由AttributeCommonInfo.h L67–70按生成表从0顺序展开。CF=60/65/66，对应0x61；NS=212/213/215/216/217，对应0x3b；OS=257..262，对应0x7e00000000000。14种合法kind在真实汇编分流逐项得到正确返回值；末尾jae只有不满足这些合法集合时执行，对应源码L1791–1792。|
|10|A|handleXReturnsXRetainedAttr入口紧接读取kind；0x7e0000000003b合并OS/NS，0x61识别CF，完整覆盖上述14种kind。与L1818调用parsedAttrToRetainOwnershipKind逐指令对应；失败jae到end只在违反其unreachable前提时出现。|

已有2个A不在本次8处范围，合计现在5A、5B。没有把未闭合控制流的B项提升。

[精确枚举/位图/行号](../../tools/bolt/results/weekend-99-20261114/step2/mask-enum-mapping-v2.json)、[14种属性逐项真值表](../../tools/bolt/results/weekend-99-20261114/step2/parsedattr-truth-table.json)、[源码与指令证据](../../tools/bolt/results/weekend-99-20261114/step2/source-and-prologue-evidence.txt)、[逐项结果](../../tools/bolt/results/weekend-99-20261114/step2/attribution.json)。

准备修正1次：初始解析整个生成文件，后续内部枚举重复编号覆盖opcode；保留原错误映射，修正为止于INSTRUCTION_LIST_END并断言不重复。见preparation-error.txt及parser-fix.diff；不是产品异常。

99步骤2 已结束 2026-11-14T06:25:32.127791-08:00 status=PASS

## 步骤3：PASS（68个函数逐一反汇编与指令diff）

两份BOLT输入重新计算SHA，与83号完整SHA一致。使用74号Toolchain根的llvm-objdump，经该根loader和library-path串行反汇编136个函数范围；没有运行BOLT、没有全ELF反汇编落盘、没有修改原件。[工具与输入身份](../../tools/bolt/results/weekend-99-20261114/step3/identities.json)。

原始T/D指令文本和raw.diff.gz全保留。分类视图去绝对地址、ThinLTO后缀，内部跳转写成指令序号，重定位控制的call/RIP地址标RELOC（仅用于分类，不是新等价门禁）。因此插入一条指令会造成后续I编号差异；这些不得误记为常量或基本块重排。另保留NOP差异，在次级分类时排除NOP及这种内部跳转编号噪声。

**这是静态形式分类，不证明寄存器分配器、优化pass或快照是成因，不代替83号字节和重定位元组比较。** 多种变化共存时按可观测主要形式归类。

|排他主类|数量|边界|
|---|---:|---|
|指令选择/序列形式变化：LEA减少、分开ADD/SUB增加|28|包含其他操作数变化，不声称每条一一语义等价|
|指令选择/序列形式变化：LEA增加、原MOV复制存在|35|观察到重新计算/复制形式差异，不推断优化原因|
|其他/混合变化|5|包含移位代替掩码、栈偏移/寄存器和较大序列变化|
|可单独确认只有寄存器操作数变化|0|混合类中仍有寄存器变化，不等于没有寄存器变化|
|可单独确认只有常量/偏移变化|0|混合类中仍有栈偏移变化|
|可单独证明仅基本块顺序变化|0|未构造CFG同构证明，不以指令排序启发式冒充基本块结论|

次级形式计数采用diff中LEA/ADD/SUB/MOV数量和明确的优先顺序，属于描述性分组，不是完整数据流归因。初始机械分组为45项少量opcode变化、23项混合；两种分组均保留，不把初始结果覆盖。

[68项完整分类](../../tools/bolt/results/weekend-99-20261114/step3/observed-forms.json)、[初始分类与argv](../../tools/bolt/results/weekend-99-20261114/step3/classification.json)、[脚本](../../tools/bolt/results/weekend-99-20261114/step3/classify.py)。每个编号都有left.asm、right.asm、instruction.diff和raw.diff.gz。

### 样例（每类3个）

LEA + 算术 → 分开算术：

- 04 `_ZL20printBSDMemberHeaderRN4llvm11raw_ostreamEmNS_9StringRefERKNSt6chrono10time_pointINS3_3_V212system_clockENS3_8durationIlSt5ratioILl1ELl1EEEEEEjjjm`：[diff](../../tools/bolt/results/weekend-99-20261114/step3/04-instruction.diff)
~~~text
T removed:
leal (%rcx,%rsi), %eax
subl %eax, %r12d
D added:
subl %ecx, %r12d
subl %esi, %r12d
~~~

- 11 `_ZN12_GLOBAL__N_117VPCSEDenseMapInfo12getHashValueEPKN4llvm17VPSingleDefRecipeE`：[diff](../../tools/bolt/results/weekend-99-20261114/step3/11-instruction.diff)
~~~text
T removed:
leaq (%r8,%r15), %r10
addq %r10, %rcx
D added:
addq %r8, %rcx
addq %r15, %rcx
~~~

- 34 `_ZN4llvm4SHA19hashBlockEv`：[diff](../../tools/bolt/results/weekend-99-20261114/step3/34-instruction.diff)
~~~text
T removed:
leal (%r12,%rsi), %ecx
addl %ecx, %eax
leal (%r12,%r8), %edi
addl %edi, %r10d
leal (%r13,%rsi), %edx
addl %edx, %r10d
D added:
addl %r12d, %eax
addl %esi, %eax
addl %r12d, %r10d
addl %r8d, %r10d
addl %r13d, %r10d
addl %esi, %r10d
~~~

寄存器复制 → LEA形式：

- 07 `_ZL37createAndCheckVectorTypesForPromotionRN4llvm9SetVectorIPNS_4TypeENS_11SmallVectorIS2_Lj0EEENS_8DenseSetIS2_NS_12DenseMapInfoIS2_vEEEELj0EEENS_8ArrayRefIPNS_10VectorTypeEEENS_12function_refIFvS2_EEERN12_GLOBAL__N_19PartitionERKNS_10DataLayoutERNS_15SmallVectorImplISD_EERbRS2_SR_SR_RSD_j`：[diff](../../tools/bolt/results/weekend-99-20261114/step3/07-instruction.diff)
~~~text
T removed:
movq %rbx, %r15
D added:
leaq 0x8(%rsi), %r15
~~~

- 57 `_ZN5clang4Sema24checkFinalSuspendNoThrowEPKNS_4StmtE`：[diff](../../tools/bolt/results/weekend-99-20261114/step3/57-instruction.diff)
~~~text
T removed:
movq %r14, 0x60(%rsp)
movq %r14, 0x18(%rsp)
D added:
movq %r14, 0x60(%rsp)
leaq 0x8(%rbp), %rax
movq %rax, 0x18(%rsp)
~~~

- 68 `_ZZN12_GLOBAL__N_115InitListChecker26CheckDesignatedInitializerERKN5clang17InitializedEntityEPNS1_12InitListExprEPNS1_18DesignatedInitExprEjRNS1_8QualTypeEPNS1_11DeclContext22specific_decl_iteratorINS1_9FieldDeclEEEPN4llvm6APSIntERjS6_SJ_bbENK3$_0clERNS1_8SemaBase21SemaDiagnosticBuilderE`：[diff](../../tools/bolt/results/weekend-99-20261114/step3/68-instruction.diff)
~~~text
T removed:
movq %rbp, %rbx
D added:
leaq 0x10(%r12), %rbx
~~~

混合/其他：

- 01 `_ZL10combineMulPN4llvm6SDNodeERNS_12SelectionDAGERNS_14TargetLowering15DAGCombinerInfoERKNS_12X86SubtargetE`：[diff](../../tools/bolt/results/weekend-99-20261114/step3/01-instruction.diff)
~~~text
T removed:
leal 0x3f(%rax), %esi
andl $-0x40, %esi
callq RELOC_TARGET
callq RELOC_TARGET
D added:
movl %edx, %esi
shll $0x6, %esi
callq RELOC_TARGET
callq RELOC_TARGET
~~~

- 03 `_ZL18lower128BitShuffleRKN4llvm5SDLocENS_8ArrayRefIiEENS_3MVTENS_7SDValueES6_RKNS_5APIntERKNS_12X86SubtargetERNS_12SelectionDAGE`：[diff](../../tools/bolt/results/weekend-99-20261114/step3/03-instruction.diff)
~~~text
T removed:
movq %r15, 0x28(%rsp)
movq %rbx, 0x20(%rsp)
movq 0x20(%rsp), %r11
movq 0x28(%rsp), %r14
pushq 0x40(%rsp)
pushq 0x40(%rsp)
D added:
movq %r15, 0x20(%rsp)
movq %rbx, 0x28(%rsp)
movq 0x28(%rsp), %r11
movq 0x20(%rsp), %r14
pushq 0x48(%rsp)
pushq 0x48(%rsp)
~~~

- 23 `_ZN4llvm13slpvectorizer7BoUpSLP24computeMinimumValueSizesEv`：[diff](../../tools/bolt/results/weekend-99-20261114/step3/23-instruction.diff)
~~~text
T removed:
leal 0x1(%rbx), %r15d
movq (%rdx,%r15,8), %rdx
movl $0x1, 0x1180(%r13)
movl 0x90(%r13), %eax
cmpl %r15d, %eax
testq %rdi, %rdi
D added:
leal 0x1(%rbx), %esi
movq (%rdx,%rsi,8), %rdx
movl %esi, %r15d
movl $0x1, 0x1180(%r13)
movl 0x90(%r13), %eax
cmpl %r15d, %eax
~~~

未读取最终clang、未做源文件/成因定位；读取83号68项名单与两份已保存输入。准备修正0次。

99步骤3 已结束 2026-11-14T06:28:48.751091-08:00 status=PASS

## 步骤4：PASS（事实资料包，不作裁决）

[六项完整资料包](../../tools/bolt/results/weekend-99-20261114/step4/pgo-decision-facts.md)覆盖设计v9第7节1/2/6/11/12/13条；每条含选项事实对比、已有数据、尚缺证据及获取资源边界。[来源行号与原文](../../tools/bolt/results/weekend-99-20261114/step4/source-excerpts.txt)。

52,528,216B PGO、194,262,069B配对BOLT profile是未压缩历史值；BOLT插桩/训练/合并460.777s、VmHWM最高17,014,747,136B；这些不是完整构建认证。没有把55号借用的非PGO后处理时间算成PGO实测。主构建可影响LLVM/Clang/LLD工具和库，但逐TU实际目标名单仍缺；运行库排除是设计约束，不能冒充已完成的盘点。计数方法、留出集和阈值缺数据，未给推荐值。

只读指定报告与JSON，未读取所有长日志或profile本体，没有新实验。准备修正0次。

99步骤4 已结束 2026-11-14T06:34:48.654365-08:00 status=PASS

## 步骤5：PASS（补足全部3853个成员的重新生成）

首次检查2026-11-14T06:35:12-08:00：未发现gbs/rpmbuild/ninja/llvm-bolt重进程，MemAvailable=26,350,829,568B，/home可用206,627,004,416B。06:35:36非阻塞取得既有共享heavy-stage.lock；没有获取另一项目私有锁，重放结束已随服务退出释放。没有等待30分钟轮询，未到截止时间是因为首次已满足全部条件。

### 输入和验证覆盖

- 从git对象导出b0c1732c转换器，基线ecb2dec7；不使用步骤1留存的脏工作树文件。
- 78号450个发货归档来自QB 1225393/1225395；79号已证明1226850/1226851的102个二进制包载荷与它们一致（本次只读79号该记录，未重读全部RPM，见baseline-chain.txt）。这些归档已是ELF。每个项目225归档、3864成员（历史3853转换+11原生），共7728；新旧inspect、elf_details、pic_relocations相同，forbidden为0，成员SHA和归档SHA未变化。实际convert保持既有的225个already-native skip行为，不能称这些输入又完成了一次代码生成。
- 10个真实debug ThinLTO归档：1093转换+7原生，两级SHA及inspect其余字段与78号保留输出一致；保留输出也与发货T相同。
- 为覆盖用户要求的全部3853个转换成员，读取63号保留build/lib64中其余215个对应原始归档，在新副本中用同样平台clang/llvm-dis/llvm-nm、loader、debug_info=yes、jobs=2转换。连同10个大归档，共225归档/3853转换+11原生；完整归档SHA、大小、成员顺序、逐成员SHA及其余inspect字段均与发货T相同。D覆盖为全量ELF检查与保留路径，不宣称D的3853成员重新代码生成。
- 合法输入新增拒绝0。所有新生成的对象都经过产品PIC/符号门禁；未改产品测试或断言，没有产品失败后的重跑。

[覆盖补足计划](../../tools/bolt/results/weekend-99-20261114/step5/coverage-plan.md)、[工具身份](../../tools/bolt/results/weekend-99-20261114/step5/tool-identities.json)、[第一段结果](../../tools/bolt/results/weekend-99-20261114/step5/result.json)、[3853全量结果/逐成员SHA](../../tools/bolt/results/weekend-99-20261114/step5/result-full.json)、[完整重放日志](../../tools/bolt/results/weekend-99-20261114/step5/replay-remaining.log)。第一段日志的“99步骤5 已结束”只指450+10子段完成，最终以本节的全量结束行为准。

本轮输出根W/temp/weekend99-replay-20261114。其余215个临时输入/输出在记录SHA和逐成员结果后仅删除本任务自己的文件，保留JSON/日志；历史根、78保留输出及发货归档未写。10个大归档的新输出仍在debug/archives/。

### 资源和准备修正

服务含准备耗时2516.527s，cgroup峰值11222745088B（含文件缓存），OOM=0、oom_kill=0、max事件=0。最低MemAvailable=26307432448B，临时目录成功采样最大3583498291B。看门狗没有触发。VmHWM采样及命令行见[资源摘要](../../tools/bolt/results/weekend-99-20261114/step5/resource-summary.json)，短命子进程可能漏采。

准备修正1次：在运行中的服务上用set-property设置RuntimeMaxSec被systemd拒绝，尚未开始重放。保留错误原文与diff，改为仅设置支持的MemoryMax/CPUQuota，并由单调时钟看门狗执行整个步骤7200秒限时；未因OOM提高上限。第二段从服务启动时间计时，包含准备及第一段，更严格。见[错误与修正](../../tools/bolt/results/weekend-99-20261114/step5/preparation-error.txt)。没有第二次准备错误。

~~~text
Failed to set unit properties on weekend99-step5-20261114.service: Cannot set property RuntimeMaxUSec, or unknown property.
~~~

### sandbox与没有运行的内容

步骤1停止，所以本任务没有新建产品提交、查询或推送sandbox。任务输入/96号最后观测是b0c1732c；没有新的远端after观测，不能将本地状态冒充ls-remote结果。无自动回退。没有运行完整构建、BOLT/report-stale、QB、Gerrit查询/评审操作。只在证据仓库提交推送。

已读：步骤1的产品git对象/既有测试，87号同源源码/反汇编及74号生成表，83号68函数名单和两份BOLT输入，58/59/84/86及设计指定段落，78号归档/转换保留产物、63号原始归档和平台工具。未读：另一项目目录、QB/Gerrit网页、全部历史GBS原日志、全部PGO profile本体；未做未授权的因果推断或决策。

99步骤5全量 已结束 2026-11-14T07:16:54.105927-08:00 status=PASS

99 已结束 2026-11-14T07:17:19.589999-08:00 1=STOP 2=PASS 3=PASS 4=PASS 5=PASS
