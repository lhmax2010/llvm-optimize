# 44 ARM Source 第一轮评审：普查、PM 裁决与修订停止记录

**续三完成（2026-10-11）：事实核查、修正后的宿主99项与根内分类验收、x86全量不变性、两ARM复验、105/106实跑和x86只读符号核查全部完成。Source未改；两ARM全部after SHA与§12相同，沿用旧消费者/strip。ARM根内AS限制不生效仍为开放问题。详见§18–§27；以下此前停止状态完整保留为历史。**

**当前状态（续二）：600例取消诊断PASS；授权小修后宿主99/99 PASS，ARM根94/99 PASS、2 FAIL+3环境ERROR，按第三步门禁停止。全量x86/两ARM复验与符号只读核查未执行。详见§13–§17；下方原有“最新/本轮”文字完整保留为此前停止记录。**

**最新状态（续接，2026-10-10）：第二步 ARM Source 修订已写入；第三步宿主测试第二次仍 FAIL，按“同一步骤第二次失败即停止”结束。** 95 项中 94 PASS，失败为既有 `test_g_failed_leader_descendants_are_killed`，读取后代进程状态为 `R (running)`、断言要求不存在或 `Z`。没有第三次尝试、没有改共用 Commands；ARM 根测试、x86 全量回归、两 ARM 重新转换和消费者、105/106 夹具、x86 module asm 只读实验均 NOT RUN。新候选未认证，不能取代历史1620或生产6bd。详见§7–§12；本页§0–§6完整保留首轮普查与当时停止结论，里面的“本轮”指此前普查轮。（证据：E2/unit-tests-host-retry.log、stop-result.json。）


日期：2026-10-10。起点 `ddc73105dbd46348c650414e7e48bfd95c5309e9`。

**本轮停在只读普查之后、Source 修订之前。** 51个“无函数属性”成员都没有函数定义，第一步第1项通过；全量函数属性也符合预期。但AArch64真实输入有 **3条 module asm**，均为 `.globl _ZSt21ios_base_library_initv`。它们直接触及本轮第二步第8项“aarch64出现任何module asm即失败”的新规则。未把符号声明自行豁免，未修改Source后再用已知不满足策略的输入长时间转换；第二至第四步未执行。**这是只读查明的新策略与输入冲突，不是已运行新Source后的转换失败，也不是重判旧消费者结果。** 第五步的独立Gerrit评审材料已完成，见docs/45。（证据：E/census-result.json、module-asm-all.json、policy-stop.json；用户本轮第二步第8项及运行方式。）

需要PM后续决定的是：是否允许这条特定的AArch64全局符号声明，以及对应认证边界/测试。当前未修改输入、未增加例外、未请求无人值守确认。旧1620候选的既有PASS只适用旧规则，不能证明新规则全量可通过。（出处：docs/40 §12、docs/43 §5；本轮policy-stop.json。）

## 0. 身份、范围和方法

W=`/home/linhao/Toolchain/development/llvm-optimize`。
E=`W/temp/arm-source-review-round1-20261010`，本轮全部原始输出只留本机。

| 项目 | 身份/路径 |
|---|---|
| 原候选Source，仍未改 | `tools/llvm_static_archives_arm_trial.py`；`1620a8da778062216bea61f6ac43eb6b64df9963b2d5778058be6ca7b31a7607` |
| 原ARM测试，仍未改 | `tools/test_arm_archive_trial.py`；`7e1dc9510bba6fbacecab26ae3ff129448ba389eb138fd39dbcb9d1c719132f6` |
| x86生产Source，仍未改 | `tools/llvm_static_archives_source.py`；`6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557` |
| ARM32输入 | `W/temp/arm-archive-standard-build-20261010/armv7l-input/usr/lib`，210档；旧普查在同证据目录armv7l-ir-census |
| AArch64输入 | `W/temp/arm-archive-tls-thumb-20261010/aarch64-input/usr/lib64`，212档；旧普查在同证据目录aarch64-ir-census |
| R32 | `/var/tmp/llvm-optimize-arm-c1-20261010/gbs-libraries-armv7l/local/BUILD-ROOTS/scratch.armv7l.0` |
| R64 | `/var/tmp/llvm-optimize-arm-tls-aarch64-20261010/gbs-aarch64/local/BUILD-ROOTS/scratch.aarch64.0` |
| 用户配置，未暂存 | `gbs_llvm.conf`，`28f1caf93cd39738a7da1e0da8d5f945f7372963bb9823a507f9157294272169` |

开场只有用户的 ` M gbs_llvm.conf`；没有覆盖或提交它。生产Source、两份评审patch、W/llvm/spec的起始摘要见E/protected-start.json。持有本项目原有两锁路径，没有接触隔离旧混合根。（证据：starting-state.txt、processes-start.txt、lock-acquired.json。）

旧普查只保留目标属性/元数据，不保留全部define与module asm，因此本轮从输入副本重新只读反汇编，未重建LLVM、未编译、未转机器码。每次按旧普查记录的成员offset/size读取，并先核SHA相同；重名成员以ordinal+name+occurrence区分。使用原根的accel llvm-dis、loader和库，命令原样记录在每成员JSON：

```sh
prlimit --as=4294967296:4294967296 --   "$R/emul/lib64/ld-linux-x86-64.so.2"   --library-path "$R/emul/lib64:$R/emul/usr/lib64"   "$R/emul/usr/bin/llvm-dis" - -o -
```

输入经stdin传入，不执行clang或ar。先串行检查51个无属性成员，再4 workers遍历两架构全部bitcode；单命令超时600s。全量只读阶段沿用18GiB/swap0、nice15/ionice3与30秒保护采样，源码/归档原件不写。（证据：census_gate.py、census_all.py、census-plan.json、各成员argv。）

计数规则：只数`define`，不把`declare`算作函数定义；解析每个define引用的#属性组，逐函数计target-cpu/features/tune。对LLVM22实际单行define头做格式断言，全部通过；原始define头、行号与属性组都保存。module asm不按目标节筛选，所有行都统计，保留IR转义原文及解码文本；统计声明指令`.globl`，不将其误称为机器指令。（证据：full-census/<架构>/<归档>/<ordinal>.json；census_all.py。）

## 1. 51个无函数属性成员：全部无define

以下逐成员来自gate-result.json；ordinal为0起，同名序号为1起。51项的define数与module asm数均为0，所以没有触发用户第一步第1项的停止条件。这里的“无函数属性”不是“有函数却忘记目标属性”。（证据：gate-ir中的51份完整.ll及gate-result.json。）

[51项逐成员完整表](44_census_tables.md)，因正文50KB上限原样移出；历史证据与结论不变。

## 2. 全部函数目标属性：精确值与逐值计数

| 架构 | bitcode成员 | 函数定义 | 缺target-cpu | 缺target-features | 缺tune-cpu | 完整组合种数 |
|---|---:|---:|---:|---:|---:|---:|
| armv7l | 3683 | 484265 | 0 | 0 | 484265 | 1 |
| aarch64 | 3699 | 329616 | 0 | 0 | 0 | 1 |

ARM32不要求tune-cpu，缺失符合LLVM22 ARM驱动忽略-mtune的既有源码依据；AArch64要求cortex-a53。本轮所有必需属性均存在。下面是不同取值的完整集合，不使用省略号；同一组合内每个字段的出现次数都等于该行count。（证据：census-result.json architectures.*.attribute_values/combinations；docs/39 §1.3。）

### armv7l

```text
count = 484265
target-cpu = generic
target-features = +armv7-a,+d32,+dsp,+fp64,+neon,+read-tp-tpidruro,+thumb-mode,+vfp2,+vfp2sp,+vfp3,+vfp3d16,+vfp3d16sp,+vfp3sp,-aes,-fp-armv8,-fp-armv8d16,-fp-armv8d16sp,-fp-armv8sp,-fp16,-fp16fml,-fullfp16,-sha2,-vfp4,-vfp4d16,-vfp4d16sp,-vfp4sp
tune-cpu = <缺失>
```

### aarch64

```text
count = 329616
target-cpu = generic
target-features = +aes,+crc,+crypto,+fp-armv8,+neon,+outline-atomics,+sha2,+v8a,-fmv
tune-cpu = cortex-a53
```

以上仅登记白名单的实测依据；由于§3冲突，未把这些值写入候选Source常量。（证据：protected-start.json及最终文件身份核对。）

## 3. 所有module asm及停止点

完整全集只有以下一种原文，ARM32出现2次、AArch64出现3次；没有其他opcode或额外多行statement。它是汇编器符号声明，本轮不会因“看起来不生成指令”而绕开用户禁止任何AArch64 module asm的规则。（证据：module-asm-all.json、census-result.json。）

```llvm
module asm ".globl _ZSt21ios_base_library_initv"
```

| 架构 | 归档 / 成员 | ordinal / 同名序号 | IR行 | 指令 | 次数 |
|---|---|---|---:|---|---:|
| aarch64 | libLLVMAnalysis.a / `MLInlineAdvisor.cpp.o` | 80 / 1 | 6 | `.globl` | 1 |
| aarch64 | libLLVMCodeGen.a / `MLRegAllocEvictAdvisor.cpp.o` | 137 / 1 | 6 | `.globl` | 1 |
| aarch64 | libarcher_static.a / `ompt-tsan.cpp.o` | 0 / 1 | 6 | `.globl` | 1 |
| armv7l | libLLVMAnalysis.a / `MLInlineAdvisor.cpp.o` | 80 / 1 | 6 | `.globl` | 1 |
| armv7l | libLLVMCodeGen.a / `MLRegAllocEvictAdvisor.cpp.o` | 137 / 1 | 6 | `.globl` | 1 |

AArch64三项的输入与本次llvm-dis输出摘要如下，均经输入成员SHA核对；详细define/attrs/原始asm可由对应JSON复核：

- `libLLVMAnalysis.a` / `MLInlineAdvisor.cpp.o`：成员SHA `92d8e0158ae2a3d19b27035b14c6254dbce0b9efc5748ce81aa35491ca9ffd05`；IR SHA `0725856dbac42474fb4dc0c38116e1a7a05210687c800d7bacffdde99417d78d`。证据 `E/full-census/aarch64/libLLVMAnalysis.a/80.json`。
- `libLLVMCodeGen.a` / `MLRegAllocEvictAdvisor.cpp.o`：成员SHA `ef37ca302541e91a4926f4243b7fd7fa7d5875153f3e616d55a733f1537839f5`；IR SHA `fc7d3b8cc193f4adb599507d64991eb430ad1d5e7ee31cdb71bfe2e48c26e981`。证据 `E/full-census/aarch64/libLLVMCodeGen.a/137.json`。
- `libarcher_static.a` / `ompt-tsan.cpp.o`：成员SHA `177ecfe8113cdcdd55486ca824d5762a527cb3a5ddecd71b50935d8b42907220`；IR SHA `4d7495fb8f822019be2bc816b3fb4bb90e37a4e03f0f87e68252a2568bd7bb3b`。证据 `E/full-census/aarch64/libarcher_static.a/0.json`。

**停止判断。** 第一阶段采集成功，不是解析器、辅助脚本或工具故障；但真实AArch64语料不满足第二步第8项拟实施的硬规则。按“规定之外停止／产品层面失败不重试”的总约束，在Source编辑前止步：不擅自把`.globl`认作例外，不删除IR语句，不仅转换其余成员，不用历史消费者PASS代替本轮规则。因而没有“先改规则再跑”的新Source SHA，也未触发辅助脚本一次修复例外。后续若PM授权可从本普查证据继续，不需重建LLVM。（证据：policy-stop.json；用户本轮第一、二步及运行方式。）

这不是声称现有1620 Source会拒绝这些输入：该版AArch64分支没有本轮拟加的“任何module asm拒绝”门禁，历史§12通过与本次发现并不矛盾。docs/43的module_asm_checked=0是ARM32可执行节模式比较统计，不等于两架构文本IR没有module asm。（出处：候选Source:485–552、582–613、675–701；docs/43 §5；本轮全集。）

## 4. 评审采纳项与实施状态

意见来源统一为**用户转述的Codex、Claude Code两家评审及PM合并裁决**；输入未给逐条原作者，不虚构归属。下表记录拟采纳内容，本轮全部未写入代码，不能标成“已修复”。（出处：本轮任务背景与第二步。）

[完整历史表格](44_census_tables.md)见附件§4：首轮普查后的评审采纳状态（历史），原数据与判定未改。

## 5. 测试与全量复验状态

| 要求 | 本轮结果 |
|---|---|
| 51成员定义/asm前置普查 | PASS，51均0/0 |
| 两架构全量define/目标属性/asm普查 | 采集PASS；新A64策略与3条语句冲突STOP |
| Source修订、新SHA、相对1620完整diff | NOT RUN；Source仍1620，差异为空，无外置diff文件 |
| 新增测试、原有测试、ARM32根python执行 | NOT RUN；本轮运行0项Source测试，未称67项重跑通过 |
| x86 225档/3864成员/3853flags回归 | NOT RUN；docs/40 §12历史PASS保持历史身份 |
| ARM32、AArch64全量重新转换/after SHA对比 | NOT RUN；未产生新after SHA，无法宣称全同或不同 |
| 消费者与两种strip证据沿用条件 | 未满足“新SHA全量相同”的前提；不把旧证据记作本轮复验 |
| 105/106共享库及dlopen夹具 | NOT RUN |
| 第五步两Gerrit补丁材料包 | 独立执行；docs/45只整理已有证据，不受上述停止影响 |

## 6. 本轮原始输出、资源与收尾

全量普查仅运行llvm-dis：成员7,382，函数定义813,881；只读脚本wall302.640097秒，scope入口304.098888秒，MemoryPeak6,487,060,480 B，18 GiB cap、swap0；exit0，problems为空，sampler/log-reader均回收。这些是普查过程记录，不是转换或编译性能结果。（证据：census-result.json、census-scope/outcome.json、commands.log。）

| E下文件 | 作用 |
|---|---|
| protected-start.json、starting-state.txt、processes-start.txt | 开始身份与工作树；用户配置单独保留 |
| lock-acquired.json、hold_lock.py | 本项目独占记录 |
| census_gate.py、gate-result.json、gate-ir/ | 51成员门禁；逐成员完整IR、stderr、SHA、命令 |
| census_all.py、census-plan.json | 全量只读遍历、约束及实际argv |
| full-census/<架构>/<归档>/<ordinal>.json | 输入成员身份、IR SHA、所有define原文/行号、attrs、全部module asm |
| census-result.json、module-asm-all.json、policy-stop.json | 全量计数、5条asm定位、新规则冲突停止判断 |
| census-scope/ | 时间、资源、命令日志、原始stdout/stderr与回收；通用包装器文件名build.log不表示执行了构建 |

未改候选Source、测试、x86共用函数、spec、两份Gerrit补丁、W/llvm或配置；不构建、转换、打包、清盘、推Gerrit。只发布报告与STATUS。第五步已完成，docs/45独立汇集既有两补丁证据。收尾final-integrity.json确认上述受保护文件摘要全相同；census scope已inactive，sampler/log-reader回收，lock-released.json记录两项目锁已释放，final-processes.json确认本任务进程与挂载残留0。本轮没有创建GBS根或挂载。

## 7. 续接授权、输入与符号声明来源

本次续接起点 `b2ea0f9cb885c1a7a719e1acd02c3fea7fc7d5ac`，E2=`W/temp/arm-source-review-continue-20261010`。PM已解除§3的旧冲突：两架构仅允许解码并去首尾空白后恰为 `.globl _ZSt21ios_base_library_initv` 的 module asm；不能删除声明，转换产物必须保留同名GLOBAL符号（预期UND）。先前51项与全量普查沿用，不重做。其余13项修订及失败停止规则不变。（来源：用户本次附件“PM裁决”“第二步第8项”；§1–§3。）

本轮只读核对两根实际头文件，GCC安装版本均为14.2.0；两个`iostream` SHA均为 `405900b25b2ecfda0e3ff3fd52c44b89df95d3fb89987235291abaec4a522d00`：

| 根内路径 | 行号与含义 |
|---|---|
| R32/usr/lib/gcc/armv7l-tizen-linux-gnueabi/14.2.0/include/c++/iostream | 75–77：init_priority可用时初始化放在编译库；78–82：init_priority与_GLIBCXX_SYMVER_GNU条件下，82行为该.globl语句 |
| R64/usr/lib64/gcc/aarch64-tizen-linux-gnu/14.2.0/include/c++/iostream | 同上，82行逐字相同 |

`__extension__ __asm (".globl _ZSt21ios_base_library_initv");` 是实际声明。注释记录这两个根内路径、GCC版本与行号；“GCC13起”的历史起点采用PM给定前提，本轮没有另查GCC历史。证据E2/iostream-evidence.json包含完整编号摘录，R32/R64绝对路径见§0。

用户配置仍SHA `28f1caf93cd39738a7da1e0da8d5f945f7372963bb9823a507f9157294272169`，开场已有的git改动未修改/暂存；生产Source、spec、两评审补丁全保持原SHA。E2/protected-start.json与final-integrity.json可逐项核对。本轮未进入构建根执行任何测试或命令，只读上述头文件。

## 8. 13项修订：实现记录与认证边界

评审来源仍为用户转述的Codex/Claude Code合并意见；输入没有逐条原评审作者，以下以本次PM编号为唯一可核对来源，不虚构三方归属。**“已写入”只描述代码实现，整套测试未通过，不称认证完成。** Source行号属于下列新SHA。（证据：本次任务第二步；Source与外置diff。）

完整明细原样移至 [docs/44表格附件](44_census_tables.md) 的§8：13项修订实施明细，正文其余说明与历史判定不变。

x86隔离：相对1620，原有非ARM函数体除`convert`与`policy_for_arch`两个分派点均AST相同；`classify_options/ir_settings/pic_relocations/validate_tools/Commands/install`等原函数未改。分派的x86 settings返回原`ir_settings`函数本体，工具预检仍调用原`validate_tools`。生产6bd的共用函数体也逐项AST相同。此项只证明源码隔离，**不替代225档的产物回归**。（证据：E2/source-isolation.json；本轮测试`test_original_functions_are_identical`、`test_x86_actual_convert_success_failure_all_arm_functions_blocked`。）

| 文件 | SHA256 |
|---|---|
| 新ARM候选 tools/llvm_static_archives_arm_trial.py | `5608aa5e2fa655370ae722d1ea1685f4b9b181eae4b24e41ead756b9353d6e28` |
| 修订测试 tools/test_arm_archive_trial.py | `4b721e8131f302a75866264df59ad8f7d61ddb1c9e1ccd6cf24d37c03156a04b` |
| 外置完整统一diff docs/44_arm_source_round1.diff | `5bdd4b6b4e93a76c3a8a509cc4ddaaf4503094335b113e08c05d03c740982abc` |
| x86生产Source（未改） | `6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557` |

完整diff相对1620，三行上下文，479行、+270/-88、26730字节；为保证本报告≤50KB而外置，见[完整diff](44_arm_source_round1.diff)。旧版本在E2/candidate-before.py，新旧AST/文件摘要在E2/revision-metadata.json与final-integrity.json。代码与测试随本报告提交供评审，**新候选未通过完整门禁，不是可提交的生产Source**。

## 9. 测试、一次辅助修正与最终停止

保留此前54项共用测试和13项ARM测试（后者修复合成ELF的symtab→真实字符串表链接、固定TLS期望值、Thumb输出格式），新增28项，共95项。测试内TLS集合、目标属性及x86常量采用字面量；ELF结构矩阵含65521扩展实节对真ABS负对照。源文件语法可由Python3.9语法解析；本轮宿主解释器版本原文在E2/stop-result.json，**未运行ARM32根python，不推断其实际环境测试结果**。（证据：两个宿主测试日志、test_arm_archive_trial.py、revision-metadata.json。）

运行命令（两次相同runner，只是第二次修正测试期望）：

```sh
python3 temp/arm-source-review-continue-20261010/run_tests.py
```

runner将`llvm_static_archives_source`测试模块绑定到候选Source，运行原九个模块。完整95个测试名与输出在E2/unit-tests-host.log及unit-tests-host-retry.log；用例中的正负探针不会构建LLVM/打包或做全量转换。（证据：run_tests.py；测试原文。）

| 次数 | 总数/通过/失败/错误 | 耗时 | 失败点与处理 |
|---|---|---:|---|
| 首次 | 95/94/1/0 | 13.374秒（runner 13.374，日志精度） | 新增x86常量测试漏写旧有-g；不是Source变化 |
| 唯一一次辅助修正后 | 95/94/1/0 | 13.377秒 | 旧取消/后代回收测试见R状态；本步骤第二次失败，STOP |

### 9.1 辅助测试缺陷：只修期望，不改Source

首次固定值列表遗漏`-g`，生产6bd及原1620的BACKEND_FLAGS原本均含`-g`，新候选也相同。只把固定字面量补为原真实值，没有删检查或改产品。E2/test-helper-correction.json与test-helper-correction.diff保存只读依据和完整修正；首轮结果另存unit-tests-host-initial-result.json，第二次未覆盖首轮日志。依据本次允许的辅助脚本缺陷条款，只重跑一次。

### 9.2 第二次失败原文与边界

```text
FAIL: test_g_failed_leader_descendants_are_killed
  (test_static_archives_source_v2.CancellationTests)
File "tools/test_static_archives_source_v2.py", line 226
    self.assertIn('Z', state)
AssertionError: 'Z' not found in 'State:\tR (running)'
Ran 95 tests in 13.377s
FAILED (failures=1)
```

该既有测试启动退出7的父进程与忽略SIGTERM的后代；期望Commands返回后后代已不存在或处于Z。观察到R是失败断言当时的快照。**根因UNKNOWN**：本轮没有证据把它定性为调度竞态，也没有证据证明是本次ARM改动造成；原测试与共用Commands都未改。不通过增加睡眠、改期望或单测第三次重跑来放行。41项ARM/分派测试在第二轮均PASS，另一个共用测试失败，所以总体仍FAIL。（证据：unit-tests-host-retry.log；tools/test_static_archives_source_v2.py:211–226；source-isolation.json。）

### 9.3 新增28项测试索引

完整明细原样移至 [docs/44表格附件](44_census_tables.md) 的§9.3：新增28项测试索引，正文其余说明与历史判定不变。

最后一项mock全部ARM函数为抛异常，实际调用x86 convert的native整档跳过成功与thin拒绝路径；它没有模拟全量3853次bitcode转换，不能代替下一步真实x86回归。（证据：ToolIsolationTests；E2/revision-metadata.json记录41个ARM模块完整测试名。）

## 10. 复验状态：停止后不继续执行

[完整历史表格](44_census_tables.md)见附件§10：前次测试停止后的复验状态（历史），原数据与判定未改。

生产x86 Source6bd的`ir_settings`不解析module asm，`check_symbols`只比较定义外部符号，不能据此证明`.globl`引入的UND引用被保留。这是代码审查边界；本轮要求的docs/35产物符号核查未执行，结果UNKNOWN，不能拿ARM头文件声明推断x86产物。已在docs/45 §5独立披露。（证据：生产Source:275–329、499–521；本轮stop-result.json。）

## 11. Gerrit只读身份补全与原始证据

允许的只读查询已成功，未fetch/推送Gerrit，也未改两patch：

```sh
GIT_TERMINAL_PROMPT=0 \
GIT_SSH_COMMAND='ssh -o BatchMode=yes -o NumberOfPasswordPrompts=0 -o ConnectTimeout=30' \
timeout 60 git ls-remote \
  ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm \
  refs/changes/39/356639/1
```

```text
b0465d099164a8f8c1ddd406e6f74c2ada8f9f9f	refs/changes/39/356639/1
```

退出0，stderr为空。该完整号替换docs/45原短号，不与本地format-patch封套号混写。（证据：E2/gerrit-356639-ls-remote.txt、gerrit-356639-ls-remote.stderr。）

[完整历史表格](44_census_tables.md)见附件§11：前次Gerrit材料身份核对（历史）；原判定未改。

## 12. 收尾与后续条件

项目两把锁已由持锁进程正常释放（2026-10-10 20:34:34+08:00），收尾扫描没有本任务测试/构建进程残留；本轮未启动scope或采样器、未创建任何挂载。没有构建、转换真实归档、打包、清盘、改宿主配置、改spec或推Gerrit。用户原有gbs配置改动保持原样且不提交。（证据：E2/lock-released.json、final-processes.json、final-integrity.json。）

当前可供评审的是**未通过全套测试的候选5608aa5e、测试与完整diff**；不能更新356627的生产附件。继续前需要明确处置既有取消测试的失败，随后才可重新启动测试与x86/ARM门禁；本任务没有授权自动第三次尝试。原1620的历史认证不作废，也不移植为5608的认证。第五步文档按要求完成并推送，停止报告保持可复核。


## 13. 续二：取消测试诊断（2026-10-10）

本节起为新授权任务，保留§1–§12原文与历史停止。证据E3=`/home/linhao/Toolchain/development/llvm-optimize/temp/arm-source-cancel-diagnosis-20261010`。取得项目两把锁；用户原有gbs配置改动保持原样。独立诊断使用候选5608aa5e的原样Commands，生产6bd及仓库测试均未改；场景与旧测试相同：父进程启动忽略SIGTERM的后代，0.1秒后退出7。（证据：E3/starting-state.txt、protected-start.json、lock-acquired.json、diagnose_cancellation.py。）

### 13.1 一次辅助诊断修正

初次诊断到普通组第58例时，辅助脚本把`X (dead)`误当作非Z存活状态，得到错误停止；该例首读X、两个待处理掩码0，5.540ms内消失。只读本机`/usr/share/man/man5/proc_pid_status.5.gz:96–106`明确X为dead，故按辅助缺陷条款修正一次：初读存活判定排除X；最终门禁仍严格要求消失或Z，X不能直接通过最终门禁。所有真正存活非Z状态仍须SIGKILL待处理位。未改Commands、信号、3秒期限或5ms轮询。旧58例保留但不计入600例；修正后两组从零各跑300次。（证据：E3/diagnostic/quiet/057/observation.json、proc-state-man-evidence.txt、diagnostic-helper-fix.json/.diff、diagnose_cancellation-before-fix.py。）

### 13.2 正式诊断结果

| 条件 | 样本 | 首读R / 存活非Z | 存活且SIGKILL待处理 | 存活但无SIGKILL | 3秒内消失/Z | 最长 / p99（ms） |
|---|---:|---:|---:|---:|---:|---:|
| 普通 | 300 | 4 / 4 | 4 | 0 | 300 | 5.430058 / 5.312265 |
| 另加4个CPU负载进程 | 300 | 4 / 4 | 4 | 0 | 300 | 5.368736 / 5.287699 |

p99按全部300例（含首读已终止）最近秩计算；耗时从Commands抛出后到首次观察消失/Z，5ms轮询提供观测上界，不是精确内核死亡时刻。首读状态全分布： `quiet: {'None': 246, 'Z': 48, 'R': 4, 'X': 2}`； `cpu4: {'Z': 51, 'None': 242, 'X': 3, 'R': 4}`；None表示/proc已不存在。所有X均另行等到消失/Z。

| 条件/序号（0起） | PID | SigPnd | ShdPnd | 消失/Z观测耗时ms |
|---|---:|---|---|---:|
| quiet/150 | 1999189 | `0000000000000000` | `0000000000000100` | 5.312265 |
| quiet/186 | 1999457 | `0000000000000000` | `0000000000000100` | 5.413135 |
| quiet/259 | 1999976 | `0000000000000000` | `0000000000000100` | 5.302628 |
| quiet/294 | 2000219 | `0000000000000000` | `0000000000000100` | 5.210187 |
| cpu4/187 | 2001599 | `0000000000000000` | `0000000000000100` | 5.277261 |
| cpu4/208 | 2001794 | `0000000000000000` | `0000000000000100` | 5.272392 |
| cpu4/213 | 2001878 | `0000000000000000` | `0000000000000100` | 5.287699 |
| cpu4/279 | 2003008 | `0000000000000000` | `0000000000000100` | 5.317995 |

**定性：预注册场景证实测试时序假设问题。** 全部8个首读存活样本的第9号信号位0x100已在ShdPnd中，600例全在3秒内消失/Z，未发现预注册反例。这支持修正测试，不是证明Commands会同步等到全部后代消失。生产Commands在已回收父进程的情况下，发出SIGKILL的同一轮可break，确有这项边界。（证据：生产Source:437–453；E3/diagnostic-retry/observations.jsonl、各例observation.json、summary.json。）

正式诊断wall 1900.553228秒（含scope回收）；18GiB/swap0、nice15/ionice3、30秒采样/宿主2GiB保护，scope峰64,118,784B，无OOM，四CPU负载进程与采样器均已回收。日志复用限流工具的命名不代表发生LLVM构建。下一步仅按授权修改测试与ARM保留节索引；此提交时Source/tests尚未改变。（证据：E3/diagnostic-retry-scope/{plan,launch,outcome,memory-summary}.json。）


## 14. 续二：测试修正与ARM保留节索引小修

诊断阶段已先提交推送`9093af2`，随后才编辑。取消测试仍使用原场景：Commands抛出后立即快照；不存在、Z、或SigPnd/ShdPnd含0x100至少满足一个；继而每5ms轮询，3秒内必须消失/Z。没有删除断言、只加sleep或改Commands；测试首读条件按用户原文，未把X额外加入接受集合（诊断中观察到X的事实另见§13.1）。

ARM专用`arm_symbol_section`对原始0xff00–0xfffe：仅0xfff1/0xfff2返回section_index=None，其余拒绝；is_absolute仅由原始0xfff1决定。原始0xffff仍从SYMTAB_SHNDX解码，解码65521仍为真实节而非ABS。mapping显式排除None；PIC不把该符号做节匹配，只有真ABS可豁免绝对重定位，COMMON仍受原PIC门禁。相对5608仅这两个函数AST变化，PIC仅增说明注释；全部生产共用函数与Commands AST不变。（证据：E3/source-revision.json、Source与本次git diff。）

新增4项固定字面量测试（原95→99）：
- `test_common_has_no_section_and_is_not_absolute`。
- `test_absolute_has_no_section_and_remains_absolute`。
- `test_other_reserved_symbol_sections_rejected`。
- `test_common_mapping_never_matches_real_section_65522`。

覆盖两架构COMMON无节且非ABS、ABS无节仍豁免、保留0xff00/0xfff3/0xfffe拒绝，以及大于65522节的独立ELF夹具：XINDEX=$t→真实65522为正例；只把raw改为SHN_COMMON后不得匹配该节，须报缺mapping。既有XINDEX=65521负对照保留。

| 文件 | 新SHA256 |
|---|---|
| tools/llvm_static_archives_arm_trial.py | `e2c2ebfa7272c6549f9be977861985ff597d3564dd26caf72438155622e30e0d` |
| tools/test_arm_archive_trial.py | `555d0e1dce12f9196347cd943d3f98e9a9fee67b88046ec02f469de2d3d7c9c6` |
| tools/test_static_archives_source_v2.py | `cddf8da7c29fa23814c7ca3548e20b4a9dc3ffd98106719f66b94d2690a41b6a` |
| docs/44_arm_source_round1.diff | `0e7c7b8eb1cf5d559ad053d0e43a43dd0c9c651578129fa655aa6553e79a2b74` |

相对1620的完整三行上下文diff已更新外置附件：484行、+275/-88、27056字节。此小修仍是待认证候选，不替换生产6bd或上传的两份patch。

## 15. 续二：第三步测试结果与停止

| 环境 | 解释器 | 总数 | PASS | FAIL / ERROR | wall |
|---|---|---:|---:|---:|---:|
| 宿主 | Python3.12.3 / GCC13.3.0 | 99 | 99 | 0 / 0 | 13.395422s |
| armv7l构建根 | Python3.14.2 / Clang22.1.8 | 99 | 94 | 2 / 3 | 18.802692s |

宿主一次全套PASS；ARM根也只跑一次，没有失败后修改或重跑。两边45项ARM/分派测试全PASS，含新增4项；旧54项共用测试在根内有以下5项问题。根内工具身份只读file显示python3.14/prlimit/as均ARM32 ELF。根内`/proc/self/status`不可见，因此后代测试虽显示ok，不能作为根内后代状态可见性的独立认证。未挂载proc、安装工具或修改根环境来绕过。（证据：E3/unit-tests-host.log、unit-tests-final-result.json、unit-tests-armv7l.log、armv7l-environment.json、armv7l-executable-identities.txt、armv7l-environment-limits.json。）

[完整历史表格](44_census_tables.md)见附件§15：续二根内五项问题（历史）；原判定未改。

根内完整版本原文：`3.14.2 (main, Oct 1 2026, 21:46:23) [Clang 22.1.8 ]`。不能把32位环境下读回-1自行宣告等价于所要求的4GiB，也不把SIGTERM结果直接定性为已证实的启动时延。原单测临时目录退出已自行回收，未额外重跑探针取得更好的结果。（证据：E3/armv7l-unit-tests-final-result.json；完整根内日志。）

运行方式：将当前tools Python文件同字节复制到R32独立`/home/abuild/arm-source-cancel-tests-20261010/tools/`；runner仍运行九个原模块，把production模块名绑定候选。复制清单逐文件SHA在E3/root-tests-manifest.json；没有改构建树、spec或工具。

```sh
python3 temp/arm-source-cancel-diagnosis-20261010/run_tests.py
sudo -n /usr/sbin/chroot --userspec=1000:1000 \
 /var/tmp/llvm-optimize-arm-c1-20261010/gbs-libraries-armv7l/local/BUILD-ROOTS/scratch.armv7l.0 \
 /bin/sh -c 'cd /home/abuild/arm-source-cancel-tests-20261010 && python3 run_tests.py'
```

**第三步STOP。** 三个环境ERROR单列后仍有两个运行失败，不满足“能运行的必须PASS”。未改x86共用函数/Commands、未改变时间/内存断言、未在本步骤动用修正重跑。第一步唯一辅助修正仅用于诊断器识别X；它不授权把根内这两个FAIL记成PASS。（证据：E3/stop-result.json。）

## 16. 续二：第四步未执行项目与证据边界

[完整历史表格](44_census_tables.md)见附件§16：续二停止后的未执行清单（历史）；原判定未改。

## 17. 续二：回收、完整性与下一步

项目锁在2026-10-10 21:57:41+08:00正常释放。四CPU负载进程/两次诊断scope采样器均回收；最终扫描无本任务残留进程、无新增挂载、两把锁不存在。新证据与根内测试副本保留，未做磁盘清理。（证据：E3/lock-released.json、final-processes.json、final-mountinfo.txt、两个scope/outcome.json。）

生产Source6bd、工作区spec、两份已上传patch及旁附Source、用户GBS配置与开场SHA一致；用户配置既有git改动不提交。未重建LLVM、未打包/运行BOLT/做性能校准/构建Chromium/推Gerrit。docs/44原有全部内容保持，并追加本轮事实；完整diff与两个测试文件随Source提交。docs/45记录取消不等待后代消失的边界，同时保留x86 module asm未核查的缺口。（证据：E3/final-integrity.json、source-revision.json；git暂存清单。）

继续所需条件：先裁决根内两个共用测试失败的环境/断言契约，补齐必要测试工具与/proc可见性方案，然后重新明确测试及后续复验授权；本轮不自行变更这些条件。新e2c2ebfa候选尚未完成产物认证，不作为356627更新附件。


## 18. 续三：根内事实核查与PM裁决

证据E4=`/home/linhao/Toolchain/development/llvm-optimize/temp/arm-source-root-probes-20261010`。本轮Source固定e2c2ebfa，无代码修改；取得项目锁，无竞争构建进程。PM将两个GNU time测试和x86 as夹具归为根内环境不适用；AS限制若实证不生效，记开放问题而不阻塞宿主离线复验；timeout须先证实启动时延再修测试。历史FAIL保留。（证据：本轮任务；E4/protected-start.json、preflight-processes.txt、lock-acquired.json。）

### 18.1 临时proc与一次辅助驱动修正

GBS后端实际采用`mount -n -tproc none $BUILD_ROOT/proc`（宿主/usr/lib/build/build:602、1140；init_buildsystem:162–163）。首次辅助驱动直接sudo宿主mount退出1：`sudo: a password is required`，未挂载、未跑探针。只读sudo -n -l证明免密表允许root chroot，不允许该宿主mount调用；/bin与/usr/bin的mount同inode，非换路径即可解决。按辅助缺陷条款修正一次，通过既有免密chroot在根内执行相同proc挂载/卸载，未改权限、门禁或系统配置；同时按只读文件清单把版本查询由binfmt分派器改为根内真实qemu。修正后整个事实步骤一次通过。（证据：E4/initial-facts-commands.json、sudo-authorizations.txt、readonly-helper-diagnosis.json、helper-fix.diff/json。）

每根分别执行`sudo -n /usr/sbin/chroot R /bin/mount -n -tproc none /proc`，探针用`--userspec=1000:1000`，finally保证`... /bin/umount /proc`。两次卸载exit0，前/中/后mountinfo完整保留；不使用lazy卸载、不改binfmt/sysctl。（证据：facts-commands.json及armv7l/aarch64-mountinfo-{before,during,after}.txt。）

### 18.2 Python启动与资源限制实测

ARM32根内已启动的python runner逐次Popen另一个python3，子进程`import signal,time; signal.signal(SIGTERM,SIG_IGN)`后立即输出monotonic_ns；从Popen前到处理器安装后的时间，共20次，不加prlimit启动开销。20/20均大于0.15秒：min159.557960ms、median164.570515ms、p95 168.314379ms、p99/p100 170.289930ms。证实原timeout=.15不能保证该环境先建立忽略TERM的前提；这项测量不声称已捕获上轮失败的同一调度轨迹。按用户公式p100<2.5s，测试timeout取5s。（证据：E4/startup_probe.py、startup-20.stdout、facts-result.json。）

| 根 | prlimit --as=4294967296后AS soft/hard | --as=1073741824后AS | --nofile=256后nofile | QEMU | /emul原生prlimit/util-linux候选 |
|---|---|---|---|---|---|
| armv7l | unlimited/unlimited | unlimited/unlimited | 256/256 | qemu-arm 9.2.3 | 均未发现 |
| aarch64 | unlimited/unlimited | unlimited/unlimited | 256/256 | qemu-aarch64 9.2.3 | 均未发现 |

每项完整命令为`chroot --userspec=1000:1000 R /usr/bin/prlimit <选项> -- /bin/cat /proc/self/limits`。AS两次未施加而nofile正常，依预注册判据证实PM推断；1GiB与AArch64对照排除了仅以ARM32的4GiB数值溢出解释全部结果。QEMU版本后缀均`Tools:qemu:9.2.3_opensuse160`。binfmt分别指向/usr/bin/qemu-arm-binfmt与qemu-aarch64-binfmt，flags P、offset0；原文/魔数/掩码见E4/binfmt-registration.json，未修改注册。/emul全路径清单见两份emul-files.json；按prlimit/taskset/ionice/setsid/flock/nsenter/unshare等util-linux名称核对均无候选，所以没有可报告的原生prlimit文件身份或归属包，不猜来源。（证据：facts-result.json、六份*-as4/as1/nofile.stdout、*-qemu-version.stdout、facts-commands.json。）

## 19. 开放问题：ARM构建根内地址空间限制不生效

事实限于上述两根/QEMU9.2.3：目标prlimit设置AS后，目标cat观察到unlimited；其他nofile限制可施加。生产Commands默认4GiB AS在这条模拟执行路径不能按既有测试证明生效。这是ARM生产集成的开放问题，不能把cgroup的整体限额称为逐编译进程AS限制。（证据：§18.2；生产Source Commands.run；PM本轮裁决3。）

x86路径不变的依据：本轮生产/候选Source及Commands均无修改，宿主上轮99测试中同一4GiB读回断言PASS（§15）；本轮将再跑宿主测试与全量不变性。后续离线ARM转换仍从宿主启动原生x86 accel工具，不经目标prlimit，因此用户允许继续该离线验证；这不认证未来ARM根内%install限流。可选方向供外部评审：在/emul提供/认证原生prlimit（当前没有）；明确记录目标AS未生效并另设计整体/单进程保护；评估QEMU路径或其他限制机制。各方向尚未选择/实施，不在本轮改Commands/安装包/放宽限额。（证据：§18；docs/40 §12工具路由；本轮约束。）


## 20. 续三：仅修超时测试，宿主99项通过

事实阶段已先提交`c4c635c`。仅改`test_g_success_and_timeout_reaped`：子进程安装SIGTERM忽略后写ready标记，再sleep30；timeout固定5秒（§18 p100=0.170290s）；异常后必须ready存在，否则报“环境未建立测试前提”，exit=-SIGKILL、wall≥8秒、children为空均保留。没有接受SIGTERM或修改Commands/Source。（证据：本提交测试diff。）

宿主一次99/99 PASS，wall 18.269634s；候选Source仍e2c2ebfa，生产6bd不变。测试文件SHA `13af0bed62f9ceb1972c6f4878e6488e8a20b6544daa4c6d632339b69b8722d9`。随后才开始临时proc环境下的根内分类验收。（证据：E4/unit-tests-host.log、unit-tests-final-result.json、run_tests.py。）


## 21. 续三：临时proc下根内99项分类验收

测试修正提交`93a3a5b`后，ARM32根Python3.14.2一次运行99项，23.663830s：95 PASS、1 FAIL、3 ERROR；原始unittest仍exit1/FAIL，不篡改。三个ERROR分别为两个辅助模块缺/usr/bin/time、x86 as --64夹具环境不适用；唯一FAIL是AS读回[[-1,-1],[0,0]]，按§18实证及PM裁决记已知环境发现。除此之外95项全部PASS，含修正的timeout与后代回收测试，故本任务分类门禁PASS。（证据：E4/armv7l-test-records.json逐项记录、root-tests-classified.json、armv7l-unit-tests-final-result.json。）

根内/proc/self/status可见；挂载前/中/后mountinfo完整保存，finally卸载exit0。复制的测试文件与宿主同SHA，未改那四项测试、未安装工具、未改Source。完整argv和原始异常见E4/root-test-commands.json、unit-tests-armv7l.stderr；解释器见armv7l-environment.json。[99项逐项名称、原始结果与分类](44_census_tables.md)已完整列出。随后执行宿主离线复验，不把此分类验收称为ARM生产AS限流通过。


## 22. 续三：x86全量不变性PASS（2026-10-11）

根内分类记录先推送`744a1fe`。输入E5/x86-input逐档before SHA均与docs/35锚点一致；用固定e2c2ebfa重新转换到E4/x86-final-conversion，225档after SHA、3,864个有序成员（ordinal/name/occurrence/SHA）、318,543项完整符号→成员索引及3,853组后端flags顺序均完全一致。3,853 bitcode转换、11原机器码保留；允许缺失W=1,920，强符号缺失0，与历史一致。（证据：E4/x86-final-input-check.json、x86-final-comparison-progress.json、x86-final-regression-result.json；锚点E5/anchor-metadata.json指向docs/35 ba-install-conversion-evidence/summary.json。）

沿用18GiB cgroup/swap0、4 workers、每命令4GiB AS、nice15/ionice3、30秒采样及宿主<2GiB保护。转换wall 1694.557544s，scope 1761.789200s；scope峰 12474638336B（含文件缓存）、宿主最低可用 17857900544B；memory.events各项0，采样器和日志线程均回收。没有LLVM重建、%install或打包。（证据：E4/run_x86_final.py、x86-plan.json、x86-regression-scope/outcome.json、memory-summary.json及全部命令JSON。）

为保持本页≤50KB，§1的51项表、§8修订明细表、§9.3测试索引原样移至[表格附件](44_census_tables.md)，没有删历史内容或重判。迁移摘要见E4/census-table-move.json、history-tables-move.json。


## 23. 续三：ARM32全量复验与证据沿用

x86里程碑先推送`823dd96`。210个输入档与构建树/输入副本摘要、accel clang/dis/nm身份均重核；宿主执行固定e2c2ebfa，输出E4/armv7l-conversion。结果：210档、3,690成员（3,683 bitcode转换+7原机器码原样保留）；bitcode归零、成员身份/次序、454,301条精确外部定义符号索引、PIC/重定位/强符号门禁均PASS；允许缺W=2,953，强符号缺失0。3,683次Thumb参考门禁及完整ARM属性比较均PASS，26个无函数属性成员逐个包含在内；无triple覆盖警告。（证据：E4/armv7l-input-check.json、armv7l-conversion-result.json、armv7l-full-attributes.json、各成员relocations/command/thumb-gate.json。）

**210/210个after SHA与docs/40 §12全部相同。** 旧基准为`temp/arm-archive-tls-thumb-20261010/armv7l-conversion/summary.json`，逐档值见E4/armv7l-comparison-result.json。依本轮授权，不重跑三套消费者及两种strip；沿用该目录`consumers-native-rerun`、`consumers-gnu`、`consumers-llvm`各7项PASS和`strip-gnu`、`strip-llvm`结果，其SHA及状态另存E4/armv7l-reused-evidence.json。没有把旧native首次辅助失败当成成功，也不把沿用写成新实测。105/106新夹具仍须另跑。

| 白名单成员 | ordinal | 转换后目标符号状态 |
|---|---:|---|
| libLLVMAnalysis.a / MLInlineAdvisor.cpp.o | 80 | GLOBAL、NOTYPE、DEFAULT、UND；raw/decoded节索引0 |
| libLLVMCodeGen.a / MLRegAllocEvictAdvisor.cpp.o | 137 | 同上 |

目标符号均`_ZSt21ios_base_library_initv`，真实ELF解析info=16/other=0，value=size=0；这是全局未定义引用，未声称生成了定义。（证据：E4/armv7l-comparison-result.json的module_asm_symbols。）

Thumb实际调用`/usr/bin/env LC_ALL=C /usr/bin/readelf -AW <对象>`，来源为宿主x86_64 ELF，不是ARM根工具；GNU Binutils for Ubuntu 2.42，readelf SHA `64c58e15274bbbb5153f31078e455e9e77ee5f51489e709bba5bb788ce9df2b0`。完整版本与实际argv在conversion/readelf-version.txt、readelf-version-command.json、每成员converted/reference-readelf.json；file证据E4/host-readelf-file.txt。

资源规则同§22。转换及额外校验wall 1836.073389s，scope 1874.627240s；scope峰9775529984B（含缓存），宿主最低可用17527791616B，无OOM，采样器/日志线程回收。（证据：E4/armv7l-conversion-scope/outcome.json、memory-summary.json。）


## 24. 续三：AArch64全量复验与证据沿用

ARM32里程碑先推送`ca66525`。AArch64输入/工具身份重核后，宿主运行同一e2c2ebfa，输出E4/aarch64-conversion：212档、3,706成员（3,699 bitcode转换+7原机器码保留）；bitcode归零、成员身份/次序、307,758项完整索引、PIC/重定位/函数属性/强符号门禁均PASS。允许缺失W=1,698、强符号缺失0。（证据：E4/convert_aarch64.py、aarch64-conversion-result.json、conversion/summary.json及各成员命令/检查JSON；这里conversion指该架构输出子目录。）

**212/212个after SHA与docs/40 §12全部相同**，逐档值在E4/aarch64-comparison-result.json；旧基准为`temp/arm-archive-tls-thumb-20261010/aarch64-conversion/summary.json`。依授权沿用其`aarch64-consumers-native/gnu/llvm`各7项PASS和`aarch64-strip-gnu/llvm`结果，未重跑；文件摘要与PASS核对记录在E4/aarch64-reused-evidence.json。

| 白名单成员 | ordinal | 转换后`_ZSt21ios_base_library_initv` |
|---|---:|---|
| libLLVMAnalysis.a / MLInlineAdvisor.cpp.o | 80 | GLOBAL / NOTYPE / DEFAULT / UND，raw/decoded节索引0 |
| libLLVMCodeGen.a / MLRegAllocEvictAdvisor.cpp.o | 137 | 同上 |
| libarcher_static.a / ompt-tsan.cpp.o | 0 | 同上 |

连同§23的ARM32两项，5个白名单成员全部保留该符号（info16、other0、value/size0），不是推测原声明对应输出。（证据：E4/aarch64-comparison-result.json的module_asm_symbols。）

资源同§22：转换wall1574.055995s、scope1616.626950s；scope峰9717932032B（含缓存）、宿主最低可用17461518336B，无OOM；采样器/日志线程回收。至此两ARM字节一致性均闭合，但ARM根内AS开放问题仍未解决；未打包、未更新Gerrit补丁。（证据：E4/aarch64-conversion-scope/outcome.json、memory-summary.json；§19。）


## 25. 续三：ARM32 TLS105/106真实链接与dlopen

两ARM复验里程碑已推送`065cf5b`。新汇编夹具以lld上游`llvm/lld/test/ELF/arm-tls-ldm32.s`的tlsldm/tlsldo表达式构造真实取TLS值函数；目标文件实有R_ARM_TLS_LDM32(105)、R_ARM_TLS_LDO32(106)及R_ARM_CALL。R32中分别用GNU ld与lld执行`-shared -Wl,-z,text,-z,defs`，各生成1条R_ARM_TLS_DTPMOD32、无TEXTREL；独立小主程序dlopen/dlsym调用，两者均输出`tls_value=37`、exit0。不是只生成未被执行的重定位。（证据：E4/tls-105-106/fixture.s、main.c、object-relocations.stdout、dynamic-bfd/lld.stdout、run-bfd/lld.stdout、result.json；完整逐命令argv/time/RSS见*.command.json。）

clang、头文件、链接器、运行库均来自保留的Tizen ARM32根，工具沿现有accel路由、目标程序经既有qemu；宿主18GiB/swap0 scope，编译外层4GiB AS、链接无AS上限。临时proc挂载/卸载均exit0，前中后mountinfo保留；未改系统配置。证据为E4/tls_ld_fixture.py、tls-plan.json、tls-fixture-scope/outcome.json和tls-105-106/mount-commands.json。

## 26. 续三：x86 module asm只读核查及辅助修正

对象是docs/35最终解包N=`W/temp/toolchain-archivefix-v2-final`，而非本轮未strip转换输出。扫描225个最终归档中的目标符号，并无条件核查ARM普查中三个源成员在x86输入中的对应项；用实际原始bitcode反汇编确认语句，不因最终符号未找到就漏掉对应输入。最终查到3个bitcode成员的IR都含`module asm ".globl _ZSt21ios_base_library_initv"`：

| x86归档 / 成员 | ordinal / 同名序号 | docs/35最终ELF符号状态 |
|---|---|---|
| libLLVMAnalysis.a / MLInlineAdvisor.cpp.o | 80 / 1 | GLOBAL / NOTYPE / DEFAULT / UND（节索引0） |
| libLLVMCodeGen.a / MLRegAllocEvictAdvisor.cpp.o | 137 / 1 | 同上 |
| libarcher_static.a / ompt-tsan.cpp.o | 0 / 1 | 同上 |

另外libLLVMAnalysis.a的原机器码成员`xla_compiled_cpu_function.cc.o`（1/1）与`executable_run_options.cc.o`（4/1）最终也有同样GLOBAL/UND符号；它们没有LLVM IR，module asm来源记UNKNOWN_NO_IR_NATIVE，不由符号反推原文本。3个bitcode项证明当前固定输入保留了声明，不把生产6bd“不检查module asm”扩称为任意asm受支持。（证据：E4/x86-module-asm-retry/result.json、各成员original.ll、symbols.txt及命令JSON；文件选择范围亦写入result.json。）

本步骤首次辅助脚本错误地把原机器码xla成员交给llvm-dis，收到`file doesn't start with bitcode header`；只读核查原成员kind=machine、魔数7f454c46、提取SHA与源d53085c5…一致，证实是检查驱动类型分派缺陷，不是转换Source或bitcode产品失败。按本步骤一次额度，只修辅助脚本：实际bitcode才反汇编；机器码仍保留完整符号观察并明确无IR。Source/Commands不动、门禁不减，在新目录重跑一次PASS。初次日志、诊断、完整diff和两个scope/outcome均保留于E4/x86-symbol-helper-diagnosis.json、x86-symbol-helper-fix.diff/json、x86-symbol-scope、x86-symbol-retry-scope。本轮共两处辅助步骤各修一次：§18挂载入口与本节类型分派；无第二次失败/产品失败重试。

## 27. 续三：收尾、完整性与边界

本轮完成全部授权步骤，无产品层面的停止。Source仍`e2c2ebfa7272c6549f9be977861985ff597d3564dd26caf72438155622e30e0d`；相对1620的[完整diff](44_arm_source_round1.diff)原样保留，SHA仍0e7c7b8e…。生产6bd、Commands、ARM测试、spec、两已上传补丁、用户GBS配置均与开场SHA相同；代码只改§20的timeout测试。未打包/重建LLVM/清理磁盘/推Gerrit。（证据：E4/final-integrity.json；两种Source与patch的完整SHA在该文件。）

全部scope采样器与日志线程回收；事实探针、根内单测、TLS夹具的临时proc均已卸载。2026-10-11 01:18:16+08:00释放两把项目锁，01:18:45复核无本任务进程、锁或两根proc挂载残留。证据E4/scope-cleanup-results.json、lock-released.json、final-processes-locks.json、final-mountinfo.txt。所有原始输出与新转换产物保留于E4；没有重判此前历史FAIL。

宿主99/99、根内95PASS+3环境不适用+1AS发现、x86与两ARM固定输入复验闭合；§19的ARM生产AS限制问题仍待外部评审，离线产物相同不能解决根内限流。docs/45补齐x86只读结果及该边界；本轮不更新Gerrit候选、不作ARM打包验收结论。
