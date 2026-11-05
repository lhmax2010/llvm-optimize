# 引用逐条索引：crash-fix-probe-20261028

本页逐条列工具脚本及55–63号文档引用。其他用途来源的完整命中在main-docs/bolt-docs-references-v3.txt.gz。路径命中不等于当前执行依赖；历史render/报告脚本仍按原文列出。

## main-scripts

无。

## bolt-scripts

- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/second-review-20261104/sandbox-direct-20261103/classify.py:16`
  ```text
  'crash-fix-probe-20261028':('建议保留','42','objcopy 缺陷、符号文件与 LLDB 实测临时产物；源码行方案/缺陷仍挂账，副本唯一性未认证。'),
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/crash-fix-probe-20261028/scripts/scheme_a.py:19`
  ```text
  addresses=json.loads((B/'tools/bolt/results/crash-probe-20261028/offline-addresses-corrected.json').read_text());save('offline-addresses.json',addresses)
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/crash-fix-probe-20261028/scripts/report.py:3`
  ```text
  rel='../../tools/bolt/results/crash-fix-probe-20261028/'
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/crash-fix-probe-20261028/scripts/report.py:19`
  ```text
  - 所有实验副本在 `temp/crash-fix-probe-20261028/`；已有根和 products 未改写。源码工作树末次 `git status --porcelain` 为空。{link('input-recheck.json')} 证明三份输入 SHA 前后相同。
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/crash-fix-probe-20261028/scripts/report.py:145`
  ```text
  旧根中没有已安装的gdb/普通lldb CLI；`lldb-instr`实际上是仪器化工具，不是调试器。因此复制**本轮已构建、无需重建的Tizen lldb/lldb-server**及所需运行库到新建`temp/crash-fix-probe-20261028/scratch.debug-probe`。clang放`/usr/bin/clang-22`，debug放标准`/usr/lib/debug/usr/bin/clang-22.debug`，没有手工`target symbols add`。
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/crash-fix-probe-20261028/scripts/report.py:221`
  ```text
  (E/'README.md').write_text('''# 42号证据\n\n- matrix.json / matrix/：3输入×5工具，完整argv、stdout/stderr、返回码。\n- elf/、elf-structures.json、elf-containment.json：原始ELF检查；gnu-keep-warnings.txt为GNU生成debug时的完整warning。\n- objcopy-gdb*：崩溃栈、反汇编、PT_PHDR与缓冲区现场。\n- sources/：实际平台脚本、f308源码快照和带原始行号版本；上游RPM4.14文件另行标注。\n- scheme-a-*、tu/：debuglink变化及15对象逐字节比较。\n- chroot-*：临时根文件来源、LLDB自动加载/崩溃栈、proc挂卸载；失败探索原文保留。\n- symbolizer-*、symbolization-summary.json：24地址显式/自动解析差异。\n- timed-*、debug-sizes.json：分离时间/RSS及压缩估算。\n- package-list-analysis.json、platform-log-anchors.txt：包归属静态证据和39日志原行号。\n- relink-inventory.json、work-file-inventory.json：方案乙输入缺失依据。\n- input-recheck.json、end-source-status.stdout：原输入不变、源码干净。\n- scripts/：全部实验脚本（只在本次临时目录写入）。\n\n完整二进制/独立chroot留在 W/temp/crash-fix-probe-20261028，不放Git。未构建RPM、未改发布代码、未推Gerrit。\n''')
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/crash-fix-probe-20261028/scripts/common.py:3`
  ```text
  W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=Path(__file__).resolve().parent;E=B/'tools/bolt/results/crash-fix-probe-20261028';E.mkdir(parents=True,exist_ok=True)
  ```

## main-config

无。

## bolt-config

无。

## recent-docs

无。
