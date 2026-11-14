import pathlib,json,hashlib,shlex,datetime,subprocess
E=pathlib.Path(__file__).resolve().parent;B=E.parents[3];W=pathlib.Path('/home/linhao/Toolchain/development/llvm-optimize')
root=W/'temp/rebase-359934-20261111-r6/basedev/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
build=root/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build'
paths={'input':W/'temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22','tool':build/'bin/llvm-bolt','loader':root/'lib64/ld-linux-x86-64.so.2','profile':build/'clang-bolt/profile.fdata'}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1048576),b''):h.update(c)
 return h.hexdigest()
ident={k:dict(path=str(p),exists=p.is_file(),bytes=p.stat().st_size if p.is_file() else None,sha256=sha(p) if p.is_file() else 'UNKNOWN') for k,p in paths.items()}
out=W/'temp/report-stale-proposal-20261116'
options=json.loads((B/'tools/bolt/results/local-full-r6-20261111/basedev/rewrite-bolt.log.argv.json').read_text())['argv'][4:]
assert options[0].startswith('-data=')
options=options[1:]
lib=':'.join(str(p) for p in [build/'lib64',root/'lib64',root/'usr/lib64'])
cmd=[str(paths['loader']),'--library-path',lib,str(paths['tool']),str(paths['input']),'-o',str(out/'clang.bolt'),'-data='+str(paths['profile']),*options,'-report-stale']
assert '--thread-count=1' in cmd and '-stale-threshold=5' in cmd
df=subprocess.run(['df','-B1','/home'],capture_output=True,text=True)
(E/'current-df.txt').write_text(df.stdout+df.stderr);assert df.returncode==0
avail=int(df.stdout.splitlines()[-1].split()[3])
peak=70485561344;minimum=2*peak+20*1024**3;target=(2*peak*12+9)//10+20*1024**3
budget=dict(time=datetime.datetime.now().astimezone().isoformat(),historical_single_root_bytes=peak,formula_minimum='2*70485561344 + 20GiB',formula_target='ceil(2*70485561344*1.2) + 20GiB',minimum_bytes=minimum,target_bytes=target,available_bytes=avail,minimum_shortfall_bytes=max(0,minimum-avail),target_shortfall_bytes=max(0,target-avail),note='历史预算草案，不保证新采集开销/新版本峰值；不含另报的实物比较副本空间')
(E/'resource-budget.json').write_text(json.dumps(budget,ensure_ascii=False,indent=2)+'\n')
inv=[json.loads(l) for l in (B/'tools/bolt/results/handover-20261114/directory-inventory.jsonl').read_text().splitlines()]
choices=[
('local-full-r6-20261111-compare','74/79','从RPM解包的比较副本；已发布比较报告，保留RPM可重解；本次未逐文件验证可重建','中：先分离日志/唯一证据，不能整目录自动删'),
('qb79-local-resume-20261112','79','源码tar/比较工作副本；报告与分类证据已发布，RPM在QB下载目录；唯一性需清单审核','中'),
('dwarf-check-20261106','67','DWARF展开文本和副本；分类结论已发布，132对原.debug需保留；文本可否完全重生未复核','中'),
('qb-1221204-1221207','71','旧QB下载；71结果已发布，不能保证公开下载长期可用；后续基线现为1226850/1','中高：旧回归追溯基线'),
('qb-1223601-1223602','73/75','旧QB下载及ARM检查源；77/79新基线可覆盖部分，不替代全部历史输入','高'),
('deleted-repo-backup-20261105','64/66','源码保护bundle/补丁；GitHub未包含全部仓库副本，85扩展盘点OOM','极高：不建议清理，需先独立源码完整性审计')]
rows=[]
for name,doc,alt,risk in choices:
 d=next(x for x in inv if x['path']==str(W/'temp'/name))
 rows.append(dict(path=d['path'],du_bytes=d['size_bytes'],measured_at=d['time'],document=doc,purpose=d['purpose'],alternative=alt,risk=risk,authorized_to_delete=False))
(E/'cleanup-candidates.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
text='''# 资源报备草案（未批准、未执行）

## D report-stale
目的只取得74号D的失配名单；保持旧profile、正式优化参数与5%门槛。不是新构建、不把输出作为新发货候选。
输入/工具/loader/profile当前身份见report-stale-plan.json；平台工具由自身根loader读取。源提交fea0fe46，输入D SHA bf15cf062439714651809cd3b5ca82619407081adca64ceb65699e6ccae50501。运行前应复核全部SHA和输出目录不存在；任一输入不存在则先PM指定保全副本，不从网络获取。
命令（只写不执行）：

    '''+shlex.join(cmd)+'''

计划输出目录为W/temp/report-stale-proposal-20261116；只在获批后创建。stdout/stderr、command.json、退出码、资源记录和一次输出ELF全部保留。
资源申请草案：单进程约10GB（83依据）；建议MemoryMax=16GiB包含文件缓存、swap0、CPUQuota=400%、nice19、idle IO、单任务。16GiB是待批准余量，不是实测需求。本任务仍4GiB，未运行llvm-bolt。
时长UNKNOWN；排期预留60分钟，拟硬停止线60分钟，不把它当实测预测。磁盘新占用暂申请5GiB（输入读取不复制、输出/日志/采样），精确上限UNKNOWN；stdout/stderr各1GiB监测告警，/home低于30GiB或目录新增超过5GiB即按获批的正常取消流程停。OOM不重试、不抬限制。信号/正常停止方式需要资源报备同时授权，本任务没有执行。
还应单列诊断-v或print开关的输出膨胀风险；本次未完成对应源码开关核对，不能把建议-v=1当作保证提供relocation明细的已验证命令。

## 下一次计划内完整构建采集
不修改当前入口。先审阅以下伪diff，再独立实现/测试，按新输出目录部署；产品源码/spec/helper不变。
1. launcher的service_stage及controller：记录monotonic_ns与wall time、项目/step/argv/service/PID、rc/signal。两类时钟分开，禁止采样器观察时间替代命令实际起止。
2. 已有driver监视器：每2秒保存memory.current/peak/events及memory.stat的anon/file；服务结束前保全最终计数，cgroup删除后不可恢复；文件缓存与进程RSS不相加。
3. 进程记账：捕获子进程创建/退出、cmdline和wait4 rusage；所有后代不能只靠controller的RUSAGE_CHILDREN。对gbs/chroot边界需要授权的进程事件采集或可审计wrapper，否则最大单进程继续UNKNOWN；/proc VmHWM轮询不能保证捕获短进程。
4. cmake/ninja大链接/BOLT各门禁/归档/打包：优先已有原始日志和.ninja_log的真实起止；但BOLT工具内部子步骤若无起止记录，仅外部采样无法精确拆分。要精确计时需另批透明exec事件采集方案；不得暗改产品helper，不凭日志相邻行推算。
5. 文件系统已用量/可用量10秒；分层du每5分钟（BUILD、BUILDROOT、SOURCES、RPM、BOLT工件、profile），每次50秒上限，记录timeout/rc/权限盲区；一次仅一个du，父子不相加。也需另批终止超时子进程。
6. resource_report按真实阶段窗口对齐采样；缺命令起止、anon/file、rusage或层级du就UNKNOWN。memory.events max>0则峰值写≥限额，时长标回收影响；不把成功du最大值当保证峰值。
7. 新测试：时钟回拨、短进程、子孙进程、cgroup消失、du超时/权限失败、prep交接、截断峰值，所有采集开销记录，不能改发布产物参数。

预计需要修改文件：toolchain/launcher.py、basedev/launcher.py的生成监控片段，两个resource_report.py；新增本地collector及tests；run-night只增加采集开关传递；README/provenance/SHA256SUMS更新。完整构建资源设置不自动改变。本草案不修复本次步骤2授权不足的问题。

## 磁盘
按85已有du列表引用原采样时间，本次只重新df、不重新du。历史最低预算2×70,485,561,344B+20GiB；目标加20%根余量。差额见resource-budget.json。新增采集、比较解包、PGO根和report-stale分别预算，不能当已有余量覆盖。
清理候选见cleanup-candidates.json，体积是85的du，不保证可实际释放量（可能有链接/共享块及同期变化），只提供PM审核清单。不可把已发布摘要视为大型输入已上传。优先审计可重解的比较副本；PGO原始profile、74 BOLT输入、恢复的TU输入、当前QB基线、源码保护备份和有效构建根不列为低风险删除项。
'''
(E/'resource-proposal.md').write_text(text)
plan=dict(status='DRAFT_NOT_EXECUTED',identity=ident,argv=cmd,output_root=str(out),memory_single_process_estimate='~10GB from83',proposed_cgroup_max='16GiB pending approval',proposed_timeout='60min cap, runtime UNKNOWN',proposed_disk_budget='5GiB provisional',budget=budget,time=budget['time'])
(E/'report-stale-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
(E/'step5-result.json').write_text(json.dumps(dict(status='DRAFT',time=budget['time'],executed=False,missing_inputs=[k for k,v in ident.items() if not v['exists']],budget=budget),ensure_ascii=False,indent=2)+'\n')
print('identity availability',[(k,v['exists']) for k,v in ident.items()]);print(json.dumps(budget,ensure_ascii=False));print('86步骤5 已结束 '+budget['time']+' status=DRAFT')
