# 提交说明逐句核对

补丁 7 只新增精确路径的 shebang 修正。移除这些新增行和分隔空行后，相对 f346dd75 的产品增删逐字节等于 154 的补丁 6 证据。下表前 8 项沿用已核实的 [补丁 6 diff](../../task154/parent-to-p6.diff) 行号，第 9 项列出 [补丁 7 完整 diff](parent-to-p7.diff) 的新增行。

| 核对 | 主张 | diff 行 | 结论 |
|---|---|---|---|
| 1 | standalone BOLT 使用已安装 LLVM，在 x86_64 和 aarch64 构建 | 686–704、769–774、792–807 | PASS。架构、provider 与独立 CMake 入口对应。 |
| 2 | standalone 链接 libLLVM.so，in-tree 链接组件库，模式在消费者之前定义 | 35–42、53–665、772–774、802 | PASS。 |
| 3 | 仅 standalone dylib 编译 X86 镜像，其他模式列为可选，runtime flags 仅 standalone 清空 | 22–27、148–155、168–173 | PASS。 |
| 4 | 固定 provider version 并检查 version-release，按架构配置及校验目标，保留 LDFLAGS，从 _lib 派生后缀，merge-fdata 安装一次 | 689–711、779–789、800、803–818、820–844、617–629 | PASS。 |
| 5 | bolt Requires libllvm = %{version} | 724–731 | PASS。 |
| 6 | clang 收录四个入口、libexec、报告资源和 Python 模块，llvm 收录 scan-view 及其数据 | 928–933、950–980、984–995 | PASS。目录与入口路径另有 CMake 和旧构建日志印证。此句描述计划的包内容。 |
| 7 | llvm 与 clang 提供原包名并废弃较旧版本 | 855–861、865–870 | PASS。严格小于完整 EVR，覆盖同版本但 release 更低的旧包。 |
| 8 | EXE 和 SHARED linker flags 加 build-id，MODULE 保留原有设置 | 803–804、894–904 | PASS。主 spec 的增量位于 _toolchain 条件下。 |
| 9 | Scripts that used an unversioned Python interpreter now use Python 3 shebangs. | 941, 942, 943, 944, 945, 946 | PASS。每条恰好对应 RPM 里扫到的一个文件。 |
