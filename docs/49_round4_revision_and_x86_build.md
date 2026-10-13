# 49 归档修复第四轮修订与 x86 完整构建

日期：2026-10-13。开场基准 `89ad784b10fb033aff4820dd9bb94d9e2fbe1f3d`。
**进行中：第零步完整性 PASS；其余步骤尚未执行。** 此文件随阶段完成更新，不把计划记为实测。

宿主沿用 GBS 初始化后的 mmap_min_addr；用户恢复命令：`sudo sysctl -w vm.mmap_min_addr=65536`，重启也会恢复。本轮仅临时挂载 /proc 并在退出时卸载，不推 Gerrit、不清理磁盘。

## 0. 范围与完整性

W=`/home/linhao/Toolchain/development/llvm-optimize`，E=`W/temp/review-round4-continue-20261013`。本报告 E 中的原始证据仅存本机。

| 核对 | 实测结果 | 证据 |
|---|---|---|
| 基准与远端 | HEAD、origin/main、远端 main 同为 89ad784；reflog 截止 2026-10-12 23:55:07+08 | E/integrity/main-head.stdout、remote-head.stdout、main-reflog.stdout |
| 工作树 | 主库全量 status 5,305,853 行，非忽略项仅既有 gbs_llvm.conf；W/llvm 仅既有三处并发改动 | E/integrity/*-status-all.stdout、llvm-diff.stdout |
| 新增元数据 | 82 条均归因，未知 0；15 个权限盲区免密只读补扫新增 0 | E/metadata-attribution.json、privileged-newer-command.json |
| 输入与工具 | 647 档（225/210/212）与工具、Source、补丁等合计 669 SHA 检查 PASS；HEAD blob 核对全部相符 | E/input-integrity-result.json、input-integrity.jsonl、integrity/head-blob-check.json |
| 编译器别名 | Rnew/build/bin/clang 为指向 clang-22 的软链接 | E/compiler-alias.json |

BOLT 兄弟工作树与分支按用户授权独立保留，本轮未修改。没有回滚或修复任何历史文件。

## 1. 资源与执行协议

轻量准入 6 GiB；全量转换、回归、根内试跑、完整构建准入 10 GiB；不足每 5 分钟复查，最多 60 分钟。scope MemoryMax=18 GiB、MemorySwapMax=0、nice15/ionice3、30秒采样，宿主 MemAvailable <2 GiB 中止。重阶段获取 `/home/linhao/Toolchain/development/heavy-stage.lock` 的 flock 独占，等待最多两小时，阶段结束即释放；两个项目锁贯穿任务。原始记录：E/*-scope/{admission.json,memory-summary.json}。

初次状态/元数据扫描 wall 102.802 秒、scope peak 5,572,915,200 B；归档核对结果见 E/integrity-result.json。采样与读取线程均回收。

## 2. 后续阶段登记

Source/测试修订、发布模式认证、两次 x86 回归、候选补丁、完整构建与验收、ARM 复验/根内负例、bash 检查、LLVM 23 探测及升级手册均待执行。
