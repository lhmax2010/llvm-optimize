from pathlib import Path
import json,datetime
E=Path(__file__).resolve().parent;B=E.parents[4]
ds=json.loads((E/'all-results.json').read_text())
def link(path,label=None):
 p=Path(path)
 try:q='../../'+str(p.relative_to(B))
 except ValueError:q=str(p)
 return '['+(label or p.name)+']('+q+')'
def stamp(n):
 return datetime.datetime.fromtimestamp(n/1e9).astimezone().isoformat() if n else 'UNKNOWN'
def source(s):
 if not s:return 'UNKNOWN'
 return link(s['file'])+':L'+str(s.get('line','?'))+('；'+stamp(s['time_ns']) if 'time_ns' in s else '')
def num(n):return str(round(n,6)) if isinstance(n,float) else str(n)
def boundary(p):
 if 'start' in p:return 'L%d [%ss] → L%d [%ss]'%(p['start']['line'],p['start']['seconds'],p['end']['line'],p['end']['seconds'])
 if 'line' in p:return 'L%d，%s'%(p['line'],p['basis'])
 return p.get('reason','UNKNOWN')
names={'cmake':'CMake配置','ordinary_ninja_including_links':'普通Ninja编译（含重叠链接）','ordinary_install':'普通安装至BOLT begin',
'BOLT_total':'BOLT begin至compare-root结束（含各子阶段）','BOLT_reconfigure':'BOLT重新配置','BOLT_tool_build':'BOLT工具构建',
'BOLT_pipeline':'BOLT pipeline总窗口','BOLT_compare_root':'compare-root门禁','cache_release':'cache-release','archive_conversion':'静态库转换',
'platform_post_before_BOLT_post_gate':'find-debuginfo开始至post门禁前的平台后处理','BOLT_post_gate':'BOLT post门禁','packaging':'RPM文件处理至最后Wrote',
'BOLT_relink':'BOLT重新链接','BOLT_reference_strip':'reference strip','BOLT_candidate_strip':'candidate strip','BOLT_rewrite':'BOLT rewrite',
'BOLT_RUNPATH':'RUNPATH调整','BOLT_tiny_gate':'tiny门禁','BOLT_security_gate':'security门禁','BOLT_real_gate_prestrip':'real gate prestrip',
'BOLT_real_gate_preinstall':'real gate preinstall','BOLT_real_gate_post':'real gate post','BOLT_debug_symbols':'debug symbols门禁','BOLT_debuglink':'debuglink门禁'}
lines=['# 84. 资源拆分第一步（已有证据，未重新构建）','',
'结论：PASS（完成已有数据的拆分；不能恢复的细项明确记为 UNKNOWN）。本报告不排候选优先级、不判断收益是否可以接受。',
'',
'## 1. 口径与读取边界','',
'已读设计 v9 §2.2、§2.4、§4.1/4.2、§6，63/74 号材料、57/77/79 号身份记录；逐行读取下表九份完整 x86_64 GBS 日志、本地三份原始内存/进程/du采样、最终build-result，以及只读构建树中的 .ninja_log 和 build.ninja。'
'没有访问 QB 网站，没有读取或修改 LLVM Git 仓库，没有运行 clang/lld/CMake/Ninja/GBS，没有重测构建。83号的微型夹具不作为资源样本。',
'',
'分析在 MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、Nice=19、IOSchedulingClass=idle 的串行用户服务中完成。'
'解析代码和原始读取清单：'+link(E/'analyze_resources.py')+'、'+link(E/'read-inputs.json')+'；'
'本地ThinLTO规则原文/行号/SHA：'+link(E/'thinlto-build-rules.json')+'；完整结构化结果：'+link(E/'all-results.json')+'。',
'',
'- GBS 时间为日志的整数秒；只用明确起止行相减。表中“总日志窗口”是 0 到最后一条 GBS 时间戳，不等于 controller 的墙钟时长。阶段可嵌套，不能相加。',
'- 普通Ninja窗口含链接。独立纯编译耗时 UNKNOWN：编译与链接并行，不能把链接时长从窗口相减。每个大链接用 .ninja_log 的 start_ms/end_ms；任务互相重叠，不能把五项求和当作串行耗时。',
'- QB只有Ninja完成行，无法恢复大链接起点；不把相邻完成行的间隔当成任务耗时。保留完成行原文作定位，时长记 UNKNOWN。',
'- 内存峰值是整个 cgroup（含文件缓存）；阶段内 memory.current 最大采样值只表示该时间窗口的整个组，不能归到一个链接器。单进程 VmHWM 仅有 llvm-bolt 采样，全构建最大单进程及其命令 UNKNOWN。',
'- 本地日志没有 cgroup memory.stat 的 anon/file；host /proc/meminfo 不能替代，均记 UNKNOWN。',
'- du是约60秒一次、单次50秒限时的根目录总量采样。峰值是成功采样最大值，不保证捕获瞬时峰值。没有分层du，完整主要目录分布 UNKNOWN；BOLT_DISK_REPORT 的有限作用域另列，不能等同整个构建根。',
'- 74-T memory.peak 等于 MemoryMax，max=3877、oom=0，记“≥ 限额（截断）”；时长标“受内存回收影响”，不作为资源候选的对照基线。D未触顶，按实测记录。',
'','## 2. 各来源身份（全部 x86_64）','','|来源|环境/项目|源码提交|快照|总日志窗口 s / 证据|','|---|---|---|---|---|']
for d in ds:
 lines.append('|%s|%s / %s|%s|%s|%s / %s|'%(d['id'],d['environment'],d['project'],d['commit'],d['snapshot'],d['log_last_seconds'],link(d['log'])))
lines+=['','总日志窗口的最后时间戳及源码路径保存在各来源 result.json；原始压缩文件大小与SHA见读取清单。不同源码、项目、环境分别列示，不合并成一次实验。']
for i,d in enumerate(ds,3):
 sid=d['id'];P=d['phases'];M=d['memory'];D=d['disk'];out=E/sid
 lines+=['',f'## {i}. {sid}：{d["environment"]} / {d["project"]}','',
 '提交 '+d['commit']+'；快照 '+d['snapshot']+'。日志 '+link(d['log'])+'；完整锚点 '+link(out/'anchors.txt')+'；数据 '+link(out/'result.json')+'。',
 '','### 阶段时长','','|阶段|秒|日志行/时间或字段|','|---|---:|---|']
 for k,p in P.items():lines.append('|%s|%s|%s|'%(names[k],num(p['seconds']),boundary(p)))
 if d['project']=='Base-Dev':lines+=['','release 未执行独立 debug symbols/debuglink 门禁，其时长为 N/A，不填0。']
 lines+=['','### 五个大链接','','|目标|秒|起止/原始证据|','|---|---:|---|']
 for k,p in d['thinlto_links'].items():
  ev=('%s → %s ms；%s:L%s；原文 %s'%(p['ninja_start_ms'],p['ninja_end_ms'],link(p['ninja_source']),p['ninja_line'],'<code>'+p['ninja_raw'].replace('\t',' / ')+'</code>')) if 'ninja_source' in p else ('仅完成 '+('L%s [%ss]'%(p['completion']['line'],p['completion']['seconds']) if p['completion'] else 'UNKNOWN')+'；起点UNKNOWN')
  lines.append('|%s|%s|%s|'%(k,num(p['seconds']),ev))
 lines+=['','### 内存与磁盘','']
 if d['environment']=='local':
  peak=('≥ '+str(M['memory_max'])+' B（限额截断；计数器读值 '+str(M['memory_peak'])+'）') if M['truncated'] else str(M['memory_peak'])+' B'
  lines+=['|量|结果|证据|','|---|---|---|',
   '|cgroup memory.peak（含文件缓存）|'+peak+'|'+link(M['peak_final_file'])+'：stats.memory.peak / memory.max；首次峰值采样 '+source(M['peak_source'])+'|',
   '|memory.events|'+json.dumps(M['events'],ensure_ascii=False)+'|'+link(M['peak_final_file'])+'：stats.memory.events；原始序列末次 '+source(M['last_sample'])+'|',
   '|构建服务墙钟秒|'+num(M['build_seconds'])+'；'+M['time_note']+'|'+link(M['peak_final_file'])+'：seconds|',
   '|anon / file|UNKNOWN / UNKNOWN|原始 resources 没有 memory.stat；未用宿主机数据代替|',
   '|全构建最大单进程 VmHWM / 命令|UNKNOWN / UNKNOWN|只有 llvm-bolt 进程采样|']
  vm=M.get('llvm_bolt_VmHWM')
  if vm:
   lines+=['|llvm-bolt 已采样最大 VmHWM|'+str(vm['bytes'])+' B|'+source(vm['source'])+'|',
    '','llvm-bolt 命令原文（对应上述 PID 记录）：','','~~~text',' '.join(vm['command'] or []),'~~~','']
  lines+=['|磁盘量|结果|证据|','|---|---|---|',
   '|构建根成功du最大值|'+str(D['root_peak'])+' B|'+source(D['source'])+'|',
   '|du样本总数 / 成功 / 超时 / 非零或缺失|%s / %s / %s / %s|%s；超时包含在非零中，不相加|'%(D['samples'],D['successful_samples'],D['timeouts'],D['nonzero_or_missing'],link(D['source']['file'])),
   '|主要目录的分层峰值|UNKNOWN|历史du只测根总量|',
   '','阶段窗口内 cgroup memory.current 最大采样值（并发任务共用，不代表独占资源）：','',
   '|阶段|最大采样 B|来源/时间|','|---|---:|---|']
  for k,p in list(P.items())+list(d['thinlto_links'].items()):
   v=p.get('cgroup_sampled_window_max')
   if isinstance(v,dict):lines.append('|%s|%s|%s|'%(names.get(k,k),v['bytes'],source(v['source'])))
 else:lines+=['cgroup memory.peak / memory.events / anon / file / 最大单进程 VmHWM及命令 / 根du峰值 / 分层du：**全部 UNKNOWN**。保存的QB包日志没有这些采样；没有把机器内存容量或BOLT自身统计当成cgroup/进程峰值。']
 lines+=['','BOLT有限作用域的已记录磁盘量（不是整个根的分层du；每个数对应原始 BOLT_DISK_REPORT 行）：','',
 '|阶段|GBS s / 行 / 记录时间|work B|tool_objects B|tool_executable B|tool_library合计 B|cache正分配delta B|','|---|---|---:|---:|---:|---:|---:|']
 for r in d['BOLT_disk_reports']:
  z=r['data'];s={}
  for item in z.get('owned_paths',[]):s[item['category']]=s.get(item['category'],0)+item['allocated_bytes']
  lines.append('|%s|%s / L%s / %s|%s|%s|%s|%s|%s|'%(z['stage'],r['gbs_seconds'],r['line'],stamp(z.get('time_ns')),s.get('work','UNKNOWN'),s.get('tool_objects','UNKNOWN'),s.get('tool_executable','UNKNOWN'),s.get('tool_library','UNKNOWN'),z.get('cache_delta_allocated_bytes','UNKNOWN') if z.get('cache_delta_known') else 'UNKNOWN'))
lines+=['','## 12. 候选项预判（不排序，不推断收益）','',
 '下表占比仅为同一来源该阶段实测秒数 / 该来源总GBS日志窗口。列顺序用于溯源，不是性能排名。'
 '74-T列只是描述已发生的构建，**受内存回收影响，禁止作为候选实验对照基线**。'
 'BOLT重链复用列用pipeline窗口定位；重链自身占比 UNKNOWN。门禁行列出三次real gate耗时总量作上界定位，复制自身占比 UNKNOWN。'
 'RPM行是文件处理至Wrote窗口，压缩自身占比 UNKNOWN。这些窗口不能直接等同可节省时间。',
 '','|候选/所对应阶段|'+'|'.join(d['id'] for d in ds)+'|','|---|'+'---:|'*len(ds)]
candidates=[
 ('并行度：普通Ninja含链接',lambda d:d['phases']['ordinary_ninja_including_links']['seconds']),
 ('静态库转换调度：转换窗口',lambda d:d['phases']['archive_conversion']['seconds']),
 ('BOLT重链复用：pipeline窗口（重链自身UNKNOWN）',lambda d:d['phases']['BOLT_pipeline']['seconds']),
 ('门禁复制瘦身：三次real gate（复制自身UNKNOWN）',lambda d:sum(d['phases'].get('BOLT_real_gate_'+k,{}).get('seconds',0) for k in ('prestrip','preinstall','post'))),
 ('find-debuginfo并发：平台后处理窗口',lambda d:d['phases']['platform_post_before_BOLT_post_gate']['seconds']),
 ('RPM压缩：文件处理/打包窗口（压缩自身UNKNOWN）',lambda d:d['phases']['packaging']['seconds'])]
for label,f in candidates:
 vals=[]
 for d in ds:
  n=f(d);vals.append((num(n)+'s / %.2f%%'%(n/d['log_last_seconds']*100)) if isinstance(n,(float,int)) else 'UNKNOWN')
 lines.append('|'+label+'|'+'|'.join(vals)+'|')
lines+=['|中间产物清理：峰值时刻/目录占比|'+'|'.join('UNKNOWN（有限BOLT作用域见本源表）' for _ in ds)+'|',
 '|非安装目标：可去除任务占比|'+'|'.join('UNKNOWN（未做依赖闭包分析）' for _ in ds)+'|',
 '','并行度还涉及五个链接任务和BOLT工具构建，两者的独立实测窗口见各来源表，不能和普通Ninja占比相加。'
 '“中间产物清理”对应缓存释放/构建后段，是否早于峰值、究竟能降低多少磁盘，现有稀疏采样不能证明。'
 '没有执行任何资源优化、清理、并行度调整或重新构建。',
 '','## 13. 能恢复与待补项','',
 '- 已恢复：九份日志的CMake、普通Ninja含链接、BOLT工具构建/pipeline/compare-root、三次real门禁、转换、后处理、打包窗口；本地三次各五个ThinLTO链接独立任务计时；本地cgroup峰值/events及llvm-bolt采样VmHWM；本地根du成功样本峰值和失败/超时计数。',
 '- 不能恢复：QB五个链接起点和独立耗时；纯编译排除链接的独占墙钟；BOLT重链/strip/rewrite/RUNPATH/tiny/security细分耗时；全构建进程最大VmHWM及命令；cgroup anon/file；完整分层磁盘峰值；各候选的实际收益。统一 UNKNOWN，不事后推算。',
 '- 74-T：≥24,482,992,128 B（截断）、max 3877、oom 0；其构建耗时受内存回收影响。74-D memory.peak=18,161,836,032 B，max 0；74-T du 32次超时，根峰值67,924,271,104 B只是91次成功样本的最大值。',
 '- 下一次计划内构建需要事先增加链接独立进程计时/VmHWM、memory.stat anon/file、连续df与分层du，以及helper各子命令的显式起止。此次没有改入口采样逻辑。',
 '']
end='84 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status=PASS'
lines+=['~~~text',end,'~~~','']
(B/'docs/bolt/84_resource_breakdown.md').write_text('\n'.join(lines))
(E/'result.json').write_text(json.dumps({'status':'PASS','sources':len(ds),'local_link_intervals':15,'unknowns':'see section 13','end':end},indent=2)+'\n')
print(end)
