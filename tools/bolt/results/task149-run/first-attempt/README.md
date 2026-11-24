# 149-run 首次尝试

G4 的 CMake 配置完成，首次 PGO Ninja 检查在启动编译前拒绝 bin/llvm-min-tblgen 链接边中的两个相同 profile-use 参数。CMake HandleLLVMOptions 将该参数追加到通用 C/C++ flags 及 EXE/SHARED linker flags。局部修正只允许链接边上的两个相同、已校验的路径，仍拒绝编译边重复、不匹配的路径及运行库上的全部 profile 参数。不改变最终 PGO 构建参数或 profile 资产，仅修正局部验证器。N2 因 G4 初次失败短暂进入准备，顺序恢复前停下，关闭开关预检记录保留。

证据仓库首次暂存检查命中原始 GBS 日志末尾空白。修正为 Markdown 执行空白门禁，原始日志按字节归档。
