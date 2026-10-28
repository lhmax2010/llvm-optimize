# 42：BOLT clang 崩溃定位根因与临时方案实测

LLVM objcopy 的崩溃是 `--only-keep-debug` 保留了后置 PT_PHDR 的旧偏移，却向缩小后的输出缓冲区写入它；两代 BOLT 产物都复现，未发现原始 BOLT ELF 的 LOAD、节范围或对齐损坏，并非 `-use-old-text` 特有问题。
平台会收集我们预置的 `/usr/lib/debug/usr/bin/clang-22.debug`，现有自动拆分规则把它对应到 clang-debuginfo；这是脚本/宏/文件归属的静态核实，本轮没有生成新 RPM。
方案甲已实测自动显示函数名：符号文件 33,147,264 字节，GNU 分离耗时 0.21 秒、峰值 RSS 100,456 KiB，clang 增加 104 字节且 15/15 对象一致；方案乙缺少带 DWARF 的重链输入，依照授权跳过，源码行、耗时、内存和大小均未实证。

## 1. 范围、身份与结果边界

- 只读输入：39 号 f308fe08eeaad4e219f8505449b88bd5f644ea8c 产物；37 号未用 old-text 的 BOLT 输出；39 ordinary。源码未改、未构建软件包、未推 Gerrit/sandbox。
- 所有实验副本在 `temp/crash-fix-probe-20261028/`；已有根和 products 未改写。源码工作树末次 `git status --porcelain` 为空。[input-recheck.json](../../tools/bolt/results/crash-fix-probe-20261028/input-recheck.json) 证明三份输入 SHA 前后相同。
- 已闭合：objcopy 崩溃根因、可用符号分离工具、外置符号的自动调试器加载、显式离线解析、debuglink 的代码不变及 15 TU 对比。
- 未闭合：发布 spec/helper 的实现、真实 clang-debuginfo RPM 验收、DWARF 源码行方案。**当前已发布 RPM 仍没有 clang-22.debug**；不能把本轮临时实验说成发布修复已落地。
- 普通工具探测/编译均单任务；长一些的脚本运行在 user systemd service，CPUQuota=100%、MemoryMax=3–6 GiB、swap=0、nice19、idle I/O。没有执行方案乙的大内存 BOLT 重写。单次时间/RSS来自 `/usr/bin/time -v`，不是整包构建增量承诺。

| 输入 | 大小 B | SHA256 |
|---|---:|---|
| bolt39 | 185,676,288 | `de2ae6e3ed1040505151c9b88b66ef1b6383f51058e6535d0a107287a1658e9d` |
| bolt37 | 218,890,224 | `bff9cd119d9323e8ccb1345ef35f2afde521b034e676f03a6a8b6bb8d5fbc425` |
| ordinary | 1,793,485,376 | `d5090159915657b235b96f1202c058e1efd1647d6a2225ac8fdb2906aeaa501d` |

最终发布 clang 为 152,532,296 B，SHA `8c2429d870f421a29a9914458bc4d4ff2ce359a15e0bdd20f39bfb4580c40bdf`。三种输入均无 `.note.gnu.build-id`，不能依靠它关联调试文件。使用 `.gnu_debuglink` 的文件名和 CRC32；无需伪造 build-id。

## 2. 工具矩阵

完整 argv、退出码、耗时和 stdout/stderr：[matrix.json](../../tools/bolt/results/crash-fix-probe-20261028/matrix.json)、[matrix 目录](../../tools/bolt/results/crash-fix-probe-20261028/matrix/)。输入没有就地操作：strip 用 `-o`，eu-strip 同时给 `-f debug` 和 `-o stripped`，debuglink 用独立输出参数。

| 输入 | LLVM only-keep-debug | GNU only-keep-debug | eu-strip -f/-o | LLVM strip-all | LLVM add-gnu-debuglink |
|---|---|---|---|---|---|
| bolt39 | SIGSEGV (-11)，2.721s | 成功 (0)，0.268s | 成功 (0)，1.469s | 成功 (0)，0.416s | 成功 (0)，0.517s |
| bolt37 | SIGSEGV (-11)，1.395s | 成功 (0)，0.266s | 成功 (0)，1.670s | 成功 (0)，0.316s | 成功 (0)，0.467s |
| ordinary | 成功 (0)，7.887s | 成功 (0)，18.424s | 成功 (0)，14.446s | 成功 (0)，2.592s | 成功 (0)，20.924s |

工具版本：LLVM 22.1.8；宿主 GNU binutils 2.42；平台 eu-strip 0.189。另用平台 GNU objcopy 2.43复测 39 输入成功，输出与宿主 GNU 文件相同（[platform-gnu-result.json](../../tools/bolt/results/crash-fix-probe-20261028/platform-gnu-result.json)）。

GNU 两次 BOLT `only-keep-debug` **rc=0 但有 warning**，不可隐藏：[gnu-keep-warnings.txt](../../tools/bolt/results/crash-fix-probe-20261028/gnu-keep-warnings.txt) 收录全部原文。39 包括：

```text
section `.note.ABI-tag' can't be allocated in segment 0
section .eh_frame lma 0x8600380 adjusted to 0x87ffd1c
section `.eh_frame_hdr' can't be allocated in segment 4
```

这些消息指向生成的 **debug 文件**：only-keep-debug 把加载节变成 NOBITS，其段映射不再用于执行；不能反推原输入损坏，也不能把该 debug 文件当可执行程序。GNU 文件已通过 LLDB 自动加载和显式 symbolizer 24/24 地址验证。eu-strip 无上述 warning，是另一个可用分离工具；其 debug 文件 35,243,760 B，显式 symbolizer 同样24/24，但本轮完整 debuglink+15TU+chroot验收选用 GNU 文件。

## 3. 原始 ELF 结构审计

原文：[elf/bolt39-gnu.stdout](../../tools/bolt/results/crash-fix-probe-20261028/elf/bolt39-gnu.stdout)、[elf/bolt39-llvm.stdout](../../tools/bolt/results/crash-fix-probe-20261028/elf/bolt39-llvm.stdout)，其余两输入同目录。两种 readelf 对三份输入的 stderr 全为空，未见 warning。程序化文件/内存范围核对：[elf-structures.json](../../tools/bolt/results/crash-fix-probe-20261028/elf-structures.json)、[elf-containment.json](../../tools/bolt/results/crash-fix-probe-20261028/elf-containment.json)。

- 三输入的各个 PT_LOAD 均 `filesz <= memsz`、文件范围有效、offset/vaddr 对 p_align 同余；没有零大小 PT_LOAD。
- 不同 LOAD 的实际文件范围、内存范围均无重叠；每个非空 ALLOC/非 NOBITS 节均完整落在同一个 LOAD 的文件范围和内存范围内，且相对偏移一致；无跨 LOAD 边界的节。
- `.symtab/.strtab/.comment/.GCC.command.line/.note.bolt_info` 等非 ALLOC 节在 LOAD 外是正常的；TLS/NOBITS 不要求占文件内容。PT_DYNAMIC、GNU_RELRO、TLS 等和 LOAD 的包含关系也是正常现象，不能把它们算“错误段重叠”。GNU_STACK 大小0不等于零大小LOAD。
- 39 的程序头表在文件偏移 **140,509,184 (`0x8600000`)**，13×56=728 B；PT_PHDR 本身被新增 LOAD 完整覆盖。37 的 PT_PHDR也是同一偏移/长度。普通文件程序头表在64 B。
- 39节头表位置185,673,536、43项×64=2,752 B，正好到文件末尾185,676,288。各输入的全部段/节和对齐数值见JSON与readelf原文。

结论限定于这些检查：没有发现 BOLT 可执行文件的结构违规。它使用合法但非典型的“后置程序头表”；LLVM objcopy 对这种布局的 only-keep-debug 处理有缺陷。

## 4. writeSegmentData 根因：精确到段和越界范围

本轮没有重新构建 LLVM。宿主 GDB 调试根内现有 llvm-objcopy+libLLVM，通过动态符号和反汇编定位；没有需要手动加载完整 DWARF。[objcopy-gdb.stdout](../../tools/bolt/results/crash-fix-probe-20261028/objcopy-gdb.stdout) 保存栈/寄存器/汇编，[objcopy-gdb-detail.stdout](../../tools/bolt/results/crash-fix-probe-20261028/objcopy-gdb-detail.stdout) 保存现场对象和缓冲区。

```text
#1 ... ELFWriter<...>::writeSegmentData()+87
SEGMENT type=6 offset=140509184 size=728
BUFFER start=0x7fffe315e040 end=0x7fffe52fa648 size=35243528
```

`type=6` 是 **第0个 PT_PHDR**，不是 `.text` 或某个 DWARF 节；它处理的内容是程序头表，表本身不对应一个常规 section。反汇编显示先取 Segment.Offset 加到 BufferStart，然后调用 memcpy；728 B与程序头表大小完全相符。越界目标区间为 `[140509184,140509912)`，而输出缓冲区有效范围仅 `[0,35243528)`。

本地 f308 源码 [sources/ELFObject.cpp.numbered.txt](../../tools/bolt/results/crash-fix-probe-20261028/sources/ELFObject.cpp.numbered.txt)：

- L2450–2456 `layoutSegmentsForOnlyKeepDebug`：`if (Seg->Type == PT_PHDR) continue;`，保留旧偏移。
- L2511–2534 `assignOffsets`：压缩 NOBITS 后的节、段布局，据此计算输出尾部与节头表。
- L2534起 `totalSize` 按缩小后的布局分配空间。
- L2125–2130 `writeSegmentData`：`memcpy(Buf->getBufferStart() + Seg.Offset, ... , Size)`，仍按旧 PHDR 偏移写入，未检查输出边界。

普通 clang 的 PT_PHDR 偏移64不触发越界；37无old-text和39有old-text都触发，故不能通过撤销 old-text 根治。上游修复方向应检查 only-keep-debug 的 PT_PHDR/ProgramHdrSegment 重布局及写入边界；本轮不改 LLVM 源码，也不把简单跳过 memcpy 当作已认证补丁。

## 5. 平台如何抽取、收集和拆分 debuginfo

实际根内脚本完整快照及行号：[sources/find-debuginfo.sh.numbered.txt](../../tools/bolt/results/crash-fix-probe-20261028/sources/find-debuginfo.sh.numbered.txt)；rpm macros、brp-strip、brp-strip-comment-note 也在 sources，来源和SHA见 [sources/provenance.json](../../tools/bolt/results/crash-fix-probe-20261028/sources/provenance.json)。

### 5.1 选择条件与分离命令

find-debuginfo L387–410 先找可执行位文件、`*.so*`、`*.ko`，排除 `*.a` 及debug目录的`.debug`；再读 `objdump -h`：

```sh
*debuglink*) continue ;;
*debug*) ;;
*gnu.version*)
  echo "WARNING: ... is already stripped!"
  continue
```

所以**并非简单依赖 file 的 not stripped**；`file` 在后面只再次确认 ELF。带 `.gnu_debuglink` 的副本会直接跳过抽取。

L248–281默认 `eu-strip --remove-comment $g $strip_option -f debug binary`；工具会同时分离符号并生成gnu_debuglink。`STRIP_DEFAULT_PACKAGE=binutils` 才走 cp+GNU strip+objcopy --add-gnu-debuglink；Kconfig/内核分支另有GNU only-keep-debug。本轮普通clang不走内核分支。

L425–468：已存在对应debug文件就return；正常DWARF抽取会调用debugedit改源码路径并取build-id，缺build-id默认警告，strict模式才失败；已有 `/usr/lib/debug` 内容不作为正常可执行文件再strip。使用我们预置的符号文件和debuglink可绕开不必要的再次抽取。

### 5.2 手工放置的文件是否进 clang-debuginfo

L678–685把**已经存在**的 `/usr/lib/debug` 文件全量写入 `debugfiles.list`。本轮在新临时根只执行同样的列表枚举，输出：

```text
/usr/lib/debug/usr/bin/clang-22.debug
```

证据：[platform-debug-list.stdout](../../tools/bolt/results/crash-fix-probe-20261028/platform-debug-list.stdout)、[package-list-analysis.json](../../tools/bolt/results/crash-fix-probe-20261028/package-list-analysis.json)。根内 macros L202–212有 `%files debuginfo -f debugfiles.list`，L581 `_debuginfo_subpackages 1`；已有 clang RPM 的主文件清单包含 `/usr/bin/clang-22`（[clang-rpm-files.stdout](../../tools/bolt/results/crash-fix-probe-20261028/clang-rpm-files.stdout)）。自动子包规则以 `/usr/lib/debug` + 主文件路径 + `.debug` 对应，因此应归入 **clang-debuginfo**，而非只挂在总llvm-debuginfo。

补充查阅 [RPM 4.14分支的 files.c](https://github.com/rpm-software-management/rpm/blob/rpm-4.14.x/build/files.c#L2843)：`filterDebuginfoPackage` 对存在的对应debug路径收集并克隆子包。保存的上游文件不是Tizen精确补丁版，报告不混称；本轮没有运行rpmbuild，最终分包归属仍需未来实现时的实际RPM验收。未来应放路径对应文件、安装为非执行模式，不仅任意扔一个名字到debug目录。

### 5.3 39号真实执行证据与工具影响

[platform-log-anchors.txt](../../tools/bolt/results/crash-fix-probe-20261028/platform-log-anchors.txt) 保留原日志行号：

```text
26060: [15636s] + /usr/lib/rpm/find-debuginfo.sh -j8 --build-id-seed 22.1.8-1 --unique-debug-src-base llvm-22.1.8-1.x86_64 -S debugsourcefiles.list /home/abuild/rpmbuild/BUILD/llvm-22.1.8
26061: [15637s] WARNING: /usr/bin/clang-22 is already stripped!
27010: [16017s] Processing files: clang-debuginfo-22.1.8-1.x86_64
```

41号实物清单也证实没有clang-22.debug。39号实际平台后处理日志是find-debuginfo、check-buildroot、brp-compress、brp-strip-static-archive、brp-python-hardlink、Tizen列表脚本，未见对clang调用LLVM only-keep-debug。因此这次LLVM objcopy缺陷不是现行QB后处理必经路径。

发布模式的brp-strip脚本按file的`not stripped`筛选，完全strip的clang不选中；debug目录被排除。通用brp-strip-comment-note仍可能选择stripped ELF清理comment/note（GNU strip，不是LLVM only-keep-debug），不能泛称所有平台工具永远不接触clang。若未来自行选用LLVM only-keep-debug生成符号文件，则会直接踩到已确认缺陷；应选本轮验证过的GNU/elfutils工具，并重验最终身份SHA与post。

## 6. 方案甲：符号文件 + GNU debuglink

### 6.1 操作、身份和代码不变

完整脚本 [scripts/scheme_a.py](../../tools/bolt/results/crash-fix-probe-20261028/scripts/scheme_a.py)。从39 pre-strip clang.bolt以GNU objcopy `--only-keep-debug`分出符号文件，将最终clang副本用LLVM objcopy `--add-gnu-debuglink=.../clang-22.debug`加链接。输出只在本轮temp。

- debug文件 33,147,264 B，SHA `231fd62322997f7914fc2f945e5ac8a6fb23c3f365d12943ec071b326a9edaf1`；有symtab/strtab，无DWARF源码行，另保留原非加载元数据，非可运行程序。
- 加debuglink后的clang 152,532,400 B（+104 B），SHA `4ce9d8fdbd3fd9b01c937b8af0cca25302c026278cce2c77372d3b3b0c4e66b6`。
- [scheme-a-layout.json](../../tools/bolt/results/crash-fix-probe-20261028/scheme-a-layout.json)：所有ALLOC非NOBITS节内容、地址、大小均相同，程序头逐项相同，RUNPATH仍为`$ORIGIN/../lib64`。新增节只有`.gnu_debuglink`。
- 严格按整个LOAD字节比较，偏移40和60不同，这是ELF头 `e_shoff`/`e_shnum` 更新；不能声称除新节外**整个文件**逐字节相同。运行代码和数据节没有改变。
- debuglink的文件名和CRC一致：[debuglink-crc.json](../../tools/bolt/results/crash-fix-probe-20261028/debuglink-crc.json)。
- 5个历史TU×3目标，完整.o逐字节 **15/15 PASS**；两边同一路径、同inode、同resource-dir与既有参数，保留.GCC.command.line。[scheme-a-correctness.json](../../tools/bolt/results/crash-fix-probe-20261028/scheme-a-correctness.json)及tu目录含argv/原始输出。

### 6.2 chroot自动加载与实际崩溃

旧根中没有已安装的gdb/普通lldb CLI；`lldb-instr`实际上是仪器化工具，不是调试器。因此复制**本轮已构建、无需重建的Tizen lldb/lldb-server**及所需运行库到新建`temp/crash-fix-probe-20261028/scratch.debug-probe`。clang放`/usr/bin/clang-22`，debug放标准`/usr/lib/debug/usr/bin/clang-22.debug`，没有手工`target symbols add`。

只使用既有`sudo -n /usr/sbin/chroot`授权。在新临时根内临时mount proc，finally正常umount成功；旧构建根/proc没有改动。命令和mountinfo见 `chroot-proc-*`、`chroot-mountinfo-*`。未申请额外权限或修改系统设置。

[chroot-lldb-with-proc.stdout](../../tools/bolt/results/crash-fix-probe-20261028/chroot-lldb-with-proc.stdout) 原文：

```text
(lldb) image list -f -s
[  0] /usr/bin/clang-22 /usr/lib/debug/usr/bin/clang-22.debug
...
stop reason = signal SIGILL: illegal operand
frame #0: ... clang-22`(anonymous namespace)::PragmaDebugHandler::HandlePragma(clang::Preprocessor&, clang::PragmaIntroducer, clang::Token&) + 3360
frame #1: ... clang-22`clang::Preprocessor::HandlePragmaDirective(clang::PragmaIntroducer) + 81
```

源码只有`#pragma clang __debug crash`；该路径执行ud2，所以是SIGILL，不能按预想硬写SIGSEGV。LLDB在信号交给clang崩溃处理器前截获，bt共有23帧，其中21个clang帧全部有函数名，2个libc帧。与41号clang自行打印27帧的总数不应直接比较。无源码行。RLIMIT_CORE=0，没有生成core文件。

初次不挂proc时虽然能静态自动加载符号，运行后无法正确关联模块基址/展开栈；补齐仅临时根的proc后成功，保留失败与成功原文，未掩盖。

### 6.3 llvm-symbolizer的明确限制

使用41号最终clang崩溃栈中已有的24个**模块相对地址**，不能直接把ASLR绝对IP交给离线工具。

| 输入方式 | 函数名 | 源码行 |
|---|---:|---:|
| `--obj=clang-22.debug`（GNU符号文件） | 24/24 | 0/24 |
| `--obj=eu.debug`（elfutils符号文件） | 24/24 | 0/24 |
| `--obj=clang-22`，让其自动找debuglink | 19/24 | 0/24 |

[symbolization-summary.json](../../tools/bolt/results/crash-fix-probe-20261028/symbolization-summary.json)、`symbolizer-*.stdout`保留原文。源码 `Symbolize.cpp` L819–824从外部文件构建DWARFContext，但仍用原始主文件`Objects.first`建立符号表模块；纯symtab外置文件没有DWARF，所以自动路径没有完整使用外置symtab。这与LLDB自动加载成功不矛盾。

**方案甲可解决安装debuginfo后的调试器/显式离线函数定位；不能保证仅在PATH放llvm-symbolizer就把clang自动打印栈全部变成函数名。** 运维应保存崩溃栈、匹配版本debug文件，显式对模块偏移运行symbolizer；若要求自动源码行，需要另行实证方案乙。

### 6.4 成本

GNU分离实测0.21s、最大RSS100,456 KiB；eu-strip分离2.73s、332,304 KiB（含另写stripped副本），只代表本机这次单文件观测，不是QB固定值。时间/RSS原文在 `timed-gnu.stderr`、`timed-eu.stderr`。

debug文件独立xz preset5估计：GNU 3,298,996 B，eu 3,519,088 B（[debug-sizes.json](../../tools/bolt/results/crash-fix-probe-20261028/debug-sizes.json)）。它应增加 **clang-debuginfo** 的载荷；主clang仅加104 B debuglink，实际RPM压缩变化须重打包才知，不能把33MB全算进clang主包。估算不含cpio、跨文件字典或RPM头。

## 7. 方案乙：更新DWARF，因缺输入跳过

[relink-inventory.json](../../tools/bolt/results/crash-fix-probe-20261028/relink-inventory.json) 和 [work-file-inventory.json](../../tools/bolt/results/crash-fix-probe-20261028/work-file-inventory.json)：39 clang-bolt目录内唯一重链ELF是`reference-relocs-clang-22`，226,739,000 B，SHA `e79409133e6c9b12eecd33ee9af3ab6bc76049db5de4f43c8622b8c8a09b0598`，有`.rela.text`、无任何`.debug*`/`.zdebug*`；ordinary有DWARF但没有所需重链输入的身份与重定位，不能替代。

helper L1376已经就地`llvm-strip --strip-debug reference`，不会保留此前带DWARF的版本。因此本轮 **NOT RUN**：不重新链接、不运行`--update-debug-sections`、不编造profile统计、源码行、输出大小、内存、时间和15TU结果。方案甲不能从已丢弃的DWARF恢复源码行。

未来方案乙需在strip-debug之前保留/使用带debug的重链输入，再用生产参数加`--update-debug-sections`，重新认证匹配、代码布局、15/90TU、RUNPATH、安全属性和debugsource映射。成本可能明显增加是**推测**，本轮没有测量，不能借ordinary的1.79GB大小当作更新DWARF后的结果。

## 8. 后续实现建议与本轮处理记录

可采用的最小函数定位方案：在BOLT输出尚有符号表时分离debug文件；完全strip并修好RUNPATH的候选副本加debuglink；完成所有代码/安全/符号匹配检查后，安装clang和标准debug路径文件。debuglinkCRC及debug文件SHA要纳入身份记录，最终clang的身份SHA必须在加debuglink后计算。post仍核对同一最终文件；当前不含debug文件的安装清单例外也须随正式设计调整。**本轮未修改以上发布逻辑。**

GNU有debug布局warning但已实证可用；eu-strip无这些warning且显式解析成功，正式实现选择它时仍需补全它对应的自动加载/对象/双模式RPM认证。不要把运行时ELF审计器原封不动用于独立debug文件：eu.debug保留的段范围不是可运行映像，在一次探索中触发运行时helper的range校验，属于工具用途不匹配，不是原始clang门禁失败。

准备性问题均保留记录：旧41地址JSON顶层是对象不是列表，脚本取`addresses`后修正；`lldb-instr`不是CLI，改用已存在的构建lldb；LLDB命令修正为`image list -f -s`和`settings set -- target.run-args ...`；无proc试验只能静态定位，临时挂载后完成动态栈；上游RPM两个猜测tag URL返回404，改用明确4.14分支，并标注它不是Tizen精确版本。以上没有改已有输入或绕过产品门禁。

原始输入末次SHA一致；source工作树干净；新临时proc已正常卸载；没有core、没有结束其他进程、没有动已有目录。脚本/结果清单见 [README.md](../../tools/bolt/results/crash-fix-probe-20261028/README.md)。

## 9. 两种方案比较

| 项目 | 甲：symtab外置debug（本轮GNU实现） | 乙：BOLT同步DWARF |
|---|---|---|
| 定位能力 | LLDB自动加载、21/21 clang栈帧有函数；显式symbolizer24/24；无源码行 | 目标为函数+源码行；本轮未测 |
| 自动llvm-symbolizer | 19/24，需显式指定debug文件才能24/24 | 需实证，不承诺 |
| 构建耗时增加 | 本地分离0.21秒；debuglink矩阵约0.5秒，RPM增量未测 | 未测 |
| 分离峰值RSS | 100,456 KiB（GNU）；eu替代332,304 KiB | 未测 |
| debuginfo大小 | 33,147,264 B；独立xz5约3,298,996 B | 未测 |
| 主clang大小 | +104 B，152,532,400 B；代码/数据不变，15/15对象一致 | 未测 |
| 风险/后续 | GNU debug布局warning、自动symbolizer限制；需正式集成并验RPM与post | 缺带DWARF重链输入；需认证布局、profile、资源、源码映射 |

总结论：**函数名定位方案甲已经实证可行，LLVM objcopy故障根因已闭合；发布包恢复仍待获准集成，源码行方案按输入缺失规则跳过，不能宣称已完成。**
