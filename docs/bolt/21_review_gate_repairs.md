# 21 续跑九：外部评审门禁修复

## 人工裁决与边界

Quickbuild 旧 tool-plan 会误拒绝 BOLT 静态库；用户取消该轮。本轮不推任何 Gerrit 分支，只更新 GitHub bolt-v4。候选生成命令及参数不改，历史后备候选 SHA256 4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9 必须保持。新源提交以 a1410e3d 为父，周五再整理。

Quickbuild 参数及项目配置不可改，x86_64 保持 `%bcond_without clang_bolt` 默认开启；本地 `--without clang_bolt` 用于零影响核对。Quickbuild 回退须提交 spec 新提交，将 x86_64 改为 `%bcond_with clang_bolt`，正式提交说明必须包含该方式。

沿用锁/资源/磁盘/保护规则；不在原树运行 cmake/ninja/-P，不进行新配置，不进入 ARM 树。查找先 rg/find；产品准备错误每类只准修正一次；产品门禁失败立即停止。

## 第一步 tool-plan

保存的配置快照离线递归遍历 llvm-bolt 全部显式、隐式与 order-only 依赖，展开 rule/edge 的 description 变量，没有运行 Ninja。闭包 1911 条边：普通 1792（含有 command 的 1715）；新增 BOLT phony 9；新增实际任务 110。普通边在 Quickbuild 应已最新，出现在 dry-run 一律拒绝。

描述全集：102 个 `Building CXX object tools/bolt/...`；7 个 `Linking CXX static library lib64/libLLVMBOLT{Core,Passes,Profile,Rewrite,RuntimeLibs,TargetX86,Utils}.a`；1 个 `Linking CXX executable bin/llvm-bolt`。逐条原文与边见 review-tool-descriptions.json 和 review-closure.json.xz。

helper 用全集的精确字符串白名单。每行必须完整匹配 `[f/t] 描述`，计数有效，不允许噪声、未知 Generating/Creating、普通任务或伪造包含 bin/llvm-bolt 的字符串；计划非空且包含最终链接。返回对象/静态库/可执行文件真实计数。spec 固定 `LC_ALL=C NINJA_STATUS='[%%f/%%t] ' ninja -n llvm-bolt`。

夹具 109/109 PASS（原103+新增6个测试方法，全集110项逐条subTest）；包含全部负例。根因由旧 helper 对静态库的拒绝及新全集夹具确认。

准备记录：执行编辑脚本时 cwd 指向 tools/bolt，误用了相对的 E 路径；改成已定位的绝对路径一次。该次未编辑 helper，随后新回归夹具对旧 helper 报错；修正入口后109项通过。属本轮一次命令工作目录准备修正，不隐藏失败记录。

后续步骤尚待，源提交与文本补丁暂不生成最终版。

## 第二步：部分实现，停止认证

已编辑但未认证：call 使用 Popen/start_new_session、异常/超时 killpg(SIGKILL)+wait 并附日志；tiny 每次删除旧输出、要求非空普通非链接文件、双方禁默认配置；inventory 验证根并对 walk 错误失败；ELF 类型/版本/头大小/节范围/字符串表/LOAD范围及filesz入口检查；clang-cl/cpp 异常别名；版本行精确校验；post 禁工具/静态库/所有CMake文件内BOLT；spec把debug路径检查移到BOLT动作前；生产prune函数/CLI删除，其三个历史夹具单独保存不随Source发布。候选生成参数未改。

rsp检查：保存的 link.original SHA256 `352a6f57fdc617c20f3e616a0f49ad113d1d5f057e44dcad0afa88c63a9a68cf`，4890字符；shlex分词后没有任何以 `@` 开头的参数。完整命令在 review-rsp-evidence.json，按裁决不增加rsp代码。

新增35个测试方法（tool-plan6、健壮性29），连同原103共138。第一次全套执行有夹具字段/异常契约及进程观察错误；各项一次修正后，最终 **137/138 PASS、1 FAIL**。其中ELF文件范围、入口、字符串、目录访问错误、tiny无输出/空/链接、别名、版本、反向检查的夹具通过；不能称全部夹具PASS。

失败项 `ProcessGroupTests.test_timeout_kills_descendants_and_heartbeat`：第一次 exists/read 的 `/proc` 竞态已修正；第二次在 helper 返回后，读取后代1199507状态为 `R`，不是消失或Z。未完成后代全部退出与心跳停止的证明，立即停止，不再修正/重跑。killpg已发送不等于已证明整个进程组退出；仅等待直接子进程不足以提供此证据。以后应先明确后代退出/回收的等待契约，再修复并重测，不在本轮追加尝试。后续只读审计该PID已不存在，两个失败scope均已回收。

历史prune三项只移位未删除证据；生产Source只有helper/spec/profile，不包含历史测试。新helper/spec仅为未完成工作副本，**没有生成新源提交**。未完成差异及SHA单独置 review-repairs-incomplete.patch/manifest，旧a141文本补丁/manifest未冒充本轮资格。

## 停止后状态

安全属性对比（ELF类型、INTERP、RELRO、STACK、PROPERTY/notes、动态flags/needed、dynsym、版本集合）全部 **NOT RUN**，不声称保持；因此安全属性门禁尚未实现。宏链逐字证据、debug/release开关OFF与cb基线比对全部NOT RUN。ARM/AArch64 30条各5次、20独立源与留出组性能全部NOT RUN，几何平均比未知。真实候选上的新tiny/security/post/compare-root及构造dry-run联合认证NOT RUN。旧20的x86性能不代替本轮目标性能。

候选仍 `4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9`；普通clang与禁用原树cache/ninja SHA未变。22RPM全SHA/大小、归档证据元数据、原源码元数据比对PASS，原ThinLTO仍47987文件/96881772832B；本轮无CMake/Ninja/链接/候选重写/原cache写入/共享锁/proc挂载/ARM根/LLVM构建。全部实验4GiB/swap0/nice19/ionice3 scope已回收；初次109项短单测直接执行，未纳入cgroup，该资源执行偏差如实登记。无>10GiB写入。

新源提交：**未生成**；源HEAD仍a1410e3d，修复在工作副本保留。本轮Gerrit任何分支均未查询或推送。GitHub阶段提交3e7141f已发布tool-plan；停止记录与未认证修复另提交bolt-v4。

准备修正与查找更正逐条见review-corrections.json；两份完整失败日志均公开。初次编辑脚本cwd错误后测试了旧helper，作为旧行为回归复现而非新实现认证；后续109项才是正确实现PASS。停止时没有继续产品步骤。

## 续跑十：PM裁决及进程组约定

上轮不是单纯测试竞态：killpg后只等待直接子进程，不能证明lld等后代已停止写缓存。call异常/超时先killpg(SIGKILL)，回收直接子进程，随后扫描/proc/*/stat，取最后一个右括号之后的state与pgrp；相同pgrp且非Z/X视为存活，每20ms复查，10秒仍存活则GateError列PID/状态。原超时/异常和日志路径保留。/proc消失视为已退出，无法读取/格式错误则失败关闭。

真实shell→子→孙，孙每30ms写心跳；按同样10秒约定观察所有后代退出/僵尸后，再等待150ms（超过两个周期）确认心跳不增。持续存活mock负例报告424242:R、原错误和日志。全套140/140 PASS，新增2方法（累计比原103新增37），reviewfinish-process-tests给原文/资源；4GiB/swap0/nice19/ionice3 scope回收。本轮尚无准备修正。

rsp不加代码、tool-plan闭包及白名单不重做；全套单测包含原有tool-plan回归。候选生成步骤/参数不改；源父a141，本轮不推sandbox或任何Gerrit分支。后续按安全属性→宏链→真实门禁顺序，任一产品失败即停。
