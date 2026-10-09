# 42 夜间磁盘清理：A1完成，A2因保留工作树依赖停止

日期：2026-10-10（Asia/Shanghai）。起点 `f6a0499`。

**早上可由用户自行执行的命令：** 以下仅删除已授权的四个旧GBS根；脚本会重新检查挂载，有挂载即退出。本会话没有执行sudo脚本，四根仍存在。

```sh
bash /home/linhao/Toolchain/development/llvm-optimize/temp/deleted-roots-logs/sudo-delete.sh
```

**本轮状态：STOPPED_A2_RETAINED_WORKTREE_DEPENDENCY。** A1按旧逐文件清单删除35,384个二进制文件，分配块回收180.533333GiB；A3可读日志已保全、脚本已生成。三个Chromium目录均未删除。B、C-armv7l、C-aarch64全部NOT RUN，见[docs/40](40_arm_archive_conversion_stage1.md)。

清理前可用 **40.821182 GiB**；停止时 **218.766911 GiB**，净增 **177.945728 GiB**。净值扣除了本轮备份/证据写入并含宿主并发活动，不等于unlink分配块。120GiB空间线已满足；**停止原因不是磁盘不足，而是清单外Git依赖需要裁决**。

## 0. 范围、锁与停止依据

W=`/home/linhao/Toolchain/development/llvm-optimize`；E=`/home/linhao/Toolchain/development/llvm-optimize/temp/night-arm-stage1-20261010`。删前读取STATUS、docs/41全文、docs/39全文、docs/28 §1、docs/32、docs/35 §2–§5、docs/38。主仓库status为空。O_EXCL持有本项目锁，记录E/lock-acquired.json；不占用或停止其他项目进程。

用户无人值守规则是“规定之外的一律停止该步骤”，A2同时要求“plan_evaluation下的其他文件……一律不动”。备份得到以下真实依赖：

```text
git -C chromium-efl worktree list
/home/linhao/Toolchain/plan_evaluation/chromium-efl           2518b54dc8a8 [sandbox/dkson95/build]
/home/linhao/Toolchain/plan_evaluation/analysis/05E_worktree  6a454b2527f5 [analysis/05e-gbs-llvm-toggle]

cat /home/linhao/Toolchain/plan_evaluation/analysis/05E_worktree/.git
gitdir: /home/linhao/Toolchain/plan_evaluation/chromium-efl/.git/worktrees/05E_worktree

git -C /home/linhao/Toolchain/plan_evaluation/analysis/05E_worktree rev-parse --git-common-dir
/home/linhao/Toolchain/plan_evaluation/chromium-efl/.git
```

`analysis/05E_worktree`实际存在（含packaging），Git status退出0且输出空，以上不是仅存在于worktree注册表的失效残项。它不在三个删除目录中；整删chromium-efl会移除该保留工作树仍在使用的索引/refs/对象库。虽然其本地独有提交已导出patch，这不能等同保留Git工作树本身。

因此在任何Chromium rm启动前，先SIGSTOP拦住**本会话**的备份/删除串行器PID541504，查证后发送SIGTERM+SIGCONT使其退出143。不是杀掉别人的任务，也不是系统死机/构建失败；没有启动任何构建。没有擅自改05E的.git、迁移公共Git目录或扩大删除清单。

依据：备份目录chromium-efl/worktrees.stdout、E/stop-context.json（完整argv/stdout/exit）；E/a2-finish.log与该任务exit143。三个源目录仍存在，A2删除命令数=0。

### 0.1 文件检查方法

每范围先保存路径、文件数、去重inode的文件分配块、顶层列表（含模式/大小/链接）；本报告大小不含目录自身元数据。findmnt检查范围及后代，均无挂载；删除前再次检查可读/proc/*/cwd，无命中。不可读/已退出PID数在每项guard中记录，不冒称有root全进程视野。

A1匹配docs/41旧清单的dev/inode/逻辑大小，unlink前再核对；不跟随符号链接。A2备份全部完成后才计划删除，因上述依赖未进入rm。A3只读拷出日志。全程没有sudo、chmod、压缩、移动原件或宿主配置修改。

## 1. A1逐文件结果

后缀范围为.a/.o/.rpm/.bc/.so，否则须≥1MiB且头为ELF/ar/bitcode；文本、JSON、脚本保留。引用旧清单：W/temp/disk-inventory-20261009/binary-payload-candidates.jsonl。

| 范围 | 删前文件数 | 文件分配GiB | 候选 | 已删 | 无旧清单 | 回收分配GiB |
|---|---:|---:|---:|---:|---:|---:|
| `W/temp/static-native-conversion-v2-20260924/conversion/archives` | 225 | 6.161209 | 225 | 225 | 0 | 6.161209 |
| `W/temp/static-native-conversion-v3-20260924/stripped/archives` | 225 | 0.485172 | 225 | 225 | 0 | 0.485172 |
| `W/temp/llvm-strip-alternative-20260929/bc-archives` | 225 | 5.106339 | 225 | 225 | 0 | 5.106339 |
| `W/temp/llvm-strip-alternative-20260929/hq-payload` | 225 | 5.106308 | 225 | 225 | 0 | 5.106308 |
| `W/temp/llvm-strip-alternative-20260929/hq-rpm-extract` | 225 | 5.106323 | 225 | 225 | 0 | 5.106323 |
| `W/temp/llvm-strip-alternative-20260929/hq-rpm-repo` | 29 | 0.000343 | 0 | 0 | 0 | 0.000000 |
| `W/temp/llvm-strip-alternative-20260929/hq-rpmbuild` | 2 | 2.036564 | 1 | 1 | 0 | 2.036560 |
| `W/temp/llvm-strip-alternative-20260929/host-consumers` | 72 | 0.947212 | 4 | 4 | 0 | 0.926846 |
| `W/temp/archive-fix-v2-build-20260929/conversion` | 67542 | 6.747952 | 225 | 225 | 0 | 6.161201 |
| `W/temp/archive-fix-v2-build-20260929/llvm-strip-overlay` | 3519 | 1.139149 | 540 | 540 | 0 | 0.955452 |
| `W/temp/archive-fix-v2-build-20260929/strip-elf-analysis` | 6 | 0.055820 | 2 | 2 | 0 | 0.000008 |
| `W/temp/gbs-root-x86_64-archivefix/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD` | 268699 | 162.492771 | 33487 | 33487 | 0 | 148.487915 |
| `W/temp/static-native-conversion-20260924` | 32955 | 6.291203 | 225 | 0 | 225 | 0.000000 |
| `W/temp/archive-fix-rebind-20260923` | 5658 | 22.623360 | 663 | 0 | 663 | 0.000000 |
| `W/temp/toolchain-hybrid-trial` | 5129 | 5.752640 | 303 | 0 | 303 | 0.000000 |
| `W/temp/hybrid-trial-20260922` | 3456 | 5.719669 | 294 | 0 | 294 | 0.000000 |

**权限删除失败0；身份变化0；未使用sudo。** A1第6–8组共1,485个候选没有旧逐文件登记，按用户“不一致的不删、单列”全部保留为NOT_IN_DOCS41；没有以本轮新清单自我放行。

P30-BUILD旧清单另有4个小文件不满足本次严格后缀/1MiB口径，保留：libRemarks.so.22.1、ld64.so.2、dyn-rel.so.elf-mips、AndroidModule.so.sym，分配20,480B。不是身份不一致，也未扩展到.so.*后缀补删。

删前全集E/a1-files.jsonl，逐文件删除结果E/a1-delete-events.jsonl；每范围删前元数据E/a1-scope-*-before.json，汇总与各次df为E/a1-summary.json；四小文件E/a1-retained-protected.json。

## 2. A2备份与未删除项

备份根=`/home/linhao/Toolchain/plan_evaluation/deleted-chromium-backup`。每条Git命令超时900秒，GIT_OPTIONAL_LOCKS=0；实际未发生超时。

| 目录 | 删前文件数 | 文件分配GiB | Git命令 | 独有提交导出 | 删除 |
|---|---:|---:|---|---|---|
| `~/Toolchain/plan_evaluation/chromium-efl` | 645023 | 54.465847 | 全部exit0 | 2 | **未执行** |
| `~/Toolchain/plan_evaluation/chromium-efl-spike-libcxx-wt` | 1029963 | 34.511261 | 全部exit0 | 1 | **未执行** |
| `~/Toolchain/plan_evaluation/chromium-efl-spike-libcxx` | 751587 | 21.047279 | 全部exit128：失效.git指针 | UNKNOWN | **未执行** |

每子目录已保存status --porcelain、branch -vv、worktree list、stash list、diff与diff --cached（--binary/--full-index）、log --branches --not --remotes及rev-list的stdout/stderr和commands.jsonl。前两个工作树status干净、未跟踪清单为空。

| 本地独有提交 | 导出位置 |
|---|---|
| `2518b54dc8a89613e202c6886acb9b1f138c1b3d` | `/home/linhao/Toolchain/plan_evaluation/deleted-chromium-backup/chromium-efl/local-patches/00000-2518b54dc8a89613e202c6886acb9b1f138c1b3d.patch.stdout` |
| `6a454b2527f5eddcd06e4de1e78407b9456fa3b8` | `/home/linhao/Toolchain/plan_evaluation/deleted-chromium-backup/chromium-efl/local-patches/00001-6a454b2527f5eddcd06e4de1e78407b9456fa3b8.patch.stdout` |
| `111f88ff245928cc9db2a717185267054570300f` | `/home/linhao/Toolchain/plan_evaluation/deleted-chromium-backup/chromium-efl-spike-libcxx-wt/local-patches/00000-111f88ff245928cc9db2a717185267054570300f.patch.stdout` |

第三目录的.git原本指向不存在的chromium-efl/.git/worktrees/chromium-efl-spike-libcxx，所有查询exit128。这项失败本来按用户预授权不阻止删除，**本次停止由另一实际保留的05E_worktree依赖触发**，不混同两个问题。

第三目录额外补存小文本的过程被安全中止：fallback-files.jsonl已完整落盘246,163条记录，含235,633条小文本备份SHA；tracked_state均UNKNOWN。out*目录仅登记目录名。备份仍是PARTIAL，不能宣称未跟踪文件已完整保全；所有原文件仍在。E/a2-fallback-partial.json登记边界。

原计划的三个rm -rf --one-file-system均**没有执行**。没有为了继续删除而改写保留工作树的.git，未删除其他两个目录来绕过“失败停止后续”的要求。

## 3. A3日志保全与sudo脚本（未执行）

| 根 | 可读文件数 | 文件分配GiB | 复制日志/文本数 | 复制字节 | 不可读目录数 |
|---|---:|---:|---:|---:|---:|
| `W/temp/gbs-root-x86_64-baseline` | 260293 | 208.766792 | 4380 | 102705873 | 3 |
| `W/temp/gbs-root-x86_64-hybrid-trial` | 220512 | 50.080677 | 4377 | 103420188 | 3 |
| `W/temp/gbs-root-hq-consumer-lld` | 15217 | 9.349163 | 12 | 2203706 | 3 |
| `W/temp/gbs-root-hq-consumer-bfd` | 15212 | 8.886868 | 11 | 2198014 | 3 |

按原相对路径复制到W/temp/deleted-roots-logs/<根名>/；各copied-manifest.json列路径/字节/SHA，复制后重新计算源与备份SHA并比较。保全.log/.build.log/.json/.jsonl/.txt/QUARANTINED.txt、logs目录内文本、local/repos构建日志。每根3个不可读特权目录单列，未输入密码/强行读取；详见E/a3-summary.json的errors。

合计复制8,780份、210,527,781B。四根均无挂载，均列入脚本；A1无权限失败文件，未追加其他删除行。脚本SHA256=`94172ac9fb7f9de7435e6b1734692fe4a7f1eeda2f95e2b6a9ec88a0a5cce7e4`；仅做bash -n语法检查，未执行。

脚本全文：

```bash
#!/bin/bash
set -euo pipefail
# Generated 2026-10-10; NOT executed by the agent.
check_mounts() {
  findmnt --json --list -o TARGET | python3 -c 'import sys,json,pathlib; p=pathlib.Path(sys.argv[1]); a=[x["target"] for x in json.load(sys.stdin)["filesystems"] if pathlib.Path(x["target"])==p or p in pathlib.Path(x["target"]).parents]; print("REFUSE mounted path: "+repr(a),file=sys.stderr) if a else None; sys.exit(1 if a else 0)' "$1"
}
check_mounts /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-baseline
check_mounts /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-hybrid-trial
check_mounts /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-hq-consumer-lld
check_mounts /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-hq-consumer-bfd
sudo rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-baseline
sudo rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-hybrid-trial
sudo rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-hq-consumer-lld
sudo rm -rf --one-file-system -- /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-hq-consumer-bfd
```

## 4. 磁盘、停止与恢复边界

原始df（停止后）：

```text
Filesystem         1B-blocks          Used    Available Use% Mounted on
/dev/sda1      1967844950016 1632909156352 234899181568  88% /home
/dev/nvme0n1p1  501809635328   95124766720 381119066112  20% /
```

120GiB门槛已满足；不以容量PASS覆盖A2的清单外依赖。按用户总规则，不启动B以及两个ARM步骤，不改Source/spec/补丁、不重试清理。

恢复所需裁决只涉及05E：若它也已作废，可明确将其Git依赖一并作废；若需保留，则需明确授权保全公共Git元数据并调整工作树引用。两者本轮均未擅自执行，也未在无人值守阶段请求确认。A1第6–8组另缺历史逐文件基线，若日后仍要删除，需要单独确定新的核对方式。

项目锁收尾释放；无本任务构建进程、采样器或新挂载。保护文件39项摘要检查无差异（此检查在写新报告/STATUS前）：E/protected-final.json；收尾进程与锁见E/final-cleanup.json、lock-released.json。

## 附录A：删前顶层列表

完整模式/大小/链接元数据在各before.json；下列仅名字，不是额外删除授权。

- `W/temp/static-native-conversion-v2-20260924/conversion/archives`：`usr`
- `W/temp/static-native-conversion-v3-20260924/stripped/archives`：`usr`
- `W/temp/llvm-strip-alternative-20260929/bc-archives`：`libLLVMFuzzMutate.a, libLLVMARMAsmParser.a, libclangBasic.a, libLLVMAsmParser.a, libclangTidyReadabilityModule.a, libLLVMAArch64Disassembler.a, libLLVMPlugins.a, libclangdSupport.a, libclangSupport.a, libclangDaemon.a, libLLVMExtensions.a, libclangInstallAPI.a, libclangTidyCustomModule.a, libclangIndexSerialization.a, libclangIncludeCleaner.a, libclangDependencyScanning.a, libLLVMObjCopy.a, libLLVMAArch64CodeGen.a, libLLVMExegesisX86.a, libLLVMMIRParser.a, libLLVMDlltoolDriver.a, libLLVMProfileData.a, libLLVMJITLink.a, libLLVMCodeGenTypes.a, libclangIncludeFixerPlugin.a, libLLVMTextAPIBinaryReader.a, libLLVMFrontendAtomic.a, libclangHandleLLVM.a, libclangTidyCppCoreGuidelinesModule.a, libclangToolingASTDiff.a, libLLVMOption.a, libclangASTMatchers.a, libLLVMipo.a, libLLVMSandboxIR.a, libLLVMRemarks.a, libclangTidy.a, libclangSema.a, libLLVMPasses.a, libclangTidyFuchsiaModule.a, libclangTidyZirconModule.a, libclangTidyAlteraModule.a, libclangTidyAbseilModule.a, libLLVMDebugInfoDWARFLowLevel.a, libLLVMLibDriver.a, libLLVMHipStdPar.a, libclangDirectoryWatcher.a, libLLVMTableGenCommon.a, libLLVMBitstreamReader.a, libclangToolingRefactoring.a, libLLVMX86Disassembler.a, libclangTidyLinuxKernelModule.a, libLLVMOrcDebugging.a, liblldCommon.a, libclangRewrite.a, libLLVMFrontendHLSL.a, libLLVMX86TargetMCA.a, libLLVMObjectYAML.a, libclangTidyPortabilityModule.a, libLLVMFrontendDriver.a, libLLVMARMCodeGen.a, libLLVMOptDriver.a, libclangAPINotes.a, libLLVMARMDesc.a, libclangTidyLLVMLibcModule.a, libclangStaticAnalyzerCheckers.a, libLLVMCAS.a, libLLVMExegesisAArch64.a, libclangIncludeFixer.a, libLLVMInterfaceStub.a, libclangTidyModernizeModule.a, libLLVMSupportLSP.a, libLLVMLinker.a, libLLVMOrcShared.a, libLLVMVectorize.a, libLLVMScalarOpts.a, libLLVMDebuginfod.a, libclangToolingInclusions.a, libclangQuery.a, libLLVMBPFDisassembler.a, libLLVMDiff.a, libclangTidyConcurrencyModule.a, liblldWasm.a, libLLVMInterpreter.a, libclangTidyMiscModule.a, libLLVMExecutionEngine.a, libfindAllSymbols.a, libLLVMFrontendOpenMP.a, libLLVMX86Info.a, libLLVMDWARFCFIChecker.a, libLLVMAArch64Utils.a, libclangReorderFields.a, libclangAnalysisFlowSensitive.a, libLLVMAArch64Info.a, libclangDoc.a, libLLVMXRay.a, libLLVMFileCheck.a, libLLVMAsmPrinter.a, libclangTidyLLVMModule.a, libLLVMExegesis.a, libclangTidyObjCModule.a, libLLVMX86AsmParser.a, libLLVMDebugInfoDWARF.a, libclangCodeGen.a, libLLVMBitWriter.a, libLLVMSupport.a, libLLVMAArch64Desc.a, libLLVMBPFCodeGen.a, libclangdMain.a, libclangToolingCore.a, libLLVMDWARFLinkerClassic.a, libLLVMTextAPI.a, libLLVMIRReader.a, libclangFrontend.a, libclangStaticAnalyzerFrontend.a, libclangTidyBoostModule.a, libLLVMTargetParser.a, libLLVMDWP.a, libclangTidyMain.a, libclangCrossTU.a, libLLVMSymbolize.a, libLLVMDebugInfoCodeView.a, libLLVMABI.a, libclangApplyReplacements.a, libLLVMWindowsManifest.a, libLLVMSelectionDAG.a, libLLVMDTLTO.a, libLLVMARMInfo.a, libLLVMCGData.a, libLLVMMCJIT.a, libclangTooling.a, libLLVMOrcJIT.a, libLLVMIRPrinter.a, libclangTransformer.a, libarcher_static.a, libclangAnalysisScalable.a, libclangFormat.a, libLLVMObjCARCOpts.a, libLLVMCoroutines.a, libLLVMLTO.a, libclangDriver.a, libLLVMDebugInfoLogicalView.a, libLLVMFrontendOffloading.a, libclangExtractAPI.a, libLLVMMCParser.a, libLLVMDWARFLinker.a, libLLVMTableGenBasic.a, libclangParse.a, libLLVMX86CodeGen.a, libLLVMObject.a, libLLVMCodeGen.a, liblldMachO.a, libclangSerialization.a, libLLVMAggressiveInstCombine.a, libclangLex.a, libclangDaemonTweaks.a, libLLVMLineEditor.a, libLLVMBitReader.a, libclangTidyCERTModule.a, libLLVMMCDisassembler.a, libclangAnalysisLifetimeSafety.a, libclangFrontendTool.a, libLLVMGlobalISel.a, libLLVMDemangle.a, libLLVMTarget.a, libclangTidyHICPPModule.a, libLLVMCoverage.a, libclangTidyPlugin.a, libclangAnalysisFlowSensitiveModels.a, libLLVMTableGen.a, libclangTidyMPIModule.a, libclangInterpreter.a, libLLVMFrontendDirective.a, libLLVMARMUtils.a, libclangChangeNamespace.a, libLLVMOrcTargetProcess.a, libLLVMAnalysis.a, liblldCOFF.a, libLLVMMCA.a, libclangAnalysis.a, libLLVMWindowsDriver.a, libclangMove.a, libLLVMBPFDesc.a, libLLVMDebugInfoMSF.a, libclangTidyGoogleModule.a, libLLVMMC.a, libLLVMDWARFLinkerParallel.a, libclangTidyPerformanceModule.a, libLLVMBPFAsmParser.a, libclangToolingInclusionsStdlib.a, libLLVMTelemetry.a, libLLVMRuntimeDyld.a, libLLVMCFGuard.a, libclangTidyBugproneModule.a, libLLVMDebugInfoPDB.a, libLLVMInstCombine.a, libLLVMAArch64AsmParser.a, libclangDynamicASTMatchers.a, libLLVMX86Desc.a, libclangHandleCXX.a, libLLVMDebugInfoGSYM.a, libclangIndex.a, libLLVMBinaryFormat.a, libclangAST.a, libclangDocSupport.a, libLLVMARMDisassembler.a, libclangToolingSyntax.a, libclangTidyAndroidModule.a, libclangOptions.a, libclangTidyOpenMPModule.a, libclangdRemoteIndex.a, libLLVMInstrumentation.a, libLLVMBPFInfo.a, libLLVMFrontendOpenACC.a, liblldMinGW.a, liblldELF.a, libLLVMCFIVerify.a, libclangStaticAnalyzerCore.a, libLLVMCore.a, libclangTidyUtils.a, libclangTidyDarwinModule.a, libLLVMTransformUtils.a, libLLVMFuzzerCLI.a, libclangRewriteFrontend.a, libLLVMDebugInfoBTF.a, libclangEdit.a`
- `W/temp/llvm-strip-alternative-20260929/hq-payload`：`usr`
- `W/temp/llvm-strip-alternative-20260929/hq-rpm-extract`：`usr`
- `W/temp/llvm-strip-alternative-20260929/hq-rpm-repo`：`clang-debuginfo-22.1.8-1.x86_64.rpm, clang-devel-debuginfo-22.1.8-1.x86_64.rpm, clang-22.1.8-1.x86_64.rpm, compiler-rt-debuginfo-22.1.8-1.x86_64.rpm, llvm-devel-debuginfo-22.1.8-1.x86_64.rpm, libomp-22.1.8-1.x86_64.rpm, lldb-22.1.8-1.x86_64.rpm, python-clang-22.1.8-1.x86_64.rpm, llvm-22.1.8-1.x86_64.rpm, libllvm-22.1.8-1.x86_64.rpm, compiler-rt-22.1.8-1.x86_64.rpm, llvm-static-devel-22.1.8.hqbc1-1.x86_64.rpm, llvm-devel-22.1.8-1.x86_64.rpm, llvm-debuginfo-22.1.8-1.x86_64.rpm, clang-devel-22.1.8-1.x86_64.rpm, repodata, lldb-devel-22.1.8-1.x86_64.rpm, llvm-debugsource-22.1.8-1.x86_64.rpm, libomp-debuginfo-22.1.8-1.x86_64.rpm, libllvm-debuginfo-22.1.8-1.x86_64.rpm, lldb-debuginfo-22.1.8-1.x86_64.rpm, libomp-devel-22.1.8-1.x86_64.rpm, lldb-devel-debuginfo-22.1.8-1.x86_64.rpm`
- `W/temp/llvm-strip-alternative-20260929/hq-rpmbuild`：`RPMS, BUILDROOT, SPECS, BUILD, SRPMS`
- `W/temp/llvm-strip-alternative-20260929/host-consumers`：`query-libs.memory.jsonl, link-clang-bfd.time, link-clang-lld.memory.jsonl, link-clang-bfd.log, query-libs.log, link-clang-bfd-llvmgold.json, query-ldflags.time, query-libs.time, query-libs.json, query-cxxflags.json, prefix, clang-bfd-llvmgold, query-system.json, compile-a-clang.time, link-gcc-bfd.time, reference-opt.log, query-system.time, link-gcc-bfd.memory.jsonl, run-clang-lld.time, run-clang-bfd-llvmgold.memory.jsonl, link-clang-lld.json, query-system.memory.jsonl, run-clang-bfd-llvmgold.json, query-cxxflags.log, gcc-bfd-driver.txt, run-clang-bfd-llvmgold.log, clang-bfd-llvmgold-driver.txt, query-cxxflags.time, query-cxxflags.memory.jsonl, compile-a-gcc.memory.jsonl, clang-lld-output.ll, link-clang-bfd.memory.jsonl, run-clang-lld.memory.jsonl, clang-lld, compile-a-gcc.time, a-clang.o, query-ldflags.txt, link-clang-lld.time, compile-a-clang.memory.jsonl, reference-opt.json, reference-opt.time, link-clang-bfd-llvmgold.memory.jsonl, query-system.log, query-ldflags.log, compile-a-gcc.json, input.ll, query-libs.txt, compile-a-clang.json, link-gcc-bfd.json, clang-bfd-driver.txt, run-clang-bfd-llvmgold.time, result.json, ld.lld, query-cxxflags.txt, reference-opt.memory.jsonl, expected.ll, a.cpp, query-system.txt, link-clang-bfd-llvmgold.log, a-gcc.o, link-clang-lld.log, query-ldflags.json, clang-lld-driver.txt, query-ldflags.memory.jsonl, link-clang-bfd-llvmgold.time, run-clang-lld.json, link-clang-bfd.json, run-clang-lld.log, compile-a-clang.log, clang-bfd-llvmgold-output.ll, compile-a-gcc.log, link-gcc-bfd.log`
- `W/temp/archive-fix-v2-build-20260929/conversion`：`compiler-version-command.json, compiler-version-command.log, archives, compiler-version.txt, compiler-version-command.time, members, summary.json`
- `W/temp/archive-fix-v2-build-20260929/llvm-strip-overlay`：`version.log, version.json, libraries.log, libraries.time, run-2, version.time, libraries.memory.jsonl, libraries.json, run-1, version.memory.jsonl, checks, summary.json`
- `W/temp/archive-fix-v2-build-20260929/strip-elf-analysis`：`allocated-content-summary.json, llvm.o, gnu.o, llvm-readelf.txt, gnu-readelf.txt, summary.json`
- `W/temp/gbs-root-x86_64-archivefix/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD`：`llvm-22.1.8`
- `W/temp/static-native-conversion-20260924`：`conversion, config-query-prefix, final-cleanup.json, other-arch-discovery.json, converter-identities.json, other-arch-packages.json, baseline-content-check.json, baseline-check.log, conversion-tests.log, scope, consumers, hold_lock.py, other-arch-accel-targets.json, executed-tools-sha256.json, check_baseline.py, run_consumer_scope.py, llvm-config-queries.json, lock-acquired.json, precheck.json, cpu-attribute-check, other-arch-accel-versions.json, write_report.py, report-audit.json, other-arch-cached-static-devel.json, lock-released.json, llvm-config-relocated-queries.json, check_empty_modules.py, consumer-scope, preservation-check.json, __pycache__, scope-cleanup.json, release-lock, push-verification.json, update_status.py, other-arch-runtime-layout.json, conversion-driver.log, conversion-summary.json, consumer-driver.log, modules-without-cpu.json, rpm-identity.json`
- `W/temp/archive-fix-rebind-20260923`：`relink, rootcause, correctness, rewrite, consumer, repack, liveness`
- `W/temp/toolchain-hybrid-trial`：`usr, home`
- `W/temp/hybrid-trial-20260922`：`capture_link_map.py, build-milestones.txt, run, progress.py, final-tools.diff, preflight-console.log, disk-du-stderr.txt, exported-source-check.json, applied-source-sha256.json, liveness-clang.log, liveness-lld.log, archives-console.log, check_archives.py, protected-after.json, ninja-query.json, identity-objcopy.exit, correctness-summary.json, link-target-map.json, identity-clang.log, exported.spec, remaining-static-source-evidence.txt, source-after.json, correctness-arm-training.log, ninja-commands.txt, run-console.log, archives, clang-comparison, correctness-aarch64, inspect_products.py, task-state.json, liveness-lld, applied-source.diff, five-tools.log, exported-spec.diff, liveness-clang, disk-after.txt, identity-objcopy.log, push-result.log, ninja-commands.stderr, correctness-console.log, products, resource-summary.json, correctness-arm-training, correctness-aarch64.log, correctness-arm-holdout.log, cache-key-lines.txt, products-console.log, correctness-arm-holdout, scope-reaped.json, liveness-tools-test, running-scope.txt, correctness-commands.json, delivery.json, build-gates-tests.log, final-audit.json, five-tools-console.log, known-bad-armap.txt, build-gates-final-tests.log, identity-clang.exit, summarize_resources.py, preflight, liveness-tools-tests.log, revision, link-command-summary.json, resource-summary.log, five-tools.json, finalize_report.py, run_correctness.py`
- `~/Toolchain/plan_evaluation/chromium-efl`：`codereview.settings, mojo, .clang-format, build, net, buildtools, .gitmodules, chrome.sh, .gitattributes, PRESUBMIT_test_mocks.py, google_apis, build_overrides, url, ATL_OWNERS, CODE_OF_CONDUCT.md, LICENSE, services, tizen_src, chromeos, PRESUBMIT.py, gpu, apps, content_shell.sh, crypto, ppapi, native_client, tools, .landmines, pdf, electron, .gn, v8, cc, printing, .vpython, .yapfignore, rlz, ash, DEPS, extensions, .gitignore, third_party, skia, native_client_sdk, ipc, .git, courgette, sandbox, .clang-tidy, packaging, DIR_METADATA, device, .vpython3, wrt, testing, content, .rustfmt.toml, media, styleguide, PRESUBMIT_test.py, AUTHORS, .mailmap, README.md, OWNERS, fuchsia_web, sql, base, storage, remoting, gin, headless, .git-blame-ignore-revs, codelabs, ui, WATCHLISTS, components, chrome, .eslintrc.js, dbus`
- `~/Toolchain/plan_evaluation/chromium-efl-spike-libcxx-wt`：`codereview.settings, mojo, .clang-format, agents, build, elfbins.list, .github, .geminiignore, net, .clangd, buildtools, chromecast, .gitmodules, infra, chrome.sh, .cursorignore, .gitattributes, PRESUBMIT_test_mocks.py, google_apis, build_overrides, android_webview, url, ATL_OWNERS, CODE_OF_CONDUCT.md, LICENSE, services, tizen_src, chromeos, PRESUBMIT.py, gpu, apps, content_shell.sh, crypto, debugsources.list, tools, .landmines, chromium-efl-debuginfo.manifest, pdf, target.txt, electron, .gn, v8, cc, printing, CRYPTO_OWNERS, .yapfignore, rlz, .DEPS.swp, ash, debugfiles.list, DEPS, extensions, .gitignore, third_party, skia, documentation.list, ipc, .git, .gitallowed, sandbox, .clang-tidy, packaging, DIR_METADATA, device, .vpython3, wrt, out.chrome.tz_v11.0.standard.armv7l, chromium-efl-debugsource.manifest, testing, content, .rustfmt.toml, media, styleguide, PRESUBMIT_test.py, AUTHORS, host_arch.txt, .mailmap, README.md, OWNERS, fuchsia_web, sql, base, debuglinks.list, storage, remoting, gin, SECURITY_OWNERS, .gemini, debugsourcefiles.list, headless, docs, ios, .git-blame-ignore-revs, CPPLINT.cfg, codelabs, ui, WATCHLISTS, components, chrome, BUILD.gn, dbus`
- `~/Toolchain/plan_evaluation/chromium-efl-spike-libcxx`：`url, tizen_src, tools, v8, ash, DEPS, extensions, .gitignore, third_party, skia, ipc, .git, .gitallowed, sandbox, .clang-tidy, packaging, DIR_METADATA, device, .vpython3, wrt, testing, content, .rustfmt.toml, media, styleguide, PRESUBMIT_test.py, AUTHORS, .mailmap, README.md, OWNERS, fuchsia_web, sql, base, storage, remoting, gin, SECURITY_OWNERS, .gemini, headless, docs, ios, .git-blame-ignore-revs, CPPLINT.cfg, codelabs, ui, WATCHLISTS, components, chrome, BUILD.gn, dbus`
- `W/temp/gbs-root-x86_64-baseline`：`local`
- `W/temp/gbs-root-x86_64-hybrid-trial`：`local`
- `W/temp/gbs-root-hq-consumer-lld`：`local`
- `W/temp/gbs-root-hq-consumer-bfd`：`local`

## 附录B：证据入口与自检

- E/cleanup.py、a1-*.json[l]：匹配与逐文件unlink；A1完成exit0。
- E/chromium_cleanup.py、a2-backup.log、a2-backup-summary.json：三树元数据备份。E/chromium_finish.py、a2-finish.log：小文本补存未完，在任何rm前中止。
- E/prepare_sudo.py、a3-*.json、a3-copy.log：日志复制及脚本生成，exit0。
- E/stop-context.json：保留工作树实际Git依赖、三原目录存在、无rm；不是把旧失效第三工作树当停止理由。
- 日志/JSON/脚本/源码全部保留于A1范围；仅按本次口径删除旧二进制。Rnew/B、N、N38、H、rpms-docs35、docs35–39、base-local-repo、docs30两测试根、共享ARM根及其他项目未清理。
- A3四根仅拷日志，不删除；没有sudo、宿主配置变更、LLVM/Chromium构建、BOLT、性能校准或Gerrit推送。
