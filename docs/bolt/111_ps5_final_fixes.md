# 111：P1/P2/S2（默认展开差异 STOP，未推sandbox）

**结论：STOP。P2使默认x86_64展开中一条内部空行从python最低版本声明之前移至之后；不符合“除前导空行外逐字节相同”的门禁。按PM要求逐行保留，不自行豁免、修正或重跑。**

sandbox前后只读核对均为92775bc36de729106b502c4e5967a5af0e4f4033。本任务未推sandbox、未写Gerrit、未生成新的LLVM候选提交。

| 步骤 | 状态 |
|---|---|
| 基底 | 56902c58ba8fc2d3a4216e69ed3acb3d2cb6f8a3，父61ef5d31，原工作树干净 |
| 补全110号 | DONE；仅照录原647/647、8组解析及session观察，未因补文档重跑测试；原STOP记录保留 |
| P1/P2/S2 | 已在新独立游离工作树修改，未提交；S2的Python AST与基底完全相同 |
| 默认x86_64 | FAIL；前导38→50行属允许范围，但还有一处内部空行位置变化 |
| 默认ARM、其余7组/五项完整解析 | NOT RUN（第一组门禁即停止） |
| 647项及P1/P2新增测试 | NOT RUN，本轮unittest总数0/通过0；不沿用110号647/647作本轮结果 |
| 新候选/推sandbox/Q6新版 | NOT RUN；原FINAL文件没有改动，无新Q6草稿 |
| 资源 | 峰值462139392 B，无OOM，看门狗未触发；准备错误修正使用0次 |

## 1. 三项修改与范围

新工作树：W/temp/ps5-final-111-20261116/source；HEAD仍为56902c58。
原110工作树不改，新工作树保留两文件未提交修改。

P1在x86_64的hybrid关闭分支、原LLVM/Clang两个OFF参数之前增加：

    -DTIZEN_HYBRID_LINK=OFF
    -UBUILD_SHARED_LIBS
    -ULLVM_TOOL_LLVM_DRIVER_BUILD

三行在真实spec中保留续行反斜杠。P2把python3 >= 3.9移到BOLT条件外、
x86_64条件内；xz/elfutils仍在BOLT条件内。S2仅把SIG_IGN注释改为
“an inherited SIG_IGN can otherwise discard exit status and defeat reliable failure reporting.”
对应措辞分两行，未改运行逻辑。

[产品diff](../../tools/bolt/results/ps5-final-111-20261116/implementation.diff)、
[范围/AST核对](../../tools/bolt/results/ps5-final-111-20261116/implementation-check.json)、
[现场](../../tools/bolt/results/ps5-final-111-20261116/stopped-state.json)。

## 2. 默认展开停止原文

使用与110号相同的Tizen RPM4.14.1 loader、宏输入和native Source目录。
基准spec从a061f4e4的git对象读取。本轮比较仅允许前导连续空行增加0至12行，
正文逐字节比较；没有去掉内部空行。

结果：基准38个前导空行，候选50个；正文不相同。
python3 >= 3.9仍存在，文字、顺序及依赖含义并未被这个空行变化改变；
但PM已明确要求P2如果产生展开文本差异也必须STOP，因此不按语义相同放行。
下面照录完整diff（第一处为允许的前导空行，第二处为触发STOP的内部差异）：

    --- baseline
    +++ candidate
    @@ -1,3 +1,15 @@
    +
    +
    +
    +
    +
    +
    +
    +
    +
    +
    +
    +
     
     
     
    @@ -74,8 +86,8 @@
     
     BuildRequires: ninja
     
    -
     BuildRequires: python3 >= 3.9
    +
     BuildRequires: xz elfutils
     
     

停止原文：

    RuntimeError: STOP default expansion differs: x86_64

[完整stdout/traceback](../../tools/bolt/results/ps5-final-111-20261116/STOP.txt)、
[原始diff](../../tools/bolt/results/ps5-final-111-20261116/parse/default-x86_64.diff)、
[结果JSON](../../tools/bolt/results/ps5-final-111-20261116/parse-result.json)、
[比较器及PM允许的三参数差异实现](../../tools/bolt/results/ps5-final-111-20261116/parse_switches.py)、
[比较器适配diff](../../tools/bolt/results/ps5-final-111-20261116/parser-adaptation.diff)。

候选x86_64的rpmspec展开、rpmbuild --nobuild解析以及显式post宏检查本身返回0；
停止发生在与a061f4e4的字节比较。由于按顺序立即停止，ARM、开关组合、
父cmake参数差异、新依赖场景和完整测试都没有继续。不能据此声称它们通过。
没有把本次门禁失败当成准备错误，也没有使用一次准备修正机会来放宽规则。

## 3. 110号报告补全与延后

[110号报告文末](110_session_tracking.md)已补充逐项测试对照、session身份与
时间限制、setsid边界、r14复用方式、F4真正的宏检查、测试适配范围和验证边界。
[照录来源记录](../../tools/bolt/results/ps5-final-111-20261116/110-report-completion.json)。
110号原来的两次准备错误及STOP文字全部保留；没有更改原结果文件。

本次依用户裁决仍延后：排空等待期间对第一个信号的更快响应；
hybrid关闭、BOLT开启组合的实际构建认证。其他110号已登记的范围外建议仍不改。
Q6新回复和提交说明均未生成；原FINAL文件保持不变。

## 4. 边界、资源与交付

已读STATUS、109/110现有报告及测试/解析证据、两份已归档PS5-final评审的相关意见，
基底helper/spec、候选spec展开与diff；只读查询sandbox身份。
未访问QB、未进行Gerrit写操作、未推sandbox、未运行RPM/LLVM目标构建或BOLT，
未进行647项回归或真实输入重放。没有删除文件或改动历史结果。

全部执行在task111-ps5-20261116.service，4GiB、swap0、CPU200%、Nice19、IOidle；
每30秒观察MemAvailable，低于6GiB停止自身。采样最低15109124 KiB，未触发；
memory.events的max/oom/oom_kill均为0。
[资源原文](../../tools/bolt/results/ps5-final-111-20261116/resources.json)、
[看门狗快照](../../tools/bolt/results/ps5-final-111-20261116/watchdog-snapshot.json)。

[推送前只读ref](../../tools/bolt/results/ps5-final-111-20261116/sandbox-before.stdout)、
[停止后只读ref](../../tools/bolt/results/ps5-final-111-20261116/sandbox-after.stdout)、
[全部raw索引](../../tools/bolt/results/ps5-final-111-20261116/RAW_LINKS.md)。

111 已结束 2026-11-16T09:57:14-08:00 status=STOP
