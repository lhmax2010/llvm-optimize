from common import *
import datetime
now=datetime.datetime.now().astimezone().isoformat()
text='''# 94号：TLS指令逐函数对照

**PASS。T、D各1187个参与函数全部相同，无法对应或内容不同项为0。** 两边各415处LD主体均由输入的data16×3填充形式变成无该填充的形式；旧`.bolt.org.text`另外各保留3处LD、1处IE，均与输入同地址、同字节。93号固定前缀计数的覆盖缺口已经闭合。

按本任务规定的逐函数静态口径：**全部TLS访问序列（IE 1536、LD 415、DTPOFF偏移）在最终发货clang中逐函数与BOLT输入一致；LD序列仅去掉冗余data16填充前缀；残留的`__tls_get_addr` PLT32记录未被应用。** 最后一项指这些已经逐项核实的TLS指令没有被旧调用重定位改坏；不声称重定位记录已从ELF移除，不扩展成任意控制流或运行可达性证明，不作“无害”判断。

PM定性记录：93号FAIL属于判据覆盖缺口，不是已发现错误。93号原脚本、输出与STOP记录保持不动；本次用新判据、新文件独立核对，不以总数吻合预设结论。

[完整证据索引](../../tools/bolt/results/night-94-20261114/README.md)。全部时间为America/Los_Angeles（UTC−08:00）。

## 1. 对照对象与发货等价性：PASS

重新计算93号登记的T/D输入、最终发货和辅助BOLT ELF共6个文件的大小/SHA，全部与原值相同，完整绝对路径见`identities.json`。

|项目|角色|字节数|SHA256|
|---|---|---:|---|
'''
for x in ids:text+=f"|{x['project']}|{x['role']}|{x['bytes']}|`{x['sha256']}`|\n"
text+='''
输入：74号保留的`reference-relocs-clang-22`。输出用于符号归组的是历史构建根`build/clang-bolt/clang.bolt`；最终文件为74号已解包发货RPM的`usr/bin/clang-22`。

T、D分别比较辅助ELF与发货ELF的全部SHF_EXECINSTR节：`.bolt.org.text`、`.text`、`.text.cold`、`.init`、`.fini`、`.plt`。节集合、各节大小、地址及全部字节均相同（每节SHA见两份`*-section-identity.json`）。因此辅助文件的指令和符号定位结论适用于最终发货clang，不仅是辅助产物结论。

## 2. 比较器与实际边界

代码：`common.py`（只读mmap ELF、符号表）、`compare.py`（流式反汇编和四项比较）、`summarize.py`（从本次结果生成LD逐函数映射与旧节证明）。复用92号ELF类时只提取类定义，不执行其历史main；没有写入任何历史目录。

- 对应74号T/D构建根的loader运行其平台llvm-objdump，先核对loader/tool SHA。命令为各`*-command.json`，使用`-d --disassemble-zeroes`。所有非空可执行节均有覆盖；不保存全量反汇编，仅保留TLS相关指令原文、字节、地址、节、函数和比较结果。
- 按ELF STT_FUNC符号范围归属。相同地址的别名保留清单并确定同一名字；输出实际`.cold`或`.cold.N`后缀仅在对应主名字存在于输入符号表时合并。不是无条件删除名称后缀。零大小或范围外TLS指令会登记UNMAPPED；本次两边均0。
- `.bolt.org.text`按输入原地址范围归到`OLD:`独立组，不参与主体/冷片段通过计数。旧组另逐条验证，不能用来补足主体遗漏。
- 指令文本只移除地址/符号注释、规范化空白和冗余前缀文字；寄存器、操作码、立即数、内存偏移保留。每函数比较：(1)全部含`%fs:`指令的多重集合；(2)IE条数；(3)LD条数；(4)LD载入的寄存器作为内存基址的指令多重集合。
- IE按相邻`movq %fs:0,%REG`与同寄存器`addq DISP(%rip),%REG`识别；原始disp与指令长度计算GOT目标，而非用注释代替。相邻非IE的fs0载入记LD；四项比较中的寄存器/内存操作差异不会被消掉。
- LD基址跟踪在寄存器被覆盖、地址不连续、所属函数变化或控制转移时结束；不做跨分支数据流猜测。这是用户规定的直线窗口，相关操作记录数494不是把88号853条DTPOFF32重定位计数重新命名。未对窗口外的任意数据流作额外断言。

原始逐函数指令证据在`*-input-tls.json.gz`和`*-output-tls.json.gz`。所有不同项文件`*-differences.json.gz`都为空数组；每函数通过记录在`*-function-verdicts.json`。

## 3. T全量结果：PASS

|统计|输入|输出主体＋冷片段|旧节保留组（单列）|
|---|---:|---:|---:|
|含TLS/%fs指令函数|1187|1187|43|
|%fs指令|2073|2073|126|
|IE|1536|1536|1|
|LD|415|415|3|
|LD直线窗口TLS基址内存操作|494|494|3|

**1187/1187函数的四项全部相同；不同0、未映射0。** `%fs:`总数还包括直接段访问等非fs0加载，不能与1951个fs0序列混为一项。

LD覆盖378个函数：输入415处全部有`66 66 66`填充，输出主体415处全部无该填充，逐函数条数、fs指令和基址内存操作多重集合相同。没有无法对应项。按函数内多重集合建立对应，不对同一函数内完全相同的重复出现强行赋予唯一的一对一地址关系。

旧节3处有填充LD是额外保留副本，并非415处主体中的3处未重写。旧节4处fs0序列与输入同地址、同字节、同类别；全部126处旧节fs指令同样与输入同地址字节相同，并能在对应新函数的多重集合中找到同文项。证据为`*-old-copies.json`及`*-old-fs-proofs.json`。

## 4. D全量结果与GOT核对：PASS

D同样先通过辅助/发货六节相等，再独立扫描输入、输出所有可执行节。参与1187个函数，四项1187/1187相同、不同0、未映射0；IE1536、LD415、窗口内基址操作494，与T的计数相同但并非借用T结果。LD也覆盖378个函数，415处全改成无填充形式；旧节43个组、126处fs指令，其中1 IE和3 LD，独立验证与输入相同。

T/D各自的`.rela.dyn` R_X86_64_TPOFF64集合按（地址、符号、addend）输入/最终完全相同，两槽均addend=0。两项目地址不同，分别核对，不相互混用：

|项目|GOT槽|符号|输入引用|输出主体引用|旧节引用|
|---|---|---|---:|---:|---:|
|T|0x8569ce0|_ZSt15__once_callable|771|771|1|
|T|0x8569ce8|_ZSt11__once_call|765|765|0|
|D|0x8569c50|_ZSt15__once_callable|771|771|1|
|D|0x8569c58|_ZSt11__once_call|765|765|0|

输出每项目1537处IE（含旧节）的目标全部在本项目GOT集合内，集合外0；全部1536个主体IE归属函数及数量与输入相同。D补完了93号未运行的GOT/IE检查。完整动态集合见`*-GOT.json`，不合格目标文件`*-outside-G.json`均为空。

## 5. 结论、资源与结束行

没有产品差异、STOP、准备修正或重试。采用一个串行用户服务：MemoryMax=4294967296、MemorySwapMax=0、Nice=19、IOSchedulingClass=idle，分析阶段观测MemoryPeak=355065856 B；memory.events见证据，无OOM。未启动构建、BOLT或report-stale。

原始结束行：

```text
'''
stdout=(E/'compare.stdout').read_text()
text+='\n'.join(x for x in stdout.splitlines() if '已结束' in x)+'\n'
text+=(E/'supplement.stdout').read_text().splitlines()[-1]+'\n```\n'
text+='''
## 6. 读取与未读取

已读：STATUS及93号报告；92/93已保存的身份、工具argv与ELF解析器；两项目实际输入/辅助/发货ELF及符号、动态重定位；各输入/输出全部可执行节流式反汇编；本次完整TLS记录、不同项、旧节与LD映射。没有以历史PASS代替本次结果。

未访问QB/Gerrit；未读取或修改LLVM源码/提交/分支；未运行BOLT、构建、运行时TLS测试、report-stale或跨完整控制流分析；未删除或覆盖历史证据。GitHub仅正常推送本任务证据到bolt-v4。

'''+f'94 已结束 {now} status=PASS\n'
(B/'docs/bolt/94_tls_per_function.md').write_text(text)
with (B/'docs/bolt/STATUS.md').open('a') as f:f.write('''

## 2026-11-14：94号

PM定性：93号FAIL为固定data16判据的覆盖缺口，不是已发现错误；原记录不改。[94号逐函数静态核对](94_tls_per_function.md) PASS：T/D各1187/1187个函数四项多重集合完全相同，未映射/不同0。辅助BOLT ELF与最终发货clang六个可执行节全同。主体IE1536、LD415、LD基址直线窗口内存操作494；415处LD均去掉冗余data16填充，旧节另保留3 LD和1 IE。每项目GOT集合相同、1537处输出IE目标全正确。全部126处旧节fs指令与输入同地址同字节。结论适用于两项目最终发货clang；不作“无害”或任意跨控制流证明。

未运行构建/BOLT/report-stale，不访问QB/Gerrit，不改LLVM；92号report-stale仍留待PM安排。4GiB/swap0/nice19/idle串行服务；无准备修正或STOP。

'''+f'94 已结束 {now} status=PASS\n')
print('94文档 已结束',now,'status=PASS')
