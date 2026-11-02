# clang hybrid + BOLT 外部评审材料（2026-11-02）

评审方请阅读 [0002-text-only.diff](0002-text-only.diff)，而不是 12.7 MB 的完整补丁；此文件仅排除 profile 二进制，完整补丁用于完整应用。

本包取代 `patches/review-20261028/` 的旧材料；旧目录原样保留。本轮仅更正 BOLT 提交说明中的三个段落，代码 tree 与已验证的 3ee2d847 完全相同，没有重新构建，也没有推送 Gerrit、sandbox 或操作 QB。

## 改动目标与补丁顺序

以 `67619ec8bbbac7238a6cfc33a481ccfbcd12206f` 为基线，先应用混合链接提交 `6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2`，再应用本包的 BOLT 提交 `219f23edaffbd84434caf912e261ddb72a4eee2e`。这两个提交是顺序依赖关系，不能把第二份单独应用在基线上。

- hybrid：x86_64 的 clang、lld、llvm-ar 保留对 LLVM/Clang 的静态链接，其余工具使用共享库，减少普通完整构建的 ThinLTO 和磁盘开销。具体例外和安装目标验收见 main 的53号文档；不把内部验收当成外部评审。
- BOLT：x86_64 默认开启，用现有 profile v2 重写 clang；改写后保持可运行性、安全属性、安装路径和编译结果，并给调试模式安装匹配的函数符号。
- 两份补丁由 `git format-patch --binary --full-index --no-signature` 生成。与10月28日包不同，本包包含 Source1200 的完整 Git 二进制补丁，不需要用占位文件替代 profile。
- `files/` 是两个提交触及的全部8个文本文件的最终完整版本，不是只提取修改片段。六个 CMake 文件、spec 和 helper 均从最终 tree 读取，没有手工改写。
- 两份 `*-commit-message.txt` 是各自完整提交说明；`commit-message.diff` 是本次三处说明更正；`SHA256SUMS` 覆盖除清单自身以外的全部文件，包括本 README，避免自引用哈希。

## 整体流程

正常 LLVM 构建和普通安装先完成，记录安装清单与普通 clang 的身份。然后仅在开启 BOLT 的 x86_64 分支中追加 bolt 配置，检查 dry-run 白名单并构建 llvm-bolt；重放 clang 链接命令加 `--emit-relocs`，再 strip-debug，使用 profile v2 与 `-use-old-text` 重写。

profile 双门禁、BOLT 标识、tiny/真实对象检查贯穿流水线；调试模式先用 eu-strip 分离符号，再 strip-all，修 RUNPATH，再加 `.gnu_debuglink` 和 CRC 检查。后续安全属性、tiny/real 与 compare-root 均需通过；再释放本树 ThinLTO 缓存，按原顺序转换静态归档，原子替换 clang，并在调试模式安装符号文件。平台原有后处理链只执行一次，最后由 BOLT post 校验身份、符号文件、RUNPATH 与反向产物检查。

这里是顺序摘要，不表示所有门禁都推迟到 debuglink 后；源码中的 pre-strip、pre-install、post 三处 real 检查均保留。没有第二次完整 CMake 安装，没有磁盘预留门槛；磁盘记录和失败诊断不改写普通构建或平台后处理。

## debug / release 与回退

| 模式 | clang | 调试包与定位 |
|---|---|---|
| debug（llvm_release_build=0） | 完全 strip，随后添加 `.gnu_debuglink`；RUNPATH `$ORIGIN/../lib64` | `/usr/lib/debug/usr/bin/clang-22.debug`，0644；函数名/冷片段可定位，没有源码行 DWARF |
| release | 完全 strip，不加 debuglink | 不生成/安装该符号文件；崩溃排查仍需保全 build-side 身份与重写记录、pre-strip ELF、匹配 ordinary ELF、工具与profile身份 |

x86_64 默认 `%bcond_without clang_bolt`。本地可用 `--without clang_bolt` 关闭；QB 参数不可调整时，回退方式是提交单行 spec 修改，把 x86_64 的 bcond_without 改为 bcond_with。不能把本包当作已执行回退。Source1200/1201 始终无条件声明，避免 GBS 生成的 Patch 声明被架构/开关条件屏蔽；其他架构不执行 BOLT。

## 关键验证与证据

以下为既有同 tree 或前序实现的实测，本轮不重跑构建。证据链接固定到打包前的 bolt-v4 文档提交 `0dc274528111434f03854b17f6c24109e68e80fe`，避免后续文档变化混淆。

| 证据 | 结论及范围 |
|---|---|
| [39：old-text定版](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/0dc274528111434f03854b17f6c24109e68e80fe/docs/bolt/39_use_old_text_final.md) | old-text完整构建、门禁、23包与90TU通过；无debuglink的最终clang为152,532,296B，RUNPATH正确；该轮尚未实现匹配符号包 |
| [43：debuglink认证，第9节](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/0dc274528111434f03854b17f6c24109e68e80fe/docs/bolt/43_debuginfo_symbols.md) | full-20261030完整产出22个二进制RPM+1个源码RPM；113/113工具任务，profile R=0.0042385453312%、S=0；23包对比和90/90完整对象一致。ar日期271项单列，不混作字节内容相同 |
| [43：第13节安装实测](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/0dc274528111434f03854b17f6c24109e68e80fe/docs/bolt/43_debuginfo_symbols.md) | 新chroot装包通过，LLDB自动加载符号；真实SIGILL中21/21 clang帧有函数名，llvm-symbolizer一致；main+5个冷函数6/6一致。第9节最初未完成的安装项已在此闭合 |
| [37：RUNPATH修复与实验](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/0dc274528111434f03854b17f6c24109e68e80fe/docs/bolt/37_runpath_and_improvements.md) | RUNPATH、工具并行构建和real检查通过；old-text初始实验及其比较口径详见第10节 |
| [main/53：hybrid验收](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/main/docs/53_hybrid_local_validation.md) | 第7节PM裁决PASS，附非安装目标N/A、--as-needed插件例外、既有脚本运行环境限制；不是宣称188个目标全部无例外产出 |

原始证据 GitHub 路径：

- `tools/bolt/results/oldtext-final-20261027/`（39号）。
- `tools/bolt/results/debuglink-20261028/full-20261030/`（完整构建、身份、逐包与90TU）。
- `tools/bolt/results/debuglink-20261028/install-test-20261102-resume3/`（装包、LLDB、崩溃栈和symbolizer）。
- `tools/bolt/results/runpath-fix-20261026/`（37号）。
- main 的 `docs/53_hybrid_local_validation_evidence/`。

debuglink实体为152,532,400B，符号文件35,243,936B。相对39号，clang RPM增加3,692B、clang-debuginfo RPM增加3,862,828B；符号分离3.242s、debuglink添加1.940s（仅这两项，不等于全部新增校验成本）。完整构建8159.098s，不是与另一机器/另一轮的受控耗时比较。最终clang SHA `4f08e12d499ebd492ce4951f74915ba435f57f2e380dc6f3520f24644996cb17`；符号文件SHA `be17f7222b30b9aff8e9cb30847b7348c5b9897096e382518410dfb053c2f281`。

## 已知限制与挂账

- release 模式仍需完整构建认证；已有展开/小实验不能替代完整打包。
- 目前实现函数级定位，不提供源码行；BOLT同步更新DWARF的成本/方案仍待实验。
- LLVM `llvm-objcopy --only-keep-debug` 在该BOLT ELF上的缺陷另行修复，本实现使用 eu-strip；不宣称已经修复上游工具。
- 当前 revision 的 QB 验证仍待完成；较早版本的QB `%install`成功不代表本版本通过。本轮不操作QB、不查询其即时状态、不更新sandbox。
- 已验证的运行时性能限于记录的训练/测量工作负载，不能推广成所有Tizen软件的收益；profile双门禁继续严格执行。
- 原普通clang含DWARF，不能把它与strip后的候选的总文件大小差异全部归因于BOLT；本包按同工具 `--strip-all` 后的139,929,432B比较，见 size-baseline.md。

## 校验与应用

在本包目录执行 `sha256sum -c SHA256SUMS`。在另一个基于67619ec8的源码工作区按0001→0002应用；本轮已用独立临时index应用两份完整补丁，最终tree为 `43d60f7523439fa0ccf4a61f668dd60622554606`，与3ee2d847逐字对应，PASS。此项只验证补丁完整性，不运行构建。


## 本次提交说明更正与身份

只替换三个指定句子，句子内部重新折行，其他字符逐字保持：体积改为 old-text+debuglink 的同口径实测；build-side崩溃排查限制限定为release模式；QB历史成功与本revision待验证分开。作者行（含作者时间）、父提交、Change-Id、Signed-off-by保持原样，提交者为Hao Lin。完整diff与可机器核对的三段替换分别为 `commit-message.diff` 和 `evidence/message-replacements.json`。

- 新BOLT提交：`219f23edaffbd84434caf912e261ddb72a4eee2e`（仅在 `W/temp/review-20261102/source` 的detached HEAD本地保留，未推送）。
- 父提交：`6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2`；基线：`67619ec8bbbac7238a6cfc33a481ccfbcd12206f`。
- tree：`43d60f7523439fa0ccf4a61f668dd60622554606`，与原debuglink提交相同，沿用43号代码验证。
- BOLT Change-Id：`Ic98eab90cc017f127a66e1729b44fab8b8e8fb41`。
- PGO使用的原源码工作区仍保持3ee2d847，本任务没有检出、提交或写入它，也没有访问修改 `temp/pgo-resource-20261102/`。
- 新尺寸说明：152,532,400B，相对stripped ordinary增加12,602,968B（+9.0%）；104B来自debuglink。完整argv、SHA、计算和历史来源见 [size-baseline.md](size-baseline.md)。
- profile：`packaging/clang-bolt-v2.fdata.xz`，9,735,212B，SHA256 `52fd8522b8cceadebfb6bfc0a19f721f1072cff95c682b12b2c4dd5b0cc1e27f`；内容在0002的二进制补丁中。

## 文件与 raw 链接

下表列出主要材料；每个文件（包括证据和README）的字节SHA见 [SHA256SUMS](SHA256SUMS)，清单本身不自哈希。分支raw用于浏览，钉提交版请将URL中的bolt-v4替换为发布本包的证据仓库提交SHA。

| 文件 | 用途 |
|---|---|
| [0001-cmake-use-hybrid-LLVM-linkage-on-x86_64.patch](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261102/0001-cmake-use-hybrid-LLVM-linkage-on-x86_64.patch) | 完整混合链接补丁 |
| [0002-text-only.diff](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261102/0002-text-only.diff) | 评审用，不含 profile 二进制；完整补丁见 [0002-packaging-optimize-x86_64-clang-with-BOLT.patch](0002-packaging-optimize-x86_64-clang-with-BOLT.patch) |
| [0002-packaging-optimize-x86_64-clang-with-BOLT.patch](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261102/0002-packaging-optimize-x86_64-clang-with-BOLT.patch) | 完整BOLT补丁，包含profile二进制 |
| [0001-commit-message.txt](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261102/0001-commit-message.txt) | hybrid完整说明 |
| [0002-commit-message.txt](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261102/0002-commit-message.txt) | 新BOLT完整说明 |
| [commit-message.diff](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261102/commit-message.diff) | 仅三处提交说明差异 |
| [size-baseline.md](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261102/size-baseline.md) | 体积实测、argv与历史口径 |
| [generation.json](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261102/generation.json) | 基线、提交、文件集合和完整应用验证 |
| [SHA256SUMS](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261102/SHA256SUMS) | 全部文件校验清单 |
| [files/clang/cmake/modules/AddClang.cmake](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261102/files/clang/cmake/modules/AddClang.cmake) | 最终完整文件 |
| [files/clang/tools/driver/CMakeLists.txt](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261102/files/clang/tools/driver/CMakeLists.txt) | 最终完整文件 |
| [files/lld/cmake/modules/AddLLD.cmake](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261102/files/lld/cmake/modules/AddLLD.cmake) | 最终完整文件 |
| [files/lld/tools/lld/CMakeLists.txt](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261102/files/lld/tools/lld/CMakeLists.txt) | 最终完整文件 |
| [files/llvm/cmake/modules/AddLLVM.cmake](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261102/files/llvm/cmake/modules/AddLLVM.cmake) | 最终完整文件 |
| [files/llvm/tools/llvm-ar/CMakeLists.txt](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261102/files/llvm/tools/llvm-ar/CMakeLists.txt) | 最终完整文件 |
| [files/packaging/clang-bolt-helper.py](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261102/files/packaging/clang-bolt-helper.py) | 最终完整文件 |
| [files/packaging/llvm.spec](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261102/files/packaging/llvm.spec) | 最终完整文件 |
