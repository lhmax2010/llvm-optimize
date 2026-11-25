# 161 · 夜间接续汇总

## 需要用户处理的事项

- PS6 等待 154-B 结束并发布验证证据。
- PGO+BOLT 候选状态为 等待 G 链。—
- 大型库已删除 0/11，3 个自测库保留。

更新于 2026-11-25T07:52:01.703275-08:00。

## 单元与顺序

154-B → PS6 评审材料发布 → 160 G 链 → 符合条件时的 157-B。

| 单元 | 状态 | 重启时间 |
|---|---|---|
| `llvm-opt-task154-after-153.service` | active/running | Wed 2026-11-25 07:36:45 PST |
| `llvm-opt-task160-g-chain.service` | active/running | Wed 2026-11-25 07:36:45 PST |
| `llvm-opt-task161-night.service` | active/running | — |
| `llvm-opt-task161-backup-scan.service` | inactive/dead | — |
| `llvm-opt-task161-backup-duplicates.service` | inactive/dead | — |
| `llvm-opt-task160-backup-large.service` | active/running | — |
| `llvm-opt-task160-backup-evidence.service` | active/running | — |
| `llvm-opt-task154-full-build-1.service` | inactive/dead | — |
| `llvm-opt-task154-full-build-2.service` | inactive/dead | — |

## 步骤与资源

| 步骤 | 结论 | 用时 s | 等待 s | 原因 |
|---|---|---:|---:|---|
| 154-B | WAITING | — | — | waiting for 139-D memory floor or build disk allowance |
| G4 | WAITING | — | — | — |
| G5 | WAITING | — | — | — |
| G6 | WAITING | — | — | — |
| G7 | WAITING | — | — | — |
| G8 | WAITING | — | — | — |
| 157-B | WAITING | — | — | — |

154-B 仍采用原磁盘准入线 302,154,457,695 B，包含 30 GB 预留。

当前 /home 可用 269,776,674,816 B，MemAvailable 26,190,389,248 B。

| 采样时间 | /home 可用 B | /home 已用 B | MemAvailable B |
|---|---:|---:|---:|
| 2026-11-25T07:42:25.370727-08:00 | 272,888,152,064 | 1,594,920,185,856 | 26,156,494,848 |

G4 已记录 0 条 ARCHIVE_MEMBER_RETRY。 [160 G 链报告](160_g_chain.md) · [采样原文](../../tools/bolt/results/task161/resources.jsonl)
