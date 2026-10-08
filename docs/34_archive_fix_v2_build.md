# 34 归档修复 v2：llvm-strip 叠加验证与完整构建记录

本轮起点：`66c5671626ad3858131bab70115f25bb45ec9578`。开始时间：2026-09-29 22:46:29 +08:00。
docs/25–33 保持不动。本文与 STATUS 同一提交更新；不推 Gerrit。

> **2026-10-08收尾：构建成功，整体验收FAIL，已按预定规则停止。** 同根增量恢复后正常产出22个RPM，225个开发归档全部通过；首个compiler-rt归档的成员ELF字节与GNU strip基线不一致，触发§4.2门禁。新文件与离线llvm-strip输出完全相同，差异涉及ELF节表，不只是ar时间戳。没有继续消费者/测试包/续跑验收，没有生成或覆盖v2提交补丁。未改6/6/2或18GiB，无OOM；暂停历史保留。

## 0. 范围、独占与目标分支

本轮独占仅针对本项目的工作树、构建根及证据目录；其他项目构建允许并存。
耗时仅为过程记录，不作性能结论。完整 LLVM 准入为 MemAvailable ≥16 GiB，低于时每300秒读取、最多6小时；
18 GiB cgroup cap、MemorySwapMax=0、宿主可用内存低于2 GiB自动中止、nice15/ionice3及采样回收不变。
测试包另用可用≥8 GiB、cap6 GiB，串行运行。任何实验门禁失败即停止，不改参数重试。

| 别名 | 绝对路径或相对 W 的路径 |
| --- | --- |
| W | `/home/linhao/Toolchain/development/llvm-optimize` |
| E | `W/temp/archive-fix-v2-build-20260929`，本轮证据；仅本机保存 |
| S | `W/temp/llvm-archivefix-trial`，隔离试验分支 `archive-fix-trial` |
| Rnew | `W/temp/gbs-root-x86_64-archivefix-v2` |
| H | `W/temp/archive-index-fix-rpm-20260923/baseline-rpm-extract` |
| R0 | `W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0` |
| B30 | `W/temp/gbs-root-x86_64-archivefix/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build` |
| E28 | `W/temp/static-native-conversion-v2-20260924` |
| E29 | `W/temp/static-native-conversion-v3-20260924` |
| E32 | `W/temp/archive-fix-v2-20260929` |

启动时主仓库 status 为空，本项目及其他项目构建进程清单均为空；docs/33 已结束，未进入最长两小时的等待。
Rnew 独占锁 session=`archivefix-rpm-3e5933f3d6fc465985a7ededd4d5388e`，holder PID=9594。
R0 的22个RPM SHA全部匹配，H按逐包元数据复核17,689个路径，模式、类型、SHA/软链接目标差异0。
证据：`E/precheck.json`、`lock-acquired.json`、`rpm-identity.json`、`baseline-content-check.json`。

W/llvm 仍在 `sandbox/fangyu.he/llvm_optmize`，HEAD=`f111162e94aa48ed367c9d2c039456c70e7160ae`，
原 spec SHA=`95887b2d060b38d5ef8f56936f7481a03d131f9d26432180a68e02ec95f0dda5`，只保留原三处4/4/1本地并发差异。
本任务未改 W/llvm、未接触隔离旧混合根。S 的构建并发为本轮授权首次验证的6/6/2；转换器独立4 workers。

### 0.1 tizen_base 核查

本地已有 `refs/remotes/origin/tizen_base`：

```text
2d23367d74afbf2bb1e9e4013fce072b3a154109
```

这是本地冻结的远端跟踪引用，未声称刚与服务器刷新；因已有引用，fetch次数为0。
其 spec SHA=`7962d176484920de6138d70c7e8a8e1764dfada6655abf0332e9748167e889fd`，
f111162e HEAD spec SHA=`1155e2e32f7d797186a1003ca6f3d4c08ddaff8ab5594370b7e1938e9d9ba9ec`。
完整差异：`E/tizen-base-vs-workspace-head.diff`，SHA=`dfbb971c2ce7a5aeaf223322eba66b3e82df2ae43b9785d80858a7fa2d2f9b22`。
该 tizen_base spec 不含显式 `-O3`、`-flto=thin` 或 `LLVM_ENABLE_LTO` 设置；不能把工作区配方当成已合入目标分支。
证据：`E/target-branch.json`、`tizen_base.spec`、`f111162e.spec`、`tizen-base-log.txt`。

提交补丁的基准应为上述 tizen_base HEAD。转换修复对含bitcode归档生效；全机器码时Source打印SKIP。
因此修复可以先进入未启用ThinLTO的配方；配方随后启用ThinLTO时须满足认证选项策略。
两者分别提交，不把工作区其他配方差异混入归档修复。这里只说明依赖关系，不冒充目标分支完整构建验证。

### 0.2 试验输入与提交范围分离

最终Source与docs/32登记版本逐字节相同：
`tools/llvm_static_archives_source.py` 和 `S/packaging/llvm-static-archives-native.py` 的SHA均为
`6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557`。
Source按原命令白名单及末项生效规则恢复认证后端策略；拒绝未知选项、类型测试元数据、thin/other成员、LLVM主版本变化和强符号丢失。
包含600秒命令超时、信号取消、同目录原子回写、完整索引检查、原机器码保留和回写后清理；仅认证x86_64。

HQ行仅加到隔离试验spec：

```spec
%ifarch x86_64
%define __strip %{_bindir}/llvm-strip
%endif
```

用户提供了定义原文，未提供额外注释文本；未编造“HQ原注释”，已有spec注释保持原样。
试验spec SHA=`a9bbb24c142382c000a13a3fe70549c44e7ab33969a1a75337f0da675afd3969`；
相对f111162e的完整试验diff（含Source/HQ行）为`E/archive-native-conversion-v2-with-hq.diff`，
SHA=`6bf352d1e746fe9954ccd958be919de54c9546d5436fe5a05a3eacb8eb40be34`。
HQ独立diff见`E/hq-only-spec.diff`。**该HQ行不属于准备提交的归档修复。**

## 1. 全库准备与 llvm-strip 叠加实验

### 1.1 最终Source的全库离线转换

E32只完成了五代表归档第一遍，没有已完成的最终Source全225档产物。
本轮因此从已核验H新复制270档到`E/all-input`，用最终Source重新转换全部含bitcode的225档；
不以旧Source输出冒充v2输出。编译器/llvm-dis/llvm-nm来自H，运行库通过独立libxml2目录提供，未安装到宿主。

结果：225档、3,853个bitcode成员转换成功；11个原机器码成员保持字节；45档纯机器码运行库跳过。
全部转换归档通过成员次序/同名身份、x86_64 ELF ET_REL、完整外部定义符号索引及PIC检查。
强符号缺失0；允许消失的W类弱符号1,920，其余类型0。Source wall=1,631.522秒，外层阶段1,656.265秒；
cgroup MemoryPeak=12,603,363,328 B，MemoryMax=19,327,352,832 B，无OOM，采样器与日志线程均回收。

命令和证据：`E/convert_all.py`、`all-conversion-scope/plan.json`、`build.log`、`outcome.json`、
`scope-after-rpm.json`、`E/conversion/summary.json`及逐成员`symbols.json`。
本轮225档整档SHA与E28转换产物全部相同：`E/conversion-vs-docs28.json`（225 PASS、差异0）。
因此GNU strip参照与本轮转换输出具有相同的开发归档输入。

### 1.2 270档、两遍 llvm-strip

脚本：`tools/verify_llvm_strip_overlay.py`。每遍都从未strip的原件另复制，不将第一遍结果作为第二遍输入。
开发225档使用上述转换输出，compiler-rt45档使用B30的`lib64/clang/22/lib/linux`原件。
显式使用R0的loader、库和llvm-strip，不写R0：

```sh
R0/lib64/ld-linux-x86-64.so.2 \
  --library-path R0/usr/lib64:R0/lib64 R0/usr/bin/llvm-strip -g COPY.a
```

完整绝对argv见`E/llvm-strip-overlay/checks/**/strip-*.json`。
llvm-strip SHA=`d0b3cf18df5154b263ea009284b07cb1faced0758923d44953f2f53d70af509d`；
版本和依赖原文为`E/llvm-strip-overlay/version.log`与`libraries.log`。

| 输入 | 归档 | 成员 | 两遍退出0/空错误输出 | 成员顺序/同名身份、ET_REL、无DWARF、完整索引 | 两遍SHA相同 |
| --- | ---: | ---: | --- | --- | --- |
| 转换后的开发归档 | 225 | 3,864 | PASS | PASS | PASS |
| compiler-rt原件 | 45 | 1,964 | PASS | PASS | PASS |

540次strip全部通过，实验wall=68.247秒，scope峰值2,486,697,984 B。
证据：`E/llvm-strip-overlay/summary.json`、`E/strip-overlay-counts.json`、`llvm-strip-overlay-scope/outcome.json`。

### 1.3 与GNU strip的差异，不能只称为ar容器变化

225个开发归档和45个compiler-rt归档均属于 **ELF_MEMBER_BYTES**：全部5,828个成员的ELF文件SHA不同；
所有归档的完整符号→成员索引多重集合仍与GNU参照相同，索引差异0。
逐成员GNU/LLVM SHA、ordinal、名称及重复出现序号保存在§1.2摘要中。

对compiler-rt额外只读分析：1,964个成员的节区身份集合均不同（llvm-strip合并字符串表），
可分配节载荷SHA差异0；64个成员共66个节的`sh_entsize`不同。
例如第一份ASan对象，GNU输出11节、单独`.shstrtab`；LLVM输出10节、共用`.strtab`，
`.preinit_array`的entry size为8对0；节区偏移、索引引用及符号表字节也变化。
完整`readelf -hSW`原文及诊断：`E/strip-elf-analysis/{gnu,llvm}-readelf.txt`、
`summary.json`、`allocated-content-summary.json`。

这是结构诊断，不证明完整语义等价，也不豁免最终RPM的成员字节一致性要求。
本步用户明确要求的退出码、成员身份、格式、DWARF、索引和两遍确定性检查均PASS；GNU差异独立记录，不能静默归为“仅时间戳不同”。

## 2. 补齐离线门禁

五归档两遍完成，10个结果的逐成员SHA与整档SHA均与docs/28相同；两遍彼此确定性PASS。
外层阶段wall=352.664秒，采样器和日志线程均回收。命令与结果：`E/five_regression.py`、`five-regression-results.json`、`five-regression-scope/outcome.json`。

| 归档 | 成员数 | 第一遍 SHA | 第二遍 SHA | 与 docs/28 比对 |
| --- | ---: | --- | --- | --- |
| libclangCodeGen.a | 101 | `6aacfe043d4f0d4672b95b7038a6f1a073a03da2f2040eb4fda4cb07504ede5b` | `6aacfe043d4f0d4672b95b7038a6f1a073a03da2f2040eb4fda4cb07504ede5b` | 两遍成员/整档均相同 |
| libLLVMSupport.a | 179 | `6f19ce053b5626554b3e843e46def5968632c0e1e8f4eefb64397aacbd706f1d` | `6f19ce053b5626554b3e843e46def5968632c0e1e8f4eefb64397aacbd706f1d` | 两遍成员/整档均相同 |
| libarcher_static.a | 1 | `8b62ad19c1d6ed134baa37706a6aa6cbb8e320c71ca774c5179d5a62cdebabbc` | `8b62ad19c1d6ed134baa37706a6aa6cbb8e320c71ca774c5179d5a62cdebabbc` | 两遍成员/整档均相同 |
| libclangSema.a | 86 | `709c7865aee2f5cfd1dbb93e18d22c7406cf50673830e6b02591160a9dcf70b7` | `709c7865aee2f5cfd1dbb93e18d22c7406cf50673830e6b02591160a9dcf70b7` | 两遍成员/整档均相同 |
| libLLVMAnalysis.a | 131 | `7ed41555e1659b9895efadaaed835f13df2a367665901583397087a0d33ad0dc` | `7ed41555e1659b9895efadaaed835f13df2a367665901583397087a0d33ad0dc` | 两遍成员/整档均相同 |

实际删除强符号负例：用真实clang转换后对目标文件执行`llvm-objcopy --strip-symbol=must_preserve`，Source exit=1，明确报`strong defined symbols missing after conversion: [('T', 'must_preserve')]`；负例PASS。
600秒复验使用声明major22、转换时挂起且忽略SIGTERM的假编译器；最终Source exit=1，wall=603.252秒，错误明确含`command timeout after 600 s`。
这包含600秒时限及3秒TERM宽限，随后进程组被回收。外层负例阶段exit=0、wall=605.540秒，sampler/log reader均回收。
证据：`E/negative-real-final-results.json`、`negative-real-final/*/run.log`与`output/summary.json`、`negative-final-scope/outcome.json`。

继承门禁的最终Source绑定未变：E32的3,853条命令白名单PASS、四项类型元数据语义标记为0；unknown-mllvm/dwarf5/unroll/type-test/thin/copy-failure负例保留。
本轮又完整执行225档最终Source转换，因此全库选项和强符号检查已实跑。
`E/offline-gates.json`记录证据文件SHA；`E/trial-fingerprint-admitted.json`与仓库认证文件登记**offline_gate_status=PASS**。
此PASS只允许启动本次构建，不等于新RPM验收成功；GNU/LLVM成员字节差异明确记在放行清单中，没有豁免最终验收。
现有68项单元测试与2项strip检查正负对照全部通过；原始日志`E/unit-tests.log`、`strip-gate-unit-tests.log`。
`-fvisibility=hidden`负例作废：它不必删除定义符号，历史探针仅作说明，不作为失败门禁。
续跑按用户新决策分两步：真实独立buildroot的%install应再次转换；同一安装树随后直接调用Source才应SKIP。

## 3. 完整构建

唯一一次入口于2026-09-29 23:50:41开始，GBS于23:50:51在新根启动；2026-09-30晚按用户请求暂停，见§3.2。
首次MemAvailable=26,727,051,264 B，直接满足16GiB准入，未等待；每次读数保存在`E/full-build/memory-admission.jsonl`。
Base/Unified固定快照均HTTP200，repomd SHA与登记指纹一致；完整配置与命令见`resource-plan.json`、`source-fingerprint.json`、`build.log`。

```text
MemoryMax=18G; MemorySwapMax=0
GBS --threads 1; Ninja/compile/link=6/6/2; _smp_mflags=-j4
nice -n 15; ionice -c3; /usr/bin/time -v
```

CMake门禁在316.524秒通过，全部登记参数差异为0（`E/full-build/cache-gate.json`）；关键原文：

```text
CLANG_LINK_CLANG_DYLIB:BOOL=OFF
CMAKE_BUILD_TYPE:STRING=Release
CMAKE_CXX_FLAGS:STRING=  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument   -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables  -g -O3 -flto=thin -fomit-frame-pointer
LLVM_ENABLE_ASSERTIONS:BOOL=No
LLVM_ENABLE_LTO:STRING=Thin
LLVM_LINK_LLVM_DYLIB:BOOL=OFF
LLVM_PARALLEL_COMPILE_JOBS:STRING=6
LLVM_PARALLEL_LINK_JOBS:STRING=2
LLVM_TARGETS_TO_BUILD:STRING=X86;ARM;AArch64;BPF
LLVM_USE_LINKER:UNINITIALIZED=lld
```

启动前仅清理本轮自建的H重复输入副本`E/all-input`和`E/five-input`（6,233,880,088 B），保留原H、全部转换输出、strip输出和JSON/日志。
清理记录`E/scratch-copy-cleanup.json`；未删除历史构建根或本次失败现场。
原样完整构建argv及唯一尝试登记在`E/full-build-attempt.json`。没有第二次入口。

### 3.1 暂停前的受限链接观察

截至2026-09-30 13:15，日志最后一个完成项仍为00:41:48的7406/7634。
两个lld进程分别链接clang-22（PID64423）与libclang-cpp.so.22.1（PID64443），没有错误退出。
scope MemoryPeak已达到18GiB上限，memory.events的max持续增长，oom/oom_kill均为0；
因此不能把18GiB称为本次构建的自然峰值，也不能把未完成的运行记成容量认证PASS。

03:38:02读取的cgroup io.pressure full avg60=83.74%，memory.pressure full avg60=2.89%，
cpu.pressure full avg60=0.00%；03:49:37两个临时ELF仍有修改时间和空间分配增长。
04:14:24两条lld的累计read_bytes为92,161,425,408与69,234,577,408，write_bytes为
7,054,073,856与6,819,713,024，较前次持续增加。这里只证明I/O活动，不能据此推断剩余时间。
宿主可用内存仍约10.8GiB，未触发2GiB运行中保护线；16GiB是启动准入线，不作为运行中中止线。
未设置用户未授权的链接超时，未调整6/6/2、18GiB或swap0，未重试。

06:23:14再次采样：memory.current=19,327,254,528 B，memory.peak=19,327,352,832 B；
memory.events max=807,849，oom/oom_kill=0；io.pressure full avg60=90.38，
memory.pressure full avg60=4.28，cpu.pressure full avg60=0.00。
06:10两份临时ELF的分配空间分别为1,593,528,320与1,466,847,232 B，较05:34的
1,584,455,680与1,457,348,608 B继续增长，修改时间也更新；这不构成剩余时间估计。

08:01:03的两份临时ELF分配空间进一步增至1,629,863,936与1,486,024,704 B；
scope MemoryMax仍为19,327,352,832 B、MemorySwapMax=0，锁持有者仍为本轮hold_lock.py。
08:42:30复核主仓库HEAD、W/llvm HEAD与原spec、S HEAD/分支/spec/Source，均与启动登记一致，
主仓库只有本轮预期的四个文件改动。证据：`E/long-link-0800.json`、`E/mid-build-worktrees-0842.json`。

10:14:21再次核对同一组工作树/Source身份，结果不变（`E/mid-build-worktrees-1014.json`）。
11:01:02的scope仍active，MemoryMax=19,327,352,832 B、MemorySwapMax=0；
io.pressure full avg60=91.43，memory.pressure full avg60=3.64，oom/oom_kill=0
（`E/long-link-1100.json`）。12:01:00两份临时ELF分配空间为1,702,629,376与1,524,363,264 B，
仍有修改时间更新，scope仍active（`E/long-link-1200.json`）。没有因耗时长而中止或另起构建；
尚未开始%install及新RPM验收。

用户询问是否卡住后，13:14:32–13:14:52执行20.011秒只读差分诊断：两个lld合计CPU增量0.32秒、
主缺页增量1,041、read_bytes增量179,740,672 B；cgroup pgscan增量51,354、pgsteal增量43,738、
workingset_refault_file增量43,882、memory.events max增量582，oom/oom_kill增量0。
末次匿名内存18,396,569,600 B（约17.13GiB），file为625,713,152 B（约0.58GiB），
I/O full avg60=87.20；两进程各有一个线程等待`folio_wait_bit_common`，其余主要等待futex。
这是18GiB上限下反复回收/重读文件页、极低CPU利用的直接诊断证据；进程未退出、文件仍写入，
不将其称为机器死机或已证实的程序死锁，也不据此承诺完成时间。
原始双快照：`E/user-status-diagnosis-1313.json`。该cgroup未提供`io.stat`，诊断改读现有的
`/proc/PID/io`；只是可观测字段缺失，没有修改或重试构建。13:00的输入SHA复核仍一致：`E/long-link-1300.json`。

16:57:55核对的W原spec、试验spec及Source SHA仍与§0一致（`E/long-link-1700.json`）。
17:19:28，原来的clang-22链接实际完成：`[62868s] [7407/7634] Linking CXX executable bin/clang-22`；
17:19:41已推进到7416/7634。宿主MemAvailable于17:19:44回升到19.217GiB，oom/oom_kill仍为0。
17:50:55完成libclang.so.22.1.8，17:53:25之前完成libclang-cpp，17:54:01推进到7502/7634；
18:25:07最后一个完成项为7530/7634（clang-refactor）。18:58:35仍在运行的链接是clang-repl与clang-check，
其采样VmHWM分别11,474,500与9,507,428KiB（`E/long-link-1900.json`）。
这给出先前长时间停留最终恢复推进的实际证据；不代表剩余链接或打包验收已通过。

原始证据：`E/linker-io-progress.jsonl`、`linker-thread-states.jsonl`、
`link-output-progress.jsonl`、`link-pressure-observations.jsonl`及`E/full-build/samples.jsonl`。
这些过程观测不代替完整构建与RPM验收。

### 3.2 用户要求暂停、回收与节后恢复

用户明确要求“我要下班了，能帮我暂停下么，节后继续”，覆盖此前无人值守继续执行的要求。
按节日期间可能关机的情形保存磁盘现场并释放内存；不把保持开机和保留18GiB进程内存作为恢复前提。
19:19先冻结本项目scope，19:21:07向核对过argv的构建守护进程PID36967发送SIGTERM。
守护程序的scope清理终止用户态构建进程；root辅助进程的kill返回Access denied，随后解冻scope，
使这些辅助进程处理已退出的子进程并自然收尾。19:22:40确认scope inactive、本项目构建进程0。
未结束其他项目进程，未重启构建、未调整并发/cap/swap或源码。

| 项目 | 暂停实测与边界 |
| --- | --- |
| 最后完成任务 | 7530/7634；未完成的clang-repl、clang-check链接不算完成 |
| CMake | 316.524秒PASS，全部登记参数一致 |
| 构建退出记录 | 外层entry=2、child=-9、`KeyboardInterrupt('signal 15')`；用户中断，不是编译错误或OOM |
| 外层经过时间 | 70,265.131秒，含观察与暂停收尾；不是完整构建耗时，也不作性能结论 |
| scope MemoryPeak / MemoryMax | 均为19,327,352,832 B（18GiB）；触顶受限值，不是自然峰值 |
| 暂停前memory.events | max=2,368,916；oom=0、oom_kill=0、oom_group_kill=0 |
| 暂停前scope累计CPU | CPUUsageNSec=42,333,739,342,000；仅已执行部分 |
| 线程回收 | sampler_reaped=true，log_reader_reaped=true |
| 回收后宿主可用内存 | `free -m` available=28648MiB，约27.98GiB |
| 新RPM、验收、v2提交补丁 | 均未产出/未执行；不能宣称通过 |

原始暂停证据目录：`E/pause-20260930-1919/`，包括`frozen-checkpoint.json`、
`user-stop-request.json`、`stopped-checkpoint.json`、`resume-input-manifest.json`和`protected-files-check.json`。
完整退出与清理原文为`E/full-build/{commands.log,outcome.json}`、`E/full-build-entry-exit.json`。
中断发生在RPM命令正常返回之前，所以没有gbs.exit；outcome中的missing completion status是用户中断后的记录，
不能当作独立打包失败。独占锁在确认进程退出后释放，记录为`E/lock-released.json`。

保留Rnew的BUILD、对象、ThinLTO cache、Ninja状态及所有证据；未清理未完成链接的临时文件。
恢复核对清单已保存为`resume-input-manifest.json`（CMakeCache、build.ninja、Ninja状态和已完成关键ELF的大小/SHA）。
试验输入SHA见§0.2；W原spec、docs/25–33、gbs配置及v1补丁/Source与启动前SHA相同。

节后须先读STATUS及本节，核对清单和无竞争进程，重新取得项目锁；确认续跑入口保留BUILD、
不会重跑清空目录的%prep，再使用已完成对象及cache增量继续。当前两条未完成链接需要重新执行。
9月30日收尾时要求等待用户明确恢复，不自动启动第二次完整构建或改6/6/2、18GiB；该恢复授权已于10月8日到达，执行见§3.3。
剩余顺序：完成本次构建→新RPM全部门禁→七项宿主消费者→两个Tizen测试包→独立%install再转换和同树Source SKIP→提交补丁。

### 3.3 2026-10-08 恢复核查与增量入口

用户本次明确“继续吧，结束后记得报告一起发出来”。新增证据目录 U=`E/resume-20261008`，
不覆盖暂停前日志。主仓库起点 `d47d1507391de67398806210b15530711896b2b8`，status为空；
未发现本项目竞争构建进程。新锁session=`archivefix-rpm-18c3fd432fd245e0b043c7c6b4ef31e8`，holder PID82912。

恢复核查结果：

- 暂停清单8项（CMakeCache/build.ninja/Ninja状态/4个已完成ELF）大小与SHA一致；13项保护文件SHA一致。
  `U/checkpoint-identities.json`。S的HEAD、分支、spec/Source/diff仍通过精确认证。
- 构建根Source脚本SHA与S一致。首次检查错误地假定GBS导出spec与S逐字节相同；只读diff确认其全部差异
  恰为GBS加入的VCS和5项Patch/%patch条目，按精确文本重建后完全一致，没有更改任何spec或重新构建。
  根内导出spec SHA=`acded99407dc2ac02e22b0fff9097b7067297613d01777e5c4ad3b455dcb396b`。
  `U/gbs-export-spec.diff`、`root-inputs.json`、`precheck.json`。
- 检查168,959个准备源码文件：168,952个等于HEAD的Git blob；其余7个等于原导出tar中对应字节
  （归档替换元数据及测试数据），无缺失。直接把准备树与Git blob比较的首次断言因此返回1；
  进一步与本次实际%prep输入tar核对后等价性PASS，没有修复或替换源码。
  `U/prepared-source-identities.json`、`prepared-source-summary.json`、`prepared-source-equivalence.json`。
- MLGO导出包中的10,866项文件/链接与准备树一致：`U/prepared-mlgo-assets.json`。
- 根内RPM 4.14.1的help明确支持`--noprep`；宏查询为`clang|-j4|/home/abuild/rpmbuild|…`。
  Ninja dry-run为193项（链接/头文件整理），无C/C++编译；原RPM安装树为空、无新RPM。
  `U/chroot-preflight.log`。

采用docs/13 §4已验证的正常`-ba --noprep`机制，区别仅是不执行会删除准备树的%prep；
正常%build/%install/打包仍执行，不使用short-circuit生成正式RPM。原%build只有`mkdir -p build`、
CMake及Ninja，未清空build。原始argv与续跑argv逐项记录在`U/resume-attempt.json`：

```sh
rpmbuild --define '_smp_mflags -j4' --define '_srcdefattr (-,root,root)' \
  --nosignature --target=x86_64 --define '_build_create_debug 1' \
  -ba --noprep /home/abuild/rpmbuild/SOURCES/llvm.spec
```

外层仍用`gbs chroot --root Rnew/local/BUILD-ROOTS/scratch.x86_64.0`中的abuild登录shell，
由原`build_llvm_x86_64.py:build()`提供systemd scope 18GiB/swap0、nice15/ionice3、
time-v、30秒采样、2GiB宿主保护和退出回收。独立完成标志弥补gbs chroot不传播子命令退出码的问题。
`U/resume_once.py`限定该暂停现场、完整配置指纹和一次增量入口；没有再次调用初始化GBS入口。

实际于17:36:58启动。恢复后的CMake在12.202秒再次验证全部登记参数一致；重配置刷新少量生成文件，
Ninja实际为208项，包含compiler-rt dummy、llvm-config等辅助重编译，仍复用已有主体对象及已完成链接。
`U/build/cache-gate.json`、`build.log`、`launch.json`。日志出现`Can't read /proc/cpuinfo`，
根内/proc未挂载；docs/13同类续跑日志也有该提示（`temp/baseline-resume-20260917/run/build.log:2105`）。
这是记录到的运行环境差异，不据提示推断成功或失败，最终以命令退出和产物验收为准；本轮未修改挂载或宿主配置。

本次中断期间的八天不计入构建执行耗时。原段与恢复段分别保存time-v、scope及采样数据，
最终汇总须同时说明包含用户中断收尾、重复的未完成链接及重配置；耗时不作性能结论。

### 3.4 恢复段的构建推进与空间回收

20:25:16完成`[208/208] ... bin/opt`，20:25:17进入真实%install。
暂停时未完成的clang-check、clang-repl分别于17:57:11、18:07:55完成。
此前所有链接均正常推进；恢复段18GiB也触顶，但截至进入%install未记录OOM。
这些为过程记录，不作性能或无约束自然峰值结论；详见`U/build/build.log`及`samples.jsonl`。

安装未剥离ELF期间磁盘余量快速下降。20:35:44采样剩余9.240GiB，后续转换仍需临时空间。
在已确认208/208完成、%install开始且Rnew无Ninja/lld进程后，仅清理本次试验根`build/lto.cache`
中按mtime/name排序的8,677个可再生`llvmcache-*`文件：实际字节21,456,918,504、
分配空间21,474,836,480 B（20GiB）；20:37:21完成，文件系统余量26,191,749,120 B。
事前保存全量选中清单并逐文件核对inode/size/mtime后删除；未改缓存裁剪参数、构建对象、ELF、
源码、安装树、历史根或实验日志。此后不可把Rnew描述为保留了全部暂停缓存，未来重链可能需要重新生成这部分缓存。
证据：`U/cache-reclaim-plan.json`、`cache-reclaim-journal.jsonl`、`cache-reclaim-result.json`。
这是本次已完成链接之后的空间管理，没有发生ENOSPC后重试，也没有启动额外构建。

20:37:22记录`NATIVE_ARCHIVES_BEGIN`，使用本次构建的clang/llvm-dis/llvm-nm转换归档；
21:10:58记录`NATIVE_ARCHIVES_END ... PASS 225`。21:52:48正常退出，21:52:49完成标志PASS。

### 3.5 正常产出22个RPM及资源实测

`U/build/outcome.json`原文：

```json
{"exit_code":0,"elapsed_seconds":15351.380564073,"command_exit_code":0,
 "cache_passed":true,"problems":[],"sampler_reaped":true,
 "log_reader_reaped":true,"interrupted":null}
```

| 项目 | 实测 | 证据与边界 |
| --- | --- | --- |
| 恢复段wall | 15,351.381秒（time-v为4:15:51） | `U/build/time-v.txt`、`outcome.json` |
| 两段外层执行时间相加 | 85,616.511秒（约23小时47分） | `U/combined-build-resources.json`；排除节间8天，含暂停收尾、未完成链接重放及重配置，不是无中断构建或性能比较 |
| 恢复段user / sys | 34,092.59 / 579.94秒 | time-v；scope另记CPU usage 34,673.333729秒 |
| scope MemoryPeak / MemoryMax | 均19,327,352,832 B（18GiB） | `scope-after-rpm.json`；仍为受限峰值，不能给出自然内存需求 |
| memory.events | max=43,314，oom=0，oom_kill=0，oom_group_kill=0 | 原段和恢复段均没有OOM；没有降低6/6/2或抬cap |
| time-v最大RSS | 10,979,624 KiB（10.470985GiB） | 子进程高水位口径，不等于整个cgroup；恢复段链接采样最大为clang-repl 10,777,844 KiB |
| 恢复段最低宿主MemAvailable | 19,535,785,984 B（18.194118GiB） | 508个30秒采样；没有触发2GiB保护线 |
| 恢复段最低文件系统余量 | 6,409,388,032 B（5.969208GiB） | 采样下界；§3.4清理的是已完成链接的缓存，未删证据/对象/ELF |
| 转换主体wall | 1,528.010秒 | Source summary的elapsed_seconds，不含全部回写/清理 |
| 转换BEGIN→END | 2,015.697秒；日志整秒差2,016秒 | `E/native-archives-install.log`；包含扫描、转换、回写和清理 |
| 单次转换编译最大RSS | 1,040,448 KiB（0.992249GiB） | 3,853份转换命令wait4记录；4 workers、每进程4GiB AS |
| 转换期cgroup采样最大current | 19,327,156,224 B | 含文件缓存，不能当作转换进程自身内存；30秒采样不能代替自然峰值 |
| Source结果 | 225档、3,853 bitcode、11原机器码；45档跳过；强符号缺失0、允许W缺失1,920 | `E/install-conversion-summary.json`，状态PASS；大文件删除为true |
| 22个二进制RPM | 合计8,856,567,168 B | `E/rpm-inventory.json`逐包记录绝对路径、字节和SHA；正常-ba生成，不是short-circuit拼包 |

本次编译及正常打包最终完成，说明该次6/6/2配置在18GiB限制内可产包；
长时间回收/重读、主动暂停和缓存处理的事实仍保留，不把它登记为无条件高效配置，
也不把构建成功当作新RPM内容验收通过。两段链接逐目标高水位见`U/combined-build-resources.json`；
`E/build-resource-summary.json`保存恢复段全部链接、转换及阶段原始行号。

后处理日志（均为`U/build/build.log`行号）：

```text
7897  2026-10-08T20:37:22+08:00 NATIVE_ARCHIVES_BEGIN 1791463042.4250536
8348  2026-10-08T21:10:58+08:00 NATIVE_ARCHIVES_END 1791465058.1219857 PASS 225
8349  + /usr/lib/rpm/find-debuginfo.sh -j4 --build-id-seed 22.1.8-1 --unique-debug-src-base llvm-22.1.8-1.x86_64 -S debugsourcefiles.list /home/abuild/rpmbuild/BUILD/llvm-22.1.8
8894  + /usr/lib/rpm//brp-compress
8895  + /usr/lib/rpm/brp-strip-static-archive /usr/bin/llvm-strip
8896  + /usr/lib/rpm/brp-python-hardlink
8897  + /usr/lib/rpm/tizen/find-docs.sh /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64
```

这些后处理全部正常返回；strip格式错误0行，Source残留非JSON大文件0。
独立`brp-strip`调用为0，与docs/13原宏链日志相同；不能为满足清单而虚构其执行。
证据：`E/postprocessing-result.json`、`check_postprocessing.py`及`native-archives-install.log`。

## 4. 新RPM验收

### 4.1 解包与开发归档：PASS

22包通过`rpm2cpio | cpio -idmu --no-absolute-filenames --no-preserve-owner`解包到
`/home/linhao/Toolchain/development/llvm-optimize/temp/toolchain-archivefix-v2`，未安装到宿主。
逐个检查rpm2cpio与cpio退出码均为0，共有路径的RPM模式、摘要和链接目标一致；
全部包元数据及归属保存在`E/*-file-metadata.tsv`、`rpm-file-owners.json`，解包日志为`rpm-extract.log`。
解包前空间诊断第一次查询RPM的`%{SIZE}`返回`(none)`；改读`FILESIZES`得到49,641,927,101 B
（含硬链接重复项），当时可用70,343,266,304 B。只是只读字段查询修正，没有构建/验收重试；
记录见`U/extraction-space-check.json`。

验收入口`E/verify_new_archives.py`使用`tools/inspect_llvm_archives.py`按ar header offset解码，
索引规范化为`(symbol, ordinal, member name, occurrence)`，不会合并同名成员或重复符号。
先执行全部225个开发归档，再执行compiler-rt；结果是225/225 PASS、3,864个成员、318,543条索引。

| 新RPM开发归档检查 | 结果 |
| --- | --- |
| 成员数、原序、名称、同名出现序号与本次构建树原件相同 | 225/225 PASS |
| bitcode=0、other=0、非thin；全部x86_64 ELF ET_REL | 225/225 PASS |
| 无DWARF调试节 | 225/225 PASS |
| 完整索引恰为各成员外部定义符号多重集合 | 225/225 PASS，非只比较非空/数量 |
| 每函数一段抽查 | 10个成员PASS，完整节名清单在结果中 |
| Source全库符号缺失 | 强符号0；允许的W类1,920，其余类型0，逐成员记录保留 |

`libarcher_static.a`仍在225个归档中；RPM归属为`llvm-static-devel`与`libomp-devel`，
共有路径内容核对一致。逐档结果及构建树/新RPM原始解析为`E/new-archive-checks/*.json`，
汇总`E/new-archives-result.json`；命令原始输出`U/archive-acceptance.log`。

### 4.2 compiler-rt首档：FAIL并停止

按路径排序检查首档时触发停止：

```text
/usr/lib64/clang/22/lib/linux/libclang_rt.asan-preinit-x86_64.a
members=1
identity_equal=True
payload_sha_equal=False
index_equal=True
index_complete=True
debug_members=0
native=True
member mtime: 1789622773 -> 0
exit_code=1 (AssertionError at verify_new_archives.py:47)
```

成员`asan_preinit.cpp.o`的原始ELF对照（不是归档头部）：

| 项目 | docs/13基线、GNU strip | 本轮新RPM、llvm-strip |
| --- | --- | --- |
| 归档字节数 | 3,748 | 3,680 |
| 归档SHA256 | `4d34b38ca21f9dc0df071c00b6faf535369484f9cedeb91bcc40922ae0eb1af1` | `35bfbc16ca99a8b1a2a48abbeeb75bce07a08d3f1cfb5369cfc6f6be20028b4f` |
| 成员字节数 | 3,536 | 3,464 |
| 成员SHA256 | `e27fcbe560590a857b063fd41e6163ba3ee1453f89f0f3c85393aa41b3ae9506` | `cb1bf7483ba50b5d3c604f84b968219db1c4b2b340906837f47a8cbd6f3dba6b` |
| ELF节数 / 节名字符串表索引 | 11 / 10 | 10 / 1 |
| 字符串表 | `.strtab`、独立`.shstrtab` | 共用`.strtab` |
| `.preinit_array` sh_entsize | 8 | 0 |

停止后仅对这一个失败对象作只读诊断，未继续其他验收实验：新RPM的整档SHA及成员SHA
均与§1离线llvm-strip第一遍输出相同；可分配节的类型、flags、大小及载荷SHA相同，
`readelf -hSWsr`显示节表排序、字符串表、偏移/索引引用和上述entry size变化。
这说明观察到的差异与已实测的两种strip输出一致，**不能据此断言运行语义受损，
也不能凭可分配载荷相同擅自改成语义等价PASS**。用户允许的ar容器字节/时间戳差异不覆盖成员ELF字节差异。
证据：`U/failed-runtime-diagnosis/summary.json`、`{baseline,new,offline_llvm_strip}-archive.json`、
对应`*-readelf.txt`及`readelf.diff`。所有原件保持不变，仅提取成员到诊断目录。

最终状态为`BUILD_PASS_RPM_ACCEPTANCE_FAIL`，并非OOM、构建失败或索引再度损坏。
没有重跑strip、修改Source/spec、放宽门禁或重新构建。

### 4.3 各验收项最终状态

| 用户要求 | 本轮结果及停止边界 |
| --- | --- |
| 225开发归档格式/索引/顺序/分段及符号缺失汇总 | PASS，见§4.1 |
| 45 compiler-rt成员内容、索引、调试信息 | 首档成员内容FAIL；其索引和无调试节PASS；其余44档未继续，不用离线结果冒充新RPM验收 |
| 非归档文件逐字节比较 | 未执行；不得引用docs/30的零差异作为本轮结论 |
| brp链、llvm-strip及转换证据清理 | 已从已完成的构建日志核对PASS，见§3.5；独立brp-strip为基线同样的0次 |
| 七项宿主消费者 | 0次；在运行前已触发停止 |
| Tizen bfd/lld两个测试包及whole-archive诊断 | 0次；未启动 |
| 独立buildroot真实-bi再转换、同树Source SKIP | 0次；未启动，不能宣称续跑幂等闭合 |
| 新RPM clang-22/lld/llvm-ar对基线SHA | 未执行；不宣称工具二进制逐字节不变 |
| tizen_base v2 format-patch与apply --check | 未生成/未执行；完整验收未通过 |

22RPM完整inventory已保存，可供后续审查使用，不将这些RPM标为可发货。
22:09:20确认scope inactive、本项目构建进程0；采样器/log reader已由守护程序回收，
22:09:21锁持有者正常退出并删除自己的锁。17项保护文件检查全部匹配（包含重复核对的S输入与v1补丁）。
证据：`U/final-process-check.json`、`lock-released.json`、`final-protected-files.json`、`task-outcome.json`。

## 5. 提交补丁与结论

尚未生成新format-patch。已验证v1暂保留：
`patches/archive-index-fix/0001-Fix-llvm-static-devel-usability-with-ThinLTO.patch`，
SHA=`0c40c91cb6b896fd93f2712b669eec6771d219268dff7d290539fbb98d0bea58`；
其Source SHA=`2476c5efa061499d7963e0f0976f0c9c86944b688f5bcc48ea40911574af399e`。
本轮验收未通过，因此不覆盖v1；拟提交作者FatTank <hao.lin@samsung.com>，
Change-Id保持`Id4eb147e7ec4764d58a81110cf7bf57d21b64ac8`。
不包含HQ定义或其他项目内容，不推Gerrit。

结论：**最终Source在真实%install完成225档转换，新RPM开发归档验收PASS；
6/6/2、18GiB下本次构建最终产包且无OOM，但HQ llvm-strip叠加未通过compiler-rt成员字节一致性门禁。
v2尚不能作为“完整验收通过”的补丁提交。** 后续需先由用户裁决strip输出差异的验收要求；
本报告不将结构诊断替代批准，也不自行切换strip、另构建或继续剩余测试。
本轮没有运行BOLT/PGO/性能校准，没有构建Chromium，没有推Gerrit；docs/25–33及W/llvm/spec均保持原样。


## 附录 A. 本轮新RPM清单

目录：`Rnew/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/RPMS/x86_64/`。
以下是产物身份备案，不是发货许可；完整绝对路径见`E/rpm-inventory.json`。

| 文件 | 字节数 | SHA256 |
| --- | ---: | --- |
| `clang-22.1.8-1.x86_64.rpm` | 310015218 | `72d929d0c402e84e322b49598de028d4b03531eafc9d30599ebd0fa14c0320d1` |
| `clang-debuginfo-22.1.8-1.x86_64.rpm` | 2928308522 | `d61c178b4597bfe219a9c33023922875f6c07e45cfba705fc01f99a61e8457d2` |
| `clang-devel-22.1.8-1.x86_64.rpm` | 4098506 | `e3dc9227111fcdda6302544a2c0c1bfe7a5bf0cf5dc59a3fb2238c910e9edfab` |
| `clang-devel-debuginfo-22.1.8-1.x86_64.rpm` | 5728786 | `eb659a1e7220fa38aabc3250a1e7b46851af8754dcc30d4c41d5e799b44d0bc8` |
| `compiler-rt-22.1.8-1.x86_64.rpm` | 3787782 | `7d3b2e354db1fb0694db37caa1c5b540e734bbbd89fba30c39560033a155a30d` |
| `compiler-rt-debuginfo-22.1.8-1.x86_64.rpm` | 1288546 | `33f873a058e01c25fc7cc7ed6c752a3fa919aa5bc2cffe782a10520e22f3a2da` |
| `libllvm-22.1.8-1.x86_64.rpm` | 23648166 | `7a486035fb406c18be38ec97da95025456fceecdd7c5cbf3a886bd8ad0cccd68` |
| `libllvm-debuginfo-22.1.8-1.x86_64.rpm` | 198056594 | `0628e4ea9ffc3c1a459c32530042fe103d85257765bb674c585b9127ce63895c` |
| `libomp-22.1.8-1.x86_64.rpm` | 373530 | `47a7e77ad829e165b911c5b337c5ebd174bf4517b501ea7c4afff2d8d19b8efc` |
| `libomp-debuginfo-22.1.8-1.x86_64.rpm` | 1141970 | `5cc9cfae89207fff22ea9d3d6dbbdc43f4ad27ef851b4e26a9f58c2a2429fdc9` |
| `libomp-devel-22.1.8-1.x86_64.rpm` | 25374 | `a69fa7c01af044f743a4dfb7b95503c910738e022fc13f970f0a82fd2770f566` |
| `lldb-22.1.8-1.x86_64.rpm` | 30771798 | `aeb76ff57fa4bc26f89f155c01d8b7b02bab13b60ed78cc5f643d5f96d9cdb22` |
| `lldb-debuginfo-22.1.8-1.x86_64.rpm` | 332845098 | `bf91924b58ca0d6e9b84723d5ec9d74209d31c71c968d3c654090f97d3b7ff54` |
| `lldb-devel-22.1.8-1.x86_64.rpm` | 30523458 | `f2686e8fcde8564c7e0d1da4873d5e8177e86073e76ac97bbb9eaf942e9fd7dc` |
| `lldb-devel-debuginfo-22.1.8-1.x86_64.rpm` | 279580782 | `895a8aca0104946a51e76577aa49f88a49ea241b3789d432e08204de270c21f6` |
| `llvm-22.1.8-1.x86_64.rpm` | 410623270 | `13704f37694b78375f5de8acc54439608e202e9eda5c5d109ad7dd3e3f30728b` |
| `llvm-debuginfo-22.1.8-1.x86_64.rpm` | 3842678322 | `2fade1f9b30190469c0901d4f6460c4fcd458bdf6e5014482d9b0d6a755ebd4f` |
| `llvm-debugsource-22.1.8-1.x86_64.rpm` | 43654026 | `d0593e50a193934b05f1c36aa6d6158cf6af78a69f2f713d708b1a4e9262f9c5` |
| `llvm-devel-22.1.8-1.x86_64.rpm` | 41190278 | `050f80387168dc7559826bb728edf9f8c9e74e948aa4ed65a6fa82bb5fe677f5` |
| `llvm-devel-debuginfo-22.1.8-1.x86_64.rpm` | 308603150 | `12ec44b207e55398a97379e4ea1283574e8785ca6e59ff759d2b6d4bbc041781` |
| `llvm-static-devel-22.1.8-1.x86_64.rpm` | 59587670 | `47e43403381d1a46765440b0d35277a6bf6ec51287242e45abfc5cd929427c9f` |
| `python-clang-22.1.8-1.x86_64.rpm` | 36322 | `6e85f9938579ad8c24a9d1fc58f1a68e9ccc9e7861d8e7e18e03b4bfc772651e` |

## 附录 B. 恢复与停止的原始证据入口

本机完整证据位于`/home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-v2-build-20260929/`；
原始日志、RPM和大JSON不上传GitHub。

| 内容 | 路径（相对E） |
| --- | --- |
| 恢复前SHA、准备源码与MLGO核查 | `resume-20261008/{checkpoint-identities,root-inputs,prepared-source-equivalence,prepared-mlgo-assets}.json` |
| 唯一增量入口及完整argv | `resume-20261008/{resume_once.py,resume-attempt.json,build/commands.log,build/launch.json}` |
| CMake快照、完整日志、time-v、内存/进程/链接采样 | `resume-20261008/build/`；原段保留`full-build/` |
| 两段资源汇总与恢复段转换汇总 | `resume-20261008/combined-build-resources.json`、`build-resource-summary.json` |
| Source完整结果与BEGIN/END原始输出 | `install-conversion-summary.json`、`native-archives-install.log` |
| 22RPM查询/解包完整命令及退出状态 | `extract_new.py`、`rpm-extract.log`、`rpm-extraction-status.json` |
| 新归档验收命令/失败原文 | `verify_new_archives.py`、`resume-20261008/archive-acceptance.log`、`new-archives-result.json` |
| 首个失败成员的只读诊断命令及readelf原文 | `resume-20261008/diagnose_failed_runtime.py`、`resume-20261008/failed-runtime-diagnosis/` |
| 最终停止、保护文件、进程及锁回收 | `resume-20261008/{task-outcome,final-protected-files,final-process-check,lock-released}.json` |

提交前自检：未改W/llvm/spec、docs/25–33；无额外完整构建/消费者包/short-circuit重试；
无BOLT/PGO/校准/Chromium/Gerrit推送。旧v1补丁SHA保持不变；本轮停止条件与未执行项明确登记，
没有将离线通过或结构诊断写成新RPM完整验收通过。
