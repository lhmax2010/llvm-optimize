# 149-clean · 工作区磁盘清理

工作区清理使 /home 净可用增加 **267,747,110,912 B**（267.75 GB），终点为 **300,193,996,800 B**。距 400 GB 目标还差 **132,252,889,088 B**。

未发现仍在运行的本项目构建单元及残留 GBS、rpmbuild、Ninja。

| 阶段 | /home 可用 B | 较上次变化 B |
|---|---:|---:|
| 起点 | 32,446,885,888 | — |
| 第 1 层结束 | 294,564,814,848 | +262,117,928,960 |
| 第 2 层结束 | 300,587,233,280 | +6,022,418,432 |
| 第 3 层交接 | 300,193,996,800 | 0（脚本等待用户执行） |

第 2 层采样到最终采样之间，文件系统可用量净变化 -393,236,480 B。df 记录整个文件系统的净值。

第 1 层删除 148 中断构建的中间文件和识别出的 GBS 中间树、tmpdir，保留日志、JSON、Git 和 profile。优先处理大文件，此后将 root 拥有的子树从普通用户扫描中分离。第 2 层逐项记录大小、SHA256 和重建提交，处理未完成的 N2 RPM、可证明一致的缓存和经 Git 验证的重复检出。未能证明状态的源码副本、旧下载和最终产物保留。

## 剩余目录

初始 du 超过只读盘点时限。以下为完整返回过测量的候选排名，不能保证覆盖未测分区。分配字节来自 du，相互包含的路径仅列较大的一项。

| 路径 | 分配 B | 类别 | 保留引用 |
|---|---:|---|---|
| W/temp/deleted-repo-backup-20261105 | 50,542,764,032 | Git / 工作树 | All future tasks |
| W/temp/keep-baselines | 30,193,508,352 | 基线 RPM / ELF | 82 input and pending T/D；361395 PS5 |
| W/archive/task145 | 13,762,039,808 | 证据、保留产物或待 sudo 构建根 | 361624 PS5 |
| W/temp/arm-archive-stage1-c-newrepo-20261010 | 9,917,100,032 | 历史源码、RPM 或证据 | 未列明，历史资产待核对 |
| W/llvm | 7,398,653,952 | Git / 工作树 | Primary LLVM checkout |
| W/temp/hq-463c9a13 | 7,249,158,144 | 历史源码、RPM 或证据 | 未列明，历史资产待核对 |
| W/.git | 6,408,699,904 | Git / 工作树 | All future tasks |
| W/temp/hybrid-link-20261015 | 5,731,500,032 | 历史源码、RPM 或证据 | 未列明，历史资产待核对 |
| W/temp/bolt-measurement-20260918 | 3,940,847,616 | 历史源码、RPM 或证据 | 未列明，历史资产待核对 |
| W/archive/task142 | 3,529,482,240 | 证据、保留产物或待 sudo 构建根 | 未列明，历史资产待核对 |
| W/temp/review-20261102 | 2,823,204,864 | 历史源码、RPM 或证据 | 未列明，历史资产待核对 |
| W/archive/task146 | 1,921,003,520 | 证据、保留产物或待 sudo 构建根 | 未列明，历史资产待核对 |
| W/temp/release-debug-independence-20261013 | 943,308,800 | 历史源码、RPM 或证据 | 未列明，历史资产待核对 |
| W/archive/task138-n-20261119 | 926,486,528 | 证据、保留产物或待 sudo 构建根 | G4–G8 checkpoints |
| W/archive/server-kit-136 | 801,185,792 | 历史源码、RPM 或证据 | G4–G8 training inputs |

G1–G3 收据与 23 份 profraw 保留。合并 profdata 核对 SHA256 成功。PS5 profile Git blob、82 基线、361395 比较 RPM、361624 B1/B2 最终 RPM、技能和证据保留。

## 工作区外

确认 /home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM 是 ARM sysroot 的历史来源。该路径只读。权限不足或计时结束时未取得完整大小。

~~~text
356757504	/home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0/usr/lib
611594240	/home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.aarch64.0/usr/lib64
~~~

## 待处理

第 3 层脚本位于 /home/linhao/Toolchain/development/llvm-optimize/archive/task149-clean/sudo-clean.py，固定校验清单含 17 条。脚本限制于原工作区中的 root 所有文件和目录，核对路径、设备、inode、挂载及打开状态。

如仍需更多空间，先决定是否处理归档 Git 副本和保留的 RPM 基线。Git 局部历史尚未证明能完整重建。361624 B1 有 3 小时 2 分 21 秒的成功记录，B2 约 17 分钟。N2 已运行 5 小时 16 分钟才在打包中断，该值只是重跑成本下界。

按用户后续确认，本轮仅清理。任务 149 的 C、D、E 等用户查看本结果后决定。

[原始 df 与各层清单](../../tools/bolt/results/task149-clean/)
