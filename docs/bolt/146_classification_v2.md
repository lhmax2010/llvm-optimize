# 146 · RPM 差异归类 v2

## 结论

**269 条中 138 条归类通过，131 条仍为 UNCLASSIFIED，归类门禁 STOP。** v2 仅用于 145 号未归类条目。两份留存 RPM 的比较输入及 145 号报告和结果原样保留。没有执行构建。[冻结规则及 SHA](../../tools/bolt/results/task146/rules-frozen.sha256) · [本次汇总](../../tools/bolt/results/task146/classification-v2-summary.json)

| 规则 | 核对 | 通过 | 未通过 |
|---|---:|---:|---:|
| R-ID1b | 132 | 2 | 130 |
| R-ID3b | 133 | 133 | 0 |
| R-PS4b | 3 | 3 | 0 |
| R-ID2b | 1 | 0 | 1 |
| 合计 | 269 | 138 | 131 |

[269 条逐条证明](../../tools/bolt/results/task146/entries-v2.json) · [131 条未归类原文及原因](../../tools/bolt/results/task146/unclassified-v2.json)

## R-ID1b · 非 BOLT ELF

132/132 的 `.gnu_debuglink` 文件名完全相同，132/132 的 C2 CRC 与逐个从实际 `.debug` 文件重新计算的 CRC32 一致。

- `lld` 和 `llvm-exegesis` 分别比较了 78,218 和 32,910 个函数键。两者覆盖全部带大小的可执行符号范围，地址归一化后的指令序列全部一致。[lld 逐函数核对](../../tools/bolt/results/task146/id1b-190-exact.json) · [llvm-exegesis 逐函数核对](../../tools/bolt/results/task146/id1b-217-exact.json)
- 128 个 ELF 的差异包含白名单外的 `.relro_padding`，其中部分同时存在 `.text`、`.rodata` 等差异。例如 `clang-apply-replacements` 的 `.relro_padding` 为 NOBITS，节大小从 3,520 变为 3,488 字节。记录节大小和地址，按原 R-ID1 白名单判定。[128 条节原始字段](../../tools/bolt/results/task146/id1b-relro-padding-records.json)
- `LLVMgold.so` 和 `ompdModule.so` 的 C2 ELF 均无 GNU build-id。两项的 debuglink CRC 核对通过，新增 build-id 的前提未满足。[所有 ID1b 条目](../../tools/bolt/results/task146/entries-v2.json)

## R-ID3b · DWARF 与字符串表

对每份输入运行 `llvm-dwarfdump --debug-info --recurse-depth=0`，提取 `DW_TAG_compile_unit` 下的 `DW_AT_name`。两侧各枚举 88,987 个编译单元。只替换两个批准的绝对前缀，133/133 文件各自的名称集合一致。对段内的 NUL 结尾字符串按内容集合比较，同时保留原始词条数和规范化集合 SHA256。

| 字符串表 | PS5 词条数 | C2 词条数 | 两侧各规范化的前缀词条 | 规范化后内容不同 |
|---|---:|---:|---:|---:|
| `.debug_str` | 11,675,005 | 11,675,005 | 11,712 | 0 |
| `.debug_line_str` | 0 | 0 | 0 | 0 |

两侧 `clang-22.debug` 都没有 DWARF 节。初步脚本要求名称集合非空，随后以 ELF 节表和 `llvm-dwarfdump` 原文验证两侧确实为空集，按冻结的集合相等条件通过。[空集证明](../../tools/bolt/results/task146/clang-debug-empty-cu-proof.json) · [逐文件计数和摘要](../../tools/bolt/results/task146/entries-v2.json)

## R-PS4b · 默认 LLD

`ClangConfig.cmake` 和 `clang/Config/config.h` 只将 `CLANG_DEFAULT_LINKER` 的空字符串改为 `lld`，逐字节替换可重现两个 C2 文件。对应 `ps4-parent-vs-ps5.diff` 第 24 行的 `-DCLANG_DEFAULT_LINKER=lld`。[父提交 diff](../../tools/bolt/results/task144/ps4-parent-vs-ps5.diff) · [文件 diff 原文](../../tools/bolt/results/task146/entries-v2.json)

`libclangDriver.a` 中唯一变化成员为 `Driver.cpp.o`。330 个可执行节的地址归一化反汇编中，唯一变化是构造函数的两条写入指令，用 `lld\0` 和长度 3 替换空字符串和长度 0。301 个可分配节的重定位表按指令位置与字符串实际值归一化后相同，字符串值的变化限于 ELF `.strtab` 的局部字符串编号。展开帧的 PC 相应移动 3 字节。首次证据匹配器误将反汇编附注中的立即数文本当作规范化后仍应保留的文字，修正为核对原始指令与操作数偏移，保留初次结果和修正 diff。[对象比较](../../tools/bolt/results/task146/driver-v2.json) · [PS5 构造函数原文](../../tools/bolt/results/task146/driver/old.constructor.txt) · [C2 构造函数原文](../../tools/bolt/results/task146/driver/new.constructor.txt) · [帧地址 diff](../../tools/bolt/results/task146/driver/frames.diff) · [证据匹配修正](../../tools/bolt/results/task146/driver-proof-correction.diff)

## R-ID2b · 发货 clang-22

复用了 145 号地址省略版的原始反汇编和调试符号副本，通过带地址版交叉验证每条指令。按实际 ELF 符号范围分函数，合并冷片段并应用 v2 的符号化操作数替换。146,959 个函数键均在两侧存在，146,957 个完全相同。以下是剩余的全部两个符号，均在 `.text`，同属 `clang::driver::Driver::Driver`，两侧各自的 C1 与 C2 都指向同一实现的范围。

```text
_ZN5clang6driver6DriverC1EN4llvm9StringRefES3_RNS_17DiagnosticsEngineENSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEENS2_18IntrusiveRefCntPtrINS2_3vfs10FileSystemEEE
_ZN5clang6driver6DriverC2EN4llvm9StringRefES3_RNS_17DiagnosticsEngineENSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEENS2_18IntrusiveRefCntPtrINS2_3vfs10FileSystemEEE
```

PS5 的函数序列为 427 条主体与 310 条冷片段指令，C2 为 732 条。除了 `lld` 和长度的写入变化，指令差异还包括条件跳转和复制序列。每个符号的全部 31 个差异段已保留原文。以下为两侧第 60 条指令起的第一处差异，其中条件跳转助记符自身发生变化。

```diff
- je	 <_ZN5clang6driver6DriverC2EN4llvm9StringRefES3_RNS_17DiagnosticsEngineENSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEENS2_18IntrusiveRefCntPtrINS2_3vfs10FileSystemEEE.cold.0>
+ jne	 <L1>
+ movq	0x8(%rsp), %rax
+ movzbl	(%rax), %eax
+ movb	%al, (%rbp)
+ jmp	 <L2>
```

[两处符号的全部反汇编差异原文](../../tools/bolt/results/task146/clang-v2-raw-differences.txt) · [归一化前后配对](../../tools/bolt/results/task146/clang-v2-disassembly.json) · [字面量与其他指令差异](../../tools/bolt/results/task146/clang-v2-interpretation.json)

## STOP 原文

```text
STOP R-ID2b: 2 of 146959 normalized function keys differ; both are clang::driver::Driver constructor aliases, and the differences are not limited to the default linker literal or its length.
STOP 146: 131 of 269 RPM differences do not satisfy the frozen v2 rules; see unclassified-v2.json
```

[服务记录](../../tools/bolt/results/task146/service-journal.txt) · [留在本地的原始工具输出和 SHA256](../../tools/bolt/results/task146/local-files.json)

## 执行前冻结的规则 v2

仅适用于 145 号剩余的 269 条差异。145 号的冻结规则和结果原样保留。

- R-ID1b（.gnu_debuglink）：两侧 .gnu_debuglink 的文件名部分完全相同；C2 侧的 CRC 等于 C2 对应 .debug 文件的 CRC32（逐个计算，不引用旧结果）；除 .gnu_debuglink 外，其余差异满足原 R-ID1（布局节白名单 + 地址归一化反汇编按函数完全一致）。
- R-ID3b（.debug 文件）：把字符串中的 /usr/src/debug/llvm-22.1.8-2.1.x86_64 与 /usr/src/debug/llvm-22.1.8-1.x86_64 视为同一前缀（与已裁决的口径 B 相同）后，DW_TAG_compile_unit 名称集合完全相同；.debug_str/.debug_line_str 中，除该前缀外不存在其他内容不同的字符串（列出比较方法和计数）。
- R-PS4b（默认链接器）：同路径的内容差异，如果 diff 只涉及 CLANG_DEFAULT_LINKER（"" → "lld"），并对应 ps4-parent-vs-ps5.diff 中 -DCLANG_DEFAULT_LINKER=lld 的行 → 归类为 PS4 父提交的默认 LLD 修改。libclangDriver.a 中 Driver.cpp.o 的差异：对两侧 Driver.cpp.o 做地址归一化反汇编和字符串表比较，差异只能是 "lld" 字面量及其引用（长度常量、字面量地址、字符串编号）。
- R-ID2b（clang-22）：在原 R-ID2 的地址归一化之外，再把符号化操作数中的局部字面量符号名（.str*、.L.str*、.Lstr*、带 .llvm.<数字> 后缀的名字）以及 <符号+偏移> 形式的最近符号注释统一替换为占位符，然后按函数比较指令序列：
  - 仍不同的函数必须全部属于 clang driver（clang::driver::* 或 clang_main），并且差异只涉及默认链接器字面量（"lld"）及其长度；
  - 其余函数必须完全一致。
  - 列出 v2 归一化后仍不同的全部函数名和差异原文。

不满足 v2 规则的条目一律保持 UNCLASSIFIED，原文列出。
