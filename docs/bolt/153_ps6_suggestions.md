# 153 · 361624 PS6 建议补丁

基于 PS6 `06f3424c543a9645707f9afbbd9b5318280fffeb` 生成四个本地提交。三个架构的 Tizen RPM 4.14.1 查询通过。OpenMP 注释和 X86 宏改动已静态核对。正文逐句检查有一处需要注明 EVR。哑包事务和 standalone 构建排在 151 单元结束且其汇总确认已推送后。

## 补丁清单

| 补丁 | 本地提交 | Diff 摘要 | 评审附件 |
|---|---|---|---|
| 1 | `09b187fa3d5061d1ae431e97d3756786ed7529b1` | `packaging/llvm.spec` +6/−3。三个旧包名提供同 EVR，并废弃严格较低的 EVR。 | [补丁 1](../../tools/bolt/results/task153/0001-suggestion-1.patch) |
| 2 | `de3bf8dc783bf54d142a448cc3673ecee3fecaef` | `packaging/llvm.spec` +3/−3，修正 OpenMP 安装目录注释。忽略注释后的 spec 内容逐字节相同。 | [补丁 2](../../tools/bolt/results/task153/0002-suggestion-2.patch) |
| 3 | `42f363793d46fbc80c924f908a987e769f083d03` | `X86BoltMnemonicTables.cpp` +4/−1，三处 `#undef` 与一处签名续行对齐。 | [补丁 3](../../tools/bolt/results/task153/0003-suggestion-3.patch) |
| 4 | `d415b9fec7d8899c3421db2dbb6efc3885bedc54` | 只改提交说明。树与补丁 3 的 `27bea5bd8171042d1f44b47f2703b0515433c568` 相同。 | [补丁 4](../../tools/bolt/results/task153/0004-suggestion-4.patch) |

本地分支为 `archive/task153/ps6-suggestions.git` 中的 `ps6-suggestions`，作者与提交者均为 Hao Lin <hao.lin@samsung.com>。前 3 份 format-patch 按顺序基于 PS6 应用。第 4 份是保留说明的空差异附件，也提供 [说明全文](../../tools/bolt/results/task153/suggested-commit-message.txt) 和 [说明 diff](../../tools/bolt/results/task153/commit-message.diff)。

## 1 · Provides / Obsoletes

**(a) PASS，3/3 架构。** x86_64、aarch64、armv7l 下，llvm 提供 `llvm-xray = 22.1.8-1` 和 `llvm-prof-tools = 22.1.8-1`，clang 提供 `clang-analyzer = 22.1.8-1`。三项 Obsoletes 全为 `< 22.1.8-1`。RPM 4.14.1 使用 139-D 的已留存 Tizen loader 和库。[包含归属的输出](../../tools/bolt/results/task153/rpmspec-results.json) · [查询命令](../../tools/bolt/results/task153/rpmspec-command-records.json)

**(b) 历史 EVR 查询。** 在 41 个留存构建、仓库或下载目录及 152 号登记的仓库路径中，检查 62 份可读 primary 文件（19 个不同 SHA256，去重后 32,608 条包记录）。 EVR 结果为 `clang-analyzer` 无命中，`llvm-xray` 无命中，`llvm-prof-tools` 无命中。 事务测试将使用 22.1.8-0 和 22.1.8-2 作为边界夹具。 收据列出 4 项无权限路径，均为构建根内的 ldconfig 缓存。 本次检查范围内未找到 testsolv。 [扫描范围与 EVR 原文](../../tools/bolt/results/task153/historical-evr.json)

**(c) 待 151。** 用同版本 RPM 和无载荷的测试包在独立 RPM 数据库验证旧包升级、虚拟依赖与自我冲突。原文随最终结果归档。

## 2 · OpenMP 安装注释

**PASS。** PS6 `openmp/runtime/src/CMakeLists.txt` 第 426、430、437–446 行在配置的 `OPENMP_INSTALL_LIBDIR` 安装，令 CMake 在 `$ENV{DESTDIR}${outdir}` 下创建别名。第 430 行令 `outdir` 使用 CMake 安装前缀和配置的库目录。PS6 `openmp/CMakeLists.txt` 第 38、67–70 行显示该目录随 libdir 后缀和目标目录设置变化。该 spec 第 469、479 行关闭按目标分目录，并用 RPM 的 _lib 派生后缀。新注释据此使用 “configured library directory” 并举 `%{_libdir}` 为例，原安装和移除命令未改变。[CMake 安装原文](../../tools/bolt/results/task153/openmp-install-rule.txt) · [目录配置原文](../../tools/bolt/results/task153/openmp-libdir-rule.txt)

## 3 · X86 镜像宏

**静态 PASS，编译待第 5 步。** 以下是补丁后的行号。

| 宏 | 定义 | 最后使用 | #undef |
|---|---:|---:|---:|
| GET_REGINFO_MC_DESC | 29 | 30 | 31 |
| GET_X86_MNEMONIC_TABLES_CPP | 33 | 34 | 35 |
| ENTRY | 40 | 46 | 47 |

## 4 · 提交说明

**新正文格式 PASS。** 全文纯 ASCII，新增正文最长 70 列、禁用词零命中。PS6 的标题、9 条历史和 trailer 均逐字节保留。全文范围的格式门禁为 FAIL，记录了原有 8 条超 72 列的行及 1 条已有的禁止词匹配，均来自要求保持原样的区段。[检查原文与范围](../../tools/bolt/results/task153/message-gates.json)

**逐句核对 7 句通过，1 句需限定 EVR。** 建议说明旧包只在 EVR 严格较低时废弃。保留用户给出的原句及另附建议改法。[8 句对照表](../../tools/bolt/results/task153/message-sentence-audit.md)

## 5 · standalone 构建

等待 151 主单元及子单元退出，并在远端 bolt-v4 上验证 151 汇总提交。之后按 145 B2 口径用 B1 的 RPM 作为 provider，构建补丁 1–3 的树，核对 bolt RPM 文件清单、目标注册和 `llvm-bolt --version`。补丁 1、2 的主 llvm spec 改动仅涉及 RPM 元数据和注释，由 1(a)、1(c) 覆盖，无需做一次主 llvm 完整构建。

145 B2 回执未记录磁盘时间序列。采用清理前整个 task145 目录实测分配量 17,143,382,016 B 作保守准入代理。按 1.15 倍、15 GiB 和 30 GB 余量计算，准入为 65,821,016,679 B。内存按 139-D，至少分配 10 GiB，使用同档位的编译及 ThinLTO 并行值、单链接并发。历史 B2 用时约 17 分钟。截止 2026-11-26 20:00 PST，当时仍未准入则记为 SKIPPED。
