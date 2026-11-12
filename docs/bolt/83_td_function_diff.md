# 83. T/D BOLT 输入的逐函数规范化差异

结论：**PASS（差异描述与比较器三项已知答案通过）**。不作因果判断。两边各147113个函数符号记录，99048个规范化后相同、47997个仅重定位目标或addend不同、68个屏蔽后机器码不同；只在一边存在的0个。源文件聚合不可得，记UNKNOWN，不猜测原因。

## 1. 输入与工具

只比较74号保留的两份 BOLT 输入，未比较最终clang。输入大小/SHA均核对通过：

|项目|字节|SHA256|
|---|---:|---|
|T|226816920|ae3d837d862673b03c3c4718f6746f6986d8abe2078bad426b97905258b91a5c|
|D|226782848|bf15cf062439714651809cd3b5ca82619407081adca64ceb65699e6ccae50501|

[路径与SHA](../../tools/bolt/results/night-82-84-20261113/83/inputs.json)；[平台工具路径、loader、库路径及SHA](../../tools/bolt/results/night-82-84-20261113/83/platform-tools.json)。小夹具使用74号T根自带clang/lld 22.1.8，经该根loader运行；没有使用宿主clang/lld，没有运行LLVM构建。

已读：v9指定章节、STATUS、74号§8.7及输入SHA、保全的objdump函数记录（仅BOLT输入）、两份ELF的符号/节/重定位。未读：最终clang反汇编、QB网站、LLVM仓库；没有运行llvm-bolt。

## 2. 比较器

[compare_functions.py](../../tools/bolt/results/night-82-84-20261113/83/compare_functions.py)解析ELF64小端x86-64：取可执行节中已定义的STT_FUNC/STT_GNU_IFUNC；按每个符号的value/size取范围。重定位按真实字段宽度置零，另比较（相对函数偏移、类型、规范化符号名、addend）。未知宽度、字段越界或跨函数边界拒绝。无名STT_SECTION用节名标识，不混为空名。

只剥离名称末尾的ThinLTO .llvm.<数字>；同名按节名和地址顺序的出现序号对齐。没有修改指令操作数、没有忽略重定位元组、没有反汇编文本地址归一化。8种实际可执行节重定位：2、4、9、19、20、21、41、42，均在宽度表内。

**覆盖边界：** 本轮统计单位是函数符号记录，含别名；74号统计单位是objdump识别的标签，不能直接把147113和144380相减当作新增函数。两边各337个零长度函数符号只比较空范围/元数据，**没有已知函数字节可作代码等同性证明**；不推断其真实长度。99048相同中含这337个空范围记录，非空范围相同为98711。[计数范围](../../tools/bolt/results/night-82-84-20261113/83/counting-scope.json)、[零长度清单](../../tools/bolt/results/night-82-84-20261113/83/zero-size-symbols.json)。

## 3. 已知答案三项

[验证程序](../../tools/bolt/results/night-82-84-20261113/83/validate_comparator.py)、[完整argv](../../tools/bolt/results/night-82-84-20261113/83/fixture-commands.jsonl)、[源码与小产物](../../tools/bolt/results/night-82-84-20261113/83/fixtures/)、[逐项JSON](../../tools/bolt/results/night-82-84-20261113/83/known-answer-results.json)。

- (a) T与只读复制出的ELF：147113/147113相同，0差异，复制后重新SHA核对。
- (b) 只把changed函数的加数7改为9：恰好1个机器码不同函数changed，其余2个相同。
- (c) 同源ThinLTO只加-g：local_fn后缀分别12306362497720474350和17132353996625038966，证明模块身份变化；三函数规范化后全部相同。未因未发生哈希改变而空过测试。

原文：

~~~text
a PASS 147113
b PASS
c PASS [['local_fn.llvm.12306362497720474350'], ['local_fn.llvm.17132353996625038966']]
已结束 2026-11-13T00:44:30.554645+08:00 comparator-known-answers
~~~

准备问题1次：解析ld.lld符号链接后以lld通用名调用，版本查询退出1（generic driver）；保留ld.lld别名通过同一loader调用即成功，工具目标SHA不变。旧输出保留，[说明](../../tools/bolt/results/night-82-84-20261113/83/tool-path-fix.txt)。未修改比较规则或测试期望。

## 4. T/D 实物结果

|类别|数量|
|---|---:|
|T函数符号记录|147113|
|D函数符号记录|147113|
|规范化字节与重定位元组完全相同|99048（含337空范围）|
|只差重定位目标或addend|47997|
|屏蔽后机器码/长度不同|68|
|只差重定位偏移/类型结构|0|
|只在T / 只在D|0 / 0|

[实物原文](../../tools/bolt/results/night-82-84-20261113/83/td.stdout)、[完整差异清单](../../tools/bolt/results/night-82-84-20261113/83/td/differences.json.gz)、[68项机器码差异](../../tools/bolt/results/night-82-84-20261113/83/machine-code-68.json.gz)、[两边函数清单](../../tools/bolt/results/night-82-84-20261113/83/td/)。

两份输入均没有.debug/.zdebug节；68个差异函数没有可用的STT_FILE原源文件标识。因此按源文件/目录聚合的前50项为 **UNKNOWN**，可归属0、未知68。[聚合检查](../../tools/bolt/results/night-82-84-20261113/83/source-aggregation.json)。没有用C++命名空间冒充源文件，也没有借助其他身份的调试文件。

## 5. 74号各3543个未配对名字的核实

原始名称多重集合差集两边均为3543；其中两边3543/3543都带末尾.llvm.<数字>。剥离后按名称、节和出现序号能配上3543对，剩余两边均0。[摘要](../../tools/bolt/results/night-82-84-20261113/83/old-3543-summary.json)、[原名/剩余完整清单](../../tools/bolt/results/night-82-84-20261113/83/old-3543-full-lists.json.gz)。

这是名称对应关系的实测，不解释T/D机器码差异的原因，不推断调试模式或快照导致差异。

## 6. 遗留与原始材料

D的-report-stale失配名单：**待做，需资源报备**，单进程约10GB超过本轮8G，未运行。337个零size符号的字节覆盖及68项源文件定位未完成；无因果实验、无析因构建。

大文件清单见[artifacts.json](../../tools/bolt/results/night-82-84-20261113/83/artifacts.json)。T自比较副本226816920字节超过GitHub单文件限制，仅记录本地路径/大小/SHA；其余完整JSON清单gzip保存，未删除任何中间文件。所有分析服务串行8G/swap0/CPU400%/nice19/idle IO。

83 已结束 2026-11-13T00:47:25.773770+08:00 status=PASS
