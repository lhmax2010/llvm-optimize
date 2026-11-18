# 131 号 A：备份目录精确清理

**STOP。** 本次删除 0 项，释放 0 B。26 个 bundle 均已完成引用和提交图检查并保留。

备份目录为 `/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105`。结束时文件系统可用 147,880,558,592 B。

## 判定和停止记录

查询 GitHub 以及 Gerrit 的 LLVM、coreutils、findutils、which 的 heads、changes、tags。sandbox 包含在 Gerrit 的 heads 下。每个 bundle 用 list-heads 列出 refs，从先前已验证的解包对象库遍历图，并扣除查询时存在且本地可读的远端提交祖先。

远端引用缺少本地对象时保守处理。结果中的「未覆盖」表示由本次可用证据未证明可达。一般提交列表按 bundle 引用闭包生成。仓库内部对象文件保留，以维持恢复副本可用。

[远端引用及命令](../../tools/bolt/results/task131/backup-remotes.json)。[逐 bundle 引用、提交清单路径、大小和 SHA256](../../tools/bolt/results/task131/backup-bundles.json)。[未证明可达的全部提交与所属仓库](../../tools/bolt/results/task131/backup-unproven.json)。

首次删除尝试遇到 root 属主的只读目录，错误原文如下。

~~~text
PermissionError: [Errno 13] Permission denied: '/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/10-archive-followup-review-20261014/apply-check-5b6fd066/repository.bundle'
~~~

一次修正后，程序跳过不能写入的目录，在第一项可写候选的哈希读取后触发完整 stat 比较断言。未进行第二次修正，以下为错误原文及断言。

~~~text
  File "<stdin>", line 68, in <module>
AssertionError
assert p.stat()==st
~~~

非 bundle 文件共 945 项，其中 69 项的 blob 在核对过的 GitHub 引用中有相同内容。未进行删除。[逐文件保留清单](../../tools/bolt/results/task131/backup-other-files.json)。

## Bundle 清单

路径相对于备份目录。原仓库的完整绝对路径见逐 bundle 数据。

| Bundle 路径 | 字节 | 提交数 | 未覆盖 | 依据及结果 |
|---|---:|---:|---:|---|
| `00-source/root-5645c783/repository.bundle` | 1,481 | 5 | 5 | 保留。有未证明可达的提交 |
| `00-source/root-759fbb28/repository.bundle` | 1,486 | 5 | 5 | 保留。有未证明可达的提交 |
| `00-source/root-e27851fd/repository.bundle` | 1,484 | 5 | 5 | 保留。有未证明可达的提交 |
| `04-pgo-resource-20261102/source-D-aa70a0e3/repository.bundle` | 4,289,677,077 | 842,234 | 2 | 保留。有未证明可达的提交 |
| `05-review-round3-continue-20261012/patch-apply-check-c54a3707/repository.bundle` | 4,280,031,786 | 842,232 | 0 | 保留。全部提交由远端引用覆盖 |
| `05-review-round3-continue-20261012/patch-work-617ca250/repository.bundle` | 4,280,035,822 | 842,234 | 2 | 保留。有未证明可达的提交 |
| `09-archive-fix-full-build-20260927/test-package-bfd-4a09ebac/repository.bundle` | 3,899 | 1 | 1 | 保留。有未证明可达的提交 |
| `09-archive-fix-full-build-20260927/test-package-lld-6ad747a2/repository.bundle` | 3,882 | 1 | 1 | 保留。有未证明可达的提交 |
| `10-archive-followup-review-20261014/apply-check-5b6fd066/repository.bundle` | 4,280,030,032 | 842,231 | 0 | 保留。全部提交由远端引用覆盖 |
| `10-archive-followup-review-20261014/submit-work-4512d286/repository.bundle` | 4,280,033,559 | 842,232 | 0 | 保留。全部提交由远端引用覆盖 |
| `18-release-x86-full-build-20261013/latest-base_source-ae3cb8ab/repository.bundle` | 4,280,032,979 | 842,232 | 2 | 保留。有未证明可达的提交 |
| `18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-bfd-1b27e3f6/repository.bundle` | 6,118 | 2 | 2 | 保留。有未证明可达的提交 |
| `18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-lld-40f1e6ad/repository.bundle` | 6,118 | 2 | 2 | 保留。有未证明可达的提交 |
| `19-release-attribution-20261013/patch-apply-check-6105a95d/repository.bundle` | 4,280,031,786 | 842,232 | 0 | 保留。全部提交由远端引用覆盖，且与另一 bundle 的 SHA256 相同 |
| `19-release-attribution-20261013/patch-work-45589d5e/repository.bundle` | 4,280,036,788 | 842,234 | 2 | 保留。有未证明可达的提交 |
| `24-llvm-strip-alternative-20260929/test-package-bfd-03f3e641/repository.bundle` | 4,527 | 1 | 1 | 保留。有未证明可达的提交 |
| `24-llvm-strip-alternative-20260929/test-package-lld-c8f02f6f/repository.bundle` | 4,518 | 1 | 1 | 保留。有未证明可达的提交 |
| `25-llvm-strip-x86_64-20261009/continue-20261009_test-package-bfd-2ca8bd4a/repository.bundle` | 5,821 | 1 | 1 | 保留。有未证明可达的提交 |
| `25-llvm-strip-x86_64-20261009/continue-20261009_test-package-lld-81b277b8/repository.bundle` | 5,815 | 1 | 1 | 保留。有未证明可达的提交 |
| `29-llvm-hybrid-trial/root-8885f3e3/repository.bundle` | 4,434,084,908 | 994,621 | 0 | 保留。全部提交由远端引用覆盖 |
| `30-llvm-archivefix-trial/root-fd4d3568/repository.bundle` | 4,434,084,904 | 994,621 | 0 | 保留。全部提交由远端引用覆盖 |
| `32-followup-356949-ps2-message-20261014/review-work-c226bed9/repository.bundle` | 4,280,033,075 | 842,231 | 0 | 保留。全部提交由远端引用覆盖 |
| `36-qb_analysis/work3_control_findutils-5ecf1d1e/repository.bundle` | 34,528,535 | 33 | 33 | 保留。有未证明可达的提交 |
| `36-qb_analysis/work3_control_which-3a31a668/repository.bundle` | 161,911 | 13 | 13 | 保留。有未证明可达的提交 |
| `36-qb_analysis/work3_coreutils-38da01e5/repository.bundle` | 7,095,491 | 50 | 50 | 保留。有未证明可达的提交 |
| `36-qb_analysis/work3_findutils-01add93a/repository.bundle` | 34,528,541 | 33 | 33 | 保留。有未证明可达的提交 |

[重复 bundle 的两条路径与 SHA256](../../tools/bolt/results/task131/backup-duplicates.json)。[删除结果及空间](../../tools/bolt/results/task131/backup-space.json)。
