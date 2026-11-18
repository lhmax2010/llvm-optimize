from pathlib import Path
import json,hashlib,gzip,datetime,subprocess
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');E=Path(__file__).resolve().parent
R='../../tools/bolt/results/qb-1232862-1232863/'
def link(label,path):return '['+label+']('+R+path+')'
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(name,obj):(E/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
packages=json.loads((E/'package-results.json').read_text());logs=json.loads((E/'log-summary.json').read_text());arches=json.loads((E/'arch-status.json').read_text());source=json.loads((E/'source-audit.json').read_text())
assert len(packages)==104
binary=[r for r in packages if not r['name'].endswith('.src.rpm')];assert len(binary)==102 and all(r['status']=='PASS' for r in binary)
local=[]
for p in sorted(E.rglob('*')):
 if p.is_file() and (p.stat().st_size>10_000_000 or p.suffix=='.log'):
  local.append({'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p),'reason':'over 10MB' if p.stat().st_size>10_000_000 else 'local execution log (repository ignores *.log)'})
save('local-only-files.json',local)
logmanifest=[]
for row in arches:
 p=E/row['build']/row['arch']/'llvm.buildlog.txt.gz'
 logmanifest.append({'build':row['build'],'arch':row['arch'],'url':row['url'],'file':str(p.relative_to(E)),'bytes':p.stat().st_size,'sha256':sha(p),'raw_bytes':row['raw_bytes'],'raw_sha256':row['raw_sha256']})
save('log-manifest.json',logmanifest)
save('summary.json',{'source':'7a7bc17467d4c5da9763e86e3c74a123b3ff0df2','candidate':'H4','tree':'472c872afe958f464112d22b6304cde006fcbf98','architectures_successful':6,'binary_packages_pass':102,'binary_packages_total':102,'llvm_static_archives_equal':sum(len(r['archives']) for r in binary if r['name'].startswith('llvm-static-devel-')),'new_keyword_lines':sum(len(x['new_keyword_hits']) for x in logs.values()),'cleanup_error_lines':sum(len(x['cleanup_hits']) for x in logs.values()),'source_verdict':'NOT_ASSIGNED: patch Date difference outside helper-only change; full text retained','stop':None})
parts=['# 128号：QB 1232862 / 1232863 核对','',
'结论：两个 QB 实际使用 **H4 `7a7bc17467d4c5da9763e86e3c74a123b3ff0df2`**，tree 为 `472c872afe958f464112d22b6304cde006fcbf98`；不是 H5。六个架构全部成功，**102/102 个二进制包载荷与 H2 基线完全一致**。SESSION_KILL_MODE 全部为 pidfd，REAL/POST 门禁通过，无新增告警/错误类关键字、无会话清理错误文字。',
'',
'两个源码包各有3个文件差异：helper 与 H2→H4 Git 内容完全对应；spec 只变 VCS；导出补丁头的 Date 另有变化。**Date 不属于 helper 内容变更，本报告保留差异原文，不自行豁免，也不对源码包作整体 PASS/FAIL 判定。** 未把此次结果记为 H5 的 QB 验证。','',
'## 1. 身份、构建状态与资源','',
'页面 Build Package List 与公开 manifest 的 llvm revision 均为 H4；tree 来自对应提交的本地 Git 对象，未声称 QB 页面直接提供 tree。'+link('身份/tree','source-tree.json')+'。','',
'|QB|项目|对照 H2 QB|Release|x86_64|aarch64|armv7l|',
'|---|---|---|---|---|---|---|',
'|1232862|Tizen-Base-Dev|1231418|5.1|SUCCESSFUL|SUCCESSFUL|SUCCESSFUL|',
'|1232863|Tizen-Base-Toolchain|1231417|2.1|SUCCESSFUL|SUCCESSFUL|SUCCESSFUL|','',
'版本均为22.1.8。Toolchain 输入快照为 tizen-base-toolchain_20261030.061318；Base-Dev 为 tizen-base-dev_20261030.061217。新旧实际 Release 相同，无需做 release 前缀替换。','',
'两个概览均为 Successful，子构建分别为1232864/1232865；同时取得每个架构 succeeded 目录下的完整 llvm 日志及 finished 行。'+link('架构原文/行号','arch-status.json')+'；'+link('Dev概览','1232862/overview.txt')+'；'+link('Toolchain概览','1232863/overview.txt')+'；'+link('Dev manifest','1232862/manifest.xml')+'；'+link('Toolchain manifest','1232863/manifest.xml')+'。','',
'全部分析作业串行放在 systemd 用户服务中，MemoryMax=4G、MemorySwapMax=0、CPUQuota=200%、Nice=19、IOSchedulingClass=idle；一次性执行，没有资源准入等待/重试。浏览器仅由用户手动登录，未导出凭据、cookie 或会话状态。未操作夜间编排、其他项目、Gerrit 或 sandbox。'+link('执行范围','execution-policy.json')+'。','',
'## 2. 下载和载荷比较','',
'共下载104个RPM（102二进制、2源码），逐包保存URL、大小、SHA256、RPM头VCS及Release。RPM保存在 `/home/linhao/Toolchain/development/llvm-optimize/temp/keep-baselines/qb-1232862-1232863/`；119号把 keep-baselines 列为保留位置。H2基线原件只读复用并重新核对完整SHA。','',
'比较沿用79号/118号解析器：逐文件内容SHA、文件类型/权限、uid/gid和符号链接目标；解析cpio硬链接内容。RPM容器元数据与payload mtime单列，未作为内容差异。新旧包名单无增减。'+link('逐包完整结果','package-results.json')+'；'+link('下载计划','rpm-plan.json')+'；'+link('适配diff','compare-adaptation.diff')+'。','',
'|项目|x86_64|aarch64|armv7l|合计|',
'|---|---|---|---|---|',
'|Base-Dev|12/12 PASS|12/12 PASS|12/12 PASS|36/36 PASS|',
'|Toolchain|22/22 PASS|22/22 PASS|22/22 PASS|66/66 PASS|','',
'llvm-static-devel：每项目 x86_64 225、aarch64 212、armv7l 210，共1294个完整归档SHA全同；这同时证明归档内成员字节相同。本次没有另行解包归档重算每个成员SHA，也未重新做ELF转换/重定位复扫。','',
'### 逐包表','',
'|QB|架构|RPM|文件数|结论|','|---|---|---|---:|---|']
for r in binary:parts.append('|'+r['build']+'|'+r['arch']+'|'+r['name']+'|'+str(r['file_count'])+'|PASS|')
parts+=['','## 3. x86_64 日志原文','',
'每项目 SESSION_KILL_MODE 命中26处：10行实际输出、16行shell赋值/printf跟踪回显，值均为pidfd；不能把26处当成26次独立调用。以下逐条保留原文；行号对应已保存的完整构建日志。',
'',link('完整日志清单与压缩前后SHA','log-manifest.json')+'；'+link('日志汇总','log-summary.json')+'。']
for bid,label in [('1232862','Base-Dev'),('1232863','Toolchain')]:
 c=json.loads((E/(bid+'-critical-lines.json')).read_text())
 parts+=['',f'### {label} {bid}','','```text']
 for k in ['SESSION_KILL_MODE','NATIVE_ARCHIVES_STARTUP','BOLT_REAL_GATE_PASS','BOLT_POST_GATE_PASS']:
  for r in c[k]:parts.append(str(r['line'])+': '+r['raw'])
 parts+=['```','',link('其他关键行及原文',bid+'-critical-lines.txt')+'。']
parts+=['','### 新关键字与清理诊断','',
'按79号已裁决规则去掉行首 `[ Ns]` 时间戳及 Ninja `[N/M]` 进度前缀，再按多重集合比较。全量关键词命中和去掉编译进度行后的命中分别核对，**两者新增均为0**。下面为大小写不敏感的文本命中计数，可能包含shell回显/构建检查文本，不等于运行失败次数；各关键字之间可重叠，不能相加当作独立告警数。','',
'|关键词|Dev旧→新|Toolchain旧→新|新增原文|','|---|---|---|---|']
for key in ['WARNING','warning_colon','error_colon','error_word','not_found','traceback','cancelled','segfault','oom']:
 vals=[]
 for bid in ['1232862','1232863']:
  x=logs[bid];vals.append(str(x['old_keyword_counts'].get(key,0))+'→'+str(x['new_keyword_counts'].get(key,0)))
 parts.append('|'+key+'|'+'|'.join(vals)+'|无|')
parts+=['',
'补充 fatal/failed/failure/exception/cancel/timeout：Dev和Toolchain均旧66→新66，规范化后新增0。'+link('补充命中索引','additional-keywords.json')+'。',
'',
'会话诊断检索 `live descendants`、`could not verify`、`cleanup deadline`、`drain deadline`、`session deadline`、`member read errors`、`scan incomplete`、`SESSION_TRANSIENT_ERRORS_RECOVERED`、`COMMAND_ERROR`：两个新日志均0处。BOLT_CANCELLED/NATIVE_ARCHIVES_CANCELLED亦无新增或实际命中。',
'',
link('Dev新旧行号索引','1232862-log-index.json.gz')+'；'+link('Toolchain新旧行号索引','1232863-log-index.json.gz')+'。两份详细分析JSON gzip均超过10MB，只留本地；路径、大小、SHA见'+link('本地文件清单','local-only-files.json')+'。完整原始日志和紧凑索引已发布。','',
'## 4. 源码包逐项核对','',
'每个源码包11个文件，无增删，3个文件内容不同，其他8个文件（上游tar、单评审0002补丁、转换器、manifest、profile、三个模型tar）完整SHA相同；权限/uid/gid/链接无差异。'+link('逐项核对','source-audit.json')+'。','',
'|文件|事实|处理|','|---|---|---|',
'|clang-bolt-helper.py|旧/新分别与H2/H4 Git blob逐字节相同|归类为helper修改|',
'|llvm.spec|仅VCS提交号 H2→H4，其他字节相同|按79号VCS身份元数据单列|',
'|1334c36-to-61ef5d3.diff|仅第2行Date不同，代码正文逐字节相同|范围外日期差异保留，不作通过/失败结论|','',
'H2→H4的Git name-status仅 `packaging/clang-bolt-helper.py`。'+link('完整Git diff','H2-to-H4-helper.diff')+'；'+link('文件范围','source-git-name-status.txt')+'。','',
'两个项目共同的范围外差异原文：','',
'```diff',
'-Date: Mon, 16 Nov 2026 19:21:59 +0000',
'+Date: Tue, 17 Nov 2026 17:16:07 +0000',
'```','',
'从第一个 `diff --git` 至文件末尾，两侧SHA均为 `9c5cadf23fea2fdfce3ea421dc31420c4937942777428b030a4574a334479c82`。这是内容核对事实，不作为放宽本任务范围的依据。未把源码包整体标为PASS，也不据此推断二进制有问题。']
for bid in ['1232862','1232863']:
 parts+=['',bid+'：'+ '；'.join(link(f['file']+' diff',f['diff']) for f in source[bid]['files'])+'。']
parts+=['','## 5. 已读、未读与交付','',
'已读：STATUS、79号比较/告警规则、118号QB证据与脚本、119号保留规则；两个新QB概览/父构建日志/公开manifest、六份llvm日志；新旧104对RPM及完整载荷清单；H2/H4 Git对象的helper和文件范围；两侧源码包的3个差异文件。','',
'未运行：构建、测试套件、插件载入、BOLT、转换器重放、内部BOLT工作日志核对、Gerrit查询或写入、sandbox查询或推送、夜间编排操作。未另行解包SHA已相同的上游tar/归档，也不推断本次H4结果覆盖H5的UTF-8修正。','',
'没有身份门禁STOP。源码Date差异按用户要求原文列出，不自行追加白名单。资料定位时只读查询 README.md 不存在；实际未依赖该文件，后续采用明确的79/118/119文档；无产品或证据内容修正。','',
'完整清单：'+link('文件SHA清单','evidence-files.jsonl')+'；'+link('本地大文件/忽略日志','local-only-files.json')+'。','',
'已结束 '+datetime.datetime.now().astimezone().isoformat()+' status=COMPLETE_SOURCE_DATE_UNCLASSIFIED','']
report=B/'docs/bolt/128_qb_1232862_1232863.md';assert not report.exists();report.write_text('\n'.join(parts))
p=B/'docs/bolt/STATUS.md'
with p.open('a') as f:f.write('\n\n## 2026-11-17：128号（H4 QB 核对完成；源码日期差异未作放行判定）\n\n1232862=Base-Dev，1232863=Toolchain，实际均为H4 7a7bc17467d4c5da9763e86e3c74a123b3ff0df2/tree472c872afe958f464112d22b6304cde006fcbf98，不是H5。六架构成功；与H2 1231418/1231417比较，102/102二进制载荷和1294个llvm-static-devel完整归档SHA相同。SESSION_KILL_MODE均pidfd（每项目26命中含10实际输出）；STARTUP flags为null，TERM/HUP default、INT ignored；REAL三阶段及POST均PASS。新告警/错误关键字0，会话清理错误0。源码helper对Git一致、spec仅VCS；1334c36-to-61ef5d3.diff仅头部Date变化，正文SHA相同，按任务要求单列且不自行判源码整体PASS。新RPM保留在keep-baselines/qb-1232862-1232863，>10MB分析只留本地并登记SHA；未操作夜间编排、Gerrit或sandbox。见[128号](128_qb_1232862_1232863.md)。\n')
(E/'README.md').write_text('# QB 1232862 / 1232863 evidence\n\nSee ../../../..'+ '/docs/bolt/128_qb_1232862_1232863.md for the report.\n\nH4 identity and all 102 binary package payloads verified. Source patch-header Date change remains listed without an acceptance verdict.\n\nRPMs are retained outside Git in /home/linhao/Toolchain/development/llvm-optimize/temp/keep-baselines/qb-1232862-1232863/. Large analysis files and ignored execution logs are recorded in local-only-files.json. Original gzip build logs and compact diagnostic line indexes are published.\n')
print('REPORT',report,report.stat().st_size,'bytes')
print('已结束',datetime.datetime.now().astimezone().isoformat(),'status=DOCUMENTED')
