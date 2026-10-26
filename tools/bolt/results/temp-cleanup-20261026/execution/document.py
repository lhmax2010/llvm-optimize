"""Append actual outcomes after the cleanup controller has finished."""
from pathlib import Path
import json, hashlib, re, subprocess
E=Path(__file__).resolve().parent;B=E.parents[4];W=Path('/home/linhao/Toolchain/development/llvm-optimize');G=2**30
load=lambda n:json.loads((E/n).read_text())
rows=load('deletion-results.json');pres=load('preservation.json')
assert len(rows)==10, 'incomplete controller results require manual accounting'
def df(n):
 r={}
 for line in (E/n).read_text().splitlines()[1:]:
  a=line.split();r[a[-1]]=dict(device=a[0],free=int(a[3]))
 return r
before=df('df-before-preservation.txt');after=load('filesystem-after-cleanup.json')
log=W/'temp/cleanup-20261026.log';text=log.read_text();assert 'CLEANUP FINISHED' in text.splitlines()[-1]
(E/'cleanup-20261026.log').write_text(text)
lines=['','## 9. 执行记录：用户批准的10个精确范围（2026-10-26）','',
'批准人：用户在本会话明确批准38号稳妥及激进方案的10个精确路径，授权先普通用户rm，root权限残留才通过图形密码框sudo -A清理同一路径。未授权扩大到父目录、同级目录或“不确定”组。本节是实际执行；前8节保持盘点快照，不回写历史空间数字。',
'','### 9.1 保全与检查','',
'逐个读取 `preserve-before-delete.json`：有同SHA的外部副本重新核对源及副本；其余复制到各父目录 `preserved-before-delete/<构建根名>/`，保留源相对路径。未有历史SHA的依赖RPM本次计算源SHA再与副本比较。每个保全目录生成manifest与SHA256SUMS。复制仅写新目录，不移动原文件，也不修改原products/脚本。',
'','| 项 | 保全清单条目 | 本次复制 | 既有同SHA副本 | 结果 |','|---|---:|---:|---:|---|']
for i in range(1,5):
 r=pres['roots'][str(i)];a=r.get('entries',[])
 lines.append(f'| {i} | {len(a)} | {sum(x.get("action")=="copied" for x in a)} | {sum(x.get("action")=="verified existing copy" for x in a)} | {r["status"]} |')
lines+=['',f'hybrid+BOLT的8个运行库及整个resource-dir：**{pres["runtime"]["status"]}**，保全到 `T/bolt-on-hybrid-20261024/perf-runtime/`；原相对符号链接布局保留，README说明以后重跑34号时重定向loader、运行库和resource-dir。',
'', '删除载荷前复核三组原包：'+ '；'.join(k+': '+v['status']+' '+str(len(v.get('files',[])))+'/22' for k,v in pres['rpm_sets'].items())+'。7/10依赖docs35，8依赖docs38，9依赖docs49；三组原RPM均不在删除范围。',
'','逐项按realpath、自身/父目录非软链接、文件系统设备、lsof +D/fuser、/proc/*/mountinfo顺序检查。进程命中即跳过，该项后续挂载与删除检查不再执行。lsof +D对root专用系统目录有Permission denied可见性警告，原文保存，并补全局可见lsof路径匹配；不把权限警告冒称完整root进程可见性。进程命中、未知错误或挂载引用都会阻止删除；检查详细结果见每项checks/日志。',
'','### 9.2 逐项执行','',
'| 项 | 精确路径 | 保全/原包前提 | 结果 | sudo | 总耗时秒（含检查/认证等待） | 对应盘df增加GiB |','|---|---|---|---|---:|---:|']
for r in rows:
 i=r['number'];fs='/home' if i in (1,2,3,4,6,7,8,9) else '/';b=r.get('df_before',{}).get(fs,{}).get('available');a=r['df_after'][fs]['available'];delta=f'{(a-b)/G:.3f}' if b is not None else '未执行'
 req='保全PASS' if i<=4 else '原包'+r['rpm_set']+' PASS' if 'rpm_set' in r else '无附加保全要求'
 lines.append(f'| {i} | `{r["path"]}` | {req} | {r["status"]} {r.get("reason","")} | {"是" if r["sudo"] else "否"} | {r["seconds"]:.1f} | {delta} |')
for r in rows:
 if r['status']!='deleted':
  prefix=E/f"item-{r['number']}-before-fuser"
  evidence=''.join(Path(str(prefix)+'.'+ext).read_text() for ext in ['stdout','stderr'] if Path(str(prefix)+'.'+ext).exists())
  if evidence.strip():lines+=['',f"第{r['number']}项fuser命中原文（未结束该进程）：",'', '```text',evidence.rstrip(),'```']
lines+=['','跳过项：'+ ('；'.join(str(r['number'])+' '+r.get('reason','')+('（普通rm已执行，可能已部分释放）' if 'rm' in r else '') for r in rows if r['status']!='deleted') or '无')+'。', '', '实际执行命令（完整stdout/stderr、返回码和时间保存在execution目录）：','', '```sh']
for r in rows:
 for k in ('rm','sudo_rm'):
  if k in r:lines.append(' '.join(r[k]['argv']))
lines+=['```','', '第1项sudo命令墙钟时间包含图形密码框等待，不是纯删除耗时；原命令耗时见JSON。sudo使用新建的图形askpass包装器，不在终端输入密码、不记录密码，每项首次认证失败后不循环索取密码。没有chmod任何现有文件，没有结束占用进程，没有使用强制或懒卸载。挂载处理以日志为准。',
'','### 9.3 两块盘前后空间','', '| 文件系统 | 保全前可用GiB | 清理结束可用GiB | 净增加GiB |','|---|---:|---:|---:|']
for fs in ('/home','/'):
 lines.append(f'| {before[fs]["device"]}（{fs}'+('，/var/tmp所在盘' if fs=='/' else '')+f'） | {before[fs]["free"]/G:.3f} | {after[fs]["available"]/G:.3f} | {(after[fs]["available"]-before[fs]["free"])/G:.3f} |')
lines+=['','保全目录实占见preserved-du.txt，约7.78 GiB；高于盘点的5.517 GiB预算，因为本次逐路径复制933项，没有对保全副本再做内容去重，另保留完整perf-runtime。', '', '净变化包括本次新增保全文件、文件系统元数据和同期其它写入，不能把各项du简单相加当成df保证。两盘不相加。所有products、验证输入、perf父目录、profile、QB配置、旧R1、ARM树、源码和三组原RPM保留；未列出的目录没有删除命令。','', '**结束标记原文：**','', '```text',text.splitlines()[-1],'```','', '### 9.4 补记2026-10-22晚间用户清理','',
'根据用户本次说明，以下清理由用户在2026-10-22晚间运行 `cleanup_home_20261022.sh` 完成。读取到 `W/temp/cleanup-20261022-evening.log`；不是本轮操作。它解决了盘点时P4与旧R1缓存去向不明的问题。日志完整原文如下：','','```text',(E/'cleanup-20261022-evening.log').read_text().rstrip(),'```','',
'日志记载删了旧R1缓存（显示92G）、旧archivefix树缓存（11G）和旧演练upper（61G），/home可用由340 GiB增至500 GiB，即日志取整口径约160 GiB，不能伪装成精确字节值。`preserved-from-upper/`当前包含所列14个产物及1份SHA256SUMS（共15个普通文件），清单另存 `preserved-from-upper-files.tsv`；本轮没有修改这些文件。','',
'本轮材料：[execution](../../tools/bolt/results/temp-cleanup-20261026/execution/)。完成后停下，不执行其它清理。']
doc=B/'docs/bolt/38_temp_cleanup_inventory.md';s=doc.read_text();assert '## 9. 执行记录' not in s;doc.write_text(s+'\n'.join(lines)+'\n')
status=B/'docs/bolt/STATUS.md'
with status.open('a') as f:
 f.write('\n\n## 2026-10-26：38号批准范围清理执行\n\n用户明确批准10个精确范围；先保全，再逐项核对并删除。结果见[38号第9节](38_temp_cleanup_inventory.md#9-执行记录用户批准的10个精确范围2026-10-26)及 `tools/bolt/results/temp-cleanup-20261026/execution/`。\n\n')
 f.write('- '+text.splitlines()[-1]+'\n')
 for fs in ('/home','/'):
  f.write(f'- {before[fs]["device"]} {fs}：保全前可用{before[fs]["free"]/G:.3f} GiB，结束{after[fs]["available"]/G:.3f} GiB，净增{(after[fs]["available"]-before[fs]["free"])/G:.3f} GiB。\n')
 f.write('- 保全清单及SHA256SUMS已生成；products、TU/C/C++输入、profile、QB配置、源码与不确定范围保持。未运行构建、未推送Gerrit。\n- 已据用户说明与原日志补记10-22晚间旧R1/旧archivefix缓存及P4 upper清理，日志340→500 GiB；14个保全产物及SHA256SUMS仍在。\n- 本次授权仅这10项，不延伸到其它目录。完成后停止。\n')
print(text.splitlines()[-1])
