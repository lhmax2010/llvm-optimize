# LLVM 吞吐优化分支状态

更新日期：2026-09-22。分支：`main`；仓库：`lhmax2010/llvm-optimize`。
本次备案核对到结果提交 `80bc93a`；完整设计以 [docs/20](20_spec_integration_v2.md) 为准。
以下 `temp/` 均相对工作区 `/home/linhao/Toolchain/development/llvm-optimize`，仅保存在本机，不在 GitHub。

## 1. 计划

总目标：降低 Tizen 全平台 RPM 包构建总耗时，优化对象覆盖实际调用的 LLVM 工具。
当前实施设计聚焦静态链接 LLVM 库的原生 x86_64 clang；生成 ARM/AArch64 代码。
基线是工作区 LLVM `f111162e94aa48ed367c9d2c039456c70e7160ae` 的自研 spec，
不是旧公开快照配方。本机筛选不能替代专用服务器 Chromium 全量及全平台验收。
依据：docs/13 §1、docs/20 §1、§4.4、§6。

| 阶段 | 范围 | 当前状态 |
| --- | --- | --- |
| 摸底与基准台 | 配方、工具调用面、身份、资源限制、可重复测量 | 完成；历史报告保留各自证据边界 |
| 静态 RPM 基线 | 固定快照、构建、debuginfo 续跑、工具验证、基线数据 | 已完成；llvm-static-devel 发货缺陷仍挂账 |
| BOLT 筛选 | 容量、插桩/profile、重写、正确性、训练/留出、中间对照、双目标 | 本机工作已结束；最终 ARM 校准 FAIL，AArch64 PASS 并完成正式轮 |
| 集成设计与评审 | docs/20、身份脚本、R01–R22 处置、冻结验收协议 | **当前阶段：设计/脚本已交付，待三家评审；尚未把 BOLT 集成进 spec** |
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
| 2026-09-22 | 本提交（下述命令定位） | `docs/STATUS.md` | 建立五段状态备案与每任务同 commit 维护规则；本轮只新增此文件。 |

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
| AArch64 最终训练集正式 GM(v2/RPM)=0.848116、GM(v1/RPM)=0.852074、GM(v2/v1)=0.995354；前置噪声底 0.835047% PASS。10 项，前两者含重链/剥离/BOLT。内部“约 15%”只能指该口径的**耗时降低**，不是吞吐增幅或全平台收益。 | docs/20 §7.1.1、§7.1.3–7.1.4；`temp/bench_results/bolt-final-split-20260921/aarch64/formal.json` | 通过校准；正式/训练集 |
| **v1 虽只用 ARM 训练，已在 aarch64 编译负载上呈现通过校准的正向效果**（上行 v1/RPM）。这不是 v1 曾采 aarch64 profile 的证据，也不证明覆盖整个 AArch64 后端；v2/v1 接近 1，增量收益未确证。 | docs/20 §3.1、§7.1.3–7.1.4 | 通过校准（性能观测）；不作函数覆盖推断 |
| 最终 ARM 校准 FAIL 4.272374%，未跑正式轮；v2/v1 两轮诊断 GM=1.002496/1.004235，不能确证 ARM 非退化。全程采样 load1 最大 4.28，无 >10 样本、无保留 suspect，采样器已回收。 | docs/20 §7.1.1–7.1.2；`temp/bench_results/bolt-final-split-20260921/attempt.json`、`loadavg-summary.json` | 诊断（性能）；硬证据（执行/门禁状态） |
| 历史 FAIL 保留：docs/17 两对 4.345326% / 6.609160%；docs/20 附录 A 为 3.846399%；附录 D 双目标为 3.334074%。不按新协议回判，也不把拆分 AArch64 PASS 合成为双目标 PASS。 | docs/20 §5、§7、§7.1、附录 A/D | 诊断；失败判定已闭合 |
| 公开 Base 快照 `tizen-base-toolchain_20260912.061113` 的 accel 仍动态链接 LLVM，与工作区静态基线不同；证明该快照陈旧，不否定已确认的 OBS 流水线。 | [docs/19 §1.2、§3](19_spec_integration_v2.md)；docs/20 §1.1 | 硬证据（ELF/VCS）；流水线为用户确认前提 |
| 已取得的同 VCS qemu-accel aarch64 spec 通用主体有 cp -aL、patchelf 解释器/RUNPATH 处理、cmp 恢复别名软链接、fdupes/转包接口；跨此环节不能要求 ELF SHA 不变。armv7l 完整分支/隐式后处理仍缺证据。 | docs/19 §2.1–2.2；docs/20 §1.2 | 硬证据（已取得源码范围） |
| 本机 patchelf 副本实验保留 `.note.bolt_info`、`.bolt.org.*`、`.text.cold`，3 TU 完整 .o PASS；不能替代 OBS brp/fdupes/完整 accel 转包验证。 | docs/20 附录 C | 硬证据；单一显式转换 |
| 身份脚本包含架构/binfmt 禁执行、动态依赖、BOLT 三态、RPM 信息项与辅助错误传播；真实 ELF 正负例和 mock 测试 49/49 PASS。 | docs/20 §5；`tools/test_verify_toolchain_identity.sh` | 硬证据（测试）；最终 worker 仍需另验 |

对外统一口径：**筛选层多轮测量方向一致，BOLT 对 LLVM 自身源码编译负载有稳定正向影响，量级待构建服务器验收。**
不对外给收益百分比，不称“五轮独立”，不将训练集结果或诊断比值当作留出泛化认证。

## 4. 人工裁决前提

下列为用户决策及其记录依据，区别于上一节的实测事实。后续 Session 不能擅自反转。

| 决策 | 依据与范围 | 登记位置 |
| --- | --- | --- |
| 基线固定工作区 spec 的 x86_64 分支，保留 -O3、ThinLTO、LLVM 静态链接等自研优化，不退回安装包配方。 | 用户指定生产 accel 同源目标；后以该 spec 构建并验证。 | docs/12“定位与基线”；docs/13 §1 |
| 本机只做筛选，最终 Chromium 全量在专用服务器；不在本机构建 Chromium，不推 Gerrit。 | 本机容量有限、筛选负载不等于平台构建；供 GitHub 评审。 | docs/README；docs/12“定位与基线”；docs/20 §6 |
| debuginfo 用调用参数 `_smp_mflags -j4`，不关 debuginfo、不改优化参数、不抬完整构建 cap。 | -j40 失败与 -j4 续跑实测；等价性优先于省时间。 | docs/13 §5–§7 |
| 完整构建以实测同构指纹准入：18 GiB、4/4/1、debuginfo -j4；新集成指纹须另认证。 | 峰值加法模型已废弃；cgroup 保护机器，准入避免无证据的长时间失败，不保证永不 OOM。 | docs/14 §2；docs/20 §2.3 |
| 22 GiB 是单次有界插桩试验的临时启动政策：单线程、SwapMax=0，available<24 GiB 记录而不拒绝。 | 18 GiB 是截断峰值，随后 22 GiB 成功；不外溢到完整构建 18 GiB。未来 OBS seed 自举须单独授权/记录。 | docs/19 §4；docs/20 §2.3、§3.1 |
| PGO 因开发机容量暂缓，待服务器容量评估重估；PGO 与 BOLT 可叠加。 | 原加法模型失效，不将旧“PGO=NO”传递为永久技术结论。 | docs/19 §4；docs/20 §2.3 |
| 首版仅 BOLT clang；emit-relocs 走单 clang 重链重放，放弃全局 CMAKE_EXE_LINKER_FLAGS。 | 已有热缓存重链实测；隔离失败可降级，不波及普通全部工具链接。普通路径改动另列 `-d keeprsp`。 | docs/19 §4；docs/20 §2、§4.4 |
| 第一版不改 CLANG_VENDOR / LLVM_VERSION_SUFFIX；身份用 Release、可信哈希、节区和实际路径。 | 避免版本字符串兼容性风险；跨 patchelf 分阶段追踪哈希。 | docs/20 §1.3 |
| 用户确认 OBS→qemu-accel→Base→Quickbuild 链路及 `_use_gbs_clang=1`；解除“旧动态快照即全线停止”。 | 旧快照陈旧不改变工作区静态目标；最终验证快照仍待定，worker 调用仍须实证。 | docs/20 §1.1；docs/19 为历史调查，不再沿用其停止状态 |
| profile v2 扩为 ARM 13 + aarch64 10；优先独立 noarch RPM，无 profile 预期降级普通包。 | Quickbuild 有 aarch64 包，补训练覆盖；首版工程门槛 stale 函数比例≤5%、有效覆盖≥10%，不是性能保证。 | docs/20 §3 |
| lld/ar 只测量记录，不参与校准 pass/noise_floor。 | 现有小夹具主要测启动开销；自 `795a5c4` 起仅对之后运行生效，旧 FAIL 不追溯改判。 | docs/20 §7 |
| 按目标拆分最后校准，冻结条件后先提交推送，再经用户“开始”启动；无论结果不再本机重试。 | 将 69 组合的最大偏差拆为两个集合，判据仍编译差≤3%、CV≤3%、无保留 suspect；启动 load1≤3。 | `ea7d120` 预注册；docs/20 §7.1；结果 `80bc93a` |
| Quickbuild 固定 A/A 一对 + A/B 三对共八轮，A 为同 source/spec/patch 的 without_clang_bolt。 | 任一 A/A 指标 d>0.10 在 A1 前中止；否则每对 B/A 严格小于 `1-max(0.03,2d)`，不满足即未确证、不加轮；保留 cpu.stat 第二口径和资源门槛。 | docs/20 §6.2–§6.3；`tools/test_final_bolt_calibration.py` |
| 对外仅定性；内部数字标分母、是否含重链剥离、训练/留出、正式/诊断和门禁状态。 | 避免把耗时降低写成等幅吞吐提升，避免跨轮漂移和失败校准混入收益认证。 | docs/19 §4；docs/20 §5、§7.1.4 |

## 5. 挂账

| 分类 | 未闭合项 | 所需材料/下一步与验收边界 | 依据 |
| --- | --- | --- | --- |
| 待用户提供 | OBS 项目、工作区自研 spec 的实际来源、最终验证 Base 快照 | 明确 source/spec/patch/MLGO 身份，之后钉元数据与 RPM；现公开旧快照不能冒充静态 BOLT 验证快照。 | docs/20 §1.1、§8 |
| 待用户提供 | Quickbuild 全平台日志 | 统计实际链接+归档占比；>10% 启动第二阶段真实链接基准/lld profile/BOLT lld/逐字节门禁；<5% 搁置；5%–10%（含边界）待决。不以 Chromium 0.2% 或小夹具代替。 | docs/20 §8 |
| 待用户提供 | qemu-accel 完整源码、armv7l 生成 spec、baselibs_body、对应 OBS 宏与构建日志 | 已取 SRPM 仅含 aarch64 spec；原 VCS `e01aa7250a1a73aa8f88ba9ac4a05cbc954d1c9f` 的公共获取受凭据/403/TLS 阻碍。补齐分支和隐式后处理，不能把通用主体当完整 armv7l 执行日志。 | docs/19 §2.1–2.2；docs/20 §1.2 |
| 待评审 | docs/20 完整 v2 与 R01–R22 最终处置、身份脚本、最终拆分结果 | 转三家评审；已采纳/实现不等于评审通过，不再安排本机校准。 | docs/20 附录 E、§7.1 |
| 待评审/实施 | spec 集成补丁、profile 包、自举/重认证、状态文件、隔离降级、debuginfo 策略 | 当前仍为设计，未改 spec。评审后才试包；5% stale/10% coverage 为工程政策；新集成容量指纹独立登记，执行 §4.5 负对照。 | docs/20 §2–§4 |
| 待试包/Quickbuild | 从 RPM 到 accel 到 worker 的最终身份和正确性 | 分别记录 OBS ELF/accel ELF/worker 哈希，跨 patchelf 不强求 SHA 相同；检查节区/别名/brp 后结果，worker `/emul/usr/bin/clang-22` 必查；ninja commands 和首次编译后非计时 exec trace 留证；最终产物再做 TU 门禁。 | docs/20 §1.2–§1.3、§4.2、§6.1 |
| 待 Quickbuild | BOLT 实际收益、v2 对 v1 增量、ARM 非退化与筛选方向是否一致 | 按冻结八轮协议执行；同资源/输入图/缓存，取完整 wall、单位编译成本、cpu.stat、memory.peak 与下游运行资源；实际 job/tee/后台状态非零立即停止。旧本机数据不作服务器 A 组。 | docs/20 §6、§7.1.4 |
| 待发货验收 | llvm-static-devel 归档符号索引缺陷 | 干净消费者链接/运行验收，或从发货集剔除；尚未修复/验收，不能伴随 BOLT 包静默发货。 | docs/13 §12；docs/20 §4.4 |
| 待需求/实验 | BOLT clang 源码级 debuginfo | 首版 stripped-evaluation 不能假配旧 DWARF；如生产要求完整崩溃分析，须另测 update-debug 的容量/时间、最终符号化与 debuglink/build-id。当前成本 UNKNOWN。 | docs/20 §4.3 |
| 待服务器容量评估 | PGO、其他工具 BOLT 与生产新输入 profile | 本机历史峰值不是其他图/配置的保证；现本机 v2 profile 不自动认证未来 OBS 输入。source/spec/patch/MLGO 变化触发重认证；不擅自新建 profile 或重写。 | docs/20 §2.3、§3、§4.4 |

已关闭、不再作为待办：本机校准重试、用新门禁回判历史 FAIL、为补漂亮数字追加轮次。
本次状态备案只新增 `docs/STATUS.md`；没有运行基准、编译、profile 采集或 BOLT，没有修改其他文件。
