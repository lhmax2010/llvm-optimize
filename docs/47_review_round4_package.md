# 47 第三轮评审修订与第四轮材料

日期：2026-10-12（Asia/Shanghai）。开场提交 `bda33ec60e694aeb92e71ac0444901350567a8ba`。

**当前完成第零步：完整性核查 PASS。事实核查、Source 修订、测试、四次全量转换、根内小试与新补丁尚未执行，不用历史通过代替本轮认证。**

## 0. 范围、证据与资源规则

W=`/home/linhao/Toolchain/development/llvm-optimize`；本轮 E=`W/temp/review-round4-20261012`，下述 temp 证据仅在本机。依用户裁决：轻量阶段准入6 GiB，全量转换10 GiB；不足每5分钟复查、最多60分钟。运行中scope 18 GiB、swap0、nice15/ionice3、30秒采样，宿主可用低于2 GiB即中止。Commands、356627 spec、W/llvm与配置不改；不做完整RPM构建、不推Gerrit。后续仅授权四个小spec实验。

宿主 `mmap_min_addr` 沿用先前GBS设置；需要恢复时用户执行 `sudo sysctl -w vm.mmap_min_addr=65536`，重启也会恢复。本轮尚未挂载/proc。

## 1. 第零步完整性

| 项目 | 结果 | E内证据 |
|---|---|---|
| 截止点 | reflog 2026-10-12 19:35:32+08；本地HEAD/origin/main/远端main均bda33ec，无新提交 | integrity/main-*.stdout、remote-head.stdout |
| 主仓库全量status | 4,995,871行；非忽略差异只有用户gbs_llvm.conf | integrity/main-status-all.stdout |
| W/llvm | HEAD f111162e94aa48ed367c9d2c039456c70e7160ae；sandbox/fangyu.he/llvm_optmize；仅原三处并发改动 | integrity/llvm-*.stdout |
| 保护文件 | 69个HEAD blob全同；spec SHA95887b2d…、配置28f1caf9…均相符 | integrity/head-blob-check.json、input-integrity.jsonl |
| 修改时间全集 | 104条全部归因，未知0；15个权限盲目录免密只读补扫，新增0 | metadata-attribution.json、privileged-newer-command.json |
| 输入内容 | x86 225+ARM32 210+AArch64 212=647档；工具/代码/补丁等合计672项SHA PASS | input-integrity-result.json、input-integrity.jsonl |

归因类别：本轮锁/证据52、Git目录元数据15、上一收尾提交对象13、Codex自动树/refs15、上一提交/推送元数据9。自动树与HEAD的唯一差异是已登记配置，其blob SHA28f1caf9…一致。没有回滚或修复任何历史文件。本阶段未动用辅助脚本重试条款。原始find exit1仅来自15个权限盲目录，已补扫补齐；不把不完整扫描本身记为PASS。（证据：metadata-gate.json、git-object-attribution.json、codex-ref-attribution.json。）

## 2. 本轮实际资源

| 阶段 | 准入GiB | 启动可用GiB | scope峰GiB | 结果 |
|---|---:|---:|---:|---|
| input-integrity-scope | 6 | 13.937710 | 1.200821 | exit 0，采样回收 |
| integrity-scope | 6 | 9.839542 | 5.730644 | exit 0，采样回收 |
| metadata-completion-scope | 6 | 10.701515 | 0.016010 | exit 0，采样回收 |

均未触发OOM或宿主2GiB保护；scope峰包含文件缓存。原始命令、日志、采样与退出状态见各scope目录。

## 3. 后续状态

第一至第七步尚未执行。开场Source仍为014fd32f…（x86）/c3edada0…（ARM），候选补丁仍为1293f698…/aab2cfd1…。发布模式仅做事实核查，策略是否调整待PM；本材料将随每阶段提交更新。第四轮评审、x86完整构建、ARM第二段均未完成。
