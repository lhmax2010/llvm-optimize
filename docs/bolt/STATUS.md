# BOLT v4 状态（新会话开场必读）

日期：2026-10-12（Asia/Shanghai）；证据目录名依用户指定为20261013。
W=`/home/linhao/Toolchain/development/llvm-optimize`；B=`/home/linhao/Toolchain/development/llvm-optimize-bolt`；E=`/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013`。
分支 `bolt-v4`；从最新 origin/main `fb833a4c8ee1ece09027a0d5d04e254ea9899a5f` 建立。W开场已有 docs/47_review_round4_package.md、gbs_llvm.conf 修改，不触碰。

## 计划

1. 独立工作树及状态备案，提交推送。
2. 只读盘点历史资料、ELF/profile/工具、spec、后处理与锁。
3. 独立scope串行轻实验，2GiB（BOLT 6GiB），nice19/ionice3；准入8/10GiB，运行低于3GiB终止。
4. 自包含设计v4（≤50KB），预注册周三/周四验证。
5. 每大步提交推送并核验远端一致。不编译LLVM、不构建、不采profile、不推Gerrit、不提问。

## 进度

| 任务 | 状态/提交 | 产出 |
|---|---|---|
| 建立分支与状态 | 完成；ba825d65（完整号见git log） | STATUS.md；inventory/opening-inputs.json与只读输入快照 |
| 资料盘点 | 完成；本条所在提交 | 02_inventory.md；E/inventory产物/SHA/spec/宏/锁快照 |
| strip实验 | 待执行 | — |
| 设计v4 | 待执行 | — |
| 收尾 | 待执行 | — |

同一提交无法包含自己的SHA：每条以所在提交为准，下一里程碑补已完成提交号。

## 已闭合结论

- 工作树隔离已建立；证据强度：git worktree list与起点SHA直接事实。
- 必读输入开场快照已封存；证据：E/inventory/opening-inputs.json（路径、大小、SHA256），后续归档会话更新不混用。

## 人工裁决前提

1. 目标：本周五（2026-10-16）前交付一个 BOLT 补丁进 Quickbuild 试验验证。试验不是上 Gerrit
2. 第一版范围：只做 x86_64 构建分支；只做 clang（lld、llvm-ar 以后）；保持现有全静态链接，混合链接不进第一版；llvm-static-devel 照常发布，不撤
3. profile 直接用现有 v2，作为 spec 的一个 Source 文件提交，不单独打 RPM；构建时必须检查 profile 与二进制的匹配度，不匹配函数比例 ≤5%，否则构建失败
4. 第一版不追求 BOLT 版 clang 的源码级调试信息，但必须保证经过完整 RPM 后处理（含 find-debuginfo、strip）后仍能正常运行
5. 补丁基线：tizen_base 提交 cb67996861d070d68fec2b4c623eed7d20ba2e23 加上归档修复的 356627 PS3 与 356639 PS2 候选；同时必须能干净应用到不带这两个补丁的 cb679968
6. 硬约束：不得影响用 LLVM 编译的其他 RPM 包——不得引起编译错误、运行时性能下降或运行内存升高；BOLT 版 clang 产出必须与原版逐字节相同；LLVM 包自身构建内存若显著增加必须报告
7. 总部计划把 bash 换成 dash：你写的任何 shell 脚本都必须是 POSIX sh，不得依赖 bash
8. 评审：周四只对补丁做一轮外部评审
9. 时间表（供你理解，不是今晚任务）：周三晚在归档会话完成的 x86 完整构建树上续跑构建（只重链 clang、做 BOLT、打包），周四验证与评审，周五交付


## 挂账

- 盘点、strip及完整RPM后处理结果尚未知；不提前承诺profile适配cb679968。
- 规定外情况停止并记录；产品材料丢失/不可读继续其余授权工作。
- 锁机制待只读查明；今晚不获取、不等待、不干扰项目锁，不进入构建根执行。

盘点闭合：全部关键历史产物仍在，SHA与历史一致；工具是docs/15实验增量构建而非spec默认产物。cb679968 profile适配UNKNOWN；续跑新树路径UNKNOWN。锁：双O_EXCL锁（项目temp及archivefix-v2根顶层），今晚不获取/不等待/不干扰。详见02_inventory.md。
