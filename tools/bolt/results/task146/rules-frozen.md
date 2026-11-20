# 146 · RPM 差异归类 v2

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
