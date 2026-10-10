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

## §21：ARM32根内99项测试逐项分类

Python3.14.2；临时/proc可见；只跑一次。原始unittest为95 PASS、1 FAIL、3 ERROR，按预注册PM例外分类通过。原始逐项记录及错误全文：`temp/arm-source-root-probes-20261010/armv7l-test-records.json`；分类断言：`root-tests-classified.json`。未跳过/改写那四项测试。

| 测试完整ID | 原始结果 | 本任务分类 |
|---|---|---|
| `test_static_archives_source.SourceCommandsTests.test_first_failure_cancels_and_reaps` | PASS | PASS |
| `test_static_archives_source.SourceCommandsTests.test_limits_accounting_and_no_external_time` | FAIL | 已知环境发现：QEMU未施加AS |
| `test_static_archives_source.SourceCommandsTests.test_wait4_is_per_child_under_four_workers` | PASS | PASS |
| `test_static_archives_source_v2.CancellationTests.test_g_failed_leader_descendants_are_killed` | PASS | PASS |
| `test_static_archives_source_v2.CancellationTests.test_g_handler_only_records_signal` | PASS | PASS |
| `test_static_archives_source_v2.CancellationTests.test_g_signal_on_success_cannot_return_pass` | PASS | PASS |
| `test_static_archives_source_v2.CancellationTests.test_g_success_and_timeout_reaped` | PASS | PASS |
| `test_static_archives_source_v2.FilesystemTests.test_d_native_pass_thin_and_other_rejected` | PASS | PASS |
| `test_static_archives_source_v2.FilesystemTests.test_e_evidence_reset_and_unsafe_rejected` | PASS | PASS |
| `test_static_archives_source_v2.FilesystemTests.test_e_native_install_skip_and_cleanup` | PASS | PASS |
| `test_static_archives_source_v2.FilesystemTests.test_f_atomic_copy_preserves_mode` | PASS | PASS |
| `test_static_archives_source_v2.FilesystemTests.test_f_failed_copy_preserves_original_and_records_failure` | PASS | PASS |
| `test_static_archives_source_v2.FilesystemTests.test_h_tools_version_and_cache` | PASS | PASS |
| `test_static_archives_source_v2.FilesystemTests.test_l_cleanup_keeps_json_only` | PASS | PASS |
| `test_static_archives_source_v2.PolicyTests.test_a_classifies_operands_without_replaying_lto` | PASS | PASS |
| `test_static_archives_source_v2.PolicyTests.test_a_unknown_and_missing_operands_fail` | PASS | PASS |
| `test_static_archives_source_v2.PolicyTests.test_b_last_values_and_defaults` | PASS | PASS |
| `test_static_archives_source_v2.PolicyTests.test_b_uncertified_last_values_fail` | PASS | PASS |
| `test_static_archives_source_v2.PolicyTests.test_c_four_type_features_fail` | PASS | PASS |
| `test_static_archives_source_v2.PolicyTests.test_c_normal_ir_and_zero_split_lto_pass` | PASS | PASS |
| `test_static_archives_source_v2.PolicyTests.test_i_missing_strong_fails_check` | PASS | PASS |
| `test_static_archives_source_v2.PolicyTests.test_i_strong_preserved_weak_missing_recorded` | PASS | PASS |
| `test_static_archives_source_v2.PolicyTests.test_j_triple_mismatch` | PASS | PASS |
| `test_static_archives_source_v2.PolicyTests.test_k_python39_and_chunk_digest` | PASS | PASS |
| `test_convert_static_archives.ConversionPolicyTests.test_absolute_allocated_relocation_rejected_but_debug_excluded` | PASS | PASS |
| `test_convert_static_archives.ConversionPolicyTests.test_gnu_packing_keeps_duplicate_names_and_order` | PASS | PASS |
| `test_convert_static_archives.ConversionPolicyTests.test_native_machine_and_wrong_machine` | PASS | PASS |
| `test_convert_static_archives.ConversionPolicyTests.test_pic_is_explicit_and_no_lto` | PASS | PASS |
| `test_convert_static_archives.ConversionPolicyTests.test_pie_and_static_distinguished` | PASS | PASS |
| `test_convert_static_archives.ConversionPolicyTests.test_recorded_backend_options_are_required_and_last_flag_wins` | PASS | PASS |
| `test_convert_static_archives.ConversionPolicyTests.test_unsupported_flags_fail` | PASS | PASS |
| `test_convert_static_archives.ConversionPolicyTests.test_wrong_target_fails` | PASS | PASS |
| `test_inspect_llvm_archives.ArchiveTests.test_64bit_index` | PASS | PASS |
| `test_inspect_llvm_archives.ArchiveTests.test_actual_member_magic` | PASS | PASS |
| `test_inspect_llvm_archives.ArchiveTests.test_corrupt_input_rejected` | PASS | PASS |
| `test_inspect_llvm_archives.ArchiveTests.test_duplicate_member_names_are_not_collapsed` | PASS | PASS |
| `test_inspect_llvm_archives.ArchiveTests.test_gnu_long_name` | PASS | PASS |
| `test_inspect_llvm_archives.ArchiveTests.test_mixed_archive_partial_index` | PASS | PASS |
| `test_inspect_llvm_archives.ArchiveTests.test_native_index_and_debug_sections` | PASS | PASS |
| `test_inspect_llvm_archives.ArchiveTests.test_order_and_not_just_count` | PASS | PASS |
| `test_inspect_llvm_archives.ArchiveTests.test_thin_never_reads_external_members` | PASS | PASS |
| `test_inspect_llvm_archives.CensusGateTests.test_runtime_native_pass_and_bitcode_stop` | PASS | PASS |
| `test_native_archive_commands.ResourcePolicyTests.test_actual_limits_and_monitor_cleanup` | ERROR | 环境不适用 |
| `test_native_archive_commands.ResourcePolicyTests.test_compile_limit_does_not_leak_to_link` | PASS | PASS |
| `test_native_archive_commands.ResourcePolicyTests.test_failure_stops_following_commands` | ERROR | 环境不适用 |
| `test_simulate_native_archive_strip.StripGateTests.test_corruption_rejected` | PASS | PASS |
| `test_simulate_native_archive_strip.StripGateTests.test_full_mapping_and_duplicate_members_pass` | PASS | PASS |
| `test_verify_native_archive_consumers.DriverGuardTests.test_all_lto_plugin_forms_rejected` | PASS | PASS |
| `test_verify_native_archive_consumers.DriverGuardTests.test_loader_cc1_regression_rejected` | PASS | PASS |
| `test_verify_native_archive_consumers.DriverGuardTests.test_object_only_bfd_and_lld` | PASS | PASS |
| `test_compare_native_conversion_options.StructuralComparisonTests.test_backend_flags_include_sections_and_exclude_lto` | PASS | PASS |
| `test_compare_native_conversion_options.StructuralComparisonTests.test_duplicate_sections_are_counted` | PASS | PASS |
| `test_compare_native_conversion_options.StructuralComparisonTests.test_equal_counts_do_not_hide_wrong_sections_or_visibility` | PASS | PASS |
| `test_compare_native_conversion_options.StructuralComparisonTests.test_sections_symbols_visibility_and_relocations` | ERROR | 环境不适用 |
| `test_arm_archive_trial.DispatchTests.test_arm_exact_options_and_cross_target_rejection` | PASS | PASS |
| `test_arm_archive_trial.DispatchTests.test_arm_ir_and_explicit_abi` | PASS | PASS |
| `test_arm_archive_trial.DispatchTests.test_arm_pic_rel_and_aarch64_rela` | PASS | PASS |
| `test_arm_archive_trial.DispatchTests.test_narrow_absolute_writable_rejected` | PASS | PASS |
| `test_arm_archive_trial.DispatchTests.test_original_functions_are_identical` | PASS | PASS |
| `test_arm_archive_trial.DispatchTests.test_x86_never_reaches_arm` | PASS | PASS |
| `test_arm_archive_trial.LayoutTests.test_absolute_has_no_section_and_remains_absolute` | PASS | PASS |
| `test_arm_archive_trial.LayoutTests.test_common_has_no_section_and_is_not_absolute` | PASS | PASS |
| `test_arm_archive_trial.LayoutTests.test_common_mapping_never_matches_real_section_65522` | PASS | PASS |
| `test_arm_archive_trial.LayoutTests.test_decoded_65521_is_real_section_not_absolute` | PASS | PASS |
| `test_arm_archive_trial.LayoutTests.test_extended_count_names_and_symbol_index` | PASS | PASS |
| `test_arm_archive_trial.LayoutTests.test_invalid_links_tables_payloads_and_truncation` | PASS | PASS |
| `test_arm_archive_trial.LayoutTests.test_missing_duplicate_badcount_extended_indexes` | PASS | PASS |
| `test_arm_archive_trial.LayoutTests.test_other_reserved_symbol_sections_rejected` | PASS | PASS |
| `test_arm_archive_trial.LayoutTests.test_rel_rela_architecture_matrix` | PASS | PASS |
| `test_arm_archive_trial.LayoutTests.test_relocation_offset_and_symbol_boundaries` | PASS | PASS |
| `test_arm_archive_trial.MappingReaderTests.test_mapping_duplicate_section_names_preserved` | PASS | PASS |
| `test_arm_archive_trial.MappingReaderTests.test_mapping_missing_and_out_of_bounds_rejected` | PASS | PASS |
| `test_arm_archive_trial.MappingReaderTests.test_mapping_thumb_only` | PASS | PASS |
| `test_arm_archive_trial.MappingReaderTests.test_mapping_transition_deduplicated` | PASS | PASS |
| `test_arm_archive_trial.MappingReaderTests.test_missing_differs_from_zero_and_missing_vfp_valid` | PASS | PASS |
| `test_arm_archive_trial.MappingReaderTests.test_reader_empty_no_aeabi_and_bad_format_rejected` | PASS | PASS |
| `test_arm_archive_trial.ReviewRelocationTests.test_nonalloc_known_not_counted_unknown_rejected` | PASS | PASS |
| `test_arm_archive_trial.ReviewRelocationTests.test_removed_tls_and_invalid_constants_in_all_contexts` | PASS | PASS |
| `test_arm_archive_trial.ReviewRelocationTests.test_tls_boundary_numbers` | PASS | PASS |
| `test_arm_archive_trial.ReviewRelocationTests.test_tls_literal_sets_and_disjointness` | PASS | PASS |
| `test_arm_archive_trial.ReviewRelocationTests.test_writable_instruction_absolute_vs_pointer` | PASS | PASS |
| `test_arm_archive_trial.TLSThumbTests.test_initial_exec_arm_descriptors_and_unknown_stop` | PASS | PASS |
| `test_arm_archive_trial.TLSThumbTests.test_local_exec_forbidden_even_debug_writable_and_absolute` | PASS | PASS |
| `test_arm_archive_trial.TLSThumbTests.test_module_asm_section_tracking` | PASS | PASS |
| `test_arm_archive_trial.TLSThumbTests.test_override_warning_is_a_failure` | PASS | PASS |
| `test_arm_archive_trial.TLSThumbTests.test_thumb_gate_rejects_attribute_mismatch` | PASS | PASS |
| `test_arm_archive_trial.TLSThumbTests.test_thumb_restore_and_reference_arguments` | PASS | PASS |
| `test_arm_archive_trial.TLSThumbTests.test_tls_allowed_each_type_readonly_and_writable` | PASS | PASS |
| `test_arm_archive_trial.TargetModuleTests.test_certified_function_targets_and_data_modules` | PASS | PASS |
| `test_arm_archive_trial.TargetModuleTests.test_cpu_features_tune_and_missing_groups_rejected` | PASS | PASS |
| `test_arm_archive_trial.TargetModuleTests.test_module_asm_all_other_statements_rejected` | PASS | PASS |
| `test_arm_archive_trial.TargetModuleTests.test_module_asm_exact_and_whitespace_only` | PASS | PASS |
| `test_arm_archive_trial.TargetModuleTests.test_module_asm_output_global_symbol_required` | PASS | PASS |
| `test_arm_archive_trial.TargetModuleTests.test_real_command_literals_and_assembler_escape` | PASS | PASS |
| `test_arm_archive_trial.ToolIsolationTests.test_disassembler_nm_version_mismatch` | PASS | PASS |
| `test_arm_archive_trial.ToolIsolationTests.test_matching_full_versions_and_gnu_reader` | PASS | PASS |
| `test_arm_archive_trial.ToolIsolationTests.test_non_gnu_reader_rejected` | PASS | PASS |
| `test_arm_archive_trial.ToolIsolationTests.test_x86_actual_convert_success_failure_all_arm_functions_blocked` | PASS | PASS |
| `test_arm_archive_trial.ToolIsolationTests.test_x86_fixed_constants_and_original_function_objects` | PASS | PASS |
