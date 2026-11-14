# 99号：周末低资源任务

逐步交付；尚未完成的步骤不标PASS。全部分析串行、4GiB/swap0/CPU200%/Nice19/IO idle；每30秒检查MemAvailable，低于6GiB只停止本任务自己的服务。步骤1准入≥8GiB、磁盘≥60GiB通过。未进入另一项目目录、未操作其锁或进程。

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

## 后续步骤

步骤2–5待执行。

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
