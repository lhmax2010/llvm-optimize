# 自研优化版 x86_64 LLVM：固定快照、RPM 续跑与吞吐基线

更新时间：2026-09-17 14:30:13 +0800。

> 2026-09-18 更新：本文第 11 节中的加法容量模型及“完整基线构建拒绝”结论已由
> [docs/14 的实测准入判据](14_bolt_feasibility.md) 替代。相同基线配置允许在 18 GiB cap 下重建；
> PGO 完整构建仍为 NO。下文保留 2026-09-17 的历史记录。

## 1. 状态、范围与路径

**debuginfo OOM 已解除，正常产出 22 个二进制 RPM 和 1 个源码 RPM；最终 RPM 的五个工具均通过静态 LLVM 依赖检查。**
在独立复制的构建根使用正常 `rpmbuild -ba --noprep`、命令行 `_smp_mflags -j4` 续跑，
MemoryMax 保持 18 GiB。10 个真实 ARM TU 采集成功，两轮完整校准噪声底 **0.755%**，
通过 3% 门禁；正式基线与 bundled clang 18 独立参考已完成。没有构建 Chromium 或向 Gerrit 推送。

**交付边界：** `llvm-static-devel` 抽查归档存在 GNU strip 删除符号索引的问题，尚未完成消费者链接验收；
这项限制与原始证据在第 12 节明确列出。PGO 完整构建按当前资源预算为 NO，单独 BOLT 内存需求为 UNKNOWN。
第 7 节是最终剥离后 RPM 工具数据，第 10 节是本次实测基线，第 11 节是内存画像。

源码基线为工作区 LLVM `f111162e94aa48ed367c9d2c039456c70e7160ae`，保留 spec 的
-O3、ThinLTO、-fomit-frame-pointer、静态链接 LLVM 库及 x86_64 MLGO 设置。
没有回退到已安装 RPM 的配方。验证分两层：本机基准台用于快速筛选 LLVM 变体；
最终验收是专用服务器 Chromium 全量构建耗时，本机不执行后者。基准排序是否与
Chromium 全量结果方向一致，仍需后续数据验证。

本轮沿用用户已确认的前提，不重新论证：构建树五工具无 libLLVM/libclang-cpp NEEDED；
原 CMake 门禁 297.775 秒通过；7634 个编译/链接任务完成，wall 2:33:40，
CPUUsageNSec 68291713114000；失败位于 `%install` 之后的 debuginfo 提取，根内
`.rpmmacros:133` 的 -j40 通过 RPM macros:183–184 传入；单次 clang-22 链接已观察到
16.83 GiB 高水位，原 8 GiB 预算假设失效。旧现场和原始日志全部保留。

| 符号 | 本机实际路径 |
| --- | --- |
| W | `/home/linhao/Toolchain/development/llvm-optimize` |
| S | `W/llvm/packaging/llvm.spec` |
| Q | `W/temp/snapshot-resolution-20260917` |
| A | `W/temp/snapshot-archive` |
| P | `W/temp/baseline-preflight-20260917` |
| L | `W/temp/baseline-build-20260917` |
| J | `W/temp/baseline-resume-20260917` |
| B | `W/temp/gbs-root-x86_64-baseline` |
| R0 | `B/local/BUILD-ROOTS/scratch.x86_64.0`（原 OOM 现场） |
| R1 | `W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0`（独立续跑根） |
| E | `J/rpm-source/rpm-4.14.1.1`（匹配安装版本的 RPM 源码） |
| U | `A/tizen-unified-toolchain_20260814.092727/build.conf` |
| ARMROOT | `/home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0` |
| TC | `W/temp/toolchain-baseline/usr`（最终 RPM 解包工具链） |
| RT | `W/temp/toolchain-runtime-baseline/libxml2/usr/lib64`（独立运行库） |

下文 `S:行号`、`R0/路径:行号` 等使用这张表展开；原始输出均落盘于 temp/，不提交。

## 2. reference 解析与固定快照

先取得两个项目的目录索引和 reference 目录索引，沿索引中的 `build.xml` 链接读取
根元素下的 `<id>`，再请求同名快照的 `repos/standard/packages/repodata/repomd.xml`。
**reference 和固定快照的 repomd.xml 按完整字节比较相等**；归档后再次获取 reference
并比较，确认解析期间没有发生切换。日期来自 XML 的 id，没有根据修改日期推断。

原始 XML 摘录（Q/*-reference-build.xml，全文亦在 Q/resolution.log）：

```xml
<id>tizen-base-toolchain_20260912.061113</id>
<base_id url="http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/">reference</base_id>

<id>tizen-unified-toolchain_20260814.092727</id>
<base_id url="http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/">tizen-base-toolchain_20260813.050338</base_id>
```

Unified 的 `base_id` 是它原始构建时的 Base 身份，不能误当成 Unified 自己的快照 id。
本任务按决策固定两个 reference 各自当前的目标，不擅自改选该历史 base_id。

| 项目 | 已解析快照 | reference / 快照 HTTP | repomd.xml SHA256（双方相同） |
| --- | --- | --- | --- |
| Tizen-Base-Toolchain | `tizen-base-toolchain_20260912.061113` | 200 / 200；二次复核仍一致 | `68b93454b4800a462e228260b11926a63ad8bba0589cc3f1a7dc4f0525bc2a74` |
| Tizen-Unified-Toolchain | `tizen-unified-toolchain_20260814.092727` | 200 / 200；二次复核仍一致 | `e7af3f222f0ce958678d964589f2d156e8b47ba463ac0b3b0b96c74663382200` |

完整 GET URL、时间、HTTP 状态、字节数、SHA256、XML 原文和 RESOLVED 记录在
Q/resolution.log；解析脚本保存在 Q/resolve.py。以下为实际包源：

- https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260912.061113/repos/standard/packages/
- https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260814.092727/repos/standard/packages/

### 配置变更

改前 SHA256：`6696073dc5a459c5b90ed51d1a5d9c90eb1505d3989615ea729f993e046deb50`
改后 SHA256：`a3fea7732532db26c11b88407464e0274a6d8b4277623364fe16b6980181b03f`

改动仅涉及 URL 行：删除失效的重复 URL 与历史 URL 注释，每节保留一个固定快照 URL。
未改变 profile、repo 顺序或 general.buildroot；命令行 `-B` 指定本次全新构建根。
改前/改后原文件分别保存在 Q/gbs_llvm.conf.before 和 Q/gbs_llvm.conf.after。
完整 diff（Q/config.diff）：

```diff
--- a/gbs_llvm.conf
+++ b/gbs_llvm.conf
@@ -6,11 +6,7 @@
 repos = repo.base-standard, repo.unified-standard

 [repo.base-standard]
-url=https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/reference/repos/standard/packages/
-#url=http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260722.045200/repos/standard/packages/
-url=http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260804.124315/repos/standard/packages/
+url=https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260912.061113/repos/standard/packages/

 [repo.unified-standard]
-url=https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/reference/repos/standard/packages/
-#url=http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260725.003315/repos/standard/packages/
-#url=https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260804.223836/repos/standard/packages/
+url=https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260814.092727/repos/standard/packages/
```

### 元数据归档

每个目录存放 repomd.xml、解压后的 primary.xml、下载到的原始压缩文件、build.conf、
reference-build.xml、比较用的两份 reference repomd，以及包含 URL/摘要的 manifest.json。
下载内容与 repomd.xml 声明的 checksum 逐项相符。元数据用于日后核对，**不是全部 RPM
包的离线镜像**；不会承诺仅凭这些 XML 就能在远端包被清理后重建。

| 归档目录（相对 W） | primary.xml 字节数 | 解压后 primary.xml SHA256 | build.conf SHA256 |
| --- | ---: | --- | --- |
| `temp/snapshot-archive/tizen-base-toolchain_20260912.061113/` | 4079780 | `5cf28889b7f9706281c019898e4c54e93e04c23d5b813f8f42eca03d7da16138` | `b8a19c32e5e153a745e3012da6dca3e3077e6a37b2b76cbf773743b6d8c9ff3c` |
| `temp/snapshot-archive/tizen-unified-toolchain_20260814.092727/` | 21165478 | `beba1f62d83b1ab105ae1a114c8fa6277bc037615c090cef9547489e7e22d286` | `1e7610b6a922d27b80eb59c1c78bdf716f7de2e8e24700e0ee7c62522739ed52` |

这些文件都在被 Git 忽略的 temp/。Unified primary.xml 超过 10 MB，未进入 Git。

## 3. 完整预检结果与 `_toolchain`

实际执行（未带 `--run`），退出码 0：

```sh
tools/build_llvm_x86_64.sh --log-dir temp/baseline-preflight-20260917
```

原始尾部关键输出（Q/preflight-console.log）：

```text
1|clang
[exit=0]
MEMORY MECHANISM systemd
PREFLIGHT PASS; no spec edit and no build. Use --run to proceed.
```

本报告中的上述四行去除了时间前缀；完整原始输出保存在 P/commands.log。
P/repositories.json 记录两个固定源的 HTTP 200、x86_64 包清单及 build.conf 摘要。

### 包与 BuildRequires

先用本机 GBS 后端 Build::read_config("x86_64", U) 和 Build::Rpm::parse 解析 S，
保留 GBS 的 `opensuse_bs=0` 定义；这只是读取 spec，不运行构建。
结果见 Q/spec-build-requires.json。随后从归档 primary.xml 的 x86_64/noarch 包名及
RPM provides 中解析直接 BuildRequires，原始匹配输出在 Q/dependencies.log/json。
后续整个依赖闭包由真正 GBS 的依赖展开和安装检查。

| Base 必须存在的 x86_64 包 | 实际版本-Release | 结果 |
| --- | --- | --- |
| clang | 22.1.8-1.6 | PASS |
| llvm | 22.1.8-1.6 | PASS |
| cmake | 3.31.2-1.2 | PASS |
| ninja | 1.13.1-1.9 | PASS |
| glibc | 2.40-1.10 | PASS |
| rpm-build | 4.14.1.1-1.4 | PASS |
| binutils | 2.43-1.9 | PASS |

| spec 实际 BuildRequires | 提供包（均来自固定 Base） | 版本-Release |
| --- | --- | --- |
| cmake | cmake.x86_64 | 3.31.2-1.2 |
| python3 | python3.x86_64 | 3.14.2-1.6 |
| python3-devel | python3-devel.x86_64 | 3.14.2-1.6 |
| patchelf | patchelf.x86_64 | 0.16.1-1.8 |
| binutils-devel | binutils-devel.x86_64 | 2.43-1.9 |
| libxml2-devel | libxml2-devel.x86_64 | 2.15.1-1.7 |
| ninja | ninja.x86_64 | 1.13.1-1.9 |

S:51–60 的 sed 在 `llvm_release_build=1` 分支，本次分支为 0，故不是本次实际
BuildRequires。所有实际 7 项均通过，没有用“按惯例存在”填空。

### 宏来源

GBS 按 gbs_llvm.conf:6 的 repo 顺序读取 repomd 中的 build 元数据，最后的 Unified
配置生效。实现依据：`/usr/lib/python3/dist-packages/gitbuildsys/utils.py:430–447,463–496`。
本次重新下载的 U:146–184 是非架构专属的 Macros 段，其中：

```text
150 %__cc_clang %{_host}-clang
151 %__cxx_clang %{_host}-clang++
161 %_toolchain %{?_toolchain_override}%{!?_toolchain_override:clang}
166 %__cc %{expand:%%{__cc_%{_toolchain}}}
167 %__cxx %{expand:%%{__cxx_%{_toolchain}}}
```

用 `/usr/lib/build/queryconfig --dist U --archpath x86_64 rawmacros` 得到宏文件，
再用 `rpm --macros /usr/lib/rpm/macros:<生成文件> --eval '%{defined _toolchain}|%{_toolchain}'`
实际得到 `1|clang`。P 与 L 的 commands.log 都记录了本次复核。
因此 S:11–16 取真分支，`_toolchain_override=clang`、`llvm_release_build=0`，
S:229–236 的 lld/ThinLTO/llvm-ar/llvm-ranlib 参数应生效。
没有增加 `--define _toolchain`。

U:121–127 的 mlgo_build_jobs=6 只在 armv7l/aarch64 分支，x86_64 不被其覆盖。
S:7–8 自己默认启用 x86_64 MLGO；S:48 的默认任务数可按允许范围调整。

## 4. 首轮构建资源与允许的 spec 改动

以下记录首轮完整构建的历史资源和命令；8 GiB 链接预算已经失效，不作为后续构建的安全依据。

构建前原始资源输出（L/commands.log，实际启动前又重新检查精确值）：

```text
2026-09-17T08:43:32+08:00 $ nproc
2026-09-17T08:43:32+08:00 20
[exit=0]
2026-09-17T08:43:32+08:00 $ free -g
2026-09-17T08:43:32+08:00                total        used        free      shared  buff/cache   available
Mem:              30           7           9           0          14          22
Swap:              3           0           3
[exit=0]
2026-09-17T08:43:32+08:00 $ df -h /home/linhao/Toolchain/development/llvm-optimize/temp
2026-09-17T08:43:32+08:00 Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       1.8T  672G  1.1T  39% /home
[exit=0]
2026-09-17T08:43:32+08:00 $ nproc
2026-09-17T08:43:32+08:00 20
[exit=0]
2026-09-17T08:43:32+08:00
```

精确资源值：MemAvailable = 24485412864 B = 22.803818 GiB；
可用磁盘 = 1146346184704 B = 1067.618080 GiB。
均通过 16 GiB / 60 GiB 门槛，见 L/resource-plan.json。

| 限制 | 实际设置 | 依据 |
| --- | --- | --- |
| systemd MemoryMax | 18 GiB | floor(可用 GiB) - 4，预留至少 4 GiB |
| MemorySwapMax | 0 | 不让构建 scope 通过 swap 扩张内存 |
| GBS 包并发 | 1 | --threads 1 |
| Ninja 总任务数 | 4 | S:48 |
| LLVM compile/link 池 | 4 / 1 | S:274–275 |
| 历史链接预算（已被实测否定） | 1 × 8 GiB < 13.682291 GiB | 严格小于可用内存的 60% |
| 其余预算 | 编译 4 × 2 GiB + 开销 2 GiB | 与链接合计 18 GiB；编译 2 GiB 是预算假设，不是实测 |
| CPU / I/O 调度 | nice 15 / ionice idle（-c3） | L/runtime-scope-check.log、L/priority-check.log 实测 |

本次仅修改的 spec diff（L/spec-concurrency.diff）：

```diff
diff --git a/packaging/llvm.spec b/packaging/llvm.spec
index 54a07ce84218..6e159c542234 100644
--- a/packaging/llvm.spec
+++ b/packaging/llvm.spec
@@ -45,7 +45,7 @@ Source1002: mlgo_arm_model.tar.gz
 Source1003: mlgo_aarch_model.tar.gz
 Source1004: mlgo_x86_model.tar.gz

-%{!?mlgo_build_jobs: %define mlgo_build_jobs 6}
+%{!?mlgo_build_jobs: %define mlgo_build_jobs 4}
 %{!?mlgo_verify_configure_only: %define mlgo_verify_configure_only 0}

 BuildRequires: cmake
@@ -271,8 +271,8 @@ cmake \
     -DLLVM_LIBDIR_SUFFIX=`echo %{_lib} | sed s/lib//g` \
     -DCLANG_RESOURCE_DIR="../%{_lib}/clang/%{llvm_version}" \
     -DLLVM_BINUTILS_INCDIR=/usr/include \
-    -DLLVM_PARALLEL_COMPILE_JOBS=6 \
-    -DLLVM_PARALLEL_LINK_JOBS=2 \
+    -DLLVM_PARALLEL_COMPILE_JOBS=4 \
+    -DLLVM_PARALLEL_LINK_JOBS=1 \
 %if %{with mlgo}
 %ifarch armv7l aarch64 x86_64
     -DTENSORFLOW_AOT_PATH="${MLGO_AOT_DIR}/mlgo_sysroot" \
```

真实执行入口：

```sh
tools/build_llvm_x86_64.sh --run --log-dir temp/baseline-build-20260917
```

脚本在执行前输出的完整底层命令（L/launch.json、commands.log）：

```sh
/usr/bin/time -v -o /home/linhao/Toolchain/development/llvm-optimize/temp/baseline-build-20260917/time-v.txt systemd-run --user --scope --unit=llvm-baseline-ce682bfbada047fcb575eaeebd4993ba.scope -p MemoryMax=18G -p MemorySwapMax=0 nice -n 15 ionice -c3 gbs -c /home/linhao/Toolchain/development/llvm-optimize/gbs_llvm.conf build -A x86_64 -B /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-baseline --threads 1 --include-all -D /home/linhao/Toolchain/development/llvm-optimize/temp/baseline-build-20260917/buildconfig.conf /home/linhao/Toolchain/development/llvm-optimize/llvm
```

`-D` 指向已下载并复核的原始 build.conf，内容没有增删宏；`--include-all` 让三处
并发修改进入源码导出。源工作树在启动前经过检查，其他源码/spec 内容没有改变。
GBS scope 实际名为 `llvm-baseline-ce682bfbada047fcb575eaeebd4993ba.scope`。

本轮没有再次修改 spec；上面的 diff 是相对源码 HEAD 累计保留的三处并发改动。

### 首轮失败与本轮约束

首轮 OOM 由用户指定的 -j40 debuginfo 根因解释，本轮采用已经批准的命令行
`--define "_smp_mflags -j4"`。不增加 MemoryMax，不关闭 debuginfo，不修改优化参数。
首轮 scope 为 oom-kill，`L/scope-final.log`、`L/scope-journal.log`、`L/outcome.json`
记录失败及采样线程回收；`L/cleanup-verification.json` 记录旧构建已无残留进程。
外层 time 的 Max RSS 只反映其可统计到的进程，不代表整个 cgroup 的内存；全流程及
单个链接器高水位在内存画像一节分开报告。

## 5. CMake 预期与配置阶段门禁

本次 x86_64 预期参数如下，出处为 S；G 表示根内展开的 `_host`，PFX 表示 `_prefix`，
LIB 表示 `_lib`，此节表中的 A 表示源码目录的 `mlgo_verify_assets`（与归档路径缩写无关）。
不能把宿主 RPM 的 `_host` 当成 Tizen 根的实测 triple。

| 参数 | x86_64 预期 | spec 行号或来源 |
| --- | --- | --- |
| Generator / source | Ninja / `../llvm` | S:219,293 |
| `TIZEN` | 1 | S:220 |
| `CMAKE_C_COMPILER` | `%__cc`，按 U 展开为 `G-clang` | S:221；U:150,161,166 |
| `CMAKE_CXX_COMPILER` | `%__cxx`，按 U 展开为 `G-clang++` | S:222；U:151,161,167 |
| `LLVM_HOST_TRIPLE` | G | S:223 |
| `LLVM_DEFAULT_TARGET_TRIPLE` | G | S:224 |
| `LLVM_TARGET_TRIPLE_ENV` | G | S:225 |
| `CMAKE_ASM_FLAGS` | 清理原 flags 后追加 `-O3 -flto=thin -fomit-frame-pointer` 的 CFLAGS | S:189–206,226 |
| `CMAKE_C_FLAGS` | 同 CFLAGS | S:227 |
| `CMAKE_CXX_FLAGS` | 清理原 flags 后追加 `-O3 -flto=thin -fomit-frame-pointer` 的 CXXFLAGS；必须无 `-Os` | S:197–206,228 |
| `CMAKE_SHARED_LINKER_FLAGS` | `-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections` | S:229–230 |
| `CMAKE_EXE_LINKER_FLAGS` | 同上一行 | S:231 |
| `LLVM_USE_LINKER` | lld | S:232 |
| `LLVM_ENABLE_LTO` | Thin | S:233 |
| `CMAKE_RANLIB` | `%{_bindir}/llvm-ranlib` | S:234 |
| `CMAKE_AR` | `%{_bindir}/llvm-ar` | S:235 |
| `LLVM_ENABLE_ASSERTIONS` | No，即布尔 OFF | S:237 |
| `LLVM_ENABLE_RTTI` | ON | S:238 |
| `CMAKE_BUILD_TYPE` | Release | S:239–240 |
| `LLVM_TARGETS_TO_BUILD` | `X86;ARM;AArch64;BPF` | S:241 |
| `CLANG_ENABLE_ARCMT` | OFF | S:257 |
| `LLVM_BUILD_LLVM_DYLIB` | ON | S:258 |
| `CLANG_BUILD_CLANG_DYLIB` | ON | S:259 |
| `LLVM_ENABLE_PROJECTS` | `clang;lldb;clang-tools-extra;lld;compiler-rt;openmp` | S:260 |
| `LLVM_ENABLE_PER_TARGET_RUNTIME_DIR` | OFF | S:261 |
| `LLVM_BUILD_EXAMPLES` / `LLVM_INCLUDE_EXAMPLES` | OFF / OFF | S:262–263 |
| `LLVM_BUILD_TESTS` / `LLVM_INCLUDE_TESTS` | OFF / OFF | S:264–265 |
| `LLVM_ENABLE_DOXYGEN` | OFF | S:266 |
| `LLVM_BUILD_DOCS` / `LLVM_INCLUDE_DOCS` | OFF / OFF | S:267–268 |
| `LLVM_OPTIMIZED_TABLEGEN` | ON | S:269 |
| `CMAKE_INSTALL_PREFIX` | PFX | S:270 |
| `LLVM_LIBDIR_SUFFIX` | LIB 去掉 `lib` | S:271 |
| `CLANG_RESOURCE_DIR` | `../LIB/clang/22` | S:18,272 |
| `LLVM_BINUTILS_INCDIR` | `/usr/include` | S:273 |
| `LLVM_PARALLEL_COMPILE_JOBS` | 4（本次资源计划已应用） | S:274 |
| `LLVM_PARALLEL_LINK_JOBS` | 1（本次资源计划已应用） | S:275 |
| `TENSORFLOW_AOT_PATH` | `A/mlgo_sysroot` | S:278 |
| `LLVM_MLGO_EXPORT_TF_XLA_RUNTIME` | OFF | S:279 |
| `LLVM_MLGO_EMBED_TF_XLA_RUNTIME_OBJECTS` | A 下的 5 个 XLA runtime objects，见下文 | S:212,280 |
| `LLVM_OVERRIDE_MODEL_HEADER_INLINERSIZEMODEL` | `A/InlinerSizeModel.h` | S:281 |
| `LLVM_OVERRIDE_MODEL_OBJECT_INLINERSIZEMODEL` | `A/InlinerSizeModel.o` | S:282 |
| `LLVM_OVERRIDE_MODEL_HEADER_REGALLOCEVICTMODEL` | `A/RegAllocEvictModel.h` | S:283 |
| `LLVM_OVERRIDE_MODEL_OBJECT_REGALLOCEVICTMODEL` | `A/RegAllocEvictModel.o` | S:284 |
| `LLVM_LINK_LLVM_DYLIB` | 未传，源码默认 OFF | `llvm/llvm/CMakeLists.txt:912` |
| `CLANG_LINK_CLANG_DYLIB` | 未传，默认继承前者，即 OFF | `llvm/clang/CMakeLists.txt:309` |

5 个 runtime object 均位于 `A/xla_runtime_objects/`：
`xla_compiled_cpu_function.cc.o`、`cpu_function_runtime.cc.o`、
`custom_call_status.cc.o`、`executable_run_options.cc.o`、
`runtime_single_threaded_matmul_f32.cc.o`（S:212）。

MLGO 为 x86_64 默认开启（S:7–8），采用 S:165–166 的 x86 模型资产；
因此 S:286–287、290–291 的两个 `MODEL_PATH=none` 分支不在本次预期清单。
`LLVM_TARGET_ARCH` 只出现在其他架构分支；x86_64 未传。
没有擅自增加其他 CMake 参数，也没有使用 configure-only 宏。

两个 LINK_DYLIB 开关的默认 OFF 分别来自 `llvm/llvm/CMakeLists.txt:912` 和
`llvm/clang/CMakeLists.txt:309`。BUILD_DYLIB=ON 仍会构建共享库，不代表工具链接这些库。
最终仍须通过工具 NEEDED 验证。断言的 No 与 OFF 在 CMake 中等价。

### 首轮实际配置门禁

脚本自 GBS 启动起 900 秒内必须发现并校验主构建目录的 CMakeCache；任何必需字段
缺失或不符均中止，两个并发池也必须与计划一致。

门禁用时：297.775 秒；原 Cache：`/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-baseline/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/CMakeCache.txt`；结果：PASS。

CMakeCache 原始关键行（完整副本 L/CMakeCache.txt）：

```text
CLANG_LINK_CLANG_DYLIB:BOOL=OFF
CMAKE_BUILD_TYPE:STRING=Release
CMAKE_CXX_FLAGS:STRING=  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument   -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables  -g -O3 -flto=thin -fomit-frame-pointer
LLVM_ENABLE_ASSERTIONS:BOOL=No
LLVM_ENABLE_LTO:STRING=Thin
LLVM_LINK_LLVM_DYLIB:BOOL=OFF
LLVM_PARALLEL_COMPILE_JOBS:STRING=4
LLVM_PARALLEL_LINK_JOBS:STRING=1
LLVM_TARGETS_TO_BUILD:STRING=X86;ARM;AArch64;BPF
LLVM_USE_LINKER:UNINITIALIZED=lld
```

本轮续跑重新执行同一 CMake 命令，并对重新写入的 Cache 再次校验，结果见第 7 节。

## 6. `_smp_mflags` 的影响面与续跑等价性

### 本轮批准的变更

命令行增加 `--define "_smp_mflags -j4"`；MemoryMax 继续为 18 GiB，
保留 debuginfo 和全部优化参数；应用原 L/proposed-real-tu-flags.diff 的六项精确白名单。
没有向 spec 增加宏，没有改变工作区源码。续跑使用独立复制的构建根，保留旧现场。

工作区 S:170 开始 `%build`，S:363 明确执行 `ninja -j %{mlgo_build_jobs}`，
该值由 S:48 设为 4。S 全文没有 `_smp_mflags` 或 `%make_build` 引用。
实际导出的 spec 对应 R0/home/abuild/rpmbuild/SOURCES/llvm.spec:187、380，
其中额外的行来自 GBS 导出的补丁声明和 `%prep` 应用语句。
因此本轮 `-j4` **不改变 Ninja 并发，在该 spec 中只影响打包阶段的 debuginfo 提取**。
根内 usr/lib/rpm/macros:182–198 的 `__debug_install_post` 把 `_smp_mflags` 传给
find-debuginfo.sh；macros:1099 的 `%make_build` 虽然也引用该宏，但此 spec 没有调用它。
全文检索原始输出在 J/investigation-evidence.log、J/preflight-investigation.log。

### 安装版本对应的机制

使用根内 ELF loader 查询到 `RPM version 4.14.1`，`--help` 实际列出 `--noprep`。
完整原始输出在 J/rpm-help.log。进一步从固定 Base 快照的 source/ 目录下载
rpm-4.14.1.1-1.4.src.rpm，包头 VCS 为
`platform/upstream/rpm#355231365d01b3fb7979a82a429f6b95c5e95993`，与已归档 primary.xml
中的 x86_64 rpm/rpm-build VCS 一致。下载 URL 在 J/rpm-source/source-url.txt，
源码在 E = J/rpm-source/rpm-4.14.1.1。检查该 SRPM 的补丁清单，相关控制逻辑未被其补丁修改。

| 方式 | 实际行为 | debuginfo hook / 等价性 | 依据 |
| --- | --- | --- | --- |
| `gbs build --noinit` | 只跳过根初始化；不等于跳过 `%prep`。正常构建仍执行 `%setup -q`，删除旧源码子目录后重新解包 | 不能据此保留 Ninja 产物 | `/usr/lib/python3/dist-packages/gitbuildsys/cmd_build.py:626–629`；`/usr/lib/build/build:817–819`；`build-recipe-spec:30–34,113–156`；导出 spec:162–173；E/build/parsePrep.c:360–382 |
| `gbs build --incremental` | 使用 `--no-topdir-cleanup`、`--no-init` 和 `--short-circuit --stage=-bs`；还会 bind mount 工作区源码 | 不是本次选择的正常打包续跑路径 | `/usr/bin/depanneur:2146–2177`；`/usr/lib/build/build-recipe-spec:158–172` |
| `rpmbuild --short-circuit -bi` | 从 `%install` 开始，包含 `%check`、文件处理；不生成二进制 RPM | 会执行 `__spec_install_post`，从而执行 `__debug_install_post` | E/rpmbuild.c:644–648；E/build/build.c:85–88,247–268；R0/usr/lib/rpm/macros:898–901 |
| `rpmbuild --short-circuit -bb` | 直接处理打包，跳过 `%install` | 不执行 debuginfo hook，并给 RPM 增加 `rpmlib(ShortCircuited)` 依赖，不能作为等价正式产物 | E/rpmbuild.c:639–643；E/build/build.c:235,275–276；E/build/pack.c:642–643 |
| **`rpmbuild -ba --noprep`** | 仅移除 PREP 阶段位；正常执行 `%build`、`%install`、hook、检查、源码及二进制打包 | `didBuild` 非零，不加 ShortCircuited 标记；可在已验证的准备树上续跑 | E/rpmbuild.c:229–232,636–663；E/build/build.c:235–281 |

关键代码原文：

```c
/* E/rpmbuild.c:231 */
{ "noprep", '\0', POPT_BIT_SET, &nobuildAmount, RPMBUILD_PREP,
/* E/rpmbuild.c:663 */
ba->buildAmount &= ~(nobuildAmount);
/* E/build/build.c:235,275–276 */
int didBuild = (what & (RPMBUILD_PREP|RPMBUILD_BUILD|RPMBUILD_INSTALL));
if (((what & RPMBUILD_PACKAGEBINARY) && !test) &&
    (rc = packageBinaries(spec, cookie, (didBuild == 0))))
/* E/build/pack.c:642–643 */
if (cheating) {
    (void) rpmlibNeedsFeature(pkg, "ShortCircuited", "4.9.0-1");
}
```

### 现有目录及准备树验证

原始 `du -sh` 输出（J/preflight-investigation.log）：

```text
156G  /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-baseline/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD
52G   /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-baseline/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILDROOT
```

旧 BUILDROOT 中 clang-22 仍是 1,793,477,048 字节，llvm-ar 已成为 14,825,632 字节；
build/bin/llvm-ar 则为 121,868,264 字节。这说明目录包含安装文件，但处于部分剥离状态，
不能作为完整、未处理的打包输入。S:373–376 还会追加 clang.cfg，因此不在旧 BUILDROOT
上反复运行安装脚本。新根不复制这个目录，从空目录重新执行完整 `%install`。

源码准备等价性按实际导出配方核对：

1. 对 llvm-22.1.8.tar.gz 的 169,010 个常规文件逐一比较内容摘要，覆盖 2,023,722,890 字节。
   首次比较发现 12 个差异，全部属于导出 spec:164–173 声明的五个补丁。
2. 在 J/replayed-patched-files/ 中重放这五个补丁，再与旧准备树比较；12 个文件全部 SHA256
   相同。没有在工作区 LLVM 树或旧构建树上应用任何补丁。
3. 对 x86 MLGO 资产归档的 10,866 个文件比较，覆盖 222,634,336 字节，全部相同。
4. 复制使用 GNU tar 的 PAX 格式，保留纳秒 mtime、数字 UID/GID、权限、符号链接和根内
   硬链接关系；常规文件在新旧根之间独立，不通过跨根硬链接复用。
5. 续跑门禁再次比较 spec、宏、CMakeCache、build.ninja、Ninja 日志/依赖库以及
   clang-22、lld、llvm-ar 的 SHA256、纳秒 mtime 和独立 inode。

证据：J/prepared-source-equivalence.json、J/prep-patch-equivalence.json、
J/prep-patch-replay.log、J/clone.log、J/clone-result.json，以及续跑目录中的
clone-key-identities.json。复制的准备树保持相同 chroot 内绝对路径；编译器、依赖包、
宏文件及构建参数随根一起保留。

**选择：使用正常 `-ba --noprep` 续跑。** 等价性指相同准备源码、配置、构建图和安装/打包
流程下的产物，不把输入和流程等价性扩大为已经完成两次 RPM 容器逐字节对照。
本次 22 个包查询的 BUILDTIME 均为 0（J/rpm-inventory.json），没有假定它随本轮时间变化；
本轮未另外执行一次从零完整构建来做容器字节比较。
Ninja 增量状态与实际续跑输出在下一节记录；不通过修改 spec 跳过构建/检查或删除
ShortCircuited 依赖来伪造等价性。

### GBS chroot 的退出状态与执行环境

本机 `/usr/lib/python3/dist-packages/gitbuildsys/cmd_chroot.py` 调用
`subprocess.call(cmd)` 后未把子进程状态返回给外层；因此 gbs 命令退出 0 不足以证明
rpmbuild 成功。续跑脚本保存独立的 `llvm-resume-rpm.exit`，缺失、无效或非零均判失败。
使用 root chroot 内的 `su -s /bin/bash -c ... - abuild` 登录 shell，与 GBS 后端
`/usr/lib/build/build-recipe-spec:180`、`/usr/lib/build/build:1365–1366` 一致。
只对 R1 使用 `gbs chroot`；该命令会复制 resolv.conf，因此不对旧现场 R0 调用它。

为了在 scope 消失前取得最终累计内存峰值，RPM 结束后 shell 写出退出码并暂候，采样线程
读取 cgroup memory.peak、memory.events、CPUUsageNSec 后写 release 文件，shell 才退出。
这是采集统计的握手，不改变 RPM 构建步骤。无害进程测试覆盖子命令失败但包装器返回 0、
缺失状态文件、Cache 被改坏、内存门禁、超时和中断等路径；线程均回收。
证据：J/build-guard-tests-final.log（5 个测试、10 个进程场景，PASS）、tools/test_build_llvm_x86_64.py、J/run/chroot-input.sh。

旧根 R0/.build.command:2 保存了实际 GBS 后端 rpmbuild argv。新命令去除本轮批准的
`--define _smp_mflags -j4` 和 `--noprep` 后，与旧 argv 完全一致；证据为
J/original-build-command.sh、J/rpmbuild-command-equivalence.json。

## 7. 正常 RPM 续跑的实测结果

本轮入口（新根、新日志，不覆盖 R0/L）：

```sh
python3 tools/resume_llvm_x86_64.py \
  --root temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0 \
  --evidence temp/baseline-resume-20260917 \
  --log-dir temp/baseline-resume-20260917/run --run
```

执行前记录的实际外层命令（J/run/launch.json）：

```sh
/usr/bin/time -v -o /home/linhao/Toolchain/development/llvm-optimize/temp/baseline-resume-20260917/run/time-v.txt systemd-run --user --scope --unit=llvm-baseline-99f508b75f0346a4ad607267cc6079e9.scope -p MemoryMax=18G -p MemorySwapMax=0 nice -n 15 ionice -c3 gbs chroot --root /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0
```

传入 chroot 的完整 shell 在 J/run/chroot-input.sh，登录 abuild 后执行：

```sh
rpmbuild --define '_srcdefattr (-,root,root)' --nosignature --target=x86_64 \
  --define '_build_create_debug 1' --define '_smp_mflags -j4' \
  -ba --noprep /home/abuild/rpmbuild/SOURCES/llvm.spec
```

### 前置资源、增量状态与门禁

启动前 MemAvailable 为 26518339584 B（24.697128 GiB），
磁盘可用 753036054528 B（701.319 GiB）；nproc=20。
通过 16 GiB / 60 GiB 门槛。J/run/commands.log 保留 nproc、free -g、df -h 的原始输出。
本轮固定 MemoryMax=18G、MemorySwapMax=0，不因主机当前空闲内存较多而上调。
只有一个 rpmbuild 实例；Ninja/compile/link 并发仍为 4/4/1，debuginfo 为 4。
大目标已经完成，此续跑计划不再假定需要一条 8 GiB 链接；新的完整构建预算见内存画像一节。

独立复制耗时 3050.495 秒（J/clone-result.json），这是准备副本的时间，不计入以下 rpmbuild 耗时。
复制排除旧 BUILDROOT；新旧关键配置和三个独立工具 ELF 的 SHA256、纳秒 mtime 相同，inode 不同。
首次复制尝试因 chroot 路径写成不存在的 /usr/bin/chroot 而失败；现场保存在 J/clone-attempt1/，
成功的 v2 复制使用实际 /usr/sbin/chroot，读写双方退出码均为 0。

预检 `ninja -n -d explain` 返回 NINJA_QUERY_EXIT=0，列出 89 项 LLDB 头文件暂存任务。
正常重跑 CMake 后实际执行 104 个短任务，含少量运行库、llvm-config 和头文件暂存；未重做 clang/lld 等大型链接。
新的 192 条 Ninja 日志记录对应 103 个实际文件，逐一与原构建树比较 SHA256，全部相同。
证据：J/ninja-preflight.log、J/resume-stage-lines.log、J/incremental-output-equivalence.json。

原轮和续跑的完整 CMake argv 完全相同（L/build.log:562 与 J/run/build.log:58，
J/cmake-command-equivalence.json）。Cache 的差别只是部分 -D 变量重新写入后的类型、注释和
编译器绝对路径/同一可执行文件名称的表示，完整 diff 在 J/resume-cache.diff。
已有 Cache 初检通过，CMake 重写后又在 6.052 秒通过全部门禁；errors=[]。

本轮 Cache 原始关键行（J/run/CMakeCache.txt）：

```text
CLANG_LINK_CLANG_DYLIB:BOOL=OFF
CMAKE_BUILD_TYPE:STRING=Release
CMAKE_CXX_FLAGS:STRING=  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument   -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables  -g -O3 -flto=thin -fomit-frame-pointer
LLVM_ENABLE_ASSERTIONS:BOOL=No
LLVM_ENABLE_LTO:STRING=Thin
LLVM_LINK_LLVM_DYLIB:BOOL=OFF
LLVM_PARALLEL_COMPILE_JOBS:STRING=4
LLVM_PARALLEL_LINK_JOBS:STRING=1
LLVM_TARGETS_TO_BUILD:STRING=X86;ARM;AArch64;BPF
LLVM_USE_LINKER:UNINITIALIZED=lld
```

### 结束状态与原始计时

**rpmbuild 实际退出码 0，外层退出码 0，problems=[]。**
采样线程和日志线程均已回收；J/resume-cleanup-verification.json 中原记录的进程残留列表为空。
J/resume-descendant-cgroups.json 证明 gbs、sudo、su、abuild shell 和 rpmbuild 在同一受限 scope；
外层 /usr/bin/time 只负责计时，位于 scope 外。nice 15、ionice idle 的实测在
J/resume-priority-check.log、J/debug-j4-priority.log。

`/usr/bin/time -v` 原始输出（J/run/time-v.txt）：

```text
	Command being timed: "systemd-run --user --scope --unit=llvm-baseline-99f508b75f0346a4ad607267cc6079e9.scope -p MemoryMax=18G -p MemorySwapMax=0 nice -n 15 ionice -c3 gbs chroot --root /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0"
	User time (seconds): 15130.98
	System time (seconds): 265.15
	Percent of CPU this job got: 469%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 54:38.90
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 3471968
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 1019
	Minor (reclaiming a frame) page faults: 50930909
	Voluntary context switches: 12105123
	Involuntary context switches: 3279990
	Swaps: 0
	File system inputs: 514116928
	File system outputs: 343707624
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
```

RPM 完成后、scope 仍存活时保存的 systemctl 原始输出（J/run/scope-after-rpm.log）：

```text
Result=success
MemoryPeak=19327094784
CPUUsageNSec=15396888995000
MemoryMax=19327352832
MemorySwapMax=0
ActiveState=active
```

这里 ActiveState=active 是统计握手时的状态；保存计数后 shell 才退出。最终 scope 已退出，
进程和线程回收另有上述检查，不把这个中间状态当作残留进程。
内核 memory.events：

```text
low 0
high 0
max 1
oom 0
oom_kill 0
oom_group_kill 0
```

完整阶段时间、RSS 和 cgroup 指标在第 11 节。

### RPM 清单与解包

正常产出 22 个二进制 RPM，合计 10,172,960,780 字节，另有 llvm-22.1.8-1.src.rpm。
完整名称、版本、大小、SHA256、Requires 在 J/rpm-inventory.json；所有二进制包的
`rpm -qp --requires` 均没有 `rpmlib(ShortCircuited)`。执行原文和状态在 J/rpm-inventory-extraction.log。

| 二进制 RPM（均为 22.1.8-1.x86_64） | 字节数 |
| --- | ---: |
| clang | 310023082 |
| clang-debuginfo | 2928319534 |
| clang-devel | 4098834 |
| clang-devel-debuginfo | 5729298 |
| compiler-rt | 3722242 |
| compiler-rt-debuginfo | 1288278 |
| libllvm | 23650574 |
| libllvm-debuginfo | 198056846 |
| libomp | 373374 |
| libomp-debuginfo | 1142190 |
| libomp-devel | 250126 |
| lldb | 30763794 |
| lldb-debuginfo | 332845250 |
| lldb-devel | 30520458 |
| lldb-devel-debuginfo | 279580570 |
| llvm | 410629530 |
| llvm-debuginfo | 3842661714 |
| llvm-debugsource | 43651146 |
| llvm-devel | 41191450 |
| llvm-devel-debuginfo | 308603238 |
| llvm-static-devel | 1375822930 |
| python-clang | 36322 |

只用 rpm2cpio | cpio 把 llvm、clang、compiler-rt 解包至 W/temp/toolchain-baseline/，不安装到宿主。
三个 RPM 共有 316 个重叠路径；包内大小、摘要、权限和链接目标均一致
（J/rpm-overlapping-files.json、J/rpm-file-dumps.log），因此 cpio 的“已有同龄文件”提示没有造成内容混用。

### 五工具验证及旧 accel 对照

实际验证命令：

```sh
 tools/verify_toolchain.sh --root temp/toolchain-baseline \
  --loader /lib64/ld-linux-x86-64.so.2 \
  --library-path /home/linhao/Toolchain/development/llvm-optimize/temp/toolchain-runtime-baseline/libxml2/usr/lib64 \
  --output temp/baseline-resume-20260917/rpm-toolchain-verification.json
```

五工具均为原生 x86_64 ELF，版本 22.1.8；NEEDED 中没有 libLLVM/libclang-cpp。
此处比较两边实际剥离后的工具文件大小，不使用原 1.79 GB 构建树 clang 与旧 accel 薄壳混比。
旧 accel 数据来自 L/accel-reference.json/log，对应 docs/10 的 ARM 根 emul/ 工具。

| 工具 | 本次 RPM 字节数 | 旧 accel 字节数 | 本次 LLVM 共享库依赖 | 旧 accel LLVM 共享库依赖 | 两边版本 |
| --- | ---: | ---: | --- | --- | --- |
| clang | 139929464 | 131592 | 无 | libclang-cpp.so.22.1, libLLVM.so.22.1 | 22.1.8 / 22.1.8 |
| clang++ | 139929464 | 131592 | 无 | libclang-cpp.so.22.1, libLLVM.so.22.1 | 22.1.8 / 22.1.8 |
| ld.lld | 83539336 | 6449904 | 无 | libLLVM.so.22.1 | 22.1.8 / 22.1.8 |
| llvm-ar | 14825632 | 81232 | 无 | libLLVM.so.22.1 | 22.1.8 / 22.1.8 |
| llvm-ranlib | 14825632 | 81232 | 无 | libLLVM.so.22.1 | 22.1.8 / 22.1.8 |

完整 NEEDED 原始验证表：

```text
| Tool | Bytes (resolved ELF) | NEEDED | Status |
| --- | ---: | --- | --- |
| clang | 139929464 | librt.so.1, libdl.so.2, libm.so.6, libz.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so.6, ld-linux-x86-64.so.2 | PASS |
| clang++ | 139929464 | librt.so.1, libdl.so.2, libm.so.6, libz.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so.6, ld-linux-x86-64.so.2 | PASS |
| ld.lld | 83539336 | libxml2.so.16, librt.so.1, libdl.so.2, libm.so.6, libz.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so.6, ld-linux-x86-64.so.2 | PASS |
| llvm-ar | 14825632 | librt.so.1, libdl.so.2, libm.so.6, libz.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so.6, ld-linux-x86-64.so.2 | PASS |
| llvm-ranlib | 14825632 | librt.so.1, libdl.so.2, libm.so.6, libz.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so.6, ld-linux-x86-64.so.2 | PASS |
Raw output: temp/baseline-resume-20260917/rpm-toolchain-verification.log
```

| 最终 ELF（别名共享文件） | SHA256 |
| --- | --- |
| clang / clang++ | `3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c` |
| ld.lld | `7ebba1bbc8a46e086c4470373315dd31730dab8fe554987894e6689e45e071fc` |
| llvm-ar / llvm-ranlib | `cad420e2daeb125b051a5d3f81b038b037c15fd30921ce880d4cc087d624313f` |

另外比较原构建树、续跑构建树及解包 RPM：clang-22、lld、llvm-ar 的构建树 ELF SHA256
保持不变；RPM 与构建树的 .text、.rodata、.data.rel.ro、.eh_frame、.gcc_except_table
节内容摘要相同。打包剥离没有改变这些已检查的代码/只读数据/异常处理节。
证据：J/elf-code-equivalence.json/log；不把这个检查扩大为所有 ELF 节逐字节相同。

## 8. 独立运行库与基准台加载方式

libxml2 来自固定 Base 快照缓存：

```text
/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-baseline/local/cache/6472de3503e3aaf43e4695c51bdf18ee/libxml2-2.15.1-1.7.x86_64.rpm
SHA256 a168b0e23b3a51132e63a6d518270b1f6375627317af7cf6341c29afdacb2dcf
```

摘要与固定快照 primary.xml 的 libxml2/x86_64 条目完全一致。
只执行 `rpm2cpio | cpio` 解包到
`W/temp/toolchain-runtime-baseline/libxml2/`，不执行 RPM 安装脚本，不修改宿主或工具二进制。
证据为 J/runtime-manifest.json、J/runtime-extraction.log。

运行时使用宿主原生 loader 的 `--library-path`：

```sh
/lib64/ld-linux-x86-64.so.2 \
  --library-path /home/linhao/Toolchain/development/llvm-optimize/temp/toolchain-runtime-baseline/libxml2/usr/lib64 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/toolchain-baseline/usr/bin/ld.lld --version
```

最终 RPM 的 ld.lld 通过同一独立运行库加载成功：`LLD 22.1.8 (compatible with GNU linkers)`，
退出 0（J/rpm-toolchain-verification.log）。较早的构建树查询保存在 J/runtime-loader-query.log。

基准台原先主动清除 LD_LIBRARY_PATH，现加入显式 `--library-path NAME=DIR`，并要求匹配
`--loader NAME=ELF_LOADER`。该参数只组成加载器 argv；JSON 记录目录、库文件 SHA256、
loader SHA256，运行库变化会使两轮校准的身份比较失败。编译 flags、统计和资源门禁不变。
这实现了本任务要求的独立运行库加载；没有把库放入宿主目录或改写 ELF。
六项真实 TU 白名单仍是单独的两行精确匹配补丁，不接受任意额外 flags。

对应基准参数为：

```sh
--toolchain baseline=/home/linhao/Toolchain/development/llvm-optimize/temp/toolchain-baseline/usr \
--loader baseline=/lib64/ld-linux-x86-64.so.2 \
--library-path baseline=/home/linhao/Toolchain/development/llvm-optimize/temp/toolchain-runtime-baseline/libxml2/usr/lib64
```

## 9. 十个真实 ARM 翻译单元

使用最终 RPM 的 clang++ 22.1.8、它自己的 clang/22 资源目录和 ARMROOT，
从 R1 的 build.ninja 按 selection.json 重新查询完整命令，并以
`--target=armv7l-tizen-linux-gnueabi --sysroot=ARMROOT -E` 生成输入。
全局预定义宏检查包含 `#define __arm__ 1`，没有 `#define __x86_64__`。
10 个预处理命令全部退出 0；未修改源码或 x86_64 构建生成的 LLVM 配置头，也没有重标 x86_64 输入。
证据：J/real-tu/collection.json、commands.log、arm-predefined-macros.txt 和每个 TU 的 time 文件。

原 x86_64 命令完整保存在 sidecar 的 original_command；preprocess_command 则记录实际 ARM 命令。
必要转换只作用于命令：把源/include 路径映射到 R1，移除 x86 的 -m64/-march=nehalem/
-msse4.2/-mfpmath=sse、LTO 与原依赖/输出选项，再指定 ARM triple、sysroot、资源目录和 -E。
移除 LTO 是因为基准台编译输出必须是 ARM ELF .o。其余编译语义 flags 保持原顺序。
批准的六项白名单为 -fPIC、-fno-semantic-interposition、-fvisibility-inlines-hidden、
-fno-common、-gdwarf-4、-frecord-gcc-switches；原批准 diff 在 L/proposed-real-tu-flags.diff。

下表源码相对于 R1/home/abuild/rpmbuild/BUILD/llvm-22.1.8/；每个名称对应同名 .ii 和 .flags.json。

| 输入名 | 实际源码 | .ii 字节数 | 位置 |
| --- | --- | ---: | --- |
| llvm_sema_SemaStmt | clang/lib/Sema/SemaStmt.cpp | 9090106 | tools/bench_inputs/real_tu/ |
| llvm_sema_SemaExprCXX | clang/lib/Sema/SemaExprCXX.cpp | 10179680 | J/real-tu/（sidecar 引用绝对路径） |
| llvm_codegen_SelectionDAG | llvm/lib/CodeGen/SelectionDAG/SelectionDAG.cpp | 6641252 | tools/bench_inputs/real_tu/ |
| llvm_codegen_MachinePipeliner | llvm/lib/CodeGen/MachinePipeliner.cpp | 6557196 | tools/bench_inputs/real_tu/ |
| llvm_transforms_Attributor | llvm/lib/Transforms/IPO/Attributor.cpp | 5485078 | tools/bench_inputs/real_tu/ |
| llvm_transforms_WholeProgramDevirt | llvm/lib/Transforms/IPO/WholeProgramDevirt.cpp | 5658860 | tools/bench_inputs/real_tu/ |
| llvm_arm_ARMISelLowering | llvm/lib/Target/ARM/ARMISelLowering.cpp | 8219975 | tools/bench_inputs/real_tu/ |
| llvm_arm_ARMTargetTransformInfo | llvm/lib/Target/ARM/ARMTargetTransformInfo.cpp | 7607820 | tools/bench_inputs/real_tu/ |
| llvm_mc_MasmParser | llvm/lib/MC/MCParser/MasmParser.cpp | 3888311 | tools/bench_inputs/real_tu/ |
| llvm_mc_AsmParser | llvm/lib/MC/MCParser/AsmParser.cpp | 4012457 | tools/bench_inputs/real_tu/ |

超过 10 MB 的唯一基线输入，完整工作区路径为：

```text
/home/linhao/Toolchain/development/llvm-optimize/temp/baseline-resume-20260917/real-tu/llvm_sema_SemaExprCXX.ii
```

其余 9 个 .ii 与全部 10 个 sidecar 提交；SHA256、triple、flags 和两条完整命令均在 sidecar 中。
单次预处理用 taskset CPU 2、prlimit 4 GiB、nice 15、ionice idle；开始每个输入前检查至少 4 GiB 可用内存。
原日志中的 x86_64 编译时长仅用于选择中等负载，不当作 ARM 测量值。

重采集入口（新的输出目录，避免覆盖）：

```sh
python3 tools/collect_llvm_real_tu.py \
  --toolchain temp/toolchain-baseline/usr --loader /lib64/ld-linux-x86-64.so.2 \
  --build-root temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0 \
  --sysroot /home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0 \
  --candidates tools/bench_inputs/real_tu/selection.json \
  --output-dir temp/real-tu-regenerated --publish-dir temp/real-tu-regenerated-inputs --cpu 2
```

### clang 18 参考输入的兼容性边界

直接让 clang 18 编译 clang 22 预处理的 SemaStmt 探测输入失败，涉及 type_traits 的
__is_convertible 内建和 sized operator delete（J/arm-feasibility-probe/reference-probe.log）。
这不是 ARM 预处理失败：clang 22 的同一探测输入已编译为 ARM ELF；clang 18 使用它自己的
资源目录重新进行 ARM 预处理后也编译成功（reference-own.log）。探测均不计入正式计时。

因此独立参考轮另存 10 个由 clang 18/clang/18 资源目录生成的 ARM 输入：
J/reference-real-tu/、J/reference-inputs/。它们没有覆盖基线输入，也没有进入 Git。
完整命令、triple、摘要和大小在 J/reference-real-tu/collection.json；10 个 -E 均成功。
参考轮须同时标注输入和资源目录不同，不能用其时间比值声称受控优化收益。

## 10. 重新校准、正式基线与独立参考

本节完整数据目录 D 为 `W/temp/bench_results/baseline-20260917-rpm`。JSON 保存全部样本、
wall/user/sys/RSS 的中位数、最小值、标准差、每次前后 loadavg、命令行和输入身份；
同名 markdown 供直接阅读，`-raw/commands.json` 与 stdout/stderr 保存原始命令输出。

### 固定测量协议与资源上限

本轮每套完整基准包含 15 项：A/B/C、10 个真实 ARM TU、ld.lld、llvm-ar。
复用历史合成生成器，seed=73419，规模 A/B/C=1/2/2；A 为标准库头文件和模板负载，
B 为多函数优化负载，C 为超大单函数优化负载。这里沿用 docs/12 的已校准规模，
B/C 不与历史 scale=1 的耗时直接混比。合成输入 -O2，真实 TU 使用各自 sidecar 的语义 flags，
不把两种编译 flags 混写成同一配置。

链接与归档使用同一批 66 个 ARM object：B 的 64 个互不重复分片加 A/C 两个 object。
真实 TU 当前只进入编译测量，不进入链接夹具。ld.lld 使用 `-shared --threads=1`，
每样本重复 4096 次；llvm-ar 使用 `rcsD`，每样本重复 1024 次；每次删除旧输出，
表中 wall/user/sys 已除以重复次数，是单次调用成本，RSS 不除。多工具链同次运行时
由首个工具链产生统一夹具；本轮两次校准与正式轮的夹具 SHA 身份完全一致。

默认 N=5，丢弃第 1 次，保留 4 次；用中位数，记录 min 和样本标准差。
显式固定 CPU 2，顺序运行；默认亲和性最多 nproc 的一半，本轮仅用 20 核中的 1 核。
每个子进程 `prlimit --as=4294967296:4294967296`，每次执行前 MemAvailable 不足 4 GiB 拒绝。
loadavg 使用 1 分钟值，阈值 10（nproc/2），每次前后均记录；ASLR 仅对子进程用 setarch -R 关闭。
临时产物位于 /dev/shm；四轮 JSON 的 scratch_removed 均为 true。机器频率策略保留原值：
CPU 2 governor=powersave、EPP=balance_performance、最大频率配置 5300000 kHz；没有修改系统调频设置。
证据：各轮 protocol/host、tools/bench_toolchain.py 的 Runner、single_run、calibration 实现。

### 两轮校准

**PASS：噪声底 0.755300%（最大对应 wall 中位数绝对差，门槛 3%）。**
全部 15 项各轮 CV ≤3%，没有保留的可疑样本；这是本次最终 RPM clang 22 与 10 个真实 TU 的重新校准，
不是沿用 docs/12 的 clang 18 数字。本轮第一次完整双轮校准即通过，没有失败轮被删去或挑样本。
沿用单核亲和、子进程关闭 ASLR、短命令批量重复、串行执行和 tmpfs；等待 RPM 工作及采样器退出后才开始，
整理报告的辅助命令绑定 CPU 0、nice 15，以减少对 CPU 2 的干扰。

| 项目 | 第 1 轮 wall s/op | 第 2 轮 wall s/op | 有符号变化 % | CV1 % | CV2 % | 门禁 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| A | 8.356045 | 8.298230 | -0.692 | 1.269 | 0.980 | PASS |
| B | 2.211774 | 2.209585 | -0.099 | 0.298 | 0.382 | PASS |
| C | 5.904442 | 5.893011 | -0.194 | 0.806 | 0.723 | PASS |
| real_llvm_arm_ARMISelLowering | 8.254461 | 8.250411 | -0.049 | 0.178 | 0.352 | PASS |
| real_llvm_arm_ARMTargetTransformInfo | 4.719774 | 4.750568 | 0.652 | 0.424 | 0.639 | PASS |
| real_llvm_codegen_MachinePipeliner | 6.116116 | 6.100009 | -0.263 | 0.431 | 0.656 | PASS |
| real_llvm_codegen_SelectionDAG | 6.763028 | 6.769247 | 0.092 | 0.292 | 0.153 | PASS |
| real_llvm_mc_AsmParser | 2.651330 | 2.644926 | -0.242 | 0.253 | 2.116 | PASS |
| real_llvm_mc_MasmParser | 3.289380 | 3.285498 | -0.118 | 0.246 | 0.526 | PASS |
| real_llvm_sema_SemaExprCXX | 6.014638 | 6.004189 | -0.174 | 0.610 | 0.362 | PASS |
| real_llvm_sema_SemaStmt | 5.763711 | 5.743033 | -0.359 | 0.495 | 0.815 | PASS |
| real_llvm_transforms_Attributor | 6.205517 | 6.188302 | -0.277 | 0.912 | 0.708 | PASS |
| real_llvm_transforms_WholeProgramDevirt | 5.712101 | 5.675919 | -0.633 | 0.253 | 0.576 | PASS |
| ld.lld | 0.004930 | 0.004937 | 0.139 | 0.376 | 0.551 | PASS |
| llvm-ar | 0.002361 | 0.002379 | 0.755 | 0.941 | 0.934 | PASS |

校准原始结果：D/calibration-01.json、calibration-01-run1.json、calibration-01-run2.json。

### 正式基线

通过校准后单独执行正式轮，协议、工具身份、资源目录、输入与夹具均与校准相同。
协议 hash：`4f8b71e0547b3c7e72deac4141ce5dec4fee1f43af6a9b8f19b4fc91bd4637e5`。
夹具 hash：`30acab6c36503bcf53f5ad6467d17a58ede7f0205f95f68dedd1125494a9096a`。
下表为正式轮本身的数据，不以校准样本替代。证据：D/formal-baseline.json。

| 项目 | wall 中位数 s/op | wall min | wall SD | CV % | user 中位数 | sys 中位数 | 峰值 RSS KiB | 可疑保留样本 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 8.399582 | 8.385821 | 0.041501 | 0.493 | 8.104869 | 0.294882 | 1040536 | 0 |
| B | 2.214020 | 2.211724 | 0.004182 | 0.189 | 2.184033 | 0.030489 | 149256 | 0 |
| C | 5.921623 | 5.880202 | 0.026910 | 0.455 | 5.409723 | 0.501274 | 1188752 | 0 |
| real_llvm_arm_ARMISelLowering | 8.238827 | 8.214626 | 0.026722 | 0.324 | 8.052297 | 0.183420 | 619892 | 0 |
| real_llvm_arm_ARMTargetTransformInfo | 4.726586 | 4.687264 | 0.031775 | 0.672 | 4.571212 | 0.163465 | 557532 | 0 |
| real_llvm_codegen_MachinePipeliner | 6.132139 | 6.094045 | 0.031066 | 0.507 | 5.976332 | 0.146442 | 486944 | 0 |
| real_llvm_codegen_SelectionDAG | 6.744573 | 6.731247 | 0.029734 | 0.440 | 6.602890 | 0.138462 | 497508 | 0 |
| real_llvm_mc_AsmParser | 2.661888 | 2.651924 | 0.008933 | 0.336 | 2.594209 | 0.065467 | 282156 | 0 |
| real_llvm_mc_MasmParser | 3.298552 | 3.295256 | 0.004698 | 0.142 | 3.233309 | 0.063475 | 285324 | 0 |
| real_llvm_sema_SemaExprCXX | 6.013191 | 5.982449 | 0.022526 | 0.375 | 5.831124 | 0.177962 | 691764 | 0 |
| real_llvm_sema_SemaStmt | 5.754308 | 5.724455 | 0.031841 | 0.553 | 5.575280 | 0.172947 | 653732 | 0 |
| real_llvm_transforms_Attributor | 6.269321 | 6.224306 | 0.050201 | 0.800 | 6.137711 | 0.129944 | 490624 | 0 |
| real_llvm_transforms_WholeProgramDevirt | 5.718177 | 5.705845 | 0.013916 | 0.243 | 5.544271 | 0.165914 | 533144 | 0 |
| ld.lld | 0.004918 | 0.004895 | 0.000022 | 0.449 | 0.001468 | 0.002889 | 79840 | 0 |
| llvm-ar | 0.002360 | 0.002346 | 0.000030 | 1.273 | 0.000616 | 0.001377 | 82240 | 0 |

### bundled clang 18 独立参考

**资源目录不同，不是受控对照，仅供量级参考。** 使用 clang 18 自己的资源目录，且第 9 节已经说明，
10 个真实输入必须由 clang 18 自己重新预处理；此轮的真实 .ii、资源目录、夹具均不同。
不把这两张表的比值称为自研优化收益。真实 .ii 在 J/reference-inputs/，大文件在 J/reference-real-tu/。
证据：D/bundled-reference.json 与 J/reference-real-tu/collection.json。

| 项目 | wall 中位数 s/op | wall min | wall SD | CV % | user 中位数 | sys 中位数 | 峰值 RSS KiB | 可疑保留样本 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 10.262100 | 10.134419 | 0.071224 | 0.696 | 9.905265 | 0.359271 | 1165884 | 0 |
| B | 2.599377 | 2.593972 | 0.004300 | 0.165 | 2.565379 | 0.030491 | 148748 | 0 |
| C | 5.619491 | 5.617344 | 0.021465 | 0.381 | 5.560080 | 0.061967 | 198296 | 0 |
| real_llvm_arm_ARMISelLowering | 10.294010 | 10.262430 | 0.028347 | 0.275 | 10.101740 | 0.184919 | 641532 | 0 |
| real_llvm_arm_ARMTargetTransformInfo | 5.814684 | 5.757381 | 0.034414 | 0.593 | 5.640074 | 0.167416 | 582124 | 0 |
| real_llvm_codegen_MachinePipeliner | 7.540681 | 7.522648 | 0.022664 | 0.300 | 7.398712 | 0.139946 | 489800 | 0 |
| real_llvm_codegen_SelectionDAG | 8.382972 | 8.322271 | 0.040709 | 0.486 | 8.226158 | 0.162936 | 503724 | 0 |
| real_llvm_mc_AsmParser | 3.130598 | 3.120219 | 0.010767 | 0.344 | 3.066089 | 0.060981 | 282808 | 0 |
| real_llvm_mc_MasmParser | 3.993098 | 3.941654 | 0.042760 | 1.071 | 3.928530 | 0.063477 | 287204 | 0 |
| real_llvm_sema_SemaExprCXX | 7.318023 | 7.293451 | 0.074852 | 1.019 | 7.112507 | 0.208424 | 719456 | 0 |
| real_llvm_sema_SemaStmt | 7.057485 | 7.005299 | 0.083948 | 1.186 | 6.869309 | 0.194467 | 681348 | 0 |
| real_llvm_transforms_Attributor | 7.771891 | 7.742923 | 0.035793 | 0.460 | 7.637894 | 0.128956 | 500472 | 0 |
| real_llvm_transforms_WholeProgramDevirt | 7.116072 | 7.099886 | 0.042274 | 0.593 | 6.949908 | 0.153943 | 529884 | 0 |
| ld.lld | 0.004028 | 0.004015 | 0.000012 | 0.294 | 0.001232 | 0.002275 | 79516 | 0 |
| llvm-ar | 0.002297 | 0.002277 | 0.000018 | 0.774 | 0.000664 | 0.001271 | 81756 | 0 |

### 运行开销与实际内存

| 运行 | 起始时间 | 完整运行 wall 秒 | 全部子命令最大 RSS KiB | 起始 MemAvailable GiB | scratch 已删除 |
| --- | --- | ---: | ---: | ---: | --- |
| calibration-01-run1 | 2026-09-17T13:55:20+0800 | 495.733 | 1188752 | 24.544 | True |
| calibration-01-run2 | 2026-09-17T14:03:36+0800 | 495.619 | 1188752 | 24.513 | True |
| formal-baseline | 2026-09-17T14:12:07+0800 | 496.257 | 1188752 | 24.300 | True |
| bundled-reference | 2026-09-17T14:20:45+0800 | 556.488 | 1165884 | 24.313 | True |

四轮观测到的单进程最高 RSS 为 1,188,752 KiB（1.133682 GiB），低于 4 GiB 上限。
这里给出的是 RSS 实测，硬限额本身作用于虚拟地址空间 RLIMIT_AS。完整运行耗时含夹具准备与测量，
不含开始前固定头文件哈希计算，也不含 TU 预处理；每轮是分钟级筛选，不能替代专用服务器最终验收。

### 本次实际命令与复用方式

在 W 目录执行。以下从 launch JSON 读取实际 argv；复跑时将 --output 改为新前缀，避免覆盖已有证据。

calibration：

```sh
python3 tools/bench_toolchain.py --toolchain baseline=/home/linhao/Toolchain/development/llvm-optimize/temp/toolchain-baseline/usr --loader baseline=/lib64/ld-linux-x86-64.so.2 --library-path baseline=/home/linhao/Toolchain/development/llvm-optimize/temp/toolchain-runtime-baseline/libxml2/usr/lib64 --sysroot /home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0 --resource-dir /home/linhao/Toolchain/development/llvm-optimize/temp/toolchain-baseline/usr/lib64/clang/22 --cpus 2 --output /home/linhao/Toolchain/development/llvm-optimize/temp/bench_results/baseline-20260917-rpm/calibration-01 --calibrate
```

formal：

```sh
python3 tools/bench_toolchain.py --toolchain baseline=/home/linhao/Toolchain/development/llvm-optimize/temp/toolchain-baseline/usr --loader baseline=/lib64/ld-linux-x86-64.so.2 --library-path baseline=/home/linhao/Toolchain/development/llvm-optimize/temp/toolchain-runtime-baseline/libxml2/usr/lib64 --sysroot /home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0 --resource-dir /home/linhao/Toolchain/development/llvm-optimize/temp/toolchain-baseline/usr/lib64/clang/22 --cpus 2 --output /home/linhao/Toolchain/development/llvm-optimize/temp/bench_results/baseline-20260917-rpm/formal-baseline
```

reference：

```sh
python3 tools/bench_toolchain.py --toolchain bundled=/home/linhao/Toolchain/plan_evaluation/chromium-efl/tizen_src/buildtools/llvm --loader bundled=/lib64/ld-linux-x86-64.so.2 --sysroot /home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0 --resource-dir /home/linhao/Toolchain/plan_evaluation/chromium-efl/tizen_src/buildtools/llvm/lib64/clang/18 --real-tu-dir /home/linhao/Toolchain/development/llvm-optimize/temp/baseline-resume-20260917/reference-inputs --cpus 2 --output /home/linhao/Toolchain/development/llvm-optimize/temp/bench_results/baseline-20260917-rpm/bundled-reference
```

后续比较多个 LLVM 变体时，重复 --toolchain/--loader（需要时 --library-path），
保持同一个 --resource-dir、--sysroot、CPU、输入集和首工具链夹具来源；协议或输入变化后必须重新校准。
库目录通过显式 ELF loader 参数传入，未使用宿主安装或修改 ELF 的方式解决 libxml2。

## 11. 内存画像与后续变体容量

这些指标必须区分：进程 `VmHWM` 是单进程 RSS 高水位；进程树 RSS 求和可能重复计算共享页；
cgroup `memory.peak` 包含文件页缓存等记账。按阶段采样的最大 RSS 是观察下界，不是连续测得的真实峰值。
旧采样不能事后恢复每个 compiler 的 VmHWM；这一项为 UNKNOWN。本轮增加每 2 秒逐进程 VmHWM 采样。

### 已完成编译/链接阶段与旧 debuginfo

| 阶段 | 观察到的进程树 RSS 高水位 GiB | 证据 |
| --- | ---: | --- |
| 编译边活跃、没有 LINKER 边活跃的样本 | 2.812 | L/samples.jsonl:99；2026-09-17T09:32:59+08:00 |
| 整个编译/链接时段（存在重叠） | 17.162 | L/samples.jsonl:125；2026-09-17T09:46:04+08:00 |
| 旧 debuginfo -j40，最终 OOM | 17.134 | L/samples.jsonl:306；2026-09-17T11:17:10+08:00 |

编译样本分类依据实际 build.ninja 的 LINKER 规则与 .ninja_log 的边起止区间；剔除链接边前后 2 秒。
共 83 个符合条件的采样；最高样本对应 .ninja_log:7128、7129、7130、7132 的编译边。
这是进程树观测值，不能当作单个编译任务峰值。首轮 cgroup 累计峰值达到 18 GiB；
这个累计值也不能重复充当每个阶段自己的峰值。算法和结果：J/summarize-memory.py、J/memory-profile-old.json。

### 单个链接目标 Top 10

按 L/linker-memory-observations.jsonl 的 VmHWM 排序，保留每个 PID 的最高观测值；共整理 50 个链接进程。
目标体积为原构建树未剥离 ELF，包含 debug 信息，不是第 7 节最终 RPM 工具的剥离后体积。

| 链接目标 | VmHWM GiB | 目标 ELF 字节数 | RSS / ELF 字节比 | 原始 JSONL 行 |
| --- | ---: | ---: | ---: | ---: |
| bin/clang-22 | 16.831 | 1793477048 | 10.077 | 3 |
| bin/clang-repl | 16.445 | 1849187144 | 9.549 | 24 |
| bin/clang-check | 14.877 | 1350644704 | 11.827 | 28 |
| bin/clang-tidy | 14.226 | 1333046608 | 11.459 | 34 |
| lib64/libclang-cpp.so.22.1 | 13.581 | 1715987144 | 8.498 | 4 |
| bin/clangd | 13.535 | 1184655080 | 12.268 | 44 |
| bin/clangd-fuzzer | 12.888 | 1155459800 | 11.977 | 42 |
| bin/clangd-indexer | 11.900 | 1079000720 | 11.842 | 46 |
| bin/lldb-instr | 10.626 | 1244982488 | 9.164 | 49 |
| lib64/liblldb.so.22.1.8 | 10.351 | 1689323520 | 6.579 | 2 |

libclang-cpp 那个进程只留下已消失的响应文件路径，因此目标名属于有证据的推断：
09:49:46.076 的采样仅被一个 Ninja 活跃边覆盖（留出前后 2 秒余量），该边是
R0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/.ninja_log:8271 的 lib64/libclang-cpp.so.22.1。
其他表中目标来自实际 argv 的 -o 或已展开响应文件；推断细节保存在该行的 target_resolution 字段。

**目标更大并不提供一个固定的内存换算系数。** 例如 liblldb 的 ELF 比 clang-check 大，
但其已观察到的链接 RSS 更低；50 个已记录进程的 RSS/ELF 比值范围为
4.112–27.564。这些是观测关系，不是未来内存的上界或线性预测。
采样可能漏掉完整的短链接和退出前增长，Top 10 是已观察样本的 Top 10。

### 本轮 debuginfo -j4 与全流程统计

| 本轮阶段 | 开始时间 | 结束时间 | 观察到的进程树 RSS 峰值 GiB | 同阶段观察到的 cgroup 当前值最大 GiB | 30 秒样本数 |
| --- | --- | --- | ---: | ---: | ---: |
| 增量构建 | 12:52:45 | 12:52:58 | UNKNOWN（仅启动样本 0.008） | UNKNOWN（启动时尚无 scope 值） | 1 |
| 重新安装 | 12:52:58 | 13:03:34 | 0.071 | 6.197 | 21 |
| debuginfo -j4 | 13:03:34 | 13:18:25 | 5.896 | 9.675 | 29 |
| check-buildroot / brp-compress | 13:18:25 | 13:24:42 | 0.562 | 6.800 | 13 |
| 静态归档 strip 等 brp | 13:24:42 | 13:27:01 | 0.066 | 9.866 | 4 |
| 包文件处理 / 检查 | 13:27:01 | 13:32:27 | 0.107 | 17.983 | 11 |
| RPM 写出 / 压缩 / clean | 13:32:27 | 13:47:24 | 2.618 | 17.070 | 30 |

本轮 debuginfo 处理 133 个 ELF，耗时 14:51。30 秒样本的进程树 RSS 最大 6330834944 B（5.896049 GiB），
该阶段 cgroup 累计峰值升至 11303559168 B（10.527260 GiB），高于此前阶段的峰值。
2 秒逐进程采样确认最多 4 个 debugedit/eu-strip 工作进程同时活跃；最初达到 4 个的记录在
J/run/process-memory.jsonl:339（2026-09-17T13:04:06+08:00）。
GNU strip 处理静态归档为其后单独的串行脚本，不受 _smp_mflags 控制；其身份是 GNU Binutils 2.43
（J/static-archive-strip-identity.log；R1/usr/lib/rpm/brp-strip-static-archive:16–20）。

本轮单进程 VmHWM 前五项：

| 进程 / 目标 | VmHWM GiB | 原始 2 秒采样行 |
| --- | ---: | ---: |
| eu-strip / llvm-22.1.8-1.x86_64/usr/bin/clang-repl | 3.311127 | 498 |
| eu-strip / llvm-22.1.8-1.x86_64/usr/bin/clang-22 | 3.209354 | 394 |
| eu-strip / llvm-22.1.8-1.x86_64/usr/lib64/libclang-cpp.so.22.1 | 3.083778 | 720 |
| eu-strip / llvm-22.1.8-1.x86_64/home/owner/share/tmp/sdk_tools/lldb/lib64/liblldb.so.22.1.8 | 3.034374 | 360 |
| eu-strip / llvm-22.1.8-1.x86_64/usr/lib64/liblldb.so.22.1.8 | 3.034012 | 735 |

全过程 cgroup 精确累计峰值为 19327094784 B（17.999760 GiB）；
接近 18 GiB cap 的峰值出现在后续包文件处理，不是新发生的链接或 debuginfo OOM。
同阶段 memory.stat 记录以 file 页缓存为主，进程 RSS 明显较小。memory.events 最终为 max=1、oom=0、oom_kill=0。
不能把 cgroup 峰值当成某个进程所需内存，也不能把一次 max 记录直接写成 OOM。
GNU time 的 Max RSS 为 3,471,968 KiB，它统计到的单进程最大值与 eu-strip 观测相符，不是所有进程 RSS 之和。
共保存 109 次 30 秒资源样本，MemAvailable 最低 18.163864 GiB，未接近 2 GiB 自动中止线。
进程树 RSS 还含外层 time 包装进程；这个包装器位于受限 gbs scope 外。
原始数据：J/run/samples.jsonl、process-memory.jsonl、scope-after-rpm.json、time-v.txt；
整理脚本与结果：J/summarize-resume-memory.py、J/memory-profile-resume.json。短暂增量编译没有独立的 30 秒样本，
其逐进程记录仍在 2 秒日志中；不虚构这一短阶段的连续总峰值。

### 30 GB 机器是否够做 PGO / BOLT

**容量规划结论：当前 30 GB 机器、18 GiB MemoryMax 和既定余量规则，不足以接纳后续 PGO 插桩完整构建；
也不能把 BOLT 变体列为已有容量保证的可执行任务。** 不再采用已经失效的 8 GiB 假设。

已观察到的单次 clang 链接为 16.831097 GiB。仅按原“链接小于 MemAvailable 的 60%”规则，
就需要 MemAvailable 严格大于 28.052 GiB；若还留 4 GiB 给系统，
可用物理内存需超过 32.052 GiB。本机 /proc/meminfo 的 MemTotal 只有约 30.8 GiB，
本轮启动时 MemAvailable 约 24.7 GiB。这已经不能满足普通基线链接的原预算规则，更没有经测量证明的插桩余量。
18 GiB cap 相对已观察到的 clang 单次链接只剩 1.169 GiB，尚未覆盖同时活跃的编译进程和其他开销。

PGO 插桩构建的实际链接高水位、单独运行 BOLT 的高水位仍为 UNKNOWN：本轮没有执行这两种工作负载。
“规划上不够”不等于声称每一次 PGO 或单独 BOLT 操作必定 OOM。BOLT 与 ThinLTO 是不同阶段，
不能把链接内存直接当作 BOLT 内存，也不能用上述 ELF 比值外推插桩后峰值。要确定单独 BOLT 能否完成，
需要在保留样本和明确内存上限下实际测量；要安排完整 PGO/BOLT 变体流水线，应先取得更大的可用内存预算，
再用对应插桩链接/重写工作的实测峰值定并发。本轮不擅自提高 cap、减少 debug 信息或修改优化参数。

完整构建脚本已把链接估计向上取整为 16.84 GiB，保留 18 GiB cap；它现在会拒绝按旧 8 GiB 假设启动新的完整构建。
仅一条链接加一个 2 GiB 编译预算及 2 GiB 开销就需 20.84 GiB，无法装入该 cap。测试覆盖这一拒绝路径。
本轮续跑使用独立入口，在证明大型目标已经完成后保留原 4/1 并发与 18 GiB cap；没有绕过完整重建的容量问题。
实现及验证：tools/build_llvm_x86_64.py:51 起的 resource_plan、tools/resume_llvm_x86_64.py、J/build-guard-tests-final.log。

容量判定分开记录：PGO 完整构建按当前预算为 **NO**；单独 BOLT 重写为 **UNKNOWN**，需要实际的受限运行测量。
包含重新链接的 BOLT 流水线同样先受当前完整构建预算门禁约束。没有用 ThinLTO 的数字伪造 BOLT 实测值。

## 12. 已发现的打包限制与 UNKNOWN

### GNU strip 对 ThinLTO 静态归档的处理

本轮正常打包日志出现 GNU strip 无法识别 LLVM IR bitcode 成员的消息。根内实际
strip 是 GNU Binutils 2.43，`R1/usr/lib/rpm/brp-strip-static-archive:16–20` 串行遍历静态归档；
该脚本没有 `set -e`，先前成员出错并未使整个 RPM 流程失败。
证据：J/static-archive-strip-identity.log、post-install-stages.log、J/run/build.log。

这不是可以忽略的纯日志噪声。对 `liblldCOFF.a` 从构建树、剥离后的 BUILDROOT、最终
`llvm-static-devel` RPM 三处进行核对，实际结果为：

| 项目 | 构建树 | 剥离后及最终 RPM |
| --- | ---: | ---: |
| 文件字节数 | 26,191,294 | 26,049,746 |
| GNU `/` 符号表 | 141,488 字节、1,807 个符号 | 已消失 |
| 18 个对象成员内容 | 基准 | SHA256 全部相等 |
| `//` 长文件名表 | 存在 | 内容相等 |

构建树归档 SHA256：`4f6e80fa34535c1d12f4fde882a00ca5509d5570db6223b5a86c45181d9dddae`。
最终 RPM 归档 SHA256：`9e8915f4a853a8a97285f34c2b51eb2bc16eb3fb3de943fdabf43f1b3e252617`，
与采集时 BUILDROOT 的结果完全相等。最终解包样本保留在
`W/temp/baseline-resume-20260917/static-archive-rpm/usr/lib64/liblldCOFF.a`；
本轮正常 `%clean` 已移除 R1 的 BUILDROOT。
证据：J/static-archive-strip-result.json、static-archive-strip-analysis.log、static-archive-rpm-extract.log。

**22 个二进制 RPM 已成功写出，不等于全部子包完成了功能验收。** 五个基准工具已单独通过版本、
ELF、共享库依赖及实际负载验证；`llvm-static-devel` 的消费者链接兼容性仍为 UNKNOWN。
没有测试每个归档，也不能仅凭索引缺失断言所有链接器一定失败。
完整重建会执行相同 BRP 步骤，因此此问题不推翻本轮正常打包流程与续跑输入的等价性。
本轮没有擅自修改 strip 宏、静态归档、spec 或优化参数。

### 其余边界

| 项目 | 当前结论 / 原因 | 确定所需条件 | 证据 |
| --- | --- | --- | --- |
| 每个 debug 子包的完整可调试性 | UNKNOWN；日志仍有缺少 build-id 的警告，本轮只确认 debuginfo 流程成功及 RPM 写出 | 对所需工具验证调试文件匹配、源路径和实际调试 | J/run/build.log、J/memory-profile-resume.json |
| RPM 容器逐字节可复现 | 未实测独立完整重建的容器字节对照；本轮 BUILDTIME 均为 0 | 在固定输入、构建和打包元数据下，独立完整构建并比较 | 第 6 节源文件/配置/增量产物等价性证据 |
| 旧编译阶段每个 compiler 的真实 VmHWM | UNKNOWN；当时只有 30 秒资源采样，无法回溯完整逐进程高水位 | 后续构建保留新增 2 秒逐进程采样，并注意采样下界 | L/samples.jsonl、J/run/process-memory.jsonl |
| 未被采样覆盖的单次链接峰值 | UNKNOWN；Top 10 限于已记录 50 个进程 | 连续进程级或逐命令 time/cgroup 计量 | L/linker-memory-observations.jsonl |
| PGO 插桩实际高水位 | UNKNOWN；当前资源预算已不能批准完整重建 | 更充足内存环境中的受限实测 | 第 11 节容量计算 |
| 单独 BOLT 重写实际高水位 | UNKNOWN；未执行 BOLT，不能由 ThinLTO 数字代替 | 对指定二进制与 profile 做受限实测 | 第 11 节容量计算 |
| 本机基准排序与 Chromium 全量耗时一致性 | UNKNOWN；本机未构建 Chromium | 专用服务器后续全量对照 | 第 1、10 节验证体系范围 |
| clang 18 与本基线的优化收益比 | 本轮不能推导；资源目录、预处理输入及链接夹具不同 | 统一可兼容输入、资源目录和夹具后受控对照 | 第 9、10 节及参考轮 JSON |

## 13. 命令、原始输出与复核入口

原始数据留在本机 temp/，不进入 Git。以下路径按第 1 节展开，命令保存在对应日志、
JSON 的 argv/invocation 字段或脚本中；报告中的表由这些记录生成，未用推测补齐缺项。

| 操作 | 完整命令与原始输出 |
| --- | --- |
| reference 解析、固定快照归档 | Q/resolve.py、Q/resolution.log、A/各快照目录、P/commands.log |
| 初次限流 GBS 构建与配置门禁 | L/build.log、L/time-v.txt、L/samples.jsonl、L/CMakeCache.txt |
| 宏影响面、GBS/RPM 续跑调查 | J/preflight-investigation.log、J/investigation-evidence.log、J/smp-all-macros.log、J/rpm-help.log、J/rpm-source/ |
| `%prep` 输入等价性 | J/verify-prepared-source.py、prepared-source-equivalence.json、verify-prep-patches.py、prep-patch-replay.log、prep-patch-equivalence.json |
| 独立构建根复制 | J/clone-root.py、clone.log、clone-result.json；早期失败尝试单独保留于 J/clone-attempt1/ |
| Ninja 空转评估与实际增量核对 | J/ninja-preflight-input.sh、ninja-preflight.log、incremental-output-equivalence.json、cmake-command-equivalence.json、resume-cache.diff |
| 正常 rpmbuild 续跑 | J/run/commands.log、build.log、time-v.txt、outcome.json；原命令 J/original-build-command.sh，argv 对照 J/rpmbuild-command-equivalence.json |
| 限流、进程树及清理 | J/run/samples.jsonl、process-memory.jsonl、scope-after-rpm.json；J/resume-priority-check.log、debug-j4-priority.log、resume-descendant-cgroups.json、resume-cleanup-verification.json |
| RPM 清单、解包、重叠文件检查 | J/inventory-extract-rpms.py、rpm-inventory-extraction.log、rpm-inventory.json、rpm-file-dumps.log、rpm-overlapping-files.json |
| 五工具及旧 accel 对照 | J/rpm-toolchain-verification.log/json、J/elf-code-equivalence.json、L/accel-reference.log/json |
| 独立 libxml2 运行库 | J/runtime-extraction.log、runtime-loader-query.log、runtime-manifest.json |
| ARM 真实 TU 采集与 clang 18 兼容性探测 | J/real-tu/collection.json 及同目录日志、J/arm-feasibility-probe/、J/reference-real-tu/collection.json、J/reference-inputs/ |
| 基准与校准全部子命令 | D/各轮 -raw/commands.json 及逐命令 stdout/stderr；J/calibration-launch.json、calibration-console.log、正式轮及参考轮 launch/console 记录 |
| 内存画像整理 | J/summarize-memory.py、memory-profile-old.json、summarize-resume-memory.py、memory-profile-resume.json |
| 静态归档 strip 核对 | J/analyze-archive-strip.py、static-archive-strip-result.json、static-archive-rpm-extract.log |
| 脚本验证 | J/bench-tests.log（12 项通过）、J/build-guard-tests-final.log（5 个测试方法，包含 10 种退出/门禁场景，通过） |
| 提交、推送、远端复核 | J/publication.log、J/publication-verification.json；本报告对应提交的固定 raw 链接在完成回复中提供 |

`tools/resume_llvm_x86_64.py --help`、`tools/collect_llvm_real_tu.py --help`、
`tools/bench_toolchain.py --help` 提供入口参数。续跑脚本专用于本次经审计的构建现场，
不是对任意失败构建无条件跳过 `%prep` 的通用开关；输入证据不匹配时应拒绝。
新的完整构建入口仍为 `tools/build_llvm_x86_64.sh`，但当前容量门禁会拒绝按旧预算启动。

## 14. 提交前自检

1. **内存上限机制、实际峰值、采样器回收？** 使用 systemd user scope 的 MemoryMax=18G、MemorySwapMax=0；没有提高上限。
   最终 cgroup MemoryPeak=19,327,094,784 B，memory.events 的 oom/oom_kill 均为 0。
   debuginfo -j4 阶段进程树 RSS 观察峰值 5.896 GiB；GNU time 单进程最大 RSS 3,471,968 KiB。
   采样线程、日志线程和记录的构建进程已全部回收。证据：J/run/outcome.json、scope-after-rpm.json、time-v.txt、J/resume-cleanup-verification.json。
2. **`_toolchain` 在 x86_64 构建时是否定义？** 是，clang。固定 Unified build.conf:161、根内 home/abuild/.rpmmacros:63，
   续跑实际宏查询 `clang|-j4`。没有通过 define 改写 `_toolchain`。`_smp_mflags` 不被此 spec 的 `%build` 使用，
   Ninja 已单独固定 4；新增 define 只影响此配方的 debuginfo 并发。证据：第 3、6 节及 J/run/build.log。
3. **CMakeCache 是否全部通过？** 是；原门禁 297.775 秒，本轮重新写入 Cache 后 6.052 秒再通过。
   Release、Thin、两个 DYLIB=OFF、lld、assertions=No（OFF）、CXX -O3 且没有 -Os、X86/ARM 均存在；关键行完整列于第 7 节。
4. **最终 RPM 产物 NEEDED 是否仍有 LLVM 共享库？** 五工具均无 libLLVM/libclang-cpp，版本 22.1.8，验证 PASS。
   lld 的 libxml2.so.16 从固定快照 RPM 独立解包，用 loader --library-path 解决；未安装到宿主、未修改二进制。
   证据：J/rpm-toolchain-verification.json/log、runtime-manifest.json。
5. **重新校准噪声底是多少？** 0.755300%，15 项全部通过 3% 门禁，CV 均 ≤3%，无保留可疑样本。
   正式基线与两轮校准的协议、工具身份、夹具 hash 完全一致。四轮基准最高 RSS 为 1,188,752 KiB。
   证据：D/calibration-01.json、D/各轮 JSON、J/benchmark-validation.json。
6. **是否修改 spec 并发数以外的内容？** 否。本轮 spec 和 gbs_llvm.conf 均未新增改动；相对源 HEAD 仅保留既有三处 4/4/1 修改。
   新增的是调用中的 `_smp_mflags -j4`、批准的六项 TU 白名单、必要的限流/续跑/采集/运行库入口及其测试。
   证据：J/prepublication-checks.log 与本提交 diff。
7. **是否构建 Chromium 或向 Gerrit 推送？** 否。LLVM 续跑使用保留输入的正常 RPM 流程，真实 TU 和合成文件属于基准负载；
   本任务只向 GitHub origin/main 交付文档、脚本与小输入，原始日志、RPM、大 .ii 均留 temp/。
8. **回复是否列出全部 raw 链接及一个固定提交链接？** 完成回复逐项列出本次 docs/ 与 tools/ 交付文件的 raw 链接，
   并提供固定到本次提交号的报告 raw 链接；远端 SHA 和 raw 内容复核记录在 J/publication-verification.json。
9. **续跑等价性是否有证据？** 有。归档/补丁准备树校验、独立副本、原 argv 对照、相同 CMake 参数、
   103 个增量输出 SHA 相同、三个独立工具构建 ELF 不变、正常 install/打包 hook、无 ShortCircuited 依赖，见第 6、7 节。
   没有把这一结论扩大成 RPM 容器逐字节可复现或全部开发子包功能验收。
10. **是否真实 ARM 预处理？** 是。10 个 -E 命令固定 ARM triple/sysroot，__arm__ 宏验证通过，
    后续完整测量的编译产物逐一通过 ARM ELF 检查。没有修改或伪装 x86_64 生成头。
11. **30 GB 物理内存够做后续 PGO/BOLT 吗？** 按当前 18 GiB cap 与 60% 链接预算，PGO 完整构建规划为 NO；
    单独 BOLT 为 UNKNOWN，需实测。已观察普通链接 16.831 GiB，不能继续沿用 8 GiB 估值，见第 11 节。
12. **是否完整说明 RPM 限制？** 是。22 个 RPM 成功写出；五个可执行工具已验证和测量。
    抽查的静态开发归档符号索引被 GNU strip 删除，以及缺少 build-id 的警告均未掩盖，也未擅自修配方。
