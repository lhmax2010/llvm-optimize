from pathlib import Path
import json,gzip,datetime,collections,subprocess,os
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');E=Path(__file__).resolve().parent;C=E/'completed';V=C/'validation';R=C/'evidence'
def read(p):
 if p.exists():return json.loads(p.read_text())
 with gzip.open(str(p)+".gz","rt") as f:return json.load(f)
def ev(n,label=None):
 if not (E/n).exists():
  if (E/(n+'.gz')).exists():n+='.gz'
  elif n.endswith('.gz') and (E/n[:-3]).exists():n=n[:-3]
 return '['+(label or n)+'](../../tools/bolt/results/qb-snapshot-rebuild-20261105/'+n+')'
r=read(V/'qb-rpm-comparison.json');details=read(E/'difference-details.json');build=read(R/'build-result.json');result=read(R/'result.json');val=read(V/'result.json');log=read(V/'log-input.json');ident=read(V/'identity.json');resource=read(R/'resource-table.json');counts=read(V/'pipeline.json')['counts'];syms=read(E/'symbols-qb-check.json');audit=read(R/'final-audit.json');space=read(E/'completion-space.json')
def stamp(ns):return datetime.datetime.fromtimestamp(ns/1e9).astimezone().isoformat()
text=['# 63：QB 同快照 Toolchain 重建（2026-11-05）','',
'**结论：完整构建成功，自动验证未全部通过。** 最终 clang、匹配的符号文件、三级 SHA、FLAGS 和 profile 计数与 QB 1216409 相同。23 包按既定规则为 3 PASS / 20 FAIL；90 TU 因旧输入路径已不存在，在第一个输入处停止，未完成任何一对编译比较。没有重试、修入口、放宽规则或手动续跑。','',
'清理另见 [66号](66_disk_cleanup.md)，提交 `b40cd743c16bf4e1db9320cb0125de89f47de7e0`。本次原始证据在 `tools/bolt/results/qb-snapshot-rebuild-20261105/`；构建根及产物原样保留。','',
'## 1. 唯一启动与结束记录','',
'启动前检查已满足：/home 可用 559,488,331,776 B（521.064 GiB）≥98.8 GiB；新根不存在；没有其他 GBS/rpmbuild。'+ev('../disk-cleanup-20261105c/launch-precheck.json','启动前记录'),'','原样执行一次：','```sh',
'/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/night-launch-20261105/launch.sh 9e39fa8a61392652bb28b75fc26216675bcad1d5 full','```','',
'前台最后的查看命令：','```sh','tail -f /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain/controller.stdout','```','',
'最终结束行原文：','```text',(C/'controller.stdout').read_text().strip(),(R/'validation.stdout').read_text().splitlines()[-1],(V/'item2-end.txt').read_text().strip(),'```','',
'GBS `exit_code=0`；构建服务从 '+stamp(build['start_ns'])+' 到 '+stamp(build['end_ns'])+'，耗时 '+str(build['seconds'])+' 秒。完整入口（含准备和自动验证）耗时 '+str(round((result['end_ns']-result['start_ns'])/1e9,3))+' 秒。controller 退出码为 1，原因是验证返回 1，不能写成构建失败或全部通过。'+ev('completed/evidence/build-result.json')+'、'+ev('completed/evidence/result.json')+'、'+ev('completed/controller.stderr'),'','验证器既有逻辑在包比较失败后继续尝试90 TU；这是入口自动行为，本轮没有手动追加执行。','',
'## 2. 源码、快照与条件','',
'- 源码：`9e39fa8a61392652bb28b75fc26216675bcad1d5`；tree `cbc33271f8a9a7a5bd4de3c806bed6182c268e98`；最终只读审计工作区干净。',
'- 快照：`tizen-base-toolchain_20261030.061318`，与 QB 1216409 相同；只启用固定快照 packages/debug。',
'- build.conf SHA256：`8f201a0d58eb634e60a1f213f47fc09dfa953d9869cdc5724f326a76203587bf`。',
'- 外层 threads30；三个宏为 jobs8、_smp_mflags -j8、_costomized_smp_mflags -j20；实际 Ninja -j6。MemoryMax 24,482,992,128 B（MemTotal减8GiB），MemorySwapMax=0，CPUQuota=1200%，nice10，ionice 2/7。',
'- 同提交、同快照并不等于所有打包元数据相同：本地 GBS Release=1，QB Release=2.1；find-debuginfo 并发为本地-j8、QB-j12，debugsource唯一目录和VCS来源字符串不同（见第5节）。','',ev('completed/plan.json')+'、'+ev('completed/evidence/final-audit.json')+'。','',
'GBS 原始成功日志：`'+log['path']+'`，'+str(log['bytes'])+' B / '+str(log['lines'])+' 行，SHA256 `'+log['sha256']+'`。行号均以此原始日志为准。压缩副本：'+ev('completed/gbs-original-0.log.gz')+'。','',
'## 3. 验证结论、身份与 FLAGS','',
'|项目|自动结论|说明|','|---|---|---|']
notes={'QB-flags-exact':'去掉时间前缀后与QB逐字相同；WARNING 0条','QB-three-stage-sha-exact':'三个SHA均相同，见下表','QB-profile-counts':'N/M/S/U/Q/R全部相同','anchors':'已有锚点检查通过','debuglink-and-debugfiles':'文件名、CRC、identity及debugfiles.list检查通过','QB-23-packages':'3 PASS / 20 FAIL，不放宽门禁','QB-objects90':'第一个输入缺失；0/90完成，非目标文件内容不一致'}
for k,v in val['checks'].items():text.append(f'|{k}|{v}|{notes[k]}|')
text+=['',ev('completed/validation/result.json')+'、'+ev('completed/validation/failure.txt')+'。','','|阶段|本轮与QB的共同SHA256|','|---|---|']
for x in read(V/'three-stage-sha.json'):text.append('|'+x['stage']+'|`'+x['actual']+'`|')
text.append('|clang-22.debug|`'+syms['actual']+'`|')
text+=['',f'最终clang为152,532,400字节；符号文件为{syms["bytes"]:,}字节。符号文件再次只读计算SHA，等于QB期望值；debuglink文件名 `clang-22.debug`，CRC32={ident["debug_file"]["crc32"]}。RUNPATH=`$ORIGIN/../lib64`，DT_RPATH为空。'+ev('symbols-qb-check.json')+'、'+ev('completed/validation/three-stage-sha.json')+'、'+ev('completed/validation/debuglink.json')+'。','',
'Profile：`N='+str(counts['N'])+' M='+str(counts['M'])+' S='+str(counts['S'])+' U='+str(counts['U'])+' Q='+str(counts['Q'])+' R='+str(counts['R'])+'`；R×100约0.004238545331242318%，与QB全部相同。'+ev('completed/validation/pipeline.json')+'。','','FLAGS原文（两条存在，WARNING为0条）：','```text',(E/'flags-with-lines.txt').read_text().strip(),'```','',
'与QB的expected/actual原文：'+ev('completed/validation/flags.json')+'。主要门禁、三处real和缓存释放原文：'+ev('anchors-with-lines.txt')+'；完整自动锚点记录：'+ev('completed/validation/anchors.json.gz')+'。','',
'## 4. 23包逐包比较','',
'old=本地，new=QB。版本/release、VCS、payload mtime单列；比较器不会仅因这些RPM头元数据判FAIL，但实际文件路径、文件mode、DWARF内容变化仍被拒绝。下表“文件差异”包括内容或权限变化，不把同SHA但mode不同冒称字节内容改变。','',
'|包/架构|结论|文件差异数|新增路径|移除路径|payload mtime变化数|','|---|---|---:|---:|---:|---:|']
for x in r:text.append('|'+x['package'].replace('\t',' / ')+'|'+('PASS' if x['PASS'] else 'FAIL')+'|'+ '|'.join(map(str,[len(x['content_changes']),len(x['added']),len(x['removed']),len(x['payload_mtime_changes'])]))+'|')
text+=['',ev('completed/validation/qb-rpm-comparison.json.gz')+' 保留每包完整判定和metadata；'+ev('all-file-differences.tsv.gz')+'逐项列出全部281个文件差异及24,284条新增/移除路径，不省略debugsource文件名。mtime每个路径及前后值也在原始比较JSON。','',
'`llvm-static-devel` 的225个归档没有内容变化（不是靠放宽ar日期规则通过），只有225条payload mtime变化；`libomp-devel`、`python-clang`同样无内容变化。clang-22和其专属符号文件相同，并不意味着整个clang/clang-debuginfo包相同：两包内其他工具和符号仍有下述差异。','',
'## 5. 差异的只读归因（不改比较结论）','',
'### 5.1 DWARF与debuglink','',
'比较器遇到首个非记录节差异即拒绝：218条报 `.debug_info`，46条报 `.debug_line`。它对带debuglink的二进制先检查配套.debug，因此这些错误不代表二进制本体包含该节。随后只读检查全部264个ELF：132个二进制的内容变化节是 `.gnu_debuglink`；132个配套符号文件的变化节均为 `.debug_info`、`.debug_line`、`.debug_str`；程序头均相同。各节大小、偏移和SHA见 '+ev('difference-details.json')+'。这份诊断不替代原门禁，也不把DWARF节纳入允许清单。','',
'132个.debug文件的 `.debug_str`，仅将 `usr/src/debug/llvm-22.1.8-1.x86_64` 替换为 `usr/src/debug/llvm-22.1.8-2.1.x86_64` 后，整节与QB逐字节相同（132/132）。平台处理命令原文：','```text',
'本地 L24621: [ 9423s] + /usr/lib/rpm/find-debuginfo.sh -j8 --build-id-seed 22.1.8-1 --unique-debug-src-base llvm-22.1.8-1.x86_64 -S debugsourcefiles.list /home/abuild/rpmbuild/BUILD/llvm-22.1.8',
'QB 1216409 L24664: [ 8649s] + /usr/lib/rpm/find-debuginfo.sh -j12 --build-id-seed 22.1.8-2.1 --unique-debug-src-base llvm-22.1.8-2.1.x86_64 -S debugsourcefiles.list /home/abuild/rpmbuild/BUILD/llvm-22.1.8','```','',
'QB原文出处：[57号§3 find-debuginfo](57_qb_1216409_1216410.md#find-debuginfo-与-release-清理)。已证实路径字符串差异来自不同Release对应的debugsource目录。**推测** `.debug_info`/`.debug_line` 的相关变化来自debugedit对字符串和目录引用的重写；本轮没有逐条解码所有DWARF引用，不能声称所有DWARF差异已被语义等价证明。现有严格门禁保持FAIL。','',
'### 5.2 debugsource路径','',
'本地和QB各12,142个路径，以 `llvm-22.1.8-1.x86_64` / `llvm-22.1.8-2.1.x86_64` 为前缀。只读按此前缀一一对应后，mode/uid/gid/大小/SHA/链接目标全部相同，未对应或其他差异为0。但原始包的路径集合不同，因此原判定仍是FAIL。全部对应关系：'+ev('debugsource-prefix-pairs.json.gz')+'。','',
'### 5.3 源码RPM','',
'17个载荷文件的mode为本地0664、QB0644；其中16个文件SHA相同。`llvm.spec`还存在VCS来源路径、Release 1/2.1，以及GBS `%patch -P N` 对QB `%patchN` 的导出语法差异。完整diff如下，源码仓库本身没有修改：','```diff',(E/'source-spec.diff').read_text().strip(),'```','',
'### 5.4 逐文件差异表','',
'以下列出281个内容/权限差异；debugsource的24,284条路径新增/移除见第4节完整TSV和第5.2节对应表。“符号严格失败”指相关.debug不满足原规则，不能仅看到二进制CRC变化就判通过。','',
'|包|文件|实际变化节/元数据|原因与原判定|','|---|---|---|---|']
for x in details:
 sec=', '.join(s['section'] for s in x['changed_sections'])
 if sec=='.gnu_debuglink':why='配套.debug的非记录节变化；FAIL'
 elif sec:why='DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL'
 else:sec='mode 0664→0644'+('; spec文本' if x['path']=='llvm.spec' else '，字节SHA相同');why='源包权限（及spec导出）差异；FAIL'
 text.append('|'+x['package'].replace('\t',' / ')+'|`'+x['path']+'`|'+sec+'|'+why+'|')
text+=['','## 6. 90 TU：未完成，未重跑','',
'失败原文：','```text',"FileNotFoundError: [Errno 2] No such file or directory: '/home/linhao/Toolchain/development/llvm-optimize/temp/hybrid-local-20261023/tu-inputs/000.ii'",'```','',
'验证器读取 `W/docs/53_hybrid_local_validation_evidence/tu-inputs.json` 中旧的copy路径，在第一个输入SHA检查处失败，尚未调用参考编译器。本轮没有完成任何一对目标文件比较，不能写90/90，也不能把clang文件SHA相同替代这项实测。该父目录已在[64号第27项](64_disk_cleanup.md)按当时用户批准清单删除；本轮未再次删除它。没有恢复输入、改入口、重跑或自行选用另一份资产。'+ev('completed/validation/failure.txt')+'。','',
'## 7. 资源和时间线','',
'以下原样保存入口生成的resource-table.md。阶段界限来自GBS原始日志 `[NNNNs]`，不是轮询观察时刻。cgroup分阶段值是采样memory.current最大值（含文件缓存），并非各阶段独立memory.peak；VmHWM仅观察llvm-bolt，全进程最大值UNKNOWN。du限时失败的单次样本保留原文，不插值。','',
(R/'resource-table.md').read_text().strip(),'',
'整轮构建cgroup memory.peak=18,533,765,120 B（17.261 GiB，含文件缓存），oom/oom_kill均0，swap峰值0。根du已成功采样的最大值67,730,743,296 B（63.079 GiB），不是保证捕获所有瞬时尖峰的理论上限；构建资源采样的/home最低可用463,856,259,072 B（约432.000 GiB）。验证阶段controller还保留单独观测：23:22 memory.peak=6,408,904,704 B；这不是构建服务峰值。'+ev('monitor.jsonl')+'。','',
'GBS锚点：','', '|阶段|起点秒|原始行号|','|---|---:|---:|']
for phase,z in log['phases'].items():text.append(f'|{phase}|{z["seconds"]}|L{z["line"]}|')
text+=['',ev('completed/evidence/resource-table.json')+'、'+ev('completed/evidence/resources.jsonl.gz')+'、'+ev('completed/evidence/du-root.jsonl')+'、'+ev('completed/evidence/bolt-process.jsonl')+'。采样文件是否压缩以'+ev('provenance.json')+'为准。','',
'## 8. 现场与交付范围','',
'入口结束审计：构建/准备服务inactive，挂载列表为空，remaining_build_processes=[]。只使用入口已有的正常收尾；没有懒卸载、杀外部进程、手动sudo或重试。controller保留failed状态供排查。构建根、RPM、比较payload和失败记录均保留。LLVM源码、spec、helper、启动入口均未修改。'+ev('completed/evidence/final-audit.json')+'。','',
'采集时/home：'+str(space['available_bytes'])+' B（'+str(round(space['available_bytes']/2**30,3))+' GiB），时间 '+space['time']+'。'+ev('df-final.txt')+'。','',
'完整原始成功日志、自动验证原文、资源采样、每包manifest和逐文件差异已入证据目录；大文本gzip压缩，来源/原大小/原SHA/压缩SHA记录于provenance.json。诊断仅解释失败，没有改变任何验证判定。','',
'**最终结论：构建成功，整体验证有问题（23包20 FAIL；90 TU缺输入未完成），本轮停止且保留现场。**','']
(B/'docs/bolt/63_qb_snapshot_rebuild.md').write_text('\n'.join(text))
print('written 63',len(text),'lines')
