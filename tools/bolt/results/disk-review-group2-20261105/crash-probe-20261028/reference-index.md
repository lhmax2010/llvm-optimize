# 引用逐条索引：crash-probe-20261028

本页逐条列工具脚本及55–63号文档引用。其他用途来源的完整命中在main-docs/bolt-docs-references-v3.txt.gz。路径命中不等于当前执行依赖；历史render/报告脚本仍按原文列出。

## main-scripts

无。

## bolt-scripts

- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/crash-fix-probe-20261028/scripts/scheme_a.py:19`
  ```text
  addresses=json.loads((B/'tools/bolt/results/crash-probe-20261028/offline-addresses-corrected.json').read_text());save('offline-addresses.json',addresses)
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/crash-probe-20261028/probe.py:4`
  ```text
  D=Path(__file__).resolve().parent; E=B/'tools/bolt/results/crash-probe-20261028';E.mkdir(parents=True,exist_ok=True)
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/crash-probe-20261028/report.py:5`
  ```text
  prefix='../../tools/bolt/results/crash-probe-20261028/'
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/crash-probe-20261028/report.py:14`
  ```text
  源码f308fe08、39号products和构建根只读。最终clang从本轮clang RPM流式解出，SHA为8c2429d870f421a29a9914458bc4d4ff2ce359a15e0bdd20f39bfb4580c40bdf；ordinary SHA d5090159915657b235b96f1202c058e1efd1647d6a2225ac8fdb2906aeaa501d；strip前BOLT输出SHA与identity.before_sha256核对一致。所有写入仅在W/temp/crash-probe-20261028及本报告证据目录。
  ```

## main-config

无。

## bolt-config

无。

## recent-docs

无。
