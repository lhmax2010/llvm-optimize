"""Append the completed continuation report without rewriting existing sections."""
from common import *
import statistics,math,datetime

def get(name):return json.loads((E/name).read_text())
def lines(name):return [json.loads(s) for s in (E/name).read_text().splitlines()]
def gm(v):return math.exp(statistics.mean(math.log(x) for x in v))
def link(name,label=None):return '['+(label or name)+'](../../tools/bolt/results/runpath-fix-20261026/continue/'+name+')'

def aggregate(mode):
 original=lines(mode+'/samples.jsonl');repeat=lines(mode+'-quiet-repeat/samples.jsonl')
 excluded={3,4} if mode=='threeway' else {0}
 rows=[r for r in original if r['round'] not in excluded]+repeat
 assert len(rows)==1200 and all(r['rc']==0 and r['byte_equal'] for r in rows)
 roles=sorted({r['role'] for r in rows});cases=get(mode+'/cases.json');metric='wall_s' if mode=='threeway' else 'max_rss_KiB';per=[]
 for i,c in enumerate(cases):
  samples={r:[x[metric] for x in rows if x['role']==r and x['index']==i] for r in roles};assert all(len(v)==5 for v in samples.values())
  med={r:statistics.median(v) for r,v in samples.items()}
  per.append({'index':i,'language':c['language'],'target':c['target'],'name':c['name'],'medians':med,'ratios':{r:med[r]/med['ordinary'] for r in roles if r!='ordinary'}})
 summaries=[]
 for language,target in sorted({(x['language'],x['target']) for x in per}):
  part=[x for x in per if (x['language'],x['target'])==(language,target)]
  summaries.append({'language':language,'target':target,'files':len(part),'metric':metric,'ratios':{r:gm([x['ratios'][r] for x in part]) for r in roles if r!='ordinary'}})
 values=[c[k]['loadavg'].split()[:3] for c in rows for k in ('before','after')]
 condition={'load1_min':min(float(v[0]) for v in values),'load1_max':max(float(v[0]) for v in values),'frequencies_kHz':[min(int(c[k]['frequency_kHz']) for c in rows for k in ('before','after')),max(int(c[k]['frequency_kHz']) for c in rows for k in ('before','after'))]}
 result={'PASS':True,'compiles':len(rows),'metric':metric,'original_samples_preserved':len(original),'repeat_samples':len(repeat),'excluded_original_rounds_due_to_environment':sorted(excluded),'per_file':per,'summary':summaries,'conditions':condition}
 save(E/(mode+'-quiet-final.json'),result)
 text='language\ttarget\tname\t'+ '\t'.join(roles)+'\t'+ '\t'.join(r+'/ordinary' for r in roles if r!='ordinary')+'\n'
 for x in per:text+='\t'.join([x['language'],x['target'],x['name'],*[str(x['medians'][r]) for r in roles],*[str(x['ratios'][r]) for r in roles if r!='ordinary']])+'\n'
 (E/(mode+'-medians.tsv')).write_text(text)
 return result

assert get('result.json')['status']=='ok' and get('quiet-result.json')['status']=='ok'
assert get('controller-result.json')['status']=='ok' and get('quiet-controller-result.json')['status']=='ok'
a=aggregate('threeway');rss=aggregate('rss');native=get('native-audit.json');assert native['PASS'];assert get('elf-literal-bytes.json')['PASS']
rpms=get('rpm-comparison/summary.json');assert len(rpms)==23 and all(r['PASS'] for r in rpms)
old=get('oldtext-result.json');elf=get('elf-comparison.json')
for name in ('objects-current/result.json','objects-oldtext/result.json'):assert get(name)['passed']==90
resources=lines('resources.jsonl')+lines('quiet-resources.jsonl');peak=max(int(x.get('memory.peak','0')) for x in resources);disk=min(x['free'] for x in resources)
for x in resources:
 for s in x.get('memory.events','').splitlines():
  k,v=s.split();assert k not in ('oom','oom_kill') or int(v)==0
assert disk>=20*1024**3
src=D/'source';head=subprocess.check_output(['git','-C',str(src),'rev-parse','HEAD'],text=True).strip();assert head=='ac112ebfd6e7983bdfd4c38dd156e6baba72731b';assert not subprocess.check_output(['git','-C',str(src),'status','--porcelain'],text=True).strip()
identity={'head':head,'tree':subprocess.check_output(['git','-C',str(src),'rev-parse','HEAD^{tree}'],text=True).strip(),'clean':True,'spec_sha':sha(src/'packaging/llvm.spec'),'helper_sha':sha(src/'packaging/clang-bolt-helper.py'),'profile_sha':sha(src/'packaging/clang-bolt-v2.fdata.xz'),'candidate_sha':sha(P/'binaries/clang.candidate'),'ordinary_sha':sha(WORK/'ordinary-clang-22')};assert identity['candidate_sha']==old['current_candidate_sha256'];save(E/'final-identity.json',identity)
save(E/'final-resources.json',{'peak_bytes':peak,'minimum_home_free_bytes':disk,'OOM':False,'MemoryMax':get('controller-result.json')['MemoryMax'],'swap_max':max(int(x.get('memory.swap.current','0')) for x in resources)})
count_dates=sum(len(r['ar_date_differences']) for r in rpms);unique_dates=len({x['path'] for r in rpms for x in r['ar_date_differences']})
size_delta=old['current_bytes']-old['candidate_bytes']
out='''\n\n## 10. 续跑验收（2026-10-27；用户批准 ar 日期差异单列）\n\n'''
out+=f"23 个 RPM 全部按本次口径通过：允许的内容变化只有 clang-22，以及源码包的 spec/helper；另有 {count_dates} 个包内归档条目只有内部日期不同，单列而不计为内容相同。最终 candidate 和 old-text candidate 分别通过 90/90 个完整对象逐字节比较。`-use-old-text` 把 clang 从 {old['current_bytes']:,} 缩到 {old['candidate_bytes']:,} 字节，减少 {size_delta:,} 字节（{size_delta/old['current_bytes']:.2%}）；old-text 相对现行参数的编译耗时变化为 {min(x['ratios']['oldtext']/x['ratios']['candidate']-1 for x in a['summary']):+.2%} 至 {max(x['ratios']['oldtext']/x['ratios']['candidate']-1 for x in a['summary']):+.2%}，最终 BOLT candidate 相对 ordinary 的最大 RSS 降低 {min(1-x['ratios']['candidate'] for x in rss['summary']):.2%}–{max(1-x['ratios']['candidate'] for x in rss['summary']):.2%}，具体语言/目标见下表。\n\n"
out+='本节是对第7、9节历史停止记录的续跑补充，之前的失败事实和原文不改。本地源码提交仍为 `'+head+'`，没有重新构建，没有修改 spec/helper/Source1200/发布 OPTIONS/白名单，没有推送 Gerrit 或 sandbox。\n\n'
out+='### 10.1 输入身份与 RPM 口径\n\n'
out+='当前 products 的 SHA256SUMS **35/35** 通过；对照 products 不存在 SHA256SUMS，使用33号任务已提交的 `preserved-products.json` 核对 **32/32** 原件。见 '+link('preflight.json')+'、'+link('new-products-sha.json')+'、'+link('old-products-sha.json')+'、'+link('input-identities.json')+'。本轮根的 BUILDROOT 已被 GBS 的 `%clean` 清理，本次没有重建它：从保留 RPM 只读解析载荷，差异归档解到本次新的 continue-work 子目录。\n\n'
out+='比较脚本只在结果目录：'+link('compare.py')+'、'+link('rpm_io.py')+'。三项条件同时成立才判 `allowed-ar-date-difference`：成员名单/顺序一致；逐成员内容 SHA 一致；把两个文件相同 ar header 偏移16起的12字节日期字段屏蔽后，其余**全部字节**一致（含索引、名称表、填充和非日期 header 字段）。独立自测2项通过，第二项同时覆盖成员内容变化和非日期 header 字节变化必须 FAIL：'+link('ar-selftests.txt')+'。未改生产门禁。\n\n'
out+='| RPM | 允许的内容变化数 | 载荷 mtime 变化数 | 允许的 ar 内部日期差异数 | 结果 |\n|---|---:|---:|---:|---|\n'
for r in rpms:out+=f"| {r['rpm']} | {len(r['content_changes'])} | {len(r['payload_mtime_changes'])} | {len(r['ar_date_differences'])} | PASS |\n"
out+=f"\n日期差异共 {count_dates} 个包内条目、{unique_dates} 个独立路径；同一 libarcher_static.a 出现在两个包中，按包各计一次。完整清单、旧新 SHA、每个归档的成员与日期范围见 "+link('rpm-comparison/summary.json')+' 及同目录逐包 JSON。没有新增、删除或其它未许可内容变化；RPM 整包 SHA 不同，不能称 RPM 二进制相同。载荷 mtime 与归档内部日期是两个独立计数。\n\n'
out+='### 10.2 两份 clang 的直接 ELF 比较\n\n'
out+=f"aa637c1 candidate `{elf['old_sha']}` 与本轮 `{elf['new_sha']}` 文件大小均为 {elf['size']:,} 字节，程序头、节头完全相同。除 `.dynstr` 和 `.dynamic` 两个区域以外，按1MiB块直接逐字节比较 PASS（不是仅比较代码节或 SHA）。见 "+link('elf-literal-bytes.json')+'、'+link('elf-comparison.json')+'。\n\n'
out+='`.dynamic` 原始 `(tag,value)` 序列的差异列表为空；其 DT_RUNPATH 指向的字符串发生以下变化，所以解码后的动态标签只差 DT_RUNPATH，DT_RPATH 两者均不存在：\n\n```text\nold DT_RUNPATH = '+elf['decoded_path_tags']['old']['DT_RUNPATH']+'\nnew DT_RUNPATH = '+elf['decoded_path_tags']['new']['DT_RUNPATH']+'\n```\n\n'
out+=link('elf-old-dynamic.txt')+'、'+link('elf-new-dynamic.txt')+' 保留 readelf 原文。\n\n'
out+='### 10.3 90 TU、old-text 重写与匹配\n\n'
out+='最终 candidate 对本轮 ordinary **90/90 PASS**；old-text 对本轮 ordinary 另做 **90/90 PASS**。都是30个历史条目×3目标，同一实体路径依次放置编译器；完整 `.o` 比较，保留 `.GCC.command.line`，没有去节或规范化对象。使用已预处理输入与记录参数，显式 `--no-default-config`，运行库、loader、resource-dir 全部来自本轮根；目标 sysroot 只读。见 '+link('objects-current/result.json')+'、'+link('objects-oldtext/result.json')+'、'+link('objects.py')+'。\n\n'
out+=f"重链输入仍在，SHA `{old['input_sha256']}` 与记录相同；没有重链。只在发布 OPTIONS 后加 `-use-old-text`，用本轮工具 `{old['tool_sha256']}` 重写并按原方法 strip-all，输出全部放 `temp/runpath-fix-20261026/old-text/`。最终实验 SHA `{old['candidate_sha256']}`。\n\n"
out+='| 指标 | 结果 |\n|---|---:|\n'
for k in ('N','M','S','U','Q'):out+=f"| {k} | {old['counts'][k]} |\n"
out+=f"| R | {old['counts']['R']*100:.10f}% |\n| S/N | 0 |\n| BOLT 耗时 | {old['seconds']:.3f} s |\n| BOLT 最大 RSS（/usr/bin/time -v） | {old['max_rss_KiB']:,} KiB |\n| strip-all 后大小 | {old['candidate_bytes']:,} B |\n\n"
out+='R≤5%、S=0，身份/ELF/strip 检查通过。见 '+link('oldtext-result.json')+'、'+link('oldtext-bolt.log')+'、'+link('oldtext-bolt.time')+'。实验产物按本项要求只执行重写及 strip-all，没有额外运行发布流水线的 RUNPATH 修补；三方均通过本轮根的显式 loader/--library-path 使用同一套运行库。实验产物没有替换发布 candidate，不是可直接发布的替代包；是否采用 old-text 仍由用户决定。\n\n'
out+='### 10.4 三方 -O2 编译耗时（五次中位数后几何平均）\n\n'
out+='每种语言/目标20个文件；普通、现行参数、old-text 三方，每侧5次；CPU2、单并行、setarch -R（personality=00040000）、同一实体路径和 inode；复制/fsync/SHA 不计入计时。monotonic_ns 围绕实际子进程 wait，独立超时线程。所有测量 `.o` 也做完整逐字节比较。\n\n'
out+='测量期间另一会话启动了 Git index-pack，约16:17–16:35与原始三方第4/5轮、RSS第1轮重叠；本会话的一次范围过大的只读指令文件查找也在 RSS 第1轮内终止。未终止其它会话进程，原始样本全部保留；等它结束并完成第一序列后，整轮补测三方第4/5轮、RSS第1轮，不按数值选择或删除异常点。主表用不重叠的完整5轮；原始整批结果另存，不能混称为无干扰测量。时间边界近似，进程退出前未取得精确 /proc 起止；为此保守重测整个轮次。见 '+link('interference.json')+'、'+link('threeway/result.json','原始三方结果')+'、'+link('rss/result.json','原始RSS结果')+'、'+link('quiet-resources.jsonl','补测进程/资源记录')+'。\n\n'
out+='| 语言 | 目标 | 现行/ordinary | old-text/ordinary | old-text/现行 |\n|---|---|---:|---:|---:|\n'
for r in a['summary']:out+=f"| {r['language']} | {r['target']} | {r['ratios']['candidate']:.6f} | {r['ratios']['oldtext']:.6f} | {r['ratios']['oldtext']/r['ratios']['candidate']:.6f} |\n"
out+='\n比值<1表示更快。含干扰的原始批次中，ARM的 old-text/现行比约为1.0167（C）和1.0146（C++），而安静整轮补测后的主表方向反转；这说明该小量级差值对测量条件敏感。原始批次不作为安静环境结论，但完整保留。微小差值不等同统计显著；本实验没有给置信区间，也不能把所有波动归因于代码布局。主表的逐文件5次中位数与全部比值：'+link('threeway-medians.tsv')+'；汇总及样本选择规则：'+link('threeway-quiet-final.json')+'。补测原样样本：'+link('threeway-quiet-repeat/samples.jsonl')+'；初次原样样本：'+link('threeway/samples.jsonl')+'。\n\n'
out+='### 10.5 运行时内存（最大 RSS）\n\n'
out+='C/C++各20文件×3目标，ordinary/最终candidate各5次，共1200次有效测量。每次以宿主 `/usr/bin/time -v` 包裹单个编译器调用，读取 Maximum resident set size (kbytes)，单位KiB；这是进程峰值RSS，不是cgroup峰值或私有页数。逐文件取5次中位数，再对 candidate/ordinary 取几何平均。\n\n'
out+='| 语言 | 目标 | candidate/ordinary 最大RSS比 | 变化 |\n|---|---|---:|---:|\n'
for r in rss['summary']:
 v=r['ratios']['candidate'];out+=f"| {r['language']} | {r['target']} | {v:.6f} | {(v-1)*100:+.3f}% |\n"
out+='\n逐文件中位数：'+link('rss-medians.tsv')+'；汇总：'+link('rss-quiet-final.json')+'；每次 `/usr/bin/time -v` 原文保存在 rss/logs 和 rss-quiet-repeat/logs，输入、argv、前后load与CPU频率在两组 samples.jsonl。old-text 的编译RSS不在本项对比范围，未由文件大小推算。\n\n'
out+='### 10.6 45 个 native 跳过归档的逐成员核对\n\n'
out+=f"原证据 tar 中 summary 与根内 native-archive-conversion/summary.json 字节相同。安装前270个 `.a` 减去明确转换的225个路径，得到45个 native跳过路径；它们与 compiler-rt 包日期不同的45项集合完全相同。全部 {native['members']} 个实际成员均为 ELF64 little-endian ET_REL、EM_X86_64；bitcode=0，其它类型=0（ar索引/长文件名表是容器元数据，不作为对象成员）。构建原件SHA与 install-before 快照相同，原件和包内成员分别检查类型；平台 strip 前后成员内容是否不同另存，未把原件与打包文件误说为SHA一致。\n\n"
out+='跳过的45个归档路径如下（与compiler-rt日期差异集合逐项相等）：\n\n```text\n'+'\n'.join(native['paths'])+'\n```\n\n'
out+='名单与逐成员SHA/类型：'+link('native-skipped-members.json')+'；集合推导：'+link('native-audit.json')+'、'+link('native-evidence-match.json')+'。\n\n'
out+='本轮 llvm-readelf 抽查原文：'+link('libclang_rt.builtins-x86_64.a.readelf.txt')+'、'+link('libclang_rt.asan-x86_64.a.readelf.txt')+'；全部列出 Type: REL、Machine: Advanced Micro Devices X86-64。\n\n'
out+='### 10.7 资源、保全与边界\n\n'
out+=f"所有编译和重写由 systemd 用户服务运行，MemoryMax={get('controller-result.json')['MemoryMax']:,} B（MemTotal减8GiB）、MemorySwapMax=0、nice10、ionice2/7；观测总cgroup峰值 {peak:,} B，最小 /home 可用 {disk:,} B，OOM/oom_kill=0，swap=0。资源每5秒采样，不冒充连续磁盘最低值。补测期间进程快照与采样完整保留。\n\n"
out+='两种有效数据集的负载/频率范围：\n\n| 数据集 | load1最小–最大 | CPU2频率kHz最小–最大 |\n|---|---:|---:|\n'
for label,r in [('三方',a),('RSS',rss)]:c=r['conditions'];out+=f"| {label} | {c['load1_min']}–{c['load1_max']} | {c['frequencies_kHz'][0]}–{c['frequencies_kHz'][1]} |\n"
out+='\n调频策略/驱动和CPU原文见各 conditions.json。所有argv、stdout/stderr、逐步耗时、资源记录和结束标记在 '+link('steps.json')+'、'+link('quiet-steps.json')+'、'+link('final-resources.json')+'、'+link('runpath-verify.log')+'、'+link('quiet-runpath-verify.log')+'。补测控制器在尚未开始任何补测时修正了一次前置结果文件路径，见 preparation-notes.txt；只终止了等待锁的本会话控制器并重启，未影响正在运行的测量。只读查找修正和干扰处理如上；没有产品门禁失败后放宽标准。\n\n'
out+='本轮根、products、continue-work、old-text全部保留。最终源码HEAD/tree/clean与二进制身份见 '+link('final-identity.json')+'。只提交文档和测量证据到 GitHub bolt-v4；没有新源提交、没有Gerrit/sandbox推送，不操作QB。\n\n'
out+='**总结论：本次用户裁决口径下23包、两组90 TU、ELF限定差异和45归档类型核对全部PASS；old-text大小/速度与普通对最终candidate的RSS测量已完成，发布源码ac112ebf保持不变，是否采用old-text仍待用户决定。**\n'
doc=E.parents[4]/'docs/bolt/37_runpath_and_improvements.md'
# E=repo/tools/bolt/results/runpath-fix/continue; parents[4] is repo.
assert doc.exists(),str(doc)
oldtext=doc.read_text();assert '## 10. 续跑验收（2026-10-27' not in oldtext
original=subprocess.check_output(['git','show','HEAD:docs/bolt/37_runpath_and_improvements.md'],cwd=E.parents[4]);assert doc.read_bytes()==original
with doc.open('a') as f:f.write(out)
status=E.parents[4]/'docs/bolt/STATUS.md'
with status.open('a') as f:
 f.write('\n\n## RUNPATH续跑验收（2026-10-27）\n\n用户裁决：仅当ar成员名单/顺序、逐成员SHA、日期字段外全部字节均一致时，允许内部日期差异；单列统计，不并入内容相同。此规则仅在结果目录比较脚本中实施，发布spec/helper不变。\n\n23RPM PASS：clang-22及源码spec/helper为允许内容变化；271个包内条目（270独立路径）的ar日期差异单列。最终candidate和old-text各90/90对象一致，45个native跳过归档全部成员为x86_64 ELF ET_REL、无bitcode。old-text体积减少30,691,864B（16.75%），三方速度及六组RSS已完成；Git解包干扰轮次完整保留并整轮补测，详见[37号第10节](37_runpath_and_improvements.md#10-续跑验收2026-10-27用户批准-ar-日期差异单列)。\n\n源码ac112ebfd6e7983bdfd4c38dd156e6baba72731b保持clean；没有重构建、改发布参数、删除根、创建分支或推送Gerrit/sandbox。old-text是否采用仍待用户决定。\n')
print('APPENDED_REPORT_PASS')
