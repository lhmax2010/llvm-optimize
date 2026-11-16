# 101号：评审修正、sandbox 推送与本地 PS4 准备

**PASS：sandbox 已为 `121b4c23bcd6a9a30b0e277c30e5dc17af3e8521`；138/138 项测试通过；本地 PS4 `8ec86c3ecb0c03889674ba7490064ff82ba63033` 导出及五项解析通过，未推 Gerrit。** 两者 tree 均为 `8097a7986fd835abc415b8651d0405358c6c22f0`。本次不构建RPM、不重放真实输入、不运行BOLT、不访问QB，未读取或干预另一项目。100号取消，由本任务和102号夜间任务替代。

## 1. 前置、评审原文与 CFLAGS 事实

sandbox 前置与推送紧前复查都为 `b0c1732c08c5a81382f9eeef27ffe1e40c6c47d1`。[前置输出](../../tools/bolt/results/hardening-ps4/review-r11/101/sandbox-before.stdout)。361395 为 NEW/PS3，revision ecb2dec7，共3个PS。相对91号保存的实际 query，新评论原文为：

```text
Patch Set 3: Code-Review+1 Verified+1
```

作者 Lin Hao，timestamp 1794661252；未见新的外部代码评审文字。当前7个评审人保存在[完整原始query](../../tools/bolt/results/hardening-ps4/review-r11/101/gerrit-before.stdout)；旧query没有allReviewers，因此“是否新增评审人”是UNKNOWN，不能把当前名单全部算新增。首份增量脚本误读91号命令元数据JSON而非.stdout，结果作废但保留；修正一次，见[错误与修正](../../tools/bolt/results/hardening-ps4/review-r11/101/preflight-preparation-fix.txt)及[有效增量](../../tools/bolt/results/hardening-ps4/review-r11/101/gerrit-delta-v2.json)。没有重试远端请求。

用户指定的两份评审原样复制到 review-r11，无编辑，两份大小和SHA均符合预期：

| 文件 | 字节 | SHA256 |
|---|---:|---|
| claude-code-review.md | 6358 | b0c0109a1898f2f1fb2d89907d706323a4a23eb9b9dbf55fb812b2a9b7bc3110 |
| codex-review.md | 5918 | 8f0225aad686d2245474b1ee12802a8cd752f41b19463080dd5b014af8da1086 |

转换器 Source1005 在 **%install** 调用（spec L702及其BOLT关闭分支），不是%build。固定参数的 `export CFLAGS CXXFLAGS LDFLAGS` 位于%build L344。74号T原始日志：L294启动%build的rpm-tmp.0iYH0m；L11291结束该脚本；L11292另启%install的rpm-tmp.VSKUrF；L24121调用转换器。%install调用前同脚本没有 `+ CFLAGS=`、`+ CXXFLAGS=` 或相应export行；只有AR/RANLIB及CC/CXX等导出，不能捏造用户所要求的CFLAGS导出佐证。

平台 `usr/lib/rpm/tizen/macros` L229–239显示：%build前导调用set_build_flags；%install前导只用___build_pre等，没有set_build_flags。基础macros L822–847导出RPM_OPT_FLAGS等，不导出CFLAGS/CXXFLAGS。%build子shell的export不能返回给后续%install脚本。若%install实际收到这两个环境变量，只能来自更外层的继承或其他未记录设置；保存材料未记录其进程环境，实际值仍UNKNOWN，不能等同成员IR内记录参数。旧rpm-tmp.VSKUrF已不存在，未运行或重建它。

[spec原文](../../tools/bolt/results/hardening-ps4/review-r11/101/spec-install-call.txt)、[日志前导](../../tools/bolt/results/hardening-ps4/review-r11/101/install-preamble.txt)、[build赋值与install调用](../../tools/bolt/results/hardening-ps4/review-r11/101/build-flags-vs-install-call.txt)、[Tizen宏](../../tools/bolt/results/hardening-ps4/review-r11/101/tizen-install-macro.txt)、[基础宏](../../tools/bolt/results/hardening-ps4/review-r11/101/rpm-preamble-full.txt)。本任务不改spec。

## 2. F1–F5 实现与范围

| 项 | 实现 |
|---|---|
| F1 | SIG_IGN=ignored；SIG_DFL/default_int_handler=default，并说明Python默认SIGINT；None=non-python；其余handler |
| F2 | 仅最终print捕获OSError/ValueError，注释说明可选诊断不可阻止转换；KeyboardInterrupt不捕获 |
| F3 | 未设置变量记null；已设置但没有架构参数记[]；解析错误仍只记录parse_error |
| F4 | 未使用的reserved改为_reserved |
| F5 | inherited的续行常规对齐；吸收99号原工作树已有的单行空白修改 |

[相对b0的完整diff](../../tools/bolt/results/hardening-ps4/review-r11/101/hardening-vs-b0.diff)。自动核对除log_startup_context和未使用变量改名外，文件其余文本完全相同；压缩节头、零宽、RELR三项逻辑不变。没有改helper或spec。延后：SHF_COMPRESSED+SHF_ALLOC、Android packed relocation、阻塞信号、ch_size、--help也打印；未扩大范围。

## 3. 全量测试

| 套件 | 通过/总数 |
|---|---:|
| 参数/转换器policy | 46/46 |
| release | 5/5 |
| r2 | 12/12 |
| r3/r4/r5 | 40/40 |
| 96号加固 | 16/16 |
| 本轮新增 | 19/19 |
| 合计 | **138/138** |

原119项全部重跑。本轮新增覆盖压缩类型1/2、对齐0/1/8、未知类型/3/截断拒绝；两字节TLSDESC call位于limit-2接受、limit/更远/空节拒绝，NONE保持；非零宽度恰好结束接受、越界1拒绝；空RELR拒绝；普通SIGINT/ignored/non-python/null、写失败/flush失败/关闭流、KeyboardInterrupt传播。压缩及多偏移使用subTest，不虚增测试总数。

PM授权修正96号 test_startup_all_signal_states 的unset期望为None/None；原因“PM裁决F1/F3改变了该诊断的输出约定”。除此之外现有测试不改。该旧测试无default_int_handler断言。[测试diff](../../tools/bolt/results/hardening-ps4/review-r11/101/test_hardening.diff)、[说明](../../tools/bolt/results/hardening-ps4/review-r11/101/test-adjustment-reason.md)、[新测试](../../tools/bolt/results/hardening-ps4/review-r11/101/test_review_r11.py)、[原103项副本SHA](../../tools/bolt/results/hardening-ps4/review-r11/101/test-provenance.json)。沿用96号已限定的40项R3/R4/R5选择，不纳入早已排除的旧三提交身份夹具test_messages。

已知 test_process_states_at_run_return 本次直接通过，重跑次数0。准备错误修正只发生在步骤1的query文件读取，测试过程无修正/失败。[结果](../../tools/bolt/results/hardening-ps4/review-r11/101/test-results.json)；全部原文：[policy](../../tools/bolt/results/hardening-ps4/review-r11/101/policy.log)、[release](../../tools/bolt/results/hardening-ps4/review-r11/101/release.log)、[r2](../../tools/bolt/results/hardening-ps4/review-r11/101/r2.log)、[r3/r4/r5](../../tools/bolt/results/hardening-ps4/review-r11/101/r3-r4-r5.log)、[加固](../../tools/bolt/results/hardening-ps4/review-r11/101/hardening.log)、[新增](../../tools/bolt/results/hardening-ps4/review-r11/101/review-r11.log)。小夹具是既有测试的一部分，没有运行RPM构建或真实输入重放。

## 4. 提交与 sandbox

加固提交：`121b4c23bcd6a9a30b0e277c30e5dc17af3e8521`，父ecb2dec7；作者Hao Lin，保留原作者日期；提交说明沿用并在日志句加入“output failures are ignored”，无Change-Id。独立detached工作树干净，其他分支/工作树未改。[提交身份](../../tools/bolt/results/hardening-ps4/review-r11/101/hardening-commit.json)、[说明](../../tools/bolt/results/hardening-ps4/review-r11/101/hardening-message.txt)。

用户本次指定的短ref模板按81/96实际记录解析为LLVM仓库的完整 `refs/heads/sandbox/lhmax2025/bolt_pgo`。所有Gerrit连接使用BatchMode，推送只有这一条（额外git -c参数仅设置身份及禁用自动gc）：

```sh
git -c user.name="Hao Lin" -c user.email=hao.lin@samsung.com -c gc.auto=0 push --force-with-lease=refs/heads/sandbox/lhmax2025/bolt_pgo:b0c1732c08c5a81382f9eeef27ffe1e40c6c47d1 ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm 121b4c23bcd6a9a30b0e277c30e5dc17af3e8521:refs/heads/sandbox/lhmax2025/bolt_pgo
```

推送前后：b0c1732c → 121b4c23bcd6a9a30b0e277c30e5dc17af3e8521。[命令](../../tools/bolt/results/hardening-ps4/review-r11/101/sandbox-push.command.json)、[远端返回](../../tools/bolt/results/hardening-ps4/review-r11/101/sandbox-push.stderr)、[后置ls-remote](../../tools/bolt/results/hardening-ps4/review-r11/101/sandbox-after.stdout)。成功后已立即在会话报告新SHA，未推refs/for、未发布Gerrit文本/评分/改评审人。

## 5. PS4 仅本地准备

PS4 `8ec86c3ecb0c03889674ba7490064ff82ba63033`，父13c3e223，tree `8097a7986fd835abc415b8651d0405358c6c22f0`，作者/作者日期沿用PS3；一组Signed-off-by然后Change-Id I28171720d5bbbf9eaf491cdafc0aee0b43f9cd06。PS3正文保持，新增Part4，总述补一句。逐行≤72列，ASCII/禁词门禁通过。

[完整PS4说明](../../tools/bolt/results/hardening-ps4/review-r11/101/PS4-message.txt)、[Part4](../../tools/bolt/results/hardening-ps4/review-r11/101/part4-message.txt)、[身份与diff核对](../../tools/bolt/results/hardening-ps4/review-r11/101/PS4-identity.json)、[相对PS3代码diff](../../tools/bolt/results/hardening-ps4/review-r11/101/PS4-vs-PS3.diff)。`git diff ecb2dec7 PS4` 与相对新加固提交的diff逐字相同。12,742,734字节完整format-patch超过10MB交付线，仅本地保留，路径/大小/SHA见[登记](../../tools/bolt/results/hardening-ps4/review-r11/101/local-only-artifact.json)。没有上传PS4。

PS4与新加固提交各一次实际gbs export（新目录W/temp/review-r11-101-exports）；21文件中18完全相同，其余两份spec和0008恰为90号三类固定例外。0008从首个diff --git到末尾完全一致；没有新白名单。[逐文件比较](../../tools/bolt/results/hardening-ps4/review-r11/101/PS4-comparison.json)、[两次导出命令](../../tools/bolt/results/hardening-ps4/review-r11/101/PS4-export.json)。

x86_64 BOLT开/关、armv7l、aarch64、一行bcond回退五个配对场景：平台rpmbuild --nobuild解析及rpmspec展开均通过（合计10次解析、10次展开）；Patch0–7全可见，规范化允许的身份/路径/Patch7后五份diff为空。[五项结果](../../tools/bolt/results/hardening-ps4/review-r11/101/PS4-five-parse-summary.json)、[脚本](../../tools/bolt/results/hardening-ps4/review-r11/101/export_parse.py)、[相对90号脚本diff](../../tools/bolt/results/hardening-ps4/review-r11/101/export_parse-vs-90.diff)。历史平台根只读，未执行prep/build。

## 6. 资源、边界与结束

前置、测试、sandbox推送、PS4、交付分别是串行systemd用户服务；4GiB、swap0、CPU200%、Nice19、IO idle。每30秒监视MemAvailable，低于6GiB停止自己的服务；未触发。测试峰766,377,984B；PS4导出/比较峰4,294,967,296B（含文件缓存），memory.events max=424，oom/oom_kill/oom_group_kill均0，未提高限制或重跑。[测试资源](../../tools/bolt/results/hardening-ps4/review-r11/101/tests-resources.txt)、[导出资源](../../tools/bolt/results/hardening-ps4/review-r11/101/ps4-resources.txt)。

已读：两份评审原文、96/99测试与停点、90号导出解析规则、当前converter/spec、74号T保存日志和平台宏、361395只读返回、sandbox前后SHA。未读QB网站、未作Gerrit写操作、未接触另一项目目录/锁/进程。没有运行新的真实转换重放；99号b0实物通过是旧tree证据，不冒称本次新tree已重放。夜间102另行安排。

全部STOP/远端拒绝：**无**。步骤1首次增量查询分析错误及作废结果已保留，不是产品FAIL。

```text
101步骤1 已结束 2026-11-16T00:55:38.610779-08:00 status=PASS
101步骤2 已结束 2026-11-16T00:59:12.299974-08:00 status=PASS tests=138/138
101步骤3 已结束 2026-11-16T00:59:54.788821-08:00 status=PASS
101步骤4 已结束 2026-11-16T01:02:37-08:00 status=PASS
```

[raw链接索引](../../tools/bolt/results/hardening-ps4/review-r11/101/RAW_LINKS.md)。
