# 55：夜间入口修复与保留产物重新验证

本地入口缺陷已修复，32 项回归测试通过，T 和 D 的 90 TU 均为 90/90。D 的全部验证经提取器专项修复后通过；T 对旧认证产物的 `.symtab` / `.strtab` 和部分包内容差异超出批准范围，因此整体仍为 FAIL。本地 T 与 QB 1216409 的符号文件按记录节规则通过，两个获批重复日志已删除，按 df 释放约 57.28 GiB。

## 1. 范围与判定

用户明确将此前单独的“补充口径”替换为本完整任务；本轮从头创建 55 号结果。
源码、spec、helper、原 `validation/`、构建根和产品均未改动。只有本地
`tools/bolt/night-launch-20261103/` 修复、`validation-02/` 新证据和第 8 节获批的两个日志删除。
没有 GBS/CMake/Ninja、sudo、装包、LLDB、QB 操作或 Gerrit/sandbox 推送。

证据根：`tools/bolt/results/night-revalidation-20261104/`。
重新验证输出分别是 `W/temp/night-20261103/{toolchain,basedev}/validation-02/`，启动前不存在。
每轮独立 systemd 用户服务，MemoryMax=16G、MemorySwapMax=0；本轮验证另用
CPUQuota=200%、nice10、ionice2/7。先 T 后 D，普通内容失败保留并继续独立检查，
内存错误/OOM 则停止整个队列。

## 2. 本地入口修复与测试

- 日志游标的 `anchor` 保留为 bytes，阶段遍历改用 `phase_anchor`，不再覆盖尾部校验值。
  测试直接 materialize 实际 run.py，抽取其读游标及阶段循环，模拟追加和空轮询：重启计数为 0、复制文件逐字节相同。
  启动演练的结束审计及 `audit_rehearsal.py` 都新增 `log-restarts=0` 与原始/复制日志大小相同断言。本轮没有重做演练或构建。
- 日志只读各根 `gbs-driver/local/repos/*/x86_64/logs/success/llvm-*/log.txt`，
  先拒绝大于 1 GiB 的文件，再逐行计算 SHA、行号、锚点及 FLAGS，不把整份日志读入内存。
- `packages()` 只扫描 `gbs-driver/local/repos`；找不到即失败。认证基线的 products 通过独立显式参数读取，不作新产物的回退路径。
- Python MemoryError 写 `status=stopped reason=memory-stop`；队列也检查验证服务的 `Result=oom-kill`。
  原来的 night 协调器通过修复后的 `critical_stop()` 取得相同停止判断。
- 阶段起止全部取原始 GBS `[NNNNs]`。日志开头 UTC `started "build llvm.spec" at ...` 对齐已有采样的 epoch，分辨率为 1 秒；不使用重复累计日志的观察时间。
- mmap/分块核对大 ELF，避免读入两份普通 clang。所有不许可的节/结构差异明确 FAIL，不跳过整个成员。

测试原文：`test-checks-02.stderr`（15 项）、`test-startup.stderr`（5 项）、
`test-revalidation-05.stderr`（9 项），以及 `test-overlap.stderr`（3 项），合计 32 项通过。9 项回归组包含真实文件的四个比较正反例、
MemoryError 主入口/实际 night 串行队列停止、服务 OOM（断言不启动 D）、原始日志上限、RPM 定位和实际生成轮询代码。
`test-revalidation-05.stderr` 中的 `MemoryError: fixture` 是预期注入，测试最终 `OK`。

D 实测还发现 clang / clang-devel 共同拥有同名头文件，原合并载荷提取器用 xb 再次创建而失败。修复为 SHA 完全相同才复用已有普通文件，拒绝不同内容和符号链接，不覆盖文件。3 个夹具通过；原失败保留，仅在新 release-check-resume 子目录补检被阻断的 release 项，不重跑 90 TU。

首次新夹具把新增字符串长度写错，断言失败；修正夹具后 PASS，旧 stdout/stderr 保留。
真实包复核发现合法 ELF 允许重名节，首次比较器多加了唯一性限制。已移除这项额外限制，仍严格比较每个有序节实例；只重算受影响的 47 个文件，保存 `section-parser-correction/` 和 `rpm23-corrected.json`，不改首轮 `rpm23.json`。修正后仍是 4 包通过、19 包失败。

逐节详细审计首次重复转换字符串表，CPU 开销过大，仅中断该自有诊断进程后缓存字符串表重跑；
没有中断验证服务，见 `section-audit-attempt1.json` 与两轮审计原文。

## 3. 逐节规则及 debuglink 实现

允许内容及长度变化的记录节仅 `.GCC.command.line`、`.llvmcmd`、`.comment`。
`.comment` 每个非空字符串及次数全部列出，非编译器/链接器标识即 FAIL。
`.GCC.command.line` 额外比较字符串多重集合，逐条列出新增、缺失及计数变化，不能把
“物理字节位置变化”说成“字符串排列变化”。

结构只允许记录节的 sh_size、其后非 ALLOC 节的 sh_offset、e_shoff、文件长度及归档成员 size/date。
节数量/顺序/名称/type/flags/address/link/info/alignment/entsize、其余节内容、程序头严格一致；
ALLOC 节的位置、大小、内容不可变。记录节重新布局产生的零对齐填充单列，非节的非零字节严格比较。
归档成员名单和顺序也严格一致；日期差异仅日期字段，大小变化必须伴随通过比较的成员变化。

真实文件副本测试：增加一个合法 linker 标识、增大 `.comment` 并更新必要节偏移 PASS；
改 `.symtab` 一字节 FAIL；改 `.text` 一字节 FAIL；加入非标识 `.comment` 字符串 FAIL。
文件保留在 `W/temp/night-revalidation-20261104-tests-05/`。

T 最终 clang 对认证版的额外例外仅 `.gnu_debuglink` 末尾 CRC32 四字节：
文件名仍为 clang-22.debug，CRC 必须与本次符号文件一致，且符号文件对认证版也必须按上述规则 PASS。
只要符号文件不通过，CRC 例外整体不通过，即使 clang 的其他所有字节相同也不能放行。

## 4. 符号文件逐节实证

### 4.1 本地 T 对认证版

认证符号 SHA：`be17f7222b30b9aff8e9cb30847b7348c5b9897096e382518410dfb053c2f281`。
本地 T：`5960755056a399e66b04ba7583403cc2cf6b907b72b3a984f4836f2ed37885a0`。
**FAIL**，原文：`('non-record section changed', '.symtab')`。

`local-vs-certified-sections.json.gz` 保存所有节的 SHA/位置/大小和全部变化值；
128,748 个符号表项的 st_name 索引变化，25,003 个解析后的名字变化，其他符号字段均相同。
例如 `.str.14.llvm.16961695757791709617` → `.str.14.llvm.10347166305274389687`；
两边 value=14166907、size=21、info=1、other=2、shndx=10。
这是非记录节真实内容差异，不能按本次规则归一化名字或忽略字符串表。
推测这些 `.llvm.<数字>` 后缀与 ThinLTO 模块身份变化相关；本轮没有用源码分析证明成因，不据此放宽门禁。


|节|旧→新位置|旧→新字节数|内容相同|判定|
|---|---|---|---|---|
|.GCC.command.line|2097328 → 2097328|4618930 → 4702918|False|PASS（记录/位置）|
|.symtab|6716264 → 6800248|7244952 → 7244952|False|**FAIL（非记录节）**|
|.shstrtab|13961216 → 14045200|467 → 467|True|PASS（记录/位置）|
|.strtab|13961683 → 14045667|21278996 → 21273042|False|**FAIL（非记录节）**|
|.note.bolt_info|35240679 → 35318709|504 → 504|True|PASS（记录/位置）|

另见 `elf-header-comparison.json`：文件长度 35,243,936 → 35,321,968 B，e_shoff 35,241,184 → 35,319,216；其他 ELF 头字段与程序头完全相同。由于同时存在非许可的符号节变化，这些布局变化不能单独使整文件通过。

GCC 命令记录字符串多重集合相同：`False`；变化字符串 4666 种（全部原文/次数见上述 JSON）。

.comment 全部字符串（旧/新次数）：

|字符串|旧|新|
|---|---|---|
|`GCC: (Tizen GCC 14.2.0 20240801 1.12) 14.2.0`|1|1|
|`GCC: (Tizen GCC 14.2.0 20240801 1.13) 14.2.0`|1|1|
|`GCC: (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0`|1|1|
|`Linker: LLD 22.1.8`|1|1|
|`clang version 22.1.8`|1|1|

### 4.2 本地 T 对 QB 1216409

QB 符号 SHA：`9942e19c75ffef55f2846e6f1ea60651b4502de6e099c038a3d93bad4f5df690`。
**PASS**：仅 `.comment` 内容/长度变化，以及后续 `.GCC.command.line` 的位置和相应零填充。
`.GCC.command.line` 本身的顺序和字节也完全相同，2335 种字符串各一次；没有新增或缺少。
`.symtab` / `.strtab` 内容完全相同。`QB-symbols.json` 与 `local-vs-QB-sections.json.gz` 保存完整证据。

本地 Toolchain 快照为 `tizen-base-toolchain_20261013.024319`，QB1216409 为
`tizen-base-toolchain_20261030.061318`，两者不同，是 `.comment` 中 GCC 标识差异的来源。
Base-Dev 本地/QB 两边相同，都是 `tizen-base-dev_20261030.061217`。


|节|旧→新位置|旧→新字节数|内容相同|判定|
|---|---|---|---|---|
|.comment|2097152 → 2097152|176 → 174|False|PASS（记录/位置）|
|.GCC.command.line|2097328 → 2097326|4702918 → 4702918|True|PASS（记录/位置）|

两者文件长度均 35,321,968 B，e_shoff 均 35,319,216；ELF 头和程序头完全相同，零填充变化单列在 JSON 中。

GCC 命令记录字符串多重集合相同：`True`；变化字符串 0 种（全部原文/次数见上述 JSON）。

.comment 全部字符串（旧/新次数）：

|字符串|旧|新|
|---|---|---|
|`GCC: (Tizen GCC 14.2.0 20240801 1.12) 14.2.0`|1|0|
|`GCC: (Tizen GCC 14.2.0 20240801 1.13) 14.2.0`|1|0|
|`GCC: (Tizen GCC 14.2.0 20240801 1.5) 14.2.0`|0|1|
|`GCC: (Tizen GCC 14.2.0 20240801 1.6) 14.2.0`|0|1|
|`GCC: (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0`|1|1|
|`Linker: LLD 22.1.8`|1|1|
|`clang version 22.1.8`|1|1|

## 5. T 验证

原始日志 18,260,483 B / 25,676 行。锚点、FLAGS、profile、本次 debugfiles 与 debuglink 自洽检查 PASS。
三级身份中 strip-all=13a07cb7…、RUNPATH 后=8c2429d8…与认证值相同；最终=6c63c5c2…对4f08e12d…仅CRC不同，
但匹配符号文件对认证版的严格比较 FAIL，因此第三项整体 FAIL。CRC 原文：旧 `0183e769`，新 `daae351c`，
文件偏移 152529896–152529899；文件名均为 clang-22.debug，其他字节和节布局完全相同，见 `debuglink-component-proof.json`。

23 个包全部尝试比较；重名节解析修正后，**4 PASS / 19 FAIL**。原始 `rpm23.json` 保留，纠正后的归因在 `rpm23-corrected.json`。
表中的“内容变化”包含被允许及被拒绝两类，mtime 不混入该列；“纯日期”要求整个文件只差许可的 ar date 字段。

|包|结论|内容变化文件|拒绝的文件|载荷mtime变化|纯ar日期文件|
|---|---|---:|---:|---:|---:|
|clang / x86_64|FAIL|24|24|66|0|
|clang-debuginfo / x86_64|FAIL|24|13|28|0|
|clang-devel / x86_64|FAIL|1|1|237|0|
|clang-devel-debuginfo / x86_64|FAIL|1|1|4|0|
|compiler-rt / x86_64|FAIL|57|52|105|0|
|compiler-rt-debuginfo / x86_64|PASS|10|0|17|0|
|libllvm / x86_64|FAIL|1|1|3|0|
|libllvm-debuginfo / x86_64|FAIL|1|1|4|0|
|libomp / x86_64|FAIL|3|3|3|0|
|libomp-debuginfo / x86_64|FAIL|3|2|6|0|
|libomp-devel / x86_64|FAIL|1|1|1|0|
|lldb / x86_64|FAIL|5|5|8|0|
|lldb-debuginfo / x86_64|FAIL|5|4|16|0|
|lldb-devel / x86_64|FAIL|3|3|34|0|
|lldb-devel-debuginfo / x86_64|FAIL|3|2|7|0|
|llvm / src|PASS|4|0|17|0|
|llvm / x86_64|FAIL|82|82|98|0|
|llvm-debuginfo / x86_64|FAIL|82|24|85|0|
|llvm-debugsource / x86_64|PASS|0|0|1292|0|
|llvm-devel / x86_64|FAIL|5|5|205|0|
|llvm-devel-debuginfo / x86_64|FAIL|4|1|11|0|
|llvm-static-devel / x86_64|FAIL|225|224|225|0|
|python-clang / x86_64|PASS|0|0|0|0|

具体路径及原错误全部在 `T-rpm-rejected-files.json`。除 `.symtab` / `.strtab`、其他程序的 `.gnu_debuglink` 外，还包括归档索引 `/`、ALLOC 节（如 `.eh_frame`）、`AddLLVM.cmake` 文本和 ompdModule.so 程序头差异。
libomp.so.debug 的 `.comment` 含 `Intel Corporation`（裸厂商名，未标明编译器/链接器）；按本轮严格标识规则拒绝，没有自行把厂商名加入白名单。
这些是“未满足批准的字节比较规则”，并不据此断言构建失败或 clang 已有功能错误。

T 的 90 TU **PASS 90/90**，本次 candidate 对认证 clang 的完整 `.o` 逐字节相同；两次均使用同一路径/同一 inode 的编译器副本和相同 resource-dir、输入及参数。原文 `OBJECT_ROLE_DONE reference`、`OBJECT_ROLE_DONE candidate`、`CHECK_PASS objects90`；逐项 SHA 和完整 argv 见 `toolchain/objects90.json` 及 objects 子目录。

结束原文：`REVALIDATION_PROJECT 已结束 2026-11-04T17:15:13.745399+08:00 toolchain status=failed reason=see-result.json`。总 FAIL 来自文件比较，不是 TU 失败或 OOM。


T profile 原文计数：`{"N": 23592, "M": 144032, "S": 0, "U": 1, "Q": 383, "R": 4.238545331242318e-05, "S_over_N": 0.0}`。FLAGS 原文（已与51号逐字核对）：

```text
TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] CXXFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] LDFLAGS=[]
TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[] CXXFLAGS=[] LDFLAGS=[]
TIZEN_LLVM_FLAGS_WARNING: 0 条
```

T 锚点原文与原始日志行号全部见 `toolchain/anchors.json`，主要条目：

|锚点|原始行号|
|---|---|
|BOLT_NINJA_EXIT_0|23165, 23169, 23283, 23397, 23511|
|BOLT_PIPELINE_PASS|24122|
|BOLT_COMPARE_ROOT_PASS|24128|
|BOLT_CACHE_RELEASE|24130|
|BOLT_POST_GATE_PASS|25192|
|NATIVE_ARCHIVES_END|24601|
|BOLT_DEBUG_SYMBOLS_PASS|24116|
|BOLT_DEBUGLINK_PASS|24118|
|TIZEN_HYBRID_LINK_OK|11326|
|BOLT_REAL_GATE_PASS|24115, 24119, 25189|
|BOLT_PROC_OK|16916|
|BOLT_TOOL_DRY_RUN_BEGIN|22794, 22797, 22801, 22802, 22804|
|BOLT_TOOL_DRY_RUN_END|23149, 23152, 23156, 23157, 23159|
|BOLT_DISK_REPORT|16907, 24113, 24124, 25194|

## 6. D 验证

D 原始日志 18,186,614 B / 25,221 行。锚点、FLAGS、profile 与身份自洽检查通过。
初次 release 合并载荷遇到多个 RPM 共同拥有相同头文件而停止，原错误保留：

```text
FileExistsError: [Errno 17] File exists: '.../validation-02/payload/usr/lib64/clang/22/include/__clang_cuda_builtin_vars.h'
```

只修本地提取器，对已存在普通文件校验 SHA 相同后复用，不覆盖；304 个重叠路径均相同。
随后在独立 16G 服务中只补该子组，输出 `release-check-resume/`，没有重跑 90 TU。
补检结束原文：

```text
RELEASE_RECHECK 已结束 2026-11-04T17:22:20.494500+08:00 status=ok reason=
```

|检查|结果|原文/证据（basedev/release-check-resume/）|
|---|---|---|
|转换成员不带调试节|PASS：3853|native-release.json|
|原样保留原生成员|1975，只计数；45 个全原生归档|native-release.json；不对它们作无调试节断言|
|真实 release C-2 正例|PASS|real-release-c2/result.json；来自 D 的 AArch64AsmParser.cpp.o bitcode|
|真实 release C-2 反例|PASS：按预期拒绝|`release conversion unexpectedly emitted debug sections`|
|产物命令记录无 DROPPED token|PASS：5802 个记录节|no-dropped-records.json|
|MODULE 链接与加载|PASS：ompdModule.so、LLVMgold.so|module-link-and-dlopen.json，两个 `DLOPEN_PASS`|
|helper post|PASS|helper-post-gate.json 原文|
|实际 debuginfo/debugsource 包|0|actual-debuginfo-packages.json=`{}`|

1975 是全 static-devel 的原生成员总数；54号的11只是被转换归档内的混合成员数，不代表全部原生成员。
MODULE 两条链接命令都含 `-Wl,-z,relro,--as-needed -Wl,--gc-sections`，完整展开命令与加载输出均存证。

平台后处理原始日志摘录：

```text
L24564 [ 4029s] + /usr/lib/rpm/find-debuginfo.sh /home/abuild/rpmbuild/BUILD/llvm-22.1.8
L24565 [ 4030s] WARNING: /usr/bin/clang-22 is already stripped!
```

D profile：`N=23592 M=144032 S=23 U=1 Q=383 R=0.0010172508794981563 S_over_N=0.0009749067480501865`。
这里 R 是比值，换算百分比为 0.10172508795%；保留 release 的实际统计，不借用 T 的 S=0。

FLAGS 原文（L627/L629，与51号逐字相同）：

```text
TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] CXXFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] LDFLAGS=[]
TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] CXXFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] LDFLAGS=[]
TIZEN_LLVM_FLAGS_WARNING: 0 条
```

D 的 90 TU **PASS 90/90**，最终 clang 对本地 T 的完整目标文件逐字节相同；`objects90.json` 和每次 argv/SHA 均保留。这是同一次串行验证，未重启。

主服务结束原文：`REVALIDATION_PROJECT 已结束 2026-11-04T17:39:41.146353+08:00 basedev status=failed reason=see-result.json`。该原始 failed 保留初次提取器错误；把已通过的 release 专项补检合入 `result-effective.json` 后，D 的 anchors/flags/profile/identity-chain/release/objects90 六项均 PASS，不改写原 `result.json`。
D 产出 12 个二进制包加 1 个源码包，T 为 22+1；D 没有新增包，缺少 T 的十个调试包：
clang-debuginfo、clang-devel-debuginfo、compiler-rt-debuginfo、libllvm-debuginfo、
libomp-debuginfo、lldb-debuginfo、lldb-devel-debuginfo、llvm-debuginfo、llvm-debugsource、llvm-devel-debuginfo。
`T-D-package-file-differences.json` 列出全部文件清单及元数据差异；该表中的 different_files 也包括 mtime，不能把它直接当成内容差异数。


## 7. 原始 GBS 时间重算资源表

仅使用本次夜间留下的采样，不补造缺失。cgroup 内存包含文件缓存；分阶段是采样的
memory.current 最大值，不冒充独立阶段 memory.peak。原始采样仅跟踪 llvm-bolt 的 VmHWM，
所以其他阶段的全进程最大 VmHWM 为 UNKNOWN。单秒以内边界无法再细化。


构建当时两根均为源码 `9e39fa8a…`，MemoryMax=24,482,979,840 B（MemTotal−8 GiB）、MemorySwapMax=0、CPUQuota=1200%、nice10、ionice2/7；GBS threads30、jobs8、_smp_mflags -j8、_costomized_smp_mflags -j20，普通 Ninja 按 spec 为 -j6。这些是原构建条件，本轮没有启动构建；重新验证服务的16G上限另见第1节。

### toolchain

|Phase|Seconds|Cgroup sampled bytes (includes cache)|llvm-bolt VmHWM bytes|Root du sampled bytes|Filesystem min available bytes|
|---|---|---|---|---|---|
|ordinary-build|7322.0|19146416128|UNKNOWN|47920926720|196361015296|
|ordinary-install|328.0|14991839232|UNKNOWN|60357607424|182599786496|
|BOLT|1469.0|16283660288|9931661312|70485561344|163517423616|
|cache-release|9.0|3716710400|UNKNOWN|UNKNOWN|163959148544|
|archive-conversion|2544.0|10596343808|UNKNOWN|55093010432|160152088576|
|platform-post|700.0|7375040512|UNKNOWN|47143387136|162207100928|
|packaging|292.0|10014306304|UNKNOWN|42598031360|163214110720|

构建服务 lifetime memory.peak（含文件缓存）：19148963840 B。

### basedev

|Phase|Seconds|Cgroup sampled bytes (includes cache)|llvm-bolt VmHWM bytes|Root du sampled bytes|Filesystem min available bytes|
|---|---|---|---|---|---|
|ordinary-build|2266.0|11202809856|UNKNOWN|10894733312|157159854080|
|ordinary-install|7.0|8221478912|UNKNOWN|11666124800|155975380992|
|BOLT|216.0|14474072064|9931550720|14148202496|152322973696|
|cache-release|1.0|UNKNOWN|UNKNOWN|UNKNOWN|UNKNOWN|
|archive-conversion|1285.0|4375175168|UNKNOWN|13821210624|141622312960|
|platform-post|49.0|3521880064|UNKNOWN|12963184640|141829160960|
|packaging|85.0|6626312192|UNKNOWN|13444767744|140572217344|

构建服务 lifetime memory.peak（含文件缓存）：14714576896 B。

## 8. 两个重复日志删除记录

仅删除用户批准的 `toolchain/evidence/rpm-build.log`、`basedev/evidence/rpm-build.log`。
`deletion.json` 保存大小、头尾各 1 MiB SHA、restarts 计数、原始日志和 54 号 gzip 解压后的
SHA/字节数/行数核对、lsof/fuser 原文、普通用户 `rm -- <精确路径>` 及每次 df。
所有 lsof/fuser 均 exit1、stdout/stderr 为空。没有删除旧 validation、构建根或任何其他文件。


|项目|重复日志字节|重启条数|原始日志字节/行|df释放字节|结果|
|---|---|---|---|---|---|
|toolchain|46429749465|6242|18260483 / 25676|46429507584|deleted|
|basedev|15076896925|2051|18186614 / 25221|15076913152|deleted|

两次 df 差值合计 61506420736 B（57.282 GiB）；删除后可用 189519749120 B（176.504 GiB）。后续验证写入副本会使当前可用空间下降，最终 df 另列。

最终证据收集后的 `/home`：

```text
Filesystem         1B-blocks          Used    Available Use% Mounted on
/dev/sda1      1967844950016 1703043465216 164764872704  92% /home
```

## 9. 最终结论与证据

最终判定：**T FAIL，D PASS（包括明确记录的提取器专项补检），整体未全部通过**。
T 的 23 包为 4 PASS / 19 FAIL；T/D 两组 90 TU 均 PASS。符号文件本地对认证版 FAIL，
本地对 QB1216409 PASS。没有把“生成目标文件相同”替代严格的二进制产物比较。

验证服务内存峰值（含缓存）：T 4,646,178,816 B，D 3,252,428,800 B；
D 专项补检 2,609,270,784 B。D 补检与同项目 TU 有时间重叠，联合采样最大
3,625,762,816 B；T/D 项目验证始终串行。所有 memory.events 的 oom/oom_kill 均0。
结束后四个服务的 MainPID=0、ControlGroup 为空，原始查询在 `ended-service-checks.json`；
两个主服务保留 failed 状态表示检查返回1，并非仍在运行，未 reset-failed 或杀外部进程。

`validation-provenance.json` 列出每份上传证据的来源、字节数及 SHA；大于1MiB的文本用gzip，
本地未压缩原件保留。`effective-results.json` 和各根 `result-effective.json` 单独汇总更正，
原始 failure.txt、result.json 和服务日志不改。资源表全文来自原始GBS时间，不沿用错误阶段时间。
源码 HEAD 仍为9e39fa8a…、已跟踪工作树无改动，见 `source-final-check.json`。

最终日志原文：

```text
REVALIDATION_EFFECTIVE 已结束 2026-11-04T17:40:08.130997+08:00 status=failed reason=T-strict-file-differences;D-release-targeted-check-applied
```

结论：入口与验证工作已完成，但 T 产物不满足本轮批准的严格比较口径，保留现场，等待用户裁决。
