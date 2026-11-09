# 72. 第三轮代码评审修复与续跑

第二步全部轻量检查与 Toolchain、Base-Dev 两次演练均通过，三个源码提交保持不变。
sandbox 已按显式 lease 更新为 fa4f9978c9162d3c6cd2113d0cfe1173f04881c8，推后 SHA 与五提交链核对通过。
359934、357163 仍为 NEW，359934 仍是 PS10/13c3e223；本次补跑与推送见 §8–9。此前失败原文保留，不代表当前状态。

## 1. 身份与资源限制

源码 W/temp/rebase-359934-20261106/source，bolt-on-359934，原 HEAD c7fd5eed5e35ca335940239cae349a6936f74a7a；基线 13c3e223d9e1b35e4affb55255c5042f8c940f35。

所有命令串行运行于独立 systemd 用户服务，MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、Nice=19、IOSchedulingClass=idle（ionice -c3）。没有 OOM、完整构建、sudo、历史根写入、删除文件、新建分支或 QB 操作。W 原有 gbs_llvm.conf 修改未触碰。

修改先作 fixup/amend fixup，再执行 GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash 13c3e223d9e1b35e4affb55255c5042f8c940f35。最终仍为三个提交，作者/提交者/Signed-off-by 均为 Hao Lin <hao.lin@samsung.com>。

|顺序|SHA|tree|标题|
|---|---|---|---|
|1|a65688b1377e91819fcd46a18da36d52b3312089|3d961cbb04f5446f84d2089b4f65f3178f2bd7fa|cmake: use hybrid LLVM linkage on x86_64|
|2|22f1c9fd79de6086ee21f235868c70167868b7ff|4d78fb7cc802b4815bd04d8e3334ca3a73576dab|packaging: optimize x86_64 clang with BOLT|
|3|fa4f9978c9162d3c6cd2113d0cfe1173f04881c8|c9f61c77a1a08f5faffd45f8a37f6b46359922f7|packaging: fix x86 LLVM flags and archive mode|

标题长度分别 40、42、46；各说明最大行宽 72。git interpret-trailers --parse 仅解析出 Change-Id 和 Signed-off-by，最后一段也只有这两行。三个 Change-Id 不变，第一提交 tree 不变。见 [commit-metadata.json](../../tools/bolt/results/third-code-review-20261109/commit-metadata.json)、[source-commits.txt](../../tools/bolt/results/third-code-review-20261109/source-commits.txt)。

## 2. 采纳的修复与证据边界

未在指定设计文档附近找到评审原文，以本轮 prompt 的具体条目为准。

|问题|采用方案 / 所属提交|当前边界|
|---|---|---|
|ar 负长度、名字越界、缺对齐|第三提交：size<0 拒绝；stored_size 非负且不超过剩余文件；补齐后 pos 不越界；BSD 长度在 0..size；GNU 偏移在表内|已实现，新正反例未运行|
|PIC 表/索引不校验|第三提交：SHT_SYMTAB、24 字节 stride、整除/边界；RELA=24、REL=16；r_sym<symbol_count|已实现，实物全归档检查未执行|
|提前回收组长|第三提交：waitid(WEXITED/WNOHANG/WNOWAIT) 先观察；最后一次 SIGKILL 发给整个组；WNOWAIT 等待后在 self.lock 内 wait4 并移出 children；两处加 SIGHUP；正常 status/rusage 仍来自 wait4|已实现，新取消/worker/回收探针未执行|
|三工具来自不同目录|第三提交：llvm-dis/nm resolve 后 parent 与 compiler 相同|已实现，新目录夹具未执行|
|Rollback 错误描述 Source 关闭|第二提交：动作/专用 BuildRequires 关闭，Source1200/1201 保持声明供 GBS 插补丁|helper 仅注释变化，393 项通过|
|bolt_checked 吞取消状态|第二提交：else 先保存 $?，打印输出后 129/130/143 直接退出，其他失败维持诊断及 exit 1|展开差异符合范围，新必需调用信号探针未执行|
|提交说明|按用户给定文本替换两段、assembler/Based 段；所有超 72 列行折行|元数据已记录|

**未采纳：混合失败退出码改成 1。** 保留 128+信号，原因是改成 1 会让 bolt_optional 吞掉取消。本轮未改这一既有行为。

完整 diff：[source-diff.patch](../../tools/bolt/results/third-code-review-20261109/source-diff.patch)。只涉及三个 packaging 文件；profile、OPTIONS、白名单和 CMake 代码未改。说明 diff 同目录 message-1.diff、message-2.diff、message-3.diff。

编辑准备中，脚本因 spec 缩进匹配、第三提交原有 75 列行的保护断言中止，修正编辑脚本/折行后才归并提交；一次只读搜索因服务 PATH 无 rg 返回 127，随后改用 Python/grep。这些不是测试通过记录。正式测试停止点如下。

## 3. 第一次尝试已执行检查（本次全量重跑见 §7）

|检查|结果|原文|
|---|---|---|
|显式 helper 全量|393/393 PASS，25.004 秒|[helper-tests.log](../../tools/bolt/results/third-code-review-20261109/helper-tests.log)|
|T/D 完整展开|12 PASS；ARM/BOLT off 相同；x86 on 只差 bolt_checked|[expansion-summary.json](../../tools/bolt/results/third-code-review-20261109/parse/expansion-summary.json)，parse/ 下全文与 diff|
|Tizen RPM 五项解析|x86 on/off/一行回退、armv7l、aarch64 PASS|[five-summary.json](../../tools/bolt/results/third-code-review-20261109/parse/five-summary.json)|
|70 号 12 项|初始化 FAIL，0 项实际执行|[test_r2.log](../../tools/bolt/results/third-code-review-20261109/test_r2.log)|

~~~text
Ran 393 tests in 25.004s

OK
EXPANSIONS_PASS 12 ALL_BYTE_IDENTICAL False
EXPANSIONS_PASS 12 FIVE_PARSE_PASS 5
~~~

ALL_BYTE_IDENTICAL False 是预期的 x86 BOLT on 改动。比较器只剥去本轮新增的 bolt_status/case 行，然后要求与 c7fd5eed 展开逐字相同；ARM/off 不作归一化。

五项解析用当前 HEAD spec 和此前保留的相同 Source 导出目录，执行 Tizen rpmbuild -bp --nodeps --nobuild 与 rpmspec -P，不运行实际 %prep/构建。本轮未重新 gbs export。argv、RPM 版本、两份 build.conf SHA 见 parse/。

预期调整：[expectation-adjustments.json](../../tools/bolt/results/third-code-review-20261109/expectation-adjustments.json)。此前 cli-only 任务要求 12 展开全同，本轮 x86 on 仅允许上述差异；Commands accounting 文字改为 waitid(WNOWAIT), wait4，但新行为未测。70 号可选调用数量仍要求 5，没有放宽。

## 4. 第一次停止原因

~~~text
File ".../third-code-review-20261109/test_r2.py", line 16, in <module>
    assert len(calls)==5,calls
AssertionError: [disk-report begin, disk-report tool-built,
                 disk-report pipeline, cache-release]
~~~

上面列表是便于阅读的缩写，未删节 traceback 在 test_r2.log。本轮准备脚本把普通 rpmspec -P 输出写成 post-expanded.stdout；它没有显式展开宏 __spec_install_post 的执行体，漏掉第 5 个 disk-report post。新 spec 第 958 行仍保留该调用，不能据此认定发布代码缺调用。此前 70 号用专门的 post-expanded.spec 显式展开平台 post，旧输出第 816 行有第 5 个调用。旧命令、spec 尾部及出处见 [fixture-stop-analysis.json](../../tools/bolt/results/third-code-review-20261109/fixture-stop-analysis.json)。

**这是本轮测试输入准备错误。** 按“第一至三步任一失败就停止，不推送”执行：未修复夹具后重跑，没有将 4 个调用视为合格。

以下全部 NOT RUN：

- 70 号 12 项实际执行、cli 取消 2 项、转换器 46 项、50 号 5 项、真实 C-2 #5/#6。
- 新增 ar、重定位、SIGHUP/组长/worker 回收顺序、工具目录和 bolt_step 三信号正反例。停止时尚未编写新增夹具；复制的旧脚本不算完成新增测试。
- T/D 各 3853 个成员重放一致性；两个 QB 的全量归档/成员/PIC 检查，计数 UNKNOWN。
- T/D 演练及 log-restarts、FLAGS、WARNING、资源报告、进程/挂载审计。
- sandbox 前置查询、推送、推后 change/patch set 查询。

“参数一致”“转换输出一致”“整包一致”都没有本轮新证明；不能沿用旧版结果认证本轮转换器。

## 5. 第一次交付与远端状态

[r4 README](../../patches/rebase-359934-20261109-r4/README.md) 包含三个 format-patch、去 profile 的 0002、九份完整文本、相对 PS10 转换器 diff、相对 7d5e28ca/c7fd5eed 两份 diff、provenance、SHA256SUMS。第一次发布时 README 标明未完成验证；续跑后状态已更新为第二步全部通过、Base-Dev 演练未执行，仍不具备推送条件。

本轮未操作 Gerrit，也未重新读取远端。sandbox 最后核对的 HEAD 为 c7fd5eed5e35ca335940239cae349a6936f74a7a（70 §10）；359934/357163 的 NEW、359934 PS10/13c3e223 来自 2026-11-09 15:54 +08:00 历史查询，不冒充本轮当前状态。新本地 HEAD 是 fa4f9978c9162d3c6cd2113d0cfe1173f04881c8。

源码工作区干净，旧包与全部现场保留；只向 GitHub bolt-v4 发布文档、证据和明确未认证的材料。

## 6. 第一次尝试结束记录

~~~text
STEP1 已结束 2026-11-09T18:58:21.967853+08:00 status=ok
SERVICE 已结束 2026-11-09T18:59:47+08:00 status=0 unit=llvm-fix-r3-1109-011
SERVICE 已结束 2026-11-09T19:00:00+08:00 status=1 unit=llvm-fix-r3-1109-012
STEP2 已结束 2026-11-09T19:05:08.538170+08:00 status=failed reason=review70_fixture_expected_5_optional_calls_found_4
STEP3 已结束 2026-11-09T19:05:08.538170+08:00 status=not-run reason=step2_failed
STEP5 已结束 2026-11-09T19:05:08.538170+08:00 status=not-run reason=step2_failed
~~~

结论：**仍有问题；源码修改已保留，测试输入检查失败，未演练、未推送 sandbox。**


## 7. 修正测试输入后的全量续跑（2026-11-09）

### 7.1 输入生成修复

仅修改本轮准备脚本，不改源码、不改夹具的五调用期望。保留此前失败原文，新证据位于 [resume/](../../tools/bolt/results/third-code-review-20261109/resume/)。新建 post-expanded.spec，在当前 spec 副本末尾显式添加 %check 和 %{__spec_install_post}，再用相同 Tizen RPM 配置展开。与 70 号相同，平台 post 现在进入输入文本。

准备脚本差异原文：

~~~diff
--- previous/parse_checks.py
+++ resume/parse_checks.py
@@ -46,7 +46,14 @@
     restored=restored.replace(added,'',1)
     assert restored==outputs['parent'],key+suffix+' unexpected spec expansion changed'
    if name=='toolchain' and case=='x86-debug' and not off:
-    (E/'post-expanded.stdout').write_text(outputs['new'])
+    post_spec=E/'post-expanded.spec'
+    post_spec.write_text((P/'new.spec').read_text()+'\n%check\n%{__spec_install_post}\n')
+    post=run('post-expanded',loader+[str(R/'usr/bin/rpmspec'),'-P',*common,str(post_spec)])
+    (E/'post-expanded.stdout').write_text(post)
+    optional=[{'line':i,'text':line} for i,line in enumerate(post.splitlines(),1) if line.strip().startswith('bolt_optional python3 -B ')]
+    (E/'optional-calls.json').write_text(json.dumps(optional,indent=2)+'\n')
+    assert len(optional)==5,optional
+    for row in optional:print(str(row['line'])+': '+row['text'])
    rows.append({'config':name,'case':case,'bolt':'off' if off else 'on','PASS':True,'byte_identical':not diff,'difference':'optional cancellation shell wrapper, literal reviewed-list assignment, empty-debug warning' if diff else 'none'})
 (P/'expansion-summary.json').write_text(json.dumps(rows,indent=2)+'\n')
 print('EXPANSIONS_PASS',len(rows),'ALL_BYTE_IDENTICAL',all(r['byte_identical'] for r in rows))
~~~

新输入中的五个可选调用原文：

~~~text
475: bolt_optional python3 -B /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/third-code-review-20261109/resume/parse/rpmbuild/SOURCES/clang-bolt-helper.py disk-report begin
507: bolt_optional python3 -B /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/third-code-review-20261109/resume/parse/rpmbuild/SOURCES/clang-bolt-helper.py disk-report tool-built
510: bolt_optional python3 -B /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/third-code-review-20261109/resume/parse/rpmbuild/SOURCES/clang-bolt-helper.py disk-report pipeline
518: bolt_optional python3 -B /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/third-code-review-20261109/resume/parse/rpmbuild/SOURCES/clang-bolt-helper.py cache-release "$PWD" "$BOLT_WORK"
820:     bolt_optional python3 -B /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/third-code-review-20261109/resume/parse/rpmbuild/SOURCES/clang-bolt-helper.py disk-report post
~~~

第 5 个调用由旧输入第 816 行变为本轮第 820 行，增加的四行正是 bolt_checked 取消退出码分支。五调用夹具原断言 len(calls)==5 保持不变。

### 7.2 全部重新执行的检查

|检查|本次结果|证据|
|---|---|---|
|显式 helper 全量|393 PASS|resume/helper-tests.log|
|70 号新增用例（含 15 组可选调用信号探针）|12 PASS|resume/test_r2.log、new-tests-02-observed.json|
|cli 非 GateError 取消/普通异常|2 PASS|resume/test_cli_cancel.log|
|参数/转换器回归|46 PASS|resume/test_regressions.log、policy-result.json|
|50 号转换器回归|5 PASS|resume/test50.log|
|本轮新增夹具|14 组 PASS|resume/test_r3.log、r3-result.json、r3-observed.json|
|真实 release C-2 #5/#6|2 PASS；正例无调试节，注入调试元数据的反例拒绝|resume/real-c2-result.json、real_c2.log|
|完整展开|12 PASS；ARM/BOLT off 逐字相同，x86 on 仅 bolt_checked 差异|resume/parse/expansion-summary.json 及各全文/diff|
|Tizen RPM 五项解析|5 PASS|resume/parse/five-summary.json|
|重放参数|T 3853/3853、D 3853/3853，合计 7706 全同|resume/replay-summary.json、replay-members.jsonl.gz|
|QB 全部静态归档解析及 PIC|450 个归档全部通过|resume/qb-archive-summary.json、qb-archive-members.jsonl.gz|

共 **472 项单元测试，另加真实 C-2 两项**。本节所有数字来自本次重跑，没有沿用上次中断前的 PASS。

新增夹具覆盖：
- ar：size=-60/-1，负 BSD 长度、BSD 超长、GNU 负/越界偏移、缺对齐、超出剩余长度、thin 负 stored_size；均在一秒内拒绝。同名成员、GNU/BSD 长名字、32/64 位正常索引通过。
- PIC：r_sym 等于符号数（文件内越界位置特意放 SHN_ABS）、更大索引、错误符号表类型/零或错误 stride/残缺或越界表、REL/RELA 残缺；均拒绝。ABS、PC-relative、普通 PIC 正例通过。
- 取消：SIGHUP；组长先退出、忽略 SIGTERM 的孙进程；一个 worker 失败取消另一 worker。记录 killpg/wait4 次序，最后 SIGKILL 先于在锁内的组长回收，回收后不再向该 PID 发组信号；子孙无存活进程。正常返回码与旧实现相同，资源仍来自 wait4 的 user/sys/max_rss 字段，不要求不同实际运行的耗时数值相同。
- 三工具同 build/bin 通过，nm 在另一目录拒绝。
- 从真实展开的 /bin/sh -e 函数调用 bolt_step，分别仅向 helper 发 SIGTERM/SIGHUP/SIGINT，退出 143/129/130，没有后续标记和 BOLT_DISK_DIAGNOSIS；普通失败仍诊断并退出 1。
- 三个提交最后一段只有两个 trailer，git interpret-trailers 可解析，所有行≤72 列。

这些是新增测试，不是修改源码或放宽期望。所有临时副本保留；既有测试清理通过保全包装器转为本次 scratch 内保留/改名，不删除文件。

### 7.3 重放与实物归档详情

7706 条原命令中 -Wa,/-Xassembler 为 0，-g0 为 0；新旧 flags 列表逐项等于保全的 recorded_flags。对照转换器来自 c7fd5eed 的保全副本。

|QB|项目|归档数|成员数|受检重定位|禁止项|归档总字节|
|---|---|---:|---:|---:|---:|---:|
|1221204|Toolchain|225|3864|3763631|0|6615246904|
|1221207|Base-Dev|225|3864|3763631|0|476672032|

每个项目 3853 个转换成员加 11 个原样保留的原生成员。检查前按既有 RPM 载荷清单核对每个归档 SHA/大小，归档清单无遗漏；验证索引、native 格式及每个成员 SHA，再调用新 PIC 检查器。仅检查，没有对这些 QB 归档进行转换或修改。PIC 按转换器原规则不计调试节重定位。

**证明边界：** 重放参数全量一致；新的解析/PIC 门禁可接受两套既有 QB 实物；真实 C-2 只实际转换一个 release 成员及其负例。未重新转换全部 7706 个成员，未重建完整包，不能把上述结果写成“新版本整包逐字节相同”。

### 7.4 Toolchain 演练通过

使用原 tools/bolt/rebase-launch-20261106-r2/toolchain/launch.sh，参数为当前完整 HEAD 和 rehearsal-02；没有修改入口。新根 W/temp/rebase-359934-20261106-r2/rehearsal/toolchain/retry-02，保留此前根。沿用入口 MemoryMax=MemTotal-8GiB、swap=0、CPUQuota=1200%、nice10、ionice2/7；只有演练采用此例外，其余服务为 8G/400%/nice19/idle。

停在真实 + cmake -G Ninja，没有运行 Ninja。log-restarts 为 0，复制日志与 GBS 原始日志大小相同，FLAGS 与 QB 1221204 逐字一致，WARNING 两边均为 0，资源报告生成，挂载为空、remaining_build_processes=[]，prep/build 服务均 inactive/dead。

原文 FLAGS：

~~~text
TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] CXXFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] LDFLAGS=[]
TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[] CXXFLAGS=[] LDFLAGS=[]
~~~

完整审计：[comparison-audit.json](../../tools/bolt/results/third-code-review-20261109/resume/rehearsal-toolchain/comparison-audit.json)。命令、控制器原文、log-copy-audit、final-audit 和 resource-table.md 均保存在同目录。

### 7.5 Base-Dev 启动参数错误：停止、未重试

本轮驱动把 Toolchain 的两参数调用形式用于 Base-Dev，漏了最后的项目参数 basedev。这是本轮调用错误，不是发布源码或真实 Base-Dev 构建失败。

实际执行：

~~~sh
/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/rebase-launch-20261106-r2/basedev/launch.sh fa4f9978c9162d3c6cd2113d0cfe1173f04881c8 rehearsal-02
~~~

入口在 shift 后要求 rehearsal 模式有两个参数（模式、项目）。少了项目，因此在 [ "$#" -eq 2 ] || exit 2 退出；stdout/stderr 均为空，驱动记录 AssertionError: 2。

只读核对原文：

~~~text
BASEDEV_NEW_ROOT_EXISTS False
LoadState=not-found
ActiveState=inactive
SubState=dead
~~~

没有创建 retry-02 根、没有启动 Base-Dev 演练服务，因此没有本轮 D 的 FLAGS、WARNING、资源报告或挂载清理可供认证。已有历史根不动。

正确形式是下面这条，**本轮未执行，也未自动重试**：

~~~sh
/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/rebase-launch-20261106-r2/basedev/launch.sh fa4f9978c9162d3c6cd2113d0cfe1173f04881c8 rehearsal-02 basedev
~~~

依据、入口全文/SHA、实际 argv、未执行的正确 argv、服务状态见 [failure-analysis.json](../../tools/bolt/results/third-code-review-20261109/resume/rehearsal-basedev/failure-analysis.json)。按“第二、三步任一失败就停止，不推送”，第五步未执行，也未复查 Gerrit 状态。三个源码提交和 tree 与 §1 完全相同，工作区干净。

### 7.6 本次结束行与交付

~~~text
STEP2 已结束 2026-11-09T19:43:20.122584+08:00 status=ok reason=all_tests_replay_archives_expansions_pass
REHEARSAL 已结束 2026-11-09T19:50:23.584415+08:00 project=toolchain status=ok reason=CMake_stop_flags_log_resources_cleanup_pass
REHEARSAL 已结束 2026-11-09T19:50:38.311286+08:00 project=basedev status=failed reason=launch-or-audit-failed
STEP3 已结束 2026-11-09T19:51:55.602362+08:00 status=failed reason=basedev_launch_missing_project_argument
STEP5 已结束 2026-11-09T19:51:55.602362+08:00 status=not-run reason=step3_failed
~~~

72 号、STATUS、r4 README/provenance/SHA256SUMS 已按本次结果更新。r4 不再沿用“测试未完成”的旧结论，明确写为“第二步全部通过；Toolchain 演练通过；Base-Dev 启动参数检查失败，尚不具备推送条件”。源码与完整补丁保持原样。

最终结论：**第二步全部通过；第三步在 Base-Dev 启动参数检查处停止；未推送 sandbox。**


## 8. Base-Dev 补跑通过（2026-11-09）

本次只补跑 Base-Dev，不重做已通过的第二步和 Toolchain 演练；不改三个源码提交或入口脚本。其余命令仍在 8G、swap0、CPU400%、nice19、ionice-c3 的独立服务内串行执行，演练沿用入口原资源设置。

### 8.1 命令核对与新根

运行前打印完整 argv，并与当时本文第 234 行逐字比较：

~~~text
FULL ARGV: /bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/rebase-launch-20261106-r2/basedev/launch.sh fa4f9978c9162d3c6cd2113d0cfe1173f04881c8 rehearsal-02 basedev
DOC LINE 234: /bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/rebase-launch-20261106-r2/basedev/launch.sh fa4f9978c9162d3c6cd2113d0cfe1173f04881c8 rehearsal-02 basedev
EXACT_EQUAL True
~~~

入口固定创建 W/temp/rebase-359934-20261106-r2/rehearsal/basedev/retry-02。执行前不存在；上次失败仅留下证据，没有创建构建根。本次为首次创建，不复用旧构建根。新的证据放到 [basedev-finish/](../../tools/bolt/results/third-code-review-20261109/resume/basedev-finish/)，原失败证据保持原样。

### 8.2 审计全部通过

|审计项|结果|
|---|---|
|停止点|真实 + cmake -G Ninja；没有 + ninja|
|log-restarts|0|
|GBS 原始日志 / evidence 副本|58297 / 58297 字节|
|FLAGS|与 QB 1221207 逐字相同|
|FLAGS_WARNING|本地及 QB 均 0|
|资源报告|resource-table.md 正常生成|
|挂载|stdout 为空|
|构建进程|remaining_build_processes=[]|
|prep/build 服务|均 inactive/dead，Result=success|
|源码 HEAD / tree|fa4f9978 / c9f61c77，与本次开始时相同；工作区干净|

本地日志原文与行号：

~~~text
574: TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] CXXFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] LDFLAGS=[]
576: TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] CXXFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] LDFLAGS=[]
~~~

对应 QB 行号分别为 670、672。完整对照与清理输出见 [comparison-audit.json](../../tools/bolt/results/third-code-review-20261109/resume/basedev-finish/rehearsal-basedev/comparison-audit.json)，其中记录 source、service、mount、process 原文；同目录保留 launcher-used.py、final-audit.json、原始日志、资源表及清理检查。

控制器结束原文：

~~~text
NIGHT_PROJECT 已结束 2026-11-09T20:43:35.970234+08:00 status=ok reason=rehearsal-complete-at-CMake
REHEARSAL 已结束 2026-11-09T20:43:53.745928+08:00 project=basedev status=ok reason=CMake_stop_flags_log_resources_cleanup_pass
~~~

### 8.3 验证结论与交付

第三步现已通过：Toolchain 和 Base-Dev 均合格。结合 §7 的 472 单元测试、真实 C-2 两项、7706 重放、450 归档全量解析/PIC、12 展开和 5 RPM 解析，已满足本轮推送前的轻量检查及演练要求。

没有完整构建；“重放参数一致”“既有归档检查通过”不扩写为“新版本整包一致”。r4 README/provenance/SHA256SUMS 已更新，源码与补丁/files 内容不变。按任务顺序先推 GitHub 材料，再执行 sandbox 核对与推送，结果记在下一节。

~~~text
STEP1 已结束 2026-11-09T20:45:23.577146+08:00 status=ok reason=exact_argv_rehearsal_CMake_stop
STEP2 已结束 2026-11-09T20:45:23.577146+08:00 status=ok reason=log_flags_resources_cleanup_pass
~~~


## 9. sandbox 推送与推后核对（2026-11-09）

完成 §8 后，先将合格材料推到 GitHub bolt-v4，提交 a21e5d9322acd75780cdc5f4b6c032146440cd0a，再进入本节。所有 Gerrit 命令均使用 SSH BatchMode 和完整 URL，不请求密码，不推 refs/for，不新建分支、不改 remote 配置。

### 9.1 推送前核对及唯一推送命令

源码仍在 bolt-on-359934，HEAD/tree 与 §1 相同，工作区干净。远端原文：

~~~text
c7fd5eed5e35ca335940239cae349a6936f74a7a	refs/heads/sandbox/lhmax2025/bolt_pgo
~~~

与期望 c7fd5eed5e35ca335940239cae349a6936f74a7a 精确相同，因此执行：

~~~sh
git push --force-with-lease=refs/heads/sandbox/lhmax2025/bolt_pgo:c7fd5eed5e35ca335940239cae349a6936f74a7a ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm bolt-on-359934:refs/heads/sandbox/lhmax2025/bolt_pgo
~~~

原样输出：

~~~text
remote: 
remote: Processing changes: refs: 1        
remote: Processing changes: refs: 1, done            
To ssh://review.tizen.org:29418/platform/upstream/llvm
 + c7fd5eed5e35...fa4f9978c916 bolt-on-359934 -> sandbox/lhmax2025/bolt_pgo (forced update)
~~~

只执行这一次指定的 force-with-lease；没有其他强推方式或重试。

### 9.2 推后 SHA、父链及 change 状态

ls-remote 原文：

~~~text
fa4f9978c9162d3c6cd2113d0cfe1173f04881c8	refs/heads/sandbox/lhmax2025/bolt_pgo
~~~

五提交链（SHA、tree、标题）：

~~~text
fa4f9978c9162d3c6cd2113d0cfe1173f04881c8 c9f61c77a1a08f5faffd45f8a37f6b46359922f7 packaging: fix x86 LLVM flags and archive mode
22f1c9fd79de6086ee21f235868c70167868b7ff 4d78fb7cc802b4815bd04d8e3334ca3a73576dab packaging: optimize x86_64 clang with BOLT
a65688b1377e91819fcd46a18da36d52b3312089 3d961cbb04f5446f84d2089b4f65f3178f2bd7fa cmake: use hybrid LLVM linkage on x86_64
13c3e223d9e1b35e4affb55255c5042f8c940f35 087e06cf9c79c571c711af8a07057496940ae73d packaging: classify -feliminate-unused-debug-types and mirror recorded backend policy
cf4b6777d056131e2534ecb460c5575327d99646 7b49745738b5512fbbed890e67e6a3861e1e39a5 Revert "Revert clang bootstrap + ThinLTO, fall back to GCC"
~~~

|change|状态|当前 patch set|revision|
|---|---|---:|---|
|359934|NEW|10|13c3e223d9e1b35e4affb55255c5042f8c940f35|
|357163|NEW|2|cf4b6777d056131e2534ecb460c5575327d99646|

359934 当前 patch set 没有变化，仍为本次基线 PS10。357163 按 Change-Id I5779f1689f330ee006bcbda377feeccf15040e85 查询并核对 change number。两者均未因本次 sandbox 推送关闭。

[Gerrit 查询与推送原文](../../tools/bolt/results/third-code-review-20261109/resume/basedev-finish/gerrit/) 保存每条命令 argv、退出码和输出；[summary.json](../../tools/bolt/results/third-code-review-20261109/resume/basedev-finish/gerrit/summary.json) 给出结构化结果。

[sandbox gitweb](https://review.tizen.org/gerrit/gitweb?p=platform/upstream/llvm.git;a=shortlog;h=refs/heads/sandbox/lhmax2025/bolt_pgo)。后续 QB 软件包行是 platform/upstream/llvm@fa4f9978c9162d3c6cd2113d0cfe1173f04881c8；本轮没有操作 QB。

### 9.3 结束行

~~~text
STEP1 已结束 2026-11-09T20:45:23.577146+08:00 status=ok reason=exact_argv_rehearsal_CMake_stop
STEP2 已结束 2026-11-09T20:45:23.577146+08:00 status=ok reason=log_flags_resources_cleanup_pass
STEP3 已结束 2026-11-09T20:45:29+08:00 status=ok reason=qualified_materials_published
STEP4 已结束 2026-11-09T20:46:35.339006+08:00 status=ok reason=authorized_sandbox_push_succeeded
STEP5 已结束 2026-11-09T20:46:45.510049+08:00 status=ok reason=remote_chain_and_change_states_recorded
~~~

最终结论：**本轮要求的轻量检查、两次演练与 sandbox 推送核对全部完成；未运行完整构建。** 三个本地提交、源码和入口脚本未因本次补跑改动。全部现场保留，GitHub bolt-v4 再次更新本文、STATUS 与 r4 材料。
