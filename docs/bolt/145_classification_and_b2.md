# 145 · RPM 差异归类与 standalone BOLT 构建

## 结论

**B2 standalone x86_64 构建与全部产物核对 PASS。** 归类部分按冻结口径 STOP：144 号余下 509 条中，240 条通过 R-ID3，269 条未归类。另有 12,142 对 debugsource 路径通过 R-B，对应 144 号的 24,284 条原始记录。B1 in-tree `llvm-bolt` 的完整 NEEDED 无法从留存 RPM 恢复。B1 复用 144 号 C2 产物。

比较对象为 C2 `5e58d65678e2d936b28eb4458bbd73a51abe5e06` 的 B1 RPM 与已有 QB 1232863 x86_64 RPM。执行前冻结规则的 SHA256 为 `4067819d9d0b239c6fb9d12e54eba2e10ce3f0210650c1f51f3f98e4c94105a2`。[冻结副本](../../tools/bolt/results/task145/rules-frozen.md)

## 逐条归类

| 规则 | 通过 | 无法归类 | 核对结果 |
|---|---:|---:|---|
| R-B | 12,142 对 | 0 | 直接读取两份 RPM 清单，只去掉 release 前缀。相对路径、mode、UID、GID、大小、SHA256 全部一致，无额外路径变化。该行在 509 条之外。 |
| R-ID1 | 0 | 132 | 每条均有白名单之外的 `.gnu_debuglink` 内容差异。该条件已经排除这 132 条，未进入逐函数反汇编成功判定。 |
| R-ID2 | 0 | 1 | clang-22 的 146,959 个函数键中 146,934 个一致，25 个差异，单侧存在为 0。 |
| R-ID3 | 240 | 133 | 109 个目录、131 个链接通过。133 个变化的 `.debug` 文件的 DWARF CU 名称集合均不同，字符串表中另有非地址值变化。 |
| R-PS4 | 0 | 3 | 509 条中没有 build-id 路径以外的增删移动。三个同路径内容变化未满足文件操作条件。 |

R-ID1 典型例子为 `clang-apply-replacements`，两侧 `.gnu_debuglink` CRC 各自与对应 debug 文件字节一致，分别为 `594d5738` 和 `e54fa42f`。R-ID3 中同一 `.debug` 文件的 `.debug_str` 含各自 release 的源文件路径。R-B 的授权范围是 debugsource 归档路径，逐条保留 `.debug` 文件的原始名称集合比较。[CRC 与 DWARF 字符串例子](../../tools/bolt/results/task145/debuglink-dwarf-examples.json) · [直接 RPM 复核](../../tools/bolt/results/task145/debugsource-first-a1/result.json)

R-ID3 初始脚本漏识别 RPM 生成的数字后缀 `.1`，第一次统计剩 270 条。按同一规则重查这一个链接，`lldb-devel-debuginfo` 中的 `.1` 与 `.1.debug` 分别指向对应的 `liblldb.so.22.1.8` 和 debug 文件，双方 build-id 均为 `5f6f2dca6e0826d6890bf54e495f6a50a0ce7791`，该条改判通过。其余链接与目录结果保持初次证据所示。[数字后缀验证](../../tools/bolt/results/task145/r-id3-numbered-link-proof.json)

R-PS4 里，`ClangConfig.cmake` 和 `clang/Config/config.h` 在原路径把 `CLANG_DEFAULT_LINKER` 从空设为 `lld`，对应 `ps4-parent-vs-ps5.diff` 第 24 行、`ps1-ps4.diff` 第 3253 行。`libclangDriver.a` 两侧各 76 个成员，只有 `Driver.cpp.o` 变化。此前已通过的 `clang.cfg` 追加对应父提交 diff 第 33–39 行，在 509 条之外。[逐行依据](../../tools/bolt/results/task145/r-ps4-source-line-evidence.json) · [PS4 父提交 diff](../../tools/bolt/results/task144/ps4-parent-vs-ps5.diff) · [PS1→PS4 diff](../../tools/bolt/results/task144/ps1-ps4.diff)

[509 条最终证据](../../tools/bolt/results/task145/entries-final-509.json) · [269 条未归类原始记录及依据](../../tools/bolt/results/task145/unclassified-final.json) · [汇总](../../tools/bolt/results/task145/classification-summary.json)

## R-ID2 clang-22 函数比较

用 B1 构建根的 LLVM 工具和对应加载器，对两份出货 clang 的实际指令字节运行 `llvm-objdump -d --no-show-raw-insn --no-leading-addr --symbolize-operands`。从各自匹配的 RPM debug 文件补回离线副本的符号表，复核 `.gnu_debuglink` CRC 和全部可执行节 SHA。用另一条带地址的反汇编逐行交叉核对，按符号大小裁定函数范围，排除范围外的对齐填充，将 `.cold` 及编号冷片段合并。旧侧 162,527 个符号范围、新侧 162,526 个均已覆盖。地址和偏移使用占位符，保留符号化操作数及非地址立即数。

精确范围比较中有 25 个函数键不匹配，均在 `.text`。例如 `clang_main` 的符号化比较操作数为 `.str.8.llvm.7132837829381176288` → `.str.9.llvm.520322885550654647`。初次按标签划分报告中的 104 个差异含函数范围外填充，归类采用已验证的符号范围结果。[前 20 个函数与反汇编 diff 原文](../../tools/bolt/results/task145/exact-first-a1/r-id2-symbol-ranges.json) · [全部 25 个名字](../../tools/bolt/results/task145/r-id2-different-function-names.txt) · [ELF 与调试符号配对](../../tools/bolt/results/task145/r-id2-pairing.json)

## B2 standalone

| 核对项 | 结果 |
|---|---|
| C2 源身份、GBS | PASS。独立 x86_64 构建，GBS 退出码 0。 |
| B1 RPM provider | PASS。用 B1 已签收的 RPM 建本地源，安装前后核对 EVR、VCS/提交和可取得的签名摘要字段。spec 原文输出 `LLVM provider Version-Release consistency check passed: 22.1.8-1`。 |
| bolt 包载荷 | PASS。7 个工具入口是 `llvm-bolt`、`perf2bolt`、`llvm-boltdiff`、`llvm-bolt-heatmap`、`llvm-bolt-binary-analysis`、`llvm-bat-dump`、`merge-fdata`，加 `libbolt_rt_instr.a`、`libbolt_rt_hugify.a`。 |
| Requires | PASS。有 `libllvm = 22.1.8`，无 `compiler-rt`。 |
| GNU_RELRO、debug build-id | PASS。7 个入口对应的 5 个真实 ELF 均有 GNU_RELRO，均与各自 debug 文件及 `.build-id` 链接配对。 |
| 注册目标 | PASS。`llvm-bolt --version` 列有 `x86-64` 和 `aarch64`。 |
| 两架构重写冒烟 | PASS。最小静态 ELF 均保留输入重定位，BOLT 进入 relocation mode。x86_64 原件与重写件实际退出码均为 37，AArch64 验证重写和输出 ELF。 |
| standalone CMake | PASS。`LLVM_LINK_LLVM_DYLIB=ON`，实际 ELF 依赖 `libLLVM.so.22.1`，编译生成 `X86BoltMnemonicTables.cpp.o`，嵌套 runtime 的 `CMAKE_C_FLAGS`、`CMAKE_CXX_FLAGS` 都为空。 |

正式一轮 04:00:43–04:17:43 PST，用时 17 分钟，Ninja 2 jobs，MemoryMax 12 GiB，服务记录内存峰值约 8.7 GiB，最低主机 MemAvailable 约 12.40 GiB。2 GiB 保护线触发 0 次，内存重试 0 次。首次准备因 OBS build 不接受 `file://` 本地仓库参数而停止，修正一次，使用绝对目录路径并复用已核对的 C2 导出。[首次准备日志](../../tools/bolt/results/task145/b2-first-a1/evidence/prep.txt) · [修正 diff](../../tools/bolt/results/task145/b2-preparation-correction.diff) · [B2 完整结果](../../tools/bolt/results/task145/b2-corrected-a1/result.json) · [RPM 构建原文](../../tools/bolt/results/task145/b2-corrected-a1/evidence/rpm-build-transcript.txt) · [安装的 provider](../../tools/bolt/results/task145/b2-corrected-a1/evidence/installed-providers.json) · [standalone 缓存](../../tools/bolt/results/task145/b2-corrected-a1/evidence/standalone-CMakeCache.txt) · [runtime 缓存](../../tools/bolt/results/task145/b2-corrected-a1/evidence/runtime-CMakeCache.txt)

## B1 in-tree llvm-bolt 的 NEEDED

核对 22 个 B1 二进制 RPM 的 SHA 与文件清单，均无 in-tree `llvm-bolt`。144 号对应工具位于已经清理的 BUILD 树，保留了 `readelf --wide -d` 命令和无 libLLVM.so 的门禁结论，该次 readelf 的完整 stdout 未单独写盘。B2 的独立包另有实测动态列表，依赖为 `libLLVM.so.22.1`、`libstdc++.so.6`、`libm.so.6`、`libc.so.6`。[B1 文件清单核对](../../tools/bolt/results/task145/needed-first-a1/b1-needed.json) · [B2 readelf 原文](../../tools/bolt/results/task145/b2-corrected-a1/evidence/standalone-readelf-dynamic.txt)

## STOP 原文与证据范围

- [B2 首次准备 STOP traceback](../../tools/bolt/results/task145/b2-first-a1/evidence/STOP.txt)
- [初始归类 STOP（270 条）](../../tools/bolt/results/task145/classify-first-a1/STOP.txt)
- [R-ID2 STOP](../../tools/bolt/results/task145/exact-first-a1/STOP.txt)
- [最终归类 STOP（269 条）](../../tools/bolt/results/task145/classification-final-STOP.txt)
- [B1 NEEDED STOP](../../tools/bolt/results/task145/needed-first-a1/STOP.txt)

读取了 B1 与 QB 的留存 RPM、下载收据、144 号比较记录与相关源码 diff、B1 原始构建日志、B2 的构建及产物证据。QB 比较使用留存副本。LLVM 的远端未发生写入。[提交证据索引](../../tools/bolt/results/task145/evidence-index.json) · [保留在本机的完整反汇编和文件 SHA256](../../tools/bolt/results/task145/local-files.json)

## 执行前冻结的 PM 规则

- R-B：llvm-debugsource 中 /usr/src/debug/llvm-<version>-<release>.x86_64 的 release 前缀差异（1 对 2.1），去掉前缀后路径、权限、属主、大小、SHA 全部一致 → 已裁决的口径 B，归类通过。
- R-ID1（非 BOLT 的 ELF 文件）：C2 侧有 .note.gnu.build-id，PS5 侧没有；节差异只出现在布局相关的节（.note.gnu.build-id、.dynamic、.dynsym、.dynstr、.got、.got.plt、.rela.dyn、.rela.plt、.shstrtab、.gnu.hash、.hash、.gnu.version*、.eh_frame_hdr、.eh_frame 的地址字段）；并且对两侧做“地址归一化反汇编”：llvm-objdump -d --no-show-raw-insn --no-leading-addr --symbolize-operands，把全部十六进制地址和偏移替换为占位符后，按函数逐个比较指令序列，必须完全一致 → 归类为 PS4 的 build-id 修改。
- R-ID2（BOLT 后的 clang-22）：同样做地址归一化反汇编，按函数比较；BOLT 拆分出的 .cold 片段按函数名合并后比较。全部函数指令序列一致 → 归类为 build-id 引起的布局变化；有不一致的函数，列出前 20 个函数名和差异原文，不归类（STOP 该类）。
- R-ID3（debuginfo 包）：新增的 /usr/lib/debug/.build-id 目录及其下的链接（链接目标必须指向本包对应的二进制或 .debug 文件，build-id 一致）；.debug 文件内容差异只来自 build-id note 和地址（对 .debug 文件同样检查 DWARF 编译单元列表一致：llvm-dwarfdump --debug-info 的 DW_TAG_compile_unit 名称集合相同）。
- R-PS4：文件在包之间移动、新增或删除，必须能对应到 ps1-ps4.diff 或 ps4-parent-vs-ps5.diff 中的具体修改（%files 行、Obsoletes、DESTDIR 安装、libgomp/libiomp5 链接、clang.cfg 的追加内容等），逐条写出对应的 diff 行号。
- 其他任何差异 → 无法归类，列出原文。
