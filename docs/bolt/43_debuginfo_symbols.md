# 43. debuglink 完整构建验证：前置认证停止记录

本轮完整构建在进入 %prep 前因新 GBS 导出源码目录缺失而失败，没有产出新的 clang-debuginfo，因此尚不能确认正式包带上了匹配符号。42 号临时实验仍支持函数级定位，但本轮安装 RPM 后的自动符号加载和崩溃栈验证没有执行。包大小变化、符号处理耗时和完整构建磁盘峰值均未测得；启动尝试用时8.123秒后按停止条件结束，未重试。

## 1. 范围、源码与预检查

任务指定目录名为 `20261028`，本次前置步骤跨到北京时间 2026-10-29。只使用旧 Toolchain 快照的独立新根，不沿用 45 号的新 Base 快照，不单独补 `_toolchain` 改变正式构建条件。未推 Gerrit、sandbox，未操作 QB，未删除任何构建根。

| 身份 | 值 |
|---|---|
| 原源码提交 | `569d734d0ccb2959e3f33494593c5cd46a01c347` |
| 原 tree | `e3fff52ab97b479bf3e1fd5bc5b90f842756c346` |
| 补齐模式分支后本地提交 | `69807d06b89f5d14140854e99485182bdef9546b` |
| 新 tree | `f117b3c47eca5739f6829bd3ff9446bc632d77c1` |
| 父提交（不变） | `6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2` |
| Change-Id（不变） | `Ic98eab90cc017f127a66e1729b44fab8b8e8fb41` |
| 作者、提交者、Signed-off-by | `Hao Lin <hao.lin@samsung.com>` |

源工作树仍为 `W/temp/debuglink-tb20261026/source`，detached HEAD；没有创建分支。使用 `git -c user.name="Hao Lin" -c user.email="hao.lin@samsung.com" commit --amend --reset-author`，未改全局配置。最终源码工作树干净。

检查发现原 569d734d 无条件调用符号分离和 debuglink，不满足本轮“发布模式不生成”的要求。按“缺项先补”的授权，增加 `pipeline --debug-symbols`（默认关闭），spec 仅在 `llvm_release_build=0` 的已有 x86+BOLT 分支传入；release 仍用原 pipeline 调用。安装/post 已按 identity 是否有 `debug_file` 分支，无需改写。提交说明补充 debug/release 范围。

其余原有实现检查如下（源码全文在证据 `source/`，此表是代码审查，不冒充本轮实际产物认证）：

| 项目 | 源码依据与结果 |
|---|---|
| 分离符号 | `separate_debug_symbols()` 使用 `eu-strip --remove-comment -f ... -o ... clang.bolt`，校验原输入 SHA；不使用 LLVM only-keep-debug |
| 符号表与地址 | `verify_debug_symbols()` 比较完整 symtab，选 24 个不同地址、包含 main 与冷片段，至少 20 个；每个解析名须属于该地址的符号集合 |
| strip/RUNPATH/debuglink 顺序 | pipeline 先分离，之后 strip-all、adjust_rpath、add_debuglink；后者检查加载内容/程序头、CRC 和安装基线安全属性 |
| 身份 | debug_file 记录 SHA、大小、CRC；after_sha256 在 debuglink 后更新 |
| 安装 | `install_candidate()` 符号文件临时写入、fsync、SHA 校验、0644、原子改名至标准路径 |
| post | 两文件 SHA/CRC/mode 校验；平台已有 debuglink 跳过规则与前后 SHA 不变共同作为 find-debuginfo 跳过依据 |
| 依赖 | `BuildRequires: elfutils` 在 x86_64 且 BOLT 开启的条件内；新根实际安装 elfutils 0.189-1.13 |
| 未改变 | profile SHA `52fd8522b8cceadebfb6bfc0a19f721f1072cff95c682b12b2c4dd5b0cc1e27f`；全部模块级常量（含 OPTIONS、白名单、认证常量）与 569d734d 相同；原有门禁保留 |

精确差异：`source.patch`（相对 569d734d）、`source-vs-f308-spec.diff`；原/新身份和常量证据分别为 `initial-identity.json`、`source-identity.json`、`constants.json`。

## 2. 测试、导出和新根准备

- **348 项测试 PASS**：原 346 项，加 debug/release 各一项 pipeline 分支测试；原 debug pipeline 顺序测试显式传 `debug_symbols=True`，未删除断言。`tests.stderr` 是 unittest 完整原文。
- 首轮测试有 3 个旧 fixture 调用方式失败、8 个宿主 PATH 找不到 cmake 的错误。前者更新显式 debug 参数，后者使用已存在的宿主 CMake 3.31 工具路径；未安装工具、未在历史根运行 CMake。原输出 `initial-tests.*` 保留，修正详见 `preparation-corrections.txt`。
- gbs export **PASS**，完整 argv 在 `export-result.json`。导出新提交，8 个源码补丁（包含 hybrid）。
- config：`W/temp/bolt-v4-20261021-disk-footprint/gbs_llvm_qb1202084.conf`；仅 `tizen-base-toolchain_20261013.024319` 的 packages/debug 两仓库。
- build.conf SHA 已核对为 `e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945`。
- 新根：`W/temp/debuglink-20261028/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0`。只完成依赖安装和 `%prep`，退出 0，用时约 150 秒，**没有开始 `%build`、CMake 配置或 ninja 构建**。
- 本地资源：systemd-run，MemoryMax **24,482,979,840 B**（MemTotal 减 8 GiB），MemorySwapMax=0，CPUQuota=1200%，nice10，ionice2/7；/home 低于20GiB停止监控在准备阶段启用。命令见 `prep-command.json`。完整构建尚未启动，外层 `--threads=30` 因而尚未执行；准备阶段已传入用户指定的三个宏。
- 39 号对照 products 的 **35 个 SHA256SUMS 条目全部通过**，没有改动原件。

## 3. 五项解析通过，BOLT-off 逐字节门禁失败

新根 RPM/rpm-build 为 **4.14.1.1-1.7**。以下各项均同时执行 `rpmbuild -bp --nodeps --nobuild` 与 `rpmspec -P`，退出码均为0，每份展开均有8个 Patch 声明。完整 argv、stdout、stderr、Source/Patch 清单见 `five-parse/`。

| 项目 | 结果 |
|---|---|
| x86_64 BOLT 默认开启 | PASS |
| x86_64 --without clang_bolt | PASS |
| x86_64 bcond 一行回退副本 | PASS |
| armv7l-tizen-linux | PASS |
| aarch64-tizen-linux | PASS |
| BOLT-off debug 与 f308fe08 原 spec 展开逐字节相同 | **FAIL：新增一个空行** |
| BOLT-off release 比较 | NOT RUN：前一门禁失败后停止 |
| ON debug/release 的额外展开断言 | NOT RUN：位于失败门禁之后；两分支单元测试已 PASS |

比较使用未注入 GBS VCS 头的两份源码 spec，同一个根、同一个环境；只切换文件名。没有过滤空白或其他归一化。共同参数为：

```text
/usr/bin/rpmspec -P --target x86_64-tizen-linux
  --define "_without_clang_bolt 1" --define "_toolchain clang"
```

基线展开15,914B，新展开15,915B。基线 SHA256：
`d2f3cad67f101b52c67be11a76ec10a5682d3948ca8b5037a3ff41709a4e7679`；新展开 SHA256：
`622bd462ff85ba2de7fd32e14a077895eeeed6fe99633bef51f99875302c1ed7`。

`off-debug.diff` 原文的差异部分：

```diff
@@ -88,6 +88,7 @@
 
 
 
+
 Requires: libllvm = 22.1.8-1
 
 %description
```

失败栈原文：

```text
AssertionError: OFF expansion differs debug
```

差异对应 569d734d 已新增的条件块内 `BuildRequires: elfutils` 行。Tizen RPM 在关闭分支的展开结果留下一个额外空行；没有新增生效的构建依赖，但用户要求的是**逐字节相同**，不能据此判 PASS。本轮不移除空白、不改变判据、不继续构建。后续可考虑将 elfutils 合并到既有条件 BuildRequires 行，再重新做全部展开检查；这里只记录建议，未实施。

## 4. 停止后的状态与未执行验证

| 后续项目 | 状态 |
|---|---|
| 完整构建，22 binary + 1 source RPM | NOT RUN |
| 本轮 profile 匹配、13a07cb7 / 8c2429d8 两级身份 | NOT RUN |
| 23 包差异与 ar 成员日期分类 | NOT RUN |
| 本轮 90 TU | NOT RUN |
| 新临时 chroot 安装 RPM，LLDB 自动加载与崩溃栈检查 | NOT RUN |
| clang/debuginfo RPM 大小、分离/加链接时间 | NOT RUN |

新根、导出目录、已有对照产品和本地源码提交全部保留。准备服务已结束；`findmnt` 最终输出中无新根的残留挂载，未执行强制或懒卸载。没有推送 Gerrit/sandbox、没有 QB 操作。

日志末行：

```text
DEBUGLINK FINISHED 2026-10-29T00:02:26.036781+08:00 status=stopped reason=BOLT_OFF_debug_expansion_has_one_extra_blank_line
```

崩溃定位状态不能写成“正式包完整认证已通过”：**函数级实现已具备、42 号临时方案已验证；完整打包/安装认证因前置门禁暂停，源码行方案待实验**。继续挂账 LLVM only-keep-debug 缺陷修复、源码行成本实验、scm/meta/qb 359363/359364 进展，以及合入后首轮 QB 的最终编译配置核对。

## 5. 证据索引

所有相对路径位于 `tools/bolt/results/debuglink-20261028/`：

- `result.json`：总结果和未执行项。
- `source-commit.txt`、`source-identity.json`、`source.patch`、`source/`：本地新提交及完整 spec/helper。
- `tests.stdout`、`tests.stderr`、`initial-tests.*`、`scripts/tests.py`：测试及原始失败记录。
- `export-result.json`、`export.stdout`、`export.stderr`：导出命令和结果。
- `prep-command.json`、`prep-result.json`、`prep.stdout`、`prep.stderr`：新根准备。
- `five-parse/`、`scripts/parse.py`、`parse.stderr`、`off-debug.diff`：解析和精确比较证据。
- `baseline-SHA256SUMS-check.txt`：35份旧产品原件身份。
- `final-*.json`、`debuglink.log`：停止状态、挂载和末行记录。

本报告 raw：<https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/43_debuginfo_symbols.md>。

**总结论：STOP；348项测试和五项解析通过，BOLT-off debug 展开多一空行触发门禁，未启动完整构建，未推源码。**


## 6. 修复空行与前置检查（2026-10-29）

用户裁决维持 BOLT-off **全文逐字节相同**的门禁。本轮只修 spec 的依赖声明，不启动完整构建。前述停止记录原样保留；本节记录修复后的新结果。

### 6.1 唯一源码改动与提交

相对 `69807d06b89f5d14140854e99485182bdef9546b` 的源码 diff 只有：

```diff
 %ifarch x86_64
 %if %{with clang_bolt}
 BuildRequires: python3 >= 3.9
-BuildRequires: elfutils
-BuildRequires: xz
+BuildRequires: xz elfutils
 %endif
 %endif
```

| 项目 | 核对结果 |
|---|---|
| 新本地提交 | `3ee2d84719e4bd358c0b2366161f70f2eb788313` |
| tree | `43d60f7523439fa0ccf4a61f668dd60622554606` |
| 父提交 | `6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2`，不变 |
| Change-Id | `Ic98eab90cc017f127a66e1729b44fab8b8e8fb41`，不变 |
| 作者/提交者/Signed-off-by | `Hao Lin <hao.lin@samsung.com>` |
| 提交说明 | 与69807d06逐字节相同 |
| helper、profile、OPTIONS、白名单 | helper/profile全部字节不变，因此其中OPTIONS、白名单均不变 |

仍在原 source worktree 的 detached HEAD 上，以单次 `git -c` 参数执行 amend/reset-author/no-edit；工作区干净，没有创建分支，没有推送源码到 Gerrit/sandbox。

### 6.2 全部前置检查

| 检查 | 结果 |
|---|---|
| 全部 helper 测试 | **348/348 PASS** |
| 新提交 gbs export | **PASS**，固定旧快照配置，完整命令/输出保留 |
| Tizen RPM：x86 BOLT 开 | **PASS** |
| Tizen RPM：x86 BOLT 关 | **PASS** |
| Tizen RPM：x86 一行回退 | **PASS** |
| Tizen RPM：armv7l | **PASS** |
| Tizen RPM：aarch64 | **PASS** |
| BOLT-off debug vs f308fe08 | **逐字节相同**，15,914B |
| BOLT-off release vs f308fe08 | **逐字节相同**，16,401B |
| BOLT-on debug | **PASS**，有 `BuildRequires: xz elfutils` 和 `--debug-symbols`；没有release去-g段 |
| BOLT-on release | **PASS**，没有 `--debug-symbols`；有release去-g段（elfutils依赖仍受x86+BOLT条件保护） |
| 新spec在准备根中的依赖/构建入口解析 | **PASS**，`rpmbuild -bc --short-circuit --nobuild`退出0，未加`--nodeps`，没有执行%build |

Tizen rpm/rpm-build 为 **4.14.1.1-1.7**。五项均执行 `rpmbuild -bp --nodeps --nobuild` 及 `rpmspec -P`，全部返回0，导出spec中8条Patch声明保留。这里的“解析”不执行%prep或%build。

BOLT-off 比较使用 f308fe08 和新提交的**原源码spec**，避免混入GBS自动VCS头；比较完整展开文件，没有过滤空白、没有内容归一化。两对SHA256为：

| 模式 | 基线与新提交共同的SHA256 |
|---|---|
| debug | `d2f3cad67f101b52c67be11a76ec10a5682d3948ca8b5037a3ff41709a4e7679` |
| release | `5c4104d75104893e7a9ba130529cddabdf4f50cfa45b6c450e0cbdecba1252a5` |

准备根的 `/home/abuild/.rpmmacros` 自带 `_toolchain`。本次 debug 明确传 `--define '_toolchain clang'`，release 明确传 **`--undefine _toolchain`**；后者不能只省略define，否则仍是debug模式。通过实际展开的 `--debug-symbols` 与去-g代码确认分支，两个模式均已测到。两种模式的 x86 CMake build type 本来都是 Release，不能用这个名称区分是否生成调试信息。

### 6.3 已准备根的复用与晚上入口

新导出保存在：

```text
W/temp/debuglink-20261028/preflight-fix-20261029/export/
```

对旧导出、新导出以及根内SOURCES逐文件核对后确认：

- 所有被 `llvm.spec` 引用的 Source/Patch 字节相同，包括源码tar、8个补丁、模型输入、profile、helper、Source1005；旧根SOURCES的文件与上一轮输入匹配。
- `llvm.spec` 只差本次BuildRequires修复及GBS自动生成的VCS提交号；导出目录里的另一份 `libcxx-runtimes.spec` 只差自动VCS号，它不是本次llvm.spec的Source/Patch输入。
- `%prep` 正文逐字节相同；上一轮 `%prep` 已退出0。准备好的 `BUILD/llvm-22.1.8/llvm/CMakeLists.txt`、`mlgo_verify_assets/` 存在，尚无build/CMakeCache.txt。
- 因而 **不需要重新%prep**。没有删除、重解包或重新应用补丁；保留上一轮SOURCES/llvm.spec作为旧准备记录。
- 新版导出spec已复制到原先为空的 `home/abuild/rpmbuild/SPECS/llvm.spec`，SHA与新导出一致。使用原有三个jobs宏、`_build_create_debug 1`和原根实际宏环境做依赖检查通过；`rpm -qf /usr/bin/eu-strip`也成功。
- 配置仍只有旧Toolchain `20261013.024319` 的 packages/debug 两仓库；build.conf SHA再次核对为 `e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945`。

**输入和依赖已准备就绪，下一轮可直接开始%build。**
`preflight-fix-20261029/ready-plan.json` 和证据中的 `readiness.json` 保存了新版提交、spec路径和**未执行**的 `rpmbuild -bc --short-circuit` argv。该命令仅是build阶段，后续完整打包仍需相应install/package阶段与原有资源、proc和日志监控。旧 `temp/debuglink-20261028/run.py`/plan仍指向旧导出/提交，作为历史脚本保留，下一轮不能原样运行它；应使用本节的新ready-plan输入。此说明避免误用旧提交，并不表示缺少依赖或需要再做%prep。

本轮没有启动systemd构建服务、没有运行CMake/ninja、没有创建新RPM、没有挂载/卸载；没有删除目录或修改VS Code配置。测试、导出和文件核对按nice19/ionice3运行。

### 6.4 检查脚本的准备性修正与证据

所有新增材料位于 `tools/bolt/results/debuglink-20261028/preflight-fix-20261029/`，没有覆盖上一轮失败证据：

- `fix.diff`、`source-identity.txt`、`unchanged.json`：唯一源码修改、作者与父提交、helper/profile不变证明。
- `tests.*`、`export-*`、`export.stdout/stderr`：348项测试与GBS导出原文。
- `five-parse/`、`off-byte-proof.json`：五项解析、双模式OFF字节证明与ON分支检查。
- `export-input-comparison.json`、`export-spec.diff`、`unchanged-prep.txt`：准备输入复用依据。
- `ready-*.json/stdout/stderr`、`readiness.json`：新根依赖检查与未执行的build argv。
- `scripts/`、`result.json`、`SHA256SUMS`：执行脚本、总结果与证据校验和。

准备脚本有两处额外假设得到修正并保留失败输出：第一处把未参与llvm构建的另一份spec自动VCS变化也当成输入变化，改为逐字证明只有VCS行变化并单列；第二处错误期待 `rpmspec -P` 输出自动生成的clang-debuginfo Name头，移除此不适用的额外断言，用已规定的debug参数和去-g分支确认模式。必需的检查没有跳过，OFF字节门禁没有归一化或放宽；完整打包认证仍留待晚上。

**本节总结：所有前置检查PASS，空行问题闭合；新版spec和源码树已准备好，仅本地提交，完整构建尚未启动。**


## 7. 完整构建验证（2026-10-30，指定目录 full-20261029）

**结果：FAIL，已停止。** 这次失败发生在本地构建入口，尚未运行%prep、%build、任何BOLT门禁或平台后处理；不能据此判断debuglink实现是否有产品缺陷。第6节已经通过的前置认证没有重跑，也没有被本轮宣称为完整构建认证。

### 7.1 身份、全新目录和启动命令

开始和结束时均核对：

- HEAD：`3ee2d84719e4bd358c0b2366161f70f2eb788313`。
- tree：`43d60f7523439fa0ccf4a61f668dd60622554606`。
- 工作区干净，源码未修改；没有生成新源码提交。
- 新建独立目录 `W/temp/debuglink-20261028/full-20261029/`，GBS根为其下 `gbs-root/`。没有使用此前准备根，也没有复制旧BUILD树。

实际GBS命令（完整argv见 `build-command.json`）：

```sh
gbs -c /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261021-disk-footprint/gbs_llvm_qb1202084.conf build   -A x86_64   -B /home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028/full-20261029/gbs-root   -c 3ee2d84719e4bd358c0b2366161f70f2eb788313 --threads=30   --define "jobs 8" --define "_smp_mflags -j8"   --define "_costomized_smp_mflags -j20"   --baselibs --style=tar --spec llvm.spec   /home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-tb20261026/source
```

没有 `--short-circuit` 或 `--noprep`。配置仍为固定Toolchain `20261013.024319` packages/debug，build.conf SHA为 `e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945`。GBS版本2.1.0。

构建在用户systemd后台服务 `debuglink-full-20261029.service` 中运行，MemoryMax **24,482,979,840 B**，MemorySwapMax=0，CPUQuota=1200%，nice10，ionice2/7；本地监控保留/home低于20GiB停止条件和门禁/身份/OOM停止检查。资源限制没有进入发布代码。

初次nohup调度没有在工具调用结束后存活，没有启动GBS；随后改由持久用户systemd控制服务运行同一个监督程序。只有后者产生了一次实际GBS尝试。没有在构建失败后再启动第二次尝试。

### 7.2 失败原文与责任边界

`failed-package-log.txt` 全文仅13行，关键原文：

```text
L9: [    0s] /usr/bin/build: line 1215: cd: /home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028/full-20261029/gbs-root/local/sources/tizen_base_toolchain_standard/llvm-22.1.8-1: No such file or directory
L10: [    0s] llvm.spec is empty.  This should not happen...
L12: [    0s] linhao-linux failed "build llvm.spec" at Thu Oct 29 16:50:02 UTC 2026.
```

`service.stderr`：

```text
error: <gbs>some packages failed to be built
Finished with result: exit-code
Main processes terminated with: code=exited/status=1
```

这是本次控制脚本的启动准备疏漏：只创建了新GBS的 `local/BUILD-ROOTS`、`local/sources`、`local/repos` 父目录，没有把已认证的导出放到GBS期待的具体source目录；这次GBS调用也没有自动补出该目录。`source-directory-inventory.json` 确认该目标目录不存在。日志不足以进一步认定GBS为何没有自动重新导出，因此不把它写成GBS产品缺陷。

失败尚未到RPM脚本段，未触发任何debuglink/BOLT产品门禁。但用户明确把“构建失败”列为停止条件，本轮据此停下，不自动补目录重试，不改源码、不绕过门禁。

下一次获准续跑时，应先将第6节已经认证的新导出放到该次GBS期待的 `local/sources/tizen_base_toolchain_standard/llvm-22.1.8-1/`，或确认GBS确实重新导出到那里，再完整启动；这只是提供tar/patch/spec等输入，不复用已%prep的BUILD树，也不需要short-circuit/noprep。本轮停止后未执行这项修复。

### 7.3 耗时、资源与所有后续验证的状态

| 项目 | 本轮结果 |
|---|---|
| 实际GBS退出码 | 1 |
| GBS尝试耗时 | 8.122648508秒（不是完整构建耗时） |
| cgroup memory.peak | 116,064,256B |
| OOM / oom_kill / oom_group_kill | 全部0 |
| swap峰值 | 0B |
| 构建内门禁与22+1 RPM | NOT RUN；RPM产出0 |
| profile及strip-all/RUNPATH两级SHA | NOT RUN |
| 39号产品SHA及23包比较 | NOT RUN：尚无待比较新产物，未读取原件做重复核对 |
| 90 TU | NOT RUN |
| 新chroot安装两个RPM、LLDB自动加载、symbolizer | NOT RUN；没有新安装chroot或临时proc |
| clang/debuginfo包大小变化 | 未测得 |
| 分离符号与debuglink耗时 | 未测得 |
| 完整构建磁盘峰值 | 未测得；唯一计划采样因新chroot的du/python尚未就绪而记missing |
| 结束时新GBS目录实际占用 | 4,857,856B，单次结束值，不冒充峰值 |

没有OOM或磁盘不足证据，失败由上述source目录缺失直接报告。记录的时间为北京时间2026-10-30 00:49–00:50；包日志中的UTC日期仍为10月29日。不改变用户指定的目录名。

### 7.4 保留、日志及交付

新目录、日志和根现场全部保留；此前所有目录及products未删除。结束后源码身份不变、工作区干净；本轮新根没有残留挂载，没有结束其他进程。没有运行CMake/ninja，没有Gerrit/sandbox推送，没有QB操作。

证据位于 `tools/bolt/results/debuglink-20261028/full-20261029/`：

- `plan.json`、`build-command.json`、`service-command.json`、`scripts/`：原始输入和本地控制脚本。
- `service.stdout/stderr`、`failed-package-log.txt`、`excerpts.txt`：GBS与包日志原文。
- `build-result.json`、`controller-result.json`、`resources.jsonl`、`du-root.jsonl`：耗时/资源/采样。
- `source-directory-inventory.json`、`launch-notes.txt`：目录缺失与启动准备说明。
- `result.json`、`source-final.json`、`source-status.json`、`services-final.json`、`mounts-final.json`：停止状态和保护边界。
- `debuglink.log`、`background.stdout/stderr`：后台终态原文。

后台日志末行：

```text
DEBUGLINK FINISHED 2026-10-30T00:50:02.713638+08:00 status=failed reason=build-failed
```

**本节总结：完整构建入口失败、没有进入%prep；所有构建后验证未运行，现场保留，源码未改、未推送。**


## 8. 启动方式修复与白天演练（2026-10-30）

**结论：演练通过，晚上可以直接启动。** 这里只证明启动流程、CMake 入口和停止清理可用，不代表完整构建或产品认证通过。前面各节保留历史原文；本节不修改第7节的失败结论。源码仍为 `3ee2d84719e4bd358c0b2366161f70f2eb788313`，tree `43d60f7523439fa0ccf4a61f668dd60622554606`，开始/结束工作树干净，没有源码修改或新源码提交。

### 8.1 沿用的入口与逐项差异

先澄清记录出处：39号的 `run.py:4–7` / `build-command.json` 实际用的是 **gbs-root/local**，`run.py:6` 明确先将 export 完整复制到 GBS 期待的 source 目录。**gbs-driver/local** 的已跑通处理记录在37号第3节以及 `tools/bolt/results/runpath-fix-20261026/preparatory-corrections.json`：用户拥有 sources/repos，BUILD-ROOTS 软链接指向物理新根。本轮沿用39号 export/prep/build 脚本与参数，并采用这条已经验证的驱动目录处理，不把37号的记录误记成39号当时实际用了 gbs-driver。

令 D 为每次独立输出目录，沿用布局：

```text
D/export/
D/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/
D/gbs-driver/local/BUILD-ROOTS -> D/gbs-root/local/BUILD-ROOTS
D/gbs-driver/local/sources/tizen_base_toolchain_standard/llvm-22.1.8-1/
D/gbs-driver/local/repos/
D/tmp/
```

39号已有的 export、依赖初始化/%prep、完整GBS三步全部恢复；正常的GBS再次执行自己的%prep，不使用 `--noprep`、`--short-circuit`，不复制历史BUILD树。导出先成功退出，准备成功后再按39号 `shutil.copytree` 把完整输入就位。`export-placement.json` 对每个文件记录原导出与GBS目录SHA相同；BUILD-ROOTS链接只指向本轮物理新根。

| 项目 | 39号 | 本轮 | 差异性质 |
|---|---|---|---|
| 源码提交 | f308fe08… | 3ee2d847… | 用户指定提交替换 |
| 源码路径 | oldtext-final-20261027/source | debuglink-tb20261026/source | 路径替换，原工作树只读 |
| `-B` | oldtext-final-20261027/gbs-root | D/gbs-driver | 路径替换，采用37号已有驱动布局 |
| export、root、日志、结果 | 39号各自目录 | D下对应目录，文本结果在D/evidence | 路径替换；保留所有历史目录 |
| config / build.conf | 旧Toolchain 20261013.024319 | **同一文件、同一快照** | 无变化；build.conf SHA e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945 |
| export参数 | llvm.spec、upstream分支/tag、outdir-directly | 相同 | 除路径/提交之外0差异 |
| prep底层build参数 | uid1000:1000、x86_64、x86_64-tizen-linux、stage=-bp、debug、baselibs、两repo、三个宏 | 相同 | 除root/spec路径之外0差异 |
| 完整GBS参数 | `-A x86_64 --threads=30 --define 'jobs 8' --define '_smp_mflags -j8' --define '_costomized_smp_mflags -j20' --baselibs --style=tar --spec llvm.spec` | 相同 | 除`-B`、`-c`和源码路径之外0差异 |
| spec/CMake/ninja并行规则 | spec内mlgo_build_jobs=6、link jobs=2 | 相同 | 没有覆盖宏、改优化参数或源文件 |

上述“0差异”限定为**构建配方的argv**，不是声称控制脚本文字完全相同。`all-argv-comparison.json` 对三步逐token认证，`run.py.diff`、`prep.py.diff`、`build-runner.py.diff` 保留控制脚本差异。模板原路径/SHA见入口的 `provenance.json`。

控制层按本轮要求处理：仍是systemd-run、MemTotal减8GiB、swap0、nice10、ionice2/7；39号首次完整构建脚本没有显式CPUQuota，本轮按用户要求加1200%上限（不采用39号重启后resume的nice15/20GiB配置）。追加演练停止监控与停止后只针对本轮根的普通卸载。39号的重任务flock锁、/home余量低于20GiB停止、BOLT门禁/身份检查及资源日志保留。348测试/五项解析沿用第6节同一提交的通过记录，本轮未重跑这些前置认证。

### 8.2 两次尝试与失败原文

首次新根：`W/temp/debuglink-20261028/rehearsal-20261030/`。14:59启动，15:06已在CMake入口正常停止；**首次整轮判失败**，原因是停止后有5层本轮挂载，未满足清理要求，不是导出、依赖或%prep失败。

原文保存在 `attempt-01/result.json`、`final-audit.json`、`controller.stdout`：

```text
"status": "failed"
"reason": "residual-process-or-mount-see-final-audit"
DEBUGLINK FINISHED 2026-10-30T15:06:10.272934+08:00 status=failed reason=residual-process-or-mount-see-final-audit
```

本轮物理根中的 `/proc` 两层、`/dev/pts` 两层、`/dev/shm` 一层残留。先通过该根的platform Python检查没有进程仍以它为根，再逐层普通 `umount -n`，全部返回0。没有 `--kill`、强制或懒卸载，没有删除目录。停止整个服务后，build程序的退出清理未能消除这些挂载；具体退出清理竞态未追踪，不将其猜测成源码、GBS导出或目录权限错误。

修正仅是控制层收尾：准备结束和最终结束时，先确认自己的服务已不活动、根内无存活进程，随后只卸载该物理scratch根下允许的挂载点并复核。`final-cleanup-mounts.json` 记录每个调用。首次脚本、原始失败日志和现场完整保留；未在该根重新执行CMake/ninja。

第二次在全新 `W/temp/debuglink-20261028/rehearsal-20261030/retry-02/` 重跑相同导出/prep/GBS流程。15:14:46–15:21:27，共 **401.781秒**（约6分42秒）。首轮和第二轮都没有完整构建；没有新RPM产出。

### 8.3 第二次逐步结果与原文

以下行号均对应证据 `attempt-02/` 中原始文件，完整长CMake命令保留在日志，表中省略的仅是展示长度。

| 检查 | 结果 | 原文/证据 |
|---|---|---|
| 导出成功 | PASS | `export.stdout:4–5`：`info: package files have been exported to:`，下一行是本轮 `retry-02/export`；export rc=0 |
| GBS预期位置有完整输入 | PASS | `export-placement.json`：每个导出文件与 `gbs-driver/local/sources/tizen_base_toolchain_standard/llvm-22.1.8-1/` 中副本SHA一致 |
| 依赖安装完成 | PASS | `prep.stdout:191`：`[    8s] now installing cumulated packages`；`:317`：`[   59s] now finalizing build dir...`；随后GBS初始化也到 `rpm-build.log:533` 的 `now finalizing build dir...` |
| 单独准备的%prep成功 | PASS | `prep.stdout:325`：`Executing(%prep)`；`:391`：`[   87s] + exit 0`；prep服务rc=0 |
| 完整GBS自己的%prep成功 | PASS | `rpm-build.log:541`：`[  245s] Executing(%prep): /bin/sh -e /var/tmp/rpm-tmp.v5UXrZ`；`:607`：`[  256s] + exit 0` |
| 进入%build | PASS | `rpm-build.log:608`：`[  256s] Executing(%build): /bin/sh -e /var/tmp/rpm-tmp.fmVspt` |
| CMake配置入口 | PASS | `rpm-build.log:658`：`[  259s] + cmake -G Ninja -DTIZEN=1 -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ ... ../llvm` |
| 即时正常停服务 | PASS | `cmake-stop.jsonl`：命中时间到systemctl stop返回 **11.036毫秒**，stop rc=0；`service.stderr:4`：`Main processes terminated with: code=killed/status=TERM` |
| 没有进入主ninja编译 | PASS | 无 `+ ninja` / `Build files have been written to:`；CMake启动命令后即 `Terminated`。没有继续等待配置结束或运行编译目标 |
| 清理完成 | PASS | `final-cleanup-root-processes.json` stdout为 `[]`；5次普通卸载均rc=0；`final-audit.json` 无剩余进程/挂载，服务inactive/dead |

这里的CMake通过项是**已经走到配置命令入口并立即停止**，不是“CMake配置全部成功”；没有产生CMakeCache或build.ninja，不以这次演练推断后面的编译/链接是否成功。

实际运行时资源属性见 `prep-live-resources.txt`、`build-live-resources.txt`，包含root build/依赖进程的cgroup及nice：MemoryMax **24,482,979,840 B**（MemTotal32,297,768KiB减8GiB）、MemorySwapMax=0、CPUQuotaPerSecUSec=12s（1200%）、Nice=10、IOSchedulingClass=2、IOSchedulingPriority=7。GBS服务采样峰值 **4,019,154,944 B**，swap0，OOM/oom_kill均0；这是本次启动演练观测值，不是完整构建峰值。

停止的是本轮 `debuglink-rehearsal-20261030[-02].service`；准备服务自然结束，控制服务在检查完后自然结束。`final-preservation.json` 复核两轮全部服务均不活动、整个rehearsal子树无挂载/残留服务进程。没有停止其他任务、删除已有目录、修改VS Code设置，未操作QB或推Gerrit/sandbox。

### 8.4 晚间完整构建入口（已准备，未运行）

在终端执行这一条即可：

```sh
/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/debuglink-launch-20261030/launch.sh full
```

入口：[launch.sh](../../tools/bolt/debuglink-launch-20261030/launch.sh)，控制器：[launcher.py](../../tools/bolt/debuglink-launch-20261030/launcher.py)。shell入口通过 `/bin/sh -n`；Python代码及三份生成脚本通过语法检查。shell部分仅用POSIX sh，沿用的39号控制程序本来就是Python，不引入Bash脚本。

正式目录固定为 **`W/temp/debuglink-20261028/full-20261030/`**，交付时不存在，入口会拒绝覆盖已存在目录。与通过的演练共用同一份模板生成代码、同一配置/宏/资源/锁规则，仅输出目录和服务名不同，且 `mode=full` 不触发CMake停止监控。整个GBS流程包括正常%prep、%build、%install及打包；不切阶段短路。由持久用户systemd控制服务运行，启动命令返回后不依赖当前终端持续打开。

日志位置：`full-20261030/controller.stdout`、`controller.stderr`、`evidence/service.stdout`、`service.stderr`、`rpm-build.log`；终态在 `evidence/result.json`。正常GBS完成后写 **`build-ok-validation-pending`**，明确不把GBS退出0当作产品验证通过；任一失败保留原文与根现场。清理逻辑与通过的第二轮相同。

完整构建结束后的验证要求不变，详见 [validation-plan.md](../../tools/bolt/debuglink-launch-20261030/validation-plan.md)：身份链与profile计数、13a07cb7/8c2429d8两级SHA及新增debuglink链、39号原件35项SHA、23包payload差异及ar日期例外逐字证明、90TU完整对象字节比较、新chroot装包/LLDB自动加载及崩溃栈、包大小和符号处理/总耗时。**这些由完整构建结束后的执行任务继续核对，启动入口不自动将它们标PASS；本轮全部NOT RUN。**

证据目录：[rehearsal-20261030](../../tools/bolt/results/debuglink-20261028/rehearsal-20261030/)。`attempt-01/`保留首次失败全文，`attempt-02/`保留通过日志；`logs-manifest.json`逐文件登记行数/大小/SHA。`all-argv-comparison.json`、`export-placement.json`、`summary.json`、`final-preservation.json`、模板diff提供复核入口。第8节追加前的文档字节数/SHA见 `provenance.json`，已检查原文前缀完全不变。
