# 132：PGO/BOLT 成对离线 profile 生成

**阶段结果：G1 STOP, G2 SKIPPED, G3 SKIPPED, G4 SKIPPED, G5 SKIPPED, G6 SKIPPED, G7 SKIPPED, G8 SKIPPED。**

| 步骤 | 结论 | 档位 | MemoryMax B | 开始 | 结束 | 等待 s | 执行 s | cgroup peak B | MemAvailable B | /home 可用 B | 依据 |
|---|---|---|---:|---|---|---:|---:|---:|---:|---:|---|
| G1 | STOP | standard | 8672698368 | 2026-11-18T08:55:09-08:00 | 2026-11-18T09:56:56-08:00 | 0.0 | 3707.223 | 8672698368 | 24326889472 | 412757606400 | 134 skill exited 1: {'status': 'STOP', 'project': 'T', 'stages': [{'name': 'instrumented-build', 'status': 'STOP', 'attempt': '/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G-profiles/instrumented-build-1795020912008271908'}], 'started_at': '2026-11-18T16:55:09+00:00', 'admission': [{'at': '2026-11-18T16:55:09+00:00', 'memory': 24307625984, 'disk': {'/home': 412757479424, '/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G-profiles': 412757479424}}], 'tier': 'managed', 'reason': 'command failed (1); see /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G-profiles/instrumented-build-1795020912008271908/build-0.txt', 'ended_at': '2026-11-18T17:56:56+00:00'} |
| G2 | SKIPPED | — | — | — | — | 0 | — | UNKNOWN | 24269447168 | 385664327680 | PGO prerequisite did not pass |
| G3 | SKIPPED | — | — | — | — | 0 | — | UNKNOWN | 24269443072 | 385664299008 | PGO prerequisite did not pass |
| G4 | SKIPPED | — | — | — | — | 0 | — | UNKNOWN | 24265154560 | 385664249856 | PGO prerequisite did not pass |
| G5 | SKIPPED | — | — | — | — | 0 | — | UNKNOWN | 24253177856 | 385664200704 | PGO prerequisite did not pass |
| G6 | SKIPPED | — | — | — | — | 0 | — | UNKNOWN | 24244826112 | 385664151552 | PGO prerequisite did not pass |
| G7 | SKIPPED | — | — | — | — | 0 | — | UNKNOWN | 24247795712 | 385664102400 | PGO prerequisite did not pass |
| G8 | SKIPPED | — | — | — | — | 0 | — | UNKNOWN | 24262656000 | 385664053248 | PGO prerequisite did not pass |

阶段依次对应 134 号技能：G1 插桩构建，G2 IR 训练，G3 合并 profdata，G4 PGO 构建及运行时检查，G5 BOLT 工具与重链，G6 BOLT 插桩、训练、合并，G7 BOLT 匹配，G8 压缩与清单。磁盘预算采用 131 号 125.626 GiB 减 30 GiB 余量，即 95.626 GiB。G5、G8 未测峰值，准入预算用 131 已测最大阶段峰值作为保守上界。其余阶段采用事件记录中的实测来源。

G1 STOP 原文

~~~text
Traceback (most recent call last):
  File "/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/worker.py", line 149, in <module>
    out=generate(A,D,W,B,TASK,TIER,JOBS,MEM,CPU)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/pgosteps.py", line 271, in generate
    raise RuntimeError(f"134 skill exited {proc.returncode}: {err}")
RuntimeError: 134 skill exited 1: {'status': 'STOP', 'project': 'T', 'stages': [{'name': 'instrumented-build', 'status': 'STOP', 'attempt': '/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G-profiles/instrumented-build-1795020912008271908'}], 'started_at': '2026-11-18T16:55:09+00:00', 'admission': [{'at': '2026-11-18T16:55:09+00:00', 'memory': 24307625984, 'disk': {'/home': 412757479424, '/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G-profiles': 412757479424}}], 'tier': 'managed', 'reason': 'command failed (1); see /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G-profiles/instrumented-build-1795020912008271908/build-0.txt', 'ended_at': '2026-11-18T17:56:56+00:00'}
~~~

G1 资源原文（VmHWM 为采样值）

~~~json
{
  "memory.peak": "8672698368",
  "VmHWM_sample": {
    "bytes": 8058806272,
    "pid": 2173033,
    "argv": "/usr/bin/ld.lld --hash-style=gnu --eh-frame-hdr -m elf_x86_64 -pie -dynamic-linker /lib64/ld-linux-x86-64.so.2 -o bin/clang-22 /usr/bin/../lib64/gcc/x86_64-tizen-linux-gnu/14.2.0/../../../../lib64/Scrt1.o /usr/bin/../lib64/gcc/x86_64-tizen-linux-gnu/14.2.0/../../../../lib64/crti.o /usr/bin/../lib64/gcc/x86_64-tizen-linux-gnu/14.2.0/crtbeginS.o -L/usr/bin/../lib64/gcc/x86_64-tizen-linux-gnu/14.2.0 -L/usr/bin/../lib64/gcc/x86_64-tizen-linux-gnu/14.2.0/../../../../lib64 -L/lib/../lib64 -L/usr/lib64 -L/usr/bin/../lib64/gcc/x86_64-tizen-linux-gnu/14.2.0/../../../../x86_64-tizen-linux-gnu/lib -L/lib -L/usr/lib -plugin-opt=mcpu=x86-64 -plugin-opt=O3 -plugin-opt=thinlto -plugin-opt=-function-sections=1 -plugin-opt=-data-sections=1 --gc-sections --color-diagnostics --thinlto-cache-dir=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache --export-dynamic --dependency-file=tools/clang/tools/driver/CMakeFiles/clang.dir/link.d tools/clang/tools/driver/CMakeFiles/clang.dir/driver.cpp.o tools/clang/tools/driver/CMakeFiles/clang.dir/cc1_main.cpp.o tools/clang/tools/driver/CMakeFiles/clang.dir/cc1as_main.cpp.o tools/clang/tools/driver/CMakeFiles/clang.dir/cc1gen_reproducer_main.cpp.o tools/clang/tools/driver/CMakeFiles/clang.dir/clang-driver.cpp.o -rpath $ORIGIN/../lib64:/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64: lib64/libLLVMX86CodeGen.a lib64/libLLVMX86AsmParser.a lib64/libLLVMX86Desc.a lib64/libLLVMX86Disassembler.a lib64/libLLVMX86Info.a lib64/libLLVMARMCodeGen.a lib64/libLLVMARMAsmParser.a lib64/libLLVMARMDesc.a lib64/libLLVMARMDisassembler.a lib64/libLLVMARMInfo.a lib64/libLLVMARMUtils.a lib64/libLLVMAArch64CodeGen.a lib64/libLLVMAArch64AsmParser.a lib64/libLLVMAArch64Desc.a lib64/libLLVMAArch64Disassembler.a lib64/libLLVMAArch64Info.a lib64/libLLVMAArch64Utils.a lib64/libLLVMBPFCodeGen.a lib64/libLLVMBPFAsmParser.a lib64/libLLVMBPFDesc.a lib64/libLLVMBPFDisassembler.a lib64/libLLVMBPFInfo.a lib64/libLLVMAnalysis.a lib64/libLLVMCodeGen.a lib64/libLLVMCore.a lib64/libLLVMipo.a lib64/libLLVMAggressiveInstCombine.a lib64/libLLVMInstCombine.a lib64/libLLVMInstrumentation.a lib64/libLLVMMC.a lib64/libLLVMMCParser.a lib64/libLLVMObjCARCOpts.a lib64/libLLVMOption.a lib64/libLLVMScalarOpts.a lib64/libLLVMSupport.a lib64/libLLVMTargetParser.a lib64/libLLVMTransformUtils.a lib64/libLLVMVectorize.a lib64/libclangBasic.a lib64/libclangCodeGen.a lib64/libclangDriver.a lib64/libclangFrontend.a lib64/libclangFrontendTool.a lib64/libclangOptions.a lib64/libclangSerialization.a lib64/libLLVMAsmPrinter.a lib64/libLLVMMCDisassembler.a lib64/libLLVMCoverage.a lib64/libLLVMFrontendDriver.a lib64/libLLVMLTO.a lib64/libLLVMPasses.a lib64/libLLVMCFGuard.a lib64/libLLVMGlobalISel.a lib64/libLLVMSelectionDAG.a lib64/libLLVMCodeGenTypes.a lib64/libLLVMIRPrinter.a lib64/libLLVMTarget.a lib64/libLLVMCoroutines.a lib64/libLLVMSandboxIR.a lib64/libLLVMHipStdPar.a lib64/libLLVMCGData.a lib64/libLLVMBitWriter.a lib64/libLLVMLinker.a lib64/libLLVMExtensions.a lib64/libclangExtractAPI.a lib64/libclangInstallAPI.a lib64/libLLVMTextAPIBinaryReader.a lib64/libclangRewriteFrontend.a lib64/libclangStaticAnalyzerFrontend.a lib64/libclangStaticAnalyzerCheckers.a lib64/libclangStaticAnalyzerCore.a lib64/libclangCrossTU.a lib64/libLLVMWindowsDriver.a lib64/libclangIndex.a lib64/libLLVMPlugins.a lib64/libclangParse.a lib64/libclangSema.a lib64/libclangAPINotes.a lib64/libclangEdit.a lib64/libclangAnalysisLifetimeSafety.a lib64/libclangAnalysis.a lib64/libclangASTMatchers.a lib64/libclangAST.a lib64/libclangSupport.a lib64/libclangFormat.a lib64/libclangToolingInclusions.a lib64/libclangToolingCore.a lib64/libclangRewrite.a lib64/libclangLex.a lib64/libLLVMFrontendOpenMP.a lib64/libLLVMFrontendOffloading.a lib64/libLLVMObjectYAML.a lib64/libLLVMFrontendAtomic.a lib64/libLLVMProfileData.a lib64/libLLVMSymbolize.a lib64/libLLVMDebugInfoGSYM.a lib64/libLLVMDebugInfoDWARF.a lib64/libLLVMDebugInfoPDB.a lib64/libLLVMDebugInfoCodeView.a lib64/libLLVMDebugInfoMSF.a lib64/libLLVMDebugInfoBTF.a lib64/libLLVMObject.a lib64/libLLVMDebugInfoDWARFLowLevel.a lib64/libLLVMIRReader.a lib64/libLLVMBitReader.a lib64/libLLVMAsmParser.a lib64/libLLVMTextAPI.a lib64/libLLVMFrontendHLSL.a lib64/libLLVMBinaryFormat.a lib64/libLLVMRemarks.a lib64/libLLVMBitstreamReader.a lib64/libLLVMFrontendDirective.a lib64/libLLVMDemangle.a -lrt -ldl -lm /usr/lib64/libz.so -rpath-link /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64 -u__llvm_profile_runtime /usr/lib64/clang/22/lib/linux/libclang_rt.profile-x86_64.a -lstdc++ -lm -lgcc_s -lgcc -lc -lgcc_s -lgcc /usr/bin/../lib64/gcc/x86_64-tizen-linux-gnu/14.2.0/crtendS.o /usr/bin/../lib64/gcc/x86_64-tizen-linux-gnu/14.2.0/../../../../lib64/crtn.o"
  },
  "memory.events": "low 0\nhigh 0\nmax 12058\noom 0\noom_kill 0\noom_group_kill 0",
  "memory.stat": "anon 9846784\nfile 8063770624",
  "memory.max": "8672698368",
  "memory.swap.peak": "0"
}
~~~


告警统计：instrumented-build 826 条。
首条 /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G-profiles/instrumented-build-1795020912008271908/build-0.txt:3170
~~~text
LLVM Profile Warning: Unable to track new values: Running out of static counters.  Consider using option -mllvm -vp-counters-per-site=<n> to allocate more value profile counters at compile time.
~~~

若对应阶段未执行，时长、告警、profile 身份、BOLT 计数和运行时检查记为未取得。

134 号配置的主机路径、23 项文件身份和对应阶段命令记录于本地 G-config。技能修正仅为目标工具单独配置运行库路径。G4 的 BUILD 在 G5 重链取证后清理，它在两阶段间是必要输入。

## 留在本机的证据

| 步骤 | 文件 | 字节 | SHA256 |
|---|---|---:|---|
| G1 | /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G-profiles/instrumented-build-1795020912008271908/build-0.txt | 710189 | 557c5fbc9f96f70cd4fd1a84b79b4a4055b30fa146a36fab13737040ec6bfacb |
| G1 | /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/build-cleanup.json | 190 | 1a9cfd8afaab1c719131bbc3f74d7af1775b205ee83fbd553f276afac118fdd0 |
| G1 | /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/instrumented-recipe.diff | 518 | a193a0e3a383c13f7b07f89deeb2a63ff2b28ac04d4f8b36e550ac231c51236a |
| G1 | /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/prep.log | 22500 | d994642ff226e56a611eaf19c156d41a459ab8ce7689a1f589ac6335c83fc469 |
| G1 | /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/service.log | 2811 | b852a19bca2873848c327ca5d33fa36b728d48029c85034b7ef20b85945047e0 |

本地结果目录 /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118。全部步骤状态见[总 JSON](../../tools/bolt/results/task133-n/summary.json)。看门狗触发：否。
