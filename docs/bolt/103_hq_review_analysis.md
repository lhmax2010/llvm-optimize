# 103号：HQ 361395评审意见只读分析

**结论：新增1条HQ总评（6个问题）及5条行内评论，共11个分析项。建议修改5项；6个问题先澄清，其中并行策略需裁决。当前PS4尚未解决这5项。** 361395仍为NEW/PS3 ecb2dec7，HQ给Code-Review +1，没有要求本任务发布任何回复。全部diff和英文回复仅为证据仓库草稿，未应用、未推LLVM远端、未写Gerrit。

|编号|类型|建议修改|影响范围|重新验证|
|---|---|---|---|---|
|H1|要求修改|是|Part 2 / helper|信号恢复/退出码/清理|
|H2|要求修改|是（实现方式需裁决）|Part 2 / helper|定向竞态、掩码与二次信号；方案需批准|
|H3|要求修改|是|Part 2 / helper + spec|显式清单、debug/release、展开和post|
|H4|要求修改|是|Part 3 + Part 4 / converter|ar正反例＋全量转换重放|
|H5|要求修改|是|Part 3 + Part 4 / converter|全部退出路径＋转换重放|
|Q1|问题/澄清|否|Part 2|合并验证再查post，无独立构建|
|Q2|问题/澄清|否（不建议按警告文本盲加门禁）|上游BOLT + Part 2门禁|现有行为解释，不据警告直接改门禁|
|Q3|问题/澄清（并行策略待裁决）|暂不纳入；可选第6项待裁决|spec的既有构建调度|决定改并行度后需资源预算与实测|
|Q4|问题/澄清（数据请求）|否；需补测数据|Part 1/2验证资料|明确accel/setup口径后补采|
|Q5|问题/澄清|否（现有证据未发现重复定义）|Part 1 / CMake|合并构建＋最小插件载入|
|Q6|问题/澄清（纠正回退范围）|否|Part 2开关 vs Part 1/3/4|解析开关；完整回退另指定tree|

## 1. 原文完整性与新旧区分

读取时间见[SSH命令与时间](../../tools/bolt/results/hq-review-361395/query-command.json)。按要求执行SSH query并保存[stdout原文](../../tools/bolt/results/hq-review-361395/query.stdout)及stderr。HQ作者Dongkyun Son (dkson95)，总评时间 **2026-11-16T03:22:07-08:00**。5条inline出现在currentPatchSet及patchSets[PS3]两处，已去重，不能算10条。前101号查询中没有这条HQ总评/这5条inline；原PS1–PS3说明、上传消息及用户自己的+1单独保留，不算新增HQ意见。

匿名REST GET `/gerrit/changes/361395/comments` 和 `/messages` 均404。只尝试已有HTTP凭据读取，未取得，不创建凭据/登录；没有保存凭据正文。SSH已取得全部返回的5条inline原文、作者、PS、文件、行号，但**inline时间、comment ID、线程in_reply_to、unresolved状态UNKNOWN**；不能从总评时间推定每条inline时间，不能把H1等报告编号冒充Gerrit线程ID。此处按任务规则不STOP。[规范化记录](../../tools/bolt/results/hq-review-361395/comments-normalized.json)、[REST可用性](../../tools/bolt/results/hq-review-361395/rest-availability.json)。若需回复时准确对应线程，请用户在Gerrit界面核对；本轮不发布。

每条inline引用的代码取自**所指PS3 ecb2dec7的git对象**，各保存前后10行；完整文件及补充上下文位于[context清单](../../tools/bolt/results/hq-review-361395/RAW_LINKS.md)，不拿当前PS4行号代替原PS3。diff候选则以PS4 `8ec86c3ecb0c03889674ba7490064ff82ba63033` / tree `8097a7986fd835abc415b8651d0405358c6c22f0` 为基底。

HQ总评开头原文：

> Code-Review +1 on PS3 (ecb2dec) from a build-time and packaging review.
>
> Inline comments cover the signal-handling and archive-parser items I consider major. Questions and concerns:

## 2. 逐条分析

### H1. helper 的 SIGCHLD 恢复

PS3 `packaging/clang-bolt-helper.py:240`；[前后10行原文](../../tools/bolt/results/hq-review-361395/context/clang-bolt-helper.py.L240.txt)。

> SIGCHLD is set to SIG_DFL here and never restored, so the handler change persists for the rest of the build. Please restore the previous handler in a finally block.

**中文要点**：call()将SIGCHLD改为默认后不恢复。

**类型 / 是否修改**：要求修改 / 是。

**判断依据**：PS3 helper L238–240确有重置，L296–297 finally仅清_ACTIVE_GROUP；cli仅恢复TERM/INT/HUP。应接受恢复要求。但“持续到剩余整个build”需限定：signal.signal只能改变当前Python进程，不能修改父RPM shell；当前CLI退出后不存在跨shell持续影响。对同进程后续调用和库式使用仍是缺口。

**最小方案**：H1.diff：在try前保存旧SIGCHLD，在现有finally中于进程组清理/回收后恢复。必须覆盖成功、命令失败、超时、取消；不应在仍需waitpid时提前恢复SIG_IGN。 [独立diff草案](../../tools/bolt/results/hq-review-361395/drafts/H1.diff)。该修改会改变tree；未应用、未测试。

**与PS4关系**：PS4没有修复；与F1日志分类不重叠。

**验证要求**：新增default/ignored/custom处理器的成功与失败恢复、waitid/waitpid不丢退出码、子孙清理；合并下一轮QB及本地T/D验证。真实转换重放不是本条单独的必要证明，但与H4/H5及Part4一起运行。

**英文回复草稿（未发布）**：[原样文本](../../tools/bolt/results/hq-review-361395/replies/H1.txt)

```text
Agreed; the previous SIGCHLD disposition should be restored after child cleanup. This will be addressed in the next patch set with a finally block covering success and failure paths. The change currently persists within the helper process; it does not change the parent RPM shell's signal disposition.
```

### H2. Popen 至进程组登记的信号窗口

PS3 `packaging/clang-bolt-helper.py:250`；[前后10行原文](../../tools/bolt/results/hq-review-361395/context/clang-bolt-helper.py.L250.txt)。

> Popen with start_new_session=True is followed by _ACTIVE_GROUP assignment. A SIGTERM/SIGINT arriving in that window can leave the new process group uncleaned (the comment at 246-247 acknowledges this). Please block signals around Popen and the assignment, e.g. signal.pthread_sigmask.

**中文要点**：Popen与_ACTIVE_GROUP赋值之间有取消竞态。

**类型 / 是否修改**：要求修改 / 是（实现方式需裁决）。

**判断依据**：PS3 L191–203首次信号只记录，peek_child_exit会check_cancel，因此通常首次信号仍能进入清理；危险的是该窗口的第二次信号：_ACTIVE_GROUP尚空便终止helper。HQ指出的窗口真实存在。不能只在父线程pthread_sigmask后Popen再解屏蔽：子进程会继承阻塞掩码，父端恢复不等于子端恢复；preexec_fn又有已知多线程死锁风险。

**最小方案**：H2.diff给出不改变子进程信号掩码的候选：仅在spawn临界区记录第二信号，登记PGID后立即交还原二次信号终止路径；Popen失败也必须退出临界区。它改变“第二信号严格立即”的边界，需要PM批准，未当作验证过的实现。若HQ坚持pthread_sigmask，须另设计并验证exec前恢复子掩码的启动机制，不能直接采用单侧屏蔽。 [独立diff草案](../../tools/bolt/results/hq-review-361395/drafts/H2.diff)。该修改会改变tree；未应用、未测试。

**与PS4关系**：PS4未解决。设计此前将阻塞信号日志延后；本条是进程创建正确性，不应误认为新增日志已经处理。

**验证要求**：确定性注入Popen返回前/后、PGID登记前/后的一次/二次TERM/INT/HUP；验证进程组无遗留、129/130/143、继承忽略不变、子掩码不变、Popen抛异常与重复调用。两条备选路线不要同时混入。合并构建验证不足以替代这些竞态夹具。

**英文回复草稿（未发布）**：[原样文本](../../tools/bolt/results/hq-review-361395/replies/H2.txt)

```text
Agreed; the process group must be registered before a second cancellation can terminate the helper. This will be addressed in the next patch set. A parent-only pthread_sigmask wrapper would also pass the blocked mask to the child, so the fix must preserve the child's original signal mask and retain group cleanup on cancellation and spawn failure.
```

### H3. 显式传入 debugfiles.list

PS3 `packaging/clang-bolt-helper.py:1056`；[前后10行原文](../../tools/bolt/results/hq-review-361395/context/clang-bolt-helper.py.L1056.txt)。

> debugfiles.list is located via Path(ordinary).parent.parent.parent, which depends on the RPM build directory layout, and the check only verifies presence and a string match. Please pass the path explicitly from the spec.

**中文要点**：不应从ordinary路径的父层数推导RPM清单位置。

**类型 / 是否修改**：要求修改 / 是。

**判断依据**：PS3 L1056确实依赖parent.parent.parent；需要显式路径。HQ所谓“只检查presence/string match”只描述debugfiles_gate这一子门禁；post_gate L1067/1077–1087另外核对可执行文件SHA、debug identity/CRC、模式及符号关联，因此不是完全没有内容检查。成员列表检查仍是打包清单要求，不能删掉。

**最小方案**：H3.diff：post CLI增加--debugfiles-list；spec传%{_builddir}/%{buildsubdir}/debugfiles.list；逐层传至debugfiles_gate。保留原成员断言与所有现有identity门禁；release无debug_file时仍不要求文件存在。 [独立diff草案](../../tools/bolt/results/hq-review-361395/drafts/H3.diff)。该修改会改变tree；未应用、未测试。

**与PS4关系**：PS4未修改helper/spec；无逻辑冲突。

**验证要求**：真实不同深度ordinary路径、显式清单成功/缺失/缺项、debug与release、CRC/SHA负例；12组展开+平台5项解析，ARM/BOLT-off保持；同一轮T/D构建及安装LLDB核对。

**英文回复草稿（未发布）**：[原样文本](../../tools/bolt/results/hq-review-361395/replies/H3.txt)

```text
Agreed; the debugfiles.list path will be passed explicitly from the spec in the next patch set. The membership check is only one part of the post gate: the helper also verifies the installed executable and debug-file identities, debuglink CRC, and debug-file permissions. Those checks will remain in place.
```

### H4. 拒绝第二张 GNU 长文件名表

PS3 `packaging/llvm-static-archives-native.py:133`；[前后10行原文](../../tools/bolt/results/hq-review-361395/context/llvm-static-archives-native.py.L133.txt)。

> The GNU '//' long-name table is overwritten each time it appears, with no duplicate check. Please reject a second table, since the offset lookup assumes exactly one.

**中文要点**：第二个//表会覆盖第一个，后续offset解析错误地统一使用最后一张表。

**类型 / 是否修改**：要求修改 / 是。

**判断依据**：PS3 inspect L120初始化longnames，L132–133无重复判断，L143之后才解析全部raw_members；因此第二张表可能改变早先成员的名字解析。应显式拒绝重复。不能仅if longnames判断，因为第一张表为空也必须算已出现。

**最小方案**：H4.diff：新增seen_longnames=False；遇到//先检查标记、拒绝第二张，再存内容。GNU普通/thin档均适用。 [独立diff草案](../../tools/bolt/results/hq-review-361395/drafts/H4.diff)。该修改会改变tree；未应用、未测试。

**与PS4关系**：PS4的Chdr、TLSDESC零宽、RELR检查未涉及ar表；与现有加固直接叠加，不改变合法单表输入输出。

**验证要求**：普通/thin档双表拒绝、空第一表+第二表拒绝、零表和单表合法；复用全部转换器测试，夜间按已批准资源做450发货档检查和原bitcode重新转换比较，覆盖3853成员及10个debug档；不可把已native归档简单扫描冒称重新转换。

**英文回复草稿（未发布）**：[原样文本](../../tools/bolt/results/hq-review-361395/replies/H4.txt)

```text
Agreed; a second GNU long-name table should be rejected, including an empty duplicate. This will be addressed in the next patch set with an explicit seen-table flag. Valid archives with one table and archives without a long-name table will retain their current behavior.
```

### H5. converter 的 SIGCHLD 恢复

PS3 `packaging/llvm-static-archives-native.py:994`；[前后10行原文](../../tools/bolt/results/hq-review-361395/context/llvm-static-archives-native.py.L994.txt)。

> SIGCHLD is set to SIG_DFL in install_main() and not restored on exit (only one signal.signal call for SIGCHLD in the file). Please restore it in a finally block.

**中文要点**：install_main中的SIGCHLD重置没有恢复。

**类型 / 是否修改**：要求修改 / 是。

**判断依据**：PS3 L993–995确有重置，L1022–1024只恢复TERM/INT/HUP；install/convert自己的finally也没有恢复SIGCHLD。范围同H1：进程内缺口，不是修改RPM父shell。恢复必须覆盖parse_args的SystemExit、工具校验和转换异常，不应仅放在现有install的try内部。

**最小方案**：H5.diff：将原解析/转换主体置于内部函数，外层install_main保留启动日志/取消初始化，并用try/finally包住SIGCHLD重置到全部退出路径。保留PS4的日志格式、信号分类、null和输出失败处理。 [独立diff草案](../../tools/bolt/results/hq-review-361395/drafts/H5.diff)。该修改会改变tree；未应用、未测试。

**与PS4关系**：PS4尚未解决；同install_main附近有新增log_startup_context，需要手工核对顺序，不得丢失F1–F3。本草案以8ec86c3e为基底，已保留这些行。

**验证要求**：default/ignored/custom恢复，--help/坏参数/校验失败/转换失败/取消；SIGCHLD忽略继承时仍正常reap，无僵尸/漏收；与H4合并真实转换重放，再合并完整构建。

**英文回复草稿（未发布）**：[原样文本](../../tools/bolt/results/hq-review-361395/replies/H5.txt)

```text
Agreed; install_main should restore the original SIGCHLD disposition. This will be addressed in the next patch set with an outer finally block that also covers argument-parser exits and conversion failures. The reset is process-local and does not change the parent RPM shell's handler.
```

### Q1. post门禁与shell函数作用域

> Please confirm QB 1226850 log shows BOLT_POST_GATE_PASS, and that bolt_status_exit / bolt_optional (llvm.spec:578, 600) are in scope inside __spec_install_post (llvm.spec:966).

**中文要点**：确认QB post通过以及函数能在RPM post宏中使用。

**类型 / 是否修改**：问题/澄清 / 否。

**判断依据**：本次直接读已保存QB1226850日志：L25269 BOLT_POST_GATE_PASS；L25270调用bolt_optional，L25272为post BOLT_DISK_REPORT。spec L578/600在%install定义函数，L963–968将post文本追加至同一个install脚本，不是另开shell。成功日志直接证明optional可用，不能冒充执行了仅失败才用的bolt_status_exit；70号实际展开的/bin/sh -e信号夹具覆盖退出码传播。

**最小方案**：无产品diff；回复给出原文与作用域解释。

**与PS4关系**：PS4没有改变这些定义。

**验证要求**：不需单独新QB；H3改参数后在合并的一轮验证中再次核对post链、退出码及列表。

**英文回复草稿（未发布）**：[原样文本](../../tools/bolt/results/hq-review-361395/replies/Q1.txt)

```text
Confirmed: the saved build log contains BOLT_POST_GATE_PASS and then successfully invokes bolt_optional for the post disk report. The RPM post macro is appended to the same install shell script in which bolt_status_exit and bolt_optional are defined; it is not a new shell invocation. Signal-exit fixtures cover status propagation; this successful build log does not execute the failure-only bolt_status_exit branch.
```

### Q2. jump-past-end nop警告

> The BOLT 'jump past end' nop warning: I could not find where it is handled in clang-bolt-helper.py. Is it benign?

**中文要点**：helper哪里处理警告，是否可以称为benign。

**类型 / 是否修改**：问题/澄清 / 否（不建议按警告文本盲加门禁）。

**判断依据**：处理在PS3的bolt/lib/Core/BinaryFunction.cpp L1418–1431：目标等于函数末端且小于MaxSize，排除AArch64 veneer，注释Result of __builtin_unreachable，createNoop；条件跳转登记IgnoredBranches。helper记录日志和做既有门禁，不自己改nop。87号原2A/8B在99号已更新为5A/5B，剩余控制流未全部闭合；不能概括“所有警告都无害”。94号TLS检查与这些jump-past-end不是同一证明，不得互相替代。

**最小方案**：无产品diff；先解释上游行为和证明边界。若HQ要求禁止该模式，需单独设计裁决，会导致已验证输入失败，不能悄悄扩大门禁。

**与PS4关系**：PS4不涉及BOLT改写。

**验证要求**：不因这条澄清重构建；若后续改变警告处理，必须重新真实BOLT/产物验证，另行资源审批。

**英文回复草稿（未发布）**：[原样文本](../../tools/bolt/results/hq-review-361395/replies/Q2.txt)

```text
The replacement is implemented by BOLT itself, not by clang-bolt-helper.py. BinaryFunction.cpp handles a branch to the exact end of a function, within its maximum extent, as a pattern produced by __builtin_unreachable; it emits a nop and records conditional branches for profile validation. The helper preserves the log and checks the candidate. The warning text alone is not sufficient to label every occurrence benign.
```

### Q3. mlgo_build_jobs是否继承外层-j

> mlgo_build_jobs defaults to 6 (llvm.spec:63). Does QuickBuild's -j20/-j32 reach this define? Otherwise the LLVM build runs at -j6.

**中文要点**：宏默认6可能让QB外层20/32没有传入。

**类型 / 是否修改**：问题/澄清（并行策略待裁决） / 暂不纳入；可选第6项待裁决。

**判断依据**：已证实：QB1226850 L3303和74T L3207均为ninja -d keeprsp -j 6；spec L63/522/644分别默认值、普通Ninja和BOLT工具Ninja显式用该宏。父13c3e223也已有默认6与ninja -j mlgo_build_jobs，非本系列新引入。不能推断QB全局选项如何传递，但本次保存日志足够否定它在该构建已自动覆盖宏。

**最小方案**：先回复事实。是否接平台_smp宏、显式定义mlgo_build_jobs或继续保守默认由PM/HQ决定；未经裁决不列为必改项，不擅自把6调到20/32。决定后再给准确平台宏diff，不能凭名字假定可用。

**与PS4关系**：PS4不涉及并行度。

**验证要求**：若改变，新增宏展开覆盖未定义/显式覆盖/平台值及合法数值，先报内存预算；完整构建需监视ThinLTO链接峰值。一次构建不能同时证明多个不同-j的性能。

**英文回复草稿（未发布）**：[原样文本](../../tools/bolt/results/hq-review-361395/replies/Q3.txt)

```text
The saved build log confirms ninja -d keeprsp -j 6. The spec uses mlgo_build_jobs, whose fallback is 6; the outer build job setting did not override that define in this build. The BOLT tool build uses the same define. Changing the job policy requires a separate decision about linker memory and the platform's parallelism macro; it is not already inherited automatically.
```

### Q4. clang-accel体积、setup时间与BOLT资源

> For issue SRC-Nanjing/llvm#29, please share clang-accel unpacked size and buildroot setup time after hybrid linking (Part 1), plus BOLT stage time and peak disk usage.

**中文要点**：请求加速包实际解包体积、buildroot setup耗时和BOLT时间/磁盘。

**类型 / 是否修改**：问题/澄清（数据请求） / 否；需补测数据。

**判断依据**：已保存QB1226850的BOLT begin至compare-root为330s，后续post门禁15s；最大已记录BOLT作用域快照5,028,364,288B，不是连续峰值，也不是根总量。74T对应749s和24s；根du最大成功样本67,924,271,104B，32次du超时。各来源不可混比。现有clang-accel搜索只找到历史包/模型及身份限制，没有当前混合链接实际accel包的解包size和同口径setup测量；两项UNKNOWN，不把clang大小或rpm安装间隔顶替。未访问SRC-Nanjing/llvm#29，不能替HQ定义其测量口径。

**最小方案**：无产品diff。请HQ/用户明确accel包版本、目标架构、软硬链接计数、setup起止是否含依赖下载/安装；在下一轮计划内构建/加速包生成中补采，不今天测。

**与PS4关系**：PS4不改变当前测量缺口。

**验证要求**：一次QB/本地构建批次可增加采样，但若accel包由独立流水线生成，还需该流水线产物和setup记录；不能承诺仅LLVM构建就覆盖。

**英文回复草稿（未发布）**：[原样文本](../../tools/bolt/results/hq-review-361395/replies/Q4.txt)

```text
The requested accel-package unpacked size and setup-time measurement need the exact package and setup boundary; they cannot be inferred from the clang executable size. Please confirm the target accel package and whether setup includes dependency installation. In the saved build, BOLT begin through compare-root took 330 seconds, with a separate 15-second post gate. The largest recorded BOLT-scoped disk snapshot was 5,028,364,288 bytes; it is not a continuously measured peak or total buildroot usage.
```

### Q5. plugin导出与混合链接重复符号

> With CLANG_PLUGIN_SUPPORT enabled, does export_executable_symbols_for_plugins(clang) (clang/tools/driver/CMakeLists.txt:94) interact with hybrid linking and cause duplicate symbols?

**中文要点**：export_executable_symbols_for_plugins是否把动态/静态LLVM重复链接。

**类型 / 是否修改**：问题/澄清 / 否（现有证据未发现重复定义）。

**判断依据**：74T/D CMakeCache均CLANG_PLUGIN_SUPPORT=ON、LLVM_ENABLE_PLUGINS=ON、LLVM_EXPORT_SYMBOLS_FOR_PLUGINS=OFF。AddLLVM L1455调用export_executable_symbols，当前实际走L1439–1443 ENABLE_EXPORTS；它不是再添加一份LLVM。两边build.ninja L92065有--export-dynamic，L92066为组件静态档，无libLLVM.so/libclang-cpp.so。TIZEN_STATIC_LLVM使clang保持组件链接。不能由此保证任意外部plugin自己再链接一份LLVM时的ODR/ABI行为；未运行任意plugin载入。

**最小方案**：无代码diff；解释导出与引入库是两件事。建议下一轮补一个正确链接方式的最小plugin载入用例，不为了未知冲突关闭插件。

**与PS4关系**：PS4不涉及CMake链接。

**验证要求**：同轮构建确认clang NEEDED/link edge/导出符号；最小插件载入与预期plugin依赖，若需验证LLVM_EXPORT_SYMBOLS_FOR_PLUGINS=ON非当前配置，另行范围批准。

**英文回复草稿（未发布）**：[原样文本](../../tools/bolt/results/hq-review-361395/replies/Q5.txt)

```text
The current clang link does not combine libLLVM or libclang-cpp with its component archives. The recorded configuration has plugin support enabled, LLVM_EXPORT_SYMBOLS_FOR_PLUGINS disabled, and adds --export-dynamic to the statically linked clang. Exporting its symbols does not itself add another LLVM definition. This does not prove compatibility with an arbitrary plugin that brings its own LLVM copy; that case needs a plugin-specific loading check.
```

### Q6. 关闭BOLT是否恢复pre-PS3

> Please confirm that switching bcond_without clang_bolt to bcond_with restores the pre-PS3 build result.

**中文要点**：一行bcond回退是否恢复以前完整产物。

**类型 / 是否修改**：问题/澄清（纠正回退范围） / 否。

**判断依据**：否。开关关闭Part2 BOLT流水线，Part1混合链接、Part3固定flags/native转换仍启用；合入后Part4加固也仍在。PS2本身还有BOLT，故“关闭BOLT=pre-PS3”尤其不能成立。101五项解析证明开关可解析/隐藏BOLT步骤，不证明完整旧产物逐字节相同。

**最小方案**：无产品diff；回复明确关闭BOLT只是局部回退，完整回退需选定旧revision或逐Part撤销。若要求一开关撤全部属于新设计，须裁决。

**与PS4关系**：PS4保持同样开关边界。

**验证要求**：保留BOLT on/off、ARM展开测试；若用户要求整包回退等价，需指定确切tree并独立完整比较。

**英文回复草稿（未发布）**：[原样文本](../../tools/bolt/results/hq-review-361395/replies/Q6.txt)

```text
No: changing bcond_without clang_bolt to bcond_with disables Part 2 only. Hybrid linking and the fixed flags and archive policy remain enabled, so this does not restore the pre-PS3 tree or its complete build result. Restoring that result requires selecting the corresponding earlier revision or explicitly reverting the later parts.
```

## 3. 合并后的下一patch set范围与路线

基底为本地PS4（尚未上传），完整增量清单：

1. 继续保留Part4的压缩Chdr、零宽marker边界、RELR拒绝和101号F1–F5日志修正；这些已有138项通过，不等于HQ五项已通过。
2. H1：helper在子进程回收后恢复SIGCHLD。
3. H2：关闭Popen/PGID登记窗口；本次给出的候选只在spawn临界区延后二次信号，需裁决；不得将阻塞掩码泄漏给执行工具。
4. H3：spec向post显式传debugfiles.list，保留已有SHA/CRC/权限门禁。
5. H4：普通/thin ar均拒绝第二张GNU长名表，包括空表。
6. H5：converter在parse/转换/取消等所有退出路径恢复SIGCHLD，保留Part4启动诊断。

改动文件仅建议为 `packaging/clang-bolt-helper.py`、`packaging/llvm-static-archives-native.py`、`packaging/llvm.spec`。[累计diff草案](../../tools/bolt/results/hq-review-361395/drafts/combined-on-PS4.diff)通过Python AST语法检查，**不是单元测试或运行验证**，未创建任何产品提交、未变更工作树。H1–H5分项按顺序生成，H2与H1共改call，H5与PS4共改install_main边界，实际实施时不得盲目并行套补丁。

**推荐一次验证批次覆盖全部修改，不对每条重复全量构建：**

- 先裁决H2与Q3，冻结代码及对外说明；所有要求修改一次实现。补上述定向测试，重跑helper完整套件、转换器138项及新增用例。启动/二次信号、继承掩码、SIGCHLD回收、parse_args退出都需正反例；正常构建成功不能证明竞态消失。
- 重跑12组spec展开、平台5项解析及gbs export，ARM/BOLT-off变化只接受事先批准的范围；不临场加白名单。
- 资源批准后的夜间真实转换重放：保留450发货档验证、10个debug档及全部3853个转换成员的原始bitcode输入，重新生成并逐档/逐成员比较；原生输入保持不变，正常日志除已批准新增行外不变。
- **一轮QB验证 + 一轮本地完整构建验证**：每轮覆盖Toolchain和Base-Dev（QB各3架构，本地T/D x86_64串行），固定同一候选源码身份。不是用一个项目代替两个项目。逐包口径B、静态成员SHA、post/安装LLDB、工具版本与signal日志、没有shell报错；补debugfiles显式路径与最小plugin装载。下一轮源码包允许差异应先裁定上述三个包装文件/VCS及提交说明派生补丁头，不能误放过代码正文变化。
- 在同一轮采集明确的BOLT起止、子阶段计时、cgroup/进程内存和磁盘采样。clang-accel如由另外的包流水线产生，仍需那条流水线的同版本产物和setup记录，不能承诺只跑LLVM就得到它。

本任务没有启动上述任何验证、构建或QB。CPU/资源测量策略变更不是这五个修复自动附带的授权。

## 4. 需PM/用户裁决的点

- **H2**：同意“仅spawn临界区短暂延后第二信号”还是要求保持绝对立即并采用能恢复子掩码的另一机制？当前草案不悄悄改变既有约束，也不把pthread_sigmask单侧用法当成完整修复。
- **Q3**：是否把并行宏接平台预算，明确来源宏、显式覆盖优先级及链接内存上限？已证实-j6，但它原已存在；不擅自提高到20/32。若获准则成为第6个修改项，冻结后再与其余一起验证。
- **Q4**：当前clang-accel包身份/架构、setup边界与大小口径；当前精确数据缺失不能用模型补齐。需要何处生成该包由用户确认，本轮没访问所提内部issue。
- **Q2**：HQ是在问解释，还是要求新增拒绝门禁？现有5A/5B不应改写为全面“benign”；若要求新门禁，需额外资源和范围裁决。
- **Q6**：若HQ实际要求一键回退所有Part，需明确目标revision及新开关设计；当前一行bcond只是关闭BOLT。

## 5. 证据边界与交付

已读：PS3与PS4的相关git对象；保存的QB1226850包日志（没有访问QB）；74号T日志及T/D CMakeCache、clang链接边；70号信号夹具记录；79号既有资格记录；84号资源锚点；87号BOLT触发源码；94号TLS结论；99号5A/5B更新；101号测试/PS4状态。关于动态plugin只读源码和既有构建边，没有实际装载测试。没有新测accel包和setup时间，没有现场运行BOLT/真实转换/构建，没有查询其他Gerrit change或写Gerrit/sandbox。

[日志锚点](../../tools/bolt/results/hq-review-361395/log-anchors.json)、[QB post原文](../../tools/bolt/results/hq-review-361395/qb1226850-post.txt)、[BOLT磁盘快照](../../tools/bolt/results/hq-review-361395/qb-bolt-disk.json)、[plugin配置/链接边](../../tools/bolt/results/hq-review-361395/plugin-link-evidence.json)、[父提交-j宏](../../tools/bolt/results/hq-review-361395/mlgo-jobs-parent.txt)、[既有信号测试摘录](../../tools/bolt/results/hq-review-361395/existing-signal-tests-evidence.txt)、[accel证据搜索范围/结果](../../tools/bolt/results/hq-review-361395/accel-evidence-search.json)。没有把搜索“未定位”写成全世界不存在测量。

REST404/元数据缺失不是STOP。准备错误1次：diff生成器假定log_startup_context紧跟def，实际前有global及取消初始化；首次断言原文保留，按授权修正一次并继续。仅涉及草案脚本，未更改产品/测试预期。[原错误](../../tools/bolt/results/hq-review-361395/preparation-error.txt)、[修正diff](../../tools/bolt/results/hq-review-361395/preparation-fix.diff)。全部STOP/远端拒绝原文：**无**。

11份英文回复逐份ASCII和对外禁词门禁通过（不提GitHub、证据仓库、内部报告号/路径或sandbox），只存证据仓库；并没有获得发布Gerrit回复的授权。[回复索引](../../tools/bolt/results/hq-review-361395/replies/README.md)。

4GiB/swap0/CPU200%/Nice19/IO idle串行用户服务，每30秒看门狗，低于6GiB停止自己的服务；资源及看门狗快照见证据。只推证据仓库bolt-v4，不推产品任何分支。

```text
103步骤1 已结束 2026-11-16T03:55:56.536839-08:00 status=PASS (inline metadata UNKNOWN)
103步骤2 已结束 2026-11-16T03:55:56.536839-08:00 status=PASS (drafts only)
103步骤3 已结束 2026-11-16T03:55:56.536839-08:00 status=PASS
```

[全部raw链接索引](../../tools/bolt/results/hq-review-361395/RAW_LINKS.md)。
