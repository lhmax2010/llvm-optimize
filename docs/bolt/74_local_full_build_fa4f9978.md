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
