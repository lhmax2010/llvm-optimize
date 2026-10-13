# 49 归档修复第四轮修订与 x86 完整构建

日期：2026-10-13。开场基准 `89ad784b10fb033aff4820dd9bb94d9e2fbe1f3d`。
**本轮状态：IN_PROGRESS，续二完整性PASS；按PM补全的六项调试无关性规则继续。§0–§13全部保留为历史，当前续接见§14起。**

历史状态（8f184dec）：**STOP_RELEASE_STRUCTURE_MISMATCH：第零步与第一步 PASS；第二步的三架构静态分类全部 PASS，但 x86 发布模式实物对照在第2个 TU 出现真实结构差异，按用户规则停止。ARM 实物夹具、全量回归、补丁再生成与完整构建均未执行。第九步停止材料及升级手册已完成；没有重试或失败后改 Source。**

宿主沿用 GBS 初始化后的 mmap_min_addr；用户恢复命令：`sudo sysctl -w vm.mmap_min_addr=65536`，重启也会恢复。本轮仅临时挂载 /proc 并在退出时卸载，不推 Gerrit、不清理磁盘。

## 0. 范围与完整性

W=`/home/linhao/Toolchain/development/llvm-optimize`，E=`W/temp/review-round4-continue-20261013`。本报告 E 中的原始证据仅存本机。

| 核对 | 实测结果 | 证据 |
|---|---|---|
| 基准与远端 | HEAD、origin/main、远端 main 同为 89ad784；reflog 截止 2026-10-12 23:55:07+08 | E/integrity/main-head.stdout、remote-head.stdout、main-reflog.stdout |
| 工作树 | 主库全量 status 5,305,853 行，非忽略项仅既有 gbs_llvm.conf；W/llvm 仅既有三处并发改动 | E/integrity/*-status-all.stdout、llvm-diff.stdout |
| 新增元数据 | 82 条均归因，未知 0；15 个权限盲区免密只读补扫新增 0 | E/metadata-attribution.json、privileged-newer-command.json |
| 输入与工具 | 647 档（225/210/212）与工具、Source、补丁等合计 669 SHA 检查 PASS；HEAD blob 核对全部相符 | E/input-integrity-result.json、input-integrity.jsonl、integrity/head-blob-check.json |
| 编译器别名 | Rnew/build/bin/clang 为指向 clang-22 的软链接 | E/compiler-alias.json |

BOLT 兄弟工作树与分支按用户授权独立保留，本轮未修改。没有回滚或修复任何历史文件。

## 1. 资源与执行协议

轻量准入 6 GiB；全量转换、回归、根内试跑、完整构建准入 10 GiB；不足每 5 分钟复查，最多 60 分钟。scope MemoryMax=18 GiB、MemorySwapMax=0、nice15/ionice3、30秒采样，宿主 MemAvailable <2 GiB 中止。重阶段获取 `/home/linhao/Toolchain/development/heavy-stage.lock` 的 flock 独占，等待最多两小时，阶段结束即释放；两个项目锁贯穿任务。原始记录：E/*-scope/{admission.json,memory-summary.json}。

初次状态/元数据扫描 wall 102.802 秒、scope peak 5,572,915,200 B；归档核对结果见 E/integrity-result.json。采样与读取线程均回收。

## 2. 后续阶段登记

第一步已完成；第二步部分完成后停止。第三至第六步均未执行；升级手册作为停止材料交付，未完成实验不得作为其认证依据。

## 3. Source 修订与测试

按用户裁决新增无调试分支：原命令完全没有调试选项时，不补 `-g/-gdwarf-4`，IR 有 `!llvm.dbg.cu` 即拒绝；有调试选项仍要求末项 DWARF4，未分类/部分选项拒绝。旧带调试后端列表保持原文，是否全库字节不变仍待下一阶段回归。（证据：tools/test_archive_review_round4_continue.py 的固定字面量测试；[生产 diff](49_x86_source.diff)、[ARM diff](49_arm_source.diff)。）

ARM 原生入口改 `--native-limit-shell /emul/usr/bin/sh`，解析实际 ELF、名称、SHA；不带 H/S 设置 AS/core 软硬值，再分别读回；错误 exit125。用 `/usr/bin/env -u BASH_ENV -u ENV` 在启动 shell 前清除环境脚本入口，`exec "$@"` 保留参数边界。只包装三工具与 limits 探针。LLVM 主版本仍为22；取消 ARM 22.1.8 精确钉死，三工具完整版本仍须一致，函数特征串仍逐字核验，差异要求按升级手册重做 docs/44 §2 普查。两份 Commands 类与开场原文逐字一致。Source 记录工具 resolved_path；Rnew 的 clang 别名核查通过，spec 别名修改待第三步生成候选时执行。

| 测试环境 | 结果 | 证据 |
|---|---|---|
| 宿主 | 147/147 PASS；原134项随接口裁决调整，新增13项；bash/dash/sh 三种实际执行 | E/host-tests-result.json |
| ARM32 根 | 143 PASS + 3 环境不适用 + 1 既有 QEMU AS 发现；无新增失败 | E/root-suite-classified.json、root-suite-raw.json |
| 根内解释器 | Python 3.14.2；临时 /proc 已卸载 | E/root-stage-result.json、armv7l-mount-{before,during,after}.txt |

3项环境不适用仍是缺 GNU time 的两个实验辅助测试与 x86 as --64 夹具；AS已知发现仍是 `test_limits_accounting_and_no_external_time`。没有放宽 Source 门禁。
根内小试辅助检查保留 PPid 树采样，修正 limits 行尾空白匹配；入口改 sh、新证据目录，尚未运行其实际小试。本次是事前授权修改，未使用失败后的辅助重试额度。完整 diff：[根内辅助驱动](49_root_helper.diff)。

- `tools/llvm_static_archives_source.py` SHA256 `c43523c0ce04fc3310e670ff97823db8260c21250dc3172575a18db56500082e`。
- `tools/llvm_static_archives_arm_trial.py` SHA256 `1bac8db608554b35d16482711bf0667f1fbee8d60c6fc52f0f448d240ffaa9e4`。

## 4. 发布模式认证与停止点

### 4.1 全量原命令静态分类

精确取 `cb67996861d070d68fec2b4c623eed7d20ba2e23:packaging/llvm.spec` 第180行的 sed 表达式，对已有记录命令的 shell-quoted 文本处理，再 shlex 拆成 token；不凭印象删除选项。输入证据路径逐条保留。（证据：E/release-sed.json、各架构-release-before.txt / -after.txt / -classified.json。）

| 架构 | 命令数 | PASS | FAIL | 模式 |
|---|---:|---:|---:|---|
| x86_64 | 3,853 | 3,853 | 0 | dwarf=None，无调试选项 |
| armv7l | 3,683 | 3,683 | 0 | dwarf=None，无调试选项 |
| aarch64 | 3,699 | 3,699 | 0 | dwarf=None，无调试选项 |

合计11,235条；分类脚本 wall 9.669秒。**这只证明策略覆盖记录命令，不证明对应实物与直接编译等价。**（E/release-static-result.json。）

### 4.2 x86 实物夹具的方法与输入

Rnew=`W/temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0`，B=`Rnew/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build`，G=`Rnew/home/abuild/review49-release-x86_64`。

在 Rnew 的原构建目录执行各记录命令的发布模式版本，保留原编译器、include、目标、优化及 ThinLTO；仅将 `-o/-MT/-MF` 指向 G 下独立产物，`CLANG_NO_DEFAULT_CONFIG=1` 防止再次注入已经记录的默认配置。第二路去掉 `-flto=thin`，其余相同；每个源各一次，总40次 clang -c 全部 exit0。构建树原对象未覆盖。（完整 argv、wait4 wall/RSS：G/generation.json 与各 `NN-{bitcode,native}.json`；环境身份：G/identity.json；驱动：E/release_physical.py。）

选择按已保存命令对应的实际源路径分组、组内源码字节数/路径排序、组名排序取20项，没有按结果调整或换样本。以下覆盖 clangd、apply-replacements、change-namespace、clang-doc、include-fixer；包含原构建生成的 CompletionModel.cpp。不是20个不同子系统，也不是发布模式全库认证。（E/release-physical-x86_64/selection.json；完整绝对路径与源码 SHA 在该文件。）

| 序号 | 源文件（相对 llvm-22.1.8） | 两路编译 |
|---|---|---|
| 0 | `build/tools/clang/tools/extra/clangd/CompletionModel.cpp` | exit0 / exit0 |
| 1 | `clang-tools-extra/clang-apply-replacements/lib/Tooling/ApplyReplacements.cpp` | exit0 / exit0 |
| 2 | `clang-tools-extra/clang-change-namespace/ChangeNamespace.cpp` | exit0 / exit0 |
| 3 | `clang-tools-extra/clang-doc/BitcodeReader.cpp` | exit0 / exit0 |
| 4 | `clang-tools-extra/clang-doc/BitcodeWriter.cpp` | exit0 / exit0 |
| 5 | `clang-tools-extra/clang-doc/ClangDoc.cpp` | exit0 / exit0 |
| 6 | `clang-tools-extra/clang-doc/Generators.cpp` | exit0 / exit0 |
| 7 | `clang-tools-extra/clang-doc/HTMLGenerator.cpp` | exit0 / exit0 |
| 8 | `clang-tools-extra/clang-doc/JSONGenerator.cpp` | exit0 / exit0 |
| 9 | `clang-tools-extra/clang-doc/MDGenerator.cpp` | exit0 / exit0 |
| 10 | `clang-tools-extra/clang-doc/Mapper.cpp` | exit0 / exit0 |
| 11 | `clang-tools-extra/clang-doc/Representation.cpp` | exit0 / exit0 |
| 12 | `clang-tools-extra/clang-doc/Serialize.cpp` | exit0 / exit0 |
| 13 | `clang-tools-extra/clang-doc/YAMLGenerator.cpp` | exit0 / exit0 |
| 14 | `clang-tools-extra/clang-doc/support/File.cpp` | exit0 / exit0 |
| 15 | `clang-tools-extra/clang-include-fixer/FuzzySymbolIndex.cpp` | exit0 / exit0 |
| 16 | `clang-tools-extra/clang-include-fixer/InMemorySymbolIndex.cpp` | exit0 / exit0 |
| 17 | `clang-tools-extra/clang-include-fixer/IncludeFixer.cpp` | exit0 / exit0 |
| 18 | `clang-tools-extra/clang-include-fixer/IncludeFixerContext.cpp` | exit0 / exit0 |
| 19 | `clang-tools-extra/clang-include-fixer/SymbolIndexManager.cpp` | exit0 / exit0 |

40条编译 wall 相加 152.488 秒；单条最高 RSS 686,996 KiB。这个相加口径不等于整个阶段wall。（E/release-generation-summary.json。）

随后 GNU `ar qcDS` 按序组成一个20成员夹具归档，使用新生产 Source、B/bin/{clang-22,llvm-dis,llvm-nm}、jobs4、每命令4GiB AS进行转换。完整命令见 E/release-physical-x86_64/commands.json、conversion/members 下的命令JSON；Source版本与§3一致。

转换本身完成：20 bitcode → 20 ELF，原成员名/次序核对、完整索引2,849项、无bitcode/other、无调试节；强符号缺失0，允许缺失W类合计41。归档5,587,040 → 6,483,328 B，转换主体28.993秒。before SHA `588b9d76f3eb3b3f898cd4aaecca3a632f5064a22ede3ea2430a20cbaecba8a1`，after SHA `d30d1626ca8c922ddc705cf5ae03c2b27d3940b03584aa9d0da3bac99c8e35f4`。（E/release-physical-x86_64/conversion/summary.json、members/release-fixture.a/after.json。）

### 4.3 实物结构门禁未通过

按顺序对比直接非 LTO 对象与转换对象。第0项 CompletionModel.cpp：616节、302个 `.text.*`，节名/数量、定义符号（含绑定/可见性）、重定位类型多重集合全部一致。
第1项 ApplyReplacements.cpp 出现下表差异后停止，剩余18项结构比较未执行，不记PASS；20成员的转换与索引检查在比较前已经完成。（E/release-physical-x86_64/comparisons.json。）

| 项目 | 直接编译 | bitcode转换 |
|---|---:|---:|
| 节区数 / `.text.*` 数 | 353 / 105 | 353 / 105 |
| 节区名多重集合 | 相同 | 相同 |
| R_X86_64_PLT32 | 681 | 678 |
| R_X86_64_PC32 | 279 | 279 |
| R_X86_64_REX_GOTPCRELX | 28 | 28 |
| R_X86_64_64 | 26 | 26 |
| `.L.str.29` | OBJECT / LOCAL / DEFAULT / 节312，size5 | 不存在 |
| 文件字节 | 136,560 | 136,632 |
| SHA256 | `f262864ad21308d2337d6049854193cdea145b9b4632a76fc858beb6d5e650dd` | `b1cc64bdd460ae3b40e25b9eb59fd1926f90f2a02396e727cf03ea61126e6f9e` |

停止后仅用独立 `/usr/bin/readelf -rW/-sW/-SW` 只读核对，同样得到681/678与上述符号差异。原文：E/release-physical-x86_64/{direct,converted}-independent-{relocations,symbols,sections}.txt；汇总 stop-diagnosis.json。直接对象在 G/01-native.o；转换对象副本在 E/release-physical-x86_64/01-comparison/converted.o。

这是真实对象的结构差异，不是行尾空白或解析错误；未启用辅助脚本修正/重跑条款。局部符号不属于 Source 的外部强符号检查，因此“Source转换成功”与“结构对照未通过”不矛盾。**没有据此认定生成代码语义错误，也没有依据自动豁免差异。** 需评审直接非LTO与已优化bitcode再次进入后端的差异及认证判据；本轮没有变更判据、修改参数、换输入或重试。尚不能宣称发布模式已完成认证。（E/stop.json。）

## 5. 各项裁决的实际落实范围

| 项目 | 本轮状态 |
|---|---|
| 无调试Source分支、IR无dbg.cu、旧调试列表 | 已实现；单元与11,235条静态分类PASS；实物门禁未通过，不作发布认证 |
| POSIX sh与实际ELF身份、软硬限制、exit125 | 已实现；宿主三种实现单测PASS；根内套件PASS（保留4项既有环境分类）；真实归档根内小试/64MiB负例NOT RUN |
| ARM只钉major22、保留函数属性逐字门禁 | 已实现；22.1.9是假工具固定字面量单测，不是该版本全库实测 |
| clang无版本别名 | B/bin/clang→clang-22已查证；Source记录resolved_path；spec/补丁更新NOT RUN |
| 356639宏体注释与提交说明 | NOT RUN；旧PS2候选保留，未借此次停止宣称已修改 |
| 根内辅助PPid/行尾空白修正 | 已准备 E/run_root_small.py；未运行小试，diff已交付 |
| bash依赖扫描 | 第六步NOT RUN；宿主bash/dash/sh单测不替代tools全目录扫描，驱动依赖挂账 |
| LLVM23官方工具下载与约600成员探测 | 第六步NOT RUN，没有下载或兼容性结论 |
| 升级手册 | [docs/48](48_llvm_gcc_upgrade_recertification.md)已交付；描述失败点与重认证顺序，不认证新版本 |

## 6. 补丁身份、全量回归与完整构建验收

**第三步未执行**：本轮两次x86 225档/3,864成员/3,853 flags全量回归均NOT RUN。docs/47的历史结果不能代替新SHA回归。两ARM全量转换、after SHA比较、消费者/两种strip证据沿用判断也均NOT RUN。

两份tools Source是§3的新候选；patches目录仍为docs/46旧候选，未再生成、未顺序apply/tree检查：

| 现存文件 | SHA256 | 状态 |
|---|---|---|
| patches/archive-index-fix/ps3/0001-packaging-fix-llvm-static-devel-with-ThinLTO.patch | `1293f6982c87cfbeefe91aa08e92a7d1b72a129f716417f8c8cee61693c463c6` | 未改，不含本轮Source |
| patches/llvm-strip/ps2/0001-packaging-use-llvm-strip-for-x86_64-archives.patch | `aab2cfd1ad3fb58bfe44cdbdda50bbe67d5343b29a6a6d598408d3bb96620e88` | 未改 |

本轮只交Source完整外置diff，不伪造新的format-patch或最终提交说明。旧候选全文仍在上述路径；新补丁全文应在第三步实际完成后产生。（E/final-identities.json。）

**第四步未启动，不存在可交接给BOLT的新构建树。** 原Rnew仍是历史树，本轮只在独立G目录放夹具，不把它冒充新配方完整构建。

| docs/47 §9.1验收项 | 本轮完整构建结果 |
|---|---|
| 1 身份/依赖与新候选应用 | NOT RUN |
| 2 实际转换、完整spec后处理与execve顺序 | NOT RUN |
| 3 225开发档、45 compiler-rt、libarcher双归属 | NOT RUN（20成员局部夹具不能替代） |
| 4 同配方无补丁基线的非归档比较 | NOT RUN |
| 5 七宿主/Tizen bfd、lld/运行库探针 | NOT RUN |
| 6 独立安装再转换、同树SKIP | NOT RUN |
| 7 ≥10成员直接编译/转换结构对照 | 完整构建后验收NOT RUN；此前发布夹具已在第2项未通过 |

没有做完整构建磁盘准入判定，没有清理文件或修改配置来寻求放行；没有完整LLVM构建、RPM打包、BOLT或Chromium构建，没有推Gerrit。

## 7. 资源实测与回收

所有列出阶段均使用18GiB/swap0、nice15/ionice3、30秒采样、宿主2GiB保护线；准入均首次满足，无内存等待。表中scope峰值含页缓存，不能当作单编译进程RSS。原始字节值见 E/resource-table.json。

| 阶段 | 准入GiB | 入场可用GiB | scope峰GiB | 宿主最低可用GiB | wall秒 | exit |
|---|---:|---:|---:|---:|---:|---:|
| integrity-scope | 6 | 13.474895 | 5.190182 | 13.132946 | 102.802 | 0 |
| integrity-input-scope | 6 | 13.417889 | 0.906307 | 13.063351 | 129.112 | 0 |
| host-tests-scope | 6 | 12.962776 | 0.364021 | 12.962776 | 112.309 | 0 |
| root-tests-scope | 10 | 13.393391 | 0.305439 | 13.129627 | 95.004 | 0 |
| release-static-scope | 6 | 13.392193 | 0.908703 | 13.392193 | 10.220 | 0 |
| release-x86-physical-scope | 10 | 13.088089 | 1.308559 | 12.558510 | 195.492 | 1 |

六个scope的 memory.events 中 max/oom/oom_kill均0。最后阶段exit1来自结构门禁，不是内存不足。根内测试与实物夹具各持共享flock，获取无等待并分别在结束时释放；release-x86-physical-scope/heavy-lock-released.json为13:32:35+08。两个项目锁13:35:22+08释放。最终核查无本轮进程、采样器、日志线程或临时挂载残留。（E/*-scope/{outcome.json,memory-summary.json,heavy-lock-*.json}、cleanup-final.json、final-mountinfo.txt。）

15个权限盲区的补扫只读；所有构建树、输入、GBS缓存与BOLT会话文件保留，未修改W/llvm/spec、gbs配置或已上传补丁。Source在停止后未再改动，Commands原文比较为True；没有用辅助缺陷条款重跑任何本轮步骤。

## 8. 原始证据索引与挂账

| 内容 | 本机路径（均在E，另注明者除外） |
|---|---|
| 本轮完整用户裁决 | task-request.txt |
| 完整性与输入 | integrity/、metadata-gate.json、input-integrity.jsonl、integrity-result.json |
| 宿主与ARM32测试 | host-tests-result.json、root-suite-raw.json、root-suite-classified.json、root-commands.json |
| 发布模式静态分类 | release-sed.json、各架构-release-{before.txt,after.txt,classified.json} |
| 20源输入清单、完整root生成命令 | release-physical-x86_64/selection.json；G/generation.json及逐命令JSON |
| 转换的版本、flags、索引、符号证据 | release-physical-x86_64/conversion/summary.json与members/ |
| 差异原文与停止判定 | release-physical-x86_64/comparisons.json、stop-diagnosis.json、stop.json |
| 资源驱动、所有阶段完整命令与原始输出 | run_stage.py、各 *-plan.json、*-scope/build.log、commands.log、time-v.txt |
| 收尾身份与清理核查（未清理磁盘） | final-identities.json、cleanup-final.json |

当前优先挂账是发布模式实物差异的解释与判据裁决；后续顺序仍为两ARM实物夹具、两次x86全量回归、补丁再生成、x86完整构建和全部验收，再做ARM全量与根内小试/64MiB负例。另保留发布模式完整构建、ARM第二段打包、LLVM23前向探测、tools驱动bash清单、总部dash替换时的LLVM源码bash检查。没有把任何未执行项写成PASS或把旧输入结果当作新Source认证。


## 9. 调试无关性门禁续接：完整性与事前判据

本轮基准 `8f184decf532be6c83937427410ddc364a720c6e`；reflog时间2026-10-13 13:39:20+08。新证据目录 D=`W/temp/release-debug-independence-20261013`，旧E及G只读保留。用户裁决：上轮直接非LTO与转换路线优化次数不同，§4.3差异属于该旧判据问题；历史停止记录不改判为实测PASS。

完整性结果：290条新元数据全部归因、未知0；其中195条属于BOLT会话，另2条旧根run/mount目录时间由该会话14:04的私有挂载调用记录核实。主库5306835行全量status只有既有gbs配置修改，LLVM树只有既有spec并发改动；80份HEAD blob一致。647输入归档与工具、Source、补丁等669次SHA核对全部PASS。没有恢复、回滚或修改BOLT文件。（D/integrity-result.json、metadata-attribution.json、bolt-session-attribution.json、input-integrity.jsonl。）

本轮事前冻结判据（用户指令）：每架构20源，debug原命令和精确sed后的发布命令均保留ThinLTO，各自产出bitcode后交同一新Source转换。逐项要求SHF_ALLOC节名称/标志/大小/内容相同、作用于这些节的重定位偏移/类型/符号名/addend相同，以及排除FILE和调试节的SECTION符号后，符号名称/类型/绑定/可见性/所在节名/值/大小相同；发布对象不得含.debug。任何差异停止。

直接非LTO结构比较只记录，不作门禁；统一标注“预期差异：转换对已做链接前优化的 bitcode 再次完整优化”。原第四步第3项的跨子系统直接编译比较亦同。x86严格沿用§4.2的20源选择，debug路新编；两ARM按相同选样规则。资源、锁、退出回收以及后续步骤顺序沿用§1和用户原任务，未授权新判据以外的放行。

## 10. 新判据实物执行方法与辅助检查

Source无改动，生产c43523c0、ARM候选1bac8db6，完整SHA见§13。x86使用§4.2同一20源，逐个重核源SHA；旧G中20份发布bitcode按旧转换before.json成员SHA核对后复制到新目录，未重新生成发布输入。旧G中的直接非LTO对象只读复制用于诊断，路径/本次SHA登记于D/physical-x86_64/reused-inputs.json。debug路使用保存的original_argv，保留所有调试和ThinLTO选项，新编20次；只把-o/-MT/-MF指向独立目录，并设置CLANG_NO_DEFAULT_CONFIG=1，避免重复注入已经记录的默认参数。

新根内产物G2=`Rnew/home/abuild/review49-independence-x86_64`。完整命令、版本与逐次wait4数据：G2/generation.json、identity.json；驱动D/release_physical.py；/proc挂载前/中/后记录在D/physical-x86_64/mount-*.txt。实验结束已卸载，没有改B中的原对象、spec、配置或BOLT目录。

debug和发布各按序以00.o–19.o作为成员名重新组成fixture.a，再用当前生产Source、B/bin三工具各转换一次，jobs4、单命令4GiB AS。两路各20个bitcode全部转成ELF；成员身份/次序及完整索引各2849项通过；强符号缺失0，两路允许缺失W均41。debug输出20成员有调试节，发布输出0成员有调试节。归档封装成员名与旧实验不同，整档SHA不可与旧release-fixture.a直接当不变性判据。（D/physical-summary.json、physical-x86_64/{debug,release}-conversion/summary.json、archive-inspections.json。）

| 路线 | bitcode归档字节 | 转换后归档字节 | 转换wall（秒） | after SHA256 |
|---|---:|---:|---:|---|
| debug | 43446384 | 56223576 | 36.806 | `e92f28b63515e1c43559784af3f7bd20600ab6ad2c84b1a0d91b46e2cbbc0ca3` |
| release | 5587040 | 6483328 | 27.737 | `7efe646e21d97a0b5b0e54db26acbf2ecc94076015ba7fa4aa15b1f8ae1ec4b5` |

新编debug路20命令均exit0，wall相加76.536s，单命令最高RSS 794,440KiB。该相加值不等于阶段wall，也不作性能结论。（G2/generation.json。）

### 10.1 比较器边界与一次辅助夹具修正

新增[只读ELF比较器](../tools/check_release_debug_independence.py)与[测试](../tools/test_release_debug_independence.py)。比较使用实际payload字节；JSON仅以SHA表示内容。NOBITS比较语义类型和大小，无文件payload。用节名及同名出现序号识别节；保留符号/重定位顺序，不把不同节号或字符串表偏移误当差异。只排除FILE和调试节的SECTION符号；绝不排除指向普通.rodata的SECTION符号。RELA直接比较addend；ARM REL无独立addend字段，记录implicit并由整个目标节字节相等保证编码的addend相同。本轮仅x86实际进入门禁，ARM REL支持仅经辅助正负例，不冒充ARM实物认证。

首次辅助测试12项中10PASS、2FAIL：测试误将GNU as有/无-g产物视为正例，但前者多一个.text SECTION符号，后者没有。这是夹具前提错误，检查器按既定符号判据拒绝正确。独立诊断保存两个ELF与解析差异，alloc/relocation均相同，唯普通.text SECTION符号不同。（D/helper-fixture-diagnosis.json、helper-original-*.o。）

只在夹具汇编末尾加`.long .text`，使双方均真实引用.text并包含该SECTION符号；比较器、Source和门禁未改。修正diff为D/helper-test-fix.diff，完整改动：

```diff
- '.size test_entry,.-test_entry\n.data\n.long 17\n'
+ '.size test_entry,.-test_entry\n.data\n.long 17\n.long .text\n'
```

使用辅助脚本缺陷条款的一次修正重跑，12/12 PASS；覆盖ELF32 REL/ELF64 RELA、调试符号排除、每类alloc/relocation/symbol字段差异、发布对象含debug拒绝、截断ELF拒绝。特别保留“额外非调试SECTION符号拒绝”的负例。错误正例的诊断复制没有运行产品Source，真实20源夹具没有换样或重试。（D/comparison-helper-tests{,-retry}-scope/build.log。）

## 11. 调试无关性门禁与直接编译诊断

### 11.1 逐文件状态

20源的两路转换均已批量完成。逐文件门禁在第3项首次FAIL时立即停止，后17项不再判定；两ARM未启动、没有选择或转换其20源，不能记为PASS。（D/physical-x86_64/result.json、comparisons.json。）

| 序号（从0） | 源文件（相对llvm-22.1.8） | SHF_ALLOC | 重定位 | 符号表 | 发布无debug | 判定 |
|---|---|---|---|---|---|---|
| 0 | `build/tools/clang/tools/extra/clangd/CompletionModel.cpp` | 一致 | 一致 | 一致 | 是 | PASS |
| 1 | `clang-tools-extra/clang-apply-replacements/lib/Tooling/ApplyReplacements.cpp` | 一致 | 一致 | 一致 | 是 | PASS |
| 2 | `clang-tools-extra/clang-change-namespace/ChangeNamespace.cpp` | 一致 | 一致 | 不一致 | 是 | FAIL |
| 3 | `clang-tools-extra/clang-doc/BitcodeReader.cpp` | 未判定 | 未判定 | 未判定 | 是（转换检查） | NOT RUN（已停止） |
| 4 | `clang-tools-extra/clang-doc/BitcodeWriter.cpp` | 未判定 | 未判定 | 未判定 | 是（转换检查） | NOT RUN（已停止） |
| 5 | `clang-tools-extra/clang-doc/ClangDoc.cpp` | 未判定 | 未判定 | 未判定 | 是（转换检查） | NOT RUN（已停止） |
| 6 | `clang-tools-extra/clang-doc/Generators.cpp` | 未判定 | 未判定 | 未判定 | 是（转换检查） | NOT RUN（已停止） |
| 7 | `clang-tools-extra/clang-doc/HTMLGenerator.cpp` | 未判定 | 未判定 | 未判定 | 是（转换检查） | NOT RUN（已停止） |
| 8 | `clang-tools-extra/clang-doc/JSONGenerator.cpp` | 未判定 | 未判定 | 未判定 | 是（转换检查） | NOT RUN（已停止） |
| 9 | `clang-tools-extra/clang-doc/MDGenerator.cpp` | 未判定 | 未判定 | 未判定 | 是（转换检查） | NOT RUN（已停止） |
| 10 | `clang-tools-extra/clang-doc/Mapper.cpp` | 未判定 | 未判定 | 未判定 | 是（转换检查） | NOT RUN（已停止） |
| 11 | `clang-tools-extra/clang-doc/Representation.cpp` | 未判定 | 未判定 | 未判定 | 是（转换检查） | NOT RUN（已停止） |
| 12 | `clang-tools-extra/clang-doc/Serialize.cpp` | 未判定 | 未判定 | 未判定 | 是（转换检查） | NOT RUN（已停止） |
| 13 | `clang-tools-extra/clang-doc/YAMLGenerator.cpp` | 未判定 | 未判定 | 未判定 | 是（转换检查） | NOT RUN（已停止） |
| 14 | `clang-tools-extra/clang-doc/support/File.cpp` | 未判定 | 未判定 | 未判定 | 是（转换检查） | NOT RUN（已停止） |
| 15 | `clang-tools-extra/clang-include-fixer/FuzzySymbolIndex.cpp` | 未判定 | 未判定 | 未判定 | 是（转换检查） | NOT RUN（已停止） |
| 16 | `clang-tools-extra/clang-include-fixer/InMemorySymbolIndex.cpp` | 未判定 | 未判定 | 未判定 | 是（转换检查） | NOT RUN（已停止） |
| 17 | `clang-tools-extra/clang-include-fixer/IncludeFixer.cpp` | 未判定 | 未判定 | 未判定 | 是（转换检查） | NOT RUN（已停止） |
| 18 | `clang-tools-extra/clang-include-fixer/IncludeFixerContext.cpp` | 未判定 | 未判定 | 未判定 | 是（转换检查） | NOT RUN（已停止） |
| 19 | `clang-tools-extra/clang-include-fixer/SymbolIndexManager.cpp` | 未判定 | 未判定 | 未判定 | 是（转换检查） | NOT RUN（已停止） |

| 架构 | 实物门禁总体结果 |
|---|---|
| x86_64 | 2 PASS、1 FAIL、17未判定，整体STOP |
| armv7l | NOT RUN，依赖x86门禁通过 |
| aarch64 | NOT RUN，依赖前置门禁通过 |

### 11.2 第3项差异原文与只读复核

`clang-tools-extra/clang-change-namespace/ChangeNamespace.cpp`：614个SHF_ALLOC节，共153529字节，名称/flags/size/payload完全相同；3102条相关重定位逐条相同；release无debug。按允许的过滤规则后，debug符号1182条，release1181条，唯一多项为：name空串、type=3/SECTION、binding=0/LOCAL、visibility=0/DEFAULT、section=.rodata.str1.1、value=0、size=0。没有release独有符号。（D/failure-readonly-proof.json。）

独立GNU readelf 2.42原始行（D/physical-x86_64/02-comparison）：

```text
# debug-symbols.txt:438；release-symbols.txt没有对应行
   434: 0000000000000000     0 SECTION LOCAL  DEFAULT 1109 .rodata.str1.1
# debug-sections.txt:1114 与 release-sections.txt:1114 相同
  [1109] .rodata.str1.1    PROGBITS        0000000000000000 01e8a8 0002da 01 AMS  0   0  1
```

完整统一差异见[49_debug_independence_failure.diff](49_debug_independence_failure.diff)，原始JSON diff如下：

```diff
--- debug/symbols
+++ release/symbols
@@ -5190,18 +5190,6 @@
     "visibility": 0,
     "section": [
       ".text._ZN5clang6format11FormatStyle15RawStringFormatD2Ev",
-      0
-    ],
-    "value": 0,
-    "size": 0
-  },
-  {
-    "name": "",
-    "type": 3,
-    "binding": 0,
-    "visibility": 0,
-    "section": [
-      ".rodata.str1.1",
       0
     ],
     "value": 0,

```

`.rodata.str1.1`有ALLOC标志，不是获准排除的调试节；故按用户新符号判据仍为FAIL。**不把可加载内容相同解释为整项通过，不排除该符号，不修改Source，不再次编译/转换。** 第2项ApplyReplacements在新门禁中PASS；上一轮直接编译的PLT32/局部字符串差异不再承担门禁职责。（D/physical-x86_64/result.json与02-comparison原文。）

### 11.3 直接非LTO对照：只记录

以下20项诊断在门禁检查之前一次性汇总，方法与旧§4相同；不用于PASS/FAIL。节数含非ALLOC元数据节；relocation为类型多重集合，定义符号为名称/类型/绑定/可见性多重集合。“直有/转有”表示多重集合相减条数，并非代码行数或不同类型数。所有差异标注：**预期差异：转换对已做链接前优化的 bitcode 再次完整优化**；不是这些条目的逐项根因新实测。（D/physical-x86_64/direct-diagnostic.json及NN-comparison的readelf输出。）

| 序号（文件对应§11.1） | 直接/转换节数 | 节名直有/转有 | 重定位直有/转有 | 定义符号直有/转有 |
|---|---:|---:|---:|---:|
| 0 | 616/616 | 0/0 | 0/0 | 0/0 |
| 1 | 353/353 | 0/0 | 3/0 | 1/0 |
| 2 | 1702/1702 | 0/0 | 2/0 | 0/0 |
| 3 | 2200/2024 | 176/0 | 270/0 | 71/0 |
| 4 | 255/255 | 0/0 | 0/0 | 0/0 |
| 5 | 80/80 | 0/0 | 0/0 | 0/0 |
| 6 | 251/251 | 0/0 | 0/0 | 0/0 |
| 7 | 116/113 | 3/0 | 6/0 | 3/0 |
| 8 | 252/249 | 3/0 | 5/0 | 4/1 |
| 9 | 168/165 | 5/2 | 4/0 | 3/1 |
| 10 | 1668/1668 | 0/0 | 0/0 | 0/0 |
| 11 | 708/708 | 2/2 | 0/2 | 0/0 |
| 12 | 504/504 | 0/0 | 0/0 | 0/0 |
| 13 | 533/527 | 6/0 | 17/0 | 3/0 |
| 14 | 16/16 | 0/0 | 0/0 | 0/0 |
| 15 | 71/71 | 0/0 | 0/0 | 0/0 |
| 16 | 61/61 | 0/0 | 0/0 | 0/0 |
| 17 | 237/237 | 0/0 | 1/0 | 0/0 |
| 18 | 34/34 | 0/0 | 0/1 | 0/0 |
| 19 | 62/62 | 0/0 | 0/0 | 0/0 |

10项在这组直接编译诊断指标上相同，10项有差异；无一因此拒绝新门禁。对比第1项PLT32仍记录直接681、转换678；新debug/发布转换门禁中它已通过。

## 12. 资源、回收与未执行步骤

全部scope沿用18GiB cap、swap0、nice15/ionice3及宿主2GiB保护。阶段实际数据如下；单位GiB=2^30B，辅助测试wall含scope管理，非测试内核执行时间。（D/resources.json与各scope原始样本。）

| 阶段 | 准入线GiB | 实际入场GiB | wall秒 | scope peak GiB | 宿主最低可用GiB | exit |
|---|---:|---:|---:|---:|---:|---:|
| comparison-helper-tests-retry-scope | 6 | 12.987717 | 2.166 | 0.017517 | 12.987717 | 0 |
| comparison-helper-tests-scope | 6 | 13.457012 | 2.117 | 0.018833 | 13.457066 | 1 |
| integrity-input-scope | 6 | 13.518318 | 126.962 | 0.900295 | 13.052597 | 0 |
| integrity-scope | 6 | 13.143818 | 249.811 | 2.341866 | 12.251553 | 0 |
| physical-x86_64-scope | 10 | 13.072792 | 151.169 | 1.166035 | 12.990803 | 1 |

所有memory.events的max/oom/oom_kill均0；x86实物stage失败来自门禁返回1。共享锁14:35:27取得、14:37:58释放，无等待；两个项目锁14:40:19释放。14:40:35只读终检：任务进程0、挂载0、项目锁0，所有采样/日志线程已回收。（D/physical-x86_64-scope/heavy-lock-*.json、cleanup-final.json。）

| 原任务后续步骤 | 本轮结果 |
|---|---|
| 第三步，两次x86 225档全量回归 | NOT RUN，不能引用旧回归作为本轮通过 |
| PS3/PS2候选再生成、apply/tree | NOT RUN，patches仍docs/46旧候选 |
| 第四步，磁盘1.2倍门禁/新x86完整构建 | NOT RUN；没有进入构建准入、没有清理 |
| 完整构建验收1身份/依赖、2安装后处理次序、3归档/运行库、4非归档、5消费者、6幂等 | 全部NOT RUN |
| 验收7直接编译比较 | 本轮20夹具的诊断已保存；完整构建产物的该项NOT RUN，判据已事前改为只记录 |
| BOLT新树交接及最终提交说明 | 无新树/无交接，不得复用本轮为已认证构建结论 |
| 第五步两ARM全量/根内小试/64MiB负例 | 全部NOT RUN |
| 第六步bash依赖全集/LLVM23探测 | NOT RUN，按产品门禁失败停止，不启动新的实验 |
| 第七步升级手册、第九步报告 | docs/48修正为调试无关性硬门禁、直接编译只诊断；docs/49保留旧停止并追加本轮结果 |

Source的147项宿主、根内143PASS+3环境不适用+1既有AS发现沿用§3：它们是在相同Source SHA上先前执行的测试，本轮没有重跑。新增辅助比较器测试是12项，不混记为生产Source测试159项。发布模式完整构建、ARM打包与实际原生限制/负例、LLVM源码bash检查及LLVM23读取兼容性仍挂账。

## 13. 冻结身份与交付

| 文件 | SHA256 | 本轮变化 |
|---|---|---|
| tools/llvm_static_archives_source.py | `c43523c0ce04fc3310e670ff97823db8260c21250dc3172575a18db56500082e` | 未改 |
| tools/llvm_static_archives_arm_trial.py | `1bac8db608554b35d16482711bf0667f1fbee8d60c6fc52f0f448d240ffaa9e4` | 未改 |
| patches/archive-index-fix/ps3/0001-packaging-fix-llvm-static-devel-with-ThinLTO.patch | `1293f6982c87cfbeefe91aa08e92a7d1b72a129f716417f8c8cee61693c463c6` | 未再生成 |
| patches/llvm-strip/ps2/0001-packaging-use-llvm-strip-for-x86_64-archives.patch | `aab2cfd1ad3fb58bfe44cdbdda50bbe67d5343b29a6a6d598408d3bb96620e88` | 未再生成 |

证据D/final-source-identity.json；补丁仍§6登记值。Commands、spec、已上传的两份补丁、W/llvm和gbs配置均未改；未运行完整构建、BOLT、性能校准、Chromium或Gerrit推送。比较器与辅助测试是新增可审阅工具，其余驱动/原始输出保存在D。完整性阶段提交`15556e7`已推送，本停止材料与STATUS同提交推送；最终提交号见仓库Git记录，避免文档自引用哈希循环。

## 14. 续二开场：完整性与事前判据

2026-10-13，以`800798e51fd2b6885f09dbb94e23642e50b1272e`为基准，reflog截止14:44:14+08。本轮证据F=`W/temp/release-contract-v2-20261013`。完整性135条新增元数据全部归因、未知0；主库完整status 5,308,096行，仅用户既有gbs配置修改；W/llvm仍仅三处并发设置。647档输入加工具/Source/候选补丁等669项SHA全部PASS。两个上轮交付JSON逐项与800798e的Git blob一致；BOLT的210f82b/4c79280及其工作树/证据归于授权会话，不修改。权限盲区免密只读补扫新增0。（F/metadata-gate.json、prior-delivery-attribution.json、bolt-session-attribution.json、input-integrity-result.json。）

PM事前补全判据：①SHF_ALLOC节按顺序比较名称/类型/标志/大小/对齐/entsize/内容；②按目标节逐条比较重定位，STT_SECTION目标规范为所指节名；③非LOCAL及非空且非`.L`开头的LOCAL符号按名称/类型/绑定/可见性/所在节名或特殊号/值/大小的多重集合比较；④排除SECTION、FILE、空名LOCAL和`.L`LOCAL；⑤COMDAT按签名/组标志/有序成员名多重集合比较，仅从成员中去掉`.debug*`及其`.rel.debug*`/`.rela.debug*`；⑥发布产物无`.debug*`。不另增豁免。REL隐式addend由目标节完整字节一致覆盖，RELA直接比较显式addend。直接非LTO比较只诊断。新比较器须先通过正负夹具，再重判上一轮全部20对x86对象；两ARM夹具和其后各阶段尚未执行。

## 15. 完整六项比较器与夹具

`tools/check_release_debug_independence.py`增加可加载节type/alignment/entsize、STT_SECTION重定位目标节名规范化、按目标节保存重定位顺序、符号多重集合与SHT_GROUP解析。符号索引与字符串表偏移不作身份，重复符号/组不去重；组内成员顺序仍必须一致。比较时使用实际payload bytes，JSON仅以SHA展示原文差异。两份Source与Commands不改。

2026-10-13 15:03宿主25项辅助测试一次全PASS（0.107s；F/comparison-tests-scope/build.log）。七个指定边界均覆盖：额外SECTION PASS、未引用`.L`LOCAL PASS、有名LOCAL差异FAIL、可加载节重定位目标差异FAIL、COMDAT成员差异FAIL、组内仅debug成员差异PASS、发布debug节FAIL。另覆盖ELF32 REL/ELF64 RELA、可加载节内容/顺序/类型/对齐/entsize、符号全部字段与重复计数、非LOCAL的`.L`名字仍比较、COMDAT签名/标志/顺序/重复计数、截断ELF拒绝。未动用本轮辅助缺陷重跑条款。Source测试仍为§3已执行的147项，不与25项比较器测试混计。
