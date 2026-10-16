from pathlib import Path
import json,subprocess,shutil,hashlib,re,lzma
E=Path(__file__).resolve().parent;W=E.parents[1];B=W.parent/'llvm-optimize-bolt';D=B/'tools/bolt/results/source-order-20261016';S=W/'temp/bolt-v4-20261013/v41/llvm-source'
R=E/'attempt-prep-count';r=json.loads((E/'certification-result.json').read_text());source=json.loads((E/'source-result.json').read_text());new=source['new']
assert r['status']=='PASS_REQUIRED' and len(r['matrix'])==10 and all(x['PASS'] for x in r['matrix'])
assert r['lower_unchanged'] and not r['unmount_errors'] and r['lock_held_seconds']<3600
assert r['prep'][0]['status']=='PASS' and r['prep'][1]['status']=='NOT RUN'
assert subprocess.check_output(['git','-C',str(S),'rev-parse','HEAD'],text=True).strip()==new
assert not subprocess.check_output(['git','-C',str(S),'status','--porcelain'])
# Copy raw files only: export trees, root-owned overlay upper/work and fixture payload are retained locally.
for folder in [E]+[E/n for n in ['attempt-version-display','attempt-rpmspec-without','attempt-prep-count']]:
 target=D if folder==E else D/folder.name;target.mkdir(exist_ok=True)
 for p in folder.iterdir():
  if p.is_file() and p.suffix not in ['.pyc']:
   assert p.stat().st_size<10000000,(str(p),p.stat().st_size)
   shutil.copy2(p,target/p.name)
# Persist equivalent bcond rollback specs used inside each overlay.
for label in ['before','after']:
 text=(E/('export-'+label)/'llvm.spec').read_text()
 (D/('export-'+label+'-rollback.spec')).write_text(text.replace('%bcond_without clang_bolt','%bcond_with clang_bolt',1))
checks=[]
for case in ['x86-default','x86-without','x86-rollback','armv7l','aarch64']:
 a=next(x for x in r['matrix'] if x['name']=='before-'+case);b=next(x for x in r['matrix'] if x['name']=='after-'+case)
 checks.append({'case':case,'old_rc':a['rc'],'old_stderr':(R/(a['name']+'.stderr')).read_text(),'new_rc':b['rc'],'new_stderr':(R/(b['name']+'.stderr')).read_text(),'new_sources':[x for x in b['source_patch_list'] if x.startswith('Source')],'new_patches':[x for x in b['source_patch_list'] if x.startswith('Patch')],'PASS':a['PASS'] and b['PASS']})
summary={'status':'PASS_REQUIRED','source_commit':new,'parent':source['parent'],'cases':checks,'prep':[{'name':x['name'],'rc':x['rc'],'seconds':x['seconds'],'patches':x['applied_patch_numbers'],'status':x['status']} for x in r['prep']],'package_rpm':'4.14.1.1-1.4','cli_rpm':'4.14.1','host_rpm_not_used_for_certification':'4.18.2','lower_unchanged':r['lower_unchanged'],'sandbox_updated':False,'QB_logs_received':(W/'temp/qb-506dc25').exists()}
(E/'verification-summary.json').write_text(json.dumps(summary,indent=2)+'\n');shutil.copy2(E/'verification-summary.json',D/'verification-summary.json')
p=B/'patches/bolt/draft-manifest.json';m=json.loads(p.read_text());m['qualification']='PASS_GBS_EXPORT_AND_ALL_10_TIZEN_RPM_PARSE_CHECKS_ARM_PREP_PASS_AARCH64_PREP_NOT_RUN';m['source_order_fix'].update(parse_matrix='PASS 10/10: old expected 1 PASS + 4 No patch number 0, new 5 PASS',rpm_package='4.14.1.1-1.4',optional_prep='armv7l PASS seven patches; aarch64 NOT RUN additional GUI authentication unanswered',spec_only_delta_applies=True)
m['final_squashed_tests']='Spec source-order regression: 10/10 expected results + armv7l prep PASS, aarch64 prep NOT RUN on '+new+'; helper unchanged, historical 257 fixtures retained on 506dc25 (not rerun)';m['post_capture']='Historical final 506dc25 evidence reused; post/build/install bytes unchanged by Source-only fix';m['disabled_macro_proof_reused']=True;m['source_order_fix']['commit_message_other_bytes_equal']=True
p.write_text(json.dumps(m,indent=2)+'\n')
p=B/'docs/bolt/26_source_order_parse_fix.md';text=p.read_text();text=text.replace('进行中：新导出与两份五项 Tizen RPM 解析；尚未更新 sandbox。','''新导出 PASS：Patch0–Patch6 位于第59–65行，第一条后续条件在第67行，所有 Patch 声明和七条 patch 命令均在全部条件块之外。七个生成补丁和源码/profile/helper/转换器载荷前后 SHA 相同（export-identities.json）；另一个 libcxx-runtimes.spec 仅由 gbs 更新自身 VCS tag，不属于仓库源码 diff。

实际认证使用 x86 构建根中的 rpm/rpm-build **4.14.1.1-1.4**；CLI 自报 RPM version 4.14.1。没有使用宿主4.18.2替代。该 x86 rpm 支持两个 ARM target，不需要 ARM 根。

Tizen rpmspec 不支持 --without，主解析命令采用 **rpmbuild -bp --nodeps --nobuild**，第二项逐字使用 --without clang_bolt；不会执行 prep。另用同版本 rpmspec -P 保存展开及 Source/Patch 清单，第二项仅在该辅助清单命令中用等价 _without_clang_bolt 宏。所有完整 argv、rc、stdout/stderr 均存证。

| 模式 | 506dc25 退出码/结果 | 新提交退出码/结果 | 新版 Patch |
| --- | --- | --- | --- |
| x86_64 默认开启 | 0，PASS | 0，PASS | 0–6全部 |
| x86_64 --without clang_bolt | 1，No patch number 0 | 0，PASS | 0–6全部 |
| x86_64 单行 bcond_with 回退 | 1，No patch number 0 | 0，PASS | 0–6全部 |
| armv7l-tizen-linux | 1，No patch number 0 | 0，PASS | 0–6全部 |
| aarch64-tizen-linux | 1，No patch number 0 | 0，PASS | 0–6全部 |

旧版四项原文均为：

```text
error: No patch number 0
```

新版五项 Source 清单均包含 Source0、1001–1005、1200–1201，Patch 文件名与用户指定系列一致；逐项清单见 verification-summary.json 与全部 *-expanded.stdout。关闭/ARM的 BOLT 实际执行条件没有改动。
''')
text+='\n## 可选 prep、资源与保护\n\n'
for row in r['prep']:
 if row['status']=='PASS':text+=f"- {row['name']}：退出码{row['rc']}，{row['seconds']:.3f}秒，stdout 逐行确认 Patch #0..#6 各一次。\n"
 else:text+=f"- {row['name']}：NOT RUN，额外图形认证未完成，代理结束多余密码框，未开始该目标的 prep；没有改用其他提权。\n"
cg=json.loads((R/'final-cgroup.json').read_text());before=json.loads((R/'lower-before-snapshot.json').read_text())
text+=f'''\n已执行的 ARM prep 合计 {sum(x['seconds'] for x in r['prep']):.3f}秒，低于20分钟；只解包/打补丁/展开既有 MLGO 资产，没有构建。所有改写在新 overlay 的专用 /home/abuild/bolt26 下。最终包装持锁 {r['lock_held_seconds']:.3f}秒，4GiB/swap0/nice19/ionice3，cgroup memory.peak={cg.get('memory.peak','unknown').strip()}B，memory.events 原文见 final-cgroup.json。磁盘准入计20GiB预算后仍≥30GiB，结束可用 {r['disk_free_after']}B。

最终下层 BUILD {before['paths']:,}路径的类型/大小/mtime/链接目标与六个关键 SHA 全部不变，manifest SHA {before['manifest_sha256']}；所有 overlay、proc、dev 已卸载，项目锁与共享锁释放。既有原树没有运行 cmake/ninja/-P。旧尝试的上层和本次上层仅保留本地，没有动此前25号演练上层。

## 完整源码 diff（506dc25 → 新提交）

```diff
{(E/'source.diff').read_text().rstrip()}
```

## 完整提交说明 diff

```diff
{(E/'commit-message.diff').read_text().rstrip()}
```

## 准备性错误完整记录

以下各类均只修正一次，没有放宽有效产品判据。全部原始异常/旧脚本/原始日志保留，通用包装器中的 PRODUCT GATE 标签对下列两种证据/参数错误并不准确，不能据此称产品失败。

'''
for row in json.loads((E/'preparation-corrections.json').read_text()):text+=f"- {row['class']}：{row['cause']}；修正：{row['correction']}\n"
text+='''
权限过程：版本展示断言与不支持的 CLI 参数使早期包装器在有效产品验证前清理退出；另一次重复 askpass 被一次性标记拒绝，未提权。纠正准备错误后重新运行完整图形 sudo -A 包装器，因不同调用未复用认证而再次显示密码框，未使用 sudo -n、终端密码或其他提权。有效认证包装器完成挂载→十项解析→ARM prep→卸载。后续用于补跑的额外密码框未获输入，由代理结束，AArch64 可选 prep 不再请求权限，记 NOT RUN；这不影响已完成的两目标解析认证。早期 ARM prep 已成功，但证据计数器同时扫描 stdout 和 shell 回显导致重复；改为 stdout 行首匹配后对保留原文重审，确认 rc0 与七个补丁均通过；没有重写日志或伪造新 prep。须承认这比要求的一次图形输入多，原始记录完整保留。

## sandbox 与 raw

认证材料先推 GitHub，待本报告后续发布记录补入指定租约的远端前后核对。QB 仍由用户控制，本任务没有操作 QB 或 refs/for/tizen_base，没有新建分支。
'''
p.write_text(text)
p=B/'docs/bolt/STATUS.md';text=p.read_text().replace('## 2026-10-16：QB Source 条件屏蔽 Patch 修复（进行中）','## 2026-10-16：QB Source 条件屏蔽 Patch 修复（本地认证 PASS，待推 sandbox）');text=text.replace('两份五项 rpm 认证与 sandbox 更新待完成。','两份五项 Tizen rpm 认证全部符合预期（旧1过4失败，新5过），ARM实际 prep 0退出/七补丁全部应用，AArch64可选prep因额外认证未完成记NOT RUN，helper/profile均不变；sandbox 更新待完成。');p.write_text(text)
for p in [B/'docs/bolt/STATUS.md',B/'docs/bolt/26_source_order_parse_fix.md']:assert p.stat().st_size<50000
print(json.dumps(summary,ensure_ascii=False,indent=2))
