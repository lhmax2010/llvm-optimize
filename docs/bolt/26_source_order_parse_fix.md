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

进行中：新导出与两份五项 Tizen RPM 解析；尚未更新 sandbox。

## 准备纠正

查找时先 rg/find；源码仓库没有 .gbs.conf，转查安装的 gbs 实现与既有 refs；旧证据 broad rg 遇保护工作目录不可读，改读已定位脚本。查找阶段曾在 export 完成前查询目标 spec，文件尚未出现，未用于产品输入。提交说明导出最初用了 git show 展示层多加一个末尾换行，推送/最终认证前改用 git cat-file 原始提交正文，严格确认除指定两句外所有字节不变；本类修正一次。中断初次 after-export 并按最终 SHA 重做，正式证据仅使用后者。没有在受保护原树运行 cmake/ninja，没有 QB 操作。
