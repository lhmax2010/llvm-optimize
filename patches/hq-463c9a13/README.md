# 总部 LLVM 463c9a13 评审材料

采集时间：2026-11-04T11:51:48.671921+08:00 至 2026-11-04T12:07:08.795237+08:00（Asia/Shanghai）。本包只记录取回、版本关系、文件差异与 cherry-pick 试探事实；没有构建、测试或取舍建议，也没有访问 QB。

## 1. 提交和 Gerrit 状态

- 项目：platform/upstream/llvm。
- 提交：`463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`；父提交：`cf4b6777d056131e2534ecb460c5575327d99646`。
- Gerrit：[change 359934](https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/359934)，目标分支 `tizen_base`，状态 **NEW**；当前 patch set 7，ref `refs/changes/34/359934/7`。
- 已存在的远端分支 `sandbox/dkson95/clang` 的tip精确等于463c9a13，证据为remote-heads.stdout；这与评审目标分支tizen_base是两回事。
- 标题：packaging: classify -feliminate-unused-debug-types and mirror recorded backend policy。
- owner / patch author：Dongkyun Son <dongkyun.s@samsung.com>。完整作者、提交者、日期和提交说明以 [show-stat.stdout](show-stat.stdout)、[commit-raw.stdout](commit-raw.stdout) 为准。
- 查询返回的当前打分：Verified 1 (Dongkyun Son), Code-Review 1 (Juitem JoonWoo Kim)。
- 评审意见含“Builds are verified on QB”及1216400、1216401链接。这是评审者原话，本任务没有读取QB验证该说法。

所有历史 patch set、打分、评审意见原文见 [gerrit-query.jsonl](gerrit-query.jsonl)。patch set 7 的行级/整组意见原文：

```text
Builds are verified on QB
- https://quickbuild.tizen.org/build/1216400
- https://quickbuild.tizen.org/build/1216401
```

首条查询即命中1条评审，因此未执行“查不到时”的替代查询。SSH 全程 BatchMode，无密码输入、凭据保存或认证设置改动。

## 2. 取回方式及范围

独立临时 clone：`/home/linhao/Toolchain/development/llvm-optimize/temp/hq-463c9a13/repo`。没有使用或修改 review-20261102/source、night-20261103 目录。完整远端地址：

```text
ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm
```

初始命令：

```sh
ssh -o BatchMode=yes -p 29418 lhmax2025@review.tizen.org gerrit query --format=JSON --current-patch-set --all-approvals --files --comments commit:463c9a133a6dfea9adf1e6c8e07ab705cbf2a587
GIT_SSH_COMMAND='ssh -o BatchMode=yes' git -c pack.threads=2 clone --no-checkout --filter=blob:none --single-branch --branch tizen_base ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm /home/linhao/Toolchain/development/llvm-optimize/temp/hq-463c9a13/repo
```

服务器返回 `warning: filtering not recognized by server, ignoring`，因此实际收取完整 tizen_base 历史。之后按完整URL fetch tizen_base、sandbox/lhmax2025/bolt_pgo 和指定 change ref，并额外按完整SHA fetch目标提交。9b8d74af首次尚未取回，rev-parse返回128（原文保留在resolve-9b8d74af.stderr），随后按完整SHA单独fetch，才执行双向祖先判定；未把缺对象当作exit1。命令、时间、返回码逐条见 [commands.json](commands.json)，stdout/stderr分别保存，不裁切。

临时 clone 使用 sparse checkout 仅展开 packaging 和仓库顶层文件，减少本地文件；历史与索引仍完整，祖先判定不使用浅历史。没有创建或推送任何远端分支。

## 3. 父链和祖先关系

采集时 `origin/tizen_base` HEAD 为 `f999bd406c0a70fe8107aa992164fe6945c5d46a`。父链的完整 first-parent SHA/parents 在 [parent-chain-complete.stdout](parent-chain-complete.stdout)；最近30层含完整提交说明见 [parent-chain-recent.stdout](parent-chain-recent.stdout)，自67619ec8后的提交与stat见 [parent-chain-since-67619ec8.stdout](parent-chain-since-67619ec8.stdout)。

|比较提交|完整SHA|该提交是463c9a13祖先|463c9a13是该提交祖先|
|---|---|---|---|
|refs/remotes/origin/tizen_base|`f999bd406c0a70fe8107aa992164fe6945c5d46a`|是 (exit0)|否 (exit1)|
|f999bd40|`f999bd406c0a70fe8107aa992164fe6945c5d46a`|是 (exit0)|否 (exit1)|
|9b8d74af|`9b8d74af825d3caab67f8ff7cbc19fcda8a7ad64`|否 (exit1)|否 (exit1)|
|67619ec8|`67619ec8bbbac7238a6cfc33a481ccfbcd12206f`|是 (exit0)|否 (exit1)|
|d4d6ca16|`d4d6ca16b55a9afcb64a30ebf634f340f968267b`|否 (exit1)|否 (exit1)|
|f2553114|`f2553114b05cbb022ff3ac062dbac284e1029df4`|否 (exit1)|否 (exit1)|
|9e39fa8a61392652bb28b75fc26216675bcad1d5|`9e39fa8a61392652bb28b75fc26216675bcad1d5`|否 (exit1)|否 (exit1)|

每个方向都实际执行 `git merge-base --is-ancestor`，原始退出码在commands.json，输出在ancestor-*.stdout/stderr。相关直接父链为 `67619ec8 → f999bd40 → cf4b6777 → 463c9a13`；我方为 `67619ec8 → d4d6ca16 → f2553114 → 9e39fa8a`。HQ父提交是9e39fa8a祖先：**否**。共同祖先原文：

```text
67619ec8bbbac7238a6cfc33a481ccfbcd12206f
```

`git branch -r --contains 463c9a13` 对已取回引用的原文：

```text
  gerrit/359934-7
```

此命令范围是本clone已取回的tizen_base、sandbox及Gerrit评审ref；Gerrit评审ref不等于已合入分支。远端全部heads的名称/SHA见 [remote-heads.stdout](remote-heads.stdout)，没有据此推断未取回分支历史的包含关系。Gerrit明确给出的目标分支是tizen_base，状态见§1。

## 4. 改动范围和三个版本

HQ此次只改 `packaging/llvm-static-archives-native.py`（20行增加、9行删除）。parent→HQ diff中的事实：

- 分类器新增识别 `-feliminate-unused-debug-types`、带操作数的 `--param` 和 `--param=`。
- `function-sections`、`data-sections`、`unique-section-names`、`addrsig` 的重放参数从记录的有效值生成 `-f` 或 `-fno-`；必须开启的检查仅保留后两项。
- DWARF检查从“列表必须非空且最后是-gdwarf-4”变为“列表非空时最后必须是-gdwarf-4”；返回值在列表为空时为None，后端只在该值存在时加入 `-g` 和DWARF选项。
- 没有修改本次提交中的spec、BOLT helper或CMake文件。

完整format-patch见 [463c9a13.patch](463c9a13.patch)，没有省略二进制或提交说明。

|我们的提交|HQ重叠文件|
|---|---|
|hybrid `d4d6ca16b55a9afcb64a30ebf634f340f968267b`|无|
|bolt `f2553114b05cbb022ff3ac062dbac284e1029df4`|无|
|flags `9e39fa8a61392652bb28b75fc26216675bcad1d5`|packaging/llvm-static-archives-native.py|

四个提交各自完整文件清单及集合交集见 [overlap.json](overlap.json)、files-*.stdout。

356627/356639的只读查询原文在 [archive-changes-query.jsonl](archive-changes-query.jsonl)：356627（67619ec8）为MERGED，涉及转换器和spec；356639为NEW，涉及spec。本包因此导出转换器，以及它在spec中的调用上下文；spec本身不是HQ此次改动文件。

|版本目录|提交|
|---|---|
|files/hq/|`463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|files/ours/|`9e39fa8a61392652bb28b75fc26216675bcad1d5`|
|files/parent/|`cf4b6777d056131e2534ecb460c5575327d99646`|

每个版本均包含 `packaging/llvm-static-archives-native.py` 和 `packaging/llvm.spec` 完整原文。`diffs/` 分别给出 parent→HQ、ours→HQ、parent→ours 的 `git diff --full-index`，每对各两个文件；parent→HQ的spec diff为空，表示该文件没有改动。

## 5. 合并试探

只在上述临时clone中基于9e39fa8a新建 `hq-463c9a13-probe`，即使HQ父提交不在我方祖先链中仍执行试探。实际命令：

```sh
git switch -c hq-463c9a13-probe 9e39fa8a61392652bb28b75fc26216675bcad1d5
git -c user.name='Hao Lin' -c user.email=hao.lin@samsung.com cherry-pick --no-commit 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587
git cherry-pick --abort
```

cherry-pick 返回 **1**；冲突文件：packaging/llvm-static-archives-native.py；冲突块 **2** 个。原始输出：

```text
Auto-merging packaging/llvm-static-archives-native.py
CONFLICT (content): Merge conflict in packaging/llvm-static-archives-native.py
error: could not apply 463c9a133a6d... packaging: classify -feliminate-unused-debug-types and mirror recorded backend policy
hint: after resolving the conflicts, mark the corrected paths
hint: with 'git add <paths>' or 'git rm <paths>'
```

git diff --stat 原文：

```text
 packaging/llvm-static-archives-native.py | Unmerged
 packaging/llvm-static-archives-native.py | 30 +++++++++++++++++++++++++-----
 1 file changed, 25 insertions(+), 5 deletions(-)
```

`--abort` 返回 **128**。abort后HEAD：

```text
9e39fa8a61392652bb28b75fc26216675bcad1d5
```

abort后 `git status --porcelain=v1` 原文（空表示干净）：

```text
UU packaging/llvm-static-archives-native.py
```

本次单提交 `--no-commit` 冲突后没有可供abort的cherry-pick/revert状态，abort原文为“error: no cherry-pick or revert in progress / fatal: cherry-pick failed”。为完成撤销，仅在此临时clone将唯一试探文件恢复到原HEAD：

```sh
git restore --source=9e39fa8a61392652bb28b75fc26216675bcad1d5 --staged --worktree -- packaging/llvm-static-archives-native.py
```

返回0，`final-trial-status.stdout`为空，`final-trial-head.stdout`仍为9e39fa8a；没有解析或合入冲突，也没有删除目录。abort失败和恢复命令均记录在commands.json。

完整冲突文件保存于conflicts/，含行号的每个冲突块见conflict-blocks.json；未合并索引、工作区diff和已暂存diff均保存。未生成试探提交，未推送该临时分支。应用结果只说明Git合并情况，不等于编译或运行验证。

## 6. 文件表与命令索引

`commands.json` 包含本clone内每条命令的完整argv、cwd、时间和退出码，`collect.py` 是采集过程。初始SSH与clone命令见§2；归档评审查询使用同一BatchMode SSH和 `project:platform/upstream/llvm (change:356627 OR change:356639)`。没有推送Gerrit或操作QB；此证据目录只提交到GitHub bolt-v4。

SHA256SUMS记录交付文件SHA256（不含自身）。以下stdout/stderr均为对应命令的原始字节；格式化的JSON是汇总或命令元数据，未替代原文。

|文件|用途|
|---|---|
|[463c9a13.patch](463c9a13.patch)|git format-patch -1 --stdout --full-index --binary 完整补丁|
|[after-abort-head.stderr](after-abort-head.stderr)|原始标准错误：`git -c pack.threads=2 rev-parse HEAD`|
|[after-abort-head.stdout](after-abort-head.stdout)|原始标准输出：`git -c pack.threads=2 rev-parse HEAD`|
|[after-abort-status.stderr](after-abort-status.stderr)|原始标准错误：`git -c pack.threads=2 status --porcelain=v1`|
|[after-abort-status.stdout](after-abort-status.stdout)|原始标准输出：`git -c pack.threads=2 status --porcelain=v1`|
|[ancestor-463c9a13-67619ec8.stderr](ancestor-463c9a13-67619ec8.stderr)|原始标准错误：`git -c pack.threads=2 merge-base --is-ancestor 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 67619ec8bbbac7238a6cfc33a481ccfbcd12206f`|
|[ancestor-463c9a13-67619ec8.stdout](ancestor-463c9a13-67619ec8.stdout)|原始标准输出：`git -c pack.threads=2 merge-base --is-ancestor 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 67619ec8bbbac7238a6cfc33a481ccfbcd12206f`|
|[ancestor-463c9a13-9b8d74af.stderr](ancestor-463c9a13-9b8d74af.stderr)|原始标准错误：`git -c pack.threads=2 merge-base --is-ancestor 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 9b8d74af825d3caab67f8ff7cbc19fcda8a7ad64`|
|[ancestor-463c9a13-9b8d74af.stdout](ancestor-463c9a13-9b8d74af.stdout)|原始标准输出：`git -c pack.threads=2 merge-base --is-ancestor 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 9b8d74af825d3caab67f8ff7cbc19fcda8a7ad64`|
|[ancestor-463c9a13-9e39fa8a.stderr](ancestor-463c9a13-9e39fa8a.stderr)|原始标准错误：`git -c pack.threads=2 merge-base --is-ancestor 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 9e39fa8a61392652bb28b75fc26216675bcad1d5`|
|[ancestor-463c9a13-9e39fa8a.stdout](ancestor-463c9a13-9e39fa8a.stdout)|原始标准输出：`git -c pack.threads=2 merge-base --is-ancestor 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 9e39fa8a61392652bb28b75fc26216675bcad1d5`|
|[ancestor-463c9a13-d4d6ca16.stderr](ancestor-463c9a13-d4d6ca16.stderr)|原始标准错误：`git -c pack.threads=2 merge-base --is-ancestor 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 d4d6ca16b55a9afcb64a30ebf634f340f968267b`|
|[ancestor-463c9a13-d4d6ca16.stdout](ancestor-463c9a13-d4d6ca16.stdout)|原始标准输出：`git -c pack.threads=2 merge-base --is-ancestor 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 d4d6ca16b55a9afcb64a30ebf634f340f968267b`|
|[ancestor-463c9a13-f2553114.stderr](ancestor-463c9a13-f2553114.stderr)|原始标准错误：`git -c pack.threads=2 merge-base --is-ancestor 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 f2553114b05cbb022ff3ac062dbac284e1029df4`|
|[ancestor-463c9a13-f2553114.stdout](ancestor-463c9a13-f2553114.stdout)|原始标准输出：`git -c pack.threads=2 merge-base --is-ancestor 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 f2553114b05cbb022ff3ac062dbac284e1029df4`|
|[ancestor-463c9a13-f999bd40-resume.stderr](ancestor-463c9a13-f999bd40-resume.stderr)|原始标准错误：`git -c pack.threads=2 merge-base --is-ancestor 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 f999bd406c0a70fe8107aa992164fe6945c5d46a`|
|[ancestor-463c9a13-f999bd40-resume.stdout](ancestor-463c9a13-f999bd40-resume.stdout)|原始标准输出：`git -c pack.threads=2 merge-base --is-ancestor 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 f999bd406c0a70fe8107aa992164fe6945c5d46a`|
|[ancestor-463c9a13-f999bd40.stderr](ancestor-463c9a13-f999bd40.stderr)|原始标准错误：`git -c pack.threads=2 merge-base --is-ancestor 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 f999bd406c0a70fe8107aa992164fe6945c5d46a`|
|[ancestor-463c9a13-f999bd40.stdout](ancestor-463c9a13-f999bd40.stdout)|原始标准输出：`git -c pack.threads=2 merge-base --is-ancestor 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 f999bd406c0a70fe8107aa992164fe6945c5d46a`|
|[ancestor-67619ec8-463c9a13.stderr](ancestor-67619ec8-463c9a13.stderr)|原始标准错误：`git -c pack.threads=2 merge-base --is-ancestor 67619ec8bbbac7238a6cfc33a481ccfbcd12206f 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[ancestor-67619ec8-463c9a13.stdout](ancestor-67619ec8-463c9a13.stdout)|原始标准输出：`git -c pack.threads=2 merge-base --is-ancestor 67619ec8bbbac7238a6cfc33a481ccfbcd12206f 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[ancestor-9b8d74af-463c9a13.stderr](ancestor-9b8d74af-463c9a13.stderr)|原始标准错误：`git -c pack.threads=2 merge-base --is-ancestor 9b8d74af825d3caab67f8ff7cbc19fcda8a7ad64 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[ancestor-9b8d74af-463c9a13.stdout](ancestor-9b8d74af-463c9a13.stdout)|原始标准输出：`git -c pack.threads=2 merge-base --is-ancestor 9b8d74af825d3caab67f8ff7cbc19fcda8a7ad64 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[ancestor-9e39fa8a-463c9a13.stderr](ancestor-9e39fa8a-463c9a13.stderr)|原始标准错误：`git -c pack.threads=2 merge-base --is-ancestor 9e39fa8a61392652bb28b75fc26216675bcad1d5 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[ancestor-9e39fa8a-463c9a13.stdout](ancestor-9e39fa8a-463c9a13.stdout)|原始标准输出：`git -c pack.threads=2 merge-base --is-ancestor 9e39fa8a61392652bb28b75fc26216675bcad1d5 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[ancestor-d4d6ca16-463c9a13.stderr](ancestor-d4d6ca16-463c9a13.stderr)|原始标准错误：`git -c pack.threads=2 merge-base --is-ancestor d4d6ca16b55a9afcb64a30ebf634f340f968267b 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[ancestor-d4d6ca16-463c9a13.stdout](ancestor-d4d6ca16-463c9a13.stdout)|原始标准输出：`git -c pack.threads=2 merge-base --is-ancestor d4d6ca16b55a9afcb64a30ebf634f340f968267b 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[ancestor-f2553114-463c9a13.stderr](ancestor-f2553114-463c9a13.stderr)|原始标准错误：`git -c pack.threads=2 merge-base --is-ancestor f2553114b05cbb022ff3ac062dbac284e1029df4 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[ancestor-f2553114-463c9a13.stdout](ancestor-f2553114-463c9a13.stdout)|原始标准输出：`git -c pack.threads=2 merge-base --is-ancestor f2553114b05cbb022ff3ac062dbac284e1029df4 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[ancestor-f999bd40-463c9a13-resume.stderr](ancestor-f999bd40-463c9a13-resume.stderr)|原始标准错误：`git -c pack.threads=2 merge-base --is-ancestor f999bd406c0a70fe8107aa992164fe6945c5d46a 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[ancestor-f999bd40-463c9a13-resume.stdout](ancestor-f999bd40-463c9a13-resume.stdout)|原始标准输出：`git -c pack.threads=2 merge-base --is-ancestor f999bd406c0a70fe8107aa992164fe6945c5d46a 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[ancestor-f999bd40-463c9a13.stderr](ancestor-f999bd40-463c9a13.stderr)|原始标准错误：`git -c pack.threads=2 merge-base --is-ancestor f999bd406c0a70fe8107aa992164fe6945c5d46a 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[ancestor-f999bd40-463c9a13.stdout](ancestor-f999bd40-463c9a13.stdout)|原始标准输出：`git -c pack.threads=2 merge-base --is-ancestor f999bd406c0a70fe8107aa992164fe6945c5d46a 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[archive-changes-query.exit-code](archive-changes-query.exit-code)|对应查询/clone的原始stdout、stderr或退出码|
|[archive-changes-query.jsonl](archive-changes-query.jsonl)|356627/356639的Gerrit查询原文|
|[archive-changes-query.stderr](archive-changes-query.stderr)|对应查询/clone的原始stdout、stderr或退出码|
|[branches-containing.stderr](branches-containing.stderr)|原始标准错误：`git -c pack.threads=2 branch -r --contains 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[branches-containing.stdout](branches-containing.stdout)|原始标准输出：`git -c pack.threads=2 branch -r --contains 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[cherry-pick-abort.stderr](cherry-pick-abort.stderr)|原始标准错误：`git -c pack.threads=2 cherry-pick --abort`|
|[cherry-pick-abort.stdout](cherry-pick-abort.stdout)|原始标准输出：`git -c pack.threads=2 cherry-pick --abort`|
|[cherry-pick.stderr](cherry-pick.stderr)|原始标准错误：`git -c pack.threads=2 -c user.name=Hao Lin -c user.email=hao.lin@samsung.com cherry-pick --no-commit 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[cherry-pick.stdout](cherry-pick.stdout)|原始标准输出：`git -c pack.threads=2 -c user.name=Hao Lin -c user.email=hao.lin@samsung.com cherry-pick --no-commit 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[clone.exit-code](clone.exit-code)|对应查询/clone的原始stdout、stderr或退出码|
|[clone.stderr](clone.stderr)|对应查询/clone的原始stdout、stderr或退出码|
|[clone.stdout](clone.stdout)|对应查询/clone的原始stdout、stderr或退出码|
|[collect.py](collect.py)|采集/试探脚本原文，仅操作独立clone和材料目录|
|[commands.json](commands.json)|后续命令、时间、返回码|
|[commit-raw.stderr](commit-raw.stderr)|原始标准错误：`git -c pack.threads=2 cat-file commit 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[commit-raw.stdout](commit-raw.stdout)|原始标准输出：`git -c pack.threads=2 cat-file commit 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[conflict-blocks.json](conflict-blocks.json)|冲突块完整原文及文件行号|
|[conflict-files.stderr](conflict-files.stderr)|原始标准错误：`git -c pack.threads=2 diff --name-only --diff-filter=U`|
|[conflict-files.stdout](conflict-files.stdout)|原始标准输出：`git -c pack.threads=2 diff --name-only --diff-filter=U`|
|[conflicts/packaging/llvm-static-archives-native.py](conflicts/packaging/llvm-static-archives-native.py)|试探时含冲突标记的完整文件，abort前保存|
|[diff-ours-hq-llvm-static-archives-native.py.stderr](diff-ours-hq-llvm-static-archives-native.py.stderr)|原始标准错误：`git -c pack.threads=2 diff --no-ext-diff --full-index 9e39fa8a61392652bb28b75fc26216675bcad1d5 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 -- packaging/llvm-static-archives-native.py`|
|[diff-ours-hq-llvm-static-archives-native.py.stdout](diff-ours-hq-llvm-static-archives-native.py.stdout)|原始标准输出：`git -c pack.threads=2 diff --no-ext-diff --full-index 9e39fa8a61392652bb28b75fc26216675bcad1d5 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 -- packaging/llvm-static-archives-native.py`|
|[diff-ours-hq-llvm.spec.stderr](diff-ours-hq-llvm.spec.stderr)|原始标准错误：`git -c pack.threads=2 diff --no-ext-diff --full-index 9e39fa8a61392652bb28b75fc26216675bcad1d5 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 -- packaging/llvm.spec`|
|[diff-ours-hq-llvm.spec.stdout](diff-ours-hq-llvm.spec.stdout)|原始标准输出：`git -c pack.threads=2 diff --no-ext-diff --full-index 9e39fa8a61392652bb28b75fc26216675bcad1d5 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 -- packaging/llvm.spec`|
|[diff-parent-hq-llvm-static-archives-native.py.stderr](diff-parent-hq-llvm-static-archives-native.py.stderr)|原始标准错误：`git -c pack.threads=2 diff --no-ext-diff --full-index cf4b6777d056131e2534ecb460c5575327d99646 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 -- packaging/llvm-static-archives-native.py`|
|[diff-parent-hq-llvm-static-archives-native.py.stdout](diff-parent-hq-llvm-static-archives-native.py.stdout)|原始标准输出：`git -c pack.threads=2 diff --no-ext-diff --full-index cf4b6777d056131e2534ecb460c5575327d99646 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 -- packaging/llvm-static-archives-native.py`|
|[diff-parent-hq-llvm.spec.stderr](diff-parent-hq-llvm.spec.stderr)|原始标准错误：`git -c pack.threads=2 diff --no-ext-diff --full-index cf4b6777d056131e2534ecb460c5575327d99646 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 -- packaging/llvm.spec`|
|[diff-parent-hq-llvm.spec.stdout](diff-parent-hq-llvm.spec.stdout)|原始标准输出：`git -c pack.threads=2 diff --no-ext-diff --full-index cf4b6777d056131e2534ecb460c5575327d99646 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 -- packaging/llvm.spec`|
|[diff-parent-ours-llvm-static-archives-native.py.stderr](diff-parent-ours-llvm-static-archives-native.py.stderr)|原始标准错误：`git -c pack.threads=2 diff --no-ext-diff --full-index cf4b6777d056131e2534ecb460c5575327d99646 9e39fa8a61392652bb28b75fc26216675bcad1d5 -- packaging/llvm-static-archives-native.py`|
|[diff-parent-ours-llvm-static-archives-native.py.stdout](diff-parent-ours-llvm-static-archives-native.py.stdout)|原始标准输出：`git -c pack.threads=2 diff --no-ext-diff --full-index cf4b6777d056131e2534ecb460c5575327d99646 9e39fa8a61392652bb28b75fc26216675bcad1d5 -- packaging/llvm-static-archives-native.py`|
|[diff-parent-ours-llvm.spec.stderr](diff-parent-ours-llvm.spec.stderr)|原始标准错误：`git -c pack.threads=2 diff --no-ext-diff --full-index cf4b6777d056131e2534ecb460c5575327d99646 9e39fa8a61392652bb28b75fc26216675bcad1d5 -- packaging/llvm.spec`|
|[diff-parent-ours-llvm.spec.stdout](diff-parent-ours-llvm.spec.stdout)|原始标准输出：`git -c pack.threads=2 diff --no-ext-diff --full-index cf4b6777d056131e2534ecb460c5575327d99646 9e39fa8a61392652bb28b75fc26216675bcad1d5 -- packaging/llvm.spec`|
|[diffs/ours-to-hq-llvm-static-archives-native.py.diff](diffs/ours-to-hq-llvm-static-archives-native.py.diff)|两版本完整文件diff，方向见文件名|
|[diffs/ours-to-hq-llvm.spec.diff](diffs/ours-to-hq-llvm.spec.diff)|两版本完整文件diff，方向见文件名|
|[diffs/parent-to-hq-llvm-static-archives-native.py.diff](diffs/parent-to-hq-llvm-static-archives-native.py.diff)|两版本完整文件diff，方向见文件名|
|[diffs/parent-to-hq-llvm.spec.diff](diffs/parent-to-hq-llvm.spec.diff)|两版本完整文件diff，方向见文件名|
|[diffs/parent-to-ours-llvm-static-archives-native.py.diff](diffs/parent-to-ours-llvm-static-archives-native.py.diff)|两版本完整文件diff，方向见文件名|
|[diffs/parent-to-ours-llvm.spec.diff](diffs/parent-to-ours-llvm.spec.diff)|两版本完整文件diff，方向见文件名|
|[fetch-9b8d74af.stderr](fetch-9b8d74af.stderr)|原始标准错误：`git -c pack.threads=2 fetch ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm 9b8d74af825d3caab67f8ff7cbc19fcda8a7ad64`|
|[fetch-9b8d74af.stdout](fetch-9b8d74af.stdout)|原始标准输出：`git -c pack.threads=2 fetch ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm 9b8d74af825d3caab67f8ff7cbc19fcda8a7ad64`|
|[fetch-commit.stderr](fetch-commit.stderr)|原始标准错误：`git -c pack.threads=2 fetch ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[fetch-commit.stdout](fetch-commit.stdout)|原始标准输出：`git -c pack.threads=2 fetch ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[fetch.stderr](fetch.stderr)|原始标准错误：`git -c pack.threads=2 fetch ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm refs/heads/tizen_base:refs/remotes/origin/tizen_base refs/heads/sandbox/lhmax2025/bolt_pgo:refs/remotes/origin/sandbox/lhmax2025/bolt_pgo refs/changes/34/359934/7:refs/remotes/gerrit/359934-7`|
|[fetch.stdout](fetch.stdout)|原始标准输出：`git -c pack.threads=2 fetch ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm refs/heads/tizen_base:refs/remotes/origin/tizen_base refs/heads/sandbox/lhmax2025/bolt_pgo:refs/remotes/origin/sandbox/lhmax2025/bolt_pgo refs/changes/34/359934/7:refs/remotes/gerrit/359934-7`|
|[files/hq/packaging/llvm-static-archives-native.py](files/hq/packaging/llvm-static-archives-native.py)|git show导出的完整源码原文，版本见§4|
|[files/hq/packaging/llvm.spec](files/hq/packaging/llvm.spec)|git show导出的完整源码原文，版本见§4|
|[files/ours/packaging/llvm-static-archives-native.py](files/ours/packaging/llvm-static-archives-native.py)|git show导出的完整源码原文，版本见§4|
|[files/ours/packaging/llvm.spec](files/ours/packaging/llvm.spec)|git show导出的完整源码原文，版本见§4|
|[files/parent/packaging/llvm-static-archives-native.py](files/parent/packaging/llvm-static-archives-native.py)|git show导出的完整源码原文，版本见§4|
|[files/parent/packaging/llvm.spec](files/parent/packaging/llvm.spec)|git show导出的完整源码原文，版本见§4|
|[files-bolt.stderr](files-bolt.stderr)|原始标准错误：`git -c pack.threads=2 diff-tree --no-commit-id --name-only -r f2553114`|
|[files-bolt.stdout](files-bolt.stdout)|原始标准输出：`git -c pack.threads=2 diff-tree --no-commit-id --name-only -r f2553114`|
|[files-flags.stderr](files-flags.stderr)|原始标准错误：`git -c pack.threads=2 diff-tree --no-commit-id --name-only -r 9e39fa8a61392652bb28b75fc26216675bcad1d5`|
|[files-flags.stdout](files-flags.stdout)|原始标准输出：`git -c pack.threads=2 diff-tree --no-commit-id --name-only -r 9e39fa8a61392652bb28b75fc26216675bcad1d5`|
|[files-hq.stderr](files-hq.stderr)|原始标准错误：`git -c pack.threads=2 diff-tree --no-commit-id --name-only -r 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[files-hq.stdout](files-hq.stdout)|原始标准输出：`git -c pack.threads=2 diff-tree --no-commit-id --name-only -r 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[files-hybrid.stderr](files-hybrid.stderr)|原始标准错误：`git -c pack.threads=2 diff-tree --no-commit-id --name-only -r d4d6ca16`|
|[files-hybrid.stdout](files-hybrid.stdout)|原始标准输出：`git -c pack.threads=2 diff-tree --no-commit-id --name-only -r d4d6ca16`|
|[final-trial-head.stderr](final-trial-head.stderr)|原始标准错误：`git rev-parse HEAD`|
|[final-trial-head.stdout](final-trial-head.stdout)|原始标准输出：`git rev-parse HEAD`|
|[final-trial-status.stderr](final-trial-status.stderr)|原始标准错误：`git status --porcelain=v1`|
|[final-trial-status.stdout](final-trial-status.stdout)|原始标准输出：`git status --porcelain=v1`|
|[format-patch.stderr](format-patch.stderr)|原始标准错误：`git -c pack.threads=2 format-patch -1 --stdout --full-index --binary 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[format-patch.stdout](format-patch.stdout)|原始标准输出：`git -c pack.threads=2 format-patch -1 --stdout --full-index --binary 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[gerrit-query.exit-code](gerrit-query.exit-code)|对应查询/clone的原始stdout、stderr或退出码|
|[gerrit-query.jsonl](gerrit-query.jsonl)|目标提交Gerrit查询原文，含评审、打分和历史patch sets|
|[gerrit-query.stderr](gerrit-query.stderr)|对应查询/clone的原始stdout、stderr或退出码|
|[git-version.stderr](git-version.stderr)|原始标准错误：`git --version`|
|[git-version.stdout](git-version.stdout)|原始标准输出：`git --version`|
|[hq-parent-in-ours.stderr](hq-parent-in-ours.stderr)|原始标准错误：`git -c pack.threads=2 merge-base --is-ancestor cf4b6777d056131e2534ecb460c5575327d99646 9e39fa8a61392652bb28b75fc26216675bcad1d5`|
|[hq-parent-in-ours.stdout](hq-parent-in-ours.stdout)|原始标准输出：`git -c pack.threads=2 merge-base --is-ancestor cf4b6777d056131e2534ecb460c5575327d99646 9e39fa8a61392652bb28b75fc26216675bcad1d5`|
|[is-shallow.stderr](is-shallow.stderr)|原始标准错误：`git rev-parse --is-shallow-repository`|
|[is-shallow.stdout](is-shallow.stdout)|原始标准输出：`git rev-parse --is-shallow-repository`|
|[merge-base-hq-ours.stderr](merge-base-hq-ours.stderr)|原始标准错误：`git -c pack.threads=2 merge-base 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 9e39fa8a61392652bb28b75fc26216675bcad1d5`|
|[merge-base-hq-ours.stdout](merge-base-hq-ours.stdout)|原始标准输出：`git -c pack.threads=2 merge-base 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587 9e39fa8a61392652bb28b75fc26216675bcad1d5`|
|[overlap.json](overlap.json)|各提交改动文件及交集|
|[parent-chain-complete.stderr](parent-chain-complete.stderr)|原始标准错误：`git -c pack.threads=2 rev-list --first-parent --parents 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[parent-chain-complete.stdout](parent-chain-complete.stdout)|原始标准输出：`git -c pack.threads=2 rev-list --first-parent --parents 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[parent-chain-recent.stderr](parent-chain-recent.stderr)|原始标准错误：`git -c pack.threads=2 log --first-parent --format=fuller -30 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[parent-chain-recent.stdout](parent-chain-recent.stdout)|原始标准输出：`git -c pack.threads=2 log --first-parent --format=fuller -30 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[parent-chain-since-67619ec8.stderr](parent-chain-since-67619ec8.stderr)|原始标准错误：`git -c pack.threads=2 log --format=fuller --stat 67619ec8..463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[parent-chain-since-67619ec8.stdout](parent-chain-since-67619ec8.stdout)|原始标准输出：`git -c pack.threads=2 log --format=fuller --stat 67619ec8..463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[parent-resume.stderr](parent-resume.stderr)|原始标准错误：`git -c pack.threads=2 rev-parse 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587^`|
|[parent-resume.stdout](parent-resume.stdout)|原始标准输出：`git -c pack.threads=2 rev-parse 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587^`|
|[parent.stderr](parent.stderr)|原始标准错误：`git -c pack.threads=2 rev-parse 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587^`|
|[parent.stdout](parent.stdout)|原始标准输出：`git -c pack.threads=2 rev-parse 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587^`|
|[refs.stderr](refs.stderr)|原始标准错误：`git -c pack.threads=2 show-ref`|
|[refs.stdout](refs.stdout)|原始标准输出：`git -c pack.threads=2 show-ref`|
|[remote-heads.stderr](remote-heads.stderr)|原始标准错误：`git -c pack.threads=2 ls-remote --heads ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm`|
|[remote-heads.stdout](remote-heads.stdout)|原始标准输出：`git -c pack.threads=2 ls-remote --heads ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm`|
|[resolve-67619ec8.stderr](resolve-67619ec8.stderr)|原始标准错误：`git -c pack.threads=2 rev-parse 67619ec8^{commit}`|
|[resolve-67619ec8.stdout](resolve-67619ec8.stdout)|原始标准输出：`git -c pack.threads=2 rev-parse 67619ec8^{commit}`|
|[resolve-9b8d74af-resume.stderr](resolve-9b8d74af-resume.stderr)|原始标准错误：`git -c pack.threads=2 rev-parse 9b8d74af^{commit}`|
|[resolve-9b8d74af-resume.stdout](resolve-9b8d74af-resume.stdout)|原始标准输出：`git -c pack.threads=2 rev-parse 9b8d74af^{commit}`|
|[resolve-9b8d74af.stderr](resolve-9b8d74af.stderr)|原始标准错误：`git -c pack.threads=2 rev-parse 9b8d74af^{commit}`|
|[resolve-9b8d74af.stdout](resolve-9b8d74af.stdout)|原始标准输出：`git -c pack.threads=2 rev-parse 9b8d74af^{commit}`|
|[resolve-9e39fa8a61392652bb28b75fc26216675bcad1d5.stderr](resolve-9e39fa8a61392652bb28b75fc26216675bcad1d5.stderr)|原始标准错误：`git -c pack.threads=2 rev-parse 9e39fa8a61392652bb28b75fc26216675bcad1d5^{commit}`|
|[resolve-9e39fa8a61392652bb28b75fc26216675bcad1d5.stdout](resolve-9e39fa8a61392652bb28b75fc26216675bcad1d5.stdout)|原始标准输出：`git -c pack.threads=2 rev-parse 9e39fa8a61392652bb28b75fc26216675bcad1d5^{commit}`|
|[resolve-d4d6ca16.stderr](resolve-d4d6ca16.stderr)|原始标准错误：`git -c pack.threads=2 rev-parse d4d6ca16^{commit}`|
|[resolve-d4d6ca16.stdout](resolve-d4d6ca16.stdout)|原始标准输出：`git -c pack.threads=2 rev-parse d4d6ca16^{commit}`|
|[resolve-f2553114.stderr](resolve-f2553114.stderr)|原始标准错误：`git -c pack.threads=2 rev-parse f2553114^{commit}`|
|[resolve-f2553114.stdout](resolve-f2553114.stdout)|原始标准输出：`git -c pack.threads=2 rev-parse f2553114^{commit}`|
|[resolve-f999bd40-resume.stderr](resolve-f999bd40-resume.stderr)|原始标准错误：`git -c pack.threads=2 rev-parse f999bd40^{commit}`|
|[resolve-f999bd40-resume.stdout](resolve-f999bd40-resume.stdout)|原始标准输出：`git -c pack.threads=2 rev-parse f999bd40^{commit}`|
|[resolve-f999bd40.stderr](resolve-f999bd40.stderr)|原始标准错误：`git -c pack.threads=2 rev-parse f999bd40^{commit}`|
|[resolve-f999bd40.stdout](resolve-f999bd40.stdout)|原始标准输出：`git -c pack.threads=2 rev-parse f999bd40^{commit}`|
|[resolve-tizen_base-resume.stderr](resolve-tizen_base-resume.stderr)|原始标准错误：`git -c pack.threads=2 rev-parse refs/remotes/origin/tizen_base^{commit}`|
|[resolve-tizen_base-resume.stdout](resolve-tizen_base-resume.stdout)|原始标准输出：`git -c pack.threads=2 rev-parse refs/remotes/origin/tizen_base^{commit}`|
|[resolve-tizen_base.stderr](resolve-tizen_base.stderr)|原始标准错误：`git -c pack.threads=2 rev-parse refs/remotes/origin/tizen_base^{commit}`|
|[resolve-tizen_base.stdout](resolve-tizen_base.stdout)|原始标准输出：`git -c pack.threads=2 rev-parse refs/remotes/origin/tizen_base^{commit}`|
|[resume.py](resume.py)|补取9b8d74af后续采集和试探脚本；首轮失败原文保留|
|[show-hq-llvm-static-archives-native.py.stderr](show-hq-llvm-static-archives-native.py.stderr)|原始标准错误：`git -c pack.threads=2 show 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587:packaging/llvm-static-archives-native.py`|
|[show-hq-llvm-static-archives-native.py.stdout](show-hq-llvm-static-archives-native.py.stdout)|原始标准输出：`git -c pack.threads=2 show 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587:packaging/llvm-static-archives-native.py`|
|[show-hq-llvm.spec.stderr](show-hq-llvm.spec.stderr)|原始标准错误：`git -c pack.threads=2 show 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587:packaging/llvm.spec`|
|[show-hq-llvm.spec.stdout](show-hq-llvm.spec.stdout)|原始标准输出：`git -c pack.threads=2 show 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587:packaging/llvm.spec`|
|[show-ours-llvm-static-archives-native.py.stderr](show-ours-llvm-static-archives-native.py.stderr)|原始标准错误：`git -c pack.threads=2 show 9e39fa8a61392652bb28b75fc26216675bcad1d5:packaging/llvm-static-archives-native.py`|
|[show-ours-llvm-static-archives-native.py.stdout](show-ours-llvm-static-archives-native.py.stdout)|原始标准输出：`git -c pack.threads=2 show 9e39fa8a61392652bb28b75fc26216675bcad1d5:packaging/llvm-static-archives-native.py`|
|[show-ours-llvm.spec.stderr](show-ours-llvm.spec.stderr)|原始标准错误：`git -c pack.threads=2 show 9e39fa8a61392652bb28b75fc26216675bcad1d5:packaging/llvm.spec`|
|[show-ours-llvm.spec.stdout](show-ours-llvm.spec.stdout)|原始标准输出：`git -c pack.threads=2 show 9e39fa8a61392652bb28b75fc26216675bcad1d5:packaging/llvm.spec`|
|[show-parent-llvm-static-archives-native.py.stderr](show-parent-llvm-static-archives-native.py.stderr)|原始标准错误：`git -c pack.threads=2 show cf4b6777d056131e2534ecb460c5575327d99646:packaging/llvm-static-archives-native.py`|
|[show-parent-llvm-static-archives-native.py.stdout](show-parent-llvm-static-archives-native.py.stdout)|原始标准输出：`git -c pack.threads=2 show cf4b6777d056131e2534ecb460c5575327d99646:packaging/llvm-static-archives-native.py`|
|[show-parent-llvm.spec.stderr](show-parent-llvm.spec.stderr)|原始标准错误：`git -c pack.threads=2 show cf4b6777d056131e2534ecb460c5575327d99646:packaging/llvm.spec`|
|[show-parent-llvm.spec.stdout](show-parent-llvm.spec.stdout)|原始标准输出：`git -c pack.threads=2 show cf4b6777d056131e2534ecb460c5575327d99646:packaging/llvm.spec`|
|[show-stat.stderr](show-stat.stderr)|原始标准错误：`git -c pack.threads=2 show --stat --format=fuller 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[show-stat.stdout](show-stat.stdout)|原始标准输出：`git -c pack.threads=2 show --stat --format=fuller 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587`|
|[sparse-init.stderr](sparse-init.stderr)|原始标准错误：`git -c pack.threads=2 sparse-checkout init --cone`|
|[sparse-init.stdout](sparse-init.stdout)|原始标准输出：`git -c pack.threads=2 sparse-checkout init --cone`|
|[sparse-packaging.stderr](sparse-packaging.stderr)|原始标准错误：`git -c pack.threads=2 sparse-checkout set packaging`|
|[sparse-packaging.stdout](sparse-packaging.stdout)|原始标准输出：`git -c pack.threads=2 sparse-checkout set packaging`|
|[summary.json](summary.json)|版本、祖先、试探与abort结果结构化汇总|
|[tizen-base-head-resume.stderr](tizen-base-head-resume.stderr)|原始标准错误：`git -c pack.threads=2 rev-parse refs/remotes/origin/tizen_base`|
|[tizen-base-head-resume.stdout](tizen-base-head-resume.stdout)|原始标准输出：`git -c pack.threads=2 rev-parse refs/remotes/origin/tizen_base`|
|[tizen-base-head.stderr](tizen-base-head.stderr)|原始标准错误：`git -c pack.threads=2 rev-parse refs/remotes/origin/tizen_base`|
|[tizen-base-head.stdout](tizen-base-head.stdout)|原始标准输出：`git -c pack.threads=2 rev-parse refs/remotes/origin/tizen_base`|
|[trial-before.stderr](trial-before.stderr)|原始标准错误：`git -c pack.threads=2 status --porcelain=v1`|
|[trial-before.stdout](trial-before.stdout)|原始标准输出：`git -c pack.threads=2 status --porcelain=v1`|
|[trial-branch.stderr](trial-branch.stderr)|原始标准错误：`git -c pack.threads=2 switch -c hq-463c9a13-probe 9e39fa8a61392652bb28b75fc26216675bcad1d5`|
|[trial-branch.stdout](trial-branch.stdout)|原始标准输出：`git -c pack.threads=2 switch -c hq-463c9a13-probe 9e39fa8a61392652bb28b75fc26216675bcad1d5`|
|[trial-cached-diff.stderr](trial-cached-diff.stderr)|原始标准错误：`git -c pack.threads=2 diff --cached --no-ext-diff`|
|[trial-cached-diff.stdout](trial-cached-diff.stdout)|原始标准输出：`git -c pack.threads=2 diff --cached --no-ext-diff`|
|[trial-cached-stat.stderr](trial-cached-stat.stderr)|原始标准错误：`git -c pack.threads=2 diff --cached --stat`|
|[trial-cached-stat.stdout](trial-cached-stat.stdout)|原始标准输出：`git -c pack.threads=2 diff --cached --stat`|
|[trial-diff-stat.stderr](trial-diff-stat.stderr)|原始标准错误：`git -c pack.threads=2 diff --stat`|
|[trial-diff-stat.stdout](trial-diff-stat.stdout)|原始标准输出：`git -c pack.threads=2 diff --stat`|
|[trial-diff.stderr](trial-diff.stderr)|原始标准错误：`git -c pack.threads=2 diff --no-ext-diff`|
|[trial-diff.stdout](trial-diff.stdout)|原始标准输出：`git -c pack.threads=2 diff --no-ext-diff`|
|[trial-restore-after-abort-error.stderr](trial-restore-after-abort-error.stderr)|原始标准错误：`git restore --source=9e39fa8a61392652bb28b75fc26216675bcad1d5 --staged --worktree -- packaging/llvm-static-archives-native.py`|
|[trial-restore-after-abort-error.stdout](trial-restore-after-abort-error.stdout)|原始标准输出：`git restore --source=9e39fa8a61392652bb28b75fc26216675bcad1d5 --staged --worktree -- packaging/llvm-static-archives-native.py`|
|[trial-status.stderr](trial-status.stderr)|原始标准错误：`git -c pack.threads=2 status --porcelain=v1`|
|[trial-status.stdout](trial-status.stdout)|原始标准输出：`git -c pack.threads=2 status --porcelain=v1`|
|[unmerged-index.stderr](unmerged-index.stderr)|原始标准错误：`git -c pack.threads=2 ls-files -u`|
|[unmerged-index.stdout](unmerged-index.stdout)|原始标准输出：`git -c pack.threads=2 ls-files -u`|
|[write-readme.py](write-readme.py)|README生成脚本|
|[README.md](README.md)|材料说明、命令和事实汇总|
|[SHA256SUMS](SHA256SUMS)|文件校验清单|
