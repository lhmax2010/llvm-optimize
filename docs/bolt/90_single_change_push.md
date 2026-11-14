# 90号：361395 PS2/PS3 上传与 sandbox 同步

**结论：推送前门禁、两次 Gerrit 上传和 sandbox 同步全部 PASS。** 361395 为 NEW/PS3；PS1 未变。361396/361397 仍为 NEW/PS1。本次三条英文 note 和两份放弃说明只是本地草稿，没有发布。无远端拒绝或 STOP；两次 Gerrit 上传均提示标题超过50字符，属于成功响应中的 warning，未修改说明（本任务上限72列）。

## 1. 冻结裁决与导出比较

先将 PM 的三类允许差异写入89号和STATUS，随后执行比较；[裁决原文](../../tools/bolt/results/single-change-20261114/push/pm-ruling.md)。只允许：两个spec的VCS；Patch7文件名和%patch前文件名注释；0008文件名及Subject/说明，代码正文必须逐字相同。以后单评审QB源码包比较也按此冻结范围处理，等同R2(e)中的Patch写法差异。89号原STOP未删。

| 配对 | 导出结果 | 同名且完整相同文件 | 允许差异 | 结论 |
|---|---|---|---|---|
| PS3 ecb2dec7 / 原2cdd37ff | 复用89号实际导出，重新读取全部文件计算SHA | 18/21 | 两个spec、0008，恰为三类裁决 | PASS |
| PS2 d0b2e82a / 原bde009d1 | 本次各执行一次gbs export，均rc=0 | 18/21 | 两个spec、0008，不涉及Part3 | PASS |

PS3两份0008从首个 `diff --git` 到末尾SHA均为 `e99fa7abdc0a828c9eb9295c163a239ed7438c0df378446bf10e07ae3a89b6c6`；PS2为 `e99fa7abdc0a828c9eb9295c163a239ed7438c0df378446bf10e07ae3a89b6c6`。[含diff标记的完整正文SHA](../../tools/bolt/results/single-change-20261114/push/patch-code-full-sha.json)。comparison.json中的同名摘要字段从首个diff标记之后起算；本处明确采用含标记的完整范围，两种范围各自的新旧结果均相同。

[PS3逐文件比较](../../tools/bolt/results/single-change-20261114/push/PS3-comparison.json)、[PS2逐文件比较](../../tools/bolt/results/single-change-20261114/push/PS2-comparison.json)包含大小、权限、SHA和差异分类，全部文本diff保留同目录。没有扩大白名单。

## 2. 五项解析（两组均通过）

用历史Tizen RPM工具及其loader只读运行；`rpmbuild -bp --nodeps --nobuild` 仅解析，不执行prep/build脚本；另用 `rpmspec -P` 保存完整展开。输入来自实际gbs导出目录，不是源码原spec。

| 配置 | PS3/2cdd配对 | PS2/bde配对 | Patch声明 | BOLT步骤 |
|---|---|---|---|---|
| x86_64 开 | PASS | PASS | 0–7全可见 | 存在 |
| x86_64 关 | PASS | PASS | 0–7全可见 | 不存在 |
| armv7l | PASS | PASS | 0–7全可见 | 不存在 |
| aarch64 | PASS | PASS | 0–7全可见 | 不存在 |
| x86一行bcond回退 | PASS | PASS | 0–7全可见 | 不存在 |

合计10个配对场景，20次平台nobuild解析和20次完整展开；10份配对展开diff为空。配对时先隔离已被导出门禁核对过的VCS元数据和本次执行各自的_sourcedir/_topdir路径，然后只规范化Patch7文件名及对应注释；不放宽构建脚本差异。回退只在新解析目录内复制的导出spec上把一行bcond_without改为bcond_with。

[PS3解析原文索引](../../tools/bolt/results/single-change-20261114/push/PS3-five-parse-summary.json)、[PS2解析原文索引](../../tools/bolt/results/single-change-20261114/push/PS2-five-parse-summary.json)、[完整脚本](../../tools/bolt/results/single-change-20261114/push/gates.py)。本轮没有准备错误修正或重试。

## 3. 推送前身份及远端复查

`tizen_base=61ef5d31ca91025c414c748477bef0c64ddfa67c`；361395 NEW/PS1，revision c5244e13258bb541458dcd4a08254217d7c556a9。sandbox为2cdd37ff747765e99c2befa3e6e8a88663ab77fe。两本地提交tree、父提交和说明与89续逐字核对。

| Patch set | revision | tree |
|---|---|---|
| PS1（不变） | c5244e13258bb541458dcd4a08254217d7c556a9 | 3d961cbb04f5446f84d2089b4f65f3178f2bd7fa |
| PS2 | d0b2e82aa90b11251a13b67d890642bf2fa6f66c | c23914776684bf94fdd5961f447f7c24e7bb79bc |
| PS3 | ecb2dec72ec5afde9c6c70f166e2ac12b47c093e | b2e8af2477cf623a945aa80bf8288a262dd4a5a9 |

三个patch set共享父13c3e223；不是在PS1之后继续叠加父链。[完整前置查询](../../tools/bolt/results/single-change-20261114/push/361395-before.stdout)。

## 4. 按顺序推送及复查

Gerrit全部使用 `GIT_SSH_COMMAND='ssh -o BatchMode=yes'` 和完整地址。三次命令实际原文：

```sh
GIT_SSH_COMMAND='ssh -o BatchMode=yes' git -c gc.auto=0 push ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm d0b2e82aa90b11251a13b67d890642bf2fa6f66c:refs/for/tizen_base
GIT_SSH_COMMAND='ssh -o BatchMode=yes' git -c gc.auto=0 push ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm ecb2dec72ec5afde9c6c70f166e2ac12b47c093e:refs/for/tizen_base
GIT_SSH_COMMAND='ssh -o BatchMode=yes' git -c gc.auto=0 push --force-with-lease=refs/heads/sandbox/lhmax2025/bolt_pgo:2cdd37ff747765e99c2befa3e6e8a88663ab77fe ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm ecb2dec72ec5afde9c6c70f166e2ac12b47c093e:refs/heads/sandbox/lhmax2025/bolt_pgo
```

- PS2上传后查询NEW/PS2，revision匹配；然后才推PS3。
- PS3上传后查询NEW/PS3，patchSets恰有1/2/3，三者revision与上表完全一致。
- 最后以指定lease同步sandbox，并ls-remote确认新HEAD。
- 只读查询361396/361397，均仍NEW/PS1；没有放弃、评论、评分或增加评审人。

[361395当前评审](https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361395)，[PS2后原始query](../../tools/bolt/results/single-change-20261114/push/361395-after-PS2.stdout)，[PS3后原始query](../../tools/bolt/results/single-change-20261114/push/361395-after-PS3.stdout)。推送完整stdout/stderr分别为push-PS2、push-PS3、push-sandbox，均在证据索引中。

sandbox：

```text
before: 2cdd37ff747765e99c2befa3e6e8a88663ab77fe
after:  ecb2dec72ec5afde9c6c70f166e2ac12b47c093e
```

[before ls-remote](../../tools/bolt/results/single-change-20261114/push/sandbox-before.stdout)、[after ls-remote](../../tools/bolt/results/single-change-20261114/push/sandbox-after.stdout)。拒绝/STOP原文：**无**。两个成功响应均含 `warning: subject >50 characters; use shorter first paragraph`，没有擅自重新生成或重推提交。

## 5. 草稿（未发布）

- [PS1 note](../../tools/bolt/results/single-change-20261114/push/PS1-note-draft.txt)：30行。
- [PS2 note](../../tools/bolt/results/single-change-20261114/push/PS2-note-draft.txt)：29行。
- [PS3 note](../../tools/bolt/results/single-change-20261114/push/PS3-note-draft.txt)：31行。
- [361396放弃说明草稿](../../tools/bolt/results/single-change-20261114/push/abandon-361396-draft.txt)。
- [361397放弃说明草稿](../../tools/bolt/results/single-change-20261114/push/abandon-361397-draft.txt)。

草稿列明实际增量文件、x86/ARM边界、回退方法和证据；不宣称PS1/PS2独立完整构建过。最终tree的102/102 QB载荷结论引用79号；本地T/D引用74/79的规则B与PM放行，不宣称所有原始RPM字节相同。PS3列出历史速度数据、QB A/B待做、jump-past-end两处A级八处B级、2804明细及后续加固。不把八处B级写成已严格证明不可达。

## 6. 读了什么、没有做什么

已读：STATUS长期署名规则、89续提交/导出证据、维护文档Source/Patch规则、两组实际导出文件、平台完整解析输出、原三个提交文件列表、79号B1–B6最终表、74号8.10 R3、87号告警证据等级、Gerrit及ls-remote原始返回。没有访问QB、重跑二进制验证、构建、修改LLVM内容/提交/分支、发布note或放弃说明。

所有分析、导出、解析及推送在同一串行用户服务内执行；[资源属性](../../tools/bolt/results/single-change-20261114/push/resource-properties.txt)：4GiB、swap0、Nice19、idle。观察到memory.peak约3.49GiB，无OOM。历史构建根只读；本次解析/导出写新目录，原证据保留。

本任务明示仅授权三项远端写操作，现已全部完成。因此本节记录时证据仓库仅准备本地提交；GitHub bolt-v4另行推送需要确认。raw索引为计划发布路径，未发布前不能声称可访问。

[raw索引](../../tools/bolt/results/single-change-20261114/push/RAW_LINKS.md)。

```text
90步骤1 已结束 2026-11-14T00:51:20-08:00 status=PASS
90步骤2 PS2 已结束 2026-11-14T00:52:15-08:00 status=PASS
90步骤2 PS3 已结束 2026-11-14T00:52:47-08:00 status=PASS
90步骤2 sandbox 已结束 2026-11-14T00:53:29-08:00 status=PASS
90步骤3 已结束 2026-11-14T00:54:46-08:00 status=PASS (drafts only)
```

90核对与授权推送 已结束 2026-11-14T00:56:59-08:00 status=PASS
