#!/usr/bin/env python3
"""Human-reviewed purpose/protection references; no filesystem changes outside evidence."""
from pathlib import Path
import json
D=Path(__file__).resolve().parent;W='/home/linhao/Toolchain/development/llvm-optimize';T=W+'/temp/'
# source is recipe identity, not evidence-repository HEAD.
a={}
def put(name,source,purpose,ref,protect='历史证据；本轮未解除保护',dependency='未发现活动 overlay；不等于不存在脚本引用',advice='保留',reason='保留复核证据，先由所属主线确认',assets='先留日志/manifest/SHA；未逐一认证独有二进制'):
 a[T+name]={'source':source,'purpose':purpose,'ref':ref,'protected':protect,'dependency':dependency,'advice':advice,'reason':reason,'assets':assets,'owner':'main patch / hybrid 线' if not name.startswith('bolt-v4') else 'BOLT 线'}
put('gbs-root-x86_64-debuginfo-j4-v2','f111162e 配方','R1 普通/BOLT v2 旧树','bolt/docs/bolt/02_inventory.md:21; main/docs/41_disk_inventory.md:69','是，历史认证基线','历史工具和性能资料依赖此根；A5 保留','保留','历史 llvm-bolt 1da7…与基线输入仍用于认证','A5；原生 clang/strip/resource-dir 也不要分拆')
put('gbs-root-x86_64-archivefix','f111162e + v1 归档修复','docs30 完整构建','main/docs/41_disk_inventory.md:68; main/docs/35_archive_fix_v2_final.md:55','是，docs30 根/RPM','main 归档历史验收依赖；无活动 overlay')
put('gbs-root-x86_64-archivefix-v2','f111162e + docs35/38 配方','Rnew；docs38 llvm-strip 根','main/docs/38_llvm_strip_x86_64.md:27; main/docs/52_hybrid_link_tizen_base.md:49','是，Rnew/B','D25 upper 的历史 lower；main hybrid52 工具环境；删后旧 overlay 无法重挂，hybrid 复验失去工具','保留','同时被 BOLT 演练与 main hybrid 引用','原始普通 clang、strip、资源目录；R/RPMS 是 docs38 包，非 docs35')
put('archive-index-fix-rpm-20260923','f111162e 基线','H 唯一 RPM 解包基线','main/docs/35_archive_fix_v2_final.md:28; main/docs/41_disk_inventory.md:71','是，H','静态库转换、非归档对照均引用 H','保留','不要把唯一 H 当成可重建副本','H/usr/bin/clang-22；原基线包/manifest')
put('archive-fix-v2-final-20261009','f111162e + v2','docs35 原始22RPM与证据','main/docs/38_llvm_strip_x86_64.md:27; bolt/docs/bolt/24_rebase_recertification.md:69','是，rpms-docs35','D24 payload-merged 可由其中22原件重建；先留此目录','保留','旧包已从 R/RPMS 移到此处，是来源原件','rpms-docs35 全部22RPM，不以抽出单个clang替代')
put('toolchain-archivefix-v2-final','f111162e + docs35','N 普通载荷','main/docs/35_archive_fix_v2_final.md:29; main/docs/41_disk_inventory.md:73','是，N','docs38/51 非静态库对照依赖')
put('toolchain-llvm-strip','f111162e + docs38','N38 llvm-strip 载荷','main/docs/38_llvm_strip_x86_64.md:32; main/docs/41_disk_inventory.md:74','是，N38','docs51 验证输入依赖')
put('toolchain-release-x86-20261013','cb679968 + PS3 3731eda7 / PS2 4c36e899','新普通 RPM 解包 N','main/docs/49_x86_build_resume_result.md:163','是，交接普通载荷','main 发布/消费者对照；与 var/tmp 原包关联')
put('release-x86-full-build-20261013','cb679968 + PS3/PS2','续跑监测、补丁和打包证据','main/docs/49_x86_build_continuation.md:12; bolt/docs/bolt/29_disk_footprint.md:70','是，历史峰值/交接证据','29 的582条原始 du 样本来源；供后续补测对照','保留','完整峰值下界仅此原始采样可溯源')
put('release-attribution-20261013','cb679968 + PS3/PS2','发布归因与转换证据','main/docs/49_release_attribution.md:15; main/docs/49_release_attribution.md:664')
put('arm-archive-stage1-20261010','cb679968；x86输入另承 docs35','ARM阶段1/x86转换输入','main/docs/40_arm_archive_conversion_stage1.md:55; main/docs/46_review_round3_package.md:20','是，ARM输入','后续 review3/review4 转换依赖 x86-input')
put('arm-archive-stage1-c-newrepo-20261010','cb679968','C1 导出/原仓库证据','main/docs/40_arm_archive_conversion_stage1.md:627; main/docs/40_arm_archive_conversion_stage1.md:772','是，ARM阶段证据')
put('arm-archive-tls-thumb-20261010','cb679968 输入；ARM helper 多轮修订','ARM Thumb/TLS与全量转换','main/docs/46_review_round3_package.md:22; main/docs/44_arm_source_review_round1.md:27','是，ARM输入','review3/review4 依赖 aarch64-input；VS Code 正打开子目录','保留','正在被编辑器读取，且是认证输入')
put('arm-source-root-probes-20261010','cb679968 输入；候选 helper','ARM源文件/根内探测','main/docs/46_review_round3_package.md:19','是，ARM证据')
put('review-round3-continue-20261012','cb679968 + PS3/PS2 候选','四路转换评审3','main/docs/46_review_round3_package.md:9')
put('review-round4-20261012','cb679968 + PS3/PS2 候选','四路转换评审4及停止证据','main/docs/47_review_round4_package.md:9')
put('archive-followup-review-20261014','d4dd40da，父67619ec8','归档后续评审/上传核对','main/docs/50_archive_followup_review.md:5; main/docs/50_archive_followup_review.md:49')
put('hybrid-link-20261015','cef4d90b / 同树后续6e9d4f2b','hybrid源码/配置验证','main/docs/52_hybrid_link_tizen_base.md:8; main/docs/52_hybrid_link_validation.md:5','是，当前 main 工作线','依赖 Rnew 内工具；源码仓库/申请材料不可只按 build 名删','保留','当前 hybrid 后续仍要验证')
put('hybrid-sandbox-20261019','6e9d4f2b','hybrid发布源码准备与导出','main/docs/52_hybrid_sandbox_evidence/README.md:19; main/docs/52_hybrid_link_validation.md:5','是，当前 main 工作线','新clone/upstream导出、打包指南证据','保留','近期主线发布资料')
put('llvm-optimize-intranet-20261020','6e9d4f2b','可续传源码归档准备','main/docs/llvm_optimize_intranet_fetch.md:9; main/docs/STATUS.md:7','是，当前 main 工作线','最新归档/分块/恢复校验来源','保留','main 最近完成任务仍指向这里')
put('bench_results','f111162e 历史BOLT配方','真实TU/预处理/profile/性能输入','main/docs/17_bolt_holdout.md:22; main/docs/41_disk_inventory.md:82','是，训练/留出输入','30/90对象及目标性能验证依赖','保留','输入资产不可由普通RPM恢复')
put('bolt-v4-20261013','9e5675f 当前源；多轮历史提交','BOLT 隔离源库/导出/早期草案','bolt/docs/bolt/29_disk_footprint.md:58','是，当前 BOLT 源码库','v41/llvm-source 是后续修改基点；含 Source1200','保留','不能删掉正在维护的本地源码仓库','A6；Git提交对象、patch/manifest')
for n,src,pur,ref in [('archive-fix-rebind-20260923','f111162e + 混合提案','旧profile重绑定/归档试验','main/docs/42_disk_cleanup.md:64'),('hybrid-trial-20260922','f111162e + 七文件提案','隔离旧混合试验','main/docs/22_hybrid_link_trial.md:15'),('toolchain-hybrid-trial','f111162e + 七文件提案','隔离旧混合载荷','main/docs/22_hybrid_link_trial.md:171'),('static-native-conversion-20260924','f111162e 输入；旧转换器','早期转换失败证据','main/docs/27_static_archive_native_conversion.md:25'),('archive-fix-v2-build-20260929','f111162e + v2','v2续跑/恢复证据','main/docs/35_archive_fix_v2_final.md:23'),('llvm-strip-alternative-20260929','f111162e + strip试验','替代strip证据','main/docs/42_disk_cleanup.md:53'),('llvm-strip-x86_64-20261009','f111162e + docs38','llvm-strip打包证据','main/docs/38_llvm_strip_x86_64.md:22')]:put(n,src,pur,ref)
put('bolt-v4-20261016-source-order','506dc25 → af82efed','Source无条件声明修复/解析 overlay','bolt/docs/bolt/26_source_order_parse_fix.md:1','历史源码/解析证据','不构成活动挂载；先保留报告与补丁','保留','本次优先四副本已足够，不扩大删除面')
for n,src,ref,child in [('bolt-v4-20261015-review3','ad8a2606','bolt/docs/bolt/23_closure_post_certification.md:47','payload-merged'),('bolt-v4-20261015-review4b','506dc25','bolt/docs/bolt/24_rebase_recertification.md:69','payload-merged'),('bolt-v4-20261015-validation','a1410e3d / candidate4ec07159','bolt/docs/bolt/20_object_validation_and_release.md:28','baseline-extract'),('bolt-v4-20261015-install-rehearsal','506dc25','bolt/docs/bolt/25_real_install_rehearsal.md:90','upper')]:
 put(n,src,'BOLT认证/演练证据父目录',ref,'证据保留；载荷待用户裁决','只建议处置其 '+child+'，其余全部保留','保留父目录','避免连同报告、120输入、脚本和日志一起删除','子目录提取清单见§5，其余证据不动')
 put(n+'/'+child,src,'可重建载荷副本' if child!='upper' else '已卸载 overlay 上层',ref,'本轮仅建议，尚无删除授权','原22RPM在旧根或rpms-docs35' if child!='upper' else 'lower=Rnew；删 upper 不损 lower，删 lower 则此upper无法重挂','删除（待批准）' if child!='upper' else '先抽出14文件再删除（待批准）','前三项可从受保护RPM重建' if child!='upper' else '旧中止演练场景；先保存工具/普通clang/profile及文本','保留父目录日志/清单；无独有候选已确认在此' if child!='upper' else 'A7–A11及reclaim-scenario.json的14文件')
(D/'annotations.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
