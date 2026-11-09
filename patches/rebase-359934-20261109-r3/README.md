# 第三轮代码评审材料（2026-11-09）

**BOLT 代码评审请先读 [0002-text-only.patch](0002-text-only.patch)，无需阅读含 profile 二进制的完整 0002.patch。**

本包只读导出自 sandbox 已核对的 HEAD **c7fd5eed5e35ca335940239cae349a6936f74a7a**，tree **24addd0a47a8e7028fe5561cb4f1153bc293d36a**。本轮仅整理设计和评审材料，不修改 LLVM 源码或提交、不运行构建、不推送 Gerrit/sandbox、不操作 QB。旧评审包保留。

## 基线和应用顺序

依次应用 0001.patch、0002.patch、0003.patch 到 **13c3e223d9e1b35e4affb55255c5042f8c940f35**（[359934](https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/359934)，**PS10，NEW**）。其父提交是 **cf4b6777d056131e2534ecb460c5575327d99646**（[357163](https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/357163)，**NEW**）。

状态引用 2026-11-09 15:54（+08:00）的只读 Gerrit 查询，见 [359934 原文](../../tools/bolt/results/cli-cancel-20261109/change-359934.txt) 和 [357163 原文](../../tools/bolt/results/cli-cancel-20261109/change-357163.txt)。两者并未合入；本包不将它们描述为 tizen_base 已合入基线。

|补丁|提交 SHA|tree|标题|
|---|---|---|---|
|0001.patch|a73a7da32049569b1360e9c13d0633c168b8f173|3d961cbb04f5446f84d2089b4f65f3178f2bd7fa|cmake: use hybrid LLVM linkage on x86_64|
|0002.patch|3dc97ef3a8fae0bbc61b208fa2bc6c369f1146b0|24b6aace2a36bb5840f33ea8fa4da710056ff078|packaging: optimize x86_64 clang with BOLT|
|0003.patch|c7fd5eed5e35ca335940239cae349a6936f74a7a|24addd0a47a8e7028fe5561cb4f1153bc293d36a|packaging: fix x86 LLVM flags and archive mode|

## 文件导览

|文件|用途|Raw|
|---|---|---|
|[0001.patch](0001.patch)|完整的混合链接提交。|[raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/rebase-359934-20261109-r3/0001.patch)|
|[0002-text-only.patch](0002-text-only.patch)|BOLT 评审首选；helper/spec 的全部改动，仅排除 profile 二进制。完整补丁见 0002.patch。|[raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/rebase-359934-20261109-r3/0002-text-only.patch)|
|[0002.patch](0002.patch)|完整 BOLT format-patch，包含 Source1200 二进制，可用于应用。|[raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/rebase-359934-20261109-r3/0002.patch)|
|[0003.patch](0003.patch)|完整的固定参数与归档转换器提交。|[raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/rebase-359934-20261109-r3/0003.patch)|
|[converter-vs-ps10.diff](converter-vs-ps10.diff)|最终转换器相对总部 PS10 的完整 full-index diff。|[raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/rebase-359934-20261109-r3/converter-vs-ps10.diff)|
|[changes-since-7d5e28ca.diff](changes-since-7d5e28ca.diff)|最终版本相对 7d5e28ca 的完整 diff，包含第二轮代码评审修复和 cli 取消漏洞修复。|[raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/rebase-359934-20261109-r3/changes-since-7d5e28ca.diff)|
|[files/](files/)|最终提交的 9 份完整文本，保留原相对路径。|—|
|[provenance.json](provenance.json)|源码身份、移动记录、文件 SHA、导出命令、补丁解析和不变性核对。|[raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/rebase-359934-20261109-r3/provenance.json)|
|[SHA256SUMS](SHA256SUMS)|本目录所有文件的 SHA256（清单自身除外）。|[raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/rebase-359934-20261109-r3/SHA256SUMS)|

### 最终完整文本

|文件|字节数|SHA256|
|---|---:|---|
|[files/packaging/llvm.spec](files/packaging/llvm.spec)|36455|adbf7dc9e9e8efacd441a60eb996a6b39762f1ed3b41ed46b40d960060ef42c8|
|[files/packaging/clang-bolt-helper.py](files/packaging/clang-bolt-helper.py)|119723|62d87ac35a2aa3a355fda59352b328db37dd6601cb902b39fe8cfc4e6a6fb50a|
|[files/packaging/llvm-static-archives-native.py](files/packaging/llvm-static-archives-native.py)|43928|45fd4f25c3258adab0cdb28a97dfc7e28f0c6bf0bb511fb7d060bb0aa1c58fed|
|[files/clang/cmake/modules/AddClang.cmake](files/clang/cmake/modules/AddClang.cmake)|8036|cc505b09c2856008843c430269fb989648090bdcfd1048ab1c2ca16d2c499480|
|[files/clang/tools/driver/CMakeLists.txt](files/clang/tools/driver/CMakeLists.txt)|7526|8b474be5974d61249fb46eb4cca01896582d94ad29377b2b07cd24ebb0591bd5|
|[files/lld/cmake/modules/AddLLD.cmake](files/lld/cmake/modules/AddLLD.cmake)|2862|d43aa8961e5f3a4fd77a2a4b2051e39bea50c643b5a60d403af7c8db68c6a72f|
|[files/lld/tools/lld/CMakeLists.txt](files/lld/tools/lld/CMakeLists.txt)|1443|5ca6faf514eab8626a5f5fea9041899d2b6e79a59efe09edf99791236ef5b3dd|
|[files/llvm/cmake/modules/AddLLVM.cmake](files/llvm/cmake/modules/AddLLVM.cmake)|105993|02222783e87051da8b468a48e411e79a917ac194f4e50939d119f80a8bcfc7b1|
|[files/llvm/tools/llvm-ar/CMakeLists.txt](files/llvm/tools/llvm-ar/CMakeLists.txt)|1025|e7db3ac8c02493dba0df01cd8ba5e3992285af11f2351c1a47fca3f3d3adc49c|

## Source1200

不另附 profile 文件；这里只列身份，完整数据位于 0002.patch。0002-text-only.patch 唯一排除的文件就是这个二进制，helper/spec 改动没有省略。

- 文件名：packaging/clang-bolt-v2.fdata.xz
- 大小：9735212 字节
- SHA256：52fd8522b8cceadebfb6bfc0a19f721f1072cff95c682b12b2c4dd5b0cc1e27f

## 本轮差异与验证边界

相对 7d5e28ca 的差异仅涉及 packaging/clang-bolt-helper.py、packaging/llvm-static-archives-native.py、packaging/llvm.spec。包括：debuglink 的执行布局校验、取消退出码及可选诊断传播、assembler 参数拒绝和三工具版本一致性、固定丢弃清单/警告文本，以及 cli 在取消后的非 GateError 异常中打印 traceback 并返回 128+signal。完整改动见 changes-since-7d5e28ca.diff。

71 号完整 QB 结果针对 **7d5e28ca**，不是本包最终 HEAD：两项目的三个架构成功；34 个二进制包载荷及 7706 个转换成员输出与前组 QB 一致。最终 **c7fd5eed** 的轻量证明见 70 §10：407 项测试和 12 项 T/D spec 展开通过；本轮没有重新构建或补做运行验证。

## 评审背景文档

|文档|用途|Raw|
|---|---|---|
|[48_review_fixes.md](../../docs/bolt/48_review_fixes.md)|早期评审修复、轻量检查与离线门禁复核。|[raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/48_review_fixes.md)|
|[51_second_review_fixes.md](../../docs/bolt/51_second_review_fixes.md)|外部评审修复、参数策略、测试及启动演练。|[raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/51_second_review_fixes.md)|
|[69_rebase_on_359934.md](../../docs/bolt/69_rebase_on_359934.md)|改接总部 PS10 的依据、冲突处理、重放一致性和演练。|[raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/69_rebase_on_359934.md)|
|[70_second_code_review_fixes.md](../../docs/bolt/70_second_code_review_fixes.md)|第二轮代码评审修复；§10 记录 cli 修复、测试与 sandbox 推送。|[raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/70_second_code_review_fixes.md)|
|[71_qb_1221204_1221207.md](../../docs/bolt/71_qb_1221204_1221207.md)|QB 身份、三架构结果、逐包比较及 7706 成员输出证据。|[raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/71_qb_1221204_1221207.md)|

## 设计文档 v4

[tizen_llvm_speed_design_v4.md](../../docs/bolt/design/tizen_llvm_speed_design_v4.md)（[raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/design/tizen_llvm_speed_design_v4.md)）已从 Downloads **移动**到 W/docs/bolt/design/，再以相同字节同步发布到 bolt-v4。

文档 53097 字节，SHA256 2be0c79a48d34d20cb003f87b9c954154b9c92a2c2d103ab0f6f82643f7615f7。正文日期及其中引用的 7d5e28ca 基线均按原件保留，不将文档改写成 c7fd5eed 的设计。W 与 bolt-v4 的 v1/v2 不变；这两个目录未发现 v3，本轮没有创建或修改它。

## 导出与核对

三个完整 format-patch 的 diff 正文逐字节等于各自父子提交的 git diff --full-index --binary；0002 文本版逐字节等于排除 profile 后的父子 diff。9 份全文逐字节等于最终 Git blob，六份 CMake 文件清单取自混合链接提交。所有补丁/diff 均通过 git apply --stat 解析检查，未在源码工作树应用补丁。provenance.json 保存具体命令和核对结果。

所有命令串行运行于独立 systemd 用户服务：MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、nice19、ionice-c3。源码工作树保持干净，未删除任何文件。
