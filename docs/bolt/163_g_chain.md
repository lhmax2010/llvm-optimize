# 163 · 按实测资源接续 G 链

160 的 G4 构建和 PGO/Ninja 门禁已完成。旧交接在重命名 root 所有的构建根时失败。G5 使用原 G4 构建目录，通过当前 UID 的非特权命名空间调用原构建工具。
G4 的 clang-22、Ninja 输入和 23 个成品 RPM 已逐项核对。RPM 原位置作为 V2 来源保留。
重启后各步串行，CPU 上限两个核，Nice 19、I/O idle、swap0。用户临时授权本次跳过 I/O 启动等待。 运行中可用内存低于 6 GiB，或 I/O full avg60 持续 180 秒不低于 80%，只停本任务的子单元。
G5 取 58 号 D 的 BOLT 子阶段 cgroup 观测峰值 14,664,306,688 B。该区间包含 BOLT 工具准备、重链及 strip-debug，也覆盖了后续旧 profile 的重写尝试。它是较宽的历史阶段采样，163 会另记实际 G5 的内核峰值。
乘 1.15 后按页向上对齐，加 3 GiB 保留，立即启动线为 20,085,178,368 B。未达到时沿用原 19 GiB 准入和 60 分钟等待。

[功能复测](161_ps6_review_packet.md) · [全部输入](../../tools/bolt/results/task162/G4-input-inventory.json) · [G4 RPM](../../tools/bolt/results/task162/G4-rpm-check.json) · [编排差异](../../tools/bolt/results/task162/B-orchestration.diff)

| 步骤 | 状态 | 档位 / 并行 | MemoryMax B | MemAvailable B | /home 可用 B | 时段 PST | 等待 / 执行 s | cgroup 峰值 B | 原因 |
|---|---|---|---:|---:|---:|---|---:|---:|---|
| G5 | FAIL | dynamic / 4/4/1 | 16578727936 | 20873695232 | 169351675904 | 2026-11-26T01:08:06-08:00 → 2026-11-26T01:08:09-08:00 | 1200.002 / 2.395 | 11063296 | [Errno 2] No such file or directory: '/home/linhao/Toolchain/development/llvm-optimize/archive/task163/recipe.sha' |
| G6 | SKIPPED | — | — | 20740775936 | 169340944384 | — → 2026-11-26T01:08:19-08:00 | — / — | — | preceding stage did not pass |
| G7 | SKIPPED | — | — | 20666183680 | 169335484416 | — → 2026-11-26T01:08:25-08:00 | — / — | — | preceding stage did not pass |
| G8 | PENDING | — | — | — | — | — → — | — / — | — | — |

[G5 回执](../../tools/bolt/results/task163/G5/result.json)

[G6 回执](../../tools/bolt/results/task163/G6/result.json)

[G7 回执](../../tools/bolt/results/task163/G7/result.json)
