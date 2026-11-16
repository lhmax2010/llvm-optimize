# 110：session 跟踪（交付准备第二次错误 STOP）

**STOP：完整报告生成遇到第二次准备错误，按规则未修正或重跑。产品修改、测试、本地候选已完成，未推sandbox。**

两份评审已原样复制并先行推送，提交c34ae595b60c8894b50f64376541a9c46fea5d16，ls-remote核对一致：
- [Claude Code 原文](../../tools/bolt/results/review-ps5-final/claude-code-review.md)：17057 B；SHA256 a481301ef44ed6841c7593b436a76d11668892380f09de5ac4b7004e830e1fa4。
- [Codex 原文](../../tools/bolt/results/review-ps5-final/codex-review.md)：26662 B；SHA256 a3edda3921c864992eb5bd2f3aad810eda53a5890578386ac3bc4fae31328be7。

## 已完成并保留

- 基底/sandbox：92775bc36de729106b502c4e5967a5af0e4f4033。新独立游离工作树：W/temp/ps5-session-110-20261116/source；原工作树和分支未改。
- F1：proc_stat增加SID，新增session扫描；成功后等整个session最多10秒；失败/超时/取消重复扫描并SIGKILL各存活PID，普通清理截止10秒。先杀leader组，保证后续/proc扫描失败时也处理直接启动组。第二信号清整个session，重扫最多1秒，再按原信号终止。未回收leader固定SID；自己setsid脱离的进程不在跟踪范围，注释与测试均明确记录。
- F2：失败路径在reap_child前清_ACTIVE_GROUP；该兼容变量名现在存SID。
- F3：LiveDescendantsError专用类型，R1不再匹配错误文本。
- F4：测试spec副本显式展开__spec_install_post，检查post调用、PASS标记、disk-report三项次数；6个正反例证明错误宏体会被拒绝。产品spec未改。
- 647/647从头通过：138转换器相关 + 393 helper + 30 HQ定向 + 6 N1 + 45既有R1回归 + 29新增session/F2/F3/r14 + 6宏检查。
- 8组平台RPM解析通过；默认x86_64/armv7l/aarch64与92775bc3包括前导空行均逐字节相同。没有把解析当作实际构建证明。
- r14探针目录存在；原样保存，复用短期/长期后代和第二信号三例，survivors均0。ninja多组结构用5进程、3进程组、同一session的模拟夹具验证，未启动ninja构建。
- 新本地单个累积候选：56902c58ba8fc2d3a4216e69ed3acb3d2cb6f8a3；tree 4b528fcbb1dfbd782d091c791e270e56ca6addf3；父61ef5d31ca91025c414c748477bef0c64ddfa67c；提交后干净。相对基底仅helper改动；说明仅改Part2的R1两行为session描述，72列及对外文本门禁通过。
- 结束只读ls-remote仍为92775bc3。没有推sandbox，没有Gerrit写操作、QB访问、RPM/LLVM目标构建或真实归档重放。

## 证据

[产品diff](../../tools/bolt/results/session-tracking-110-20261116/final-product.diff)、[候选身份](../../tools/bolt/results/session-tracking-110-20261116/candidate.json)、[说明](../../tools/bolt/results/session-tracking-110-20261116/commit-message.txt)、[说明diff](../../tools/bolt/results/session-tracking-110-20261116/commit-message.diff)。

[测试总表](../../tools/bolt/results/session-tracking-110-20261116/test-summary.json)、[567项](../../tools/bolt/results/session-tracking-110-20261116/legacy-output.txt)、[45项](../../tools/bolt/results/session-tracking-110-20261116/regression109-output.txt)、[35项](../../tools/bolt/results/session-tracking-110-20261116/sessions110-output.txt)、[session实测](../../tools/bolt/results/session-tracking-110-20261116/session-observations.json)、[8组解析](../../tools/bolt/results/session-tracking-110-20261116/parse-result.json)、[F4修正](../../tools/bolt/results/session-tracking-110-20261116/F4-parser.diff)。

测试环境从109号复制；接口mock由group改session，proc_stat假记录增加SID，错误名称随接口变化，断点按原语句重定位；计数与判定未放宽。[完整测试适配diff](../../tools/bolt/results/session-tracking-110-20261116/legacy-adaptations.diff)。旧结果未覆盖；scratch仅保留本地，不作为交付输入重新运行。

## 延后与读取边界

只实施F1–F4。/proc提前失败、首次取消在正常等待内加速、嵌套信号R2、SystemExit/KeyboardInterrupt前记录cleanup错误、复用CMakeCache的关闭处理、BOLT关闭时Python最低版本依赖、注释/使用说明和hybrid关闭而BOLT开启的实际构建认证，均登记延后，不改。

已读两份评审、109号报告与helper/spec/测试、r14探针、实际测试与平台展开；未读QB网站、新Gerrit评论，未做产品构建/重放。所有执行在4GiB、swap0、CPU200%、Nice19、IOidle的串行用户服务内。内存峰值975003648 B，无OOM；30秒看门狗未触发，采样最低MemAvailable为11748952 KiB。[资源](../../tools/bolt/results/session-tracking-110-20261116/resources.json)。

## 准备错误与STOP原文

第一次：生成新测试文件时，外层shell单引号与heredoc内单引号冲突；shell解析失败，测试未创建或执行。已按唯一一次机会修正为直接传入heredoc，原文及修正记录保留：
[第一次错误](../../tools/bolt/results/session-tracking-110-20261116/preparation-error-1.txt)、[修正记录](../../tools/bolt/results/session-tracking-110-20261116/preparation-fix-1.diff)。

第二次发生在647测试、解析、候选创建均完成之后，完整报告的JS模板含Markdown反引号，提前结束字符串，工具解析失败；shell未执行。

    Script error:
    SyntaxError: Unexpected identifier 'text'

按第二次准备错误STOP，不再修正或重跑完整报告生成，只保存本停止报告和已有证据。[STOP原文](../../tools/bolt/results/session-tracking-110-20261116/second-preparation-STOP.txt)。

[raw索引](../../tools/bolt/results/session-tracking-110-20261116/RAW_LINKS.md)。

110 已结束 2026-11-16T09:43:26-08:00 status=STOP（交付准备错误；产品647/647）
