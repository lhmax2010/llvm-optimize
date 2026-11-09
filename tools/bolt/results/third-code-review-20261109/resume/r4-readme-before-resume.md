# 第三轮代码评审修复材料（未完成验证）

**本包未达到推送条件，未推送 sandbox。** 第二步在 70 号夹具初始化时失败：本轮普通 rpmspec -P 输出未显式展开 __spec_install_post，只找到 4 个可选调用，夹具要求 5 个。尚未执行这 12 项，也未继续其余测试或演练。详见 [72 号](../../docs/bolt/72_third_code_review_fixes.md)。

BOLT 评审请读 [0002-text-only.patch](0002-text-only.patch)。它只排除 profile 二进制；完整可应用补丁为 0002.patch。旧 r3 包保留不动。

## 基线与三个本地提交

基线 13c3e223d9e1b35e4affb55255c5042f8c940f35（359934 PS10），父 cf4b6777d056131e2534ecb460c5575327d99646（357163）。两 change 的 **NEW** 状态引用 2026-11-09 15:54 +08:00 的历史查询，见 [359934](../../tools/bolt/results/cli-cancel-20261109/change-359934.txt)、[357163](../../tools/bolt/results/cli-cancel-20261109/change-357163.txt)。本轮因测试停止，没有重新查询状态或当前 patch set；不将历史状态冒充当前查询。

|补丁|SHA|tree|标题|
|---|---|---|---|
|0001.patch|a65688b1377e91819fcd46a18da36d52b3312089|3d961cbb04f5446f84d2089b4f65f3178f2bd7fa|cmake: use hybrid LLVM linkage on x86_64|
|0002.patch|22f1c9fd79de6086ee21f235868c70167868b7ff|4d78fb7cc802b4815bd04d8e3334ca3a73576dab|packaging: optimize x86_64 clang with BOLT|
|0003.patch|fa4f9978c9162d3c6cd2113d0cfe1173f04881c8|c9f61c77a1a08f5faffd45f8a37f6b46359922f7|packaging: fix x86 LLVM flags and archive mode|

三个 Change-Id 保留；第一提交只折行说明，tree 不变。按序应用到上述基线；不应用到旧 sandbox HEAD 上。

## 本轮改动

- 转换器：ar 长度/名字/对齐边界；符号表、重定位步长及符号索引边界；SIGHUP；waitid(WNOWAIT) 保留组长，最后一次组信号后在锁内 wait4 回收；三工具真实目录一致性。
- helper：只修改 Rollback 说明，明确 Source1200/1201 保持声明。
- spec：bolt_checked 保存失败退出码，取消状态 129/130/143 打印捕获输出后直接退出，其他失败仍诊断后退出 1。
- 提交说明：用户指定文本、72 列折行、两个 trailer 单独为最后一段。
- 未采纳把混合失败退出码改成 1：会让 bolt_optional 吞掉取消；保持 128+signal。

## 文件

|文件|用途|
|---|---|
|0001.patch / 0002.patch / 0003.patch|三个完整 format-patch，按上述顺序应用|
|0002-text-only.patch|BOLT 文本改动，只排除 profile 二进制|
|converter-vs-ps10.diff|转换器相对总部 PS10 的完整 diff|
|changes-since-7d5e28ca.diff|第二、三轮修复的累计 diff|
|changes-since-c7fd5eed.diff|本轮相对入口 HEAD 的完整 diff|
|files/|spec、helper、转换器、六个 CMake 文件最终全文|
|provenance.json|源码身份、提交说明元数据及停止边界|
|SHA256SUMS|所有材料的 SHA256，清单自身除外|

所有 raw 路径为：https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/rebase-359934-20261109-r4/<文件名>。

|全文文件|字节数|SHA256|
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

Source1200：packaging/clang-bolt-v2.fdata.xz，9735212 字节，SHA256 52fd8522b8cceadebfb6bfc0a19f721f1072cff95c682b12b2c4dd5b0cc1e27f。不单独复制二进制；完整内容保留在 0002.patch。

## 证据与验证边界

本轮通过 helper 393 项、两配置完整展开 12 项、Tizen RPM 解析 5 项。ARM 与 BOLT 关闭展开相同；x86 BOLT 开启只差 bolt_checked。这些结果不代表新转换器取消、畸形输入、重放参数及全部实物归档检查已通过。

[72 号](../../docs/bolt/72_third_code_review_fixes.md) 与 [本轮原始证据](../../tools/bolt/results/third-code-review-20261109/) 给出停止原因。历史评审背景为 48、51、69、70、71 号；历史完整构建/7706 成员结论不转用为本轮转换器的认证。
