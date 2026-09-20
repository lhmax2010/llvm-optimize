# 18 BOLT 的 spec 集成设计与工具链身份识别

日期：2026-09-20。**本轮交付身份检查脚本与集成设计，未修改 spec，未构建或重写任何二进制。**

按本轮范围更正，直接采用既定结论：20 对 TU 的完整 `.o` 逐字节相同；五轮独立
测量方向一致，筛选层编译吞吐改善约 14–15%；纯优化重写自身峰值
3.481499 GiB、wall 21.83 秒。**不再追 docs/17 的噪声门禁。** 最终收益由专用
服务器上的 Chromium 全量构建验收；这些筛选结果不等于 Chromium 总 wall 收益。

建议第一版仅重写 x86_64 clang 及其 clang++ 等别名；使用固定存档 profile，
不在包构建中插桩训练。身份采用“保守 vendor 标识 + 最终 RPM/ELF 哈希清单 +
实测 BOLT 节区 + 实际调用路径”共同确认。Quickbuild 性能试验包可以先采用
已测的去 DWARF 路径，**明确不提供该 clang 的源码级调试能力**；正式发布前另行验证
保留并更新 DWARF 的路径。后者的资源代价目前 UNKNOWN，不能用 3.48 GiB 替代。

## 0. 证据与路径

下文源码路径相对 W，行号对应工作区 LLVM 提交
`f111162e94aa48ed367c9d2c039456c70e7160ae`。源码树已有的三处并发改动保持原样。
命令、stdout/stderr、退出码归档在 A；本文中的代码块标为“设计/服务器操作”的均未执行。

```text
W   = /home/linhao/Toolchain/development/llvm-optimize
A   = W/temp/spec-integration-20260920
TC  = W/temp/toolchain-baseline/usr
E16 = W/temp/bolt-final-20260918
Q   = W/temp/bolt-measurement-20260918/run
R1  = W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0
B   = R1/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build
C   = /home/linhao/Toolchain/plan_evaluation/chromium-efl
J   = W/temp/baseline-resume-20260917
FD  = R1/usr/lib/rpm/find-debuginfo.sh
RM  = R1/usr/lib/rpm/macros
```

既有资源数据引自 [13](13_baseline_build.md)、[14](14_bolt_feasibility.md)、
[15](15_bolt_measurement.md)、[16](16_bolt_final.md) 及其原始记录；本轮只重新读取。
A/initial-state.txt、source-git-diff.txt 保存起始状态。spec SHA256：
`95887b2d060b38d5ef8f56936f7481a03d131f9d26432180a68e02ec95f0dda5`。

## 1. 工具链身份识别

### 1.1 自报身份：推荐只设置 CLANG_VENDOR

**拟议 CMake 参数，尚未应用：**

```text
-DCLANG_VENDOR=TizenLLVM-opt-r1
-DLLVM_VERSION_SUFFIX=
```

`opt-r1` 表示本项目的构建配方身份，**不要写成 bolt-enabled**：BOLT 是后链接阶段，
可能降级，而此时版本字符串已经编进原 clang。是否实际重写成功必须由最终清单与 ELF
确认。RPM Release 另取唯一构建标识，例如 `1.opt1`，并按服务器版本策略递增。
所有相互有 `%{version}-%{release}` 依赖的子包保持一致（spec:63、100）。

精确语义如下：

| 项目 | 当前源码行为 | 证据 |
| --- | --- | --- |
| `CLANG_VENDOR` | STRING cache，默认来自 PACKAGE_VENDOR；非空时给 Version.cpp 定义该字符串并**追加一个空格** | `llvm/clang/CMakeLists.txt:293`；`llvm/clang/lib/Basic/CMakeLists.txt:52` |
| `LLVM_VERSION_SUFFIX` | 当前默认空；接在数字版本后，成为 LLVM PACKAGE_VERSION；默认传给 CLANG_VERSION_SUFFIX，再进入 CLANG_VERSION_STRING | `llvm/cmake/Modules/LLVMVersion.cmake:3`；`llvm/llvm/CMakeLists.txt:23`；`llvm/clang/CMakeLists.txt:335`；`llvm/clang/include/clang/Basic/Version.inc.in:2` |
| `--version` / `-v` | 相同 PrintVersion 首行：vendor + `clang version ` + 完整版本 + 可选仓库信息；分别写 stdout / stderr | `llvm/clang/lib/Basic/Version.cpp:100`；`llvm/clang/lib/Driver/Driver.cpp:2330`、`:2487` |
| `__clang_version__` | 完整版本字符串 + 空格 + 仓库信息，**不含 vendor** | `llvm/clang/lib/Frontend/InitPreprocessor.cpp:847` |
| `__clang_major__` / minor / patchlevel | 独立数字宏，不从展示字符串解析；以上两个参数不修改它们 | 同文件 `:842`；Version.inc.in:3–6 |
| `__VERSION__` | vendor + `Clang ` + 完整版本及仓库信息，**会受 vendor 影响** | InitPreprocessor.cpp:915；Version.cpp:113 |
| `-dumpversion` | 直接输出 CLANG_VERSION_STRING，因此 suffix 会改变它，vendor 不改变它 | Driver.cpp:2469 |

本轮只读查询的实际输出（A/current-version-queries.txt）：

```text
clang version 22.1.8
Target: x86_64-tizen-linux-gnu
Thread model: posix
InstalledDir: /usr/lib/x86_64-linux-gnu
22.1.8
#define __VERSION__ "Clang 22.1.8"
#define __clang_major__ 22
#define __clang_minor__ 1
#define __clang_patchlevel__ 8
#define __clang_version__ "22.1.8 "
```

这里通过 `/lib64/ld-linux-x86-64.so.2 <ELF>` 查询，InstalledDir 是 loader 目录，
**不能据此认定 clang 安装位置或资源目录**。版本第一行与宏可以读取，后续真正构建
必须在正确运行环境中直接调用 clang，并核对 `-print-resource-dir` 和实际配置文件。

以下为根据源码推导的输出，**不是本轮重新构建后的实测**；假定仓库字符串仍为空：

| 查询 | 只设 vendor 为 `TizenLLVM-opt-r1` | 再设 suffix 为 `-tizenopt1`（不推荐） |
| --- | --- | --- |
| `clang --version`、`clang -v` 首行 | `TizenLLVM-opt-r1 clang version 22.1.8` | `TizenLLVM-opt-r1 clang version 22.1.8-tizenopt1` |
| `__clang_version__` | `"22.1.8 "` | `"22.1.8-tizenopt1 "` |
| `__VERSION__` | `"TizenLLVM-opt-r1 Clang 22.1.8"` | `"TizenLLVM-opt-r1 Clang 22.1.8-tizenopt1"` |
| `-dumpversion` | `22.1.8` | `22.1.8-tizenopt1` |
| major/minor/patchlevel | 22 / 1 / 8 | 22 / 1 / 8 |

若构建生成了 repository/revision 信息，Version.cpp:68 会按原规则追加；不要把上表
空仓库的示例当成所有环境下的完整固定字符串。Target、线程模型也不由这两个参数改变。

**兼容性结论：只改 vendor 的风险较小，但不是零；不建议改 LLVM_VERSION_SUFFIX。**

- 已检查 R1 的 CMake 探测：`usr/share/cmake/Modules/Compiler/Clang-DetermineCompiler.cmake:2`
  用 `defined(__clang__)`；`Clang-DetermineCompilerInternal.cmake:3` 用三个数字宏。
  这条探测路径不受 vendor/suffix 影响。不是对所有包的 configure 作保证。
- 以 `^clang version` 为锚点或固定取第 3 个单词的解析器会因 vendor 前缀改变而失败；
  要求纯数字 `-dumpversion` 的解析器会受 suffix 影响。这是根据上述明确输出推导的
  风险例子，**尚未证明某个 Tizen 包实际用了这些表达式**。本机没有全平台全部 configure
  脚本；宿主 `/usr/share/autoconf/autoconf/c.m4` 也不存在，不能声称完成兼容性普查。
- suffix 不只是展示文字：`llvm/llvm/cmake/modules/AddLLVM.cmake:704` 把它加入某些
  共享库 SOVERSION/VERSION；`:731` 也用于共享库文件名。即使 clang 本身静态链接，
  同 spec 仍产出共享库和开发包。改变它可能影响 `%files`、依赖解析及第三方加载。
- vendor 还进入 `llvm.ident`（`llvm/clang/lib/CodeGen/CodeGenModule.cpp:8026`）和
  DWARF producer（`llvm/clang/lib/CodeGen/CGDebugInfo.cpp:804`）。因此换 vendor 后，
  `.o` 的标识元数据、使用 `__VERSION__` 的程序字符串可能改变。不能声称所有输出字节不变。

保守部署顺序：先用现有二进制 + RPM Release/可信哈希清单实施身份检查；需要自报身份时，
再对**未 BOLT 与 BOLT 两组同时**设置相同 vendor，suffix 留空，做 configure 和编译烟测。
若第三方解析不兼容，可保持 vendor 也不变，继续用包清单和哈希识别。不能通过删除
`.comment`、`.GCC.command.line` 等来掩盖集成后的一致性差异。

### 1.2 无需改 spec 的四层检查

#### RPM 与 SHA256

在**真正执行编译的根/worker 内**执行：

```bash
CC_PATH=$(command -v clang)
CC_ELF=$(readlink -f -- "$CC_PATH")
rpm -qf --qf '%{NAME} %{EPOCHNUM}:%{VERSION}-%{RELEASE}.%{ARCH}\nSOURCE=%{SOURCERPM}\n' "$CC_PATH" "$CC_ELF"
rpm -Vf "$CC_ELF"                 # 无输出且 exit 0：所属包通过 RPM 文件校验
sha256sum "$CC_ELF"               # 再与可信发布清单逐字节身份匹配
readelf -SW "$CC_ELF"
readelf -n "$CC_ELF"
```

本次源 RPM 查询（A/baseline-package-metadata.txt）：

```text
clang 22.1.8-1.x86_64
SOURCE=llvm-22.1.8-1.src.rpm
```

这是 `rpm -qp .../RPMS/x86_64/clang-22.1.8-1.x86_64.rpm` 的实际结果。
**TC 是解包目录**：宿主 `rpm -qf TC/bin/clang-22` 实际返回
`is not owned by any package`，退出 1；BOLT 文件同样无归属。不能把 `rpm -qp` 的
源包信息伪装成宿主已经安装了该包。原清单 J/rpm-inventory.json 记录全部 22 个包。

| 手段 | 能证明 | 不能单独证明 |
| --- | --- | --- |
| NEVRA、SOURCERPM、qf | 当前 RPM 数据库登记的包身份、路径归属 | 文件未被手工覆盖；实际执行的是这个路径；该包真的启用了 BOLT |
| `rpm -Vf` | 与该 RPM 数据库记录的一致性检查 | 数据库/包的来源可信；构建任务绕过该文件的情况 |
| SHA256 + 可信发布清单 | 文件与指定发布产物字节相同 | 一个无人认证的 hash 自己不证明来源；相同字符串版本不等于相同 hash |
| BOLT 节区/note | 文件保留了 BOLT 后处理迹象，note 可记录具体命令 | 来自本项目、一定优化成功、性能有收益；标记也可伪造或被后续 strip 删除 |
| 实际命令/exec 路径 + worker 内 hash | 当前构建实际用了哪一个文件 | 单看 PATH、CC 环境变量、某个配置默认值仍不够 |

#### 本轮两个 ELF 的实际节区对比

原始 `readelf -SW/-n/-d` 分别在 A/rpm-sections.txt、bolt-sections.txt、
rpm-notes.txt、bolt-notes.txt、*-needed.txt；完整结构化结果在 elf-inspection.json。

| 项目 | TC/bin/clang-22 | E16/optimized/bin/clang-22 |
| --- | --- | --- |
| 字节数 | 139,929,464 | 215,899,856 |
| SHA256 | `3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c` | `d6538b5ee1fdc429008b4481b651f994e354eabd55853666a0a9f0da03692e63` |
| `--version` 首行 | clang version 22.1.8 | clang version 22.1.8 |
| `.note.bolt_info` | 无 | 有，NOTE，0x2a0 字节 |
| `.bolt.org.text` | 无 | 有，AX，0x5affa8f 字节 |
| `.bolt.org.rodata` / `.bolt.org.eh_frame` / `.bolt.org.eh_frame_hdr` | 无 | 均有 |
| `.text.cold` / `.rodata.cold` | 无 | 均有 |
| `.symtab` / `.strtab` / `.comment` / `.GCC.command.line` | 无 | 均有；不是 BOLT 专有证据，也反映剥离方式不同 |
| `.gnu_debuglink` | 有 | 无 |
| `.note.gnu.build-id` | 无 | 无；不能用不存在的 build ID 识别本次二者 |

BOLT-only 节区**全集**是上表的 11 项；RPM-only 只有 `.gnu_debuglink`。
两者均没有单独的 `.text.hot`、`.text.unlikely`；不能把通用 hot/cold 节区当作必备条件。
BOLT 输出也没有 `.rela.text`，因为它是重写前的输入要求，不能作为最终 BOLT 产物的必备条件。
本版本 `llvm/bolt/lib/Rewrite/RewriteInstance.cpp:4829` 会剥离非 ALLOC 的 RELA。

实际 note 摘录（完整绝对路径在 A/bolt-notes.txt）：

```text
Displaying notes found in: .note.bolt_info
Owner GNU; NT_GNU_GOLD_VERSION
Version: BOLT revision: <unknown>, command line: .../bin/llvm-bolt .../stripped/bin/clang-22
-o .../optimized/bin/clang-22 -data=.../merged.fdata
-reorder-blocks=ext-tsp -reorder-functions=cdsort -split-functions
-split-all-cold -split-eh -dyno-stats --thread-count=1
```

`revision: <unknown>` **不能充当 BOLT 工具版本证明**；发布清单还要记录 llvm-bolt 自身的
SHA256 与源码提交。RPM 后处理可能再改 ELF，当前 BOLT hash 不是将来 RPM 内文件的预定 hash。

#### 从 Chromium 的实际调用确认

本机读取到的证据层级必须区分：

1. C/tizen_src/build/config/tizen_features.gni:31 的默认
   `tizen_clang_base_path="//tizen_src/buildtools/llvm"`，以及
   C/tizen_src/build/toolchain/tizen/BUILD.gn:22–32 把 cc/cxx 指向该目录的
   clang/clang++，ld=cxx。这只是 GN 规则，不是某轮最终展开值。
2. 既有 Chromium 日志
   `/home/linhao/Toolchain/plan_evaluation/chromium_analysis/evidence/spike_libcxx/full_gbs_attempt13_visibility.log:156`
   实际导出 `CC=armv7l-tizen-linux-gnueabi-clang`、`CXX=...-clang++`。
   这证明该构建环境设置，仍不能代替 Ninja 最终使用路径。
3. 既有编译分派 trace
   `/home/linhao/Toolchain/plan_evaluation/analysis/compiler_throughput/matrix-v2-1789128556949030207/runtime-dispatch/native-trace/llvm-compile-execve.log:1–2`
   显示 `/usr/bin/clang++` → `/emul//usr/bin/clang-22`，参数含 ARM triple 与 `-c`。
   **这条是既有诊断编译 trace，不冒称 Chromium 全量构建 trace。**

本机本轮未找到可读取的目标 Chromium 输出目录/toolchain.ninja：用户先前给定的
whole_image 路径与 OLD scratch 路径均不存在；C 下定向文件枚举也未返回 toolchain.ninja。
因此 **Quickbuild 最终实际 cc/cxx 路径及 hash 当前 UNKNOWN**，需服务器执行第 3 节。
A/chromium-discovery.txt、chromium-root-presence.txt、actual-compiler-search.txt、
historical-compile-path.txt 保存搜索与原始证据。尤其不能只更新 `/usr/bin/clang`，
却继续由 bundled clang 或旧 `/emul` accel 编译。

### 1.3 可立即运行的身份脚本

交付 [tools/verify_toolchain_identity.sh](../tools/verify_toolchain_identity.sh)。
依赖 Bash、coreutils、awk、readelf；rpm 不存在时明确 UNKNOWN，不依赖 Python、
本工作区、root 权限或网络。默认查 PATH 中的 clang，也接受工具链根、bin 目录、直接文件。

```bash
bash verify_toolchain_identity.sh
bash verify_toolchain_identity.sh /opt/tizen-llvm/usr
bash verify_toolchain_identity.sh /usr/bin/clang++ --expected-sha256 "$RELEASE_CLANG_SHA256"
# 不执行版本查询，只静态检查；wrapper 会自动采用这种保守行为并返回 2：
bash verify_toolchain_identity.sh --no-exec /path/to/compiler
# 仅本机解包 Tizen ELF 时使用显式 loader，不安装依赖：
bash tools/verify_toolchain_identity.sh --loader /lib64/ld-linux-x86-64.so.2 \
  --library-path "$W/temp/toolchain-runtime-baseline/libxml2/usr/lib64" "$TC"
```

输出版本全文、SHA256、ELF machine、BOLT 特征和 notes、选中/解析后路径的 RPM 查询。
`--expected-sha256` 与可信清单匹配才输出 PASS。退出 0 仅表示检查完成，不代表自动批准
工具链；1 为期望 SHA 不符；2 为参数/查询错误或检查不完整。无 RPM 归属及缺少 rpm
保留原始原因，不将它们改写成“官方版”。wrapper 不自动执行，也不尝试猜测其下一层。

本轮实测：RPM 基线 `BOLT_FEATURES=NOT_OBSERVED`；BOLT 文件
`BOLT_FEATURES=PRESENT (.note.bolt_info)`；两个 expected SHA 都 PASS。
15/15 功能检查通过，包括大小写 SHA、错误 SHA、默认 PATH、根/bin/直接文件、带空格
符号链接、目录内 symlink 越界拒绝、缺文件/缺工具、wrapper 不执行。宿主默认 PATH 实际没有 clang，默认调用
如实返回 2；默认分支另用显式测试 PATH 验证。原始结果 A/identity-*.txt、
identity-tests.json、test-*.txt。测试输入和代码仅在 A，不提交。

## 2. spec 集成设计（以下均未实施）

### 2.1 集成位置、CMake 与四步处理

只对 `%ifarch x86_64` 的 opt-in `with_clang_bolt` 路径启用。其他架构及
`without_clang_bolt` 仍走原配方。保持 O3、ThinLTO、静态链接、断言、MLGO 和并发
4/4/1、debuginfo -j4 不变；不导入上游整个 BOLT.cmake cache，因为它会改项目、目标和训练流程。

**构建工具来源：** 当前 spec:260 的 LLVM_ENABLE_PROJECTS 没有 bolt。
B/bin/llvm-bolt 是 docs/15 实验增量产物，不能直接把本机绝对路径写进 spec。
第一版建议先提供同源码版本、固定 NEVRA/哈希的 **builder 专用 BOLT tools RPM**，
在 Quickbuild 构建环境内提供 llvm-bolt；它不是 clang 的运行时依赖。
若选单 spec 自包含方案，应把 projects 扩成
`clang;lldb;clang-tools-extra;lld;compiler-rt;openmp;bolt` 并补全 `%files`/安装策略；
这会新增构建/打包范围，不能只加参数而忽略未打包文件。该方案不作为本设计首选。
原增量实测能证明工具可构建，不能证明未来全包新配置已经通过容量门禁。

#### 步骤 1：保留重定位

在 `%build` 的 cmake 调用（spec:218），对现有 EXE flags（spec:231）**追加**：

```text
-DCMAKE_EXE_LINKER_FLAGS="-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections -Wl,--emit-relocs"
```

作用范围是该 CMake 工程所有使用此变量的**可执行目标**，**不只 clang**；会给 lld、
llvm-ar 等增加链接重定位元数据。不修改 CMAKE_SHARED_LINKER_FLAGS（spec:230），
因此没有要求共享库也保留 reloc。本地例子 `llvm/clang/cmake/caches/BOLT.cmake:3–4`
区分这两类参数；语义见 [CMake EXE flags](https://cmake.org/cmake/help/latest/variable/CMAKE_EXE_LINKER_FLAGS.html)
与 [SHARED flags](https://cmake.org/cmake/help/latest/variable/CMAKE_SHARED_LINKER_FLAGS.html)。
这里使用既有 `-Wl,` 语法，不引入新版 CMake 才有的变量中 `LINKER:` 语法。

第一版**重写范围仅 clang**，但该 CMake 方案的“保留 reloc 范围”较大，应在试包中检查
其他工具最终大小、NEEDED、hash 和 `%files`，不能谎称它们的文件完全没变。
若要求连保留 reloc 都仅影响 clang，替代设计是 docs/14 已验证的单 clang 链接命令重放：
读取 `ninja -t commands clang` 的最终链接命令，保留响应文件、cwd、ThinLTO 参数，
只追加 `-Wl,--emit-relocs` 并把 `-o` 指向独立文件。这不是一个所谓
`-DCLANG_LINKER_FLAGS` 开关，本轮未找到该开关。它增加一次热缓存重链，需独立日志和
容量预算，后续实施时二选一，不能同时全量链接后又无故重链。

#### 步骤 2、3：独立输入剥离与优化

在 spec:363 原 ninja 完成后执行可选阶段，使用 `$PWD/bin/clang-22` 的完整 ELF，
先把原件哈希、节区、CMakeCache、链接命令归档，再创建独立目录。以下是**拟议命令**：

```bash
# 位于 build/；BOLT_TOOL 是构建环境提供的固定版本 llvm-bolt。
# PROFILE 是经清单/hash验证的 fdata；work 在 BUILD 中，绝不覆盖 bin/clang-22。
work="$PWD/bolt-stage"
mkdir -p "$work"
"$PWD/bin/llvm-objcopy" --strip-debug "$PWD/bin/clang-22" "$work/clang.input"
readelf -SW "$work/clang.input" > "$work/input.sections"
# helper 检查 .symtab 非空、.rela.text 和非调试 REL/RELA 保留后，进入受限子阶段：
"$BOLT_TOOL" "$work/clang.input" -o "$work/clang.candidate" -data="$PROFILE" \
  -reorder-blocks=ext-tsp -reorder-functions=cdsort \
  -split-functions -split-all-cold -split-eh -dyno-stats --thread-count=1
```

上面两个写文件命令必须由 2.3 的资源隔离 helper 执行，不能直接在无上限环境运行。
不传 `-instrument`，不采新 profile；也不加 `CLANG_BOLT=INSTRUMENT`。
`--strip-debug` 不是 `--strip-all`：要求保留代码/数据对应 `.rela.*` 和 `.symtab`。
调试段自己的 `.rela.debug_*` 会一起删除，这是已测行为，不能要求这些重定位也保留。
Q/strip-audit/result.json 已证非调试 ALLOC payload 不变；符号编号重排不要求整个 symtab
哈希不变。具体优化选项与 E16/optimize/stage.json、源码 README:212 完全相同。

#### 步骤 4：安装、打包与身份清单

`%install` 首先保持 spec:367 的原 cmake_install，以及 :368–378 的别名和 clang.cfg
生成。仅在候选通过 2.3 的检查时，在 **%install 末尾、RPM 自动 post 之前**，用同目录
临时文件 + rename 替换 `%{buildroot}/usr/bin/clang-22`。原 build/bin/clang-22 不动；
clang/clang++ 等应仍解析到唯一这个 ELF（源码 clang/tools/driver/CMakeLists.txt:83）。
失败则不触碰安装好的原 clang，也不复制部分 BOLT 输出。

新增 `%files -n clang` 条目（当前起于 spec:539）建议为
`%{_datadir}/tizen-llvm/toolchain-identity.json`，保存：

- schema、配方/source commit、spec/config hash、构建器 NEVRA、原 ELF hash；
- BOLT 工具 hash、profile ID/hash、完整参数；`bolt_requested`、`bolt_applied`；
- 状态 APPLIED / FALLBACK_NO_PROFILE / FALLBACK_PROFILE_MISMATCH /
  FALLBACK_TOOL_UNAVAILABLE / FALLBACK_RESOURCE / FALLBACK_REWRITE / FALLBACK_VALIDATION；
- 调试策略 `clang_dwarf=absent` 或 `updated_and_verified`，匹配性统计、失败原因与日志定位。

**最终 ELF hash 必须在 find-debuginfo/brp 之后生成**，否则它只是打包前 hash。
推荐 `%check` 中只读检查处理后的 BUILDROOT，写最终清单，再由发布端对实际 RPM 解包
复核。RM:898–901 证明自动 debug/install post 会运行；实现时还要对发行环境确认
`%check` 被执行，禁用 `%check` 的包不能通过发布门禁。外部发布清单同时记录 RPM hash
和解包后每个 ELF hash，避免一个包含自身哈希的清单造成循环依赖。
当前 RPM 源码 `J/rpm-source/rpm-4.14.1.1/build/build.c:247–264` 的顺序为
install 脚本、check 脚本、processBinaryFiles，支持上述清单生成位置。

当前两份 ELF 都无 GNU build ID；不能承诺 rpm 会替缺失 note 自动生成它。将来如启用
build ID，必须检查它与**最终** ELF/debug 文件配对，不能让旧 debuglink/build-ID 映射
指向已改地址的 clang。当前路径优先依赖最终 SHA256，不复用原 `.gnu_debuglink`。

#### 已有阶段实测与“增量”边界

| 阶段 | 已有 wall | 已有内存 | 能推出什么 / 不能推出什么 |
| --- | ---: | --- | --- |
| 单 clang 带 relocs 热 ThinLTO cache 重链 | 227.656 s（阶段） | lld VmHWM 9.760868 GiB；scope peak 10.451344 GiB | docs/14 实测；若首次链接直接加参数，就不能把这 227.656 s 当必增量；与无 relocs 的同条件差值 UNKNOWN |
| objcopy --strip-debug | 命令 2.31 s；阶段 4.166983 s | time-v Max RSS 4,507,492 KiB = 4.298679 GiB；scope peak 2,921,844,736 B | Q/strip/tool-time-v.txt、outcome.json；两种峰值口径不同，不相加 |
| 纯 BOLT 优化重写 | 命令 21.83 s；阶段 22.271900 s | 自身 3.481499 GiB；scope 3.416550 GiB | docs/16 第 5 节、E16/optimize；只适用于剥离输入与此次 profile，**不是带 DWARF 更新的上界** |
| 原完整包 debuginfo -j4 | 14:51 | 30 秒进程树 RSS 观察峰值 5.896049 GiB；clang eu-strip VmHWM 3.209354 GiB | docs/13 第 9 节、J/run；没有做 BOLT RPM，本次设计对这一阶段的耗时/内存增量 UNKNOWN |
| 若改用工程内补建 BOLT 工具 | configure 26.426 s；126 项构建 545.525 s | scope peak 分别 627,392,512 / 4,907,880,448 B | docs/15 第 3.1 节；推荐预置 builder tools，因此这不是每次使用存档 profile 的重写成本 |

不能把不同时刻的峰值相加成必需 RAM，也不能把 ELF 文件大小当成 BOLT 或 clang RSS。
本文没有补跑任何阶段来填 UNKNOWN。

### 2.2 profile 的存放、版本与旧 profile

现有文件：`E16/profile-work/merged.fdata`，**153,887,224 字节**，SHA256
`d8b6c9146822fbe19ce0c3646d57d17e797d865100a7b0193562db6ea371c24d`。
原始训练输入/flags、工具与 manifest 跟随档案。大文件不进本仓库。

| 方案 | 具体做法 | 优点 | 缺点与缺失时处理 |
| --- | --- | --- | --- |
| Source/tarball（推荐首版） | 发布 profile tarball + manifest；可放 Source0 内独立可选目录，或有条件的 Source1005 | 与源包一起归档，离线可复现，评审能钉 hash | 增加约 154 MB 未压缩材料；压缩后大小未测；单独 Source1005 若根本取不到，会在 `%prep` 前失败，需上层预检切回不含该 Source 的构建配置 |
| 独立 noarch profile RPM | 例如提案名 `llvm-bolt-profile-clang22`；路径 `/usr/share/llvm-bolt-profiles/<profile-id>/merged.fdata`，固定 NEVRA/hash | 多个构建复用仓库缓存；独立发布/回滚 | 新增供应链与源包外依赖；不能只依赖滚动 latest；若设为无条件 BuildRequires，缺包会在 spec 运行前失败，违反自动降级目标 |
| 构建服务器固定路径 | 只读挂载 `/srv/toolchain-profiles/<profile-id>/...`，每次校验 manifest/hash | 部署快，不扩大 SRPM | 只钉目录名不等于可复现，异机/离线缺失；必须归档真实内容、禁止原地更新，缺失立即走普通包 |

**推荐落地：** profile + manifest 作为可选目录随 Source0 归档，未提供则该目录缺失，
脚本能安全降级；若用独立 Source，Quickbuild 入队前检查完整性，失败时选择
`without_clang_bolt` 源包/宏组合，不能指望 shell `test -f` 修复 RPM 前置 Source 校验。
BOLT builder tools 同理：可选预置且校验，不添加不可解析的无条件 BuildRequires。
若团队要求所有构建依赖强声明，则维护有/无 BOLT 两个条件依赖集合，由入队预检选择。

profile manifest 至少钉：LLVM source/patch/spec 身份、x86_64 宿主架构、关键 CMake/MLGO
配置、relocs输入 SHA、BOLT 工具/格式、训练 corpus hash/flags/triple/资源目录、新旧 profile
ID 和完整 fdata hash。注意**被重写的是 x86_64 clang**，训练任务的目标可以是 ARM。
数字版本 `22.1.8` 相同并不保证同一个代码图。

旧 profile 并非一改源码就绝对不能用，也不能默认兼容：

以下文件简称分别为 `llvm/bolt/lib/Profile/DataReader.cpp`、
`llvm/bolt/lib/Passes/BinaryPasses.cpp`、`llvm/bolt/lib/Profile/StaleProfileMatching.cpp`。

- `llvm/bolt/README.md:220–227` 明确支持输入非完全相同，但要求关注 stale；
  DataReader.cpp:409 先找函数数据，对易变名称可重新匹配；`:510` 验证分支/偏移。
- BinaryPasses.cpp:1487 区分有效、无效 profile；`:1536–1564` 输出 stale 函数与样本比例。
  `--stale-threshold` 默认 **100**（`:211`），所以 exit 0 不代表匹配良好。
  本次使用 branch profile reader（E16/optimize/build.log:11），不能拿 YAML-only
  function hash 检查冒充本次格式的校验。
- `--infer-stale-profile` 默认关闭（StaleProfileMatching.cpp:50），首版不加自动推断绕过。
  378 个 “with profile could not be optimized” 来自 non-simple 函数计数
  （BinaryPasses.cpp:1466、1531），**不是“378 个 stale”**。

发布策略：source/优化配置/BOLT版本变更即失配，默认回退并请求 profile 重新认证；
并非只比 fdata 文件存在。重建导致 ELF hash 改变但语义配置相同，也需一次资格验证，
不能强令每个可复现性尚未验证的构建都与本机历史 ELF hash 相同。
首版资格验证要求非零有效 profile、stale=0、未匹配/non-simple/relocation 告警与已审核
日志基线相符、20 TU 一致性通过；新增告警或未识别日志格式先回退。这里的阈值是拟议
验收政策，不是声称 BOLT 默认严格拒绝失配。发布分支升级、MLGO/链接配置变化、训练
负载代表性改变时更新 profile，profile 自身发布使用不可变 ID。

### 2.3 降级与 OOM 隔离

**目标是可选 BOLT 失败仍产出普通包，不吞掉原 LLVM 构建错误。** 保留原 ELF 和原安装
流程，只在所有条件满足后提升候选。下面是控制流设计；函数名是后续实施 helper 的接口，
不是当前仓库已经存在的命令：

```bash
bolt_state=FALLBACK_NO_PROFILE
if profile_manifest_matches && bolt_tool_matches && isolated_worker_available; then
    if run_isolated_strip_and_rewrite; then
        if candidate_elf_and_profile_checks; then
            bolt_state=CANDIDATE_READY
        else
            bolt_state=FALLBACK_VALIDATION
        fi
    else
        # 根据 command.exit / memory.events 区分 RESOURCE 和 REWRITE。
        bolt_state=$(classify_failure)
    fi
fi
# 原 ninja 和原 cmake_install 自身仍正常检查错误，不使用全局 `|| true`。
# 在 %install 末尾：
if [ "$bolt_state" = CANDIDATE_READY ]; then
    if install_candidate_to_sibling_temp && verify_staged_candidate; then
        # 同一文件系统 rename；发布前发生任何失败都还保有原文件。
        if atomic_promote_candidate; then bolt_state=APPLIED
        else bolt_state=FALLBACK_VALIDATION; fi
    else bolt_state=FALLBACK_VALIDATION; fi
fi
write_identity_manifest_and_preserve_logs
```

具体契约与测试判据：

1. 隔离对象包含 objcopy 和 llvm-bolt，可顺序运行；分别保存 time -v、VmHWM、
   memory.events、memory.peak、命令退出码、输入/输出 hash，失败候选保留在 BUILD 日志目录。
   无 profile、坏 hash、工具缺失、资源隔离不可用时，**尚未执行重写就返回可解释降级状态**。
2. Quickbuild executor 需提供委派 cgroup v2 子组：父 rpmbuild 留在外面，BOLT/objcopy
   全部子孙进入子组；子组内存上限低于整个构建限额，MemorySwapMax=0。建议试集成时
   子组从 **8 GiB** 作为可配置试验上限开始：这是给已测 4.30/3.48 GiB 留余量的
   **设计值，不是已测充分上界**；不足即降级。全 LLVM 的既有 18 GiB 门禁本轮不改，
   不把本轮设计新参数伪装成已通过“同构”容量认证的配置。
3. 有 user manager 且确实委派时，可由 executor 使用
   `systemd-run --user --scope -p MemoryMax=8G -p MemorySwapMax=0 ...`；
   **不能在 chroot 内盲目假定 systemd/user bus 可用，也不能把 sibling scope 当作父构建预算内子组。**
   优先由 executor 在构建 cgroup 内建子组并校验实际 membership/限制；做不到就跳过 BOLT。
   本轮没有 Quickbuild 权限/配置证据，该能力 UNKNOWN，需实施前验证。
4. 保留 nice 15、ionice idle、每 30 秒 free/loadavg/进程树 RSS、低可用内存中止 BOLT、
   EXIT/INT/TERM trap 回收采样器。OOM 测试必须证明被杀的是可选工作进程，父 rpm 存活；
   只写一个 `if llvm-bolt ...` **不足以防止全局/父 cgroup OOM 杀掉 rpmbuild**。
5. candidate 检查包括有效 x86_64 ELF、执行版本查询成功、BOLT note/配置身份、资源目录、
   NEEDED 未引入 LLVM 共享库、profile 匹配审核以及代码生成烟测；最终完整 20 TU 门禁见 2.6。
6. 需在实施时做负对照：删/损坏 profile、错源码清单、缺工具、模拟非零退出、
   小子 cap 注入 OOM、输出截断、磁盘写失败、替换失败。每种均检查普通 RPM 可产出、
   无部分文件覆盖、manifest=FALLBACK、采样器已退出。APPLIED 路径检查最终 RPM 解包身份。

这不能保证整机断电、磁盘彻底耗尽、原 LLVM 编译失败时也必产包；承诺范围是**隔离且
可捕获的可选 BOLT 阶段失败**。正常 LLVM/打包仍受既有限额。上层耗尽所有资源不能靠
隐藏退出码解决。降级 RPM 可交付普通构建，但必须从 BOLT 性能验收队列排除。

### 2.4 debuginfo：试验包与正式发布分开

**没有更新的原 DWARF 不能用于已改地址的 BOLT clang 源码级崩溃分析。**
行表、地址范围、内联栈/位置表达式可能对应错误地址，不能复用 TC 的 debuglink/debug 包。
BOLT 的符号和 unwind 段与源级 DWARF 是不同东西；保留符号不等于保留行号、变量和内联信息。
现有 BOLT ELF 实测有新的 `.eh_frame`、符号表，是否覆盖所有异常/回溯场景仍需验收。

源码依据：RewriteInstance.cpp:2207 在不更新 debug 时警告剥离；`:4833` 真正剥离；
`llvm/bolt/lib/Utils/CommandLineOpts.cpp:301` 定义 `--update-debug-sections`。
**对已 strip-debug 的输入加该选项，不能恢复已经删除的 DWARF。**

推荐两阶段：

- **Quickbuild 试验首版：** 延续已测 strip-debug → BOLT。仅这个 clang 明确无 DWARF，
  其他工具仍按原 find-debuginfo -j4 提取。FD:389–399 按 objdump 节区选输入，遇到无 debug
  而有 gnu.version 会提示 already stripped 并跳过；本次 BOLT ELF符合该形状。
  不全局关闭 `%debug_package`，不关闭其他工具的 debuginfo，也不重用原 clang 的 `.debug`。
  在全新 BUILDROOT/RPM 构建中确认 clang-debuginfo 不包含该 ELF 的陈旧映射；它仍可包含
  clang 包内其他文件的调试信息，包名存在不等于 clang-22 可源级调试。
- **正式发布优先：** 从完整 relocs ELF 运行同一组优化参数再加
  `--update-debug-sections`，随后才走 find-debuginfo。需先补一次有上限的实验：
  记录自身 VmHWM/wall/cgroup、输出 DWARF/重定位完整性；抽查热/冷拆分函数、内联栈、
  异常栈的 gdb/addr2line 回溯，RPM 解包后再次验证 debuglink/build ID 配对，并做 20 TU
  门禁。**该路径时间、内存和最终可调试性当前 UNKNOWN**；超限或校验不通过则产普通包。

上游 README:215 的文字不能替代本项目测量。现有 3.56 GB 完整 ELF → 226.7 MB
剥离输入与“带 DWARF 更新”的内存形状不同，不承诺后者能装进 18 GiB。
部署试验 RPM 时，应同步处理匹配的 debuginfo 包集合，避免服务器残留旧 clang .debug
导致误导；归档原工具链及其匹配 debug RPM 用于回滚，不能用它解释 BOLT 的新地址。

### 2.5 第一版范围

仅优化原生 x86_64 clang-22，clang/clang++/triple 别名指向同一文件。当前 profile 来自
clang 执行，不能直接拿来优化 lld/llvm-ar。Chromium 链接仅占 0.2% 是既定的该包形状，
不是排除所有其他工具的依据；普通 RPM 的链接、归档及 debuginfo 成本还需代表性数据。
后续如覆盖 lld/ar，应各有训练负载、profile、输入/输出正确性与整包收益验收。
本轮没有测这些工具的 BOLT 收益，不能宣传“整套工具都提升 14–15%”。

### 2.6 其他包的代码生成与并发内存

集成后继续设置红线：用**同一次构建、相同 vendor、相同资源目录/ARM sysroot/flags、
同 driver 模式**的原 clang 与候选编译全部 20 个训练+留出 TU，完整 `.o` 做 cmp/SHA256；
保留 `-frecord-gcc-switches`，不跳过任何节区。建议以 `clang-22 --driver-mode=g++`
统一调用。该门禁应再对**最终 RPM 解包文件**执行，以覆盖打包后的变化；运行机必须有
归档的 .ii、flags、资源头和必要 sysroot。CI 中先做版本/目标/小 C/C++ 烟测，完整数据集
在发布/Quickbuild 验收 worker 做；未通过不得标为验收成功，不能只引用历史 20 对 PASS。
任何对象不一致为 BLOCKER，停止发布 BOLT 候选，使用普通包；不通过修改比较方法消除差异。

**需要报备的体积变化：** 已有 clang 139,929,464 → 215,899,856 字节，增加
75,970,392 字节 = **72.451 MiB（54.292%）**。这是两个现存文件的实测，不是未来 RPM
压缩体积或 RSS 的估计；两者剥离方式还不同，最终 RPM 大小必须重新记录。

读取既有 docs/16 formal.json 得到下列资源观察，**没有新跑基准**。表中为丢首样后的
max RSS（KiB），由 harness 的 `wait4(...).ru_maxrss` 记录，见 tools/bench_toolchain.py:221、239；
不是整机并发内存，也不是优化重写进程的 3.48 GiB。

| 历史负载 | RPM 基线 max RSS KiB | BOLT max RSS KiB | 基线 / BOLT 中位 wall s |
| --- | ---: | ---: | --- |
| A | 1,040,532 | 1,023,764 | 8.297694 / 7.332046 |
| B | 149,252 | 125,788 | 2.201669 / 1.681161 |
| C | 1,188,748 | 1,165,452 | 5.901407 / 5.679014 |
| ARMISelLowering | 619,888 | 590,064 | 8.191364 / 7.029427 |
| SemaExprCXX | 691,760 | 661,744 | 5.991850 / 4.921860 |

原数据 `W/temp/bench_results/bolt-final-20260918/formal.json`；完整 13 行提取在
A/historical-rss.json。本次观察没有显示“文件变大就每个编译进程按等量增加 RSS”，
但也不能据此保证 Chromium 并发不会增加内存。相同 ELF 的只读代码映射可以由进程共享；
各进程的私有分配、实际触达热页和页缓存不同。不能用“并发数 × 整个 ELF 大小”推算。

服务器应同时记录构建 cgroup memory.peak/memory.stat、进程树 RSS、代表时刻各 clang 的
`smaps_rollup` PSS/Private_*、major faults、swap/oom 事件、并发数。RSS 求和会重复计共享页；
cgroup/宿主可用内存用于判断真实压力。**Chromium 高并发总内存变化 UNKNOWN**，
先保持 A/B 并发相同，不因局部提速擅自提高并发；若新增 OOM、swap 或明显容量恶化，
单列为验收阻塞/资源需求，不把它隐藏在平均耗时内。

## 3. Quickbuild 服务器验收操作

### 3.1 准备与替换检查

以下是服务器执行方案，本机未执行。Quickbuild 的项目名、入库/安装权限、worker 类型与
完整构建入口本工作区无证据，**不虚构专用 CLI**；由现有项目操作者填入其已使用的
完整构建命令/参数。命令模板使用 Bash 数组，不用 eval。

1. 为一次试验固定 source/spec/patch、GN args、ARM sysroot、clang 22 资源目录、依赖包
   快照、构建器、目标、Ninja 图及并发。保存 A/B RPM 集与可信 manifest，各标普通/BOLT状态。
   回滚也切换匹配的一组子包，不能混装不匹配的版本依赖。
2. 在**独立 Quickbuild worker/buildroot** 中按平台现有仓库/镜像机制部署候选 RPM，
   不替换生产 worker 或只手工拷一个 ELF。安装前 `rpm -K`、`rpm -qp` 和外部 sha256 清单
   核对来源；如缺签名则按项目的可信制品校验流程处理，不把有 checksum 说成已签名。
3. 两组使用同一 GN toolchain 路由，先确认选择平台 clang，非 bundled clang 18。
   不在 B 组才改变 GN 编译配置或资源头。每个会执行编译的 worker 都运行身份脚本；
   ARM accel 环境同时检查实际 `/emul/.../clang-22`。只有调度节点 PATH 正确不算通过。
4. 先完成最终 RPM 的 20 TU 逐字节门禁与必要 Chromium 测试，再做耗时验收。
   FALLBACK 包是普通包，可以构建，但不得进入 BOLT 样本。

单轮证据准备（把下列输入填成该项目已有值；在 source 根下执行）：

```bash
# 必填：本轮唯一目录；真实 GN 输出目录；本项目完整构建命令（完整 RPM 或 Ninja 层）。
EVIDENCE=/server/evidence/llvm-bolt/A1
OUT=/server/chromium/out.actual
BUILD_COMMAND=(/path/to/the/existing/build-entry --its-existing-arguments)
CC_REAL=/actual/worker/path/to/clang-22
EXPECTED_CLANG_SHA256='替换为可信发布清单中的64位hash'

mkdir -p "$EVIDENCE"
date -Ins > "$EVIDENCE/start-preflight.txt"
nproc > "$EVIDENCE/nproc.txt"
free -b > "$EVIDENCE/free-before.txt"
cat /proc/loadavg > "$EVIDENCE/loadavg-before.txt"
ps -eo pid,ppid,rss,args --sort=-rss > "$EVIDENCE/processes-before.txt"
printf '%q ' "${BUILD_COMMAND[@]}" > "$EVIDENCE/build-command.txt"
printf '\n' >> "$EVIDENCE/build-command.txt"
git rev-parse HEAD > "$EVIDENCE/source-head.txt"
git status --porcelain > "$EVIDENCE/source-status.txt"
git diff --binary > "$EVIDENCE/source-working.diff"
rpm -qa --qf '%{NAME} %{EPOCHNUM}:%{VERSION}-%{RELEASE}.%{ARCH}\n' | sort > "$EVIDENCE/packages.txt"
cp "$OUT/args.gn" "$EVIDENCE/args.gn"
# Ninja 查询不构建。展开 cc/cxx/response-file 所需信息全部保存。
ninja -C "$OUT" -t commands > "$EVIDENCE/ninja-commands.txt"
ninja -C "$OUT" -t rules > "$EVIDENCE/ninja-rules.txt"
find "$OUT" -name '*.ninja' -type f -print0 | sort -z | xargs -0 sha256sum > "$EVIDENCE/ninja-files.sha256"
grep -nE 'clang(\+\+|-22)?([[:space:]]|$)|(^|[[:space:]])(cc|cxx) =' \
  "$EVIDENCE/ninja-commands.txt" > "$EVIDENCE/compiler-command-excerpts.txt" || true
bash verify_toolchain_identity.sh "$CC_REAL" --expected-sha256 "$EXPECTED_CLANG_SHA256" \
  > "$EVIDENCE/compiler-identity.txt" || exit 1
"$CC_REAL" -print-resource-dir > "$EVIDENCE/resource-dir.txt"
"$CC_REAL" -dumpmachine > "$EVIDENCE/default-triple.txt"
# 若 OUT 尚未生成，应把以上 GN/Ninja 查询放在该项目生成图之后、首次编译之前的 hook。
```

这里的 hash 字符串是文档占位符，执行前必须替换为真实的 64 位 hash。
还需复制相关 toolchain.ninja、响应文件及编译命令引用的 `.cfg`；保存已解析的实际
`--target`、`--sysroot`、`-resource-dir`（default-triple 不是命令覆盖后的 target）。
从 ninja-commands 找到 compiler 后按 **OUT 的 cwd** 解析相对路径，不能用 source 根
错误拼接。有 ccache/goma/accel/远程执行时要继续追踪到最终 worker 的 ELF；必要时在
一次非计时编译诊断中用 exec trace 确认，正式计时不附加 strace。路径无法确认则该轮无效。

采集资源目录与 sysroot 的快照/内容 manifest；不能只记录路径相同就当内容相同。
GN 图应比较规则、输出边与完整 flags；A/B 若只因编译器安装路径不同造成字节 hash变化，
记录该唯一允许差异后再做规范化比较，不能忽略其他图变化。

### 3.2 执行与数据保全

使用既有项目的**全量构建入口**。每轮先由项目标准 clean/重新展开源码步骤恢复同一
干净状态，在同一工作路径生成同一图；严禁 B 组复用 A 组已编译对象成为增量构建。
compiler cache/远程 cache 全部关闭或给两组相同、明确的冷/热策略，并保存命中统计；
不得 A 冷 B 热。不要用全局 drop_caches 改变同机其他任务。

```bash
set -o pipefail
/usr/bin/time -v -o "$EVIDENCE/time-v.txt" "${BUILD_COMMAND[@]}" 2>&1 \
  | tee "$EVIDENCE/build.log"
status_pair=("${PIPESTATUS[@]}")
printf 'build=%s tee=%s\n' "${status_pair[0]}" "${status_pair[1]}" > "$EVIDENCE/exit-status.txt"
cp "$OUT/.ninja_log" "$EVIDENCE/ninja_log"
cp "$OUT/args.gn" "$EVIDENCE/args-after.gn"
cat /proc/loadavg > "$EVIDENCE/loadavg-after.txt"
free -b > "$EVIDENCE/free-after.txt"
# 把 executor 提供的本轮 cgroup 路径记入记录：
for metric in memory.peak memory.events memory.stat cpu.stat io.stat; do
  cat "$BUILD_CGROUP/$metric" > "$EVIDENCE/$metric"
done
bash verify_toolchain_identity.sh "$CC_REAL" --expected-sha256 "$EXPECTED_CLANG_SHA256" \
  > "$EVIDENCE/compiler-identity-after.txt" || exit 1
```

`BUILD_CGROUP` 是该轮 executor 实际分配的 cgroup，不是随意取宿主根 cgroup。
从开始到结束每 30 秒保存 free/loadavg、进程树 RSS、memory.current，采样器使用 trap
回收；包装器只负责记录，不修改现有构建命令。若完整 RPM 流程会删除 OUT，把复制
.ninja_log/args/GN 图的 hook 放在删除前。time-v 的 max RSS 不是并发全部进程的和，
cgroup 应每轮新建/清零基线，避免读到前一轮的 peak。若父服务先退出、编译在远端异步
运行，time-v 包装提交命令不能代表总 wall，改取 Quickbuild job 的实际开始/完成时刻。

至少做交错次序 **A1 B1 B2 A2**，条件允许再做 A3 B3，固定机器/核绑定/并发/频率策略；
每次完整独立构建，记录开始/结束、宿主竞争负载、磁盘/网络和缓存状态。规则在看结果前
确定，失败/高负载样本保留并按同一规则重跑，不能只挑最快的一轮。

### 3.3 可比指标与收益判据

| 指标 | 定义与可比条件 | 注意事项 |
| --- | --- | --- |
| 总 wall（主验收） | 同机同资源的完整 Quickbuild job / 同一全量构建区间 | 排队/下载等待另列；只计 ninja 时只能称编译构建 wall，不能称完整 RPM job wall |
| 单位编译成本（主要诊断） | `.ninja_log` 中实际编译 edge 的 `(end-start)` 总和 / 同样的编译任务数 | 用展开命令中的 `-c`、输出与规则映射分类，不把链接/归档算编译；这是 edge wall，不是 CPU user 时间 |
| 编译成本分布 | 对同一个 TU 配对比值、中位数/几何平均及分位数，分 C/C++/子系统 | 处理 Ninja 日志多输出同一 edge、重跑/追加记录：每轮干净日志，按 edge 去重，不能按日志行数盲算 |
| 链接、归档、打包 | 分阶段 edge/job 数据单列 | 未修改阶段可作环境漂移参照；不同 Chromium 图与普通包不能直接套比例 |
| CPU/内存/IO | user/sys、cpu.stat、memory.peak、PSS、major faults、swap、IO | 记录统计范围；wall 下降不保证 CPU 或内存等比例下降 |
| 正确性 | 20 TU 完整 `.o` 一致、全量构建成功、既有 Chromium 测试通过 | 对象不一致或功能失败直接 BLOCKER，不以性能弥补 |

本项目教训是跨轮次绝对耗时可漂移，单位编译成本在受控同图下更稳定，但也受竞争影响。
不能拿 docs/13/16 本机历史绝对值充当服务器 A 组；也不能把所有 edge 时间相加当作总 wall，
因为并行任务区间重叠。当前筛选收益边界仅 LLVM 源码编译负载，最终结论针对实际验收平台。

**预先约定的判定标准：** 身份与配置/图/工作量一致、正确性门禁通过、无新增 OOM/swap
或不可接受容量回退是前提。在交错的多次完整构建中，配对 B/A 的总 wall 持续小于 1，
差异超过这些整轮配对的环境波动（足够重复后给整轮比值的不确定性区间；不能把数万个
相关 TU 冒充独立整轮样本），且单位编译成本同向改善，才认定 Quickbuild 收益成立。
若仅单位编译成本改善、总 wall 落在波动内，结论为“编译改善已观察，总构建收益未确证”；
若身份未替换或是 FALLBACK，本轮不属于 BOLT 对照。**不预设服务器必须达到 14–15%。**

## 4. 未知项、实施门禁与本轮自检

| UNKNOWN | 当前原因 | 后续需要 |
| --- | --- | --- |
| 全平台版本字符串解析兼容性 | 仅查到本地源码/CMake/GN/部分日志，缺所有包的 configure | vendor 试包的 configure/依赖/ABI 烟测；故 suffix 保持空 |
| 最终 BOLT RPM 大小、hash、note/debuglink 保留情况 | 目前 BOLT 文件不是 RPM，本轮只设计 | 实施后从真正 RPM 解包重跑身份/节区/20 TU 门禁 |
| 全局 emit-relocs 相对原链接的纯耗时/内存增量 | 只有热缓存单 clang 重链，非同条件成对链接 | 首个集成构建日志与原配置对照；不猜增量 |
| update-debug-sections 的耗时、峰值与可调试性 | 现有成功重写输入已剥离 DWARF | 完整 relocs ELF 的受限实验 + RPM 后 gdb/addr2line 验证 |
| Quickbuild cgroup 委派、包部署入口和真实 cc/cxx | 无服务器现场，给定 Chromium 输出路径本机不存在 | 在实际 worker 验证；隔离不可用就普通包，不假装 fail-open 已可靠实现 |
| Chromium/全平台 wall 与并发内存收益 | 本机筛选不能代表服务器全量负载 | 执行第 3 节，不再追本机噪声门禁 |

提交前自检：

1. **spec、LLVM 源码是否修改？否。** spec/GBS 配置/完整构建脚本/18 GiB 容量清单 hash
   与起始一致；源码仓库仍只有原来三处并发差异。
2. **是否跑校准、基准台、采 profile、BOLT、PGO、完整 LLVM 或 Chromium 构建？否。**
   本轮仅源码/日志/ELF读取、`--version/-v/-dumpversion/-dM -E /dev/null` 查询与脚本测试。
3. **是否向 Gerrit 推送？否。** 仅提交本报告和身份脚本到 GitHub main。
4. **是否把预测输出当实测？否。** vendor/suffix 输出明确由源码推导；两个现有 ELF 的
   section/hash/version 是本轮实际查询；spec helper 与 Quickbuild 操作是待实施设计。
5. **身份脚本是否验证？是。** `bash -n` 及 15/15 功能检查通过；详见 A/identity-tests-final.txt。
6. **缺失 profile/OOM 会不会仍声称 BOLT 生效？不会。** 设计明确原件保留、隔离失败回退、
   manifest 记录 FALLBACK；该设计尚未实施，必须通过 2.3 的负对照后才可用于正式包。
7. **交付与原始数据在哪？** 仅 docs/18_spec_integration.md 与
   tools/verify_toolchain_identity.sh 提交；所有原始记录在
   `/home/linhao/Toolchain/development/llvm-optimize/temp/spec-integration-20260920/`。
   不包含大文件。发布后的提交号、push 输出、远端与 raw 内容 hash 核对保存在同目录
   publication.log / publication-verification.json，完成回复附所有 raw 链接和固定提交报告链接。

### 原始证据索引

A/commands.jsonl 记录本轮审计命令、时间与退出码；同名 txt 保存 argv 与原始输出。
核心文件如下：

| 文件 | 内容 |
| --- | --- |
| initial-state.txt、source-git-diff.txt、final-preservation.json | Git 状态与保护文件 hash |
| version-source.txt、source-context-final.txt、cmake-module-evidence.txt、local-version-parsers.txt | 版本标识源码和数字宏探测 |
| current-version-queries.txt、elf-inspection.json、rpm/bolt-sections.txt、rpm/bolt-notes.txt | 实际版本/宏/节区/notes/hash；`rpm/bolt-` 表示两份分别命名的文件，不是子目录 |
| spec-sections.txt、installed-rpm-hooks.txt、bolt-behavior.txt、profile-matching.txt | spec 插入位置、debuginfo 选择规则、BOLT 失配/剥离处理源码 |
| history-times.txt、remaining-design-evidence.txt、historical-rss.json | 既有资源实测读取与数据提取，无新测量 |
| chromium-discovery.txt、chromium-root-presence.txt、actual-compiler-search.txt、historical-compile-path.txt | Chromium 路径搜索和历史调用证据 |
| identity-rpm.txt、identity-bolt.txt、identity-system-default.txt、identity-tests-final.txt、identity-tests.json | 脚本实际输出及测试；首次测试的 hash 常量少字符报错保存在 identity-tests.txt，已修正测试输入 |
| baseline-package-metadata.txt、rpm-archive-identity.txt | 原 RPM 元数据与清单摘录 |
| publication.log、publication-verification.json | 提交、push、远端 HEAD、raw 内容一致性 |
