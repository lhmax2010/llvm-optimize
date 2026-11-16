> **最新结论（109号续二）：PASS。** 新 sandbox HEAD 为
> 92775bc36de729106b502c4e5967a5af0e4f4033；612/612 测试、8组解析通过。
> 完整结果见 §7；下面首次执行及109号续的 STOP 原文保留，均为历史记录。

# 109：PS5 最终候选准备（STOP，未推送）

**结论：STOP。默认x86_64展开失败，未推sandbox、未生成新的LLVM提交。**
sandbox只读核对仍为a061f4e415a895412516ffe076084f407f2d70a8。
本次新增有效宏采用了平台RPM不支持的expr宏；这是产品spec兼容性失败，
不按准备脚本错误处理，没有改代码后重跑。

| 项目 | 结果 |
|---|---|
| 基底身份 | a061f4e4，tree 8d08d49a1c70ebb06118d8d84734c695e24e6d32，父61ef5d31；原工作树干净 |
| 先行开关设计 | 已保存，再在新独立游离工作树实施 |
| 代码 | 仅llvm.spec开关、helper R1及注释；未提交、未验证通过 |
| 默认x86_64展开 | FAIL：RPM无法解析新增有效宏；基底的展开及nobuild解析rc=0 |
| armv7l/aarch64、总开关关闭、单项组合 | NOT RUN |
| 原567项、R1、评审回归 | NOT RUN，总数/通过数不冒称567；本轮unittest运行0项 |
| 提交说明、sandbox推送、回复更新 | NOT RUN；原FINAL文件不动 |
| 交付 | 保存设计、diff、解析命令与错误、资源及现场；提交bolt-v4 |

## 1. 开关设计与读取范围

[先行设计](../../tools/bolt/results/ps5-final-109-20261116/switch-design.md)在产品编辑之前保存。
读取a061f4e4及父提交61ef5d31的完整llvm.spec、原Part1的spec差异，
[Codex评审](../../tools/bolt/results/review-ps5/codex-review.md)及
[Claude Code评审](../../tools/bolt/results/review-ps5/claude-code-review.md)，
以及helper进程组管理、原测试驱动和已通过的RPM解析工具配置。

Part1全部spec改动：LLVM_LINK_LLVM_DYLIB和CLANG_LINK_CLANG_DYLIB由OFF改ON；
新增TIZEN_HYBRID_LINK=ON、BUILD_SHARED_LIBS=OFF、LLVM_TOOL_LLVM_DRIVER_BUILD=OFF；
构建后驱动NEEDED断言、readelf用途注释。没有Part1的%files或%install清单变化。
父提交没有后三参数，设计关闭时省略它们，保留父提交的两个OFF；
原有LLVM_BUILD_LLVM_DYLIB和CLANG_BUILD_CLANG_DYLIB仍ON。

设计的总开关llvm_speedup和单项hybrid_link均默认开；clang_bolt沿用架构默认。
总开关关时两个有效宏都关，Part3/4不受影响；单独关hybrid_link时BOLT仍开。
依据：父链接方式也让clang静态链接组件，BOLT自身仍强制组件链接，
helper没有要求混合链接开启；这只是源码接入判断，实际组合和产物尚未验证。
安装的AddLLVM.cmake/AddClang.cmake文本仍不同，不声称关闭开关能恢复整个父tree或全部包。

## 2. 未提交实现与R1

[完整diff](../../tools/bolt/results/ps5-final-109-20261116/implementation.diff)仅包含两文件。
新工作树：/home/linhao/Toolchain/development/llvm-optimize/temp/ps5-final-109-20261116/source，
HEAD仍a061f4e4，保留未提交的两文件修改；原105工作树不动。

R1草案在rc==0后调用wait_group_exit(pid,10)，超时存活组错误转换为指定
COMMAND_ERROR并走原kill/wait/reap；其他/proc错误继续保留原诊断。
成功确认后先清_ACTIVE_GROUP再reap。只新增要求的spawn不变量英文注释，
未改H1–H5/N1或转换器。因更早的展开门禁失败，R1没有运行测试，不能称修复已完成。

## 3. 展开失败原文及只读原因核对

```text
error: parse error in expression
error: /home/linhao/Toolchain/development/llvm-optimize/temp/ps5-final-109-20261116/source/packaging/llvm.spec:81: bad %if condition
```

[失败条件](../../tools/bolt/results/ps5-final-109-20261116/failed-condition.txt)：
新增llvm_hybrid_enabled/llvm_bolt_enabled通过expr宏合成；第81行使用后者作为%if。
平台工具为既有Tizen根中通过自身loader运行的RPM 4.14.1。
只读能力核对输出如下（没有重跑产品门禁）：

```text
RPM version 4.14.1
--eval '%{expr:1 && 1}' 的输出仍是：
%{expr:1 && 1}
```

即该RPM未展开expr宏，导致%if接收到非法表达式。
[工具与参数原文](../../tools/bolt/results/ps5-final-109-20261116/rpm-capability-readonly.json)、
[解析脚本](../../tools/bolt/results/ps5-final-109-20261116/parse_switches.py)、
[STOP](../../tools/bolt/results/ps5-final-109-20261116/STOP.txt)。
脚本在第一份候选展开时立即退出，后续五项/组合比较均未执行。
没有使用准备错误修正机会来放宽或重跑这个产品失败。

## 4. 回归材料与延后清单

用户提供的两个探针目录均存在，已只读确认及阅读说明，尚未复制、适配或运行：
- /tmp/claude-1000/-home-linhao-Toolchain-development-llvm-optimize/5e8aa240-5caa-4416-a0c4-218f8c1eb336/scratchpad/r13/probe/
- /tmp/codex-review-ps5-05g9bu2m/

按PM D3延后且未改：嵌套信号R2；SystemExit/KeyboardInterrupt重新抛出前记录cleanup错误。
567既有项不能沿用为本轮通过，R1四类场景、信号发布窗口、Popen失败、
SIGCHLD四类状态和评审探针均待运行。未创建累计候选提交、未改提交说明或Q6/H1/H2最终回复。
没有访问QB/Gerrit评论API，没有构建RPM或LLVM目标，没有推refs/for或sandbox。
仅只读ls-remote证明sandbox仍a061f4e4。

## 5. 资源与交付

串行systemd用户服务4GiB、swap0、CPU200%、Nice19、IO idle，
MemAvailable低于6GiB停止自身的看门狗已启用，现场未触发；没有OOM。
[资源原文](../../tools/bolt/results/ps5-final-109-20261116/resources.json)、
[结束行](../../tools/bolt/results/ps5-final-109-20261116/ended.txt)、
[全部证据索引](../../tools/bolt/results/ps5-final-109-20261116/RAW_LINKS.md)。

本次只读核对失败原因后停止，没有修正产品、没有重跑。

## 6. 109号续：RPM兼容块已替换，第二次准备错误STOP

PM授权把expr定义替换为明确的0/1派生宏块；已逐字采用，其余产品位置不改。
[授权替换diff](../../tools/bolt/results/ps5-final-109-20261116/resume/rpm414-authorized-fix.diff)、
[八处使用点的x86_64条件核对](../../tools/bolt/results/ps5-final-109-20261116/resume/effective-macro-guards.json)。
设计不变：总开关、两个独立单项，Part3/4不受影响。

默认x86_64候选已能被RPM解析，首次比较仅显示开头新增12个空行，
对应2个bcond与10行派生宏块。原比较脚本未实现PM授权的宏块例外，因此使用本次一次准备修正：
仅拟匹配12个新增前导换行，之后仍逐字节比较；不做全局空白归一化。
原错误与修正diff均保存，新结果写parse-rerun，没有覆盖parse中的首轮结果。

但修正脚本把换行写成了字面反斜杠+n，第二次比较再次误报相同的12个空行。
这是我的第二次准备错误，不是新产品差异。按PM规则立即STOP，未修正、未重跑。
[错误代码与原文](../../tools/bolt/results/ps5-final-109-20261116/resume/second-preparation-STOP.txt)、
[准备修正diff](../../tools/bolt/results/ps5-final-109-20261116/resume/preparation-fix.diff)。

当前状态：默认展开比较未完成；ARM、关闭总开关与父cmake参数比较、单项组合、五项解析、
567项+R1+评审回归均未完成/未运行（本续跑unittest 0项）。未生成新LLVM提交，
原a061f4e4工作树未改，新独立工作树保留未提交修改；未推sandbox，未更新回复文件。
只读远端结果见sandbox-readonly.stdout，仍a061f4e415a895412516ffe076084f407f2d70a8。
没有Gerrit写入、构建、QB访问或对另一项目的操作。只保全现场和交付停止报告。


## 7. 109号续二：PM裁决后的完整验证与推送（PASS）

### 7.1 裁决、比较规则和结果

PM已核对resume/parse/default-x86_64.diff，原始差异只有新增12个空行，
来自RPM 4.14派生宏块，属于允许的定义块差异；default-x86_64判PASS。
本次按授权用真实换行符（chr(10)，等价于换行字符）移除两侧前导连续空行，
单独记录数量，再逐字节比较正文。只允许新增宏块带来的0–12行，不全局去空白。
基底原本已有38行，候选50行，三架构均新增12行；不是把已有38行算作新差异。
本次没有再次修改产品宏块或放宽产品判定，没有新的准备错误。

- [PM原文记录](../../tools/bolt/results/ps5-final-109-20261116/resume2/PM-ruling.txt)
- [授权的脚本修正diff](../../tools/bolt/results/ps5-final-109-20261116/resume2/PM-authorized-parser-fix.diff)
- [解析与比较脚本](../../tools/bolt/results/ps5-final-109-20261116/resume2/parse_switches.py)
- [8组结果](../../tools/bolt/results/ps5-final-109-20261116/resume2/parse-result.json)

| 展开配置 | 结果与证据边界 |
|---|---|
| 默认x86_64 | PASS；原始展开仅多12个前导空行，正文逐字节相同 |
| 默认armv7l | PASS；原始展开仅多12个前导空行，正文逐字节相同 |
| 默认aarch64 | PASS；原始展开仅多12个前导空行，正文逐字节相同 |
| llvm_speedup关闭 | PASS；混合链接/BOLT均关，主cmake argv与61ef5d31逐项相同 |
| 仅hybrid_link关闭 | PASS；混合链接关、BOLT开，主cmake argv与父提交逐项相同 |
| 仅clang_bolt关闭 | PASS；混合链接开、BOLT关 |
| 两单项均关闭 | PASS；两者均关，主cmake argv与父提交逐项相同 |
| 一行bcond回退 | PASS；混合链接开、BOLT关 |

以上8组均通过平台RPM 4.14.1的rpmspec展开与rpmbuild --nobuild解析，
包含原五项（x86开/关、两个ARM、一行bcond回退）及新增组合。
[Source/Patch检查](../../tools/bolt/results/ps5-final-109-20261116/resume2/source-and-patch-parse-check.json)
显示全部Source可定位、native模式Patch数为0，符合105号已裁决的导出模式。
未运行RPM构建或LLVM目标构建。

关闭总开关时，%build相对父提交只保留既有Part3的固定参数逻辑：
去除原sed重写，增加架构/调试序列分类和固定CFLAGS/CXXFLAGS，
固定LDFLAGS、NORMALIZED/DROPPED/WARNING日志及export。
主cmake参数无差异；BOLT段和混合链接驱动断言不存在。
[完整%build差异](../../tools/bolt/results/ps5-final-109-20261116/resume2/total-off-vs-parent-build.diff)逐行保留。
Part4转换器文件未改；关闭开关不关闭Part3/4。
安装的AddLLVM/AddClang文本仍不同，不能将开关关闭称为整个父tree恢复。
“BOLT开、混合链接关”本次证明到源码接入和展开；实际构建/产物仍需后续验证。

### 7.2 R1、回归与全量测试

原567项全部重新运行，没有沿用105号的通过结果：

| 套件 | 通过/总数 |
|---|---:|
| 转换器/policy/release/r2/r3/r4/r5/加固/r11 | 138/138 |
| helper既有 | 393/393 |
| HQ H1–H5定向 | 30/30 |
| N1 | 6/6 |
| 新R1与评审回归 | 45/45 |
| 合计 | **612/612** |

138项内部为policy46、release5、r2 12、选定r3/r4/r5 40、加固16、r11 19。
[567结果](../../tools/bolt/results/ps5-final-109-20261116/resume2/test-results.json)、
[45项完整输出](../../tools/bolt/results/ps5-final-109-20261116/resume2/regression109-output.txt)、
[新增夹具](../../tools/bolt/results/ps5-final-109-20261116/resume2/tests/test_109_regressions.py)。

R1四项全部PASS：成功父进程留下长期存活后代时约10.11秒后报指定
COMMAND_ERROR、杀组并回收；短期后代约2.46秒退出时成功；
普通成功先清_ACTIVE_GROUP再reap；/proc读取失败保留原诊断并清理。
其余41项覆盖spawn窗口、发布前两次信号、Popen异常有/无暂存信号、
SIGCHLD四种状态、各退出路径和子进程信号掩码。

两份评审的原探针目录都存在，原脚本按SHA复制保存。
只把源路径、临时输出位置和源码行号断点适配到候选；
Codex旧R1缺陷探针的“成功并留下后代”观察改为断言本任务D2要求的失败及清理，
其差异明确列出，不改567项既有测试的判定。
测试过程保留自己的临时目录，运行时scratch未提交；tests/environment内复制来的历史输入
与历史元数据只是夹具输入，不冒称本轮新证据。

[探针来源](../../tools/bolt/results/ps5-final-109-20261116/resume2/external-inputs.json)、
[全部适配diff](../../tools/bolt/results/ps5-final-109-20261116/resume2/external-adaptations.diff)、
[实际观察输出](../../tools/bolt/results/ps5-final-109-20261116/resume2/external-probe-observed.json)、
[既有测试路径适配](../../tools/bolt/results/ps5-final-109-20261116/resume2/legacy-path-adaptations.diff)。

### 7.3 候选与sandbox

| 项目 | 值 |
|---|---|
| 新单个累积提交 | 92775bc36de729106b502c4e5967a5af0e4f4033 |
| tree | 534550c983f19fee4a89427e18c92533c62854f4 |
| 父提交 | 61ef5d31ca91025c414c748477bef0c64ddfa67c |
| sandbox推送前 | a061f4e415a895412516ffe076084f407f2d70a8 |
| sandbox推送后 | 92775bc36de729106b502c4e5967a5af0e4f4033 |

[最终产品diff](../../tools/bolt/results/ps5-final-109-20261116/resume2/final-product.diff)
只有llvm.spec开关和helper R1/注释；转换器与CMake模块未改。
H1–H5/N1实现保留。提交说明只在Part1/2补开关与R1文字，
单组trailer、最长72列、对外文本门禁通过；工作树干净。
D3两项（嵌套信号R2、SystemExit/KeyboardInterrupt前记录cleanup错误）继续延后，没有实施。

[提交说明diff](../../tools/bolt/results/ps5-final-109-20261116/resume2/commit-message.diff)、
[身份核对](../../tools/bolt/results/ps5-final-109-20261116/resume2/candidate.json)、
[完整推送命令](../../tools/bolt/results/ps5-final-109-20261116/resume2/sandbox-push-command.txt)、
[远端推送原文](../../tools/bolt/results/ps5-final-109-20261116/resume2/sandbox-push.stderr)、
[推送前](../../tools/bolt/results/ps5-final-109-20261116/resume2/sandbox-before.stdout)、
[推送后](../../tools/bolt/results/ps5-final-109-20261116/resume2/sandbox-after.stdout)。

实际远端ref沿用既有记录的refs/heads/sandbox/lhmax2025/bolt_pgo；
按a061f4e4做force-with-lease一次推送，ls-remote确认一致。
服务器提示subject超过50字符，但没有拒绝；任务要求的72列门禁已通过。
未推refs/for，未发布任何Gerrit评论、回复或投票。

### 7.4 回复草稿、资源与读取范围

[新版FINAL回复](../../tools/bolt/results/hq-review-361395/round2/replies/FINAL-replies-for-user.md)
仅更新H1/H2/Q6；[旧版-v1](../../tools/bolt/results/hq-review-361395/round2/replies/FINAL-replies-for-user-v1.md)
逐字保留。H1旧文件实际措辞是“after child cleanup”，按用户要求替换为
“after cleanup (killing the process group if needed and reaping the child)”；
H2追加R1一句；Q6说明总开关、单项及Part3/4保持原因。
[草稿diff](../../tools/bolt/results/ps5-final-109-20261116/resume2/reply-update.diff)、
[对外文本门禁](../../tools/bolt/results/ps5-final-109-20261116/resume2/reply-gate.json)。
全部只是供用户发布的草稿。

本续跑使用task109-resume2-20261116.service，4GiB/swap0/CPU200%/Nice19/idle，
每30秒检查MemAvailable、低于6GiB停止自身。
交付前采样memory.peak=670097408字节，memory.events的max/oom/oom_kill均0；
看门狗未触发。[资源](../../tools/bolt/results/ps5-final-109-20261116/resume2/resources-final.json)。
已读候选/父spec与helper、两份外部评审和探针、既有测试、实际展开与全量新日志、远端sandbox身份。
未访问QB、未进行真实输入转换重放、未构建RPM/LLVM/BOLT、未干预另一项目。
本续跑无新STOP；首次和109号续的STOP原文仍保留在前文及历史证据目录。

步骤3 已结束 2026-11-16T08:13:03.684149-08:00 PASS
步骤4 已结束 2026-11-16T08:16:00.753042-08:00 PASS
步骤5 已结束 2026-11-16T08:16:47.929131-08:00 PASS
