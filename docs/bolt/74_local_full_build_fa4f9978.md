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


## 5. 入口准备与演练（2026-11-11）：前置条件变化，未运行

本次计划改为固定新HEAD fea0fe464d56e17f2c7588c557bfffd9f6ac352b / tree b2e8af2477cf623a945aa80bf8288a262dd4a5a9。前面fa4f9978完整构建的第一次停止记录保持原文，不以此替换。

[78号第四次续跑](78_fifth_review_fixes.md#9-第四次续跑2026-11-11剩余验证通过gerrit状态变化停止推送)已完成10个debug ThinLTO归档输出对照、census、12组展开、5项RPM解析和提交说明检查。但sandbox推送前要求359934/357163仍为NEW，实际两者均已MERGED（PS10/PS2及revision未变）。因此没有推送，最后实际读到的远端仍为60fabc723f30c5cc04146a9dd83487ebed63f259；无法满足本步骤“远端sandbox也是fea0fe46”的核对条件。

|入口准备项|实际结果|
|---|---|
|git clone --local --no-hardlinks新源码副本|NOT RUN，目标目录未创建|
|新入口相对r2的路径/名字/授权说明diff|NOT RUN，没有复制或修改入口|
|入口自带test_*.py|NOT RUN，执行数0|
|Toolchain/Base-Dev演练argv与72号核对|NOT RUN，没有启动|
|log-restarts、FLAGS、WARNING、资源报告、残留审计|NOT RUN，没有本轮演练结果|
|night各根不存在、151.3GiB预算核对|NOT RUN，没有进入晚间启动预检|
|今晚命令、服务名和进度日志位置|尚未准备，不提供可执行命令|
|完整构建|未启动|

[只读前置查询及入口未运行记录](../../tools/bolt/results/fifth-review-20261111/rerun4/entry-not-run.json)，[change状态原文](../../tools/bolt/results/fifth-review-20261111/rerun4/push-preflight.json)。W/temp/rebase-359934-20261111-r6、B/tools/bolt/rebase-launch-20261111-r6和W/tools/bolt/rebase-launch-20261111-r6均未创建。旧入口、源码工作树及历史根未修改。需要先由用户裁决两change已经MERGED这一新状态，再继续后续准备，不能把本节视为“今晚可以启动”。

ITEM4 已结束 2026-11-11T16:58:21+08:00 status=not_run reason=sandbox_precondition_not_met


## 6. 入口准备与演练（2026-11-11）：sandbox 已更新，模板 night 调度审计停止

前面两次停止记录保留不变。本轮先完成 [78 号第五次续跑](78_fifth_review_fixes.md#10-第五次续跑2026-11-11总部合入判定bsandbox推送完成)：tizen_base 判定 B，sandbox 已从 60fabc723f30c5cc04146a9dd83487ebed63f259 更新为 fea0fe464d56e17f2c7588c557bfffd9f6ac352b；该小节先行提交并推送 bolt-v4（37d3e9d1），随后才开始本节。

### 6.1 独立源码副本：通过

执行原文：

~~~sh
git clone --local --no-hardlinks /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106/source /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/source
git -C /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/source checkout --detach fea0fe464d56e17f2c7588c557bfffd9f6ac352b
~~~

HEAD fea0fe464d56e17f2c7588c557bfffd9f6ac352b、tree b2e8af2477cf623a945aa80bf8288a262dd4a5a9、detached HEAD、工作树干净均通过。父链为 1e415935a83a187aab7c41f9713115a0974a0365 → 8a50d7122346258fd1171d270861a4ae28a8717c → 13c3e223d9e1b35e4affb55255c5042f8c940f35。复制后再次 ls-remote 确认 sandbox 仍为 fea0fe46。原工作树、源码和提交说明未改。

原文证据：[clone 身份](../../tools/bolt/results/local-entry-r6-20261111/clone-identity.json)、[clone 输出](../../tools/bolt/results/local-entry-r6-20261111/clone.stderr)、[checkout](../../tools/bolt/results/local-entry-r6-20261111/checkout.stderr)、[远端](../../tools/bolt/results/local-entry-r6-20261111/sandbox-identity.stdout)。

### 6.2 模板审计：需要超出路径/名字清单的修改，停止

没有修改模板，没有复制出新入口。逐行审计发现：

|位置|原文/行为|影响与边界|
|---|---|---|
|basedev/night.py:19|str(L.T/'launcher.py')|T 和 D 始终调用 basedev/launcher.py；L.T 是该文件目录，不随 project 改变。|
|basedev/launcher.py:28–31|temp/final-20261103/configs/ + PROJECT，Toolchain build.conf SHA e5187fd7…|T 将使用 tizen-base-toolchain_20261013.024319；而指定 toolchain/launcher.py 的配置是 tizen-base-toolchain_20261030.061318、SHA 8f201a0d…。改 SOURCE、输出根、服务名或汇总 N 不会改变这个选择。需要改调度器调用的项目入口；这不在本轮逐项列明的允许修改范围内。|
|basedev/night.py:16、21、54–55 与 launcher.py:292、308|N/project 与 rebase 输出根不同，night-…controller-20261103 与 rebase359934r2-…controller-20261106 不同|鲜根检查、结果读取和服务监控不指向实际子任务。这部分可由输出路径/服务名修改解决，但不能解决上一项和下一项。|
|basedev/night.py:58；basedev/launcher.py:35–36|L.save(N/'night-command.json',argv)；save 直接 p.write_text|新 N 不存在时写入会抛 FileNotFoundError；night.py 没有 mkdir。需要补充目录准备或创建逻辑，不能声称只替换常量就已就绪。|

以上为只读静态审计结论，没有实际启动一个错误的 night 来验证。没有把这些模板问题算成本轮获准修正的“测试输入准备错误”或“核对脚本比较了本来不同的字段”；这两类修正本轮使用 0 次。

原文和行号：[night.py](../../tools/bolt/results/local-entry-r6-20261111/template-basedev-night.py.txt)、[Base-Dev launcher](../../tools/bolt/results/local-entry-r6-20261111/template-basedev-launcher.py.txt)、[Toolchain launcher](../../tools/bolt/results/local-entry-r6-20261111/template-toolchain-launcher.py.txt)。配置实证：[旧配置](../../tools/bolt/results/local-entry-r6-20261111/config-old.txt)、[QB 同快照配置](../../tools/bolt/results/local-entry-r6-20261111/config-qb.txt)；[审计 JSON](../../tools/bolt/results/local-entry-r6-20261111/entry-template-audit.json)记录模板 SHA。

### 6.3 未运行项、预算和待用命令

|项|结果|
|---|---|
|新入口 diff、provenance、SHA256SUMS|NOT RUN；没有复制/修改新入口，无实际 diff。预定修改类别为 SOURCE、输出根、N、服务名、README 授权说明及 provenance/checksums；审计发现还需调度入口和目录准备改动，按限制停止。|
|入口自测|执行 0 项，NOT RUN；原因是复制前审计停止，不是目录没有测试。|
|T/D rehearsal-02|两者 NOT RUN；argv 未执行，无 FLAGS/log-restarts/WARNING/资源报告/残留审计结果。|
|完整构建/night|未启动。|
|新根|toolchain、basedev、rehearsal 和 night-20261111-r6 均不存在；只有独立 source 副本已创建并保留。|
|空间|277355724800 B / 258.308 GiB，大于 151.3 GiB；不是本轮停止原因。|
|服务名和进度日志|新入口尚未生成，服务名未定稿；计划汇总日志为 W/temp/night-20261111-r6/night.log，目前不存在。|

[空间原文](../../tools/bolt/results/local-entry-r6-20261111/df-before-stop.txt)、[活动服务](../../tools/bolt/results/local-entry-r6-20261111/running-services.txt)。所有本轮执行命令使用串行受限 systemd 用户服务（8G、swap 0、400%、Nice 19、idle）；没有执行 sudo 或构建命令，没有删除文件。

用户指定的**待准备命令，仅记录，当前不可启动**：

~~~sh
/bin/sh /home/linhao/Toolchain/development/llvm-optimize/tools/bolt/rebase-launch-20261111-r6/basedev/launch.sh fea0fe464d56e17f2c7588c557bfffd9f6ac352b night
~~~

不能把这条命令视为“今晚可以启动”：新入口不存在，且模板问题尚未获准修正。需要后续明确允许按项目选择已有 T/D launcher、对齐实际输出根/服务名，以及创建新汇总目录；本轮未实施这些变更。

~~~text
ITEM3 已结束 2026-11-11T17:24:03.087548+08:00 status=stopped reason=template-night-dispatch-and-summary-directory-outside-allowed-edits
~~~
