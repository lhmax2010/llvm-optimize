# 122：120复审修正（STOP，未生成H4）

**结论：新增15/15通过，既有118真实夹具失败后STOP。计划737项，实际29项：28通过、1失败、708未运行。未生成H4、未推sandbox；六个逐项工作提交保留，尚未认证。**

N2改变了历史错误的处理策略：最终完整空扫描确认干净时成功，并打印恢复日志。未修改的118夹具仍要求permission场景抛出异常，出现直接冲突。按任务规则保留断言、不修实现去恢复旧策略，也不继续剩余测试或探针。

## 逐项修改与全部复审发现

|编号/来源|处理与范围|工作提交|对应测试及状态|
|---|---|---|---|
|D1 / N4 名称（Codex/Claude）|stat第2字段comm与扫描成员一起保存；snapshot无额外I/O，旧内部无名描述用?；不改变身份校验字段索引|`0085be668dee7ebb442bf91d84ca2bc66ccaa595`|test_real_scan_names_survive_exit_without_comm_reads、test_stat_name_parentheses通过；119部分成员PID:python原断言通过|
|N4 长度（Claude）|snapshot和共享deadline的成员列表最多20个，尾部+N more|`64357fab1e56812c7abd41b14d979130c8e221c8`|snapshot/deadline列表截断两项通过|
|N4 措辞（Claude）|kill模式cleanup deadline，排空模式drain deadline|`626882948ec1059428aa8a7d5be22678572c11f7`|cleanup/drain两项通过|
|D2 / N1（Codex/Claude）|共享deadline消息去掉scan incomplete；读取错误标签member read errors|`50932b50a3542d2982c5a63484bf9a1693ca77ae`|完整扫描后signal截止、部分扫描截止、EIO/EMFILE四项通过|
|N2（Claude；PM新策略）|最终完整空扫描且无本轮错误成功；历史错误以SESSION_TRANSIENT_ERRORS_RECOVERED记录。leader group错误也在验证干净后作为恢复诊断；原命令失败仍保留|`c2e34724e42ed3b1f28aa173e0c345ae29e3b0cc`|瞬时恢复两项、持续错误失败、原命令rc7保持失败通过；118 permission真实夹具FAIL，STOP|
|N3（Claude）|仅注释说明持续扫描错误可能消耗排空和清理约两个预算，不改预算|`f47f0ad8d7bad4b30ca777a2c10ebce367ea790a`|未单独测时；后续全套未完成|

其他复审发现全部登记如下；本次未扩大产品修改范围：

|发现|来源|处理|
|---|---|---|
|此前R1/R2、R3/L2、L1、EACCES已经闭合；退休SID/pidfd/force latch等不变量|两份报告|保留H3实现；本次只有已执行的部分回归结果，不能把722旧结果沿用|
|进程级EMFILE导致pidfd无法杀死leader组外成员，禁止运行时静默降级|Claude已知限制、Codex不变量|保留限制，不增加数字PID回退；本次未运行all-EMFILE探针|
|扫描阶段malformed stat GateError、/proc/self身份读取失败仍会直接失败|两份报告|记录，未修改；本次EIO/EMFILE测试只针对成员读取OSError|
|首取消信号在排空等待期间不立即缩短预算；setsid逃逸、权限/不可杀死成员、fallback PID竞争、单次内核操作超时|Codex不变量、Claude既有行为|保留已知边界，不承诺cgroup隔离或硬实时截止|
|fixture真实/mock证据层次、formatter覆盖不足、瞬时扫描及kill-pass deadline覆盖不足|两份测试章节|新增15项，3项真实自有进程结合注入/观测，12项纯mock；未冒称全部为真实实物测试|
|worker pidfd/fallback运行资格、Python3.9与产品其他功能未独立复审|两份范围限制|未新增构建、QB或worker认证|

## 工作树与测试

- 独立稀疏工作树：`/home/linhao/Toolchain/development/llvm-optimize/temp/ps5-helper-122/source`，分支`task122-session-review`，只检出packaging；完整Git tree仍保留其他文件。
- 基底H3：`db7ac04bd2b854b144f6e5c5fcf3a0aa9645c01e`。
- 未认证工作末端：`f47f0ad8d7bad4b30ca777a2c10ebce367ea790a`，tree `e47327fbfd340ec8688c14f4e4bfd9895862484e`；不是单提交H4。
- 工作tree相对H3：`24	18	packaging/clang-bolt-helper.py`；[helper.diff](../../tools/bolt/results/ps5-helper-122/helper.diff)仅为未认证工作差异。
- 原118工作树、其他项目和120-N编排脚本未操作；未获取其锁或向其发信号。

|套件|计划|执行|结果|
|---|---:|---:|---|
|review122|15|15|PASS|
|review120|2|2|PASS|
|review119|6|6|PASS|
|review118|19|6|5 PASS / 1 FAIL|

剩余708项未运行，包括118剩余13项及其后套件；不能声明全部722既有项通过。所有旧断言保持原样，顶层测试源码逐字节一致检查见[test-source-equality.json](../../tools/bolt/results/ps5-helper-122/test-source-equality.json)。解析driver只切换被测源码路径。

新增测试共15：混合真实进程3项（名称扫描后退出、失败命令恢复后仍失败、第二信号真实自终止并运行真实formatter），纯mock12项。没有按名称或裸PID清理外部进程；真实Popen由持有者清理或自身信号退出。`test_119.py`的第一个部分成员PID:python要求本次通过，未改断言。

## STOP原文

```text
test_ESRCH_after_real_pidfd_open (__main__.Review118.test_ESRCH_after_real_pidfd_open) ... ok
test_L1_failure_before_retirement_store (__main__.Review118.test_L1_failure_before_retirement_store) ... SESSION_KILL_MODE=pidfd
ok
test_L1_success_before_retirement_store (__main__.Review118.test_L1_success_before_retirement_store) ... SESSION_KILL_MODE=pidfd
ok
test_L2_incomplete_empty_keeps_previous (__main__.Review118.test_L2_incomplete_empty_keeps_previous) ... ok
test_L2_timed_out_empty_keeps_previous (__main__.Review118.test_L2_timed_out_empty_keeps_previous) ... ok
test_R1_permission_rescan_fork_real (__main__.Review118.test_R1_permission_rescan_fork_real) ... FAIL

======================================================================
FAIL: test_R1_permission_rescan_fork_real (__main__.Review118.test_R1_permission_rescan_fork_real)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/ps5-helper-122/tests/test_118.py", line 19, in test_R1_permission_rescan_fork_real
    def test_R1_permission_rescan_fork_real(self):self.scenario('permission')
                                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/ps5-helper-122/tests/test_118.py", line 17, in scenario
    self.assertEqual(r.returncode,0,r.stderr+r.stdout);v=json.loads(r.stdout);self.assertTrue(v['PASS'])
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : SESSION_TRANSIENT_ERRORS_RECOVERED PID 907391 errno=EPERM: [Errno 1] injected member denial
Traceback (most recent call last):
  File "/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/ps5-helper-122/tests/owned_scenario.py", line 58, in <module>
    assert (message is None)==(case=='esrch'),message
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: None


----------------------------------------------------------------------
Ran 6 tests in 1.161s

FAILED (failures=1)
```

失败原因证据：owned_scenario.py的`assert (message is None)==(case=='esrch')`要求permission场景必须存在错误；实际打印SESSION_TRANSIENT_ERRORS_RECOVERED，随后message为None，符合新N2但不符合旧断言。是否允许按N2更新这一旧契约由PM裁决，本次不自行修改。

其他潜在契约冲突仅静态发现、未运行判定：test_member_runtime_errno_matrix_no_fallback要求最终空扫描后仍抛历史错误；114用例匹配共享deadline中的scan incomplete；110/114用例断言旧成员/进程stat元组形状。未将这些记为本次实际FAIL。

## 探针、H4与远端

既有测试FAIL后，Claude Code probe-120的阅读/执行、本次H4合成/说明核对和sandbox推送均NOT RUN。未把121的“只归档”当作已执行探针。

停止后只读ls-remote：`db7ac04bd2b854b144f6e5c5fcf3a0aa9645c01e	refs/heads/sandbox/lhmax2025/bolt_pgo`，rc=0。未推送；[原文](../../tools/bolt/results/ps5-helper-122/sandbox-read.stdout)。

## 准备修正与证据边界

使用一次准备修正：git worktree add --no-checkout后，sparse-checkout set没有初始化文件；添加read-tree -mu HEAD初始化新工作树。首次AssertionError及diff见[preparation-error.txt](../../tools/bolt/results/ps5-helper-122/preparation-error.txt)、[preparation-fix.diff](../../tools/bolt/results/ps5-helper-122/preparation-fix.diff)。之后无准备重试。测试FAIL不按准备错误处理。

已读：两份120复审全文、H3 helper、118/119/120及相关旧测试、此次测试与自身工作树状态。未读QB、未写Gerrit、未构建RPM/LLVM，未重放归档。停止后仅收尾报告和证据推送。所有工作串行使用4GiB、swap0、CPU200%、Nice19、IO idle用户服务；无资源等待/轮询或放大限制，无OOM。

日志被.gitignore排除或文件超过10MB时只留本地；路径/大小/SHA见[local-only-files.json](../../tools/bolt/results/ps5-helper-122/local-only-files.json)，不因此STOP。[全部测试调用](../../tools/bolt/results/ps5-helper-122/test-invocation.json)、[结果](../../tools/bolt/results/ps5-helper-122/test-results.json)、[六提交](../../tools/bolt/results/ps5-helper-122/work-commits.json)、[最终状态](../../tools/bolt/results/ps5-helper-122/final-state.json)。

已结束 2026-11-17T06:17:24.288332-08:00 D tests STOP


## 123 续做

**结论：STOP，未生成H4、未推sandbox。N2已撤销，保持H3的fail-closed策略；保留新增11/11与118的19/19通过。旧114断言仍要求scan incomplete，与本次保留的中性deadline文本冲突，按规则停止。计划733项，实际40项39通过1失败，剩余693未运行。**

### N2撤销与最终处理清单

在task122-session-review上用git revert撤销`c2e34724e42ed3b1f28aa173e0c345ae29e3b0cc`，得到工作提交`3cdf92b648687f0aa7412318d6be495cf1b1994f`。不输出SESSION_TRANSIENT_ERRORS_RECOVERED；历史检查/清理错误仍导致失败。仅从123测试副本移除122为N2新增的4个测试及其公共方法，122历史文件不删除。

|编号/来源|最终处理|验证状态|
|---|---|---|
|D1 / N4 名称：Codex/Claude|保留scan-time comm，formatter无额外I/O|新增名称及括号测试通过；119原PID:python断言通过|
|N4 长度：Claude|保留最多20个成员和+N more|两项截断测试通过|
|N4 措辞：Claude|保留cleanup/drain两种阶段|两项通过|
|D2 / N1：Codex/Claude|保留中性deadline和member read errors|新kill-pass/部分扫描/EIO/EMFILE测试通过；旧114文字断言FAIL|
|N2：Claude|**策略确认：保持fail-closed，不修改**；撤销122策略提交|118的permission、errno matrix等19项全部通过|
|N3：Claude|保留持续扫描错误约两个预算的注释|不修改预算，无单独计时认证|
|此前R1/R2、R3/L2、L1、EACCES：两份复审|保持H3已接受实现|本次118、119、120套件通过，后续既有套件未完成|
|pidfd进程级EMFILE；不静默降级：Claude|保持已知限制，不增加裸PID回退|本次探针未运行|
|malformed stat GateError、/proc/self读取失败：两份报告|保留fail-closed，不扩展错误类型范围|未新增验证|
|首信号等待响应、setsid逃逸、不可杀死成员、fallback竞争、单操作预算超时：两份报告|保留限制，不声称强隔离或硬实时保证|未新增认证|
|formatter覆盖、真实/mock层次：两份测试章节|保留11项新测试：2混合真实进程、9纯mock|11/11通过，不冒称全为实物测试|
|Python3.9/worker资格、未评审产品范围：复审范围说明|不扩大本次工作，不构建或访问QB|未运行|

[撤销原文](../../tools/bolt/results/ps5-helper-123/revert.stdout)、[移除N2测试diff](../../tools/bolt/results/ps5-helper-123/removed-n2-tests.diff)、[工作状态](../../tools/bolt/results/ps5-helper-123/work-state.json)。其余五项对应122工作提交不变，见上一节六提交表。

### 测试结果与STOP

既有断言未改，旧顶层测试文件逐字节核对见[legacy-test-equality.json](../../tools/bolt/results/ps5-helper-123/legacy-test-equality.json)。全部从头运行，没有沿用122的PASS。

|套件|计划|执行|结果|
|---|---:|---:|---|
|review122-retained|11|11|PASS|
|review120|2|2|PASS|
|review119|6|6|PASS|
|review118|19|19|PASS|
|review114|34|2|1 PASS / 1 FAIL|

新测试中的混合真实进程两项为：名称扫描后退出且无额外I/O、第二信号真实自终止且运行真实formatter；其余9项mock。全部只管理自有进程。

```text
test_cleanup_error_is_failure (__main__.Hardening.test_cleanup_error_is_failure) ... SESSION_KILL_MODE=pidfd
ok
test_deadline_after_empty_scan_fails (__main__.Hardening.test_deadline_after_empty_scan_fails) ... FAIL

======================================================================
FAIL: test_deadline_after_empty_scan_fails (__main__.Hardening.test_deadline_after_empty_scan_fails)
----------------------------------------------------------------------
helper114.SessionDeadlineError: session deadline expired; last observed members: 

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/ps5-helper-123/tests/test_114.py", line 241, in test_deadline_after_empty_scan_fails
    with self.assertRaisesRegex(h.GateError,'scan incomplete'):h.live_session_members(42,1)
AssertionError: "scan incomplete" does not match "session deadline expired; last observed members: "

----------------------------------------------------------------------
Ran 2 tests in 0.080s

FAILED (failures=1)
```

`session_deadline()`按PM要求去掉scan incomplete，但未修改的114测试仍以该词匹配。异常类型仍为SessionDeadlineError，测试因文字匹配失败。未修断言、未继续运行；其余693项（含114剩余32项、其后套件）未运行。是否更新这项旧诊断契约需PM裁决。

### H4、探针与sandbox

H4未生成。工作末端`3cdf92b648687f0aa7412318d6be495cf1b1994f`仅为撤销N2后的未认证工作链。H3→工作差异`19	15	packaging/clang-bolt-helper.py`，仅helper，不能称为已认证H3→H4差异。

测试FAIL后，probe-120阅读/运行、H4合成与sandbox推送均NOT RUN。停止后只读sandbox：`db7ac04bd2b854b144f6e5c5fcf3a0aa9645c01e	refs/heads/sandbox/lhmax2025/bolt_pgo`，查询rc=0。没有Gerrit写操作、没有refs/for。

[未认证helper.diff](../../tools/bolt/results/ps5-helper-123/helper.diff)、[STOP原文](../../tools/bolt/results/ps5-helper-123/STOP.txt)、[测试调用](../../tools/bolt/results/ps5-helper-123/test-invocation.json)、[测试结果](../../tools/bolt/results/ps5-helper-123/test-results.json)、[sandbox原文](../../tools/bolt/results/ps5-helper-123/sandbox-read.stdout)。

### 资源与归档

串行用户服务4GiB/swap0/CPU200%/Nice19/IO idle；无准入等待或资源轮询，无OOM，无准备错误修正。未碰120-N编排脚本、另一项目目录/进程/锁，未构建、未访问QB。本轮读取122工作提交及测试、H3差异和停止结果；两份复审依据122已全文读取的原文，处理清单如上。

日志受gitignore排除或文件超过10MB时仅留本地，其路径/大小/SHA见[local-only-files.json](../../tools/bolt/results/ps5-helper-123/local-only-files.json)，不因此停止。

已结束 2026-11-17T07:08:23.852586-08:00 D tests STOP


## 124 续做

**结论：STOP。首轮完整覆盖735项，724通过、11项失败/错误。分类(a)0项、(b)1项、(c)10项；(c)是proc_stat/成员元组接口与旧夹具不兼容，超出文字修改授权，故不修改断言、不运行第二轮、不生成H4、不推sandbox。所有套件均已跑至结束。**

### 阶段实现与未认证工作链

`session_deadline(deadline, members, *, phase='scan')`：扫描调用保留`session deadline expired; scan incomplete; last observed members: ...`；kill_session_member及wait_session_exit逐成员发信号前的调用显式传入`phase='signalling'`，输出`session deadline expired while signalling; last observed members: ...`。扫描中断时仍由wait_session_exit附final scan incomplete，完整扫描后的signal阶段不附。

工作提交`5c6d9a2951840220a41fc9891cec1731ab7bcf66`，tree `0a92c37b67f8d169590a11c7b51f8a5276101d62`，基于123工作分支继续，不是H4。H3→当前工作仅helper **+26/-20**（增删46行），spec与其他文件未改。[本次phase diff](../../tools/bolt/results/ps5-helper-124/phase-implementation.diff)、[未认证helper.diff](../../tools/bolt/results/ps5-helper-124/helper.diff)。

### 首轮全部结果及采集修正

计划735＝722既有＋122保留11＋124新增2。本次2个新增阶段测试全部通过。新增部分合计13项：2项混合真实自有进程测试、11项纯mock；结果12通过、1项新测试文字断言失败。

|套件|计划|完成|FAIL|ERROR|结论|
|---|---:|---:|---:|---:|---|
|review124|2|2|0|0|PASS|
|review122-retained|11|11|1|0|FAIL|
|review120|2|2|0|0|PASS|
|review119|6|6|0|0|PASS|
|review118|19|19|0|0|PASS|
|review114|34|34|0|2|FAIL|
|policy|46|46|0|0|PASS|
|release|5|5|0|0|PASS|
|r2|12|12|0|0|PASS|
|r3-r4-r5|40|40|0|0|PASS|
|hardening|16|16|0|0|PASS|
|review-r11|19|19|0|0|PASS|
|helper|393|393|0|2|FAIL|
|targeted|30|30|0|0|PASS|
|N1|6|6|0|0|PASS|
|regression109|45|45|0|0|PASS|
|sessions110|35|35|1|5|FAIL|
|P1-P2-S2|14|14|0|0|PASS|

一次准备修正：首个采集器只覆盖unittest.TextTestRunner，unittest.main经unittest.runner.TextTestRunner绕过了它，导致122保留套件首次只跑2项。其他套件继续到结束后，将两个入口统一为不fail-fast的采集器，仅完整补跑该11项套件；首次2项输出不覆盖。首轮唯一用例735，实际执行次数737（2项重复），未将补齐11项冒称第二轮全套。部分原本全部通过的unittest.main套件没有独立details.json，按完整.log中的Ran/OK计数。

[采集器diff](../../tools/bolt/results/ps5-helper-124/runner-collect-all.diff)、[首次问题](../../tools/bolt/results/ps5-helper-124/preparation-error.txt)、[修正diff](../../tools/bolt/results/ps5-helper-124/preparation-fix.diff)、[补齐原文结果](../../tools/bolt/results/ps5-helper-124/run1-completion/details.json)、[首轮汇总](../../tools/bolt/results/ps5-helper-124/first-run-summary.json)。

### 全部失败分类与断言清单

(a)既有文字断言：0个实际失败。123停止的test_deadline_after_empty_scan_fails本次扫描文字保留后已通过。

(b)122新用例1项：test_complete_scan_signal_deadline_entire_message第42行仍匹配`errors: session deadline expired;`，本次真实异常为`errors: session deadline expired while signalling;`。属于允许的新测试文字适配，但由于同时存在(c)，本次未应用修改。

(c)10项：9个ERROR为`ValueError: not enough values to unpack (expected 7, got 6)`，旧mock proc_stat仍返回6字段；另1个FAIL为真实/proc/self/stat返回带comm的7字段而旧断言要求6字段。涉及成员扫描输入/输出结构，不能仅修改被断言的字符串，按规则STOP。不是已证明的错误进程信号事件；也不能据此宣称新接口已经兼容认证。

|套件|用例|类别|
|---|---|---|
|review122-retained|test_complete_scan_signal_deadline_entire_message (__main__.Review122.test_complete_scan_signal_deadline_entire_message)|b|
|review114|test_deadline_partial_scan_never_empty_success (__main__.Hardening.test_deadline_partial_scan_never_empty_success)|c|
|review114|test_scan_permission_retains_other_members_and_fails (__main__.Hardening.test_scan_permission_retains_other_members_and_fails)|c|
|helper|test_single_zombie (test_second_review.SecondProcessTests.test_single_zombie)|c|
|helper|test_zombie_threads (test_second_review.SecondProcessTests.test_zombie_threads)|c|
|sessions110|test_proc_stat_session_field (__main__.SessionTests.test_proc_stat_session_field)|c|
|sessions110|test_foreign_session_excluded (__main__.SessionTests.test_foreign_session_excluded)|c|
|sessions110|test_session_dead_excluded (__main__.SessionTests.test_session_dead_excluded)|c|
|sessions110|test_session_matches_different_group (__main__.SessionTests.test_session_matches_different_group)|c|
|sessions110|test_session_zombie_excluded (__main__.SessionTests.test_session_zombie_excluded)|c|
|sessions110|test_zombie_leader_live_threads_included (__main__.SessionTests.test_zombie_leader_live_threads_included)|c|

**断言修改清单为空。** 没有修改任何旧/新断言，也没有在分类后修产品代码或重跑。准备时仅更新了外部探针的trace行号坐标以对应当前相同spawn语句、关闭fail-fast、增加结果采集；均有独立diff，场景和断言不变。

[全部失败及分类JSON](../../tools/bolt/results/ps5-helper-124/first-run-failures.json)、[易读清单](../../tools/bolt/results/ps5-helper-124/failure-classification.md)、[全部原始traceback](../../tools/bolt/results/ps5-helper-124/STOP.txt)、[断言清单](../../tools/bolt/results/ps5-helper-124/assertion-changes.json)、[测试源码差异](../../tools/bolt/results/ps5-helper-124/test-source-differences.json)、[trace坐标适配](../../tools/bolt/results/ps5-helper-124/trace-coordinate-adaptation.json)。

### 两份复审全部发现的最终处理

|编号/来源|最终处理|当前证据|
|---|---|---|
|D1 / N4名称（Codex/Claude）|保留stat扫描时comm、snapshot无额外I/O|新名称测试及119的PID:python通过；旧6字段接口有10项未解决，未认证|
|N4长度（Claude）|保留20项上限和+N more|新截断测试通过|
|N4措辞（Claude）|保留cleanup/drain|新两项通过|
|D2 / N1（Codex/Claude）|按本轮PM决定区分scan/signalling；member read errors保留|124新两项通过；122文字断言1项待适配，未修改|
|N2（Claude）|策略确认：保持fail-closed，不修改；不输出SESSION_TRANSIENT_ERRORS_RECOVERED|118全部19项通过|
|N3（Claude）|保留约两个截止预算注释，不改预算|不新增单独耗时认证|
|原R1/R2、R3/L2、L1、EACCES闭合项（两份）|保持H3行为|118/119/120、regression109等通过；不能覆盖未通过接口测试|
|进程级EMFILE、禁止静默fallback（Claude）|已知限制保留|未运行probe-120|
|malformed stat、/proc/self读取失败（两份）|保留fail-closed、未扩大错误恢复范围|未新增认证|
|首取消响应、setsid逃逸、不可杀死成员、fallback竞争、单次内核操作超预算（两份）|保留限制，不声称强隔离或硬实时|未新增资格结论|
|formatter及kill-pass缺口、真实/mock层次（两份测试章节）|新测试覆盖，按证据层次报告|13新增中12通过、1文字断言失败|
|Python3.9、worker pidfd/fallback资格及未审产品范围（两份范围说明）|不扩大本次工作|没有构建、QB或实物重放|

### H4、探针、远端和未运行项

第二轮全套NOT RUN（因(c)立即STOP）；probe-120安全阅读与执行、H4合成/身份验证、sandbox推送均NOT RUN。H4完整SHA不存在。停止后只读sandbox=`db7ac04bd2b854b144f6e5c5fcf3a0aa9645c01e	refs/heads/sandbox/lhmax2025/bolt_pgo`，rc=0。

[最终状态](../../tools/bolt/results/ps5-helper-124/final-state.json)、[远端原文](../../tools/bolt/results/ps5-helper-124/sandbox-read.stdout)。未操作120-N、另一项目目录/进程/锁；未写Gerrit、未推refs/for，未构建LLVM/RPM或访问QB。资源4GiB/swap0/CPU200%/Nice19/IO idle，串行；无准入等待或资源轮询，无OOM。

读取：123实现和测试、122/123已有复审处理记录、本轮全部套件结果、H3差异和sandbox引用。未运行项目如上。所有超10MB/忽略日志仅本地保留，路径、大小和SHA见[local-only-files.json](../../tools/bolt/results/ps5-helper-124/local-only-files.json)，不因此STOP。

已结束 2026-11-17T07:21:21.166304-08:00 first run initial pass completed total=726
已结束 2026-11-17T07:21:37.398701-08:00 first-run completion tests=11


## 125 续做

**结论：PASS。H4 `7a7bc17467d4c5da9763e86e3c74a123b3ff0df2` 已推 sandbox，ls-remote 一致。首轮完整739项：733通过、3 FAIL与3 ERROR，全部为(b)类122新夹具仍把名称放进元组元素；(a)=0、(c)=0。一次授权的新夹具修正后，第二轮从头739/739通过。19项归档探针全部符合预期。本轮无STOP。122–124的停止原文保留。**

### 实现、身份与远端

`_StatTuple(tuple)`不带`__slots__`。`proc_stat()`保留H3的6元素，在同一次stat读取中解析第二字段comm并设置属性；`live_session_members()`返回带comm属性的3元素成员。普通tuple的解包、长度、相等、排序、hash保持兼容。`session_snapshot()`只读属性，无名称时为`?`，不额外读取procfs。

保留：扫描阶段deadline含`scan incomplete`；发信号阶段含`while signalling`且不误报扫描中断；实际中断的扫描仍附`final scan incomplete`；`member read errors`、cleanup/drain、20成员及`+N more`、N3两预算注释。N2为**策略确认：保持fail-closed，不修改**，没有SESSION_TRANSIENT_ERRORS_RECOVERED。

本轮工作提交`77cdadbc7eb788959e2a3ce0ceb7a7ade9ad1f1f`。最终H4是单提交，父`61ef5d31ca91025c414c748477bef0c64ddfa67c`，tree `472c872afe958f464112d22b6304cde006fcbf98`；Change-Id不变，提交说明与H3逐字节相同。H4与测试过的工作树一致；相对H3仅helper **+37/-19（增删56行）**，spec及其他所有文件不变。

[实现diff](../../tools/bolt/results/ps5-helper-125/tuple-attribute.diff)、[H3→H4最终diff](../../tools/bolt/results/ps5-helper-125/helper.diff)、[身份核对](../../tools/bolt/results/ps5-helper-125/candidate.json)、[提交说明](../../tools/bolt/results/ps5-helper-125/h4-message.txt)。

sandbox使用H3 lease：`db7ac04bd2b854b144f6e5c5fcf3a0aa9645c01e` → `7a7bc17467d4c5da9763e86e3c74a123b3ff0df2`。完整地址`ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm`，ref `refs/heads/sandbox/lhmax2025/bolt_pgo`；SSH BatchMode，推送一次成功，未推refs/for。远端提示继承的标题超过50字符；按本任务要求不改H3说明，未拒绝推送。

[推送命令](../../tools/bolt/results/ps5-helper-125/sandbox-push.command)、[远端原文](../../tools/bolt/results/ps5-helper-125/sandbox-push.stderr)、[之前](../../tools/bolt/results/ps5-helper-125/sandbox-before.stdout)、[之后](../../tools/bolt/results/ps5-helper-125/sandbox-after.stdout)。

### 两轮全套测试、分类与全部断言修改

739＝722既有＋122保留11＋124新增2＋125新增4。每轮所有套件都跑完，没有遇到首个失败就停止，没有复用先前PASS。全部既有722项的断言保持原样；外部trace探针只随源码行号调整坐标，场景和断言不改。

|套件|数量|第一轮|第二轮|
|---|---:|---|---|
|review125|4|PASS|PASS|
|review124|2|PASS|PASS|
|review122-retained|11|5 PASS / 3 FAIL / 3 ERROR|PASS|
|review120|2|PASS|PASS|
|review119|6|PASS|PASS|
|review118|19|PASS|PASS|
|review114|34|PASS|PASS|
|policy|46|PASS|PASS|
|release|5|PASS|PASS|
|r2|12|PASS|PASS|
|r3-r4-r5|40|PASS|PASS|
|hardening|16|PASS|PASS|
|review-r11|19|PASS|PASS|
|helper|393|PASS|PASS|
|targeted|30|PASS|PASS|
|N1|6|PASS|PASS|
|regression109|45|PASS|PASS|
|sessions110|35|PASS|PASS|
|P1-P2-S2|14|PASS|PASS|

第一轮6项均在122新测试：
- `test_real_scan_names_survive_exit_without_comm_reads`仍读取member[3]，IndexError；改读member.comm，仍验证扫描后进程退出、名称保留且无额外I/O。
- `test_stat_name_parentheses`仍把最后元素当名称；改读v.comm，括号名称期望不变。
- `test_member_read_eio_continues`、`test_member_read_emfile_continues`模拟7元素stat，导致解包错误；改为6元素附comm属性。成员仍核对相同PID/state/starttime，并单独核对comm，PID/errno断言不变。
- `test_snapshot_twenty_limit`、`test_deadline_member_list_twenty_limit`模拟4元素成员；改为3元素附comm属性，20条与+5 more的断言不变。

一次新夹具纠正同时更新这些测试共用的deadline成员工厂，使用同样属性契约；无产品代码修正。交付阶段有一次准备脚本修正，见下文。125新增4项覆盖6/3元素解包与普通tuple相等、属性、sort/hash、普通tuple的`?`及无额外I/O。保留/新增17项中4项真实或混合自有进程/procfs、13项mock/合成（4:13）；探针另计，不合并为测试总数。

另有**运行前PM已明确授权**的122文字断言1处：`test_complete_scan_signal_deadline_entire_message`原第42行 `errors: session deadline expired;` → `errors: session deadline expired while signalling;`，原因是完整扫描后的发信号阶段；另外两个not-in断言未改。所有断言和夹具变更的旧/新行号及原文均见下列JSON/diff；没有修改118之前的断言，也未修改119的PID:python断言。

[首轮汇总](../../tools/bolt/results/ps5-helper-125/first-run-summary.json)、[全部失败及分类](../../tools/bolt/results/ps5-helper-125/first-run-failures.json)、[traceback原文](../../tools/bolt/results/ps5-helper-125/first-run-failures.txt)、[第二轮结果](../../tools/bolt/results/ps5-helper-125/run2/test-results.json)、[第二轮失败清单（空）](../../tools/bolt/results/ps5-helper-125/run2/failure-list.json)、[断言及夹具逐处清单](../../tools/bolt/results/ps5-helper-125/assertion-and-fixture-changes.json)、[授权文字diff](../../tools/bolt/results/ps5-helper-125/authorized-text-assertion.diff)、[一次新夹具修正diff](../../tools/bolt/results/ps5-helper-125/new-fixture-correction.diff)、[测试源码差异](../../tools/bolt/results/ps5-helper-125/test-source-differences.json)、[trace坐标](../../tools/bolt/results/ps5-helper-125/trace-coordinate-adaptation.json)、[真实/mock口径](../../tools/bolt/results/ps5-helper-125/test-kinds.json)。

### 探针

完整阅读归档probe-120的harness.py与runner.py：harness作为subreaper，只通过持有的Popen发信号，并用pidfd清理其自身未回收子进程；helper只操作自己启动的session。原样复制脚本，用74号只读根的loader运行ninja 1.13.1；Ninja仅执行sleep/shell测试，不构建产品。

按归档results.jsonl中实际登记的19个场景逐一执行，19/19符合基线的结果类别、退出码、信号模式、SIGCHLD恢复及交还harness的残留数。普通/正常取消/超时场景无残留；6个注入不可杀/EPERM/EMFILE场景各留1个设计内故障成员，由harness用其持有的pidfd清理。transient-scan仍失败，验证N2未采用；persistent-scan仍失败，约两个预算。第二信号和门闩场景符合预期。

复审正文说运行过22个H3探针，但入库results.jsonl仅19条，本次明确只复跑这19条；未冒称22条，也未新增全进程EMFILE探针或H2比较。

[安全审阅](../../tools/bolt/results/ps5-helper-125/probes/ownership-review.json)、[结果原文](../../tools/bolt/results/ps5-helper-125/probes/results.json)、[驱动](../../tools/bolt/results/ps5-helper-125/probes/run_probes.py)、[工具身份](../../tools/bolt/results/ps5-helper-125/probes/tool.json)。

### 两份复审全部发现的最终处理清单

|编号/来源|最终处理|本轮证据|
|---|---|---|
|D1 / N4名称（Codex/Claude）|同次stat扫描取得comm，附加属性，不改6/3元素形状，snapshot无I/O|125新增4项、122名称测试、119原断言与全部旧tuple夹具通过|
|N4长度（Claude）|最多20成员，余数+N more|两项截断测试通过|
|N4措辞（Claude）|kill=True cleanup，kill=False drain|两项测试通过；故障探针记录实际消息|
|D2 / N1（Codex/Claude）|扫描与signalling分别描述；member read errors保留PID/errno|124两阶段＋122全消息/EIO/EMFILE测试通过|
|N2（Claude）|策略确认：保持fail-closed，不修改|原722项通过；transient-scan仍COMMAND_ERROR|
|N3（Claude）|仅注释持续错误约两个截止预算，不改预算|persistent-scan失败，实际时长见探针JSON|
|原R1/R2、R3/L2、L1、EACCES（两份）|保留H3已闭合行为|118/119/120、regression109、110与19探针通过|
|进程级EMFILE、禁止静默fallback（Claude）|保留限制，不增加运行时裸PID回退|单成员故障探针通过；全进程EMFILE未新增运行|
|malformed stat、/proc/self读取失败（两份）|保持fail-closed，不扩展恢复范围|既有套件通过；不声称所有procfs错误可重试|
|首取消等待、setsid逃逸、不可杀死成员、fallback竞争、单内核操作超预算（两份）|限制保留，不声称强隔离/硬实时|仅既有覆盖和本次19探针，不扩大承诺|
|formatter/kill-pass缺口、真实/mock层次（两份测试章节）|真实formatter与阶段测试覆盖，并明确分层|新增/保留17项4:13；全套739项，不冒称均为实物测试|
|Python3.9、实际worker pidfd/fallback资格、未审产品范围|不扩大本任务|未作Python3.9/QB/完整构建认证|

### 资源、读取范围和未运行项

各worker串行systemd用户服务，MemoryMax=4G、MemorySwapMax=0、CPUQuota=200%、Nice19、IOSchedulingClass=idle；无准入等待/资源轮询，无OOM。未操作120-N或另一项目的目录、进程、锁；没有构建LLVM/RPM、访问QB、Gerrit评审写入或refs/for推送。

读取：124工作实现和测试、H3对象、两份120复审全文、19条历史探针结果、探针源码、本轮两轮完整结果、父链/tree/message和sandbox引用。没有读取另一项目材料；未做实物转换重放、完整构建或新QB。

日志被gitignore排除或大于10MB时仅本地保存，路径/大小/SHA见[local-only-files.json](../../tools/bolt/results/ps5-helper-125/local-only-files.json)，不因此STOP。[交付文件清单](../../tools/bolt/results/ps5-helper-125/publication-files.json)。本次STOP原文：无。历史122–124 STOP保持原文。

已结束 2026-11-17T07:58:45.294246-08:00 first full run completed total=739

已结束 2026-11-17T08:02:36.288479-08:00 second full run completed total=739

已结束 2026-11-17T08:05:32.317852-08:00 probes=PASS count=19

已结束 2026-11-17T08:06:45.171033-08:00 sandbox=PASS

交付准备修正一次：全暂存区`git diff --check`错误覆盖原样patch、RPM展开及归档探针，因原有空白返回2；不是产品门禁失败。保留[首次错误](../../tools/bolt/results/ps5-helper-125/preparation-error.txt)及[同一暂存区完整原文](../../tools/bolt/results/ps5-helper-125/preparation-first-check.stdout)，仅将检查限于H3→H4产品diff及新文档，两项通过。原始证据不做空白清洗。[检查修正diff](../../tools/bolt/results/ps5-helper-125/preparation-check-fix.diff)、[修正结果](../../tools/bolt/results/ps5-helper-125/preparation-fix-result.json)。一次授权准备修正已用，无第二次错误；产品、测试、sandbox结果均保持不变。
