# 169 · PS7 与 PGO+BOLT 的 QB 核对

**PS7 两个项目的三架构 LLVM 包构建通过。PGO+BOLT 两个项目的 x86_64 均在 %build 参数解析处失败，其余两架构的 LLVM 包构建通过。**

| QB | 项目 | 候选 | x86_64 | aarch64 | armv7l | LLVM worker 区间（PST） | QB 概览状态和起止 |
|---|---|---|---|---|---|---|---|
| [1241534](https://quickbuild.tizen.org/build/1241534) | Tizen-Base-Dev | PS7 | PASS | PASS | PASS | 11-26 03:49:51 → 11-26 05:26:46 | 需登录 |
| [1241535](https://quickbuild.tizen.org/build/1241535) | Tizen-Base-Toolchain | PS7 | PASS | PASS | PASS | 11-26 03:55:59 → 11-26 06:29:43 | 需登录 |
| [1241584](https://quickbuild.tizen.org/build/1241584) | Tizen-Base-Dev | PGO+BOLT | FAIL | PASS | PASS | 11-26 04:33:39 → 11-26 08:30:52 | 需登录 |
| [1241585](https://quickbuild.tizen.org/build/1241585) | Tizen-Base-Toolchain | PGO+BOLT | FAIL | PASS | PASS | 11-26 04:39:15 → 11-26 08:22:43 | 需登录 |

LLVM worker 区间取三架构包日志最早的开始和最晚的结束。原始 worker 时钟为 UTC。
QB 概览需要登录，匿名 REST 只读请求返回 HTTP 401。表中标注了未核实的构建级起止与总体状态。

- PS7 `sandbox/lhmax2025/llvm-361624-ps7-20261126` → `de305f2c4de2721c7aeb5a677cd0ee32c3be505c`。
- PGO+BOLT `sandbox/lhmax2025/llvm-pgo-bolt-20261125` → `4080f55abfc7c48097c9bd7fdbf9334e37c661af`。

四份发布 manifest 含对应提交，Gerrit 只读查询确认两个分支头。 [构建与逐架构时间](../../tools/bolt/results/task169/build-records.json) · [Gerrit 原文](../../tools/bolt/results/task169/gerrit-refs.txt)

## PS7 成品 RPM

| QB | 架构 | 目标归属 | RPM shebang | 日志后置检查 | 未打包错误 | clang Requires |
|---|---|---|---:|---:|---|---|
| 1241534 | x86_64 | [PASS](../../tools/bolt/results/task169/1241534/x86_64/audit.json) | 6/6 | 6/6 | 无 | 无 Python 条目；仅 llvm release 变更 |
| 1241534 | aarch64 | [PASS](../../tools/bolt/results/task169/1241534/aarch64/audit.json) | 6/6 | 6/6 | 无 | 无 Python 条目；无 154-B 同架构对照 |
| 1241534 | armv7l | [PASS](../../tools/bolt/results/task169/1241534/armv7l/audit.json) | 6/6 | 6/6 | 无 | 无 Python 条目；无 154-B 同架构对照 |
| 1241535 | x86_64 | [PASS](../../tools/bolt/results/task169/1241535/x86_64/audit.json) | 6/6 | 6/6 | 无 | 无 Python 条目；仅 llvm release 变更 |
| 1241535 | aarch64 | [PASS](../../tools/bolt/results/task169/1241535/aarch64/audit.json) | 6/6 | 6/6 | 无 | 无 Python 条目；无 154-B 同架构对照 |
| 1241535 | armv7l | [PASS](../../tools/bolt/results/task169/1241535/armv7l/audit.json) | 6/6 | 6/6 | 无 | 无 Python 条目；无 154-B 同架构对照 |

18 个 RPM 的 VCS 字段均指向 PS7。scan-build 的资源和手册页在 clang，scan-view 的数据在 llvm。libscanbuild、libear 在 clang。llvm-devel 未保留这些条目。两个 x86_64 的 Requires 原始差异均为 llvm 从 22.1.8-1 锁定改成 22.1.8-2.1。 [六套审计](../../tools/bolt/results/task169/ps7-audit.json) · [18 个 RPM 的下载地址和 SHA256](../../tools/bolt/results/task169/ps7-downloads.json)

## PGO+BOLT x86_64 的共同失败

两个日志首先在 %build 的 pgo-prepare 参数解析处报错，CMake 尚未开始。spec 把可选宏紧贴带引号的 profdata 位置参数。RPM 展开和 shell 实际命令均将 .xz 和 --bolt-profile 合为一个参数，所以下一个 fdata 被 argparse 拒绝。166 的静态验收为 helper 单独构造了传参列表，而 spec 展开核对只检查子串出现，漏掉了 shell 实际分词。

1240310 在完成参数解析后报 D 映射缺失。本次 Base-Dev 在解析阶段已退出。新候选 manifest 的两个键仍只覆盖 T。1240310 的错误原文如下。

> [   78s] BOLT_GATE_FAILED: missing profile mapping: ('D', True, False)

Toolchain 未到 PGO Ninja、BOLT（含 -stale-threshold=5）、运行时依赖门禁或归档转换阶段。没有 ARCHIVE_MEMBER_RETRY 行。本次未产出 x86_64 成品，ELF、V3 身份比较和 V3q 补测均为 SKIPPED。
 [spec、RPM 展开和实参分词](../../tools/bolt/results/task169/pgo-bolt-argument-audit.json)

### 1241584 首个实际错误原文

第 684 行。以下保留第 644–693 行，前 40 行及错误后至日志结束。

```text
[   71s] + case $tizen_llvm_release in
[   71s] + tizen_llvm_debug_sequence=
[   71s] + TIZEN_LLVM_UNREVIEWED=
[   71s] + tizen_llvm_arch=
[   71s] + tizen_llvm_debug_head=
[   71s] + tizen_llvm_debug_tail=
[   71s] + TIZEN_LLVM_NORMALIZED=
[   71s] + TIZEN_LLVM_DROPPED=
[   71s] + tizen_llvm_ifs_set=x
[   71s] + tizen_llvm_saved_ifs=' 	
[   71s] '
[   71s] + unset IFS
[   71s] + case $- in
[   71s] + tizen_llvm_glob_off=0
[   71s] + set -f
[   71s] + test x = x
[   71s] + IFS=' 	
[   71s] '
[   71s] + test 0 = 0
[   71s] + set +f
[   71s] + case $tizen_llvm_kind:$tizen_llvm_release in
[   71s] + case $tizen_llvm_kind in
[   71s] + TIZEN_LLVM_RESULT='-Wl,-z,relro,--as-needed -Wl,--gc-sections'
[   71s] + LDFLAGS='-Wl,-z,relro,--as-needed -Wl,--gc-sections'
[   71s] + printf 'TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[%s] CXXFLAGS=[%s] LDFLAGS=[%s]\n' '-O2 -fstack-protector-strong -fno-omit-frame-pointer' '-O2 -fstack-protector-strong -fno-omit-frame-pointer' ''
[   71s] TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] CXXFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] LDFLAGS=[]
[   71s] + printf 'TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[%s] CXXFLAGS=[%s] LDFLAGS=[%s]\n' '-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4' '-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4' ''
[   71s] TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] CXXFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] LDFLAGS=[]
[   71s] + tizen_llvm_report_warnings '' '' ''
[   71s] + test -n ''
[   71s] + export CFLAGS CXXFLAGS LDFLAGS
[   71s] + MLGO_AOT_DIR=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets
[   71s] + MLGO_BUILD_DIR=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build
[   71s] + MLGO_RUNTIME_OBJECTS='/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/xla_compiled_cpu_function.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/cpu_function_runtime.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/custom_call_status.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/executable_run_options.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/runtime_single_threaded_matmul_f32.cc.o'
[   71s] + MLGO_REQUIRED_RUNTIME_OBJECTS='xla_compiled_cpu_function.cc.o cpu_function_runtime.cc.o custom_call_status.cc.o executable_run_options.cc.o runtime_single_threaded_matmul_f32.cc.o'
[   71s] + mkdir -p build
[   71s] + cd build
[   71s] + python3 -B /home/abuild/rpmbuild/SOURCES/clang-bolt-helper.py pgo-prepare /home/abuild/rpmbuild/SOURCES/llvm-profiles.manifest D /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/pgo-profiles /home/abuild/rpmbuild/SOURCES/T-clang.profdata.xz--bolt-profile /home/abuild/rpmbuild/SOURCES/T-clang.fdata.xz
[   71s] usage: clang-bolt-helper.py [-h]
[   71s]                             {preflight,certified,security,tool-prepare,tool-verify,tool-plan,pipeline,strip-all,cache-release,cache-copy,package-compare,unpack,replay,rewrite,tiny,installed-baseline,snapshot,compare-root,install,post,pgo-prepare,pgo-check-ninja,pgo-post,disk-report,disk-diagnose,run-step} ...
[   71s] clang-bolt-helper.py: error: unrecognized arguments: /home/abuild/rpmbuild/SOURCES/T-clang.fdata.xz
[   71s] + exit 1
[   71s] error: Bad exit status from /var/tmp/rpm-tmp.oLwA6m (%build)
[   71s] 
[   71s] 
[   71s] RPM build errors:
[   71s]     Bad exit status from /var/tmp/rpm-tmp.oLwA6m (%build)
[   71s] 
[   71s] 062be1f938ad failed "build llvm.spec" at Thu Nov 26 16:30:52 UTC 2026.
[   71s] 
```

[上下文原文](../../tools/bolt/results/task169/1241584/x86_64-first-error-40x40.txt) · [完整包日志](../../tools/bolt/results/task169/1241584/x86_64.buildlog.txt.gz)

### 1241585 首个实际错误原文

第 719 行。以下保留第 679–728 行，前 40 行及错误后至日志结束。

```text
[   32s] + TIZEN_LLVM_NORMALIZED=
[   32s] + TIZEN_LLVM_DROPPED=
[   32s] + tizen_llvm_ifs_set=x
[   32s] + tizen_llvm_saved_ifs=' 	
[   32s] '
[   32s] + unset IFS
[   32s] + case $- in
[   32s] + tizen_llvm_glob_off=0
[   32s] + set -f
[   32s] + for tizen_llvm_token in '$tizen_llvm_input'
[   32s] + case $tizen_llvm_token in
[   32s] + case $tizen_llvm_kind:$tizen_llvm_token in
[   32s] + for tizen_llvm_token in '$tizen_llvm_input'
[   32s] + case $tizen_llvm_token in
[   32s] + case $tizen_llvm_kind:$tizen_llvm_token in
[   32s] + test x = x
[   32s] + IFS=' 	
[   32s] '
[   32s] + test 0 = 0
[   32s] + set +f
[   32s] + case $tizen_llvm_kind:$tizen_llvm_release in
[   32s] + case $tizen_llvm_kind in
[   32s] + TIZEN_LLVM_RESULT='-Wl,-z,relro,--as-needed -Wl,--gc-sections'
[   32s] + LDFLAGS='-Wl,-z,relro,--as-needed -Wl,--gc-sections'
[   32s] + printf 'TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[%s] CXXFLAGS=[%s] LDFLAGS=[%s]\n' '-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer' '-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer' ''
[   32s] TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] CXXFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] LDFLAGS=[]
[   32s] + printf 'TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[%s] CXXFLAGS=[%s] LDFLAGS=[%s]\n' '' '' ''
[   32s] TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[] CXXFLAGS=[] LDFLAGS=[]
[   32s] + tizen_llvm_report_warnings '' '' ''
[   32s] + test -n ''
[   32s] + export CFLAGS CXXFLAGS LDFLAGS
[   32s] + MLGO_AOT_DIR=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets
[   32s] + MLGO_BUILD_DIR=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build
[   32s] + MLGO_RUNTIME_OBJECTS='/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/xla_compiled_cpu_function.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/cpu_function_runtime.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/custom_call_status.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/executable_run_options.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/runtime_single_threaded_matmul_f32.cc.o'
[   32s] + MLGO_REQUIRED_RUNTIME_OBJECTS='xla_compiled_cpu_function.cc.o cpu_function_runtime.cc.o custom_call_status.cc.o executable_run_options.cc.o runtime_single_threaded_matmul_f32.cc.o'
[   32s] + mkdir -p build
[   32s] + cd build
[   32s] + python3 -B /home/abuild/rpmbuild/SOURCES/clang-bolt-helper.py pgo-prepare /home/abuild/rpmbuild/SOURCES/llvm-profiles.manifest T /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/pgo-profiles /home/abuild/rpmbuild/SOURCES/T-clang.profdata.xz--bolt-profile /home/abuild/rpmbuild/SOURCES/T-clang.fdata.xz
[   32s] usage: clang-bolt-helper.py [-h]
[   32s]                             {preflight,certified,security,tool-prepare,tool-verify,tool-plan,pipeline,strip-all,cache-release,cache-copy,package-compare,unpack,replay,rewrite,tiny,installed-baseline,snapshot,compare-root,install,post,pgo-prepare,pgo-check-ninja,pgo-post,disk-report,disk-diagnose,run-step} ...
[   32s] clang-bolt-helper.py: error: unrecognized arguments: /home/abuild/rpmbuild/SOURCES/T-clang.fdata.xz
[   32s] + exit 1
[   32s] error: Bad exit status from /var/tmp/rpm-tmp.xlAlfF (%build)
[   32s] 
[   32s] 
[   32s] RPM build errors:
[   32s]     Bad exit status from /var/tmp/rpm-tmp.xlAlfF (%build)
[   32s] 
[   32s] 6a87a2b5ee05 failed "build llvm.spec" at Thu Nov 26 16:22:43 UTC 2026.
[   32s] 
```

[上下文原文](../../tools/bolt/results/task169/1241585/x86_64-first-error-40x40.txt) · [完整包日志](../../tools/bolt/results/task169/1241585/x86_64.buildlog.txt.gz)
