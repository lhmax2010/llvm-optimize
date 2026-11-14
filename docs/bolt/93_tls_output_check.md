# 93号：BOLT最终输出的TLS静态核对

**总体 FAIL / STOP，等待PM裁决；未对Gerrit作任何操作。** T的最终发货clang身份通过；T输入/输出TPOFF64 GOT集合完全相同，1537处IE访问全部指向集合内的两个槽。多出的1处已定位为旧代码节中的同地址、同字节保留序列，`.text + .text.cold`为1536处。LD→LE固定填充前缀计数 **415→3**，同前缀非零`%fs:`位移为0；剩余412处输出表示未被本轮核对覆盖，不能给出“全部TLS序列正确”的结论。停止后未继续D的指令核对、未修改判据或重跑。

这次FAIL是**固定序列覆盖未闭合**，不是已发现错误GOT目标或非零`%fs:`位移；不能直接等同于产品TLS误编译。对361395的后续处置由PM决定。

92号秘密扫描按本次PM裁决关闭为 **PASS（无凭据）**；原STOP与已推送历史不改。report-stale由PM周一另行安排，本任务未运行。

[完整证据raw索引](../../tools/bolt/results/night-93-20261114/README.md)。时间使用America/Los_Angeles（UTC−08:00）。

## 1. 被检查的ELF：身份PASS

所有文件均直接读取已保留实体，没有重新解包、复制或修改：

|项目|角色|大小（B）|SHA256|
|---|---|---:|---|
|toolchain|final_rpm|152532400|`e08724d81231d8675c51d4908f4ff0e8d233ef3740c878da1c7eda42dd3532f5`|
|toolchain|input|226816920|`ae3d837d862673b03c3c4718f6746f6986d8abe2078bad426b97905258b91a5c`|
|toolchain|auxiliary_bolt_before_strip|185754320|`9d36bd998d17ac0e6e433ab6c31b63c39608b9b0def0922eb49814e9793f2bb9`|
|basedev|final_rpm|152531536|`1664b9d2d70d0cbbbde31f51bf26593c4eed05e776489768dac09aa7234b3362`|
|basedev|input|226782848|`bf15cf062439714651809cd3b5ca82619407081adca64ceb65699e6ccae50501`|
|basedev|auxiliary_bolt_before_strip|185717808|`a6be662e5432d1db81dadd188a4f0f6206dbfe42b81c1ac629ae50459cdf4ece`|

最终发货路径分别为：

- `W/temp/local-full-r6-20261111-materials/toolchain/final-clang-rpm/usr/bin/clang-22`
- `W/temp/local-full-r6-20261111-materials/basedev/final-clang-rpm/usr/bin/clang-22`

输入路径为同一materials目录各项目下的`reference-relocs-clang-22`。辅助strip前BOLT产物为各自74号构建根的`build/clang-bolt/clang.bolt`，本轮只登记身份，不以辅助文件代替最终发货clang。完整绝对路径/大小/SHA见`identities.json`。

两份最终SHA均与用户指定值及74号既有RPM提取证据一致；T输入为ae3d837d，D输入为bf15cf06。使用对应构建根loader运行平台llvm-objdump，argv、loader/tool SHA见`toolchain-output-command.json`。

## 2. T的IE静态核对

### 2.1 G_in / G_out：PASS

直接解析两份ELF的`.rela.dyn`，取R_X86_64_TPOFF64(18)，按**地址、符号名、addend**比较。两个集合各2条，差异为空：

|GOT地址|TLS符号|addend|输入引用|最终全部可执行节引用|
|---|---|---:|---:|---:|
|0x8569ce0|`_ZSt15__once_callable`|0|771|772|
|0x8569ce8|`_ZSt11__once_call`|0|765|765|

`toolchain-dynamic.json`保存完整动态符号记录：两符号均为STB_GLOBAL/STT_TLS，SHN_UNDEF、st_value=0。输入/输出NEEDED相同：librt.so.1、libdl.so.2、libm.so.6、libz.so.1、libstdc++.so.6、libgcc_s.so.1、libc.so.6、ld-linux-x86-64.so.2。

依据这些ELF信息，它们不是本可执行文件中已定义、位置可直接确定的TLS对象，仍需要动态TLS GOT解析；这与保留IE形式相符。NEEDED说明共享库依赖存在，但仅凭NEEDED与符号名不能严格证明具体由哪个共享库实例提供，本轮未解析外部提供者或断言具体抢占绑定结果。

### 2.2 输出所有可执行节扫描

`check_tls_output.py`使用对应loader的llvm-objdump `-d --disassemble-zeroes`，逐行处理，不保存全量反汇编。覆盖所有非空SHF_EXECINSTR节：`.bolt.org.text`、`.text`、`.text.cold`、`.init`、`.fini`、`.plt`。解析实际指令长度和disp32，计算 `add指令地址 + 指令长度 + 有符号位移`，不用反汇编注释作为目标计算依据。

查找不限通用寄存器的`movq %fs:0, %REG`→`addq DISP(%rip), %REG`；另跟踪同一连续指令段内最多32条指令中的寄存器复制和无关指令，遇到覆盖、控制转移或地址不连续结束跟踪，相邻不同寄存器也单列。本轮命中的1537处**全部是相邻同寄存器形式**，变体0；有界跟踪不是任意跨基本块数据流证明。

每个命中目标都属于G_out，**集合外目标0**，未命中错误的__tls_get_addr/PLT/.text目标。完整每处两条指令、原始字节、目标地址、节名在`toolchain-full-static-check.json.gz`；样例原文在`toolchain-examples-and-all-bad.txt`，没有坏目标列表。

### 2.3 1536→1537差值说明

|输出节|引用once_callable|引用once_call|合计|
|---|---:|---:|---:|
|.bolt.org.text|1|0|1|
|.text|242|239|481|
|.text.cold|529|526|1055|
|.text+.text.cold|771|765|1536|

额外1处位于`.bolt.org.text`地址 **0x27e3521**。只用已保存的核对结果进一步对照：它与输入在同一地址的16字节序列完全相同，目标仍为0x8569ce0；见`retained-old-section.json`的`same_address_and_bytes_and_target=true`。因此原始总计差1可定位为该旧代码保留条目，不能说它指向错误GOT。没有证明其运行时可达性，也不下“无害”判断。

初始机械汇总要求总数严格相等，原`toolchain-summary.json`与stdout中的FAIL原文保留；用户本来允许有证据的计数差值解释，故报告单独给出上述事实，不重跑或更改原输出。IE的目标核对和差值定位已完成；总体停止仍由下节LD覆盖问题决定。

## 3. T的LD→LE固定序列：覆盖未闭合，FAIL / STOP

对所有可执行节的原始字节找前缀`66 66 66 64 48 8b 04 25`及其后disp32，同时核对命中地址确为平台反汇编的指令边界。输入有415处位移0的完整序列；输出只找到3处，均在`.bolt.org.text`：

```text
27cb8cd: 66 66 66 64 48 8b 04 25 00 00 00 00  movq %fs:0x0, %rax
27d01af: 66 66 66 64 48 8b 04 25 00 00 00 00  movq %fs:0x0, %rax
27d1a84: 66 66 66 64 48 8b 04 25 00 00 00 00  movq %fs:0x0, %rax
```

同前缀而disp32非0的变体 **0**。没有错误位移原文可列出。当前输出可执行节共1955处一般`movq %fs:0,...`，但这不证明412个未再出现固定填充前缀的输入序列分别对应到其中哪一处。**未把“找不到原字节模式”写成“TLS访问消失”**，也未假定只是BOLT去掉了data16填充。

需要PM裁决的最小后续是只读跟踪这412处是否被重编码为无填充形式及对应地址；本轮按停止规则未继续该扩展，也未运行辅助BOLT产物比较。D只完成输入/最终/辅助ELF身份登记，G集合、IE、LD核对均NOT RUN。

## 4. 分级与全部STOP原文

|项目|结论|
|---|---|
|T/D身份|PASS|
|T G_in=G_out、所有IE GOT目标|PASS|
|T IE计数差值|额外1处已定位为旧节同地址同字节保留序列；原机械FAIL保留|
|T LD→LE固定序列|415→3，覆盖未闭合；FAIL|
|D G/IE/LD|NOT RUN（T停止后未继续）|
|本任务总评|FAIL / STOP，等PM处理|

不能写用户规定的全部通过结论，也不能声称全部残留PLT32未被应用；本轮确实核实了IE命中的GOT目标，尚未核实所有LD输入对应的输出形式。

```text
{"project": "toolchain", "G_equal": true, "G_count": 2, "input_IE": 1536, "output_IE": 1537, "IE_variants": 0, "outside_G": 0, "references_by_slot": [{"address": "0x8569ce0", "symbol": "_ZSt15__once_callable", "input": 771, "output": 772}, {"address": "0x8569ce8", "symbol": "_ZSt11__once_call", "input": 765, "output": 765}], "input_LD_zero": 415, "output_LD_zero": 3, "output_LD_nonzero": 0, "executable_sections": [".bolt.org.text", ".text", ".text.cold", ".init", ".fini", ".plt"], "decoded_instructions_by_section": {".bolt.org.text": 107620, ".text": 3468385, ".text.cold": 19575896, ".init": 7, ".fini": 3, ".plt": 1017}, "fs0_load_count": 1955, "time": "2026-11-14T02:37:33.629704-08:00", "status": "FAIL"}
93静态核对 已结束 2026-11-14T02:37:33.629704-08:00 toolchain status=FAIL
STOP: final clang TLS static-check mismatch; no rule changes or retries.
```

本轮无资源OOM、无工具错误、无准备修正或重试。服务属性见`service-properties.txt`：MemoryMax4GiB、MemorySwapMax0、Nice19、IOSchedulingClass3，观测峰值1360162816 B。只读汇总既有结果的节计数和旧地址对照未重新执行扫描。

## 5. 关闭92号扫描与长期规则

PM裁决原意记录：92号步骤2为误报。88号报告L98和packaging-v2.stderr L3均引用扫描断言行，PM已在GitHub核对其后没有密钥正文，**结论PASS（无凭据）**。本轮没有访问GitHub页面重新取证，不把PM核对表述为本轮独立扫描结论；原STOP、脚本和已推送提交全部保留。

长期规则：**引用扫描规则自身文字的报告和日志行，今后登记为已知误报，不触发STOP。** 这只针对引用规则文字，不豁免实际凭据正文。

92号report-stale SKIPPED正确，由PM周一另行安排。本任务未运行report-stale、不查询Gerrit、不对361395或其他评审作任何远端写操作。

## 6. 读取范围与未运行项

已读：74号报告及final-clang-command.json的RPM提取身份；92号T/D输入身份与平台工具命令；实际T/D输入和最终及辅助ELF的大小/SHA；T输入/输出动态表和重定位、全部输出可执行节的流式反汇编；已生成结果用于差值定位；本轮PM裁决。

未读/未运行：QB/Gerrit网络、构建、BOLT、report-stale、D指令扫描、辅助BOLT ELF的指令对比、旧源码编辑、跨完整控制流的TLS数据流证明。没有删除、移动或修改任何历史产物。记录时间：2026-11-14T02:41:17.337891-08:00。
