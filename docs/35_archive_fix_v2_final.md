# 35 归档修复 v2：提交配置恢复与增量续跑准入记录

日期：2026-10-09（Asia/Shanghai）。起点：`c1856d0415b9b7ee82b2062fa162476669836914`。
本报告与STATUS同一提交更新；docs/25–34保留不动。

**结果：提交配置已恢复，增量构建因磁盘准入不足而未启动。**
试验spec、完整diff及配置指纹与docs/32登记的v2候选一致，Source未变；
只读Ninja dry-run成功，但现有可用磁盘18.761GiB，即使删除全部允许清理的本根缓存，
可用空间上界仍只有54.724GiB，达不到原入口60GiB要求。
因此本轮没有执行`rpmbuild -ba --noprep`、新RPM验收、消费者测试或短路安装，没有生成新提交补丁。
没有降低门槛、清理其他目录或重试；本根缓存也未删除。

## 0. 范围、路径与现场

本轮只恢复用户指定的提交配置，使用标准GNU strip；编译配方、Source及6/6/2并发不变。
预定运行方式为原构建根的正常`-ba --noprep`，不重新执行会清空准备树的`%prep`。
完整LLVM资源规则继续使用MemAvailable≥16GiB、18GiB cap、MemorySwapMax=0、debuginfo -j4；
构建入口磁盘准入仍为≥60GiB。测试包为≥8GiB准入、6GiB cap、逐包串行。
这些均为预定规则，本轮没有启动构建scope，不能将其写成运行实测。

| 别名 | 路径 |
| --- | --- |
| W | `/home/linhao/Toolchain/development/llvm-optimize` |
| E35 | `W/temp/archive-fix-v2-final-20261009`，本轮命令、原始输出与JSON，仅保存在本机 |
| E34 | `W/temp/archive-fix-v2-build-20260929`，历史证据不覆盖 |
| U34 | `E34/resume-20261008` |
| S | `W/temp/llvm-archivefix-trial`，分支`archive-fix-trial` |
| Rnew | `W/temp/gbs-root-x86_64-archivefix-v2` |
| R | `Rnew/local/BUILD-ROOTS/scratch.x86_64.0` |
| B | `R/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build` |

开场主仓库`git status --short`为空，未发现本项目的gbs/rpmbuild/ninja/lld等竞争进程。
12:00:03取得项目锁，session=`archivefix-rpm-b4cc90d5cc92417d9368db5b64013005`，holder PID211110。
S的HEAD仍为`f111162e94aa48ed367c9d2c039456c70e7160ae`；工作树仅候选spec修改与新增Source，
没有额外源码改动。W/llvm与其spec未改，隔离的旧混合根未访问。
证据：`E35/task-start.json`、`lock-acquired.json`、`current-state-audit.json`。

### 0.1 原构建根核查及证据边界

| 对象 | 本轮检查 | 结论 |
| --- | --- | --- |
| CMakeCache.txt | 与U34/build/CMakeCache.txt最终配置快照逐字节SHA比对 | PASS |
| clang-22、llvm-ar、lld、libclang-cpp.so.22.1 | 与docs/34核对过的4个关键ELF SHA比对 | 全部PASS |
| .ninja_log | docs/34进入续跑前的1,079,791字节前缀SHA仍相同，当前1,106,041字节 | 前缀PASS；多26,250字节，最后mtime为10月8日20:25 |
| .ninja_deps | 同期12,627,012字节前缀SHA仍相同，当前12,663,784字节 | 前缀PASS；多36,772字节，最后mtime为10月8日20:25 |
| build.ninja | 当前29,952,987字节，mtime为10月8日17:37，与docs/34重配时间相符 | docs/34未保存重配后的图SHA，不能声称完整末态SHA比对PASS；不拿重配前的旧SHA误判污染 |

Ninja状态的完整末态SHA在docs/34中没有独立存档；本轮明确记录这个证据缺口。
前缀匹配、时间及dry-run只能证明已检查的事实，不替代缺失的历史末态摘要。
当前完整恢复清单已保存为`E35/resume-input-manifest.json`，后续应以它核对本轮结束现场：

| 文件 | 当前SHA256 |
| --- | --- |
| CMakeCache.txt | `d9970d7332f1f4fdd9eeca10531fa6b126a20e6fa4a0603a538a3cabc2385f8b` |
| build.ninja | `81216d3d30685a3c4ade8a667c92b51da923fba54331ebfefd38c69906bc7120` |
| .ninja_log | `a1b3272554227136cd77909250746bb4308f1f5b7393ee830cb372e302699d80` |
| .ninja_deps | `921b76a168ab6d570ec9640495bf366f502176ea4e5e0da6907b5b5e820560c8` |
| bin/clang-22 | `d25e99607c9ea23bf2e50da5075c21f0145f6da24a39a4228d2fd8026ead70cf` |
| bin/llvm-ar | `3d8ed30f0cfb0ce3bf1dc096b7b3cb840291ff0e49f3aaa26975ad3a2a681d8f` |
| bin/lld | `9895d67f7020ac1ca573ac7d40b1cda93ace9aa504c17cfed358211bd1554f47` |
| lib64/libclang-cpp.so.22.1 | `15e1e964312209cc04bc89c09caa02445988947f3e0622b28eebe360023d2f11` |

## 1. 提交配置恢复与认证

只在S及本次实际续跑会读取的`R/home/abuild/rpmbuild/SOURCES/llvm.spec`中，
删除用户指定的三行额外条件定义和紧随的分隔空行。根内GBS导出的VCS、5项Patch/%patch条目均保留，
没有拿S原文覆盖GBS导出spec。改前/改后副本及最小diff均存E35。

| 身份 | SHA256 / 证明 |
| --- | --- |
| S spec改前 | `a9bbb24c142382c000a13a3fe70549c44e7ab33969a1a75337f0da675afd3969` |
| S spec改后 | `6a91a0bf3d8d2044473662b65ed3d32d4696a697ccd52200d983ce4334aeafdf`；与docs/32 §5逐字节SHA相同 |
| Source，tools/S/根内副本 | `6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557`；未修改 |
| 相对f111162e的完整候选diff | `751a629228ed49fb013d95d8d8a451dc341e841c142db67198c7624d36f1ccdb`；与docs/32保存的diff逐字节相同 |
| 根内导出spec改前 | `acded99407dc2ac02e22b0fff9097b7067297613d01777e5c4ad3b455dcb396b` |
| 根内导出spec改后 | `91f684691eb35af52b1a9f2a2cba478f88dbfd8a48b4c2281dac6144d71d3bd0` |
| 完整configuration对象 | 与`git show 4adbdfb:tools/llvm_archive_fix_trial_fingerprint.json`中的configuration完全一致 |

`tools/llvm_archive_fix_trial_fingerprint.json`已同步spec、完整diff与normalized_spec摘要，
Source、CMake参数和6/6/2均未改变。`archive_trial_source_identity(S)`实际检查通过。
按本轮用户明确授权沿用docs/34的Source离线PASS证据；不声称旧manifest里的试验spec哈希就是本轮spec。
本轮新配置对应的证明是`E35/configuration-restoration.json`与上述docs/32字节比对。

候选diff本机路径：
`/home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-v2-final-20261009/archive-native-conversion-v2.diff`。
这仍是相对f111162e的试验diff，**不是已生成的tizen_base提交补丁**。

### 1.1 只读dry-run

通过`gbs chroot --root R`进入abuild登录shell，执行：

```sh
set -eu
cd /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build
rpm --define '_smp_mflags -j4' --eval '%{__strip}|%{_toolchain}|%{_smp_mflags}'
ninja -n -j 6
printf '%s\n' 'DOCS35_DRYRUN_PASS'
```

原始输出关键行：

```text
/bin/strip|clang|-j4
[1/87] LLDB headers: stage LLDB headers in include directory
...
[86/87] LLDB headers: stage LLDB headers in include directory
[87/87] Running utility command for liblldb-header-staging
DOCS35_DRYRUN_PASS
```

退出0且末尾标志存在。待办数是87，不能写成0：86项头文件stage加1项utility；
没有列出C/C++编译或链接任务。没有为消除待办修改配置。
这只是重配前dry-run；因为未准入构建，本轮CMake重配后实际执行项数及是否重链均为**未测**。
完整argv、输入shell和全部87行见`E35/dry-run{.py,.json,.log}`、`dry-run-abuild.sh`、`dry-run-chroot-input.sh`。

## 2. 资源准入：磁盘不足，未启动

12:04:06调用现有`build_llvm_x86_64.resource_plan()`，先验证恢复后的完整配置与认证文件一致。
内存满足；磁盘触发`tools/build_llvm_x86_64.py:103`原有60GiB门禁，未创建构建scope或启动rpmbuild：

```text
disk free 18.761 GiB < 60 GiB
```

| 项目 | 实际字节 | GiB |
| --- | ---: | ---: |
| MemAvailable | 23,448,223,744 | 21.837860 |
| 内存准入线 | 17,179,869,184 | 16 |
| 文件系统可用空间 | 20,144,885,760 | 18.761387 |
| 本根20,872个可再生cache文件的分配空间 | 38,614,765,568 | 35.962803 |
| 可用空间 + 全部允许回收cache的上界 | 58,759,651,328 | 54.724190 |
| 磁盘准入线 | 64,424,509,440 | 60 |
| 即使全部回收cache仍缺少的空间 | 5,664,858,112 | 5.275810 |

cache逻辑字节38,572,354,832；测量按`st_blocks × 512`计算可回收分配空间，
逐文件记录name、size、blocks、inode、mtime、link count。这里是回收空间上界，不是已释放空间。
即使此上界也不足，因此没有先删除整份缓存再启动必然失败的入口；缓存保留，删除文件数0。
没有清理历史根、已解包RPM、源码、对象或其他证据，没有调整缓存裁剪参数。

这是同一原入口的资源门禁拒绝，**不属于编译/链接失败**，也没有消耗一次实际增量rpmbuild执行。
未进入内存等待：内存已满足，等待内存不会解除本次磁盘门禁。
如保持当前缓存不动，距60GiB尚差约41.239GiB；若以后另获空间处置授权，
至少还需在本次允许cache之外提供5.276GiB，且再回收该cache，才能达到本次读数下的准入下限。
达到准入下限不保证后续打包和新目录解包全程空间充足，启动前仍需重新记录资源。

证据：`E35/check_admission.py`、`resource-admission.json`、`resource-commands.log`、
`cache-inventory.json`、`current-state-audit.json`。构建脚本资源规则未改。

## 3. 本轮构建与验收状态

| 项目 | 状态 |
| --- | --- |
| 恢复提交配置 / Source不变 / docs/32指纹一致 | PASS，§1 |
| 原根只读ninja -n | PASS；87项stage/utility，§1.1 |
| 增量`-ba --noprep` | **0次，磁盘准入拒绝** |
| CMake重配、实际Ninja任务、重链、转换段及后处理 | 未执行；没有本轮耗时、峰值或日志结果 |
| 新22RPM inventory与`temp/toolchain-archivefix-v2-final`解包 | 未产出、未创建；不使用docs/34旧产物冒充 |
| 225开发档、全库符号缺失汇总及分段抽查 | 未执行本轮新RPM验收 |
| compiler-rt 45档成员ELF字节、索引及无DWARF | 未执行；要求仍是与docs/13基线逐字节一致，不放宽 |
| 非归档文件与基线逐字节比对 | 未执行，不自动豁免差异 |
| GNU strip后处理、零格式错误、转换证据清理 | 未执行；只查询了默认宏，不等同实际后处理日志 |
| 七项宿主消费者 | 0次 |
| Tizen bfd/lld测试包及whole-archive诊断 | 0次 |
| 独立安装根真实-bi再转换及归档检查 | 0次 |
| 同一安装树Source SKIP | 0次 |
| 新RPM clang-22/lld/llvm-ar对基线SHA | 未执行；§0.1的构建树身份检查不是这一项 |
| tizen_base提交生成及apply --check | 未执行 |

按用户“失败即停止、不改后重试”的约束结束本轮执行，未绕过磁盘准入启动任何构建。

## 4. 提交补丁及基准分支

本轮未进入第三步，未刷新目标分支、未新建补丁工作树、未生成format-patch。
最近已知的本地`origin/tizen_base`记录仍为docs/34 §0.1的
`2d23367d74afbf2bb1e9e4013fce072b3a154109`；不称其为本轮已刷新到的远端HEAD。
后续生成时仍须按用户要求无凭据刷新或记录冻结基准，并只包含归档修复的spec改动与Source。

现有v1保持不动：

| 文件 | SHA256 |
| --- | --- |
| `patches/archive-index-fix/0001-Fix-llvm-static-devel-usability-with-ThinLTO.patch` | `0c40c91cb6b896fd93f2712b669eec6771d219268dff7d290539fbb98d0bea58` |
| `patches/archive-index-fix/llvm-static-archives-native.py` | `2476c5efa061499d7963e0f0976f0c9c86944b688f5bcc48ea40911574af399e` |

v2候选Source为`6bd0546a…`，不能与上表已发布v1混用，也不能写成v2完整验收通过。
预定作者仍为FatTank <hao.lin@samsung.com>，Change-Id保持
`Id4eb147e7ec4764d58a81110cf7bf57d21b64ac8`；本轮没有创建该LLVM提交或推Gerrit。

## 5. 收尾与恢复入口

本轮已完成配置恢复和资源核查；真正的增量构建、全部新RPM/消费者/幂等验收及提交补丁仍未完成。
原根及候选配置保留；后续读取STATUS、本文和`E35/resume-input-manifest.json`，
先核对独占与现场、解决磁盘空间，再执行仍未启动的增量机制；不得将本轮准入失败写成实际构建失败或已验收。

本轮命令及原始输出均在E35：`audit_current.py`、`restore_submission_config.py`、
`configuration-restoration.json`、两个spec改前/改后副本与restoration.diff、`dry-run.log`、
`resource-admission.json`、`task-outcome.json`、`final-integrity.json`、`lock-released.json`。
收尾复核13项保护文件全部匹配，本项目构建进程0；12:08:40锁持有者正常退出并删除自己的锁。
本轮没有创建构建采样器；唯一锁维护进程已回收，原构建根没有后台续跑任务。
`tools/llvm_archive_fix_trial_fingerprint.json`状态登记为`STOP_DISK_ADMISSION_NO_BUILD_STARTED`；
离线PASS仅表示沿用已验证Source，不代表本轮构建或新RPM验收PASS。

约束自检：没有修改W/llvm/spec或docs/25–34，没有访问隔离旧混合根；没有完整重建、BOLT、
性能校准、Chromium或Gerrit推送；增量rpmbuild、测试包和-bi均0次；缓存清理0次。
