# 151 B · G 链

**G4 已通过资源准入并启动。** 2026-11-25 00:48:12 PST，编排单元 llvm-opt-151-g-chain.service 启动。采用任务 150 最终配方 750d7a83475a3c3c6fecf545ea74ba110fc845f5。该配方已通过 150 的仅配置预演，G4 的实际 CMake 配置后仍执行完整 Ninja 门禁。

| 步骤 | 磁盘准入 B | 内存下限 | 当前状态 |
|---|---:|---|---|
| G4 | 302154457695 | 10 GiB | 运行，4/4/1，MemoryMax 16009859072 B |
| G5 | 78318382080 | 15 GiB | 等待 G4 |
| G6 | 51054246912 | 首选 18 GiB，回退 16 GiB | 等待 G5 |
| G7 | 52548578304 | 9 GiB | 等待 G6 |
| G8 | 48253611008 | 1 GiB | 等待 G7 |

启动时 /home 可用 304,148,254,720 B，MemAvailable 20,304,826,368 B。P 采用 222,650,722,030 B，磁盘预留为 15 GiB 加 30 GB。G4 最多等待 3 小时，G5 最多等待 60 分钟。G6 等待截止为 2026-11-26 06:00 PST，总截止为 2026-11-26 20:00 PST。

用户的两份 sudo 输出共登记 5 条，均无拒绝。149-run 三处记录为 0 B。150 两处记录为 1,065,443,328 B 和 1,065,447,424 B。脚本统计的已释放块和两个时点的全机 df 差值分别保留。

7 项编排单测通过，覆盖更新后的磁盘预留、首选与回退、回退档 OOM、步骤清理以及看门狗停止后的准入。N2 沿用 149-run 结果。

[启动 JSON](../../tools/bolt/results/task151/startup.json) · [sudo 输出与复测](../../tools/bolt/results/task151/sudo-recheck.json) · [编排单测](../../tools/bolt/results/task151/tests.txt)

### 运行时依赖门禁准备核对

用 149-run 保存的成品编译器运行时 RPM 复现了外部技能检查的误报。旧检查递归审计了编译器资源目录中的 libclang_rt.profile-x86_64.a，该归档本身就是链接插桩时使用的运行时库。技能现与 R 的 RPM 门禁使用相同范围，检查发货 ELF 和普通库目录中的静态开发归档。PGO 配方、实际 Ninja 门禁和禁止运行时依赖的条件保持一致。真实夹具与技能 60 项测试通过。

[旧检查原文](../../tools/bolt/results/task151/runtime-scope-legacy.json) · [修正 diff](../../tools/bolt/results/task151/runtime-scope-correction.diff) · [真实夹具结果](../../tools/bolt/results/task151/runtime-scope-corrected.json)
