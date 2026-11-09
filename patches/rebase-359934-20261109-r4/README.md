# 第三轮代码评审修复材料（检查、演练与 sandbox 推送完成）

**BOLT 评审请先读 [0002-text-only.patch](0002-text-only.patch)**，它只排除 Source1200 二进制；完整可应用补丁见 0002.patch。

本包 HEAD 为 **fa4f9978c9162d3c6cd2113d0cfe1173f04881c8**，tree **c9f61c77a1a08f5faffd45f8a37f6b46359922f7**。2026-11-09 已通过指定 force-with-lease 更新 sandbox/lhmax2025/bolt_pgo，推后 ls-remote 相同。三个源码提交和 tree 从第一步完成后未再修改。本轮不完整构建。

## 基线与三个提交

基线 **13c3e223d9e1b35e4affb55255c5042f8c940f35**（359934 PS10），父 **cf4b6777d056131e2534ecb460c5575327d99646**（357163 PS2）。推后查询：两 change 都是 **NEW**，359934 当前仍为 PS10，未变化。原文见 [gerrit/](../../tools/bolt/results/third-code-review-20261109/resume/basedev-finish/gerrit/)。

按下面顺序应用三个完整补丁到基线，不应用到旧 sandbox HEAD：

|补丁|SHA|tree|标题|
|---|---|---|---|
|0001.patch|a65688b1377e91819fcd46a18da36d52b3312089|3d961cbb04f5446f84d2089b4f65f3178f2bd7fa|cmake: use hybrid LLVM linkage on x86_64|
|0002.patch|22f1c9fd79de6086ee21f235868c70167868b7ff|4d78fb7cc802b4815bd04d8e3334ca3a73576dab|packaging: optimize x86_64 clang with BOLT|
|0003.patch|fa4f9978c9162d3c6cd2113d0cfe1173f04881c8|c9f61c77a1a08f5faffd45f8a37f6b46359922f7|packaging: fix x86 LLVM flags and archive mode|

## 本轮修改

- 转换器：ar 长度、名字、对齐边界；PIC 符号表/重定位表步长与索引边界；SIGHUP；WNOWAIT 保留退出组长，最后组信号之后在锁内 wait4 回收；三工具真实目录一致性。
- helper：仅 Rollback 说明，明确 Source1200/1201 仍声明供 GBS 插入补丁。
- spec：bolt_checked 打印已捕获输出后，取消状态 129/130/143 直接退出，不运行磁盘诊断；普通失败行为不变。
- 提交说明按指定文本更新、所有行≤72列、Change-Id/Signed-off-by 为最后独立段。
- 未采纳将混合失败退出码改为 1；仍保持 128+signal，防止 bolt_optional 吞掉取消。

## 文件导览

|文件|用途|
|---|---|
|0001.patch / 0002.patch / 0003.patch|三个完整 format-patch|
|0002-text-only.patch|BOLT 全部文本改动，仅排除 profile 二进制|
|converter-vs-ps10.diff|转换器相对总部 PS10 的完整 diff|
|changes-since-7d5e28ca.diff|第二、三轮修复累计 diff|
|changes-since-c7fd5eed.diff|本轮改动的完整 diff|
|files/|spec、helper、转换器和六个 CMake 文件全文|
|provenance.json|提交身份、检查、演练、sandbox 与 change 状态|
|SHA256SUMS|全部材料 SHA256，清单自身除外|

所有 raw 文件路径为 https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/rebase-359934-20261109-r4/ 加对应文件名。

|完整文本|字节数|SHA256|
|---|---:|---|
|packaging/llvm.spec|36552|b0fe97b9dc5d6d69d8a790a92be05414580deb68eadbe0d1bda9a9837bb03a5b|
|packaging/clang-bolt-helper.py|119789|147ea231341e75eef204d2d9118aab3cc597b95e665c4511a3adf2e49593866f|
|packaging/llvm-static-archives-native.py|45451|ae786dbd2da385a535c60c77c59b6617427d1236010a261b58660e0e9e1d3a92|
|clang/cmake/modules/AddClang.cmake|8036|cc505b09c2856008843c430269fb989648090bdcfd1048ab1c2ca16d2c499480|
|clang/tools/driver/CMakeLists.txt|7526|8b474be5974d61249fb46eb4cca01896582d94ad29377b2b07cd24ebb0591bd5|
|lld/cmake/modules/AddLLD.cmake|2862|d43aa8961e5f3a4fd77a2a4b2051e39bea50c643b5a60d403af7c8db68c6a72f|
|lld/tools/lld/CMakeLists.txt|1443|5ca6faf514eab8626a5f5fea9041899d2b6e79a59efe09edf99791236ef5b3dd|
|llvm/cmake/modules/AddLLVM.cmake|105993|02222783e87051da8b468a48e411e79a917ac194f4e50939d119f80a8bcfc7b1|
|llvm/tools/llvm-ar/CMakeLists.txt|1025|e7db3ac8c02493dba0df01cd8ba5e3992285af11f2351c1a47fca3f3d3adc49c|

Source1200：packaging/clang-bolt-v2.fdata.xz，9735212 字节，SHA256 52fd8522b8cceadebfb6bfc0a19f721f1072cff95c682b12b2c4dd5b0cc1e27f。不另附 profile 文件；完整内容在 0002.patch。

## 验证结论与边界

- 472 项单元测试和真实 release C-2 #5/#6 两项全部通过。
- 两配置展开 12 项、Tizen RPM 解析 5 项通过；ARM/off 相同，x86 on 仅 bolt_checked 改动。
- T/D 各 3853 条重放参数与 c7fd5eed 逐项相同，共 7706。
- 两套 QB 各 225 个静态归档、3864 个成员、3763631 条受检重定位通过，总计 450 归档、7728 成员、7527262 条受检重定位。
- T/D 演练均停在 CMake，未跑 Ninja；log-restarts=0，FLAGS 分别与 QB1221204/1221207 逐字一致，WARNING=0，资源报告正常，无残留进程和挂载。
- 本次 D 日志/副本均 58297 字节。此前测试输入和启动参数错误的原文保留；完成情况以 72 §8–9 为准。

[72 号](../../docs/bolt/72_third_code_review_fixes.md)、[测试证据](../../tools/bolt/results/third-code-review-20261109/resume/)、[Base-Dev 补跑证据](../../tools/bolt/results/third-code-review-20261109/resume/basedev-finish/)。

重放参数全量一致、既有归档门禁通过，不等于本轮新版本整包逐字节认证。本轮未完整构建，也未重新转换全部 7706 个成员；真实 C-2 只重转一个 release 成员及负例。背景文档为 48、51、69、70、71 号。旧评审包保留不动。

## sandbox

推后 HEAD：fa4f9978c9162d3c6cd2113d0cfe1173f04881c8。只推该 sandbox，未推 refs/for，未操作 QB。

后续软件包行：platform/upstream/llvm@fa4f9978c9162d3c6cd2113d0cfe1173f04881c8。
