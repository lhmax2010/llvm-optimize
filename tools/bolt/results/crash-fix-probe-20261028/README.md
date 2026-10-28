# 42号证据

- matrix.json / matrix/：3输入×5工具，完整argv、stdout/stderr、返回码。
- elf/、elf-structures.json、elf-containment.json：原始ELF检查；gnu-keep-warnings.txt为GNU生成debug时的完整warning。
- objcopy-gdb*：崩溃栈、反汇编、PT_PHDR与缓冲区现场。
- sources/：实际平台脚本、f308源码快照和带原始行号版本；上游RPM4.14文件另行标注。
- scheme-a-*、tu/：debuglink变化及15对象逐字节比较。
- chroot-*：临时根文件来源、LLDB自动加载/崩溃栈、proc挂卸载；失败探索原文保留。
- symbolizer-*、symbolization-summary.json：24地址显式/自动解析差异。
- timed-*、debug-sizes.json：分离时间/RSS及压缩估算。
- package-list-analysis.json、platform-log-anchors.txt：包归属静态证据和39日志原行号。
- relink-inventory.json、work-file-inventory.json：方案乙输入缺失依据。
- input-recheck.json、end-source-status.stdout：原输入不变、源码干净。
- scripts/：全部实验脚本（只在本次临时目录写入）。

完整二进制/独立chroot留在 W/temp/crash-fix-probe-20261028，不放Git。未构建RPM、未改发布代码、未推Gerrit。
