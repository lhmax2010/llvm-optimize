# 118 A：磁盘清点（只读，测量有缺口）

**/home 可用 113,540,780,032B（105.74GiB）；总量 1,967,844,950,016B，已用 1,754,267,557,888B。列出 6 个非重叠删除候选，已测占用合计 94,678,958,080B（88.18GiB）。没有删除任何文件。**

主工作区整根du达到900秒限时；补测未覆盖一级目录，每目录120秒。night-20261103仍超时，部分历史GBS根有权限拒绝；UNKNOWN或已测下限均保留原文，不冒称全量精确总和。没有访问另一项目目录/进程/锁，没有sudo。/home/abuild不存在；本项目BUILD-ROOTS位于W/temp下。外部GBS根97号已标为其他项目或归属未明，本轮不遍历。

du按实际分配块计数、单次遍历对硬链接去重；不同测量调用间可能共享硬链接。表中目录包含关系不可相加，候选和也不保证等于实际释放空间。当前完整Git仓库、74号RPM/日志、1226850/1226851、未来1231417/1231418下载目录、H2/H3及114/118源码均保留。候选只是待用户批准的名单，不构成删除授权。

## 不重叠主要位置前30

| 绝对路径 | GiB | 目录mtime（非递归最后改动） | 分类 | 依据 |
|---|---:|---|---|---|
| /home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105 | 91.294 | 2026-11-05T02:03:45.836235-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6 | 86.035 | 2026-11-11T09:56:13.411926-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2 | 84.157 | 2026-09-16T20:57:22.794994-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-archivefix-v2 | 79.287 | 2026-10-18T23:41:08.486525-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105 | 54.800 | 2026-11-05T04:21:50.023564-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028 | 39.188 | 2026-10-30T08:45:54.288482-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106-r2 | 36.691 | 2026-11-06T05:29:48.364021-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-tls-thumb-20261010 | 30.505 | 2026-10-10T03:23:59.598452-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261022-cache-release | 26.140 | 2026-10-26T06:51:27.618118-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106 | 22.022 | 2026-11-06T00:37:00.476591-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/qb-1225393-1225395 | 18.007 | 2026-11-10T21:34:07.507159-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/runpath-fix-20261026 | 16.929 | 2026-11-04T23:33:17.499877-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013 | 16.150 | 2026-10-12T22:23:08.412019-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/fifth-review-20261111 | 16.006 | 2026-11-11T00:15:49.476544-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/hq-review-104-20261116 | 11.842 | 2026-11-16T04:41:33.871048-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/crash-fix-probe-20261028 | 11.055 | 2026-10-27T23:08:09.131251-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-v2-final-20261009 | 10.339 | 2026-10-09T04:03:23.245118-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/oldtext-final-20261027 | 10.031 | 2026-11-04T23:33:49.361878-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-stage1-c-newrepo-20261010 | 9.236 | 2026-10-09T21:23:45.905594-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/review-20261103 | 8.539 | 2026-11-02T04:39:53.557296-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-on-hybrid-20261024 | 7.854 | 2026-10-26T03:49:40.959841-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/qb-1226850-1226851 | 7.760 | 2026-11-14T05:30:47.206310-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize-bolt | 7.653 | 2026-10-12T08:24:33.021022-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/bench_results | 7.284 | 2026-09-21T09:21:32.561284-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/llvm | 6.891 | 2026-09-15T23:29:38.804929-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/arm-source-root-probes-20261010 | 6.440 | 2026-10-10T10:22:40.834448-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/hq-463c9a13 | 6.284 | 2026-11-03T19:52:05.930922-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-stage1-20261010 | 5.957 | 2026-10-09T20:01:54.663399-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/hybrid-sandbox-20261019 | 5.663 | 2026-10-18T22:59:49.263426-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/pgo-bolt-followup-20261105 | 5.626 | 2026-11-04T18:18:48.781128-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |

## 全部已测目录前30（包含父子关系，禁止累加）

| 绝对路径 | GiB | 目录mtime | 分类 | 依据 |
|---|---:|---|---|---|
| /home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105 | 91.294 | 2026-11-05T02:03:45.836235-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6 | 86.035 | 2026-11-11T09:56:13.411926-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2 | 84.157 | 2026-09-16T20:57:22.794994-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local | 84.157 | 2026-09-16T20:57:22.794994-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS | 84.157 | 2026-09-16T20:57:22.794994-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0 | 84.157 | 2026-09-16T20:17:21.986898-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-archivefix-v2 | 79.287 | 2026-10-18T23:41:08.486525-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-archivefix-v2/local | 79.287 | 2026-09-29T08:51:40.552175-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS | 78.762 | 2026-09-29T08:51:40.554175-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0 | 78.762 | 2026-09-30T04:21:56.302961-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105 | 54.800 | 2026-11-05T04:21:50.023564-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain | 44.513 | 2026-11-05T07:16:43.359980-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028 | 39.188 | 2026-10-30T08:45:54.288482-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106-r2 | 36.691 | 2026-11-06T05:29:48.364021-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-tls-thumb-20261010 | 30.505 | 2026-10-10T03:23:59.598452-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain/gbs-root | 28.626 | 2026-11-05T04:22:44.074353-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain/gbs-root/local | 28.626 | 2026-11-05T04:22:44.074353-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106-r2/rehearsal | 27.008 | 2026-11-06T05:10:18.077107-08:00 | 可以删除 | 已结束的旧入口演练输出，69/72号已发布；不包含其兄弟source目录。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261022-cache-release | 26.140 | 2026-10-26T06:51:27.618118-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106 | 22.022 | 2026-11-06T00:37:00.476591-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106/rehearsal | 21.865 | 2026-11-05T23:05:44.225239-08:00 | 可以删除 | 已结束的旧演练输出，69/72号有记录；保留兄弟source仓库。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/qb-1225393-1225395 | 18.007 | 2026-11-10T21:34:07.507159-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/runpath-fix-20261026 | 16.929 | 2026-11-04T23:33:17.499877-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106-r2/rehearsal/basedev | 16.722 | 2026-11-09T04:35:53.031308-08:00 | 可以删除 | 已结束的旧入口演练输出，69/72号已发布；不包含其兄弟source目录。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106/rehearsal/basedev | 16.722 | 2026-11-06T00:37:48.969458-08:00 | 可以删除 | 已结束的旧演练输出，69/72号有记录；保留兄弟source仓库。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev | 16.558 | 2026-11-11T11:03:45.832087-08:00 | 必须保留 | 74号完整构建及比较基线容器；RPM、日志和工具后续仍需使用，不整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/10-archive-followup-review-20261014 | 16.460 | 2026-11-05T00:18:31.499985-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/05-review-round3-continue-20261012 | 16.460 | 2026-11-04T23:57:56.813936-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/19-release-attribution-20261013 | 16.460 | 2026-11-05T01:08:57.028105-08:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013 | 16.150 | 2026-10-12T22:23:08.412019-07:00 | 必须保留 | 证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。 |

## 可删除候选

| 绝对路径 | GiB | 目录mtime | 分类 | 依据 |
|---|---:|---|---|---|
| /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106-r2/rehearsal | 27.008 | 2026-11-06T05:10:18.077107-08:00 | 可以删除 | 已结束的旧入口演练输出，69/72号已发布；不包含其兄弟source目录。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106/rehearsal | 21.865 | 2026-11-05T23:05:44.225239-08:00 | 可以删除 | 已结束的旧演练输出，69/72号有记录；保留兄弟source仓库。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/rehearsal | 13.504 | 2026-11-11T01:48:58.681766-08:00 | 可以删除 | 74号已结束演练输出；保留同根toolchain/basedev完整构建和RPM、日志。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/toolchain/validation/payload | 13.145 | 2026-11-11T09:31:26.496514-08:00 | 可以删除 | 74号入口的RPM载荷展开副本；原完整构建根和RPM保留，重新解包可重建；不删validation其他证据。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain/validation/payload | 12.574 | 2026-11-05T07:20:39.288830-08:00 | 可以删除 | 63号入口的RPM载荷展开副本；同层gbs-root及其RPM/真实转换输入保留，可重新解包。 |
| /home/linhao/Toolchain/development/llvm-optimize/temp/combined-112-20261116 | 0.082 | 2026-11-16T21:14:10.249411-08:00 | 可以删除 | 112准备停止后保留的补丁试应用工作树；112已发布patch-only diff和提交身份；按本任务明确列入过期工作树候选。删除前须另获批准并保全Git工作树登记。 |

[完整逐目录分类](../../tools/bolt/results/disk-118/inventory.jsonl)、[删除候选原文](../../tools/bolt/results/disk-118/delete-candidates.txt)、[测量总结](../../tools/bolt/results/disk-118/summary.json)、[初始du状态](../../tools/bolt/results/disk-118/measurement-errors.json)。B下载的新RPM会另附容量补记，不把后来下载计入本次时点。

A 已结束 2026-11-16T22:38:24.747322-08:00 status=PARTIAL（测量缺口；只读清单已交付）

## B下载补充
QB 1231417/1231418 的保留目录 W/temp/qb-1231417-1231418 新测占用 8,374,734,848 B（含源码审计副本）；RPM和日志为当前保留基线，不在删除候选中。见118 B download-disk.txt。
