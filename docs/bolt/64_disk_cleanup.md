# 64：2026-11-05 批准目录清理

批准的34个实际路径中，整项删除 29 项、未整项删除（跳过或恢复对象库）5 项；编号34、35没有操作。/home 可用空间从 118.944 GiB 变为 335.444 GiB，整个执行窗口净增加 216.500 GiB。PGO profiles 已移出并逐文件核对，保留目录及第1–3项的其他兄弟条目检查结果见下文；今晚构建未启动。

## 1. 范围与执行方式

用户明确批准本轮清单；仅清理这些精确目录，未扩展到父目录或同级目录。`targets.json`为完整路径表，34、35为保留编号。所有rm使用`rm -rf --one-file-system -- <精确路径>`。普通用户目录的rm以UID 1000执行，权限不足的目录以root执行。一次`sudo -A -k /bin/sh root-delete.sh`覆盖root补查、必要保全和删除；图形askpass沿用52号zenity方式，最多3次，取消锁定，不记录密码。

执行前打印root-delete.sh全文及SHA256：`52d66217c16dbea1576aad4c758e83c1abebeb0e0c39b0ce3a969f4081726e61`。调用器及各检查脚本SHA见executor-manifest.json。没有构建、Gerrit/sandbox推送、QB操作、权限更改或VS Code配置修改。

## 2. 检查与逐项结果

每项先核对realpath、真实目录、自身及父目录非软链接、设备/inode身份；用findmnt检查挂载及overlay，并以root补查所有可读/proc/*/mountinfo、cwd/root/exe/fd/maps及活动systemd用户服务。保全后、删除前再次检查。第2项扩大占用检查到整个oldtext-final父目录，包括VS Code。普通用户扫描的权限盲区由root补扫；没有绕过检查或卸载挂载。

|编号|路径（相对W/temp，36为绝对路径）|du GiB|RPM数|结果 / rm UID|df净增GiB|原因|
|---:|---|---:|---:|---|---:|---|
|1|`runpath-fix-20261026/gbs-root`|34.878|23|deleted / 0|33.361|all checks and repository preservation passed|
|2|`oldtext-final-20261027/gbs-root`|34.655|145|deleted / 0|34.654|all checks and repository preservation passed|
|3|`debuglink-20261028/full-20261030/gbs-root`|32.757|23|deleted / 0|31.246|all checks and repository preservation passed|
|4|`pgo-resource-20261102`|27.755|122|deleted / 0|27.755|all checks and repository preservation passed|
|5|`review-round3-continue-20261012`|26.396|0|deleted / 1000|26.395|all checks and repository preservation passed|
|6|`review-round4-20261012`|25.811|0|deleted / 1000|25.811|all checks and repository preservation passed|
|7|`archive-fix-v2-build-20260929`|11.661|0|deleted / 1000|11.661|all checks and repository preservation passed|
|8|`archive-fix-v2-20260929`|1.871|0|deleted / 1000|1.871|all checks and repository preservation passed|
|9|`archive-fix-full-build-20260927`|10.566|22|deleted / 1000|2.316|all checks and repository preservation passed|
|10|`archive-followup-review-20261014`|9.090|0|retained-object-store / 1000|9.090|原目录删除后发现第26/28/32项依赖其Git alternates对象库；从已验证副本恢复对象库，工作内容已删除，仅恢复对象库目录，未完成整项删除。未改依赖仓库配置。|
|11|`static-native-conversion-v2-20260924`|2.428|0|deleted / 1000|2.427|all checks and repository preservation passed|
|12|`static-native-conversion-v3-20260924`|1.351|0|deleted / 1000|1.351|all checks and repository preservation passed|
|13|`gbs-root-x86_64-archivefix`|13.630|166|deleted / 0|13.630|all checks and repository preservation passed|
|14|`gbs-root-release-consumer-20261014-lld`|4.557|113|deleted / 0|4.557|all checks and repository preservation passed|
|15|`gbs-root-release-consumer-20261014-bfd`|4.557|113|deleted / 0|4.557|all checks and repository preservation passed|
|16|`gbs-root-archive-consumer-bfd`|4.347|113|deleted / 0|4.347|all checks and repository preservation passed|
|17|`gbs-root-archive-consumer-lld`|4.347|113|deleted / 0|4.347|all checks and repository preservation passed|
|18|`release-x86-full-build-20261013`|16.188|0|deleted / 1000|16.005|all checks and repository preservation passed|
|19|`release-attribution-20261013`|14.101|0|deleted / 1000|14.101|all checks and repository preservation passed|
|20|`bolt-v4-20261013`|16.150|0|skipped / —|—|Git公共目录被4个清单外保留worktree依赖，整项跳过。|
|21|`bolt-v4-20261014`|1.287|0|deleted / 1000|1.287|all checks and repository preservation passed|
|22|`bolt-v4-20261015-install-rehearsal`|2.678|0|deleted / 0|2.678|all checks and repository preservation passed|
|23|`bolt-v4-20261016-source-order`|2.001|0|deleted / 0|2.001|all checks and repository preservation passed|
|24|`llvm-strip-alternative-20260929`|9.642|7|deleted / 1000|9.642|all checks and repository preservation passed|
|25|`llvm-strip-x86_64-20261009`|9.473|22|deleted / 1000|1.224|all checks and repository preservation passed|
|26|`hybrid-sandbox-20261019`|5.663|1|skipped / —|—|依赖第10项alternates对象库，删除该对象库后Git检查失败；对象库已恢复且读取PASS，本项保持跳过，不重试删除。|
|27|`hybrid-local-20261023`|5.595|168|deleted / 1000|5.595|all checks and repository preservation passed|
|28|`hybrid-link-20261015`|5.338|0|skipped / —|—|依赖第10项alternates对象库，删除该对象库后Git检查失败；对象库已恢复且读取PASS，本项保持跳过，不重试删除。|
|29|`llvm-hybrid-trial`|2.419|0|deleted / 1000|2.419|all checks and repository preservation passed|
|30|`llvm-archivefix-trial`|2.419|0|deleted / 1000|2.419|all checks and repository preservation passed|
|31|`qb-full-compare-20261105`|20.995|0|deleted / 1000|20.995|all checks and repository preservation passed|
|32|`followup-356949-ps2-message-20261014`|2.439|0|deleted / 1000|2.438|all checks and repository preservation passed|
|33|`gnu-strip-merged-check-20261014`|1.060|0|deleted / 1000|1.060|all checks and repository preservation passed|
|36|`/home/linhao/qb_analysis`|166.646|5009|skipped / —|—|检查脚本对bare仓库acl.git运行stash list，命令不适用；已完成4/253仓库的保全，其余检查未完成。整目录保留，不做第二次sudo。|

34、35：保留编号，未检查、未删除任何路径。du为逐项扫描值，可存在硬链接重复计数；df差值是该时间窗口实际可用空间变化，包含并发系统写入，不能视为孤立文件大小。第10行是原删除窗口，尚未扣除随后恢复的对象库；全任务净值已包含恢复及备份新增占用。顶层列表、RPM名称/字节数/SHA256及普通用户权限错误在path-NN.json；root补查在execution-NN/complete-inventory.json。

## 3. 源码保护

逐仓库记录用户指定的`git log --branches --tags --not --remotes`，额外计入detached HEAD。部分临时克隆缺remote-tracking refs，原查询会把大量已发布LLVM历史也列出（部分克隆约27万条）。保留原输出gzip后，另通过BatchMode SSH只读查询Gerrit实际heads/tags，并只用本仓库确实存在的已发布对象做排除；没有fetch或改原仓库的ref/remote。查询原文见published-llvm-refs.stdout，逐仓库原始结果见git-inspection/。

发现未发布提交、stash或已跟踪改动时，保存完整format-patch、二进制staged/unstaged diff、stash（含untracked部分）及standalone bundle。bundle在新建空仓库中verify/unbundle，并逐个确认commit可读；补丁通过git apply --numstat解析。自测覆盖1个未发布提交、2份stash、同时存在暂存/未暂存改动。保全位置为W/temp/deleted-repo-backup-20261105/，每份有SHA256SUMS；这些保全和测试夹具保留。收尾du为98,026,516,480 B（91.294 GiB），包含完整bundle以及用于空仓库读回验证的对象副本；见backup-du.json。

|原目录编号|仓库|未发布提交|stash|tracked dirty|保全 / 判定|
|---:|---|---:|---:|---|---|
|4|`/home/linhao/Toolchain/development/llvm-optimize/temp/pgo-resource-20261102/source-D`|2|0|False|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/04-pgo-resource-20261102/source-D-aa70a0e3|
|5|`/home/linhao/Toolchain/development/llvm-optimize/temp/review-round3-continue-20261012/patch-apply-check`|0|0|True|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-apply-check-c54a3707|
|5|`/home/linhao/Toolchain/development/llvm-optimize/temp/review-round3-continue-20261012/patch-work`|2|0|False|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/05-review-round3-continue-20261012/patch-work-617ca250|
|9|`/home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-full-build-20260927/test-package-bfd`|1|0|False|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-bfd-4a09ebac|
|9|`/home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-full-build-20260927/test-package-lld`|1|0|False|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/09-archive-fix-full-build-20260927/test-package-lld-6ad747a2|
|10|`/home/linhao/Toolchain/development/llvm-optimize/temp/archive-followup-review-20261014/apply-check`|1|0|True|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/10-archive-followup-review-20261014/apply-check-5b6fd066|
|10|`/home/linhao/Toolchain/development/llvm-optimize/temp/archive-followup-review-20261014/submit-work`|2|0|False|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/10-archive-followup-review-20261014/submit-work-4512d286|
|18|`/home/linhao/Toolchain/development/llvm-optimize/temp/release-x86-full-build-20261013/latest-base/source`|2|0|False|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/18-release-x86-full-build-20261013/latest-base_source-ae3cb8ab|
|18|`/home/linhao/Toolchain/development/llvm-optimize/temp/release-x86-full-build-20261013/round2-eight-output-proof/test-package-bfd`|2|0|False|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-bfd-1b27e3f6|
|18|`/home/linhao/Toolchain/development/llvm-optimize/temp/release-x86-full-build-20261013/round2-eight-output-proof/test-package-lld`|2|0|False|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/18-release-x86-full-build-20261013/round2-eight-output-proof_test-package-lld-40f1e6ad|
|19|`/home/linhao/Toolchain/development/llvm-optimize/temp/release-attribution-20261013/patch-apply-check`|0|0|True|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/19-release-attribution-20261013/patch-apply-check-6105a95d|
|19|`/home/linhao/Toolchain/development/llvm-optimize/temp/release-attribution-20261013/patch-work`|2|0|False|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/19-release-attribution-20261013/patch-work-45589d5e|
|20|`/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source`|未判定|0|False|external live worktree uses common git directory|
|24|`/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-strip-alternative-20260929/test-package-bfd`|1|0|False|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-bfd-03f3e641|
|24|`/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-strip-alternative-20260929/test-package-lld`|1|0|False|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/24-llvm-strip-alternative-20260929/test-package-lld-c8f02f6f|
|25|`/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-strip-x86_64-20261009/continue-20261009/test-package-bfd`|1|0|False|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-bfd-2ca8bd4a|
|25|`/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-strip-x86_64-20261009/continue-20261009/test-package-lld`|1|0|False|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/25-llvm-strip-x86_64-20261009/continue-20261009_test-package-lld-81b277b8|
|29|`/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-hybrid-trial`|1|0|True|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/29-llvm-hybrid-trial/root-8885f3e3|
|30|`/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-archivefix-trial`|1|0|True|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/30-llvm-archivefix-trial/root-fd4d3568|
|32|`/home/linhao/Toolchain/development/llvm-optimize/temp/followup-356949-ps2-message-20261014/review-work`|2|0|False|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/32-followup-356949-ps2-message-20261014/review-work-c226bed9|
|36|`/home/linhao/qb_analysis/work3/control/findutils`|5|0|False|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/36-qb_analysis/work3_control_findutils-5ecf1d1e|
|36|`/home/linhao/qb_analysis/work3/control/which`|12|0|False|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/36-qb_analysis/work3_control_which-3a31a668|
|36|`/home/linhao/qb_analysis/work3/coreutils`|4|0|False|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/36-qb_analysis/work3_coreutils-38da01e5|
|36|`/home/linhao/qb_analysis/work3/findutils`|5|0|False|/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105/36-qb_analysis/work3_findutils-01add93a|

第20项内的Git公共目录仍服务于清单外、必须保留的worktree，因此整项跳过。具体依赖路径见该项repositories.json；未移动或修复任何worktree。无Git仓库的目录记录为空列表；检查/保全失败项不删除。

## 4. PGO profiles 与保留项

`full/stage-A/profiles`同文件系统rename到`W/temp/pgo-profiles-keep-20261102/`。24文件共798,841,688 B；移动前、移动后、删除前以及最终SHA清单均保存，最终一致=True。

第1–3项父目录其他条目逐项元数据一致=True；用户列出的12个保护目录身份一致=True；依赖主仓库的保留源码worktree可读=True；今晚完整构建未启动=True。完整路径/结果见protected-before/after.json、parents-before/after.json、protected-source-heads.json及postcheck.json。

## 5. df、认证与结束记录

删除前：

```text
Filesystem         1B-blocks          Used    Available Use% Mounted on
/dev/sda1      1967844950016 1740092968960 127715368960  94% /home
```

最终：

```text
Filesystem         1B-blocks          Used    Available Use% Mounted on
/dev/sda1      1967844950016 1507627786240 360180551680  81% /home
```

`auth-attempts.log`：

```text
2026-11-05T15:30:00+08:00 attempt=1 opened
2026-11-05T15:32:51+08:00 attempt=1 submitted
```

`root-invocation.json`：

```text
{
  "time_start": "2026-11-05T15:30:00.924913+08:00",
  "time_end": "2026-11-05T18:03:54.302090+08:00",
  "argv": [
    "sudo",
    "-A",
    "-k",
    "/bin/sh",
    "/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/disk-cleanup-20261105b/root-delete.sh"
  ],
  "rc": 0
}
```

最后的执行记录：

```text
2026-11-05T18:03:45.356256+08:00 REPOSITORY_BACKUP 36 /home/linhao/qb_analysis/work3/control/findutils
2026-11-05T18:03:48.814854+08:00 REPOSITORY_BACKUP 36 /home/linhao/qb_analysis/work3/control/which
2026-11-05T18:03:50.181813+08:00 REPOSITORY_BACKUP 36 /home/linhao/qb_analysis/work3/coreutils
2026-11-05T18:03:51.535137+08:00 REPOSITORY_BACKUP 36 /home/linhao/qb_analysis/work3/findutils
2026-11-05T18:03:54.204049+08:00 REPOSITORY_BACKUP 36 /home/linhao/qb_analysis/work3/four-package-work/inventory-git/acl.git
2026-11-05T18:03:54.275537+08:00 SKIP 36 (PosixPath('/home/linhao/qb_analysis/work3/four-package-work/inventory-git/acl.git'), 'stash', {'argv': ['stash', 'list', '--format=%H%x09%gd%x09%gs'], 'rc': 128, 'stdout': '', 'stderr': 'fatal: this operation must be run in a work tree\n'})
CLEANUP_PATH 已结束 2026-11-05T18:03:54.284260+08:00 number=36 status=skipped
CLEANUP 已结束 2026-11-05T18:03:54.284282+08:00 status=partial deleted=30 skipped=4
```

证据目录：[`tools/bolt/results/disk-cleanup-20261105b/`](../../tools/bolt/results/disk-cleanup-20261105b/)。未承诺可释放的du总量等于df增量：源码保全新增占用、共享硬链接及系统活动均会影响净值。

## 6. alternates检查缺口与恢复记录

本轮预检查识别了worktree依赖，但漏查Git objects/info/alternates的反向依赖。第10项删除后，第26和28项在Git查询中报unable to normalize alternate object path及fatal: bad object 2020.06-alpha，因此执行器跳过这两项。后续只读补查11条alternates，唯一缺失的对象库是第10项submit-work/.git/objects；第32项的review-work也直接依赖它。这个问题由本轮检查遗漏造成，不归因于用户或原仓库。

从第10项已经在空仓库验证通过的standalone bundle读回副本中复制objects到新的暂存目录；逐文件核对SHA后，原子rename到原对象库路径。没有改依赖仓库配置，没有覆盖已有文件，没有第二次sudo，也没有额外删除。第10项的工作内容已删除，但对象库现已恢复，因此最终统计不把第10项算作整项删除。第26/28项保持跳过，不重试删除。

恢复对象库：`/home/linhao/Toolchain/development/llvm-optimize/temp/archive-followup-review-20261014/submit-work/.git/objects`；4,556,627,020 B，3个文件，来源与恢复副本SHA全部相同。详见alternates-restoration.json及restore_alternates.py。

|受影响仓库|恢复后原Git查询、HEAD tree及status|
|---|---|
|`/home/linhao/Toolchain/development/llvm-optimize/temp/hybrid-sandbox-20261019/prepare`|PASS|
|`/home/linhao/Toolchain/development/llvm-optimize/temp/hybrid-sandbox-20261019/remote-check`|PASS|
|`/home/linhao/Toolchain/development/llvm-optimize/temp/hybrid-link-20261015/source`|PASS|
|`/home/linhao/Toolchain/development/llvm-optimize/temp/hybrid-link-20261015/apply-check`|PASS|
|`/home/linhao/Toolchain/development/llvm-optimize/temp/followup-356949-ps2-message-20261014/review-work`|PASS|

全部11条已知alternates路径恢复存在，六个明确保留源码仓库在发现问题时HEAD对象检查均通过。后续清理应先扫描完整的worktree及alternates依赖图，并在任何对象库删除之前完成所有消费者的保全；不能仅按目录顺序边保全边删除。原执行器日志和失败原文保留，未改写成成功。最终路径状态以postcheck.json为准。

## 7. 第36项的bare仓库检查中止

第36项root补扫134处权限盲区成功，实际du=178,935,205,888 B，253个Git仓库、5,009个RPM。执行器完成前4个仓库的保全后，对第5个仓库`work3/four-package-work/inventory-git/acl.git`执行`git stash list`，返回128：

```text
fatal: this operation must be run in a work tree
```

只读复核 `git --git-dir=... rev-parse --is-bare-repository` 返回0和 `true`（bare-repository-confirmation.json）。这是检查器未区分bare仓库造成的失败，不证明该仓库损坏、存在stash或未发布改动。没有继续检查余下仓库，没有删除qb_analysis。下一次应对bare仓库直接检查refs/stash及其reflog，并将工作区改动检查记为不适用；本轮不绕过检查，不增加第二次sudo调用。已完成的4份保全及全部失败原文保留在execution-36/和deleted-repo-backup-20261105/。

最终结果为部分完成：整项删除29项，第10项仅删除工作内容后恢复对象库，第20/26/28/36项保留；34/35无操作。没有启动night-launch-20261105。

最终收尾记录（区别于对象库恢复前的原始删除计数）：

```text
CLEANUP_FINAL 已结束 2026-11-05T18:12:58.872411+08:00 status=partial fully_deleted=29 object_store_retained=1 skipped=4 night_not_started=true
```
