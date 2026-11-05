from pathlib import Path
import json,datetime,gzip
E=Path(__file__).resolve().parent;B=E.parents[3]
j=lambda n:json.loads((E/n).read_text()) if (E/n).exists() else json.loads(gzip.open(E/(n+'.gz'),'rt').read())
def avail(d):
 try:return int(d['stdout'].splitlines()[-1].split()[3])
 except Exception:return None
def size(b):return 'UNKNOWN' if b is None else f'{b:,} B ({b/2**30:.3f} GiB)'
inv=j('inventory.json');repos=j('repositories.json');audit=j('root-audit.json') if (E/'root-audit.json').exists() else {};backup=j('backup-manifests.json');slims=j('slim-results.json')
r=(E/'root-delete.stdout').read_text();dfrows=[l for l in r.splitlines() if l.startswith('/dev/')];before=int(dfrows[0].split()[3]) if dfrows else None;after=int(dfrows[-1].split()[3]) if dfrows else None
x=['# 66：清理与 QB 同快照重建启动准备（2026-11-05）','',
'本轮只执行用户明确授权的清理。qb_analysis整体删除；备份精简因恢复条件或普通用户权限不足保留；65号瘦身仅删除历史SHA与本次SHA相同的精确候选文件。没有扩大范围、修改LLVM源码或夜间入口。','',
'证据：`tools/bolt/results/disk-cleanup-20261105c/`。W为`/home/linhao/Toolchain/development/llvm-optimize`。df差值是该时间窗口整个/home文件系统的变化，可能含其他进程写入，不冒称精确的单目录块释放量。','',
'## 1. 删除 qb_analysis','',
'用户明确豁免逐仓库源码保全；本轮只登记，不导出patch或bundle。顶层清单及du见inventory.json，全部仓库路径/HEAD/未推送候选见repositories.json。未推送按本地remote-tracking refs统计；缺失或陈旧refs会高估，不能当成远端实际未发布的证明。',
f"发现{len(repos['rows'])}个仓库；du原文：",'```text',inv['du']['stdout']+inv['du']['stderr'],'```',
'沿用52号zenity + sudo -A；清理LD/GTK环境，同一次sudo最多三次弹窗，取消锁定。密码不保存、不输出。执行前打印完整root-delete.sh及SHA；源码保护已由用户豁免。只有这一部分调用sudo。','',
'root补查：'+str(audit.get('pass','NOT RUN'))+'；真实目录/realpath一致、非软链接；findmnt及所有可读/proc/*/mountinfo无挂载/overlay引用；/proc cwd/root/exe/fd/maps无占用；系统及用户活动服务未引用。完整原文见root-audit.json。','',
'实际删除命令：','```sh','rm -rf --one-file-system -- /home/linhao/qb_analysis','```','',
'执行原文：','```text',r.rstrip(),'```',f'该窗口可用空间：{size(before)} → {size(after)}；净增 {size(after-before) if before is not None and after is not None else "UNKNOWN"}。认证记录见auth-attempts.log；stderr保留IBUS窗口环境警告。','',
'## 2. 精简源码备份：保留，未删除','',
'逐组校验原SHA256SUMS中的补丁/inspection摘要，所有补丁通过git apply --numstat --allow-empty解析；检查format-patch覆盖的commit、父链、HEAD重建路径，再用64号published-llvm-refs已保存结果证明基础提交可达。根提交、非线性历史、旧测试夹具字段缺失或无法证明基础可取得的组不放行。没有重新查询或修改Gerrit。','',
'26组中9组恢复条件通过，但目录均root:root且普通用户不可写。本任务只允许第一部分使用root删除，因此这9组也未删除；没有第二次sudo、chmod或所有权修改。其余17组保留。`backup-manifests.json`列出每个format-patch的完整commit/parents、index/worktree基准、stash父提交、Gerrit基础可取得性与原因。因原备份目录不可写，manifest保存在本次证据目录；原备份manifest/SHA256SUMS未更改，内容仍完整保留。','',
'|备份子目录|恢复检查|基础提交|实际处理/原因|','|---|---|---|---|']
for z in backup:x.append('|`'+str(Path(z['directory']).relative_to(Path('/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105')))+'`|'+('通过' if z['eligible'] else '未通过')+'|`'+str(z.get('series_base','NONE/UNKNOWN，见逐补丁parents'))+'`|'+z['execution_reason'].replace('|','/')+'|')
x+=['','其他顶层_selftest、_alternates-restoration等不属于可证明安全删除的bundle/readback候选，全部保留；见backup-unclassified-top.json。','',
'精简前后du：','```text',j('backup-du-before.json')['stdout'].rstrip(),j('backup-du-after.json')['stdout'].rstrip(),'```',
'前后df：','```text',j('backup-df-before.json')['stdout'].rstrip(),j('backup-df-after.json')['stdout'].rstrip(),'```',(E/'backup-finished.txt').read_text().strip(),'',
'## 3. 65号精确候选瘦身','',
'删除边界只取65号recommendation.json与suggested-files.tsv.gz，不扩展到父/同级目录。65号中没有逐文件历史SHA的目录候选保持整体原样，不能把本次现算SHA当作65号基线。已记录SHA的普通文件再核对真实路径、属主、inode/mtime稳定、当前SHA一致后，用普通用户rm -f --删除该文件；不删除空父目录，不使用sudo。','',
'普通用户/proc及findmnt检查没有可见占用/挂载；/proc权限盲区完整保存，不宣称root级全机检查。逐文件当前SHA查询、删除命令/rc、跳过原因及每项df在slim-<目录>.json。','',
'|目录|删除文件数|保留候选数|df可用空间净增|结论|','|---|---:|---:|---:|---|']
for z in slims:
 q=j('slim-'+z['name']+'.json');b=avail(q['df_before']);a=avail(q['df_after']);x.append(f"|`{z['name']}`|{z['deleted']}|{z['retained']}|{size(a-b) if a is not None and b is not None else 'UNKNOWN'}|{'部分保留（历史SHA缺失）' if z['retained'] else '候选全部删除'}|")
x+=['','cache-release的两份解包目录、内网源码检出/导出和MLGO解包root因缺完整的65号逐文件SHA，整组保留；所有products、原始RPM、独有符号复现文件和未发布源码保持原样。','', '结束行原文：','```text',(E/'slim65.stdout').read_text().rstrip(),'```','',
'## 4. 清理结束与构建入口','',
'前三部分全部结束后才检查98.8GiB、全新根和无其他GBS/rpmbuild运行三项条件。实际启动与自动验证结果另见[63号](63_qb_snapshot_rebuild.md)；只使用用户指定命令，没有重试或修改入口。',
'```sh','/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/night-launch-20261105/launch.sh 9e39fa8a61392652bb28b75fc26216675bcad1d5 full','```']
(B/'docs/bolt/66_disk_cleanup.md').write_text('\n'.join(x)+'\n');print('66 written')
