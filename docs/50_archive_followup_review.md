# 50 x86_64静态归档后续增量评审与升级调查

当前阶段：合入状态核查PASS；新提交生成与上传尚未完成。日期2026-10-14，时间均为北京时间。

证据E=`temp/archive-followup-review-20261014`；已验收最终树为`4c36e899dffee2869af9afd174346e3eb9a7d7ca`，生产Source SHA `c43523c0ce04fc3310e670ff97823db8260c21250dc3172575a18db56500082e`。既有Source、冻结候选补丁、W/gbs配置和已交接x86构建树不修改。本轮不处理ARM根内执行环境。

## 1. tizen_base合入核查

无交互fetch后最新HEAD=`67619ec8bbbac7238a6cfc33a481ccfbcd12206f`，父提交=`cb67996861d070d68fec2b4c623eed7d20ba2e23`。Gerrit查询356627为MERGED、currentPatchSet=2且revision精确等于该HEAD；356639为NEW，patchset1=`b0465d099164a8f8c1ddd406e6f74c2ada8f9f9f`，未合入。

从cb679968之后全部提交只有以下一条，未发现其他提交修改spec或Source：

|提交|作者时间|标题|文件|
|---|---|---|---|
|67619ec8bbbac7238a6cfc33a481ccfbcd12206f|2026-10-09T16:58:36+08:00|packaging: fix llvm-static-devel with ThinLTO|新增packaging/llvm-static-archives-native.py；修改packaging/llvm.spec|

作者时间不是合入时间。上传PS2与合入commit完全相同，逐文件SHA：spec `d93a549206434c4512c60d5a96bfeb133b7aaf6ea13b8cd0302e06c1cb99b1c9`；Source `6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557`。证据merge-check.json、gerrit-status.jsonl、target-commits-since-base.txt、fetch-tizen-base.*。

已验收候选commit保存在此前隔离仓库`temp/release-attribution-20261013/patch-work`。初次只读git diff在W/llvm查询该本地commit得到bad object；随后核实原候选仓库HEAD精确为4c36e899，未更改输入、门禁或任何Source。证据candidate-location.json。合入版到候选的完整二进制diff存E/merged-to-validated.diff，只涉及spec与Source（116插入/17删除）。

## 2. 本轮用户裁决与执行边界

- 新建独立Gerrit change，父为最新tizen_base，将已验收PS3相对合入版的增量与PS2静态库llvm-strip合为一条提交；两份旧候选文件保持冻结。
- 作者FatTank <hao.lin@samsung.com>，只推refs/for/tizen_base，不直推分支、不推sandbox。356639由用户在新change上传后Abandon，本会话不代办。
- 最终packaging内容须与4c36e899同字节，必须完成干净apply检查、实际apply、整树比较、debug/发布两模式rpmspec parse后才能上传。
- 发布完整构建、同环境未打补丁非归档对照仍不能宣称完成；新快照若可用按本轮条件核对。ARM根内小试/64MiB暂停至下周，宿主不修改。
- 资源、项目锁与共享重任务锁、1.2倍/30GiB磁盘规则沿用。开场轻任务内存准入通过，用户gbs配置改动SHA与登记一致。
