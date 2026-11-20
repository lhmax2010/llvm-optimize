# 145 · RPM 差异归类与 standalone BOLT 构建

## 执行前冻结的 PM 规则

- R-B：llvm-debugsource 中 /usr/src/debug/llvm-<version>-<release>.x86_64 的 release 前缀差异（1 对 2.1），去掉前缀后路径、权限、属主、大小、SHA 全部一致 → 已裁决的口径 B，归类通过。
- R-ID1（非 BOLT 的 ELF 文件）：C2 侧有 .note.gnu.build-id，PS5 侧没有；节差异只出现在布局相关的节（.note.gnu.build-id、.dynamic、.dynsym、.dynstr、.got、.got.plt、.rela.dyn、.rela.plt、.shstrtab、.gnu.hash、.hash、.gnu.version*、.eh_frame_hdr、.eh_frame 的地址字段）；并且对两侧做“地址归一化反汇编”：llvm-objdump -d --no-show-raw-insn --no-leading-addr --symbolize-operands，把全部十六进制地址和偏移替换为占位符后，按函数逐个比较指令序列，必须完全一致 → 归类为 PS4 的 build-id 修改。
- R-ID2（BOLT 后的 clang-22）：同样做地址归一化反汇编，按函数比较；BOLT 拆分出的 .cold 片段按函数名合并后比较。全部函数指令序列一致 → 归类为 build-id 引起的布局变化；有不一致的函数，列出前 20 个函数名和差异原文，不归类（STOP 该类）。
- R-ID3（debuginfo 包）：新增的 /usr/lib/debug/.build-id 目录及其下的链接（链接目标必须指向本包对应的二进制或 .debug 文件，build-id 一致）；.debug 文件内容差异只来自 build-id note 和地址（对 .debug 文件同样检查 DWARF 编译单元列表一致：llvm-dwarfdump --debug-info 的 DW_TAG_compile_unit 名称集合相同）。
- R-PS4：文件在包之间移动、新增或删除，必须能对应到 ps1-ps4.diff 或 ps4-parent-vs-ps5.diff 中的具体修改（%files 行、Obsoletes、DESTDIR 安装、libgomp/libiomp5 链接、clang.cfg 的追加内容等），逐条写出对应的 diff 行号。
- 其他任何差异 → 无法归类，列出原文。
