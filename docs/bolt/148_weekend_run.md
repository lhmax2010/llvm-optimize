# 148 · 周末构建与离线 profile

**进行中：N2 INTERRUPTED，G4 SKIPPED，G5 SKIPPED，G6 SKIPPED，G7 SKIPPED，G8 PENDING，N4 SUPERSEDED。**

周报原样归档，提交 4ff2be33d7c8d1a68c8495955b2717a033b3a75d。[周报](weekly/2026-11-20_weekly_report.md)

361624 PS5 cbaa01f5c148f5cc705f969e13ac41fef811a9f9 的树 ef1ab363fa8e9be29eb930916e86c6e8f10f11af 与 C2 相同。144 的 B1 与 145 的 B2 覆盖 N4.1 / N4.2；145、146 及 147 裁决完成差异归类。旧 I 的 133-N 和 138-N N4 均未运行，替代依据是后继产品树的验证。

[112](112_361624_combined_validation.md) · [138-N](138_night_validation.md) · [144](144_361624_next_ps.md) · [145](145_classification_and_b2.md) · [146](146_classification_v2.md) · [147 裁决](147_pm_ruling_and_prep.md) · [147 PS5](147_push.md)

首次 N2 和 G4 在开始编译前均被 GBS 拒绝。使用 144 B1 已验证的正常初始化，移除 --noinit 并将 GBS tmpdir 指向各步骤的新目录。两步各用一次修正机会。[首次原文和修正](../../tools/bolt/results/task148/first-attempt/README.md)

## 执行记录

|步骤|结果|档位|MemoryMax B|编译/ThinLTO/链接|开始|结束|等待 s|执行 s|cgroup 峰值 B|准入 MemAvailable B|准入 /home B|原因|
|---|---|---|---:|---|---|---|---:|---:|---:|---:|---:|---|
| N2 | INTERRUPTED | dynamic | 20829827072 | 4/4/1 | 2026-11-20T07:58:57-08:00 | 2026-11-20T13:14:53-08:00 | 0.0 | 18956.297 | 20829827072 | 25124794368 | 251896111104 | — |
| G4 | SKIPPED | — | — | —/—/— | — | — | 0 | — | — | 27002327040 | 15896154112 | watchdog crossed stop line |
| G5 | SKIPPED | — | — | —/—/— | — | — | 0 | — | — | 27003068416 | 15896084480 | watchdog crossed stop line |
| G6 | SKIPPED | — | — | —/—/— | — | — | 0 | — | — | 26952196096 | 15896002560 | watchdog crossed stop line |
| G7 | SKIPPED | — | — | —/—/— | — | — | 0 | — | — | 26996269056 | 15895928832 | watchdog crossed stop line |
| G8 | PENDING | — | — | —/—/— | — | — | — | — | — | — | — | — |

启动时 2026-11-20T07:58:57-08:00，MemAvailable 25,124,794,368 B，/home 可用 251,896,115,200 B。截止 2026-11-23T06:00:00-08:00。

每步资源采用 [139-D](139_resource_diagnosis.md)；N2、G4、G5 等待上限各 60 分钟，G6 内存下限 18 GiB。编排使用本任务独立锁；G1–G3 收据只读核对后迁入本次根。

## 门禁和产物

### N2

[逐步记录及结束日志](../../tools/bolt/results/task148/N2.json)

### G4

[逐步记录及结束日志](../../tools/bolt/results/task148/G4.json)

~~~json
{
  "artifacts": []
}
~~~

### G5

[逐步记录及结束日志](../../tools/bolt/results/task148/G5.json)

### G6

[逐步记录及结束日志](../../tools/bolt/results/task148/G6.json)

~~~json
{
  "artifacts": []
}
~~~

### G7

[逐步记录及结束日志](../../tools/bolt/results/task148/G7.json)
