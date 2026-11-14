# 98号：批准目录清理与96号重放准入

**清理PASS：批准的20项全部删除，0项跳过。96号真实输入重放SKIPPED：存在另一项目GBS重构建，且MemAvailable低于20GiB；未取锁、不等待、不重试、未运行重放、未回退sandbox。**

删除前占块合计 **173.902 GiB**；从第一项删除前到最后一项删除后，df可用净增 **173.548 GiB**。清理完成核对时可用 **197.404 GiB**；最终记录 **196.018 GiB**（2026-11-14T05:38:10.730846-08:00）。共享文件系统期间仍有其他写入，df变化不等于目录占块，具体差额没有逐项归因。97号“约199GiB”是按当时df的预测，不是本轮保证值。

| 步骤 | 结论 |
|---|---|
|批准清单与97核对|18个A＋2个指定B，20/20完全相符|
|删除前检查|20项大小与97逐字节数相等，偏差0%；无可见打开句柄/锁文件/内部挂载|
|删除|20/20成功，普通用户、nice19、IO idle；无通配符|
|原件与父目录核对|368项原件/工具检查通过，250个保留兄弟条目通过|
|96重放|SKIPPED；无产品实物PASS/FAIL结果，未触发回退条件|

[全部证据raw索引](../../tools/bolt/results/disk-cleanup-20261114/delete/RAW_LINKS.md)、[汇总JSON](../../tools/bolt/results/disk-cleanup-20261114/delete/summary.json)。

## 1. 授权、预检与一次准备修正

按2026-11-14授权，只处理97号A-list的18项和B-list中的qb-1221204-1221207、qb-1223601-1223602。98清单与97表格、inventory分区逐项集合核对；路径没有增减、没有用通配符展开删除目标。[批准清单](../../tools/bolt/results/disk-cleanup-20261114/delete/approved-paths.json)。

每项核对：真实目录、非软链接、realpath精确匹配、du占块与97相差不超过5%，并记录设备/inode；检查lsof（含cwd/root/mmap）、锁文件名称、lslocks、findmnt。所有偏差实为0。删除前再次检查inode、占用、持锁和挂载；所有查询成功。普通用户视图有权限边界，没有宣称完成root不可见进程的特权审计，也没有使用sudo。

原件检查使用97号retained-rpm-sources.json和dwarf-retained-inputs.json列出的路径，历史字节大小来自97使用的74/67原身份清单；包括72个RPM、264个.debug原件。十个调试输入和二十个old/new归档按97 replay-assets-current.json核对大小。两个平台工具另核对存在性；97对它们没有登记历史字节大小，本轮记录181072和251728字节，前后相同，不冒充已经与97未记录的大小比较。

首次准备脚本错误假定全部368项都有历史大小，在两个辅助工具处expected_bytes=None，误把18个A标SKIPPED；336个RPM/DWARF和30个重放输入/产物实际全部通过。**首次未执行删除**。按长期准备错误可修正一次规则，辅助工具沿用97的存在性判定，所有原始数据文件仍严格比较历史大小；重新完整预检20项通过。不改历史97结果，也未放宽任何真实原件大小差异。[原始误判](../../tools/bolt/results/disk-cleanup-20261114/delete/originals-before.json)、[修正说明](../../tools/bolt/results/disk-cleanup-20261114/delete/preparation-error.json)、[diff](../../tools/bolt/results/disk-cleanup-20261114/delete/preflight-preparation-fix.diff)、[最终预检](../../tools/bolt/results/disk-cleanup-20261114/delete/check02/preflight.json)。

删除前find逐项生成相对路径、大小、mtime和类型的gzip清单，20份均小于10MB，全部提交；没有只留本地的大清单。[清单索引及SHA](../../tools/bolt/results/disk-cleanup-20261114/delete/listings-index.json)。check02保留重跑记录；顶层listings是正式20份，原先19/20清单逐SHA相同才复用，没有覆盖不同结果。

## 2. 逐项结果

路径均相对W/temp。占块是被删目录的测量量；df增加是该项执行前后的实际观测，可能受其他写入影响，不能混同。

|序号|路径|删除前占块GiB|该项df增加GiB|结果|证据|
|---|---|---:|---:|---|---|
| 1 | qb-1226850-1226851/member-check | 34.550 | 34.536 | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-01.json) |
| 2 | qb-1226850-1226851/source-audit | 0.001 | 0.001 | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-02.json) |
| 3 | dwarf-check-20261106 | 29.886 | 29.869 | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-03.json) |
| 4 | local-full-r6-20261111-compare/toolchain/payload | 24.892 | 24.891 | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-04.json) |
| 5 | local-full-r6-20261111-compare/basedev/payload | 1.569 | 1.569 | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-05.json) |
| 6 | qb79-local-resume-20261112/toolchain/payload | 24.892 | 24.861 | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-06.json) |
| 7 | qb79-local-resume2-20261112/basedev/payload | 1.569 | 1.569 | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-07.json) |
| 8 | qb79-source-resume2-20261112 | 0.188 | 0.187 | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-08.json) |
| 9 | fifth-review-20261111/rerun3/debug-conversion-00/retained-cleanup | 4.100 | 4.099 | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-09.json) |
| 10 | fifth-review-20261111/rerun4/debug-conversion-01/retained-cleanup | 2.624 | 2.624 | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-10.json) |
| 11 | fifth-review-20261111/rerun4/debug-conversion-02/retained-cleanup | 2.926 | 2.926 | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-11.json) |
| 12 | fifth-review-20261111/rerun4/debug-conversion-03/retained-cleanup | 3.090 | 3.090 | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-12.json) |
| 13 | fifth-review-20261111/rerun4/debug-conversion-04/retained-cleanup | 2.530 | 2.525 | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-13.json) |
| 14 | fifth-review-20261111/rerun4/debug-conversion-05/retained-cleanup | 1.986 | 1.986 | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-14.json) |
| 15 | fifth-review-20261111/rerun4/debug-conversion-06/retained-cleanup | 2.099 | 2.099 | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-15.json) |
| 16 | fifth-review-20261111/rerun4/debug-conversion-07/retained-cleanup | 1.687 | 1.687 | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-16.json) |
| 17 | fifth-review-20261111/rerun4/debug-conversion-08/retained-cleanup | 1.536 | 1.536 | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-17.json) |
| 18 | fifth-review-20261111/rerun4/debug-conversion-09/retained-cleanup | 1.597 | 1.593 | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-18.json) |
| 19 | qb-1221204-1221207 | 16.089 | 16.088 | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-19.json) |
| 20 | qb-1223601-1223602 | 16.090 | 16.062 | 删除 | [原文](../../tools/bolt/results/disk-cleanup-20261114/delete/item-20.json) |

每项均使用普通用户执行下列明确argv，额外使用one-file-system保护；没有删除父目录，没有重试rm：
~~~sh
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/qb-1226850-1226851/member-check
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/qb-1226850-1226851/source-audit
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/dwarf-check-20261106
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-compare/toolchain/payload
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-compare/basedev/payload
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/qb79-local-resume-20261112/toolchain/payload
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/qb79-local-resume2-20261112/basedev/payload
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/qb79-source-resume2-20261112
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/fifth-review-20261111/rerun3/debug-conversion-00/retained-cleanup
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/fifth-review-20261111/rerun4/debug-conversion-01/retained-cleanup
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/fifth-review-20261111/rerun4/debug-conversion-02/retained-cleanup
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/fifth-review-20261111/rerun4/debug-conversion-03/retained-cleanup
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/fifth-review-20261111/rerun4/debug-conversion-04/retained-cleanup
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/fifth-review-20261111/rerun4/debug-conversion-05/retained-cleanup
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/fifth-review-20261111/rerun4/debug-conversion-06/retained-cleanup
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/fifth-review-20261111/rerun4/debug-conversion-07/retained-cleanup
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/fifth-review-20261111/rerun4/debug-conversion-08/retained-cleanup
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/fifth-review-20261111/rerun4/debug-conversion-09/retained-cleanup
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/qb-1221204-1221207
rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/qb-1223601-1223602
~~~

每项原始df、rm返回码/stdout/stderr、即时占用核对、inode检查及结束时间都在item-01至item-20.json。保留了local-full-r6-20261111-compare/toolchain/dwarf-proofs、各父目录的已发布结果、fifth-review的old/new/archives。B其他项和C保留范围未列入任何删除命令。

## 3. 删除后保护检查

20个批准路径全部不存在。368项检查全部通过：336个RPM/DWARF原件和30个重放输入/产物仍符合97所用大小；2工具前后大小相同。父目录中的250个非目标兄弟条目仍存在、inode一致；文件大小也一致，目录不把内部内容大小当成单文件大小。[完整postcheck](../../tools/bolt/results/disk-cleanup-20261114/delete/postcheck.json)。

|关键保留位置|存在性|大小核对GiB／抽查|
|---|---|---|
| deleted-repo-backup-20261105 | 存在 | 91.294；与97相同 |
| local-full-r6-20261111-materials | 存在 | 0.707；与97相同 |
| qb-1226850-1226851/1226850 | 存在 | 5.897；与97相同 |
| qb-1226850-1226851/1226851 | 存在 | 1.863；与97相同 |
| qb-1225393-1225395 | 存在 | 18.007；与97相同 |
| night-20261103 | 存在 | Verified original RPM/DWARF/tool files individually; full root du not repeated |
| night-20261105 | 存在 | Verified original RPM/DWARF/tool files individually; full root du not repeated |
| fifth-review-20261111/rerun3/debug-inputs | 存在 | 1.983；与97相同 |
| tu-inputs-restored-20261106 | 存在 | 0.632；与97相同 |
| pgo-profiles-keep-20261102 | 存在 | 0.744；与97相同 |

night-20261103的T/D evidence分别34537472/12144640 B，night-20261105/toolchain/evidence为31604736 B，均与97相同；未重新扫描巨大构建根全量大小。[补充抽查](../../tools/bolt/results/disk-cleanup-20261114/delete/night-root-samples-after.json)。保留原件没有重新全量哈希；本任务要求的是存在性与大小抽查，不冒充内容重新认证。

清理完成df：
~~~text
Filesystem         1B-blocks          Used    Available Use% Mounted on
/dev/sda1      1967844950016 1655846887424 211961450496  89% /home
~~~

最终df（2026-11-14T05:38:10.730846-08:00）：
~~~text
Filesystem         1B-blocks          Used    Available Use% Mounted on
/dev/sda1      1967844950016 1657335390208 210472947712  89% /home
~~~

## 4. 96号重放：SKIPPED

准入时间：2026-11-14T05:34:27.632615-08:00；仅检查一次，不等待、不重试。

|条件|观测|结果|
|---|---|---|
|无其他gbs/rpmbuild/ninja/llvm-bolt|gbs PID 126249，m1-ffmpeg-a32-20261114-fix1.scope|不满足|
|/home≥30GiB|210794860544 B（196.318 GiB）|满足|
|MemAvailable≥20GiB|21313306624 B（19.850 GiB）；阈值21474836480 B|不满足|
|共享锁立即可得|其他条件已失败，未尝试|NOT ATTEMPTED|

[准入原文](../../tools/bolt/results/disk-cleanup-20261114/delete/replay-admission.json)。进程属于另一项目llvm_autofdo_bolt_agent；只读取准入所需/proc信息，没有进入它的构建目录、发信号或干预。未启动16GiB重放服务，也未执行450归档、10调试归档或3853成员转换比较。此前119/119测试不能替代本次未运行的真实重放。

本次没有实物差异或新增拒绝，没有触发“b0c1732c用lease退回ecb2dec7”的条件；**未访问或修改sandbox/Gerrit/QB**。按96已记录状态，sandbox仍领先PS3一个提交，本任务没有新的远端SHA观测。真实输入重放PASS之前不得触发QB。

## 5. 资源、阅读范围和结束记录

清理、检查和交付串行使用llvm-task98-cleanup-20261114用户服务：MemoryMax4GiB、swap0、CPU400%、Nice19、IO idle。未OOM。16GiB/90分钟重放资源未使用。[资源记录](../../tools/bolt/results/disk-cleanup-20261114/delete/resource-final.json)。

读过：97分类、分区和原件清单；96续二及STATUS长期规则；74/67原身份大小记录；78驱动和census脚本（只读，为可能的重放准备）；批准路径的元数据与删除清单；进程、锁、挂载、df及meminfo。未运行产品转换、BOLT或构建；没有QB/Gerrit查询；未读取另一项目目录内容；未修改LLVM代码或分支；没有删除批准清单以外的历史路径。

本轮实际STOP：无。首次原件检查的脚本误标SKIPPED及全部原文保留，已通过一次准备修正闭合；重放SKIPPED是准入结果，不是产品FAIL。

~~~text
98步骤1 已结束 2026-11-14T05:28:49.883519-08:00 status=PASS
98步骤2 已结束 2026-11-14T05:33:40.420436-08:00 status=PASS
98步骤3 已结束 2026-11-14T05:33:42.600273-08:00 status=PASS
98步骤4准入 已结束 2026-11-14T05:34:27.632615-08:00 status=SKIPPED
~~~

98 已结束 2026-11-14T05:38:10.730846-08:00 status=PASS cleanup=20/20 replay=SKIPPED
