# Tizen Base LLVM / clang-accel RPM 体积事实与逐文件证据

对象：基线 `tizen-base-toolchain_20260914.073422` 与优化快照 `tizen-base-toolchain_20261015.022255`。本文中的“旧/新”只表示这两个快照。快照、实际包版本、下载 URL、SHA256、RPM payload 元数据见 [rpm_metadata.csv](rpm_metadata.csv)，原始下载记录为 [raw/fetch_manifest.jsonl:1](raw/fetch_manifest.jsonl#L1) 起。

x86_64 clang、llvm 和 llvm-devel 的主要文件增量落在满足“旧版依赖 libLLVM/libclang-cpp，新版不再依赖对应库”规则的 ELF 上。clang-accel 中大部分文件与指定来源 RPM 不同 SHA256，必须保留为“无匹配”；qemu-accel 两端源码的 clang 收录和 strip 规则未变化。下面给出机械分类和逐项证据，不把多个编译选项、不同源码提交或打包处理的作用分摊为未经验证的因果比例。

## 采集范围和计量口径

工作目录采用用户已确认的当前工作区 `/home/toolchain/Desktop/tmp_hfy/qb_analysis/llvm-optimize`。开始前 temp 所在磁盘可用 **213,247,823,872 bytes**，记录在 [raw/preflight.txt:1-6](raw/preflight.txt#L1)。本轮 RPM 和解包内容仅放 `temp/qb_size/`，每个包依次下载、解包、记录，再删除该包解包目录。没有编译、安装 RPM、执行产品脚本、修改产品代码或提交 Gerrit。

采集覆盖用户指定的全部 RPM；下载与解包串行，源码下载同时最多两路，总下载并发未超过用户上限。采集服务 CPU 配额为单核的 25%，MemoryMax 为 768 MiB；配置原文及成功退出状态见 [raw/package_resource_limits.txt:1](raw/package_resource_limits.txt#L1) 起，逐包完成/删除记录见 [raw/package_collection_journal.txt:1](raw/package_collection_journal.txt#L1) 起。

本文所有大小均为 bytes，不把目录网页四舍五入的 MB 用作计算输入。`rpm_bytes` 是下载到的压缩 RPM 文件大小；`path_bytes` 是全部路径的 regular 文件长度加符号链接文本长度，目录记零。对缺失路径，差值计算用零，同时明确标记“仅旧有/仅新有”，不把零当成已取得的文件。每个 regular 文件 SHA256 与 RPM 头中 FILEDIGESTS 一致，解包大小与 FILESIZES 一致；按路径和按物理 regular 文件去重的合计相同。核验见 [raw/validation.json:1-12](raw/validation.json#L1) 和各包 `*_complete.json`。

压缩流无法按单个文件无损分摊为 RPM 增量。因此以下分类占比的分母固定为**解包路径大小净增量**，不是 RPM 压缩增量。没有给出压缩后各类字节的估算；该项为“未获取：RPM 使用整体 payload 压缩，现有证据不能提供逐文件压缩贡献”。

## RPM 总量、版本和压缩格式

| 架构 / 包 | 旧 RPM | 新 RPM | RPM 增量 | 旧路径总量 | 新路径总量 | 路径净增量 | raw 证据 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| armv7l / clang | 20,908,589 | 21,194,993 | 286,404 | 83,053,598 | 80,088,546 | -2,965,052 | [raw/analysis_facts.jsonl:1](raw/analysis_facts.jsonl#L1) |
| armv7l / clang-accel-x86_64-armv7l | 54,806,369 | 659,624,309 | 604,817,940 | 239,912,044 | 2,756,647,372 | 2,516,735,328 | [raw/analysis_facts.jsonl:10](raw/analysis_facts.jsonl#L10) |
| armv7l / llvm | 6,326,401 | 6,522,761 | 196,360 | 19,005,897 | 17,808,101 | -1,197,796 | [raw/analysis_facts.jsonl:19](raw/analysis_facts.jsonl#L19) |
| x86_64 / clang | 29,048,537 | 309,990,089 | 280,941,552 | 146,690,147 | 1,321,214,032 | 1,174,523,885 | [raw/analysis_facts.jsonl:28](raw/analysis_facts.jsonl#L28) |
| x86_64 / libllvm | 21,243,613 | 23,650,253 | 2,406,640 | 83,596,278 | 90,738,518 | 7,142,240 | [raw/analysis_facts.jsonl:37](raw/analysis_facts.jsonl#L37) |
| x86_64 / llvm | 16,780,897 | 410,626,521 | 393,845,624 | 69,348,485 | 1,683,790,149 | 1,614,441,664 | [raw/analysis_facts.jsonl:46](raw/analysis_facts.jsonl#L46) |
| x86_64 / llvm-devel | 5,327,809 | 41,191,657 | 35,863,848 | 37,024,727 | 172,451,936 | 135,427,209 | [raw/analysis_facts.jsonl:55](raw/analysis_facts.jsonl#L55) |

精确版本：旧 x86_64 LLVM 系列为 `22.1.8-1.6`，旧 armv7l clang/llvm 为 `22.1.8-1.7`；新 LLVM 系列为 `22.1.8-3.1`。clang-accel 为旧 `0.4-1.1`、新 `0.4-2.2`。每个包分别可查 `raw/{old,new}_{arch}_{package}_rpm_header.txt:1-6`，例如 [raw/old_x86_64_clang_rpm_header.txt:1-6](raw/old_x86_64_clang_rpm_header.txt#L1)、[raw/old_armv7l_clang_rpm_header.txt:1-6](raw/old_armv7l_clang_rpm_header.txt#L1)、[raw/new_armv7l_clang-accel-x86_64-armv7l_rpm_header.txt:1-6](raw/new_armv7l_clang-accel-x86_64-armv7l_rpm_header.txt#L1)。

全部 **14** 个 RPM 的 `PAYLOADCOMPRESSOR=xz`、`PAYLOADFLAGS=5T`，未观察到压缩格式或该头字段标志变化；逐包原文在 header 文件第 5–6 行，合计见 [raw/coverage_facts.jsonl:47](raw/coverage_facts.jsonl#L47)。相同格式不代表相同压缩率。armv7l clang/llvm 的 RPM 增大而解包文件总量减少，两个口径都保留在上表。

## 源码提交、完整 diff 和对应范围

LLVM 精确区间 `8dfebafe1a477b3dcc678ee4cb18a3a4306d5a7c..67619ec8bbbac7238a6cfc33a481ccfbcd12206f` 的全部提交如下。作者按原始历史记录保留，日期为 author date；CSV 另列 cgit 页面中的 committer date。

| 提交 | 原始作者 | 作者日期 | 标题 | raw 证据 |
| --- | --- | --- | --- | --- |
| 6771dbc48b7e3db2ec53919a8eebd3514374137b | lhmax2025 <hao.lin@samsung.com> | Tue, 1 Sep 2026 16:15:34 +0900 | libcxx: backport EH ABI forced-unwind handling | [raw/llvm_range.patch:1-5](raw/llvm_range.patch#L1)<br>[raw/llvm_range_log.html:275](raw/llvm_range_log.html#L275) |
| 2d23367d74afbf2bb1e9e4013fce072b3a154109 | He Fangyu <fangyu.he@samsung.com> | Wed, 2 Sep 2026 18:07:18 +0800 | packaging: select Clang explicitly for libc++ runtimes | [raw/llvm_range.patch:1005-1009](raw/llvm_range.patch#L1005)<br>[raw/llvm_range_log.html:253](raw/llvm_range_log.html#L253) |
| 7e4dc62d8ac01f90488a0cc8e0f34f8373228c84 | "fangyu.he" <fangyu.he@samsung.com> | Thu, 24 Sep 2026 12:55:12 +0800 | optimize llvm performance | [raw/llvm_range.patch:1070-1074](raw/llvm_range.patch#L1070)<br>[raw/llvm_range_log.html:243](raw/llvm_range_log.html#L243) |
| cb67996861d070d68fec2b4c623eed7d20ba2e23 | "fangyu.he" <fangyu.he@samsung.com> | Wed, 30 Sep 2026 16:41:10 +0800 | remove '-fno-inline-functions' compile options | [raw/llvm_range.patch:1176-1180](raw/llvm_range.patch#L1176)<br>[raw/llvm_range_log.html:229](raw/llvm_range_log.html#L229) |
| 67619ec8bbbac7238a6cfc33a481ccfbcd12206f | FatTank <hao.lin@samsung.com> | Fri, 9 Oct 2026 16:58:36 +0800 | packaging: fix llvm-static-devel with ThinLTO | [raw/llvm_range.patch:1218-1222](raw/llvm_range.patch#L1218)<br>[raw/llvm_range_log.html:173](raw/llvm_range_log.html#L173) |

完整最终 packaging diff 为 [raw/llvm_packaging_complete.diff](raw/llvm_packaging_complete.diff)，逐字节筛自 [raw/llvm_full.diff](raw/llvm_full.diff) 的全部 `packaging/` diff 块；来源说明见 [raw/derived_source_provenance.txt:1](raw/derived_source_provenance.txt#L1)。完整提交补丁序列另存 [raw/llvm_range.patch](raw/llvm_range.patch)。

qemu-accel 正向 `e01aa7250a1a73aa8f88ba9ac4a05cbc954d1c9f..2737f3bf78ed33be4333114c0e5c741a1deca467` 与补充的反向提交集合均列出，防止把正向提交标题误认为端点树差异：

| 方向 | 提交 | 作者 | 作者日期 | 标题 | raw 证据 |
| --- | --- | --- | --- | --- | --- |
| old..new | 2737f3bf78ed33be4333114c0e5c741a1deca467 | Dongkyun Son <dongkyun.s@samsung.com> | Wed, 9 Sep 2026 08:12:26 +0900 | Add libabigail binaries to qemu-accel for native ABI analysis | [raw/qemu-accel_range.patch:1-5](raw/qemu-accel_range.patch#L1) |
| new..old（补充反向集合） | 06b287039cd401739123946f47c01977de5c925f | Dongkyun Son <dongkyun.s@samsung.com> | Wed, 9 Sep 2026 08:12:26 +0900 | Add libabigail binaries to qemu-accel for native ABI analysis | [raw/qemu-accel_reverse_range.patch:1-5](raw/qemu-accel_reverse_range.patch#L1) |
| new..old（补充反向集合） | e01aa7250a1a73aa8f88ba9ac4a05cbc954d1c9f | Dongkyun Son <dongkyun.s@samsung.com> | Wed, 9 Sep 2026 09:41:02 +0900 | hack: add dash to BuildRequires | [raw/qemu-accel_reverse_range.patch:127-131](raw/qemu-accel_reverse_range.patch#L127) |

qemu-accel 的完整端点 diff 为 [raw/qemu-accel_full_retry.diff](raw/qemu-accel_full_retry.diff)：各架构 spec 及模板仅删除 `BuildRequires:  dash`。两端完整 armv7l spec 独立作文本 diff 得到同一行删除，见 [raw/qemu_armv7l_endpoint_spec.diff:1-10](raw/qemu_armv7l_endpoint_spec.diff#L1)。正向 `2737f3bf` 与反向 `06b28703` 均包含 libabigail 增补，不能把这批工具当作两个快照之间的新增工具。

[source_changes.csv](source_changes.csv) 保存最终 diff 和提交序列中**每条增删行**的文件、原/新行号、原文、主题及 raw 行号；不是只保留关键词命中的摘要。`scope=endpoint_*` 是最终差异，`commit_series` 是途中改动，不能重复计数。[source_to_categories.csv](source_to_categories.csv) 对每条记录给出分类主题对应或“未对应”及限制。

| 源码位置 / 原文 | 可对应的观测类别 | 限制 / raw 证据 |
| --- | --- | --- |
| `llvm.spec`: `-DLLVM_LINK_LLVM_DYLIB=OFF`、`-DCLANG_LINK_CLANG_DYLIB=OFF`，在 `%ifarch x86_64` 中 | 链接方式变化 | 目标库依赖变化逐文件核对；[raw/llvm_new_llvm.spec:279-289](raw/llvm_new_llvm.spec#L279) |
| `llvm.spec`: C/CXX flags 清除既有选项并追加 `-O3 -flto=thin -fomit-frame-pointer`；显式 clang/clang++ | 代码节变大（只作选项主题对应） | 多个选项及源码同时变化，单项效果未对应；[raw/llvm_new_llvm.spec:200-243](raw/llvm_new_llvm.spec#L200) |
| `llvm.spec`: 链接 flags 增加 ThinLTO、`LLVM_ENABLE_LTO=Thin`、llvm-ar/ranlib | 代码节变大（只作选项主题对应） | 条件是 `%if %{defined _toolchain}`，不能概括为仅 x86_64；[raw/llvm_new_llvm.spec:250-257](raw/llvm_new_llvm.spec#L250) |
| 新增 `llvm-static-archives-native.py`，x86_64 `%install` 调用，保留 archive strip -g | 未对应 | 处理静态归档，本轮没有 llvm-static-devel 样本；不能分配到工具 ELF 增量；[raw/llvm_packaging_complete.diff:240-245](raw/llvm_packaging_complete.diff#L240)、[raw/llvm_new_llvm.spec:429-441](raw/llvm_new_llvm.spec#L429) |
| 新增 libcxx-runtimes.spec、manifest、map 和来源记录；运行库编译器改动 | 未对应 | 运行库子包不在本轮 RPM 集合；[raw/llvm_packaging_complete.diff:1-239](raw/llvm_packaging_complete.diff#L1) |
| qemu-accel 最终差异仅删除 dash 构建依赖 | 未对应 | 未取得将该依赖删除对应到任一目标文件增量的证据；[raw/qemu-accel_full_retry.diff:1-48](raw/qemu-accel_full_retry.diff#L1) |
| qemu-accel 的 clang 文件列表、strip、压缩、子包划分 | 最终 diff 未变化 / 未对应新增源码改动 | 完整端点 spec 与全文 diff 可复查；上下文逐行索引见 [source_context.csv](source_context.csv) |

LLVM 主 `packaging/llvm.spec` 的 `%files` 列表在端点 diff 中没有改动；新增运行库 spec 自带 `%files`，已经完整纳入逐行表。没有把“源码中新建打包脚本”当作“RPM 中新增文件”。

## 逐文件增量和 ELF 明细

[files_compare.csv](files_compare.csv) 是全部包按完整路径配对的结果，包含旧/新大小、差值、存在性、类型、SHA256、分类和原始行号。[top30_files.csv](top30_files.csv) 对每个包按差值降序、路径字典序打破同值排序，保留前 30 个非目录路径；少于 30 个时全部列出，零值和负值没有伪造为增长。

以下是每包最大增量的实际路径，完整排行见 CSV：

| 架构 / 包 | 路径 | 旧大小 | 新大小 | 差值 | raw 证据 |
| --- | --- | --- | --- | --- | --- |
| armv7l / clang | `/usr/lib/libclang.so.22.1.8` | 16,611,424 | 16,817,208 | 205,784 | [raw/old_armv7l_clang_files.jsonl:355](raw/old_armv7l_clang_files.jsonl#L355)<br>[raw/new_armv7l_clang_files.jsonl:355](raw/new_armv7l_clang_files.jsonl#L355) |
| armv7l / clang | `/usr/bin/armv7l-tizen-linux-gnueabi-clang` | 5 | 5 | 0 | [raw/old_armv7l_clang_files.jsonl:1](raw/old_armv7l_clang_files.jsonl#L1)<br>[raw/new_armv7l_clang_files.jsonl:1](raw/new_armv7l_clang_files.jsonl#L1) |
| armv7l / clang | `/usr/bin/armv7l-tizen-linux-gnueabi-clang++` | 7 | 7 | 0 | [raw/old_armv7l_clang_files.jsonl:2](raw/old_armv7l_clang_files.jsonl#L2)<br>[raw/new_armv7l_clang_files.jsonl:2](raw/new_armv7l_clang_files.jsonl#L2) |
| armv7l / clang-accel-x86_64-armv7l | `/emul/usr/bin/clang-repl` | 61,400 | 144,021,680 | 143,960,280 | [raw/old_armv7l_clang-accel-x86_64-armv7l_files.jsonl:28](raw/old_armv7l_clang-accel-x86_64-armv7l_files.jsonl#L28)<br>[raw/new_armv7l_clang-accel-x86_64-armv7l_files.jsonl:28](raw/new_armv7l_clang-accel-x86_64-armv7l_files.jsonl#L28) |
| armv7l / clang-accel-x86_64-armv7l | `/emul/usr/bin/clang-22` | 131,592 | 141,497,504 | 141,365,912 | [raw/old_armv7l_clang-accel-x86_64-armv7l_files.jsonl:8](raw/old_armv7l_clang-accel-x86_64-armv7l_files.jsonl#L8)<br>[raw/new_armv7l_clang-accel-x86_64-armv7l_files.jsonl:8](raw/new_armv7l_clang-accel-x86_64-armv7l_files.jsonl#L8) |
| armv7l / clang-accel-x86_64-armv7l | `/emul/usr/bin/clang-check` | 44,104 | 95,232,088 | 95,187,984 | [raw/old_armv7l_clang-accel-x86_64-armv7l_files.jsonl:11](raw/old_armv7l_clang-accel-x86_64-armv7l_files.jsonl#L11)<br>[raw/new_armv7l_clang-accel-x86_64-armv7l_files.jsonl:11](raw/new_armv7l_clang-accel-x86_64-armv7l_files.jsonl#L11) |
| armv7l / llvm | `/usr/bin/llvm-tblgen` | 2,016,956 | 2,085,588 | 68,632 | [raw/old_armv7l_llvm_files.jsonl:88](raw/old_armv7l_llvm_files.jsonl#L88)<br>[raw/new_armv7l_llvm_files.jsonl:88](raw/new_armv7l_llvm_files.jsonl#L88) |
| armv7l / llvm | `/usr/bin/llvm-readobj` | 1,038,168 | 1,049,912 | 11,744 | [raw/old_armv7l_llvm_files.jsonl:76](raw/old_armv7l_llvm_files.jsonl#L76)<br>[raw/new_armv7l_llvm_files.jsonl:76](raw/new_armv7l_llvm_files.jsonl#L76) |
| armv7l / llvm | `/usr/bin/llvm-cxxfilt` | 14,580 | 14,608 | 28 | [raw/old_armv7l_llvm_files.jsonl:33](raw/old_armv7l_llvm_files.jsonl#L33)<br>[raw/new_armv7l_llvm_files.jsonl:33](raw/new_armv7l_llvm_files.jsonl#L33) |
| x86_64 / clang | `/usr/bin/clang-22` | 120,608 | 139,929,464 | 139,808,856 | [raw/old_x86_64_clang_files.jsonl:5](raw/old_x86_64_clang_files.jsonl#L5)<br>[raw/new_x86_64_clang_files.jsonl:5](raw/new_x86_64_clang_files.jsonl#L5) |
| x86_64 / clang | `/usr/bin/clang-check` | 40,544 | 95,220,448 | 95,179,904 | [raw/old_x86_64_clang_files.jsonl:8](raw/old_x86_64_clang_files.jsonl#L8)<br>[raw/new_x86_64_clang_files.jsonl:8](raw/new_x86_64_clang_files.jsonl#L8) |
| x86_64 / clang | `/usr/bin/clang-tidy` | 11,903,760 | 97,926,712 | 86,022,952 | [raw/old_x86_64_clang_files.jsonl:25](raw/old_x86_64_clang_files.jsonl#L25)<br>[raw/new_x86_64_clang_files.jsonl:25](raw/new_x86_64_clang_files.jsonl#L25) |
| x86_64 / libllvm | `/usr/lib64/libLLVM.so.22.1` | 83,596,248 | 90,738,488 | 7,142,240 | [raw/old_x86_64_libllvm_files.jsonl:3](raw/old_x86_64_libllvm_files.jsonl#L3)<br>[raw/new_x86_64_libllvm_files.jsonl:3](raw/new_x86_64_libllvm_files.jsonl#L3) |
| x86_64 / libllvm | `/usr/lib64/libLLVM-22.so` | 15 | 15 | 0 | [raw/old_x86_64_libllvm_files.jsonl:1](raw/old_x86_64_libllvm_files.jsonl#L1)<br>[raw/new_x86_64_libllvm_files.jsonl:1](raw/new_x86_64_libllvm_files.jsonl#L1) |
| x86_64 / libllvm | `/usr/lib64/libLLVM.so` | 15 | 15 | 0 | [raw/old_x86_64_libllvm_files.jsonl:2](raw/old_x86_64_libllvm_files.jsonl#L2)<br>[raw/new_x86_64_libllvm_files.jsonl:2](raw/new_x86_64_libllvm_files.jsonl#L2) |
| x86_64 / llvm | `/usr/bin/clang-repl` | 56,272 | 142,400,632 | 142,344,360 | [raw/old_x86_64_llvm_files.jsonl:5](raw/old_x86_64_llvm_files.jsonl#L5)<br>[raw/new_x86_64_llvm_files.jsonl:5](raw/new_x86_64_llvm_files.jsonl#L5) |
| x86_64 / llvm | `/usr/bin/lldb-instr` | 189,280 | 81,583,048 | 81,393,768 | [raw/old_x86_64_llvm_files.jsonl:16](raw/old_x86_64_llvm_files.jsonl#L16)<br>[raw/new_x86_64_llvm_files.jsonl:16](raw/new_x86_64_llvm_files.jsonl#L16) |
| x86_64 / llvm | `/usr/bin/lld` | 6,313,048 | 83,539,336 | 77,226,288 | [raw/old_x86_64_llvm_files.jsonl:13](raw/old_x86_64_llvm_files.jsonl#L13)<br>[raw/new_x86_64_llvm_files.jsonl:13](raw/new_x86_64_llvm_files.jsonl#L13) |
| x86_64 / llvm-devel | `/usr/lib64/libLTO.so.22.1` | 62,992 | 69,314,024 | 69,251,032 | [raw/old_x86_64_llvm-devel_files.jsonl:2470](raw/old_x86_64_llvm-devel_files.jsonl#L2470)<br>[raw/new_x86_64_llvm-devel_files.jsonl:2470](raw/new_x86_64_llvm-devel_files.jsonl#L2470) |
| x86_64 / llvm-devel | `/usr/lib64/LLVMgold.so` | 76,600 | 66,248,512 | 66,171,912 | [raw/old_x86_64_llvm-devel_files.jsonl:2426](raw/old_x86_64_llvm-devel_files.jsonl#L2426)<br>[raw/new_x86_64_llvm-devel_files.jsonl:2426](raw/new_x86_64_llvm-devel_files.jsonl#L2426) |
| x86_64 / llvm-devel | `/usr/lib64/cmake/lld/LLDTargets.cmake` | 6,175 | 9,360 | 3,185 | [raw/old_x86_64_llvm-devel_files.jsonl:2430](raw/old_x86_64_llvm-devel_files.jsonl#L2430)<br>[raw/new_x86_64_llvm-devel_files.jsonl:2430](raw/new_x86_64_llvm-devel_files.jsonl#L2430) |

[elf_detail.csv](elf_detail.csv) 包含 x86_64 clang 的全部 **24** 个 ELF（不足所要求上限）、llvm 增量最大的 **30** 个 ELF，两版分别列出；另加 libLLVM 对照。选择数量与 strip/build-id 检查见 [raw/coverage_facts.jsonl:45-46](raw/coverage_facts.jsonl#L45)。字段包括完整 NEEDED、目标库标志、`.symtab`、所有 `.debug_*`/`.zdebug_*`、指定节大小、build-id，以及 raw readelf 行号。[elf_sections.csv](elf_sections.csv) 把这些 ELF 的全部节逐节列出。[elf_all.csv](elf_all.csv) 保留整个样本中的 ELF 字段，支持核对排行外的分类。

例如 `/usr/bin/clang-22`：旧版 NEEDED 包含 `libclang-cpp.so.22.1` 和 `libLLVM.so.22.1`；新版 NEEDED 不含这两个名称，仍有其他共享库依赖。不能把“不依赖这两个库”写成“整个程序完全静态链接”。证据：[raw/elf/old_x86_64_clang/00005.txt:78-86](raw/elf/old_x86_64_clang/00005.txt#L78)、[raw/elf/new_x86_64_clang/00005.txt:81-91](raw/elf/new_x86_64_clang/00005.txt#L81)。

整个样本的 **646** 个 regular ELF 观测中，`.symtab` 和 `.debug_*`/`.zdebug_*` 均未出现；按本任务定义没有 strip/调试节“有无”变化。`.dynsym` 与 `.gnu_debuglink` 不当作 `.symtab` 或 DWARF 调试节。合计证据：[raw/coverage_facts.jsonl:48](raw/coverage_facts.jsonl#L48)，逐对象 `readelf -S` 原文可由 `elf_all.csv` 追溯。所选排行 ELF 与 libLLVM 对照的 build-id 均为**未获取：readelf -n 没有列出 Build ID**，并非下载失败；每个 CSV 行附对应 note 输出位置。

## libLLVM.so.22.1 动态库对照

| 字段 | 旧 | 新 | 差值 / 状态 | raw 证据 |
| --- | --- | --- | --- | --- |
| 文件大小 | 83,596,248 | 90,738,488 | 7,142,240 | [raw/old_x86_64_libllvm_files.jsonl:3](raw/old_x86_64_libllvm_files.jsonl#L3)<br>[raw/new_x86_64_libllvm_files.jsonl:3](raw/new_x86_64_libllvm_files.jsonl#L3) |
| .text | 51,282,558 | 58,938,494 | 7,655,936 | [raw/elf/old_x86_64_libllvm/00003.txt:47](raw/elf/old_x86_64_libllvm/00003.txt#L47)<br>[raw/elf/new_x86_64_libllvm/00003.txt:47](raw/elf/new_x86_64_libllvm/00003.txt#L47) |
| .rodata | 18,413,664 | 18,556,000 | 142,336 | [raw/elf/old_x86_64_libllvm/00003.txt:41](raw/elf/old_x86_64_libllvm/00003.txt#L41)<br>[raw/elf/new_x86_64_libllvm/00003.txt:41](raw/elf/new_x86_64_libllvm/00003.txt#L41) |
| .data.rel.ro | 1,247,696 | 1,273,248 | 25,552 | [raw/elf/old_x86_64_libllvm/00003.txt:53](raw/elf/old_x86_64_libllvm/00003.txt#L53)<br>[raw/elf/new_x86_64_libllvm/00003.txt:53](raw/elf/new_x86_64_libllvm/00003.txt#L53) |
| .eh_frame | 3,592,380 | 4,316,028 | 723,648 | [raw/elf/old_x86_64_libllvm/00003.txt:44](raw/elf/old_x86_64_libllvm/00003.txt#L44)<br>[raw/elf/new_x86_64_libllvm/00003.txt:44](raw/elf/new_x86_64_libllvm/00003.txt#L44) |
| `.symtab` / 调试节 | 均无 | 均无 | 无有无变化 | [raw/elf/old_x86_64_libllvm/00003.txt:26-65](raw/elf/old_x86_64_libllvm/00003.txt#L26)<br>[raw/elf/new_x86_64_libllvm/00003.txt:26-65](raw/elf/new_x86_64_libllvm/00003.txt#L26) |
| build-id | 未获取 | 未获取 | 两版 note 输出未列出 | [raw/elf/old_x86_64_libllvm/00003.txt:116-120](raw/elf/old_x86_64_libllvm/00003.txt#L116)<br>[raw/elf/new_x86_64_libllvm/00003.txt:116-120](raw/elf/new_x86_64_libllvm/00003.txt#L116) |

两版均为 `DYN (Shared object file)`，完整 NEEDED 集合相同：`ld-linux-x86-64.so.2`, `libc.so.6`, `libdl.so.2`, `libgcc_s.so.1`, `libm.so.6`, `librt.so.1`, `libstdc++.so.6`, `libxml2.so.16`, `libz.so.1`。证据：[raw/elf/old_x86_64_libllvm/00003.txt:8-10](raw/elf/old_x86_64_libllvm/00003.txt#L8)、[raw/elf/new_x86_64_libllvm/00003.txt:8-10](raw/elf/new_x86_64_libllvm/00003.txt#L8)、[raw/elf/old_x86_64_libllvm/00003.txt:77-85](raw/elf/old_x86_64_libllvm/00003.txt#L77)、[raw/elf/new_x86_64_libllvm/00003.txt:77-85](raw/elf/new_x86_64_libllvm/00003.txt#L77)。这是动态库体积/节大小的端点观测；没有单独改变一个优化选项的对照实验，不能从本表分离 O3、ThinLTO 或其它改动各自的作用。

## clang-accel 收录和来源核对

匹配集合严格使用**同一快照 x86_64 clang、llvm、libllvm RPM**，普通文件以完整字节 SHA256 查找所有匹配路径。[clang_accel_sources.csv](clang_accel_sources.csv) 包含每个路径、类型、大小、SHA、所有来源匹配或“无匹配”。符号链接单独按链接文本 SHA256 核对，明确标为“链接文本匹配（非文件内容匹配）”；目录没有文件内容哈希。`llvm-devel` 等不属于用户指定的来源匹配集合，没有用它们补造匹配。

| 快照 | regular 文件数 | 原样匹配数 / bytes | 无匹配数 / bytes | raw 合计证据 |
| --- | --- | --- | --- | --- |
| 旧 | 107 | 2 / 146,346,256 | 105 / 93,565,744 | [raw/coverage_facts.jsonl:43](raw/coverage_facts.jsonl#L43) |
| 新 | 105 | 0 / 0 | 105 / 2,756,647,328 | [raw/coverage_facts.jsonl:44](raw/coverage_facts.jsonl#L44) |

旧版的两项原样匹配为 `/emul/usr/lib64/libLLVM.so.22.1`（来自 libllvm）和 `/emul/usr/lib64/libclang-cpp.so.22.1`（来自 clang）；新版均未收录。对应原文：[raw/old_armv7l_clang-accel-x86_64-armv7l_files.jsonl:113](raw/old_armv7l_clang-accel-x86_64-armv7l_files.jsonl#L113)、[raw/old_x86_64_libllvm_files.jsonl:3](raw/old_x86_64_libllvm_files.jsonl#L3)、[raw/old_armv7l_clang-accel-x86_64-armv7l_files.jsonl:116](raw/old_armv7l_clang-accel-x86_64-armv7l_files.jsonl#L116)、[raw/old_x86_64_clang_files.jsonl:355](raw/old_x86_64_clang_files.jsonl#L355)；新完整列表见 [raw/new_armv7l_clang-accel-x86_64-armv7l_files.jsonl:1-117](raw/new_armv7l_clang-accel-x86_64-armv7l_files.jsonl#L1)。两项移除合计 **−146,346,256 bytes**，共同路径净增加 **2,663,081,584 bytes**，合为包路径净增加 **2,516,735,328 bytes**；合计见 [raw/analysis_facts.jsonl:10-13](raw/analysis_facts.jsonl#L10)。

全部无匹配路径和大小单独列于 [clang_accel_unmatched.csv](clang_accel_unmatched.csv)。无匹配只证明指定集合内没有相同完整文件 SHA，不能证明该文件没有来源于这些 RPM，也不能证明 qemu-accel 源码新增了打包处理。完整 spec 已有 `cp -aL`、修改 interpreter、条件修改 RUNPATH 的逻辑，旧/新文本相同：[raw/qemu-accel_old_armv7l_retry.spec:383-400](raw/qemu-accel_old_armv7l_retry.spec#L383)、[raw/qemu-accel_new_armv7l_retry.spec:382-399](raw/qemu-accel_new_armv7l_retry.spec#L382)。本轮没有修改文件再试图反推 SHA。

两端 spec 同样调用 `prepare_package_list clang` 收录 clang-*、clang++、opt、lli、llc、llvm-*、lld、ld.lld、libLTO.so*、LLVMgold.so*，同时用 ldd 展开依赖；clang 子包从该列表去除 qemu-accel 共有文件。证据：[raw/qemu-accel_new_armv7l_retry.spec:303-346](raw/qemu-accel_new_armv7l_retry.spec#L303)、[raw/qemu-accel_new_armv7l_retry.spec:665-669](raw/qemu-accel_new_armv7l_retry.spec#L665)。strip 禁用宏同样存在于两端 [raw/qemu-accel_old_armv7l_retry.spec:29-31](raw/qemu-accel_old_armv7l_retry.spec#L29)、[raw/qemu-accel_new_armv7l_retry.spec:29-31](raw/qemu-accel_new_armv7l_retry.spec#L29)。完整 diff 没有这些条目的变化。

## 机械归类规则、金额和占比

分类只根据已保存的结构和字节事实执行，规则在 [scripts/analyze_sizes.py](scripts/analyze_sizes.py) 中。每条配对路径保留全部命中标签；为获得可加总结果，另外按以下优先级选取一个主类：新增文件 → 删除文件 → qemu-accel 打包变化 → 链接方式变化 → strip/调试信息变化 → 代码节变大 → 未分类/大小未变。优先级是记账约定，不是因果强弱判断。

| 规则 | 机械条件 |
| --- | --- |
| 链接方式变化 | 同路径两端均为 ELF；旧 NEEDED 中的 libLLVM.so.22.1 或 libclang-cpp.so.22.1 至少一个在新版消失。仍保留完整其它 NEEDED。 |
| 代码节变大 | 同路径两端均为 ELF，完整 NEEDED 集合相同，且 .text/.rodata/.data.rel.ro/.eh_frame 任一节增大。该标签不表示整个文件一定增大；其它节缩小的净结果照实记录。 |
| strip/调试信息变化 | 两端 ELF 的 .symtab 存在性，或 .debug_*/.zdebug_* 节名集合发生变化。只比较节大小但有无不变时不命中此类。 |
| 新增文件 / 删除文件 | 路径仅新版存在 / 仅旧版存在。无新文件时不设虚构增长。 |
| 压缩格式 | 按每包的 PAYLOADCOMPRESSOR/PAYLOADFLAGS 独立比较；不分配解包字节，不混入可加总类别。 |
| qemu-accel 打包变化 | clang-accel 路径任一端 SHA 无匹配，或仅一端收录；这是用户要求的分类标签，不等价于端点打包源码改变。 |
| 未分类 / 大小未变 | 不满足其它条件且文件长度有差异 / 无差异。大小未变不表示内容相同，CSV 另保留 SHA。 |

主类净金额为所属路径的 `新大小−旧大小` 之和；占比 = 主类净金额 / 包路径净增量 × 100%，显示小数仅作显示，CSV 保留精确整数分数。负增量、负占比和超过 100% 的值允许存在，用于保留移除文件的抵扣。armv7l 总量为负，分类净额也可为负。

| 架构 / 包 | 主类 | 路径数 | 净增量 bytes | 占包路径净增量 | raw 证据 |
| --- | --- | --- | --- | --- | --- |
| armv7l / clang | 代码节变大 | 19 | -2,498,016 | 84.24864050% | [raw/analysis_facts.jsonl:7](raw/analysis_facts.jsonl#L7) |
| armv7l / clang | 未分类 | 5 | -467,036 | 15.75135950% | [raw/analysis_facts.jsonl:8](raw/analysis_facts.jsonl#L8) |
| armv7l / clang-accel-x86_64-armv7l | 删除文件 | 2 | -146,346,256 | -5.81492437% | [raw/analysis_facts.jsonl:12](raw/analysis_facts.jsonl#L12) |
| armv7l / clang-accel-x86_64-armv7l | qemu-accel 打包变化 | 105 | 2,663,081,584 | 105.81492437% | [raw/analysis_facts.jsonl:13](raw/analysis_facts.jsonl#L13) |
| armv7l / llvm | 代码节变大 | 54 | -799,236 | 66.72555260% | [raw/analysis_facts.jsonl:25](raw/analysis_facts.jsonl#L25) |
| armv7l / llvm | 未分类 | 28 | -398,560 | 33.27444740% | [raw/analysis_facts.jsonl:26](raw/analysis_facts.jsonl#L26) |
| x86_64 / clang | 链接方式变化 | 24 | 1,174,512,328 | 99.99901603% | [raw/analysis_facts.jsonl:32](raw/analysis_facts.jsonl#L32) |
| x86_64 / clang | 未分类 | 3 | 11,557 | 0.00098397% | [raw/analysis_facts.jsonl:35](raw/analysis_facts.jsonl#L35) |
| x86_64 / libllvm | 代码节变大 | 1 | 7,142,240 | 100.00000000% | [raw/analysis_facts.jsonl:43](raw/analysis_facts.jsonl#L43) |
| x86_64 / llvm | 链接方式变化 | 79 | 1,610,256,272 | 99.74075297% | [raw/analysis_facts.jsonl:50](raw/analysis_facts.jsonl#L50) |
| x86_64 / llvm | 代码节变大 | 3 | 4,185,392 | 0.25924703% | [raw/analysis_facts.jsonl:52](raw/analysis_facts.jsonl#L52) |
| x86_64 / llvm-devel | 链接方式变化 | 3 | 135,423,120 | 99.99698067% | [raw/analysis_facts.jsonl:59](raw/analysis_facts.jsonl#L59) |
| x86_64 / llvm-devel | 代码节变大 | 1 | 280 | 0.00020675% | [raw/analysis_facts.jsonl:61](raw/analysis_facts.jsonl#L61) |
| x86_64 / llvm-devel | 未分类 | 4 | 3,809 | 0.00281258% | [raw/analysis_facts.jsonl:62](raw/analysis_facts.jsonl#L62) |

上表省略零金额行，完整含零行的主类表为 [category_summary.csv](category_summary.csv)。所有包“新增文件”和“strip/调试信息变化”金额均为零；其证据为该表各行的 `derived_evidence`。主类合计与包增量逐包相等，见 [raw/validation.json:7](raw/validation.json#L7)。

为不掩盖 clang-accel 上同时存在的 NEEDED 变化，另列**非互斥**命中统计。此表的类别金额不能跨类相加，完整表见 [category_membership.csv](category_membership.csv)：

| 架构 / 包 | 所有命中标签 | 路径数 | 净额 bytes | 占包路径净增量 | raw 证据 |
| --- | --- | --- | --- | --- | --- |
| armv7l / clang-accel-x86_64-armv7l | 删除文件 | 2 | -146,346,256 | -5.81492437% | [raw/coverage_facts.jsonl:8](raw/coverage_facts.jsonl#L8) |
| armv7l / clang-accel-x86_64-armv7l | qemu-accel 打包变化 | 107 | 2,516,735,328 | 100.00000000% | [raw/coverage_facts.jsonl:9](raw/coverage_facts.jsonl#L9) |
| armv7l / clang-accel-x86_64-armv7l | 链接方式变化 | 102 | 2,658,899,664 | 105.64875990% | [raw/coverage_facts.jsonl:10](raw/coverage_facts.jsonl#L10) |
| armv7l / clang-accel-x86_64-armv7l | 代码节变大 | 3 | 4,181,920 | 0.16616447% | [raw/coverage_facts.jsonl:12](raw/coverage_facts.jsonl#L12) |

因此，qemu-accel 类别的百分比不能解释为“qemu-accel 源码改动造成了这些字节”。两版收录规则文本、无匹配事实、对应 ELF 的链接变化分别独立记录。LLVM 编译/链接选项也只对应到观察类别，没有把一个工具的整个字节增量归因给某一个源码行。

## 获取状态、验证和复现

指定 RPM、文件清单、哈希和 readelf 输出已全部取得。aarch64 不在本轮指定下载清单，未获取本轮逐文件扫描，不能用 armv7l 数据替代。独立单选项优化效果、逐文件压缩贡献未获取，原因如前。所选 ELF 没有可读出的 build-id，逐行注明。

部分 cgit 请求返回 HTTP 502，失败正文保留，不能当作源码：`llvm_packaging.diff`、`qemu-accel_full.diff`、`qemu-accel_full_diff.html`、最初的 `qemu-accel_{old,new}_qemu-accel-armv7l.spec`、commit 页面和反向 log 页面。成功替代是 `llvm_packaging_complete.diff`、`qemu-accel_full_retry.diff`、`qemu-accel_{old,new}_armv7l_retry.spec` 和正/反向 format-patch。每次 URL、状态、正文 SHA 都在 [raw/fetch_manifest.jsonl:1](raw/fetch_manifest.jsonl#L1) 起，失败不会被静默覆盖。

下载/采集脚本位于 `scripts/collect_*.py`、`scripts/retry_source_context.py`；文本分析为 `analyze_sizes.py`、`analyze_sources.py`、`analyze_coverage.py`，报告为 `write_findings.py`。离线复现只需运行后三个分析脚本及报告脚本；不执行 raw 中的产品源码。脚本使用 Python、requests、BeautifulSoup，以及 rpm/rpm2cpio/cpio/readelf；采集日志记录命令与退出码。

数据验证：14 个包完成标记和解包删除标记齐全；全部 regular 文件大小和 SHA 与 RPM 头相符；readelf 调用退出正常；逐类净额可回算各包净增量。机器核验见 [raw/validation.json](raw/validation.json)，收尾目录/引用/文件集核验见 [raw/final_validation.json](raw/final_validation.json)。RPM 和解包内容不在提交范围。

全部 CSV 均在本目录，raw 证据引用相对此目录；`:N`/`:N-M` 是保存文件的物理行号，GitHub 链接锚点定位到首行。下载来的 HTML、diff、spec、readelf 输出不做排版清理，便于核对原文。
