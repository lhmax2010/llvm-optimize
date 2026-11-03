from pathlib import Path
import json,re
E=Path(__file__).parent;B=E.parents[4];W=Path('/home/linhao/Toolchain/development/llvm-optimize');T=W/'temp'
rows=json.loads((E/'units.json').read_text());assets={r['path']:r for r in json.loads((E/'local-assets-shallow.json').read_text())}
docs=list((B/'docs/bolt').glob('*.md'));content={str(p.relative_to(B)):p.read_text().splitlines() for p in docs}
lsof=(E/'lsof-matches.stdout').read_text()
mounts=(E/'mounts.stdout').read_text()
known={
'bolt-on-hybrid-20261024':('建议保留','33、34、37','products、perf-runtime 和保全 RPM 是后续包/性能对照；二进制未随 GitHub 文本证据发布。'),
'bolt-v4-20261022-cache-release':('建议保留','32、34、38','baseline/revised-products、preserved-before-delete 是已认证静态版本原件；根已清理不代表剩余 products 可删。'),
'debuglink-20261028':('建议保留','43、47、51','full-20261030/products、原始转换成员、llvm-profdata/runtime 仍供身份验证和 PGO 使用；GitHub 只发布报告/哈希等证据。'),
'debuglink-tb20261026':('建议保留','45、47','受保护原源码工作区，PGO 启动输入；不得清理整个父目录。'),
'pgo-resource-20261102':('建议保留','47','尚待执行的 PGO 试验现场、source-D、两次演练和训练准备；不以已提交设计文档代替现场。'),
'oldtext-final-20261027':('建议保留','39、41、42、43','已认证 products/符号实验输入；本轮 lsof 还看到 VS Code 打开文件。'),
'runpath-fix-20261026':('建议保留','37、39','认证 products、old-text 实验与测量输入；原始二进制不能从 GitHub 文本恢复。'),
'crash-fix-probe-20261028':('建议保留','42','objcopy 缺陷、符号文件与 LLDB 实测临时产物；源码行方案/缺陷仍挂账，副本唯一性未认证。'),
'final-20261103':('建议保留','50、51','configs/build.conf 和未来启动入口依赖仍需使用；只可另行评估已结束 rehearsal/gbs-root 子目录，不能整删父目录。'),
'second-review-20261104':('建议可删','51','两次演练已结束，日志/参数/清理/合成夹具结果已发布；没有完整 LLVM 构建产物，导出、包缓存、临时工具和合成 bitcode 可重建。保留本轮推送日志后方可整目录清理；重跑测试须重新准备绝对路径工具。'),
'review-20261102':('建议保留','48、51','当前三提交源码克隆和评审准备现场；不是清理范围。'),
'review-20261103':('建议保留','50','检查/演练准备输入，未证明所有现场均有发布副本；源码/工具依赖保留。'),
'gbs-root-x86_64-debuginfo-j4-v2':('建议保留','31、38','旧 R1 明确受保护的普通构建树；不是本轮可删项。'),
'gbs-root-x86_64-archivefix-v2':('建议保留','24、31、38','静态库修复历史根和受保护原始 RPM 组；不把后来的包冒充新基线。'),
'arm-source-root-probes-20261010':('建议保留','31、34、38','ARM sysroot/验证资产；不替主线决定弃用。'),
'archive-fix-v2-final-20261009':('建议保留','24、38','含 rpms-docs35 原始22包及来源记录，明确保留。'),
'perf-c-o2-os-20261025':('建议保留','34、37','C/C++ 测量输入和原始数据保留。'),
'hybrid-local-20261023':('建议保留','38、41；main 53','保全的 hybrid RPM/关键二进制，原构建根清理后这是对照资产。'),
'bolt-v4-20261021-disk-footprint':('建议保留','29、43、47','固定快照配置/build.conf 和测量准备需继续使用。')}
result=[]
for r in rows:
 if r['bytes'] is not None and r['bytes']<=5*2**30:continue
 name=Path(r['path']).name;a=assets.get(r['path'],{});marks=a.get('markers',[])
 hits=[]
 for doc,lines in content.items():
  if doc.endswith('51_second_review_fixes.md'):limit=153
  else:limit=len(lines)
  for n,line in enumerate(lines[:limit],1):
   if name in line and ('temp/' in line or name in ('second-review-20261104',)):
    hits.append({'document':doc,'line':n,'text':line})
 if name in known:group,source,reason=known[name]
 elif any(m['kind']=='git-worktree' for m in marks):group,source,reason='建议保留','38（或下列路径引用）','含源码仓库/工作树；未证明未发布提交和产物均有独立副本，不整目录删除。'
 else:group,source,reason='需要用户判断','38（历史盘点）' if any(h['document'].endswith('38_temp_cleanup_inventory.md') for h in hits) else '未找到明确任务归属','旧主线/归档/实验现场：未证明唯一证据和二进制都有可恢复副本；保留原件，由用户判断用途是否结束。'
 live=[l for l in lsof.splitlines() if r['path']+'/' in l and not l.startswith(('du ','python3 '))]
 if live:group='建议保留';reason+=' 本轮有进程打开文件，不建议删除。'
 mounted=[line for line in mounts.splitlines() if r['path']+'/' in line]
 if mounted:group='建议保留';reason+=' 存在挂载引用，不处理。'
 historical=[h for h in hits if h['document'].endswith('38_temp_cleanup_inventory.md') and h['text'].startswith('| `W/temp/')]
 purpose=historical[0]['text'].split('|')[3].split('源码')[0].replace('<br>',' ')[:150] if historical else name
 r.update(purpose=purpose,mount_references=mounted,group=group,task_documents=source,reason=reason,citations=hits,assets=marks,assets_scan_complete=not a.get('bounded',True),lsof_non_scan_hits=live,uniqueness='未做全盘逐文件SHA去重；未证实无唯一副本。已认证products/原始RPM/源码按保留处理。')
 result.append(r)
(E/'classified.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
for g in ['建议可删','建议保留','需要用户判断']:
 a=[r for r in result if r['group']==g];print(g,len(a),'measured GiB',sum(r['bytes'] or 0 for r in a)/2**30,'UNKNOWN',sum(r['bytes'] is None for r in a))
