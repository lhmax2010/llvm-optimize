# 52：用户批准的十个目录清理（2026-11-03）

批准的 10 个精确路径全部删除，跳过 0 项。删除执行窗口内 `/home` 的 `df` 可用空间增加 132,982,358,016 字节（123.849 GiB），执行结束时可用 285,199,704,064 字节（265.613 GiB）。父目录内其他条目检查通过，源码、保全产物和 PGO 现场保留。

## 1. 授权范围与检查

`W=/home/linhao/Toolchain/development/llvm-optimize`。本次用户明确批准下表 10 项；路径均相对 `W/temp/`。没有扩展至父目录或同级目录，没有构建、Gerrit/sandbox/QB 操作，也没有修改权限或 VS Code 配置。

每项在删除前检查真实目录、非软链接、父目录非软链接、realpath 精确匹配及 dev/inode 未变化；`findmnt -rn -o TARGET,SOURCE,FSTYPE,OPTIONS` 无内部挂载或 overlay 引用；逐个读取 `/proc/*/{cwd,root,exe,fd,maps}` 无命中；active/activating/reloading/deactivating 的 systemd 用户服务无引用。10 份最终 root-precheck 均为挂载命中 0、进程命中 0、读取错误 0、服务查询成功。

普通用户首次 `/proc` 检查有 1424 条权限盲区，没有据此删除；同一次用户授权的 root 调用补查并消除了盲区，再逐项执行。证据：[processes-before.json](../../tools/bolt/results/disk-cleanup-20261103/processes-before.json)、[mounts-before.json](../../tools/bolt/results/disk-cleanup-20261103/mounts-before.json)、[services-before.json](../../tools/bolt/results/disk-cleanup-20261103/services-before.json)。

|序号|批准路径（相对 W/temp）|最终检查|删除身份|结果|逐项 df 增量（字节 / GiB）|rm 耗时秒|
|---|---|---|---|---|---|---|
|1|`final-20261103/toolchain-rehearsal/gbs-root`|[PASS](../../tools/bolt/results/disk-cleanup-20261103/root-precheck-01.json)|root：普通用户不可写|已删除，rc=0|7,022,100,480 / 6.540|42.899|
|2|`final-20261103/basedev-rehearsal/gbs-root`|[PASS](../../tools/bolt/results/disk-cleanup-20261103/root-precheck-02.json)|root：普通用户不可写|已删除，rc=0|6,969,180,160 / 6.491|34.986|
|3|`final-20261103/basedev-rehearsal/retry-02/gbs-root`|[PASS](../../tools/bolt/results/disk-cleanup-20261103/root-precheck-03.json)|root：普通用户不可写|已删除，rc=0|6,969,315,328 / 6.491|31.198|
|4|`second-review-20261104/toolchain-rehearsal/gbs-root`|[PASS](../../tools/bolt/results/disk-cleanup-20261103/root-precheck-04.json)|root：普通用户不可写|已删除，rc=0|7,021,027,328 / 6.539|48.918|
|5|`second-review-20261104/basedev-rehearsal/gbs-root`|[PASS](../../tools/bolt/results/disk-cleanup-20261103/root-precheck-05.json)|root：普通用户不可写|已删除，rc=0|6,956,515,328 / 6.479|46.270|
|6|`archive-index-fix-rpm-20260923`|[PASS](../../tools/bolt/results/disk-cleanup-20261103/root-precheck-06.json)|普通用户 UID 1000|已删除，rc=0|54,659,883,008 / 50.906|6.792|
|7|`archive-fix-rebind-20260923`|[PASS](../../tools/bolt/results/disk-cleanup-20261103/root-precheck-07.json)|普通用户 UID 1000|已删除，rc=0|24,292,904,960 / 22.625|3.512|
|8|`static-native-conversion-20260924`|[PASS](../../tools/bolt/results/disk-cleanup-20261103/root-precheck-08.json)|普通用户 UID 1000|已删除，rc=0|6,771,978,240 / 6.307|2.414|
|9|`toolchain-hybrid-trial`|[PASS](../../tools/bolt/results/disk-cleanup-20261103/root-precheck-09.json)|普通用户 UID 1000|已删除，rc=0|6,178,152,448 / 5.754|1.132|
|10|`hybrid-trial-20260922`|[PASS](../../tools/bolt/results/disk-cleanup-20261103/root-precheck-10.json)|普通用户 UID 1000|已删除，rc=0|6,141,784,064 / 5.720|1.411|

完整逐项身份、命令、df 原文、时间和存在性结果：[execution.json](../../tools/bolt/results/disk-cleanup-20261103/execution.json)。

## 2. 第 6–10 项删除前清单

顶层文件/子目录元数据以及全部 RPM 文件名、字节数和本次读取计算的 SHA256 已在删除前落盘；只保存清单，没有复制 RPM。RPM 读取前后 inode/size/mtime 一致，遍历/哈希错误均为 0。

|序号|du 实际占用字节 / GiB|RPM 数|RPM 字节合计|顶层清单|RPM SHA256 清单|
|---|---|---|---|---|---|
|6|54,659,932,160 / 50.906|2|1,094,914|[inventory-06-top.json](../../tools/bolt/results/disk-cleanup-20261103/inventory-06-top.json)|[inventory-06-rpms.json](../../tools/bolt/results/disk-cleanup-20261103/inventory-06-rpms.json)|
|7|24,293,048,320 / 22.625|69|9,637,357,281|[inventory-07-top.json](../../tools/bolt/results/disk-cleanup-20261103/inventory-07-top.json)|[inventory-07-rpms.json](../../tools/bolt/results/disk-cleanup-20261103/inventory-07-rpms.json)|
|8|6,771,978,240 / 6.307|0|0|[inventory-08-top.json](../../tools/bolt/results/disk-cleanup-20261103/inventory-08-top.json)|[inventory-08-rpms.json](../../tools/bolt/results/disk-cleanup-20261103/inventory-08-rpms.json)|
|9|6,178,152,448 / 5.754|0|0|[inventory-09-top.json](../../tools/bolt/results/disk-cleanup-20261103/inventory-09-top.json)|[inventory-09-rpms.json](../../tools/bolt/results/disk-cleanup-20261103/inventory-09-rpms.json)|
|10|6,141,796,352 / 5.720|0|0|[inventory-10-top.json](../../tools/bolt/results/disk-cleanup-20261103/inventory-10-top.json)|[inventory-10-rpms.json](../../tools/bolt/results/disk-cleanup-20261103/inventory-10-rpms.json)|

第 1–5 项的额外限时 du 均超时，大小记 UNKNOWN，不借用历史数值；用户要求的第 6–10 项总大小均取得。第 6 项首次 du 超时，完整路径/RPM遍历后一次只读重测成功（11.730 秒），才纳入删除计划。没有放宽占用、挂载或身份检查。[plan-initial.json](../../tools/bolt/results/disk-cleanup-20261103/plan-initial.json) 保留初始结果，[du-06-retry.json](../../tools/bolt/results/disk-cleanup-20261103/du-06-retry.json) 记录重测，[plan.json](../../tools/bolt/results/disk-cleanup-20261103/plan.json) 为执行计划。

清单读取遭遇明显磁盘 I/O 等待。仅将本任务准备进程的 ionice 从 idle 改为 best-effort 7，再改为 best-effort 4，nice 仍为 19；没有改变其他进程或系统设置。一次尝试调整已退出的自有 du 子进程返回 No such process，未重试。删除脚本用 nice 19、ionice best-effort 7。见 [io-adjustment.json](../../tools/bolt/results/disk-cleanup-20261103/io-adjustment.json)。

## 3. 图形认证与实际命令

沿用 [43号§13](43_debuginfo_symbols.md#13-安装实测续跑三2026-11-02) 的 zenity + sudo -A：清理 LD/GTK/GIO 相关环境变量；同一次 sudo 内最多三次弹窗；取消立即停止后续弹窗。实际仅调用一次 sudo、弹窗一次、第一次提交通过。密码未保存或打印；仅记录次数、时间和提交/取消状态。

执行前打印完整 POSIX sh 脚本与 SHA，并通过 `/bin/sh -n`；内嵌 Python 语法检查通过。删除目标集合为表中 10 个绝对路径，所有 rm 均使用此集合的单个元素。

|脚本|SHA256|
|---|---|
|[root-delete.sh](../../tools/bolt/results/disk-cleanup-20261103/root-delete.sh)|`c001f27cdb73e8d387880cd073afdd3a691daea878f2e8f95d489f38bfec6ef2`|
|[askpass.sh](../../tools/bolt/results/disk-cleanup-20261103/askpass.sh)|`01448534c7f7abe6c6c0f094362164b0111e70bdd9435359d2bb278e8280c974`|

唯一认证调用（E 为本证据目录的绝对路径）：

```sh
SUDO_ASKPASS="$E/askpass.sh" sudo -A -k /bin/sh "$E/root-delete.sh"
```

第 1–5 项找到 root 属主且 UID 1000 不可写的目录，由该授权脚本以 root 删除。第 6–10 项用 setpriv 降为 UID/GID 1000 后删除，未使用 root 删除。每条命令原文：

```text
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/final-20261103/toolchain-rehearsal/gbs-root
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/final-20261103/basedev-rehearsal/gbs-root
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/final-20261103/basedev-rehearsal/retry-02/gbs-root
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/second-review-20261104/toolchain-rehearsal/gbs-root
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/second-review-20261104/basedev-rehearsal/gbs-root
setpriv --reuid=1000 --regid=1000 --init-groups rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/archive-index-fix-rpm-20260923
setpriv --reuid=1000 --regid=1000 --init-groups rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-rebind-20260923
setpriv --reuid=1000 --regid=1000 --init-groups rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/static-native-conversion-20260924
setpriv --reuid=1000 --regid=1000 --init-groups rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/toolchain-hybrid-trial
setpriv --reuid=1000 --regid=1000 --init-groups rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/hybrid-trial-20260922
```

认证记录：

```text
2026-11-03T16:31:25+08:00 attempt=1 opened
2026-11-03T16:38:49+08:00 attempt=1 submitted
```

sudo 返回 0。窗口启动有 IBUS 连接 warning，但认证成功；原文见 [sudo.stderr](../../tools/bolt/results/disk-cleanup-20261103/sudo.stderr)。删除命令输出保存在 `delete-NN-root.log` / `delete-NN-ordinary.log`，均为空且 rc=0。[sudo-result.json](../../tools/bolt/results/disk-cleanup-20261103/sudo-result.json)、[execution.log](../../tools/bolt/results/disk-cleanup-20261103/execution.log) 保留原始结果。

## 4. df 与实际释放量

删除窗口：2026-11-03T16:38:49.906401+08:00 至 2026-11-03T16:42:33.358684+08:00。以下来自每次 `df -B1 -T <对应父目录>`；所有目标都在 `/dev/sda1`，挂载点 `/home`。

删除前：

```text
Filesystem     Type     1B-blocks          Used    Available Use% Mounted on
/dev/sda1      ext4 1967844950016 1715590991872 152217346048  92% /home
```

删除后：

```text
Filesystem     Type     1B-blocks          Used    Available Use% Mounted on
/dev/sda1      ext4 1967844950016 1582608633856 285199704064  85% /home
```

执行窗口 df 差值：`285199704064 - 152217346048 = 132982358016` 字节，约 **123.849 GiB**。逐项增量见第 1 节，不把 du 大小当作 df 释放量。

df 是整个文件系统的观测，可能包含其他进程在窗口内的写入。清单开始时的 df 另存 [df-before.json](../../tools/bolt/results/disk-cleanup-20261103/df-before.json)，不混作删除执行前的值。删除后再次只读核对时，可用空间已随其他活动变化，故另列时间和原文：

时间：2026-11-03T16:43:41.388261+08:00。

```text
Filesystem     Type     1B-blocks          Used    Available Use% Mounted on
/dev/sda1      ext4 1967844950016 1584822386688 282985951232  85% /home
```

## 5. 删除后保护检查与结束记录

10 个路径均不存在。各父目录中除批准路径外的全部直接条目，其名称、inode、设备、类型/权限、uid/gid、软链接目标，以及普通文件大小和 mtime 与删除前一致；目录大小/mtime 不比较，因为删除批准的子目录会自然改变它们。此检查不是对所有保留目录内容重新计算哈希。

五个演练父目录的 `evidence`、`export`、`gbs-driver`、`tmp`、启动/控制脚本和 JSON 均保留；父目录 `W/temp` 的其他条目全部保留。额外确认认证 products、baseline/revised-products、perf-runtime、GBS 配置、PGO 目录、full-20261030 和两处源码工作区仍存在。详见 [parent-before-final.json](../../tools/bolt/results/disk-cleanup-20261103/parent-before-final.json)、[final-verification.json](../../tools/bolt/results/disk-cleanup-20261103/final-verification.json)。

日志末行原文：

```text
2026-11-03T16:42:33.367823+08:00 DISK_CLEANUP FINISHED status=ok
```

**结论：批准范围内 10/10 删除完成，0 跳过；其他目录保留。**
