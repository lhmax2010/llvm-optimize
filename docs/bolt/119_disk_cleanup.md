# 119：磁盘清理

结论：本轮核对后删除241项、跳过9项；没有删除Git工作树、没有执行worktree prune，没有删除任何保护目录。D独立因测试FAIL停止，未生成H3。

/home可用：104,394,362,880 → 206,063,710,208 B（97.22 → 191.91 GiB）；净增加 **94.69 GiB**。
删除目标allocated大小合计119,833,190,400 B（111.60 GiB），逐项删除瞬间df增量合计119,556,751,360 B。与净增量不同，主要因为保全文件新增占用；df也是共享文件系统即时读数，不把所有波动归因于删除。

## 执行边界与扫描

166个W/temp一级目录逐个新扫描（du -s -x -B1 --time），不读取97/118 inventory作为分类输入。每目录60秒，超时/权限错误记UNKNOWN或partial，不重试。已发布报告由当前bolt-v4 HEAD的docs/bolt清单核对。构建根内BUILD/lto.cache另一次定向发现（每根10秒）；发现不完整不声称清点了全部中间树。

分析、测试、复制与删除串行systemd用户服务，4GiB/swap0/CPU200%/Nice19/IOidle。删除服务耗时18min03.865s、memory peak约2.4G、swap0。保全过程较慢时只读检查过本任务服务状态和自身fd/文件大小；没有检查另一项目的目录、进程或锁。没有提高资源。

删除前校验realpath仍在W/temp、保护路径、挂载、Git标记、逐目录写入权限；不跟随符号链接。顶层符号链接保守保留；删除树内的链接由rm自身移除，不递归其目标。逐项使用nice19/ionice3和明确路径rm -rf --one-file-system，命令原文见delete-results.jsonl。

所有找到的RPM及常规日志均先复制到W/temp/keep-baselines/<一级目录>/task119/，逐文件SHA相同才删除；共16,601个文件/链接。backup-NNN.json保存来源、目标、SHA/链接。删除后再次确认备份大小/链接和保护路径存在；不把大小复核当作第二次全量SHA重算。

## 最大删除项目

|路径（相对W/temp）|GiB|类别|
|---|---:|---|
|gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD|66.739|A2(d)|
|bolt-v4-20261022-cache-release|26.140|A2(c)|
|arm-archive-stage1-20261010|5.957|A2(c)|
|arm-archive-standard-build-20261010|4.738|A2(c)|
|rebase-359934-20261106/rehearsal/basedev/retry-02/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD|2.674|A2(d)|
|rebase-359934-20261106-r2/rehearsal/basedev/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD|2.674|A2(d)|
|rebase-359934-20261106/rehearsal/basedev/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD|2.674|A2(d)|
|gbs-root-x86_64-debuginfo-j4|0.003|A2(a)|
|night-revalidation-20261104-tests-05|0.000|A2(c)|
|night-revalidation-20261104-tests|0.000|A2(c)|

[完整241项删除清单](../../tools/bolt/results/disk-119/deleted.md)；[9项跳过清单](../../tools/bolt/results/disk-119/skipped.md)；[全部一级目录、保留与待决定清单](../../tools/bolt/results/disk-119/inventory-and-retained.md)。

## 保留与待决定

永久保留：W/B Git工作区、H2/114/118工作树及本轮证据、74号材料/RPM/日志、两组重点QB产物、review-*、keep-baselines。另保留当前真实转换输入和测试运行时依赖。全部路径见protection-rules.json及postcheck.json。

旧combined-112-20261116尚不足7天，且C1为本地提交61d821ab；保留。rebase-*为含源码/演练/结果的复合目录，不按父目录整删，只处理独立核实的BUILD子目录。当前公共LLVM对象库相对“本地已有且与当前远端广告引用相同”的29个锚点尚有28个未覆盖提交，原文见worktree-commit-reachability.json。此口径是保守的可达性证明范围，不把未覆盖等同于从未推送；未补fetch隐含refs、未更改任何工作树/引用，A2(b)未达到删除门禁。

9项删除前跳过：8项目录不可写/不可搜索、1项主BUILD验证超过60秒。未sudo、未改权限、未重试。其他大目录du或Git标记扫描超时、报告/期限/提交可达性不能证明时，也保留并列为不确定。

## deleted-repo-backup-20261105

大小98,026,516,480 B（91.30 GiB），原样保留。包含26份仓库bundle、验证对象库、原工作区/index/unpublished补丁和检查记录，另有3个selftest。涵盖LLVM历史构建/PGO/混合链接/归档工作，以及findutils/coreutils/which实验源码。

[逐仓库内容概要](../../tools/bolt/results/disk-119/backup-summary.md)，[完整分支、提交和覆盖记录](../../tools/bolt/results/disk-119/backup-bundle-summary.json)。其中followup-356949的review-work备份可由已核实当前引用覆盖；其余存在未覆盖提交或UNKNOWN。没有删除、fetch或改写这些备份。

## 已读与未做

已读：本次目录实测、发布文档32/43/51/55/65等、Git worktree与只读远端引用、备份bundle头/原inspection记录、删除前清单与保全SHA。未重建、未运行BOLT、未访问QB、未写Gerrit；未删除源码保护备份或保护产物；未强行清理权限/超时条目。

A 已结束 2026-11-17T01:11:44.631896-08:00 status=PASS_WITH_SKIPS
