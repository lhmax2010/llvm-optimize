import json,pathlib,datetime
B=pathlib.Path.cwd();E=B/'tools/bolt/results/handover-20261114'
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
def read(n):return json.loads((E/n).read_text())
def lk(n):return '['+n+'](../../tools/bolt/results/handover-20261114/'+n+')'
items=[]
def add(n,s,e,b,a,r='L'):items.append(dict(item=n,status=s,evidence=e,blocker=b,next_action=a,resource=r))
add('Gerrit第一批上传/评审','PARTIAL','81；gerrit-361395/6/7.json','待评审；REST完整性UNKNOWN','只读跟踪NEW/PS1，不主动加评审人')
add('入口跟进82','PARTIAL','82；entry-copy-drift.json','B完成，W执行副本仍旧','下次使用前另行授权同步并复核')
add('产品加固§7.18','NOT STARTED','v9§6/7.18','需单独产品任务及资源授权','先列压缩节头/零宽/RELR/架构及信号日志修复计划','S')
add('claims补PS10一句','BLOCKED','claims-step-stop.json','给定的整条条件相同前提不成立','PM批准准确措辞后再补，不改代码')
add('T/D规范化描述','DONE','83','仅描述不是归因','复用已验证比较器，保留原始名单')
add('D report-stale','BLOCKED','83；v9§2.4','约10GB单进程，需要资源报备','先提交运行/磁盘/停止线方案','R')
add('337零size符号','PARTIAL','83','无函数字节范围','只读分类别名/边界，不能算作已证明机器码相同','S')
add('68项源文件定位','BLOCKED','83','输入无DWARF/可用STT_FILE','核对匹配符号/中间物；没有就UNKNOWN','S')
add('T/D因果实验','NOT STARTED','v9§2.2；83','实验矩阵及资源待批','冻结变量/身份，先比较已有材料，不预设debug或快照原因','F')
add('84已有资源拆分','DONE','84；resource-reference.json','不包含未采集项','保留来源独立表，不混测、不排序')
add('84 UNKNOWN补采','PARTIAL','84','新构建须授权','先设计命令起止、memory.stat、子进程VmHWM和分层du采集','S')
add('V1b/V2身份方法','NOT STARTED','v9§2.5；67','恢复输入不等于方法跑通','冻结输入，核对V1b无BOLT与V2材料；缺构建则先申请','F')
add('四组合身份矩阵','NOT STARTED','v9§2.5','方法/profile/资源','T/D各四组合，对象+退出码+stderr；90输入、30+C、100BC、小样本/PCH/模块/ThinLTO','F')
add('发货库/工具/消费者验收','NOT STARTED','v9§2.5','乙一产物未实现','冻结ABI、共享/静态消费者、lld/ar输入；另测消费者性能内存','F')
add('资源报备§2.4','PARTIAL','58/59/74/84','需要PM批准，平台上限未知','分编译器构建/编译其他包/消费者运行三类，不下可接受结论','S')
add('乙一离线成对生成','NOT STARTED','v9§2.2；59','已有实验不等于产品入口','定义同一PGO clang采集BOLT、可再生入口/许可/责任','P')
add('乙一清单与输入身份','NOT STARTED','v9§2.2；§7.3/12','认证强制范围待裁决','先列源码/参数/工具链/配置摘要schema及拒绝用例','S')
add('乙一配置头审计','NOT STARTED','v9§2.2','需明确影响结果的配置','只读列配置头和摘要覆盖范围','S')
add('乙一spec接入','NOT STARTED','v9§2.2；§7.1/2/11','产品修改未授权、交付选择待裁决','先列默认关闭开关与profile组合表','S')
add('乙一PGO作用范围','NOT STARTED','v9§2.2；§7.6','发货库变化需PM接受','盘点目标属性；运行库排除，静态库变化单列','S')
add('乙一转换器PGO分类','NOT STARTED','v9§2.2','真实参数及实现次序待安排','只读枚举token/metadata再提分类用例，未知项不默认接受','S')
add('PGO覆盖计数方法','BLOCKED','v9§7.13；58','无认证方法/阈值','先验证覆盖计数和留出集，不能借用BOLT 5%','S')
for n,t in {1:'BOLT profile交付乙一/乙二',2:'PGO profile交付',3:'未认证身份处理',4:'新段与体积上限',6:'PGO作用范围/发货库',7:'第二类内存幅度',10:'分配器新增依赖',11:'PGO关闭的BOLT profile',12:'身份强制范围',13:'PGO匹配率/留出集阈值'}.items():
 add('§7.'+str(n)+' '+t,'BLOCKED','v9§7.'+str(n),'需要PM裁决；推荐不是批准','提供现有证据及选项；6/12/13未决前PGO不得默认开启','PM')
add('两处nop改写','BLOCKED','v9§8；59','可达性与定向输入未解释','定位AArch64/x86函数，与非PGO日志对照；再申请定向验证','S')
add('1551条relocation警告','BLOCKED','v9§8；59','尚未逐类解释','先聚合目标节/符号和风险，不宣称无害','S')
add('830条计数器耗尽','BLOCKED','v9§8；58','是否进入发布profile UNKNOWN','对profraw/合并清单追溯；缺失不能推断，重采需批准','S')
add('每周tizen_base','DONE','weekly-tizen-base.json','仅本周B','下周只读重查HEAD/tree/非merge，不更新本地分支')
add('资产来源许可责任','PARTIAL','v9§6；47/58/59','实验有记录，产品维护未闭环','确定责任人、许可、更新条件、受限根内可获得性','S')
add('三层测速/QB A/B','NOT STARTED','v9§3/6/8','PGO验收及用户操作','冻结训练外输入和配对统计，历史训练集噪声数据非最终结论','P')
add('资源候选/第二批发布','NOT STARTED','v9§4.2/6','84缺数据、资源和评审','补采后选2–3项实证口径A，不预排收益','F')
add('两干净根可复现性','NOT STARTED','v9§2.5','乙一实现和资源','固定profile SHA/清单比较ELF和payload','F')
add('第二批其余验收','NOT STARTED','v9§2.5/6','新产物和授权','T/D、install/LLDB、安全debuglink、accel、安装后CMake两类消费者、QB全架构','F')
(E/'open-items.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
txt='''# 85：PM 交接快照（2026-11-14）

**结论：盘点 PARTIAL，不推进产品。** 三条 Gerrit change 仍 NEW/PS1，sandbox与上传链一致；本周tizen_base为verdict B。82修复已在证据仓库B，但 **W执行副本仍旧**。claims补句因条件不相同而STOP，原文件未改。扩展旧仓库盘点OOM、REST查询不可用，相关范围UNKNOWN。

本报告是时点快照。历史失败、原始结果和后续PM裁决分别保留。参数一致、转换输出一致、整包一致是不同证明；69号重放7706条不等于重新转换7706成员。

## 1. 范围与读过/没读过

W=/home/linhao/Toolchain/development/llvm-optimize；B=/home/linhao/Toolchain/development/llvm-optimize-bolt。长期状态文件为B的docs/bolt/STATUS.md，W的main不是当前bolt-v4交付版。

已读：STATUS署名与最新记录；v9§2.2/2.4/2.5/6/7/8；81–84结果；下述Git状态、只读远端/查询、机器/进程/目录证据；PS10/fea转换器对应条件。历史结果不冒充重跑。

未做：构建、测试、重新比较RPM/IR、访问QB、Gerrit评论/投票/改评审人、LLVM fetch/分支修改/推送、锁获取/释放、清理、VS Code变更；未读凭据文件或创建凭据；未审计其他会话/私人笔记。只使用既有SSH认证，REST失败不引入新凭据。

分析串行用户服务：MemoryMax=4G、MemorySwapMax=0、Nice=19、IOSchedulingClass=idle。只读Git设置GIT_OPTIONAL_LOCKS=0；唯一写入为B的证据/报告及STATUS追加，提交推送仅B bolt-v4。用户明确允许“仅终止本次超时du”，du每次8秒，超时UNKNOWN，不推算。没有主动向其他现场进程发信号；服务005被系统OOM终止，原文见§7。

## 2. 仓库与远端

### 2.1 W/B与LLVM工作树

'''
txt+='|工作区|分支|采集时HEAD|状态|\n|---|---|---|---|\n'
for k,d in read('workspaces.json').items():
 txt+=f"|{k}|{d['branch']['stdout'].strip()}|{d['head']['stdout'].strip()}|porcelain {len(d['status']['stdout'].splitlines())}行；stash {len(d['stash']['stdout'].splitlines())}条；相对本地remote-tracking未推送 {len(d['unpushed_vs_local_remote_tracking']['stdout'].splitlines())}条|\n"
txt+='''
W已跟踪修改为gbs_llvm.conf，未还原。B开始时已跟踪文件干净；未跟踪项包括历史未压缩结果及本次采集文件，不一并提交。未推送数按本地refs，不代表全体历史对象已发布；另查GitHub main/bolt-v4实时HEAD与当时W/B一致。
'''
txt+=lk('workspaces.json')+'；'+lk('evidence-ls-remote-before.json')+'；'+lk('W-gbs-config-local-diff.json')+'\n\n'
txt+='|LLVM工作树（W/temp下）|分支/HEAD|dirty|\n|---|---|---|\n'
for d in read('llvm-workspaces.json'):
 txt+='|'+d['path'].split('/temp/')[-1]+'|'+(d['branch']['stdout'].strip() or 'DETACHED')+' / '+d['head']['stdout'].strip()+'|'+('是' if d['status']['stdout'] else '否')+'|\n'
txt+='''
每个工作树的worktree list、HEAD、porcelain、stash、分支/remote-tracking及未推送列表均保存在JSON。共享仓库本地分支：bolt-on-359934=fea0fe46、hq-463c9a13-probe=9e39fa8a、tizen_base=f999bd40；**本地tizen_base陈旧，不等于远端61ef5d31**。r6副本的本地bolt-on-359934也为fea。新上传链在detached工作树。fea等相对旧remote-tracking列作未推送，不等于从未上传；81记录了同tree重建。

发现32个仓库位置，其中以上5个保存完成；另外27个旧仓库扩展扫描OOM，汇总未写出，记UNKNOWN，不能声称均干净或无未发布内容。没有重试。
'''
txt+=lk('llvm-workspaces.json')+'；'+lk('discovery.json')+'；'+lk('oom-scope.json')+'\n\n'
txt+='''### 2.2 实时远端与每周核对

- sandbox/lhmax2025/bolt_pgo：2cdd37ff747765e99c2befa3e6e8a88663ab77fe
- tizen_base：61ef5d31ca91025c414c748477bef0c64ddfa67c

13c3e223为祖先；区间仅合并提交，--no-merges为空；两棵tree均087e06cf9c79c571c711af8a07057496940ae73d，内容diff为空。**verdict B**。对象已在本地，未fetch。未来内容变化要重新评估改接/认证，不自动继承本次结论。
'''
txt+=lk('llvm-ls-remote.json')+'；'+lk('weekly-tizen-base.json')+'\n\n'
txt+='|Change|状态/PS|revision|依赖|\n|---|---|---|---|\n'
for n in [361395,361396,361397]:
 d=next(x for x in read(f'gerrit-{n}-parsed.json') if 'number' in x)
 txt+=f"|[{n}](https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/{n})|{d['status']}/PS{d['currentPatchSet']['number']}|{d['currentPatchSet']['revision']}|"+','.join(str(x['number']) for x in d.get('dependsOn',[]))+'|\n'
txt+='''
SSH query包含--current-patch-set、--patch-sets、--all-approvals、--all-reviewers、--dependencies、--comments。各返回一条顶层评论“Uploaded patch set 1.”，时间1794500787；没有返回allReviewers或approval项。**不把未返回解释为所有Label配置/投票为0，也不把行内评论完整性宣称已证实。** REST detail/comments/reviewers均404，尝试一次根路径修正仍404；独立REST完整性UNKNOWN，不再绕过访问。
'''
txt+='；'.join(lk(f'gerrit-{n}.json') for n in [361395,361396,361397])+'；'+lk('gerrit-rest-root-check.json')+'\n\n'
txt+='''## 3. 机器与现场

20逻辑CPU；MemTotal=32,297,772kB；SwapTotal/SwapFree均4,194,300kB。本次服务swap0。

|路径|文件系统|可用B|说明|
|---|---|---:|---|
|/home|/dev/sda1|69,934,309,376|约65.13GiB，使用97%|
|/var/tmp|/dev/nvme0n1p1|152,047,968,256|使用69%|
|/home/abuild|不存在|UNKNOWN|仅可报最近存在父目录/home；不是构建根内同名路径|

/home低于历史两根151.3GiB阈值约86.17GiB。不是新预算或清理授权；后续需重新报备。
'''
txt+=lk('machine.json')+'\n\n'
txt+='''用户service/scope、timer和cron原文保存。修正后的ps采样没有匹配gbs/ninja/llvm-bolt/python/rpmbuild且elapsed≥60秒的长进程，仅代表该时点和筛选范围。桌面scope和系统服务仍在。原ps的--ww无效，一次准备修正为-ww成功，旧输出保留。用户crontab无条目；timer含firmware notifier及launchpadlib cache cleaner，系统cron另列。末次unit快照含本任务服务和005失败记录，不代表产品失败。

锁只列路径和拥有者：qb-install-20261105根中的.rpm.lock（root）、local-full-r6-20261111-install根中的.rpm.lock（linhao），均空文件。遍历有深度/剪枝限制及权限盲区，不声称没有其他锁；存在锁文件也不代表被持有。不探测获取、不删除、不解锁。
'''
txt+='；'.join(lk(n) for n in ['services-processes.json','processes-corrected.json','long-process-summary.json','scheduled-config.json','units-at-handover-end.json','lock-files.json','process-preparation-fix.diff'])+'\n\n'
txt+='''## 4. 保留的根与大目录

223条：W/temp一级、B/results一级及指定构建根。193条du成功、29超时、1其他错误，共30UNKNOWN。父子目录重叠，不能相加。全部记录含时间、路径、大小/UNKNOWN、du原文、文档引用行、用途及保留判断。无引用命中不是无用途。

下面列>5GiB和当前重要根。**不是删除清单**：当前输入/profile用于后续归因和真实样本；旧比较/备份/ARM实验唯一性未完整核实，暂保留。
'''
txt+=lk('directory-inventory.jsonl')+'；'+lk('directory-summary.json')+'\n\n'
txt+='|W/temp相对路径|du字节|用途/依据和需要程度|\n|---|---:|---|\n'
purpose={'local-full-r6-20261111-compare':'74/79逐包比较；后续归因暂保留','local-full-r6-20261111-materials':'74/83 BOLT输入；必须保留','pgo-profiles-keep-20261102':'58/64 profile保全；830追溯需保留','tu-inputs-restored-20261106':'67固定输入；必须保留','deleted-repo-backup-20261105':'64/66源码保护；替代物未全验，保留','qb79-local-resume-20261112':'79源码分类；保留','dwarf-check-20261106':'67逐节规则证据；保留'}
needed=['night-20261103','night-20261105','rebase-359934-20261111-r6',*purpose]
for l in (E/'directory-inventory.jsonl').read_text().splitlines():
 d=json.loads(l); p=d['path'];name=p.split('/temp/')[-1];s=d.get('size_bytes')
 if '/temp/' not in p or not ((isinstance(s,int) and s>5*1024**3) or name in needed or name.startswith('rebase-359934-20261111-r6/') or name.startswith('night-2026110')):continue
 refs=', '.join(x['file'].split('/')[-1] for x in d.get('references',[])[:2]) or '用途文档未定位，需PM确认'
 txt+=f"|{name}|{s}|"+purpose.get(name,refs+'；基线/实验/历史证据，暂保留')+'|\n'
txt+='''## 5. 本地上下文与过时状态

- W留有gbs_llvm.conf修改、旧设计副本、53号未压缩大JSON；B也有历史未跟踪结果。逐路径清单含状态、大小和小文件SHA；有同名.gz只登记位置，未做解压内容等价检查，不能据此删副本。
- B的82修复与W执行副本5处SHA不同：run-night.sh、test_serial.py、basedev/launcher.py、README、SHA256SUMS。下一次入口使用前须先授权同步和复核，本任务不做。
- PGO乙一/产品加固：5个活跃工作树干净，未找到可确认的独立半成品；47/58/59实验脚本、PGO+BOLT材料和保全profile不是产品乙一。27旧仓库未知，不能声称全盘没有未发布工作。
- v9§6仍写81“待上传”，实际已NEW/PS1；82在B完成、W未同步；claims仍待补且本次前提不符。设计正文不改。
- STATUS中的旧FAIL/NOT RUN、旧sandbox SHA是历史：79最终B1–B6 PASS、81上传链、82–84是最新入口；源码原始FAIL与双维度裁决PASS分别展示。
- 历史一次性的构建、清理、sandbox/refs-for授权不延续到85/第二批。新PM只读GitHub，本地路径不是完整交付；大实物仍依赖该机器。POSIX sh、平台loader、原始失败保留等偏好汇总到context JSON。
- 本轮直接裁决：允许仅终止本次超时du。没有可确认应覆盖v9却未入证据的额外产品裁决；其他会话和私人笔记未查，不能声称不存在。
'''
txt+='；'.join(lk(n) for n in ['local-only-files.json','entry-copy-drift.json','pgo-hardening-candidates.json','context-only-instructions.json'])+'\n\n'
txt+='''## 6. 未结事项总表和11/16起顺序

状态限已审计范围。DONE仅指表中范围。以下资源是**下一最小动作的规划估计，不是实测或授权**：
L=只读整理10–60分钟、≤4GiB、0–1GiB新证据；S=分析/方案0.5–1人日、≤4GiB、1–5GiB，超过另报；PM=裁决耗时UNKNOWN、无计算。
R=report-stale单进程约10GB、时长/磁盘UNKNOWN，需报备。
F=新构建时长/内存/磁盘待报备；74历史T7875s/D3901s不是新版本保证，T受回收影响；151.3/177.6GiB历史预算仅参考。
P=PGO资源需批准；58/59历史普通阶段约13.3e9B、BOLT插桩约17.0e9B VmHWM，时长/磁盘须按方案重算。

|事项|状态|证据|阻塞；最小下一步|资源|
|---|---|---|---|---|
'''
for x in items:txt+='|'+x['item']+'|'+x['status']+'|'+x['evidence']+'|'+x['blocker']+'；'+x['next_action']+'|'+x['resource']+'|\n'
txt+='''### 84的UNKNOWN怎么补

|缺项|旧材料边界|下次构建采集要求|
|---|---|---|
|QB ThinLTO链接起点|结束进度不能倒推|平台允许时记录命令起止/目标ID，不擅改QB|
|rewrite/strip/独立门禁耗时|只有窗口则保留窗口|逐步骤单调时钟起止、命令|
|全构建单进程峰值|llvm-bolt专项不等于全局|子进程退出rusage/命令，加存活峰值采样|
|anon/file|旧未保存就UNKNOWN|memory.stat定期及阶段边界记录|
|分层磁盘/du缺口|成功样本最大值是下界|分层限时du、失败计数、文件系统已用量短周期采样|
|T未受限峰值/时长|不能由触顶值反推|先报备，不自行提高内存重跑|

74-T memory.peak=24,482,992,128B，标“≥限额（截断）”；max3877、oom0，时长受内存回收影响。T的67,924,271,104B磁盘峰值仅91个成功样本最大值，32次超时。D memory.peak=18,161,836,032B、max0。字段/来源行号与时间见resource-reference及84；QB与本地不混算。

### 建议第二批顺序（不是执行授权）

1. 新PM先确认UNKNOWN和claims措辞；只读跟踪Gerrit，维持第一批tree。
2. 下次入口使用前，授权同步B的82修复到W；先资源报备/磁盘计划，不自发清理。
3. 冻结V1b/V2方法和输入、PGO覆盖/配置摘要方案；先用已有材料整理nop/1551/830、零size和源文件定位。
4. 获资源批准后做D report-stale及因果矩阵，为§7.12/13提供依据，不预设原因。
5. PM裁决§7.1/2/3/4/6/7/10/11/12/13；6/12/13未决PGO默认关闭。再授权乙一和独立加固补丁，各自评审/真实样本验证。
6. 轻检查/报备通过后才做T/D、四组合、消费者、两根可复现性和install/LLDB；QB另需用户操作授权。tree改变不继承整包认证。
7. 补齐资源后再选2–3候选并实证口径A；三层留出/配对统计后才QB A/B。日期到来不等于发布门槛通过。

§7其余条款：8是冻结双维度规则；15的ARM例外已有77证明；16旧衔接被74最终tree实构建取代；17主性能对象为Toolchain；18已裁决跟进但未实现；5/9是验收要求，不能由建议推断新的放宽。§8的快照漂移、训练集测速噪声、profile交付体积、理论产物不变仍需实证、QB资源上限未知，均不能从已上传推定已解决。
'''
txt+=lk('open-items.json')+'；'+lk('resource-reference.json')+'\n\n'
txt+='''## 7. STOP和盲区原文

### 步骤5：claims保持不动

PS10（13c3e223）转换器第376行：

    if symbol[3] != 0xfff1 and (kind in (10, 11) or (kind == 1 and not target[2] & 1)):

fea0fe46第533行：

    if symbol[3] != 0xfff1 and (kind in (10, 11, 12, 14) or (kind == 1 and not target[2] & 1)):

STOP：

    PS10 line376 full condition differs from fea0fe46 line533 (kind 10,11 versus 10,11,12,14); required equality not met

整条条件不同，不能写“条件相同”。既有32/64位子条件保留与整条相同不是同一判断。仅停止步骤5，继续交接；claims未改，SHA256=d65c382f1d773a9593db45e9f607a3757750f85f73fd7ddfd4ed0a63417fcdca。建议PM批准准确表述后再补。
'''
txt+=lk('claims-step-stop.json')+'；'+lk('claims-ps10-check.json')+'；'+lk('claims-preserved.json')+'\n\n'
txt+='''### 旧仓库扩展OOM（未重试）

    Finished with result: oom-kill
    Main processes terminated with: code=killed/status=TERM
    Service runtime: 5min 20.887s
    CPU time consumed: 2min 9.740s
    Memory peak: 4.0G
    Memory swap peak: 0B

服务005已保存机器/服务/目录发现；扩展旧仓库汇总未写出，UNKNOWN。未提高上限或重跑。后续仅做独立查询/du/报告。
'''
txt+=lk('machine-stop.json')+'；'+lk('oom-scope.json')+'\n\n'
txt+='''REST404和du错误见原文。准备问题：ps参数修正一次；REST路径修正一次仍失败；收尾先读取尚未生成85文件失败、误将STATUS放在仓库根的读取失败，均未修改历史内容。正确路径为docs/bolt/STATUS.md。另一次工具请求JS语法错误未执行任何shell。这些不产生产品结果。

## 8. 交付索引

所有本次文件的bolt-v4 raw链接见[RAW_LINKS.md](../../tools/bolt/results/handover-20261114/RAW_LINKS.md)。GitHub可直接读取JSON/原文；大产物仅登记，不复制。唯一既有文件修改是STATUS追加；claims因STOP不变。报告≤30KB、暂存单文件≤10MB，提交前核对并记录。
'''
txt+='\n85 盘点已结束 '+now+' status=PARTIAL（步骤5 STOP；旧仓库扩展/REST完整性UNKNOWN）\n'
p=B/'docs/bolt/85_handover_snapshot.md';assert not p.exists();assert len(txt.encode())<=30000,len(txt.encode());p.write_text(txt)
print('report bytes',p.stat().st_size,'open items',len(items))
