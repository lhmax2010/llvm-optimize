# 104：HQ新评审、补丁范围与本地候选

**最终 STOP：用户补充的前置门禁要求 PS4 与 PS3 的父提交相同，现场不满足。PS3 的父是13c3e223，PS4的父是61ef5d31。tree与提交说明相同。未推送任何LLVM分支，未回复Gerrit，未执行361624试合并。**

在该补充到达之前，已根据原任务及PM的H1–H5裁决生成本地候选，最终适用测试561/561通过；但导出比较也已因准备脚本期望0008而遇到native导出停止，五项解析未运行。候选保留，仅供审阅，**不可作为已放行或待上传PS5**。102号与旧本地PS4继续暂缓。

| 对象 | 结论 | 本轮状态 |
|---|---|---|
| 361395 PS4 改接 | STOP：新父提交门禁不满足 | e9f16ee3；Gerrit标记NO_CHANGE，但父确实不同 |
| H1 helper SIGCHLD | HQ NEEDS-FIX | 本地候选已按PM方案恢复，测试通过 |
| H2 spawn窗口 | HQ NEEDS-FIX | 本地候选暂存第二信号，不改子进程mask |
| H3 debugfiles.list | HQ NEEDS-FIX | 本地候选显式路径；五项展开未完成 |
| H4 GNU长名称表 | HQ NEEDS-FIX | 本地候选拒绝第二表，包括首表为空 |
| H5 converter SIGCHLD | HQ NEEDS-FIX | 本地候选外层finally覆盖解析和退出 |
| Q1/Q2/Q4/Q5/Q6 | ACCEPT：按PM只解释、不改代码 | 英文草稿；Q5登记下轮插件载入验证 |
| Q3 | ACCEPT：本系列维持父提交默认6 | 草稿说明可另起change评估并发 |
| 361624整体纳入候选 | REJECT（仅本轮范围） | 独立后续WIP，只读评审，未并入 |
| 361624试合并 | NOT RUN | 新父提交门禁STOP，未启动cherry-pick |
| 导出比较、五项解析 | STOP / NOT RUN | gbs返回0；输出模式不符合驱动预期 |

## 1. 收集与新增门禁

所有Gerrit操作均为SSH BatchMode只读query或fetch。保存主query，以及owner和message/topic搜索完整argv/stdout/stderr。对照103原query：

- 新增PS4：e9f16ee3c078f9a5ae563ee01e52ace27b28da4d，上传记录时间2026-11-16T03:47:54-08:00，uploader/author显示Lin Hao；kind=NO_CHANGE。
- 新增Dongkyun Son的Code-Review+1汇总：2026-11-16T04:04:40-08:00，包含一条patch-set-level评论。
- 原PS3五条行内意见、六问总评逐字未变。没有新的源码行评论。
- 新评论file=/PATCHSET_LEVEL、line=0，没有可附的代码行。SSH不返回它的独立时间、thread id、unresolved、in_reply_to，这些字段UNKNOWN，不能拿汇总时间代替。

新评论原文：

> NOTE: a follow-up change, 361624 (split tool subpackages into llvm-tools-subpkgs.spec; also touches bolt/ CMake), will be rebased onto this change after it merges.

**“在361395合入后改接”出自361395 PS4这条评论，不在361624提交说明正文中。** 未把它误归为提交说明。

| 对象 | revision | 父提交 | tree |
|---|---|---|---|
| 361395 PS3 | ecb2dec72ec5afde9c6c70f166e2ac12b47c093e | 13c3e223d9e1b35e4affb55255c5042f8c940f35 | b2e8af2477cf623a945aa80bf8288a262dd4a5a9 |
| 361395 PS4 | e9f16ee3c078f9a5ae563ee01e52ace27b28da4d | 61ef5d31ca91025c414c748477bef0c64ddfa67c | b2e8af2477cf623a945aa80bf8288a262dd4a5a9 |
| 361624 PS1 | da885208aeb52f55c448ff46873d242346727522 | 61ef5d31ca91025c414c748477bef0c64ddfa67c | 6f65022eea40016853aa77bbbbbb87f70f0fc7ce |

PS4相对PS3完整代码diff为空，说明全文相同；**父提交不同**，不自行豁免用户新增门禁。361624为NEW/WIP，作者自己的Verified−1仅作记录，不推断具体构建失败，未访问QB。

证据：[主query](../../tools/bolt/results/hq-review-361395/round2/query.stdout)、[新增记录](../../tools/bolt/results/hq-review-361395/round2/collection-delta.json)、[总评差异](../../tools/bolt/results/hq-review-361395/round2/general-review.diff)、[父提交门禁](../../tools/bolt/results/hq-review-361395/round2/parent-gate.json)、[361624 query](../../tools/bolt/results/hq-review-361395/round2/followup-query.stdout)、[owner查询](../../tools/bolt/results/hq-review-361395/round2/owner-query.stdout)、[message/topic查询](../../tools/bolt/results/hq-review-361395/round2/related-query.stdout)。

两个对象已fetch到新独立clone下的detached工作树。原hardening工作树仍121b4c23且tracked clean，[核对](../../tools/bolt/results/hq-review-361395/round2/original-worktree-readonly.json)。没有移动任何现有分支。

## 2. 361395候选评审与实现

### 2.1 HQ版本的H1–H5

PS4代码与PS3同树，H1–H5均没有被HQ新代码解决。对每个hunk的映射因此是空diff；所有H实现来自PM授权的103草案，非冒称采用HQ已完成的修复。

- **H1 NEEDS-FIX**：helper重置SIGCHLD后不恢复。候选在原有BaseException清理/回收之后的finally恢复原值；成功、失败、超时、取消、SystemExit、KeyboardInterrupt、Popen异常覆盖。SIGCHLD改变仅在helper进程内，不修改父RPM shell。清理本身失败仍按原逻辑记录，SIGKILL等不可捕获终止不承诺执行Python finally。
- **H2 NEEDS-FIX**：HQ没有pthread_sigmask，也未修窗口。候选以_SPAWNING标识临界区，暂存第二信号，登记_ACTIVE_GROUP后立即处理；Popen抛异常同样经过finally。没有preexec_fn，没有改子进程掩码。定向注入检查成功/异常及第一信号路径，真实子进程mask相同；既有真实双信号与子孙清理测试继续通过。不是所有调度交错的形式证明。
- **H3 NEEDS-FIX**：候选spec显式传入 --debugfiles-list "%{_builddir}/%{buildsubdir}/debugfiles.list"；CLI要求参数，debug门禁用显式路径，release内容检查仍跳过。installed SHA、debug-file SHA、debuglink CRC、权限、alias/security/tiny/real原校验没有删改。非标准路径/缺失/错误成员/release/spec字面值夹具通过；实际五种RPM展开未完成。
- **H4 NEEDS-FIX**：候选用seen_longnames记录是否出现过，不以表内容真假判断。normal/thin两种归档，空首表+第二表、双非空表拒绝，单空表和合法长名仍接受。
- **H5 NEEDS-FIX**：候选将解析/安装主体放在_install_main，外层finally覆盖parse_args帮助/错误和各种异常退出；Part4日志仍在reset前反映继承状态。入口mock与既有真实转换/信号夹具分别覆盖入口和子进程运行路径。

Q项按PM裁决：Q1日志与函数作用域只解释；Q2说明10处、5处逐指令闭合到llvm_unreachable、另5处结构相符尚未逐一闭合，不称“全部无害”；Q3默认6本来就在父提交，本系列不改；Q4需明确accel包及setup边界，现有数据不足；Q5不改代码，下轮增加正确链接方式的最小插件载入；Q6关闭Part2不等于回退Part1/3/4。

### 2.2 候选身份和差异

补充父门禁到达之前生成：
- SHA：3a1b0e2970d6ba4d09d7c357379723158a78ac56
- tree：50ff47dd6b712f4aab83e7825993a2a97cba8f07
- 父：61ef5d31ca91025c414c748477bef0c64ddfa67c
- 组合：361395 PS4树 + git diff ecb2dec7 121b4c23 + PM批准的H1–H5。
- 为单评审形式创建一个累积本地提交，不是上传的PS5；无合并冲突。旧8ec86c3e和121b4c23不变。
- 只改helper、converter、spec三个文件。没有纳入361624、没有改并行度或BOLT参数。

[身份](../../tools/bolt/results/hq-review-361395/round2/candidate-identity.json)、[相对HQ差异](../../tools/bolt/results/hq-review-361395/round2/candidate-vs-HQ.diff)、[相对PS3](../../tools/bolt/results/hq-review-361395/round2/candidate-vs-PS3.diff)、[相对8ec86c3e](../../tools/bolt/results/hq-review-361395/round2/candidate-vs-localPS4.diff)、[Part4输入](../../tools/bolt/results/hq-review-361395/round2/part4-on-PS4.diff)、[合并记录](../../tools/bolt/results/hq-review-361395/round2/merge.json)。

[说明全文](../../tools/bolt/results/hq-review-361395/round2/candidate-message.txt)沿用HQ说明，补总述、Part4与H修复；将第二信号“立即”保证限定为spawn临界区登记后立即处理，其余Part1–3保留。[说明diff](../../tools/bolt/results/hq-review-361395/round2/candidate-message-vs-HQ.diff)。最长72列，英文、对外文本门禁通过；草稿行宽预检过程另存，不曾上传超长草稿。

### 2.3 测试结果及未通过原文

| 对象 | 套件 | 结果 |
|---|---|---|
| HQ PS4 | policy / release / r2 | 46/46、5/5、12/12 |
| HQ PS4 | r3/r4/r5 | 39/40；1个ProcessLookupError |
| HQ PS4 | helper | 393/393 |
| HQ PS4 | H定向30项 | 7通过、22FAIL、1ERROR |
| 候选 | 原有+加固+101新增 | 138/138 |
| 候选 | H定向 | 30/30 |
| 候选 | helper首轮 | 392/393 |
| 候选 | helper按H1新约定全量重跑 | 393/393 |
| **候选最终** | **138+30+393** | **561/561** |

119原套件包括16项Part4专用，HQ不含Part4，因此排除这16项，跑其余103项；候选跑全部138。既有单独身份测试test_messages不适用现在单提交，沿用101选择，身份另查，未把排除计为通过。

HQ旧测试错误：test_converter_exited_leader_descendant读取刚退出进程的/proc/.../stat时ProcessLookupError；未重跑、未修改HQ。新定向的H3 ERROR为旧推导路径导致GateError，属于暴露的缺口，不是隐去的导入错误。[HQ全套结果](../../tools/bolt/results/hq-review-361395/round2/hq-tests/test-results.json)、[HQ helper](../../tools/bolt/results/hq-review-361395/round2/hq-tests/helper.log)、[HQ定向](../../tools/bolt/results/hq-review-361395/round2/hq-tests/targeted-rerun.log)。

准备修正一次：首次新定向脚本因字节串转义SyntaxError，在进入任何测试之前退出；[原脚本](../../tools/bolt/results/hq-review-361395/round2/test_hq_requests.initial.txt)、[首次错误](../../tools/bolt/results/hq-review-361395/round2/hq-tests/targeted.log)、[修正diff](../../tools/bolt/results/hq-review-361395/round2/preparation-fix-1.diff)保留，未改产品期望。

H3的显式路径接口变化只调整测试副本的调用参数，原断言不改；相关diff保留。H1旧夹具先设置SIG_IGN，却断言返回后SIG_DFL，直接与PM“恢复原值”冲突；仅该断言改为SIG_IGN，重新全量393项，产品实现不因该失败修改。[原因](../../tools/bolt/results/hq-review-361395/round2/candidate-tests/H1-contract-test-update.md)、[diff](../../tools/bolt/results/hq-review-361395/round2/candidate-tests/H1-contract-test-update.diff)、[原FAIL](../../tools/bolt/results/hq-review-361395/round2/candidate-tests/helper.log)、[重跑](../../tools/bolt/results/hq-review-361395/round2/candidate-tests/helper-contract.log)。

[候选138结果](../../tools/bolt/results/hq-review-361395/round2/candidate-tests/test-results.json)、[定向30原文](../../tools/bolt/results/hq-review-361395/round2/candidate-tests/targeted.log)、[定向源代码](../../tools/bolt/results/hq-review-361395/round2/test_hq_requests.py)。均为单元/mock及既有小对象夹具；不等于RPM构建或450归档真实重放。

### 2.4 导出和五项解析 STOP

两次实际gbs export均rc0，但产生native tar、spec、Source等13文件，没有0008。驱动沿用101的独立补丁导出预期，next(glob('0008-*.patch'))抛StopIteration。原因尚未确定；只观察到新独立clone的本地branch/config与旧仓库不同，不能未经证明归因。未改配置、未改预期、未重跑。五种解析全部NOT RUN，不能沿用101的PASS。

[错误原文](../../tools/bolt/results/hq-review-361395/round2/STOP.txt)、[HQ命令](../../tools/bolt/results/hq-review-361395/round2/HQ-export.json)、[候选命令](../../tools/bolt/results/hq-review-361395/round2/candidate-export.json)、[清单](../../tools/bolt/results/hq-review-361395/round2/export-inventory.json)、[比较驱动](../../tools/bolt/results/hq-review-361395/round2/export_parse.py)、[驱动相对101 diff](../../tools/bolt/results/hq-review-361395/round2/export_parse-vs-101.diff)。大tar仅在新本地exports目录，不入证据Git。

## 3. 361624独立评审

### 3.1 范围与身份

[自身完整diff](../../tools/bolt/results/hq-review-361395/round2/361624-ps1-own.diff)涉及24文件；[相对PS3完整diff](../../tools/bolt/results/hq-review-361395/round2/361624-ps1-vs-PS3.diff)会包含本系列缺失，因为361624是从共同父61ef5d31出发的兄弟提交，不是以PS3为父。不能将那些删除hunk解释成HQ有意撤销本系列。

[全文说明](../../tools/bolt/results/hq-review-361395/round2/361624-ps1-commit.txt)、[逐hunk映射](../../tools/bolt/results/hq-review-361395/round2/hunk-map.json)。全部属于独立新改动，未实现H1–H5。作者Dongkyun Son，自有Change-Id Ie2c1d45…，两条Signed-off-by和Co-Authored-By；不替换本系列身份。标题75列、若干正文超过72列；按本系列文本规则需整理，但这不是代码失败。

### 3.2 与Part1–4的相互影响（静态观察，未试合并）

| 区域 | 观察与结论 |
|---|---|
| clang/lld/llvm-ar路径/所属包 | 自身diff没有直接移动这三个bin路径或把它们移入新bolt子包；不能据此认定改接后的全部打包等价 |
| Part1静态链接 | 未直接改三驱动hybrid标记；但去掉多处BOLT DISABLE_LLVM_LINK_LLVM_DYLIB不限standalone，会改变in-tree BOLT工具链接策略 |
| Part2 clang替换/post | 361624基于不含Part2的父，未携带post、debugfiles.list或identity实现；改接必须保留整个post链和本轮显式清单参数 |
| %install | 改为DESTDIR安装并移除libgomp/libiomp5链接；需要与普通clang安装、RUNPATH、post冻结/清单对照，不能只套用旧包SHA结论 |
| %files及依赖 | 新bolt子包；原spec加python3/Obsoletes，部分%files重排；未见直接搬走clang/lld/llvm-ar，但需改接后逐包清单验收 |
| debuginfo | 新spec设置debug_package为空，依赖平台注入；主spec新增build-id；必须对新子包及主包分别验收，不能借用本轮解析 |
| llvm-static-devel/Part3/4 | 新spec BuildRequires llvm-static-devel，未直接改converter；其“未安装static-devel”注释与BuildRequires矛盾。后续改接须保留转换调用/信号状态/summary行为 |
| ARM | armv7l targets从ARM;BPF增加AArch64;X86；新bolt打包、runtime条件及固定lib64路径也需ARM检查，因此不能宣称ARM不变 |
| X86镜像helper | standalone条件存在；仍需同版逐函数比对与实际链接检查，不以源码阅读宣称链接成功 |
| 新说明范围 | 是独立后续方案，不适合作为H修复的整体替代 |

逐项评审：standalone ZLIB/LibXml2依赖方向ACCEPT；不区分standalone的链接/flags改动NEEDS-FIX（至少隔离in-tree既有策略或单独认证）；build-id/ARM目标/安装布局NEEDS-FIX（分项验收范围尚未完成）；镜像helper NEEDS-FIX（验证缺口，不代表已证明机器码错）。将整份并入本轮候选REJECT，仅为范围判断，不是否定后续拆包方向。[后续最小修改方向](../../tools/bolt/results/hq-review-361395/round2/followup-review-notes.md)，未应用。

用户新增的试合并授权到达时，其前置父提交门禁已经不满足。故 **没有cherry-pick，没有冲突现场，没有解决或提交冲突**；实际冲突清单UNKNOWN。只列潜在接合点，不伪造实际冲突结果。

### 3.3 英文意见草稿

N1仅陈述独立后续改接以及BOLT链接、安装布局、ARM验收依赖；更细意见等待前置裁决和实际试合并后补充，不在未试合并时承诺“no blocking issues”。没有在Gerrit发布任何文本。

## 4. 草稿、后续验证及待PM裁决

[12份回复索引](../../tools/bolt/results/hq-review-361395/round2/replies/README.md)包括更新的H1–H5/Q1–Q6与新增N1；[对外门禁](../../tools/bolt/results/hq-review-361395/round2/reply-text-gate.json)全部通过。HQ未实现H项，因此草稿不虚称HQ已经解决；Q2为5A/5B，Q3另起change，Q5下轮插件验证。仍需用户明确批准才能发布。

待裁决：
1. 父提交13c3e223→61ef5d31虽同tree，违反用户本次要求；是否允许以已改接PS4继续？本任务不自行解释NO_CHANGE来豁免。
2. 是否授权另一次导出环境准备修正：确认与90号同模式后，完成导出比较和五项解析。
3. 看门狗早期采样缺口如何补验；不能将未采样期间当作符合阈值的证明。
4. 前置放行后才能在新的隔离位置试合并361624、不解决冲突，并补实际冲突表。当前候选不含它。

放行后推荐路线仍是冻结一个最终tree：补轻量门禁、真实转换重放和最小插件验证，然后一次QB批次（T/D×三个架构）与一次本地T/D完整构建覆盖全部修改，逐包规则B、静态成员SHA、debuglink/LLDB/post、FLAGS与工具版本核对。本任务未执行或授权触发这些重任务。

## 5. 资源、已读/未读与全部STOP

4GiB、swap0、CPU200%、Nice19、IO idle；资源限制未调高。clone/导出缓存触及4GiB；memory.events的OOM项均0。

看门狗启动存在缺口：仅留下首条04:27:18采样，04:45左右复查发现没有持续记录；当时MemAvailable=19520232kB，恢复同一脚本到存活服务shell后有30秒采样。缺口期间是否低于6GiB **UNKNOWN**，不写“全程看门狗通过”。[记录](../../tools/bolt/results/hq-review-361395/round2/watchdog-gap.md)、[采样快照](../../tools/bolt/results/hq-review-361395/round2/watchdog-snapshot.jsonl)、[资源](../../tools/bolt/results/hq-review-361395/round2/resources.json)。

已读：103/101/长期状态、当前query和两份源码对象、所有diff/说明、103草案、保留测试环境/小夹具输入、两次导出文件名和日志。未读QB网站、内部issue29、新构建产物；未运行RPM完整构建/BOLT/真实输入重放；未执行361624试合并；未修改旧工作树、历史根、旧证据或远端LLVM分支。只在新工作树写候选，证据仅推bolt-v4。

STOP原文：

    STOP: 104号导出比较准备脚本期望 0008-*.patch，但两份 gbs export 均为 native source archive；export_parse.py:105 的 next(a.glob('0008-*.patch')) 抛出 StopIteration。本轮准备修正机会已用于定向测试脚本转义，未修改导出配置、未重跑，五项解析 NOT RUN。

    STOP: 104号新增前置门禁不满足：PS3 ecb2dec7 的父提交为 13c3e223d9e1b35e4affb55255c5042f8c940f35；PS4 e9f16ee3 的父提交为 61ef5d31ca91025c414c748477bef0c64ddfa67c。父提交不同；tree相同、说明相同不能代替该门禁。停止候选后续工作，不推送，不执行361624试合并。

[全部raw文件索引](../../tools/bolt/results/hq-review-361395/round2/RAW_LINKS.md)
