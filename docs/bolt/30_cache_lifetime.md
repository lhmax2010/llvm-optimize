# 30：ThinLTO 缓存最后使用点与 BOLT 中间产物生命周期

2026-10-22。**只读源码/历史证据分析；没有改 spec/helper/Source1005，没有执行构建、CMake/Ninja、清理或 Gerrit 操作。**

最后一次**依赖缓存内容进行编译链接**的是 BOLT pipeline 中重链 clang 的命令，成功返回后，后面的静态库转换、安装和 tiny 检查都不需要这些缓存对象；但 post 的磁盘报告仍会遍历缓存做统计。可以考虑在 BOLT 块内、pipeline 和 compare-root 成功之后清理，关闭 BOLT 的路径保持不动；若“后面不再读缓存”连目录统计都不允许，则必须等最后的 `disk-report post` 完成。按29号已有数据，清理后续阶段的占用可能减少约 **96.88 GB / 90.22 GiB（估算）**，但此前普通安装与重链已保留了这份缓存，**不能据此承诺整个构建峰值降低90 GiB**。

## 1. 范围、源码身份与引用方式

分析基点：`9e5675f57d122549997caffa39b655dfefc46fee`，源码 tree `941fc226aeb6b32ea6c78b03d78b5af2b87561a5`。通过 `git show <SHA>:<路径>` 读取，未 checkout、配置或编译。主要讨论 QB 对应的 **x86_64、定义 `_toolchain`** 的配置；`--without clang_bolt` 是BOLT开关，不等于取消 `_toolchain`。

所有源码行号均对应该提交，不是工作副本的后续版本。以下短名在全文中固定使用；每条短引文的完整上下文见 [source-excerpts.txt](../../tools/bolt/results/cache-lifetime-20261022/source-excerpts.txt)，范围索引见 [excerpt-index.json](../../tools/bolt/results/cache-lifetime-20261022/excerpt-index.json)。

| 短名 | 文件与固定副本 |
|---|---|
| S | [packaging/llvm.spec](../../tools/bolt/results/cache-lifetime-20261022/source/packaging/llvm.spec) |
| H | [packaging/clang-bolt-helper.py](../../tools/bolt/results/cache-lifetime-20261022/source/packaging/clang-bolt-helper.py) |
| A | [packaging/llvm-static-archives-native.py（Source1005）](../../tools/bolt/results/cache-lifetime-20261022/source/packaging/llvm-static-archives-native.py) |
| C | [llvm/cmake/modules/HandleLLVMOptions.cmake](../../tools/bolt/results/cache-lifetime-20261022/source/llvm/cmake/modules/HandleLLVMOptions.cmake) |
| P | [llvm/include/llvm/Support/CachePruning.h](../../tools/bolt/results/cache-lifetime-20261022/source/llvm/include/llvm/Support/CachePruning.h) |
| K | [llvm/lib/Support/CachePruning.cpp](../../tools/bolt/results/cache-lifetime-20261022/source/llvm/lib/Support/CachePruning.cpp) |
| L / D | [lld/ELF/LTO.cpp](../../tools/bolt/results/cache-lifetime-20261022/source/lld/ELF/LTO.cpp) / [lld/ELF/Driver.cpp](../../tools/bolt/results/cache-lifetime-20261022/source/lld/ELF/Driver.cpp) |

S SHA256 `0f9bd9333c614129fd5951ed8a1c062793c7cef74b83dbe9e52b03fffedf6a8d`；H `28f61031cb5ff60eaa46ebdc6a07014e4019ce1046f3ccee07794b6c173d1f23`；A `6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557`。完整源码身份见 [source-provenance.json](../../tools/bolt/results/cache-lifetime-20261022/source-provenance.json)。

历史 CMakeCache、Ninja边、生成安装脚本与Tizen后处理脚本只作旁证，**不是重新配置出的9e树，也不是QB 1202084的x86包日志**；来源和SHA单列在 [historical-provenance.json](../../tools/bolt/results/cache-lifetime-20261022/historical-provenance.json)。没有声称拿到了该次QB运行的实际缓存用量或系统LLD版本。

## 2. 缓存路径、开关与自动清理策略

### 2.1 配置与实际路径

- S:248–250：`mkdir -p build`、`cd build`、`cmake`；S:266–273在 `_toolchain` 条件内设置 `-DLLVM_USE_LINKER=lld`、`-DLLVM_ENABLE_LTO=Thin`。这部分不受 `clang_bolt` 开关保护，因此**同一toolchain配置关闭BOLT仍有普通ThinLTO缓存**。S:236–237还设置了 `-flto=thin`；不能把BOLT开关与ThinLTO开关混为一谈。
- 精确选项名是 **`LLVM_THINLTO_CACHE_PATH`**。C:1307原文：`set(LLVM_THINLTO_CACHE_PATH "${PROJECT_BINARY_DIR}/lto.cache" CACHE STRING ...)`。C:1327–1329在UNIX+lld下加入 `-Wl,--thinlto-cache-dir=${LLVM_THINLTO_CACHE_PATH}`，作用于可执行文件和共享库的链接参数。
- 默认因此是 **`%{_builddir}/%{buildsubdir}/build/lto.cache`**。历史根内实值为 **`/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache`**，对应保存的 [build-CMakeCache.txt:1769](../../tools/bolt/results/cache-lifetime-20261022/historical/build-CMakeCache.txt)：`LLVM_THINLTO_CACHE_PATH:STRING=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache`；L1407是 `LLVM_ENABLE_LTO:STRING=Thin`，L2158为 `LLVM_USE_LINKER:UNINITIALIZED=lld`。QB宿主侧NGBS根前缀没有从缺失的x86包日志中确认，不能把本地宿主路径当QB路径。
- H:284–288要求原始链接命令只有一个绝对 `--thinlto-cache-dir=`，只有显式传 `cache` 才替换。S:485调用 `pipeline "$PWD" "$BOLT_WORK" "$PWD/bin/llvm-bolt"`，没有 `--cache-dir`；H:1168记录 `cache_policy='original-in-place' if cache is None else 'explicit-copy'`。因此9e生产路径**原地使用普通缓存，不复制**。`cache-copy`是未被本spec调用的独立CLI能力（H:1189–1206、1300、1350），不属于这次正常流水线。

### 2.2 有LLD默认淘汰，但没有spec自定义容量策略

S与A未设置 `--thinlto-cache-policy`、`prune_interval`、`cache_size` 或 `prune_after`；查询记录为 [policy-search.json](../../tools/bolt/results/cache-lifetime-20261022/policy-search.json)。历史链接命令和CMakeCache也没有显式策略参数。**这不等于缓存永远不自动删除**：

- D:1568–1571：`thinLTOCacheDir = ...OPT_thinlto_cache_dir`，`parseCachePruningPolicy(...OPT_thinlto_cache_policy)`。
- L:330–336：`localCache("ThinLTO", "Thin", ctx.arg.thinLTOCacheDir, ...)`；L:373–374在链接中调用 `pruneCache(ctx.arg.thinLTOCacheDir, ctx.arg.thinLTOCachePolicy, files)`。
- 9e同源默认值：P:34 `Interval = ...seconds(1200)`；P:39 `Expiration = ...hours(7 * 24)`；P:46 `MaxSizePercentageOfAvailableSpace = 75`；P:51 `MaxSizeBytes = 0`；P:62 `MaxSizeFiles = 1000000`。即20分钟扫描间隔、1周未访问过期、百分比75%、不设固定字节上限、文件数上限100万。
- 百分比分母并非“现在剩余空间”的简单75%：K:288 `AvailableSpace = TotalSize + SpaceInfo.free`，K:294–296再计算目标。它是链接时触发的淘汰，不能保证完整构建任何时刻都不写满。

以上默认数值是**9e源码中LLD的实现**。链接实际由构建环境的clang/lld执行；缺QB包日志，尚未核对预装LLD二进制及其默认值是否恰好同版。可以确认spec没有覆盖策略，不能将上述源码默认值冒充已读到的QB运行记录。

## 3. 按实际顺序核对所有缓存访问

区分三种访问：**内容读写**（影响链接）、**路径/元数据统计**（缺失可以接受）、**不访问**。以下讨论正常成功路径；失败诊断另列。

| 执行阶段 | 是否使用该缓存 | 文件、行号与原文依据 |
|---|---|---|
| 普通配置与构建 | 配置记录路径；ThinLTO可执行/共享库链接读、写、可能淘汰缓存。普通`.o`编译和`ar`并不各自使用LLD缓存 | S:269–270 `LLVM_USE_LINKER=lld` / `LLVM_ENABLE_LTO=Thin`；S:411 `ninja -d keeprsp ...`、关闭BOLT时S:413 `ninja -j ...`；C:1328 `--thinlto-cache-dir=...` |
| 普通 `%install` CMake install | **不再次启动链接**；安装既有文件、改RPATH/链接别名，可选strip | S:421 `cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}/usr -P cmake_install.cmake`，不是 `ninja install` 或 `cmake --build`。历史生成的clang安装脚本L57 `file(INSTALL ... TYPE EXECUTABLE FILES`，L67 `file(RPATH_CHANGE`，L71–72只在 `CMAKE_INSTALL_DO_STRIP` 时执行llvm-strip；详见下文全量旁证 |
| BOLT begin与准备 | begin枚举缓存做基线；拷贝ordinary、取链接命令、解压profile不做ThinLTO链接 | S:455 `disk-report begin`；S:465–468复制/`ninja -t commands`/`unpack`。`ninja -t commands`只输出命令；H:904–922取缓存清单并保存基线 |
| 追加bolt CMake配置、dry-run | 配置保留同一缓存参数；检测用小链接可能访问缓存（历史已有记录），dry-run只列任务 | S:469–472 `cmake -S ../llvm -B . ...`；S:475 `ninja -n llvm-bolt`。没有执行配置来验证本轮的具体检测任务；这一阶段早于工具构建和重链，不改变最后使用点 |
| llvm-bolt工具构建 | 最后的llvm-bolt链接也带ThinLTO缓存；TF刷新任务是编译/归档，不等于新的普通全量链接 | S:480 `ninja -j 1 llvm-bolt`；历史追加bolt图 `build.ninja:148611–148621` 的 `LINK_FLAGS = ... -flto=thin ... --thinlto-cache-dir=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache ...`，原边在 `historical-bolt-link-edge.json`；S:481–484验证、统计工具构建 |
| **pipeline重链clang** | **最后一次依赖缓存对象的读写/淘汰** | H:1159生成重放脚本；H:1160 `call(['/bin/sh',str(script)],work/'reference-relocs.log',cwd=build,timeout=1800)`；H:284–292保留原缓存参数，只改输出/depfile并加emit-relocs |
| strip-debug、BOLT改写、strip-all | 不调用LLD/ThinLTO缓存 | H:1161 `llvm-strip --strip-debug`；H:699–700 `argv = [bolt, input_elf, '-o', output, '-data='+str(profile)] + OPTIONS`；H:1233–1234复制后 `--strip-all` |
| pipeline中的两次tiny | 只编译为`.o`，不链接，不使用该缓存 | H:1163/1166；H:507 `argv = [cc, '--no-default-config', '--target='+triple, '-c', '-O2', ...]`，无 `-flto` 或缓存参数 |
| pipeline磁盘报告 | **仍遍历缓存路径和lstat**，不是读取对象内容 | S:487 `disk-report pipeline`；H:880 `cache = disk_cache(build, work); current = disk_entries(cache)`；H:843–852 `path.lstat()` / `os.walk(...)` |
| compare-root | 只读BUILDROOT、比较JSON；不读build/lto.cache | S:490–492；H:556 `current = root_snapshot(root)`；H:560–568比较文件/权限，H:522–538遍历的是传入的安装根 |
| 静态库转换（Source1005） | **使用LLVM后端做IR→本地对象，但不做ThinLTO、不调用LLD、不使用缓存** | S:531–538指向build/bin普通clang、llvm-dis、llvm-nm。A:240–241将 `-flto=thin` 分类为 `irrelevant`，理由 `pre-link bitcode format already materialized; never replay LTO`；A:322–323实际flags含 `--no-default-config ... -x ir ... -c`；A:650编译，A:680–681用 `/usr/bin/ar qcDS` / `sD` 打包 |
| candidate安装 | ELF/SHA/别名检查与复制、fsync、rename；无链接 | S:544–545；H:615 `validate_identity(identity, candidate)`；H:623 `shutil.copyfile(candidate,tmp)`；H:639 `os.replace(tmp,entity)` |
| 平台后处理、打包 | 正常链处理BUILDROOT、调试来源文件，不调用ThinLTO链接。源文件复制边界见§5 | S:783–785保存并展开原平台链；S:555–778列RPM载荷。历史Tizen脚本L83 `find-debuginfo.sh`、L108 `brp-strip-static-archive`，没有缓存参数；strip脚本仅在RPM_BUILD_ROOT内查找ELF/归档 |
| BOLT post尾检 | 普通/已安装clang对照、SHA/ELF、别名、CMake扫描与tiny；不需要缓存对象 | S:786；H:649/659校验安装SHA，H:660 `no_bolt_products(root)`，H:661–662 `security_compare(ordinary, str(entity))` / `tiny_gate(...)` |
| **disk-report post** | **正常成功路径最后一次缓存目录统计读取**；无内容依赖 | S:788；H:913调用 `disk_measure`，H:880枚举cache；H:839–840明确 `if not root.exists() and not root.is_symlink(): return {}`，缓存不存在不是门禁失败 |
| 任一BOLT失败的诊断 | 可能再次枚举缓存及读取统计基线；失败路径不存在唯一固定的“最后访问行” | H:1372–1377 `diagnose_safely(...)`后返回1；H:1091读取 `disk-baseline.json`、H:1098 `disk_measure(build,work,baseline)`。H:932–1133是只读诊断；缺cache返回空清单 |

**CMake install的旁证范围：** 对16号已保存的普通配置快照中**667份** `cmake_install.cmake` 做文本检查，137条 `execute_process`中134条为 `/bin/llvm-strip`，3条为 `cmake -E create_symlink`；未匹配 `ninja`、`--build`、`--target`、`thinlto`、`lto.cache`。9e源码 `LLVMInstallSymlink.cmake:22–24` 也只调用 `cmake -E ${link_or_copy}`。清单/原文在 [historical-install-audit.json](../../tools/bolt/results/cache-lifetime-20261022/historical-install-audit.json)。这是对保存配置的核对，不是新的CMake运行，也不宣称核对了未取得的QB生成脚本。

由此，**最后一次必需使用点是 H:1160成功返回之后**，不是“所有install结束”之后，也不是Source1005结束之后。若“读”包括统计，则正常路径最后一次是S:788；不能写成“H:1160以后完全没人碰这个路径”。

## 4. 清理位置：ON / OFF 与两种前提

本节只给建议位置，**没有新增或运行删除命令**。

| 场景 | 可考虑的位置 | 理由、限制 |
|---|---|---|
| BOLT ON，要求没有后续**内容依赖** | helper内部最早是H:1160成功返回后；spec层建议在 **S:492 `BOLT_COMPARE_ROOT_PASS` 后、S:494关闭条件块前** | 此时S:487已记录pipeline用量，compare-root也已通过；普通LLVM与llvm-bolt链接、BOLT重链全部结束。Source1005随后A:322–323明确只做 `-x ir -c`；OFF完全不进入S:422–495。若要更早降低strip临时峰值，H:1160后是理论位置，但属于未来helper修改/认证，不是本轮执行 |
| BOLT ON，按“后续任何步骤都不得再读这个路径”的**字面条件** | **S:788最后disk-report post完成之后**，仍限制在BOLT的post尾段内 | 中间插入清理不满足这个严格字面条件，因为H:880还会统计cache、失败诊断也可能统计；虽然缺失是受支持状态（H:839–840），不能把“允许缺失”说成“没有访问”。post后再删对早已出现的重链/静态转换/平台后处理峰值无改善 |
| BOLT OFF | **不加入删除** | 内容上的最后链接是S:413普通ninja返回；理论上随后不需要其缓存，但用户要求关闭BOLT行为逐字节不变，不能在普通build/install链里加清理。现有S:421普通安装和S:531–538转换也不能包装或改写 |

选择中段清理意味着接受“后续report仍查询路径，但空目录/不存在不影响产物”的语义，不需要改变四次disk-report的位置或返回码；报告会如实出现cache净减少。H:901 `cache_net_allocation_delta_bytes = current - old`可为负，H:887的正增量对不存在条目不计，逻辑能表达缓存已删除。保留 `disk-baseline.json` 和 `link.original` 才能维持同一路径的比较（H:856–862、911–913）。

未来若实现，必须确认实际缓存是当前构建独占的预期路径、没有并行链接或共享缓存用户；不能仅用默认字符串推断任意重定向的 `LLVM_THINLTO_CACHE_PATH` 都可整目录删除。C:1307明说该选项可以跨多个构建目录共用，H:284–285目前只验证唯一绝对参数，**没有证明缓存独占**。这些是清理安全边界，不是要写进发布代码的本地资源门槛。

## 5. 后续耗时、产物与RPM影响

**静态结论：** 在H:1160已成功结束、没有额外并行/重试链接的前提下，后续标准步骤没有依赖缓存命中的计算。删除不会让Source1005或tiny“退回无缓存ThinLTO”：它们根本没有执行ThinLTO链接（A:240–241、322–323；H:507）。删除本身有目录遍历/unlink耗时；报告枚举的条目减少，但没有测量可声称具体节省时间。

若以后重跑链接/增量构建，缓存命中会丢失，可能明显变慢。C:1317–1319原文 `This improves initial build time a little ... and significantly improves incremental build time.`；`llvm/lib/Support/Caching.cpp:45–59`构造 `llvmcache-`条目并尝试命中，L72–74将不存在作为cache miss处理。这是**后续重跑**的代价，不是正常post链会发生的工作。

缓存是build下的中间对象，不是BUILDROOT载荷。S:682的 `%{_libdir}/lib*.a`、S:692–697的clang条目指安装目录，S:555–778没有缓存目录条目；H:554–569的compare-root也只比较BUILDROOT。由此推断，在指定位置只删cache不会改动已完成clang、原生静态库或安装文件字节。

**debugsource要单独说明：** 不能仅凭 `%files` 没写cache就忽略间接读。历史Tizen `find-debuginfo.sh:445–448`调用 `debugedit ... -l "$SOURCEFILE" "$f"`，L665–667据该来源清单运行 `cpio -pd0mL`，因此真实源码/生成头即使在build目录仍可能被读取；不能删除普通源码/生成头。ThinLTO cache是后端对象，不是源文件；对保留的历史22RPM清单、其他132个debug ELF来源集合和clang-debuginfo来源JSON搜索 `lto.cache` / `llvmcache-` / Thin临时对象，无命中，证据见 [historical-debug-cache-search.json](../../tools/bolt/results/cache-lifetime-20261022/historical-debug-cache-search.json)。这是历史旁证，**不是9e同条件全RPM字节一致性认证**。若未来实施清理，仍应核对新构建debugsource来源没有意外落进cache、RPM文件清单/文件SHA及候选一致；本轮不能保证压缩RPM容器本身逐字节相同，也没有运行该验证。

## 6. BOLT自有产物生命周期

下表的“最后读取”指**正常业务步骤真正需要内容的最后读取**；磁盘报告在H:865–901还会lstat所有BOLT自有范围。删除后report允许路径不存在，但失败预测H:991–1065会根据现存文件/任务输出推算：提前删工具对象或各阶段clang可能使其估算降级，不能据下面的最早业务删除点就宣称诊断语义也完全不变。保留文本/SHA证据、设计清理完成记录后再认证，是未来工作。本轮不修改任何逻辑。

另有一项保全要求不能遗漏：H:44–45原文为 `Retain ordinary/pre-strip BOLT ELFs, rewrite/identity records, final RPM/accel SHA and Build-ID for crash localization`。因此表中“最早业务清理点”只表示不再被本次成功流水线读取，不表示这些文件已经没有崩溃定位价值；未来若改成只留SHA和文本，还需明确改变这项保全策略，或先在构建根外保存所需ELF。本轮没有修改该说明，也不授权删除。

`Wk = build/clang-bolt`（S:430）；`build`为普通LLVM共用构建目录。**不能删除整个build，也没有独立的第二套BOLT build tree。** S:469 `-B .` 和S:480 `ninja -j 1 llvm-bolt`都在同一个build中。

| 文件/目录 | 产生位置（spec → helper/CMake） | 最后内容读取与原文依据 | 9e目前何时删除 | 最早业务清理点；post要求 |
|---|---|---|---|---|
| `build/tools/bolt/` 的对象、VCS生成文件等 | S:469配置，S:480构建；工具白名单H:712含 `Generating VCSVersion.inc`、`Building CXX object tools/bolt/...` | S:480的llvm-bolt链接；历史边148611把BOLT库/对象纳入输入 | 无BOLT成功收尾删除；H:866统计 `build/'tools/bolt'` | 工具链接成功后；实际建议S:481–484验证和report之后。post产品门禁不需要它们；后续诊断可能检查任务输出H:1002–1009 |
| `build/lib64/libLLVMBOLT*.a`（7个） | S:480的静态归档任务；H:712列任务 | S:480链接 `bin/llvm-bolt`；不是运行时共享库 | 无主动删除；H:868逐个glob统计 | 同上。只限BOLT库，不能扩成 `lib64/*`；普通库和TF归档不属于可删BOLT资产 |
| `build/bin/llvm-bolt` | S:480，H:791–806验证本次产出与SHA | H:697读版本，H:700执行重写，H:707 `digest(bolt)`；在H:1162返回前完成 | 无主动删除；H:867/stat继续统计 | H:1162成功返回后；spec层pipeline成功之后。不需要保留未被生产调用的perf2bolt；S:471禁BOLT工具全集，H:699只调用llvm-bolt |
| `Wk/ordinary-clang-22` | S:466 `cp -p bin/clang-22 ...` | **post**：S:786显式传入；H:661 `security_compare(ordinary, str(entity))`、H:662 tiny，H:503运行version | 无主动删除 | **post成功之后**；不能在pipeline或install后删。普通 `build/bin/clang-22` 另供Source1005（S:535），也不能顺带删除 |
| `Wk/profile.fdata` | S:468；H:253–255解压、核SHA | H:696校验、H:699–700作为 `-data=` 重写输入 | 只在解压异常H:256–259删除不完整输出；成功保留 | H:1162重写和结果记录成功后；post产品门禁不需要，诊断H:1021–1032仍可能测量profile需求 |
| `SOURCES/clang-bolt-v2.fdata.xz`（Source1200） | S:55原始Source声明；不是pipeline新生成物 | S:468解压；失败诊断H:1023–1030可能再流式读取Source大小 | 无删除 | **不作为本次BOLT中间产物清理**；保留原始构建输入，尤其诊断仍会使用 |
| `Wk/link.original` | S:467的 `ninja -t commands`，H:1143 `atomic_text(output,text)` | H:1155构造重放命令；**post报告/诊断** H:857–861再次读以定位cache | 无删除 | 为报告/诊断保留至S:788结束，文本很小，应归档而非优先删 |
| `Wk/reference-relocs.sh`、`.d` | H:1159生成脚本，H:289–292改输出/depfile，H:1160链接器写`.d` | 脚本H:1160；`.d`是重链新depfile，不在本轮后续Ninja图中消费（S:480之后无新ninja执行） | 无删除 | 重链完成后无产品内容依赖；先保留文本证据。不要把它与原build图的普通对象/depfile混淆 |
| `Wk/reference-relocs-clang-22`及链接器 `.tmp*` | H:1156–1160；临时名由链接器产生。29§4仅实测到未完成 `.tmpc53946f` | H:1161就地strip-debug；H:699重写读输入，H:708 `digest(input_elf)` | 正常reference无主动删除；helper没有兜底清理残留`.tmp*` | **H:1162完整返回后**可删有效reference。残留临时文件须等链接进程退出且成功状态明确，不能在链接/失败诊断未结束时按通配符删 |
| `Wk/clang.bolt`（strip-all前） | H:1162 / H:699 `'-o', output` | H:1163预strip tiny、H:1233生成candidate；**安装阶段仍读** H:615 → H:1211 `digest(identity['before_path'])`、H:1212 `ELF(...)` | 无删除 | **S:544–545安装成功返回后**；不能只在pipeline完成时删。post H:659只核state中的after SHA，不再打开before_path |
| `Wk/clang.candidate`（完全strip） | H:1164 → H:1233 `copy2`、H:1234 `--strip-all` | H:1165–1166安全/tiny；H:615校验、H:623复制、H:628比大小 | 无成功删除 | **S:544–545成功后**；post读取BUILDROOT中的已安装clang，不读工作副本。注意H:1055的失败预测当前还用candidate判断已安装状态，提前删需另行认证诊断 |
| `Wk/identity.json` | H:1235–1239记录strip前后SHA与note | S:545 / H:1362加载；H:633把identity完整嵌入install-state | 无删除 | install成功后无产品读取，但它是关键身份链文本，应留存；**post需要内嵌identity的install-state，而非此原JSON文件** |
| `Wk/install-state.json` | S:545 / H:636 `save(state,result)`，在最终rename前 | **post** S:786 / H:1364加载；H:649、659核安装SHA，H:650–653核别名 | 无删除 | **post成功后**才可归档/清理；缺失直接使尾检失败 |
| `Wk/install-before.json` / `install-after-pipeline.json`（compare-root） | S:464 / H:1359快照；S:490–491 / H:557写after | H:558–568比较before与当前；after写入后无再加载消费者 | 无删除 | S:490–492成功后无产品内容依赖；保留文本审计。**不是两套安装目录，不可能通过删它回收几十GiB** |
| `Wk/install-manifest-before.txt` | S:465复制普通install_manifest | 当前生产代码没有再消费它；S:465为唯一引用 | 无删除 | 拷贝完成后是证据；原build/install_manifest不是BOLT新增物，不能混删 |
| `Wk/tool-dry-run.txt`、`tool-plan.json`、`tool-before.json`、`tool-build.txt`、`tool-build-verification.json` | S:475/477/479/480/481–482；H:751–808 | plan/state/log由tool-verify消费；**失败诊断**H:991–1009仍读plan/log/产出。verification在S:483 `cat` | 无删除 | 不影响产品的最早点是验证之后，但应保留为文本并供post失败诊断使用；不要删除任务完成证据 |
| `Wk/{reference-relocs,reference-strip,identity.strip}.log`、`rewrite/{bolt.log,bolt-version.log,rewrite-result.json}`、各`.argv.json` | H:202–217每次call写log/argv/completed；H:700/710写rewrite证据；H:1160/1161/1234各阶段 | 业务匹配H:701读bolt日志；**诊断**H:968–973、1036–1048用completed判断未完成步骤 | 无删除 | 文本应至少保留到post完成；否则可能被误判为步骤未完成并放大需求估算 |
| `Wk/prestrip-gate/`、`preinstall-gate/`中的tiny.c、same.o、六个目标对象与日志 | H:1163/1166 → H:501/512/515 | H:517整对象比较；H:518保存result | H:510–511每次编译前仅删旧same.o；各目标输出最终保留 | 各自tiny返回后无产品内容依赖；保留结果/SHA与日志，未来可只清理二进制输出 |
| `Wk/post-gate/`中的同类对象、post-result.json | S:786 → H:662；H:1365保存post-result | **post内部** H:517比较；之后S:788统计 | 除轮次内same.o外，无最终清理 | post成功、文本结果保全后；若要保留四次report完整端点，等S:788后 |
| `Wk/pipeline-result.json` | H:1169保存identity/security/match等结果 | helper返回后H:1366打印result；后续生产子命令不再从该JSON加载 | 无删除 | 属于应保留的文本证据；不存在必须保留巨型目录的要求 |
| `Wk/disk-baseline.json`、`disk-{begin,tool-built,pipeline,post}.json` | S:455/484/487/788 → H:918–922 | **post报告/失败诊断** H:911–913、1091–1098读baseline；阶段报告供审计，当前算法不逐份回读 | 无删除 | baseline至少至S:788完成；阶段JSON保留用于解释峰值与清理效果 |
| BUILDROOT中的 `.clang-bolt.new` / `.名字.bolt-link` | S:544 → H:620–632 | H:626–628核SHA/大小，H:638–639原子替换 | 成功rename后临时名消失；异常H:641–644尝试unlink | 已有安全顺序，不另加提前清理；真实安装clang要供post/RPM使用，**不是可删中间物** |

**普通共有文件不归BOLT清理：** `lib64/libtf_xla_runtime.a` 是tool-prepare/verify要验证不变的普通归档（H:758–760、797–800），也是重链输入的一部分；`build/bin/clang-22`、llvm-dis、llvm-nm继续供S:535–537的Source1005使用；post的资源目录是BUILDROOT下clang/22（S:786），pipeline的资源目录仍是build/lib64/clang/22（H:1163/1166）。不能把build/、lib64/或安装根当BOLT工具目录整树清掉。

Source1005的 `build/native-archive-conversion` 也不是BOLT自有目录，它在OFF仍执行（S:527–539只有架构条件）。它已有自己的生命周期：A:649在IR设置取完后删`.ll`；A:704–707每档归档验证后删提取的bitcode/本地对象；A:744–747逐档安装新归档；A:752调用 `cleanup_evidence`，A:581–587删除archives和非JSON，只留审计JSON。S:530还会在运行前清掉上轮转换目录。这些现有行为本轮只分析，不修改，也不能借BOLT清理扩大范围。

## 7. 仅用29号已有数字作峰值估算

29号不是一轮完成的9e ON/OFF对照。它给出：

| 29号来源 | 数值 | 允许如何使用 |
|---|---:|---|
| 29号L69–82，历史无BOLT第579样本 | 236,149,145,600B = **219.931GiB** | 整个GBS根已观测下界；不是9e OFF完整峰值。样本位于普通安装/静态转换末段，平台后处理前 |
| 29号L108，13号温缓存端点 | 96,877,810,360B = **90.224GiB**，47,107文件 | 普通构建既有cache文件总大小；不是BOLT新增量，也未给同一时点独立du回收量 |
| 29号L100，25号未完成演练 | 工具+工作+上层cache共12,247,695,360B = **11.407GiB** | 冷cache、overlay上层、中止在重链的保留终点；不能认证“BOLT净增峰值12–15GiB” |
| 29号L102，安装上层 | **49.031GiB** | 普通BUILDROOT，S:421在BOLT清理候选点之前已产生；不是BOLT新增第二份安装目录 |
| 29号L108，重链输入端点 | strip前3,560,483,168B；strip后226,738,888B | 中间文件端点；不足以重建完整时间序列峰值 |

**估算一：后续阶段。** 若在建议的S:492之后清理，并假定当时cache仍约96.88GB且实际分配接近文件总大小，则静态库转换、平台后处理和打包阶段的根占用，相比不清理的同一时刻，可能少约 **90.22GiB**。这是后续时点减量，不是整轮峰值实测。将历史219.931GiB样本机械减去90.224GiB会得到129.707GiB，**只能作同一时点假设下的算术示例，不能写成清理后的构建峰值**。

**估算二：整个构建峰值。** 设清理前各阶段的最高占用为A，后续不清理时的最高占用为B，可实际释放的cache为C：

```text
原峰值 = max(A, B)
清理后峰值 ≈ max(A, B - C)
峰值降低 ≈ min(C, max(0, B - A))
```

因此在C≈90.22GiB的假设下，整轮降低可能从 **0到约90.22GiB**；若A已经最高，就几乎不降全局峰值，只给后续阶段腾空间。该公式假设比较后段保留的cache大小相同；真实cache会自动淘汰/增长，C仍需现场采样。

**峰值可能移到的阶段（推测）：** 普通CMake安装完成后、BOLT工具构建/重链/strip期间，也可能仍在静态转换或debug打包期间，取决于两段的实际最大值。理由是S:421先形成普通BUILDROOT，S:466再留ordinary副本，S:480/485还需要缓存；到建议S:492才清理，之前的重叠占用无法回溯消除。29号没有A/B的同条件完整曲线，也缺post后半程样本，所以不能定量断言一定在哪一步达到峰值或会下降多少。

计算原始输入与公式见 [estimate.json](../../tools/bolt/results/cache-lifetime-20261022/estimate.json)。本轮未使用31号其他目录的释放量来充当构建优化收益，也没有把用户背景中的12–15GiB估计升级成实测结论。

## 8. 后续方向与本轮交付边界

- 若目标是给后处理腾空间，优先考虑§4的BOLT成功块内清理cache；先确认独占路径与没有并行链接，并保留四次report及失败诊断。严格禁止任何后续路径读取时，只能选择最后report之后，收益边界更小。
- BOLT对象/库、中间clang按§6各自最后使用点清理；不能在pipeline后立即删 `clang.bolt`，更不能删post还要用的ordinary/state。诊断读取现存中间文件做预测，提前清理必须一起认证诊断准确性，不能只验证最终clang能运行。
- 若后续获准实现，再以连续根du与阶段端点测量A/B/C，验证clang、逐包文件SHA、debugsource以及tool-plan/compare-root/post；本轮不运行这些构建认证。

只新增本文与 [cache-lifetime-20261022](../../tools/bolt/results/cache-lifetime-20261022/) 中的固定源码、原文摘录、历史旁证和只读统计结果。未删除任何文件或缓存，未运行历史评审脚本、源码helper、Source1005或cmake/ninja，未创建分支或访问Gerrit。查找时修正了POSIX sh不展开的花括号文件名、错误证据仓库相对temp范围，并用 `rg --files --no-ignore` 定位被忽略的历史tar；这些只发生在查找阶段，没有产品操作，也没有把查找失败作为证据缺失的最终结论。完成后停止，等待下一步指令。
