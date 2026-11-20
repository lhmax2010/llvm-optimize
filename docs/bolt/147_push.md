# 147-push · 361624 PS5（F3）

**PASS。** Gerrit 361624 最新为 PS5，revision `cbaa01f5c148f5cc705f969e13ac41fef811a9f9`，状态 `NEW`，目标 `tizen_base`。PS4 `1ddecbe8729f832b5ef565092d039f68df647a43` 保留。提交说明按要求修正三处，代码树保持 F2 的原值。[Gerrit 361624 PS5](https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361624/5)

## 推送前核对

| 项目 | 结果 |
|---|---|
| Gerrit 状态 | NEW，PS4 `1ddecbe8729f832b5ef565092d039f68df647a43`，从查询取得目标分支 `tizen_base`。 |
| F2 | `636ef90aa1ff75ca8731b84b1526e6a557cffcd6` |
| F2/F3 tree | `ef1ab363fa8e9be29eb930916e86c6e8f10f11af` |
| F2/F3 父提交 | `f346dd75e87de324dc2abe61454ca1c49969d12d` |
| F2/F3 作者及作者日期 | `Dongkyun Son <dongkyun.s@samsung.com> 1794637555 +0900`，原始头逐字节一致。 |
| F3 提交者及当前时间 | `Hao Lin <hao.lin@samsung.com> 1795187554 -0800` |
| F3 Change-Id | `Ie2c1d45cea6703a0caef72187397275a03e66468` |
| 主 spec 的 build-id 参数 | 第 415–416 行，仅 CMAKE_SHARED_LINKER_FLAGS 和 CMAKE_EXE_LINKER_FLAGS。 |
| 独立包 spec 的 build-id 参数 | 第 129–130 行，仅 CMAKE_EXE_LINKER_FLAGS 和 CMAKE_SHARED_LINKER_FLAGS。 |
| MODULE 链接参数 | 两份 spec 中均无 `--build-id=sha1` 的 MODULE 设置。 |
| 正文和历史 | 正文最长 72 列，PS4→F3 的 9 条原始历史行 diff 为零字节。全部 PS4 签名行以原顺序保留，Hao Lin 的 Signed-off-by 为末行。 |
| 禁用词与远端 HEAD | 新说明行零命中。146 个 Gerrit 分支头均未指向 F3。 |

[推送前查询原文](../../tools/bolt/results/task147-push/gerrit-before.jsonl) · [推送前一刻查询原文](../../tools/bolt/results/task147-push/gerrit-immediately-before.stdout) · [核对表 JSON](../../tools/bolt/results/task147-push/checks.json) · [F3 format-patch](../../tools/bolt/results/task147-push/0001-361624-PS5-F3.patch) · [F3 说明全文](../../tools/bolt/results/task147-push/F3-message.txt)

## F2→F3 说明 diff 原文

```diff
--- F2
+++ F3
@@ -11,9 +11,9 @@
 * 67304f964043 - packaging: install with DESTDIR and do not ship libgomp/libiomp5 links
 
 Keep in-tree BOLT on component libraries by setting BOLT_LLVM_LINK_MODE
-before its consumers. List the unused X86 mirror in LLVM_OPTIONAL_SOURCES
-and compile it only for standalone dylib builds. Clear the inherited
-runtime C and C++ flags only for standalone builds.
+before its consumers. List the X86 mirror in LLVM_OPTIONAL_SOURCES, as
+only standalone dylib builds compile it. Clear the inherited runtime C
+and C++ flags only for standalone builds.
 
 Restore ARM;BPF as the armv7l LLVM target list and drop the explicit
 python3 requirement from llvm. Limit the standalone spec to x86_64 and
@@ -21,11 +21,14 @@
 registration.
 
 Bind the LLVM provider build requirements to the LLVM version and check
-that the installed providers share one version and release. Keep the
-libllvm version requirement for bolt and remove its compiler-rt runtime
-requirement. Derive LLVM_LIBDIR_SUFFIX from %{_lib}, retain distribution
-LDFLAGS, correct the debug packaging comments, and let CMake install
-merge-fdata once.
+that the installed providers share one version and release. Require
+libllvm = %{version} at runtime for bolt and drop its explicit
+compiler-rt runtime requirement. Derive LLVM_LIBDIR_SUFFIX from %{_lib},
+retain distribution LDFLAGS, correct the debug packaging comments, and
+let CMake install merge-fdata once.
+
+The --build-id=sha1 flag is added to the executable and shared-library
+linker flags; module linker flags keep their existing settings.
 
 Change-Id: Ie2c1d45cea6703a0caef72187397275a03e66468
 Signed-off-by: Dongkyun Son <dongkyun.s@samsung.com>
```

## 推送原文

开始 `2026-11-20T07:13:17-08:00`，结束 `2026-11-20T07:13:24-08:00`，退出码 0。Gerrit 提示标题超过 50 字符，标题按任务要求保留。

```text
/usr/bin/git --git-dir=/home/linhao/Toolchain/development/llvm-optimize/archive/task144/objects.git push ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm cbaa01f5c148f5cc705f969e13ac41fef811a9f9:refs/for/tizen_base
```

```text
remote: 
remote: Processing changes: refs: 1, updated: 1        
remote: Processing changes: refs: 1, updated: 1, done            
remote: commit cbaa01f: warning: subject >50 characters; use shorter first paragraph        
remote: 
remote: SUCCESS        
remote: 
remote:   https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361624 packaging: split tool subpackages into a standalone llvm-tools-subpkgs spec        
remote: 
To ssh://review.tizen.org:29418/platform/upstream/llvm
 * [new reference]             cbaa01f5c148f5cc705f969e13ac41fef811a9f9 -> refs/for/tizen_base
```

[推送输出原始字节](../../tools/bolt/results/task147-push/push-output.txt)

## 推送后核对及查询原文

```text
cbaa01f5c148f5cc705f969e13ac41fef811a9f9	refs/changes/24/361624/5
```

```json
{"project":"platform/upstream/llvm","branch":"tizen_base","id":"Ie2c1d45cea6703a0caef72187397275a03e66468","number":361624,"subject":"packaging: split tool subpackages into a standalone llvm-tools-subpkgs spec","owner":{"name":"Dongkyun Son","email":"dongkyun.s@samsung.com","username":"dkson95"},"url":"https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361624","hashtags":[],"createdOn":1794638184,"lastUpdated":1795187618,"open":true,"status":"NEW","currentPatchSet":{"number":5,"revision":"cbaa01f5c148f5cc705f969e13ac41fef811a9f9","parents":["f346dd75e87de324dc2abe61454ca1c49969d12d"],"ref":"refs/changes/24/361624/5","uploader":{"name":"Lin Hao","email":"hao.lin@samsung.com","username":"lhmax2025"},"createdOn":1795187618,"author":{"name":"Dongkyun Son","email":"dongkyun.s@samsung.com","username":"dkson95"},"kind":"REWORK","sizeInsertions":650,"sizeDeletions":29},"patchSets":[{"number":1,"revision":"da885208aeb52f55c448ff46873d242346727522","parents":["61ef5d31ca91025c414c748477bef0c64ddfa67c"],"ref":"refs/changes/24/361624/1","uploader":{"name":"Dongkyun Son","email":"dongkyun.s@samsung.com","username":"dkson95"},"createdOn":1794638184,"author":{"name":"Dongkyun Son","email":"dongkyun.s@samsung.com","username":"dkson95"},"kind":"REWORK","sizeInsertions":563,"sizeDeletions":30},{"number":2,"revision":"d1c32eb37fa1be1196923b839e405fd0d9de2955","parents":["61ef5d31ca91025c414c748477bef0c64ddfa67c"],"ref":"refs/changes/24/361624/2","uploader":{"name":"Dongkyun Son","email":"dongkyun.s@samsung.com","username":"dkson95"},"createdOn":1795044644,"author":{"name":"Dongkyun Son","email":"dongkyun.s@samsung.com","username":"dkson95"},"kind":"REWORK","sizeInsertions":574,"sizeDeletions":30},{"number":3,"revision":"420a8aab1106c307270a6730a0483c2adf23175c","parents":["7b05a13744d1cf81a5e9cff22a27eb037bf1b6a8"],"ref":"refs/changes/24/361624/3","uploader":{"name":"Dongkyun Son","email":"dongkyun.s@samsung.com","username":"dkson95"},"createdOn":1795046250,"author":{"name":"Dongkyun Son","email":"dongkyun.s@samsung.com","username":"dkson95"},"kind":"REWORK","sizeInsertions":575,"sizeDeletions":30},{"number":4,"revision":"1ddecbe8729f832b5ef565092d039f68df647a43","parents":["f346dd75e87de324dc2abe61454ca1c49969d12d"],"ref":"refs/changes/24/361624/4","uploader":{"name":"Dongkyun Son","email":"dongkyun.s@samsung.com","username":"dkson95"},"createdOn":1795146544,"author":{"name":"Dongkyun Son","email":"dongkyun.s@samsung.com","username":"dkson95"},"kind":"TRIVIAL_REBASE","sizeInsertions":575,"sizeDeletions":30},{"number":5,"revision":"cbaa01f5c148f5cc705f969e13ac41fef811a9f9","parents":["f346dd75e87de324dc2abe61454ca1c49969d12d"],"ref":"refs/changes/24/361624/5","uploader":{"name":"Lin Hao","email":"hao.lin@samsung.com","username":"lhmax2025"},"createdOn":1795187618,"author":{"name":"Dongkyun Son","email":"dongkyun.s@samsung.com","username":"dkson95"},"kind":"REWORK","sizeInsertions":650,"sizeDeletions":29}]}
{"type":"stats","rowCount":1,"runTimeMilliseconds":2,"moreChanges":false}
```

[推送后查询原始 JSONL](../../tools/bolt/results/task147-push/gerrit-after.jsonl) · [推送后核对表](../../tools/bolt/results/task147-push/postflight.json)

本次 Gerrit 写入为一次明确指定的 `refs/for/tizen_base` 推送。证据归档分支为 `bolt-v4`。
