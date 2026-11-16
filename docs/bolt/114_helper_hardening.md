# 114：clang-bolt-helper 会话清理加固

**结论：PASS。最终 695/695 测试通过（既有 661＋新增 34）；H2 已按指定 lease 推送 sandbox，并经 ls-remote 核对。产品仅 helper 改动；spec、转换器及其他文件与 H 逐字节相同。未写 Gerrit 评论、未推 refs/for、未运行完整 LLVM/RPM 构建。**

- H：`378f8d5c94aeadd2a8618d04ad39a531529c726c`
- H2：`b06ee2ac62085748b1b137523582c989ac78184e`
- H2 tree：`02a7036249700830fe90fe24c66e07e08f18edb7`
- 唯一父提交：`61ef5d31ca91025c414c748477bef0c64ddfa67c`，父上仅一个累积提交。
- Change-Id：`I28171720d5bbbf9eaf491cdafc0aee0b43f9cd06`。
- 提交说明与 H 的原始 message **逐字节相同**；没有修改说明行。
- 工作分支 `task114-session-hardening` 有六项提交，随后用最终 tree 和原 message 生成单提交 H2；工作分支保留，候选 ref 为 `task114-ps5-candidate`。测试位于本仓库证据目录，不加入产品 tree。
- H→H2：仅 `packaging/clang-bolt-helper.py`，**+164/-72**（236 行变动）；统一 diff 文件共 **356 行**。

[候选身份](../../tools/bolt/results/ps5-helper-114/candidate.json)、[六个工作提交](../../tools/bolt/results/ps5-helper-114/working-commits.txt)、[helper.diff](../../tools/bolt/results/ps5-helper-114/helper.diff)、[提交说明](../../tools/bolt/results/ps5-helper-114/commit-message.txt)。

## 逐项结果

| 项目 | 结果与行为 |
|---|---|
| 1. F2/C | `session_retired` 在最终 reap 前置位；退役后普通异常路径不再扫描/kill SID，活动 SID 同时清空；仅 returncode 为 None 才重试 reap。已覆盖 waitpid 前、真实 reap 后、metadata 写入三个注入点，另覆盖真实 waitpid 后、returncode 赋值前的窗口。清理失败保留失败；额外防止 `SystemExit(0)` 隐藏清理错误。 |
| 2. F3/B | `_FORCE_EXITING` 只允许一次紧急 kill_session。清理期间再收到信号，跳过扫描并经 finally 恢复该信号默认处置、重发信号；不重启计时。mock 和真实 TERM→HUP 短时序均只进入一次清理。spawn 延迟第二信号契约保留。 |
| 3. F1 | 第一次 spawn 前探测 pidfd 并明确打印模式。成员信号先 pidfd_open，再读 stat 核对 SID，再通过 pidfd 发 SIGKILL，finally 关闭 fd。AttributeError/ENOSYS/EPERM 明确选 fallback-recheck；回退紧邻 os.kill 核对 SID/starttime，并注释仍有最后检查至发送之间的竞争窗口，不等同 pidfd。其他探测错误在 spawn 前失败，运行时不静默降级。 |
| 4. A | 成员 ProcessLookupError/FileNotFoundError 视为已消失；PermissionError 收集后继续处理其他成员，最终失败。扫描权限错误保留已看到的成员供清理，但检查不完整绝不能判空成功。leader killpg 的 PermissionError 也不阻止后续成员处理。 |
| 5. 截止时间 | kill_session、wait、扫描、逐成员信号使用同一个绝对截止时间；逐条目和 pidfd 复核后检查，到期明确报告 scan incomplete。诊断列表标为 last observed members。这是合作式截止时间，不保证单次内核调用或调度延迟能被硬中断。 |
| 6. 清理与边界 | 删除 live_group_members/wait_group_exit，活动变量改为 `_ACTIVE_SESSION`。注释与夹具明确 setsid 逃逸限制；产品未添加 cgroup、subreaper 或对逃逸后代的收容。 |

## 测试与夹具

[最终总表](../../tools/bolt/results/ps5-helper-114/all-tests-summary.json)、[34 项新夹具](../../tools/bolt/results/ps5-helper-114/tests/test_114.py)、[新测试原文](../../tools/bolt/results/ps5-helper-114/new-tests-final.log)、[既有测试最终列表](../../tools/bolt/results/ps5-helper-114/final-results.json)。

| 套件 | 通过/总数 |
|---|---:|
| policy / release | 46/46、5/5 |
| r2 / r3-r4-r5 / hardening / r11 | 12/12、40/40、16/16、19/19 |
| helper | 393/393 |
| H1–H5 / N1 | 30/30、6/6 |
| 109 / 110 / 111 | 45/45、35/35、14/14 |
| 114 新增 | 34/34 |
| 合计 | **695/695** |

初次 661＋32 已通过。最终检查补上 `SystemExit(0)` 与 cleanup 错误组合的非零失败分支，并新增两个夹具；之后重新运行受影响的所有 610 项既有测试和全部 34 项新增测试。policy/release 的 51 项保留本任务已执行结果，其 spec/converter 输入未改变。首次和最终日志都保留，未将两次运行数相加充当测试覆盖数。

测试适配只涉及路径、活动变量名、stat/starttime 元组、同一语句的信号注入行号及诊断文字；[适配完整 diff](../../tools/bolt/results/ps5-helper-114/test-adaptations.diff)与[复制来源 SHA](../../tools/bolt/results/ps5-helper-114/test-copy-manifest.json)保留。

111 的 S2 历史断言仍比较 56902c58→H 的注释变更，不声称本轮 helper AST 未变；其余 13 项检查当前 spec。110 的三个 r14 场景使用原有受控进程树夹具重做短期/长期后代和第二信号验证，不执行全局 pgrep 清理脚本。旧测试框架原有的 subreaper 仅用于回收其自建测试后代，不属于产品实现。

## Claude 探针与本机 pidfd

已完整阅读归档 `adv.py`、`adv2.py`。**原脚本均跳过**：清理阶段按全局 `pgrep -f` 标记取得裸 PID 后 SIGKILL，并未持有测试自有进程身份；不能严格证明只清理测试自身。此外，其 os.kill 注入不能直接验证新 pidfd 信号路径。符合“否则跳过并说明”的要求，没有运行这两个脚本。

[探针处置记录](../../tools/bolt/results/ps5-helper-114/probe-disposition.json)。对应场景由新夹具验证：测试自建其他 session 的过期 PID 被跳过；匹配成员经 pidfd 杀掉；PermissionError 后下一个成员仍处理；紧急清理内重复信号只进入一次。真实进程均由测试持有的 Popen 管理，finally 清理；没有对机器上的任意匹配 PID 发送测试信号。

本机 `uname -r`：`6.17.0-1033-oem`；`os.pidfd_open` 和 `signal.pidfd_send_signal` 均可用，对自身 pidfd 发送 signal 0 的实际探测 PASS。运行 Python 为 3.12；另做 Python 3.9 AST 语法检查，不把它描述为 Python 3.9 实际运行认证。[环境原文](../../tools/bolt/results/ps5-helper-114/environment.json)。

## 范围与三架构默认展开

H2 与 H 的完整 tree diff 只有 helper；spec 的 Git blob 均为 `ce6284ae26e5bca06a9fc1703a4e34ce6f961d5e`。转换器、其他 packaging 文件和 CMake 文件没有差异。

按任务要求，spec 未变，记录 x86_64/armv7l/aarch64 默认展开与 H 相同；证明依据是相同 spec、相同宏输入及 111 号的三份平台 RPM 4.14 展开原文 SHA。本轮没有声称重新执行三份默认展开。111 的 8 组合夹具在本轮再次进行平台 rpmspec 和 rpmbuild --nobuild 检查，它不是实际构建。[核对记录](../../tools/bolt/results/ps5-helper-114/scope-and-default-expansion.json)。

## 资源、准备错误与执行边界

所有执行命令均通过受限 systemd scope，MemoryMax=4294967296、MemorySwapMax=0、CPUQuota=200%；nice=19、IO idle。测试前逐套件检查所有可见 /proc 进程，未发现 gbs/rpmbuild/ninja 或 task102/task-102 活动任务时才启动；无法完整检查也不准入。[准入原文](../../tools/bolt/results/ps5-helper-114/test-admission.jsonl)、[检查器](../../tools/bolt/results/ps5-helper-114/test-admission.py)。未启动完整 LLVM、GBS、RPM 或 Ninja 构建；旧套件的 --nobuild 解析也串行执行。

[测试 scope 采样](../../tools/bolt/results/ps5-helper-114/test-resource-snapshot.json)时 memory.peak=421306368 B，OOM/oom_kill 为 0；这是运行中采样，不冒称整个任务最终峰值。

准备纠正：第一次只读查找把 temp 路径放在 bolt worktree 下，改到主 workspace 后找到，未启动测试；r2 的固定输入 post-expanded.stdout 在最初仅复制 Python/JSON 时漏掉，执行测试前报 FileNotFoundError（该次 r2 为 0 项）。补齐非 Python 固定夹具一次，原失败日志保留，随后 12/12 通过。[r2 纠正记录](../../tools/bolt/results/ps5-helper-114/preparation-correction-r2.json)。归档暂存另有一次准备错误：仓库 *.log 忽略规则使 git add 返回 1；仅对明确清单中的证据使用 git add -f 修正一次，不改忽略规则。[暂存纠正记录](../../tools/bolt/results/ps5-helper-114/preparation-correction-staging.json)。未遇到需要改变用户既定设计的取舍，没有用准备修正放宽测试判据。

## sandbox 交付

只推 `refs/heads/sandbox/lhmax2025/bolt_pgo`，以 H 为 force-with-lease 的旧值；push rc=0，ls-remote=b06ee2ac62085748b1b137523582c989ac78184e。远端只有继承的标题超过 50 字符提示；按要求保留提交说明。没有推 refs/for，也没有发布评论或回复。

[推送命令](../../tools/bolt/results/ps5-helper-114/sandbox-push-command.txt)、[返回原文](../../tools/bolt/results/ps5-helper-114/sandbox-push.stderr)、[推送后 ref](../../tools/bolt/results/ps5-helper-114/sandbox-after.stdout)、[结果](../../tools/bolt/results/ps5-helper-114/sandbox-result.json)。
