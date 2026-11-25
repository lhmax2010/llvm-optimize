# 建议提交说明逐句核对

行号对应 [父提交至补丁 3 的完整 diff](base-to-patch3.diff)。补丁 4 保留给定正文原文。

| 句 | 正文摘要 | diff 行号 | 核对 |
|---|---|---|---|
| 1 | standalone spec 使用已安装 LLVM 构建 x86_64、aarch64 的 BOLT | 680–704、769–774、792–807 | PASS。ExclusiveArch、版本约束和 CMake 的独立源码入口都有对应。 |
| 2 | standalone 链接 libLLVM.so，in-tree 使用组件库，模式在消费者之前设置 | 31–46、51–665、769–774、802 | PASS。模式在 add_subdirectory 之前设置，组件链接标志传给各消费者。 |
| 3 | X86 镜像仅在 standalone dylib 下编译，其他模式标为可选，运行库 flags 仅在 standalone 清空 | 17–29、147–156、168–174 | PASS。两个镜像条件和 runtime 条件可分别核对。 |
| 4 | provider 版本和同一 release、按架构选 target 和注册、保留 LDFLAGS、从 _lib 派生后缀、单次安装 merge-fdata | 689–704、707–711、779–789、800、803–806、813–818、820–844 | PASS。安装段仅通过 ninja install 安装 merge-fdata，源码中该工具使用 add_bolt_tool。 |
| 5 | bolt 运行时依赖 libllvm = %{version} | 724–731 | PASS。 |
| 6 | clang 收编四个分析工具和配套 libexec 脚本 | 950–970 | PASS。该句描述打包归属。分析工具所需的 Python 模块和 share 文件的可用性见 152 号取证。 |
| 7 | llvm 和 clang 提供旧包名并废弃旧包 | 856–861、865–870 | 需限定 EVR。Provides 为精确 EVR，Obsoletes 严格小于当前 EVR。建议改法见下方，正文按用户原稿保留。 |
| 8 | EXE/SHARED linker flags 加 build-id，MODULE linker flags 保持原有设置 | 803–804、894–904 | PASS。主 spec 在 _toolchain 条件内，独立 spec 有对应的 EXE 和 SHARED 两行。 |

第 7 句建议改为 `The llvm and clang packages provide the former names and obsolete older releases of those packages.`
