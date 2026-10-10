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

## §4：首轮普查后的评审采纳状态（历史）

以下表格从docs/44原样迁移，历史判定不变。

| PM项 | 裁决内容 | 本轮状态 |
|---|---|---|
| 1 | 未知重定位在非ALLOC前拒绝，统计仍只计ALLOC | 未实施，停于§3 |
| 2 | A64 TLS仅562/563/564/569；其余原ALLOW转PENDING | 未实施 |
| 3 | 按每个define精确核cpu/features/tune | 普查完成，必需属性缺失0；门禁未实施 |
| 4 | A64移除absolute317/580、allowed256 | 未实施 |
| 5 | 固定GNU readelf/LC_ALL=C；aeabi/CPU_arch；缺失None | 未实施 |
| 6 | ARM专用ELF边界/扩展索引解析，真ABS辨别 | 未实施 |
| 7 | 指令绝对重定位不因可写而放行，仅完整宽度指针例外 | 未实施 |
| 8 | ARM32 asm白名单与同名节多序列；A64任意asm拒绝 | 全集普查完成；A64有3条真实语句，与拟实施规则冲突，停止 |
| 9 | 显式拒-Wa, | 未实施 |
| 10 | ARM专用完整工具版本与GNU reader预检 | 未实施 |
| 11 | ARM32补PENDING13/17/18/19/109/165/166/167 | 未实施 |
| 12 | mtune源码注释、TARGET1严格ABS解释 | 未实施 |
| 13 | ARM summary记录纯机器码整档跳过身份 | 未实施 |

## §10：前次测试停止后的复验状态（历史）

以下表格从docs/44原样迁移，历史判定不变。

| 任务 | 本轮结果与不可外推的范围 |
|---|---|
| 宿主全套测试 | FAIL，95项中94通过；无第三次重跑 |
| ARM32根python全套测试/版本记录 | NOT RUN，宿主门禁第二次失败后停止 |
| x86 225档/3864成员/完整索引/3853flags | NOT RUN；旧§12 PASS不绑定5608aa5e新候选 |
| ARM32 210档重新转换、含asm的2成员GLOBAL符号 | NOT RUN；没有新after SHA/真实符号状态 |
| A64 212档重新转换、含asm的3成员GLOBAL符号 | NOT RUN；没有新after SHA/真实符号状态 |
| 两架构after SHA与docs/40 §12逐档相同 | UNKNOWN（未执行）；不能沿用旧消费者作为本候选认证 |
| 消费者三套与两种strip | 本轮未重跑，亦未以“SHA相同”为由沿用认证；旧证据仍仅认证1620 |
| ARM32 105/106共享库-z text、GNU/lld、dlopen | NOT RUN |
| x86最终产物的同module asm成员只读核查 | NOT RUN；按第三步停止，不声称符号存在/缺失 |

## §16：续二停止后的未执行清单（历史）

原样移出的历史表，原结果不变。

| 项目 | 本轮结果 |
|---|---|
| x86 225档/3864有序成员/完整索引/3853 flags | NOT RUN；源码隔离和99宿主测试不能代替真实回归 |
| ARM32 210档、AArch64 212档新输出全量转换 | NOT RUN；两架构after SHA与docs/40 §12是否全部相同为UNKNOWN |
| 5个白名单module asm成员的输出符号绑定/节索引 | NOT RUN / UNKNOWN；不根据原声明猜GLOBAL/UND |
| Thumb门禁本轮实际readelf路径、来源、版本 | NOT RUN；没有真实新转换调用记录，不把代码内路径当成实测 |
| 消费者三套、GNU/LLVM strip复验 | 未重跑，也未援引“after SHA相同”继承旧认证；旧证据仅适用1620 |
| ARM32 TLS105/106、bfd/lld -shared -z text、dlopen | NOT RUN |
| docs/35最终x86产物同module asm成员只读核查 | NOT RUN；实际成员/符号状态UNKNOWN，已同步docs/45 §5 |

## §15：续二根内五项问题（历史）

原样移出的历史表，原结果不变。

| 根内用例 | 原始结果 | 判定/边界 |
|---|---|---|
| test_actual_limits_and_monitor_cleanup | FileNotFoundError: `/usr/bin/time` | 环境缺依赖，无法运行；不改测试 |
| test_failure_stops_following_commands | 同上 | 环境缺依赖，无法运行；不改测试 |
| test_sections_symbols_visibility_and_relocations | `as --64 ...probe.s -o ...probe.o` exit1 | 宿主x86汇编夹具在ARM根无法运行；异常未输出所捕获stderr，精确错误文本UNKNOWN，不编造 |
| test_limits_accounting_and_no_external_time | 实际`[[-1,-1],[0,0]]`，期望`[[4294967296,4294967296],[0,0]]` | 4GiB地址空间限制未按测试期望读回；不是缺工具例外，保留FAIL |
| test_g_success_and_timeout_reaped | 实际exit=-15，期望=-9 | 超时探针由SIGTERM终止，未达到测试预期SIGKILL；原因未由本次证据确定，保留FAIL |

## §11：前次Gerrit材料身份核对（历史）

原样移出的历史表，原结果不变。

| E2下文件 | 用途 |
|---|---|
| candidate-before.py、tests-before.py | 本轮编辑前的原件副本 |
| protected-start.json、final-integrity.json | 生产Source/spec/patch/用户配置未变；候选/测试新SHA |
| iostream-evidence.json | 两ARM根头文件路径、SHA、编号摘录 |
| revision-metadata.json、source-isolation.json | diff计数/摘要、函数行号、测试名、未改函数AST核对 |
| run_tests.py、unit-tests-host.log、unit-tests-host-initial-result.json | 首轮完整命令与95项结果 |
| test-helper-correction.diff/json | 唯一辅助修正的依据与diff |
| unit-tests-host-retry.log、unit-tests-final-result.json、stop-result.json | 第二次FAIL、实际解释器、停止边界 |
| lock-acquired.json、lock-released.json、final-processes.json、final-mountinfo.txt | 独占与退出回收、无本任务残留 |
| gerrit-356639-ls-remote.* | 只读完整提交号 |
