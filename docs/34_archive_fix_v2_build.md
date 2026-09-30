# 34 归档修复 v2：llvm-strip 叠加验证与构建暂停备案

本轮起点：`66c5671626ad3858131bab70115f25bb45ec9578`。开始时间：2026-09-29 22:46:29 +08:00。
docs/25–33 保持不动。本文与 STATUS 同一提交更新；不推 Gerrit。

> **2026-09-30 用户要求节前暂停，当前为 PAUSED_BY_USER。** 离线门禁及CMake门禁通过；唯一一次完整构建完成7530/7634项后按用户请求停止，已释放内存并保留磁盘现场。没有OOM，不判构建失败，也没有完整构建/RPM验收PASS。节后等待用户明确恢复；v1补丁不变，尚未生成可提交v2补丁。

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
**不自动启动第二次完整构建，不自动改6/6/2或18GiB；等待用户明确恢复。**
剩余顺序：完成本次构建→新RPM全部门禁→七项宿主消费者→两个Tizen测试包→独立%install再转换和同树Source SKIP→提交补丁。

## 4. 新RPM验收

因用户暂停尚未执行，不将离线检查记成新RPM验收。特别是§1.3的GNU/LLVM strip成员ELF差异，
后续必须按用户要求逐项验收、记录，不能在运行后改成宽松门禁。

## 5. 提交补丁与结论

尚未生成新format-patch。已验证v1暂保留：
`patches/archive-index-fix/0001-Fix-llvm-static-devel-usability-with-ThinLTO.patch`，
SHA=`0c40c91cb6b896fd93f2712b669eec6771d219268dff7d290539fbb98d0bea58`；
其Source SHA=`2476c5efa061499d7963e0f0976f0c9c86944b688f5bcc48ea40911574af399e`。
只有本轮完整验收成功才覆盖v1；拟提交作者FatTank <hao.lin@samsung.com>，
Change-Id保持`Id4eb147e7ec4764d58a81110cf7bf57d21b64ac8`。
不包含HQ定义或其他项目内容，不推Gerrit。

本提交发布的是离线证据与暂停备案。完整构建、6/6/2容量认证、llvm-strip叠加后的新RPM验收及v2可提交性仍未闭合。
本轮没有运行BOLT/PGO/性能校准，没有构建Chromium，没有推Gerrit；docs/25–33及W/llvm/spec均保持原样。
