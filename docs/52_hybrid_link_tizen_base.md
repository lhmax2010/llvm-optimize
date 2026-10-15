# x86_64 混合链接：最新 tizen_base 补丁与配置级核对

2026-10-15；状态：**补丁与配置级核对完成，供 PM review；本次没有完整编译、安装、RPM 或运行时验证，也没有推 Gerrit/sandbox。** 原配方开关和三组静态选择符合核对结果；“除三组和五个例外外，链接命令完全不出现组件 `.a`”这一更强预期不成立，详见 §4。交付指南：[52_hybrid_link_validation.md](52_hybrid_link_validation.md)。

## 1. 基线、隔离与交付身份

- 从 `ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm` 无交互 fetch `refs/heads/tizen_base`，HEAD **`67619ec8bbbac7238a6cfc33a481ccfbcd12206f`**。356627 PS2 已 MERGED，且就是该 HEAD；356949 PS2 `a18ce53708d3b6ef596dcd27d0b51e18ce1db282` 仍 NEW，未合入。本补丁没有带入 356949。证据：[356627 查询](52_hybrid_link_evidence/gerrit-356627.json)、[356949 查询](52_hybrid_link_evidence/gerrit-356949.json)，各第 1 行。
- 独立仓库 `temp/hybrid-link-20261015/source`，本地分支 **hybrid_link**；提交 `cef4d90b478597e20ff105591af3c5f4417363f1`，作者/提交者 Hao Lin `<hao.lin@samsung.com>`，使用命令级 `git -c`，全局配置未改。主工作区 `llvm/` 和另一个会话的资产未改。
- 补丁：[52_hybrid_link.patch](52_hybrid_link.patch)，SHA256 **`30e90aa305dd1e5ae237adaa19b27996a722b53ef481aa8ba53f510cb3f9c678`**。
- 新建 `temp/hybrid-link-20261015/apply-check`，在干净基线上先 `git apply --check`，再实际 `git am`，两者 PASS；工作树干净，应用后的 tree 与候选完全一致：**`80a6fd231c4564a3b762f4ec288cf2c41f9d2e20`**。证据：[patch-identity.json](52_hybrid_link_evidence/patch-identity.json)、[fresh-apply.json](52_hybrid_link_evidence/fresh-apply.json)。
- 原始本地证据 E=`temp/hybrid-link-20261015`；报告引用的核心证据同步到 [52_hybrid_link_evidence/](52_hybrid_link_evidence/)。`gbs_llvm.conf` 是用户既有修改，SHA `28f1caf93cd39738a7da1e0da8d5f945f7372963bb9823a507f9157294272169`，未修改/提交。

仓库惯例是**直接提交源码**：`fd7a4929c0e4` 直接改 `llvm/CMakeLists.txt` 与 `TensorFlowCompile.cmake`；本基线 `packaging/llvm.spec:167–181` 的 `%prep` 是 `%setup` 加 MLGO assets 解包，没有 Patch 声明或 `%patch`。因此不额外引入 packaging patch 层。证据：[repository-convention.txt](52_hybrid_link_evidence/repository-convention.txt) 与补丁基线 spec。

## 2. 七文件补丁与范围

沿用 docs/21 附录 A.2、docs/22 已试构建的六个源码文件机制。六个文件最终 SHA 与旧 `hybrid-link-trial` 完全一致；本次重写 spec hunk，放在最新 spec 已有的 `%ifarch x86_64` 内。完整 diff 在补丁，七文件 SHA 在 patch-identity.json。

| 文件 | 改动 / 源码定位（补丁应用后） |
| --- | --- |
| llvm/cmake/modules/AddLLVM.cmake | `tizen_hybrid_llvm_interface`（1035 起）：只在开关开启、LLVM DYLIB 开启且目标为 STATIC_LIBRARY 时，将原 `LLVM` interface 替换为按最终消费者 `TIZEN_STATIC_LLVM` 选择的依赖 |
| clang/cmake/modules/AddClang.cmake | `llvm_add_library` 后调用上述 helper（110） |
| lld/cmake/modules/AddLLD.cmake | 同上（14） |
| clang/tools/driver/CMakeLists.txt | 42 起：仅 clang driver 目录关闭 CLANG DYLIB，声明 DISABLE_LLVM_LINK_LLVM_DYLIB，并给实体 clang 设置属性 |
| lld/tools/lld/CMakeLists.txt | 6 起：仅 lld 实体声明静态并设置属性 |
| llvm/tools/llvm-ar/CMakeLists.txt | 14 起：仅 llvm-ar 实体声明静态并设置属性 |
| packaging/llvm.spec | 281 起的 x86_64 分支：两项 LINK_DYLIB OFF→ON，加 HYBRID=ON、BUILD_SHARED_LIBS=OFF、LLVM_TOOL_LLVM_DRIVER_BUILD=OFF |

开关关闭时 helper 立即返回，三个 driver 的条件块不执行；§4 还实测与未打补丁的共享配置逐目标对比。ARM spec 不传本开关，默认未定义即 false。没有改 O3、ThinLTO、frame-pointer、MLGO、6/6/2、Source1005、归档转换、strip 或 `%files`。356627 Source SHA 仍 `6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557`（以 [packaging-invariance.json](52_hybrid_link_evidence/packaging-invariance.json) 的实际摘要为准）。

## 3. 三架构 RPM 展开

使用旧验证根的原生 x86_64 `rpmspec`，加载各架构根的完整 rpmrc/macros/abuild `.rpmmacros`，分别 `--target=x86_64/armv7l/aarch64`。通用宏：`--define '_smp_mflags -j4' --define '_srcdefattr (-,root,root)' --nosignature --define '_build_create_debug 1' --define '_topdir /home/abuild/rpmbuild'`；`_toolchain` 来自已有宏环境。未执行 `%build/%install`。完整命令 E/*-rpmspec-argv.json，完整展开 [证据目录](52_hybrid_link_evidence/) 中 `*-{baseline,hybrid}-build.txt/install.txt/cmake.json`。

| 架构 | 阶段 | 结论 | 基线 SHA256 | 补丁 SHA256 |
| --- | --- | --- | --- | --- |
| x86_64 | build | 仅 5 个链接配置参数差异 | 8841d6101457a190ffd34617fb3afc9583701e882a06360d758b3a02a26cb935 | 1ac35626e246fa501025c6a046d4c37ba3754053bdd9aa0a3fc465062a53bc50 |
| x86_64 | install | 同字节 | a0dc294e2991e73bee6341edacbfae9fb36ee95285791fcae7b8a4b269bdc9a3 | a0dc294e2991e73bee6341edacbfae9fb36ee95285791fcae7b8a4b269bdc9a3 |
| armv7l | build | 同字节 | 62ad7d2d21b45b8db5518c6e0906889a5acea2b7239bba107c88d99204f66fca | 62ad7d2d21b45b8db5518c6e0906889a5acea2b7239bba107c88d99204f66fca |
| armv7l | install | 同字节 | 5b2d2e342fa9a686962d6a30513c3976f2bbcf6362ee1e20ec177b31293bd78a | 5b2d2e342fa9a686962d6a30513c3976f2bbcf6362ee1e20ec177b31293bd78a |
| aarch64 | build | 同字节 | 071b96eb590e9efb272688afdc6eb8ab502e358dc21b95987b78102f18846ee1 | 071b96eb590e9efb272688afdc6eb8ab502e358dc21b95987b78102f18846ee1 |
| aarch64 | install | 同字节 | 9ee8ddb2ab3e4b2faf5877314b48cfc900b81a949fc3dc9924ede9900d9b6d61 | 9ee8ddb2ab3e4b2faf5877314b48cfc900b81a949fc3dc9924ede9900d9b6d61 |


x86_64 build 差异全文：[x86_64-build.diff](52_hybrid_link_evidence/x86_64-build.diff)。两个 ON 替换加三个明确开关，其余零差异。ARM 两阶段零 diff，全部架构 install 零 diff；这证明配方文本不变，不冒充 ARM 新构建验证。证据：[macro-comparison.json](52_hybrid_link_evidence/macro-comparison.json)。

## 4. CMake 生成结果与最终链接命令

工具来自未交接的历史根 `temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0`：Clang/LLD 22.1.8、CMake 3.31.2、Ninja 1.13.1，原构建环境包 clang/llvm 22.1.8-1.6；版本原文：[configuration-tools.txt](52_hybrid_link_evidence/configuration-tools.txt)。不以此证明最新快照完整构建。

在私有 user/mount namespace 中把本任务 E 绑定为 `/tmp/hybrid52`，运行该根 CMake；namespace 退出后挂载自动回收，未修改宿主配置。三组使用 spec 完整参数及随源码的 x86 MLGO assets，**未删除任何 LTO/链接器参数**。仅改源码/输出路径，另显式指定各自 `LLVM_THINLTO_CACHE_PATH=/tmp/hybrid52/config-*/lto.cache`。没有使用已有构建树或缓存。CMake 自身执行小型编译器/功能探针；没有发出 LLVM target 的 Ninja 构建命令，没有 gbs build、install 或打包。

配置进程 nice19 / ionice3；共享 heavy-stage 锁；scope MemoryMax=18GiB、swap=0；每 2 秒检查宿主 2GiB 与磁盘 30GiB 底线。各次 exit 0，无保护中止。生成时间只记录，不作性能比较。原始 argv、完整 configure 日志和资源读数为 `{a,b,c,d}-configure-*`。

| 组 | 源码 / 参数 | exit | 包含外围监控的 wall（秒） |
| --- | --- | --- | --- |
| a | 补丁 + hybrid spec | 0 | 34.005 |
| b | 未打补丁源码 + 原 spec（全部静态） | 0 | 38.006 |
| c | 补丁 + 两 DYLIB ON + HYBRID OFF | 0 | 32.005 |
| d，补充退化对照 | 未打补丁源码 + 与 c 相同参数 | 0 | 34.007 |

每组生成 **188** 个可执行/共享/模块库链接目标。用 `ninja -C /tmp/hybrid52/config-a -t commands -s bin/clang-22`（其他目标/组同理）只读取最终命令。llvm-strip 是 llvm-objcopy 的 alias，无独立链接命令；表中取其实体。完整 17 目标命令见 [a](52_hybrid_link_evidence/a-selected-commands.json)、[b](52_hybrid_link_evidence/b-selected-commands.json)、[c](52_hybrid_link_evidence/c-selected-commands.json)。

表格单元为 `共享库 / LLVM .a 数 / clang .a 数`；L=libLLVM.so，C=libclang-cpp.so；归档按名称去重；这些是链接输入，**不是已产出 ELF 的 NEEDED 实测**。

| 目标 | a 混合 | b 原配方静态 | c 开关 OFF / 动态 |
| --- | --- | --- | --- |
| clang | — / 84 / 29 | — / 84 / 29 | L + C / 0 / 0 |
| lld | — / 84 / 0 | — / 84 / 0 | L / 0 / 0 |
| llvm-ar | — / 34 / 0 | — / 34 / 0 | L / 0 / 0 |
| clang-repl | L + C / 0 / 0 | — / 92 / 30 | L + C / 0 / 0 |
| clang-check | L + C / 0 / 0 | — / 79 / 28 | L + C / 0 / 0 |
| clang-tidy | L + C / 0 / 30 | — / 54 / 62 | L + C / 0 / 30 |
| clangd | L + C / 0 / 33 | — / 42 / 66 | L + C / 0 / 33 |
| opt | L / 1 / 0 | — / 75 / 0 | L / 1 / 0 |
| llc | L / 0 / 0 | — / 74 / 0 | L / 0 / 0 |
| lli | L / 0 / 0 | — / 70 / 0 | L / 0 / 0 |
| llvm-objcopy | L / 0 / 0 | — / 17 / 0 | L / 0 / 0 |
| llvm-nm | L / 0 / 0 | — / 39 / 0 | L / 0 / 0 |
| llvm-strip | L / 0 / 0 | — / 17 / 0 | L / 0 / 0 |
| libLTO.so | L / 0 / 0 | — / 79 / 0 | L / 0 / 0 |
| LLVMgold.so | L / 0 / 0 | — / 79 / 0 | L / 0 / 0 |
| lldb | L + C / 0 / 0 | — / 16 / 0 | L + C / 0 / 0 |
| liblldb | L + C / 1 / 0 | — / 90 / 21 | L + C / 1 / 0 |


三组 driver 无 LLVM/clang-cpp 共享输入，其他指定目标均恢复 libLLVM 共享输入；clang 工具与 LLDB 同时有 clang-cpp。lld 的 6 个 lld 组件归档、liblldb 内部的 LLDB 组件归档仍正常参与构建，原始 JSON 明列。a 的 clang/lld/ar 组件集合与 b 相同；其余目标与 c 同类。

**需要 PM 注意的预期边界：动态工具并非“链接行零 .a”。** 这些归档在 c 和未打补丁的 d 中同样存在，不能删掉或把数据改成只有三组静态：

| 上游私有归档 | a 中使用者 |
| --- | --- |
| libLLVMOptDriver.a | opt |
| libLLVMDebuginfod.a | llvm-profdata、llvm-cov、llvm-debuginfod、llvm-debuginfod-find、llvm-objdump、llvm-symbolizer、liblldb、lldb-test |
| libLLVMDiff.a | llvm-diff |
| libLLVMCFIVerify.a | llvm-cfi-verify |
| libclangTidy*.a、libclangIncludeCleaner.a、libclangQuery.a 等 | clang-tidy / clangd 等工具自己的实现模块；它们同时链接共享 clang-cpp/LLVM |
| LLVM 组件集合 | libLLVM.so 本身的生产链接，不能视为另一个工具选择静态 LLVM |

源码依据见 [source-evidence.txt](52_hybrid_link_evidence/source-evidence.txt)，如 `llvm/tools/opt/CMakeLists.txt:34,52`。全量名单（含不安装的构建工具、测试/benchmark 目标与 DSO 生产者）见 [a](52_hybrid_link_evidence/a-component-archive-consumers.txt)、[b](52_hybrid_link_evidence/b-component-archive-consumers.txt)、[c](52_hybrid_link_evidence/c-component-archive-consumers.txt)；逐个归档/图行号见 `*-all-link-targets.json`。名称前缀 `lld*` 统计也包括 `lldb*`，不将 LLDB 内部归档误称 LLVM 核心。

安装工具中保留用户指定的五个强制静态例外：llvm-tblgen、clang-tblgen、lldb-tblgen（TableGen.cmake:186）、llvm-config（tools/llvm-config/CMakeLists.txt:17）、llvm-exegesis（tools/llvm-exegesis/CMakeLists.txt:22）。全图还含 llvm-min-tblgen、FileCheck/count/not、lli-child-target 等构建 utility；`LLVM_INSTALL_UTILS=OFF`，不能把它们算作新增发货工具。benchmark 目标生成但 `LLVM_BUILD_BENCHMARKS=OFF`，不是默认构建/安装目标。依据 `a-cache-keys.txt`、全量名单、对应 `%files`。

开关 OFF 的 c 与未打补丁动态配置 d：规范化本任务输出目录后，**188 个完整 link edge（含输入次序与全部属性）相同，CMakeFiles/rules.ninja 也完全相同**。证据：[switch-off-control.json](52_hybrid_link_evidence/switch-off-control.json)。没有通过改期望或增删依赖实现此结果。a 与 c 的全部 188 个 link edge 中，只有 clang-22/lld/llvm-ar 三个不同，其余 185 个相同；见 [hybrid-vs-shared-control.json](52_hybrid_link_evidence/hybrid-vs-shared-control.json)。

## 5. 安装与打包边界

生成规则继续 `install_symlink(...,create_symlink)`：clang++/clang-cl/clang-cpp→clang；clang 的 VERSION=22 生成 clang→clang-22；lld 四别名→lld；llvm-ranlib/lib/dlltool→llvm-ar；llvm-strip→llvm-objcopy。逐行证据：[install-aliases.txt](52_hybrid_link_evidence/install-aliases.txt)，clang 版本设置 `clang/tools/driver/CMakeLists.txt:88`。本轮未实际安装，因此不宣称 RPM 内 inode/链接类型已实测。

`%files` 与整个 `%install` 不变，现有 clang 包提供 clang-cpp，libllvm 包提供 libLLVM，主 llvm 包本已有严格版本 libllvm Requires（llvm.spec:75）。当前没有证据要求修改包划分或安装脚本。356627 转换仍在 install 末尾调用；转换器 clang 仍静态，llvm-dis/nm 恢复动态后依赖的 build/lib64 和 `$ORIGIN/../lib64` 必须在完整构建安装阶段验证。完整运行/依赖闭合属于组员验收，不由配置图替代。证据：packaging-invariance.json、x86_64-hybrid-install.txt、a-selected-commands.json。

常规非 devel 包零 **LLVM 开发归档** 的打包规则保持；compiler-rt 的 45 个运行库 `.a` 是已有范围，不能写成所有非 devel 包字面上没有任何 `.a`。llvm-static-devel 照常发布；基线 libarcher 同时有 libomp-devel 归属。历史包检查见 docs/22 §5.2、docs/35 §2–§3；本次 RPM 实测未获取（本任务禁止构建）。

## 6. clang-accel 影响

使用 GitHub main `88349f6` 新收集的 QB 清单，原始位置 `docs/qb_1199098_vs_1178133/size_attribution/`。其中新/旧实际快照是 20261015.022255 / 20260914.073422，不混用其他历史快照。

新 accel `/emul/usr/bin` 共 **107** 条：按本次 a 图映射，三组静态 **13** 条，上游静态例外 **2** 条（llvm-exegesis、llvm-tblgen），动态 **92** 条。这里按包内路径计数，含别名；实际 SHA 可能受 patchelf 改写，不要求与来源 ELF 同字节。证据：[accel-summary.json](52_hybrid_link_evidence/accel-summary.json)、[accel-tool-map.csv](52_hybrid_link_evidence/accel-tool-map.csv)。

逐项表的“清单行”指 QB `raw/new_armv7l_clang-accel-x86_64-armv7l_files.jsonl`，“Ninja 行”指 E/config-a/build.ninja；`a-all-link-targets.json` 也保留该行号。下表全部是本次配置预测，非新 accel RPM 实测。

| accel 的 /emul/usr/bin/ 条目 | 实际链接目标 | 补丁后配置形态 | 清单行 / Ninja 行 |
| --- | --- | --- | --- |
| armv7l-tizen-linux-gnueabi-clang | bin/clang-22 | 静态 LLVM（三组） | 4 / 100708 |
| armv7l-tizen-linux-gnueabi-clang++ | bin/clang-22 | 静态 LLVM（三组） | 5 / 100708 |
| clang | bin/clang-22 | 静态 LLVM（三组） | 6 / 100708 |
| clang++ | bin/clang-22 | 静态 LLVM（三组） | 7 / 100708 |
| clang-22 | bin/clang-22 | 静态 LLVM（三组） | 8 / 100708 |
| clang-apply-replacements | bin/clang-apply-replacements | 动态 LLVM+clang-cpp | 9 / 104943 |
| clang-change-namespace | bin/clang-change-namespace | 动态 LLVM+clang-cpp | 10 / 115923 |
| clang-check | bin/clang-check | 动态 LLVM+clang-cpp | 11 / 103650 |
| clang-cl | bin/clang-22 | 静态 LLVM（三组） | 12 / 100708 |
| clang-cpp | bin/clang-22 | 静态 LLVM（三组） | 13 / 100708 |
| clang-doc | bin/clang-doc | 动态 LLVM+clang-cpp | 14 / 116562 |
| clang-extdef-mapping | bin/clang-extdef-mapping | 动态 LLVM+clang-cpp | 15 / 103814 |
| clang-format | bin/clang-format | 动态 LLVM+clang-cpp | 16 / 101015 |
| clang-include-cleaner | bin/clang-include-cleaner | 动态 LLVM+clang-cpp | 17 / 118908 |
| clang-include-fixer | bin/clang-include-fixer | 动态 LLVM+clang-cpp | 18 / 117273 |
| clang-installapi | bin/clang-installapi | 动态 LLVM+clang-cpp | 19 / 102955 |
| clang-linker-wrapper | bin/clang-linker-wrapper | 动态 LLVM | 20 / 102010 |
| clang-move | bin/clang-move | 动态 LLVM+clang-cpp | 21 / 118043 |
| clang-nvlink-wrapper | bin/clang-nvlink-wrapper | 动态 LLVM | 22 / 102197 |
| clang-offload-bundler | bin/clang-offload-bundler | 动态 LLVM+clang-cpp | 23 / 102378 |
| clang-offload-packager | bin/llvm-offload-binary | 动态 LLVM | 24 / 169830 |
| clang-query | bin/clang-query | 动态 LLVM+clang-cpp | 25 / 118395 |
| clang-refactor | bin/clang-refactor | 动态 LLVM+clang-cpp | 26 / 103311 |
| clang-reorder-fields | bin/clang-reorder-fields | 动态 LLVM+clang-cpp | 27 / 105295 |
| clang-repl | bin/clang-repl | 动态 LLVM+clang-cpp | 28 / 103136 |
| clang-scan-deps | bin/clang-scan-deps | 动态 LLVM+clang-cpp | 29 / 102559 |
| clang-sycl-linker | bin/clang-sycl-linker | 动态 LLVM | 30 / 102746 |
| clang-tidy | bin/clang-tidy | 动态 LLVM+clang-cpp | 31 / 115147 |
| ld.lld | bin/lld | 静态 LLVM（三组） | 32 / 70332 |
| llc | bin/llc | 动态 LLVM | 33 / 159313 |
| lld | bin/lld | 静态 LLVM（三组） | 34 / 70332 |
| lli | bin/lli | 动态 LLVM | 35 / 159477 |
| llvm-addr2line | bin/llvm-symbolizer | 动态 LLVM | 36 / 174439 |
| llvm-ar | bin/llvm-ar | 静态 LLVM（三组） | 37 / 68889 |
| llvm-as | bin/llvm-as | 动态 LLVM | 38 / 159777 |
| llvm-bcanalyzer | bin/llvm-bcanalyzer | 动态 LLVM | 39 / 160036 |
| llvm-bitcode-strip | bin/llvm-objcopy | 动态 LLVM | 40 / 169093 |
| llvm-c-test | bin/llvm-c-test | 动态 LLVM | 41 / 160332 |
| llvm-cas | bin/llvm-cas | 动态 LLVM | 42 / 160502 |
| llvm-cat | bin/llvm-cat | 动态 LLVM | 43 / 160683 |
| llvm-cfi-verify | bin/llvm-cfi-verify | 动态 LLVM | 44 / 160847 |
| llvm-cgdata | bin/llvm-cgdata | 动态 LLVM | 45 / 161200 |
| llvm-cov | bin/llvm-cov | 动态 LLVM | 46 / 161502 |
| llvm-ctxprof-util | bin/llvm-ctxprof-util | 动态 LLVM | 47 / 69364 |
| llvm-cvtres | bin/llvm-cvtres | 动态 LLVM | 48 / 161672 |
| llvm-cxxdump | bin/llvm-cxxdump | 动态 LLVM | 49 / 161864 |
| llvm-cxxfilt | bin/llvm-cxxfilt | 动态 LLVM | 50 / 162045 |
| llvm-cxxmap | bin/llvm-cxxmap | 动态 LLVM | 51 / 162226 |
| llvm-debuginfo-analyzer | bin/llvm-debuginfo-analyzer | 动态 LLVM | 52 / 162401 |
| llvm-debuginfod | bin/llvm-debuginfod | 动态 LLVM | 53 / 162582 |
| llvm-debuginfod-find | bin/llvm-debuginfod-find | 动态 LLVM | 54 / 162780 |
| llvm-diff | bin/llvm-diff | 动态 LLVM | 55 / 162961 |
| llvm-dis | bin/llvm-dis | 动态 LLVM | 56 / 163308 |
| llvm-dlltool | bin/llvm-ar | 静态 LLVM（三组） | 57 / 68889 |
| llvm-dwarfdump | bin/llvm-dwarfdump | 动态 LLVM | 58 / 163736 |
| llvm-dwarfutil | bin/llvm-dwarfutil | 动态 LLVM | 59 / 164012 |
| llvm-dwp | bin/llvm-dwp | 动态 LLVM | 60 / 164210 |
| llvm-exegesis | bin/llvm-exegesis | 静态 LLVM（上游例外） | 61 / 164391 |
| llvm-extract | bin/llvm-extract | 动态 LLVM | 62 / 165313 |
| llvm-gsymutil | bin/llvm-gsymutil | 动态 LLVM | 63 / 165494 |
| llvm-ifs | bin/llvm-ifs | 动态 LLVM | 64 / 165703 |
| llvm-install-name-tool | bin/llvm-objcopy | 动态 LLVM | 65 / 169093 |
| llvm-ir2vec | bin/llvm-ir2vec | 动态 LLVM | 66 / 165884 |
| llvm-jitlink | bin/llvm-jitlink | 动态 LLVM | 67 / 166386 |
| llvm-lib | bin/llvm-ar | 静态 LLVM（三组） | 68 / 68889 |
| llvm-libtool-darwin | bin/llvm-libtool-darwin | 动态 LLVM | 69 / 166703 |
| llvm-link | bin/llvm-link | 动态 LLVM | 70 / 166884 |
| llvm-lipo | bin/llvm-lipo | 动态 LLVM | 71 / 167065 |
| llvm-lto | bin/llvm-lto | 动态 LLVM | 72 / 69528 |
| llvm-lto2 | bin/llvm-lto2 | 动态 LLVM | 73 / 167246 |
| llvm-mc | bin/llvm-mc | 动态 LLVM | 74 / 167421 |
| llvm-mca | bin/llvm-mca | 动态 LLVM | 75 / 167918 |
| llvm-ml | bin/llvm-ml | 动态 LLVM | 76 / 168257 |
| llvm-ml64 | bin/llvm-ml | 动态 LLVM | 77 / 168257 |
| llvm-modextract | bin/llvm-modextract | 动态 LLVM | 78 / 168487 |
| llvm-mt | bin/llvm-mt | 动态 LLVM | 79 / 168668 |
| llvm-nm | bin/llvm-nm | 动态 LLVM | 80 / 168866 |
| llvm-objcopy | bin/llvm-objcopy | 动态 LLVM | 81 / 169093 |
| llvm-objdump | bin/llvm-objdump | 动态 LLVM | 82 / 169583 |
| llvm-offload-binary | bin/llvm-offload-binary | 动态 LLVM | 83 / 169830 |
| llvm-offload-wrapper | bin/llvm-offload-wrapper | 动态 LLVM | 84 / 170043 |
| llvm-opt-report | bin/llvm-opt-report | 动态 LLVM | 85 / 170354 |
| llvm-otool | bin/llvm-objdump | 动态 LLVM | 86 / 169583 |
| llvm-pdbutil | bin/llvm-pdbutil | 动态 LLVM | 87 / 170727 |
| llvm-profdata | bin/llvm-profdata | 动态 LLVM | 88 / 69692 |
| llvm-profgen | bin/llvm-profgen | 动态 LLVM | 89 / 170946 |
| llvm-ranlib | bin/llvm-ar | 静态 LLVM（三组） | 90 / 68889 |
| llvm-rc | bin/llvm-rc | 动态 LLVM | 91 / 171188 |
| llvm-readelf | bin/llvm-readobj | 动态 LLVM | 92 / 171562 |
| llvm-readobj | bin/llvm-readobj | 动态 LLVM | 93 / 171562 |
| llvm-readtapi | bin/llvm-readtapi | 动态 LLVM | 94 / 171809 |
| llvm-reduce | bin/llvm-reduce | 动态 LLVM | 95 / 172485 |
| llvm-remarkutil | bin/llvm-remarkutil | 动态 LLVM | 96 / 172748 |
| llvm-rtdyld | bin/llvm-rtdyld | 动态 LLVM | 97 / 172912 |
| llvm-sim | bin/llvm-sim | 动态 LLVM | 98 / 173398 |
| llvm-size | bin/llvm-size | 动态 LLVM | 99 / 173579 |
| llvm-split | bin/llvm-split | 动态 LLVM | 100 / 173907 |
| llvm-stress | bin/llvm-stress | 动态 LLVM | 101 / 174071 |
| llvm-strings | bin/llvm-strings | 动态 LLVM | 102 / 174241 |
| llvm-strip | bin/llvm-objcopy | 动态 LLVM | 103 / 169093 |
| llvm-symbolizer | bin/llvm-symbolizer | 动态 LLVM | 104 / 174439 |
| llvm-tblgen | bin/llvm-tblgen | 静态 LLVM（上游例外） | 105 / 3829 |
| llvm-tli-checker | bin/llvm-tli-checker | 动态 LLVM | 106 / 174675 |
| llvm-undname | bin/llvm-undname | 动态 LLVM | 107 / 174856 |
| llvm-windres | bin/llvm-rc | 动态 LLVM | 108 / 171188 |
| llvm-xray | bin/llvm-xray | 动态 LLVM | 109 / 175130 |
| opt | bin/opt | 动态 LLVM | 110 / 175895 |


该包还收录 libLTO.so / LLVMgold.so，本次均恢复动态 LLVM（§4）。当前静态版 accel 不含两个核心 DSO；**不能复用它承载新的动态工具**。旧动态版明确包含 `/emul/usr/lib64/libLLVM.so.22.1`、`/emul/usr/lib64/libclang-cpp.so.22.1`。证据：QB `raw/{old,new}_armv7l_clang-accel-x86_64-armv7l_files.jsonl` 末尾及 [accel-elf-baselines.csv](52_hybrid_link_evidence/accel-elf-baselines.csv)。

qemu-accel spec 的 `prepare_package_list` 对每个可执行/DSO 运行 ldd，收集解析到的绝对路径（原文 **309–324**）；clang 收录 `clang-*`、clang++、opt/lli/llc、llvm-*、lld/ld.lld、libLTO/LLVMgold（**335–345**）；之后 cp -aL、改 interpreter/条件 RUNPATH（**382–397**），最后重建 clang 软链接（**617–643**）。来源：[qemu-accel_new_armv7l_retry.spec](qb_1199098_vs_1178133/size_attribution/raw/qemu-accel_new_armv7l_retry.spec)。

因此现有自动依赖收录机制有历史动态包实物支持，**未发现本次必需的 qemu-accel 源码修改**；仍必须从新的 LLVM RPM **重建 accel 和 Base 镜像**，验收新包 DSO 可解析。若完整构建中 ldd 收录失败，配套修改点是该 spec/模板的 prepare_package_list 与 clang-accel 文件列表；应显式收录两库及其传递依赖、检查 RUNPATH/loader。此项仅定位，未修改或实测新 accel。现有 QB 只有 armv7l accel 完整文件样本，aarch64 accel 同等闭合情况**未获取**。

## 7. 数字口径、风险与交接

| 数据 | 数值 | 证据与边界 |
| --- | --- | --- |
| 9 月旧源码混合试构建 | 22 RPM；30/30 TU 对象同字节；5040.295 秒 | docs/22 §3–§6，f111162e，旧源码参考，**不是本次实测** |
| 旧源码链接峰值 | libLLVM 11.292168GiB；clang 15.177582GiB | docs/22 §4；scope 曾达到 18GiB；不是本次容量认证 |
| QB x86 LLVM wall | 5686 → 29864 秒 | QB llvm_builds.csv:2,5，不把跨快照差分分摊为某个参数因果 |
| QB armv7l accel RPM | 54,806,369 → 659,624,309 字节 | QB SIZE_FINDINGS.md 的 RPM 表 |
| QB accel 解包路径总字节 | 239,912,044 → 2,756,647,372 | 同表，regular 长度+symlink 文本长度，非 du 物理占用 |
| 本次新 RPM、耗时/峰值、accel 大小、运行验证 | 未获取 | 只做配置，不能预测压缩体积或宣称性能收益 |

风险/未验证项：实际静态三工具是否无共享 LLVM NEEDED；全部动态依赖闭合；共享 libLLVM 和 clang 两个大链接的容量；LLVM_EXPORT_SYMBOLS_FOR_PLUGINS 当前 OFF，不能推广到开启插件符号导出遍历的配置（docs/22 §3.2）；356627 的既有 GNU strip/addrsig 边界仍在 docs/51，本补丁不修 strip；armv7l/aarch64 仅宏展开不变；将来基线包含 356949 后需重新 rebase/核对，不能提前声称兼容。私有 `.a` 的实际存在已在 §4 明列，应由 PM review 接受“恢复上游动态方式”的边界。

组员开工前还有实际仓库门禁：W/gbs_llvm.conf 的 Base 20261001.092726 repomd 当前 **404**，Unified 20260814.092727 **200**（SHA `e7af3f222f0ce958678d964589f2d156e8b47ba463ac0b3b0b96c74663382200`）。本任务未换源。见 [team-repository-preflight.json](52_hybrid_link_evidence/team-repository-preflight.json)。本轮到此，等待 PM review 后再交组员完整验证。
