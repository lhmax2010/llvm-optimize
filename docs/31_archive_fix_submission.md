# x86_64 归档修复提交补丁

日期：2026-09-28。**PASS：提交补丁可在干净分支 HEAD 应用；与 docs/30 验证内容仅差三处本机并发数。**
本轮只生成、检查和发布评审材料，没有构建，没有修改 W/llvm 的源码/spec，没有推送 Gerrit。
[docs/30](30_archive_fix_full_build.md) 及 docs/25–29 保留原样。

## 1. 来源与提交内容

- 基准：`sandbox/fangyu.he/llvm_optmize` 的 `f111162e94aa48ed367c9d2c039456c70e7160ae`。
- 独立临时工作树：`/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-archivefix-submission-20260928`，detached HEAD，稀疏检出 packaging；不移动原分支。
- 补丁：[单提交 format-patch](../patches/archive-index-fix/0001-Fix-llvm-static-devel-usability-with-ThinLTO.patch)；其中的 LLVM 提交为 `228642e04e3a0e6b1ae81f37c644068f88e2d4d9`，父提交即上述基准。
- 便于直接评审的 Source：[llvm-static-archives-native.py](../patches/archive-index-fix/llvm-static-archives-native.py)；补丁内已包含此文件，不需要另行拷贝后再应用。
- Commit message 为英文，说明 ThinLTO bitcode、GNU strip 成功退出却损坏索引、无插件 GNU ld 兼容性、转换策略和实测范围；沿用分支的 `Change-Id` 风格，ID 为 `Id4eb147e7ec4764d58a81110cf7bf57d21b64ac8`。
- 作者沿用本机现有 Git 配置 `liushanshan <ss0217.liu@samsung.com>`；没有修改 Git 身份配置。

提交只涉及 **2 个文件、511 行新增**：spec 两处修改（x86_64 条件内的 Source1005 声明及 `%install` 末尾调用），以及 500 行新增 Source。
没有修改并发、RPM 宏、工具的编译/链接参数；armv7l/aarch64 后续分别处理。

Source 与 docs/30 的 `tools/llvm_static_archives_source.py`、试验工作树副本、真实构建根 SOURCES 副本均逐字节相同。
完整构建和消费者结论沿用 docs/30 §2–§4：22 RPM；225 开发归档无 bitcode、完整索引；
非归档文件差异 0；Tizen GNU ld（无 LTO、无插件）及 lld 消费者通过。本轮未重跑这些实验。

## 2. 与验证内容一致性的证明

docs/30 构建入口登记的输入 spec 是 `temp/llvm-archivefix-trial/packaging/llvm.spec`，SHA 为下表中的“验证 spec”。
提交版保留分支 HEAD 的 **6/6/2**；验证版为本机限流 **4/4/1**。完整 diff 如下，除此之外逐字节相同：

```diff
--- submission/packaging/llvm.spec
+++ docs30-validated/packaging/llvm.spec
@@ -48,7 +48,7 @@
 Source1005: llvm-static-archives-native.py
 %endif

-%{!?mlgo_build_jobs: %define mlgo_build_jobs 6}
+%{!?mlgo_build_jobs: %define mlgo_build_jobs 4}
 %{!?mlgo_verify_configure_only: %define mlgo_verify_configure_only 0}

 BuildRequires: cmake
@@ -274,8 +274,8 @@
     -DLLVM_LIBDIR_SUFFIX=`echo %{_lib} | sed s/lib//g` \
     -DCLANG_RESOURCE_DIR="../%{_lib}/clang/%{llvm_version}" \
     -DLLVM_BINUTILS_INCDIR=/usr/include \
-    -DLLVM_PARALLEL_COMPILE_JOBS=6 \
-    -DLLVM_PARALLEL_LINK_JOBS=2 \
+    -DLLVM_PARALLEL_COMPILE_JOBS=4 \
+    -DLLVM_PARALLEL_LINK_JOBS=1 \
 %if %{with mlgo}
 %ifarch armv7l aarch64 x86_64
     -DTENSORFLOW_AOT_PATH="${MLGO_AOT_DIR}/mlgo_sysroot" \
```

这证明功能修复内容一致；不声称 6/6/2 已在本机完成容量认证，docs/30 的构建实测仍为 4/4/1。
GBS 导出的 `SOURCES/llvm.spec` 另含自动生成的 VCS、Patch 声明和 `%prep` 应用行，不能直接当作源 spec；
这些导出差异全文另存证据 `validated-vs-gbs-exported.diff`，不纳入提交补丁。

## 3. 最终补丁应用检查与 SHA256

在临时工作树提交后，切回干净基准，对**最终 format-patch 文件本身**执行（P 为补丁绝对路径）：

```text
git switch --detach f111162e94aa48ed367c9d2c039456c70e7160ae
git status --porcelain
# stdout 为空，exit 0
git apply --check --index "$P"
# stdout/stderr 为空，exit 0
git apply --index "$P"
# stdout/stderr 为空，exit 0
git diff --cached --check
# stdout/stderr 为空，exit 0
git write-tree
29316bffd01f0e4e7e90773cc2b17337c6707883
```

应用后的完整 Git tree 与补丁提交的 tree 完全相同，父提交到补丁提交的提交数为 1。
Source 全字节比较、spec 仅三处并发差异断言全部 PASS；未向 W/llvm 应用补丁。

| 文件/版本 | SHA256 |
| --- | --- |
| format-patch（29,364 B） | `0c40c91cb6b896fd93f2712b669eec6771d219268dff7d290539fbb98d0bea58` |
| 新增 Source（25,912 B） | `2476c5efa061499d7963e0f0976f0c9c86944b688f5bcc48ea40911574af399e` |
| 提交 spec（6/6/2） | `fb3899d4d9a9bf498da72f17212833948bb1a0f171fa3ba895702d14e03518e5` |
| docs/30 验证输入 spec（4/4/1） | `83dc994ab6d7ffe65cdf2bf38dbe027599775ffa71c6614219123856f8be1d2d` |
| docs/30 GBS 导出 spec（含生成元数据） | `855f0a63333f69ae80ccb86d2a2a19f3f4c4248a67f228bd40824087ce6c060a` |

原始命令、退出码、stdout/stderr 与核对结果在：
`/home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-submission-20260928/`，
入口为 `commands.jsonl`、`verification.json`、`submission-vs-validated.diff`、`final-integrity.json`。
初始化稀疏工作树的记录见 `worktree-setup-note.txt`；干净状态确认后才进行补丁应用。

**结论：此 format-patch 是供 Gerrit 评审的 x86_64 提交版本，已发布至 GitHub；尚未提交 Gerrit 或进入 OBS。**
