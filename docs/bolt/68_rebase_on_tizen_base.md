# 68：改接最新 tizen_base 的核对结果（2026-11-06）

**第一项停止：359934实际仍为NEW，没有合入tizen_base。** 最新远端是撤销ThinLTO/静态库转换的f999bd40，不能当成任务要求的已合入基线。没有新建分支或worktree，没有cherry-pick或修改三个提交；第二、三项继续独立执行。

## 1. 只读远端证据

使用SSH BatchMode完整URL ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm，在W/temp/hq-463c9a13/repo操作，没有索要密码。查询、fetch、ls-remote原文均在[证据目录](../../tools/bolt/results/rebase-tizen-base-20261106/)。

```text
Gerrit change 359934: status=NEW, branch=tizen_base
current patch set=10
revision=13c3e223d9e1b35e4affb55255c5042f8c940f35
parent=cf4b6777d056131e2534ecb460c5575327d99646
ref=refs/changes/34/359934/10
ls-remote: f999bd406c0a70fe8107aa992164fe6945c5d46a refs/heads/tizen_base
```

PS10不是分支HEAD的祖先。当前HEAD没有packaging/llvm-static-archives-native.py，git show退出128：

```text
fatal: path 'packaging/llvm-static-archives-native.py' exists on disk, but not in 'f999bd406c0a70fe8107aa992164fe6945c5d46a'
```

完整查询：[gerrit-359934.stdout](../../tools/bolt/results/rebase-tizen-base-20261106/gerrit-359934.stdout)。最近10个提交及完整说明：[latest-log10.stdout](../../tools/bolt/results/rebase-tizen-base-20261106/latest-log10.stdout)。没有把评审中的PS10称为已合入版本。

## 2. 四条意见在PS10中的采纳情况（尚未合入）

|意见|PS10结果|实现|
|---|---|---|
|任何-g都要求-gdwarf-4|已采纳|has_debug_options检测任何-g开头；无DWARF或最后DWARF不是-gdwarf-4则报错|
|release输出带调试节时报错|已采纳|policy.dwarf为空而elf_details(data)[1]非空则报release conversion unexpectedly emitted debug sections|
|--param X仅接受ssp-buffer-size|已采纳|operand必须完整匹配ssp-buffer-size及整数值，否则报unclassified --param value|
|--param=X仅接受ssp-buffer-size|已采纳|只接受完整匹配--param=ssp-buffer-size及整数值，移除了泛化--param=前缀白名单|

[PS7→PS10转换器完整diff](../../tools/bolt/results/rebase-tizen-base-20261106/patchset7-final-converter.stdout)。证据文件名沿初始脚本，但内容明确为PS10，不是已合入版本。完整源码在pending-ps10-converter.txt。行号原文：

```text
L216:             if token == '--param' and not re.fullmatch(r'ssp-buffer-size=\d+', argv[index+1]):
L248:         elif re.fullmatch(r'--param=ssp-buffer-size=\d+', token):
L263:     has_debug_options = any(token.startswith('-g') for token in argv)
L264:     if has_debug_options and (not dwarfs or dwarfs[-1] != '-gdwarf-4'):
L669:                     raise ValueError('release conversion unexpectedly emitted debug sections')
```

以上是源码核对，没有声称跑过新分支测试。

## 3. 撤销的撤销与基线diff

cf4b6777d056131e2534ecb460c5575327d99646与67619ec8bbbac7238a6cfc33a481ccfbcd12206f的tree均为7b49745738b5512fbbed890e67e6a3861e1e39a5，diff为空。但cf4b6777不在当前远端tizen_base上。

最新tizen_base相对67619ec8：

```text
 packaging/llvm-static-archives-native.py | 788 -------------------------------
 packaging/llvm.spec                      |  67 +--
 2 files changed, 2 insertions(+), 853 deletions(-)
```

[全部文件完整diff](../../tools/bolt/results/rebase-tizen-base-20261106/base-diff.stdout)。当前HEAD提交说明为“Revert clang bootstrap + ThinLTO, fall back to GCC”。

## 4. 未执行范围与停止记录

改接、三个新SHA、标题修改、冲突合并、7706成员重放一致性、新分支测试、T/D演练均为NOT RUN。没有用未合入PS10替代用户指定基线。评审包目录仅有停止说明，没有伪造三个新补丁；原源码工作树不变。

命令全部使用串行systemd用户服务：MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、nice19、I/O idle。服务001因当前分支文件缺失退出128；服务002完成复核；没有OOM。没有sudo、构建或演练。

```text
ITEM1 已结束 2026-11-06T10:35:58.085829+08:00 status=stopped reason=359934-NEW-and-not-in-tizen_base
```
