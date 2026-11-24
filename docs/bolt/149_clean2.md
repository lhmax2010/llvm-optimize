# 149-clean2 · 工作区进一步清理

最终可用 **413,877,944,320 B（413.878 GB）**，400 GB 目标已达到。余量 13,877,944,320 B，差额 0 B。149-run 等用户另外发令。

## 可用空间与逐步释放

| 步骤 | 释放或变化 B | 依据 |
|---|---:|---|
| 0 复测上次 sudo | +113,239,748,608 | 从前次最终采样到本次起点的 df 净变化。sudo 独立释放字节未取得 |
| 1 八个历史路径 | 0 | 逐项检查后全部保留 |
| 2 task145 | +859,156,480 | 第 2 步单独前后 df。删除 18 个文件，文件分配量 709,468,160 B |
| 3 Git GC | 0 | 远端同名分支核对未通过，跳过 |
| 4 备份仓库 | 0 | 原目录全部保留。新增 3 个 bundle，共 3,513 B 文件内容 |

起点可用 413,433,745,408 B，终点可用 413,877,944,320 B，本轮 df 净变化 +444,198,912 B。df 为整个文件系统采样。

## 上次 sudo 复核

journal 确认用户于 2026-11-23 21:27:12 PST 启动脚本，sudo 会话于 21:29:15 PST 结束。复查了 17 个路径及 inode。脚本允许保留日志等文件，因此目录仍存在不能判作拒绝。未找到保存的终端 stdout 和两张 sudo 内部 df，成功数、拒绝数及由脚本单独释放的字节记为未知。

## 保留项目

| 路径 | 保留原因 |
|---|---|
| W/temp/arm-archive-stage1-c-newrepo-20261010 | 有 3 个嵌套打包仓库和本地 ARM 重建输入，未证明完整归档覆盖。 |
| W/temp/hq-463c9a13 | 有独立 Git 对象库，对应远端与本地历史覆盖未证明。 |
| W/temp/hybrid-link-20261015 | 保留原始 CMake 比较与本地实验，未证明 bolt-v4 的归档覆盖完整。 |
| W/temp/bolt-measurement-20260918 | 包含独有的插桩和原始 profile 数据，未证明可从提交重建。 |
| W/temp/review-20261102 | 保留本地评审源码和补丁序列，未证明远端覆盖及全部现场可重建。 |
| W/temp/release-debug-independence-20261013 | 包含实物 release/debug 对比输入及产物，未证明完整归档。 |
| W/archive/task142 | 142 号报告引用本地路径和原始工具结果。 |
| W/archive/task146 | 146、147 号报告引用本地比较、原始工具输出和其身份记录。 |

149 号空间盘点中的目录提及已与实际证据引用区分。每个路径的命中行、可识别的本地仓库和状态均附在清单中。

task145 删除了 16 份已与保留 B1 RPM 校验相同的 provider 副本及 2 份已校验的 GBS 暂存源码包。另有 112 份 root 所有缓存 RPM 保留，保留 B2 最终 4 个 RPM、全部鉴定证据与实物冒烟输入输出。清理前后按原收据复核了四个成品。对 sudo 处理过的 chroot 只做入口复核，此轮未再次清理。

W/.git 两次 du 分别为 6,745,923,584 B 和 6,408,810,496 B。main 与 bolt-v4 同名远端头完全一致。arm-archive-stage1-20261010 的提交可从远端 bolt-v4 到达，同名分支未推送，故未运行 git gc --prune=now。

## 备份仓库和 bundle

检查了 29 个 Git 目录，包括 26 个当前没有 refs 的历史验证对象库。历史 bundle 中的 ref 名不等于验证对象库当前安装的 ref。至少在抽查的对象库里仍有悬空提交，且这些库不配置远端，全部原样保留。本次以实时 GitHub refs 核验 W/.git。未访问 Gerrit/QB，历史备份缺少可据以删除的对应远端证明。

备份目录中单列了 49 个非 Git 内部条目，共 7,120,131 B。没有删除。

| 仓库 | Ref 数 | 字节 | SHA256 |
|---|---:|---:|---|
| W/temp/deleted-repo-backup-20261105/_selftest/source | 3 | 1,173 | 0750794448e89e58b7f6b7d9375d5f70b6548a6f1ca6ab4c11b69d096a458af5 |
| W/temp/deleted-repo-backup-20261105/_selftest2/source | 3 | 1,169 | 3b18df6dd55f9947eb4e7eb9bb4cc3a923f15c51bf39246eadc2f1c293f4bae1 |
| W/temp/deleted-repo-backup-20261105/_selftest3/source | 3 | 1,171 | 5b649b8950871aa92003f3b869b4dbebdad7b293a796804a70b999a6af356060 |

bundle 均保存于 W/archive/backup-unique/task149-clean2/。每份 bundle 分别执行验证并镜像克隆，克隆中的 ref 名和提交 ID 与源逐项相同。验证克隆已删除。自测仓库本身保留以保存工作树、index 和 reflog。

[原始 df、备份仓库逐项结果及保留清单](../../tools/bolt/results/task149-clean2/)
