# 63：QB 同快照 Toolchain 重建（2026-11-05）

**结论：完整构建成功，自动验证未全部通过。** 最终 clang、匹配的符号文件、三级 SHA、FLAGS 和 profile 计数与 QB 1216409 相同。23 包按既定规则为 3 PASS / 20 FAIL；90 TU 因旧输入路径已不存在，在第一个输入处停止，未完成任何一对编译比较。没有重试、修入口、放宽规则或手动续跑。

清理另见 [66号](66_disk_cleanup.md)，提交 `b40cd743c16bf4e1db9320cb0125de89f47de7e0`。本次原始证据在 `tools/bolt/results/qb-snapshot-rebuild-20261105/`；构建根及产物原样保留。

## 1. 唯一启动与结束记录

启动前检查已满足：/home 可用 559,488,331,776 B（521.064 GiB）≥98.8 GiB；新根不存在；没有其他 GBS/rpmbuild。[启动前记录](../../tools/bolt/results/qb-snapshot-rebuild-20261105/../disk-cleanup-20261105c/launch-precheck.json)

原样执行一次：
```sh
/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/night-launch-20261105/launch.sh 9e39fa8a61392652bb28b75fc26216675bcad1d5 full
```

前台最后的查看命令：
```sh
tail -f /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain/controller.stdout
```

最终结束行原文：
```text
NIGHT_PROJECT 已结束 2026-11-05T23:26:50.821583+08:00 status=failed reason=build-or-validation-failed-see-failure
VALIDATION 已结束 2026-11-05T23:26:10.499198+08:00 status=failed
ITEM2 已结束 2026-11-05T23:26:05.593395+08:00 status=differences reason=comparison-complete
```

GBS `exit_code=0`；构建服务从 2026-11-05T20:23:52.782356+08:00 到 2026-11-05T23:16:43.006423+08:00，耗时 10370.224068672 秒。完整入口（含准备和自动验证）耗时 11100.729 秒。controller 退出码为 1，原因是验证返回 1，不能写成构建失败或全部通过。[completed/evidence/build-result.json](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/build-result.json)、[completed/evidence/result.json](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/result.json)、[completed/controller.stderr](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/controller.stderr)

验证器既有逻辑在包比较失败后继续尝试90 TU；这是入口自动行为，本轮没有手动追加执行。

## 2. 源码、快照与条件

- 源码：`9e39fa8a61392652bb28b75fc26216675bcad1d5`；tree `cbc33271f8a9a7a5bd4de3c806bed6182c268e98`；最终只读审计工作区干净。
- 快照：`tizen-base-toolchain_20261030.061318`，与 QB 1216409 相同；只启用固定快照 packages/debug。
- build.conf SHA256：`8f201a0d58eb634e60a1f213f47fc09dfa953d9869cdc5724f326a76203587bf`。
- 外层 threads30；三个宏为 jobs8、_smp_mflags -j8、_costomized_smp_mflags -j20；实际 Ninja -j6。MemoryMax 24,482,992,128 B（MemTotal减8GiB），MemorySwapMax=0，CPUQuota=1200%，nice10，ionice 2/7。
- 同提交、同快照并不等于所有打包元数据相同：本地 GBS Release=1，QB Release=2.1；find-debuginfo 并发为本地-j8、QB-j12，debugsource唯一目录和VCS来源字符串不同（见第5节）。

[completed/plan.json](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/plan.json)、[completed/evidence/final-audit.json](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/final-audit.json)。

GBS 原始成功日志：`/home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain/gbs-driver/local/repos/tizen_base_toolchain_standard/x86_64/logs/success/llvm-22.1.8-1/log.txt`，18261438 B / 25693 行，SHA256 `6ea4da5e3053ae8264af2f32aa9288a98b9d88bfef0e4e41b7d62c039e7dfa6a`。行号均以此原始日志为准。压缩副本：[completed/gbs-original-0.log.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/gbs-original-0.log.gz)。

## 3. 验证结论、身份与 FLAGS

|项目|自动结论|说明|
|---|---|---|
|QB-flags-exact|PASS|去掉时间前缀后与QB逐字相同；WARNING 0条|
|QB-three-stage-sha-exact|PASS|三个SHA均相同，见下表|
|QB-profile-counts|PASS|N/M/S/U/Q/R全部相同|
|anchors|PASS|已有锚点检查通过|
|debuglink-and-debugfiles|PASS|文件名、CRC、identity及debugfiles.list检查通过|
|QB-23-packages|FAIL|3 PASS / 20 FAIL，不放宽门禁|
|QB-objects90|FAIL|第一个输入缺失；0/90完成，非目标文件内容不一致|

[completed/validation/result.json](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/validation/result.json)、[completed/validation/failure.txt](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/validation/failure.txt)。

|阶段|本轮与QB的共同SHA256|
|---|---|
|strip_all_sha256|`13a07cb7f84bd1ceda4d851c8bd71bddf7ef0c2d4864892eba64cbbb9a0350b8`|
|rpath_adjusted_sha256|`8c2429d870f421a29a9914458bc4d4ff2ce359a15e0bdd20f39bfb4580c40bdf`|
|after_sha256|`e08724d81231d8675c51d4908f4ff0e8d233ef3740c878da1c7eda42dd3532f5`|
|clang-22.debug|`9942e19c75ffef55f2846e6f1ea60651b4502de6e099c038a3d93bad4f5df690`|

最终clang为152,532,400字节；符号文件为35,321,968字节。符号文件再次只读计算SHA，等于QB期望值；debuglink文件名 `clang-22.debug`，CRC32=3891159848。RUNPATH=`$ORIGIN/../lib64`，DT_RPATH为空。[symbols-qb-check.json](../../tools/bolt/results/qb-snapshot-rebuild-20261105/symbols-qb-check.json)、[completed/validation/three-stage-sha.json](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/validation/three-stage-sha.json)、[completed/validation/debuglink.json](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/validation/debuglink.json)。

Profile：`N=23592 M=144032 S=0 U=1 Q=383 R=4.238545331242318e-05`；R×100约0.004238545331242318%，与QB全部相同。[completed/validation/pipeline.json](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/validation/pipeline.json)。

FLAGS原文（两条存在，WARNING为0条）：
```text
L676: [  183s] TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] CXXFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] LDFLAGS=[]
L678: [  183s] TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[] CXXFLAGS=[] LDFLAGS=[]
```

与QB的expected/actual原文：[completed/validation/flags.json](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/validation/flags.json)。主要门禁、三处real和缓存释放原文：[anchors-with-lines.txt](../../tools/bolt/results/qb-snapshot-rebuild-20261105/anchors-with-lines.txt)；完整自动锚点记录：[completed/validation/anchors.json](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/validation/anchors.json)。

两个RPM载荷manifest也再次核对，clang-22和clang-22.debug各自与QB完全同SHA，见 [packaged-identities.json](../../tools/bolt/results/qb-snapshot-rebuild-20261105/packaged-identities.json)。

## 4. 23包逐包比较

old=本地，new=QB。版本/release、VCS、payload mtime单列；比较器不会仅因这些RPM头元数据判FAIL，但实际文件路径、文件mode、DWARF内容变化仍被拒绝。下表“文件差异”包括内容或权限变化，不把同SHA但mode不同冒称字节内容改变。

|包/架构|结论|文件差异数|新增路径|移除路径|payload mtime变化数|
|---|---|---:|---:|---:|---:|
|clang / x86_64|FAIL|23|0|0|66|
|clang-debuginfo / x86_64|FAIL|23|0|0|28|
|clang-devel / x86_64|FAIL|1|0|0|237|
|clang-devel-debuginfo / x86_64|FAIL|1|0|0|4|
|compiler-rt / x86_64|FAIL|10|0|0|105|
|compiler-rt-debuginfo / x86_64|FAIL|10|0|0|17|
|libllvm / x86_64|FAIL|1|0|0|3|
|libllvm-debuginfo / x86_64|FAIL|1|0|0|4|
|libomp / x86_64|FAIL|3|0|0|3|
|libomp-debuginfo / x86_64|FAIL|3|0|0|6|
|libomp-devel / x86_64|PASS|0|0|0|1|
|lldb / x86_64|FAIL|5|0|0|8|
|lldb-debuginfo / x86_64|FAIL|5|0|0|16|
|lldb-devel / x86_64|FAIL|3|0|0|34|
|lldb-devel-debuginfo / x86_64|FAIL|3|0|0|7|
|llvm / src|FAIL|17|0|0|17|
|llvm / x86_64|FAIL|82|0|0|98|
|llvm-debuginfo / x86_64|FAIL|82|0|0|85|
|llvm-debugsource / x86_64|FAIL|0|12142|12142|0|
|llvm-devel / x86_64|FAIL|4|0|0|205|
|llvm-devel-debuginfo / x86_64|FAIL|4|0|0|11|
|llvm-static-devel / x86_64|PASS|0|0|0|225|
|python-clang / x86_64|PASS|0|0|0|0|

[completed/validation/qb-rpm-comparison.json.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/validation/qb-rpm-comparison.json.gz) 保留每包完整判定和metadata；[all-file-differences.tsv.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/all-file-differences.tsv.gz)逐项列出全部281个文件差异及24,284条新增/移除路径，不省略debugsource文件名。mtime每个路径及前后值也在原始比较JSON。

`llvm-static-devel` 的225个归档没有内容变化（不是靠放宽ar日期规则通过），只有225条payload mtime变化；`libomp-devel`、`python-clang`同样无内容变化。clang-22和其专属符号文件相同，并不意味着整个clang/clang-debuginfo包相同：两包内其他工具和符号仍有下述差异。

## 5. 差异的只读归因（不改比较结论）

### 5.1 DWARF与debuglink

比较器遇到首个非记录节差异即拒绝：218条报 `.debug_info`，46条报 `.debug_line`。它对带debuglink的二进制先检查配套.debug，因此这些错误不代表二进制本体包含该节。随后只读检查全部264个ELF：132个二进制的内容变化节是 `.gnu_debuglink`；132个配套符号文件的变化节均为 `.debug_info`、`.debug_line`、`.debug_str`；程序头均相同。各节大小、偏移和SHA见 [difference-details.json](../../tools/bolt/results/qb-snapshot-rebuild-20261105/difference-details.json)。这份诊断不替代原门禁，也不把DWARF节纳入允许清单。

132个.debug文件的 `.debug_str`，仅将 `usr/src/debug/llvm-22.1.8-1.x86_64` 替换为 `usr/src/debug/llvm-22.1.8-2.1.x86_64` 后，整节与QB逐字节相同（132/132）。平台处理命令原文：
```text
本地 L24621: [ 9423s] + /usr/lib/rpm/find-debuginfo.sh -j8 --build-id-seed 22.1.8-1 --unique-debug-src-base llvm-22.1.8-1.x86_64 -S debugsourcefiles.list /home/abuild/rpmbuild/BUILD/llvm-22.1.8
QB 1216409 L24664: [ 8649s] + /usr/lib/rpm/find-debuginfo.sh -j12 --build-id-seed 22.1.8-2.1 --unique-debug-src-base llvm-22.1.8-2.1.x86_64 -S debugsourcefiles.list /home/abuild/rpmbuild/BUILD/llvm-22.1.8
```

QB原文出处：[57号§3 find-debuginfo](57_qb_1216409_1216410.md#find-debuginfo-与-release-清理)。已证实路径字符串差异来自不同Release对应的debugsource目录。**推测** `.debug_info`/`.debug_line` 的相关变化来自debugedit对字符串和目录引用的重写；本轮没有逐条解码所有DWARF引用，不能声称所有DWARF差异已被语义等价证明。现有严格门禁保持FAIL。

### 5.2 debugsource路径

本地和QB各12,142个路径，以 `llvm-22.1.8-1.x86_64` / `llvm-22.1.8-2.1.x86_64` 为前缀。只读按此前缀一一对应后，mode/uid/gid/大小/SHA/链接目标全部相同，未对应或其他差异为0。但原始包的路径集合不同，因此原判定仍是FAIL。全部对应关系：[debugsource-prefix-pairs.json.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/debugsource-prefix-pairs.json.gz)。

### 5.3 源码RPM

17个载荷文件的mode为本地0664、QB0644；其中16个文件SHA相同。`llvm.spec`还存在VCS来源路径、Release 1/2.1，以及GBS `%patch -P N` 对QB `%patchN` 的导出语法差异。完整diff如下，源码仓库本身没有修改：
```diff
--- local/llvm.spec
+++ QB/llvm.spec
@@ -37,10 +37,10 @@
 %endif

 Name:      llvm
-VCS:       home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-tb20261026/source#9e39fa8a61392652bb28b75fc26216675bcad1d5
+VCS:       platform/upstream/llvm#9e39fa8a61392652bb28b75fc26216675bcad1d5
 Summary:   The LLVM Project is a collection of modular and reusable compiler and toolchain technologies
 Version:   22.1.8
-Release:   1
+Release:   2.1
 Group:     Development/Toolchain
 License:   NCSA
 Source0:   %{name}-%{version}.tar.gz
@@ -193,21 +193,21 @@
 %prep
 %setup -q
 # 0001-Add-support-for-Tizen-toolchain-vendor.patch
-%patch -P 0 -p1
+%patch0 -p1
 # 0002-Link-libclang_rt.asan.so-against-libatomic-when-nece.patch
-%patch -P 1 -p1
+%patch1 -p1
 # 0003-Fix-armv7l-build-when-compiler-is-clang.patch
-%patch -P 2 -p1
+%patch2 -p1
 # 0004-clang-add-support-for-LLVM-gold-plugin-in-case-of-ac.patch
-%patch -P 3 -p1
+%patch3 -p1
 # 0005-Merge-MLGO-AOT-compilation-support-and-optimization-.patch
-%patch -P 4 -p1
+%patch4 -p1
 # 0006-libcxxabi-declare-__gnu_unwind_frame-in-cxa_personal.patch
-%patch -P 5 -p1
+%patch5 -p1
 # 0007-libcxx-backport-EH-ABI-forced-unwind-handling.patch
-%patch -P 6 -p1
+%patch6 -p1
 # 0008-cmake-use-hybrid-LLVM-linkage-on-x86_64.patch
-%patch -P 7 -p1
+%patch7 -p1
 %if %{with mlgo}
 mkdir -p mlgo_verify_assets
 %ifarch armv7l
```

### 5.4 逐文件差异表

以下列出281个内容/权限差异；debugsource的24,284条路径新增/移除见第4节完整TSV和第5.2节对应表。“符号严格失败”指相关.debug不满足原规则，不能仅看到二进制CRC变化就判通过。

|包|文件|实际变化节/元数据|原因与原判定|
|---|---|---|---|
|clang / x86_64|`usr/bin/clang-apply-replacements`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/bin/clang-change-namespace`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/bin/clang-check`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/bin/clang-doc`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/bin/clang-extdef-mapping`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/bin/clang-format`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/bin/clang-include-cleaner`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/bin/clang-include-fixer`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/bin/clang-installapi`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/bin/clang-move`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/bin/clang-nvlink-wrapper`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/bin/clang-offload-bundler`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/bin/clang-query`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/bin/clang-refactor`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/bin/clang-reorder-fields`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/bin/clang-scan-deps`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/bin/clang-sycl-linker`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/bin/clang-tidy`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/bin/clangd`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/bin/find-all-symbols`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/bin/modularize`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/lib64/libclang-cpp.so.22.1`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang / x86_64|`usr/lib64/libclang.so.22.1.8`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-apply-replacements.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-change-namespace.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-check.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-doc.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-extdef-mapping.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-format.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-include-cleaner.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-include-fixer.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-installapi.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-move.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-nvlink-wrapper.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-offload-bundler.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-query.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-refactor.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-reorder-fields.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-scan-deps.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-sycl-linker.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-tidy.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/clangd.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/find-all-symbols.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/bin/modularize.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/lib64/libclang-cpp.so.22.1.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-debuginfo / x86_64|`usr/lib/debug/usr/lib64/libclang.so.22.1.8.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|clang-devel / x86_64|`usr/bin/clang-tblgen`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|clang-devel-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-tblgen.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|compiler-rt / x86_64|`usr/lib64/clang/22/lib/linux/libclang_rt.asan-x86_64.so`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|compiler-rt / x86_64|`usr/lib64/clang/22/lib/linux/libclang_rt.dyndd-x86_64.so`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|compiler-rt / x86_64|`usr/lib64/clang/22/lib/linux/libclang_rt.hwasan-x86_64.so`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|compiler-rt / x86_64|`usr/lib64/clang/22/lib/linux/libclang_rt.hwasan_aliases-x86_64.so`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|compiler-rt / x86_64|`usr/lib64/clang/22/lib/linux/libclang_rt.memprof-x86_64.so`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|compiler-rt / x86_64|`usr/lib64/clang/22/lib/linux/libclang_rt.nsan-x86_64.so`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|compiler-rt / x86_64|`usr/lib64/clang/22/lib/linux/libclang_rt.scudo_standalone-x86_64.so`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|compiler-rt / x86_64|`usr/lib64/clang/22/lib/linux/libclang_rt.tsan-x86_64.so`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|compiler-rt / x86_64|`usr/lib64/clang/22/lib/linux/libclang_rt.ubsan_minimal-x86_64.so`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|compiler-rt / x86_64|`usr/lib64/clang/22/lib/linux/libclang_rt.ubsan_standalone-x86_64.so`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|compiler-rt-debuginfo / x86_64|`usr/lib/debug/usr/lib64/clang/22/lib/linux/libclang_rt.asan-x86_64.so.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|compiler-rt-debuginfo / x86_64|`usr/lib/debug/usr/lib64/clang/22/lib/linux/libclang_rt.dyndd-x86_64.so.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|compiler-rt-debuginfo / x86_64|`usr/lib/debug/usr/lib64/clang/22/lib/linux/libclang_rt.hwasan-x86_64.so.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|compiler-rt-debuginfo / x86_64|`usr/lib/debug/usr/lib64/clang/22/lib/linux/libclang_rt.hwasan_aliases-x86_64.so.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|compiler-rt-debuginfo / x86_64|`usr/lib/debug/usr/lib64/clang/22/lib/linux/libclang_rt.memprof-x86_64.so.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|compiler-rt-debuginfo / x86_64|`usr/lib/debug/usr/lib64/clang/22/lib/linux/libclang_rt.nsan-x86_64.so.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|compiler-rt-debuginfo / x86_64|`usr/lib/debug/usr/lib64/clang/22/lib/linux/libclang_rt.scudo_standalone-x86_64.so.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|compiler-rt-debuginfo / x86_64|`usr/lib/debug/usr/lib64/clang/22/lib/linux/libclang_rt.tsan-x86_64.so.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|compiler-rt-debuginfo / x86_64|`usr/lib/debug/usr/lib64/clang/22/lib/linux/libclang_rt.ubsan_minimal-x86_64.so.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|compiler-rt-debuginfo / x86_64|`usr/lib/debug/usr/lib64/clang/22/lib/linux/libclang_rt.ubsan_standalone-x86_64.so.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|libllvm / x86_64|`usr/lib64/libLLVM.so.22.1`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|libllvm-debuginfo / x86_64|`usr/lib/debug/usr/lib64/libLLVM.so.22.1.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|libomp / x86_64|`usr/lib64/libarcher.so`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|libomp / x86_64|`usr/lib64/libomp.so`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|libomp / x86_64|`usr/lib64/libompd.so`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|libomp-debuginfo / x86_64|`usr/lib/debug/usr/lib64/libarcher.so.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|libomp-debuginfo / x86_64|`usr/lib/debug/usr/lib64/libomp.so.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|libomp-debuginfo / x86_64|`usr/lib/debug/usr/lib64/libompd.so.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|lldb / x86_64|`home/owner/share/tmp/sdk_tools/lldb/bin/lldb`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|lldb / x86_64|`home/owner/share/tmp/sdk_tools/lldb/bin/lldb-argdumper`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|lldb / x86_64|`home/owner/share/tmp/sdk_tools/lldb/bin/lldb-server`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|lldb / x86_64|`home/owner/share/tmp/sdk_tools/lldb/lib64/liblldb.so.22.1.8`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|lldb / x86_64|`usr/bin/lldb-mcp`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|lldb-debuginfo / x86_64|`usr/lib/debug/home/owner/share/tmp/sdk_tools/lldb/bin/lldb-argdumper.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|lldb-debuginfo / x86_64|`usr/lib/debug/home/owner/share/tmp/sdk_tools/lldb/bin/lldb-server.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|lldb-debuginfo / x86_64|`usr/lib/debug/home/owner/share/tmp/sdk_tools/lldb/bin/lldb.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|lldb-debuginfo / x86_64|`usr/lib/debug/home/owner/share/tmp/sdk_tools/lldb/lib64/liblldb.so.22.1.8.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|lldb-debuginfo / x86_64|`usr/lib/debug/usr/bin/lldb-mcp.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|lldb-devel / x86_64|`usr/bin/lldb-tblgen`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|lldb-devel / x86_64|`usr/lib64/liblldb.so.22.1.8`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|lldb-devel / x86_64|`usr/lib64/liblldbIntelFeatures.so.22.1`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|lldb-devel-debuginfo / x86_64|`usr/lib/debug/usr/bin/lldb-tblgen.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|lldb-devel-debuginfo / x86_64|`usr/lib/debug/usr/lib64/liblldb.so.22.1.8.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|lldb-devel-debuginfo / x86_64|`usr/lib/debug/usr/lib64/liblldbIntelFeatures.so.22.1.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm / src|`0001-Add-support-for-Tizen-toolchain-vendor.patch`|mode 0664→0644，字节SHA相同|源包权限（及spec导出）差异；FAIL|
|llvm / src|`0002-Link-libclang_rt.asan.so-against-libatomic-when-nece.patch`|mode 0664→0644，字节SHA相同|源包权限（及spec导出）差异；FAIL|
|llvm / src|`0003-Fix-armv7l-build-when-compiler-is-clang.patch`|mode 0664→0644，字节SHA相同|源包权限（及spec导出）差异；FAIL|
|llvm / src|`0004-clang-add-support-for-LLVM-gold-plugin-in-case-of-ac.patch`|mode 0664→0644，字节SHA相同|源包权限（及spec导出）差异；FAIL|
|llvm / src|`0005-Merge-MLGO-AOT-compilation-support-and-optimization-.patch`|mode 0664→0644，字节SHA相同|源包权限（及spec导出）差异；FAIL|
|llvm / src|`0006-libcxxabi-declare-__gnu_unwind_frame-in-cxa_personal.patch`|mode 0664→0644，字节SHA相同|源包权限（及spec导出）差异；FAIL|
|llvm / src|`0007-libcxx-backport-EH-ABI-forced-unwind-handling.patch`|mode 0664→0644，字节SHA相同|源包权限（及spec导出）差异；FAIL|
|llvm / src|`0008-cmake-use-hybrid-LLVM-linkage-on-x86_64.patch`|mode 0664→0644，字节SHA相同|源包权限（及spec导出）差异；FAIL|
|llvm / src|`clang-bolt-helper.py`|mode 0664→0644，字节SHA相同|源包权限（及spec导出）差异；FAIL|
|llvm / src|`clang-bolt-v2.fdata.xz`|mode 0664→0644，字节SHA相同|源包权限（及spec导出）差异；FAIL|
|llvm / src|`llvm-22.1.8.tar.gz`|mode 0664→0644，字节SHA相同|源包权限（及spec导出）差异；FAIL|
|llvm / src|`llvm-static-archives-native.py`|mode 0664→0644，字节SHA相同|源包权限（及spec导出）差异；FAIL|
|llvm / src|`llvm.manifest`|mode 0664→0644，字节SHA相同|源包权限（及spec导出）差异；FAIL|
|llvm / src|`llvm.spec`|mode 0664→0644; spec文本|源包权限（及spec导出）差异；FAIL|
|llvm / src|`mlgo_aarch_model.tar.gz`|mode 0664→0644，字节SHA相同|源包权限（及spec导出）差异；FAIL|
|llvm / src|`mlgo_arm_model.tar.gz`|mode 0664→0644，字节SHA相同|源包权限（及spec导出）差异；FAIL|
|llvm / src|`mlgo_x86_model.tar.gz`|mode 0664→0644，字节SHA相同|源包权限（及spec导出）差异；FAIL|
|llvm / x86_64|`usr/bin/bugpoint`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/clang-linker-wrapper`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/clang-repl`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/diagtool`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/dsymutil`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llc`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/lld`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/lldb-dap`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/lldb-instr`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/lli`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-ar`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-as`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-bcanalyzer`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-c-test`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-cas`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-cat`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-cfi-verify`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-cgdata`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-config`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-cov`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-ctxprof-util`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-cvtres`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-cxxdump`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-cxxfilt`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-cxxmap`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-debuginfo-analyzer`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-debuginfod`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-debuginfod-find`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-diff`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-dis`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-dwarfdump`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-dwarfutil`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-dwp`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-exegesis`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-extract`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-gsymutil`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-ifs`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-ir2vec`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-jitlink`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-libtool-darwin`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-link`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-lipo`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-lto`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-lto2`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-mc`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-mca`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-ml`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-modextract`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-mt`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-nm`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-objcopy`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-objdump`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-offload-binary`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-offload-wrapper`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-opt-report`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-pdbutil`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-profdata`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-profgen`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-rc`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-readobj`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-readtapi`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-reduce`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-remarkutil`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-rtdyld`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-sim`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-size`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-split`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-stress`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-strings`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-symbolizer`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-tblgen`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-tli-checker`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-undname`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/llvm-xray`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/offload-arch`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/opt`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/pp-trace`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/reduce-chunk-list`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/sancov`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/sanstats`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/verify-uselistorder`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm / x86_64|`usr/bin/yaml2macho-core`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/bugpoint.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-linker-wrapper.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/clang-repl.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/diagtool.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/dsymutil.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llc.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/lld.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/lldb-dap.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/lldb-instr.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/lli.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-ar.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-as.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-bcanalyzer.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-c-test.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-cas.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-cat.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-cfi-verify.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-cgdata.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-config.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-cov.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-ctxprof-util.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-cvtres.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-cxxdump.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-cxxfilt.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-cxxmap.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-debuginfo-analyzer.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-debuginfod-find.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-debuginfod.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-diff.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-dis.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-dwarfdump.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-dwarfutil.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-dwp.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-exegesis.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-extract.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-gsymutil.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-ifs.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-ir2vec.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-jitlink.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-libtool-darwin.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-link.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-lipo.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-lto.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-lto2.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-mc.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-mca.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-ml.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-modextract.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-mt.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-nm.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-objcopy.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-objdump.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-offload-binary.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-offload-wrapper.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-opt-report.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-pdbutil.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-profdata.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-profgen.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-rc.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-readobj.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-readtapi.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-reduce.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-remarkutil.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-rtdyld.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-sim.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-size.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-split.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-stress.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-strings.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-symbolizer.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-tblgen.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-tli-checker.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-undname.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/llvm-xray.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/offload-arch.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/opt.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/pp-trace.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/reduce-chunk-list.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/sancov.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/sanstats.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/verify-uselistorder.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-debuginfo / x86_64|`usr/lib/debug/usr/bin/yaml2macho-core.debug`|.debug_info, .debug_line, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-devel / x86_64|`usr/lib64/LLVMgold.so`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm-devel / x86_64|`usr/lib64/libLTO.so.22.1`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm-devel / x86_64|`usr/lib64/libRemarks.so.22.1`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm-devel / x86_64|`usr/share/gdb/python/ompd/ompdModule.so`|.gnu_debuglink|配套.debug的非记录节变化；FAIL|
|llvm-devel-debuginfo / x86_64|`usr/lib/debug/usr/lib64/LLVMgold.so.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-devel-debuginfo / x86_64|`usr/lib/debug/usr/lib64/libLTO.so.22.1.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-devel-debuginfo / x86_64|`usr/lib/debug/usr/lib64/libRemarks.so.22.1.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|
|llvm-devel-debuginfo / x86_64|`usr/lib/debug/usr/share/gdb/python/ompd/ompdModule.so.debug`|.debug_line, .debug_info, .debug_str|DWARF非记录节变化，debug_str已证实为Release路径差异；FAIL|

## 6. 90 TU：未完成，未重跑

失败原文：
```text
FileNotFoundError: [Errno 2] No such file or directory: '/home/linhao/Toolchain/development/llvm-optimize/temp/hybrid-local-20261023/tu-inputs/000.ii'
```

验证器读取 `W/docs/53_hybrid_local_validation_evidence/tu-inputs.json` 中旧的copy路径，在第一个输入SHA检查处失败，尚未调用参考编译器。本轮没有完成任何一对目标文件比较，不能写90/90，也不能把clang文件SHA相同替代这项实测。该父目录已在[64号第27项](64_disk_cleanup.md)按当时用户批准清单删除；本轮未再次删除它。没有恢复输入、改入口、重跑或自行选用另一份资产。[completed/validation/failure.txt](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/validation/failure.txt)。

## 7. 资源和时间线

以下原样保存入口生成的resource-table.md。阶段界限来自GBS原始日志 `[NNNNs]`，不是轮询观察时刻。cgroup分阶段值是采样memory.current最大值（含文件缓存），并非各阶段独立memory.peak；VmHWM仅观察llvm-bolt，全进程最大值UNKNOWN。du限时失败的单次样本保留原文，不插值。

|Phase|Seconds|Cgroup sampled bytes (includes cache)|llvm-bolt VmHWM bytes|Root du sampled bytes|Filesystem min available bytes|
|---|---|---|---|---|---|
|ordinary-build|4518.0|18465832960|UNKNOWN|45166219264|485629710336|
|ordinary-install|374.0|12894543872|UNKNOWN|58750799872|472185999360|
|BOLT|1934.0|15773831168|9929744384|67730743296|463856259072|
|cache-release|122.0|5733998592|UNKNOWN|63076773888|464171540480|
|archive-conversion|2285.0|15946149888|UNKNOWN|52332785664|477582393344|
|platform-post|434.0|8691818496|UNKNOWN|44324790272|485440192512|
|packaging|494.0|12610822144|UNKNOWN|46525587456|484759506944|

整轮构建cgroup memory.peak=18,533,765,120 B（17.261 GiB，含文件缓存），oom/oom_kill均0，swap峰值0。根du已成功采样的最大值67,730,743,296 B（63.079 GiB），不是保证捕获所有瞬时尖峰的理论上限；构建资源采样的/home最低可用463,856,259,072 B（约432.000 GiB）。验证阶段controller还保留单独观测：23:22 memory.peak=6,408,904,704 B；这不是构建服务峰值。[monitor.jsonl](../../tools/bolt/results/qb-snapshot-rebuild-20261105/monitor.jsonl)。

GBS锚点：

|阶段|起点秒|原始行号|
|---|---:|---:|
|ordinary-build|182|L347|
|ordinary-install|4700|L11345|
|BOLT|5074|L16924|
|BOLT-end|7008|L24145|
|cache-release|7008|L24146|
|cache-release-end|7130|L24147|
|archive-conversion|7131|L24167|
|archive-conversion-end|9416|L24618|
|platform-post|9423|L24621|
|packaging|9857|L25212|

[completed/evidence/resource-table.json](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resource-table.json)、[completed/evidence/resources.jsonl.gz](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/resources.jsonl.gz)、[completed/evidence/du-root.jsonl](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/du-root.jsonl)、[completed/evidence/bolt-process.jsonl](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/bolt-process.jsonl)。采样文件是否压缩以[provenance.json](../../tools/bolt/results/qb-snapshot-rebuild-20261105/provenance.json)为准。

内存采样5,096条；du采样173条，其中116条成功、50条超时、7条无rc（保留为UNKNOWN）。根占用最大有效样本出现在2026-11-05T22:09:52.692404+08:00，/home最低可用出现在2026-11-05T22:10:09.061579+08:00。见 [resource-sample-summary.json](../../tools/bolt/results/qb-snapshot-rebuild-20261105/resource-sample-summary.json)。

## 8. 现场与交付范围

入口结束审计：构建/准备服务inactive，挂载列表为空，remaining_build_processes=[]。只使用入口已有的正常收尾；没有懒卸载、杀外部进程、手动sudo或重试。controller保留failed状态供排查。构建根、RPM、比较payload和失败记录均保留。LLVM源码、spec、helper、启动入口均未修改。[completed/evidence/final-audit.json](../../tools/bolt/results/qb-snapshot-rebuild-20261105/completed/evidence/final-audit.json)。

采集时/home：484415164416 B（451.147 GiB），时间 2026-11-05T23:53:46.163517+08:00。[df-final.txt](../../tools/bolt/results/qb-snapshot-rebuild-20261105/df-final.txt)。

完整原始成功日志、自动验证原文、资源采样、每包manifest和逐文件差异已入证据目录；大文本gzip压缩，来源/原大小/原SHA/压缩SHA记录于provenance.json。诊断仅解释失败，没有改变任何验证判定。

提交前/home可用484,308,074,496 B（451.047 GiB），时间2026-11-06T00:06:06.577522+08:00；[df原文](../../tools/bolt/results/qb-snapshot-rebuild-20261105/df-before-delivery.txt)。

**最终结论：构建成功，整体验证有问题（23包20 FAIL；90 TU缺输入未完成），本轮停止且保留现场。**
