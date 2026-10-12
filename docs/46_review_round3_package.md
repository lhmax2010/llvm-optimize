# 46 第二轮评审修订：准入停止记录与第三轮材料待办

日期：2026-10-12（Asia/Shanghai）。起点：`66e3369cd8fd10803963de5dcc09d3074a80cd25`。

**本轮停止于第一步只读普查的启动入口，尚未修改代码。第三轮评审所需的 PS3、PS2 候选及新 ARM Source 没有生成，本页不能作为这些修订已完成的材料包。** 复用上轮辅助驱动时，其 16 GiB 准入断言测得 MemAvailable 为 15,255,969,792 B（14.208229 GiB），在创建 scope 和运行 `llvm-dis` 前退出。该数值门槛来自代理复制的历史驱动，本轮任务并未单独规定只读普查的内存准入线；不是 Source、输入或转换失败。未降低门槛、等待重试或修改产品代码。依“规定之外停止、停止时仍完成第五步文档”的要求，发布本记录和 STATUS。（证据：E/stop-result.json、census-driver.log、run_stage.py:9；本轮任务运行方式。）

## 0. 范围、身份与证据

W=`/home/linhao/Toolchain/development/llvm-optimize`。
E=`W/temp/review-round3-20261012`，原始输出仅保存在本机，不上传 GitHub。

开场无构建竞争进程；仓库只有用户既有的 ` M gbs_llvm.conf`，未覆盖或暂存。使用项目既有两个锁路径，锁持有进程 PID 329052，开始于 14:27:11+08:00；停止后已释放。没有访问隔离旧混合根，没有创建或清理构建树。（证据：E/starting-state.txt、processes-start.json、lock-acquired.json、lock-released.json、cleanup-result.json。）

| 文件 | 本轮前后均相同的 SHA256 |
|---|---|
| `tools/llvm_static_archives_source.py` | `6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557` |
| `tools/llvm_static_archives_arm_trial.py` | `e2c2ebfa7272c6549f9be977861985ff597d3564dd26caf72438155622e30e0d` |
| 原 356627 评审补丁 `patches/archive-index-fix/0001-Fix-llvm-static-devel-usability-with-ThinLTO.patch` | `ddef2221db9ba1c044b0087b9fcde2a93202fdf28c518b4d0dcd1c4653119ac6` |
| 原 356639 评审补丁 `patches/llvm-strip/0001-Use-llvm-strip-for-x86_64-archive-packaging.patch` | `49c5618226a8d281d9aed9427eb651391684e17a4e75bf68673d5cf2bf8761a5` |
| 用户配置 `gbs_llvm.conf` | `28f1caf93cd39738a7da1e0da8d5f945f7372963bb9823a507f9157294272169` |
| `W/llvm/packaging/llvm.spec` | `95887b2d060b38d5ef8f56936f7481a03d131f9d26432180a68e02ec95f0dda5` |

以上是旧版本的身份复核，不是新候选摘要。两份新补丁 SHA 为 NOT GENERATED。全部受保护文件逐项核对一致，见 E/protected-start.jsonl、protected-final.json。

## 1. 本次入口及停止原因

准备的只读驱动为 E/census_x86.py，计划从 E5/x86-input 按原归档和成员摘要读取 bitcode，使用现有 `llvm-dis` 反汇编并收集所有 module asm，不执行编译或转换。E5=`W/temp/arm-archive-stage1-20261010`。运行入口如下：

```sh
python3 temp/review-round3-20261012/run_stage.py \
  temp/review-round3-20261012/census-plan.json \
  > temp/review-round3-20261012/census-driver.log 2>&1
```

E/run_stage.py 逐字复制自 `temp/arm-source-root-probes-20261010/run_stage.py`，plan 登记 `admission_gib=16`、`memory_max_gib=18`。原始错误：

```text
  File ".../temp/review-round3-20261012/run_stage.py", line 9, in <module>
    available=guard.mem_available();assert available>=p['admission_gib']*guard.GIB,available
                                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 15255969792
```

| 记录 | 数值或状态 |
|---|---|
| 开场 `/proc/meminfo` MemAvailable | 17,268,344 KiB，随后准入时发生变化 |
| 准入读取 | 15,255,969,792 B，14.208229 GiB |
| 复制的辅助驱动要求 | 17,179,869,184 B，16 GiB |
| 驱动退出码 | 1 |
| `llvm-dis` / 转换 / 测试调用 | 0 / 0 / 0 |
| scope、采样器、临时 proc 挂载 | 均未启动 |
| 产品层面的失败 | 未观测，产品操作未运行 |
| 辅助脚本缺陷条款重跑 | 未使用；没有改变准入判断 |

E/x86-census-scope/commands.log 为零字节，普查输出目录和结果 JSON 未产生。上述限制不能被解释为“只读反汇编实际需要 16 GiB”或“14.208 GiB 不足以运行转换”；本轮没有测量这些需求。也不将代理复用的阈值记成 PM 对本轮另作的裁决。（证据：E/stop-result.json、census-plan.json、census-driver.log。）

## 2. 第一步七项核查的实际状态

| 核查项 | 本轮结果 | 对后续的影响 |
|---|---|---|
| x86 全部 bitcode 的 module asm 全集 | NOT RUN；停于上述入口 | 尚不能证明全集仅含白名单声明；不能用 docs/44 的定向三个成员核查代替全集 |
| 两 ARM 记录命令中 `--target=` 次数和取值 | NOT RUN | B5 未实施，不推测出现次数 |
| 两 ARM 转换产物 REL/RELA 数量 | NOT RUN | B3 未实施，不推测节类型分布 |
| cb679968 spec 的 debug 定义及条件全文 | NOT RUN | 未形成新宏评审所需的本轮核查记录 |
| x86 根生效 `__strip_install_post` 原文及包版本 | NOT RUN | C 未实施；不凭历史说明拼造宏体 |
| 两根 `/emul` 原生 shell/解释器 | NOT RUN | 不将此前“无原生 prlimit”外推为“无原生解释器” |
| 宿主和两 ARM 根 `/usr/bin/cat` | NOT RUN | B7 前置条件尚未在本轮核查 |

本表明确区分未测与 FAIL。docs/44 §18–§27 的已有结果仍有效，但其范围不能扩展为本轮新增普查或加固的实测证据。（出处：docs/44 §18–§27；E/stop-result.json。）

## 3. 评审修订登记：已接受要求，尚未实施

评审背景由用户给定为 Kimi、Codex、Claude 三家第二轮评审合并后的 PM 裁决；未提供逐条评审原文归属，本页不猜分配给某一家。以下编号沿用本轮任务，不表示代码已修改。（出处：本轮任务第二步。）

| 编号 | 修订与采纳理由 | 实施状态 |
|---|---|---|
| A1 | 通用 `-W` 前显式拒绝 `-Wa,`，避免汇编选项被当成诊断忽略 | NOT RUN |
| A2 | 保留 clang 主版本 22 门禁，另要求 dis/nm 完整版本与 clang 一致，记录三者版本 | NOT RUN |
| A3 | 共用 module asm 白名单，仅允许指定 `.globl` 声明，记录到 IR settings | 待全集核查，NOT RUN |
| A4 | x86 对上述声明的输出要求 llvm-nm 恰好一个 U 符号 | NOT RUN |
| A5 | x86 重定位符号索引先做范围检查再读取 | NOT RUN |
| B1 | ARM module asm 符号要求唯一、精确 GLOBAL/NOTYPE/DEFAULT/UND 和零值/大小 | NOT RUN |
| B2 | ARM clang 固定 22.1.8，三个工具拒绝 ARM ELF；工具版本一致性使用 A2 | NOT RUN |
| B3 | ARM32 只接受 REL、AArch64 只接受 RELA | **未实施，待第一步 3 的普查条件** |
| B4 | ARM PIC 使用 layout 已解析的 section_index/is_absolute，避免重复解析 | NOT RUN |
| B5 | 原命令恰好一个已认证 `--target=` | **未实施，待第一步 2 的普查条件** |
| B6 | ARM 节名表索引为 0 时拒绝 | NOT RUN |
| B7 | 相同 prlimit 路径读回 AS；默认失败，ARM 显式确认才允许未施加，x86 禁止该确认项 | NOT RUN |
| C | 356639 仅替换归档 strip 参数，保持可执行文件 strip 默认；install 检查 llvm-strip 版本 | NOT RUN |
| D | 固定字面量正负例、ready 后代取消夹具、安装部分失败、真实 x86 隔离转换、AST 同步 | NOT RUN |

A 仅限 A1–A5，Commands 不改；356627 的 spec 部分不改；旧补丁保留，新候选分别写 `patches/archive-index-fix/ps3/` 和 `patches/llvm-strip/ps2/`。本轮没有建立这些目录或生成任何空占位补丁，不把空 diff 当作新修订。（出处：本轮任务约束；E/protected-final.json。）

## 4. 不采纳项及理由（PM 已裁决）

下列为用户明确规定的设计边界，不是本轮实验新结论：

| 项目 | 不采纳理由 / 后续位置 |
|---|---|
| 重定位偏移加写入宽度检查 | 门禁不读目标字节；宽度随类型变化，统一 4 字节会误拒节末 1/2 字节重定位 |
| 内存看门狗 | 事后反应式，不等价于 RLIMIT_AS，且需改共用 Commands 循环 |
| `/emul` 原生 prlimit | 需改 qemu-accel 打包，超出 LLVM 包范围；保留为长期方案 |
| Python 解析 ARM 属性替代 readelf | 待第二段实测 qemu 调用开销再决定 |
| spec 改 `%{?buildsubdir}`、删除 `rm -rf`、补 binutils 依赖 | 非缺陷，不对总部评审中的 spec 做无功能收益改动 |
| 安装失败时另打印已安装清单 | summary 已记录，不为日志改共用安装函数 |
| 合并两个 change | Gerrit 依赖链保证顺序 |
| 把诊断数字写进 Commands 注释 | 证据放文档，不改 Commands |

出处：本轮任务第五步“不采纳项及理由”清单。

## 5. 测试、离线复验与补丁的证据边界

| 阶段 | 本轮结果 |
|---|---|
| 宿主新增与原有测试 | NOT RUN，新增测试数 0 |
| ARM32 根内测试 | NOT RUN，没有临时挂载 `/proc` |
| R32/R64 B7 拒绝/确认探针 | NOT RUN；探针代码未实现 |
| 新 x86 生产 Source 全量回归 | NOT RUN |
| 新 ARM 候选 x86 路径全量回归 | NOT RUN |
| 新 ARM 候选两 ARM 全量转换 | NOT RUN；没有新的 after SHA 比较或消费者复验 |
| 356639 新宏 debug 开/关展开 | NOT RUN |
| 356627 PS3 / 356639 PS2 格式补丁及顺序 apply 检查 | NOT GENERATED / NOT RUN |

历史可供后续比较的证据是 docs/44 §22–§26：x86 225 档/3,864 有序成员/3,853 flags、ARM32 210 档与 AArch64 212 档均与各自锚点相同；历史宿主 99 PASS，根内 95 PASS+3 环境不适用+1 AS 发现。这些历史结果属于旧 6bd/e2 源文件，**本轮没有重跑，不为未生成的候选背书**。本轮没有新 Source diff 或新补丁全文可外置；读旧实现请用本页第 8 节链接。（出处：docs/44 §20–§26；E/stop-result.json。）

## 6. 第三轮及生产集成待验证清单

1. 先完成本轮第一步七项核查，再根据其结果实施 A–D；特别是 B3/B5 不能跳过条件。
2. 第三轮评审材料应含新 x86 Source 相对 6bd、新 ARM Source 相对 e2 的完整 diff、新补丁全文和所有新增测试结果；当前缺项仍未完成。
3. x86 完整构建：下一轮评审后，在 cb679968 上叠两个新补丁；扩大原编译与转换产物的结构对照样本。当前没有该构建授权或新结果。
4. ARM 第二段打包验证：实际根内 readelf 版本、输出格式和调用开销；GNU ar 根内产物与宿主离线逐字节一致性；32 位 Python 峰值；每条命令耗时及 600 秒超时余量；`/proc` 可用性；磁盘；按架构 BuildRequires；spec 必须选 `/emul` 原生工具并显式传 AS 确认参数；并发设置；最终 RPM 格式、索引、符号、PIC、运行消费者验收。
5. 地址空间长期方案：调查原生限制器及其交付边界。已有 AS 失效证据不能被显式确认参数解释为限制已生效。

这些是任务规定的挂账和后续验收项，不含新的可行性判断。（出处：本轮任务第五步；docs/44 §19。）

## 7. 收尾核对

14:30:07+08:00 核对两个项目锁均不存在，没有本任务 Python 子进程；R32/R64 均无遗留 `/proc` 挂载。本轮从未创建资源 scope 或采样器，无需中止构建。没有磁盘清理、RPM 构建、代码/spec/已上传补丁修改或 Gerrit 推送。GitHub 本次仅提交本报告和 STATUS，不提交用户配置或本机证据脚本。（证据：E/cleanup-result.json、mountinfo-final.txt、protected-final.json、lock-released.json。）

## 8. 读取入口

以下旧 Source / 补丁固定于本轮开场提交，明确不是本轮尚未生成的候选：

- [生产 Source 6bd](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/66e3369cd8fd10803963de5dcc09d3074a80cd25/tools/llvm_static_archives_source.py)
- [ARM 候选 e2](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/66e3369cd8fd10803963de5dcc09d3074a80cd25/tools/llvm_static_archives_arm_trial.py)
- [原 356627 补丁](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/66e3369cd8fd10803963de5dcc09d3074a80cd25/patches/archive-index-fix/0001-Fix-llvm-static-devel-usability-with-ThinLTO.patch)
- [原 356639 补丁](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/66e3369cd8fd10803963de5dcc09d3074a80cd25/patches/llvm-strip/0001-Use-llvm-strip-for-x86_64-archive-packaging.patch)
- [此前完整复验报告](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/66e3369cd8fd10803963de5dcc09d3074a80cd25/docs/44_arm_source_review_round1.md)
- [此前评审材料](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/66e3369cd8fd10803963de5dcc09d3074a80cd25/docs/45_gerrit_patches_review_package.md)

本页只记录这次入口停止，不给出 PS3/PS2 可提交或 ARM 生产可部署的结论。
