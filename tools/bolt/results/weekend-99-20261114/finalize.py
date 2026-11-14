from pathlib import Path
import json,datetime,os,subprocess,threading,time
E=Path(__file__).parent; B=E.parents[3]
assert (B/'docs/bolt/STATUS.md').is_file(),B
mem=lambda:int(next(l.split()[1] for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemAvailable:')))*1024
v=os.statvfs('/home');admission={'time':datetime.datetime.now().astimezone().isoformat(),'MemAvailable':mem(),'home_available':v.f_bavail*v.f_frsize}
assert admission['MemAvailable']>=8*2**30 and admission['home_available']>=60*2**30,admission
(E/'finalize-admission.json').write_text(json.dumps(admission,indent=2)+'\n')
done=threading.Event()
def watch():
 while not done.wait(30):
  m=mem()
  if m<6*2**30:
   (E/'finalize-watchdog-stop.json').write_text(json.dumps({'MemAvailable':m,'time':datetime.datetime.now().astimezone().isoformat()})+'\n')
   subprocess.run(['systemctl','--user','stop','--no-block','weekend99-finalize-20261114.service']);return
thread=threading.Thread(target=watch,daemon=True);thread.start()
try:
 r=json.loads((E/'step5/result.json').read_text());f=json.loads((E/'step5/result-full.json').read_text())
 assert r['status']=='PASS' and f['status']=='PASS',(r.get('failure'),f.get('failure'))
 assert f['converted']==3853 and f['preserved']==11 and f['archives']==225
 samples=[json.loads(l) for l in (E/'step5/runtime-samples.jsonl').read_text().splitlines()]
 watched=[]
 for p in E.glob('step[1-5]-watchdog.jsonl'):
  watched.extend(json.loads(l) for l in p.read_text().splitlines())
 assert not any(x['triggered'] for x in watched)
 assert not any(x['stop_reasons'] for x in samples)
 events={l.split()[0]:int(l.split()[1]) for l in f['memory_events'].splitlines()};assert events['oom']==events['oom_kill']==0
 peaks=[]
 for s in samples:
  for p in s['processes']:
   if p['hwm']:peaks.append({'bytes':int(p['hwm'].split()[1])*1024,'time':s['time'],'pid':p['pid'],'argv':p['argv']})
 resource={'cgroup_peak_bytes':int(f['memory_peak']),'memory_events':events,'sampled_max_VmHWM':max(peaks,key=lambda x:x['bytes']) if peaks else None,'min_MemAvailable_bytes':min(x['MemAvailable'] for x in samples),'max_temporary_output_bytes':max(x['output_bytes'] for x in samples),'min_home_available_bytes':min(x['home_available'] for x in samples),'sample_count':len(samples),'watchdog_triggered':False,'time_from_service_start_seconds':f['total_step_seconds'],'note':'cgroup includes file cache; sampled VmHWM may miss short-lived children'}
 (E/'step5/resource-summary.json').write_text(json.dumps(resource,ensure_ascii=False,indent=2)+'\n')
 for n in range(1,6):
  q=subprocess.run(['journalctl','--user','-u',f'weekend99-step{n}-20261114.service','--no-pager','-o','short-iso'],capture_output=True,text=True)
  (E/f'step{n}-service-journal.txt').write_text(q.stdout+q.stderr)
 end=f"99步骤5全量 已结束 {f['end']} status=PASS"
 final=f"99 已结束 {datetime.datetime.now().astimezone().isoformat()} 1=STOP 2=PASS 3=PASS 4=PASS 5=PASS"
 summary={'steps':{'1':'STOP','2':'PASS','3':'PASS','4':'PASS','5':'PASS'},'sandbox':{'before_last_observed':'b0c1732c08c5a81382f9eeef27ffe1e40c6c47d1','after':'NO_NEW_OBSERVATION','push_attempted':False,'note':'step1 test ERROR; no product commit created or remote queried/pushed; replay exported git object b0'},'watchdog_triggered':False,'preparation_corrections':{'step1':0,'step2':1,'step3':0,'step4':0,'step5':1},'end':final}
 (E/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 p=B/'docs/bolt/99_weekend.md';s=p.read_text();s=s.replace('逐步交付；尚未完成的步骤不标PASS。全部分析串行、4GiB/swap0/CPU200%/Nice19/IO idle；每30秒检查MemAvailable，低于6GiB只停止本任务自己的服务。步骤1准入≥8GiB、磁盘≥60GiB通过。未进入另一项目目录、未操作其锁或进程。','''**五步已结束：1 STOP，2–5 PASS。** 步骤1既有测试出现进程读取竞态，未创建新产品提交或推送sandbox。步骤5使用已提交b0c1732c，完成450发货归档复核，以及225个原始归档的3853个转换成员重新生成/字节比较，全部一致。看门狗未触发，无OOM。

步骤1–4和收尾服务4GiB/swap0/CPU200%/Nice19/IO idle；步骤5准备4GiB，实际重放按授权12GiB/CPU400%、jobs=2，每进程地址空间4GiB。所有服务串行，重放含准备总限120分钟，每30秒检查MemAvailable<6GiB即停止自己的服务。首次准入全部满足，没有进入30分钟等待。未进入另一项目目录、未操作其锁或进程。

|步骤|状态|结果|
|---|---|---|
|1|STOP|103项已运行：102通过、1ERROR，16未运行；sandbox未推送|
|2|PASS|8处B完成复核，3升A、5仍B；连同87号现为5A/5B|
|3|PASS|68函数逐对指令diff；28算术序列、35 LEA/复制形式、5混合|
|4|PASS|设计6项事实资料包；无推荐/裁决|
|5|PASS|450发货归档/7728 ELF成员新旧检查一致；225 T原始归档重新转换3853成员、保留11成员，归档和逐成员SHA与发货T一致|

[raw链接索引](../../tools/bolt/results/weekend-99-20261114/RAW_LINKS.md)。''')
 s=s.replace('步骤1–4已结束，步骤5待准入检查。','五步均已结束；各步原始记录如下。')
 s+='''\n## 步骤5：PASS（补足全部3853个成员的重新生成）

首次检查2026-11-14T06:35:12-08:00：未发现gbs/rpmbuild/ninja/llvm-bolt重进程，MemAvailable=26,350,829,568B，/home可用206,627,004,416B。06:35:36非阻塞取得既有共享heavy-stage.lock；没有获取另一项目私有锁，重放结束已随服务退出释放。没有等待30分钟轮询，未到截止时间是因为首次已满足全部条件。

### 输入和验证覆盖

- 从git对象导出b0c1732c转换器，基线ecb2dec7；不使用步骤1留存的脏工作树文件。
- 78号450个发货归档来自QB 1225393/1225395；79号已证明1226850/1226851的102个二进制包载荷与它们一致（本次只读79号该记录，未重读全部RPM，见baseline-chain.txt）。这些归档已是ELF。每个项目225归档、3864成员（历史3853转换+11原生），共7728；新旧inspect、elf_details、pic_relocations相同，forbidden为0，成员SHA和归档SHA未变化。实际convert保持既有的225个already-native skip行为，不能称这些输入又完成了一次代码生成。
- 10个真实debug ThinLTO归档：1093转换+7原生，两级SHA及inspect其余字段与78号保留输出一致；保留输出也与发货T相同。
- 为覆盖用户要求的全部3853个转换成员，读取63号保留build/lib64中其余215个对应原始归档，在新副本中用同样平台clang/llvm-dis/llvm-nm、loader、debug_info=yes、jobs=2转换。连同10个大归档，共225归档/3853转换+11原生；完整归档SHA、大小、成员顺序、逐成员SHA及其余inspect字段均与发货T相同。D覆盖为全量ELF检查与保留路径，不宣称D的3853成员重新代码生成。
- 合法输入新增拒绝0。所有新生成的对象都经过产品PIC/符号门禁；未改产品测试或断言，没有产品失败后的重跑。

[覆盖补足计划](../../tools/bolt/results/weekend-99-20261114/step5/coverage-plan.md)、[工具身份](../../tools/bolt/results/weekend-99-20261114/step5/tool-identities.json)、[第一段结果](../../tools/bolt/results/weekend-99-20261114/step5/result.json)、[3853全量结果/逐成员SHA](../../tools/bolt/results/weekend-99-20261114/step5/result-full.json)、[完整重放日志](../../tools/bolt/results/weekend-99-20261114/step5/replay-remaining.log)。第一段日志的“99步骤5 已结束”只指450+10子段完成，最终以本节的全量结束行为准。

本轮输出根W/temp/weekend99-replay-20261114。其余215个临时输入/输出在记录SHA和逐成员结果后仅删除本任务自己的文件，保留JSON/日志；历史根、78保留输出及发货归档未写。10个大归档的新输出仍在debug/archives/。

### 资源和准备修正

'''
 s+=f"服务含准备耗时{f['total_step_seconds']:.3f}s，cgroup峰值{resource['cgroup_peak_bytes']}B（含文件缓存），OOM={events['oom']}、oom_kill={events['oom_kill']}、max事件={events.get('max',0)}。最低MemAvailable={resource['min_MemAvailable_bytes']}B，临时目录成功采样最大{resource['max_temporary_output_bytes']}B。看门狗没有触发。VmHWM采样及命令行见[资源摘要](../../tools/bolt/results/weekend-99-20261114/step5/resource-summary.json)，短命子进程可能漏采。\n\n"
 s+='''准备修正1次：在运行中的服务上用set-property设置RuntimeMaxSec被systemd拒绝，尚未开始重放。保留错误原文与diff，改为仅设置支持的MemoryMax/CPUQuota，并由单调时钟看门狗执行整个步骤7200秒限时；未因OOM提高上限。第二段从服务启动时间计时，包含准备及第一段，更严格。见[错误与修正](../../tools/bolt/results/weekend-99-20261114/step5/preparation-error.txt)。没有第二次准备错误。

~~~text
Failed to set unit properties on weekend99-step5-20261114.service: Cannot set property RuntimeMaxUSec, or unknown property.
~~~

### sandbox与没有运行的内容

步骤1停止，所以本任务没有新建产品提交、查询或推送sandbox。任务输入/96号最后观测是b0c1732c；没有新的远端after观测，不能将本地状态冒充ls-remote结果。无自动回退。没有运行完整构建、BOLT/report-stale、QB、Gerrit查询/评审操作。只在证据仓库提交推送。

已读：步骤1的产品git对象/既有测试，87号同源源码/反汇编及74号生成表，83号68函数名单和两份BOLT输入，58/59/84/86及设计指定段落，78号归档/转换保留产物、63号原始归档和平台工具。未读：另一项目目录、QB/Gerrit网页、全部历史GBS原日志、全部PGO profile本体；未做未授权的因果推断或决策。

'''+end+'\n\n'+final+'\n'
 p.write_text(s)
 p=B/'docs/bolt/STATUS.md';p.write_text(p.read_text()+f'''\n### 2026-11-14：99号周末任务结束

[99号](99_weekend.md)：步骤1 STOP（既有test_process_states_at_run_return读取/proc/stat时ProcessLookupError；103运行、102通过、1ERROR、16未运行），未生成新产品提交/推sandbox，b0工作树留存单行空白修改。步骤2 PASS：剩余8B中3升A、5仍B，总5A/5B。步骤3 PASS：68函数指令diff和描述性分类，不推因果。步骤4 PASS：六项PGO事实包，不作推荐/裁决。

步骤5 PASS：b0c1732c的450发货归档/7728 ELF成员复核无新增拒绝；另用保全原始输入完成225个T归档全部3853转换+11原生，逐归档与逐成员SHA均与发货T相同（含78号10个大debug归档）。D做全量ELF检查，不冒称重新代码生成。全量实物证明已完成；本任务仍不触发QB。12GiB/swap0/CPU400%/jobs2，含准备{f['total_step_seconds']:.1f}s，cgroup峰{resource['cgroup_peak_bytes']}B，无OOM，看门狗未触发；共享锁仅持有本任务重放期间。sandbox无新观测/推送，最近已知b0不变于本任务操作。

{final}
''')
 files=[B/'docs/bolt/99_weekend.md',B/'docs/bolt/STATUS.md']
 for p in E.rglob('*'):
  if p.is_file() and not p.is_symlink() and not any(x=='environment' or x.endswith('-scratch') for x in p.relative_to(E).parts):files.append(p)
 index=E/'RAW_LINKS.md';files=sorted(set(files+[index]));base='https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/'
 index.write_text('# 99号 raw链接索引\n\n'+''.join(f'- [{p.relative_to(B)}]({base}{p.relative_to(B)})\n' for p in files))
 subprocess.run(['python3','-B',str(E/'publish.py'),'docs: complete weekend replay and summary (99)'],check=True)
 print(final,flush=True)
finally:
 done.set();thread.join()
