# 第8版交付包：已上传 Gerrit 的三个提交

新 HEAD：2cdd37ff747765e99c2befa3e6e8a88663ab77fe。三个评审已创建，sandbox/lhmax2025/bolt_pgo 已同步为同一 HEAD。

基线 13c3e223d9e1b35e4affb55255c5042f8c940f35（总部359934 PS10，已合入）。本轮 tizen_base 为61ef5d31ca91025c414c748477bef0c64ddfa67c，tree与基线相同，verdict B。

|序号|提交 SHA|tree SHA|标题|
|---|---|---|---|
|1|c5244e13258bb541458dcd4a08254217d7c556a9|3d961cbb04f5446f84d2089b4f65f3178f2bd7fa|cmake: use hybrid LLVM linkage on x86_64|
|2|bde009d1197a09f7b7b76382a0166e03c841bdb9|c23914776684bf94fdd5961f447f7c24e7bb79bc|packaging: optimize x86_64 clang with BOLT|
|3|2cdd37ff747765e99c2befa3e6e8a88663ab77fe|b2e8af2477cf623a945aa80bf8288a262dd4a5a9|packaging: fix x86 LLVM flags and archive mode|


|Change|Patch set|状态/分支|revision|
|---|---|---|---|
|[361395](https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361395)|1|NEW / tizen_base|c5244e13258bb541458dcd4a08254217d7c556a9|
|[361396](https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361396)|1|NEW / tizen_base|bde009d1197a09f7b7b76382a0166e03c841bdb9|
|[361397](https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361397)|1|NEW / tizen_base|2cdd37ff747765e99c2befa3e6e8a88663ab77fe|


依赖：混合链接 → BOLT → 固定参数/转换器。未加评审人、未打分、未提交合入。

相对 r7（4e80f54e），仅第三个说明的“For PIC”改为“For converted PIC members”，只重新折行所在段落。三棵树、作者及作者日期不变。第一次先推 sandbox 的链 01c503a5 被 Gerrit 以 no new changes 拒绝；本次保持三份说明和代码树不变，仅更新提交者时间并重建父链，先推 refs/for，查询通过后再同步 sandbox。

## 交付文件

目录只有三个完整 format-patch 和本 README；[PATCH 1/3] 至 [PATCH 3/3]。0002 携带完整 profile 的 Git binary patch 文本编码。三个补丁从首个 diff --git 到文件结尾与 r7 对应补丁逐字节相同；只读 git apply --numstat 解析通过。

|文件|字节|SHA256|
|---|---:|---|
|0001.patch|11168|295fcdc7b0d8a7c76d765108b1f58f29ff912de973a8f9687c8c775496de20e6|
|0002.patch|12685576|fb158b3b551b059656b9cb0b0d63ee5cae7b3aa7310e95ac36edfad941d040d5|
|0003.patch|45213|0266d046fc238707d4cb0513f36eba96156f5ce0d9027c563bd07b2488a31097|


## 验证依据

[81号原文与证据](../../docs/bolt/81_gerrit_upload.md)；[79号](../../docs/bolt/79_qb_1226850_1226851.md) B1–B6 最终 PASS（原始源码包 FAIL 保留，R2 归类 PASS）；[80号](../../docs/bolt/80_final_message_push.md) 的只改说明/树不变裁决继续适用。本轮未构建、未访问QB，没有产生新产品验证结论。

设计以 [v9](../../docs/bolt/design/tizen_llvm_speed_design_v9.md) 为准。后续上传新 patch set 必须先推 refs/for，成功后再同步 sandbox。
