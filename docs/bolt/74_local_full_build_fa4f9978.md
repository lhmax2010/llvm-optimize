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


## 7. 入口准备与演练（2026-11-11，第二次）

**准备完成，T/D 演练均通过；本轮没有启动完整构建。** 本节按用户新增授权保留旧 night.py 不用，新增 run-night.sh；前面各次停止记录原文保留。本轮不推 Gerrit/sandbox、不操作 QB、不改 LLVM 源码或提交说明。

### 7.1 前置身份与入口 diff

源码副本 W/temp/rebase-359934-20261111-r6/source 的 HEAD 为 fea0fe464d56e17f2c7588c557bfffd9f6ac352b，tree 为 b2e8af2477cf623a945aa80bf8288a262dd4a5a9，工作树干净。开始前 SSH BatchMode ls-remote 再次读到 sandbox 为同一 fea0fe46；没有写远端。结束时再次检查本地身份和工作树通过。

证据仓库 B=../llvm-optimize-bolt 是 bolt-v4 的发布工作树；用户指定 W/tools 下的执行副本与 B/tools 下的新入口逐文件相同。原 tools/bolt/rebase-launch-20261106-r2 的完整文件 SHA 清单在准备前后完全一致。

[完整 diff](../../tools/bolt/results/local-entry-r6-20261111/second/entry-vs-r2.diff)、[逐文件及精确替换审计](../../tools/bolt/results/local-entry-r6-20261111/second/final-diff-audit.json)。修改范围：

|文件|实际修改|
|---|---|
|两个 launcher.py|SOURCE 指向独立副本；完整构建/演练根改为 W/temp/rebase-359934-20261111-r6；prep/build/controller 服务前缀 rebase359934r6，日期后缀 20261111。对原文逐项替换后与新文件逐字节相同。|
|basedev/launch.sh|仅更新 usage，加入用户指定的 full basedev 分支；其他分支不变。|
|run-night.sh（新增）|分别调用两个项目自己的 shell 入口；追加汇总日志；完整根存在则拒绝；每 60 秒读取 ActiveState 并输出进度/构建日志尾行；读取 result.json；T 成功或失败均继续 D。|
|README、provenance.json、SHA256SUMS|记录 2026-11-11 一次 night 构建及白天演练授权、来源 SHA、路径和服务名。|

两个 night.py 完整内容不变，明确不使用：旧协调器固定调用 Base-Dev launcher。没有修改构建资源、构建检查、门禁、验证器或比较规则。新 run-night.sh 若读不到服务状态则停止串行调度，避免在无法确认 T 结束时启动 D；这与已确认 T 失败后继续 D 区分开。命令替换得到的状态、结果和路径在使用前检查非空；全程不读终端输入。

实际 night 运行开始才 mkdir -p W/temp/night-20261111-r6 并追加 night.log。--dry-run 不创建根、不启动服务。汇总脚本本身以前台 POSIX sh 运行，T/D 的实际工作由独立 systemd controller/prep/build 服务执行；需要保留启动终端直到串行脚本结束。没有宣称一个未创建的 night 协调器服务。

入口校验：顶层 54/54、Toolchain 子目录 27/27、Base-Dev 子目录 23/23、W 执行副本顶层 54/54，全部 sha256sum -c PASS。见 final-sha256-*.txt。所有轻量命令在串行 systemd 用户服务中，MemoryMax=8G、MemorySwapMax=0、CPUQuota=400%、Nice=19、IOSchedulingClass=idle；演练沿用入口 MemTotal−8GiB / swap0 / CPU1200% / Nice10 / ionice2/7。

### 7.2 两项目 full 配置核对

配置不依赖 full/rehearsal 模式；分别以 FINAL_PROJECT 导入实际 launcher 并执行 check_source，打印实际配置。与 77 号保全的 QB 1225393/1225395 概览、固定快照 build.conf 证据比较通过。QB 日志本身不打印 build.conf SHA，不能声称从日志直接读到 SHA；这里用其已确认快照下载证据中的 SHA 对照本地实测。没有访问或操作 QB。

**toolchain / QB 1225393：PASS**

- 快照：tizen-base-toolchain_20261030.061318
- gbs.conf：/home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/configs/toolchain/gbs.conf
- build.conf：/home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/configs/toolchain/build.conf
- SHA256：8f201a0d58eb634e60a1f213f47fc09dfa953d9869cdc5724f326a76203587bf
- packages：http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261030.061318/repos/standard/packages/
- debug：http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261030.061318/repos/standard/debug/

**basedev / QB 1225395：PASS**

- 快照：tizen-base-dev_20261030.061217
- gbs.conf：/home/linhao/Toolchain/development/llvm-optimize/temp/final-20261103/configs/basedev/gbs.conf
- build.conf：/home/linhao/Toolchain/development/llvm-optimize/temp/final-20261103/configs/basedev/build.conf
- SHA256：8ace286a5f98f2e02a79be275a64c22a86ea2b0034174c1e293381e181ce3f6a
- packages：http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Dev/tizen-base-dev_20261030.061217/repos/standard/packages/
- debug：http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Dev/tizen-base-dev_20261030.061217/repos/standard/debug/

[配置原文与对照 JSON](../../tools/bolt/results/local-entry-r6-20261111/second/configs.json)。

### 7.3 自测与准备修正

入口内全部 11 个 test_*.py 均已运行：**82 项，80 PASS，2 项模板原有 SKIP，0 FAIL/ERROR**。两项 SKIP 都是 Toolchain 的“无 Base-Dev 串行队列”不适用测试，保留原装饰器，未修改期望值。Base-Dev 的同两项未跳过并通过。新增 run-night.sh 另用 6 个隔离模拟用例，6/6 PASS。因此合计 88 项，86 PASS、2 原有 SKIP。

|项目|套件|项数|PASS|原有 SKIP|
|---|---|---:|---:|---:|
|toolchain|test_checks.py|15|15|0|
|toolchain|test_integration.py|8|8|0|
|toolchain|test_payload_overlap.py|3|3|0|
|toolchain|test_revalidation.py|9|7|2|
|toolchain|test_startup.py|5|5|0|
|basedev|test_checks.py|15|15|0|
|basedev|test_handoff_report.py|2|2|0|
|basedev|test_integration.py|8|8|0|
|basedev|test_payload_overlap.py|3|3|0|
|basedev|test_revalidation.py|9|9|0|
|basedev|test_startup.py|5|5|0|

入口中的测试文件完全未改；为避免写历史目录，运行的是新测试工作区的副本，只改输出路径，以及把相对历史结果输入改为现有绝对路径。输入 SHA/数据、测试断言和判定不变；被测模块来自新入口。原始输入逐项存在性检查通过，临时文件全部保留。副本路径 diff、每套 stdout/stderr、实际 argv/environment 都保存在本节证据目录。

[测试清单/计数](../../tools/bolt/results/local-entry-r6-20261111/second/tests.json)、[输入预检](../../tools/bolt/results/local-entry-r6-20261111/second/test-input-preflight.json)、[副本准备](../../tools/bolt/results/local-entry-r6-20261111/second/test-preparation.json)。6 个串行模拟用例是：T/D 成功、T 结果失败仍运行 D、T launcher 失败仍运行 D、服务状态空则不冒险启动 D、已存在完整根拒绝、dry-run 无副作用。只运行 stub launcher/systemctl，没有运行实际 full 构建或启动服务。[模拟结果](../../tools/bolt/results/local-entry-r6-20261111/second/coordinator-mock-results.json)。

本轮准备问题修正 **1/2 次**，不是产品 FAIL：自写 argv 核对脚本只搜索 72 号正文中的完整命令，遗漏 §7.4 链接的 Toolchain launch-command.json，报：

~~~text
Traceback (most recent call last):
  File "<stdin>", line 45, in <module>
AssertionError: toolchain
~~~

补充读取 72 号 §7.4 链接的同一次 launch-command.json 后，两条 argv 比较通过；仍严格只允许参数位置 1（入口目录）和 2（源码 SHA）不同，没有更改比较期望或产品测试。旧错误、输入定位 diff、修正后结果见 [preparation-correction-1/](../../tools/bolt/results/local-entry-r6-20261111/second/preparation-correction-1/result.json)。这次错误发生在选择基线输入时，未运行演练，也没有真实产品不一致；先前入口测试结果未受影响。

### 7.4 dry-run：命令、服务和根三者一致

对实际新入口执行 --dry-run，未创建汇总目录或完整根。用 AST 独立求值两个 launcher 在 full 模式下的根与 controller 名，和以下输出逐项一致。

~~~text
ARGV /bin/sh /home/linhao/Toolchain/development/llvm-optimize/tools/bolt/rebase-launch-20261111-r6/toolchain/launch.sh fea0fe464d56e17f2c7588c557bfffd9f6ac352b full
SERVICE rebase359934r6-toolchain-full-controller-20261111.service
ROOT /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/toolchain
RESULT /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/toolchain/evidence/result.json
ARGV /bin/sh /home/linhao/Toolchain/development/llvm-optimize/tools/bolt/rebase-launch-20261111-r6/basedev/launch.sh fea0fe464d56e17f2c7588c557bfffd9f6ac352b full basedev
SERVICE rebase359934r6-basedev-full-controller-20261111.service
ROOT /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev
RESULT /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev/evidence/result.json
LOG /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261111-r6/night.log
DRY_RUN 已结束 2026-11-11T17:40:18+08:00 status=ok
~~~

[原文](../../tools/bolt/results/local-entry-r6-20261111/second/dry-run.stdout)。run-night.sh 按 T→D 串行等待；各项目还有对应的 rebase359934r6-{project}-full-prep-20261111.service 和 rebase359934r6-{project}-full-20261111.service，均由原入口逻辑生成。

### 7.5 两次真实演练及审计

每次运行前打印完整 argv，与 72 号对应命令逐项比较，只有入口目录和 SHA 不同；D 的最后一个 basedev 参数保留。T 完成并审计通过后才启动 D，两者没有并行。命令如下：

~~~sh
/bin/sh /home/linhao/Toolchain/development/llvm-optimize/tools/bolt/rebase-launch-20261111-r6/toolchain/launch.sh fea0fe464d56e17f2c7588c557bfffd9f6ac352b rehearsal-02
/bin/sh /home/linhao/Toolchain/development/llvm-optimize/tools/bolt/rebase-launch-20261111-r6/basedev/launch.sh fea0fe464d56e17f2c7588c557bfffd9f6ac352b rehearsal-02 basedev
~~~

|审计|T（对 QB 1225393）|D（对 QB 1225395）|
|---|---|---|
|CMake 停点|PASS|PASS|
|未运行 Ninja|PASS|PASS|
|log-restarts|0|0|
|FLAGS 去掉 GBS 时间前缀后逐字相同|PASS|PASS|
|WARNING|0 条|0 条|
|原始日志/复制日志大小|58,805 / 58,805 B|58,297 / 58,297 B|
|原始日志/复制日志 SHA|相同|相同|
|资源报告生成|PASS|PASS|
|入口最终挂载/进程审计|无残留|无残留|
|结束后当前挂载/进程复查|无可见残留|无可见残留|

当前普通用户 /proc 检查的权限盲区数量保存在 audit.json，盲区不冒充已读取；同时保留入口原有、已授权清理流程生成的最终进程和挂载原文。没有额外 sudo、卸载或杀进程操作。

**toolchain FLAGS 原文**（行号来自本轮 rpm-build-final.log）：

~~~text
L623: [  180s] TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] CXXFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] LDFLAGS=[]
L625: [  180s] TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[] CXXFLAGS=[] LDFLAGS=[]
~~~

对应 QB 行号：719、721；payload 逐字相同。WARNING=0。

[审计 JSON](../../tools/bolt/results/local-entry-r6-20261111/second/rehearsal-toolchain/audit.json)、[原日志](../../tools/bolt/results/local-entry-r6-20261111/second/rehearsal-toolchain/rpm-build-final.log)、[资源报告](../../tools/bolt/results/local-entry-r6-20261111/second/rehearsal-toolchain/resource-table.md)、[最终清理原文](../../tools/bolt/results/local-entry-r6-20261111/second/rehearsal-toolchain/final-audit.json)。

~~~text
NIGHT_PROJECT 已结束 2026-11-11T17:47:29.858490+08:00 status=ok reason=rehearsal-complete-at-CMake
REHEARSAL 已结束 2026-11-11T17:48:46.073199+08:00 project=toolchain status=ok reason=CMake_flags_log_resources_cleanup_pass
~~~

**basedev FLAGS 原文**（行号来自本轮 rpm-build-final.log）：

~~~text
L574: [  325s] TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] CXXFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] LDFLAGS=[]
L576: [  325s] TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] CXXFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] LDFLAGS=[]
~~~

对应 QB 行号：670、672；payload 逐字相同。WARNING=0。

[审计 JSON](../../tools/bolt/results/local-entry-r6-20261111/second/rehearsal-basedev/audit.json)、[原日志](../../tools/bolt/results/local-entry-r6-20261111/second/rehearsal-basedev/rpm-build-final.log)、[资源报告](../../tools/bolt/results/local-entry-r6-20261111/second/rehearsal-basedev/resource-table.md)、[最终清理原文](../../tools/bolt/results/local-entry-r6-20261111/second/rehearsal-basedev/final-audit.json)。

~~~text
NIGHT_PROJECT 已结束 2026-11-11T17:58:42.962936+08:00 status=ok reason=rehearsal-complete-at-CMake
REHEARSAL 已结束 2026-11-11T17:59:14.754830+08:00 project=basedev status=ok reason=CMake_flags_log_resources_cleanup_pass
~~~

### 7.6 今晚准备：只检查，没有运行

W/temp/rebase-359934-20261111-r6/toolchain、basedev，以及 W/temp/night-20261111-r6 **均不存在**；演练根与测试副本另行保留。完整构建 controller 服务未启动。源码副本 HEAD/tree/干净状态再次核对通过。

/home 可用 **262015647744 B / 244.021 GiB**，大于 151.3 GiB，余量 92.721 GiB。[最终准备检查](../../tools/bolt/results/local-entry-r6-20261111/second/final-readiness.json)、[df 原文](../../tools/bolt/results/local-entry-r6-20261111/second/df-final.txt)。

今晚命令（本轮只打印，不执行；使用 run-night.sh，不使用旧 night 分支）：

~~~sh
/bin/sh /home/linhao/Toolchain/development/llvm-optimize/tools/bolt/rebase-launch-20261111-r6/run-night.sh fea0fe464d56e17f2c7588c557bfffd9f6ac352b
~~~

进度查看：

~~~sh
tail -f /home/linhao/Toolchain/development/llvm-optimize/temp/night-20261111-r6/night.log
~~~

完整构建、完整构建后的包/90 TU/安装/LLDB 验证本轮均未运行；本节只证明入口准备、配置、自测、dry-run 与 CMake 入口演练，不冒充完整构建通过。

ITEM4 已结束 2026-11-11T18:01:19.926722+08:00 status=ok reason=ready_not_started

ENTRY_PREP2 已结束 2026-11-11T18:03:29.724748+08:00 status=ok reason=T_D_rehearsals_pass_full_build_not_started


## 8. 入口修正与完整构建（fea0fe46）

本节记录 2026-11-11 夜间启动、2026-11-12 完成的实际结果，前面的停止与演练记录均保留。**T/D 两次 GBS 完整构建成功且无 OOM；指定 QB 的二进制包比较为 T 22/22 口径 B PASS、D 12/12 原始载荷相同。两份源码包原始比较仍为 FAIL，差异归因逐项列在 §8.6，未扩充比较器白名单。** 安装测试中 21 个 clang 崩溃帧全部具名并完成符号化交叉核对。

原入口自动验证仍报告 T failed、D ok，不能把本次补充比较改写成原队列全绿。T 的失败发生在旧 QB 基线的包比较，GBS 自身 exit_code=0；本轮按指定 QB 1225393/1225395 另做比较。

证据总目录：[local-full-r6-20261111/](../../tools/bolt/results/local-full-r6-20261111/)。源码始终为 fea0fe464d56e17f2c7588c557bfffd9f6ac352b / tree b2e8af2477cf623a945aa80bf8288a262dd4a5a9，detached 且工作树干净；[收尾复核](../../tools/bolt/results/local-full-r6-20261111/source-final.json)。未推送 Gerrit/sandbox、未操作 QB、未删除文件，旧构建根和产品源码未改。

### 8.1 串行调度修正与测试

只修改获准的 r6 run-night.sh、basedev/launch.sh、README、provenance、SHA256SUMS 与新增入口测试；两个 launcher.py、资源设置、门禁、比较器及原 r2 未改。B 发布副本与 W 执行副本一致。

- launch.sh 非零即停队列：129/130/143 原样传递，其他转 2，不启动 D。
- controller 终止后再查询该项目所有 full-* 服务；active/activating/deactivating、查询失败、result.json 缺失或无效均停止。
- T 的有效结果为 failed/stopped 且全部服务已结束时继续 D；D 启动前再次要求 /home ≥80 GiB。
- 所有停止路径打印项目和队列结束行；dry-run 不创建根或启动服务。
- Base-Dev 删除 legacy night 和 rehearsal toolchain，仅接受 full/rehearsal/rehearsal-02 basedev；usage 同步。

[完整入口 diff](../../tools/bolt/results/local-full-r6-20261111/entry-changes.diff)；[run-night.sh.diff](../../tools/bolt/results/local-full-r6-20261111/run-night.sh.diff)；[basedev-launch.sh.diff](../../tools/bolt/results/local-full-r6-20261111/basedev-launch.sh.diff)。

全部测试 **98 项：96 PASS，2 项原有不适用 SKIP，0 FAIL/ERROR**。其中原有 82 项（80 PASS、2 SKIP），新串行 mock 16/16 PASS；没有把跳过写成通过。旧测试期望没有改，路径副本差异保存在证据目录。新增 mock 覆盖用户八类场景，另覆盖信号状态、空服务状态、无效结果、根已存在和 legacy 分支拒绝。

|项目|套件|总数|PASS|原有 SKIP|
|---|---|---:|---:|---:|
|toolchain|test_checks.py|15|15|0|
|toolchain|test_integration.py|8|8|0|
|toolchain|test_payload_overlap.py|3|3|0|
|toolchain|test_revalidation.py|9|7|2|
|toolchain|test_startup.py|5|5|0|
|basedev|test_checks.py|15|15|0|
|basedev|test_handoff_report.py|2|2|0|
|basedev|test_integration.py|8|8|0|
|basedev|test_payload_overlap.py|3|3|0|
|basedev|test_revalidation.py|9|9|0|
|basedev|test_startup.py|5|5|0|
|coordinator|test_serial.py|16|16|0|

[tests.json](../../tools/bolt/results/local-full-r6-20261111/tests.json)、[16项测试原文](../../tools/bolt/results/local-full-r6-20261111/test_serial.stderr)。测试生成器曾在写入测试前因嵌套引号产生 SyntaxError，只改生成器字符串边界，没有改测试判定；[原始准备错误](../../tools/bolt/results/local-full-r6-20261111/test-generator-preparation.txt)。

### 8.2 启动、Linger 与队列原文

启动前源身份、干净状态、无其他任务、完整根不存在均通过；/home 239.601 GiB ≥151.3 GiB。[preflight.json](../../tools/bolt/results/local-full-r6-20261111/preflight.json)、[services-before.txt](../../tools/bolt/results/local-full-r6-20261111/services-before.txt)。Linger=no（[linger.txt](../../tools/bolt/results/local-full-r6-20261111/linger.txt)），启动时已明确告知：**构建期间不要注销登录**。

只执行一次后台调度命令：
~~~text
systemd-run --user --unit=rebase359934r6-night-20261111 --collect /bin/sh /home/linhao/Toolchain/development/llvm-optimize/tools/bolt/rebase-launch-20261111-r6/run-night.sh fea0fe464d56e17f2c7588c557bfffd9f6ac352b
~~~


调度、T、D 串行；没有重试。完整构建沿用原入口 MemoryMax=24482992128 B（MemTotal−8 GiB）、swap=0、CPUQuota=1200%、Nice=10、IO 2/7。入口自带的自动验证也由原 controller 执行，仍使用原入口配置；本轮随后新增的审计、包比较、函数比较和安装检查均在独立 8 GiB / swap 0 / CPU 400% / Nice 19 / IO idle 服务中串行运行。没有调整内存限制。

监控连接约 00:02 断开，恢复连接时已是 11:36，期间服务独立完成；没有声称全程人工持续观测。原 night.log 和资源采样保留。恢复时只读查询，没有重启或干预构建服务。

~~~text
NIGHT_PROJECT 已结束 2026-11-12T01:56:13+08:00 toolchain status=failed reason=controller-result-failed
NIGHT_PROJECT 已结束 2026-11-12T03:21:14+08:00 basedev status=ok reason=controller-result-ok
NIGHT 已结束 2026-11-12T03:21:14+08:00 T=failed D=ok reason=serial-builds-and-validation-finished rc=1
~~~


[完整 night.log](../../tools/bolt/results/local-full-r6-20261111/night-final.log)、[night-launch-command.json](../../tools/bolt/results/local-full-r6-20261111/night-launch-command.json)、[结束后服务状态](../../tools/bolt/results/local-full-r6-20261111/services-final.json)。

**toolchain**：GBS exit_code=0，构建 7875.23 秒；controller failed。

~~~text
{
  "status": "failed",
  "checks": {
    "QB-flags-exact": "PASS",
    "QB-three-stage-sha-exact": "PASS",
    "QB-profile-counts": "PASS",
    "anchors": "PASS",
    "debuglink-and-debugfiles": "PASS",
    "QB-23-packages": "FAIL",
    "QB-objects90": "PASS"
  }
}
~~~


~~~text
Traceback (most recent call last):
  File "/home/linhao/Toolchain/development/llvm-optimize/tools/bolt/rebase-launch-20261111-r6/toolchain/launcher.py", line 252, in worker
    stage(D, 'validation', ['python3', '-B', str(T / 'validate.py'), '--project', PROJECT, '--root', str(D), '--peer', str(D.parent / 'toolchain')])
  File "/home/linhao/Toolchain/development/llvm-optimize/tools/bolt/rebase-launch-20261111-r6/toolchain/launcher.py", line 69, in stage
    raise RuntimeError(name + ' failed, rc=' + str(r.returncode))
RuntimeError: validation failed, rc=1
~~~

[toolchain/build-result.json](../../tools/bolt/results/local-full-r6-20261111/toolchain/build-result.json)；[toolchain/entry-validation-result.json](../../tools/bolt/results/local-full-r6-20261111/toolchain/entry-validation-result.json)。

**basedev**：GBS exit_code=0，构建 3900.703 秒；controller ok。

~~~text
{
  "status": "ok",
  "project": "basedev",
  "checks": {
    "anchors": {
      "status": "PASS"
    },
    "flags": {
      "status": "PASS"
    },
    "profile": {
      "status": "PASS"
    },
    "identity-chain": {
      "status": "PASS"
    },
    "release": {
      "status": "PASS"
    },
    "objects90": {
      "status": "PASS"
    }
  },
  "historical_selftest": false
}
~~~

[basedev/build-result.json](../../tools/bolt/results/local-full-r6-20261111/basedev/build-result.json)；[basedev/entry-validation-result.json](../../tools/bolt/results/local-full-r6-20261111/basedev/entry-validation-result.json)。

### 8.3 构建审计与最终参数

|检查|T / QB 1225393|D / QB 1225395|
|---|---|---|
|GBS 完整构建|PASS|PASS|
|log-restarts|0|0|
|FLAGS 去时间前缀后逐字比较|相同|相同|
|FLAGS_WARNING|0|0|
|shell not found / NATIVE_ARCHIVES_CANCELLED / BOLT_CANCELLED|0|0|
|BOLT_POST_GATE_PASS 之后 post BOLT_DISK_REPORT|存在|存在|
|NATIVE_ARCHIVES_END|PASS 225|PASS 225|
|converted / preserved|3853 / 11|3853 / 11|
|compiler / disassembler / nm 版本|22.1.8 / 22.1.8 / 22.1.8|22.1.8 / 22.1.8 / 22.1.8|
|与对应 QB 的 profile 计数|相同|相同|

**toolchain 原文**（L 为 GBS 原始日志行号）：

~~~text
L623: [  175s] TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] CXXFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] LDFLAGS=[]
L625: [  175s] TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[] CXXFLAGS=[] LDFLAGS=[]
L24123: [ 5074s] NATIVE_ARCHIVES_TOOLS {"tool_versions": {"compiler": "22.1.8", "disassembler": "22.1.8", "nm": "22.1.8"}, "tool_directory": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin"}
L24574: [ 7044s] NATIVE_ARCHIVES_END 1794417245.101607 PASS 225
L25165: [ 7447s] BOLT_POST_GATE_PASS
L25168: [ 7447s] BOLT_DISK_REPORT {"stage": "post", "time_ns": 1794417648942525944, "recorded": true, "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt", "device": 2049, "free_bytes": 210683092992, "build": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build", "work": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt", "root": "/home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64", "scopes": ["clang-bolt/**", "tools/bolt/**", "lib64/libLLVMBOLT*.a", "bin/llvm-bolt", "ThinLTO cache positive allocation delta"], "owned_paths": [{"category": "work", "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt", "allocated_bytes": 3089846272, "logical_file_bytes": 3089831346}, {"category": "tool_objects", "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/tools/bolt", "allocated_bytes": 146677760, "logical_file_bytes": 146220305}, {"category": "tool_executable", "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-bolt", "allocated_bytes": 566870016, "logical_file_bytes": 566862784}, {"category": "tool_library", "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64/libLLVMBOLTCore.a", "allocated_bytes": 32727040, "logical_file_bytes": 32726484}, {"category": "tool_library", "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64/libLLVMBOLTPasses.a", "allocated_bytes": 58339328, "logical_file_bytes": 58331192}, {"category": "tool_library", "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64/libLLVMBOLTProfile.a", "allocated_bytes": 16060416, "logical_file_bytes": 16059382}, {"category": "tool_library", "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64/libLLVMBOLTRewrite.a", "allocated_bytes": 33910784, "logical_file_bytes": 33908010}, {"category": "tool_library", "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64/libLLVMBOLTRuntimeLibs.a", "allocated_bytes": 1105920, "logical_file_bytes": 1104318}, {"category": "tool_library", "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64/libLLVMBOLTTargetX86.a", "allocated_bytes": 3297280, "logical_file_bytes": 3294190}, {"category": "tool_library", "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64/libLLVMBOLTUtils.a", "allocated_bytes": 1228800, "logical_file_bytes": 1225252}], "owned_filesystem_bytes": {"2049": 3950063616}, "used_bytes": 3950063616, "cache_path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache", "cache_delta_known": true, "cache_delta_allocated_bytes": 0, "cache_delta_logical_bytes": 0, "cache_net_allocation_delta_bytes": -20397096960, "filesystem_device": 2049}
~~~


profile N/M/S/U/Q/R：
~~~text
{"N": 23592, "M": 144032, "S": 0, "U": 1, "Q": 383, "R": 4.238545331242318e-05, "S_over_N": 0.0}
~~~


CMake 前最终环境变量赋值原文：
~~~text
L454: [  175s] + CFLAGS=' -ffunction-sections -fdata-sections  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument   -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables  -g -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument'
L584: [  175s] + CXXFLAGS=' -ffunction-sections -fdata-sections  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument   -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables  -g -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument'
L621: [  175s] + LDFLAGS='-Wl,-z,relro,--as-needed -Wl,--gc-sections'
~~~


[全部门禁与 post 摘录](../../tools/bolt/results/local-full-r6-20261111/toolchain/required-log-excerpts.txt)；[完整 GBS 原始日志](../../tools/bolt/results/local-full-r6-20261111/toolchain/original-build.log.gz)；[审计及 QB 对照](../../tools/bolt/results/local-full-r6-20261111/toolchain/audit.json)。

**basedev 原文**（L 为 GBS 原始日志行号）：

~~~text
L574: [  248s] TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] CXXFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] LDFLAGS=[]
L576: [  248s] TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] CXXFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] LDFLAGS=[]
L24066: [ 2637s] NATIVE_ARCHIVES_TOOLS {"tool_versions": {"compiler": "22.1.8", "disassembler": "22.1.8", "nm": "22.1.8"}, "tool_directory": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin"}
L24517: [ 3804s] NATIVE_ARCHIVES_END 1794423737.4974277 PASS 225
L24905: [ 3816s] BOLT_POST_GATE_PASS
L24908: [ 3816s] BOLT_DISK_REPORT {"stage": "post", "time_ns": 1794423749920735746, "recorded": true, "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt", "device": 2049, "free_bytes": 190745182208, "build": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build", "work": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt", "root": "/home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64", "scopes": ["clang-bolt/**", "tools/bolt/**", "lib64/libLLVMBOLT*.a", "bin/llvm-bolt", "ThinLTO cache positive allocation delta"], "owned_paths": [{"category": "work", "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt", "allocated_bytes": 1429270528, "logical_file_bytes": 1429273773}, {"category": "tool_objects", "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/tools/bolt", "allocated_bytes": 16089088, "logical_file_bytes": 15612289}, {"category": "tool_executable", "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-bolt", "allocated_bytes": 47284224, "logical_file_bytes": 47280568}, {"category": "tool_library", "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64/libLLVMBOLTCore.a", "allocated_bytes": 3424256, "logical_file_bytes": 3420984}, {"category": "tool_library", "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64/libLLVMBOLTPasses.a", "allocated_bytes": 6823936, "logical_file_bytes": 6822720}, {"category": "tool_library", "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64/libLLVMBOLTProfile.a", "allocated_bytes": 1748992, "logical_file_bytes": 1748198}, {"category": "tool_library", "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64/libLLVMBOLTRewrite.a", "allocated_bytes": 3608576, "logical_file_bytes": 3607590}, {"category": "tool_library", "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64/libLLVMBOLTRuntimeLibs.a", "allocated_bytes": 163840, "logical_file_bytes": 160506}, {"category": "tool_library", "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64/libLLVMBOLTTargetX86.a", "allocated_bytes": 475136, "logical_file_bytes": 475102}, {"category": "tool_library", "path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64/libLLVMBOLTUtils.a", "allocated_bytes": 217088, "logical_file_bytes": 213124}], "owned_filesystem_bytes": {"2049": 1509105664}, "used_bytes": 1509105664, "cache_path": "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache", "cache_delta_known": true, "cache_delta_allocated_bytes": 0, "cache_delta_logical_bytes": 0, "cache_net_allocation_delta_bytes": -1509134336, "filesystem_device": 2049}
~~~


profile N/M/S/U/Q/R：
~~~text
{"N": 23592, "M": 144032, "S": 23, "U": 1, "Q": 383, "R": 0.0010172508794981563, "S_over_N": 0.0009749067480501865}
~~~


CMake 前最终环境变量赋值原文：
~~~text
L435: [  248s] + CFLAGS=' -ffunction-sections -fdata-sections  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument    -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables   -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument'
L541: [  248s] + CXXFLAGS=' -ffunction-sections -fdata-sections  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument    -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables   -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument'
L572: [  248s] + LDFLAGS='-Wl,-z,relro,--as-needed -Wl,--gc-sections'
~~~


[全部门禁与 post 摘录](../../tools/bolt/results/local-full-r6-20261111/basedev/required-log-excerpts.txt)；[完整 GBS 原始日志](../../tools/bolt/results/local-full-r6-20261111/basedev/original-build.log.gz)；[审计及 QB 对照](../../tools/bolt/results/local-full-r6-20261111/basedev/audit.json)。

逐 token 比较：CFLAGS、CXXFLAGS 都只有 T 多出 -g2、-gdwarf-4、-g，移除这三个调试 token 后顺序和重复次数也完全相同；D 没有额外 token。两边架构参数都为 -m64 -march=nehalem -msse4.2 -mfpmath=sse，没有 -mtune。LDFLAGS 完全相同：-Wl,-z,relro,--as-needed -Wl,--gc-sections。空格数量在原文中保留，[token 差异](../../tools/bolt/results/local-full-r6-20261111/final-flags-diff.json)不据此推断 T/D 机器码差异的原因。

### 8.4 资源

阶段起止按 GBS 原始日志 [NNNNs] 锚点，非采样观察时刻。下表为入口 resource-table.md 原样；各阶段 cgroup 列是采样峰值，含文件缓存，不冒充独立阶段的内核 memory.peak。

**toolchain**：全构建内核 memory.peak=24482992128 B；memory.events：low 0, high 0, max 3877, oom 0, oom_kill 0, oom_group_kill 0。swap peak=0；anon/file 未采集，均 **UNKNOWN**。

|Phase|Seconds|Cgroup sampled bytes (includes cache)|llvm-bolt VmHWM bytes|Root du sampled bytes|Filesystem min available bytes|
|---|---|---|---|---|---|
|ordinary-build|3940.0|24482992128|UNKNOWN|46199988224|208583450624|
|ordinary-install|191.0|18861355008|UNKNOWN|56534003712|195123052544|
|BOLT|749.0|19720630272|9911152640|67924271104|187207700480|
|cache-release|4.0|6185476096|UNKNOWN|UNKNOWN|190053105664|
|archive-conversion|1984.0|15945318400|UNKNOWN|52422615040|202770407424|
|platform-post|403.0|10600947712|UNKNOWN|44519174144|209042124800|
|packaging|413.0|18198597632|UNKNOWN|47027040256|208326524928|


资源样本 3887；du 132 次、50秒超时 32 次、全部非零 41 次。[非零原文](../../tools/bolt/results/local-full-r6-20261111/toolchain/du-nonzero-samples.json)；[阶段数据与边界](../../tools/bolt/results/local-full-r6-20261111/toolchain/resource-table.json)。

**basedev**：全构建内核 memory.peak=18161836032 B；memory.events：low 0, high 0, max 0, oom 0, oom_kill 0, oom_group_kill 0。swap peak=0；anon/file 未采集，均 **UNKNOWN**。

|Phase|Seconds|Cgroup sampled bytes (includes cache)|llvm-bolt VmHWM bytes|Root du sampled bytes|Filesystem min available bytes|
|---|---|---|---|---|---|
|ordinary-build|2226.0|11902005248|UNKNOWN|11207655424|192575094784|
|ordinary-install|4.0|8761819136|UNKNOWN|UNKNOWN|191307046912|
|BOLT|157.0|18123169792|9924120576|13375045632|189562822656|
|cache-release|1.0|8222638080|UNKNOWN|UNKNOWN|189562437632|
|archive-conversion|1168.0|8333471744|UNKNOWN|14028967936|189830004736|
|platform-post|14.0|7196106752|UNKNOWN|UNKNOWN|190611931136|
|packaging|71.0|10406600704|UNKNOWN|13605498880|190077300736|


资源样本 1941；du 66 次、50秒超时 0 次、全部非零 0 次。[非零原文](../../tools/bolt/results/local-full-r6-20261111/basedev/du-nonzero-samples.json)；[阶段数据与边界](../../tools/bolt/results/local-full-r6-20261111/basedev/resource-table.json)。

实际采样方式：约每2秒采 cgroup/文件系统，约每60秒由入口既有 chroot sudo -n 调用 du -sx -B1 /，单次50秒超时。T 的32次超时、其余9次非零样本均未估算补齐；D无超时。未启用入口不支持的10秒/5分钟新模式，构建根占用是成功 du 样本的峰值，下界而非连续精确峰值。T采样磁盘峰值67924271104 B，D14028967936 B；最小文件系统剩余见表。

### 8.5 BOLT 输入及改写日志保全

ELF 副本保存于 W/temp/local-full-r6-20261111-materials/{toolchain,basedev}/reference-relocs-clang-22，来源是各自 helper 实际 pipeline 输入；历史原文件只读。

|项目|输入字节数|SHA256|
|---|---:|---|
|toolchain|226816920|ae3d837d862673b03c3c4718f6746f6986d8abe2078bad426b97905258b91a5c|
|basedev|226782848|bf15cf062439714651809cd3b5ca82619407081adca64ceb65699e6ccae50501|


[toolchain BOLT 改写日志原文](../../tools/bolt/results/local-full-r6-20261111/toolchain/rewrite-bolt.log)；[来源/大小/SHA](../../tools/bolt/results/local-full-r6-20261111/toolchain/rewrite-log-copies.json)；[输入身份](../../tools/bolt/results/local-full-r6-20261111/function-comparison/toolchain-bolt-input-command.json)。

[basedev BOLT 改写日志原文](../../tools/bolt/results/local-full-r6-20261111/basedev/rewrite-bolt.log)；[来源/大小/SHA](../../tools/bolt/results/local-full-r6-20261111/basedev/rewrite-log-copies.json)；[输入身份](../../tools/bolt/results/local-full-r6-20261111/function-comparison/basedev-bolt-input-command.json)。

### 8.6 与指定 QB 的逐包比较及源码包归因

使用67号§8.1口径B，Release 从两边RPM头取得：本地T/D均1，QB T为2.1、D为5.1。实际RPM身份、VCS和SHA见各项目 comparison/rpm-identities.json。RPM头时间、release、payload mtime分别记录；不借此跳过文件内容。QB下载文件先按77号receipt复核SHA。

T的非调试代码/数据保持相同；.debug及其debuglink按已批准release前缀规则通过，所以“口径B PASS”不等于这些调试文件原始SHA相同。D12个二进制包内容SHA全部直接相同。T的debugsource前缀路径映射后文件内容相同。

|包|T 对 1225393|D 对 1225395|
|---|---|---|
|clang|PASS|PASS|
|clang-debuginfo|PASS|无此包|
|clang-devel|PASS|PASS|
|clang-devel-debuginfo|PASS|无此包|
|compiler-rt|PASS|PASS|
|compiler-rt-debuginfo|PASS|无此包|
|libllvm|PASS|PASS|
|libllvm-debuginfo|PASS|无此包|
|libomp|PASS|PASS|
|libomp-debuginfo|PASS|无此包|
|libomp-devel|PASS|PASS|
|lldb|PASS|PASS|
|lldb-debuginfo|PASS|无此包|
|lldb-devel|PASS|PASS|
|lldb-devel-debuginfo|PASS|无此包|
|llvm|PASS|PASS|
|llvm-debuginfo|PASS|无此包|
|llvm-debugsource|PASS|无此包|
|llvm-devel|PASS|PASS|
|llvm-devel-debuginfo|PASS|无此包|
|llvm-src|FAIL|FAIL|
|llvm-static-devel|PASS|PASS|
|python-clang|PASS|PASS|

[T每文件结果（含允许的逐节差异）](../../tools/bolt/results/local-full-r6-20261111/toolchain/comparison/packages.json.gz)；[D每文件结果](../../tools/bolt/results/local-full-r6-20261111/basedev/comparison/packages.json)。源码包原始FAIL保留，没有为了得到PASS修改规则。

每组 llvm-static-devel 的225个归档、3864个实际成员（3853转换+11原样保留）都逐成员计算并比较SHA，全同；合计 **7706个转换成员 + 22个原生成员**。额外连同其他包的归档，每组271归档、5829成员全部通过；完整归档SHA也相同。[T全量成员](../../tools/bolt/results/local-full-r6-20261111/toolchain/comparison/static-members.json.gz)、[D全量成员](../../tools/bolt/results/local-full-r6-20261111/basedev/comparison/static-members.json.gz)。这次确实运行了逐成员比较。

源码包逐项事实：

- spec/helper/转换器的差异来自 fea0fe46 对60fabc72，完整diff随比较结果保全；spec还含VCS、Release和GBS/QB的Patch/%patch写法差异。
- Source1200、模型tar、llvm.manifest 的内容SHA相同，只存在0664/0644权限差异；与设计第7节第8条的源码包权限环境差异单列。
- QB把8个补丁作为独立source文件；本地GBS将已应用补丁的源码直接导出tar，因而没有独立0001–0008。只在新临时目录应用QB八个补丁，27个受影响文件核对通过；没有改历史构建根。
- 对两个tar逐文件流式核对184839/184826条目。应用QB补丁之后，除下述14项（含一个目录）外，全体路径/type/size/mode/link/内容SHA相同。
- 本地多出的packaging/目录及12个文件，内容都逐个与 fea0fe46 的git对象SHA相同，属于GBS导出整个Git tree而QB使用上游tar的组织差异。
- 唯一共有文件差异为 clang/bindings/python/.git_archival.txt：git archive 的提交身份展开。本地node=fea0fe46，QB上游tar node=ca7933e4；原文如下。该差异已经定位，但不把它偷偷加入既有白名单，源码包仍保留原始FAIL。

local
~~~text
node: fea0fe464d56e17f2c7588c557bfffd9f6ac352b
node-date: 2026-11-11T15:13:45+08:00
describe-name: llvmorg-14-init-170503-gfea0fe464d56
~~~


qb
~~~text
node: ca7933e47d3a3451d81e72ac174dcb5aa28b59d1
node-date: 2026-06-15T22:33:53+00:00
describe-name: llvmorg-14-init-170484-gca7933e47d3a
~~~


本地tar354741498 B / 2ef564ef162f8f184199196a51886c58c356741b38628f4ca2fda7affc94d722；QBtar258009434 B / 1f5fe8da0a18255a63cde36f1570c88265bb8ffc6458deae06d04e77abc6f7d2。T/D各自的两个tar SHA均相同，因此同一份内容归因覆盖两组。

[全部14项差异与补丁清单](../../tools/bolt/results/local-full-r6-20261111/source-attribution.json)、[12个packaging文件Git核对](../../tools/bolt/results/local-full-r6-20261111/source-extra-packaging-git-check.json)、[tar及归档标识](../../tools/bolt/results/local-full-r6-20261111/source-container-details.json)。tar全文件SHA清单：[本地](../../tools/bolt/results/local-full-r6-20261111/source-local-tar-manifest.json.gz)、[QB原始](../../tools/bolt/results/local-full-r6-20261111/source-qb-tar-manifest.json.gz)。没有无法定位的代码文件差异；以上事实不等于未经裁决把源码包改判PASS。

### 8.7 T/D 函数差异（只记录事实）

通过各自构建根的loader运行平台llvm-objdump --disassemble --no-show-raw-insn，在8GiB服务中流式处理成功。按可识别符号名及同名出现序号对齐；去掉指令行首地址，但保留操作数字面地址。计数包含地址引起的文本差异，不能据此认定对应数量的函数算法或性能改变。最终strip后的文件只覆盖objdump仍能识别的符号范围。

|比较|T函数记录|D函数记录|完全相同记录|仅入口地址不同|指令文本/条数不同|只在T/只在D的名字|
|---|---:|---:|---:|---:|---:|---|
|bolt-input|144380|144380|347|13284|127206|3543/3543|
|final-clang|51827|51827|75|5793|45959|0/0|

完整差异函数名/地址/文本SHA：[BOLT输入](../../tools/bolt/results/local-full-r6-20261111/function-comparison/bolt-input-different-functions.json.gz)、[最终clang](../../tools/bolt/results/local-full-r6-20261111/function-comparison/final-clang-different-functions.json.gz)。未归一化 .llvm 数字后缀，没有下因果结论；完整反汇编四份约234–247MB gzip各自留在本地证据目录，[完整路径/大小/SHA索引](../../tools/bolt/results/local-full-r6-20261111/large-local-artifacts.json)，未上传超GitHub单文件限制的原文；逐函数清单与差异已上传。

### 8.8 T RPM 安装与 LLDB

遵守“不执行额外sudo”：预检rootless bwrap用户namespace可用，在新 W/temp/local-full-r6-20261111-install/root 内实际rpm --initdb、--noplugins --nodeps -ivh安装本次clang与clang-debuginfo。运行库/工具从本次T根只读复制，完整依赖闭包和10条rpmpopt exec预检通过；不是在历史chroot里装包。namespace内uid0只映射当前普通用户，无宿主root权限。

这与43号sudo chroot的提权机制不同，测试对象和崩溃方法相同：LLDB仅打开/usr/bin/clang-22，自动加载/usr/lib/debug/usr/bin/clang-22.debug；真实SIGILL崩溃，core关闭。

结果：安装SHA与RPM载荷一致，debug文件0644，debuglink CRC32匹配；**21/21 clang帧具名，21/21与llvm-symbolizer同地址名称相同**；另6个冷函数抽查一致。

~~~text
Preparing...                          ########################################
Updating / installing...
clang-debuginfo-22.1.8-1              ########################################
clang-22.1.8-1                        ########################################
clang-22.1.8-1.x86_64
clang-debuginfo-22.1.8-1.x86_64
~~~


安装身份：
~~~text
{
  "usr/bin/clang-22": "e08724d81231d8675c51d4908f4ff0e8d233ef3740c878da1c7eda42dd3532f5",
  "usr/lib/debug/usr/bin/clang-22.debug": "9942e19c75ffef55f2846e6f1ea60651b4502de6e099c038a3d93bad4f5df690"
}
~~~


[LLDB完整原文（image list/lookup/bt all）](../../tools/bolt/results/local-full-r6-20261111/install/lldb-auto.stdout)、[install/symbolizer.stdout](../../tools/bolt/results/local-full-r6-20261111/install/symbolizer.stdout)、[21帧/冷函数逐项及清理](../../tools/bolt/results/local-full-r6-20261111/install/result.json)、[复制来源与SHA](../../tools/bolt/results/local-full-r6-20261111/install/copied-files.json.gz)；完整argv保存在install/*-command.json。

清理：所有bwrap进程已返回，临时proc/dev等namespace挂载随退出回收，未做宿主挂载/卸载。findmnt返回0，无测试根挂载；可读/proc中无测试根cwd/root/exe进程。306个外部进程有普通用户权限盲区，明确保留这个限制；未提权查看。根和RPM均保留。

### 8.9 收尾与边界

/home收尾可用 154250567680 B（143.657 GiB）；[df-final.txt](../../tools/bolt/results/local-full-r6-20261111/df-final.txt)。比较解包、函数反汇编、安装根与全部产物均保留，未删除任何文件。

原入口自动完成的90 TU结果为T、D均PASS（不是本次额外重跑的检查），其原result已保全。本轮未运行新QB、额外完整构建、性能测量或函数差异因果实验。没有OOM，未提高限制或重试失败构建；T原自动验证失败和源码包原始FAIL均未隐藏。

本次结论：构建和指定QB二进制/静态成员验证完成，安装符号检查通过；源码包组织/归档标识差异已定位但严格原比较为FAIL，不能写“整包全部逐字节相同”。

~~~text
NIGHT_PROJECT 已结束 2026-11-12T01:56:13+08:00 toolchain status=failed reason=controller-result-failed
NIGHT_PROJECT 已结束 2026-11-12T03:21:14+08:00 basedev status=ok reason=controller-result-ok
NIGHT 已结束 2026-11-12T03:21:14+08:00 T=failed D=ok reason=serial-builds-and-validation-finished rc=1
AUDIT 已结束 2026-11-12T11:37:14.186866+08:00 toolchain status=recorded
AUDIT 已结束 2026-11-12T11:37:19.808416+08:00 basedev status=recorded
AUDIT_ALL 已结束 2026-11-12T11:37:19.810006+08:00
FUNCTION_COMPARE 已结束 2026-11-12T12:07:42.084940+08:00 result={"bolt-input": {"status": "recorded", "toolchain_functions": 144380, "basedev_functions": 144380, "different_functions": 147576, "identical_function_records": 347, "scope": "functions identified by llvm-objdump from available symbols; instruction leading addresses removed, operand addresses retained; includes address-only differences; no causal claim"}, "final-clang": {"status": "recorded", "toolchain_functions": 51827, "basedev_functions": 51827, "different_functions": 51752, "identical_function_records": 75, "scope": "functions identified by llvm-objdump from available symbols; instruction leading addresses removed, operand addresses retained; includes address-only differences; no causal claim"}}
INSTALL_LLDB 已结束 2026-11-12T12:08:57.826486+08:00 status=ok phase=symbolizer
LOCAL_FULL_R6 已结束 2026-11-12T12:13:57.322734+08:00 status=completed_with_differences reason=builds_ok_binary_policyB_pass_source_raw_FAIL_attributed
~~~


文档生成阶段另有一次读取 JSON 层级的 KeyError（在写文档之前），只修正报告生成器的 data/ counts 层级，未修改测试、比较判据或产物；[原文](../../tools/bolt/results/local-full-r6-20261111/report-generator-error.txt)、[修正 diff](../../tools/bolt/results/local-full-r6-20261111/report-generator-correction.diff)。


### 8.10 PM 裁决

2026-11-12，以下为用户裁决；不改原始证据或 §8.6 的原始 FAIL。

R1 T 的 controller status=failed，唯一来源是入口内置检查 QB-23-packages 用了过时的 r2 模板基线；其余 6 项 PASS。这不是产品失败，以 §8.6 的规则 B 比较为准。原 result.json 不动。

R2 第 8 条定案。本地 GBS 对 QB 源码包的“已知差异固定清单”只有以下五项，清单外任何差异仍判 FAIL：

- (a) 内容 SHA 相同、只有权限 0664/0644 不同的文件：Source1200、模型 tar、llvm.manifest；

  **PM 修正（2026-11-12T21:00:58.812766+08:00，原文保留）：** R2(a) 由“指定文件名清单”改为按规律判定：源码包中内容 SHA 相同、仅权限为本地 0664 对 QB 0644（只差组写位）的文件，属于已知差异。其他任何权限变化（含可执行位、属主、其他位）仍判 FAIL。

  原因：原清单是 PM 起草时漏列。74 号比较的是 60fabc72 的 QB，helper 和转换器当时内容不同，权限差异被内容差异覆盖；同提交比较时才暴露。来源相同，都是本地 GBS 导出的权限。

- (b) QB 把补丁 0001–0008 作为独立 source 文件，本地 tar 里补丁已经应用；应用 QB 补丁后，受影响的文件必须逐个一致；
- (c) 本地多出 packaging/ 目录及其文件，每个文件的内容必须与当次提交的 git 对象 SHA 一致；
- (d) clang/bindings/python/.git_archival.txt 的 node、node-date、describe-name 三行；
- (e) spec 中的 VCS、Release，以及 Patch/%patch 写法差异。

比较报告把“原始结果”和“按第 8 条清单归类后的结果”分开展示，原始 FAIL 照常保留。

R3 74 号放行：fea0fe46 本地 T/D 完整构建通过上传门槛。

R4 决策 18：通用级和建议级的加固项推迟到上传后的跟进补丁；第 7 轮评审只做定向检查，不阻塞上传；评审只看问题是否严重。

R5 T 的 memory.peak 等于 MemoryMax，触顶事件 3877 次，无 OOM。作为资源数据记入，现在不处理。

R6 T/D 函数差异只记录事实，因果留给以后的归因实验。
