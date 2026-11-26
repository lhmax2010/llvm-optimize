# 165 · 361624 PS7 定稿与上传

**PASS**。

P8 `de305f2c4de2721c7aeb5a677cd0ee32c3be505c`，tree `f10c60b808225b98464ab0109fc8e945da7fcb8c`，parent `f346dd75e87de324dc2abe61454ca1c49969d12d`。
Change-Id `Ie2c1d45cea6703a0caef72187397275a03e66468`。作者行与 PS6 逐字节相同。

## P7 → P8

产品差异仅为六个 shebang 的后置检查、两个包名声明位置的注释、独立 spec 末尾一个空行。
后置检查采用 Kimi 第 5 节精确路径循环及 Codex 第 5 节的 test 写法，保留原六条 sed。
注释依据 Claude Code 的 D3，用包名及较旧版本描述当前行为。正文以该评审第 7 节为基础，补充 MLGO 解压条件、两项历史撤回、build-id 的 _toolchain 限定和 shebang 检查。
[代码 diff](../../tools/bolt/results/task165-push/p7-to-p8.diff) · [说明 diff](../../tools/bolt/results/task165-push/p7-to-p8-message.diff) · [正文逐句核对](../../tools/bolt/results/task165-push/body-sentence-audit.md)

## 验证

Tizen RPM 4.14.1 对 x86_64、aarch64、armv7l 展开通过。独立包仍仅允许前两架构构建。
GBS 使用 154-B 的 clang、llvm、libllvm 及其依赖，确认 llvm-devel 未安装。
正例通过六个路径。反例替换 scan-view 首行为 #!/usr/bin/python，检查退出 1。

> Unexpected interpreter in usr/bin/scan-view

[正例原文](../../tools/bolt/results/task165-push/positive-original.txt) · [反例原文](../../tools/bolt/results/task165-push/negative-original.txt) · [完整 GBS 日志](../../tools/bolt/results/task165-push/gbs-build.txt) · [RPM 核对](../../tools/bolt/results/task165-push/static.json)

准备脚本修正了 Git 路径排序比较和 RPM 对 armv7l 展开的 BUILDROOT 后缀假设，产品内容相同。
[路径排序失败原文](../../tools/bolt/results/task165-push/preparation-first.txt) · [ARM 解析失败原文](../../tools/bolt/results/task165-push/preparation-arm-parser.txt)

首轮正反例均到达预期结果。测试 RPM 安装包含 BUILDROOT 路径的文本日志，触发 RPM 封包检查。复跑只改测试包的安装载荷，原始追踪留在构建日志。 [首轮日志](../../tools/bolt/results/task165-push/gbs-first-build.txt)

## PS7 推送

[stdout](../../tools/bolt/results/task165-push/ps7-push.stdout) · [stderr](../../tools/bolt/results/task165-push/ps7-push.stderr)

~~~text
remote: 
remote: Processing changes: refs: 1, updated: 1        
remote: Processing changes: refs: 1, updated: 1        
remote: Processing changes: refs: 1, updated: 1, done            
remote: commit de305f2: warning: subject >50 characters; use shorter first paragraph        
remote: 
remote: SUCCESS        
remote: 
remote:   https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361624 packaging: split tool subpackages into a standalone llvm-tools-subpkgs spec        
remote: 
remote: The following approvals got outdated and were removed:        
remote: * Code-Review+1 by Dongkyun Son        
remote: * Verified-1 by Dongkyun Son        
remote: 
remote: 
To ssh://review.tizen.org:29418/platform/upstream/llvm
 * [new reference]             de305f2c4de2721c7aeb5a677cd0ee32c3be505c -> refs/for/tizen_base
~~~

## 验证分支推送

[stdout](../../tools/bolt/results/task165-push/sandbox-push.stdout) · [stderr](../../tools/bolt/results/task165-push/sandbox-push.stderr)

~~~text
remote: 
remote: Processing changes: refs: 1        
remote: Processing changes: refs: 1, done            
To ssh://review.tizen.org:29418/platform/upstream/llvm
 * [new branch]                de305f2c4de2721c7aeb5a677cd0ee32c3be505c -> sandbox/lhmax2025/llvm-361624-ps7-20261126
~~~

## 评审意见发送

[stdout](../../tools/bolt/results/task165-push/comment.stdout) · [stderr](../../tools/bolt/results/task165-push/comment.stderr)

~~~text

~~~

验证分支 `sandbox/lhmax2025/llvm-361624-ps7-20261126` 指向同一 P8。 [ls-remote](../../tools/bolt/results/task165-push/sandbox-after.stdout)

[PS7 查询原文](../../tools/bolt/results/task165-push/ps7-after-push.stdout) · [PS7 ref 原文](../../tools/bolt/results/task165-push/ps7-change-ref.stdout)

PS7 评论核对 PASS，新增 1 条。逐字节一致：True，label 与其他评审元数据未变：True。
[原文](../../tools/bolt/results/task165-push/ps7-review-comment.txt) · [评论后查询](../../tools/bolt/results/task165-push/ps7-after-comment.stdout) · [核对回执](../../tools/bolt/results/task165-push/comment-verification.json)

