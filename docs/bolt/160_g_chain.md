# 160 · PGO/BOLT profile 重跑

**最终**

|步骤|结论|档位|MemoryMax B|编译/ThinLTO/链接|起止 PST|等待 s|执行 s|cgroup 峰值 B|准入内存 B|准入磁盘 B|清理 df 差值 B|原因|
|---|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| G4 | FAIL | dynamic | 23250112512 | 6/6/1 | 2026-11-25T11:41:50-08:00 → 2026-11-25T13:54:34-08:00 | 0.0 | 7963.344 | 23250112512 | 27545079808 | 310068699136 | -1630748672 | PermissionError: [Errno 13] Permission denied: '/home/linhao/Toolchain/development/llvm-optimize/archive/task160/run/G4/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0' -> '/home/linhao/Toolchain/development/llvm-optimize/archive/task160/run/G5/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0' |
| G5 | SKIPPED | — | — | —/—/— | — → 2026-11-25T13:54:54-08:00 | 0 | — | — | 28049133568 | 248547352576 | — | G chain prerequisite did not pass |
| G6 | SKIPPED | — | — | —/—/— | — → 2026-11-25T13:55:02-08:00 | 0 | — | — | 28018921472 | 248547192832 | — | G chain prerequisite did not pass |
| G7 | SKIPPED | — | — | —/—/— | — → 2026-11-25T13:55:06-08:00 | 0 | — | — | 28039430144 | 248547115008 | — | G chain prerequisite did not pass |
| G8 | SKIPPED | — | — | —/—/— | — → 2026-11-25T13:55:10-08:00 | 0 | — | — | 28034629632 | 248547037184 | — | G chain prerequisite did not pass |

本地配方 ce627fa087233d9da415887222009155fe8b5029。转换器重试修复未触及 PGO Ninja 门禁，沿用 150 的预演。G4 的配方在 CMake 后、编译前执行完整 Ninja 门禁。N2 已由 149-run 完成。

峰值增长 P 为 222,650,722,030 B。G4 准入包含 15% 系数、15 GiB 安全线和另一项目的 30 GB 磁盘预留。

启动时 2026-11-25T11:41:50-08:00，MemAvailable 27,545,120,768 B，/home 可用 310,068,703,232 B。
G6 等待截止 2026-11-27T06:00:00-08:00。整体截止 2026-11-27T20:00:00-08:00。

- G4 磁盘准入 302,154,457,695 B
- G5 磁盘准入 78,318,382,080 B
- G6 磁盘准入 51,054,246,912 B
- G7 磁盘准入 52,548,578,304 B
- G8 磁盘准入 48,253,611,008 B

若 G4 通过，先保留经过 SHA256 核对的 clang 和成品清单。G5 复用 G4 的对象和 Ninja 图重链，核对导出的 ELF、BOLT 工具和匹配运行库后清理交接根。G3 检查点按内容核对，IR 源提交与新的 PGO 源提交分别登记。

看门狗只停止本任务当前子单元。清理之后按依赖关系和准入规则继续。

[150 的配方和预演](150_g_chain.md) · [修复和候选报告](160_converter_retry.md) · [160 编排单测](../../tools/bolt/results/task160/g-chain/tests.txt)

## 日志与结果

看门狗触发 False，结束时 /home 可用 248,546,959,360 B。
需要 sudo 复核的残留 2 项。脚本仅保留在本地。
[最终汇总 JSON](../../tools/bolt/results/task160/g-chain/summary.json)

### G4

[G4 JSON 与日志索引](../../tools/bolt/results/task160/g-chain/G4.json)

~~~json
{
  "pgo_clang": {
    "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task160/run/G4/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/clang-22",
    "bytes": 1630727512,
    "sha256": "8e12df73617ccf3e086c32f1ceba67e85712f1007dba7e6e1895ac5d3d8abf90"
  },
  "merged_profdata": {
    "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task160/run/G-profiles/clang.profdata",
    "bytes": 52530416,
    "sha256": "39171c4a5fcb6166ac86d6d47ad16c7890527a73e66c26f035fb910288f496aa"
  },
  "archive_member_retries": [
    "[ 4766s] ARCHIVE_MEMBER_RETRY usr/lib64/libclangAST.a Disasm.cpp.o 8589934592 PASS"
  ]
}
~~~

### G5

[G5 JSON 与日志索引](../../tools/bolt/results/task160/g-chain/G5.json)

~~~json
{
  "artifacts": []
}
~~~

### G6

[G6 JSON 与日志索引](../../tools/bolt/results/task160/g-chain/G6.json)

~~~json
{
  "artifacts": [],
  "VmHWM_sample": null
}
~~~

### G7

[G7 JSON 与日志索引](../../tools/bolt/results/task160/g-chain/G7.json)

### G8

[G8 JSON 与日志索引](../../tools/bolt/results/task160/g-chain/G8.json)

~~~json
{
  "artifacts": []
}
~~~
