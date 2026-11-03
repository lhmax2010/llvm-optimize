# 54：2026-11-03 夜间 Toolchain / Base-Dev 完整构建结果

两轮 GBS 构建均退出 0 并产出 RPM，但**整轮结论是“有问题”，不是全部通过**：T 的构建后验证读日志时发生 `MemoryError`，D 随后在构建后验证控制器中发生 OOM，night 于 2026-11-04 04:13:34 +08:00 停止。T 的 strip-all 和 RUNPATH 后 SHA 与认证值一致，最终 clang 只有 debuglink CRC 的 4 个字节不同；该差异不在已批准的命令记录节例外内，不能认定通过。23 包内容比较、两组 90 TU、D 的真实 release 成员复测、MODULE 加载等没有完成，现场全部保留，未重试、未手动启动 D。

## 1. 启动与监控

源码 `9e39fa8a61392652bb28b75fc26216675bcad1d5`，tree `cbc33271f8a9a7a5bd4de3c806bed6182c268e98`。证据仓库启动时为 `38a6a12ccc53a3407ae7091944caf766b3cd9db8`；本轮未修改 LLVM、spec、helper 或任何入口脚本。

23:18 启动前只读检查：/home 可用 261,111,164,928 B（243.179 GiB），超过 176 GiB；`temp/night-20261103/{toolchain,basedev,night.log}` 均不存在；没有其他 GBS/rpmbuild 构建进程。原样执行一次：

```sh
/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/night-launch-20261103/launch.sh 9e39fa8a61392652bb28b75fc26216675bcad1d5 night
```

前台输出（启动时会话记录）：

```text
Running as unit: llvm-night-20261103.service; invocation ID: 94396e91c36e4602b0c4771caad24fb5
Night controller started; T then D, never parallel
tail -f /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261103/night.log
```

启动后确认 service active/running，night.log 首条 T 记录：

```text
NIGHT_PROGRESS 2026-11-03T23:18:57.843751+08:00 toolchain service=active tail=''
```

会话期间只读观察，约每 30 分钟读取进度与资源，临近阶段切换增加只读日志检查。T 与 D 串行；T 普通 validation failure 后由已授权入口自动启动 D，并非手动续跑。没有重试、杀外部进程、手工卸载、删除、装包或 LLDB 测试。原入口自己的 du 采样沿用既有 `sudo -n chroot ... du`，其 argv 保存在 du-root.jsonl；本轮没有另发 sudo 命令或认证。

## 2. 结束标记与失败位置

night.log 原文：

```text
NIGHT_PROJECT 已结束 2026-11-04T02:58:38.377282+08:00 toolchain {'status': 'failed', 'reason': 'build-or-validation-failed-see-failure', 'start_ns': 1793719137855810597, 'end_ns': 1793732315853963528}
NIGHT_PROJECT 已结束 2026-11-04T04:13:32.290708+08:00 basedev {'status': 'stopped', 'reason': 'memory-oom-stop'}
NIGHT 已结束 2026-11-04T04:13:34.194671+08:00 status=stopped reason=memory-oom-stop
```

来源：[night.log](../../tools/bolt/results/night-results-20261103/night.log)、[night-result.json](../../tools/bolt/results/night-results-20261103/night-result.json)。

|项目|GBS build-result|耗时|自动 validation/result.json|项目最终状态|
|---|---|---:|---|---|
|T / Toolchain debug|exit_code=0|12943.782 秒|status=failed，checks={}|failed|
|D / Base-Dev release|exit_code=0|4173.033 秒|未生成；只有 certified-sha-check.json|stopped / memory-oom-stop|

T 开始/结束：2026-11-03T23:21:38.006783+08:00 → 2026-11-04T02:57:21.788362+08:00；D：2026-11-04T03:00:57.231037+08:00 → 2026-11-04T04:10:30.263878+08:00。这是 build-result 的 GBS 调用时段，不包含此前 export/prep 与之后验证。

T 的 [toolchain/validation/failure.txt](../../tools/bolt/results/night-results-20261103/toolchain/validation/failure.txt) 原文：

```text
Traceback (most recent call last):
  File "/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/night-launch-20261103/validate.py", line 100, in main
    log=logpath.read_text(errors='replace');lines=log.splitlines();anchors={}
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/pathlib.py", line 1030, in read_text
    return f.read()
           ^^^^^^^^
MemoryError
```

T 控制器 failure.txt：

```text
Traceback (most recent call last):
  File "/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/night-launch-20261103/launcher.py", line 243, in worker
    stage(D, 'validation', ['python3', '-B', str(T / 'validate.py'), '--project', PROJECT, '--root', str(D), '--peer', str(D.parent / 'toolchain')])
  File "/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/night-launch-20261103/launcher.py", line 69, in stage
    raise RuntimeError(name + ' failed, rc=' + str(r.returncode))
RuntimeError: validation failed, rc=1
```

D 没有生成 failure.txt 或 validation/result.json，不能补造 traceback。systemd 原文：

```text
Nov 04 04:13:31 linhao-linux systemd[2503]: night-basedev-full-controller-20261103.service: A process of this unit has been killed by the OOM killer.
Nov 04 04:13:32 linhao-linux systemd[2503]: night-basedev-full-controller-20261103.service: Failed with result 'oom-kill'.
Nov 04 04:13:32 linhao-linux systemd[2503]: night-basedev-full-controller-20261103.service: Consumed 3min 12.503s CPU time, 16.4G memory peak, 0B memory swap peak.
```

[services-final.json](../../tools/bolt/results/night-results-20261103/services-final.json) 显示 D controller `Result=oom-kill`、`ExecMainStatus=15`、MemoryPeak=17,712,934,912 B；T controller MemoryPeak=7,971,561,472 B。两轮**构建服务**的 memory.events 均 oom=0、oom_kill=0；OOM 发生在其后的控制器/验证服务。D 已保存 validation-command.json 与认证清单核对结果，却没有后续 checks；结合与 T 相同的日志读取代码，推测在同一个日志读取阶段触发内存耗尽，日志不能精确定位被杀时的 Python 指令。

### 2.1 只读定位到的入口缺陷

[launcher.py.excerpt.txt](../../tools/bolt/results/night-results-20261103/launcher.py.excerpt.txt) 中的日志游标尾部校验变量 `anchor` 起初是 bytes，阶段识别循环又用 `for phase,anchor in ...` 将它覆盖为 str。下一轮 `src.read(len(anchor)) != anchor` 必然为真，反复把读取位置重置为 0。生成的 run.py 同样保留此逻辑；log-restarts.jsonl 有 T=6242、D=2051 条。

|日志|T 字节|D 字节|
|---|---:|---:|
|GBS canonical success/log.txt|18,260,483|18,186,614|
|采样器 evidence/rpm-build.log|46,429,749,465|15,076,896,925|

validate.py:100 把整个累计日志 `read_text()` 后 `splitlines()`，T 已直接证明 MemoryError；D 的同类大日志和 OOM 是同方向证据。这些累计日志共约 57.283 GiB，本轮不删除，也不把它们整体压缩上传。上传的是两份 GBS 完整 canonical 日志与原始资源采样；源码证据、日志重置计数和失败输出均保留。

另一个停止策略缺口：`critical_stop()` 检查 cgroup OOM/disk/residual，但没有将 Python `MemoryError` 归为内存停止。因此 T 被归为普通验证失败后 D 自动继续；D 的 `Result=oom-kill` 才停止全流程。记录此事实，不改入口，不将它解释为用户手工授权重试。

只读发现的后续风险（本次尚未执行到）：validate.py `packages()` 在无 products 时查询 `gbs-root/local/repos`，实际 RPM 在 `gbs-driver/local/repos`。此项不是本次最先失败原因。修复入口/验证器或补做验证均留待后续授权，本轮未实施。

## 3. T：构建内证据与未完成项

### 3.1 三级 SHA 与精确字节差异

identity.json 原始记录见 [toolchain/work/identity.json](../../tools/bolt/results/night-results-20261103/toolchain/work/identity.json)：

|阶段|本轮 SHA256|与认证值|
|---|---|---|
|strip-all|`13a07cb7f84bd1ceda4d851c8bd71bddf7ef0c2d4864892eba64cbbb9a0350b8`|相同|
|RUNPATH 调整后|`8c2429d870f421a29a9914458bc4d4ff2ce359a15e0bdd20f39bfb4580c40bdf`|相同|
|最终 clang（debuglink 后）|`6c63c5c26bf68a7079d69ac8a41500c696267e1553a44e8be839632e9d676f17`|不同，认证值 `4f08e12d499ebd492ce4951f74915ba435f57f2e380dc6f3520f24644996cb17`|

结束后仅按本任务要求做了只读最终文件差异分析，未重跑验证器。两份文件均 152,532,400 B，ELF 头和全部节头相同。全文件分块逐字节比较得到**唯一**差异：

|文件偏移（十进制）|认证值 hex|本轮 hex|所属节|
|---:|---|---|---|
|152529896|01|da|.gnu_debuglink|
|152529897|83|ae|.gnu_debuglink|
|152529898|e7|35|.gnu_debuglink|
|152529899|69|1c|.gnu_debuglink|

其余全部字节相同，没有整节或成员跳过。`.gnu_debuglink` 文件名均为 clang-22.debug，CRC 从 1776780033（0x69e78301）变为 473280218（0x1c35aeda）。本轮符号文件 SHA=`5960755056a399e66b04ba7583403cc2cf6b907b72b3a984f4836f2ed37885a0`、35,321,968 B；post 记录同一 CRC，认证符号 SHA 是 be17f722…，因此 CRC 变化与不同符号文件相符。但本轮未完成符号文件差异归因；**最终差异发生在 debuglink，不是 .GCC.command.line，不能套用既定例外判 PASS**。详情、每个偏移和比较代码：[toolchain-final-byte-diff.json](../../tools/bolt/results/night-results-20261103/toolchain-final-byte-diff.json)、[elf-diff.py](../../tools/bolt/results/night-results-20261103/elf-diff.py)。

### 3.2 FLAGS / profile / 构建内门禁

FLAGS 原文（T canonical 日志行号）：

```text
L659: [  255s] TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] CXXFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] LDFLAGS=[]
L661: [  255s] TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[] CXXFLAGS=[] LDFLAGS=[]
```

`TIZEN_LLVM_FLAGS_WARNING` 实际输出 **0 条**；不存在的 warning 行不伪造为日志。DROPPED 为空，符合预期。

profile 计数原文（pipeline-result.json）：

```text
{"N": 23592, "M": 144032, "S": 0, "U": 1, "Q": 383, "R": 4.238545331242318e-05, "S_over_N": 0.0}
```

R=0.004238545331242318%，与 39/43 号认证计数相同。BOLT rewrite 日志摘录见 [toolchain/profile-log-excerpts.txt](../../tools/bolt/results/night-results-20261103/toolchain/profile-log-excerpts.txt)。

构建日志锚点（不是重新执行的门禁）：

|锚点|T 行号 / [秒]|
|---|---|
|TIZEN_HYBRID_LINK_OK|L11326 / 7576|
|BOLT_PROC_OK|L16916 / 7904|
|真实 tool dry-run BEGIN / END|L22804 / 8231；L23159 / 8233|
|BOLT_NINJA_EXIT_0|L23511 / 8461|
|BOLT_DEBUG_SYMBOLS_PASS / BOLT_DEBUGLINK_PASS|L24116 / 9186；L24118 / 9194|
|三处 BOLT_REAL_GATE_PASS|L24115 / 9183；L24119 / 9207；L25189 / 12633|
|BOLT_PIPELINE_PASS|L24122 / 9207|
|BOLT_COMPARE_ROOT_PASS|L24128 / 9373|
|BOLT_CACHE_RELEASE removed|L24130 / 9382；21,630,156,800 B|
|NATIVE_ARCHIVES_END PASS 225|L24601 / 11928|
|BOLT_POST_GATE_PASS|L25192 / 12633|

原文：[toolchain/anchors.txt](../../tools/bolt/results/night-results-20261103/toolchain/anchors.txt)、[toolchain/extra-anchors.txt](../../tools/bolt/results/night-results-20261103/toolchain/extra-anchors.txt)；完整日志：[toolchain/gbs-success.log.gz](../../tools/bolt/results/night-results-20261103/toolchain/gbs-success.log.gz)（解压后共25,676行）。tool-plan/tool-verify 与 post JSON 均存于 toolchain/work/，不是新跑的检查。

### 3.3 T 验证状态

|项目|本次结果|
|---|---|
|构建并打包|22 个二进制 RPM + 1 个 SRPM；GBS exit0|
|构建内 post 与 debugfiles.list|post 原记录通过，debugfiles.list 包含 /usr/lib/debug/usr/bin/clang-22.debug；RPM 文件清单也含该路径|
|认证 products SHA256SUMS|自动验证已完成，见 validation/certified-sha-check.json|
|23 包载荷逐字节比较（含 ar 日期分类）|**NOT RUN**，验证读取日志失败在前；包数不能代替内容比较|
|本轮对认证 clang 的 90 TU|**NOT RUN**，没有 90/90 结论|
|装包/LLDB|按要求未做，留到明早；最终 SHA 已变，不能直接沿用认证安装结果|

## 4. D：release 产物与验证缺口

### 4.1 FLAGS 和 profile

FLAGS 原文：

```text
L627: [  245s] TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] CXXFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] LDFLAGS=[]
L629: [  245s] TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] CXXFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] LDFLAGS=[]
```

WARNING 实际输出 **0 条**。CFLAGS/CXXFLAGS 的 DROPPED 恰为四个预期 token，LDFLAGS=[]。

pipeline-result.json 计数：

```text
{"N": 23592, "M": 144032, "S": 23, "U": 1, "Q": 383, "R": 0.0010172508794981563, "S_over_N": 0.0009749067480501865}
```

R=0.10172508794981563%，S/N=0.09749067480501865%，均小于现有 5% 门槛。不能要求 release 的统计与 debug 相同。本轮没有放宽门禁。BOLT 原文（[basedev/bolt-rewrite.log](../../tools/bolt/results/night-results-20261103/basedev/bolt-rewrite.log)）：

```text
L9: BOLT-INFO: pre-processing profile using branch profile reader
L23: BOLT-INFO: 23592 out of 144032 functions in the binary (16.4%) have non-empty execution profile
L24: BOLT-INFO: 383 functions with profile could not be optimized
L25: BOLT-WARNING: 23 (0.1% of all profiled) functions have invalid (possibly stale) profile. Use -report-stale to see the list.
L26: BOLT-WARNING: 1004909918 out of 140739851572 samples in the binary (0.7%) belong to functions with invalid (possibly stale) profile.
L27: BOLT-INFO: profile for 1 objects was ignored
L28: BOLT-INFO: profile quality metrics for the hottest 1000 functions (reporting top 5% values): function CFG discontinuity 0.00%; call graph flow conservation gap 0.00%; CFG flow conservation gap 0.00% (weighted) 0.00% (worst); exception handling usage 0.00% (of total BBEC) 0.00% (of total InvokeEC)
```

D 构建内锚点：HYBRID_OK L11294 [2510s]，PIPELINE_PASS L24082 [2686s]，COMPARE_ROOT_PASS L24088 [2733s]，CACHE_RELEASE L24090 [2734s]（1,602,985,984 B），NATIVE_ARCHIVES_END L24561 [4024s] PASS 225，POST_GATE_PASS L24949 [4072s]。三处 real 在 L24077、L24079、L24946。release 没有 DEBUG_SYMBOLS_PASS/DEBUGLINK_PASS，identity 没有 debug_file/debuglink 字段。完整原文见 [basedev/anchors.txt](../../tools/bolt/results/night-results-20261103/basedev/anchors.txt)、[basedev/gbs-success.log.gz](../../tools/bolt/results/night-results-20261103/basedev/gbs-success.log.gz)（25,221 行）。

### 4.2 find-debuginfo 与实际包

[basedev/find-debuginfo.json](../../tools/bolt/results/night-results-20261103/basedev/find-debuginfo.json)，关键原文：

```text
L24564: [ 4029s] + /usr/lib/rpm/find-debuginfo.sh /home/abuild/rpmbuild/BUILD/llvm-22.1.8
L24565: [ 4030s] WARNING: /usr/bin/clang-22 is already stripped!
```

因此 release 模式仍实际执行平台 find-debuginfo 链，但已 strip 的 clang-22 被跳过。它也处理了其他未完全剥离文件；这不表示最终一定发布 debuginfo 子包。

实际仅 **12 个二进制 RPM + 1 个 SRPM**，没有任何 debuginfo/debugsource RPM，故不存在可列的 D 调试包载荷。D 全部包名：

clang, clang-devel, compiler-rt, libllvm, libomp, libomp-devel, lldb, lldb-devel, llvm, llvm-devel, llvm-static-devel, python-clang, llvm [src].

D 相对 T 缺少的十个调试包：clang-debuginfo, clang-devel-debuginfo, compiler-rt-debuginfo, libllvm-debuginfo, libomp-debuginfo, lldb-debuginfo, lldb-devel-debuginfo, llvm-debuginfo, llvm-debugsource, llvm-devel-debuginfo。D 无新增包；双方共有包的路径集合按 `rpm -qpl` 对比相同（**仅文件清单，不是内容/hash 相同**）。[rpm-list-differences.json](../../tools/bolt/results/night-results-20261103/rpm-list-differences.json)、两个 rpm-inventory.json 保存路径、包大小、完整文件清单和查询输出；原始 RPM 都留在各自 gbs-driver/local/repos/。

### 4.3 静态库、MODULE 与其余验证

|项目|本次能确认的事实 / 未完成项|
|---|---|
|转换器构建内输出|225 个 NATIVE_ARCHIVE_INSTALLED 记录，合计3853个转换成员、11个原样保留成员；D 的 debug_members 合计0（T为3853）。来源是转换器自己的输出，未冒充独立RPM载荷复核|
|static-devel RPM 成员独立检查|**NOT RUN**；未重新解包并逐成员检查调试节|
|真实 release 成员 C-2 正/反例|**NOT RUN**；没有把合成夹具结果当真实成员结果|
|产物 .GCC.command.line 不含四个 DROPPED token|**NOT RUN**；FLAGS日志仅能证明输入过滤，不能代替全产物扫描|
|MODULE 库命令与 dlopen|**NOT RUN**；本轮只补查 Cache 值，未加载库|
|D 对 T 90 TU|**NOT RUN**，没有90/90结论|
|helper post|已有 post JSON：sha_unchanged、aliases_pass、strip_identity_pass、installed_security_preserved、real_pass 为 true，三目标 tiny byte_equal 均 true；debug=null|

D post 完整 JSON 原文：[basedev/work/post-gate/post-result.json](../../tools/bolt/results/night-results-20261103/basedev/work/post-gate/post-result.json)；225条转换输出：[basedev/native-installed-records.json](../../tools/bolt/results/night-results-20261103/basedev/native-installed-records.json)。其中tiny/real用例不能代替90 TU。

## 5. 补查 MODULE 参数

两份 CMakeCache.txt 均为以下**同一原值**：

```text
CMAKE_MODULE_LINKER_FLAGS:STRING=-Wl,-z,relro,--as-needed -Wl,--gc-sections
```

精确等于用户要求的 `-Wl,-z,relro,--as-needed -Wl,--gc-sections`，无额外空格或 token。来源：[toolchain/CMakeCache.txt](../../tools/bolt/results/night-results-20261103/toolchain/CMakeCache.txt)、[basedev/CMakeCache.txt](../../tools/bolt/results/night-results-20261103/basedev/CMakeCache.txt)。这是只读缓存检查，不证明每个 MODULE 的链接/加载已经验证。

## 6. 资源与磁盘（只记录，不作通过判定）

固定条件：原入口 MemoryMax=24,482,979,840 B（MemTotal−8 GiB）、MemorySwapMax=0、CPUQuota=1200%、nice10、ionice2/7；GBS --threads=30，jobs8 / _smp_mflags -j8 / _costomized_smp_mflags -j20；普通 Ninja 和 llvm-bolt 工具 Ninja 实际均 -j6。T/D 构建服务全程 memory.peak 分别 19,148,963,840 B（17.834 GiB）、14,714,576,896 B（13.704 GiB），**包含文件缓存**；构建 swap 峰值0。控制器/验证器峰值另见§2，不能与构建服务峰值混成一个数。

### 6.1 T：resource-table.md 原样

|Phase|Seconds|Cgroup sampled bytes (includes cache)|llvm-bolt VmHWM bytes|Root du sampled bytes|Filesystem min available bytes|
|---|---|---|---|---|---|
|ordinary-build|7321.286190718|19146416128|UNKNOWN|47920926720|196272267264|
|ordinary-install|328.149041528|14991839232|UNKNOWN|60357607424|182595039232|
|BOLT|1469.823620199|16283660288|9931661312|70485561344|163517423616|
|cache-release|10.353324958|3645648896|UNKNOWN|UNKNOWN|164688289792|
|archive-conversion|2551.103411269|10596343808|UNKNOWN|55093010432|160152088576|
|platform-post|699.857052253|7375040512|UNKNOWN|47143387136|162207100928|
|packaging|298.865193413|10014306304|UNKNOWN|42598031360|163214110720|

来源：[toolchain/evidence/resource-table.md](../../tools/bolt/results/night-results-20261103/toolchain/evidence/resource-table.md)。独立读取采样并复算得到逐字相同的表；没有改写原文件。

### 6.2 D：原表缺失，结束后只读汇总

D 在生成 `evidence/resource-table.md` 之前被 OOM 杀死，**原表不存在**。不能伪造“原样”表。下面是结束后读取本次原始 JSONL，按同一汇总公式生成到新证据目录的表，明确标为 **postmortem**；没有重跑入口或修改 D：

|Phase|Seconds|Cgroup sampled bytes (includes cache)|llvm-bolt VmHWM bytes|Root du sampled bytes|Filesystem min available bytes|
|---|---|---|---|---|---|
|ordinary-build|2264.477146341|11202809856|UNKNOWN|10894733312|157159854080|
|ordinary-install|8.079896843|8609935360|UNKNOWN|11666124800|155562627072|
|BOLT|216.263532098|14474072064|9931550720|14148202496|152322973696|
|cache-release|4.15174922|3453927424|UNKNOWN|UNKNOWN|153846063104|
|archive-conversion|1291.066992962|4375175168|UNKNOWN|13821210624|141622312960|
|platform-post|49.590006624|3694190592|UNKNOWN|12963184640|141810987008|
|packaging|85.032977433|6626312192|UNKNOWN|13444767744|140572217344|

来源：[basedev/resource-table-postmortem.md](../../tools/bolt/results/night-results-20261103/basedev/resource-table-postmortem.md)、[resource-postmortem.py](../../tools/bolt/results/night-results-20261103/resource-postmortem.py)。阶段内存列是采样 memory.current 最大值，不是各阶段独立 cgroup memory.peak；llvm-bolt 列是采到的该进程 VmHWM，不是全进程峰值。UNKNOWN 表示没采到，不外推。

### 6.3 采样覆盖、最低空间与干扰

- toolchain：根占用最高采样 70,485,561,344 B（65.645 GiB），2026-11-04T01:52:37.998482+08:00；/home 最低采样 160,152,088,576 B（149.153 GiB），2026-11-04T02:30:17.767233+08:00。du 216条，其中非0返回/超时76条；资源样本6357条。
- basedev：根占用最高采样 14,148,202,496 B（13.177 GiB），2026-11-04T03:45:57.200668+08:00；/home 最低采样 140,572,217,344 B（130.918 GiB），2026-11-04T04:10:20.773723+08:00。du 70条，其中非0返回/超时0条；资源样本2076条。

T 的长链接时段有明显I/O等待，且du有缺样，不能把采样峰值说成连续观测的真实峰值。日志重复读取/写入污染了本轮耗时、整盘空间和控制器内存数据，不能用这次 T/D 用时比直接评估 LLVM 性能。两轮日志膨胀都在根外 evidence 目录，因此根 du 不包含约57GiB的累计日志，但 df 包含。

当前 /home（结束后只读记录）：

```text
Filesystem         1B-blocks          Used    Available Use% Mounted on
/dev/sda1      1967844950016 1726090432512 141717905408  93% /home
```

该次可用141,717,905,408 B，约131.985 GiB。采样数据没有触及20GiB停止线，最终停止原因是内存/OOM，不是磁盘不足。此数字会随系统其他写入变化，不作为未来开工保证。

## 7. 现场、交付与待处理项

[mounts-final.json](../../tools/bolt/results/night-results-20261103/mounts-final.json) 中 findmnt 对本次 N 的匹配为空；[processes-final.json](../../tools/bolt/results/night-results-20261103/processes-final.json) 中可读 /proc 无本次构建进程/cwd/root残留（不可读链接的盲区按文件说明），服务均已退出/failed。没有执行清理、删除、手工重试或手动启动D，所有根、RPM、日志和中间产物继续保留。

[source-status.json](../../tools/bolt/results/night-results-20261103/source-status.json) 显示源码已跟踪文件clean，HEAD/tree仍是本轮指定值。现场的两个验证目录没有补写成功结果；结束后新增的只是本报告的读取/汇总证据。

后续需要先处理入口日志重复和大文件一次性读入的问题，并明确 Python MemoryError 的串行停止规则；再按用户决定安排缺失的验证。T 的 debuglink CRC/符号差异还需按既定字节口径处理，不能自行扩大例外。D MODULE加载、release真实成员、两组90TU与逐包内容比较仍未认证。**本轮结论：有问题，保留现场，未重试。**

## 8. 证据索引

所有新证据位于 `tools/bolt/results/night-results-20261103/`：

- `night.log` / `night-result.json` / `night-progress.json`：全程与结束状态。
- `toolchain/`、`basedev/`：GBS完整成功日志gzip、构建结果、已有验证结果/失败原文、FLAGS与锚点、CMakeCache、BOLT JSON、包清单、资源JSONL。
- `toolchain-final-byte-diff.json`：最终clang四字节差异完整证明。
- `provenance.json`：复制的原文件路径、大小和SHA；`SHA256SUMS`：交付文件SHA清单。
- `services-final.json` / `basedev-controller-journal.json` / `mounts-final.json` / `processes-final.json`：结束后只读状态。
- `collect.py`、`supplement.py`、`elf-diff.py`、`resource-postmortem.py`：只读整理脚本，输出仅在本轮证据目录；不是构建或验证重试入口。

大累计日志仍在本机原位置，本报告使用可独立解压核对行号的 canonical GBS 日志。没有推送Gerrit/sandbox，也没有操作QB。
