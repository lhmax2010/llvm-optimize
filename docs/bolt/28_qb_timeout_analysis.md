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

**已证实：QB层报超时，并在等待子构建状态时被中断。暂归A（推测，最符合现有总控证据）；A的具体阈值和子构建根因无法确认。**

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

- **A，总时长超限：最可能的解释，仍标推测。** P:L2689–2692显示Build is timed out / TimeoutException / GridTaskFuture.get / DefaultBuildEngine.run；没有QB configured timeout的数值、起止日期或实际worker终止记录，不能进一步声称“已证实24h上限”。
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
