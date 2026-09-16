# 10 Tizen LLVM 构建配置与 Chromium bundled LLVM 对照

调查日期：2026-09-16。范围：只读源码、Git 对象、RPM 数据库、宏和脚本、已有日志、ELF 信息及工具查询。没有构建 LLVM/Chromium，没有执行 `gbs build` 或 `rpmbuild`，没有修改 LLVM 源码或配置。

用户提供的受控性能对照、背景负载、历史采样、断言状态与 Chromium 构建形状均作为既定前提；本报告不重测、不重新裁定这些结论。下文的频度为调用规则对应的量级，不是耗时测量；差异表不提供收益百分比。

证据记号（后文 `文件记号:行号` 均指下列确定的文件，不表示猜测路径）：

| 记号 | 实际文件或路径 |
| --- | --- |
| W | /home/linhao/Toolchain/development/llvm-optimize |
| C | /home/linhao/Toolchain/plan_evaluation/chromium-efl |
| R | /home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0 |
| A | /home/linhao/Toolchain/development/llvm-optimize/temp/build-config-audit |
| S | /home/linhao/Toolchain/development/llvm-optimize/temp/build-config-audit/installed-source；从工作区 LLVM 的 Git 对象 8dfebafe1a477b3dcc678ee4cb18a3a4306d5a7c 导出，只写到 temp/ |
| TS | /home/linhao/Toolchain/development/llvm-optimize/temp/build-config-audit/installed-source/packaging/llvm.spec |
| WS | /home/linhao/Toolchain/development/llvm-optimize/llvm/packaging/llvm.spec |
| B | /home/linhao/Toolchain/plan_evaluation/chromium-efl/tools/clang/scripts/build.py |
| P | /home/linhao/Toolchain/plan_evaluation/chromium-efl/tools/clang/scripts/package.py |
| U | /home/linhao/Toolchain/plan_evaluation/chromium-efl/tools/clang/scripts/update.py |
| RM | /home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0/usr/lib/rpm/macros |
| TM | /home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0/usr/lib/rpm/tizen_macros |
| AM | /home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0/home/abuild/.rpmmacros |
| FD | /home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0/usr/lib/rpm/find-debuginfo.sh |
| GN | /home/linhao/Toolchain/plan_evaluation/chromium-efl/tizen_src/build/toolchain/tizen/BUILD.gn |
| GT | /home/linhao/Toolchain/plan_evaluation/chromium-efl/build/toolchain/gcc_toolchain.gni |
| GS | /home/linhao/Toolchain/plan_evaluation/chromium-efl/build/toolchain/gcc_solink_wrapper.py |
| LOG13 | /home/linhao/Toolchain/plan_evaluation/chromium_analysis/evidence/spike_libcxx/full_gbs_attempt13_visibility.log |
| E编号 | A 下同编号 .log，含实际命令、完整 stdout/stderr 和返回码；第 8 节给出完整索引 |

## 1. 核心结论：PGO / BOLT

**对当前实际安装、执行的整套 Tizen 工具链：PGO = UNKNOWN，BOLT = UNKNOWN。对已安装 ARM RPM 对应的源码打包配方：PGO = NO，BOLT = NO。** 这两种判断的证据强度不同，不能将后者直接升级为前者。

| 对象 | PGO | BOLT | 证据及边界 |
| --- | --- | --- | --- |
| 已安装 ARM RPM 对应的 spec | NO（配方未启用） | NO（配方无后处理步骤） | `TS:198–274` 的完整 CMake 调用；`TS:343–348` 的普通构建/安装；E020、E029、E032 的全文检索。默认 `LLVM_BUILD_INSTRUMENTED=OFF` 位于 `S/llvm/cmake/modules/HandleLLVMOptions.cmake:1181`，`LLVM_PROFDATA_FILE=""` 位于 `S/llvm/CMakeLists.txt:1000` |
| ARM 发布二进制及 libLLVM/libclang-cpp | UNKNOWN | UNKNOWN（未发现 BOLT 节区标记） | E023 保存主程序和两个库的全部节区；没有对应发布任务的完整 configure/build/post-link 日志与 CMakeCache，ELF 未保留 `.GCC.command.line`。负面节区检查不能单独证明没有使用 profile 或后处理 |
| GBS 中实际可被分派调用的 x86_64 accel 工具及库 | UNKNOWN | UNKNOWN（未发现 BOLT 节区标记） | E027 的既有 execve 记录显示 `/usr/bin/clang++` 分派到 `/emul//usr/bin/clang-22`；E016/E027 表明 accel 来自 `qemu-accel` 包，不能直接用 ARM LLVM RPM 的 VCS 证明其原始构建参数；E023 检查其主程序与共享库 |
| 工作区当前 spec | NO（配方未启用） | NO（配方无后处理步骤） | `WS:218–293`、`WS:362–367`，E002/E004；新增的是优化 flags、ThinLTO 与链接配置，不是 PGO/BOLT |

安装包提供了明确的源码版本关联，不是仅按文件名猜测（E016）：

```text
clang 22.1.8-1.6 armv7l
VCS=platform/upstream/llvm#8dfebafe1a477b3dcc678ee4cb18a3a4306d5a7c
SOURCE=llvm-22.1.8-1.6.src.rpm
llvm 22.1.8-1.6 armv7l
VCS=platform/upstream/llvm#8dfebafe1a477b3dcc678ee4cb18a3a4306d5a7c
libllvm 22.1.8-1.6 armv7l
VCS=platform/upstream/llvm#8dfebafe1a477b3dcc678ee4cb18a3a4306d5a7c
```

**不能把 MLGO 当成 PGO。** `TS:41–46,188–193,257–272` 引入的是预编译 inliner/regalloc 模型对象；没有调用 LLVM profile 采集/合并流程。Tizen 的 `TM:100–102` 确实定义了 `%do_profiling`、`%cflags_profile_generate`、`%cflags_profile_feedback`，但这些是宏能力；对应 LLVM spec 没有引用它们，当前展开的 `%optflags` 也没有 profile flags（E013、E032）。

**不能把 Chromium 的官方打包脚本当作本次 bundled 二进制的构建证明。** 本次所指的 131,174,064 字节 clang 位于 `C/tizen_src/buildtools/llvm/bin/clang`，其引入提交明确说明是为 Tizen 构建并加速的 LLVM 18；另有 `C/third_party/llvm-build/Release+Asserts/bin/clang`，大小为 98,020,320 字节，属于另一份工具。`tools/clang/scripts/package.py` 会请求 PGO/ThinLTO/BOLT，但尚无证据把该脚本的某次执行与前一份二进制关联（E009、E015、E024、E030；`U:42–56`）。因此本任务不能确认“PGO/BOLT 从零开始”这一优化前提。

## 2. Tizen LLVM 完整 CMake 配置

### 2.1 实际路径、版本与条件分支

- 工作区源码：`W/llvm`，当前提交 `f111162e94aa48ed367c9d2c039456c70e7160ae`；工作区已有改动提交不能等同于安装包配方（E003、E029）。
- 安装包配方：从同一 Git 对象库中的 `8dfebafe1a477b3dcc678ee4cb18a3a4306d5a7c:packaging/llvm.spec` 导出到 `TS`；SHA256 为 `7962d176484920de6138d70c7e8a8e1764dfada6655abf0332e9748167e889fd`（E020）。不需要另猜 `RS-RANO/llvm-22` 路径。
- 已枚举 41 个现存 GBS 实例，完整列表见 E006 和 `A/roots.json`；选取的 `R` 含用户前提中 75,956 字节的 clang。工作区 `gbs_llvm.conf:3` 指向的 `temp/GBS-ROOT-TIZEN-UNIFIED-LLVM-CODES` 尚不存在，未初始化它（E001、E006、E009）。
- 所选 ARM 包已安装的 `R/usr/lib/cmake/llvm/LLVMConfig.cmake:20,30,36,171,180` 分别记录 `MinSizeRel`、`LLVM_LINK_LLVM_DYLIB=ON`、`ARM;BPF`、断言关闭、RTTI 开启；工具查询与之吻合（E018、E020）。
- 同一实例另有 accel x86_64 工具：其 `llvm-config --build-mode` 为 `Release`，targets 为 `X86 ARM AArch64 BPF`，host 为 `x86_64-tizen-linux-gnu`（E027）。ARM 配置不能用来代替 accel 配置。

| 条件 | 所有分支 | 已安装包实际情况 / 证据 |
| --- | --- | --- |
| `%{defined _toolchain}` | 真：`llvm_release_build=0`、覆盖 clang，传 lld 和两项 DYLIB link=ON；假：`llvm_release_build=1`，不传这些参数 | ARM 导出配置和 NEEDED 确认链接共享库；由 TS 的分支结构判断与真分支一致。当前 AM:65 也定义 clang，但原发布任务的全部宏仍 UNKNOWN。`TS:11–16,209–240`，E018/E020/E023 |
| `%ifarch x86_64 i686` | Release；X86/ARM/AArch64/BPF | 不适用于 ARM RPM；accel 的查询与该目标集合一致，原始构建入口 UNKNOWN。`TS:216–219`，E027 |
| `%ifarch armv7l` | MinSizeRel；ARM/BPF；target arch ARM；QEMU_RESERVED_VA=0x100000000 | 当前 ARM RPM 已由查询和导出配置确认。`TS:184–186,220–224`，E018/E020 |
| `%ifarch aarch64` | Release；AArch64/BPF；target arch AArch64 | 此次不把其他实例的发布分支代入。`TS:225–229` |
| `%ifarch riscv64` | Release；RISCV/BPF | 当前实例非该架构。`TS:230–233` |
| `%{with mlgo}` 与架构 | armv7l/aarch64/x86_64 默认 `%bcond_without mlgo`；with 且命中架构时使用 AOT 对象；其余分支两个模型路径设 none | 当前 AM:47 为 `_with_mlgo=1`，但原发布构建是否覆盖宏 UNKNOWN。`TS:7–9,155–168,257–273` |
| `mlgo_verify_configure_only` | 默认 0；非零分支检查模型、会构建 `tf_xla_runtime`、安装探针并 `exit 86` | 发布 RPM 存在与普通成功打包路径一致，原任务宏需日志确认。未执行此所谓 configure-only 分支。`TS:49,276–341` |
| `llvm_release_build` | 真时去掉输入 flags 的调试信息并覆盖 debuginfo post；假时保留输入 flags | 此名字不等同于 `CMAKE_BUILD_TYPE=Release`。`TS:24–30,170–179` |
| `%{?asan:...}` | 定义 asan 时展开 `%gcc_unforce_options`；否则不展开 | 原发布任务是否定义 asan UNKNOWN。`TS:182` |

### 2.2 安装包对应 spec：逐项完整参数

下面逐行记录 `TS:198–274` 内所有 `-D` 参数；条件原样保留。宏和环境变量未取得原发布展开值时，不伪造具体值。生成器是 `Ninja`（TS:199），source directory 是 `../llvm`（TS:274）。

| 参数 | 原始值 | 条件 | 出处 |
| --- | --- | --- | --- |
| `TIZEN` | `1` | 无条件 | `TS:200` |
| `CMAKE_C_COMPILER` | `%__cc` | 无条件 | `TS:201` |
| `CMAKE_CXX_COMPILER` | `%__cxx` | 无条件 | `TS:202` |
| `LLVM_HOST_TRIPLE` | `%{_host}` | 无条件 | `TS:203` |
| `LLVM_DEFAULT_TARGET_TRIPLE` | `%{_host}` | 无条件 | `TS:204` |
| `LLVM_TARGET_TRIPLE_ENV` | `%{_host}` | 无条件 | `TS:205` |
| `CMAKE_ASM_FLAGS` | `"$CFLAGS"` | 无条件 | `TS:206` |
| `CMAKE_C_FLAGS` | `"$CFLAGS"` | 无条件 | `TS:207` |
| `CMAKE_CXX_FLAGS` | `"$CXXFLAGS"` | 无条件 | `TS:208` |
| `CMAKE_SHARED_LINKER_FLAGS` | `"-fuse-ld=lld -ffunction-sections -fdata-sections -Wl,--gc-sections"` | %if %{defined _toolchain} | `TS:210` |
| `CMAKE_EXE_LINKER_FLAGS` | `"-fuse-ld=lld -ffunction-sections -fdata-sections -Wl,--gc-sections"` | %if %{defined _toolchain} | `TS:211` |
| `LLVM_USE_LINKER` | `lld` | %if %{defined _toolchain} | `TS:212` |
| `LLVM_ENABLE_ASSERTIONS` | `No` | 无条件 | `TS:214` |
| `LLVM_ENABLE_RTTI` | `ON` | 无条件 | `TS:215` |
| `CMAKE_BUILD_TYPE` | `Release` | %ifarch x86_64 i686 | `TS:217` |
| `LLVM_TARGETS_TO_BUILD` | `'X86;ARM;AArch64;BPF'` | %ifarch x86_64 i686 | `TS:218` |
| `CMAKE_BUILD_TYPE` | `MinSizeRel` | %ifarch armv7l | `TS:221` |
| `LLVM_TARGETS_TO_BUILD` | `'ARM;BPF'` | %ifarch armv7l | `TS:222` |
| `LLVM_TARGET_ARCH` | `"ARM"` | %ifarch armv7l | `TS:223` |
| `CMAKE_BUILD_TYPE` | `Release` | %ifarch aarch64 | `TS:226` |
| `LLVM_TARGETS_TO_BUILD` | `'AArch64;BPF'` | %ifarch aarch64 | `TS:227` |
| `LLVM_TARGET_ARCH` | `"AArch64"` | %ifarch aarch64 | `TS:228` |
| `CMAKE_BUILD_TYPE` | `Release` | %ifarch riscv64 | `TS:231` |
| `LLVM_TARGETS_TO_BUILD` | `'RISCV;BPF'` | %ifarch riscv64 | `TS:232` |
| `CLANG_ENABLE_ARCMT` | `OFF` | 无条件 | `TS:234` |
| `LLVM_BUILD_LLVM_DYLIB` | `ON` | 无条件 | `TS:235` |
| `CLANG_BUILD_CLANG_DYLIB` | `ON` | 无条件 | `TS:236` |
| `LLVM_LINK_LLVM_DYLIB` | `ON` | %if %{defined _toolchain} | `TS:238` |
| `CLANG_LINK_CLANG_DYLIB` | `ON` | %if %{defined _toolchain} | `TS:239` |
| `LLVM_ENABLE_PROJECTS` | `"clang;lldb;clang-tools-extra;lld;compiler-rt;openmp"` | 无条件 | `TS:241` |
| `LLVM_ENABLE_PER_TARGET_RUNTIME_DIR` | `OFF` | 无条件 | `TS:242` |
| `LLVM_BUILD_EXAMPLES` | `OFF` | 无条件 | `TS:243` |
| `LLVM_INCLUDE_EXAMPLES` | `OFF` | 无条件 | `TS:244` |
| `LLVM_BUILD_TESTS` | `OFF` | 无条件 | `TS:245` |
| `LLVM_INCLUDE_TESTS` | `OFF` | 无条件 | `TS:246` |
| `LLVM_ENABLE_DOXYGEN` | `OFF` | 无条件 | `TS:247` |
| `LLVM_BUILD_DOCS` | `OFF` | 无条件 | `TS:248` |
| `LLVM_INCLUDE_DOCS` | `OFF` | 无条件 | `TS:249` |
| `LLVM_OPTIMIZED_TABLEGEN` | `ON` | 无条件 | `TS:250` |
| `CMAKE_INSTALL_PREFIX` | `%{_prefix}` | 无条件 | `TS:251` |
| `LLVM_LIBDIR_SUFFIX` | ``echo %{_lib} \| sed s/lib//g`` | 无条件 | `TS:252` |
| `CLANG_RESOURCE_DIR` | `"../%{_lib}/clang/%{llvm_version}"` | 无条件 | `TS:253` |
| `LLVM_BINUTILS_INCDIR` | `/usr/include` | 无条件 | `TS:254` |
| `LLVM_PARALLEL_COMPILE_JOBS` | `6` | 无条件 | `TS:255` |
| `LLVM_PARALLEL_LINK_JOBS` | `2` | 无条件 | `TS:256` |
| `TENSORFLOW_AOT_PATH` | `"${MLGO_AOT_DIR}/mlgo_sysroot"` | %if %{with mlgo} 且 %ifarch armv7l aarch64 x86_64 | `TS:259` |
| `LLVM_MLGO_EXPORT_TF_XLA_RUNTIME` | `OFF` | %if %{with mlgo} 且 %ifarch armv7l aarch64 x86_64 | `TS:260` |
| `LLVM_MLGO_EMBED_TF_XLA_RUNTIME_OBJECTS` | `"${MLGO_RUNTIME_OBJECTS}"` | %if %{with mlgo} 且 %ifarch armv7l aarch64 x86_64 | `TS:261` |
| `LLVM_OVERRIDE_MODEL_HEADER_INLINERSIZEMODEL` | `"${MLGO_AOT_DIR}/InlinerSizeModel.h"` | %if %{with mlgo} 且 %ifarch armv7l aarch64 x86_64 | `TS:262` |
| `LLVM_OVERRIDE_MODEL_OBJECT_INLINERSIZEMODEL` | `"${MLGO_AOT_DIR}/InlinerSizeModel.o"` | %if %{with mlgo} 且 %ifarch armv7l aarch64 x86_64 | `TS:263` |
| `LLVM_OVERRIDE_MODEL_HEADER_REGALLOCEVICTMODEL` | `"${MLGO_AOT_DIR}/RegAllocEvictModel.h"` | %if %{with mlgo} 且 %ifarch armv7l aarch64 x86_64 | `TS:264` |
| `LLVM_OVERRIDE_MODEL_OBJECT_REGALLOCEVICTMODEL` | `"${MLGO_AOT_DIR}/RegAllocEvictModel.o"` | %if %{with mlgo} 且 %ifarch armv7l aarch64 x86_64 | `TS:265` |
| `LLVM_INLINER_MODEL_PATH` | `none` | %if %{with mlgo} 且 ELSE(%ifarch armv7l aarch64 x86_64) | `TS:267` |
| `LLVM_RAEVICT_MODEL_PATH` | `none` | %if %{with mlgo} 且 ELSE(%ifarch armv7l aarch64 x86_64) | `TS:268` |
| `LLVM_INLINER_MODEL_PATH` | `none` | ELSE(%if %{with mlgo}) | `TS:271` |
| `LLVM_RAEVICT_MODEL_PATH` | `none` | ELSE(%if %{with mlgo}) | `TS:272` |

另有安装期 `cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}/usr -P cmake_install.cmake`（TS:348），它只指定打包安装目标，不是第二阶段编译器构建。

| spec 未显式传入的重点项 | 能证明的配置 / 不能证明的发布事实 | 证据 |
| --- | --- | --- |
| `LLVM_BUILD_INSTRUMENTED` | 所绑定源码默认 OFF；发布 cache UNKNOWN | `S/llvm/cmake/modules/HandleLLVMOptions.cmake:1181` |
| `LLVM_PROFDATA_FILE` / `LLVM_SPROFDATA_FILE` | 对应源码默认空；spec 无赋值；发布 cache UNKNOWN | `S/llvm/CMakeLists.txt:1000,1003`；`S/llvm/cmake/modules/HandleLLVMOptions.cmake:1262–1291`；E029/E033 |
| `LLVM_ENABLE_BOLT` / BOLT post-link | spec 没有变量、训练输入、`llvm-bolt`、`perf2bolt` 或合并步骤；发布任务外部步骤 UNKNOWN | TS 全文，E020/E032 |
| `LLVM_ENABLE_LTO` | 此 spec 未设；对应源码默认 OFF；发布二进制是否受外部 flags 影响 UNKNOWN | `S/llvm/cmake/modules/HandleLLVMOptions.cmake:32`；E020/E029 |
| `LLVM_ENABLE_RUNTIMES` | 未设；对应源码初始默认空；compiler-rt/openmp 已通过 PROJECTS 列出 | `S/llvm/CMakeLists.txt:141`；TS:241 |
| `CMAKE_C_FLAGS_RELEASE` / `CMAKE_CXX_FLAGS_RELEASE` | 未设；未取得原发布 CMake 版本、cache 和最终编译命令，优化级别 UNKNOWN | TS:198–274；E017/E020 的 cache 搜索 |
| `CMAKE_C_FLAGS_MINSIZEREL` / `CMAKE_CXX_FLAGS_MINSIZEREL` | 同样未设；不能仅按名字补填 `-Os`。当前构建根 RPM optflags 是 `-Os ...`，这是另一层已观测输入 | TS:206–208,221；E013；AM:56 |
| Bootstrap | 配方只有一个普通 LLVM configure/build；`CLANG_ENABLE_BOOTSTRAP` 默认 OFF。安装期 `cmake -P`、MLGO 探针、优化 TableGen 不算两阶段 clang | `S/clang/CMakeLists.txt:68`；TS:198,329,344,348；E032 |

`CFLAGS/CXXFLAGS` 来自构建环境，当前 AM:56 和 E013 的宏展开含 `-Os -fstack-protector ... -g2 -gdwarf-4 ...`。这不是原发布包全部编译命令的替代证据；`llvm-config --cxxflags` 是供 LLVM 消费方编译使用的 flags，也不能当作 LLVM 自身的历史构建 flags（E018）。

### 2.3 工作区当前 spec 的差异（全部增删参数）

E029 的完整 diff 显示，除下表列出的变动外，安装包 spec 与工作区 spec 的 CMake 参数一致；行号按 WS 为准。

| 变动 | 当前内容 | 出处 |
| --- | --- | --- |
| 环境 flags 处理 | 用 sed 删除若干优化/栈保护/frame-pointer 字符串，追加 `-O3 -flto=thin -fomit-frame-pointer` | WS:188–206 |
| Shared / EXE linker flags | 原 lld/section flags 增加 `-flto=thin`，仍仅在 `_toolchain` 定义分支传入 | WS:229–236 |
| 新 CMake 参数 | `LLVM_ENABLE_LTO=Thin`、`CMAKE_RANLIB=%{_bindir}/llvm-ranlib`、`CMAKE_AR=%{_bindir}/llvm-ar` | WS:233–235 |
| 删除 CMake 参数 | 不再显式传 `LLVM_LINK_LLVM_DYLIB=ON`、`CLANG_LINK_CLANG_DYLIB=ON` | E029 diff；原 TS:237–240；现 WS:258–260 |
| 仍构建共享库 | `LLVM_BUILD_LLVM_DYLIB=ON`、`CLANG_BUILD_CLANG_DYLIB=ON` 保留；“构建库”和“工具链接该库”是两项不同配置 | WS:258–259；`S/llvm/CMakeLists.txt:912–919` |
| 未改变的架构选择 | ARM 仍是 MinSizeRel，x86/aarch64/riscv 仍是 Release | WS:239–256 |

当前源码 `LLVM_LINK_LLVM_DYLIB` 默认 OFF，`CLANG_LINK_CLANG_DYLIB` 默认继承它（`W/llvm/llvm/CMakeLists.txt:912`、`W/llvm/clang/CMakeLists.txt:309`）。但没有构建或生成 cache，不能把上述改动宣称为已生效的工具链，更不能仅凭 `CFLAGS` 中追加 `-O3` 推断最终命令最后一个优化选项。

## 3. Chromium bundled LLVM 完整配置及能力边界

### 3.1 两套 bundled 工具的身份

实际用于本题比较的工具是 `C/tizen_src/buildtools/llvm/bin/clang`，GN 默认路径由 `C/tizen_src/build/config/tizen_features.gni:31` 指定。其引入提交 `83f4935fbcbeae0ed2c8a11e0f74b2c9d84c4128` 的原文说明：

```text
[Clang] Updated to Clang 18

Open source llvm 18.0 is built and accelerated for tizen to generate clang,
lld and llvm binaries that are required for clang build for standard profile.
```

同一提交记录 clang 从 99,646,400 变为 131,174,064 字节；实际查询为 `clang version 18.1.0rc`、默认 target `x86_64-tizen-linux-gnu`（E024/E030）。这些是这份 bundled 的身份依据，**不证明其 PGO/BOLT/ThinLTO/Bootstrap 选项**。

另一个目录 `C/third_party/llvm-build/Release+Asserts` 的 stamp 为 `llvmorg-18-init-9505-g10664813-1`，与 `U:42–56` 的更新目标相符（E012）。`B` 与 `P` 的输出目标是这一系列 `third_party/llvm-*` 目录；没有找到生产 Tizen `tizen_src/buildtools/llvm` 二进制的 CMakeCache、构建日志或发布清单（E028）。下面完整提取的是**现存 Chromium 构建脚本能力/打包入口配置**；对本题实际 bundled 的未证实项保持 UNKNOWN。

### 3.2 基础参数与最终覆盖

所有平台公共基础参数在 B:819–846；Linux/非 Darwin 补充及外部依赖在 B:848–939。动态路径保留符号，不运行脚本求值，以避免下载、configure 或构建副作用。

| 参数 | 脚本值 / 条件 | 出处 |
| --- | --- | --- |
| CMAKE_BUILD_TYPE | Release | B:821 |
| LLVM_ENABLE_ASSERTIONS | --disable-asserts 时 OFF，否则 ON；bootstrap 强制 ON | B:822,972 |
| LLVM_ENABLE_PROJECTS | clang;lld;clang-tools-extra；--bolt 追加 bolt | B:811–814,823 |
| LLVM_ENABLE_RUNTIMES | compiler-rt；bootstrap 可覆盖 | B:824,964 |
| LLVM_TARGETS_TO_BUILD | AArch64;ARM;LoongArch;Mips;PowerPC;RISCV;SystemZ;WebAssembly;X86 | B:811,825 |
| LLVM_ENABLE_PIC | --pic 或 Windows 时 ON，否则 OFF | B:816–817,826 |
| LLVM_ENABLE_TERMINFO | OFF | B:827 |
| LLVM_ENABLE_Z3_SOLVER | OFF | B:828 |
| CLANG_PLUGIN_SUPPORT | OFF | B:829 |
| CLANG_ENABLE_STATIC_ANALYZER | OFF | B:830 |
| CLANG_ENABLE_ARCMT | OFF | B:831 |
| BUG_REPORT_URL | BUG_REPORT_URL 变量 | B:832 |
| LLVM_ENABLE_DIA_SDK | OFF | B:834 |
| LLVM_ENABLE_LLD | ON | B:838 |
| LLVM_ENABLE_PER_TARGET_RUNTIME_DIR | 基础 OFF；Linux 最终 ON | B:840,1166 |
| LLVM_ENABLE_CURL | OFF | B:842 |
| LIBCLANG_BUILD_STATIC | ON（libclang.a，不能据此证明 clang 静态链接 LLVM） | B:844 |
| LLVM_ENABLE_ZSTD | with_zstd 决定；启用时附带静态 zstd 路径 | B:845,934–939 |
| LLVM_ENABLE_UNWIND_TABLES | 非 Darwin 为 OFF | B:852 |
| LLVM_STATIC_LINK_CXX_STDLIB | Linux 且使用 pinned clang 分支 ON | B:871–892 |
| CMAKE_SYSROOT | Linux aarch64 使用 sysroot_arm64，其余 sysroot_amd64 | B:894–905 |
| LLVM_ENABLE_LIBXML2 | FORCE_ON | B:390 |
| LIBXML2_INCLUDE_DIR / LIBXML2_LIBRARIES / LIBXML2_LIBRARY | 构建的 libxml2 include 路径及 libxml2.a（Windows 为 .lib） | B:385–393 |
| CLANG_ENABLE_LIBXML2 | NO | B:398 |
| LLVM_USE_STATIC_ZSTD / zstd_INCLUDE_DIR / zstd_LIBRARY | ON、构建目录 include/libzstd.a；with_zstd 分支 | B:463–470 |
| CMAKE_C_COMPILER / CMAKE_CXX_COMPILER | host 参数或 pinned clang；bootstrap 后改为 bootstrap-install/bin/clang{,++} | B:871–889,1009–1011,1114–1115 |
| CMAKE_C_FLAGS / CMAKE_CXX_FLAGS | 拼接 cflags/cxxflags：SANITIZER_OVERRIDE_INTERCEPTORS、sanitizers include、LIBXML_STATIC 等 | B:854–861,929–932,1119–1120 |
| CMAKE_EXE_LINKER_FLAGS / CMAKE_SHARED_LINKER_FLAGS / CMAKE_MODULE_LINKER_FLAGS | ldflags；--bolt 时增加 -Wl,--emit-relocs -Wl,-znow | B:1105–1108,1121–1123 |
| CMAKE_INSTALL_PREFIX | --install-dir 或 LLVM_BUILD_DIR | B:1117,1124 |
| LLVM_EXTERNAL_PROJECTS / LLVM_EXTERNAL_CHROMETOOLS_SOURCE_DIR / CHROMIUM_TOOLS | 未指定 --no-tools 时 chrometools、C/tools/clang、plugins/blink_gc_plugin/translation_unit 与 extra-tools | B:1110–1113,1126–1132 |
| LLVM_PROFDATA_FILE | --pgo 时 LLVM_INSTRUMENTED_DIR/profdata.prof | B:55,1133–1134 |
| LLVM_ENABLE_LTO | --thinlto 时 Thin；用于编译最终 LLVM 工具自身 | B:1135–1136 |
| LLVM_DEFAULT_TARGET_TRIPLE | Linux aarch64/riscv64/loongarch64 各自 triple；其余 x86_64-unknown-linux-gnu；Darwin/Windows 另分支 | B:1146–1168 |
| LLVM_INLINER_MODEL_PATH / TENSORFLOW_AOT_PATH / LLVM_RAEVICT_MODEL_PATH | with-ml-inliner-model 分支：模型路径、TF 路径、none；Linux 参数默认 default | B:686–691,1364–1386 |
| LLVM_BUILTIN_TARGETS / LLVM_RUNTIME_TARGETS | 排序后的 runtime triples 分号串 | B:1392–1413 |
| CMAKE_C_COMPILER_LAUNCHER / CMAKE_CXX_COMPILER_LAUNCHER | with-goma 时设置；bootstrap 使用，未 bootstrap 的 final 使用 | B:863–869,961,1415–1418 |

`LLVM_LINK_LLVM_DYLIB`、`LLVM_BUILD_LLVM_DYLIB`、`CLANG_LINK_CLANG_DYLIB`、`LLVM_OPTIMIZED_TABLEGEN`、`CMAKE_{C,CXX}_FLAGS_RELEASE`、`LLVM_ENABLE_RTTI` 未在该脚本中显式赋值。它们的**这份实际 bundled 构建值 UNKNOWN**；不从 LLVM 22 的源码默认值反推 LLVM 18 发布物。脚本使用 `LLVM_ENABLE_LLD=ON`，而不是显式 `LLVM_USE_LINKER=lld`（B:838）。生成器为 Ninja（B:820）。Windows/macOS 专用变量、依赖库构建和 runtime triples 的完整条件源码见本节末的展开清单。

### 3.3 PGO、BOLT、ThinLTO 与 bootstrap 的完整流程

**入口能力与打包配方：** B:643–659 定义 `--bootstrap/--pgo/--thinlto/--bolt`；B:724–726 要求 PGO/ThinLTO 配合 bootstrap。P:243–253 总是给出 `--bootstrap --disable-asserts --run-tests --pgo`，非 Darwin 加 `--thinlto`，Linux 再加 `--bolt`。这些是入口源码证据，不是本题 bundled 的执行证明。

1. **Bootstrap。** B:941–1013 用 host/pinned clang 构建 `clang;lld`；targets 在 Linux 为 X86，assertions 强制 ON，PGO 时构建 compiler-rt profile runtime，然后 install，后续编译器切换到 `llvm-bootstrap-install/bin/clang{,++}`。最终发布编译器的 assertions 仍由 disable-asserts 决定。
2. **PGO 插桩。** B:1015–1039 以 bootstrap 编译器配置 `LLVM_ENABLE_PROJECTS=clang`、`LLVM_BUILD_INSTRUMENTED=IR`，构建 instrumented clang。此阶段在 bootstrap 之外，因此启用 PGO 的流水线不只是两次构建，而是 bootstrap、instrumented、final 三个编译器构建阶段。
3. **PGO 训练输入。** B:1044–1046、1064–1069 指定 `pgo_training-1.ii`，源码注释标明来自 Blink `third_party/blink/renderer/core/layout/layout_object.cc` 的预处理结果；从 `CDS_URL + '/pgo_training-1.ii'` 下载。CDS_URL 默认 `https://commondatastorage.googleapis.com/chromium-browser-clang`，允许环境变量覆盖（U:49–50）。训练命令是 instrumented `clang++ -target x86_64-unknown-unknown -O2 -g -std=c++14 -fno-exceptions -fno-rtti -w -c pgo_training-1.ii`（B:1067–1072）。本任务没有执行该命令。
4. **PGO 合并与使用。** B:1074–1079 用 bootstrap `llvm-profdata merge` 合并 instrumented `profiles/*.profraw` 到 `third_party/llvm-instrumented/profdata.prof`（B:54–55）；B:1133–1134 把它传入最终 LLVM CMake。不是下载一个已成品的 `.profdata`。该 profile 训练入口只编译一个 C++ translation unit，没有独立运行 lld/ar 训练负载（B:1067–1079）。最终 LLVM 构建整体收到 profile，不能把收益范围写成只有 clang，也不能承诺 lld/ar 得到足够训练覆盖。
5. **ThinLTO。** B:1135–1136 在 final compiler 的 CMake 参数中加入 `LLVM_ENABLE_LTO=Thin`，所以脚本确实支持用 ThinLTO 构建 clang/LLVM 工具自身；Chromium GN 的 `use_thin_lto=true`（C/tizen_src/build/gn_chromiumefl.sh:222）是构建 Chromium 产物的另一层设置，不能混为一谈。实际 bundled 自身是否用了 ThinLTO 仍 UNKNOWN。
6. **BOLT。** B:1105–1108 在 final link 保留 relocations 并设置 `-znow`；B:1433–1448 在 final build 完成后，以 `bin/clang` 为输入运行 `bin/llvm-bolt -instrument --instrumentation-file-append-pid`，产生 instrumented clang 及 `prof.fdata`。B:1451–1474 让它仅编译 `tools/clang/lib/Sema/CMakeFiles/obj.clangSema.dir/Sema.cpp.o` 作为训练负载。B:1477–1488 用 `perf-helper.py merge-fdata bin/merge-fdata` 合并 fdata，再执行 `-reorder-blocks=ext-tsp -reorder-functions=hfsort+ -split-functions -split-all-cold -split-eh -dyno-stats -icf=1 -use-gnu-stack -use-old-text`。B:1491–1493 用优化结果替换 `bin/clang`。该脚本 BOLT 步骤**只处理 clang 二进制**，没有对 lld、llvm-ar 或 libLLVM 执行相同 BOLT 步骤。

### 3.4 所有条件参数的源码展开索引

为避免只列“重点参数”而遗漏 runtime/平台条件，以下保留完整的 CMake 参数生成区间。这里是**只读源码摘录**，不是本次执行日志；其中的 `RunCommand` 没有被运行。其他 libxml2/zstd 自身的完整构建参数已在 E008 全文保存，其向 LLVM 返回的参数包含在下面。

<details>
<summary>libxml2 传入 LLVM 的参数（B:385–402）</summary>

```text
385:   if sys.platform == 'win32':
386:     libxml2_lib = os.path.join(dirs.lib_dir, 'libxml2s.lib')
387:   else:
388:     libxml2_lib = os.path.join(dirs.lib_dir, 'libxml2.a')
389:   extra_cmake_flags = [
390:       '-DLLVM_ENABLE_LIBXML2=FORCE_ON',
391:       '-DLIBXML2_INCLUDE_DIR=' + dirs.include_dir.replace('\\', '/'),
392:       '-DLIBXML2_LIBRARIES=' + libxml2_lib.replace('\\', '/'),
393:       '-DLIBXML2_LIBRARY=' + libxml2_lib.replace('\\', '/'),
394:
395:       # This hermetic libxml2 has enough features enabled for lld-link, but not
396:       # for the libxml2 usage in libclang. We don't need libxml2 support in
397:       # libclang, so just turn that off.
398:       '-DCLANG_ENABLE_LIBXML2=NO',
399:   ]
400:   extra_cflags = ['-DLIBXML_STATIC']
401:
402:   return extra_cmake_flags, extra_cflags
```

</details>

<details>
<summary>zstd 传入 LLVM 的参数（B:463–474）</summary>

```text
463:     zstd_lib = os.path.join(dirs.lib_dir, 'zstd_static.lib')
464:   else:
465:     zstd_lib = os.path.join(dirs.lib_dir, 'libzstd.a')
466:   extra_cmake_flags = [
467:       '-DLLVM_ENABLE_ZSTD=ON',
468:       '-DLLVM_USE_STATIC_ZSTD=ON',
469:       '-Dzstd_INCLUDE_DIR=' + dirs.include_dir.replace('\\', '/'),
470:       '-Dzstd_LIBRARY=' + zstd_lib.replace('\\', '/'),
471:   ]
472:   extra_cflags = []
473:
474:   return extra_cmake_flags, extra_cflags
```

</details>

<details>
<summary>compiler-rt 参数生成器（B:610–629）</summary>

```text
610: def compiler_rt_cmake_flags(*, sanitizers, profile):
611:   # Don't set -DCOMPILER_RT_BUILD_BUILTINS=ON/OFF as it interferes with the
612:   # runtimes logic of building builtins.
613:   args = [
614:       # Build crtbegin/crtend. It's just two tiny TUs, so just enable this
615:       # everywhere, even though we only need it on Linux.
616:       'COMPILER_RT_BUILD_CRT=ON',
617:       'COMPILER_RT_BUILD_LIBFUZZER=OFF',
618:       'COMPILER_RT_BUILD_MEMPROF=OFF',
619:       'COMPILER_RT_BUILD_ORC=OFF',
620:       'COMPILER_RT_BUILD_PROFILE=' + ('ON' if profile else 'OFF'),
621:       'COMPILER_RT_BUILD_SANITIZERS=' + ('ON' if sanitizers else 'OFF'),
622:       'COMPILER_RT_BUILD_XRAY=OFF',
623:       # See crbug.com/1205046: don't build scudo (and others we don't need).
624:       'COMPILER_RT_SANITIZERS_TO_BUILD=asan;dfsan;msan;hwasan;tsan;cfi',
625:       # We explicitly list all targets we want to build, do not autodetect
626:       # targets.
627:       'COMPILER_RT_DEFAULT_TARGET_ONLY=ON',
628:   ]
629:   return args
```

</details>

<details>
<summary>基础参数及平台条件（B:811–939）</summary>

```text
811:   targets = 'AArch64;ARM;LoongArch;Mips;PowerPC;RISCV;SystemZ;WebAssembly;X86'
812:   projects = 'clang;lld;clang-tools-extra'
813:   if args.bolt:
814:     projects += ';bolt'
815:
816:   pic_default = sys.platform == 'win32'
817:   pic_mode = 'ON' if args.pic or pic_default else 'OFF'
818:
819:   base_cmake_args = [
820:       '-GNinja',
821:       '-DCMAKE_BUILD_TYPE=Release',
822:       '-DLLVM_ENABLE_ASSERTIONS=%s' % ('OFF' if args.disable_asserts else 'ON'),
823:       '-DLLVM_ENABLE_PROJECTS=' + projects,
824:       '-DLLVM_ENABLE_RUNTIMES=compiler-rt',
825:       '-DLLVM_TARGETS_TO_BUILD=' + targets,
826:       f'-DLLVM_ENABLE_PIC={pic_mode}',
827:       '-DLLVM_ENABLE_TERMINFO=OFF',
828:       '-DLLVM_ENABLE_Z3_SOLVER=OFF',
829:       '-DCLANG_PLUGIN_SUPPORT=OFF',
830:       '-DCLANG_ENABLE_STATIC_ANALYZER=OFF',
831:       '-DCLANG_ENABLE_ARCMT=OFF',
832:       '-DBUG_REPORT_URL=' + BUG_REPORT_URL,
833:       # See crbug.com/1126219: Use native symbolizer instead of DIA
834:       '-DLLVM_ENABLE_DIA_SDK=OFF',
835:       # Link all binaries with lld. Effectively passes -fuse-ld=lld to the
836:       # compiler driver. On Windows, cmake calls the linker directly, so there
837:       # the same is achieved by passing -DCMAKE_LINKER=$lld below.
838:       '-DLLVM_ENABLE_LLD=ON',
839:       # The default value differs per platform, force it off everywhere.
840:       '-DLLVM_ENABLE_PER_TARGET_RUNTIME_DIR=OFF',
841:       # Don't use curl.
842:       '-DLLVM_ENABLE_CURL=OFF',
843:       # Build libclang.a as well as libclang.so
844:       '-DLIBCLANG_BUILD_STATIC=ON',
845:       '-DLLVM_ENABLE_ZSTD=%s' % ('ON' if args.with_zstd else 'OFF'),
846:   ]
847:
848:   if sys.platform == 'darwin':
849:     isysroot = subprocess.check_output(['xcrun', '--show-sdk-path'],
850:                                        universal_newlines=True).rstrip()
851:   else:
852:     base_cmake_args += ['-DLLVM_ENABLE_UNWIND_TABLES=OFF']
853:
854:   # See https://crbug.com/1302636#c49 - #c56 -- intercepting crypt_r() does not
855:   # work with the sysroot for not fully understood reasons. Disable it.
856:   sanitizers_override = [
857:     '-DSANITIZER_OVERRIDE_INTERCEPTORS',
858:     '-I' + os.path.join(THIS_DIR, 'sanitizers'),
859:   ]
860:   cflags += sanitizers_override
861:   cxxflags += sanitizers_override
862:
863:   goma_cmake_args = []
864:   goma_ninja_args = []
865:   if args.with_goma:
866:     goma_path = StartGomaAndGetGomaCCPath()
867:     goma_cmake_args.append('-DCMAKE_C_COMPILER_LAUNCHER=' + goma_path)
868:     goma_cmake_args.append('-DCMAKE_CXX_COMPILER_LAUNCHER=' + goma_path)
869:     goma_ninja_args = ['-j' + str(multiprocessing.cpu_count() * 50)]
870:
871:   if args.host_cc or args.host_cxx:
872:     assert args.host_cc and args.host_cxx, \
873:            "--host-cc and --host-cxx need to be used together"
874:     cc = args.host_cc
875:     cxx = args.host_cxx
876:   else:
877:     DownloadPinnedClang()
878:     if sys.platform == 'win32':
879:       cc = os.path.join(PINNED_CLANG_DIR, 'bin', 'clang-cl.exe')
880:       cxx = os.path.join(PINNED_CLANG_DIR, 'bin', 'clang-cl.exe')
881:       lld = os.path.join(PINNED_CLANG_DIR, 'bin', 'lld-link.exe')
882:       # CMake has a hard time with backslashes in compiler paths:
883:       # https://stackoverflow.com/questions/13050827
884:       cc = cc.replace('\\', '/')
885:       cxx = cxx.replace('\\', '/')
886:       lld = lld.replace('\\', '/')
887:     else:
888:       cc = os.path.join(PINNED_CLANG_DIR, 'bin', 'clang')
889:       cxx = os.path.join(PINNED_CLANG_DIR, 'bin', 'clang++')
890:
891:     if sys.platform.startswith('linux'):
892:       base_cmake_args += [ '-DLLVM_STATIC_LINK_CXX_STDLIB=ON' ]
893:
894:   if sys.platform.startswith('linux'):
895:     sysroot_amd64 = DownloadDebianSysroot('amd64')
896:     sysroot_i386 = DownloadDebianSysroot('i386')
897:     sysroot_arm = DownloadDebianSysroot('arm')
898:     sysroot_arm64 = DownloadDebianSysroot('arm64')
899:
900:     # Add the sysroot to base_cmake_args.
901:     if platform.machine() == 'aarch64':
902:       base_cmake_args.append('-DCMAKE_SYSROOT=' + sysroot_arm64)
903:     else:
904:       # amd64 is the default toolchain.
905:       base_cmake_args.append('-DCMAKE_SYSROOT=' + sysroot_amd64)
906:
907:   if sys.platform == 'win32':
908:     AddGnuWinToPath()
909:
910:     base_cmake_args.append('-DCMAKE_MSVC_RUNTIME_LIBRARY=MultiThreaded')
911:
912:     # Require zlib compression.
913:     zlib_dir = AddZlibToPath()
914:     cflags.append('-I' + zlib_dir)
915:     cxxflags.append('-I' + zlib_dir)
916:     ldflags.append('-LIBPATH:' + zlib_dir)
917:
918:     # Use rpmalloc. For faster ThinLTO linking.
919:     rpmalloc_dir = DownloadRPMalloc()
920:     base_cmake_args.append('-DLLVM_INTEGRATED_CRT_ALLOC=' + rpmalloc_dir)
921:
922:     # Set a sysroot to make the build more hermetic.
923:     base_cmake_args.append('-DLLVM_WINSYSROOT="%s"' %
924:                            os.path.dirname(os.path.dirname(GetWinSDKDir())))
925:
926:   # Statically link libxml2 to make lld-link not require mt.exe on Windows,
927:   # and to make sure lld-link output on other platforms is identical to
928:   # lld-link on Windows (for cross-builds).
929:   libxml_cmake_args, libxml_cflags = BuildLibXml2()
930:   base_cmake_args += libxml_cmake_args
931:   cflags += libxml_cflags
932:   cxxflags += libxml_cflags
933:
934:   if args.with_zstd:
935:     # Statically link zstd to make lld support zstd compression for debug info.
936:     zstd_cmake_args, zstd_cflags = BuildZStd()
937:     base_cmake_args += zstd_cmake_args
938:     cflags += zstd_cflags
939:     cxxflags += zstd_cflags
```

</details>

<details>
<summary>bootstrap 参数覆盖（B:948–992）</summary>

```text
948:     runtimes = []
949:     if args.pgo or sys.platform == 'darwin':
950:       # Need libclang_rt.profile for PGO.
951:       # On macOS, the bootstrap toolchain needs to have compiler-rt because
952:       # dsymutil's link needs libclang_rt.osx.a. Only the x86_64 osx
953:       # libraries are needed though, and only libclang_rt (i.e.
954:       # COMPILER_RT_BUILD_BUILTINS).
955:       runtimes.append('compiler-rt')
956:
957:     bootstrap_targets = 'X86'
958:     if sys.platform == 'darwin':
959:       # Need ARM and AArch64 for building the ios clang_rt.
960:       bootstrap_targets += ';ARM;AArch64'
961:     bootstrap_args = base_cmake_args + goma_cmake_args + [
962:         '-DLLVM_TARGETS_TO_BUILD=' + bootstrap_targets,
963:         '-DLLVM_ENABLE_PROJECTS=clang;lld',
964:         '-DLLVM_ENABLE_RUNTIMES=' + ';'.join(runtimes),
965:         '-DCMAKE_INSTALL_PREFIX=' + LLVM_BOOTSTRAP_INSTALL_DIR,
966:         '-DCMAKE_C_FLAGS=' + ' '.join(cflags),
967:         '-DCMAKE_CXX_FLAGS=' + ' '.join(cxxflags),
968:         '-DCMAKE_EXE_LINKER_FLAGS=' + ' '.join(ldflags),
969:         '-DCMAKE_SHARED_LINKER_FLAGS=' + ' '.join(ldflags),
970:         '-DCMAKE_MODULE_LINKER_FLAGS=' + ' '.join(ldflags),
971:         # Ignore args.disable_asserts for the bootstrap compiler.
972:         '-DLLVM_ENABLE_ASSERTIONS=ON',
973:     ]
974:     # PGO needs libclang_rt.profile but none of the other compiler-rt stuff.
975:     bootstrap_args.extend([
976:         '-D' + f
977:         for f in compiler_rt_cmake_flags(sanitizers=False, profile=args.pgo)
978:     ])
979:     if sys.platform == 'darwin':
980:       bootstrap_args.extend([
981:           '-DCOMPILER_RT_ENABLE_IOS=OFF',
982:           '-DCOMPILER_RT_ENABLE_WATCHOS=OFF',
983:           '-DCOMPILER_RT_ENABLE_TVOS=OFF',
984:           ])
985:       if platform.machine() == 'arm64':
986:         bootstrap_args.extend(['-DDARWIN_osx_ARCHS=arm64'])
987:       else:
988:         bootstrap_args.extend(['-DDARWIN_osx_ARCHS=x86_64'])
989:
990:     if cc is not None:  bootstrap_args.append('-DCMAKE_C_COMPILER=' + cc)
991:     if cxx is not None: bootstrap_args.append('-DCMAKE_CXX_COMPILER=' + cxx)
992:     if lld is not None: bootstrap_args.append('-DCMAKE_LINKER=' + lld)
```

</details>

<details>
<summary>instrumented 参数覆盖（B:1022–1035）</summary>

```text
1022:     instrument_args = base_cmake_args + [
1023:         '-DLLVM_ENABLE_PROJECTS=clang',
1024:         '-DCMAKE_C_FLAGS=' + ' '.join(cflags),
1025:         '-DCMAKE_CXX_FLAGS=' + ' '.join(cxxflags),
1026:         '-DCMAKE_EXE_LINKER_FLAGS=' + ' '.join(ldflags),
1027:         '-DCMAKE_SHARED_LINKER_FLAGS=' + ' '.join(ldflags),
1028:         '-DCMAKE_MODULE_LINKER_FLAGS=' + ' '.join(ldflags),
1029:         # Build with instrumentation.
1030:         '-DLLVM_BUILD_INSTRUMENTED=IR',
1031:     ]
1032:     # Build with the bootstrap compiler.
1033:     if cc is not None:  instrument_args.append('-DCMAKE_C_COMPILER=' + cc)
1034:     if cxx is not None: instrument_args.append('-DCMAKE_CXX_COMPILER=' + cxx)
1035:     if lld is not None: instrument_args.append('-DCMAKE_LINKER=' + lld)
```

</details>

<details>
<summary>最终 flags 和 CMake 参数（B:1082–1138）</summary>

```text
1082:   deployment_target = '10.12'
1083:
1084:   # If building at head, define a macro that plugins can use for #ifdefing
1085:   # out code that builds at head, but not at CLANG_REVISION or vice versa.
1086:   if args.llvm_force_head_revision:
1087:     cflags += ['-DLLVM_FORCE_HEAD_REVISION']
1088:     cxxflags += ['-DLLVM_FORCE_HEAD_REVISION']
1089:
1090:   # Build PDBs for archival on Windows.  Don't use RelWithDebInfo since it
1091:   # has different optimization defaults than Release.
1092:   # Also disable stack cookies (/GS-) for performance.
1093:   if sys.platform == 'win32':
1094:     cflags += ['/Zi', '/GS-']
1095:     cxxflags += ['/Zi', '/GS-']
1096:     ldflags += ['/DEBUG', '/OPT:REF', '/OPT:ICF']
1097:
1098:   deployment_env = None
1099:   if deployment_target:
1100:     deployment_env = os.environ.copy()
1101:     deployment_env['MACOSX_DEPLOYMENT_TARGET'] = deployment_target
1102:
1103:   print('Building final compiler.')
1104:
1105:   # Keep static relocations in the executable for BOLT to analyze. Resolve all
1106:   # symbols on program start to allow BOLT's PLT optimization.
1107:   if args.bolt:
1108:     ldflags += ['-Wl,--emit-relocs', '-Wl,-znow']
1109:
1110:   chrome_tools = []
1111:   if not args.no_tools:
1112:     default_tools = ['plugins', 'blink_gc_plugin', 'translation_unit']
1113:     chrome_tools = list(set(default_tools + args.extra_tools))
1114:   if cc is not None:  base_cmake_args.append('-DCMAKE_C_COMPILER=' + cc)
1115:   if cxx is not None: base_cmake_args.append('-DCMAKE_CXX_COMPILER=' + cxx)
1116:   if lld is not None: base_cmake_args.append('-DCMAKE_LINKER=' + lld)
1117:   final_install_dir = args.install_dir if args.install_dir else LLVM_BUILD_DIR
1118:   cmake_args = base_cmake_args + [
1119:       '-DCMAKE_C_FLAGS=' + ' '.join(cflags),
1120:       '-DCMAKE_CXX_FLAGS=' + ' '.join(cxxflags),
1121:       '-DCMAKE_EXE_LINKER_FLAGS=' + ' '.join(ldflags),
1122:       '-DCMAKE_SHARED_LINKER_FLAGS=' + ' '.join(ldflags),
1123:       '-DCMAKE_MODULE_LINKER_FLAGS=' + ' '.join(ldflags),
1124:       '-DCMAKE_INSTALL_PREFIX=' + final_install_dir,
1125:   ]
1126:   if not args.no_tools:
1127:     cmake_args.extend([
1128:         '-DLLVM_EXTERNAL_PROJECTS=chrometools',
1129:         '-DLLVM_EXTERNAL_CHROMETOOLS_SOURCE_DIR=' +
1130:         os.path.join(CHROMIUM_DIR, 'tools', 'clang'),
1131:         '-DCHROMIUM_TOOLS=%s' % ';'.join(chrome_tools)
1132:     ])
1133:   if args.pgo:
1134:     cmake_args.append('-DLLVM_PROFDATA_FILE=' + LLVM_PROFDATA_FILE)
1135:   if args.thinlto:
1136:     cmake_args.append('-DLLVM_ENABLE_LTO=Thin')
1137:   if sys.platform == 'win32':
1138:     cmake_args.append('-DLLVM_ENABLE_ZLIB=FORCE_ON')
```

</details>

<details>
<summary>平台 triples、runtime 参数与 MLGO 生成规则（B:1140–1413）</summary>

```text
1140:   if args.build_mac_arm:
1141:     assert platform.machine() != 'arm64', 'build_mac_arm for cross build only'
1142:     cmake_args += [
1143:         '-DCMAKE_OSX_ARCHITECTURES=arm64', '-DCMAKE_SYSTEM_NAME=Darwin'
1144:     ]
1145:
1146:   # The default LLVM_DEFAULT_TARGET_TRIPLE depends on the host machine.
1147:   # Set it explicitly to make the build of clang more hermetic, and also to
1148:   # set it to arm64 when cross-building clang for mac/arm.
1149:   if sys.platform == 'darwin':
1150:     if args.build_mac_arm or platform.machine() == 'arm64':
1151:       cmake_args.append('-DLLVM_DEFAULT_TARGET_TRIPLE=arm64-apple-darwin')
1152:     else:
1153:       cmake_args.append('-DLLVM_DEFAULT_TARGET_TRIPLE=x86_64-apple-darwin')
1154:   elif sys.platform.startswith('linux'):
1155:     if platform.machine() == 'aarch64':
1156:       cmake_args.append(
1157:           '-DLLVM_DEFAULT_TARGET_TRIPLE=aarch64-unknown-linux-gnu')
1158:     elif platform.machine() == 'riscv64':
1159:       cmake_args.append(
1160:           '-DLLVM_DEFAULT_TARGET_TRIPLE=riscv64-unknown-linux-gnu')
1161:     elif platform.machine() == 'loongarch64':
1162:       cmake_args.append(
1163:           '-DLLVM_DEFAULT_TARGET_TRIPLE=loongarch64-unknown-linux-gnu')
1164:     else:
1165:       cmake_args.append('-DLLVM_DEFAULT_TARGET_TRIPLE=x86_64-unknown-linux-gnu')
1166:     cmake_args.append('-DLLVM_ENABLE_PER_TARGET_RUNTIME_DIR=ON')
1167:   elif sys.platform == 'win32':
1168:     cmake_args.append('-DLLVM_DEFAULT_TARGET_TRIPLE=x86_64-pc-windows-msvc')
1169:
1170:   # Map from triple to {
1171:   #   "args": list of CMake vars without '-D' common to builtins and runtimes
1172:   #   "profile": bool # build profile runtime
1173:   #   "sanitizers": bool # build sanitizer runtimes
1174:   # }
1175:   runtimes_triples_args = {}
1176:
1177:   if sys.platform.startswith('linux'):
1178:     runtimes_triples_args['i386-unknown-linux-gnu'] = {
1179:         "args": [
1180:             'CMAKE_SYSROOT=%s' % sysroot_i386,
1181:             # TODO(https://crbug.com/1374690): pass proper flags to i386 tests so they compile correctly
1182:             'LLVM_INCLUDE_TESTS=OFF',
1183:         ],
1184:         "profile":
1185:         True,
1186:         "sanitizers":
1187:         True,
1188:     }
1189:     runtimes_triples_args['x86_64-unknown-linux-gnu'] = {
1190:         "args": [
1191:             'CMAKE_SYSROOT=%s' % sysroot_amd64,
1192:         ],
1193:         "profile": True,
1194:         "sanitizers": True,
1195:     }
1196:     # Using "armv7a-unknown-linux-gnueabhihf" confuses the compiler-rt
1197:     # builtins build, since compiler-rt/cmake/builtin-config-ix.cmake
1198:     # doesn't include "armv7a" in its `ARM32` list.
1199:     # TODO(thakis): It seems to work for everything else though, see try
1200:     # results on
1201:     # https://chromium-review.googlesource.com/c/chromium/src/+/3702739/4
1202:     # Maybe it should work for builtins too?
1203:     runtimes_triples_args['armv7-unknown-linux-gnueabihf'] = {
1204:         "args": [
1205:             'CMAKE_SYSROOT=%s' % sysroot_arm,
1206:             # Can't run tests on x86 host.
1207:             'LLVM_INCLUDE_TESTS=OFF',
1208:         ],
1209:         "profile":
1210:         True,
1211:         "sanitizers":
1212:         True,
1213:     }
1214:     runtimes_triples_args['aarch64-unknown-linux-gnu'] = {
1215:         "args": [
1216:             'CMAKE_SYSROOT=%s' % sysroot_arm64,
1217:             # Can't run tests on x86 host.
1218:             'LLVM_INCLUDE_TESTS=OFF',
1219:         ],
1220:         "profile":
1221:         True,
1222:         "sanitizers":
1223:         True,
1224:     }
1225:   elif sys.platform == 'win32':
1226:     sysroot = os.path.dirname(os.path.dirname(GetWinSDKDir()))
1227:     runtimes_triples_args['i386-pc-windows-msvc'] = {
1228:         "args": [
1229:             'LLVM_ENABLE_PER_TARGET_RUNTIME_DIR=OFF',
1230:             'LLVM_WINSYSROOT="%s"' % sysroot,
1231:         ],
1232:         "profile":
1233:         True,
1234:         "sanitizers":
1235:         False,
1236:     }
1237:     runtimes_triples_args['x86_64-pc-windows-msvc'] = {
1238:         "args": [
1239:             'LLVM_ENABLE_PER_TARGET_RUNTIME_DIR=OFF',
1240:             'LLVM_WINSYSROOT="%s"' % sysroot,
1241:         ],
1242:         "profile":
1243:         True,
1244:         "sanitizers":
1245:         True,
1246:     }
1247:     runtimes_triples_args['aarch64-pc-windows-msvc'] = {
1248:         "args": [
1249:             'LLVM_ENABLE_PER_TARGET_RUNTIME_DIR=OFF',
1250:             'LLVM_WINSYSROOT="%s"' % sysroot,
1251:             # Can't run tests on x86 host.
1252:             'LLVM_INCLUDE_TESTS=OFF',
1253:         ],
1254:         "profile":
1255:         True,
1256:         "sanitizers":
1257:         False,
1258:     }
1259:   elif sys.platform == 'darwin':
1260:     # compiler-rt is built for all platforms/arches with a single
1261:     # configuration, we should only specify one target triple. 'default' is
1262:     # specially handled.
1263:     runtimes_triples_args['default'] = {
1264:         "args": [
1265:             'SANITIZER_MIN_OSX_VERSION=' + deployment_target,
1266:             'COMPILER_RT_ENABLE_MACCATALYST=ON',
1267:             'COMPILER_RT_ENABLE_IOS=ON',
1268:             'COMPILER_RT_ENABLE_WATCHOS=OFF',
1269:             'COMPILER_RT_ENABLE_TVOS=OFF',
1270:             'DARWIN_ios_ARCHS=arm64',
1271:             'DARWIN_iossim_ARCHS=arm64;x86_64',
1272:             'DARWIN_osx_ARCHS=arm64;x86_64',
1273:         ],
1274:         "sanitizers":
1275:         True,
1276:         "profile":
1277:         True
1278:     }
1279:
1280:   if args.with_android:
1281:     for target_arch in ['aarch64', 'arm', 'i686', 'riscv64', 'x86_64']:
1282:       toolchain_dir = ANDROID_NDK_TOOLCHAIN_DIR
1283:       target_triple = target_arch
1284:       if target_arch == 'arm':
1285:         target_triple = 'armv7'
1286:       api_level = '19'
1287:       if target_arch == 'aarch64' or target_arch == 'x86_64':
1288:         api_level = '21'
1289:       elif target_arch == 'riscv64':
1290:         api_level = '35'
1291:         toolchain_dir = ANDROID_NDK_CANARY_TOOLCHAIN_DIR
1292:       target_triple += '-linux-android' + api_level
1293:       android_cflags = [
1294:           '--sysroot=%s/sysroot' % toolchain_dir,
1295:
1296:           # We don't have an unwinder ready, and don't need it either.
1297:           '--unwindlib=none',
1298:       ]
1299:
1300:       if target_arch == 'aarch64':
1301:         # Use PAC/BTI instructions for AArch64
1302:         android_cflags += ['-mbranch-protection=standard']
1303:
1304:       android_args = [
1305:           'LLVM_ENABLE_RUNTIMES=compiler-rt',
1306:           # On Android, we want DWARF info for the builtins for unwinding. See
1307:           # crbug.com/1311807.
1308:           'CMAKE_BUILD_TYPE=RelWithDebInfo',
1309:           'CMAKE_C_FLAGS=' + ' '.join(android_cflags),
1310:           'CMAKE_CXX_FLAGS=' + ' '.join(android_cflags),
1311:           'CMAKE_ASM_FLAGS=' + ' '.join(android_cflags),
1312:           'COMPILER_RT_USE_BUILTINS_LIBRARY=ON',
1313:           'SANITIZER_CXX_ABI=libcxxabi',
1314:           'CMAKE_SHARED_LINKER_FLAGS=-Wl,-u__cxa_demangle',
1315:           'ANDROID=1',
1316:           'LLVM_ENABLE_PER_TARGET_RUNTIME_DIR=OFF',
1317:           'LLVM_INCLUDE_TESTS=OFF',
1318:           # This prevents static_asserts from firing in 32-bit builds.
1319:           # TODO: remove once we only support API >=24.
1320:           'ANDROID_NATIVE_API_LEVEL=' + api_level,
1321:       ]
1322:       runtimes_triples_args[target_triple] = {
1323:           "args": android_args,
1324:           "sanitizers": True,
1325:           "profile": True
1326:       }
1327:
1328:   if args.with_fuchsia:
1329:     # Fuchsia links against libclang_rt.builtins-<arch>.a instead of libgcc.a.
1330:     for target_arch in ['aarch64', 'x86_64']:
1331:       fuchsia_arch_name = {'aarch64': 'arm64', 'x86_64': 'x64'}[target_arch]
1332:       toolchain_dir = os.path.join(
1333:           FUCHSIA_SDK_DIR, 'arch', fuchsia_arch_name, 'sysroot')
1334:       target_triple = target_arch + '-unknown-fuchsia'
1335:       # Build the Fuchsia profile and asan runtimes.  This is done after the rt
1336:       # builtins have been created because the CMake build runs link checks that
1337:       # require that the builtins already exist to succeed.
1338:       # TODO(thakis): Figure out why this doesn't build with the stage0
1339:       # compiler in arm cross builds.
1340:       build_profile = target_arch == 'x86_64' and not args.build_mac_arm
1341:       # Build the asan runtime only on non-Mac platforms.  Macs are excluded
1342:       # because the asan install changes library RPATHs which CMake only
1343:       # supports on ELF platforms and MacOS uses Mach-O instead of ELF.
1344:       build_sanitizers = build_profile and sys.platform != 'darwin'
1345:       # TODO(thakis): Might have to pass -B here once sysroot contains
1346:       # binaries (e.g. gas for arm64?)
1347:       fuchsia_args = [
1348:           'LLVM_ENABLE_RUNTIMES=compiler-rt',
1349:           'CMAKE_SYSTEM_NAME=Fuchsia',
1350:           'CMAKE_SYSROOT=%s' % toolchain_dir,
1351:           # TODO(thakis|scottmg): Use PER_TARGET_RUNTIME_DIR for all platforms.
1352:           # https://crbug.com/882485.
1353:           'LLVM_ENABLE_PER_TARGET_RUNTIME_DIR=ON',
1354:       ]
1355:       if build_sanitizers:
1356:         fuchsia_args.append('SANITIZER_NO_UNDEFINED_SYMBOLS=OFF')
1357:
1358:       runtimes_triples_args[target_triple] = {
1359:           "args": fuchsia_args,
1360:           "sanitizers": build_sanitizers,
1361:           "profile": build_profile
1362:       }
1363:
1364:   # Embed MLGO inliner model. If tf_path is not specified, a vpython3 env
1365:   # will be created which contains the necessary source files for compilation.
1366:   # MLGO is only officially supported on linux. This condition is checked at
1367:   # the top of main()
1368:   if args.with_ml_inliner_model:
1369:     if args.with_ml_inliner_model == 'default':
1370:       model_path = ('https://commondatastorage.googleapis.com/'
1371:                     'chromium-browser-clang/tools/mlgo_model2.tgz')
1372:     else:
1373:       model_path = args.with_ml_inliner_model
1374:     if not args.tf_path:
1375:       tf_path = subprocess.check_output(
1376:           ['vpython3', os.path.join(THIS_DIR, 'get_tensorflow.py')],
1377:           universal_newlines=True).rstrip()
1378:     else:
1379:       tf_path = args.tf_path
1380:     print('Embedding MLGO inliner model at %s using Tensorflow at %s' %
1381:           (model_path, tf_path))
1382:     cmake_args += [
1383:         '-DLLVM_INLINER_MODEL_PATH=%s' % model_path,
1384:         '-DTENSORFLOW_AOT_PATH=%s' % tf_path,
1385:         # Disable Regalloc model generation since it is unused
1386:         '-DLLVM_RAEVICT_MODEL_PATH=none'
1387:     ]
1388:
1389:   # Convert FOO=BAR CMake flags per triple into
1390:   # -DBUILTINS_$triple_FOO=BAR/-DRUNTIMES_$triple_FOO=BAR and build up
1391:   # -DLLVM_BUILTIN_TARGETS/-DLLVM_RUNTIME_TARGETS.
1392:   all_triples = ''
1393:   for triple in sorted(runtimes_triples_args.keys()):
1394:     all_triples += triple + ';'
1395:     for arg in runtimes_triples_args[triple]["args"]:
1396:       assert not arg.startswith('-')
1397:       # 'default' is specially handled to pass through relevant CMake flags.
1398:       if triple == 'default':
1399:         cmake_args.append('-D' + arg)
1400:       else:
1401:         cmake_args.append('-DRUNTIMES_' + triple + '_' + arg)
1402:         cmake_args.append('-DBUILTINS_' + triple + '_' + arg)
1403:     for arg in compiler_rt_cmake_flags(
1404:         profile=runtimes_triples_args[triple]["profile"],
1405:         sanitizers=runtimes_triples_args[triple]["sanitizers"]):
1406:       # 'default' is specially handled to pass through relevant CMake flags.
1407:       if triple == 'default':
1408:         cmake_args.append('-D' + arg)
1409:       else:
1410:         cmake_args.append('-DRUNTIMES_' + triple + '_' + arg)
1411:
1412:   cmake_args.append('-DLLVM_BUILTIN_TARGETS=' + all_triples)
1413:   cmake_args.append('-DLLVM_RUNTIME_TARGETS=' + all_triples)
```

</details>

<details>
<summary>BOLT 训练阶段 CMake 参数（B:1454–1469）</summary>

```text
1454:     bolt_train_cmake_args = base_cmake_args + [
1455:         '-DLLVM_TARGETS_TO_BUILD=X86',
1456:         '-DLLVM_ENABLE_PROJECTS=clang',
1457:         '-DCMAKE_C_FLAGS=' + ' '.join(cflags),
1458:         '-DCMAKE_CXX_FLAGS=' + ' '.join(cxxflags),
1459:         '-DCMAKE_EXE_LINKER_FLAGS=' + ' '.join(ldflags),
1460:         '-DCMAKE_SHARED_LINKER_FLAGS=' + ' '.join(ldflags),
1461:         '-DCMAKE_MODULE_LINKER_FLAGS=' + ' '.join(ldflags),
1462:         '-DCMAKE_C_COMPILER=' +
1463:         os.path.join(LLVM_BUILD_DIR, 'bin/clang-bolt.inst'),
1464:         '-DCMAKE_CXX_COMPILER=' +
1465:         os.path.join(LLVM_BUILD_DIR, 'bin/clang++-bolt.inst'),
1466:         '-DCMAKE_ASM_COMPILER=' +
1467:         os.path.join(LLVM_BUILD_DIR, 'bin/clang-bolt.inst'),
1468:         '-DCMAKE_ASM_COMPILER_ID=Clang',
1469:     ]
```

</details>

## 4. 工具清单、调用面与共享库依赖

### 4.1 RPM 实际安装清单与统计口径

E019 对同一 RPM 数据库执行 `rpm -qa --qf`，选择 source RPM 为 `llvm-22.1.8-1.6.src.rpm` 的全部已安装子包，再逐包执行 **`rpm -ql`**。没有用 spec `%files` 代替安装清单。包含 `libllvm`、`clang`、`llvm`、`lldb`、`llvm-devel`；同时单列 accel 包。原始 `rpm-ql-*.txt` 全文均在 A 下。可执行工具按文件执行位、bin/libexec 路径或 shebang 识别，排除作为库而非工具安装的 `.so`；符号链接在 **chroot 根内**解析，避免误读宿主同名绝对路径。每个工具均保存 `ls -la`、目标文件大小、`readelf -d` 和 `file -L`（E019；`A/inventory.py`）。脚本的 readelf 失败保留，标 N/A。

统计按已安装路径计数，符号链接别名会重复计入，不能解读为独立 ELF 数；以下为 E031 输出：

```text
libllvm paths 0 ELF 0 direct LLVM shared 0
clang paths 36 ELF 29 direct LLVM shared 29
llvm paths 105 ELF 98 direct LLVM shared 95
lldb paths 5 ELF 5 direct LLVM shared 5
llvm-devel paths 9 ELF 2 direct LLVM shared 2
clang-accel-x86_64-armv7l paths 110 ELF 110 direct LLVM shared 107
```

本次普通 LLVM 子包有 155 个可执行路径，其中 134 个 ELF 路径的 131 个直接依赖 `libLLVM*.so` 或 `libclang-cpp*.so`；accel 有 110 个 ELF 路径的 107 个符合条件（E019/E031）。这证明共有代码位于共享库中，但不能据此断言改成静态链接必然提高吞吐，也不能把 lld 自身的多 MB 代码忽略。ARM 与 x86_64 使用不同架构的库文件（E023）。

### 4.2 重点工具：是否调用、阶段、频度

“规则确认”表示发现了能产生调用的有效规则，不等同于取得全平台执行轨迹。“UNKNOWN”不表示没有调用。频度用每编译单元、每链接目标、每归档、每待处理 ELF 表示；除用户给定 Chromium 量级外，不外推到全部 RPM。

| 工具 | 调用判断 / 阶段 | 频度量级与范围 | 证据 |
| --- | --- | --- | --- |
| clang / clang++（含 triple 别名） | YES：RPM `%build/%install` 导出 CC/CXX；Chromium clang 分支编译和 compiler-driver 链接 | 编译约每 translation unit 一次，另有配置探针、汇编、链接 driver；用户给定样本为约四万个编译任务，不据此推导全部 RPM 总数 | AM:54–55,78–86,121–124；GN:22–32；GT:383–404；LOG13:156–158；E027 的历史 --version execve |
| lld / ld.lld | 条件 YES：Chromium `use_lld` 分支通过 clang driver 的 `-fuse-ld=lld` 调用；任意 RPM 并非自动统一用 lld，当前 `%__ld=/bin/ld` 是 GNU | 每链接目标量级；用户给定 Chromium 为数百个链接目标；具体选中 bundled 还是平台 lld 需对应命令/execve，全平台频度 UNKNOWN | C/tizen_src/build/gn_chromiumefl.sh:218–223；C/build/config/compiler/BUILD.gn:398–402；RM:77；E018；LOG13:330–331 只证明 LINK 阶段 |
| llvm-ar | YES：RPM AR 宏和 Chromium clang 分支；静态归档 | 每归档动作量级；精确总数 UNKNOWN | AM:52,68,75–85；GN:26；GT:410–434；LOG13:153–154 |
| llvm-ranlib | 规则确认：RPM RANLIB 导出；静态归档索引，是否另发进程取决于项目 | 每需要独立索引的归档量级；Chromium 所查 alink 已用 `ar -s`，该规则没有独立 ranlib；全平台实际次数 UNKNOWN | AM:53,69,75–85；GT:418；E028 |
| llvm-nm | 已安装；所查 RPM/GN 符号处理用 GNU `nm`，LLVM 版本实际调用 UNKNOWN | GNU nm 在 shared-library TOC 及可选 minidebug 路径按每 ELF/共享库调用；LLVM 次数 UNKNOWN | GN:34；GS:39–48；FD:309,314；E018 |
| llvm-objcopy | 已安装；所查 debuginfo 脚本用 GNU `objcopy`，LLVM 版本实际调用 UNKNOWN | GNU 分支按每 ELF、每 kernel artifact 或 minidebug 处理；LLVM 次数 UNKNOWN | RM:79；FD:279,318,322,476,495；E018 |
| llvm-strip | 已安装；BRP 宏明确传 `/bin/strip`，为 GNU binutils；LLVM 版本实际调用 UNKNOWN | GNU BRP 对每个匹配的 ELF/静态归档；LLVM 次数 UNKNOWN | TM:34–44；R/usr/lib/rpm/brp-strip:15–20、brp-strip-static-archive:15–19；E018 |
| llvm-readelf | 已安装；所查 RPM/GN 用 GNU `readelf`，LLVM 版本实际调用 UNKNOWN | GNU TOC 每共享库、可选 minidebug 每 ELF；LLVM 次数 UNKNOWN | GN:33；GS:23–35；FD:301,615；E018 |
| clang-scan-deps | **UNKNOWN（未取得实际使用证据）**；所查 RPM 宏/脚本、Chromium build/tizen_src/build/packaging 和两份已有日志均无命中；不能将“已安装”写成“在用” | 所查 cc/cxx 规则直接使用 `-MD/-MMD -MF`，没有单独 scan-deps 命令；全平台次数 UNKNOWN | E028 的完整搜索、`SCAN_DEPS_SEARCH_RC=1`；GT:367–370,383–396；安装证据 E019 |
| llvm-profdata | 已安装；所查普通 Tizen RPM 流程未发现调用；Chromium LLVM 构建脚本的 PGO 分支明确调用 | 脚本每次 PGO 训练后一次 merge；不是每个 RPM 默认调用；实际 bundled 发布是否执行 UNKNOWN | B:1074–1079；E020/E028/E032；E019 |
| llvm-config | 构建配置查询工具，本任务有只读调用；不能把本次调查调用计入 RPM 生产频度 | 包构建中使用次数 UNKNOWN | E018/E027；E028 所查范围 |
| 其余已安装工具 | 逐个安装/依赖记录在 4.4；尚无足以确认其在目标 RPM 构建中实际运行的证据 | 阶段与频度均 UNKNOWN；包含 llc、opt、llvm-as/dis/link、llvm-cov、llvm-symbolizer、clangd、clang-tidy 等，不凭名称分配“在用” | E019 安装事实；E028 的流程搜索；完整流程证据 E011/E026 |

现有 LOG13 是其他 Chromium 构建尝试的日志，只用于证明环境导出和出现过 LINK，不冒充用户给定受控对照的完整日志。`attempt13_postbuild.log` 只有开始时间，没有打包子工具执行记录（E032）。因此精确全平台频度和受控对照中每个工具的执行次数列入 UNKNOWN。

### 4.3 RPM debuginfo / strip 的实际实现

1. `TM:53–56` 在 install post 中按 `__debug_package` 条件调用 `__debug_install_post`，再执行 arch/os post。E018 的实际宏展开给出 `/usr/lib/rpm/find-debuginfo.sh -j2 ...`，以及 `brp-strip /bin/strip`、`brp-strip-static-archive /bin/strip`。
2. `FD:387–420,425–448,555–562` 按选中的未剥离 ELF 及硬链接分组处理，每个主文件调用 `debugedit`；它归属 `rpm-build-4.14.1.1-1.7.armv7l`（E018）。频度为待处理 ELF 主文件量级，不是源文件量级。
3. `FD:264–280`：kernel module 分支用 `eu-strip`；非 kernel 分支在 `STRIP_DEFAULT_PACKAGE != binutils` 时用 `eu-strip`，否则用 GNU `strip` 和 GNU `objcopy --add-gnu-debuglink`。`eu-strip` 属于 `elfutils-0.189-1.7.armv7l`，不是 LLVM，也不是 GNU binutils（E018）。历史每个 RPM 任务的该环境变量取值 UNKNOWN，两个分支均保留。
4. `FD:473–495` 的 Kconfig 分支调用 GNU `objcopy --only-keep-debug` 和第二次 objcopy；`FD:301–322,511` 的可选 minidebug 分支每 ELF 调用 readelf、两次 nm、两次 objcopy 及 xz。只有条件启用时这些调用才发生。
5. BRP `TM:35–42` 受 `__debug_package` 和 `_rpm_strip_disable` 条件控制；`brp-strip-comment-note` 在该宏中被注释掉，`brp-strip-shared` 虽安装但未在当前展开宏中列出。不能按目录里有脚本就计为执行（E018、E030）。

原始归属查询节选（E018）：

```text
PATH /bin/strip
/usr/bin/strip
binutils-2.43-1.6.armv7l
PATH /bin/objcopy
/usr/bin/objcopy
binutils-2.43-1.6.armv7l
PATH /bin/nm
/usr/bin/nm
binutils-2.43-1.6.armv7l
PATH /bin/readelf
/usr/bin/readelf
binutils-2.43-1.6.armv7l
PATH /usr/bin/eu-strip
/usr/bin/eu-strip
elfutils-0.189-1.7.armv7l
```

因此，仅优化 LLVM 的 strip/objcopy 不能声称覆盖当前已证实的 RPM 后处理路径；后处理成本本次没有测量（FD 与 E018）。

### 4.4 全量安装工具与 NEEDED 对照表

下面是 E019 的 `rpm -ql` 安装路径全集筛选结果，每个工具一行。`L` = 直接 NEEDED `libLLVM.so.22.1`；`C+L` = 还直接 NEEDED `libclang-cpp.so.22.1`；`否` = ELF 直接 NEEDED 不含这两类库；`N/A` = 脚本、非 ELF。这里的“否”只回答直接动态依赖，不据此宣称脚本不会启动依赖 LLVM 的子程序。字节数为解析符号链接后的工具文件大小，原链接 `ls -la` 也保存在 E019。

调用标记沿用 4.2：`CC`=clang 编译/driver 规则；`LD`=条件 lld 链接；`AR`=归档；`RANLIB`=RPM 宏指定、实际独立调用次数 UNKNOWN；`U`=生产调用阶段/频度 UNKNOWN。别名是否实际被使用也仍需调用证据，不能只因共享一个目标文件就计算调用次数。

<details>
<summary>clang：36 个路径（rpm -ql；逐项 ls/readelf 见 E019）</summary>

| 包内路径 / 工具名 | 字节 | LLVM 共享库 | 调用标记 |
| --- | --- | --- | --- |
| `/usr/bin/armv7l-tizen-linux-gnueabi-clang` | 75956 | C+L | CC |
| `/usr/bin/armv7l-tizen-linux-gnueabi-clang++` | 75956 | C+L | CC |
| `/usr/bin/clang` | 75956 | C+L | CC |
| `/usr/bin/clang++` | 75956 | C+L | CC |
| `/usr/bin/clang++-22` | 75956 | C+L | CC |
| `/usr/bin/clang-22` | 75956 | C+L | CC |
| `/usr/bin/clang-apply-replacements` | 59356 | C+L | U |
| `/usr/bin/clang-change-namespace` | 158788 | C+L | U |
| `/usr/bin/clang-check` | 25736 | C+L | U |
| `/usr/bin/clang-cl` | 75956 | C+L | U |
| `/usr/bin/clang-cpp` | 75956 | C+L | U |
| `/usr/bin/clang-doc` | 512616 | C+L | U |
| `/usr/bin/clang-extdef-mapping` | 22628 | C+L | U |
| `/usr/bin/clang-format` | 55276 | C+L | U |
| `/usr/bin/clang-include-cleaner` | 192372 | C+L | U |
| `/usr/bin/clang-include-fixer` | 96912 | C+L | U |
| `/usr/bin/clang-installapi` | 97064 | C+L | U |
| `/usr/bin/clang-move` | 131404 | C+L | U |
| `/usr/bin/clang-nvlink-wrapper` | 63144 | L | U |
| `/usr/bin/clang-offload-bundler` | 36156 | C+L | U |
| `/usr/bin/clang-query` | 85676 | C+L | U |
| `/usr/bin/clang-refactor` | 53276 | C+L | U |
| `/usr/bin/clang-reorder-fields` | 74076 | C+L | U |
| `/usr/bin/clang-scan-deps` | 103428 | C+L | U |
| `/usr/bin/clang-sycl-linker` | 46360 | L | U |
| `/usr/bin/clang-tidy` | 7006004 | C+L | U |
| `/usr/bin/clangd` | 8847268 | C+L | U |
| `/usr/bin/find-all-symbols` | 151480 | C+L | U |
| `/usr/bin/git-clang-format` | 28325 | N/A | U |
| `/usr/bin/modularize` | 117616 | C+L | U |
| `/usr/libexec/analyze-c++` | 488 | N/A | U |
| `/usr/libexec/analyze-cc` | 487 | N/A | U |
| `/usr/libexec/c++-analyzer` | 203 | N/A | U |
| `/usr/libexec/ccc-analyzer` | 21103 | N/A | U |
| `/usr/libexec/intercept-c++` | 493 | N/A | U |
| `/usr/libexec/intercept-cc` | 493 | N/A | U |

</details>

<details>
<summary>llvm：105 个路径（rpm -ql；逐项 ls/readelf 见 E019）</summary>

| 包内路径 / 工具名 | 字节 | LLVM 共享库 | 调用标记 |
| --- | --- | --- | --- |
| `/usr/bin/analyze-build` | 557 | N/A | U |
| `/usr/bin/bugpoint` | 202460 | L | U |
| `/usr/bin/clang-linker-wrapper` | 103412 | L | U |
| `/usr/bin/clang-offload-packager` | 28444 | L | U |
| `/usr/bin/clang-repl` | 38312 | C+L | U |
| `/usr/bin/diagtool` | 526688 | C+L | U |
| `/usr/bin/dsymutil` | 183116 | L | U |
| `/usr/bin/hmaptool` | 9997 | N/A | U |
| `/usr/bin/intercept-build` | 563 | N/A | U |
| `/usr/bin/ld.lld` | 3400272 | L | LD |
| `/usr/bin/ld64.lld` | 3400272 | L | U |
| `/usr/bin/llc` | 117376 | L | U |
| `/usr/bin/lld` | 3400272 | L | LD |
| `/usr/bin/lld-link` | 3400272 | L | U |
| `/usr/bin/lldb-dap` | 516488 | C+L | U |
| `/usr/bin/lldb-instr` | 84304 | C+L | U |
| `/usr/bin/lli` | 114812 | L | U |
| `/usr/bin/llvm-addr2line` | 61960 | L | U |
| `/usr/bin/llvm-ar` | 45292 | L | AR |
| `/usr/bin/llvm-as` | 17816 | L | U |
| `/usr/bin/llvm-bcanalyzer` | 13236 | L | U |
| `/usr/bin/llvm-bitcode-strip` | 116228 | L | U |
| `/usr/bin/llvm-c-test` | 66684 | L | U |
| `/usr/bin/llvm-cas` | 23928 | L | U |
| `/usr/bin/llvm-cat` | 16796 | L | U |
| `/usr/bin/llvm-cfi-verify` | 58620 | L | U |
| `/usr/bin/llvm-cgdata` | 23616 | L | U |
| `/usr/bin/llvm-config` | 145824 | 否 | U |
| `/usr/bin/llvm-cov` | 232136 | L | U |
| `/usr/bin/llvm-ctxprof-util` | 15676 | L | U |
| `/usr/bin/llvm-cvtres` | 17848 | L | U |
| `/usr/bin/llvm-cxxdump` | 36640 | L | U |
| `/usr/bin/llvm-cxxfilt` | 14580 | L | U |
| `/usr/bin/llvm-cxxmap` | 16284 | L | U |
| `/usr/bin/llvm-debuginfo-analyzer` | 98384 | L | U |
| `/usr/bin/llvm-debuginfod` | 53656 | L | U |
| `/usr/bin/llvm-debuginfod-find` | 40440 | L | U |
| `/usr/bin/llvm-diff` | 33476 | L | U |
| `/usr/bin/llvm-dis` | 25960 | L | U |
| `/usr/bin/llvm-dlltool` | 45292 | L | U |
| `/usr/bin/llvm-dwarfdump` | 115124 | L | U |
| `/usr/bin/llvm-dwarfutil` | 179172 | L | U |
| `/usr/bin/llvm-dwp` | 29860 | L | U |
| `/usr/bin/llvm-exegesis` | 5210100 | 否 | U |
| `/usr/bin/llvm-extract` | 45636 | L | U |
| `/usr/bin/llvm-gsymutil` | 41880 | L | U |
| `/usr/bin/llvm-ifs` | 37532 | L | U |
| `/usr/bin/llvm-install-name-tool` | 116228 | L | U |
| `/usr/bin/llvm-ir2vec` | 47888 | L | U |
| `/usr/bin/llvm-jitlink` | 211392 | L | U |
| `/usr/bin/llvm-lib` | 45292 | L | U |
| `/usr/bin/llvm-libtool-darwin` | 52356 | L | U |
| `/usr/bin/llvm-link` | 36840 | L | U |
| `/usr/bin/llvm-lipo` | 41616 | L | U |
| `/usr/bin/llvm-lto` | 74616 | L | U |
| `/usr/bin/llvm-lto2` | 74440 | L | U |
| `/usr/bin/llvm-mc` | 52812 | L | U |
| `/usr/bin/llvm-mca` | 133312 | L | U |
| `/usr/bin/llvm-ml` | 32912 | L | U |
| `/usr/bin/llvm-ml64` | 32912 | L | U |
| `/usr/bin/llvm-modextract` | 13132 | L | U |
| `/usr/bin/llvm-mt` | 15916 | L | U |
| `/usr/bin/llvm-nm` | 81548 | L | U |
| `/usr/bin/llvm-objcopy` | 116228 | L | U |
| `/usr/bin/llvm-objdump` | 537628 | L | U |
| `/usr/bin/llvm-offload-binary` | 28444 | L | U |
| `/usr/bin/llvm-offload-wrapper` | 24148 | L | U |
| `/usr/bin/llvm-opt-report` | 27716 | L | U |
| `/usr/bin/llvm-otool` | 537628 | L | U |
| `/usr/bin/llvm-pdbutil` | 474064 | L | U |
| `/usr/bin/llvm-profdata` | 253960 | L | U |
| `/usr/bin/llvm-profgen` | 226300 | L | U |
| `/usr/bin/llvm-ranlib` | 45292 | L | RANLIB |
| `/usr/bin/llvm-rc` | 103716 | L | U |
| `/usr/bin/llvm-readelf` | 1038168 | L | U |
| `/usr/bin/llvm-readobj` | 1038168 | L | U |
| `/usr/bin/llvm-readtapi` | 64056 | L | U |
| `/usr/bin/llvm-reduce` | 179128 | L | U |
| `/usr/bin/llvm-remarkutil` | 109136 | L | U |
| `/usr/bin/llvm-rtdyld` | 66664 | L | U |
| `/usr/bin/llvm-sim` | 15116 | L | U |
| `/usr/bin/llvm-size` | 39472 | L | U |
| `/usr/bin/llvm-split` | 36372 | L | U |
| `/usr/bin/llvm-stress` | 34356 | L | U |
| `/usr/bin/llvm-strings` | 18496 | L | U |
| `/usr/bin/llvm-strip` | 116228 | L | U |
| `/usr/bin/llvm-symbolizer` | 61960 | L | U |
| `/usr/bin/llvm-tblgen` | 2016956 | 否 | U |
| `/usr/bin/llvm-tli-checker` | 22896 | L | U |
| `/usr/bin/llvm-undname` | 16720 | L | U |
| `/usr/bin/llvm-windres` | 103716 | L | U |
| `/usr/bin/llvm-xray` | 199376 | L | U |
| `/usr/bin/offload-arch` | 33872 | L | U |
| `/usr/bin/opt` | 167648 | L | U |
| `/usr/bin/pp-trace` | 34468 | C+L | U |
| `/usr/bin/reduce-chunk-list` | 14004 | L | U |
| `/usr/bin/run-clang-tidy` | 26285 | N/A | U |
| `/usr/bin/sancov` | 60868 | L | U |
| `/usr/bin/sanstats` | 12060 | L | U |
| `/usr/bin/scan-build` | 57300 | N/A | U |
| `/usr/bin/scan-build-py` | 551 | N/A | U |
| `/usr/bin/scan-view` | 4691 | N/A | U |
| `/usr/bin/verify-uselistorder` | 22136 | L | U |
| `/usr/bin/wasm-ld` | 3400272 | L | U |
| `/usr/bin/yaml2macho-core` | 37464 | C+L | U |

</details>

<details>
<summary>lldb：5 个路径（rpm -ql；逐项 ls/readelf 见 E019）</summary>

| 包内路径 / 工具名 | 字节 | LLVM 共享库 | 调用标记 |
| --- | --- | --- | --- |
| `/home/owner/share/tmp/sdk_tools/lldb/bin/lldb` | 112528 | C+L | U |
| `/home/owner/share/tmp/sdk_tools/lldb/bin/lldb-argdumper` | 8600 | C+L | U |
| `/home/owner/share/tmp/sdk_tools/lldb/bin/lldb-server` | 1648180 | C+L | U |
| `/usr/bin/lldb` | 112528 | C+L | U |
| `/usr/bin/lldb-mcp` | 141960 | C+L | U |

</details>

<details>
<summary>llvm-devel：9 个路径（rpm -ql；逐项 ls/readelf 见 E019）</summary>

| 包内路径 / 工具名 | 字节 | LLVM 共享库 | 调用标记 |
| --- | --- | --- | --- |
| `/usr/bin/amdgpu-arch` | 33872 | L | U |
| `/usr/bin/nvptx-arch` | 33872 | L | U |
| `/usr/share/clang/clang-format-diff.py` | 6356 | N/A | U |
| `/usr/share/clang/clang-tidy-diff.py` | 14324 | N/A | U |
| `/usr/share/clang/run-find-all-symbols.py` | 4020 | N/A | U |
| `/usr/share/opt-viewer/opt-diff.py` | 2593 | N/A | U |
| `/usr/share/opt-viewer/opt-stats.py` | 2471 | N/A | U |
| `/usr/share/opt-viewer/opt-viewer.py` | 13774 | N/A | U |
| `/usr/share/opt-viewer/optrecord.py` | 10175 | N/A | U |

</details>

<details>
<summary>clang-accel-x86_64-armv7l：110 个路径（rpm -ql；逐项 ls/readelf 见 E019）</summary>

| 包内路径 / 工具名 | 字节 | LLVM 共享库 | 调用标记 |
| --- | --- | --- | --- |
| `/emul/usr/bin/armv7l-tizen-linux-gnueabi-clang` | 131592 | C+L | CC |
| `/emul/usr/bin/armv7l-tizen-linux-gnueabi-clang++` | 131592 | C+L | CC |
| `/emul/usr/bin/clang` | 131592 | C+L | CC |
| `/emul/usr/bin/clang++` | 131592 | C+L | CC |
| `/emul/usr/bin/clang-22` | 131592 | C+L | CC |
| `/emul/usr/bin/clang-apply-replacements` | 110264 | C+L | U |
| `/emul/usr/bin/clang-change-namespace` | 255024 | C+L | U |
| `/emul/usr/bin/clang-check` | 44104 | C+L | U |
| `/emul/usr/bin/clang-cl` | 131592 | C+L | U |
| `/emul/usr/bin/clang-cpp` | 131592 | C+L | U |
| `/emul/usr/bin/clang-doc` | 1162016 | C+L | U |
| `/emul/usr/bin/clang-extdef-mapping` | 39720 | C+L | U |
| `/emul/usr/bin/clang-format` | 98888 | C+L | U |
| `/emul/usr/bin/clang-include-cleaner` | 401016 | C+L | U |
| `/emul/usr/bin/clang-include-fixer` | 182800 | C+L | U |
| `/emul/usr/bin/clang-installapi` | 194272 | C+L | U |
| `/emul/usr/bin/clang-linker-wrapper` | 183904 | L | U |
| `/emul/usr/bin/clang-move` | 216528 | C+L | U |
| `/emul/usr/bin/clang-nvlink-wrapper` | 107680 | L | U |
| `/emul/usr/bin/clang-offload-bundler` | 60512 | C+L | U |
| `/emul/usr/bin/clang-offload-packager` | 47168 | L | U |
| `/emul/usr/bin/clang-query` | 161240 | C+L | U |
| `/emul/usr/bin/clang-refactor` | 98240 | C+L | U |
| `/emul/usr/bin/clang-reorder-fields` | 137456 | C+L | U |
| `/emul/usr/bin/clang-repl` | 61400 | C+L | U |
| `/emul/usr/bin/clang-scan-deps` | 198728 | C+L | U |
| `/emul/usr/bin/clang-sycl-linker` | 81736 | L | U |
| `/emul/usr/bin/clang-tidy` | 12174768 | C+L | U |
| `/emul/usr/bin/ld.lld` | 6449904 | L | LD |
| `/emul/usr/bin/llc` | 187816 | L | U |
| `/emul/usr/bin/lld` | 6449904 | L | LD |
| `/emul/usr/bin/lld-link` | 6449904 | L | U |
| `/emul/usr/bin/lli` | 190976 | L | U |
| `/emul/usr/bin/llvm-addr2line` | 98888 | L | U |
| `/emul/usr/bin/llvm-ar` | 81232 | L | AR |
| `/emul/usr/bin/llvm-as` | 30496 | L | U |
| `/emul/usr/bin/llvm-bcanalyzer` | 21800 | L | U |
| `/emul/usr/bin/llvm-bitcode-strip` | 208352 | L | U |
| `/emul/usr/bin/llvm-c-test` | 115024 | L | U |
| `/emul/usr/bin/llvm-cas` | 42592 | L | U |
| `/emul/usr/bin/llvm-cat` | 26232 | L | U |
| `/emul/usr/bin/llvm-cfi-verify` | 94048 | L | U |
| `/emul/usr/bin/llvm-cgdata` | 34808 | L | U |
| `/emul/usr/bin/llvm-cov` | 462672 | L | U |
| `/emul/usr/bin/llvm-ctxprof-util` | 25968 | L | U |
| `/emul/usr/bin/llvm-cvtres` | 30496 | L | U |
| `/emul/usr/bin/llvm-cxxdump` | 67840 | L | U |
| `/emul/usr/bin/llvm-cxxfilt` | 26016 | L | U |
| `/emul/usr/bin/llvm-cxxmap` | 26160 | L | U |
| `/emul/usr/bin/llvm-debuginfo-analyzer` | 167824 | L | U |
| `/emul/usr/bin/llvm-debuginfod` | 90480 | L | U |
| `/emul/usr/bin/llvm-debuginfod-find` | 64968 | L | U |
| `/emul/usr/bin/llvm-diff` | 67312 | L | U |
| `/emul/usr/bin/llvm-dis` | 43480 | L | U |
| `/emul/usr/bin/llvm-dlltool` | 81232 | L | U |
| `/emul/usr/bin/llvm-dwarfdump` | 190344 | L | U |
| `/emul/usr/bin/llvm-dwarfutil` | 286888 | L | U |
| `/emul/usr/bin/llvm-dwp` | 52200 | L | U |
| `/emul/usr/bin/llvm-exegesis` | 43978384 | 否 | U |
| `/emul/usr/bin/llvm-extract` | 72896 | L | U |
| `/emul/usr/bin/llvm-gsymutil` | 69232 | L | U |
| `/emul/usr/bin/llvm-ifs` | 64200 | L | U |
| `/emul/usr/bin/llvm-install-name-tool` | 208352 | L | U |
| `/emul/usr/bin/llvm-ir2vec` | 82072 | L | U |
| `/emul/usr/bin/llvm-jitlink` | 369792 | L | U |
| `/emul/usr/bin/llvm-lib` | 81232 | L | U |
| `/emul/usr/bin/llvm-libtool-darwin` | 89784 | L | U |
| `/emul/usr/bin/llvm-link` | 60632 | L | U |
| `/emul/usr/bin/llvm-lipo` | 80464 | L | U |
| `/emul/usr/bin/llvm-lto` | 136400 | L | U |
| `/emul/usr/bin/llvm-lto2` | 128952 | L | U |
| `/emul/usr/bin/llvm-mc` | 94120 | L | U |
| `/emul/usr/bin/llvm-mca` | 253824 | L | U |
| `/emul/usr/bin/llvm-ml` | 56608 | L | U |
| `/emul/usr/bin/llvm-ml64` | 56608 | L | U |
| `/emul/usr/bin/llvm-modextract` | 22016 | L | U |
| `/emul/usr/bin/llvm-mt` | 26016 | L | U |
| `/emul/usr/bin/llvm-nm` | 147800 | L | U |
| `/emul/usr/bin/llvm-objcopy` | 208352 | L | U |
| `/emul/usr/bin/llvm-objdump` | 946640 | L | U |
| `/emul/usr/bin/llvm-offload-binary` | 47168 | L | U |
| `/emul/usr/bin/llvm-offload-wrapper` | 38904 | L | U |
| `/emul/usr/bin/llvm-opt-report` | 55096 | L | U |
| `/emul/usr/bin/llvm-otool` | 946640 | L | U |
| `/emul/usr/bin/llvm-pdbutil` | 886760 | L | U |
| `/emul/usr/bin/llvm-profdata` | 437480 | L | U |
| `/emul/usr/bin/llvm-profgen` | 401928 | L | U |
| `/emul/usr/bin/llvm-ranlib` | 81232 | L | RANLIB |
| `/emul/usr/bin/llvm-rc` | 204448 | L | U |
| `/emul/usr/bin/llvm-readelf` | 2073064 | L | U |
| `/emul/usr/bin/llvm-readobj` | 2073064 | L | U |
| `/emul/usr/bin/llvm-readtapi` | 138240 | L | U |
| `/emul/usr/bin/llvm-reduce` | 331488 | L | U |
| `/emul/usr/bin/llvm-remarkutil` | 208712 | L | U |
| `/emul/usr/bin/llvm-rtdyld` | 111920 | L | U |
| `/emul/usr/bin/llvm-sim` | 26016 | L | U |
| `/emul/usr/bin/llvm-size` | 68104 | L | U |
| `/emul/usr/bin/llvm-split` | 56416 | L | U |
| `/emul/usr/bin/llvm-stress` | 56608 | L | U |
| `/emul/usr/bin/llvm-strings` | 30376 | L | U |
| `/emul/usr/bin/llvm-strip` | 208352 | L | U |
| `/emul/usr/bin/llvm-symbolizer` | 98888 | L | U |
| `/emul/usr/bin/llvm-tblgen` | 4415736 | 否 | U |
| `/emul/usr/bin/llvm-tli-checker` | 38952 | L | U |
| `/emul/usr/bin/llvm-undname` | 26112 | L | U |
| `/emul/usr/bin/llvm-windres` | 204448 | L | U |
| `/emul/usr/bin/llvm-xray` | 403168 | L | U |
| `/emul/usr/bin/opt` | 264832 | L | U |
| `/emul/usr/bin/wasm-ld` | 6449904 | L | U |
| `/usr/lib/baselibs-x86_64-armv7l/bin/llvm-config` | 329624 | 否 | U |

</details>

`libllvm` 的 rpm -ql 列表没有独立可执行工具，内容是共享库，原始清单见 `A/rpm-ql-libllvm.txt`（E019）。库本身的 ELF 检查见 E023。

## 5. 二进制反推交叉验证

### 5.1 主二进制身份及原始查询

| 项目 | Tizen ARM RPM clang | Chromium-EFL 的 Tizen bundled clang | 证据 |
| --- | --- | --- | --- |
| 实际路径 | `R/usr/bin/clang -> clang-22` | `C/tizen_src/buildtools/llvm/bin/clang` | E009/E015/E023 |
| 大小 | 75,956 字节 | 131,174,064 字节 | E023 的 ls 原文 |
| ELF | ELF32、ARM、DYN/PIE、EABI5 soft-float | ELF64、x86-64、EXEC | E023 的 file/readelf -h |
| 解释器 | `/lib/ld-linux.so.3` | `/emul/lib64/ld-linux-x86-64.so.2` | E023 |
| 版本 | clang 22.1.8 | clang 18.1.0rc | E013/E024 |
| RPM 归属 | clang-22.1.8-1.6.armv7l | 同 hash 的现有 chroot 副本查询明确无 RPM 归属 | E013/E024 |
| 直接 LLVM NEEDED | libclang-cpp.so.22.1、libLLVM.so.22.1 | 没有 LLVM/clang-cpp NEEDED | E023 |
| `.note.bolt_info` / `.text.hot` / `.text.unlikely` | 未见 | 未见 | E023 完整 readelf -SW |
| text 布局 | 一段名为 `.text` 的执行节 | 一段名为 `.text` 的执行节 | E023；仅描述观测，是否被历史布局工具改变 UNKNOWN |
| `.GCC.command.line` | 不存在 | 不存在 | E023；不能从已删除的节恢复全部 flags |
| llvm-config | build-mode=MinSizeRel，has-rtti=YES，shared-mode=shared | 同目录无 llvm-config | E018/E024 |

SHA256 原始输出（E023）：

```text
71c7a04fb70afb28973dcc5b5343bf948468c8bb949fd861bf11c1ed58a5993f  /home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0/usr/bin/clang-22
2b6de207d210216f7a4251cfb244b8101d5d6d1f8542f0b690123b0c86141ee7  /home/linhao/Toolchain/plan_evaluation/chromium-efl/tizen_src/buildtools/llvm/bin/clang
```

完整 `file`、`readelf -h/-d/-SW/-n`、sha256sum 及各命令返回码见 E023；每份 clang 的全部 NEEDED 在该日志中，不只截取 LLVM 名称。

### 5.2 ldd 与执行根

Tizen clang 在 `gbs chroot R` 中的 ldd 能解析两类 LLVM 库（E013）：

```text
libclang-cpp.so.22.1 => /usr/bin/../lib/libclang-cpp.so.22.1
libLLVM.so.22.1 => /usr/bin/../lib/libLLVM.so.22.1
```

上两行是去掉装载地址的摘录，完整原始输出保存在 E013。bundled clang 的宿主 ldd 成功，完整输出在 E024；它描述宿主库解析，不代替 Tizen 根环境。为在 chroot 内查询，使用此前已经存在的 `R/analysis/compiler-throughput-iwp74r1q/reference/bin/clang`，本次未复制/改写二进制，其 SHA256 与 C 下原件完全相同（E024）。

```text
clang version 18.1.0rc
Target: x86_64-tizen-linux-gnu
Thread model: posix
InstalledDir: /analysis/compiler-throughput-iwp74r1q/reference/bin
VERSION_RC=0
        not a dynamic executable
LDD_RC=1
```

ARM 根内 ldd 对该 x86_64 ELF 失败，已保留失败原文；随后执行其实际解释器 `/emul/lib64/ld-linux-x86-64.so.2 --list`，返回 `LOADER_RC=0`，解析的是 `/emul/usr/lib64/` 系统库，没有 LLVM 共享库（E024）。这不是“静态可执行文件”：它仍动态依赖 libc/libstdc++ 等系统库。

### 5.3 llvm-config 与共享库本体

逐项查询结果（E018）：`--assertion-mode=OFF`、`--build-mode=MinSizeRel`、`--has-rtti=YES`、`--targets-built=ARM BPF`。用户要求的 `--link-mode` **不受此 llvm-config 支持，返回 1 并打印 usage**；使用帮助中实际列出的 `--shared-mode` 补充，结果 `shared`。没有把失败项默默写为成功。

accel 的 llvm-config 显示 Release、RTTI YES、X86/ARM/AArch64/BPF；其 `--shared-mode` 因安装的 component libraries 不全而返回 1，不能作为“静态链接”证据。accel 主工具 NEEDED 直接证明依赖两类 LLVM 库（E023/E027/E031）。

除两个 clang 主 ELF，E023 还检查了 ARM 和 accel 各自的 `libLLVM.so.22.1`、`libclang-cpp.so.22.1`，没有发现上述 BOLT 专用标记或 hot/unlikely 独立节。只看 75 KB 壳程序不足以判断库代码的 PGO/BOLT 状态，所以已覆盖库本体；但节区负结果仍不能证明历史没有 profile-use/post-link（第 1 节 UNKNOWN）。

## 6. 逐项差异表

Tizen 列以安装包对应 spec 为基线，并标注已由二进制证实的值；工作区改动另写。Chromium 列同时标出脚本配置与实际 Tizen bundled 的事实边界。“影响方向”针对执行吞吐，未测量的配置差异均写“未知”；相同已确认设置的差异作用写“无影响”。作用工具范围按参数传递与 NEEDED 判定，**不是收益保证**。

| CMake 参数 / 特征 | Tizen LLVM | Chromium bundled | 是否差异 | 对执行吞吐的影响方向 | 影响哪些工具 | 证据 |
| --- | --- | --- | --- | --- | --- | --- |
| CMAKE_BUILD_TYPE | ARM 已证 MinSizeRel；accel 已证 Release | 脚本 Release；实际 bundled UNKNOWN | ARM 对脚本有；实际二者 UNKNOWN | 未知 | LLVM 工具及对应架构共享库 | TS:217–231；B:821；E018/E027 |
| LLVM_ENABLE_ASSERTIONS | OFF（既定前提；查询 No/OFF） | 实际 OFF（用户既定前提）；脚本 final 可 OFF，bootstrap 强制 ON | 实际无 | 无影响 | clang/LLVM 核心；bootstrap 非发布工具 | TS:214；B:822,972；E018；用户任务前提 |
| LLVM_LINK_LLVM_DYLIB | ARM 导出 ON；accel NEEDED 有 libLLVM；WS 已去掉显式 ON | 实际 bundled 无 LLVM NEEDED；脚本未显式设该项 | 已确认链接形态不同 | 未知 | 全部依赖对应 libLLVM 的工具；非仅 clang | TS:238；E019/E020/E023；WS:258–260 |
| LLVM_BUILD_LLVM_DYLIB | ON；实际有共享库 | 脚本未设；实际产线配置 UNKNOWN | UNKNOWN | 未知 | 生成 libLLVM；是否影响工具取决于链接关系 | TS:235；E023；B 全文 E008 |
| CLANG_LINK_CLANG_DYLIB | ARM ON；accel 直接依赖 clang-cpp | 实际 bundled 不依赖 clang-cpp；脚本值未显式设 | 已确认链接形态不同 | 未知 | clang 及依赖 libclang-cpp 的工具；并非所有 llvm-* | TS:239；E019/E023 |
| CLANG_BUILD_CLANG_DYLIB | ON | 脚本未显式设；实际 UNKNOWN | UNKNOWN | 未知 | 构建 clang-cpp；使用范围由 NEEDED 决定 | TS:236；E008/E019 |
| LLVM_ENABLE_LTO | 对应配方未设、源码默认 OFF；WS 条件 Thin；发布实值 UNKNOWN | 脚本 --thinlto 时 Thin，package 非 Darwin 指定；实际 bundled UNKNOWN | 配方不同；发布二进制 UNKNOWN | 未知 | 最终 LLVM 工具/库；不只 clang | S/llvm/cmake/modules/HandleLLVMOptions.cmake:32；WS:233；B:1135–1136；P:250–251 |
| LLVM_BUILD_INSTRUMENTED | 配方未启用，默认 OFF；发布 UNKNOWN | 脚本 PGO 中间阶段 IR；最终不是 instrumentation 阶段；实际 UNKNOWN | 脚本流程不同；实际 UNKNOWN | 未知 | 训练用 clang；最终 profile 消费涉及 LLVM 工具/库 | TS:198–274；S/llvm/cmake/modules/HandleLLVMOptions.cmake:1181；B:1030 |
| LLVM_PROFDATA_FILE / PGO | 配方无输入；发布 UNKNOWN | 脚本本地训练合并 profdata.prof；实际 UNKNOWN | 配方不同；实际 UNKNOWN | 未知 | 最终 LLVM 构建；训练仅覆盖 clang/其 LLVM 路径 | B:1064–1079,1133–1134；TS 全文 |
| BOLT | 配方无步骤；发布 UNKNOWN | 脚本 --bolt 后处理 bin/clang；实际 UNKNOWN | 脚本能力不同；实际 UNKNOWN | 未知 | 该脚本只处理 clang，不自动处理 lld/ar/共享库 | B:1433–1493；E023/E032 |
| LLVM_TARGETS_TO_BUILD | ARM: ARM/BPF；accel: X86/ARM/AArch64/BPF；其他架构见条件表 | 脚本九种目标；实际 bundled 完整目标集合 UNKNOWN | 脚本不同；实际 UNKNOWN | 未知 | 含 target 后端的工具和共享库 | TS:216–232；B:811；E018/E027 |
| LLVM_ENABLE_PROJECTS | clang;lldb;clang-tools-extra;lld;compiler-rt;openmp | 脚本 clang;lld;clang-tools-extra，bolt 条件追加；实际 UNKNOWN | 脚本不同 | 未知 | 决定交付工具集合；非只 clang | TS:241；B:812–814 |
| LLVM_ENABLE_RUNTIMES | spec 未设；初始默认空 | 脚本 compiler-rt，bootstrap/runtime triple 覆盖；实际 UNKNOWN | 脚本不同 | 未知 | 运行库产品；profile runtime 支持训练 | TS:241；S/llvm/CMakeLists.txt:141；B:824,964,1392–1413 |
| LLVM_OPTIMIZED_TABLEGEN | ON | 脚本未设；实际 UNKNOWN | UNKNOWN | 未知 | 构建时 TableGen；不据此推断已安装其他工具加速 | TS:250；B 全文 E008 |
| LLVM_USE_LINKER / LLVM_ENABLE_LLD | 条件 LLVM_USE_LINKER=lld；RPM 普通 __ld 仍 GNU | 脚本 LLVM_ENABLE_LLD=ON；actual compiler builder UNKNOWN | 配置入口不同 | 未知 | 构建 LLVM 时的链接；不是所有 RPM 使用 lld 的证明 | TS:209–212；B:838；RM:77；E018 |
| CMAKE_C_FLAGS_RELEASE / CMAKE_CXX_FLAGS_RELEASE | spec 未设，发布 cache UNKNOWN | 脚本未设，实际 cache UNKNOWN | UNKNOWN | 未知 | 全部被这些 flags 编译的 LLVM 工具/库 | TS:198–274；B 全文 E008 |
| CMAKE_C_FLAGS / CMAKE_CXX_FLAGS | 引用环境 CFLAGS/CXXFLAGS；当前 RPM 输入 Os；WS 追加 O3/ThinLTO/frame-pointer flags | 脚本有 sanitizers include/LIBXML_STATIC 等；实际构建 flags UNKNOWN | 脚本不同；有效发布 flags UNKNOWN | 未知 | 全部相关 LLVM 工具/库；需分架构 | TS:206–208；AM:56；WS:188–206；B:854–861,1119–1120 |
| Bootstrap | 配方单阶段；probe 非 bootstrap；发布外围流水线 UNKNOWN | 脚本支持且 package 指定；PGO 时三编译器阶段；实际 UNKNOWN | 脚本不同；实际 UNKNOWN | 未知 | 最终 LLVM 工具与库 | TS:198,344,348；B:941–1079；P:245–246 |
| LLVM_ENABLE_RTTI | ON，ARM/accel 查询 YES | 脚本未设；实际 UNKNOWN | UNKNOWN | 未知 | LLVM 工具/库；不得把 training -fno-rtti 当 compiler 构建值 | TS:215；E018/E027；B:1069 |
| LLVM_ENABLE_PIC | spec 未显式设；ARM ELF 为 PIE 是二进制另一维度 | 脚本 Linux 默认 OFF；--pic 可 ON；实际 UNKNOWN | UNKNOWN | 未知 | LLVM 工具/库；PIC 选项不等同于 ELF 类型 | B:816–826；E023 |
| MLGO | spec AOT inliner/regalloc；发布模型宏 UNKNOWN | 脚本 Linux 默认 model2.tgz inliner、regalloc none；实际 UNKNOWN | 配方不同；实际 UNKNOWN | 未知 | 用到 ML 模型的 clang/LLVM 路径；不是 PGO | TS:257–272；B:686–691,1368–1386 |
| LLVM_PARALLEL_COMPILE_JOBS / LINK_JOBS | 6 / 2 | 脚本未显式设；实际 UNKNOWN | UNKNOWN | 未知 | 构建 LLVM 的并发限制；本次未证明其改变工具运行吞吐 | TS:255–256；E008 |
| RPM debuginfo/strip 调用实现 | GNU binutils、elfutils、rpm-build debugedit | bundled LLVM 并未被这些宏选为默认 strip/objcopy | LLVM 与打包调用对象不同 | 未知 | 当前确认的打包符号处理不是 LLVM 工具 | TM:34–56；FD:264–322,445,476,495；E018 |

## 7. UNKNOWN 清单

| 未确定事项 | 原因与本次已尝试方法 | 确认所需条件 |
| --- | --- | --- |
| 实际 Tizen 工具/库是否用了 PGO | 已查安装 RPM VCS、对应 spec/默认值、当前宏、LLVMConfig、ELF 与 cache/日志路径；只有配方无启用证据，不能证明发布外部 flags。accel 包只记录 qemu-accel VCS | 与二进制 hash/包版本绑定的完整构建日志、CMakeCache、最终编译命令、profile 输入及产物清单；accel 还需其原始 x86_64 LLVM 包来源 |
| 实际 Tizen/实际 bundled 是否 BOLT 处理 | 已查主 ELF 和共享库节区，没有 bolt_info/hot/unlikely；未找到其发布后处理日志 | 对应 hash 的 post-link 命令、BOLT 版本及 fdata 来源，或完整可信发布流水线 |
| 实际 bundled 完整 CMake / PGO / ThinLTO / bootstrap | 已查 B/P/U、二进制引入提交、tizen_src 构建脚本和现有二进制目录；官方 third_party 脚本与 Tizen bundled 产物链未接通 | 引入提交 83f4935… 对应的 LLVM 构建 recipe、源码 revision、cache、buildlog 和加速/重打包记录 |
| 发布任务的环境 CFLAGS、RELEASE/MINSIZEREL flags、所有宏分支 | spec 保留环境与宏；当前 ARM root 宏不能自动代表发布时宏；ELF 没有 .GCC.command.line | 原发布 job 的 project config、宏展开、环境及编译命令；不应在本次运行 configure 来“补证” |
| MLGO 发布实值及模型版本 | spec 支持/default with，当前 AM with=1，但没有绑定发布任务的 cache/model hash | 原发布 cache、模型包 hash、对象清单和构建日志 |
| clang-scan-deps 是否在全平台生产中使用 | E028 搜索所查流程无命中，已确认安装但没有 execve 记录；没有全平台全部 spec/构建图 | 对目标 RPM 集合的真实命令日志/执行跟踪，含模块依赖扫描配置 |
| llvm-nm/objcopy/strip/readelf 等其他工具的全平台使用与频度 | 所查默认链使用 GNU/elfutils；不能排除个别包直接调用 LLVM；4.4 全表 U 项逐项保留 UNKNOWN | 全平台 spec、完整命令或进程执行清单及包/阶段标识 |
| lld/ranlib 精确调用数、实际平台或 bundled 路径 | RPM 变量导出不等于执行；GN lld 有条件；独立 ranlib 可被 ar -s 覆盖 | 每个实际构建命令和链接 driver 的 execve；本次没有新建构建图或运行构建 |
| 历史 RPM debuginfo 的具体分支与累计开销 | 已查宏、FD 和包归属；未取得每任务 STRIP_DEFAULT_PACKAGE、minidebug、strip_disable 等实际值；已有 postbuild 日志仅开始标记 | 完整 `%install`/post 脚本展开、环境与进程日志；性能分析需另行授权测量 |
| 其他 GBS 实例/架构的发布配置 | E006 枚举有多种版本和架构；本报告详细取证绑定选定 R，不将它概括为所有 Tizen 发布快照 | 明确要覆盖的发布快照/架构及其 RPM、日志、源码版本 |

以上未知项均对应 E016–E032 的实际尝试。`rpm --root` 使用宿主 RPM 的 `bdb_ro` 回退只读读取现有数据库，原始警告保留（E009/E016/E019），没有执行 RPM 安装或数据库重建。

## 8. 附录：命令与原始输出

全部调查日志保存在：

```text
/home/linhao/Toolchain/development/llvm-optimize/temp/build-config-audit/
```

`commands.jsonl` 逐条保存外层命令、返回码和时长；`commands.md` 保存完整命令展开与日志对应关系。每个 `NNN_*.log` 顶部保存执行的 shell 原文，后接未截断的 stdout/stderr 与返回码。E019/E023 内部批量查询还逐条打印每个 rpm/ls/readelf/file/sha256sum 的实际 argv 和返回码。原始日志不上 GitHub；此报告保留关键原文、完整配置条件和工具表，评审者在该工作区可复核全文。

注意：本报告引用的代码片段中存在 build 命令，那是 `nl/rg/git show` 读取的文件内容；本任务没有执行它们。非零返回包括预期的无命中、`git diff --no-index` 有差异、工具选项不支持、缺失文件，以及部分无权限目录搜索，均保留在对应日志中，没有解释为成功。

| 证据 | 原始输出文件 | 外层返回码 |
| --- | --- | --- |
| E001 | `A/001_discovery.log` | 0 |
| E002 | `A/002_spec.log` | 0 |
| E003 | `A/003_paths.log` | 0 |
| E004 | `A/004_cmake_defaults.log` | 0 |
| E005 | `A/005_storage.log` | 0 |
| E006 | `A/006_instances.log` | 0 |
| E007 | `A/007_other_source.log` | 0 |
| E008 | `A/008_chromium_scripts.log` | 0 |
| E009 | `A/009_root_packages.log` | 0 |
| E010 | `A/010_legacy_spec.log` | 0 |
| E011 | `A/011_root_macros.log` | 2 |
| E012 | `A/012_chromium_focus.log` | 0 |
| E013 | `A/013_chroot_query.log` | 0 |
| E014 | `A/014_chromium_flow.log` | 0 |
| E015 | `A/015_actual_bundled.log` | 0 |
| E016 | `A/016_macro_focus.log` | 0 |
| E017 | `A/017_version_source.log` | 2 |
| E018 | `A/018_config_queries.log` | 0 |
| E019 | `A/019_tool_inventory.log` | 0 |
| E020 | `A/020_snapshot_source.log` | 0 |
| E021 | `A/021_chromium_base_pgo.log` | 0 |
| E022 | `A/022_log_discovery.log` | 0 |
| E023 | `A/023_binary_inspection.log` | 0 |
| E024 | `A/024_binary_execution.log` | 0 |
| E025 | `A/025_actual_logs.log` | 1 |
| E026 | `A/026_call_sites.log` | 0 |
| E027 | `A/027_chromium_provenance.log` | 0 |
| E028 | `A/028_scan_deps_scope.log` | 0 |
| E029 | `A/029_source_defaults_precise.log` | 1 |
| E030 | `A/030_last_evidence.log` | 0 |
| E031 | `A/031_inventory_summary.log` | 0 |
| E032 | `A/032_profile_macro_and_logs.log` | 0 |
| E033 | `A/033_precommit_validation.log` | 0 |
| E034 | `A/034_collector_reproduction.log` | 0 |
| E035 | `A/035_final_validation.log` | 0 |
| E036 | `A/036_stage_review.log` | 2 |
| E037 | `A/037_stage_review_pass.log` | 0 |

其他原始/派生证据：`roots.json` 为实际实例列表；`rpm-ql-*.txt` 为每包完整安装文件列表；`tool_inventory.json` 为工具路径、目标、大小、ELF 类型和 NEEDED 的机器可读全集；`installed-source/` 为安装包 VCS 对应的只读源码导出；`capture.py` 与 `inventory.py` 是仅在 temp 下使用的记录/盘点脚本。源码导出命令与 SHA256 见 E020。初始目录与路径定位见 E001/E003/E005/E006。

可复用的盘点脚本已整理为 [tools/collect_llvm_inventory.py](../tools/collect_llvm_inventory.py)，必须显式传入已确认存在的 root。下面命令仅执行 RPM/文件/ELF 查询，把输出写到 temp，不执行所盘点的 LLVM 工具。E034 验证其 265 条记录与首次盘点完全一致。

```bash
python3 tools/collect_llvm_inventory.py \
  --root /home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0 \
  --output-dir temp/build-config-audit/recheck \
  --extra-package clang-accel-x86_64-armv7l
```

最终逐条路径核对见 E035，工具表完整性为 265/265。E033/E035 同时检查 LLVM 源码无工作区改动、GBS 配置与 HEAD 一致、源码/原始证据仍被忽略。

### 提交前自检

1. **是否存在没有 file:line 或命令输出作为证据的结论？** 否。静态配置引用 TS/WS/B/P 等确定文件及行号；安装/动态依赖/版本/宏展开引用 E 编号原始输出。用户提供的性能与断言事实明确标为前提，不伪称本次测得。推断（例如 ARM 共享链接分支）已标明依据和边界。
2. **是否有用“通常”“一般”“按惯例”填空的项？** 否。缺少发布环境、执行轨迹和构建记录的项均标 UNKNOWN；默认值仅在读到所绑定源码定义时使用，不外推不同版本。
3. **是否明确区分脚本支持与实际使用？** 是。仅能力/配方证据包括：B 的 `--pgo`、IR 插桩/训练/merge、`--bolt` 训练/重排、`--thinlto`、`--bootstrap`、MLGO、可选 runtime/平台参数；P 的 Linux 发布调用组合；TM:100–102 的 profile 宏；TS 的 MLGO 条件及 verify 分支。这些均未写成实际 Tizen bundled 或 accel 发布二进制已使用。实际事实仅采用 RPM 版本/VCS、ELF、llvm-config 和明确的既有调用记录。
4. **是否覆盖 RPM 打包阶段？** 是。debuginfo、BRP、minidebug、Kconfig 路径均已记录。GNU `strip/objcopy/nm/readelf/objdump` 来自 binutils 2.43-1.6；`eu-strip` 来自 elfutils 0.189-1.7；`debugedit` 来自 rpm-build 4.14.1.1-1.7。没有把这些算作 LLVM 工具调用（FD、TM、E018）。
5. **是否构建 LLVM、Chromium，或执行 gbs build / rpmbuild？** 否。只执行记录中的查询；`gbs chroot` 内命令为 --version、-print-*、llvm-config、ldd/loader --list、rpm 查询和文件读取。读取 spec/build.py 不等于运行其构建步骤。
6. **PGO / BOLT 结论依据是什么？** 安装包 VCS 对应 spec 无启用/训练/后处理步骤、绑定源码默认值、现存宏和主程序/库 ELF 检查支持“配方 NO”。发布产物整体仍 UNKNOWN，需要与包版本和 hash 绑定的完整构建及后处理证据，尤其 accel 的原始 LLVM 来源。Chromium 官方脚本的优化能力不能代替本题实际 bundled 的来源证明。
7. **是否向 Gerrit 推送任何内容？** 否。读取嵌套源码仓库的 remote/git 对象不涉及推送；本任务产出仅按工作区 GitHub origin 提交推送。
