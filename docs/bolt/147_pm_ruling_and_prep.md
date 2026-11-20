# 147-prep · 361624 PM 裁决与上传准备

## 结论

**PM 判定 146 号剩余的 131 条全部归类通过。B1 与 PS5 对比的 509 条差异均已归类。** 按 PM 裁决，差异来自 PS4 及其父提交的改动或 RPM release 前缀，没有一条来自 C2。145 和 146 的逐条记录及当时的 STOP 原样保留。[145 号归类与 B2 报告](145_classification_and_b2.md) · [146 号 v2 报告](146_classification_v2.md)

**上传前准备 PASS。** 最终候选 `2fdceb61ca6e2309fb4885615dc1f430721d21e9` 已保存在本地分支 `361624-ps5`。2026-11-20 05:28:58 PST 只读查询确认 361624 仍为 `NEW`、最新 PS4。[准备结果](../../tools/bolt/results/task147-prep/result.json) · [Gerrit 查询原文](../../tools/bolt/results/task147-prep/gerrit-361624.stdout)

## PM 裁决

| 项目 | 条数 | 依据 |
|---|---:|---|
| `.relro_padding` | 128 | 这是 lld 的 RELRO 页对齐填充节，大小随布局变化。PM 将此节补入布局节白名单，并将这组差异归类通过。每个 ELF 的 `.gnu_debuglink` 文件名和 CRC 已逐一核对。 |
| `LLVMgold.so`、`ompdModule.so` | 2 | 模块库不受 PS4 的 EXE/SHARED 链接参数影响，两侧均无 build-id。唯一节差异是 `.gnu_debuglink` CRC，两项均与 C2 对应的 `.debug` 文件一致。 |
| BOLT 后的 `clang-22` | 1 | 剩余两个符号是同一个 `clang::driver::Driver::Driver` 的 C1/C2 别名。默认链接器的变化为 `"" → "lld"`，指令写入 `movl $0x646c6c` 和长度 3。PM 将其余差异归为代码变化后 BOLT 随之调整的热/冷块布局和跳转方向。其余 146,957 个函数键完全一致。 |

[146 号未归类原文及 CRC 证据](../../tools/bolt/results/task146/unclassified-v2.json) · [clang-22 两个符号的反汇编原文](../../tools/bolt/results/task146/clang-v2-raw-differences.txt)

## 提交 F 核对

| 事项 | 核对结果 |
|---|---|
| 生成方式 | 用 `git commit-tree` 保留 C2 的 tree、父提交、作者原始头和提交说明字节，在签名区末尾追加 `Signed-off-by: Hao Lin <hao.lin@samsung.com>`。提交者为 Hao Lin。 |
| Tree | `ef1ab363fa8e9be29eb930916e86c6e8f10f11af`，等于 C2。 |
| 父提交 | `f346dd75e87de324dc2abe61454ca1c49969d12d`，等于 PS4 的父提交。 |
| 作者及日期 | `Dongkyun Son <dongkyun.s@samsung.com> 1794637555 +0900`，原始头与 PS4、C2 逐字节一致。 |
| Change-Id | `Ie2c1d45cea6703a0caef72187397275a03e66468`，保留原值。 |
| 远端引用 | `ls-remote --heads` 返回 146 个 Gerrit 分支头，F 的 SHA 无命中。 |
| 禁用词检查 | 不区分大小写，检查说明新增的 1 行和 PS4→F diff 新增的 109 行，零命中。 |
| PS4→F | 21 个文件，增加 109 行、删除 54 行。完整 diff 与 PS4→C2 逐字节相同。 |
| 最新 patch set | PS4 `1ddecbe8729f832b5ef565092d039f68df647a43`，项目 `platform/upstream/llvm`，目标 `tizen_base`。 |

[F 完整提交说明原文](../../tools/bolt/results/task147-prep/F-commit-message.txt) · [PS4→F diffstat](../../tools/bolt/results/task147-prep/ps4-to-F.diffstat) · [PS4→F diff](../../tools/bolt/results/task147-prep/ps4-to-F.diff) · [F format-patch](../../tools/bolt/results/task147-prep/0001-361624-ps5.patch)

[远端分支头核对](../../tools/bolt/results/task147-prep/remote-branch-screen.json) · [ls-remote 原文](../../tools/bolt/results/task147-prep/gerrit-heads-1.stdout) · [禁用词核对](../../tools/bolt/results/task147-prep/outbound-text-verification.json)

本次准备无 STOP。LLVM 的 Gerrit 操作为只读查询，远端写入限于证据仓库 `bolt-v4`。F 的补丁随证据保存。

## 147-fix · F2 与 14 个 ELF 补证

**A PASS，F2 为 `636ef90aa1ff75ca8731b84b1526e6a557cffcd6`。B 已完成 14/14 个 ELF 的逐函数比较。** 12 个文件的所有函数键一致。另两份 Clang DSO 各有两个不同的函数键，均为同一个 `Driver::Driver` 构造函数的 C1/C2 别名，各有 686 条指令，归一化后的唯一差异为默认链接器的 `lld` 字面量及长度。两份评审原文按指定 SHA256 逐字节归档。[Codex 评审](../../tools/bolt/results/review-session/codex-review-c2-final.md) · [Claude Code 评审](../../tools/bolt/results/review-session/claude-code-review-c2-final.md) · [SHA256 收据](../../tools/bolt/results/task147-fix/review-receipts.json)

### A · 提交说明与身份

F2 替换本地 `361624-ps5` 的 F。用 `git commit-tree` 保留 tree `ef1ab363fa8e9be29eb930916e86c6e8f10f11af` 和父提交 `f346dd75e87de324dc2abe61454ca1c49969d12d`。作者头与 PS4 逐字节相同，提交者为 Hao Lin，Change-Id 仍为 `Ie2c1d45cea6703a0caef72187397275a03e66468`。

9 条 HQ 历史列表与 PS4 逐字节一致，历史 diff 为零字节。保留全部 HQ trailer，末行仍为 `Signed-off-by: Hao Lin <hao.lin@samsung.com>`。我方新增说明禁用词零命中。Gerrit 只读查询于 2026-11-20 06:40:24 PST 确认 361624 为 `NEW`，最新为 PS4 `1ddecbe8729f832b5ef565092d039f68df647a43`，146 个分支头均未命中 F2。F2 保留在本地，补丁随证据分支发布。

[F2 核对](../../tools/bolt/results/task147-fix/result-a.json) · [F2 完整说明](../../tools/bolt/results/task147-fix/F2-message.txt) · [F→F2 说明 diff](../../tools/bolt/results/task147-fix/F-to-F2-message.diff) · [PS4→F2 历史列表 diff](../../tools/bolt/results/task147-fix/PS4-to-F2-history.diff) · [F2 补丁](../../tools/bolt/results/task147-fix/0001-361624-ps5-F2.patch)

### B · 修订 .relro_padding 的证据表述

上文的 147-prep 裁决原文保留。两份最终评审指出，128 个 `.relro_padding` 条目中有 14 个还改变了 `.text`，146 号在节白名单检查处退出，尚未逐函数核对。补证后，`.relro_padding` 本身仍归为 lld 的页对齐填充。对这 14 个文件，节类型均为 NOBITS，并在 PT_GNU_RELRO 末尾的 4 KiB 页边界结束。它们的代码差异分为两组来源。[段布局与 build-id 证据](../../tools/bolt/results/task147-fix/relro14-segment-proof.json)

按 146 号方法核对所有 ELF 与相应 debug 文件的 CRC32 和 build-id。在离线副本上恢复符号表，逐节验证可执行字节保持一致。用带地址输出交叉验证地址省略版的反汇编，按符号范围逐函数比较并应用 R-ID2b 的局部字面量与最近符号注释归一化。14 个文件均覆盖全部带大小的可执行符号范围。函数键按符号名计数，别名单独列出。

| x86_64 ELF | 总数 | 一致 | 不同 | 差异来源 |
|---|---:|---:|---:|---|
| clang-installapi | 120 | 120 | 0 | PS4 链接布局 |
| libclang-cpp.so.22.1 | 87,985 | 87,983 | 2 | PS4 父提交默认 LLD，Driver C1/C2 |
| libclang.so.22.1.8 | 44,664 | 44,662 | 2 | PS4 父提交默认 LLD，Driver C1/C2 |
| libclang_rt.asan | 4,104 | 4,104 | 0 | PS4 链接布局 |
| libclang_rt.dyndd | 446 | 446 | 0 | PS4 链接布局 |
| libclang_rt.hwasan | 1,765 | 1,765 | 0 | PS4 链接布局 |
| libclang_rt.hwasan_aliases | 1,766 | 1,766 | 0 | PS4 链接布局 |
| libclang_rt.memprof | 3,353 | 3,353 | 0 | PS4 链接布局 |
| libclang_rt.nsan | 789 | 789 | 0 | PS4 链接布局 |
| libclang_rt.scudo_standalone | 232 | 232 | 0 | PS4 链接布局，另检查了 `.init`、`.plt` |
| libclang_rt.tsan | 4,349 | 4,349 | 0 | PS4 链接布局 |
| libclang_rt.ubsan_standalone | 507 | 507 | 0 | PS4 链接布局 |
| libomp.so | 2,274 | 2,274 | 0 | PS4 链接布局，另检查了 `.plt` |
| lldb-server | 4,285 | 4,285 | 0 | PS4 链接布局 |

12 个完全一致文件的改变节中，共有 38,167 条指令编码改变。逐字节核对确认这些变化均限于 PC 相对位移。38,165 条指令两侧指向同一节的同一偏移，另两条是 hwasan 与 hwasan_aliases 各一条，均指向同一数值地址 `0x0`。这证实这些可执行指令差异与 PS4 增加 build-id 后的链接布局一致。`clang-installapi` 和 `lldb-server` 的 `.rodata` 与 unwind 节里的变化另存原始字，分别呈现 `-4096`、`+4096` 的相对移动。[逐条类别和原始指令样例](../../tools/bolt/results/task147-fix/b-layout.json) · [两个 0x0 引用原文](../../tools/bolt/results/task147-fix/layout12-resolved-targets.json) · [节相对移动](../../tools/bolt/results/task147-fix/section-offset-proof.json)

两份 Clang DSO 的四个不同函数键均为以下两个符号。每份 DSO 内，两个符号在各自一侧指向同一个函数范围。两侧各为 686 条指令，归一化后的差异原文相同。

```text
_ZN5clang6driver6DriverC1EN4llvm9StringRefES3_RNS_17DiagnosticsEngineENSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEENS2_18IntrusiveRefCntPtrINS2_3vfs10FileSystemEEE
_ZN5clang6driver6DriverC2EN4llvm9StringRefES3_RNS_17DiagnosticsEngineENSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEENS2_18IntrusiveRefCntPtrINS2_3vfs10FileSystemEEE
```

```diff
- movq	$0x0, 0x4b8(%rbx)
- movb	$0x0, 0x4c0(%rbx)
+ movl	$0x646c6c, 0x4c0(%rbx)  # imm = 0x646C6C
+ movq	$0x3, 0x4b8(%rbx)
```

两个 DSO 的构造函数范围之外还有 13 和 9 个变化字节，逐条解码对应 10 和 8 条 PC 相对指令。虽然它们的字符串地址改变，两侧目标的 NUL 结尾字节逐一相同。[18 条字符串引用原文](../../tools/bolt/results/task147-fix/clang-dso-other-references.json)

该变化对应 `clang/lib/Driver/Driver.cpp` 第 183 行的 `PreferredLinker(CLANG_DEFAULT_LINKER)`，以及 PS4 父提交相对 PS5 的 diff 第 24 行 `-DCLANG_DEFAULT_LINKER=lld`。[libclang-cpp 原文与符号证据](../../tools/bolt/results/task147-fix/binaries/24/comparison.json) · [libclang 原文与符号证据](../../tools/bolt/results/task147-fix/binaries/25/comparison.json) · [14 个文件总表](../../tools/bolt/results/task147-fix/b-summary.json)

**F 的源码作用范围。** PS4→F 的 19 个 BOLT 文件全是 CMake 文件。在 B1 的 in-tree 配置中，链接模式仍为父提交的组件链接，X86 镜像和 flags 清空只在对应的 standalone 条件启用，B1 的 BOLT runtime 关闭。`llvm.spec` 中相对 PS4 的实质改动仅为删除运行时 Python 依赖和恢复 armv7l 目标列表，x86_64 的编译与链接参数相同。另一份 spec 属于独立包。这 14 个 ELF 均无 BOLT 节，在普通安装阶段已生成，随后流水线只为 `clang-22` 生成并安装重写产物。因此，在本次 x86_64 B1 路径下，F 的改动没有途径产生这 14 个 ELF 的指令差异。[源码和流水线证据](../../tools/bolt/results/task147-fix/source-b-scope.json) · [PS4→F 主 spec 原文](../../tools/bolt/results/task147-fix/PS4-to-F2-llvm.spec.diff) · [父提交→F 的 BOLT diff](../../tools/bolt/results/task147-fix/parent-to-F2-bolt.diff)

### 停止记录

A 与主逐函数比较均无最终 STOP。附加的指令编码检查第一次在 10 字节指令后误取显示分隔符，修正一次并重跑通过。另一次读取 Clang 节范围时，C2 符号副本尚未生成，待生成后用同一脚本完成检查。[首次解析 STOP 全部原文](../../tools/bolt/results/task147-fix/b-layout-preparation-STOP.json) · [修正 diff](../../tools/bolt/results/task147-fix/layout-parser-correction.diff) · [提前读取原文](../../tools/bolt/results/task147-fix/section-offset-first-read.txt) · [完整反汇编本地路径及 SHA](../../tools/bolt/results/task147-fix/local-large.json)
