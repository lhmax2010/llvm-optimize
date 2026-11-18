# 133-N：PS5 补验证

**N1 PASS，N2 SKIPPED。** S0 核对 239 条路径全部不存在，提交 0604b323ac64a243b8f25facbb2e4adafe0e42f9。启动时 MemAvailable=20,745,383,936 B，/home 可用=412,408,229,888 B。

| 步骤 | 结论 | 档位 | MemoryMax B | 开始 | 结束 | 等待 s | 执行 s | cgroup peak B | MemAvailable B | /home 可用 B | 依据 |
|---|---|---|---:|---|---|---:|---:|---:|---:|---:|---|
| N1 | PASS | standard | 12884901888 | 2026-11-18T07:44:59-08:00 | 2026-11-18T08:25:00-08:00 | 300.0 | 2401.045 | 7854043136 | 23316848640 | 415109783552 | — |
| N2 | SKIPPED | — | — | — | — | 1800.004 | — | UNKNOWN | 24337256448 | 412757655552 | MemAvailable minus 8 GiB below reduced MemoryMax |

N1 采用任务指定标准 12 GiB，缩减档依据 99 号第 5 步实测 11,222,745,088 B。N2、N4 预算引用 74 号 T 实测 24,482,992,128 B（触顶），按规则计算两个档位。SKIPPED 行记录最后准入测量。

N1 完整细项见状态 JSON。

N1 资源原文（VmHWM 为采样值）

~~~json
{
  "memory.peak": "7854043136",
  "VmHWM_sample": {
    "bytes": 561270784,
    "pid": 2124518,
    "argv": "/usr/bin/python3 -B /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/worker.py /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118 N1 standard 2 12884901888 400"
  },
  "memory.events": "low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0",
  "memory.stat": "anon 154038272\nfile 5930164224",
  "memory.max": "12884901888",
  "memory.swap.peak": "0"
}
~~~



N2 的 RPM 4.14 只读展开：hybrid_OFF=True, unsets_cache=True, bolt_absent=True, python3_required=True, converter_active=True, thin_lto_retained=True。有效定义为 gbs build --define '_without_llvm_speedup 1'。首次脚本误把仍然存在的 Source1201 声明当作调用，修正后只检查执行段，未改 spec。

## 留在本机的证据

| 步骤 | 文件 | 字节 | SHA256 |
|---|---|---:|---|
| N1 | /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/N1/replay-results.json | 44015 | 5223bc7310c48db7f9fa5227042706b4a0ca9a6dcf93c2561f7a40d6a4e0bb59 |
| N1 | /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/N1/service.log | 145897 | b9eaa32e8342122f0bd51193265678e543b82de11d1be67d9ab70ea53128925e |

本地结果目录 /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118。全部步骤状态见[总 JSON](../../tools/bolt/results/task133-n/summary.json)。看门狗触发：否。
