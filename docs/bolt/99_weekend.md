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
