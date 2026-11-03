# 53：夜间 T / D 完整构建的白天准备

两个新入口演练通过，T 的认证产物自测（23包、90/90 TU）通过，今晚可以启动。D 的验证逻辑已用正反夹具通过，真实 release 产物仍须夜间验证。两完整根尚未创建，空间规划余量约69.7GiB。

本轮只准备和演练，没有启动 full 或 night；源码仍为 `9e39fa8a61392652bb28b75fc26216675bcad1d5`，tree `cbc33271f8a9a7a5bd4de3c806bed6182c268e98`，未修改源码、spec、helper、历史根和历史入口。证据目录：[night-prep-20261103](../../tools/bolt/results/night-prep-20261103/)。本轮源码身份沿用51号，不重复构建或推送 sandbox。

## 1. 入口与隔离

新入口：[night-launch-20261103](../../tools/bolt/night-launch-20261103/README.md)。模板为 `final-launch-20261103/launcher.py`，SHA256 `43f25064710a0dd82d48a1042567ab34fa43d138f9257edbca25669514dc57df`；底层 run/prep/build-runner、导出 argv、两个配置及 build.conf 的路径和 SHA、修改清单全部在 [provenance.json](../../tools/bolt/night-launch-20261103/provenance.json)。仍用已经跑通的 gbs-driver：driver 的 BUILD-ROOTS 指向本次物理新根。

|项目|Toolchain（T）|Base-Dev（D）|
|---|---|---|
|模式|debug|release|
|快照|tizen-base-toolchain_20261013.024319|tizen-base-dev_20261030.061217|
|build.conf SHA|e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945|8ace286a5f98f2e02a79be275a64c22a86ea2b0034174c1e293381e181ce3f6a|
|完整根（本轮未创建）|W/temp/night-20261103/toolchain|W/temp/night-20261103/basedev|
|演练根（保留）|W/temp/night-20261103/rehearsal/toolchain|W/temp/night-20261103/rehearsal/basedev|

参数保持 `jobs 8`、`_smp_mflags -j8`、`_costomized_smp_mflags -j20`、外层 `--threads=30`。spec 内 Ninja 为 `-j6`，CMake compile pool=6/link pool=2；工具构建并发沿用源码。MemoryMax=MemTotal−8GiB，MemorySwapMax=0，CPUQuota=1200%，nice10，ionice class2/priority7，OOMPolicy=stop。实际 argv 与上限在各根 plan.json、service-command.json 中。所有资源规则仅在本地驱动。

入口要求显式40位源码 SHA，启动及工作开始时检查 HEAD 和已跟踪文件；未跟踪文件忽略。每个目标根已存在就拒绝，不复用旧根。T 完成构建、验证和清理后才启动 D；普通构建/验证失败不阻止 D，磁盘不足、OOM、残留进程、残留挂载、清理无法确认时停止串行队列。T 没有产出候选时，D 仍可构建，但其 D/T 90 TU 会明确失败，不能写成通过。配置/源码身份在 D 启动前再次核对。

每个项目在 controller.stdout 写 `NIGHT_PROJECT 已结束 <ISO+时区> status=... reason=...`；整体在 night.log 写 `NIGHT 已结束 ...`。协调器每60秒写项目、服务状态和包日志末行；结果另写 JSON。最终审计或资源整理异常也会记录结束状态。OOM 导致子控制器不能自行写结束行时，由仍在运行的串行协调器记录；机器掉电/SIGKILL 整个协调器的情况不能由进程自身保证写入。

## 2. 验证清单与判定方法

### T：debug

|验证项|预期值和判定方法|
|---|---|
|保全基线|先逐项核对 full-20261030/products/SHA256SUMS；只读|
|strip-all SHA|13a07cb7f84bd1ceda4d851c8bd71bddf7ef0c2d4864892eba64cbbb9a0350b8|
|RUNPATH 后 SHA|8c2429d870f421a29a9914458bc4d4ff2ce359a15e0bdd20f39bfb4580c40bdf|
|最终 SHA|4f08e12d499ebd492ce4951f74915ba435f57f2e380dc6f3520f24644996cb17；实际文件同时等于 identity.after_sha256|
|profile|N=23592、M=144032、S=0、U=1、Q=383；R=0.00004238545331242318（比例，0.004238545331242318%），S/N=0；整个 counts JSON 与认证值相同|
|身份链|prestrip 实物 SHA、ordinary、符号文件、install-state、post-result、实际 RUNPATH=$ORIGIN/../lib64；无 RPATH；tool-plan/verify 的 planned=executed=plan.tasks|
|BOLT 锚点|NINJA_EXIT_0、PIPELINE、DEBUG_SYMBOLS、DEBUGLINK、至少三处 REAL、COMPARE_ROOT、CACHE_RELEASE、POST、NATIVE_ARCHIVES_END；原文/行号保留；PROC、dry-run BEGIN/END、四次 DISK_REPORT 同步采集|
|新参数/混合链接|HYBRID_LINK_OK；NORMALIZED/DROPPED 原文；T 的 DROPPED 三组为空，WARNING=0；演练另外与51号实测 C/CXX/链接参数逐字节比|
|23包|包集合/文件集合一致；mode/uid/gid/符号链接目标一致；载荷 mtime 单列；内容按下述严格字节规则；源码变更必须等于本次 pinned export 的实物，逐项列出|
|debugfile|debugfiles.list 含 clang-22.debug；RPM 中该文件 SHA=identity；candidate .gnu_debuglink 文件名、CRC 与 debug 文件和 identity 一致|
|90 TU|30 TU×三目标；输入 SHA 复核；认证 candidate 和本次 candidate 使用同一可执行路径/同一 inode、同一输入及输出路径、同一 resource-dir/运行库；完整 .o 字节相等|

SHA 不同不自动放宽：仅 `.GCC.command.line` / `.llvmcmd` 的差异可进入命令记录证明；记录每个变化范围的文件偏移、节内偏移、长度和 old/new hex，验证节外全部字节相同，布局和文件长度也相同。不整节跳过、不整成员跳过。若 identity 的 strip-all/RUNPATH SHA 不同且已被流水线覆盖、没有该阶段原件，脚本直接 FAIL“stage bytes unavailable”，不从最终文件反推不存在的证据。最终候选、ordinary、debug 文件及归档成员都有实际字节可比。

ar 日期规则仍为三条件同时满足：成员名单和顺序相同、每成员内容 SHA 相同、所有差异只在成员头16起12字节 date 字段。只差日期单列，不能叫内容相同；命令记录差异另分类，仍逐字节验证成员其他内容和非日期头。任何其他差异 FAIL。

### D：release

|验证项|预期值和判定方法；真实结果留待夜间|
|---|---|
|参数|C/CXX 的 DROPPED 各为 `-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4`，LD 空，WARNING=0；保存 NORMALIZED 原文|
|BOLT/profile|生产门禁保持；保存 pipeline counts 和重写原文（匹配数、比例），不要求和 T 的布局计数相同|
|release/debug产物|identity 不含 debug_file/debuglink；候选无 .gnu_debuglink；收集 find-debuginfo 及 clang-22 附近日志；记录真实 debuginfo/debugsource RPM 名单和载荷，不凭模式名猜内容|
|static-devel|读取本轮 Source1005 summary 225 项；只对 converted 成员断言无 .debug*/.zdebug*，同时 SHA 与转换记录一致；原样保留 native 成员只计数，skipped 归档计数单列|
|真实 C-2 #5/#6|从 D/build/lib64 中前转换 bitcode 成员取真实 recorded command，用本提交 Source1005 debug_info=no 转换；正例无调试节；其新副本注入 DICompileUnit/DISubprogram/DILocation 后必须拒绝。源成员及负例全部保留，标清真实来源|
|命令记录|扫描实际 RPM 的 ELF/归档成员 .GCC.command.line/.llvmcmd，完整 token 匹配，四个 DROPPED 均不得存在|
|MODULE|离线解析 build.ninja/rules.ninja 的 MODULE_LIBRARY_LINKER 规则（不运行 ninja）；匹配已打包文件，核对 module linker flags；用本轮运行库和 loader、RPM 原字节做 RTLD_NOW dlopen；soname 链接在新 scratch 内复原|
|post|保存 helper post gate JSON 原文并核对布尔结论|
|90 TU|同 T 方法，D vs T candidate 完整 .o 比较，90/90；没有 T 候选就不能通过|
|包对照|列 T/D 各自 RPM、额外/缺失包以及共享包文件集合/属性/内容差异，只作对照记录|

所有验证输出位于新根 validation，认证根只读。装包、LLDB、sudo 图形认证留到明早，不自动执行。

## 3. 白天自测

认证 T 自测第二次执行 `status=ok`，23/23 包通过、90/90 完整目标文件逐字节相同；结束原文：`VALIDATION 已结束 2026-11-03T22:19:03.391578+08:00 status=ok`。证据：[selftest-certified-02/result.json](../../tools/bolt/results/night-prep-20261103/selftest-certified-02/result.json)、[objects90.json](../../tools/bolt/results/night-prep-20261103/selftest-certified-02/objects90.json)、[原始stdout](../../tools/bolt/results/night-prep-20261103/certified-selftest-02.stdout)。额外身份链复核也 PASS，见 selftest-identity-extra。历史日志没有新提交的 FLAGS/HYBRID 标记，这一项明确为历史自测不适用；不是豁免今晚检查，新逻辑已用51号原文及本轮两个真实演练单独通过。

`test_checks.py` 14项、`test_startup.py` 5项全部 PASS；[unit-final-04.stderr](../../tools/bolt/results/night-prep-20261103/unit-final-04.stderr)、[startup-final-03.stderr](../../tools/bolt/results/night-prep-20261103/startup-final-03.stderr) 是测试原文。集成负例8项 PASS（真实 clang 新副本翻转 .text 的一个字节、DROPPED 注入、MODULE 解析、dlopen 正反、普通失败/磁盘/OOM 串行策略），见 [integration.json](../../tools/bolt/results/night-prep-20261103/integration.json)。正常失败允许 D；磁盘/OOM/残留拒绝 D。

RPM 提取实测：认证 clang RPM 中340个正大小普通文件，包含 cpio 硬链接别名，提取后全部 SHA 等于 manifest；绝对 soname 链接转成 scratch 内相对链接，见 rpm-extract-selftest.json。MODULE 在认证图中识别12个目标（保留 Ninja 转义后的 `$ORIGIN`，不会再次按变量清空），并在新测试进程中实际 dlopen 保留的 LLVMgold.so 和已打包的 ompdModule.so 成功；不执行历史根里的 CMake/Ninja。

D 尚无真实 release 构建产物。白天 C-2 使用51号保留的合成 release bitcode，explicit 导入本提交 Source1005，正例 CONVERTED、负例拒绝 `release conversion unexpectedly emitted debug sections`，2/2 PASS，见 c2-fixtures-03/real-release-c2/result.json。真实 D 成员、RPM 无 DROPPED、打包 MODULE 和 D/T 90 TU 只能等夜间，未标为已实测。

准备错误均保留：首次 T 自测把 source RPM 的 ARCH=x86_64 当成二进制 key，造成 duplicate llvm；改为按 `.src.rpm` 标识 src 后复测。首次 MODULE 方法测试从历史已清空 BUILDROOT 查文件失败，随后改为读取保留的 build/lib64/LLVMgold.so 做方法测试，真实夜间仍用 RPM 字节。C-2 最初仅注入 CU 被后端优化掉，负例未触发；补充附着于真实函数的 subprogram/return location 后正确拒绝。对应 *stderr 和各新 scratch 原件均保留，不隐藏首次失败。本轮没有生产门禁失败，也没有修改生产代码。

## 4. 两次真实演练

新入口按 T→D 串行真实运行；看到 `+ cmake -G Ninja` 后正常停止服务，不运行 Ninja、不完成 CMake 配置。各根保留。以下参数与51号§5的审计 JSON逐字节相同，包括空格；WARNING 均0。原始完整日志、导出/服务argv、plan、cleanup、final-audit、资源采样在 [rehearsal/](../../tools/bolt/results/night-prep-20261103/rehearsal/)。

### toolchain

状态 `ok`，原因 `rehearsal-complete-at-CMake`，控制器总耗时 434.660 秒。

```text
L659: [  255s] TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] CXXFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] LDFLAGS=[]
L661: [  255s] TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[] CXXFLAGS=[] LDFLAGS=[]
```

CMake 实收和环境 LDFLAGS（完整值）：

```text
CMAKE_C_FLAGS= -ffunction-sections -fdata-sections  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument   -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables  -g -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument
CMAKE_CXX_FLAGS= -ffunction-sections -fdata-sections  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument   -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables  -g -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument
CMAKE_EXE_LINKER_FLAGS=-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections
CMAKE_SHARED_LINKER_FLAGS=-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections
LDFLAGS=-Wl,-z,relro,--as-needed -Wl,--gc-sections
```

### basedev

状态 `ok`，原因 `rehearsal-complete-at-CMake`，控制器总耗时 424.755 秒。

```text
L627: [  259s] TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] CXXFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] LDFLAGS=[]
L629: [  259s] TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] CXXFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] LDFLAGS=[]
```

CMake 实收和环境 LDFLAGS（完整值）：

```text
CMAKE_C_FLAGS= -ffunction-sections -fdata-sections  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument    -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables   -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument
CMAKE_CXX_FLAGS= -ffunction-sections -fdata-sections  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument    -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables   -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument
CMAKE_EXE_LINKER_FLAGS=-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections
CMAKE_SHARED_LINKER_FLAGS=-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections
LDFLAGS=-Wl,-z,relro,--as-needed -Wl,--gc-sections
```

清理核对命令：`systemctl --user show <本轮prep/build/controller单元> -p Id -p ActiveState -p SubState -p Result`；`findmnt -rn -o TARGET,SOURCE,FSTYPE` 按本轮根筛选；遍历 `/proc/*/cgroup` 对本轮 prep/build 单元确认进程为空。两边 `final-audit.json` 均为 mounts.stdout=""、remaining_build_processes=[]；prep/build/controller 都 inactive/dead，Result=success。原文见 services-after-rehearsal.txt、每根 final-audit.json。只正常卸载本次新根，不懒卸载、不杀外部进程。

演练后仅补强本地验证器和结束日志：RPM硬链接/库符号链接提取、负例DI注入、最终审计异常也输出已结束行；没有改变已演练的导出、准备、GBS/CMake参数、资源限制或 CMake 停止条件。相关单元/静态物化检查重跑，生成 run/prep/build-runner 可以通过 Python语法检查；POSIX入口 `/bin/sh -n` 通过。

## 5. 资源记录与空间

每次构建独立产生 evidence/resources.jsonl、du-root.jsonl、bolt-process.jsonl、phase-events.jsonl，结束产生 resource-table.json 和 .md。阶段为 ordinary-build、ordinary-install、BOLT（begin至compare-root）、cache-release、archive-conversion、platform-post、packaging。阶段时间来自实时日志观察的宿主时钟，并保留包日志原文；有2秒轮询精度，不伪称内部精确耗时。日志截断/重开保留原有检测。

整次 cgroup memory.peak 含文件缓存；分阶段列 memory.current 采样最大值，不能用累计 peak 冒充独立峰值。llvm-bolt 记录 VmRSS/VmHWM；du约60秒一次，超时缺失；df约2秒记录最低值。没有锚点或采样的阶段写 UNKNOWN，不拿历史值补齐。演练只到 CMake，BOLT/打包等资源为 UNKNOWN，不是0。

演练后的空间估算继续使用51号§9.6的历史实测下界；不把release预计更小当作可扣减量。

|项目|字节|GiB|
|---|---:|---:|
|两根历史峰值|136,504,475,648|127.130|
|两根外部开销|3,251,683,328|3.028|
|本地运行保留量|21,474,836,480|20.000|
|参考需求|161,230,995,456|150.158|
|两根峰值20%规划余量|27,300,895,130|25.426|
|建议总量|188,531,890,586|175.584|
|当前/home可用|263,345,737,728|245.260|
|建议量外余量|74,813,847,142|69.676|
|需释放|0|0.000|

采样时间 `2026-11-03T22:16:19.576463+08:00`。原文 [df-after-rehearsal.txt](../../tools/bolt/results/night-prep-20261103/df-after-rehearsal.txt)，公式输入 [space-after-rehearsal.json](../../tools/bolt/results/night-prep-20261103/space-after-rehearsal.json)。历史峰值68,252,237,824B是采样下界，20%只是本地规划余量，不保证未知的瞬时峰值。此时空间足够上述规划，不需要删除；运行中仍保留20GiB停止条件。

## 6. 今晚启动命令（本轮仅写出，没有执行）

```sh
/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/night-launch-20261103/launch.sh 9e39fa8a61392652bb28b75fc26216675bcad1d5 night
```

前台最后单独打印：

```sh
tail -f /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261103/night.log
```

具体包输出在对应根 `evidence/rpm-build.log`；每根结果 `evidence/result.json`、`validation/result.json`，整体 `night-result.json`。任务已结束时读取带时区的“已结束”行，不能把服务退出或旧日志末行当成验证通过。两完整根仍不存在，所有白天产物和演练根保留。

结论：**白天准备、自测与两次演练通过，今晚可以启动；本轮没有运行完整构建。**
