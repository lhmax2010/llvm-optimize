# 12 周三新树：身份通过，资格探测参数错误后停止

日期：2026-10-14（北京时间）。本次状态 **STOP_QUALIFICATION_ARGUMENT_ERROR**。第一步交接身份核验通过，但匹配度查询调用失败，没有得到N/M/S/U/Q或R、S/N。遵守用户“规定之外停止”而不改参数重试；第二至第七步全部NOT RUN，未推Gerrit sandbox。

## 授权与本次前提

最新PM要求：正式交接后在新树原地cache；同树追加bolt项目/runtime OFF/BOLT_BUILD_TOOLS OFF、只构建llvm-bolt；配置前后clang唯一链接命令逐字相同；最终候选由这个新工具产生。30/90完整对象同一实体路径；重做两模式小spec并按22普通RPM生成逐项DWARF预期差异；x86历史30文件各5次，逐文件中位数及几何平均candidate/ordinary须<0.98。前六步全部PASS后才授权把父cb679968、无归档补丁的完整BOLT提交直接推refs/heads/sandbox/lhmax2025/bolt_pgo；拒绝时原样停，不拆profile、不换方案。不推refs/for或tizen_base。

内存不足每5分钟复查、最多60分钟；本次heavy入场17.43GiB，未进入等待。shared flock≤60分钟/段、16GiB/swap0/nice15/ionice3、运行MemAvailable<3GiB中止；轻cap4GiB/nice19/ionice3。大写入>10GiB结束仍≥30GiB，未复制96.88GB cache、未做大安装。

## 交接核对 PASS

main只读同步至91b45c167a8773bbe1564b5ab902033da5060d83；docs/STATUS.md和docs/49_x86_build_resume_result.md §11/15确认READY，交接997dbb1，时间2026-10-14T13:10:12.026995+08:00。根/目录均逐项相符：

- R=/var/tmp/llvm-optimize-x86-archivefix-20261013/local/BUILD-ROOTS/scratch.x86_64.0
- build=R/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build
- cache=build/lto.cache，47,107文件、96,877,810,360B；本次未变，不复制。
- clang-22 SHA7df0ff90dbca7f99ed6a642546281584dbfaab1528a94abf7a1bb524ca371b2c
- CMakeCache SHAf7e93b874c5aefdbe4515e6bedb8318ee7c207a95442162e460480545cceb59f
- build.ninja SHA9fcc86836b133cff1968f7393e608969341f2775cfbbd11d2e3a00199b36f551
- 交接8个文件（含导出spec、生产Source、.ninja_log、ar/lld）逐SHA/大小通过；22个RPM逐SHA/大小及集合通过。
- 冻结环境记录Base tizen-base-toolchain_20261010.120615 / Unified tizen-unified-toolchain_20260814.092727；基线cb679968、PS3/PS2链终点4c36e899，与用户交接及main记录一致，导出spec和生产Source实物SHA相符。完整repository repomd/补丁指纹保存在wednesday-handoff.json，未更换快照。

只读保护home/abuild/review49-independent-install的元数据清单，另冻结22RPM；所有输出仅在本会话新目录，不改这些原件。归档验收4依其原裁决SKIP，READY交接仍成立，不将其冒充PASS。

## 资格探测失败与责任边界

历史llvm-bolt（SHA1da7bb735f7bc1afab9a863154260699b0b0f88c6fd05b99231dd21ef653fd5a）仅复制到新BOLT目录作先查匹配度的资格探针。profile v2解压SHA核对通过。普通clang保持原SHA，不带emit-relocs。探测脚本错误地复用了最终生产重写的固定选项，包含-reorder-functions=cdsort和-split-eh；这组参数需要重定位，不能直接用于此普通ELF的先行资格查询。

实际仅一次调用，rc1，原文：

```text
BOLT-WARNING: debug info will be stripped from the binary. Use -update-debug-sections to keep it.
BOLT-WARNING: disabling -split-eh in non-relocation mode
BOLT-ERROR: function reordering only works when relocations are enabled
```

这是本任务探测入口参数错误，不是交接身份失败、资源不足或profile失配。N/M/S/U/Q、R、S/N全部UNKNOWN，5%双门禁NOT EVALUATED。没有删函数重排参数重试、先重链绕过步骤1或用历史R1的R值代替新树数据；没有启动生产llvm-bolt构建。失败argv、全部原始输出及scope证据保留。生产草案对带emit-relocs的输入使用cdsort本身未由这次失败否定，未修改生产helper/patch/profile。

下次恢复必须先明确独立的非重定位匹配度查询入口，不能再把最终重写参数原样套给普通ELF；本轮没有执行修正或再次查询，不能预称修正后会PASS。

## 已运行资源与回收

|阶段|scope wall(s)|cgroup峰GiB|最大采样VmHWM(kB)|状态|
|---|---:|---:|---:|---|
|身份核对|7.052|2.322|110220|PASS，轻cap4GiB|
|探测准备|6.545|1.548|153048|PASS，轻cap4GiB|
|匹配探测|1.025|0.480|12596|rc1，heavy cap16GiB|

0.5秒进程采样没有捕获短命llvm-bolt的VmHWM；12596kB是被采到的Python进程值，不能当BOLT峰值。cgroup peak515,751,936B由内核给出，二者分开记录。匹配段MemAvailable入场18,717,745,152B，采样最低18,678,910,976B；OOM0/swap0。共享锁等约0.000014s、持1.063s，finally释放。普通chroot仅临时proc，无私有namespace/selfbind/hostbind，before/during/after mountinfo均保存，after无残留。

停止后只读审计：8个交接文件、22RPM再次SHA/大小一致；归档证据元数据清单相同；原cache完整name/size/mtime清单相同，仍47,107文件/96,877,810,360B。stop-audit为轻任务，scope7.541s并已回收；全部本次scope消失，无仍运行的BOLT进程/采样器，无临时proc。没有进入本次交接资料中的两棵/var/tmp ARM构建根，W tracked/llvm不写。

## 第二至第七步 NOT RUN

|步骤|结果|
|---|---|
|同树llvm-bolt配置/构建/链接命令对照/install差集|NOT RUN；无新工具SHA、CMake差异或资源数据|
|原地重链/strip-debug/新BOLT/strip-all/三目标/SHA链|NOT RUN；无本次最终候选|
|30历史与90资产完整对象|NOT RUN；旧R1 PASS不继承|
|双模式小spec与22RPM预期清单/DWARF|NOT RUN；旧小spec不继承，未生成本次预期差异|
|30文件×5性能复核|NOT RUN；无中位数/几何均值或达标结论|
|sandbox推送|NOT ATTEMPTED；前六步未通过，不声称推送前后远端核对已完成|

源草案仍d6ddbff5ba74bfb420b357b5b6ba9ed300971bb4（父cb679968，无归档补丁）；没有提交新BOLT源码或推Gerrit。若tizen_base后续合入归档补丁，周五定稿仍需在新tizen_base变基并解决llvm.spec冲突，本轮未做。

原始E=W/temp/bolt-v4-20261014-wednesday；根内新/home/abuild/bolt-work/bolt-v4-20261014-wednesday仅helper、历史工具与profile副本/解压文件，全部保留。公开wednesday-handoff/matching/stop JSON、qualification.log；raw全分支/钉提交索引见10。此处STOP来自用户任务规则，不是额外审批或skill门禁。
