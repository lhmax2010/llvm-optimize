# 166 · 恢复 G 链

160 的 G4 构建和 PGO/Ninja 门禁已完成。旧交接在重命名 root 所有的构建根时失败。G5 使用原 G4 构建目录，通过当前 UID 的非特权命名空间调用原构建工具。
G4 的 clang-22、Ninja 输入和 23 个成品 RPM 的既有记录已核对。原 G4 RPM 保留供对照。V2 使用 QB 1240309 的 x86_64 成品。
上一轮脚本从自身目录定位配方收据，导入时退出。续跑传入原运行根并分开保存各次收据。首次实际 G5 完成工具构建和重链后，归档脚本拒绝了加载器对自己的绝对路径引用。续跑按 SHA256 复核并复用四个产物，只重做运行库归档和阶段检查。各阶段串行，Nice 19、I/O idle、swap0。G5 的 CPU 上限由入场负载决定。保留本任务子单元的内存、磁盘和 I/O 看门狗。
G5 取 58 号 D 的 BOLT 子阶段 cgroup 观测峰值 14,664,306,688 B。该区间包含 BOLT 工具准备、重链及 strip-debug，也覆盖了后续旧 profile 的重写尝试。它是较宽的历史阶段采样，166 另记实际 G5 的内核峰值。
乘 1.15 后按页向上对齐，加 3 GiB 保留，立即启动线为 20,085,178,368 B。G5 和 G6 每 10 分钟复测，等待至 2026-11-26 20:00 PST。

[功能复测](161_ps6_review_packet.md) · [全部输入](../../tools/bolt/results/task162/G4-input-inventory.json) · [G4 RPM](../../tools/bolt/results/task162/G4-rpm-check.json) · [编排差异](../../tools/bolt/results/task162/B-orchestration.diff)

| 步骤 | 状态 | 档位 / 并行 | MemoryMax B | MemAvailable B | /home 可用 B | 时段 PST | 等待 / 执行 s | cgroup 峰值 B | 原因 |
|---|---|---|---:|---:|---:|---|---:|---:|---|
| G5 | PASS | historical-peak / 6/6/1 | 21789810688 | 25011036160 | 150190710784 | 2026-11-26T03:58:12-08:00 → 2026-11-26T03:58:45-08:00 | 0.0 / 32.873 | 3860570112 | — |
| G6 | PASS | preferred / 1/—/— | 20685475840 | 24980443136 | 199175290880 | 2026-11-26T04:00:30-08:00 → 2026-11-26T04:06:40-08:00 | 0.0 / 370.086 | 16909234176 | — |
| G7 | PASS | dynamic / 1/—/— | 21397573632 | 25692540928 | 193619304448 | 2026-11-26T04:06:48-08:00 → 2026-11-26T04:09:24-08:00 | 0.0 / 155.387 | 8742191104 | — |
| G8 | PASS | dynamic / 1/—/— | 21264715776 | 25559683072 | 191514800128 | 2026-11-26T04:09:29-08:00 → 2026-11-26T04:10:19-08:00 | 0.0 / 50.021 | 141516800 | — |

[G5 回执](../../tools/bolt/results/task166/G5/result.json)

[G6 回执](../../tools/bolt/results/task166/G6/result.json)

[G7 回执](../../tools/bolt/results/task166/G7/result.json)

[G8 回执](../../tools/bolt/results/task166/G8/result.json)

157-B 状态为 **READY_AWAITING_PUSH**。已完成候选本地核对，由独立发布单元执行 157-B
[候选回执](../../tools/bolt/results/task166/paired-candidate.json)

## 157-B · 验证分支

**PASS**。新建 `sandbox/lhmax2025/llvm-pgo-bolt-20261125`，集成提交 `070c94c9263e8b003a899e6c31bcee34f6a64640`，测试提交 `4080f55abfc7c48097c9bd7fdbf9334e37c661af`。远端 ls-remote 与测试提交一致，QB 由用户触发。

[发布回执](../../tools/bolt/results/task166/candidate-upload/sandbox-result.json)
