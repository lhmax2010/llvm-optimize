# 138-N 夜间验证

**N2 SKIPPED，G2 PASS，G3 PASS，G4 SKIPPED，G5 SKIPPED，G6 SKIPPED，G7 SKIPPED，G8 SKIPPED，N4 SKIPPED。**

单元 llvm-opt-138n-20261119.service，截止 2026-11-20T08:30:00+08:00。启动 MemAvailable 20.22 GiB，/home 可用 352.98 GiB。看门狗触发：否。[逐步 JSON](../../tools/bolt/results/task138-n-20261119/summary.json)

| 步骤 | 结论 | 档位 | MemoryMax GiB | 并行 | 开始 | 结束 | 等待秒 | 执行秒 | 内存峰值 B | 准入 MemAvailable GiB | 准入 /home GiB | 原因 |
|---|---|---|---:|---:|---|---|---:|---:|---:|---:|---:|---|
| N2 | SKIPPED | — | — | — | — | — | 1800.003 | — | — | 18.89 | 352.97 | MemAvailable minus 6 GiB below stage floor |
| G2 | PASS | dynamic | 1.66 | 1 | 2026-11-19T00:54:06-08:00 | 2026-11-19T00:58:06-08:00 | 0.0 | 239.723 | 1778184192 | 18.88 | 352.97 | — |
| G3 | PASS | dynamic | 2.04 | 1 | 2026-11-19T00:58:08-08:00 | 2026-11-19T00:58:22-08:00 | 0.0 | 13.129 | 2189705216 | 18.92 | 370.78 | — |
| G4 | SKIPPED | — | — | — | — | — | 1800.002 | — | — | 19.00 | 370.73 | MemAvailable minus 6 GiB below stage floor |
| G5 | SKIPPED | — | — | — | — | — | 0 | — | — | 18.96 | 370.73 | PGO prerequisite did not pass |
| G6 | SKIPPED | — | — | — | — | — | 0 | — | — | 18.95 | 370.73 | PGO prerequisite did not pass |
| G7 | SKIPPED | — | — | — | — | — | 0 | — | — | 18.94 | 370.73 | PGO prerequisite did not pass |
| G8 | SKIPPED | — | — | — | — | — | 0 | — | — | 18.94 | 370.73 | PGO prerequisite did not pass |
| N4 | SKIPPED | — | — | — | — | — | 1800.004 | — | — | 19.05 | 370.73 | MemAvailable minus 6 GiB below stage floor |

N2、N4 使用 82 号 Toolchain 入口所核对的源码、配置和导出步骤。每步重新测量内存，按 `min(MemAvailable − 6 GiB, 标准上限)` 分配 cgroup 限额。完整构建通过 `mlgo_build_jobs` 传递并行度，产品参数保持原样。N2、N4 磁盘线为 90 GiB。G2、G3 磁盘线取旧 G1 构建根、profraw 和 profdata 分项，其余 G 步骤取 131 号去掉 30 GiB 余量后的规划值 95.626 GiB。

N2 关闭开关预检

~~~json
{
  "switch": "_without_llvm_speedup 1",
  "checks": {
    "hybrid_OFF": true,
    "unsets_cache": true,
    "bolt_absent": true,
    "python3_required": true,
    "converter_active": true,
    "thin_lto_retained": true
  }
}
~~~



| 步骤 | 本地路径 | 字节 | SHA256 |
|---|---|---:|---|

[PGO 续跑](132_pgo_pair_generation.md) · [361624 续跑](112_361624_combined_validation.md)
