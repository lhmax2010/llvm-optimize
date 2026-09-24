# 静态库 bitcode 转机器码 v3：离线全部通过，完整构建因内存准入停止

日期：2026-09-24。起点提交 `fbac89613bfa8a38e72c8716eda29150b9884c75`。
docs/25–28 保留不动；本文件登记本次明确授权的规则变更和实测，不回判旧任务结果。

**结果：第一段全部功能门禁 PASS；第二段已准备隔离 spec/Source 和精确认证，但唯一一次构建入口在预检时停止。**
`2026-09-24T15:35:18+08:00`，MemAvailable **15.929 GiB < 16 GiB**，因此 GBS 没有启动。
没有等待后重试、没有修改资源门槛；完整 LLVM 构建 0 次、新 RPM 0 个、Tizen 测试包构建 0 次。
修法可以进入完整构建验证，**尚不能作为已验收的修复提交 Gerrit/发货**。

## 0. 路径、独占与输入核对

所有缩写在本文内定义；`temp/` 原始证据仅在本机，不上传 GitHub。

| 名称 | 绝对路径或展开 |
| --- | --- |
| W | `/home/linhao/Toolchain/development/llvm-optimize` |
| E | `W/temp/static-native-conversion-v3-20260924`，本轮证据 |
| E28 | `W/temp/static-native-conversion-v2-20260924`，docs/28 证据 |
| H | `W/temp/archive-index-fix-rpm-20260923/baseline-rpm-extract`，基线 RPM 内容 |
| R0 | `W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0` |
| Rnew | `W/temp/gbs-root-x86_64-archivefix`，任务期间只有独占锁，没有初始化 GBS |
| S | `W/temp/llvm-archivefix-trial`，隔离试验工作树 |
| U | `E28/conversion/archives`，未经 strip 的机器码归档 |
| N | `E/stripped/archives`，本次模拟 strip 后的机器码归档 |
| RT | `W/temp/toolchain-runtime-baseline/libxml2/usr/lib64` |
| L | `/lib64/ld-linux-x86-64.so.2`，宿主 loader |

前置核对结果（`E/precheck.json`）：主仓库 status 空，没有其他 rpmbuild/gbs/ninja/lld/llvm-bolt。
S HEAD=`f111162e94aa48ed367c9d2c039456c70e7160ae`，分支 `archive-fix-trial`；
初始 spec SHA=`95887b2d060b38d5ef8f56936f7481a03d131f9d26432180a68e02ec95f0dda5`，
相对 HEAD 只有 4/4/1 三处并发修改，与 W 的 spec 完全一致。

Rnew 的 O_EXCL 锁：session=`archivefix-rpm-5672ca9cb245414e9b5c8dedf9f983ec`，PID=1734976，
开始 `2026-09-24T15:13:47.385803+08:00`；实验与报告期间独占，收尾回收。
证据：`E/hold_lock.py`、`lock-acquired.json`、`lock-released.json`、`final-cleanup.json`。

| 输入核查 | 本次结果 | 证据 |
| --- | --- | --- |
| R0 指定 RPMS 的 docs/13 22 包 | 22/22 SHA 匹配 | E/rpm-identity.json |
| H 逐包文件类型、模式、SHA、软链接目标 | 17,689 唯一路径，差异 0 | E/baseline-content-check.json、baseline-check.log |
| 321 个多包归属路径 | 各包记录的期望元数据一致 | E/duplicate-owner-metadata.json |
| U 中 225 归档 | 每个 SHA/字节数均与 E28/conversion/summary.json 相符 | E/converted-input-identity.json |

因此复用 U，**没有重新转换 bitcode**。完整内容核查实际读取了包括 debuginfo 在内的大文件，
没有把旧核查结果当成本次核查。R0 只读指定 RPMS、rpm 宏/脚本，以及获准执行的 strip/依赖；
不访问其 BUILD，也不访问已隔离的混合构建根。W/llvm 及其 spec 始终未改。

## 1. 事前资源规则变更

依据用户本次决定，编译的 4 GiB 虚拟地址空间限制不再套用到链接。
这是本次运行前的政策变更；记录为 `E/resource-rule-before-run.json`，不是失败后临时调参。

- 编译：`clang -c` 保留 `prlimit --as=4294967296 --core=0`。
- 链接：不传 `--as`，且入口拒绝父进程已有限 AS 的环境；仍禁 core dump。
- 内存用 systemd 用户 scope 总量控制，`MemorySwapMax=0`。普通离线阶段 cap 为
  `min(18, floor(MemAvailable / GiB) - 4)`；完整构建仍为 18 GiB，MemAvailable<16 GiB 拒绝。
- 唯一因果诊断保留 docs/28 原来的 **12 GiB** cap；其启动时公式计算结果也恰为 12 GiB。
- 保留 nice 15、ionice c3、30 秒宿主 free/loadavg/进程树 RSS、低于 2 GiB available 中止、退出回收。
- 新增每命令 **50 ms** `/proc` 子树采样：VmPeak/VmSize/VmHWM/VmRSS/Threads；原始数据为 `.memory.jsonl`。
  核心诊断另从全部采样中筛出实际 lld；不把虚拟地址空间相加冒充内存需求。
  本次诊断 1,506 次采样，最大实际间隔 0.234618 s（<1 s），见 `E/diagnostic-sample-interval.json`。

实现：[native_archive_commands.py](../tools/native_archive_commands.py)。编译限额、链接无 AS、失败后拒绝继续和采样器回收有正负测试。
外层复用 `build_llvm_x86_64.py` 的 scope/宿主采样/收尾机制，实际入口原文 `E/run_stage.py`。
它的通用日志含 “build/chroot” 字样，不代表离线阶段运行了 GBS。

## 2. B-lld 单次诊断：确认地址空间上限是旧失败原因

从 `E28/consumers/link-b-lld.json` 读取原 `argv`，原 b.o、原 U、原 wrapper、原 121 个库、原输出路径全部不变。
对比检查 `same_argv=true`。只从外层 prlimit 去掉 `--as=4294967296`，保留 cgroup 12 GiB/swap=0。
成功后把新成品从原来未存在的 E28/consumers/b-lld 移到 `E/diagnostic/b-lld`，不覆盖旧证据或输入。
完整命令在 `E/diagnostic/input-command.json`、`link-b-lld.json`；执行脚本 `E/diagnose_b_lld.py`。

| 指标 | 本次实测 |
| --- | --- |
| 退出码 | 0，链接成功 |
| 链接 wall / 外层阶段 wall | 77.81 s / 78.696615 s |
| lld VmPeak / 最大采样 VmSize | 5,343,096 KiB = 5.095573 GiB |
| lld VmHWM / time 最大 RSS | 3,773,956 KiB = 3.599125 GiB；两口径相同 |
| lld Threads 最大值 | 17；没有添加线程参数 |
| lld 被采到的存活区间 | 0.102124–77.752183 s，末尾存在采样间隙 |
| cgroup MemoryPeak / MemoryMax | 3,997,483,008 B / 12,884,901,888 B（12 GiB） |
| memory.events | low/high/max/oom/oom_kill/oom_group_kill 全 0 |
| 宿主最低 MemAvailable | 16,641,945,600 B，30 秒采样最小值 |

按用户预设判据：相同链接命令移除 AS 限制后成功，VmPeak **>4 GiB**，RSS 和 cgroup 峰值明显低于 cap，
因此 docs/28 的失败归因于 **4 GiB RLIMIT_AS**。不需要也没有提高 cgroup cap。
本次 77.81 秒包含输入读盘；它不是性能对照，不与旧 21.06 秒失败时长计算加速比。
证据：`E/diagnostic-summary.json`、`diagnostic/link-b-lld.memory.jsonl`、`diagnostic-scope/memory-summary.json`。

## 3. Tizen 打包 strip 模拟：225/225 PASS

### 3.1 工具身份与实际命令

R0 `usr/lib/rpm/brp-strip-static-archive:7,15–19` 选择 strip，并对每个 ar archive 执行 `$STRIP -g "$f"`。
本轮没有运行整个 brp，也没有写 R0；复制 U 全部 225 个归档后，对 N 每个副本执行：

```bash
<R0>/lib64/ld-linux-x86-64.so.2 \
  --library-path <R0>/usr/lib64:<R0>/lib64 \
  <R0>/usr/bin/strip -g <N>/usr/lib64/<archive>.a
```

实测 `GNU strip (GNU Binutils) 2.43`，strip SHA256：
`ee80ec36060dc467f57a3c7ae7155affbfcd39cec254892cffa45096a9f5e7ec`。
loader、libbfd-2.43.so、libc.so.6、libsframe.so.1 **均从 R0 加载**；--list 和每个文件 SHA 在
`E/stripped/strip-libraries.log`、`strip-runtime-identities.json`。宏脚本原文为 `brp-strip-static-archive-numbered.txt`。

### 3.2 逐归档门禁

[simulate_native_archive_strip.py](../tools/simulate_native_archive_strip.py) 调用已有 `inspect_llvm_archives.py`：
按 ordinal/name/occurrence 核成员数、次序、名称，同名成员不合并；
逐成员读实际 ELF 头确认 ELF64 little-endian、机器 x86_64、ET_REL；拒绝 bitcode/other/thin。
调试节检测包含 `.debug*`、`.zdebug*` 及相关重定位节。
索引必须恰为各成员外部定义符号多重集合，且 strip 前后完整“符号→ordinal/name/occurrence”多重映射相同。
任何失败立即停止，不运行 ranlib 修补或跳过。

| 项目 | 实测 |
| --- | --- |
| strip 退出 0 / 格式错误行 | 225/225 / 0 |
| 成员 | 3,864 个；数量、次序、名字与重复身份全部保持 |
| 输出格式 / 调试节 | 全 x86_64 ET_REL，bitcode=0；调试节 0 |
| 完整索引 | 318,543 条；逐归档前后映射和成员定义符号检查全部 PASS |
| strip 前 / 后总字节 | 6,615,084,040 / 520,479,520 B |
| 复制、strip、校验 wall / 外层阶段 wall | 213.185329 / 214.538489 s |
| cgroup MemoryPeak / cap | 6,935,126,016 B / 12 GiB；包含文件页缓存，不是 strip 单进程 RSS |
| memory.events | 全 0 |

原有 11 个机器码成员分布于 Analysis 6、CodeGen 1、Support 4 个：本轮也经过同一 strip/索引/格式门禁，
全部通过、无调试节；它们没有重新 codegen。逐成员 strip 后 SHA 在 `E/strip-summary.json`。
compiler-rt 45 个归档不在这 225 个转换归档内，本次模拟不动它们，**不能据此宣称新 RPM 的 compiler-rt 验收通过**。

完整 225 行清单、前后 SHA、大小、每次 strip argv/time/采样：`E/stripped/summary.json` 和
`E/stripped/checks/usr/lib64/<archive>.a/{before,after,strip}.json`；附录 A 给出摘要。

## 4. strip 后的完整消费者验证：7/7 PASS

### 4.1 环境与命令入口

每个 C++ 源先独立编译为 .o，再由 clang 驱动链接；链接步骤只输入已存在的 .o。
完整 argv、driver `-###`、stdout/stderr、time 与内存采样均在 `E/consumers/`。
GNU ld 的 driver 展开没有 -flto、-plugin/--plugin；守卫发现这些选项或 cc1 链接子任务即拒绝。
实现：[verify_native_archive_consumers.py](../tools/verify_native_archive_consumers.py)。

| 组成 | 本次实际来源 |
| --- | --- |
| clang / opt / lld / llvm-config | H 解包的 Tizen LLVM 22.1.8；经 L 与 RT 执行，不安装宿主 |
| clang SHA | `3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c` |
| 目标与资源头 | `--target=x86_64-linux-gnu --no-default-config --driver-mode=g++`；H/usr/lib64/clang/22 |
| LLVM/lld 头文件 | H/usr/include |
| C++ 标准库头 | **宿主 GCC 13**：/usr/include/c++/13、/usr/include/x86_64-linux-gnu/c++/13、backward |
| libc 头、crt、libgcc | **宿主** /usr/include、/usr/include/x86_64-linux-gnu、/lib/x86_64-linux-gnu、/usr/lib/gcc/x86_64-linux-gnu/13 |
| LLVM/lld 静态库 | **只用 N/usr/lib64 的 strip 后新库**；临时 prefix/lib64 指向 N，llvm-config --link-static 取参数 |
| GNU ld | **宿主 /usr/bin/ld.bfd**；显式 --ld-path，不经过 g++/collect2 插件路径 |
| libstdc++、glibc、libm、libgcc_s、zlib | **宿主**；实际 loader --list 和 SHA 见 E/consumer-runtime-identities.json |
| libxml2 | **Tizen 固定快照** RT/libxml2.so.16，绝对路径链接、library-path 运行；SHA `0d70127304264bd46387484ed7e566fc5fec96fb9c77de8c06fe0a9e9a0a8034` |

这是明确的宿主 ABI 离线验证，不冒充尚未执行的 Tizen 包内测试。
llvm-config 仍通过 prefix/bin 中同字节 loader 副本查询，避免显式 loader 下的 prefix 识别错误。
代码、依赖解析、头文件搜索原文见 `a.cpp`、`b.cpp`、`shared-main.cpp`、`compile-*.log`、`query-*.txt/json`。

### 4.2 程序、输出与反例

A 解析固定 IR，verifyModule，注册 PassBuilder analyses/proxies，运行默认 O2 module pipeline，再 verify 并打印。
对照是同一路径 input.ll 经 H/usr/bin/opt `-S -O2` 的输出；输入无 triple，A 与 opt 都不创建 TargetMachine，
依据 `llvm/llvm/tools/opt/optdriver.cpp:636–643`。IR 固定输入/输出保存在本轮 consumers 目录。

B 通过 `lld::lldMain` + `lld::elf::link` 在进程内把预编译的 minimal.o 链为 x86_64 ELF，
然后实际执行生成物并核对退出码 37。外层 bfd/lld 两个 B 都完成了内部链接与执行。

| 检查 | 结果与证据 |
| --- | --- |
| A GNU ld | PASS，完整 IR 与 opt 输出一致，E/consumers/run-a-bfd.txt |
| A lld | PASS，完整 IR 与 opt 输出一致，run-a-lld.txt |
| B GNU ld | PASS，库内链接成功，生成物 exit=37，b-bfd-generated-run.json |
| B lld | PASS，库内链接成功，生成物 exit=37，b-lld-generated-run.json |
| A 共享库 | PASS，GNU ld `-shared -z defs -z text`；小主程序 dlopen 并运行，IR 一致，run-shared-a.txt |
| A GNU ld --gc-sections | PASS，运行 IR 一致；47,387,472 B → 28,378,320 B，少 19,009,152 B |
| 未转换 bitcode 反例 | PASS（预期失败），同一 GNU ld 无 LTO/插件链接换用 H，exit=1 |

五份完整文本（expected、A-bfd、A-lld、shared、GC）均 463 B，SHA：
`a4247224bc4e71814e125fc4f88d11d3009314655e00e11ced644dbed5014691`。
B 两个生成物 SHA 均为 `3609167ac2889072dcca787a8cf2cbcdb762c280e55350b797ef02e6842ce789`，均实测 exit=37。
证据：`E/consumer-ir-identities.json`、`consumers/result.json`。
GC 减少体积是本消费者实际删除未使用节区的证据，不是运行性能结论。

反例原文：

```text
/usr/bin/ld.bfd: <H>/usr/lib64/libLLVMPasses.a: error adding symbols: archive has no index; run ranlib to add one
clang-22: error: linker command failed with exit code 1 (use -v to see invocation)
```

反例保留了原 bitcode 包的受损索引，因此观察到的是索引门禁先拒绝；**未把它夸大为消除索引因素后的格式隔离实验**。
本任务要求的“原归档同命令失败”已成立；没有修补原库或额外重跑。

### 4.3 每项资源记录与精度边界

下表 RSS 为 `/usr/bin/time` 的 max RSS（含被等待的子进程）；VmPeak 是 50 ms 子树采样的单进程最大值。
单位均 KiB，不把 VmPeak 与 RSS 混用。单次只有一个样本、只捕获启动器的短命令，目标程序 VmPeak 标 **UNKNOWN**；
原采样值仍完整保存，不用启动器的几百 KiB 冒充实际目标峰值。其运行退出码、输出和 time RSS 均有实测。
0.00 秒是 time 两位小数精度，不代表没有执行。未为补峰值数据重复功能实验。

| 命令记录名 | 阶段 | exit | wall s | time RSS KiB | VmPeak KiB（采样） |
| --- | --- | ---: | ---: | ---: | ---: |
| b-bfd-generated-run | run | 37 | 0.00 | 1884 | UNKNOWN（仅1次采样） |
| b-lld-generated-run | run | 37 | 0.00 | 1884 | UNKNOWN（仅1次采样） |
| compile-a-shared | compile | 0 | 1.93 | 338716 | 418332 |
| compile-a | compile | 0 | 3.73 | 336748 | 418344 |
| compile-b | compile | 0 | 0.29 | 115664 | 175020 |
| compile-minimal | compile | 0 | 0.00 | 4056 | UNKNOWN（仅1次采样） |
| compile-shared-main | compile | 0 | 0.02 | 81540 | UNKNOWN（仅1次采样） |
| link-a-bfd-gc | link | 0 | 2.32 | 314928 | 320388 |
| link-a-bfd | link | 0 | 4.95 | 351348 | 361392 |
| link-a-lld | link | 0 | 0.45 | 301868 | 1464784 |
| link-b-bfd | link | 0 | 6.16 | 530464 | 539400 |
| link-b-lld | link | 0 | 0.47 | 472736 | 1662508 |
| link-libprobe | link | 0 | 3.13 | 355356 | 366340 |
| link-shared-main | link | 0 | 0.04 | 45356 | UNKNOWN（仅1次采样） |
| negative | link | 1 | 0.01 | 45504 | UNKNOWN（仅1次采样） |
| reference-opt | query | 0 | 0.96 | 35792 | 81848 |
| run-a-bfd-gc | run | 0 | 0.00 | 19752 | UNKNOWN（仅1次采样） |
| run-a-bfd | run | 0 | 0.00 | 26664 | UNKNOWN（仅1次采样） |
| run-a-lld | run | 0 | 0.00 | 28072 | UNKNOWN（仅1次采样） |
| run-b-bfd | run | 0 | 0.01 | 31800 | UNKNOWN（仅1次采样） |
| run-b-lld | run | 0 | 0.00 | 35724 | UNKNOWN（仅1次采样） |
| run-shared-a | run | 0 | 0.01 | 31128 | UNKNOWN（仅1次采样） |

消费者 scope wall=26.424932 s，cap=11 GiB（启动 MemAvailable=17,168,551,936 B），
MemoryPeak=1,034,035,200 B；memory.events 全 0。
VmSize/VmHWM/Threads 及逐命令高精度 elapsed_seconds 在 `E/consumer-measurements.json`、每条命令 `.json/.memory.jsonl`；
outer scope 与宿主最小可用内存在 `consumers-scope/memory-summary.json`。

## 5. 隔离 spec 集成与精确认证：已准备，尚未构建验证

只有第一段七项全部通过后，才修改 S。W/llvm 与原 spec 不动。
S 中新增 `packaging/llvm-static-archives-native.py`，Source1005 与 %install 转换均用 `%ifarch x86_64` 限定；
没有改 RPM 宏、CMake/优化参数、工具构建或链接步骤，原 4/4/1 保留。

### 5.1 最小 spec diff 与完整 Source

以下 diff 相对 **W 当前 spec**，不重复带入已存在的三处并发修改：

```diff
diff --git a/packaging/llvm.spec b/packaging/llvm.spec
--- a/packaging/llvm.spec
+++ b/packaging/llvm.spec
@@ -44,6 +44,9 @@
 Source1002: mlgo_arm_model.tar.gz
 Source1003: mlgo_aarch_model.tar.gz
 Source1004: mlgo_x86_model.tar.gz
+%ifarch x86_64
+Source1005: llvm-static-archives-native.py
+%endif

 %{!?mlgo_build_jobs: %define mlgo_build_jobs 4}
 %{!?mlgo_verify_configure_only: %define mlgo_verify_configure_only 0}
@@ -395,6 +398,14 @@
 rm -rf %{buildroot}%{_libdir}/debug/*
 rm -rf %{buildroot}/usr/lib/libear/*
 rm -rf %{buildroot}/usr/lib/libscanbuild/*
+
+
+%ifarch x86_64
+# Native static-devel objects for non-LTO, plugin-free GNU ld consumers.
+# Keep the normal RPM post-processing chain, including strip -g, unchanged.
+python3 %{SOURCE1005} --root "%{buildroot}" --build "$PWD" \
+    --evidence "$PWD/native-archive-conversion" || exit 1
+%endif

 %post -n clang -p /sbin/ldconfig
 %postun -n clang -p /sbin/ldconfig
```

完整 Source 随本提交公开：[llvm_static_archives_source.py](../tools/llvm_static_archives_source.py)，
与 S/packaging/llvm-static-archives-native.py **逐字节一致**。
它内嵌已验证的 archive inspector 与 docs/28 转换器；AST 对照证明 convert、Commands、ir_settings、PIC 检查等核心定义未改。
四 workers，每转换命令 4 GiB AS，后端选项为：

```text
-O3 -ffunction-sections -fdata-sections -funique-section-names
-faddrsig -g -gdwarf-4 -ffp-contract=on
```

PIC/PIE、CPU/features、可见性沿用经核实的 IR；转换 argv 不传 -flto。
转换器选择本次 build/bin/clang-22 与 build/bin/llvm-dis，输出证据到 build/native-archive-conversion。
按 ordinal 保留同名成员；原机器码复制不重新生成；全部转换验证成功后才逐归档回写安装根，
再次核 SHA，并打印 `NATIVE_ARCHIVE_INSTALLED`、`NATIVE_ARCHIVES_BEGIN/END`。
任何转换或复制异常均使 %install 非零退出，无降级。compiler-rt 纯机器码归档不转换，正常 brp strip 后处理保留。
该集成逻辑尚未在一次完整 RPM 构建中执行，不能拿离线 PASS 替代此验证。

| 文件/补丁 | SHA256 |
| --- | --- |
| S/packaging/llvm.spec | `83dc994ab6d7ffe65cdf2bf38dbe027599775ffa71c6614219123856f8be1d2d` |
| Source1005 / tools 中完整副本 | `735f4731c6061638a35dce7daf8e03b5e582da3e16e7d38d2edecc1b852319a8` |
| E/archive-native-conversion.patch（含新增 Source） | `0369cc0fc821ba358346d2f650d5c09abdb0a3d6435fa48ef8db3a60a0b71dd9` |
| E/trial-head.diff（含原三处并发修改） | `58078a578ec4473549cb999f0065ccc0b6ad984511b3bca5cc13abaa75629636` |

`git -C W/llvm apply --check E/archive-native-conversion.patch` 返回 0，未应用到 W；完整输出 `E/patch-apply-check.json`。
S Source 使用 intent-to-add 进入完整 diff；没有向 LLVM/Gerrit 提交。

### 5.2 认证入口

`build_llvm_x86_64.py --certify-fingerprint archive-fix-trial` 只接受：

- 固定 S 路径、archive-fix-trial 分支、f111162e HEAD；精确 spec/Source 两文件变更清单。
- 上表 spec、Source、HEAD diff 和相对 W patch 的精确 SHA；其他文件或字节变化拒绝。
- Rnew 内只有匹配 session 的活 PID 独占锁；允许这个“只有锁”的新根，不允许复用已有构建内容。
- 除新增包装文件与对应 spec 身份外，所有配置字段与 docs/13 全静态指纹相同；
  CMake 参数表逐项完全相同，包含 Release、ThinLTO、O3、静态 LLVM、lld、断言 OFF、4/4/1。
- 18 GiB、MemorySwapMax=0、GBS threads=1、debuginfo -j4、原 900 秒 CMake 门禁及采样/回收机制不变。

固定清单：[llvm_archive_fix_trial_fingerprint.json](../tools/llvm_archive_fix_trial_fingerprint.json)。
7 项新测试覆盖放行、各身份字段错误、错误路径/HEAD/分支/清单、spec/Source/diff 变化、锁归属和旧根拒绝、CMake 契约及打包 Source 一致性。
14 项原构建门禁测试也通过；它们只启动模拟 Python 子进程，没有执行 GBS。

## 6. 唯一完整构建入口与停止结果

实际调用（完整 argv 另存 `E/full-build-attempt.json`）：

```bash
python3 tools/build_llvm_x86_64.py --run \
  --source <S> --buildroot <Rnew> --log-dir <E>/full-build \
  --certify-fingerprint archive-fix-trial \
  --exclusive-lock-session archivefix-rpm-5672ca9cb245414e9b5c8dedf9f983ec
```

原始资源检查输出摘录：

```text
2026-09-24T15:35:18+08:00 $ nproc
2026-09-24T15:35:18+08:00 20
[exit=0]
2026-09-24T15:35:18+08:00 $ free -g
2026-09-24T15:35:18+08:00                total        used        free      shared  buff/cache   available
Mem:              30          14           1           0          15          15
Swap:              3           3           0
[exit=0]
2026-09-24T15:35:18+08:00 $ df -h /home/linhao/Toolchain/development/llvm-optimize/temp
2026-09-24T15:35:18+08:00 Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       1.8T  1.3T  507G  71% /home
[exit=0]
2026-09-24T15:35:18+08:00 $ nproc
2026-09-24T15:35:18+08:00 20
[exit=0]
2026-09-24T15:35:18+08:00 STOPPED MemAvailable 15.929 GiB < 16 GiB
```

入口 exit=2。停止发生在检查仓库 URL、source 认证和 systemd 启动 **之前**：
本次新认证有测试与只读身份检查通过，但没有伪称生产入口已走完全部预检。
**唯一一次入口调用 ≠ 一次 GBS 构建；本次实际 GBS 启动次数是 0。**
没有等待、清理用户进程、放宽 16 GiB 门槛或重新调用 --run。
门禁只保存三位小数的 MemAvailable；该判定瞬间更精确的字节数为 UNKNOWN，不能拿事后 meminfo 冒充。

| 第二段剩余验收 | 结果 |
| --- | --- |
| LLVM 全新构建 / CMakeCache 校验 / 构建峰值和耗时 | NOT RUN；没有 CMakeCache，无构建峰值/耗时 |
| %install 转换实测 | NOT RUN；只有离线原理验证，没有新构建树转换日志 |
| 22 新 RPM inventory / temp/toolchain-archivefix | 未产出 |
| 新 RPM 全 native、零 debug、完整索引、成员顺序/每函数一段 | NOT RUN |
| 新 compiler-rt 与基线逐成员/索引一致 | NOT RUN |
| 新包 brp-strip-static-archive 照常且零格式错误、其余 brp 链 | NOT RUN；模拟的 225 次 strip 不能替代完整后处理 |
| 新旧 RPM 逐文件清单/SHA 全差异分类 | NOT RUN |
| 新 RPM 全套消费者 | NOT RUN |
| 两个新 Tizen 测试包（bfd/lld，包内 A+B 和 %check） | 均 NOT RUN，构建 0 次 |
| 新 RPM clang-22/lld/llvm-ar SHA 对照 | NOT RUN |

**结论：离线转换＋真实 Tizen strip＋宿主消费者兼容性已通过；spec 补丁与认证入口准备完成，完整 RPM/Tizen 验收仍未闭合。**
恢复工作需要资源满足既有构建准入，以及用户对下一次尝试的决定；本任务不自动重试。
修法准备补丁的路径和 SHA 见 §5；“可以评审补丁”不等于“可以发货/提交 Gerrit”。

## 7. 测试、保护和收尾

| 测试脚本 | 本次结果 |
| --- | --- |
| test_native_archive_commands.py | 3 PASS：compile/link AS 正负、实际限额、失败取消和 sampler 回收 |
| test_simulate_native_archive_strip.py | 2 PASS：完整映射/重复成员、顺序/符号/调试节/格式/索引损坏负例 |
| test_verify_native_archive_consumers.py | 3 PASS：对象链接、loader/cc1 回归、LTO/plugin 拒绝 |
| test_archive_fix_trial.py | 7 PASS：新认证精确绑定与 Source 一致性 |
| test_build_llvm_x86_64.py | 14 PASS：原容量/CMake/失败/回收路径 |

共 29 项功能测试；日志为 `E/{resource,strip,consumer,archive-trial,build-guard}-tests.log`。
三阶段 scope 均 inactive/dead，采样器和 reader 均回收；独占锁收尾删除。
`E/preservation-check.json` 证明 W/spec、docs/25–28 未变；S 的改后文件保持已登记指纹。
新根没有 GBS 产物，已准备的 S diff 不自动撤销；没有修改源 C++/CMake 文件或 RPM 宏。

自检：

1. 链接 AS 是否按事前新规修正？**是**；诊断原 argv 相同、12 GiB/swap0 不变，成功且 VmPeak>4 GiB。
2. 225 个归档 strip、完整索引、原11机器码是否通过？**是**；原始逐归档证据保留，未修索引重试。
3. 离线消费者是否全部通过？**是**；短命令 VmPeak 未捕获处明确 UNKNOWN，不编造。
4. 是否完成新 RPM 与 Tizen 环境验收？**否**；入口因 available<16 GiB 停止，未启动 GBS。
5. 是否修改 W/llvm/spec 或旧 docs/25–28？**否**；仅获准修改 S/spec、新增 S Source。
6. 是否运行 BOLT、PGO、性能校准、Chromium 或推 Gerrit？**否**。
7. 是否发生失败后调参/重试？**否**；第一段诊断是用户本次明确授权，完整构建准入失败后停止。
8. STATUS 是否同 commit 更新？**是**；本提交用 `git log -1 -- docs/29_static_archive_native_conversion_v3.md` 定位。

主要原始证据索引：

- 前置：precheck.json、rpm-identity.json、baseline-content-check.json、duplicate-owner-metadata.json、converted-input-identity.json。
- 规则/诊断：resource-rule-before-run.json、diagnostic-summary.json、diagnostic/、diagnostic-scope/。
- strip：strip-summary.json、strip-runtime-identities.json、stripped/summary.json、stripped/checks/、strip-scope/。
- 消费者：consumers/ 全源码、完整 compile/link/run argv、driver 原文、输出/time/采样；consumer-measurements.json、consumer-ir-identities.json、consumer-runtime-identities.json、consumers-scope/。
- 补丁/构建：archive-native-conversion.patch、trial-head.diff、patch-apply-check.json、full-build-attempt.json、full-build-entry.log、full-build/stopped.json。
- 收尾：preservation-check.json、scope-cleanup.json、lock-released.json、final-cleanup.json；Git 推送/核对另存 git-publication.json、publication-verification.json。

## 附录 A：225 个 strip 结果摘要

所有行均 PASS。完整成员和符号映射、SHA/错误日志位于 §3 指定的逐归档 JSON；不是新 RPM 清单。

| 归档（usr/lib64） | 成员数 | strip 前 B | strip 后 B | 索引条目 |
| --- | ---: | ---: | ---: | ---: |
| libLLVMAArch64AsmParser.a | 1 | 6893338 | 1742162 | 62 |
| libLLVMAArch64CodeGen.a | 63 | 122389448 | 11915248 | 4339 |
| libLLVMAArch64Desc.a | 12 | 12139650 | 4055714 | 658 |
| libLLVMAArch64Disassembler.a | 2 | 2891522 | 368722 | 24 |
| libLLVMAArch64Info.a | 1 | 109418 | 16322 | 10 |
| libLLVMAArch64Utils.a | 1 | 1275944 | 380384 | 62 |
| libLLVMABI.a | 1 | 27106 | 3066 | 1 |
| libLLVMARMAsmParser.a | 1 | 5281016 | 959064 | 76 |
| libLLVMARMCodeGen.a | 49 | 75145022 | 6630374 | 3410 |
| libLLVMARMDesc.a | 13 | 8057644 | 1860492 | 434 |
| libLLVMARMDisassembler.a | 1 | 3899352 | 510424 | 8 |
| libLLVMARMInfo.a | 1 | 106986 | 13722 | 10 |
| libLLVMARMUtils.a | 1 | 161576 | 23784 | 10 |
| libLLVMAggressiveInstCombine.a | 2 | 4142074 | 231802 | 110 |
| libLLVMAnalysis.a | 131 | 167649884 | 13390372 | 9363 |
| libLLVMAsmParser.a | 4 | 13656758 | 1176166 | 658 |
| libLLVMAsmPrinter.a | 27 | 37204402 | 2398674 | 1956 |
| libLLVMBPFAsmParser.a | 1 | 618142 | 59702 | 28 |
| libLLVMBPFCodeGen.a | 26 | 22685390 | 1796830 | 1688 |
| libLLVMBPFDesc.a | 5 | 982304 | 146768 | 110 |
| libLLVMBPFDisassembler.a | 1 | 297004 | 21540 | 4 |
| libLLVMBPFInfo.a | 1 | 101344 | 11216 | 7 |
| libLLVMBinaryFormat.a | 14 | 3840472 | 605520 | 247 |
| libLLVMBitReader.a | 5 | 14377108 | 977604 | 506 |
| libLLVMBitWriter.a | 4 | 12335882 | 639434 | 243 |
| libLLVMBitstreamReader.a | 1 | 867898 | 58602 | 48 |
| libLLVMCAS.a | 15 | 9372568 | 608080 | 427 |
| libLLVMCFGuard.a | 1 | 887178 | 35354 | 18 |
| libLLVMCFIVerify.a | 2 | 2540524 | 154268 | 151 |
| libLLVMCGData.a | 7 | 6053066 | 372490 | 296 |
| libLLVMCodeGen.a | 238 | 309230198 | 19541798 | 14191 |
| libLLVMCodeGenTypes.a | 1 | 121410 | 12298 | 6 |
| libLLVMCore.a | 80 | 108913924 | 9558596 | 7628 |
| libLLVMCoroutines.a | 11 | 15439752 | 683624 | 339 |
| libLLVMCoverage.a | 3 | 9054598 | 566054 | 214 |
| libLLVMDTLTO.a | 1 | 547072 | 36064 | 35 |
| libLLVMDWARFCFIChecker.a | 4 | 1782882 | 123922 | 122 |
| libLLVMDWARFLinker.a | 2 | 127072 | 9560 | 3 |
| libLLVMDWARFLinkerClassic.a | 4 | 7887016 | 516304 | 416 |
| libLLVMDWARFLinkerParallel.a | 11 | 18205574 | 1065438 | 819 |
| libLLVMDWP.a | 2 | 1740564 | 125060 | 68 |
| libLLVMDebugInfoBTF.a | 2 | 1608904 | 120664 | 65 |
| libLLVMDebugInfoCodeView.a | 40 | 19514906 | 1995394 | 1772 |
| libLLVMDebugInfoDWARF.a | 29 | 29232472 | 2395576 | 1908 |
| libLLVMDebugInfoDWARFLowLevel.a | 3 | 1363484 | 104652 | 60 |
| libLLVMDebugInfoGSYM.a | 14 | 10543558 | 692158 | 504 |
| libLLVMDebugInfoLogicalView.a | 19 | 31377046 | 2618382 | 2322 |
| libLLVMDebugInfoMSF.a | 4 | 2216994 | 156610 | 173 |
| libLLVMDebugInfoPDB.a | 93 | 36522520 | 3200056 | 3174 |
| libLLVMDebuginfod.a | 4 | 2591862 | 200574 | 197 |
| libLLVMDemangle.a | 6 | 3726450 | 812002 | 767 |
| libLLVMDiff.a | 3 | 1715016 | 111336 | 82 |
| libLLVMDlltoolDriver.a | 1 | 807748 | 48860 | 15 |
| libLLVMExecutionEngine.a | 5 | 3937996 | 285540 | 265 |
| libLLVMExegesis.a | 25 | 18878154 | 1011322 | 822 |
| libLLVMExegesisAArch64.a | 1 | 1355912 | 73584 | 37 |
| libLLVMExegesisX86.a | 2 | 3200732 | 207316 | 73 |
| libLLVMExtensions.a | 1 | 28162 | 3698 | 2 |
| libLLVMFileCheck.a | 1 | 3454862 | 280686 | 239 |
| libLLVMFrontendAtomic.a | 1 | 691416 | 31272 | 22 |
| libLLVMFrontendDirective.a | 1 | 58204 | 3444 | 1 |
| libLLVMFrontendDriver.a | 1 | 106746 | 5922 | 4 |
| libLLVMFrontendHLSL.a | 6 | 2536698 | 179330 | 129 |
| libLLVMFrontendOffloading.a | 3 | 3934314 | 185850 | 106 |
| libLLVMFrontendOpenACC.a | 1 | 269846 | 43030 | 11 |
| libLLVMFrontendOpenMP.a | 4 | 13240828 | 1563044 | 571 |
| libLLVMFuzzMutate.a | 4 | 5403798 | 397822 | 210 |
| libLLVMFuzzerCLI.a | 1 | 455194 | 27074 | 8 |
| libLLVMGlobalISel.a | 30 | 38998706 | 3399690 | 2127 |
| libLLVMHipStdPar.a | 1 | 1294444 | 61500 | 18 |
| libLLVMIRPrinter.a | 1 | 214970 | 11866 | 12 |
| libLLVMIRReader.a | 1 | 625872 | 31312 | 13 |
| libLLVMInstCombine.a | 15 | 49160210 | 4068114 | 2421 |
| libLLVMInstrumentation.a | 28 | 60554610 | 3946642 | 2005 |
| libLLVMInterfaceStub.a | 3 | 3377390 | 209486 | 116 |
| libLLVMInterpreter.a | 3 | 4020704 | 329520 | 166 |
| libLLVMJITLink.a | 35 | 52323618 | 3352730 | 2507 |
| libLLVMLTO.a | 6 | 22542308 | 1237932 | 893 |
| libLLVMLibDriver.a | 1 | 1183798 | 74750 | 25 |
| libLLVMLineEditor.a | 1 | 309326 | 17446 | 26 |
| libLLVMLinker.a | 2 | 4126960 | 206816 | 109 |
| libLLVMMC.a | 70 | 32792224 | 2718864 | 2012 |
| libLLVMMCA.a | 24 | 6776938 | 443898 | 516 |
| libLLVMMCDisassembler.a | 5 | 857968 | 55784 | 59 |
| libLLVMMCJIT.a | 1 | 1364980 | 80676 | 83 |
| libLLVMMCParser.a | 13 | 12056802 | 1143994 | 305 |
| libLLVMMIRParser.a | 3 | 8302686 | 606614 | 315 |
| libLLVMObjCARCOpts.a | 8 | 6594226 | 287386 | 144 |
| libLLVMObjCopy.a | 26 | 22489410 | 1544722 | 1124 |
| libLLVMObject.a | 36 | 42919506 | 3704258 | 2665 |
| libLLVMObjectYAML.a | 29 | 59168528 | 5086344 | 3619 |
| libLLVMOptDriver.a | 2 | 8067228 | 644396 | 572 |
| libLLVMOption.a | 4 | 2339734 | 166502 | 128 |
| libLLVMOrcDebugging.a | 7 | 8593618 | 456970 | 410 |
| libLLVMOrcJIT.a | 57 | 102092560 | 6710344 | 5160 |
| libLLVMOrcShared.a | 7 | 1292968 | 119424 | 160 |
| libLLVMOrcTargetProcess.a | 15 | 11955410 | 727810 | 551 |
| libLLVMPasses.a | 6 | 56112162 | 9491226 | 9766 |
| libLLVMPlugins.a | 1 | 160254 | 6758 | 2 |
| libLLVMProfileData.a | 21 | 44655670 | 3314558 | 2560 |
| libLLVMRemarks.a | 11 | 6221326 | 413214 | 419 |
| libLLVMRuntimeDyld.a | 8 | 11263406 | 1144430 | 921 |
| libLLVMSandboxIR.a | 15 | 11682580 | 1180332 | 1674 |
| libLLVMScalarOpts.a | 81 | 152741868 | 8132348 | 4116 |
| libLLVMSelectionDAG.a | 26 | 78634320 | 8040352 | 3756 |
| libLLVMSupport.a | 179 | 57661498 | 5833978 | 4993 |
| libLLVMSupportLSP.a | 3 | 3732054 | 324086 | 251 |
| libLLVMSymbolize.a | 5 | 6074076 | 444100 | 332 |
| libLLVMTableGen.a | 14 | 15164270 | 1225134 | 1073 |
| libLLVMTableGenBasic.a | 13 | 12185040 | 935768 | 361 |
| libLLVMTableGenCommon.a | 23 | 36407104 | 2545648 | 1686 |
| libLLVMTarget.a | 5 | 1816770 | 142370 | 189 |
| libLLVMTargetParser.a | 15 | 7853802 | 942130 | 364 |
| libLLVMTelemetry.a | 1 | 293446 | 13886 | 17 |
| libLLVMTextAPI.a | 15 | 12953402 | 810626 | 509 |
| libLLVMTextAPIBinaryReader.a | 1 | 1722358 | 88630 | 52 |
| libLLVMTransformUtils.a | 94 | 117722746 | 6398042 | 3562 |
| libLLVMVectorize.a | 33 | 109954874 | 7772154 | 4812 |
| libLLVMWindowsDriver.a | 1 | 449310 | 41470 | 14 |
| libLLVMWindowsManifest.a | 1 | 461204 | 34820 | 27 |
| libLLVMX86AsmParser.a | 1 | 4426026 | 1095794 | 80 |
| libLLVMX86CodeGen.a | 66 | 155716736 | 12464320 | 4564 |
| libLLVMX86Desc.a | 16 | 17489566 | 4280134 | 2278 |
| libLLVMX86Disassembler.a | 1 | 4350188 | 2938884 | 4 |
| libLLVMX86Info.a | 1 | 98228 | 9060 | 6 |
| libLLVMX86TargetMCA.a | 1 | 162210 | 11466 | 14 |
| libLLVMXRay.a | 14 | 6226342 | 443518 | 438 |
| libLLVMipo.a | 45 | 143953740 | 9688340 | 5246 |
| libarcher_static.a | 1 | 902270 | 65814 | 9 |
| libclangAPINotes.a | 5 | 13291554 | 955082 | 440 |
| libclangAST.a | 114 | 310997140 | 34407772 | 26686 |
| libclangASTMatchers.a | 3 | 19946726 | 1760054 | 494 |
| libclangAnalysis.a | 31 | 54280024 | 4301720 | 2344 |
| libclangAnalysisFlowSensitive.a | 18 | 22779134 | 1557038 | 885 |
| libclangAnalysisFlowSensitiveModels.a | 3 | 16578484 | 1582708 | 1246 |
| libclangAnalysisLifetimeSafety.a | 10 | 13245156 | 988892 | 307 |
| libclangAnalysisScalable.a | 4 | 1076572 | 50116 | 40 |
| libclangApplyReplacements.a | 1 | 2258704 | 165080 | 117 |
| libclangBasic.a | 73 | 53439930 | 9264154 | 6167 |
| libclangChangeNamespace.a | 1 | 7388962 | 669618 | 605 |
| libclangCodeGen.a | 101 | 259333370 | 20275986 | 7734 |
| libclangCrossTU.a | 1 | 2107986 | 128650 | 106 |
| libclangDaemon.a | 82 | 211512204 | 19114804 | 7271 |
| libclangDaemonTweaks.a | 20 | 45926080 | 3619544 | 512 |
| libclangDependencyScanning.a | 7 | 9811016 | 615752 | 446 |
| libclangDirectoryWatcher.a | 2 | 850084 | 56364 | 32 |
| libclangDoc.a | 11 | 33777900 | 3184508 | 1972 |
| libclangDocSupport.a | 2 | 471418 | 29570 | 10 |
| libclangDriver.a | 76 | 102978706 | 8290106 | 5935 |
| libclangDynamicASTMatchers.a | 5 | 66575532 | 7166092 | 6495 |
| libclangEdit.a | 3 | 1967996 | 117660 | 75 |
| libclangExtractAPI.a | 6 | 23206096 | 2535024 | 1241 |
| libclangFormat.a | 23 | 25745424 | 2113352 | 1168 |
| libclangFrontend.a | 32 | 75408826 | 6228970 | 2631 |
| libclangFrontendTool.a | 1 | 1185088 | 31352 | 14 |
| libclangHandleCXX.a | 1 | 612292 | 36604 | 36 |
| libclangHandleLLVM.a | 1 | 1647782 | 78854 | 27 |
| libclangIncludeCleaner.a | 8 | 13062746 | 1015506 | 282 |
| libclangIncludeFixer.a | 6 | 4585712 | 245816 | 164 |
| libclangIncludeFixerPlugin.a | 1 | 957700 | 108468 | 128 |
| libclangIndex.a | 9 | 18512482 | 1387730 | 265 |
| libclangIndexSerialization.a | 1 | 407702 | 18422 | 15 |
| libclangInstallAPI.a | 8 | 11225958 | 1033678 | 710 |
| libclangInterpreter.a | 10 | 11999338 | 529546 | 478 |
| libclangLex.a | 25 | 31194110 | 2314974 | 1497 |
| libclangMove.a | 2 | 7695100 | 472108 | 380 |
| libclangOptions.a | 2 | 1441206 | 625062 | 24 |
| libclangParse.a | 18 | 39277850 | 2882506 | 1358 |
| libclangQuery.a | 2 | 6763448 | 409384 | 325 |
| libclangReorderFields.a | 2 | 4465864 | 226672 | 155 |
| libclangRewrite.a | 3 | 1797478 | 118566 | 79 |
| libclangRewriteFrontend.a | 8 | 3774930 | 256874 | 241 |
| libclangSema.a | 86 | 401026782 | 33990462 | 10187 |
| libclangSerialization.a | 17 | 73419922 | 4663218 | 3164 |
| libclangStaticAnalyzerCheckers.a | 134 | 203611274 | 14270514 | 6526 |
| libclangStaticAnalyzerCore.a | 49 | 76933338 | 5246666 | 3639 |
| libclangStaticAnalyzerFrontend.a | 7 | 7500860 | 731524 | 225 |
| libclangSupport.a | 1 | 979584 | 91616 | 47 |
| libclangTidy.a | 9 | 16967812 | 900860 | 650 |
| libclangTidyAbseilModule.a | 22 | 54966470 | 2815934 | 2993 |
| libclangTidyAlteraModule.a | 6 | 12572560 | 450712 | 485 |
| libclangTidyAndroidModule.a | 17 | 29965152 | 931440 | 1148 |
| libclangTidyBoostModule.a | 3 | 5990184 | 207152 | 171 |
| libclangTidyBugproneModule.a | 105 | 292228194 | 17213274 | 15809 |
| libclangTidyCERTModule.a | 1 | 2834826 | 170402 | 135 |
| libclangTidyConcurrencyModule.a | 3 | 5142566 | 131750 | 113 |
| libclangTidyCppCoreGuidelinesModule.a | 32 | 75533126 | 3756102 | 3977 |
| libclangTidyCustomModule.a | 2 | 3709432 | 67776 | 43 |
| libclangTidyDarwinModule.a | 3 | 4917030 | 100326 | 110 |
| libclangTidyFuchsiaModule.a | 8 | 13671956 | 328524 | 355 |
| libclangTidyGoogleModule.a | 16 | 32539456 | 1210536 | 1304 |
| libclangTidyHICPPModule.a | 6 | 12378282 | 496474 | 522 |
| libclangTidyLLVMLibcModule.a | 5 | 8629272 | 184064 | 205 |
| libclangTidyLLVMModule.a | 9 | 19647680 | 792136 | 795 |
| libclangTidyLinuxKernelModule.a | 2 | 3409660 | 70180 | 72 |
| libclangTidyMPIModule.a | 3 | 5366690 | 99922 | 64 |
| libclangTidyMain.a | 1 | 1820940 | 176340 | 109 |
| libclangTidyMiscModule.a | 28 | 73489072 | 4140776 | 3325 |
| libclangTidyModernizeModule.a | 50 | 183027596 | 13976164 | 10328 |
| libclangTidyObjCModule.a | 10 | 18272696 | 563776 | 606 |
| libclangTidyOpenMPModule.a | 3 | 5262686 | 119566 | 120 |
| libclangTidyPerformanceModule.a | 21 | 52598424 | 2812856 | 3052 |
| libclangTidyPlugin.a | 1 | 989446 | 48382 | 31 |
| libclangTidyPortabilityModule.a | 6 | 11269716 | 371140 | 410 |
| libclangTidyReadabilityModule.a | 59 | 170138912 | 9669584 | 7593 |
| libclangTidyUtils.a | 23 | 39993608 | 1910992 | 1224 |
| libclangTidyZirconModule.a | 1 | 1502138 | 14370 | 7 |
| libclangTooling.a | 17 | 15460956 | 924644 | 731 |
| libclangToolingASTDiff.a | 1 | 6879038 | 388422 | 84 |
| libclangToolingCore.a | 2 | 1996790 | 126566 | 103 |
| libclangToolingInclusions.a | 3 | 1652280 | 97400 | 55 |
| libclangToolingInclusionsStdlib.a | 1 | 1611900 | 715532 | 30 |
| libclangToolingRefactoring.a | 12 | 39499616 | 3880656 | 383 |
| libclangToolingSyntax.a | 8 | 13354140 | 838892 | 304 |
| libclangTransformer.a | 7 | 13771252 | 520588 | 266 |
| libclangdMain.a | 2 | 8314068 | 776780 | 676 |
| libclangdRemoteIndex.a | 1 | 103998 | 5134 | 2 |
| libclangdSupport.a | 16 | 5858298 | 449106 | 405 |
| libfindAllSymbols.a | 8 | 8924516 | 579956 | 493 |
| liblldCOFF.a | 18 | 34231348 | 2945532 | 1792 |
| liblldCommon.a | 13 | 5906708 | 449140 | 341 |
| liblldELF.a | 41 | 90489890 | 7813490 | 4021 |
| liblldMachO.a | 30 | 37908310 | 2915470 | 2217 |
| liblldMinGW.a | 1 | 1055272 | 98368 | 13 |
| liblldWasm.a | 14 | 16736056 | 1380600 | 1246 |
