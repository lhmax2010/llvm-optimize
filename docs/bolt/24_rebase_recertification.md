# 24 第三轮修复、变基与十四B重新认证

当前：十四B本地认证全部PASS，sandbox待推；十四B结果在文末。以下十四A记录是保留的历史停止原文，已由十四B的PM裁决纠正来源解释。

STOP；压缩源提交 `8be7348a6baf9d4b8b55c382b8a04dade712208d`，父 `67619ec8bbbac7238a6cfc33a481ccfbcd12206f`；新分支 sandbox/lhmax2025/bolt_pgo_v2 未推。未启动 QB 或真实树演练。

## 人工裁决与执行边界

采用 PM 第三轮十二项修复、最新 tizen_base 单提交与重新认证要求。保持 profile/生成参数和候选4ec不变，不重生成。原树禁 cmake/ninja/-P，保护归档证据、22普通RPM和ARM树；作者/提交者/Signed-off-by均Hao Lin <hao.lin@samsung.com>，git -c、不改全局。全部门禁通过才允许推新sandbox；本轮有身份门禁失败，立即停止后续产品操作。

## 逐项状态

|项目|结果|
|---|---|
|helper/spec修复、0004|已实现，修复提交91f2ab3618900bb828a228c274d19004681e6d4d；完整patch公开|
|原214测试+38新增|252/252 PASS；stdout实为2600字节/5条夹具JSON（原空文件描述撤回），stderr全部逐项原文|
|最后两项日志诊断微调及压缩提交后的全量重测|NOT RUN，停在载荷身份；不得把上述252项冒充最终压缩版本认证|
|新增安装顺序测试方法|已加入，读取实际展开快照；最终测试运行NOT RUN|
|真实link.original更严格检查|PASS，未执行链接|
|普通7df/候选4ec新增安全字段|PASS；RPATH均无，RUNPATH均为$ORIGIN/../lib64:|
|严格CLI离线闭包|PASS：1911边、1791普通、9新phony、111新任务，分类变化0；确切argv、输入SHA和rules子集已发布|
|最新tizen_base|PASS，与预期67619ec8一致；无额外提交，356949未合入|
|压缩单提交及身份|PASS，父为新基线；helper/profile与0004逐字节相同；spec只加基线Source1005/util-linux/转换原文|
|OFF两模式展开|PASS，与新基线debug 20段、release 18段逐字节相同|
|ON两模式安装顺序|PASS：snapshot < compare-root < 转换 < 替换；ON/OFF转换均一次|
|四份新基线post捕获|PASS，平台链逐字节同基线、BOLT尾检最后；debug有FD、release有brp-strip|
|22RPM完整载荷|FAIL，首个RPM与docs35历史记录身份不符，未解包|
|压缩提交上再次全量测试、tiny/双根post|NOT RUN，身份门禁失败后停止；不得沿用旧基线认证冒充本轮|
|maintenance.md完整维护手册|NOT RUN，停止后不继续实现后续步骤|
|新sandbox推送/QB/真实树演练|NOT RUN；新sandbox未查询/未推，不触碰旧分支|

## 阻断原文及身份

`GateError: docs35 RPM SHA changed: /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/RPMS/x86_64/clang-22.1.8-1.x86_64.rpm`

|字段|docs35历史记录|当前只读观测|
|---|---|---|
|字节|310019538|310008958|
|SHA256|82970941d586e91861ebe5afe7d0c99db98e6142bd77e5c2b9d6aaf44c2e2604|6317baba9fd2e1b99d5076d85b08849b556245302618b7d01239c1245d305ed1|

这只证明当前路径的RPM不是docs35登记的同一文件，不推断文件损坏或变化原因。未自行信任新SHA、改载荷、改用其他包或重试门禁。1199098关联Base快照索引仅有12个非debug LLVM包，缺所需10个debug包，故选择PM已授权的docs35完整22包回退；也不把该回退集说成67619ec8新构建物。

共享锁持有44.195秒后释放，失败scope退出并回收；未开始解包、无大文件写入。两个post/宏采集proc挂载均finally卸载，前/中/后mountinfo见execution包。未在原树运行cmake/ninja/-P、未改原RPM或归档证据。

## 准备性错误与测试断言

1. 查AGENTS搜索范围一次过大，遇到其他目录权限拒绝；随后改逐级明确路径，未修改该处文件。
2. 首轮夹具旧语义未同步，作为一类准备错误修正一次：10GiB写入正例改为11GiB free；warning负例改error；另按新约定同步两处英文重生成断言与真实构建标记。首轮260含导入类的重复计数，纠正导入后252个不同测试方法通过；原214方法保留，新增38。
3. 新展开解析器用\s把换行纳入段名，触发KeyError，没有产品差异判定；一次改为水平空白后，两模式OFF及安装顺序全PASS。保留初次stdout/stderr。
4. 发布预检发现包含profile二进制的完整format-patch压缩后仍超10MB公开上限；一次修正为公开文本补丁+已有Source，完整二进制补丁只在E保留。该限制未变更产品门禁。
5. 新安装顺序测试与最后日志诊断修改已保存，尚未作最终全量重跑；停止后不补跑。

## 材料与后续边界

0004保留相对ad8完整format-patch；0000是压缩单提交的完整文本format-patch，profile二进制Source另附既有clang-bolt-v2.fdata.xz。包含二进制的完整format-patch仅留本地：xz后仍超过10,000,000字节公开上限，未上传，身份/大小见source-result；不能把公开文本补丁说成自包含二进制补丁。公开原始helper/spec、两模式六份展开、四post脚本及逐字比较、真实链接/安全结果、完整测试原文、闭包输入SHA与rules子集、失败原文/资源记录。原始脚本与format-patch空白均保留，不纳入人工空白修整。

下一轮需要PM指定可信且可取得的完整普通RPM身份或明确新的处置；本轮不替用户重新授权。压缩提交尚未认证完成，不能启动QB。代码评审材料先提交GitHub bolt-v4；后续启动仍由用户决定。

## 发布材料纠正

发布脚本把默认 format-patch 误当作不含二进制；实际默认包含binary数据。cad1c935提交中0000为12,623,564字节，超过公开单文件10,000,000字节限制。这是可避免的发布准备错误；当前分支已改为显式 --no-binary，完整二进制补丁保留E，不重写已推历史，故cad1c935历史文件仍存在。不得将该历史提交作为符合大小约束的材料pin；最终索引指向纠正后的提交。完整原文与SHA见review4-publication-correction.json。产品认证此前已STOP，未因此恢复任何产品操作或推sandbox。

## 最后发布核对

96个branch/pinned raw URL的HTTP200和字节SHA检查已全部通过，之后独立git ls-remote查询GitHub失败：`Failure when receiving data from the peer`（exit128）。因此HTTP阶段PASS，完整发布核验不是PASS；此前bolt-v4各次push均返回成功。完整错误原文见review4-publication-check.json。查找该日志时曾把W下相对路径用于B工作目录，发现后按已定位的W绝对范围读取；只发生在查找阶段，未影响产品输入或门禁。

## 续跑十四B：RPM来源纠正与阶段1

PM确认上一轮不是产品问题：旧R/RPMS现存docs38试构建22包，6317baba符合docs38附录A；docs35原件在rpms-docs35，经docs38记录的rename保全。按新授权，逐一用docs35附录A核对保全22包大小/SHA，全部一致后完整合并解包。未读取docs38的RPM载荷，未称任何历史集为67619ec8新构建物。

阶段1 PASS：paths_checked=17722、cmake_files_checked=47。Source1005字节相同；spec差异为构建依赖、编译器/优化参数与动态链接配置，%install及之后文本逐字相同，不触及.cmake安装/%files；完整diff与来源身份公开。最终helper文档更新后还会在同根重跑反向检查。

补做GitHub远端查询成功，起点ac56ad25aeda6a96ea5d9488c4b885e60a19d203。本轮查找曾在源子仓库使用W相对路径，发现不存在后在产品操作前改正；查找阶段不计准备错误，原文记录保留。

### 十四B阶段2–3：提交维护说明与全部测试

新压缩源506dc25c86e4e2154150796d10b77b71d71ad6bb，父67619ec8，Change-Id保留，作者/提交者/Signed-off-by均Hao Lin。只更新helper模块docstring的维护说明，去掉提交说明里的内部PM启动流程，维护入口改为helper文件头；其余提交说明不变。AST逐字表示相同（去除docstring及位置属性），spec/profile字节保持。新增4夹具覆盖文件头/可执行AST和两处最终日志诊断细化；252+安装顺序1+新增4=257/257 PASS，stdout 2609字节、stderr完整原文已发布。独立index应用含二进制完整补丁后tree与源提交相同。公开0000用显式--no-binary，profile Source单独保留；完整二进制补丁本地保存，不再误发超限材料。

## 续跑十四B最终本地认证（sandbox待推）

总状态：本地认证PASS。最终源`506dc25c86e4e2154150796d10b77b71d71ad6bb`，父`67619ec8bbbac7238a6cfc33a481ccfbcd12206f`，新sandbox尚未推；材料先GitHub，全部公开后才执行已授权推送。没有启动QB或真实树演练。

|本轮要求|结果|证据前缀tools/bolt/results/review4b-|
|---|---|---|
|保全22RPM对docs35附录A大小/SHA|PASS，22/22；不使用docs38包|RPM-identities.json|
|来源spec/Source1005逐字比对|Source相同；spec仅构建差异，%install及其后逐字相同；准许继续|source-audit.json、llvm.spec.diff、llvm-static-archives-native.py.diff|
|完整合并载荷|PASS，17722路径/47 cmake；旧8be helper及最终helper均检查通过|full-payload-result.json、real-gates.json|
|提交说明两处与嵌入维护|PASS，AST不变、spec/profile不变、Change-Id和Hao Lin署名保持|source-result.json、commit-message-check.json|
|全部夹具|PASS，257=原252+安装顺序1+本轮4；stdout2609字节/5条夹具JSON|tests.stdout.txt、tests.stderr.txt、tests-source-certification.json|
|独立index完整二进制patch应用/整树|PASS，tree一致；完整binary patch仅留E，公开文本patch+Source|tests-source-certification.json|
|OFF两模式与67619ec8逐字展开|PASS，debug 20段/release 18段全部一致|macro-result.json、macro-*.expanded.spec.xz|
|ON两模式顺序及OFF转换保留|PASS，snapshot < compare-root < 转换 < install；ON/OFF转换均一次|macro-result.json|
|四份新生成post脚本|PASS，原平台链逐字一致，BOLT尾检最后；debug有FD、release有brp-strip|post-*.sh、post-capture-result.json|
|7df/4ec安全属性|PASS（包括shndx和RPATH/RUNPATH），无属性丢失；两边均无GNU property/CET|real-gates.json、real-security.stdout.txt|
|三目标tiny|PASS，ordinary/candidate完整.o逐字相同，含--no-default-config|real-gates.json、real-tiny.stdout.txt|
|debug/release双根post、反向检查、compare-root|PASS；注入BOLT工具负例被拒，最终SHA不变|real-gates.json、real-post-*.stdout.txt|
|111描述计划正例+普通任务负例|PASS；真实Ninja未执行|real-tool-plan*.txt、real-gates.json|
|受保护树/RPM、原坏配置/缓存、归档证据|PASS，旧文件及4ec未变，原树未运行cmake/ninja/-P|protection-audit.json|
|维护完整版/23说明/manifest/原文与raw索引|已完成，先公开材料后推sandbox|maintenance.md、draft-manifest.json|
|QB、真实树演练、发布模式完整构建、accel/worker实物身份|NOT RUN，仍需后续现场验证|不得由本轮本地认证冒充|

### 后处理与安全要点

新基线debug平台post 1455字节、release 885字节；四次捕获均只因空BUILDROOT文件清单错误退出，脚本存在且非空，错误均为预期File not found类别，wrapper没有执行%install或平台post。真实双根只执行helper尾检；不把采集当作完整%install实际执行。新helper文件头变更纳入重新采集与真实运行。

候选仍为4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9，普通仍7df0ff90dbca7f99ed6a642546281584dbfaab1528a94abf7a1bb524ca371b2c。本轮不生成候选、不改重链/strip/BOLT参数、不重训profile、不重测先前已认证的性能或120份对象；维持历史工具后备路线。Quickbuild后续应看自己的匹配统计同量级且5%双门禁PASS、tool-plan/真实构建与TF SHA、compare-root、post/包/DWARF/debugsource清单及自身clang性能，不比较本地与QB clang SHA。

### 资源与准备记录

重阶段payload scope 767.609s，共享锁767.617s，cgroup峰2675634176B；准入与运行MemAvailable、每进程VmHWM、swap0/nice/ionice、磁盘预检与scope回收见resources.json及execution包。全部scope回收、各proc挂载finally卸载。单次大写入预检预计写后约316.8GB，实际最低抽样剩余318925639680B，高于30GiB。

查找阶段更正：曾在源子仓库用W相对路径，改正后才进行产品操作；曾查找不存在的十四A real_gates.py，随后定位并复用十三A脚本，执行前适配111描述及现有错误文本。技能清单的符号链接路径经rg --follow/已安装根定位。均未作为产品输入使用，不计准备错误。产品步骤准备错误修正0次，产品门禁失败0次；发布证据描述准备修正1次：撤回stdout为空的错误假设，保留失败断言原文后按实际2600/2609字节及5条JSON纠正说明，不涉及产品代码或门禁。

发布前按ship技能适用检查审阅源差异、身份与新鲜测试：本次可执行代码AST无变化、说明文本变更范围准确，无新增审查问题。用户固定父提交/单提交/写入范围/直接sandbox/不提问规则优先于通用PR与全局状态流程；未扩展为PR、版本变更或其他目录写入。

发布暂存另有一类准备修正一次：显式*.xz包含被忽略的execution.tar.xz，git add返回1，set -e在提交前停止；改为按目录暂存，再对自有证据包显式git add -f。产品代码、测试输出与门禁不变。合计两类发布准备修正各一次，产品准备错误/产品门禁失败均0。
