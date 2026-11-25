# 150 · PGO/BOLT profile 生成

**进行中**

|步骤|结论|档位|MemoryMax B|编译/ThinLTO/链接|起止 PST|等待 s|执行 s|cgroup 峰值 B|准入内存 B|准入磁盘 B|清理 df 差值 B|原因|
|---|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| G4 | SKIPPED | — | — | —/—/— | — → 2026-11-24T21:08:30-08:00 | 3600.0 | — | — | 16467451904 | 303165779968 | — | disk below floor |
| G5 | SKIPPED | — | — | —/—/— | — → 2026-11-24T21:08:34-08:00 | 0 | — | — | 16437882880 | 303165681664 | — | G chain prerequisite did not pass |
| G6 | SKIPPED | — | — | —/—/— | — → 2026-11-24T21:08:38-08:00 | 0 | — | — | 16414334976 | 303165595648 | — | G chain prerequisite did not pass |
| G7 | SKIPPED | — | — | —/—/— | — → 2026-11-24T21:08:41-08:00 | 0 | — | — | 16465092608 | 303165509632 | — | G chain prerequisite did not pass |
| G8 | SKIPPED | — | — | —/—/— | — → 2026-11-24T21:08:45-08:00 | 0 | — | — | 16441831424 | 303165419520 | — | G chain prerequisite did not pass |

本地配方 750d7a83475a3c3c6fecf545ea74ba110fc845f5。两轮仅配置预演最终扫描 25,940 条 Ninja 记录，0 条违规。第一轮的 5 条分类误报及修正已保留。门禁 8/8、技能 59/59、编排 6/6 通过。N2 已由 149-run 完成。预演只运行 CMake 和门禁，配置之后退出。

峰值增长 P 为 222,650,722,030 B。G4 准入包含 15% 系数、15 GiB 安全线和另一项目的 40 GB 磁盘预留。

启动时 2026-11-24T20:08:30-08:00，MemAvailable 16,909,451,264 B，/home 可用 303,195,275,264 B。
G6 等待截止 2026-11-25T06:00:00-08:00。整体截止 2026-11-26T20:00:00-08:00。

- G4 磁盘准入 312,154,457,695 B
- G5 磁盘准入 88,318,382,080 B
- G6 磁盘准入 61,054,246,912 B
- G7 磁盘准入 62,548,578,304 B
- G8 磁盘准入 58,253,611,008 B

若 G4 通过，先保留经过 SHA256 核对的 clang 和成品清单。G5 复用 G4 的对象和 Ninja 图重链，核对导出的 ELF、BOLT 工具和匹配运行库后清理交接根。G3 检查点按内容核对，IR 源提交与新的 PGO 源提交分别登记。

看门狗只停止本任务当前子单元。清理之后按依赖关系和准入规则继续。

[最终配方补丁](../../tools/bolt/results/task150/pgo-recipe-final.patch) · [门禁修正](../../tools/bolt/results/task150/preview-1/gate-correction.diff) · [两轮预演](../../tools/bolt/results/task150/preview-summary.json) · [门禁单测](../../tools/bolt/results/task150/gate-tests-final.txt) · [上次 sudo 结果复测](../../tools/bolt/results/task150/sudo-recheck.json)

## 日志与结果

### G4

[G4 JSON 与日志索引](../../tools/bolt/results/task150/G4.json)

### G5

[G5 JSON 与日志索引](../../tools/bolt/results/task150/G5.json)

~~~json
{
  "artifacts": []
}
~~~

### G6

[G6 JSON 与日志索引](../../tools/bolt/results/task150/G6.json)

~~~json
{
  "artifacts": [],
  "VmHWM_sample": null
}
~~~

### G7

[G7 JSON 与日志索引](../../tools/bolt/results/task150/G7.json)

### G8

[G8 JSON 与日志索引](../../tools/bolt/results/task150/G8.json)

~~~json
{
  "artifacts": []
}
~~~
