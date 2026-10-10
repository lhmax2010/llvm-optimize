# 44 ARM Source 第一轮评审：只读普查与新策略冲突停止记录

日期：2026-10-10。起点 `ddc73105dbd46348c650414e7e48bfd95c5309e9`。

**本轮停在只读普查之后、Source 修订之前。** 51个“无函数属性”成员都没有函数定义，第一步第1项通过；全量函数属性也符合预期。但AArch64真实输入有 **3条 module asm**，均为 `.globl _ZSt21ios_base_library_initv`。它们直接触及本轮第二步第8项“aarch64出现任何module asm即失败”的新规则。未把符号声明自行豁免，未修改Source后再用已知不满足策略的输入长时间转换；第二至第四步未执行。**这是只读查明的新策略与输入冲突，不是已运行新Source后的转换失败，也不是重判旧消费者结果。** 第五步的独立Gerrit评审材料仍须完成，见docs/45。（证据：E/census-result.json、module-asm-all.json、policy-stop.json；用户本轮第二步第8项及运行方式。）

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

未改候选Source、测试、x86共用函数、spec、两份Gerrit补丁、W/llvm或配置；不构建、转换、打包、清盘、推Gerrit。只发布报告与STATUS。第五步完成后的保护文件核对、锁与进程收尾记录追加至本节。
