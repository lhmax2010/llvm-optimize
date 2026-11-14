# 89号：361395 单一评审的本地准备

**结论：STOP（准备脚本错误，不是产品失败）。PS2、PS3 尚未生成。**

前置身份核对通过；读取原 BOLT 提交的 trailer 时，我编写的准备脚本错误要求其顺序与 PS1 相同，触发断言。遵守本任务“规定外情况 STOP”，未修改断言或重跑。未创建新工作树、未运行 commit-tree、未推送 LLVM 或写入 Gerrit。

## 1. 已完成的只读核对

| 原提交 | 完整 SHA | tree |
|---|---|---|
| 混合链接 PS1 | c5244e13258bb541458dcd4a08254217d7c556a9 | 3d961cbb04f5446f84d2089b4f65f3178f2bd7fa |
| BOLT | bde009d1197a09f7b7b76382a0166e03c841bdb9 | c23914776684bf94fdd5961f447f7c24e7bb79bc |
| 固定参数/转换器 | 2cdd37ff747765e99c2befa3e6e8a88663ab77fe | b2e8af2477cf623a945aa80bf8288a262dd4a5a9 |

PS1 父提交为 `13c3e223d9e1b35e4affb55255c5042f8c940f35`。只读 ls-remote 返回：

```
61ef5d31ca91025c414c748477bef0c64ddfa67c	refs/heads/tizen_base
```

tizen_base tree 与 PS10 相同，符合本次前提；未 fetch、未更新本地分支。完整提交对象及身份见 [original-chain.json](../../tools/bolt/results/single-change-20261114/original-chain.json) 和证据索引。

## 2. STOP 原文及原因

以下为此次执行工具返回的 traceback 原文转录，未重跑以重新取得错误：

```text
Traceback (most recent call last):
  File "/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/single-change-20261114/create_commits.py", line 23, in <module>
    trailers=parts[1].splitlines();assert len(trailers)==2 and trailers[0]=='Signed-off-by: Hao Lin <hao.lin@samsung.com>' and trailers[1].startswith('Change-Id: ')
                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError
```

触发点是第二个原提交。PS1 的末段为 Signed-off-by、Change-Id；BOLT 和固定参数原提交的末段均为 Change-Id、Signed-off-by。用户只要求新 PS2/PS3 的 trailer 顺序以 PS1 为准，并未要求旧三个提交顺序相同。脚本把这两项混淆，属于我的准备错误，不是提交内容错误。错误脚本原样保留：[create_commits.py](../../tools/bolt/results/single-change-20261114/create_commits.py)。

原说明与 r8 比较的断言在原提交 1、2 均已越过；第 3 份未运行。没有将这两个局部结果表述为全部说明核对通过。新独立工作树不存在，停止前后 worktree list 逐字节相同：True。

## 3. 各步状态与未运行项

| 用户步骤 | 结果 |
|---|---|
| 1 生成提交 | 前置核对通过；生成前 STOP；PS2/PS3 SHA 均无 |
| 2 核对与导出 | NOT RUN：未生成新提交，未运行增量 diff、分节正文 diff、gbs export 或导出 spec 解析 |
| 3 三条 note | NOT RUN：三条 note 草稿均未生成 |
| 4 记录 | 已保存本停止报告、原始对象、错误脚本和停止后只读核对；STATUS 追加停点 |

未运行构建；未改变现有 LLVM 分支、工作树、源码或提交；未访问 QB；没有 Gerrit/sandbox 推送。只读远端操作只有上述 tizen_base ls-remote。没有新两份提交说明或完整 format-patch，不能提供这些文件及三条 note 的 raw 链接。

## 4. 证据边界与资源

已读：STATUS、81 号、r8 README、维护文档的 Source 声明与导出解析规则、三个原提交对象、r8 的 0001/0002 补丁说明、tizen_base 提交和树、工作树列表。未读/未执行：r8 第三份说明的脚本比对、构建产物、QB 网页或日志、导出源码包、Gerrit 评审状态。

执行在串行用户服务 `llvm-prep89-20261114` 中，MemoryMax=4G、MemorySwapMax=0、Nice=19、IOSchedulingClass=idle。未构建，未发生 OOM，未修改资源上限。证据仓库中已有无关未跟踪文件保持原样，不纳入本次提交。

[全部 raw 链接索引](../../tools/bolt/results/single-change-20261114/RAW_LINKS.md)。后续需用户裁决是否允许纠正 trailer 解析后继续；本次不自行继续。

89 已结束 2026-11-14T16:26:31+08:00 status=STOP


## 89号续

**结论：步骤1与提交核对通过；步骤2的导出比较 STOP。两个本地单提交已生成，尚不能宣称全部核对完成。** 原 STOP 原文及此前结论保留在上面；本节为最新停点。

### PM 裁决与准备修正

PM 定性：首次 STOP 为准备脚本错误，不是产品问题；原提示词没有说明三个原提交 trailer 顺序不同，不计准备错误次数。本次按 PM 授权接受顺序不限的两行末段，只允许唯一 Signed-off-by 和唯一 Change-Id；新 PS2/PS3 仍按 PS1 顺序写 Signed-off-by、Change-Id。没有改变正文或产品代码。

[首次错误](../../tools/bolt/results/single-change-20261114/resume/first-error.txt)、[修正 diff](../../tools/bolt/results/single-change-20261114/resume/preparation-fix.diff)、[执行输出](../../tools/bolt/results/single-change-20261114/resume/create.stdout)。diff 另含新证据目录由原目录改为 resume/，旧脚本未覆盖。

再次只读查询 tizen_base：`61ef5d31ca91025c414c748477bef0c64ddfa67c`，tree 与 `13c3e223` 相同。PS1 父提交及原三提交链、tree 均重新核对通过。[preflight.json](../../tools/bolt/results/single-change-20261114/resume/preflight.json)。没有 fetch 或 Gerrit 写操作。

### 步骤1：两个单提交

| 意图 | SHA | tree | 父提交 |
|---|---|---|---|
| PS2 | d0b2e82aa90b11251a13b67d890642bf2fa6f66c | c23914776684bf94fdd5961f447f7c24e7bb79bc | 13c3e223d9e1b35e4affb55255c5042f8c940f35 |
| PS3 | ecb2dec72ec5afde9c6c70f166e2ac12b47c093e | b2e8af2477cf623a945aa80bf8288a262dd4a5a9 | 13c3e223d9e1b35e4affb55255c5042f8c940f35 |

两个提交均使用独立游离工作树 `/home/linhao/Toolchain/development/llvm-optimize/temp/single-change-20261114/source` 内的 `git commit-tree` 创建，未新建或修改分支。当前该新工作树 HEAD 为 PS3，工作树干净。已有本地分支 refs 和原 source 工作树 status 在操作前后逐字相同。PS1 不动。

作者均为 `Hao Lin <hao.lin@samsung.com>`，作者时间沿用 PS1 的 `1792065558 +0800`；提交者以指定 git -c 身份设置。PS2/PS3 使用建议标题，无需调整。原三说明的正文与 r8 补丁逐字核对通过；分节标题不替换正文用词。所有新说明行长≤72列，唯一 trailer 为：

```text
Signed-off-by: Hao Lin <hao.lin@samsung.com>
Change-Id: I28171720d5bbbf9eaf491cdafc0aee0b43f9cd06
```

[PS2说明](../../tools/bolt/results/single-change-20261114/resume/PS2-message.txt)、[PS3说明](../../tools/bolt/results/single-change-20261114/resume/PS3-message.txt)；完整 format-patch 为同目录 `PS2.patch`、`PS3.patch`。五份 Part diff 均为空，见 `PS2-part1.diff`、`PS2-part2.diff` 和 `PS3-part1.diff` 至 `PS3-part3.diff`。

### 步骤2：已通过的提交检查与导出 STOP

[提交核对](../../tools/bolt/results/single-change-20261114/resume/commit-validation.json)：

- PS2/PS3 的 tree、父提交、作者、作者日期、提交者、trailer 和说明全文均符合要求。
- `git diff c5244e13 PS2` 与 `git diff c5244e13 bde009d1` 逐字节相同。
- `git diff PS2 PS3` 与 `git diff bde009d1 2cdd37ff` 逐字节相同。
- `git diff 2cdd37ff PS3` 为空。

两次 gbs export 均 rc=0，命令完整 argv、stdout/stderr 已保存。使用新工作树加 `--commit` 分别导出，未修改旧工作树，未使用 `--no-patch-export` 隐藏补丁。导出目录：

- `/home/linhao/Toolchain/development/llvm-optimize/temp/single-change-20261114/export-PS3`
- `/home/linhao/Toolchain/development/llvm-optimize/temp/single-change-20261114/export-old`

每侧21个文件。18个同名文件大小、SHA、权限完全相同，包括源码 tar、Source1200、helper、转换器、模型、0001–0007 和 SOURCE_PROVENANCE。两个 spec 与0008有以下差异：

| 文件 | 差异 | 本次处理 |
|---|---|---|
| llvm.spec | VCS 行；Patch7 引用名；%patch 前的补丁文件名注释 | 后两项超出仅 VCS/提交号预期，STOP |
| libcxx-runtimes.spec | 同上 | STOP |
| 0008 | 文件名、Subject、总述、Part 标题及新增 Part 2/3 提交说明 | 不是单纯提交号变化，STOP |

旧补丁名为 `0008-cmake-use-hybrid-LLVM-linkage-on-x86_64.patch`，新补丁名为 `0008-x86_64-hybrid-linkage-BOLT-clang-fixed-flags-and-arc.patch`。

两份0008从第一个 `diff --git` 到文件末尾**逐字节相同**，SHA256均为 `e99fa7abdc0a828c9eb9295c163a239ed7438c0df378446bf10e07ae3a89b6c6`。这说明代码正文没变，但不能据此自行放宽用户的导出文件比较规则。

[逐文件清单与结论](../../tools/bolt/results/single-change-20261114/resume/export-comparison.json)、[0008完整diff](../../tools/bolt/results/single-change-20261114/resume/export-0008.diff)、[llvm.spec diff](../../tools/bolt/results/single-change-20261114/resume/export-llvm.spec.diff)、[libcxx-runtimes.spec diff](../../tools/bolt/results/single-change-20261114/resume/export-libcxx-runtimes.spec.diff)。源码包文件留在本地新导出目录，GitHub保存清单、SHA和全部文本差异，没有上传两份大tar。

本次 STOP 原文：

```text
STOP: export comparison exceeded the permitted VCS/commit-ID-only differences: 0008 patch filename and commit message changed; llvm.spec and libcxx-runtimes.spec Patch7 declarations and patch-name comments changed. No exception was added. Exported-spec parsing and patch-set notes were not run.
```

停止后整理报告时，我的显示命令还错误请求了 `export-SOURCE_PROVENANCE.diff`；实际上该文件没有差异，所以不存在 diff。报错为：

```text
FileNotFoundError: [Errno 2] No such file or directory: 'tools/bolt/results/single-change-20261114/resume/export-SOURCE_PROVENANCE.diff'
```

按新长期规则，报告准备阶段修正一次：只从比较结果中的 changed 列表读取实际 diff，原始错误与 [修正diff](../../tools/bolt/results/single-change-20261114/resume/report-display-fix.diff) 保留。重新显示成功；未重跑导出，未改变任何比较结果或放宽规则，导出 STOP 保持。

### 步骤3、4与证据边界

步骤3三条 note **NOT RUN**，因此没有三条 note 的 raw 链接。导出 spec 的五项平台解析（x86开/关、ARM两架构、一行bcond回退）也 **NOT RUN**，不能用提交 tree 相同代替解析通过。步骤4完成停点记录、完整补丁和说明的归档，以及 STATUS 追加。

本轮已读：原三提交、r8三份完整说明、维护文档 Source/Patch 规则、已有解析脚本、远端 tizen_base、两份实际导出目录的全部文件SHA和差异文本。未读/未做：QB、构建结果重新验证、Gerrit评审状态、产品编译或运行、note发布；没有任何LLVM远端推送。

分析和导出均在串行4GiB/swap0/Nice19/idle用户服务 `llvm-prep89-resume-20261114` 中运行。所有既有证据只读；原 STOP 未删除。新 [raw链接索引](../../tools/bolt/results/single-change-20261114/resume/RAW_LINKS.md)。需 PM 裁决是否允许上述导出说明/文件名变化，不能作为准备错误修正规则来自动放行。

89续 已结束 2026-11-14T00:40:16-08:00 status=STOP
