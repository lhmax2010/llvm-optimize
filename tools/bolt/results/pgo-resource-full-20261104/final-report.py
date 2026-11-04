"""Render finished-run evidence, preserving missing measurements as UNKNOWN."""
from pathlib import Path
import json,datetime,re,hashlib,gzip
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt'); E=Path(__file__).parent
D=B.parent/'llvm-optimize/temp/pgo-resource-20261102/full'
s=json.loads((D/'resources-summary.json').read_text());rows={r['stage']:r for r in s['stages']}
def gi(n):return f'{n/1024**3:.3f}'
def dt(n):return datetime.datetime.fromtimestamp(n/1e9,datetime.timezone(datetime.timedelta(hours=8))).isoformat()
def val(v,key):return v[key] if isinstance(v,dict) else None
def sz(n):return f'{n:,} B ({gi(n)} GiB)' if isinstance(n,(int,float)) else 'UNKNOWN'
log=D/'stage-D/gbs-driver/local/repos/tizen_base_toolchain_standard/x86_64/logs/fail/llvm-22.1.8-1/log.txt'
work=D/'stage-D/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt'
bolt=work/'rewrite/bolt.log'; excerpt=[]
for p in [log,bolt,D/'controller.stdout']:
 with p.open(errors='replace') as f:
  for i,l in enumerate(f,1):
   if p!=log or any(k in l for k in ('Executing(%build)','Executing(%install)','BOLT_DISK_REPORT','BOLT_PROC_OK','BOLT_NINJA_EXIT_0','pipeline /','BOLT_DISK_DIAGNOSIS','BOLT_GATE_FAILED','Bad exit status','failed "build')):
    excerpt.append(f'{p}:L{i}: {l.rstrip()}')
(E/'failure-and-anchors.txt').write_text('\n'.join(excerpt)+'\n')
profiles=json.loads((D/'stage-A/evidence/profraw.json').read_text());profdata=json.loads((D/'stage-A/evidence/profdata.json').read_text())
ends=[l for l in (D/'controller.stdout').read_text().splitlines() if l.startswith('PGO_RESOURCE 已结束 ')]
assert len(ends)==1
f=json.loads((E/'finished-facts.json').read_text());minimum=f['home_min']
text='''## 3. 最终结果与失败原文

A 插桩 clang、B 的23份训练、C 的 profdata 合并通过。D 普通编译、普通安装、BOLT工具113项构建完成，随后 llvm-bolt 因陈旧 profile 超过5%主动返回1，%install失败。没有重试、手动续跑、改发布参数或放宽门禁；不是磁盘不足或OOM。本轮没有完成PGO+BOLT打包，不能作为完整构建通过的认证。

总结束行（controller.stdout:L2）：

```text
'''+ends[-1]+'''\n```

GBS 原始失败日志 `full/stage-D/gbs-driver/local/repos/tizen_base_toolchain_standard/x86_64/logs/fail/llvm-22.1.8-1/log.txt.gz`：

```text
L23684 [ 7190s] + python3 -B /home/abuild/rpmbuild/SOURCES/clang-bolt-helper.py pipeline /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-bolt --debug-symbols
L23685 [ 7463s] BOLT_DISK_DIAGNOSIS {"cause": "not-disk", "step": "pipeline", "free_bytes": 86711771136}
L23686 [ 7463s] BOLT_GATE_FAILED: COMMAND_FAILED rc=1: /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-bolt (see /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt/rewrite/bolt.log)
L23688 [ 7463s] error: Bad exit status from /var/tmp/rpm-tmp.ZCXagu (%install)
```

根因日志 rewrite/bolt.log 全文如下（原件含行号摘录见 `failure-and-anchors.txt`）：

```text
'''+''.join(f'L{i} {l}'.rstrip()+'\n' for i,l in enumerate(bolt.read_text().splitlines(),1))+'''```

工具返回1，helper没有执行成功日志的match_counts，也没有生成pipeline-result.json。日志直接给出N=18343、M=164430、S=15638、Q=603；没有U行，**U及正式R均UNKNOWN，不能把失败日志中缺失的可选计数当零**。S/N可直接由已打印数字计算，''' + f'{15638/18343*100:.8f}%'+'''，与日志85.3%一致，远超原5%门槛。失效样本比例为98.6%，这是样本权重口径，不与函数数比例混用。

|同口径统计|43号非PGO Toolchain debug|54号T非PGO Toolchain debug|本轮PGO D Toolchain debug（失败日志）|
|---|---:|---:|---:|
|N（带profile函数）|23592|23592|18343|
|M（总函数）|144032|144032|164430|
|S（陈旧函数）|0|0|15638|
|U（忽略profile对象）|1|1|UNKNOWN|
|Q（不能优化函数）|383|383|603|
|R=(S+U)/(N+U)，百分比|0.004238545331%|0.004238545331%|UNKNOWN（成功解析未运行）|
|S/N，百分比|0%|0%|85.25322902%|

基线来自两次保全的pipeline-result.json原件，路径、SHA和原始计数见 `non-PGO-baseline-counts.json`，不是摘要估算。43号与本实验同为3ee2d847基线；54号T为9e39fa8a，存在固定参数/记录变化，因此用作同模式对照而非相同输入认证。Source1200和5%门槛未改：现有非PGO训练profile不适用于本次PGO输入，后续若继续需单独设计重新采样；本轮不实施。

## 4. A/B/C/D资源与耗时

已在总结束后执行47号原始 `report.py` 一次，exit0；完整输出 `report.stdout`、结构化结果 `full/resources-summary.json`，命令见 `report-command.json`。下列cgroup值来自每个独立服务结束前的内核memory.peak，**包含文件缓存**；进程VmHWM来自2秒抽样的所有可读PID，短进程或不可读进程可能漏采，不能冒充完整进程记账。通过loader启动时进程名为ld-linux-x86-64，真实工具见完整cmdline。

|阶段|状态|服务实测耗时s|cgroup峰值|最大进程VmHWM|进程/命令摘要|构建根边界du最大值|/home最小可用|
|---|---|---:|---|---|---|---|---|
'''
cmds={};timings={}
for name in 'ABCD':
 r=rows['stage-'+('D' if name=='D' else 'A')+'/'+name];p=r['process_VmHWM_max'];cmds[name]=p;res=r['result'];timings[name]={'start':dt(res['start_ns']),'end':dt(res['end_ns']),'seconds':r['seconds']}
 command={'A':'ld.lld … -o bin/clang-22','B':'loader … 插桩clang-22，训练0','C':'loader … llvm-profdata merge','D':'ld.lld … -o bin/clang-22（普通编译）'}[name]
 text+=f"|{name}|{'PASS' if res['rc']==0 else 'FAIL：BOLT stale profile'}|{r['seconds']:.3f}|{sz(r['cgroup_peak_bytes'])}|{sz(p['VmHWM_bytes'])}|{p['name']}；{command}|{sz(val(r['root_boundary_disk_max'],'bytes'))}|{sz(val(r['filesystem_available_min'],'available_bytes'))}|\n"
text+='\n完整VmHWM的PID、进程名、命令原文和采样时间见 `process-peak-identities.json`；不是仅采llvm-bolt。服务起止时间见 `stage-times.json`。A耗时包含CMake配置和profile运行库/clang构建；B/C不包含前后记录SHA的时间；prepare服务另列，不混入A/D。\n\n'
for key in ['stage-A/prepare','stage-D/prepare']:
 r=rows[key];text+=f"- {key}：{r['seconds']:.3f}s，cgroup峰值{sz(r['cgroup_peak_bytes'])}，结束根du{sz(val(r['root_boundary_disk_max'],'bytes'))}。\n"
text+='''
D子阶段：耗时同时列日志秒数差和采样器观察时间（服务开始/结束还包括GBS收尾），两者不混用。磁盘只是边界扫描，**所有真实连续峰值UNKNOWN**；普通编译退出/安装入口的扫描90秒超时，7,074,676,736B只是普通编译入口观测，不能据此说编译峰值只有6.59GiB。

|D子阶段|GBS日志区间/差值s|采样观察耗时s|阶段cgroup峰值|最大进程VmHWM|边界du观测|/home最小可用|
|---|---|---:|---|---|---|---|
'''
labels={'setup':'开始→[268s]','ordinary-compile':'[268s]→[6444s] / 6176','ordinary-install':'[6444s]→[6772s] / 328','BOLT':'[6772s]→失败[7463s] / 691'}
for r in rows['stage-D/D']['subphases']:
 p=r['process_VmHWM_max'];cmds['D/'+r['phase']]=p
 disk='UNKNOWN（出口扫描超时；入口6.589GiB）' if r['phase']=='ordinary-compile' else sz(val(r['root_boundary_disk_max'],'bytes'))
 text+=f"|{r['phase']}|{labels[r['phase']]}|{r['observed_seconds']:.3f}|{sz(r['cgroup_peak']['memory_peak_bytes'])}|{sz(val(p,'VmHWM_bytes'))} / {p.get('name','UNKNOWN') if isinstance(p,dict) else 'UNKNOWN'}|{disk}|{sz(val(r['filesystem_available_min'],'available_bytes'))}|\n"
text+='''|cache-release / archive-install / platform-post / packaging|NOT RUN|NOT RUN|UNKNOWN|UNKNOWN|UNKNOWN|UNKNOWN|

锚点：GBS:L345 %build=268s，L10888 %install=6444s，L16467 disk-report begin=6772s，L23683 tool-built=7190s，L23686失败=7463s。工具构建BOLT_NINJA_EXIT_0见L23081；tool-verify报告113/113。pipeline失败早于compare-root、cache-release、静态库转换、平台后处理、打包，不能用此前构建补全后续资源。

本地资源限制：MemoryMax=24,482,979,840B（MemTotal减8GiB），MemorySwapMax=0，CPUQuota=1200%，nice10，ionice best-effort/7；Ninja -j6，GBS外层threads30，三个宏仍为jobs8、_smp_mflags -j8、_costomized_smp_mflags -j20。每阶段systemd-command.json、command.json、service-result.json保存实际值，所有已运行阶段oom/oom_kill为0。systemd-run打印的Memory peak与内核采样值不是同一记录来源，表中统一使用内核memory.peak，不采用其14.4M/512K等尾行值。

C阶段进程VmHWM可大于cgroup记账峰值：两个量分别是进程驻留高水位和cgroup计费，不作加减或相等推断。VmHWM为PID生命周期高水位，阶段内采样不能消去它此前的驻留峰值。

## 5. 训练与profile磁盘数据

'''
text+=f"23/23训练PASS（13 ARM、10 AArch64），生成profraw **{profiles['count']}份，共{sz(profiles['total_bytes'])}**。合并profdata **{sz(profdata['bytes'])}**，SHA256 `{profdata['sha256']}`。两者在阶段A根外的profiles目录，单独列出，不混入根du。profdata另复制一份到D根内，该副本已计入D根占用，汇总时不再重复相加。\n\n"
text+='''profraw阶段末保留量即已观察最大保留量；写入过程没有profile目录连续大小采样，因此瞬时峰值UNKNOWN。profdata亦只记录完成大小，合并过程中临时输出峰值UNKNOWN。完整每文件SHA/逻辑大小/分配大小见 `profile-final-inventory.json`，训练argv和每条结束标记见stage-A证据。工具llvm-profdata使用同源码的full-20261030已有版本，未额外编译目标，身份见profdata.json。

## 6. 两根共存、磁盘下界与清理状态

'''
a=rows['stage-A/C']['root_boundary_disk_max']['bytes'];d=rows['stage-D/D']['root_boundary_disk_max']['bytes']
text+=f"A在B/C边界均为{a:,}B，D退出边界为{d:,}B。D运行期间A不再构建/写入，按这一不变前提组合的**边界记录最大共存根占用为{sz(a+d)}**；这不是同时连续扫描的精确峰值，真实共存峰值仍UNKNOWN。没有把两个历史独立峰值直接当作同一时刻实测值。普通用户结束后du对两个根分别可见{a-4096:,}B和{d-4096:,}B，均exit1、有root属主目录权限盲区，只作下界；完整full目录可见94,775,939,072B，也有同样盲区。没有为补测另行sudo。\n\n"
text+=f"全过程/home最低可用 **{sz(minimum['available_bytes'])}**，时间 **{dt(minimum['time_ns'])}**，D/BOLT阶段，距20GiB停止线仍{gi(minimum['available_bytes']-20*1024**3)}GiB。结束后的df原文：\n\n```text\n"+(E/'final-df.txt').read_text()+'''```

所有原始根、profraw/profdata和失败现场保留。原入口完成正常清理；audit.json中的mounts和remaining_stage_processes均为空。控制器最终failed是D的rc1，不是残留资源或OOM。没有重试、手动启动后续阶段、懒卸载或杀外部进程。

## 7. 证据与外推范围

证据根：`tools/bolt/results/pgo-resource-full-20261104/`。`full-provenance.json`记录所有已归档原件/副本大小、SHA256和gzip状态；大于1MiB文本压缩保存，原始现场不删。`SHA256SUMS`校验本目录交付文件。15项测试原文、预算警告、获批清理的文件清单/检查/df、启动前检查和一次启动命令均在同目录。日志未包含成功的pipeline报告时，明确记录缺失，不制造N/M/S/U/Q认证结果。

这些数值仅代表本机、固定Toolchain快照、3ee2d847及23份训练输入的这一次试验；源码A只构建插桩clang与profile运行库，不能视为一次完整插桩软件包构建。PGO输出大小、profile不兼容事实可用于后续设计；cgroup内存（含缓存）、耗时和磁盘边界下界受并发、内核和机器影响，不能直接当作QB三架构共享磁盘的容量上限。BOLT失败后的缓存释放/转换/打包资源尚无PGO数据。

结论：PGO A/B/C完成；D在原BOLT 5%陈旧profile门禁停止，整套PGO+BOLT构建未通过，保留现场等待用户决定。
'''
# Use the exact calculated value instead of a manually rounded ratio.
text=text.replace('85.25322902%',f'{15638/18343*100:.8f}%')
p=B/'docs/bolt/58_pgo_resource_results.md';old=p.read_text();prefix=old[:old.index('## 3. 最终阶段结果')]
prefix=prefix.replace('实验目前运行中，最终结果待控制器结束后填写。','A/B/C已完成；D在原BOLT陈旧profile门禁失败（85.3% > 5%），未完成打包。没有OOM或磁盘不足，没有重试。')
p.write_text(prefix+text)
(E/'process-peak-identities.json').write_text(json.dumps(cmds,indent=2)+'\n');(E/'stage-times.json').write_text(json.dumps(timings,indent=2)+'\n')
print('REPORT_WRITTEN',p)
