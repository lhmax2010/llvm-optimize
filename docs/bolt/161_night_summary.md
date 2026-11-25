# 161 · 夜间接续汇总

## 需要用户处理的事项

- PS6 的 154-B 结果为 **PARTIAL**。 [评审材料](161_ps6_review_packet.md)
- PGO+BOLT 候选状态为 等待 G 链。—
- 大型库已删除 11/11，3 个自测库保留。
- [154-B 的 sudo 清理脚本](../../tools/bolt/results/task154/sudo-clean.sh) 等待用户审核。
- G4 FAIL。PermissionError: [Errno 13] Permission denied: '/home/linhao/Toolchain/development/llvm-optimize/archive/task160/run/G4/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0' -> '/home/linhao/Toolchain/development/llvm-optimize/archive/task160/run/G5/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'。
- 大型库归档首轮 STOP，原因是 SHA256 检查调用错误。续做已通过。 [首轮原始提交](https://github.com/lhmax2010/llvm-optimize/blob/2720eb0b/tools/bolt/results/task160/backup-supplement/large-terminal.json)

更新于 2026-11-25T13:54:46.406371-08:00。

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
| G4 | FAIL | 7963.344 | 0.0 | PermissionError: [Errno 13] Permission denied: '/home/linhao/Toolchain/development/llvm-optimize/archive/task160/run/G4/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0' -> '/home/linhao/Toolchain/development/llvm-optimize/archive/task160/run/G5/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0' |
| G5 | WAITING | — | — | — |
| G6 | WAITING | — | — | — |
| G7 | WAITING | — | — | — |
| G8 | WAITING | — | — | — |
| 157-B | WAITING | — | — | — |

154-B 准入时 /home 可用 318,757,634,048 B，MemAvailable 22,569,095,168 B。

154-B 仍采用原磁盘准入线 302,154,457,695 B，包含 30 GB 预留。
160 补充累计净释放 46,013,472,768 B，其中本次接续 46,010,806,272 B。清理结束时 /home 可用 318,757,769,216 B。

当前 /home 可用 248,547,512,320 B，MemAvailable 28,047,671,296 B。

| 采样时间 | /home 可用 B | /home 已用 B | MemAvailable B |
|---|---:|---:|---:|
| 2026-11-25T12:43:43.222284-08:00 | 268,700,606,464 | 1,599,107,731,456 | 27,001,974,784 |
| 2026-11-25T12:53:43.724476-08:00 | 247,243,841,536 | 1,620,564,496,384 | 26,940,633,088 |
| 2026-11-25T13:03:44.137797-08:00 | 244,001,533,952 | 1,623,806,803,968 | 22,610,481,152 |
| 2026-11-25T13:13:44.551629-08:00 | 240,898,097,152 | 1,626,910,240,768 | 26,321,682,432 |
| 2026-11-25T13:23:45.030415-08:00 | 239,462,756,352 | 1,628,345,581,568 | 26,916,491,264 |
| 2026-11-25T13:33:45.483531-08:00 | 245,240,287,232 | 1,622,568,050,688 | 27,077,296,128 |
| 2026-11-25T13:43:45.957085-08:00 | 243,365,498,880 | 1,624,442,839,040 | 25,281,990,656 |
| 2026-11-25T13:53:46.371676-08:00 | 250,178,469,888 | 1,617,629,868,032 | 27,773,317,120 |

G4 已记录 1 条 ARCHIVE_MEMBER_RETRY。 [160 G 链报告](160_g_chain.md) · [采样原文](../../tools/bolt/results/task161/resources.jsonl)

~~~text
[ 4766s] ARCHIVE_MEMBER_RETRY usr/lib64/libclangAST.a Disasm.cpp.o 8589934592 PASS
~~~
