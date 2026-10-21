# 28 BOLT QB 超时日志分析（2026-10-21）

这份文件能确认的是 **QB 总控等待任务超时；A 最吻合，但“总时长阈值触发”仍是推测，日志没有写出 QB 阈值**。
能定位到的是总控等待子构建 **1202084** 的状态时被中断，不能定位 LLVM 究竟在普通编译、BOLT 重链还是后处理。
文件没有 `[NNNNs]` 包日志、Ninja 进度或 BOLT 运行标记，因此无法确认 9e5675f 的输出缓冲是否参与了超时，甚至不能确认导致等待超时的包就是 LLVM。
没有找到 506dc25 的原始 QB 包日志，**基线来自摘要，不是原始日志**；本次普通构建耗时也缺失，所以无法计算慢在哪一段、慢了多少。
本机另一份三架构日志来自不同构建和提交，已排除；不能拿它补本次缺失的编译时间线。

## 1. 输入身份与可确认信息

行号统一以用户给定的 `docs/quickbuild_logs/full-log.txt` 为准，记作 **P:L行号**。原文可从 [full-log.txt.gz](../../tools/bolt/results/qb-timeout-20261021/full-log.txt.gz) 无损解压；[excerpts.txt](../../tools/bolt/results/qb-timeout-20261021/excerpts.txt) 保留带原始行号的锚点和最后300行。未访问 QB、未查询/推送 Gerrit、未运行构建、未改源码或spec。只新增本报告及指定证据文件。

|项目|实际结果|证据|
|---|---|---|
|原文件大小|283,622 B（276.975 KiB）|对原始字节stat/len；无换行转换|
|总行数|2,698行，LF换行数2,698|wc -lc；末行为P:L2698|
|SHA256|`537754ed05cedc0280b57adf4af01f986e50b484a51646e3d5c64baeab6d5851`|原始文件全部字节；gzip解压后逐字节一致|
|日志层级|QB总控TRIGGER/master，非某架构LLVM包日志|P:L6、L12、L2313–2327|
|提交|`9e5675f57d122549997caffa39b655dfefc46fee`已用于源码checkout/导出|P:L204、L2243、L2246；未读到worker内二次提交身份|
|父/子构建|QB_TRIGGER_ID=1202070；报表链接到1202084|P:L1570、L2550–2551|
|架构|请求armv7l、aarch64、x86_64；实际超时架构未知|P:L19、L2549；总控导出ARCHITECTURE为空，不是x86_64包的证明|
|worker主机名|无法确认|只有workspace名称qbsource26_8947/8811（P:L1547、L2282），不能据此认定编译worker主机；未出现worker hostname|
|首条日志|`07:17:46,446`|P:L1，前置动作开始，不冒充独立QB startDate|
|末条带时戳日志|`07:17:57,458`|P:L2689，Build is timed out|
|最后物理行|Java堆栈，无时间戳|P:L2698|
|日期/时区|标签含20261019.071746；行首没有日期或时区|P:L1561；不能把分析日期2026-10-21当构建日期，也不擅自转北京时间|
|实际ninja -j、nproc|均未读到|全P:L1–2698，实际Ninja命令/进度和nproc均缺失|

关键身份原文：

```text
full-log.txt:L19: export CHILD_CONFIGURATIONS='standard-armv7l:aarch64:x86_64'
full-log.txt:L204: 07:17:55,557 INFO  - platform/upstream/llvm@9e5675f57d122549997caffa39b655dfefc46fee
full-log.txt:L2243: 07:18:01,717 INFO  -  + e2463165829c...9e5675f57d12 sandbox/lhmax2025/bolt_pgo -> origin/sandbox/lhmax2025/bolt_pgo  (forced update)
full-log.txt:L2244: 07:18:01,717 INFO  -  * [new branch]                sandbox/lhmax2025/llvm_optimize -> origin/sandbox/lhmax2025/llvm_optimize
full-log.txt:L2245: 07:18:03,124 INFO  - Previous HEAD position was f999bd406c0a Revert clang bootstrap + ThinLTO, fall back to GCC
full-log.txt:L2246: 07:18:03,125 INFO  - HEAD is now at 9e5675f57d12 packaging: optimize x86_64 clang with BOLT
full-log.txt:L2549:       <td>standard-armv7l:aarch64:x86_64</td>
full-log.txt:L2550:       <td><a href="https://quickbuild.tizen.org/build/1202084">https://quickbuild.tizen.org/build/1202084</a></td>
full-log.txt:L2551:       <td>FAILED</td>
full-log.txt:L2552:       <td><a href="https://quickbuild.tizen.org/build/1202084/build_profiling">Link</a></td>
```

### 并行度和超时数值：配置文本不等于执行证据

```text
full-log.txt:L387: 07:17:55,558 INFO  - DEFAULT_GBS_BUILD_CMD:
full-log.txt:L388: 07:17:55,558 INFO  - ---------------------------------
full-log.txt:L389: 07:17:55,558 INFO  - timeout 9h gbs build --threads=32 --define "jobs 8" --define "_smp_mflags -j8" --baselibs --clean-once --skip-srcrpm --style=tar
full-log.txt:L1509: 07:17:55,562 INFO  - USER_DEFINED_GBS_BUILD_CMD:
full-log.txt:L1510: 07:17:55,562 INFO  - ---------------------------------
full-log.txt:L1511: 07:17:55,562 INFO  - timeout 8h gbs build --threads=30 --define "jobs 8" --define "_smp_mflags -j8" --define "_costomized_smp_mflags -j20" --baselibs --clean-once --style=tar
full-log.txt:L1541: 07:17:55,562 INFO  - WORKER_N:
full-log.txt:L1542: 07:17:55,562 INFO  - ---------------------------------
full-log.txt:L1543: 07:17:55,562 INFO  - 28
```

能抄出的配置是 DEFAULT_GBS_BUILD_CMD 的 `timeout 9h`（32400秒）、`--threads=32`、jobs8/-j8，和 USER_DEFINED_GBS_BUILD_CMD 的 `timeout 8h`（28800秒）、`--threads=30`、jobs8/-j8、自定义宏 `_costomized_smp_mflags -j20`。拼写按原文保留。WORKER_N的值为28，但日志没有说明它等于CPU核数或实际同时运行的编译进程数。**不能把GBS的--threads当成Ninja -j，也不能把28当nproc。**

这些出现在参数展开中；没有读到实际worker启动命令、宏最终取值或shell timeout的124退出码，不能证明8h/9h中哪个实际生效。这两个值也不是日志明确声明的QB总控超时上限。

## 2. A/B/C/D 判断与停止原文

**更新结论：A，总控24小时时限，基本确认。** 用户补充确认：快照标签 `20261019.071746`（P:L1561）对应2026-10-19启动；P:L1为 `07:17:46,446`，次日P:L2321为 `07:17:46,444`，间隔 `86399.998秒`，距24小时只差2毫秒，随后P:L2689明确报 `Build is timed out.`。第11节取得的子构建概览也显示其在2026-10-19启动。尚未读到QB后台配置项本身，但不再把是否跨日当成未定问题。

本次只更新本节结论并追加第11节；报告开头及原有条件计算保留为8b5ea408的历史分析。**总控24小时与子构建自身记录的47小时56分不能混为一谈**，子构建为何拖延须以第11节证据和限制为准。

```text
full-log.txt:L2321: 07:17:46,444 INFO  - Executing post-execute action...
full-log.txt:L2322: 07:17:46,445 ERROR - Step 'master>TRIGGER>Parallel_Build>Trigger_Each_Build?REPO_ARCHS=standard-armv7l:aarch64:x86_64' is failed.
full-log.txt:L2323:     java.lang.RuntimeException: java.lang.InterruptedException
full-log.txt:L2324:     	at com.pmease.quickbuild.util.WaitableHashMap.waitFor(WaitableHashMap.java:93)
full-log.txt:L2325:     	at com.pmease.quickbuild.grid.NodeServiceImpl.getBuildStatus(NodeServiceImpl.java:279)
full-log.txt:L2326:     	at com.pmease.quickbuild.plugin.basis.TriggerBuildStep.run(TriggerBuildStep.java:308)
full-log.txt:L2689: 07:17:57,458 ERROR - Build is timed out.
full-log.txt:L2690:     java.util.concurrent.TimeoutException: Timed out waiting for task completion.
full-log.txt:L2691:     	at com.pmease.quickbuild.grid.GridTaskFuture.get(GridTaskFuture.java:148)
full-log.txt:L2692:     	at com.pmease.quickbuild.DefaultBuildEngine.run(DefaultBuildEngine.java:645)
full-log.txt:L2693:     	at com.pmease.quickbuild.DefaultBuildEngine.process(DefaultBuildEngine.java:482)
full-log.txt:L2694:     	at com.pmease.quickbuild.DefaultBuildEngine.access$000(DefaultBuildEngine.java:156)
full-log.txt:L2695:     	at com.pmease.quickbuild.DefaultBuildEngine$2.run(DefaultBuildEngine.java:1333)
full-log.txt:L2696:     	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
full-log.txt:L2697:     	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
full-log.txt:L2698:     	at java.lang.Thread.run(Thread.java:750)
```

- **A，总时长超限：总控24小时时限，基本确认。** 依据P:L1、L1561、L2321、L2689–2692及用户补充的起始日期；未读取QB后台超时配置，也没有据此认定worker被8h/9h命令杀死。
- **B，无输出判卡住：未获证实。** 全文件没有idle/no-output阈值或相应停止原因；这份父日志没有包输出，父日志长间隔不能证明worker没输出。
- **C，编译进程真卡死：未获证实。** P:L2324–2326及L2343附近是QB等待子构建状态的Java线程，不是clang/lld的进程栈；没有编译PID、CPU、I/O或锁状态。
- **D，其他原因：无法排除子构建内部其他失败。** P:L2551只报告子构建FAILED，不说明包、架构或原因；不能把该行直接归因为BOLT。

取消传播原文：

```text
full-log.txt:L2348: 07:17:48,441 ERROR - Step 'master>TRIGGER>Parallel_Build' is failed.
full-log.txt:L2349:     java.lang.RuntimeException: java.lang.InterruptedException: Composite step 'Parallel_Build' is cancelled as a child step is cancelled.
full-log.txt:L2673: 07:17:56,800 ERROR - Step 'master' is failed.
full-log.txt:L2674:     java.lang.RuntimeException: java.lang.InterruptedException: Composite step 'master' is cancelled as a child step is cancelled.
```

### 唯一的时间回退：只能给出条件计算

P:L2320 `07:20:35,741` 后紧接P:L2321 `07:17:46,444`，直接钟面差为 **-169.297秒**。如果假设日志按时间顺序、只跨一天，则该父任务等待间隔为 `86400-169.297=86230.703秒`（23:57:10.703），首行到最后时戳为 **86411.012秒**（24:00:11.012）。

**以上均为推测**：每行没有日期，不能排除日志拼接或时钟变化；也未读到“24小时”配置。这不是LLVM编译耗时，不能拿它与506dc25的单个x86_64包10712秒直接相减。最大正向间隔统计保留原始钟面，不偷偷给时间回退加一天。

## 3. 时间线与506dc25对照

搜索了用户输入目录、W/docs中的本地QB日志集合、约定的W/temp/qb-506dc25位置，以及B仓库的QB相关日志文件。输入目录只有full-log.txt，约定基线目录不存在；B的506dc25安装演练日志是本地演练，不能当QB基线。未在这些范围找到506dc25原始QB包日志，以下严格采用用户给出的摘要，**不声称全机绝无该文件**。

**基线来自摘要，不是原始日志。** 摘要没有原始行号，不能为它编造行号。摘要推算BOLT区间1065秒、compare-root至包结束4309秒；后一段还可能包括剩余安装/转换，不能当find-debuginfo的精确耗时。

|阶段/锚点|本次 `[NNNNs]`|506dc25摘要|本次减基线|
|---|---|---|---|
|%prep开始|未知|未给|无法计算|
|%build开始|未知|未给|无法计算|
|Ninja [1000/N]|未知，N也未知|未给|无法计算|
|Ninja约一半[N/2/N]|未知|未给|无法计算|
|Ninja最后[x/N]|未知|未给|无法计算|
|普通构建**持续时间**|未知|约5100秒；不是起点|无法计算|
|%install开始|未知|未给；不等同BOLT开始|无法计算|
|BOLT阶段开始|未知|约5338秒|无法计算|
|disk-report begin|无对应运行行|摘要未给该标记|无法计算|
|tool-built|无对应运行行|未给|无法计算|
|pipeline及PASS|无对应运行行|未给|无法计算|
|各bolt_step/bolt_checked起止|无对应运行行|未给|无法计算|
|compare-root|未知|约6403秒|无法计算|
|BOLT开始→compare-root|未知|约1065秒（17分45秒，摘要约18分钟）|无法计算|
|post / disk-report post|无对应运行行|未给|无法计算|
|find-debuginfo开始|未知|未给|无法计算|
|打包开始|未知|未给|无法计算|
|compare-root→结束|未知|约4309秒（71分49秒）|无法计算|
|x86_64包最后输出/全程|不存在可识别的包日志边界|10712秒（2:58:32）|无法计算|
|输入文件最后输出|P:L2698，无时戳Java堆栈；最近时戳P:L2689 07:17:57,458|不是同一日志层级|不做混算|

本次能列出的只有**总控墙钟锚点**：

|原始时戳|行号|事件与原文|
|---|---:|---|
|07:17:46,446|1|Executing pre-execute action...|
|07:18:03,125|2246|HEAD is now at 9e5675f57d12 packaging: optimize x86_64 clang with BOLT|
|07:20:24,453|2257–2258|package files have been exported to: .../llvm-22.1.8-1|
|07:20:35,613|2314|Child step names of step 'Parallel_Build': [Trigger_Each_Build]|
|07:20:35,741|2320|use_ngbs from project_env: yes|
|07:17:46,445|2322|Trigger_Each_Build... is failed.（日期不明/钟面回退后）|
|无时戳；报表正文始于P:L2476 07:17:54,995|2549–2551|子构建1202084被写入报表，FAILED；这些HTML行本身无时戳|
|07:17:57,458|2689|Build is timed out.|

这里的gbs export只是源码导出，不是%prep或普通LLVM构建。完整[timeline.tsv](../../tools/bolt/results/qb-timeout-20261021/timeline.tsv)将value_type、墙钟、包elapsed、摘要来源和缺失原因分列；缺失值写NA，不填0。

## 4. 最后200行：能定位到总控等待，定位不到编译工序

最后200行为 **P:L2499–2698**，主要是子构建报表、Snapshot步骤/清理，以及总控取消后的堆栈。能确认的是报表已输出1202084及FAILED（P:L2549–2551），该步骤随后进入post-execute hook（P:L2564）；只能称“报告输出/进入收尾”，不能把它当作LLVM某一步成功。

```text
full-log.txt:L2549:       <td>standard-armv7l:aarch64:x86_64</td>
full-log.txt:L2550:       <td><a href="https://quickbuild.tizen.org/build/1202084">https://quickbuild.tizen.org/build/1202084</a></td>
full-log.txt:L2551:       <td>FAILED</td>
full-log.txt:L2563: 07:17:54,995 WARN  - target_snapshot_url : http://download.tizen.org/RBS/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261019.071746
full-log.txt:L2564: 07:17:54,996 INFO  - Executing post-execute action...
full-log.txt:L2565: 07:17:55,113 INFO  - Checking step execute condition...
full-log.txt:L2566: 07:17:55,113 INFO  - Step execute condition satisfied, executing...
full-log.txt:L2567: 07:17:55,249 INFO  - Executing pre-execute action...
full-log.txt:L2568: 07:17:55,249 INFO  - cmd:cd /home/tizenbuild/build_meta;git pull
full-log.txt:L2569: 07:17:55,371 INFO  - cmd result: Already up to date.
full-log.txt:L2571: 07:17:55,371 INFO  - Running step...
```

超时前最后可辨认的等待点是Parallel_Build/Trigger_Each_Build获取子构建状态（P:L2313–2327），不是一个已显示的编译命令。取消前能明确确认的LLVM相关完成操作，是**源码导出**（P:L2257–2258），不代表普通构建完成。到P:L2689时总控已经报告超时；没有依据说此刻worker还在哪条命令内。

文件末行P:L2698是堆栈尾。EOF以后没有时间戳，不能凭“文件到此结束”计算一段长静默。唯一可能的长等待是前述P:L2320→2321跨日假设，属于父任务等待子任务；**不能证明其间正好运行bolt_step/bolt_checked**。这两个名字在整个输入出现0次；没有标记也不证明子构建没有进入BOLT，因为这份父日志本来就没有包输出。9e5675f的BOLT输出缓冲是否影响了子任务，需要1202084的实际LLVM日志才能判定。

## 5. 静默/输出间隔前10

用户要求的 `[NNNNs]` 包时间差无法统计：全P:L1–2698该前缀为0。下面是额外提供的**总控HH:MM:SS,mmm**统计，不能冒充编译静默。主表要求两行在原文件中物理相邻且都有时间戳，排除日期不明的负差；只有这种配对能说明两条输出间的可见正向钟面差。

|排名|起止行|秒|阶段|起始原文|结束原文|
|---:|---|---:|---|---|---|
|1|L2255→L2256|52.322|源码同步/导出/输入校验|`07:19:29,341 INFO  - info: llvm-22.1.8.tar.gz does not exist, creating from 'upstream/22.1.8'`|`07:20:21,663 INFO  - info: Generating patches from git (upstream/22.1.8..HEAD)`|
|2|L2249→L2250|52.262|源码同步/导出/输入校验|`07:18:18,423 INFO  - info: llvm-22.1.8.tar.gz does not exist, creating from 'upstream/22.1.8'`|`07:19:10,685 INFO  - info: Generating patches from git (upstream/22.1.8..HEAD)`|
|3|L2247→L2248|14.501|源码同步/导出/输入校验|`07:18:03,787 INFO  - info: tracking branch: origin/upstream -> upstream`|`07:18:18,288 INFO  - info: Generating patches from git (upstream/22.1.8..HEAD)`|
|4|L2253→L2254|13.580|源码同步/导出/输入校验|`07:19:15,624 INFO  - info: tracking branch: origin/upstream -> upstream`|`07:19:29,204 INFO  - info: Generating patches from git (upstream/22.1.8..HEAD)`|
|5|L2279→L2280|8.640|源码同步/导出/输入校验|`07:20:26,615 INFO  - Total 313 (delta 100), reused 193 (delta 100)`|`07:20:35,255 INFO  - ---[chk_input_variable JOB STARTED]----------------------------------------`|
|6|L2250→L2251|2.813|源码同步/导出/输入校验|`07:19:10,685 INFO  - info: Generating patches from git (upstream/22.1.8..HEAD)`|`07:19:13,498 INFO  - info: package files have been exported to:`|
|7|L2256→L2257|2.790|源码同步/导出/输入校验|`07:20:21,663 INFO  - info: Generating patches from git (upstream/22.1.8..HEAD)`|`07:20:24,453 INFO  - info: package files have been exported to:`|
|8|L2240→L2241|2.668|源码同步/导出/输入校验|`07:17:58,390 INFO  - export_src_git_commit_id_path : /data/gbs/export_src/review.tizen.org/platform/upstream/util-linux/87a36ce91d6ddff60e2be7470d95765a1dd29e2d, export_src_path: util-linux-2.41.2-0, spec_file_exists: True`|`07:18:01,058 INFO  - export_src_git_commit_id_path : /data/gbs/export_src/review.tizen.org/product/upstream/findutils/2b41eecd82b95d7aa07abb308b66dbacd056cdda, export_src_path: findutils-4.3.8-0, spec_file_exists: TrueTotal 30 (delta 19), reused 30 (delta 19)`|
|9|L2252→L2253|2.126|源码同步/导出/输入校验|`07:19:13,498 INFO  -      /home/tizenbuild/ci_tizen_workspace/qbsource26_8811/f72dwyp2/libcxx-runtimes-22.1.8-1`|`07:19:15,624 INFO  - info: tracking branch: origin/upstream -> upstream`|
|10|L2258→L2259|1.544|源码同步/导出/输入校验|`07:20:24,453 INFO  -      /home/tizenbuild/ci_tizen_workspace/qbsource26_8811/7nfqf2zk/llvm-22.1.8-1`|`07:20:25,997 INFO  - `|

最大可直接确认正差52.322秒发生在LLVM源码tar导出，不是BOLT构建。P:L2320→2321负差单列，不从主表中消失，也不强行认作24小时。如果采用“一天”假设，它会以86230.703秒排第一，后接上表前9项；该条件排行仍不是worker无输出排行。

[silent_gaps.txt](../../tools/bolt/results/qb-timeout-20261021/silent_gaps.txt)另外提供“相邻带时间戳行”的前10，注明其中夹着多少无时间戳行，避免把未计时输出也算成静默。506dc25原始日志未找到，不能生成它的前10。

## 6. 普通构建是否变慢

**无法确认。** 本次没有包级%build/%install边界，也没有Ninja [x/N]，因此连“超时发生在BOLT之前”这一前提也无法确认。配置中的threads30/32、-j8/-j20、WORKER_N28不能代替实际Ninja并行度；没有nproc、任务总数N、CPU配额/负载、I/O、cache状态或相同进度采样点。

无法计算两次的任务/秒、相同x任务的耗时差，也无法区分机器负载、并行度和任务数变化。把父任务可能24小时的等待直接与506包10712秒对比，会混合工程/包两个层级。上述因素可作为**待核实推测**，不是本报告认定的原因。

## 7. 磁盘及缺失标记的完整扫描

全2698行、原始SHA固定的输入扫描结果：

|匹配串/模式|命中行数|可抄原文|
|---|---:|---|
|`[NNNNs] elapsed prefix`|0|无对应行；不伪造不存在的行号|
|`Ninja [x/N] progress`|0|无对应行；不伪造不存在的行号|
|`Executing(%prep)`|0|无对应行；不伪造不存在的行号|
|`Executing(%build)`|0|无对应行；不伪造不存在的行号|
|`Executing(%install)`|0|无对应行；不伪造不存在的行号|
|`BOLT_DISK_REPORT`|0|无对应行；不伪造不存在的行号|
|`BOLT_DISK_DIAGNOSIS`|0|无对应行；不伪造不存在的行号|
|`bolt_step`|0|无对应行；不伪造不存在的行号|
|`bolt_checked`|0|无对应行；不伪造不存在的行号|
|`BOLT_PIPELINE_PASS`|0|无对应行；不伪造不存在的行号|
|`BOLT_COMPARE_ROOT_PASS`|0|无对应行；不伪造不存在的行号|
|`BOLT_POST_GATE_PASS`|0|无对应行；不伪造不存在的行号|
|`find-debuginfo`|0|无对应行；不伪造不存在的行号|
|`RPM Processing files`|0|无对应行；不伪造不存在的行号|
|`RPM Wrote`|0|无对应行；不伪造不存在的行号|
|`No space left on device`|0|无对应行；不伪造不存在的行号|
|`Disk quota exceeded`|0|无对应行；不伪造不存在的行号|
|`nproc`|0|无对应行；不伪造不存在的行号|

因此**本输入没有任何BOLT_DISK_REPORT或BOLT_DISK_DIAGNOSIS行可原样抄录**；No space left on device与Disk quota exceeded也均为0。不能由此推断worker磁盘充足、没有BOLT或没有ENOSPC。全文检索范围/正则和计数见excerpts.txt，完整输入随gzip保留。不存在的行没有可引用的原文，用全文件扫描作负证据；摘要数据也不编造原始行号。

可复核的读取命令（只读，不执行日志中的命令）：

```sh
wc -lc docs/quickbuild_logs/full-log.txt
rg -n '^\s*\[\s*[0-9]+s\]|Executing\(%|\[[0-9]+/[0-9]+\]' docs/quickbuild_logs/full-log.txt
rg -n 'BOLT_DISK_REPORT|BOLT_DISK_DIAGNOSIS|bolt_step|bolt_checked' docs/quickbuild_logs/full-log.txt
rg -ni 'No space left on device|Disk quota exceeded|nproc' docs/quickbuild_logs/full-log.txt
```

后三条对指定运行模式没有匹配，rg的退出1表示没有匹配，不是构建失败。日志中只有提交标题的BOLT字样或软件清单里的ninja名字，不能把它们算作BOLT/Ninja运行标记。

## 8. armv7l / aarch64与其他本地日志

- **armv7l：结果未知。** 输入目录没有本轮架构包日志；P:L2549–2551只有三架构组合子构建FAILED，无法分配到armv7l或某阶段。
- **aarch64：结果未知。** 同上，不能判通过、失败或超时于哪一步。

本地另存的`W/docs/qb_1203397_lld/raw/llvm_<arch>.log.xz`不能补入这次分析。它的来源与提交原文为：

```text
/home/linhao/Toolchain/development/llvm-optimize/docs/qb_1203397_lld/raw/parent_log_provenance.json:L2:   "url": "https://quickbuild.tizen.org/build/1203397/log",
/home/linhao/Toolchain/development/llvm-optimize/docs/qb_1203397_lld/raw/source_manifest.xml:L108:   <project name="platform/upstream/llvm" path="platform/upstream/llvm" revision="120afe9cd158e5de9fe26d4282785c5d59c657bc"/>
```

这是QB1203397、LLVM120afe9c，和本次日志指向的1202084/9e5675f不同。这里只用两条身份元数据排除串轮，没有采用别轮的worker、并行度、耗时或成功状态。这两条原文也保存在本轮excerpts.txt。

## 9. 建议方向（本轮均不实现）

|建议|理由|风险/限制|
|---|---|---|
|下一轮先补齐子构建1202084的实际GBS调度日志及llvm.spec三架构包日志，并保留原日期/时区和行首秒数|P:L2550已给出明确子构建；当前只有总控，不能定位到包/架构/工序|需要用户导出或另行授权只读采集；不要把不同QB/提交的日志混入。本轮不登录QB、不触发重建|
|核对QB总时限、触发器等待上限和最终生效的8h/9h命令，区分工程、子构建、单包口径|P:L389/1511与L2689只有配置文本及QB超时，没有实际阈值链|盲目增加时限可能掩盖真卡死和占用worker，不能只凭跨日推测改成更长|
|**推测/有条件**：若子日志证实停在BOLT专用包装且因无输出超时，再考虑只给BOLT步骤实时转发或独立心跳|9e缓冲是用户指出的候选因素，当前没有执行证据；需要先看到包级起止与QB idle判定|不能再包装普通构建/平台post；必须保留退出码、进程组回收和严格tool-plan/构建日志格式，心跳不能污染认证输入|
|**推测/有条件**：若补日志证明普通构建变慢，再按同任务数比较worker负载、实际-j、nproc/CPU配额与缓存|当前没有Ninja采样点，无法证明速率下降|盲目增大并行度可能OOM或I/O争用；改变编译参数会破坏比较条件|

没有证据支持本轮直接改spec、恢复磁盘门槛、改BOLT参数或再跑一次构建。本轮只交付分析和证据，等待下一步指令。

## 10. 归档与一致性

原始输入SHA256为`537754ed05cedc0280b57adf4af01f986e50b484a51646e3d5c64baeab6d5851`。完整gzip为`full-log.txt.gz`，压缩后 **52904 B**，小于50MB，已按要求随证据交付；解压后逐字节等于原始输入，不是截断或替代日志。gzip SHA256：`8b873d0f835e4a7c8ef38d0f2ec643d0a8563a6edaaa052d61c4dc79abc374d0`。

- excerpts.txt：阶段/配置/停止锚点、全文件扫描计数、排除别轮的身份原文、最后300行（P:L2399–2698）。
- timeline.tsv：包级秒数缺失写NA，摘要与推算分开；总控墙钟另列，不混算。
- silent_gaps.txt：相邻物理行/相邻计时行两套前10，回退和跨日假设单列。
- 完整源码、spec和受保护构建树均未修改；没有cmake/ninja/重建/提权/QB访问或Gerrit推送。


## 第11节：子构建 1202084

总控的24小时时限已基本确认，但子构建页面记录了 **47小时56分1秒**，两者不是同一个结束事件。
armv7l、aarch64 的 LLVM 都有明确的成功记录；最后可见的工程状态是 armv7l 已发布，aarch64 与 x86_64 尚未结束，不能把24小时延迟归给唯一架构或某条编译命令。
**已证实子构建最终发生磁盘写入错误**：异常栈落在 QB 的 `BuildLogger.close`，尚不能证明它就是总控达到24小时的最初原因。
x86_64 的 LLVM 没有成功记录，且被重新派发；本轮未取得它的包日志，因此不能确认9e5675f的BOLT输出缓冲是否参与，更不能据此认定要修改BOLT。
性能页没有给出分包数据、页面没有包日志下载入口，已按用户约定停止继续探查，以下只分析已实际取得的页面和子构建总日志，不猜测日志是否被清理。

### 11.1 采集身份、范围与停止位置

本轮采用有界面的Playwright Chromium，用户在窗口中手动登录；登录状态只在本机临时目录，未导出cookies、凭据、认证头或登录表单到仓库。登录后仅访问构建详情/性能/日志/步骤状态页面及页面中实际出现的Save下载链接，没有点击或请求Rebuild、Stop、Cancel、Promote等动作，也没有重跑构建。采集后已关闭浏览器。

证据目录：[child](../../tools/bolt/results/qb-timeout-20261021/child/)。下面记子总日志为 **C**，即解压 `1202084-full-log.txt.gz` 后的原始行号；P仍是第1–10节的总控原日志。页面文本的行号直接以对应`.txt`为准。所有文件的来源URL、字节数、SHA256及转换说明在 [provenance.json](../../tools/bolt/results/qb-timeout-20261021/child/provenance.json)。

|采集项|实际结果|
|---|---|
|概览|[HTML](../../tools/bolt/results/qb-timeout-20261021/child/overview.html)、[文本](../../tools/bolt/results/qb-timeout-20261021/child/overview.txt)、[全页截图](../../tools/bolt/results/qb-timeout-20261021/child/overview.png)已保存；含磁盘错误告警及节点|
|`/build/1202084/build_profiling`|HTTP200，但返回概览内容，没有每包开始/结束/耗时表；[文本](../../tools/bolt/results/qb-timeout-20261021/child/build-profiling.txt)与overview.txt逐字节相同，HTML/截图均保留。不把HTTP200冒充性能报告可用|
|Build Log页面|[HTML](../../tools/bolt/results/qb-timeout-20261021/child/build-log-page.html)、文本、截图已保存；初次渲染正文未显示日志行，但有Save链接，不能据此声称日志被清理|
|Save原始下载|HTTP200，**1,851,509 B / 20,939行**，SHA256 `90fc3c123f6ab795a5b9bb714ce18b9354d4cba5ad2678ab15b4c3f53e37de19`；无损gzip为 **194,398 B**，小于50MB，已提交|
|Step Status|[文本](../../tools/bolt/results/qb-timeout-20261021/child/step-status.txt)、HTML、截图已保存，列出所有可见步骤|
|三架构LLVM包日志、架构独立构建日志|**NOT ACQUIRED**：以上页面未显示包/架构日志下载入口。未猜测隐藏API或文件路径，没有用其他构建的日志代替；无法判断是否未发布、已清理或另存他处|
|worker资源信息|概览显示No space left错误，已截图；可见页面没有剩余容量、设备号、历史资源曲线。未继续进入worker管理页|

子构建的请求源码映射在C:L136、L278、L417均含 `'platform/upstream/llvm': '9e5675f57d122549997caffa39b655dfefc46fee'`（行内原文片段）；这证明请求的源提交，不能冒充缺失包日志中的checkout认证。

概览原文：

```text
overview.txt:L26: Id	Status	Begin Date	Duration	Triggered By	#Dependents 	#Dependencies 
overview.txt:L27: 1202084	Failed	2026-10-19 07:21:52	1 day 23 hours 56 minutes 1 second	lhmax2025 (Lin)	0 builds	0 builds
overview.txt:L29: Error executing step execution job.
overview.txt:L30: caused by: java.io.IOException: No space left on device
overview.txt:L31: caused by: No space left on device
overview.txt:L34: master @ ip-192-168-56-80:8811 
```

开始时间为页面直接显示的 **2026-10-19 07:21:52**；页面没有单独End Date列，按开始时间加Duration推算结束为 **2026-10-21 07:17:53**，不是直接读取的结束日期。该钟面与C:L20910 `07:17:53,525 ERROR - Build is failed.`吻合。日志/页面未声明时区，不擅自换算。这个47小时56分是QB状态持续时间，不是有效CPU编译时间。

`step-status.txt:L26–61`显示：master FAILED；TRIGGER、BUILD_ABS SKIPPED；BUILD、Build、Build_GBS、后续Update_Trigger_Description、Publish、SNAPSHOT、IMAGE均CANCELLED；Enable_SWAP、前置Update_Trigger_Description、Sync及其两个子步骤SUCCESSFUL。**CANCELLED不证明这些步骤从未执行**，也不自动等同某架构LLVM失败；包级结果另看调度日志。

### 11.2 三目标是否并行、各自完成到哪里

三目标调度器同一钟面启动（C:L526、L528、L530，均07:28:52,531）；LLVM在07:30附近分别收到派发。08:00和后续08:10/20/30/40的调度快照均同时把三目标LLVM列为building，支持**调度层面并行，非逐架构串行**。这些不是CPU执行轨迹，不能把派发视为实际编译起点。

|目标|LLVM首次派发事件时间|LLVM结果及事件时间|工程最后可见状态/阶段|
|---|---|---|---|
|armv7l|2026-10-19 07:30:16，C:L1247|**BUILD_SUCCESS**，10-19 08:43:11，C:L9045；派发到成功事件相差4375秒|首次观察published在15:39:03,683（C:L13170）；18:44:43,317仍published（C:L20438）。该工程此时已结束构建/发布，非拖满24小时的未完成LLVM|
|aarch64|2026-10-19 07:30:16，C:L1245|**BUILD_SUCCESS**，10-19 08:58:20，C:L9102；派发到成功事件相差5284秒|工程16:14:36仍building且scheduled1（C:L13374）；最后DEBUG快照18:44:43,317仍building（C:L20439）。16:05:57派发的是gcc-riscv64（C:L13349），不是LLVM；最终工程独立结果未知|
|x86_64|2026-10-19 07:30:08，C:L1178|**未见BUILD_SUCCESS/FAIL llvm standard x86_64**；共30条LLVM派发，最后一次为16:05:59（C:L13351）；不能当30次完整编译|工程16:14:36为scheduled1、blocked256（C:L13375），最后DEBUG快照18:44:43,318为building（C:L20440）。最后可定位到LLVM调度/未完成，无法定位普通Ninja、BOLT或post|

4375/5284秒包含派发后的准备、构建及打包等，**不是`%build`纯耗时**。子总日志没有三架构最终独立状态页；子构建整体Failed、Build_GBS在步骤页CANCELLED，也不能用来覆盖已明确成功的ARM LLVM结果。

并行及结果原文：

```text
C:L526: 07:28:52,531 INFO  - Starting bs_sched armv7l
C:L528: 07:28:52,531 INFO  - Starting bs_sched aarch64
C:L530: 07:28:52,531 INFO  - Starting bs_sched x86_64
C:L1245: 07:30:38,879 INFO  - 2026-10-19 07:30:16: [57]    assignjob aarch64/Tizen-Base-Toolchain::standard::llvm-6815d113cfaa7555f744da30333afc87 -> x86_64:67ef2284678f:13
C:L1247: 07:30:38,879 INFO  - 2026-10-19 07:30:16: [57]    assignjob armv7l/Tizen-Base-Toolchain::standard::llvm-6815d113cfaa7555f744da30333afc87 -> x86_64:67ef2284678f:16
C:L1553: 08:00:20,362 INFO  - 	 llvm building
C:L2058: 08:00:20,367 INFO  - 	 llvm building
C:L2565: 08:00:20,373 INFO  - 	 llvm building
C:L9045: 08:43:13,759 INFO  - Mon Oct 19 08:43:11 2026 BUILD_SUCCESS llvm standard armv7l
C:L9102: 08:58:29,278 INFO  - Mon Oct 19 08:58:20 2026 BUILD_SUCCESS llvm standard aarch64
C:L13170: 15:39:03,683 INFO  - standard armv7l   published  | succeeded     252  excluded        6
```

后期待调度/再次派发证据：

```text
C:L13349: 16:06:03,453 INFO  - 2026-10-19 16:05:57: [57]    assignjob aarch64/Tizen-Base-Toolchain::standard::gcc-riscv64-2088b0e4e1c7f71cd06f94d8f432df7b -> x86_64:67ef2284678f:12
C:L13351: 16:06:03,462 INFO  - 2026-10-19 16:05:59: [57]    assignjob x86_64/Tizen-Base-Toolchain::standard::llvm-6815d113cfaa7555f744da30333afc87 -> x86_64:67ef2284678f:21
C:L13373: 16:14:36,139 INFO  - standard armv7l   published  | succeeded     252  excluded        6
C:L13374: 16:14:36,139 INFO  - standard aarch64  building   | succeeded     251  scheduled       1  excluded        6
C:L13375: 16:14:36,139 INFO  - standard x86_64   building   | scheduled       1  excluded        1  blocked       256
C:L20438: 18:44:43,317 INFO  - Tizen-Base-Toolchain standard armv7l published published
C:L20439: 18:44:43,317 INFO  - Tizen-Base-Toolchain standard aarch64 building building
C:L20440: 18:44:43,318 INFO  - Tizen-Base-Toolchain standard x86_64 building building
```

全部实际派发及BUILD_SUCCESS/FAIL/UNCHANGED事件共1057条，保留在 [package-scheduler-events.tsv](../../tools/bolt/results/qb-timeout-20261021/child/package-scheduler-events.tsv)，包括每个被记录的包、目标、原行号、原文和事件时戳。它是调度事件表；没有从不完整派发/重试记录伪造每包的真实编译耗时或完整profiling数据。

### 11.3 LLVM阶段、最后200行与输出缓冲

三份LLVM包日志均未取得，子总日志中没有`[NNNNs]`前缀、Ninja `[x/N]`、Executing(%prep/%build/%install)、find-debuginfo、RPM打包或BOLT运行标记。各目标的`%prep`、`%build`、Ninja采样点、`%install`、最后一条编译输出，以及x86的disk-report/bolt_step起止/pipeline/compare-root/post，均记 **NA，无法读取**；不能把调度器时戳填到包elapsed列中。[llvm-timeline.tsv](../../tools/bolt/results/qb-timeout-20261021/child/llvm-timeline.tsv)逐项列出缺失，另列真实LLVM调度事件。

最后200行是 **C:L20740–20939**，见 [excerpts.txt](../../tools/bolt/results/qb-timeout-20261021/child/excerpts.txt)：前段是blocked包清单，最后30行是QB异常栈。最后一条可见的普通日志是C:L20909的`tinyxml2 blocked`；**这不是某个构建步骤完成**。最后明确成功的包事件在C:L13338：gcc-armv7hl/aarch64成功；LLVM自身最后成功事件为aarch64的C:L9102。最后可见调度快照中的未完成工程是aarch64/x86_64；最终QB状态为失败/步骤取消，没有证据说明EOF时还在某条编译命令里。

```text
C:L13338: 16:04:02,365 INFO  - Mon Oct 19 16:04:00 2026 BUILD_SUCCESS gcc-armv7hl standard aarch64
C:L20909: 18:44:43,339 INFO  - 	 tinyxml2 blocked
C:L20910: 07:17:53,525 ERROR - Build is failed.
C:L20911:     java.lang.RuntimeException: Error executing step execution job.
```

C:L20909 `18:44:43,339`到C:L20910 `07:17:53,525`有钟面回退。按概览起始日/47小时56分及日志内10-19的日期，给前者配10-19、后者配10-21，**推算**可见输出间隔为131590.186秒（36小时33分10.186秒）。其中跨过父任务10-20的24小时终止；不能误算成只等了12小时33分，也不能把整个间隔认作LLVM命令耗时。没有原始QB日志写入时间/完整worker日志来验证中间是否丢失、缓冲或停止了输出。

**9e5675f的BOLT缓冲是否参与：无法确认。** 本轮没有读到x86的bolt_step/bolt_checked起止或BOLT_DISK_REPORT。已取得的父日志里没有这些子调度输出，而子调度日志此前持续输出polling/status；其最后的QB日志写盘异常也可能影响日志完整性（**推测**）。这些均不能证明“长静默时正在跑一个BOLT包装命令”，更不能把QB的BuildLogger缓冲与spec中BOLT步骤输出缓冲当成一件事。

### 11.4 输出间隔前10

以下只是**子总调度日志**物理相邻且均有HH时戳的正向钟面差，未把日期回退自动加一天；每对原文及相邻计时行的另一套统计在 [silent-gaps.txt](../../tools/bolt/results/qb-timeout-20261021/child/silent-gaps.txt)。三架构包日志各自的`[NNNNs]`前10仍不可得。

|排名|起止C行|秒|阶段/原文摘要|
|---:|---|---:|---|
|1|494→495|209.135|NGBS参考根归档准备：`Archive_file From: ...archive_ngbs_root.tar.zst_027` → `To: ...archive_ngbs_root.tar.zst_027`|
|2|432→433|146.428|NGBS元数据/参考根准备：`create_meta_for_ngbs...` → snapshot URL|
|3|9171→9172|46.172|`standard x86_64 building ...` → `polling...`|
|4|12884→12885|42.800|`polling...` → `polling...`|
|5|12909→12910|34.993|`standard x86_64 building ...` → `polling...`|
|6|12916→12917|32.755|`polling...` → `polling...`|
|7|9253→9254|31.422|`polling...` → `polling...`|
|8|12371→12372|31.315|`polling...` → `polling...`|
|9|12535→12536|31.140|`standard x86_64 building ...` → `polling...`|
|10|12564→12565|31.085|`polling...` → `polling...`|

如按上节日期重建，C:L20909→20910推算的131590.186秒应排第一，后接上表前9。它属于总调度/日志层级，不是已确认的编译静默；不能据此匹配到某个bolt_step。506dc25原始包日志仍未找到，不能列出其前10作假精确对比。

### 11.5 8h/9h与杀进程证据

对子总日志C全部20939行搜索：`timeout 8h`、`timeout 9h`、`Terminated`、`Killed`均无匹配；明确的exit/return/status 124也无匹配。裸数字124在时戳/包计数中出现，不作退出码证据。三份包日志未取得，不能将“C中没有”扩大成“实际命令从未被timeout杀死”。

与父日志只展示GBS配置不同，本次实际启动原文是 **NGBS**：

```text
C:L523: 07:28:46,207 INFO  - [07:28:46.207152] docker_exec_cmd: docker exec gbsbuild_ip-192-168-56-80_8811 bash -lc  "export NGBS_ROOT=/root/gbsbuild-ROOT/NGBS-ROOT;export JOBS_N=12;export WORKER_N=28;/root/ngbs/ngbs server start;python3 /root/gbsbuild-ROOT/6pmm91yf/exec_ngbs_build.py /root/ngbs /root/gbsbuild-ROOT/build_meta /root/gbsbuild-ROOT/gbs_exported"
```

此处为`JOBS_N=12`、`WORKER_N=28`；28个bs_worker启动见C:L551–578。这不是Ninja `-j12/-j28`的认证，也不是nproc。此命令里没有8h/9h的timeout包装，不能仅凭父日志的DEFAULT/USER_DEFINED_GBS_BUILD_CMD认定NGBS实际用了它们。子终态为`Build is failed`，直接异常是磁盘写入失败，不是已读到的shell超时124。

### 11.6 磁盘

#### 全文扫描与全部命中原文

[磁盘全文检索](../../tools/bolt/results/qb-timeout-20261021/child/disk-search.txt)不区分大小写，逐项覆盖用户要求的全部15个模式。**三架构LLVM包日志没有取得，其匹配数为NA，不是0。**

|模式|子总日志命中|三份LLVM包日志|
|---|---:|---|
|No space left|2|均NA|
|ENOSPC、Disk quota、EDQUOT|各0|均NA|
|write error、cpio: write、Unable to write|各0|均NA|
|Input/output error、failed to write、short write|各0|均NA|
|Bad exit status、Terminated、Killed|各0|均NA|
|BOLT_DISK_REPORT、BOLT_DISK_DIAGNOSIS|各0|均NA|

全部2处命中都属于 **未分架构的QB日志关闭步骤**，不是x86/BOLT包内报错；上下文原文：

```text
C:L20922:     Caused by: java.lang.RuntimeException: java.io.IOException: No space left on device
C:L20923:     	at com.pmease.quickbuild.log.BuildLogger.close(BuildLogger.java:67)
C:L20924:     	at com.pmease.quickbuild.BuildAwareJob.execute(BuildAwareJob.java:81)
C:L20925:     	at com.pmease.quickbuild.grid.GridJob.run(GridJob.java:131)
C:L20926:     	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
C:L20927:     	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
C:L20928:     	... 3 more
C:L20929:     Caused by: java.io.IOException: No space left on device
C:L20930:     	at java.io.FileOutputStream.writeBytes(Native Method)
C:L20931:     	at java.io.FileOutputStream.write(FileOutputStream.java:326)
C:L20932:     	at java.io.BufferedOutputStream.flushBuffer(BufferedOutputStream.java:82)
C:L20933:     	at java.io.BufferedOutputStream.write(BufferedOutputStream.java:126)
C:L20934:     	at java.io.ObjectOutputStream$BlockDataOutputStream.drain(ObjectOutputStream.java:1877)
C:L20935:     	at java.io.ObjectOutputStream$BlockDataOutputStream.writeByte(ObjectOutputStream.java:1915)
C:L20936:     	at java.io.ObjectOutputStream.writeFatalException(ObjectOutputStream.java:1576)
C:L20937:     	at java.io.ObjectOutputStream.writeObject(ObjectOutputStream.java:351)
C:L20938:     	at com.pmease.quickbuild.log.BuildLogger.close(BuildLogger.java:65)
C:L20939:     	... 7 more
```

概览的错误框也直接显示No space left（overview.txt:L29–36），[overview.png](../../tools/bolt/results/qb-timeout-20261021/child/overview.png)是该告警截图。没有free-byte、quota、inode或文件系统设备号数据；不能从ENOSPC字样区分数据块耗尽、inode等具体原因，也不能把报错时刻当磁盘最早耗尽的时刻。

#### 四次BOLT空间记录

|x86 BOLT阶段|剩余字节|BOLT实际占用字节|最后行号/缺失说明|
|---|---|---|---|
|begin|未知|未知|包日志未取得；C中无该标记|
|tool-built|未知|未知|同上|
|pipeline|未知|未知|同上|
|post|未知|未知|同上|

**无法计算变化趋势，也不存在一个可引用的“最后一次BOLT_DISK_REPORT行”。** C:L20909之后是上述推算长间隔和QB写日志失败；这不是某一次disk-report之后的已认证流水线区间。没有把缺失测量填0，也没有用当前机器空间代替构建当时空间。

#### 同机、同盘与时间重叠

概览节点为`ip-192-168-56-80:8811`（overview.txt:L34）；工作区、Docker卷映射及三架构派发原文：

```text
C:L42: 07:21:53,176 DEBUG - Command working directory: /home/tizenbuild/ci_tizen_workspace/ip-192-168-56-80_8811
C:L125: 07:21:58,979 INFO  - gbsbuild_workspace: /data/workspace/gbsbuild-ROOT/
C:L134: 07:21:58,979 INFO  - build_root: /data/workspace/gbsbuild-ROOT/NGBS-ROOT
C:L214: 07:22:05,412 INFO  - docker init cmd: docker stop gbsbuild_ip-192-168-56-80_8811;docker rm gbsbuild_ip-192-168-56-80_8811;docker run --privileged -e no_proxy=localhost,127.0.0.1 -t -d --cap-add ipc_lock -v /etc/localtime:/etc/localtime:ro  -w /root/gbsbuild-ROOT -v /data/workspace/gbsbuild-ROOT/:/root/gbsbuild-ROOT --name gbsbuild_ip-192-168-56-80_8811 tizen-docker-local.bart.sec.samsung.net/ngbs:20260727.0452
C:L1178: 07:30:08,011 INFO  - 2026-10-19 07:30:08: [57]    assignjob x86_64/Tizen-Base-Toolchain::standard::llvm-6815d113cfaa7555f744da30333afc87 -> x86_64:67ef2284678f:16
C:L1245: 07:30:38,879 INFO  - 2026-10-19 07:30:16: [57]    assignjob aarch64/Tizen-Base-Toolchain::standard::llvm-6815d113cfaa7555f744da30333afc87 -> x86_64:67ef2284678f:13
C:L1247: 07:30:38,879 INFO  - 2026-10-19 07:30:16: [57]    assignjob armv7l/Tizen-Base-Toolchain::standard::llvm-6815d113cfaa7555f744da30333afc87 -> x86_64:67ef2284678f:16
```

三个目标的派发均使用`x86_64:67ef2284678f:<slot>`这一执行节点标识；调度快照C:L1553/L2058/L2565在08:00同时列出LLVM building，至08:40仍有三目标building采样（C:L7753/L8258/L8765）。这是**同一NGBS池、共享所示根目录且目标状态重叠**的证据；不等于能逐秒证明CPU并行。

宿主`/data/workspace/gbsbuild-ROOT/`映射到容器`/root/gbsbuild-ROOT`；另有QB工作区`/home/tizenbuild/ci_tizen_workspace/...`。**没有mountinfo、设备号或日志文件落盘路径，无法证明这些路径和QB日志位于同一文件系统/同一块物理磁盘。** 各包自身BUILDROOT完整路径未读到。不能因为共用节点，就断言是BOLT的ThinLTO缓存挤满了QB日志盘。

#### 三档结论与适用范围

|档位|本轮适用结论|依据/不能扩大的范围|
|---|---|---|
|**已证实是磁盘**|子构建**最终失败**存在磁盘写入原因|C:L20922–20938的No space left、FileOutputStream和BuildLogger.close；概览一致。只落实到QB写日志，不落实到BOLT重链输出|
|**有迹象但未证实**|磁盘问题是否更早造成调度/日志停滞，继而让父任务达到24小时|存在最终写盘失败、后期未完成/待调度状态及长日志间隔；但失败写盘的可见终态晚于父超时，缺少当时空间、worker状态和包日志，因果链仍是**推测**|
|**没有磁盘证据**|现有可读日志中，没有BOLT四阶段空间趋势或LLVM包内ENOSPC证据|C中无BOLT_DISK_REPORT/DIAGNOSIS；三份包日志缺失。此档仅描述证据缺口，**不证明LLVM/BOLT没有磁盘问题**|

因此不能把用户的磁盘假设直接升级为“已证实BOLT用满磁盘拖到了24小时”，也不能忽略已经明确出现的QB写盘失败。

### 11.7 与506dc25的可比范围

**基线来自摘要，不是原始日志。** 506dc25的x86单包全程10712秒、普通构建约5100秒、BOLT约5338→6403秒（1065秒），其后约4309秒到结束，仍按第3节摘要口径使用。

本次没有x86 LLVM包起止或Ninja进度。C:L1178的07:30:08与C:L13351的16:05:59相差30951秒，**是两次派发之间的间隔**，可能包含重试、排队和失效派发，不能减去10712秒后声称“LLVM慢20239秒”，也不能拿47小时56分的整个多包子构建与单个包比较。ARM两个LLVM成功事件也不用于冒充x86 BOLT性能复核。本次普通构建、BOLT、后处理究竟分别慢多少，仍未取得可比数据。

### 11.8 只给方向的建议与交付状态

|建议|理由|风险/限制|
|---|---|---|
|先由维护人员保全已有NGBS worker/调度服务记录及三架构LLVM包日志，特别是x86的首次与16:05再次派发|C:L1178、L1245、L1247、L13351给出具体任务及节点；当前没有包入口，无法定位流水线|只读保全现有数据，不为取日志重跑；已删除的数据不能补造。后续采集需新的入口或用户指令|
|核对该worker在10-19至10-21的块空间/inode/quota、QB日志目录与/data挂载关系|QB写盘失败已证实，但盘号、最初耗尽时刻、占用来源均未知|不要未经保全就清理缓存/日志；不能用现在的df结果证明事发时容量，也不要恢复发布代码里的磁盘门槛|
|核对NGBS反复派发、scheduled1及父任务24小时终止后子任务仍显示未结束的处理|同一x86 LLVM有30条派发；概览记录47小时56分，父/子终态明显不同|派发并不等于完整构建，必须先查调度/worker失效原因；盲目改重试/取消逻辑可能误杀正常包。本轮不改QB状态|
|**有条件/推测**：取得包日志后，若证明BOLT包装导致无输出超时，再评估只对BOLT步骤实时转发/心跳|当前没有BOLT运行标记或idle超时证据，不能直接归因9e缓冲|保留退出码/进程组终止、tool-plan原文及普通构建/post原样执行；心跳不能掩盖真卡死或污染认证日志|

本轮**部分采集完成，在缺少包日志入口处停止**：已保存四个页面的HTML/文本/全页截图、子总原始日志gzip、完整磁盘检索、总日志间隔、调度事件与缺失阶段表。19个文件均小于50MB；没有因超50MB而省略已下载文件。没有修改代码、helper或spec，没有访问受保护构建树执行命令，没有Gerrit推送或QB状态变更。第1–10节除第2节结论外保留原文，新结论以本节证据和范围为准。
