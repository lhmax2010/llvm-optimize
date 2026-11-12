# 84. 资源拆分第一步（已有证据，未重新构建）

结论：PASS（完成已有数据的拆分；不能恢复的细项明确记为 UNKNOWN）。本报告不排候选优先级、不判断收益是否可以接受。

## 1. 口径与读取边界

已读设计 v9 §2.2、§2.4、§4.1/4.2、§6，63/74 号材料、57/77/79 号身份记录；逐行读取下表九份完整 x86_64 GBS 日志、本地三份原始内存/进程/du采样、最终build-result，以及只读构建树中的 .ninja_log 和 build.ninja。没有访问 QB 网站，没有读取或修改 LLVM Git 仓库，没有运行 clang/lld/CMake/Ninja/GBS，没有重测构建。83号的微型夹具不作为资源样本。

分析在 MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、Nice=19、IOSchedulingClass=idle 的串行用户服务中完成。解析代码和原始读取清单：[analyze_resources.py](../../tools/bolt/results/night-82-84-20261113/84/analyze_resources.py)、[read-inputs.json](../../tools/bolt/results/night-82-84-20261113/84/read-inputs.json)；本地ThinLTO规则原文/行号/SHA：[thinlto-build-rules.json](../../tools/bolt/results/night-82-84-20261113/84/thinlto-build-rules.json)；完整结构化结果：[all-results.json](../../tools/bolt/results/night-82-84-20261113/84/all-results.json)。

- GBS 时间为日志的整数秒；只用明确起止行相减。表中“总日志窗口”是 0 到最后一条 GBS 时间戳，不等于 controller 的墙钟时长。阶段可嵌套，不能相加。
- 普通Ninja窗口含链接。独立纯编译耗时 UNKNOWN：编译与链接并行，不能把链接时长从窗口相减。每个大链接用 .ninja_log 的 start_ms/end_ms；任务互相重叠，不能把五项求和当作串行耗时。
- QB只有Ninja完成行，无法恢复大链接起点；不把相邻完成行的间隔当成任务耗时。保留完成行原文作定位，时长记 UNKNOWN。
- 内存峰值是整个 cgroup（含文件缓存）；阶段内 memory.current 最大采样值只表示该时间窗口的整个组，不能归到一个链接器。单进程 VmHWM 仅有 llvm-bolt 采样，全构建最大单进程及其命令 UNKNOWN。
- 本地日志没有 cgroup memory.stat 的 anon/file；host /proc/meminfo 不能替代，均记 UNKNOWN。
- du是约60秒一次、单次50秒限时的根目录总量采样。峰值是成功采样最大值，不保证捕获瞬时峰值。没有分层du，完整主要目录分布 UNKNOWN；BOLT_DISK_REPORT 的有限作用域另列，不能等同整个构建根。
- 74-T memory.peak 等于 MemoryMax，max=3877、oom=0，记“≥ 限额（截断）”；时长标“受内存回收影响”，不作为资源候选的对照基线。D未触顶，按实测记录。

## 2. 各来源身份（全部 x86_64）

|来源|环境/项目|源码提交|快照|总日志窗口 s / 证据|
|---|---|---|---|---|
|63-T|local / Toolchain|9e39fa8a61392652bb28b75fc26216675bcad1d5|tizen-base-toolchain_20261030.061318|10351 / [gbs-original-0.log.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/gbs-original-0.log.gz)|
|74-T|local / Toolchain|fea0fe464d56e17f2c7588c557bfffd9f6ac352b|tizen-base-toolchain_20261030.061318|7863 / [original-build.log.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/original-build.log.gz)|
|74-D|local / Base-Dev|fea0fe464d56e17f2c7588c557bfffd9f6ac352b|tizen-base-dev_20261030.061217|3890 / [original-build.log.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/original-build.log.gz)|
|1216409|QB / Toolchain|9e39fa8a61392652bb28b75fc26216675bcad1d5|tizen-base-toolchain_20261030.061318|9115 / [llvm.buildlog.txt.gz](../../tools/bolt/results/qb-1216409-1216410/1216409/x86_64/llvm.buildlog.txt.gz)|
|1216410|QB / Base-Dev|9e39fa8a61392652bb28b75fc26216675bcad1d5|tizen-base-dev_20261030.061217|5816 / [llvm.buildlog.txt.gz](../../tools/bolt/results/qb-1216409-1216410/1216410/x86_64/llvm.buildlog.txt.gz)|
|1225393|QB / Toolchain|60fabc723f30c5cc04146a9dd83487ebed63f259|tizen-base-toolchain_20261030.061318|9200 / [llvm.buildlog.txt.gz](../../tools/bolt/results/qb-1225393-1225395/1225393/x86_64/llvm.buildlog.txt.gz)|
|1225395|QB / Base-Dev|60fabc723f30c5cc04146a9dd83487ebed63f259|tizen-base-dev_20261030.061217|5862 / [llvm.buildlog.txt.gz](../../tools/bolt/results/qb-1225393-1225395/1225395/x86_64/llvm.buildlog.txt.gz)|
|1226850|QB / Toolchain|fea0fe464d56e17f2c7588c557bfffd9f6ac352b|tizen-base-toolchain_20261030.061318|9138 / [llvm.buildlog.txt.gz](../../tools/bolt/results/qb-1226850-1226851/1226850/x86_64/llvm.buildlog.txt.gz)|
|1226851|QB / Base-Dev|fea0fe464d56e17f2c7588c557bfffd9f6ac352b|tizen-base-dev_20261030.061217|5801 / [llvm.buildlog.txt.gz](../../tools/bolt/results/qb-1226850-1226851/1226851/x86_64/llvm.buildlog.txt.gz)|

总日志窗口的最后时间戳、原文行号见 [log-window-endpoints.json](../../tools/bolt/results/night-82-84-20261113/84/log-window-endpoints.json)，源码路径保存在各来源 result.json；原始压缩文件大小与SHA见读取清单。不同源码、项目、环境分别列示，不合并成一次实验。

## 3. 63-T：local / Toolchain

提交 9e39fa8a61392652bb28b75fc26216675bcad1d5；快照 tizen-base-toolchain_20261030.061318。日志 [gbs-original-0.log.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/gbs-original-0.log.gz)；完整锚点 [anchors.txt](../../tools/bolt/results/night-82-84-20261113/84/63-T/anchors.txt)；数据 [result.json](../../tools/bolt/results/night-82-84-20261113/84/63-T/result.json)。

### 阶段时长

|阶段|秒|日志行/时间或字段|
|---|---:|---|
|CMake配置|58|L690 [183s] → L3259 [241s]|
|普通Ninja编译（含重叠链接）|4458|L3260 [241s] → L10981 [4699s]|
|普通安装至BOLT begin|374|L11345 [4700s] → L16924 [5074s]|
|BOLT begin至compare-root结束（含各子阶段）|1934|L16924 [5074s] → L24145 [7008s]|
|BOLT重新配置|14|L16971 [5290s] → L18922 [5304s]|
|BOLT工具构建|148|L23182 [5307s] → L23528 [5455s]|
|BOLT pipeline总窗口|1033|L24131 [5456s] → L24139 [6489s]|
|compare-root门禁|518|L24142 [6490s] → L24145 [7008s]|
|cache-release|122|L24146 [7008s] → L24147 [7130s]|
|静态库转换|2285|L24167 [7131s] → L24618 [9416s]|
|find-debuginfo开始至post门禁前的平台后处理|404|L24621 [9423s] → L25205 [9827s]|
|BOLT post门禁|27|L25205 [9827s] → L25209 [9854s]|
|RPM文件处理至最后Wrote|489|L25212 [9857s] → L25681 [10346s]|
|BOLT重新链接|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|reference strip|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|candidate strip|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|BOLT rewrite|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|RUNPATH调整|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|tiny门禁|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|security门禁|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|real gate prestrip|26.412496|L24132，BOLT_REAL_GATE_PASS.seconds|
|debug symbols门禁|8.678917|L24133，BOLT_DEBUG_SYMBOLS_PASS.seconds|
|debuglink门禁|7.30451|L24135，BOLT_DEBUGLINK_PASS.debuglink_seconds|
|real gate preinstall|8.401841|L24136，BOLT_REAL_GATE_PASS.seconds|
|real gate post|7.659572|L25206，BOLT_REAL_GATE_PASS.seconds|

### 五个大链接

|目标|秒|起止/原始证据|
|---|---:|---|
|clang|955.511|2886972 → 3842483 ms；[.ninja_log](/home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/.ninja_log):L8034；原文 <code>2886972 / 3842483 / 1793884568328692913 / bin/clang-22 / ce06141be8593158</code>|
|libLLVM.so|1830.958|715325 → 2546283 ms；[.ninja_log](/home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/.ninja_log):L6539；原文 <code>715325 / 2546283 / 1793882396681606757 / lib64/libLLVM.so.22.1 / bdb65336becd43db</code>|
|libclang-cpp.so|323.003|2625017 → 2948020 ms；[.ninja_log](/home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/.ninja_log):L7253；原文 <code>2625017 / 2948020 / 1793884306373682520 / lib64/libclang-cpp.so.22.1 / 14385b5f5078bf50</code>|
|lld|426.968|3952091 → 4379059 ms；[.ninja_log](/home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/.ninja_log):L8457；原文 <code>3952091 / 4379059 / 1793885633446735169 / bin/lld / 6fb684c1133c5261</code>|
|liblldb|41.357|3870758 → 3912115 ms；[.ninja_log](/home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/.ninja_log):L8269；原文 <code>3870758 / 3912115 / 1793885552113731942 / lib64/liblldb.so.22.1.8 / d9e7ca4c2b22340a</code>|

### 内存与磁盘

|量|结果|证据|
|---|---|---|
|cgroup memory.peak（含文件缓存）|18533765120 B|[build-result.json](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/build-result.json)：stats.memory.peak / memory.max；首次峰值采样 [resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz):L1650；2026-11-05T21:20:12.227114+08:00|
|memory.events|{"low": 0, "high": 0, "max": 0, "oom": 0, "oom_kill": 0, "oom_group_kill": 0}|[build-result.json](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/build-result.json)：stats.memory.events；原始序列末次 [resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz):L5096；2026-11-05T23:16:41.151188+08:00|
|构建服务墙钟秒|10370.224069；未观测到memory.events max触顶|[build-result.json](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/build-result.json)：seconds|
|anon / file|UNKNOWN / UNKNOWN|原始 resources 没有 memory.stat；未用宿主机数据代替|
|全构建最大单进程 VmHWM / 命令|UNKNOWN / UNKNOWN|只有 llvm-bolt 进程采样|
|llvm-bolt 已采样最大 VmHWM|9929744384 B|[bolt-process.jsonl](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/bolt-process.jsonl):L3855；2026-11-05T22:10:52.917402+08:00|

llvm-bolt 命令原文（对应上述 PID 记录）：

~~~text
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-bolt /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt/reference-relocs-clang-22 -o /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt/clang.bolt -data=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt/profile.fdata -reorder-blocks=ext-tsp -reorder-functions=cdsort -split-functions -split-all-cold -split-eh -dyno-stats --thread-count=1 -stale-threshold=5 -use-old-text
~~~

|磁盘量|结果|证据|
|---|---|---|
|构建根成功du最大值|67730743296 B|[du-root.jsonl](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/du-root.jsonl):L107；2026-11-05T22:09:52.692404+08:00|
|du样本总数 / 成功 / 超时 / 非零或缺失|173 / 116 / 50 / 57|[du-root.jsonl](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/du-root.jsonl)；超时包含在非零中，不相加|
|主要目录的分层峰值|UNKNOWN|历史du只测根总量|

阶段窗口内 cgroup memory.current 最大采样值（并发任务共用，不代表独占资源）：

|阶段|最大采样 B|来源/时间|
|---|---:|---|
|CMake配置|3743920128|[resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz):L122；2026-11-05T20:27:59.353407+08:00|
|普通Ninja编译（含重叠链接）|18465832960|[resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz):L1650；2026-11-05T21:20:12.227114+08:00|
|普通安装至BOLT begin|12894543872|[resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz):L2349；2026-11-05T21:43:46.632988+08:00|
|BOLT begin至compare-root结束（含各子阶段）|15773831168|[resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz):L3145；2026-11-05T22:10:53.280393+08:00|
|BOLT重新配置|7781556224|[resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz):L2604；2026-11-05T21:52:23.134210+08:00|
|BOLT工具构建|13309165568|[resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz):L2679；2026-11-05T21:54:53.847640+08:00|
|BOLT pipeline总窗口|15773831168|[resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz):L3145；2026-11-05T22:10:53.280393+08:00|
|compare-root门禁|9267843072|[resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz):L3184；2026-11-05T22:12:11.618674+08:00|
|cache-release|5733998592|[resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz):L3433；2026-11-05T22:20:53.927749+08:00|
|静态库转换|15946149888|[resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz):L4563；2026-11-05T22:58:49.209564+08:00|
|find-debuginfo开始至post门禁前的平台后处理|8046120960|[resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz):L4665；2026-11-05T23:02:14.462148+08:00|
|BOLT post门禁|8691818496|[resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz):L4842；2026-11-05T23:08:11.113187+08:00|
|RPM文件处理至最后Wrote|12610822144|[resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz):L5075；2026-11-05T23:15:58.973920+08:00|
|clang|18465832960|[resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz):L1650；2026-11-05T21:20:12.227114+08:00|
|libLLVM.so|14771875840|[resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz):L1329；2026-11-05T21:09:27.289292+08:00|
|libclang-cpp.so|17218625536|[resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz):L1500；2026-11-05T21:15:10.727215+08:00|
|lld|18369339392|[resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz):L2265；2026-11-05T21:40:57.285716+08:00|
|liblldb|9823481856|[resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz):L2034；2026-11-05T21:33:12.594799+08:00|

BOLT有限作用域的已记录磁盘量（不是整个根的分层du；每个数对应原始 BOLT_DISK_REPORT 行）：

|阶段|GBS s / 行 / 记录时间|work B|tool_objects B|tool_executable B|tool_library合计 B|cache正分配delta B|
|---|---|---:|---:|---:|---:|---:|
|begin|5074 / L16924 / 2026-11-05T21:48:34.307082+08:00|0|0|0|UNKNOWN|UNKNOWN|
|tool-built|5456 / L24130 / 2026-11-05T21:54:56.029737+08:00|1995563008|146677760|566865920|146665472|1233014784|
|pipeline|6490 / L24141 / 2026-11-05T22:12:10.703200+08:00|2935140352|146677760|566870016|146665472|1233014784|
|post|9854 / L25211 / 2026-11-05T23:08:14.874124+08:00|3089850368|146677760|566870016|146665472|0|

## 4. 74-T：local / Toolchain

提交 fea0fe464d56e17f2c7588c557bfffd9f6ac352b；快照 tizen-base-toolchain_20261030.061318。日志 [original-build.log.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/original-build.log.gz)；完整锚点 [anchors.txt](../../tools/bolt/results/night-82-84-20261113/84/74-T/anchors.txt)；数据 [result.json](../../tools/bolt/results/night-82-84-20261113/84/74-T/result.json)。

### 阶段时长

|阶段|秒|日志行/时间或字段|
|---|---:|---|
|CMake配置|42|L637 [175s] → L3206 [217s]|
|普通Ninja编译（含重叠链接）|3896|L3207 [217s] → L10928 [4113s]|
|普通安装至BOLT begin|191|L11292 [4114s] → L16872 [4305s]|
|BOLT begin至compare-root结束（含各子阶段）|749|L16872 [4305s] → L24098 [5054s]|
|BOLT重新配置|10|L16920 [4452s] → L18871 [4462s]|
|BOLT工具构建|124|L23131 [4464s] → L23477 [4588s]|
|BOLT pipeline总窗口|348|L24082 [4588s] → L24090 [4936s]|
|compare-root门禁|117|L24095 [4937s] → L24098 [5054s]|
|cache-release|4|L24099 [5054s] → L24101 [5058s]|
|静态库转换|1984|L24122 [5060s] → L24574 [7044s]|
|find-debuginfo开始至post门禁前的平台后处理|376|L24577 [7047s] → L25161 [7423s]|
|BOLT post门禁|24|L25161 [7423s] → L25165 [7447s]|
|RPM文件处理至最后Wrote|406|L25170 [7450s] → L25639 [7856s]|
|BOLT重新链接|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|reference strip|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|candidate strip|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|BOLT rewrite|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|RUNPATH调整|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|tiny门禁|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|security门禁|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|real gate prestrip|19.599657|L24083，BOLT_REAL_GATE_PASS.seconds|
|debug symbols门禁|3.347537|L24084，BOLT_DEBUG_SYMBOLS_PASS.seconds|
|debuglink门禁|1.933019|L24086，BOLT_DEBUGLINK_PASS.debuglink_seconds|
|real gate preinstall|22.819021|L24087，BOLT_REAL_GATE_PASS.seconds|
|real gate post|7.158449|L25162，BOLT_REAL_GATE_PASS.seconds|

### 五个大链接

|目标|秒|起止/原始证据|
|---|---:|---|
|clang|1101.7|2387528 → 3489228 ms；[.ninja_log](/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/.ninja_log):L8307；原文 <code>2387528 / 3489228 / 1794412806468649625 / bin/clang-22 / ce06141be8593158</code>|
|libLLVM.so|737.258|662634 → 1399892 ms；[.ninja_log](/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/.ninja_log):L4669；原文 <code>662634 / 1399892 / 1794411081574581194 / lib64/libLLVM.so.22.1 / bdb65336becd43db</code>|
|libclang-cpp.so|1184.95|1711210 → 2896160 ms；[.ninja_log](/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/.ninja_log):L7249；原文 <code>1711210 / 2896160 / 1794412130150622794 / lib64/libclang-cpp.so.22.1 / 14385b5f5078bf50</code>|
|lld|222.465|3502440 → 3724905 ms；[.ninja_log](/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/.ninja_log):L8427；原文 <code>3502440 / 3724905 / 1794413921380693857 / bin/lld / 6fb684c1133c5261</code>|
|liblldb|35.737|3413096 → 3448833 ms；[.ninja_log](/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/.ninja_log):L8246；原文 <code>3413096 / 3448833 / 1794413832036690312 / lib64/liblldb.so.22.1.8 / d9e7ca4c2b22340a</code>|

### 内存与磁盘

|量|结果|证据|
|---|---|---|
|cgroup memory.peak（含文件缓存）|≥ 24482992128 B（限额截断；计数器读值 24482992128）|[build-result.json](../../tools/bolt/results/local-full-r6-20261111/toolchain/build-result.json)：stats.memory.peak / memory.max；首次峰值采样 [resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/resources.jsonl.gz):L1488；2026-11-12T00:07:19.890445+08:00|
|memory.events|{"low": 0, "high": 0, "max": 3877, "oom": 0, "oom_kill": 0, "oom_group_kill": 0}|[build-result.json](../../tools/bolt/results/local-full-r6-20261111/toolchain/build-result.json)：stats.memory.events；原始序列末次 [resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/resources.jsonl.gz):L3887；2026-11-12T01:27:47.193623+08:00|
|构建服务墙钟秒|7875.230391；受内存回收影响|[build-result.json](../../tools/bolt/results/local-full-r6-20261111/toolchain/build-result.json)：seconds|
|anon / file|UNKNOWN / UNKNOWN|原始 resources 没有 memory.stat；未用宿主机数据代替|
|全构建最大单进程 VmHWM / 命令|UNKNOWN / UNKNOWN|只有 llvm-bolt 进程采样|
|llvm-bolt 已采样最大 VmHWM|9911152640 B|[bolt-process.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/bolt-process.jsonl.gz):L3481；2026-11-12T00:37:39.123446+08:00|

llvm-bolt 命令原文（对应上述 PID 记录）：

~~~text
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-bolt /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt/reference-relocs-clang-22 -o /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt/clang.bolt -data=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt/profile.fdata -reorder-blocks=ext-tsp -reorder-functions=cdsort -split-functions -split-all-cold -split-eh -dyno-stats --thread-count=1 -stale-threshold=5 -use-old-text
~~~

|磁盘量|结果|证据|
|---|---|---|
|构建根成功du最大值|67924271104 B|[du-root.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/du-root.jsonl.gz):L81；2026-11-12T00:36:35.705157+08:00|
|du样本总数 / 成功 / 超时 / 非零或缺失|132 / 91 / 32 / 41|[du-root.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/du-root.jsonl.gz)；超时包含在非零中，不相加|
|主要目录的分层峰值|UNKNOWN|历史du只测根总量|

阶段窗口内 cgroup memory.current 最大采样值（并发任务共用，不代表独占资源）：

|阶段|最大采样 B|来源/时间|
|---|---:|---|
|CMake配置|4334379008|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/resources.jsonl.gz):L111；2026-11-11T23:20:16.721913+08:00|
|普通Ninja编译（含重叠链接）|24482992128|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/resources.jsonl.gz):L1500；2026-11-12T00:07:43.995599+08:00|
|普通安装至BOLT begin|18861355008|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/resources.jsonl.gz):L2092；2026-11-12T00:27:34.446239+08:00|
|BOLT begin至compare-root结束（含各子阶段）|19720630272|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/resources.jsonl.gz):L2340；2026-11-12T00:35:52.946574+08:00|
|BOLT重新配置|14329933824|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/resources.jsonl.gz):L2195；2026-11-12T00:31:01.431312+08:00|
|BOLT工具构建|18147221504|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/resources.jsonl.gz):L2258；2026-11-12T00:33:08.012633+08:00|
|BOLT pipeline总窗口|19720630272|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/resources.jsonl.gz):L2340；2026-11-12T00:35:52.946574+08:00|
|compare-root门禁|6478233600|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/resources.jsonl.gz):L2432；2026-11-12T00:38:58.628805+08:00|
|cache-release|6185476096|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/resources.jsonl.gz):L2490；2026-11-12T00:40:55.291681+08:00|
|静态库转换|15945318400|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/resources.jsonl.gz):L3479；2026-11-12T01:14:02.155034+08:00|
|find-debuginfo开始至post门禁前的平台后处理|10600947712|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/resources.jsonl.gz):L3491；2026-11-12T01:14:26.262149+08:00|
|BOLT post门禁|10542161920|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/resources.jsonl.gz):L3676；2026-11-12T01:20:43.431112+08:00|
|RPM文件处理至最后Wrote|18198597632|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/resources.jsonl.gz):L3871；2026-11-12T01:27:15.025798+08:00|
|clang|24482992128|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/resources.jsonl.gz):L1500；2026-11-12T00:07:43.995599+08:00|
|libLLVM.so|11443593216|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/resources.jsonl.gz):L600；2026-11-11T23:36:39.657206+08:00|
|libclang-cpp.so|24482992128|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/resources.jsonl.gz):L1500；2026-11-12T00:07:43.995599+08:00|
|lld|24482357248|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/resources.jsonl.gz):L1917；2026-11-12T00:21:42.512988+08:00|
|liblldb|18813722624|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/toolchain/resources.jsonl.gz):L1799；2026-11-12T00:17:45.477841+08:00|

BOLT有限作用域的已记录磁盘量（不是整个根的分层du；每个数对应原始 BOLT_DISK_REPORT 行）：

|阶段|GBS s / 行 / 记录时间|work B|tool_objects B|tool_executable B|tool_library合计 B|cache正分配delta B|
|---|---|---:|---:|---:|---:|---:|
|begin|4305 / L16872 / 2026-11-12T00:28:25.944602+08:00|0|0|0|UNKNOWN|UNKNOWN|
|tool-built|4588 / L24080 / 2026-11-12T00:33:09.698560+08:00|1995563008|146677760|566865920|146669568|1233039360|
|pipeline|4937 / L24093 / 2026-11-12T00:38:58.233443+08:00|2935136256|146677760|566870016|146669568|1233039360|
|post|7447 / L25168 / 2026-11-12T01:20:48.942526+08:00|3089846272|146677760|566870016|146669568|0|

## 5. 74-D：local / Base-Dev

提交 fea0fe464d56e17f2c7588c557bfffd9f6ac352b；快照 tizen-base-dev_20261030.061217。日志 [original-build.log.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/original-build.log.gz)；完整锚点 [anchors.txt](../../tools/bolt/results/night-82-84-20261113/84/74-D/anchors.txt)；数据 [result.json](../../tools/bolt/results/night-82-84-20261113/84/74-D/result.json)。

### 阶段时长

|阶段|秒|日志行/时间或字段|
|---|---:|---|
|CMake配置|34|L588 [248s] → L3157 [282s]|
|普通Ninja编译（含重叠链接）|2191|L3158 [282s] → L10879 [2473s]|
|普通安装至BOLT begin|4|L11243 [2474s] → L16817 [2478s]|
|BOLT begin至compare-root结束（含各子阶段）|157|L16817 [2478s] → L24041 [2635s]|
|BOLT重新配置|7|L16865 [2481s] → L18816 [2488s]|
|BOLT工具构建|87|L23076 [2489s] → L23422 [2576s]|
|BOLT pipeline总窗口|57|L24027 [2577s] → L24033 [2634s]|
|compare-root门禁|1|L24038 [2634s] → L24041 [2635s]|
|cache-release|1|L24042 [2635s] → L24044 [2636s]|
|静态库转换|1168|L24065 [2636s] → L24517 [3804s]|
|find-debuginfo开始至post门禁前的平台后处理|6|L24520 [3805s] → L24901 [3811s]|
|BOLT post门禁|5|L24901 [3811s] → L24905 [3816s]|
|RPM文件处理至最后Wrote|70|L24910 [3819s] → L25167 [3889s]|
|BOLT重新链接|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|reference strip|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|candidate strip|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|BOLT rewrite|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|RUNPATH调整|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|tiny门禁|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|security门禁|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|real gate prestrip|4.122809|L24028，BOLT_REAL_GATE_PASS.seconds|
|real gate preinstall|4.020605|L24030，BOLT_REAL_GATE_PASS.seconds|
|real gate post|3.916588|L24902，BOLT_REAL_GATE_PASS.seconds|

release 未执行独立 debug symbols/debuglink 门禁，其时长为 N/A，不填0。

### 五个大链接

|目标|秒|起止/原始证据|
|---|---:|---|
|clang|156.064|1770916 → 1926980 ms；[.ninja_log](/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/.ninja_log):L7665；原文 <code>1770916 / 1926980 / 1794421986338013817 / bin/clang-22 / 5d104410b389af75</code>|
|libLLVM.so|94.512|526370 → 620882 ms；[.ninja_log](/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/.ninja_log):L3827；原文 <code>526370 / 620882 / 1794420741791964442 / lib64/libLLVM.so.22.1 / ecf0930f84c26ba0</code>|
|libclang-cpp.so|76.732|1027167 → 1103899 ms；[.ninja_log](/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/.ninja_log):L4892；原文 <code>1027167 / 1103899 / 1794421242588984310 / lib64/libclang-cpp.so.22.1 / cc5002ab77e701d7</code>|
|lld|77.941|2029454 → 2107395 ms；[.ninja_log](/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/.ninja_log):L8410；原文 <code>2029454 / 2107395 / 1794422244876024074 / bin/lld / 4f3f4c77fae04dad</code>|
|liblldb|19.0|1586176 → 1605176 ms；[.ninja_log](/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/.ninja_log):L6421；原文 <code>1586176 / 1605176 / 1794421801598006487 / lib64/liblldb.so.22.1.8 / 3c83db55c6b4678</code>|

### 内存与磁盘

|量|结果|证据|
|---|---|---|
|cgroup memory.peak（含文件缓存）|18161836032 B|[build-result.json](../../tools/bolt/results/local-full-r6-20261111/basedev/build-result.json)：stats.memory.peak / memory.max；首次峰值采样 [resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/resources.jsonl.gz):L1307；2026-11-12T02:42:30.436226+08:00|
|memory.events|{"low": 0, "high": 0, "max": 0, "oom": 0, "oom_kill": 0, "oom_group_kill": 0}|[build-result.json](../../tools/bolt/results/local-full-r6-20261111/basedev/build-result.json)：stats.memory.events；原始序列末次 [resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/resources.jsonl.gz):L1941；2026-11-12T03:03:44.616001+08:00|
|构建服务墙钟秒|3900.702903；未观测到memory.events max触顶|[build-result.json](../../tools/bolt/results/local-full-r6-20261111/basedev/build-result.json)：seconds|
|anon / file|UNKNOWN / UNKNOWN|原始 resources 没有 memory.stat；未用宿主机数据代替|
|全构建最大单进程 VmHWM / 命令|UNKNOWN / UNKNOWN|只有 llvm-bolt 进程采样|
|llvm-bolt 已采样最大 VmHWM|9924120576 B|[bolt-process.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/bolt-process.jsonl.gz):L3431；2026-11-12T02:42:30.278838+08:00|

llvm-bolt 命令原文（对应上述 PID 记录）：

~~~text
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-bolt /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt/reference-relocs-clang-22 -o /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt/clang.bolt -data=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt/profile.fdata -reorder-blocks=ext-tsp -reorder-functions=cdsort -split-functions -split-all-cold -split-eh -dyno-stats --thread-count=1 -stale-threshold=5 -use-old-text
~~~

|磁盘量|结果|证据|
|---|---|---|
|构建根成功du最大值|14028967936 B|[du-root.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/du-root.jsonl.gz):L59；2026-11-12T02:56:44.991340+08:00|
|du样本总数 / 成功 / 超时 / 非零或缺失|66 / 66 / 0 / 0|[du-root.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/du-root.jsonl.gz)；超时包含在非零中，不相加|
|主要目录的分层峰值|UNKNOWN|历史du只测根总量|

阶段窗口内 cgroup memory.current 最大采样值（并发任务共用，不代表独占资源）：

|阶段|最大采样 B|来源/时间|
|---|---:|---|
|CMake配置|5122686976|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/resources.jsonl.gz):L144；2026-11-12T02:03:34.144757+08:00|
|普通Ninja编译（含重叠链接）|11902005248|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/resources.jsonl.gz):L1099；2026-11-12T02:35:32.724753+08:00|
|普通安装至BOLT begin|8761819136|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/resources.jsonl.gz):L1237；2026-11-12T02:40:09.797988+08:00|
|BOLT begin至compare-root结束（含各子阶段）|18123169792|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/resources.jsonl.gz):L1307；2026-11-12T02:42:30.436226+08:00|
|BOLT重新配置|9228918784|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/resources.jsonl.gz):L1242；2026-11-12T02:40:19.837353+08:00|
|BOLT工具构建|10664656896|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/resources.jsonl.gz):L1262；2026-11-12T02:41:00.024878+08:00|
|BOLT pipeline总窗口|18123169792|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/resources.jsonl.gz):L1307；2026-11-12T02:42:30.436226+08:00|
|cache-release|8222638080|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/resources.jsonl.gz):L1316；2026-11-12T02:42:48.524919+08:00|
|静态库转换|8333471744|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/resources.jsonl.gz):L1707；2026-11-12T02:55:53.866887+08:00|
|find-debuginfo开始至post门禁前的平台后处理|7196106752|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/resources.jsonl.gz):L1898；2026-11-12T03:02:18.197401+08:00|
|BOLT post门禁|7143145472|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/resources.jsonl.gz):L1902；2026-11-12T03:02:26.233970+08:00|
|RPM文件处理至最后Wrote|10406600704|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/resources.jsonl.gz):L1922；2026-11-12T03:03:06.411037+08:00|
|clang|11902005248|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/resources.jsonl.gz):L1099；2026-11-12T02:35:32.724753+08:00|
|libLLVM.so|8858959872|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/resources.jsonl.gz):L443；2026-11-12T02:13:34.753410+08:00|
|libclang-cpp.so|9614360576|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/resources.jsonl.gz):L685；2026-11-12T02:21:40.993305+08:00|
|lld|9297674240|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/resources.jsonl.gz):L1189；2026-11-12T02:38:33.430099+08:00|
|liblldb|8290254848|[resources.jsonl.gz](../../tools/bolt/results/local-full-r6-20261111/basedev/resources.jsonl.gz):L942；2026-11-12T02:30:17.426156+08:00|

BOLT有限作用域的已记录磁盘量（不是整个根的分层du；每个数对应原始 BOLT_DISK_REPORT 行）：

|阶段|GBS s / 行 / 记录时间|work B|tool_objects B|tool_executable B|tool_library合计 B|cache正分配delta B|
|---|---|---:|---:|---:|---:|---:|
|begin|2478 / L16817 / 2026-11-12T02:40:10.961405+08:00|0|0|0|UNKNOWN|UNKNOWN|
|tool-built|2577 / L24025 / 2026-11-12T02:41:49.950037+08:00|370499584|16089088|47284224|16461824|93855744|
|pipeline|2634 / L24036 / 2026-11-12T02:42:47.501604+08:00|1274572800|16089088|47284224|16461824|93855744|
|post|3816 / L24908 / 2026-11-12T03:02:29.920736+08:00|1429270528|16089088|47284224|16461824|0|

## 6. 1216409：QB / Toolchain

提交 9e39fa8a61392652bb28b75fc26216675bcad1d5；快照 tizen-base-toolchain_20261030.061318。日志 [llvm.buildlog.txt.gz](../../tools/bolt/results/qb-1216409-1216410/1216409/x86_64/llvm.buildlog.txt.gz)；完整锚点 [anchors.txt](../../tools/bolt/results/night-82-84-20261113/84/1216409/anchors.txt)；数据 [result.json](../../tools/bolt/results/night-82-84-20261113/84/1216409/result.json)。

### 阶段时长

|阶段|秒|日志行/时间或字段|
|---|---:|---|
|CMake配置|41|L733 [34s] → L3302 [75s]|
|普通Ninja编译（含重叠链接）|4204|L3303 [75s] → L11024 [4279s]|
|普通安装至BOLT begin|36|L11388 [4279s] → L16967 [4315s]|
|BOLT begin至compare-root结束（含各子阶段）|345|L16967 [4315s] → L24188 [4660s]|
|BOLT重新配置|10|L17014 [4335s] → L18965 [4345s]|
|BOLT工具构建|152|L23225 [4347s] → L23571 [4499s]|
|BOLT pipeline总窗口|126|L24174 [4500s] → L24182 [4626s]|
|compare-root门禁|34|L24185 [4626s] → L24188 [4660s]|
|cache-release|2|L24189 [4660s] → L24190 [4662s]|
|静态库转换|3984|L24210 [4662s] → L24661 [8646s]|
|find-debuginfo开始至post门禁前的平台后处理|134|L24664 [8649s] → L25256 [8783s]|
|BOLT post门禁|15|L25256 [8783s] → L25260 [8798s]|
|RPM文件处理至最后Wrote|314|L25263 [8799s] → L25732 [9113s]|
|BOLT重新链接|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|reference strip|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|candidate strip|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|BOLT rewrite|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|RUNPATH调整|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|tiny门禁|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|security门禁|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|real gate prestrip|4.098861|L24175，BOLT_REAL_GATE_PASS.seconds|
|debug symbols门禁|2.363561|L24176，BOLT_DEBUG_SYMBOLS_PASS.seconds|
|debuglink门禁|1.851375|L24178，BOLT_DEBUGLINK_PASS.debuglink_seconds|
|real gate preinstall|4.156708|L24179，BOLT_REAL_GATE_PASS.seconds|
|real gate post|4.480566|L25257，BOLT_REAL_GATE_PASS.seconds|

### 五个大链接

|目标|秒|起止/原始证据|
|---|---:|---|
|clang|UNKNOWN|仅完成 L10374 [3892s]；起点UNKNOWN|
|libLLVM.so|UNKNOWN|仅完成 L6640 [1315s]；起点UNKNOWN|
|libclang-cpp.so|UNKNOWN|仅完成 L7660 [2273s]；起点UNKNOWN|
|lld|UNKNOWN|仅完成 L10939 [4126s]；起点UNKNOWN|
|liblldb|UNKNOWN|仅完成 L9096 [3313s]；起点UNKNOWN|

### 内存与磁盘

cgroup memory.peak / memory.events / anon / file / 最大单进程 VmHWM及命令 / 根du峰值 / 分层du：**全部 UNKNOWN**。保存的QB包日志没有这些采样；没有把机器内存容量或BOLT自身统计当成cgroup/进程峰值。

BOLT有限作用域的已记录磁盘量（不是整个根的分层du；每个数对应原始 BOLT_DISK_REPORT 行）：

|阶段|GBS s / 行 / 记录时间|work B|tool_objects B|tool_executable B|tool_library合计 B|cache正分配delta B|
|---|---|---:|---:|---:|---:|---:|
|begin|4315 / L16967 / 2026-11-03T18:30:45.021240+08:00|0|0|0|UNKNOWN|UNKNOWN|
|tool-built|4500 / L24173 / 2026-11-03T18:33:50.303847+08:00|1995583488|146677760|566865920|146665472|1233039360|
|pipeline|4626 / L24184 / 2026-11-03T18:35:56.480036+08:00|2935140352|146677760|566870016|146665472|1233039360|
|post|8798 / L25262 / 2026-11-03T19:45:28.760849+08:00|3089850368|146677760|566870016|146665472|0|

## 7. 1216410：QB / Base-Dev

提交 9e39fa8a61392652bb28b75fc26216675bcad1d5；快照 tizen-base-dev_20261030.061217。日志 [llvm.buildlog.txt.gz](../../tools/bolt/results/qb-1216409-1216410/1216410/x86_64/llvm.buildlog.txt.gz)；完整锚点 [anchors.txt](../../tools/bolt/results/night-82-84-20261113/84/1216410/anchors.txt)；数据 [result.json](../../tools/bolt/results/night-82-84-20261113/84/1216410/result.json)。

### 阶段时长

|阶段|秒|日志行/时间或字段|
|---|---:|---|
|CMake配置|24|L684 [84s] → L3253 [108s]|
|普通Ninja编译（含重叠链接）|3329|L3254 [108s] → L10975 [3437s]|
|普通安装至BOLT begin|2|L11339 [3437s] → L16912 [3439s]|
|BOLT begin至compare-root结束（含各子阶段）|230|L16912 [3439s] → L24131 [3669s]|
|BOLT重新配置|5|L16959 [3444s] → L18910 [3449s]|
|BOLT工具构建|126|L23170 [3450s] → L23516 [3576s]|
|BOLT pipeline总窗口|90|L24119 [3577s] → L24125 [3667s]|
|compare-root门禁|2|L24128 [3667s] → L24131 [3669s]|
|cache-release|1|L24132 [3669s] → L24133 [3670s]|
|静态库转换|2036|L24153 [3670s] → L24604 [5706s]|
|find-debuginfo开始至post门禁前的平台后处理|4|L24607 [5707s] → L24988 [5711s]|
|BOLT post门禁|7|L24988 [5711s] → L24992 [5718s]|
|RPM文件处理至最后Wrote|98|L24995 [5718s] → L25252 [5816s]|
|BOLT重新链接|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|reference strip|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|candidate strip|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|BOLT rewrite|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|RUNPATH调整|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|tiny门禁|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|security门禁|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|real gate prestrip|3.739329|L24120，BOLT_REAL_GATE_PASS.seconds|
|real gate preinstall|3.690507|L24122，BOLT_REAL_GATE_PASS.seconds|
|real gate post|3.525455|L24989，BOLT_REAL_GATE_PASS.seconds|

release 未执行独立 debug symbols/debuglink 门禁，其时长为 N/A，不填0。

### 五个大链接

|目标|秒|起止/原始证据|
|---|---:|---|
|clang|UNKNOWN|仅完成 L10236 [3186s]；起点UNKNOWN|
|libLLVM.so|UNKNOWN|仅完成 L6531 [1112s]；起点UNKNOWN|
|libclang-cpp.so|UNKNOWN|仅完成 L7554 [1899s]；起点UNKNOWN|
|lld|UNKNOWN|仅完成 L10890 [3369s]；起点UNKNOWN|
|liblldb|UNKNOWN|仅完成 L9040 [2789s]；起点UNKNOWN|

### 内存与磁盘

cgroup memory.peak / memory.events / anon / file / 最大单进程 VmHWM及命令 / 根du峰值 / 分层du：**全部 UNKNOWN**。保存的QB包日志没有这些采样；没有把机器内存容量或BOLT自身统计当成cgroup/进程峰值。

BOLT有限作用域的已记录磁盘量（不是整个根的分层du；每个数对应原始 BOLT_DISK_REPORT 行）：

|阶段|GBS s / 行 / 记录时间|work B|tool_objects B|tool_executable B|tool_library合计 B|cache正分配delta B|
|---|---|---:|---:|---:|---:|---:|
|begin|3439 / L16912 / 2026-11-03T18:07:20.797260+08:00|0|0|0|UNKNOWN|UNKNOWN|
|tool-built|3577 / L24118 / 2026-11-03T18:09:38.203837+08:00|370511872|16089088|47284224|16461824|93880320|
|pipeline|3667 / L24127 / 2026-11-03T18:11:08.879610+08:00|1274576896|16089088|47284224|16461824|93880320|
|post|5718 / L24994 / 2026-11-03T18:45:19.452416+08:00|1429270528|16089088|47284224|16461824|0|

## 8. 1225393：QB / Toolchain

提交 60fabc723f30c5cc04146a9dd83487ebed63f259；快照 tizen-base-toolchain_20261030.061318。日志 [llvm.buildlog.txt.gz](../../tools/bolt/results/qb-1225393-1225395/1225393/x86_64/llvm.buildlog.txt.gz)；完整锚点 [anchors.txt](../../tools/bolt/results/night-82-84-20261113/84/1225393/anchors.txt)；数据 [result.json](../../tools/bolt/results/night-82-84-20261113/84/1225393/result.json)。

### 阶段时长

|阶段|秒|日志行/时间或字段|
|---|---:|---|
|CMake配置|37|L733 [34s] → L3302 [71s]|
|普通Ninja编译（含重叠链接）|4198|L3303 [72s] → L11024 [4270s]|
|普通安装至BOLT begin|36|L11388 [4270s] → L16968 [4306s]|
|BOLT begin至compare-root结束（含各子阶段）|359|L16968 [4306s] → L24194 [4665s]|
|BOLT重新配置|11|L17016 [4340s] → L18967 [4351s]|
|BOLT工具构建|152|L23227 [4352s] → L23573 [4504s]|
|BOLT pipeline总窗口|124|L24178 [4506s] → L24186 [4630s]|
|compare-root门禁|35|L24191 [4630s] → L24194 [4665s]|
|cache-release|3|L24195 [4665s] → L24197 [4668s]|
|静态库转换|4090|L24218 [4668s] → L24670 [8758s]|
|find-debuginfo开始至post门禁前的平台后处理|117|L24673 [8759s] → L25265 [8876s]|
|BOLT post门禁|15|L25265 [8876s] → L25269 [8891s]|
|RPM文件处理至最后Wrote|305|L25274 [8892s] → L25743 [9197s]|
|BOLT重新链接|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|reference strip|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|candidate strip|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|BOLT rewrite|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|RUNPATH调整|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|tiny门禁|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|security门禁|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|real gate prestrip|4.049648|L24179，BOLT_REAL_GATE_PASS.seconds|
|debug symbols门禁|2.355354|L24180，BOLT_DEBUG_SYMBOLS_PASS.seconds|
|debuglink门禁|2.07442|L24182，BOLT_DEBUGLINK_PASS.debuglink_seconds|
|real gate preinstall|4.129989|L24183，BOLT_REAL_GATE_PASS.seconds|
|real gate post|4.283787|L25266，BOLT_REAL_GATE_PASS.seconds|

### 五个大链接

|目标|秒|起止/原始证据|
|---|---:|---|
|clang|UNKNOWN|仅完成 L10351 [3879s]；起点UNKNOWN|
|libLLVM.so|UNKNOWN|仅完成 L6651 [1303s]；起点UNKNOWN|
|libclang-cpp.so|UNKNOWN|仅完成 L7674 [2278s]；起点UNKNOWN|
|lld|UNKNOWN|仅完成 L10939 [4125s]；起点UNKNOWN|
|liblldb|UNKNOWN|仅完成 L9095 [3313s]；起点UNKNOWN|

### 内存与磁盘

cgroup memory.peak / memory.events / anon / file / 最大单进程 VmHWM及命令 / 根du峰值 / 分层du：**全部 UNKNOWN**。保存的QB包日志没有这些采样；没有把机器内存容量或BOLT自身统计当成cgroup/进程峰值。

BOLT有限作用域的已记录磁盘量（不是整个根的分层du；每个数对应原始 BOLT_DISK_REPORT 行）：

|阶段|GBS s / 行 / 记录时间|work B|tool_objects B|tool_executable B|tool_library合计 B|cache正分配delta B|
|---|---|---:|---:|---:|---:|---:|
|begin|4306 / L16968 / 2026-11-11T00:41:57.892356+08:00|0|0|0|UNKNOWN|UNKNOWN|
|tool-built|4506 / L24176 / 2026-11-11T00:45:18.005191+08:00|1995583488|146677760|566865920|146665472|1233043456|
|pipeline|4630 / L24189 / 2026-11-11T00:47:22.859461+08:00|2935140352|146677760|566870016|146665472|1233043456|
|post|8891 / L25272 / 2026-11-11T01:58:23.555230+08:00|3089854464|146677760|566870016|146665472|0|

## 9. 1225395：QB / Base-Dev

提交 60fabc723f30c5cc04146a9dd83487ebed63f259；快照 tizen-base-dev_20261030.061217。日志 [llvm.buildlog.txt.gz](../../tools/bolt/results/qb-1225393-1225395/1225395/x86_64/llvm.buildlog.txt.gz)；完整锚点 [anchors.txt](../../tools/bolt/results/night-82-84-20261113/84/1225395/anchors.txt)；数据 [result.json](../../tools/bolt/results/night-82-84-20261113/84/1225395/result.json)。

### 阶段时长

|阶段|秒|日志行/时间或字段|
|---|---:|---|
|CMake配置|24|L684 [86s] → L3253 [110s]|
|普通Ninja编译（含重叠链接）|3342|L3254 [110s] → L10975 [3452s]|
|普通安装至BOLT begin|2|L11339 [3452s] → L16913 [3454s]|
|BOLT begin至compare-root结束（含各子阶段）|231|L16913 [3454s] → L24137 [3685s]|
|BOLT重新配置|5|L16961 [3459s] → L18912 [3464s]|
|BOLT工具构建|126|L23172 [3465s] → L23518 [3591s]|
|BOLT pipeline总窗口|91|L24123 [3592s] → L24129 [3683s]|
|compare-root门禁|2|L24134 [3683s] → L24137 [3685s]|
|cache-release|1|L24138 [3685s] → L24140 [3686s]|
|静态库转换|2065|L24161 [3686s] → L24613 [5751s]|
|find-debuginfo开始至post门禁前的平台后处理|5|L24616 [5752s] → L24997 [5757s]|
|BOLT post门禁|6|L24997 [5757s] → L25001 [5763s]|
|RPM文件处理至最后Wrote|99|L25006 [5763s] → L25263 [5862s]|
|BOLT重新链接|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|reference strip|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|candidate strip|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|BOLT rewrite|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|RUNPATH调整|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|tiny门禁|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|security门禁|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|real gate prestrip|3.777885|L24124，BOLT_REAL_GATE_PASS.seconds|
|real gate preinstall|3.709663|L24126，BOLT_REAL_GATE_PASS.seconds|
|real gate post|3.494366|L24998，BOLT_REAL_GATE_PASS.seconds|

release 未执行独立 debug symbols/debuglink 门禁，其时长为 N/A，不填0。

### 五个大链接

|目标|秒|起止/原始证据|
|---|---:|---|
|clang|UNKNOWN|仅完成 L10235 [3203s]；起点UNKNOWN|
|libLLVM.so|UNKNOWN|仅完成 L6519 [1119s]；起点UNKNOWN|
|libclang-cpp.so|UNKNOWN|仅完成 L7544 [1910s]；起点UNKNOWN|
|lld|UNKNOWN|仅完成 L10890 [3384s]；起点UNKNOWN|
|liblldb|UNKNOWN|仅完成 L9040 [2804s]；起点UNKNOWN|

### 内存与磁盘

cgroup memory.peak / memory.events / anon / file / 最大单进程 VmHWM及命令 / 根du峰值 / 分层du：**全部 UNKNOWN**。保存的QB包日志没有这些采样；没有把机器内存容量或BOLT自身统计当成cgroup/进程峰值。

BOLT有限作用域的已记录磁盘量（不是整个根的分层du；每个数对应原始 BOLT_DISK_REPORT 行）：

|阶段|GBS s / 行 / 记录时间|work B|tool_objects B|tool_executable B|tool_library合计 B|cache正分配delta B|
|---|---|---:|---:|---:|---:|---:|
|begin|3454 / L16913 / 2026-11-11T00:19:15.358697+08:00|0|0|0|UNKNOWN|UNKNOWN|
|tool-built|3592 / L24121 / 2026-11-11T00:21:33.560439+08:00|370511872|16089088|47284224|16461824|93847552|
|pipeline|3683 / L24132 / 2026-11-11T00:23:04.607069+08:00|1274576896|16089088|47284224|16461824|93847552|
|post|5763 / L25004 / 2026-11-11T00:57:44.673287+08:00|1429270528|16089088|47284224|16461824|0|

## 10. 1226850：QB / Toolchain

提交 fea0fe464d56e17f2c7588c557bfffd9f6ac352b；快照 tizen-base-toolchain_20261030.061318。日志 [llvm.buildlog.txt.gz](../../tools/bolt/results/qb-1226850-1226851/1226850/x86_64/llvm.buildlog.txt.gz)；完整锚点 [anchors.txt](../../tools/bolt/results/night-82-84-20261113/84/1226850/anchors.txt)；数据 [result.json](../../tools/bolt/results/night-82-84-20261113/84/1226850/result.json)。

### 阶段时长

|阶段|秒|日志行/时间或字段|
|---|---:|---|
|CMake配置|42|L733 [32s] → L3302 [74s]|
|普通Ninja编译（含重叠链接）|4199|L3303 [74s] → L11024 [4273s]|
|普通安装至BOLT begin|34|L11388 [4273s] → L16968 [4307s]|
|BOLT begin至compare-root结束（含各子阶段）|330|L16968 [4307s] → L24194 [4637s]|
|BOLT重新配置|10|L17016 [4327s] → L18967 [4337s]|
|BOLT工具构建|141|L23227 [4339s] → L23573 [4480s]|
|BOLT pipeline总窗口|128|L24178 [4481s] → L24186 [4609s]|
|compare-root门禁|28|L24191 [4609s] → L24194 [4637s]|
|cache-release|2|L24195 [4637s] → L24197 [4639s]|
|静态库转换|4055|L24218 [4639s] → L24670 [8694s]|
|find-debuginfo开始至post门禁前的平台后处理|127|L24673 [8695s] → L25265 [8822s]|
|BOLT post门禁|15|L25265 [8822s] → L25269 [8837s]|
|RPM文件处理至最后Wrote|294|L25274 [8839s] → L25743 [9133s]|
|BOLT重新链接|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|reference strip|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|candidate strip|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|BOLT rewrite|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|RUNPATH调整|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|tiny门禁|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|security门禁|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|real gate prestrip|4.113914|L24179，BOLT_REAL_GATE_PASS.seconds|
|debug symbols门禁|2.379652|L24180，BOLT_DEBUG_SYMBOLS_PASS.seconds|
|debuglink门禁|2.040842|L24182，BOLT_DEBUGLINK_PASS.debuglink_seconds|
|real gate preinstall|4.051948|L24183，BOLT_REAL_GATE_PASS.seconds|
|real gate post|4.457706|L25266，BOLT_REAL_GATE_PASS.seconds|

### 五个大链接

|目标|秒|起止/原始证据|
|---|---:|---|
|clang|UNKNOWN|仅完成 L10356 [3879s]；起点UNKNOWN|
|libLLVM.so|UNKNOWN|仅完成 L6618 [1307s]；起点UNKNOWN|
|libclang-cpp.so|UNKNOWN|仅完成 L7638 [2267s]；起点UNKNOWN|
|lld|UNKNOWN|仅完成 L10939 [4121s]；起点UNKNOWN|
|liblldb|UNKNOWN|仅完成 L9096 [3306s]；起点UNKNOWN|

### 内存与磁盘

cgroup memory.peak / memory.events / anon / file / 最大单进程 VmHWM及命令 / 根du峰值 / 分层du：**全部 UNKNOWN**。保存的QB包日志没有这些采样；没有把机器内存容量或BOLT自身统计当成cgroup/进程峰值。

BOLT有限作用域的已记录磁盘量（不是整个根的分层du；每个数对应原始 BOLT_DISK_REPORT 行）：

|阶段|GBS s / 行 / 记录时间|work B|tool_objects B|tool_executable B|tool_library合计 B|cache正分配delta B|
|---|---|---:|---:|---:|---:|---:|
|begin|4307 / L16968 / 2026-11-11T22:55:27.647634+08:00|0|0|0|UNKNOWN|UNKNOWN|
|tool-built|4481 / L24176 / 2026-11-11T22:58:21.527453+08:00|1995583488|146677760|566865920|146665472|1233010688|
|pipeline|4609 / L24189 / 2026-11-11T23:00:29.873969+08:00|2935140352|146677760|566870016|146665472|1233010688|
|post|8837 / L25272 / 2026-11-12T00:10:57.832461+08:00|3089846272|146677760|566870016|146665472|0|

## 11. 1226851：QB / Base-Dev

提交 fea0fe464d56e17f2c7588c557bfffd9f6ac352b；快照 tizen-base-dev_20261030.061217。日志 [llvm.buildlog.txt.gz](../../tools/bolt/results/qb-1226850-1226851/1226851/x86_64/llvm.buildlog.txt.gz)；完整锚点 [anchors.txt](../../tools/bolt/results/night-82-84-20261113/84/1226851/anchors.txt)；数据 [result.json](../../tools/bolt/results/night-82-84-20261113/84/1226851/result.json)。

### 阶段时长

|阶段|秒|日志行/时间或字段|
|---|---:|---|
|CMake配置|24|L684 [82s] → L3253 [106s]|
|普通Ninja编译（含重叠链接）|3310|L3254 [106s] → L10975 [3416s]|
|普通安装至BOLT begin|1|L11339 [3416s] → L16913 [3417s]|
|BOLT begin至compare-root结束（含各子阶段）|229|L16913 [3417s] → L24137 [3646s]|
|BOLT重新配置|5|L16961 [3422s] → L18912 [3427s]|
|BOLT工具构建|125|L23172 [3428s] → L23518 [3553s]|
|BOLT pipeline总窗口|90|L24123 [3554s] → L24129 [3644s]|
|compare-root门禁|2|L24134 [3644s] → L24137 [3646s]|
|cache-release|1|L24138 [3646s] → L24140 [3647s]|
|静态库转换|2042|L24161 [3647s] → L24613 [5689s]|
|find-debuginfo开始至post门禁前的平台后处理|4|L24616 [5690s] → L24997 [5694s]|
|BOLT post门禁|7|L24997 [5694s] → L25001 [5701s]|
|RPM文件处理至最后Wrote|100|L25006 [5701s] → L25263 [5801s]|
|BOLT重新链接|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|reference strip|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|candidate strip|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|BOLT rewrite|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|RUNPATH调整|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|tiny门禁|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|security门禁|UNKNOWN|no isolated start/end in preserved command logs; no inference from adjacent stdout gaps|
|real gate prestrip|3.749738|L24124，BOLT_REAL_GATE_PASS.seconds|
|real gate preinstall|3.642523|L24126，BOLT_REAL_GATE_PASS.seconds|
|real gate post|3.534202|L24998，BOLT_REAL_GATE_PASS.seconds|

release 未执行独立 debug symbols/debuglink 门禁，其时长为 N/A，不填0。

### 五个大链接

|目标|秒|起止/原始证据|
|---|---:|---|
|clang|UNKNOWN|仅完成 L10240 [3176s]；起点UNKNOWN|
|libLLVM.so|UNKNOWN|仅完成 L6525 [1105s]；起点UNKNOWN|
|libclang-cpp.so|UNKNOWN|仅完成 L7548 [1887s]；起点UNKNOWN|
|lld|UNKNOWN|仅完成 L10890 [3353s]；起点UNKNOWN|
|liblldb|UNKNOWN|仅完成 L9040 [2777s]；起点UNKNOWN|

### 内存与磁盘

cgroup memory.peak / memory.events / anon / file / 最大单进程 VmHWM及命令 / 根du峰值 / 分层du：**全部 UNKNOWN**。保存的QB包日志没有这些采样；没有把机器内存容量或BOLT自身统计当成cgroup/进程峰值。

BOLT有限作用域的已记录磁盘量（不是整个根的分层du；每个数对应原始 BOLT_DISK_REPORT 行）：

|阶段|GBS s / 行 / 记录时间|work B|tool_objects B|tool_executable B|tool_library合计 B|cache正分配delta B|
|---|---|---:|---:|---:|---:|---:|
|begin|3417 / L16913 / 2026-11-11T22:32:23.854728+08:00|0|0|0|UNKNOWN|UNKNOWN|
|tool-built|3554 / L24121 / 2026-11-11T22:34:40.113313+08:00|370511872|16089088|47284224|16461824|93863936|
|pipeline|3644 / L24132 / 2026-11-11T22:36:10.572373+08:00|1274576896|16089088|47284224|16461824|93863936|
|post|5701 / L25004 / 2026-11-11T23:10:27.500294+08:00|1429274624|16089088|47284224|16461824|0|

## 12. 候选项预判（不排序，不推断收益）

下表占比仅为同一来源该阶段实测秒数 / 该来源总GBS日志窗口。列顺序用于溯源，不是性能排名。74-T列只是描述已发生的构建，**受内存回收影响，禁止作为候选实验对照基线**。BOLT重链复用列用pipeline窗口定位；重链自身占比 UNKNOWN。门禁行列出三次real gate耗时总量作上界定位，复制自身占比 UNKNOWN。RPM行是文件处理至Wrote窗口，压缩自身占比 UNKNOWN。这些窗口不能直接等同可节省时间。

|候选/所对应阶段|63-T|74-T|74-D|1216409|1216410|1225393|1225395|1226850|1226851|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|并行度：普通Ninja含链接|4458s / 43.07%|3896s / 49.55%|2191s / 56.32%|4204s / 46.12%|3329s / 57.24%|4198s / 45.63%|3342s / 57.01%|4199s / 45.95%|3310s / 57.06%|
|静态库转换调度：转换窗口|2285s / 22.08%|1984s / 25.23%|1168s / 30.03%|3984s / 43.71%|2036s / 35.01%|4090s / 44.46%|2065s / 35.23%|4055s / 44.38%|2042s / 35.20%|
|BOLT重链复用：pipeline窗口（重链自身UNKNOWN）|1033s / 9.98%|348s / 4.43%|57s / 1.47%|126s / 1.38%|90s / 1.55%|124s / 1.35%|91s / 1.55%|128s / 1.40%|90s / 1.55%|
|门禁复制瘦身：三次real gate（复制自身UNKNOWN）|42.473909s / 0.41%|49.577127s / 0.63%|12.060001s / 0.31%|12.736135s / 0.14%|10.95529s / 0.19%|12.463423s / 0.14%|10.981914s / 0.19%|12.623569s / 0.14%|10.926463s / 0.19%|
|find-debuginfo并发：平台后处理窗口|404s / 3.90%|376s / 4.78%|6s / 0.15%|134s / 1.47%|4s / 0.07%|117s / 1.27%|5s / 0.09%|127s / 1.39%|4s / 0.07%|
|RPM压缩：文件处理/打包窗口（压缩自身UNKNOWN）|489s / 4.72%|406s / 5.16%|70s / 1.80%|314s / 3.44%|98s / 1.69%|305s / 3.32%|99s / 1.69%|294s / 3.22%|100s / 1.72%|
|中间产物清理：峰值时刻/目录占比|UNKNOWN（有限BOLT作用域见本源表）|UNKNOWN（有限BOLT作用域见本源表）|UNKNOWN（有限BOLT作用域见本源表）|UNKNOWN（有限BOLT作用域见本源表）|UNKNOWN（有限BOLT作用域见本源表）|UNKNOWN（有限BOLT作用域见本源表）|UNKNOWN（有限BOLT作用域见本源表）|UNKNOWN（有限BOLT作用域见本源表）|UNKNOWN（有限BOLT作用域见本源表）|
|非安装目标：可去除任务占比|UNKNOWN（未做依赖闭包分析）|UNKNOWN（未做依赖闭包分析）|UNKNOWN（未做依赖闭包分析）|UNKNOWN（未做依赖闭包分析）|UNKNOWN（未做依赖闭包分析）|UNKNOWN（未做依赖闭包分析）|UNKNOWN（未做依赖闭包分析）|UNKNOWN（未做依赖闭包分析）|UNKNOWN（未做依赖闭包分析）|

并行度还涉及五个链接任务和BOLT工具构建，两者的独立实测窗口见各来源表，不能和普通Ninja占比相加。“中间产物清理”对应缓存释放/构建后段，是否早于峰值、究竟能降低多少磁盘，现有稀疏采样不能证明。没有执行任何资源优化、清理、并行度调整或重新构建。

## 13. 能恢复与待补项

- 已恢复：九份日志的CMake、普通Ninja含链接、BOLT工具构建/pipeline/compare-root、三次real门禁、转换、后处理、打包窗口；本地三次各五个ThinLTO链接独立任务计时；本地cgroup峰值/events及llvm-bolt采样VmHWM；本地根du成功样本峰值和失败/超时计数。
- 不能恢复：QB五个链接起点和独立耗时；纯编译排除链接的独占墙钟；BOLT重链/strip/rewrite/RUNPATH/tiny/security细分耗时；全构建进程最大VmHWM及命令；cgroup anon/file；完整分层磁盘峰值；各候选的实际收益。统一 UNKNOWN，不事后推算。
- 74-T：≥24,482,992,128 B（截断）、max 3877、oom 0；其构建耗时受内存回收影响。74-D memory.peak=18,161,836,032 B，max 0；74-T du 32次超时，根峰值67,924,271,104 B只是91次成功样本的最大值。
- 下一次计划内构建需要事先增加链接独立进程计时/VmHWM、memory.stat anon/file、连续df与分层du，以及helper各子命令的显式起止。此次没有改入口采样逻辑。

~~~text
84 已结束 2026-11-13T00:56:47.575244+08:00 status=PASS
~~~
