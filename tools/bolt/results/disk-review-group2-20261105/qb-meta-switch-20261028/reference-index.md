# 引用逐条索引：qb-meta-switch-20261028

本页逐条列工具脚本及55–63号文档引用。其他用途来源的完整命中在main-docs/bolt-docs-references-v3.txt.gz。路径命中不等于当前执行依赖；历史render/报告脚本仍按原文列出。

## main-scripts

无。

## bolt-scripts

- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028/scripts/qb_read.py:3`
  ```text
  W=Path('/home/linhao/Toolchain/development/llvm-optimize');E=W.parent/'llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028';D=Path(__file__).resolve().parent
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028/scripts/unified_checks.py:3`
  ```text
  W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=Path(__file__).resolve().parent;E=B/'tools/bolt/results/qb-meta-switch-20261028';M=E/'metadata'
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028/scripts/start.py:3`
  ```text
  W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=Path(__file__).resolve().parent;E=B/'tools/bolt/results/qb-meta-switch-20261028';R=W/'temp/qb-meta-20261028/repo'
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028/scripts/mlgo.py:3`
  ```text
  W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=Path(__file__).resolve().parent;E=B/'tools/bolt/results/qb-meta-switch-20261028';out=E/'mlgo';out.mkdir(exist_ok=True)
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028/scripts/base_checks.py:3`
  ```text
  W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';E=B/'tools/bolt/results/qb-meta-switch-20261028';P=B/'tools/bolt/results/qb-fail-20261028/meta/buildconf';D=Path(__file__).resolve().parent
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028/scripts/qb_logs.py:3`
  ```text
  W=Path('/home/linhao/Toolchain/development/llvm-optimize');E=W.parent/'llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028';D=Path(__file__).resolve().parent
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028/scripts/report.py:3`
  ```text
  W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=Path(__file__).resolve().parent;E=B/'tools/bolt/results/qb-meta-switch-20261028';P=B/'tools/bolt/results/qb-fail-20261028/meta/buildconf';R=W/'temp/qb-meta-20261028/repo'
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028/scripts/report.py:4`
  ```text
  base=json.loads((E/'base-missing-dependencies.json').read_text());unified=json.loads((E/'unified-missing-dependencies.json').read_text());source=json.loads((E/'unified-fixed-source-comparison.json').read_text());cfg=json.loads((E/'base-config-providers.json').read_text());tests=json.loads((E/'mlgo/tests.json').read_text());prefix='../../tools/bolt/results/qb-meta-switch-20261028/'
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028/scripts/final_data.py:3`
  ```text
  W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';E=B/'tools/bolt/results/qb-meta-switch-20261028';D=Path(__file__).resolve().parent;R=W/'temp/qb-meta-20261028/repo'
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028/scripts/repos.py:3`
  ```text
  W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=Path(__file__).resolve().parent;E=B/'tools/bolt/results/qb-meta-switch-20261028';F=B/'tools/bolt/results/qb-meta-fix-and-snapshot-20261028/snapshots'
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028/scripts/finish.py:3`
  ```text
  W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=Path(__file__).resolve().parent;E=B/'tools/bolt/results/qb-meta-switch-20261028';R=W/'temp/qb-meta-20261028/repo';(E/'scripts').mkdir(exist_ok=True)
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028/second-ruling/second_audit.py:3`
  ```text
  W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';E=B/'tools/bolt/results/qb-meta-switch-20261028';D=E/'second-ruling';R=W/'temp/qb-meta-20261028/repo'
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028/second-ruling/finalize_closure.py:3`
  ```text
  W=Path('/home/linhao/Toolchain/development/llvm-optimize');E=W.parent/'llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028';D=E/'second-ruling'
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028/second-ruling/submit_unified.py:3`
  ```text
  W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';E=B/'tools/bolt/results/qb-meta-switch-20261028';D=E/'second-ruling';R=W/'temp/qb-meta-20261028/repo'
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028/second-ruling/unified_specs.py:3`
  ```text
  W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=W/'temp/qb-meta-switch-20261028/second-specs';E=B/'tools/bolt/results/qb-meta-switch-20261028/second-ruling';D.mkdir(exist_ok=True)
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028/second-ruling/base_provider_current.py:3`
  ```text
  E=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028/second-ruling');D=E/'base-current';D.mkdir(exist_ok=True)
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028/second-ruling/scan_unified_specs.py:3`
  ```text
  W=Path('/home/linhao/Toolchain/development/llvm-optimize');E=W.parent/'llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028';D=E/'second-ruling'
  ```

## main-config

无。

## bolt-config

无。

## recent-docs

无。
