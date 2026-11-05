# 59：PGO clang 的 BOLT 资源补测（工具补齐，补测完成）

工具已补齐，23份训练、新profile合并和正式参数BOLT优化成功，R=0.005089%通过原5%门槛。优化llvm-bolt自身VmHWM为8.280GiB，比非PGO同口径低10.48%；但use-old-text因原.text容量不足发出警告，实际未strip输出为259,324,032字节。23份-O2用例三轮中位数：nonPGO BOLT 120.362s、PGO 108.553s、PGO+BOLT 104.708s；清理仅限批准两处，详情见61号。

**第1–4节保留首次缺工具的历史停止记录；第5–8节是本轮补齐后的最新结论。**

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


## 5. 2026-11-05 补齐工具后的实测（本节起为最新结果）

用户本轮允许复用同版本工具，或缺失时在新目录构建两个目标。实际找到16号原采集工具，未运行cmake/ninja，也没有编译任何目标。原工具对应13号§1记录的源码提交`f111162e94aa48ed367c9d2c039456c70e7160ae`；其bolt树与`3ee2d847`均为`3b71c6953c01c28c95956fcf79906e4ed1fc052c`。对旧根bolt/实际1,154个文件逐个计算Git blob hash，与3ee逐个一致，额外文件0；CMakeCache版本和两个工具--version均为22.1.8。完整证据：resume/bolt-source-comparison.json、versions.json。

旧工具根：`W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/`，只读；复制到`W/temp/pgo-bolt-followup-20261105/tools/`。

|工具|原路径（相对build）|字节|复制前后SHA256|
|---|---|---:|---|
|merge-fdata|bin/merge-fdata|11891568|`9a725e368f39cc9fbaaf32fe8698ea3e1d120fee7de565373e376e3fc759a6a7`|
|libbolt_rt_instr.a|lib64/libbolt_rt_instr.a|33468|`4d00fc0a9c00913892ef2a3851a44a1c0ba39b695c7c9ca463883f317a9916ff`|

### 5.1 输入、流程和边界

继续使用§1已核对的D根reference-relocs-clang-22副本及D根llvm-bolt副本；输入SHA再次核对一致。插桩参数直接沿16号§4，只换本次路径；通过D根loader和运行库启动，不chroot。23份训练输入逐个核对training.json的SHA，13 ARM+10 AArch64，保留清单的完整编译参数（真实TU含-O3，3个合成TU为-O2）；resource-dir和sysroot也按该清单原样使用。每次编译前后清点fdata，要求恰好新增1个非空文件；23/23通过。原来采集也是BOLT插桩，不是perf。

没有改Source1200或发布OPTIONS。正式优化完整argv见resume/optimize/bolt-optimize.argv.json；使用3ee helper的match_counts原函数离线判定，成功退出+已核对工具身份后才调用，R和S/N仍各不超过5%。这次是资源/训练实验，不是完整打包、安装或90TU认证。

每步独立systemd用户服务，MemoryMax=24,482,992,128B（本机MemTotal−8GiB）、MemorySwapMax=0、CPUQuota=1200%、nice10、ionice2/7。每2秒采样各PID的VmHWM/命令及磁盘可用空间，另用time -v记录每个命令的完整最大RSS；保留30GiB磁盘停止线。服务与阶段均有带时区结束行。没有OOM；所有产物保留。

### 5.2 资源与文件

|步骤|阶段耗时s|cgroup memory.peak B（含文件缓存）|进程VmHWM B（2秒采样）|time -v 最大RSS B|
|---|---:|---:|---:|---:|
|instrument|77.954|17074352128|17014747136|17014747136|
|train|379.427|3890348032|1293144064|1293144064|
|merge|3.396|1585553408|1162305536|1369427968|
|optimize|44.984|8712601600|8890351616|8890351616|
|speed|1175.357|4953731072|1204346880|1205088256|

VmHWM按完整cmdline识别，loader启动的进程Name为ld-linux-x86-64，不误称为loader本身的工作集；完整PID/命令见step-resource-summary.json。merge仅约3秒，2秒采样低于time -v；不把采样下界冒充完整峰值。cgroup含缓存但共享页按内核记账归属，可能小于进程RSS，不能把两者相加。阶段耗时含SHA/清单落盘及初始化，speed阶段还会读取大编译器文件核对身份；这些额外时间不计入三轮编译中位数。命令本身耗时见各commands.json。

|产物|逻辑字节|SHA256/证据|
|---|---:|---|
|插桩clang|577278208|`d43b3cfcaa264f84ba248b64e55de4e4cf794b29ca075d77195fe8f93b4491b3`|
|23份fdata合计|3006326841|train/profiles.json逐文件SHA|
|merged.fdata|194262069|`6dbac6326e419b37d60334ed4a8614e31547799bc97d98ac49e67199c02b9d55`|
|PGO+BOLT clang，未strip/打包|259324032|`f2914387cfa1f3140078f6cb98fb85b8560d48b3ff7a10414b572c4883d868b5`|

优化llvm-bolt自身VmHWM为8,890,351,616B；54号非PGO同口径为9,931,661,312B，减少1,041,309,696B（10.485%），比值0.895153。这是两个具体输入的实测，不是通用PGO降内存保证。插桩峰值与优化峰值必须分开。

### 5.3 Profile与BOLT警告

```json
{"N": 19648, "M": 164430, "S": 0, "U": 1, "Q": 599, "R": 5.08931752252023e-05, "S_over_N": 0.0}
```

R=0.005089318%，S/N=0，PASS；54号非PGO T为N=23592/M=144032/S=0/U=1/Q=383，R=0.0042385453%。本次是不同PGO二进制和重新采集的profile，N/M/Q不要求与非PGO相同。58号同PGO输入配旧profile的85.3%失效已被本次新profile门禁通过所取代，但58号完整构建停止记录仍保留，不追认该构建成功。

原文及行号：

```text
instrument/bolt-instrument.log:L10: BOLT-WARNING: Failed to analyze 1551 relocations
instrument/bolt-instrument.log:L11: BOLT-WARNING: jump past end detected at 0x3ee314a in function _ZNK4llvm16AArch64InstrInfo18getBranchDestBlockERKNS_12MachineInstrE/1 : replacing with nop.
instrument/bolt-instrument.log:L12: BOLT-WARNING: jump past end detected at 0x4a05080 in function _ZNK4llvm12X86InstrInfo28convertToThreeAddressWithLEAEjRNS_12MachineInstrEPNS_13LiveVariablesEPNS_13LiveIntervalsEb/1 : replacing with nop.
instrument/bolt-instrument.log:L15: BOLT-INFO: 0 out of 164430 functions in the binary (0.0%) have non-empty execution profile
instrument/bolt-instrument.log:L17: BOLT-INSTRUMENTER: Number of indirect call site descriptors: 70849
instrument/bolt-instrument.log:L18: BOLT-INSTRUMENTER: Number of indirect call target descriptors: 163006
instrument/bolt-instrument.log:L19: BOLT-INSTRUMENTER: Number of function descriptors: 162992
instrument/bolt-instrument.log:L20: BOLT-INSTRUMENTER: Number of branch counters: 1775675
instrument/bolt-instrument.log:L21: BOLT-INSTRUMENTER: Number of ST leaf node counters: 893486
instrument/bolt-instrument.log:L22: BOLT-INSTRUMENTER: Number of direct call counters: 41
instrument/bolt-instrument.log:L23: BOLT-INSTRUMENTER: Total number of counters: 2669202
instrument/bolt-instrument.log:L24: BOLT-INSTRUMENTER: Total size of counters: 21353616 bytes (static alloc memory)
instrument/bolt-instrument.log:L25: BOLT-INSTRUMENTER: Total size of string table emitted: 19083062 bytes in file
instrument/bolt-instrument.log:L26: BOLT-INSTRUMENTER: Total size of descriptors: 183490244 bytes in file
instrument/bolt-instrument.log:L27: BOLT-INSTRUMENTER: Profile will be saved to file /home/linhao/Toolchain/development/llvm-optimize/temp/pgo-bolt-followup-20261105/profiles/clang
optimize/bolt-optimize.log:L8: BOLT-WARNING: Failed to analyze 1551 relocations
optimize/bolt-optimize.log:L10: BOLT-WARNING: jump past end detected at 0x3ee314a in function _ZNK4llvm16AArch64InstrInfo18getBranchDestBlockERKNS_12MachineInstrE/1 : replacing with nop.
optimize/bolt-optimize.log:L11: BOLT-WARNING: jump past end detected at 0x4a05080 in function _ZNK4llvm12X86InstrInfo28convertToThreeAddressWithLEAEjRNS_12MachineInstrEPNS_13LiveVariablesEPNS_13LiveIntervalsEb/1 : replacing with nop.
optimize/bolt-optimize.log:L15: BOLT-INFO: 19648 out of 164430 functions in the binary (11.9%) have non-empty execution profile
optimize/bolt-optimize.log:L16: BOLT-INFO: 599 functions with profile could not be optimized
optimize/bolt-optimize.log:L17: BOLT-INFO: profile for 1 objects was ignored
optimize/bolt-optimize.log:L67: BOLT-WARNING: --use-old-text failed. The original .text too small to fit the new code using 0x200000 alignment. 81469838 bytes needed, have 80783150 bytes available. Rebuilding without --use-old-text may produce a smaller binary
```

特别注意：`--use-old-text failed`是BOLT的警告，命令退出0；原.text可用80,783,150B、需要81,469,838B。没有去掉该参数、改对齐或重试。上表259,324,032B是实际输出的未strip ELF，不能拿它冒充发布包大小。1551个relocation分析警告和两处jump-past-end警告也完整保留，不隐去。

## 6. 三方编译速度（额外观察，不改变门禁结论）

同training.json的23份输入，所有-O*优化等级token移除后统一加-O2，其余参数不变；只做-c。三种编译器各3轮，每轮每种编译器顺序跑完23份，轮间轮换编译器顺序。通过各自根的loader/库启动：nonPGO BOLT来自55号T的clang.candidate，PGO来自D的ordinary-clang-22，PGO+BOLT来自本次optimize/clang-22。完整身份在speed/compiler-identities.json。没有用宿主编译器。

取每轮23份耗时之和，再取3轮中位数；time -v RSS取69次中最大值。未绑核、未关闭ASLR、没有清页缓存；未停止外部进程。每次记录load average，1分钟load范围2.31–32.06，存在明显负载高点；没有连续采样外部进程CPU，无法确认高load来源。该结果是训练集内观察，不外推到未见源码或Tizen全量构建。

|clang|三轮23份耗时s|中位数s|最大RSS B|相对nonPGO BOLT|
|---|---|---:|---:|---:|
|nonpgo-bolt|120.362, 107.038, 130.257|120.362|1178853376|1.000000|
|pgo|110.209, 106.972, 108.553|108.553|1205088256|0.901886|
|pgo-bolt|104.708, 104.284, 135.639|104.708|1195032576|0.869938|

异常耗时例：`speed/2-pgo-bolt-22.time`记录user=4.67s、system=0.17s、elapsed=32.64s、CPU=14%，不是32秒都在执行编译器CPU指令；原因未确认，原始记录保留。

**轮间波动明显**：nonPGO BOLT为107.038–130.257s，PGO+BOLT为104.284–135.639s；中位数的3.542%差小于轮间波动幅度，不能据此认定稳定加速，也不归因于某个未经证实的后台负载。

PGO+BOLT / PGO 中位数比=0.964577；相对PGO耗时变化=-3.542%。逐输入中位数与全部207次原始记录见speed-unit-medians.json、speed/measurements.json。编译器strip状态不同（nonPGO已strip，PGO ordinary含debug，PGO+BOLT未strip），因此首轮读取/缓存效应也属于本次观察条件，不声称是只控制代码布局的冷启动实验。

## 7. 更新后的PGO+BOLT完整资源估算

下表严格区分实测和借用；顺序执行的内存不能相加。58号kernel memory.peak与55号阶段采样memory.current口径不同。

|阶段|耗时s|cgroup B|进程VmHWM B|性质/来源|
|---|---:|---:|---:|---|
|PGO插桩clang构建|4068.547|7227248640|5930262528|58§4实测|
|IR训练|201.930|1481818112|1046290432|58§4实测；profraw746313472B|
|IR合并|3.278|1824751616|1976971264|58§4实测；profdata52528216B|
|PGO普通编译|6176|21703991296|13305700352|58§4实测|
|PGO普通安装|328|11565408256|65052672|58§4实测；进程峰值是所见gbs，非完整安装工具峰值|
|BOLT工具准备/构建及检查|418|UNKNOWN|UNKNOWN|58§4日志6772→7190实测；该子段内存未独立拆分|
|PGO重链/strip-debug|UNKNOWN|UNKNOWN|UNKNOWN|58§4的273s pipeline还含旧profile失败rewrite，不能直接归作重链时间|
|BOLT instrument|77.954|17074352128|17014747136|本次实测|
|BOLT train|379.427|3890348032|1293144064|本次实测|
|BOLT merge|3.396|1585553408|1162305536|本次实测|
|BOLT optimize|44.984|8712601600|8890351616|本次实测|
|缓存释放|9|3716710400|UNKNOWN|借用55§7 T非PGO采样值，估算|
|静态库转换|2544|10596343808|UNKNOWN|借用55§7 T非PGO采样值，估算|
|平台后处理|700|7375040512|UNKNOWN|借用55§7 T非PGO采样值，估算|
|打包|292|10014306304|UNKNOWN|借用55§7 T非PGO采样值，估算|

58号整个旧BOLT阶段为691s、cgroup 14,664,306,688B、进程峰值9,267,929,088B（ld.lld）；它包含工具准备、重链、strip-debug和失败rewrite，不拿来替代本次优化数据，也不直接与本次优化时间相加。A/D prepare另有117.427s/124.614s；本表不能直接求和冒充完整流水线耗时。

已测cgroup阶段最大为PGO普通编译21,703,991,296B（20.213GiB），不是将各阶段峰值相加；不代表尚未完成的PGO打包端到端上限。后处理和打包未对PGO产物重跑，借用值不能写作本次实测。

两根磁盘：58号A+D边界组合实测91,275,411,456B（85.007GiB），连续共存峰值UNKNOWN；普通编译出口du缺采样。借用55号T根采样峰值70,485,561,344B加A根26,444,713,984B，得96,930,275,328B（90.274GiB），这是估算而非本次同时测得。
本次补测目录（排除额外speed测试）的普通文件分配占用（st_blocks×512，不含目录块）4,948,119,552B（4.608GiB），分项在experiment-footprint.json；其中包含输入/工具副本、插桩输出、23份fdata、合并profile、优化输出和训练对象。为保留本实验全部现场，保守额外加上这份副本占用及根外IR profraw/profdata，得到102,677,236,568B（95.626GiB）已知部分规划值，加30GiB保留空间为125.626GiB。它可能重复保留生产流程中可复用的文件，且仍不是完整构建可保证峰值；真实PGO根峰值和后处理需要完整构建再测。speed额外产物独立列出，不计入构建需求。

## 8. 结束、清理与证据

按本轮授权只删除两处目录，详见[61号](61_disk_cleanup.md)。stage-A构建根已删除，但证据、profiles、objects保留；D根和其他历史根只读，没有重建、打包、源码修改或Gerrit推送。现有Source1200未改。本次工具复制、fdata、优化产物、全部速度测试输出保留。

```text
SERVICE 已结束 2026-11-05T10:11:20.528235+08:00 status=ok reason=exit-0
SERVICE 已结束 2026-11-05T10:17:53.763207+08:00 status=ok reason=exit-0
SERVICE 已结束 2026-11-05T10:18:02.573817+08:00 status=ok reason=exit-0
SERVICE 已结束 2026-11-05T10:18:48.662863+08:00 status=ok reason=exit-0
SERVICE 已结束 2026-11-05T10:38:26.052281+08:00 status=ok reason=exit-0
PGO_BOLT_FOLLOWUP 已结束 2026-11-05T10:38:26.061801+08:00 status=ok reason=completed
```

证据：`tools/bolt/results/pgo-bolt-followup-20261105/resume/`。结论：工具已补齐，23份采集、合并、正式参数优化和207次速度编译全部完成；profile门槛通过，use-old-text空间不足警告仍需另行考虑，未把实验当作完整发布验证。
