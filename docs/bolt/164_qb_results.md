# 164 · QB 1240309 / 1240310 诊断

**Toolchain 三架构成功。Base-Dev 的 x86_64 在 CMake 前因缺少 D 项目的 PGO 映射失败，aarch64 和 armv7l 成功。**

两份 QB 源码清单与任务 160 的分支回执指向同一测试提交 7a54d3ff49841eb4753453813ed68d9f2e63d405，仓库为 platform/upstream/llvm，分支为 sandbox/lhmax2025/llvm-pgo-only-20261125。Base-Dev 清单还列出了基线 LLVM 条目，实际构建的 llvm 项目由失败包的检出日志确认。 [身份回执](../../tools/bolt/results/task164/candidate-identity.json) · [Toolchain manifest](../../tools/bolt/results/task164/T-manifest.xml) · [Base-Dev manifest](../../tools/bolt/results/task164/D-manifest.xml)

| QB | 项目 | 开始（QB 界面时钟） | 结束（同一时钟） | x86_64 | aarch64 | armv7l | 总体 |
|---|---|---|---|---|---|---|---|
| 1240309 / 1240313 | Tizen-Base-Toolchain | 2026-11-25 14:36:36 | 2026-11-25 19:37:44 | PASS | PASS | PASS | Successful |
| 1240310 / 1240314 | Tizen-Base-Dev | 2026-11-25 14:37:41 | 2026-11-25 18:53:31 | FAIL | PASS | PASS | Failed |

结束时间由界面开始时间加界面时长得出。 [1240309](../../tools/bolt/results/task164/1240309-overview.json) · [1240310](../../tools/bolt/results/task164/1240310-overview.json) · [构建详情 T](../../tools/bolt/results/task164/1240313-overview.json) · [构建详情 D](../../tools/bolt/results/task164/1240314-overview.json)

## 失败原因和最小修复方案

测试候选的 manifest 只有 T 项目的 PGO-only 映射，状态为 UNQUALIFIED。测试提交允许该状态，但映射键仍要求项目和开关完全一致。spec 在 `_toolchain` 已定义时选择 T，其余选择 D。失败包的 `pgo-prepare` 明确传入 D，随后报出 `missing profile mapping: ('D', True, False)`。配置尚未进入 CMake、Ninja、链接、归档转换或打包，因此 D 的日志没有 `ARCHIVE_MEMBER_RETRY`。出错时构建根报告剩余 392,246,706,176 B，日志未显示 OOM、超时或磁盘耗尽。QB 未提供该 worker 的 cgroup 计数器。

最近可核实的成功对照是同项目 QB 1239277 的 x86_64 LLVM。其成功包日志进入 CMake/Ninja、通过归档转换并完成 RPM 构建（第 16757、17410 行），没有 PGO prepare 或 Ninja PGO 门禁。较近的 QB 1240308 未取到 x86_64 LLVM 成功包日志（HTTP 404）。 [历史对照](../../tools/bolt/results/task164/D-prior-reference.json) · [历史下载查询](../../tools/bolt/results/task164/D-prior-package-lookup.txt)

最小改动是在仅供 QB 的候选中只对 T 启用 PGO。要验证 D 上的 PGO，需要为 D 准备并验证与其身份绑定的 profile，再加入精确的 D 映射。此处只记录方案。

## Toolchain 成品核对

- Ninja 门禁 PASS，扫描 25,940 条边、6,236 条编译边，5,357 条使用 profile，879 条为运行库编译，零违规。PGO 匹配度为 UNKNOWN，方法尚未验证。
- `ARCHIVE_MEMBER_RETRY usr/lib64/libclangAST.a Disasm.cpp.o 8589934592 PASS`。归档转换 PASS。构建内运行时依赖门禁检查 225 个归档、133 个 ELF，零发现。
- 独立解包并用 readelf 检查可执行文件和共享库，状态 **PASS**，共 133 个 ELF，0 项发现。此处 ELF 核对使用普通 x86_64 二进制 RPM。静态成员以 QB 构建日志门禁为证。
- QB RPM 的 clang-22 为 125,444,840 B，.text 为 80,773,998 B，SHA256 为 `79d0bb08a31ad6eeb996662c6756a175811378a6021833f5229d02fec020e86e`，BOLT 节为 无。
- 本地 G4 RPM 的 clang-22 为 125,444,840 B，.text 为 80,773,998 B，SHA256 为 `0bcf83e9104103c9ff320e5ef3137605dea20a139d43a25965cbe517b2fcbcb2`，BOLT 节为 无。两个成品的 SHA256 不同。

[T-success-gates.txt](../../tools/bolt/results/task164/T-success-gates.txt) · [elf-audit.json](../../tools/bolt/results/task164/elf-audit.json) · [clang-comparison.txt](../../tools/bolt/results/task164/clang-comparison.txt) · [downloads.json](../../tools/bolt/results/task164/downloads.json) · [llvm-profiles.manifest](../../tools/bolt/results/task164/llvm-profiles.manifest) · [td-selection-source.txt](../../tools/bolt/results/task164/td-selection-source.txt) · [local-logs.json](../../tools/bolt/results/task164/local-logs.json)

## Base-Dev 首个错误原文

包日志第 643–692 行，第一处实际错误在第 683 行。错误前完整保留 40 行，错误后保留至日志结束。

```
[   78s] + tizen_llvm_release=1
[   78s] + case $tizen_llvm_release in
[   78s] + tizen_llvm_debug_sequence=
[   78s] + TIZEN_LLVM_UNREVIEWED=
[   78s] + tizen_llvm_arch=
[   78s] + tizen_llvm_debug_head=
[   78s] + tizen_llvm_debug_tail=
[   78s] + TIZEN_LLVM_NORMALIZED=
[   78s] + TIZEN_LLVM_DROPPED=
[   78s] + tizen_llvm_ifs_set=x
[   78s] + tizen_llvm_saved_ifs=' 	
[   78s] '
[   78s] + unset IFS
[   78s] + case $- in
[   78s] + tizen_llvm_glob_off=0
[   78s] + set -f
[   78s] + test x = x
[   78s] + IFS=' 	
[   78s] '
[   78s] + test 0 = 0
[   78s] + set +f
[   78s] + case $tizen_llvm_kind:$tizen_llvm_release in
[   78s] + case $tizen_llvm_kind in
[   78s] + TIZEN_LLVM_RESULT='-Wl,-z,relro,--as-needed -Wl,--gc-sections'
[   78s] + LDFLAGS='-Wl,-z,relro,--as-needed -Wl,--gc-sections'
[   78s] + printf 'TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[%s] CXXFLAGS=[%s] LDFLAGS=[%s]\n' '-O2 -fstack-protector-strong -fno-omit-frame-pointer' '-O2 -fstack-protector-strong -fno-omit-frame-pointer' ''
[   78s] TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] CXXFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] LDFLAGS=[]
[   78s] + printf 'TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[%s] CXXFLAGS=[%s] LDFLAGS=[%s]\n' '-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4' '-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4' ''
[   78s] TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] CXXFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] LDFLAGS=[]
[   78s] + tizen_llvm_report_warnings '' '' ''
[   78s] + test -n ''
[   78s] + export CFLAGS CXXFLAGS LDFLAGS
[   78s] + MLGO_AOT_DIR=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets
[   78s] + MLGO_BUILD_DIR=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build
[   78s] + MLGO_RUNTIME_OBJECTS='/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/xla_compiled_cpu_function.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/cpu_function_runtime.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/custom_call_status.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/executable_run_options.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/runtime_single_threaded_matmul_f32.cc.o'
[   78s] + MLGO_REQUIRED_RUNTIME_OBJECTS='xla_compiled_cpu_function.cc.o cpu_function_runtime.cc.o custom_call_status.cc.o executable_run_options.cc.o runtime_single_threaded_matmul_f32.cc.o'
[   78s] + mkdir -p build
[   78s] + cd build
[   78s] + python3 -B /home/abuild/rpmbuild/SOURCES/clang-bolt-helper.py pgo-prepare /home/abuild/rpmbuild/SOURCES/llvm-profiles.manifest D /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/pgo-profiles /home/abuild/rpmbuild/SOURCES/clang-pgo.profdata.xz
[   78s] BOLT_DISK_DIAGNOSIS {"cause": "unknown", "step": "pgo-prepare", "free_bytes": 392246706176, "used_bytes": 0, "reason": "日志不可用，无法判定原因"}
[   78s] BOLT_GATE_FAILED: missing profile mapping: ('D', True, False)
[   78s] + exit 1
[   78s] error: Bad exit status from /var/tmp/rpm-tmp.JKcBOi (%build)
[   78s] 
[   78s] 
[   78s] RPM build errors:
[   78s]     Bad exit status from /var/tmp/rpm-tmp.JKcBOi (%build)
[   78s] 
[   78s] 0f88ab419dab failed "build llvm.spec" at Wed Nov 25 18:42:24 UTC 2026.
[   78s]
```

[失败包完整日志](../../tools/bolt/results/task164/D-x86_64.buildlog.txt) · [T x86_64 完整日志](../../tools/bolt/results/task164/T-x86_64.buildlog.txt) · [主构建 T 日志](../../tools/bolt/results/task164/1240313-full-log.txt) · [主构建 D 日志](../../tools/bolt/results/task164/1240314-full-log.txt)
