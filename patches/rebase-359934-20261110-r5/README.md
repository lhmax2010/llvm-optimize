# 第四轮评审修复材料 r5

BOLT 文本评审请先读 [0002-text-only.patch](0002-text-only.patch)；仅排除 profile 二进制，完整可应用补丁是 0002.patch。本包完成本轮轻量检查与实物门禁复扫，未运行完整构建或推送 sandbox。

## 基线与提交

基线 13c3e223d9e1b35e4affb55255c5042f8c940f35（359934 PS10）及其父 cf4b6777d056131e2534ecb460c5575327d99646（357163）。两 change 的 NEW 状态引用此前记录，本轮未查询 Gerrit。按 0001、0002、0003 顺序应用到基线。

|SHA|tree|标题|
|---|---|---|
|8a50d7122346258fd1171d270861a4ae28a8717c|3d961cbb04f5446f84d2089b4f65f3178f2bd7fa|cmake: use hybrid LLVM linkage on x86_64|
|358615447c2596c30aa6d064fc8c388292e443e4|9e4948eba61ca48156f5b4534f49adaf0f47cab1|packaging: optimize x86_64 clang with BOLT|
|60fabc723f30c5cc04146a9dd83487ebed63f259|90fc87dde4d11c8c57f5d3de45a9995dcc35d5f9|packaging: fix x86 LLVM flags and archive mode|

三个 Change-Id 保持不变，作者、提交者和 Signed-off-by 为 Hao Lin <hao.lin@samsung.com>。完整说明在补丁及 provenance.json，所有行不超过 72 列。

## 修改与检查

- spec：直接调用的 129/130/143 传递，printf 的 RPM 宏转义。BOLT 关闭时转换调用仍 exit 1，展开与 fa4f9978 相同。
- 转换器：ar/ELF/PIC 边界及 8/16 位绝对重定位、版本摘要、取消与 SIGCHLD 处理。R_X86_64_NONE 不做 r_offset 越界检查，其余不变。
- 混合链接仅更新说明；tree 仍为 3d961cbb。helper、Source1200、发布 OPTIONS 和白名单未改。
- 本次修正 module asm 夹具的追加位置，未放宽转换器；487/487 单元测试从头通过，包括此前未运行的三个新增测试和类型 0 用例。
- 12 组展开、5 项 Tizen RPM 解析通过；ARM 和 BOLT 关闭逐字节相同，x86 开启只有退出码传播差异，printf 展开相同。
- 450 归档 / 7728 成员 / 7527262 条受检重定位新旧结果一致；7706 转换成员零拒绝，22 原生成员禁止项只记录、不拦截（本次新旧均为 0）。
- 一个真实 release 成员及完整单成员小归档新旧转换输出逐字节相同。这不是全量重新转换，也不是新版本整包一致证明。
- QB 1223601/1223602 两 ARM 架构的 AddLLVM/AddClang 均等于 fa4f9978，相对 PS10 仅混合链接改动；四组均未安装 AddLLD.cmake。
- x86 初始化日志没有独立 lld 包，未打印 /usr/bin/ld.lld 的包归属查询；不把构建输出中的 ld.lld 链接当作依赖包归属证据。
- 未运行完整构建、演练、90 TU 或新 QB；旧停止记录保留，续跑结果见 [75 号 §6](../../docs/bolt/75_fourth_review_fixes.md#6-续跑2026-11-10)。

## 文件导览

|文件|作用|
|---|---|
|0001.patch / 0002.patch / 0003.patch|带 PATCH 1/3、2/3、3/3 编号的完整补丁|
|0002-text-only.patch|仅排除 profile 二进制的 BOLT 文本补丁|
|changes-since-fa4f9978.diff|第四轮累计完整源码差异|
|converter-vs-ps10.diff|转换器相对总部 PS10 的完整差异|
|files/|最终 spec、helper、转换器及六个 CMake 全文|
|provenance.json|源码身份、完整提交说明、文件 SHA 和检查范围|
|SHA256SUMS|全部材料的 SHA256，清单自身除外|

|完整文本路径|字节数|SHA256|
|---|---:|---|
|packaging/llvm.spec|36919|20f29ee7f81cc487d9c1fdb5000b2ff0bb15e3dc1dc043ea6f886ab465c544e7|
|packaging/clang-bolt-helper.py|119789|147ea231341e75eef204d2d9118aab3cc597b95e665c4511a3adf2e49593866f|
|packaging/llvm-static-archives-native.py|48310|ba441406b107046876db469110f7834e77babe71e86ea60a1dbf01294ac74460|
|clang/cmake/modules/AddClang.cmake|8036|cc505b09c2856008843c430269fb989648090bdcfd1048ab1c2ca16d2c499480|
|clang/tools/driver/CMakeLists.txt|7526|8b474be5974d61249fb46eb4cca01896582d94ad29377b2b07cd24ebb0591bd5|
|lld/cmake/modules/AddLLD.cmake|2862|d43aa8961e5f3a4fd77a2a4b2051e39bea50c643b5a60d403af7c8db68c6a72f|
|lld/tools/lld/CMakeLists.txt|1443|5ca6faf514eab8626a5f5fea9041899d2b6e79a59efe09edf99791236ef5b3dd|
|llvm/cmake/modules/AddLLVM.cmake|105993|02222783e87051da8b468a48e411e79a917ac194f4e50939d119f80a8bcfc7b1|
|llvm/tools/llvm-ar/CMakeLists.txt|1025|e7db3ac8c02493dba0df01cd8ba5e3992285af11f2351c1a47fca3f3d3adc49c|

Source1200 仅另列身份：packaging/clang-bolt-v2.fdata.xz，9735212 字节，SHA256 52fd8522b8cceadebfb6bfc0a19f721f1072cff95c682b12b2c4dd5b0cc1e27f。不另放二进制文件，完整内容在 0002.patch。

设计以 [v6.1](../../docs/bolt/design/tizen_llvm_speed_design_v6.1.md) 为准。历史背景：48、51、69、70、71、72、73；本轮原文和边界见 [75 号](../../docs/bolt/75_fourth_review_fixes.md)及[证据](../../tools/bolt/results/fourth-review-20261110/resume/)。
下一次 QB 源码包白名单：llvm.spec、llvm-static-archives-native.py、VCS 行、第一个提交说明改动带来的 0008 补丁变化。最终发货一致仍待授权后的 QB 验证。
