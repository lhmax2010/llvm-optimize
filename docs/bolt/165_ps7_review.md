# 165 · 361624 PS7 候选与评审材料

**P7 已在本地生成，身份、tree、代码 diff 和正文门禁均通过。** P7 为 `00a0a925bc04b2b1e40b2e23ffe256082c25aebf`，tree 为 `0771b37d18e5263cda004650aacdc6cb2f7e4a10`。候选保存在本地 `361624-ps7` 分支。

| 核对项 | 结果 |
|---|---|
| Tree | 与验证分支 HEAD `e6baffc9a84ea930d366e9574ebe8557f243578a` 相同。 |
| 父提交 | 唯一父提交为 PS6 的父提交 `f346dd75e87de324dc2abe61454ca1c49969d12d`。 |
| 作者 | 姓名、邮件、时间戳和时区逐字节与 PS6 相同。 |
| 提交者 | Hao Lin <hao.lin@samsung.com>，使用生成时的时间。 |
| 提交说明 | PS6 标题、9 条历史和全部 trailer 逐字节相同。Change-Id 为 `Ie2c1d45cea6703a0caef72187397275a03e66468`。新正文与最终补丁 4 一致，纯 ASCII，最长 70 列，禁用词零命中。 |
| 代码 | PS6→P7 完整 diff 与归档的 1、2、3、5、6、7 合并 diff 逐字节相同。补丁 4 提供新正文，tree 与验证分支一致。 |
| Gerrit 分支头 | 只读枚举 151 个分支头，验证分支指向预期 HEAD，P7 命中数为 0。 |

[PS6→P7 完整代码 diff](../../tools/bolt/results/task165-prep/ps6-to-p7.diff) · [提交说明 diff 原文](../../tools/bolt/results/task165-prep/ps6-to-p7-message.diff) · [P7 提交说明全文](../../tools/bolt/results/task165-prep/p7-message.txt) · [核对回执](../../tools/bolt/results/task165-prep/checks.json)

~~~text
 bolt/lib/Target/X86/X86BoltMnemonicTables.cpp |  5 ++++-
 packaging/llvm.spec                           | 32 ++++++++++++++++++++-------
 2 files changed, 28 insertions(+), 9 deletions(-)
~~~

## PS6→P7 提交说明 diff

~~~diff
--- PS6 commit message
+++ P7 commit message
@@ -10,22 +10,28 @@
 * c7edd8f43c66 - packaging: note that scan-build needs clang at runtime
 * 67304f964043 - packaging: install with DESTDIR and do not ship libgomp/libiomp5 links
 
-Keep in-tree BOLT on component libraries by setting BOLT_LLVM_LINK_MODE
-before its consumers. List the X86 mirror in LLVM_OPTIONAL_SOURCES, as
-only standalone dylib builds compile it. Clear the inherited runtime C
-and C++ flags only for standalone builds.
+Build BOLT from the standalone llvm-tools-subpkgs spec against the
+installed LLVM packages on x86_64 and aarch64. That build links
+libLLVM.so, while in-tree BOLT keeps linking the LLVM component
+libraries; BOLT_LLVM_LINK_MODE selects the mode before its consumers.
+The X86 helper mirror is compiled only for the standalone dylib build
+and is listed in LLVM_OPTIONAL_SOURCES otherwise, and the inherited
+runtime C and C++ flags are cleared only for standalone builds.
 
-Restore ARM;BPF as the armv7l LLVM target list and drop the explicit
-python3 requirement from llvm. Limit the standalone spec to x86_64 and
-aarch64, set BOLT_TARGETS_TO_BUILD per architecture, and verify target
-registration.
+The standalone spec pins its LLVM provider build requirements to the
+LLVM version and checks that the installed providers share one version
+and release, sets BOLT_TARGETS_TO_BUILD per architecture and verifies
+target registration, keeps the distribution LDFLAGS, derives
+LLVM_LIBDIR_SUFFIX from %{_lib}, and lets CMake install merge-fdata
+once. bolt requires libllvm = %{version} at runtime.
 
-Bind the LLVM provider build requirements to the LLVM version and check
-that the installed providers share one version and release. Require
-libllvm = %{version} at runtime for bolt and drop its explicit
-compiler-rt runtime requirement. Derive LLVM_LIBDIR_SUFFIX from %{_lib},
-retain distribution LDFLAGS, correct the debug packaging comments, and
-let CMake install merge-fdata once.
+clang now ships scan-build, scan-build-py, analyze-build and
+intercept-build together with the libexec scripts, the report
+resources and the Python modules they use. Scripts that used an
+unversioned Python interpreter now use Python 3 shebangs. llvm
+ships the scan-view data next to scan-view. llvm and clang provide
+the llvm-xray, llvm-prof-tools and clang-analyzer names and
+obsolete their older versions.
 
 The --build-id=sha1 flag is added to the executable and shared-library
 linker flags; module linker flags keep their existing settings.
~~~

## 改动和验证

| 补丁 | 目的 | 验证证据 |
|---|---|---|
| 1 | 在 llvm 和 clang 中提供三个旧包名，只废弃 EVR 严格较低的包。 | RPM 4.14.1 三架构查询和哑包事务通过。 [153 RPM 查询](../../tools/bolt/results/task153/rpmspec-results.json) · [事务原文](../../tools/bolt/results/task153/transactions/commands.json) |
| 2 | OpenMP 安装注释反映配置的库目录，安装命令逐字节相同。 | [153 CMake 安装规则](../../tools/bolt/results/task153/openmp-install-rule.txt) · [目录推导](../../tools/bolt/results/task153/openmp-libdir-rule.txt) |
| 3 | 三个 X86 镜像辅助宏在最后使用后取消定义，对齐一处函数签名续行。 | x86_64 standalone 构建、目标注册和 bolt 文件清单通过。 [153 构建收据](../../tools/bolt/results/task153/final.json) |
| 5 | 将 scan-build 报告资源和手册归入 clang，将 scan-view 数据归入 llvm。 | 九个目标路径归属检查和全路径守恒模拟通过，154-B 成品的文件变更符合预期。 [154-A 模拟](../../tools/bolt/results/task154/static-package-simulation.json) · [154-B RPM 文件对比](../../tools/bolt/results/task154/attempt-1/evidence/rpm-file-comparison.json) |
| 6 | 停止删除 libscanbuild、libear，clang 打包其已安装的模块。 | 154-B 完整构建、模块清单及 clang 的 Python 依赖差异核对通过。162-A 无 llvm-devel 环境中三个 Python 分析器入口返回 0。 [154-A 安装记录](../../tools/bolt/results/task154/module-install-history.json) · [154-B 模块](../../tools/bolt/results/task154/attempt-1/evidence/clang-python-module-files.json) · [154-B 依赖](../../tools/bolt/results/task154/attempt-1/evidence/clang-requires-diff.json) · [162-A](../../tools/bolt/results/task162/A-result.json) |
| 7 | 将六个已安装脚本的无版本号 Python shebang 改为 Python 3。 | Tizen RPM 4.14.1 三架构展开通过。163-A 对 154-B RPM 的同一组文件应用精确 sed 命令，六个首行正确，scan-view --help 从 127 变为 0，HTML 报告和资源检查通过。 [162-A 原退出 127](../../tools/bolt/results/task162/A-retry-scan-view-help.txt) · [163-A 展开](../../tools/bolt/results/task163/ps6/rpmspec.json) · [163-A GBS 原文](../../tools/bolt/results/task163/ps6/smoke-build.txt) |
| 4 | 将最终评审正文纳入单提交，包含 163-A 的 shebang 说明。 | [163-A 逐句核对](../../tools/bolt/results/task163/ps6/message-sentence-audit.md) · [P7 说明 diff](../../tools/bolt/results/task165-prep/ps6-to-p7-message.diff) |

历史过程见 [153 建议补丁](153_ps6_suggestions.md)、[154 打包核对](154_ps6_fixes.md) 和 [161 评审材料（含 162-A、163-A）](161_ps6_review_packet.md)。

## 已知验证范围

- aarch64、armv7l 已通过 RPM 静态展开，最终 tree 的两架构完整构建结果尚待 QB。163-A 是在 154-B x86_64 RPM 上复测修改命令，最终 tree 的打包核对仍使用该验证分支的 QB 构建。
- 最小 GBS 环境中，opt-diff.py、opt-stats.py 和 optrecord.py 由 Python 3 启动后报缺少 `yaml`，opt-viewer.py 报缺少 `pygments`。这四个入口的完整功能未在具备相应 Python 依赖的环境中验证。 [163-A 逐项结果](../../tools/bolt/results/task163/ps6/smoke-result.json)
