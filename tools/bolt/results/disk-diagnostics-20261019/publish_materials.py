from pathlib import Path
import json,shutil,subprocess,hashlib,difflib,ast,re,time
E=Path(__file__).resolve().parent;W=E.parents[1];B=W.parent/'llvm-optimize-bolt';S=W/'temp/bolt-v4-20261013/v41/llvm-source';D=B/'tools/bolt/results/disk-diagnostics-20261019';D.mkdir(parents=True,exist_ok=True)
release=json.loads((E/'release.json').read_text());new=release['commit'];base='e2463165829cc91b0a1d60a3e0f915a587865f70'
def git(*args):return subprocess.check_output(['git',*args],cwd=S)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert git('status','--porcelain')==b''
assert git('show','HEAD:packaging/clang-bolt-helper.py')==(B/'tools/bolt/bolt_helper.py').read_bytes()
assert git('diff','--name-only',base,new).decode().splitlines()==['packaging/clang-bolt-helper.py','packaging/llvm.spec']
raw=git('ls-remote','origin','refs/heads/sandbox/lhmax2025/bolt_pgo');(E/'remote-final.txt').write_bytes(raw);assert raw.decode().split()[0]==base
# Refresh host OFF comparison using the final source; production spec did not change since capture.
for label,p in [('base',E/'base-llvm.spec'),('new',S/'packaging/llvm.spec')]:
 for mode,extra in [('off',['--define','_without_clang_bolt 1']),('on',[])]:
  a=['rpmspec','-P','--target','x86_64-tizen-linux','--define','_toolchain clang']+extra+[str(p)]
  r=subprocess.run(a,capture_output=True);assert r.returncode==0
  (E/f'host-{label}-{mode}.expanded.spec').write_bytes(r.stdout);(E/f'host-{label}-{mode}.stderr').write_bytes(r.stderr)
def install(text):return text.split('%install\n',1)[1].split('\n%post',1)[0]
assert install((E/'host-base-off.expanded.spec').read_text())==install((E/'host-new-off.expanded.spec').read_text())
# Binary profile is separately published and unchanged; do not emit a 12MB base85 patch.
(B/'patches/bolt/0000-clang-bolt-squashed.patch').write_bytes(git('format-patch','--stdout','--no-binary','--no-signature','-1',new))
delta=git('diff','--binary',base,new);message=(E/'new-message.txt').read_text();header=f'From {new} Mon Sep 17 00:00:00 2001\nFrom: Hao Lin <hao.lin@samsung.com>\nSubject: [PATCH] packaging: diagnose disk failures without disk gates\nDelta-base: {base}\n\n{message}\n---\n'
patch=B/'patches/bolt/0006-disk-report-and-failure-diagnostics.patch';patch.write_bytes(header.encode()+delta)
# Delta patch independent apply: unchanged binary source is not involved.
A=E/'delta-apply';A.mkdir(exist_ok=True);(A/'packaging').mkdir(exist_ok=True)
for name in ['clang-bolt-helper.py','llvm.spec']:(A/'packaging'/name).write_bytes(git('show',base+':packaging/'+name))
a=['patch','-p1','--batch','--input',str(patch)];r=subprocess.run(a,cwd=A,capture_output=True);(E/'delta-apply.stdout').write_bytes(r.stdout);(E/'delta-apply.stderr').write_bytes(r.stderr);assert r.returncode==0
assert all((A/'packaging'/n).read_bytes()==(S/'packaging'/n).read_bytes() for n in ['clang-bolt-helper.py','llvm.spec'])
# New own evidence only; no export source tar, RPM payload, protected data or credentials.
for p in E.iterdir():
 if p.is_file() and p.suffix in ('.txt','.json','.diff','.py','.stdout','.stderr','.spec','.sh'):
  shutil.copyfile(p,D/p.name)
for n in ['injection','host-capture']:
 dest=D/n;dest.mkdir(exist_ok=True)
 for p in (E/n).iterdir():
  if p.is_file():shutil.copyfile(p,dest/p.name)
shutil.copyfile(E/'export/llvm.spec',D/'gbs-exported-llvm.spec')
shutil.copyfile(S/'packaging/llvm.spec',D/'llvm.spec');shutil.copyfile(S/'packaging/clang-bolt-helper.py',D/'clang-bolt-helper.py')
# The final suite has 258 retained/reworked tests plus 27 disk-observation/injection cases.
assert 'Ran 285 tests' in (E/'release-tests.stderr').read_text() and (E/'release-tests.stderr').read_text().rstrip().endswith('OK')
summary={'status':'LOCAL_VALIDATION_PASS_PUBLICATION_BLOCKED_BY_REQUIRED_PARSE_NOT_RUN','commit':new,'parent':release['parent'],'base':base,'fixtures':285,'baseline_fixtures':257,'new_non_disk_invariant':1,'new_disk_fixtures':27,'enospc_injection':'PASS','non_disk_error':'PASS original stderr preserved','diagnostic_exception':'PASS original rc1 preserved','known_size_formula':'PASS tool 12288 B, remaining peak 69632 B','disk_report_existing_and_missing':'PASS rc0','gbs_export':'PASS','host_rpm_4_18_2_supplemental':'PASS 5/5; not Tizen certification','tizen_rpm_4_14_1_1':'NOT RUN: one graphical authentication failed; no retry','real_tmpfs_full':'NOT RUN same reason','sandbox_pushed':False,'remote_final':base,'graphical_prompts':1,'root_wrapper_started':False,'protected_tree_mutated':False,'original_cmake_ninja_executed':False,'QB_logs_received':(W/'temp/qb-e2463165').exists(),'explicit_write_check_or_commit_integrity_fixes':25,'helper_writer_sites':61,'spec_checked_or_observability_lines':45,'delta_apply':'PASS byte-identical final helper/spec','files':release['files']}
(D/'validation-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
# Current manifest describes this unpushed draft; historical certification remains explicitly historical.
mp=B/'patches/bolt/draft-manifest.json';m=json.loads(mp.read_text());m.update(draft_commit=new,squashed_commit=new,tree=release['tree'],amended_from=base,files=[x for x in release['files'] if x['path']!='packaging/llvm-static-archives-native.py'],qualification='LOCAL_285_PASS_TIZEN_FIVE_PARSE_NOT_RUN_SINGLE_GRAPHICAL_AUTH_FAILURE',fixtures=285,sandbox_pushed=False,remote_before=base,remote_after=base,final_squashed_tests='285 PASS; Tizen 4.14.1.1 mandatory matrix NOT RUN; no sandbox push',material_pin=None,material_index_pin=None,disabled_macro_proof_reused=False)
m['patch'].update(sha256=sha(B/'patches/bolt/0000-clang-bolt-squashed.patch'));m['disk_diagnostics']=summary;m['disk_diagnostics']['evidence']='tools/bolt/results/disk-diagnostics-20261019';m['incremental_patch']={'file':patch.name,'base':base,'sha256':sha(patch),'delta_apply':'PASS'}
mp.write_text(json.dumps(m,indent=2)+'\n')
# Maintenance: production policy separated from local development operations.
p=B/'docs/bolt/maintenance.md';s=p.read_text();s=s.replace('TF归档SHA、磁盘/环境）失败均停止','TF归档SHA、环境）失败均停止；实际写入失败也停止，磁盘观测与诊断自身不作门禁')
s=s.replace('- disk-preflight 检查声明的写入上界、额外预留和写后剩余空间。单次计划写入 >10GiB，写后至少30GiB；<=10GiB，写后至少1GiB。16GiB默认BOLT阶段预算来自本地热缓存估计，不能当作冷缓存增长上限。必须把缓存增长和临时文件计入预算。','- 长期规则：发布代码不设磁盘空间门槛，只记录剩余空间；磁盘失败的诊断值必须在失败后由本次构建实际数据计算。profile、BOLT、clang 变化会改变用量，不能把旧预算当准入依据。disk-report 永远 rc0；disk-diagnose 只读 stdout，以本步骤 errno28/122 或四类日志文本判定，不以 free 大小判定。实际写入失败仍 rc1，原 clang 通过临时文件+SHA+最终 rename 保护。公式、降级与完整审计见27。\n- 长期规则：本地开发机的资源、锁、磁盘规则只约束本地操作，不得进入发布代码。本地单次 >10GiB 写入后保留 >=30GiB 仍适用，不能写入 helper/spec。')
s=s.replace('- ninja -j1 只限制Ninja同时调度的任务数，不限制链接器内部并行或内存。当前本地重阶段','- ninja -j1 只限制Ninja同时调度的任务数，不限制链接器内部并行或内存。以下仅约束本地开发操作：当前本地重阶段')
p.write_text(s)
# Source-message full diff + full release-source diff are public artifacts, not abbreviated stats.
writer=json.loads((E/'writer-audit.json').read_text());specwriters=json.loads((E/'spec-writer-audit.json').read_text());removed=json.loads((E/'removed-gates.json').read_text())
md=f'''# 27 磁盘门槛移除、实际用量观测和失败诊断（本地通过，发布暂停）

最终本地源 `{new}`；父 `{release['parent']}`；BASE/当前远端 `{base}`。署名均 Hao Lin <hao.lin@samsung.com>，Change-Id 保持。285 项本地测试 PASS；gbs export PASS。唯一一次图形密码认证失败，sudo 原文 `sudo: 1 incorrect password attempt`，包装器未启动；Tizen rpm 4.14.1.1 五项解析及可选真实 tmpfs 写满 NOT RUN，不重试、不换提权方式，故 **未推 sandbox**。主机 rpm 4.18.2 补充五项解析 PASS，不能替代构建根认证。没有 refs/for、QB、新分支或完整 LLVM 构建操作。

## 用户裁决、QB 原因及适用边界

1. 发布代码不设磁盘空间门槛：profile、BOLT、clang 变化会改变用量，固定门槛无法长期认证。
2. 确认磁盘失败后才按本次实际数据估算需求/缺口；不以 free 低判磁盘原因。
3. 长期规则：发布代码不设磁盘空间门槛，只记录剩余空间；磁盘失败的诊断值必须在失败后由本次构建实际数据计算。
4. 长期规则：本地开发机的资源、锁、磁盘规则只约束本地操作，不得进入发布代码。

用户交接 QB e2463165 在 %install 第5340秒：

```text
BOLT_GATE_FAILED: SKIP_DISK: write/reserve would leave -1765326848 bytes; require 32212254720 bytes (planned 17179869184)
```

W/temp/qb-e2463165/ 开工时不存在，收尾复核亦未收到日志，因此这是用户提供的原文，不能声称已用QB日志核实。未操作QB。

## 删除清单（行号均相对 BASE）

|文件/原行号|删除内容|
|---|---|
|spec:438、461|两处16GiB disk-preflight 调用及预算注释|
|helper:595|install_candidate 的安装预检|
|helper:656|rewrite 的四倍输入预算预检|
|helper:803|pipeline 的默认预算预检及 disk-admission.json|
|helper:847|cache_copy 的缓存大小+4GiB预留|
|helper:885|strip_all 的复制预检|
|helper:770–790、952–954、973|GIB/DISK_FLOOR/LARGE_WRITE/STAGE_WRITE_BUDGET、函数、CLI及分派；pipeline planned-write-bytes 参数|

完整逐项原文见 removed-gates.json。发布代码不包含本地 cgroup、共享锁、30GiB/10GiB底线；不改变候选重链、strip-debug、BOLT OPTIONS、strip-all 参数或 profile。

## 观测与诊断设计

`python3 -B helper disk-report STAGE` 在 begin（BOLT动作开始）、tool-built、pipeline、post 各一次。输出设备号、time_ns、free_bytes、明确的 owned_paths；同时原子保存 disk-baseline.json 与 disk-STAGE.json。**观测永远rc0**，包括目录尚不存在、空间零、记录写失败；唯一的持久写入非门禁例外。保存失败会注明 report_error，不能声称记录已落盘。

BOLT自有集合：build/clang-bolt/**、build/tools/bolt/**、build/lib64/libLLVMBOLT*.a、build/bin/llvm-bolt，及链接命令 ThinLTO 缓存相对begin快照的正向分配增量。通过lstat/st_blocks*512度量实际分配，同设备+inode去重硬链接；不跟随软链接。目录占用包括在内。缓存每个条目取 max(当前分配-基线分配,0)，新条目取当前分配；LLD清理旧条目不会抵消新增长。额外记录净变化，仅供核对。普通缓存原有内容不算BOLT新增。

`python3 -B helper disk-diagnose STEP LOG` 只读、不写任何文件，包括无pyc；优先本步骤Python OSError errno28/122，另处理 copytree 保留的本步骤结构化文件错误列表。日志匹配表（re.I）：

|匹配|含义|
|---|---|
|No space left on device|写满原文|
|Disk quota exceeded|配额原文|
|\\bENOSPC\\b|错误名|
|\\bEDQUOT\\b|配额错误名|

不读取无关步骤日志，不用低剩余空间判定。not-disk 只一行 cause/step/free_bytes，不预测。disk 输出固定 BOLT_DISK_DIAGNOSIS JSON 段，注明“估计值，依据本次构建实际文件大小”。报告/诊断错误不替代原失败，helper与spec原始stderr保留并exit1。损坏记录降级为当前free与实际自有占用，明确标degraded，禁止填造固定需求。未知数据也明确列unknown_components/incomplete_estimate；EDQUOT的真实配额余量不可由statvfs推断，单独标注。

spec 每步由 bolt_checked/bolt_step/bolt_capture 捕获同一步的原始输出；regular日志写满时输出仍在内存，失败后把它交给disk-diagnose /dev/stdin，随后exit1。平台post是原链在一个shell heredoc内执行一次，由checked runner监督；尾检和最后观测顺序保留。原%sinstall的关闭开关路径不加wrapper，主机展开字节相同比较PASS；构建根验证未运行。

## 失败后公式与边界

以失败文件系统为范围；used_bytes 为当前实际分配及已观测缓存正向增量；estimated_remaining_bytes 为剩余保留产物增长加各阶段临时副本的最大同时占用；estimated_total_bytes=used_bytes+estimated_remaining_bytes；shortfall_bytes=max(estimated_remaining_bytes-free_bytes,0)。不同设备分开记录，当前缺口只比较失败设备。

- 工具：ceil(已完成任务实际输出文件总字节 / 已完成任务数 × 剩余任务数)，再扣已有未完成输出分配。任务来自本次tool-plan与真实日志；FAILED的上一任务不算完成。零完成任务或无法量出产物时注明未知，不能除零或套默认预算。
- 重链：max(本次ordinary clang实际大小, 已观测重链部分大小)-已存在分配。
- strip-debug：重链完成大小（未完成时用上项实际数据估计）作为临时副本峰值。
- BOLT：max(本次输入大小, 已观测BOLT部分大小)-已存在分配；完成后用实测完整大小。
- strip-all：本次BOLT输出/候选实际大小推算候选副本和strip临时峰值；不是固定倍数预算。保存与临时副本按顺序计算峰值，不把不同时存在的临时文件相加。
- profile未解包：只读流式解压本次压缩Source并计数，不写新文件。
- cache-copy（R1类可选能力）：本次源文件实测大小减目标已分配；新树仍原地缓存，不复制。
- ThinLTO：实测正向增长已经计入used一次，不再重复叠加；未来未观测的增长不可从旧预算得知，明确标为未知。故不完整估计是可观测下界，**不承诺预测全部未来缓存增长**。
- 写失败的原子JSON/文本：异常附本次UTF-8序列化真实字节数；临时文件删除后把该值计入仍需写入部分。

已知大小夹具（B）：ordinary16384；完成工具输出4096+8192、完成2/剩余2，预测12288；未完成工具已分配4096，新增8192；重链已有4096，新增12288；后续重写16384、候选16384保留，加最大临时16384，剩余峰值=8192+12288+16384+16384+16384=69632，实测算法69632。详情 FORMULA_FIXTURE 原文见release-tests.stdout。注入测试free4096为mock值，非宿主真剩余；install注入used81920、总151552、短缺65536。

## 写满必停审计与25处加固

25处为“缺少显式立即错误检查、写出完整性或最终提交顺序”的加固计数，**不表示旧版25处都会静默成功**（RPM -e、后续门禁可能已有保护）：普通CMake安装1处；后续17个ln/mkdir/mv/cp/rm命令17处；clang.cfg heredoc1处；成功标记追加1处；子进程日志写入1处；临时clang SHA核对1处；install-state前移1处；别名写入前移1处；JSON/文本原子写长度及fsync1处。合计25。原转换器已有exit1，这次只补同一步诊断，不重复计数。profile失败清理不遮蔽原错另作健壮性修正。

安装顺序：审计ELF/身份/别名 → 同目录临时复制 → chmod、fsync、大小+SHA → 准备别名 → 原子保存state并发布结果 → 改名别名（此时仍解析为普通clang） → **最后一次可失败文件操作为clang实体os.replace**。部分复制、JSON失败、别名失败和最终rename失败均保留原clang SHA。若后续平台post失败，构建仍失败；完整安装候选也不会因此成为成功RPM，不能把“原子安装”理解成绕过post门禁。

以下行号针对最终源提交。所有save及原子写经异常传播rc1，call父进程拥有日志写入并监测短写/flush/fsync，写错则kill/reap整个组；清理unlink错误只保留原失败。纯观测save为用户要求的明确例外。源中字符串replace不属于文件写入，未算入表。

### helper写入点、子进程与JSON结果保存

|行|函数|写入/调用原文|失败处置|
|---|---|---|---|
'''
for row in writer:
 src=row['source'].replace('\n',' ').replace('|','&#124;');md+=f"|{row['line']}|{row['function']}|`{src}`|{row['handling']}|\n"
md+='\n### spec中受检查的写入及四次观测\n\n|行|原文|失败处置|\n|---|---|---|\n'
for row in specwriters:md+=f"|{row['line']}|`{row['source'].replace('|','&#124;')}`|{row['handling']}|\n"
md+='''
## 全部测试与准备过程

|验证|结果|原始证据|
|---|---|---|
|既有基线257测试（TMPDIR在E/tmp）|257 PASS|baseline-home-tests.stdout/stderr|
|保留/按新语义替换既有测试，加非磁盘AST不变约束|258 PASS|legacy-updated-tests.stdout/stderr|
|最终全部本地测试|285 PASS，15.035秒|release-tests.stdout/stderr|
|复制/JSON/子进程命令/子进程日志/四类install ENOSPC|各真实CLI退出1，cause=disk，字段齐全；原clang不变|injection/* 原文与argv/rc|
|普通门禁非磁盘失败|rc1、cause=not-disk、原始错误不变|injection/not-disk.*|
|诊断自身异常（磁盘与非磁盘）|仍原始rc1及原始错误|injection/*diagnostic-exception.*|
|损坏baseline记录|只报当前free/used、degraded，不抛异常|injection/corrupt-records.*|
|精确已知大小公式|12288及69632符合期望|release-tests.stdout FORMULA_FIXTURE|
|disk-report正常/不存在目录、free=0、观测保存异常|全部rc0|test_disk_diagnostics.py、release-tests.*|
|真实copytree包装异常结构识别|PASS新增1项|CopytreeEvidenceTests|
|发布参数/匹配/ELF/安全/tiny/plan/verify等AST保持|PASS|test_non_disk_gates_unchanged|
|最终spec脚本只捕获、/bin/sh -n|PASS，四次report，无产品命令执行|host-capture/*|
|gbs export最终提交|PASS 7个Patch均声明，49.384秒|gbs-export.json/stdout/stderr；gbs-exported-llvm.spec|
|主机rpm4.18.2补充五项展开|5 PASS，仅补充|host-final-matrix.json及5对原文|
|Tizen rpm4.14.1.1必须五项解析|NOT RUN，唯一图形认证失败|sudo.stderr、privileged-validation.json|
|可选真实tmpfs写满|NOT RUN，同上|privileged-validation.json|
|sandbox推送|NOT RUN，缺必须认证|remote-final.txt仍e2463165|

已有13项“门槛拒绝”相关断言按本轮语义调整：CacheTests两项、DiskTests八项、PipelineTests一项、FourthPrereqTests两项，数量保留。历史“只改文件头AST不变”用例改为比较已保存历史两份helper，避免错误地冻结未来实现；新增当前非磁盘门禁AST逐项不变检查。新磁盘模块27项；总285。没有删掉非磁盘负例门禁。测试stdout含真实故障输出及FORMULA_FIXTURE，并非只有测试汇总；stderr含逐项unittest原文。

准备记录：首次既有测试沿用/tmp导致两个旧预算门禁报错（原始baseline-tests.*保留）；设置TMPDIR=E/tmp后257 PASS。新增故障夹具最初把edge文本而非文件路径传入cache-copy，修正为已保存link.original；子进程心跳/输出夹具用flush=True确保立即触发日志失败。disk-tests.*、disk-tests-fixed.*及随后完整PASS原文均保留，不掩盖早期夹具失败。读文件定位误用了过宽的上级find，遇到无关保护根Permission denied后立即中止，未修改任何树；后改为只查明确父目录AGENTS，不再递归该区域。临时目录/输入均位于本会话E，受保护树未写入。

图形认证只实际弹一次。sudo第一次失败后single-use askpass拒绝后续请求，因此第二次调用仅mkdir报已存在，没有第二个图形框；未切换sudo -n或其他提权。原文另含zenity输入法Gtk warning，不能把它误写为产品失败。root-entry.json不存在，无锁/挂载/根内命令，无需伪造下层前后快照。

## 完整diff、提交说明及发布状态

[完整源码diff（e2463165→新提交）](../../tools/bolt/results/disk-diagnostics-20261019/source.diff)，仅helper与spec；[完整增量补丁](../../patches/bolt/0006-disk-report-and-failure-diagnostics.patch)，独立patch -p1后两文件逐字节等于新提交；[完整压缩文本版0000](../../patches/bolt/0000-clang-bolt-squashed.patch)；profile单独交付且SHA不变。完整源码diff不是从父676计算的旧BOLT全量，增量基点明确e2463165。完整cat-file见new-commit.txt，spec/helper完整文件一并保存。

提交说明只新增磁盘段及替换Still open中的首次install措辞；标题不变42字符、每行≤72，Signed-off-by/Change-Id保持。全文差异：

```diff
'''+(E/'message.diff').read_text()+'''```

原候选4ec07159及profile未重生成。原树未运行cmake/ninja/-P，未对ARM树执行构建、安装或写入操作；没有新的产品二进制验证或Quickbuild执行。源码最终本地提交已保留，材料在bolt-v4发布供复核，**不能把未推的草案写成远端交付**。后续仍须获可用单次图形授权完成Tizen五项，然后按当时远端SHA复核精确租约；本轮不重试。单次认证失败是当前唯一发布阻塞，非产品门禁FAIL。
'''
md=md.replace('原%sinstall','原%install')
(B/'docs/bolt/27_disk_diagnostics.md').write_text(md)
status=B/'docs/bolt/STATUS.md';s=status.read_text().split('\n\n## 2026-10-19：去掉磁盘门槛，诊断与原子安装；发布暂停')[0];s+=f'''\n\n## 2026-10-19：去掉磁盘门槛，诊断与原子安装；发布暂停\n\n长期规则：发布代码不设磁盘空间门槛，只记录剩余空间；磁盘失败的诊断值必须在失败后由本次构建实际数据计算。本地开发机的资源、锁、磁盘规则只约束本地操作，不得进入发布代码。\n\n本地源 `{new}`（父67619ec8，Hao Lin/原Change-Id），BASE与远端仍e2463165。删除spec两处及helper五处磁盘准入、预算常量与CLI；四阶段disk-report永远rc0，disk-diagnose只读按本步骤errno/原文判磁盘，实际大小推算并明确未知/降级。25处显式检查或提交顺序加固，临时clang经SHA核对再最终rename。285测试PASS：ENOSPC、非磁盘、诊断自身异常、原clang保持、公式及非磁盘AST均覆盖。gbs export PASS；主机rpm4.18.2补充5/5 PASS，**不等于Tizen认证**。唯一图形密码认证失败，不重试；包装器未启动，Tizen4.14.1.1五项与真实tmpfs NOT RUN，因此sandbox未推。QB日志未收到；未操作QB/refs-for/新分支/保护树。完整审计、diff、原始失败与最终测试见[27](27_disk_diagnostics.md)，当前manifest明确sandbox_pushed=false。\n'''
status.write_text(s)
print(json.dumps({'commit':new,'evidence_files':len(list(D.rglob('*'))),'report_bytes':len(md.encode()),'status_bytes':status.stat().st_size,'source_delta_paths':git('diff','--name-only',base,new).decode().splitlines()},indent=2))
