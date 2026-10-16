# QB 跨架构 spec 解析修复（2026-10-16）

源提交：`af82efed1a688ba0877a4b4ca723922abbc96d20`；父提交保持 `67619ec8bbbac7238a6cfc33a481ccfbcd12206f`。作者、提交者、Signed-off-by 为 Hao Lin <hao.lin@samsung.com>，Change-Id 保持 Ic98eab90cc017f127a66e1729b44fab8b8e8fb41。

## 复现与根因

gbs 2.1.0，host rpm 4.18.2。完整命令、stdout/stderr、导出 spec、前后10行摘录、条件栈判定保存于 `tools/bolt/results/source-order-20261016/`。指定精确上游 tag `upstream/22.1.8`，正常补丁导出模式；由于本地没有 upstream 分支，显式指定既有分支 sandbox/fangyu.he/llvm_optmize 满足 gbs 的非 native 检测，不创建分支；真正源码/补丁基点由精确上游 tag 决定。gbs 日志确认为 upstream/22.1.8..源提交，得到题述七个补丁。

旧导出第66–72行 Patch0–Patch6 被第61行 `%ifarch x86_64`、第62行 `%if %{with clang_bolt}` 包住；第199–211行七条 `%patch -P N -p1` 均无条件。安装的 git-buildpackage 实现 `/usr/lib/python3/dist-packages/gbp/rpm/__init__.py` 649–680行明确采用“last Source 后插 Patch、setup 后插 patch macro”。

## 唯一源码改动

Source1200/1201 移至 Source1005 后无条件声明，删除原四条条件指令。其余 spec 字节、helper/profile/静态库转换器均保持，具体 SHA 见 source-result.json；完整源码 diff 与提交说明 diff 见 source.diff、commit-message.diff。

## QB 日志可用性

截至开工，`W/temp/qb-506dc25/` 不存在，三份日志未收到，无法独立摘录门禁数字或计算日志 SHA。用户提供的事实为：x86_64 日志第332行起依次应用 Patch0..6，构建全部通过；armv7l/aarch64 在进入 prep 前报 `error: No patch number 0`。这些目前标为用户交接事实，不能冒作本地日志核验。下方本地解析将单独记录复现原文。

## 认证与发布

新导出 PASS：Patch0–Patch6 位于第59–65行，第一条后续条件在第67行，所有 Patch 声明和七条 patch 命令均在全部条件块之外。七个生成补丁和源码/profile/helper/转换器载荷前后 SHA 相同（export-identities.json）；另一个 libcxx-runtimes.spec 仅由 gbs 更新自身 VCS tag，不属于仓库源码 diff。

实际认证使用 x86 构建根中的 rpm/rpm-build **4.14.1.1-1.4**；CLI 自报 RPM version 4.14.1。没有使用宿主4.18.2替代。该 x86 rpm 支持两个 ARM target，不需要 ARM 根。

Tizen rpmspec 不支持 --without，主解析命令采用 **rpmbuild -bp --nodeps --nobuild**，第二项逐字使用 --without clang_bolt；不会执行 prep。另用同版本 rpmspec -P 保存展开及 Source/Patch 清单，第二项仅在该辅助清单命令中用等价 _without_clang_bolt 宏。所有完整 argv、rc、stdout/stderr 均存证。

| 模式 | 506dc25 退出码/结果 | 新提交退出码/结果 | 新版 Patch |
| --- | --- | --- | --- |
| x86_64 默认开启 | 0，PASS | 0，PASS | 0–6全部 |
| x86_64 --without clang_bolt | 1，No patch number 0 | 0，PASS | 0–6全部 |
| x86_64 单行 bcond_with 回退 | 1，No patch number 0 | 0，PASS | 0–6全部 |
| armv7l-tizen-linux | 1，No patch number 0 | 0，PASS | 0–6全部 |
| aarch64-tizen-linux | 1，No patch number 0 | 0，PASS | 0–6全部 |

旧版四项原文均为：

```text
error: No patch number 0
```

新版五项 Source 清单均包含 Source0、1001–1005、1200–1201，Patch 文件名与用户指定系列一致；逐项清单见 verification-summary.json 与全部 *-expanded.stdout。关闭/ARM的 BOLT 实际执行条件没有改动。


## 准备纠正

查找时先 rg/find；源码仓库没有 .gbs.conf，转查安装的 gbs 实现与既有 refs；旧证据 broad rg 遇保护工作目录不可读，改读已定位脚本。查找阶段曾在 export 完成前查询目标 spec，文件尚未出现，未用于产品输入。提交说明导出最初用了 git show 展示层多加一个末尾换行，推送/最终认证前改用 git cat-file 原始提交正文，严格确认除指定两句外所有字节不变；本类修正一次。中断初次 after-export 并按最终 SHA 重做，正式证据仅使用后者。没有在受保护原树运行 cmake/ninja，没有 QB 操作。

## 可选 prep、资源与保护

- prep-armv7l：退出码0，34.620秒，stdout 逐行确认 Patch #0..#6 各一次。
- prep-aarch64：NOT RUN，额外图形认证未完成，代理结束多余密码框，未开始该目标的 prep；没有改用其他提权。

已执行的 ARM prep 合计 34.620秒，低于20分钟；只解包/打补丁/展开既有 MLGO 资产，没有构建。所有改写在新 overlay 的专用 /home/abuild/bolt26 下。最终包装持锁 136.386秒，4GiB/swap0/nice19/ionice3，cgroup memory.peak=4294967296B，memory.events 原文见 attempt-prep-count/final-cgroup.json。磁盘准入计20GiB预算后仍≥30GiB，结束可用 247765385216B。

最终下层 BUILD 240,718路径的类型/大小/mtime/链接目标与六个关键 SHA 全部不变，manifest SHA ee0e3adffe0c54a048236af45bebb4af1b2166edf16f5947371dbee00c856c19；所有 overlay、proc、dev 已卸载，项目锁与共享锁释放。既有原树没有运行 cmake/ninja/-P。旧尝试的上层和本次上层仅保留本地，没有动此前25号演练上层。

## 完整源码 diff（506dc25 → 新提交）

```diff
diff --git a/packaging/llvm.spec b/packaging/llvm.spec
index 56b141bec5cd..2c9b72b126a1 100644
--- a/packaging/llvm.spec
+++ b/packaging/llvm.spec
@@ -52,17 +52,13 @@ Source1002: mlgo_arm_model.tar.gz
 Source1003: mlgo_aarch_model.tar.gz
 Source1004: mlgo_x86_model.tar.gz
 Source1005: llvm-static-archives-native.py
+Source1200: clang-bolt-v2.fdata.xz
+Source1201: clang-bolt-helper.py
 
 %ifarch x86_64
 BuildRequires: util-linux
 %endif
 
-%ifarch x86_64
-%if %{with clang_bolt}
-Source1200: clang-bolt-v2.fdata.xz
-Source1201: clang-bolt-helper.py
-%endif
-%endif
 
 %{!?mlgo_build_jobs: %define mlgo_build_jobs 6}
 %{!?mlgo_verify_configure_only: %define mlgo_verify_configure_only 0}
```

## 完整提交说明 diff

```diff
--- 506dc25-message
+++ new-message
@@ -6,8 +6,13 @@
 strip all, compare-root, native archive conversion, candidate replacement,
 and one unchanged platform post chain followed by the final identity gate.
 Other architectures retain the baseline behavior. Roll back in Quickbuild
-with the one-line bcond_without -> bcond_with change; Source1200/1201 and
-BOLT-specific BuildRequires are guarded by that same x86_64 BOLT condition.
+with the one-line bcond_without -> bcond_with change; Source1200/1201 are declared
+unconditionally because gbs inserts generated Patch declarations after the
+last Source line, and conditional Sources would hide those declarations on
+other architectures and when BOLT is disabled. BOLT-specific BuildRequires
+remain guarded by the same x86_64 BOLT condition, leaving binary packages on
+other architectures unchanged while adding these two files to the source
+package.
 --without clang_bolt is available for local builds. Only enabled %build
 adds -d keeprsp. No project configuration change is required.
```

## 准备性错误完整记录

以下各类均只修正一次，没有放宽有效产品判据。全部原始异常/旧脚本/原始日志保留，通用包装器中的 PRODUCT GATE 标签对下列两种证据/参数错误并不准确，不能据此称产品失败。

- commit-message serialization：git show --format=%B adds a presentation newline; caught before final verification and push；修正：Use raw git cat-file commit body; exact bytes outside requested sentence verified. Interrupted the preliminary after-export and restarted for corrected final SHA.
- nested-repository patch verification：git apply invoked below W treated paths outside its prefix as skipped, returning 0 without editing fixture; SHA check caught it；修正：GNU patch --dry-run then apply in dedicated fixture, full spec SHA/bytes verified; W tracked files unchanged
- rpm version identity display：CLI reports RPM version 4.14.1, package version 4.14.1.1; first wrapper exited before parsing；修正：rpm -q package identity verification; complete graphical sudo -A wrapper retry, no -n or alternate elevation. Original unmount/audit PASS.
- archive root-owned overlay directories：unprivileged rename of root-owned overlay upper to a subdirectory denied; subsequent shell command lacked set -e and invoked the unchanged wrapper; one-use askpass marker refused another prompt so no root/product execution occurred；修正：Retain root-owned prior upper/work untouched; archive owned evidence files only; fresh upper-final/work-final/merged-final; set -eu in shell orchestration. No password error or cancellation.
- rpm parser CLI arguments：Tizen rpmspec -P rejects --without before parsing spec; wrapper labelled this generic failure as PRODUCT GATE but no valid product parse occurred；修正：Primary matrix uses rpmbuild -bp --nodeps --nobuild with exact --without flag after checking local --help supports both options; secondary rpmspec -P uses equivalent _without_clang_bolt macro only to collect Source/Patch headers. Preserved original unsupported-option stderr. Fresh overlay, same sudo -A, no -n/alternate elevation.
- prep transcript parsing：Regex scanned stdout+stderr and counted both Patch #N output and shell + echo lines, marking successful arm prep rc0 as FAIL；修正：Anchored ^Patch #N on stdout only; re-audited retained raw (rc0, exactly 0..6). Extra rerun invocation never entered root because graphical authentication remained unanswered; agent closed it. No claim of a new prep run.

权限过程：版本展示断言与不支持的 CLI 参数使早期包装器在有效产品验证前清理退出；另一次重复 askpass 被一次性标记拒绝，未提权。纠正准备错误后重新运行完整图形 sudo -A 包装器，因不同调用未复用认证而再次显示密码框，未使用 sudo -n、终端密码或其他提权。有效认证包装器完成挂载→十项解析→ARM prep→卸载。后续用于补跑的额外密码框未获输入，由代理结束，AArch64 可选 prep 不再请求权限，记 NOT RUN；这不影响已完成的两目标解析认证。早期 ARM prep 已成功，但证据计数器同时扫描 stdout 和 shell 回显导致重复；改为 stdout 行首匹配后对保留原文重审，确认 rc0 与七个补丁均通过；没有重写日志或伪造新 prep。须承认这比要求的一次图形输入多，原始记录完整保留。

## sandbox 与 raw

认证材料先推 GitHub：efb591178a7f52cf61d2e0719235d6858603a031；全部218项材料共436个 raw URL（分支版+钉提交版）SHA核验 PASS，索引发布于fe08dbb6c7a20c78fad6678b403381f24b6b1c54。随后按指定租约成功更新既有分支，推前/后原文：

```text
506dc25c86e4e2154150796d10b77b71d71ad6bb	refs/heads/sandbox/lhmax2025/bolt_pgo
af82efed1a688ba0877a4b4ca723922abbc96d20	refs/heads/sandbox/lhmax2025/bolt_pgo
```

实际 push 退出码0，未拒收；服务器有提交说明长度警告，按“其余说明一字不改”要求原样保留说明，没有另改内容。原始 stdout/stderr、完整 push argv 保存于 sandbox-* 与 push_sandbox.py。仅强推此已授权分支，未新建分支。

供 QB 使用：`platform/upstream/llvm@af82efed1a688ba0877a4b4ca723922abbc96d20`。

完整源码 diff 与提交说明 diff 已在上文贴全。新提交五项解析全部通过；armv7l可选prep通过，aarch64可选prep未运行，不将它冒作通过。QB日志未收到，无法独立摘录x86门禁数字；用户交接的第332行锚点已单独标明证据来源。

全部raw索引：[12](10_raw_links_part12.md)、[13](10_raw_links_part13.md)、[14](10_raw_links_part14.md)、[15](10_raw_links_part15.md)、[16](10_raw_links_part16.md)、[17](10_raw_links_part17.md)、[18](10_raw_links_part18.md)、[19](10_raw_links_part19.md)，每条都有分支版及固定提交地址。收尾发布结果在19末尾补充。QB 仍由用户控制，本任务没有操作 QB 或 refs/for/tizen_base，没有新建分支。

查找更正补记：整理证据时曾在 B 工作目录中按 W 的相对路径查找 E，首次读取即报文件不存在；产品操作前改为已经定位的绝对路径，不计准备性错误。
