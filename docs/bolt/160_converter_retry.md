# 160 · 归档转换 OOM 串行重试

## 转换器

本地 `pgo-dev` 配方为 `ce627fa087233d9da415887222009155fe8b5029`。转换器 CLI 默认不重试。开启后，只有正常退出并在成员编译 stderr 报告 LLVM OOM 或明确分配失败的调用进入队列。并行池结束后，按成员顺序一次只重跑一个，首次和重试的命令回执保留为 `convert.json` 和 `convert-retry.json`。退出信号、超时及其他错误走失败路径。重试仍失败则该构建失败。

R 的 `llvm.spec` 有一个归档转换调用，按 BOLT 开关选择两条后缀。两条均保留 worker 数 4 和原 4 GiB 上限，新增 8 GiB 串行重试上限。Tizen RPM 4.14.1 对 x86_64 的默认、关闭 BOLT、关闭总开关三组，以及 aarch64、armv7l 默认展开均通过。ARM 延续现有 spec 的架构范围。

`process()` 在重试时读取该成员已保存的 `ir-settings.json`，使用同一 bitcode、输出路径和 Clang 参数。地址空间值仅传给 `Commands.run()` 构造的 `prlimit --as`，两次调用的编译器 argv 一致。符号、重定位和 native 归档检查仍执行。测试中的真实 GNU ar 输出与改动前逐字节相同，未产生重试行。实际成员用量由后续 QB 和本机 G4 回执核验。

5/5 定向测试通过，包括两成员串行成功、二次 OOM 失败、普通错误与默认禁用、无失败字节一致、明确 ENOMEM 诊断。第一次测试夹具缺少 mock 归档收据中的 SHA 与大小，已补齐夹具。离线技能直接调用源码配方中的转换器，目录中没有独立的转换器副本。技能说明已同步加入重试与 RSS 取证要求。

[产品补丁](../../tools/bolt/results/task160/archive-retry.patch) · [单测](../../tools/bolt/results/task160/archive-tests.txt) · [RPM 核对](../../tools/bolt/results/task160/spec-checks.json)

## 备份压缩

29 个仓库中，3 个对象库重打包并删除，3 个自测库已打包但保留原目录，23 个因属主或父目录权限保留。自测库还有独立对象和未提交的工作树/index 数据。打包使用只存在于临时对象库的 `refs/lost`，逐项核对现有 ref 和新增 lost ref。每个被删库的镜像克隆核对了 ref 与对象集合。临时验证目录按原流程清理。

49 个非 Git 条目中，48 个通过同文件系统 rename 移到 `archive/backup-unique/task160/non-git/`，内容共 24,640 B。剩下一个 7,095,491 B 的历史 bundle 因父目录权限保留，原路径及 SHA256 已登记。归档 bundle 存在 `archive/backup-unique/task160/bundles/`。

开始与结束的 /home 可用字节为 273,691,967,488 → 273,580,232,704。同期文件系统净变化为 −111,734,784 B，不能把全盘变化视作这三个小库本身的释放量。这轮整理未达到 154-B 的磁盘准入线。

[备份仓库、现有/lost refs、bundle SHA256、文件移动的逐项记录](../../tools/bolt/results/task160/backup-results.json)

## PGO-only 候选

集成提交 `dc690a0660683830f653d71a8025c10e4a6b3fd8`，QB 测试提交 `7a54d3ff49841eb4753453813ed68d9f2e63d405`。静态核对三架构均通过，x86_64 的 PGO 开启、BOLT 关闭。集成提交保留 UNQUALIFIED、生产门禁继续拒绝。QB 测试提交仅允许此状态，通过 profile SHA256、大小和映射检查。第一次新建分支推送在 Git 对象打包时超时。已先核对远端仍无该分支，再以相同提交和新建专用 hook 重试。

[157 脚本变更](../../tools/bolt/results/task160/157-candidate-update.diff) · [第一次推送结果](../../tools/bolt/results/task160/candidate-a/first-push-result.json)

## 重跑编排

`llvm-opt-task160-g-chain.service` 已排队，等待 154-B 退出且其最终证据已推送并可从远端 bolt-v4 追溯。它继续使用 151 的准入和看门狗。G6 等待截止 11 月 27 日 06:00 PST，总截止当天 20:00 PST。G4 记录每个重试行和成员 RSS 回执，G6、G7、G8 均 PASS 才准备 157-B。

G1–G3 的输入与产物字节及 SHA256 已核对。保留原插桩来源，G4 以新配方身份开始，复用同一 G3 profdata。编排与队列 **10/10** 测试通过，离线技能 **60/60** 测试通过。dry-run 已生成，未开始 G4 构建。

[154-B 初始等待状态](../../tools/bolt/results/task160/154-wait-initial.json) · [G3 复用核对](../../tools/bolt/results/task160/recover-g3.json) · [G4–G8 dry-run](../../tools/bolt/results/task160/g4-g8-dry-run.json)
