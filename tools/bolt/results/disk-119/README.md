# 119 清理证据

本次扫描/分类替代118错误的容器继承分类，不依赖97/118 inventory。scan119.py归档本次内联扫描的只读核心；未为交付重复运行。classification的完整输入为本目录本次inventory-raw、protection-rules、report-matches、candidate-git-checks，输出为inventory-classified和delete-plan。不能只按目录名执行delete-plan：实际删除前再次逐项检查，结果以delete-results为准。

- deleted.md：实际删除的241个精确路径。
- skipped.md：9项删除前跳过，保留原文。
- listings/：删除前清单（检查失败时可能只有部分清单，不能视为完整）。
- backup-NNN.json：复制保全的来源、目标、SHA或链接。
- postcheck.json：删除后路径、备份大小/链接、保护目录检查与df。
- backup-summary.md / backup-bundle-summary.json：源码保护备份的分支与提交概要。
- worktree-commit-reachability.json：保守的已验证远端锚点覆盖检查；未覆盖不等同于从未发布。

所有删除命令的完整argv、退出码、前后df在delete-results.jsonl。无源码工作树删除、无worktree prune、无LLVM推送。只读控制面检查过自身service和PID702460的fd/文件大小，用于解释较慢RPM保全；未检查其他项目。
