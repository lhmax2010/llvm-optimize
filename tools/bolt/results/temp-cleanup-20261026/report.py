from pathlib import Path
import json,csv,datetime,collections,re
E=Path(__file__).resolve().parent;B=E.parents[3];W=Path('/home/linhao/Toolchain/development/llvm-optimize');T=W/'temp';G=2**30
load=lambda n:json.loads((E/n).read_text())
u=load('units.json');sub=load('subunits.json');meta={x['path']:x for x in load('metadata.json')};old={x['path']:x for x in json.loads((B/'tools/bolt/results/root-inventory-20261022/inventory.json').read_text())};refs=load('doc-references.json');scripts=load('script-references.json');hard=load('hardlinks.json');plans=load('scenarios.json');activity=load('final-activity.json');repo=load('repository-state.json');allassets=load('asset-hashes.json')+load('asset-hashes-supplement.json')+load('asset-hashes-inode-aliases.json')+load('report-assets.json')+load('small-assets-supplement.json')
assert not activity['active_paths'] and not activity['mounts'] and activity['fuser_rc']==1 and not activity['fuser_stdout'] and not activity['fuser_stderr']
heads={k:v['head']['stdout'].strip() for k,v in repo.items()};du={x['path']:x for x in u+sub}
def short(p):return p.replace(str(W),'W',1) if p.startswith(str(W)) else p
def dt(ns):return datetime.datetime.fromtimestamp(ns/1e9,datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec='seconds') if ns else '未取得'
def within(p,r):return p==r or p.startswith(r+'/')
def cite(text):
 out=[]
 for branch,file,line in re.findall(r'(main|bolt|bolt-v4)/(docs/[^:;；\s]+):(\d+)',text):
  key='main' if branch=='main' else 'bolt-v4';out.append(f'[{key}/{file}:{line}](https://github.com/lhmax2010/llvm-optimize/blob/{heads[key]}/{file}#L{line})')
 return '；'.join(out[:2]) or text
new={
 'bolt-v4-20261022-cache-release':('BOLT/cache-release','9e5675f、d20e873；双轮完整构建与比较已完成','bolt/docs/bolt/32_cache_release.md:232; bolt/docs/bolt/32_cache_release.md:244'),
 'hybrid-local-20261023':('hybrid','6e9d4f2；本地构建完成，PM裁决PASS附例外','main/docs/53_hybrid_local_validation.md:9; main/docs/53_hybrid_local_validation.md:182'),
 'bolt-on-hybrid-20261024':('hybrid+BOLT','aa637c1；本地完整构建与验证PASS','bolt/docs/bolt/33_bolt_on_hybrid.md:3; bolt/docs/bolt/33_bolt_on_hybrid.md:7'),
 'archive-fix-full-build-20260927':('archive fix','历史完整构建/临时RPM仓库；源码提交本轮未核定，不判定可弃用','main/docs/36_archive_fix_tizen_consumers.md:15; main/docs/STATUS.md:405'),
}
extra=set(plans['aggressive']['home']['paths']+plans['aggressive']['var_tmp']['paths'])-set(plans['conservative']['home']['paths']+plans['conservative']['var_tmp']['paths'])
selected=set(plans['aggressive']['home']['paths']+plans['aggressive']['var_tmp']['paths'])
rows=[];linkrows=[]
for x in sorted([x for x in u if x['group']!='W' and x['bytes'] and x['bytes']>5*G],key=lambda x:-x['bytes']):
 p=x['path'];name=Path(p).name;m=meta[p];o=old.get(p,{})
 if name in new:line,purpose,ref=new[name]
 else:
  purpose=o.get('purpose','出处未完整认证')+'；源码 '+o.get('source','未知')
  line='BOLT' if name.startswith('bolt') or name=='bench_results' else 'hybrid' if 'hybrid' in name or 'intranet' in name else 'llvm-strip' if 'strip' in name else 'release归因' if 'release' in name else 'ARM/archive fix' if 'arm' in name else 'archive fix'
  ref=o.get('ref','')
  if not ref:
   rr=[r for r in refs.get(name,[]) if not r['file'].endswith('31_build_root_inventory.md')]
   if rr:ref=f"{rr[0]['repo']}/{rr[0]['file']}:{rr[0]['line']}"
 own=[s for s in selected if within(s,p)];git=m['git_roots'];shared=[]
 for key,h in hard.items():
  here=[q for q in h['paths'] if within(q,p)]
  if here and len(here)<h['nlink']:shared.append(dict(inode=key,nlink=h['nlink'],paths_here=here,known_other_paths=[q for q in h['paths'] if not within(q,p)],unlocated_links=h['nlink']-len(h['paths']),bytes=h['allocated']))
 linkrows.append(dict(path=p,external_hardlink_inodes=len(shared),details=shared))
 if name in ['bolt-v4-20261022-cache-release','hybrid-local-20261023','bolt-on-hybrid-20261024']:
  advice='先保存小文件再删除（仅所列构建根）';reason='已完成；products、输入、source、脚本和报告留在父目录，见第3节精确范围'
 elif p in extra:advice='可以删除（激进方案，待批准）';reason='已完成的RPM载荷，原包仍在；重跑历史脚本前须重新解包'
 elif name=='bolt-v4-20261016-source-order':advice='可以删除 upper-parse；其余保留';reason='旧解析overlay上层；无活动挂载，报告/脚本和导出留在父目录'
 elif name=='llvm-optimize-x86-archivefix-20261013':advice='仅 lto.cache 可以删除；其余保留';reason='历史树禁恢复/配置；后续安装不读缓存，但原输入、归档证据和RPM仍保留'
 elif git:advice='保留';reason='包含源码仓库/工作树，明确排除；不能按整个父目录删除'
 elif name=='bench_results':advice='保留';reason='profile训练/留出输入与真实TU资产，用户明确保留'
 elif name=='archive-index-fix-rpm-20260923':advice='保留（待用户判断）';reason='H为旧唯一基线；未认证可完整恢复它的原RPM，不能当普通解包副本'
 elif name=='gbs-root-x86_64-debuginfo-j4-v2':advice='保留';reason='34号性能输入的x86 sysroot和历史工具来源；旧保护未解除，本次未纳入整根清理'
 elif 'arm' in name:advice='保留（待用户判断）';reason='ARM转换/主线历史输入，部分仍是34号sysroot；不代替主线决定弃用'
 else:advice='保留（待用户判断）';reason='旧主线结果/保护范围或复现输入，尚无明确弃用裁决'
 assets=[a for a in allassets if within(a['path'],p)]
 rootnote=f"root目录{m['root_owned_dirs']}；不可写目录{m['not_writable_dirs']}；遍历错误{len(m['errors'])}"
 row=dict(path=p,bytes=x['bytes'],filesystem='/dev/sda1 (/home)' if p.startswith('/home/') else '/dev/nvme0n1p1 (/)',latest_file=dt(m['newest_file_ns']),latest_file_path=m['newest_file'],line=line,source_purpose=purpose,provenance=ref,publication='所引文档在已核对的GitHub HEAD；不等于全部temp原件已发布',completion='完成，结论已发布' if name in new and name!='archive-fix-full-build-20260927' else '历史轮有记录；是否还要重跑/后续用途待确认',advice=advice,reason=reason,cleanup_scopes=own,git_roots=git,permissions=rootnote,script_reference_count=len(scripts.get(name,[])),external_hardlink_inodes=len(shared),asset_hash_rows=len(assets),blind=x['rc']!=0)
 rows.append(row)
(E/'analysis-inventory.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');(E/'external-hardlinks.json').write_text(json.dumps(linkrows,indent=2)+'\n')
for name,data in [('inventory.tsv',rows),('top-level-du.tsv',sorted(u,key=lambda x:-int(x['bytes'] or 0)))]:
 with (E/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(data)
dups=collections.defaultdict(list)
for a in allassets:
 if a.get('sha256'):dups[a['sha256']].append(a['path'])
with (E/'asset-catalog.tsv').open('w') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['path','bytes','SHA256','same_sha_other_paths','reason'])
 for a in sorted(allassets,key=lambda a:a['path']):w.writerow([a['path'],a['bytes'],a.get('sha256','ERROR'),';'.join(p for p in dups.get(a.get('sha256'),[]) if p!=a['path']),a.get('reason','')])
df=(E/'df-final.stdout').read_text();avail={}
for l in df.splitlines()[1:]:
 v=l.split();avail['home' if v[-1]=='/home' else 'var_tmp']=int(v[3])
lines=['# 38. W/temp 与项目构建根：只读清理建议（2026-10-26）','', '**本轮没有删除、移动、改权限、提权、挂载、构建或推送 Gerrit。下面均为待用户逐项批准的建议，不是执行记录。**','',f"W 可见实占 **{du[str(W)]['bytes']/G:.3f} GiB**，其中 W/temp **{next(x['bytes'] for x in u if x['path']==str(T))/G:.3f} GiB**。优先处理已完成的两轮 cache-release、hybrid、hybrid+BOLT 构建根；先保全未有同 SHA 副本的RPM、关键文件和性能运行环境。products、TU/C输入、profile、源码工作树、工具及已提交证据全部保留。",'', '| 方案 | /home净释放估算 | /home执行后可用估算 | /var/tmp所在盘净释放估算 | 该盘执行后可用估算 |','|---|---:|---:|---:|---:|']
for label,title in [('conservative','稳妥：仅所列构建根/缓存'),('aggressive','激进：再加可恢复载荷/旧解析upper')]:
 p=plans[label];h=p['home']['net_reclaim_estimate'];v=p['var_tmp']['net_reclaim_estimate'];lines.append(f'| {title} | {h/G:.3f} GiB | {(avail["home"]+h)/G:.3f} GiB | {v/G:.3f} GiB | {(avail["var_tmp"]+v)/G:.3f} GiB |')
lines+=['',f"/home 当前可用 {avail['home']/G:.3f} GiB；/var/tmp 在 `/dev/nvme0n1p1` 的 `/` 文件系统，可用 {avail['var_tmp']/G:.3f} GiB。**两盘不可相加。** 上表已从 /home 扣除 {plans['conservative']['home']['copy_budget_allocated']/G:.3f} GiB 的先保全预算，包括所有RPM（连依赖缓存包也保守保留）。未认证重复内容的包不擅自去重；已实测同SHA或同inode的文件才计为已有副本。新副本预算按原分配块估计，复制时仍须实际校验，表中不是可立即兑现的空间承诺。",'', '## 1. 范围、方法与盲区','', f'- `W={W}`；`T=W/temp`；`B={B}`。所有扫描以 `nice -n 19 ionice -c3` 运行；没有获取锁或改变正在运行任务的设置。只在B写本次证据和文档。',f'- 实测 {len(u)} 个一级目录（W 6项、temp {sum(x["group"]=="temp" for x in u)}项、项目名匹配或GBS候选/var/tmp {sum(x["group"]=="var-tmp" for x in u)}项），另 {len(sub)} 个精细范围；原始 `du -sx -B1` stdout/stderr、退出码和耗时见 units.json、commands.json、subunits.json。>50 GiB父目录额外有 expand-*.stdout 一层展开。所有大小为实际分配，不是 apparent-size。', '- 同一父子目录不能重复相加。**scenarios.json** 中的选定范围不重叠，用 st_dev/st_ino/st_nlink 修正跨范围硬链接；对本次两套方案修正值均为0。其他目录有外部硬链接时已单列，不能直接按独立du相加。', f'- 元数据遍历见到 {sum(m["files"] for m in meta.values()):,} 个普通文件、{sum(len(m["errors"]) for m in meta.values())} 条遍历错误。†为可见下界；不提权，root/ldconfig/upgrade等盲区原文保留。mtime取最新后代**普通文件**，不是目录mtime，更不是最后使用时间；未来/固定测试时间戳照录。', '- 先后两次全局lsof，辅以fuser、ps、全部可读/proc/*/mountinfo和cwd/root。最终本次范围未见lsof/fuser命中，活动overlay/挂载引用0。无权限打开的FD仍是盲区；fuser目录检查不递归证明所有后代无打开文件，因此同时做全局lsof路径边界筛选。删除前必须再检查，不把本次快照当永久许可。', '- 本机 fuser 首次带 `--` 返回 “No process specification given”，这是参数兼容性错误，不是无进程；已去掉该分隔符，以绝对路径重新检查。原始失败保留在 fuser.*，有效结果为 fuser-checked.* 与 fuser-final.*（退出1、stdout/stderr空）。没有据失败命令放行。', f'- 已只读核对GitHub：main `{heads["main"]}`、bolt-v4 `{heads["bolt-v4"]}` 与本地HEAD一致。文档出处因此已发布；不能由此推出temp中的所有二进制/日志都已备份。main中已有gbs_llvm.conf修改和未跟踪证据未动。', '- 本轮发现P1–P3均不存在。P4旧upper也已不存在，旁边有root属主的preserved-from-upper；31号文档仍记P4未获批准，本轮没有找到对应后续执行记录，不推测是谁、何时删除。P4旧60.530 GiB不再计入方案。runpath-fix-20261026当前不存在；若之后创建，整目录自动保留。','', '## 2. 一级占用排序','', '完整122个temp子目录与12个/var/tmp项目目录（包括小目录）见 [top-level-du.tsv](../../tools/bolt/results/temp-cleanup-20261026/top-level-du.tsv)。下面先列W一级；temp大目录的逐项分析在第4节。没有列入方案的目录默认保留。','', '| W一级目录 | 实占GiB | 处理 |','|---|---:|---|']
for x in sorted([x for x in u if x['group']=='W'],key=lambda x:-x['bytes']):lines.append(f'| `{short(x["path"])}` | {x["bytes"]/G:.3f}{"†" if x["rc"] else ""} | '+('仅按第3节子范围建议，不能整删' if x['path']==str(T) else '保留：源码/Git/工具/已提交文档证据')+' |')
lines+=['','## 3. 两套方案的精确范围（待批准）','', '**稳妥方案**只涉及下面5个范围；四个GBS根须先完成 preserve-before-delete.json 中的保全。绝不删除这些范围的父目录，因其中有products、source、脚本、报告和输入。','', '| 精确路径 | 毛占用GiB | 建议/前提 |','|---|---:|---|']
for p in plans['conservative']['home']['paths']+plans['conservative']['var_tmp']['paths']:
 lines.append(f'| `{short(p)}` | {du[p]["bytes"]/G:.3f} | '+('可以删除缓存；保留该树其他输入/RPM；以后重链将重新生成缓存' if p.endswith('lto.cache') else '先保全未有同SHA副本的RPM/关键文件，再删除此构建根；root系统目录需另行授权sudo')+' |')
lines+=['','**激进方案**在稳妥基础上增加下面5项。载荷可从列明的原RPM重新解包；引用这些路径的历史脚本将不能直接重跑，须先恢复载荷。本轮不修改这些脚本。','', '| 精确路径 | 毛占用GiB | 恢复依据/风险 |','|---|---:|---|']
restore={str(T/'toolchain-archivefix-v2-final'):'docs35原22RPM：T/archive-fix-v2-final-20261009/rpms-docs35；原件保留',str(T/'toolchain-llvm-strip'):'docs38的22RPM仍在gbs-root-x86_64-archivefix-v2/.../rpmbuild/RPMS/x86_64；不把它们说成67619ec8新构建',str(T/'toolchain-release-x86-20261013'):'docs49交接树/var/tmp/llvm-optimize-x86-archivefix-20261013/.../rpmbuild/RPMS/x86_64；该树仅删缓存，RPM保留',str(T/'bolt-v4-20261016-source-order/upper-parse'):'docs26解析实验已结束；upper-parse不是原始输入，报告/脚本/导出留在父目录；原下层保留','/var/tmp/llvm-optimize-archivefix-v2-final-20261009/independent-install':'docs35独立安装载荷；原RPM及外部验收报告保留；重跑需重建DESTDIR'}
for p in sorted(extra):lines.append(f'| `{short(p)}` | {du[p]["bytes"]/G:.3f} | {restore[p]} |')
lines+=['', 'docs35、docs38、docs49三组各22个原始二进制RPM已逐包读到并计算SHA，66/66与各自原始报告中的SHA一致，见 payload-original-rpm-sets.json。docs35目录另有1个源码RPM；初次数量检查把它计入而得到23，已按*.x86_64.rpm分开统计，见 rpm-count-correction.txt。原始RPM文件路径、大小及当前SHA在 [asset-catalog.tsv](../../tools/bolt/results/temp-cleanup-20261026/asset-catalog.tsv)。这里只认证原包仍在，不冒称本轮重新解包做了逐文件恢复认证。H=`archive-index-fix-rpm-20260923/baseline-rpm-extract`没有同等原包恢复证据，明确排除。', '', '稳妥方案不会把hybrid的19.736GiB缓存再加一次：它已经包含在hybrid gbs-root中。两轮cache-release根及hybrid+BOLT根的缓存已经释放，不按历史91GiB/20GiB再加。旧R1当前84.157GiB，明显小于31号记录175.75GiB；本轮只按实际读数，不推测外部操作。', '', '精确删除范围各自的最新后代文件时间、root属主/不可写目录计数与错误列表另见 scope-metadata.json；父目录的mtime不能代替两轮构建根各自的mtime。','', '## 4. 所有 >5 GiB 顶层范围逐项分析','', '“保留”行不计入可释放总量。含源码工作树的父目录即使有可删子树，也不整删。以下来源引用钉到本次核对的GitHub提交；同目录完整引用原文见 docs-grep.txt、doc-references.json，脚本引用见 scripts-grep.txt、script-references.json。', '', '| 路径 / GiB | 最新后代文件mtime（+08） | 所属线、来源、完成状态/出处 | 建议及理由 | 权限、依赖、小文件 |','|---|---|---|---|---|']
for r in rows:
 text=f"{r['line']}；{r['source_purpose']}；{r['completion']}。{cite(r['provenance'])}"
 deps=f"无可见进程/活动overlay；脚本引用{r['script_reference_count']}处；外部硬链接inode {r['external_hardlink_inodes']}；{r['permissions']}。已核验资产{r['asset_hash_rows']}条（含输入/RPM/报告），见catalog；不等于都应新增保存。"
 lines.append(f"| `{short(r['path'])}`<br>{r['bytes']/G:.3f}{'†' if r['blind'] else ''} | {r['latest_file']} | {text} | **{r['advice']}**：{r['reason']} | {deps} |")
lines+=['', 'W/llvm（源码仓库）也超过5GiB，但明确不在清理范围，最新后代普通文件见 source-latest-file.json。拟删GBS根内的LLVM是已导出的构建输入副本，不是独立Git工作树；保留的W/llvm及temp中的source工作树不动。W/docs、W/tools、W/.git、所有识别出的Git工作树及源码仓库都保留；每个大目录的git_roots和精确权限计数在 inventory.tsv/metadata.json。', '', '### 4.1 >50 GiB父目录再展开一层','', '| 父目录 | 直接子目录 | 实占GiB |','|---|---|---:|']
for parent in [x for x in u if x['group']!='W' and x['bytes']>50*G]:
 for s in sorted([x for x in sub if str(Path(x['path']).parent)==parent['path']],key=lambda x:-(x['bytes'] or 0)):
  lines.append(f"| `{short(parent['path'])}` | `{Path(s['path']).name}` | {(s['bytes'] or 0)/G:.3f}{'†' if s['rc'] else ''} |")
lines+=['', '深入build/、lto.cache、RPMS、SRPMS和BUILDROOT的独立du全部在 subunits.json。它们是解释父目录组成的重叠数据，不能累加成“清理收益”。','', '## 5. 必须保留、需要先保全的小资产','', '- `T/runpath-fix-20261026/`：当前不存在；一旦创建整目录保留，不推断其任务已结束。', '- `T/bolt-on-hybrid-20261024/products/`（3.886GiB）、`T/bolt-v4-20261022-cache-release/{baseline-products,revised-products}/`（各11.248GiB）：整体保留，RUNPATH/RPM比较仍要用。', '- `T/bolt-v4-20261021-disk-footprint/` 的gbs_llvm_qb1202084.conf和build.conf整体保留。固定快照配置及build.conf实际SHA见catalog；build.conf预期e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945。', '- 90份TU：`T/hybrid-local-20261023/tu-inputs/`，以及旧validation/bench_results资产；34号C输入`T/perf-c-o2-os-20261025/inputs/`和C++ .ii原件全部保留。perf父目录本次整体保留，包括测量脚本所用槽位/对象；不因报告已发布自动删除原始数据。', '- profile/Source1200原件、`W/tools/collect_bolt_profile.py`、`extend_bolt_profile_aarch64.py`、final_bolt_calibration_plan.json及训练/留出清单保留；bench_results整体保留。所有*.fdata及clang-bolt-v2.fdata.xz的本轮SHA见catalog。源码仓库中的同名Source也不会删除。', '- **新增保全前提**：34号通过hybrid+BOLT根的Tizen loader/运行库和build/lib64/clang/22运行。删除该gbs-root前，先保全 runtime-preservation.json 的8个运行库路径/符号链接布局及整个resource-dir，并在将来重测时显式重定向路径；本轮未复制、未改脚本。旧R1、ARM32/64 sysroot仍保留。', '', '### 5.1 已有同SHA副本与需要补存的清单','', '完整逐文件表：[asset-catalog.tsv](../../tools/bolt/results/temp-cleanup-20261026/asset-catalog.tsv)（路径、大小、SHA、同SHA其它路径）；本次删除范围对应的动作与保全预算：[preserve-before-delete.json](../../tools/bolt/results/temp-cleanup-20261026/preserve-before-delete.json)。副本判断不只比文件名；同inode复用SHA时也核对size/mtime，来源记录在asset-hashes-inode-aliases.json。仅列少量关键二进制如下：','', '| 保留文件 | 字节数 | SHA256 | 副本/结论 |','|---|---:|---|---|']
for a in allassets:
 p=a['path']
 if (('baseline-products/binaries/' in p or 'bolt-on-hybrid-20261024/products/binaries/' in p) and Path(p).name in ['ordinary-clang-22','clang.candidate','llvm-bolt']):
  copies=[q for q in dups[a['sha256']] if q!=p];lines.append(f"| `{short(p)}` | {a['bytes']} | `{a['sha256']}` | 已实测同SHA其它路径{len(copies)}个；本文件明确保留 |")
lines+=['', '每个大目录匹配的资产数量已列在第4节，catalog保留完整路径而非只列上述示例。对未核验到独立小资产的旧转换目录，不宣称“报告够了即可删”；225个归档/bitcode可能就是原始复现输入，列为保留待用户判断。', '', '### 5.2 旧脚本、overlay与硬链接','', '当前所有可读mountinfo未出现指向本范围的lowerdir/upperdir/workdir，findmnt也无残留项目挂载。磁盘上的旧overlay脚本不因此失效：旧解析upper仍依赖原下层才可挂回，方案只删除upper-parse，不删除其下层。所选新根的脚本引用未发现其它overlay把它们作为lowerdir；一般历史脚本直接引用仍存在，已逐行存证，未来重跑须先恢复/改指保全路径。搜索覆盖docs和分析脚本，不对LLVM源码/系统树做全量文本grep；未做任意程序的动态依赖证明，变量拼接和外部程序引用仍需执行前复核。', '', 'external-hardlinks.json列出每个大目录的外部链接inode、已定位其它路径和未定位链接数；源库/导出的Git对象有硬链接不等于能独立回收。两套精确删除范围未出现跨范围存活链接扣减，但这是当前可见元数据，实际执行前仍须复核。', '', '## 6. 不确定、需用户判断的目录','', '除第3节精确范围外，本轮不替主线废弃归档、release或ARM验证输入。特别是：','']
for r in rows:
 if '待用户判断' in r['advice']:lines.append(f"- `{short(r['path'])}`（{r['bytes']/G:.3f}GiB）：{r['reason']}；{cite(r['provenance'])}。")
lines+=['', 'W/temp内未识别出应归为M1的>5GiB独立目录；旧41号文档的M1工作树在W之外，不在本轮扫描范围，不能拿其它项目空间补本项目缺口。找不到准确源码提交或结束裁决的项目仍按未知处理。root属主本身不等于必需sudo，但表中有不可写目录/Permission denied的GBS根和upper-parse无法保证普通用户删干净；将来需用户另行授权，不绕过权限。', '', '## 7. 按分类与文件系统汇总','', '| 分类（只算精确不重叠范围） | /home | /var/tmp所在盘 |','|---|---:|---:|',f"| 先保存后删：4个新构建根，毛占用 | {plans['conservative']['home']['gross_du_bytes']/G:.3f} GiB | 0 |",f"| 上项先保全预算（扣减） | {plans['conservative']['home']['copy_budget_allocated']/G:.3f} GiB | 0 |",f"| 可以删除缓存（稳妥） | 0 | {plans['conservative']['var_tmp']['gross_du_bytes']/G:.3f} GiB |",f"| 可以删除载荷/旧upper（激进追加） | {(plans['aggressive']['home']['gross_du_bytes']-plans['conservative']['home']['gross_du_bytes'])/G:.3f} GiB | {(plans['aggressive']['var_tmp']['gross_du_bytes']-plans['conservative']['var_tmp']['gross_du_bytes'])/G:.3f} GiB |",'| 保留/不确定范围 | 可释放计0；不纳入清理收益 | 可释放计0；不纳入清理收益 |','', '方案是用户选择清单，不是执行脚本。尤其不要用父目录大小直接替代子范围预算。权限盲区、文件系统元数据、稀疏/复制分配以及其它进程写入会让最终df变化不同；实际清理时以保存成功、即时进程/挂载/引用核查、前后df为准。', '', '## 8. 原始材料与本轮边界','', '证据目录：`tools/bolt/results/temp-cleanup-20261026/`。包括du逐项stdout/stderr、完整下钻JSON、df、findmnt、lsof项目原文、fuser原文、所有命中行的rg输出、/proc挂载检查、元数据/权限、硬链接、资产SHA、重复副本和方案计算程序。lsof全主机原始输出与ps全命令行只留在本机同目录，不提交无关个人进程/文件列表；发布的lsof-project和lsof-final-project保留项目命中原文，NOFD可见性另列。', '', '未删除任何文件（包括看起来可重建的目录），未移动任何文件，未复制待保全产物，未改权限或全局Git配置，未提权、挂载/卸载、运行cmake/ninja或构建，未新建分支、未推Gerrit。仅更新bolt-v4盘点文档和证据。完成后等待用户逐项批准。','']
(B/'docs/bolt/38_temp_cleanup_inventory.md').write_text('\n'.join(lines))
print('report rows',len(rows),'home available',avail['home'],'plan net',plans['conservative']['home']['net_reclaim_estimate'])
