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
