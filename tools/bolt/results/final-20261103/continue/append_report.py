from pathlib import Path
import json,hashlib,datetime,subprocess,shutil
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=W/'temp/final-20261103';E=D/'continue-20261103'
t=json.loads((E/'toolchain-rehearsal-audit.json').read_text());d=json.loads((E/'basedev-rehearsal-audit.json').read_text())
assert t['PASS'] and d['PASS']
assert not (D/'toolchain').exists() and not (D/'basedev').exists()
free=shutil.disk_usage('/home').free;budget=json.loads((E/'disk-budget.json').read_text());budget['after_rehearsals_available_bytes']=free
rows=json.loads((E/'outside-root-overhead.json').read_text());totals={}
for row in rows:
 assert row['rc']==0
 totals[row['rehearsal']]=totals.get(row['rehearsal'],0)+row['bytes']
budget['outside_root_observed_bytes']=totals
budget['per_full_root_outside_allowance_bytes']=max(totals.values())
budget['final_required_bytes']=budget['two_roots_bytes']+2*max(totals.values())+budget['reserve_bytes']
budget['after_rehearsals_PASS']=free>=budget['final_required_bytes']
budget['initial_extra_20_percent_target_still_met']=free>=budget['required_bytes']
budget['extra_space_after_final_estimate_bytes']=free-budget['final_required_bytes']
budget['timestamp']=datetime.datetime.now().astimezone().isoformat()
(E/'disk-budget-final.json').write_text(json.dumps(budget,indent=2)+'\n')
assert budget['after_rehearsals_PASS'],budget
inv=json.loads((E/'test-invocation.json').read_text())
base='../../tools/bolt/results/final-20261103/continue/'
s='''\n\n## 7. 轻量检查与演练（续）\n\n本次恢复后，378 项 helper 测试、35 项转换器/新增夹具、双配置展开、五项 Tizen RPM 解析和两套入口的最终演练均通过。共三次演练（D重试一次），均在 CMake 入口停止，没有执行 LLVM Ninja，没有运行完整构建。今晚入口已准备；以下结果不代表 23 包、身份链或 90 TU 已通过。\n\n### 7.1 身份、测试环境与夹具\n\n源码仍为 `a379c766e17d12ba7738ff6079adb39645c0a740`，tree `37c8c6d3f249b5948db1517d84a79a4d53c9a112`；父 `5aff6c0c`、祖父 `38477c9b` 均未改，工作区干净。本轮没有修改发布代码或 amend 提交。前文及上一轮失败证据原样保留。\n\n沿用 48 号 §13 的 `W/temp/review-20261103/host-tools/cmake`：该入口以新配置根的 loader、库目录运行其 CMake，测试驱动在本轮目录执行，fixture 使用宿主临时目录；没有进入历史根运行 CMake/Ninja。完整 PATH、入口/实际 ELF/loader 的 SHA 和 argv 见 [test-invocation.json](BASEtest-invocation.json)。版本原文：\n\n```text\nVERSION```\n\n| 检查 | 结果 | 原文证据 |\n|---|---|---|\n| 显式 helper 的既有测试 | 378/378 PASS，`Ran 378 tests` / `OK` | [stderr](BASEhelper-tests.stderr)、[stdout](BASEhelper-tests.stdout) |\n| 转换器既有测试 | 24/24 PASS | [fixtures.stderr](BASEfixtures.stderr) |\n| 新参数与 release 夹具 | 11/11 PASS；合计35项 `OK` | [测试脚本](BASEtest_continuation.py)、[逐输入输出](BASEflags-observed.json) |\n\n转换器通过 importlib 显式导入源码提交中的 `packaging/llvm-static-archives-native.py`，注入既有测试使用的模块名；没有导入工具目录里的旧实现。路径和 SHA 原文在 [fixtures.stdout](BASEfixtures.stdout)。\n\n新增覆盖：Toolchain CFLAGS/CXXFLAGS/LDFLAGS 与 A-X:L427/L429及L395精确字符串相等；Base-Dev 固定输出、架构、NORMALIZED/DROPPED；strong 完整 token；空输入；重复 token；混合空格/tab/换行。重复架构项按原顺序保留、固定项只按固定列表输出，审计列表保留重复输入。release 无 DWARF 通过、带 -g 时保留原 DWARF 规则、未知 token 拒绝、真实 QB 参数负例拒绝、转换路径中产生含 `.debug_info` ELF 时拒绝。\n\nQB 1214821 日志保留的是原始/生效 CFLAGS，不是完整逐对象 Ninja 命令；负例将日志里的生效 CFLAGS 原文接到 `clang` 后送入分类器，命中 `-feliminate-unused-debug-types` 拒绝。未把重建的 argv 冒充日志中完整命令。[输入来源及行号](../..//tools/bolt/results/final-20261103/flags-inputs.json)。\n\n### 7.2 导出、完整展开与解析\n\nGBS export 退出0，[命令/返回码](BASEexport.json)、[stdout](BASEexport.stdout)、[导出spec](BASEexported.spec)、[文件大小与SHA](BASEexport-inventory.json)。\n\n使用 Tizen RPM/RPM-build `4.14.1.1-1.7`，通过同一配置根的 loader 和库从宿主临时目录只读调用；没有依赖宿主 RPM 版本。`RPM_CONFIGDIR` 指向 Tizen 目录；去掉宿主/用户宏文件来源，再用 `/usr/lib/build/queryconfig` 从两份固定 build.conf 生成各架构 rawmacros 和 optflags/rpmrc。每次命令、rc、stdout/stderr 均在 [parse](BASEparse/) 中保存。debug/release 用显式 `_toolchain` 定义/取消选择，只用于本轮模式矩阵；真实 D 演练不增加 `_toolchain`。\n\n- Toolchain build.conf：`e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945`。\n- Base-Dev build.conf：`8ace286a5f98f2e02a79be275a64c22a86ea2b0034174c1e293381e181ce3f6a`。\n\n| 配置 | x86 debug / release | armv7l / aarch64 | BOLT OFF |\n|---|---|---|---|\n| Toolchain | PASS，唯一diff为参数块 | PASS，与5aff逐字节相同 | PASS，仅参数块变化 |\n| Base-Dev | PASS，唯一diff为参数块 | PASS，与5aff逐字节相同 | PASS，仅参数块变化 |\n\n[12组逐字节/限定区间比较](BASEparse/expansion-summary.json)，原始全文未去空行。x86每份diff均为“旧sed规范化块→新完整token参数函数、固定参数、NORMALIZED/DROPPED输出”；检查脚本同时断言该块前后**所有字节**相同。48 §15 的 `bc0d58ff` 与5aff的spec blob都是 `7a51be894f830043acbf25e4d822fa1af51d4a06`，因此既有Source/空行/hybrid差异不变，[衔接证据](BASEoff-section15-baseline.json)。\n\n导出spec的 x86 ON、OFF、一行回退、armv7l、aarch64 五项，`rpmbuild -bp --nodeps --nobuild` 与 `rpmspec -P` 均退出0，各含8个生成补丁声明：[five-summary.json](BASEparse/five-summary.json)。这五项命令只做解析/校验，不执行%prep；后续另行执行的启动演练见7.3。\n\n准备性处理：初版比较脚本把旧参数块起点错误定位到中间的 `export CFLAGS`，在执行展开前触发边界 AssertionError。保留 [初版脚本](BASEparse_checks.attempt1.py) 和 [错误原文](BASEparse.attempt1.stderr)，改为完整 `%ifarch x86_64` 块边界后通过；没有放宽比较。一次只读查找误用不存在的48号文档文件名，随后 `rg --files docs/bolt` 定位为 `48_review_fixes.md`；不影响产品操作。\n\n### 7.3 两个真实启动演练\n\n[入口](../../tools/bolt/final-launch-20261103/launch.sh) 和 [控制器](../../tools/bolt/final-launch-20261103/launcher.py) 复制自dca920a8布局，[完整差异](BASElauncher-final.diff)。沿用physical gbs-root + gbs-driver的BUILD-ROOTS链接、先prep后正常GBS流程。仅本地选择source/config/root/service；D不套用T的固定profile/strip身份监视，发布helper门禁和BOLT失败/磁盘停止监视不变。固定profile键名保留以兼容driver sources目录；实际来源由URL和build.conf决定，不因此把Base-Dev当成Toolchain。\n\n- T：`W/temp/final-20261103/toolchain-rehearsal`，快照 `tizen-base-toolchain_20261013.024319`。\n- D：`W/temp/final-20261103/basedev-rehearsal/retry-02`（首轮保留），快照 `tizen-base-dev_20261030.061217`。\n- 两者都只启用各自 packages/debug，完整配置副本在 [configs](BASEconfigs/)。\n- MemoryMax=24,482,979,840B（本机MemTotal−8GiB），MemorySwapMax=0，CPUQuota=1200%，nice10，ionice2/7。GBS `--threads=30`，三个宏为jobs8、_smp_mflags=-j8、_costomized_smp_mflags=-j20；spec的LLVM编译并行6、链接2不改。\n- T首轮通过；D首轮到达CMake并正常停止，但增量日志漏掉%build开始行，使控制器断言失败。修复本地采集器后在全新retry-02重做并通过；没有执行Ninja。平台日志里的 `Terminated`/`failed build` 是主动停止的预期结果，控制器最终按停止原因和清理事实判定PASS，不把它当作完整构建成功。\n\n'''.replace('BASE',base).replace('VERSION',inv['cmake_version'])
for project,row in [('Toolchain',t),('Base-Dev',d)]:
 slug=row['project']; evidence_slug=slug+('/retry-02' if 'retry-02' in row['root'] else '');s+='#### '+project+' 原文与参数\n\n'
 s+='日志 `rehearsals/'+evidence_slug+'/evidence/'+Path(row['logfile']).name+'`：\n\n```text\n'
 for key in ['TIZEN_LLVM_NORMALIZED_FLAGS','TIZEN_LLVM_DROPPED_FLAGS']:s+='L'+str(row[key]['line'])+': '+row[key]['text']+'\n'
 s+='```\n\nCMake命令在L'+str(row['cmake']['line'])+'，参数逐字保存如下（C与C++分别比较，并非只比较token集合）：\n\n```text\n'
 for k,v in row['cmake']['flags'].items():s+=k+'='+v+'\n'
 s+='LDFLAGS='+row['LDFLAGS']['value']+'\n```\n\n'
 s+='LDFLAGS来自CMake执行前导出的环境，不虚构为一个`-D`参数。完整CMake argv、原文行和精确比较：[审计JSON]('+base+slug+'-rehearsal-audit.json)。\n\n'
 s+='清理原文：[final-audit.json]('+base+'rehearsals/'+evidence_slug+'/evidence/final-audit.json)：`ActiveState=inactive`、`SubState=dead`，mounts stdout为空，`remaining_build_processes=[]`；普通umount命令与返回码单独保存。控制器结束行：\n\n```text\n'+(Path(row['root'])/'controller.stdout').read_text().strip()+'\n```\n\n'
s+='''#### Base-Dev首轮采集失败与修复

GBS重写同一个`.build.log`后，旧增量采集器仍沿用prep时的偏移；原始文件有`Executing(%prep)`和`Executing(%build)`，拼接副本却缺少后者。第一轮控制器原文：

```text
assert 'Executing(%prep)' in log and 'Executing(%build)' in log
AssertionError
FINAL_PROJECT_FLAGS 已结束 2026-11-03T12:16:48.289526+08:00 status=failed reason=unexpected-controller-error
```

[原始根日志副本](BASEbasedev-attempt1-authoritative-build.log)、[失败控制器栈](BASErehearsals/basedev/evidence/failure.txt)、[首次清理](BASErehearsals/basedev/evidence/final-audit.json)保留；这不是发布门禁失败，也没有补写原来的FAIL为PASS。

仅改本地日志采集：核对上次读取尾部128字节来检测截断/重写，记录重置事件；停止后另存完整`rpm-build-final.log`，控制器验证这份权威副本。新增模拟“截断后增长超过旧偏移”的夹具通过；[修复diff](BASElauncher-logging-fix.diff)、[夹具](BASEtest_log_restart.py)、[结果](BASElog-restart-fixture.json)。最终源码仍a379，378项helper与35项参数/转换器测试不受本地采集修复影响。

### 7.4 磁盘与今晚命令（本轮未执行）\n\n历史full-20261030整根实测峰值为68,252,237,824B（63.565GiB）。规划同时保留两根：2×68,252,237,824=136,504,475,648B。演练前先加20%保守余量，再保留20GiB运行空间，参考目标185,280,207,258B（172.56GiB），当时满足。额外保留D失败现场后，再用演练实测的根外导出/driver/cache占用替代百分比粗估：两根历史峰值＋两份较大根外实测占用＋20GiB保留。20%是本轮规划参考，不是用户规定的硬门槛，更不是发布门槛；没有把旧构建峰值冒充本轮实测。\n\n'''
s+=f"演练前可用 {budget['available_bytes']:,}B；演练后 {free:,}B（{free/1024**3:.3f}GiB），按最终分项估算需 {budget['final_required_bytes']:,}B（{budget['final_required_bytes']/1024**3:.3f}GiB），另外还余 {budget['extra_space_after_final_estimate_bytes']:,}B。原20%保守参考是否仍满足：{budget['initial_extra_20_percent_target_still_met']}；明确保留该结果，不改写最初估算。根外实测见[outside-root-overhead.json]({base}outside-root-overhead.json)；[前后空间记录]({base}disk-budget-final.json)。T及D首轮、D重试根全部保留，full根toolchain/basedev尚不存在。启动当天仍按入口检查剩余空间，运行中低于20GiB停止，不删除任何历史目录。\n\n"
s+='''先T，T验证通过后才D，不能并行。本轮只写好以下命令，没有执行：\n\n```sh\n/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/final-launch-20261103/launch.sh toolchain full\n/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/final-launch-20261103/launch.sh basedev full\n```\n\n每次入口最后打印对应 `tail -f .../controller.stdout`；后台成功、失败、停止都打印带ISO时间、status、reason的“已结束”行。\n\n### 7.5 今晚T的验证口径\n\n| 对象 | 判定 |\n|---|---|\n| strip-all之后、RUNPATH之前 | SHA必须为 `13a07cb7f84bd1ceda4d851c8bd71bddf7ef0c2d4864892eba64cbbb9a0350b8` |\n| RUNPATH之后、debuglink之前 | SHA必须为 `8c2429d870f421a29a9914458bc4d4ff2ce359a15e0bdd20f39bfb4580c40bdf` |\n| 最终clang | SHA必须为 `4f08e12d499ebd492ce4951f74915ba435f57f2e380dc6f3520f24644996cb17` |\n| ordinary未strip、clang-22.debug、静态归档成员 | 允许记录编译命令的节导致SHA变化，但须逐文件/成员证明差异只在`.GCC.command.line`等明确的命令记录节，其余字节相同 |\n\n不能笼统忽略整个`.debug_info`、全部非LOAD节或整个归档成员。任何新增允许的“命令记录节”须给出其性质与逐字节范围证据；不能把无法解释的结构变化自动归入允许项。ar成员日期继续按成员顺序一致、成员内容SHA一致、全部差异仅date字段的三条件单列。23包对比按上述口径逐包给出内容/mtime/ar日期/命令记录差异，不把允许差异写成“完全相同”；源码包允许spec/helper/转换脚本的既定变化。90TU和其他原门禁仍必须执行。\n\n**总结论：本轮轻量检查及两次演练全部通过，今晚可以启动；本轮未运行完整构建，产物验证尚未发生。**\n'''
s=s.replace('../..//tools/bolt/results','../../tools/bolt/results').replace('BASE',base)
p=B/'docs/bolt/50_project_flag_independence.md';before=p.read_bytes();prefix=json.loads((E/(p.name+'.prefix.json')).read_text());assert len(before)==prefix['bytes'] and hashlib.sha256(before).hexdigest()==prefix['sha256'];p.write_bytes(before+s.encode())
status=B/'docs/bolt/STATUS.md'
with status.open('a') as f:f.write('''\n\n## 2026-11-03：50号轻量检查与两套演练闭合（未运行完整构建）\n\n- 源码仍a379c766（tree37c8c6d3），父5aff6c0c/祖父38477c9b未改；无发布代码改动。\n- 恢复48§13的host-tools/cmake后，显式helper378/378 PASS；显式新Source1005既有24项与新增11项全部PASS。\n- GBS export、双build.conf的12组完整展开比较、Tizen RPM4.14.1.1五项解析PASS；ARM逐字节同父提交，x86及OFF只差参数块。\n- T/D真实演练均到CMake即正常停止；T参数精确匹配QB1215143，D输出固定参数与架构参数，NORMALIZED/DROPPED原文存证。两根保留，服务/挂载/进程清理通过。\n- 今晚入口见[50号§7](50_project_flag_independence.md#7-轻量检查与演练续)，先T验证后D，full模式本轮没有执行。演练后按两份历史峰值＋两份根外实测占用＋20GiB保留重新分项核对满足；演练前额外20%保守参考及重试后的变化均明列于50号，不冒充强制门槛。\n- T的strip-all/RUNPATH/最终SHA保持硬要求；ordinary/debug/static成员仅允许严格证明为命令记录节的差异，ar日期单列，90TU仍必做。上一轮停止记录保留，不把轻量PASS冒充产物认证。\n- 仅推GitHub bolt-v4，无Gerrit/sandbox/QB操作，不触碰PGO现场和历史根。\n''')
print('REPORT_APPENDED',free)
