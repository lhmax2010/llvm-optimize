# 161 · 361624 PS6 评审材料

**162-A 功能复测 FAIL，唯一失败项为 scan-view --help，退出码 127。** [入口与解释器核对](../../tools/bolt/results/task162/A-scan-view-entry.txt)

154-B 的归档结论为 **PARTIAL**。证据提交 `5631413ab5e34fc6bd74f3344385ffcccb7f62a2`。
补丁基底 `06f3424c543a9645707f9afbbd9b5318280fffeb`，顺序为 1、2、3、5、6、4。
[完整合并 diff](../../tools/bolt/results/task161/ps6-final/ps6-to-final.diff) · [提交与 tree 核对](../../tools/bolt/results/task161/ps6-final/identity.json)

## 补丁与证据

| 补丁 | 目的 | 文件 | 验证证据 |
|---|---|---|---|
| 1 | 为原来的三个子包名新增带版本的 Provides，并限制 Obsoletes 的范围。 | [补丁](../../tools/bolt/results/task161/ps6-final/0001-suggestion-1.patch) | [153 RPM 解析](../../tools/bolt/results/task153/rpmspec-results.json) · [153 事务测试](../../tools/bolt/results/task153/transactions/) |
| 2 | 让 libgomp/libiomp5 安装路径注释反映配置的库目录，安装命令维持原样。 | [补丁](../../tools/bolt/results/task161/ps6-final/0002-suggestion-2.patch) | [153 CMake 安装规则](../../tools/bolt/results/task153/openmp-libdir-rule.txt) |
| 3 | 在最后一次使用后取消 X86 文件辅助宏定义，并对齐函数签名。 | [补丁](../../tools/bolt/results/task161/ps6-final/0003-suggestion-3.patch) | [153 standalone 构建](../../tools/bolt/results/task153/final.json) |
| 5 | 将 scan-build HTML 资源和手册页归到 clang，将 scan-view 数据归到 llvm。 | [补丁](../../tools/bolt/results/task161/ps6-final/0004-suggestion-5.patch) | [154-A 路径模拟](../../tools/bolt/results/task154/static-package-simulation.json) · [154-B 核对](../../tools/bolt/results/task154/final.json) |
| 6 | 将已安装的 libscanbuild 和 libear 模块归到 clang。 | [补丁](../../tools/bolt/results/task161/ps6-final/0005-suggestion-6.patch) | [154-A 安装记录](../../tools/bolt/results/task154/module-install-history.json) · [154-B 核对](../../tools/bolt/results/task154/final.json) |
| 4 | 更新提交说明，树与补丁 6 相同。 | [补丁](../../tools/bolt/results/task161/ps6-final/0006-suggestion-4.patch) | [154-A 文本核对](../../tools/bolt/results/task154/message-gates.json) |

## 154-B 实测

[154-B 完整回执](../../tools/bolt/results/task154/final.json) · [154 报告](154_ps6_fixes.md)

### 154-B 第 1 轮

结论为 PARTIAL，耗时 11035.8 秒。

| 核对项 | 实测 | 依据 |
|---|---|---|
| 完整构建 | PASS | GBS 返回 0。 |
| 未打包或文件缺失诊断 | 0 | [原文](../../tools/bolt/results/task154/attempt-1/evidence/rpm-packaging-errors.txt) |
| rpm -qlp 与预期文件移动 | PASS | [原文](../../tools/bolt/results/task154/attempt-1/evidence/rpm-file-comparison.json) |
| clang 新增 Python Requires | [] | [原文](../../tools/bolt/results/task154/attempt-1/evidence/clang-requires-diff.json) |
| Python 模块与 __pycache__ | ABSENT | [原文](../../tools/bolt/results/task154/attempt-1/evidence/clang-python-module-files.json) |
| scan-build HTML、sorttable.js、scanview.css | 未取得 | 未取得 [原文](../../tools/bolt/results/task154/attempt-1/evidence/functional-results.json) |
| analyze-build --help | SKIPPED | runtime-plan exited 1, raw output /home/linhao/Toolchain/development/llvm-optimize/archive/task154/attempt-1/evidence/runtime-plan.txt |
| intercept-build --help | SKIPPED | runtime-plan exited 1, raw output /home/linhao/Toolchain/development/llvm-optimize/archive/task154/attempt-1/evidence/runtime-plan.txt |
| scan-build-py --help | SKIPPED | runtime-plan exited 1, raw output /home/linhao/Toolchain/development/llvm-optimize/archive/task154/attempt-1/evidence/runtime-plan.txt |
| scan-view --help | 未取得 | 未取得 |

## 未完成的验证

aarch64 和 armv7l 有 RPM 展开记录。实际构建范围为 x86_64。

- 第 1 轮 analyze-build。runtime-plan exited 1, raw output /home/linhao/Toolchain/development/llvm-optimize/archive/task154/attempt-1/evidence/runtime-plan.txt
- 第 1 轮 intercept-build。runtime-plan exited 1, raw output /home/linhao/Toolchain/development/llvm-optimize/archive/task154/attempt-1/evidence/runtime-plan.txt
- 第 1 轮 scan-build-py。runtime-plan exited 1, raw output /home/linhao/Toolchain/development/llvm-optimize/archive/task154/attempt-1/evidence/runtime-plan.txt

[154-B 残留清理脚本](../../tools/bolt/results/task154/sudo-clean.sh)


## 补丁 4 完整提交说明

~~~text
packaging: split tool subpackages into a standalone llvm-tools-subpkgs spec

* 3a5189033a1f - packaging: move tool subpackages to a standalone llvm-tools-subpkgs spec
* d364b338759a - bolt: create ZLIB/LibXml2 targets in standalone build
* 28e72ec6b05d - bolt: mirror X86 mnemonic tables and helpers for standalone build
* 1b9c1ce174de - packaging: add --build-id=sha1 to toolchain linker flags
* 0cc528da035e - bolt: standalone build fixes for LLVM_LINK_LLVM_DYLIB=ON
* 3abe328e2c30 - packaging: build profiling tools and BOLT for armv7l (Tizen)
* d3f74e4f484d - packaging: add Obsoletes and python3 Requires to llvm; tidy tools subpackages
* c7edd8f43c66 - packaging: note that scan-build needs clang at runtime
* 67304f964043 - packaging: install with DESTDIR and do not ship libgomp/libiomp5 links

Build BOLT from the standalone llvm-tools-subpkgs spec against the
installed LLVM packages on x86_64 and aarch64. That build links
libLLVM.so, while in-tree BOLT keeps linking the LLVM component
libraries; BOLT_LLVM_LINK_MODE selects the mode before its consumers.
The X86 helper mirror is compiled only for the standalone dylib build
and is listed in LLVM_OPTIONAL_SOURCES otherwise, and the inherited
runtime C and C++ flags are cleared only for standalone builds.

The standalone spec pins its LLVM provider build requirements to the
LLVM version and checks that the installed providers share one version
and release, sets BOLT_TARGETS_TO_BUILD per architecture and verifies
target registration, keeps the distribution LDFLAGS, derives
LLVM_LIBDIR_SUFFIX from %{_lib}, and lets CMake install merge-fdata
once. bolt requires libllvm = %{version} at runtime.

clang now ships scan-build, scan-build-py, analyze-build and
intercept-build together with the libexec scripts, the report
resources and the Python modules they use, and llvm ships the
scan-view data next to scan-view. llvm and clang provide the
llvm-xray, llvm-prof-tools and clang-analyzer names and obsolete
their older versions.

The --build-id=sha1 flag is added to the executable and shared-library
linker flags; module linker flags keep their existing settings.

Change-Id: Ie2c1d45cea6703a0caef72187397275a03e66468
Signed-off-by: Dongkyun Son <dongkyun.s@samsung.com>
Signed-off-by: Pareek Eshaan <e.pareek@samsung.com>
Co-Authored-By: Cline SR
Signed-off-by: Hao Lin <hao.lin@samsung.com>
~~~

## 162-A · PS6 功能复测

**FAIL**。首轮 GBS 源码目录缺失。补齐后复测进入 %build，scan-view --help 因入口使用 env python 而返回 127，其余项目通过。

测试包的 BuildRequires 仅为 clang、perl、python3。GBS 配置优先使用 154-B 的本地 RPM 仓库。项目配置的 Support 行移去 llvm-devel，实际安装状态仍由 spec 内的 rpm -q 核对。
清理输出文件为 0 B，原构建根已不存在。 [复测 df](../../tools/bolt/results/task162/df-before.txt) · [清理核对](../../tools/bolt/results/task162/sudo-recheck.json)

| 功能 | 结果 | 退出码与原文 |
|---|---|---|
| llvm-devel-absent | PASS | 1 |
| provider-clang | PASS | 0 |
| provider-llvm | PASS | 0 |
| provider-libllvm | PASS | 0 |
| scan-build | PASS | 0 |
| report-html-assets | PASS | 0 |
| analyze-build | PASS | 0 [原文](../../tools/bolt/results/task162/A-retry-analyze-build-help.txt) |
| intercept-build | PASS | 0 [原文](../../tools/bolt/results/task162/A-retry-intercept-build-help.txt) |
| scan-build-py | PASS | 0 [原文](../../tools/bolt/results/task162/A-retry-scan-build-py-help.txt) |
| scan-view | FAIL | 127 [原文](../../tools/bolt/results/task162/A-retry-scan-view-help.txt) |

[GBS 输出](../../tools/bolt/results/task162/A-retry-gbs.txt) · [systemd 记录](../../tools/bolt/results/task162/A-retry-systemd.txt) · [RPM 构建原文](../../tools/bolt/results/task162/A-retry-build-fail.txt) · [首轮 GBS 输出](../../tools/bolt/results/task162/A-gbs.txt)
