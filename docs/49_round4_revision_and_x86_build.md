# 49 归档修复第四轮修订与 x86 完整构建

日期：2026-10-13。开场基准 `89ad784b10fb033aff4820dd9bb94d9e2fbe1f3d`。
**进行中：第零步与第一步 PASS；发布模式实物认证、全量回归及构建尚未执行。** 此文件随阶段完成更新，不把计划记为实测。

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

第一步已完成；第二至第七步待执行。

## 3. Source 修订与测试

按用户裁决新增无调试分支：原命令完全没有调试选项时，不补 `-g/-gdwarf-4`，IR 有 `!llvm.dbg.cu` 即拒绝；有调试选项仍要求末项 DWARF4，未分类/部分选项拒绝。旧带调试后端列表保持原文，是否全库字节不变仍待下一阶段回归。（证据：tools/test_archive_review_round4_continue.py 的固定字面量测试；[生产 diff](49_x86_source.diff)、[ARM diff](49_arm_source.diff)。）

ARM 原生入口改 `--native-limit-shell /emul/usr/bin/sh`，解析实际 ELF、名称、SHA；不带 H/S 设置 AS/core 软硬值，再分别读回；错误 exit125。用 `/usr/bin/env -u BASH_ENV -u ENV` 在启动 shell 前清除环境脚本入口，`exec "$@"` 保留参数边界。只包装三工具与 limits 探针。LLVM 主版本仍为22；取消 ARM 22.1.8 精确钉死，三工具完整版本仍须一致，函数特征串仍逐字核验，差异要求按升级手册重做 docs/44 §2 普查。两份 Commands 类与开场原文逐字一致。Source 记录工具 resolved_path；Rnew 的 clang 别名核查通过，spec 别名修改待第三步生成候选时执行。

| 测试环境 | 结果 | 证据 |
|---|---|---|
| 宿主 | 147/147 PASS；原134项随接口裁决调整，新增13项；bash/dash/sh 三种实际执行 | E/host-tests-result.json |
| ARM32 根 | 143 PASS + 3 环境不适用 + 1 既有 QEMU AS 发现；无新增失败 | E/root-suite-classified.json、root-suite-raw.json |
| 根内解释器 | Python 3.14.2；临时 /proc 已卸载 | E/root-stage-result.json、armv7l-mount-{before,during,after}.txt |

3项环境不适用仍是缺 GNU time 的两个实验辅助测试与 x86 as --64 夹具；AS已知发现仍是 `test_limits_accounting_and_no_external_time`。没有放宽 Source 门禁。
根内小试辅助检查保留 PPid 树采样，修正 limits 行尾空白匹配；入口改 sh、新证据目录，尚未运行其实际小试。本次是事前授权修改，未使用失败后的辅助重试额度。完整 diff：[根内辅助驱动](49_root_helper.diff)。

- `tools/llvm_static_archives_source.py` SHA256 `c43523c0ce04fc3310e670ff97823db8260c21250dc3172575a18db56500082e`。
- `tools/llvm_static_archives_arm_trial.py` SHA256 `1bac8db608554b35d16482711bf0667f1fbee8d60c6fc52f0f448d240ffaa9e4`。
