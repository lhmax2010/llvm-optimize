# 41：BOLT clang 崩溃定位现状探测（2026-10-28）

现行BOLT clang在这个pragma崩溃中有20帧显示函数名、7帧只有地址，有无llvm-symbolizer均如此。保留符号表且提供symbolizer后变为24帧有名字、3帧只有地址，clang增大33,142,648字节；不提供symbolizer时仍为20/7。完整符号表版能离线解析全部24个clang地址，但llvm-objcopy生成“只含符号文件”时发生SIGSEGV，因此该文件的大小和离线解析能力未验证成功。

**状态：部分完成。** 未生成只含符号文件；其它六次崩溃测试、布局核对、24地址离线解析、大小估算与15/15对象抽查均完成。崩溃定位方案仍挂账：**探测已完成，待用户决定**。不改变发布参数或推荐立即改变交付形态。

## 1. 输入与边界

源码f308fe08、39号products和构建根只读。最终clang从本轮clang RPM流式解出，SHA为8c2429d870f421a29a9914458bc4d4ff2ce359a15e0bdd20f39bfb4580c40bdf；ordinary SHA d5090159915657b235b96f1202c058e1efd1647d6a2225ac8fdb2906aeaa501d；strip前BOLT输出SHA与identity.before_sha256核对一致。所有写入仅在W/temp/crash-probe-20261028及本报告证据目录。

宿主loader加39号根lib64/usr/lib64，resource-dir为本轮build/lib64/clang/22；固定CPU2，setarch -R。测试副本与任何llvm-symbolizer隔离，absent时PATH仅含空目录、unset LLVM_SYMBOLIZER_PATH；present时PATH仅含执行本轮symbolizer的POSIX sh wrapper。core limit=0，避免生成大core。源文件只有`#pragma clang __debug crash`。使用-fsyntax-only和-fno-crash-diagnostics保留栈、避免另建预处理重现包；这不是正常编译失败。

主探测service CPUQuota100%、MemoryMax4GiB、swap0、nice19、idle I/O，运行5分8秒，cgroup峰值3.9GiB（含文件缓存），非编译器RSS。仅在新临时目录执行CMake `file(RPATH_CHANGE)`脚本处理符号表副本，与发布流程一致；没有在构建根配置或运行CMake/Ninja，没有构建软件包、提权或改变系统设置。

## 2. debuginfo完整文件清单

BOLT clang-debuginfo共有27项，无clang-22自身调试文件；纯hybrid保全包有28项，`/usr/lib/debug/usr/bin/clang-22.debug`为1,652,177,424字节。以下为RPM头文件清单，不需要解压整个大debuginfo包。包来源和SHA见[debuginfo.json](../../tools/bolt/results/crash-probe-20261028/debuginfo.json)。

### bolt

来源：`/home/linhao/Toolchain/development/llvm-optimize/temp/oldtext-final-20261027/products/RPMS/clang-debuginfo-22.1.8-1.x86_64.rpm`

| 路径 | 字节 |
|---|---:|
| `/usr/lib/debug` | 0 |
| `/usr/lib/debug/usr` | 0 |
| `/usr/lib/debug/usr/bin` | 0 |
| `/usr/lib/debug/usr/bin/clang-apply-replacements.debug` | 1839592 |
| `/usr/lib/debug/usr/bin/clang-change-namespace.debug` | 5123888 |
| `/usr/lib/debug/usr/bin/clang-check.debug` | 801872 |
| `/usr/lib/debug/usr/bin/clang-doc.debug` | 15710304 |
| `/usr/lib/debug/usr/bin/clang-extdef-mapping.debug` | 668208 |
| `/usr/lib/debug/usr/bin/clang-format.debug` | 1182648 |
| `/usr/lib/debug/usr/bin/clang-include-cleaner.debug` | 8241480 |
| `/usr/lib/debug/usr/bin/clang-include-fixer.debug` | 3373712 |
| `/usr/lib/debug/usr/bin/clang-installapi.debug` | 3632288 |
| `/usr/lib/debug/usr/bin/clang-move.debug` | 4679008 |
| `/usr/lib/debug/usr/bin/clang-nvlink-wrapper.debug` | 1480672 |
| `/usr/lib/debug/usr/bin/clang-offload-bundler.debug` | 706704 |
| `/usr/lib/debug/usr/bin/clang-query.debug` | 4104272 |
| `/usr/lib/debug/usr/bin/clang-refactor.debug` | 2198944 |
| `/usr/lib/debug/usr/bin/clang-reorder-fields.debug` | 3043576 |
| `/usr/lib/debug/usr/bin/clang-scan-deps.debug` | 3339640 |
| `/usr/lib/debug/usr/bin/clang-sycl-linker.debug` | 1260104 |
| `/usr/lib/debug/usr/bin/clang-tidy.debug` | 274462568 |
| `/usr/lib/debug/usr/bin/clangd.debug` | 369810440 |
| `/usr/lib/debug/usr/bin/find-all-symbols.debug` | 4564576 |
| `/usr/lib/debug/usr/bin/modularize.debug` | 6492864 |
| `/usr/lib/debug/usr/lib64` | 0 |
| `/usr/lib/debug/usr/lib64/libclang-cpp.so.22.1.debug` | 857890304 |
| `/usr/lib/debug/usr/lib64/libclang.so.22.1.8.debug` | 485910072 |

### hybrid

来源：`/home/linhao/Toolchain/development/llvm-optimize/temp/hybrid-local-20261023/preserved-before-delete/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/RPMS/x86_64/clang-debuginfo-22.1.8-1.x86_64.rpm`

| 路径 | 字节 |
|---|---:|
| `/usr/lib/debug` | 0 |
| `/usr/lib/debug/usr` | 0 |
| `/usr/lib/debug/usr/bin` | 0 |
| `/usr/lib/debug/usr/bin/clang-22.debug` | 1652177424 |
| `/usr/lib/debug/usr/bin/clang-apply-replacements.debug` | 1839592 |
| `/usr/lib/debug/usr/bin/clang-change-namespace.debug` | 5123888 |
| `/usr/lib/debug/usr/bin/clang-check.debug` | 801872 |
| `/usr/lib/debug/usr/bin/clang-doc.debug` | 15710304 |
| `/usr/lib/debug/usr/bin/clang-extdef-mapping.debug` | 668208 |
| `/usr/lib/debug/usr/bin/clang-format.debug` | 1182648 |
| `/usr/lib/debug/usr/bin/clang-include-cleaner.debug` | 8241480 |
| `/usr/lib/debug/usr/bin/clang-include-fixer.debug` | 3373712 |
| `/usr/lib/debug/usr/bin/clang-installapi.debug` | 3632288 |
| `/usr/lib/debug/usr/bin/clang-move.debug` | 4679008 |
| `/usr/lib/debug/usr/bin/clang-nvlink-wrapper.debug` | 1480672 |
| `/usr/lib/debug/usr/bin/clang-offload-bundler.debug` | 706704 |
| `/usr/lib/debug/usr/bin/clang-query.debug` | 4104272 |
| `/usr/lib/debug/usr/bin/clang-refactor.debug` | 2198944 |
| `/usr/lib/debug/usr/bin/clang-reorder-fields.debug` | 3043576 |
| `/usr/lib/debug/usr/bin/clang-scan-deps.debug` | 3339640 |
| `/usr/lib/debug/usr/bin/clang-sycl-linker.debug` | 1260104 |
| `/usr/lib/debug/usr/bin/clang-tidy.debug` | 274462568 |
| `/usr/lib/debug/usr/bin/clangd.debug` | 369810440 |
| `/usr/lib/debug/usr/bin/find-all-symbols.debug` | 4564576 |
| `/usr/lib/debug/usr/bin/modularize.debug` | 6492864 |
| `/usr/lib/debug/usr/lib64` | 0 |
| `/usr/lib/debug/usr/lib64/libclang-cpp.so.22.1.debug` | 857890304 |
| `/usr/lib/debug/usr/lib64/libclang.so.22.1.8.debug` | 485910072 |

## 3. build-id与六份崩溃栈

最终BOLT、ordinary、strip前BOLT输出三者均无`.note.gnu.build-id`，没有可比较的ID值；不是“三个相同的有效ID”。见[build-ids.json](../../tools/bolt/results/crash-probe-20261028/build-ids.json)及build-id-*.stdout原文。

| 编译器 | symbolizer | 有函数名帧 | 仅地址帧 | 总帧 | 原文 |
|---|---|---:|---:|---:|---|
| ordinary | absent | 20 | 7 | 27 | [stderr](../../tools/bolt/results/crash-probe-20261028/crash-ordinary-absent.stderr) |
| ordinary | present | 41 | 4 | 45 | [stderr](../../tools/bolt/results/crash-probe-20261028/crash-ordinary-present.stderr) |
| final | absent | 20 | 7 | 27 | [stderr](../../tools/bolt/results/crash-probe-20261028/crash-final-absent.stderr) |
| final | present | 20 | 7 | 27 | [stderr](../../tools/bolt/results/crash-probe-20261028/crash-final-present.stderr) |
| symbols | absent | 20 | 7 | 27 | [stderr](../../tools/bolt/results/crash-probe-20261028/crash-symbols-absent.stderr) |
| symbols | present | 24 | 3 | 27 | [stderr](../../tools/bolt/results/crash-probe-20261028/crash-symbols-present.stderr) |

ordinary带DWARF且symbolizer展开内联帧，总帧45；其它栈27帧。表中计数是输出帧，不将内联帧增加误当作物理调用层数变化。即使完全strip，dynsym仍能提供部分名字，不能说“所有名字丢失”。没有外部symbolizer时dladdr式回溯不会利用普通.symtab，所以符号表版仍为20/7。

原始计数脚本起初只识别`#N`格式，未识别无symbolizer的`N module address`格式；只修正读取原文的统计，不重跑或改写六份崩溃测试。正确统计见crashes-corrected.json，初始输出保留以便复核。

## 4. 布局与离线解析

所有SHF_ALLOC非NOBITS节的地址、文件位置、大小及内容逐字节一致，程序头相同。整个PT_LOAD字节并非绝对相同：仅偏移40、41、42、43、60、62共6字节不同，属于ELF头的e_shoff/e_shnum/e_shstrndx，指向不同的非加载符号/节名表布局；代码与运行数据未变。符号表版额外保留.symtab、.strtab、.comment、.GCC.command.line、.note.bolt_info。详见layout.json，不把这6字节隐瞒为“全文件相同”。

最终clang是PIE；从final-present栈直接读取LLVM打印的模块相对偏移，未把ASLR绝对地址直接输入symbolizer。用符号表版--obj、--inlining=false解析24个clang帧，24/24得到函数名；三个libc帧不拿clang文件解析。符号表不含源码行调试信息，函数名成功不代表恢复行号。见offline-addresses-corrected.json、offline-resolution.json、offline-symbols-corrected.stdout。

`llvm-objcopy --only-keep-debug clang.symbols clang.symbols-only`返回-11（SIGSEGV），未产出有效文件，栈落在`llvm::objcopy::elf::ELFWriter<...>::writeSegmentData()`。没有换工具重试、重建或修复objcopy；原因尚未定位，不能仅凭这一帧断言根因。原文：

```text
PLEASE submit a bug report to https://github.com/llvm/llvm-project/issues/ and include the crash backtrace and instructions to reproduce the bug.
Stack dump:
0.	Program arguments: /home/linhao/Toolchain/development/llvm-optimize/temp/oldtext-final-20261027/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-objcopy --only-keep-debug /home/linhao/Toolchain/development/llvm-optimize/temp/crash-probe-20261028/clang.symbols /home/linhao/Toolchain/development/llvm-optimize/temp/crash-probe-20261028/clang.symbols-only
Stack dump without symbol names (ensure you have llvm-symbolizer in your PATH or set the environment var `LLVM_SYMBOLIZER_PATH` to point to it):
0  libLLVM.so.22.1 0x00007260196f9658 llvm::sys::PrintStackTrace(llvm::raw_ostream&, int) + 40
1  libLLVM.so.22.1 0x00007260196f6375 llvm::sys::RunSignalHandlers() + 293
2  libLLVM.so.22.1 0x00007260196f9dc1
3  libc.so.6       0x0000726017262ac0
4  libc.so.6       0x0000726017374277
5  libLLVM.so.22.1 0x000072601b950647 llvm::objcopy::elf::ELFWriter<llvm::object::ELFType<(llvm::endianness)1, true>>::writeSegmentData() + 87
6  libLLVM.so.22.1 0x000072601b951da6 llvm::objcopy::elf::ELFWriter<llvm::object::ELFType<(llvm::endianness)1, true>>::write() + 22
7  libLLVM.so.22.1 0x000072601b92c437
8  libLLVM.so.22.1 0x000072601b92c6fd llvm::objcopy::elf::executeObjcopyOnBinary(llvm::objcopy::CommonConfig const&, llvm::objcopy::ELFConfig const&, llvm::object::ELFObjectFileBase&, llvm::raw_ostream&) + 269
9  libLLVM.so.22.1 0x000072601b918e4e llvm::objcopy::executeObjcopyOnBinary(llvm::objcopy::MultiFormatConfig const&, llvm::object::Binary&, llvm::raw_ostream&) + 94
10 libLLVM.so.22.1 0x00007260196d8c9e llvm::writeToOutput(llvm::StringRef, std::function<llvm::Error (llvm::raw_ostream&)>) + 350
11 llvm-objcopy    0x000072601cf94c59
12 llvm-objcopy    0x000072601cf95657
13 libc.so.6       0x000072601724db97
14 libc.so.6       0x000072601724dc55 __libc_start_main + 133
15 llvm-objcopy    0x000072601cf762e1
```

初始分析空地址集、后续尝试打开未生成的文件也都记录在steps.json；它们不是独立的clang正确性失败。后续只用现有完整符号表版重新做日志解析与大小估算，不把未生成文件标成成功。

## 5. 大小与RPM增量估算

| 文件 | 字节 | xz preset5独立压缩字节 |
|---|---:|---:|
| final | 152532296 | 37739272 |
| symbols | 185674944 | 41256308 |
| symbols-only | 未生成 | 未测 |

符号表版比最终版增加33,142,648 B（21.73%）；估计clang RPM增加3,517,036 B。方法：实际RPM的payload compressor=xz、flags=5T；分别单流xz preset5压缩两个ELF，取压缩长度差，不构建RPM。此估算不包含cpio/header、线程分块或与其他文件跨文件压缩的影响，不能当成实测新RPM大小。原始size-estimate.json、sizes-followup.json保留输入、SHA和压缩耗时。首遍因不存在的symbols-only文件未保存汇总，补算仅两个有效ELF，未重做崩溃或产品验证。

## 6. 正确性抽查与结论

选docs/22沿用资产中的前5个独立TU，每个3目标，共15对。两份编译器依次覆盖相同路径/同inode，输入SHA、完整参数、resource-dir相同，完整.o逐字节相同，15/15 PASS；不删除.GCC.command.line。见[correctness.json](../../tools/bolt/results/crash-probe-20261028/correctness.json)及tu-*.json/stdout/stderr。

本轮没有改源码/spec/helper或已有products，没有发布任何Gerrit/sandbox提交。保留符号表能提高外部symbolizer/离线函数定位能力，但会增加包体；只含符号文件路径遇到工具崩溃，不能认定可交付。**崩溃定位仍挂账：探测已完成，待用户决定；symbols-only生成和验证未完成。**
