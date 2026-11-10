# 76. r5 sandbox 推送与 ARM 基线候选

sandbox 已由 fa4f9978 更新为 **60fabc723f30c5cc04146a9dd83487ebed63f259**，指定 lease 推送一次成功，推后 ls-remote 相同。359934 仍 NEW / PS10，357163 仍 NEW / PS2。已找到两组可用的同快照、无混合链接 ARM 基线：**QB 1216401（Toolchain）和 QB 1216400（Base-Dev）**。

## 1. 范围与推送前核对

先读取 STATUS 和 [75 号 §6](75_fourth_review_fixes.md#6-续跑2026-11-10)。所有命令串行在独立 systemd 用户服务中运行，MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、Nice=19、IOSchedulingClass=idle；未 OOM。只有本任务授权的 sandbox 分支被写入；未创建分支，未推 refs/for，未构建、未操作 QB，未删除文件，未修改源码、远端配置或 VS Code 配置。Gerrit 全部显式 SSH BatchMode；QB 登录只在有界面 Chromium 中手动完成，没有导出 cookie、认证头、密码或登录表单。

源码目录：W/temp/rebase-359934-20261106/source，工作树干净，HEAD 为 60fabc723f30c5cc04146a9dd83487ebed63f259。[空 status 原文](../../tools/bolt/results/sandbox-r5-20261110/source-status.txt)。

|提交|SHA|tree|
|---|---|---|
|混合链接|8a50d7122346258fd1171d270861a4ae28a8717c|3d961cbb04f5446f84d2089b4f65f3178f2bd7fa|
|BOLT|358615447c2596c30aa6d064fc8c388292e443e4|9e4948eba61ca48156f5b4534f49adaf0f47cab1|
|固定参数/转换器|60fabc723f30c5cc04146a9dd83487ebed63f259|90fc87dde4d11c8c57f5d3de45a9995dcc35d5f9|

三提交及 tree 与 75 号 §6.1 完全一致；三提交下方基线为 13c3e223，接着是 cf4b6777。按 1/3、2/3、3/3 重新导出后，分别比较 r5 的补丁正文及提交说明；仅排除 format-patch 首行和 Date，三个补丁均相同。[逐项结果](../../tools/bolt/results/sandbox-r5-20261110/patch-precheck.json)、[完整前置结果](../../tools/bolt/results/sandbox-r5-20261110/precheck.json)。

推前 ls-remote：

~~~text
fa4f9978c9162d3c6cd2113d0cfe1173f04881c8	refs/heads/sandbox/lhmax2025/bolt_pgo
~~~

查询命令（359934、357163 各执行一次，保存全部 patch set、评论和审批）：

~~~sh
ssh -o BatchMode=yes -p 29418 lhmax2025@review.tizen.org gerrit query --format=JSON --current-patch-set --patch-sets --comments --all-approvals change:359934
ssh -o BatchMode=yes -p 29418 lhmax2025@review.tizen.org gerrit query --format=JSON --current-patch-set --patch-sets --comments --all-approvals change:357163
~~~

|Change|推前状态|当前 patch set|revision|
|---|---|---:|---|
|359934|NEW|10|13c3e223d9e1b35e4affb55255c5042f8c940f35|
|357163|NEW|2|cf4b6777d056131e2534ecb460c5575327d99646|

原文：[359934](../../tools/bolt/results/sandbox-r5-20261110/359934-before.jsonl)、[357163](../../tools/bolt/results/sandbox-r5-20261110/357163-before.jsonl)。所有指定前置条件通过后才推送。

## 2. 唯一一次 sandbox 推送及推后核对

在源码目录执行，环境设置 GIT_SSH_COMMAND='ssh -o BatchMode=yes'、GIT_TERMINAL_PROMPT=0，推送命令原样如下，没有重试：

~~~sh
git push --force-with-lease=refs/heads/sandbox/lhmax2025/bolt_pgo:fa4f9978c9162d3c6cd2113d0cfe1173f04881c8 ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm 60fabc723f30c5cc04146a9dd83487ebed63f259:refs/heads/sandbox/lhmax2025/bolt_pgo
~~~

退出码为 0，stdout/stderr 原文：

~~~text
remote: 
remote: Processing changes: refs: 1        
remote: Processing changes: refs: 1, done            
To ssh://review.tizen.org:29418/platform/upstream/llvm
 + fa4f9978c916...60fabc723f30 60fabc723f30c5cc04146a9dd83487ebed63f259 -> sandbox/lhmax2025/bolt_pgo (forced update)
~~~

[命令](../../tools/bolt/results/sandbox-r5-20261110/push-command.txt)、[stdout](../../tools/bolt/results/sandbox-r5-20261110/push.stdout)、[stderr](../../tools/bolt/results/sandbox-r5-20261110/push.stderr)、[退出码](../../tools/bolt/results/sandbox-r5-20261110/push-exit.txt)。

推后用同一完整 URL 执行 ls-remote：

~~~text
60fabc723f30c5cc04146a9dd83487ebed63f259	refs/heads/sandbox/lhmax2025/bolt_pgo
~~~

[推前原文](../../tools/bolt/results/sandbox-r5-20261110/ls-remote-before.stdout)、[推后原文](../../tools/bolt/results/sandbox-r5-20261110/ls-remote-after.stdout)。推后本地父链（第一列 SHA，第二列 tree）：

~~~text
60fabc723f30c5cc04146a9dd83487ebed63f259 90fc87dde4d11c8c57f5d3de45a9995dcc35d5f9 packaging: fix x86 LLVM flags and archive mode
358615447c2596c30aa6d064fc8c388292e443e4 9e4948eba61ca48156f5b4534f49adaf0f47cab1 packaging: optimize x86_64 clang with BOLT
8a50d7122346258fd1171d270861a4ae28a8717c 3d961cbb04f5446f84d2089b4f65f3178f2bd7fa cmake: use hybrid LLVM linkage on x86_64
13c3e223d9e1b35e4affb55255c5042f8c940f35 087e06cf9c79c571c711af8a07057496940ae73d packaging: classify -feliminate-unused-debug-types and mirror recorded backend policy
cf4b6777d056131e2534ecb460c5575327d99646 7b49745738b5512fbbed890e67e6a3861e1e39a5 Revert "Revert clang bootstrap + ThinLTO, fall back to GCC"
~~~

~~~text
PUSH_VERIFY PASS
SERVICE 已结束 2026-11-10T23:03:15+08:00 status=0 unit=llvm-r5-push-1110-003
~~~

再次只读查询两 change，仍为 **359934 NEW / PS10 / 13c3e223；357163 NEW / PS2 / cf4b6777**，未被 sandbox 推送关闭。[推后查询摘要](../../tools/bolt/results/sandbox-r5-20261110/post-query.json)、[359934 原文](../../tools/bolt/results/sandbox-r5-20261110/359934-after.jsonl)、[357163 原文](../../tools/bolt/results/sandbox-r5-20261110/357163-after.jsonl)。

## 3. 全部评论中的候选与源码证据

359934 PS7 的行内评论原文：

~~~text
Builds are verified on QB
- https://quickbuild.tizen.org/build/1216400
- https://quickbuild.tizen.org/build/1216401
~~~

该评论位于查询 JSON 的 patchSets[6].comments[0]；不能只搜索顶层 comments。357163 全部评论没有 QB 链接。其余评论中有关 1214821、1215143 的文字是历史问题/我们的方案背景，含占位文字 <QB link>，不是新的可验证基线链接。[递归检索结果](../../tools/bolt/results/sandbox-r5-20261110/all-comment-links.json)。75 号所列 QB 1214821 是历史候选，上一轮公开 RPM 地址 404；本次两个可访问候选取代该缺口，不把 1214821 记为当前可用。

两个候选的概览 Build Package List 均为：

~~~text
platform/upstream/llvm@463c9a133a6dfea9adf1e6c8e07ab705cbf2a587
~~~

两份公开 manifest 均只有一个 platform/upstream/llvm 条目，revision 同样为上述 PS7 SHA；概览与 manifest 双重确认。源码对象相对无混合链接基线 67619ec8 的完整 tree diff 只有转换器：

~~~text
packaging/llvm-static-archives-native.py | 29 ++++++++++++++++++++---------
 1 file changed, 20 insertions(+), 9 deletions(-)
~~~

因此 spec、六个 CMake 文件及其他源码均与无混合链接基线一致；所构建的源码不含我们的混合链接实现。463c9a13 的直接父提交为 cf4b6777。[源码内容证明](../../tools/bolt/results/sandbox-r5-20261110/candidate-source.json)、[六个提交的父链与说明](../../tools/bolt/results/sandbox-r5-20261110/candidate-source-chain.txt)。

额外的 git merge-base 全历史祖先遍历约 13 分钟无结果，已中断，结果记 UNKNOWN；当时尚未访问 ARM 产物目录，未 OOM。确认原服务 inactive/dead 后才执行有界的后续查询。这个额外祖先遍历不作为通过依据；“不含混合链接”由全 tree 文件差异和已确认的源码身份直接证明。原查询脚本、已产生的结果全部保留，未更改源码或放宽四项条件。[中断记录](../../tools/bolt/results/sandbox-r5-20261110/interrupted-query.txt)、[后续有界查询脚本](../../tools/bolt/results/sandbox-r5-20261110/check_candidates_bounded.py)。

## 4. ARM 基线候选表

候选必须同时满足：源码无混合链接、输入快照一致、ARM 产物仍可下载、构建记录可确认源码身份。这里的快照是 **Profile URL 的输入快照**，与输出产物目录的日期区分。

|QB|项目|源码/patch set|输入快照|ARM 公开目录|判定及原因|
|---|---|---|---|---|---|
|[1216400](https://quickbuild.tizen.org/build/1216400)|Tizen-Base-Dev|463c9a13（359934 PS7）|tizen-base-dev_20261030.061217|[armv7l](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Dev/tizen-base-dev_20261103.083743/repos/standard/packages/armv7l/) HTTP 200 / [aarch64](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Dev/tizen-base-dev_20261103.083743/repos/standard/packages/aarch64/) HTTP 200|可用：四条件全部满足|
|[1216401](https://quickbuild.tizen.org/build/1216401)|Tizen-Base-Toolchain|463c9a13（359934 PS7）|tizen-base-toolchain_20261030.061318|[armv7l](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261103.084003/repos/standard/packages/armv7l/) HTTP 200 / [aarch64](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261103.084003/repos/standard/packages/aarch64/) HTTP 200|可用：四条件全部满足|

- 1216400：Base-Dev 对应 1223602；输入 tizen-base-dev_20261030.061217，输出 tizen-base-dev_20261103.083743。子构建 1216403 覆盖 armv7l:aarch64:x86_64，状态 SUCCESSFUL；总耗时 4h55m13s。
- 1216401：Toolchain 对应 1223601；输入 tizen-base-toolchain_20261030.061318，输出 tizen-base-toolchain_20261103.084003。子构建 1216404 覆盖 armv7l:aarch64:x86_64，状态 SUCCESSFUL；总耗时 7h7m24s。

[1216400 概览](../../tools/bolt/results/sandbox-r5-20261110/1216400/overview.txt)、[manifest](../../tools/bolt/results/sandbox-r5-20261110/1216400/manifest.xml)；[1216401 概览](../../tools/bolt/results/sandbox-r5-20261110/1216401/overview.txt)、[manifest](../../tools/bolt/results/sandbox-r5-20261110/1216401/manifest.xml)。

公开访问仅 GET 小型 manifest/目录列表，以及 HEAD RPM；**没有下载 RPM，也没有做包内容比较**。四个目录及下面八个 RPM 的 HEAD 均 HTTP 200，Content-Type 为 application/x-redhat-package-manager，未重定向到登录页面。记录时间为 2026-11-10T23:23:48 至 23:24:02+08:00。

|QB|架构|RPM（仅 HEAD）|HTTP|Content-Length|
|---|---|---|---:|---:|
|1216400|armv7l|[clang-22.1.8-5.1.armv7l.rpm](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Dev/tizen-base-dev_20261103.083743/repos/standard/packages/armv7l/clang-22.1.8-5.1.armv7l.rpm)|200|192229577|
|1216400|armv7l|[llvm-devel-22.1.8-5.1.armv7l.rpm](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Dev/tizen-base-dev_20261103.083743/repos/standard/packages/armv7l/llvm-devel-22.1.8-5.1.armv7l.rpm)|200|22902413|
|1216400|aarch64|[clang-22.1.8-5.1.aarch64.rpm](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Dev/tizen-base-dev_20261103.083743/repos/standard/packages/aarch64/clang-22.1.8-5.1.aarch64.rpm)|200|301039741|
|1216400|aarch64|[llvm-devel-22.1.8-5.1.aarch64.rpm](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Dev/tizen-base-dev_20261103.083743/repos/standard/packages/aarch64/llvm-devel-22.1.8-5.1.aarch64.rpm)|200|36109837|
|1216401|armv7l|[clang-22.1.8-2.1.armv7l.rpm](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261103.084003/repos/standard/packages/armv7l/clang-22.1.8-2.1.armv7l.rpm)|200|21195269|
|1216401|armv7l|[llvm-devel-22.1.8-2.1.armv7l.rpm](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261103.084003/repos/standard/packages/armv7l/llvm-devel-22.1.8-2.1.armv7l.rpm)|200|5290109|
|1216401|aarch64|[clang-22.1.8-2.1.aarch64.rpm](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261103.084003/repos/standard/packages/aarch64/clang-22.1.8-2.1.aarch64.rpm)|200|29465601|
|1216401|aarch64|[llvm-devel-22.1.8-2.1.aarch64.rpm](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261103.084003/repos/standard/packages/aarch64/llvm-devel-22.1.8-2.1.aarch64.rpm)|200|5323793|

[全部请求结果及四条件判定](../../tools/bolt/results/sandbox-r5-20261110/arm-candidates.json)。可用性以本次访问为准，未来公开快照保留策略可能变化；本轮没有计算 RPM 内容 SHA。

~~~text
QB_CANDIDATES 已结束 2026-11-10T23:09:21.971390+08:00 status=ok
ARM_CANDIDATES 已结束 2026-11-10T23:24:02.955483+08:00 status=ok
~~~

## 5. 当前状态与下一步

sandbox/lhmax2025/bolt_pgo 已为 60fabc723f30c5cc04146a9dd83487ebed63f259。下一步依次为：**用户启动两个项目的 QB → 夜间完整构建（fa4f9978，74 号）→ QB 核对 → 三家完整评审（设计 v6.1 + r5 代码）**。本轮不启动这些步骤。

ARM 基线已找到：Toolchain 使用 QB 1216401，Base-Dev 使用 QB 1216400。这个结论是基线候选可用，不表示已经完成 ARM 产物逐字节比较。

R5_SANDBOX 已结束 2026-11-10T23:26:22+08:00 status=ok
