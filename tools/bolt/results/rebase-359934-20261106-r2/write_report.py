from pathlib import Path
import json,hashlib,subprocess,os
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=Path(str(W)+'-bolt');S=W/'temp/rebase-359934-20261106/source';E=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=json.loads((E/'commit-identities.json').read_text());head=rows[-1]['sha'];q=chr(96);fence=q*3
hp=S/'packaging/clang-bolt-helper.py';cp=S/'packaging/llvm-static-archives-native.py'
assert sha(hp) in (E/'helper-02.stdout').read_text().splitlines()[0]
assert sha(cp) in (E/'converter.stdout').read_text().splitlines()[0]
cm=W/'temp/review-20261103/host-tools/cmake';env=dict(os.environ,PATH=str(cm.parent)+':'+os.environ['PATH'])
v=subprocess.run([str(cm),'--version'],cwd=E,env=env,capture_output=True,text=True,check=True)
inv={'helper':str(hp),'helper_sha256':sha(hp),'converter':str(cp),'converter_sha256':sha(cp),'source_head':head,
 'PATH':env['PATH'],'cmake_wrapper':str(cm),'cmake_wrapper_sha256':sha(cm),'cmake_wrapper_text':cm.read_text(),'cmake_version':v.stdout,
 'resource_properties':{'MemoryMax':'8G','MemorySwapMax':0,'CPUQuota':'400%','Nice':19,'IOSchedulingClass':'idle'},
 'helper_argv':['python3','-B',str(E/'run_preserved.py'),str(B/'tools/bolt/run_review_tests.py'),'--helper',str(hp)],
 'helper_scratch':str(W/'temp/rebase-359934-20261106-r2/helper-tests-02'),
 'fixture_cleanup':'temporary files retained; Path.unlink/rmtree redirected to scratch retained-cleanup',
 'rehearsal_exception':'existing MemoryMax=MemTotal-8GiB, swap0, CPUQuota1200%, Nice10, ionice2/7'}
(E/'test-invocation.json').write_text(json.dumps(inv,ensure_ascii=False,indent=2)+'\n')
T=json.loads((E/'rehearsal-toolchain/rehearsal-audit.json').read_text());D=json.loads((E/'rehearsal-basedev/rehearsal-audit.json').read_text())
r=json.loads((E/'real-gates-result-02.json').read_text())
adjust=[
 ['取消测试笼统 nonzero 或 rc=1','SIGHUP=129、SIGINT=130、SIGTERM=143；纯 Python SIGTERM 从 1 改为 143','取消不能被 spec 可选诊断吞掉'],
 ['expected debug, found release (expected=yes found=no)','expected debug, found release（反向同理）','去掉重复部分'],
 ['环境空 expected-dropped 注入负例','环境任何值无效；负例改写副本字面值','不允许环境覆盖发布清单'],
 ['空调试序列 []','no debug options','明确警告含义'],
 ['稀疏 checkout 直接读 AddLLVM.cmake','文件未检出时 git show HEAD:llvm/cmake/modules/AddLLVM.cmake；断言不变','首次 helper 唯一 ERROR 为未检出文件'],
 ['复制的解析脚本假定 export 有 8 个 Patch','按本 clone 的 native export 核对，Patch 数 0','源码归档实际为 llvm-22.1.8.tar.gz，五项解析完整通过'],
 ['普通 rpmspec -P 已可见第 5 个调用','测试副本追加 %check 调用 __spec_install_post，实际展开后取第 5 行','宏默认不执行；发布 spec 未加测试段'],
 ['旧源测试拒绝 -fno-function-sections','沿用69号对 PS10 的接受/按开关重放预期','既有基线行为，非本轮放宽']]
(E/'expectation-adjustments.json').write_text(json.dumps(adjust,ensure_ascii=False,indent=2)+'\n')
base='../../tools/bolt/results/rebase-359934-20261106-r2/'
def link(name,label=None):return '['+(label or name)+']('+base+name+')'
def block(text,kind='text'):return '\n'+fence+kind+'\n'+text.rstrip()+'\n'+fence+'\n'
table='\n'.join('| '+x['title']+' | '+x['sha']+' | '+x['tree']+' | '+str(x['title_length'])+' |' for x in rows)
report=f"""# 70. 第二轮代码评审修复（2026-11-06）

本轮代码修复、轻量检查、实物门禁复核和两次 CMake 入口演练均通过。
7706 个成员的重放参数完全一致，保留的 BOLT 中间产物重新 strip、修 RUNPATH、加 debuglink 后，最终 clang 与 63 号产物逐字节相同。
没有完整重建 LLVM 或 RPM；全量归档转换输出和新整包一致性尚未证明，三个源码提交仅保留在本地。

## 1. 提交、归属和资源边界

分支仍为 bolt-on-359934，基线固定 13c3e223d9e1b35e4affb55255c5042f8c940f35。
在原 HEAD 7d5e28ca89ed68e3360765bc4e42234eaaabae27 上制作 BOLT fixup ee58716244c9385da9d70d55514b279c686cca13 和第三提交的 amend/fixup 594676e15f9d4923ee17374095cf9e479b7c5ddb，再执行 GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash 13c3e223d9e1b35e4affb55255c5042f8c940f35。
仍恰好三个提交，混合链接的 SHA/tree 均不变。作者、提交者、Signed-off-by 均为 Hao Lin <hao.lin@samsung.com>，三个 Change-Id 保持原值。

| 标题 | SHA | tree | 标题字符数 |
|---|---|---|---|
{table}

{link('commit-identities.json','完整身份、父链和 trailers')}；[三个补丁及全文](../../patches/rebase-359934-20261106-r2/README.md)。
三个 format-patch 在独立临时 index 中从 PS10 顺序应用，得到 tree {rows[-1]['tree']}，与 HEAD 相同（{link('patch-application.json','应用验证')}）；没有新建分支或改变源码工作树。

除演练沿用原入口限制外，所有命令串行运行在独立 systemd 用户服务中：MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、Nice=19、IOSchedulingClass=idle。没有 OOM、没有提高限制；服务均打印带时区的结束行。没有完整构建、手动 sudo、文件删除、Gerrit/sandbox/QB 操作。新根及失败夹具保留。

{link('test-invocation.json','测试入口、完整 PATH、CMake 版本和包装器 SHA、源码 SHA')}。CMake 通过既有 host-tools 包装器在新临时目录执行，未在历史构建根运行 CMake/Ninja/GBS。

## 2. 逐条修复与评审方案

| 评审意见 | 采用的方案与验证 |
|---|---|
| assembler 参数被宽泛 -W 分支放过 | 第三提交在宽泛分支前拒绝 -Xassembler/-Wa,，其他 HQ 分支不改。3 个负例拒绝，-Wall/-Wno-unused 通过。 |
| 三工具可能不是同一版本 | 按 Kimi 方案匹配 clang version X.Y.Z、LLVM version X.Y.Z；保留主版本检查和原返回字段。dis/nm 任一不等均拒绝，同版通过；真实 C-2 也通过实际版本核对。 |
| debug-info 报错重复、-g0 边界 | 保留 expected/found 两个值，去掉括号重复；仅补 -g0 注释，分类逻辑不改。7706 条实际命令中 -g0 为 0。 |
| debuglink 未覆盖 ELF 头和 LOAD 填充 | 第二提交加入 execution_layout=strip_layout(path)，仍只归一化 e_shoff[40,48)、e_shnum[60,62)、e_shstrndx[62,64)，不扩大例外。真实正例和四个单字节负例均符合预期。 |
| 可选诊断吞掉取消 | cli 返回 128+signal；bolt_optional 对 129/130/143 退出整个脚本，其他非零返回 0。只改五处可选调用，失败分支中随后 exit 1 的诊断不动。 |
| 清理取消覆盖原命令失败 | call 保留原错误，生成 CANCELLED: cancelled by signal N; while handling: COMMAND_ERROR: COMMAND_FAILED …。纯取消信息沿用。GateError.cancel_originated 属性决定是否跳过磁盘诊断，混合失败仍诊断。 |
| 混合错误可能再被 TIMEOUT 包装 | run_step 的 TIMEOUT 判断由包含改为 startswith，避免覆盖前置 CANCELLED；TIMEOUT 原路径保持。 |
| 注释与 docstring | rpath_layout 注释放在 docstring 后；Popen/ACTIVE_GROUP 注明第二次信号微秒窗口与 preexec_fn 死锁风险；record_cancel 注明第二次信号终止不恢复旧处理器。 |
| expected-dropped 受环境影响 | 第三提交固定四 token 字面值，上方注明 QB 1214821；环境未设、空值、其他值的行为都一致。 |
| 空 debug 序列提示不清 | debug CFLAGS/CXXFLAGS 序列为空时显示 no debug options；非空序列沿用原格式，不改变编译参数。 |
| 第三提交 MODULE/LDFLAGS 说明 | 明确 Base-Dev MODULE 获得 -z relro、--as-needed、--gc-sections，EXE/SHARED 仍由 spec 指定；补充 assembler 拒绝和三工具版本检查一句。 |

## 3. 测试与预期调整

| 检查 | 本轮结果 | 原始证据 |
|---|---|---|
| 显式 helper 全部既有测试 | 393/393，27.070 s | {link('helper-02.stderr')}、{link('helper-02.stdout')} |
| 51/69 参数与转换器回归（既有 42 + HQ 4） | 46/46，17.759 s；显式导入新转换器并打印 SHA | {link('converter.stderr')}、{link('test_regressions.py')} |
| 50 号 release 回归 | 5/5 | {link('converter50.stderr')} |
| 53/69 真实 release C-2 #5/#6 | 真实 AArch64AsmParser.cpp.o 正例无 debug 节；注入调试元数据反例拒绝 | {link('real-c2-result.json')} |
| 本轮新增检查 | 12/12，1.408 s | {link('new-tests-02.stderr')}、{link('new-tests-02-observed.json')} |
| 真实 ELF strip/debuglink/post | 全通过；3 个 tiny、8 个 real 用例 | {link('real-gates-result-02.json')}、{link('real-post-result-02.json')} |
| 两配置完整展开 | 12/12 | {link('parse-03/expansion-summary.json')} |
| Tizen RPM 五项解析 | 5/5 | {link('parse-03/five-summary.json')} |

C-2 #1–4、#7、#8 与原转换器测试包含在 46 项中；#5/#6 另用 D 保存的真实 bitcode 成员实测，不使用 tools 旧转换器副本。
五个可选调用点分别为 disk-report begin、tool-built、pipeline、cache-release、post。探针从实际 Tizen RPM 展开的函数和调用行构造 /bin/sh -e 脚本，只向 helper 发三种信号：15 个组合退出码均为 143/129/130，后续标记均不执行；5 个普通 rc=1 组合均继续。
post 宏通过测试副本追加 %check 调用 __spec_install_post 展开，发布 spec 不加测试段。命令 rc=1 后清理期间 SIGTERM 的并发例同时保留 COMMAND_FAILED/CANCELLED 并调用磁盘诊断。二次信号及子孙进程清理既有测试继续通过。

| 原预期/准备方式 | 新预期/处理 | 原因 |
|---|---|---|
"""
report+='\n'.join('| '+' | '.join(x)+' |' for x in adjust)
report+=f"""

完整清单见 {link('expectation-adjustments.json')}。第一次 helper 缺文件 ERROR、旧解析脚本对象/导出布局错误、post 宏探针准备错误、实物 post 夹具缺 int_lib.h 的原文均保留。实物第二次准备将 compiler-rt builtins 头文件复制到新目录；没有为测试失败放宽发布门禁。成功结果使用 -02/-03 文件名，与失败证据分开。

## 4. 导出与展开逐处比较

GBS native export 成功，源码为最终 HEAD（{link('export-command.json','命令')}、{link('export.stdout','输出')}）。
Toolchain build.conf SHA e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945；
Base-Dev SHA 8ace286a5f98f2e02a79be275a64c22a86ea2b0034174c1e293381e181ce3f6a。

各配置覆盖 x86 debug/release 的 BOLT on/off，以及 armv7l/aarch64，共 12 项。相对 7d5e28ca：

- 两配置的 ARM 展开逐字节相同，diff 为空。
- x86 BOLT on 仅 expected-dropped 字面赋值/注释、空调试序列描述、bolt_optional 定义和五处可选调用有变化。
- x86 BOLT off 仅参数函数中上述两处变化。
- 每项按精确允许片段还原后与旧版逐字节相同，全部 *-unexpected.diff 为空。源码末尾 post 宏另有实际展开探针。

全文、原始 diff 和允许片段位于 {link('parse-03/','parse-03/')}；五项解析覆盖 x86 on/off/一行回退及两个 ARM 架构。

## 5. 参数和转换输出一致性的证据

{link('replay-summary.json')}：
"""
report+=block((E/'replay-summary.json').read_text(),'json')
report+=f"""
T 3853 + D 3853 条参数列表逐项相同；-Wa,/-Xassembler 条数 0；-g0 条数 0。每条原命令、新旧列表和成员路径见 {link('replay-members.jsonl.gz')}。

helper 的 pipeline、replay_script、add_debuglink、adjust_rpath、tiny_gate、real_gate、post_gate AST 均与旧版相同；全部大写常量及 Source1200 不变。本轮修改检查和取消路径，成功路径生成参数不变。{link('generation-parameters-proof.json')}。

一个真实 release bitcode 成员用旧/新转换器分别生成原生对象，SHA 均为 ec3c09329a17d0809ac8371d258bf8b9ae364b59b57c0e4f94d123f352696106（{link('output-sample-result.json')}）。此处仅抽查 **1 个真实成员**，没有全量重转 7706 个成员。

## 6. 保留产物上的门禁复核

只读来源为 63 号 temp/night-20261105/toolchain 的 build/clang-bolt。来源/副本逐个校验 SHA；在本轮新目录使用该根 llvm-strip、llvm-objcopy、loader/运行库处理副本，CMake RPATH_CHANGE 也只改新副本。

| 阶段 | 本轮 SHA | 与保留产物 |
|---|---|---|
| strip-all | {r['strip_sha']} | 相同 |
| RUNPATH 后 | {r['RUNPATH_sha']} | 相同 |
| 重新加 debuglink 后 | {r['final_sha']} | 相同 |

符号文件 SHA 9942e19c75ffef55f2846e6f1ea60651b4502de6e099c038a3d93bad4f5df690。CRC、debugfiles.list、安装 SHA、别名和安全属性检查通过；post 原函数在新目录安装形态副本上通过 3 个 tiny + 8 个 real 编译检查。没有重新装 RPM、运行平台后处理或执行 BOLT 重写。

| 真正添加 debuglink 后的副本负例 | 文件偏移 | 结果 |
|---|---:|---|
| e_entry 一个字节 | 24 | 拒绝 |
| e_flags 一个字节 | 48 | 拒绝 |
| LOAD 内节间填充一个字节 | 796 | 拒绝 |
| .text 一个字节 | 41938944 | 拒绝 |

{link('real-gates-copies-02.json','复制清单')}、{link('real-gates-calls-02.json','完整 argv')}、{link('debuglink-real-cases-02.json','正反例')}、{link('real-gates-02.stdout','原始输出')}。

## 7. T/D 串行演练

新入口副本为 tools/bolt/rebase-launch-20261106-r2/，只替换 T 源码路径、新根和服务名前缀。T 继承 night-launch-20261105，D 继承已修复的 rebase-launch-20261106/basedev。
{link('toolchain-launcher.diff','T 入口 diff')}、{link('basedev-launcher.diff','D 入口 diff')}；各副本 provenance.json 记录模板 SHA。

源码均为 {head}。T 使用 tizen-base-toolchain_20261030.061318，build.conf SHA 8f201a0d58eb634e60a1f213f47fc09dfa953d9869cdc5724f326a76203587bf；
D 使用 tizen-base-dev_20261030.061217，SHA 8ace286a5f98f2e02a79be275a64c22a86ea2b0034174c1e293381e181ce3f6a。
沿用 MemoryMax=MemTotal−8GiB、swap0、CPUQuota1200%、Nice10、ionice2/7。

| 审计 | T | D |
|---|---|---|
| 停止点 | + cmake -G Ninja | + cmake -G Ninja |
| Ninja | 未运行 | 未运行 |
| log-restarts | 0 | 0 |
| 原始/复制日志字节数 | {T['source_bytes']}/{T['copy_bytes']} | {D['source_bytes']}/{D['copy_bytes']} |
| 日志逐字节相同 | PASS | PASS |
| FLAGS 与对应 QB | PASS | PASS |
| WARNING | 0 | 0 |
| 资源报告 | 正常生成 | 正常生成 |
| 残留挂载/进程 | 0/0 | 0/0 |
| prep/build/controller | inactive，Result=success | inactive，Result=success |
"""
for label,a in [('toolchain',T),('basedev',D)]:
 report+='\n### '+label+' 原文\n'
 report+=block('\n'.join(x['text'] for x in a['local_flags'])+'\nTIZEN_LLVM_FLAGS_WARNING: 0 条\n'+(E/f'rehearsal-{label}/rehearsal/controller.stdout').read_text())
 report+='\n'+link('rehearsal-'+label+'/','原日志、行号、清理检查和资源表')+'\n'
report+="""
## 8. 证明边界

| 主张 | 已证明 | 未证明 |
|---|---|---|
| 参数一致 | 7706 条新/旧重放列表相同；helper 成功路径生成代码/常量不变；T/D 演练 FLAGS 与 QB 相同 | 新完整构建所有命令的最终观察 |
| 转换输出一致 | 1 个真实 release 成员的原生对象 SHA 相同；真实 C-2 正反例通过 | 7706 个成员全量重新转换后的逐字节比较 |
| clang 产物一致 | 保留中间产物的新 strip/RUNPATH/debuglink 结果 SHA 与 63 号一致；新 post 门禁通过 | 新源码完整构建后产生的 BOLT 输入/clang |
| 整包一致 | 本轮不作此结论；完成 export、展开、解析 | 新完整构建及逐包/成员比较和平台后处理实测 |

## 9. 相对 7d5e28ca 的完整 diff

仅三个 packaging 文件，67 行新增、23 行删除；六个 CMake 文件不变。
"""
report+=block((E/'source-vs-7d5e.diff').read_text(),'diff')
report+='\n结论：轻量检查、实物门禁复核和两个演练通过；三个提交仅本地，未做完整构建，未推 Gerrit/sandbox。\n'
target=B/'docs/bolt/70_second_code_review_fixes.md';assert not target.exists();target.write_text(report)
with (B/'docs/bolt/STATUS.md').open('a') as f:f.write(f"""
## 2026-11-06：第二轮代码评审修复（70 号）

- 本地三提交：混合链接 {rows[0]['sha']} 不变；BOLT {rows[1]['sha']}；固定参数/转换器 {head}。Change-Id 保留，标题 40/42/46 字符，未推 Gerrit/sandbox。
- helper 393、参数/转换器 46（包含既有 42）、50 号 5 项、新增 12 项及真实 C-2 正反例通过；12 项展开和 5 项 RPM 解析通过。
- 7706/7706 重放参数一致，assembler token 和 -g0 均为 0；一个真实 release 成员新旧转换输出一致。63 号实物副本 strip/RUNPATH/debuglink/post 通过，最终 SHA e08724d8… 不变。
- T/D 串行演练通过，log-restarts=0，FLAGS 对 QB 一致，WARNING=0，无残留；未运行 Ninja 或完整构建。
- 参数一致已全量核对；转换输出仅实测一个真实成员；整包一致尚未重建验证。其余挂账和风险保持。
- [70 号文档](70_second_code_review_fixes.md)；[本轮评审包](../../patches/rebase-359934-20261106-r2/README.md)。
""")
print('REPORT_WRITTEN',target)
