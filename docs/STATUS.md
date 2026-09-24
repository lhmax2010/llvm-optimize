# LLVM 吞吐优化分支状态

更新日期：2026-09-24。分支：`main`；仓库：`lhmax2010/llvm-optimize`。
历史状态核对到 `ae6d938`；完整设计以 [docs/21](21_spec_integration_v3.md) 为准，混合构建见 [docs/22](22_hybrid_link_trial.md)，
归档根因与前次失败记录见 [docs/23](23_archive_fix_and_profile_rebind.md)；
旧混合根核查停止记录见 [docs/24](24_archive_fix_verification.md)，该根已隔离，不再读写。
docs/25保留前次停止记录；用户已更正旧构建图门禁，改用docs/13的22 RPM作唯一基线。
docs/26 的 libarcher 范围停止已由用户新方案解除：全部 bitcode 归档（含 libarcher）转机器码，旧改宏方案作废。
docs/27 转换遗漏后端分段选项，旧产物本轮作废、不复用。补齐后的重新转换通过；消费者 A 两组、B 的 GNU ld 组通过，B 的 lld 组分配失败后停止，见 [docs/28](28_static_archive_native_conversion_v2.md)。
docs/21 取代 docs/20 的后续实施方案；历史报告、校准判定和预注册文件保持原样。
以下 `temp/` 均相对工作区 `/home/linhao/Toolchain/development/llvm-optimize`，仅保存在本机，不在 GitHub。

## 1. 计划

总目标：降低 Tizen 全平台 RPM 包构建总耗时，优化对象覆盖实际调用的 LLVM 工具。
**当前第一任务：静态库 bitcode 转机器码，使 GNU ld 无 LTO/无插件也能消费；离线验证通过后才进工作区全静态 spec 的隔离试验与一次完整构建。设计 v4 与 BOLT 暂缓。**
本轮22 RPM与17,689个解包路径复核通过；真实TU选项对照通过，补齐后端选项重新转换225归档/3,853 bitcode，11原ELF不变、318,543索引条目完整，10成员分段抽查通过。
编译/链接拆开后A的bfd/lld输出与基线opt O2一致，B的bfd组库内链接成功、生成物exit=37；B的lld组在4GiB AS下分配失败，无cgroup OOM。按失败即停；共享库/GC/反例未执行，未改spec/宏/认证入口，LLVM及Tizen测试包构建均0次。
后续混合目标保留：原生 x86_64 clang/clang++、llvm-ar、lld/ld.lld 静态链接 LLVM 库，
其他工具走共享库路径；别名继承实体形态，上游强制静态例外待审。仅 clang 做首版 BOLT，生成 ARM/AArch64 代码。
基线是工作区 LLVM `f111162e94aa48ed367c9d2c039456c70e7160ae` 的自研 spec，
不是旧公开快照配方。本机筛选不能替代专用服务器 Chromium 全量及全平台验收。
依据：docs/13 §1；docs/21 §0、§1、§4、§6。历史全静态 RPM 仍作为已有基线证据；混合版本一次构建成功且30 TU通过，但额外静态工具及归档索引尚有BLOCKER。

| 阶段 | 范围 | 当前状态 |
| --- | --- | --- |
| 摸底与基准台 | 配方、工具调用面、身份、资源限制、可重复测量 | 完成；历史报告保留各自证据边界 |
| 静态 RPM 基线 | 固定快照、构建、debuginfo 续跑、工具验证、基线数据 | 已完成；static-devel保留，既有归档索引缺陷须通过修复与消费者验收 |
| BOLT 筛选 | 容量、插桩/profile、重写、正确性、训练/留出、中间对照、双目标 | 本机工作已结束；最终 ARM 校准 FAIL，AArch64 PASS 并完成正式轮 |
| 静态库兼容性修复 | bitcode→机器码、保持原brp宏、GNU ld无LTO/插件消费者、一次完整构建与新RPM验收 | **当前第一任务；docs/28补选项后转换PASS，A两组/B-bfd PASS，B-lld分配FAIL；后续消费者及spec/RPM验收未执行** |
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
| 2026-09-24 | 本提交（`git log -1 -- docs/28_static_archive_native_conversion_v2.md`定位） | docs/28、STATUS、转换/对照/消费者脚本及测试 | 后端选项补齐，225归档重新转换782.346s、索引/分段PASS；A-bfd/A-lld/B-bfd运行通过，B-lld在4GiB AS下分配失败后停，无cgroup OOM，完整构建0次。 |

本文件建立提交：`git log --diff-filter=A --format='%h %ad %s' --date=iso-strict -- docs/STATUS.md`。
上述历史主报告可能后续原地更新，核查当时结论使用 `git show <提交号>:<文件路径>`。

## 3. 已闭合结论

证据强度约定：**硬证据**＝源码/元数据/原始命令/逐字节检查等直接事实；
**通过校准**＝相应测量对满足当时协议，不自动代表服务器验收；
**诊断**＝未通过门禁或未做正式验收的数据，只能描述观测，不能作认证收益。
“闭合”仅限表中命题和输入范围；不是所有未知问题都已解决。

| 结论与边界 | 证据 | 强度 |
| --- | --- | --- |
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

对外统一口径：**筛选层多轮测量方向一致，BOLT 对 LLVM 自身源码编译负载有稳定正向影响，量级待构建服务器验收。**
不对外给收益百分比，不称“五轮独立”，不将训练集结果或诊断比值当作留出泛化认证。

## 4. 人工裁决前提

下列为用户决策及其记录依据，区别于上一节的实测事实。后续 Session 不能擅自反转。

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

## 5. 挂账

| 分类 | 未闭合项 | 所需材料/下一步与验收边界 | 依据 |
| --- | --- | --- | --- |
| 待用户提供 | OBS 项目、工作区自研 spec 的实际来源、最终验证 Base 快照 | 明确 source/spec/patch/MLGO 身份，之后钉元数据与 RPM；现公开旧快照不能冒充静态 BOLT 验证快照。 | docs/20 §1.1、§8 |
| 待用户提供 | Quickbuild 全平台日志 | 统计实际链接+归档占比；>10% 启动第二阶段真实链接基准/lld profile/BOLT lld/逐字节门禁；<5% 搁置；5%–10%（含边界）默认搁置。占比用链接/归档边累计时间除全部边累计时间，与总wall另列；不以Chromium 0.2%或小夹具代替。 | docs/21 §8 |
| 待用户提供 | qemu-accel 完整源码、armv7l 生成 spec、baselibs_body、对应 OBS 宏与构建日志 | 已取 SRPM 仅含 aarch64 spec；原 VCS `e01aa7250a1a73aa8f88ba9ac4a05cbc954d1c9f` 的公共获取受凭据/403/TLS 阻碍。补齐分支和隐式后处理，不能把通用主体当完整 armv7l 执行日志。 | docs/19 §2.1–2.2；docs/20 §1.2 |
| 待评审 | docs/21完整v3与V01–V36落实、七文件混合提案、脚本/strip实验 | docs/20保持历史原文；已采纳/实现不等于评审通过，不再安排本机校准。 | docs/21附录D/E |
| 待评审/修订 | 五个额外静态工具未符合混合范围 | llvm-config、llvm-exegesis与三tblgen实测仍静态；修订方案或由用户确认明确例外，不能自动豁免/重建。保留static-devel及runtime。 | docs/22 §5.1；docs/21 §0.1 |
| 后续待验 | 混合profile rebind、seed与accel试包 | 本机容量/混合RPM别名/活性/30TU已实测；docs/23在打包失败后未启动profile适用性实证；docs/24再因完整性门禁失败而未执行，保持未认证、不能据此要求重训；尚待图提取器认证或适用性测试后决定重训、同job seed解包文件级等价、seed热缓存两模式、accel patchelf/alias/后处理链验证。 | docs/22 §4–§6；docs/21 §1–§4 |
| 待内部团队定稿 | Quickbuild协议/δ/容差 | 本文仅结构与占位，内部团队在入队前冻结；dead_zone保留，不再提供δ建议值。 | docs/21 §6 |
| 待评审/实施 | spec 集成补丁、profile 包、自举/重认证、状态文件、隔离降级、debuginfo 策略 | 生产BOLT集成仍为设计；只在本机hybrid-link-trial分支应用获批混合补丁，原spec未改。5% stale/10% coverage 为工程政策；新集成容量指纹独立登记，执行 §4.4 负对照；先在目标executor验证子cgroup委派。 | docs/21 §2–§4 |
| 待试包/Quickbuild | 从 RPM 到 accel 到 worker 的最终身份和正确性 | 分别记录 OBS ELF/accel ELF/worker 哈希，跨 patchelf 不强求 SHA 相同；检查节区/别名/brp 后结果，worker `/emul/usr/bin/clang-22` 必查；ninja commands 和首次编译后非计时 exec trace 留证；最终产物再做 TU 门禁。 | docs/20 §1.2–§1.3、§4.2、§6.1 |
| 待 Quickbuild | BOLT 实际收益、v2 对 v1 增量、ARM 非退化与筛选方向是否一致 | 按docs/21八轮公式先冻结参数并通过preflight；同资源/输入图/缓存，取完整 wall、单位编译成本、cpu.stat、memory.peak 与下游运行资源；实际 job/tee/后台状态非零立即停止。旧本机数据不作服务器 A 组。 | docs/21 §6；docs/20 §7.1.4 |
| 待发货验收 | 静态开发包索引与后处理活性 | 常规包零LLVM.a，static-devel全归档armap与构建树完整对照、bfd/lld组件消费者及坏liblldCOFF.a负例；runtime保持。docs/22为223空/3残缺；docs/23已复现GNU strip根因，提出spec局部去掉归档strip。唯一重打包因试验入口错误失败，226完整映射/22包非.a等价/消费者负例均未验；docs/24全局前置失败未普查；docs/25的旧图门禁已由用户更正；docs/26完成RPM普查；docs/27按用户新方案离线转机器码成功（含libarcher），旧改宏方案作废。docs/27产物因后端选项不全已作废；docs/28补齐后新转换通过，A两组和B-bfd通过，B-lld分配失败，spec、完整构建、新包strip后索引与剩余消费者仍未验。每层后处理活性必过。 | docs/13 §12；docs/22 §5.2；docs/23 §1；docs/21 §4、附录 C |
| 待需求/实验 | BOLT clang 源码级 debuginfo | 首版 stripped-evaluation 不能假配旧 DWARF；如生产要求完整崩溃分析，须另测 update-debug 的容量/时间、最终符号化与 debuglink/build-id。当前成本 UNKNOWN。 | docs/21 §4.3 |
| 待服务器容量评估 | PGO、其他工具 BOLT 与生产新输入 profile | 取得worker实际内存/并发/cgroup后重估PGO；现v2不自动认证混合输入，source/spec/patch/MLGO改变触发图与profile重认证；不擅自新建profile或重写。 | docs/21 §3、§8 |
| 当前第一任务/完整消费者与RPM验收未闭合 | v2离线库保留，A两组与B-bfd通过；B-lld分配失败停止 | 证据和新库在temp/static-native-conversion-v2-20260924；不得复用docs/27旧转换结果。B-lld失败涉及4GiB AS及含调试信息依赖集合，具体分配未定位；共享库/GC/原bitcode反例未执行。所有离线门禁通过后才可实施隔离spec、精确认证、一次完整LLVM和两次Tizen消费者包构建。没有自动重试。 | docs/28 §4–§6 |
| 待其他架构输入 | ARM/AArch64 static-devel与转换器兼容性、耗时 | 两现有根与cache均无static-devel；accel clang实测22.1.8并有ARM/AArch64目标，不等于实际IR读取已验证。需对应归档及真实调用路由，不能套用x86 O3或耗时。 | docs/27 §5；docs/28 §5（工作区ARM/AArch64分支均有ThinLTO，需各自转换认证） |
| 已隔离/暂缓 | 旧混合构建根与profile适用性；设计v4 | docs/24旧根不再读写；外来docs/23与重链脚本改动在备份SHA匹配后已按新授权恢复HEAD，不再是脏工作树。设计v4及BOLT后续等归档任务完成。 | docs/24；docs/25 §0 |

已关闭、不再作为待办：本机校准重试、用新门禁回判历史 FAIL、为补漂亮数字追加轮次。
历史混合试构建/根因/隔离记录保留，docs/25、docs/26不改；旧图SHA门禁与libarcher范围待决已由用户更正/解除。
本轮docs/28重新核22 RPM与17,689路径；补齐后端选项后225归档全量重新转换，旧产物未复用。
真实TU结构对照、完整索引/PIC静态检查及10成员分段抽查通过；A-bfd/A-lld、B-bfd有实际运行成功证据。
B-lld报内存分配失败，4GiB AS、无cgroup OOM；未采VmSize，不把RSS当地址空间或自然容量上界。
依失败即停规则，未继续共享库/GC/反例、未改spec或认证入口，LLVM/测试包构建均0次；设计v4/BOLT保持暂缓。
