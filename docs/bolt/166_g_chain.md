# 166 · 恢复 G 链

160 的 G4 构建和 PGO/Ninja 门禁已完成。旧交接在重命名 root 所有的构建根时失败。G5 使用原 G4 构建目录，通过当前 UID 的非特权命名空间调用原构建工具。
G4 的 clang-22、Ninja 输入和 23 个成品 RPM 的既有记录已核对。原 G4 RPM 保留供对照。V2 使用 QB 1240309 的 x86_64 成品。
上一轮脚本从自身目录定位配方收据，导入时退出。续跑传入原运行根并分开保存各次收据。各阶段串行，Nice 19、I/O idle、swap0。G5 的 CPU 上限由入场负载决定。保留本任务子单元的内存、磁盘和 I/O 看门狗。
G5 取 58 号 D 的 BOLT 子阶段 cgroup 观测峰值 14,664,306,688 B。该区间包含 BOLT 工具准备、重链及 strip-debug，也覆盖了后续旧 profile 的重写尝试。它是较宽的历史阶段采样，166 另记实际 G5 的内核峰值。
乘 1.15 后按页向上对齐，加 3 GiB 保留，立即启动线为 20,085,178,368 B。G5 和 G6 每 10 分钟复测，等待至 2026-11-26 20:00 PST。

[功能复测](161_ps6_review_packet.md) · [全部输入](../../tools/bolt/results/task162/G4-input-inventory.json) · [G4 RPM](../../tools/bolt/results/task162/G4-rpm-check.json) · [编排差异](../../tools/bolt/results/task162/B-orchestration.diff)

| 步骤 | 状态 | 档位 / 并行 | MemoryMax B | MemAvailable B | /home 可用 B | 时段 PST | 等待 / 执行 s | cgroup 峰值 B | 原因 |
|---|---|---|---:|---:|---:|---|---:|---:|---|
| G5 | FAIL | historical-peak / 4/4/1 | 18862358528 | 22083584000 | 156518502400 | 2026-11-26T03:38:25-08:00 → 2026-11-26T03:53:42-08:00 | 0.0 / 916.842 | 13785956352 | profile skill exited 1: {'status': 'STOP', 'project': 'T', 'stages': [{'name': 'bolt-tools-relink', 'status': 'STOP', 'attempt': '/home/linhao/Toolchain/development/llvm-optimize/archive/task160/run/G-profiles/bolt-tools-relink-1795693154435989441'}], 'started_at': '2026-11-26T11:38:44+00:00', 'admission': [{'at': '2026-11-26T11:38:44+00:00', 'memory': 22491115520, 'disk': {'/home': 156518469632, '/home/linhao/Toolchain/development/llvm-optimize/archive/task160/run/G-profiles': 156518469632}, 'admission_memory': 22083584000, 'stage': 'bolt-tools-relink', 'memory_max': 18862358528, 'floor': 16863952896, 'admitted': True, 'tier': 'historical-peak', 'jobs': 4, 'thinlto_jobs': 4, 'link_jobs': 1, 'actual_memory_max': 18862358528}], 'reason': 'command failed (1); see /home/linhao/Toolchain/development/llvm-optimize/archive/task160/run/G-profiles/bolt-tools-relink-1795693154435989441/build-1.txt', 'ended_at': '2026-11-26T11:53:40+00:00'} |
| G6 | SKIPPED | — | — | 26106208256 | 150201425920 | — → 2026-11-26T03:53:56-08:00 | — / — | — | preceding stage did not pass |
| G7 | SKIPPED | — | — | 26045743104 | 150201348096 | — → 2026-11-26T03:54:01-08:00 | — / — | — | preceding stage did not pass |
| G8 | PENDING | — | — | — | — | — → — | — / — | — | — |

[G5 回执](../../tools/bolt/results/task166/G5/result.json)

[G6 回执](../../tools/bolt/results/task166/G6/result.json)

[G7 回执](../../tools/bolt/results/task166/G7/result.json)
