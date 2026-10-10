# LLVM 吞吐优化分支状态

更新日期：2026-10-10。分支：`main`；仓库：`lhmax2010/llvm-optimize`。
**当前任务（docs/44续二）诊断阶段完成**：独立600例（普通300+四CPU负载300）全通过；8次首读R均有SIGKILL待处理，最长5.430ms内消失/Z。定性为预注册场景下的测试时序问题，原Commands保持不变。辅助诊断误将X(dead)当存活，按授权只修辅助判定并完整重跑一次；最终消失/Z门禁未放宽。准备进入测试与ARM保留节索引小修，尚未改Source/tests。证据docs/44 §13及temp/arm-source-cancel-diagnosis-20261010；项目锁继续持有。

**历史文档任务（docs/43）已完成**：已将ARM候选1620a8da的设计、逐token分类、TLS/PIC集合、两ARM实测摘要、限制和67项测试清单整理为不超过50KB的外部评审材料包；生产6bd0546a到候选的完整三行上下文diff单列文档附件。仅整理已有证据，未运行测试/构建/转换、未改Source/spec/补丁，候选仍待外部评审；ARM打包验收尚未执行。

**上轮收尾（docs/40 §12）**：ARM转换第一段全部PASS。Source1620a8da的67测试/夹具与x86 225档/3864成员不变性PASS；ARM32 210档、AArch64 212档全量转换/重定位、三套消费者和两种strip均PASS。AArch64唯一一次-bc成功（2321.728s、scope峰16.417GiB、无OOM）。两BUILD/原件/缓存保留，项目锁/进程/采样器/挂载回收。后续需ARM的spec集成与RPM验收，生产Source/两review补丁未动。

历史状态核对到 `4d80d94`；完整设计以 [docs/21](21_spec_integration_v3.md) 为准，混合构建见 [docs/22](22_hybrid_link_trial.md)，
归档根因与前次失败记录见 [docs/23](23_archive_fix_and_profile_rebind.md)；
旧混合根核查停止记录见 [docs/24](24_archive_fix_verification.md)，该根已隔离，不再读写。
docs/25保留前次停止记录；用户已更正旧构建图门禁，改用docs/13的22 RPM作唯一基线。
docs/26 的 libarcher 范围停止已由用户新方案解除：全部 bitcode 归档（含 libarcher）转机器码，旧改宏方案作废。
docs/27 旧转换产物作废；docs/28–29 的后端选项、链接 AS 诊断与离线门禁保留历史结论。历史完成 [docs/30](30_archive_fix_full_build.md)：移除构建根缺失的 GNU time 依赖，五归档逐成员回归 PASS；一次完整构建成功，22 RPM、225 开发归档、45 compiler-rt、全部宿主消费者和 Tizen bfd/lld 两次测试包验收 PASS。补丁仅限 x86_64，待提交评审；没有推 Gerrit。
上一轮完成 [docs/31](31_archive_fix_submission.md)：从 LLVM 干净 HEAD 生成单提交 format-patch，Source 与 docs/30 同字节，提交 spec 与实测输入仅差 6/6/2 对 4/4/1；补丁与 Source 已置 patches/archive-index-fix/ 供评审，没有推 Gerrit。
上一轮 [docs/32](32_archive_fix_v2.md)：v2 Source/spec 与测试已修订，3853条白名单、类型元数据普查、五档第一遍回归通过；运行期间出现另一会话的 Ninja，10:52中止独占实验。确定性及600s复验未完成，完整构建未启动，认证 INCOMPLETE；未覆盖docs/31的v1补丁。
上一轮 [docs/33](33_llvm_strip_alternative.md) 收尾：225档llvm-strip均失败且不改文件，宿主无插件GNU ld失败、lld22/LLVMgold22的A通过；公开快照直接BR两包实际走共享LLVM。按新8 GiB准入/6 GiB cap串行执行两个Tizen测试包：bfd格式失败；lld A链接及独立运行通过，B在7325.348s因严重内存回收/I/O抖动由代理诊断性中止，无OOM，整包%check未执行。B兼容性仍UNKNOWN，不将中止记成用户预注册门禁或本征链接失败；没有重试/加cap。
**2026-10-09 docs/35历史收尾（9f27fbc）：授权三项清理后109.523GiB，原60GiB门槛PASS；唯一一次标准提交配置-ba --noprep成功（5381.375s，scope峰值16.408GiB，无OOM）。22新RPM：225开发归档验收PASS；45 compiler-rt的1,964成员字节一致，17,689路径非归档差异0；标准brp链通过。独立buildroot真实-bi、同树Source SKIP与七项宿主消费者全部PASS。Tizen bfd在依赖解析阶段FAIL，固定Base repomd只读查询HTTP404；未创建测试chroot，未编译/链接。按规则停止，lld测试包与v2最终补丁未执行，没有重试。证据：temp/archive-fix-v2-final-20261009/continue-20261009；scope/采样器/临时挂载/项目锁均已回收。f49a561磁盘停止历史保留。**
**2026-10-09 docs/36完成：按新授权从docs/30两个测试根各107缓存RPM复原本地Base；107个摘要与原primary完全相符，缺失0，无需最新快照备用方案。bfd/lld各一次串行构建、A/B %check及225归档+4工具身份全部PASS；每根113包NEVRA与docs/30差异0。tizen_base无交互fetch到cb679968，基于其生成v2 format-patch并完成干净base应用及完整tree一致性核对。patch SHA ddef2221…，Source仍6bd0546a…；已替换评审目录中的v1，旧摘要/副本保留。未重建LLVM、未改W原件/配置、未推Gerrit。新目标整套配方未在本轮重建，不能混同原认证输入。**

**2026-10-09 docs/37完成：在docs/35同一x86_64 buildconfig/宏环境下，只读展开cb679968与f111162e。公共C/CXX/ASM flags只多一个原已存在的诊断token，编译器别名和显式OFF逐项核查；225档/3,853条历史命令替换新公共flags后，现有classify_options全部PASS、未分类0、末项策略不变。结论为认证策略覆盖；不是新配方完整构建/%install认证。Source、spec、补丁与认证指纹均未改。证据：docs/37、temp/target-recipe-policy-check-20261009。**

**2026-10-09 docs/38首次停止（834f9aa，历史记录）：22个docs/35 RPM与N的17,689路径全部匹配；当前debuginfo宏链只有静态归档后处理实际使用%__strip。/home可用50.800056GiB，计入全部允许cache回收的乐观上界仍仅50.816586GiB；允许清理的独立安装树在另一个SSD，无法补齐60GiB门槛。未删除文件、未改spec、构建/消费者/新提交补丁均0；锁已释放。证据：temp/llvm-strip-x86_64-20261009。用户确认356627 PS2已上传；本轮没有向Gerrit推送。**

**2026-10-09 docs/38续接完成：按新增授权先rename保全docs/35的22 RPM+SRPM，只清理第一类旧解包载荷后/home可用97.118GiB，未删第2/3类。仅加x86_64三行宏，唯一一次-ba --noprep成功（6318.155s，scope峰值17.504GiB，无OOM）；225开发归档、45 compiler-rt/1964成员的SHF_ALLOC及索引PASS，结构与docs/34逐成员同SHA；17,689路径仅270个.a不同，非静态库差异0。270次llvm-strip全部exit0，七宿主消费者及宿主/Tizen bfd/lld运行库探针全PASS；两个测试根114包仅比docs/36多compiler-rt。已无交互fetch核验356627 PS2=67619ec8bbbac7238a6cfc33a481ccfbcd12206f；独立4行补丁apply/tree PASS，patch SHA49c56182…，新Change-Id Iac085555112855d60cc7591931e91466691db6b2，待用户上传。证据：temp/llvm-strip-x86_64-20261009/continue-20261009；未推Gerrit。**

**2026-10-09 docs/39完成：按cb679968分别用两ARM根原生rpmspec展开，ThinLTO均生效；ARM32 MinSizeRel/候选末项Os，AArch64 Release/候选末项O3，均保留stack protector，不能套x86策略。accel工具与原生clang均22.1.8；显式dispatcher进入/emul、两架构小C跨目标编译/bitcode往返及strip成功，全部编译实验6.507秒。普通GBS chroot因无ARM binfmt注册失败；包装器刷新根内resolver的副作用已在报告§0登记。当前磁盘40.93GiB低于60GiB，ARM完整构建资源与实际归档命令仍UNKNOWN。只交认证设计，未构建/改Source/改补丁/推Gerrit。用户确认356627与356639已上传；ARM如后续通过，更新同两个change的patchset，保持x86行为不变。证据：docs/39、temp/arm-archive-feasibility-20261009。**

**2026-10-10 docs/41完成只读磁盘盘点：覆盖/home/linhao可读范围及567条agent元数据，253个权限盲区明确保留UNKNOWN。主表102项按项目/大小分组；P28/P29旧纯归档树可删建议6.646GiB，docs/38第2/3类已核算二进制载荷173.887GiB，合计180.533GiB（已扣范围外硬链接；尚未执行）。64GiB未启用swap另列需用户判断；Rnew/B、N、N38、H、rpms-docs35、docs35–39证据、Base本地仓库与ARM输入保留。仅是建议，任何清理仍等用户逐项确认；没有删除、移动、构建或推Gerrit。证据：docs/41、temp/disk-inventory-20261009。**

docs/21 取代 docs/20 的后续实施方案；历史报告、校准判定和预注册文件保持原样。
以下 `temp/` 均相对工作区 `/home/linhao/Toolchain/development/llvm-optimize`，仅保存在本机，不在 GitHub。

**历史2026-10-10夜间任务停止：A1完成；A2清单外共享Git依赖触发停止，三个Chromium目录未删；A3只拷日志/生成sudo脚本。B/x86与C两ARM均NOT RUN，未改Source/spec/补丁、未构建。无人值守阶段不问询不重试，按约定发布停止报告。证据docs/42、docs/40、temp/night-arm-stage1-20261010。**

## 1. 计划

总目标：降低 Tizen 全平台 RPM 包构建总耗时，优化对象覆盖实际调用的 LLVM 工具。
当前阶段：取消诊断600例PASS，进入授权测试/ARM小修与重新认证；旧5608候选尚未通过全量复验，生产6bd与评审补丁不改。
上轮任务执行docs/40 §12：GD/LD/TLSDESC按明确清单授权，LE无条件拒绝，IE与其他未认证类型仍停止；-mthumb补回并增加逐成员参考对象模式门禁。67测试及最终SHA全量x86回归已通过；两ARM全库转换、重定位与三套消费者/strip全部通过，第一段结束。不重建ARM32、不install/打包，生产Source与两个review补丁不改。
**x86_64归档转换与llvm-strip已由用户上传Gerrit 356627、356639，代理未推Gerrit。ARM未来通过后更新同两个change的patchset，保持x86行为；当前生产Source/补丁仍仅认证x86，候选ARM Source已通过本轮固定输入第一段功能认证，ARM的spec集成/RPM验收尚未执行。设计v4/BOLT继续暂缓；W/llvm/spec和评审补丁未改。**
docs/30 从 docs/13 的 22 RPM 及 docs/26 登记的基线解包开始复核，环境预检确认 GNU time 缺失，Source 改用 wait4；五代表归档与 docs/28 逐成员及整档 SHA 相同，45 项单元测试 PASS。
一次完整 LLVM 构建 16,011.555 s，18 GiB/swap0/4/4/1/debuginfo4，无 OOM；真实 %install 转换 225 归档、3,853 bitcode（含回写 1,054.025 s）。新 RPM 225 开发归档格式/顺序/完整索引及零调试节 PASS，45 运行库成员和索引与基线一致。
17,689 路径仅 225 开发归档与 45 compiler-rt ar 时间戳变化，其他文件差异 0；clang/lld/ar SHA 相同。七项宿主消费者及两个独立 Tizen 根的 bfd/lld A+B %check 均 PASS。实测候选 patch SHA `4ca1dc3e…`；docs/31提交版 SHA `0c40c91c…`，W 原件、docs/25–30 均未改。
后续混合目标保留：原生 x86_64 clang/clang++、llvm-ar、lld/ld.lld 静态链接 LLVM 库，
其他工具走共享库路径；别名继承实体形态，上游强制静态例外待审。仅 clang 做首版 BOLT，生成 ARM/AArch64 代码。
基线是工作区 LLVM `f111162e94aa48ed367c9d2c039456c70e7160ae` 的自研 spec，
不是旧公开快照配方。本机筛选不能替代专用服务器 Chromium 全量及全平台验收。
依据：docs/13 §1；docs/21 §0、§1、§4、§6。历史全静态 RPM 仍作为已有基线证据；混合版本一次构建成功且30 TU通过，但额外静态工具及归档索引尚有BLOCKER。

| 阶段 | 范围 | 当前状态 |
| --- | --- | --- |
| 摸底与基准台 | 配方、工具调用面、身份、资源限制、可重复测量 | 完成；历史报告保留各自证据边界 |
| 静态 RPM 基线 | 固定快照、构建、debuginfo 续跑、工具验证、基线数据 | 已完成；历史基线缺陷保留，新x86_64 RPM修法与消费者验收见docs/30 |
| BOLT 筛选 | 容量、插桩/profile、重写、正确性、训练/留出、中间对照、双目标 | 本机工作已结束；最终 ARM 校准 FAIL，AArch64 PASS 并完成正式轮 |
| 静态库兼容性修复 | bitcode→机器码、保持原brp宏、GNU ld无LTO/插件消费者、完整构建及新RPM验收 | **v2新RPM/归档/非归档、独立-bi/SKIP、七宿主消费者与两Tizen包均PASS；基于cb679968的v2补丁已生成并验apply，用户确认356627 PS2已上传、评审中；本轮未重建新目标配方** |
| LLVM包x86_64切换llvm-strip | 叠在356627之后，新增compiler-rt真实运行库消费者及包内验收 | **docs/38全部PASS；用户确认已上传356639，依赖356627；目标流水线待验，代理未推Gerrit** |
| ARM静态库转换 | 参数/工具/路由/PIC与x86不变性设计 | **§12最终x86不变性、两ARM全量转换/重定位/消费者/两种strip PASS；AArch64-bc成功；ARM打包待后续，生产补丁不改** |
| 集成设计与评审 | docs/21 完整 v3、混合链接拟议补丁、身份/活性脚本与协议检查 | 历史混合构建/30 TU结果保留；设计 v4 与 BOLT 实施暂缓，待归档修复完成 |
| OBS 试包与服务器验收 | LLVM RPM → qemu-accel → 新 Base 快照 → Quickbuild | 未执行；项目/验证快照待用户提供，试包与收益验收均未完成 |
| 后续工具/PGO | 依全平台调用占比和服务器容量决定 | 挂账；没有自动启动授权 |

本文件维护规则：

- **每个任务收尾，在同一个产出 commit 更新本文件**：增加进度行，更新结论、裁决和挂账；失败/停止也是任务结果，不冒充成功。
- **新 Session 开场先读本文件**，再核对 `git status --short`、`git log -5 --oneline` 与所引报告/证据；不得因旧报告的历史 STOP/NO 状态重启已关闭工作。
- 每条事实保留证据和适用范围；新证据可替代旧结论，但历史 FAIL 不重判。人工决定单列，不能伪装成实测。
- 当前任务提交无法在内容中嵌入自身 SHA。进度行用“本提交”标明并给出 Git 定位方式；下一任务更新时回填真实 SHA，禁止猜写哈希或为自引用反复追加提交。
- 原始日志、大文件仍放 `temp/`；提交推送遵守 [docs/README.md](README.md)。

## 2. 进度

日期为 Git 提交日期（本地 +08:00），实验跨日时间以报告为准。产出列列出主报告与主要入口；
完整变更清单可用 `git show --stat <提交号>` 查询。每行代表已完成的任务或明确收尾的阶段。

| 日期 | 提交号 | 产出文件 | 一句话结论 |
| --- | --- | --- | --- |
| 2026-09-16 | `2c6e496` | `.gitignore`、`docs/README.md`、`gbs_llvm.conf` | 初始化仓库与产出规范，排除 LLVM 源码和中间产物。 |
| 2026-09-16 | `b1ac328` | `docs/00_workspace_setup.md` | 归档初始化、忽略检查与首次推送证据。 |
| 2026-09-16 | `c31b44e` | `docs/10_tizen_llvm_build_config.md`、`tools/collect_llvm_inventory.py` | 完成配置/工具调查，区分配方能力与实际发布二进制的 UNKNOWN。 |
| 2026-09-16 | `b95ec86` | `docs/12_benchmark_harness.md`、`tools/bench_toolchain.py`、`tools/test_bench_toolchain.py`、`tools/bench_inputs/` | 建立限资源基准台，clang 18 初始校准 PASS，噪声底 0.220%。 |
| 2026-09-16 | `179196d` | `docs/13_baseline_build.md`、`tools/build_llvm_x86_64.{sh,py}`、`tools/test_build_llvm_x86_64.py`、`tools/verify_toolchain.sh` | 交付限流构建与预检入口，预检阻塞时未强行构建。 |
| 2026-09-17 | `d642e1f` | `docs/13_baseline_build.md`、`gbs_llvm.conf` | 钉住实际快照后启动构建，CMake 门禁 297.775 秒通过。 |
| 2026-09-17 | `85d1b8b` | `docs/13_baseline_build.md` | 7634 个编译/链接任务完成，随后 debuginfo -j40 OOM，现场保留。 |
| 2026-09-17 | `647e0d5` | `docs/13_baseline_build.md`、`tools/resume_llvm_x86_64.py`、`tools/collect_llvm_real_tu.py`、`tools/bench_inputs/real_tu/` | -j4 等价续跑产出 22 个二进制 RPM，校准 0.755300% PASS，完成基线与 clang 18 独立参考。 |
| 2026-09-18 | `36a765c` | `docs/14_bolt_feasibility.md`、`tools/llvm_baseline_capacity.json`、`tools/relink_clang_for_bolt.py`、`tools/verify_compiler_outputs.py` | 废除加法容量模型、放行实测同构基线；单 clang 重链成功，记录 BOLT 前置阻塞。 |
| 2026-09-18 | `6d4d73f` | `docs/15_bolt_measurement.md`、`tools/build_bolt_incremental.py`、`tools/run_bolt_stage.py`、`tools/collect_bolt_profile.py` | 统一 driver 后 10 TU PASS，增量补齐 BOLT；18 GiB 插桩两次 OOM。 |
| 2026-09-18 | `6b69661` | `docs/16_bolt_final.md`、`tools/bolt_final_attempt.py`、`tools/finish_bolt_final.py` | 22 GiB 单线程插桩成功，完成 v1 重写、正确性和通过校准的 ARM 训练集正式测量。 |
| 2026-09-20 | `71ba91e` | `docs/17_bolt_holdout.md`、`tools/measure_bolt_holdout.py`、`tools/select_llvm_holdout.py`、`tools/bench_inputs/holdout_tu/` | 新留出集与三方对照齐备，20 TU PASS；两对校准 FAIL，无正式收益认证。 |
| 2026-09-20 | `1ae4437` | `docs/18_spec_integration.md`、`tools/verify_toolchain_identity.sh` | 交付首版集成设计和身份脚本，未改 spec。 |
| 2026-09-21 | `bb2c313` | `docs/19_spec_integration_v2.md` | 确认公开快照 accel 为旧动态形态并登记评审决策；当时停止，后由用户解除。 |
| 2026-09-21 | `16aa937` | `docs/20_spec_integration_v2.md`、`tools/verify_toolchain_identity.sh`、`tools/test_verify_toolchain_identity.sh` | 完整设计 v2；A/A FAIL，relocs 三方校准 PASS，patchelf 节区及 3 TU PASS。 |
| 2026-09-21 | `795a5c4` | `docs/20_spec_integration_v2.md`、`tools/extend_bolt_profile_aarch64.py`、`tools/measure_bolt_aarch64.py`、`tools/bench_inputs/real_tu_aarch64/`、基准台/身份脚本及测试 | 加入 aarch64 profile、产出 v2，30 TU PASS；双目标校准 FAIL 3.334074%，lld/ar 自此仅诊断。 |
| 2026-09-21 | `ea7d120` | `docs/20_spec_integration_v2.md`、`tools/final_bolt_calibration_plan.json`、`tools/run_final_bolt_calibration.py`、`tools/test_final_bolt_calibration.py`、基准台及测试 | 补齐 A/A 事前中止并先提交推送最终拆分校准预注册，等待用户启动确认。 |
| 2026-09-22 | `80bc93a` | `docs/20_spec_integration_v2.md` | 获确认后执行：ARM FAIL 4.272374%，AArch64 PASS 0.835047% 并完成正式轮；本机不再重试。 |
| 2026-09-22 | `312a358` | `docs/STATUS.md` | 建立五段状态备案与每任务同 commit 维护规则。 |
| 2026-09-22 | `153e33e` | `docs/21_spec_integration_v3.md`、`tools/check_bolt_liveness.sh`及测试、身份/基准台/验收规则脚本与测试、`docs/STATUS.md` | 混合机制有条件可行但未应用/构建；两种 strip 均退出0却使副本失活；完成 v3 与功能检查，本机性能校准保持关闭。 |
| 2026-09-22 | `8facdfa` | docs/21、STATUS、活性脚本与测试、验收规则测试 | 保留static-devel并恢复索引门禁；host-arch覆盖；seed改文件级；Quickbuild交内部团队；先推修订再启动本机试构建。 |
| 2026-09-22 | `559879a` | docs/22、STATUS、构建/活性脚本与测试、混合认证指纹 | 新根18GiB构建成功，22 RPM、30 TU PASS；额外五工具仍静态，223空/3残缺归档索引，一次ranlib不能修残缺表。 |
| 2026-09-23 | `dab197c` | docs/23、STATUS | Analysis索引9445→82由GNU strip副本复现；重打包入口遗漏install-pre清理而失败，按约定停止，profile重链/BOLT/30TU未执行。 |
| 2026-09-23 | `583dad4` | docs/24、STATUS | 独占核查通过但22 RPM SHA全异、cache多2文件/7168B，SOURCES spec也已变化；第零步停止，无普查/install/profile实验，未修复资产。 |
| 2026-09-23 | `c12c0e1` | docs/25、STATUS | 归档修复升为第一任务；外来改动备份核对后恢复，新根/新分支就位；全静态基线三个ELF匹配但build.ninja SHA异，第一步停止，完整构建0次。 |
| 2026-09-23 | `773543e` | docs/26、STATUS、归档检查/普查脚本及测试 | 22 RPM与坏COFF SHA通过；270唯一路径/271包条目普查完成；compiler-rt全机器码，libarcher含bitcode且双包归属，按约定停止，构建0次。 |
| 2026-09-24 | `ae6d938` | docs/27、STATUS、离线转换/限流/消费者脚本及测试 | 新方案取消改宏；225归档/3,853 bitcode转换与索引PASS，722.644s、单次最大RSS0.989GiB；程序A调用入口错误、ld未运行，停止且完整构建0次。 |
| 2026-09-24 | `fbac896` | docs/28、STATUS、转换/对照/消费者脚本及测试 | 后端选项补齐，225归档重新转换782.346s、索引/分段PASS；A-bfd/A-lld/B-bfd运行通过，B-lld在4GiB AS下分配失败后停，无cgroup OOM，完整构建0次。 |
| 2026-09-24 | `262480a` | docs/29、STATUS、离线资源/strip/消费者脚本、打包Source、认证入口/指纹及测试 | B-lld诊断、225归档strip、7项消费者PASS；隔离spec已准备，29项测试PASS；唯一构建入口因15.929GiB<16GiB停止，GBS/RPM/测试包均0。 |
| 2026-09-27 | `2267ab4` | docs/30、STATUS、Source/认证指纹/内存等待及测试 | 环境预检修正 GNU time 依赖，五归档回归与45测试PASS；一次完整构建22 RPM，225开发/45运行库、其他文件零差异、七消费者及Tizen bfd/lld两个A+B包内验收全PASS。 |
| 2026-09-28 | `81ca23c` | docs/31、STATUS、patches/archive-index-fix/ 下补丁与 Source | 干净 f111162e 上最终 format-patch apply --check PASS，完整 tree 一致；Source SHA2476c5ef…，spec 与docs/30仅三处并发差异，无构建/无Gerrit推送。 |
| 2026-09-29 | `4adbdfb` | docs/32、STATUS、候选Source/测试及构建指纹 | 68测试PASS；3853命令分类、类型普查与五档第一遍同SHA；外部Ninja破坏独占后中止，确定性/600s复验未完，无完整构建，v2未发布为可提交format-patch。 |
| 2026-09-29 | `4d80d94` | docs/33、STATUS、probe_hq_llvm_strip.py、inventory_llvm_source_consumers.py | 中间发布strip/宿主/快照调查与新8/6内存规则；当时Tizen B-lld仍运行，未冒称完整验收。 |
| 2026-09-29 | `66c5671` | docs/33、STATUS | 两包串行各一次，bfd格式失败；lld A链接/独立运行正确，B在6GiB下持续抖动后诊断性中止、无OOM/%check未执行；完整记录等待读数、峰值、边界与回收，无方案选择结论。 |
| 2026-09-30 | `d47d150` | docs/34、STATUS、verify_llvm_strip_overlay.py、认证指纹 | v2离线门禁补齐、70测试PASS；HQ llvm-strip叠加的一次6/6/2构建CMake PASS，7530/7634后按用户要求节前暂停；无OOM，现场保留、进程和锁已回收，未生成v2提交补丁。 |
| 2026-10-08 | `c1856d0` | docs/34、STATUS、认证指纹状态 | 核验后恢复同一构建，4:15:51正常产出22RPM、225开发档PASS；首个compiler-rt成员ELF与基线不同，按预定门禁停止；未继续消费者/测试包/续跑，v1不变，无Gerrit推送。 |
| 2026-10-09 | `f49a561` | docs/35、STATUS、认证指纹 | S/根内spec恢复标准提交配置，Source不变；87项头文件dry-run。磁盘连全部允许cache回收上界仍不足60GiB，增量构建0次、缓存未删，后续验收/补丁未执行。 |
| 2026-10-09 | `9f27fbc` | docs/35、STATUS、认证执行状态 | 授权清理后增量产出22RPM；225开发/45运行库、非归档零差异、独立-bi/SKIP与7宿主消费者PASS；Tizen bfd依赖解析FAIL、Base HTTP404，按规则停止，无重试/无v2最终补丁。 |
| 2026-10-09 | `213041c` | docs/36、STATUS、patches/archive-index-fix/ | 107历史Base缓存RPM与原primary摘要一致；两Tizen包113环境零NEVRA差异、A/B及身份PASS；v2补丁基于刷新tizen_base cb679968，apply/tree验证PASS，无LLVM重建/无Gerrit推送。 |
| 2026-10-09 | `25e2b18` | docs/37、STATUS | 原根rpmspec/完整宏环境只读展开；cb679968参数差异已分类，225档/3,853条派生命令全PASS、未分类0；认证策略覆盖，无构建/转换/spec/Source/补丁变更。 |
| 2026-10-09 | `834f9aa` | docs/38、STATUS | 22RPM与N的17,689路径身份PASS，宏链作用范围只读核查完成；允许清理后空间上界50.816586GiB<60GiB，第零步STOP；未改spec、未构建/验收/生成llvm-strip补丁。 |
| 2026-10-09 | `08e0889` | docs/38、STATUS、patches/llvm-strip/ | 授权rename保全+清理后一次增量22RPM成功；225/45归档、270次strip、非静态库零差异、宿主/Tizen全部消费者PASS；叠在356627 PS2的独立4行补丁apply/tree PASS，未推Gerrit。 |
| 2026-10-09 | `d849dc8` | docs/39、STATUS | ARM配方/策略差异与22.1.8工具查明；显式accel/QEMU小实验成功，自动binfmt/磁盘与全量认证仍有缺口；只交实施草案，未改Source或补丁。 |
| 2026-10-10 | `f6a0499` | docs/41、STATUS | 只读盘点102项目录/子范围，567条会话元数据；明确保留输入及权限/归属缺口，量化6.646GiB可删建议与173.887GiB仅载荷建议，未清理。 |
| 2026-10-10 | `26da4ac` | docs/42、docs/40、STATUS | A1回收180.533333GiB；A2因保留05E工作树的共享Git依赖在rm前停止；A3日志与sudo脚本已准备未执行；B/C未执行。 |
| 2026-10-10 | `e66396a` | docs/40、STATUS、新ARM试验Source及夹具 | 225原档身份一致；225整档/3864成员/完整索引/后端flags与docs/35完全一致；60测试PASS，ARM仍为待认证草案。 |
| 2026-10-10 | `e44fb63` | docs/40、STATUS | B全量x86回归PASS已发布；C0查明正常GBS会写宿主mmap_min_addr，遵守禁止sysctl变更而不启动，ARM两阶段NOT RUN；锁/scope/采样器回收。 |
| 2026-10-10 | `d1d720e` | docs/40 §8、STATUS | 标准GBS初始化获授权后只读预检：指定Base404、Unified200，GBS零次，C1–C4未执行；Source/配置/宿主状态不变，锁已回收。 |
| 2026-10-10 | `2c9081b` | docs/40 §9、STATUS | 用户新配置两源200；ARM32/AArch64 C0、accel22和宏一致性PASS；GBS导出成功后代理SHA断言误拒VCS元数据，停止且未进入LLVM prep/configure/编译；缓存保留，锁/采样器/挂载回收。 |
| 2026-10-10 | `256d759` | docs/40 §10、STATUS | 导出spec/tar身份PASS；新ARM32 prep与宏参数PASS，代理configure准备宏查询修正后exit28，按第二次失败停止；LLVM编译0，缓存/现场保留。 |
| 2026-10-10 | `8dd3d9a` | docs/40 §11、STATUS | ARM32标准-bc全7147任务PASS，scope峰15.335GiB；210档普查/参数PASS，转换遇TLS_GD32按门禁停止；消费者及A64未运行，原件/cache保留。 |
| 2026-10-10 | `cb899cd` | docs/40 §12、STATUS、ARM候选Source及测试 | TLS/Thumb修订，67测试和最终SHA的225档/3864成员x86全量回归PASS；先发布，再继续ARM32。 |
| 2026-10-10 | `256267b` | docs/40 §12.4–12.7、STATUS | ARM32 210档/3690成员转换与Thumb/重定位PASS；未strip、GNU/LLVM strip三套消费者PASS；辅助资源目录遗漏修正一次。 |
| 2026-10-10 | `2058761` | docs/40 §12.8–12.13、STATUS | AArch64-bc 7545任务PASS；212档/3706成员、3699 bitcode转换、全集重定位与三套消费者/两种strip全PASS；原件/cache保全，锁/进程/挂载回收，第一段结束。 |
| 2026-10-10 | `ddc7310` | docs/43、Source差异文档附件、docs/40入口、STATUS | 整理候选1620a8da外部评审包（≤50KB）：固定版本链接、策略/实测边界、67项测试；仅文档，既有认证结果不改判。 |
| 2026-10-10 | `835ebef` | docs/44、STATUS | 51无属性成员/全部函数属性普查通过；A64三条真实module asm与新禁止规则冲突，修改前STOP；无Source/测试/转换修改或复验。 |
| 2026-10-10 | `b2ea0f9` | docs/45、docs/44收尾、STATUS | 两待评审Gerrit补丁材料包完成，仅既有证据；保持ARM策略冲突STOP，Source/测试/patch未改，scope/锁/进程回收。 |
| 2026-10-10 | `c8898cd` | docs/44 §7–§12、完整diff、候选Source/测试、STATUS | 13项修订已写入；唯一辅助修正后94/95 PASS，既有取消测试FAIL；全量复验NOT RUN。 |
| 2026-10-10 | `270f3ec` | docs/45、STATUS | 只读补全356639 PS1完整号，链接本轮最终docs/44；披露x86 module asm符号核查未执行，维持测试STOP。 |

本文件建立提交：`git log --diff-filter=A --format='%h %ad %s' --date=iso-strict -- docs/STATUS.md`。
上述历史主报告可能后续原地更新，核查当时结论使用 `git show <提交号>:<文件路径>`。

| 2026-10-10 | 本次诊断提交（git log -- docs/44） | docs/44 §13、STATUS | 600例诊断PASS，8次R均挂起SIGKILL；原Commands不改，进入后续门禁。 |

## 3. 已闭合结论

- 硬证据（实现/测试观察，非产物认证）：候选5608aa5e与1620的x86共用函数AST相同；95测试第二次94 PASS/1 FAIL，失败时子进程状态R。根因UNKNOWN，不能宣称新候选已通过；x86/ARM全量复验均未执行。证据docs/44 §8–§10、temp/arm-source-review-continue-20261010/source-isolation.json、unit-tests-host-retry.log。


- 硬证据：51无目标函数属性成员全部define=0、module asm=0；ARM32 484,265/A64 329,616个define必需属性齐备。实际module asm ARM32=2、A64=3，原文均`.globl _ZSt21ios_base_library_initv`；证据docs/44 §1–§3及E/census-result.json、module-asm-all.json。新门禁冲突不重判docs/40历史功能PASS。

- 文档整理完成，非新增实测：docs/43把最终Source1620a8da与既有x86/ARM第一段证据绑定，并列出未覆盖类型/安装边界；完整diff相对生产6bd0546a。证据强度：硬证据（文档与固定版本核对），沿用docs/40 §12实测；67测试与全量回归没有在本轮重跑。

证据强度约定：**硬证据**＝源码/元数据/原始命令/逐字节检查等直接事实；
**通过校准**＝相应测量对满足当时协议，不自动代表服务器验收；
**诊断**＝未通过门禁或未做正式验收的数据，只能描述观测，不能作认证收益。
“闭合”仅限表中命题和输入范围；不是所有未知问题都已解决。

| 结论与边界 | 证据 | 强度 |
| --- | --- | --- |
| 指定ARM配置Base 20260813.050338的repomd返回HTTP404（146B、SHA55f7d9e9…），Unified200；未启动GBS，mmap_min_addr前后65536、binfmt未变。该时点仓库不可用，不是ARM代码生成失败。 | docs/40 §8；temp/arm-archive-stage1-c-20261010/c0-preflight/、result.json | 硬证据（HTTP/身份/未执行边界） |
| 隔离ARM草案Source选择x86时，225原始归档身份一致；转换后225整档、3864有序成员及完整索引与docs/35完全相同，3853条后端flags顺序一致，60相关测试PASS。仅认证x86路径，不认证真实ARM归档。 | docs/40 §5；temp/arm-archive-stage1-20261010/x86-regression-result.json | 硬证据 |
| 工作区 spec 配方未启用 PGO/BOLT；不能据此断言旧发布/accel 二进制也未使用，后者仍有 UNKNOWN。 | [docs/10 §1、§2.3](10_tizen_llvm_build_config.md) | 硬证据（配方）；发布身份缺口不填空 |
| 静态 RPM 基线已产出 22 个二进制 RPM；clang/clang++/ld.lld/llvm-ar/llvm-ranlib 均无 libLLVM/libclang-cpp NEEDED。“静态”只指 LLVM 库，不指 libc。 | [docs/13 §7](13_baseline_build.md)；`temp/baseline-resume-20260917/rpm-inventory.json`；docs/20 §1.1 | 硬证据 |
| 首轮 7634 任务在 18 GiB cap 下完成；OOM 在 debuginfo -j40，改 -j4 后产包。单次链接高水位 16.83 GiB，不能将不同阶段峰值简单相加。 | docs/13 §1、§7、§11；[docs/14 §2](14_bolt_feasibility.md) | 硬证据 |
| 单 clang emit-relocs 重链成功：227.656 s、lld VmHWM 9.760868 GiB；这是热 ThinLTO cache 实测，不能当冷缓存上界。 | docs/14 §4.1；docs/20 §2.4 | 硬证据 |
| BOLT 插桩 18 GiB 两次 OOM 为 cap 截断；22 GiB、单线程后成功，自身峰值 19.722076 GiB、66.00 s，非截断。 | [docs/15 §4.2](15_bolt_measurement.md)；[docs/16 §5](16_bolt_final.md) | 硬证据；仅该输入/参数 |
| **纯重写约 3.7 GiB**：v2 自身 VmHWM 3.678791 GiB、24.43 s，在 6 GiB cap 下完成且无 OOM；v1 为 3.481499 GiB、21.83 s。不同于插桩；不覆盖更新 DWARF 的资源成本。 | docs/20 附录 D.3；docs/16 §5 | 硬证据 |
| **30 TU 逐字节相同**：v2 对 RPM 基线，ARM 训练 10 + ARM 留出 10 + aarch64 训练 10；统一 `clang-22 --driver-mode=g++`，比较完整 .o，未排除命令行节区。此前 v1 的 ARM 训练+留出共 20 TU 也 PASS。 | docs/20 附录 D.4；[docs/17 的 20/20 记录](17_bolt_holdout.md) | 硬证据；不自动覆盖未来 RPM/accel 后处理产物 |
| **重链/剥离中间影响在本次负载上接近 1，不能写“严格无影响”**。两轮 GM(relocs/RPM)=0.999675/0.997163，GM(stripped/relocs)=1.001075/1.000822，GM(stripped/RPM)=1.000749/0.997983。噪声底 1.986133% PASS；未追加正式轮，不能跨轮反算 docs/16 的纯 BOLT 收益。 | docs/20 附录 B 的同轮三方表及因果边界 | 通过校准；中间对照诊断实验 |
| ARM v1 训练集正式 GM(v1/RPM)=0.846042，即耗时降低 15.3958%；前置噪声底 1.595225% PASS。13 项，分母同轮 RPM，**含重链/剥离/BOLT**。 | docs/16 §8；docs/20 §5 | 通过校准；正式/训练集，不是留出或平台收益 |
| AArch64 最终训练集正式 GM(v2/RPM)=0.848116、GM(v1/RPM)=0.852074、GM(v2/v1)=0.995354；前置噪声底 0.835047% PASS。10 项，前两者含重链/剥离/BOLT。内部“约 15%”只能指该口径的**耗时降低**，不是吞吐增幅或全平台收益。 | docs/20 §7.1.1、§7.1.3–7.1.4；`temp/bench_results/bolt-final-split-20260921/aarch64/formal.json` | 通过校准；正式/训练集、第二顺位已暖机 |
| **v1 虽只用 ARM 训练，已在第二顺位、已暖机的 aarch64 编译负载上呈现通过校准的正向效果**（上行 v1/RPM）。这不是 v1 曾采 aarch64 profile 的证据，也不证明覆盖整个 AArch64 后端；v2/v1 接近 1，增量收益未确证。 | docs/20 §3.1、§7.1.3–7.1.4 | 通过校准（性能观测）；不作函数覆盖推断 |
| 最终 ARM 校准 FAIL 4.272374%，未跑正式轮；v2/v1 两轮诊断 GM=1.002496/1.004235，不能确证 ARM 非退化。全程采样 load1 最大 4.28，无 >10 样本、无保留 suspect，采样器已回收。 | docs/20 §7.1.1–7.1.2；`temp/bench_results/bolt-final-split-20260921/attempt.json`、`loadavg-summary.json` | 诊断（性能）；硬证据（执行/门禁状态） |
| 历史 FAIL 保留：docs/17 两对 4.345326% / 6.609160%；docs/20 附录 A 为 3.846399%；附录 D 双目标为 3.334074%。不按新协议回判，也不把拆分 AArch64 PASS 合成为双目标 PASS。 | docs/20 §5、§7、§7.1、附录 A/D | 诊断；失败判定已闭合 |
| 公开 Base 快照 `tizen-base-toolchain_20260912.061113` 的 accel 仍动态链接 LLVM，与工作区静态基线不同；证明该快照陈旧，不否定已确认的 OBS 流水线。 | [docs/19 §1.2、§3](19_spec_integration_v2.md)；docs/20 §1.1 | 硬证据（ELF/VCS）；流水线为用户确认前提 |
| 已取得的同 VCS qemu-accel aarch64 spec 通用主体有 cp -aL、patchelf 解释器/RUNPATH 处理、cmp 恢复别名软链接、fdupes/转包接口；跨此环节不能要求 ELF SHA 不变。armv7l 完整分支/隐式后处理仍缺证据。 | docs/19 §2.1–2.2；docs/20 §1.2 | 硬证据（已取得源码范围） |
| 本机 patchelf 副本实验保留 `.note.bolt_info`、`.bolt.org.*`、`.text.cold`，3 TU 完整 .o PASS；不能替代 OBS brp/fdupes/完整 accel 转包验证。 | docs/20 附录 C | 硬证据；单一显式转换 |
| 身份脚本新增 NAME_ONLY、扩展名、foreign 注册表错误、只读非可执行文件及强制 no-exec 测试 override；67 项 PASS。基准台完整性与任意行 suspect 门禁 19 项 PASS；验收规则共29项 PASS；冻结 plan/启动器未改。 | docs/21 §7、附录 E；`temp/spec-v3-20260922/*tests*.log` | 硬证据（功能/协议测试）；无新性能认证 |
| 原 BOLT clang 活性 PASS；R1 GNU strip/eu-strip 处理副本均退出0，前者 LOAD=5 但 version/最小TU SIGSEGV，后者 LOAD=0、version/编译127；原件SHA未变。后处理仅看退出码或 BOLT note 不够。 | docs/21 附录 C；`temp/spec-v3-20260922/liveness/` | 硬证据；仅所列工具/输入/默认 strip 参数 |
| AddLLVM per-target与Clang/LLD PUBLIC传递边的七文件补丁已在隔离分支试构建；CMake302.105秒通过，plugin导出分支OFF未覆盖；三静态实体与八共享抽查工具NEEDED符合。 | docs/22 §1–§5；`temp/hybrid-trial-20260922/run/`、`products/` | 硬证据；五个额外静态工具仍不符合范围 |
| 按旧 accel 文件集合的模型，混合+BOLT v1 常规文件668507104 B，全静态工具+BOLT v1 为2763020832 B；旧包54806369 B。压缩代理分别152926303/632062933 B，不是实包预测保证。 | docs/21 §1.2；`temp/spec-v3-20260922/size-model.json` | 诊断（实测文件大小上的模型估算）；新 ldd 闭包/压缩实包未测 |
| 两归档 primary 中包名及225开发归档路径/文件名 Requires 查询均0；不覆盖 OBS BuildRequires 或未声明的文件使用。基线 compiler-rt 另有45个.a，libarcher_static.a也归libomp-devel。 | docs/21 §0.1、附录 B；`temp/spec-v3-20260922/reverse-dependencies.json`及`*-files.txt` | 硬证据（查询范围）；删除安全性未闭合 |
| 最后 ARM 原始数据为39/39组合跨轮负偏；v2/RPM配对GM跨轮变化0.068292%，不是所有行误差上界。run1 CV高、无load>10；与暖机共模漂移解释一致，未唯一证明物理根因。 | docs/21 §7；`temp/spec-v3-20260922/noise-reanalysis.json` | 诊断；原ARM FAIL不变 |
| 混合指纹全新构建18GiB、4/4/1、debuginfo4成功，wall1:24:00，22二进制RPM；scope峰值18GiB并回收，OOM=0，采样器回收、scope inactive。普通基线准入未放宽。 | docs/22 §2–§4；`temp/hybrid-trial-20260922/run/outcome.json`、`scope-reaped.json` | 硬证据；单次受限容量实测，不是无上限峰值 |
| 混合libLLVM链接129.854s/11.292168GiB，clang静态链接443.526s/15.177582GiB；2秒VmHWM采样有末区间遗漏界限。 | docs/22 §4；`temp/hybrid-trial-20260922/resource-summary.json` | 硬证据；构建资源，无性能比较 |
| 混合clang对全静态TC：ARM训练10+留出10+AArch6410，完整.o全部逐字节PASS；统一driver/资源/sysroot/flags。RPM SHA不同，profile v2不能直接认证。 | docs/22 §6；`temp/hybrid-trial-20260922/correctness-*/result.json` | 硬证据；仅30个TU，不证明代码图/性能相同 |
| 19个包.a清单空，static-devel225、libomp-devel1、compiler-rt45（明确保留运行库）。226开发归档中223无索引，3仅残缺；一次ranlib副本全非空，但3残缺未补齐，因为源码遇已有表直接return。原RPM不改。 | docs/22 §5.2；`temp/hybrid-trial-20260922/archives/`；llvm/llvm/tools/llvm-ar/llvm-ar.cpp:1084–1093 | 硬证据；非空不足认证完整性，发货BLOCKER |
| 额外静态例外实测为llvm-config、llvm-exegesis、llvm-tblgen、clang-tblgen、lldb-tblgen；本轮未豁免或修改补丁。clang/lld活性及身份脚本检查PASS。 | docs/22 §5.1、§5.3；`temp/hybrid-trial-20260922/products/tools.json` | 硬证据；混合范围未全部满足 |
| Analysis的131成员含125 bitcode+6 ELF；原RPM的82条索引恰好来自6 ELF，一次GNU strip -g副本9445→82且映射与RPM相同，退出0仍损坏索引。 | docs/23 §1.1；`temp/archive-profile-rebind-20260923/root-cause/` | 硬证据；当前R工具/输入组合 |
| 唯一重打包尝试失败：试验入口漏处理Tizen install-pre清空BUILDROOT，rpmbuild rc=1、新RPM=0；不是修法被证伪，也不能断言RPM不支持短路。按失败即停，未重试或继续profile实验。 | docs/23 §1.2、§2；`temp/archive-profile-rebind-20260923/repack-scope/outcome.json` | 硬证据；修法包级验收与profile适用性仍缺失 |
| 本轮独占检查无相关外部进程/既有锁；会话锁已回收。B/clang体积及已提交docs/23的SHA参考匹配，三归档计数9445/14276/5023匹配；22 RPM对docs/22 SHA为0/22匹配，cache为12471文件/20363368128B（+2/+7168），SOURCES spec SHA已异。仅证明文件身份差异，未比较RPM payload或定位写入者。 | docs/24 §1–§3；`temp/archive-fix-verification-20260923-173328/assets.json`、锁记录 | 硬证据；第零步FAIL，不能外推修法或profile结果 |
| 指定全静态B0的clang-22/lld/llvm-ar三SHA匹配docs/13；build.ninja当前133b142f…，docs/14为81216d3d…，第一步身份核查退出2。docs/15此前登记同目录获准加bolt重新configure；不能把目录继续当原始图，也不能从图差异推断归档损坏。后续RPM/归档检查未跑。 | docs/25 §1；`temp/archive-index-fix-20260923/baseline-identity.json`；docs/15 §3.2 | 硬证据（3 ELF/图身份）；归档与修法仍未测 |
| docs/13基线22 RPM SHA全匹配，重新解包坏liblldCOFF.a为9e8915f4…；270唯一归档/271包条目。compiler-rt45个、1964成员全ELF且索引完整覆盖机器码外部定义；static-devel225个（含libarcher）222空索引/3混合残缺。libarcher唯一成员ompt-tsan.cpp.o头4243c0de，空索引，同时属于libomp-devel与static-devel，触发运行库格式停止条件。 | docs/26 §1–§2、附录A；`temp/archive-index-fix-rpm-20260923/census-summary.json`、`runtime-blocker-raw.json` | 硬证据；只读基线普查，非新修法验收 |
| 22 RPM SHA与17,689基线路径元数据复核一致；225归档中的3,853 bitcode全部转x86_64 ET_REL，11原ELF SHA不变，成员顺序/名称一致，索引恰为外部定义多重集合318,543条。PIC静态扫描无禁止项，但共享库PIC/消费者未验。 | docs/27 §1–§3、附录A；`temp/static-native-conversion-20260924/conversion-summary.json` | 硬证据；docs/27历史格式/索引结果，因后端选项不全，产物已按新决策作废，不再复用 |
| 离线转换wall722.644133s、单次最大RSS0.989471GiB、11GiB scope峰值6.532276GiB，无OOM；首个消费者因显式loader下多job cc1路径错误退出1，尚未进入GNU ld，不是转换方案被证伪。未重试，spec/构建入口未改。 | docs/27 §3–§4；`temp/static-native-conversion-20260924/consumers/link-a-bfd.log`、两scope outcome.json | 硬证据；消费者兼容性未验证 |
| 补齐function/data sections及后端默认值后，225归档/3,853 bitcode重新转机器码；11原ELF SHA不变，顺序/名字一致，完整索引318,543条，PIC静态扫描和10成员分段抽查PASS。wall782.346390s，单次最大RSS0.998772GiB，13GiB scope峰值6.184643GiB，无OOM。 | docs/28 §1–§3、附录A/B；`temp/static-native-conversion-v2-20260924/conversion-summary.json` | 硬证据；仍为未strip离线库，不是新RPM认证 |
| 真实ARM TU直接native与ThinLTO-IR/native均917个非NULL节区、205函数节区；定义符号集合/绑定/可见性一致。重定位和ARM映射标记重复次数的差异逐项解释；不要求或宣称字节相同。 | docs/28 §2；`temp/static-native-conversion-v2-20260924/options/review.json` | 硬证据；单TU结构对照，不是全库语义证明 |
| 消费者入口拆成-c及对象链接，A-bfd/A-lld均跑PassBuilder O2并与基线opt全文一致；B-bfd库内lld链接并运行生成物exit=37。B-lld在4GiB AS下报分配失败，scope峰值4.983799GiB/12GiB、oom/oom_kill=0、宿主最低available15.835712GiB；没采VmSize，具体失败分配未知，不能推断物理内存需求。失败后未重试或继续共享库/GC/反例，未改spec，构建0次。 | docs/28 §4–§6；`temp/static-native-conversion-v2-20260924/consumers/result.json`、consumer-scope/memory-summary.json | 硬证据；三项消费者通过，整体验收FAIL且未发货 |
| 原未strip B-lld同argv仅去掉AS后链接成功，VmPeak5,343,096KiB>4GiB、VmHWM3,773,956KiB、17线程；12GiB scope峰值3,997,483,008B、事件全0。满足预设判据，确认docs/28失败来自4GiB RLIMIT_AS。 | docs/29 §1–§2；`temp/static-native-conversion-v3-20260924/diagnostic-summary.json` | 硬证据；单次诊断，77.81s不是性能对照 |
| docs/28新转换225归档经R0 GNU strip2.43副本实验全部PASS，3,864个成员次序/重复身份不变、零调试节、318,543完整索引；原11机器码所在三归档也通过。体积6,615,084,040→520,479,520B。 | docs/29 §3/附录A；`temp/static-native-conversion-v3-20260924/strip-summary.json` | 硬证据；离线strip，不等于完整RPM后处理 |
| strip后A-bfd/A-lld、共享库dlopen及GC输出与opt O2全文相同；B-bfd/B-lld库内链接生成物均exit37；未转换H反例因原索引缺失被GNU ld拒绝。七项功能门禁PASS；短命令VmPeak未捕获处UNKNOWN。 | docs/29 §4；`temp/static-native-conversion-v3-20260924/consumers/result.json`、consumer-ir-identities.json | 硬证据；宿主GCC13/glibc＋Tizen LLVM/libxml2离线环境，非Tizen包内验收 |
| x86_64-only %install转换和Source仅写S，精确认证绑定spec/Source/diff/路径/分支/锁，CMake契约与docs/13相同；29测试PASS。15:35:18唯一完整构建入口被15.929GiB<16GiB门禁拒绝，未启动GBS，未重试。 | docs/29 §5–§7；`temp/static-native-conversion-v3-20260924/full-build/stopped.json` | 硬证据；补丁可评审，完整构建/RPM/Tizen验证未闭合 |
| 固定构建根安装 Python3 3.14.2，未安装 GNU time；Source 改为 wait4，prlimit 4GiB 与后端选项不变。五代表归档498成员（488转换）与docs/28逐成员及整档SHA相同，45测试PASS。 | docs/30 §1；temp/archive-fix-full-build-20260927/five-result.json、依赖/测试日志 | 硬证据；已在真实Tizen %install执行成功 |
| 新根一次完整LLVM构建成功、22 RPM；CMake门禁316.081s；入口wall16,011.555s，scope18GiB/swap0、4/4/1、debuginfo4，无OOM。scope峰值恰到18GiB，含页缓存，不是无约束自然峰值；time RSS16,599,128KiB。 | docs/30 §2；temp/archive-fix-full-build-20260927/full-build/ | 硬证据；容量/正确性实测，不是性能基准 |
| 新RPM开发归档225个/3864成员全x86_64 ET_REL、零bitcode/调试节，完整索引318543条，成员身份顺序与本次构建树一致；compiler-rt45个/1964成员SHA和索引相同，整档仅ar header mtime不同。 | docs/30 §3.1–3.3；new-archives-result.json、runtime-ar-header-differences.json（均在temp/archive-fix-full-build-20260927） | 硬证据；真实完整RPM后处理已验 |
| 新旧17689路径差异只含225开发归档与45 runtime时间戳，其他0；clang-22/lld/llvm-ar SHA同基线。原brp宏未改，归档strip执行1次、格式错误0。七项宿主消费者PASS；两个新Tizen根分别用bfd/lld构建A+B，%check O2输出相同、生成物exit37，各根225归档+4工具SHA匹配新RPM。 | docs/30 §3–§4；rpm-file-comparison.json、new-rpm-consumers/、tizen-bfd/、tizen-lld/（均在temp/archive-fix-full-build-20260927） | 硬证据；x86_64固定快照验证，不外推ARM/AArch64 |

提交补丁新增闭合项：docs/31 §2–§3、`temp/archive-fix-submission-20260928/verification.json` 证明 format-patch 在干净 HEAD 可应用、应用后完整 tree 与单提交一致、Source 同字节、spec 仅三处并发差异。**证据强度：硬证据**。不把 6/6/2 当成本机已验证容量。

对外统一口径：**筛选层多轮测量方向一致，BOLT 对 LLVM 自身源码编译负载有稳定正向影响，量级待构建服务器验收。**
不对外给收益百分比，不称“五轮独立”，不将训练集结果或诊断比值当作留出泛化认证。

v2修订阶段新增证据：docs/32 §1–§2、`temp/archive-fix-v2-20260929/final-tests.log`（68 PASS）、`final-policy-audit.json`（3853命令）、`type-metadata-census.json`（225档/3853成员语义类型标记0）、`five-regression-results.json`（首遍498成员/5整档与E28相同）。**证据强度：硬证据，限已完成检查**；不能外推为最终v2 Source两遍确定性、新RPM验收或6/6/2容量PASS。

上一轮新增实测（docs/33）；E33=`temp/llvm-strip-alternative-20260929`：

| 结论 | 证据 | 证据强度 |
| --- | --- | --- |
| R0 llvm-strip22 对225个完整索引bitcode归档均exit1且SHA不变，共225错误；ASan纯ELF strip成功、调试节去掉、索引保留。索引保留来自失败未写回。 | docs/33 §1；temp/llvm-strip-alternative-20260929/strip/、bc-inventory.json、strip-all-bitcode/ | 硬证据 |
| 完整索引BC的A：clang+bfd无插件与g+++bfd失败；lld22和bfd+LLVMgold22均成功且IR与opt一致。 | docs/33 §2；E33/host-consumers/result.json | 硬证据（正确性）；链接耗时/RSS是受限单次诊断，不是性能认证 |
| LLD18读LLVM22 BinaryFormat报Unknown attribute kind；同工具读取转换后的机器码BinaryFormat成功。g+++bfd链接转换库成功，A输出正确。 | docs/33 §2/§4；E33/old-llvm/、additional-controls/ | 硬证据；版本结论限该样本 |
| 固定Base/Unified源元数据361/1061条：static-devel直接BR只有bcc-tools、bpftrace；bcc三架构与bpftrace两ARM实际选择共享LLVM/clang，不能把BR名单等同静态库受影响名单。 | docs/33 §5；E33/dependency-scan-summary.json、consumer-buildlog-evidence.json、sources/ | 硬证据（限定公开固定快照）；未完整跟踪最终ld exec的项明确UNKNOWN |
| Tizen模拟HQ RPM：225归档身份核对；bfd A报file format not recognized；lld A链接64.106504s/6012260KiB，单独运行输出与同根opt逐字节相同。 | docs/33 §3；E33/tizen-summary.json、tizen-a-postabort.json | 硬证据（限定A）；包内完整%check未执行 |
| B-lld在6GiB下7325.348s后由代理诊断性中止，RSS峰6101756KiB；scopepeak=6GiB、oom/oom_kill=0，宿主最低8.765GiB。不能解释为本征不兼容或成功耗时；用户未新增时限批准。 | docs/33 §3.2；E33/tizen-lld/diagnostic-abort.json、build.log、scope-after-rpm.json | 诊断；B最终链接/运行结果UNKNOWN |
| 完整LLVM16GiB准入/18GiBcap未改；本轮两小包按8GiB/6GiB/swap0串行，全部69旧等待读数保留。保护资产SHA相同，采样/日志线程已回收、锁已释放。 | docs/33 §0、§3、附录；E33/final-integrity.json、lock-released.json | 硬证据 |

本轮阶段备案（docs/34）；E34=`temp/archive-fix-v2-build-20260929`：

| 结论与边界 | 证据 | 证据强度 |
| --- | --- | --- |
| 最终v2 Source转换225档全部通过，与docs/28整档SHA相同；五档两遍确定性、真实删除强符号负例、603.252秒的600秒超时复验通过；68+2项测试PASS。 | docs/34 §1–§2；E34/offline-gates.json、conversion-vs-docs28.json、five-regression-results.json、negative-real-final-results.json | 硬证据，限离线检查 |
| 225开发档+45运行库两遍llvm-strip共540次exit0；身份/索引/无DWARF/确定性PASS。与GNU输出全部成员ELF字节不同，运行库allocated载荷相同但部分节头亦有差异，不能称仅ar时间戳不同。 | docs/34 §1.2–§1.3；E34/llvm-strip-overlay/、strip-elf-analysis/ | 硬证据；语义诊断不豁免新RPM门禁 |
| 9月30日历史暂停：一次6/6/2构建CMake316.524秒PASS；clang和libclang-cpp受限链接后完成，7530/7634时用户要求暂停。18GiB触顶、OOM0；当时构建及新RPM验收未完成。 | docs/34 §3.1–§3.2；E34/full-build/、pause-20260930-1919/ | 硬证据（历史执行与暂停）；内存压力为诊断 |
| 10月8日核验暂停输入与准备源码后，正常-ba --noprep完成208个增量任务及打包，产出22RPM。恢复段15351.381秒，两段合计85616.511秒，18GiB触顶但OOM0；耗时不作性能结论。 | docs/34 §3.3–§3.5；E34/resume-20261008/build/{outcome,scope-after-rpm}.json、E34/rpm-inventory.json | 硬证据，仅该次受限构建；不是无中断或自然内存峰值认证 |
| 新RPM全部225开发归档：3864成员、bitcode/other=0、全x86_64 ET_REL、无DWARF、完整符号索引和原序/同名身份PASS；10成员分段抽查PASS。Source强符号缺失0，允许W缺失1920。 | docs/34 §4.1；E34/new-archives-result.json、new-archive-checks/、install-conversion-summary.json | 硬证据，不替代消费者验证 |
| 新RPM compiler-rt首档asan-preinit成员3536→3464B，ELF节11→10，字节一致性FAIL；索引/无DWARF通过。新输出与离线llvm-strip整档及成员SHA相同；allocated载荷相同只作诊断，不豁免门禁。其余44档及后续验收未继续。 | docs/34 §4.2–§4.3；E34/resume-20261008/failed-runtime-diagnosis/、archive-acceptance.log | 硬证据（字节与门禁）；语义等价仍未证明 |
| 构建后仅回收本次已完成链接的20GiB可再生cache；没有改裁剪参数/对象/ELF/历史根。最终scope inactive、本项目构建进程0、采样器与锁均回收；W、docs25–33、v1等保护文件一致。 | docs/34 §3.4、§4.3；E34/resume-20261008/cache-reclaim-result.json、final-process-check.json、lock-released.json、final-protected-files.json | 硬证据 |


前次备案（docs/35，以下四行按`f49a561`原报告节号核对）；E35=`temp/archive-fix-v2-final-20261009`：

| 结论与边界 | 证据 | 证据强度 |
| --- | --- | --- |
| S spec恢复为6a91a0bf…，Source仍6bd0546a…，完整diff751a6292…；三者与docs/32候选一致。configuration对象逐项等于docs/32，根内导出spec仅作同一获准删除。 | docs/35 §1；E35/configuration-restoration.json、trial/root-spec-restoration.diff | 硬证据 |
| 原根最终CMakeCache及4个关键ELF SHA匹配；Ninja两状态文件旧前缀SHA匹配。docs/34未单独存末态图/状态完整SHA，不能声称有该历史比对；本轮已存完整恢复清单。 | docs/35 §0.1；E35/current-state-audit.json、resume-input-manifest.json | 硬证据限已核项目；未存的历史摘要UNKNOWN，不判污染 |
| ninja -n退出0：86个LLDB头文件stage+1个utility，未列编译/链接；查询宏为/bin/strip、clang、-j4。未运行CMake或%install。 | docs/35 §1.1；E35/dry-run.log、dry-run.json | 硬证据，仅dry-run和宏查询 |
| 可用内存21.837860GiB满足；磁盘18.761387GiB，全部20872个cache回收上界54.724190GiB仍不足60GiB。原资源入口拒绝，未启动构建、未删缓存；没有耗时/峰值/新RPM或消费者结果。 | docs/35 §2–§3；E35/resource-admission.json、cache-inventory.json | 硬证据；回收数字为上界而非已释放空间 |

本轮新增证据（docs/35）；C=`temp/archive-fix-v2-final-20261009/continue-20261009`：

| 结论与边界 | 证据 | 证据强度 |
| --- | --- | --- |
| 按新增授权只清作废解包、旧22RPM及SRPM、20,872个登记cache文件；清理后109.523376GiB，原60GiB门槛PASS。SRPM没有历史摘要，只记录实测SHA，不冒称历史核验。 | docs/35 §0.3；C/cleanup-result.json、deletion-journal.jsonl | 硬证据 |
| 相同Source/提交spec/6/6/2的唯一一次-ba --noprep成功：5381.375232s、scope峰值16.408142GiB、无内存事件。CMake PASS，实际102个Ninja任务含少量重编/重链，三个主工具未重链。 | docs/35 §1–§2；C/build-resource-summary.json、ninja-actual-tasks.json | 硬证据；增量执行，不是完整构建或性能认证 |
| 新RPM225开发档/3864成员/318543完整索引、无bitcode/DWARF、次序及重复身份PASS；45 compiler-rt/1964成员与H ELF及索引完全相同，整档仅ar时间戳变化。17,689路径非归档差异0；clang/lld/ar SHA同基线。 | docs/35 §3；C/new-archives-result.json、rpm-file-comparison.json、runtime-ar-header-differences.json、three-tools-sha.json | 硬证据 |
| 新RPM前四项PASS后，独立SSD buildroot真实-bi重新转换225档并验收PASS；对同树直接调用Source打印SKIP，270档native、225开发档SHA不变。 | docs/35 §4；C/independent-archives-result.json、independent-skip-verification.json | 硬证据；与正常-ba安装树分离 |
| 七项宿主消费者全部PASS，A/共享库/GC输出与opt相同，B两组生成物exit37；标准/bin/strip后处理和证据清理通过。 | docs/35 §3.2、§5.1；C/postprocessing-result.json、new-rpm-consumers/result.json | 硬证据；宿主混合运行库环境，不替代Tizen包内验收 |
| 唯一Tizen bfd GBS调用12.177772s后exit1，189条缺依赖，测试root未创建；固定Base repomd只读HTTP404、Unified200。内存准入24,855,044,096B、6GiB cap峰值147,640,320B、无内存事件；不是OOM或已测得的链接不兼容。 | docs/35 §5.2–§5.3；C/tizen-bfd/、failure-diagnosis/ | 硬证据（仓库与执行阶段）；Tizen兼容性未测试 |
| 未重试、未换仓库、未启动lld测试或生成v2最终format-patch；W/spec/Source、docs25–34及v1资产保护核验通过，scope/采样器/挂载/锁回收。 | docs/35 §6；C/final-outcome.json、final-integrity.json、final-process-check.json、lock-released.json | 硬证据 |

本轮闭合（docs/36）；E36=`temp/archive-fix-tizen-consumers-20261009`：

| 结论与边界 | 证据 | 证据强度 |
| --- | --- | --- |
| docs/35原22RPM及C/new-rpm-repo的SHA/大小全部匹配附录A，gbs配置不变；两历史测试根各107缓存，同NEVRA摘要相同且逐个等于原Base primary登记。复原97,776,140B的107包子集，缺失0，不切换最新快照。 | docs/36 §0–§1、附录A；E36/new-rpm-identity.json、historical-metadata-verification.json、local-base-repository.json | 硬证据；是消费者环境子集，不是全快照镜像 |
| bfd/lld各一次串行GBS成功；各安装113包=107本地Base+6本项目新包，与docs/30 NEVRA差异0；每包来源唯一且摘要校验。根内225归档+4工具SHA同N，A输出与opt O2相同，B生成物exit37。 | docs/36 §2；E36/tizen-{bfd,lld}/environment-verification.json、installed-identities.json、build.log | 硬证据；x86_64固定环境的API消费者，不外推其他架构或任意下游 |
| 两组实际链接器ld.bfd/ld.lld，driver无-flto或插件；8GiB准入/6GiB cap/swap0原规则，wall88.644845/58.435464s，scope峰6,230,188,032/5,762,170,880B，无内存事件、采样器回收。whole-archive两组exit0且记录508/507行未定义符号，仅诊断。 | docs/36 §2.3–2.4；E36/tizen-summary.json、各check-outputs/ | 硬证据（功能/资源记录）；不作性能或任意全集语义认证 |
| 无交互fetch取得tizen_base cb679968（已含x86_64 O3/ThinLTO）；单提交2d773cb6、作者FatTank、固定Change-Id，最终format-patch在干净base apply --check PASS且完整tree相同。只有两个spec插入块及Source；Source SHA6bd0546a…完全同已验输入。 | docs/36 §3；E36/target-fetch.json、submission-verification.json、submission-commands.jsonl | 硬证据；新目标整套配方未本轮重建 |
| 评审目录v2 patch SHA ddef2221db9ba1c044b0087b9fcde2a93202fdf28c518b4d0dcd1c4653119ac6；v1旧patch/Source摘要与副本保留。docs25–35、W原spec和配置不动，无LLVM重建、无Gerrit推送，项目锁/进程/挂载回收。 | docs/36 §3.2、§4；E36/v1-backup/、final-integrity.json、lock-released.json | 硬证据 |

本轮闭合（docs/37）；E37=`temp/target-recipe-policy-check-20261009`：

| 结论 | 证据 | 强度/边界 |
| --- | --- | --- |
| docs/35同一根、buildconfig和define下，target cb679968与validated f111162e的optflags相同；C/CXX/ASM flags仅新增一次已有的-Wno-unused-command-line-argument。名称不同的编译器在本根为同ELF别名，显式两项OFF同旧默认。 | docs/37 §0–§2；E37/exact-showrc.diff、*-exact-build.txt、*-cmake.json、root-showrc.stdout | 硬证据（只读参数展开）；限定本宏/工具环境 |
| 新公共flags精确替换3853条原bitcode命令中唯一对应子序列；225档全部classify_options PASS，未分类0，末项O3/DWARF4/分段/fp-contract与原策略相同；源码/补丁没有改动。 | docs/37 §3；E37/all-target-command-tokens.jsonl、policy-result.json、final-integrity.json | 硬证据（纯文本分类）；证明参数策略覆盖，不是新配方IR/转换/完整构建PASS |

历史闭合（docs/38 的 `834f9aa`）；E38=`temp/llvm-strip-x86_64-20261009`：

| 结论与边界 | 证据 | 强度 |
| --- | --- | --- |
| docs/35的22个RPM摘要/大小、N的17,689路径类型/模式/大小/SHA或链接目标均一致，额外非目录路径0。 | docs/38 §0.1/附录A；E38/rpm-identity.json、N-identity.json、N-files.json | 硬证据；仅本轮对照身份，不代替新配置产物验收 |
| 当前LLVM spec开debuginfo的宏链中，%__strip只传给brp-strip-static-archive；find-debuginfo在当前环境走elfutils的eu-strip。 | docs/38 §1；E38/all-strip-macro-references.stdout、macro-query.stdout、macro-inputs.json | 硬证据（文件与展开）；不外推到关闭debuginfo或其他包 |
| 允许清理的独立安装树位于另一文件系统；本根cache计入全部分配块回收仍仅50.816586GiB，低于60GiB。 | `834f9aa` 中 docs/38 §2；E38/resource-admission.json、cache-inventory.json、df-bytes.log | 硬证据（首次历史容量准入），已由新增清理授权解除；不是构建失败或llvm-strip功能失败 |

本轮闭合（docs/38）；下列未展开 JSON 路径均在 `E38/continue-20261009/`：

| 结论与边界 | 证据 | 强度 |
| --- | --- | --- |
| 当前开启debuginfo的LLVM包中，%__strip只被静态归档后处理实际消费；find-debuginfo仍用eu-strip。本次270档llvm-strip全部exit0，原其余brp链不变。 | docs/38 §1、§3.4；E38/continue-20261009/postprocessing-result.json、rpm-exec-exit.trace | 硬证据；限当前宏链/debuginfo配置 |
| 225开发档无bitcode/DWARF、完整索引及顺序PASS；45 compiler-rt/1964成员所有SHF_ALLOC类型/flags/大小/载荷SHA、完整索引相同，无新结构差异类别。64成员66共同节sh_entsize变化是已登记结构差异。 | docs/38 §3.1–§3.2；new-archives-result.json、runtime-archives-result.json、runtime-structure-common-sections.json | 硬证据；不要求compiler-rt全ELF字节相同 |
| 新解包对docs/35 N共17689路径，仅270个.a不同，非静态库差异0；clang/lld/ar未变。七项宿主API消费者、宿主及Tizen bfd/lld的ASan好/坏、UBSan、profile合并、128位builtins全部PASS。 | docs/38 §3.3、§4、§5；new-vs-docs35-file-comparison.json、runtime-host/result.json、tizen-{bfd,lld}/ | 硬证据；所列功能消费者，不覆盖运行库所有功能 |
| 18GiB增量构建峰值17.503872GiB，无OOM；bfd小包6GiB达到cap并回收但无OOM，lld峰值5697142784B。均正常完成，不能把bfd受限峰值当自然需求。 | docs/38 §2.2、§5；scope-after-rpm.json、outcome.json | 硬证据；资源观测，不作性能比较 |
| 后续补丁父提交67619ec8bbba已fetch核验，只加x86_64宏3行+注释1行；干净父提交apply及tree相同PASS。 | docs/38 §6；patches/llvm-strip/；submission-result.json | 硬证据；待用户提交评审，未合入 |

本轮闭合（docs/39）；E39=`temp/arm-archive-feasibility-20261009`：

| 结论与边界 | 证据 | 证据强度 |
| --- | --- | --- |
| cb679968在现有两ARM根宏下均LLVM_ENABLE_LTO=Thin；ARM32公共Os/MinSizeRel，AArch64公共Os/Release，只有x86执行强制O3的flags清理。ARM末项需以未来CMake/真实argv确认，不能继承x86认证。 | docs/39 §1；E39/*-parsed.stdout、cmake-comparison.json | 硬证据（宏展开）；最终对象flags为配置推导 |
| accel的clang/dis/nm/ar/strip均22.1.8；显式dispatcher加载/emul的x86库。ARM32/aarch64小C直接与QEMU各一次成功，两个bitcode往返成功。普通GBS chroot因ARM binfmt未注册失败。 | docs/39 §2–§3；E39/*dispatcher-loader-trace.stderr、small-experiment-summary.json、*.ll | 硬证据（局部功能）；单次wall/RSS仅诊断，不外推全量或性能 |
| ARM32 mtune=cortex-a8被当前Clang忽略，AArch64 mtune写入tune-cpu；ARM32 IR triple为thumbv7，softfp还涉及后端ABI。 | docs/39 §1.3；clang Arch/ARM.cpp:660–662、CodeGenModule.cpp:2983–2984；E39/*.ll | 硬证据（源码与小样本） |
| docs/35 strip前225档/3864成员记录仍在、SHA4d824c4f…；后续x86不变性必须逐档/逐成员对它核验。本轮没有运行全量回归。 | docs/39 §7；E39/x86-regression-anchor.json | 硬证据（基准可用性）；实现验证尚未执行 |
| 当前/home40.93GiB低于60GiB；没有找到本机对应ARM LLVM完整构建日志。公开固定快照两直接BR消费者实际走共享LLVM，不能据此断言全平台无静态消费者。 | docs/39 §5–§6；E39/capacity-now.json；docs/33 §5 | 硬证据（限定范围）；ARM完整成本UNKNOWN |

本轮闭合（docs/41）；E41=`temp/disk-inventory-20261009`：

| 结论与边界 | 证据 | 证据强度 |
| --- | --- | --- |
| /home起始可用40.931GiB；可读大目录与本项目全部一级temp证据已盘点，253个不可读子目录及shared/lost+found未知。跨扫描目录账不冒充精确释放量。 | docs/41 §1、§3、§7；E41/du-*.tsv、inventory-rows.json、completion.json | 硬证据（限可读范围/时点） |
| P28/P29合计6.646GiB，限定旧二进制候选173.887GiB；以dev/inode/nlink扣除外部硬链接，总180.533GiB。docs/30 RPM+SRPM存在外部链接，释放记0；64GiB未启用swap未计入。 | docs/41 §4；E41/binary-payload-summary.json、inactive-swap.json | 硬证据（分配块估算；未删除，未来须复核打开文件/链接） |
| Session只证明cwd/时间/标题关联，不能确证所有目录创建者；Gemini ID非唯一、早期创建Session存在缺口。 | docs/41 §2；E41/session-metadata.json、project-path-references.json | 硬证据（元数据关联）；创建者UNKNOWN不推测 |

新增硬证据（docs/42 §0–§4）：35,384个旧载荷匹配dev/inode/大小后删除；1,485个缺旧清单候选保留；四根8,780份可读日志/文本SHA保全。Chromium主仓库公共.git仍被实际存在且Git可用的analysis/05E_worktree引用，三个待删目录均保留。可用空间已满足120GiB，但不绕过清单外依赖继续B/C。

本轮闭合（docs/40 §9）；E9=`temp/arm-archive-stage1-c-newrepo-20261010`：

| 结论与边界 | 证据 | 证据强度 |
| --- | --- | --- |
| 用户新配置SHA28f1caf9…；Base20261001.092726与Unified20260814.092727的repomd均200，两架构accel clang ELF都自报22.1.8、SHA31cdc6d7… | docs/40 §9.1–§9.2；E9/repositories、accel-check/、protected-final.json | 硬证据；指定时间/快照 |
| 两架构新根极小GBS包各一次成功：运行trace加载/emul x86_64 loader/库，生成ARM/AArch64程序经qemu运行exit0；两根宏展开完整CMake argv/optflags与docs39相同 | docs/40 §9.3–§9.4；E9/c0-*/check-outputs、macro-precheck/ | 硬证据（极小包/宏展开），不替代LLVM CMake/真实归档 |
| GBS按正常初始化将mmap65536→0并注册arm/armeb/aarch64/riscv64，结束保留；没有手工注册/其他sysctl/宿主安装 | docs/40 §9.3；E9/c0-*/host-{before,after}.json、RPM脚本、host-init/ | 硬证据（所查路径与实际状态），不是宿主全量写审计 |
| GBS export exit0；代理整文件SHA断言exit1，diff只有自动VCS行；LLVM prep/configure/库构建未执行。未重试，停止原因是校验器错误，不是ARM能力失败 | docs/40 §9.5；E9/c1-export-commands.jsonl、c1-export-spec.diff、c1-export-readonly-diagnosis.json | 硬证据（停止点）；ARM认证仍UNKNOWN |

本轮新增证据（docs/40 §10）；E10=`temp/arm-archive-stage1-c1-20261010`：

| 结论 | 证据 | 强度/边界 |
| --- | --- | --- |
| E9导出spec仅多一个精确目标VCS行，删除后SHA同cb679968；tar的184,836个条目与git archive内容/类型/mode/链接目标完全一致，旧导出全部SHA匹配。 | docs/40 §10.1；E10/export-identity.json、两个tar manifest、export-files-recheck.json | 硬证据；身份检查，不是编译通过 |
| 新R10仅-bp成功，116.850637s、18GiB/swap0内峰7,616,188,416B、OOM0；宏完整argv/optflags对docs39相同。新cache123RPM保留。 | docs/40 §10.2–§10.3；E10/c1-armv7l-prep-rerun/、macro-precheck/、cache-final-inventory.json | 硬证据；未运行实际CMake/LLVM编译 |
| CMake驱动准备首次未展开宏断言失败；一次辅助修正后独立rpmspec查询exit28，按规则停止；stdout非空不豁免退出码。 | docs/40 §10.4；E10/initial-build-pre.*、build-pre.*、helper-configure-fix.diff | 硬证据（代理辅助错误）；ARM能力仍UNKNOWN |


本轮新增证据（docs/40 §11）；E11=`temp/arm-archive-standard-build-20261010`：

| 结论 | 证据 | 强度与边界 |
| --- | --- | --- |
| 标准ARM32-bc完整7147任务成功，62项Cache对docs39一致；wall1998.953884s、scope峰16465817600B、memory.events无OOM。 | docs/40 §11.1–§11.3；E11/c1-armv7l-build-rerun、armv7l-cmake-comparison.json | 硬证据；功能/容量记录，不是性能对照；未install/打包 |
| 编译实际执行/emul的x86_64 clang22；自产三个tblgen的执行捕获到qemu-arm。 | docs/40 §11.3；execution-observations.jsonl、build-phase-evidence.json、process-memory.jsonl | 硬证据；短进程采样不穷尽 |
| CMake安装规则对应210档、3690成员：3683 BC+7机器码；所有BC为thumbv7/PIC2/PIE0/末项Os，命令未分类0。 | docs/40 §11.4、§11.6；E11/armv7l-ir-census、armv7l-native-census | 硬证据；命令普查不等于整库转换/PIC/ABI认证 |
| 转换只完成2档；第3档ARMAsmPrinter.cpp.o有3处R_ARM_TLS_GD32，候选按未认证类型拒绝；无OOM/超时。ABI/lld定义为GOT-PC相对TLS路径。 | docs/40 §11.5；E11/conversion-stop-diagnosis、armv7l-conversion/summary.json；ARM.def:111、ARM.cpp:147–148、AAELF32:1974/2595 | 硬证据（停止及静态语义）；允许策略与消费者仍待PM/实测，未修改Source |
| 210构建树原归档与独立副本收尾SHA一致，123缓存RPM未变，保护文件未改；scope/采样器/挂载回收。 | E11/originals-and-copies-final.json、cache-retention-check.json、protected-final.json、final-cleanup.json | 硬证据；BUILD/cache保留，锁释放 |

本轮§12新增：最终Source1620a8da的225整档/3864有序成员/完整索引/3853后端flags与docs/35一致。证据docs/40 §12.2、E12/x86-final-regression-result.json；强度：硬证据，范围仅x86不变性。两架构TLS正负与Thumb小夹具PASS是规则测试，不能替代ARM全库和消费者。

本轮ARM32闭合：210档/3690成员、3683 bitcode转换、7原机器码保留；全属性/26缺函数属性/完整索引/重定位PASS，三套GNU ld/lld消费者、TLS动态重定位与call_once运行证据PASS。证据docs/40 §12.4–12.7、E12/armv7l-consumer-summary.json；强度：硬证据，仅当前ARM32输入与候选Source，非发布打包认证。

本轮AArch64闭合：212档/3706成员，3699 bitcode转机器码、7原机器码保留；末项O3/PIC2/tune-cortex-a53策略及完整索引/重定位PASS；三套GNU ld/lld消费者、10个TLSDESC动态重定位与call_once=6全部PASS。一次标准-bc 2321.728s、7545任务、scope峰16.417076GiB，无OOM。证据docs/40 §12.8–12.13、E12/aarch64-consumer-summary.json、final-retention.json、final-sanity.json；强度：硬证据，资源数值仅诊断，不作性能结论，不替代ARM RPM集成验收。

## 4. 人工裁决前提

本轮用户决定：只整理ARM Source与测试评审材料，单文件≤50KB，完整diff超限可外置文档附件；docs/40只加开头入口，其余不动。不改代码/spec/补丁、不运行测试/构建/转换；三家外部评审尚未执行。

下列为用户决策及其记录依据，区别于上一节的实测事实。后续 Session 不能擅自反转。

本轮磁盘裁决：只盘点、不删除/移动/压缩/改权限；Rnew/B、N、N38、H、rpms-docs35、docs35–39证据、base-local-repo强制保留。隔离旧混合根本轮仅获准目录stat/du盘点，未解除其构建/认证用途隔离。任何删除须另经用户逐项确认（docs/41）。

| 决策 | 依据与范围 | 登记位置 |
| --- | --- | --- |
| 历史基线固定工作区 spec 的 x86_64 分支，保留 -O3、ThinLTO 等自研优化，不退回安装包配方；下一实施目标按本轮用户决策改混合链接。 | 用户指定生产 accel 同源目标；后以该 spec 构建并验证。 | docs/12“定位与基线”；docs/13 §1 |
| 本机只做筛选，最终 Chromium 全量在专用服务器；不在本机构建 Chromium，不推 Gerrit。 | 本机容量有限、筛选负载不等于平台构建；供 GitHub 评审。 | docs/README；docs/12“定位与基线”；docs/20 §6 |
| debuginfo 用调用参数 `_smp_mflags -j4`，不关 debuginfo、不改优化参数、不抬完整构建 cap。 | -j40 失败与 -j4 续跑实测；等价性优先于省时间。 | docs/13 §5–§7 |
| 完整构建以实测同构指纹准入：18 GiB、4/4/1、debuginfo -j4；新集成指纹须另认证。 | 峰值加法模型已废弃；cgroup 保护机器，准入避免无证据的长时间失败，不保证永不 OOM。 | docs/14 §2；docs/20 §2.3 |
| 22 GiB 是单次有界插桩试验的临时启动政策：单线程、SwapMax=0，available<24 GiB 记录而不拒绝。 | 18 GiB 是截断峰值，随后 22 GiB 成功；不外溢到完整构建 18 GiB。未来 OBS seed 自举须单独授权/记录。 | docs/19 §4；docs/20 §2.3、§3.1 |
| PGO 因开发机容量暂缓，待服务器容量评估重估；PGO 与 BOLT 可叠加。 | 原加法模型失效，不将旧“PGO=NO”传递为永久技术结论。 | docs/19 §4；docs/20 §2.3 |
| 首版仅 BOLT clang；emit-relocs 走单 clang 重链重放，放弃全局 CMAKE_EXE_LINKER_FLAGS。 | 已有热缓存重链实测；隔离失败可降级，不波及普通全部工具链接。普通路径改动另列 `-d keeprsp`。 | docs/19 §4；docs/20 §2、§4.4 |
| 第一版不改 CLANG_VENDOR / LLVM_VERSION_SUFFIX；身份用 Release、可信哈希、节区和实际路径。 | 避免版本字符串兼容性风险；跨 patchelf 分阶段追踪哈希。 | docs/20 §1.3 |
| 用户确认 OBS→qemu-accel→Base→Quickbuild 链路及 `_use_gbs_clang=1`；解除“旧动态快照即全线停止”。 | 旧快照陈旧不改变工作区静态目标；最终验证快照仍待定，worker 调用仍须实证。 | docs/20 §1.1；docs/19 为历史调查，不再沿用其停止状态 |
| profile v2 扩为 ARM 13 + aarch64 10；优先独立 noarch RPM，无 profile 预期降级普通包。 | Quickbuild 有 aarch64 包，补训练覆盖；首版工程门槛 stale 函数比例≤5%、有效覆盖≥10%，不是性能保证。 | docs/20 §3 |
| lld/ar 的耗时/CV 只测量记录，不参与编译校准 pass/noise_floor；本轮另要求任何行 suspect 均失败。 | 现有小夹具主要测启动开销；自 `795a5c4` 起仅对之后运行生效，旧 FAIL 不追溯改判。 | docs/20 §7 |
| 按目标拆分最后校准，冻结条件后先提交推送，再经用户“开始”启动；无论结果不再本机重试。 | 将 69 组合的最大偏差拆为两个集合，逐行判据仍编译差≤3%、CV≤3%、无保留 suspect，决策规则由联合改各自判定；启动 load1≤3。 | `ea7d120` 预注册；docs/20 §7.1；结果 `80bc93a` |
| Quickbuild 固定 A/A一对+A/B三对；LLVM A/B各构建一次，八轮指Chromium。 | 全指标preflight；任一时间/CPU A/A d>0.10中止，最终d取A/A与A间漂移最大值；冻结δ与dead_zone，资源噪声同样阻止发货。δ、容差及协议由内部团队冻结；本设计不再给默认数值。 | docs/21 §6；`tools/test_final_bolt_calibration.py` |
| 混合链接、保留llvm-static-devel；第一版只BOLT clang（本轮不做BOLT）。 | clang/clang++、ar家族、lld家族静态，其余共享；常规非devel包零LLVM.a，compiler-rt/libarcher不动。附录A获准本机试构建。 | 本轮用户决策；docs/21 §0、附录 A |
| 历史接受的容差记录；当前Quickbuild参数转内部团队负责定稿。 | 保留2d≤tol、每对≤1+tol且GM≤1结构；不再将历史2%/3%/5%写成执行默认值。未冻结占位拒绝。 | 本轮用户决策；docs/21 §6.3 |
| 本机只做功能/稳定性，不再性能校准；armv7l筛选层无合格认证。 | 保留docs/16一次训练正式PASS，不能替代留出/最终确认；本轮在批准分支执行一次混合构建与30TU正确性、原始RPM及归档副本检查。 | 本轮用户决策；docs/21 §5、§7 |
| compile-only-v3只约束未来记录：lld/ar时间/CV不入门禁，任意行retained suspect均FAIL。 | 增加摘要/全集/样本/summary完整性验证；冻结旧计划和启动器，历史JSON不重判。 | 本轮用户要求；docs/21 §7 |
| 对外仅定性；内部数字标分母、是否含重链剥离、训练/留出、正式/诊断和门禁状态。 | 避免把耗时降低写成等幅吞吐提升，避免跨轮漂移和失败校准混入收益认证。 | docs/19 §4；docs/20 §5、§7.1.4 |
| 用户四项决定（本修订） | ①static-devel/运行库保留、常规包零LLVM.a；②批准hybrid-link-trial本机一次正确性构建，失败不改补丁重试；③Quickbuild协议及数值交内部团队；④docs/21修订交三家评审。 | 本轮用户指令；docs/21 §0/§4/§6，V37–V40 |
| seed与chroot修订 | 非seed RPM解包逐文件SHA/属性相同，SOURCE_DATE_EPOCH固定，不比RPM头；活性脚本允许显式host-arch并核ELF Machine。 | docs/21 §1.3/§3.1 |
| 本轮单会话独占、逐项完整性不符即停，不修复；docs/23保留，外来会话证据仅作线索。 | 用户新任务第零步；两项共享资产不匹配触发全局停止，第二/三部分的独立性不能绕过第零步。外来未提交STATUS先备份，本文件从已提交dab197c及本会话证据更新。 | docs/24 §0–§6 |
| 归档修复优先于BOLT，设计v4暂缓；改用工作区全静态spec新根一次完整构建，隔离旧混合根不读写。 | 本轮用户决策；只有独立archive-fix-trial允许修法，保留4/4/1，18GiB/swap0/debuginfo4。身份不符即停，不自行用改后图放行。 | docs/25 §0–§5 |
| 撤销旧构建树SHA作为本次归档修复基准；只用docs/13的22 RPM新解包。R0仅RPMS和usr/lib/rpm允许读取。运行库compiler-rt或libarcher含bitcode/其他即停，不自行扩大修法。 | 用户第二次执行更正；docs/15重新configure是已登记合法变更。22 RPM已核验，实际因libarcher bitcode停止；设计v4/BOLT继续暂缓。 | docs/26 §0–§5 |
| GNU ld不开LTO、不带插件的兼容性是硬要求。弃用“改宏+选择性strip”；改为归档bitcode→机器码，含libarcher，compiler-rt不转换，工具构建/链接及RPM后处理不改。 | 用户本轮方案变更；libarcher范围已批准，不再作为待决问题。离线第一段任一失败即停，不进入第二段、不重试。 | docs/27 §0、§4、§6 |
| docs/27转换结果作废，补齐原编译的后端选项后全部重新转换；消费者编译/链接分开，A升级为PassBuilder O2对照、B实际库内链接、增加GC/共享库加载与Tizen包内验证。 | 用户本轮决定；只在全部离线门禁通过后才允许x86_64 spec转换与一次完整LLVM构建、两次测试包构建。4GiB AS下B-lld失败已触发停止；不改限额或参数重试。 | docs/28 §0–§7 |
| 编译保留4GiB AS；链接不设AS、由cgroup与swap=0约束。明确授权原B-lld单次诊断，核SHA后复用docs/28新归档，先模拟Tizen strip与全部消费者，通过后才做隔离spec及一次完整构建。 | 用户本轮事前更正规则：lld映射输入，虚拟空间不是RSS；诊断支持该判断。完整构建16GiB可用门槛与18GiB cap不变；准入失败后不自动等待或重试。 | docs/29 §1–§2、§6 |
| 先从旧日志/固定元数据预检构建根环境；缺失依赖改Source，不给LLVM spec新增BuildRequires；五代表归档须逐成员SHA相同后才准入完整构建。 | 用户docs/30任务；GNU time缺失已按授权移除，改用wait4，构建根实际执行PASS。 | docs/30 §1 |
| 预授权内存等待：可用≥16GiB，低于时每300秒读取、最长6小时；满足才启动，每次LLVM/测试包构建仍仅一次，失败不改后重试。 | 用户事前授权，覆盖docs/29“准入失败即停、不等待”的本轮行为；不终止他人进程、不降门槛。三次构建均立即满足，等待分支有正负测试。 | docs/30 §2/§4；memory-admission.jsonl、tools/test_build_memory_wait.py |
| 提交版以工作区 LLVM 分支 HEAD 为基准，排除三处本机并发设置，Source 必须与docs/30逐字节相同；只向GitHub发布补丁，不应用W、不推Gerrit、不重构建。 | 用户docs/31任务；生成单提交、英文问题/修法/范围/验证说明；与实测输入除6/6/2和4/4/1外完全相同。 | docs/31 §1–§3 |

| v2采用用户A–M合并评审：原命令白名单/末项政策、类型与符号断言、原子回写、600s取消、LLVM22版本闸门、Python3.9、显式工具路径与清理。 | spec在隔离S中改；W不动；Source1005移出ifarch、x86_64显式依赖util-linux；转换仍4 workers/4GiB AS，标准brp不变。具体评审来自三家中的哪一家未提供，不编造归属。 | docs/32 §1–§2 |
| v2首次本机完整构建保留HEAD的6/6/2，18GiB/swap0/debuginfo4；失败不自行回退。 | 用户本轮明确授权；前提是离线全部通过且独占。本轮他人Ninja在10:39启动，10:52发现后停止自己的实验，完整构建尚未消耗。 | docs/32 §0.1、§4 |

| HQ方案只做事实调查 | 用docs/30构建树完整索引BC副本、R0的llvm-strip实测；模拟RPM只换static-devel，最多两个测试包+三个真实消费者的HQ/转换对照；不构建LLVM、不改W/spec、不推Gerrit。不替用户决定采用哪种方案。 | 本轮用户指令；docs/33 |
| 小测试包资源规则与完整LLVM分开 | 用户在首次测试包GBS启动前改为MemAvailable≥8 GiB、cap6 GiB、swap0，逐包串行，宿主低于2 GiB中止；完整LLVM仍16 GiB准入/18 GiB cap。此前16 GiB等待69次均未启动；不改旧记录、不属于失败后放宽重试。 | docs/33 §0、§3、附录；E33/resource-policy-change.json、tizen-bfd-wait16GiB/memory-admission.jsonl |

本轮追加裁决（docs/34）：

| 决策 | 依据与范围 | 登记位置 |
| --- | --- | --- |
| 独占仅本项目，允许其他项目构建并存；耗时不作性能结论。 | 完整构建可用≥16GiB、每300秒最多等6小时仅为准入；运行中可用<2GiB才中止，18GiB/swap0不改；未授权人为链接时限。 | 用户通宵任务；docs/34 §0、§3 |
| hidden负例作废，改真实删除强符号；续跑拆成真实安装与同树Source SKIP两步。 | 用户已裁决，不再等待答复；真实删除及600秒复验本轮已完成。 | docs/34 §2 |
| HQ __strip=llvm-strip只叠加试验，不包含在归档修复提交中。 | 提交仍是ThinLTO归档转换修复；GNU/LLVM strip差异须实测，不能默认为只有容器变化。 | docs/34 §0.2、§1 |
| Gerrit候选以可取得的tizen_base引用为基准，未启用ThinLTO时为SKIP。 | 本地origin/tizen_base=2d23367d已取得；作者FatTank、固定Change-Id，用户自行上传；完整验收成功前不覆盖v1。 | docs/34 §0.1、§5 |
| 2026-09-30节前暂停，节后由用户明确恢复。 | 用户“我要下班了，能帮我暂停下么，节后继续”覆盖此前无人值守继续规则；按可能关机保存磁盘现场并释放内存，不将主动停止记为构建FAIL。恢复前核验对象/cache及不会清空BUILD的增量入口。 | docs/34 §3.2；temp/archive-fix-v2-build-20260929/pause-20260930-1919/ |
| 2026-10-08恢复同一暂停构建。 | 用户“继续吧，结束后记得报告一起发出来”；先核验再正常-ba --noprep增量执行，不重做%prep、不改变并发或cap。 | docs/34 §3.3；E34/resume-20261008/ |


本轮用户决定（docs/35）：恢复标准GNU strip提交配置；仍要求compiler-rt成员ELF与docs/13逐字节一致。
授权原根一次正常-ba --noprep、两测试包和一次独立-bi；不重新完整构建；离线PASS沿用docs/34最终Source证据。
新增清理授权仅三类：作废解包、经登记核对的旧22RPM及SRPM、本根登记的剩余llvmcache文件；仍须清理后满足60GiB，否则停止，不能再删其他资产。
独立-bi及同树SKIP须在新RPM第1–4项通过后执行，不覆盖正常-ba安装树；本轮已按此顺序完成。
完整构建/续跑18GiB、6/6/2、debuginfo4及小包8GiB准入/6GiB cap均不变；任一步失败即停，不改后重试。
最终提交以tizen_base为基准，未启用ThinLTO时SKIP、超认证选项策略则失败；完整验收前不覆盖v1。
依据：用户docs/35主任务及清理补充；docs/35 §0、§2、§4、§6。SSD独立存储是代理实施选择，不冒称用户新增政策。

本轮追加人工决定（docs/36）：允许从docs/30测试根缓存复原同Base环境；精确排除本项目Release=1包，缺项先查同NVR Unified，仍不足才可临时加最新Base且不改gbs配置。本轮107包齐备，备用分支未触发。只授权bfd/lld两小包各一次，8GiB准入/6GiB cap/串行；通过后刷新tizen_base并生成供用户上传的补丁，不重建LLVM、不推Gerrit。原docs/35的STOP规则不再阻止这次新授权；原历史记录仍不修改。依据：本次用户任务、docs/36 §0–§3。

本轮人工任务范围（docs/37）：只读核查cb679968在docs/35同一宏环境的编译参数；有差异仅调用既有分类函数。不能借此修改Source/补丁或启动构建，失败只报告。本轮分类通过，未扩大到新配方完整构建。依据：用户本次任务、docs/37 §0及§4。

本轮人工决定（docs/38）：仅LLVM包、仅x86_64改用llvm-strip，作为356627 PS2之后的独立change；compiler-rt门禁为全部SHF_ALLOC指定字段/载荷及完整索引一致，允许docs/34已登记结构差异，并以宿主/Tizen sanitizer、profile、builtins补功能证据。原834f9aa磁盘STOP保持历史有效。用户补充授权：先rename保全docs/35原22RPM+SRPM，再按三类顺序仅清理/home载荷，达到75GiB立即停止；保留指定资产及日志/JSON/脚本。本次只执行第一类、未删除第2/3类，原60GiB启动门槛不变。非静态库对照仍为N；补丁叠在实际fetch核验的PS2上；构建/验收失败即停不重试，不推Gerrit。依据：用户主任务与清理补充；docs/38 §0、§2–§6。

本轮人工决定（docs/39）：仅调查与不超过30分钟小实验，不构建LLVM、不改spec/Source/补丁。用户确认356627与356639已上传；ARM若认证通过，转换扩展作为356627新patchset（原Change-Id不变），strip扩展作为356639新patchset并rebase在新的356627上；不新开review，x86已验证行为不变。依据：本轮用户任务；docs/39 §7–§9。

本轮夜间人工规则（2026-10-10）：用户授权A指定清理→B x86全量SHA回归→C两ARM静态库第一段；规定之外停止，失败停止全部后续，每阶段/停止均提交推送；A2 Git报错可保留可得备份后删除，但未授权处理保留路径的共享Git依赖。A3四根仅生成sudo脚本；A1逐文件须匹配docs/41。最终停在A2依赖，不重新要求夜间确认。

前次用户裁决（已由下一条更新初始化范围）：仅执行B/C；清理与Chromium不在范围，也不再阻塞本任务。四个待用户sudo删除的旧根不读写。B失败不进C，ARM32失败不进AArch64；禁止宿主binfmt/sysctl/包变更，规定之外停止报告。

前次人工裁决（docs/40 §8）：允许正常 GBS/init_buildsystem/initvm 注册 qemu binfmt，以及临时写宿主 vm.mmap_min_addr=0；不手工注册、不改其他配置/脚本/宿主包。结束不替用户恢复，报告提供原值恢复命令。固定 ARM 配置的 Base/Unified 不可用即停止，不自行换源；未知真实 ARM relocation（如 TARGET2）只列证据/建议后停交 PM。候选 Source 只有 C2 实证才能定稿，任何改动必须重跑全部测试与 225档/3864成员 x86回归。此次固定Base404，未触发任何宿主写入或Source修改。

本次人工裁决（docs/40 §9）：仅使用用户更新的W/gbs_llvm.conf，接受开场新SHA28f1caf9…为基准；不修改/自行换源，每源repomd须200，accel LLVM主版本须22。GBS标准binfmt/mmap初始化仍获准，结束不代恢复；所有GBS缓存保留。C1只构建指定静态库、不执行LLVM install/打包，新宏影响编译参数或未知重定位须停；任一步失败不重试。本轮C0通过后因代理导出身份检查错误停止，未把本轮错误写成用户新增门禁。

本轮人工裁决（docs/40 §10）：导出身份取代整spec SHA断言——唯一VCS行须指向cb679968，去掉后原spec逐字节相同，tar内容同git archive，满足即复用E9不重导出。辅助脚本缺陷可在只读证明门禁不放宽后修正并重跑该步骤一次，同一步骤再次失败即停止；产品失败无此例外。本轮缓存准备、prep参数修正后PASS，CMake驱动准备第二次失败后不再尝试。仅W配置SHA28f1caf9…，候选Source变更仍须全测试/x86回归，宿主初始化授权与缓存保留不变。


本轮人工裁决（docs/40 §11）：取消手写%build/CMake驱动；允许标准build后端--stage=-bc执行原样完整%prep/%build，复用R10 --noinit，6/6/2与18GiB/swap0/16GiB准入不变。两架构BUILD与cache都保留，不install/打包、不清磁盘。辅助门禁同inode别名错误获一次修正重跑（未改实质配置门禁）；实际未知重定位仍按既有规则停止交PM，不以该例外自动扩大Source认证。宿主mmap0/已有binfmt保持，恢复命令保留。

本轮用户裁决（§12）：ARM32补回-mthumb；TLS GD/LD及AArch64描述符明确放行，LE任何节禁止，IE/ARM32描述符/其他未知仍交PM；每次Source改动重跑全部测试与x86全量回归。复用B10，不重建ARM32；AArch64只在ARM32全部通过后执行一次-bc；不清理。

历史首轮PM裁决（docs/44 §3）：A64任意module asm拒绝，曾导致普查后停止。
续接PM已将其替换为两架构精确白名单`.globl _ZSt21ios_base_library_initv`且须保留输出GLOBAL符号；其余未知声明仍失败。辅助修正仅一次，本轮用于测试期望遗漏-g；第二次宿主套件再次失败后停止，不改共用取消代码或继续复验。生产Source与两patch不改。

## 5. 挂账

- 历史清理挂账：analysis/05E_worktree共享Git元数据尚需处理；用户已解除它对B/C的阻塞，清理不在当前范围；三个Chromium目录未删，第三个小文本备份PARTIAL。四旧根日志已保全，temp/deleted-roots-logs/sudo-delete.sh留用户自行执行，本代理未运行。A1第6–8组1,485候选缺旧逐文件记录，仍保留；其他项目/swap无清理授权。

| 分类 | 未闭合项 | 所需材料/下一步与验收边界 | 依据 |
| --- | --- | --- | --- |
| 待用户提供 | OBS 项目、工作区自研 spec 的实际来源、最终验证 Base 快照 | 明确 source/spec/patch/MLGO 身份，之后钉元数据与 RPM；现公开旧快照不能冒充静态 BOLT 验证快照。 | docs/20 §1.1、§8 |
| 待用户提供 | Quickbuild 全平台日志 | 统计实际链接+归档占比；>10% 启动第二阶段真实链接基准/lld profile/BOLT lld/逐字节门禁；<5% 搁置；5%–10%（含边界）默认搁置。占比用链接/归档边累计时间除全部边累计时间，与总wall另列；不以Chromium 0.2%或小夹具代替。 | docs/21 §8 |
| 待用户提供 | qemu-accel 完整源码、armv7l 生成 spec、baselibs_body、对应 OBS 宏与构建日志 | 已取 SRPM 仅含 aarch64 spec；原 VCS `e01aa7250a1a73aa8f88ba9ac4a05cbc954d1c9f` 的公共获取受凭据/403/TLS 阻碍。补齐分支和隐式后处理，不能把通用主体当完整 armv7l 执行日志。 | docs/19 §2.1–2.2；docs/20 §1.2 |
| 待外部复审 | 356627 PS2与356639 PS1 | 已交付docs/45固定版本材料；上传身份与本地封套区别、生产Source/spec、证据边界齐备。材料准备不是评审通过，代理未推Gerrit。 | docs/45 §1–§6 |
| 待处置/复验 | ARM候选5608aa5e与测试 | module asm旧冲突已解除；新套件第二次95项中既有取消测试FAIL，根因未明。ARM根测试/x86与两ARM全量/105–106/x86符号只读核查未执行，不把1620历史PASS当成新候选认证。 | docs/44 §7–§12；E2/stop-result.json |
| 待评审 | docs/21完整v3与V01–V36落实、七文件混合提案、脚本/strip实验 | docs/20保持历史原文；已采纳/实现不等于评审通过，不再安排本机校准。 | docs/21附录D/E |
| 待评审/修订 | 五个额外静态工具未符合混合范围 | llvm-config、llvm-exegesis与三tblgen实测仍静态；修订方案或由用户确认明确例外，不能自动豁免/重建。保留static-devel及runtime。 | docs/22 §5.1；docs/21 §0.1 |
| 后续待验 | 混合profile rebind、seed与accel试包 | 本机容量/混合RPM别名/活性/30TU已实测；docs/23在打包失败后未启动profile适用性实证；docs/24再因完整性门禁失败而未执行，保持未认证、不能据此要求重训；尚待图提取器认证或适用性测试后决定重训、同job seed解包文件级等价、seed热缓存两模式、accel patchelf/alias/后处理链验证。 | docs/22 §4–§6；docs/21 §1–§4 |
| 待内部团队定稿 | Quickbuild协议/δ/容差 | 本文仅结构与占位，内部团队在入队前冻结；dead_zone保留，不再提供δ建议值。 | docs/21 §6 |
| 待评审/实施 | spec 集成补丁、profile 包、自举/重认证、状态文件、隔离降级、debuginfo 策略 | 生产BOLT集成仍为设计；只在本机hybrid-link-trial分支应用获批混合补丁，原spec未改。5% stale/10% coverage 为工程政策；新集成容量指纹独立登记，执行 §4.4 负对照；先在目标executor验证子cgroup委派。 | docs/21 §2–§4 |
| 待试包/Quickbuild | 从 RPM 到 accel 到 worker 的最终身份和正确性 | 分别记录 OBS ELF/accel ELF/worker 哈希，跨 patchelf 不强求 SHA 相同；检查节区/别名/brp 后结果，worker `/emul/usr/bin/clang-22` 必查；ninja commands 和首次编译后非计时 exec trace 留证；最终产物再做 TU 门禁。 | docs/20 §1.2–§1.3、§4.2、§6.1 |
| 待 Quickbuild | BOLT 实际收益、v2 对 v1 增量、ARM 非退化与筛选方向是否一致 | 按docs/21八轮公式先冻结参数并通过preflight；同资源/输入图/缓存，取完整 wall、单位编译成本、cpu.stat、memory.peak 与下游运行资源；实际 job/tee/后台状态非零立即停止。旧本机数据不作服务器 A 组。 | docs/21 §6；docs/20 §7.1.4 |
| 待发货/其他流水线验收 | 混合/OBS/其他架构的静态库与后处理 | docs/30已经闭合工作区全静态x86_64新RPM的机器码/索引、运行库、后处理、文件差异与Tizen消费者；不能直接替代未来混合配方、OBS输出或ARM/AArch64。旧改宏方案作废，后续保持原brp并按各自输入重新认证。 | docs/30 §3–§5；docs/21 §4；docs/28 §5 |
| 待需求/实验 | BOLT clang 源码级 debuginfo | 首版 stripped-evaluation 不能假配旧 DWARF；如生产要求完整崩溃分析，须另测 update-debug 的容量/时间、最终符号化与 debuglink/build-id。当前成本 UNKNOWN。 | docs/21 §4.3 |
| 待服务器容量评估 | PGO、其他工具 BOLT 与生产新输入 profile | 取得worker实际内存/并发/cgroup后重估PGO；现v2不自动认证混合输入，source/spec/patch/MLGO改变触发图与profile重认证；不擅自新建profile或重写。 | docs/21 §3、§8 |
| 待裁决/补证据 | HQ方案的Tizen B-lld完整运行与实际平台覆盖 | 本轮6GiB约122分钟链接未完成、代理诊断性中止；不擅自提高cap/重试。A已通过，不替代B或完整%check。公开快照源primary只覆盖显式直接依赖；两个直接BR包实际共享，未找到满足真实包失败对照触发条件的对象，未构建真实消费者包。 | docs/33 §3、§5、§7 |
| 评审中/待目标流水线 | 归档修复v2与356627 PS2 | docs/35+36门禁闭合；docs/38已fetch核验PS2提交67619ec8bbba及父cb679968。docs/37确认同宏环境参数策略覆盖；目标配方仍需流水线正常构建，新选项须重新核查。 | docs/36 §3–§4；docs/37 §4；docs/38 §6 |
| 评审中/待目标流水线 | 356639：x86_64 LLVM包切换llvm-strip | 用户已确认上传、依赖356627；本机要求PASS，目标流水线另验。ARM条件需在转换认证后更新同change并rebase，不能借x86 PASS直接扩大范围。 | docs/38 §3–§6；docs/39 §8–§9；用户本轮确认 |
| 已闭合（保留记录） | 修正后的续跑验收 | 新RPM第1–4项PASS后独立buildroot真实-bi重新转换225档并验收，通过后对同树Source SKIP，225档SHA不变；这两项不再挂账。 | docs/35 §4；C/independent-archives-result.json、independent-skip-verification.json |
| 已闭合第一段；后续待实施 | ARM/AArch64转换与打包集成 | §12最终x86不变性、两ARM全库/重定位/三套消费者/strip均PASS；需另任务实施spec/Source集成与ARM RPM验收，再更新356627/356639的patchset。生产补丁未改，未知类型仍停止。 | docs/40 §12；docs/39 §4、§7 |
| 已隔离/暂缓 | 旧混合构建根与profile适用性；设计v4 | docs/24旧根不再读写；外来docs/23与重链脚本改动在备份SHA匹配后已按新授权恢复HEAD，不再是脏工作树。设计v4及BOLT后续等归档任务完成。 | docs/24；docs/25 §0 |

已关闭、不再作为待办：本机校准重试、用新门禁回判历史 FAIL、为补漂亮数字追加轮次。
历史混合试构建/根因/隔离记录保留，docs/25、docs/26不改；旧图SHA门禁与libarcher范围待决已由用户更正/解除。
docs/30的v1完整构建及全部新RPM/Tizen验收、docs/31的干净HEAD提交补丁保留；docs/25–31不改。
当前tools/llvm_static_archives_source.py与patches/archive-index-fix/中的v2 Source同SHA6bd0546a…；提交patch已更新为ddef2221…。v1保留在Git历史及E36/v1-backup，不能混用两个版本身份。
原宏关闭方案继续作废；转换只在x86_64安装根进行，W/llvm/spec不动；代理未推Gerrit，用户已确认上传356627 PS2。
归档修复v2提交材料及两Tizen包验收已在docs/36完成；固定Base缓存复原解除此消费者环境的依赖阻塞，不代表远端404消失。docs/37已闭合相同环境下编译参数策略覆盖；当前归档修复评审中，待目标流水线完整验证；x86 llvm-strip已完成并由用户上传356639。docs/39 ARM可行性调查已完成，实施与完整试包待PM决定；不自动构建新配方或上传Gerrit。设计v4/BOLT没有自动启动授权。

前次执行备案（e44fb63，初始化政策随后已解除）：用户明确清理任务不再阻塞B/C，四个待sudo删除旧根不读写；B已PASS；C0在GBS启动前停止，证据`temp/arm-archive-stage1-20261010`。x86不变性为硬证据，ARM能力仍未认证。无磁盘清理/宿主配置修改/补丁更新/Gerrit推送。

当前挂账（docs/40 §12）：第一段已全部PASS（x86不变性、ARM32 Thumb/TLS及两ARM全量转换/消费者/两种strip）；需后续ARM spec集成与RPM验证。生产Source/两个review补丁仍未改，不等于ARM打包验证已完成。两套BUILD和各123缓存RPM保留供后续增量使用。

本轮人工裁决（docs/44续二）：取消诊断通过才修测试；ABS/COMMON无真实节，其余保留索引拒绝，XINDEX逻辑不变；全套测试后才做x86/两ARM复验，任一停止仍完成文档。
