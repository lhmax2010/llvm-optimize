# 28 静态库 bitcode 转机器码 v2：后端选项补齐，消费者 B 的 lld 链接 OOM 后停止

日期：2026-09-24（+08:00）。起点提交 `ae6d93831351307f30b240a376d7eb1ac480588e`。
docs/25–27 保留不动。本报告和 STATUS 在同一个提交更新。

**本轮重新转换的 225 个归档、3,853 个 bitcode 成员全部通过格式、成员顺序、完整索引与 PIC 静态检查。**
程序 A 用 GNU ld 和 lld 链接、运行均成功，PassBuilder O2 输出与基线 opt 完全一致；
程序 B 的 GNU ld 组成功，进程内 lld 链出的小程序退出码为 37，符合预期。
但 **程序 B 的 lld 组在 4 GiB 地址空间限制下报分配失败**，触发用户的“任一项失败即停”。
共享库、GC、原归档反例及全部第二段验收 **NOT RUN**；没有改限额、减依赖或重试。
**未修改 spec、未增加认证入口、LLVM 完整构建 0 次、Tizen 消费者测试包构建 0 次。归档修法尚不能提交发货。**

## 0. 范围、独占与基线身份

用户确认旧命令遗漏后端分段参数，故 docs/27 的转换结果本轮作废、不复用。
方向仍是仅在打包安装阶段把 bitcode 变为机器码，保留原 RPM 宏和通用归档 strip；
libarcher_static.a 包含在内，compiler-rt 45 个纯机器码归档保持原行为。工具本身的构建与链接不改。
本轮只完成下面记为 PASS 的离线步骤，没有把后续计划写成已完成。

| 别名 | 实际路径 |
| --- | --- |
| W | `/home/linhao/Toolchain/development/llvm-optimize` |
| E | `W/temp/static-native-conversion-v2-20260924`，本轮独立证据目录 |
| H | `W/temp/archive-index-fix-rpm-20260923/baseline-rpm-extract`，唯一 RPM 内容基线 |
| R0 | `W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0` |
| Rnew | `W/temp/gbs-root-x86_64-archivefix`，只有本任务独占锁，未初始化 GBS |
| S | `W/temp/llvm-archivefix-trial`，隔离源码工作树 |
| C | `E/conversion`；新归档为 `C/archives/usr/lib64/*.a` |
| RT | `W/temp/toolchain-runtime-baseline/libxml2/usr/lib64` |
| L | `/lib64/ld-linux-x86-64.so.2`，宿主显式 loader |

`E/precheck.json`：主仓库 status 空；没有其他 rpmbuild/gbs/ninja/lld/ld.lld/llvm-bolt 进程。
S 的 HEAD=`f111162e94aa48ed367c9d2c039456c70e7160ae`，分支 `archive-fix-trial`；
spec SHA256=`95887b2d060b38d5ef8f56936f7481a03d131f9d26432180a68e02ec95f0dda5`。
完整 diff 仅原先三处并发修改：mlgo_build_jobs 6→4、compile 6→4、link 2→1。

锁采用 O_EXCL；session=`archivefix-rpm-eac7f8f5abba40a6a6c92af1c16d248c`、PID=1703487，
取得时间 `2026-09-24T14:10:24.638067+08:00`。核查、实验及报告期间持有，收尾删除。
证据：`E/hold_lock.py`、`lock-acquired.json`、`lock-released.json`、`final-cleanup.json`。

重新读取 R0 指定 RPMS 目录中的 22 个 RPM：**22/22 SHA 匹配** docs/26 记录。
随后按逐包 file-metadata.tsv/`baseline-file-owners.json` 核对 H 的文件类型、模式、SHA、软链接目标：
**17,689 个唯一包内路径，差异 0**，因此复用 H，没有重新解包。
证据：`E/check_baseline.py`、`rpm-identity.json`、`baseline-content-check.json`、`baseline-check.log`。
旧全静态 BUILD 与隔离的混合根均不作为输入；没有修改 W/llvm、其 spec 或 S/spec。

## 1. 原编译选项分类与补齐

### 1.1 输入来源与覆盖范围

- `tools/bench_inputs/real_tu/*.flags.json`：10 个 TU 的原 x86_64 `original_command` 和 ARM `flags`。
  代表文件为 `llvm_mc_AsmParser.flags.json`；其 `.ii` SHA256 为
  `8738c245d51bfc7e94c0de216d027b2d0d8ddbd77f0147bf76ac52665d0f9b55`。
- `temp/baseline-resume-20260917/real-tu/compdb.json`：docs/13 保存的 Ninja compdb 原始命令，511 条闭包记录，
  包含非编译动作。本轮提取其中 313 条 clang `-c` 命令（含汇编）到 `E/original-compile-commands.json`；
  不从旧 BUILD 重新生成 compdb。全部开关频次在 `E/all-original-options.json`。
- 本轮 llvm-dis 还从 **全部 3,853 个 bitcode** 的 `llvm.commandline` 读回原命令，
  原文保存在每成员 `ir-settings.json` 和 `C/summary.json`。
  `E/all-bitcode-original-options.json` 证明这些成员均有 -O3、-gdwarf-4、-ffunction-sections、-fdata-sections。
  同时发现一个 `-ftrapping-math` 特例，见下表；没有据代表 TU 假定所有命令完全一致。

`E/option-classification.json` 逐 token 登记代表 argv 与出处；源码关键行抄录在 `E/source-evidence.txt`。
下表路径均相对 W，源码版本为上述 f111162e；“写入 IR”不意味着全部驱动默认值也会自动恢复。

| 原开关（同类列全） | 分类与转换处理 | 源码依据 |
| --- | --- | --- |
| `-ffunction-sections`、`-fdata-sections` | 后端 CodeGenOptions→TargetOptions；**必须显式补回** | `llvm/clang/include/clang/Options/Options.td:4594–4613`；`llvm/clang/lib/CodeGen/BackendUtil.cpp:453–454` |
| `-O3`（重复，末项生效） | 优化流水线和机器码生成等级；转换保留 O3 | `llvm/clang/lib/CodeGen/BackendUtil.cpp:618–631,1131–1140` |
| `-flto=thin`（重复） | 选择 ThinLTO pre-link 流水线/bitcode 输出；**转换 argv 一律不传** | 同文件 `1135–1140` |
| `-fPIC` | PIC Level 写入 IR；目标机器仍使用命令行 relocation model，因此按模块值显式传入 | `llvm/clang/lib/CodeGen/CodeGenModule.cpp:1469–1474`；`BackendUtil.cpp:618–631` |
| `-m64`、`-march=nehalem`、`-msse4.2` | triple/data layout、函数 target-cpu/features 保存在 IR；按 IR target 转换，不用宿主 CPU 覆盖 | `llvm/clang/lib/CodeGen/CodeGenModule.cpp:2929–2992`；`llvm/llvm/lib/Target/X86/X86TargetMachine.cpp:216–231` |
| `-mfpmath=sse` | X86 前端校验 SSE 特性；源码明确 LLVM 无独立 fpmath 开关，IR 的 CPU/features 继续使用 | `llvm/clang/lib/Basic/Targets/X86.cpp:492–497` |
| `-mavx512vl` | 保存的 compdb 中用于一个 BLAKE3 `.S`；对应已有机器码不重新生成 | `E/original-compile-commands.json`；本轮 11 原机器码 SHA 对照 |
| `-fomit-frame-pointer` | IR 模块/函数 frame-pointer 属性，none 是默认；保留 IR | `llvm/clang/lib/CodeGen/CGCall.cpp:1989–2000`；`CodeGenModule.cpp:1507–1522` |
| `-fasynchronous-unwind-tables`、`-funwind-tables` | IR uwtable 模块/函数属性；两开关同时存在时 async 为 2，保留 IR | `llvm/clang/lib/Driver/ToolChains/Clang.cpp:6000–6017`；`CodeGenModule.cpp:1504–1505,2716–2717` |
| `-fexceptions`、`-fno-exceptions` | 前端 EH 结构/调用及属性写入 IR；末项决定源语言异常开关，不能用统一 no-exceptions 覆盖 libarcher 等原命令 | `llvm/clang/lib/CodeGen/CGException.cpp:477–478`；后端异常模型入口 `BackendUtil.cpp:417–424` |
| `-fno-semantic-interposition` | IR 语义插入标志、链接属性和 dso-local 处理，保留 IR | `llvm/clang/lib/CodeGen/CodeGenModule.cpp:1113–1115,1834–1893` |
| `-fvisibility-inlines-hidden`、`-fvisibility=hidden` | 前端决定 IR GlobalValue 可见性，保留 IR | 同文件 `1782–1831` |
| `-fno-common` | 决定 IR common/external linkage，保留 IR | 同文件 `6230–6235,6356–6362` |
| `-g2`、`-g`、`-gdwarf-4` | DI 元数据/Dwarf Version 在 IR；后端 debug/MC 设置也存在，显式保留 `-g -gdwarf-4`，其中 O3+debug 还会启用 EmitCallSiteInfo | `CodeGenModule.cpp:472–482,1105–1111`；`llvm/clang/lib/Frontend/CompilerInvocation.cpp:1894–1902`；`BackendUtil.cpp:459–520` |
| `-frecord-gcc-switches`（记录中规范化为 `-frecord-command-line`） | 原命令写入 `llvm.commandline`；保留这份元数据，不用转换命令覆盖。记录中仍有原 ThinLTO 字样不等于转换实际带 LTO | `llvm/clang/lib/CodeGen/CodeGenModule.cpp:8036–8043` |
| `-ftrapping-math`（仅 ConstantFolding.cpp.o） | 转为 strict FP exception behavior、constrained FP IR/strictfp；实际 IR 属性含 strictfp，保留而非丢弃 | `llvm/clang/lib/Driver/ToolChains/Clang.cpp:2774,2981–2991,3240–3242`；`llvm/clang/lib/CodeGen/CodeGenFunction.cpp:1085–1095`；`E/trapping-math-record.json` |
| `-std=c++17` | 前端解析/语言语义已体现在 IR；IR 再编译不传 C++ 标准选项 | `llvm/clang/lib/Frontend/CompilerInvocation.cpp:3994–4010` |
| 所有 `-D…`、`-I…`、`-Wp,-D_FORTIFY_SOURCE=2` | 预处理/头文件搜索；结果已进入 IR，不重新预处理归档成员 | 同文件 `3438–3462,4816–4865` |
| 所有 `-W…`（上一行 Wp 除外）、`-pedantic`、`-fmessage-length=0`、`-fdiagnostics-color[=never]`、`-fcolor-diagnostics` | 诊断控制；不属于机器码选项，转换不重放 | 同文件 `2610–2750`；完整枚举见 `E/all-original-options.json` |
| `-pipe` | 驱动显式忽略；不重放 | `llvm/clang/lib/Driver/Driver.cpp:1541–1542` |
| `-MD`、`-MT`、`-MF` 及参数，`-c`、`-o`、源/目标路径 | 依赖输出/动作/文件路径；转换重建单输入 -c 与独立 -o，不沿用旧目录 | `llvm/clang/lib/Frontend/CompilerInvocation.cpp:2310–2385`；每成员实际 argv |

### 1.2 显式固定的后端默认值

另外固定 `-funique-section-names`、`-faddrsig`、`-ffp-contract=on`：

- unique section names 的默认值为 true：`llvm/clang/include/clang/Options/Options.td:4658–4663`，进入 TargetOptions 的位置为 `BackendUtil.cpp:456`。
- 当前 ELF+integrated assembler 驱动默认添加 addrsig：`llvm/clang/lib/Driver/ToolChains/Clang.cpp:7992–7999`；后端读取位置 `BackendUtil.cpp:466`。
- 非 CUDA/HIP 的驱动默认 FPContract=on：同一 Clang.cpp `2789–2797`；后端 AllowFPOpFusion 的读取为 `BackendUtil.cpp:393–405`。

实际驱动展开保存在 `E/options/*-driver.txt`。本轮转换器的 `BACKEND_FLAGS` 与对照脚本共享同一份定义；
PIC/PIE 来自 IR，不把它写死为适用于所有归档的假设。原命令缺失、最后优化级别非 O3、
分段未启用、DWARF 设置不符、非 x86_64 或不支持的 code model 均拒绝处理。
这仍是**针对本基线输入的验证工具，不是任意 LLVM 配方的通用选项推断器**。

## 2. 真实 TU 两路对照：PASS（差异逐项解释）

选择训练集中的 `llvm/lib/MC/MCParser/AsmParser.cpp`，使用已有 `.ii` 和 sidecar；
没有换 TU、重采输入或把 ARM `.ii` 改标 x86_64。target=`armv7l-tizen-linux-gnueabi`，sysroot=
`/home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0`；resource-dir=`H/usr/lib64/clang/22`。

甲使用 sidecar flags 直接 `-x c++-cpp-output -c`；乙使用同样 flags，恢复原 x86_64 argv 已记录、
基准 sidecar 按规则移除的 `-flto=thin`，生成 ARM bitcode，再用 §1.2 后端选项和 `-fPIC -x ir -c` 生成 ARM .o。
两路编译器都是 `L --library-path RT H/usr/bin/clang-22 --no-default-config --driver-mode=g++`。
完整三条 argv 与输入 SHA：`E/options/plan.json`；原始 readelf：`*-sections.txt`、`*-symbols.txt`、`*-relocations.txt`。

| 检查 | 甲：直接 native | 乙：ThinLTO IR→native | 判定 |
| --- | ---: | ---: | --- |
| 非 NULL 节区数 | 917 | 917 | 全部节区名及重数相同 |
| `.text.*` 函数节区数 | 205 | 205 | 相同 |
| 定义符号集合＋type/binding/visibility | 相同 | 相同 | PASS，未忽略全局/弱符号差异 |
| 定义符号条目数（含重复 ARM mapping symbols） | 1032 | 1030 | 差两个 LOCAL DEFAULT 映射标记，不是定义符号集合差异 |

重定位类型分布完整记录：

| 类型 | 甲 | 乙 | 解释 |
| --- | ---: | ---: | --- |
| R_ARM_NONE | 205 | 205 | 相同 |
| R_ARM_PREL31 | 211 | 211 | 相同 |
| R_ARM_CALL | 2194 | 2195 | 下述五个函数内调用点变化，净 +1 |
| R_ARM_JUMP24 | 12 | 12 | 相同 |
| R_ARM_REL32 | 599 | 598 | parseMacroLikeBody 少一个 `.L.str.65` 地址引用 |
| R_ARM_GOT_PREL | 37 | 38 | parseEscapedString 对同一个 hexDigitValue LUT 多一个常量池引用 |
| R_ARM_ABS32 | 64415 | 64603 | 增加 188 条全部在调试节：debug_info +77、debug_loc +81、debug_ranges +30 |

`E/options/relocation-difference-by-section.json` 逐节、逐目标符号列出差异，
`affected-function-disassembly.diff` 是本次两个 .o 的实际反汇编差异，没有为解释差异重新编译：

- expandMacro 多一个 raw_ostream `operator<<` 调用；其 lambda 少一个 raw_ostream::write 调用。
- parseMacroArguments 多 Error、vector::_M_realloc_append 各一个调用。
- parseMacroLikeBody 少一个 bcmp 调用及 `.L.str.65` 引用；反汇编可见使用立即数的比较，调用序列/常量池布局改变。
- parseEscapedString 的同一 LUT 从一个 GOT 常量池项变为两个；定义仍为 WEAK DEFAULT，没有变更符号可见性。
- parseStatement 少一个 `$a` 与 `$d` 重复标记。它们表示代码/数据连续区间边界，
  不是用户函数；该函数仍有四个 `.word`，区域排列改变。源码 `llvm/llvm/lib/Target/ARM/MCTargetDesc/ARMELFStreamer.cpp:465–469,656–687`；
  原始定位见 `*-mapping.json`、`mapping-symbol-analysis.json`。

原因边界：甲为一次 per-module O3；乙先 ThinLTO pre-link 再 per-module O3，
`llvm/clang/lib/CodeGen/BackendUtil.cpp:1135–1140` 明确区分这两条流水线。
因此指令、调用数量和对应调试重定位不要求字节相同；本次节区结构、定义符号集合及可见性符合用户判据。
初始机器记录为 `REVIEW_REQUIRED`，逐项解释后的明确放行记录为 `E/options/review.json`。
**这不是整个库语义等价的证明，后续消费者仍必须全部通过。**

## 3. 重新转换：225/225 PASS

### 3.1 本轮实际命令与资源限制

每个 bitcode 成员使用：

```bash
/usr/bin/time -f '%e %U %S %M %x' -o <成员>/convert.time \
  prlimit --as=4294967296 --core=0 -- \
  /lib64/ld-linux-x86-64.so.2 --library-path <RT> \
  <H>/usr/bin/clang-22 --no-default-config \
  --target=x86_64-tizen-linux-gnu -x ir \
  -O3 -ffunction-sections -fdata-sections -funique-section-names \
  -faddrsig -g -gdwarf-4 -ffp-contract=on -c -fPIC \
  <成员>/input.bc -o <成员>/<原成员名>
```

本批实际 PIC Level=2/PIE Level=0，故均为 -fPIC。IR 保留原 CPU/features、可见性、异常及原命令元数据。
转换器为 H 中 clang 22.1.8，SHA256=`3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c`。
libxml2 独立运行库 SHA=`0d70127304264bd46387484ed7e566fc5fec96fb9c77de8c06fe0a9e9a0a8034`，来源仍为 docs/13 固定快照。
没有安装宿主软件或修改二进制。

按 archive/ordinal 分目录提取，保留同名成员，不覆盖；原机器码复制后核 SHA。
按原顺序执行 `/usr/bin/ar qcDS <新.a> <逐成员路径...>`，随后 `/usr/bin/ar sD <新.a>`。
转换后检查通过才删除该归档临时成员；新归档、逐成员命令/time/IR 设置/检查结果全部保留。

执行入口为 [run_static_archive_conversion.py](../tools/run_static_archive_conversion.py)；
实际转换器为 [convert_static_archives.py](../tools/convert_static_archives.py)。
整体 13 GiB cap=`min(18, floor(MemAvailable/GiB)-4)`，启动可用内存 18,303,188,992 B；
MemorySwapMax=0、nice 15、ionice c3、4 workers、每工具 4 GiB AS，低于 2 GiB available 自动终止。
沿用 30 秒资源采样、2 秒进程 VmHWM 采样及退出回收；没有改完整构建 18 GiB 准入规则。

| 指标 | 实测 |
| --- | --- |
| 归档 / 转换 bitcode / 保留原机器码 | 225 / 3853 / 11 |
| 成员数、次序、名字和同名 ordinal/occurrence | 全部一致 |
| 输出格式 | 全部 x86_64 ELF64 little-endian ET_REL，bitcode=0、other=0 |
| 索引 | 318,543 条；逐归档恰为成员已定义外部符号多重集合，不以“非空”代替完整性 |
| PIC 静态扫描 | 无禁止项，原 11 机器码也无禁止项 |
| 转换前 / 后归档总字节 | 5,449,996,190 / 6,615,084,040 |
| 带调试节的成员 | 3,849；尚未进入打包 strip |
| 转换 wall / 外层 scope wall | 782.346390 / 783.586232 秒 |
| 单成员最大 RSS | 1,047,288 KiB = 0.998772 GiB；Registry.cpp.o，libclangDynamicASTMatchers.a ordinal 3，wall 15.70 s |
| cgroup MemoryPeak / MemoryMax | 6,640,709,632 B（6.184643 GiB）/ 13 GiB |
| 宿主最低 MemAvailable | 15.895012 GiB（采样值） |
| OOM / oom_kill / max 事件 | 均 0 |
| sampler / log reader / scope | 已回收、已回收、inactive/dead |

证据：`E/conversion-summary.json`、`C/summary.json`、`C/members/`、`E/conversion-scope/`。
PIC 检查方法沿用 `inspect_llvm_archives.py`/`convert_static_archives.py`：
只检查 SHF_ALLOC 目标节的重定位，拒绝非 SHN_ABS 的 R_X86_64_32/32S，以及只读 allocated 节中的 R_X86_64_64；
不把合法 PC-relative 或调试节重定位一律拒绝。**完整 `.so -z defs -z text` PIC 验证因消费者先失败未执行。**
compiler-rt 45 个本轮扫描后不转换，H 保持只读；不能将这写成“新 RPM 的 compiler-rt 验收通过”。

### 3.2 每函数一段抽查

从已完成归档列表固定位置 0/25/50/75/100/125/150/175/200/224 各取第一个原 bitcode 成员。
10/10 输出中所有定义 FUNC 都位于 `.text.*` 节；不抽原生汇编成员，也不重复选择失败样本。
成员 SHA、每个函数对应节区和原始 readelf 输出：`E/function-section-check/results.json` 及同目录文件。
抽查清单见附录 B；全量成员顺序/索引结果见附录 A。

## 4. 消费者：三项 PASS，第四项 OOM 后停止

### 4.1 环境和入口

[verify_native_archive_consumers.py](../tools/verify_native_archive_consumers.py) 将编译与链接分开：
每个 C++ 源先单独 `clang-22 ... -c source.cpp -o source.o`；链接调用只输入既有 `.o`。
每次链接保存 `-###` 并拒绝 cc1/cc1as、-flto、-plugin/--plugin。已执行两组 GNU ld 的展开均无 LTO/插件。
所有完整 argv、wall/user/sys/max RSS、退出码在 `E/consumers/{compile,link,run}-*.json` 和 `.log/.time`。

| 组成 | 实际来源/处理 |
| --- | --- |
| C++ 编译器 | 基线 RPM 的 H/usr/bin/clang-22，经 L 和 RT 执行；单独 -c 避免显式 loader 多 job 的 cc1 路径问题 |
| 消费者目标 | 显式 `--target=x86_64-linux-gnu --no-default-config`；这是宿主 ABI 离线验证，不冒充 Tizen 包内验证 |
| LLVM/lld 头文件 | H/usr/include，经临时 prefix/include 软链接引用 |
| C++ 标准库头 | **宿主 GCC 13**：`/usr/include/c++/13`、`/usr/include/x86_64-linux-gnu/c++/13`、backward；见 compile-a.log/compile-b.log |
| libc 头文件、crt、libgcc | **宿主** `/usr/include{,/x86_64-linux-gnu}`、`/lib/x86_64-linux-gnu/{Scrt1,crti,crtn}.o`、`/usr/lib/gcc/x86_64-linux-gnu/13/` |
| clang 资源头 | H/usr/lib64/clang/22/include |
| LLVM/lld 静态库 | **仅本轮 C/archives/usr/lib64**；llvm-config --link-static 给出参数，A 使用 asmparser/passes/core/support，B 用 lldELF/lldCommon + all 依赖组 |
| GNU linker | 宿主 `/usr/bin/ld.bfd`，clang --ld-path 直接选择，不通过会自动加插件的 g++/collect2 |
| lld linker | 基线 H/usr/bin/lld，经独立 wrapper 执行 `L --library-path RT lld -flavor gnu`；无宿主安装 |
| libstdc++、glibc、libm、libgcc_s、zlib | **宿主** `/lib/x86_64-linux-gnu/`；链接与实际 loader --list 均有记录 |
| libxml2 | **Tizen 固定快照** libxml2.so.16，链接指定 RT 中绝对路径，运行指定 --library-path；不用宿主不同 ABI 的 libxml2 |

llvm-config 通过放在新 prefix/bin 的同字节 loader 副本查询，解决 `/proc/self/exe` 导致的 prefix 误判；
prefix/lib64 指向 C 新归档，不指向 docs/27 旧产物。证据：`query-*.txt/json`、`a-*-driver.txt`、
`a-*-runtime.txt`、`host-runtime-identities.json`。A 两个成品 NEEDED 均无 libLLVM/libclang。

### 4.2 程序与实测结果

A 从固定 input.ll 解析 IR，verifyModule，然后注册 PassBuilder analyses/proxies，运行默认 O2 module pipeline，
再次 verify 并打印完整结果。输入没有目标 triple，因此与 opt 同样不创建 TargetMachine；
依据 `llvm/llvm/tools/opt/optdriver.cpp:636–643`。基线参考执行 `H/usr/bin/opt -S -O2 input.ll -o expected.ll`。
两次 A 输出与 expected.ll **完整文本一致（包含 ModuleID）**；核心结果为 `%b = shl i32 %x, 1`。

B 使用 lldCommon/lldELF 的 `lld::lldMain`，注册 `lld::elf::link`，在进程内执行：
`ld.lld -m elf_x86_64 -e _start minimal.o -o generated`。
minimal.o 由宿主 `as --64` 预编译，程序直接执行 exit(37) 系统调用；生成文件实际运行核对退出码。
完整源码在脚本常量及 `E/consumers/{a,b,shared-main}.cpp`、`minimal.s`、`input.ll`。

| 项目 | 结果 | 实测/证据 |
| --- | --- | --- |
| A 编译 | PASS | 3.29 s，337,000 KiB RSS；compile-a.json |
| A GNU ld 链接 + 运行 | **PASS** | 链接 26.54 s / 966,800 KiB；完整 IR 与 opt 一致；link-a-bfd.json、run-a-bfd.txt |
| A lld 链接 + 运行 | **PASS** | 链接 1.10 s / 2,531,748 KiB；完整 IR 与 opt 一致；link-a-lld.json、run-a-lld.txt |
| B 编译 | PASS | 0.23 s，115,652 KiB；compile-b.json |
| B GNU ld 链接 + 库内链接 + 生成物运行 | **PASS** | 外层链接 44.50 s / 1,381,568 KiB；输出 lld-in-process-link-ok；生成物 exit=37，b-bfd-generated-run.json |
| B lld 链接 | **FAIL** | 21.06 s，驱动 exit=1，lld aborted；link-b-lld.log/json/time |
| B lld 组成品运行 | NOT RUN | 未生成可用成品 |
| A 共享库 `-shared -z defs -z text` + dlopen 主程序 | NOT RUN | 上一步失败即停 |
| A GNU ld `--gc-sections` 与大小对照 | NOT RUN | 同上 |
| 原 bitcode 归档 GNU ld 无插件反例 | NOT RUN | 同上，未用旧报告结果代替本次执行 |

A 成品大小分别 664,194,552 / 664,829,616 B；B-bfd 为 961,119,776 B，均含尚未 strip 的调试信息。
这不是打包后大小，也不是性能比较。完整 SHA 在 `E/consumers/product-identities.json`；B 生成的最小成品为 1,000 B。

### 4.3 停止原因与内存证据

原始错误（`E/consumers/link-b-lld.log`）：

```text
LLVM ERROR: out of memory
Allocation failed
...
LLVM ERROR: out of memory
Allocation failed
clang-22: error: unable to execute command: Aborted (core dumped)
clang-22: error: linker command failed due to signal (use -v to see invocation)
```

| 项目 | 实测 |
| --- | --- |
| 实际继承 RLIMIT_AS | 4,294,967,296 B；bounded_argv 中 prlimit --as=4294967296；core=0 |
| B-lld 外层 time 最大 RSS | 1,324,500 KiB；包括被启动的链接子进程统计，不是地址空间峰值 |
| 2 秒采样的 lld VmHWM | 1,327,612 KiB；最后采到 Threads=17。没有传 --threads，使用 lld 默认线程策略 |
| 消费者阶段 wall | 101.273472 s，终止状态 1 |
| 消费者 MemoryPeak / MemoryMax | 5,351,313,408 B（4.983799 GiB）/ 12 GiB |
| memory.events | low/high/max/oom/oom_kill/oom_group_kill 均 0 |
| 宿主最低 MemAvailable | 17,003,466,752 B = 15.835712 GiB，4 次 30 秒采样的最小值 |
| scope/采样器/reader | 已 inactive/dead，采样器与日志 reader 已回收 |

本次**不是 cgroup OOM kill，也没有证据表明宿主物理内存耗尽**。
B 链接选取 121 个归档，总 2,862,013,208 B；A 为 52 个、1,899,252,244 B。
它们是含调试信息的完整库集合；这些大小不能直接当作 RSS。
现象与 4 GiB 地址空间压力一致，但本轮未采 VmSize/分配调用，
**不能精确断言是哪个 mmap、heap 分配或线程栈请求失败，也不能据此给自然物理内存峰值。**
证据：`link-b-library-sizes.json`、`consumer-scope/process-memory.jsonl`、`samples.jsonl`、`memory-summary.json`。

失败后没有调 AS/cgroup cap、线程数、依赖集合或 strip 状态重跑，没有继续其他消费者。
通用监控器日志中的 “build/chroot command” 是复用入口的标签；实际命令只有离线 Python 工具，未执行 GBS。
systemd scope 的清理状态 Result=success 不覆盖子命令 exit=1，结果以 outcome.json 的 command_exit_code 为准。

## 5. 其他架构：只读结论与边界

工作区 `llvm/packaging/llvm.spec:205–206` 不分架构地追加 -flto=thin；226–228 将它们送入 CMake C/ C++/ASM flags。
`%{defined _toolchain}` 条件在 229–236：宏定义时还启用 LLVM_ENABLE_LTO=Thin、lld、llvm-ar/ranlib；
宏未定义时，这个条件块不展开，但 205–206 的全局 ThinLTO flags 并未因此消失。
armv7l 分支为 MinSizeRel（243–247），aarch64 为 Release（248–252）。
因此**工作区配方的这两个 clang 构建分支同样启用 ThinLTO，成功生成的 bitcode 静态库要满足 GNU ld 无插件要求，也需要转换**。
这是当前 spec 的静态推导，不是旧公开快照 static-devel 的实测形态。

沿用 docs/27 §5 已登记调查：两个 GBS 根中的 accel 是 x86_64 clang 22.1.8，具备 ARM/AArch64 目标，
但根内和对应缓存没有 static-devel 可读样本，实际未来 IR 可读性仍 UNKNOWN。
在 x86_64 worker 上，建议先核实系统 clang→accel 路由并用实际 IR 验证，再选择经 accel 执行的系统转换器；
不能假定构建树的新 ARM ELF 可原生直接执行。
ARM MinSizeRel 的最后有效优化等级、PIC/ABI/后端 flags 必须按其实际 argv 重新确定，不能复制本轮 O3/x86_64 认证。
本轮未运行其他架构转换，未给出其耗时数字；782.346 s 只适用于本批 x86_64 3,853 成员/并发4。

## 6. 第二段与补丁状态

| 用户要求 | 本次状态 |
| --- | --- |
| S/spec x86_64 %install 转换、新增 Source、不改宏 | NOT RUN；消费者未全部通过，S/spec SHA 保持原值 |
| spec 最小 patch、git apply --check、patch SHA | **无 spec 修法补丁；路径和 SHA 不适用** |
| archive-fix-trial 精确认证入口及正负测试 | NOT RUN；build_llvm_x86_64.py 与起点 HEAD 完全一致 |
| 18 GiB/swap0/4-4-1/debuginfo4 完整 LLVM 构建 | **0 次**；未启动，CMake 门禁不适用 |
| 22 个新 RPM inventory、新解包 | 无新 RPM，temp/toolchain-archivefix 未作为本次产物创建 |
| 新 RPM 全量索引/成员次序/分段、compiler-rt 对照 | NOT RUN |
| 新 RPM 原 brp 链执行及零 GNU strip 格式错误 | NOT RUN；没有改任何宏，不能把“未执行”写成零错误通过 |
| 新旧包逐文件差异分类/工具 SHA 对照 | NOT RUN |
| 新 RPM A/B/共享库/GC 消费者 | NOT RUN |
| Tizen 最小测试包 bfd / lld 两次 GBS 构建和 %check | **0 次**，均 NOT RUN |
| 是否可提交归档修复到 Gerrit | **NO，验收未完成；本轮不推 Gerrit** |

已闭合的范围：后端选项补齐后的离线格式/完整索引/静态 PIC/抽样分段；A 的 GNU ld/lld O2 结果；B 的 GNU ld 和库内 lld 实际链接/运行。
尚未闭合：B 外层 lld、共享库动态加载、GC、原归档反例、spec/完整 RPM/Tizen 消费者。
不能用前三个成功项替代用户要求的全部门禁。

## 7. 功能检查、保护检查和收尾

- `tools/test_convert_static_archives.py`：8 项 PASS，含记录开关的最后一项生效、缺失/冲突拒绝、不得带 LTO、同名成员和确定性归档、PIC 正负对照。
- `tools/test_compare_native_conversion_options.py`：4 项 PASS；实际 as/readelf 检查、同数量不同节名/可见性负例、重复节区计数。
- `tools/test_verify_native_archive_consumers.py`：3 项 PASS；对象链接正例、loader/cc1 回归负例、LTO/plugin 参数负例。
- 这些是入口/策略功能测试，**不把未执行的共享库/GC/反例当作测试通过**。日志：`E/*tests.log`。
- `E/preservation-check.json`：W/spec、S/spec 和 docs/25–27 SHA 未变；构建门禁、离线资源入口未变。
- `E/scope-cleanup.json`：三个 scope 均 inactive/dead、cgroup 路径消失；`E/post-failure-processes.json` 无遗留构建/链接进程。

| 自检 | 回答 |
| --- | --- |
| 旧转换结果是否复用/覆盖 | 否，新目录重新转换全部 bitcode |
| 新命令是否传 LTO | 否；原 IR 的命令记录仍保留原 -flto，不等于实际转换参数 |
| 同名成员、原机器码、完整索引是否验证 | 是，225 归档检查和逐成员证据齐全 |
| 选项对照是否偷偷要求/宣称字节相同 | 否；逐项报告节区、符号与重定位，解释流水线/布局差异 |
| GNU ld 无 LTO/无插件是否有实际成功证据 | 有：A 和 B 的 GNU ld 组成功，完整 driver/argv/运行记录保留；不代表全验收成功 |
| 全部消费者门禁是否通过 | 否，B-lld 分配失败即停，其后均 NOT RUN |
| 是否修改 spec/LLVM 源码/RPM 宏 | 否 |
| 是否完整构建 LLVM、构建测试包或 Chromium | 否，均 0 次 |
| 是否跑 BOLT/性能校准/向 Gerrit 推送 | 否 |
| 失败后是否改参数重试 | 否 |
| 资源监控/独占锁是否回收 | 是，scope-cleanup.json、lock-released.json、final-cleanup.json |
| STATUS 是否同 commit 更新 | 是；定位命令：git log -1 -- docs/28_static_archive_native_conversion_v2.md |

所有原始输出均在 E（完整绝对前缀见 §0），主要索引：

- 基线/锁：precheck.json、rpm-identity.json、baseline-content-check.json、baseline-check.log、lock-*.json。
- 源选项：original-compile-commands.json、option-classification.json、all-original-options.json、all-bitcode-original-options.json、source-evidence.txt、trapping-math-record.json。
- 对照：options/plan.json、comparison.json、review.json、readelf/反汇编/driver 原文与差异文件。
- 转换：conversion-summary.json、conversion/summary.json、conversion/members/ 每归档 before/after.json、每成员 ir-settings/convert/relocations。
- 抽查：function-section-check/results.json 及 readelf 原文。
- 消费者：consumers/ 完整源码、输入/预期 IR、全部 compile/link/run argv、log/time/json、driver 展开、实际运行库列表、result.json。
- 资源：options-scope/、conversion-scope/、consumer-scope/ 的 launch/commands/build.log、time-v、samples/process-memory、memory-summary、outcome。
- 保护/回收：tool-identities.json、preservation-check.json、scope-cleanup.json、post-failure-processes.json、final-cleanup.json。

超过 10 MB 的 .a/.o/二进制/原始数据保留本机，不提交 GitHub。

## 附录 A：225 个归档转换结果

全部行成员顺序/身份、x86_64 ET_REL、索引多重集合与 PIC 静态检查均 PASS；不是 RPM 或完整消费者认证。
完整新旧 SHA、原命令和逐成员信息见 C/summary.json 及 members/ 下 before/after.json。

| 归档（usr/lib64/） | 成员 | BC→ELF | 原 ELF | 前 B | 后 B | 索引条目 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| libLLVMAArch64AsmParser.a | 1 | 1 | 0 | 4874780 | 6893338 | 62 |
| libLLVMAArch64CodeGen.a | 63 | 63 | 0 | 93637138 | 122389448 | 4339 |
| libLLVMAArch64Desc.a | 12 | 12 | 0 | 8790320 | 12139650 | 658 |
| libLLVMAArch64Disassembler.a | 2 | 2 | 0 | 2002576 | 2891522 | 24 |
| libLLVMAArch64Info.a | 1 | 1 | 0 | 95582 | 109418 | 10 |
| libLLVMAArch64Utils.a | 1 | 1 | 0 | 1022860 | 1275944 | 62 |
| libLLVMABI.a | 1 | 1 | 0 | 27172 | 27106 | 1 |
| libLLVMARMAsmParser.a | 1 | 1 | 0 | 4114928 | 5281016 | 76 |
| libLLVMARMCodeGen.a | 49 | 49 | 0 | 59210366 | 75145022 | 3410 |
| libLLVMARMDesc.a | 13 | 13 | 0 | 5966318 | 8057644 | 434 |
| libLLVMARMDisassembler.a | 1 | 1 | 0 | 2257304 | 3899352 | 8 |
| libLLVMARMInfo.a | 1 | 1 | 0 | 93594 | 106986 | 10 |
| libLLVMARMUtils.a | 1 | 1 | 0 | 139416 | 161576 | 10 |
| libLLVMAggressiveInstCombine.a | 2 | 2 | 0 | 3290774 | 4142074 | 110 |
| libLLVMAnalysis.a | 131 | 125 | 6 | 134030922 | 167649884 | 9363 |
| libLLVMAsmParser.a | 4 | 4 | 0 | 10663380 | 13656758 | 658 |
| libLLVMAsmPrinter.a | 27 | 27 | 0 | 30774180 | 37204402 | 1956 |
| libLLVMBPFAsmParser.a | 1 | 1 | 0 | 490640 | 618142 | 28 |
| libLLVMBPFCodeGen.a | 26 | 26 | 0 | 19082078 | 22685390 | 1688 |
| libLLVMBPFDesc.a | 5 | 5 | 0 | 839732 | 982304 | 110 |
| libLLVMBPFDisassembler.a | 1 | 1 | 0 | 291164 | 297004 | 4 |
| libLLVMBPFInfo.a | 1 | 1 | 0 | 91270 | 101344 | 7 |
| libLLVMBinaryFormat.a | 14 | 14 | 0 | 2994558 | 3840472 | 247 |
| libLLVMBitReader.a | 5 | 5 | 0 | 11509418 | 14377108 | 506 |
| libLLVMBitWriter.a | 4 | 4 | 0 | 8448570 | 12335882 | 243 |
| libLLVMBitstreamReader.a | 1 | 1 | 0 | 672008 | 867898 | 48 |
| libLLVMCAS.a | 15 | 15 | 0 | 7837688 | 9372568 | 427 |
| libLLVMCFGuard.a | 1 | 1 | 0 | 750524 | 887178 | 18 |
| libLLVMCFIVerify.a | 2 | 2 | 0 | 2147476 | 2540524 | 151 |
| libLLVMCGData.a | 7 | 7 | 0 | 4890264 | 6053066 | 296 |
| libLLVMCodeGen.a | 238 | 237 | 1 | 250523280 | 309230198 | 14191 |
| libLLVMCodeGenTypes.a | 1 | 1 | 0 | 94620 | 121410 | 6 |
| libLLVMCore.a | 80 | 80 | 0 | 84203524 | 108913924 | 7628 |
| libLLVMCoroutines.a | 11 | 11 | 0 | 12862536 | 15439752 | 339 |
| libLLVMCoverage.a | 3 | 3 | 0 | 7331182 | 9054598 | 214 |
| libLLVMDTLTO.a | 1 | 1 | 0 | 485968 | 547072 | 35 |
| libLLVMDWARFCFIChecker.a | 4 | 4 | 0 | 1573624 | 1782882 | 122 |
| libLLVMDWARFLinker.a | 2 | 2 | 0 | 120604 | 127072 | 3 |
| libLLVMDWARFLinkerClassic.a | 4 | 4 | 0 | 6648528 | 7887016 | 416 |
| libLLVMDWARFLinkerParallel.a | 11 | 11 | 0 | 15430734 | 18205574 | 819 |
| libLLVMDWP.a | 2 | 2 | 0 | 1423520 | 1740564 | 68 |
| libLLVMDebugInfoBTF.a | 2 | 2 | 0 | 1232706 | 1608904 | 65 |
| libLLVMDebugInfoCodeView.a | 40 | 40 | 0 | 15137966 | 19514906 | 1772 |
| libLLVMDebugInfoDWARF.a | 29 | 29 | 0 | 24375292 | 29232472 | 1908 |
| libLLVMDebugInfoDWARFLowLevel.a | 3 | 3 | 0 | 1094162 | 1363484 | 60 |
| libLLVMDebugInfoGSYM.a | 14 | 14 | 0 | 8206230 | 10543558 | 504 |
| libLLVMDebugInfoLogicalView.a | 19 | 19 | 0 | 25733758 | 31377046 | 2322 |
| libLLVMDebugInfoMSF.a | 4 | 4 | 0 | 1725236 | 2216994 | 173 |
| libLLVMDebugInfoPDB.a | 93 | 93 | 0 | 29948434 | 36522520 | 3174 |
| libLLVMDebuginfod.a | 4 | 4 | 0 | 2117992 | 2591862 | 197 |
| libLLVMDemangle.a | 6 | 6 | 0 | 2421668 | 3726450 | 767 |
| libLLVMDiff.a | 3 | 3 | 0 | 1349944 | 1715016 | 82 |
| libLLVMDlltoolDriver.a | 1 | 1 | 0 | 675070 | 807748 | 15 |
| libLLVMExecutionEngine.a | 5 | 5 | 0 | 3144502 | 3937996 | 265 |
| libLLVMExegesis.a | 25 | 25 | 0 | 15890110 | 18878154 | 822 |
| libLLVMExegesisAArch64.a | 1 | 1 | 0 | 1076316 | 1355912 | 37 |
| libLLVMExegesisX86.a | 2 | 2 | 0 | 2441458 | 3200732 | 73 |
| libLLVMExtensions.a | 1 | 1 | 0 | 27942 | 28162 | 2 |
| libLLVMFileCheck.a | 1 | 1 | 0 | 2707708 | 3454862 | 239 |
| libLLVMFrontendAtomic.a | 1 | 1 | 0 | 557552 | 691416 | 22 |
| libLLVMFrontendDirective.a | 1 | 1 | 0 | 52380 | 58204 | 1 |
| libLLVMFrontendDriver.a | 1 | 1 | 0 | 101978 | 106746 | 4 |
| libLLVMFrontendHLSL.a | 6 | 6 | 0 | 2050758 | 2536698 | 129 |
| libLLVMFrontendOffloading.a | 3 | 3 | 0 | 3435454 | 3934314 | 106 |
| libLLVMFrontendOpenACC.a | 1 | 1 | 0 | 193824 | 269846 | 11 |
| libLLVMFrontendOpenMP.a | 4 | 4 | 0 | 10101866 | 13240828 | 571 |
| libLLVMFuzzMutate.a | 4 | 4 | 0 | 4457938 | 5403798 | 210 |
| libLLVMFuzzerCLI.a | 1 | 1 | 0 | 368288 | 455194 | 8 |
| libLLVMGlobalISel.a | 30 | 30 | 0 | 30399224 | 38998706 | 2127 |
| libLLVMHipStdPar.a | 1 | 1 | 0 | 1078348 | 1294444 | 18 |
| libLLVMIRPrinter.a | 1 | 1 | 0 | 194296 | 214970 | 12 |
| libLLVMIRReader.a | 1 | 1 | 0 | 510364 | 625872 | 13 |
| libLLVMInstCombine.a | 15 | 15 | 0 | 38363862 | 49160210 | 2421 |
| libLLVMInstrumentation.a | 28 | 28 | 0 | 48745550 | 60554610 | 2005 |
| libLLVMInterfaceStub.a | 3 | 3 | 0 | 2707424 | 3377390 | 116 |
| libLLVMInterpreter.a | 3 | 3 | 0 | 2729236 | 4020704 | 166 |
| libLLVMJITLink.a | 35 | 35 | 0 | 43854792 | 52323618 | 2507 |
| libLLVMLTO.a | 6 | 6 | 0 | 19886408 | 22542308 | 893 |
| libLLVMLibDriver.a | 1 | 1 | 0 | 969160 | 1183798 | 25 |
| libLLVMLineEditor.a | 1 | 1 | 0 | 262042 | 309326 | 26 |
| libLLVMLinker.a | 2 | 2 | 0 | 3566984 | 4126960 | 109 |
| libLLVMMC.a | 70 | 70 | 0 | 26865518 | 32792224 | 2012 |
| libLLVMMCA.a | 24 | 24 | 0 | 5719358 | 6776938 | 516 |
| libLLVMMCDisassembler.a | 5 | 5 | 0 | 755262 | 857968 | 59 |
| libLLVMMCJIT.a | 1 | 1 | 0 | 1133612 | 1364980 | 83 |
| libLLVMMCParser.a | 13 | 13 | 0 | 8974300 | 12056802 | 305 |
| libLLVMMIRParser.a | 3 | 3 | 0 | 6391244 | 8302686 | 315 |
| libLLVMObjCARCOpts.a | 8 | 8 | 0 | 5573878 | 6594226 | 144 |
| libLLVMObjCopy.a | 26 | 26 | 0 | 18755368 | 22489410 | 1124 |
| libLLVMObject.a | 36 | 36 | 0 | 36229380 | 42919506 | 2665 |
| libLLVMObjectYAML.a | 29 | 29 | 0 | 44639128 | 59168528 | 3619 |
| libLLVMOptDriver.a | 2 | 2 | 0 | 6892208 | 8067228 | 572 |
| libLLVMOption.a | 4 | 4 | 0 | 1766016 | 2339734 | 128 |
| libLLVMOrcDebugging.a | 7 | 7 | 0 | 7483054 | 8593618 | 410 |
| libLLVMOrcJIT.a | 57 | 57 | 0 | 86983258 | 102092560 | 5160 |
| libLLVMOrcShared.a | 7 | 7 | 0 | 1100678 | 1292968 | 160 |
| libLLVMOrcTargetProcess.a | 15 | 15 | 0 | 9955228 | 11955410 | 551 |
| libLLVMPasses.a | 6 | 6 | 0 | 45016450 | 56112162 | 9766 |
| libLLVMPlugins.a | 1 | 1 | 0 | 146814 | 160254 | 2 |
| libLLVMProfileData.a | 21 | 21 | 0 | 33022822 | 44655670 | 2560 |
| libLLVMRemarks.a | 11 | 11 | 0 | 5117214 | 6221326 | 419 |
| libLLVMRuntimeDyld.a | 8 | 8 | 0 | 9462968 | 11263406 | 921 |
| libLLVMSandboxIR.a | 15 | 15 | 0 | 9963148 | 11682580 | 1674 |
| libLLVMScalarOpts.a | 81 | 81 | 0 | 125040642 | 152741868 | 4116 |
| libLLVMSelectionDAG.a | 26 | 26 | 0 | 55822938 | 78634320 | 3756 |
| libLLVMSupport.a | 179 | 175 | 4 | 44309346 | 57661498 | 4993 |
| libLLVMSupportLSP.a | 3 | 3 | 0 | 2793464 | 3732054 | 251 |
| libLLVMSymbolize.a | 5 | 5 | 0 | 4829590 | 6074076 | 332 |
| libLLVMTableGen.a | 14 | 14 | 0 | 11789056 | 15164270 | 1073 |
| libLLVMTableGenBasic.a | 13 | 13 | 0 | 9411646 | 12185040 | 361 |
| libLLVMTableGenCommon.a | 23 | 23 | 0 | 28135432 | 36407104 | 1686 |
| libLLVMTarget.a | 5 | 5 | 0 | 1580756 | 1816770 | 189 |
| libLLVMTargetParser.a | 15 | 15 | 0 | 5674402 | 7853802 | 364 |
| libLLVMTelemetry.a | 1 | 1 | 0 | 235708 | 293446 | 17 |
| libLLVMTextAPI.a | 15 | 15 | 0 | 10020890 | 12953402 | 509 |
| libLLVMTextAPIBinaryReader.a | 1 | 1 | 0 | 1414020 | 1722358 | 52 |
| libLLVMTransformUtils.a | 94 | 94 | 0 | 96853102 | 117722746 | 3562 |
| libLLVMVectorize.a | 33 | 33 | 0 | 86713910 | 109954874 | 4812 |
| libLLVMWindowsDriver.a | 1 | 1 | 0 | 321640 | 449310 | 14 |
| libLLVMWindowsManifest.a | 1 | 1 | 0 | 402650 | 461204 | 27 |
| libLLVMX86AsmParser.a | 1 | 1 | 0 | 3512772 | 4426026 | 80 |
| libLLVMX86CodeGen.a | 66 | 66 | 0 | 115303032 | 155716736 | 4564 |
| libLLVMX86Desc.a | 16 | 16 | 0 | 11916092 | 17489566 | 2278 |
| libLLVMX86Disassembler.a | 1 | 1 | 0 | 1553368 | 4350188 | 4 |
| libLLVMX86Info.a | 1 | 1 | 0 | 89482 | 98228 | 6 |
| libLLVMX86TargetMCA.a | 1 | 1 | 0 | 137814 | 162210 | 14 |
| libLLVMXRay.a | 14 | 14 | 0 | 5172708 | 6226342 | 438 |
| libLLVMipo.a | 45 | 45 | 0 | 115556998 | 143953740 | 5246 |
| libarcher_static.a | 1 | 1 | 0 | 709448 | 902270 | 9 |
| libclangAPINotes.a | 5 | 5 | 0 | 9659868 | 13291554 | 440 |
| libclangAST.a | 114 | 114 | 0 | 230364922 | 310997140 | 26686 |
| libclangASTMatchers.a | 3 | 3 | 0 | 17098112 | 19946726 | 494 |
| libclangAnalysis.a | 31 | 31 | 0 | 48744872 | 54280024 | 2344 |
| libclangAnalysisFlowSensitive.a | 18 | 18 | 0 | 21959454 | 22779134 | 885 |
| libclangAnalysisFlowSensitiveModels.a | 3 | 3 | 0 | 13934446 | 16578484 | 1246 |
| libclangAnalysisLifetimeSafety.a | 10 | 10 | 0 | 11088326 | 13245156 | 307 |
| libclangAnalysisScalable.a | 4 | 4 | 0 | 874110 | 1076572 | 40 |
| libclangApplyReplacements.a | 1 | 1 | 0 | 1716482 | 2258704 | 117 |
| libclangBasic.a | 73 | 73 | 0 | 48594198 | 53439930 | 6167 |
| libclangChangeNamespace.a | 1 | 1 | 0 | 6155072 | 7388962 | 605 |
| libclangCodeGen.a | 101 | 101 | 0 | 219606070 | 259333370 | 7734 |
| libclangCrossTU.a | 1 | 1 | 0 | 1852100 | 2107986 | 106 |
| libclangDaemon.a | 82 | 82 | 0 | 177215514 | 211512204 | 7271 |
| libclangDaemonTweaks.a | 20 | 20 | 0 | 39566066 | 45926080 | 512 |
| libclangDependencyScanning.a | 7 | 7 | 0 | 7917672 | 9811016 | 446 |
| libclangDirectoryWatcher.a | 2 | 2 | 0 | 716314 | 850084 | 32 |
| libclangDoc.a | 11 | 11 | 0 | 24918148 | 33777900 | 1972 |
| libclangDocSupport.a | 2 | 2 | 0 | 379852 | 471418 | 10 |
| libclangDriver.a | 76 | 76 | 0 | 76126900 | 102978706 | 5935 |
| libclangDynamicASTMatchers.a | 5 | 5 | 0 | 51442378 | 66575532 | 6495 |
| libclangEdit.a | 3 | 3 | 0 | 1616232 | 1967996 | 75 |
| libclangExtractAPI.a | 6 | 6 | 0 | 16909170 | 23206096 | 1241 |
| libclangFormat.a | 23 | 23 | 0 | 19479866 | 25745424 | 1168 |
| libclangFrontend.a | 32 | 32 | 0 | 56621002 | 75408826 | 2631 |
| libclangFrontendTool.a | 1 | 1 | 0 | 1099362 | 1185088 | 14 |
| libclangHandleCXX.a | 1 | 1 | 0 | 514850 | 612292 | 36 |
| libclangHandleLLVM.a | 1 | 1 | 0 | 1510004 | 1647782 | 27 |
| libclangIncludeCleaner.a | 8 | 8 | 0 | 10889168 | 13062746 | 282 |
| libclangIncludeFixer.a | 6 | 6 | 0 | 3831196 | 4585712 | 164 |
| libclangIncludeFixerPlugin.a | 1 | 1 | 0 | 891206 | 957700 | 128 |
| libclangIndex.a | 9 | 9 | 0 | 15628096 | 18512482 | 265 |
| libclangIndexSerialization.a | 1 | 1 | 0 | 341666 | 407702 | 15 |
| libclangInstallAPI.a | 8 | 8 | 0 | 9276748 | 11225958 | 710 |
| libclangInterpreter.a | 10 | 10 | 0 | 11054336 | 11999338 | 478 |
| libclangLex.a | 25 | 25 | 0 | 24823768 | 31194110 | 1497 |
| libclangMove.a | 2 | 2 | 0 | 6544622 | 7695100 | 380 |
| libclangOptions.a | 2 | 2 | 0 | 1158292 | 1441206 | 24 |
| libclangParse.a | 18 | 18 | 0 | 32397796 | 39277850 | 1358 |
| libclangQuery.a | 2 | 2 | 0 | 6203984 | 6763448 | 325 |
| libclangReorderFields.a | 2 | 2 | 0 | 3663994 | 4465864 | 155 |
| libclangRewrite.a | 3 | 3 | 0 | 1512124 | 1797478 | 79 |
| libclangRewriteFrontend.a | 8 | 8 | 0 | 3424270 | 3774930 | 241 |
| libclangSema.a | 86 | 86 | 0 | 347385702 | 401026782 | 10187 |
| libclangSerialization.a | 17 | 17 | 0 | 57396436 | 73419922 | 3164 |
| libclangStaticAnalyzerCheckers.a | 134 | 134 | 0 | 184402564 | 203611274 | 6526 |
| libclangStaticAnalyzerCore.a | 49 | 49 | 0 | 63939322 | 76933338 | 3639 |
| libclangStaticAnalyzerFrontend.a | 7 | 7 | 0 | 7620978 | 7500860 | 225 |
| libclangSupport.a | 1 | 1 | 0 | 750028 | 979584 | 47 |
| libclangTidy.a | 9 | 9 | 0 | 14027276 | 16967812 | 650 |
| libclangTidyAbseilModule.a | 22 | 22 | 0 | 49671914 | 54966470 | 2993 |
| libclangTidyAlteraModule.a | 6 | 6 | 0 | 11507890 | 12572560 | 485 |
| libclangTidyAndroidModule.a | 17 | 17 | 0 | 27905792 | 29965152 | 1148 |
| libclangTidyBoostModule.a | 3 | 3 | 0 | 5481838 | 5990184 | 171 |
| libclangTidyBugproneModule.a | 105 | 105 | 0 | 261792300 | 292228194 | 15809 |
| libclangTidyCERTModule.a | 1 | 1 | 0 | 2618622 | 2834826 | 135 |
| libclangTidyConcurrencyModule.a | 3 | 3 | 0 | 4800888 | 5142566 | 113 |
| libclangTidyCppCoreGuidelinesModule.a | 32 | 32 | 0 | 68425502 | 75533126 | 3977 |
| libclangTidyCustomModule.a | 2 | 2 | 0 | 3385102 | 3709432 | 43 |
| libclangTidyDarwinModule.a | 3 | 3 | 0 | 4586320 | 4917030 | 110 |
| libclangTidyFuchsiaModule.a | 8 | 8 | 0 | 12816724 | 13671956 | 355 |
| libclangTidyGoogleModule.a | 16 | 16 | 0 | 29916542 | 32539456 | 1304 |
| libclangTidyHICPPModule.a | 6 | 6 | 0 | 11395730 | 12378282 | 522 |
| libclangTidyLLVMLibcModule.a | 5 | 5 | 0 | 8165866 | 8629272 | 205 |
| libclangTidyLLVMModule.a | 9 | 9 | 0 | 18048700 | 19647680 | 795 |
| libclangTidyLinuxKernelModule.a | 2 | 2 | 0 | 3172032 | 3409660 | 72 |
| libclangTidyMPIModule.a | 3 | 3 | 0 | 4970726 | 5366690 | 64 |
| libclangTidyMain.a | 1 | 1 | 0 | 1384694 | 1820940 | 109 |
| libclangTidyMiscModule.a | 28 | 28 | 0 | 66384070 | 73489072 | 3325 |
| libclangTidyModernizeModule.a | 50 | 50 | 0 | 157657284 | 183027596 | 10328 |
| libclangTidyObjCModule.a | 10 | 10 | 0 | 16878450 | 18272696 | 606 |
| libclangTidyOpenMPModule.a | 3 | 3 | 0 | 4897156 | 5262686 | 120 |
| libclangTidyPerformanceModule.a | 21 | 21 | 0 | 47561864 | 52598424 | 3052 |
| libclangTidyPlugin.a | 1 | 1 | 0 | 860756 | 989446 | 31 |
| libclangTidyPortabilityModule.a | 6 | 6 | 0 | 10491864 | 11269716 | 410 |
| libclangTidyReadabilityModule.a | 59 | 59 | 0 | 153356446 | 170138912 | 7593 |
| libclangTidyUtils.a | 23 | 23 | 0 | 35972392 | 39993608 | 1224 |
| libclangTidyZirconModule.a | 1 | 1 | 0 | 1421768 | 1502138 | 7 |
| libclangTooling.a | 17 | 17 | 0 | 12731232 | 15460956 | 731 |
| libclangToolingASTDiff.a | 1 | 1 | 0 | 6122252 | 6879038 | 84 |
| libclangToolingCore.a | 2 | 2 | 0 | 1585990 | 1996790 | 103 |
| libclangToolingInclusions.a | 3 | 3 | 0 | 1411784 | 1652280 | 55 |
| libclangToolingInclusionsStdlib.a | 1 | 1 | 0 | 1169404 | 1611900 | 30 |
| libclangToolingRefactoring.a | 12 | 12 | 0 | 32120646 | 39499616 | 383 |
| libclangToolingSyntax.a | 8 | 8 | 0 | 10389626 | 13354140 | 304 |
| libclangTransformer.a | 7 | 7 | 0 | 12336640 | 13771252 | 266 |
| libclangdMain.a | 2 | 2 | 0 | 6948846 | 8314068 | 676 |
| libclangdRemoteIndex.a | 1 | 1 | 0 | 100048 | 103998 | 2 |
| libclangdSupport.a | 16 | 16 | 0 | 4838814 | 5858298 | 405 |
| libfindAllSymbols.a | 8 | 8 | 0 | 8067408 | 8924516 | 493 |
| liblldCOFF.a | 18 | 18 | 0 | 26049746 | 34231348 | 1792 |
| liblldCommon.a | 13 | 13 | 0 | 4521058 | 5906708 | 341 |
| liblldELF.a | 41 | 41 | 0 | 70073250 | 90489890 | 4021 |
| liblldMachO.a | 30 | 30 | 0 | 29987584 | 37908310 | 2217 |
| liblldMinGW.a | 1 | 1 | 0 | 789500 | 1055272 | 13 |
| liblldWasm.a | 14 | 14 | 0 | 13501042 | 16736056 | 1246 |

## 附录 B：10 个函数分段抽样

| 归档 | 原 ordinal / 成员 | 定义 FUNC 数 | 结果 |
| --- | --- | ---: | --- |
| libLLVMAArch64AsmParser.a | 0 / AArch64AsmParser.cpp.o | 464 | PASS |
| libLLVMBitstreamReader.a | 0 / BitstreamReader.cpp.o | 30 | PASS |
| libLLVMDemangle.a | 0 / Demangle.cpp.o | 2 | PASS |
| libLLVMInterpreter.a | 0 / Execution.cpp.o | 111 | PASS |
| libLLVMRemarks.a | 0 / BitstreamRemarkParser.cpp.o | 82 | PASS |
| libLLVMX86TargetMCA.a | 0 / X86CustomBehaviour.cpp.o | 9 | PASS |
| libclangEdit.a | 0 / Commit.cpp.o | 26 | PASS |
| libclangStaticAnalyzerCore.a | 0 / APSIntType.cpp.o | 1 | PASS |
| libclangTidyOpenMPModule.a | 0 / ExceptionEscapeCheck.cpp.o | 30 | PASS |
| liblldWasm.a | 0 / Driver.cpp.o | 97 | PASS |
