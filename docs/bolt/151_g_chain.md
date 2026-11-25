# 151 · PGO/BOLT profile 生成

**进行中**

|步骤|结论|档位|MemoryMax B|编译/ThinLTO/链接|起止 PST|等待 s|执行 s|cgroup 峰值 B|准入内存 B|准入磁盘 B|清理 df 差值 B|原因|
|---|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| G4 | FAIL | dynamic | 16009859072 | 4/4/1 | 2026-11-25T00:48:12-08:00 → 2026-11-25T04:25:55-08:00 | 0.0 | 13063.27 | 14270107648 | 20304826368 | 304148250624 | 60365758464 | profile skill exited 1: {'status': 'STOP', 'project': 'T', 'stages': [{'name': 'pgo-build', 'status': 'STOP', 'attempt': '/home/linhao/Toolchain/development/llvm-optimize/archive/task151/G-profiles/pgo-build-1795596865301453852'}], 'started_at': '2026-11-25T08:53:12+00:00', 'admission': [{'at': '2026-11-25T08:53:12+00:00', 'memory': 19849625600, 'disk': {'/home': 303581949952, '/home/linhao/Toolchain/development/llvm-optimize/archive/task151/G-profiles': 303581949952}, 'admission_memory': 20304826368, 'stage': 'pgo-build', 'memory_max': 16009859072, 'standard_cap': 25769803776, 'floor': 10737418240, 'jobs': 4, 'thinlto_jobs': 4, 'link_jobs': 1, 'admitted': True, 'actual_memory_max': 16009859072}], 'reason': 'command failed (1); see /home/linhao/Toolchain/development/llvm-optimize/archive/task151/G-profiles/pgo-build-1795596865301453852/build-0.txt', 'ended_at': '2026-11-25T12:25:55+00:00'} |
| G5 | SKIPPED | — | — | —/—/— | — → 2026-11-25T04:28:44-08:00 | 0 | — | — | 18881126400 | 293855117312 | — | G chain prerequisite did not pass |
| G6 | SKIPPED | — | — | —/—/— | — → 2026-11-25T04:28:48-08:00 | 0 | — | — | 18922160128 | 293855035392 | — | G chain prerequisite did not pass |
| G7 | PENDING | — | — | —/—/— | — → — | — | — | — | — | — | — | — |
| G8 | PENDING | — | — | —/—/— | — → — | — | — | — | — | — | — | — |

本地配方 750d7a83475a3c3c6fecf545ea74ba110fc845f5。采用 150 最终仅配置预演，没有重复预演。G4 的配方在 CMake 后、编译前执行完整 Ninja 门禁。N2 已由 149-run 完成。

峰值增长 P 为 222,650,722,030 B。G4 准入包含 15% 系数、15 GiB 安全线和另一项目的 30 GB 磁盘预留。

启动时 2026-11-25T00:48:12-08:00，MemAvailable 20,304,826,368 B，/home 可用 304,148,254,720 B。
G6 等待截止 2026-11-26T06:00:00-08:00。整体截止 2026-11-26T20:00:00-08:00。

- G4 磁盘准入 302,154,457,695 B
- G5 磁盘准入 78,318,382,080 B
- G6 磁盘准入 51,054,246,912 B
- G7 磁盘准入 52,548,578,304 B
- G8 磁盘准入 48,253,611,008 B

若 G4 通过，先保留经过 SHA256 核对的 clang 和成品清单。G5 复用 G4 的对象和 Ninja 图重链，核对导出的 ELF、BOLT 工具和匹配运行库后清理交接根。G3 检查点按内容核对，IR 源提交与新的 PGO 源提交分别登记。

看门狗只停止本任务当前子单元。清理之后按依赖关系和准入规则继续。

[150 的配方和预演](150_g_chain.md) · [用户的 sudo 输出与复测](../../tools/bolt/results/task151/sudo-recheck.json) · [151 编排单测](../../tools/bolt/results/task151/tests.txt)

## 日志与结果

### G4

[G4 JSON 与日志索引](../../tools/bolt/results/task151/G4.json)

### G5

[G5 JSON 与日志索引](../../tools/bolt/results/task151/G5.json)

~~~json
{
  "artifacts": []
}
~~~

### G6

[G6 JSON 与日志索引](../../tools/bolt/results/task151/G6.json)

~~~json
{
  "artifacts": [],
  "VmHWM_sample": null
}
~~~
