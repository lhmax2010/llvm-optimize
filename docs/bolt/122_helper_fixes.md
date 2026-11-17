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
