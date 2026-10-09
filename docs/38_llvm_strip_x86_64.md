# 38 LLVM 包 x86_64 打包改用 llvm-strip

日期：2026-10-09（Asia/Shanghai）。本次续接 `834f9aab34e2a495f1f53940096992d41cd19d4e`。
docs/25–37 保持原文；非静态库文件的对照始终为 docs/35 的 N，不以本次新产物自比。
原 `834f9aa` 因磁盘准入停止的记录仍是有效历史事实：当时未构建、未改 spec。
本次按用户新增的保全与清理授权解除空间阻塞，执行一次正常 `%build/%install/打包` 增量续跑。

**结果：PASS，补丁已具备本轮要求的评审证据。** 一次增量续跑产出 22 个 RPM；225 个开发归档与 45 个 compiler-rt 归档通过新门禁，
非静态库文件与 docs/35 的 N 零差异。270 次 llvm-strip 全部退出 0。
七项宿主归档消费者，以及宿主/Tizen 的 bfd/lld sanitizer、profile、builtins 消费者全部通过。
仅生成供用户 review 的独立 format-patch，未推 Gerrit。原件保全、清理、构建、验收和提交身份分列如下。

## 0. 范围、身份与独占

用户确认归档修复已上传 Gerrit 356627 patchset 2，提交前缀 `67619ec8bbba`、父提交 `cb67996861d0`。
本任务只验证 LLVM 包、只限 x86_64 的 `%__strip` 替换，拟作为归档转换修复之后的独立 change；
平台已全量切换 LLVM 编译作为用户前提使用。未修改 W/llvm 原件、gbs_llvm.conf、转换 Source 或任何优化/并发参数。

| 别名 | 路径 |
| --- | --- |
| W | `/home/linhao/Toolchain/development/llvm-optimize` |
| E0 | `W/temp/llvm-strip-x86_64-20261009`，原磁盘 STOP 与宏链证据 |
| E | `E0/continue-20261009`，本次续跑证据；以下无前缀文件相对 E |
| C | `W/temp/archive-fix-v2-final-20261009/continue-20261009`，docs/35 证据 |
| E34 / E36 | `W/temp/archive-fix-v2-build-20260929` / `W/temp/archive-fix-tizen-consumers-20261009` |
| S | `W/temp/llvm-archivefix-trial`，隔离的 archive-fix-trial 分支 |
| Rnew | `W/temp/gbs-root-x86_64-archivefix-v2` |
| R | `Rnew/local/BUILD-ROOTS/scratch.x86_64.0` |
| B | `R/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build` |
| N | `W/temp/toolchain-archivefix-v2-final`，docs/35 非静态库对照，保留 |
| H | `W/temp/archive-index-fix-rpm-20260923/baseline-rpm-extract`，docs/13 compiler-rt 对照，保留 |
| N38 | `W/temp/toolchain-llvm-strip`，本次新 RPM 解包目标 |
| 保全 RPM | `W/temp/archive-fix-v2-final-20261009/rpms-docs35` |

开场主仓库干净，无本项目竞争构建进程。用 O_EXCL 获取 `Rnew/.llvm-optimize-exclusive.lock`，
session=`llvm-strip-continue-851a7c5278ff49f8a659d394da53a136`、持锁 PID=477369。
证据：`processes-start.json`、`lock-acquired.json`、`identity-result.json`、`protected-start.json`。
复核 docs/35 22 个 RPM SHA/大小全部一致；N 的 17,689 个路径的类型、模式、大小、内容 SHA/链接目标一致，额外非目录路径 0。
`prepare-resume.json` 对照 C 的 `final-integrity.json`，核验已登记的 CMakeCache/build.ninja/Ninja 状态及关键 ELF，没有读取隔离旧混合根。

### 0.1 原 RPM 的 rename 保全

先对 R 的 22 个 RPM 及一个 SRPM 记录路径、字节、设备、inode、SHA，再用 `os.rename` 移至同文件系统的 `rpms-docs35`。
23 个文件全部设备号 2049、移动前后 inode 与 SHA 相同，没有复制再删除；22 个二进制包摘要全部与 docs/35 附录 A 一致。
这些文件不参与本次构建覆盖；N 与 C/new-rpm-repo 也保留。

**SRPM 证据边界：** docs/35 附录 A 只登记 22 个二进制包，没有历史 SRPM SHA。
因此只能确认该原根 SRPM 的移动前后摘要和 inode 不变，并对应历史日志的写出位置，不能冒称与不存在的历史 SHA 比较通过。
它为 340,919,240 B，SHA256 `2e944e3d34b11620a2307d4df3416e98aeb28912e22f957edbe67bd22982a21d`，inode=23122923。
完整逐文件证据：`preserved-rpms.json`。

### 0.2 按授权清理至 75 GiB 即停

原 `834f9aa` 时 `/home` 可用 50.800056 GiB；允许的 SSD 独立安装树不在同一文件系统，cache 全回收上界也仅 50.816586 GiB，原停止正确。
本次保全后、删除前可用 54,568,103,936 B。只执行新增清单第 1 类：旧 `W/temp/toolchain-archivefix` 解包的大载荷。
删除前该目录有 16,436 个文件，逻辑 49,672,070,325 B、分配 49,707,630,592 B。
实际删除 16,392 个载荷文件；按“保留所有日志/脚本/文本”的总原则留下 44 个文本/脚本，故目录仍有小体积保留内容。
逐项路径、大小、文件数、删除清单和 df 见 `cleanup-1-manifest.json`、`cleanup-1-summary.json`、`df-after-cleanup-1.log`。

删除后可用 **104,280,035,328 B（97.118 GiB）**，已达到 75 GiB，立即停止清理。
未执行第 2/3 类，未删除 Rnew cache、SSD 独立安装树、N、H、保全 RPM、docs/35–37/Base repo、docs/30 两测试根或隔离根。
`cleanup-result.json`：`completed_categories=[1]`、`target75_reached=true`、`disk_admission_pass=true`。

### 0.3 试验 spec 和精确认证

S HEAD/分支保持 `f111162e94aa48ed367c9d2c039456c70e7160ae` / `archive-fix-trial`。
S 与根内导出 spec 均只在开头加入下列三行；完整 diff 为 `trial-three-lines.diff`、`exported-three-lines.diff`。

```diff
+%ifarch x86_64
+%define __strip %{_bindir}/llvm-strip
+%endif
```

| 文件 | 改前 SHA256 | 改后 SHA256 |
| --- | --- | --- |
| S/packaging/llvm.spec | `6a91a0bf3d8d2044473662b65ed3d32d4696a697ccd52200d983ce4334aeafdf` | `4711c7f61798f34d5e581df9436681af00c3d9e88cb6d9c74db31183cd6556b8` |
| R/home/abuild/rpmbuild/SOURCES/llvm.spec | `91f684691eb35af52b1a9f2a2cba478f88dbfd8a48b4c2281dac6144d71d3bd0` | `901ea3f6332e890b84287d3cee466763f32ddda811bb6375d89142b5ab8aa4bb` |

Source SHA 始终 `6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557`。
W 原 spec SHA 始终 `95887b2d060b38d5ef8f56936f7481a03d131f9d26432180a68e02ec95f0dda5`，
gbs_llvm.conf 始终 `a3fea7732532db26c11b88407464e0274a6d8b4277623364fe16b6980181b03f`。

私有 `E/llvm-strip-trial-fingerprint.json` 精确绑定本次三个新增宏行及原 Source；续跑包装器只在自身进程中指定这个登记文件。
仓库的 GNU-strip archive-fix 指纹没有改，不能用它直接放行当前 S。
正例为本次精确配置；修改 ninja_jobs、normalized_spec_sha256、source_files 三个负例分别被拒绝，见 `trial-fingerprint-tests.json`。
保留 18 GiB、6/6/2 与其余原 CMake 参数，不通过扩大通用认证范围来绕过门禁。

## 1. `%__strip` 的实际影响面

只读宏链原文及带行号文件在 E0；递归检索得到 201 条引用，其中 65 个其他/本架构 platform 定义各 3 条，不能全视为当前生效路径。

| R 内文件:行 | 当前开 debuginfo 时的作用 |
| --- | --- |
| `usr/lib/rpm/macros:83` | 默认 `%__strip /bin/strip`；解析本试验 spec 后由三行宏覆盖 |
| `usr/lib/rpm/platform/x86_64-linux/macros:72–74` | 默认三条 strip 调用；Tizen 宏随后重定义 |
| `usr/lib/rpm/tizen/macros:34–38` | 有效 strip-install-post（此路径为 ../tizen_macros 软链接） |
| `usr/lib/rpm/tizen/macros:35` | brp-strip 在 `!__debug_package` 下才运行，本配置不运行 |
| `usr/lib/rpm/tizen/macros:36` | brp-strip-static-archive 传入 `%__strip`，唯一实际使用点 |
| `usr/lib/rpm/tizen/macros:37` | brp-strip-comment-note 已注释 |
| `usr/lib/rpm/tizen/macros:40–46、53–60` | compress、strip 链、python-hardlink、find-docs；debug 阶段先执行且独立 |
| `usr/lib/rpm/macros:182–196` | find-debuginfo 接 `_smp_mflags`，不接 `%__strip` |
| `usr/lib/rpm/find-debuginfo.sh:269、275、277–280` | 当前 STRIP_DEFAULT_PACKAGE 未设置，选择 elfutils eu-strip；binutils 后备分支同样不读 `%__strip` |
| `usr/lib/rpm/brp-strip-static-archive:7、15–20` | 首参取 STRIP，扫描非 debug 目录中的 ar，逐个 `$STRIP -g`；没有聚合逐档退出码 |

根内工具归属原始输出：

```text
/usr/bin/eu-strip                         elfutils-0.189-1.10.x86_64
/usr/bin/llvm-strip                       llvm-22.1.8-1.6.x86_64
/usr/lib/rpm/find-debuginfo.sh             rpm-build-4.14.1.1-1.4.x86_64
/usr/lib/rpm/brp-strip-static-archive      rpm-build-4.14.1.1-1.4.x86_64
```

证据 E0/`all-strip-macro-references.stdout`、`macro-query.stdout`、`macro-inputs.json`、`*.numbered.txt`。
结论限定本 LLVM spec、当前 Tizen 宏链及开启 debuginfo 的配置，不外推到其他包或关闭 debuginfo。
为独立证明每档 exit0，在 R/home/abuild/llvm-strip-audit-20261009 私有目录放宿主 strace 与其 loader/依赖，
先 `/bin/true` 探针验证，再只跟踪 `execve,exit_group`。未给构建根安装软件包，也未改宿主配置；tracer 子进程仍正常执行 Tizen ELF。
`tracer-probe.json`、`rpm-exec-exit.trace` 保存工具身份及实际后处理调用，不能只拿 rpmbuild 总退出码代替逐档状态。

## 2. 一次增量续跑的方法与配置

入口为 `E/resume_once.py`，实际通过 `gbs chroot --root R` 以 abuild 执行以下命令（未重新做 %prep）：

```sh
rpmbuild --define '_smp_mflags -j4' \
  --define '_srcdefattr (-,root,root)' --nosignature --target=x86_64 \
  --define '_build_create_debug 1' -ba --noprep \
  /home/abuild/rpmbuild/SOURCES/llvm.spec
```

外层沿用 `tools/build_llvm_x86_64.py` 的 systemd scope、GNU time、nice15/ionice3、30秒采样与回收；
18 GiB MemoryMax=19,327,352,832 B，MemorySwapMax=0，6/6/2 并发，debuginfo -j4。
转换 Source 自身仍为 4 workers，每个转换 clang 4 GiB 地址空间；链接不设 4 GiB AS。
宿主 MemAvailable <2 GiB 自动中止；没有增加构建时限或调整这些资源规则。
开始 `2026-10-09T19:08:48+08:00`，MemAvailable=21,926,617,088 B ≥16 GiB，磁盘=103,731,417,088 B ≥60 GiB，立即准入，无等待重试。

构建前 dry-run 显示 85 项 LLDB 头文件 staging，没有编译/链接待办。
正常 `%build` 重新 configure 后实际有 **100 项 Ninja 输出**：7 条编译（tf_xla_runtime dummy、5 个 sanitizer version-script dummy、llvm-config.cpp），
8 条归档/链接（libtf_xla_runtime.a、6 个 compiler-rt 共享库、bin/llvm-config），其余为 staging/生成项。
clang-22、lld、llvm-ar 没有重链。不能写成“完全空转”或“零重链”；完整任务列表已保存。
未因此改配置；这些重新生成的共享库、llvm-config 与所有其他非归档文件均接受 N 的逐字节门禁，不自动豁免。
原 dry-run 不是 reconfigure 后任务数的保证。完整内容在 `dry-run.log`、`build/build.log`、`build-resource-summary.json` 的 ninja_tasks。

配置门禁沿用 docs/35；已有 cache 首次检查通过，正常 configure 后按监测机制复核。
保存的关键行（`build/CMakeCache.txt`）：

```text
CLANG_LINK_CLANG_DYLIB:BOOL=OFF
CMAKE_BUILD_TYPE:STRING=Release
LLVM_ENABLE_ASSERTIONS:BOOL=No
LLVM_ENABLE_LTO:STRING=Thin
LLVM_LINK_LLVM_DYLIB:BOOL=OFF
LLVM_TARGETS_TO_BUILD:STRING=X86;ARM;AArch64;BPF
LLVM_USE_LINKER:UNINITIALIZED=lld
```

`CMAKE_CXX_FLAGS` 仍含 `-g2 -gdwarf-4 ... -g -O3 -flto=thin -fomit-frame-pointer`，无 `-Os`。
完整 flags、首次/重配门禁、命令与采样在 `build/cache-gate.json`、`build/CMakeCache.txt`、`build/resource-plan.json`、
`build/launch.json`、`build/samples.jsonl`、`build/linker-memory-observations.jsonl`。
时间与内存仅作为本次构建资源记录，不用来评价编译性能。

### 2.1 安装阶段转换已完成的记录

```text
2026-10-09T20:03:15+08:00 NATIVE_ARCHIVES_END 1791547395.190955 PASS 225
2026-10-09T20:03:15+08:00 + /usr/lib/rpm/find-debuginfo.sh -j4 --build-id-seed 22.1.8-1 --unique-debug-src-base llvm-22.1.8-1.x86_64 -S debugsourcefiles.list /home/abuild/rpmbuild/BUILD/llvm-22.1.8
```

Source 摘要：扫描 270 档，转换 225 档/3,853 个 bitcode 成员，跳过 45 档纯机器码运行库；原 11 个机器码成员按既有规则保留。
转换计算 `elapsed_seconds=1786.5090367794037`；含回写与清理的 BEGIN/END 日志间隔 **2,437 秒**（19:22:38→20:03:15）。
这两个数的边界不同，不互相代用。Source 状态 PASS，`large_files_deleted=true`；允许消失的 W 类汇总 1,920，强符号缺失 0。
这是安装阶段证据；最终 RPM 的 strip 后结构、索引及消费者另按 §3–§5 独立验收。

### 2.2 构建与资源结果

构建于 20:54:06 正常结束，`build/outcome.json` 的 command/outer exit 均 0，`problems=[]`，CMake 门禁通过。
仅执行一次增量入口，没有完整重建、失败后改配置或重试。

| 指标 | 实测与边界 |
| --- | --- |
| 总 wall | 6,318.154842 s（约 1:45:18） |
| scope MemoryPeak | 18,794,639,360 B = 17.503872 GiB；18 GiB cap；包含文件缓存，不能当单进程 RSS |
| memory.events | low/high/max/oom/oom_kill/oom_group_kill 全 0 |
| GNU time | user 16,871.11 s，sys 889.00 s，max RSS 3,472,020 KiB，exit 0，swaps 0 |
| 30 秒采样 | 209 次；宿主最低 MemAvailable 15,808,446,464 B；进程树 RSS 采样最大 7,789,813,760 B |
| `/home` 最低采样可用 | 41,450,336,256 B；这是运行期读数，60 GiB 是启动门槛 |
| Source 转换段 | 计算 1,786.509037 s；含回写/清理 2,437 s |
| Source 编译进程 | 最大 wait4 RSS 1,042,136 KiB；每进程 4 GiB AS 未变 |
| 转换期间 cgroup | 阶段末累计 MemoryPeak 11,181,322,240 B；该段采样 MemoryCurrent 最大 10,834,137,088 B，非纯编译器 RSS |
| 采样/日志线程 | `sampler_reaped=true`、`log_reader_reaped=true` |

完整数据为 `build-resource-summary.json`、`install-conversion-summary.json`、`build/time-v.txt`、`build/scope-after-rpm.json`、
`build/samples.jsonl` 和转换目录中的逐成员命令 JSON。没有因中间日志长时间不刷新判断“死机”：
find-debuginfo 20:03:15 开始，20:22:43 之后 check-buildroot，20:30:35 进入归档 strip，20:54:04 写完二进制包。
这些时间是本次环境下的记录，不作构建效率结论。

22 个二进制 RPM 合计 8,856,554,732 B，逐包大小/SHA 见附录 A；以 `rpm2cpio | cpio` 解包至独立 N38，所有命令退出 0。
`rpm-inventory.json`、`rpm-extraction-status.json`、`rpm-file-owners.json` 和各包元数据记录文件所有权及路径清单。

## 3. 新 RPM 验收

### 3.1 开发静态库与完整索引

**225/225 PASS**。对 N38 的归档用 `tools/inspect_llvm_archives.py` 解析；按成员序号、名称、同名出现序号区分身份，
与 B 的原归档比较数量和顺序。所有成员为 x86_64 ELF ET_REL，无 bitcode，无调试节。
符号索引与成员已定义外部符号的多重集合相等，不是只判断“非空”或条目数。
10 个成员的每函数一段抽查通过；完整记录 `new-archives-result.json` 的 development/section_samples、`new-archive-checks/`。
该文件的 `compiler_rt_status=PENDING_NEW_RULE` 表示此开发库工具不负责运行库；运行库最终结果为下节独立的 PASS，不能误读为未验收。

Source 全库符号对照汇总：允许消失的弱符号 W=1,920，其他缺失类别 0，强符号缺失 0；详见 `install-conversion-summary.json`。
225 个唯一路径包含 `libarcher_static.a`；该文件由 llvm-static-devel 与 libomp-devel 双归属，不重复计成第 226 个归档。

### 3.2 compiler-rt：可加载内容、结构和索引

**45/45 归档、1,964/1,964 成员 PASS**。相对 docs/13 的 H：

- 成员数量、名称、次序和同名身份一致；完整符号→成员索引映射一致；无调试节。
- 每个 SHF_ALLOC 节区的类型、flags、字节数及内容 SHA 一致，差异 0；NOBITS 按节区大小/类型处理。
- 不要求非加载 ELF 元数据逐字节相同。全部 1,964 个成员原始 ELF 字节有差异，属于已知的字符串表合并、空表处理、节区及符号索引重编号、偏移变化等。
- **64 个成员的 66 个共同节区 sh_entsize 变化**（主要 init/preinit 数组）；对应 docs/34 §1.3 的已登记类别。
- 进一步把本次每个成员 SHA 与 E34/llvm-strip-overlay/checks 中的 after-1 结果对照，1,964 个全部相同；没有新结构差异类别。

证据：`runtime-archives-result.json`、`runtime-structure-common-sections.json`、`verify-runtime.log`。
统计口径说明：原结构诊断把节区新增/删除时字段从有到无也纳入 union-of-fields，得到 entry_size_sections=3132；
该数不是共同节区 sh_entsize 的改变数。补充分类只比较两边均存在的节区，得到上面的 64/66；原始记录保留，没有修改门禁或重试产物。

这支持本次输入下“可加载内容及索引保留”，不是对所有 compiler-rt 功能的穷举证明；本轮要求的实际运行消费者见 §4–§5。

### 3.3 非静态库逐文件对照

**N38 对 N，共 17,689 个路径；差异恰为 270 个 `.a`；非静态库差异 0。**
比较文件集合、类型/模式、大小、SHA、软链接目标；完整逐项分类见 `new-vs-docs35-file-comparison.json`。
没有把 RPM 头部/压缩容器 SHA 当成文件内容相等，也没有豁免重生成的 llvm-config 或 compiler-rt `.so`。
以下三个工具在 N38、N 及已有 docs/13 基线 SHA 一致：

| 工具 | 字节 | SHA256 |
| --- | ---: | --- |
| clang-22 | 139,929,464 | `3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c` |
| lld | 83,539,336 | `7ebba1bbc8a46e086c4470373315dd31730dab8fe554987894e6689e45e071fc` |
| llvm-ar | 14,825,632 | `cad420e2daeb125b051a5d3f81b038b037c15fd30921ce880d4cc087d624313f` |

### 3.4 实际后处理调用

| 步骤 | 次数 | 证据：E/build/build.log |
| --- | ---: | --- |
| find-debuginfo，eu-strip 路径 | 1 | :8142；工具选择见 §1 宏链及 exec trace |
| brp-compress | 1 | :8687 |
| 独立 brp-strip | 0 | debuginfo 条件下原本不运行，与 docs/35 一致 |
| brp-strip-static-archive `/usr/bin/llvm-strip` | 1 | :8688 |
| brp-python-hardlink | 1 | :8689 |
| find-docs | 1 | :8690 |

原始关键行：

```text
2026-10-09T20:30:35+08:00 + /usr/lib/rpm/brp-strip-static-archive /usr/bin/llvm-strip
2026-10-09T20:32:34+08:00 + /usr/lib/rpm/brp-python-hardlink
```

`rpm-exec-exit.trace` 实测 **270 个唯一归档路径的 llvm-strip -g 均 exit_group(0)**，路径集合恰等于新包内全部 `.a`。
GNU/LLVM strip 格式错误行 0，strip 诊断错误行 0；不能仅用 brp 总退出码作此结论。
`postprocessing-result.json` 为 PASS，NATIVE_ARCHIVES_BEGIN/END 完整，Source 的 output/archives 与 output/members 大载荷已删除，摘要/逐成员证据保留。

## 4. 宿主消费者

### 4.1 原七项归档消费者

使用 `tools/verify_native_archive_consumers.py --baseline H --archives N38/usr/lib64`，
由 `E/run_stage.py` 包装为 18 GiB/swap0、nice15/ionice3、宿主低可用保护的 scope。
消费者编译/链接分开，编译 4 GiB AS，链接不设 AS；GNU ld 无 LTO/插件。
LLVM 头文件、llvm-config 和参考 opt 来自 H，归档来自本次 N38；H 的 clang/lld/resource 内容与本次工具一致已独立核验。
C++ 头文件来自宿主 GCC 13（compile-a.log 的 include search），libstdc++/glibc 来自宿主；
libxml2.so.16 来自独立 `W/temp/toolchain-runtime-baseline/libxml2/usr/lib64`，以显式宿主 loader 的 library-path 提供，没有装入宿主。

| 项目 | 结果 |
| --- | --- |
| A / GNU ld | PASS；PassBuilder O2 输出与 opt -O2 逐字一致，exe 47,387,472 B |
| A / lld | PASS；输出一致，exe 47,378,880 B |
| B / GNU ld | PASS；进程内 lld ELF 链接产物运行 exit 37，exe 84,455,656 B |
| B / lld | PASS；产物 exit 37，exe 84,467,760 B |
| 共享库 | PASS；GNU ld `-shared -z defs -z text`，dlopen 执行输出一致 |
| `--gc-sections` | PASS；GNU ld A 从 47,387,472 B 到 28,378,320 B，输出一致 |
| 原 bitcode 负对照 | PASS；无插件 GNU ld 如预期拒绝原归档，保存完整错误 |

总阶段 22.280471 s，scope peak 986,374,144 B，memory.events 全 0。
证据：`new-rpm-consumers/result.json`、该目录每次 compile/link/run 的 argv/日志/资源记录、`new-consumers-scope/`。

### 4.2 新 compiler-rt 运行消费者

直接使用 **N38 的 clang-22、resource-dir 和 llvm-profdata**；显式宿主 loader/独立 libxml2，
`--no-default-config --driver-mode=gcc -fintegrated-cc1 --target=x86_64-linux-gnu`。
源文件五个：asan_bad.c、asan_good.c、ubsan.c、profile.c、builtins.c；均在 `E/runtime-host/`，编译和链接分步。
两个链接器分别为 GNU ld.bfd 与本次 N38 的 lld；driver 展开逐项确认链接到本次 compiler-rt 资源目录，无 -flto/-plugin。

| 消费者及判据 | GNU ld | lld |
| --- | --- | --- |
| ASan 堆越界：非零退出，heap-buffer-overflow | PASS | PASS |
| ASan 无越界：退出 0 | PASS | PASS |
| UBSan 有符号溢出：runtime error + signed integer overflow | PASS | PASS |
| profile：运行生成非空 profraw，新 llvm-profdata merge 成功 | PASS | PASS |
| builtins：128 位除法结果正确，输入 `.o` 有未定义 `__divti3` | PASS | PASS |

示意调用（完整展开 argv 以 JSON 为准）：

```sh
# 编译仅此阶段限制 4 GiB AS
clang -O1 -g -fno-omit-frame-pointer -fsanitize=address -c asan_bad.c -o asan_bad.o
# 对 bfd/lld 分别只输入 .o 链接
clang --ld-path=LINKER asan_bad.o -fsanitize=address -o asan_bad
ASAN_OPTIONS=detect_leaks=0:halt_on_error=1 ./asan_bad
LLVM_PROFILE_FILE=result.profraw ./profile
llvm-profdata merge result.profraw -o result.profdata
```

实际输出含 `ERROR: AddressSanitizer: heap-buffer-overflow`、`runtime error: signed integer overflow`、`builtins-ok`。
10 项全部 PASS；阶段 6.218614 s、scope peak 186,019,840 B、无内存事件。
证据：`runtime-host/result.json`、每条命令 JSON/log、`runtime-host-scope/`、执行器 `verify_runtime_consumers.py`。
宿主显式 loader 模式下 ASan 栈中的模块标签可显示 loader 路径；本轮通过判据是检测/退出行为，未宣称该调用模式的符号化显示已经验收。
Tizen 下直接执行 ELF，另行检查以下结果。

## 5. Tizen 串行测试包：原 A/B 与新增运行库一起验收

采用 E36 已重建的本地 Base 仓库（107 包，原快照摘要相符），并加入本次 E/new-rpm-repo。
两个新根在 `/var/tmp/llvm-optimize-llvm-strip-tizen-20261009/gbs-root-llvm-strip-consumer-{bfd,lld}`，不是 LLVM 构建根，也不覆盖 docs/30 测试根。
两个包各执行一次、先 bfd 完成身份/环境核验再 lld；没有改变 gbs_llvm.conf 或 skip-conf-repos。

```sh
gbs -c W/gbs_llvm.conf build -A x86_64 -B TEST_ROOT   --threads 1 --include-all --define '_smp_mflags -j4'   -D E34/full-build/buildconfig.conf   -R E/new-rpm-repo -R E36/base-local-repo E/test-package-FLAVOR
```

外层 systemd scope：MemoryMax=6G、MemorySwapMax=0，nice15/ionice3，30 秒采样与 MemAvailable<2GiB 中止。
准入 >=8 GiB；实际两次立即满足。编译 prlimit AS=4GiB，链接不限 AS。
完整 argv、时间戳、stdout/stderr 在 `tizen-{bfd,lld}/launch.json`、`build.log`、`compiler-linker-commands.json`、`time-v.txt`。
所有 package Source/spec 保存在 `E/test-package-{bfd,lld}/`，未改 LLVM Source/spec。

BuildRequires 将 llvm-static-devel、llvm-devel、llvm、clang、compiler-rt 精确钉到 22.1.8-1。
每个根实际 114 包：107 来自重建 Base；7 个本次包为 clang、compiler-rt、libllvm、lldb、llvm、llvm-devel、llvm-static-devel。
与 docs/36 的 113 包对照，仅新增 compiler-rt-22.1.8-1，其余 NEVRA 零差异；
逐包缓存路径/SHA 来源见 `environment-verification.json`，采用保留的 `.repo.cache` F 记录与安装 NEVRA 一一匹配。
两个根各核对 270 个归档及 clang-22/opt/llvm-config/lld/llvm-profdata 5 工具 SHA，与 N38 全部一致。
C++/libc 头文件与动态运行库均来自 Tizen 根（GCC/libstdc++ 14.2.0、glibc 2.40）；没有混入宿主头文件或宿主链接器。

| 指标 | bfd | lld |
| --- | --- | --- |
| 准入 MemAvailable B | 23,173,316,608 | 23,269,236,736 |
| 总 wall s | 96.748626 | 58.472380 |
| scope MemoryPeak B | 6,442,450,944 | 5,697,142,784 |
| 宿主最低采样可用 B | 22,132,678,656 | 23,126,917,120 |
| memory.events max / oom / oom_kill | 294 / 0 / 0 | 0 / 0 / 0 |
| A 输出与根内 opt -O2 相同 | PASS | PASS |
| B 进程内链接生成物 exit 37 | PASS | PASS |
| ASan bad/good | PASS | PASS |
| UBSan signed overflow | PASS | PASS |
| profile 生成/合并 | PASS；224 B profraw → 640 B profdata | PASS；224 B → 640 B |
| compiler-rt builtins128位除法 | PASS | PASS |
| whole-archive 诊断 | exit 0，仅记录 | exit 0，仅记录 |
| 7 条 driver 链接器核验 | /usr/bin/ld.bfd，无 LTO/plugin | /usr/bin/ld.lld，无 LTO/plugin |

bfd 的 MemoryPeak 正好 6 GiB，max 事件表明发生了上限回收；它不是无上限自然内存需求，也不是 OOM。
两包均正常完成 %check 与打包，所有监测线程回收。运行时间不作 bfd/lld 性能比较。
本轮将新增运行库测试与既有 A/B 放在同一测试包；总共两个 gbs 测试包构建，没有多跑一对。

原始 PASS 行：

```text
TIZEN_CONSUMER_CHECK_PASS bfd A_IR_IDENTICAL B_GENERATED_EXIT_37
TIZEN_RUNTIME_CHECK_PASS bfd ASAN_BAD_GOOD UBSAN PROFILE BUILTINS
TIZEN_CONSUMER_CHECK_PASS lld A_IR_IDENTICAL B_GENERATED_EXIT_37
TIZEN_RUNTIME_CHECK_PASS lld ASAN_BAD_GOOD UBSAN PROFILE BUILTINS
```

bfd 证据行：build.log:1069、1144；lld：build.log:1068、1143。
ASan/UBSan 预期错误是测试成功条件，不算构建失败；完整输出及 profraw/profdata 保存在每根的 `check-outputs/`。

## 6. 叠在 356627 patchset 2 之后的提交补丁

全部验收通过后，在独立 `W/temp/llvm-strip-submission-20261009` checkout 做一次无交互 fetch：

```sh
GIT_TERMINAL_PROMPT=0 GIT_SSH_COMMAND='ssh -o BatchMode=yes -o NumberOfPasswordPrompts=0 -o ConnectTimeout=30'   git fetch --no-tags ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm refs/changes/27/356627/2
```

使用已有 SSH 身份，无输入密码/新凭据；W/llvm 本身未 fetch 或修改。

| 身份 | 值 |
| --- | --- |
| 356627 PS2，独立核验的父提交 | `67619ec8bbbac7238a6cfc33a481ccfbcd12206f` |
| PS2 的父 tizen_base | `cb67996861d070d68fec2b4c623eed7d20ba2e23` |
| 本地候选提交 | `f86dc69a7461a9708c2280fe49961c9730dd9beb` |
| 新 Change-Id | `Iac085555112855d60cc7591931e91466691db6b2` |
| 作者 | `FatTank <hao.lin@samsung.com>` |
| 标题 | `Use llvm-strip for x86_64 archive packaging`（43 字符） |
| 补丁 | `patches/llvm-strip/0001-Use-llvm-strip-for-x86_64-archive-packaging.patch` |
| 补丁 SHA256 | `49c5618226a8d281d9aed9427eb651391684e17a4e75bf68673d5cf2bf8761a5` |
| 目标 spec SHA256 | `58fc6ee88d9fde6db0011a4d0572abaf5a265f9b1186c04a968dd6618cb2ea4f` |

只改 `packaging/llvm.spec`，新增 4 行、删除 0 行：

```diff
+%ifarch x86_64
+# With debuginfo, __strip handles static archives; find-debuginfo uses eu-strip.
+%define __strip %{_bindir}/llvm-strip
+%endif
```

没有包含转换 Source、并发、优化或其他配方差异；Source 在父提交和候选提交均为 `6bd0546a…`。
干净 PS2 上 `git apply --check --index` PASS，随后应用并验证完整 tree 与候选 commit 一致（`9abaeb2c2f090970274a70234b0b009d988061bd`）。
`gerrit-parent.json`、`submission-commands.jsonl`、`submission-result.json`、`submission-spec.diff` 保存原始依据。
实测构建仍用已认证 S 配方；PS2 目标配方的参数覆盖已见 docs/37。本轮没有宣称在干净 PS2 上另做一次完整 LLVM 构建。
未推 Gerrit；由用户上传为独立后续 change。

提交说明全文：

```text
Use llvm-strip for x86_64 archive packaging

The platform now builds with LLVM. Use llvm-strip for the LLVM package's
x86_64 static archive post-processing as well.

Override __strip only for x86_64. With the current debuginfo-enabled
RPM macro chain, brp-strip-static-archive is its only active consumer;
find-debuginfo continues to use eu-strip. Keep archive conversion and
all other packaging steps unchanged.

llvm-strip changes compiler-rt member ELF structure, including string
tables, section numbering and some section entry sizes. All allocated
section types, flags, sizes and contents remain identical to the
GNU-stripped baseline, as do archive symbol-to-member mappings.

Validation: one incremental RPM rebuild, all 225 development archives
native with complete indexes and no DWARF, and all 45 compiler-rt
archives checked member by member. All 270 llvm-strip invocations exit
successfully. Non-static-library files, including clang, lld and
llvm-ar, are byte-identical to the prior package contents.

Host LLVM/lld API consumers and Tizen consumer packages pass with both
plugin-free GNU ld without LTO and lld. Compiler-rt tests pass on both
the host and Tizen with both linkers: ASan detects heap overflow and
accepts a valid program, UBSan diagnoses signed overflow, instrumented
profiles merge successfully, and 128-bit division uses the builtins
runtime and returns the expected result.

Limit this change to x86_64. Follow up on ARM after static archive
conversion is available and validated there.

Change-Id: Iac085555112855d60cc7591931e91466691db6b2
Signed-off-by: FatTank <hao.lin@samsung.com>
```

## 7. 收尾与自检

1. 保全 docs/35 原件：22 RPM 在移动前后与附录 A 摘要相同；另一个 SRPM 按移动前后 SHA/inode 保全，历史摘要缺口如 §0.1 所述。
2. 清理边界：仅第 1 类旧解包载荷，达到 75 GiB 即停；第 2/3 类没有执行。最终保护文件与原件复核见 `final-integrity.json`。
3. 构建/测试次数：1 次 -ba --noprep 增量、2 次串行 Tizen 测试包；没有完整 LLVM 重建、BOLT、性能校准或 Chromium 构建。
4. 归档/非归档/后处理/宿主/Tizen 门禁全部 PASS；没有真实门禁失败后的修改重试。
5. W/llvm/spec、gbs_llvm.conf、转换 Source、原归档修复补丁及 docs/25–37 摘要不变；S 与 R 的试验 spec 只增三行。原通用认证指纹未放宽。
6. scope/日志/采样器已回收，项目锁释放证据为 `lock-released.json`；最终进程与 scope 核验为 `final-processes.json`。
7. 只向 GitHub 发布本报告、STATUS 与新补丁，不向 Gerrit 推送。可评审不等于已合入，也不扩大到 ARM。

## 附录 A：本次 22 个二进制 RPM

均位于 `R/home/abuild/rpmbuild/RPMS/x86_64/`；原件仍在 R，E/new-rpm-repo 为本次测试用的硬链接仓库。
docs/35 的旧包则单独保存在 rpms-docs35，二者不能混用。

| RPM | 字节 | SHA256 |
| --- | ---: | --- |
| `clang-22.1.8-1.x86_64.rpm` | 310,008,958 | `6317baba9fd2e1b99d5076d85b08849b556245302618b7d01239c1245d305ed1` |
| `clang-debuginfo-22.1.8-1.x86_64.rpm` | 2,928,314,502 | `a82ec766c3d98f6275eb33e46dd462105d75eb1776d16431a8767f94761a2976` |
| `clang-devel-22.1.8-1.x86_64.rpm` | 4,098,754 | `67d1f53e862e6bdcbf5735061f5f1b696d2a58405c3cdb846d82216cde4fca5d` |
| `clang-devel-debuginfo-22.1.8-1.x86_64.rpm` | 5,729,462 | `8100a26d11e24ade599c48769d27cdb8bae87c88e265a4f8042cb7a0dd1395d0` |
| `compiler-rt-22.1.8-1.x86_64.rpm` | 3,785,326 | `363d91077e776cfe422f387a2190a2a600a2f4d7c0c66bd0e037f49f7661fdde` |
| `compiler-rt-debuginfo-22.1.8-1.x86_64.rpm` | 1,290,302 | `92120c27f940c92395fa73a49e3d27dd7b25c22683996e82227a3a409104a20d` |
| `libllvm-22.1.8-1.x86_64.rpm` | 23,647,078 | `01c75e07bd5f082c85319776e5f53ce2b3ddd7d07ec91e54e99df611aaed0120` |
| `libllvm-debuginfo-22.1.8-1.x86_64.rpm` | 198,056,690 | `1f121f73fcc8a37f3429d15ee6f1bc6bd255ad8de3f4821fabc0f0a742bc346a` |
| `libomp-22.1.8-1.x86_64.rpm` | 373,498 | `4fafffd4b05d3dc56f5362a9740590d327748f3a2f374aefaa173d209a7702c1` |
| `libomp-debuginfo-22.1.8-1.x86_64.rpm` | 1,142,482 | `434252eb9201096aaa8700786e93e60675848a76c038b4ae9d58d572c4d37613` |
| `libomp-devel-22.1.8-1.x86_64.rpm` | 25,398 | `52169c48f2153483403cbefc648466d91184284bdf354527e925fea8467a0fd2` |
| `lldb-22.1.8-1.x86_64.rpm` | 30,767,866 | `77359efe863d26e6e9e13f4b0b5d046ebe15199fb65045430e8251a5ac7a49ed` |
| `lldb-debuginfo-22.1.8-1.x86_64.rpm` | 332,846,294 | `1287c05b3013e19ace1e22dfed438462466bc9b26e11b8fe798c95c60b4e5ffc` |
| `lldb-devel-22.1.8-1.x86_64.rpm` | 30,521,594 | `743c1d72e49c2d41b79bf3cc8e8bd69bfa1fa50ef28950b1bd61c38f24b345c5` |
| `lldb-devel-debuginfo-22.1.8-1.x86_64.rpm` | 279,581,334 | `1de3593e1b999230e28536cc1fac02cc4ccf4e6f3e955c2c26783c714029049a` |
| `llvm-22.1.8-1.x86_64.rpm` | 410,620,978 | `9cd1934274f76805143e09ff35b1b08f7bb2445edbbec88e8b3a214b79dccbbb` |
| `llvm-debuginfo-22.1.8-1.x86_64.rpm` | 3,842,672,078 | `483551ea0ef740f82629c06995e984f3b3708b4f7013f8ad7c07a1840ffa5362` |
| `llvm-debugsource-22.1.8-1.x86_64.rpm` | 43,654,298 | `ddbd5aa928bf3e65b1d244bac6ea7bbb7effc8f83247e2c300a275fe3ee0b58d` |
| `llvm-devel-22.1.8-1.x86_64.rpm` | 41,190,830 | `c4364a220fcc135f6a156217d6a7241dfe39790845542738d26390e0c8206774` |
| `llvm-devel-debuginfo-22.1.8-1.x86_64.rpm` | 308,602,810 | `76895c51156509c8dbe91d330495262e9b21a03d3ff7d2203e9f73fdb147534d` |
| `llvm-static-devel-22.1.8-1.x86_64.rpm` | 59,587,878 | `491cc6f17a3a637ca8be4899502cd784634e8789868fc0773a39782436e488e4` |
| `python-clang-22.1.8-1.x86_64.rpm` | 36,322 | `a919ec8cb0bdb1c13f8b7b4d29ede91413611590feab2d7a2d4eb2e6c9b8d5f8` |

## 附录 B：原始证据定位与复核入口

所有路径以 §0 的 E（工作区绝对路径可展开）为根；这些大文件/日志只在本机，未上传 GitHub。
下面脚本是本轮证据工具，不是新增 spec Source；复核日志优先，不应重复执行一次性构建入口。

| 范围 | 原始证据/入口 |
| --- | --- |
| 起始核验/锁 | processes-start.json、lock-acquired.json、identity-result.json、protected-start.json |
| rename 与清理 | preserved-rpms.json、cleanup-1-manifest.json、cleanup-1-summary.json、cleanup-result.json、df-after-cleanup-1.log |
| spec/指纹 | prepare-resume.json、trial-three-lines.diff、exported-three-lines.diff、llvm-strip-trial-fingerprint.json、trial-fingerprint-tests.json |
| 宏链 | E0 的 commands.jsonl、all-strip-macro-references.stdout、macro-query.stdout、带行号全文与 macro-inputs.json |
| 构建 | resume_once.py、build/launch.json、build/build.log、build/CMakeCache.txt、build/time-v.txt、build/samples.jsonl、build/outcome.json |
| 270 次 strip | rpm-exec-exit.trace、tracer-probe.json、postprocessing-result.json |
| 新 RPM/解包 | rpm-inventory.json、rpm-extraction-status.json、rpm-file-owners.json、逐包元数据 |
| 225 开发归档 | verify_development_archives.py、new-archives-result.json、new-archive-checks/ |
| 45 运行库 | verify_runtime_archives.py、runtime-archives-result.json、analyze_runtime_structure.py、runtime-structure-common-sections.json |
| 全文件差异 | compare_new_files.py、new-vs-docs35-file-comparison.json |
| 七宿主消费者 | new-rpm-consumers/、new-consumers-scope/；仓库 tools/verify_native_archive_consumers.py |
| 宿主运行库 | verify_runtime_consumers.py、runtime-host/、runtime-host-scope/ |
| 两 Tizen 包 | prepare_tizen_packages.py、test-package-{bfd,lld}/、run_tizen_consumer.py、tizen-{bfd,lld}/ 的 build.log/launch.json/check-outputs/result.json/installed-identities.json/environment-verification.json |
| 提交补丁 | fetch_parent.py、make_strip_submission.py、gerrit-parent.json、submission-result.json、submission-commands.jsonl、commit-message.txt |
| 收尾 | final-integrity.json、final-processes.json、lock-released.json、git-publication.log |

`temp/` 原始输出不在远端；评审所需关键参数、结论、SHA 和提交说明已在本文自包含列出。
