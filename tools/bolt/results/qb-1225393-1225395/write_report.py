from pathlib import Path
import json,gzip,re,datetime,hashlib
E=Path(__file__).resolve().parent;B=E.parents[3]
load=lambda p:json.loads((E/p).read_text())
rows=load('package-results.json');arm=load('arm-baseline-results.json');source=load('source-audit.json');arch=load('arch-status.json');summary=load('analysis-summary.json')
assert len(rows)==104 and sum(r['status']=='PASS' for r in rows)==102
assert len(arm)==68 and all(r['status']=='PASS' for r in arm)
assert len(source)==2 and all(r['status']=='PASS' for r in source)
assert sum(len(r['changes']) for r in arm)==8
# Preserve originals; publish compressed copies of oversized JSON.
for name in ['package-results.json','arm-baseline-results.json']:
 data=(E/name).read_bytes()
 with gzip.open(E/(name+'.gz'),'wb') as f:f.write(data)
prefix='../../tools/bolt/results/qb-1225393-1225395/'
def link(name,label=None):return '['+(label or name)+']('+prefix+name+')'
lines=[]
def add(s=''):lines.append(s)
def block(text):add('\n~~~text\n'+text.rstrip()+'\n~~~\n')
add('# 77. QB 1225393 / 1225395：r5 与前版及 ARM PS7 基线核对')
add('\n第一项 PASS：1225393 是 Toolchain，1225395 是 Base-Dev，源码均为 60fabc723f30c5cc04146a9dd83487ebed63f259，输入快照符合要求，六个架构构建成功。第二项 PASS：对 fa4f9978 的 102 个二进制包载荷完全相同，其中 x86_64 为 34/34；两份源码包仅有授权差异。第三项 PASS：对 PS7 的 68 个 ARM 包，60 包完全相同，8 包仅含精确匹配混合链接提交的 AddLLVM/AddClang 文本变化。')
add('\n## 1. 范围、身份与执行条件')
add('\n只读访问 QB 与公开 RBS/snapshot 下载；未启动构建、未操作 QB、未推 Gerrit/sandbox、未删除文件、未改源码或 VS Code。开始时 '+link('running-services.txt','服务清单')+' 未见其他 Codex 任务服务。所有命令串行运行于独立 systemd 用户服务，MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、Nice=19、IOSchedulingClass=idle；未发生 OOM。浏览器采用有界面临时会话，未导出认证材料。')
add('\n|QB|项目|源码|输入快照|Release|子构建|\n|---|---|---|---|---|---|')
for bid,project,snap,release,child in [('1225393','Tizen-Base-Toolchain','tizen-base-toolchain_20261030.061318','2.1','1225398'),('1225395','Tizen-Base-Dev','tizen-base-dev_20261030.061217','5.1','1225399')]:
 add(f'|[{bid}](https://quickbuild.tizen.org/build/{bid})|{project}|60fabc723f30c5cc04146a9dd83487ebed63f259|{snap}|{release}|[{child}](https://quickbuild.tizen.org/build/{child}) SUCCESSFUL|')
 add('\n'+link(bid+'/overview.txt',bid+' 概览原文')+'；'+link(bid+'/full-log.txt','父日志')+'。')
 text=(E/bid/'overview.txt').read_text()
 block('\n'.join(s for s in text.splitlines() if s.startswith(('Build Package List','Profile URL','Base URL','Download_URL'))))
add('源码身份由概览软件包行、公开 manifest 和全部下载 RPM 的 VCS 三方核对。Release 从实际 RPM 查询取得，不写死归一化前缀。两代 QB 的 Release 相同（Toolchain 2.1，Base-Dev 5.1），本轮无需使用 release 前缀替换来放宽比较。')
add('\n|QB|架构|结果|包日志时间与耗时（UTC）|原文|\n|---|---|---|---|---|')
for a in arch:
 sec=int(re.search(r'\[\s*(\d+)s\]',a['end'][0]['raw'])[1])
 add(f"|{a['build']}|{a['arch']}|SUCCESS / LLVM 成功|{sec}s ({sec//3600}h {(sec%3600)//60}m {sec%60}s)|"+link(a['build']+'/'+a['arch']+'/llvm.buildlog.txt.gz',f"L{a['start'][0]['line']} / L{a['end'][0]['line']}")+'|')
 block(a['start'][0]['raw']+'\n'+a['end'][0]['raw'])
add('x86_64 包构建时长分别为 **9200 秒（2h33m20s）** 与 **5862 秒（1h37m42s）**。概览父流程时长分别为 5h6m38s、4h35m10s，二者不是同一口径。概览未注明时区；上表使用包日志明确打印的 UTC。')
add('\n输入 build.conf 重新从固定快照下载后测得 SHA256；QB 日志不打印 worker 文件的 SHA，不能称为直接核验 worker SHA：')
for bid,v in summary.items():add('\n- '+bid+': '+v['buildconf']['sha256']+'，'+str(v['buildconf']['bytes'])+' B；[来源]('+v['buildconf']['url']+')。')
add('\n完整身份、行数、原始日志 SHA：'+link('arch-status.json')+'。')
add('\n## 2. x86_64 日志逐项核对')
add('\n按 [73 号](73_qb_1223601_1223602.md) 方法，只去掉 [NNNNs] 时间前缀比较 FLAGS；profile 比较 N/M/S/U/Q/R 数值。其余门禁验证实际 PASS 行及顺序，不要求资源计数、耗时和任务输出顺序相同。')
for bid in ['1225393','1225395']:
 v=summary[bid];extra=load(bid+'/tools-cancel-notfound.json');comparison=load(bid+'/anchor-comparison.json')
 assert not extra['prohibited'] and not any(x['shell_error'] for x in extra['not_found'])
 add('\n### 2.'+('1' if bid=='1225393' else '2')+' '+bid+' 对 '+v['old_build'])
 add('\nFLAGS 逐字一致；FLAGS_WARNING 两边均为 0。NATIVE_ARCHIVES_END PASS 225，converted 合计 3853、preserved 合计 11。'+link(bid+'/anchor-comparison.json','逐条新旧原文与行号')+'；'+link(bid+'/native-records.json','225 条转换记录')+'。')
 for group in comparison:
  if group['group'] in ('flags','warnings'):
   assert group['exact_after_timestamp_removal']
   for label in ['old','new']:
    if group[label]:block(label+'\n'+'\n'.join('L'+str(x['line'])+': '+x['raw'] for x in group[label]))
 c=v['counts'][0];add('\nprofile 与旧 QB 相同：'+', '.join(k+'='+str(c[k]) for k in ['N','M','S','U','Q','R'])+'。')
 selected=[];profile_raw=[]
 with gzip.open(E/bid/'x86_64/llvm.buildlog.txt.gz','rt') as f:
  for i,line in enumerate(f,1):
   text=re.sub(r'^\[\s*\d+s\]\s*','',line).rstrip()
   if (re.match(r'^(?:TIZEN_HYBRID_LINK_OK|BOLT_[A-Z_]*PASS|BOLT_PROC_OK|NATIVE_ARCHIVES_TOOLS|NATIVE_ARCHIVES_END)\b',text) or text=='BOLT_NINJA_EXIT_0' or text.startswith('BOLT_DISK_REPORT ') and '"post"' in text):
    selected.append('L'+str(i)+': '+line.rstrip())
   if '"counts"' in text and '"N"' in text and '"R"' in text:profile_raw.append('L'+str(i)+': '+line.rstrip())
 (E/bid/'required-log-excerpts.txt').write_text('\n'.join(selected+profile_raw)+'\n')
 add('\n门禁、工具版本及 post 原文：');block('\n'.join(selected))
 if profile_raw:
  add('profile 原始 JSON 行（完整保留）：');block('\n'.join(profile_raw))
 else:add('profile 原始记录见 '+link(bid+'/profile-counts.json')+' 和 '+link(bid+'/anchors.txt')+'。')
 post=[i for i,t in enumerate(selected) if 'BOLT_POST_GATE_PASS' in t];disk=[i for i,t in enumerate(selected) if 'BOLT_DISK_REPORT ' in t and '"post"' in t]
 assert post and disk and max(disk)>max(post)
 add('NATIVE_ARCHIVES_TOOLS 明确记录 compiler/disassembler/nm 均为 22.1.8，tool_directory 为 /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin，与转换命令的编译器目录一致。BOLT_POST_GATE_PASS 后存在 post 阶段 BOLT_DISK_REPORT。')
 add('\nNATIVE_ARCHIVES_CANCELLED=0，NATIVE_ARCHIVES_SIGCHLD_RESET=0，shell “not found” 错误=0。日志有 '+str(len(extra['not_found']))+' 条非 shell 的 not found（CMake 功能/头文件探测、Git 版本探测）；全部原文逐条保留于 '+link(bid+'/tools-cancel-notfound.json')+'，未将正常探测误计为 shell 错误。')
add('\n## 3. 对 fa4f9978 的逐包载荷比较')
add('\n比较流式读取 rpm2cpio：文件集合、逐文件完整内容 SHA256、字节数、mode、uid/gid、符号链接目标全部核对；解析 cpio 硬链接的实际内容。仅 payload mtime 单列，不计内容差异。RPM 头的 VCS/构建时间/签名与压缩层不作为载荷。**102/102 个二进制包载荷相同，未使用 ELF 节例外、ar 日期例外或 release 前缀归一化消除差异。**')
add('\n'+link('package-results.json.gz','逐文件/逐归档结果及 mtime 差异')+'；downloads/ 保存每份 RPM 的 URL、大小、SHA 和查询原文，manifests/ 保存完整载荷清单。新包及旧 ARM 包在 W/temp/qb-1225393-1225395/；旧 x86_64 包从既有目录复用并核对历史 SHA。')
add('\n|新 QB|旧 QB|架构|RPM|结果|载荷条目|mtime 差异数|\n|---|---|---|---|---|---:|---:|')
for q in rows:
 if q['status']!='PASS':continue
 add(f"|{q['build']}|{q['baseline']}|{q['arch']}|{q['name']}|PASS|{q['file_count']}|{len(q['payload_mtime_differences'])}|")
add('\n### 完整静态归档')
for q in rows:
 if q['arch']=='x86_64' and q['name'].startswith('llvm-static-devel-'):
  assert len(q['archives'])==225 and all(a['equal'] for a in q['archives'])
  add(f"\n- {q['build']} 对 {q['baseline']}：225/225 个完整归档 SHA 相同。")
add('\n7706 个转换成员由两组完整归档相同覆盖，**未另外逐成员计算 SHA**；不写成“7706/7706 已逐成员核对”。')
add('\n## 4. 两份源码包与 0008 说明归因')
add('\n两份源码包均 PASS（允许差异）。17 个载荷文件没有增删，差异精确为 llvm.spec、llvm-static-archives-native.py、0008-cmake-use-hybrid-LLVM-linkage-on-x86_64.patch。helper、profile、源码压缩包等其他文件内容相同。spec diff 包含 VCS 更新；转换器内容与两侧 Git 对象完全相同。')
add('\n'+link('source-audit.json')+'；')
for bid in ['1225393','1225395']:
 add('\n- '+bid+'：'+', '.join(link(bid+'-'+f+'.diff',f+' 完整 diff') for f in ['llvm.spec','llvm-static-archives-native.py','0008-cmake-use-hybrid-LLVM-linkage-on-x86_64.patch'])) 
add('\n0008 从第一个 diff --git 到文件结尾逐字节相同，SHA256 均为 e99fa7abdc0a828c9eb9295c163a239ed7438c0df378446bf10e07ae3a89b6c6。包内 Subject 标题与正文精确匹配各自 Git 提交说明。说明仅有 [75 号](75_fourth_review_fixes.md) 记录的两处修改：删除过时 QB pending 句；增加 ARM 安装 AddLLVM/AddClang 而行为不变的说明。')
block((E/'hybrid-message.diff').read_text())
add('\n## 5. PS7→PS10 与 ARM 是否相关')
add('\n'+link('ps7-to-ps10.stat')+'；'+link('ps7-to-ps10.diff','完整源码 diff')+'；'+link('ps10-converter-spec-context.txt','Source1005 的 spec 上下文与行号')+'。')
block((E/'ps7-to-ps10.stat').read_text())
add('\n唯一文件 packaging/llvm-static-archives-native.py：限制 --param 的分离/等号形式；任何 -g 要求最后 DWARF 为 -gdwarf-4；release 转换结果含调试节时报错。spec 本身未变。该脚本调用位于 PS10 spec L429–441 的 %ifarch x86_64 块，L433 调用 Source1005、L436 明确 --arch x86_64。ARM 不执行它，因此这些源码变化不影响 armv7l/aarch64 的构建；本次没有用它解释任何 ARM 载荷差异。')
add('\n基线采用 [76 号](76_sandbox_push_r5.md) 已核实的同快照：Toolchain QB1216401，Base-Dev QB1216400；均为 PS7/463c9a133a6dfea9adf1e6c8e07ab705cbf2a587，**不是 PS10**。本轮重新下载公开 manifest、两架构成功日志及全部 ARM 二进制 RPM，manifest 和 RPM VCS 均确认 PS7。')
add('\n'+link('arm-baseline-identities.json','基线 manifest 身份/URL/SHA')+'；输入快照仍分别为 tizen-base-toolchain_20261030.061318、tizen-base-dev_20261030.061217，与新 QB 相同。')
add('\n## 6. ARM 对 PS7：逐包结果及差异归因')
add('\n**68/68 包 PASS**：60 包载荷完全相同；8 包只含下表标记的 CMake 文本变化，无其他程序、库、静态归档、调试信息或源码调试载荷差异。'+link('arm-baseline-results.json.gz','完整逐文件结果')+'。')
add('\n|新 QB|PS7 基线|架构|RPM|结果与差异|\n|---|---|---|---|---|')
for q in arm:
 detail='PASS，全部载荷相同' if not q['changes'] else 'PASS，已知例外：'+','.join(Path(c['file']).name for c in q['changes'])
 add(f"|{q['build']}|{q['baseline']}|{q['arch']}|{q['name']}|{detail}|")
add('\n### 八处文本变化的证据链')
add('\n|QB/架构|文件|归因|证据|\n|---|---|---|---|')
for q in arm:
 for c in q['changes']:
  add(f"|{q['build']}/{q['arch']}|{c['file']}|混合链接提交，精确完整文本匹配|"+link(c['proof_diff'],'完整 diff')+'|')
add('\n首组实测：旧模块字节 = PS7 = PS10 = 混合链接提交父版本；新模块字节 = 混合链接提交 8a50d712 = 60fabc72。后续组逐字节匹配这些已核实的两侧文件，且解出文件 SHA 必须等于对应 RPM 载荷 SHA。不是按文件名直接豁免，不跳过任何剩余字节。AddLLD 不在允许例外中，本次没有该文件差异。')
add('\n## 7. 执行问题、证据与未运行检查')
add('\n1. 辅助源码审计初次把 GBS 不带 [PATCH] 的邮件 Subject 和临时 format-patch 带 [PATCH] 的邮件 Subject 相比，产生工具断言失败；它不是两份 RPM 之间的差异。原脚本保留，改为直接比较包内标题/正文与 Git %B，精确两处说明修改核验通过。'+link('source-audit-instrumentation-note.txt')+'。')
add('\n2. 首次 ARM 服务在 Toolchain armv7l 的重复 git show 源码查询超过 30 秒时停止，已完成 22 个 aarch64 包保留。'+link('arm-baseline-failure.txt','超时原文')+'。未 OOM，未重试该 Git 查询；续跑用首组已经和五个 Git 对象核实的相同文件字节作传递证明。已完成包未重跑。'+link('arm-resume-note.txt')+'。')
add('\n3. 本任务要求的三项核对最终均完成；未运行任何构建、TU/安装/LLDB 测试、Gerrit 查询或写操作。未另行逐成员重算 7706 个 SHA（整归档相同已覆盖）。未验证 worker 内 build.conf 的直接 SHA（日志不可见，只测固定快照文件）。未使用逐节放宽规则，因为本轮二进制载荷及归档已经全字节相同。')
add('\n原文日志 gzip、概览、下载清单、逐包清单和执行脚本都位于 '+prefix+'。本机 RPM 和解包证据保留于 W/temp/qb-1225393-1225395/，没有删除。')
add('\n## 8. 结束行')
block('ITEM1 已结束 2026-11-11T09:57:49.099952+08:00 status=ok reason=identities_snapshots_and_three_arch_builds_verified\n'+(E/'item2-ending.txt').read_text()+(E/'item3-ending.txt').read_text()+(E/'item3-resume-ending.txt').read_text())
out=B/'docs/bolt/77_qb_1225393_1225395.md';assert not out.exists();out.write_text('\n'.join(lines)+'\n')
entry='\n\n## 2026-11-11：r5 的 QB 验证及 ARM PS7 基线比较完成（77 号）\n\n[77 号](77_qb_1225393_1225395.md)：1225393=Toolchain、1225395=Base-Dev，源码均为60fabc723f30c5cc04146a9dd83487ebed63f259，固定输入快照与1223601/1223602一致，三架构均成功。对fa4f9978：x86_64 34/34、ARM 68/68二进制包载荷全同；两组各225完整归档SHA全同；源码包仅spec/转换器/VCS和授权0008说明变化，PASS。FLAGS/profile同旧QB，WARNING及shell not found、取消/SIGCHLD_RESET均0，NATIVE_ARCHIVES_TOOLS明确三个工具22.1.8且同目录。\n\nARM对PS7基线1216401/1216400：68/68包PASS，60包全同，8包只含AddLLVM/AddClang精确混合链接文本变化；PS7→PS10仅x86转换器变动，不影响ARM。记录过一次辅助邮件标题断言问题及重复Git读取超时；原文保留，最终均以精确字节证据闭合，未OOM。7706成员由整体归档相同覆盖，未另行逐成员算SHA。未构建、未操作QB、未推Gerrit/sandbox；74号启动前停止仍未解决。后续仍需74号本地完整构建及三家完整评审（设计v6.1+r5）。\n'
status=B/'docs/bolt/STATUS.md';status.write_text(status.read_text()+entry)
root=B/'STATUS.md'
print('ROOT STATUS HEAD',root.read_text()[:1300])
print('DOCUMENT',out,'bytes',out.stat().st_size)
print('NOT_FOUND',[(bid,len(load(bid+'/tools-cancel-notfound.json')['not_found'])) for bid in summary])
print('END',datetime.datetime.now().astimezone().isoformat())
