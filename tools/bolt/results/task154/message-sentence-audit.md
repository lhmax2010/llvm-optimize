# 新提交说明逐句核对

行号对应 [父提交 f346dd75 至补丁 6 的完整 diff](parent-to-p6.diff)。

| 句 | 主张 | diff 行 | 结论 |
|---|---|---|---|
| 1 | standalone BOLT 使用已安装 LLVM，在 x86_64 和 aarch64 构建 | 686–704、769–774、792–807 | PASS。架构、provider 与独立 CMake 入口对应。 |
| 2 | standalone 链接 libLLVM.so，in-tree 链接组件库，模式在消费者之前定义 | 35–42、53–665、772–774、802 | PASS。 |
| 3 | 仅 standalone dylib 编译 X86 镜像，其他模式列为可选，runtime flags 仅 standalone 清空 | 22–27、148–155、168–173 | PASS。 |
| 4 | 固定 provider version 并检查 version-release，按架构配置及校验目标，保留 LDFLAGS，从 _lib 派生后缀，merge-fdata 安装一次 | 689–711、779–789、800、803–818、820–844、617–629 | PASS。 |
| 5 | bolt Requires libllvm = %{version} | 724–731 | PASS。 |
| 6 | clang 收录四个入口、libexec、报告资源和 Python 模块，llvm 收录 scan-view 及其数据 | 928–933、950–980、984–995 | PASS。目录与入口路径另有 CMake 和旧构建日志印证。此句描述计划的包内容。 |
| 7 | llvm 与 clang 提供原包名并废弃较旧版本 | 855–861、865–870 | PASS。严格小于完整 EVR，覆盖同版本但 release 更低的旧包。 |
| 8 | EXE 和 SHARED linker flags 加 build-id，MODULE 保留原有设置 | 803–804、894–904 | PASS。主 spec 的增量位于 _toolchain 条件下。 |

三段沿用 153 原文。第三段按任务文本逐字保留。新增正文最长 70 列，纯 ASCII，禁用词零命中。原标题、9 条历史和 trailer 逐字节保留。
