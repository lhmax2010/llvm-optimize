# 65：历史目录第二组只读盘点（2026-11-05）

64号清理已经结束，本轮没有删除、移动、改写任何被分析文件，也没有运行构建或sudo。只把已核对的重复副本、可从保留RPM重新解包的载荷及已发布源码的临时导出列为瘦身候选；原始RPM、profiles、未发布探针提交、认证products和尚未归档的报告均保留。A/B存在权限盲区，不能把可读部分的du或Git扫描当成整根完整审计。

文档引用基准：bolt-v4 `b3a20dd5377d3ddbadfe1c4e818086913dd2bbf9`；main `613fa5ee8703c14f56e0b682bf0910f639f48ec9`。本次共有528个RPM路径，525个取得SHA，3个限时超时记UNKNOWN。另对QB保留目录的39个RPM做大小筛选；已取得SHA的候选中仅1个同大小，SHA不同，没有证实同SHA替代包，见qb-size-candidate-check.json。

## 1. 方法、边界与证据

W为`/home/linhao/Toolchain/development/llvm-optimize`；目录均相对`W/temp/`。只读扫描使用nice19/ionice-c3；du整根180s、一级子目录90s、细分60s，sha256sum逐文件120s（小证据30s）。超时/权限错误原样保存，记UNKNOWN，不拿历史大小补值。证据写入本次结果目录；被检查目录未写入。64号结束行在[previous-finished.txt](../../tools/bolt/results/disk-review-group2-20261105/previous-finished.txt)。
一级du是各子目录单独计算，可能重复计算共享硬链接，**不能直接相加**。建议释放量只算已确认候选的唯一文件数据块，若硬链接还有清单外名字则不计释放，不计目录元数据；不是删除后df实测。建议保留大小为本次du减这个保守文件块值，盲区目录仍只是可读下界。所有候选只是一份建议，未来实际操作前还须逐项授权并重新查占用/挂载/仓库依赖。
RPM清单包含所有可读命中的RPM，而不是只列LLVM包；每个文件的名字、大小、SHA、同SHA其他位置在各节链接的rpm.tsv。重复检索范围是W/temp可读目录与本次13个目录；全树索引限时480s，权限/超时见duplicate-candidate-index.json。未找到副本仅表示该范围内未证实，不冒充全盘唯一；未对所有旧自构建RPM逐个探测公开下载站，因此无法证明可下载的原始RPM一律保留。
引用检索覆盖main/bolt-v4的docs及tools中所有可读.py/.sh/.conf（含被gitignore的历史结果脚本），逐条文件与行号另列reference-index.md，完整命中原文gzip保留。55–63号中不存在的文档不造内容；生成报告/历史检查脚本的引用与仍会执行的入口应区别看待。路径无命中不等于任意动态拼接路径均已证明无依赖。
另读/proc的cwd/root/exe/fd，只见本轮扫描器打开目标文件，未见可见外部占用；有权限盲区，不能证明全机无占用，详见usage.json。未执行sudo。
Git按原要求保存branches/tags相对remote-tracking refs的日志，另查detached HEAD、stash ref、tracked status、worktrees/alternates；对LLVM再只读ls-remote核对Gerrit所有可见refs（含评审refs），只使用本仓库已存在的commit对象，不fetch、不改ref/config。首版stdin排除写法不正确，保留失败/中间结果；结论仅用git-remote-followup-v2.json及带^的排除查询。无远端的临时探针仓库按未发布保留，不宣称查询了不存在的全世界远端。

## 2. A：`gbs-root-x86_64-debuginfo-j4-v2`

BOLT v2旧认证根R1；f111162e普通/重链/插桩工具来源。16号当时插桩与优化成功，正式ARM耗时降低15.396%；59号本日仍复用其merge-fdata/runtime。
出处：main/docs/16_bolt_final.md:3–40；docs/bolt/59_pgo_bolt_followup.md:73–82。

当前du：**84.157 GiB (90,363,416,576 B)**；有权限/扫描盲区，仅可读下界，完整值UNKNOWN。

一级子目录（完整顶层文件和目录清单见inventory.json）：

|子目录|du GiB|类型/用途|
|---|---:|---|
|`local`|84.157（盲区/失败，见原文）|构建根/缓存（不等于可直接删除）|

可读文件208,520；RPM路径27；发现Git仓库0。扫描错误：[Errno 13] Permission denied: '/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade'；[Errno 13] Permission denied: '/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig'；[Errno 13] Permission denied: '/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0/root'

全部RPM与副本核对：[rpm.tsv](../../tools/bolt/results/disk-review-group2-20261105/gbs-root-x86_64-debuginfo-j4-v2/rpm.tsv)；工具/profile/products等关键资产：[assets.tsv](../../tools/bolt/results/disk-review-group2-20261105/gbs-root-x86_64-debuginfo-j4-v2/assets.tsv)；全部文件元数据：[files.jsonl.gz](../../tools/bolt/results/disk-review-group2-20261105/gbs-root-x86_64-debuginfo-j4-v2/files.jsonl.gz)。

RPM本次SHA已取得27/27；UNKNOWN 0；0个路径找到其他同SHA位置（包括同目录的其他名字，不等于可释放独立数据块）。未查到副本或超时的原包全部保留。

可读范围未发现Git仓库；若本节有权限盲区，不据此宣称盲区也没有仓库。

顶层关键文本/脚本0份，其中0份找到Git跟踪的同名同SHA副本；其余不推断已归档，一律纳入保留清单。逐文件路径/大小/SHA：[small-evidence.json](../../tools/bolt/results/disk-review-group2-20261105/gbs-root-x86_64-debuginfo-j4-v2/small-evidence.json)。

当前引用检索：脚本5处；55–63号文档1处。
逐条位置与原文：[reference-index.md](../../tools/bolt/results/disk-review-group2-20261105/gbs-root-x86_64-debuginfo-j4-v2/reference-index.md)。

**结论：必须保留。** 历史工具、普通clang/RPM和运行环境仍有引用；只有merge-fdata/runtime已证实复制到59号tools，不代表全部84GiB都已保全。权限盲区未消除，保留整根。A的lto.cache已不存在，不能再次按旧91.6GiB计算可释放量。
建议保留：[gbs-root-x86_64-debuginfo-j4-v2/retain-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/gbs-root-x86_64-debuginfo-j4-v2/retain-files.tsv.gz)逐路径列出，84.157 GiB (90,363,416,576 B)（与本节du相同盲区口径）。建议移除文件清单：[suggested-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/gbs-root-x86_64-debuginfo-j4-v2/suggested-files.tsv.gz)，共0条；预计释放文件块 **0.000 GiB (0 B)**。

构建目录细分：完整du原文见[deep-sizes.json](../../tools/bolt/results/disk-review-group2-20261105/deep-sizes.json)。A的build/bin为46,543,589,376 B、build/lib64为14,953,287,680 B；B分别为48,569,888,768 B和14,804,201,472 B。A的lto.cache已不存在，B现存仅17,752,064 B；当前大户主要是工具二进制及构建对象，不能套用旧缓存97GB的估算。

## 3. B：`gbs-root-x86_64-archivefix-v2`

Rnew：x86静态归档修复及llvm-strip验证环境；docs35完成22 RPM和225开发归档验收，docs38/51继续研究GNU/LLVM strip差异；不是新的QB同快照基线。
出处：main/docs/38_llvm_strip_x86_64.md:27；main/docs/40_arm_archive_conversion_stage1.md:75；docs/bolt/31_build_root_inventory.md:94–96。

当前du：**79.287 GiB (85,133,877,248 B)**；有权限/扫描盲区，仅可读下界，完整值UNKNOWN。

一级子目录（完整顶层文件和目录清单见inventory.json）：

|子目录|du GiB|类型/用途|
|---|---:|---|
|`local`|79.287（盲区/失败，见原文）|构建根/缓存（不等于可直接删除）|

可读文件236,374；RPM路径154；发现Git仓库0。扫描错误：[Errno 13] Permission denied: '/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0/usr/share/upgrade'；[Errno 13] Permission denied: '/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0/var/cache/ldconfig'；[Errno 13] Permission denied: '/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0/root'

全部RPM与副本核对：[rpm.tsv](../../tools/bolt/results/disk-review-group2-20261105/gbs-root-x86_64-archivefix-v2/rpm.tsv)；工具/profile/products等关键资产：[assets.tsv](../../tools/bolt/results/disk-review-group2-20261105/gbs-root-x86_64-archivefix-v2/assets.tsv)；全部文件元数据：[files.jsonl.gz](../../tools/bolt/results/disk-review-group2-20261105/gbs-root-x86_64-archivefix-v2/files.jsonl.gz)。

RPM本次SHA已取得152/154；UNKNOWN 2；111个路径找到其他同SHA位置（包括同目录的其他名字，不等于可释放独立数据块）。未查到副本或超时的原包全部保留。

可读范围未发现Git仓库；若本节有权限盲区，不据此宣称盲区也没有仓库。

顶层关键文本/脚本0份，其中0份找到Git跟踪的同名同SHA副本；其余不推断已归档，一律纳入保留清单。逐文件路径/大小/SHA：[small-evidence.json](../../tools/bolt/results/disk-review-group2-20261105/gbs-root-x86_64-archivefix-v2/small-evidence.json)。

当前引用检索：脚本31处；55–63号文档0处。
逐条位置与原文：[reference-index.md](../../tools/bolt/results/disk-review-group2-20261105/gbs-root-x86_64-archivefix-v2/reference-index.md)。

**结论：必须保留。** 旧普通clang、工具/安装环境仍被归档和historical launcher引用；其RPM不是QB新快照同SHA的当然替代品。权限盲区未消除，保留整根；现lto.cache只有本次deep-sizes记录的大小。
建议保留：[gbs-root-x86_64-archivefix-v2/retain-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/gbs-root-x86_64-archivefix-v2/retain-files.tsv.gz)逐路径列出，79.287 GiB (85,133,877,248 B)（与本节du相同盲区口径）。建议移除文件清单：[suggested-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/gbs-root-x86_64-archivefix-v2/suggested-files.tsv.gz)，共0条；预计释放文件块 **0.000 GiB (0 B)**。

构建目录细分：完整du原文见[deep-sizes.json](../../tools/bolt/results/disk-review-group2-20261105/deep-sizes.json)。A的build/bin为46,543,589,376 B、build/lib64为14,953,287,680 B；B分别为48,569,888,768 B和14,804,201,472 B。A的lto.cache已不存在，B现存仅17,752,064 B；当前大户主要是工具二进制及构建对象，不能套用旧缓存97GB的估算。

## 4. C1：`arm-archive-tls-thumb-20261010`

ARM TLS/Thumb修复和两架构全量转换/消费者实验；210/212档转换及原消费者/strip证据是后续回归对照。
出处：main/docs/40_arm_archive_conversion_stage1.md:2051–2209、2490–2578；main/docs/49_x86_build_resume_result.md:262–284。

当前du：**30.505 GiB (32,754,786,304 B)**；本目录遍历无权限错误。

一级子目录（完整顶层文件和目录清单见inventory.json）：

|子目录|du GiB|类型/用途|
|---|---:|---|
|`__pycache__`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-build`|0.082|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-consumers-gnu`|0.015|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-consumers-gnu-scope`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-consumers-llvm`|0.015|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-consumers-llvm-scope`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-consumers-native`|0.021|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-consumers-native-scope`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-conversion`|6.861|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-conversion-scope`|0.003|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-full-census`|0.004|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-full-census-scope`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-init`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-input`|4.919|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-ir-census`|0.128|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-ir-census-scope`|0.001|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-native-census`|0.051|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-native-census-scope`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-strip-gnu`|0.003|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-strip-gnu-scope`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-strip-llvm`|0.003|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-strip-llvm-scope`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-tool-wrappers`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`armv7l-census-scope`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`armv7l-consumers-gnu-scope`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`armv7l-consumers-llvm-scope`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`armv7l-consumers-native-rerun-scope`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`armv7l-consumers-native-scope`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`armv7l-conversion`|4.666|实验输入、结果或辅助脚本；具体见文件清单|
|`armv7l-conversion-scope`|0.005|实验输入、结果或辅助脚本；具体见文件清单|
|`armv7l-full-census`|0.003|实验输入、结果或辅助脚本；具体见文件清单|
|`armv7l-strip-gnu-scope`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`armv7l-strip-llvm-scope`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`consumers-gnu`|0.020|实验输入、结果或辅助脚本；具体见文件清单|
|`consumers-llvm`|0.019|实验输入、结果或辅助脚本；具体见文件清单|
|`consumers-native`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`consumers-native-rerun`|0.027|实验输入、结果或辅助脚本；具体见文件清单|
|`local-dynamic-fixture`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`real-fixtures`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`real-fixtures-final`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`strip-gnu`|0.003|实验输入、结果或辅助脚本；具体见文件清单|
|`strip-llvm`|0.003|实验输入、结果或辅助脚本；具体见文件清单|
|`x86-conversion`|6.814|实验输入、结果或辅助脚本；具体见文件清单|
|`x86-final-conversion`|6.814|实验输入、结果或辅助脚本；具体见文件清单|
|`x86-final-regression-scope`|0.004|实验输入、结果或辅助脚本；具体见文件清单|
|`x86-regression-scope`|0.003|实验输入、结果或辅助脚本；具体见文件清单|

可读文件317,904；RPM路径0；发现Git仓库0。扫描错误：无

全部RPM与副本核对：[rpm.tsv](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-tls-thumb-20261010/rpm.tsv)；工具/profile/products等关键资产：[assets.tsv](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-tls-thumb-20261010/assets.tsv)；全部文件元数据：[files.jsonl.gz](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-tls-thumb-20261010/files.jsonl.gz)。

RPM本次SHA已取得0/0；UNKNOWN 0；0个路径找到其他同SHA位置（包括同目录的其他名字，不等于可释放独立数据块）。未查到副本或超时的原包全部保留。

可读范围未发现Git仓库；若本节有权限盲区，不据此宣称盲区也没有仓库。

顶层关键文本/脚本149份，其中0份找到Git跟踪的同名同SHA副本；其余不推断已归档，一律纳入保留清单。逐文件路径/大小/SHA：[small-evidence.json](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-tls-thumb-20261010/small-evidence.json)。

当前引用检索：脚本1处；55–63号文档0处。
逐条位置与原文：[reference-index.md](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-tls-thumb-20261010/reference-index.md)。

**结论：必须保留。** 保留ARM输入、完整已认证转换结果及消费者/strip证据，作为其他重复档的保留对照。不能因离线通过便删除未完成根内认证所需输入。
建议保留：[arm-archive-tls-thumb-20261010/retain-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-tls-thumb-20261010/retain-files.tsv.gz)逐路径列出，30.505 GiB (32,754,786,304 B)（与本节du相同盲区口径）。建议移除文件清单：[suggested-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-tls-thumb-20261010/suggested-files.tsv.gz)，共0条；预计释放文件块 **0.000 GiB (0 B)**。

## 5. C2：`arm-source-root-probes-20261010`

ARM Source与根内约束探针；保留三架构转换结果、TLS/module-asm探针及原始诊断。
出处：main/docs/44_arm_source_review_round1.md:27；main/docs/46_review_round3_package.md:19。

当前du：**18.378 GiB (19,733,180,416 B)**；本目录遍历无权限错误。

一级子目录（完整顶层文件和目录清单见inventory.json）：

|子目录|du GiB|类型/用途|
|---|---:|---|
|`aarch64-conversion`|6.862|实验输入、结果或辅助脚本；具体见文件清单|
|`aarch64-conversion-scope`|0.003|实验输入、结果或辅助脚本；具体见文件清单|
|`armv7l-conversion`|4.668|实验输入、结果或辅助脚本；具体见文件清单|
|`armv7l-conversion-scope`|0.005|实验输入、结果或辅助脚本；具体见文件清单|
|`tls-105-106`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`tls-fixture-scope`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`x86-final-conversion`|6.814|实验输入、结果或辅助脚本；具体见文件清单|
|`x86-module-asm`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`x86-module-asm-retry`|0.022|实验输入、结果或辅助脚本；具体见文件清单|
|`x86-regression-scope`|0.003|实验输入、结果或辅助脚本；具体见文件清单|
|`x86-symbol-retry-scope`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`x86-symbol-scope`|0.000|实验输入、结果或辅助脚本；具体见文件清单|

可读文件241,408；RPM路径0；发现Git仓库0。扫描错误：无

全部RPM与副本核对：[rpm.tsv](../../tools/bolt/results/disk-review-group2-20261105/arm-source-root-probes-20261010/rpm.tsv)；工具/profile/products等关键资产：[assets.tsv](../../tools/bolt/results/disk-review-group2-20261105/arm-source-root-probes-20261010/assets.tsv)；全部文件元数据：[files.jsonl.gz](../../tools/bolt/results/disk-review-group2-20261105/arm-source-root-probes-20261010/files.jsonl.gz)。

RPM本次SHA已取得0/0；UNKNOWN 0；0个路径找到其他同SHA位置（包括同目录的其他名字，不等于可释放独立数据块）。未查到副本或超时的原包全部保留。

可读范围未发现Git仓库；若本节有权限盲区，不据此宣称盲区也没有仓库。

顶层关键文本/脚本93份，其中0份找到Git跟踪的同名同SHA副本；其余不推断已归档，一律纳入保留清单。逐文件路径/大小/SHA：[small-evidence.json](../../tools/bolt/results/disk-review-group2-20261105/arm-source-root-probes-20261010/small-evidence.json)。

当前引用检索：脚本2处；55–63号文档0处。
逐条位置与原文：[reference-index.md](../../tools/bolt/results/disk-review-group2-20261105/arm-source-root-probes-20261010/reference-index.md)。

**结论：瘦身。** 仅建议移除已逐文件SHA证实等于C1保留副本的归档；组检查超时未完成的其余档、members/summary、TLS/module-asm探针全部保留。
建议保留：[arm-source-root-probes-20261010/retain-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/arm-source-root-probes-20261010/retain-files.tsv.gz)逐路径列出，6.440 GiB (6,914,539,520 B)（与本节du相同盲区口径）。建议移除文件清单：[suggested-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/arm-source-root-probes-20261010/suggested-files.tsv.gz)，共494条；预计释放文件块 **11.938 GiB (12,818,640,896 B)**。

候选边界/原因（文件级重复项完整列表在recommendation.json）：

- `/home/linhao/Toolchain/development/llvm-optimize/temp/arm-source-root-probes-20261010/x86-final-conversion/archives/usr/lib64/libLLVMAArch64AsmParser.a`：same-SHA duplicate; retained /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-tls-thumb-20261010/x86-final-conversion/archives/usr/lib64/libLLVMAArch64AsmParser.a
- `/home/linhao/Toolchain/development/llvm-optimize/temp/arm-source-root-probes-20261010/x86-final-conversion/archives/usr/lib64/libLLVMAArch64CodeGen.a`：same-SHA duplicate; retained /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-tls-thumb-20261010/x86-final-conversion/archives/usr/lib64/libLLVMAArch64CodeGen.a
- `/home/linhao/Toolchain/development/llvm-optimize/temp/arm-source-root-probes-20261010/x86-final-conversion/archives/usr/lib64/libLLVMAArch64Desc.a`：same-SHA duplicate; retained /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-tls-thumb-20261010/x86-final-conversion/archives/usr/lib64/libLLVMAArch64Desc.a
- `/home/linhao/Toolchain/development/llvm-optimize/temp/arm-source-root-probes-20261010/x86-final-conversion/archives/usr/lib64/libLLVMAArch64Disassembler.a`：same-SHA duplicate; retained /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-tls-thumb-20261010/x86-final-conversion/archives/usr/lib64/libLLVMAArch64Disassembler.a
- `/home/linhao/Toolchain/development/llvm-optimize/temp/arm-source-root-probes-20261010/x86-final-conversion/archives/usr/lib64/libLLVMAArch64Info.a`：same-SHA duplicate; retained /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-tls-thumb-20261010/x86-final-conversion/archives/usr/lib64/libLLVMAArch64Info.a
- `/home/linhao/Toolchain/development/llvm-optimize/temp/arm-source-root-probes-20261010/x86-final-conversion/archives/usr/lib64/libLLVMAArch64Utils.a`：same-SHA duplicate; retained /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-tls-thumb-20261010/x86-final-conversion/archives/usr/lib64/libLLVMAArch64Utils.a
- `/home/linhao/Toolchain/development/llvm-optimize/temp/arm-source-root-probes-20261010/x86-final-conversion/archives/usr/lib64/libLLVMABI.a`：same-SHA duplicate; retained /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-tls-thumb-20261010/x86-final-conversion/archives/usr/lib64/libLLVMABI.a
- `/home/linhao/Toolchain/development/llvm-optimize/temp/arm-source-root-probes-20261010/x86-final-conversion/archives/usr/lib64/libLLVMARMAsmParser.a`：same-SHA duplicate; retained /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-tls-thumb-20261010/x86-final-conversion/archives/usr/lib64/libLLVMARMAsmParser.a
- 其余486条逐文件列于[recommendation.json](../../tools/bolt/results/disk-review-group2-20261105/arm-source-root-probes-20261010/recommendation.json)；不能扩展为删除整个父目录。

## 6. C3：`arm-archive-stage1-20261010`

ARM第一阶段的x86不变性回归；225归档转换PASS，ARM环境阶段随后独立推进。
出处：main/docs/40_arm_archive_conversion_stage1.md:55–118；main/docs/46_review_round3_package.md:20。

当前du：**11.923 GiB (12,802,723,840 B)**；本目录遍历无权限错误。

一级子目录（完整顶层文件和目录清单见inventory.json）：

|子目录|du GiB|类型/用途|
|---|---:|---|
|`c0-preflight`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`x86-conversion`|6.814|实验输入、结果或辅助脚本；具体见文件清单|
|`x86-input`|5.106|实验输入、结果或辅助脚本；具体见文件清单|
|`x86-regression-scope`|0.002|实验输入、结果或辅助脚本；具体见文件清单|

可读文件67,828；RPM路径0；发现Git仓库0。扫描错误：无

全部RPM与副本核对：[rpm.tsv](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-stage1-20261010/rpm.tsv)；工具/profile/products等关键资产：[assets.tsv](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-stage1-20261010/assets.tsv)；全部文件元数据：[files.jsonl.gz](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-stage1-20261010/files.jsonl.gz)。

RPM本次SHA已取得0/0；UNKNOWN 0；0个路径找到其他同SHA位置（包括同目录的其他名字，不等于可释放独立数据块）。未查到副本或超时的原包全部保留。

可读范围未发现Git仓库；若本节有权限盲区，不据此宣称盲区也没有仓库。

顶层关键文本/脚本30份，其中0份找到Git跟踪的同名同SHA副本；其余不推断已归档，一律纳入保留清单。逐文件路径/大小/SHA：[small-evidence.json](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-stage1-20261010/small-evidence.json)。

当前引用检索：脚本1处；55–63号文档0处。
逐条位置与原文：[reference-index.md](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-stage1-20261010/reference-index.md)。

**结论：瘦身。** 仅建议移除已逐文件SHA证实等于C1的归档副本；x86原始输入及全部文本证据保留。
建议保留：[arm-archive-stage1-20261010/retain-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-stage1-20261010/retain-files.tsv.gz)逐路径列出，5.957 GiB (6,396,665,856 B)（与本节du相同盲区口径）。建议移除文件清单：[suggested-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-stage1-20261010/suggested-files.tsv.gz)，共215条；预计释放文件块 **5.966 GiB (6,406,057,984 B)**。

候选边界/原因（文件级重复项完整列表在recommendation.json）：

- `/home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-stage1-20261010/x86-conversion/archives/usr/lib64/libLLVMAArch64AsmParser.a`：same-SHA duplicate; retained /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-tls-thumb-20261010/x86-final-conversion/archives/usr/lib64/libLLVMAArch64AsmParser.a
- `/home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-stage1-20261010/x86-conversion/archives/usr/lib64/libLLVMAArch64CodeGen.a`：same-SHA duplicate; retained /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-tls-thumb-20261010/x86-final-conversion/archives/usr/lib64/libLLVMAArch64CodeGen.a
- `/home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-stage1-20261010/x86-conversion/archives/usr/lib64/libLLVMAArch64Desc.a`：same-SHA duplicate; retained /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-tls-thumb-20261010/x86-final-conversion/archives/usr/lib64/libLLVMAArch64Desc.a
- `/home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-stage1-20261010/x86-conversion/archives/usr/lib64/libLLVMAArch64Disassembler.a`：same-SHA duplicate; retained /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-tls-thumb-20261010/x86-final-conversion/archives/usr/lib64/libLLVMAArch64Disassembler.a
- `/home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-stage1-20261010/x86-conversion/archives/usr/lib64/libLLVMAArch64Info.a`：same-SHA duplicate; retained /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-tls-thumb-20261010/x86-final-conversion/archives/usr/lib64/libLLVMAArch64Info.a
- `/home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-stage1-20261010/x86-conversion/archives/usr/lib64/libLLVMAArch64Utils.a`：same-SHA duplicate; retained /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-tls-thumb-20261010/x86-final-conversion/archives/usr/lib64/libLLVMAArch64Utils.a
- `/home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-stage1-20261010/x86-conversion/archives/usr/lib64/libLLVMABI.a`：same-SHA duplicate; retained /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-tls-thumb-20261010/x86-final-conversion/archives/usr/lib64/libLLVMABI.a
- `/home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-stage1-20261010/x86-conversion/archives/usr/lib64/libLLVMARMAsmParser.a`：same-SHA duplicate; retained /home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-tls-thumb-20261010/x86-final-conversion/archives/usr/lib64/libLLVMARMAsmParser.a
- 其余207条逐文件列于[recommendation.json](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-stage1-20261010/recommendation.json)；不能扩展为删除整个父目录。

## 7. C4：`arm-archive-stage1-c-newrepo-20261010`

C0新根路由/极小包、C1原源码导出与accel输入；两个C0通过，旧导出校验错误保留，后续标准构建在其他根继续。
出处：main/docs/40_arm_archive_conversion_stage1.md:627–844。

当前du：**9.236 GiB (9,917,100,032 B)**；本目录遍历无权限错误。

一级子目录（完整顶层文件和目录清单见inventory.json）：

|子目录|du GiB|类型/用途|
|---|---:|---|
|`accel-check`|6.364|构建根/缓存（不等于可直接删除）|
|`c0-aarch64`|0.002|实验输入、结果或辅助脚本；具体见文件清单|
|`c0-armv7l`|0.002|实验输入、结果或辅助脚本；具体见文件清单|
|`c0-package-aarch64`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`c0-package-armv7l`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`c1-export`|0.403|实验输入、结果或辅助脚本；具体见文件清单|
|`c1-export-repository`|2.438|实验输入、结果或辅助脚本；具体见文件清单|
|`c1-source-export`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`host-init`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`macro-precheck`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`repositories`|0.025|实验输入、结果或辅助脚本；具体见文件清单|
|`required-reading`|0.000|实验输入、结果或辅助脚本；具体见文件清单|

可读文件169,476；RPM路径2；发现Git仓库3。扫描错误：无

全部RPM与副本核对：[rpm.tsv](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-stage1-c-newrepo-20261010/rpm.tsv)；工具/profile/products等关键资产：[assets.tsv](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-stage1-c-newrepo-20261010/assets.tsv)；全部文件元数据：[files.jsonl.gz](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-stage1-c-newrepo-20261010/files.jsonl.gz)。

RPM本次SHA已取得2/2；UNKNOWN 0；0个路径找到其他同SHA位置（包括同目录的其他名字，不等于可释放独立数据块）。未查到副本或超时的原包全部保留。

|仓库|HEAD|未发布候选/远端核对|stash|tracked改动|
|---|---|---|---|---|
|`/home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-stage1-c-newrepo-20261010/c0-package-aarch64`|`a6f4fe4b364800d93d97dea3dce19d568eb2ca98`|1（无远端/未证实已发布，须保留）|无|无|
|`/home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-stage1-c-newrepo-20261010/c1-export-repository`|`cb67996861d070d68fec2b4c623eed7d20ba2e23`|0（Gerrit可见refs排除后）|无|无|
|`/home/linhao/Toolchain/development/llvm-optimize/temp/arm-archive-stage1-c-newrepo-20261010/c0-package-armv7l`|`e9a6aa0671aee170424abed1cf6319c2d2977c5c`|1（无远端/未证实已发布，须保留）|无|无|

顶层关键文本/脚本41份，其中0份找到Git跟踪的同名同SHA副本；其余不推断已归档，一律纳入保留清单。逐文件路径/大小/SHA：[small-evidence.json](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-stage1-c-newrepo-20261010/small-evidence.json)。

当前引用检索：脚本1处；55–63号文档0处。
逐条位置与原文：[reference-index.md](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-stage1-c-newrepo-20261010/reference-index.md)。

**结论：必须保留。** 两个C0最小包各有无远端的本地提交，需先保全源码；accel/导出/buildconfig仍是重搭ARM环境的输入，本轮不移动或导出备份。
建议保留：[arm-archive-stage1-c-newrepo-20261010/retain-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-stage1-c-newrepo-20261010/retain-files.tsv.gz)逐路径列出，9.236 GiB (9,917,100,032 B)（与本节du相同盲区口径）。建议移除文件清单：[suggested-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-stage1-c-newrepo-20261010/suggested-files.tsv.gz)，共0条；预计释放文件块 **0.000 GiB (0 B)**。

## 8. C5：`arm-archive-standard-build-20261010`

ARM32标准-bc构建、bitcode/原生成员普查及首次转换停止现场；后续TLS/Thumb方案在C1目录完成复验。
出处：main/docs/40_arm_archive_conversion_stage1.md:1170–1242。

当前du：**4.738 GiB (5,087,920,128 B)**；本目录遍历无权限错误。

一级子目录（完整顶层文件和目录清单见inventory.json）：

|子目录|du GiB|类型/用途|
|---|---:|---|
|`__pycache__`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`armv7l-conversion`|0.063|实验输入、结果或辅助脚本；具体见文件清单|
|`armv7l-input`|4.333|实验输入、结果或辅助脚本；具体见文件清单|
|`armv7l-ir-census`|0.145|实验输入、结果或辅助脚本；具体见文件清单|
|`armv7l-native-census`|0.076|实验输入、结果或辅助脚本；具体见文件清单|
|`armv7l-tool-wrappers`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`c1-armv7l-build`|0.001|实验输入、结果或辅助脚本；具体见文件清单|
|`c1-armv7l-build-rerun`|0.074|实验输入、结果或辅助脚本；具体见文件清单|
|`c2-armv7l-ir`|0.001|实验输入、结果或辅助脚本；具体见文件清单|
|`c2-armv7l-native`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`c3-armv7l-convert`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`conversion-stop-diagnosis`|0.044|实验输入、结果或辅助脚本；具体见文件清单|

可读文件4,444；RPM路径0；发现Git仓库0。扫描错误：无

全部RPM与副本核对：[rpm.tsv](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-standard-build-20261010/rpm.tsv)；工具/profile/products等关键资产：[assets.tsv](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-standard-build-20261010/assets.tsv)；全部文件元数据：[files.jsonl.gz](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-standard-build-20261010/files.jsonl.gz)。

RPM本次SHA已取得0/0；UNKNOWN 0；0个路径找到其他同SHA位置（包括同目录的其他名字，不等于可释放独立数据块）。未查到副本或超时的原包全部保留。

可读范围未发现Git仓库；若本节有权限盲区，不据此宣称盲区也没有仓库。

顶层关键文本/脚本69份，其中0份找到Git跟踪的同名同SHA副本；其余不推断已归档，一律纳入保留清单。逐文件路径/大小/SHA：[small-evidence.json](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-standard-build-20261010/small-evidence.json)。

当前引用检索：脚本0处；55–63号文档0处。该两类均无。
逐条位置与原文：[reference-index.md](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-standard-build-20261010/reference-index.md)。

**结论：必须保留。** 唯一的ARM32原始输入、首次失败对象与标准构建日志仍用于ARM待办，保留。
建议保留：[arm-archive-standard-build-20261010/retain-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-standard-build-20261010/retain-files.tsv.gz)逐路径列出，4.738 GiB (5,087,920,128 B)（与本节du相同盲区口径）。建议移除文件清单：[suggested-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/arm-archive-standard-build-20261010/suggested-files.tsv.gz)，共0条；预计释放文件块 **0.000 GiB (0 B)**。

## 9. D：`bolt-v4-20261022-cache-release`

两轮ThinLTO cache-release完整构建；32号记录两轮candidate和RPM验证。两个GBS根已按38号后续清理，本目录主要是两套products及保全/报告。
出处：docs/bolt/32_cache_release.md；docs/bolt/38_temp_cleanup_inventory.md:121–143及第9节。

当前du：**26.140 GiB (28,067,635,200 B)**；本目录遍历无权限错误。

一级子目录（完整顶层文件和目录清单见inventory.json）：

|子目录|du GiB|类型/用途|
|---|---:|---|
|`baseline-evidence`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`baseline-export`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`baseline-preserve`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`baseline-products`|11.248|认证/保全产物|
|`baseline-resume1`|0.001|实验输入、结果或辅助脚本；具体见文件清单|
|`baseline-resume2`|0.010|实验输入、结果或辅助脚本；具体见文件清单|
|`baseline-resume2-evidence`|0.139|实验输入、结果或辅助脚本；具体见文件清单|
|`baseline-rpm-inventory`|0.005|实验输入、结果或辅助脚本；具体见文件清单|
|`baseline-segment1`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`baseline-segment2`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`baseline-space-recovery`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`baseline-tmp`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`config`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`five-parse`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`preserved-before-delete`|1.955|认证/保全产物|
|`resume2-preflight`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`revised-evidence`|0.139|实验输入、结果或辅助脚本；具体见文件清单|
|`revised-export`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`revised-export-files`|0.331|实验输入、结果或辅助脚本；具体见文件清单|
|`revised-preserve`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`revised-products`|11.248|认证/保全产物|
|`revised-rpm-inventory`|0.005|实验输入、结果或辅助脚本；具体见文件清单|
|`revised-run`|0.015|实验输入、结果或辅助脚本；具体见文件清单|
|`rpm-difference-analysis`|1.043|实验输入、结果或辅助脚本；具体见文件清单|
|`rpm-difference-job`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`rpm-validation`|0.001|实验输入、结果或辅助脚本；具体见文件清单|

可读文件57,343；RPM路径290；发现Git仓库0。扫描错误：无

全部RPM与副本核对：[rpm.tsv](../../tools/bolt/results/disk-review-group2-20261105/bolt-v4-20261022-cache-release/rpm.tsv)；工具/profile/products等关键资产：[assets.tsv](../../tools/bolt/results/disk-review-group2-20261105/bolt-v4-20261022-cache-release/assets.tsv)；全部文件元数据：[files.jsonl.gz](../../tools/bolt/results/disk-review-group2-20261105/bolt-v4-20261022-cache-release/files.jsonl.gz)。

RPM本次SHA已取得289/290；UNKNOWN 1；244个路径找到其他同SHA位置（包括同目录的其他名字，不等于可释放独立数据块）。未查到副本或超时的原包全部保留。

可读范围未发现Git仓库；若本节有权限盲区，不据此宣称盲区也没有仓库。

顶层关键文本/脚本45份，其中42份找到Git跟踪的同名同SHA副本；其余不推断已归档，一律纳入保留清单。逐文件路径/大小/SHA：[small-evidence.json](../../tools/bolt/results/disk-review-group2-20261105/bolt-v4-20261022-cache-release/small-evidence.json)。

当前引用检索：脚本17处；55–63号文档0处。
逐条位置与原文：[reference-index.md](../../tools/bolt/results/disk-review-group2-20261105/bolt-v4-20261022-cache-release/reference-index.md)。

**结论：瘦身。** 保留baseline-products、revised-products、preserved-before-delete及全部报告/配置；只建议移除从原RPM提取的rpm-difference-analysis/baseline与revised，保留同级差异JSON。
建议保留：[bolt-v4-20261022-cache-release/retain-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/bolt-v4-20261022-cache-release/retain-files.tsv.gz)逐路径列出，25.099 GiB (26,949,812,224 B)（与本节du相同盲区口径）。建议移除文件清单：[suggested-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/bolt-v4-20261022-cache-release/suggested-files.tsv.gz)，共540条；预计释放文件块 **1.041 GiB (1,117,822,976 B)**。

候选边界/原因（文件级重复项完整列表在recommendation.json）：

- `/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261022-cache-release/rpm-difference-analysis/baseline`：32号提取脚本逐文件从保留的原始RPM解出；保留同级JSON报告
- `/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261022-cache-release/rpm-difference-analysis/revised`：32号提取脚本逐文件从保留的原始RPM解出；保留同级JSON报告

## 10. E1：`crash-fix-probe-20261028`

42号objcopy only-keep-debug崩溃根因和GNU/eu-strip方案矩阵；函数级方案通过，源码行方案因没有带DWARF重链输入未测。
出处：docs/bolt/42_crash_localization_rootcause.md:3–32及第4–8节。

当前du：**11.055 GiB (11,869,986,816 B)**；本目录遍历无权限错误。

一级子目录（完整顶层文件和目录清单见inventory.json）：

|子目录|du GiB|类型/用途|
|---|---:|---|
|`bolt37`|0.614|实验输入、结果或辅助脚本；具体见文件清单|
|`bolt39`|0.521|实验输入、结果或辅助脚本；具体见文件清单|
|`ordinary`|6.551|实验输入、结果或辅助脚本；具体见文件清单|
|`scheme-a`|0.516|实验输入、结果或辅助脚本；具体见文件清单|
|`scratch.debug-probe`|2.617|实验输入、结果或辅助脚本；具体见文件清单|

可读文件102；RPM路径0；发现Git仓库0。扫描错误：无

全部RPM与副本核对：[rpm.tsv](../../tools/bolt/results/disk-review-group2-20261105/crash-fix-probe-20261028/rpm.tsv)；工具/profile/products等关键资产：[assets.tsv](../../tools/bolt/results/disk-review-group2-20261105/crash-fix-probe-20261028/assets.tsv)；全部文件元数据：[files.jsonl.gz](../../tools/bolt/results/disk-review-group2-20261105/crash-fix-probe-20261028/files.jsonl.gz)。

RPM本次SHA已取得0/0；UNKNOWN 0；0个路径找到其他同SHA位置（包括同目录的其他名字，不等于可释放独立数据块）。未查到副本或超时的原包全部保留。

可读范围未发现Git仓库；若本节有权限盲区，不据此宣称盲区也没有仓库。

顶层关键文本/脚本12份，其中12份找到Git跟踪的同名同SHA副本；其余不推断已归档，一律纳入保留清单。逐文件路径/大小/SHA：[small-evidence.json](../../tools/bolt/results/disk-review-group2-20261105/crash-fix-probe-20261028/small-evidence.json)。

当前引用检索：脚本7处；55–63号文档0处。
逐条位置与原文：[reference-index.md](../../tools/bolt/results/disk-review-group2-20261105/crash-fix-probe-20261028/reference-index.md)。

**结论：必须保留。** 保留objcopy缺陷的工具矩阵、两代BOLT重现副本、scheme-a及运行库。64号已删除输入构建根；没有证明全部矩阵可由仍存同SHA工具重建，不能按普通缓存处理。
建议保留：[crash-fix-probe-20261028/retain-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/crash-fix-probe-20261028/retain-files.tsv.gz)逐路径列出，11.055 GiB (11,869,986,816 B)（与本节du相同盲区口径）。建议移除文件清单：[suggested-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/crash-fix-probe-20261028/suggested-files.tsv.gz)，共0条；预计释放文件块 **0.000 GiB (0 B)**。

## 11. E2：`crash-probe-20261028`

41号普通/最终/符号表版clang崩溃栈与15TU实验；发现LLVM only-keep-debug SIGSEGV，之后由42/43号推进。
出处：docs/bolt/41_crash_localization_probe.md:3–16。

当前du：**2.359 GiB (2,533,433,344 B)**；本目录遍历无权限错误。

一级子目录（完整顶层文件和目录清单见inventory.json）：

|子目录|du GiB|类型/用途|
|---|---:|---|
|`__pycache__`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`empty-path`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`symbolizer-path`|0.000|实验输入、结果或辅助脚本；具体见文件清单|

可读文件43；RPM路径0；发现Git仓库0。扫描错误：无

全部RPM与副本核对：[rpm.tsv](../../tools/bolt/results/disk-review-group2-20261105/crash-probe-20261028/rpm.tsv)；工具/profile/products等关键资产：[assets.tsv](../../tools/bolt/results/disk-review-group2-20261105/crash-probe-20261028/assets.tsv)；全部文件元数据：[files.jsonl.gz](../../tools/bolt/results/disk-review-group2-20261105/crash-probe-20261028/files.jsonl.gz)。

RPM本次SHA已取得0/0；UNKNOWN 0；0个路径找到其他同SHA位置（包括同目录的其他名字，不等于可释放独立数据块）。未查到副本或超时的原包全部保留。

可读范围未发现Git仓库；若本节有权限盲区，不据此宣称盲区也没有仓库。

顶层关键文本/脚本4份，其中4份找到Git跟踪的同名同SHA副本；其余不推断已归档，一律纳入保留清单。逐文件路径/大小/SHA：[small-evidence.json](../../tools/bolt/results/disk-review-group2-20261105/crash-probe-20261028/small-evidence.json)。

当前引用检索：脚本4处；55–63号文档0处。
逐条位置与原文：[reference-index.md](../../tools/bolt/results/disk-review-group2-20261105/crash-probe-20261028/reference-index.md)。

**结论：瘦身。** 建议移除与ref-N.o全SHA相同的tu-N.o副本、与oldtext保全products同SHA的clang.final/clang.ordinary，以及与clang.symbols同SHA的same-clang。保留ref对象、独有符号表版、脚本及报告；若重跑旧脚本，须从列出的保留副本恢复原路径。缺陷修复仍挂账，不删除独有重现输入。
建议保留：[crash-probe-20261028/retain-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/crash-probe-20261028/retain-files.tsv.gz)逐路径列出，0.274 GiB (293,752,832 B)（与本节du相同盲区口径）。建议移除文件清单：[suggested-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/crash-probe-20261028/suggested-files.tsv.gz)，共18条；预计释放文件块 **2.086 GiB (2,239,680,512 B)**。

候选边界/原因（文件级重复项完整列表在recommendation.json）：

- `/home/linhao/Toolchain/development/llvm-optimize/temp/crash-probe-20261028/tu-11.o`：逐字节SHA相同，保留 /home/linhao/Toolchain/development/llvm-optimize/temp/crash-probe-20261028/ref-11.o
- `/home/linhao/Toolchain/development/llvm-optimize/temp/crash-probe-20261028/tu-0.o`：逐字节SHA相同，保留 /home/linhao/Toolchain/development/llvm-optimize/temp/crash-probe-20261028/ref-0.o
- `/home/linhao/Toolchain/development/llvm-optimize/temp/crash-probe-20261028/tu-5.o`：逐字节SHA相同，保留 /home/linhao/Toolchain/development/llvm-optimize/temp/crash-probe-20261028/ref-5.o
- `/home/linhao/Toolchain/development/llvm-optimize/temp/crash-probe-20261028/tu-6.o`：逐字节SHA相同，保留 /home/linhao/Toolchain/development/llvm-optimize/temp/crash-probe-20261028/ref-6.o
- `/home/linhao/Toolchain/development/llvm-optimize/temp/crash-probe-20261028/tu-4.o`：逐字节SHA相同，保留 /home/linhao/Toolchain/development/llvm-optimize/temp/crash-probe-20261028/ref-4.o
- `/home/linhao/Toolchain/development/llvm-optimize/temp/crash-probe-20261028/tu-7.o`：逐字节SHA相同，保留 /home/linhao/Toolchain/development/llvm-optimize/temp/crash-probe-20261028/ref-7.o
- `/home/linhao/Toolchain/development/llvm-optimize/temp/crash-probe-20261028/tu-13.o`：逐字节SHA相同，保留 /home/linhao/Toolchain/development/llvm-optimize/temp/crash-probe-20261028/ref-13.o
- `/home/linhao/Toolchain/development/llvm-optimize/temp/crash-probe-20261028/tu-3.o`：逐字节SHA相同，保留 /home/linhao/Toolchain/development/llvm-optimize/temp/crash-probe-20261028/ref-3.o
- 其余10条逐文件列于[recommendation.json](../../tools/bolt/results/disk-review-group2-20261105/crash-probe-20261028/recommendation.json)；不能扩展为删除整个父目录。

## 12. F：`archive-fix-v2-final-20261009`

docs35最终22 RPM、225开发归档和45 compiler-rt验证、独立安装和消费者；原始RPM与本地测试包仓库保留。
出处：main/docs/STATUS.md:21、258–267；main/docs/35_archive_fix_v2_final.md。

当前du：**10.339 GiB (11,101,380,608 B)**；本目录遍历无权限错误。

一级子目录（完整顶层文件和目录清单见inventory.json）：

|子目录|du GiB|类型/用途|
|---|---:|---|
|`continue-20261009`|10.017|实验输入、结果或辅助脚本；具体见文件清单|
|`github-publication`|0.000|实验输入、结果或辅助脚本；具体见文件清单|
|`rpms-docs35`|8.567|认证/保全产物|

可读文件56,713；RPM路径45；发现Git仓库2。扫描错误：无

全部RPM与副本核对：[rpm.tsv](../../tools/bolt/results/disk-review-group2-20261105/archive-fix-v2-final-20261009/rpm.tsv)；工具/profile/products等关键资产：[assets.tsv](../../tools/bolt/results/disk-review-group2-20261105/archive-fix-v2-final-20261009/assets.tsv)；全部文件元数据：[files.jsonl.gz](../../tools/bolt/results/disk-review-group2-20261105/archive-fix-v2-final-20261009/files.jsonl.gz)。

RPM本次SHA已取得45/45；UNKNOWN 0；44个路径找到其他同SHA位置（包括同目录的其他名字，不等于可释放独立数据块）。未查到副本或超时的原包全部保留。

|仓库|HEAD|未发布候选/远端核对|stash|tracked改动|
|---|---|---|---|---|
|`/home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-v2-final-20261009/continue-20261009/test-package-lld`|`1e556a14e6b88066f316c7f1ecbff3bbb7dd277a`|1（无远端/未证实已发布，须保留）|无|无|
|`/home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-v2-final-20261009/continue-20261009/test-package-bfd`|`4a78b9c666b92fa1ea4171c82d311ee84ea71a48`|1（无远端/未证实已发布，须保留）|无|无|

顶层关键文本/脚本28份，其中0份找到Git跟踪的同名同SHA副本；其余不推断已归档，一律纳入保留清单。逐文件路径/大小/SHA：[small-evidence.json](../../tools/bolt/results/disk-review-group2-20261105/archive-fix-v2-final-20261009/small-evidence.json)。

当前引用检索：脚本3处；55–63号文档0处。
逐条位置与原文：[reference-index.md](../../tools/bolt/results/disk-review-group2-20261105/archive-fix-v2-final-20261009/reference-index.md)。

**结论：必须保留。** 两份消费者探针各有本地未发布提交，原始docs35 RPM需保留；rpms-docs35与continue中的硬链接使一级du不可相加，不能把重复名字当作可释放的8GiB。
建议保留：[archive-fix-v2-final-20261009/retain-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/archive-fix-v2-final-20261009/retain-files.tsv.gz)逐路径列出，10.339 GiB (11,101,380,608 B)（与本节du相同盲区口径）。建议移除文件清单：[suggested-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/archive-fix-v2-final-20261009/suggested-files.tsv.gz)，共0条；预计释放文件块 **0.000 GiB (0 B)**。

## 13. G1：`llvm-optimize-intranet-20261020`

6e9d4f2 hybrid源码内网交接：shallow Git归档、5个分片、GBS导出缩写/标签/恢复验证。GitHub release已由原文记录发布；本次不重新下载或重建。
出处：main/docs/llvm_optimize_intranet_fetch.md:1–50。

当前du：**5.069 GiB (5,443,145,728 B)**；本目录遍历无权限错误。

一级子目录（完整顶层文件和目录清单见inventory.json）：

|子目录|du GiB|类型/用途|
|---|---:|---|
|`assets`|0.792|实验输入、结果或辅助脚本；具体见文件清单|
|`export-abbrev12`|0.322|实验输入、结果或辅助脚本；具体见文件清单|
|`export-first`|0.403|实验输入、结果或辅助脚本；具体见文件清单|
|`export-roundtrip-abbrev12`|0.322|实验输入、结果或辅助脚本；具体见文件清单|
|`export-tag-upstream`|0.322|实验输入、结果或辅助脚本；具体见文件清单|
|`llvm`|2.832|实验输入、结果或辅助脚本；具体见文件清单|
|`tmp`|0.000|实验输入、结果或辅助脚本；具体见文件清单|

可读文件169,225；RPM路径0；发现Git仓库1。扫描错误：无

全部RPM与副本核对：[rpm.tsv](../../tools/bolt/results/disk-review-group2-20261105/llvm-optimize-intranet-20261020/rpm.tsv)；工具/profile/products等关键资产：[assets.tsv](../../tools/bolt/results/disk-review-group2-20261105/llvm-optimize-intranet-20261020/assets.tsv)；全部文件元数据：[files.jsonl.gz](../../tools/bolt/results/disk-review-group2-20261105/llvm-optimize-intranet-20261020/files.jsonl.gz)。

RPM本次SHA已取得0/0；UNKNOWN 0；0个路径找到其他同SHA位置（包括同目录的其他名字，不等于可释放独立数据块）。未查到副本或超时的原包全部保留。

|仓库|HEAD|未发布候选/远端核对|stash|tracked改动|
|---|---|---|---|---|
|`/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-optimize-intranet-20261020/llvm`|`6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2`|0（Gerrit可见refs排除后）|无|无|

顶层关键文本/脚本106份，其中0份找到Git跟踪的同名同SHA副本；其余不推断已归档，一律纳入保留清单。逐文件路径/大小/SHA：[small-evidence.json](../../tools/bolt/results/disk-review-group2-20261105/llvm-optimize-intranet-20261020/small-evidence.json)。

当前引用检索：脚本2处；55–63号文档0处。
逐条位置与原文：[reference-index.md](../../tools/bolt/results/disk-review-group2-20261105/llvm-optimize-intranet-20261020/reference-index.md)。

**结论：瘦身。** 远端核对无未发布提交、tracked clean/stash无；assets完整归档和5分片的当前SHA均与保留SHA256SUMS一致（6/6）；保留assets的完整归档/5分片、manifest、全部本地脚本与导出对照报告，只建议移除可恢复的llvm检出和4个export目录。未来删除前须再核对worktree/alternates反向依赖和远端状态。
建议保留：[llvm-optimize-intranet-20261020/retain-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/llvm-optimize-intranet-20261020/retain-files.tsv.gz)逐路径列出，0.932 GiB (1,000,333,312 B)（与本节du相同盲区口径）。建议移除文件清单：[suggested-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/llvm-optimize-intranet-20261020/suggested-files.tsv.gz)，共169159条；预计释放文件块 **4.138 GiB (4,442,812,416 B)**。

候选边界/原因（文件级重复项完整列表在recommendation.json）：

- `/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-optimize-intranet-20261020/llvm`：交接源码HEAD/refs已由Gerrit可达性核对，tracked clean；完整assets和导出/恢复证据保留
- `/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-optimize-intranet-20261020/export-abbrev12`：交接源码HEAD/refs已由Gerrit可达性核对，tracked clean；完整assets和导出/恢复证据保留
- `/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-optimize-intranet-20261020/export-first`：交接源码HEAD/refs已由Gerrit可达性核对，tracked clean；完整assets和导出/恢复证据保留
- `/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-optimize-intranet-20261020/export-roundtrip-abbrev12`：交接源码HEAD/refs已由Gerrit可达性核对，tracked clean；完整assets和导出/恢复证据保留
- `/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-optimize-intranet-20261020/export-tag-upstream`：交接源码HEAD/refs已由Gerrit可达性核对，tracked clean；完整assets和导出/恢复证据保留

## 14. G2：`qb-meta-switch-20261028`

46号scm/meta/qb两评审的依赖、MLGO与1030仓库spec审计；最终上传359363/359364，构建配置拼接仍需后续QB确认。这里只分析旧证据，不查询QB或评审新状态。
出处：docs/bolt/46_qb_meta_toolchain_switch.md:540–670。

当前du：**4.489 GiB (4,820,525,056 B)**；本目录遍历无权限错误。

一级子目录（完整顶层文件和目录清单见inventory.json）：

|子目录|du GiB|类型/用途|
|---|---:|---|
|`mlgo`|3.164|实验输入、结果或辅助脚本；具体见文件清单|
|`second-specs`|1.319|实验输入、结果或辅助脚本；具体见文件清单|

可读文件1,919；RPM路径10；发现Git仓库0。扫描错误：无

全部RPM与副本核对：[rpm.tsv](../../tools/bolt/results/disk-review-group2-20261105/qb-meta-switch-20261028/rpm.tsv)；工具/profile/products等关键资产：[assets.tsv](../../tools/bolt/results/disk-review-group2-20261105/qb-meta-switch-20261028/assets.tsv)；全部文件元数据：[files.jsonl.gz](../../tools/bolt/results/disk-review-group2-20261105/qb-meta-switch-20261028/files.jsonl.gz)。

RPM本次SHA已取得10/10；UNKNOWN 0；5个路径找到其他同SHA位置（包括同目录的其他名字，不等于可释放独立数据块）。未查到副本或超时的原包全部保留。

可读范围未发现Git仓库；若本节有权限盲区，不据此宣称盲区也没有仓库。

顶层关键文本/脚本33份，其中16份找到Git跟踪的同名同SHA副本；其余不推断已归档，一律纳入保留清单。逐文件路径/大小/SHA：[small-evidence.json](../../tools/bolt/results/disk-review-group2-20261105/qb-meta-switch-20261028/small-evidence.json)。

当前引用检索：脚本17处；55–63号文档0处。
逐条位置与原文：[reference-index.md](../../tools/bolt/results/disk-review-group2-20261105/qb-meta-switch-20261028/reference-index.md)。

**结论：瘦身。** 保留10个原始RPM、所有日志/脚本/对象及second-specs；mlgo.py明确root只来自这5包解压，编译对象在root外，因此只建议移除两份mlgo/*/root。
建议保留：[qb-meta-switch-20261028/retain-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/qb-meta-switch-20261028/retain-files.tsv.gz)逐路径列出，1.962 GiB (2,106,159,104 B)（与本节du相同盲区口径）。建议移除文件清单：[suggested-files.tsv.gz](../../tools/bolt/results/disk-review-group2-20261105/qb-meta-switch-20261028/suggested-files.tsv.gz)，共840条；预计释放文件块 **2.528 GiB (2,714,365,952 B)**。

候选边界/原因（文件级重复项完整列表在recommendation.json）：

- `/home/linhao/Toolchain/development/llvm-optimize/temp/qb-meta-switch-20261028/mlgo/base/root`：mlgo.py逐包rpm2cpio解包5个保留RPM；试验对象在root外
- `/home/linhao/Toolchain/development/llvm-optimize/temp/qb-meta-switch-20261028/mlgo/toolchain/root`：mlgo.py逐包rpm2cpio解包5个保留RPM；试验对象在root外

## 15. A：Source1200原始fdata与合并关系

A根的可读文件中没有Source1200采集合并前的clang.PID.fdata；扫描到的.profraw/.profdata主要是LLVM源码测试夹具，不能误认成训练原件。历史docs16:31–40和docs20附录D:1395–1446定位原件于 **W/temp/bolt-measurement-20260918/run/profiles/**，不在A根内。
13份ARM+10份AArch64共23文件，本次逐一SHA全部吻合原profile-work/result.json，合计2,688,124,144 B；原合并文件171,232,190 B，SHA `d9b132f9430dfed32e080c65b4422bd76eba4a9c2101a2b18a7f66c94133b326`，和源码Source1200解压SHA `d9b132f9430dfed32e080c65b4422bd76eba4a9c2101a2b18a7f66c94133b326`一致。原压缩Source1200 SHA为 `52fd8522b8cceadebfb6bfc0a19f721f1072cff95c682b12b2c4dd5b0cc1e27f`。
使用同SHA的22.1.8 merge-fdata只读重合并（stdout只哈希/比较，不改原件），未运行训练或构建。首次重合并SHA不同，不能写成逐字相同。源代码merge-fdata.cpp:341–371按线程DenseMap和StringMap输出，未排序；第二次逐完整行多重集比较（含所有计数）为：
```json
{
  "rc": 0,
  "seconds": 31.915118535998772,
  "expected_lines": 746704,
  "actual_lines": 746704,
  "sha256": "0faa5f40f7d7cedd552a787479b39932cfaf8919ce7170807d5ef7c3667691ab",
  "missing_line_count": 0,
  "extra_sample": [],
  "same_lines_and_counts": true,
  "explanation": "merge-fdata legacy output iterates thread-id DenseMap then StringMap without sorting; physical line order is not canonical; all complete lines including counts compared as multiset."
}
```
因此证实是同23输入、同计数内容，字节排列不固定；原已保存merged-v2.fdata与Source1200则仍逐字节同SHA。23原件、旧merged及清单都在本次分析清单外，必须继续保留。详见[profile-correspondence.json](../../tools/bolt/results/disk-review-group2-20261105/profile-correspondence.json)、[merge-fdata-ordering.txt](../../tools/bolt/results/disk-review-group2-20261105/merge-fdata-ordering.txt)。

## 16. C：ARM静态库修复的最后状态与恢复输入

最后明确的ARM实测是2026-10-14 main/docs/49_x86_build_resume_result.md §12–14（L262–339）；main/docs/50_archive_followup_review.md和main/docs/STATUS.md:833–857保留待办。ARM32 210档/3690成员（3683 bitcode+7原生）及AArch64 212档/3706成员（3699+7）离线全量PASS，各档after SHA与docs40§12相同，沿用消费者/strip证据。ARM32根内小试在挂载前因Exec format error/无ARM binfmt停止，Source未运行；不能称为两ARM安装/打包已认证。
待办事实：ARM根内生产限制/64MiB负例及后续打包；两种架构原生shell/AS读回；14文件bash债务与LLVM23多行IR重新认证。是否继续、是否重新授权GBS初始化binfmt及mmap_min_addr，由用户决定，本轮不改变环境。
恢复需保留：C1的aarch64-input、两架构转换/原生比较证据；C5的armv7l-input及原始失败对象；C3的x86-input；C4的c0-package两仓库、c1-export/c1-export-repository、buildconfig-from-W.conf、repositories和accel-check；main已冻结ARM候选Source SHA `1bac8db608554b35d16482711bf0667f1fbee8d60c6fc52f0f448d240ffaa9e4`及对应Commands/测试/补丁。旧配方固定Base-Toolchain 20261001.092726与Unified-Toolchain 20260814.092727，并不是今晚的QB 20261030快照；恢复时需核对可取得性，不能偷偷替换。
历史时间（事实，不是本次重搭承诺）：docs40:L820–827的两个C0为344.287/418.849s；ARM32完整-bc 1998.954s（L1217–1221），AArch64初始化104.799s及-bc 2321.728s（L2188–2203）；docs49:L274/284最新离线转换分别1787.344/1571.769s。可参考为两次旧环境-bc合计约72分钟、两次离线转换约56分钟，另加初始化/下载/调查；**从零重搭总耗时UNKNOWN**，没有完整ARM安装打包的实测时长，不据此估算。

## 17. 汇总与需要用户决定的问题

没有任何目录被判为可以整个删除。以下为本轮实证支持的保守瘦身建议；“保留”不是永久禁止，只表示尚无足够证据批准整项或更多内容删除。

|目录|当前du GiB|结论|建议保留内容/大小 GiB|预计释放 GiB|用户需决定|
|---|---:|---|---|---:|---|
|`gbs-root-x86_64-debuginfo-j4-v2`|84.157†|必须保留|整根：普通clang、工具、27 RPM及证据；84.157†|0.000|先消除权限盲区并另做工具/产物保全？|
|`gbs-root-x86_64-archivefix-v2`|79.287†|必须保留|整根：工具、154 RPM及证据；79.287†|0.000|先消除权限盲区并另做原RPM保全？|
|`arm-archive-tls-thumb-20261010`|30.505|必须保留|整目录：ARM输入、认证转换及消费者；30.505|0.000|是否继续ARM根内认证？|
|`arm-source-root-probes-20261010`|18.378|瘦身|members/summary、探针及未核对归档；6.440|11.938|是否删除已核对的494份重复档？|
|`arm-archive-stage1-20261010`|11.923|瘦身|x86-input、全部报告及未核对归档；5.957|5.966|是否删除已核对的215份重复档？|
|`arm-archive-stage1-c-newrepo-20261010`|9.236|必须保留|两本地探针仓库、导出与accel输入；9.236|0.000|是否先备份两个本地探针提交？|
|`arm-archive-standard-build-20261010`|4.738|必须保留|ARM32输入、失败对象及日志；4.738|0.000|是否继续ARM根内认证？|
|`bolt-v4-20261022-cache-release`|26.140|瘦身|两套products、preserved和报告；25.099|1.041|是否仅删除两份解包副本？|
|`crash-fix-probe-20261028`|11.055|必须保留|全部复现矩阵、符号文件及运行库；11.055|0.000|缺陷定位关闭前是否另做最小复现保全？|
|`crash-probe-20261028`|2.359|瘦身|clang.symbols、ref对象和全部报告；0.274|2.086|是否按清单删重复二进制/对象？|
|`archive-fix-v2-final-20261009`|10.339|必须保留|45 RPM、两探针仓库及报告；10.339|0.000|是否先备份本地探针并另盘RPM？|
|`llvm-optimize-intranet-20261020`|5.069|瘦身|assets完整包/分片、manifest及报告；0.932|4.138|是否接受从assets恢复源码/导出？|
|`qb-meta-switch-20261028`|4.489|瘦身|10 RPM、对象/脚本/报告、second-specs；1.962|2.528|是否仅删除两个MLGO解包root？|

预计可释放文件块合计 **27.697 GiB**；本轮实际释放 **0 B**。†表示权限盲区，数值只代表可读部分，完整占用UNKNOWN。候选清单没有包含任何原RPM、profile原件、认证products或未发布源码仓库。

本次仅提交65号报告、STATUS和本次证据到GitHub bolt-v4；没有删除/移动待分析内容，没有sudo、构建、Gerrit/sandbox推送或QB操作。
