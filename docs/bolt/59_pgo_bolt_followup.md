# 59：PGO clang 的 BOLT 资源补测（前置缺项停止）

D根未构建merge-fdata与BOLT插桩运行库，本项停止在工具核对，没有启动插桩、采集或优化；没有替换工具、重编LLVM或改动旧根。PGO clang与llvm-bolt已复制到新目录并核对SHA，旧Source1200来自13个ARM加10个AArch64用例的BOLT插桩采集，不是perf。完整PGO+BOLT资源仍有本次未测项，下面只给已有实测与明确标出的借用估算。

## 1. 身份与停止原因

实验目录`W/temp/pgo-bolt-followup-20261105/`启动前不存在。/home初始86,649,049,088B，高于30GiB；复制/哈希在独立systemd用户服务完成，MemoryMax=MemTotal−8GiB、swap0、CPUQuota1200%、nice10、ionice2/7。服务成功表示前置检查完成，**不代表本项插桩实验成功**。

D根为`W/temp/pgo-resource-20261102/full/stage-D/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0`；下表路径相对其中`home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/`：

|文件|字节|SHA256|
|---|---:|---|
|reference-relocs-clang-22|212193208|`1a72e99d92b857524a82c5cff257b48fc72b56e6290f6b90cd5d0dadd31741f7`|
|llvm-bolt|571204360|`ec9b68d142ae1b588474c354b17da24523eb5c97f3ecda14bf544b699ac73dfb`|

实际pipeline输入由rewrite/bolt.log.argv.json确认，是`clang-bolt/reference-relocs-clang-22`。helper:L1546先重链，L1547执行`llvm-strip --strip-debug`，L1548交给rewrite；因此本文件已经strip-debug，**尚未strip-all**，不是重新链接或臆造的“未strip”输入。原argv及复制前后身份在identities.json/options.json。

D根的`build/bin/merge-fdata`不存在；全根只读find命中的3个merge-fdata均为源/构建目录，不是可执行文件。未找到libbolt_rt_instr.a或其他libbolt_rt*。find对/root、var/cache/ldconfig、usr/share/upgrade有权限盲区，原文保留；不提权、不声称检查了不可读目录。通常工具位置和构建目录均已直接核对，所需工具无法按用户指定来源取得。

58号生产工具流程仅ninja llvm-bolt（111+2任务），未构建merge-fdata和插桩runtime；已有docs/bolt/01:L68、02工具清单也区分这些独立目标。本轮不允许运行cmake/ninja/gbs，且不能从其他历史根替代D工具，故按最保守规则停止该项，继续第二项。

```text
ITEM1 已结束 2026-11-05T00:11:43.545431+08:00 status=stopped reason=missing-D-root-merge-fdata-and-instrumentation-runtime
SERVICE 已结束 2026-11-05T00:11:44.701881+08:00 status=ok reason=exit-0
```

## 2. Source1200采集方法与本次计划

主线docs/16_bolt_final.md:L125–135原始argv采用`-instrument --thread-count=1 -runtime-instrumentation-lib=.../libbolt_rt_instr.a -instrumentation-file=.../profiles/clang -instrumentation-file-append-pid -instrumentation-binpath=.../instrumented/bin/clang-22`。tools/collect_bolt_profile.py:L63要求13份ARM输入；tools/extend_bolt_profile_aarch64.py:L38要求10份AArch64输入，L69每TU新增一个PID fdata，L77–81保留13份旧profile并合并23份。这是**BOLT插桩**；未用perf。

本次可复用47/58号已核对的同23份训练输入，完整路径、SHA、目标与编译参数见training.json。本轮未运行训练，不能声称取得新的PGO适配fdata。与旧采集的计划差异为编译器换成本次PGO clang、运行loader/库改用D根、输出改到本次新目录；不能声称命令整体与旧版相同。旧原件/脚本没有运行，因为它们会写旧路径并删除临时文件。

正式优化参数直接从3ee2d847 helper的OPTIONS提取（顺序不变）：

```text
-reorder-blocks=ext-tsp -reorder-functions=cdsort -split-functions -split-all-cold -split-eh -dyno-stats --thread-count=1 -stale-threshold=5 -use-old-text
```

完整正式argv见options.json中的pipeline_input_argv；5%门槛未改。D根loader/运行库不需要chroot，但缺少merge/runtime已阻止进入这一步。

## 3. PGO+BOLT完整流程资源估算表

cgroup含文件缓存。58号为独立服务内核峰值；55号为阶段memory.current采样最大值，**口径不同，不能把55号值称为同精度峰值**。磁盘均是根边界或60秒采样最大值，不保证瞬时峰值。其他行借用非PGO历史值只作估算，不宣称PGO后不变。

|阶段|时间s|cgroup B|进程VmHWM B|根磁盘B|来源/性质|
|---|---:|---:|---:|---:|---|
|A插桩clang构建|4068.547|7227248640|5930262528|26444713984|58§4，本次PGO实测；只构建clang/runtime|
|B IR训练|201.930|1481818112|1046290432|26444713984|58§4实测；根外profraw746313472B|
|C IR合并|3.278|1824751616|1976971264|26444713984|58§4实测；根外profdata52528216B|
|PGO普通编译|6176（日志）|21703991296|13305700352|UNKNOWN（出口du超时）|58§4实测|
|PGO普通安装|328（日志）|11565408256|65052672（gbs采样，非安装工具完整峰值）|60700127232|58§4实测|
|BOLT插桩|NOT RUN|UNKNOWN|UNKNOWN|UNKNOWN|本项缺工具|
|BOLT训练与fdata合并|NOT RUN|UNKNOWN|UNKNOWN|UNKNOWN|本项缺工具|
|PGO输入BOLT正式优化|NOT RUN|UNKNOWN|UNKNOWN|UNKNOWN|本项未生成新profile；58旧profile失败不能代替成功数据|
|缓存释放|9|3716710400|UNKNOWN|UNKNOWN|55§7 T非PGO实测，借用估算|
|静态库转换|2544|10596343808|UNKNOWN|55093010432|55§7 T非PGO实测，借用估算|
|平台后处理|700|7375040512|UNKNOWN|47143387136|55§7 T非PGO实测，借用估算|
|打包|292|10014306304|UNKNOWN|42598031360|55§7 T非PGO实测，借用估算|

54/55号非PGO llvm-bolt自身VmHWM为9,931,661,312B；本次没有执行llvm-bolt，比较项UNKNOWN，不能拿58号BOLT阶段ld.lld的VmHWM或cgroup值冒充llvm-bolt自身。

两个构建根同时保留：58号已观测A24.629GiB + D60.378GiB，边界组合85.007GiB，真实峰值UNKNOWN。若借用55号非PGO D峰值70,485,561,344B，A+D合计96,930,275,328B（90.274GiB），还需单列根外profraw/profdata约0.744GiB、新复制文件783,397,568B及尚未知的BOLT插桩/fdata/优化输出。再加30GiB运行保留线得到约121.75GiB的**已知部分规划下界**，不是可保证的完整容量预算；PGO普通编译磁盘出口缺采样、新插桩产物未测，不给伪精确总量。

## 4. 保留现场

证据：`tools/bolt/results/pgo-bolt-followup-20261105/`，包含原文来源、缺工具检查、复制身份、训练清单、正式OPTIONS、独立服务argv/资源/结束行。新实验目录仅存复制件，所有历史根只读。没有sudo、弹窗、删除或发布代码改动。

结论：前置调查完成，实际BOLT补测未运行；缺D根merge-fdata和插桩runtime，等待用户后续决定。
