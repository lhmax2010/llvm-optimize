# 自研优化版 x86_64 LLVM：固定快照、限流构建与基线

更新时间：2026-09-17T08:49:47+08:00。

## 1. 状态与范围

**BUILDING：配置门禁已通过，构建中。** 当前唯一源码基线是工作区 LLVM
`f111162e94aa48ed367c9d2c039456c70e7160ae`。没有回退到已安装 RPM 的构建配方。
使用原生 x86_64 GBS 构建，保留 spec 的 -O3、ThinLTO、-fomit-frame-pointer、
静态链接 LLVM 库及 MLGO 设置。源码侧只允许三处并发数字变化。

本次已将 Base 和 Unified 分别固定为其 reference 当前实际指向的快照，
完整预检通过，随后真实执行 `tools/build_llvm_x86_64.sh --run`。
资源守护、配置门禁和日志机制沿用已有脚本，未改动 tools/ 中的实现。
不构建 Chromium，不向 Gerrit 推送。

验证体系分两层：本机基准台用于分钟级筛选 LLVM 变体；最终验收是专用构建服务器
的 Chromium 全量构建耗时。本机不做后一层。本次 clang 22 与新增真实 TU 输入集
必须重新校准，不能沿用 docs/12 的 clang 18 噪声结果。

路径约定（均是本机真实路径）：

| 符号 | 路径 |
| --- | --- |
| W | `/home/linhao/Toolchain/development/llvm-optimize` |
| S | `W/llvm/packaging/llvm.spec` |
| Q | `W/temp/snapshot-resolution-20260917` |
| A | `W/temp/snapshot-archive` |
| P | `W/temp/baseline-preflight-20260917` |
| L | `W/temp/baseline-build-20260917` |
| B | `W/temp/gbs-root-x86_64-baseline` |
| U | `A/tizen-unified-toolchain_20260814.092727/build.conf` |

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

## 4. 资源、并发、实际启动命令

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
| 链接内存预算 | 1 × 8 GiB < 13.682291 GiB | 严格小于可用内存的 60% |
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

### 守护与实测内存

脚本后台线程每 30 秒落盘 free -m 原文、loadavg、进程树 RSS 总和、PID 清单及 cgroup
内存属性；每 2 秒检查 MemAvailable，小于 2 GiB 立即中止并保留现场。
正常退出、失败及可捕获中断均在 finally 中 join 采样线程；结果写 outcome.json。
本机 systemd 用户 scope 可用，实际使用 cgroup 聚合内存上限，没有走 prlimit 后备。

截至本次报告生成：采样 13 次，可用内存最低 21.561661 GiB；
进程树 RSS 求和最大 1144090624 B（1.065517 GiB）；从有效 scope 采样读到的
MemoryPeak 最大 7214977024 B（6.719471 GiB）。RSS 求和重复计共享页，cgroup
用量还包括文件缓存，两者不能混用。构建最终数据必须以结束后的记录补齐。

构建尚未结束；最终耗时、time -v 峰值 RSS 和真实采样器回收结果暂为 PENDING。

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

### 实际配置门禁

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

## 6. 产物验证、真实 TU 和吞吐基线

以下阶段必须等待构建成功，当前不能给出成功结论或测量数字：

| 项目 | 当前数据 |
| --- | --- |
| 新 RPM 解包到 temp/toolchain-baseline/ | PENDING / 未完成 |
| clang、clang++、ld.lld、llvm-ar、llvm-ranlib 的大小/SHA256/NEEDED/版本 | UNKNOWN，待新产物 |
| 静态链接 LLVM 库是否实际生效 | UNKNOWN；任一 NEEDED 含 libLLVM/libclang-cpp 则为 BLOCKER |
| 8–10 个真实 TU（Sema/CodeGen/Transforms/Target/ARM/MC） | 未采集 |
| clang 22 两轮完整噪声校准 | UNKNOWN / NOT RUN；门槛仍为 3% |
| A/B/C + 真实 TU + lld + ar 正式基线 | UNKNOWN / NOT RUN |
| bundled clang 18 独立参考轮 | UNKNOWN / NOT RUN |
| 基线 JSON | 尚未生成 |

产物验证入口是 tools/verify_toolchain.sh，不安装到宿主系统；解包使用 rpm2cpio | cpio。
旧 accel 对照值如下（docs/10 的原始 ELF 清单）：

| 工具 | accel 字节数 | accel LLVM NEEDED | 新基线 |
| --- | ---: | --- | --- |
| clang / clang++ | 131592 | libclang-cpp.so.22.1、libLLVM.so.22.1 | 待产物 |
| ld.lld | 6449904 | libLLVM.so.22.1 | 待产物 |
| llvm-ar / llvm-ranlib | 81232 | libLLVM.so.22.1 | 待产物 |

证据：docs/10_tizen_llvm_build_config.md:1177–1179,1203,1209,1262；完整清单为
W/temp/build-config-audit/tool_inventory.json。新产物版本必须实际执行 --version 后填写。

真实 TU 从本次 build.ninja/.ninja_log 选择中等耗时文件；原始命令与用新 clang++
执行的实际 ARM 预处理命令分别保留。遵守 tools/bench_inputs/real_tu/README.md，
统一 ARM triple/sysroot，不能把 x86_64 预处理文本重标为 ARM。超过 10 MB 的 `.ii`
留 temp，sidecar 通过绝对路径引用。

新工具链用自己的 clang 22 资源目录，完成两轮校准后才跑正式数据。
bundled clang 18 单独运行、使用它自己的资源目录，并必须注明：
**资源目录不同，不是受控对照，仅供量级参考。**

## 7. 复现与证据索引

```sh
# 当前固定配置下只做预检；新的 --log-dir 必须不存在。
tools/build_llvm_x86_64.sh --log-dir temp/下一次预检目录
# 当前 B 已使用，脚本会拒绝覆盖；不要对现有构建根再次 --run。
tools/build_llvm_x86_64.sh --help
tools/verify_toolchain.sh --help
```

| 证据路径 | 内容 |
| --- | --- |
| Q/index-requests.log、Q/*-index.html、Q/*-reference.html | 原始目录索引、HTTP 状态 |
| Q/resolution.log、Q/resolve.py、Q/resolved.json | XML id 解析、双向 repomd 比较、归档摘要 |
| A/两个快照目录/ | repomd、primary、build.conf、压缩原件、manifest |
| Q/config-checksums.json、Q/config.diff、Q/gbs_llvm.conf.before/after | 完整配置前后证据 |
| Q/spec-build-requires.json、Q/check_dependencies.py、Q/dependencies.log/json | GBS 后端解析和包/provides 匹配 |
| P/commands.log、resource-plan.json、repositories.json、x86_64.rpmmacros | 不带 --run 的真实完整预检 |
| L/launch.json、commands.log、build.log | 真实启动 argv、命令原始输出、逐行时间戳构建日志 |
| L/resource-plan.json、spec-concurrency.diff | 启动前资源重算、仅三处数字的 spec diff |
| L/runtime-scope-check.log、priority-check.log、samples.jsonl | 真实 scope 属性、nice/ionice、后台采样 |
| L/cache-gate.json、CMakeCache.txt（出现后） | 门禁结果和实际 Cache 原件 |
| L/outcome.json、time-v.txt（结束后） | 退出码、线程回收、外层时间/RSS |

工具脚本与保护逻辑测试沿用提交 179196d，本轮没有调整限流或放宽任何门禁。
所有大文件及原始输出留在 temp，不纳入提交。

## 8. 提交前自检

1. 内存机制为 systemd 用户 scope / MemoryMax=18 GiB / MemorySwapMax=0；实际峰值、
   耗时与采样器回收状态见第 4 节，未结束时不声称已回收。
2. `_toolchain` 已重新按固定 Unified build.conf 的 x86_64 分支验证为 clang，依据 U:161
   以及 P、L 中的 `1|clang` 原始输出。
3. CMakeCache 是否全部通过、关键行见第 5 节；没有结果时不得声称通过。
4. 新产物 NEEDED 是否仍依赖 LLVM 共享库：待真实产物验证，不能以 spec 预期代替。
5. 新噪声底：待 clang 22 + 新 TU 集的两轮校准，不沿用旧值。
6. 除三处并发数外是否修改 LLVM 源码/spec：否。gbs_llvm.conf 只修改 URL 行，完整 diff
   和前后 SHA256 见第 2 节；tools 实现未修改。
7. 是否构建 Chromium 或向 Gerrit 推送：否。
8. 配置门禁通过后的中间回复及最终回复均列报告、配置与全部相关 tools 的 raw 链接；
   若后续生成真实 TU/sidecar，也逐个列出其 raw 链接。
