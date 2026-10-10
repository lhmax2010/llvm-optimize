# 43 ARM 静态库转换 Source 外部评审包

日期：2026-10-10。本文只整理已有证据；未运行测试、构建、转换或 strip。审阅范围是候选 Source 与测试，不是批准 ARM 发布包。docs/40 保留全部历史；本文为其 §12 的独立入口。

## 1. 背景与版本边界

ThinLTO 静态归档含 bitcode，标准 GNU strip 会损坏索引，GNU ld 无 LTO/插件也不能消费 bitcode。已上传的 Gerrit **356627** 用安装阶段转换解决 x86_64 问题；本候选拟作为同一 change 的新 patchset 扩展 ARM，必须保持 x86 原有行为。当前两 ARM 仅完成构建树归档的离线功能认证；尚未执行 ARM `%install`、RPM 集成与发货验收。（docs/35、docs/36、docs/40 §12.12–12.13）

| 审阅对象 | SHA256 | 可完整下载的固定版本 |
|---|---|---|
| x86 生产 Source | `6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557` | [tools/llvm_static_archives_source.py](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/2058761dc310e7ccfac7fd5929b0c9e5be518b93/tools/llvm_static_archives_source.py) |
| ARM 候选 Source | `1620a8da778062216bea61f6ac43eb6b64df9963b2d5778058be6ca7b31a7607` | [tools/llvm_static_archives_arm_trial.py](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/2058761dc310e7ccfac7fd5929b0c9e5be518b93/tools/llvm_static_archives_arm_trial.py) |
| ARM 专项测试 | `7e1dc9510bba6fbacecab26ae3ff129448ba389eb138fd39dbcb9d1c719132f6` | [tools/test_arm_archive_trial.py](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/2058761dc310e7ccfac7fd5929b0c9e5be518b93/tools/test_arm_archive_trial.py) |

版本依据：docs/40 §12.1、§12.12；测试文件对应 `2058761` 的既有文件。全文中 **S** 指候选 Source，行号均为该 SHA；LLVM 源码依据沿用 docs/28 §1.1、docs/39 §1.3、docs/40 §12.1 已登记的版本与行号。不要混用旧候选 `6a36f173…` 或中间版本 `399000c3…` 的结果。（docs/40 §12.2）

证据路径缩写（原始 `temp/` 文件仅在工作区，不在 GitHub）：

- W=`/home/linhao/Toolchain/development/llvm-optimize`
- E12=`W/temp/arm-archive-tls-thumb-20261010`
- E11=`W/temp/arm-archive-standard-build-20261010`
- E5=`W/temp/arm-archive-stage1-20261010`
- E39=`W/temp/arm-archive-feasibility-20261009`

出处：docs/40 §5、§11、§12；docs/39 §0。外部审阅可依据本文完整摘要与仓库内 Source/测试；原始大体积证据需工作区访问，不能把本地路径当网页链接。

## 2. 设计与认证策略

### 2.1 分派、归档身份与失败行为

`policy_for_arch` 在 x86_64 返回原 `ir_settings`/`pic_relocations`，在 ARM 返回独立函数；`convert` 只在 ARM 检查 triple 覆盖警告，只在 armv7l 构建 Thumb 参考对象。原函数/类 AST 对比排除必需改动的 `convert`、`install_main`，其余保持一致；运行时 mock 将 ARM 入口设为异常，x86 分派仍通过。再用最终 SHA 做整库逐字节回归，不能仅用 AST 推定产物不变。（S:785、1018、1084；docs/40 §12.1–12.2；专项测试 DispatchTests）

按归档 header offset 识别成员，以序号、名称、同名序号保持次序；原机器码逐字节保留。bitcode 由 llvm-dis 读取记录命令与 IR 属性，再由 clang 生成 ET_REL；使用 GNU `ar qcDS`、`ar sD` 确定性重打包。索引比较的是 `(符号, 成员序号, 名称, 同名序号)` 多重集合，不是非空/条数门禁。（S:97、1018；docs/40 §12.2、§12.4、§12.10）

继承生产门禁：Python≥3.9、clang 主版本22、三个工具可执行、build 下存在 CMakeCache；thin/other/软链接归档拒绝；未知参数、错误 triple、显式 Code Model、type-test/vcall/SplitLTOUnit=1 拒绝。强符号按名称保留；W/V/U及小写缺失另记，不能称“所有符号完全相同”。命令默认600秒、编译AS4GiB、4worker；失败取消进程组；安装状态 CONVERTED→INSTALLING→PASS，逐档临时文件校验后 os.replace，失败记 INSTALL_FAILED；这不是全库事务回滚。（S:485、808、928、953、1166；docs/40 §12.2 的历史回归）

### 2.2 参数分类表

`IR`=语义/属性/元数据已在IR；`补回`=转换显式重建；`无关`=IR→机器码阶段无需重放。IR 类不等于所有 driver 默认值都可忽略：优化级和 PIC 模型仍显式传入。此表是固定配方的认证策略，不是任意编译命令重放器。（docs/28 §1.1–1.2；docs/40 §11.4、§12.9；S:395–558）

ARM 专有项逐 token 如下；§11 的 `-mthumb=IR` 已由 §12 的决定取代。

| 架构 | token | 类别及处理 | 已登记依据（路径相对 W/llvm） |
|---|---|---|---|
| armv7l | `-march=armv7-a` | IR，精确值必需，triple/features | clang/lib/Driver/ToolChains/Arch/ARM.cpp:275–353,540–573；CodeGenModule.cpp:2929–2992；docs/39 §1.3 |
| armv7l | `-mthumb` | **补回**，必需；禁止 driver 改成ARM模式 | clang/lib/Driver/ToolChain.cpp:1276,1291；Arch/ARM.cpp:286,310–316,345–351；docs/40 §12.1 |
| armv7l | `-mfpu=neon` | IR，必需；拒绝 attrs 中显式 -neon | Arch/ARM.cpp:664–679；docs/39 §1.3；S:543 |
| armv7l | `-mfloat-abi=softfp` | 补回，必需；调用约定/FloatABI | ToolChains/Clang.cpp:1475–1491；CodeGen/BackendUtil.cpp:383–391；docs/39 §1.3 |
| armv7l | `-mlittle-endian` | 补回，必需；同时核验ELF端序 | Arch/ARM.cpp:34–45,275–282；docs/39 §1.3 |
| armv7l | `-mtune=cortex-a8` | 无关，本版ARM driver忽略；非必需集合成员 | Arch/ARM.cpp:660–662；docs/39 §1.3；S:375–392 |
| armv7l | `-Wp,-D__SOFTFP__` | 无关，预处理已完成 | clang/lib/Frontend/CompilerInvocation.cpp:3438–3462,4816–4865；docs/39 §1.3 |
| armv7l | `-D_FILE_OFFSET_BITS=64` | 无关，预处理已完成 | 同上；docs/39 §1.3 |
| aarch64 | `-march=armv8-a+fp+simd+crc+crypto` | IR，精确值必需，CPU/features | Arch/AArch64.cpp:200–266；docs/39 §1.3 |
| aarch64 | `-mtune=cortex-a53` | IR，必需；有tune属性时必须为cortex-a53 | Arch/AArch64.cpp:233–238；CodeGenModule.cpp:2983–2984；docs/39 §1.3；S:549 |

允许的原 driver target：ARM32 armv7l/ thumbv7 两种 Tizen gnueabi，IR仅接受 `thumbv7-tizen-linux-gnueabi`；A64两者均仅 `aarch64-tizen-linux-gnu`。其他 `-m*` 值，包括 -marm、-mcpu、hard-float，直接拒绝。末项优化必须ARM32 -Os、A64 -O3；末项DWARF必须4；四个分段/addrsig开关末项必须启用，unique-section-names/addrsig缺省true；fp-contract取末项on/off/fast，缺省on。（S:370–483；docs/40 §11.4、§12.9；docs/28 §1.2）

下面逐项列出真实记录命令的其余开关。为避免复制数千个旧源路径和宏值，`-D*`/`-I*`及其操作数按同一语法族列出；完整逐 token 原文在 E11/ir-policy-summary.json、E11/armv7l-ir-census/ 与 E12/aarch64-ir-policy-summary.json。ARM32历史表的Thumb类别按上表修正；本节不是再次执行分类。（docs/40 §11.4、§12.9）

依据索引（均为既有证据，行号相对 W/llvm）：

- O：CodeGen/BackendUtil.cpp:618–631,1131–1140，优化/ThinLTO；docs/28 §1.1。
- S：Options/Options.td:4594–4613；BackendUtil.cpp:453–466，分段；docs/28 §1.1–1.2。
- P：CodeGenModule.cpp:1469–1474；BackendUtil.cpp:618–631，PIC；docs/28 §1.1。
- F：CodeGenModule.cpp:2729–2740，ssp；docs/39 §1.3。
- E：CodeGen/CGException.cpp:477–478；BackendUtil.cpp:417–424，异常；docs/28 §1.1。
- U：ToolChains/Clang.cpp:6000–6017；CodeGenModule.cpp:1504–1505,2716–2717，unwind；docs/28 §1.1。
- V：CodeGenModule.cpp:1782–1831、1113–1115,1834–1893、6230–6235,6356–6362，可见性/插入/common；docs/28 §1.1。
- G：CodeGenModule.cpp:472–482,1105–1111；CompilerInvocation.cpp:1894–1902；BackendUtil.cpp:459–520，debug；docs/28 §1.1。
- R：CodeGenModule.cpp:8036–8043，llvm.commandline；docs/28 §1.1。
- T：ToolChains/Clang.cpp:2774,2981–2991,3240–3242；CodeGenFunction.cpp:1085–1095，strict FP；docs/28 §1.1。
- C：CompilerInvocation.cpp:3994–4010，语言；docs/28 §1.1。
- D：CompilerInvocation.cpp:2610–2750，诊断；docs/28 §1.1。
- H：CompilerInvocation.cpp:3438–3462,4816–4865，预处理；docs/28 §1.1。
- A：CompilerInvocation.cpp:2310–2385，动作/依赖路径；Driver/Driver.cpp:1541–1542，pipe；docs/28 §1.1；S:395–454，操作数/driver分类。

以上 CodeGenModule/BackendUtil/CodeGenFunction 位于 clang/lib/CodeGen；CompilerInvocation 位于 clang/lib/Frontend；ToolChains 位于 clang/lib/Driver；Options 位于 clang/include/clang。

| token | 出现架构 | 类别 | 依据索引 |
|---|---|---|---|
| `--driver-mode=g++` | 32/64 | 无关 | A |
| `-MD` | 32/64 | 无关 | A |
| `-MF` | 32/64 | 无关 | A |
| `-MT` | 32/64 | 无关 | A |
| `-O3` | 64 | IR | O |
| `-Os` | 32/64 | IR | O |
| `-Wall` | 32/64 | 无关 | D |
| `-Wc++98-compat-extra-semi` | 32/64 | 无关 | D |
| `-Wcast-qual` | 32/64 | 无关 | D |
| `-Wcovered-switch-default` | 32/64 | 无关 | D |
| `-Wctad-maybe-unsupported` | 32/64 | 无关 | D |
| `-Wdelete-non-virtual-dtor` | 32/64 | 无关 | D |
| `-Werror=date-time` | 32/64 | 无关 | D |
| `-Werror=global-constructors` | 32/64 | 无关 | D |
| `-Werror=unguarded-availability-new` | 32/64 | 无关 | D |
| `-Wextra` | 32/64 | 无关 | D |
| `-Wformat` | 32/64 | 无关 | D |
| `-Wformat-pedantic` | 64 | 无关 | D |
| `-Wformat-security` | 32/64 | 无关 | D |
| `-Wimplicit-fallthrough` | 32/64 | 无关 | D |
| `-Wmisleading-indentation` | 32/64 | 无关 | D |
| `-Wmissing-field-initializers` | 32/64 | 无关 | D |
| `-Wno-error=unused-but-set-variable` | 32/64 | 无关 | D |
| `-Wno-error=unused-command-line-argument` | 32/64 | 无关 | D |
| `-Wno-extra` | 64 | 无关 | D |
| `-Wno-long-long` | 32/64 | 无关 | D |
| `-Wno-nested-anon-types` | 32/64 | 无关 | D |
| `-Wno-noexcept-type` | 32/64 | 无关 | D |
| `-Wno-pass-failed` | 32/64 | 无关 | D |
| `-Wno-pedantic` | 64 | 无关 | D |
| `-Wno-unused` | 32/64 | 无关 | D |
| `-Wno-unused-command-line-argument` | 32/64 | 无关 | D |
| `-Wno-unused-parameter` | 32/64 | 无关 | D |
| `-Wnon-virtual-dtor` | 32/64 | 无关 | D |
| `-Woverloaded-virtual` | 32/64 | 无关 | D |
| `-Wp,-D_FORTIFY_SOURCE=2` | 32/64 | 无关 | H |
| `-Wsign-compare` | 64 | 无关 | D |
| `-Wstring-conversion` | 32/64 | 无关 | D |
| `-Wsuggest-override` | 32/64 | 无关 | D |
| `-Wwrite-strings` | 32/64 | 无关 | D |
| `-c` | 32/64 | 无关 | A |
| `-fPIC` | 32/64 | IR | P |
| `-fcolor-diagnostics` | 32/64 | 无关 | D |
| `-fdata-sections` | 32/64 | 补回 | S |
| `-fexceptions` | 32/64 | IR | E |
| `-ffunction-sections` | 32/64 | 补回 | S |
| `-flto=thin` | 32/64 | 无关 | O |
| `-fmessage-length=0` | 32/64 | 无关 | D |
| `-fno-common` | 32/64 | IR | V |
| `-fno-exceptions` | 32/64 | IR | E |
| `-fno-semantic-interposition` | 32/64 | IR | V |
| `-frecord-command-line` | 32/64 | IR | R |
| `-fstack-protector` | 32/64 | IR | F |
| `-ftrapping-math` | 32/64 | IR | T |
| `-funwind-tables` | 32/64 | IR | U |
| `-fvisibility-inlines-hidden` | 32/64 | IR | V |
| `-fvisibility=hidden` | 32/64 | IR | V |
| `-g` | 32/64 | IR | G |
| `-g2` | 32/64 | IR | G |
| `-gdwarf-4` | 32/64 | 补回 | G |
| `-isystem` | 32/64 | 无关 | A |
| `-o` | 32/64 | 无关 | A |
| `-pedantic` | 32/64 | 无关 | D |
| `-pipe` | 32/64 | 无关 | A |
| `-resource-dir` | 32/64 | 无关 | A |
| `-std=c++17` | 32/64 | IR | C |
| `-D*`、`-I*`；分离式 `-D`/`-I` 与紧随操作数 | 32/64 | 无关，保留审计不重放 | H、S:403 |
| `-isystem`/`-resource-dir`/`-o`/`-MT`/`-MF`/`-x` 的操作数 | 按记录出现 | 无关，消费一个非开关操作数；缺失拒绝 | A、S:426 |
| 首个clang路径、源/目标路径 | 32/64 | 无关；限制driver名及文件后缀 | A、S:415,453 |

未在本批显式出现的补回默认值仍重要：`-funique-section-names`（Options.td:4658–4663）、`-faddrsig`（Clang.cpp:7992–7999）、`-ffp-contract=on`（Clang.cpp:2789–2797；BackendUtil.cpp:393–405）。认证策略也识别各自否定开关，但末项禁用会失败；不是默认接受任意 -f/-fno- 项。（docs/28 §1.2；S:435–479）

本批转换命令的固定部分（不含工具路径、输入和输出）：

```text
ARM32: --no-default-config --target=thumbv7-tizen-linux-gnueabi -x ir -Os
       -ffunction-sections -fdata-sections -funique-section-names -faddrsig
       -g -gdwarf-4 -ffp-contract=on -c -fPIC
       -mfloat-abi=softfp -mlittle-endian -mthumb
A64:   --no-default-config --target=aarch64-tizen-linux-gnu -x ir -O3
       -ffunction-sections -fdata-sections -funique-section-names -faddrsig
       -g -gdwarf-4 -ffp-contract=on -c -fPIC
```

出处：S:538–558，E12/armv7l-conversion 与 aarch64-conversion 各成员 ir-settings.json。这里 -fPIC 来自本批 PIC2/PIE0；一般分支仍按模块值区分 pic/pie/non-PIC，不硬编码所有输入为 PIC。没有 -flto，也没有用宿主CPU覆盖函数属性。（docs/40 §12.4、§12.9–12.10）

### 2.3 Thumb 与参考对象

每个ARM32 bitcode成员用同一IR、原记录flags再编一个参考对象，去掉 LTO、原输入输出/依赖动作，保留预处理选项的成对操作数，追加 `-x ir -c`。比较 Tag_ARM_ISA_use、Tag_THUMB_ISA_use、Tag_ABI_VFP_args；缺失记录default(0)。module asm 所在可执行非空节比较 `$a/$t/$d` 去相邻重复的模式序列，不比较地址或机器码字节。转换或参考stderr有 `-Woverride-module`/triple覆盖文字即失败。（S:576–701；docs/40 §12.1）

源文件级汇编解析跟踪 .text/.data/.bss、.section/.pushsection/.popsection/.previous，拒绝栈不平衡或无法解析的module asm包装。真实归档的可执行module asm门禁触发数为0，只有小夹具覆盖该分支，见§5。（S:582–613；docs/40 §12.2、§12.4）

### 2.4 TLS 三类集合

下面编号均为十进制，名称完整。**ALLOW是ET_REL/PIC策略许可，不等于当前lld支持全部类型。** STOP显式集合与其余未认证TLS分开列；后者走通用未知类型路径。完整LLVM定义/lld/ABI逐号依据见docs/40 §12.1、E12/tls-source-evidence.json。动态输出重定位不自动获得输入许可。（S:562–573,770–779）

**armv7l**（docs/40 §12.1）：

ALLOW：

```text
104 R_ARM_TLS_GD32
105 R_ARM_TLS_LDM32
106 R_ARM_TLS_LDO32
```
FORBIDDEN_LE：

```text
108 R_ARM_TLS_LE32
110 R_ARM_TLS_LE12
```
STOP：显式 pending 与其余未认证 TLS：

```text
13 R_ARM_TLS_DESC
17 R_ARM_TLS_DTPMOD32
18 R_ARM_TLS_DTPOFF32
19 R_ARM_TLS_TPOFF32
90 R_ARM_TLS_GOTDESC
91 R_ARM_TLS_CALL
92 R_ARM_TLS_DESCSEQ
93 R_ARM_THM_TLS_CALL
107 R_ARM_TLS_IE32
109 R_ARM_TLS_LDO12
111 R_ARM_TLS_IE12GP
129 R_ARM_THM_TLS_DESCSEQ16
130 R_ARM_THM_TLS_DESCSEQ32
165 R_ARM_TLS_GD32_FDPIC
166 R_ARM_TLS_LDM32_FDPIC
167 R_ARM_TLS_IE32_FDPIC
```

**aarch64**（docs/40 §12.1）：

ALLOW：

```text
512 R_AARCH64_TLSGD_ADR_PREL21
513 R_AARCH64_TLSGD_ADR_PAGE21
514 R_AARCH64_TLSGD_ADD_LO12_NC
515 R_AARCH64_TLSGD_MOVW_G1
516 R_AARCH64_TLSGD_MOVW_G0_NC
517 R_AARCH64_TLSLD_ADR_PREL21
518 R_AARCH64_TLSLD_ADR_PAGE21
519 R_AARCH64_TLSLD_ADD_LO12_NC
520 R_AARCH64_TLSLD_MOVW_G1
521 R_AARCH64_TLSLD_MOVW_G0_NC
522 R_AARCH64_TLSLD_LD_PREL19
523 R_AARCH64_TLSLD_MOVW_DTPREL_G2
524 R_AARCH64_TLSLD_MOVW_DTPREL_G1
525 R_AARCH64_TLSLD_MOVW_DTPREL_G1_NC
526 R_AARCH64_TLSLD_MOVW_DTPREL_G0
527 R_AARCH64_TLSLD_MOVW_DTPREL_G0_NC
528 R_AARCH64_TLSLD_ADD_DTPREL_HI12
529 R_AARCH64_TLSLD_ADD_DTPREL_LO12
530 R_AARCH64_TLSLD_ADD_DTPREL_LO12_NC
531 R_AARCH64_TLSLD_LDST8_DTPREL_LO12
532 R_AARCH64_TLSLD_LDST8_DTPREL_LO12_NC
533 R_AARCH64_TLSLD_LDST16_DTPREL_LO12
534 R_AARCH64_TLSLD_LDST16_DTPREL_LO12_NC
535 R_AARCH64_TLSLD_LDST32_DTPREL_LO12
536 R_AARCH64_TLSLD_LDST32_DTPREL_LO12_NC
537 R_AARCH64_TLSLD_LDST64_DTPREL_LO12
538 R_AARCH64_TLSLD_LDST64_DTPREL_LO12_NC
560 R_AARCH64_TLSDESC_LD_PREL19
561 R_AARCH64_TLSDESC_ADR_PREL21
562 R_AARCH64_TLSDESC_ADR_PAGE21
563 R_AARCH64_TLSDESC_LD64_LO12
564 R_AARCH64_TLSDESC_ADD_LO12
565 R_AARCH64_TLSDESC_OFF_G1
566 R_AARCH64_TLSDESC_OFF_G0_NC
567 R_AARCH64_TLSDESC_LDR
568 R_AARCH64_TLSDESC_ADD
569 R_AARCH64_TLSDESC_CALL
572 R_AARCH64_TLSLD_LDST128_DTPREL_LO12
573 R_AARCH64_TLSLD_LDST128_DTPREL_LO12_NC
```
FORBIDDEN_LE：

```text
544 R_AARCH64_TLSLE_MOVW_TPREL_G2
545 R_AARCH64_TLSLE_MOVW_TPREL_G1
546 R_AARCH64_TLSLE_MOVW_TPREL_G1_NC
547 R_AARCH64_TLSLE_MOVW_TPREL_G0
548 R_AARCH64_TLSLE_MOVW_TPREL_G0_NC
549 R_AARCH64_TLSLE_ADD_TPREL_HI12
550 R_AARCH64_TLSLE_ADD_TPREL_LO12
551 R_AARCH64_TLSLE_ADD_TPREL_LO12_NC
552 R_AARCH64_TLSLE_LDST8_TPREL_LO12
553 R_AARCH64_TLSLE_LDST8_TPREL_LO12_NC
554 R_AARCH64_TLSLE_LDST16_TPREL_LO12
555 R_AARCH64_TLSLE_LDST16_TPREL_LO12_NC
556 R_AARCH64_TLSLE_LDST32_TPREL_LO12
557 R_AARCH64_TLSLE_LDST32_TPREL_LO12_NC
558 R_AARCH64_TLSLE_LDST64_TPREL_LO12
559 R_AARCH64_TLSLE_LDST64_TPREL_LO12_NC
570 R_AARCH64_TLSLE_LDST128_TPREL_LO12
571 R_AARCH64_TLSLE_LDST128_TPREL_LO12_NC
```
STOP：显式 pending 与其余未认证 TLS：

```text
539 R_AARCH64_TLSIE_MOVW_GOTTPREL_G1
540 R_AARCH64_TLSIE_MOVW_GOTTPREL_G0_NC
541 R_AARCH64_TLSIE_ADR_GOTTPREL_PAGE21
542 R_AARCH64_TLSIE_LD64_GOTTPREL_LO12_NC
543 R_AARCH64_TLSIE_LD_GOTTPREL_PREL19
595 R_AARCH64_AUTH_TLSDESC_ADR_PAGE21
596 R_AARCH64_AUTH_TLSDESC_LD64_LO12
597 R_AARCH64_AUTH_TLSDESC_ADD_LO12
80 R_AARCH64_P32_TLSGD_ADR_PREL21
81 R_AARCH64_P32_TLSGD_ADR_PAGE21
82 R_AARCH64_P32_TLSGD_ADD_LO12_NC
83 R_AARCH64_P32_TLSLD_ADR_PREL21
84 R_AARCH64_P32_TLSLD_ADR_PAGE21
85 R_AARCH64_P32_TLSLD_ADD_LO12_NC
86 R_AARCH64_P32_TLSLD_LD_PREL19
87 R_AARCH64_P32_TLSLD_MOVW_DTPREL_G1
88 R_AARCH64_P32_TLSLD_MOVW_DTPREL_G0
89 R_AARCH64_P32_TLSLD_MOVW_DTPREL_G0_NC
90 R_AARCH64_P32_TLSLD_ADD_DTPREL_HI12
91 R_AARCH64_P32_TLSLD_ADD_DTPREL_LO12
92 R_AARCH64_P32_TLSLD_ADD_DTPREL_LO12_NC
93 R_AARCH64_P32_TLSLD_LDST8_DTPREL_LO12
94 R_AARCH64_P32_TLSLD_LDST8_DTPREL_LO12_NC
95 R_AARCH64_P32_TLSLD_LDST16_DTPREL_LO12
96 R_AARCH64_P32_TLSLD_LDST16_DTPREL_LO12_NC
97 R_AARCH64_P32_TLSLD_LDST32_DTPREL_LO12
98 R_AARCH64_P32_TLSLD_LDST32_DTPREL_LO12_NC
99 R_AARCH64_P32_TLSLD_LDST64_DTPREL_LO12
100 R_AARCH64_P32_TLSLD_LDST64_DTPREL_LO12_NC
101 R_AARCH64_P32_TLSLD_LDST128_DTPREL_LO12
102 R_AARCH64_P32_TLSLD_LDST128_DTPREL_LO12_NC
103 R_AARCH64_P32_TLSIE_ADR_GOTTPREL_PAGE21
104 R_AARCH64_P32_TLSIE_LD32_GOTTPREL_LO12_NC
105 R_AARCH64_P32_TLSIE_LD_GOTTPREL_PREL19
106 R_AARCH64_P32_TLSLE_MOVW_TPREL_G1
107 R_AARCH64_P32_TLSLE_MOVW_TPREL_G0
108 R_AARCH64_P32_TLSLE_MOVW_TPREL_G0_NC
109 R_AARCH64_P32_TLSLE_ADD_TPREL_HI12
110 R_AARCH64_P32_TLSLE_ADD_TPREL_LO12
111 R_AARCH64_P32_TLSLE_ADD_TPREL_LO12_NC
112 R_AARCH64_P32_TLSLE_LDST8_TPREL_LO12
113 R_AARCH64_P32_TLSLE_LDST8_TPREL_LO12_NC
114 R_AARCH64_P32_TLSLE_LDST16_TPREL_LO12
115 R_AARCH64_P32_TLSLE_LDST16_TPREL_LO12_NC
116 R_AARCH64_P32_TLSLE_LDST32_TPREL_LO12
117 R_AARCH64_P32_TLSLE_LDST32_TPREL_LO12_NC
118 R_AARCH64_P32_TLSLE_LDST64_TPREL_LO12
119 R_AARCH64_P32_TLSLE_LDST64_TPREL_LO12_NC
120 R_AARCH64_P32_TLSLE_LDST128_TPREL_LO12
121 R_AARCH64_P32_TLSLE_LDST128_TPREL_LO12_NC
122 R_AARCH64_P32_TLSDESC_LD_PREL19
123 R_AARCH64_P32_TLSDESC_ADR_PREL21
124 R_AARCH64_P32_TLSDESC_ADR_PAGE21
125 R_AARCH64_P32_TLSDESC_LD32_LO12
126 R_AARCH64_P32_TLSDESC_ADD_LO12
127 R_AARCH64_P32_TLSDESC_CALL
184 R_AARCH64_P32_TLS_DTPREL
185 R_AARCH64_P32_TLS_DTPMOD
186 R_AARCH64_P32_TLS_TPREL
187 R_AARCH64_P32_TLSDESC
```

其中显式 pending：ARM32={90,91,92,93,107,111,129,130}，A64={539,540,541,542,543}；LE与这些pending在任何节（含非ALLOC、SHN_ABS）直接抛错。上表其余STOP由未认证类型规则处理；**当前Source对其余非ALLOC类型会先跳过**，详见§5，不将表格写成所有节都拒绝的实现保证。（S:770–779；docs/40 §12.1）

### 2.5 非 TLS PIC/重定位集合与判定

下列是S:728–744的完整集合；编号名称取LLVM ELFRelocs定义（docs/39 §4、docs/40 §12.1）。`narrow`是`absolute`子集；ALLOW再并上§2.4的TLS ALLOW。

**armv7l**：

absolute：

```text
2 R_ARM_ABS32
5 R_ARM_ABS16
6 R_ARM_ABS12
7 R_ARM_THM_ABS5
8 R_ARM_ABS8
38 R_ARM_TARGET1
43 R_ARM_MOVW_ABS_NC
44 R_ARM_MOVT_ABS
47 R_ARM_THM_MOVW_ABS_NC
48 R_ARM_THM_MOVT_ABS
55 R_ARM_ABS32_NOI
132 R_ARM_THM_ALU_ABS_G0_NC
133 R_ARM_THM_ALU_ABS_G1_NC
134 R_ARM_THM_ALU_ABS_G2_NC
135 R_ARM_THM_ALU_ABS_G3
```
narrow：

```text
5 R_ARM_ABS16
6 R_ARM_ABS12
7 R_ARM_THM_ABS5
8 R_ARM_ABS8
```
allowed：

```text
0 R_ARM_NONE
1 R_ARM_PC24
3 R_ARM_REL32
4 R_ARM_LDR_PC_G0
10 R_ARM_THM_CALL
11 R_ARM_THM_PC8
24 R_ARM_GOTOFF32
25 R_ARM_BASE_PREL
26 R_ARM_GOT_BREL
27 R_ARM_PLT32
28 R_ARM_CALL
29 R_ARM_JUMP24
30 R_ARM_THM_JUMP24
40 R_ARM_V4BX
42 R_ARM_PREL31
45 R_ARM_MOVW_PREL_NC
46 R_ARM_MOVT_PREL
49 R_ARM_THM_MOVW_PREL_NC
50 R_ARM_THM_MOVT_PREL
51 R_ARM_THM_JUMP19
52 R_ARM_THM_JUMP6
53 R_ARM_THM_ALU_PREL_11_0
54 R_ARM_THM_PC12
56 R_ARM_REL32_NOI
57 R_ARM_ALU_PC_G0_NC
58 R_ARM_ALU_PC_G0
59 R_ARM_ALU_PC_G1_NC
60 R_ARM_ALU_PC_G1
61 R_ARM_ALU_PC_G2
62 R_ARM_LDR_PC_G1
63 R_ARM_LDR_PC_G2
64 R_ARM_LDRS_PC_G0
65 R_ARM_LDRS_PC_G1
66 R_ARM_LDRS_PC_G2
67 R_ARM_LDC_PC_G0
68 R_ARM_LDC_PC_G1
69 R_ARM_LDC_PC_G2
96 R_ARM_GOT_PREL
97 R_ARM_GOT_BREL12
98 R_ARM_GOTOFF12
102 R_ARM_THM_JUMP11
103 R_ARM_THM_JUMP8
```

**aarch64**：

absolute：

```text
257 R_AARCH64_ABS64
258 R_AARCH64_ABS32
259 R_AARCH64_ABS16
263 R_AARCH64_MOVW_UABS_G0
264 R_AARCH64_MOVW_UABS_G0_NC
265 R_AARCH64_MOVW_UABS_G1
266 R_AARCH64_MOVW_UABS_G1_NC
267 R_AARCH64_MOVW_UABS_G2
268 R_AARCH64_MOVW_UABS_G2_NC
269 R_AARCH64_MOVW_UABS_G3
270 R_AARCH64_MOVW_SABS_G0
271 R_AARCH64_MOVW_SABS_G1
272 R_AARCH64_MOVW_SABS_G2
317 R_AARCH64_FUNCINIT64
580 R_AARCH64_AUTH_ABS64
```
narrow：

```text
258 R_AARCH64_ABS32
259 R_AARCH64_ABS16
```
allowed：

```text
0 R_AARCH64_P32_NONE
256 UNNAMED_IN_LLVM_DEF
260 R_AARCH64_PREL64
261 R_AARCH64_PREL32
262 R_AARCH64_PREL16
273 R_AARCH64_LD_PREL_LO19
274 R_AARCH64_ADR_PREL_LO21
275 R_AARCH64_ADR_PREL_PG_HI21
276 R_AARCH64_ADR_PREL_PG_HI21_NC
277 R_AARCH64_ADD_ABS_LO12_NC
278 R_AARCH64_LDST8_ABS_LO12_NC
279 R_AARCH64_TSTBR14
280 R_AARCH64_CONDBR19
282 R_AARCH64_JUMP26
283 R_AARCH64_CALL26
284 R_AARCH64_LDST16_ABS_LO12_NC
285 R_AARCH64_LDST32_ABS_LO12_NC
286 R_AARCH64_LDST64_ABS_LO12_NC
287 R_AARCH64_MOVW_PREL_G0
288 R_AARCH64_MOVW_PREL_G0_NC
289 R_AARCH64_MOVW_PREL_G1
290 R_AARCH64_MOVW_PREL_G1_NC
291 R_AARCH64_MOVW_PREL_G2
292 R_AARCH64_MOVW_PREL_G2_NC
293 R_AARCH64_MOVW_PREL_G3
299 R_AARCH64_LDST128_ABS_LO12_NC
300 R_AARCH64_MOVW_GOTOFF_G0
301 R_AARCH64_MOVW_GOTOFF_G0_NC
302 R_AARCH64_MOVW_GOTOFF_G1
303 R_AARCH64_MOVW_GOTOFF_G1_NC
304 R_AARCH64_MOVW_GOTOFF_G2
305 R_AARCH64_MOVW_GOTOFF_G2_NC
306 R_AARCH64_MOVW_GOTOFF_G3
307 R_AARCH64_GOTREL64
308 R_AARCH64_GOTREL32
309 R_AARCH64_GOT_LD_PREL19
310 R_AARCH64_LD64_GOTOFF_LO15
311 R_AARCH64_ADR_GOT_PAGE
312 R_AARCH64_LD64_GOT_LO12_NC
313 R_AARCH64_LD64_GOTPAGE_LO15
314 R_AARCH64_PLT32
315 R_AARCH64_GOTPCREL32
```

判定顺序：核验little-endian ET_REL及ARM32/64 Machine → 遍历REL/RELA与符号表 → LE/pending无条件抛错 → 跳过非ALLOC → 其余类型必须属于absolute/allowed/TLS ALLOW → 非SHN_ABS符号的narrow任何ALLOC节违规，其他absolute只在只读ALLOC违规。converted成员在PIC Level非零时拒绝该违规清单；混合归档中原机器码ARM成员出现违规直接拒绝。SHN_ABS常量例外不覆盖LE/pending。共享库 `-z text` 与运行验证是另一个独立门禁，不能由静态扫描替代。（S:704–781,1065–1095；docs/40 §12.2、§12.5、§12.11）

## 3. 相对生产 Source 的完整差异

完整统一diff（上下文3行）保存在仓库 [docs/43_arm_conversion_source.diff](43_arm_conversion_source.diff)：**492行、27663字节**，新增442行、删除6行；SHA256 `b0f8120cec5d5b578076aa27bb922a44cd229d9222142d8d5484f9060eaf00a9`。它由§1两份既有Source文本直接比较生成，是文档附件，不是修改/替换Gerrit补丁。全文嵌入会超过材料包50KB上限，因此按任务允许的替代方式外置。候选Source全文raw链接见§1；这里相对的是生产 **6bd0546a**，不是docs/40 §12.3相对旧ARM候选的diff。

## 4. 既有实测证据摘要

下述 PASS 均为已有记录，不是本次执行。单位 B/KiB/GiB、转换wall与scope wall分开；耗时只描述功能实验资源，不作性能收益结论。（docs/40 §12.2、§12.7、§12.12）

### 4.1 x86 不变性与构建/普查

| x86 最终候选回归 | 结果 | 出处 |
|---|---|---|
| 输入与docs/35 before SHA | 225/225相同 | §12.2；E12/x86-final-regression-result.json |
| 整档after SHA | 225/225相同 | 同上 |
| 有序成员身份与SHA | 3864/3864相同（3853转换、11原机器码） | 同上 |
| 完整索引/补回flags及顺序 | 225/225、3853/3853相同 | 同上 |
| 弱符号缺失 | W=1920，原策略允许，非新回归 | §12.2；E12/x86-final-conversion/summary.json |
| 转换wall / scope峰值 | 1909.148431s / 9.004063GiB | §12.2 |
| 测试 | 67项PASS，0 failures/errors；真实夹具另列 | §12.2；E12/unit-tests-final-result.json |

| 项目 | armv7l | aarch64 | 出处 |
|---|---|---|---|
| 原配方/阶段 | cb679968，标准-bc完整%build；§12复用不重建 | cb679968，标准-bc一次 | §11.3、§12.8 |
| 构建Ninja/wall | 7147/7147；1998.953884s | 7545/7545；2321.728104s | §11.3、§12.8 |
| scope峰值 | 15.335GiB | 16.417076GiB；OOM=0 | §11.3、§12.8 |
| CMake | MinSizeRel、Thin、最终-Os | Release、Thin、公共-Os被Release -O3覆盖 | §11.3、§12.8 |
| 共享库开关/目标 | LLVM、clang dylib均ON；ARM/BPF | 同为ON；AArch64/BPF | 同上 |
| 并发/保护 | 构建6/6/2，18GiB cap/swap0 | 同左 | §11.1、§12.8 |
| 实际执行方式 | 编译/链接进/emul，构建期工具经qemu | 同左，有TableGen进程记录 | §11.3、§12.8 |
| 安装规则库清单 | 210档、3690成员 | 212档、3706成员 | §11.4、§12.9 |
| bitcode/机器码/other/thin | 3683/7/0/0 | 3699/7/0/0 | 同上 |
| IR triple | thumbv7-tizen-linux-gnueabi（3683/3683） | aarch64-tizen-linux-gnu（3699/3699） | 同上 |
| PIC/PIE、DWARF | 全部2/0、4 | 全部2/0、4 | 同上 |
| 末项优化 | 全部-Os | 全部-O3 | 同上 |
| CPU/模式/tune | 3657有generic/Thumb/NEON attrs，26无函数attrs；softfp、小端、mthumb；mtune a8被忽略 | 3674有generic/cortex-a53，25无函数attrs | 同上 |
| 原命令token全集 | 11580种token/类别组合，71种switch/类别/理由；无未分类 | 11640种token/类别组合；无未分类 | E11/ir-policy-summary.json；E12/aarch64-ir-policy-summary.json |
| ARM32特例 | spec排除libarcher_static.a，不能要求225或含libarcher | 含libarcher_static.a | §11.4、§12.9清单 |

ARM32普查表是在修正Thumb分类前生成；最终命令明确补回-mthumb。两个清单均按CMake安装规则选择static-devel/libomp-devel库，**不包含clang资源目录中的compiler-rt库**。原件与输入副本均保留；候选首次ARM支持不是对所有可能ARM静态库的认证。（docs/40 §11.4、§12.4、§12.9、§12.13）

### 4.2 全量转换、索引与Thumb

| 项目 | armv7l | aarch64 | 出处（E12下） |
|---|---|---|---|
| 转换档数/成员 | 210 / 3690 | 212 / 3706 | armv7l-conversion-result.json；aarch64-conversion-result.json；§12.4、§12.10 |
| 转换/原字节保留 | 3683 / 7 | 3699 / 7 | 同上及各conversion/summary.json |
| 输出格式 | 全部ELF32 ARM ET_REL，BC=0 | 全部ELF64 AArch64 ET_REL，BC=0 | 各full-census/summary.json |
| 完整符号→成员索引 | 454301项、每档多重集合正确，身份/次序保持 | 307758项、同左 | §12.4、§12.10 |
| 强符号缺失/允许弱符号缺失 | 0 / W=2953 | 0 / W=1698 | 各conversion/summary.json及symbols.json |
| triple覆盖警告 | 0 | 0 | 各metrics.json |
| Thumb参考门禁 | 3683/3683；缺属性26/26 PASS | 不适用 | armv7l-metrics.json；各thumb-gate.json |
| 三属性与全属性 | 门禁三属性一致；独立全Tag_*检查也3683/3683一致 | 不适用 | armv7l-full-attributes.json；§12.4 |
| 缺属性26成员的三属性 | ARM_ISA=Yes、THUMB_ISA=Thumb-2、VFP_args=default(0) | 不适用 | §12.4逐成员表 |
| module asm真实触发 | 0，不能称真实全库模式分支覆盖 | ARM32专用门禁 | armv7l-metrics.json |
| 转换前→后归档字节 | 4652224292→3981756412 | 5280834808→6696311532 | 各metrics.json |
| strip前含debug成员 | 3679 | 3696 | 同上 |
| 转换wall（含ARM32参考对象） | 1800.448876s | 1544.023960s | 各conversion-result.json |
| scope wall/峰值 | 1840.142586s / 10.280182GiB | 1594.103391s / 10.988628GiB | §12.7、§12.12 |
| 单转换命令最大RSS | 1145892KiB；参考1147192KiB | 1446248KiB | 各metrics.json |

最终候选在两ARM实测期间没有再修改，因此§4.1最终SHA的x86回归覆盖同一候选。全量转换并发4、单编译AS4GiB；链接不设AS限制，由cgroup保护。所有归档通过不代表每一种策略允许的TLS/重定位都已被真实输入覆盖。（docs/40 §12.7、§12.12）

### 4.3 真实重定位类型全集

每行数量是全部转换成员加原机器码成员，按**目标节**属性分列。只读非ALLOC主要是调试段，不等于文本重定位。下表就是已有全集，未出现的类别不补0推测；两架构未知类型均0。位置、归档、成员、符号示例在各 `*-full-census/summary.json` 的examples，明细在members.jsonl。（docs/40 §12.4、§12.10）

**ARM32**（docs/40 §12.4）：

| 编号/名称 | 目标节访问 | 可加载 | 数量 |
|---|---|---|---:|
| 0 / `R_ARM_NONE` | readonly | alloc | 457370 |
| 2 / `R_ARM_ABS32` | readonly | nonalloc | 77584415 |
| 2 / `R_ARM_ABS32` | writable | alloc | 395313 |
| 3 / `R_ARM_REL32` | readonly | alloc | 233146 |
| 10 / `R_ARM_THM_CALL` | readonly | alloc | 1778253 |
| 28 / `R_ARM_CALL` | readonly | alloc | 36 |
| 30 / `R_ARM_THM_JUMP24` | readonly | alloc | 104665 |
| 38 / `R_ARM_TARGET1` | writable | alloc | 580 |
| 42 / `R_ARM_PREL31` | readonly | alloc | 461250 |
| 96 / `R_ARM_GOT_PREL` | readonly | alloc | 144469 |
| 104 / `R_ARM_TLS_GD32` | readonly | alloc | 1193 |
| 106 / `R_ARM_TLS_LDO32` | readonly | nonalloc | 25 |

**AArch64**（docs/40 §12.10）：

| 编号/名称 | 目标节访问 | 可加载 | 数量 |
|---|---|---|---:|
| 257 / `R_AARCH64_ABS64` | readonly | nonalloc | 32948462 |
| 257 / `R_AARCH64_ABS64` | writable | alloc | 396590 |
| 258 / `R_AARCH64_ABS32` | readonly | nonalloc | 66209577 |
| 260 / `R_AARCH64_PREL64` | readonly | alloc | 21 |
| 261 / `R_AARCH64_PREL32` | readonly | alloc | 314536 |
| 275 / `R_AARCH64_ADR_PREL_PG_HI21` | readonly | alloc | 288096 |
| 277 / `R_AARCH64_ADD_ABS_LO12_NC` | readonly | alloc | 236407 |
| 278 / `R_AARCH64_LDST8_ABS_LO12_NC` | readonly | alloc | 2040 |
| 282 / `R_AARCH64_JUMP26` | readonly | alloc | 103886 |
| 283 / `R_AARCH64_CALL26` | readonly | alloc | 1910650 |
| 284 / `R_AARCH64_LDST16_ABS_LO12_NC` | readonly | alloc | 245 |
| 285 / `R_AARCH64_LDST32_ABS_LO12_NC` | readonly | alloc | 1663 |
| 286 / `R_AARCH64_LDST64_ABS_LO12_NC` | readonly | alloc | 38227 |
| 299 / `R_AARCH64_LDST128_ABS_LO12_NC` | readonly | alloc | 10835 |
| 311 / `R_AARCH64_ADR_GOT_PAGE` | readonly | alloc | 195565 |
| 312 / `R_AARCH64_LD64_GOT_LO12_NC` | readonly | alloc | 195305 |
| 562 / `R_AARCH64_TLSDESC_ADR_PAGE21` | readonly | alloc | 2028 |
| 563 / `R_AARCH64_TLSDESC_LD64_LO12` | readonly | alloc | 2028 |
| 564 / `R_AARCH64_TLSDESC_ADD_LO12` | readonly | alloc | 2028 |
| 569 / `R_AARCH64_TLSDESC_CALL` | readonly | alloc | 2028 |

ARM32 GD32只读ALLOC=1193；LDO32=25仅出现在非ALLOC，LDM32不在真实全集；另有实际汇编105/106夹具。A64真实TLS只有描述符562/563/564/569各2028，不能拿此推定legacy GD/LD指令已验证。（docs/40 §12.2、§12.4、§12.10）

### 4.4 两架构各三套消费者及两种strip

三套指未strip、GNU strip副本、llvm-strip副本；每套均编译/链接分步。所有工具、C++/glibc头、系统库与运行库取对应Tizen根，LLVM头/llvm-config/opt取对应本次构建树。进程采样证明编译器、bfd/lld走/emul原生工具，目标程序经qemu-arm/qemu-aarch64。GNU ld实际driver argv拒绝LTO/plugin。完整命令与原始输出分别为 E12/consumers-{native-rerun,gnu,llvm}/ 和 aarch64-consumers-{native,gnu,llvm}/。（docs/40 §12.5、§12.11）

| 检查 | ARM32 未strip / GNU / LLVM | A64 未strip / GNU / LLVM | 门禁含义 |
|---|---|---|---|
| A-bfd | PASS / PASS / PASS | PASS / PASS / PASS | parse IR + PassBuilder O2，输出逐字节等于对应构建树opt -O2 |
| A-lld | PASS / PASS / PASS | PASS / PASS / PASS | 同上 |
| B-bfd | PASS / PASS / PASS | PASS / PASS / PASS | 进程内lld ELF入口链接，生成物exit37 |
| B-lld | PASS / PASS / PASS | PASS / PASS / PASS | 同上 |
| 共享库 | PASS / PASS / PASS | PASS / PASS / PASS | GNU ld -shared -z defs -z text，无TEXTREL；dlopen输出正确 |
| --gc-sections | PASS / PASS / PASS | PASS / PASS / PASS | GNU ld，输出仍正确 |
| 原bitcode负例 | 预期失败 / 同 / 同 | 预期失败 / 同 / 同 | 无插件GNU ld报file format not recognized |

表格依据：docs/40 §12.5、§12.11；E12/armv7l-consumer-summary.json、aarch64-consumer-summary.json。负例不是把预期失败误写为成功链接。

| TLS/strip检查 | ARM32 | A64 | 出处 |
|---|---|---|---|
| 每套共享库动态TLS | 10 DTPMOD32 + 3 DTPOFF32 | 10 R_AARCH64_TLSDESC | §12.5、§12.11；各shared-dynamic-relocations.stdout |
| 每套4个运行的call_once | A-bfd/A-lld/shared/GC均LLVM_CALL_ONCE_COUNT=6 | 同左 | 各run-*.log |
| 调用路径证据 | initializeCore→LLVM Pass注册→call_once→pthread_once包装计数 | 同左 | llvm/include/llvm/PassSupport.h:52；Support/Threading.h:26–38,86–90；§12.5 |
| GNU strip -g | 210档exit0、stderr空 | 212档exit0、stderr空 | E12/strip-gnu/result.json；aarch64-strip-gnu/result.json |
| llvm-strip -g | 210档exit0、stderr空 | 212档exit0、stderr空 | 对应strip-llvm/result.json |
| strip后门禁 | 身份/次序/完整索引不变，BC/other/thin/debug=0 | 同左 | §12.5、§12.11 |
| GNU strip后总字节 | 501071652 | 505924764 | 同上 |
| llvm-strip后总字节 | 442022188 | 463259024 | 同上 |

TLS动态重定位存在与call_once路径执行是两项证据；本次没有跟踪每条动态重定位的解析次数。ARM32第一次辅助消费者驱动遗漏 `--no-default-config` 下的resource-dir，编译缺stddef.h；按授权仅补回根内cfg已有路径，重跑一次通过，原失败保留。没有改Source/降低消费者门禁；A64无此失败重跑。（docs/40 §12.6、§12.11）

## 5. 已知限制与开放问题（请评审重点检查）

1. **允许表不等于链接器能力表。** A64许多legacy GD/LD、DTPREL片段虽获ABI/PIC策略放行，当前lld getRelExpr没有case；真实输入只覆盖TLSDESC四种。是否收窄ALLOW或增加逐类型真实链接夹具，待评审；本次不改规则。（docs/40 §12.1–12.2；§4.3）
2. **module asm批量覆盖缺口。** 实际`module_asm_checked=0`；只有带文件级汇编的小夹具验证 `$t` 正例及去-mthumb后 `$a`/覆盖警告负例。解析器不是通用汇编语法解析器；分号、多语句、宏、特殊节切换的覆盖须另审，不能由0触发推定安全。（docs/40 §12.2、§12.4；S:582–613,639–672）
3. **ARM32参考对象开销。** 每个bitcode成员额外编译一次，相当于编译调用数加倍；现有wall1800.448876s包含此成本，没有同条件关闭门禁的对照，不能宣称实测wall恰好2倍。取消该门禁会改变认证条件。（docs/40 §12.4；S:675–701）
4. **TARGET1按绝对地址处理。** 编号38属于absolute，当前580处均可写ALLOC；GNU/lld消费者通过不证明其他链接器TARGET1政策均相同。TARGET2未认证，遇到仍停。（docs/40 §12.4；S:729–734；docs/39 §4）
5. **IE/ARM32描述符仍STOP。** ARM32显式pending与A64 TLSIE在非ALLOC也停止，LE在任何节禁止。真实库未出现IE/LE；小夹具覆盖拒绝行为；本轮没有扩展其运行时适用范围。（docs/40 §12.1–12.2、§12.10；S:770–775）
6. **通用未知非ALLOC的边界。** LE/pending检查之后，Source跳过其他非ALLOC类型；因此§2.4其余STOP不保证在非ALLOC也失败。全集普查另覆盖全部节并报告未知0，但这项外部普查不是Source本身。请评审“未知类型硬失败”的要求是否需覆盖所有节。（S:776–779；docs/40 §12.4、§12.10）
7. **allow编号256无定义名。** A64 allowed含0x100，但当前LLVM AArch64.def未定义该号；本材料忠实列为UNNAMED_IN_LLVM_DEF，不补猜类型名称。它没有出现在真实全集；是否删除或补认证依据待评审。（S:739；llvm/llvm/include/llvm/BinaryFormat/ELFRelocs/AArch64.def；docs/40 §12.10）
8. **认证是固定输入，不是通用转换证明。** ARM32/A64末项优化、triple、softfp、tune、DWARF及后端开关均有限定；A64有25个成员无函数属性，ARM32有26个，不能声称所有成员均记录CPU/tune。需特别复核缺属性时driver默认值依赖；ARM32有逐成员参考，A64没有对应参考门禁。（docs/40 §11.4、§12.4、§12.9；S:485–558）
9. **符号门禁强度有限。** 强符号只要求名称保留，未比较其type/binding/visibility完全一致；允许弱符号缺失已计数。索引正确与程序A/B通过不是每一个API语义/ABI等价证明。（S:928–950；docs/40 §12.4、§12.10）
10. **测试不是全部隔离在一个文件。** 67项含生产回归与辅助校验测试；13项在ARM测试文件。TLS合成ELF逐号测试只测试解析/策略，不是逐号真实链接；Python3.9项是语法解析及摘要测试，不是完整Python3.9环境运行。（E12/unit-tests-final.log；tools/test_static_archives_source_v2.py:100；docs/40 §12.2）
11. **部署与安装未闭合。** 本轮ARM没有%install/RPM后处理集成，也未验证新patchset在OBS的完整流程。ARM32新门禁调用外部readelf，生产集成要确保根内可用及输出格式稳定；Version闸门只核验compiler major=22，未核验disassembler/nm版本一致。逐档原子替换不等于整库回滚。（S:675,964,992,1166；docs/40 §12.12）
12. **纯机器码档跳过转换。** validate_archive先拒绝thin/other，但bitcode=0即跳过process，因此Source不会为纯机器码整档执行ARM PIC/Thumb/索引重认证；本次输入全集的独立普查与消费者补证不能被误写成Source保证。（S:1037–1044；docs/40 §11.4、§12.9–12.10）

以上新增阅读观察均给出可核对的现有Source位置；未修改候选、测试、spec或已上传补丁。请外部评审分别指出必须修改项、可接受边界及需新增的实验，不把这份材料包的完成当作评审通过。

## 6. 67项测试逐项清单

既有结果：67 tests、0 failures、0 errors、13.410827s，全部ok。以下按原日志顺序列出**每个测试方法**，子用例不另计项；共9个模块，其中ARM专用13项，其余54项。证据统一为 `E12/unit-tests-final.log`、`unit-tests-final-result.json`；下表模块链接定位测试文件，方法附定义行，覆盖点来自现有断言。真实编译夹具不是这67项的另一个重复计数。（docs/40 §12.2）

**[test_static_archives_source.py](../tools/test_static_archives_source.py)**：

| 项 | 测试方法（定义行） | 覆盖点 |
|---:|---|---|
| 1 | `test_first_failure_cancels_and_reaps`:28 | 首错取消、子进程回收、禁止后续命令 |
| 2 | `test_limits_accounting_and_no_external_time`:14 | 4GiB AS/core0与wait4统计，无外部time |
| 3 | `test_wait4_is_per_child_under_four_workers`:38 | 四worker资源统计逐子进程归属 |

**[test_static_archives_source_v2.py](../tools/test_static_archives_source_v2.py)**：

| 项 | 测试方法（定义行） | 覆盖点 |
|---:|---|---|
| 4 | `test_g_failed_leader_descendants_are_killed`:211 | 失败leader的后代也终止 |
| 5 | `test_g_handler_only_records_signal`:193 | 信号处理器仅记录，不持锁取消 |
| 6 | `test_g_signal_on_success_cannot_return_pass`:228 | 成功边界收到信号仍失败 |
| 7 | `test_g_success_and_timeout_reaped`:201 | 超时TERM→KILL并回收 |
| 8 | `test_d_native_pass_thin_and_other_rejected`:112 | native通过，thin/other拒绝 |
| 9 | `test_e_evidence_reset_and_unsafe_rejected`:125 | 旧证据重置，重叠目录拒绝 |
| 10 | `test_e_native_install_skip_and_cleanup`:134 | 全native打印SKIP并PASS |
| 11 | `test_f_atomic_copy_preserves_mode`:143 | 原子替换保留权限 |
| 12 | `test_f_failed_copy_preserves_original_and_records_failure`:152 | 复制失败保留原件并记失败 |
| 13 | `test_h_tools_version_and_cache`:166 | 工具可执行、major22、Cache门禁 |
| 14 | `test_l_cleanup_keeps_json_only`:182 | 清理大文件，仅留JSON |
| 15 | `test_a_classifies_operands_without_replaying_lto`:32 | 逐token及成对操作数分类，不重放LTO |
| 16 | `test_a_unknown_and_missing_operands_fail`:39 | 未知token/缺操作数失败 |
| 17 | `test_b_last_values_and_defaults`:46 | 优化/DWARF/FP末项生效及默认值 |
| 18 | `test_b_uncertified_last_values_fail`:58 | 不认证末项与禁用后端开关失败 |
| 19 | `test_c_four_type_features_fail`:68 | 四种type/vcall/SplitLTO特性拒绝 |
| 20 | `test_c_normal_ir_and_zero_split_lto_pass`:64 | 普通IR/字符串/零SplitLTO通过 |
| 21 | `test_i_missing_strong_fails_check`:83 | 真实缺强符号时check失败 |
| 22 | `test_i_strong_preserved_weak_missing_recorded`:76 | 强符号保留，缺W/V计数 |
| 23 | `test_j_triple_mismatch`:94 | 错误triple/未认证架构失败 |
| 24 | `test_k_python39_and_chunk_digest`:100 | Python3.9语法、分块SHA、单shebang |

**[test_convert_static_archives.py](../tools/test_convert_static_archives.py)**：

| 项 | 测试方法（定义行） | 覆盖点 |
|---:|---|---|
| 25 | `test_absolute_allocated_relocation_rejected_but_debug_excluded`:71 | x86只读ALLOC绝对地址拒绝，debug排除 |
| 26 | `test_gnu_packing_keeps_duplicate_names_and_order`:85 | GNU确定性打包保留同名/顺序 |
| 27 | `test_native_machine_and_wrong_machine`:64 | x86 Machine核验及错误架构拒绝 |
| 28 | `test_pic_is_explicit_and_no_lto`:19 | 显式PIC、O3，无LTO/宿主CPU覆盖 |
| 29 | `test_pie_and_static_distinguished`:28 | PIE与非PIC区别 |
| 30 | `test_recorded_backend_options_are_required_and_last_flag_wins`:45 | 非法PIC/PIE/Code Model拒绝 |
| 31 | `test_unsupported_flags_fail`:34 | 错误target拒绝 |
| 32 | `test_wrong_target_fails`:41 | 原命令必需，后端末项门禁 |

**[test_inspect_llvm_archives.py](../tools/test_inspect_llvm_archives.py)**：

| 项 | 测试方法（定义行） | 覆盖点 |
|---:|---|---|
| 33 | `test_64bit_index`:73 | 64位ar索引读取 |
| 34 | `test_actual_member_magic`:44 | 按真实魔数分机器码/BC/other |
| 35 | `test_corrupt_input_rejected`:87 | 损坏/截断归档拒绝 |
| 36 | `test_duplicate_member_names_are_not_collapsed`:59 | 同名成员不折叠，索引需指对成员 |
| 37 | `test_gnu_long_name`:77 | GNU长名称解析 |
| 38 | `test_mixed_archive_partial_index`:54 | 混合档索引只含机器码的识别 |
| 39 | `test_native_index_and_debug_sections`:49 | 机器码索引及debug节检测 |
| 40 | `test_order_and_not_just_count`:67 | 映射/次序不能只比较条数 |
| 41 | `test_thin_never_reads_external_members`:82 | thin不读取外部成员 |
| 42 | `test_runtime_native_pass_and_bitcode_stop`:92 | 历史运行库普查native/BC策略分支 |

**[test_native_archive_commands.py](../tools/test_native_archive_commands.py)**：

| 项 | 测试方法（定义行） | 覆盖点 |
|---:|---|---|
| 43 | `test_actual_limits_and_monitor_cleanup`:18 | 实际AS差异及监视器回收 |
| 44 | `test_compile_limit_does_not_leak_to_link`:11 | 编译AS上限不泄漏到链接 |
| 45 | `test_failure_stops_following_commands`:32 | 失败停止后续命令并回收 |

**[test_simulate_native_archive_strip.py](../tools/test_simulate_native_archive_strip.py)**：

| 项 | 测试方法（定义行） | 覆盖点 |
|---:|---|---|
| 46 | `test_corruption_rejected`:15 | strip后顺序/符号/debug/格式破坏拒绝 |
| 47 | `test_full_mapping_and_duplicate_members_pass`:12 | 完整映射与重名成员通过 |

**[test_verify_native_archive_consumers.py](../tools/test_verify_native_archive_consumers.py)**：

| 项 | 测试方法（定义行） | 覆盖点 |
|---:|---|---|
| 48 | `test_all_lto_plugin_forms_rejected`:15 | LTO/plugin/cc1as各形式拒绝 |
| 49 | `test_loader_cc1_regression_rejected`:11 | 显式loader错误cc1入口拒绝 |
| 50 | `test_object_only_bfd_and_lld`:7 | 仅对象输入的bfd/lld通过 |

**[test_compare_native_conversion_options.py](../tools/test_compare_native_conversion_options.py)**：

| 项 | 测试方法（定义行） | 覆盖点 |
|---:|---|---|
| 51 | `test_backend_flags_include_sections_and_exclude_lto`:39 | 补回分段，不带LTO |
| 52 | `test_duplicate_sections_are_counted`:34 | 重复节按重数统计 |
| 53 | `test_equal_counts_do_not_hide_wrong_sections_or_visibility`:29 | 同条数不掩盖节名/可见性差异 |
| 54 | `test_sections_symbols_visibility_and_relocations`:11 | 节、符号可见性、重定位提取 |

**[test_arm_archive_trial.py](../tools/test_arm_archive_trial.py)**：

| 项 | 测试方法（定义行） | 覆盖点 |
|---:|---|---|
| 55 | `test_arm_exact_options_and_cross_target_rejection`:45 | 两ARM精确选项及跨目标/未知项拒绝 |
| 56 | `test_arm_ir_and_explicit_abi`:53 | ARM IR/PIC/显式ABI及type-test拒绝 |
| 57 | `test_arm_pic_rel_and_aarch64_rela`:63 | ARM REL/A64 RELA、ABS例外/安全类型 |
| 58 | `test_narrow_absolute_writable_rejected`:71 | 窄绝对重定位在可写节仍拒绝 |
| 59 | `test_original_functions_are_identical`:30 | 原函数/类AST一致（排除两入口） |
| 60 | `test_x86_never_reaches_arm`:37 | x86不进入ARM策略，未知架构拒绝 |
| 61 | `test_initial_exec_arm_descriptors_and_unknown_stop`:90 | IE/ARM描述符/未知类型停止 |
| 62 | `test_local_exec_forbidden_even_debug_writable_and_absolute`:83 | LE在debug/可写/SHN_ABS均拒绝 |
| 63 | `test_module_asm_section_tracking`:118 | module asm节跟踪、空输入、失衡拒绝 |
| 64 | `test_override_warning_is_a_failure`:112 | 两种triple覆盖警告均失败 |
| 65 | `test_thumb_gate_rejects_attribute_mismatch`:125 | mock参考对象属性不一致拒绝 |
| 66 | `test_thumb_restore_and_reference_arguments`:100 | Thumb补回，原flags参考去LTO/旧路径 |
| 67 | `test_tls_allowed_each_type_readonly_and_writable`:76 | 每个TLS ALLOW号的只读/可写正例 |

执行对象辨析：历史驱动 `E12/run_tests_final.py` 将生产Source模块别名指向候选，再加载上述模块；并不代表所有辅助模块的旧规则都是新Source的生产规则。例如运行库普查测试保留早期范围门禁，不限制本次候选对含bitcode的libarcher转换。（E12/run_tests_final.py；test_inspect_llvm_archives.py:92；docs/40 §12.9）

67项之外的真实夹具：两架构GD/LD小C、IE/LE拒绝例；ARM32另用真实汇编覆盖105/106；A64小C实际生成562/563/564/569；无函数属性的Thumb module asm正例及去-mthumb负例。结果均来自 `E12/real-fixtures-final/summary.json`、`local-dynamic-fixture/result.json`，本次未重跑。（docs/40 §12.2）

本材料不改变历史PASS/FAIL，不新增实验结果，不改代码/spec/补丁，不构建或转换，不推Gerrit；只补齐外部评审可读的上下文与边界。
