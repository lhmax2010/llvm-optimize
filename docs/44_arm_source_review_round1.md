# 44 ARM Source 第一轮评审：普查、PM 裁决与修订停止记录

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

| 架构 | 归档 | 成员（ordinal / 同名序号） | define数 | module asm数 |
|---|---|---|---:|---:|
| armv7l | libLLVMABI.a | `Types.cpp.o` (0 / 1) | 0 | 0 |
| armv7l | libLLVMAnalysis.a | `TFLiteUtils.cpp.o` (117 / 1) | 0 | 0 |
| armv7l | libLLVMAnalysis.a | `DevelopmentModeInlineAdvisor.cpp.o` (37 / 1) | 0 | 0 |
| armv7l | libLLVMAnalysis.a | `ModelUnderTrainingRunner.cpp.o` (88 / 1) | 0 | 0 |
| armv7l | libLLVMDWARFLinker.a | `Utils.cpp.o` (1 / 1) | 0 | 0 |
| armv7l | libLLVMDWP.a | `DWPError.cpp.o` (1 / 1) | 0 | 0 |
| armv7l | libLLVMFrontendHLSL.a | `HLSLResource.cpp.o` (2 / 1) | 0 | 0 |
| armv7l | libLLVMMC.a | `MCAsmMacro.cpp.o` (13 / 1) | 0 | 0 |
| armv7l | libLLVMOrcShared.a | `OrcRTBridge.cpp.o` (4 / 1) | 0 | 0 |
| armv7l | libLLVMPasses.a | `CodeGenPassBuilder.cpp.o` (0 / 1) | 0 | 0 |
| armv7l | libLLVMPasses.a | `OptimizationLevel.cpp.o` (1 / 1) | 0 | 0 |
| armv7l | libLLVMSandboxIR.a | `Argument.cpp.o` (0 / 1) | 0 | 0 |
| armv7l | libLLVMSandboxIR.a | `Pass.cpp.o` (7 / 1) | 0 | 0 |
| armv7l | libLLVMSupport.a | `UnicodeNameToCodepointGenerated.cpp.o` (139 / 1) | 0 | 0 |
| armv7l | libLLVMSupport.a | `RWMutex.cpp.o` (169 / 1) | 0 | 0 |
| armv7l | libLLVMSupport.a | `AutoConvert.cpp.o` (17 / 1) | 0 | 0 |
| armv7l | libLLVMSupport.a | `zOSLibFunctions.cpp.o` (174 / 1) | 0 | 0 |
| armv7l | libLLVMSupport.a | `blake3_neon.c.o` (3 / 1) | 0 | 0 |
| armv7l | libLLVMSupport.a | `ABIBreak.cpp.o` (4 / 1) | 0 | 0 |
| armv7l | libLLVMSupport.a | `MathExtras.cpp.o` (84 / 1) | 0 | 0 |
| armv7l | libLLVMVectorize.a | `InstrMaps.cpp.o` (5 / 1) | 0 | 0 |
| armv7l | libclangBasic.a | `CharInfo.cpp.o` (4 / 1) | 0 | 0 |
| armv7l | libclangRewriteFrontend.a | `RewriteModernObjC.cpp.o` (5 / 1) | 0 | 0 |
| armv7l | libclangRewriteFrontend.a | `RewriteObjC.cpp.o` (6 / 1) | 0 | 0 |
| armv7l | libclangStaticAnalyzerCore.a | `CommonBugCategories.cpp.o` (15 / 1) | 0 | 0 |
| armv7l | liblldMachO.a | `Target.cpp.o` (27 / 1) | 0 | 0 |
| aarch64 | libLLVMABI.a | `Types.cpp.o` (0 / 1) | 0 | 0 |
| aarch64 | libLLVMAnalysis.a | `TFLiteUtils.cpp.o` (117 / 1) | 0 | 0 |
| aarch64 | libLLVMAnalysis.a | `DevelopmentModeInlineAdvisor.cpp.o` (37 / 1) | 0 | 0 |
| aarch64 | libLLVMAnalysis.a | `ModelUnderTrainingRunner.cpp.o` (88 / 1) | 0 | 0 |
| aarch64 | libLLVMDWARFLinker.a | `Utils.cpp.o` (1 / 1) | 0 | 0 |
| aarch64 | libLLVMDWP.a | `DWPError.cpp.o` (1 / 1) | 0 | 0 |
| aarch64 | libLLVMFrontendHLSL.a | `HLSLResource.cpp.o` (2 / 1) | 0 | 0 |
| aarch64 | libLLVMMC.a | `MCAsmMacro.cpp.o` (13 / 1) | 0 | 0 |
| aarch64 | libLLVMOrcShared.a | `OrcRTBridge.cpp.o` (4 / 1) | 0 | 0 |
| aarch64 | libLLVMPasses.a | `CodeGenPassBuilder.cpp.o` (0 / 1) | 0 | 0 |
| aarch64 | libLLVMPasses.a | `OptimizationLevel.cpp.o` (1 / 1) | 0 | 0 |
| aarch64 | libLLVMSandboxIR.a | `Argument.cpp.o` (0 / 1) | 0 | 0 |
| aarch64 | libLLVMSandboxIR.a | `Pass.cpp.o` (7 / 1) | 0 | 0 |
| aarch64 | libLLVMSupport.a | `UnicodeNameToCodepointGenerated.cpp.o` (139 / 1) | 0 | 0 |
| aarch64 | libLLVMSupport.a | `RWMutex.cpp.o` (169 / 1) | 0 | 0 |
| aarch64 | libLLVMSupport.a | `AutoConvert.cpp.o` (17 / 1) | 0 | 0 |
| aarch64 | libLLVMSupport.a | `zOSLibFunctions.cpp.o` (174 / 1) | 0 | 0 |
| aarch64 | libLLVMSupport.a | `ABIBreak.cpp.o` (4 / 1) | 0 | 0 |
| aarch64 | libLLVMSupport.a | `MathExtras.cpp.o` (84 / 1) | 0 | 0 |
| aarch64 | libLLVMVectorize.a | `InstrMaps.cpp.o` (5 / 1) | 0 | 0 |
| aarch64 | libclangBasic.a | `CharInfo.cpp.o` (4 / 1) | 0 | 0 |
| aarch64 | libclangRewriteFrontend.a | `RewriteModernObjC.cpp.o` (5 / 1) | 0 | 0 |
| aarch64 | libclangRewriteFrontend.a | `RewriteObjC.cpp.o` (6 / 1) | 0 | 0 |
| aarch64 | libclangStaticAnalyzerCore.a | `CommonBugCategories.cpp.o` (15 / 1) | 0 | 0 |
| aarch64 | liblldMachO.a | `Target.cpp.o` (27 / 1) | 0 | 0 |

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

| PM项 | 裁决内容 | 本轮状态 |
|---|---|---|
| 1 | 未知重定位在非ALLOC前拒绝，统计仍只计ALLOC | 未实施，停于§3 |
| 2 | A64 TLS仅562/563/564/569；其余原ALLOW转PENDING | 未实施 |
| 3 | 按每个define精确核cpu/features/tune | 普查完成，必需属性缺失0；门禁未实施 |
| 4 | A64移除absolute317/580、allowed256 | 未实施 |
| 5 | 固定GNU readelf/LC_ALL=C；aeabi/CPU_arch；缺失None | 未实施 |
| 6 | ARM专用ELF边界/扩展索引解析，真ABS辨别 | 未实施 |
| 7 | 指令绝对重定位不因可写而放行，仅完整宽度指针例外 | 未实施 |
| 8 | ARM32 asm白名单与同名节多序列；A64任意asm拒绝 | 全集普查完成；A64有3条真实语句，与拟实施规则冲突，停止 |
| 9 | 显式拒-Wa, | 未实施 |
| 10 | ARM专用完整工具版本与GNU reader预检 | 未实施 |
| 11 | ARM32补PENDING13/17/18/19/109/165/166/167 | 未实施 |
| 12 | mtune源码注释、TARGET1严格ABS解释 | 未实施 |
| 13 | ARM summary记录纯机器码整档跳过身份 | 未实施 |

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

| PM项 | 本次写入内容 | 新Source证据 |
|---|---|---|
| 1 | 未知/STOP/LE检查均在非ALLOC跳过前；checked/types仅累计ALLOC | arm_pic_relocations:912起 |
| 2 | A64 TLS ALLOW精确562/563/564/569；移除的旧GD/LD/描述符片段显式PENDING | ARM_TLS_ALLOWED/LOCAL_EXEC/PENDING:783–797 |
| 3 | 每个define必须引用属性组，cpu/features/tune等于§2精确元组；无define放行 | ARM_CERTIFIED_FUNCTION_TARGET:486起；arm_function_targets:499；arm_ir_settings:706 |
| 4 | A64 absolute移除317/580、allowed移除256 | arm_pic_relocations:933–943 |
| 5 | 固定env LC_ALL=C GNU readelf -AW；aeabi与CPU_arch必需；缺项None，缺项与显式0不同 | arm_attributes:661；arm_thumb_gate:888 |
| 6 | ARM专用ELF布局/边界校验；REL/RELA、扩展数量/名称/符号索引；raw shndx==0xfff1才是真ABS；重定位offset须在目标节内 | arm_elf_layout:544；arm_symbol_section:636 |
| 7 | 指令ABS在可写ALLOC同样禁止；可写完整指针只放ARM32 2/38/55、A64 257；真ABS独立豁免 | arm_pic_relocations:947–955 |
| 8 | 两架构精确module asm白名单先于ARM32原节跟踪；同名节保留各序列；输出GLOBAL符号必需 | arm_module_asm_whitelist:526；arm_check_module_asm_symbol:650；arm_mapping_modes:863；convert:1265起 |
| 9 | -Wa,在通用-W诊断分类前显式拒绝 | arm_classify_options:430 |
| 10 | ARM专用工具完整版本匹配；dis/nm路径/SHA/版本；ARM32另验env/readelf可执行与GNU身份 | validate_arm_tools:676；convert:1210起 |
| 11 | ARM32 PENDING增13/17/18/19/109/165/166/167 | ARM_TLS_PENDING:794–797 |
| 12 | 两-mtune注释补Driver/CodeGen源码出处；TARGET1按ABS32/REL32中更严格ABS解释 | ARM_EXACT_TOKENS:375–394；arm_pic_relocations:921 |
| 13 | ARM summary增加纯机器码整档跳过的相对路径、SHA、成员数；x86不增加字段 | convert:1219–1221 |

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

| 组 | 新增测试名称（test_前缀省略）与覆盖 |
|---|---|
| TLS/重定位5项 | tls_literal_sets_and_disjointness；tls_boundary_numbers；removed_tls_and_invalid_constants_in_all_contexts；nonalloc_known_not_counted_unknown_rejected；writable_instruction_absolute_vs_pointer |
| ELF结构6项 | rel_rela_architecture_matrix；extended_count_names_and_symbol_index；decoded_65521_is_real_section_not_absolute；missing_duplicate_badcount_extended_indexes；invalid_links_tables_payloads_and_truncation；relocation_offset_and_symbol_boundaries |
| mapping/读取6项 | mapping_thumb_only；mapping_transition_deduplicated；mapping_duplicate_section_names_preserved；mapping_missing_and_out_of_bounds_rejected；reader_empty_no_aeabi_and_bad_format_rejected；missing_differs_from_zero_and_missing_vfp_valid |
| 函数/参数/asm6项 | certified_function_targets_and_data_modules；cpu_features_tune_and_missing_groups_rejected；real_command_literals_and_assembler_escape；module_asm_exact_and_whitespace_only；module_asm_all_other_statements_rejected；module_asm_output_global_symbol_required |
| 工具/x86隔离5项 | matching_full_versions_and_gnu_reader；disassembler_nm_version_mismatch；non_gnu_reader_rejected；x86_fixed_constants_and_original_function_objects；x86_actual_convert_success_failure_all_arm_functions_blocked |

最后一项mock全部ARM函数为抛异常，实际调用x86 convert的native整档跳过成功与thin拒绝路径；它没有模拟全量3853次bitcode转换，不能代替下一步真实x86回归。（证据：ToolIsolationTests；E2/revision-metadata.json记录41个ARM模块完整测试名。）

## 10. 复验状态：停止后不继续执行

| 任务 | 本轮结果与不可外推的范围 |
|---|---|
| 宿主全套测试 | FAIL，95项中94通过；无第三次重跑 |
| ARM32根python全套测试/版本记录 | NOT RUN，宿主门禁第二次失败后停止 |
| x86 225档/3864成员/完整索引/3853flags | NOT RUN；旧§12 PASS不绑定5608aa5e新候选 |
| ARM32 210档重新转换、含asm的2成员GLOBAL符号 | NOT RUN；没有新after SHA/真实符号状态 |
| A64 212档重新转换、含asm的3成员GLOBAL符号 | NOT RUN；没有新after SHA/真实符号状态 |
| 两架构after SHA与docs/40 §12逐档相同 | UNKNOWN（未执行）；不能沿用旧消费者作为本候选认证 |
| 消费者三套与两种strip | 本轮未重跑，亦未以“SHA相同”为由沿用认证；旧证据仍仅认证1620 |
| ARM32 105/106共享库-z text、GNU/lld、dlopen | NOT RUN |
| x86最终产物的同module asm成员只读核查 | NOT RUN；按第三步停止，不声称符号存在/缺失 |

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

| E2下文件 | 用途 |
|---|---|
| candidate-before.py、tests-before.py | 本轮编辑前的原件副本 |
| protected-start.json、final-integrity.json | 生产Source/spec/patch/用户配置未变；候选/测试新SHA |
| iostream-evidence.json | 两ARM根头文件路径、SHA、编号摘录 |
| revision-metadata.json、source-isolation.json | diff计数/摘要、函数行号、测试名、未改函数AST核对 |
| run_tests.py、unit-tests-host.log、unit-tests-host-initial-result.json | 首轮完整命令与95项结果 |
| test-helper-correction.diff/json | 唯一辅助修正的依据与diff |
| unit-tests-host-retry.log、unit-tests-final-result.json、stop-result.json | 第二次FAIL、实际解释器、停止边界 |
| lock-acquired.json、lock-released.json、final-processes.json、final-mountinfo.txt | 独占与退出回收、无本任务残留 |
| gerrit-356639-ls-remote.* | 只读完整提交号 |

## 12. 收尾与后续条件

项目两把锁已由持锁进程正常释放（2026-10-10 20:34:34+08:00），收尾扫描没有本任务测试/构建进程残留；本轮未启动scope或采样器、未创建任何挂载。没有构建、转换真实归档、打包、清盘、改宿主配置、改spec或推Gerrit。用户原有gbs配置改动保持原样且不提交。（证据：E2/lock-released.json、final-processes.json、final-integrity.json。）

当前可供评审的是**未通过全套测试的候选5608aa5e、测试与完整diff**；不能更新356627的生产附件。继续前需要明确处置既有取消测试的失败，随后才可重新启动测试与x86/ARM门禁；本任务没有授权自动第三次尝试。原1620的历史认证不作废，也不移植为5608的认证。第五步文档按要求完成并推送，停止报告保持可复核。
