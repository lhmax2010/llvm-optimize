# 126号：非 UTF-8 进程名与 H5

**结论：PASS。H5 `ed922413c19b01d07e0ec6547771267f40ab5469` 已推sandbox并ls-remote核对一致。第二轮完整743/743通过，r18探针通过，包装器没有残留进程需要清理。H4→H5仅helper +3/-2；父提交、Change-Id及说明保持要求，spec与其他文件不变。没有STOP。**

## 1. 原文归档与分类

步骤0已单独立即提交并推送bolt-v4：`eb9855aa36c83c09e61df306acb1941186a39362`，远端HEAD核对一致。两份原文大小与SHA：

|原文|字节|SHA256|
|---|---:|---|
|[Claude Code 125](../../tools/bolt/results/review-session/claude-code-review-125.md)|9185|a95be144fee5ecdd266f9c1fb58f93a3a2c8494d230335d70312ff64a026169d|
|[Codex 125](../../tools/bolt/results/review-session/codex-review-125.md)|11967|c69704b29625c492d1cf6c771daac88edd862bbf4a0f66ee0d3405b5a34e7b9c|

r18目录存在，原样复制badcomm.py、reaper.py两个文本脚本。[全部原路径/大小/SHA清单](../../tools/bolt/results/ps5-helper-126/archive.json)。

### Codex 125 全部发现的分类与处理

正确性/安全问题：**未发现新的问题，0项待修**。报告明确接受H4，没有需要设计取舍的新阻塞项。其八项核对结论如下；本任务不把“确认已有不变量”误写成八个新缺陷。

|原文项目|分类/处理|
|---|---|
|1 D1/N4诊断无额外procfs读取|已闭合；保留，无新逻辑修改|
|2 6字段stat/3字段成员、属性不改变比较|已闭合；本轮仍保持，新增实进程核对|
|3 名称不参与信号身份选择|已闭合；PID/SID/starttime判断不改|
|4 20成员上限只限制显示，不限制清理|已闭合；保留|
|5 D2/N1阶段deadline和member read errors|已闭合；保留|
|6 N2 sticky errors fail-closed|已闭合；保留，不恢复成功|
|7 retirement、取消、回收|已闭合；不改控制流|
|8 N3注释约两个预算|文档说明；保留，不改预算|
|test_124仍用普通4元组夹具|测试维护/风格；跟进，不改|
|显示控制字符可能换行|措辞/显示风格；跟进，不改控制字符策略|
|20项并非整个历史errors聚合的全局长度上限|文档口径；明确按每个成员列表，不扩展限长|

既有fallback数值PID竞争、setsid逃逸、不可杀死成员、单操作超预算等限制不变；没有新增强隔离或硬实时保证。

Claude Code另外报告的**非UTF-8名称导致未处理异常、中断扫描/清理**属于正确性问题，虽非H4新引入，本任务按PM授权作局部修正。未发现需要追加设计裁决的其他正确性项。[分类JSON](../../tools/bolt/results/ps5-helper-126/review-classification.json)。

## 2. 修改位置与读取审计

|H4行→H5行|位置|处理|
|---|---|---|
|169→169|proc_stat|`Path(path).read_bytes().decode('utf-8', errors='surrogateescape')`，字段解析仍相同；stat里的非UTF8字节不再因解码抛异常|
|278→278–279|session_snapshot|对显示用comm执行UTF8 surrogateescape编码再replace解码；输出可用替换字符，原stat属性不被改写，无额外I/O|
|495→496|call成功路径的argv元数据JSON读取|从严格read_text改为read_bytes+UTF8 surrogateescape；JSON解析及完成字段写回规则不变|

所有`/proc/<pid>/stat`读取都经过proc_stat：扫描前self命名空间检查、逐成员扫描、pidfd及fallback发送前重查。它们共享本次修正，不另增读取或信号路径。call的命令日志读取原本`errors='replace'`，已经容错，保持不变；其他错误日志摘录也已replace。已列出helper全部read_text/read_bytes/decode调用，区分进程控制路径和BOLT、ELF、构建/包配置读取，后者未扩大修改范围。

[范围审计](../../tools/bolt/results/ps5-helper-126/read-audit.json)、[全部文本读取位置及所属函数](../../tools/bolt/results/ps5-helper-126/all-text-read-sites.json)、[H4→H5精确diff](../../tools/bolt/results/ps5-helper-126/helper.diff)。没有改变判断逻辑、6/3元组形状、fail-closed策略。这里只修正编码容错；换行/制表符转义仍按跟进项处理。

## 3. 完整测试与失败分类

743＝125通过版本739＋本轮新增4。两轮均从头跑完所有套件；原739项没有沿用旧PASS。第一轮742通过、1 FAIL、0 ERROR，分类(a)=0、(b)=1、(c)=0；第二轮743/743通过、0失败/错误。

|套件|数量|首轮|第二轮|
|---|---:|---|---|
|review126|4|PASS|PASS|
|review125|4|PASS|PASS|
|review124|2|PASS|PASS|
|review122-retained|11|10 PASS / 1 FAIL|PASS|
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

唯一失败：122新写的`test_stat_name_parentheses`仍patch `Path.read_text`，产品按本轮要求调用read_bytes，所以实际读到python3而非注入名称。这不是括号解析算法失败；属于(b)新夹具与已授权接口不符。一次纠正仅把patch目标改成read_bytes、将同一模拟stat文本编码成UTF8；**原名称期望和全部断言不改**。产品未在首轮后改动。旧739项中除这一个122新夹具适配外，只随源码移动更新两个trace坐标，场景/断言不变。

[首轮失败分类与原文](../../tools/bolt/results/ps5-helper-126/first-run-failures.json)、[原始traceback](../../tools/bolt/results/ps5-helper-126/first-run-failures.txt)、[夹具修正diff](../../tools/bolt/results/ps5-helper-126/fixture-correction.diff)、[原因与行号](../../tools/bolt/results/ps5-helper-126/fixture-correction.json)、[断言修改清单（空）](../../tools/bolt/results/ps5-helper-126/assertion-changes.json)、[源码差异审计](../../tools/bolt/results/ps5-helper-126/test-source-differences.json)、[第一轮结果](../../tools/bolt/results/ps5-helper-126/test-results.json)、[第二轮结果](../../tools/bolt/results/ps5-helper-126/run2/test-results.json)、[第二轮失败清单（空）](../../tools/bolt/results/ps5-helper-126/run2/failure-list.json)。

### 新增4项

1. 真实自有子进程prctl设置`b'\xff\xfe'`；proc_stat返回正确6字段及comm，surrogateescape可还原原始字节。
2. 该进程在独立外部session中：扫描正常，另一个成功步骤正常返回，外部自有进程仍存活。
3. 实际超时步骤的session内，子成员setpgid到自己的组并设置坏编码名称：helper报告TIMEOUT而非编码/清理异常；扫描诊断出现替换字符，持有的pidfd确认成员死亡。场景包装器只清理自身未回收子进程，最终为空。
4. 合成坏编码comm：真实snapshot在read_text/read_bytes均被设为失败时仍可格式化，得到替换字符且可严格编码为UTF8。

本轮新增3项真实自有进程、1项合成/mock。进程只由测试自己的Popen或所属未回收子进程pidfd清理；不按名称或任意裸PID杀进程。[新测试](../../tools/bolt/results/ps5-helper-126/run2/tests/test_126.py)、[所有权包装场景](../../tools/bolt/results/ps5-helper-126/run2/tests/owned_utf8_scenario.py)。

## 4. r18探针

已完整阅读badcomm.py和reaper.py后才执行：badcomm的直接孩子由自己持有的Popen管理；包装器作subreaper，只对自己未回收的孩子打开pidfd发信号，不按名字或任意PID清理。原样运行归档脚本，没有改其逻辑。

原文结果：A_scan=`ok`；A_call=`OK`；B_call=`GateError: TIMEOUT...`，无codec或cleanup error；child_rc=0，survivors_cleaned=0。说明坏编码成员由helper完成清理，包装器没有剩余进程需要杀死。SIGCHLD/信号模式全套回归亦通过；实际探针模式为pidfd。

[安全审阅](../../tools/bolt/results/ps5-helper-126/probes/ownership-review.json)、[调用](../../tools/bolt/results/ps5-helper-126/probes/invocation.json)、[完整stdout](../../tools/bolt/results/ps5-helper-126/probes/stdout.txt)、[stderr](../../tools/bolt/results/ps5-helper-126/probes/stderr.txt)、[结果](../../tools/bolt/results/ps5-helper-126/probes/result.json)。

## 5. 证据整理和跟进清单

按明确授权，把125的`tests/test_122.py`重命名为`tests/test_122.pre-correction.py`，内容字节不变；[README](../../tools/bolt/results/ps5-helper-125/README.md)说明它是首轮旧副本，125通过版本是`run2/tests/test_122.py`。历史日志中的旧路径保留，未重写结果。[重命名SHA核对](../../tools/bolt/results/ps5-helper-126/evidence-rename.json)。

以下只登记，本轮不修改：

|来源|项目|处理|
|---|---|---|
|Claude 1|真正扫描截断时空的last observed members后缀|措辞跟进|
|Claude 2|枚举刚结束的deadline仍称scan incomplete|诊断边界措辞跟进，不改判定|
|Claude 3|errors历史聚合长度未设上限|显示风格跟进，不改收集策略|
|Claude 4|普通GateError缺少成功退出上下文|措辞跟进|
|Codex|test_124普通4元组夹具|测试维护跟进|
|Codex|名称换行/tab/control字符转义|显示风格跟进；本轮仅处理非法UTF8|
|Codex|20项为每列表上限，不是整条日志上限|文档口径，未扩展成全局截断|

Claude第5项旧测试副本已按步骤4处理。关于125的19/22探针口径：Claude说明另外3条H3运行在cmp.jsonl；本轮照录此说明，不回改125实际只跑19条的事实。本轮不重跑r17全套，r18探针单独报告。

## 6. H5和sandbox

- H4：`7a7bc17467d4c5da9763e86e3c74a123b3ff0df2`。
- H5：`ed922413c19b01d07e0ec6547771267f40ab5469`，tree `66aa08d9e6717b904a0eb390096d908fea1109c0`。
- 单提交父：`61ef5d31ca91025c414c748477bef0c64ddfa67c`。
- Change-Id：`I28171720d5bbbf9eaf491cdafc0aee0b43f9cd06`。
- 原作者/日期保留；提交者Hao Lin；提交说明与H4逐字节相同。
- H4→H5仅`packaging/clang-bolt-helper.py` **+3/-2**；spec及所有其他文件完全相同；H5 tree等于实际测试的tree。

以H4为lease，完整SSH URL为`ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm`，只推`refs/heads/sandbox/lhmax2025/bolt_pgo`。推送一次成功；前后ls-remote分别等于H4/H5。远端继承标题>50字符提示保留，不是拒绝；按任务不改提交说明。没有Gerrit评审写入或refs/for推送。

[身份核对](../../tools/bolt/results/ps5-helper-126/candidate.json)、[说明全文](../../tools/bolt/results/ps5-helper-126/h5-message.txt)、[命令](../../tools/bolt/results/ps5-helper-126/sandbox-push.command)、[远端原文](../../tools/bolt/results/ps5-helper-126/sandbox-push.stderr)、[之前](../../tools/bolt/results/ps5-helper-126/sandbox-before.stdout)、[之后](../../tools/bolt/results/ps5-helper-126/sandbox-after.stdout)。

## 7. 资源、读取范围和未运行项

所有worker串行systemd用户服务：MemoryMax=4G、MemorySwapMax=0、CPUQuota=200%、Nice19、IOSchedulingClass=idle。无资源准入等待/轮询，无OOM；一次新夹具接口修正及一次交付准备修正已记录。未操作120-N，未操作另一项目目录、进程、锁；没有构建、QB访问或实物重放。

读取：两份125复审全文、H4 helper完整进程控制区域及全文件读取调用、125成功版测试、本轮两次完整结果、r18两个脚本、Git身份和sandbox引用。未重新审阅非进程控制产品功能；未运行完整构建、新QB、真实归档重放、r17全部探针或Python3.9环境认证。

原样证据不作空白清洗；产品实际diff和文档单独检查。超10MB或gitignore排除日志本地保留，路径/大小/SHA见[local-only-files.json](../../tools/bolt/results/ps5-helper-126/local-only-files.json)。[发布文件索引](../../tools/bolt/results/ps5-helper-126/publication-files.json)。

**本次STOP原文：无。** 首轮唯一失败原文和分类已保留，并按授权纠正后全套通过。

已结束 2026-11-17T09:26:50.751071-08:00 archive=PASS

已结束 2026-11-17T09:34:25.948647-08:00 first full run completed total=743

已结束 2026-11-17T09:38:55.638541-08:00 second full run completed total=743

已结束 2026-11-17T09:39:13.623278-08:00 r18 probes=PASS

已结束 2026-11-17T09:40:33.940507-08:00 sandbox=PASS

交付准备修正一次：默认`git diff --cached --name-only`对R100只返回目标名，清单断言误要求源名同时存在。改用`--no-renames`检查删除/新增路径，并直接比较HEAD旧文件与暂存新文件字节，两项通过。原证据内容不变。[首次原文](../../tools/bolt/results/ps5-helper-126/preparation-error.txt)、[R100原文](../../tools/bolt/results/ps5-helper-126/preparation-rename-proof.stdout)、[修正diff](../../tools/bolt/results/ps5-helper-126/preparation-fix.diff)。这一次准备修正已使用，无第二次错误；不影响产品、测试和sandbox结果。
