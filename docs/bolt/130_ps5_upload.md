# 130号 Gerrit 361395 PS5 上传核对


**续做结果：按 PM 修订规则通过文本门禁，Gerrit 拒绝上传（`no new changes`）。361395 最新仍为 PS4，未生成 PS5。**

**STOP，未上传 PS5。** 提交说明无命中。PS4→H5 完整 diff 的第622行上下文命中禁止词 `sandbox`。H5 和远端引用核对符合要求，Gerrit 最新仍为 PS4。未执行任何推送，未改提交或产品文件。

核对记录时间 `2026-11-17T22:12:48-08:00`。没有推送时间、推送输出或上传后核对结果。

## 命中原文

```diff
diff --git a/packaging/llvm.spec b/packaging/llvm.spec
@@ -1,9 +1,21 @@
 # Quickbuild sandbox: x86_64 BOLT is on by default; other architectures unchanged.
```

上述行在原始 diff 中有一个前导空格，是上下文行。任务门禁覆盖完整 diff，因此该行仍触发停止。停止原文如下。

```text
STOP: forbidden external text found in H5 message / full PS4 to H5 diff
```

## 上传前核对

- H5 `ed922413c19b01d07e0ec6547771267f40ab5469`
- Tree `66aa08d9e6717b904a0eb390096d908fea1109c0`
- 父提交 `61ef5d31ca91025c414c748477bef0c64ddfa67c`
- 唯一 Change-Id `I28171720d5bbbf9eaf491cdafc0aee0b43f9cd06`
- 远端 sandbox 分支指向 H5。
- 361395 项目为 `platform/upstream/llvm`，目标分支为 `tizen_base`，状态为 NEW，当前为 PS4。

| Patch set | Revision |
|---|---|
| 1 | `c5244e13258bb541458dcd4a08254217d7c556a9` |
| 2 | `d0b2e82aa90b11251a13b67d890642bf2fa6f66c` |
| 3 | `ecb2dec72ec5afde9c6c70f166e2ac12b47c093e` |
| 4 | `e9f16ee3c078f9a5ae563ee01e52ace27b28da4d` |

## 核对命令与扫描规则

Git 的 SSH 命令设置为 `/usr/bin/ssh -o BatchMode=yes`。只读命令均返回 0。

```sh
/usr/bin/git -C /home/linhao/Toolchain/development/llvm-optimize/temp/ps5-helper-126/source show -s --format=%H%n%T%n%P ed922413c19b01d07e0ec6547771267f40ab5469
/usr/bin/git -C /home/linhao/Toolchain/development/llvm-optimize/temp/ps5-helper-126/source show -s --format=%B ed922413c19b01d07e0ec6547771267f40ab5469
/usr/bin/git -C /home/linhao/Toolchain/development/llvm-optimize/temp/ps5-helper-126/source diff --no-ext-diff --no-textconv --full-index --binary --no-color e9f16ee3c078f9a5ae563ee01e52ace27b28da4d ed922413c19b01d07e0ec6547771267f40ab5469 --
/usr/bin/git -C /home/linhao/Toolchain/development/llvm-optimize/temp/ps5-helper-126/source ls-remote --exit-code ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm refs/heads/sandbox/lhmax2025/bolt_pgo
/usr/bin/ssh -o BatchMode=yes -p 29418 lhmax2025@review.tizen.org gerrit query --format=JSON --current-patch-set --patch-sets change:361395
```

逐行执行 Python `re.search(pattern, line, re.IGNORECASE)`，输入为上面命令返回的完整提交说明和完整 diff。实际模式如下。

```text
github|lhmax|llvm-optimize|sandbox|bolt-v4|codex|claude|/home/|\bAI[\s_-]+(?:review\w*|audit\w*|feedback|assist\w*|generat\w*|tool\w*|agent\w*|analysis)|\b(?:review\w*|audit\w*)[\s_-]+(?:by[\s_-]+)?AI\b|(?:AI|人工智能|模型)[\s_-]*(?:评审|审查|审阅|生成)|(?:评审|审查|审阅)[\s_-]*AI\b|\b(?:task|report|ticket|issue)[\s_#:-]*1[0-9x]{2}\b|(?<!\d)1[0-9x]{2}\s*号
```

- `/home/linhao/Toolchain/development/llvm-optimize/temp/task130-ps5-upload/h5-message.txt` 共 261 行、14197 字节。
- `/home/linhao/Toolchain/development/llvm-optimize/temp/task130-ps5-upload/ps4-to-h5.diff` 共 737 行、34911 字节。

共1处命中，见上文。原始命令回执和扫描记录位于同一本地目录的 `preflight-commands.json` 和 `scan.json`。

## 续做

**Gerrit 拒绝上传，PS5 未生成。** 上传尝试开始于 `2026-11-17T22:31:53-08:00`，结束于 `2026-11-17T22:32:04-08:00`。尝试上传的 H5 为 `ed922413c19b01d07e0ec6547771267f40ab5469`。

### 文本门禁

沿用首次核对中的大小写不敏感正则。提交说明逐行检查。diff 只对以 `+` 开头且不以 `+++` 开头的行执行门禁。两份输入均与首次保存的版本逐字节一致。

~~~sh
/usr/bin/git -C /home/linhao/Toolchain/development/llvm-optimize/temp/ps5-helper-126/source show -s --format=%B ed922413c19b01d07e0ec6547771267f40ab5469
/usr/bin/git -C /home/linhao/Toolchain/development/llvm-optimize/temp/ps5-helper-126/source diff --no-ext-diff --no-textconv --full-index --binary --no-color e9f16ee3c078f9a5ae563ee01e52ace27b28da4d ed922413c19b01d07e0ec6547771267f40ab5469 --
~~~

- 提交说明扫描 261 行，命中 0 处。
- 完整 diff 共 737 行，门禁扫描 393 行新增内容，命中 0 处。
- diff 第 622 行是 `packaging/llvm.spec` 的 PS4 既有上下文，保留为非门禁命中。删除行无命中。

~~~diff
 # Quickbuild sandbox: x86_64 BOLT is on by default; other architectures unchanged.
~~~

### 推送及后续核对

沿用首次已通过的 tree、父提交、Change-Id 与 sandbox HEAD 核对。推送前重新查询同一个项目和分支上的 361395，状态为 NEW，最新为 PS4 `e9f16ee3c078f9a5ae563ee01e52ace27b28da4d`。

~~~sh
/usr/bin/ssh -o BatchMode=yes -p 29418 lhmax2025@review.tizen.org gerrit query --format=JSON --current-patch-set --patch-sets change:361395
/usr/bin/git -C /home/linhao/Toolchain/development/llvm-optimize/temp/ps5-helper-126/source push ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm ed922413c19b01d07e0ec6547771267f40ab5469:refs/for/tizen_base
~~~

Gerrit 推送退出码为 1。以下为完整输出，终端进度的回车按换行呈现。

~~~text
remote: 
remote: Processing changes: refs: 1        
remote: Processing changes: refs: 1, done            
To ssh://review.tizen.org:29418/platform/upstream/llvm
 ! [remote rejected]           ed922413c19b01d07e0ec6547771267f40ab5469 -> refs/for/tizen_base (no new changes)
error: failed to push some refs to 'ssh://review.tizen.org:29418/platform/upstream/llvm'
~~~

推送命令执行一次。未提交评论、投票或评审人变更。拒绝后做了两项只读核对。

~~~sh
/usr/bin/git -C /home/linhao/Toolchain/development/llvm-optimize/temp/ps5-helper-126/source ls-remote --exit-code ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm refs/changes/95/361395/5
/usr/bin/ssh -o BatchMode=yes -p 29418 lhmax2025@review.tizen.org gerrit query --format=JSON --current-patch-set --patch-sets change:361395
~~~

`ls-remote --exit-code` 返回 2，stdout 为空。Gerrit 查询再次返回 NEW，最新仍为 PS4。以下 patch set 列表在推送尝试前后相同。

| Patch set | Revision |
|---|---|
| PS1 | `c5244e13258bb541458dcd4a08254217d7c556a9` |
| PS2 | `d0b2e82aa90b11251a13b67d890642bf2fa6f66c` |
| PS3 | `ecb2dec72ec5afde9c6c70f166e2ac12b47c093e` |
| PS4 | `e9f16ee3c078f9a5ae563ee01e52ace27b28da4d` |

原始回执（含进度回车）及核对数据保存在本地 `/home/linhao/Toolchain/development/llvm-optimize/temp/task130-ps5-upload/resume`。
