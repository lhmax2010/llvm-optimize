# 25 llvm-static-devel 归档索引修复：基线身份门禁停止报告

日期：2026-09-23（+08:00）。起点提交：`583dad4371c65884bd5771ab921fde838d7e1dd6`。
**当前第一任务是归档索引修复；BOLT 与设计 v4 修订暂缓。** 本任务基于工作区全静态 spec，未采用混合链接补丁。

**结果：第一步的基线身份核查 FAIL，尚未进入归档普查、修法或完整构建。**
全静态构建树的 clang-22、lld、llvm-ar 三个 ELF SHA 与 docs/13 相同；第四项 `build.ninja` SHA 与 docs/14 不同。
检查在该项失败时立即退出 2，没有更换比较基准、恢复构建图或继续执行后续项。
因此，本轮**无归档修复补丁可提交，无新 RPM，无修法验收结论**。获准的一次完整构建实际启动 **0 次**。

[docs/15 §3、§3.2](15_bolt_measurement.md) 已记载同一构建目录后来获准重新 configure 并加入 BOLT。
这说明“当前构建目录仍等于 docs/13、docs/14 原始状态”并非可直接沿用的前提；
**不把这次哈希差异称为归档损坏，也不据此推断其他文件被污染。** 当前图是否恰等于 docs/15 的改后图未测。
本次用户明确要求“与 docs/13、docs/14 记录的 SHA 对照，不符即停止”，故不自行把 docs/15 改后状态当作新的放行条件。

## 0. 路径、独占与工作现场

| 别名 | 本机路径/用途 |
| --- | --- |
| W | `/home/linhao/Toolchain/development/llvm-optimize` |
| E | `/home/linhao/Toolchain/development/llvm-optimize/temp/archive-index-fix-20260923`，本轮证据 |
| R0 | `W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0`，指定全静态基线根，只读核查 |
| B0 | `R0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build` |
| TC0 | `W/temp/toolchain-baseline`，基线 RPM 解包目录；本轮因前序失败未开始检查 |
| J | `W/temp/baseline-resume-20260917`，docs/13 的原始证据/22 包 inventory |
| Q14 | `W/temp/bolt-feasibility-20260918`，docs/14 原始证据 |
| Rnew | `W/temp/gbs-root-x86_64-archivefix`，全新独占根；未运行 GBS 初始化 |
| Snew | `W/temp/llvm-archivefix-trial`，新源码工作树，分支 `archive-fix-trial` |

`temp/` 证据不上传。**本轮未读写 docs/24 隔离的旧混合构建根**，也没有复用其工具、RPM、宏或缓存。
历史 docs/22、23 的根因作为用户确认背景，不重做论证；该背景不替代本轮基线核查。

### 0.1 外部进程与锁

扫描 `/proc` 的进程名及命令 argv，检查 rpmbuild/gbs/ninja/lld/ld.lld/llvm-bolt（含 Python 启动入口）。
`E/process-check.json` 的 `processes=[]`：没有发现这些外部构建进程。

创建 Rnew 后立即以 O_EXCL 建立独占锁 `.llvm-optimize-exclusive.lock`，没有覆盖既有根或他人锁。
锁记录（`E/lock-acquired.json`）：

```text
session=archive-index-fix-b45e7b1c64844bbcbc0fb245b92e61e5
pid=1563923
started=2026-09-23T22:31:30.553069+08:00
```

锁在本轮检查与报告整理期间持有，收尾在核对归属后删除，持有进程回收；
实际结束时间和 removed 状态见 `E/lock-released.json`。没有启动构建 scope 或构建采样器。
独占锁为协作约束，不宣称它能阻止不遵守锁的外部写入。

### 0.2 外来工作树修改：验证备份后按授权恢复

进入时 `git status --short`（`E/git-status-before.txt`）：

```text
 M docs/23_archive_fix_and_profile_rebind.md
 M tools/relink_clang_for_bolt.py
```

两者逐字节 SHA 均与 `temp/foreign-artifacts/20260923-173328/tracked-working-copies/` 对应备份相符：

| 文件 | 工作副本 = 既有备份 SHA256 |
| --- | --- |
| docs/23_archive_fix_and_profile_rebind.md | `aa44933696d679759a098d1e9dbfcaf730759190ca92c0df40a999cf266d2028` |
| tools/relink_clang_for_bolt.py | `683e88c98a05d75edc6b3d1cc517b181f4b8e837c05c6f9c09c4766723f4acc6` |

确认后按本次授权执行：

```bash
git restore --source=HEAD --worktree -- \
  docs/23_archive_fix_and_profile_rebind.md tools/relink_clang_for_bolt.py
```

恢复后的主仓库 status 为空。备份未删，外来代码未执行；docs/23 的**已提交版本**没有变化。
证据：`E/foreign-backup-check.json`、`git-status-restored.txt`、`preservation-check.json`。

### 0.3 隔离源码工作树

实际创建命令：

```bash
git -C llvm worktree add -b archive-fix-trial \
  /home/linhao/Toolchain/development/llvm-optimize/temp/llvm-archivefix-trial \
  f111162e94aa48ed367c9d2c039456c70e7160ae
```

随后仅将原工作区 spec 复制到 Snew，继承已有三处并发差异。原 `W/llvm` 的 HEAD、分支和源文件未改；
Git 为新分支/worktree 写入共用仓库管理元数据是此次明确要求的建工作树操作。
原 spec 与 Snew spec 均为：

```text
SHA256=95887b2d060b38d5ef8f56936f7481a03d131f9d26432180a68e02ec95f0dda5
HEAD=f111162e94aa48ed367c9d2c039456c70e7160ae
```

Snew `git status --short` 仅 ` M packaging/llvm.spec`；相对 HEAD 的 diff 只有 ninja 6→4、compile 6→4、link 2→1。
该 diff 与原工作树的并发 diff 完全相同，**尚无归档修法**。
证据：`E/source-before.json`、`worktree-create.log`、`worktree-spec.original`、
`worktree-concurrency.diff`、`trial-concurrency.diff`、`preservation-check.json`。

## 1. 基线身份核查：第四项失败即停止

用本会话脚本只读计算 SHA256（`hashlib.file_digest`），不执行基线二进制。
命令为：

```bash
nice -n 15 ionice -c3 python3 \
  temp/archive-index-fix-20260923/check_baseline_identity.py \
  > temp/archive-index-fix-20260923/baseline-identity.log 2>&1
```

实际窗口：`2026-09-23T22:32:42.175719+08:00` 至 `2026-09-23T22:33:04.024667+08:00`。
退出码 **2**。前三项参考 docs/13 §7 所引 `J/elf-code-equivalence.json` 的 `resumed_build_sha256`；
第四项参考 docs/14 §4.2 所引 `Q14/relink/preservation-check.json` 的 `after`。

| B0 内文件 | 字节数 | 历史 SHA256 | 当前 SHA256 | 结果 |
| --- | ---: | --- | --- | --- |
| `bin/clang-22` | 1793477048 | `d25e99607c9ea23bf2e50da5075c21f0145f6da24a39a4228d2fd8026ead70cf` | `d25e99607c9ea23bf2e50da5075c21f0145f6da24a39a4228d2fd8026ead70cf` | PASS |
| `bin/lld` | 1079523024 | `9895d67f7020ac1ca573ac7d40b1cda93ace9aa504c17cfed358211bd1554f47` | `9895d67f7020ac1ca573ac7d40b1cda93ace9aa504c17cfed358211bd1554f47` | PASS |
| `bin/llvm-ar` | 121868264 | `3d8ed30f0cfb0ce3bf1dc096b7b3cb840291ff0e49f3aaa26975ad3a2a681d8f` | `3d8ed30f0cfb0ce3bf1dc096b7b3cb840291ff0e49f3aaa26975ad3a2a681d8f` | PASS |
| `build.ninja` | 30446051 | `81216d3d30685a3c4ade8a667c92b51da923fba54331ebfefd38c69906bc7120` | `133b142f3f10cb4b87f1283d2ace8616bfd9013681609ee23134d6dccd44f99a` | FAIL |

原始逐项输出和结构化结果分别为 `E/baseline-identity.log`、`E/baseline-identity.json`。
前三个 PASS 只证明三个 ELF 的身份，不能外推所有归档、Ninja 图、RPM 或安装树均未改。

### 1.1 与已登记历史的关系

已提交 `docs/15_bolt_measurement.md:65–80` 记录：原目录重新 configure，
`LLVM_ENABLE_PROJECTS` 加入 bolt，cache SHA 从
`e730feac1d721f5485c7ac3e981f3537110af5da1a4416c077e292e05b576a8b`
变为 `23848f0d9a5b46a83c8d2ed7b099d2e6e1d6e9935a4632fb7ba8ba2c8d1f0d55`。
`:159–164` 明确原 build 已成为实验目录，改前图/cache 已归档；`:167–172` 记录关键 ELF 哈希不变。
本轮只引用这段**历史事实**解释为何不能默认目录未变化；没有继续测当前 cache、追查修改者或自动回滚。
历史摘录保存为 `E/historical-configure-reference.txt`。

### 1.2 未执行的其余身份检查

`build.ninja` 不匹配后程序立即退出，下列均 **NOT RUN**：

- 当前 `CMakeCache.txt` 对 docs/14 的 SHA 比较。
- TC0 的 clang-22/lld/llvm-ar SHA 比较。
- J inventory 的 22 个 RPM 全部 SHA 比较。
- 已知坏 `liblldCOFF.a` 与构建树对应归档的 SHA 比较。

因此，**本轮不宣称基线 RPM/TC0 被改动，也不宣称它们已经完整核验通过**。
没有访问其他基线副本来替换输入，没有用新 SHA 替代用户指定门禁。

## 2. 普查与宏链查证：NOT RUN

第一步的身份先决条件未通过，故未进行逐归档普查，不能提供本轮实测成员表或作修法分支选择。

| 指定类别 | 请求覆盖数 | 本轮成员/bitcode/机器码/其他/thin/索引状态 |
| --- | ---: | --- |
| llvm-static-devel | 225 | UNKNOWN，未普查 |
| libarcher_static.a | 1 | UNKNOWN，未普查 |
| compiler-rt 运行库归档 | 45 | UNKNOWN，未普查 |

请求数来自任务范围，不作为本轮实际枚举计数。未确认 RPM 索引是否恰为机器码成员符号。
`_rpm_strip_disable` 及 `__strip_install_post` 的基线根宏体/file:line 本轮未查证；
不将旧混合根中的宏体当作指定全静态根的证据，也不为补齐报告而越过停止点读取该隔离根。

## 3. 修法与补丁状态：NOT RUN

用户要求的修法方向保持登记：spec 局部去掉通用归档 strip；在 `%install` 末尾按成员实际字节识别，
仅将全部成员为机器码的非 thin 归档交 `/bin/strip -g`，bitcode/其他/thin 不交 GNU strip。
这是**授权方案，不是本轮实现结果**。若运行库含 bitcode，须在对应停止点报告，不能自行扩大范围。

由于普查未做，本轮没有编写新的宏体、安装尾段或成员分类器，没有产生归档修法最小 diff，未执行修法的 `git apply --check`。
`E/trial-concurrency.diff` 只是原有 4/4/1 调整，**不是可提交归档修复补丁**。

可提交的归档修复补丁路径：**无**。补丁 SHA：**不适用**。结论：**尚不能以本轮完整验证通过为由提交**。

## 4. 完整构建与最终 RPM 验收：均 NOT RUN

没有修改 `tools/build_llvm_x86_64.py`，没有新增或放宽认证指纹；原 18 GiB 基线门禁保持原状。
本轮完整构建命令执行次数 **0**，因此构建 wall、峰值内存、磁盘消耗、新 22 包 inventory、
`temp/toolchain-archivefix` 解包产物均不适用；未把前轮构建数据填入本轮结果。

| 第四步验收要求 | 本轮结果 |
| --- | --- |
| 所有开发归档完整符号→成员映射相等，区分重名成员与次序 | NOT RUN，无本次 RPM |
| 纯机器码归档无调试节、成员内容与基线相等、索引完整 | NOT RUN |
| brp-compress/strip/python-hardlink/find-docs/find-debuginfo 等仍执行，归档 strip 与格式错误为零 | NOT RUN；不能把没启动构建的“零次”当作后处理通过 |
| 22 包清单/逐文件 SHA 差异分类并逐个分析其他差异 | NOT RUN |
| LLVMContext/Module，core/support 与 lld 组件两组，各用 GNU ld/lld 链接并运行 | NOT RUN |
| 已知坏 liblldCOFF.a 的链接和完整索引负对照 | NOT RUN |
| 本次 clang-22/lld/llvm-ar 对 docs/13 的可复现性比较 | NOT RUN；§1 检查的是旧构建树，不是新产物 |

未跑 BOLT、性能校准、profile 采集、Chromium 或 Gerrit 推送；没有重试构建或更改修法绕过失败。

## 5. 恢复条件与本项目优先级

归档索引修复仍为本项目第一任务，设计 v4/BOLT 实施暂缓；当前未完成原因是指定基线目录的身份门禁。
继续前需明确以下两条路径中的一条，而不是自动放宽判据：

1. 明确允许使用 docs/15 已授权重新 configure 后的 B0 作归档普查来源，并给出应验证的改后身份范围；
   仍须核对归档自身、基线 RPM/TC0 后才能开展修法。关键 ELF 相同不自动证明归档完整。
2. 提供与 docs/13、docs/14 原始记录一致的可信构建树作为普查对照；本轮不自行恢复或拼装它。

现有 Rnew/Snew 保留，未应用修法、未初始化 GBS；结束时独占锁删除。再次执行前需重新取得锁，
不得将本次停止报告当成后续任意配置/补丁的构建许可。

## 附录：证据与自检

| E 下文件 | 内容 |
| --- | --- |
| process-check.json、hold_lock.py、lock-acquired.json、lock-released.json | 外部进程核查与独占生命周期 |
| git-status-before.txt、foreign-backup-check.json、git-status-restored.txt | 外来备份核实及获准恢复 |
| source-before.json、worktree-create.log、worktree-spec.original | 原源码身份与新工作树建立 |
| worktree-concurrency.diff、trial-concurrency.diff、preservation-check.json | 三处并发差异与原 spec 未改证明 |
| check_baseline_identity.py、baseline-identity.log、baseline-identity.json | 实际身份核查命令/输出；第四项即退出 2 |
| historical-configure-reference.txt | docs/15 已登记的历史配置变更，不代替本轮检查 |
| final-cleanup.json | 收尾锁/进程回收、原文件保护检查 |

自检：先读 STATUS；未读写隔离旧混合根；外来文件确认备份后才恢复；原 LLVM spec/源文件未改；
一次完整构建尚未启动；没有失败后重试；只提交本报告与 STATUS，新增优先级与停止原因，GitHub 推送不涉及 Gerrit。
