# 81. 第三个提交说明修正、Gerrit 上传与 sandbox 同步

结论：**PASS（续跑完成）**。第一批已上传、评审中，三个 Change 均为 NEW / tizen_base / Patch Set 1；sandbox HEAD=2cdd37ff747765e99c2befa3e6e8a88663ab77fe。旧失败原始文件保留不动。本文同时记录第一次被拒与本次续跑，不把旧失败改写成成功。

## 1. 读取范围与执行边界

已读取：80号、STATUS 的相关历史/最新停点、79号最终总结；r7 三个补丁、v2/v3 草稿；两次提交对象/作者/树/说明；本次和上次 Gerrit query、ls-remote、push 原始输出；v9 全文件大小及 SHA。第七轮外部评审结论按用户本次提供的信息记录，不声称独立读取两份外部评审原件。

未读取或运行：QB 页面/日志/产物、历史构建根、构建或产品测试；未加评审人、未打分、未提交合入、未推其他 LLVM 分支。本次只在独立游离 HEAD 重建，原 LLVM 工作分支不变。

所有命令由串行 systemd 用户服务执行：MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、Nice=19、IOSchedulingClass=idle。[本服务属性](../../tools/bolt/results/gerrit-upload81-20261113/resume/resource-properties.txt)。Gerrit 全程 SSH BatchMode，完整 URL，禁用终端凭据提示；没有密码输入。身份使用 git -c user.name="Hao Lin" -c user.email=hao.lin@samsung.com。

准备阶段：一次 STATUS.md 路径读取错误（实际文件为 docs/bolt/STATUS.md）已修正；rg 在服务 PATH 中不可用，改用已知路径直接读取；没有改产品判定或证据。[记录](../../tools/bolt/results/gerrit-upload81-20261113/resume/preparation-notes.txt)。上次推送顺序问题按 PM 裁决不计入准备修正次数。

## 2. 第一次执行：说明修改、树不变，上传被拒

原链8e35d0c9 → 51417b0f → 4e80f54e，底父13c3e223。三个 Change-Id 的第一次 query 均查不到。0003 的 Ic76505ddb122f1e06271ff7462e24eceee4d400a **不是**已合入359934；359934实际 Change-Id 为 I1c0d0bcccb1dc3c64efbb635e3e6f3de6748209e（状态MERGED），见[原始查询](../../tools/bolt/results/gerrit-upload81-20261113/pre-query-359934.stdout)。

只把“For PIC, reject 8- and 16-bit absolute relocations”改为“For converted PIC members, reject 8- and 16-bit absolute relocations”；仅该段重新按72列折行，连字符词不拆分。其余段落逐字节不变。前两个说明与r7相同。

[v3草稿](../../tools/bolt/results/qb-1226850-1226851/commit-message-drafts/0003-final-draft-v3.txt)；[v3相对v2完整diff](../../tools/bolt/results/gerrit-upload81-20261113/0003-v3-vs-v2.diff)；[第一次核对JSON](../../tools/bolt/results/gerrit-upload81-20261113/verification.json)。

第一次 range-diff 原文：

~~~text
1:  8e35d0c90d5d = 1:  1d02292f6697 cmake: use hybrid LLVM linkage on x86_64
2:  51417b0fa060 = 2:  ccf9b4e756bd packaging: optimize x86_64 clang with BOLT
3:  4e80f54e10fe ! 3:  01c503a5158e packaging: fix x86 LLVM flags and archive mode
    @@ Commit message
         indexes. Check each relocation against an explicit x86_64 field width
         table taken from LLVM 22.1.8, excluding seven dynamic-linking-only
         types: COPY, GLOB_DAT, JUMP_SLOT, RELATIVE, DTPMOD64, TLSDESC and
    -    IRELATIVE. Reject types outside the table and CREL sections. For PIC,
    -    reject 8- and 16-bit absolute relocations in allocated sections when
    -    they reference non-absolute symbols; retain the existing 32- and 64-bit
    -    PIC checks. Validate relocation field bounds against the target section;
    -    for compressed targets, use the declared uncompressed size as the bound.
    -    Handle SIGHUP and process-group reaping during conversion, reset an
    -    inherited ignored SIGCHLD, keep inherited ignored TERM, INT and HUP
    -    ignored, and exit with 128+signal after cancellation, deciding the final
    -    status after the original handlers are restored. With BOLT enabled, the
    -    spec passes the converter's 129/130/143 through; with BOLT disabled, the
    -    call keeps exit 1 so that expansion is unchanged.
    +    IRELATIVE. Reject types outside the table and CREL sections. For
    +    converted PIC members, reject 8- and 16-bit absolute relocations in
    +    allocated sections when they reference non-absolute symbols; retain the
    +    existing 32- and 64-bit PIC checks. Validate relocation field bounds
    +    against the target section; for compressed targets, use the declared
    +    uncompressed size as the bound. Handle SIGHUP and process-group reaping
    +    during conversion, reset an inherited ignored SIGCHLD, keep inherited
    +    ignored TERM, INT and HUP ignored, and exit with 128+signal after
    +    cancellation, deciding the final status after the original handlers are
    +    restored. With BOLT enabled, the spec passes the converter's 129/130/143
    +    through; with BOLT disabled, the call keeps exit 1 so that expansion is
    +    unchanged.
     
         Based on Change 359934: keeps its token classification, per-switch
         replay and adopted checks; adds the declared debug-info mode with a
~~~

第一次新链：1d02292f6697b31a6f88461310108c4e4df8227f → ccf9b4e756bd76109c8bcc268ec4383d0206f633 → 01c503a5158ecec8b6df5c338765f675f0d7bed4。
三棵树仍为下表相同值，作者及作者日期相同，最终diff为空；只第三个说明指定段落变化。第一次 sandbox 已成功更新到01c503a5，然后上传评审被拒，未重试。

第一次上传命令：

~~~sh
git push ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm 01c503a5158ecec8b6df5c338765f675f0d7bed4:refs/for/tizen_base
~~~

远端拒绝原文（stdout为空，以下为stderr）：

~~~text
remote: 
remote: Processing changes: refs: 1        
remote: Processing changes: refs: 1, done            
To ssh://review.tizen.org:29418/platform/upstream/llvm
 ! [remote rejected]           01c503a5158ecec8b6df5c338765f675f0d7bed4 -> refs/for/tizen_base (no new changes)
error: failed to push some refs to 'ssh://review.tizen.org:29418/platform/upstream/llvm'
~~~

**PM 裁决（本次续跑授权）：** 先推 sandbox 再用同组提交推 refs/for，提交已在仓库分支上，导致 no new changes；这是 PM 安排的推送顺序错误，不是代码问题。本次更新时间重建新 SHA，先上传评审，核对成功后同步 sandbox。

## 3. 续跑前置与第二次重建

前置 sandbox 仍为01c503a5；tizen_base=61ef5d31ca91025c414c748477bef0c64ddfa67c，tree=087e06cf9c79c571c711af8a07057496940ae73d，等于13c3e223的tree，**verdict B**。原提交链和树正确，工作树干净，三个 Change-Id 仍查不到。

ls-remote：

~~~text
01c503a5158ecec8b6df5c338765f675f0d7bed4	refs/heads/sandbox/lhmax2025/bolt_pgo
61ef5d31ca91025c414c748477bef0c64ddfa67c	refs/heads/tizen_base
~~~


从13c3e223使用 commit-tree 重建，逐提交保留原tree、作者、作者日期、说明、Change-Id和Signed-off-by；仅提交者时间更新，后续提交的父SHA随之更新，不改文件内容。原提交者和新提交者均为Hao Lin，详细时间见[重建JSON](../../tools/bolt/results/gerrit-upload81-20261113/resume/rebuilt.json)。

|序号|提交 SHA|tree SHA|标题|
|---|---|---|---|
|1|c5244e13258bb541458dcd4a08254217d7c556a9|3d961cbb04f5446f84d2089b4f65f3178f2bd7fa|cmake: use hybrid LLVM linkage on x86_64|
|2|bde009d1197a09f7b7b76382a0166e03c841bdb9|c23914776684bf94fdd5961f447f7c24e7bb79bc|packaging: optimize x86_64 clang with BOLT|
|3|2cdd37ff747765e99c2befa3e6e8a88663ab77fe|b2e8af2477cf623a945aa80bf8288a262dd4a5a9|packaging: fix x86 LLVM flags and archive mode|


两次重建的树核对：上述三棵树分别与r7旧链、第一次重建链完全相同；第一次核对JSON及本次重建JSON都为PASS。三份说明与第一次链逐字节相同、最长72列。git diff 01c503a5 新HEAD 输出为空；本次range-diff全部为“=”：

~~~text
1:  1d02292f6697 = 1:  c5244e13258b cmake: use hybrid LLVM linkage on x86_64
2:  ccf9b4e756bd = 2:  bde009d1197a packaging: optimize x86_64 clang with BOLT
3:  01c503a5158e = 3:  2cdd37ff7477 packaging: fix x86 LLVM flags and archive mode
~~~

推送前 fetch 了完整URL的 refs/heads/* 到独立审计 remote-tracking refs，未修改本地工作分支/remote配置；fetch前后逐一运行 git branch -r --contains 新SHA，六份输出均为空。[fetch原文](../../tools/bolt/results/gerrit-upload81-20261113/resume/fetch-all-remote-branches.stderr)、[refs快照](../../tools/bolt/results/gerrit-upload81-20261113/resume/refs-after-fetch.stdout)、[全部命令](../../tools/bolt/results/gerrit-upload81-20261113/resume/commands.jsonl)。

## 4. 三个 Change-Id：推送前后 query 原文

使用 ssh -o BatchMode=yes -p 29418 lhmax2025@review.tizen.org gerrit query --format=JSON --current-patch-set change:<Change-Id>。前置均0条，上传后均NEW，branch=tizen_base，currentPatchSet.revision逐个等于上传SHA。

### 1. I28171720d5bbbf9eaf491cdafc0aee0b43f9cd06

第一次前置：

~~~json
{"type":"stats","rowCount":0,"runTimeMilliseconds":0,"moreChanges":false}
~~~

续跑上传前：

~~~json
{"type":"stats","rowCount":0,"runTimeMilliseconds":0,"moreChanges":false}
~~~

上传后：

~~~json
{"project":"platform/upstream/llvm","branch":"tizen_base","id":"I28171720d5bbbf9eaf491cdafc0aee0b43f9cd06","number":361395,"subject":"cmake: use hybrid LLVM linkage on x86_64","owner":{"name":"Lin Hao","email":"hao.lin@samsung.com","username":"lhmax2025"},"url":"https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361395","hashtags":[],"createdOn":1794500787,"lastUpdated":1794500787,"open":true,"status":"NEW","currentPatchSet":{"number":1,"revision":"c5244e13258bb541458dcd4a08254217d7c556a9","parents":["13c3e223d9e1b35e4affb55255c5042f8c940f35"],"ref":"refs/changes/95/361395/1","uploader":{"name":"Lin Hao","email":"hao.lin@samsung.com","username":"lhmax2025"},"createdOn":1794500787,"author":{"name":"Lin Hao","email":"hao.lin@samsung.com","username":"lhmax2025"},"kind":"REWORK","sizeInsertions":163,"sizeDeletions":3}}
{"type":"stats","rowCount":1,"runTimeMilliseconds":1,"moreChanges":false}
~~~
### 2. Ic98eab90cc017f127a66e1729b44fab8b8e8fb41

第一次前置：

~~~json
{"type":"stats","rowCount":0,"runTimeMilliseconds":1,"moreChanges":false}
~~~

续跑上传前：

~~~json
{"type":"stats","rowCount":0,"runTimeMilliseconds":1,"moreChanges":false}
~~~

上传后：

~~~json
{"project":"platform/upstream/llvm","branch":"tizen_base","id":"Ic98eab90cc017f127a66e1729b44fab8b8e8fb41","number":361396,"subject":"packaging: optimize x86_64 clang with BOLT","owner":{"name":"Lin Hao","email":"hao.lin@samsung.com","username":"lhmax2025"},"url":"https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361396","hashtags":[],"createdOn":1794500787,"lastUpdated":1794500787,"open":true,"status":"NEW","currentPatchSet":{"number":1,"revision":"bde009d1197a09f7b7b76382a0166e03c841bdb9","parents":["c5244e13258bb541458dcd4a08254217d7c556a9"],"ref":"refs/changes/96/361396/1","uploader":{"name":"Lin Hao","email":"hao.lin@samsung.com","username":"lhmax2025"},"createdOn":1794500787,"author":{"name":"Lin Hao","email":"hao.lin@samsung.com","username":"lhmax2025"},"kind":"REWORK","sizeInsertions":2215,"sizeDeletions":0}}
{"type":"stats","rowCount":1,"runTimeMilliseconds":1,"moreChanges":false}
~~~
### 3. Ic76505ddb122f1e06271ff7462e24eceee4d400a

第一次前置：

~~~json
{"type":"stats","rowCount":0,"runTimeMilliseconds":0,"moreChanges":false}
~~~

续跑上传前：

~~~json
{"type":"stats","rowCount":0,"runTimeMilliseconds":1,"moreChanges":false}
~~~

上传后：

~~~json
{"project":"platform/upstream/llvm","branch":"tizen_base","id":"Ic76505ddb122f1e06271ff7462e24eceee4d400a","number":361397,"subject":"packaging: fix x86 LLVM flags and archive mode","owner":{"name":"Lin Hao","email":"hao.lin@samsung.com","username":"lhmax2025"},"url":"https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361397","hashtags":[],"createdOn":1794500787,"lastUpdated":1794500787,"open":true,"status":"NEW","currentPatchSet":{"number":1,"revision":"2cdd37ff747765e99c2befa3e6e8a88663ab77fe","parents":["bde009d1197a09f7b7b76382a0166e03c841bdb9"],"ref":"refs/changes/97/361397/1","uploader":{"name":"Lin Hao","email":"hao.lin@samsung.com","username":"lhmax2025"},"createdOn":1794500787,"author":{"name":"Lin Hao","email":"hao.lin@samsung.com","username":"lhmax2025"},"kind":"REWORK","sizeInsertions":488,"sizeDeletions":64}}
{"type":"stats","rowCount":1,"runTimeMilliseconds":2,"moreChanges":false}
~~~

## 5. 上传成功与依赖核对

上传命令（执行前已打印）：

~~~sh
git push ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm 2cdd37ff747765e99c2befa3e6e8a88663ab77fe:refs/for/tizen_base
~~~

远端原文（stdout为空，stderr如下）：

~~~text
remote: 
remote: Processing changes: refs: 1, new: 3        
remote: Processing changes: refs: 1, new: 3, done            
remote: 
remote: SUCCESS        
remote: 
remote:   https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361395 cmake: use hybrid LLVM linkage on x86_64 [NEW]        
remote:   https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361396 packaging: optimize x86_64 clang with BOLT [NEW]        
remote:   https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361397 packaging: fix x86 LLVM flags and archive mode [NEW]        
remote: 
To ssh://review.tizen.org:29418/platform/upstream/llvm
 * [new reference]             2cdd37ff747765e99c2befa3e6e8a88663ab77fe -> refs/for/tizen_base
~~~


|Change|Patch set|状态/分支|revision|
|---|---|---|---|
|[361395](https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361395)|1|NEW / tizen_base|c5244e13258bb541458dcd4a08254217d7c556a9|
|[361396](https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361396)|1|NEW / tizen_base|bde009d1197a09f7b7b76382a0166e03c841bdb9|
|[361397](https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361397)|1|NEW / tizen_base|2cdd37ff747765e99c2befa3e6e8a88663ab77fe|


依赖核对依据：query返回的三个当前revision与本地commit对象完全相同，parent依次为13c3e223、c5244e13、bde009d1。因此混合链接 ← BOLT ← 固定参数/转换器。[核对JSON](../../tools/bolt/results/gerrit-upload81-20261113/resume/post-query-summary.json)。

## 6. 上传后同步 sandbox

命令：

~~~sh
git push --force-with-lease=refs/heads/sandbox/lhmax2025/bolt_pgo:01c503a5158ecec8b6df5c338765f675f0d7bed4 ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm 2cdd37ff747765e99c2befa3e6e8a88663ab77fe:refs/heads/sandbox/lhmax2025/bolt_pgo
~~~

推送前 ls-remote：

~~~text
01c503a5158ecec8b6df5c338765f675f0d7bed4	refs/heads/sandbox/lhmax2025/bolt_pgo
~~~

推送输出：

~~~text
remote: 
remote: Processing changes: refs: 1        
remote: Processing changes: refs: 1, done            
To ssh://review.tizen.org:29418/platform/upstream/llvm
 + 01c503a5158e...2cdd37ff7477 2cdd37ff747765e99c2befa3e6e8a88663ab77fe -> sandbox/lhmax2025/bolt_pgo (forced update)
~~~

推送后 ls-remote：

~~~text
2cdd37ff747765e99c2befa3e6e8a88663ab77fe	refs/heads/sandbox/lhmax2025/bolt_pgo
~~~

先完成评审上传与三项查询核对，再执行本次sandbox推送。没有添加评审人/打分/提交合入。

## 7. v9 移动与 r8 交付

v9大小95367字节。移动前后SHA256均为 534ac688da10ee10f3905a0780ec71da2c57b5a3b24e5cdad50f1963e070b989。从 /home/linhao/Downloads/tizen_llvm_speed_design_v9.md **移动**到 /home/linhao/Toolchain/development/llvm-optimize-bolt/docs/bolt/design/tizen_llvm_speed_design_v9.md；目标事先不存在，移动后源文件不存在。[移动核对](../../tools/bolt/results/gerrit-upload81-20261113/resume/v9-move.json)；[设计v9](design/tizen_llvm_speed_design_v9.md)。

[r8 README](../../patches/rebase-359934-20261113-r8/README.md)及三个上传提交的完整format-patch；目录内只有这四个交付文件。三个补丁的代码正文与r7全部相同，git apply --numstat只读解析通过，未应用到源码。
|文件|字节|SHA256|
|---|---:|---|
|0001.patch|11168|295fcdc7b0d8a7c76d765108b1f58f29ff912de973a8f9687c8c775496de20e6|
|0002.patch|12685576|fb158b3b551b059656b9cb0b0d63ee5cae7b3aa7310e95ac36edfad941d040d5|
|0003.patch|45213|0266d046fc238707d4cb0513f36eba96156f5ce0d9027c563bd07b2488a31097|


## 8. 当前状态与后续规则

- 第一批已上传、评审中：361395、361396、361397，均PS1/NEW。
- 第七轮评审结论（用户提供）：两家都判可以上传，没有严重问题。
- 上传后跟进：入口子服务状态改为白名单及其他入口小项（下次使用入口之前完成）；产品加固补丁；claims文档补充PS10对照。
- 设计以v9为准。
- 新规则：以后推送新patch set时，必须先推refs/for，成功后再同步sandbox，不能先推sandbox。
- 本轮没有重新构建/运行QB/产品测试。代码树不变；沿用80号PM裁决及79号已记录的验证结论，不把它们写成本轮新运行。

## 9. 结束行原文

第一次停止：

~~~text
STEP4 已结束 2026-11-13T00:11:05.409475+08:00 status=FAIL
~~~

本次：

~~~text
STEP1 已结束 2026-11-13T00:21:25.122026+08:00 status=PASS
~~~

~~~text
STEP2 已结束 2026-11-13T00:25:45.730339+08:00 status=PASS
~~~

~~~text
STEP3 已结束 2026-11-13T00:26:00.766069+08:00 status=PASS
~~~

~~~text
STEP4 已结束 2026-11-13T00:26:20.554364+08:00 status=PASS
~~~

~~~text
STEP5 已结束 2026-11-13T00:26:42.876949+08:00 status=PASS
~~~

~~~text
STEP6 已结束 2026-11-13T00:26:52.004879+08:00 status=PASS
~~~

~~~text
STEP7 已结束 2026-11-13T00:28:46.368642+08:00 status=PASS
~~~
