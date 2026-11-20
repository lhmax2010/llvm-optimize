# 148 · 周末构建与离线 profile

**最终：N2 FAIL，G4 FAIL，G5 SKIPPED，G6 SKIPPED，G7 SKIPPED，G8 SKIPPED，N4 SUPERSEDED。**

周报原样归档，提交 4ff2be33d7c8d1a68c8495955b2717a033b3a75d。[周报](weekly/2026-11-20_weekly_report.md)

361624 PS5 cbaa01f5c148f5cc705f969e13ac41fef811a9f9 的树 ef1ab363fa8e9be29eb930916e86c6e8f10f11af 与 C2 相同。144 的 B1 与 145 的 B2 覆盖 N4.1 / N4.2；145、146 及 147 裁决完成差异归类。旧 I 的 133-N 和 138-N N4 均未运行，替代依据是后继产品树的验证。

[112](112_361624_combined_validation.md) · [138-N](138_night_validation.md) · [144](144_361624_next_ps.md) · [145](145_classification_and_b2.md) · [146](146_classification_v2.md) · [147 裁决](147_pm_ruling_and_prep.md) · [147 PS5](147_push.md)

## 执行记录

|步骤|结果|档位|MemoryMax B|编译/ThinLTO/链接|开始|结束|等待 s|执行 s|cgroup 峰值 B|准入 MemAvailable B|准入 /home B|原因|
|---|---|---|---:|---|---|---|---:|---:|---:|---:|---:|---|
| N2 | FAIL | dynamic | 22000951296 | 6/6/1 | 2026-11-20T07:47:49-08:00 | 2026-11-20T07:51:57-08:00 | 0.0 | 247.467 | 10126950400 | 26295918592 | 267874074624 | Command '['/usr/bin/gbs', '-c', '/home/linhao/Toolchain/development/llvm-optimize/archive/task148/N2/gbs.conf', 'build', '-A', 'x86_64', '-B', '/home/linhao/Toolchain/development/llvm-optimize/archive/task148/N2/gbs-driver', '-c', '7b05a13744d1cf81a5e9cff22a27eb037bf1b6a8', '--threads=6', '--define', 'jobs 6', '--define', '_smp_mflags -j6', '--define', '_costomized_smp_mflags -j6', '--define', 'mlgo_build_jobs 6', '--define', '_without_llvm_speedup 1', '--define', '_buildshell /var/tmp/llvm-stage-jobs/build-shell', '--noinit', '--baselibs', '--style=tar', '--spec', 'llvm.spec', '/home/linhao/Toolchain/development/llvm-optimize/archive/task148/N2/source']' returned non-zero exit status 1. |
| G4 | FAIL | dynamic | 21220311040 | 4/4/1 | 2026-11-20T07:51:59-08:00 | 2026-11-20T07:55:25-08:00 | 0.0 | 206.242 | 11801169920 | 25515278336 | 259943448576 | profile skill exited 1: {'status': 'STOP', 'project': 'T', 'stages': [{'name': 'pgo-build', 'status': 'STOP', 'attempt': '/home/linhao/Toolchain/development/llvm-optimize/archive/task148/G-profiles/pgo-build-1795189969263471273'}], 'started_at': '2026-11-20T15:52:45+00:00', 'admission': [{'at': '2026-11-20T15:52:45+00:00', 'memory': 25715462144, 'disk': {'/home': 259890814976, '/home/linhao/Toolchain/development/llvm-optimize/archive/task148/G-profiles': 259890814976}, 'admission_memory': 25515278336, 'stage': 'pgo-build', 'memory_max': 21220311040, 'standard_cap': 25769803776, 'floor': 10737418240, 'jobs': 4, 'thinlto_jobs': 4, 'link_jobs': 1, 'admitted': True, 'actual_memory_max': 21220311040}], 'reason': 'command failed (1); see /home/linhao/Toolchain/development/llvm-optimize/archive/task148/G-profiles/pgo-build-1795189969263471273/build-0.txt', 'ended_at': '2026-11-20T15:55:25+00:00'} |
| G5 | SKIPPED | — | — | —/—/— | — | — | 0 | — | — | 25114677248 | 251896549376 | PGO prerequisite did not pass |
| G6 | SKIPPED | — | — | —/—/— | — | — | 0 | — | — | 25104842752 | 251896532992 | PGO prerequisite did not pass |
| G7 | SKIPPED | — | — | —/—/— | — | — | 0 | — | — | 25102618624 | 251896516608 | PGO prerequisite did not pass |
| G8 | SKIPPED | — | — | —/—/— | — | — | 0 | — | — | 25099423744 | 251896500224 | PGO prerequisite did not pass |

启动时 2026-11-20T07:47:49-08:00，MemAvailable 26,295,918,592 B，/home 可用 267,874,078,720 B。截止 2026-11-23T06:00:00-08:00。

每步资源采用 [139-D](139_resource_diagnosis.md)；N2、G4、G5 等待上限各 60 分钟，G6 内存下限 18 GiB。编排使用本任务独立锁；G1–G3 收据只读核对后迁入本次根。

## 门禁和产物

### N2

[逐步记录及结束日志](../../tools/bolt/results/task148/N2.json)

~~~json
{
  "failure": "Traceback (most recent call last):\n  File \"/home/linhao/Toolchain/development/llvm-optimize/archive/task148/orchestration/worker.py\", line 157, in <module>\n    out=build(A,D,W,B,TASK,TIER,JOBS,MEM,CPU)\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/linhao/Toolchain/development/llvm-optimize/archive/task148/orchestration/buildsteps.py\", line 292, in build\n    rpms=run_gbs(w,d,source,ref,\"llvm.spec\",jobs,exp,extra)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/linhao/Toolchain/development/llvm-optimize/archive/task148/orchestration/buildsteps.py\", line 154, in run_gbs\n    checked(*argv,cwd=source,output=d/\"gbs.log\")\n  File \"/home/linhao/Toolchain/development/llvm-optimize/archive/task148/orchestration/buildsteps.py\", line 30, in checked\n    return subprocess.run(argv,cwd=cwd,env=env or CLEAN_ENV,stdout=f,stderr=subprocess.STDOUT,check=True)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/usr/lib/python3.12/subprocess.py\", line 571, in run\n    raise CalledProcessError(retcode, process.args,\nsubprocess.CalledProcessError: Command '['/usr/bin/gbs', '-c', '/home/linhao/Toolchain/development/llvm-optimize/archive/task148/N2/gbs.conf', 'build', '-A', 'x86_64', '-B', '/home/linhao/Toolchain/development/llvm-optimize/archive/task148/N2/gbs-driver', '-c', '7b05a13744d1cf81a5e9cff22a27eb037bf1b6a8', '--threads=6', '--define', 'jobs 6', '--define', '_smp_mflags -j6', '--define', '_costomized_smp_mflags -j6', '--define', 'mlgo_build_jobs 6', '--define', '_without_llvm_speedup 1', '--define', '_buildshell /var/tmp/llvm-stage-jobs/build-shell', '--noinit', '--baselibs', '--style=tar', '--spec', 'llvm.spec', '/home/linhao/Toolchain/development/llvm-optimize/archive/task148/N2/source']' returned non-zero exit status 1.\n"
}
~~~

### G4

[逐步记录及结束日志](../../tools/bolt/results/task148/G4.json)

~~~json
{
  "artifacts": [],
  "failure": "Traceback (most recent call last):\n  File \"/home/linhao/Toolchain/development/llvm-optimize/archive/task148/orchestration/worker.py\", line 163, in <module>\n    out=generate(A,D,W,B,TASK,TIER,JOBS,MEM,CPU)\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/linhao/Toolchain/development/llvm-optimize/archive/task148/orchestration/pgosteps.py\", line 288, in generate\n    raise RuntimeError(f\"profile skill exited {proc.returncode}: {err}\")\nRuntimeError: profile skill exited 1: {'status': 'STOP', 'project': 'T', 'stages': [{'name': 'pgo-build', 'status': 'STOP', 'attempt': '/home/linhao/Toolchain/development/llvm-optimize/archive/task148/G-profiles/pgo-build-1795189969263471273'}], 'started_at': '2026-11-20T15:52:45+00:00', 'admission': [{'at': '2026-11-20T15:52:45+00:00', 'memory': 25715462144, 'disk': {'/home': 259890814976, '/home/linhao/Toolchain/development/llvm-optimize/archive/task148/G-profiles': 259890814976}, 'admission_memory': 25515278336, 'stage': 'pgo-build', 'memory_max': 21220311040, 'standard_cap': 25769803776, 'floor': 10737418240, 'jobs': 4, 'thinlto_jobs': 4, 'link_jobs': 1, 'admitted': True, 'actual_memory_max': 21220311040}], 'reason': 'command failed (1); see /home/linhao/Toolchain/development/llvm-optimize/archive/task148/G-profiles/pgo-build-1795189969263471273/build-0.txt', 'ended_at': '2026-11-20T15:55:25+00:00'}\n"
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

### G8

[逐步记录及结束日志](../../tools/bolt/results/task148/G8.json)

~~~json
{
  "artifacts": []
}
~~~

看门狗未触发。

[可机读最终记录](../../tools/bolt/results/task148/summary.json)

两步为准备问题，已安排各一次修正重跑。[首次原文](../../tools/bolt/results/task148/first-attempt/README.md)
