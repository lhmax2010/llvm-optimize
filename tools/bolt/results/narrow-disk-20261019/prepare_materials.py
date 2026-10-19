from pathlib import Path
import subprocess,json,hashlib,shutil,difflib,ast
E=Path(__file__).resolve().parent;W=E.parents[1];B=W.parent/'llvm-optimize-bolt';S=W/'temp/bolt-v4-20261013/v41/llvm-source';D=B/'tools/bolt/results/narrow-disk-20261019';D.mkdir(parents=True,exist_ok=True)
def git(*a):return subprocess.check_output(['git',*a],cwd=S)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((E/'release.json').read_text());new=r['commit'];base=r['base'];parse=json.loads((E/'parse-results.json').read_text());structure=json.loads((E/'structure-result.json').read_text())
assert parse['status']=='PASS' and parse['lower_unchanged'] and not parse['unmount_errors']
assert len(parse['matrix'])==5 and all(x['PASS'] for x in parse['matrix'])
assert structure['PASS'] and 'Ran 289 tests' in (E/'tests.stderr').read_text() and (E/'tests.stderr').read_text().rstrip().endswith('OK')
assert json.loads((E/'shell-failure.json').read_text())['PASS'];assert git('status','--porcelain')==b''
assert git('diff','--name-only',base,new).decode().splitlines()==['packaging/clang-bolt-helper.py','packaging/llvm.spec']
check=subprocess.run(['git','diff','--check',base,new],cwd=S,capture_output=True,text=True);assert check.returncode==0
(E/'source-diff-check.json').write_text(json.dumps({'rc':check.returncode,'stdout':check.stdout,'stderr':check.stderr},indent=2)+'\n')
# Prove call delegates stdout directly to its log and retains existing success behavior.
t=ast.parse((S/'packaging/clang-bolt-helper.py').read_text());call=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='call');calls=[n for n in ast.walk(call) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='Popen'];assert len(calls)==1
stdout=next(k.value for k in calls[0].keywords if k.arg=='stdout');assert isinstance(stdout,ast.Name) and stdout.id=='output';assert 'threading' not in (S/'packaging/clang-bolt-helper.py').read_text()
assert all(not(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='disk_evidence') for n in ast.walk(call))
(E/'call-structure.json').write_text(json.dumps({'direct_log_stdout':True,'no_threads_or_pipe':True,'successful_log_not_checked_for_disk_words':True,'completed_sidecar_retained':True,'failure_log_attached':True},indent=2)+'\n')
# Delta BASE and amended NEW are siblings, so generate a genuine BASE->NEW diff.
message=(E/'new-message.txt').read_text();p=B/'patches/bolt/0007-narrow-bolt-disk-diagnostics.patch';p.write_bytes((f'From {new} Mon Sep 17 00:00:00 2001\nFrom: Hao Lin <hao.lin@samsung.com>\nSubject: [PATCH] packaging: keep disk diagnostics inside BOLT steps\nDelta-base: {base}\n\n'+message+'\n---\n').encode()+git('diff','--binary',base,new))
(B/'patches/bolt/0000-clang-bolt-squashed.patch').write_bytes(git('format-patch','--stdout','--no-binary','--no-signature','-1',new))
A=E/'delta-apply';(A/'packaging').mkdir(parents=True,exist_ok=True)
for name in ['clang-bolt-helper.py','llvm.spec']:(A/'packaging'/name).write_bytes(git('show',base+':packaging/'+name))
a=['patch','-p1','--batch','--input',str(p)];v=subprocess.run(a,cwd=A,capture_output=True);(E/'delta-apply.stdout').write_bytes(v.stdout);(E/'delta-apply.stderr').write_bytes(v.stderr);assert v.returncode==0
assert all((A/'packaging'/n).read_bytes()==(S/'packaging'/n).read_bytes() for n in ['clang-bolt-helper.py','llvm.spec'])
for f in E.iterdir():
 if f.is_file() and f.suffix in ('.json','.stdout','.stderr','.txt','.diff','.py','.spec','.sh','.xz'):
  shutil.copyfile(f,D/f.name)
for f in (E/'injection').iterdir():
 if f.is_file(): (D/'injection').mkdir(exist_ok=True);shutil.copyfile(f,D/'injection'/f.name)
shutil.copyfile(E/'export/llvm.spec',D/'gbs-exported-llvm.spec');shutil.copyfile(S/'packaging/llvm.spec',D/'llvm.spec');shutil.copyfile(S/'packaging/clang-bolt-helper.py',D/'clang-bolt-helper.py')
summary={'source_commit':new,'parent':r['parent'],'amended_from':base,'supersedes_unpushed':'e97171ff28b085a200ad1dbe69c1292e42b28ec7','tests':289,'ENOSPC':'PASS','non_disk':'PASS','diagnostic_exception':'PASS','unknown':'PASS','structure_byte_equal':True,'structural_exceptions':'post helper -B and appended disk-report post only','sh_e_failure':'PASS rc1','five_tizen_parses':'PASS 5/5','rpm_package':(E/'tizen-rpm-package-version.stdout').read_text().strip(),'lower_unchanged':True,'lock_held_seconds':parse['lock_held_seconds'],'graphical_prompts':1,'sandbox_pushed':False,'delta_apply':'PASS','files':r['files']}
(D/'validation-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
mp=B/'patches/bolt/draft-manifest.json';m=json.loads(mp.read_text());m.update(draft_commit=new,squashed_commit=new,tree=r['tree'],amended_from=base,files=r['files'],fixtures=289,qualification='NARROW_BOLT_SCOPE_LOCAL_AND_TIZEN_CERTIFICATION_PASS_WAITING_SANDBOX_PUSH',final_squashed_tests='289 PASS; structure byte-equal; sh-e rc1; Tizen rpm 4.14.1.1 five cases PASS',sandbox_pushed=False,remote_before=base,remote_after=base,remote_before_raw=(E/'remote-before.txt').read_text(),remote_after_raw=(E/'remote-before.txt').read_text(),material_pin=None,material_index_pin=None)
m['patch']['sha256']=sha(B/'patches/bolt/0000-clang-bolt-squashed.patch');m['incremental_patch']={'file':p.name,'base':base,'sha256':sha(p),'delta_apply':'PASS'};m['narrow_disk_revision']=summary;m['historical_unpushed_e971_disk_diagnostics']=m['disk_diagnostics'];m['historical_unpushed_e971_disk_diagnostics']['superseded_by_narrow_revision']=new;m['disk_diagnostics']=summary;m['sandbox_result']='PENDING: narrowed source fully certified, materials published before push';m['publication_order']='Narrowed source 289 tests, byte comparisons, sh-e and five Tizen parses PASS; publish materials before exact-lease sandbox push';m['GitHub_raw_URLs_verified_before_sandbox']=0;m['post_capture']='Baseline and narrowed host scripts copied only; full platform chain byte-equal; no product execution';mp.write_text(json.dumps(m,indent=2)+'\n')
# Current maintenance policy: baseline RPM execution is not ours to wrap.
f=B/'docs/bolt/maintenance.md';text=f.read_text();anchor='## 运行前提与资源\n';text=text.replace(anchor,anchor+'\n长期规则：rpm 以 sh -e 执行脚本段；BOLT 改动不得改写普通构建、基线 %install 步骤和平台后处理链的执行方式。诊断只覆盖BOLT自身步骤，不捕获普通ninja或平台post的输出；基线失败仍由原脚本执行方式停止。\n',1)
text=text.replace('以本步骤 errno28/122 或四类日志文本判定，不以 free 大小判定。','以本步骤 errno28/122 或四类日志文本判定，不以 free 大小判定。日志非空可读且无磁盘迹象为not-disk；日志缺失、空或不可读为unknown，只报剩余和已用，注明“日志不可用，无法判定原因”，不得猜测。')
f.write_text(text)
checks=structure['checks'];unknown=next(l for l in (E/'injection/unknown.stdout').read_text().splitlines() if l.startswith('BOLT_DISK_DIAGNOSIS '))
section=f'''\n\n## 收窄修订（2026-10-19；e97171ff不采用）

PM结论：RPM用`/bin/sh -e`执行脚本段，普通命令失败已有停止机制。e97171ff包装普通LLVM ninja、基线安装和平台post，会使长阶段输出延迟到命令结束，并改变已认证平台链。撤回这些包装，不推e97171ff。

本次直接在BASE `{base}` 上amend，最终源 `{new}`，父仍 `{r['parent']}`，不是在e97171ff上叠加；Hao Lin作者/提交者/Signed-off-by及原Change-Id保留，说明每行≤72。profile、BOLT生成参数、既有4ec候选不变。当前为全部认证PASS、待按精确租约推sandbox；发布结果在后续收尾节登记。

长期规则：**rpm 以 sh -e 执行脚本段；BOLT 改动不得改写普通构建、基线 %install 步骤和平台后处理链的执行方式**。本地资源/锁/磁盘规则仅用于本地执行，不进入发布代码。

### 撤回与保留

- `%build`普通ninja行和全部条件分支恢复BASE；删除BOLT_BUILD_OUTPUT内存捕获，主构建正常即时输出。
- 普通cmake install、所有ln/clang.cfg heredoc/mkdir/mv/cp/rm及静态库转换调用恢复BASE；删除__bolt_disk_reporting全套前缀和宏。
- 平台post恢复原宏原样执行一次，删除platform-post的run-step、内存捕获及嵌套shell/heredoc。BOLT尾检保留原结构，仅helper加-B及最后附一行disk-report post。
- BOLT helper子命令保持BASE直接`python3 ... || exit 1`，只加-B；失败由自身cli先诊断再rc1，不另包一层run-step。
- 只包装下面8个BOLT动作（六类命令加BEGIN/END两个标记）。spec完整diff见下，人工复核差异仅用户1a–e允许范围；普通基线没有新增函数调用。
- call恢复BASE：Popen stdout=日志文件、stderr=STDOUT，无管道/线程，成功不扫描日志字样。只保留成功completed=True侧记录和失败bolt_log。atomic_text/save、临时clang fsync/SHA/最终rename及磁盘实际大小公式保留。

|新spec行|BOLT命令|
|---|---|
'''
for row in structure['wrapped_BOLT_actions']:section+=f"|{row['line']}|`{row['text'].replace('|','&#124;')}`|\n"
section+='''
### 三态原因判定

直接errno28/122，或本步骤日志匹配四类磁盘字样 => disk；日志可读、非空且无磁盘迹象 => not-disk；日志不存在、为空或不可读 => unknown。unknown只报当前free/used，说明“日志不可用，无法判定原因”，不做需求推算。/dev/stdin只读取一次，分类和证据复用同一份文本，避免第二次读取空流造成错误判定。成功命令即使日志出现ENOSPC文本也不失败。

unknown CLI故障注入原文（free4096为夹具值）：

```text
'''+unknown+'''
```

### 逐字节结构比较

`python3 -B structure_check.py`：完整脚本及提取结果随证据公开。%build取`%build`至`%install`全部字节；%install保留BOLT架构/开关双块以外的全部行（包括普通x86静态库转换块）；平台链从两次RPM真正生成但只复制的脚本提取，宏路径完全相同。post尾检另外仅撤销被允许的-B和新增观测后比较，不能声称含允许差异的尾检全文原始字节相同。

|cmp项目|字节|退出码|结论|
|---|---:|---:|---|
'''
for name in ['build','install-baseline','platform-post','post-tail-allowed-edits-only']:
 c=checks[name];section+=f"|{name}|{c['bytes']}|{c['rc']}|逐字节相同|\n"
section+='\n实际比较命令和结果（完整argv也见structure-result.json）：\n\n```sh\n'
for name in ['build','install-baseline','platform-post','post-tail-allowed-edits-only']:
 c=checks[name];section+=' '.join(c['argv'])+'\n# exit '+str(c['rc'])+'; stdout/stderr empty\n'
section+='''```

Host两个capture的rpmbuild退出1是copy-only包装之后空BUILDROOT的文件清单失败，不是执行安装失败；两个生成脚本都`/bin/sh -n`通过。没有执行其中任何cmake/ninja命令。完整平台链原文分别见base-platform-post.txt/new-platform-post.txt。

### 本次全部验证

|项目|结果|
|---|---|
|既有测试按新行为更新+新增unknown等|289/289 PASS（49.103秒）|
|ENOSPC复制/JSON/子进程/安装|PASS，rc1，磁盘判定及字段保持；安装原clang SHA不变|
|非磁盘失败|PASS，非空可读本步骤日志，not-disk，原始错误不变|
|诊断自身异常|PASS，原始错误/rc1不变|
|unknown缺失/空/不可读日志|PASS，仅free/used与说明，无推算|
|成功日志含ENOSPC|PASS，命令成功不变成失败|
|/dev/stdin日志一次读取|PASS，分类和evidence保持一致|
|sh -e +仅BOLT函数+失败命令|PASS，诊断后rc1，不运行SHOULD_NOT_RUN|
|结构cmp与完整spec diff|PASS，范围符合用户1a–e|
|gbs export新提交|PASS，命令/版本/导出spec全部保存|
'''
for row in parse['matrix']:section+=f"|Tizen rpm {row['name']}|PASS，主解析rc{row['rc']}，7个Patch，Source/Patch清单保存|\n"
section+=f'''|下层完整清单与六SHA|前后完全一致，锁持有{parse['lock_held_seconds']:.3f}秒，卸载错误0|

构建根rpm包版本 `{summary['rpm_package'].replace(chr(10),'; ')}`，CLI显示4.14.1；主解析用rpmbuild -bp --nodeps --nobuild，关闭项确用--without clang_bolt。辅助Source/Patch清单用rpmspec -P，因该rpmspec不支持--without，清单项用等效宏，不替代主解析。五个目标均在同一x86根的rpm完成，不进入ARM树。唯一一次图形认证成功，一次sudo完成overlay/proc/dev挂载、abuild解析、卸载；下层仅只读，未运行原树cmake/ninja/-P。

准备记录：图形包装的启动比gbs导出完成稍早；在任何根内产品操作之前加导出完成等待与rc0核对，实际root-entry发生在最终导出成功之后。没有重复图形认证，没有产品输入/环境重试。既有“线程日志ENOSPC”用例改为直接打开日志ENOSPC，符合恢复后的直接输出方式；非磁盘用例提供真实非空步骤日志，缺失日志另列unknown。其余原测试保留，新增4项，总数从285到289。前半的25处宽泛包装审计属于未采用e971历史方案，不再代表本修订；本修订普通步骤依赖原RPM sh-e停止机制。

### 两份spec完整diff（BASE→本次）

```diff
'''+(E/'spec.diff').read_text()+'''```

完整helper/spec总diff见本轮source.diff；0007为e2463165到本修订的真正增量（不是676父提交的全量），独立patch -p1后两文件逐字节等于新提交；0000文本版与profile分开交付。提交说明完整原文和message.diff也一并公开。
'''
f=B/'docs/bolt/27_disk_diagnostics.md';text=f.read_text().split('\n\n## 收窄修订（2026-10-19；e97171ff不采用）')[0];f.write_text(text+section)
f=B/'docs/bolt/STATUS.md';text=f.read_text();start=text.index('本地源 `e97171ff28b085a200ad1dbe69c1292e42b28ec7`');text=text[:start]+'''历史未采用草案e97171ff：本地285测试PASS，唯一图形认证失败，Tizen五项NOT RUN，未推sandbox。其普通步骤包装与25处审计已被下节收窄修订取代；原文保留在27前半和67b0227材料钉提交。\n'''
text+=f'''\n## 2026-10-19：收窄磁盘诊断范围（认证PASS，待推）\n\n长期规则：rpm 以 sh -e 执行脚本段；BOLT 改动不得改写普通构建、基线 %install 步骤和平台后处理链的执行方式。\n\n直接在e2463165 amend为 `{new}`（父67619ec8，Hao Lin/原Change-Id），不叠加e971。%build全段9331B、基线install1895B、实际平台链304B逐字节相同；只允许尾检-B及末尾report，8个BOLT shell动作包装。call恢复直接日志，无线程/管道、不检查成功日志文本；诊断disk/not-disk/unknown，日志不可用不猜测。289测试、三类加unknown、sh-e rc1、gbs export及构建根Tizen五项全部PASS。一次图形认证，锁{parse['lock_held_seconds']:.1f}秒，overlay/proc/dev卸载完、下层清单及六SHA不变；未运行原树cmake/ninja/-P。材料先GitHub，随后按e246精确租约更新唯一bolt_pgo；推送结果另记收尾。详见27末节和narrow-disk-20261019。\n'''
f.write_text(text)
print(json.dumps({'new':new,'evidence_files':len([f for f in D.rglob('*') if f.is_file()]),'report_bytes':(B/'docs/bolt/27_disk_diagnostics.md').stat().st_size,'status_bytes':f.stat().st_size,'ready_for_sandbox':True},indent=2))
