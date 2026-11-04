from pathlib import Path
import json,datetime,hashlib
E=Path(__file__).parent
s=json.loads((E/'summary.json').read_text());ov=json.loads((E/'overlap.json').read_text());cmds=json.loads((E/'commands.json').read_text());q=next(json.loads(l) for l in (E/'gerrit-query.jsonl').read_text().splitlines() if '"project"' in l)
def fence(t):return '\n```text\n'+t.rstrip()+'\n```\n'
def read(n):return (E/n).read_text()
text=f'''# 总部 LLVM 463c9a13 评审材料

采集时间：{datetime.datetime.fromtimestamp((E/'gerrit-query.jsonl').stat().st_mtime).astimezone().isoformat()} 至 {cmds[-1]['end']}（Asia/Shanghai）。本包只记录取回、版本关系、文件差异与 cherry-pick 试探事实；没有构建、测试或取舍建议，也没有访问 QB。

## 1. 提交和 Gerrit 状态

- 项目：platform/upstream/llvm。
- 提交：`{s['hq']}`；父提交：`{s['parent']}`。
- Gerrit：[change {q['number']}]({q['url']})，目标分支 `{q['branch']}`，状态 **{q['status']}**；当前 patch set {q['currentPatchSet']['number']}，ref `{s['change_ref']}`。
- 已存在的远端分支 `sandbox/dkson95/clang` 的tip精确等于463c9a13，证据为remote-heads.stdout；这与评审目标分支tizen_base是两回事。
- 标题：{q['subject']}。
- owner / patch author：{q['owner']['name']} <{q['owner']['email']}>。完整作者、提交者、日期和提交说明以 [show-stat.stdout](show-stat.stdout)、[commit-raw.stdout](commit-raw.stdout) 为准。
- 查询返回的当前打分：{', '.join(x['type']+' '+x['value']+' ('+x['by']['name']+')' for x in q['currentPatchSet']['approvals'])}。
- 评审意见含“Builds are verified on QB”及1216400、1216401链接。这是评审者原话，本任务没有读取QB验证该说法。

所有历史 patch set、打分、评审意见原文见 [gerrit-query.jsonl](gerrit-query.jsonl)。patch set 7 的行级/整组意见原文：
'''
for x in q['currentPatchSet'].get('comments',[]):text+=fence(x['message'])
text+='''
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

'''+f"采集时 `origin/tizen_base` HEAD 为 `{s['tizen_base_head']}`。父链的完整 first-parent SHA/parents 在 [parent-chain-complete.stdout](parent-chain-complete.stdout)；最近30层含完整提交说明见 [parent-chain-recent.stdout](parent-chain-recent.stdout)，自67619ec8后的提交与stat见 [parent-chain-since-67619ec8.stdout](parent-chain-since-67619ec8.stdout)。\n\n"
text+='|比较提交|完整SHA|该提交是463c9a13祖先|463c9a13是该提交祖先|\n|---|---|---|---|\n'
for i in range(0,len(s['ancestry']),2):
 a,b=s['ancestry'][i:i+2];text+=f"|{a['name']}|`{a['ancestor']}`|{'是 (exit0)' if a['is_ancestor'] else '否 (exit1)'}|{'是 (exit0)' if b['is_ancestor'] else '否 (exit1)'}|\n"
text+=f'''
每个方向都实际执行 `git merge-base --is-ancestor`，原始退出码在commands.json，输出在ancestor-*.stdout/stderr。相关直接父链为 `67619ec8 → f999bd40 → cf4b6777 → 463c9a13`；我方为 `67619ec8 → d4d6ca16 → f2553114 → 9e39fa8a`。HQ父提交是9e39fa8a祖先：**{'是' if s['parent_is_ancestor_of_ours'] else '否'}**。共同祖先原文：
'''+fence(read('merge-base-hq-ours.stdout'))+'''
`git branch -r --contains 463c9a13` 对已取回引用的原文：
'''+fence(read('branches-containing.stdout'))+'''
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
'''
for k,sha in [('hybrid','d4d6ca16b55a9afcb64a30ebf634f340f968267b'),('bolt','f2553114b05cbb022ff3ac062dbac284e1029df4'),('flags','9e39fa8a61392652bb28b75fc26216675bcad1d5')]:text+=f"|{k} `{sha}`|{', '.join(ov['per_commit'][k]) or '无'}|\n"
text+='\n四个提交各自完整文件清单及集合交集见 [overlap.json](overlap.json)、files-*.stdout。\n\n'
text+='''356627/356639的只读查询原文在 [archive-changes-query.jsonl](archive-changes-query.jsonl)：356627（67619ec8）为MERGED，涉及转换器和spec；356639为NEW，涉及spec。本包因此导出转换器，以及它在spec中的调用上下文；spec本身不是HQ此次改动文件。

|版本目录|提交|
|---|---|
'''
for k,v in s['versions'].items():text+=f'|files/{k}/|`{v}`|\n'
text+='''
每个版本均包含 `packaging/llvm-static-archives-native.py` 和 `packaging/llvm.spec` 完整原文。`diffs/` 分别给出 parent→HQ、ours→HQ、parent→ours 的 `git diff --full-index`，每对各两个文件；parent→HQ的spec diff为空，表示该文件没有改动。

## 5. 合并试探

只在上述临时clone中基于9e39fa8a新建 `hq-463c9a13-probe`，即使HQ父提交不在我方祖先链中仍执行试探。实际命令：

```sh
git switch -c hq-463c9a13-probe 9e39fa8a61392652bb28b75fc26216675bcad1d5
git -c user.name='Hao Lin' -c user.email=hao.lin@samsung.com cherry-pick --no-commit 463c9a133a6dfea9adf1e6c8e07ab705cbf2a587
git cherry-pick --abort
```

'''+f"cherry-pick 返回 **{s['cherry_pick_exit_code']}**；冲突文件：{', '.join(s['conflicts']) or '无'}；冲突块 **{s['conflict_blocks']}** 个。原始输出：\n"+fence(read('cherry-pick.stdout')+read('cherry-pick.stderr'))+'\ngit diff --stat 原文：\n'+fence(read('trial-diff-stat.stdout'))+f"\n`--abort` 返回 **{s['abort_exit_code']}**。abort后HEAD：\n"+fence(read('after-abort-head.stdout'))+'\nabort后 `git status --porcelain=v1` 原文（空表示干净）：\n'+fence(read('after-abort-status.stdout'))+'''
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
'''
labels={x['label']:x for x in cmds}
for p in sorted(E.rglob('*')):
 if not p.is_file() or p.name in ('README.md','SHA256SUMS'):continue
 rel=str(p.relative_to(E));desc=''
 if p.suffix in ('.stdout','.stderr') and p.stem in labels:desc=('原始标准输出：' if p.suffix=='.stdout' else '原始标准错误：')+'`'+' '.join(labels[p.stem]['argv'])+'`'
 elif rel.startswith('files/'):desc='git show导出的完整源码原文，版本见§4'
 elif rel.startswith('diffs/'):desc='两版本完整文件diff，方向见文件名'
 elif rel.startswith('conflicts/'):desc='试探时含冲突标记的完整文件，abort前保存'
 else:desc={'463c9a13.patch':'git format-patch -1 --stdout --full-index --binary 完整补丁','gerrit-query.jsonl':'目标提交Gerrit查询原文，含评审、打分和历史patch sets','archive-changes-query.jsonl':'356627/356639的Gerrit查询原文','summary.json':'版本、祖先、试探与abort结果结构化汇总','overlap.json':'各提交改动文件及交集','conflict-blocks.json':'冲突块完整原文及文件行号','commands.json':'后续命令、时间、返回码','collect.py':'采集/试探脚本原文，仅操作独立clone和材料目录','write-readme.py':'README生成脚本','resume.py':'补取9b8d74af后续采集和试探脚本；首轮失败原文保留'}.get(rel,'对应查询/clone的原始stdout、stderr或退出码')
 text+=f'|[{rel}]({rel})|{desc.replace("|","&#124;")}|\n'
text+='|[README.md](README.md)|材料说明、命令和事实汇总|\n|[SHA256SUMS](SHA256SUMS)|文件校验清单|\n'
(E/'README.md').write_text(text)
rows=[]
for p in sorted(E.rglob('*')):
 if p.is_file() and p.name!='SHA256SUMS':
  h=hashlib.sha256()
  with p.open('rb') as f:
   for b in iter(lambda:f.read(1048576),b''):h.update(b)
  rows.append(h.hexdigest()+'  '+str(p.relative_to(E)))
(E/'SHA256SUMS').write_text('\n'.join(rows)+'\n')
