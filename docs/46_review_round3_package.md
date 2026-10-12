# 46 第二轮评审修订与第三轮评审材料

日期：2026-10-12（Asia/Shanghai）。开场 HEAD 与 origin/main 均为 `cb1e34af0958de17155459f7406869a91cadbe00`。

**当前完成：x86生产与ARM候选x86路径的两次全量回归均PASS（各225档/3864成员/完整索引/3853 flags全同）；待两ARM全量转换与宏/补丁。**

## 0. 范围与上次停止记录

W=`/home/linhao/Toolchain/development/llvm-optimize`；本轮 E=`W/temp/review-round3-continue-20261012`。temp 证据只留本机。开场开场生产 Source 为 `6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557`，ARM 候选为 `e2c2ebfa7272c6549f9be977861985ff597d3564dd26caf72438155622e30e0d`；新 SHA 见§2.1。

上次 cb1e34a 停于代理复制的历史 16 GiB 准入断言：MemAvailable=15,255,969,792 B（14.208229 GiB）；scope、llvm-dis、测试和转换均未启动，代码未改。这不是产品失败。本轮用户明确改为轻量阶段 ≥6 GiB、全量转换 ≥10 GiB；不足时每5分钟读一次，最长60分钟；运行中18 GiB cap、swap0、nice15/ionice3、30秒采样、宿主可用低于2 GiB中止。上一停止原始输出保留在 `temp/review-round3-20261012`，旧报告完整内容可读 cb1e34a 版本。（证据：旧 E/stop-result.json；本轮任务资源准入；E/run_stage.py。）

## 1. 本地完整性核查

| 核查 | 本轮结果 | 证据（相对 E） |
|---|---|---|
| 主仓库全量 `git status --porcelain=v1 --ignored` | 4,682,969 行；唯一受跟踪改动为用户 `gbs_llvm.conf`，没有额外未跟踪非忽略项 | integrity-retry/main-status-all.stdout |
| 提交 / 远端 | `66e3369..HEAD` 只有 cb1e34a；本地 HEAD、origin/main 与远端 main 均一致 | integrity-retry/main-log.stdout、main-head.stdout、remote-head.stdout |
| 基准时间后 reflog | c1ebb68（10-11 01:21:36）、66e3369（01:22:06）为上一任务文档收尾；cb1e34a（10-12 14:33:04）为准入停止记录 | integrity-retry/main-reflog.stdout；git-object-attribution.json |
| tools/*.py、patches 全部文件、docs/43–46 | 61 个受检查文件与 HEAD blob 全同，关键 Source、补丁与最终测试 SHA 全同 | integrity-retry/head-blob-check.json；input-integrity.jsonl |
| W/llvm | HEAD `f111162e94aa48ed367c9d2c039456c70e7160ae`，分支 `sandbox/fangyu.he/llvm_optmize`；仅 spec 三处既有 6→4、6→4、2→1；基准后 reflog 无记录 | integrity-retry/llvm-*.stdout |
| W/llvm spec / 用户配置 | spec `95887b2d060b38d5ef8f56936f7481a03d131f9d26432180a68e02ec95f0dda5`；配置 `28f1caf93cd39738a7da1e0da8d5f945f7372963bb9823a507f9157294272169` | input-integrity.jsonl；integrity-retry/llvm-diff.stdout |
| W 全树 find（包括源码与 temp） | 基准 2026-10-11 01:18:45+08 后 186 条；无法归因 0 | metadata-complete.json；metadata-attribution.json |
| 15 个权限盲目录 | 经免密 chroot 只读补扫元数据，exit0，新增修改记录0；未改权限/文件 | privileged-newer-command.json、privileged-newer.stdout/stderr |
| 输入与工具 | x86 225、ARM32 210、AArch64 212，共647归档全同；两根6个accel ELF及包装器、宿主readelf、保护文件共671项 SHA PASS | input-integrity-result.json、input-integrity.jsonl |

修改时间归因：本轮核查/锁/证据94条；前次准入停止23条；前次完整任务文档收尾10条；Git对象/索引/ref/log59条。Git新对象逐一核验属于 c1ebb68、66e3369、cb1e34a 或 Codex turn-diffs 自动树快照；后者只是已登记用户配置与上述文档状态，不是额外分支提交。**无法归因清单为空**。cutoff 比上轮报告正式提交早数分钟，因此没有把已登记收尾提交误判为外来修改。（证据：metadata-attribution.json、git-object-attribution.json。）

本轮唯一一次第零步辅助脚本修正：初版 Python 字符串把 find `-printf` 中的 `\0` 解码为 NUL，Popen 在执行 find 前报 ValueError。只将字符串改为 raw 字符串，范围、时间及判据均未变；改后完整扫描完成。15个权限盲目录的追加只读补扫补齐覆盖。原失败和差异保留，不当作产品失败或降低核查门禁。（证据：integrity-helper-diagnosis.json、integrity-helper-fix.diff、integrity-scope、integrity-retry-scope。）

## 2. 只读普查与后续修订状态

| 核查 | 实测结果 | 证据（相对 E） |
|---|---|---|
| x86 module asm 全集 | 225档全部3,853 bitcode；仅3个成员含语句，全部 `.globl _ZSt21ios_base_library_initv`，其他0 | x86-asm-census-result.json；x86-asm-census/逐成员 |
| ARM32 target | 3,683条全部出现2次；均 `--target=armv7l-tizen-linux-gnueabi`，共7,366次 | armv7l-target-census.json |
| AArch64 target | 3,699条全部出现2次；均 `--target=aarch64-tizen-linux-gnu`，共7,398次 | aarch64-target-census.json |
| ARM32转换归档重定位节 | 210档SHA与E4相同；SHT_REL=922,209，SHT_RELA=0 | armv7l-relocation-section-census.json |
| AArch64转换归档重定位节 | 212档SHA与E4相同；SHT_RELA=325,692，SHT_REL=0 | aarch64-relocation-section-census.json |
| 两根 /emul 解释器 | 都有原生x86_64 bash/dash/sh（bin与usr/bin路径）；未找到busybox/python/perl。仅只读识别，不作为AS方案已可用的证明 | readonly-census-result.json 的 emul_interpreters |
| `/usr/bin/cat` | 宿主、R32、R64均存在且可执行 | readonly-census-result.json 的 cat |

**B3实施；B5不实施**：两种ELF节格式完全符合收窄前提；target次数全部为2，不能改成“恰好1次”，也不自行换成“恰好2次”。A/B及D的实现与宿主验证见§2.1；C宏覆盖候选在后续补丁阶段生成。（出处：本轮条件裁决；以上全集。）

x86三个module asm位置（均IR第6行）：`libLLVMAnalysis.a/MLInlineAdvisor.cpp.o` ordinal80、`libLLVMCodeGen.a/MLRegAllocEvictAdvisor.cpp.o` ordinal137、`libarcher_static.a/ompt-tsan.cpp.o` ordinal0。同名 occurrence 均1。根内 `usr/lib64/gcc/x86_64-tizen-linux-gnu/14.2.0/include/c++/iostream:82` 实际声明匹配，文件SHA `405900b25b2ecfda0e3ff3fd52c44b89df95d3fb89987235291abaec4a522d00`。（证据：x86-asm-census-result.json、readonly-census-result.json。）

目标spec直接取 `cb67996861d070d68fec2b4c623eed7d20ba2e23:packaging/llvm.spec`，完整原文 `target-spec.txt`。debug相关条件原文：

```spec
# 11–16
%if %{defined _toolchain}
%define _toolchain_override clang
%define llvm_release_build 0
%else
%define llvm_release_build 1
%endif
# 24–30
%if 0%{llvm_release_build}
# Disable debug packages building
%define debug_package %{nil}
%define __debug_install_post %{_rpmconfigdir}/find-debuginfo.sh %{?_find_debuginfo_opts} %{?_find_debuginfo_strip_opts} %{?_find_debuginfo_ko_strip_opts} "%{_builddir}/%{?buildsubdir}"\
    rm -rf "%{buildroot}/usr/lib/debug"\
    rm -rf "%{buildroot}/usr/src/debug"
%endif
```

同条件还控制spec57–59的sed依赖及178–182的编译参数处理；420行删除安装根libdir/debug残留。实际文件带tab的逐字原文以target-spec.txt为准，未改spec。（证据：target-spec.txt、readonly-census-result.json/debug_matches。）

宏取docs/38同一x86根 `W/temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0`，包 `rpm-build-4.14.1.1-1.4.x86_64`，`usr/lib/rpm/tizen_macros:34–38`：

```rpm
%__strip_install_post    \
    %{!?__debug_package:%{_rpmconfigdir}/brp-strip %{__strip}} \
    %{_rpmconfigdir}/brp-strip-static-archive %{__strip} \
#    %{_rpmconfigdir}/brp-strip-comment-note %{__strip} %{__objdump} \
%{nil}
```

文件SHA `f0f991bd97f44b7bf906ac4a7a45cd34b7444c1acce2358261e4a95b3e68ebc8`；根内直接rpm --eval读到默认strip为`/bin/strip`。本轮尚未加入新的宏覆盖，后续会分别验证debug开启/关闭。（证据：tizen_macros.txt、rpm-build-version.json、strip-macro.json、strip-default.json。）

### 2.1 本轮 Source 与测试修订

评审来源：用户给定 Kimi、Codex、Claude 第二轮合并意见和PM裁决；未给逐条原文归属，不自行分配到某一家。

| 编号 | 处理 | 当前证据 |
|---|---|---|
| A1 | 通用-W前拒绝-Wa,，保留Wall/Wp诊断 | 新负例通过 |
| A2 | clang主版本22；dis/nm完整版本与clang一致，summary记三工具版本/原文/SHA | 21.1.0、22.1.9错配负例通过 |
| A3/A4 | 共用单条module asm白名单；x86输出同名符号恰好一个U | 全集前置通过；缺失/T/w/重复负例通过 |
| A5 | 读取x86重定位符号前检查表内边界 | 越界负例通过 |
| B1 | ARM声明唯一且info=0x10、other/raw_section/section_index/value/size均0 | UND正例；定义/ABS/COMMON/WEAK/HIDDEN/FUNC/重复/非零值/大小负例通过 |
| B2 | ARM clang固定22.1.8，变化要求重做docs/44§2普查；三个工具拒绝machine40/183；版本一致性复用A2 | 版本及三工具双架构ELF负例通过 |
| B3 | ARM32仅REL、AArch64仅RELA | 全集满足前置；格式正负例通过 |
| B4 | PIC直接读layout合并后的symbol记录 | 原重定位夹具通过 |
| B5 | **不实施**：真实命令均为2次target，不擅改条件 | §2全集 |
| B6 | 节名表索引0拒绝 | 正负例通过 |
| B7 | 不改Commands，经相同prlimit调用cat读AS软硬值；默认拒绝失效，仅ARM CLI显式确认才允许 | mock正负例、x86参数拒绝、宿主真实enforced=true通过；两ARM根探针见§2.2 |
| D | 就绪后退出的后代取消夹具、第二归档原子替换失败、真实x86 bitcode转换屏蔽全部ARM函数、逐字+AST共用函数对照 | 全部通过 |

B7的显式确认只存在ARM分派路径：ARM install包装器用线程局部上下文限定一次调用，finally恢复；共用install/Commands不改。失败读回值保存在address-space-probe.json及summary；确认不代表AS已经生效。（出处：本次Source差异。）

宿主原99项+新增17项，共116/116 PASS。初轮129.708s通过；静态复核后，把新增READY/退出码断言移到立即/proc快照之后，避免推迟取样，所有断言保留；最终全套再次116/116，87.567s。不是失败后重试。仍保留已知的强符号“仅名称包含”边界，没有扩大成绑定/大小完全等价。（证据：host-tests-initial-result.json、host-tests-result.json、test-authoring-order-note.json；Source compare_symbols未变。）

| 文件 | 当前 SHA256 |
|---|---|
| `tools/llvm_static_archives_source.py` | `014fd32f309bc0be80471eebf8a4a3cf50a5656ce3a2584e4bbdfb9a05a9affd` |
| `tools/llvm_static_archives_arm_trial.py` | `c3edada01a077496f797ce766906008ae95d9a0430a389db8972b055c73191c8` |
| `tools/test_static_archives_source_v2.py` | `e1468a933a3acf82c0bceda8c44bf2710459da52859d647782097037144570b9` |
| `tools/test_arm_archive_trial.py` | `6b5d2cf7a17fb2bd2b97ecaaea6b4a10d24d7e05141f7555cbebc8b9bf6e8ed4` |
| `tools/test_archive_review_round3.py` | `21d55d0504262358d979699aeb607dfd310f7f1e27b33961b51a59a1bd754805` |

完整diff：[x86相对6bd](46_x86_source_round3.diff)、[ARM相对e2](46_arm_source_round3.diff)。这两份是本轮代码差异，不是Gerrit format-patch。旧上传补丁与其随附Source保留不动；PS3/PS2目录尚未生成。根内结果见§2.2；本轮新Source的独立全量离线结果见§2.3。

### 2.2 根内测试与地址空间探针

R32的Python为`3.14.2 (main, Oct 1 2026, 21:46:23) [Clang 22.1.8]`。完整116项执行一次，按预注册规则分类：112 PASS、3环境不适用、1已知AS发现；原始unittest仍报告1 FAIL+3 ERROR，没有篡改成116 PASS。

| 原测试 | 分类及实际原因 |
|---|---|
| test_actual_limits_and_monitor_cleanup | 环境不适用：FileNotFoundError /usr/bin/time |
| test_failure_stops_following_commands | 环境不适用：FileNotFoundError /usr/bin/time |
| test_sections_symbols_visibility_and_relocations | 环境不适用：as --64 返回1（x86汇编夹具） |
| test_limits_accounting_and_no_external_time | 已知AS发现：读回[-1,-1]，预期[4294967296,4294967296]；core仍[0,0] |
| 其余112项（含17项新增） | 全部PASS，无额外跳过 |

证据：root-suite-raw.json、root-suite-classified.json、armv7l-tests.stdout/stderr。没有改上述四个测试或安装工具；新真实B7测试在宿主要求enforced=true，在已识别的ARM解释器环境验证拒绝/确认行为，不替代原AS测试。

| B7直接探针 | 未确认 | ARM显式确认 | AS软/硬读回 | enforced |
|---|---|---|---|---|
| R32 | 拒绝，错误要求显式参数 | 通过并记录确认true | unlimited / unlimited | false |
| R64 | 拒绝，错误要求显式参数 | 通过并记录确认true | unlimited / unlimited | false |

宿主真实探针读取4294967296/4294967296、enforced=true。这里“确认后通过”只允许用户知情接续，不声称qemu的AS限制已生效。原生限制器仍挂账。（证据：armv7l-b7-result.json、aarch64-b7-result.json、host-tests-result.json。）

两个根的/proc分别临时挂载，finally均卸载；挂载前/期间/后mountinfo、全部chroot命令与退出码存`*-mount-*.txt`、root-commands.json。没有运行GBS或构建LLVM。（证据：root-stage-result.json。）

### 2.3 新 Source 全量离线复验

所有输入均先复核SHA；使用独立新输出目录，不回写构建树原件。x86两条路径分别执行，不以一条路径的成功替代另一条。

| 路径 | 归档 / 有序成员 | 完整索引条目 | 与历史整档SHA | 后端flags / Thumb | 转换wall秒 | 证据（E内） |
|---|---|---:|---|---|---:|---|
| x86-production | 225 / 3864 | 318543 | 225/225全同（docs/35） | 3853 flags逐项全同 | 2792.146 | x86-production-result.json；x86-production-conversion/summary.json |
| x86-candidate | 225 / 3864 | 318543 | 225/225全同（docs/35） | 3853 flags逐项全同 | 4673.640 | x86-candidate-result.json；x86-candidate-conversion/summary.json |

- x86-production：module asm 3个全部通过；强符号缺失0；允许缺失按类型`{'W': 1920}`。
- x86-candidate：module asm 3个全部通过；强符号缺失0；允许缺失按类型`{'W': 1920}`。

x86判据覆盖整档after SHA、每个成员的序号/名称/同名序号/SHA、完整符号→成员映射与3853套后端flags。ARM判据覆盖格式、完整索引、原机器码保留、强符号、PIC/TLS、ARM32参考Thumb与全部属性；两ARM在宿主使用原生转换器，探针软/硬均4294967296、enforced=true，未使用忽略AS确认。

## 3. 本轮资源记录

| 阶段 | 准入 GiB | 启动可用 GiB | scope 峰值 GiB | 结果 |
|---|---:|---:|---:|---|
| integrity-scope | 6 | 16.121895 | 2.951160 | exit 1；采样器已回收 |
| integrity-retry-scope | 6 | 15.857098 | 4.945427 | exit 0；采样器已回收 |
| integrity-inputs-scope | 6 | 15.716362 | 1.474655 | exit 0；采样器已回收 |
| x86-census-scope | 6 | 14.778671 | 3.315685 | exit 0；采样器已回收 |
| readonly-census-scope | 6 | 14.689720 | 1.802883 | exit 0；采样器已回收 |
| host-tests-scope | 6 | 14.172653 | 1.136986 | exit 0；采样器已回收 |
| host-tests-final-scope | 6 | 14.067207 | 0.873978 | exit 0；采样器已回收 |
| root-tests-probes-scope | 6 | 14.211998 | 0.310577 | exit 0；采样器已回收 |
| x86-production-scope | 10 | 14.185158 | 6.883991 | exit 0；采样器已回收 |
| x86-candidate-scope | 10 | 14.023224 | 7.113110 | exit 0；采样器已回收 |

全部阶段 MemoryMax=19,327,352,832 B、MemorySwapMax=0，未触发 OOM 或2 GiB宿主保护线。Git/find 的 scope 峰值包含文件缓存和内核 slab，不等于应用匿名内存。（证据：各 scope/plan.json、memory-summary.json。）

## 4. 不采纳项及理由（PM 已裁决）

下列为用户明确规定的设计边界，不是本轮实验新结论：

| 项目 | 不采纳理由 / 后续位置 |
|---|---|
| 重定位偏移加写入宽度检查 | 门禁不读目标字节；宽度随类型变化，统一 4 字节会误拒节末 1/2 字节重定位 |
| 内存看门狗 | 事后反应式，不等价于 RLIMIT_AS，且需改共用 Commands 循环 |
| `/emul` 原生 prlimit | 需改 qemu-accel 打包，超出 LLVM 包范围；保留为长期方案 |
| Python 解析 ARM 属性替代 readelf | 待第二段实测 qemu 调用开销再决定 |
| spec 改 `%{?buildsubdir}`、删除 `rm -rf`、补 binutils 依赖 | 非缺陷，不对总部评审中的 spec 做无功能收益改动 |
| 安装失败时另打印已安装清单 | summary 已记录，不为日志改共用安装函数 |
| 合并两个 change | Gerrit 依赖链保证顺序 |
| 把诊断数字写进 Commands 注释 | 证据放文档，不改 Commands |

出处：本轮任务第五步“不采纳项及理由”清单。

## 5. 第三轮与生产集成挂账

1. 完成七项只读普查，实施 A–D，宿主/根内测试与 B7 探针；依序完成 x86 两次和两 ARM 全量离线复验。
2. 生成第三轮评审的 PS3/PS2 候选与全量 diff；当前未生成。
3. 下一轮评审后做 x86 完整构建：cb679968 叠两个新补丁，扩大原编译与转换产物结构对照样本。本轮不做 RPM 构建。
4. ARM 第二段：根内 readelf 版本/输出/耗时、GNU ar 根内与宿主一致性、32位Python峰值、每命令600秒余量、/proc、磁盘、架构BuildRequires、/emul原生工具及显式AS确认、并发、最终RPM索引/符号/PIC/消费者验收。
5. 地址空间长期方案：原生限制器及交付边界；显式确认不等于限制已生效。

历史证据入口：[docs/44](44_arm_source_review_round1.md)、[docs/45](45_gerrit_patches_review_package.md)。不推 Gerrit、不清理磁盘；项目锁在后续阶段继续持有。
