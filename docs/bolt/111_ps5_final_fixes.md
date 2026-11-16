> 最新结论：111号续已完成，661/661通过，sandbox为378f8d5c94aeadd2a8618d04ad39a531529c726c。下方首次STOP记录原样保留；续跑详情见文末。

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


## 111号续：PM空行裁决与完成结果

结论：PASS。PM已核对原STOP的差异，仅有开头12个空行及BuildRequires区域一个空行从python3声明之前移至之后。RPM前导部分空行无语义、依赖集合不变，按PM裁决放行；历史STOP原文保留。比较规则改为双方去掉全部空行后逐字节比较，空行数量、位置和原始diff仍存档。本续跑没有再改产品文件，未使用准备错误修正机会。

### 提交、范围和说明

新单个累积候选：HEAD `378f8d5c94aeadd2a8618d04ad39a531529c726c`，tree `ad3898ff67a65939778d3831090d4270ac771879`，父 `61ef5d31ca91025c414c748477bef0c64ddfa67c`。
产品diff逐字节等于第一次111实施时的implementation.diff，仅P1/P2/S2：关闭hybrid时添加三个复位项；python3 >= 3.9保留在x86_64但移到BOLT条件外；S2仅注释措辞，helper AST不变。
说明在Part 1和Part 2的开关段各补充：关闭后ThinLTO/MLGO、固定参数、native archive转换仍开启。保留Change-Id和Signed-off-by；全部行不超过72列。推送前工作树干净。

证据：[候选身份](../../tools/bolt/results/ps5-final-111-20261116/resume/candidate.json)、[产品未再变化](../../tools/bolt/results/ps5-final-111-20261116/resume/unchanged-product-check.json)、[说明全文](../../tools/bolt/results/ps5-final-111-20261116/resume/commit-message.txt)、[说明diff](../../tools/bolt/results/ps5-final-111-20261116/resume/commit-message.diff)、[提交前门禁](../../tools/bolt/results/ps5-final-111-20261116/resume/prepush-gates.json)。

### 展开与组合

默认三架构删除空行后均与a061f4e4逐字节相同。空行统计：

| 架构 | 基准空行数 | 候选空行数 | 非空行逐字节比较 |
|---|---:|---:|---|
| default-x86_64 | 130 | 142 | PASS |
| default-armv7l | 129 | 141 | PASS |
| default-aarch64 | 129 | 141 | PASS |

三份原始diff与逐行空行位置均保存：[展开结果](../../tools/bolt/results/ps5-final-111-20261116/resume/parse-result.json)、[比较器修正diff](../../tools/bolt/results/ps5-final-111-20261116/resume/parse-script.diff)。未豁免任何非空行内容差异。

总开关关闭的%build与父61ef5d31的完整差异仅为既有Part 3固定参数块，以及P1新增三项：-DTIZEN_HYBRID_LINK=OFF、-UBUILD_SHARED_LIBS、-ULLVM_TOOL_LLVM_DRIVER_BUILD。删去这三个argv后，主cmake argv与父提交逐项相同；BOLT段和post宏均不存在；ThinLTO/MLGO和固定参数保留。ARM默认展开仍与a061f4e4非空内容完全相同。

[完整build diff](../../tools/bolt/results/ps5-final-111-20261116/resume/total-off-build-vs-parent.diff)、[逐参数证明](../../tools/bolt/results/ps5-final-111-20261116/resume/parse/total-off-cmake-reset-proof.json)。

除沿用的8组平台展开/解析（默认三架构、总关、hybrid关、BOLT关、两项关、bcond回退）外，另运行三个布尔开关的全部8种组合。顺序为llvm_speedup/hybrid_link/clang_bolt：000、001、010、011均关闭hybrid和BOLT；100两项关闭；101仅BOLT开启；110仅hybrid开启；111两项开启。每组都检查显式展开后的安装post宏、依赖和Part 3。python3最低版本在全部x86_64组合保留，xz/elfutils随BOLT关闭；ARM不增加该python依赖。原五项解析（x86开/关、armv7l、aarch64、一行bcond回退）均覆盖并PASS，均为平台RPM4.14.1解析和--nobuild，没有执行构建。

### 全量测试（本次重新运行）

| 套件 | 通过/总数 |
|---|---:|
| policy / release / r2 / r3-r4-r5 / hardening / r11 | 138/138（46+5+12+40+16+19） |
| helper | 393/393 |
| HQ H1–H5 | 30/30 |
| N1 | 6/6 |
| 109回归 | 45/45 |
| 110会话跟踪/F2/F3/探针/post宏 | 35/35 |
| 111 P1/P2/S2及8组合专项 | 14/14 |
| 合计 | **661/661** |

原647项全部从头运行，未沿用110通过记录。新14项逐项断言和全部原文见[p1p2-output.txt](../../tools/bolt/results/ps5-final-111-20261116/resume/p1p2-output.txt)；总表见[all-tests-summary.json](../../tools/bolt/results/ps5-final-111-20261116/resume/all-tests-summary.json)。既有各套件原始输出在tests/*.log、regression109-output.txt、sessions110-output.txt；复制清单记录测试来源及SHA，没有修改既有测试的输入或预期，仅测试副本路径适配到本轮工作树。

### sandbox推送与Q6

推送前：`92775bc36de729106b502c4e5967a5af0e4f4033`。
推送后：`378f8d5c94aeadd2a8618d04ad39a531529c726c`，ls-remote核对一致。
使用原有完整SSH URL、BatchMode和实际ref refs/heads/sandbox/lhmax2025/bolt_pgo；严格带旧HEAD lease，仅推送一次。

[命令原文](../../tools/bolt/results/ps5-final-111-20261116/resume/push-command.txt)、[远端完整返回](../../tools/bolt/results/ps5-final-111-20261116/resume/sandbox-push.stderr)、[推送前](../../tools/bolt/results/ps5-final-111-20261116/resume/sandbox-before.stdout)、[推送后](../../tools/bolt/results/ps5-final-111-20261116/resume/sandbox-after.stdout)。远端仅给出“subject >50 characters”提示，推送成功；本任务每行≤72列要求通过。

Q6新版明确总开关只关闭混合链接和BOLT；ThinLTO/MLGO、固定参数和转换器保留；给出项目Macros部分及gbs build的宏写法，恢复必须删除宏而不是设为0；单项开关存在，但hybrid关/BOLT开尚未通过实际构建认证。FINAL旧内容保留为-v2（已有-v1也保留），只替换Q6，其余回复逐字不变；对外文本门禁通过，未发布。

[新版回复](../../tools/bolt/results/hq-review-361395/round2/replies/FINAL-replies-for-user.md)、[旧版-v2](../../tools/bolt/results/hq-review-361395/round2/replies/FINAL-replies-for-user-v2.md)、[Q6 diff](../../tools/bolt/results/ps5-final-111-20261116/resume/Q6-reply.diff)。

### 资源、边界与延后

本次受限服务task111-resume-20261116：MemoryMax=4GiB、swap0、CPUQuota=200%、Nice19、IO idle。记录时memory.peak=710877184 B，memory.events的OOM/oom_kill均为0；30秒MemAvailable看门狗未触发（阈值6GiB）。数据是交付前采样，见[resources.json](../../tools/bolt/results/ps5-final-111-20261116/resume/resources.json)和[看门狗记录](../../tools/bolt/results/ps5-final-111-20261116/resume/watchdog-snapshot.jsonl)。

未构建、未访问QB、未重放实物、未运行BOLT、未写Gerrit、未操作另一项目；本轮只推sandbox和证据bolt-v4。110报告补全已经在首次111交付中完成，照录其既有证据，原STOP均保留。

继续延后：排空等待期间第一个信号的响应优化；hybrid关/BOLT开组合的实际构建认证；setsid脱离session仍为已知限制；嵌套第二信号及SystemExit/KeyboardInterrupt前cleanup错误记录等既定延后项不扩展实现。轻量展开与测试不代替下一轮QB和本地完整构建。

已读：111现场产品diff、110测试环境与原始证据、a061f4e4/61ef5d31的spec、平台RPM宏、当前回复草稿。未读/未访问：新的HQ评论、QB页面、另一项目的目录或进程。无新增STOP，准备错误修正0次。

已结束 2026-11-16T10:07:06.595060-08:00 STEP3 sandbox PASS
已结束 2026-11-16T10:09:29.746200-08:00 STEP4 Q6 PASS（仅草稿）
