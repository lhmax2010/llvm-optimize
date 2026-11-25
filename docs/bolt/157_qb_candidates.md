# 157 · QB PGO 候选

固定配方 `750d7a83475a3c3c6fecf545ea74ba110fc845f5`，tree `0ab6abcd20184eeab988d139b28d2ef164707dcf`，直接父提交 `e42a56bd17f2870e184e48f7d0b8769f7b505d85`。PS5 `7b05a13744d1cf81a5e9cff22a27eb037bf1b6a8` 是祖先。

候选面向 Toolchain 项目 T，当前 profile 只含 T 的映射。x86_64 的 RPM 展开使用 LLVM_PROFDATA_FILE，CMake 源码将它转换为 -fprofile-instr-use。验证通过脚本模式执行对应 CMake 片段，不配置或编译 LLVM。ARM 展开与集成提交逐字节比较。

| 候选 | 结论 | 集成提交 | QB 测试提交 | 远端分支或停止原因 |
|---|---|---|---|---|
| A | STOP | — | — | G4 FAIL: profile skill exited 1: {'status': 'STOP', 'project': 'T', 'stages': [{'name': 'pgo-build', 'status': 'STOP', 'attempt': '/home/linhao/Toolchain/development/llvm-optimize/archive/task151/G-profiles/pgo-build-1795596865301453852'}], 'started_at': '2026-11-25T08:53:12+00:00', 'admission': [{'at': '2026-11-25T08:53:12+00:00', 'memory': 19849625600, 'disk': {'/home': 303581949952, '/home/linhao/Toolchain/development/llvm-optimize/archive/task151/G-profiles': 303581949952}, 'admission_memory': 20304826368, 'stage': 'pgo-build', 'memory_max': 16009859072, 'standard_cap': 25769803776, 'floor': 10737418240, 'jobs': 4, 'thinlto_jobs': 4, 'link_jobs': 1, 'admitted': True, 'actual_memory_max': 16009859072}], 'reason': 'command failed (1); see /home/linhao/Toolchain/development/llvm-optimize/archive/task151/G-profiles/pgo-build-1795596865301453852/build-0.txt', 'ended_at': '2026-11-25T12:25:55+00:00'} |
| B | STOP | — | — | A prerequisites did not pass |

远端 refs/heads 创建使用普通 push。pre-push 门禁要求 Gerrit 通告该引用的旧 SHA 全零，避免并发更新已存在分支。

[A 状态和阶段原文](../../tools/bolt/results/task157/A/result.json)
[B 状态和阶段原文](../../tools/bolt/results/task157/B/result.json)

## 160 号续做

A 的 G4 前置条件已按 160 号裁决移除。新的 PGO-only 测试分支 `sandbox/lhmax2025/llvm-pgo-only-20261125` 已核对为 `7a54d3ff49841eb4753453813ed68d9f2e63d405`。B 仍须等 160 重跑的 G6、G7、G8 都通过。[验收和远端回执](160_converter_retry.md)
