# 61：批准的两处磁盘清理（2026-11-05）

两处批准目录均已删除，其余目录没有删除。删除窗口内 `/home` 可用空间由 49,522,663,424 B 增至 82,764,091,392 B（77.080 GiB），净增加 30.958 GiB；df 是全文件系统读数，含同时发生的系统写入。stage-A 的 evidence、profiles、objects 等兄弟条目及 attribution 的其他条目，经父目录清单核对保持一致。

## 授权与检查

用户只批准 `W/temp/attribution-20261105/payload` 和 `W/temp/pgo-resource-20261102/full/stage-A/gbs-root`，W 为 `/home/linhao/Toolchain/development/llvm-optimize`。
两者真实目录、非软链接、父目录非软链接、realpath 匹配。findmnt 无内部挂载，lsof/fuser 无命中，活动用户服务无使用。普通用户 /proc 检查有 1427 条权限盲区；未据此直接删除，沿用52号同一次 sudo 调用补作只读检查，root检查进程命中与权限错误均为0，stage-A 所有可读 mountinfo 引用为0且无读取错误。

|目录|删除前du B|身份|结果|逐项df增加B|
|---|---:|---|---|---:|
|stage-A/gbs-root|26,444,709,888（普通用户du有3处权限盲区，是已见占用）|sudo -A|已删除|26,444,509,184|
|attribution/payload|6,958,198,784|普通用户|已删除|6,958,190,592|

为先消除普通用户的 /proc 盲区，实际执行顺序为 stage-A，再 payload。root对payload只读检查，payload的rm以普通用户执行。

## 命令与认证

执行前打印 `root-delete.sh` 全文和SHA256，`/bin/sh -n` 通过。脚本唯一可删除绝对路径为批准的stage-A/gbs-root；先检查再执行：

```sh
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/pgo-resource-20261102/full/stage-A/gbs-root
```

脚本SHA256：`b25f318f9b515096493f18862dee1bdf1c83d82dad67d5045200de843270fbe8`。
沿用52号 zenity + sudo -A，清除LD/GTK相关环境；同一次sudo最多3次弹窗，取消后不再弹。本次只调用一次sudo、弹窗一次，首次认证通过，没有记录密码。原始调用：

```sh
SUDO_ASKPASS="$E/askpass.sh" sudo -A -k /bin/sh "$E/root-delete.sh"
```

payload命令：

```sh
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/attribution-20261105/payload
```

## 原始输出及保全

```text
Filesystem         1B-blocks          Used   Available Use% Mounted on
/dev/sda1      1967844950016 1818285674496 49522663424  98% /home
Filesystem         1B-blocks          Used   Available Use% Mounted on
/dev/sda1      1967844950016 1785044246528 82764091392  96% /home
CLEANUP_STAGE_A 已结束 2026-11-05T10:08:46.027701+08:00 status=ok
CLEANUP 已结束 2026-11-05T10:09:10.393624+08:00 status=ok deleted=2
```

两个路径均不存在；`parents-before.json`与`parents-after.json`相同（目录自身mtime不参与比较，保留普通文件的size/mtime参与比较）。这不是对保留目录全部内容重新计算SHA。D根、所有products、profile和其余历史根未改。
证据：`tools/bolt/results/disk-cleanup-20261105/`，包括检查原文、脚本、认证次数、逐项df、rm返回码/耗时及父目录保全核对。清理结果：全部完成，跳过0项。
