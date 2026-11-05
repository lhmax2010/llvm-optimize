from pathlib import Path
import json,gzip,collections,datetime,re,subprocess,os
E=Path(__file__).resolve().parent;B=E.parents[3];W=Path('/home/linhao/Toolchain/development/llvm-optimize');T=W/'temp';N=json.loads((E/'targets.json').read_text());G=2**30
j=lambda p:json.loads(p.read_text())
inv={n:j(E/n/'inventory.json') for n in N}
source={
N[0]:('BOLT v2旧认证根R1；f111162e普通/重链/插桩工具来源。16号当时插桩与优化成功，正式ARM耗时降低15.396%；59号本日仍复用其merge-fdata/runtime。','main/docs/16_bolt_final.md:3–40；docs/bolt/59_pgo_bolt_followup.md:73–82'),
N[1]:('Rnew：x86静态归档修复及llvm-strip验证环境；docs35完成22 RPM和225开发归档验收，docs38/51继续研究GNU/LLVM strip差异；不是新的QB同快照基线。','main/docs/38_llvm_strip_x86_64.md:27；main/docs/40_arm_archive_conversion_stage1.md:75；docs/bolt/31_build_root_inventory.md:94–96'),
N[2]:('ARM TLS/Thumb修复和两架构全量转换/消费者实验；210/212档转换及原消费者/strip证据是后续回归对照。','main/docs/40_arm_archive_conversion_stage1.md:2051–2209、2490–2578；main/docs/49_x86_build_resume_result.md:262–284'),
N[3]:('ARM Source与根内约束探针；保留三架构转换结果、TLS/module-asm探针及原始诊断。','main/docs/44_arm_source_review_round1.md:27；main/docs/46_review_round3_package.md:19'),
N[4]:('ARM第一阶段的x86不变性回归；225归档转换PASS，ARM环境阶段随后独立推进。','main/docs/40_arm_archive_conversion_stage1.md:55–118；main/docs/46_review_round3_package.md:20'),
N[5]:('C0新根路由/极小包、C1原源码导出与accel输入；两个C0通过，旧导出校验错误保留，后续标准构建在其他根继续。','main/docs/40_arm_archive_conversion_stage1.md:627–844'),
N[6]:('ARM32标准-bc构建、bitcode/原生成员普查及首次转换停止现场；后续TLS/Thumb方案在C1目录完成复验。','main/docs/40_arm_archive_conversion_stage1.md:1170–1242'),
N[7]:('两轮ThinLTO cache-release完整构建；32号记录两轮candidate和RPM验证。两个GBS根已按38号后续清理，本目录主要是两套products及保全/报告。','docs/bolt/32_cache_release.md；docs/bolt/38_temp_cleanup_inventory.md:121–143及第9节'),
N[8]:('42号objcopy only-keep-debug崩溃根因和GNU/eu-strip方案矩阵；函数级方案通过，源码行方案因没有带DWARF重链输入未测。','docs/bolt/42_crash_localization_rootcause.md:3–32及第4–8节'),
N[9]:('41号普通/最终/符号表版clang崩溃栈与15TU实验；发现LLVM only-keep-debug SIGSEGV，之后由42/43号推进。','docs/bolt/41_crash_localization_probe.md:3–16'),
N[10]:('docs35最终22 RPM、225开发归档和45 compiler-rt验证、独立安装和消费者；原始RPM与本地测试包仓库保留。','main/docs/STATUS.md:21、258–267；main/docs/35_archive_fix_v2_final.md'),
N[11]:('6e9d4f2 hybrid源码内网交接：shallow Git归档、5个分片、GBS导出缩写/标签/恢复验证。GitHub release已由原文记录发布；本次不重新下载或重建。','main/docs/llvm_optimize_intranet_fetch.md:1–50'),
N[12]:('46号scm/meta/qb两评审的依赖、MLGO与1030仓库spec审计；最终上传359363/359364，构建配置拼接仍需后续QB确认。这里只分析旧证据，不查询QB或评审新状态。','docs/bolt/46_qb_meta_toolchain_switch.md:540–670')}

def link(f):return '../../tools/bolt/results/disk-review-group2-20261105/'+f

def readfiles(n):
 with gzip.open(E/n/'files.jsonl.gz','rt') as f:
  for l in f:yield json.loads(l)

def byteval(d):
 try:return int(d['du']['stdout'].split()[0])
 except (KeyError,ValueError,IndexError):return None

def fmt(b):return 'UNKNOWN' if b is None else f'{b/G:.3f} GiB ({b:,} B)'
# Only independently hashed identical files qualify, even if the group scan timed out.
archive=j(E/'archive-copy-comparison.json') if (E/'archive-copy-comparison.json').exists() else []
duplicate_proof={x['path']:x['other'] for r in archive for x in r['files'] if x['equal']}
remove={n:[] for n in N};why={}
for path,other in duplicate_proof.items():
 for n in N:
  if path.startswith(str(T/n)+'/'):remove[n].append({'path':path,'reason':'same-SHA duplicate; retained '+other})
# Re-extractable payload directories: original RPMs and all reports remain retained.
for n,subs,reason in [(N[7],['rpm-difference-analysis/baseline','rpm-difference-analysis/revised'],'32号提取脚本逐文件从保留的原始RPM解出；保留同级JSON报告'),(N[12],['mlgo/base/root','mlgo/toolchain/root'],'mlgo.py逐包rpm2cpio解包5个保留RPM；试验对象在root外')]:
 for sub in subs:remove[n].append({'path':str(T/n/sub),'reason':reason})
# Published, clean handoff clone and regenerable exports. Keep assets and local-only reports/scripts.
for sub in ['llvm','export-abbrev12','export-first','export-roundtrip-abbrev12','export-tag-upstream']:
 remove[N[11]].append({'path':str(T/N[11]/sub),'reason':'交接源码HEAD/refs已由Gerrit可达性核对，tracked clean；完整assets和导出/恢复证据保留'})
# Only object pairs whose full SHA agrees; binaries and symbolization matrices stay.
probe=j(E/'probe-binary-hashes.json') if (E/'probe-binary-hashes.json').exists() else []
pmap={x['path']:x for x in probe}
for path,x in pmap.items():
 p=Path(path)
 if p.parent==T/N[9] and p.name.startswith('tu-') and p.suffix=='.o':
  q=p.with_name(p.name.replace('tu-','ref-',1));y=pmap.get(str(q))
  if y and x['hash'].get('sha256') and x['hash']['sha256']==y['hash'].get('sha256'):
   remove[N[9]].append({'path':path,'reason':'逐字节SHA相同，保留 '+str(q)})
# Additional compiler copies: full SHA verified against retained products or symbols.
for x in j(E/'probe-external-duplicates.json'):
 if x['same_sha_retained_products'] and x['hash'].get('sha256'):
  remove[N[9]].append({'path':x['file'],'reason':'same-SHA retained product '+x['same_sha_retained_products'][0]+'; rerunning archived scripts requires restoring their path'})
a=pmap.get(str(T/N[9]/'same-clang'));b=pmap.get(str(T/N[9]/'clang.symbols'))
if a and b and a['hash'].get('sha256') and a['hash']['sha256']==b['hash'].get('sha256'):
 remove[N[9]].append({'path':a['path'],'reason':'same-SHA retained '+b['path']})
# Never infer deletability from filename alone when hash is unavailable.
summary=[]
for n in N:
 d=inv[n];chosen=remove[n];rr=[];keep=[];byinode=collections.defaultdict(list);allfiles=list(readfiles(n))
 # Include Git administration files for the one clone proposed for slimming.
 if n==N[11]:
  for base,ds,fs in os.walk(T/n/'llvm/.git',followlinks=False):
   for f in fs:
    p=Path(base)/f
    try:
     s=p.lstat();allfiles.append({'path':str(p),'size':s.st_size,'allocated':s.st_blocks*512,'dev':s.st_dev,'ino':s.st_ino,'nlink':s.st_nlink})
    except OSError:pass
 for x in allfiles:
  hit=next((c for c in chosen if x['path']==c['path'] or x['path'].startswith(c['path']+'/')),None)
  if hit:rr.append(dict(x,reason=hit['reason']));byinode[(x['dev'],x['ino'])].append(x)
  else:keep.append(x)
 free=sum(v[0]['allocated'] for v in byinode.values() if len(v)>=v[0]['nlink'])
 # Keep-size includes retained directory overhead; release excludes all directory metadata conservatively.
 total=byteval(d);status='瘦身' if free else '必须保留'
 result={'directory':n,'classification':status,'current_observed_bytes':total,'current_complete':d['du']['rc']==0 and not d['errors'],'retain_allocated_upper_bytes':None if total is None else total-free,'suggested_release_file_blocks':free,'candidate_files':len(rr),'candidate_paths':chosen,'hardlinked_inodes_not_counted':sum(len(v)<v[0]['nlink'] for v in byinode.values())}
 (E/n/'recommendation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 for fname,rows in [('retain-files.tsv.gz',keep),('suggested-files.tsv.gz',rr)]:
  with gzip.open(E/n/fname,'wt') as f:
   f.write('path\tbytes\tallocated_bytes\n')
   for x in rows:f.write(f"{x['path']}\t{x['size']}\t{x['allocated']}\n")
 summary.append(result)
refs=j(E/'reference-locations.json');remote=j(E/'git-remote-followup-v2.json');remote={x['repo']:x for x in remote}
text=['# 65：历史目录第二组只读盘点（2026-11-05）','',
'64号清理已经结束，本轮没有删除、移动、改写任何被分析文件，也没有运行构建或sudo。只把已核对的重复副本、可从保留RPM重新解包的载荷及已发布源码的临时导出列为瘦身候选；原始RPM、profiles、未发布探针提交、认证products和尚未归档的报告均保留。A/B存在权限盲区，不能把可读部分的du或Git扫描当成整根完整审计。','',
'## 1. 方法、边界与证据','',
'W为`/home/linhao/Toolchain/development/llvm-optimize`；目录均相对`W/temp/`。只读扫描使用nice19/ionice-c3；du整根180s、一级子目录90s、细分60s，sha256sum逐文件120s（小证据30s）。超时/权限错误原样保存，记UNKNOWN，不拿历史大小补值。证据写入本次结果目录；被检查目录未写入。64号结束行在[previous-finished.txt]('+link('previous-finished.txt')+')。',
'一级du是各子目录单独计算，可能重复计算共享硬链接，**不能直接相加**。建议释放量只算已确认候选的唯一文件数据块，若硬链接还有清单外名字则不计释放，不计目录元数据；不是删除后df实测。建议保留大小为本次du减这个保守文件块值，盲区目录仍只是可读下界。所有候选只是一份建议，未来实际操作前还须逐项授权并重新查占用/挂载/仓库依赖。',
'RPM清单包含所有可读命中的RPM，而不是只列LLVM包；每个文件的名字、大小、SHA、同SHA其他位置在各节链接的rpm.tsv。重复检索范围是W/temp可读目录与本次13个目录；全树索引限时480s，权限/超时见duplicate-candidate-index.json。未找到副本仅表示该范围内未证实，不冒充全盘唯一；未对所有旧自构建RPM逐个探测公开下载站，因此无法证明可下载的原始RPM一律保留。',
'引用检索覆盖main/bolt-v4的docs及tools中所有可读.py/.sh/.conf（含被gitignore的历史结果脚本），逐条文件与行号另列reference-index.md，完整命中原文gzip保留。55–63号中不存在的文档不造内容；生成报告/历史检查脚本的引用与仍会执行的入口应区别看待。路径无命中不等于任意动态拼接路径均已证明无依赖。',
'另读/proc的cwd/root/exe/fd，只见本轮扫描器打开目标文件，未见可见外部占用；有权限盲区，不能证明全机无占用，详见usage.json。未执行sudo。',
'Git按原要求保存branches/tags相对remote-tracking refs的日志，另查detached HEAD、stash ref、tracked status、worktrees/alternates；对LLVM再只读ls-remote核对Gerrit所有可见refs（含评审refs），只使用本仓库已存在的commit对象，不fetch、不改ref/config。首版stdin排除写法不正确，保留失败/中间结果；结论仅用git-remote-followup-v2.json及带^的排除查询。无远端的临时探针仓库按未发布保留，不宣称查询了不存在的全世界远端。','']
for i,n in enumerate(N):
 d=inv[n];s=summary[i];h=j(E/n/'hashes.json') if (E/n/'hashes.json').exists() else [];repos=j(E/n/'git-review.json');small=j(E/n/'small-evidence.json') if (E/n/'small-evidence.json').exists() else []
 label=('A','B','C1','C2','C3','C4','C5','D','E1','E2','F','G1','G2')[i]
 text += [f'## {i+2}. {label}：`{n}`','',source[n][0],f'出处：{source[n][1]}。','',f"当前du：**{fmt(s['current_observed_bytes'])}**"+('；有权限/扫描盲区，仅可读下界，完整值UNKNOWN。' if not s['current_complete'] else '；本目录遍历无权限错误。'),'','一级子目录（完整顶层文件和目录清单见inventory.json）：','', '|子目录|du GiB|类型/用途|','|---|---:|---|']
 for x in d['top']:
  if 'du' not in x:continue
  try:v=int(x['du']['stdout'].split()[0]);vs=f'{v/G:.3f}'
  except (IndexError,ValueError):vs='UNKNOWN'
  if x['du']['rc']:vs+='（盲区/失败，见原文）'
  kind='构建根/缓存（不等于可直接删除）' if x['name'] in ('local','gbs-root','BUILD-ROOTS','accel-check') else '认证/保全产物' if any(k in x['name'] for k in ('products','preserved','rpms')) else '实验输入、结果或辅助脚本；具体见文件清单'
  text.append(f"|`{x['name']}`|{vs}|{kind}|")
 text+=['',f"可读文件{d['file_count']:,}；RPM路径{len(d['rpms'])}；发现Git仓库{len(repos)}。扫描错误："+('无' if not d['errors'] else '；'.join(d['errors'])),'',f"全部RPM与副本核对：[rpm.tsv]({link(n+'/rpm.tsv')})；工具/profile/products等关键资产：[assets.tsv]({link(n+'/assets.tsv')})；全部文件元数据：[files.jsonl.gz]({link(n+'/files.jsonl.gz')})。",'']
 cs=j(E/'catalog-summary.json');cs=next(x for x in cs if x['directory']==n)
 text += [f"RPM本次SHA已取得{cs['hash_known']}/{cs['RPM_paths']}；UNKNOWN {cs['hash_unknown']}；{cs['verified_copy_paths']}个路径找到其他同SHA位置（包括同目录的其他名字，不等于可释放独立数据块）。未查到副本或超时的原包全部保留。",'']
 if repos:
  text+=['|仓库|HEAD|未发布候选/远端核对|stash|tracked改动|','|---|---|---|---|---|']
  for r in repos:
   z=remote[r['repo']];live=z.get('after_live_remote');count=live['count'] if live and live['rc']==0 else r['with_detached']['count'];note=f'{count}（Gerrit可见refs排除后）' if live and live['rc']==0 else f'{count}（无远端/未证实已发布，须保留）'
   head=r['head']['stdout'].splitlines()[0].removeprefix('commit ');stash='无' if z['stash_ref']['rc']==0 and not z['stash_ref']['stdout'] else '见原文/UNKNOWN'
   text.append(f"|`{r['repo']}`|`{head}`|{note}|{stash}|{r.get('status',{}).get('stdout','UNKNOWN').strip() or '无'}|")
 else:text.append('可读范围未发现Git仓库；若本节有权限盲区，不据此宣称盲区也没有仓库。')
 text+=['',f"顶层关键文本/脚本{len(small)}份，其中{sum(bool(x['tracked_same_name_same_sha']) for x in small)}份找到Git跟踪的同名同SHA副本；其余不推断已归档，一律纳入保留清单。逐文件路径/大小/SHA：[small-evidence.json]({link(n+'/small-evidence.json')})。",'']
 scripts=[x for r in refs if r['directory']==n and r['category'].endswith('scripts') for x in r['hits']]
 recent=[x for r in refs if r['directory']==n and r['category'].endswith('docs') for x in r['hits'] if re.search(r'/docs/bolt/(55|56|57|58|59|60|61|62|63)[^/]*\.md$',x['file'])]
 text += [f"当前引用检索：脚本{len(scripts)}处；55–63号文档{len(recent)}处。"+('该两类均无。' if not scripts and not recent else ''),f"逐条位置与原文：[reference-index.md]({link(n+'/reference-index.md')})。",'']
 reason={N[0]:'历史工具、普通clang/RPM和运行环境仍有引用；只有merge-fdata/runtime已证实复制到59号tools，不代表全部84GiB都已保全。权限盲区未消除，保留整根。A的lto.cache已不存在，不能再次按旧91.6GiB计算可释放量。',N[1]:'旧普通clang、工具/安装环境仍被归档和historical launcher引用；其RPM不是QB新快照同SHA的当然替代品。权限盲区未消除，保留整根；现lto.cache只有本次deep-sizes记录的大小。',N[2]:'保留ARM输入、完整已认证转换结果及消费者/strip证据，作为其他重复档的保留对照。不能因离线通过便删除未完成根内认证所需输入。',N[3]:'仅建议移除已逐文件SHA证实等于C1保留副本的归档；组检查超时未完成的其余档、members/summary、TLS/module-asm探针全部保留。',N[4]:'仅建议移除已逐文件SHA证实等于C1的归档副本；x86原始输入及全部文本证据保留。',N[5]:'两个C0最小包各有无远端的本地提交，需先保全源码；accel/导出/buildconfig仍是重搭ARM环境的输入，本轮不移动或导出备份。',N[6]:'唯一的ARM32原始输入、首次失败对象与标准构建日志仍用于ARM待办，保留。',N[7]:'保留baseline-products、revised-products、preserved-before-delete及全部报告/配置；只建议移除从原RPM提取的rpm-difference-analysis/baseline与revised，保留同级差异JSON。',N[8]:'保留objcopy缺陷的工具矩阵、两代BOLT重现副本、scheme-a及运行库。64号已删除输入构建根；没有证明全部矩阵可由仍存同SHA工具重建，不能按普通缓存处理。',N[9]:'建议移除与ref-N.o全SHA相同的tu-N.o副本、与oldtext保全products同SHA的clang.final/clang.ordinary，以及与clang.symbols同SHA的same-clang。保留ref对象、独有符号表版、脚本及报告；若重跑旧脚本，须从列出的保留副本恢复原路径。缺陷修复仍挂账，不删除独有重现输入。',N[10]:'两份消费者探针各有本地未发布提交，原始docs35 RPM需保留；rpms-docs35与continue中的硬链接使一级du不可相加，不能把重复名字当作可释放的8GiB。',N[11]:'远端核对无未发布提交、tracked clean/stash无；assets完整归档和5分片的当前SHA均与保留SHA256SUMS一致（6/6）；保留assets的完整归档/5分片、manifest、全部本地脚本与导出对照报告，只建议移除可恢复的llvm检出和4个export目录。未来删除前须再核对worktree/alternates反向依赖和远端状态。',N[12]:'保留10个原始RPM、所有日志/脚本/对象及second-specs；mlgo.py明确root只来自这5包解压，编译对象在root外，因此只建议移除两份mlgo/*/root。'}[n]
 text += [f"**结论：{s['classification']}。** {reason}",f"建议保留：[{n}/retain-files.tsv.gz]({link(n+'/retain-files.tsv.gz')})逐路径列出，{fmt(s['retain_allocated_upper_bytes'])}（与本节du相同盲区口径）。建议移除文件清单：[suggested-files.tsv.gz]({link(n+'/suggested-files.tsv.gz')})，共{s['candidate_files']}条；预计释放文件块 **{fmt(s['suggested_release_file_blocks'])}**。",'']
 if n in (N[0],N[1]):
  ds=j(E/'deep-sizes.json')
  text += ['构建目录细分：完整du原文见[deep-sizes.json]('+link('deep-sizes.json')+')。A的build/bin为46,543,589,376 B、build/lib64为14,953,287,680 B；B分别为48,569,888,768 B和14,804,201,472 B。A的lto.cache已不存在，B现存仅17,752,064 B；当前大户主要是工具二进制及构建对象，不能套用旧缓存97GB的估算。','']
 if s['candidate_paths']:
  text+=['候选边界/原因（文件级重复项完整列表在recommendation.json）：','']
  for x in s['candidate_paths'][:8]:text.append('- `'+x['path']+'`：'+x['reason'])
  if len(s['candidate_paths'])>8:text.append(f"- 其余{len(s['candidate_paths'])-8}条逐文件列于[recommendation.json]({link(n+'/recommendation.json')})；不能扩展为删除整个父目录。")
  text+=['']
# Dedicated factual investigation.
pc=j(E/'profile-correspondence.json');ps=j(E/'profile-semantic-comparison.json')
text += ['## 15. A：Source1200原始fdata与合并关系','',
'A根的可读文件中没有Source1200采集合并前的clang.PID.fdata；扫描到的.profraw/.profdata主要是LLVM源码测试夹具，不能误认成训练原件。历史docs16:31–40和docs20附录D:1395–1446定位原件于 **W/temp/bolt-measurement-20260918/run/profiles/**，不在A根内。',
f"13份ARM+10份AArch64共23文件，本次逐一SHA全部吻合原profile-work/result.json，合计{sum(x['size'] for x in pc['profiles']):,} B；原合并文件171,232,190 B，SHA `{pc['original_merge_hash']['sha256']}`，和源码Source1200解压SHA `{pc['source_uncompressed']['sha256']}`一致。原压缩Source1200 SHA为 `{pc['source_hash']['sha256']}`。",
'使用同SHA的22.1.8 merge-fdata只读重合并（stdout只哈希/比较，不改原件），未运行训练或构建。首次重合并SHA不同，不能写成逐字相同。源代码merge-fdata.cpp:341–371按线程DenseMap和StringMap输出，未排序；第二次逐完整行多重集比较（含所有计数）为：', '```json',json.dumps(ps,ensure_ascii=False,indent=2),'```',
'因此证实是同23输入、同计数内容，字节排列不固定；原已保存merged-v2.fdata与Source1200则仍逐字节同SHA。23原件、旧merged及清单都在本次分析清单外，必须继续保留。详见[profile-correspondence.json]('+link('profile-correspondence.json')+')、[merge-fdata-ordering.txt]('+link('merge-fdata-ordering.txt')+')。','',
'## 16. C：ARM静态库修复的最后状态与恢复输入','',
'最后明确的ARM实测是2026-10-14 main/docs/49_x86_build_resume_result.md §12–14（L262–339）；main/docs/50_archive_followup_review.md和main/docs/STATUS.md:833–857保留待办。ARM32 210档/3690成员（3683 bitcode+7原生）及AArch64 212档/3706成员（3699+7）离线全量PASS，各档after SHA与docs40§12相同，沿用消费者/strip证据。ARM32根内小试在挂载前因Exec format error/无ARM binfmt停止，Source未运行；不能称为两ARM安装/打包已认证。',
'待办事实：ARM根内生产限制/64MiB负例及后续打包；两种架构原生shell/AS读回；14文件bash债务与LLVM23多行IR重新认证。是否继续、是否重新授权GBS初始化binfmt及mmap_min_addr，由用户决定，本轮不改变环境。',
'恢复需保留：C1的aarch64-input、两架构转换/原生比较证据；C5的armv7l-input及原始失败对象；C3的x86-input；C4的c0-package两仓库、c1-export/c1-export-repository、buildconfig-from-W.conf、repositories和accel-check；main已冻结ARM候选Source SHA `1bac8db608554b35d16482711bf0667f1fbee8d60c6fc52f0f448d240ffaa9e4`及对应Commands/测试/补丁。旧配方固定Base-Toolchain 20261001.092726与Unified-Toolchain 20260814.092727，并不是今晚的QB 20261030快照；恢复时需核对可取得性，不能偷偷替换。',
'历史时间（事实，不是本次重搭承诺）：docs40:L820–827的两个C0为344.287/418.849s；ARM32完整-bc 1998.954s（L1217–1221），AArch64初始化104.799s及-bc 2321.728s（L2188–2203）；docs49:L274/284最新离线转换分别1787.344/1571.769s。可参考为两次旧环境-bc合计约72分钟、两次离线转换约56分钟，另加初始化/下载/调查；**从零重搭总耗时UNKNOWN**，没有完整ARM安装打包的实测时长，不据此估算。','',
'## 17. 汇总与需要用户决定的问题','',
'没有任何目录被判为可以整个删除。以下为本轮实证支持的保守瘦身建议；“保留”不是永久禁止，只表示尚无足够证据批准整项或更多内容删除。','',
'|目录|当前du GiB|结论|建议保留内容/大小 GiB|预计释放 GiB|用户需决定|','|---|---:|---|---|---:|---|']
keep_names={N[0]:'整根：普通clang、工具、27 RPM及证据',N[1]:'整根：工具、154 RPM及证据',N[2]:'整目录：ARM输入、认证转换及消费者',N[3]:'members/summary、探针及未核对归档',N[4]:'x86-input、全部报告及未核对归档',N[5]:'两本地探针仓库、导出与accel输入',N[6]:'ARM32输入、失败对象及日志',N[7]:'两套products、preserved和报告',N[8]:'全部复现矩阵、符号文件及运行库',N[9]:'clang.symbols、ref对象和全部报告',N[10]:'45 RPM、两探针仓库及报告',N[11]:'assets完整包/分片、manifest及报告',N[12]:'10 RPM、对象/脚本/报告、second-specs'}
questions={N[0]:'先消除权限盲区并另做工具/产物保全？',N[1]:'先消除权限盲区并另做原RPM保全？',N[2]:'是否继续ARM根内认证？',N[3]:'是否删除已核对的494份重复档？',N[4]:'是否删除已核对的215份重复档？',N[5]:'是否先备份两个本地探针提交？',N[6]:'是否继续ARM根内认证？',N[7]:'是否仅删除两份解包副本？',N[8]:'缺陷定位关闭前是否另做最小复现保全？',N[9]:'是否按清单删重复二进制/对象？',N[10]:'是否先备份本地探针并另盘RPM？',N[11]:'是否接受从assets恢复源码/导出？',N[12]:'是否仅删除两个MLGO解包root？'}
for s in summary:
 n=s['directory'];size=s['current_observed_bytes'];suffix='†' if not s['current_complete'] else ''
 text.append(f"|`{n}`|{size/G:.3f}{suffix}|{s['classification']}|{keep_names[n]}；{s['retain_allocated_upper_bytes']/G:.3f}{suffix}|{s['suggested_release_file_blocks']/G:.3f}|{questions[n]}|")
text += ['',f"预计可释放文件块合计 **{sum(s['suggested_release_file_blocks'] for s in summary)/G:.3f} GiB**；本轮实际释放 **0 B**。†表示权限盲区，数值只代表可读部分，完整占用UNKNOWN。候选清单没有包含任何原RPM、profile原件、认证products或未发布源码仓库。",'',
'本次仅提交65号报告、STATUS和本次证据到GitHub bolt-v4；没有删除/移动待分析内容，没有sudo、构建、Gerrit/sandbox推送或QB操作。']
text[4:4]=['文档引用基准：bolt-v4 `b3a20dd5377d3ddbadfe1c4e818086913dd2bbf9`；main `613fa5ee8703c14f56e0b682bf0910f639f48ec9`。本次共有528个RPM路径，525个取得SHA，3个限时超时记UNKNOWN。另对QB保留目录的39个RPM做大小筛选；已取得SHA的候选中仅1个同大小，SHA不同，没有证实同SHA替代包，见qb-size-candidate-check.json。','']
(B/'docs/bolt/65_disk_review_group2.md').write_text('\n'.join(text)+'\n')
(E/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print('report written',len(text),'lines')
