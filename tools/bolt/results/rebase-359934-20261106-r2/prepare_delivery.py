from pathlib import Path
import hashlib,json,subprocess,datetime,os
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=Path(str(W)+'-bolt');S=W/'temp/rebase-359934-20261106/source'
E=B/'tools/bolt/results/rebase-359934-20261106-r2';P=B/'patches/rebase-359934-20261106-r2';P.mkdir(exist_ok=False)
BASE='13c3e223d9e1b35e4affb55255c5042f8c940f35';OLD='7d5e28ca89ed68e3360765bc4e42234eaaabae27'
rows=json.loads((E/'commit-identities.json').read_text());HEAD=rows[-1]['sha']
def git(*args,**kw):return subprocess.check_output(['git','-C',str(S),*args],**kw)
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
for n,row in enumerate(rows,1):
 (P/f'{n:04d}.patch').write_bytes(git('format-patch','--stdout','--full-index','--binary','-1',row['sha']))
 (P/f'{n:04d}-message.txt').write_text(row['message']+'\n')
(P/'0002-text-only.patch').write_bytes(git('format-patch','--stdout','--full-index','-1',rows[1]['sha'],'--','.',':(exclude)packaging/clang-bolt-v2.fdata.xz'))
(P/'series-text-only.diff').write_bytes(git('diff','--full-index',BASE,HEAD,'--','.',':(exclude)packaging/clang-bolt-v2.fdata.xz'))
(P/'since-7d5e28ca.diff').write_bytes((E/'source-vs-7d5e.diff').read_bytes())
cmake=[x for x in git('diff','--name-only',BASE,rows[0]['sha']).decode().splitlines() if x!='packaging/llvm.spec']
assert len(cmake)==6
paths=['packaging/llvm.spec','packaging/clang-bolt-helper.py','packaging/llvm-static-archives-native.py']+cmake
for name in paths:
 p=P/'files'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(git('show',HEAD+':'+name))
profile=S/'packaging/clang-bolt-v2.fdata.xz'
committable='\n'.join('| '+str(n)+' | '+r['sha']+' | '+r['title']+' | '+r['tree']+' |' for n,r in enumerate(rows,1))
readme=f"""# 第二轮代码评审修复包（2026-11-06）

评审本轮增量先读 [since-7d5e28ca.diff](since-7d5e28ca.diff)。BOLT 的可读补丁为 [0002-text-only.patch](0002-text-only.patch)，不含 profile 二进制；可应用的完整补丁为 [0002.patch](0002.patch)。

基线固定为 \u0060{BASE}\u0060（Change 359934 PS10）。按顺序应用三个完整 format-patch；相对于前轮 \u0060{OLD}\u0060 的改动仅涉及 spec、helper、转换器。混合链接提交原样保留。源码提交仅在本地，没有推送 Gerrit 或 sandbox。

| 顺序 | SHA | 标题 | tree |
|---|---|---|---|
{committable}

## 本轮内容

- 转换器拒绝未经认证的 assembler 参数，核对 clang/llvm-dis/llvm-nm 完整版本一致，简化模式不一致错误并注明 -g0 风险。
- debuglink 门禁加入 ELF 头/程序头/全部 LOAD 内容检查，仅继续归一化已批准的三个节表定位字段。
- 取消返回 128+signal；命令失败后清理中又取消时保留原失败，磁盘诊断是否跳过由错误来源属性决定。五处可选调用不再吞掉取消。
- 固定 expected-dropped 字面值；空调试序列提示 no debug options；补齐注释并改写第三个提交的 MODULE/LDFLAGS 说明。

验证：helper 393、参数/转换器 46（包含既有 42）、50 号 5、新增 12 项通过；真实 release C-2 正反例通过；12 项展开与 5 项 RPM 解析通过；7706 个成员重放参数完全一致；T/D 演练通过。实物副本 strip、RUNPATH、debuglink、post 门禁通过；一个真实 release 成员转换前后对象相同。没有重新构建 LLVM 或 RPM，未宣称全量转换输出或整包一致。

详细证据见 [70 号文档](../../docs/bolt/70_second_code_review_fixes.md) 与 [结果目录](../../tools/bolt/results/rebase-359934-20261106-r2/)。

Source1200：\u0060packaging/clang-bolt-v2.fdata.xz\u0060，{profile.stat().st_size} 字节，SHA256 \u0060{sha(profile)}\u0060。二进制只包含在完整 0002.patch 中，files/ 不复制 profile。

## 文件

- 0001.patch / 0002.patch / 0003.patch：完整提交补丁。
- 0001-message.txt / 0002-message.txt / 0003-message.txt：完整提交说明。
- 0002-text-only.patch：BOLT 文本评审补丁。
- series-text-only.diff：三个提交相对 PS10 的全部文本改动。
- since-7d5e28ca.diff：本轮增量完整 diff。
- files/：最终 spec、helper、转换器及六个 CMake 文件全文。
- SHA256SUMS：除自身以外全部文件的 SHA256（包含 README）。

旧评审包保留；本包描述本地修复后的三提交，未修改远端分支。
"""
(P/'README.md').write_text(readme)
(P/'SHA256SUMS').write_text(''.join(sha(p)+'  '+str(p.relative_to(P))+'\n' for p in sorted(P.rglob('*')) if p.is_file() and p.name!='SHA256SUMS'))
# Check materialized patch application using a fresh index, without checkout/branch.
idx=W/'temp/rebase-359934-20261106-r2/review-apply.index'
assert not idx.exists();env=dict(os.environ,GIT_INDEX_FILE=str(idx))
subprocess.run(['git','-C',str(S),'read-tree',BASE],check=True,env=env)
for n in range(1,4):subprocess.run(['git','-C',str(S),'apply','--cached',str(P/f'{n:04d}.patch')],check=True,env=env)
tree=git('write-tree',env=env).decode().strip();assert tree==rows[-1]['tree']
(E/'patch-application.json').write_text(json.dumps({'baseline':BASE,'result_tree':tree,'expected_tree':rows[-1]['tree'],'PASS':True,'index':str(idx)},indent=2)+'\n')
print('PATCH_APPLY_PASS',tree)
