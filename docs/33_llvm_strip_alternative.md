# HQ llvm-strip 方案、bitcode 消费兼容性与固定快照消费者

日期：2026-09-29。本报告记录实际行为，不给出采用哪一种方案的建议。
docs/25–32 保留原样；本轮不续做 docs/32 的 v2 完整构建。

**阶段状态（2026-09-29 20:34 +08:00）：实验一、实验二宿主部分、实验三调查已完成；Tizen bfd 包按预期因归档格式失败。Tizen lld 的 A 链接成功，B 仍在6 GiB cap下链接，尚未进入 `%check`。本次发布是中间记录，不是完整任务验收结束；继续同一次运行，不重试、不调整cap。**

## 0. 范围、身份与原始证据

工作区 `W=/home/linhao/Toolchain/development/llvm-optimize`。下表路径以 W 展开，均指本机文件：

| 缩写 | 路径 |
| --- | --- |
| E | `/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-strip-alternative-20260929` |
| R0 | `W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0` |
| B30 | `W/temp/gbs-root-x86_64-archivefix/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build` |
| H | `W/temp/archive-index-fix-rpm-20260923/baseline-rpm-extract` |
| N | `W/temp/toolchain-archivefix`，docs/30 转换版 RPM 解包 |
| P30 | `W/temp/archive-fix-full-build-20260927` |
| RT | `W/temp/toolchain-runtime-baseline/libxml2/usr/lib64` |

`temp/` 原始输出不上传，须在上述工作区读取。查询脚本、命令 argv、HTTP URL/响应/SHA、完整 stderr、采样及汇总均保存在 E，附录列入口。
开始时主仓库 HEAD=`4adbdfbf657e48201e9991548f7b8e0b4a4d43c9`，status 为空，无他人 gbs/rpmbuild/ninja/lld/llvm-bolt。
独占锁位于 `W/temp/gbs-root-llvm-strip-alternative/.llvm-optimize-exclusive.lock`，由存活进程持有，会话标识、PID、开始时间见 `E/lock-acquired.json`。
W/llvm 与 spec、隔离旧混合根均未修改；R0 不读 BUILD，strip 通过它自己的 loader/库运行。B30 只读。
证据：`E/precheck.json`、`E/lock-acquired.json`；结束检查见附录。

225 个 B30 原件逐个 SHA 与 docs/30 的 `P30/new-archives-result.json` 中 `build_sha256` 核对，通过后复制到 `E/bc-archives/`。
这些是转换前且索引完整的构建树原件，**不是 docs/13 索引已坏的 RPM 归档**。
本轮还逐个复核docs/30的22个RPM SHA和N中225档SHA，均与原inventory一致（E/docs30-rpm-integrity.json、native-control-integrity.json）。
清单、成员数、bitcode/机器码数、索引条目数和 SHA：`E/bc-inventory.json`；原始完整映射：`P30/new-archive-checks/*.json` 的 build 项。

资源：离线阶段沿用 `min(18, floor(MemAvailable/GiB)-4)` GiB cgroup、swap=0、nice 15、ionice 3、采样/低内存中止/回收；编译 AS=4 GiB，链接无 AS 限制。
**运行前规则变更（用户于本轮首次 GBS 启动前决定）**：16 GiB 准入 / 18 GiB cap 仅用于完整 LLVM 构建。测试包及消费者包改为 **MemAvailable≥8 GiB、MemoryMax=6 GiB、MemorySwapMax=0**，宿主 MemAvailable<2 GiB 仍自动中止；逐包串行。磁盘≥60 GiB、nice 15/ionice 3、编译 AS 4 GiB、链接无 AS、采样与回收不变。
依据为用户引用的 docs/30 §4 小测试包实测峰值约4.6 GB；这是测试前政策，不是链接失败后的重试放宽。完整 LLVM 的 tools/build_llvm_x86_64.py 未改，测试入口在 E/run_tizen_consumer.py 单独实现8/6政策。
原16 GiB等待从13:34:52开始，19:17:50因用户新决策主动结束，期间GBS启动0次；全部读数见附录和 E/tizen-bfd-wait16GiB/memory-admission.jsonl。原脚本存 E/run_tizen_consumer-16g-prior.py，变更登记 E/resource-policy-change.json。
第一包实际于19:18:35准入，MemAvailable=16506318848 B（15.373 GiB），明确启动6 GiB/swap0 scope；其测得峰值与第二包结果见§3。
各阶段实际上限和事件见 `E/*-scope/plan.json`、`memory-summary.json`、`scope-after-rpm.json`，不能把 cgroup 总峰值混作单个链接进程 RSS。

## 1. llvm-strip：保留索引是成功处理，还是失败未写回

### 1.1 工具与三个样本

实际运行：

```sh
"$R0/lib64/ld-linux-x86-64.so.2" \
  --library-path "$R0/usr/lib64:$R0/lib64" \
  "$R0/usr/bin/llvm-strip" -g COPY.a
```

`llvm-strip` 是 llvm-objcopy 的别名；保留 argv[0] 为 llvm-strip，没有把该路径 resolve 成 llvm-objcopy。
实际 ELF SHA256=`d0b3cf18df5154b263ea009284b07cb1faced0758923d44953f2f53d70af509d`；loader SHA256=`e5f09939e3bb271e04524de3eb82d9d26bb528d3fe10cb9c6e7ebbaa069f466a`。
`--list` 的全部共享库路径保存在 `E/strip/dependencies.*`，没有安装到宿主。

```text
llvm-strip, compatible with GNU strip
LLVM (http://llvm.org/):
  LLVM version 22.1.8
  Optimized build.
```

| 构建树原件 | bitcode / 机器码成员 | exit | 字节数（前→后） | 索引条目（前→后） | SHA 是否改变 | ELF 调试节成员（前→后） |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| `lib64/libLLVMAnalysis.a` | 125 / 6 | 1 | 134892324→134892324 | 9445→9445 | 否 | 0→0 |
| `lib64/libLLVMBinaryFormat.a` | 14 / 0 | 1 | 3007612→3007612 | 247→247 | 否 | 0→0 |
| `lib64/clang/22/lib/linux/libclang_rt.asan-x86_64.a` | 0 / 125 | 0 | 7124522→3968658 | 5450→5450 | 是 | 76→0 |

证据：`E/strip/result.json`，含前后完整成员及索引；`strip-0/1/2.json` 含完整 argv、退出码、stderr。三个 B30 原件处理后再次验 SHA，均未修改。
前两个样本的 stderr 各一行，错误正文分别为：

```text
libLLVMAnalysis.a(AliasAnalysis.cpp.o)': The file was not recognized as a valid object file
libLLVMBinaryFormat.a(AMDGPUMetadataVerifier.cpp.o)': The file was not recognized as a valid object file
```

上述为去掉绝对路径前缀的摘录；完整原文在 `E/strip/strip-0.stderr`、`strip-1.stderr`。ASan 的 stderr 为空，完整符号→成员（含ordinal/重名序号）映射前后相同，且均恰为机器码外部定义符号；E/asan-index-crosscheck.json。
bitcode 内的调试元数据不是 ELF 调试节；表中前两项“0”不能解释成调试信息已剥离，其文件逐字节没改。

三个样本 SHA：

| 文件 | 处理前 SHA256 | 处理后 SHA256 |
| --- | --- | --- |
| Analysis | `26a56befd7f7e6309396586449c56d393b51afd6e4e401cda37d650d7eefffe4` | 同前 |
| BinaryFormat | `ee38e333dd84acb6ffb940b3a8e3c2456afaa4adf7d6634c9d45e8fbc4f8da83` | 同前 |
| ASan | `c556a14e396a2e01ff7021d737f8069889f33db046622daabd3f18d72781a4be` | `18879ada8c6e5ed5505e72dca4c0f7a0a66d03676d471c67a4d03bf939c3fa46` |

### 1.2 225 个含 bitcode 归档与 brp 的返回值

对 BC 集全部 225 个副本实际执行相同 `llvm-strip -g`：**225 次 exit=1、225 条错误行，225 个文件 SHA 与完整索引均未改变**。
不是按三个样本推算错误数量。逐档全文见 `E/strip-all-bitcode/`；汇总 `E/bc-inventory.json`。
因此本输入下是**整档失败、未写回，所以原索引保留**，不是 bitcode 被正确 strip 后保留索引。
工作区源码也与实测一致：`llvm/llvm/lib/ObjCopy/Archive.cpp:31` 的 `Child.getAsBinary()` 失败即返回；`:100` 构造所有新成员，`:101` 先检查失败，`:104` 才执行 `deepWriteArchive`。

R0 的脚本没有检查每次 `$STRIP` 的退出码，也没有 `set -e`：

```text
7  STRIP=${1:-strip}
15 for f in `find "$RPM_BUILD_ROOT" -type f -a -exec file {} \; | \
16         grep -v "^${RPM_BUILD_ROOT}/\?usr/lib/debug"  | \
17         grep 'current ar archive' | \
18         sed -n -e 's/^\(.*\):[ \t]*current ar archive/\1/p'`; do
19         $STRIP -g "$f"
20 done
```

出处：`R0/usr/lib/rpm/brp-strip-static-archive:7,15–20`；编号原文及 SHA 存 `E/rpm-macro-evidence/`。
它会继续处理后续归档，但**不能据此声称打包必定成功**：最后一次循环命令的状态会成为脚本状态；若最后一档失败，外层 RPM 的 `sh -e` 仍可能令安装阶段失败。
外层依据：`R0/usr/lib/rpm/macros:819–820,893–894,898–901`；宏调用链 `tizen_macros:34–42,53–56`。
本轮未完整构建 HQ LLVM spec，所以真实整包最后一个处理对象和整体退出状态没有冒充实测。

## 2. 完整索引 bitcode 的宿主消费者

### 2.1 环境和调用边界

程序 A 沿用 docs/29：解析固定 IR、执行 PassBuilder O2、输出 IR；成功项均与 H 中 opt `-O2` 输出逐字节比较。
源码、输入、expected.ll：`E/host-consumers/`；实现来源 `tools/verify_native_archive_consumers.py` 的 PROGRAM_A/IR。
编译、链接分开；通过 `llvm-config --link-static` 获取 asmparser/passes/core/support 库和系统库，配置查询前缀的 lib64 指向 BC 集。
clang 为 H 的 x86_64 22.1.8；头文件来自 H，C++ 标准库头文件/启动对象/glibc/libstdc++ 来自宿主 GCC 13，libxml2.so.16 来自独立 RT。
每个依赖的完整路径、compiler `-v` 搜索路径见 `E/host-consumers/compile-a-clang.log`、`compile-a-gcc.log`、`E/host-tools-identity.json`。

显式 host loader 调用 clang/lld；链接只输入 `.o`，没有 `-flto`。clang+GNU ld 的 `-###` 输出中没有 `-plugin`。
g++ 自行加入的是 GCC 的 `liblto_plugin.so`，不是 LLVMgold；本报告不把 g++ 组冒充“完全无任何插件”的 clang+GNU ld 组。
GNU ld+LLVMgold 是单独的显式插件组。所有真实完整 argv、计时、退出码、50 ms VmPeak/VmHWM/线程采样见各 `link-*.json/.log/.memory.jsonl`；`*-driver.txt` 保留 driver 展开。

### 2.2 结果与转换版历史值

| A 链接方式 | 完整索引 BC 结果 | 本次 wall s | 本次最大 RSS KiB | 可执行文件字节 | docs/30 转换+标准 strip 后同类历史值 |
| --- | --- | ---: | ---: | ---: | --- |
| clang22 + GNU ld.bfd，无 LTO/插件 | FAIL，file format not recognized | 0.04 | 44896 | 无 | PASS；2.57 s / 352084 KiB / 47387472 B |
| g++ + GNU ld.bfd，无 `-flto`/LLVM 插件 | FAIL，相同错误 | 0.01 | 6224 | 无 | 本轮追加对照PASS；5.79 s / 381524 KiB，IR一致 |
| clang22 + lld22 | PASS，IR 一致 | 83.13 | 6150588 | 496359272 | PASS；0.87 s / 299540 KiB / 47378880 B |
| clang22 + GNU ld.bfd + LLVMgold22 | PASS，IR 一致 | 70.79 | 5624248 | 498786960 | 无同插件历史轮；转换版无须插件的实测见首行 |

本次证据 `E/host-consumers/result.json`；历史证据 `P30/new-consumer-measurements.json`、`P30/new-rpm-consumers/result.json`（docs/30 §3.4）。
这里只并列成本，不算性能收益百分比：两次运行环境/缓存不同；HQ 留下 IR 调试元数据，转换版已经标准 strip，最终文件调试内容也不同；readelf节区原文及调试节列表见 `E/consumer-debug-sections.json`、`*-sections.log`。
宿主四组共同scope上限实际为6 GiB，MemoryPeak=6442450944 B恰到cap，memory.events max=2421、oom/oom_kill=0。存在受限回收压力，计时不能当不受限链接成本；cgroup峰值也不是自然需求上界。lld 的 bitcode 代码生成成本包含在链接阶段。`LLVMgold.so` 来自基线 RPM，路径 H/usr/lib64/LLVMgold.so；大小、SHA 在 `E/host-tools-identity.json`。

完整错误摘录（绝对库路径略）：

```text
/usr/bin/ld.bfd: .../libLLVMPasses.a: error adding symbols: file format not recognized
clang-22: error: linker command failed with exit code 1 (use -v to see invocation)
```

g++ 组尾行为 `collect2: error: ld returned 1 exit status`。原文：`link-clang-bfd.log`、`link-gcc-bfd.log`。
这证明索引完整并不足以让不支持 LLVM bitcode 的链接器使用该归档，失败不再归因于索引缺失。

## 3. HQ 模拟 RPM 与 Tizen 两个测试包

实验进行中；本节将在两次入口结束后写入实际状态，不能提前记为 PASS。

模拟包只重打 `llvm-static-devel`：从 docs/30 原 RPM 解包，以 BC 集替换 225 `.a`，版本为 `22.1.8.hqbc1-1`；其他 21 个 RPM 使用 docs/30 原件。
采用临时 spec 的空后处理以保留测得的原件字节，**这是消费者实验载体，不是 HQ LLVM spec 完整构建成功的证明**。
宿主不安装该 RPM；模拟RPM 2186733463 B，SHA256=`bd7dc99a6b02335836ba99cf3da31c7c4020dcec5a482be139742f007b373411`；再解包225档逐SHA均等于BC集。宿主打包使用gzip level1，不能拿压缩RPM大小与docs/30不同压缩政策直接算格式收益。临时 spec、命令、SHA 与解包核对见 `E/prepare_hq_rpm.py`、`hq-repack-command.json`、`hq-rpm.json`、`hq-payload-check.json`。

两个小包沿用 docs/30 的 A+B：精确 BuildRequires HQ static-devel 和 docs/30 llvm-devel/llvm/clang；编译 AS 4 GiB，链接无 AS，GNU ld 组拒绝出现 `-flto`/`-plugin`。
Python wait4 记录两个链接的 wall/user/sys/RSS；%check 比对 A 与根内 opt O2 输出，B 进程内调用 lld 生成小程序，验证退出码 37。
临时 source/spec 完整内容在 `E/test-package-{bfd,lld}/`，运行入口 `E/run_tizen_consumer.py`。
“逐包串行”指只有一个 GBS 包、一个链接命令同时运行，不等于 lld 内部单线程；A/B 的 lld 进程实测37线程，见 `E/tizen-lld/process-memory.jsonl`。没有追加 `--threads` 改写本轮链接命令。

### 3.1 GNU ld 测试包：格式失败，不是内存失败

第一次 GBS 于19:18:35开始，19:25:11结束，入口总 wall=396.149 s（包含准备/下载/安装），GBS exit=1。A 的链接命令 exit=1，wall=0.260502 s，最大 RSS=45360 KiB；完整 argv 与计时在 `E/tizen-bfd/build.log:538`。

```text
/usr/bin/ld.bfd: /usr/lib64/libLLVMPasses.a: error adding symbols: file format not recognized
```

原文 `E/tizen-bfd/build.log:536`。:304/:413/:483 分别显示选择、安装、rpm查询 `llvm-static-devel-22.1.8.hqbc1-1.x86_64`；不是因缺少模拟包失败。
A 失败后按 `set -e` 停止，B 链接和 `%check` 均未执行。没有重试。

本包 scope MemoryPeak=6442450944 B（6 GiB），memory.events 为 max=8346、oom=0、oom_kill=0；30秒采样宿主最低 MemAvailable=16038318080 B。
峰值恰到 cap，安装归档时以文件缓存为主，不等于 bfd 自身用了6 GiB，也不能当无约束自然峰值；bfd 的RSS以上述wait4数值为准。
采样器/日志线程均回收（`E/tizen-bfd/outcome.json` 两项 true）。完整采样、scope退出前快照与原始日志同目录。

### 3.2 lld 测试包

此包在bfd结束后于19:25:11启动，准入MemAvailable=16188317696 B；同样6 GiB/swap0，没有并行GBS。
后续结果在本轮完成后填入；完整原始输出持续写入 `E/tizen-lld/`。

A-lld 已退出0：wall=64.106504 s、max RSS=6012260 KiB（`build.log:536`）。B 从19:31:51开始，20:33:12后的进程检查仍存活，已运行3686 s、累计CPU34:20；当时累计读盘1762341175296 B、尚未写出结果。该时刻 OOM/OOM-kill=0，宿主30秒采样可用8.873 GiB。原始进程stat/io在 `link-progress-diagnostics.jsonl`，cgroup回收及I/O压力快照在 `resource-pressure-observation.json`。
这组值是**进行中的下界/快照**，不是最终wall、自然内存峰值或成功验收。20:34:16全机独占复查仅有本scope的gbs/rpmbuild/ld.lld，外来构建进程0（`E/exclusive-during-long-link.json`）。

## 4. 旧版本读取实测

本机找到 Chromium bundled `lld`，版本查询为 `LLD 18.1.0 (compatible with GNU linkers)`。
其解释器写成 `/emul/lib64/ld-linux-x86-64.so.2`；直接执行因宿主缺该路径失败，改用显式宿主 loader 后正常运行。
没有修改二进制。这个低版本候选的文件大小为 74278160 B，SHA256=`2a9553f0bee743d90a33d2dd6aa6ff0e5f83dd221793076fc54b07cdc7d459a1`；身份记录 `E/old-llvm/tool-identity.json`。命令：

```sh
/lib64/ld-linux-x86-64.so.2 \
 /home/linhao/Toolchain/plan_evaluation/chromium-efl/tizen_src/buildtools/llvm/bin/lld \
 -flavor gnu -r --whole-archive "$E/bc-archives/libLLVMBinaryFormat.a" \
 -o "$E/old-llvm/binaryformat-old.o"
```

exit=1，错误原文（仅省略绝对归档路径）：

```text
lld: error: .../libLLVMBinaryFormat.a(AMDGPUMetadataVerifier.cpp.o): Unknown attribute kind (102) (Producer: 'LLVM22.1.8' Reader: 'LLVM 18.1.0rc')
```

证据 `E/old-llvm/result.json`、`read-bitcode.stderr`；限流记录 `E/old-version-probe-scope/`。
此为一个实际不兼容样本，不能概括成所有旧版本都失败。追加同命令读取 N 中机器码 BinaryFormat：exit=0，1.10 s、28448 KiB；记录 E/additional-controls/old-lld-native.json。
兼容承诺方向的本项目源码依据：`llvm/llvm/docs/DeveloperPolicy.rst:774–780`，当前 reader 支持读取自 3.0 起的 bitcode；它没有承诺旧 reader 能读取未来 writer 的全部特性，文本 IR 也没有一般兼容承诺。

## 5. 固定快照消费者与实际链接路径

### 5.1 数据覆盖与直接 BuildRequires 清单

调查范围限定于 gbs_llvm.conf 钉住的两个公开快照，不代表私有 OBS 项目、所有历史快照或未发布包。
这两个公开快照是旧配方产物（docs/19），而本轮BC来自docs/30工作区ThinLTO配方。公开快照已有构建成功日志只证明原来的选择路径，**不是替换HQ模拟RPM后重新构建成功的证明**。表中据共享路径判断“不属于已证实失败集合”，不将其标成HQ试包PASS。

- Base：`tizen-base-toolchain_20260912.061113`，根 URL 为 `https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260912.061113/`。
- Unified：`tizen-unified-toolchain_20260814.092727`，根 URL 为 `https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260814.092727/`。

两者 `builddata/depends/` 均 HTTP 404；保留响应及目录索引。按要求退回 `repos/standard/source/repodata/repomd.xml` 指向的 primary，下载压缩原件并解压解析所有 src.rpm requires。
Base 共 361 条源包记录，Unified 共 1061 条。另对所有requires做llvm子串审计，只有libllvm/llvm/llvm-devel/llvm-static-devel四种名称，没有漏掉isa后缀或富依赖表达式（E/llvm-requirement-substring-audit.json）。源 primary 是 src 架构，不能直接拿它当三个架构均构建的证据；再结合 spec 的 ExclusiveArch 和该快照三个架构成功 buildlog 目录判定。
普查口径是该 source primary 实际暴露的直接 requires；并未取得三个架构的完整 OBS 依赖图，也未展开其余源包 spec 的所有架构条件。若条件依赖未进入这份 SRPM 元数据，本次无法从它发现，不能据此证明全平台消费者名单绝无遗漏。
元数据解析工具为 `tools/inventory_llvm_source_consumers.py`。完整 URL、HTTP 状态、SHA：`E/downloads/**/*.request.json`；解析结果 `E/dependency-scan-summary.json`、`{base,unified}-consumer-source-metadata.json`。

| 架构 | Base：BuildRequires llvm-static-devel | Unified：同项 | BuildRequires llvm-devel 参照（Base；Unified） |
| --- | --- | --- | --- |
| x86_64 | bcc-tools | 无 | bcc-tools、qemu-accel；coreclr、coreclr-diagnostics、coreprofiler、netcoredbg |
| armv7l | bcc-tools、bpftrace | 无 | bcc-tools、bpftrace；coreclr、coreclr-diagnostics、coreprofiler、netcoredbg |
| aarch64 | bcc-tools、bpftrace | 无 | bcc-tools、bpftrace；coreclr、coreclr-diagnostics、coreprofiler、netcoredbg |

`bpftrace.spec:19` 的 ExclusiveArch 只有 armv7l/aarch64，与日志目录一致。
qemu-accel 在 x86_64 上生成不同目标的 accel；这不是 ARM 架构 native static-devel 消费者。
`llvm-devel` 本身不含 `.a`：实际 `rpm -qpl` 输出 `E/llvm-devel-filelist.txt`，过滤 `.a` 为 0（`dependency-scan-summary.json` 保存 argv）。不能把该参照列表等同静态库消费者。

### 5.2 配方和实际日志的交叉核对

七个源 RPM 已全部下载并按 primary checksum 核对，spec/脚本在 `E/sources/<name-version-release>/`。
bcc/bpftrace 依 spec 顺序对独立分析副本应用 70/6 个补丁，`effective/` 是生效 CMake 内容；完整 patch 输出见 `E/source-patch-replay.json`。
其他四个 .NET 源包提取构建脚本到各 `scripts/`，没有执行这些构建脚本。
spec 命中、20 份真实 buildlog 命中及行号分别存 `consumer-spec-evidence.json`、`consumer-buildlog-evidence.json`。

| 包 | 证据和已核实路径 | 不能由此推出的事实 |
| --- | --- | --- |
| bcc-tools 0.35.0-1.1 | spec:88–89 同时依赖 devel/static-devel；:272–275 LLVM≥22 设置 `ENABLE_LLVM_SHARED=ON`，:284 传给 CMake。effective/cmake/clang_libs.cmake:1–2 选 LLVM，:35–36 选共享 clang；effective/src/cc/CMakeLists.txt:129–145,177–179 使用该同一库集。三个架构日志实测 Clang22.1.8、共享选项 ON、产物依赖 libLLVM/libclang-cpp。 | BuildRequires static-devel 不证明这些构建消费 LLVM `.a`；gcc BuildRequires 也不证明实际由 GCC 编译。 |
| bpftrace 0.24.2-1.1 | spec:19 仅两 ARM，:27–29 声明 LLVM 依赖，:93 `STATIC_LINKING=OFF`。effective/src/ast/CMakeLists.txt:91–103 选 USE_SHARED/libclang/clang-cpp；两个日志完整最终链接行直接列三种 `.so`。 | 0004 补丁新增静态路径只在 STATIC_LINKING 分支；不能把支持能力写成本次实际静态链接。 |
| qemu-accel 0.4-1.1 | qemu-accel-aarch64.spec:81–82 为 LLVMgold 取 llvm-devel；:337–347 复制工具和 LLVMgold.so。三个 x86_64 accel buildlog 已留档。 | 它消费/变换已编好的工具与共享对象，不是用 static-devel 链出工具；源包不含完整 armv7l 生成 spec 的历史边界仍保留。 |
| coreclr 8.0.11-0 | spec:90–99 为 clang/llvm/lldb 工具及 devel；:32–33 PGO开关0，:342–350 得 `--nopgooptimize`，x86_64日志:303 实际传入、:419–420 HAVE_LTO Failed。scripts/coreclr-8.0.11/eng/common/native/init-compiler.sh:136–139 探测成功才设 lld。 | 日志没打印最终所有 linker argv，具体最终 linker 标 UNKNOWN；不把脚本条件能力写成已发生。 |
| coreclr-diagnostics 8.0.547301-37 | spec:16–33 为工具/devel；:178 调用build.sh；scripts/coreclr-diagnostics-8.0.547301/eng/common/native/init-compiler.sh:136–139 同样条件选择lld。三个日志实测Clang22.1.8。 | 最终 linker 和完整 LTO 状态缺 argv，UNKNOWN；未发现系统 LLVM 静态库依赖。 |
| coreprofiler 1.2.1-1 | spec:14–19；scripts/coreprofiler-1.2.1/CMakeLists.txt:4–5 指定clang/clang++；src/CMakeLists.txt:51起链接CLR相关库。三架构日志Clang22.1.8。 | 不把 llvm-devel 依赖当作静态 LLVM 链接；日志不含最终 ld exec。 |
| netcoredbg 3.1.2-1 | spec:25–28、:125–137 指定clang/clang++；scripts/netcoredbg-3.1.2/src/CMakeLists.txt:206–278 链corguids/dl/pthread/linenoise/elf++/dwarf++/unwind/dlog。三架构日志Clang22.1.8。 | 不把 llvm-devel 或 clang-devel 依赖当作静态 LLVM 链接；日志不含最终 ld exec。 |

表中相对 spec/脚本路径的完整前缀均为 `E/sources/<包版本>/`。这四个 .NET 包只是 llvm-devel 参照项；没有据此计入 static-devel 受影响数。

实际共享链接日志定位（均相对 `E/downloads/base/logs/<arch>/succeeded/`）：

| 包 / 架构 | configure / compiler | 最终链接或 RPM NEEDED 派生依赖证据 |
| --- | --- | --- |
| bcc-tools / x86_64 | bcc-tools.buildlog.txt:876–879 | :2662 libLLVM.so.22.1、libclang-cpp.so.22.1 |
| bcc-tools / armv7l | :895–898 | :2701 同上 |
| bcc-tools / aarch64 | :898–901 | :2684 同上 |
| bpftrace / armv7l | bpftrace.buildlog.txt:429–431 | :3578、:3594 完整 clang++ 链接行，LLVM/clang 均 `.so` |
| bpftrace / aarch64 | :434–436 | :3583、:3599 同上 |

### 5.3 默认链接器、架构与判定边界

R0 与两个 ARM 根的 clang.cfg/clang++.cfg 只有目标 triple 和 resource-dir，没有 `-fuse-ld`。
R0/usr/lib/rpm/macros:74,76 为 x86_64-tizen-linux-gnu-clang/clang++；ARM 对应架构宏、optflags 文件的摘录和 SHA 在 `E/platform-defaults.json` 及 `E/*-rpm-config/`、`rpm-optflags-evidence.json`。各根 rpmrc:24/80/101 与 platform/<arch>-linux/macros:12 是文件默认；GBS可覆盖它们，因此不冒充实际展开值。
固定buildconfig（P30/full-build/buildconfig.conf:161–168）默认_toolchain=clang并选择__cc/__cxx；:304–305 Support含gcc/gcc-c++、clang/llvm-devel。llvm-devel的RPM Requires含llvm（E/llvm-devel-requires.json），lld在llvm包中。这是对应构建配置的依赖依据，不声称其他任意GBS配置也如此。
这些根均有 `/usr/bin/ld`、`ld.bfd` 和 `ld.lld -> lld`；“装有 lld”不等于“默认使用 lld”。

为遵守 R0 执行范围，实际 `clang -### -x c /dev/null` 查询在 docs/30 新根执行：输出最终 `/usr/bin/ld`；rpm -qf 为 binutils-2.43-1.9.x86_64；ld --version 为 GNU ld 2.43；ld.lld 属 llvm-22.1.8-1.6。
原文 `E/x86_64-default-query.log`。`-###` 没有执行编译/链接。
两个 ARM 根的 gbs chroot 均在 `su` 阶段报 Exec format error，GBS自身退出0不能冒充子命令成功；`E/{armv7l,aarch64}-default-query.log` 原文保留。
源码 `llvm/clang/lib/Driver/ToolChains/Linux.cpp:978–981` 对非Android回退，`llvm/clang/include/clang/Driver/ToolChain.h:494` 默认是 ld。
ARM 的 GNU ld 默认是根据 cfg/宏/源码推导，实际 chroot 调用未获证实，不能升格为 trace。

| 直接消费者 | 架构 | 实际编译器 | linker 证据强度 | LTO | HQ 归档的影响判定 | 转换归档的影响判定 |
| --- | --- | --- | --- | --- | --- | --- |
| bcc-tools | x86_64 | Clang22.1.8 | 默认GNU ld推导；本包无最终ld exec记录 | 配方/可见日志无-flto；无完整argv | 实际库集为共享LLVM/clang，未发现BC归档输入，不能判不能链接 | 同一共享路径，不消费被替换`.a`；未重构本包 |
| bcc-tools | armv7l | Clang22.1.8 | 默认GNU ld静态推导，运行态UNKNOWN | 同上 | 共享路径；本轮HQ改动仅x86_64 | 本轮转换仅x86_64，ARM归档未改 |
| bcc-tools | aarch64 | Clang22.1.8 | 同上 | 同上 | 同上 | 同上 |
| bpftrace | armv7l | Clang22.1.8 | 完整clang++链接行无-fuse-ld；最终ld exec未打印，默认GNU推导 | 两条最终链接行无-flto | LLVM输入明确为.so；本轮HQ改动仅x86_64 | 同一共享路径；ARM归档未改 |
| bpftrace | aarch64 | Clang22.1.8 | 同上 | 同上 | 同上 | 同上 |

**当前快照范围内，识别到 2 个直接 BuildRequires 包、5 个架构构建组合；已证实因 HQ bitcode 不能链接的真实包数为 0，而不是证明全平台永远零影响。**
故实验三第5项“选择判为不能链接的消费者”集合为空，没有为了凑失败样本修改 bcc/bpftrace 的共享配置，也没有启动真实消费者包 GBS 构建。
通用静态消费者的 bfd 不兼容已由实验二直接测得，与当前这两个包是否实际使用归档是两个不同结论。

## 6. HQ 方案与转换方案的实测对照

| 项目 | HQ：llvm-strip、保留bitcode | docs/30：转换机器码、原后处理 |
| --- | --- | --- |
| 索引 | 225档因strip失败未改写，完整索引保留 | 225档最终索引逐成员完整，docs/30 §3.1 |
| strip日志 | BC集225次exit1、225条错误；整包退出状态取决于宏链/顺序，未完整构建HQ | 标准brp执行，GNU strip格式错误0，docs/30 §3.2 |
| GNU ld无LTO/插件 | 宿主A失败；Tizen状态见§3 | 宿主A/B/共享库/GC与Tizen A+B PASS，docs/30 §3.4、§4 |
| GCC消费者 | g+++bfd实际失败（默认GCC插件不读取LLVM22bitcode） | 本轮同一g++生成的a.o链接转换库PASS，IR与opt一致（E/additional-controls/） |
| lld消费者成本 | 本次A 83.13s / 6150588KiB / 496359272B | 历史A 0.87s / 299540KiB / 47378880B；非受控成本并列 |
| GNU ld+LLVMgold | 本次A成功70.79s，输出正确 | 无插件即已成功；未额外测插件组 |
| Tizen内部lld | 见§3当轮结果 | docs/30两程序%check通过 |
| 版本错位 | LLD18读取LLVM22 BinaryFormat报Unknown attribute kind | 同一LLD18读取转换版BinaryFormat成功（-r/whole-archive正对照），不外推全部归档/API兼容 |
| 当前固定快照真实受影响数 | 找到2直接BR包/5组合，均走共享LLVM；未证实受影响包 | 未对真实包做替换重构；作用边界同左 |
| 225档未压缩总字节 | 5482378620（IR调试信息留存） | 520479520（转换后标准strip）；不能把差额全部归为bitcode格式本身 |
| 包/产物体积 | 模拟RPM2186733463B；gzip level1，压缩政策与基线不同 | static-devel RPM60449442B；SHA见P30/rpm-inventory.json |

## 7. UNKNOWN 与实验边界

- 真实 HQ LLVM 完整构建是否结束成功：本任务不构建LLVM，只复现strip和模拟消费者载体；需要实际HQ spec全日志和最终文件顺序。
- ARM 根内 driver 实际调用：本机 binfmt/chroot 的 su 不能执行，保留失败；没有更改宿主注册/sysctl/capability。需要可运行的ARM环境或worker exec trace。
- bcc 最终 ld exec、四个 .NET 参照包最终链接argv：公开日志不完整；已读spec/scripts并指出条件，没有按惯例填值。需要 CMake link.txt/verbose日志/trace。
- 覆盖范围只包含这两个固定公开快照。新增私有包、其他快照、未显式声明BuildRequires而依赖Support间接带入的消费者、`llvm-config --link-static` 的第三方应用仍需自己的依赖/链接证据。
- 性能数字为单次功能实验和docs/30历史成本，不是校准后的性能收益，也不是Chromium/全平台收益。

## 附录：命令、原始输出与检查

本轮入口与主要证据：

| 实验 | 完整命令/输入 | 原始输出 |
| --- | --- | --- |
| 独占/现场 | E/precheck.json、hold_lock.py | lock-acquired.json、结束检查 |
| 三样本strip | tools/probe_hq_llvm_strip.py --build B30 --rpm-root R0 --output E/strip，经E/run_stage.py执行 | strip/*.json/*.stdout/*.stderr、strip-scope/ |
| BC集验证/225档strip | E/prepare_bc.py | bc-inventory.json、strip-all-bitcode/、prepare-bc-scope/ |
| 宿主四组 | E/host_consumers.py、host-consumers/*driver.txt、compile-*.json/link-*.json | *.log/*.time/*.memory.jsonl、result.json、host-consumers-scope/ |
| 旧LLVM | E/probe_old.py | old-llvm/、old-version-probe-scope/ |
| 模拟RPM | E/prepare_hq_rpm.py、hq-rpmbuild/SPECS/llvm-static-devel-hq.spec | hq-repack-ready-scope/、hq-rpm.json、hq-payload-check.json |
| 两个Tizen测试包 | E/prepare_tests.py、test-package-*/、run_tizen_consumer.py | tizen-*/，包括内存准入、启动argv、GBS全日志、cgroup与采样 |
| 网络/源包 | E/fetch.py、fetch_consumer_logs.py、extract_build_scripts.py、prepare_effective_sources.py | downloads/**及request.json、sources/、dependency-scan-summary.json |
| 默认工具链查询 | E/query_defaults.py，stdin和argv均另存JSON | 三架构default-query.log、platform-defaults.json、rpm-macro-evidence/ |

网络索引清单见 `E/download-index.json`；下面保留关键下载身份。最终测试状态收尾时补齐。

### 下载身份

| 元数据/源RPM | SHA256 | 原始URL |
| --- | --- | --- |
| source-primary.xml.gz | `8509c65aee1a8a5e88deb7e7c3fb10097a1d01c119f42c1c9bc24e54b189df8b` | [原始文件](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260912.061113/repos/standard/source/repodata/8509c65aee1a8a5e88deb7e7c3fb10097a1d01c119f42c1c9bc24e54b189df8b-primary.xml.gz) |
| source-repomd.xml | `eb10cdac95fe61e745104ca06712a827426d8a25e0ee864fe03767585a65b984` | [原始文件](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260912.061113/repos/standard/source/repodata/repomd.xml) |
| bcc-tools-0.35.0-1.1.src.rpm | `bc55b08a3a79e50eb0a64ed607712cf2b80f4c78db6e9ad8355b3f796517895b` | [原始文件](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260912.061113/repos/standard/source/bcc-tools-0.35.0-1.1.src.rpm) |
| bpftrace-0.24.2-1.1.src.rpm | `9c257b769c858d884d94444475ab11b71a72aa7ebe5f5209d6b5e15e028ec9fc` | [原始文件](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260912.061113/repos/standard/source/bpftrace-0.24.2-1.1.src.rpm) |
| coreclr-8.0.11-0.src.rpm | `46ac02ef3e79a2f380e8b02ba97bb99ac4f81fbd743a5d0e0750bd0e9152b798` | [原始文件](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260814.092727/repos/standard/source/coreclr-8.0.11-0.src.rpm) |
| coreclr-diagnostics-8.0.547301-37.src.rpm | `ebb038b57d2f7800d1377a445c4790da7f9171524a9a17669a9a4991513edaba` | [原始文件](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260814.092727/repos/standard/source/coreclr-diagnostics-8.0.547301-37.src.rpm) |
| coreprofiler-1.2.1-1.src.rpm | `6cf6e57d0e650ce93e646ee3af677309dab63366387da1b9830ea7f29b58d55f` | [原始文件](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260814.092727/repos/standard/source/coreprofiler-1.2.1-1.src.rpm) |
| netcoredbg-3.1.2-1.src.rpm | `b8f7f2a48e01b0102071fc1b9b97a7ec8eac2e926a6aeda6ab4fdf6d36fcc62e` | [原始文件](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260814.092727/repos/standard/source/netcoredbg-3.1.2-1.src.rpm) |
| qemu-accel-0.4-1.1.src.rpm | `1a78b7b192b2151cc1e0b12cf92ba1b1bc179ccfb8aec3090a68f365b623ff0b` | [原始文件](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260912.061113/repos/standard/source/qemu-accel-0.4-1.1.src.rpm) |
| source-primary.xml.gz | `32fd3292f71a65a5e38296ce64dc218ccdb196dbf7156b19a649da72f99b3865` | [原始文件](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260814.092727/repos/standard/source/repodata/32fd3292f71a65a5e38296ce64dc218ccdb196dbf7156b19a649da72f99b3865-primary.xml.gz) |
| source-repomd.xml | `4661aa031895fbfa509f0fc8b625a0d3a936e08a2cefad29a62bf0c7ac6436ab` | [原始文件](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260814.092727/repos/standard/source/repodata/repomd.xml) |

两个 primary.gz 的 checksum 与各自 repomd 声明完全一致：`E/source-metadata-checksums.json`。完整 requires 列表由 `tools/inventory_llvm_source_consumers.py` 导出到 `E/{base,unified}-consumers-complete.json`；不要把 src 字段当目标架构。

### 原 16 GiB 准入等待读数（完整）

门槛 17179869184 B；以下 69 次均未准入，未启动 GBS。时间均为 2026-09-29 +08:00。19:17:50 按用户新规则结束等待，随后改用 8 GiB 门槛，并非旧规则超时或测试失败。

| 时间 | MemAvailable 字节 | GiB |
| --- | ---: | ---: |
| 13:34:52 | 12615606272 | 11.749199 |
| 13:39:52 | 12957564928 | 12.067673 |
| 13:44:52 | 12795002880 | 11.916275 |
| 13:49:52 | 12517355520 | 11.657696 |
| 13:54:52 | 12520230912 | 11.660374 |
| 13:59:52 | 12856102912 | 11.973179 |
| 14:04:52 | 12739002368 | 11.864120 |
| 14:09:52 | 12731805696 | 11.857418 |
| 14:14:52 | 12853641216 | 11.970886 |
| 14:19:52 | 12810416128 | 11.930630 |
| 14:24:52 | 12466044928 | 11.609909 |
| 14:29:52 | 12787064832 | 11.908882 |
| 14:34:52 | 12865941504 | 11.982342 |
| 14:39:52 | 12523806720 | 11.663704 |
| 14:44:52 | 12856180736 | 11.973251 |
| 14:49:52 | 12724224000 | 11.850357 |
| 14:54:52 | 12549746688 | 11.687862 |
| 14:59:52 | 12558622720 | 11.696129 |
| 15:04:52 | 12538880000 | 11.677742 |
| 15:09:52 | 12661616640 | 11.792049 |
| 15:14:52 | 12109570048 | 11.277916 |
| 15:19:52 | 11769753600 | 10.961437 |
| 15:24:52 | 12072345600 | 11.243248 |
| 15:29:52 | 12125577216 | 11.292824 |
| 15:34:52 | 12159074304 | 11.324020 |
| 15:39:52 | 12309942272 | 11.464527 |
| 15:44:52 | 12128993280 | 11.296005 |
| 15:49:52 | 12230660096 | 11.390690 |
| 15:54:52 | 12062236672 | 11.233833 |
| 15:59:52 | 12018982912 | 11.193550 |
| 16:04:52 | 12085841920 | 11.255817 |
| 16:09:52 | 12153696256 | 11.319012 |
| 16:14:52 | 12171993088 | 11.336052 |
| 16:19:52 | 12135747584 | 11.302296 |
| 16:24:52 | 12001226752 | 11.177013 |
| 16:29:52 | 12551929856 | 11.689896 |
| 16:34:52 | 12502945792 | 11.644276 |
| 16:39:52 | 12441432064 | 11.586987 |
| 16:44:52 | 12451872768 | 11.596710 |
| 16:49:52 | 12312305664 | 11.466728 |
| 16:54:52 | 12450009088 | 11.594975 |
| 16:59:52 | 12480925696 | 11.623768 |
| 17:04:52 | 12337434624 | 11.490131 |
| 17:09:52 | 12619722752 | 11.753033 |
| 17:14:52 | 12620812288 | 11.754047 |
| 17:19:52 | 12388339712 | 11.537540 |
| 17:24:52 | 11996618752 | 11.172722 |
| 17:29:52 | 12109066240 | 11.277447 |
| 17:34:52 | 16579547136 | 15.440907 |
| 17:39:52 | 16322818048 | 15.201809 |
| 17:44:52 | 16420196352 | 15.292500 |
| 17:49:52 | 16275484672 | 15.157726 |
| 17:54:52 | 16262868992 | 15.145977 |
| 17:59:52 | 16364134400 | 15.240288 |
| 18:04:52 | 16300580864 | 15.181099 |
| 18:09:52 | 16586346496 | 15.447239 |
| 18:14:52 | 16569524224 | 15.431572 |
| 18:19:52 | 16526954496 | 15.391926 |
| 18:24:52 | 16622612480 | 15.481014 |
| 18:29:52 | 16661508096 | 15.517239 |
| 18:34:52 | 16579665920 | 15.441017 |
| 18:39:52 | 16406089728 | 15.279362 |
| 18:44:52 | 16474210304 | 15.342804 |
| 18:49:52 | 16628293632 | 15.486305 |
| 18:54:52 | 16257466368 | 15.140945 |
| 18:59:52 | 16463454208 | 15.332787 |
| 19:04:52 | 16266723328 | 15.149567 |
| 19:09:52 | 16206520320 | 15.093498 |
| 19:14:52 | 16781361152 | 15.628860 |
