# Training inputs

The reference workload contains 13 ARMv7 and 10 AArch64 compiler invocations. Use the same ordered rows for IR and BOLT training. Each invocation is a single translation-unit compile with the complete ordered argv in [training-set.json](training-set.json). Append -c INPUT -o OBJECT to that argv.

## Obtain and verify the inputs

- Generate A at seed 73419 and scale 1, and B/C at the same seed and scale 2. The bundled generator writes all three inputs for each scale. Copy A from scale 1 and B/C from scale 2 into the configured synthetic directory. Verify the recorded bytes and SHA-256.
- Obtain the .ii inputs from an authorized corpus mirror or reproduce them with the matching LLVM source and compiler, target sysroot, and dependency configuration. Enable the CMake compilation database in the pinned root, locate the source by its translation-unit name below, and take the corresponding compile argv. Preserve preprocessing flags, defines, include order, target and language mode. Remove the object/dependency outputs and replace the compile action with -E -o INPUT.ii. Preserve line markers. Use the matching architecture for each row.
- The JSON hashes identify historical input bytes. A fresh preprocessing run can differ because of headers, macros or paths in line markers. On mismatch, use authorized matching bytes or approve a new input snapshot with newly computed hashes, full preprocessing argv and revised provenance, then regenerate both profiles. The two architecture directories are distinct even where filenames match.
- LLVM source is generally Apache-2.0 with LLVM exceptions. Preserve applicable notices and consult the source tree license. Preprocessed files can contain headers from third parties and platform SDKs. Confirm redistribution rights for every captured input before transferring it. The preprocessed files and SDKs are supplied separately by the operator. The synthetic recipe generates benchmark inputs without distributing SDK headers.

## Ordered rows

| # | Training entry | Input |
|---:|---|---|
| 1 | A | {synthetic_dir}/A.cpp |
| 2 | B | {synthetic_dir}/B.cpp |
| 3 | C | {synthetic_dir}/C.cpp |
| 4 | real_llvm_arm_ARMISelLowering | {inputs}/armv7l/llvm_arm_ARMISelLowering.ii |
| 5 | real_llvm_arm_ARMTargetTransformInfo | {inputs}/armv7l/llvm_arm_ARMTargetTransformInfo.ii |
| 6 | real_llvm_codegen_MachinePipeliner | {inputs}/armv7l/llvm_codegen_MachinePipeliner.ii |
| 7 | real_llvm_codegen_SelectionDAG | {inputs}/armv7l/llvm_codegen_SelectionDAG.ii |
| 8 | real_llvm_mc_AsmParser | {inputs}/armv7l/llvm_mc_AsmParser.ii |
| 9 | real_llvm_mc_MasmParser | {inputs}/armv7l/llvm_mc_MasmParser.ii |
| 10 | real_llvm_sema_SemaExprCXX | {inputs}/armv7l/llvm_sema_SemaExprCXX.ii |
| 11 | real_llvm_sema_SemaStmt | {inputs}/armv7l/llvm_sema_SemaStmt.ii |
| 12 | real_llvm_transforms_Attributor | {inputs}/armv7l/llvm_transforms_Attributor.ii |
| 13 | real_llvm_transforms_WholeProgramDevirt | {inputs}/armv7l/llvm_transforms_WholeProgramDevirt.ii |
| 14 | real_aarch64_llvm_arm_ARMISelLowering | {inputs}/aarch64/llvm_arm_ARMISelLowering.ii |
| 15 | real_aarch64_llvm_arm_ARMTargetTransformInfo | {inputs}/aarch64/llvm_arm_ARMTargetTransformInfo.ii |
| 16 | real_aarch64_llvm_codegen_MachinePipeliner | {inputs}/aarch64/llvm_codegen_MachinePipeliner.ii |
| 17 | real_aarch64_llvm_codegen_SelectionDAG | {inputs}/aarch64/llvm_codegen_SelectionDAG.ii |
| 18 | real_aarch64_llvm_mc_AsmParser | {inputs}/aarch64/llvm_mc_AsmParser.ii |
| 19 | real_aarch64_llvm_mc_MasmParser | {inputs}/aarch64/llvm_mc_MasmParser.ii |
| 20 | real_aarch64_llvm_sema_SemaExprCXX | {inputs}/aarch64/llvm_sema_SemaExprCXX.ii |
| 21 | real_aarch64_llvm_sema_SemaStmt | {inputs}/aarch64/llvm_sema_SemaStmt.ii |
| 22 | real_aarch64_llvm_transforms_Attributor | {inputs}/aarch64/llvm_transforms_Attributor.ii |
| 23 | real_aarch64_llvm_transforms_WholeProgramDevirt | {inputs}/aarch64/llvm_transforms_WholeProgramDevirt.ii |

## Exact invocation groups

**Group 1.** A, B, C

~~~text
--target=armv7l-tizen-linux-gnueabi --sysroot={sysroot_armv7l} -resource-dir={resource_dir} -std=c++17 -O2
~~~

**Group 2.** real_llvm_arm_ARMISelLowering, real_llvm_arm_ARMTargetTransformInfo

~~~text
--target=armv7l-tizen-linux-gnueabi --sysroot={sysroot_armv7l} -resource-dir={resource_dir} -g2 -gdwarf-4 -fexceptions -frecord-gcc-switches -fasynchronous-unwind-tables -g -O3 -fomit-frame-pointer -fPIC -fno-semantic-interposition -fvisibility-inlines-hidden -ffunction-sections -fdata-sections -O3 -std=c++17 -fvisibility=hidden -fno-exceptions -funwind-tables -x c++-cpp-output
~~~

**Group 3.** real_llvm_codegen_MachinePipeliner, real_llvm_codegen_SelectionDAG, real_llvm_mc_AsmParser, real_llvm_mc_MasmParser, real_llvm_transforms_Attributor, real_llvm_transforms_WholeProgramDevirt

~~~text
--target=armv7l-tizen-linux-gnueabi --sysroot={sysroot_armv7l} -resource-dir={resource_dir} -g2 -gdwarf-4 -fexceptions -frecord-gcc-switches -fasynchronous-unwind-tables -g -O3 -fomit-frame-pointer -fPIC -fno-semantic-interposition -fvisibility-inlines-hidden -ffunction-sections -fdata-sections -O3 -std=c++17 -fno-exceptions -funwind-tables -x c++-cpp-output
~~~

**Group 4.** real_llvm_sema_SemaExprCXX, real_llvm_sema_SemaStmt

~~~text
--target=armv7l-tizen-linux-gnueabi --sysroot={sysroot_armv7l} -resource-dir={resource_dir} -g2 -gdwarf-4 -fexceptions -frecord-gcc-switches -fasynchronous-unwind-tables -g -O3 -fomit-frame-pointer -fPIC -fno-semantic-interposition -fvisibility-inlines-hidden -ffunction-sections -fdata-sections -fno-common -O3 -std=c++17 -fno-exceptions -funwind-tables -x c++-cpp-output
~~~

**Group 5.** real_aarch64_llvm_arm_ARMISelLowering, real_aarch64_llvm_arm_ARMTargetTransformInfo

~~~text
--target=aarch64-tizen-linux-gnu --sysroot={sysroot_aarch64} -resource-dir={resource_dir} -g2 -gdwarf-4 -fexceptions -frecord-gcc-switches -fasynchronous-unwind-tables -g -O3 -fomit-frame-pointer -fPIC -fno-semantic-interposition -fvisibility-inlines-hidden -ffunction-sections -fdata-sections -O3 -std=c++17 -fvisibility=hidden -fno-exceptions -funwind-tables -x c++-cpp-output
~~~

**Group 6.** real_aarch64_llvm_codegen_MachinePipeliner, real_aarch64_llvm_codegen_SelectionDAG, real_aarch64_llvm_mc_AsmParser, real_aarch64_llvm_mc_MasmParser, real_aarch64_llvm_transforms_Attributor, real_aarch64_llvm_transforms_WholeProgramDevirt

~~~text
--target=aarch64-tizen-linux-gnu --sysroot={sysroot_aarch64} -resource-dir={resource_dir} -g2 -gdwarf-4 -fexceptions -frecord-gcc-switches -fasynchronous-unwind-tables -g -O3 -fomit-frame-pointer -fPIC -fno-semantic-interposition -fvisibility-inlines-hidden -ffunction-sections -fdata-sections -O3 -std=c++17 -fno-exceptions -funwind-tables -x c++-cpp-output
~~~

**Group 7.** real_aarch64_llvm_sema_SemaExprCXX, real_aarch64_llvm_sema_SemaStmt

~~~text
--target=aarch64-tizen-linux-gnu --sysroot={sysroot_aarch64} -resource-dir={resource_dir} -g2 -gdwarf-4 -fexceptions -frecord-gcc-switches -fasynchronous-unwind-tables -g -O3 -fomit-frame-pointer -fPIC -fno-semantic-interposition -fvisibility-inlines-hidden -ffunction-sections -fdata-sections -fno-common -O3 -std=c++17 -fno-exceptions -funwind-tables -x c++-cpp-output
~~~
