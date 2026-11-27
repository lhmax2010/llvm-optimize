# 171 · PGO+BOLT Toolchain QB 核对

[QB 1242771](https://quickbuild.tizen.org/build/1242771) · Tizen-Base-Toolchain · `sandbox/lhmax2025/llvm-pgo-bolt-20261127-2` · `a752ddf8e826ab70bffe2354619a7f9977513764`。 [分支头原文](../../tools/bolt/results/task171/gerrit-ref.txt)

QB 概览状态为 **Running**，界面开始时间 2026-11-27 09:37:03，最近一次界面时长 4 hours 11 minutes 58 seconds。
 [构建身份](../../tools/bolt/results/task171/build.json) · [QB 概览快照](../../tools/bolt/results/task171/qb-overview.json)

最后回读 QB 概览时遇到连接或授权阻塞，终态以发布的逐架构包日志核对。

| 架构 | LLVM 包结论 | 开始（worker 原文） | 结束（worker 原文） | 日志 |
|---|---|---|---|---|
| x86_64 | FAIL | Fri Nov 27 13:43:50 UTC 2026. | Fri Nov 27 14:58:25 UTC 2026. | [原文](../../tools/bolt/results/task171/x86_64.buildlog.txt.gz) |
| aarch64 | PASS | Fri Nov 27 09:54:39 UTC 2026. | Fri Nov 27 11:12:36 UTC 2026. | [原文](../../tools/bolt/results/task171/aarch64.buildlog.txt.gz) |
| armv7l | PASS | Fri Nov 27 09:54:39 UTC 2026. | Fri Nov 27 11:02:49 UTC 2026. | [原文](../../tools/bolt/results/task171/armv7l.buildlog.txt.gz) |

[发布源码清单](../../tools/bolt/results/task171/standard-manifest.xml) · [逐架构日志回执](../../tools/bolt/results/task171/package-log-audit.json)

## x86_64 首个实际错误

第 12141 行，阶段 %install，编译、配置或链接报错，原始命令和诊断见上下文。 原文第 12101–12181 行。 [上下文](../../tools/bolt/results/task171/x86_64-first-error-40x40.txt)

```text
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.dd-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.dyndd-x86_64.so
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.tsan-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.tsan_cxx-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.tsan-x86_64.so
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.tsan-x86_64.a.syms
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.tsan_cxx-x86_64.a.syms
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.tysan-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.safestack-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.cfi-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.cfi_diag-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/share/cfi_ignorelist.txt
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.scudo_standalone-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.scudo_standalone_cxx-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.scudo_standalone-x86_64.so
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.ubsan_minimal-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.ubsan_minimal-x86_64.so
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.ubsan_minimal-x86_64.a.syms
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.gwp_asan-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.nsan-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.nsan-x86_64.so
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.profile-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.ctx_profile-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.xray-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.xray-fdr-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.xray-basic-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.xray-profiling-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.xray-dso-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.fuzzer-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.fuzzer_no_main-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.fuzzer_interceptors-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.memprof-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.memprof_cxx-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.memprof-preinit-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.memprof-x86_64.so
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.memprof_cxx-x86_64.a.syms
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/libclang_rt.memprof-x86_64.a.syms
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/lib/linux/liborc_rt-x86_64.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/lib64/libomp.so
[ 4218s] failed to create symbolic link 'libgomp.so' because existing path cannot be removed: Permission denied
[ 4218s] CMake Error: failed to create symbolic link 'libiomp5.so': Permission denied
[ 4218s] failed to create symbolic link 'libgomp.so.1' because existing path cannot be removed: Permission denied
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/include/omp.h
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/include/ompx.h
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/include/omp-tools.h
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/include/ompt.h
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/lib64/libarcher.so
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/lib64/libarcher_static.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/lib64/cmake/openmp/FindOpenMPTarget.cmake
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/../lib64/clang/22/include/ompt-multiplex.h
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/lib64/libompd.so
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/share/gdb/python//ompd
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/share/gdb/python//ompd/ompd_callbacks.py
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/share/gdb/python//ompd/ompd_handles.py
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/share/gdb/python//ompd/ompd_address_space.py
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/share/gdb/python//ompd/ompdModule.so
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/share/gdb/python//ompd/__init__.py
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/share/gdb/python//ompd/frame_filter.py
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/share/gdb/python//ompd/ompd.py
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/lib64/libLTO.so.22.1
[ 4218s] -- Set non-toolchain portion of runtime path of "/home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/lib64/libLTO.so.22.1" to "$ORIGIN/../lib64"
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/lib64/libLTO.so
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/include/llvm-c/lto.h
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/lib64/LLVMgold.so
[ 4218s] -- Set non-toolchain portion of runtime path of "/home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/lib64/LLVMgold.so" to "$ORIGIN/../lib64"
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/llvm-ar
[ 4218s] -- Set non-toolchain portion of runtime path of "/home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/llvm-ar" to "$ORIGIN/../lib64"
[ 4218s] -- Creating llvm-ranlib
[ 4218s] -- Creating llvm-lib
[ 4218s] -- Creating llvm-dlltool
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/llvm-config
[ 4218s] -- Set non-toolchain portion of runtime path of "/home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/llvm-config" to "$ORIGIN/../lib64"
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/llvm-ctxprof-util
[ 4218s] -- Set non-toolchain portion of runtime path of "/home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/llvm-ctxprof-util" to "$ORIGIN/../lib64"
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/llvm-lto
[ 4218s] -- Set non-toolchain portion of runtime path of "/home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/llvm-lto" to "$ORIGIN/../lib64"
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/llvm-profdata
[ 4218s] -- Set non-toolchain portion of runtime path of "/home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/llvm-profdata" to "$ORIGIN/../lib64"
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/lib64/liblldCommon.a
[ 4218s] -- Installing: /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/lld
[ 4218s] -- Set non-toolchain portion of runtime path of "/home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-2.1.x86_64/usr/bin/lld" to "$ORIGIN/../lib64"
```

## x86_64 门禁

[日志门禁行原文](../../tools/bolt/results/task171/x86_64-gates.txt)

- `PGO_NINJA_CHECK {"edges": 25940, "compile": 6236, "profile_use": 5357, "runtime_compile": 879, "violation_count": 0, "violations": []}`
- `PGO_MATCH UNKNOWN method-not-qualified`
- `PGO_RUNTIME_CHECK` 未在日志出现。
- `BOLT_PIPELINE_PASS` 未在日志出现。
- `BOLT_REAL_GATE_PASS {"work": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt/prestrip-real", "cases": 8, "seconds": 3.654276948000188}`
- `BOLT_POST_GATE_PASS` 未在日志出现。

- BOLT 日志中的阈值参数 未记录。
- ARCHIVE_MEMBER_RETRY 共 0 行。

没有本次 x86_64 成品，ELF、clang 身份比较和 V3q 补测均跳过。
