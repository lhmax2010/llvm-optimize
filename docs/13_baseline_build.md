# 自研优化版 x86_64 LLVM：构建前置检查与阻塞记录

记录时间：2026-09-16，Asia/Shanghai。

## 1. 当前结论：BLOCKED，尚未构建

**当前生效的 Base 包源返回 HTTP 404，按任务第一步的包源门禁停止。**
没有执行 `gbs build` 或 `rpmbuild`，没有创建正式构建根，没有修改
`gbs_llvm.conf`、LLVM 源码或 spec；后续的 RPM 验证、真实 TU 采集、重新校准和
正式基准均未执行。本报告不把旧的 0.220% 校准结果当成本次 clang 22 的结果。

已交付限流构建入口、实现、产物检查脚本和保护逻辑测试；它们经过只读预检、
查询命令和模拟子进程测试，**尚未经过真实 LLVM 构建验证**。

| 前置条件 | 结果 | 证据 |
| --- | --- | --- |
| 工作区 LLVM HEAD | `f111162e94aa48ed367c9d2c039456c70e7160ae`，工作树干净 | P/script-check/commands.log 中 git 输出 |
| 可用内存 ≥ 16 GiB | PASS：22.929450989 GiB | P/script-check/resource-plan.json |
| 构建根所在磁盘可用 ≥ 60 GiB | PASS：1067.667564392 GiB | 同上 |
| systemd 用户 scope 内存限额 | 可用；小进程探针确认设置和整组终止命令成功 | P/scope-control.log |
| x86_64 包源 | **BLOCKED**：Base 404；Unified 有 3078 个 x86_64 RPM，但缺失下述基础构建包 | P/metadata-fetch.log、P/base-reference-readonly.log、P/script-check/repositories.json |
| `_toolchain` | 当前可下载的 Unified build.conf 对 x86_64 定义为 clang | U:146–168；P/script-check/commands.log 的 `1\|clang` 输出 |
| 正式构建与基准 | NOT RUN | P/script-check/stopped.json；正式构建根不存在 |

本报告路径缩写：

- `W` = `/home/linhao/Toolchain/development/llvm-optimize`
- `S` = `W/llvm/packaging/llvm.spec`，上述 HEAD
- `P` = `W/temp/baseline-build-preflight`
- `U` = `P/repo.unified-standard.build.conf`
- `B` = `W/temp/gbs-root-x86_64-baseline`（未创建）

## 2. 包源阻塞与待决策的最小变更

`gbs_llvm.conf:8–11` 的同一节存在两个未注释的 `url`。
本机 GBS 使用 `BrainConfigParser(strict=False)`，后一项覆盖前一项，见
`/usr/lib/python3/dist-packages/gitbuildsys/conf.py:319`。
因此第 9 行的 reference URL 目前没有生效。

原始输出摘录（P/metadata-fetch.log）：

```text
2026-09-16T22:39:41.616978+08:00 GET http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260804.124315/repos/standard/packages/repodata/repomd.xml
HTTPError HTTP Error 404: Not Found
2026-09-16T22:39:42.337410+08:00 GET https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/reference/repos/standard/packages/repodata/repomd.xml
HTTP 200 FINAL https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/reference/repos/standard/packages/repodata/repomd.xml
X86_64_PACKAGE_COUNT 3078
```

这里不是“所有源都没有 x86_64”。Unified 确有 x86_64 包，但其 primary.xml 中
找不到 x86_64 的 `clang`、`llvm`、`lld`、`gcc`、`glibc`、`ninja`、`cmake`、
`rpm-build`、`binutils` 这些包名；失效的 Base 源不能由它代替。
逐项存在性检查保存为 P/unified-package-coverage.json。
`S:51–60` 还直接要求 cmake、ninja 等构建依赖。

已只读检查配置第 9 行的
[Base reference 仓库元数据](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/reference/repos/standard/packages/repodata/repomd.xml)。
它返回 HTTP 200，有 537 个 x86_64 包，包含 clang/llvm 22.1.8-1.6、
cmake 3.31.2-1.2、ninja 1.13.1-1.9、glibc 2.40-1.10 和 rpm-build 4.14.1.1-1.4。
这些是可供引导构建的仓库包，**不替代待构建的 f111162e 基线产物**。
证据：P/base-reference-readonly.log 和保存的 primary.xml。

待用户决定的最小变更如下，**尚未应用**（P/proposed-config.diff）：

```diff
 [repo.base-standard]
 url=https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/reference/repos/standard/packages/
-url=http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260804.124315/repos/standard/packages/
+#url=http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260804.124315/repos/standard/packages/
```

上面仅摘录有关行，完整上下文见该 diff。选择此源后仍须重新运行所有前置检查；
reference 内容会变化，脚本保存每次实际取得的元数据、摘要和 build.conf。
没有自行换源，也没有加 `--define _toolchain` 绕过检查。

## 3. `_toolchain` 的定义来源与分支

GBS 的仓库处理逻辑按配置顺序读取 repo；标准仓库 repomd.xml 的 `type=build`
项给出 build.conf，读取后赋给 `self.buildconf`。本配置最后是 Unified，
依据 `/usr/lib/python3/dist-packages/gitbuildsys/utils.py:430–447,463–496`。
当前 gbs 配置未设置单独的 `buildconf`。GBS 选择过程见
`/usr/lib/python3/dist-packages/gitbuildsys/cmd_build.py:176–192`。

下载到的 U 有如下定义（不是 ARM 专属分支）：

```text
146 Macros:
150 %__cc_clang %{_host}-clang
151 %__cxx_clang %{_host}-clang++
161 %_toolchain %{?_toolchain_override}%{!?_toolchain_override:clang}
166 %__cc %{expand:%%{__cc_%{_toolchain}}}
167 %__cxx %{expand:%%{__cxx_%{_toolchain}}}
184 :Macros
```

用本机 GBS 后端按 x86_64 解析该配置，再用 RPM 读取生成的宏文件：

```sh
/usr/lib/build/queryconfig --dist "$P/repo.unified-standard.build.conf" \
  --archpath x86_64 rawmacros > "$P/x86_64.rpmmacros"
rpm --macros "/usr/lib/rpm/macros:$P/x86_64.rpmmacros" \
  --eval '%{defined _toolchain}|%{_toolchain}'
```

实际输出（脚本复核也相同）：

```text
1|clang
```

这里证明 **仓库配置的宏展开**，还没有新构建根的运行时宏证据。
宿主 RPM 的 `_host` 展开是宿主环境的值，不能拿来宣称新 Tizen 根的最终 triple。
首次试用宿主 `rpm --load ... --target ...` 时，宿主默认 `__cc` 覆盖了加载值；
该试验输出保留在 P/macro-evaluation.log，但不用于判断 Tizen 编译器。
上面的显式宏文件顺序输出见 P/macro-evaluation-controlled.log。

据此，`S:11–16` 应取真分支：`_toolchain_override=clang`、`llvm_release_build=0`；
`S:229–236` 应传 lld、ThinLTO、llvm-ar 和 llvm-ranlib。
`U:121–127` 中 `mlgo_build_jobs=6` 只对 armv7l/aarch64 生效，x86_64 不被该段覆盖，
所以可调整 `S:48` 的并发默认值。`S:7–8` 自身为 x86_64 默认开启 MLGO。

当前 spec 不再传 `LLVM_LINK_LLVM_DYLIB` / `CLANG_LINK_CLANG_DYLIB`。
前者默认 OFF 来自 `llvm/llvm/CMakeLists.txt:912`；后者继承前者来自
`llvm/clang/CMakeLists.txt:309`。静态链接 LLVM 库的预期需要这两个默认值和最终
NEEDED 检查共同验证，不能仅以“参数已删除”宣布成功。
`LLVM_BUILD_LLVM_DYLIB=ON` / `CLANG_BUILD_CLANG_DYLIB=ON` 仍会构建共享库；
“构建共享库”与“工具链接共享库”是不同开关。

## 4. 机器资源与限流计算

2026-09-16 22:47:31 的原始输出（P/script-check/commands.log）：

```text
$ nproc
20
$ free -g
               total        used        free      shared  buff/cache   available
Mem:              30           7          10           0          13          22
Swap:              3           0           3
$ df -h /home/linhao/Toolchain/development/llvm-optimize/temp
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       1.8T  672G  1.1T  39% /home
```

精确值取 `/proc/meminfo` 的 MemAvailable 和 `shutil.disk_usage`，避免把 `free -g`
的向下取整当成精确值：内存 24,620,310,528 B = 22.929450989 GiB；
磁盘 1,146,399,318,016 B = 1067.667564392 GiB。两项门槛均通过。

| 项目 | 本次预检计划 | 计算或用途 |
| --- | --- | --- |
| 整个 scope 的 MemoryMax | 18 GiB | `floor(22.929450989) - 4`，在当前可用内存外留至少 4 GiB |
| GBS `--threads` | 1 | GBS 的包级并发，不能代替 Ninja 并发限制 |
| Ninja `mlgo_build_jobs` | 4 | 限制 Ninja 总任务数 |
| `LLVM_PARALLEL_COMPILE_JOBS` | 4 | 最多半数 CPU，并额外封顶 4；每个编译任务暂按 2 GiB 预算 |
| `LLVM_PARALLEL_LINK_JOBS` | 1 | 1 × 8 GiB = 8 GiB < 22.929450989 × 60% = 13.757670593 GiB |
| 编译、链接和其他开销预算 | 18 GiB | 1 × 8 + 4 × 2 + 2 = 18 GiB；编译预算是限流假设，尚未实测 |

原 spec 的链接并发 2 对应 16 GiB，超过 13.758 GiB，不能直接使用。
计划仅将 `S:48` 的 6 改为 4、`S:274` 的 6 改为 4、`S:275` 的 2 改为 1。
**本次实际 spec diff 为空**，因为包源门禁未通过；脚本只在 `--run` 且前置检查
全部通过之后修改这三处数字，并保存完整 diff。启动前会重算资源，不固定沿用本表数字。

### 内存机制与生命周期

本机 systemd 用户 scope 实测可用，故后续应使用它，不需要 prlimit 后备路径。
无构建负载的探针原始输出（P/scope-control.log）：

```text
ControlGroup=/user.slice/user-1000.slice/user@1000.service/app.slice/llvm-limit-probe-10624f6bb90a4cd38233ff5c4588aafd.scope
MemoryCurrent=425984
MemoryPeak=524288
MemoryMax=1073741824
MemorySwapMax=0
rc=0
['systemctl', '--user', 'kill', '--kill-whom=all', '--signal=SIGTERM', 'llvm-limit-probe-10624f6bb90a4cd38233ff5c4588aafd.scope']
rc=0
child_wait=-15
```

这里的 524,288 B 是 `/bin/sleep` 探针的 scope 峰值，**不是 LLVM 构建峰值**。
LLVM 构建耗时和峰值均为 UNKNOWN / NOT RUN。

实现见 `tools/build_llvm_x86_64.py` 的 `resource_plan`、`build`、`monitor`、
`stop_build` 和 `main`：

- 外层 `/usr/bin/time -v`，其内 `systemd-run --user --scope -p MemoryMax=<N>G
  -p MemorySwapMax=0`，随后 `nice -n 15 ionice -c3 gbs ...`。MemoryMax 对 scope
  内整个进程组生效，包含继承该 cgroup 的构建子进程。
- 如果 systemd 探针失败，则使用继承给子进程的 `prlimit --as=<bytes>:<bytes>`。
  **RLIMIT_AS 是逐进程地址空间上限，不是整个进程树的硬内存上限**；后备路径另以
  每 2 秒进程树 RSS 检查中止超额构建。它仍有采样间隔，且终止特权子进程可能受权限
  限制。本机没有用到此后备机制，不把它与 cgroup 的保障混为一谈。
- 后台采样线程每 30 秒写 `samples.jsonl`，含 `free -m` 原文、loadavg、
  外层构建进程及全部可追踪后代的 RSS 总和、PID/RSS 清单及 cgroup MemoryCurrent/
  MemoryPeak/memory.events。RSS 求和会重复计算共享页，不能等同 cgroup 实际用量。
- 守护轮询每 2 秒检查 MemAvailable；小于 2 GiB、配置不符或配置门禁超时即终止
  scope 的全部进程。日志、源导出、失败构建根与 Cache 保留。
- 后台工作采用进程内线程；正常退出、失败、SIGINT/SIGTERM/SIGHUP/SIGQUIT 均进入
  `finally` 设置退出事件并 `join` 采样线程，将回收状态写入 `outcome.json`。
  不会留下独立运行的采样进程。不可捕获的 SIGKILL 不会执行 Python 清理，但 OS
  会随进程销毁其线程。

真实 GBS 特权子进程的 scope 归属、终止效果和实际峰值，仍需首次获准构建时核验。

## 5. x86_64 CMake 预期清单

下表是 **从 S 推导的预期，尚非 CMakeCache 实测**。G = 展开的 `_host`，
PFX = `_prefix`，LIB = `_lib`，A = 源码目录下 `mlgo_verify_assets`。
新构建根尚不存在，G/PFX/LIB 的最终 RPM 宏值不以宿主宏猜测。

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
| `LLVM_PARALLEL_COMPILE_JOBS` | 当前 6；获准启动时按资源计划改为 4（重新计算为准） | S:274 |
| `LLVM_PARALLEL_LINK_JOBS` | 当前 2；获准启动时按资源计划改为 1 | S:275 |
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

### 配置门禁状态

**NOT RUN：没有真实 CMakeCache.txt，不能贴出实测关键行。**
脚本自 GBS 启动计时，最多等待 900 秒，每 2 秒定位主 LLVM build 目录的 Cache；
首次发现即复制到日志目录并验证以下七组条件，任何缺项也视为失败：

1. Release；2. Thin；3. 两个 DYLIB 链接开关均为假；4. lld；5. assertions 为假；
6. CXX flags 含独立的 `-O3` 且不含 `-Os`；7. targets 同时包含 X86 与 ARM。

另外核对 Cache 的两个并发池值与资源计划相等。布尔值接受 CMake 的
OFF/NO/FALSE/0 等价表示。只有门禁通过才允许继续；本报告不将模拟 Cache 的
PASS 当成真实配置通过。

## 6. 产物验证与 accel 对照：待构建

`tools/verify_toolchain.sh` 接受含 `bin/` 的根或 RPM 解包后的含 `usr/bin/` 的根，
对五个工具逐项执行 `ls -la`、`file -L`、`readelf -h/-d`、`--version`，计算已解析
ELF 文件的字节数和 SHA256，输出 JSON、原始日志与 Markdown 表。
工具缺失、逃出解包根的符号链接、非 x86_64 ELF、版本查询失败，或 NEEDED 出现
`libLLVM`/`libclang-cpp`，均返回 2（BLOCKER）。它不安装 RPM、不改变系统工具。

下表仅复用 docs/10 已有 accel 证据，新产物列保持 UNKNOWN：

| 工具 | docs/10 accel 字节数 | accel LLVM NEEDED | 新基线大小 / NEEDED / SHA / 版本 |
| --- | ---: | --- | --- |
| clang | 131592 | libclang-cpp.so.22.1、libLLVM.so.22.1 | UNKNOWN / NOT BUILT |
| clang++ | 131592 | 同上 | UNKNOWN / NOT BUILT |
| ld.lld | 6449904 | libLLVM.so.22.1 | UNKNOWN / NOT BUILT |
| llvm-ar | 81232 | libLLVM.so.22.1 | UNKNOWN / NOT BUILT |
| llvm-ranlib | 81232 | libLLVM.so.22.1 | UNKNOWN / NOT BUILT |

大小和依赖证据：`docs/10_tizen_llvm_build_config.md:1177–1179,1203,1209,1262`，
原始逐项 ELF 数据见 `W/temp/build-config-audit/tool_inventory.json`。
这些 accel 项目的包身份是 clang-accel-x86_64-armv7l；不能仅依据包名里的 0.4
把它当成 clang 的版本。与新产物逐项版本的最终并排比较待构建后补齐。

脚本查询验证使用现有 bundled 根和显式宿主 loader，未编译文件。
clang/clang++/ld.lld/llvm-ar 的 ELF 查询和 `--version` 成功；该 bundled 根没有
llvm-ranlib，脚本按预期返回 2，而非错误地判为工具集完整。
输出：P/verify-smoke-command.log、P/verify-bundled-final.json/.log。
这项测试不是新基线产物验证。

## 7. 真实 TU、重新校准和正式基线：均未执行

| 产出 | 当前状态 | 原因 / 后续条件 |
| --- | --- | --- |
| 新 RPM / `temp/toolchain-baseline/` | NOT BUILT | Base 源门禁失败，未启动构建 |
| Sema/CodeGen/Transforms/Target/ARM/MC 的 8–10 个真实 TU | NOT COLLECTED | 无新 build.ninja 和新 clang++；real_tu 仍仅有 README |
| clang 22 两轮完整校准 | UNKNOWN / NOT RUN | 无新产物及其资源目录 |
| A/B/C、真实 TU、lld、ar 正式数据 | UNKNOWN / NOT RUN | 需新输入集的完整校准先通过 3% 门槛 |
| bundled clang 18 参考轮 | NOT RUN | 没有先得到基线，本轮仅运行 --version 等查询 |
| `temp/bench_results/baseline-*/` JSON | 未生成 | 不生成空数据冒充测量 |

解除阻塞后的执行顺序仍是：配置门禁 → 完整 RPM 构建 → 解包验证 → 真实 TU →
新工具链两轮校准 → 正式基线 → bundled 18 独立参考轮。
真实 TU 必须按 `tools/bench_inputs/real_tu/README.md` 用 ARM triple 和 ARM sysroot
预处理，不能把 LLVM 的 x86_64 预处理文本重新标为 ARM；原命令与实际预处理命令均需保留。
超过 10 MB 的 `.ii` 放 temp，并由 flags sidecar 绝对路径引用。

两套工具链必须分别使用自己的资源目录。将来 bundled 18 数据必须标为：
**“资源目录不同，不是受控对照，仅供量级参考”**。
本机不进行 Chromium 全量验证；基准台作为分钟级快速筛选层，最终吞吐验收仍在
专用构建服务器执行 Chromium 全量构建，参见 docs/12。

## 8. 用法、测试与证据索引

```sh
# 默认只检查，当前配置应因 HTTP 404 返回 2，不会改 spec 或启动构建。
tools/build_llvm_x86_64.sh

# 包源问题获得明确决定并处理之后，重新预检通过才能使用：
tools/build_llvm_x86_64.sh --run

# 查看参数；支持指定 source/config/buildroot/log-dir，拒绝复用已存在的构建根。
tools/build_llvm_x86_64.sh --help
tools/verify_toolchain.sh --help

# 将来逐个解包所需 RPM，DEST 必须是独立 temp 目录；此处没有执行解包。
# rpm2cpio /实际/产出的.rpm | (cd "$DEST" && cpio -idm --no-absolute-filenames)
# tools/verify_toolchain.sh --root "$DEST" --output temp/实际日志目录/verification.json

# 保护逻辑测试；GBS 启动调用在测试中替换为临时 Python 小进程。
python3 tools/test_build_llvm_x86_64.py
```

脚本将下载到且通过宏检查的原始 build.conf 以 `gbs -D <日志目录>/buildconfig.conf`
传入；内容不作修改，避免检查后又取另一份宏配置。没有通过 `-D` 添加新宏。
正式启动形状如下，真正完整 argv 会在执行之前写入日志：

```text
/usr/bin/time -v -o <log>/time-v.txt systemd-run --user --scope --unit=<unique>.scope -p MemoryMax=18G -p MemorySwapMax=0 nice -n 15 ionice -c3 gbs -c /home/linhao/Toolchain/development/llvm-optimize/gbs_llvm.conf build -A x86_64 -B /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-baseline --threads 1 --include-all -D <log>/buildconfig.conf /home/linhao/Toolchain/development/llvm-optimize/llvm
```

此行是按本次资源计划展示的命令模板，**未执行**。`--include-all` 使仅有的 spec
并发修改进入源码导出；脚本先拒绝 LLVM 工作树里其他修改或未跟踪文件，并比较
HEAD 与工作树 spec，确认差异只限三处并发数字。

测试包括资源阈值边界、并发预算、不允许修改优化参数、全部 Cache 条件拒绝测试，
以及正常退出、配置不符、低内存、子进程失败、配置超时、外部中断六种生命周期模拟。
生命周期模拟没有启动 GBS 或任何编译器；均断言 `sampler_reaped=true` 和
`log_reader_reaped=true`。模拟日志会显示待替换的命令模板，紧接着明确记录实际
执行的 Python argv，不应将其模板误读为执行过 GBS。

原始输出全部放在 P：

| 文件 | 内容 |
| --- | --- |
| `repo-index.log`、`metadata-fetch.log` | 当前两源目录/元数据的 HTTP 状态、URL、摘要和包计数 |
| `repo.unified-standard.repomd.xml`、`.build.conf`、`.primary.xml` | 原始 Unified 元数据；primary 超过 10 MB，留 temp |
| `unified-package-coverage.json` | Unified 中上述九个 x86_64 包名的存在性结果，均为 false |
| `base-reference-readonly.log`、`base-reference.repomd.xml`、`.primary.xml` | 待选源的只读核验，未修改配置 |
| `x86_64.rpmmacros`、`macro-evaluation*.log` | x86 宏提取和两种宿主查询的原始输出 |
| `resources.json`、`local-preflight.log` | 较早一次资源快照及 systemd 真值探针 |
| `scope-control.log` | 1 GiB scope 的属性、峰值和终止/回收输出 |
| `script-check/` | 独立预检脚本的一次真实执行：命令、资源计划、仓库快照、宏查询、停止原因 |
| `proposed-config.diff` | 未应用的单行换源建议 |
| `gate-tests.log` | 5 个测试方法，含 6 种生命周期模拟的 outcome |
| `verify-smoke-command.log`、`verify-bundled-final.json/.log` | 现有 bundled 工具的只读查询及预期退出码 2 |
| `build-help.txt`、`verify-help.txt` | 两个入口的帮助输出 |

## 9. 提交前自检

1. **内存上限机制、实际峰值、采样器回收？** 已验证本机 systemd scope 可用，
   计划 MemoryMax=18 GiB；正式构建尚未启动，实际 LLVM 峰值 UNKNOWN。
   1 GiB sleep 探针峰值 524,288 B。六种模拟退出路径均验证线程回收；真实 GBS 回收待验证。
2. **x86_64 的 `_toolchain` 是否定义？** 当前 Unified build.conf：是，clang；
   U:161、x86_64 rawmacros 和 `1|clang` 输出为依据。新构建根的实测尚不存在。
3. **CMakeCache 门禁是否全部通过？** 未运行。没有真实关键行，不能回答“已通过”；
   预期表和检查器已经准备好。
4. **新产物 NEEDED 是否仍有 LLVM 共享库？** UNKNOWN，没有新产物；检查器会将其判为 BLOCKER。
5. **重新校准噪声底？** UNKNOWN / NOT RUN；不沿用 clang 18 的 0.220%。
6. **是否修改 spec 并发数以外的内容？** 否。本次连并发数也尚未修改，LLVM 工作树干净。
7. **是否构建 Chromium 或向 Gerrit 推送？** 否，也没有启动 LLVM 构建或 rpmbuild。
8. **完成回复是否列出全部 raw 链接？** 列出本报告、构建 shell 入口、Python 实现、
   产物验证脚本及测试脚本共 5 个链接。尚未产生真实 TU 或基准 JSON。
