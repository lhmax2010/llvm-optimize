# 152 · 361624 PS6 评审取证

**镜像函数 1,784 个，144 B1 的 libLLVM.so.22.1 动态定义命中 0 个，145 B2 的 llvm-bolt 动态未定义命中 0 个，配对 debuginfo 可见内部定义 11 个。** PS6 将四个 analyzer 入口移到 clang。clang 的 Requires 链覆盖 llvm 中的 scan-view 可执行文件，覆盖不了 llvm-devel 中的共享资源或未随 B1 RPM 提供的 Python 模块。三个旧依赖名均无 Requires 或 BuildRequires 命中。

## 证据适用范围

144 B1 的 C2 提交 5e58d65678e2d936b28eb4458bbd73a51abe5e06 的 tree 为 ef1ab363fa8e9be29eb930916e86c6e8f10f11af，等于 361624 PS5。PS5 与 PS6 的 bolt/ 子树均为 007a88ce01f69f7e223ca337111a911cf6f38f22。PS5→PS6 只改 packaging/llvm.spec 和 packaging/llvm-tools-subpkgs.spec 的工具归属、Obsoletes 和说明。三个镜像源码文件也与 B2 debugsource 逐字节相同。符号结论来自保留的 B1/B2 RPM，PS6 打包归属来自 spec 对照。本任务未执行 PS6 构建。[源码核对](../../tools/bolt/results/task152/source-identity.json) · [代码 diff](../../tools/bolt/results/task152/PS5-to-PS6.diff)

## 2 · X86 镜像符号

清单包括 PS6 镜像编译单元的 7 个直接函数、GET_REGINFO_MC_DESC 所包含的静态内联 InitX86MCRegisterInfo，以及 B2 保留生成表中 1,776 个 mnemonic 函数定义。两个 Body.inc 为对应包装函数提供函数体。B2 llvm-bolt 的 DT_NEEDED 含 libLLVM.so.22.1。llvm-bolt.debug 的 build-id 为 77cb5dedfd048492b154f3fa8c1c9fa9b8200c64，debuglink CRC32 为 e4f3b4e8，均与二进制核对一致。[逐函数 TSV](../../tools/bolt/results/task152/mirror-symbols.tsv) · [结构化原文行](../../tools/bolt/results/task152/mirror-symbols.json) · [生成表](../../tools/bolt/results/task152/X86GenMnemonicTables.inc)

| 函数范围 | libLLVM 动态导出 | llvm-bolt 动态导入 | llvm-bolt 配对调试符号表 |
|---|---:|---:|---|
| 全部 1,784 项 | 0 | 0 | 11 项有定义，1,773 项无同名定义行 |
| isNOP、getX86SubSuperRegister、needsAddressSizeOverride | 0 | 0 | 三项均有定义 |
| 其余可见定义 | 0 | 0 | getOpcodeForShortImmediateForm、is16BitMemOperand、isADD、isAND、isCMP、isJCC、isSUB、isTEST |

三个评审点的解码原文如下。

~~~text
000000000032d050 T llvm::X86::isNOP(unsigned int)
000000000032d690 T llvm::getX86SubSuperRegister(llvm::MCRegister, unsigned int, bool)
000000000032db00 T llvm::X86_MC::needsAddressSizeOverride(llvm::MCInst const&, llvm::MCSubtargetInfo const&, int, unsigned long)
~~~

使用 nm -D --defined-only、nm -D --undefined-only 和对调试文件的 nm --defined-only，各用 c++filt 解码。三份原文分别有 41,749、640 和 7,564 行。[libLLVM 动态定义](../../tools/bolt/results/task152/libllvm-defined.txt.gz) · [llvm-bolt 动态未定义](../../tools/bolt/results/task152/bolt-undefined.txt.gz) · [llvm-bolt 调试定义](../../tools/bolt/results/task152/bolt-debug-defined.txt.gz) · [11 条匹配原文](../../tools/bolt/results/task152/bolt-debug-defined.mirror-matches.txt) · [输出哈希](../../tools/bolt/results/task152/nm-output-manifest.json)

## 3 · 分析工具打包

| 路径或资源 | PS5 实测归属 | PS6 spec 归属及运行关系 |
|---|---|---|
| /usr/bin/{analyze-build,intercept-build,scan-build,scan-build-py} | llvm | 移至 clang。analyze-build、intercept-build、scan-build-py 是 Python 入口，scan-build 是 Perl。 |
| /usr/libexec/{analyze-c++,analyze-cc,c++-analyzer,ccc-analyzer,intercept-c++,intercept-cc} | clang | 仍属 clang。Perl scan-build 直接找 ccc-analyzer 和 c++-analyzer。 |
| /usr/lib*/libscanbuild | 22 个 B1 RPM 均无 | PS6 未新增。三个 Python 入口将 /usr/lib 加入模块搜索路径，随后导入 libscanbuild。 |
| /usr/lib*/libear | 22 个 B1 RPM 均无 | PS6 未新增。libscanbuild.intercept 导入 libear。PS6 %install 第 759–760 行仍删除这两个库目录下的内容。 |
| /usr/share/scan-build | llvm-devel | 仍在 llvm-devel 的 share 通配范围。Perl scan-build 生成 HTML 报告时读取 sorttable.js 和 scanview.css。 |
| /usr/share/scan-view | llvm-devel | 仍在 llvm-devel。scan-view 从该目录导入查看器模块。 |
| /usr/share/man/man1/scan-build.1 | llvm-devel，实物为 scan-build.1.gz | 仍在 llvm-devel。该文件是手册。 |
| /usr/bin/scan-view | llvm | 仍属 llvm。clang 的 Requires 会拉入同版本 release 的 llvm。 |

实物 clang 的 Requires 中有 llvm = 22.1.8-1，llvm 有 libllvm = 22.1.8-1。clang、llvm 和 libllvm 的留存 Requires 未要求 llvm-devel。llvm-devel 反向要求 llvm。PS6 保留这些 spec 关系。因此 clang 和其 llvm 依赖能提供四个入口、libexec 脚本与 scan-view 程序，无法通过该链保证其支持文件齐全。B1 两包的 Requires 均记录 /usr/bin/env，未直接点名入口所需的 python3 或 perl。没有运行分析工具。[llvm 文件清单](../../tools/bolt/results/task152/llvm-rpm-qlp.txt) · [clang 文件清单](../../tools/bolt/results/task152/clang-rpm-qlp.txt) · [llvm-devel 文件清单](../../tools/bolt/results/task152/llvm-devel-rpm-qlp.txt) · [22 包清单](../../tools/bolt/results/task152/b1-analyzer-package-owners.json) · [Python 支持路径核对](../../tools/bolt/results/task152/python-support-paths.json) · [Requires](../../tools/bolt/results/task152/clang-rpm-requires.txt) · [入口和源码原文](../../tools/bolt/results/task152/runtime-source-excerpts.txt)

## 4 · 旧依赖名

检查了 144 B1、145 B2 首次和完成轮保留的 GBS 仓库及缓存、provider 仓库和构建根范围。共解析 8 份 repomd 指向的 primary 文件，5 份内容 SHA 不同，读到 6,605 条包记录，含重复快照。另读了留存的 2 个源 RPM 的 rpm -qp --requires。clang-analyzer、llvm-xray、llvm-prof-tools 在二进制 Requires、源包 BuildRequires 里均为 0。匹配按元数据字段及完整依赖名判断。[输入范围、计数与原文](../../tools/bolt/results/task152/dependency-scan.json)

## RPM 路径与 SHA256

下表的 B1 目录为 /home/linhao/Toolchain/development/llvm-optimize/archive/task144/b1-a1/gbs-driver/local/repos/tizen_base_toolchain_standard/x86_64/RPMS/，B2 目录为 /home/linhao/Toolchain/development/llvm-optimize/archive/task145/b2-corrected-a1/gbs-driver/local/repos/tizen_base_toolchain_standard/x86_64/RPMS/。下列 RPM 已重算哈希并与原始收据核对。其余参与文件归属扫查的 B1 路径及既有哈希见 22 包清单。

| 目录 | RPM | SHA256 |
|---|---|---|
| B1 | libllvm-22.1.8-1.x86_64.rpm | `83043cb3290738b569b5b41ddaac4cc93d9b6f5fc622b026f6d8edb3e47a5729` |
| B1 | llvm-22.1.8-1.x86_64.rpm | `c7e564b397b135f9a642de9812165d0965b27f6aba31bec63a8a351dee5b5ad2` |
| B1 | clang-22.1.8-1.x86_64.rpm | `5cfec198849eb1042f11dd2036b1e4df5956cba14c67aea595922f67d35fa1ad` |
| B2 | bolt-22.1.8-1.x86_64.rpm | `1d29742e257dfc083b5812caf7b67a3ec813d1cb280347d35e02c04d6b114c30` |
| B2 | bolt-debuginfo-22.1.8-1.x86_64.rpm | `8bade5dd00452403c2916db862cf011eea77dfc679d54c513fe0f46fdab3439c` |
| B2 | llvm-tools-subpkgs-debugsource-22.1.8-1.x86_64.rpm | `418421035b26d632097f8af8250b9c7e573463b4dffbc6e1187feef89367252c` |
| B1 | llvm-devel-22.1.8-1.x86_64.rpm | `df4e7759c247a1f9b4d8545befc3bd30ea5d8814b99b97f001c0921d353b3bfb` |

[完整路径与身份](../../tools/bolt/results/task152/rpm-identities.json)
