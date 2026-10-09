# 37 tizen_base 新配方与静态归档转换认证策略核查

日期：2026-10-09（Asia/Shanghai）。起点主仓库提交 `213041c85721caadf84ea5f438634a54447e613f`。
先读 STATUS 与 docs/36；docs/25–36 保持原样。

**结论：认证策略覆盖。** 在 docs/35 同一 x86_64 buildconfig、RPM 宏及 define 下，
`cb679968` 的编译参数与已验证 `f111162e` **并非逐 token 完全相同**：
C/C++/ASM 公共 flags 末尾多一次 `-Wno-unused-command-line-argument`。
该 token 已在原参数中存在，分类为诊断控制；没有增加新的机器码生成选项。
两组编译器名称和两个显式链接开关也有变化，实际含义见 §2。

把新公共参数替换进 docs/28 保存的全部 **225 档、3,853 条** bitcode 原命令，
保留每条命令其余 LLVM CMake/目标/成员参数，逐条调用未修改的 `classify_options`：
**3,853/3,853 PASS，未分类 token 0，所有末项策略检查 PASS**。
因此这些参数不会触发转换脚本的选项分类/末项拒绝；无需为这次配方差异修改 Source 或补丁。
证据：`E/policy-result.json`、`all-target-command-tokens.jsonl`。

这是只读的**编译参数策略覆盖核查**，不是新目标整套配方的完整构建或 `%install` 执行结果。
没有运行 CMake、Ninja、编译、归档转换或 rpmbuild；不把新配方尚未产生的 IR、符号与运行资源门禁记成通过。
结论限定为下述同一宏环境，未来 buildconfig、编译器默认配置或源码追加选项变化仍要重新核查。

## 0. 输入身份与方法

| 别名 | 路径/版本 |
| --- | --- |
| W | `/home/linhao/Toolchain/development/llvm-optimize` |
| E | `W/temp/target-recipe-policy-check-20261009`，本轮证据；以下未加前缀的证据文件均相对 E |
| R | `W/temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0`，docs/35 原根，只读 |
| B | `R/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build`，只读取现有 Cache/构建图作交叉核对 |
| BC | `W/temp/archive-fix-v2-build-20260929/full-build/buildconfig.conf`，docs/35 沿用的 buildconfig |
| E28 | `W/temp/static-native-conversion-v2-20260924` |
| E36 | `W/temp/archive-fix-tizen-consumers-20261009` |
| validated | `f111162e94aa48ed367c9d2c039456c70e7160ae:packaging/llvm.spec`，读取 Git blob，不用本地三处并发修改的原件 |
| target | `cb67996861d070d68fec2b4c623eed7d20ba2e23:packaging/llvm.spec`，读取 Git blob |

| 输入 | SHA256 |
| --- | --- |
| validated spec 快照 | `1155e2e32f7d797186a1003ca6f3d4c08ddaff8ab5594370b7e1938e9d9ba9ec` |
| target spec 快照 | `9ee73e37f1297a261b835bcd9c7fa2fbff72e271816950991cbe95be0945edda` |
| E36 原始 spec diff，本轮逐字节核对 Git diff | `e976a71cbb9fd98dd9f3b0365c91641850f2ef29dd820449fadc043676f67f5c` |
| BC | `1e7610b6a922d27b80eb59c1c78bdf716f7de2e8e24700e0ee7c62522739ed52` |
| R/home/abuild/.rpmmacros | `9b49f3dd05542ffe0ad772444207b856a3f23591872aa8af12e61ec8de4e61ec` |
| R/home/abuild/.rpmrc | `fe35ff5b81c0509d9ff633dd569f8cd5b433a6c61c1a170ae9bd037d92b0442c` |
| R/usr/bin/rpmspec | `c182909104906c5da7d398529d898ad2ebe10b241ab08cda03f8480f6e66eefe` |
| tools/llvm_static_archives_source.py | `6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557` |
| E28/conversion/summary.json（原命令语料） | `581dba7e10adeb0bcab4570bcea72d3820f9109bcd5ca85f7eb65c0a6de1bedb` |

`git status --porcelain` 开场为空。保护清单 `protected-start.json`、收尾 `final-integrity.json`；
W/llvm 原 spec、Source、评审补丁、gbs 配置、原根宏/Cache/build.ninja 和 docs/25–36 均未改。
没有访问已隔离混合根。只新增本报告、更新 STATUS，并在 E 保存查询证据。

### 0.1 使用原根 rpmspec，保持同一宏环境

docs/35 的 define 原文取自
`temp/archive-fix-v2-final-20261009/continue-20261009/abuild-resume.sh:5`：

```text
--define '_smp_mflags -j4'
--define '_srcdefattr (-,root,root)'
--nosignature --target=x86_64
--define '_build_create_debug 1'
```

先用 `gbs chroot --root R`、`su ... - abuild` 只读查询 `rpm --showrc`、`%optflags`、编译器链接及 cfg。
根内 `rpmspec --version` 输出 `RPM version 4.14.1`；HOME=/home/abuild，_toolchain=clang，_smp_mflags=-j4。
**没有手工加 `_toolchain` define。** 原根 `.rpmmacros:47–70` 来自 BC:141–168，
`.rpmrc:6` 登记 x86_64 optflags，BC:356–362 是其上游定义；末尾 `-g` 以已生成的原根配置为准。
`R/usr/lib/rpm/macros:1046–1059` 及 `R/usr/lib/rpm/tizen/macros:229` 使 build 前 CFLAGS/CXXFLAGS 取该 optflags；
与 docs/35 `continue-20261009/build/build.log:8–11` 的实际值交叉核对。

首次尝试根内 `/dev/stdin` 读 spec 时该节点不可用，原输出保留在 `*-expanded.stdout`，没有获得可用展开结果。
最终方法不向原根复制或写入任何文件：用 **R 自带 loader、依赖库、rpmspec** 在宿主路径读取两份原样 Git blob。
设置 `RPM_CONFIGDIR=R/usr/lib/rpm`、`HOME=R/home/abuild`，并把根内 `--showrc` 列出的**完整 macro path**
逐段映射到 R（包括 `/etc/rpm/macros.*`、platform、fileattrs 和 abuild 的宏文件）。
只额外把 `_topdir` 固定为根内实际展开的 `/home/abuild/rpmbuild`，防止宿主路径前缀污染结果。

两边 `--showrc` 的 **505 个活动宏**在仅去除文件系统 R 前缀、宏搜索路径行及等价 `_topdir` 定义后全量相同，
差异文件 `exact-showrc.diff` 为空。所有输入宏文件摘要在 `environment-inputs.json`。
这不是调用宿主 rpm，也没有用一个手写 optflags 替代原根宏环境。

完整 argv、环境覆盖、stdout/stderr 和退出码：`commands.jsonl`、`expand_exact.py`。
最终调用形式如下（R/E 见路径表，M 是上述原宏搜索路径逐项映射到 R 后的冒号分隔串；完整 M 在 commands.jsonl）：

```sh
env HOME="$R/home/abuild" RPM_CONFIGDIR="$R/usr/lib/rpm" \
  "$R/lib64/ld-linux-x86-64.so.2" --library-path "$R/lib64:$R/usr/lib64" \
  "$R/usr/bin/rpmspec" --macros "$M" \
  --define '_smp_mflags -j4' --define '_srcdefattr (-,root,root)' \
  --nosignature --target=x86_64 --define '_build_create_debug 1' \
  --define '_topdir /home/abuild/rpmbuild' --parse "$E/target.spec"
# validated.spec 使用完全相同的命令，仅替换输入文件名。
```

最终两份 `rpmspec --parse` exit0，分别保存 `validated-exact-parsed.stdout`、`target-exact-parsed.stdout`；
`*-exact-build.txt` 是对应 `%build` 全文，未执行。
只抽取其中变量赋值、echo/sed 和 CMake 参数文本，用 shell 的 printf 展开成 `*-cmake-argv.stdout`，
**没有调用 cmake**，也未执行 cp、mkdir、ninja、安装段。`*-text-expand.sh` 保存准确的纯文本展开程序。

## 1. spec 差异逐段说明

下面是 E36 的完整 diff，方向是 **target cb679968 → validated f111162e**：
`-` 属于新 target，`+` 属于旧 validated。不能按相反方向解释。

```diff
diff --git a/packaging/llvm.spec b/packaging/llvm.spec
index 64705188b67c..54a07ce84218 100644
--- a/packaging/llvm.spec
+++ b/packaging/llvm.spec
@@ -59,13 +59,6 @@ BuildRequires: sed
 %endif
 BuildRequires: ninja
 
-%if %{undefined _toolchain}
-%ifarch x86_64
-BuildRequires: clang, llvm, libllvm
-%{!?_toolchain: %define _toolchain clang}
-%endif
-%endif
-
 
 Requires: libllvm = %{version}-%{release}
 
@@ -192,29 +185,25 @@ cp %{SOURCE1001} .
 export QEMU_RESERVED_VA=0x100000000
 %endif
 
-%ifarch x86_64
 # Strip pre-existing optimization flags and remove performance-harming flags, then force -O3 + ThinLTO
 OPTFLAGS_CFLAGS=$(echo "$CFLAGS" | sed \
     -e 's/\-O[0-9sz]//g' \
     -e 's/\-Ofast//g' \
-    -e 's/\-fstack-protector-strong//g' \
-    -e 's/\-fstack-protector-all//g' \
     -e 's/\-fstack-protector//g' \
-    -e 's/\-fno-inline-functions//g' \
+    -e 's/\-fstack-protector-all//g' \
+    -e 's/\-fstack-protector-strong//g' \
     -e 's/\-fno-omit-frame-pointer//g' \
     -e 's/\-momit-leaf-frame-pointer//g')
 OPTFLAGS_CXXFLAGS=$(echo "$CXXFLAGS" | sed \
     -e 's/\-O[0-9sz]//g' \
     -e 's/\-Ofast//g' \
-    -e 's/\-fstack-protector-strong//g' \
-    -e 's/\-fstack-protector-all//g' \
     -e 's/\-fstack-protector//g' \
-    -e 's/\-fno-inline-functions//g' \
+    -e 's/\-fstack-protector-all//g' \
+    -e 's/\-fstack-protector-strong//g' \
     -e 's/\-fno-omit-frame-pointer//g' \
     -e 's/\-momit-leaf-frame-pointer//g')
-export CFLAGS="$OPTFLAGS_CFLAGS -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument"
-export CXXFLAGS="$OPTFLAGS_CXXFLAGS -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument"
-%endif
+export CFLAGS="$OPTFLAGS_CFLAGS -O3 -flto=thin -fomit-frame-pointer"
+export CXXFLAGS="$OPTFLAGS_CXXFLAGS -O3 -flto=thin -fomit-frame-pointer"
 
 # Set up MLGO AOT model paths from bundled verify assets
 %if %{with mlgo}
@@ -229,13 +218,8 @@ cd build
 cmake \
     -G Ninja \
     -DTIZEN=1 \
-%ifarch x86_64
-    -DCMAKE_C_COMPILER=clang \
-    -DCMAKE_CXX_COMPILER=clang++ \
-%else
     -DCMAKE_C_COMPILER=%__cc \
     -DCMAKE_CXX_COMPILER=%__cxx \
-%endif
     -DLLVM_HOST_TRIPLE=%{_host} \
     -DLLVM_DEFAULT_TARGET_TRIPLE=%{_host} \
     -DLLVM_TARGET_TRIPLE_ENV=%{_host} \
@@ -273,15 +257,6 @@ cmake \
     -DCLANG_ENABLE_ARCMT=OFF \
     -DLLVM_BUILD_LLVM_DYLIB=ON \
     -DCLANG_BUILD_CLANG_DYLIB=ON \
-%ifarch x86_64
-    -DLLVM_LINK_LLVM_DYLIB=OFF \
-    -DCLANG_LINK_CLANG_DYLIB=OFF \
-%else
-%if %{defined _toolchain}
-    -DLLVM_LINK_LLVM_DYLIB=ON \
-    -DCLANG_LINK_CLANG_DYLIB=ON \
-%endif
-%endif
     -DLLVM_ENABLE_PROJECTS="clang;lldb;clang-tools-extra;lld;compiler-rt;openmp" \
     -DLLVM_ENABLE_PER_TARGET_RUNTIME_DIR=OFF \
     -DLLVM_BUILD_EXAMPLES=OFF \
```

| 段 | 新 target 相对 validated 的变化 | 在本次 x86_64 宏环境中是否影响编译参数 |
| --- | --- | --- |
| 1，target:62–68 | `_toolchain` 未定义时，x86_64 补 clang/llvm/libllvm BR 并定义 clang | **不触发**；BC 与原根已定义 clang。原来的 llvm_release_build=0 分支不变，未删调试参数 |
| 2a，target:195–214 | 限 x86_64 做 flags 清理；先删 strong/all 再删普通 stack-protector，另删 fno-inline-functions | x86_64 两边均执行；实际输入只有普通 `-fstack-protector`，没有 strong/all 或 fno-inline-functions，所以本环境清理后 token 相同。其他宏环境下不能据此认定相同 |
| 2b，target:215–216 | C/C++ flags 尾部额外 `-Wno-unused-command-line-argument` | **有文本差异**；ASM 使用同一 CFLAGS，故也多一次。是原有诊断 token 的重复，§3 实际分类通过 |
| 3，target:232–238 | x86_64 显式用 clang/clang++，不再用 __cc/__cxx 拼前缀名 | **编译器名称有差异**；本根四个名字解析到同一 clang-22，cfg 的 target/resource 相同，详见 §2.2 |
| 4，target:276–284 | x86_64 显式 LLVM_LINK_LLVM_DYLIB=OFF、CLANG_LINK_CLANG_DYLIB=OFF；非 x86_64 条件另有 ON | x86_64 旧版未传入而默认 OFF，新版显式 OFF；不是新增归档成员编译选项。非 x86_64 分支不在本任务认证范围 |

完整源码树差异名单为 `source-changes.txt`：除 packaging 外，变化在 libcxx/libcxxabi；
**本次沿用的 llvm/clang CMake 及命令分类所引 Clang 源码没有差异**。
本 spec 的项目列表不含 libcxx/libcxxabi，未设置 LLVM_ENABLE_RUNTIMES；
因此沿用 docs/28 保存的 LLVM CMake 追加项有可核对依据，而非假定任意新源码都相同。
证据：`git diff --name-only f111162e… cb679968…` 原输出，§2 完整项目参数。

## 2. x86_64 宏展开与完整 CMake 参数

### 2.1 optflags 与公共 flags

两份 spec 使用同一 `%optflags`，以下是原根原始值（保留两个空格）：

```text
-Os -fstack-protector -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument -momit-leaf-frame-pointer  -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables -fno-omit-frame-pointer -g
```

证据：`root-macros.stdout:5`、`exact-optflags-{validated,target}.stdout`。
spec 没有重定义 optflags；CFLAGS/CXXFLAGS 的清理发生在其后。
为了便于表格阅读，以下 `F`、`T` 只合并空白，不改变 token、次序或重复项：

```text
F = -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables -g -O3 -flto=thin -fomit-frame-pointer
T = -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables -g -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument
```

T=F 后接一个 `-Wno-unused-command-line-argument`；不是新的不认识的后端开关。
F 所代表的原始展开值与 docs/35 现有 Cache 的 C/CXX/ASM flags **逐字节相同**（连空白也核对），
证据 `B/CMakeCache.txt:348,385,421`、`policy-result.json`。
Release 自身的 `-O3 -DNDEBUG` 未通过 -D 覆盖，由 CMake 追加；已验 Cache:357,394,430 为该值。

### 2.2 所有显式 CMake 参数逐项对比

两边生成器均 `-G Ninja`，源码参数均 `../llvm`，调用 cwd 均 `P/build`；
`P=/home/abuild/rpmbuild/BUILD/llvm-22.1.8`。表中 P 仅缩写路径。
validated 45 个、target 47 个 -D 参数，没有省略 MLGO 或链接参数。
原始完整 argv 是 `validated-cmake-argv.stdout`、`target-cmake-argv.stdout`；JSON 为 `*-cmake.json`。

| 参数 | validated f111162e | target cb679968 | 对比 |
| --- | --- | --- | --- |
| `CLANG_BUILD_CLANG_DYLIB` | `ON` | `ON` | 相同 |
| `CLANG_ENABLE_ARCMT` | `OFF` | `OFF` | 相同 |
| `CLANG_LINK_CLANG_DYLIB` | 未传入（默认 OFF） | `OFF` | 不同，见下文 |
| `CLANG_RESOURCE_DIR` | `../lib64/clang/22` | `../lib64/clang/22` | 相同 |
| `CMAKE_AR` | `/usr/bin/llvm-ar` | `/usr/bin/llvm-ar` | 相同 |
| `CMAKE_ASM_FLAGS` | `F` | `T` | 不同，见下文 |
| `CMAKE_BUILD_TYPE` | `Release` | `Release` | 相同 |
| `CMAKE_CXX_COMPILER` | `x86_64-tizen-linux-gnu-clang++` | `clang++` | 不同，见下文 |
| `CMAKE_CXX_FLAGS` | `F` | `T` | 不同，见下文 |
| `CMAKE_C_COMPILER` | `x86_64-tizen-linux-gnu-clang` | `clang` | 不同，见下文 |
| `CMAKE_C_FLAGS` | `F` | `T` | 不同，见下文 |
| `CMAKE_EXE_LINKER_FLAGS` | `-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections` | `-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections` | 相同 |
| `CMAKE_INSTALL_PREFIX` | `/usr` | `/usr` | 相同 |
| `CMAKE_RANLIB` | `/usr/bin/llvm-ranlib` | `/usr/bin/llvm-ranlib` | 相同 |
| `CMAKE_SHARED_LINKER_FLAGS` | `-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections` | `-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections` | 相同 |
| `LLVM_BINUTILS_INCDIR` | `/usr/include` | `/usr/include` | 相同 |
| `LLVM_BUILD_DOCS` | `OFF` | `OFF` | 相同 |
| `LLVM_BUILD_EXAMPLES` | `OFF` | `OFF` | 相同 |
| `LLVM_BUILD_LLVM_DYLIB` | `ON` | `ON` | 相同 |
| `LLVM_BUILD_TESTS` | `OFF` | `OFF` | 相同 |
| `LLVM_DEFAULT_TARGET_TRIPLE` | `x86_64-tizen-linux-gnu` | `x86_64-tizen-linux-gnu` | 相同 |
| `LLVM_ENABLE_ASSERTIONS` | `No` | `No` | 相同 |
| `LLVM_ENABLE_DOXYGEN` | `OFF` | `OFF` | 相同 |
| `LLVM_ENABLE_LTO` | `Thin` | `Thin` | 相同 |
| `LLVM_ENABLE_PER_TARGET_RUNTIME_DIR` | `OFF` | `OFF` | 相同 |
| `LLVM_ENABLE_PROJECTS` | `clang;lldb;clang-tools-extra;lld;compiler-rt;openmp` | `clang;lldb;clang-tools-extra;lld;compiler-rt;openmp` | 相同 |
| `LLVM_ENABLE_RTTI` | `ON` | `ON` | 相同 |
| `LLVM_HOST_TRIPLE` | `x86_64-tizen-linux-gnu` | `x86_64-tizen-linux-gnu` | 相同 |
| `LLVM_INCLUDE_DOCS` | `OFF` | `OFF` | 相同 |
| `LLVM_INCLUDE_EXAMPLES` | `OFF` | `OFF` | 相同 |
| `LLVM_INCLUDE_TESTS` | `OFF` | `OFF` | 相同 |
| `LLVM_LIBDIR_SUFFIX` | `64` | `64` | 相同 |
| `LLVM_LINK_LLVM_DYLIB` | 未传入（默认 OFF） | `OFF` | 不同，见下文 |
| `LLVM_MLGO_EMBED_TF_XLA_RUNTIME_OBJECTS` | `P/mlgo_verify_assets/xla_runtime_objects/xla_compiled_cpu_function.cc.o;P/mlgo_verify_assets/xla_runtime_objects/cpu_function_runtime.cc.o;P/mlgo_verify_assets/xla_runtime_objects/custom_call_status.cc.o;P/mlgo_verify_assets/xla_runtime_objects/executable_run_options.cc.o;P/mlgo_verify_assets/xla_runtime_objects/runtime_single_threaded_matmul_f32.cc.o` | `P/mlgo_verify_assets/xla_runtime_objects/xla_compiled_cpu_function.cc.o;P/mlgo_verify_assets/xla_runtime_objects/cpu_function_runtime.cc.o;P/mlgo_verify_assets/xla_runtime_objects/custom_call_status.cc.o;P/mlgo_verify_assets/xla_runtime_objects/executable_run_options.cc.o;P/mlgo_verify_assets/xla_runtime_objects/runtime_single_threaded_matmul_f32.cc.o` | 相同 |
| `LLVM_MLGO_EXPORT_TF_XLA_RUNTIME` | `OFF` | `OFF` | 相同 |
| `LLVM_OPTIMIZED_TABLEGEN` | `ON` | `ON` | 相同 |
| `LLVM_OVERRIDE_MODEL_HEADER_INLINERSIZEMODEL` | `P/mlgo_verify_assets/InlinerSizeModel.h` | `P/mlgo_verify_assets/InlinerSizeModel.h` | 相同 |
| `LLVM_OVERRIDE_MODEL_HEADER_REGALLOCEVICTMODEL` | `P/mlgo_verify_assets/RegAllocEvictModel.h` | `P/mlgo_verify_assets/RegAllocEvictModel.h` | 相同 |
| `LLVM_OVERRIDE_MODEL_OBJECT_INLINERSIZEMODEL` | `P/mlgo_verify_assets/InlinerSizeModel.o` | `P/mlgo_verify_assets/InlinerSizeModel.o` | 相同 |
| `LLVM_OVERRIDE_MODEL_OBJECT_REGALLOCEVICTMODEL` | `P/mlgo_verify_assets/RegAllocEvictModel.o` | `P/mlgo_verify_assets/RegAllocEvictModel.o` | 相同 |
| `LLVM_PARALLEL_COMPILE_JOBS` | `6` | `6` | 相同 |
| `LLVM_PARALLEL_LINK_JOBS` | `2` | `2` | 相同 |
| `LLVM_TARGETS_TO_BUILD` | `X86;ARM;AArch64;BPF` | `X86;ARM;AArch64;BPF` | 相同 |
| `LLVM_TARGET_TRIPLE_ENV` | `x86_64-tizen-linux-gnu` | `x86_64-tizen-linux-gnu` | 相同 |
| `LLVM_USE_LINKER` | `lld` | `lld` | 相同 |
| `TENSORFLOW_AOT_PATH` | `P/mlgo_verify_assets/mlgo_sysroot` | `P/mlgo_verify_assets/mlgo_sysroot` | 相同 |
| `TIZEN` | `1` | `1` | 相同 |

两个“未传入”不当作未知：`llvm/llvm/CMakeLists.txt:912–913` 默认 LLVM_LINK_LLVM_DYLIB=OFF，
`llvm/clang/CMakeLists.txt:309–310` 让 CLANG_LINK_CLANG_DYLIB 默认继承它；
现有 B/Cache:193、1643 实际均 OFF。新 spec 只是显式写出相同值。
`BUILD_SHARED_LIBS`、`CMAKE_C_FLAGS_RELEASE`、`CMAKE_CXX_FLAGS_RELEASE`、`LLVM_ENABLE_RUNTIMES`
均没有新增显式设置，不构造它们不存在的 -D 参数。

编译器名称的只读原始输出（`root-showrc.stdout` 末尾）：

```text
/usr/bin/clang -> clang-22
/usr/bin/clang++ -> clang
/usr/bin/x86_64-tizen-linux-gnu-clang -> clang
/usr/bin/x86_64-tizen-linux-gnu-clang++ -> clang++
# clang.cfg；clang++.cfg -> clang.cfg
-target x86_64-tizen-linux-gnu
-resource-dir /usr/lib64/clang/22
```

模式 cfg 查找依据为 `llvm/clang/lib/Driver/Driver.cpp:1417–1463`；
这是在**当前根**的同一 ELF/配置上的名称变化，不能外推另一个根中裸 clang 一定同版本。
历史记录里已含 cfg 和 driver 推导的 `--target`，可能重复；§3 保留历史 argv 做主体检查，
另对每条用 clang/clang++ 名义并去掉一个重复 target 的文本变体检查，3,853 条也全部 PASS。
该补充检查不是新编译命令的实测采集。

## 3. 转换脚本逐 token 核查

### 3.1 完整语料与调用方式

未修改的 `tools/llvm_static_archives_source.py:189–267` 是本轮唯一分类器。
只导入模块并调用 `classify_options(argv, 'x86_64')`；未调用 convert/main、llvm-dis、clang 或任何归档转换命令。

原语料是 docs/28 §1.1 的 `E28/conversion/summary.json`，每个 bitcode 成员的
`results[].settings.recorded_command`；来自当时 llvm-dis 读出的 `llvm.commandline`。
该元数据产生位置：`llvm/clang/lib/CodeGen/CodeGenModule.cpp:8036–8043`。
CMake/成员差异保留，包括仅一个成员的 `-ftrapping-math`，没有只核查代表 TU。

构造方法及断言：

1. 将 F 的 `-frecord-gcc-switches` 按历史记录的 driver 规范化表示为 `-frecord-command-line`。
2. 在每条原 argv 中寻找整个 F token 序列，**3,853 条均恰好匹配一次**。
3. 仅把这个序列替换成 T 的规范化序列；其余 include、定义、源/目标路径及 CMake 追加项逐 token 保留。
4. 原 argv 与派生 argv 分别分类；除逐 token 列表多一个诊断项外，最终策略对象逐字段相同。

调用代码、断言和完整输入/输出：`classify.py`、`all-target-command-tokens.jsonl`。
后者每行带归档路径、成员 ordinal/name、原 argv、**派生 target argv**、每个 token 的 index/category/reason。
它们是静态推导，不标成“cb679968 本轮实际生成的 llvm.commandline”。

LLVM 自身追加项来源：`llvm/llvm/cmake/modules/HandleLLVMOptions.cmake:441,455,481,1155–1157,1313`，
对应 PIC、语义插入、inline 可见性、函数/数据分段、ThinLTO；
`llvm/llvm/cmake/modules/AddLLVM.cmake:40` 对应异常关闭时 unwind 参数。
完整分类依据沿用 docs/28 §1.1–1.2，原记录中的其他诊断、C++ 标准、优化级、成员级 flag 都列在下表及 JSONL。

### 3.2 每种开关 token 的实际分类

下表列全 **74 种以 - 开头的 token**，次数是派生语料中的出现总数（保留重复项）。
`ir` 表示前端语义/IR 属性类，其中优化等级也按末项补回；
`restore` 表示后端策略补回；`irrelevant` 表示转换不重放（包括已物化的 ThinLTO 输出动作，非声称 LTO 对原构建无影响）。
不把分类用的 `--target` 行等同于跳过 IR triple 检查，Source:310 仍独立校验 triple。

| Token | 分类 | 次数 |
| --- | --- | ---: |
| `--driver-mode=g++` | 不重放（irrelevant） | 3844 |
| `--target=x86_64-tizen-linux-gnu` | 不重放（irrelevant） | 7706 |
| `-D` | 不重放（irrelevant） | 26690 |
| `-I` | 不重放（irrelevant） | 23847 |
| `-MD` | 不重放（irrelevant） | 3853 |
| `-MF` | 不重放（irrelevant） | 3853 |
| `-MT` | 不重放（irrelevant） | 3853 |
| `-O3` | 已进 IR（ir） | 7706 |
| `-Wall` | 不重放（irrelevant） | 7707 |
| `-Wc++98-compat-extra-semi` | 不重放（irrelevant） | 3853 |
| `-Wcast-qual` | 不重放（irrelevant） | 3854 |
| `-Wcovered-switch-default` | 不重放（irrelevant） | 3853 |
| `-Wctad-maybe-unsupported` | 不重放（irrelevant） | 3853 |
| `-Wdelete-non-virtual-dtor` | 不重放（irrelevant） | 3844 |
| `-Werror=date-time` | 不重放（irrelevant） | 3853 |
| `-Werror=global-constructors` | 不重放（irrelevant） | 169 |
| `-Werror=unguarded-availability-new` | 不重放（irrelevant） | 3853 |
| `-Wextra` | 不重放（irrelevant） | 3853 |
| `-Wformat` | 不重放（irrelevant） | 3853 |
| `-Wformat-pedantic` | 不重放（irrelevant） | 1 |
| `-Wformat-security` | 不重放（irrelevant） | 3853 |
| `-Wimplicit-fallthrough` | 不重放（irrelevant） | 3854 |
| `-Wmisleading-indentation` | 不重放（irrelevant） | 3853 |
| `-Wmissing-field-initializers` | 不重放（irrelevant） | 3853 |
| `-Wno-error=unused-but-set-variable` | 不重放（irrelevant） | 3853 |
| `-Wno-error=unused-command-line-argument` | 不重放（irrelevant） | 3853 |
| `-Wno-extra` | 不重放（irrelevant） | 1 |
| `-Wno-long-long` | 不重放（irrelevant） | 3853 |
| `-Wno-nested-anon-types` | 不重放（irrelevant） | 1569 |
| `-Wno-noexcept-type` | 不重放（irrelevant） | 3844 |
| `-Wno-pass-failed` | 不重放（irrelevant） | 3844 |
| `-Wno-pedantic` | 不重放（irrelevant） | 1 |
| `-Wno-unused` | 不重放（irrelevant） | 1 |
| `-Wno-unused-command-line-argument` | 不重放（irrelevant） | 7706 |
| `-Wno-unused-parameter` | 不重放（irrelevant） | 3853 |
| `-Wnon-virtual-dtor` | 不重放（irrelevant） | 3844 |
| `-Woverloaded-virtual` | 不重放（irrelevant） | 1569 |
| `-Wp,-D_FORTIFY_SOURCE=2` | 不重放（irrelevant） | 3853 |
| `-Wsign-compare` | 不重放（irrelevant） | 1 |
| `-Wstring-conversion` | 不重放（irrelevant） | 3853 |
| `-Wsuggest-override` | 不重放（irrelevant） | 3844 |
| `-Wwrite-strings` | 不重放（irrelevant） | 3853 |
| `-c` | 不重放（irrelevant） | 3853 |
| `-fPIC` | 已进 IR（ir） | 3853 |
| `-fasynchronous-unwind-tables` | 已进 IR（ir） | 3853 |
| `-fcolor-diagnostics` | 不重放（irrelevant） | 3854 |
| `-fdata-sections` | 后端补回（restore） | 3854 |
| `-fdiagnostics-color=never` | 不重放（irrelevant） | 3853 |
| `-fexceptions` | 已进 IR（ir） | 3853 |
| `-ffunction-sections` | 后端补回（restore） | 3853 |
| `-flto=thin` | 不重放（irrelevant） | 7706 |
| `-fmessage-length=0` | 不重放（irrelevant） | 3853 |
| `-fno-common` | 已进 IR（ir） | 1569 |
| `-fno-exceptions` | 已进 IR（ir） | 3843 |
| `-fno-semantic-interposition` | 已进 IR（ir） | 3854 |
| `-fomit-frame-pointer` | 已进 IR（ir） | 3853 |
| `-frecord-command-line` | 已进 IR（ir） | 3853 |
| `-ftrapping-math` | 已进 IR（ir） | 1 |
| `-funwind-tables` | 已进 IR（ir） | 3843 |
| `-fvisibility-inlines-hidden` | 已进 IR（ir） | 3844 |
| `-fvisibility=hidden` | 已进 IR（ir） | 266 |
| `-g` | 已进 IR（ir） | 3853 |
| `-g2` | 已进 IR（ir） | 3853 |
| `-gdwarf-4` | 后端补回（restore） | 3853 |
| `-isystem` | 不重放（irrelevant） | 20 |
| `-m64` | 已进 IR（ir） | 3853 |
| `-march=nehalem` | 已进 IR（ir） | 3853 |
| `-mfpmath=sse` | 已进 IR（ir） | 3853 |
| `-msse4.2` | 已进 IR（ir） | 3853 |
| `-o` | 不重放（irrelevant） | 3853 |
| `-pedantic` | 不重放（irrelevant） | 3853 |
| `-pipe` | 不重放（irrelevant） | 3853 |
| `-resource-dir` | 不重放（irrelevant） | 3853 |
| `-std=c++17` | 已进 IR（ir） | 3844 |

其余 token 是 driver 路径、-D/-I/-isystem/-resource-dir/-o/-MT/-MF 的参数或输入输出路径；
**每一个原文字面值和分类**在 `unique-token-classification.tsv`，共 **15,979 个 token/category/reason 去重行**。
完整逐次记录共 **379,739 个 token**，在 JSONL；文件名/路径未用一个抽象“所有路径”代替实际分类。
代表完整 argv 和结果另存 `representative-commands.json`（含 libarcher）。这些大份原始证据留 temp，不进 Git。

新增 token 的语义证据：
`llvm/clang/include/clang/Basic/DiagnosticGroups.td:1014` 定义 `unused-command-line-argument` 诊断组；
`DiagnosticDriverKinds.td:470–472` 将“argument unused during compilation”归入它。
现有分类器 Source:241–245 对 `-W*` 返回 `irrelevant`；不需要扩白名单，也没有新的分类依据待 PM 决策。

### 3.3 策略判定结果

```text
commands = 3853
archives = 225
unclassified = 0
categories.ir = 71153
categories.restore = 11560
categories.irrelevant = 297026
status = CERTIFIED_OPTION_POLICY_COVERED
```

3,853 条一致的末项结果：

| 策略项 | 实际结果 | Source 规则 |
| --- | --- | --- |
| 优化末项 | -O3 | :173、253–254 |
| DWARF 末项 | -gdwarf-4 | :255–256 |
| function-sections/data-sections | true/true，均显式启用 | :218–224、257–262 |
| unique-section-names/addrsig | true/true，原命令未显式改默认 | :178、259–261 |
| fp-contract | on，LLVM 22 非 CUDA/HIP 默认 | :264–267；默认来源 docs/28 §1.2，Clang.cpp:2797 |
| 与原命令最终策略相比 | 每条全部相同 | classify.py 的对象相等断言 |

补充纯文本负对照（不是配方中真实存在的错误）：追加 `-mllvm` →
`unclassified original command token: -mllvm`；追加 `-O2` →
`uncertified last optimization: ['-O2']`；追加 `-gdwarf-5` →
`uncertified last DWARF option: ['-gdwarf-5']`。三者均如预期拒绝，分类器未被绕过。
`driver-spelling-check.json` 另记 3,853 个 driver 名称/重复 target 变体 PASS。

## 4. 结论与边界

- **cb679968 的 x86_64 原编译参数落在现有转换认证策略内**，在 docs/35 同一宏/编译器配置与已有 LLVM CMake 追加项下，
  分类和末项检查会通过；不存在需要修改 Source 才能接受的本轮新增 token。
- 文本并非完全相同，故没有直接走“参数相同即结束”的捷径：新增重复告警 flag、编译器名称、显式 OFF 都已逐项处理。
- 这不证明新配方未来 `%install` 的全部文件、IR 类型元数据、符号保留、超时/内存门禁必然通过；
  当前没有新构建产物。docs/36 关于“新目标完整配方未重建”的边界仍保留，后续交目标流水线正常构建。
- 未修改 spec、Source、补丁和认证指纹；未启动构建或转换，未推 Gerrit。

## 附录：可复核证据

E 的绝对路径是 `/home/linhao/Toolchain/development/llvm-optimize/temp/target-recipe-policy-check-20261009`。

| 文件 | 内容 |
| --- | --- |
| `commands.jsonl` | 核心 rpm/Git 查询 argv、stdin、环境覆盖、退出码及输出文件指针 |
| `target.spec`、`validated.spec`、`target-vs-validated-base.diff` | 原样 Git blob 和完整差异 |
| `root-showrc.stdout`、`exact-showrc.stdout`、`exact-showrc.diff` | 根内宏查询、根二进制重定位运行及等价对照 |
| `environment-inputs.json`、`macro-files.json` | 实际加载的宏、rpmrc、编译器配置及 CMake 源码 SHA |
| `*-exact-parsed.stdout`、`*-exact-build.txt` | 两份 rpmspec 全文与 build 段 |
| `*-text-expand.sh`、`*-cmake-argv.stdout`、`*-cmake.json`、`expanded-build.diff` | 不执行构建的参数展开与完整对比 |
| `all-target-command-tokens.jsonl`、`unique-token-classification.tsv`、`option-token-classification.json` | 全部命令、每个 token 的原文与分类 |
| `policy-result.json`、`driver-spelling-check.json` | 总判定、末项策略、负对照与 driver 名称补充检查 |
| `audit.py`、`expand.py`、`expand_exact.py`、`classify.py` | 查询/静态展开/纯文本分类过程；探索性读取失败也保留，最终以 exact 输出为准 |
| `protected-start.json`、`final-integrity.json` | 开始/结束保护文件哈希；只允许 docs/STATUS.md 随本报告更新 |

自检：构建 0；归档转换 0；spec/Source/补丁改动 0；Gerrit 推送 0。
本报告与 STATUS 在同一提交更新并推送 GitHub；提交号由 Git 历史定位，避免自引用哈希。
