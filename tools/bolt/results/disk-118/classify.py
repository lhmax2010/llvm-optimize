from pathlib import Path
import json,datetime
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.with_name('llvm-optimize-bolt');E=B/'tools/bolt/results/disk-118'
rows=json.loads((E/'measurements-combined.json').read_text())
old=[json.loads(l) for l in (B/'tools/bolt/results/disk-cleanup-20261114/inventory.jsonl').read_text().splitlines()]
oldkeep=[x['path'] for x in old if x.get('category')=='C']
candidates={
 str(W/'temp/combined-112-20261116'):'112准备停止后保留的补丁试应用工作树；112已发布patch-only diff和提交身份；按本任务明确列入过期工作树候选。删除前须另获批准并保全Git工作树登记。',
 str(W/'temp/rebase-359934-20261106-r2/rehearsal'):'已结束的旧入口演练输出，69/72号已发布；不包含其兄弟source目录。',
 str(W/'temp/rebase-359934-20261106/rehearsal'):'已结束的旧演练输出，69/72号有记录；保留兄弟source仓库。',
 str(W/'temp/rebase-359934-20261111-r6/rehearsal'):'74号已结束演练输出；保留同根toolchain/basedev完整构建和RPM、日志。',
 str(W/'temp/rebase-359934-20261111-r6/toolchain/validation/payload'):'74号入口的RPM载荷展开副本；原完整构建根和RPM保留，重新解包可重建；不删validation其他证据。',
 str(W/'temp/night-20261105/toolchain/validation/payload'):'63号入口的RPM载荷展开副本；同层gbs-root及其RPM/真实转换输入保留，可重新解包。',
}
by={x['path']:x for x in rows}
# Permission-denied roots are explicitly retained as incomplete measurements.
denied=[]
for f in E.glob('*stderr'):
 for l in f.read_text(errors='replace').splitlines():
  if "'" in l:denied.append(l.split("'",2)[1])
protected=[str(W/'temp'/n) for n in ['local-full-r6-20261111-materials','qb-1226850-1226851','qb-1231417-1231418','ps5-helper-114','ps5-helper-118','deleted-repo-backup-20261105','pgo-profiles-keep-20261102','tu-inputs-restored-20261106','fifth-review-20261111','night-20261103','weekend99-replay-20261114']]
def below(p,root):return p==root or p.startswith(root+'/')
for r in rows:
 p=r['path'];path=Path(p)
 if any(below(p,x) for x in candidates):
  x=next(x for x in candidates if below(p,x));cat='可以删除';why=candidates[x]
 elif below(p,str(B)) or p==str(W) or '/.git' in p or (path/'.git').exists() or any(below(p,x) for x in protected+oldkeep) or path.name in ('RPMS','SRPMS','repos','logs'):
  cat='必须保留';why='证据/源码仓库、114/118候选、保留基线或97号保护项；父目录含此类输入时不可整体删除。'
 else:cat='不确定';why='尚未逐项证明所有源输入、RPM、日志或未发布状态另有保留；不从名称/年代推断已无用途。'
 if '/rebase-359934-20261111-r6/' in p and not any(below(p,x) for x in candidates):
  cat='必须保留';why='74号完整构建及比较基线容器；RPM、日志和工具后续仍需使用，不整体删除。'
 r.update(category=cat,basis=why,permission_gap=any(below(x,p) for x in denied))
items=[dict(by[p],basis=why) for p,why in candidates.items() if p in by]
missing=[p for p in candidates if p not in by]
assert not missing,missing
items.sort(key=lambda x:x['bytes'] or 0,reverse=True)
total=sum(x['bytes'] or 0 for x in items)
(E/'delete-candidates.txt').write_text(''.join(x['path']+'\t'+str(x['bytes'])+'\t'+x['basis']+'\n' for x in items))
(E/'inventory.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
(E/'protected-locations.json').write_text(json.dumps([{'path':p,'exists':Path(p).exists(),'classification':'必须保留'} for p in protected],ensure_ascii=False,indent=2)+'\n')
# Top 30 are measured directory entries, with containment explicitly displayed;
# a second non-overlapping top-level table is provided for practical planning.
rank=sorted([r for r in rows if r['bytes'] is not None],key=lambda r:r['bytes'],reverse=True)
top=[r for r in rank if Path(r['path']).parent==W/'temp' or r['path']==str(B) or Path(r['path']).parent==W][:30]
df=json.loads((E/'df.json').read_text())
summary={'df':df,'candidate_bytes_observed':total,'candidate_count':len(items),'directory_records':len(rows),'root_W_total':'UNKNOWN: 900s timeout','home_abuild_exists':Path('/home/abuild').exists(),'other_project_directories_traversed':False,'top30_nonoverlapping':top,'top30_all':rank[:30]}
(E/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
fmt=lambda r:f"| {r['path']} | {r['bytes']/1024**3:.3f} | {r['mtime']} | {r['category']} | {r['basis']} |\n"
text='# 118 A：磁盘清点（只读，测量有缺口）\n\n'
text+=f"**/home 可用 {df['available']:,}B（{df['available']/1024**3:.2f}GiB）；总量 {df['total']:,}B，已用 {df['used']:,}B。列出 {len(items)} 个非重叠删除候选，已测占用合计 {total:,}B（{total/1024**3:.2f}GiB）。没有删除任何文件。**\n\n"
text+='主工作区整根du达到900秒限时；补测未覆盖一级目录，每目录120秒。night-20261103仍超时，部分历史GBS根有权限拒绝；UNKNOWN或已测下限均保留原文，不冒称全量精确总和。没有访问另一项目目录/进程/锁，没有sudo。/home/abuild不存在；本项目BUILD-ROOTS位于W/temp下。外部GBS根97号已标为其他项目或归属未明，本轮不遍历。\n\n'
text+='du按实际分配块计数、单次遍历对硬链接去重；不同测量调用间可能共享硬链接。表中目录包含关系不可相加，候选和也不保证等于实际释放空间。当前完整Git仓库、74号RPM/日志、1226850/1226851、未来1231417/1231418下载目录、H2/H3及114/118源码均保留。候选只是待用户批准的名单，不构成删除授权。\n\n'
text+='## 不重叠主要位置前30\n\n| 绝对路径 | GiB | 目录mtime（非递归最后改动） | 分类 | 依据 |\n|---|---:|---|---|---|\n'+''.join(fmt(r) for r in top)
text+='\n## 全部已测目录前30（包含父子关系，禁止累加）\n\n| 绝对路径 | GiB | 目录mtime | 分类 | 依据 |\n|---|---:|---|---|---|\n'+''.join(fmt(r) for r in rank[:30])
text+='\n## 可删除候选\n\n| 绝对路径 | GiB | 目录mtime | 分类 | 依据 |\n|---|---:|---|---|---|\n'+''.join(fmt(r) for r in items)
text+='\n[完整逐目录分类](../../tools/bolt/results/disk-118/inventory.jsonl)、[删除候选原文](../../tools/bolt/results/disk-118/delete-candidates.txt)、[测量总结](../../tools/bolt/results/disk-118/summary.json)、[初始du状态](../../tools/bolt/results/disk-118/measurement-errors.json)。B下载的新RPM会另附容量补记，不把后来下载计入本次时点。\n'
text+='\nA 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status=PARTIAL（测量缺口；只读清单已交付）\n'
(B/'docs/bolt/118_disk_audit.md').write_text(text)
print('candidate bytes',total,'count',len(items),'top10',[(r['path'],r['bytes']) for r in top[:10]])
print(text[-200:])
