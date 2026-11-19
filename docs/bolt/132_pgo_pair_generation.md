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


## G1 恢复预检：STOP

2026-11-18T10:39:43-08:00，原 G1 的 Ninja 完成且记录了 `PGO_INSTRUMENTED_BUILD_PASS`。首个停止是清理 BUILD 时目标工具拒绝选项，原文如下。

~~~text
rm: Unknown option 'one-file-system' (see "rm --help")
~~~

按一次准备修正机会拟改用 Python 的目录清理，并在续跑前测试已保留的插桩 clang。候选恢复改动的技能单测 41/41 通过。运行 `clang-22 --version` 的预检实际失败如下。

~~~text
subprocess.CalledProcessError: Command '['/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G-config/ir-artifacts/clang-22', '--version']' died with <Signals.SIGSEGV: 11>.
~~~

ELF 请求主机的 `/lib64/ld-linux-x86-64.so.2`。预检的 `LD_LIBRARY_PATH` 同时指向 Tizen 根的 `usr/lib64` 和 `lib64`，程序依赖包含 `libc.so.6` 和 `ld-linux-x86-64.so.2`。这是可见的运行环境差异。SIGSEGV 本身的确切原因未做二次运行验证。未启动恢复队列，未重编译或重新执行插桩 clang，G2–G8 仍为 SKIPPED。首次运行时 G1 内存达到限制，有 12,058 次 max 事件，OOM 与 OOM kill 都为 0。

已保留 BUILD `/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD`，清理前实测 20,000,354,304 B。保留的插桩 clang `/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G-config/ir-artifacts/clang-22` 为 1,466,952,360 B，SHA256 `381789a9f576f9e6e7affe25ee568e303da6816ba28e64c86135d29c55ea06a7`。它是编译产物，训练和 profile 生成均尚未执行。未完成现场恢复验证的技能改动作为本地 diff 保存，证据分支保留先前已测试并推送的目标工具独立运行库配置修正。原始编排报告和各步 JSON 保留。[恢复预检 JSON](../../tools/bolt/results/task133-n/G1-recovery.json)


## 138-N 续跑

**G2 PASS, G3 PASS, G4 SKIPPED, G5 SKIPPED, G6 SKIPPED, G7 SKIPPED, G8 SKIPPED。**

单元 llvm-opt-138n-20261119.service，截止 2026-11-20T08:30:00+08:00。启动 MemAvailable 20.22 GiB，/home 可用 352.98 GiB。看门狗触发：否。[逐步 JSON](../../tools/bolt/results/task138-n-20261119/summary.json)

| 步骤 | 结论 | 档位 | MemoryMax GiB | 并行 | 开始 | 结束 | 等待秒 | 执行秒 | 内存峰值 B | 准入 MemAvailable GiB | 准入 /home GiB | 原因 |
|---|---|---|---:|---:|---|---|---:|---:|---:|---:|---:|---|
| G2 | PASS | dynamic | 1.66 | 1 | 2026-11-19T00:54:06-08:00 | 2026-11-19T00:58:06-08:00 | 0.0 | 239.723 | 1778184192 | 18.88 | 352.97 | — |
| G3 | PASS | dynamic | 2.04 | 1 | 2026-11-19T00:58:08-08:00 | 2026-11-19T00:58:22-08:00 | 0.0 | 13.129 | 2189705216 | 18.92 | 370.78 | — |
| G4 | SKIPPED | — | — | — | — | — | 1800.002 | — | — | 19.00 | 370.73 | MemAvailable minus 6 GiB below stage floor |
| G5 | SKIPPED | — | — | — | — | — | 0 | — | — | 18.96 | 370.73 | PGO prerequisite did not pass |
| G6 | SKIPPED | — | — | — | — | — | 0 | — | — | 18.95 | 370.73 | PGO prerequisite did not pass |
| G7 | SKIPPED | — | — | — | — | — | 0 | — | — | 18.94 | 370.73 | PGO prerequisite did not pass |
| G8 | SKIPPED | — | — | — | — | — | 0 | — | — | 18.94 | 370.73 | PGO prerequisite did not pass |

### 执行与技能对照

- G2 PASS。匹配加载器、集成 cc1、G1 恢复收据。训练和 SHA 核对通过后清理原 G1 BUILD。
- G3 PASS。对 23 份训练 profile 运行收据核对过的 llvm-profdata。
- G4 SKIPPED。用临时 R 派生打包副本注入本地 profdata。保留 G4 BUILD 至 G5 消费完 Ninja 图和链接输入。
- G5 SKIPPED。在 G4 构建树内重链并提取 BOLT 输入、工具及运行时归档。提取核对后清理 G4 BUILD。
- G6 SKIPPED。此阶段共享 19.08 GiB 的历史峰值下限。
- G7 SKIPPED。沿用 5% 双比率门禁。
- G8 SKIPPED。压缩资产与 provenance 留在结果目录，按物料身份生成离线清单。

告警、profile、门禁和清理

~~~json
{
  "G1_retained_build": {
    "logs_scanned": 1,
    "count": 826,
    "first": {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G-profiles/instrumented-build-1795020912008271908/build-0.txt",
      "line": 3170,
      "text": "LLVM Profile Warning: Unable to track new values: Running out of static counters.  Consider using option -mllvm -vp-counters-per-site=<n> to allocate more value profile counters at compile time."
    }
  },
  "G2_training": {
    "logs_scanned": 23,
    "count": 0,
    "first": null
  },
  "profile_artifacts": [
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/clang.profdata",
      "bytes": 52530416,
      "sha256": "39171c4a5fcb6166ac86d6d47ad16c7890527a73e66c26f035fb910288f496aa"
    }
  ],
  "BOLT_counts": null,
  "G4_ninja": [],
  "G4_runtime_logs": [],
  "G1_cleanup": {
    "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD",
    "bytes": 20000354304,
    "deleted": true
  },
  "G4_cleanup": null
}
~~~

G2 资源（VmHWM 为两秒采样，可能漏过短进程）

~~~json
{
  "memory.peak": "1778184192",
  "VmHWM_sample": {
    "bytes": 1095176192,
    "pid": 2318215,
    "argv": "/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64/ld-linux-x86-64.so.2 --library-path /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G-config/ir-artifacts/lib64:/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64:/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/lib64 /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G-config/ir-artifacts/clang-22 --target=armv7l-tizen-linux-gnueabi --sysroot=/home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0 -resource-dir=/home/linhao/Toolchain/development/llvm-optimize/temp/toolchain-baseline/usr/lib64/clang/22 -std=c++17 -O2 -c /home/linhao/Toolchain/development/llvm-optimize/archive/workspace-cleanup-135/recovered-training/A/A.cpp -o /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/00/input.o -fintegrated-cc1"
  },
  "memory.events": "low 0\nhigh 0\nmax 5726\noom 0\noom_kill 0\noom_group_kill 0",
  "memory.stat": "anon 10035200\nfile 1750503424",
  "memory.max": "1778184192",
  "memory.swap.peak": "0",
  "MemoryMax触顶事件": 5726,
  "before_disk": 378997821440,
  "after_disk": 398123458560
}
~~~

G2 结果

~~~json
{
  "stage": "ir-train",
  "artifacts": [
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/00/4921513259987090381_0-2318215.profraw",
      "bytes": 32385336,
      "sha256": "c601ad6994b0e80d4a4718ef11e78ca8e3133ccb770f51b6452d6e86e6aaf799"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/01/4921513259987090381_0-2318239.profraw",
      "bytes": 32366728,
      "sha256": "4d921b89f0b5cd2e3134bd352832aad8b2dee8d7513dec01ff8a1323d487a231"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/02/4921513259987090381_0-2318241.profraw",
      "bytes": 32366824,
      "sha256": "7ab93c8bbfba5fd9633371312fb69da2c3812bb2d6ffa881eff275120e17f089"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/03/4921513259987090381_0-2318248.profraw",
      "bytes": 32464808,
      "sha256": "cdcf2693a99f639587e46121124dbc71c7a4c708d891b1bbd1c7f4059ea2d132"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/04/4921513259987090381_0-2318268.profraw",
      "bytes": 32455624,
      "sha256": "77fbd461d113ebe86a571255911d6d191f5777b1e195473269e92966e016ead8"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/05/4921513259987090381_0-2318274.profraw",
      "bytes": 32458120,
      "sha256": "ba9b0637cc058028156cafbb33c9cd3c64157e6e31fed400e9795e664606c790"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/06/4921513259987090381_0-2318293.profraw",
      "bytes": 32463000,
      "sha256": "8d9d852fda5879833a45d746f0a7db9b09a518e8cefa0b470e645a27bf30ad2c"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/07/4921513259987090381_0-2318299.profraw",
      "bytes": 32452040,
      "sha256": "495fb8545f5f31ec0e30faa50638cacbe1d2b37d2c0d119cfd138af9f7153879"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/08/4921513259987090381_0-2318308.profraw",
      "bytes": 32453736,
      "sha256": "57454dc2a0e5f189c09e3d536a4d20a220689c13360b787fff6837854eff151e"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/09/4921513259987090381_0-2318315.profraw",
      "bytes": 32455576,
      "sha256": "3c0311ff56ea579f117861a05bfe95b9030cab7cf0e78d2b50f7a0b8d7ed6f26"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/10/4921513259987090381_0-2318322.profraw",
      "bytes": 32455160,
      "sha256": "b3c56e22efb7c41422ebfe887221dd177843a5f93561a6e2db801a078af549ad"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/11/4921513259987090381_0-2318329.profraw",
      "bytes": 32453400,
      "sha256": "5a1dc1cad89fd78cb22b3fb78e3ce1384d3b3919ff4a86b0dc9a972c892ff407"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/12/4921513259987090381_0-2318345.profraw",
      "bytes": 32456984,
      "sha256": "6bf1030aedab8de3776f11ccb87110072f98e5f9c5a390046f34792beb58c20e"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/13/4921513259987090381_0-2318360.profraw",
      "bytes": 32476584,
      "sha256": "37bd474cb7a7a7b280149be09dd30fdc2a38d9f560e87568feabf018de7f699a"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/14/4921513259987090381_0-2318369.profraw",
      "bytes": 32467144,
      "sha256": "a051c5950018d8e7feeddb9e46dcc254624c042c99a0b334b09c0533e3a57447"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/15/4921513259987090381_0-2318384.profraw",
      "bytes": 32468648,
      "sha256": "97229516a41fe5ecba17f8519baff9bb3c5c45b8984178004f995b0ef174ef20"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/16/4921513259987090381_0-2318393.profraw",
      "bytes": 32475256,
      "sha256": "52a6d9216135ae4767a94869b94ec0f989d85ebc55450bc5bc9039672881f0c4"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/17/4921513259987090381_0-2318400.profraw",
      "bytes": 32462488,
      "sha256": "678ca5ef57d6b25cc07845ff0d168c2cfea42c5eb2552b6df36f4fb374382d5a"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/18/4921513259987090381_0-2318405.profraw",
      "bytes": 32464056,
      "sha256": "f373c1ab316b253431854afd6ec8ce1457f70bc0e70a989f7942a8882ca262e3"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/19/4921513259987090381_0-2318410.profraw",
      "bytes": 32466120,
      "sha256": "df22c13b10d6c72f36d3f1805cfa509a7ab3222316c99bb05441fe39710151f6"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/20/4921513259987090381_0-2318433.profraw",
      "bytes": 32465384,
      "sha256": "0969705f08f9387cd0f9f571694dc91577c3fad5512d6584048d12ed6399249f"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/21/4921513259987090381_0-2318454.profraw",
      "bytes": 32465016,
      "sha256": "c1d414046b1374578a96791835582a7f441f3e4b54c98c37aba32e58d193f02c"
    },
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/22/4921513259987090381_0-2318462.profraw",
      "bytes": 32468136,
      "sha256": "34965ddefe63244dfc132d52e5f35e00b0cb5bb0df9d386f7e1426232001d6ea"
    }
  ],
  "bolt_match": null,
  "G1_cleanup": {
    "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD",
    "bytes": 20000354304,
    "deleted": true
  }
}
~~~

G3 资源（VmHWM 为两秒采样，可能漏过短进程）

~~~json
{
  "memory.peak": "2189705216",
  "VmHWM_sample": {
    "bytes": 1934172160,
    "pid": 2318781,
    "argv": "/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64/ld-linux-x86-64.so.2 --library-path /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64:/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/lib64 /home/linhao/Toolchain/development/llvm-optimize/temp/task133-d/tizen-tools/bin/llvm-profdata merge -o /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/clang.profdata /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/00/4921513259987090381_0-2318215.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/01/4921513259987090381_0-2318239.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/02/4921513259987090381_0-2318241.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/03/4921513259987090381_0-2318248.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/04/4921513259987090381_0-2318268.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/05/4921513259987090381_0-2318274.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/06/4921513259987090381_0-2318293.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/07/4921513259987090381_0-2318299.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/08/4921513259987090381_0-2318308.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/09/4921513259987090381_0-2318315.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/10/4921513259987090381_0-2318322.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/11/4921513259987090381_0-2318329.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/12/4921513259987090381_0-2318345.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/13/4921513259987090381_0-2318360.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/14/4921513259987090381_0-2318369.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/15/4921513259987090381_0-2318384.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/16/4921513259987090381_0-2318393.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/17/4921513259987090381_0-2318400.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/18/4921513259987090381_0-2318405.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/19/4921513259987090381_0-2318410.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/20/4921513259987090381_0-2318433.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/21/4921513259987090381_0-2318454.profraw /home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir/22/4921513259987090381_0-2318462.profraw"
  },
  "memory.events": "low 0\nhigh 0\nmax 231\noom 0\noom_kill 0\noom_group_kill 0",
  "memory.stat": "anon 9900032\nfile 556400640",
  "memory.max": "2189705216",
  "memory.swap.peak": "0",
  "MemoryMax触顶事件": 231,
  "before_disk": 398123384832,
  "after_disk": 398070784000
}
~~~

G3 结果

~~~json
{
  "stage": "merge-profdata",
  "artifacts": [
    {
      "path": "/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/clang.profdata",
      "bytes": 52530416,
      "sha256": "39171c4a5fcb6166ac86d6d47ad16c7890527a73e66c26f035fb910288f496aa"
    }
  ],
  "bolt_match": null
}
~~~

### 本地日志身份

| 步骤 | 本地路径 | 字节 | SHA256 |
|---|---|---:|---|
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-00.json` | 1,514 | `3f7e9785b78426c69abdd1502530f9546638203e89296b7f444171685c0da090` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-00.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-01.json` | 1,513 | `0b204ad7f4aae489c7c04bd9eaacf2fa648fcbf4bc6de2668a877766b0879d48` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-01.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-02.json` | 1,513 | `21bf9339b6973677e82d0297b60c1188147c46f25f657aee79a04829b057b21d` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-02.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-03.json` | 1,912 | `1cacde823692281e547e9d0824556dc8b2b27b944255cb34d7e3afdd1a45ecf4` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-03.txt` | 200,039 | `d066e4befd35ea7010311135b276e4532743f57cb3d3369a6e7636ad27d96939` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-04.json` | 1,918 | `397d47d6a4f6832beef80bf62788cb8bf9ed5e1bc65a6a6c2d7892e9925d0f07` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-04.txt` | 200,961 | `a7c5aabf4e7c795602d3159c491959256f88df84ace74f168502eca2c66ab21f` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-05.json` | 1,889 | `9d4c32cce3549035bfc2dc3f4740b88252d15d4c66bd8a73466a6af039d070aa` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-05.txt` | 200,507 | `e1f909c10f54c21d22a557686009e67c82911013e480f29af10c17a02229b805` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-06.json` | 1,885 | `28ff3d4c250a1545e6fb147afeb3cc69d050f3fa0b57879498f2906d4a844918` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-06.txt` | 199,811 | `956a5877b338c1bc380f5e6656a155f3dcdab6bd88dd31f6ef5cba2c73f0203b` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-07.json` | 1,877 | `0e0968a4a4a49d5ca6ff1aa8ae192bb35a414f4c5799dd3e6cd7a090f0367bcd` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-07.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-08.json` | 1,877 | `d88800a8cb979851e98d6a5f820a9b8390616c638b3d1b2aa50795f13faa3fb1` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-08.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-09.json` | 1,911 | `fcffbf594b65877827837a2a5bb65a0c3c8b8f6172df8b1ae623287261843de5` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-09.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-10.json` | 1,897 | `3f672db45485d0c9709af43522e7912cacd5f5f52c8e53bc2d0bc4755ce4549e` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-10.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-11.json` | 1,886 | `81eada50277cfc06f2719a885b73b8031b4fc83f8e3284960fdb4a9435057cef` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-11.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-12.json` | 1,894 | `44f670475b525aea42a3bf871c298d4c8e118b8850c656fd07e9485cba3f1936` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-12.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-13.json` | 1,918 | `fd02fd5f000878969091967df2174d64c410456530cef1a61f900ff314a7b7cb` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-13.txt` | 200,039 | `d066e4befd35ea7010311135b276e4532743f57cb3d3369a6e7636ad27d96939` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-14.json` | 1,923 | `4147435d532b5af1c3e1f4d8bfcdec90e4e9dd4eb6b824d31f208911ee7cb8a4` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-14.txt` | 200,961 | `a7c5aabf4e7c795602d3159c491959256f88df84ace74f168502eca2c66ab21f` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-15.json` | 1,895 | `951ce61558be83815f307a6faad0bf7fa26ef70e7d7404ef449c5dab8ec2e752` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-15.txt` | 200,507 | `e1f909c10f54c21d22a557686009e67c82911013e480f29af10c17a02229b805` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-16.json` | 1,891 | `1269b81c9fea4f4ccf5bf46dc7c43e36f25f198749cce583648abb16a1c98b47` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-16.txt` | 199,811 | `956a5877b338c1bc380f5e6656a155f3dcdab6bd88dd31f6ef5cba2c73f0203b` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-17.json` | 1,883 | `2827df2b49d07f065cf4d5588c275443ef58c39761e06c42ae9d0c829555990e` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-17.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-18.json` | 1,884 | `e3b0bd65fa47fdf1c59f810ae657cf492a867dba7be0502c0144a3bbeaec9999` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-18.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-19.json` | 1,912 | `9068aa24609ab1b5e0f19beea700405b3c4fa37f3afe71c23e3252f8e60308a2` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-19.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-20.json` | 1,903 | `ad9916dffcb1d748647b37ef5b0543b071aba55d6172d40c4e379d35c50ee49d` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-20.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-21.json` | 1,892 | `550257ade8d339104d926f530b79d5c028172b123d4f0cd42ddbd34f9fd32aa9` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-21.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-22.json` | 1,900 | `ae68ac9ee318b90d8e171e36c84de5bab9807f56ebc03226cdbdddbf70cbfac3` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/ir-train-1795078458515497910/ir-22.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G2/build-cleanup.json` | 209 | `eea9232267cc91780389014866f6ed8fc1d56d350ec984ffea97dac167f4bf55` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G2/resources.jsonl` | 178,660 | `44e20fd712f3e147e2f3e029a78d0d8d06ff974aa92515a7c60091f5beb4a41b` |
| G2 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G2/service.log` | 2,178 | `28ad44631bb89de5a7b1b1a24e427fb8f7ffc5cb3426a642cf0e322fe6e7da41` |
| G3 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/merge-profdata-1795078696026602008/merge.json` | 4,191 | `41723402cac2b2eb7dec512f8ba5e9860c7d30e7c7740d6a94591552198615a0` |
| G3 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G-profiles/merge-profdata-1795078696026602008/merge.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| G3 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G3/resources.jsonl` | 11,906 | `92a597dd3cfa20c055d68f226babb9ee0a7b41b30f5be7facf49b66aca1c8dfa` |
| G3 | `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-n-20261119/G3/service.log` | 1,555 | `1ca652a1ac63bacd71048df24649fd08e84992848718bc635084ab932c329cce` |
