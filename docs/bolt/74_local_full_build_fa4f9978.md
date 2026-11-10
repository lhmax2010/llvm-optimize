# 74. fa4f9978 本地 T/D 完整构建：入口核对停止

**本次没有启动任何完整构建。** 第零步通过：无其他 Codex 任务服务运行，指定提交/tree 正确，/home 可用 313.113 GiB，大于 151.3 GiB。第一步只读入口核对发现 Base-Dev shell 入口没有 full 模式，且两个入口固定读取的源码工作树 HEAD 不是 fa4f9978；按“不符就停止”保留现场，没有修改入口、切换源码或绕过入口。

## 1. 前置条件

全部命令串行运行于独立 systemd 用户服务：MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、Nice=19、IOSchedulingClass=idle。没有构建，因此没有启用完整构建的 MemTotal−8GiB/1200% 资源规则。没有 sudo、Gerrit/sandbox/QB 操作、删除文件或历史根写入。

[服务列表](../../tools/bolt/results/local-full-fa4f9978-20261110/running-services.txt)：除本轮前置检查自身，其他活动服务为桌面/用户基础服务，没有 76 号或其他 Codex 任务服务。未读取 sandbox HEAD。

|项|结果|
|---|---|
|本地提交|fa4f9978c9162d3c6cd2113d0cfe1173f04881c8 存在|
|tree|c9f61c77a1a08f5faffd45f8a37f6b46359922f7，符合要求|
|初次可用空间|336202661888 B / 313.113 GiB|
|记录时可用空间|336202637312 B / 313.113 GiB|
|最低要求|151.3 GiB|
|缺口|0 GiB|

~~~text
Filesystem         1B-blocks          Used    Available Use% Mounted on
/dev/sda1      1967844950016 1531605700608 336202637312  83% /home
~~~

[核对 JSON](../../tools/bolt/results/local-full-fa4f9978-20261110/preflight.json)、[源码身份](../../tools/bolt/results/local-full-fa4f9978-20261110/source-identity.txt)、[df](../../tools/bolt/results/local-full-fa4f9978-20261110/df-before.txt)。

## 2. 待执行 argv 与停止依据

以下是从 72 号同一入口的 rehearsal-02 命令仅改模式为 full 后得到的命令，**只打印，没有执行**：

~~~sh
/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/rebase-launch-20261106-r2/toolchain/launch.sh fa4f9978c9162d3c6cd2113d0cfe1173f04881c8 full
/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/rebase-launch-20261106-r2/basedev/launch.sh fa4f9978c9162d3c6cd2113d0cfe1173f04881c8 full basedev
~~~

Base-Dev 最后的 basedev 参数保留，与 72 号第 234 行逐项比较，仅 rehearsal-02 → full；但是 shell 入口不接受这个 full 分支。原入口全文：

~~~sh
#!/bin/sh
set -eu
[ "$#" -ge 2 ] || { echo 'usage: launch.sh SOURCE_SHA night | launch.sh SOURCE_SHA rehearsal toolchain|basedev' >&2; exit 2; }
NIGHT_SOURCE_SHA=$1; export NIGHT_SOURCE_SHA
shift
case "$1" in
 night) [ "$#" -eq 1 ] || exit 2; exec python3 -B "$(dirname "$0")/night.py" ;;
 rehearsal|rehearsal-02) [ "$#" -eq 2 ] || exit 2; case "$2" in toolchain|basedev) FINAL_PROJECT=$2; export FINAL_PROJECT ;; *) exit 2 ;; esac; exec python3 -B "$(dirname "$0")/launcher.py" "$1" ;;
 *) exit 2 ;;
esac
~~~

其 *) exit 2 会拒绝 full basedev。night 模式不能替代：它既不是上述演练命令仅模式的对应变化，也不保留规定的最后 basedev 参数；没有自行调用 night 或直接执行 launcher.py。

两个 launcher.py 另有固定路径和 HEAD 检查：

~~~python
SOURCE = W / 'temp/rebase-359934-20261106/source'
assert rev[0] == COMMIT and not status, (rev, status)
~~~

该路径当前 HEAD 为 **60fabc723f30c5cc04146a9dd83487ebed63f259**。第零步只要求 fa4f9978 对象存在，已通过；但实际启动入口要求 HEAD 本身等于传入 fa4f9978，当前不符。没有把这误记成目标对象不存在，也没有读取或依赖远端 sandbox。

计划根目录由现有入口固定为 W/temp/rebase-359934-20261106-r2/toolchain 和 basedev，存在情况见 preflight.json；没有创建或复用它们。入口文件 SHA、全文及行号摘录保全：[Toolchain](../../tools/bolt/results/local-full-fa4f9978-20261110/toolchain/launch.sh)、[Base-Dev](../../tools/bolt/results/local-full-fa4f9978-20261110/basedev/launch.sh)、[摘录](../../tools/bolt/results/local-full-fa4f9978-20261110/entry-excerpts.txt)。本次没有尝试运行会被拒绝的命令。

继续本任务需要先明确获准的完整构建入口和 fa4f9978 本地源码视图。按本任务“不改入口脚本”和“argv 不符就停止”的约束，本轮不自行修补，也不把直接调用 Python 当作原 shell 入口通过。

## 3. 构建、审计及比较状态

|要求|T|D|说明|
|---|---|---|---|
|完整构建|NOT RUN|NOT RUN|启动前停止|
|FLAGS、WARNING、log-restarts、shell not found|NOT RUN|NOT RUN|无本轮构建日志|
|BOLT profile/post disk report、PASS225/3853/11|NOT RUN|NOT RUN|不沿用 QB 或历史构建结果|
|转换器版本间接满足|NOT RUN|NOT RUN|只有本次 NATIVE_ARCHIVES_END PASS 才能判间接满足|
|资源、GBS 阶段耗时、anon/file、磁盘峰值|UNKNOWN|UNKNOWN|未产生本轮采样；不估算、不借用|
|BOLT 输入 ELF 副本与改写日志|NOT RUN|NOT RUN|没有新构建产物，未复制历史产物代替|
|对 QB 1223601/1223602 的逐包/逐成员比较|NOT RUN|NOT RUN|本地本轮产物不存在|
|T/D BOLT 输入及最终 clang 函数差异|NOT RUN|NOT RUN|未运行 llvm-objdump|
|T RPM install/LLDB 21 项|NOT RUN|—|无本轮 RPM，未执行 sudo|

构建未开始，因此没有声称启用“10 秒文件系统采样/5 分钟分层 du”；实际运行采样方式亦无本轮结果。没有 OOM、构建失败或重试；这是入口前置核对的停止记录。

## 4. 结束记录与进度查看

~~~text
ITEM0 已结束 2026-11-10T23:30:01+08:00 status=ok reason=services_commit_tree_disk_pass
ITEM1 已结束 2026-11-10T23:30:01+08:00 status=stopped reason=basedev_shell_entry_has_no_full_mode_and_source_HEAD_mismatch
ITEM2 已结束 2026-11-10T23:30:01+08:00 status=not_run reason=build_not_started
ITEM3 已结束 2026-11-10T23:30:01+08:00 status=not_run reason=build_not_started
ITEM4 已结束 2026-11-10T23:30:01+08:00 status=not_run reason=build_not_started
LOCAL74 已结束 2026-11-10T23:30:01+08:00 status=stopped reason=entry_preflight_blocked
~~~

目前没有运行中的构建服务。下面只查看本次停止记录，不代表构建已启动：

~~~sh
tail -f /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/local-full-fa4f9978-20261110/progress.log
~~~
