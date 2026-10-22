#!/usr/bin/env python3
from pathlib import Path
import os,json,re,datetime,hashlib
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=Path(__file__).resolve().parent
GB=2**30; threshold=5*GB;mainsha='8a276db1cb7b0824ea82ea2cba0f0f49e6cc4a91';bsha='4513444f57a6e5e99d15607aa0de2418d1bf1671'
a=json.loads((D/'annotations.json').read_text()); activity=json.loads((D/'activity-by-unit.json').read_text()); measurements={};allrows={}
for file in ['du-filesystem-0.stdout','du-filesystem-2.stdout','du-project.stdout']:
 for i,l in enumerate((D/file).read_text().splitlines(),1):
  try:n,t,p=l.split('\t',2);allrows[p]={'path':p,'bytes':int(n),'latest_descendant_mtime':t,'du_evidence':file+':'+str(i),'method':'filesystem traversal; cross-root hardlinks counted once'}
  except ValueError:continue
for p in json.loads((D/'all-unit-paths.json').read_text()):
 if p in allrows:measurements[p]=dict(allrows[p])
records=[('du-units.json',i,r) for i,r in enumerate(json.loads((D/'du-units.json').read_text()))]
if (D/'du-additional.json').exists():records += [('du-additional.json',i,r) for i,r in enumerate(json.loads((D/'du-additional.json').read_text()))]
for measurefile,i,r in records:
 if 'bytes' in r:
  out=r['stdout'].strip().split('\t',2)
  measurements[r['path']]={'path':r['path'],'bytes':r['bytes'],'latest_descendant_mtime':out[1],'blind_spots':bool(r['stderr']),'du_exit':r['rc'],'du_evidence':measurefile+' entry '+str(i+1),'method':'independent du -sx; hardlinks unique within this root'}
# Large original directories not all independent Git roots; never sum these nested rows.
for p,r in allrows.items():
 name=Path(p).name
 if name in {'lto.cache','lto-cache','BUILDROOT','review49-independent-install','independent-install','baseline-rpm-extract','RPMS','rpmbuild','bolt-work','build'} and ('llvm' in p.lower() or 'gbs' in p.lower()):
  if p not in measurements:measurements[p]=dict(r)
# Include any additional large external GBS/cache/export directories discovered by full scan.
for p,r in allrows.items():
 if any(x in p.lower() for x in ['/gbs-root','/.gbs_export','/lto.cache','/lto-cache']) and not any(p==u or p.startswith(u+'/') for u in measurements):measurements[p]=dict(r)
# M0G/M1 external projects (not ordinary unrelated user directories).
for p,r in allrows.items():
 if p in ['/home/linhao/Toolchain/development/MLGO','/home/linhao/Toolchain/development/llvm_inline_development'] and p not in measurements:measurements[p]=dict(r)
measurements={p:r for p,r in measurements.items() if r['bytes']>threshold}
errors='\n'.join((D/f).read_text() for f in ['du-filesystem-0.stderr','du-filesystem-2.stderr','du-project.stderr'])
for p,r in measurements.items():
 r.setdefault('blind_spots',p+'/' in errors)
 try:s=Path(p).stat();r.update(root_mtime=datetime.datetime.fromtimestamp(s.st_mtime).astimezone().isoformat(),device_number=s.st_dev)
 except OSError as e:r['stat_error']=str(e)
 r['filesystem_device']='/dev/sda1' if p.startswith('/home/') else '/dev/nvme0n1p1';r['mountpoint']='/home' if p.startswith('/home/') else '/'
 parents=[u for u in a if p.startswith(u+'/')];parent=max(parents,key=len) if parents else None
 ann=dict(a.get(p,a.get(parent,{'source':'未知','purpose':'其他LLVM/GBS资料','ref':'main/docs/41_disk_inventory.md:326','protected':'其他项目；未知','dependency':'用途/下游引用未穷举','advice':'保留','reason':'未证明可安全废弃','assets':'独有二进制未认证，先保留','owner':'其他 LLVM 项目'})))
 if p not in a:
  ann['purpose']='内含 '+Path(p).name+'；'+ann['purpose'];ann['advice']='随父目录保留' if '删除' not in ann['advice'] else '随 upper 处置，不另计';ann['dependency']='已计入父目录；'+ann['dependency']
 r.update(ann);r['nested_under']=max([u for u in measurements if p.startswith(u+'/')],key=len,default=None)
 hits=[]
 for u,items in activity.items():
  if p==u:
   for it in items:
    if it not in hits:hits.append(it)
 r['visible_processes']=hits
rows=sorted(measurements.values(),key=lambda x:(x['mountpoint'],x['path']))
for i,r in enumerate(rows,1):r['id']='R%02d'%i
ids={r['path']:r['id'] for r in rows}
(D/'inventory.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
with (D/'inventory.tsv').open('w') as f:
 cols=['id','path','bytes','filesystem_device','mountpoint','latest_descendant_mtime','root_mtime','blind_spots','source','purpose','protected','advice','nested_under','du_evidence']
 f.write('\t'.join(cols)+'\n')
 for r in rows:f.write('\t'.join(str(r.get(c,'')).replace('\t',' ').replace('\n',' ') for c in cols)+'\n')
refs={};source_errors=[]
def citation(s):
 def rep(m):
  label,file,line=m.groups();base=W if label=='main' else B;p=base/file
  if p.exists():
   ls=p.read_text(errors='replace').splitlines();n=int(line)
   if n<=len(ls):refs[(label,file,n)]={'repo':label,'path':file,'line':n,'text':ls[n-1],'file_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
   else:source_errors.append(m[0])
  else:source_errors.append(m[0])
  sha=mainsha if label=='main' else bsha
  return '['+label+'/'+file+':'+line+'](https://github.com/lhmax2010/llvm-optimize/blob/'+sha+'/'+file+'#L'+line+')'
 return re.sub(r'(main|bolt)/(docs/[^; ]+\.md):(\d+)',rep,s)
def short(p):
 return p.replace(str(W)+'/temp/','T/').replace('/home/linhao/','~/')
scenario=json.loads((D/'reclaim-scenario.json').read_text());assets=json.loads((D/'preserve-assets.json').read_text())
if (D/'additional-assets.json').exists():assets+=json.loads((D/'additional-assets.json').read_text())
free={}
for l in (D/'df-final.stdout').read_text().splitlines()[1:]:
 x=l.split()
 if len(x)>=7 and x[0] in ['/dev/sda1','/dev/nvme0n1p1','/dev/nvme0n1p2']:free[x[0]]={'available':int(x[4]),'mount':x[6]}
net=scenario['net_reclaim_scenario'];hfree=free['/dev/sda1']['available'];vfree=free['/dev/nvme0n1p1']['available'];need=236149145600+30*GB
text=f'''# 31：LLVM / GBS 构建根只读盘点与处置建议

2026-10-22（Asia/Shanghai）。**只盘点；未删除、移动、改权限、挂载或构建，未推 Gerrit。所有“删除”都只是待用户逐项批准的建议。**

建议优先考虑三个可由原 RPM 重建的解包目录，以及一个先提取关键文件的旧 overlay upper。四项合计 **{scenario['gross_unique_allocated']/GB:.3f} GiB**；扣除拟保存文件 **{scenario['preserve_copy_reservation']/GB:.3f} GiB**，预计净释放 **{net/GB:.3f} GiB**，全部位于 `/home`。原始 RPM、历史候选、原构建树及 main 的 patch / hybrid 工作目录暂时保留。按本次快照，方案执行后 `/home` 预计约 **{(hfree+net)/GB:.3f} GiB** 可用，适合作为后续补测盘；`/var/tmp` 仍只有约 **{vfree/GB:.3f} GiB**，不能把两盘空间相加。

## 1. 范围、口径与盲区

- 全盘只读 `findmnt`、`df`、`du`：覆盖 `/`（含 `/var/tmp`、`/tmp`）、独立 `/home`、`/boot/efi`；没有发现第四块已挂载的本地物理盘。snap loop、tmpfs、proc 等不当作可放长期构建根的磁盘。只列 **>5 GiB（5,368,709,120 B）** 的相关目录；其他系统/个人目录不属于 LLVM/GBS 盘点范围。
- `du -x -B1 --threshold=5368709121 --time --time-style=full-iso /挂载点` 找出大目录，再对已发现的顶层候选用每目录独立的 `du -sx -B1 --time --time-style=full-iso -- 路径` 复核。没有使用 apparent-size。全盘一次遍历会把跨根硬链接只计一次，独立 du 才表示该目录单独占用的可见数据；独立目录数也不能直接相加。
- 下表的时间为 **du 看到的最新后代 mtime**，不是最后一次使用时间。目录 inode 本身的 mtime、完整纳秒时间、字节数、命令来源均在 `inventory.json/tsv`。旧源码可能带固定或未来时间戳，不能因此判断仍在构建。
- `‡` 表示只取全盘/项目遍历中的该行，跨目录硬链接可能已记到别处；独立复核过的顶层行无此标记。`†` 表示 du 遇到权限错误，是可见占用下界。GBS 根通常有 `root`、`var/cache/ldconfig`、`usr/share/upgrade` 盲区；其他用户/系统目录也可能不可读。没有 sudo、chmod 或绕过权限。因此“所有”仅覆盖当前用户可见范围，不能保证不可读目录内没有额外根。
- 可见进程使用 `lsof -nP` 全表按**路径边界**匹配，辅以 `fuser -v`、`ps`、`/proc/*/{{cwd,root,mountinfo}}` 和 `lslocks`。`fuser` 对传入目录 inode 的无命中不代表其全部后代无打开文件；无匹配也不是未来可删的证明。首次 `/proc` cwd/root 读取有297个不可读或已退出项；最终全量lsof有394条NOFD行（不等于394个独立进程），原文见 `lsof-complete-unreadable-fds.txt`。
- 本次轻量扫描使用 4 GiB/swap0 scope、nice19/ionice3；没有获取项目锁或共享重任务锁。这些只是本地扫描规则。证据目录以外没有主动写入；读取可能由文件系统更新 atime。

已在9份实存导出spec只读取得VCS行，原路径/行号/全文见 `exported-vcs.json`；`-dirty` 保留，不能把它忽略成精确干净提交。

全盘扫描 `/` 用时19.461秒、`/home` 用时2522.271秒；分别只有105、115条 Permission denied，未超时。另完成85个候选和3个追加目录的独立du。时间与退出码见 `scan-summary.json`。

原始证据：[root-inventory-20261022](../../tools/bolt/results/root-inventory-20261022/)。`du-filesystem-*.stdout/stderr` 保留完整扫描结果和盲区；`du-units.*` 是独立复核；`reclaim-scenario.json` 是四项的 inode 去重核算。`lsof-root-matches.txt` 是原始 lsof 中相关行，完整本机 lsof 留在 `T/bolt-v4-20261022-root-inventory/lsof-all.stdout`、`lsof-final.stdout` 和 `lsof-complete.stdout`，未发布无关个人应用打开文件列表。扫描不是原子快照，df/du 的采样时刻可能不同。

路径缩写：`~=/home/linhao`；`W=/home/linhao/Toolchain/development/llvm-optimize`；`T=W/temp`；`B=/home/linhao/Toolchain/development/llvm-optimize-bolt`。绝对路径全部在 `inventory.tsv`。FS **H=/dev/sda1，挂载点 /home**；**V=/dev/nvme0n1p1，挂载点 /**。证据文档读取基准：main `{mainsha}`，bolt-v4 `{bsha}`；引用精确到文件与行，保全摘录在 `cited-sources.json`。若没有可靠源码身份，明确写“未知”，不把文档仓库提交当作 LLVM 源提交。

## 2. 可独立裁决的目录清单

共 {len(rows)} 行，包含父目录和有独立意义的大缓存/安装子目录；标注“内含”者**不再相加**。状态 U0=未见可见进程打开该目录、目标 project lock 不存在；U1=本次 lsof 快照见进程句柄（不是仅凭目录mtime推定）。初始快照见 VS Code PID 6296 读取 ARM 转换目录；最终快照结果见 activity-by-unit.json。共享 `heavy-stage.lock` 只有一个 0 B 文件，`lslocks` 未见其被持有；历史 `lock.json/acquired.json/released.json` 是证据，不当作仍持锁。相关原文见 `lock-presence.json`、`local-lock-file-metadata.json`、`fuser-all.*`、`ps-after.stdout`。

| ID / 路径 | du 实占 GiB / 字节 | FS；最新后代 mtime | 源码 / 用途 / 出处 | 依赖与保护 | 使用 / 所属线 | 建议、理由；值得保全的文件 |
|---|---:|---|---|---|---|---|
'''
for r in rows:
 nested=('内含于 '+ids[r['nested_under']]+'；') if r['nested_under'] else ''
 status='U1' if r['visible_processes'] else 'U0'
 size=f"{r['bytes']/GB:.3f}{'†' if r['blind_spots'] else ''}{'‡' if r['method'].startswith('filesystem') else ''} / {r['bytes']:,}"
 text+=f"| {r['id']} `{short(r['path'])}` | {size} | {'H' if r['mountpoint']=='/home' else 'V'}；{r['latest_descendant_mtime'][:19]} | {r['source']}；{r['purpose']}。{citation(r['ref'])} | {nested}{r['dependency']}。保护：{r['protected']} | {status}；{r['owner']} | **{r['advice']}**：{r['reason']}。{r['assets']} |\n"
text+='''
外部 LLVM/GCC/C99/MLGO/M1 目录的准确源码身份与当前负责人未全部确认；这里的“保留”是证据不足时的建议，不是断言仍在编译。其他项目的源码 Git 目录即使大于5GiB，也不当作构建缓存直接删除。对于父目录下的微小导出/overlay work、未超过5GiB的根，不单独列入大目录表；原始扫描和独立单位结果仍能查到。未知范围不能据此归零。

## 3. overlay、硬链接与原树保护

最后一次 lsof 对清单路径无可见句柄，fuser 无命中；初始快照的 VS Code 句柄已经不在末次快照中。权限盲区仍存在，不能因此解除保护。

当前宿主 `mountinfo` 和可读取的所有进程 mountinfo 中，均未发现活动 overlay 或 llvm-optimize 挂载（`process-mounts.json`）。这只说明目前未挂载，**旧 upper 仍有下层依赖**：

```text
T/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0
  └─历史 lower → T/bolt-v4-20261015-install-rehearsal/upper
                   （work 同父目录；merged 现已卸载）
  └─main hybrid52 的 clang / CMake / Ninja 工具环境
  └─docs26现存 upper / upper-parse / upper-final
  └─docs27 narrow-disk现存 upper-rpm（以上四个各自小于5GiB）
```

'''+citation('bolt/docs/bolt/25_real_install_rehearsal.md:90; main/docs/52_hybrid_link_tizen_base.md:49')+'''。`overlay-dependency-excerpt.txt` 保存原 wrapper 的 lowerdir/upperdir/workdir 原文。删除 lower 会使旧 upper 无法按原方式重新挂载，并使 main hybrid 的旧复验入口失去工具；删除 upper 只丢弃那次中止演练的写层，不会改 lower。当前方案仅建议保全后删除 docs25 的 upper，lower 保留。docs26/27四个小upper的独立du见 `other-overlay-upper-du.json`；disk-diagnostics旧脚本也引用同一下层，但该目录本次未见残存upper，不能把脚本路径当成现存挂载。

`/home/abuild/rpmbuild/BUILD/llvm-22.1.8` **是 chroot 内路径，宿主没有 /home/abuild**，不能直接把它理解成 /home 盘上的目录：

| 上下文 | 宿主根 | 保护原因 / 当前仍需内容 |
|---|---|---|
| docs49交接后、BOLT“原树禁用” | `/var/tmp/llvm-optimize-x86-archivefix-20261013/local/BUILD-ROOTS/scratch.x86_64.0` | 两次失败CMake配置改写生成头，恢复mtime会触发大量重编；PM禁止在原树运行cmake/ninja（含 -n/-P）。仍需7df普通clang、strip/resource-dir、重链输入、候选与22RPM；禁止配置不等于可删除 |
| docs35/38旧Rnew、docs25 overlay的lower | `T/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0` | 原始下层只读，含旧普通工具及docs38包；main hybrid52也复用工具；本轮没有直接执行树内工具 |
| 历史R1 | `T/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0` | f111历史资格实验环境，仍有1da7历史llvm-bolt及旧基准；不能与上两根混同 |

'''+citation('main/docs/49_x86_build_resume_result.md:238; bolt/docs/bolt/16_fallback_and_config_install.md:8; bolt/docs/bolt/15_rpm_environment_execution.md:42; bolt/docs/bolt/02_inventory.md:21')+'''

`/var/tmp/llvm-optimize-x86-archivefix-20261013-new-rpm-repo` 的22RPM与原根RPMS是硬链接（'''+citation('main/docs/49_x86_build_resume_result.md:167')+'''，本次 inode 核查见 `rpm-hardlinks.json`）。只删某一份目录，其他链接仍在，就不能算释放整份RPM数据。此处两者均建议保留。对 T 下深度≤4的软链接另做了只读检查（`shallow-external-symlinks.json`）；这不是全局脚本/软链接依赖的穷举证明，未知外部引用仍需删除前确认。四个优先处置目录则已逐inode确认没有外部硬链接；其总量不与父目录或嵌套BUILDROOT/lto.cache重复相加。

main 的 patch / hybrid 线最近使用 `T/hybrid-link-20261015`、`T/hybrid-sandbox-20261019`、`T/llvm-optimize-intranet-20261020`；源6e9d4f2b的源码归档刚完成，仍等待服务器构建验证。'''+citation('main/docs/STATUS.md:7; main/docs/STATUS.md:9; main/docs/52_hybrid_link_validation.md:5')+'''。这些目录和关联Rnew工具环境均保留。PID与Codex会话的精确归属没有从`ps`证明；不把“当前未见编译进程”写成“另一会话已弃用”。

## 4. 两盘的处置方案与补测位置

| 文件系统 / 挂载点 | 本次df可用 B / GiB | 建议删除的原占用 | 拟保全文件占用 | 预计净释放 | 处置后预计可用 |
|---|---:|---:|---:|---:|---:|
'''
text+=f"| /dev/sda1 `/home` | {hfree:,} / {hfree/GB:.3f} | {scenario['gross_unique_allocated']:,} B / {scenario['gross_unique_allocated']/GB:.3f} GiB | {scenario['preserve_copy_reservation']:,} B / {scenario['preserve_copy_reservation']/GB:.3f} GiB | {net:,} B / {net/GB:.3f} GiB | {hfree+net:,} B / {(hfree+net)/GB:.3f} GiB |\n"
text+=f"| /dev/nvme0n1p1 `/`，含 `/var/tmp` | {vfree:,} / {vfree/GB:.3f} | 0 | 0 | 0 | {vfree:,} B / {vfree/GB:.3f} GiB |\n"
text+=f"| /dev/nvme0n1p2 `/boot/efi` | {free['/dev/nvme0n1p2']['available']:,} / {free['/dev/nvme0n1p2']['available']/GB:.3f} | 0 | 0 | 0 | 不适合构建根 |\n"
text+=f"\n若仅批准 **P1–P3**，可释放 {sum(x['allocated_bytes'] for x in scenario['roots'][:3]):,} B（{sum(x['allocated_bytes'] for x in scenario['roots'][:3])/GB:.3f} GiB），`/home` 预计可用 {(hfree+sum(x['allocated_bytes'] for x in scenario['roots'][:3]))/GB:.3f} GiB；P4 的旧演练上层可继续原样保留。P4 是增加余量的可选项，不是启动任何操作的自动授权。其 upper、upper/home 等目录实际为 UID/GID 0、mode 0755（`upper-directory-ownership.txt`），普通用户不能据可读性推定可递归删除；后续执行身份需另行确定。本轮没有提权或改权限。\n"
text+='''
仅在用户确认后才执行所批准的项；表内数字不是已经释放的空间。保全预算按文件逻辑大小向4096字节取整，已从回收量扣除；新保全目录的少量元数据未估入，实际df仍需执行后复测。没有把未知权限区计入可回收量。

'''
text+=f"29口径的本地规划下界是 **236,149,145,600 B（219.931 GiB）+ 32,212,254,720 B（30 GiB本地保留量）= {need:,} B（{need/GB:.3f} GiB）**。当前 `/home` 相对它仍差 {max(0,need-hfree):,} B；四项方案后高于这个下界 {(hfree+net-need)/GB:.3f} GiB。建议把后续全新补测根放 `/home/linhao/Toolchain/development/llvm-optimize/temp/` 下独立目录。`/var/tmp` 不能借用 `/home` 的余量；保留现有系统盘根后明显不足。\n"
text+='''
这个下界不是BOLT开启后精确峰值，也不保证下一次一定够用：29的OFF采样未覆盖最终收尾且有权限盲区，ON完整净增量仍未测。本轮不启动补测、不改代码、不将这些本地规划值写进spec。

## 5. 关键小文件保全清单（本次实际SHA）

“先抽出”只是方案，尚未复制。所有 A 项当前原位保留；只有旧 upper 内14个文件会作为四项处置方案的前置条件，详细名单、大小与预算在 `reclaim-scenario.json`。下面的17项跨不同父根，不能把全部大小再次从四项净量中扣除。普通clang虽有1.67GiB，相对整树仍适合作为最小复核资产；单独二进制不能替代其运行库/resource-dir。

| ID / 用途 | 原路径 | 文件大小 B | SHA256 |
|---|---|---:|---|
'''
for i,x in enumerate(assets,1):
 text+=f"| A{i} {x['role']} | `{short(x['path'])}` | {x.get('bytes','未知'):,} | `{x.get('sha256',x.get('error','未知'))}` |\n" if isinstance(x.get('bytes'),int) else f"| A{i} {x['role']} | `{short(x['path'])}` | 未读到 | {x.get('error','未完成')} |\n"
text+='''
`4ec07159…` 在这里是**已认证的本地历史工具后备候选**，不是本轮从QB下载并验证过的产物；不能据简称声称与QB实体相同。Source1200压缩profile和解压fdata身份均实测，未重训。历史ordinary7df与旧Rnew ordinary d25e属于不同树，不能互换。120份 `.ii`、性能逐样本数据、原始RPM和DWARF证明继续留在原父目录；本方案没有建议删除它们。其他外部项目未判定出可以替代整树的最小文件集，因此建议保留，未凭猜测填SHA。

## 6. 执行边界与复核

- 没有执行任何删除、改权限、提权、挂载、CMake/Ninja或构建；没有操作Gerrit或QB，没有新建分支。只在B与本会话temp下写采样/报告。
- lsof路径匹配草稿曾使用子串，会把`…/llvm`误匹配`…/llvm-optimize`；正式结果改为路径边界后，只剩ARM转换目录的VS Code读句柄。原树和任何产品数据未受影响。
- 已有文件定位使用rg/find与文档路径。查找时读取尚未生成的`du-units.json`一次返回不存在，随后等待扫描写出；没有把不存在的报告当成已验证结果。两处文档简称已按实际文件名校正。
- 所有删除建议都停在审批；旧报告“保留至周五”等日期已过去也不自动解除保护。后续实际删除前应再次核查进程/锁/挂载、确认提取文件SHA并复测df。此项留待用户逐项决定。
'''
priority='| 待批准项 | 目录（均在T下） | 原占用 GiB | 建议 |\n|---|---|---:|---|\n'
for i,x in enumerate(scenario['roots'],1):
 priority+=f"| P{i} | `{short(x['path'])}` | {x['allocated_bytes']/GB:.3f} | {'先保存14文件，再删除upper' if i==4 else '保留原RPM与父目录证据，删除可重建解包副本'} |\n"
text=text.replace('## 1. 范围、口径与盲区',priority+'\n## 1. 范围、口径与盲区')
(B/'docs/bolt/31_build_root_inventory.md').write_text(text)
(D/'cited-sources.json').write_text(json.dumps(list(refs.values()),ensure_ascii=False,indent=2)+'\n')
(D/'report-validation.json').write_text(json.dumps({'rows':len(rows),'citation_errors':source_errors,'reclaim_errors':scenario['errors'],'net_reclaim':net,'data_only':True},ensure_ascii=False,indent=2)+'\n')
print('rows',len(rows),'report bytes',len(text.encode()),'citation errors',source_errors)
