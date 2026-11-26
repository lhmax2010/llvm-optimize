# 162 · 从 G5 原地接续

160 的 G4 构建和 PGO/Ninja 门禁已完成。旧交接在重命名 root 所有的构建根时失败。G5 使用原 G4 构建目录，通过当前 UID 的非特权命名空间调用原构建工具。
G4 的 clang-22、Ninja 输入和 23 个成品 RPM 已逐项核对。RPM 原位置作为 V2 来源保留。

[功能复测](161_ps6_review_packet.md) · [全部输入](../../tools/bolt/results/task162/G4-input-inventory.json) · [G4 RPM](../../tools/bolt/results/task162/G4-rpm-check.json) · [编排差异](../../tools/bolt/results/task162/B-orchestration.diff)

| 步骤 | 状态 | 档位 | MemoryMax B | MemAvailable B | /home 可用 B | 用时 s | 原因 |
|---|---|---|---:|---:|---:|---:|---|
| G5 | SKIPPED | — | — | 17954267136 | 222012657664 | — | memory below floor |
| G6 | SKIPPED | — | — | 17970012160 | 222008430592 | — | preceding stage did not pass |
| G7 | SKIPPED | — | — | 17879654400 | 222003163136 | — | preceding stage did not pass |
| G8 | PENDING | — | — | — | — | — | — |

[G5 回执](../../tools/bolt/results/task162/G5/result.json)

[G6 回执](../../tools/bolt/results/task162/G6/result.json)

[G7 回执](../../tools/bolt/results/task162/G7/result.json)
