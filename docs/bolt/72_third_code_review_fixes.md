# 72. 第三轮代码评审修复（在测试输入检查处停止）

本轮已完成三个本地提交的修改与归并，尚未完成验证。
helper 393 项、两配置展开 12 项和 Tizen RPM 解析 5 项通过；70 号 12 项夹具初始化时，发现本轮输入少了平台 post 展开，已按用户要求停止。
没有继续测试或演练，没有推送 sandbox；本包只供检查当前修改，不能作为通过认证的发布版本。

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

## 3. 已执行检查

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

## 4. 停止原因

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

## 5. 评审包与远端状态

[r4 README](../../patches/rebase-359934-20261109-r4/README.md) 包含三个 format-patch、去 profile 的 0002、九份完整文本、相对 PS10 转换器 diff、相对 7d5e28ca/c7fd5eed 两份 diff、provenance、SHA256SUMS。README 标明**未完成验证，不具备推送条件**。

本轮未操作 Gerrit，也未重新读取远端。sandbox 最后核对的 HEAD 为 c7fd5eed5e35ca335940239cae349a6936f74a7a（70 §10）；359934/357163 的 NEW、359934 PS10/13c3e223 来自 2026-11-09 15:54 +08:00 历史查询，不冒充本轮当前状态。新本地 HEAD 是 fa4f9978c9162d3c6cd2113d0cfe1173f04881c8。

源码工作区干净，旧包与全部现场保留；只向 GitHub bolt-v4 发布文档、证据和明确未认证的材料。

## 6. 结束记录

~~~text
STEP1 已结束 2026-11-09T18:58:21.967853+08:00 status=ok
SERVICE 已结束 2026-11-09T18:59:47+08:00 status=0 unit=llvm-fix-r3-1109-011
SERVICE 已结束 2026-11-09T19:00:00+08:00 status=1 unit=llvm-fix-r3-1109-012
STEP2 已结束 2026-11-09T19:05:08.538170+08:00 status=failed reason=review70_fixture_expected_5_optional_calls_found_4
STEP3 已结束 2026-11-09T19:05:08.538170+08:00 status=not-run reason=step2_failed
STEP5 已结束 2026-11-09T19:05:08.538170+08:00 status=not-run reason=step2_failed
~~~

结论：**仍有问题；源码修改已保留，测试输入检查失败，未演练、未推送 sandbox。**
