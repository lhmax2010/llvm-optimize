# 118 D：helper 修正（STOP，未生成H3、未推sandbox）

结论：六项修改已分别提交至独立工作分支；新19项和114的34项通过。完整重跑执行624项，623通过、1失败，剩余90项未执行。门禁未满足，停止D，不改代码或断言继续重跑。没有生成H3，没有查询或推送sandbox。

基底H2为 b06ee2ac62085748b1b137523582c989ac78184e，tree 02a7036249700830fe90fe24c66e07e08f18edb7，父61ef5d31ca91025c414c748477bef0c64ddfa67c。工作树W/temp/ps5-helper-118/source，分支task118-session-review。只改helper；spec和其他文件未改。工作末端不是已认证H3。

## 两份评审全部发现与处置

|发现|来源|处理/边界|工作提交|验证|
|---|---|---|---|---|
|R1/A：错误后仅扫一遍|Claude R1、Codex部分关闭评价|错误跨轮聚合，完整空扫描或截止才结束，处理清理中新fork，最终仍失败|e1ce9bf9|真实进程+EPERM注入和清理时fork通过|
|R2：运行时OSError中断|Claude R2、Codex§2|ESRCH/ENOENT视为消失，其余PID/errno汇总并重试，不降级；畸形stat的GateError也聚合|1c933cc7|EMFILE/ENOMEM真实进程注入、ESRCH竞态及errno矩阵通过|
|R3/L2：快照丢失、误称存活|Claude R3、Codex L2|保留完整扫描PID/comm快照，仅用于诊断；不完整扫描用could not verify，完整存活观察用live descendants|703ba8e6|新增诊断测试通过；旧109真实回归前缀断言FAIL|
|L1：退休发布顺序|Codex L1|两条路径先清_ACTIVE_SESSION，再写session_retired|27087bee|真实成功/失败call逐行trace通过|
|EACCES探测|两份建议，PM已采纳|fallback允许EACCES并打印errno，EINVAL仍spawn前失败|d314c011|四种真实隔离seccomp、send-probe fd关闭通过|
|R4/边界措辞|Claude R4、Codex边界说明|cooperative deadline保留；强制退出明确best effort；fallback不保证PID复用安全|9e562a06|代码审阅；不承诺全部后代收容或硬墙钟时限|
|F2/C：reap后清理|两份已关闭|生命周期保留，L1进一步收紧发布顺序|无其他改动|114退休边界通过|
|F3/B：重复信号重启清理|两份已关闭|保留_FORCE_EXITING门闩|不改|114重复信号测试通过；110全套尚未运行|
|F1：pidfd重验、fallback窗口|两份已关闭/限制|打开→SID重验→发送顺序不改；fallback保留窗口说明|不改|114同SID/外SID、fd关闭通过|
|部分扫描当空会话|两份|继续失败关闭，旧快照不参与发信号或判存活|703ba8e6|部分/空/从未观察成员测试通过|
|脆弱时钟测试|两份测试建议|按事件推进模拟时间，补齐遗漏的旧夹具|测试diff|一次准备修正，原文保留|
|真实EPERM成员|两份测试缺口|未改变UID/权限；成员EPERM采用注入、多PGID是真实进程。能力探测另用真实seccomp EPERM|测试|不把注入称为真实权限拒绝|
|setsid逃逸/首信号排空响应|两份已知限制|不扩大设计，原行为保留|不改|114扫描排除通过；110完整生命周期NOT RUN|

完整局部提交SHA见 working-commits.json；完整diff见helper.diff。

## 测试与准备修正

计划714项=695既有+19新增。首轮helper执行340项时失败：旧test_wait_deadline_stubborn按monotonic调用序号给出[0,11]，新增截止检查在扫描前耗尽模拟时间。D2明确要求改为模拟时间驱动，准备时遗漏旧helper/110中的三处。使用本部分唯一一次准备修正，在新retry1目录补齐，产品未改。首次原文见first-test-stop.txt，修正见retry1/preparation-fix.diff。首轮不沿用；第二轮全部从头开始：

|套件|已执行/计划|结果|
|---|---:|---|
|review118|19/19|PASS|
|review114|34/34|PASS|
|policy|46/46|PASS|
|release|5/5|PASS|
|r2|12/12|PASS|
|r3-r4-r5|40/40|PASS|
|hardening|16/16|PASS|
|review-r11|19/19|PASS|
|helper|393/393|PASS|
|targeted|30/30|PASS|
|N1|6/6|PASS|
|regression109|4/45|FAIL：3通过、1失败|

新增19项：真实行为5项（26.3%）；真实进程+故障注入/trace混合7项（36.8%）；纯mock7项（36.8%）。涉及真实进程/内核共12/19。逐项标签见retry1/tests/test-118-kinds.json。seccomp仅安装在测试自己的子进程；ENOSYS/EPERM/EACCES/EINVAL实际返回均符合预期。真实清理夹具只通过自己持有的Popen/pidfd收尾。

本机pidfd真实测试通过，SESSION_KILL_MODE=pidfd；QB模式由B另行记录，不用本机代替worker证据。

## 最终 STOP

完整traceback见[retry1/STOP.txt](../../tools/bolt/results/ps5-helper-118/retry1/STOP.txt)。

~~~text
FAIL: test_success_with_live_descendant_fails_and_cleans
AssertionError: "COMMAND_ERROR: command exited successfully with live descendants"
does not match "COMMAND_ERROR: command exited successfully;
could not verify that the session is empty;
last observed snapshot: 672932:python3 (S);
errors: session deadline expired; scan incomplete; last observed members: ..."
~~~

真实回归在新一轮扫描开始时到期。新实现保留上次完整扫描PID/comm，按不完整扫描不得冒称存活的诊断规则报告could not verify；旧回归固定要求with live descendants前缀，形成FAIL。这里只记录触发机制，不自行裁决豁免、不再改测试或产品。需要PM统一诊断规则与这条既有回归。

## 已读和未运行

已读两份完整评审、H2 helper、114测试运行方式和Claude安全探针harness.py/runner.py。探针采用subreaper、自身Popen与pidfd收尾；因套件FAIL，未对修改版本运行，不报告探针PASS。

剩余109回归41项、110会话35项、P1/P2/S2解析14项未运行；H3累积提交、最终message/tree门禁、sandbox查询/推送未执行。未构建RPM、运行BOLT或实物重放、写Gerrit。helper.diff是H2到未认证工作末端，不是已认证H3。

D 已结束 2026-11-16T23:57:17.923381-08:00 status=STOP
