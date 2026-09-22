# LLVM 吞吐优化分支状态

更新日期：2026-09-22。分支：`main`；仓库：`lhmax2010/llvm-optimize`。
历史状态核对到 `8facdfa`；完整设计以 [docs/21](21_spec_integration_v3.md) 为准，本次本机试验结果见 [docs/22](22_hybrid_link_trial.md)，
取代 docs/20 的后续实施方案；历史报告、校准判定和预注册文件保持原样。
以下 `temp/` 均相对工作区 `/home/linhao/Toolchain/development/llvm-optimize`，仅保存在本机，不在 GitHub。

## 1. 计划

总目标：降低 Tizen 全平台 RPM 包构建总耗时，优化对象覆盖实际调用的 LLVM 工具。
当前目标改为混合链接：原生 x86_64 clang/clang++、llvm-ar、lld/ld.lld 静态链接 LLVM 库，
其他工具走共享库路径；别名继承实体形态，上游强制静态例外待审。仅 clang 做首版 BOLT，生成 ARM/AArch64 代码。
基线是工作区 LLVM `f111162e94aa48ed367c9d2c039456c70e7160ae` 的自研 spec，
不是旧公开快照配方。本机筛选不能替代专用服务器 Chromium 全量及全平台验收。
依据：docs/13 §1；docs/21 §0、§1、§4、§6。历史全静态 RPM 仍作为已有基线证据；混合版本一次构建成功且30 TU通过，但额外静态工具及归档索引尚有BLOCKER。

| 阶段 | 范围 | 当前状态 |
| --- | --- | --- |
| 摸底与基准台 | 配方、工具调用面、身份、资源限制、可重复测量 | 完成；历史报告保留各自证据边界 |
| 静态 RPM 基线 | 固定快照、构建、debuginfo 续跑、工具验证、基线数据 | 已完成；static-devel保留，既有归档索引缺陷须通过修复与消费者验收 |
| BOLT 筛选 | 容量、插桩/profile、重写、正确性、训练/留出、中间对照、双目标 | 本机工作已结束；最终 ARM 校准 FAIL，AArch64 PASS 并完成正式轮 |
| 集成设计与评审 | docs/21 完整 v3、混合链接拟议补丁、身份/活性脚本与协议检查 | **当前阶段：docs/21修订交三家评审；本机一次混合构建成功、30 TU PASS，范围/索引缺陷待处理；不进OBS/Gerrit** |
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
| 2026-09-22 | 本提交（`git log -1 -- docs/22_hybrid_link_trial.md`定位） | docs/22、STATUS、构建/活性脚本与测试、混合认证指纹 | 新根18GiB构建成功，22 RPM、30 TU PASS；额外五工具仍静态，223空/3残缺归档索引，一次ranlib不能修残缺表。 |

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

## 5. 挂账

| 分类 | 未闭合项 | 所需材料/下一步与验收边界 | 依据 |
| --- | --- | --- | --- |
| 待用户提供 | OBS 项目、工作区自研 spec 的实际来源、最终验证 Base 快照 | 明确 source/spec/patch/MLGO 身份，之后钉元数据与 RPM；现公开旧快照不能冒充静态 BOLT 验证快照。 | docs/20 §1.1、§8 |
| 待用户提供 | Quickbuild 全平台日志 | 统计实际链接+归档占比；>10% 启动第二阶段真实链接基准/lld profile/BOLT lld/逐字节门禁；<5% 搁置；5%–10%（含边界）默认搁置。占比用链接/归档边累计时间除全部边累计时间，与总wall另列；不以Chromium 0.2%或小夹具代替。 | docs/21 §8 |
| 待用户提供 | qemu-accel 完整源码、armv7l 生成 spec、baselibs_body、对应 OBS 宏与构建日志 | 已取 SRPM 仅含 aarch64 spec；原 VCS `e01aa7250a1a73aa8f88ba9ac4a05cbc954d1c9f` 的公共获取受凭据/403/TLS 阻碍。补齐分支和隐式后处理，不能把通用主体当完整 armv7l 执行日志。 | docs/19 §2.1–2.2；docs/20 §1.2 |
| 待评审 | docs/21完整v3与V01–V36落实、七文件混合提案、脚本/strip实验 | docs/20保持历史原文；已采纳/实现不等于评审通过，不再安排本机校准。 | docs/21附录D/E |
| 待评审/修订 | 五个额外静态工具未符合混合范围 | llvm-config、llvm-exegesis与三tblgen实测仍静态；修订方案或由用户确认明确例外，不能自动豁免/重建。保留static-devel及runtime。 | docs/22 §5.1；docs/21 §0.1 |
| 后续待验 | 混合profile rebind、seed与accel试包 | 本机容量/混合RPM别名/活性/30TU已实测；尚待图提取器认证或重训、同job seed解包文件级等价、seed热缓存两模式、accel patchelf/alias/后处理链验证。 | docs/22 §4–§6；docs/21 §1–§4 |
| 待内部团队定稿 | Quickbuild协议/δ/容差 | 本文仅结构与占位，内部团队在入队前冻结；dead_zone保留，不再提供δ建议值。 | docs/21 §6 |
| 待评审/实施 | spec 集成补丁、profile 包、自举/重认证、状态文件、隔离降级、debuginfo 策略 | 生产BOLT集成仍为设计；只在本机hybrid-link-trial分支应用获批混合补丁，原spec未改。5% stale/10% coverage 为工程政策；新集成容量指纹独立登记，执行 §4.4 负对照；先在目标executor验证子cgroup委派。 | docs/21 §2–§4 |
| 待试包/Quickbuild | 从 RPM 到 accel 到 worker 的最终身份和正确性 | 分别记录 OBS ELF/accel ELF/worker 哈希，跨 patchelf 不强求 SHA 相同；检查节区/别名/brp 后结果，worker `/emul/usr/bin/clang-22` 必查；ninja commands 和首次编译后非计时 exec trace 留证；最终产物再做 TU 门禁。 | docs/20 §1.2–§1.3、§4.2、§6.1 |
| 待 Quickbuild | BOLT 实际收益、v2 对 v1 增量、ARM 非退化与筛选方向是否一致 | 按docs/21八轮公式先冻结参数并通过preflight；同资源/输入图/缓存，取完整 wall、单位编译成本、cpu.stat、memory.peak 与下游运行资源；实际 job/tee/后台状态非零立即停止。旧本机数据不作服务器 A 组。 | docs/21 §6；docs/20 §7.1.4 |
| 待发货验收 | 静态开发包索引与后处理活性 | 常规包零LLVM.a，static-devel全归档armap非空、bfd/lld组件消费者及坏liblldCOFF.a负例；runtime保持。新试验223空/3残缺索引；普通ranlib只补空，方案B不足，须改设计并做消费者验收。每层后处理活性必过。 | docs/13 §12；docs/22 §5.2；docs/21 §4、附录 C |
| 待需求/实验 | BOLT clang 源码级 debuginfo | 首版 stripped-evaluation 不能假配旧 DWARF；如生产要求完整崩溃分析，须另测 update-debug 的容量/时间、最终符号化与 debuglink/build-id。当前成本 UNKNOWN。 | docs/21 §4.3 |
| 待服务器容量评估 | PGO、其他工具 BOLT 与生产新输入 profile | 取得worker实际内存/并发/cgroup后重估PGO；现v2不自动认证混合输入，source/spec/patch/MLGO改变触发图与profile重认证；不擅自新建profile或重写。 | docs/21 §3、§8 |

已关闭、不再作为待办：本机校准重试、用新门禁回判历史 FAIL、为补漂亮数字追加轮次。
本轮先推8facdfa，再在隔离hybrid-link-trial分支完成唯一一次18GiB正确性试构建。原LLVM分支/spec及历史校准文件SHA不变；产物留本机，未进OBS/Gerrit。docs/22与本文件同提交收尾，不隐含修补后再构建或本机性能重试授权。
