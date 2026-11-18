# 135 号工作区清理

**结论。** 删除 66 项，已删除条目的占用合计 50,666,196,992 B（47.19 GiB）。本轮 /home 可用量净变化 +50,179,301,376 B（46.73 GiB），由 137,630,318,592 B 变为 187,809,619,968 B（174.91 GiB）。脚本列出 239 个权限待审项，已知占用 233,302,179,840 B。未使用 sudo。

实际删除分类：build-cache 11, experiment 8, qb-download 45, worktree 2。保护清单 116 条，已保留；末尾实际核对通过。构建根中有少数目录普通用户不可读，du 对相应树为已见下界。df 为整盘净值，包含了本轮归档写入和同文件系统并发变化。

## 保留与权限待审

- 保留两个项目工作区的 Git 元数据与已发布证据，R/I、PS5/H5、审阅目录和 keep-baselines。
- 82 入口、74 号四个项目配置文件、131 编排和 23 个输入均定位。20 个真实输入内容与原记录一致。三个缺失合成输入以相同 SHA256 保存在本地回补目录，由 131 的既有生成器处理原地址缺失的情况。对应的 20 个源码 Git 对象均可读取。
- 核对了 merge-fdata 和 libbolt_rt_instr.a 的 SHA256。保留了 99 的 450 个发货归档、两份源 RPM、原始转换输入和工具路径。
- 三组 QB 的每个构建均保留已定位的 RPM。修改时间门槛、Git 归属、未证明的证据用途或保护输入所阻止的目录见清单。
- 手工审核脚本 /home/linhao/Toolchain/development/llvm-optimize/archive/sudo-delete.sh 共 239 条。目录占用可能有权限盲区，另有 2 条大小未知。脚本先检查 canonical 路径、身份、挂载和 Git/修改时间条件，然后验证备份 SHA。仅执行了语法检查。

[保留清单](../../tools/bolt/results/workspace-cleanup-135/retention.json) · [清理目录与保留理由](../../tools/bolt/results/workspace-cleanup-135/directory-plan.json) · [实际逐项结果](../../tools/bolt/results/workspace-cleanup-135/directories-outcomes.json) · [目录待审](../../tools/bolt/results/workspace-cleanup-135/directories-pending.json) · [备份待审](../../tools/bolt/results/workspace-cleanup-135/backup-pending.json) · [近期目录](../../tools/bolt/results/workspace-cleanup-135/recent-directories.json)

## 备份导出

26 个 bundle 共发现 162 个按 bundle 计的未证明可达提交，成功导出 158 份补丁，共 499,552,894 B。引用核对使用当前 GitHub 和 Gerrit 的只读结果，复用了证实仍由远端覆盖的历史图。涉及当前不可写的 bundle，完整文件 SHA 校验由待审核脚本在根路径验证后执行。分支来源、父提交、git log、每份补丁路径、字节数与 SHA256 均有记录。超过 50 MB，证据仓库只提交索引与摘要。

| Bundle 原工作区 | 未覆盖提交 | 已导出补丁 | 补丁字节 | 判定 |
|---|---:|---:|---:|---|
| W/temp/deleted-repo-backup-20261105/_selftest2/source | 5 | 4 | 1,361 | 保留 |
| W/temp/deleted-repo-backup-20261105/_selftest/source | 5 | 4 | 1,361 | 保留 |
| W/temp/deleted-repo-backup-20261105/_selftest3/source | 5 | 4 | 1,361 | 保留 |
| W/temp/pgo-resource-20261102/source-D | 2 | 2 | 12,676,367 | 权限待审 |
| W/temp/review-round3-continue-20261012/patch-apply-check | 0 | 0 | 0 | 权限待审 |
| W/temp/review-round3-continue-20261012/patch-work | 2 | 2 | 53,063 | 权限待审 |
| W/temp/archive-fix-full-build-20260927/test-package-bfd | 1 | 1 | 7,864 | 权限待审 |
| W/temp/archive-fix-full-build-20260927/test-package-lld | 1 | 1 | 7,842 | 权限待审 |
| W/temp/archive-followup-review-20261014/apply-check | 0 | 0 | 0 | 权限待审 |
| W/temp/archive-followup-review-20261014/submit-work | 0 | 0 | 0 | 权限待审 |
| W/temp/release-x86-full-build-20261013/latest-base/source | 2 | 2 | 55,821 | 权限待审 |
| W/temp/release-x86-full-build-20261013/round2-eight-output-proof/test-package-bfd | 2 | 2 | 13,247 | 权限待审 |
| W/temp/release-x86-full-build-20261013/round2-eight-output-proof/test-package-lld | 2 | 2 | 13,247 | 权限待审 |
| W/temp/release-attribution-20261013/patch-apply-check | 0 | 0 | 0 | 权限待审 |
| W/temp/release-attribution-20261013/patch-work | 2 | 2 | 55,821 | 权限待审 |
| W/temp/llvm-strip-alternative-20260929/test-package-bfd | 1 | 1 | 8,890 | 权限待审 |
| W/temp/llvm-strip-alternative-20260929/test-package-lld | 1 | 1 | 8,880 | 权限待审 |
| W/temp/llvm-strip-x86_64-20261009/continue-20261009/test-package-bfd | 1 | 1 | 12,325 | 权限待审 |
| W/temp/llvm-strip-x86_64-20261009/continue-20261009/test-package-lld | 1 | 1 | 12,320 | 权限待审 |
| W/temp/llvm-hybrid-trial | 0 | 0 | 0 | 权限待审 |
| W/temp/llvm-archivefix-trial | 0 | 0 | 0 | 权限待审 |
| W/temp/followup-356949-ps2-message-20261014/review-work | 0 | 0 | 0 | 权限待审 |
| /home/linhao/qb_analysis/work3/control/findutils | 33 | 33 | 227,725,029 | 权限待审 |
| /home/linhao/qb_analysis/work3/control/which | 13 | 13 | 501,609 | 权限待审 |
| /home/linhao/qb_analysis/work3/coreutils | 50 | 49 | 30,671,457 | 保留 |
| /home/linhao/qb_analysis/work3/findutils | 33 | 33 | 227,725,029 | 权限待审 |

[完整 bundle 索引](../../tools/bolt/results/workspace-cleanup-135/bundle-export.json) · [提交摘要目录](../../tools/bolt/results/workspace-cleanup-135/bundle-commit-summaries/) · [非 bundle 移动/重复核对](../../tools/bolt/results/workspace-cleanup-135/backup-misc-plan.json)

## 删除前后目录占用

同一项目文件系统内三层 du 统计。不含 W、W/temp 和 B 三个汇总容器，子目录可以同时出现，行之间不能相加。前置扫描退出码 1，原因为权限错误。后置排名对三个受影响且较小的分支重新运行 du，其余行从前置读数及逐项删除记录对账；没有二次全量扫描。每行口径在 JSON 中保留。

### 删除前 20

| 排名 | 目录 | 已分配字节 | 最后修改时间 |
|---:|---|---:|---|
| 1 | /home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105 | 98,026,516,480 | 2026-11-05T02:03:45-08:00 |
| 2 | /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6 | 92,379,582,464 | 2026-11-11T09:56:13-08:00 |
| 3 | /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-archivefix-v2 | 85,133,672,448 | 2026-10-18T23:41:08-07:00 |
| 4 | /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-archivefix-v2/local | 85,133,668,352 | 2026-09-29T08:51:40-07:00 |
| 5 | /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261103 | 72,489,062,400 | 2026-11-03T12:13:34-08:00 |
| 6 | /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105 | 58,841,325,568 | 2026-11-05T04:21:50-08:00 |
| 7 | /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/toolchain | 50,761,310,208 | 2026-11-11T09:27:49-08:00 |
| 8 | /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain | 47,795,748,864 | 2026-11-05T07:16:43-08:00 |
| 9 | /home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028 | 42,077,601,792 | 2026-10-30T08:45:54-07:00 |
| 10 | /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261103/toolchain | 37,586,169,856 | 2026-11-04T00:31:55-08:00 |
| 11 | /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106-r2 | 36,524,761,088 | 2026-11-06T05:29:48-08:00 |
| 12 | /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-tls-thumb-20261010 | 32,754,786,304 | 2026-10-10T03:23:59-07:00 |
| 13 | /home/linhao/Toolchain/development/llvm-optimize/temp/keep-baselines | 30,193,508,352 | 2026-11-17T19:31:24-08:00 |
| 14 | /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106-r2/rehearsal | 26,128,203,776 | 2026-11-06T05:10:18-08:00 |
| 15 | /home/linhao/Toolchain/development/llvm-optimize/temp/keep-baselines/bolt-v4-20261022-cache-release | 19,689,316,352 | 2026-11-17T00:51:00-08:00 |
| 16 | /home/linhao/Toolchain/development/llvm-optimize/temp/qb-1225393-1225395 | 19,335,061,504 | 2026-11-10T21:34:07-08:00 |
| 17 | /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2 | 18,702,589,952 | 2026-09-16T20:57:22-07:00 |
| 18 | /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local | 18,702,585,856 | 2026-09-16T20:57:22-07:00 |
| 19 | /home/linhao/Toolchain/development/llvm-optimize/temp/runpath-fix-20261026 | 18,177,810,432 | 2026-11-04T23:33:17-08:00 |
| 20 | /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106 | 17,903,505,408 | 2026-11-06T00:37:00-08:00 |

### 删除后 20

| 排名 | 目录 | 已分配字节 | 最后修改时间 |
|---:|---|---:|---|
| 1 | /home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105 | 98,026,516,480 | 2026-11-05T02:03:45-08:00 |
| 2 | /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6 | 92,379,582,464 | 2026-11-11T09:56:13-08:00 |
| 3 | /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-archivefix-v2 | 85,133,672,448 | 2026-10-18T23:41:08-07:00 |
| 4 | /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-archivefix-v2/local | 85,133,668,352 | 2026-09-29T08:51:40-07:00 |
| 5 | /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261103 | 72,489,062,400 | 2026-11-03T12:13:34-08:00 |
| 6 | /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105 | 58,841,227,264 | 2026-11-05T04:21:50-08:00 |
| 7 | /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/toolchain | 50,761,310,208 | 2026-11-11T09:27:49-08:00 |
| 8 | /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain | 47,795,748,864 | 2026-11-05T07:16:43-08:00 |
| 9 | /home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028 | 42,077,601,792 | 2026-10-30T08:45:54-07:00 |
| 10 | /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261103/toolchain | 37,586,169,856 | 2026-11-04T00:31:55-08:00 |
| 11 | /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106-r2 | 36,524,761,088 | 2026-11-06T05:29:48-08:00 |
| 12 | /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-tls-thumb-20261010 | 32,754,786,304 | 2026-10-10T03:23:59-07:00 |
| 13 | /home/linhao/Toolchain/development/llvm-optimize/temp/keep-baselines | 30,193,508,352 | 2026-11-17T19:31:24-08:00 |
| 14 | /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106-r2/rehearsal | 26,128,203,776 | 2026-11-06T05:10:18-08:00 |
| 15 | /home/linhao/Toolchain/development/llvm-optimize/temp/keep-baselines/bolt-v4-20261022-cache-release | 19,689,316,352 | 2026-11-17T00:51:00-08:00 |
| 16 | /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2 | 18,702,589,952 | 2026-09-16T20:57:22-07:00 |
| 17 | /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local | 18,702,585,856 | 2026-09-16T20:57:22-07:00 |
| 18 | /home/linhao/Toolchain/development/llvm-optimize/temp/runpath-fix-20261026 | 18,177,810,432 | 2026-11-04T23:33:17-08:00 |
| 19 | /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106 | 17,903,505,408 | 2026-11-06T00:37:00-08:00 |
| 20 | /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev | 17,779,294,208 | 2026-11-11T11:03:45-08:00 |

[前 40](../../tools/bolt/results/workspace-cleanup-135/top40-before.json) · [清理后前 20](../../tools/bolt/results/workspace-cleanup-135/top20-after.json) · [空间读数](../../tools/bolt/results/workspace-cleanup-135/space.json) · [前置 du 原文](../../tools/bolt/results/workspace-cleanup-135/du-before.stderr) · [后置 du 原文](../../tools/bolt/results/workspace-cleanup-135/du-after.stderr) · [后置逐行口径](../../tools/bolt/results/workspace-cleanup-135/du-after-method.json)

## STOP 原文

- /home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/00-source/root-5645c783/repository.bundle

~~~text
format-patch count 4 != unique commit count 5
~~~

- /home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/00-source/root-759fbb28/repository.bundle

~~~text
format-patch count 4 != unique commit count 5
~~~

- /home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/00-source/root-e27851fd/repository.bundle

~~~text
format-patch count 4 != unique commit count 5
~~~

- /home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/36-qb_analysis/work3_coreutils-38da01e5/repository.bundle

~~~text
format-patch count 49 != unique commit count 50
~~~

完整精确路径和逐项保留原因见上述清单。任务工具的准备错误及处理如下。

~~~text
/bin/bash: line 4: /usr/bin/gawk: No such file or directory
/bin/bash: -c: line 4: unexpected EOF while looking for matching `"'
TypeError: s.index is not a function
SyntaxError: Unexpected token '%'
~~~

以上分别改用 Python 读取挂载表、直接调用 systemctl、修正脚本生成表达式及 shell 模板。原稿未触发删除。
