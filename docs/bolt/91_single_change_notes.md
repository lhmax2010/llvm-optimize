# 91号：发布361395三条patch-set note，放弃361396/361397

**结论：PASS。授权的五项Gerrit写操作全部完成且回读核对通过。** 361395仍为NEW/PS3（ecb2dec7）；361396与361397均为ABANDONED/PS1。三条note使用PM定稿，逐字节一致；未推代码、未动sandbox、未构建、未投票或增加评审人。没有STOP、远端拒绝、准备错误或重试。

## 1. 输入与发布前门禁

[PM任务全文](../../tools/bolt/results/single-change-20261114/publish/pm-request.txt)来自本次附件。提取 `<<<PSn` 与 `>>>` 标记之间的正文行，保持行内文字、标点和正文换行不变，不包含标记及其分隔换行；文件末尾不另加换行。三份PM定稿覆盖的是发布内容选择，90号草稿文件本身未改动。

| 待发文本 | SHA256 | 字节数 |
|---|---|---|
| PS1-note.txt | 7bf81b733b612274667fa79dc85280634e4d436e481486d29e497c25b924ecc2 | 1262 |
| PS2-note.txt | c4004ef41e9423b1905f8d5943925213b498251cb9fe691b7bb0fbdea9d2b680 | 1759 |
| PS3-note.txt | 1ba8c66df7b48204029fd793dc3da82d8159163ba0c1672ddd248acb6aca1b93 | 2002 |
| abandon-361396.txt | 4a914a4a00207f8385b615a5fdaa4f364a2e09596268f919b908dd41793fd486 | 126 |
| abandon-361397.txt | dc6e53f8dd5ac9e9ec1238aa62b0ba279cdbf92d2306be55569872f93843e260 | 126 |

两份放弃说明逐字复制90号草稿；发送时仅不发送文件末尾的一枚换行符。原文件仍完整保存。所有五份文本均运行以下两条命令；10次检查都是grep rc=1、stdout/stderr为空，没有命中或执行错误。

```sh
grep -nP '[^\x00-\x7F]' TEXT
grep -niE 'github|lhmax|raw\.githubusercontent|bolt-v4|sandbox|/home/|docs/bolt|tools/bolt|\bmaster\b|\bmain\b|号' TEXT
```

[完整门禁argv/返回码](../../tools/bolt/results/single-change-20261114/publish/text-gates.json)。正文没有`tools/`路径命中；LLVM的cmake模块路径与clang/lld/llvm-ar CMakeLists均是产品源码定位，属于允许的LLVM路径，不是证据仓库引用。STATUS已新增长期对外文本规则：英文/ASCII；禁止总部不可访问的引用；每次发布前执行这两条门禁；任何命中停止。

发布前只读查询：

| Change | 状态 | 当前PS | revision |
|---|---|---|---|
| 361395 | NEW | 3 | ecb2dec72ec5afde9c6c70f166e2ac12b47c093e |
| 361396 | NEW | 1 | bde009d1197a09f7b7b76382a0166e03c841bdb9 |
| 361397 | NEW | 1 | 2cdd37ff747765e99c2befa3e6e8a88663ab77fe |

361395恰有3个PS，revision依次为c5244e13258bb541458dcd4a08254217d7c556a9、d0b2e82aa90b11251a13b67d890642bf2fa6f66c、ecb2dec72ec5afde9c6c70f166e2ac12b47c093e，符合授权；三条定稿尚未存在，未重复发布。[前置完整JSON](../../tools/bolt/results/single-change-20261114/publish/preflight-PASS.json)。

## 2. 三条note逐条发布与核对

全部SSH使用 `-o BatchMode=yes -p 29418 lhmax2025@review.tizen.org`。对远端命令整体使用POSIX shell quoting（Python shlex.join），作为ssh的单个远端命令参数传入；多行正文是远端review的单一 `--message` 参数。发布前还验证 `shlex.split(command)==remote_argv`。原始远端命令与argv均落盘，包含原始多行正文；没有任何label或reviewer参数。

| 操作 | 命令目标 | 发布rc | 回读比较 | 查询原文 |
|---|---|---|---|---|
| PS1 note | gerrit review 361395,1 --message … | 0 | PASS | [after-note1](../../tools/bolt/results/single-change-20261114/publish/361395-after-note1.stdout) |
| PS2 note | gerrit review 361395,2 --message … | 0 | PASS | [after-note2](../../tools/bolt/results/single-change-20261114/publish/361395-after-note2.stdout) |
| PS3 note | gerrit review 361395,3 --message … | 0 | PASS | [after-note3](../../tools/bolt/results/single-change-20261114/publish/361395-after-note3.stdout) |

每次都在本条回读通过后才执行下一条。比较仅移除自动前缀 `Patch Set N:\n\n`，不规范化空白、不重新折行、不做其他替换。其余正文UTF-8字节与PSn-note.txt完全相同，且恰有一条新匹配评论。完整实际消息分别保存为note1/2/3-actual-message.txt；验证JSON为note1/2/3-PASS.json。

[PS1正文](../../tools/bolt/results/single-change-20261114/publish/PS1-note.txt)；[PS2正文](../../tools/bolt/results/single-change-20261114/publish/PS2-note.txt)；[PS3正文](../../tools/bolt/results/single-change-20261114/publish/PS3-note.txt)。发布页：[361395](https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361395)。

## 3. 放弃旧change与最终状态

仅三条note全部核对通过后，依次执行：

```text
gerrit review 361396,1 --abandon --message <90号Part 2说明>
gerrit review 361397,1 --abandon --message <90号Part 3说明>
```

| 操作 | rc | 状态回读 | 放弃说明 | 原始查询 |
|---|---|---|---|---|
| 361396,1 abandon | 0 | ABANDONED/PS1 | 与草稿正文一致并已显示 | [361396-after-abandon](../../tools/bolt/results/single-change-20261114/publish/361396-after-abandon.stdout) |
| 361397,1 abandon | 0 | ABANDONED/PS1 | 与草稿正文一致并已显示 | [361397-after-abandon](../../tools/bolt/results/single-change-20261114/publish/361397-after-abandon.stdout) |

放弃说明查询中带有自动 `Abandoned\n\n` 前缀，后面完整正文与草稿一致。每次放弃后都另查361395，仍为NEW/PS3、三个revision不变。[最终361395查询](../../tools/bolt/results/single-change-20261114/publish/361395-after-abandon-361397.stdout)还再次确认三条定稿各存在一次。

说明原文：

```text
Superseded by 361395 PS3, which carries this commit unchanged as Part 2 (identical diff). Abandoning to keep a single review.
Superseded by 361395 PS3, which carries this commit unchanged as Part 3 (identical diff). Abandoning to keep a single review.
```

## 4. 边界、读证据与执行结果

已读：本次PM附件、STATUS长期规则、90号两份放弃草稿、发布前及每次写入后的Gerrit query完整返回。没有重新审计PM定稿中的历史技术数字，执行的是用户指定定稿发布；没有访问QB、运行构建或产品工具、修改LLVM提交/工作树、查询或修改sandbox。Gerrit写入恰为三个review message与两次abandon；没有评论外的其他写操作。

全部命令串行运行在 `llvm-review91-20261114` 用户服务，4GiB、swap0、Nice19、idle。[资源原文](../../tools/bolt/results/single-change-20261114/publish/resource-properties.txt)。证据仓库按长期规则只提交/普通推送bolt-v4，不推main、不force push；旧草稿、历史证据未删除或覆盖。

STOP原文：**无**。远端拒绝原文：**无**。准备错误与重试：**0**。五项写操作的stdout/stderr与完整argv均见 [raw索引](../../tools/bolt/results/single-change-20261114/publish/RAW_LINKS.md)。

```text
91 preflight 已结束 2026-11-14T01:22:34-08:00 status=PASS
91 note1 已结束 2026-11-14T01:23:11-08:00 status=PASS
91 note2 已结束 2026-11-14T01:23:31-08:00 status=PASS
91 note3 已结束 2026-11-14T01:24:03-08:00 status=PASS
91 abandon361396 已结束 2026-11-14T01:24:32-08:00 status=PASS
91 abandon361397 已结束 2026-11-14T01:25:03-08:00 status=PASS
```

91 已结束 2026-11-14T01:26:43-08:00 status=PASS
