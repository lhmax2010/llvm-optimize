# 137 号：sudo-delete.sh 执行前复核

**UNSAFE。** 复核 239 条删除路径。保留清单命中 0 条，项目单元命中 0 条，挂载命中 0 条，进程路径命中 0 条，路径身份异常 0 条。非内核线程的进程读取盲区覆盖 56 个 PID。

- 采样 2026-11-18T06:13:23-08:00 至 2026-11-18T06:13:24-08:00。/home 可用 **185,010,585,600 B（172.30 GiB）**，按普通用户可用块统计。
- 脚本 SHA256 `d6569d76909fdbbef97b3615cb967aba2f41f360e4c18e35d358a526c5e9b4c1` 与批准值一致。将 239 条 `rm` 目标与脚本里的身份校验项和挂载校验项逐一对齐。只解析脚本，检查过程未执行脚本。
- 本地保留清单与 135 号证据仓库副本逐字节相同，SHA256 `d2360c073b4b41c2b964f3840510a41fe8bae975d8c7761d9ffdddab5b9b6365`。比较 116 条记录的原路径、清单记录的解析路径和现场 realpath，按目录边界双向比对。[135 号保留清单](../../tools/bolt/results/workspace-cleanup-135/retention.json)
- 从 `/proc/self/mountinfo` 前后分别读取 63、63 个挂载记录，解码八进制路径转义后匹配。结果的挂载范围为采样服务所在的挂载命名空间。
- 枚举 `/proc` 中 454 个 PID，成功读取 145 个 cwd、145 个 root 和 4224 个 fd 链接。0 个 PID 在读取期间退出。记录指向删除路径的边界匹配，包含带 ` (deleted)` 后缀的打开文件。
- 检查前后两次用用户及系统 systemd 查询活动单元的工作路径、启动参数和 cgroup，与可见进程交叉核对；项目相关单元 0 个。133-N 的活动记录为 0 条。该项报告本次观察窗口的用量。
- 使用用户服务执行，MemoryMax=2GiB、Nice=19、IOSchedulingClass=idle。未使用 sudo。

## U1：进程可见性不足

本次权限无法核实 56 个非内核线程 PID 的全部 cwd、root 或 fd，其中当前用户的 PID 有 13 个。内核线程单独计数；仅内核线程出现读取失败的有 253 个。正在运行的进程可改变打开文件；读权限盲区无法按目标路径排除，因此每条无进程命中的路径仍记为「未证实（U1）」。

- `/proc/1/cwd errno=EACCES`
- `/proc/1/root errno=EACCES`
- `/proc/1/fd_directory errno=EACCES`
- `/proc/2/cwd errno=EACCES`
- `/proc/2/root errno=EACCES`
- `/proc/2/fd_directory errno=EACCES`
- `/proc/3/cwd errno=EACCES`
- `/proc/3/root errno=EACCES`

## 逐条结果

表中目标路径相对于 `/home/linhao/Toolchain/development/llvm-optimize/temp`。脚本行号为对应 `rm` 的位置。「无」表示在该列给定范围内没有发现命中。

| 脚本行 | 相对目标路径 | 保留清单 | 活动单元 | 挂载点 | cwd/root/fd | 路径身份 |
|---:|---|---|---|---|---|---|
| 760 | `debuglink-20261028` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 762 | `gbs-root-x86_64-archivefix-v2` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 764 | `gbs-root-x86_64-debuginfo-j4-v2` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 766 | `night-20261105/rehearsal/toolchain/gbs-root` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 768 | `night-20261105/rehearsal/toolchain/retry-02/gbs-root` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 770 | `qb-install-20261105` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 772 | `rebase-359934-20261106-r2` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 774 | `deleted-repo-backup-20261105/04-pgo-resource-20261102/source-D-aa70a0e3/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 776 | `deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-apply-check-c54a3707/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 778 | `deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-work-617ca250/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 780 | `deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-bfd-4a09ebac/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 782 | `deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-lld-6ad747a2/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 784 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/apply-check-5b6fd066/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 786 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/submit-work-4512d286/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 788 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/latest-base_source-ae3cb8ab/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 790 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-bfd-1b27e3f6/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 792 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-lld-40f1e6ad/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 794 | `deleted-repo-backup-20261105/19-release-attribution-20261013/patch-apply-check-6105a95d/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 796 | `deleted-repo-backup-20261105/19-release-attribution-20261013/patch-work-45589d5e/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 798 | `deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-bfd-03f3e641/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 800 | `deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-lld-c8f02f6f/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 802 | `deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-bfd-2ca8bd4a/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 804 | `deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-lld-81b277b8/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 806 | `deleted-repo-backup-20261105/29-llvm-hybrid-trial/root-8885f3e3/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 808 | `deleted-repo-backup-20261105/30-llvm-archivefix-trial/root-fd4d3568/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 810 | `deleted-repo-backup-20261105/32-followup-356949-ps2-message-20261014/review-work-c226bed9/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 812 | `deleted-repo-backup-20261105/36-qb_analysis/work3_control_findutils-5ecf1d1e/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 814 | `deleted-repo-backup-20261105/36-qb_analysis/work3_control_which-3a31a668/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 816 | `deleted-repo-backup-20261105/36-qb_analysis/work3_findutils-01add93a/repository.bundle` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 818 | `deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-apply-check-c54a3707/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 820 | `deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-apply-check-c54a3707/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 822 | `deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-apply-check-c54a3707/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 824 | `deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-apply-check-c54a3707/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 826 | `deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-apply-check-c54a3707/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 828 | `deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-apply-check-c54a3707/index.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 830 | `deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-apply-check-c54a3707/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 832 | `deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-apply-check-c54a3707/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 834 | `deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-apply-check-c54a3707/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 836 | `deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-work-617ca250/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 838 | `deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-work-617ca250/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 840 | `deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-work-617ca250/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 842 | `deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-work-617ca250/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 844 | `deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-work-617ca250/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 846 | `deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-work-617ca250/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 848 | `deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-work-617ca250/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 850 | `deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-work-617ca250/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 852 | `deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-work-617ca250/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 854 | `deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-bfd-03f3e641/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 856 | `deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-bfd-03f3e641/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 858 | `deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-bfd-03f3e641/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 860 | `deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-bfd-03f3e641/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 862 | `deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-bfd-03f3e641/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 864 | `deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-bfd-03f3e641/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 866 | `deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-bfd-03f3e641/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 868 | `deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-bfd-03f3e641/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 870 | `deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-bfd-03f3e641/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 872 | `deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-lld-c8f02f6f/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 874 | `deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-lld-c8f02f6f/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 876 | `deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-lld-c8f02f6f/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 878 | `deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-lld-c8f02f6f/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 880 | `deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-lld-c8f02f6f/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 882 | `deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-lld-c8f02f6f/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 884 | `deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-lld-c8f02f6f/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 886 | `deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-lld-c8f02f6f/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 888 | `deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-lld-c8f02f6f/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 890 | `deleted-repo-backup-20261105/29-llvm-hybrid-trial/root-8885f3e3/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 892 | `deleted-repo-backup-20261105/29-llvm-hybrid-trial/root-8885f3e3/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 894 | `deleted-repo-backup-20261105/29-llvm-hybrid-trial/root-8885f3e3/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 896 | `deleted-repo-backup-20261105/29-llvm-hybrid-trial/root-8885f3e3/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 898 | `deleted-repo-backup-20261105/29-llvm-hybrid-trial/root-8885f3e3/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 900 | `deleted-repo-backup-20261105/29-llvm-hybrid-trial/root-8885f3e3/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 902 | `deleted-repo-backup-20261105/29-llvm-hybrid-trial/root-8885f3e3/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 904 | `deleted-repo-backup-20261105/29-llvm-hybrid-trial/root-8885f3e3/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 906 | `deleted-repo-backup-20261105/29-llvm-hybrid-trial/root-8885f3e3/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 908 | `deleted-repo-backup-20261105/29-llvm-hybrid-trial/root-8885f3e3/worktree.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 910 | `deleted-repo-backup-20261105/19-release-attribution-20261013/patch-apply-check-6105a95d/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 912 | `deleted-repo-backup-20261105/19-release-attribution-20261013/patch-apply-check-6105a95d/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 914 | `deleted-repo-backup-20261105/19-release-attribution-20261013/patch-apply-check-6105a95d/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 916 | `deleted-repo-backup-20261105/19-release-attribution-20261013/patch-apply-check-6105a95d/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 918 | `deleted-repo-backup-20261105/19-release-attribution-20261013/patch-apply-check-6105a95d/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 920 | `deleted-repo-backup-20261105/19-release-attribution-20261013/patch-apply-check-6105a95d/index.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 922 | `deleted-repo-backup-20261105/19-release-attribution-20261013/patch-apply-check-6105a95d/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 924 | `deleted-repo-backup-20261105/19-release-attribution-20261013/patch-apply-check-6105a95d/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 926 | `deleted-repo-backup-20261105/19-release-attribution-20261013/patch-apply-check-6105a95d/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 928 | `deleted-repo-backup-20261105/19-release-attribution-20261013/patch-work-45589d5e/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 930 | `deleted-repo-backup-20261105/19-release-attribution-20261013/patch-work-45589d5e/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 932 | `deleted-repo-backup-20261105/19-release-attribution-20261013/patch-work-45589d5e/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 934 | `deleted-repo-backup-20261105/19-release-attribution-20261013/patch-work-45589d5e/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 936 | `deleted-repo-backup-20261105/19-release-attribution-20261013/patch-work-45589d5e/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 938 | `deleted-repo-backup-20261105/19-release-attribution-20261013/patch-work-45589d5e/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 940 | `deleted-repo-backup-20261105/19-release-attribution-20261013/patch-work-45589d5e/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 942 | `deleted-repo-backup-20261105/19-release-attribution-20261013/patch-work-45589d5e/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 944 | `deleted-repo-backup-20261105/19-release-attribution-20261013/patch-work-45589d5e/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 946 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/submit-work-4512d286/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 948 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/submit-work-4512d286/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 950 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/submit-work-4512d286/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 952 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/submit-work-4512d286/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 954 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/submit-work-4512d286/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 956 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/submit-work-4512d286/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 958 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/submit-work-4512d286/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 960 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/submit-work-4512d286/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 962 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/submit-work-4512d286/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 964 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/apply-check-5b6fd066/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 966 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/apply-check-5b6fd066/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 968 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/apply-check-5b6fd066/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 970 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/apply-check-5b6fd066/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 972 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/apply-check-5b6fd066/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 974 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/apply-check-5b6fd066/index.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 976 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/apply-check-5b6fd066/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 978 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/apply-check-5b6fd066/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 980 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/apply-check-5b6fd066/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 982 | `deleted-repo-backup-20261105/10-archive-followup-review-20261014/apply-check-5b6fd066/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 984 | `deleted-repo-backup-20261105/32-followup-356949-ps2-message-20261014/review-work-c226bed9/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 986 | `deleted-repo-backup-20261105/32-followup-356949-ps2-message-20261014/review-work-c226bed9/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 988 | `deleted-repo-backup-20261105/32-followup-356949-ps2-message-20261014/review-work-c226bed9/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 990 | `deleted-repo-backup-20261105/32-followup-356949-ps2-message-20261014/review-work-c226bed9/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 992 | `deleted-repo-backup-20261105/32-followup-356949-ps2-message-20261014/review-work-c226bed9/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 994 | `deleted-repo-backup-20261105/32-followup-356949-ps2-message-20261014/review-work-c226bed9/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 996 | `deleted-repo-backup-20261105/32-followup-356949-ps2-message-20261014/review-work-c226bed9/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 998 | `deleted-repo-backup-20261105/32-followup-356949-ps2-message-20261014/review-work-c226bed9/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1000 | `deleted-repo-backup-20261105/32-followup-356949-ps2-message-20261014/review-work-c226bed9/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1002 | `deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-bfd-2ca8bd4a/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1004 | `deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-bfd-2ca8bd4a/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1006 | `deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-bfd-2ca8bd4a/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1008 | `deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-bfd-2ca8bd4a/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1010 | `deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-bfd-2ca8bd4a/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1012 | `deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-bfd-2ca8bd4a/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1014 | `deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-bfd-2ca8bd4a/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1016 | `deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-bfd-2ca8bd4a/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1018 | `deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-bfd-2ca8bd4a/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1020 | `deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-lld-81b277b8/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1022 | `deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-lld-81b277b8/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1024 | `deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-lld-81b277b8/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1026 | `deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-lld-81b277b8/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1028 | `deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-lld-81b277b8/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1030 | `deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-lld-81b277b8/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1032 | `deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-lld-81b277b8/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1034 | `deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-lld-81b277b8/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1036 | `deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-lld-81b277b8/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1038 | `deleted-repo-backup-20261105/04-pgo-resource-20261102/source-D-aa70a0e3/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1040 | `deleted-repo-backup-20261105/04-pgo-resource-20261102/source-D-aa70a0e3/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1042 | `deleted-repo-backup-20261105/04-pgo-resource-20261102/source-D-aa70a0e3/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1044 | `deleted-repo-backup-20261105/04-pgo-resource-20261102/source-D-aa70a0e3/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1046 | `deleted-repo-backup-20261105/04-pgo-resource-20261102/source-D-aa70a0e3/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1048 | `deleted-repo-backup-20261105/04-pgo-resource-20261102/source-D-aa70a0e3/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1050 | `deleted-repo-backup-20261105/04-pgo-resource-20261102/source-D-aa70a0e3/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1052 | `deleted-repo-backup-20261105/04-pgo-resource-20261102/source-D-aa70a0e3/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1054 | `deleted-repo-backup-20261105/04-pgo-resource-20261102/source-D-aa70a0e3/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1056 | `deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-lld-6ad747a2/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1058 | `deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-lld-6ad747a2/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1060 | `deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-lld-6ad747a2/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1062 | `deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-lld-6ad747a2/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1064 | `deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-lld-6ad747a2/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1066 | `deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-lld-6ad747a2/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1068 | `deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-lld-6ad747a2/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1070 | `deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-lld-6ad747a2/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1072 | `deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-lld-6ad747a2/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1074 | `deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-bfd-4a09ebac/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1076 | `deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-bfd-4a09ebac/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1078 | `deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-bfd-4a09ebac/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1080 | `deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-bfd-4a09ebac/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1082 | `deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-bfd-4a09ebac/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1084 | `deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-bfd-4a09ebac/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1086 | `deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-bfd-4a09ebac/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1088 | `deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-bfd-4a09ebac/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1090 | `deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-bfd-4a09ebac/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1092 | `deleted-repo-backup-20261105/36-qb_analysis/work3_control_findutils-5ecf1d1e/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1094 | `deleted-repo-backup-20261105/36-qb_analysis/work3_control_findutils-5ecf1d1e/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1096 | `deleted-repo-backup-20261105/36-qb_analysis/work3_control_findutils-5ecf1d1e/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1098 | `deleted-repo-backup-20261105/36-qb_analysis/work3_control_findutils-5ecf1d1e/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1100 | `deleted-repo-backup-20261105/36-qb_analysis/work3_control_findutils-5ecf1d1e/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1102 | `deleted-repo-backup-20261105/36-qb_analysis/work3_control_findutils-5ecf1d1e/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1104 | `deleted-repo-backup-20261105/36-qb_analysis/work3_control_findutils-5ecf1d1e/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1106 | `deleted-repo-backup-20261105/36-qb_analysis/work3_control_findutils-5ecf1d1e/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1108 | `deleted-repo-backup-20261105/36-qb_analysis/work3_control_findutils-5ecf1d1e/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1110 | `deleted-repo-backup-20261105/36-qb_analysis/work3_coreutils-38da01e5/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1112 | `deleted-repo-backup-20261105/36-qb_analysis/work3_coreutils-38da01e5/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1114 | `deleted-repo-backup-20261105/36-qb_analysis/work3_coreutils-38da01e5/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1116 | `deleted-repo-backup-20261105/36-qb_analysis/work3_coreutils-38da01e5/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1118 | `deleted-repo-backup-20261105/36-qb_analysis/work3_coreutils-38da01e5/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1120 | `deleted-repo-backup-20261105/36-qb_analysis/work3_coreutils-38da01e5/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1122 | `deleted-repo-backup-20261105/36-qb_analysis/work3_coreutils-38da01e5/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1124 | `deleted-repo-backup-20261105/36-qb_analysis/work3_coreutils-38da01e5/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1126 | `deleted-repo-backup-20261105/36-qb_analysis/work3_coreutils-38da01e5/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1128 | `deleted-repo-backup-20261105/36-qb_analysis/work3_findutils-01add93a/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1130 | `deleted-repo-backup-20261105/36-qb_analysis/work3_findutils-01add93a/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1132 | `deleted-repo-backup-20261105/36-qb_analysis/work3_findutils-01add93a/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1134 | `deleted-repo-backup-20261105/36-qb_analysis/work3_findutils-01add93a/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1136 | `deleted-repo-backup-20261105/36-qb_analysis/work3_findutils-01add93a/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1138 | `deleted-repo-backup-20261105/36-qb_analysis/work3_findutils-01add93a/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1140 | `deleted-repo-backup-20261105/36-qb_analysis/work3_findutils-01add93a/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1142 | `deleted-repo-backup-20261105/36-qb_analysis/work3_findutils-01add93a/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1144 | `deleted-repo-backup-20261105/36-qb_analysis/work3_findutils-01add93a/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1146 | `deleted-repo-backup-20261105/36-qb_analysis/work3_control_which-3a31a668/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1148 | `deleted-repo-backup-20261105/36-qb_analysis/work3_control_which-3a31a668/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1150 | `deleted-repo-backup-20261105/36-qb_analysis/work3_control_which-3a31a668/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1152 | `deleted-repo-backup-20261105/36-qb_analysis/work3_control_which-3a31a668/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1154 | `deleted-repo-backup-20261105/36-qb_analysis/work3_control_which-3a31a668/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1156 | `deleted-repo-backup-20261105/36-qb_analysis/work3_control_which-3a31a668/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1158 | `deleted-repo-backup-20261105/36-qb_analysis/work3_control_which-3a31a668/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1160 | `deleted-repo-backup-20261105/36-qb_analysis/work3_control_which-3a31a668/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1162 | `deleted-repo-backup-20261105/36-qb_analysis/work3_control_which-3a31a668/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1164 | `deleted-repo-backup-20261105/30-llvm-archivefix-trial/root-fd4d3568/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1166 | `deleted-repo-backup-20261105/30-llvm-archivefix-trial/root-fd4d3568/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1168 | `deleted-repo-backup-20261105/30-llvm-archivefix-trial/root-fd4d3568/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1170 | `deleted-repo-backup-20261105/30-llvm-archivefix-trial/root-fd4d3568/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1172 | `deleted-repo-backup-20261105/30-llvm-archivefix-trial/root-fd4d3568/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1174 | `deleted-repo-backup-20261105/30-llvm-archivefix-trial/root-fd4d3568/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1176 | `deleted-repo-backup-20261105/30-llvm-archivefix-trial/root-fd4d3568/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1178 | `deleted-repo-backup-20261105/30-llvm-archivefix-trial/root-fd4d3568/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1180 | `deleted-repo-backup-20261105/30-llvm-archivefix-trial/root-fd4d3568/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1182 | `deleted-repo-backup-20261105/30-llvm-archivefix-trial/root-fd4d3568/worktree.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1184 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-bfd-1b27e3f6/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1186 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-bfd-1b27e3f6/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1188 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-bfd-1b27e3f6/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1190 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-bfd-1b27e3f6/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1192 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-bfd-1b27e3f6/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1194 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-bfd-1b27e3f6/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1196 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-bfd-1b27e3f6/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1198 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-bfd-1b27e3f6/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1200 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-bfd-1b27e3f6/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1202 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/latest-base_source-ae3cb8ab/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1204 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/latest-base_source-ae3cb8ab/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1206 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/latest-base_source-ae3cb8ab/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1208 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/latest-base_source-ae3cb8ab/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1210 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/latest-base_source-ae3cb8ab/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1212 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/latest-base_source-ae3cb8ab/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1214 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/latest-base_source-ae3cb8ab/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1216 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/latest-base_source-ae3cb8ab/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1218 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/latest-base_source-ae3cb8ab/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1220 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-lld-40f1e6ad/SHA256SUMS` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1222 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-lld-40f1e6ad/bundle-create.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1224 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-lld-40f1e6ad/bundle-unbundle.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1226 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-lld-40f1e6ad/bundle-verify.txt` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1228 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-lld-40f1e6ad/index.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1230 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-lld-40f1e6ad/inspection-before.json` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1232 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-lld-40f1e6ad/unpublished.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1234 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-lld-40f1e6ad/unpublished.patch.readcheck` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
| 1236 | `deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-lld-40f1e6ad/worktree.patch` | 无 | 无 | 无 | 无命中；未证实（U1） | 一致 |
