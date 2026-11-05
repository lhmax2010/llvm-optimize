from pathlib import Path
import json,hashlib
E=Path(__file__).parent; B=E.parents[3]
def load(n):return json.loads((E/n).read_text())
def avail(x):return int(x['stdout'].splitlines()[1].split()[3])
def gi(n):return f'{n/2**30:.3f}'
rows=load('inventory.json');rr=load('execution-results.json');rs={r['number']:r for r in rr};before=load('df-before.json');after=load('df-after.json');post=load('postcheck.json')
if (E/'alternates-restoration.json').exists():
 v=rs[10];v['original_status']=v['status'];v['status']='retained-object-store';v['reason']='原目录删除后发现第26/28/32项依赖其Git alternates对象库；从已验证副本恢复对象库，工作内容已删除，仅恢复对象库目录，未完成整项删除。未改依赖仓库配置。'
a=avail(before);z=avail(after);deleted=[r for r in rr if r['status']=='deleted'];skipped=[r for r in rr if r['status']!='deleted']
s=['# 64：2026-11-05 批准目录清理','',f'批准的34个实际路径中，整项删除 {len(deleted)} 项、未整项删除（跳过或恢复对象库）{len(skipped)} 项；编号34、35没有操作。/home 可用空间从 {gi(a)} GiB 变为 {gi(z)} GiB，整个执行窗口净增加 {gi(z-a)} GiB。PGO profiles 已移出并逐文件核对，保留目录及第1–3项的其他兄弟条目检查结果见下文；今晚构建未启动。','', '## 1. 范围与执行方式','', '用户明确批准本轮清单；仅清理这些精确目录，未扩展到父目录或同级目录。`targets.json`为完整路径表，34、35为保留编号。所有rm使用`rm -rf --one-file-system -- <精确路径>`。普通用户目录的rm以UID 1000执行，权限不足的目录以root执行。一次`sudo -A -k /bin/sh root-delete.sh`覆盖root补查、必要保全和删除；图形askpass沿用52号zenity方式，最多3次，取消锁定，不记录密码。', '', '执行前打印root-delete.sh全文及SHA256：`'+hashlib.sha256((E/'root-delete.sh').read_bytes()).hexdigest()+'`。调用器及各检查脚本SHA见executor-manifest.json。没有构建、Gerrit/sandbox推送、QB操作、权限更改或VS Code配置修改。','', '## 2. 检查与逐项结果','', '每项先核对realpath、真实目录、自身及父目录非软链接、设备/inode身份；用findmnt检查挂载及overlay，并以root补查所有可读/proc/*/mountinfo、cwd/root/exe/fd/maps及活动systemd用户服务。保全后、删除前再次检查。第2项扩大占用检查到整个oldtext-final父目录，包括VS Code。普通用户扫描的权限盲区由root补扫；没有绕过检查或卸载挂载。','', '|编号|路径（相对W/temp，36为绝对路径）|du GiB|RPM数|结果 / rm UID|df净增GiB|原因|','|---:|---|---:|---:|---|---:|---|']
W='/home/linhao/Toolchain/development/llvm-optimize/temp/'
for r in rows:
 n=r['number'];v=rs[n];du=r.get('du',{});rootdu=E/f'execution-{n:02d}/du-root.json'
 if rootdu.exists():du=json.loads(rootdu.read_text())
 try:size=gi(int(du['stdout'].split()[0]))+('（下界）' if du['rc'] else '')
 except (KeyError,ValueError,IndexError):size='UNKNOWN'
 complete=E/f'execution-{n:02d}/complete-inventory.json';nrpm=len(json.loads(complete.read_text())['rpms']) if complete.exists() else len(r.get('rpms',[]))
 reason=v['reason'].replace('|','/').replace('\n',' ')[:700]
 if n==20:reason='Git公共目录被4个清单外保留worktree依赖，整项跳过。'
 if n in (26,28):reason='依赖第10项alternates对象库，删除该对象库后Git检查失败；对象库已恢复且读取PASS，本项保持跳过，不重试删除。'
 if n==36:reason='检查脚本对bare仓库acl.git运行stash list，命令不适用；已完成4/253仓库的保全，其余检查未完成。整目录保留，不做第二次sudo。'
 delta=gi(v['df_available_delta_bytes']) if 'df_available_delta_bytes' in v else '—'
 s.append(f"|{n}|`{r['path'].removeprefix(W)}`|{size}|{nrpm}|{v['status']} / {v.get('uid_for_rm','—')}|{delta}|{reason}|")
s+=['','34、35：保留编号，未检查、未删除任何路径。du为逐项扫描值，可存在硬链接重复计数；df差值是该时间窗口实际可用空间变化，包含并发系统写入，不能视为孤立文件大小。第10行是原删除窗口，尚未扣除随后恢复的对象库；全任务净值已包含恢复及备份新增占用。顶层列表、RPM名称/字节数/SHA256及普通用户权限错误在path-NN.json；root补查在execution-NN/complete-inventory.json。','', '## 3. 源码保护','', '逐仓库记录用户指定的`git log --branches --tags --not --remotes`，额外计入detached HEAD。部分临时克隆缺remote-tracking refs，原查询会把大量已发布LLVM历史也列出（部分克隆约27万条）。保留原输出gzip后，另通过BatchMode SSH只读查询Gerrit实际heads/tags，并只用本仓库确实存在的已发布对象做排除；没有fetch或改原仓库的ref/remote。查询原文见published-llvm-refs.stdout，逐仓库原始结果见git-inspection/。','', '发现未发布提交、stash或已跟踪改动时，保存完整format-patch、二进制staged/unstaged diff、stash（含untracked部分）及standalone bundle。bundle在新建空仓库中verify/unbundle，并逐个确认commit可读；补丁通过git apply --numstat解析。自测覆盖1个未发布提交、2份stash、同时存在暂存/未暂存改动。保全位置为W/temp/deleted-repo-backup-20261105/，每份有SHA256SUMS；这些保全和测试夹具保留。收尾du为98,026,516,480 B（91.294 GiB），包含完整bundle以及用于空仓库读回验证的对象副本；见backup-du.json。','', '|原目录编号|仓库|未发布提交|stash|tracked dirty|保全 / 判定|','|---:|---|---:|---:|---|---|']
for r in rr:
 f=E/f"execution-{r['number']:02d}/repositories.json"
 if not f.exists():continue
 for q in json.loads(f.read_text()):
  s.append(f"|{r['number']}|`{q['path']}`|{q.get('unpublished_commits',len(q['effective_unpublished']) if 'effective_unpublished' in q else '未判定')}|{q.get('stashes',0)}|{q.get('tracked_dirty',bool(q.get('status',{}).get('stdout')))}|{q.get('backup') or q.get('reason') or q.get('conclusion','')}|")
s+=['', '第20项内的Git公共目录仍服务于清单外、必须保留的worktree，因此整项跳过。具体依赖路径见该项repositories.json；未移动或修复任何worktree。无Git仓库的目录记录为空列表；检查/保全失败项不删除。','', '## 4. PGO profiles 与保留项','',f"`full/stage-A/profiles`同文件系统rename到`W/temp/pgo-profiles-keep-20261102/`。24文件共798,841,688 B；移动前、移动后、删除前以及最终SHA清单均保存，最终一致={post['profiles_unchanged']}。",'',f"第1–3项父目录其他条目逐项元数据一致={post['parents_unchanged']}；用户列出的12个保护目录身份一致={post['protected_unchanged']}；依赖主仓库的保留源码worktree可读={post.get('protected_source_repositories_readable')}；今晚完整构建未启动={post['night_not_started']}。完整路径/结果见protected-before/after.json、parents-before/after.json、protected-source-heads.json及postcheck.json。",'', '## 5. df、认证与结束记录','','删除前：','','```text',before['stdout'].rstrip(),'```','','最终：','','```text',after['stdout'].rstrip(),'```','']
for n in ['auth-attempts.log','root-invocation.json']:
 if (E/n).exists():s+=['`'+n+'`：','','```text',(E/n).read_text().rstrip(),'```','']
if (E/'execution.stdout').exists():s+=['最后的执行记录：','','```text','\n'.join((E/'execution.stdout').read_text().splitlines()[-8:]),'```','']
s+=['证据目录：[`tools/bolt/results/disk-cleanup-20261105b/`](../../tools/bolt/results/disk-cleanup-20261105b/)。未承诺可释放的du总量等于df增量：源码保全新增占用、共享硬链接及系统活动均会影响净值。','']
if (E/'alternates-restoration.json').exists():
 recovery=load('alternates-restoration.json');checks=load('alternates-restored-readcheck.json')
 s+=['## 6. alternates检查缺口与恢复记录','','本轮预检查识别了worktree依赖，但漏查Git objects/info/alternates的反向依赖。第10项删除后，第26和28项在Git查询中报unable to normalize alternate object path及fatal: bad object 2020.06-alpha，因此执行器跳过这两项。后续只读补查11条alternates，唯一缺失的对象库是第10项submit-work/.git/objects；第32项的review-work也直接依赖它。这个问题由本轮检查遗漏造成，不归因于用户或原仓库。','','从第10项已经在空仓库验证通过的standalone bundle读回副本中复制objects到新的暂存目录；逐文件核对SHA后，原子rename到原对象库路径。没有改依赖仓库配置，没有覆盖已有文件，没有第二次sudo，也没有额外删除。第10项的工作内容已删除，但对象库现已恢复，因此最终统计不把第10项算作整项删除。第26/28项保持跳过，不重试删除。','',f"恢复对象库：`{recovery['target']}`；{recovery['bytes']:,} B，{len(recovery['files'])}个文件，来源与恢复副本SHA全部相同。详见alternates-restoration.json及restore_alternates.py。",'', '|受影响仓库|恢复后原Git查询、HEAD tree及status|','|---|---|']
 for r in checks:s.append('|`'+r['repo']+'`|'+('PASS' if r['PASS'] else 'FAIL')+'|')
 s+=['','全部11条已知alternates路径恢复存在，六个明确保留源码仓库在发现问题时HEAD对象检查均通过。后续清理应先扫描完整的worktree及alternates依赖图，并在任何对象库删除之前完成所有消费者的保全；不能仅按目录顺序边保全边删除。原执行器日志和失败原文保留，未改写成成功。最终路径状态以postcheck.json为准。','']
s+=['## 7. 第36项的bare仓库检查中止','','第36项root补扫134处权限盲区成功，实际du=178,935,205,888 B，253个Git仓库、5,009个RPM。执行器完成前4个仓库的保全后，对第5个仓库`work3/four-package-work/inventory-git/acl.git`执行`git stash list`，返回128：','','```text','fatal: this operation must be run in a work tree','```','','这是检查器未区分bare仓库造成的失败，不证明该仓库损坏、存在stash或未发布改动。没有继续检查余下仓库，没有删除qb_analysis。下一次应对bare仓库直接检查refs/stash及其reflog，并将工作区改动检查记为不适用；本轮不绕过检查，不增加第二次sudo调用。已完成的4份保全及全部失败原文保留在execution-36/和deleted-repo-backup-20261105/。','','最终结果为部分完成：整项删除29项，第10项仅删除工作内容后恢复对象库，第20/26/28/36项保留；34/35无操作。没有启动night-launch-20261105。','']
(B/'docs/bolt/64_disk_cleanup.md').write_text('\n'.join(s))
print('report written',B/'docs/bolt/64_disk_cleanup.md')
