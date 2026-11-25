| PS5 项目 | 状态 | PS6 文件行和 diff 覆盖 |
|---|---|---|
| BOLT_LLVM_LINK_MODE 及 18 处使用 | 保留 | bolt/CMakeLists.txt:203–210 及独立的 18 处行号清单。diff 无 bolt/ hunk。 |
| LLVM_OPTIONAL_SOURCES | 保留 | bolt/lib/Target/X86/CMakeLists.txt:27–31。diff 无 bolt/ hunk。 |
| X86 镜像编译与定义条件 | 保留 | 同文件 27–31、46–49。diff 无 bolt/ hunk。 |
| runtime flags 只在 standalone 清空 | 保留 | bolt/CMakeLists.txt:156–163。diff 无 bolt/ hunk。 |
| merge-fdata 单次安装 | 保留 | bolt/tools/merge-fdata/CMakeLists.txt:1–12，standalone spec:146–170。diff 5–17 只改说明。 |
| ExclusiveArch | 保留 | standalone spec:12。diff 5–17 只改说明。 |
| 按架构的 BOLT_TARGETS_TO_BUILD 与注册检查 | 保留 | standalone spec:32–37、132、137–144。diff 5–17 只改说明。 |
| BuildRequires 版本绑定和 provider 一致性检查 | 保留 | standalone spec:15–29、105–115。diff 5–17 只改说明。 |
| bolt 的 Requires | 保留 | standalone spec:52–59 仍为 libllvm = %{version}，没有显式 compiler-rt 运行依赖。diff 5–17 只改说明。 |
| LLVM_LIBDIR_SUFFIX | 保留 | standalone spec:126，主 spec:476。对应 CMake 区块无 diff hunk。 |
| 发行版 LDFLAGS | 保留 | standalone spec:129–130。diff 5–17 只改说明。 |
| debuginfo/debugsource 注释 | 保留 | standalone spec:68–79。diff 5–17 只改说明。 |
| armv7l ARM;BPF | 保留 | 主 spec:425–429。对应 CMake 区块无 diff hunk。 |
| 删除 llvm 的显式 Requires: python3 | 保留 | 主 spec:58–64、108–116。diff 22–35 改 analyzer 注释及 Obsoletes，未新增此 Requires。 |
