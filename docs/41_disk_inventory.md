# /home 磁盘与 Session / 项目只读盘点

盘点日期：2026-10-09；开始 **23:18:08 +08:00**，本版汇总于 **2026-10-09T23:59:50+08:00**。
本报告只提供待用户逐项确认的建议。**没有删除、移动、压缩任何被盘点资产，没有修改权限、系统配置或其他项目文件；没有启动构建。** 本轮写入仅为本报告、STATUS 和 `temp/` 下的盘点元数据/辅助脚本。

**已量化：可删类 6.646 GiB；只删大载荷保留日志类 173.887 GiB，合计 180.533 GiB。** 这里的“可删”也是建议，尚未获得本轮逐项删除确认。另有一个当前未启用的 64 GiB swap 文件，归属/后续用途未确证，列为“需用户判断”，不计入上述合计。

## 1. 范围、计量与缺口

| 项目 | 实测 / 边界 |
|---|---|
| 文件系统 | `/home` → `/dev/sda1`，ext4；`findmnt -R /home` 未列出子挂载；所有 du 带 `-x`，不跟随符号链接。 |
| 起始 df | 总量 `1967844950016 B`，已用 `1823859675136 B`，普通用户可用 `43948662784 B` = **40.931 GiB**，Use% 98%。厂商十进制 TB 与 GiB 不混用。 |
| 一级范围 | `/home/linhao`；`/home/shared` 与 `/home/lost+found` 无读取权限，无法统计，不填 0。 |
| 权限 | 两次不同范围的 `sudo -n du` 都返回 `sudo: a password is required`；未输入密码、未绕过权限。带 `†` 的行有不可读后代，所示为可读部分下界。 |
| 限时 | 全盘前两段 du 每次 900s、第三段480s；本项目 temp 单独 600s；ARM 根 240s；保留项 90s；缓存 180s；单仓库 Git status 25s。超时保留已完成目录，下一段按排除清单跳过它们。 |
| 大小 | `du -B1` 的实际分配块，按 2^30 换算。不是逻辑文件长度。各次扫描不是原子快照；跨扫描的共享 inode 可能重复计入目录账，**不把主表相加当作精确释放量**。 |
| 释放量 | §4 对候选逐文件记录 dev/inode/nlink/st_blocks，同一 inode 只计一次，只有全部硬链接都在该候选集合内才计为可释放。目录元数据未计；若将来仍有打开的文件描述符，实际回收可能延迟，执行前仍须复核。 |
| 修改时间 | 主表为 `du --time` 的树内最大 mtime；不是创建时间、不是 Session 完成时间。少数 M1 树含 **2029-01-01** 文件时间，照录，不能据此判断仍在运行。 |
| Git | `GIT_OPTIONAL_LOCKS=0`，不刷新索引写盘；检查 tracked 与 untracked。超时/报错一律 UNKNOWN；非Git根的内嵌仓库未穷举。clean 不等于远端备份完备或没有独有提交。 |
| 活动进程 | 仅记录 `/proc/*/cwd`、进程名与PID，不采命令行/环境。观察到 LogAnalysisSkill 的 bash/claude；297 个 PID 不可读或已退出。没有把“未观察到”当作全机无运行任务的证明。 |

`W = /home/linhao/Toolchain/development/llvm-optimize`；`~ = /home/linhao`。会话解析只选择 cwd、ID、时间、索引标题；不提取、不保存或发布消息正文、工具参数、凭据或令牌字段。原始会话不会提交到 GitHub。

扫描退出状态：第一段900s rc=124，第二段900s rc=124；第三段在480s限时内走完剩余可读范围，rc=1仅因权限错误。本项目temp、ARM根均rc=1（权限），保留项单独统计rc=0。完成记录见completion.json。前两段被跳过的已完成目录清单均落盘；没有未报告的超时目录被算作0。

完成范围：主表列出已统计到的 ≥5 GiB 目录，止于可辨识的仓库、构建根或实验范围；本项目所有一级 temp 证据目录（包括 <5 GiB）及指定保留项也列入。父目录与子目录的“进一步定位”不重复计入主表。小于5GiB的普通用户目录未逐项展开；权限盲区无法保证没有≥5GiB目录。

## 2. Session 对应：已证实的是关联，不是全部创建者

共读取 **567 条会话元数据记录**：Codex 129、Claude 11及其8份子agent记录、Kimi Code 84、旧Kimi 115、Gemini 220。它们不是567个独立任务：Gemini记录的 `sessionId` 全为通用值 `a2a-server`，必须用会话文件名区分；旧Kimi没有可用索引标题，其中112条仅通过工作目录哈希与已知路径匹配，仍属候选关联。已删除或不在本机的Session不可恢复。

下表是主表所用关联索引。起止均为**首条元数据 / 最后记录活动时间**，不宣称任务已完成。目录被报告引用可确认项目用途；cwd 相同、日期接近、名字含 codex/kimi 等都不能单独证明具体创建者。尤其本项目现存主执行 Session 始于9月29日，不能把9月16–28日目录的创建归到它名下。

| 代号 | Agent / Session ID | 记录起–末（+08:00） | 工作目录 / 可确认任务 | 归属强度 |
|---|---|---|---|---|
| S01 | codex `01a0a8f6-2b80-7031-98a3-84575e630d24` | 2026-09-29 22:43 → 2026-10-09 23:21 | `~/Toolchain/development/llvm-optimize`；llvm-optimize：仓库/构建/归档修复持续线；本次Session | cwd与报告关联；早期目录创建者UNKNOWN |
| S02 | codex `019eac4d-132e-79e3-bb81-159426003d85` | 2026-06-09 20:13 → 2026-06-18 18:55 | `~/Toolchain/development/MLGO`；MLGO：Tizen GBS / ARM native MLGO可行性 | cwd+MLGO/REPORT明确引用共享根 |
| S03 | codex `019f49cf-f9a3-7f11-945e-b88d0d9aead9` | 2026-07-10 10:16 → 2026-07-24 16:40 | `~/Toolchain/development/MLGO`；MLGO/llvm_optimize_docs：C99 inline R3–R7验证 | 任务标题与日期/报告关联 |
| S04 | codex `019fb29c-a399-7b01-9fdf-cdadcc6b6cf7` | 2026-07-30 18:40 → 2026-09-29 22:48 | `~/Toolchain/development/llvm_inline_development`；llvm_inline_development：M1主线开发/验证 | cwd+M1交接；未逐文件证明创建者 |
| S05 | codex `01a08f16-d474-7fa0-b5f4-82791e224712` | 2026-09-11 14:10 → 2026-09-14 19:16 | `~/Toolchain/plan_evaluation`；plan_evaluation：Chromium-EFL编译参数与吞吐调查 | cwd+WORKSPACE_STATE |
| S05 | codex `019f5aa6-de24-7630-9505-88f13af7eca0` | 2026-07-13 16:45 → 2026-07-24 15:17 | `~/Toolchain/plan_evaluation`；plan_evaluation：C++ ABI传播图证据采集 | 较早同工作区；不混同上条任务 |
| S07 | codex `01a11138-5ffa-7990-8725-da7187f69909` | 2026-10-06 20:37 → 2026-10-08 12:12 | `~/Toolchain/development/llvm_image_analysis`；llvm_image_analysis：mic打包失败/稀疏归档实验 | cwd+docs/status、实验报告 |
| S08 | codex `019f1c4c-3a40-77f1-8ffd-41daecc96ae7` | 2026-07-01 14:09 → 2026-07-01 14:50 | `~/temp/llvm`；~/temp/llvm：旧LLVM源码上传 | 精确cwd；后续用途未确证 |
| S09 | codex `01a0b2b5-92ee-78d0-9227-6a339c5a07b0` | 2026-09-18 12:10 → 2026-09-18 12:31 | `~/Toolchain/codes`；Toolchain/codes：DALi事件与无障碍API核查 | 容器cwd关联；api仓库创建者UNKNOWN |
| S09 | codex `019fd4f3-9c6b-7593-95c9-4fefaef4bf18` | 2026-08-06 10:42 → 2026-08-06 10:49 | `~/Toolchain/codes`；Toolchain/codes：平台包依赖排查 | 容器cwd关联 |
| S13 | codex `019e16eb-d1d7-7ea2-91be-796cc8e77bfc` | 2026-10-08 17:50 → 2026-10-09 18:46 | `~/Toolchain/development/LogAnalysisSkill`；LogAnalysisSkill：开发/发布线，仍有交互进程 | cwd与进程元数据 |
| S13 | claude `290d4284-3bdf-4a43-9154-f8563c1d5280` | 2026-08-06 11:20 → 2026-10-09 18:30 | `~/Toolchain/development/LogAnalysisSkill`；LogAnalysisSkill：Claude任务标题UNKNOWN | 仅cwd/时间；未取正文 |
| S14 | codex `019f3be2-d53d-7440-87ea-c0d394e6acf0` | 2026-07-07 17:22 → 2026-08-31 15:47 | `~/Toolchain/glibc`；Toolchain/glibc：内存优化方案可行性审计 | 精确cwd |
| S14 | codex `019f3ca1-080b-7451-83d4-fdd770fa30d0` | 2026-07-07 20:50 → 2026-09-15 20:06 | `~/Toolchain/glibc`；Toolchain/glibc：glibc memopt评审 | 精确cwd |
| S06 | Gemini `a2a-server`（非唯一）；文件 `session-2026-08-26T06-39-a2a-serv.jsonl`<br>`session-2026-08-26T06-38-a2a-serv.jsonl`<br>`session-2026-08-26T06-41-a2a-serv.jsonl`；共3条 | 2026-08-26 14:38 → 2026-08-26 14:41 | `~/Toolchain/LLVM_Upgrade`；任务标题UNKNOWN | 精确cwd；不能唯一指定创建Session |
| S11 | Gemini `a2a-server`（非唯一）；文件 `session-2026-08-17T09-12-a2a-serv.jsonl`<br>`session-2026-08-26T08-53-a2a-serv.jsonl`<br>`session-2026-08-26T08-55-a2a-serv.jsonl`<br>`session-2026-08-26T08-52-a2a-serv.jsonl`<br>`session-2026-08-26T08-54-a2a-serv.jsonl`；共6条 | 2026-08-17 16:59 → 2026-08-26 16:55 | `~/Toolchain/remove-debuginfo`；任务标题UNKNOWN | 精确cwd；不能唯一指定创建Session |
| S12 | Gemini `a2a-server`（非唯一）；文件 `session-2026-08-21T13-27-a2a-serv.jsonl`<br>`session-2026-08-21T13-25-a2a-serv.jsonl`<br>`session-2026-08-21T13-24-a2a-serv.jsonl`；共3条 | 2026-08-21 21:24 → 2026-08-21 21:27 | `~/Toolchain/development/llvm_inline_development_second`；任务标题UNKNOWN | 精确cwd；不能唯一指定创建Session |
| S10 | codex `01a0aa09-4057-7bb2-bf06-1a43e8e96c49` | 2026-09-16 19:45 → 2026-09-27 16:41 | `~/Downloads`；多项目下载/评审，具体大文件任务UNKNOWN | cwd关联，不证明文件由该会话生成 |
| S10 | claude `82756f3a-8c91-40fe-b82b-339350297298` | 2026-09-16 20:35 → 2026-09-16 22:17 | `~/Downloads`；多项目下载/评审，具体大文件任务UNKNOWN | cwd关联，不证明文件由该会话生成 |

本项目另有评审关联 Session：Codex `01a0c2d3-a36a-7c33-98ee-1e0d4a21420e`（9/21）、`01a0c2ec-862d-77c2-90a4-1332ed066bb2`（9/21–9/28），Claude `5e8aa240-5caa-4416-a0c4-218f8c1eb336`（9/21–9/28），Kimi `session_f269fe27-3a22-4400-8ad1-bd0abf4c9b2b`（索引标题为评审）。它们不能被当作构建资产创建者。完整元数据路径见§7；报告不展开无关会话任务正文。

## 3. 主表：按项目分组，组内大小降序

建议含义：**可删**＝已定位为旧纯载荷且日志不在其中，仍等待确认；**只删大载荷保留日志**＝只考虑§4清单，禁止整目录删除；**保留**＝指定保留/在用输入/源码或证据；**需用户判断**＝归属、作废状态或备份不足。`†`表示统计有权限缺口。

### llvm-optimize

| 路径 | GiB | 树内最近mtime | Session / 内容 | Git状态 | 证据/输入引用 | 建议与理由 |
|---|---:|---|---|---|---|---|
| `W/temp/gbs-root-x86_64-baseline` | 208.859† | 2026-09-17 11:17 | S01（关联；创建者未逐目录确证）；GBS构建根 | 产物/忽略目录；非独立Git根 | docs/13:41,279（首轮构建/OOM现场） | **需用户判断**：旧实验/历史现场仍被引用；没有确认作废全部内容，不按目录日期删除 |
| `W/temp/gbs-root-x86_64-archivefix` | 172.910† | 2026-09-29 13:25 | S01（关联；创建者未逐目录确证）；GBS构建根 | 产物/忽略目录；非独立Git根 | docs/30；docs/38 §0.2 第3类 | **只删大载荷保留日志**：docs/38尚未执行的候选；仅§4已量化二进制清单，日志/JSON/脚本/源码保留 |
| `W/temp/gbs-root-x86_64-debuginfo-j4-v2` | 172.727† | 2026-09-18 12:40 | S01（关联；创建者未逐目录确证）；GBS构建根 | 产物/忽略目录；非独立Git根 | docs/13、docs/15；本任务保留边界 | **保留**：docs/13基线R0与RPM，后续比较依赖 |
| `W/temp/gbs-root-x86_64-archivefix-v2` | 70.971† | 2026-10-09 21:37 | S01（关联；创建者未逐目录确证）；GBS构建根 | 产物/忽略目录；非独立Git根 | docs/39_arm_archive_conversion_feasibility.md:19；docs/38_llvm_strip_x86_64.md:27 | **保留**：Rnew及构建树，ARM/x86回归输入；用户指定保留 |
| `W/temp/archive-index-fix-rpm-20260923` | 50.906 | 2026-09-23 23:15 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/STATUS.md:154；docs/38_llvm_strip_x86_64.md:31 | **保留**：包含H（唯一基线内容），用户指定保留 |
| `W/temp/gbs-root-x86_64-hybrid-trial` | 50.169† | 2026-09-23 17:39 | S01（关联；创建者未逐目录确证）；GBS构建根 | 产物/忽略目录；非独立Git根 | docs/24；STATUS开头（隔离） | **保留**：docs/24隔离现场；本轮只做目录统计 |
| `W/temp/toolchain-archivefix-v2-final` | 46.299 | 2026-10-09 15:09 | S01（关联；创建者未逐目录确证）；RPM解包/工具链 | 产物/忽略目录；非独立Git根 | docs/38_llvm_strip_x86_64.md:30；docs/36_archive_fix_tizen_consumers.md:17 | **保留**：N；非静态库逐字节对照基准 |
| `W/temp/toolchain-llvm-strip` | 46.256 | 2026-10-09 21:08 | S01（关联；创建者未逐目录确证）；RPM解包/工具链 | 产物/忽略目录；非独立Git根 | docs/38_llvm_strip_x86_64.md:32 | **保留**：N38；最新llvm-strip RPM解包 |
| `W/temp/llvm-strip-alternative-20260929` | 27.924 | 2026-09-29 21:43 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/33；docs/38 §0.2 第2类 | **只删大载荷保留日志**：docs/38尚未执行的候选；仅§4已量化二进制清单，日志/JSON/脚本/源码保留 |
| `W/temp/archive-fix-rebind-20260923` | 22.625 | 2026-09-23 15:26 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/23–24（竞争会话线索，非最终认证证据） | **需用户判断**：旧实验/历史现场仍被引用；没有确认作废全部内容，不按目录日期删除 |
| `W/temp/archive-fix-v2-build-20260929` | 18.778 | 2026-10-08 22:16 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/34；docs/38 §0.2 第2类 | **只删大载荷保留日志**：docs/38尚未执行的候选；仅§4已量化二进制清单，日志/JSON/脚本/源码保留 |
| `W/temp/archive-fix-v2-final-20261009` | 10.339 | 2026-10-09 19:05 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/STATUS.md:13；docs/STATUS.md:201 | **保留**：docs/35证据与rpms-docs35 |
| `W/temp/llvm-strip-x86_64-20261009` | 9.473 | 2026-10-09 21:39 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/STATUS.md:18；docs/STATUS.md:20 | **保留**：docs/38构建/运行库验证证据 |
| `W/temp/gbs-root-hq-consumer-lld` | 9.356† | 2026-09-29 21:39 | S01（关联；创建者未逐目录确证）；GBS构建根 | 产物/忽略目录；非独立Git根 | 直接路径引用未检出；属本项目证据台账，当前用途需确认 | **需用户判断**：旧实验/历史现场仍被引用；没有确认作废全部内容，不按目录日期删除 |
| `W/temp/gbs-root-hq-consumer-bfd` | 8.894† | 2026-09-29 19:25 | S01（关联；创建者未逐目录确证）；GBS构建根 | 产物/忽略目录；非独立Git根 | 直接路径引用未检出；属本项目证据台账，当前用途需确认 | **需用户判断**：旧实验/历史现场仍被引用；没有确认作废全部内容，不按目录日期删除 |
| `W/temp/bench_results` | 7.284 | 2026-09-22 02:03 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/STATUS.md:132；docs/STATUS.md:134 | **保留**：真实TU、profile/基准JSON与诊断输入，不整目录删除 |
| `W/llvm` | 6.891 | 2026-10-09 23:08 | S01（关联）；LLVM源码/Git | 有：1已跟踪 / 0未跟踪项 | STATUS §1；llvm-source-status.txt | **保留**：W原件及spec本地并发修改；不能作为临时产物清理 |
| `W/temp/static-native-conversion-20260924` | 6.307 | 2026-09-24 01:18 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/27–28：旧转换结果作废 | **需用户判断**：旧实验/历史现场仍被引用；没有确认作废全部内容，不按目录日期删除 |
| `W/temp/static-native-conversion-v2-20260924/conversion/archives` | 6.161 | 2026-09-24 14:35 | S01（关联；早期创建ID UNKNOWN）；仅225个.a的产物树 | 产物/忽略目录；非独立Git根 | docs/28；docs/38 §0.2 第2类 | **可删**：本轮为删除建议，仍须用户确认；docs/38已列为旧载荷；日志位于树外 |
| `W/temp/toolchain-hybrid-trial` | 5.754 | 2026-09-22 21:56 | S01（关联；创建者未逐目录确证）；RPM解包/工具链 | 产物/忽略目录；非独立Git根 | docs/22、docs/24 | **需用户判断**：旧实验/历史现场仍被引用；没有确认作废全部内容，不按目录日期删除 |
| `W/temp/hybrid-trial-20260922` | 5.720 | 2026-09-22 22:12 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/22 | **需用户判断**：旧实验/历史现场仍被引用；没有确认作废全部内容，不按目录日期删除 |
| `W/temp/gbs-root-archive-consumer-bfd` | 4.347† | 2026-09-27 21:46 | S01（关联；创建者未逐目录确证）；GBS构建根 | 产物/忽略目录；非独立Git根 | docs/36_archive_fix_tizen_consumers.md:18；docs/30_archive_fix_full_build.md:322 | **保留**：docs/30测试根；docs/36原快照缓存来源 |
| `W/temp/gbs-root-archive-consumer-lld` | 4.347† | 2026-09-27 21:52 | S01（关联；创建者未逐目录确证）；GBS构建根 | 产物/忽略目录；非独立Git根 | docs/36_archive_fix_tizen_consumers.md:18；docs/30_archive_fix_full_build.md:322 | **保留**：docs/30测试根；docs/36原快照缓存来源 |
| `W/temp/bolt-measurement-20260918` | 3.670 | 2026-09-21 19:34 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/21_spec_integration_v3.md:15；docs/20_spec_integration_v2.md:1164 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/toolchain-baseline` | 2.840 | 2026-09-17 13:49 | S01（关联；创建者未逐目录确证）；RPM解包/工具链 | 产物/忽略目录；非独立Git根 | docs/26_archive_index_fix.md:53；docs/25_archive_index_fix.md:24 | **保留**：历史基线工具链与基准输入 |
| `W/temp/static-native-conversion-v2-20260924（不含 conversion/archives）` | 2.428 | 2026-09-24 15:25 | S01（关联）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/28；docs/38 §0.2 第2类 | **保留**：保留该证据目录其余内容，尤其summary/命令/日志 |
| `W/temp/llvm-archivefix-trial` | 2.419 | 2026-10-09 19:07 | S01（关联；创建者未逐目录确证）；源码工作树 | UNKNOWN（Git超时/报错） | docs/38_llvm_strip_x86_64.md:26；docs/35_archive_fix_v2_final.md:24 | **保留**：当前试验源码工作树，保留修改与共享Git依赖 |
| `W/temp/llvm-hybrid-trial` | 2.419 | 2026-09-22 20:26 | S01（关联；创建者未逐目录确证）；源码工作树 | UNKNOWN（Git超时/报错） | docs/22_hybrid_link_trial.md:15；docs/22_hybrid_link_trial.md:45 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/archive-fix-full-build-20260927` | 2.316 | 2026-09-27 21:59 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/STATUS.md:164；docs/STATUS.md:165 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/archive-fix-v2-20260929` | 1.871 | 2026-09-29 11:02 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/STATUS.md:174；docs/34_archive_fix_v2_build.md:26 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/static-native-conversion-v3-20260924（不含 stripped/archives）` | 1.351 | 2026-09-24 15:48 | S01（关联）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/29；docs/38 §0.2 第2类 | **保留**：保留该证据目录其余内容，尤其summary/命令/日志 |
| `W/temp/bolt-aarch64-v2-20260921` | 0.917 | 2026-09-21 20:58 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/23_archive_fix_and_profile_rebind.md:23；docs/21_spec_integration_v3.md:16 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/spec-v3-20260922` | 0.564 | 2026-09-22 17:27 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/STATUS.md:139；docs/STATUS.md:140 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/static-native-conversion-v3-20260924/stripped/archives` | 0.485 | 2026-09-24 15:29 | S01（关联；早期创建ID UNKNOWN）；仅225个.a的产物树 | 产物/忽略目录；非独立Git根 | docs/29；docs/38 §0.2 第2类 | **可删**：本轮为删除建议，仍须用户确认；docs/38已列为旧载荷；日志位于树外 |
| `W/temp/bolt-final-20260918` | 0.440 | 2026-09-18 21:00 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/21_spec_integration_v3.md:16；docs/20_spec_integration_v2.md:309 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/archive-fix-20260923` | 0.403 | 2026-09-23 13:38 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/23_archive_fix_and_profile_rebind.md:22；docs/23_archive_fix_and_profile_rebind.md:145 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/baseline-resume-20260917` | 0.366 | 2026-09-17 14:31 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/STATUS.md:124；docs/34_archive_fix_v2_build.md:324 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/bolt-holdout-20260920` | 0.284 | 2026-09-20 15:42 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/17_bolt_holdout.md:21；docs/17_bolt_holdout.md:22 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/spec-integration-v2-20260921` | 0.238 | 2026-09-21 18:41 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/20_spec_integration_v2.md:1159；docs/20_spec_integration_v2.md:1160 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/archive-profile-rebind-20260923` | 0.144 | 2026-09-23 13:32 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/STATUS.md:150；docs/STATUS.md:151 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/archive-fix-tizen-consumers-20261009` | 0.111 | 2026-10-09 17:06 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/STATUS.md:222；docs/38_llvm_strip_x86_64.md:25 | **保留**：docs/36证据与107包Base本地仓库 |
| `W/temp/llvm-strip-submission-20261009` | 0.101 | 2026-10-09 21:30 | S01（关联；创建者未逐目录确证）；源码工作树 | clean（含未跟踪检查） | docs/38_llvm_strip_x86_64.md:378 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/llvm-archivefix-submission-v2-20261009` | 0.101 | 2026-10-09 16:58 | S01（关联；创建者未逐目录确证）；源码工作树 | clean（含未跟踪检查） | docs/36_archive_fix_tizen_consumers.md:20 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/llvm-archivefix-submission-20260928` | 0.082 | 2026-09-28 10:39 | S01（关联；创建者未逐目录确证）；源码工作树 | 有：2已跟踪 / 0未跟踪项 | docs/31_archive_fix_submission.md:10 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/llvm-archivefix-v2-apply-check` | 0.082 | 2026-09-29 10:39 | S01（关联；创建者未逐目录确证）；源码工作树 | UNKNOWN（Git超时/报错） | docs/32_archive_fix_v2.md:266 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/spec-review-20260921` | 0.079 | 2026-09-21 17:03 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/21_spec_integration_v3.md:18；docs/20_spec_integration_v2.md:50 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/target-recipe-policy-check-20261009` | 0.066 | 2026-10-09 17:33 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/STATUS.md:16；docs/STATUS.md:232 | **保留**：docs/37配方认证证据 |
| `W/temp/disk-inventory-20261009` | 0.063 | 2026-10-09 23:36 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | 直接路径引用未检出；属本项目证据台账，当前用途需确认 | **保留**：本报告元数据与只读统计输出 |
| `W/temp/snapshot-archive` | 0.025 | 2026-09-17 08:42 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/19_spec_integration_v2.md:164；docs/13_baseline_build.md:37 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/baseline-build-preflight` | 0.025 | 2026-09-16 22:59 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | 直接路径引用未检出；属本项目证据台账，当前用途需确认 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/bolt-feasibility-20260918` | 0.017 | 2026-09-18 11:46 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/25_archive_index_fix.md:26；docs/14_bolt_feasibility.md:18 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/archive-fix-verification-20260923-173328` | 0.010 | 2026-09-23 17:46 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/STATUS.md:152；docs/24_archive_fix_verification.md:24 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/archive-fix-submission-20260928` | 0.009 | 2026-09-28 10:42 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/STATUS.md:169；docs/31_archive_fix_submission.md:87 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/baseline-build-20260917` | 0.007 | 2026-09-17 11:38 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/30_archive_fix_full_build.md:39；docs/30_archive_fix_full_build.md:405 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/arm-archive-feasibility-20261009` | 0.004 | 2026-10-09 23:09 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/STATUS.md:22；docs/STATUS.md:257 | **保留**：docs/39调查与后续ARM输入 |
| `W/temp/gbs-root-x86_64-debuginfo-j4` | 0.003 | 2026-09-17 11:55 | S01（关联；创建者未逐目录确证）；GBS构建根 | 产物/忽略目录；非独立Git根 | 直接路径引用未检出；属本项目证据台账，当前用途需确认 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/build-config-audit` | 0.003 | 2026-09-16 19:24 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/10_tizen_llvm_build_config.md:14；docs/10_tizen_llvm_build_config.md:15 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/baseline-preflight-20260917` | 0.002 | 2026-09-17 08:42 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/13_baseline_build.md:38；docs/13_baseline_build.md:131 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/toolchain-runtime-baseline` | 0.001 | 2026-09-17 12:02 | S01（关联；创建者未逐目录确证）；RPM解包/工具链 | 产物/忽略目录；非独立Git根 | docs/38_llvm_strip_x86_64.md:274；docs/35_archive_fix_v2_final.md:286 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/toolchain-archivefix` | 0.001 | 2026-10-09 19:05 | S01（关联；创建者未逐目录确证）；RPM解包/工具链 | 产物/忽略目录；非独立Git根 | docs/38_llvm_strip_x86_64.md:55；docs/33_llvm_strip_alternative.md:20 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/spec-integration-20260920` | 0.000 | 2026-09-20 16:41 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/18_spec_integration.md:24；docs/18_spec_integration.md:686 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/snapshot-resolution-20260917` | 0.000 | 2026-09-17 11:24 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/13_baseline_build.md:36 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/final-calibration-prereg-20260921` | 0.000 | 2026-09-22 02:08 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/20_spec_integration_v2.md:1132；docs/20_spec_integration_v2.md:1142 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/foreign-artifacts` | 0.000 | 2026-09-23 17:39 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/25_archive_index_fix.md:60；docs/24_archive_fix_verification.md:25 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/archive-index-fix-20260923` | 0.000 | 2026-09-23 22:38 | S01（关联；创建者未逐目录确证）；试验/报告证据（含载荷） | 产物/忽略目录；非独立Git根 | docs/STATUS.md:153；docs/25_archive_index_fix.md:21 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |
| `W/temp/gbs-root-llvm-strip-alternative` | 0.000 | 2026-09-29 21:42 | S01（关联；创建者未逐目录确证）；GBS构建根 | 产物/忽略目录；非独立Git根 | docs/33_llvm_strip_alternative.md:26 | **保留**：报告/脚本/原始证据；没有整目录作废依据 |

### MLGO / C99 inline早期验证

| 路径 | GiB | 树内最近mtime | Session / 内容 | Git状态 | 证据/输入引用 | 建议与理由 |
|---|---:|---|---|---|---|---|
| `~/Toolchain/development/MLGO/llvm_optimize_docs` | 53.603 | 2026-07-30 16:51 | S02/S03；源码、M0G/R3/R4等验证资产 | 非独立Git根；内嵌仓库未穷举 | MLGO/REPORT.md:10–19；llvm_optimize_docs/codex-verification-r4-results-20260714/REPORT.md:26–42 | **需用户判断**：保留历史记录；载荷是否仍用于后续工作须项目负责人确认 |
| `~/GBS-ROOT-TOOLCHAIN-LLVM-R4-RETRY-20260715` | 23.486† | 2026-07-15 13:17 | S03（报告+cwd关联）；GBS构建根/缓存/RPM | 非独立Git根；内嵌仓库未穷举 | ~/Toolchain/development/MLGO/llvm_optimize_docs/codex-verification-r4-results-20260714/REPORT.md:38 | **需用户判断**：存在历史引用或归属未明；根内特权路径有统计缺口，不能认定废弃 |
| `~/Toolchain/development/MLGO/llvm_mlgo` | 18.421 | 2026-07-31 14:27 | S02/S03；源码、M0G/R3/R4等验证资产 | UNKNOWN（Git超时/报错） | MLGO/REPORT.md:10–19；llvm_optimize_docs/codex-verification-r4-results-20260714/REPORT.md:26–42 | **需用户判断**：保留历史记录；载荷是否仍用于后续工作须项目负责人确认 |
| `~/GBS-ROOT-TOOLCHAIN-GCC-R4-20260714` | 9.238† | 2026-07-15 11:38 | S03（报告+cwd关联）；GBS构建根/缓存/RPM | 非独立Git根；内嵌仓库未穷举 | ~/Toolchain/development/llvm_inline_development/docs/llvm_optimize_docs/verification/EXTERNAL_LINKS_REMOVED.md:7；~/Toolchain/development/llvm_inline_development/docs/llvm_optimize_docs/verification/EXTERNAL_LINKS_REMOVED.md:8 | **需用户判断**：存在历史引用或归属未明；根内特权路径有统计缺口，不能认定废弃 |
| `~/GBS-ROOT-TOOLCHAIN-GCC-R3-1R-20260713` | 9.237† | 2026-07-13 17:12 | S03（报告+cwd关联）；GBS构建根/缓存/RPM | 非独立Git根；内嵌仓库未穷举 | ~/Toolchain/development/MLGO/llvm_optimize_docs/codex-verification-r3-1r-results-20260713/REPORT.md:22；~/Toolchain/development/MLGO/llvm_optimize_docs/codex-verification-r3-1r-results-20260713/REPORT.md:35 | **需用户判断**：存在历史引用或归属未明；根内特权路径有统计缺口，不能认定废弃 |
| `~/GBS-ROOT-TOOLCHAIN-GCC-R3-1R` | 9.219† | 2026-07-10 17:59 | S03（报告+cwd关联）；GBS构建根/缓存/RPM | 非独立Git根；内嵌仓库未穷举 | ~/Toolchain/development/MLGO/llvm_optimize_docs/codex-verification-r3-1r-results-20260710/REPORT.md:22；~/Toolchain/development/MLGO/llvm_optimize_docs/codex-verification-r3-1r-results-20260710/REPORT.md:34 | **需用户判断**：存在历史引用或归属未明；根内特权路径有统计缺口，不能认定废弃 |
| `~/Toolchain/development/MLGO/llvm` | 6.604 | 2026-07-31 14:25 | S02/S03；源码、M0G/R3/R4等验证资产 | clean（含未跟踪检查） | MLGO/REPORT.md:10–19；llvm_optimize_docs/codex-verification-r4-results-20260714/REPORT.md:26–42 | **需用户判断**：保留历史记录；载荷是否仍用于后续工作须项目负责人确认 |
| `~/Toolchain/development/MLGO（不含上述独立子目录）` | 5.515 | 2026-07-31 14:27 | S02/S03；源码、M0G/R3/R4等验证资产 | 非独立Git根；内嵌仓库未穷举 | MLGO/REPORT.md:10–19；llvm_optimize_docs/codex-verification-r4-results-20260714/REPORT.md:26–42 | **需用户判断**：同项目其余内容；每个已完成子目录均小于5GiB |
| `~/GBS-ROOT-TOOLCHAIN-LLVM-R4-20260714` | 5.180† | 2026-07-15 11:15 | S03（报告+cwd关联）；GBS构建根/缓存/RPM | 非独立Git根；内嵌仓库未穷举 | 所查STATUS/报告未找到直接路径引用；仍需确认 | **需用户判断**：存在历史引用或归属未明；根内特权路径有统计缺口，不能认定废弃 |

### Chromium工具链评估

| 路径 | GiB | 树内最近mtime | Session / 内容 | Git状态 | 证据/输入引用 | 建议与理由 |
|---|---:|---|---|---|---|---|
| `~/Toolchain/plan_evaluation/chromium-efl` | 54.721 | 2026-09-14 18:07 | S05；Chromium源码/工作树（部分含构建输出） | UNKNOWN（Git超时/报错） | handover/chromium_tizen_llvm_compile_time/WORKSPACE_STATE.md:3–15；docs/12复用生成器/工具 | **保留**：保留历史记录；载荷是否仍用于后续工作须项目负责人确认 |
| `~/Toolchain/plan_evaluation/chromium-efl-spike-libcxx-wt` | 34.891 | 2026-07-22 20:24 | S05；Chromium源码/工作树（部分含构建输出） | UNKNOWN（Git超时/报错） | handover/chromium_tizen_llvm_compile_time/WORKSPACE_STATE.md:3–15；docs/12复用生成器/工具 | **保留**：保留历史记录；载荷是否仍用于后续工作须项目负责人确认 |
| `~/Toolchain/plan_evaluation/chromium-efl-spike-libcxx` | 21.337 | 2026-07-14 12:58 | S05；Chromium源码/工作树（部分含构建输出） | UNKNOWN（Git超时/报错） | handover/chromium_tizen_llvm_compile_time/WORKSPACE_STATE.md:3–15；docs/12复用生成器/工具 | **保留**：保留历史记录；载荷是否仍用于后续工作须项目负责人确认 |

### C99 inline M1

| 路径 | GiB | 树内最近mtime | Session / 内容 | Git状态 | 证据/输入引用 | 建议与理由 |
|---|---:|---|---|---|---|---|
| `~/Toolchain/development/llvm_inline_development/tmp/GBS-ROOT-TIZEN-UNIFIED-LLVM` | 29.312† | 2029-01-01 08:00 | S04；GBS根/验证载荷与证据 | 非独立Git根；内嵌仓库未穷举 | m1-c99-inline-handover-v16.md:3–5,49–80（关闭版仍列待办）；docs/README.md:40–53 | **需用户判断**：保留历史记录；载荷是否仍用于后续工作须项目负责人确认 |
| `~/Toolchain/development/llvm_inline_development/tmp（不含上述独立子目录）` | 24.210† | 2029-01-01 08:00 | S04；GBS根/验证载荷与证据 | 非独立Git根；内嵌仓库未穷举 | m1-c99-inline-handover-v16.md:3–5,49–80（关闭版仍列待办）；docs/README.md:40–53 | **需用户判断**：同项目其余内容；每个已完成子目录均小于5GiB |
| `~/Toolchain/development/llvm_inline_development/docs/llvm_optimize_docs` | 20.186 | 2026-09-29 12:27 | S04；GBS根/验证载荷与证据 | 非独立Git根；内嵌仓库未穷举 | m1-c99-inline-handover-v16.md:3–5,49–80（关闭版仍列待办）；docs/README.md:40–53 | **需用户判断**：保留历史记录；载荷是否仍用于后续工作须项目负责人确认 |
| `~/Toolchain/development/llvm_inline_development/codes（不含上述独立子目录）` | 12.317 | 2026-09-28 18:20 | S04；源码工作树 | 非独立Git根；内嵌仓库未穷举 | m1-c99-inline-handover-v16.md:3–5,49–80（关闭版仍列待办）；docs/README.md:40–53 | **需用户判断**：同项目其余内容；每个已完成子目录均小于5GiB |
| `~/Toolchain/development/llvm_inline_development/codes/llvm` | 6.874 | 2026-09-28 18:20 | S04；源码工作树 | UNKNOWN（Git超时/报错） | m1-c99-inline-handover-v16.md:3–5,49–80（关闭版仍列待办）；docs/README.md:40–53 | **需用户判断**：保留历史记录；载荷是否仍用于后续工作须项目负责人确认 |

### 本机工具链安装 / 项目未确证

| 路径 | GiB | 树内最近mtime | Session / 内容 | Git状态 | 证据/输入引用 | 建议与理由 |
|---|---:|---|---|---|---|---|
| `~/clang-toolchains/llvm-build.swap` | 64.000 | 2026-07-09 12:24 | UNKNOWN；未启用的swap文件 | 非独立Git根；内嵌仓库未穷举 | inactive-swap.json | **需用户判断**：当前/proc/swaps及fstab均无此路径；未来是否复用UNKNOWN |
| `~/clang-toolchains（不含llvm-build.swap）` | 7.819 | 2026-07-17 15:47 | UNKNOWN；clangd 21/22、源码、构建/日志 | 非独立Git根；内嵌仓库未穷举 | 直接目录元数据；未查到文档路径引用 | **需用户判断**：工具安装与未启用swap分开；未查到明确所属项目 |

### GBS历史根 / 创建项目未确证

| 路径 | GiB | 树内最近mtime | Session / 内容 | Git状态 | 证据/输入引用 | 建议与理由 |
|---|---:|---|---|---|---|---|
| `~/GBS-ROOT-TIZEN-UNIFIED-LLVM-UPGRADE` | 30.617† | 2026-07-08 21:49 | UNKNOWN；GBS构建根/缓存/RPM | 非独立Git根；内嵌仓库未穷举 | 所查STATUS/报告未找到直接路径引用；仍需确认 | **需用户判断**：存在历史引用或归属未明；根内特权路径有统计缺口，不能认定废弃 |
| `~/GBS-ROOT-LLVM-MLGO` | 16.059† | 2026-07-17 14:47 | UNKNOWN（仅名称有MLGO，不能确认创建者）；GBS构建根/缓存/RPM | 非独立Git根；内嵌仓库未穷举 | 所查STATUS/报告未找到直接路径引用；仍需确认 | **需用户判断**：存在历史引用或归属未明；根内特权路径有统计缺口，不能认定废弃 |

### 平台源码工作区

| 路径 | GiB | 树内最近mtime | Session / 内容 | Git状态 | 证据/输入引用 | 建议与理由 |
|---|---:|---|---|---|---|---|
| `~/Toolchain/codes/api` | 17.854 | 2026-08-06 10:41 | S09；Git源码集合 | clean（含未跟踪检查） | Toolchain/codes/README.md；git-status.json（集合内多仓库dirty） | **保留**：保留历史记录；载荷是否仍用于后续工作须项目负责人确认 |
| `~/Toolchain/codes（不含上述独立子目录）` | 9.558 | 2026-09-18 12:34 | S09；Git源码集合 | 非独立Git根；内嵌仓库未穷举 | Toolchain/codes/README.md；git-status.json（集合内多仓库dirty） | **保留**：同项目其余内容；每个已完成子目录均小于5GiB |

### Tizen文档/源码发布副本

| 路径 | GiB | 树内最近mtime | Session / 内容 | Git状态 | 证据/输入引用 | 建议与理由 |
|---|---:|---|---|---|---|---|
| `~/Toolchain/tizen-docs-release` | 20.866 | 2026-06-25 20:22 | UNKNOWN；Git仓库（Git历史约10.43GiB） | clean（含未跟踪检查） | Git clean；未查到STATUS/会话直接创建记录 | **需用户判断**：没有整目录作废依据；有Git改动/报告输入则优先保留 |

### mic镜像/压缩器调查

| 路径 | GiB | 树内最近mtime | Session / 内容 | Git状态 | 证据/输入引用 | 建议与理由 |
|---|---:|---|---|---|---|---|
| `~/Toolchain/development/llvm_image_analysis/work/sparse` | 7.708 | 2026-10-08 11:23 | S07；稀疏镜像/中间tar/压缩器实验 | 非独立Git根；内嵌仓库未穷举 | docs/status.md:1–15；docs/sparse_experiment.md:7–11：特意保留中间tar供核验 | **需用户判断**：保留历史记录；载荷是否仍用于后续工作须项目负责人确认 |
| `~/Toolchain/development/llvm_image_analysis/work/signature` | 7.524 | 2026-10-06 21:49 | S07；稀疏镜像/中间tar/压缩器实验 | 非独立Git根；内嵌仓库未穷举 | docs/status.md:1–15；docs/sparse_experiment.md:7–11：特意保留中间tar供核验 | **需用户判断**：保留历史记录；载荷是否仍用于后续工作须项目负责人确认 |

### LLVM升级

| 路径 | GiB | 树内最近mtime | Session / 内容 | Git状态 | 证据/输入引用 | 建议与理由 |
|---|---:|---|---|---|---|---|
| `~/Toolchain/LLVM_Upgrade/llvm` | 14.674 | 2026-08-07 11:09 | S06（路径大小写迁移未确证）；LLVM源码/Git | 有：9已跟踪 / 22未跟踪项 | git-status.json：llvm有9项tracked+22项untracked；现存Gemini cwd | **保留**：保留历史记录；载荷是否仍用于后续工作须项目负责人确认 |

### 共享ARM构建环境

| 路径 | GiB | 树内最近mtime | Session / 内容 | Git状态 | 证据/输入引用 | 建议与理由 |
|---|---:|---|---|---|---|---|
| `~/GBS-ROOT-TIZEN-UNIFIED-LLVM` | 11.430† | 2026-10-09 22:43 | S01/S02；多人多阶段复用；GBS根/accel/sysroot/缓存 | 非独立Git根；内嵌仓库未穷举 | docs/39 §2；MLGO/REPORT.md:10–19 | **保留**：docs/39后续ARM认证输入；MLGO历史也引用，非单Session私产 |

### Android开发环境

| 路径 | GiB | 树内最近mtime | Session / 内容 | Git状态 | 证据/输入引用 | 建议与理由 |
|---|---:|---|---|---|---|---|
| `~/Android` | 10.723 | 2026-05-21 15:41 | UNKNOWN；Android SDK | 非独立Git根；内嵌仓库未穷举 | 目录子项Sdk；Session创建归属UNKNOWN | **需用户判断**：不是已确认的会话废物；是否继续Android开发待确认 |

### 桌面应用配置与用户数据

| 路径 | GiB | 树内最近mtime | Session / 内容 | Git状态 | 证据/输入引用 | 建议与理由 |
|---|---:|---|---|---|---|---|
| `~/.config` | 8.690 | 2026-10-09 23:51 | UNKNOWN；应用配置/用户数据 | 非独立Git根；内嵌仓库未穷举 | 所查STATUS/报告未找到直接路径引用；仍需确认 | **保留**：当前桌面浏览器/编辑器在运行；配置混有状态与用户数据，不当构建缓存删除 |

### 去调试信息调查

| 路径 | GiB | 树内最近mtime | Session / 内容 | Git状态 | 证据/输入引用 | 建议与理由 |
|---|---:|---|---|---|---|---|
| `~/Toolchain/remove-debuginfo/linux-rpi` | 7.811 | 2026-08-26 17:23 | S11（Gemini仅元数据）；linux-rpi源码/产物 | UNKNOWN（未完成Git检查） | 目录与会话cwd关联；没有作废依据 | **需用户判断**：保留历史记录；载荷是否仍用于后续工作须项目负责人确认 |

### C99 inline 第二工作区

| 路径 | GiB | 树内最近mtime | Session / 内容 | Git状态 | 证据/输入引用 | 建议与理由 |
|---|---:|---|---|---|---|---|
| `~/Toolchain/development/llvm_inline_development_second/codes` | 6.769 | 2026-08-25 21:20 | S12（Gemini仅元数据）；LLVM源码工作树 | 非独立Git根；内嵌仓库未穷举 | 现存Gemini cwd；主线关系和Git状态未完全确定 | **保留**：保留历史记录；载荷是否仍用于后续工作须项目负责人确认 |

### LLVM旧开发仓库

| 路径 | GiB | 树内最近mtime | Session / 内容 | Git状态 | 证据/输入引用 | 建议与理由 |
|---|---:|---|---|---|---|---|
| `~/Toolchain/development/llvm` | 6.758 | 2026-09-16 14:32 | UNKNOWN；源码/Git | UNKNOWN（Git超时/报错） | Git status超时，不把未完成检查当clean | **保留**：没有整目录作废依据；有Git改动/报告输入则优先保留 |

### LLVM源码上传旧工作树

| 路径 | GiB | 树内最近mtime | Session / 内容 | Git状态 | 证据/输入引用 | 建议与理由 |
|---|---:|---|---|---|---|---|
| `~/temp/llvm` | 6.186 | 2026-07-01 14:50 | S08；LLVM Git仓库 | clean（含未跟踪检查） | session元数据；git-status.json | **保留**：即使clean也未核验远端备份/独有提交，暂不删 |

### glibc

| 路径 | GiB | 树内最近mtime | Session / 内容 | Git状态 | 证据/输入引用 | 建议与理由 |
|---|---:|---|---|---|---|---|
| `~/Toolchain/glibc` | 5.664† | 2026-09-15 19:59 | S14（若cwd匹配）；创建者未确证；源码/构建/项目资产 | 有：0已跟踪 / 7未跟踪项 | Git/会话元数据；工作区文档索引 | **保留**：没有整目录作废依据；有Git改动/报告输入则优先保留 |

### 个人下载 / 多项目

| 路径 | GiB | 树内最近mtime | Session / 内容 | Git状态 | 证据/输入引用 | 建议与理由 |
|---|---:|---|---|---|---|---|
| `~/Downloads` | 5.124 | 2026-10-09 23:08 | S10（关联；具体文件创建者UNKNOWN）；下载档案/未完成下载 | 非独立Git根；内嵌仓库未穷举 | 只读stat；不按后缀直接判可删 | **需用户判断**：主要为4.23GiB tizen-docs-release-master.zip及0.53GiB未完成下载；未做内容等价核验 |

## 4. 释放量逐项核算（不是删除指令）

只选择明确的旧载荷。P30的 BUILD 范围进一步收窄为 `.a/.o/.rpm/.bc/.so`，以及≥1MiB且文件头确认为 ELF/ar/bitcode 的文件；源码、日志、脚本、JSON不计入建议删除量。P33/P34只取此前授权列出的子目录中的二进制载荷，其他下载、源码、文本证据保留。逐文件清单带inode与nlink，见 `binary-payload-candidates.jsonl`。

| 编号 | 精确范围 | 候选文件数 | 可释放GiB | 范围外硬链接GiB（不计释放） | 建议 |
|---|---|---:|---:|---:|---|
| P28 | `W/temp/static-native-conversion-v2-20260924/conversion/archives` | 225 | 6.161 | 0.000 | 可删（仅旧.a树） |
| P29 | `W/temp/static-native-conversion-v3-20260924/stripped/archives` | 225 | 0.485 | 0.000 | 可删（仅旧.a树） |
| P33 | `W/temp/llvm-strip-alternative-20260929`；仅 `bc-archives / hq-payload / hq-rpm-extract / hq-rpm-repo / hq-rpmbuild / host-consumers` 内二进制 | 680 | 18.282 | 0.000 | 只删大载荷保留日志 |
| P34 | `W/temp/archive-fix-v2-build-20260929`；仅 `conversion / llvm-strip-overlay / strip-elf-analysis` 内二进制 | 767 | 7.117 | 0.000 | 只删大载荷保留日志 |
| P30-BUILD | `W/temp/gbs-root-x86_64-archivefix/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD` | 33491 | 148.488 | 0.000 | 只删大载荷保留日志 |
| P30-BUILDROOT | `W/temp/gbs-root-x86_64-archivefix/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILDROOT` | 0 | 0.000 | 0.000 | 只删大载荷保留日志 |
| P30-RPMS | `W/temp/gbs-root-x86_64-archivefix/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/RPMS` | 22 | 0.000 | 8.249 | 只删大载荷保留日志 |
| P30-SRPMS | `W/temp/gbs-root-x86_64-archivefix/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/SRPMS` | 1 | 0.000 | 0.318 | 只删大载荷保留日志 |

P28/P29均恰有225个普通 `.a`，没有其他普通文件；外部硬链接为0。候选集合之间共享但需联合删除才释放的块为 **0 B**。P30 BUILDROOT 当前无可计二进制载荷；22 RPM与SRPM仍有范围外硬链接，删该路径不能释放这些数据块，明确计 **0**。

| 建议类别 | 主表账面GiB（仅所见目录、非释放承诺） | 已核算可释放GiB | 限制 |
|---|---:|---:|---|
| 可删 | 6.646 | 6.646 | 仅P28/P29，尚待确认 |
| 只删大载荷保留日志 | 219.612 | 173.887 | 仅本节二进制清单，不能删整根 |
| 保留 | 702.008 | 0（政策保留） | 不得计入清理收益 |
| 需用户判断 | 679.168 | UNKNOWN；其中未启用swap为64.000候选 | 不能把不明归属/仍被引用/可能共享的目录直接算成可删空间 |

**只删“可删”一类：约 6.646 GiB。** 按起始空闲量静态相加也只有约 **47.577 GiB**，仍低于60GiB构建磁盘门槛。可删与已核算的“只删大载荷”合计 **180.533 GiB**；这里没有把保留目录、未知目录或64GiB未启用swap加入总数。

## 5. 明确保留的输入与不能混删的范围

以下是主表的定位补充，**不再次加入合计**。

| 别名 / 资产 | 精确路径 | GiB | 原因 |
|---|---|---:|---|
| Rnew | `W/temp/gbs-root-x86_64-archivefix-v2` | 70.971 | 当前构建/续跑根，用户指定 |
| B | `W/temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build` | 66.031 | ARM实施前x86全量回归的225个原始归档 |
| N | `W/temp/toolchain-archivefix-v2-final` | 46.299 | docs/35 GNU strip基准 |
| N38 | `W/temp/toolchain-llvm-strip` | 46.256 | docs/38最新验收产物 |
| H | `W/temp/archive-index-fix-rpm-20260923/baseline-rpm-extract` | 50.890 | docs/13基线内容 |
| rpms-docs35 | `W/temp/archive-fix-v2-final-20261009/rpms-docs35` | 8.567 | rename保全的22 RPM+SRPM |
| base-local-repo | `W/temp/archive-fix-tizen-consumers-20261009/base-local-repo` | 0.092 | 旧公开Base已404，107缓存包复原仓库不能随旧根误删 |
| ARM `armv7l` | `~/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0` | 8.377 | docs/39认证所需sysroot/accel；共享多项目环境，保留 |
| ARM `aarch64` | `~/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.aarch64.0` | 1.590 | docs/39认证所需sysroot/accel；共享多项目环境，保留 |

docs/35、36、37、38、39整个证据目录均已在主表标“保留”。docs/30的两个消费者测试根也保留：它们是原快照缓存的来源；本轮没有把“Base仓库已复原”自行扩大为可删除原缓存的授权。隔离旧混合根只做目录stat/du，仍不作为任何构建或认证输入。

## 6. 大目录内部定位与Git/Session缺口

下面进一步解释主表中较大的混合范围，不重复计量。

| 已列父范围内的子范围 | GiB | 性质 / 判断 |
|---|---:|---|
| `~/Toolchain/plan_evaluation/chromium-efl/.git` | 37.760 | Git历史，不单独删objects/pack |
| `~/Toolchain/codes/api/.git` | 17.854 | Git历史，不单独删objects/pack |
| `~/Toolchain/development/MLGO/llvm_mlgo/.git` | 16.226 | Git历史，不单独删objects/pack |
| `~/Toolchain/development/MLGO/llvm_optimize_docs/codex-verification-r5-results-20260722` | 15.098 | 历史验证/工作树载荷；需所属项目裁决，报告仍引用 |
| `~/Toolchain/development/MLGO/llvm_optimize_docs/codex-verification-r6-results-20260722` | 12.410 | 历史验证/工作树载荷；需所属项目裁决，报告仍引用 |
| `~/Toolchain/tizen-docs-release/.git` | 10.433 | Git历史，不单独删objects/pack |
| `~/Toolchain/development/MLGO/llvm_optimize_docs/codex-verification-r4-results-20260714` | 9.763 | 历史验证/工作树载荷；需所属项目裁决，报告仍引用 |
| `~/Toolchain/development/llvm_inline_development/docs/llvm_optimize_docs/verification/port22/artifacts/m1-t30-behavior-20260929T021838Z` | 7.077 | 历史验证/工作树载荷；需所属项目裁决，报告仍引用 |
| `~/Toolchain/development/MLGO/llvm_optimize_docs/codex-verification-r7-results-20260723` | 6.628 | 历史验证/工作树载荷；需所属项目裁决，报告仍引用 |
| `~/Toolchain/development/llvm_inline_development/docs/llvm_optimize_docs/verification/port22/artifacts/m1-snapshot-20260928T105826Z-restore` | 6.081 | 历史验证/工作树载荷；需所属项目裁决，报告仍引用 |
| `~/Toolchain/plan_evaluation/chromium-efl-spike-libcxx-wt/out.chrome.tz_v11.0.standard.armv7l/obj` | 5.916 | 历史验证/工作树载荷；需所属项目裁决，报告仍引用 |

主表的报告引用分为当前输入与历史证据：§5及用户指定保留项为当前保留输入；旧R3/R4、M1、spike等有历史引用，但其是否继续用于新任务UNKNOWN。没有用“会话最后活动较早”代替项目负责人作废决定。

Git检查原始结果在 `git-status.json`。本项目W开始时clean；W/llvm为 ` M packaging/llvm.spec`，本轮未改。LogAnalysisSkill有5项已跟踪变动与172项未跟踪条目且有活动交互进程；LLVM_Upgrade/llvm有9项已跟踪变动与22项未跟踪条目。MLGO/llvm_mlgo、若干M1工作树和Chromium仓库的25s检查超时，标UNKNOWN，不补写clean。`chromium-efl-spike-libcxx` Git查询128，与其交接状态表一致，不能当作可随意丢弃的空目录。

没有查到Session的目录明确保留UNKNOWN：例如clang-toolchains的创建Session、tizen-docs-release发布副本、部分GBS历史根。R3/R4根有报告路径证据，可以归入早期C99/MLGO验证线，但不能据此给每个文件指定创建Session。会话末活动时间也不等于项目关闭；是否仍需原始二进制，仍应由对应项目负责人确认。

不可读路径去重 **253** 个，完整列表 `unreadable-paths.json`。主要是GBS根的 root、cynara、ldconfig、security-manager等特权目录；不能猜它们体积。未统计的 `/home/shared`、`/home/lost+found` 单独记UNKNOWN。

## 7. 证据、命令与交付检查

所有原始输出位于 **`/home/linhao/Toolchain/development/llvm-optimize/temp/disk-inventory-20261009`**（本机，未上传）。

| 文件 | 内容 |
|---|---|
| `filesystem.txt`、`filesystem-final.txt`、`home-root-metadata.json` | df、不可访问/home目录元数据 |
| `du-large.tsv`、`du-pass2.tsv`、`du-pass3.tsv`、相应errors/exit/end、排除清单 | 全盘限时分段du；父级排除部分只在汇总中还原显示 |
| `project-temp.tsv`、`mandatory-details.tsv`、`arm-roots.tsv`、`cache.tsv` | 项目所有一级证据目录、强制保留子项、两ARM根、缓存 |
| `session-metadata.json` | 567条白名单元数据；不含会话正文/工具参数/凭据 |
| `workspace-doc-index.json`、`buildroot-doc-references.json`、`project-path-references.json` | 4,143份工作区文档的标题/路径索引及构建根路径引用行号 |
| `git-status.json`、`llvm-source-status.txt`、`process-cwd.json` | 非写入式Git检查，进程名/cwd |
| `binary-payload-candidates.jsonl`、`binary-payload-summary.json` | 候选逐文件元数据、硬链接扣除与类别合计 |
| `inactive-swap.json` | 64GiB文件stat、/proc/swaps、fstab路径命中数0 |
| `inventory-rows.json`、`merged-du.json`、`method.json`、`completion.json`、辅助`.py` | 复核本报告表格和统计方法 |

核心统计命令（均只读）：

```sh
findmnt -R /home -o TARGET,SOURCE,FSTYPE
df -B1 /home
sudo -n du -sx -B1 /home/linhao   # rc=1，未输入密码
timeout 900s du -x -B1 --threshold=5368709120 --time --time-style=long-iso /home/linhao
timeout 900s du -x -B1 --threshold=5368709120 --time --time-style=long-iso --exclude-from=<已完成目录清单> /home/linhao
timeout 600s du -x -B1 --max-depth=1 --time --time-style=long-iso W/temp
GIT_OPTIONAL_LOCKS=0 timeout 25s git -C <工作树> status --porcelain --untracked-files=normal
cat /proc/swaps
```

交付自检：仅新增docs/41并同commit更新STATUS；未改历史docs/25–39、Source、spec或补丁；未删除/移动/压缩资产；未执行GBS、rpmbuild、BOLT或性能测量；仅推GitHub，不推Gerrit。所有建议等待用户逐项确认，当前没有清理执行计划或自动删除任务。
