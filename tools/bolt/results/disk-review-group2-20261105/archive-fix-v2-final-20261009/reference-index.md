# 引用逐条索引：archive-fix-v2-final-20261009

本页逐条列工具脚本及55–63号文档引用。其他用途来源的完整命中在main-docs/bolt-docs-references-v3.txt.gz。路径命中不等于当前执行依赖；历史render/报告脚本仍按原文列出。

## main-scripts

无。

## bolt-scripts

- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/root-inventory-20261022/annotate.py:14`
  ```text
  put('archive-fix-v2-final-20261009','f111162e + v2','docs35 原始22RPM与证据','main/docs/38_llvm_strip_x86_64.md:27; bolt/docs/bolt/24_rebase_recertification.md:69','是，rpms-docs35','D24 payload-merged 可由其中22原件重建；先留此目录','保留','旧包已从 R/RPMS 移到此处，是来源原件','rpms-docs35 全部22RPM，不以抽出单个clang替代')
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/second-review-20261104/sandbox-direct-20261103/classify.py:24`
  ```text
  'archive-fix-v2-final-20261009':('建议保留','24、38','含 rpms-docs35 原始22包及来源记录，明确保留。'),
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/temp-cleanup-20261026/report.py:77`
  ```text
  restore={str(T/'toolchain-archivefix-v2-final'):'docs35原22RPM：T/archive-fix-v2-final-20261009/rpms-docs35；原件保留',str(T/'toolchain-llvm-strip'):'docs38的22RPM仍在gbs-root-x86_64-archivefix-v2/.../rpmbuild/RPMS/x86_64；不把它们说成67619ec8新构建',str(T/'toolchain-release-x86-20261013'):'docs49交接树/var/tmp/llvm-optimize-x86-archivefix-20261013/.../rpmbuild/RPMS/x86_64；该树仅删缓存，RPM保留',str(T/'bolt-v4-20261016-source-order/upper-parse'):'docs26解析实验已结束；upper-parse不是原始输入，报告/脚本/导出留在父目录；原下层保留','/var/tmp/llvm-optimize-archivefix-v2-final-20261009/independent-install':'docs35独立安装载荷；原RPM及外部验收报告保留；重跑需重建DESTDIR'}
  ```

## main-config

- `/home/linhao/Toolchain/development/llvm-optimize/tools/llvm_archive_fix_trial_fingerprint.json:119`
  ```text
      "patch_path": "/home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-v2-final-20261009/archive-native-conversion-v2.diff",
  ```
- `/home/linhao/Toolchain/development/llvm-optimize/tools/llvm_archive_fix_trial_fingerprint.json:129`
  ```text
      "resume_checkpoint": "/home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-v2-final-20261009/continue-20261009",
  ```
- `/home/linhao/Toolchain/development/llvm-optimize/tools/llvm_archive_fix_trial_fingerprint.json:131`
  ```text
      "result_evidence": "/home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-v2-final-20261009/continue-20261009/final-outcome.json",
  ```

## bolt-config

- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/llvm_archive_fix_trial_fingerprint.json:119`
  ```text
      "patch_path": "/home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-v2-final-20261009/archive-native-conversion-v2.diff",
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/llvm_archive_fix_trial_fingerprint.json:129`
  ```text
      "resume_checkpoint": "/home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-v2-final-20261009/continue-20261009",
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/llvm_archive_fix_trial_fingerprint.json:131`
  ```text
      "result_evidence": "/home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-v2-final-20261009/continue-20261009/final-outcome.json",
  ```

## recent-docs

无。
