# docs/44 逐成员普查表

本页从 [docs/44 §1](44_arm_source_review_round1.md#1-51个无函数属性成员全部无define) 原样移出完整51项表，不改历史数字与判定。证据：`temp/arm-source-review-round1-20261010/gate-result.json`。ordinal为0起，同名序号为1起。

## §1：51个无函数属性成员

| 架构 | 归档 | 成员（ordinal / 同名序号） | define数 | module asm数 |
|---|---|---|---:|---:|
| armv7l | libLLVMABI.a | `Types.cpp.o` (0 / 1) | 0 | 0 |
| armv7l | libLLVMAnalysis.a | `TFLiteUtils.cpp.o` (117 / 1) | 0 | 0 |
| armv7l | libLLVMAnalysis.a | `DevelopmentModeInlineAdvisor.cpp.o` (37 / 1) | 0 | 0 |
| armv7l | libLLVMAnalysis.a | `ModelUnderTrainingRunner.cpp.o` (88 / 1) | 0 | 0 |
| armv7l | libLLVMDWARFLinker.a | `Utils.cpp.o` (1 / 1) | 0 | 0 |
| armv7l | libLLVMDWP.a | `DWPError.cpp.o` (1 / 1) | 0 | 0 |
| armv7l | libLLVMFrontendHLSL.a | `HLSLResource.cpp.o` (2 / 1) | 0 | 0 |
| armv7l | libLLVMMC.a | `MCAsmMacro.cpp.o` (13 / 1) | 0 | 0 |
| armv7l | libLLVMOrcShared.a | `OrcRTBridge.cpp.o` (4 / 1) | 0 | 0 |
| armv7l | libLLVMPasses.a | `CodeGenPassBuilder.cpp.o` (0 / 1) | 0 | 0 |
| armv7l | libLLVMPasses.a | `OptimizationLevel.cpp.o` (1 / 1) | 0 | 0 |
| armv7l | libLLVMSandboxIR.a | `Argument.cpp.o` (0 / 1) | 0 | 0 |
| armv7l | libLLVMSandboxIR.a | `Pass.cpp.o` (7 / 1) | 0 | 0 |
| armv7l | libLLVMSupport.a | `UnicodeNameToCodepointGenerated.cpp.o` (139 / 1) | 0 | 0 |
| armv7l | libLLVMSupport.a | `RWMutex.cpp.o` (169 / 1) | 0 | 0 |
| armv7l | libLLVMSupport.a | `AutoConvert.cpp.o` (17 / 1) | 0 | 0 |
| armv7l | libLLVMSupport.a | `zOSLibFunctions.cpp.o` (174 / 1) | 0 | 0 |
| armv7l | libLLVMSupport.a | `blake3_neon.c.o` (3 / 1) | 0 | 0 |
| armv7l | libLLVMSupport.a | `ABIBreak.cpp.o` (4 / 1) | 0 | 0 |
| armv7l | libLLVMSupport.a | `MathExtras.cpp.o` (84 / 1) | 0 | 0 |
| armv7l | libLLVMVectorize.a | `InstrMaps.cpp.o` (5 / 1) | 0 | 0 |
| armv7l | libclangBasic.a | `CharInfo.cpp.o` (4 / 1) | 0 | 0 |
| armv7l | libclangRewriteFrontend.a | `RewriteModernObjC.cpp.o` (5 / 1) | 0 | 0 |
| armv7l | libclangRewriteFrontend.a | `RewriteObjC.cpp.o` (6 / 1) | 0 | 0 |
| armv7l | libclangStaticAnalyzerCore.a | `CommonBugCategories.cpp.o` (15 / 1) | 0 | 0 |
| armv7l | liblldMachO.a | `Target.cpp.o` (27 / 1) | 0 | 0 |
| aarch64 | libLLVMABI.a | `Types.cpp.o` (0 / 1) | 0 | 0 |
| aarch64 | libLLVMAnalysis.a | `TFLiteUtils.cpp.o` (117 / 1) | 0 | 0 |
| aarch64 | libLLVMAnalysis.a | `DevelopmentModeInlineAdvisor.cpp.o` (37 / 1) | 0 | 0 |
| aarch64 | libLLVMAnalysis.a | `ModelUnderTrainingRunner.cpp.o` (88 / 1) | 0 | 0 |
| aarch64 | libLLVMDWARFLinker.a | `Utils.cpp.o` (1 / 1) | 0 | 0 |
| aarch64 | libLLVMDWP.a | `DWPError.cpp.o` (1 / 1) | 0 | 0 |
| aarch64 | libLLVMFrontendHLSL.a | `HLSLResource.cpp.o` (2 / 1) | 0 | 0 |
| aarch64 | libLLVMMC.a | `MCAsmMacro.cpp.o` (13 / 1) | 0 | 0 |
| aarch64 | libLLVMOrcShared.a | `OrcRTBridge.cpp.o` (4 / 1) | 0 | 0 |
| aarch64 | libLLVMPasses.a | `CodeGenPassBuilder.cpp.o` (0 / 1) | 0 | 0 |
| aarch64 | libLLVMPasses.a | `OptimizationLevel.cpp.o` (1 / 1) | 0 | 0 |
| aarch64 | libLLVMSandboxIR.a | `Argument.cpp.o` (0 / 1) | 0 | 0 |
| aarch64 | libLLVMSandboxIR.a | `Pass.cpp.o` (7 / 1) | 0 | 0 |
| aarch64 | libLLVMSupport.a | `UnicodeNameToCodepointGenerated.cpp.o` (139 / 1) | 0 | 0 |
| aarch64 | libLLVMSupport.a | `RWMutex.cpp.o` (169 / 1) | 0 | 0 |
| aarch64 | libLLVMSupport.a | `AutoConvert.cpp.o` (17 / 1) | 0 | 0 |
| aarch64 | libLLVMSupport.a | `zOSLibFunctions.cpp.o` (174 / 1) | 0 | 0 |
| aarch64 | libLLVMSupport.a | `ABIBreak.cpp.o` (4 / 1) | 0 | 0 |
| aarch64 | libLLVMSupport.a | `MathExtras.cpp.o` (84 / 1) | 0 | 0 |
| aarch64 | libLLVMVectorize.a | `InstrMaps.cpp.o` (5 / 1) | 0 | 0 |
| aarch64 | libclangBasic.a | `CharInfo.cpp.o` (4 / 1) | 0 | 0 |
| aarch64 | libclangRewriteFrontend.a | `RewriteModernObjC.cpp.o` (5 / 1) | 0 | 0 |
| aarch64 | libclangRewriteFrontend.a | `RewriteObjC.cpp.o` (6 / 1) | 0 | 0 |
| aarch64 | libclangStaticAnalyzerCore.a | `CommonBugCategories.cpp.o` (15 / 1) | 0 | 0 |
| aarch64 | liblldMachO.a | `Target.cpp.o` (27 / 1) | 0 | 0 |

## §8：13项修订实施明细

原位置的证据说明仍保留在docs/44，以下表格逐字节迁移。

| PM项 | 本次写入内容 | 新Source证据 |
|---|---|---|
| 1 | 未知/STOP/LE检查均在非ALLOC跳过前；checked/types仅累计ALLOC | arm_pic_relocations:912起 |
| 2 | A64 TLS ALLOW精确562/563/564/569；移除的旧GD/LD/描述符片段显式PENDING | ARM_TLS_ALLOWED/LOCAL_EXEC/PENDING:783–797 |
| 3 | 每个define必须引用属性组，cpu/features/tune等于§2精确元组；无define放行 | ARM_CERTIFIED_FUNCTION_TARGET:486起；arm_function_targets:499；arm_ir_settings:706 |
| 4 | A64 absolute移除317/580、allowed移除256 | arm_pic_relocations:933–943 |
| 5 | 固定env LC_ALL=C GNU readelf -AW；aeabi与CPU_arch必需；缺项None，缺项与显式0不同 | arm_attributes:661；arm_thumb_gate:888 |
| 6 | ARM专用ELF布局/边界校验；REL/RELA、扩展数量/名称/符号索引；raw shndx==0xfff1才是真ABS；重定位offset须在目标节内 | arm_elf_layout:544；arm_symbol_section:636 |
| 7 | 指令ABS在可写ALLOC同样禁止；可写完整指针只放ARM32 2/38/55、A64 257；真ABS独立豁免 | arm_pic_relocations:947–955 |
| 8 | 两架构精确module asm白名单先于ARM32原节跟踪；同名节保留各序列；输出GLOBAL符号必需 | arm_module_asm_whitelist:526；arm_check_module_asm_symbol:650；arm_mapping_modes:863；convert:1265起 |
| 9 | -Wa,在通用-W诊断分类前显式拒绝 | arm_classify_options:430 |
| 10 | ARM专用工具完整版本匹配；dis/nm路径/SHA/版本；ARM32另验env/readelf可执行与GNU身份 | validate_arm_tools:676；convert:1210起 |
| 11 | ARM32 PENDING增13/17/18/19/109/165/166/167 | ARM_TLS_PENDING:794–797 |
| 12 | 两-mtune注释补Driver/CodeGen源码出处；TARGET1按ABS32/REL32中更严格ABS解释 | ARM_EXACT_TOKENS:375–394；arm_pic_relocations:921 |
| 13 | ARM summary增加纯机器码整档跳过的相对路径、SHA、成员数；x86不增加字段 | convert:1219–1221 |

## §9.3：新增28项测试索引

原位置的证据说明仍保留在docs/44，以下表格逐字节迁移。

| 组 | 新增测试名称（test_前缀省略）与覆盖 |
|---|---|
| TLS/重定位5项 | tls_literal_sets_and_disjointness；tls_boundary_numbers；removed_tls_and_invalid_constants_in_all_contexts；nonalloc_known_not_counted_unknown_rejected；writable_instruction_absolute_vs_pointer |
| ELF结构6项 | rel_rela_architecture_matrix；extended_count_names_and_symbol_index；decoded_65521_is_real_section_not_absolute；missing_duplicate_badcount_extended_indexes；invalid_links_tables_payloads_and_truncation；relocation_offset_and_symbol_boundaries |
| mapping/读取6项 | mapping_thumb_only；mapping_transition_deduplicated；mapping_duplicate_section_names_preserved；mapping_missing_and_out_of_bounds_rejected；reader_empty_no_aeabi_and_bad_format_rejected；missing_differs_from_zero_and_missing_vfp_valid |
| 函数/参数/asm6项 | certified_function_targets_and_data_modules；cpu_features_tune_and_missing_groups_rejected；real_command_literals_and_assembler_escape；module_asm_exact_and_whitespace_only；module_asm_all_other_statements_rejected；module_asm_output_global_symbol_required |
| 工具/x86隔离5项 | matching_full_versions_and_gnu_reader；disassembler_nm_version_mismatch；non_gnu_reader_rejected；x86_fixed_constants_and_original_function_objects；x86_actual_convert_success_failure_all_arm_functions_blocked |
