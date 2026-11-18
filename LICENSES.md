# Training inputs and dependency licenses

The source package and license information below describes the origin of the archived bytes. The licenses and notices supplied with the inputs remain applicable. Original inputs, headers and notices retain their byte contents.

## Training inputs

| Entry | File | Origin | Version | License |
|---|---|---|---|---|
| A | training-inputs/synthetic/A.cpp | Synthetic benchmark generator | seed 73419, scale 1 | Original generated fixture; no separate upstream RPM license |
| B | training-inputs/synthetic/B.cpp | Synthetic benchmark generator | seed 73419, scale 2 | Original generated fixture; no separate upstream RPM license |
| C | training-inputs/synthetic/C.cpp | Synthetic benchmark generator | seed 73419, scale 2 | Original generated fixture; no separate upstream RPM license |
| real_llvm_arm_ARMISelLowering | training-inputs/armv7l/llvm_arm_ARMISelLowering.ii | llvm (source package; LLVM or Clang translation unit) | 22.1.8 | Apache-2.0 WITH LLVM-exception |
| real_llvm_arm_ARMTargetTransformInfo | training-inputs/armv7l/llvm_arm_ARMTargetTransformInfo.ii | llvm (source package; LLVM or Clang translation unit) | 22.1.8 | Apache-2.0 WITH LLVM-exception |
| real_llvm_codegen_MachinePipeliner | training-inputs/armv7l/llvm_codegen_MachinePipeliner.ii | llvm (source package; LLVM or Clang translation unit) | 22.1.8 | Apache-2.0 WITH LLVM-exception |
| real_llvm_codegen_SelectionDAG | training-inputs/armv7l/llvm_codegen_SelectionDAG.ii | llvm (source package; LLVM or Clang translation unit) | 22.1.8 | Apache-2.0 WITH LLVM-exception |
| real_llvm_mc_AsmParser | training-inputs/armv7l/llvm_mc_AsmParser.ii | llvm (source package; LLVM or Clang translation unit) | 22.1.8 | Apache-2.0 WITH LLVM-exception |
| real_llvm_mc_MasmParser | training-inputs/armv7l/llvm_mc_MasmParser.ii | llvm (source package; LLVM or Clang translation unit) | 22.1.8 | Apache-2.0 WITH LLVM-exception |
| real_llvm_sema_SemaExprCXX | training-inputs/armv7l/llvm_sema_SemaExprCXX.ii | llvm (source package; LLVM or Clang translation unit) | 22.1.8 | Apache-2.0 WITH LLVM-exception |
| real_llvm_sema_SemaStmt | training-inputs/armv7l/llvm_sema_SemaStmt.ii | llvm (source package; LLVM or Clang translation unit) | 22.1.8 | Apache-2.0 WITH LLVM-exception |
| real_llvm_transforms_Attributor | training-inputs/armv7l/llvm_transforms_Attributor.ii | llvm (source package; LLVM or Clang translation unit) | 22.1.8 | Apache-2.0 WITH LLVM-exception |
| real_llvm_transforms_WholeProgramDevirt | training-inputs/armv7l/llvm_transforms_WholeProgramDevirt.ii | llvm (source package; LLVM or Clang translation unit) | 22.1.8 | Apache-2.0 WITH LLVM-exception |
| real_aarch64_llvm_arm_ARMISelLowering | training-inputs/aarch64/llvm_arm_ARMISelLowering.ii | llvm (source package; LLVM or Clang translation unit) | 22.1.8 | Apache-2.0 WITH LLVM-exception |
| real_aarch64_llvm_arm_ARMTargetTransformInfo | training-inputs/aarch64/llvm_arm_ARMTargetTransformInfo.ii | llvm (source package; LLVM or Clang translation unit) | 22.1.8 | Apache-2.0 WITH LLVM-exception |
| real_aarch64_llvm_codegen_MachinePipeliner | training-inputs/aarch64/llvm_codegen_MachinePipeliner.ii | llvm (source package; LLVM or Clang translation unit) | 22.1.8 | Apache-2.0 WITH LLVM-exception |
| real_aarch64_llvm_codegen_SelectionDAG | training-inputs/aarch64/llvm_codegen_SelectionDAG.ii | llvm (source package; LLVM or Clang translation unit) | 22.1.8 | Apache-2.0 WITH LLVM-exception |
| real_aarch64_llvm_mc_AsmParser | training-inputs/aarch64/llvm_mc_AsmParser.ii | llvm (source package; LLVM or Clang translation unit) | 22.1.8 | Apache-2.0 WITH LLVM-exception |
| real_aarch64_llvm_mc_MasmParser | training-inputs/aarch64/llvm_mc_MasmParser.ii | llvm (source package; LLVM or Clang translation unit) | 22.1.8 | Apache-2.0 WITH LLVM-exception |
| real_aarch64_llvm_sema_SemaExprCXX | training-inputs/aarch64/llvm_sema_SemaExprCXX.ii | llvm (source package; LLVM or Clang translation unit) | 22.1.8 | Apache-2.0 WITH LLVM-exception |
| real_aarch64_llvm_sema_SemaStmt | training-inputs/aarch64/llvm_sema_SemaStmt.ii | llvm (source package; LLVM or Clang translation unit) | 22.1.8 | Apache-2.0 WITH LLVM-exception |
| real_aarch64_llvm_transforms_Attributor | training-inputs/aarch64/llvm_transforms_Attributor.ii | llvm (source package; LLVM or Clang translation unit) | 22.1.8 | Apache-2.0 WITH LLVM-exception |
| real_aarch64_llvm_transforms_WholeProgramDevirt | training-inputs/aarch64/llvm_transforms_WholeProgramDevirt.ii | llvm (source package; LLVM or Clang translation unit) | 22.1.8 | Apache-2.0 WITH LLVM-exception |

The C++ generator supplies A, B and C without a separate upstream package. This kit records their generation parameters and makes no new upstream license grant. The other 20 files are compiler-preprocessed translation units from Tizen LLVM 22.1.8. They can include portions of the toolchain headers listed below.

## Header dependency packages

| Package | Version-release | Architecture | License field | Corresponding source |
|---|---|---|---|---|
| clang-devel | 22.1.8 | x86_64 | Apache-2.0 WITH LLVM-exception | llvm-22.1.8 source package |
| glibc-devel | 2.40-1.6 | armv7l | BSD-3-Clause and LGPL-2.1+ and LGPL-2.1+-with-GCC-exception and GPL-2.0+ | glibc-2.40-1.6.src.rpm |
| glibc-devel | 2.40-2.9 | aarch64 | BSD-3-Clause and LGPL-2.1+ and LGPL-2.1+-with-GCC-exception and GPL-2.0+ | glibc-2.40-2.9.src.rpm |
| libstdc++-devel | 14.2.0-1.15 | aarch64 | GPL-3.0-with-GCC-exception | gcc-14.2.0-1.15.src.rpm |
| libstdc++-devel | 14.2.0-1.6 | armv7l | GPL-3.0-with-GCC-exception | gcc-14.2.0-1.6.src.rpm |
| linux-glibc-devel | 6.6-1.16 | aarch64 | GPL-2.0 | linux-glibc-devel-6.6-1.16.src.rpm |
| linux-glibc-devel | 6.6-1.7 | armv7l | GPL-2.0 | linux-glibc-devel-6.6-1.7.src.rpm |

Original LLVM/Clang, glibc and GNU C++ notices appear under training-inputs/licenses after extraction. The kernel header package license field is preserved above. Individual header notices and exceptions remain in the original header bytes. The manifest records the package identity and SHA-256 of each included dependency.

## SDK prerequisites

Use the matching Tizen SDK sysroots and compiler resource directory for a live run. The archive provides the source header closure; install binary compiler-discovery and build dependencies from the pinned Tizen snapshot. The gcc package rows below identify the driver startup object the full SDK supplies. This kit contains no copies of those objects.

| Target | GCC package | Version-release | License field | Source RPM |
|---|---|---|---|---|
| armv7l | gcc | 14.2.0-1.6 | GPL-3.0+ | gcc-14.2.0-1.6.src.rpm |
| aarch64 | gcc | 14.2.0-1.15 | GPL-3.0+ | gcc-14.2.0-1.15.src.rpm |
