# 161 · 夜间接续汇总

## 需要用户处理的事项

- PS6 等待 154-B 结束并发布验证证据。
- PGO+BOLT 候选状态为 等待 G 链。—
- 大型库已删除 11/11，3 个自测库保留。
- 大型库归档首轮 STOP，原因是 SHA256 检查调用错误。续做已通过。 [首轮原始提交](https://github.com/lhmax2010/llvm-optimize/blob/2720eb0b/tools/bolt/results/task160/backup-supplement/large-terminal.json)

更新于 2026-11-25T08:32:08.255670-08:00。

## 单元与顺序

154-B → PS6 评审材料发布 → 160 G 链 → 符合条件时的 157-B。

| 单元 | 状态 | 重启时间 |
|---|---|---|
| `llvm-opt-task154-after-153.service` | active/running | Wed 2026-11-25 07:36:45 PST |
| `llvm-opt-task160-g-chain.service` | active/running | Wed 2026-11-25 07:36:45 PST |
| `llvm-opt-task161-night.service` | active/running | — |
| `llvm-opt-task161-backup-scan.service` | inactive/dead | — |
| `llvm-opt-task161-backup-duplicates.service` | inactive/dead | — |
| `llvm-opt-task160-backup-large.service` | inactive/dead | — |
| `llvm-opt-task160-backup-evidence.service` | active/running | — |
| `llvm-opt-task154-full-build-1.service` | active/running | — |
| `llvm-opt-task154-full-build-2.service` | inactive/dead | — |

## 步骤与资源

| 步骤 | 结论 | 用时 s | 等待 s | 原因 |
|---|---|---:|---:|---|
| 154-B | RUNNING | — | — | waiting for 139-D memory floor or build disk allowance |
| G4 | WAITING | — | — | active: llvm-opt-task154-after-153.service |
| G5 | WAITING | — | — | — |
| G6 | WAITING | — | — | — |
| G7 | WAITING | — | — | — |
| G8 | WAITING | — | — | — |
| 157-B | WAITING | — | — | — |

154-B 准入时 /home 可用 318,757,634,048 B，MemAvailable 22,569,095,168 B。

154-B 仍采用原磁盘准入线 302,154,457,695 B，包含 30 GB 预留。
160 补充累计净释放 46,013,472,768 B，其中本次接续 46,010,806,272 B。清理结束时 /home 可用 318,757,769,216 B。

当前 /home 可用 318,737,539,072 B，MemAvailable 22,498,668,544 B。

| 采样时间 | /home 可用 B | /home 已用 B | MemAvailable B |
|---|---:|---:|---:|
| 2026-11-25T07:42:25.370727-08:00 | 272,888,152,064 | 1,594,920,185,856 | 26,156,494,848 |
| 2026-11-25T07:52:38.788365-08:00 | 269,105,528,832 | 1,598,702,809,088 | 26,224,234,496 |
| 2026-11-25T08:02:41.431837-08:00 | 268,303,159,296 | 1,599,505,178,624 | 21,684,121,600 |
| 2026-11-25T08:12:57.194729-08:00 | 263,856,209,920 | 1,603,952,128,000 | 19,990,609,920 |
| 2026-11-25T08:22:57.550108-08:00 | 263,856,209,920 | 1,603,952,128,000 | 18,980,921,344 |

G4 已记录 0 条 ARCHIVE_MEMBER_RETRY。 [160 G 链报告](160_g_chain.md) · [采样原文](../../tools/bolt/results/task161/resources.jsonl)
