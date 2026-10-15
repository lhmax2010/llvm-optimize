# 24 续跑十四：第三轮修复、变基与停止记录

STOP；压缩源提交 `8be7348a6baf9d4b8b55c382b8a04dade712208d`，父 `67619ec8bbbac7238a6cfc33a481ccfbcd12206f`；新分支 sandbox/lhmax2025/bolt_pgo_v2 未推。未启动 QB 或真实树演练。

## 人工裁决与执行边界

采用 PM 第三轮十二项修复、最新 tizen_base 单提交与重新认证要求。保持 profile/生成参数和候选4ec不变，不重生成。原树禁 cmake/ninja/-P，保护归档证据、22普通RPM和ARM树；作者/提交者/Signed-off-by均Hao Lin <hao.lin@samsung.com>，git -c、不改全局。全部门禁通过才允许推新sandbox；本轮有身份门禁失败，立即停止后续产品操作。

## 逐项状态

|项目|结果|
|---|---|
|helper/spec修复、0004|已实现，修复提交91f2ab3618900bb828a228c274d19004681e6d4d；完整patch公开|
|原214测试+38新增|252/252 PASS；stdout为空、stderr全部逐项原文|
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
