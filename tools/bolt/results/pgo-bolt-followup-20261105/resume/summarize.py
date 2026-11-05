from pathlib import Path
import json,statistics,hashlib,subprocess,os,math,datetime
E=Path(__file__).resolve().parent;B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=Path('/home/linhao/Toolchain/development/llvm-optimize');F=W/'temp/pgo-bolt-followup-20261105'
def j(p):return json.loads(p.read_text())
def save(n,v):(E/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
rows=[]
for phase in ('instrument','train','merge','optimize','speed'):
 stats=j(E/(phase+'-service')/'worker-result.json');ps=j(E/(phase+'-service')/'process-maxima.json');commands=j(E/phase/'commands.json');times=j(E/phase/'result.json');assert times['status']=='ok'
 top=max(ps,key=lambda r:r['VmHWM_bytes']);row={'phase':phase,'wall_s':times['wall_s'],'cgroup_peak_bytes':int(stats['stats']['memory.peak']),'process':top,'time_max_rss_bytes':max(r['max_rss_bytes'] for r in commands),'oom_events':stats['stats']['memory.events']};rows.append(row)
save('step-resource-summary.json',rows)
units=j(E/'speed/measurements.json');assert len(units)==207
per=[]
for u in sorted({x['unit'] for x in units}):
 row={'unit':u}
 for label in ('nonpgo-bolt','pgo','pgo-bolt'):
  rr=[x for x in units if x['unit']==u and x['compiler']==label];assert len(rr)==3
  row[label]={'median_wall_s':statistics.median(x['wall_s'] for x in rr),'max_rss_bytes':max(x['max_rss_bytes'] for x in rr)}
 per.append(row)
save('speed-unit-medians.json',per)
loads=[x for r in units for x in [r['load_before'][0],r['load_after'][0]]];save('speed-load-summary.json',{'load1_min':min(loads),'load1_max':max(loads),'note':'unbound CPU, default ASLR, sequential single TU; ordinary desktop activity not stopped'})
inventory=[]
for p in sorted(F.iterdir()):
 if p.is_symlink():continue
 files=[p] if p.is_file() else [q for q in p.rglob('*') if q.is_file() and not q.is_symlink()]
 inventory.append({'path':str(p),'files':len(files),'logical_bytes':sum(q.stat().st_size for q in files),'allocated_bytes':sum(q.stat().st_blocks*512 for q in files)})
save('experiment-footprint.json',inventory)
free=os.statvfs('/home');save('df-final.json',{'available_bytes':free.f_bavail*free.f_frsize,'time':datetime.datetime.now().astimezone().isoformat(),'df':subprocess.check_output(['df','-B1','/home'],text=True)})
profile=j(E/'optimize/profile-counts.json');sp=j(E/'speed/summary.json');instr=j(E/'instrument/output.json');opt=j(E/'optimize/output.json');merge=j(E/'merge/output.json');tools=j(E/'tools.json');fdata=sum(x['profile']['bytes'] for x in j(E/'train/profiles.json'))
peak=rows[3]['process']['VmHWM_bytes'];base=9931661312
report='''\n\n## 5. 2026-11-05 补齐工具后的实测（本节起为最新结果）\n\n用户本轮允许复用同版本工具，或缺失时在新目录构建两个目标。实际找到16号原采集工具，未运行cmake/ninja，也没有编译任何目标。原工具对应13号§1记录的源码提交`f111162e94aa48ed367c9d2c039456c70e7160ae`；其bolt树与`3ee2d847`均为`3b71c6953c01c28c95956fcf79906e4ed1fc052c`。对旧根bolt/实际1,154个文件逐个计算Git blob hash，与3ee逐个一致，额外文件0；CMakeCache版本和两个工具--version均为22.1.8。完整证据：resume/bolt-source-comparison.json、versions.json。\n\n旧工具根：`W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/`，只读；复制到`W/temp/pgo-bolt-followup-20261105/tools/`。\n\n|工具|原路径（相对build）|字节|复制前后SHA256|\n|---|---|---:|---|\n'''
for t in tools:report+=f"|{Path(t['copy']).name}|{'bin/merge-fdata' if 'merge-fdata' in t['copy'] else 'lib64/libbolt_rt_instr.a'}|{t['bytes']}|`{t['sha256']}`|\n"
report+='''\n### 5.1 输入、流程和边界\n\n继续使用§1已核对的D根reference-relocs-clang-22副本及D根llvm-bolt副本；输入SHA再次核对一致。插桩参数直接沿16号§4，只换本次路径；通过D根loader和运行库启动，不chroot。23份训练输入逐个核对training.json的SHA，13 ARM+10 AArch64，保留清单的完整编译参数（真实TU含-O3，3个合成TU为-O2）；resource-dir和sysroot也按该清单原样使用。每次编译前后清点fdata，要求恰好新增1个非空文件；23/23通过。原来采集也是BOLT插桩，不是perf。\n\n没有改Source1200或发布OPTIONS。正式优化完整argv见resume/optimize/bolt-optimize.argv.json；使用3ee helper的match_counts原函数离线判定，成功退出+已核对工具身份后才调用，R和S/N仍各不超过5%。这次是资源/训练实验，不是完整打包、安装或90TU认证。\n\n每步独立systemd用户服务，MemoryMax=24,482,992,128B（本机MemTotal−8GiB）、MemorySwapMax=0、CPUQuota=1200%、nice10、ionice2/7。每2秒采样各PID的VmHWM/命令及磁盘可用空间，另用time -v记录每个命令的完整最大RSS；保留30GiB磁盘停止线。服务与阶段均有带时区结束行。没有OOM；所有产物保留。\n\n### 5.2 资源与文件\n\n|步骤|阶段耗时s|cgroup memory.peak B（含文件缓存）|进程VmHWM B（2秒采样）|time -v 最大RSS B|\n|---|---:|---:|---:|---:|\n'''
for r in rows:report+=f"|{r['phase']}|{r['wall_s']:.3f}|{r['cgroup_peak_bytes']}|{r['process']['VmHWM_bytes']}|{r['time_max_rss_bytes']}|\n"
report+=f'''\nVmHWM按完整cmdline识别，loader启动的进程Name为ld-linux-x86-64，不误称为loader本身的工作集；完整PID/命令见step-resource-summary.json。merge仅约3秒，2秒采样低于time -v；不把采样下界冒充完整峰值。cgroup含缓存但共享页按内核记账归属，可能小于进程RSS，不能把两者相加。阶段耗时含少量SHA/清单落盘，命令本身耗时见各commands.json。\n\n|产物|逻辑字节|SHA256/证据|\n|---|---:|---|\n|插桩clang|{instr['bytes']}|`{instr['sha256']}`|\n|23份fdata合计|{fdata}|train/profiles.json逐文件SHA|\n|merged.fdata|{merge['bytes']}|`{merge['sha256']}`|\n|PGO+BOLT clang，未strip/打包|{opt['bytes']}|`{opt['sha256']}`|\n\n优化llvm-bolt自身VmHWM为{peak:,}B；54号非PGO同口径为{base:,}B，减少{base-peak:,}B（{(1-peak/base)*100:.3f}%），比值{peak/base:.6f}。这是两个具体输入的实测，不是通用PGO降内存保证。插桩峰值与优化峰值必须分开。\n\n### 5.3 Profile与BOLT警告\n\n```json\n{json.dumps(profile,ensure_ascii=False)}\n```\n\nR={profile['R']*100:.9f}%，S/N=0，PASS；54号非PGO T为N=23592/M=144032/S=0/U=1/Q=383，R=0.0042385453%。本次是不同PGO二进制和重新采集的profile，N/M/Q不要求与非PGO相同。58号同PGO输入配旧profile的85.3%失效已被本次新profile门禁通过所取代，但58号完整构建停止记录仍保留，不追认该构建成功。\n\n原文及行号：\n\n```text\n{(E/'log-excerpts.txt').read_text().strip()}\n```\n\n特别注意：`--use-old-text failed`是BOLT的警告，命令退出0；原.text可用80,783,150B、需要81,469,838B。没有去掉该参数、改对齐或重试。上表259,324,032B是实际输出的未strip ELF，不能拿它冒充发布包大小。1551个relocation分析警告和两处jump-past-end警告也完整保留，不隐去。\n\n## 6. 三方编译速度（额外观察，不改变门禁结论）\n\n同training.json的23份输入，所有-O*优化等级token移除后统一加-O2，其余参数不变；只做-c。三种编译器各3轮，每轮每种编译器顺序跑完23份，轮间轮换编译器顺序。通过各自根的loader/库启动：nonPGO BOLT来自55号T的clang.candidate，PGO来自D的ordinary-clang-22，PGO+BOLT来自本次optimize/clang-22。完整身份在speed/compiler-identities.json。没有用宿主编译器。\n\n取每轮23份耗时之和，再取3轮中位数；time -v RSS取69次中最大值。未绑核、未关闭ASLR、没有清页缓存；桌面正常活动保留。每次记录load average，1分钟load范围{min(loads):.2f}–{max(loads):.2f}。该结果是训练集内观察，不外推到未见源码或Tizen全量构建。\n\n|clang|三轮23份耗时s|中位数s|最大RSS B|相对nonPGO BOLT|\n|---|---|---:|---:|---:|\n'''
for k,v in sp.items():report+=f"|{k}|{', '.join(f'{x:.3f}' for x in v['round_wall_s'])}|{v['median_wall_s']:.3f}|{v['max_rss_bytes']}|{v['median_wall_s']/sp['nonpgo-bolt']['median_wall_s']:.6f}|\n"
report+=f"\nPGO+BOLT / PGO 中位数比={sp['pgo-bolt']['median_wall_s']/sp['pgo']['median_wall_s']:.6f}；相对PGO耗时变化={(sp['pgo-bolt']['median_wall_s']/sp['pgo']['median_wall_s']-1)*100:+.3f}%。逐输入中位数与全部207次原始记录见speed-unit-medians.json、speed/measurements.json。轮间波动明显，需同时阅读三轮原始数值；中位数差不能认定为稳定加速。编译器strip状态不同（nonPGO已strip，PGO ordinary含debug，PGO+BOLT未strip），因此首轮读取/缓存效应也属于本次观察条件，不声称是只控制代码布局的冷启动实验。\n"
report+='''\n## 7. 更新后的PGO+BOLT完整资源估算\n\n下表严格区分实测和借用；顺序执行的内存不能相加。58号kernel memory.peak与55号阶段采样memory.current口径不同。\n\n|阶段|耗时s|cgroup B|进程VmHWM B|性质/来源|\n|---|---:|---:|---:|---|\n|PGO插桩clang构建|4068.547|7227248640|5930262528|58§4实测|\n|IR训练|201.930|1481818112|1046290432|58§4实测；profraw746313472B|\n|IR合并|3.278|1824751616|1976971264|58§4实测；profdata52528216B|\n|PGO普通编译|6176|21703991296|13305700352|58§4实测|\n|PGO普通安装|328|11565408256|65052672|58§4实测；进程峰值是所见gbs，非完整安装工具峰值|\n|BOLT工具准备/构建及检查|418|UNKNOWN|UNKNOWN|58§4日志6772→7190实测；该子段内存未独立拆分|\n|PGO重链/strip-debug|UNKNOWN|UNKNOWN|UNKNOWN|58§4的273s pipeline还含旧profile失败rewrite，不能直接归作重链时间|\n'''
for r in rows[:4]:report+=f"|BOLT {r['phase']}|{r['wall_s']:.3f}|{r['cgroup_peak_bytes']}|{r['process']['VmHWM_bytes']}|本次实测|\n"
report+='''|缓存释放|9|3716710400|UNKNOWN|借用55§7 T非PGO采样值，估算|
|静态库转换|2544|10596343808|UNKNOWN|借用55§7 T非PGO采样值，估算|
|平台后处理|700|7375040512|UNKNOWN|借用55§7 T非PGO采样值，估算|
|打包|292|10014306304|UNKNOWN|借用55§7 T非PGO采样值，估算|

58号整个旧BOLT阶段为691s、cgroup 14,664,306,688B、进程峰值9,267,929,088B（ld.lld）；它包含工具准备、重链、strip-debug和失败rewrite，不拿来替代本次优化数据，也不直接与本次优化时间相加。A/D prepare另有117.427s/124.614s；本表不能直接求和冒充完整流水线耗时。

已测cgroup阶段最大为PGO普通编译21,703,991,296B（20.213GiB），不是将各阶段峰值相加；不代表尚未完成的PGO打包端到端上限。后处理和打包未对PGO产物重跑，借用值不能写作本次实测。
'''
alloc=sum(x['allocated_bytes'] for x in inventory if not x['path'].endswith('/speed'));estimate=96930275328+746313472+52528216+alloc
report+=f'''\n两根磁盘：58号A+D边界组合实测91,275,411,456B（85.007GiB），连续共存峰值UNKNOWN；普通编译出口du缺采样。借用55号T根采样峰值70,485,561,344B加A根26,444,713,984B，得96,930,275,328B（90.274GiB），这是估算而非本次同时测得。\n本次补测目录（排除额外speed测试）的普通文件分配占用（st_blocks×512，不含目录块）{alloc:,}B（{alloc/2**30:.3f}GiB），分项在experiment-footprint.json；其中包含输入/工具副本、插桩输出、23份fdata、合并profile、优化输出和训练对象。为保留本实验全部现场，保守额外加上这份副本占用及根外IR profraw/profdata，得到{estimate:,}B（{estimate/2**30:.3f}GiB）已知部分规划值，加30GiB保留空间为{estimate/2**30+30:.3f}GiB。它可能重复保留生产流程中可复用的文件，且仍不是完整构建可保证峰值；真实PGO根峰值和后处理需要完整构建再测。speed额外产物独立列出，不计入构建需求。\n\n## 8. 结束、清理与证据\n\n按本轮授权只删除两处目录，详见[61号](61_disk_cleanup.md)。stage-A构建根已删除，但证据、profiles、objects保留；D根和其他历史根只读，没有重建、打包、源码修改或Gerrit推送。现有Source1200未改。本次工具复制、fdata、优化产物、全部速度测试输出保留。\n\n```text\n'''
for phase in ('instrument','train','merge','optimize','speed'):report+=(E/(phase+'-service')/'end.txt').read_text()
report+=(E/'end.txt').read_text()+'```\n\n证据：`tools/bolt/results/pgo-bolt-followup-20261105/resume/`。结论：工具已补齐，23份采集、合并、正式参数优化和207次速度编译全部完成；profile门槛通过，use-old-text空间不足警告仍需另行考虑，未把实验当作完整发布验证。\n'
p=B/'docs/bolt/59_pgo_bolt_followup.md';old=p.read_text();assert '## 5. 2026-11-05' not in old
old=old.replace('# 59：PGO clang 的 BOLT 资源补测（前置缺项停止）','# 59：PGO clang 的 BOLT 资源补测（工具补齐，补测完成）',1)
start=old.index('\n\n');end=old.index('\n\n## 1.')
intro=f'''\n\n工具已补齐，23份训练、新profile合并和正式参数BOLT优化成功，R={profile['R']*100:.6f}%通过原5%门槛。优化llvm-bolt自身VmHWM为{peak/2**30:.3f}GiB，比非PGO同口径低{(1-peak/base)*100:.2f}%；但use-old-text因原.text容量不足发出警告，实际未strip输出为{opt['bytes']:,}字节。23份-O2用例三轮中位数：nonPGO BOLT {sp['nonpgo-bolt']['median_wall_s']:.3f}s、PGO {sp['pgo']['median_wall_s']:.3f}s、PGO+BOLT {sp['pgo-bolt']['median_wall_s']:.3f}s；清理仅限批准两处，详情见61号。\n\n**第1–4节保留首次缺工具的历史停止记录；第5–8节是本轮补齐后的最新结论。**'''
p.write_text(old[:start]+intro+old[end:]+report)
print('report written',p)
