# 43. debuglink 完整构建验证：前置认证停止记录

本轮尚未产出新的 clang-debuginfo RPM，不能宣称正式包已带上匹配符号：关闭 BOLT 的 debug 模式展开比基线多一个空行，触发逐字节门禁后已停止。42 号临时实验的函数级定位结论仍有效，但本轮实际安装两个 RPM 后的自动加载与崩溃栈认证尚未运行。clang/debuginfo 包大小和完整构建耗时的影响尚未测得，不以符号文件实验大小代替新 RPM 数据。

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
