# 66：清理与 QB 同快照重建启动准备（2026-11-05）

本轮只执行用户明确授权的清理。qb_analysis整体删除；备份精简因恢复条件或普通用户权限不足保留；65号瘦身仅删除历史SHA与本次SHA相同的精确候选文件。没有扩大范围、修改LLVM源码或夜间入口。

证据：`tools/bolt/results/disk-cleanup-20261105c/`。W为`/home/linhao/Toolchain/development/llvm-optimize`。df差值是该时间窗口整个/home文件系统的变化，可能含其他进程写入，不冒称精确的单目录块释放量。

## 1. 删除 qb_analysis

用户明确豁免逐仓库源码保全；本轮只登记，不导出patch或bundle。顶层清单及du见inventory.json，全部仓库路径/HEAD/未推送候选见repositories.json。未推送按本地remote-tracking refs统计；缺失或陈旧refs会高估，不能当成远端实际未发布的证明。
发现253个仓库；du原文：
```text
178934099968	/home/linhao/qb_analysis
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-transition-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-transition-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-transition-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-C1-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-C1-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-C1-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-bootstrap-coreutils-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-bootstrap-coreutils-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-bootstrap-coreutils-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-C2-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-C2-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-C2-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-B-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-B-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-B-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-bootstrap-coreutils-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-bootstrap-coreutils-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-bootstrap-coreutils-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-C2-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-C2-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-C2-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-A-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-A-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-A-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-A-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-A-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-A-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-C1-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-C1-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-C1-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-transition-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-transition-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-transition-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-B-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-B-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work4/gbs-B-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-fixed1-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-fixed1-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-fixed1-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-fixed2-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-fixed2-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-fixed2-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-fixed2-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-fixed2-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-fixed2-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/four-package-work/gbs-order-CFW-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/four-package-work/gbs-order-CFW-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/four-package-work/gbs-order-CFW-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-control-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-control-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-control-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-compat-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-compat-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-compat-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-control-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-control-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-control-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-supplement-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-supplement-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-supplement-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-compat-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-compat-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-compat-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/gbs-CFWT-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/gbs-CFWT-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/gbs-CFWT-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/gbs-WFCT-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/gbs-WFCT-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/gbs-WFCT-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/fixture-armv7l-old/scratch.armv7l.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/fixture-armv7l-old/scratch.armv7l.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/fixture-armv7l-old/scratch.armv7l.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/fixture-armv7l-old/scratch.armv7l.0/tmp/tmp.qAP1387081': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/gbs-CFWT-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/gbs-CFWT-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/gbs-CFWT-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/fixture-armv7l-new/scratch.armv7l.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/fixture-armv7l-new/scratch.armv7l.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/fixture-armv7l-new/scratch.armv7l.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/fixture-armv7l-new/scratch.armv7l.0/tmp/tmp.XXXXHDUHNj': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/fixture-x86_64-new/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/fixture-x86_64-new/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/fixture-x86_64-new/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/fixture-x86_64-new/scratch.x86_64.0/tmp/tmp.XXXXtaFcr2': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/fixture-x86_64-old/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/fixture-x86_64-old/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/fixture-x86_64-old/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round8/fixture-x86_64-old/scratch.x86_64.0/tmp/tmp.KXj1333097': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-supplement-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-supplement-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-supplement-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/c4-armv7l-old/scratch.armv7l.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/c4-armv7l-old/scratch.armv7l.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/c4-armv7l-old/scratch.armv7l.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-FWC-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-FWC-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-FWC-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/c4-armv7l-new/scratch.armv7l.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/c4-armv7l-new/scratch.armv7l.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/c4-armv7l-new/scratch.armv7l.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/c4-armv7l-new/scratch.armv7l.0/tmp/tmp.XXXXB684kJ': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/c4-armv7l-new/scratch.armv7l.0/tmp/tmp.XXXXrBD3ZJ': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/c4-x86_64-old/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/c4-x86_64-old/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/c4-x86_64-old/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-FCW-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-FCW-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-FCW-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-CFW-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-CFW-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-CFW-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-CWF-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-CWF-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-CWF-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-WFC-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-WFC-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-WFC-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-WFC-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-WFC-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-WFC-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/c4-x86_64-new/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/c4-x86_64-new/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/c4-x86_64-new/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/c4-x86_64-new/scratch.x86_64.0/tmp/tmp.XXXXM2taI5': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/c4-x86_64-new/scratch.x86_64.0/tmp/tmp.XXXXTX11ZF': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-CFW-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-CFW-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-CFW-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-WCF-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-WCF-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/round7/gbs-WCF-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/root': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-fixed1-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-fixed1-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig': Permission denied
du: cannot read directory '/home/linhao/qb_analysis/work3/gbs-fixed1-x86_64/local/BUILD-ROOTS/scratch.x86_64.0/root': Permission denied

```
沿用52号zenity + sudo -A；清理LD/GTK环境，同一次sudo最多三次弹窗，取消锁定。密码不保存、不输出。执行前打印完整root-delete.sh及SHA；源码保护已由用户豁免。只有这一部分调用sudo。

root补查：True；真实目录/realpath一致、非软链接；findmnt及所有可读/proc/*/mountinfo无挂载/overlay引用；/proc cwd/root/exe/fd/maps无占用；系统及用户活动服务未引用。完整原文见root-audit.json。

实际删除命令：
```sh
rm -rf --one-file-system -- /home/linhao/qb_analysis
```

执行原文：
```text
root precheck True process matches 0 errors 0
Filesystem         1B-blocks          Used    Available Use% Mounted on
/dev/sda1      1967844950016 1508661403648 359146934272  81% /home
Filesystem         1B-blocks          Used    Available Use% Mounted on
/dev/sda1      1967844950016 1329726283776 538082054144  72% /home
CLEANUP_QB 已结束 2026-11-05T20:12:52+08:00 status=ok reason=approved-path-removed
```
该窗口可用空间：359,146,934,272 B (334.482 GiB) → 538,082,054,144 B (501.128 GiB)；净增 178,935,119,872 B (166.646 GiB)。认证记录见auth-attempts.log；stderr保留IBUS窗口环境警告。

## 2. 精简源码备份：保留，未删除

逐组校验原SHA256SUMS中的补丁/inspection摘要，所有补丁通过git apply --numstat --allow-empty解析；检查format-patch覆盖的commit、父链、HEAD重建路径，再用64号published-llvm-refs已保存结果证明基础提交可达。根提交、非线性历史、旧测试夹具字段缺失或无法证明基础可取得的组不放行。没有重新查询或修改Gerrit。

26组中9组恢复条件通过，但目录均root:root且普通用户不可写。本任务只允许第一部分使用root删除，因此这9组也未删除；没有第二次sudo、chmod或所有权修改。其余17组保留。`backup-manifests.json`列出每个format-patch的完整commit/parents、index/worktree基准、stash父提交、Gerrit基础可取得性与原因。因原备份目录不可写，manifest保存在本次证据目录；原备份manifest/SHA256SUMS未更改，内容仍完整保留。

|备份子目录|恢复检查|基础提交|实际处理/原因|
|---|---|---|---|
|`00-source/root-5645c783`|未通过|`318908bd1b5a0ea740ec4e84169f8e7b7add60bc`|preconditions not met: no published LLVM ref object available; base availability not proven|
|`00-source/root-759fbb28`|未通过|`NONE/UNKNOWN，见逐补丁parents`|preconditions not met: 'effective_unpublished'|
|`00-source/root-e27851fd`|未通过|`c78bd91662e15479293183b6ca142282f6fbe259`|preconditions not met: no published LLVM ref object available; base availability not proven|
|`04-pgo-resource-20261102/source-D-aa70a0e3`|通过|`6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2`|root-owned non-writable backup; user permits root deletion only in part 1; no sudo in part 2|
|`05-review-round3-continue-20261012/patch-apply-check-c54a3707`|通过|`cb67996861d070d68fec2b4c623eed7d20ba2e23`|root-owned non-writable backup; user permits root deletion only in part 1; no sudo in part 2|
|`05-review-round3-continue-20261012/patch-work-617ca250`|通过|`cb67996861d070d68fec2b4c623eed7d20ba2e23`|root-owned non-writable backup; user permits root deletion only in part 1; no sudo in part 2|
|`09-archive-fix-full-build-20260927/test-package-bfd-4a09ebac`|未通过|`NONE/UNKNOWN，见逐补丁parents`|preconditions not met: root/merge commit: no single published base|
|`09-archive-fix-full-build-20260927/test-package-lld-6ad747a2`|未通过|`NONE/UNKNOWN，见逐补丁parents`|preconditions not met: root/merge commit: no single published base|
|`10-archive-followup-review-20261014/apply-check-5b6fd066`|通过|`cb67996861d070d68fec2b4c623eed7d20ba2e23`|root-owned non-writable backup; user permits root deletion only in part 1; no sudo in part 2|
|`10-archive-followup-review-20261014/submit-work-4512d286`|通过|`cb67996861d070d68fec2b4c623eed7d20ba2e23`|root-owned non-writable backup; user permits root deletion only in part 1; no sudo in part 2|
|`18-release-x86-full-build-20261013/latest-base_source-ae3cb8ab`|通过|`cb67996861d070d68fec2b4c623eed7d20ba2e23`|root-owned non-writable backup; user permits root deletion only in part 1; no sudo in part 2|
|`18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-bfd-1b27e3f6`|未通过|`NONE/UNKNOWN，见逐补丁parents`|preconditions not met: root/merge commit: no single published base|
|`18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-lld-40f1e6ad`|未通过|`NONE/UNKNOWN，见逐补丁parents`|preconditions not met: root/merge commit: no single published base|
|`19-release-attribution-20261013/patch-apply-check-6105a95d`|通过|`cb67996861d070d68fec2b4c623eed7d20ba2e23`|root-owned non-writable backup; user permits root deletion only in part 1; no sudo in part 2|
|`19-release-attribution-20261013/patch-work-45589d5e`|通过|`cb67996861d070d68fec2b4c623eed7d20ba2e23`|root-owned non-writable backup; user permits root deletion only in part 1; no sudo in part 2|
|`24-llvm-strip-alternative-20260929/test-package-bfd-03f3e641`|未通过|`NONE/UNKNOWN，见逐补丁parents`|preconditions not met: root/merge commit: no single published base|
|`24-llvm-strip-alternative-20260929/test-package-lld-c8f02f6f`|未通过|`NONE/UNKNOWN，见逐补丁parents`|preconditions not met: root/merge commit: no single published base|
|`25-llvm-strip-x86_64-20261009/continue-20261009_test-package-bfd-2ca8bd4a`|未通过|`NONE/UNKNOWN，见逐补丁parents`|preconditions not met: root/merge commit: no single published base|
|`25-llvm-strip-x86_64-20261009/continue-20261009_test-package-lld-81b277b8`|未通过|`NONE/UNKNOWN，见逐补丁parents`|preconditions not met: root/merge commit: no single published base|
|`29-llvm-hybrid-trial/root-8885f3e3`|未通过|`67619ec8bbbac7238a6cfc33a481ccfbcd12206f`|preconditions not met: patch series does not reconstruct original HEAD|
|`30-llvm-archivefix-trial/root-fd4d3568`|未通过|`67619ec8bbbac7238a6cfc33a481ccfbcd12206f`|preconditions not met: patch series does not reconstruct original HEAD|
|`32-followup-356949-ps2-message-20261014/review-work-c226bed9`|通过|`cb67996861d070d68fec2b4c623eed7d20ba2e23`|root-owned non-writable backup; user permits root deletion only in part 1; no sudo in part 2|
|`36-qb_analysis/work3_control_findutils-5ecf1d1e`|未通过|`af85ff6958d87b1fb93efbe71e24fc4aba0f5da1`|preconditions not met: non-linear patch history|
|`36-qb_analysis/work3_control_which-3a31a668`|未通过|`62589b5e2bd0b8188a5843ab85f0af386240c772`|preconditions not met: non-linear patch history|
|`36-qb_analysis/work3_coreutils-38da01e5`|未通过|`f6bee3a536aa946ad3a8401b0543bec188a5e3c9`|preconditions not met: non-linear patch history|
|`36-qb_analysis/work3_findutils-01add93a`|未通过|`af85ff6958d87b1fb93efbe71e24fc4aba0f5da1`|preconditions not met: non-linear patch history|

其他顶层_selftest、_alternates-restoration等不属于可证明安全删除的bundle/readback候选，全部保留；见backup-unclassified-top.json。

精简前后du：
```text
98026516480	/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105
98026516480	/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105
```
前后df：
```text
Filesystem         1B-blocks          Used    Available Use% Mounted on
/dev/sda1      1967844950016 1329727393792 538080944128  72% /home
Filesystem         1B-blocks          Used    Available Use% Mounted on
/dev/sda1      1967844950016 1329728311296 538080026624  72% /home
```
BACKUP_SLIM 已结束 2026-11-05T20:15:27.858523+08:00 status=skipped reason=9-eligible-but-root-owned;17-unproven;no-second-sudo

## 3. 65号精确候选瘦身

删除边界只取65号recommendation.json与suggested-files.tsv.gz，不扩展到父/同级目录。65号中没有逐文件历史SHA的目录候选保持整体原样，不能把本次现算SHA当作65号基线。已记录SHA的普通文件再核对真实路径、属主、inode/mtime稳定、当前SHA一致后，用普通用户rm -f --删除该文件；不删除空父目录，不使用sudo。

普通用户/proc及findmnt检查没有可见占用/挂载；/proc权限盲区完整保存，不宣称root级全机检查。逐文件当前SHA查询、删除命令/rc、跳过原因及每项df在slim-<目录>.json（超过1MiB的公开证据为同名.json.gz；原文件本地保留）。

|目录|删除文件数|保留候选数|df可用空间净增|结论|
|---|---:|---:|---:|---|
|`arm-source-root-probes-20261010`|494|0|12,817,043,456 B (11.937 GiB)|候选全部删除|
|`arm-archive-stage1-20261010`|215|0|6,405,808,128 B (5.966 GiB)|候选全部删除|
|`bolt-v4-20261022-cache-release`|0|540|0 B (0.000 GiB)|部分保留（历史SHA缺失）|
|`crash-probe-20261028`|18|0|2,239,483,904 B (2.086 GiB)|候选全部删除|
|`llvm-optimize-intranet-20261020`|0|169159|-737,280 B (-0.001 GiB)|部分保留（历史SHA缺失）|
|`qb-meta-switch-20261028`|0|840|-40,960 B (-0.000 GiB)|部分保留（历史SHA缺失）|

cache-release的两份解包目录、内网源码检出/导出和MLGO解包root因缺完整的65号逐文件SHA，整组保留；所有products、原始RPM、独有符号复现文件和未发布源码保持原样。

结束行原文：
```text
SLIM65 已结束 2026-11-05T20:18:11.592714+08:00 status=ok path=arm-source-root-probes-20261010 deleted=494 retained=0
SLIM65 已结束 2026-11-05T20:19:07.906566+08:00 status=ok path=arm-archive-stage1-20261010 deleted=215 retained=0
SLIM65 已结束 2026-11-05T20:19:08.013139+08:00 status=partial path=bolt-v4-20261022-cache-release deleted=0 retained=540
SLIM65 已结束 2026-11-05T20:19:23.624760+08:00 status=ok path=crash-probe-20261028 deleted=18 retained=0
SLIM65 已结束 2026-11-05T20:19:23.972856+08:00 status=partial path=llvm-optimize-intranet-20261020 deleted=0 retained=169159
SLIM65 已结束 2026-11-05T20:19:31.724397+08:00 status=partial path=qb-meta-switch-20261028 deleted=0 retained=840
SLIM65_ALL 已结束 2026-11-05T20:19:32.061080+08:00 status=partial reason=historical-SHA-missing-candidates-preserved
```

## 4. 清理结束与构建入口

前三部分全部结束后才检查98.8GiB、全新根和无其他GBS/rpmbuild运行三项条件。完整结果将于全部结束后写入63号；只使用用户指定命令，没有重试或修改入口。
```sh
/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/night-launch-20261105/launch.sh 9e39fa8a61392652bb28b75fc26216675bcad1d5 full
```

启动前可用559,488,331,776 B（521.064 GiB），新根不存在，无其他GBS/rpmbuild；指定命令仅执行一次。服务初始active/running，MemoryMax=24,482,992,128 B、swap0、CPUQuota=1200%。启动原文见launch.stdout，构建结束后的验证结果另记63号。
