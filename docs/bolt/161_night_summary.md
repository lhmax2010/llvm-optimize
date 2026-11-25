# 161 · 夜间接续汇总

## 需要用户处理的事项

- PS6 的 154-B 结果为 **PARTIAL**。 [评审材料](161_ps6_review_packet.md)
- PGO+BOLT 候选状态为 等待 G 链。—
- 大型库已删除 11/11，3 个自测库保留。
- [154-B 的 sudo 清理脚本](../../tools/bolt/results/task154/sudo-clean.sh) 等待用户审核。
- 大型库归档首轮 STOP，原因是 SHA256 检查调用错误。续做已通过。 [首轮原始提交](https://github.com/lhmax2010/llvm-optimize/blob/2720eb0b/tools/bolt/results/task160/backup-supplement/large-terminal.json)

更新于 2026-11-25T11:37:59.125899-08:00。

## 单元与顺序

154-B → PS6 评审材料发布 → 160 G 链 → 符合条件时的 157-B。

| 单元 | 状态 | 重启时间 |
|---|---|---|
| `llvm-opt-task154-after-153.service` | inactive/dead | Wed 2026-11-25 07:36:45 PST |
| `llvm-opt-task160-g-chain.service` | active/running | Wed 2026-11-25 07:36:45 PST |
| `llvm-opt-task161-night.service` | active/running | — |
| `llvm-opt-task161-backup-scan.service` | inactive/dead | — |
| `llvm-opt-task161-backup-duplicates.service` | inactive/dead | — |
| `llvm-opt-task160-backup-large.service` | inactive/dead | — |
| `llvm-opt-task160-backup-evidence.service` | inactive/dead | — |
| `llvm-opt-task154-full-build-1.service` | inactive/dead | — |
| `llvm-opt-task154-full-build-2.service` | inactive/dead | — |

## 步骤与资源

| 步骤 | 结论 | 用时 s | 等待 s | 原因 |
|---|---|---:|---:|---|
| 154-B | PARTIAL | 11035.8 | — | waiting for 139-D memory floor or build disk allowance |
| G4 | WAITING | — | — | active: llvm-opt-task154-after-153.service |
| G5 | WAITING | — | — | — |
| G6 | WAITING | — | — | — |
| G7 | WAITING | — | — | — |
| G8 | WAITING | — | — | — |
| 157-B | WAITING | — | — | — |

154-B 准入时 /home 可用 318,757,634,048 B，MemAvailable 22,569,095,168 B。

154-B 仍采用原磁盘准入线 302,154,457,695 B，包含 30 GB 预留。
160 补充累计净释放 46,013,472,768 B，其中本次接续 46,010,806,272 B。清理结束时 /home 可用 318,757,769,216 B。

当前 /home 可用 310,068,912,128 B，MemAvailable 27,545,559,040 B。

| 采样时间 | /home 可用 B | /home 已用 B | MemAvailable B |
|---|---:|---:|---:|
| 2026-11-25T10:23:25.515784-08:00 | 250,425,229,312 | 1,617,383,108,608 | 26,958,491,648 |
| 2026-11-25T10:33:26.110338-08:00 | 270,238,650,368 | 1,597,569,687,552 | 27,584,143,360 |
| 2026-11-25T10:43:26.530112-08:00 | 267,048,554,496 | 1,600,759,783,424 | 27,065,364,480 |
| 2026-11-25T10:53:26.956209-08:00 | 264,027,705,344 | 1,603,780,632,576 | 27,138,060,288 |
| 2026-11-25T11:03:27.460222-08:00 | 262,865,657,856 | 1,604,942,680,064 | 27,697,020,928 |
| 2026-11-25T11:13:28.031951-08:00 | 270,328,713,216 | 1,597,479,624,704 | 25,749,872,640 |
| 2026-11-25T11:23:28.466634-08:00 | 269,397,483,520 | 1,598,410,854,400 | 25,646,190,592 |
| 2026-11-25T11:33:28.905613-08:00 | 268,167,094,272 | 1,599,641,243,648 | 25,623,969,792 |

G4 已记录 0 条 ARCHIVE_MEMBER_RETRY。 [160 G 链报告](160_g_chain.md) · [采样原文](../../tools/bolt/results/task161/resources.jsonl)
