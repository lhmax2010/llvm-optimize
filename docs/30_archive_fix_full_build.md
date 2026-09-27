# 归档修复：构建根环境预检与一次完整构建

日期：2026-09-27。起点提交 `262480a7a03592c9ab39c8f184d7a97751cb2ea6`。
docs/25–29 保留不动。本文只登记本次新证据；docs/29 的离线 PASS 不代替新 RPM 验收。

**结果：PASS。** 一次完整构建产出22 RPM，新包全部归档门禁、七项宿主消费者、
Tizen bfd/lld 两次A+B包内验收全部通过；17,689路径中非归档文件差异0。
候选修法具备x86_64独立评审提交依据，尚未推Gerrit。

## 0. 范围、路径与独占

| 缩写 | 绝对路径或展开 |
| --- | --- |
| W | `/home/linhao/Toolchain/development/llvm-optimize` |
| E | `W/temp/archive-fix-full-build-20260927`，本次全部原始输出 |
| S | `W/temp/llvm-archivefix-trial`，分支 `archive-fix-trial` |
| Rnew | `W/temp/gbs-root-x86_64-archivefix` |
| R | `Rnew/local/BUILD-ROOTS/scratch.x86_64.0`，本次全新构建实例 |
| B | `R/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build`，本次新构建树 |
| R0 | `W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0` |
| H | `W/temp/archive-index-fix-rpm-20260923/baseline-rpm-extract`，旧 22 RPM 内容 |
| E28 | `W/temp/static-native-conversion-v2-20260924` |
| E29 | `W/temp/static-native-conversion-v3-20260924` |
| RT | `W/temp/toolchain-runtime-baseline/libxml2/usr/lib64` |

初始主仓库 status 为空，没有其他会话的 GBS/rpmbuild/ninja/lld/llvm-bolt 进程。
S 的 HEAD 是 `f111162e94aa48ed367c9d2c039456c70e7160ae`；spec 与 Source 初始 SHA 均与 docs/29 §5.1 相符。
这次 S 已包含 docs/29 获准的转换 Source/spec，不再套用更早“只有三处并发改动”的旧前提。
Rnew 独占锁的会话为 `archivefix-rpm-a04c65b4b09a4ad19da2d4016d68ad01`，PID 31306，
开始 `2026-09-27T16:29:57.818498+08:00`；持有至任务收尾。证据：`E/precheck.json`、`lock-acquired.json`。

R0 的 22 RPM SHA **22/22 一致**；H 的 **17,689 唯一路径**按 RPM 文件类型、模式、摘要、软链接目标复核，差异 0；
321 个多包归属路径的元数据一致；额外非目录文件 0。证据：`rpm-identity.json`、`baseline-content-check.json`、
`baseline-extra-check.json`。R0 只读指定 RPMS 与 `/usr/lib/rpm`，没有读取旧 BUILD，没有接触隔离的旧混合根。
W/llvm/spec 原始 SHA 为 `95887b2d060b38d5ef8f56936f7481a03d131f9d26432180a68e02ec95f0dda5`。

## 1. 构建根环境预检

原日志 temp/baseline-build-20260917/build.log:339–458 安装 120 包；完整版本与快照 checksum 见 installed-packages.json。
原 %install 日志 temp/baseline-resume-20260917/run/build.log:2107–2120，cwd=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build。
隔离 spec:369–370 的 cd build 后没有再次 cd，因此 --build "$PWD" 对应该目录；Source:487 定位 bin/clang-22 与 bin/llvm-dis。
新编工具没有指向旧 BUILD 或宿主安装，原安装日志:3759、5098 也确认两个目标被构建/安装。

| 依赖 | 实际情况与证据 | 处理 |
| --- | --- | --- |
| python3 | python3/python3-base/libpython3_141_0 3.14.2-1.6；日志:357、405、431–432；filelists 覆盖所有非内建模块 | 满足 |
| hashlib.file_digest | Python >=3.11；文件以阻塞 rb 打开；[官方说明](https://docs.python.org/3/library/hashlib.html#hashlib.file_digest) | 3.14.2 满足，不必改摘要 |
| str.removesuffix、Path.is_relative_to、os.waitstatus_to_exitcode | >=3.9；[字符串](https://docs.python.org/3/library/stdtypes.html#str.removesuffix)、[pathlib](https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.is_relative_to)、[os](https://docs.python.org/3/library/os.html#os.waitstatus_to_exitcode) | 满足 |
| pathlib Path/open/resolve/relative_to/rglob/is_symlink/exists/unlink/with_suffix | Path >=3.4；read_bytes/write_bytes/write_text 和 mkdir exist_ok >=3.5；默认非 strict resolve >=3.6 | 满足 |
| concurrent.futures ThreadPoolExecutor、submit、wait FIRST_COMPLETED、Future.result/cancel、上下文回收 | >=3.2；文件在 python3-base；[官方](https://docs.python.org/3/library/concurrent.futures.html) | 满足 |
| subprocess.Popen start_new_session | >=3.2；stdout/stderr 重定向；[官方](https://docs.python.org/3/library/subprocess.html#subprocess.Popen) | 满足；无 threaded preexec_fn |
| os.wait4、killpg、signal.signal、SIGTERM/SIGINT | Python 3.0 Unix 已有；wait4 EINTR 自动重试 >=3.5；[官方](https://docs.python.org/3/library/os.html#os.wait4) | Linux 构建根满足；wait4 取指定 child 资源，替代 GNU time |
| time.monotonic / time.time | monotonic >=3.3，time 内建 | 满足 |
| collections.Counter | >=3.1，完整符号多重集合对照 | 满足 |
| re.search/findall/sub、shlex.split、struct.unpack_from/calcsize、json.dumps、hashlib.sha256/hexdigest | Python 3.0 已有；re.fullmatch >=3.4 | 满足 |
| mmap ACCESS_READ / 上下文 | mmap 已有；with mmap >=3.2；成员头 offset 检查 | 满足 |
| threading.Event/Lock 上下文及 set/is_set、os 与文件 I/O、shutil.copyfile | Python 3.0 已有 | 满足 |
| argparse ArgumentParser/add_argument/parse_args/error | >=3.2 标准库 | 满足 |
| int.from_bytes、bytes.hex、surrogateescape、f-string | 分别 >=3.2 / 3.5 / 3.1 / 3.6 | 满足 |
| 其他内建容器/迭代/字符串/数值运算 | Python 3.0；所有实际 API 名称及行号见 source-api-inventory.json | 满足；Source 总体最低为 3.11 |
| /usr/bin/time（原 Source） | 原 120 包无 time/toybox-symlinks-full；固定仓库只有 toybox-symlinks-full 提供该路径，且该包未安装 | 不满足；移除调用，用 os.wait4 + time.monotonic，无新 BuildRequires |
| /usr/bin/prlimit | util-linux 2.41.2-1.4；日志:420，metadata/filelists 提供此文件 | 满足；4 GiB AS、core=0 不变 |
| /usr/bin/ar | binutils 2.43-1.9；日志:395；metadata/filelists 提供此文件 | 满足；qcDS / sD 不变 |
| build/bin/clang-22、build/bin/llvm-dis | 当前构建产物；原日志:3759、5098 | 路径满足；新产物实际运行由完整构建验证 |
| 编译器动态运行库 | glibc 2.40-1.10、libstdc++ 14.2.0-1.10、libxml2 2.15.1-1.7、zlib 1.3.1-1.9 等在 120 包中；配方静态 LLVM | 以已成功 baseline 相同编译/环境指纹为依据；新 ELF 仍需实际执行 |

文件提供者和版本证据：dependency-metadata.json、external-providers.json、dependency-filelists.json、python-module-providers.json。
filelists 从固定 Base URL 获取，压缩与解压 SHA 均与归档 repomd.xml 一致；记录 filelists-fetch.json。
Source 没有 shell 管道或隐式调用 strip/find/readelf/nm；外部调用闭包为 prlimit + clang-22/llvm-dis/ar，exec 的库依赖不新增安装。
此处只做源代码/日志/元数据预检，未到 R0 执行 Python、查询 rpmdb 或读取 BUILD。

### 1.1 唯一依赖修正：移除 GNU time

原 Source 依赖 `/usr/bin/time -f ...`，原 120 包未提供此程序，不能把宿主离线成功外推为构建根可运行。
这次改为 `time.monotonic()` 计 wall，`os.wait4(child.pid, 0)` 获取该子进程 user/sys/max RSS；
Linux 的 `ru_maxrss` 以 KiB 记录。四个转换 worker 各等待自己的 child，不用全局累计值代替单成员峰值。
仍通过 `/usr/bin/prlimit --as=4294967296 --core=0 --` 启动转换命令，退出失败仍取消后续任务并回收进程组。
没有 threaded `preexec_fn`，没有新增 BuildRequires，没有修改 bitcode 后端选项、归档规则、spec 或 RPM 宏。

实现是 `tools/llvm_static_archives_source.py` 与 S/packaging/llvm-static-archives-native.py 的同字节副本。
完整 48 行环境修正 diff：`E/source-environment-fix.diff`；改前/后 Source：`source-before.py`、`source-after.py`。

| 身份 | SHA256 |
| --- | --- |
| 本次前 spec / 本次后 spec（不变） | `83dc994ab6d7ffe65cdf2bf38dbe027599775ffa71c6614219123856f8be1d2d` |
| 本次前 Source | `735f4731c6061638a35dce7daf8e03b5e582da3e16e7d38d2edecc1b852319a8` |
| 本次后 Source | `2476c5efa061499d7963e0f0976f0c9c86944b688f5bcc48ea40911574af399e` |
| 相对工作区 spec、含新增 Source 的完整 patch | `4ca1dc3e51ee7eeb8b9c526d50c4d5345ef967b4537ddbc1107c86427c099413` |

最终候选补丁：`E/archive-native-conversion.patch`。`git -C W/llvm apply --check` 通过；没有向 W 应用。
认证指纹同时更新 Source/spec/diff/patch 精确 SHA；CMake 参数、固定仓库、build.conf 与 docs/13 基线指纹保持一致。
证据：`new-identities.json`、`patch-apply-check.json`、`tools/llvm_archive_fix_trial_fingerprint.json`。

### 1.2 五个代表归档回归

从 H 重新取原 bitcode，经修改后的 Source 转换到新目录 `E/five-conversion/archives`，
没有复用 E28 转换结果作输入；E28 只作逐成员预期 SHA。四 worker、单进程 4 GiB AS，scope 15 GiB/swap=0。

| 归档 | 成员数 | 覆盖点 | 逐成员名称/次序/重复身份/SHA |
| --- | ---: | --- | --- |
| libclangCodeGen.a | 101 | 同名成员 | 全部一致 |
| libLLVMSupport.a | 179 | 175 bitcode + 4 原机器码 | 全部一致 |
| libarcher_static.a | 1 | libarcher bitcode | 一致 |
| libclangSema.a | 86 | 最大归档 | 全部一致 |
| libLLVMAnalysis.a | 131 | 125 bitcode + 6 原机器码 | 全部一致 |

合计 **498 成员，488 转换、10 原样保留**；五个完整归档 SHA 也与 E28 相同。
转换 wall **97.557340 s**，单成员最大 RSS **556,368 KiB**；含比较的阶段 wall **124.513931 s**。
scope MemoryPeak **3,107,987,456 B**，无 OOM，采样器/日志线程均回收。
证据：`five-selection.json`、`five-result.json`、`five-summary.json`、`five-scope/outcome.json`、`scope-after-rpm.log`。

Source/转换器/归档解析/认证/内存等待/构建门禁相关 **45 项测试 PASS**：
`source-resource-tests.log`(3)、`conversion-tests.log`(8)、`inspector-tests.log`(10)、
`archive-trial-tests.log`(7)、`memory-wait-tests.log`(3)、`build-guard-tests.log`(14)。
包含单进程 AS 约束、四 worker 独立资源计数、失败回收、精确指纹正负对照和六小时超时边界。

## 2. 预授权内存等待与完整构建

`tools/build_llvm_x86_64.py --wait-for-memory` 为显式开关：每次低于 **16 GiB** 时记录原始 MemAvailable，
每 **300 秒**再读，最长 **6 小时**，满足立即进入原构建入口；超时抛错，不重试构建。
未传开关保持原来的立即拒绝行为。本次从第一次预检到启动前的多个检查共用六小时截止时刻，
没有结束任何他人进程、降低门槛或修改配置。

这次三次检查均满足，无实际等待：

| 时间（+08:00） | MemAvailable，B | 判定 |
| --- | ---: | --- |
| 16:40:51 | 20,963,885,056 | 准入 |
| 16:41:01 | 20,752,142,336 | 准入 |
| 16:41:01 | 20,763,930,624 | 准入 |

证据：`E/full-build/memory-admission.jsonl`。18 GiB scope、MemorySwapMax=0、GBS 包并发 1、
Ninja/LLVM compile/link=4/4/1、debuginfo -j4、nice 15、ionice c3 均保持；
每 30 秒 free/loadavg/树 RSS/磁盘采样，每 2 秒进程/链接高水位采样，宿主 available<2 GiB 自动中止。
转换和后续消费者编译的单进程 AS 为 4 GiB；链接按 docs/29 不设 AS 上限，受 cgroup 限制。

唯一 LLVM 构建入口完整 argv：`E/full-build-attempt.json`；实际外层 time/systemd/GBS 命令：
`E/full-build/launch.json`、`commands.log`；日志逐行有时间戳，没有第二次 GBS 尝试。
新根安装 120 包与旧日志版本逐项一致；五个 RPM 宏/脚本 SHA 与 R0 一致；新根 SOURCES 中 Source SHA 与候选一致。
证据：`actual-installed-packages.json`、`actual-root-identities.json`。

CMake 门禁 **PASS，316.081322 s**，在 15 分钟内：

```text
CMAKE_BUILD_TYPE=Release
LLVM_ENABLE_LTO=Thin
LLVM_LINK_LLVM_DYLIB=OFF
CLANG_LINK_CLANG_DYLIB=OFF
LLVM_USE_LINKER=lld
LLVM_ENABLE_ASSERTIONS=No
LLVM_PARALLEL_COMPILE_JOBS=4
LLVM_PARALLEL_LINK_JOBS=1
LLVM_TARGETS_TO_BUILD=X86;ARM;AArch64;BPF
CMAKE_CXX_FLAGS=  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument   -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables  -g -O3 -flto=thin -fomit-frame-pointer

```
### 2.1 完整构建结果：PASS

唯一完整 GBS 构建成功，22 个二进制 RPM（另有 1 个 SRPM），二进制 RPM 总字节数 8,857,356,368。
入口开始 `2026-09-27T16:40:51.938659+08:00`，结束 `21:07:43.494640+08:00`，退出码 0。
`E/full-build-entry-exit.json`、`full-build/outcome.json`、`full-build/time-v.txt` 是三层计时原文。

| 指标 | 实测 |
| --- | --- |
| 含预检的完整入口 wall | 16,011.555025 s（4:26:51.555） |
| scope/GBS wall | 16,001.786853 s；time 原文 4:26:41 |
| time user / sys | 82,397.81 / 1,528.23 s |
| time 最大 RSS | 16,599,128 KiB（15.830162 GiB） |
| cgroup MemoryPeak / MemoryMax | 19,327,352,832 / 19,327,352,832 B，均为 18 GiB |
| cgroup MemorySwapMax / CPUUsageNSec | 0 / 83,927,270,922,000 |
| memory.events | max=153；oom=0、oom_kill=0、oom_group_kill=0 |
| 30 秒采样次数 / 宿主最低 MemAvailable | 529 / 11,634,499,584 B |
| 最大进程树 RSS（采样） | 17,166,979,072 B；可能重复计共享页，不能当单进程 RSS |
| 磁盘可用：入口 / 最低采样 / 完成 | 546,240,655,360 / 310,857,240,576 / 360,287,780,864 B |
| 收尾 | sampler_reaped=true，log_reader_reaped=true，problems=[] |

cgroup 峰值恰到 cap，包含文件页缓存；这不是不受限的自然峰值，也没有发生 OOM。
`max=153` 不能写成 153 次 OOM。运行中最低可用内存仍超过 2 GiB，未触发宿主保护。
磁盘变化包含新构建树、ThinLTO cache、转换证据和 RPM，不等于最终包大小。
证据：`build-resource-summary.json`、`full-build/samples.jsonl`、`scope-after-rpm.log`。

| 链接目标（Top 5） | VmHWM，KiB | 首末采样（+08:00） |
| --- | ---: | --- |
| bin/clang-22 | 16,599,128 | 17:45:58–17:53:06 |
| bin/clang-repl | 16,340,760 | 18:28:26–18:37:12 |
| lib64/libclang-cpp.so.22.1 | 16,282,872 | 17:53:11–18:00:17 |
| lib64/liblldb.so.22.1.8 | 15,950,052 | 17:38:12–17:45:38 |
| bin/clang-check | 15,749,964 | 18:38:33–18:43:24 |

原始 2 秒采样为 `full-build/linker-memory-observations.jsonl`；首末采样是存活区间下界，不能冒充完整链接 wall。

### 2.2 真实 %install 转换结果

7634/7634 编译/链接任务在 **19:40:54** 完成并进入 `%install`；
`NATIVE_ARCHIVES_BEGIN` **19:55:55**，`NATIVE_ARCHIVES_END ... PASS 225` **20:13:29**。
转换器内部计时 **891.253564 s**；BEGIN/END 含回写安装树等工作的高精度 wall **1,054.024996 s**。

- 225 个归档，3,864 成员，其中 **3,853 bitcode 转换、11 原机器码成员保留**。
- 转换前 5,482,378,620 B；转换后未 strip 为 6,615,100,896 B。这是本次构建输入/输出，不复用 docs/28 的数值。
- 每个成员的 wall/user/sys/RSS 与 argv 在 `B/native-archive-conversion/members/`；单转换进程最大 RSS **1,040,144 KiB**。
- 该时段最大采样进程树 RSS **1,234,276,352 B**；cgroup current 最大 **17,386,770,432 B** 包含此前编译遗留页缓存，不能当转换进程所需内存。
- 所有转换成功后才进入原有 find-debuginfo `-j4`，没有取消原后处理，也没有调用 ranlib 修补最终 RPM。

原始完整转换日志：`E/native-archives-install.log`；原始 Source JSON：`B/native-archive-conversion/summary.json`，
归档副本：`E/install-conversion-summary.json`；摘要：`install-conversion-brief.json`。
构建后再次读取五份新根 RPM 宏/脚本，SHA 与 R0 仍逐项相同，见 `actual-root-identities.json`。

## 3. 新 RPM 验收

新 RPM 经 `rpm2cpio | cpio -idmu --no-absolute-filenames --no-preserve-owner` 解包到
`W/temp/toolchain-archivefix`（下称 N），没有安装宿主。22 次两个管道进程退出码均为 0；
新目录不存在时才创建，不覆盖旧基线。`E/rpm-extraction-status.json`、`rpm-extract.log`、`rpm-file-owners.json` 保存逐包证据。

### 3.1 开发归档与 compiler-rt：全部 PASS

`E/verify_new_archives.py` 调用已测试的 `tools/inspect_llvm_archives.py`，
GNU 索引的每个成员 header offset 被解析为 ordinal/name/occurrence；
逐归档将完整 `(symbol, ordinal, name, occurrence)` 多重集合与成员外部定义符号比较。
没有用非空或相同条目数代替完整映射。构建树仍含原 bitcode，所以它用于成员身份/顺序核对，
新 RPM 索引的符号依据是它自身的新机器码成员，不能拿 bitcode 索引当原生符号的预期值。

| 门禁 | 实测 |
| --- | --- |
| static-devel 归档 / 成员 | 225 / 3,864；包含 libarcher_static.a，双包归属不重复计算 |
| 与本次 B 原归档成员数量/顺序/名称/重复身份 | 225/225 一致 |
| 格式 | 全部 ELF64 little-endian、x86_64 ET_REL；bitcode=0、other=0、thin=0 |
| 调试节 | 0（含 .debug/.zdebug 及对应重定位节） |
| 完整索引 | 225/225 PASS，共 318,543 条，等于成员定义外部符号多重集合 |
| 每函数分节抽查 | 10 个成员均有独立 .text.* 节，计数 464/55/8/250/218/66/91/100/83/18 |
| compiler-rt | 45 归档、1,964 成员；名称/顺序/内容 SHA、完整索引均与 H 一致；无 bitcode、无调试节 |
| compiler-rt 时间戳 | 1,964 个 ar 成员 mtime 与 H 不同；内容和索引不变，按事前规则单列、不判失败 |

逐归档完整记录：`E/new-archive-checks/<归档名>.json`；45 个运行库及全部成员时间戳：
`E/new-archives-result.json`；抽查的完整节名列表也在其中；摘要：`new-archives-brief.json`。
本项未执行任何 ranlib、重写或修补。

### 3.2 RPM 后处理链：PASS

| 步骤 | 本次次数 | 基线次数 | 本次 build.log 行号 |
| --- | ---: | ---: | --- |
| brp-compress | 1 | 1 | 17441 |
| brp-strip | 0 | 0 | 未执行：宏条件跳过 |
| brp-strip-static-archive | 1 | 1 | 17442 |
| brp-python-hardlink | 1 | 1 | 17443 |
| find-docs | 1 | 1 | 17444 |
| find-debuginfo | 1 | 1 | 16896 |

GNU strip 的 `format not recognized` / `Unable to recognise/recognize` 行为 **0**；
`NATIVE_ARCHIVES_BEGIN/END` 各 1 次且 END 为 PASS 225。
普通 `brp-strip` 为 0 是原宏在启用 debuginfo 时的既有条件：
`R0/usr/lib/rpm/tizen_macros:35` 的 `%{!?__debug_package:...}`；归档 strip 在 :36。
因此准确结论是“宏链与基线一致”，不能虚构所有条目都被执行。
`find-isufiles`、HAL/app rootstrap 检查等原命令也保留在原始日志。

证据：`E/postprocessing-result.json`（含所有命令原文与行号）、`tizen-macro-evidence.txt`、
`full-build/build.log`。缺少 build-id 的 debuginfo 警告在新旧日志都存在，
对照 `build-id-warning-comparison.json`；它不属于本次 bitcode strip 格式错误，未隐藏或作为新修复宣称已解决。
### 3.3 逐文件清单与 SHA：其他差异为 0

实际读取 N 与 H 的全部 17,689 唯一路径，核模式/类型/链接目标/文件 SHA；
同时与各自 RPM 头部文件记录交叉核对，元数据不匹配 0。没有只信 RPM 头部摘要而跳过解包内容读取。

| 差异分类 | 数量 | 分析与判定 |
| --- | ---: | --- |
| static-devel 的 .a | 225 | 本次有意将 bitcode 转为机器码；格式、完整索引、成员身份门禁全 PASS |
| compiler-rt 的 .a | 45 | 只规范化 ar 各 header（含索引等特殊 header）的 12 字节 mtime 后，整档逐字节一致；原始成员内容/索引已独立通过 |
| 其他 | **0** | 文件清单、模式、链接目标、SHA 全相同；无需逐项豁免 |

全部差异路径与新旧摘要：`E/rpm-file-comparison.json`；运行库字节级归因：
`runtime-ar-header-differences.json`；逐项审查结果：`file-differences-reviewed.json`。
这是这一次受控重建的实测，不宣称所有未来构建或 RPM 头部可复现。

### 3.4 七项宿主消费者：7/7 PASS

输入归档全部改为 **N/usr/lib64（新 RPM）**，沿用已通过的 `tools/verify_native_archive_consumers.py`。
编译与链接分开；编译 4 GiB AS，链接无 AS 上限但在有界 scope 内；GNU ld 的实际 driver 展开无 LTO、无插件。
H 的编译器/头文件/llvm-config/opt 用作同协议夹具，它们与 N 的同路径文件已逐字节相同，
没有将旧归档用作正例。H 原 bitcode 归档只用于失败反例。

| 环境组成 | 实际来源 |
| --- | --- |
| clang、opt、lld、LLVM/lld 头、resource-dir | H 解包；本次已证实与 N 同文件 SHA 相同 |
| 被验静态库 | N/usr/lib64，llvm-config --link-static 经临时 prefix 查询 |
| C++ 标准库头/运行库、glibc、crt、libgcc、GNU ld | 宿主 GCC 13 搜索路径及 /usr/bin/ld.bfd，编译 -v 和 loader --list 原文留存 |
| libxml2.so.16 | 固定 Tizen 快照的 RT，SHA `0d70127304264bd46387484ed7e566fc5fec96fb9c77de8c06fe0a9e9a0a8034`；不安装宿主 |
| loader | 宿主 /lib64/ld-linux-x86-64.so.2，显式 --library-path=RT |

| 检查 | 实测 |
| --- | --- |
| A-bfd、A-lld | 两者解析/验证固定 IR，PassBuilder O2 后输出均与同输入 opt -O2 完整相同 |
| B-bfd、B-lld | 两者调用 lld ELF 入口完成进程内链接；生成物实际运行 exit=37，SHA 同为 `3609167ac2889072dcca787a8cf2cbcdb762c280e55350b797ef02e6842ce789` |
| 共享库 | GNU ld -shared -z defs -z text 成功，小程序 dlopen 调用后输出一致 |
| GNU ld --gc-sections | 47,387,472 → 28,378,320 B；GC 版本同样运行正确；不是性能测量 |
| 原 bitcode 反例 | 相同无 LTO/插件的 GNU ld 命令换入 H 原归档，预期 exit=1；先报索引缺失，不能夸大为排除索引因素的格式隔离实验 |

消费者 scope wall **20.271952 s**。每条 compile/link/run 的完整 argv、耗时、RSS、50 ms VmPeak/Threads 采样：
`E/new-rpm-consumers/*.json`、`*.memory.jsonl`；摘要 `new-consumer-measurements.json`；
实际运行库列表 `new-consumer-runtime-libraries.txt`；全部门禁 `new-rpm-consumers/result.json`。
短命令只有一个采样时，不能用启动器 VmPeak 当目标程序峰值；原始样本保留，不为补峰值重复功能实验。
这是宿主 ABI 消费者验证，Tizen 原生包内验证另列下一节。

### 3.5 三个工具二进制身份

| 工具 | 新/旧字节数 | 新/旧 SHA256（相同） |
| --- | ---: | --- |
| clang-22 | 139,929,464 | `3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c` |
| lld | 83,539,336 | `7ebba1bbc8a46e086c4470373315dd31730dab8fe554987894e6689e45e071fc` |
| llvm-ar | 14,825,632 | `cad420e2daeb125b051a5d3f81b038b037c15fd30921ce880d4cc087d624313f` |

证据：`E/new-tool-identities.json`。这次转换位于工具构建/链接后的安装阶段，三个成品与基线逐字节相同。

## 4. Tizen 新根测试包：bfd / lld 两次全部 PASS

仅在上述新 RPM 门禁全部通过后，创建两个临时测试源码仓库，分别启动一次 GBS。
它们不在工作区 LLVM 内；spec/源文件/tarball 均留在 E/test-package-bfd/ 与 E/test-package-lld/，不安装到宿主系统。
两个 spec 除包名与 `-fuse-ld` 值外相同。

- BuildRequires 精确指定 `llvm-static-devel/llvm-devel/llvm/clang = 22.1.8-1`，保证消费本次包；
  测试包另声明 libxml2-devel 与 zlib-devel，满足 `llvm-config --system-libs`。**没有给 LLVM spec 新增 BuildRequires**。
- 附加仓库 `E/new-rpm-repo/` 由 22 个本次 RPM 的硬链接和 `createrepo_c --workers 2` 生成；
  命令/清单为 `new-rpm-repo-command.json`，GBS 用 `-R` 加入；固定 Base/Unified 来源不变。
- bfd 根：`W/temp/gbs-root-archive-consumer-bfd`；lld 根：`W/temp/gbs-root-archive-consumer-lld`。
  都是新建实例 `local/BUILD-ROOTS/scratch.x86_64.0`，共安装 113 包（107 个来自远端下载，另有本地 RPM）。
- 18 GiB cap、MemorySwapMax=0、nice15/ionice3、宿主采样与回收保持；每次各自先检查可用≥16 GiB，
  低于时300秒轮询、最多6小时。两次都立即满足，**实际等待0次**。
- 每个源码先用 `prlimit --as=4294967296 --core=0 -- clang/clang++ ... -c` 编译；链接只输入 .o、无AS上限。
  保存 `-###` 展开并拒绝 `-flto/-plugin/--plugin/-cc1`；实际链接器分别为 `/usr/bin/ld.bfd`、`/usr/bin/ld.lld`。
- 这是 Tizen x86_64 原生环境：glibc **2.40-1.10**、GCC/libstdc++ **14.2.0-1.10**、binutils **2.43-1.9**、
  libxml2 **2.15.1-1.7**、zlib **1.3.1-1.9**；clang/LLVM **22.1.8-1**。
  实际 clang 配置为 `/usr/bin/clang++.cfg`，target 为 `x86_64-tizen-linux-gnu`，不使用宿主头/运行库。

| 项目 | bfd | lld |
| --- | --- | --- |
| 启动 / 完成（+08:00） | 21:42:22+08:00 / 21:46:46+08:00 | 21:48:28+08:00 / 21:52:39+08:00 |
| 准入 MemAvailable，B | 18410356736 | 18376101888 |
| 入口 wall，s | 264.099215 | 251.660013 |
| scope MemoryPeak，B | 4601528320 | 4322967552 |
| CPUUsageNSec | 65225299000 | 59937735000 |
| 宿主最低可用内存，B | 18194694144 | 18169155584 |
| GBS / %check | 0 / PASS | 0 / PASS |
| A 与根内 opt -O2 | 逐字节相同 | 逐字节相同 |
| B 进程内 lld 链接 / 生成物运行 | 成功 / exit 37 | 成功 / exit 37 |
| 根内225归档+4工具SHA与新RPM | 全部一致 | 全部一致 |
| sampler / log-reader 回收 | true / true | true / true |

两次 memory.events 均无 OOM；完整事件原文见 `E/tizen-summary.json` 和各 scope 的 samples.jsonl。
根内库身份不是仅凭版本号推断：`verify_tizen_installed.py` 实际核对全部 225 个开发归档，
另核 clang-22、opt、llvm-config、lld 四工具，与 N 中同文件 SHA 全相同。
`installed-identities.json` 保存逐文件结果；`check-outputs/` 保存 expected.ll、actual.ll、b.output、两个 driver 展开。

两个 `%check` 的关键原始输出（各日志:573、579、581）：

```text
+ cmp expected.ll actual.ll
+ test 37 = 37
TIZEN_CONSUMER_CHECK_PASS bfd A_IR_IDENTICAL B_GENERATED_EXIT_37
```

```text
+ cmp expected.ll actual.ll
+ test 37 = 37
TIZEN_CONSUMER_CHECK_PASS lld A_IR_IDENTICAL B_GENERATED_EXIT_37
```

完整命令、依赖/安装日志、实际编译链接 argv、%check、RPM 产出与 GBS 总结分别在
`E/tizen-bfd/{attempt.json,build.log,result.json,outcome.json}` 与 `E/tizen-lld/` 同名文件。
完整 GBS 参数形如（每个 flavor 只运行了一次）：

```text
gbs -c W/gbs_llvm.conf build -A x86_64 -B W/temp/gbs-root-archive-consumer-<flavor>
    --threads 1 --include-all --define '_smp_mflags -j4'
    -D E/full-build/buildconfig.conf -R E/new-rpm-repo E/test-package-<flavor>
```

scope 经检查保留峰值后退出，事件与实际退出码共同作为通过依据；没有只看成功提示而忽略 job/管道状态。

## 5. 结论、补丁状态与收尾自检

**YES：本次 x86_64 归档转换修法已具备提交独立修复评审的实测依据。**
一次完整构建、真实 RPM 后处理、新 RPM 的格式/完整索引/成员身份、compiler-rt 保持、
逐文件差异、七项宿主消费者以及 Tizen 原生 bfd/lld 两次 A+B 测试包均 PASS。
无 LTO/无插件 GNU ld 的兼容性在规定消费者上得到验证；不是只证明 ranlib 索引非空。

候选补丁在附录 C，SHA `4ca1dc3e51ee7eeb8b9c526d50c4d5345ef967b4537ddbc1107c86427c099413`。
**尚未提交 Gerrit、未进入 OBS，也未修改 W 的源码/spec。** 后续由用户安排评审和正式提交。
本实现 `%ifarch x86_64`；ARM/AArch64 的转换器、输入与环境仍须分别验证，不能把这里的 backend flags 或耗时直接套用。
BOLT、设计 v4 与其他架构实施没有在本轮启动。

| 提交前检查 | 答案与证据 |
| --- | --- |
| 构建根环境依赖是否满足 | 是；移除原 Source 的 GNU time，wait4 方案实际完成 Tizen %install，五归档回归与45测试PASS（§1） |
| 是否新增 LLVM BuildRequires / 修改 RPM 宏或优化参数 | 否；本次相对docs/29只改Source资源记账和认证身份，spec不变；完整候选仅增加x86_64安装转换（附录C） |
| 是否按预授权等待与原门槛执行 | 是；入口16GiB、18GiB/swap0不变；三次构建全部即时准入，未结束他人进程或重试（§2、§4） |
| 构建次数 | LLVM完整构建1次；Tizen消费者包bfd1次、lld1次；没有失败后重试 |
| CMake/新 RPM/消费者门禁 | 全部PASS，逐项见§2–§4 |
| 是否保持工作区原件与历史报告 | 是；W spec与docs/25–29六个受保护SHA仍相同，E/final-integrity.json |
| 资源进程回收 | 所有构建、离线验收scope的sampler/log-reader均回收；完整GBS与两个包构建均exit0；E/final-cleanup.json |
| 独占锁 | 同session锁持续持有至最终收尾；推送核对后由持有进程校验身份并释放，记录E/lock-released.json |
| 其他禁止任务 | 未跑BOLT、未做性能校准、未构建Chromium、未推Gerrit |

日志中的秒数是本次构建/功能验证的资源记录，不作为优化收益或噪声校准结果。

## 附录 A：原 x86_64 构建根的完整 120 包清单

来源：`temp/baseline-build-20260917/build.log:339–458`。新根版本逐项相同，固定快照 checksum/架构见 `E/installed-packages.json`。

| 包及版本-release | 原日志行 |
| --- | ---: |
| `setup-0.9-1.11` | 339 |
| `filesystem-3.1-1.1` | 340 |
| `glibc-2.40-1.10` | 341 |
| `bash-3.2.57-1.8` | 342 |
| `zlib-1.3.1-1.9` | 343 |
| `libgcc-14.2.0-1.10` | 344 |
| `libstdc++-14.2.0-1.10` | 345 |
| `coreutils-6.9-14.2` | 346 |
| `liblzma-5.8.1-1.9` | 347 |
| `libbz2-1.0.8-1.8` | 348 |
| `pkg-config-0.29.2-1.8` | 349 |
| `libelf-0.189-1.10` | 350 |
| `libxml2-2.15.1-1.7` | 351 |
| `libdw-0.189-1.10` | 352 |
| `libopenssl3-3.5.5-1.8` | 353 |
| `libxcrypt-4.4.36-1.10` | 354 |
| `libllvm-22.1.8-1.6` | 355 |
| `libblkid-2.41.2-1.4` | 356 |
| `libpython3_141_0-3.14.2-1.6` | 357 |
| `libsqlite-3.51.0-1.9` | 358 |
| `nspr-4.36-1.1` | 359 |
| `llvm-22.1.8-1.6` | 360 |
| `clang-22.1.8-1.6` | 361 |
| `pam-1.1.6-1.4` | 362 |
| `terminfo-base-full-6.6-1.3` | 363 |
| `libncurses6-6.6-1.3` | 364 |
| `libreadline-5.2-1.8` | 365 |
| `gdbm-1.8.3-1.10` | 366 |
| `perl-5.42.0-1.8` | 367 |
| `libexpat-2.7.3-1.8` | 368 |
| `libfreebl3-3.109-1.1` | 369 |
| `libpopt-1.16-1.8` | 370 |
| `libuuid-2.41.2-1.4` | 371 |
| `libfdisk-2.41.2-1.4` | 372 |
| `build-mkbaselibs-20120927-1.1` | 373 |
| `libncurses5-6.6-1.3` | 374 |
| `ncurses-devel-6.6-1.3` | 375 |
| `readline-devel-5.2-1.8` | 376 |
| `nss-certs-3.109-1.1` | 377 |
| `libsoftokn3-3.109-1.1` | 378 |
| `nss-3.109-1.1` | 379 |
| `liblastlog2-2.41.2-1.4` | 380 |
| `libmount-2.41.2-1.4` | 381 |
| `libasm-0.189-1.10` | 382 |
| `libxml2-tools-2.15.1-1.7` | 383 |
| `xz-devel-5.8.1-1.9` | 384 |
| `bzip2-1.0.8-1.8` | 385 |
| `xz-5.8.1-1.9` | 386 |
| `linux-glibc-devel-6.6-1.9` | 387 |
| `libxcrypt-devel-4.4.36-1.10` | 388 |
| `glibc-devel-2.40-1.10` | 389 |
| `zlib-devel-1.3.1-1.9` | 390 |
| `gzip-1.3.12-1.8` | 391 |
| `libcc1-14.2.0-1.10` | 392 |
| `libgfortran-14.2.0-1.10` | 393 |
| `binutils-libs-2.43-1.9` | 394 |
| `binutils-2.43-1.9` | 395 |
| `make-4.4.1-1.8` | 396 |
| `findutils-4.3.8-1.8` | 397 |
| `libatomic-14.2.0-1.10` | 398 |
| `libattr-2.5.1-1.9` | 399 |
| `libacl-2.3.2-1.8` | 400 |
| `libarchive-3.8.1-1.4` | 401 |
| `libarchive-tools-3.8.1-1.4` | 402 |
| `libcap-2.73-1.10` | 403 |
| `libffi-3.4.7-1.10` | 404 |
| `python3-base-3.14.2-1.6` | 405 |
| `libgomp-14.2.0-1.10` | 406 |
| `libitm-14.2.0-1.10` | 407 |
| `libltdl-2.5.4-1.10` | 408 |
| `liblua-5.1.5-1.7` | 409 |
| `libpcre-8.45-1.9` | 410 |
| `libquadmath-14.2.0-1.10` | 411 |
| `libsmack-1.3.1-1.7` | 412 |
| `libsmartcols-2.41.2-1.4` | 413 |
| `libzstd1-1.5.7-1.8` | 414 |
| `m4-1.4.20-1.1` | 415 |
| `autoconf-2.71-1.11` | 416 |
| `automake-1.16.5-1.11` | 417 |
| `patch-2.8-1.8` | 418 |
| `sed-4.1c-1.9` | 419 |
| `util-linux-2.41.2-1.4` | 420 |
| `libmagic-data-5.46-1.8` | 421 |
| `libmagic-5.46-1.8` | 422 |
| `rpm-4.14.1.1-1.4` | 423 |
| `rpm-build-4.14.1.1-1.4` | 424 |
| `file-5.46-1.8` | 425 |
| `util-linux-su-2.41.2-1.4` | 426 |
| `libtool-2.5.4-1.10` | 427 |
| `smack-1.3.1-1.7` | 428 |
| `gcc-14.2.0-1.10` | 429 |
| `grep-2.5.2-1.10` | 430 |
| `python3-3.14.2-1.6` | 431 |
| `python3-devel-3.14.2-1.6` | 432 |
| `build-20120927-1.1` | 433 |
| `cmake-3.31.2-1.2` | 434 |
| `tar-1.17-1.1` | 435 |
| `binutils-devel-2.43-1.9` | 436 |
| `libxml2-devel-2.15.1-1.7` | 437 |
| `elfutils-0.189-1.10` | 438 |
| `libncurses-6.6-1.3` | 439 |
| `less-685-1.1` | 440 |
| `llvm-devel-22.1.8-1.6` | 441 |
| `glibc-locale-2.40-1.10` | 442 |
| `tzdata-2025b-1.1` | 443 |
| `libstdc++-devel-14.2.0-1.10` | 444 |
| `ninja-1.13.1-1.9` | 445 |
| `patchelf-0.16.1-1.8` | 446 |
| `cpp-14.2.0-1.10` | 447 |
| `gcc-c++-14.2.0-1.10` | 448 |
| `app-rootstrap-checker-1.0.0-1.1` | 449 |
| `build-compare-2023.06.18-1.2` | 450 |
| `hal-rootstrap-checker-1.0.0-4.1` | 451 |
| `gawk-3.1.5-1.1` | 452 |
| `cpio-2.8-1.1` | 453 |
| `diffutils-3.10-1.1` | 454 |
| `hostname-3.23-1.1` | 455 |
| `net-tools-2.0_20121208git-1.3` | 456 |
| `update-alternatives-1.22.21-1.1` | 457 |
| `which-2.17-1.1` | 458 |

## 附录 B：22 个新二进制 RPM

路径前缀为 `R/home/abuild/rpmbuild/RPMS/x86_64/`。原始清单：`E/rpm-inventory.json`。

| RPM | 字节 | SHA256 |
| --- | ---: | --- |
| clang-22.1.8-1.x86_64.rpm | 310020438 | `57e31c3c6cfe587e945b72f2c934e3f5d73c319edbfc3780246f2e075d763cc1` |
| clang-debuginfo-22.1.8-1.x86_64.rpm | 2928314794 | `2b4456490c2200e4e7756c00d63c29e5b60851154c613a8aa22d0c4b17ca647c` |
| clang-devel-22.1.8-1.x86_64.rpm | 4098438 | `91f2c1e86c4bc1663ed76b3da5bc92d3ee9212cc79a319556e93ab0e78b74e5d` |
| clang-devel-debuginfo-22.1.8-1.x86_64.rpm | 5728458 | `374f21829749167843bb5852764ad1d1c864c94432a83bbaeb22e74b9eff7f97` |
| compiler-rt-22.1.8-1.x86_64.rpm | 3720882 | `a04d4c8d87946926fd0c864361d12696dbee774871c9e26a1cca1b0a1386d6a7` |
| compiler-rt-debuginfo-22.1.8-1.x86_64.rpm | 1290054 | `1704da28f2a85265442651998ceb09bd6c822be5ef02746cd201be5241c3577a` |
| libllvm-22.1.8-1.x86_64.rpm | 23651730 | `b1a0a608bdd5c24d4bd22f4b97ca3a693f8a3bed111921441c303d98ba82962e` |
| libllvm-debuginfo-22.1.8-1.x86_64.rpm | 198056882 | `baa767aa71c56953f5b64c76238b2a3635a9b0b2161975a8e8e31f7bc22c7d5f` |
| libomp-22.1.8-1.x86_64.rpm | 373526 | `638f0336ff915fe528f44a89f461365a30d81d10e9eb9d0c955b5a9cdcc55179` |
| libomp-debuginfo-22.1.8-1.x86_64.rpm | 1142462 | `ffe93ca0288ecbbc935676fb0db63d049893d462739a2bca3ff0c34f63de5acb` |
| libomp-devel-22.1.8-1.x86_64.rpm | 25510 | `5511b614db588d02a46ccb2bb4b9b7af08fdd5f602f8c06002ec2b0f6fec2b06` |
| lldb-22.1.8-1.x86_64.rpm | 30772886 | `7affe5bd2875ff235faf9f424006f06903f7bbda44b20e1cc87bc0984a4e400e` |
| lldb-debuginfo-22.1.8-1.x86_64.rpm | 332844614 | `c0e4cb273943f08b9f2184f596f38e5594846b7c597d0049334ff086d1a307f9` |
| lldb-devel-22.1.8-1.x86_64.rpm | 30525346 | `73575e9baac3fee292389094db1a88b8d835825eec26e986171537d017b61dba` |
| lldb-devel-debuginfo-22.1.8-1.x86_64.rpm | 279581026 | `af830ca834b1df9a309ee8de83e4edeae7c193735d25e7df07f5b5b638576fb0` |
| llvm-22.1.8-1.x86_64.rpm | 410603926 | `87285f27404581b1ac4661328869bc110466db56aaf5af09d0ce925ffb54b211` |
| llvm-debuginfo-22.1.8-1.x86_64.rpm | 3842671946 | `0f47d2e6089ebfc1427088a69b0153b0b7fb7d319fb4f2ee69492a01fbda831a` |
| llvm-debugsource-22.1.8-1.x86_64.rpm | 43653706 | `c09eed9cda9d2cbfc4e3d3ae04523b4baf3578d5acad462b72efa6bd05183023` |
| llvm-devel-22.1.8-1.x86_64.rpm | 41190662 | `b5e7f0942fe777215812e0b348bfbcff32b2900d34fa71516ce725a6fe205fd0` |
| llvm-devel-debuginfo-22.1.8-1.x86_64.rpm | 308603318 | `ef4ffe9f66f606972353deb65b659ce88dce4afbbfffb4f7bac8b495e0e92dd8` |
| llvm-static-devel-22.1.8-1.x86_64.rpm | 60449442 | `2b26e3c34bb3c4476f96e481a09271b9a85ba074c8f729575dc064e28cc7a9fa` |
| python-clang-22.1.8-1.x86_64.rpm | 36322 | `03ecac25de89870038e403b7b63fa127bb3000fb1e70389b03379e3df2564384` |

## 附录 C：最终候选补丁与环境修正

相对 W/llvm 当前 spec（保留三处 4/4/1）的完整补丁为：

`/home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-full-build-20260927/archive-native-conversion.patch`

SHA256：`4ca1dc3e51ee7eeb8b9c526d50c4d5345ef967b4537ddbc1107c86427c099413`。
包含下列 spec 差异及完整 500 行新增 Source。Source 全文随仓库保存在
[tools/llvm_static_archives_source.py](../tools/llvm_static_archives_source.py)，与补丁和 S 中副本同字节。
该补丁不含工作区原有并发差异，不修改 RPM 宏，不改优化/链接参数，不修改 W 原件。

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

本次针对 docs/29 Source 的环境修正全文：

```diff
--- docs29/Source1005
+++ docs30/Source1005
@@ -1,5 +1,5 @@
 #!/usr/bin/env python3
-# Standalone RPM Source; copied policy from the certified docs/28 converter.
+# Standalone RPM Source; docs/28 conversion policy, wait4 resource accounting.
 # Embedded inspect_llvm_archives.py SHA256 81008a4859172318da880f224e53c5136958c29ebc9e12194e8f729fbd2d9ae0
 #!/usr/bin/env python3
 """Read GNU/BSD ar metadata without executing members; retain duplicate identities.
@@ -317,8 +317,9 @@
         prefix = Path(prefix)
         timing = prefix.with_suffix('.time')
         log = prefix.with_suffix('.log')
-        command = ['/usr/bin/time', '-f', '%e %U %S %M %x', '-o', str(timing),
-                   'prlimit', '--as=4294967296', '--core=0', '--', *map(str, argv)]
+        # GNU time is absent from the pinned Tizen buildroot. Keep limits in
+        # prlimit (util-linux); wait4 returns per-child, not process-global usage.
+        command = ['/usr/bin/prlimit', '--as=4294967296', '--core=0', '--', *map(str, argv)]
         start = time.monotonic()
         with log.open('wb') as err:
             with self.lock:
@@ -328,17 +329,19 @@
                                          stderr=err, start_new_session=True)
                 self.children.add(child)
             try:
-                rc = child.wait()
+                _, status, usage = os.wait4(child.pid, 0)
+                rc = os.waitstatus_to_exitcode(status)
+                child.returncode = rc
             finally:
                 with self.lock:
                     self.children.discard(child)
+        elapsed = time.monotonic()-start
         record = dict(argv=list(map(str, argv)), bounded_argv=command,
-                      elapsed_seconds=time.monotonic()-start, exit=rc)
-        if timing.exists():
-            record['time_raw'] = timing.read_text()
-            line = record['time_raw'].splitlines()[-1].split()
-            if len(line) == 5:
-                record.update(wall=float(line[0]), user=float(line[1]), sys=float(line[2]), max_rss_kib=int(line[3]))
+                      elapsed_seconds=elapsed, exit=rc, wall=elapsed,
+                      user=usage.ru_utime, sys=usage.ru_stime, max_rss_kib=usage.ru_maxrss,
+                      accounting='os.wait4; Linux ru_maxrss is KiB')
+        record['time_raw'] = f"{elapsed:.9f} {usage.ru_utime:.9f} {usage.ru_stime:.9f} {usage.ru_maxrss} {rc}\n"
+        timing.write_text(record['time_raw'])
         prefix.with_suffix('.json').write_text(json.dumps(record, indent=2)+'\n')
         if rc:
             self.cancel()
```

最终 patch 的 `git apply --check` 在工作区原 spec 上通过；原文 `E/patch-apply-check.json`。
这只是可应用性检查，没有向 W 或 Gerrit 应用/推送。

## 附录 D：证据入口与命令

全部 E 文件都在本机 temp/，不随 Git 上传；日志体积大的文件保留原文，不截断替代证据。

| 阶段 | 完整命令/原始输出 |
| --- | --- |
| 独占、输入、源身份 | precheck.json、lock-acquired.json、rpm-identity.json、baseline-content-check.json |
| 依赖与 API | installed-packages.json、source-api-inventory.json、dependency-filelists.json、python-module-providers.json |
| 五归档回归 | probe_five.py、five-conversion/、five-result.json、five-scope/ |
| 45 项测试 | source-resource-tests.log、conversion-tests.log、inspector-tests.log、archive-trial-tests.log、memory-wait-tests.log、build-guard-tests.log |
| 唯一 LLVM 构建 | full-build-attempt.json、full-build/launch.json、commands.log、build.log、time-v.txt、samples.jsonl、process-memory.jsonl、linker-memory-observations.jsonl |
| %install 转换 | native-archives-install.log、install-conversion-summary.json、B/native-archive-conversion/ |
| 新 RPM 解包与验收 | rpm-inventory.json、rpm-extract.log、rpm-extraction-status.json、new-archive-checks/、new-archives-result.json、postprocessing-result.json、rpm-file-comparison.json |
| 宿主消费者 | new-rpm-consumers/、new-consumer-measurements.json、new-consumers-scope/ |
| Tizen 测试源与入口 | test-package-bfd/、test-package-lld/、prepare_test_packages.py、run_tizen_consumer.py、tizen-bfd/、tizen-lld/（仅实际执行的目录存在） |
| 最终保护与回收 | final-integrity.json、final-cleanup.json、lock-released.json |

本次使用的完整 LLVM 入口如下（执行原文另见 JSON，不能把它当重复构建授权）：

```bash
python3 tools/build_llvm_x86_64.py --run --wait-for-memory \
  --source /home/linhao/Toolchain/development/llvm-optimize/temp/llvm-archivefix-trial \
  --buildroot /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-archivefix \
  --log-dir /home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-full-build-20260927/full-build \
  --certify-fingerprint archive-fix-trial \
  --exclusive-lock-session archivefix-rpm-a04c65b4b09a4ad19da2d4016d68ad01
```

两个纯监控/显示脚本曾出现取字段/截断尾行错误，记录 `E/monitor-query-note.txt`；
它们未执行构建或消费者，没有修改证据，也没有触发实验重试。实际构建/验收退出码按各自 outcome/result 判断。
