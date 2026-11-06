from pathlib import Path
import collections,datetime,gzip,hashlib,json,shutil
E=Path(__file__).resolve().parent;B=E.parents[3];W=Path('/home/linhao/Toolchain/development/llvm-optimize')
assert B.name=='llvm-optimize-bolt',B
U=json.loads((E/'restored-inputs.json').read_text());R=json.loads((E/'dwarf-results.json').read_text());S=json.loads((E/'classification-summary.json').read_text());A=json.loads((E/'attribute-differences.json').read_text());T=json.loads((E/'dwarfdump-tool.json').read_text())
fence=chr(96)*3
evbase='../../tools/bolt/results/tu-dwarf-20261106/'
def ev(name,label=None):return '['+(label or name)+']('+evbase+name+')'
# Keep large uncompressed evidence locally; publish its additional gzip copy.
for p in list(E.iterdir()):
 if p.is_file() and p.suffix in ('.json','.txt','.stdout','.stderr') and p.stat().st_size>1048576:
  target=p.with_name(p.name+'.gz')
  if not target.exists():
   with p.open('rb') as src,gzip.open(target,'wb',compresslevel=6) as dst:shutil.copyfileobj(src,dst,1048576)
def published(n):
 p=E/n;return n+'.gz' if p.stat().st_size>1048576 and (E/(n+'.gz')).exists() else n
q=['# 67. 90 TU 输入恢复与 Toolchain 调试信息逐项比较','',
'90 份输入全部从保留副本恢复，SHA256 与 53 号清单逐项一致；没有重新预处理，也没有重跑 90 TU。'
'132 对调试文件全部检查完成，按本次指定的文本替换规则为 **0 PASS、132 DIFFERENT、0 UNKNOWN**。'
'差异已归因于行表编码长度，以及 8 个文件的 19 处编译目录重复斜杠；其他要求严格比较的节全部逐字节相同。','',
'## 1. 范围、执行条件与证据','',
'- 日期：2026-11-06，Asia/Shanghai。第一项改接因上游前提不成立停止，见 [68 号](68_rebase_on_tizen_base.md)；第二、三项继续串行完成。',
'- 全部本机命令放入独立 systemd 用户服务，服务之间不并行：MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、Nice=19、IOSchedulingClass=idle（ionice -c3）。没有演练或构建，没有 sudo。',
'- '+ev('service-policy.json')+' 实读 memory.max=8589934592、memory.swap.max=0、cpu.max=400000 100000、nice=19。DWARF 服务末次 memory.events 的 oom=0、oom_kill=0、oom_group_kill=0；max=7081 是触及限额/回收事件，不是 OOM。',
'- 历史构建根和原产物只读，没有删除文件；LLVM 源码、spec、helper 未修改。仅两个现用本地验证入口更新输入清单路径。',
'- DWARF 服务正常退出，运行 2h 24min 29.124s。每侧输入的三种导出合计限时 30 分钟；最大实际导出耗时 %.3f 秒，最大整对检查耗时 %.3f 秒，均未超过 30 分钟。'%(S['max_input_dump_seconds'],S['max_pair_seconds']),
'- 完整原始/归一化导出和 stderr 保留在 W/temp/dwarf-check-20261106/，合计 %s B；逐文件路径、大小与 SHA 见 %s。完整差异前后各 5 行原文已复制到本仓库 contexts/，合计 %s B。'%(S['raw_dump_bytes'],ev(published('raw-dump-manifest.json')),S['context_bytes']),
'- '+ev('dwarf-service-end.txt')+' 保留 systemd-run 原样结束输出。其中退出后显示的 Memory peak=508.0K 不用作整个工作负载的内存峰值结论；本任务只据限额配置与 memory.events 判断限制和 OOM。',
'','## 2. 输入恢复','',
'原清单：W/docs/53_hybrid_local_validation_evidence/tu-inputs.json。'+ev('original-tu-inputs.json')+' 保留原始内容；'+ev('restored-inputs.json')+' 保留每项原路径、原 argv、provenance.asset_preprocessing_argv、找到的副本路径及恢复路径。','',
'| 项目 | 结果 |','|---|---:|','| 原清单条目 | 90 |','| 找到并复制同 SHA 副本 | 90 |','| 重新生成 | 0 |','| 未恢复 | 0 |','| 唯一内容 SHA | 60 |','| 复制的实际文件字节数 | 677,747,108 |','| armv7l / aarch64 / x86_64 | 各 30 |','',
'新目录为 W/temp/tu-inputs-restored-20261106/，包含 000.ii–089.ii、tu-inputs.json 和 SHA256SUMS。全部命中来源为 W/temp/debuglink-20261028/full-20261030/validation-work/objects-current/<编号>/input.ii；原副本未修改。','',
'搜索设整体 900 秒、单文件 SHA 45 秒限时；实际 264.265 秒，检查 148,380 个目录和 1,372,984 个文件元数据。存在 9 个 Permission denied 盲区，原文见 '+ev('restore-search.json')+'；所需 90 项均已找到并逐项 SHA 复核，盲区不影响恢复结果。没有使用宿主工具链重新生成任何输入。','',
'以下编号同时对应新目录 <编号>.ii 与来源 objects-current/<编号>/input.ii。完整源文件路径和预处理命令见 restored-inputs.json，表中列源文件名便于检索。','',
'| 编号 | 目标 | 原始源文件 | 字节数 | SHA256 |','|---|---|---|---:|---|']
for u in U:
 argv=u['provenance'].get('asset_preprocessing_argv',[]);src=[x for x in argv if x.endswith(('.cpp','.c','.cc','.cxx'))];source=Path(src[-1]).name if src else '(见 provenance)'
 q.append('| %03d | %s | %s | %d | %s |'%(u['index'],u['target'],source,u['bytes'],u['sha256']))
q+=['','## 3. 本地验证入口与测试','',
'只改两个现用入口的一个路径行：','',
'- tools/bolt/night-launch-20261105/validation_common.py:65',
'- tools/bolt/night-launch-20261103/validate.py:65','',
'两者从旧 docs/53_hybrid_local_validation_evidence/tu-inputs.json 改读 temp/tu-inputs-restored-20261106/tu-inputs.json。原来的逐输入 SHA 检查保留，完整 diff 和前后脚本 SHA 见 '+ev('script-changes.diff')+'、'+ev('script-changes.json')+'。','',
'tools/ 下引用检索见 '+ev('tu-script-references.json')+'。results/ 下的历史验证脚本、测量脚本与报告生成器是历史证据，保留原文和原 SHA；不把它们作为现用入口，也不原地运行。今后重放历史脚本时应先复制并改接新清单。其余现用入口未发现旧清单引用。','',
'测试直接提取现用 objects() 的清单读取语句和 SHA 断言：验证 90 项元数据与原清单一致、全部输入 SHA、有效副本可通过、改坏字节必被拒绝、两个现用入口没有旧清单路径。','',fence+'text',(E/'tests.stderr').read_text().rstrip(),fence,'',
'没有重跑 63 号的 90 TU，也没有把 SHA 恢复检查说成编译正确性重测。','',
'## 4. DWARF 检查方法','',
'配对表来自 63 号保留的 validation/qb-changed-file-paths.json，筛出全部 132 对 .debug；本地来自 W/temp/night-20261105/toolchain，QB 来自 1216409 的已解包完整 RPM。每个文件导出前均核对配对表中记录的 SHA。配对完整路径、包名和两边 SHA 见 '+ev('dwarf-pairs.json')+'。','',
'平台工具版本为 LLVM 22.1.8，不使用宿主 llvm-dwarfdump。'+ev('dwarfdump-tool.json')+' 记录路径、版本与 SHA：','',
'- llvm-dwarfdump：'+T['tool_sha256'],
'- loader：'+T['loader_sha256'],'',
'实际 argv 模式如下（所有 792 次导出的完整 argv、rc、耗时、行数和摘要见 '+ev(published('dwarf-results.json'))+'）：','',
fence+'text',T['loader']+' --library-path '+T['library_path']+' '+T['tool']+' --debug-info <file>',
'同样分别执行 --debug-line 和 --debug-aranges。',fence,'',
'132 对均没有 .debug_str_offsets，故 str-offsets 导出不适用。全部导出 rc=0，stderr 均为空。文本逐行处理；每个差异区间完整保留前后各 5 行，长区间流式写入 gzip，摘要只保留有限样例。','',
'归一化限定为：源码路径前缀 usr/src/debug/llvm-22.1.8-1.x86_64 → usr/src/debug/llvm-22.1.8-2.1.x86_64；输出文件名标题；DIE 行首偏移、debug_line[...] 位置、next unit at、abbr_offset/cu_offset/debug_info_offset/str_offsets_base、DW_AT_stmt_list 与显式字符串位置字段。不会删除实际 PC、地址范围、DW_OP 值、行列值、类型引用值或长度字段，也不折叠重复斜杠。实现为 '+ev('dwarf_check.py')+'。','',
fence+'text',(E/'dwarf-normalization-tests.txt').read_text().rstrip(),fence,'',
'## 5. 总体结果与差异分类','',
'| 检查 | 完全相同 | 有差异 | UNKNOWN |','|---|---:|---:|---:|',
'| 整个文件的指定归一化文本 | 0 | 132 | 0 |',
'| --debug-info | 124 | 8（19 行） | 0 |',
'| --debug-line | 0 | 132（176,482 行） | 0 |',
'| --debug-aranges | 132 | 0 | 0 |',
'| 节数量、名称及顺序 | 132 | 0 | 0 |',
'| 除 .debug_info/.debug_line/.debug_str/.debug_aranges 外的节内容 | 132 | 0 | 0 |','',
'### 5.1 行表编码长度','',
'176,482 处差异全部为 total_length 或 prologue_length。没有把长度值作为偏移列删除，因此这些文件严格文本结论保持 DIFFERENT。例如 libRemarks.so.22.1.debug：','',fence+'text',
'old: total_length: 0x0000015a    new: total_length: 0x0000015c',
'old: prologue_length: 0x0000013e new: prologue_length: 0x00000140',fence,'',
'进一步按真实 .debug_line 二进制逐单元核对，共 88,987 个单元、132 对全部通过以下辅助归因检查：格式/版本前缀相同；目录和文件表头仅替换获批源码前缀后逐字节相同；行号程序本身逐字节相同；total_length 和 prologue_length 的增加值都精确等于路径替换次数 × 2 字节。完整单元旧值、新值、偏移与逐项断言见 '+ev('line-unit-proof.jsonl.gz')+'，逐文件汇总见 '+ev('line-unit-proof-summary.json')+'，实现见 '+ev('classify_dwarf.py')+'。','',
'这证明行表长度差异来自版本路径从 -1 增长为 -2.1，并非地址或行号程序变化。辅助归因 PASS 不替换上面的严格文本 DIFFERENT。','',
'### 5.2 8 个文件、19 处 DW_AT_comp_dir','',
'| 文件 | 差异行数 |','|---|---:|']
for i in sorted({a['index'] for a in A}):q.append('| '+R[i]['path']+' | '+str(sum(a['index']==i for a in A))+' |')
q+=['','源码前缀替换后，剩余差异是内部重复斜杠数量；所有 19 处按 POSIX 路径词法归一化都指向同一目录。但用户本轮只授权前缀替换和位置偏移处理，所以这里不额外折叠斜杠，不把这些属性行改判为文本相同。全部 19 行原文、行号和词法核对见 '+ev('attribute-differences.json')+'。不同原文组合及出现次数如下：','']
for (a,b),count in collections.Counter((x['old_raw'].strip(),x['new_raw'].strip()) for x in A).items():q +=[fence+'text','occurrences='+str(count),'old: '+a,'new: '+b,fence,'']
q+=['未发现除此之外的属性、类型引用、实际 PC、地址范围或行号文本差异；UNKNOWN=0。分类计数原文见 '+ev('classification-summary.json')+'。','',
'## 6. 132 对逐文件清单','',
'路径均相对 /usr/lib/debug/；info 一列标出差异行数，line 一列为长度字段差异行数。每行链接为包含差异及前后各 5 行的完整原文；aranges 与其他节检查均 PASS，strict 均 DIFFERENT。','',
'| 编号 | 文件 | info | line | 原文上下文 |','|---:|---|---|---:|---|']
for r in R:
 n=r['index'];info=r['sections']['debug_info'];line=r['sections']['debug_line'];links=[ev(f'contexts/{n:03d}-debug_line.txt.gz','line')]
 if not info['equal']:links.append(ev(f'contexts/{n:03d}-debug_info.txt.gz','info'))
 q.append('| %d | %s | %s | %d | %s |'%(n,r['path'].removeprefix('usr/lib/debug/'),'PASS' if info['equal'] else 'DIFFERENT '+str(info['different_lines']),line['different_lines'],' / '.join(links)))
q+=['','## 7. 结束记录与结论','',fence+'text',(E/'item2-end.txt').read_text().rstrip(),(E/'item3-end.txt').read_text().rstrip(),fence,'',
'第三项的 status=partial 表示严格文本未达到全部 PASS；132/132 已完整检查，不是漏跑。单文件没有超时、MemoryError 或 OOM。全部成果与历史产物保留。','',
'结论：90 TU 输入恢复完成，现用入口已改接并通过 4 项测试；132 对调试文件的差异已逐项定位，行号程序及要求保持一致的其他节全部相同，但按指定的严格文本规则仍保留 132 个 DIFFERENT。']
doc=B/'docs/bolt/67_tu_inputs_and_dwarf_check.md';assert not doc.exists();doc.write_text('\n'.join(q)+'\n')
status=B/'docs/bolt/STATUS.md'
with status.open('a') as f:f.write('\n## 2026-11-06：90 TU 恢复与 DWARF 逐项核对（67 号）\n\n- 90/90 输入从 full-20261030 保留副本恢复至 temp/tu-inputs-restored-20261106，全部 SHA 匹配；0 重新生成，两个现用验证入口改接，4 项测试 PASS；未重跑 90 TU。\n- 132/132 调试文件检查完成：严格文本 0 PASS、132 DIFFERENT、0 UNKNOWN；全部其他节及节数量/名称/顺序相同。差异为 176,482 个行表编码长度字段，以及 8 个文件的 19 处 DW_AT_comp_dir 重复斜杠。88,987 个行表单元证明路径增长精确解释长度变化，行号程序字节相同；未擅自扩展归一化规则。\n- 无 OOM/超时；历史根只读。改接停止的原因及未执行的检查/演练仍见 68 号，未创建新的 LLVM 分支或提交，未推送 Gerrit。\n- 证据与逐文件清单：[67_tu_inputs_and_dwarf_check.md](67_tu_inputs_and_dwarf_check.md)。\n')
# Publish only generated evidence, excluding Python caches and uncompressed >1MiB copies.
files=[p for p in sorted(E.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name not in ('SHA256SUMS','publication-files.json') and not(p.stat().st_size>1048576 and p.suffix in ('.json','.txt','.stdout','.stderr') and p.with_name(p.name+'.gz').exists())]
(E/'publication-files.json').write_text(json.dumps([str(p.relative_to(B)) for p in files],indent=2)+'\n');files.append(E/'publication-files.json')
(E/'SHA256SUMS').write_text(''.join(hashlib.file_digest(p.open('rb'),'sha256').hexdigest()+'  '+str(p.relative_to(E))+'\n' for p in files))
print('DOC',doc,'bytes',doc.stat().st_size,'EVIDENCE_FILES',len(files),'bytes',sum(p.stat().st_size for p in files))
print('REPORT 已结束',datetime.datetime.now().astimezone().isoformat(),'status=ok reason=all-results-recorded;strict-text-differences-retained')
