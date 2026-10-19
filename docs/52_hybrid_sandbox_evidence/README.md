# 混合链接统一 sandbox 与指南 v3 交付证据

2026-10-19：A 创建分支、远端回读、新克隆与 GBS patch-export 检查全部 PASS；B 指南 v3 已完成。本轮没有编译或运行 GBS build，没有推 refs/for，没有访问 BOLT 分支、工作目录或已交接构建树。

## 1. 冻结补丁与新提交

| 项目 | 身份 / 结果 |
|---|---|
| 原补丁 | `docs/52_hybrid_link.patch`，SHA256 `30e90aa305dd1e5ae237adaa19b27996a722b53ef481aa8ba53f510cb3f9c678`，未修改 |
| 父提交 | `67619ec8bbbac7238a6cfc33a481ccfbcd12206f` |
| 统一分支 | `refs/heads/sandbox/lhmax2025/llvm_optimize` |
| 推送提交 | `6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2` |
| tree | `80a6fd231c4564a3b762f4ec288cf2c41f9d2e20`，与已批准补丁一致 |
| Change-Id | `I28171720d5bbbf9eaf491cdafc0aee0b43f9cd06`，原补丁已含，保留 |
| 作者 / 提交者 | 均为 `Hao Lin <hao.lin@samsung.com>`；逐命令 `git -c`，未改全局配置 |
| 提交说明 | 标题 40 字符，最长行 72 字符；只重新折行，词序及 tree 不变 |
| 工作区 | 新检出应用后干净；独立远端克隆复核后仍干净 |

来源：[a1-identity.json](a1-identity.json)、[完整说明](a1-commit.txt)、[git am](a1-am.txt)、[折行 amend](a1-rewrap.txt)。准备目录为本任务新建的 `temp/hybrid-sandbox-20261019/prepare`，从已有非 BOLT LLVM 对象库新克隆、检出指定父提交后应用补丁。它不是对 W/llvm 的修改。

辅助核对器最初把 Change-Id 行长度误算为 51，实际是 52；改为精确正则 `^Change-Id: I[0-9a-f]{40}$` 后通过，未再应用补丁或改变产品内容。原文见 [a1-checker-correction.txt](a1-checker-correction.txt)。

## 2. 唯一分支推送与回读

推送前 `git ls-remote` 返回码 0、该 ref 无输出，证明目标当时不存在：[查询命令/结果](a2-remote-before.json)、[空输出](a2-remote-before.txt)。执行一次：

```text
git push ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm 6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2:refs/heads/sandbox/lhmax2025/llvm_optimize
```

返回原文（包括远端进度；没有额外警告）：

```text
remote:
remote: Processing changes: refs: 1
remote: Processing changes: refs: 1, done
To ssh://review.tizen.org:29418/platform/upstream/llvm
 * [new branch]                6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2 -> sandbox/lhmax2025/llvm_optimize
```

退出码 0；未经排版的输出及 argv 见 [a2-push.txt](a2-push.txt)、[a2-push.json](a2-push.json)。[推后查询](a2-remote-after.txt) 精确等于上述 SHA；[新 Gerrit 克隆](a3-fresh-clone.txt)、[克隆身份](a3-fresh-clone-identity.json) 再次核对 HEAD、parent、tree、clean。新克隆以 prepare 为对象参考加速，但 clone 的 origin 是 Gerrit，分支由远端取得。

匿名 HTTPS 只读探针与错误原文见 [anonymous-read-probes.json](anonymous-read-probes.json)。因此指南提供需组员仓库读取权限的 SSH clone，不要求组员提交或推送。

## 3. GBS 导出，未构建

最初 single-branch 新克隆不含 upstream 引用，GBS 自动选择 native export，成功但不生成补丁段；该次结果保留，不拿它充当 Patch 位置门禁。只读核查 `/usr/lib/python3/dist-packages/gitbuildsys/cmd_export.py:60–69,76–96` 后，补取远端 upstream 引用，再在**新输出目录**运行标准 patch-export。依据与原输出见 [导出模式](a3-export-mode.txt)、[首次命令](a3-gbs-export-command.json)、[首次输出](a3-gbs-export.txt)、[fetch upstream](a3-fetch-upstream.txt)。没有改变配置文件、GBS 脚本或源码。

标准导出命令、TMPDIR、起止与退出码见 [a3-gbs-patch-export-command.json](a3-gbs-patch-export-command.json)，完整输出见 [a3-gbs-patch-export.txt](a3-gbs-patch-export.txt)。TMPDIR 在本任务 /home 证据目录，未使用已有构建树。结果：

- [exported-llvm.spec.txt](exported-llvm.spec.txt) SHA256：`1da77fe8dfe45134bf7ae558ef366da2cfda6eccd917740449b85557b00e7f07`。
- 自动 `Patch0`–`Patch7`：50–57 行；`%patch -P 0`–`%patch -P 7`：180、182、184、186、188、190、192、194 行。
- 16 处条件栈均为空，全部不在 `%if`/`%ifarch`/`%ifnarch` 条件块内，条件块配对闭合。完整逐行记录：[a3-export-conditions.json](a3-export-conditions.json)。
- 本次混合源码 patch 为 Patch7；spec 的 x86_64 条件保持原设计，不能把“源码 patch 无条件应用”误读为“ARM 开启混合开关”。

## 4. B1–B6 修订及证据边界

| 项 | v3 处理 | 依据 / 检查 |
|---|---|---|
| B1 | 统一分支只读 clone、固定 HEAD/tree/parent；QB 直接选择分支；删除个人 sandbox push | §1–§3 身份与远端记录 |
| B2 | 删除本机锁/cgroup/磁盘准入/杀进程规则；保留 time -v 与旧源码资源参考 | docs/22 §4；docs/49_x86_build_resume_result §1；只供规划，不是硬性阈值 |
| B3 | TEST_ROOT 只来自组员已完成的本地 x86_64 GBS 根，在该根实际安装本次 RPM；没有根则如实记未执行 | 指南 §3、§4.2；ARM 独立 hello 删除，由六格下游构建覆盖，不冒充原生 x86/SDK 全工具专项验证 |
| B4 | 同架构两个 accel RPM 同目录解包，或真实本地 GBS 根的 emul；显式 loader/库路径；目录外依赖失败 | 指南 §6；不要求 QB worker 登录；本轮未取得新混合 RPM，运行结果仍待组员验证 |
| B5 | qemu-accel 消费新 LLVM 已证实，触发方式未获取，需向 QB 管理员确认 | 下节原始文件与行号 |
| B6 | 静态开发归档按对照 RPM 路径清单逐项比较，不以固定数量代替 | 下节来源与 SHA；缺失/新增任一路径都失败 |

188 目标 NEEDED 期望表仍为原 v2 文件，SHA256 `cbcf8c0b1000c7c6a962c545f39fb826968713c98e0889f621e3c450872273fc`；本轮不改补丁、期望表或产品 Source/spec。指南 shell/Python 语法、清单重算、188 项自检与原检查器测试结果记于 [validation-v3.json](validation-v3.json)。这些是文档/检查器自检，不是构建或新 RPM 验收。

## 5. accel 重建机制：可证实与不可证实

路径前缀均为 `docs/qb_1199098_vs_1178133/`：

| 文件与行号 | 原始事实 |
|---|---|
| [llvm_builds.csv:2](../qb_1199098_vs_1178133/llvm_builds.csv#L2) | Base x86_64 llvm 22.1.8-3.1，2026-10-14 15:22:15 UTC 完成；Unified 包列表没有 llvm |
| [qemu_builds.csv:2–3](../qb_1199098_vs_1178133/qemu_builds.csv#L2) | 两个 qemu-accel 包都以 x86_64 打包构建，17:18:03 UTC 开始；Unified 包列表没有 qemu-accel |
| [armv7l 原始日志:247、253、312](../qb_1199098_vs_1178133/raw/1199098_base_x86_64_qemu-accel-armv7l.txt#L247) | 实际安装 libllvm、llvm、clang 22.1.8-3.1 |
| [aarch64 原始日志:247、253、312](../qb_1199098_vs_1178133/raw/1199098_base_x86_64_qemu-accel-aarch64.txt#L247) | 同上 |
| [quickbuild.txt:315–323](../qb_1199098_vs_1178133/raw/1199098_quickbuild.txt#L315) | 此 Unified 请求引用已存在的 Base `20261015.022255`，不是该请求重建这些包的证据 |

**结论：新 LLVM 先完成、accel 后使用该版本构建是硬证据；同一 Base QB 请求/自动触发/人工触发三者无法由这些日志区分。需向 QB 管理员确认。** 指南只给确认请求、记录新 llvm 版本、核查 accel 安装清单的操作，不编造具体触发按钮/CLI 或自动规则。

## 6. 对照归档清单

从既有 [fetch_manifest.jsonl:66](../qb_1199098_vs_1178133/raw/fetch_manifest.jsonl#L66) 的**同一 URL**重新下载 `llvm-static-devel-22.1.8-3.1.x86_64.rpm`；60,447,525 B，SHA256 `d20ac3887926586aa6a43062e6c30d71e06e56ff5c4062d5f5e7c0e9a38af82a`，与历史摘要完全一致。RPM 仅保存在本轮 temp，不入 Git。

`rpm -qpl` 退出 0；[完整输出](baseline-static-devel-files.txt)、[stderr](baseline-static-devel-rpm-query.stderr.txt)。对以 `.a` 结尾的行去重、按路径排序，生成 [expected-static-devel-archives.txt](expected-static-devel-archives.txt)，SHA256 `da78f24cc4bdc1b3180a138be9e44b75f9009f0d14c934c4cc5d16af7a96b1a8`。本次基线含 225 路径，这是来源事实；**指南门禁比较完整路径列表，不写死数量**。URL、原证据行号、命令和摘要见 [baseline-static-devel-provenance.json](baseline-static-devel-provenance.json)。
