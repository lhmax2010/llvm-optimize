# 60：本地/QB逐包比较与旧认证产物差异归因

Base-Dev 的12个二进制RPM内容全部通过；Toolchain的22个二进制包中，python-clang通过、debugsource只有release目录名差异，其余20包在严格规则下仍有差异。对本地T相对旧认证版的449个拒绝文件已全部审计：ThinLTO名字后缀变化、归档索引位移、compiler-rt记录节增长和AddLLVM文本变化都有具体证据。ompdModule.so确实有加载内容变化，虽与MODULE链接参数变化相伴，本轮没有隔离重链接证明每个字节的因果关系，因此仍列“未解释”，没有把归因结果变成新的门禁豁免。

## 1. 范围、身份、串行和证据

2026-11-05通宵任务的第二、三项；第一项见[59号](59_pgo_bolt_followup.md)。所有重操作使用独立systemd用户服务，MemoryMax=24,482,979,840B（MemTotal减8GiB）、swap0、CPUQuota1200%、nice10、ionice2/7；30GiB停止线持续检查。没有sudo、浏览器、QB操作、软件包构建、删除、LLVM源码/spec/helper修改。三个历史根严格只读。只执行了3次单文件C编译用于ThinLTO哈希实验，输出在新attribution目录。

主证据目录为 `tools/bolt/results/baseline-attribution-20261105/`；驱动和本轮比较器副本在 `tools/bolt/overnight-20261105/`。55号原比较器未改。大于1MiB的原始文本另附gzip；本地原文件保留。`SHA256SUMS`覆盖提交的证据；各服务保存完整argv、stdout/stderr、memory.events、资源采样和结束行。

## 2. 第二项：公开RPM下载与逐包比较

全部36个RPM已取得，`rpm-downloads.json`逐个记录公开URL、大小、SHA和本地对照RPM的SHA。3个先前下载文件经SHA核对复用，其余通过无cookie、无认证头的公开下载完成。文件保存在`W/temp/qb-1216409-1216410/full-rpms/{1216409,1216410}/`。

- T：`https://download.tizen.org/RBS/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261103.085926/repos/standard/`，二进制release 2.1。
- D：`https://download.tizen.org/RBS/TIZEN/Tizen/Tizen-Base-Dev/tizen-base-dev_20261103.090039/repos/standard/`，二进制release 5.1。
- 包目录为packages/x86_64、packages/noarch、debug；源码包在source。初次推定packages/src返回404；保留失败后读取公开目录，按其source入口取得源码包。另一次本地服务因输出路径用了相对路径而未执行下载，原文也保留；后续改用绝对证据路径，无鉴权或提权。
- 每个RPM的VCS指向`9e39fa8a61392652bb28b75fc26216675bcad1d5`。T发布的共享源码RPM头ARCH为armv7l，D源码RPM头ARCH为x86_64；它们都按.src.rpm比较，没有把T的源码包冒称为专属x86构建产物。

### 2.1 规则与测试

`.comment`仅检查新增、消失或计数变化的字符串是否为编译器/链接器标识；两边相同次数的Intel Corporation不拒绝。任意ELF的debuglink必须同文件名/填充，两边CRC各自匹配实际debug文件，debug文件对满足严格逐节规则；随后只在内存副本中将末尾4字节CRC归零，继续严格比较二进制其余部分。没有放宽.symtab、.strtab、ALLOC、程序头或其他调试节。

8个正反例全部通过：共同非标识字符串保留；改变非标识字符串拒绝；改变其计数拒绝；任意文件名的合法debuglink通过；坏CRC、坏文件名、坏符号.text、坏主程序.text各拒绝。原文在`rules-test-service/stderr`：

```text
Ran 8 tests in 0.003s
OK
```

RPM版本/release/VCS/buildtime/buildhost、payload mtime和属主/权限分开记录。初次比较将源码RPM的17个属主/权限差异挡在内容比较之前；`qb-rpm-comparison-v2.json`修正为先分列元数据、再完整核对内容，初版保留供追溯。二进制包没有这类属主/权限差异；源包的模型tar文件本身均相同。

### 2.2 每包结论

下表“内容差异”是严格规则拒绝的文件数；mtime与文件属性单列。不把包头时间/release变化算成文件内容变化。完整旧/新RPM头及每个文件的mtime/属性值在v2 JSON。

|项目|包|结论|内容差异文件|mtime变化|属性变化|
|---|---|---|---:|---:|---:|
|toolchain|clang / x86_64|FAIL|23|66|0|
|toolchain|clang-debuginfo / x86_64|FAIL|23|28|0|
|toolchain|clang-devel / x86_64|FAIL|1|237|0|
|toolchain|clang-devel-debuginfo / x86_64|FAIL|1|4|0|
|toolchain|compiler-rt / x86_64|FAIL|55|105|0|
|toolchain|compiler-rt-debuginfo / x86_64|FAIL|10|17|0|
|toolchain|libllvm / x86_64|FAIL|1|3|0|
|toolchain|libllvm-debuginfo / x86_64|FAIL|1|4|0|
|toolchain|libomp / x86_64|FAIL|3|3|0|
|toolchain|libomp-debuginfo / x86_64|FAIL|3|6|0|
|toolchain|libomp-devel / x86_64|FAIL|1|1|0|
|toolchain|lldb / x86_64|FAIL|5|8|0|
|toolchain|lldb-debuginfo / x86_64|FAIL|5|16|0|
|toolchain|lldb-devel / x86_64|FAIL|3|34|0|
|toolchain|lldb-devel-debuginfo / x86_64|FAIL|3|7|0|
|toolchain|llvm / x86_64|FAIL|82|98|0|
|toolchain|llvm-debuginfo / x86_64|FAIL|82|85|0|
|toolchain|llvm-debugsource / x86_64|内容PASS；release目录名变化|0|0|0|
|toolchain|llvm-devel / x86_64|FAIL|4|205|0|
|toolchain|llvm-devel-debuginfo / x86_64|FAIL|4|11|0|
|toolchain|llvm-static-devel / x86_64|FAIL|225|225|0|
|toolchain|python-clang / x86_64|PASS|0|0|0|
|toolchain|llvm / src|FAIL|1|17|17|
|basedev|clang / x86_64|PASS|0|66|0|
|basedev|clang-devel / x86_64|PASS|0|237|0|
|basedev|compiler-rt / x86_64|PASS|0|105|0|
|basedev|libllvm / x86_64|PASS|0|3|0|
|basedev|libomp / x86_64|PASS|0|3|0|
|basedev|libomp-devel / x86_64|PASS|0|1|0|
|basedev|lldb / x86_64|PASS|0|8|0|
|basedev|lldb-devel / x86_64|PASS|0|34|0|
|basedev|llvm / x86_64|PASS|0|98|0|
|basedev|llvm-devel / x86_64|PASS|0|205|0|
|basedev|llvm-static-devel / x86_64|PASS|0|225|0|
|basedev|python-clang / x86_64|PASS|0|0|0|
|basedev|llvm / src|FAIL|1|17|17|

原始严格路径集合结果为13/36包PASS；额外按用户允许的release元数据口径核对debugsource：两边12,142条路径只把`usr/src/debug/llvm-22.1.8-<release>.x86_64`中的release部分归一后，文件内容SHA、大小、模式、链接目标全部相同（`debugsource-release-path-check.json`）。它不应被描述为源码内容变化，但原始路径集合确实不同。此项不豁免其他ELF里嵌入的DWARF字节变化。

两个源码包除spec外的内容相同。spec差异全文见`toolchain-source-spec.diff`和`basedev-source-spec.diff`：VCS路径、Release是元数据；另有8条`%patch -P N -p1`与`%patchN -p1`的文本差异，仍记严格内容FAIL，未擅自增加“等价shell语法”例外。

### 2.3 所有失败文件与原因

全部537条失败文件记录在[`qb-failures.tsv`](../../tools/bolt/results/baseline-attribution-20261105/qb-failures.tsv)（T536，D1）；JSON保留对应旧/新SHA和证明。每行含项目、包、文件以及第一个严格拒绝原因/节名。这里的失败表示不满足字节规则，不表示运行功能已失败，本轮没有重跑90 TU。

|项目|拒绝原因/节|文件数|
|---|---|---:|
|toolchain|('non-record section changed', '.debug_info')|214|
|toolchain|('non-ELF member changed (including archive index)', '/')|203|
|toolchain|non-date/size archive header changed|68|
|toolchain|('non-record section changed', '.debug_line')|30|
|toolchain|('ELF header changed', 11, 37, 38)|14|
|toolchain|('non-record section changed', '.debug_aranges')|4|
|toolchain|('ELF header changed', 11, 36, 37)|2|
|toolchain|non-ELF file content changed|1|
|basedev|non-ELF file content changed|1|

本地T快照为tizen-base-toolchain_20261013.024319，QB T为tizen-base-toolchain_20261030.061318；两边D均为tizen-base-dev_20261030.061217。工具链环境不同可解释部分记录标识来源，但不能据此豁免.debug_info/.debug_line内容或节数量差异。cmp已单独证实T的clang-22及其符号文件符合本轮记录节/debuglink规则；这不代表整个clang包通过。

```text
ITEM2 已结束 2026-11-05T00:41:25.825515+08:00 status=differences reason=comparison-complete
```

## 3. 第三项：本地T对3ee2d847旧认证产物

输入是55号`T-rpm-rejected-files.json`中的449项（19包），逐项核对从RPM取得的内容SHA后分析。`attribution-files.json`保存每项身份和原门禁结果；`all-section-audits.jsonl.gz`包含每个变化ELF/归档成员的完整节名序列、节头变化、记录字符串及符号统计；`all-changed-names.jsonl.gz`列全量变化名字。复用第二项已解出的本地T文件时同样先核对载荷SHA。

### 3.1 符号和归档索引：证实主体，列出全部例外

- 共检查993,378个旧符号及相同数量的新符号。110,801条语义记录有变化，其中110,591条名字变化符合`.llvm.<数字>`后缀变化；这些名字的基础部分以及地址、大小、info、other、shndx均相同。43个文件有这类符号表变化，47个文件有符合归一化后的字符串表变化。
- 210条例外分别来自ompdModule.so的.dynsym（84条）和其.debug的.symtab（126条）：名字本身未变，但地址和节索引等属性变化。完整例外（无截断）在[`module-symbol-exceptions.tsv`](../../tools/bolt/results/baseline-attribution-20261105/module-symbol-exceptions.tsv)；语义集合差集420项是旧侧210加新侧210，不是420个独立符号。除此之外没有符号属性例外。
- 200个变化的归档索引全部通过后缀/目标校验。索引的351,642条变化记录中，名字没有变化，变化是成员偏移；独立复核使用成员的**次序+名称**，防止同名成员混淆，200/200目标仍相同。完整原值/新值见all-changed-names，次序证明见archive-index-ordinal-proof.json。
- 这些是归因证据，不是严格门禁豁免：.symtab/.strtab以及索引原始字节仍不同。

### 3.2 ThinLTO单文件实验：参数改变会改变模块哈希

使用新根平台clang（139,929,464B，SHA ac7d3aad80ed038e0759121b1cd01644096b6c49ef3e2c644cd72d71c4175427）及同根loader/库，不chroot。输入LLVM自身`llvm/lib/Support/BLAKE3/blake3_portable.c`，旧新源码SHA相同：`2bc25b0dad67b4329d0b49cfa075ab2b0d04e424addbddc4e9c389c52a192524`。

旧configure原文在full-20261030的GBS成功log.txt:L395，新configure在night/toolchain的成功log.txt:L673。两份CMakeCache及build.ninja实际对象FLAGS/DEFINES/INCLUDES的原文、行号和SHA收在configuration-evidence.json；实验保留两套实际FLAGS，共用新根的相同include路径和defines以隔离变量。两套参数的实质字符串差异是开头多出的`-ffunction-sections -fdata-sections`，后段原本也有这两项。argv固定`-o -`，分别保存stdout，避免输出文件名污染记录。完整argv、返回码、时间、SHA和bcanalyzer HASH原文在thinlto-probe.json。

|运行|bitcode SHA256|llvm-bcanalyzer HASH|
|---|---|---|
|old|`addcdf514f073b4bb6d93bbb3d690b14d01277a6870a0e28b2b40b478b3e2560`|`  <HASH op0=196974278 op1=923357849 op2=62127414 op3=3949019228 op4=1137177426/>`|
|new|`45c2dade7dc231febc702a0cdb1164a957bffe7b6de19f9dca66f93fe109b602`|`  <HASH op0=522892871 op1=912529554 op2=61144370 op3=2521988536 op4=4204398245/>`|
|repeat|`45c2dade7dc231febc702a0cdb1164a957bffe7b6de19f9dca66f93fe109b602`|`  <HASH op0=522892871 op1=912529554 op2=61144370 op3=2521988536 op4=4204398245/>`|

结论：旧/新HASH不同；同一新参数重复两次，HASH和整个bitcode SHA都相同。这直接证明参数字符串变化能改变此模块哈希，支持名字后缀变化的归因；并不把单TU实验外推为所有输出的功能验证。

### 3.3 compiler-rt：否定“新增函数分节改变ALLOC内容”

受影响的42个compiler-rt归档中，1237个成员有ALLOC位置/节头差异。它们的ALLOC内容全部相同，完整节名序列、.text.* / .data.* / .rodata.* / .bss.*列表也全部相同；旧命令已经有-ffunction-sections和-fdata-sections。1,237份记录命令的新旧差异均只是额外插入一次这两个token，没有例外。完整命令与节清单在alloc-layout-details.jsonl.gz，逐token差分在compiler-rt-causality.json。

例：libclang_rt.asan-x86_64.a / asan_allocator.cpp.o：.GCC.command.line大小2326→2362（+36B），起点43054不变；.eh_frame从45384→45416（+32B），大小5568不变，内容SHA两边均`6e74c4b49e9c120ed9794d2a1b2033be69ae26dee70319e5e4471e756545b060`。旧记录末尾45380到.eh_frame有4B填充，新末尾45416到.eh_frame为0B，故位移为36+(0−4)=32B。并非增加了新的函数节或改变了.eh_frame内容；原严格规则拒绝的是ALLOC文件位置变化。

全449文件范围，共269文件、5,066个ELF有ALLOC节头/位置差异。排除两个节顺序改变的MODULE文件后，5,064个ELF的5,064处ALLOC变化内容全部相同。两个MODULE必须按节名对齐复核，最终确认8个ALLOC节内容不同。初次按节次序配对得出的11处不是最终结论；两版原始证据保留。不能把“ALLOC section changed”直接译为代码被改变。

### 3.4 MODULE：配置变化证实，具体字节因果仍未解释

两份CMakeCache原文：

```text
old CMAKE_MODULE_LINKER_FLAGS:STRING=-Wl,-z,relro,--as-needed
new CMAKE_MODULE_LINKER_FLAGS:STRING=-Wl,-z,relro,--as-needed -Wl,--gc-sections
```

两份build.ninja:L61788均标明`C_MODULE_LIBRARY_LINKER__ompdModule_Release`。实际LINK_FLAGS原文：

```text
old LINK_FLAGS = -Wl,-z,relro,--as-needed -Wl,-z,nodelete -fuse-ld=lld -Wl,--color-diagnostics   -Xlinker --dependency-file=projects/openmp/libompd/gdb-plugin/CMakeFiles/ompdModule.dir/link.d
new LINK_FLAGS = -Wl,-z,relro,--as-needed -Wl,--gc-sections -Wl,-z,nodelete -fuse-ld=lld -Wl,--color-diagnostics   -Xlinker --dependency-file=projects/openmp/libompd/gdb-plugin/CMakeFiles/ompdModule.dir/link.d
```

ompdModule.so与其.debug的程序头都有差异；module-program-headers.json列出全部旧/新字段（ELF64顺序type,flags,offset,vaddr,paddr,filesz,memsz,align）。例如可执行LOAD从offset33504/vaddr37600/filesz21040变为33492/37588/21052，RW LOAD从offset55104/filesz2872变为55096/2880。可见变化与新增--gc-sections的MODULE链接输入相伴，但没有在本轮做隔离重链接，不能断言每个变化字节只由它导致。**推测：链接节保留和布局策略变化是主要原因；精确因果仍未解释。**

### 3.5 AddLLVM.cmake：证实来自混合链接提交的检查新增

完整打包文件diff如下；它与6e9d4f2→d4d6ca16的源码diff内容一致，不是CMake参数生成的差异。两边打包文件的SHA还分别与各自构建树的源码文件SHA完全相同；源码原件和git diff也随证据提交。

```diff
--- /home/linhao/Toolchain/development/llvm-optimize/temp/attribution-20261105/payload/llvm-devel-x86_64/old/usr/lib64/cmake/llvm/AddLLVM.cmake
+++ /home/linhao/Toolchain/development/llvm-optimize/temp/attribution-20261105/payload/llvm-devel-x86_64/new/usr/lib64/cmake/llvm/AddLLVM.cmake
@@ -1048,6 +1048,10 @@
   cmake_parse_arguments(H "" ""
     "LINK_COMPONENTS;LINK_LIBS;DEPENDS;OBJLIBS;ADDITIONAL_HEADERS" ${ARGN})
   llvm_map_components_to_libnames(components ${H_LINK_COMPONENTS} ${LLVM_LINK_COMPONENTS})
+  if(NOT components)
+    message(FATAL_ERROR
+      "${name}: empty LLVM component interface; declare LINK_COMPONENTS or disable TIZEN_HYBRID_LINK")
+  endif()
   set(static_consumer "$<BOOL:$<TARGET_PROPERTY:TIZEN_STATIC_LLVM>>")
   set(replacement "$<$<NOT:${static_consumer}>:LLVM>")
   foreach(component IN LISTS components)
```

### 3.6 .comment与debuglink重新判定

libomp.so.debug两边共同的Intel Corporation不再被拒绝，但之后.symtab仍不同，属于上面的名字后缀变化，故严格比较仍FAIL；没有把它误报为.comment问题。所有.comment旧/新字符串及计数随逐节审计保存。

133个带debuglink的文件重新核验：85 PASS，48 FAIL。失败中43项因符号文件.symtab、4项因.strtab、1项因MODULE程序头变化。clang-22的CRC本身与自己的符号文件一致，但其符号文件与旧认证版的严格逐节比较不通过，故整体仍FAIL。完整逐文件证明/错误在cert-debuglink-recheck.json。另独立计算了全部133对符号文件的CRC，两边存储CRC、实际CRC及文件名/填充全部匹配（cert-all-crc.json，133/133）；所以48项失败不能归咎于错误CRC。

### 3.7 未解释清单

其他可分类差异均已给出事实证据；尚未完成严格字节因果解释的是以下两文件。最终按节名对齐后的全部差异范围保存在module-named-sections.json，含旧/新节文件偏移和节内半开区间[start,end)，可直接换算文件偏移。all-section-audits和unexplained-ranges是初次按序遍历的原始记录；MODULE节序变化时，以module-named-sections为准，非MODULE原审计不受影响。符号属性例外另见210行TSV；完整程序头原值/新值另表。CRC依赖符号文件严格FAIL的48项也继续保留为门禁FAIL，不能当作通过。

|文件|节/字段|归因状态|
|---|---|---|
|usr/share/gdb/python/ompd/ompdModule.so|.dynamic、.dynsym、.eh_frame、.eh_frame_hdr、.init、.rela.dyn、.rodata、.text；程序头/节顺序|未解释：MODULE链接变化有证据，精确因果未隔离|
|usr/lib/debug/usr/share/gdb/python/ompd/ompdModule.so.debug|.debug_aranges、.debug_info、.debug_line、.debug_loc、.debug_ranges、.shstrtab、.symtab；程序头/节顺序|未解释：地址/布局及调试记录变化；.GCC.command.line另列记录节|

实际ALLOC内容差异全部位于`usr/share/gdb/python/ompd/ompdModule.so`：`.dynsym, .rela.dyn, .rodata, .eh_frame_hdr, .eh_frame, .text, .init, .dynamic`。对应.debug文件没有这些节的加载内容，但其程序头/符号地址变化不能忽略。未把“预期差异”当成“已证明无影响”。

```text
ITEM3 已结束 2026-11-05T01:04:01.863726+08:00 status=partial reason=449-files-audited-module-byte-causality-unproven
```

## 4. 文件索引、现场和结论

|证据|内容|
|---|---|
|rpm-downloads.json|36个公开RPM来源、SHA、大小、复用方式|
|qb-rpm-comparison-v2.json（gzip）/ qb-failures.tsv|每包内容结论、每文件错误、mtime和属性原值|
|manifests/|两边完整载荷清单|
|attribution-files.json / attribution-summary.json|449文件身份、严格结果和归因统计|
|all-changed-names.jsonl.gz / module-symbol-exceptions.tsv|全量名字变化和全部210条属性例外|
|all-section-audits.jsonl.gz / alloc-layout-details.jsonl.gz|每成员节清单、内容/位置、命令原文|
|archive-index-ordinal-proof.json|200归档索引目标名称+次序证明|
|thinlto-probe.json / probe-*-bcanalyzer.stdout|单文件3次编译的完整argv、SHA和HASH原文|
|configuration-evidence.json / module-program-headers.json|CMake/ninja原文与全部程序头|
|cert-debuglink-recheck.json|133个debuglink重新判定|
|module-named-sections.json / module-named-summary.json|最终MODULE按名字对齐的完整差异范围、节头和符号记录|
|unexplained-ranges.jsonl.gz|初次顺序遍历原始范围；MODULE以named结果为准，CRC以debuglink重判为准|
|各*-service/|独立服务命令、限制、资源、退出原文；非零前置尝试也保留|

采集末尾df原文（后续写证据/提交会略有变化）：

```text
Filesystem         1B-blocks          Used   Available Use% Mounted on
/dev/sda1      1967844950016 1814593863680 53214474240  98% /home
```

未删除任何文件；所有历史根只读。新复制/解包目录和单文件实验保留。第二项完成了全量比较，结果有FAIL；第三项完成全449项审计及小实验，但MODULE具体字节因果仍未解释。没有重跑软件包构建或90 TU，没有改变发布门禁。
