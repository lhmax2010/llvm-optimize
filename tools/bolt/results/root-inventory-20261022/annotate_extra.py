#!/usr/bin/env python3
from pathlib import Path
import json
D=Path(__file__).resolve().parent; a=json.loads((D/'annotations.json').read_text())
def add(p,source,purpose,ref,protect,dep,reason,assets='先保留原包/清单/日志；未逐一认证可独立迁出的二进制',owner='main patch / hybrid 线'):
 a[p]={'source':source,'purpose':purpose,'ref':ref,'protected':protect,'dependency':dep,'advice':'保留','reason':reason,'assets':assets,'owner':owner}
add('/var/tmp/llvm-optimize-x86-archivefix-20261013','cb679968 + PS3 3731eda7 / PS2 4c36e899','2026-10-14 正式交接树','main/docs/49_x86_build_resume_result.md:238; bolt/docs/bolt/16_fallback_and_config_install.md:8','是，普通clang/22RPM/review49不可改','new-rpm-repo与RPM硬链接；候选/重链/性能资料依赖；无活动overlay','原树虽禁重新配置，仍是后备输入与基准','A1–A4、A12；22RPM和review49证据整体保留','main 已交接给 BOLT')
add('/var/tmp/llvm-optimize-x86-archivefix-20261013-new-rpm-repo','cb679968 + PS3/PS2','22RPM临时消费者仓库','main/docs/49_x86_build_resume_result.md:167','普通RPM链接副本，谨慎保留','与上项RPMS共inode；只删其中一份不释放RPM数据','消费者复验入口；不能重复计算可回收量')
for n,source,purpose,ref in [('llvm-optimize-arm-c1-20261010','cb679968','ARM32增量树/原生工具','main/docs/40_arm_archive_conversion_stage1.md:874; main/docs/46_review_round3_package.md:17'),('llvm-optimize-arm-tls-aarch64-20261010','cb679968','AArch64增量树/原生工具','main/docs/40_arm_archive_conversion_stage1.md:2185; main/docs/46_review_round3_package.md:18'),('llvm-optimize-arm-stage1-20261010','cb679968 仓库环境','C0/阶段1消费者根','main/docs/40_arm_archive_conversion_stage1.md:628; main/docs/40_arm_archive_conversion_stage1.md:991'),('llvm-optimize-llvm-strip-tizen-20261009','docs38 LLVM包，f111162e配方','bfd/lld消费者根','main/docs/38_llvm_strip_x86_64.md:325'),('llvm-optimize-archivefix-v2-tizen-20261009','docs35 LLVM包，f111162e配方','v2 bfd/lld消费者根','main/docs/36_archive_fix_tizen_consumers.md:19'),('llvm-optimize-archivefix-v2-final-20261009','f111162e + docs35','独立安装幂等性验收根','main/docs/35_archive_fix_v2_final.md:208')]:
 add('/var/tmp/'+n,source,purpose,ref,'是，main 历史根/证据，未解除','ARM32/64根供转换后续验证；旧消费者根不等于完整LLVM构建' if 'arm-' in n else 'main 归档安装/消费者证据；未发现活动overlay','本轮优先可重建BOLT副本，保留主线根')
H='/home/linhao/'
external={
 'temp/llvm':('未知，未在本仓库找到准确提交出处','独立LLVM源码副本','main/docs/41_disk_inventory.md:326'),
 'clang-toolchains':('未知','clangd21/22及源码/工具安装','main/docs/41_disk_inventory.md:171'),
 'lld_base_1193909_work':('QB1193909与reference包；准确源码提交未找到','三架构包和readelf对照资料','main/docs/41_disk_inventory.md:326'),
 'Toolchain/LLVM_Upgrade/llvm':('未知；旧调查有未提交修改，本轮不推定clean','LLVM升级工作树','main/docs/41_disk_inventory.md:204'),
 'Toolchain/tizen-docs-release':('未知','工具链文档与源码发布副本','main/docs/41_disk_inventory.md:191'),
 'Toolchain/development/llvm':('当前源码库；本轮不作为构建根使用','W外独立LLVM源码库','main/docs/41_disk_inventory.md:326'),
 'Toolchain/development/llvm_inline_development/codes/llvm':('未知；M1项目','M1 LLVM源码','main/docs/41_disk_inventory.md:164'),
 'Toolchain/development/llvm_inline_development/tmp':('未知；M1项目','多套GBS/验证临时目录的父目录','main/docs/41_disk_inventory.md:161'),
 'Toolchain/development/llvm_inline_development/docs/llvm_optimize_docs/verification/port22/artifacts':('未知；M1项目','port22验证载荷','main/docs/41_disk_inventory.md:162'),
 'Toolchain/development/llvm_inline_development_second/codes/llvm':('未知；另一M1工作树','LLVM源码','main/docs/41_disk_inventory.md:234'),
 'Toolchain/development/llvm_image_analysis/work/sparse':('不适用：镜像稀疏实验','中间tar/镜像证据','main/docs/41_disk_inventory.md:197'),
 'Toolchain/development/llvm_image_analysis/work/signature':('不适用：镜像签名实验','镜像/归档证据','main/docs/41_disk_inventory.md:198')}
for p,(s,pu,r) in external.items():
 add(H+p,s,pu,r,'非本BOLT线；是否正式保护未知','未证明其他项目已不再依赖；源码库不可当缓存删','归属/复用需求未核定，交用户与所属项目确认',owner='其他 LLVM / 工具链项目')
for p in json.loads((D/'all-unit-paths.json').read_text()):
 if p in a:continue
 if 'GBS-' in p:
  add(p,'准确源码SHA未知，不能用目录日期替代','历史C99/MLGO/M1 GBS根','main/docs/41_disk_inventory.md:139; main/docs/41_disk_inventory.md:160','所属其他项目；保护状态未知','可能共享硬链接缓存；无活动overlay证据','保留，待该项目确认用途',owner='其他 LLVM / 工具链项目')
 else:
  add(p,'未知，未查到准确源提交','临时导出或LLVM/GBS相关目录','本轮只读路径清单；文档无准确对应','未知','未证明没有下游引用','用途未核定，不建议据名称直接删除',owner='未确定')
(D/'annotations.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
