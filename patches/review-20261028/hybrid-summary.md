# Hybrid改动摘要（首次提交外部评审）

**hybrid提交6e9d4f2从未经过外部评审。** main文档里的PM裁决是内部验收，不能当作外部review通过。本材料将它作为独立0001，BOLT为其上的0002，保留两者独立Change-Id。

- 提交：6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2；父67619ec8bbbac7238a6cfc33a481ccfbcd12206f；Change-Id I28171720d5bbbf9eaf491cdafc0aee0b43f9cd06。
- x86_64开启LLVM_LINK_LLVM_DYLIB、CLANG_LINK_CLANG_DYLIB、TIZEN_HYBRID_LINK；BUILD_SHARED_LIBS和unified LLVM driver仍OFF。
- clang、lld、llvm-ar及它们的别名继续静态链接LLVM/Clang组件；其它适用工具保留上游共享接口。不是“所有其它目标都必须动态”：上游强制静态的tblgen、llvm-config、llvm-exegesis、工具私有归档/构建工具保持原行为。
- AddLLVM.cmake新增按最终consumer的TIZEN_STATIC_LLVM属性选择组件或共享LLVM的接口；AddClang/AddLLD调用该接口，三个driver显式选择静态。没有全局替换其它消费者的依赖，也不改ARM配方、优化参数、static-devel/Source1005。
- 目的：避免大量工具重复静态嵌入LLVM，缩小构建树和RPM，同时保留三个核心驱动的静态组件链接方式。

## 本地验证与边界

main/docs/53第7节的最终PM裁决是PASS（附例外），第1–6节保留原始未裁决结果；请结合阅读。

- 完整构建22个二进制RPM+1源码RPM；188预期目标中183原始PASS、4个非默认且不安装的测试/示例N/A、AnnotateFunctions.so因--as-needed无libLLVM NEEDED但加载实测PASS（接受例外）。不写成188个严格同一规则PASS。
- 14个脚本缺python/git/libscanbuild运行依赖；与全静态基线脚本逐字节相同，内部裁决为原有环境问题、另行跟踪。可执行工具库解析无缺失。
- 90对象逐字节验证、LLVM/Clang开发包示例配置/编译/运行、导出引用存在性、225静态归档转换/索引有原始证据。
- 采样峰值66.696GiB；历史全静态+BOLT224.718GiB，差158.022GiB，但有76.3分钟采样空档和不同构建条件，不能当成严格控制变量的因果减幅。历史BOLT自有约4.347GiB单列。
- 22二进制RPM合计约7.990→1.449GiB，减6.541GiB（81.87%）；对照含历史全静态+BOLT，详见53逐包表。ARM/AArch64没有在该任务完整构建，只做导出/解析。

- [53_hybrid_local_validation.md raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/main/docs/53_hybrid_local_validation.md)
- [evidence-manifest.json raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/main/docs/53_hybrid_local_validation_evidence/evidence-manifest.json)
- [linkage-188-classification.json raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/main/docs/53_hybrid_local_validation_evidence/linkage-188-classification.json)
- [linkage-188-supplemental.json raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/main/docs/53_hybrid_local_validation_evidence/linkage-188-supplemental.json)
- [annotate-plugin-smoke-corrected.json raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/main/docs/53_hybrid_local_validation_evidence/annotate-plugin-smoke-corrected.json)
- [runtime-baseline-comparison.json raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/main/docs/53_hybrid_local_validation_evidence/runtime-baseline-comparison.json)
- [objects-result.json raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/main/docs/53_hybrid_local_validation_evidence/objects-result.json)
- [sdk-result.json raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/main/docs/53_hybrid_local_validation_evidence/sdk-result.json)
- [archives-result.json raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/main/docs/53_hybrid_local_validation_evidence/archives-result.json)

[main证据目录（GitHub tree，目录不是raw文件）](https://github.com/lhmax2010/llvm-optimize/tree/main/docs/53_hybrid_local_validation_evidence)
