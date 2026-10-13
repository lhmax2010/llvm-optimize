# 49 续八：第二轮 x86 完整构建停止报告

**最终状态：STOP_HOST_MEMORY_FLOOR_ROUND2。** 2026-10-13 20:33:26（北京时间），宿主 MemAvailable=2,140,217,344B（1.993233GiB），触发预设的低于2GiB中止条件。唯一一次第二轮GBS已用完；未重试、未改资源或配方。Ninja最后完成6829/7634项，尚未执行%install，RPM为0，BOLT交接NOT_READY。

本页承接[环境、清理、准入和配置门禁](49_x86_build_continuation.md) §16–§17，历史章节保留。原始证据E8=`temp/release-x86-full-build-20261013/round2-launch`，只在本机；E6=`temp/release-x86-full-build-20261013/latest-base`。本轮边界为用户“续八”，没有修改Source、Commands、比较器、候选补丁、W/gbs_llvm.conf或BOLT资产；没有推Gerrit。

## 1. 清理、准入与唯一调用

19:20后mtime/ctime变化的/var/tmp顶层条目共4个。只删除符合属主linhao、19:21:00–19:22:10时间窗和本轮导出归属证据的三项：`.gbs_export_3hy1gs20`、`.gbs_export_xyqf69nu`、`gbp_qpdqpzal`。`linhao-gbs`为持久配置目录，保留。完整184853条删除前清单含路径、大小、时间、inode；内容身份和第一轮进程argv直接证明归属。更早临时目录未动；可读/proc未发现引用，其他身份的权限盲区如实登记于前页§16.1。

删除前/后可用空间283075473408/285916327936B，释放2840854528B（2.645752GiB）。19:52:09启动前再次读取285916323840B（266.280327GiB），正常准入283208338637B通过；减历史写入预算236006948864B后仍有46.481727GiB。**未使用一次性放宽**。内存准入沿用docs/49 §1的重阶段10GiB：实读13963427840B，通过。不是将此前普通构建16GiB门槛事后降低。证据：deletion-result.json、full-build-scope/{disk-admission,admission}.json。

入口`tools/run_certified_x86_release_build.py --round 2`使用独立标记E8/gbs-invoked-round2.json及full-build-scope，GBS显式选择`--spec llvm.spec`。第一轮E6标记/证据未改，第二轮GBS调用恰好1次。入口4项测试PASS，覆盖正常准入、例外双边界、两轮标记隔离和输入身份；本轮未使用例外分支。18GiB、swap0、6/6/2、debuginfo-j4、nice15/ionice3、共享锁以及每2秒30GiB磁盘底线保持。详见前页§16.3、E8/driver-tests.log、registered-plan.json。

## 2. 固定输入与构建环境

|项|身份|
|---|---|
|PS3候选提交|3731eda7e1b81bd313849a61d60fbac4970a99b1|
|PS2候选提交/实际源码checkout|4c36e899dffee2869af9afd174346e3eb9a7d7ca|
|spec SHA256|e88ef4cb4cfc4010bceb62a94389f517aedff0b2c2df819ba64dd988d9910426|
|生产Source SHA256|c43523c0ce04fc3310e670ff97823db8260c21250dc3172575a18db56500082e|
|PS3 patch SHA256|0d777afbf7b1a7b86afc5c1da5f7bef6b622315efc1316be0cac2b6e782d94e7|
|PS2 patch SHA256|c679f342a72d52de92914cd2d0007c981e0d6d22a6b378f811ca8ee8e12da9ff|
|专用配置E6/gbs-build.conf SHA256|d1ff39acbaffd03f3c626e9fa8c4a397ea902066e722fd305539cb298de7ab34|
|Base快照|tizen-base-toolchain_20261010.120615|
|Base repomd SHA256|2a99108e748092148d1161f4ef5e50fbaa57d98132460db6ad02852fea4a39a5|
|Unified快照|tizen-unified-toolchain_20260814.092727|
|Unified repomd SHA256|e7af3f222f0ce958678d964589f2d156e8b47ba463ac0b3b0b96c74663382200|

GBS导出spec去唯一VCS行后与候选相同，Source相同；120个依赖包实际安装清单与工具归属保存在installed-rpm-qa.tsv、installed-tool-ownership.txt。新环境clang/llvm为22.1.8-1.6、prlimit属util-linux2.41.2-1.6。14项保护文件最终SHA与开场一致，见final-integrity.json。专用配置与W配置的完整diff、仓库预检、旧新包版本表沿用前页§7–§8，不把不同环境的旧RPM当作本轮可比基线。

CMake门禁PASS，GBS启动至门禁425.898847s；包含导出/依赖初始化，不能当成纯CMake耗时。关键项：Release、Thin、C/CXX/ASM追加`-O3 -DNDEBUG`、LLVM_LINK_LLVM_DYLIB=OFF、CLANG_LINK_CLANG_DYLIB=OFF、BUILD_SHARED_LIBS=OFF、LLVM_BUILD_LLVM_DYLIB=ON、并发6/2；完整公共flags含-g2/-gdwarf-4/-g/-O3/-flto=thin。证据：full-build-scope/{CMakeCache.txt,cache-gate.json}、cmake-key-lines.json。

## 3. 构建阶段与资源实测

|阶段/指标|结果与口径|
|---|---|
|GBS启动→导出结束|19:52:09→19:53:28，约79s，日志秒级时间戳|
|标准后端→%prep→%build|19:53:35→19:58:39→19:58:48|
|CMake configure/generate|25.5s / 2.4s，CMake自身输出|
|Ninja第一/最后完成记录|19:59:17→20:33:15，6829/7634；不是全部完成|
|已记录操作|6080 Building、337 Linking、其余412；Linking包括归档，不能全部称为ELF链接|
|编译与链接|交错执行；首项完成至scope终止约2073s，为部分执行窗口，不能分拆相加为两个独立阶段耗时|
|%install转换/后处理/打包|NOT RUN，BUILDROOT/RPMS/SRPMS内文件均0|
|总wall，含中止回收|2506.665618s（41分46.666秒），入口outcome|
|scope最终MemoryPeak|12023508992B（11.197765GiB），systemd最终资源日志|
|scope最终MemorySwapPeak|0B|
|scope CPUUsageNSec|15934149446000，即15934.149446 CPU秒；不作性能结论|
|最大进程VmHWM采样|lld链接liblldb.so.22.1.8：9353887744B（8.711487GiB），采样下界|
|编译进程VmHWM采样最大值|PassBuilder.cpp.o：1471422464B（1.370369GiB），采样下界|
|/var/tmp运行采样最低可用|260640415744B（242.740303GiB）；30GiB保护未触发|
|新根du观察峰值|29829660672B（27.781036GiB），权限盲区下的下界；不是精确磁盘峰值|

构建中磁盘每2秒检查、常规资源每30秒留样，因此表中磁盘最低值是**已保存周期样本最低值**，不是每2秒数值的完整最小值。结束后20:41:58复查可用260557185024B。du对根内var/cache/ldconfig、usr/share/upgrade、root无读取权限；保留stderr，未提权。文件系统变化还可能含同时运行的其他项目，不全部归因本构建。证据：final-results.json、root-space-samples.jsonl、full-build-scope/{samples.jsonl,process-memory.jsonl,outcome.json}。

主要链接进程采样（时间是首次/末次被观察的界限，不是精确链接wall）：

|目标|PID|观察区间|VmHWM GiB|
|---|---:|---|---:|
|liblldb.so.22.1.8|2077100|20:26:26–20:30:06|8.711487|
|bugpoint|2078692|20:31:39–20:33:14|7.031693|
|libLTO.so.22.1|2079538|20:32:54–20:33:14|4.502689|
|llvm-tblgen|2066704|20:02:10–20:02:16|1.877548|
|clang-tblgen|2066875|20:02:32–20:02:34|1.058918|

全部观测见linker-peaks-final.json及原始linker-memory-observations.jsonl。bugpoint/libLTO在中止时仍在运行。各峰值不能相加当作同时占用；不能据此宣称6/6/2必然撞18GiB，亦不能把未走到的clang链接或打包阶段视为通过。

本轮GBS新建的四个导出临时目录及大小已在前页§17逐项列出，10秒采样同时占用峰值3039793152B（约2.831GiB）。GBS导出结束后自行删除四项；采样下界不能当作未来预算的严格上界。本会话只执行§1获批清理，没有增加清理范围。

## 4. 停止原因、证据边界与回收

20:33:26 guard原文：`BUILD ABORT: MemAvailable 2140217344 < 2 GiB: emergency stop`。20:33:30请求杀scope，20:33:50 systemd逐进程记录`Sending signal SIGKILL ... on client request`。因此是**宿主可用内存保护触发**；当时scope最终峰值仅11.197765GiB，不能归因为18GiB cgroup cap OOM，也不能归因为磁盘不足。未调查或更改其他项目负载，不能将宿主压力指定归因某一会话。

82个保存样本的memory.events中max/oom/oom_kill均为0；scope退出后的最终memory.events已不可读，不能把采样0扩写成无任何漏采事件的保证。最终MemoryPeak/CPU/Swap计数从systemd journal补取，来源scope-final-journal-counters.json。最初build-summary.json的`scope_peak_final_counter=false`仅表示预期scope-after-rpm文件未生成；最终汇总final-results.json明确采用journal计数，不覆盖原始汇总。

systemctl kill返回1/Access denied；journal显示本任务GBS/build/rpmbuild/ninja/clang/lld均已发SIGKILL，但另记auxiliary processes权限失败。随后实际核查scope inactive/dead、任务进程0、挂载0，不能以该警告声称残留，也不能隐藏警告。gbs.exit缺失是强制中止后的附带结果。outcome exit137，不是成功；trace helper exit0只表示附加会话退出。保存了CMakeCache/build.ninja/.ninja_log、原始日志、终止journal；未修改部分构建树。

辅助脚本缺陷条款使用一次：新写的只读汇总器把GBS下载`[n/N]`也识别成Ninja进度。由原日志证明Ninja总数为7634后，仅加`total==7634`筛选，重跑汇总一次，得到6829条；门禁和构建均未重跑/放宽。旧汇总与修正diff保存在build-summary-before-helper-fix.json、summary-helper-fix.diff。

共享重任务锁20:33:55释放；两项目锁20:42:21释放；20:42:42终检任务进程/临时挂载/项目锁均0，scope inactive/dead，采样器、日志读取线程、磁盘/export观察器、trace会话已回收。证据cleanup-final.json、lock-released.json、各reaped.json。没有接触BOLT工作树或获取其锁后作额外操作。

## 5. 验收1–7、交接与挂账

|验收项|本轮结论|
|---|---|
|1 输入身份、根内依赖/工具归属|冻结身份、导出、120包清单/工具归属、CMake门禁PASS；未产出最终RPM，不能代表整体验收|
|2 install-post及逐档strip|NOT RUN；只有宏静态摘录，没有实际后处理执行证据|
|3 开发归档、compiler-rt、libarcher|NOT RUN，无新RPM/安装树|
|4 同环境未打补丁安装树比较|NOT RUN；未满足1–3、5–7先通过的时点。保留有条件授权和“本项不阻塞交接”裁决，不能豁免其他未完成项|
|5 七宿主/Tizen/运行库消费者|NOT RUN|
|6 独立真实-bi及同树SKIP|NOT RUN|
|7 跨子系统直接非LTO结构诊断|本轮NOT RUN；此前发布60对认证仅是既有证据|

**BOLT交接：NOT_READY，未交接。** 保留的部分构建树为：

```text
/var/tmp/llvm-optimize-x86-archivefix-20261013/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build
```

ThinLTO缓存为上述路径`/lto.cache`，build.ninja有176行明确指定它（E8/thinlto-cache-link-lines.txt）。这里有部分编译/链接产物，**没有构建成功时间、完整RPM或验收通过记录**，不得作为本轮通过验收的交接树。停止时间20:33:26，scope终止20:33:50；未来如何使用由后续任务决定，本轮不续跑。

两ARM全量、根内小试与64MiB负例、bash依赖清单、LLVM23探测均NOT RUN。发布模式完整构建继续挂账，已通过的60对认证不变。第二轮只允许一次调用的授权已用完，按规则停止后续步骤；没有重新生成或改写已冻结候选，没有发布可提交/可交接的新验证结论。

## 6. GitHub交付

此前进度提交1261f77（清理/入口）、b7a1257（唯一调用）、cc75c36（CMake门禁）、485b870（中途进度）均已推送main。本收尾提交同时更新本页、前页状态链接与STATUS；原始temp证据留本机。保护文件14项最终一致；主仓库仅保留用户原有gbs_llvm.conf未提交改动。
