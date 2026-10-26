# 38. W/temp 与项目构建根：只读清理建议（2026-10-26）

**本轮没有删除、移动、改权限、提权、挂载、构建或推送 Gerrit。下面均为待用户逐项批准的建议，不是执行记录。**

W 可见实占 **1011.690 GiB**，其中 W/temp **1004.114 GiB**。优先处理已完成的两轮 cache-release、hybrid、hybrid+BOLT 构建根；先保全未有同 SHA 副本的RPM、关键文件和性能运行环境。products、TU/C输入、profile、源码工作树、工具及已提交证据全部保留。

| 方案 | /home净释放估算 | /home执行后可用估算 | /var/tmp所在盘净释放估算 | 该盘执行后可用估算 |
|---|---:|---:|---:|---:|
| 稳妥：仅所列构建根/缓存 | 256.833 GiB | 405.893 GiB | 90.322 GiB | 136.768 GiB |
| 激进：再加可恢复载荷/旧解析upper | 398.888 GiB | 547.948 GiB | 136.621 GiB | 183.067 GiB |

/home 当前可用 149.060 GiB；/var/tmp 在 `/dev/nvme0n1p1` 的 `/` 文件系统，可用 46.446 GiB。**两盘不可相加。** 上表已从 /home 扣除 5.517 GiB 的先保全预算，包括所有RPM（连依赖缓存包也保守保留）。未认证重复内容的包不擅自去重；已实测同SHA或同inode的文件才计为已有副本。新副本预算按原分配块估计，复制时仍须实际校验，表中不是可立即兑现的空间承诺。

## 1. 范围、方法与盲区

- `W=/home/linhao/Toolchain/development/llvm-optimize`；`T=W/temp`；`B=/home/linhao/Toolchain/development/llvm-optimize-bolt`。所有扫描以 `nice -n 19 ionice -c3` 运行；没有获取锁或改变正在运行任务的设置。只在B写本次证据和文档。
- 实测 140 个一级目录（W 6项、temp 122项、项目名匹配或GBS候选/var/tmp 12项），另 481 个精细范围；原始 `du -sx -B1` stdout/stderr、退出码和耗时见 units.json、commands.json、subunits.json。>50 GiB父目录额外有 expand-*.stdout 一层展开。所有大小为实际分配，不是 apparent-size。
- 同一父子目录不能重复相加。**scenarios.json** 中的选定范围不重叠，用 st_dev/st_ino/st_nlink 修正跨范围硬链接；对本次两套方案修正值均为0。其他目录有外部硬链接时已单列，不能直接按独立du相加。
- 元数据遍历见到 9,713,064 个普通文件、65 条遍历错误。†为可见下界；不提权，root/ldconfig/upgrade等盲区原文保留。mtime取最新后代**普通文件**，不是目录mtime，更不是最后使用时间；未来/固定测试时间戳照录。
- 先后两次全局lsof，辅以fuser、ps、全部可读/proc/*/mountinfo和cwd/root。最终本次范围未见lsof/fuser命中，活动overlay/挂载引用0。无权限打开的FD仍是盲区；fuser目录检查不递归证明所有后代无打开文件，因此同时做全局lsof路径边界筛选。删除前必须再检查，不把本次快照当永久许可。
- 本机 fuser 首次带 `--` 返回 “No process specification given”，这是参数兼容性错误，不是无进程；已去掉该分隔符，以绝对路径重新检查。原始失败保留在 fuser.*，有效结果为 fuser-checked.* 与 fuser-final.*（退出1、stdout/stderr空）。没有据失败命令放行。
- 已只读核对GitHub：main `613fa5ee8703c14f56e0b682bf0910f639f48ec9`、bolt-v4 `4aad31b261906bc159811411181ffc9e91e02958` 与本地HEAD一致。文档出处因此已发布；不能由此推出temp中的所有二进制/日志都已备份。main中已有gbs_llvm.conf修改和未跟踪证据未动。
- 本轮发现P1–P3均不存在。P4旧upper也已不存在，旁边有root属主的preserved-from-upper；31号文档仍记P4未获批准，本轮没有找到对应后续执行记录，不推测是谁、何时删除。P4旧60.530 GiB不再计入方案。runpath-fix-20261026当前不存在；若之后创建，整目录自动保留。

## 2. 一级占用排序

完整122个temp子目录与12个/var/tmp项目目录（包括小目录）见 [top-level-du.tsv](../../tools/bolt/results/temp-cleanup-20261026/top-level-du.tsv)。下面先列W一级；temp大目录的逐项分析在第4节。没有列入方案的目录默认保留。

| W一级目录 | 实占GiB | 处理 |
|---|---:|---|
| `W/temp` | 1004.114† | 仅按第3节子范围建议，不能整删 |
| `W/llvm` | 6.891 | 保留：源码/Git/工具/已提交文档证据 |
| `W/docs` | 0.311 | 保留：源码/Git/工具/已提交文档证据 |
| `W/.git` | 0.229 | 保留：源码/Git/工具/已提交文档证据 |
| `W/tools` | 0.145 | 保留：源码/Git/工具/已提交文档证据 |
| `W/patches` | 0.000 | 保留：源码/Git/工具/已提交文档证据 |

## 3. 两套方案的精确范围（待批准）

**稳妥方案**只涉及下面5个范围；四个GBS根须先完成 preserve-before-delete.json 中的保全。绝不删除这些范围的父目录，因其中有products、source、脚本、报告和输入。

| 精确路径 | 毛占用GiB | 建议/前提 |
|---|---:|---|
| `W/temp/bolt-v4-20261022-cache-release/baseline-root` | 85.418 | 先保全未有同SHA副本的RPM/关键文件，再删除此构建根；root系统目录需另行授权sudo |
| `W/temp/bolt-v4-20261022-cache-release/revised-root` | 83.025 | 先保全未有同SHA副本的RPM/关键文件，再删除此构建根；root系统目录需另行授权sudo |
| `W/temp/hybrid-local-20261023/gbs-root` | 58.529 | 先保全未有同SHA副本的RPM/关键文件，再删除此构建根；root系统目录需另行授权sudo |
| `W/temp/bolt-on-hybrid-20261024/gbs-root` | 35.377 | 先保全未有同SHA副本的RPM/关键文件，再删除此构建根；root系统目录需另行授权sudo |
| `/var/tmp/llvm-optimize-x86-archivefix-20261013/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache` | 90.322 | 可以删除缓存；保留该树其他输入/RPM；以后重链将重新生成缓存 |

**激进方案**在稳妥基础上增加下面5项。载荷可从列明的原RPM重新解包；引用这些路径的历史脚本将不能直接重跑，须先恢复载荷。本轮不修改这些脚本。

| 精确路径 | 毛占用GiB | 恢复依据/风险 |
|---|---:|---|
| `W/temp/bolt-v4-20261016-source-order/upper-parse` | 3.243 | docs26解析实验已结束；upper-parse不是原始输入，报告/脚本/导出留在父目录；原下层保留 |
| `W/temp/toolchain-archivefix-v2-final` | 46.299 | docs35原22RPM：T/archive-fix-v2-final-20261009/rpms-docs35；原件保留 |
| `W/temp/toolchain-llvm-strip` | 46.256 | docs38的22RPM仍在gbs-root-x86_64-archivefix-v2/.../rpmbuild/RPMS/x86_64；不把它们说成67619ec8新构建 |
| `W/temp/toolchain-release-x86-20261013` | 46.256 | docs49交接树/var/tmp/llvm-optimize-x86-archivefix-20261013/.../rpmbuild/RPMS/x86_64；该树仅删缓存，RPM保留 |
| `/var/tmp/llvm-optimize-archivefix-v2-final-20261009/independent-install` | 46.299 | docs35独立安装载荷；原RPM及外部验收报告保留；重跑需重建DESTDIR |

docs35、docs38、docs49三组各22个原始二进制RPM已逐包读到并计算SHA，66/66与各自原始报告中的SHA一致，见 payload-original-rpm-sets.json。docs35目录另有1个源码RPM；初次数量检查把它计入而得到23，已按*.x86_64.rpm分开统计，见 rpm-count-correction.txt。原始RPM文件路径、大小及当前SHA在 [asset-catalog.tsv](../../tools/bolt/results/temp-cleanup-20261026/asset-catalog.tsv)。这里只认证原包仍在，不冒称本轮重新解包做了逐文件恢复认证。H=`archive-index-fix-rpm-20260923/baseline-rpm-extract`没有同等原包恢复证据，明确排除。

稳妥方案不会把hybrid的19.736GiB缓存再加一次：它已经包含在hybrid gbs-root中。两轮cache-release根及hybrid+BOLT根的缓存已经释放，不按历史91GiB/20GiB再加。旧R1当前84.157GiB，明显小于31号记录175.75GiB；本轮只按实际读数，不推测外部操作。

精确删除范围各自的最新后代文件时间、root属主/不可写目录计数与错误列表另见 scope-metadata.json；父目录的mtime不能代替两轮构建根各自的mtime。

## 4. 所有 >5 GiB 顶层范围逐项分析

“保留”行不计入可释放总量。含源码工作树的父目录即使有可删子树，也不整删。以下来源引用钉到本次核对的GitHub提交；同目录完整引用原文见 docs-grep.txt、doc-references.json，脚本引用见 scripts-grep.txt、script-references.json。

| 路径 / GiB | 最新后代文件mtime（+08） | 所属线、来源、完成状态/出处 | 建议及理由 | 权限、依赖、小文件 |
|---|---|---|---|---|
| `/var/tmp/llvm-optimize-x86-archivefix-20261013`<br>225.605† | 2026-10-15T22:40:54+08:00 | archive fix；2026-10-14 正式交接树；源码 cb679968 + PS3 3731eda7 / PS2 4c36e899；实存 VCS=4c36e899dffee2869af9afd174346e3eb9a7d7ca-dirty；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/49_x86_build_resume_result.md:238](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/49_x86_build_resume_result.md#L238)；[bolt-v4/docs/bolt/16_fallback_and_config_install.md:8](https://github.com/lhmax2010/llvm-optimize/blob/4aad31b261906bc159811411181ffc9e91e02958/docs/bolt/16_fallback_and_config_install.md#L8) | **仅 lto.cache 可以删除；其余保留**：历史树禁恢复/配置；后续安装不读缓存，但原输入、归档证据和RPM仍保留 | 无可见进程/活动overlay；脚本引用74处；外部硬链接inode 22；root目录1844；不可写目录1842；遍历错误3。已核验资产50条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/bolt-v4-20261022-cache-release`<br>192.628† | 2026-10-23T22:12:02+08:00 | BOLT/cache-release；9e5675f、d20e873；双轮完整构建与比较已完成；完成，结论已发布。[bolt-v4/docs/bolt/32_cache_release.md:232](https://github.com/lhmax2010/llvm-optimize/blob/4aad31b261906bc159811411181ffc9e91e02958/docs/bolt/32_cache_release.md#L232)；[bolt-v4/docs/bolt/32_cache_release.md:244](https://github.com/lhmax2010/llvm-optimize/blob/4aad31b261906bc159811411181ffc9e91e02958/docs/bolt/32_cache_release.md#L244) | **先保存小文件再删除（仅所列构建根）**：已完成；products、输入、source、脚本和报告留在父目录，见第3节精确范围 | 无可见进程/活动overlay；脚本引用17处；外部硬链接inode 0；root目录3693；不可写目录3689；遍历错误6。已核验资产157条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/gbs-root-x86_64-debuginfo-j4-v2`<br>84.157† | 2026-10-13T17:42:53+08:00 | archive fix；R1 普通/BOLT v2 旧树；源码 f111162e 配方；实存 VCS=f111162e94aa48ed367c9d2c039456c70e7160ae-dirty；历史轮有记录；是否还要重跑/后续用途待确认。[bolt-v4/docs/bolt/02_inventory.md:21](https://github.com/lhmax2010/llvm-optimize/blob/4aad31b261906bc159811411181ffc9e91e02958/docs/bolt/02_inventory.md#L21)；[main/docs/41_disk_inventory.md:69](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/41_disk_inventory.md#L69) | **保留**：34号性能输入的x86 sysroot和历史工具来源；旧保护未解除，本次未纳入整根清理 | 无可见进程/活动overlay；脚本引用54处；外部硬链接inode 0；root目录1844；不可写目录1842；遍历错误3。已核验资产36条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/gbs-root-x86_64-archivefix-v2`<br>79.287† | 2026-10-13T14:36:47+08:00 | archive fix；Rnew；docs38 llvm-strip 根；源码 f111162e + docs35/38 配方；实存 VCS=f111162e94aa48ed367c9d2c039456c70e7160ae-dirty；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/38_llvm_strip_x86_64.md:27](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/38_llvm_strip_x86_64.md#L27)；[main/docs/52_hybrid_link_tizen_base.md:49](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/52_hybrid_link_tizen_base.md#L49) | **保留（待用户判断）**：旧主线结果/保护范围或复现输入，尚无明确弃用裁决 | 无可见进程/活动overlay；脚本引用196处；外部硬链接inode 22；root目录1844；不可写目录1842；遍历错误3。已核验资产32条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/hybrid-local-20261023`<br>59.483† | 2026-10-23T18:07:40+08:00 | hybrid；6e9d4f2；本地构建完成，PM裁决PASS附例外；完成，结论已发布。[main/docs/53_hybrid_local_validation.md:9](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/53_hybrid_local_validation.md#L9)；[main/docs/53_hybrid_local_validation.md:182](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/53_hybrid_local_validation.md#L182) | **先保存小文件再删除（仅所列构建根）**：已完成；products、输入、source、脚本和报告留在父目录，见第3节精确范围 | 无可见进程/活动overlay；脚本引用12处；外部硬链接inode 0；root目录2979；不可写目录2977；遍历错误3。已核验资产146条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/archive-index-fix-rpm-20260923`<br>50.906 | 2026-09-23T23:15:49+08:00 | archive fix；H 唯一 RPM 解包基线；源码 f111162e 基线；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/35_archive_fix_v2_final.md:28](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/35_archive_fix_v2_final.md#L28)；[main/docs/41_disk_inventory.md:71](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/41_disk_inventory.md#L71) | **保留（待用户判断）**：H为旧唯一基线；未认证可完整恢复它的原RPM，不能当普通解包副本 | 无可见进程/活动overlay；脚本引用66处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产3条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `/var/tmp/llvm-optimize-archivefix-v2-final-20261009`<br>46.316 | 2026-10-09T16:16:32+08:00 | archive fix；独立安装幂等性验收根；源码 f111162e + docs35；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/35_archive_fix_v2_final.md:208](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/35_archive_fix_v2_final.md#L208) | **保留（待用户判断）**：旧主线结果/保护范围或复现输入，尚无明确弃用裁决 | 无可见进程/活动overlay；脚本引用10处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产1条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/toolchain-archivefix-v2-final`<br>46.299 | 2026-10-09T14:36:14+08:00 | archive fix；N 普通载荷；源码 f111162e + docs35；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/35_archive_fix_v2_final.md:29](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/35_archive_fix_v2_final.md#L29)；[main/docs/41_disk_inventory.md:73](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/41_disk_inventory.md#L73) | **可以删除（激进方案，待批准）**：已完成的RPM载荷，原包仍在；重跑历史脚本前须重新解包 | 无可见进程/活动overlay；脚本引用20处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产1条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/toolchain-release-x86-20261013`<br>46.256 | 2026-10-14T06:35:37+08:00 | release归因；新普通 RPM 解包 N；源码 cb679968 + PS3 3731eda7 / PS2 4c36e899；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/49_x86_build_resume_result.md:163](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/49_x86_build_resume_result.md#L163) | **可以删除（激进方案，待批准）**：已完成的RPM载荷，原包仍在；重跑历史脚本前须重新解包 | 无可见进程/活动overlay；脚本引用9处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产1条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/toolchain-llvm-strip`<br>46.256 | 2026-10-09T20:32:34+08:00 | llvm-strip；N38 llvm-strip 载荷；源码 f111162e + docs38；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/38_llvm_strip_x86_64.md:32](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/38_llvm_strip_x86_64.md#L32)；[main/docs/41_disk_inventory.md:74](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/41_disk_inventory.md#L74) | **可以删除（激进方案，待批准）**：已完成的RPM载荷，原包仍在；重跑历史脚本前须重新解包 | 无可见进程/活动overlay；脚本引用14处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产1条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/bolt-on-hybrid-20261024`<br>42.052† | 2026-10-24T01:06:09+08:00 | hybrid+BOLT；aa637c1；本地完整构建与验证PASS；完成，结论已发布。[bolt-v4/docs/bolt/33_bolt_on_hybrid.md:3](https://github.com/lhmax2010/llvm-optimize/blob/4aad31b261906bc159811411181ffc9e91e02958/docs/bolt/33_bolt_on_hybrid.md#L3)；[bolt-v4/docs/bolt/33_bolt_on_hybrid.md:7](https://github.com/lhmax2010/llvm-optimize/blob/4aad31b261906bc159811411181ffc9e91e02958/docs/bolt/33_bolt_on_hybrid.md#L7) | **先保存小文件再删除（仅所列构建根）**：已完成；products、输入、source、脚本和报告留在父目录，见第3节精确范围 | 无可见进程/活动overlay；脚本引用30处；外部硬链接inode 0；root目录1846；不可写目录1844；遍历错误3。已核验资产96条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `/var/tmp/llvm-optimize-arm-tls-aarch64-20261010`<br>38.256† | 2026-10-13T17:03:10+08:00 | ARM/archive fix；AArch64增量树/原生工具；源码 cb679968；实存 VCS=cb67996861d070d68fec2b4c623eed7d20ba2e23；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/40_arm_archive_conversion_stage1.md:2185](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/40_arm_archive_conversion_stage1.md#L2185)；[main/docs/46_review_round3_package.md:18](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/46_review_round3_package.md#L18) | **保留（待用户判断）**：ARM转换/主线历史输入，部分仍是34号sysroot；不代替主线决定弃用 | 无可见进程/活动overlay；脚本引用46处；外部硬链接inode 0；root目录1862；不可写目录1860；遍历错误3。已核验资产9条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `/var/tmp/llvm-optimize-arm-c1-20261010`<br>34.131† | 2026-10-14T14:14:15+08:00 | ARM/archive fix；ARM32增量树/原生工具；源码 cb679968；实存 VCS=cb67996861d070d68fec2b4c623eed7d20ba2e23；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/40_arm_archive_conversion_stage1.md:874](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/40_arm_archive_conversion_stage1.md#L874)；[main/docs/46_review_round3_package.md:17](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/46_review_round3_package.md#L17) | **保留（待用户判断）**：ARM转换/主线历史输入，部分仍是34号sysroot；不代替主线决定弃用 | 无可见进程/活动overlay；脚本引用56处；外部硬链接inode 0；root目录1858；不可写目录1856；遍历错误3。已核验资产9条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/arm-archive-tls-thumb-20261010`<br>30.505 | 2026-10-10T18:24:02+08:00 | ARM/archive fix；ARM Thumb/TLS与全量转换；源码 cb679968 输入；ARM helper 多轮修订；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/46_review_round3_package.md:22](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/46_review_round3_package.md#L22)；[main/docs/44_arm_source_review_round1.md:27](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/44_arm_source_review_round1.md#L27) | **保留（待用户判断）**：ARM转换/主线历史输入，部分仍是34号sysroot；不代替主线决定弃用 | 无可见进程/活动overlay；脚本引用47处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产3条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/review-round3-continue-20261012`<br>26.396 | 2026-10-12T19:35:08+08:00 | archive fix；四路转换评审3；源码 cb679968 + PS3/PS2 候选；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/46_review_round3_package.md:9](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/46_review_round3_package.md#L9) | **保留**：包含源码仓库/工作树，明确排除；不能按整个父目录删除 | 无可见进程/活动overlay；脚本引用19处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产2条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/review-round4-20261012`<br>25.811 | 2026-10-12T23:54:49+08:00 | archive fix；四路转换评审4及停止证据；源码 cb679968 + PS3/PS2 候选；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/47_review_round4_package.md:9](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/47_review_round4_package.md#L9) | **保留（待用户判断）**：旧主线结果/保护范围或复现输入，尚无明确弃用裁决 | 无可见进程/活动overlay；脚本引用14处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产2条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/archive-fix-rebind-20260923`<br>22.625 | 2026-09-23T15:26:54+08:00 | archive fix；旧profile重绑定/归档试验；源码 f111162e + 混合提案；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/42_disk_cleanup.md:64](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/42_disk_cleanup.md#L64) | **保留（待用户判断）**：旧主线结果/保护范围或复现输入，尚无明确弃用裁决 | 无可见进程/活动overlay；脚本引用10处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产5条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/arm-source-root-probes-20261010`<br>18.378 | 2026-10-11T01:22:40+08:00 | ARM/archive fix；ARM源文件/根内探测；源码 cb679968 输入；候选 helper；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/46_review_round3_package.md:19](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/46_review_round3_package.md#L19) | **保留（待用户判断）**：ARM转换/主线历史输入，部分仍是34号sysroot；不代替主线决定弃用 | 无可见进程/活动overlay；脚本引用13处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产2条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/release-x86-full-build-20261013`<br>16.188 | 2026-10-14T14:19:28+08:00 | release归因；续跑监测、补丁和打包证据；源码 cb679968 + PS3/PS2；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/49_x86_build_continuation.md:12](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/49_x86_build_continuation.md#L12)；[bolt-v4/docs/bolt/29_disk_footprint.md:70](https://github.com/lhmax2010/llvm-optimize/blob/4aad31b261906bc159811411181ffc9e91e02958/docs/bolt/29_disk_footprint.md#L70) | **保留**：包含源码仓库/工作树，明确排除；不能按整个父目录删除 | 无可见进程/活动overlay；脚本引用88处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产7条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/bolt-v4-20261013`<br>16.093 | 2026-10-24T14:34:15+08:00 | BOLT；BOLT 隔离源库/导出/早期草案；源码 9e5675f 当前源；多轮历史提交；历史轮有记录；是否还要重跑/后续用途待确认。[bolt-v4/docs/bolt/29_disk_footprint.md:58](https://github.com/lhmax2010/llvm-optimize/blob/4aad31b261906bc159811411181ffc9e91e02958/docs/bolt/29_disk_footprint.md#L58) | **保留**：包含源码仓库/工作树，明确排除；不能按整个父目录删除 | 无可见进程/活动overlay；脚本引用279处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产24条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/release-attribution-20261013`<br>14.101 | 2026-10-14T15:52:37+08:00 | release归因；发布归因与转换证据；源码 cb679968 + PS3/PS2；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/49_release_attribution.md:15](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/49_release_attribution.md#L15)；[main/docs/49_release_attribution.md:664](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/49_release_attribution.md#L664) | **保留**：包含源码仓库/工作树，明确排除；不能按整个父目录删除 | 无可见进程/活动overlay；脚本引用12处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产4条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/gbs-root-x86_64-archivefix`<br>13.630† | 2026-09-29T13:25:02+08:00 | archive fix；docs30 完整构建；源码 f111162e + v1 归档修复；实存 VCS=f111162e94aa48ed367c9d2c039456c70e7160ae-dirty；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/41_disk_inventory.md:68](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/41_disk_inventory.md#L68)；[main/docs/35_archive_fix_v2_final.md:55](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/35_archive_fix_v2_final.md#L55) | **保留（待用户判断）**：旧主线结果/保护范围或复现输入，尚无明确弃用裁决 | 无可见进程/活动overlay；脚本引用227处；外部硬链接inode 22；root目录1844；不可写目录1842；遍历错误3。已核验资产52条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/arm-archive-stage1-20261010`<br>11.923 | 2026-10-10T11:01:54+08:00 | ARM/archive fix；ARM阶段1/x86转换输入；源码 cb679968；x86输入另承 docs35；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/40_arm_archive_conversion_stage1.md:55](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/40_arm_archive_conversion_stage1.md#L55)；[main/docs/46_review_round3_package.md:20](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/46_review_round3_package.md#L20) | **保留（待用户判断）**：ARM转换/主线历史输入，部分仍是34号sysroot；不代替主线决定弃用 | 无可见进程/活动overlay；脚本引用33处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产2条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/archive-fix-v2-build-20260929`<br>11.661 | 2026-10-08T22:16:15+08:00 | archive fix；v2续跑/恢复证据；源码 f111162e + v2；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/35_archive_fix_v2_final.md:23](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/35_archive_fix_v2_final.md#L23) | **保留（待用户判断）**：旧主线结果/保护范围或复现输入，尚无明确弃用裁决 | 无可见进程/活动overlay；脚本引用34处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产2条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/archive-fix-full-build-20260927`<br>10.566 | 2026-09-27T21:59:56+08:00 | archive fix；历史完整构建/临时RPM仓库；源码提交本轮未核定，不判定可弃用；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/36_archive_fix_tizen_consumers.md:15](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/36_archive_fix_tizen_consumers.md#L15)；[main/docs/STATUS.md:405](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/STATUS.md#L405) | **保留**：包含源码仓库/工作树，明确排除；不能按整个父目录删除 | 无可见进程/活动overlay；脚本引用21处；外部硬链接inode 22；root目录0；不可写目录0；遍历错误0。已核验资产24条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/archive-fix-v2-final-20261009`<br>10.339 | 2026-10-09T16:55:23+08:00 | archive fix；docs35 原始22RPM与证据；源码 f111162e + v2；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/38_llvm_strip_x86_64.md:27](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/38_llvm_strip_x86_64.md#L27)；[bolt-v4/docs/bolt/24_rebase_recertification.md:69](https://github.com/lhmax2010/llvm-optimize/blob/4aad31b261906bc159811411181ffc9e91e02958/docs/bolt/24_rebase_recertification.md#L69) | **保留**：包含源码仓库/工作树，明确排除；不能按整个父目录删除 | 无可见进程/活动overlay；脚本引用34处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产47条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/llvm-strip-alternative-20260929`<br>9.642 | 2026-09-29T21:43:34+08:00 | llvm-strip；替代strip证据；源码 f111162e + strip试验；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/42_disk_cleanup.md:53](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/42_disk_cleanup.md#L53) | **保留**：包含源码仓库/工作树，明确排除；不能按整个父目录删除 | 无可见进程/活动overlay；脚本引用27处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产2条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/llvm-strip-x86_64-20261009`<br>9.473 | 2026-10-09T21:39:13+08:00 | llvm-strip；llvm-strip打包证据；源码 f111162e + docs38；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/38_llvm_strip_x86_64.md:22](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/38_llvm_strip_x86_64.md#L22) | **保留**：包含源码仓库/工作树，明确排除；不能按整个父目录删除 | 无可见进程/活动overlay；脚本引用18处；外部硬链接inode 22；root目录0；不可写目录0；遍历错误0。已核验资产24条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/arm-archive-stage1-c-newrepo-20261010`<br>9.236 | 2026-10-10T12:23:45+08:00 | ARM/archive fix；C1 导出/原仓库证据；源码 cb679968；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/40_arm_archive_conversion_stage1.md:627](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/40_arm_archive_conversion_stage1.md#L627)；[main/docs/40_arm_archive_conversion_stage1.md:772](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/40_arm_archive_conversion_stage1.md#L772) | **保留**：包含源码仓库/工作树，明确排除；不能按整个父目录删除 | 无可见进程/活动overlay；脚本引用13处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产11条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/archive-followup-review-20261014`<br>9.090 | 2026-10-14T16:18:28+08:00 | archive fix；归档后续评审/上传核对；源码 d4dd40da，父67619ec8；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/50_archive_followup_review.md:5](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/50_archive_followup_review.md#L5)；[main/docs/50_archive_followup_review.md:49](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/50_archive_followup_review.md#L49) | **保留**：包含源码仓库/工作树，明确排除；不能按整个父目录删除 | 无可见进程/活动overlay；脚本引用12处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产2条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `/var/tmp/llvm-optimize-llvm-strip-tizen-20261009`<br>8.928† | 2026-10-09T21:29:08+08:00 | llvm-strip；bfd/lld消费者根；源码 docs38 LLVM包，f111162e配方；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/38_llvm_strip_x86_64.md:325](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/38_llvm_strip_x86_64.md#L325) | **保留（待用户判断）**：旧主线结果/保护范围或复现输入，尚无明确弃用裁决 | 无可见进程/活动overlay；脚本引用5处；外部硬链接inode 0；root目录3364；不可写目录3360；遍历错误6。已核验资产14条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `/var/tmp/llvm-optimize-arm-stage1-20261010`<br>8.928† | 2026-10-10T12:14:18+08:00 | ARM/archive fix；C0/阶段1消费者根；源码 cb679968 仓库环境；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/40_arm_archive_conversion_stage1.md:628](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/40_arm_archive_conversion_stage1.md#L628)；[main/docs/40_arm_archive_conversion_stage1.md:991](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/40_arm_archive_conversion_stage1.md#L991) | **保留（待用户判断）**：ARM转换/主线历史输入，部分仍是34号sysroot；不代替主线决定弃用 | 无可见进程/活动overlay；脚本引用8处；外部硬链接inode 0；root目录3349；不可写目录3345；遍历错误6。已核验资产20条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `/var/tmp/llvm-optimize-archivefix-v2-tizen-20261009`<br>8.922† | 2026-10-09T16:56:13+08:00 | archive fix；v2 bfd/lld消费者根；源码 docs35 LLVM包，f111162e配方；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/36_archive_fix_tizen_consumers.md:19](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/36_archive_fix_tizen_consumers.md#L19) | **保留（待用户判断）**：旧主线结果/保护范围或复现输入，尚无明确弃用裁决 | 无可见进程/活动overlay；脚本引用5处；外部硬链接inode 0；root目录3356；不可写目录3352；遍历错误6。已核验资产14条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `/var/tmp/llvm-optimize-x86-archivefix-20261013-new-rpm-repo`<br>8.248 | 2026-10-14T11:58:20+08:00 | archive fix；22RPM临时消费者仓库；源码 cb679968 + PS3/PS2；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/49_x86_build_resume_result.md:167](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/49_x86_build_resume_result.md#L167) | **保留（待用户判断）**：旧主线结果/保护范围或复现输入，尚无明确弃用裁决 | 无可见进程/活动overlay；脚本引用4处；外部硬链接inode 22；root目录0；不可写目录0；遍历错误0。已核验资产22条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/bench_results`<br>7.284 | 2026-09-22T02:03:03+08:00 | BOLT；真实TU/预处理/profile/性能输入；源码 f111162e 历史BOLT配方；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/17_bolt_holdout.md:22](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/17_bolt_holdout.md#L22)；[main/docs/41_disk_inventory.md:82](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/41_disk_inventory.md#L82) | **保留**：profile训练/留出输入与真实TU资产，用户明确保留 | 无可见进程/活动overlay；脚本引用48处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产2条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/static-native-conversion-20260924`<br>6.307 | 2026-09-24T01:18:43+08:00 | archive fix；早期转换失败证据；源码 f111162e 输入；旧转换器；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/27_static_archive_native_conversion.md:25](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/27_static_archive_native_conversion.md#L25) | **保留（待用户判断）**：旧主线结果/保护范围或复现输入，尚无明确弃用裁决 | 无可见进程/活动overlay；脚本引用13处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产2条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/toolchain-hybrid-trial`<br>5.754 | 2026-09-22T21:48:06+08:00 | hybrid；隔离旧混合载荷；源码 f111162e + 七文件提案；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/22_hybrid_link_trial.md:171](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/22_hybrid_link_trial.md#L171) | **保留（待用户判断）**：旧主线结果/保护范围或复现输入，尚无明确弃用裁决 | 无可见进程/活动overlay；脚本引用14处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产1条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/hybrid-trial-20260922`<br>5.720 | 2026-09-22T22:12:48+08:00 | hybrid；隔离旧混合试验；源码 f111162e + 七文件提案；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/22_hybrid_link_trial.md:15](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/22_hybrid_link_trial.md#L15) | **保留（待用户判断）**：旧主线结果/保护范围或复现输入，尚无明确弃用裁决 | 无可见进程/活动overlay；脚本引用12处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产2条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/hybrid-sandbox-20261019`<br>5.663 | 2026-10-19T13:59:49+08:00 | hybrid；hybrid发布源码准备与导出；源码 6e9d4f2b；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/52_hybrid_sandbox_evidence/README.md:19](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/52_hybrid_sandbox_evidence/README.md#L19)；[main/docs/52_hybrid_link_validation.md:5](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/52_hybrid_link_validation.md#L5) | **保留**：包含源码仓库/工作树，明确排除；不能按整个父目录删除 | 无可见进程/活动overlay；脚本引用8处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产12条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/hybrid-link-20261015`<br>5.338 | 2026-10-19T13:50:40+08:00 | hybrid；hybrid源码/配置验证；源码 cef4d90b / 同树后续6e9d4f2b；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/52_hybrid_link_tizen_base.md:8](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/52_hybrid_link_tizen_base.md#L8)；[main/docs/52_hybrid_link_validation.md:5](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/52_hybrid_link_validation.md#L5) | **保留**：包含源码仓库/工作树，明确排除；不能按整个父目录删除 | 无可见进程/活动overlay；脚本引用17处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产12条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/bolt-v4-20261016-source-order`<br>5.245† | 2026-10-16T10:47:52+08:00 | BOLT；Source无条件声明修复/解析 overlay；源码 506dc25 → af82efed；历史轮有记录；是否还要重跑/后续用途待确认。[bolt-v4/docs/bolt/26_source_order_parse_fix.md:1](https://github.com/lhmax2010/llvm-optimize/blob/4aad31b261906bc159811411181ffc9e91e02958/docs/bolt/26_source_order_parse_fix.md#L1) | **可以删除 upper-parse；其余保留**：旧解析overlay上层；无活动挂载，报告/脚本和导出留在父目录 | 无可见进程/活动overlay；脚本引用13处；外部硬链接inode 0；root目录17；不可写目录16；遍历错误3。已核验资产15条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |
| `W/temp/llvm-optimize-intranet-20261020`<br>5.069 | 2026-10-20T21:22:42+08:00 | hybrid；可续传源码归档准备；源码 6e9d4f2b；历史轮有记录；是否还要重跑/后续用途待确认。[main/docs/llvm_optimize_intranet_fetch.md:9](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/llvm_optimize_intranet_fetch.md#L9)；[main/docs/STATUS.md:7](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/STATUS.md#L7) | **保留**：包含源码仓库/工作树，明确排除；不能按整个父目录删除 | 无可见进程/活动overlay；脚本引用13处；外部硬链接inode 0；root目录0；不可写目录0；遍历错误0。已核验资产7条（含输入/RPM/报告），见catalog；不等于都应新增保存。 |

W/llvm（源码仓库）也超过5GiB，但明确不在清理范围，最新后代普通文件见 source-latest-file.json。拟删GBS根内的LLVM是已导出的构建输入副本，不是独立Git工作树；保留的W/llvm及temp中的source工作树不动。W/docs、W/tools、W/.git、所有识别出的Git工作树及源码仓库都保留；每个大目录的git_roots和精确权限计数在 inventory.tsv/metadata.json。

### 4.1 >50 GiB父目录再展开一层

| 父目录 | 直接子目录 | 实占GiB |
|---|---|---:|
| `W/temp/bolt-v4-20261022-cache-release` | `baseline-root` | 85.418† |
| `W/temp/bolt-v4-20261022-cache-release` | `revised-root` | 83.025† |
| `W/temp/bolt-v4-20261022-cache-release` | `baseline-products` | 11.248 |
| `W/temp/bolt-v4-20261022-cache-release` | `revised-products` | 11.248 |
| `W/temp/bolt-v4-20261022-cache-release` | `rpm-difference-analysis` | 1.043 |
| `W/temp/bolt-v4-20261022-cache-release` | `revised-export-files` | 0.331 |
| `W/temp/bolt-v4-20261022-cache-release` | `revised-evidence` | 0.139 |
| `W/temp/bolt-v4-20261022-cache-release` | `baseline-resume2-evidence` | 0.139 |
| `W/temp/bolt-v4-20261022-cache-release` | `revised-run` | 0.015 |
| `W/temp/bolt-v4-20261022-cache-release` | `baseline-resume2` | 0.010 |
| `W/temp/bolt-v4-20261022-cache-release` | `baseline-rpm-inventory` | 0.005 |
| `W/temp/bolt-v4-20261022-cache-release` | `revised-rpm-inventory` | 0.005 |
| `W/temp/bolt-v4-20261022-cache-release` | `baseline-resume1` | 0.001 |
| `W/temp/bolt-v4-20261022-cache-release` | `rpm-validation` | 0.001 |
| `W/temp/bolt-v4-20261022-cache-release` | `baseline-segment2` | 0.000 |
| `W/temp/bolt-v4-20261022-cache-release` | `five-parse` | 0.000 |
| `W/temp/bolt-v4-20261022-cache-release` | `baseline-segment1` | 0.000 |
| `W/temp/bolt-v4-20261022-cache-release` | `baseline-evidence` | 0.000 |
| `W/temp/bolt-v4-20261022-cache-release` | `baseline-space-recovery` | 0.000 |
| `W/temp/bolt-v4-20261022-cache-release` | `baseline-preserve` | 0.000 |
| `W/temp/bolt-v4-20261022-cache-release` | `config` | 0.000 |
| `W/temp/bolt-v4-20261022-cache-release` | `revised-preserve` | 0.000 |
| `W/temp/bolt-v4-20261022-cache-release` | `rpm-difference-job` | 0.000 |
| `W/temp/bolt-v4-20261022-cache-release` | `baseline-export` | 0.000 |
| `W/temp/bolt-v4-20261022-cache-release` | `revised-export` | 0.000 |
| `W/temp/bolt-v4-20261022-cache-release` | `resume2-preflight` | 0.000 |
| `W/temp/bolt-v4-20261022-cache-release` | `baseline-tmp` | 0.000 |
| `W/temp/gbs-root-x86_64-archivefix-v2` | `local` | 79.287† |
| `W/temp/gbs-root-x86_64-debuginfo-j4-v2` | `local` | 84.157† |
| `W/temp/archive-index-fix-rpm-20260923` | `baseline-rpm-extract` | 50.890 |
| `W/temp/archive-index-fix-rpm-20260923` | `census` | 0.008 |
| `W/temp/archive-index-fix-rpm-20260923` | `rpm-macros` | 0.000 |
| `W/temp/hybrid-local-20261023` | `gbs-root` | 58.529† |
| `W/temp/hybrid-local-20261023` | `tu-inputs` | 0.631 |
| `W/temp/hybrid-local-20261023` | `export` | 0.322 |
| `W/temp/hybrid-local-20261023` | `tmp` | 0.000 |
| `/var/tmp/llvm-optimize-x86-archivefix-20261013` | `local` | 225.605† |

深入build/、lto.cache、RPMS、SRPMS和BUILDROOT的独立du全部在 subunits.json。它们是解释父目录组成的重叠数据，不能累加成“清理收益”。

## 5. 必须保留、需要先保全的小资产

- `T/runpath-fix-20261026/`：当前不存在；一旦创建整目录保留，不推断其任务已结束。
- `T/bolt-on-hybrid-20261024/products/`（3.886GiB）、`T/bolt-v4-20261022-cache-release/{baseline-products,revised-products}/`（各11.248GiB）：整体保留，RUNPATH/RPM比较仍要用。
- `T/bolt-v4-20261021-disk-footprint/` 的gbs_llvm_qb1202084.conf和build.conf整体保留。固定快照配置及build.conf实际SHA见catalog；build.conf预期e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945。
- 90份TU：`T/hybrid-local-20261023/tu-inputs/`，以及旧validation/bench_results资产；34号C输入`T/perf-c-o2-os-20261025/inputs/`和C++ .ii原件全部保留。perf父目录本次整体保留，包括测量脚本所用槽位/对象；不因报告已发布自动删除原始数据。
- profile/Source1200原件、`W/tools/collect_bolt_profile.py`、`extend_bolt_profile_aarch64.py`、final_bolt_calibration_plan.json及训练/留出清单保留；bench_results整体保留。所有*.fdata及clang-bolt-v2.fdata.xz的本轮SHA见catalog。源码仓库中的同名Source也不会删除。
- **新增保全前提**：34号通过hybrid+BOLT根的Tizen loader/运行库和build/lib64/clang/22运行。删除该gbs-root前，先保全 runtime-preservation.json 的8个运行库路径/符号链接布局及整个resource-dir，并在将来重测时显式重定向路径；本轮未复制、未改脚本。旧R1、ARM32/64 sysroot仍保留。

### 5.1 已有同SHA副本与需要补存的清单

完整逐文件表：[asset-catalog.tsv](../../tools/bolt/results/temp-cleanup-20261026/asset-catalog.tsv)（路径、大小、SHA、同SHA其它路径）；本次删除范围对应的动作与保全预算：[preserve-before-delete.json](../../tools/bolt/results/temp-cleanup-20261026/preserve-before-delete.json)。副本判断不只比文件名；同inode复用SHA时也核对size/mtime，来源记录在asset-hashes-inode-aliases.json。仅列少量关键二进制如下：

| 保留文件 | 字节数 | SHA256 | 副本/结论 |
|---|---:|---|---|
| `W/temp/bolt-on-hybrid-20261024/products/binaries/clang.candidate` | 183224160 | `8b799f18e2bc37269385db125c881609e8457de1dd179f5d9d0ff9f557b58d16` | 已实测同SHA其它路径3个；本文件明确保留 |
| `W/temp/bolt-on-hybrid-20261024/products/binaries/llvm-bolt` | 566824200 | `0ecdff6172f7fffb08d30f3865976ca15dc8708c3a1ef9fe0d2a543059996f75` | 已实测同SHA其它路径5个；本文件明确保留 |
| `W/temp/bolt-on-hybrid-20261024/products/binaries/ordinary-clang-22` | 1793485376 | `d5090159915657b235b96f1202c058e1efd1647d6a2225ac8fdb2906aeaa501d` | 已实测同SHA其它路径3个；本文件明确保留 |
| `W/temp/bolt-v4-20261022-cache-release/baseline-products/binaries/clang.candidate` | 183224160 | `4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9` | 已实测同SHA其它路径15个；本文件明确保留 |
| `W/temp/bolt-v4-20261022-cache-release/baseline-products/binaries/llvm-bolt` | 566824200 | `0ecdff6172f7fffb08d30f3865976ca15dc8708c3a1ef9fe0d2a543059996f75` | 已实测同SHA其它路径5个；本文件明确保留 |
| `W/temp/bolt-v4-20261022-cache-release/baseline-products/binaries/ordinary-clang-22` | 1793485312 | `06c940726269210ce3655e17366820a080bfe236a3adc24622958e6a6709e309` | 已实测同SHA其它路径5个；本文件明确保留 |

每个大目录匹配的资产数量已列在第4节，catalog保留完整路径而非只列上述示例。对未核验到独立小资产的旧转换目录，不宣称“报告够了即可删”；225个归档/bitcode可能就是原始复现输入，列为保留待用户判断。

### 5.2 旧脚本、overlay与硬链接

当前所有可读mountinfo未出现指向本范围的lowerdir/upperdir/workdir，findmnt也无残留项目挂载。磁盘上的旧overlay脚本不因此失效：旧解析upper仍依赖原下层才可挂回，方案只删除upper-parse，不删除其下层。所选新根的脚本引用未发现其它overlay把它们作为lowerdir；一般历史脚本直接引用仍存在，已逐行存证，未来重跑须先恢复/改指保全路径。搜索覆盖docs和分析脚本，不对LLVM源码/系统树做全量文本grep；未做任意程序的动态依赖证明，变量拼接和外部程序引用仍需执行前复核。

external-hardlinks.json列出每个大目录的外部链接inode、已定位其它路径和未定位链接数；源库/导出的Git对象有硬链接不等于能独立回收。两套精确删除范围未出现跨范围存活链接扣减，但这是当前可见元数据，实际执行前仍须复核。

## 6. 不确定、需用户判断的目录

除第3节精确范围外，本轮不替主线废弃归档、release或ARM验证输入。特别是：

- `W/temp/gbs-root-x86_64-archivefix-v2`（79.287GiB）：旧主线结果/保护范围或复现输入，尚无明确弃用裁决；[main/docs/38_llvm_strip_x86_64.md:27](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/38_llvm_strip_x86_64.md#L27)；[main/docs/52_hybrid_link_tizen_base.md:49](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/52_hybrid_link_tizen_base.md#L49)。
- `W/temp/archive-index-fix-rpm-20260923`（50.906GiB）：H为旧唯一基线；未认证可完整恢复它的原RPM，不能当普通解包副本；[main/docs/35_archive_fix_v2_final.md:28](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/35_archive_fix_v2_final.md#L28)；[main/docs/41_disk_inventory.md:71](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/41_disk_inventory.md#L71)。
- `/var/tmp/llvm-optimize-archivefix-v2-final-20261009`（46.316GiB）：旧主线结果/保护范围或复现输入，尚无明确弃用裁决；[main/docs/35_archive_fix_v2_final.md:208](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/35_archive_fix_v2_final.md#L208)。
- `/var/tmp/llvm-optimize-arm-tls-aarch64-20261010`（38.256GiB）：ARM转换/主线历史输入，部分仍是34号sysroot；不代替主线决定弃用；[main/docs/40_arm_archive_conversion_stage1.md:2185](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/40_arm_archive_conversion_stage1.md#L2185)；[main/docs/46_review_round3_package.md:18](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/46_review_round3_package.md#L18)。
- `/var/tmp/llvm-optimize-arm-c1-20261010`（34.131GiB）：ARM转换/主线历史输入，部分仍是34号sysroot；不代替主线决定弃用；[main/docs/40_arm_archive_conversion_stage1.md:874](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/40_arm_archive_conversion_stage1.md#L874)；[main/docs/46_review_round3_package.md:17](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/46_review_round3_package.md#L17)。
- `W/temp/arm-archive-tls-thumb-20261010`（30.505GiB）：ARM转换/主线历史输入，部分仍是34号sysroot；不代替主线决定弃用；[main/docs/46_review_round3_package.md:22](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/46_review_round3_package.md#L22)；[main/docs/44_arm_source_review_round1.md:27](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/44_arm_source_review_round1.md#L27)。
- `W/temp/review-round4-20261012`（25.811GiB）：旧主线结果/保护范围或复现输入，尚无明确弃用裁决；[main/docs/47_review_round4_package.md:9](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/47_review_round4_package.md#L9)。
- `W/temp/archive-fix-rebind-20260923`（22.625GiB）：旧主线结果/保护范围或复现输入，尚无明确弃用裁决；[main/docs/42_disk_cleanup.md:64](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/42_disk_cleanup.md#L64)。
- `W/temp/arm-source-root-probes-20261010`（18.378GiB）：ARM转换/主线历史输入，部分仍是34号sysroot；不代替主线决定弃用；[main/docs/46_review_round3_package.md:19](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/46_review_round3_package.md#L19)。
- `W/temp/gbs-root-x86_64-archivefix`（13.630GiB）：旧主线结果/保护范围或复现输入，尚无明确弃用裁决；[main/docs/41_disk_inventory.md:68](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/41_disk_inventory.md#L68)；[main/docs/35_archive_fix_v2_final.md:55](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/35_archive_fix_v2_final.md#L55)。
- `W/temp/arm-archive-stage1-20261010`（11.923GiB）：ARM转换/主线历史输入，部分仍是34号sysroot；不代替主线决定弃用；[main/docs/40_arm_archive_conversion_stage1.md:55](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/40_arm_archive_conversion_stage1.md#L55)；[main/docs/46_review_round3_package.md:20](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/46_review_round3_package.md#L20)。
- `W/temp/archive-fix-v2-build-20260929`（11.661GiB）：旧主线结果/保护范围或复现输入，尚无明确弃用裁决；[main/docs/35_archive_fix_v2_final.md:23](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/35_archive_fix_v2_final.md#L23)。
- `/var/tmp/llvm-optimize-llvm-strip-tizen-20261009`（8.928GiB）：旧主线结果/保护范围或复现输入，尚无明确弃用裁决；[main/docs/38_llvm_strip_x86_64.md:325](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/38_llvm_strip_x86_64.md#L325)。
- `/var/tmp/llvm-optimize-arm-stage1-20261010`（8.928GiB）：ARM转换/主线历史输入，部分仍是34号sysroot；不代替主线决定弃用；[main/docs/40_arm_archive_conversion_stage1.md:628](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/40_arm_archive_conversion_stage1.md#L628)；[main/docs/40_arm_archive_conversion_stage1.md:991](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/40_arm_archive_conversion_stage1.md#L991)。
- `/var/tmp/llvm-optimize-archivefix-v2-tizen-20261009`（8.922GiB）：旧主线结果/保护范围或复现输入，尚无明确弃用裁决；[main/docs/36_archive_fix_tizen_consumers.md:19](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/36_archive_fix_tizen_consumers.md#L19)。
- `/var/tmp/llvm-optimize-x86-archivefix-20261013-new-rpm-repo`（8.248GiB）：旧主线结果/保护范围或复现输入，尚无明确弃用裁决；[main/docs/49_x86_build_resume_result.md:167](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/49_x86_build_resume_result.md#L167)。
- `W/temp/static-native-conversion-20260924`（6.307GiB）：旧主线结果/保护范围或复现输入，尚无明确弃用裁决；[main/docs/27_static_archive_native_conversion.md:25](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/27_static_archive_native_conversion.md#L25)。
- `W/temp/toolchain-hybrid-trial`（5.754GiB）：旧主线结果/保护范围或复现输入，尚无明确弃用裁决；[main/docs/22_hybrid_link_trial.md:171](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/22_hybrid_link_trial.md#L171)。
- `W/temp/hybrid-trial-20260922`（5.720GiB）：旧主线结果/保护范围或复现输入，尚无明确弃用裁决；[main/docs/22_hybrid_link_trial.md:15](https://github.com/lhmax2010/llvm-optimize/blob/613fa5ee8703c14f56e0b682bf0910f639f48ec9/docs/22_hybrid_link_trial.md#L15)。

W/temp内未识别出应归为M1的>5GiB独立目录；旧41号文档的M1工作树在W之外，不在本轮扫描范围，不能拿其它项目空间补本项目缺口。找不到准确源码提交或结束裁决的项目仍按未知处理。root属主本身不等于必需sudo，但表中有不可写目录/Permission denied的GBS根和upper-parse无法保证普通用户删干净；将来需用户另行授权，不绕过权限。

## 7. 按分类与文件系统汇总

| 分类（只算精确不重叠范围） | /home | /var/tmp所在盘 |
|---|---:|---:|
| 先保存后删：4个新构建根，毛占用 | 262.349 GiB | 0 |
| 上项先保全预算（扣减） | 5.517 GiB | 0 |
| 可以删除缓存（稳妥） | 0 | 90.322 GiB |
| 可以删除载荷/旧upper（激进追加） | 142.055 GiB | 46.299 GiB |
| 保留/不确定范围 | 可释放计0；不纳入清理收益 | 可释放计0；不纳入清理收益 |

方案是用户选择清单，不是执行脚本。尤其不要用父目录大小直接替代子范围预算。权限盲区、文件系统元数据、稀疏/复制分配以及其它进程写入会让最终df变化不同；实际清理时以保存成功、即时进程/挂载/引用核查、前后df为准。

## 8. 原始材料与本轮边界

证据目录：`tools/bolt/results/temp-cleanup-20261026/`。包括du逐项stdout/stderr、完整下钻JSON、df、findmnt、lsof项目原文、fuser原文、所有命中行的rg输出、/proc挂载检查、元数据/权限、硬链接、资产SHA、重复副本和方案计算程序。lsof全主机原始输出与ps全命令行只留在本机同目录，不提交无关个人进程/文件列表；发布的lsof-project和lsof-final-project保留项目命中原文，NOFD可见性另列。

未删除任何文件（包括看起来可重建的目录），未移动任何文件，未复制待保全产物，未改权限或全局Git配置，未提权、挂载/卸载、运行cmake/ninja或构建，未新建分支、未推Gerrit。仅更新bolt-v4盘点文档和证据。完成后等待用户逐项批准。
