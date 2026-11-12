# 第五轮评审修复材料 r6

BOLT 文本评审请先读 [0002-text-only.patch](0002-text-only.patch)，仅排除 profile 二进制；完整可应用补丁是 0002.patch。按 0001、0002、0003 顺序应用到基线。

## 基线与提交

基线 13c3e223d9e1b35e4affb55255c5042f8c940f35（359934 PS10），父提交 cf4b6777d056131e2534ecb460c5575327d99646（357163 PS2）。359934 为 MERGED/PS10，357163 为 MERGED/PS2，revision 均未变。后续已按新授权推送 sandbox，HEAD=fea0fe464d56e17f2c7588c557bfffd9f6ac352b；tizen_base 判定为 verdict B。历史停止及第五次续跑见 [78号](../../docs/bolt/78_fifth_review_fixes.md)。本地 T/D 完整构建已由 [74号 §8.10 PM 裁决](../../docs/bolt/74_local_full_build_fa4f9978.md#810-pm-裁决)放行；新 QB 1226850/1226851 的结果以79号为准。

|SHA|tree|标题|
|---|---|---|
|8a50d7122346258fd1171d270861a4ae28a8717c|3d961cbb04f5446f84d2089b4f65f3178f2bd7fa|cmake: use hybrid LLVM linkage on x86_64|
|1e415935a83a187aab7c41f9713115a0974a0365|c23914776684bf94fdd5961f447f7c24e7bb79bc|packaging: optimize x86_64 clang with BOLT|
|fea0fe464d56e17f2c7588c557bfffd9f6ac352b|b2e8af2477cf623a945aa80bf8288a262dd4a5a9|packaging: fix x86 LLVM flags and archive mode|

三个 Change-Id 保留，作者、提交者及 Signed-off-by 为 Hao Lin <hao.lin@samsung.com>；说明每行不超过72列。混合链接提交与r5完全相同。

## 评审意见、修改与证据

|意见/问题|实现|证据|
|---|---|---|
|失败诊断也要传递取消状态|spec两处disk-diagnose使用bolt_status_exit|changes-since-60fabc72.diff；78§9的12组展开|
|取消必须在恢复原处理器后决定状态，保持SIG_IGN|helper cli与转换器install_main保存结果/异常，恢复后决策；忽略信号保持忽略|499项回归及R5真实信号夹具，rerun3/r3-r4-r5-tests.log|
|重定位宽度和ELF/ar边界|显式类型宽度表、字段末端、压缩目标大小、CREL/sh_link/数字字段检查|450个QB归档复扫和10个debug ThinLTO归档转换census|
|Commands.run取消边界说明|补进程组/subreaper/离组及不可中断睡眠说明|converter-vs-ps10.diff，最终文件全文|
|本轮测试抓到漏import sys|取消路径触发NameError；仅补import sys归入第三提交，说明不变|78§7、§8；rerun3/import-sys.diff；原失败用例重跑PASS|
|实物核对驱动误比较输出路径|仅排除inspect.path，SHA/成员/节/重定位/计数仍全部比较|rerun4/inspect-path-fix.diff、debug-conversion-summary.json|

证据根：[第五轮结果](../../tools/bolt/results/fifth-review-20261111/)，本次[第四次续跑](../../tools/bolt/results/fifth-review-20261111/rerun4/)。产品源码和产品测试在本次续跑没有再改。

- 同一HEAD已从头通过499/499测试；本次未重复已通过的产品测试。
- 450个QB归档、7728个成员新旧检查一致，转换成员7706，原生22；调试节重定位94400431条，表外类型0。
- 10/10 debug ThinLTO归档新旧输出逐字节相同：1100成员（1093转换、7原生），调试节重定位35560547条，类型1与10；全部重定位7种类型，表外类型0。libclangSema.a复用已有两份输出并重算SHA，其余9个本轮重新转换。
- 12组spec展开、5项RPM解析PASS；ARM/BOLT关闭相对60fabc72字节全同，x86开启仅两处disk-diagnose差异。
- pyflakes未安装，NOT RUN；未联网安装。评审包制作时未运行完整构建、新QB、90 TU或整包重新认证；其后已完成74号本地完整构建与审计，并按 §8.10 放行。原始失败记录保留，见74号。

## 文件导览

|文件|作用|
|---|---|
|0001.patch / 0002.patch / 0003.patch|PATCH 1/3、2/3、3/3的完整补丁|
|0002-text-only.patch|不含profile二进制的BOLT文本补丁|
|changes-since-60fabc72.diff|相对r5 HEAD的完整源码差异|
|converter-vs-ps10.diff|转换器相对总部PS10的完整diff|
|files/|spec/helper/转换器及六个CMake完整文本|
|provenance.json|SHA、tree、提交说明、文件身份、检查范围|
|SHA256SUMS|全部材料SHA256，清单自身除外|

Source1200仅列身份：packaging/clang-bolt-v2.fdata.xz，9735212字节，SHA256 52fd8522b8cceadebfb6bfc0a19f721f1072cff95c682b12b2c4dd5b0cc1e27f。不另放二进制文件，完整内容在0002.patch。

当前设计为[v8](../../docs/bolt/design/tizen_llvm_speed_design_v8.md)；历史背景48、51、69–73、75、77；本轮结果以[78号](../../docs/bolt/78_fifth_review_fixes.md)为准。
下一次QB源码包白名单：llvm.spec、clang-bolt-helper.py、llvm-static-archives-native.py、VCS行；0008必须不变。
