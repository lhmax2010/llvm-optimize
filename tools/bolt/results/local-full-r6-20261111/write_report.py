from pathlib import Path
import json,gzip,datetime,collections,hashlib
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize';E=Path(__file__).parent
doc=B/'docs/bolt/74_local_full_build_fa4f9978.md'
assert '## 8. 入口修正与完整构建（fea0fe46）' not in doc.read_text()
def j(p):return json.loads(p.read_text())
def link(path,label=None):return '['+(label or path)+'](../../tools/bolt/results/local-full-r6-20261111/'+path+')'
def block(t):return '\n~~~text\n'+t.rstrip()+'\n~~~\n'
a={p:j(E/p/'audit.json') for p in ('toolchain','basedev')}
raw={p:j(E/p/'log-audit-raw.json') for p in a}
pkg={p:j(E/p/'comparison/packages.json') for p in a}
lines=[]
def add(s=''):lines.append(s)
add('\n\n## 8. 入口修正与完整构建（fea0fe46）')
add('\n本节记录 2026-11-11 夜间启动、2026-11-12 完成的实际结果，前面的停止与演练记录均保留。**T/D 两次 GBS 完整构建成功且无 OOM；指定 QB 的二进制包比较为 T 22/22 口径 B PASS、D 12/12 原始载荷相同。两份源码包原始比较仍为 FAIL，差异归因逐项列在 §8.6，未扩充比较器白名单。** 安装测试中 21 个 clang 崩溃帧全部具名并完成符号化交叉核对。')
add('\n原入口自动验证仍报告 T failed、D ok，不能把本次补充比较改写成原队列全绿。T 的失败发生在旧 QB 基线的包比较，GBS 自身 exit_code=0；本轮按指定 QB 1225393/1225395 另做比较。')
add('\n证据总目录：'+link('','local-full-r6-20261111/')+'。源码始终为 fea0fe464d56e17f2c7588c557bfffd9f6ac352b / tree b2e8af2477cf623a945aa80bf8288a262dd4a5a9，detached 且工作树干净；'+link('source-final.json','收尾复核')+'。未推送 Gerrit/sandbox、未操作 QB、未删除文件，旧构建根和产品源码未改。')
add('\n### 8.1 串行调度修正与测试')
add('\n只修改获准的 r6 run-night.sh、basedev/launch.sh、README、provenance、SHA256SUMS 与新增入口测试；两个 launcher.py、资源设置、门禁、比较器及原 r2 未改。B 发布副本与 W 执行副本一致。')
add('\n- launch.sh 非零即停队列：129/130/143 原样传递，其他转 2，不启动 D。\n- controller 终止后再查询该项目所有 full-* 服务；active/activating/deactivating、查询失败、result.json 缺失或无效均停止。\n- T 的有效结果为 failed/stopped 且全部服务已结束时继续 D；D 启动前再次要求 /home ≥80 GiB。\n- 所有停止路径打印项目和队列结束行；dry-run 不创建根或启动服务。\n- Base-Dev 删除 legacy night 和 rehearsal toolchain，仅接受 full/rehearsal/rehearsal-02 basedev；usage 同步。')
add('\n'+link('entry-changes.diff','完整入口 diff')+'；'+link('run-night.sh.diff')+'；'+link('basedev-launch.sh.diff')+'。')
tests=j(E/'tests.json')
add('\n全部测试 **98 项：96 PASS，2 项原有不适用 SKIP，0 FAIL/ERROR**。其中原有 82 项（80 PASS、2 SKIP），新串行 mock 16/16 PASS；没有把跳过写成通过。旧测试期望没有改，路径副本差异保存在证据目录。新增 mock 覆盖用户八类场景，另覆盖信号状态、空服务状态、无效结果、根已存在和 legacy 分支拒绝。')
add('\n|项目|套件|总数|PASS|原有 SKIP|\n|---|---|---:|---:|---:|')
for t in tests:add('|'+ '|'.join(map(str,[t['project'],t['suite'],t['count'],t['count']-t['skipped'],t['skipped']]))+'|')
add('\n'+link('tests.json')+'、'+link('test_serial.stderr','16项测试原文')+'。测试生成器曾在写入测试前因嵌套引号产生 SyntaxError，只改生成器字符串边界，没有改测试判定；'+link('test-generator-preparation.txt','原始准备错误')+'。')
add('\n### 8.2 启动、Linger 与队列原文')
add('\n启动前源身份、干净状态、无其他任务、完整根不存在均通过；/home 239.601 GiB ≥151.3 GiB。'+link('preflight.json')+'、'+link('services-before.txt')+'。Linger=no（'+link('linger.txt')+'），启动时已明确告知：**构建期间不要注销登录**。')
add('\n只执行一次后台调度命令：'+block('systemd-run --user --unit=rebase359934r6-night-20261111 --collect /bin/sh /home/linhao/Toolchain/development/llvm-optimize/tools/bolt/rebase-launch-20261111-r6/run-night.sh fea0fe464d56e17f2c7588c557bfffd9f6ac352b'))
add('\n调度、T、D 串行；没有重试。完整构建沿用原入口 MemoryMax=24482992128 B（MemTotal−8 GiB）、swap=0、CPUQuota=1200%、Nice=10、IO 2/7。入口自带的自动验证也由原 controller 执行，仍使用原入口配置；本轮随后新增的审计、包比较、函数比较和安装检查均在独立 8 GiB / swap 0 / CPU 400% / Nice 19 / IO idle 服务中串行运行。没有调整内存限制。')
add('\n监控连接约 00:02 断开，恢复连接时已是 11:36，期间服务独立完成；没有声称全程人工持续观测。原 night.log 和资源采样保留。恢复时只读查询，没有重启或干预构建服务。')
ends='\n'.join(l for l in (E/'night-final.log').read_text().splitlines() if '已结束' in l)
add(block(ends))
add('\n'+link('night-final.log','完整 night.log')+'、'+link('night-launch-command.json')+'、'+link('services-final.json','结束后服务状态')+'。')
for p in a:
 add('\n**'+p+'**：GBS exit_code='+str(a[p]['build_result']['exit_code'])+'，构建 '+str(round(a[p]['build_result']['seconds'],3))+' 秒；controller '+a[p]['controller_result']['status']+'。')
 v=j(E/p/'entry-validation-result.json')
 add(block(json.dumps(v,ensure_ascii=False,indent=2)))
 if (E/p/'failure.txt').exists():add(block((E/p/'failure.txt').read_text()[-2200:]))
 add(link(p+'/build-result.json')+'；'+link(p+'/entry-validation-result.json')+'。')
add('\n### 8.3 构建审计与最终参数')
add('\n|检查|T / QB 1225393|D / QB 1225395|\n|---|---|---|\n|GBS 完整构建|PASS|PASS|\n|log-restarts|0|0|\n|FLAGS 去时间前缀后逐字比较|相同|相同|\n|FLAGS_WARNING|0|0|\n|shell not found / NATIVE_ARCHIVES_CANCELLED / BOLT_CANCELLED|0|0|\n|BOLT_POST_GATE_PASS 之后 post BOLT_DISK_REPORT|存在|存在|\n|NATIVE_ARCHIVES_END|PASS 225|PASS 225|\n|converted / preserved|3853 / 11|3853 / 11|\n|compiler / disassembler / nm 版本|22.1.8 / 22.1.8 / 22.1.8|22.1.8 / 22.1.8 / 22.1.8|\n|与对应 QB 的 profile 计数|相同|相同|')
for p in a:
 add('\n**'+p+' 原文**（L 为 GBS 原始日志行号）：')
 take=raw[p]['flags']+a[p]['tools']+a[p]['native_end']+raw[p]['post_gate']+[x for x in raw[p]['disk_reports'] if x.get('data',{}).get('stage')=='post']
 add(block('\n'.join('L'+str(x['line'])+': '+x['text'] for x in take)))
 add('\nprofile N/M/S/U/Q/R：'+block(json.dumps(a[p]['profile_records'][0]['data'],ensure_ascii=False)))
 add('\nCMake 前最终环境变量赋值原文：'+block('\n'.join('L'+str(x['line'])+': '+x['text'] for x in a[p]['final_flags'].values())))
 add('\n'+link(p+'/required-log-excerpts.txt','全部门禁与 post 摘录')+'；'+link(p+'/original-build.log.gz','完整 GBS 原始日志')+'；'+link(p+'/audit.json','审计及 QB 对照')+'。')
add('\n逐 token 比较：CFLAGS、CXXFLAGS 都只有 T 多出 -g2、-gdwarf-4、-g，移除这三个调试 token 后顺序和重复次数也完全相同；D 没有额外 token。两边架构参数都为 -m64 -march=nehalem -msse4.2 -mfpmath=sse，没有 -mtune。LDFLAGS 完全相同：-Wl,-z,relro,--as-needed -Wl,--gc-sections。空格数量在原文中保留，'+link('final-flags-diff.json','token 差异')+'不据此推断 T/D 机器码差异的原因。')
add('\n### 8.4 资源')
add('\n阶段起止按 GBS 原始日志 [NNNNs] 锚点，非采样观察时刻。下表为入口 resource-table.md 原样；各阶段 cgroup 列是采样峰值，含文件缓存，不冒充独立阶段的内核 memory.peak。')
for p in a:
 br=a[p]['build_result'];s=a[p]['resource_supplement']
 add('\n**'+p+'**：全构建内核 memory.peak='+br['stats']['memory.peak'].strip()+' B；memory.events：'+br['stats']['memory.events'].strip().replace('\n',', ')+'。swap peak=0；anon/file 未采集，均 **UNKNOWN**。')
 add('\n'+(E/p/'resource-table.md').read_text())
 add('\n资源样本 '+str(s['sample_count'])+'；du '+str(s['du_samples'])+' 次、50秒超时 '+str(s['du_timeout_count'])+' 次、全部非零 '+str(s['du_nonzero_count'])+' 次。'+link(p+'/du-nonzero-samples.json','非零原文')+'；'+link(p+'/resource-table.json','阶段数据与边界')+'。')
add('\n实际采样方式：约每2秒采 cgroup/文件系统，约每60秒由入口既有 chroot sudo -n 调用 du -sx -B1 /，单次50秒超时。T 的32次超时、其余9次非零样本均未估算补齐；D无超时。未启用入口不支持的10秒/5分钟新模式，构建根占用是成功 du 样本的峰值，下界而非连续精确峰值。T采样磁盘峰值67924271104 B，D14028967936 B；最小文件系统剩余见表。')
add('\n### 8.5 BOLT 输入及改写日志保全')
add('\nELF 副本保存于 W/temp/local-full-r6-20261111-materials/{toolchain,basedev}/reference-relocs-clang-22，来源是各自 helper 实际 pipeline 输入；历史原文件只读。')
add('\n|项目|输入字节数|SHA256|\n|---|---:|---|')
for p in a:
 m=next(x for x in a[p]['materials'] if 'reference-relocs-clang-22' in str(x))
 # Schema comes from copy evidence; get authoritative disassembler input identity.
 z=j(E/'function-comparison'/(p+'-bolt-input-command.json'))
 add('|'+p+'|'+str(z['input_bytes'])+'|'+z['input_sha256']+'|')
 add('\n'+link(p+'/rewrite-bolt.log',p+' BOLT 改写日志原文')+'；'+link(p+'/rewrite-log-copies.json','来源/大小/SHA')+'；'+link('function-comparison/'+p+'-bolt-input-command.json','输入身份')+'。')
add('\n### 8.6 与指定 QB 的逐包比较及源码包归因')
add('\n使用67号§8.1口径B，Release 从两边RPM头取得：本地T/D均1，QB T为2.1、D为5.1。实际RPM身份、VCS和SHA见各项目 comparison/rpm-identities.json。RPM头时间、release、payload mtime分别记录；不借此跳过文件内容。QB下载文件先按77号receipt复核SHA。')
add('\nT的非调试代码/数据保持相同；.debug及其debuglink按已批准release前缀规则通过，所以“口径B PASS”不等于这些调试文件原始SHA相同。D12个二进制包内容SHA全部直接相同。T的debugsource前缀路径映射后文件内容相同。')
add('\n|包|T 对 1225393|D 对 1225395|\n|---|---|---|')
maps={p:{x['package']:x for x in pkg[p]} for p in a}
for n in sorted(maps['toolchain'].keys()|maps['basedev'].keys()):
 add('|'+n+'|'+ '|'.join(maps[p].get(n,{}).get('status','无此包') for p in a)+'|')
add('\n'+link('toolchain/comparison/packages.json.gz','T每文件结果（含允许的逐节差异）')+'；'+link('basedev/comparison/packages.json','D每文件结果')+'。源码包原始FAIL保留，没有为了得到PASS修改规则。')
add('\n每组 llvm-static-devel 的225个归档、3864个实际成员（3853转换+11原样保留）都逐成员计算并比较SHA，全同；合计 **7706个转换成员 + 22个原生成员**。额外连同其他包的归档，每组271归档、5829成员全部通过；完整归档SHA也相同。'+link('toolchain/comparison/static-members.json.gz','T全量成员')+'、'+link('basedev/comparison/static-members.json.gz','D全量成员')+'。这次确实运行了逐成员比较。')
add('\n源码包逐项事实：\n\n- spec/helper/转换器的差异来自 fea0fe46 对60fabc72，完整diff随比较结果保全；spec还含VCS、Release和GBS/QB的Patch/%patch写法差异。\n- Source1200、模型tar、llvm.manifest 的内容SHA相同，只存在0664/0644权限差异；与设计第7节第8条的源码包权限环境差异单列。\n- QB把8个补丁作为独立source文件；本地GBS将已应用补丁的源码直接导出tar，因而没有独立0001–0008。只在新临时目录应用QB八个补丁，27个受影响文件核对通过；没有改历史构建根。\n- 对两个tar逐文件流式核对184839/184826条目。应用QB补丁之后，除下述14项（含一个目录）外，全体路径/type/size/mode/link/内容SHA相同。\n- 本地多出的packaging/目录及12个文件，内容都逐个与 fea0fe46 的git对象SHA相同，属于GBS导出整个Git tree而QB使用上游tar的组织差异。\n- 唯一共有文件差异为 clang/bindings/python/.git_archival.txt：git archive 的提交身份展开。本地node=fea0fe46，QB上游tar node=ca7933e4；原文如下。该差异已经定位，但不把它偷偷加入既有白名单，源码包仍保留原始FAIL。')
src=j(E/'source-container-details.json')
for side in ('local','qb'):add('\n'+side+block(src['toolchain'][side]['git_archival_text']))
add('\n本地tar354741498 B / '+src['toolchain']['local']['sha256']+'；QBtar258009434 B / '+src['toolchain']['qb']['sha256']+'。T/D各自的两个tar SHA均相同，因此同一份内容归因覆盖两组。')
add('\n'+link('source-attribution.json','全部14项差异与补丁清单')+'、'+link('source-extra-packaging-git-check.json','12个packaging文件Git核对')+'、'+link('source-container-details.json','tar及归档标识')+'。tar全文件SHA清单：'+link('source-local-tar-manifest.json.gz','本地')+'、'+link('source-qb-tar-manifest.json.gz','QB原始')+'。没有无法定位的代码文件差异；以上事实不等于未经裁决把源码包改判PASS。')
add('\n### 8.7 T/D 函数差异（只记录事实）')
fun=j(E/'function-comparison/result.json');cats=j(E/'function-comparison/categories.json')
add('\n通过各自构建根的loader运行平台llvm-objdump --disassemble --no-show-raw-insn，在8GiB服务中流式处理成功。按可识别符号名及同名出现序号对齐；去掉指令行首地址，但保留操作数字面地址。计数包含地址引起的文本差异，不能据此认定对应数量的函数算法或性能改变。最终strip后的文件只覆盖objdump仍能识别的符号范围。')
add('\n|比较|T函数记录|D函数记录|完全相同记录|仅入口地址不同|指令文本/条数不同|只在T/只在D的名字|\n|---|---:|---:|---:|---:|---:|---|')
for k in fun:
 f=fun[k];c=cats[k];add('|'+ '|'.join(map(str,[k,f['toolchain_functions'],f['basedev_functions'],f['identical_function_records'],c.get('address_only',0),c.get('instruction_text_or_count',0),str(c.get('only_toolchain',0))+'/'+str(c.get('only_basedev',0))]))+'|')
add('\n完整差异函数名/地址/文本SHA：'+link('function-comparison/bolt-input-different-functions.json.gz','BOLT输入')+'、'+link('function-comparison/final-clang-different-functions.json.gz','最终clang')+'。未归一化 .llvm 数字后缀，没有下因果结论；完整反汇编四份约234–247MB gzip各自留在本地证据目录，'+link('large-local-artifacts.json','完整路径/大小/SHA索引')+'，未上传超GitHub单文件限制的原文；逐函数清单与差异已上传。')
add('\n### 8.8 T RPM 安装与 LLDB')
i=j(E/'install/result.json')
add('\n遵守“不执行额外sudo”：预检rootless bwrap用户namespace可用，在新 W/temp/local-full-r6-20261111-install/root 内实际rpm --initdb、--noplugins --nodeps -ivh安装本次clang与clang-debuginfo。运行库/工具从本次T根只读复制，完整依赖闭包和10条rpmpopt exec预检通过；不是在历史chroot里装包。namespace内uid0只映射当前普通用户，无宿主root权限。')
add('\n这与43号sudo chroot的提权机制不同，测试对象和崩溃方法相同：LLDB仅打开/usr/bin/clang-22，自动加载/usr/lib/debug/usr/bin/clang-22.debug；真实SIGILL崩溃，core关闭。')
add('\n结果：安装SHA与RPM载荷一致，debug文件0644，debuglink CRC32匹配；**21/21 clang帧具名，21/21与llvm-symbolizer同地址名称相同**；另'+str(len(i['cold_samples']))+'个冷函数抽查一致。')
add(block((E/'install/rpm-install.stdout').read_text()))
add('\n安装身份：'+block(json.dumps(i['installed_sha256'],indent=2)))
add('\n'+link('install/lldb-auto.stdout','LLDB完整原文（image list/lookup/bt all）')+'、'+link('install/symbolizer.stdout')+'、'+link('install/result.json','21帧/冷函数逐项及清理')+'、'+link('install/copied-files.json.gz','复制来源与SHA')+'；完整argv保存在install/*-command.json。')
add('\n清理：所有bwrap进程已返回，临时proc/dev等namespace挂载随退出回收，未做宿主挂载/卸载。findmnt返回0，无测试根挂载；可读/proc中无测试根cwd/root/exe进程。'+str(i['cleanup']['permission_blind_processes'])+'个外部进程有普通用户权限盲区，明确保留这个限制；未提权查看。根和RPM均保留。')
add('\n### 8.9 收尾与边界')
disk=j(E/'disk-final.json')
add('\n/home收尾可用 '+str(disk['free_bytes'])+' B（'+format(disk['free_bytes']/2**30,'.3f')+' GiB）；'+link('df-final.txt')+'。比较解包、函数反汇编、安装根与全部产物均保留，未删除任何文件。')
add('\n原入口自动完成的90 TU结果为T、D均PASS（不是本次额外重跑的检查），其原result已保全。本轮未运行新QB、额外完整构建、性能测量或函数差异因果实验。没有OOM，未提高限制或重试失败构建；T原自动验证失败和源码包原始FAIL均未隐藏。')
add('\n本次结论：构建和指定QB二进制/静态成员验证完成，安装符号检查通过；源码包组织/归档标识差异已定位但严格原比较为FAIL，不能写“整包全部逐字节相同”。')
allends=[ends,(E/'audit.stdout').read_text().strip(),(E/'function-comparison.stdout').read_text().strip(),(E/'install-rootless.stdout').read_text().strip()]
end='LOCAL_FULL_R6 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status=completed_with_differences reason=builds_ok_binary_policyB_pass_source_raw_FAIL_attributed'
add(block('\n'.join(allends+[end])))
doc.write_text(doc.read_text()+'\n'.join(lines)+'\n')
status=B/'docs/bolt/STATUS.md'
status.write_text(status.read_text()+'''
\n## 2026-11-12：fea0fe46 T/D 完整构建、审计与比较完成（74号§8）

串行入口已修正，98项测试：96PASS、2项原有SKIP、无FAIL/ERROR。Linger=no，启动时已告知不要注销。T/D GBS均exit0、无OOM；原队列T=failed（旧自动包比较）、D=ok，原失败保留。新增审计/比较在8GiB受限服务串行完成。

指定QB1225393/1225395：T22/22二进制包按67号口径B PASS，D12/12载荷原始内容相同；各225静态归档的3853转换+11原生成员逐SHA全同，合计7706+22。FLAGS/profile/门禁/工具22.1.8检查通过，T/D最终参数仅差-g2/-gdwarf-4/-g。两份源码包原始FAIL保留：GBS合并源码tar vs QB八补丁、packaging目录及.git_archival提交标识的差异已逐文件归因，未扩大白名单。

T RPM在新的rootless namespace中实际安装，LLDB自动加载符号，21/21 clang帧与llvm-symbolizer一致，冷函数抽查通过；无额外sudo。T/D BOLT输入与改写日志已保全，函数差异清单已生成，只记录事实。资源数据及UNKNOWN、du超时见[74号§8](74_local_full_build_fa4f9978.md#8-入口修正与完整构建fea0fe46)。全部根/副本保留，无Gerrit/sandbox推送或QB操作。
\n'''+end+'\n')
(E/'task-end.txt').write_text(end+'\n')
print(end);print('report_bytes',doc.stat().st_size)
