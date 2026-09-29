# 32 归档修复 v2：Source 修订与离线证据，独占条件失效后停止

日期：2026-09-29（+08:00）；起点提交 `81ca23c504ca84814679cc0d701081995181d11c`。
docs/25–31 保持原文。本报告和 STATUS 同 commit 更新。

**状态：STOPPED_EXCLUSIVITY_LOST，未启动 LLVM 完整构建。**
Source A–M 和 spec 修订已写入隔离工作树，68 项单元测试通过；3853 条原命令全部分类通过；
225 个归档的类型元数据普查完成，五代表归档第一遍与 docs/28 逐成员及整档 SHA 相同。
但另一会话在本任务进行期间启动了 Ninja，破坏用户要求的独占条件。本会话于 10:52:10 中止自己的实验；
第二遍确定性与修正后 600 秒超时复验未完成，不能将离线阶段或 v2 整体记为 PASS。

**LLVM 构建 0 次、Tizen 测试包构建 0 次、短路 %install 0 次。**
未进入内存等待，未产生新 RPM，6/6/2 容量未认证。
`patches/archive-index-fix/` 保留 docs/31 已发布的 v1，不用未验证 v2 覆盖它；没有生成可发货 v2 format-patch。
候选 Source 与测试随本报告发布，完整候选 diff 留在下述 E；构建认证状态明确为 INCOMPLETE。

## 0. 范围、身份与独占

| 别名 | 路径 |
| --- | --- |
| W | `/home/linhao/Toolchain/development/llvm-optimize` |
| E | `W/temp/archive-fix-v2-20260929`，本次原始输出、命令 JSON 与实验产物 |
| S | `W/temp/llvm-archivefix-trial`，分支 `archive-fix-trial` |
| Rnew | `W/temp/gbs-root-x86_64-archivefix-v2`，未初始化 GBS |
| H | `W/temp/archive-index-fix-rpm-20260923/baseline-rpm-extract` |
| E28 | `W/temp/static-native-conversion-v2-20260924` |
| R30 | `W/temp/gbs-root-x86_64-archivefix/local/BUILD-ROOTS/scratch.x86_64.0`，docs/30 新构建根 |
| B30 | `R30/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build`，仅用于 Cache 路径存在性检查 |
| RT | `W/temp/toolchain-runtime-baseline/libxml2/usr/lib64` |

S 的 HEAD 为 `f111162e94aa48ed367c9d2c039456c70e7160ae`。
W/llvm 及其 spec 不动；W/spec SHA 为 `95887b2d060b38d5ef8f56936f7481a03d131f9d26432180a68e02ec95f0dda5`。
不接触已隔离旧混合根。R0 仅从原 RPMS 核验输入，未读取其 BUILD。

10:17:13 的主仓库 status 为空，无外来修改需要备份/恢复；独占锁采用 O_EXCL，
session=`archivefix-rpm-978e1efa5e184b7b9d4914a14624b66f`，holder PID=437594。
证据：`E/precheck.json`、`lock-acquired.json`。基线 22 RPM 的 SHA 全部匹配；
H 的 17,689 个唯一包内路径按逐包元数据核对，差异为 0（`rpm-identity.json`、`baseline-content-check.json`）。

### 0.1 中途出现的独占冲突

`E/exclusivity-recheck.json` 与 `other-ninja-ps.txt` 记录另一会话：

```text
PID 447427, PPID 447426, STARTED Tue Sep 29 10:39:04 2026
.../llvm_inline_development/docs/llvm_optimize_docs/verification/port22/artifacts/
m1-t30-behavior-20260929T021838Z/tools-venv/bin/ninja
-C .../m1-t30-behavior-20260929T021838Z/build -j1 clang clang-cpp clang-resource-headers
```

它在初始核查之后启动。本会话未结束、暂停或更改对方进程。
只向本会话两个 `run_stage.py` 发 SIGINT：PID 453632（五归档）与 455580（负例复验）。
两个 scope 均由现有 guard 回收，`sampler_reaped=true`、`log_reader_reaped=true`；
137 是本次主动终止，不是 OOM 证据（`owned-stage-stop.json`、对应 `*-scope/outcome.json`）。
本次后半段离线运行与其他构建重叠，不用其耗时作性能结论。
收尾释放本任务锁，现场和部分结果保留；最终记录见 `lock-released.json`、`final-integrity.json`。

## 1. 逐条评审落实与来源

来源使用用户合并评审编号 **A–M** 及“spec/单元测试/离线验证”条目。
输入没有给三家各自的逐条归属，不能编造某条来自哪一家。
“实现”仅指候选代码，不等于完成新 RPM 认证。
下表行号相对本提交的 `tools/llvm_static_archives_source.py`（与 S Source 同字节）。

| 条目/来源 | 处置与实现 | 证据/边界 |
| --- | --- | --- |
| A 选项白名单 | 采纳。逐 token 消费，包括分离参数；未分类项点名拒绝。IR、无关、补回三类明确；原 `-flto=thin` 只说明输入已为 bitcode，转换不重放。 | Source:189；§2.1 的完整 3853 条审计；docs/28 §1.1 |
| B 末项生效 | 采纳。最后 O 必须 O3、最后 DWARF 必须 4；sections/unique/addrsig 最后有效值须启用；FP contraction 取末项，缺省 on。BACKEND_FLAGS 不再硬编码 O3/FP。 | Source:172–178、253–266；§2.1；正负/顺序覆盖单测 |
| C 类型元数据 | 采纳语义检查：拒绝 intrinsic 引用、vcall metadata、SplitLTOUnit=1。LLVM 实现里的字符串不当成调用。 | Source:270；§2.2 同时列实际类型标记与纯字符串计数，不宣称所有字面串为 0 |
| D 归档格式 | 采纳。所有归档先拒绝 thin/other，再跳过 bitcode=0。 | Source:524、606；thin/other 正负单测，thin 实跑拒绝 |
| E 幂等/证据目录 | 采纳。安全边界检查后清理重建证据；全 native 打印 SKIP 成功。 | Source:552、730；单测通过；独立 buildroot 的短路验收语义待澄清，见§3.2 |
| F 原子回写 | 采纳。状态 CONVERTED→INSTALLING→PASS；JSON 临时文件+replace；归档同目录临时文件，核 SHA、复制模式后 replace；回写失败 INSTALL_FAILED。转换失败保留 FAILED。 | Source:366、563、730；中途复制失败实跑 exit 1；不声称多归档整体事务回滚 |
| G 取消/超时 | 采纳。handler 只记信号；wait4 WNOHANG 50ms；每命令 600s，TERM 后 3s KILL 进程组；成功返回前复核信号。额外处理 leader 失败后的后代。 | Source:379；首次 600s 实跑正确杀进程但顶层原因丢失，已修正；复验因独占中止，§2.4 |
| H 版本/工具/Cache | 采纳。编译器 major=22；三个工具存在且可执行；build/CMakeCache.txt 必须存在。 | Source:535；major 错误、缺工具、不可执行、缺 Cache 单测 |
| I 符号集合 | 采纳。每成员 bitcode/native 分别 llvm-nm defined/extern；大写强符号缺失拒绝；弱符号缺失按类型记账。 | Source:487–522；五归档强符号缺失 0、W 缺失 295；全库转换统计 NOT RUN；hidden 负例预期不成立，§3.1 |
| J 参数化 | 采纳。arch 仅 x86_64，并核 IR triple；工具路径/jobs/AS 全显式参数。 | Source:771；不含 ARM 执行分支 |
| K Python 3.9 | 采纳。分块 SHA，去掉 file_digest；头注释 >=3.9。 | Source:1、181；AST 按 3.9 语法解析测试；实际执行宿主 Python，不冒充 Python3.9 运行验证 |
| L 清理 | 采纳。全部回写成功后删除归档输出和非 JSON 大文件，只留摘要/IR设置/重定位/命令/符号记录。 | Source:580、758；单测与小探针成功路径通过；完整新 RPM 清理实测 NOT RUN |
| M 清理/说明 | 采纳。单一 shebang/import 区；去掉嵌入旧 SHA、内部报告引用、未用 loader/library_path/mapping_equal；说明重复成员 header-offset 身份和四个架构策略点。 | Source 头注释、inspect:97；语法/旧解析测试保留 |
| spec 条目 | 采纳。Source1005 无架构条件；util-linux 只在 x86_64；安装末尾显式路径与全部参数；清证据目录；不改 RPM 宏；6/6/2。 | §1.1、附录A；B30 路径由 Tizen rpm 解析证实 |
| 单元测试条目 | 采纳，A–I 正负例加原有测试，总计 68 PASS。 | §1.2 |
| 完整构建/验收/补丁 | 未执行。独占条件失效且离线门禁未完成，不能提前发放构建许可或覆盖已验证 v1。 | §4–§5 |

### 1.1 spec 与构建入口

Source 只在 S 更新；编译/链接并发保持 HEAD 的 **6/6/2**，转换器独立使用 **4 workers**。
转换在编译结束后的 `%install` 串行阶段，不与 Ninja 并发相叠加。GNU brp strip 链保留。

在 docs/30 的 Tizen RPM 4.14.1 中对临时 spec 副本执行 `rpmspec --parse --target x86_64 --define '_toolchain clang'`，
确认 `%{_builddir}/%{buildsubdir}/build` 展开为：

```text
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build
QUERY_EXIT=0
```

证据：`E/explicit-build-path-query-via-file.json`；临时副本移除，R30 的原 spec 未改。
此前尝试经 `/dev/stdin` 解析因该 chroot 没有该文件而失败，保留查询日志，不能当构建失败；
改用临时文件仅用于宏展开验证。此查询证明 buildsubdir，不代表 v2 spec 已完整构建。
util-linux/prlimit 的旧根包证据仍见 docs/30 §1，本版按用户要求显式加 BuildRequires。

`tools/build_llvm_x86_64.py` 仅从精确认证指纹取得 jobs；普通已认证基线仍为 4/4/1。
archive-fix-trial 限定 S 路径/分支/HEAD/spec/Source/diff SHA 和 Rnew 独占锁，
额外要求 `evidence.offline_gate_status=PASS`；本次保存 **INCOMPLETE**，即使其它字节完全相符也拒绝完整构建。
单元正例在隔离 mock 中置 PASS，不给当前候选假认证。
18 GiB、swap0、debuginfo-j4、内存>=16GiB、磁盘>=60GiB及最多六小时/每300秒的等待政策未改变。

### 1.2 单元测试

最终命令（无实际 GBS 构建，guard 测试使用模拟进程）：

```sh
PYTHONPATH=tools python3 -m unittest   tools/test_static_archives_source.py tools/test_static_archives_source_v2.py   tools/test_archive_fix_trial.py tools/test_build_llvm_x86_64.py   tools/test_build_memory_wait.py tools/test_convert_static_archives.py   tools/test_inspect_llvm_archives.py
```

```text
Ran 68 tests in 36.208s
OK
```

证据：`E/final-tests.log`。分组为原 Source 3、新增 Source 21、认证 9、guard 14、内存等待 3、原转换器 8、归档解析 10。
开发期间发现并修正了后代退出的 `/proc` 读取竞争测试、过期指纹及取消原因传播；早期失败日志仍保留，不用最终 PASS 覆盖它们。
Python3.9 的要求依据 `str.removesuffix`、`Path.is_relative_to`、`os.waitstatus_to_exitcode` 等 API；
不依赖 `hashlib.file_digest` 或 GNU time。实跑外部命令为 prlimit、clang、llvm-dis、llvm-nm、GNU ar。

## 2. 已完成与中止的离线验证

### 2.1 原命令白名单：3853/3853 PASS

输入来自 `E28/conversion/members/**/ir-settings.json`，没有凭代表 TU 猜全库选项。
`E/original-command-corpus.json` 保存每条 argv、原文件路径及 SHA；
`original-token-counts.json` 保存实际 token 频次。最终 Source 重新对全部命令分类，结果：

```text
commands=3853, status=PASS
irrelevant=293173, ir=71153, restore=11560
fp_contract: on=3853
```

证据：`E/final-policy-audit.json`。分类表源码依据沿用 docs/28 §1.1；
unique-section-names/addrsig 缺省启用的依据是
`W/llvm/clang/include/clang/Options/Options.td:4658–4663`、
`W/llvm/clang/lib/Driver/ToolChains/Clang.cpp:7992–7999`；
非 CUDA/HIP 的 FPContract 缺省 on 见同一 Clang.cpp:2789–2797。
显式反向开关和末项 DWARF5/O2 仍拒绝，不用默认值覆盖后出现的参数。

### 2.2 类型元数据普查：语义标记为 0

| 检查 | 225 归档、3853 bitcode 成员总计 |
| --- | ---: |
| `@llvm.type.test` intrinsic 引用 | 0 |
| `@llvm.public.type.test` intrinsic 引用 | 0 |
| `!vcall_visibility` | 0 |
| `EnableSplitLTOUnit=1` | 0 |

证据：`E/type-metadata-census.json`，逐成员表全部在其中。
不能把上表改写成“所有纯字符串为零”：`llvm.type.test` 字面串出现 **2** 次，
`llvm.public.type.test` 字面串出现 **1** 次，位于 libLLVMCore.a 的 Intrinsics.cpp.o 和
libLLVMipo.a 的 LowerTypeTests.cpp.o，是 LLVM 实现自身的文本，不是这些成员调用类型测试 intrinsic。
该差别在代码和 JSON 中明确保留；实际注入 intrinsic 声明的负例被拒绝。

### 2.3 五归档回归与确定性

第一遍输入取 H，编译器/llvm-dis/llvm-nm 均来自 H；通过 `LD_LIBRARY_PATH=RT` 解析现有 libxml2，未向宿主安装库。
4 workers、每命令 4GiB AS、scope 6GiB/swap0/nice15/ionice3，原机器码逐字节保留。

| 归档 | 成员 | 逐成员次序/名称/重复身份/SHA | 整档 SHA 与 E28 |
| --- | ---: | --- | --- |
| libclangCodeGen.a | 101 | PASS | `6aacfe043d4f0d4672b95b7038a6f1a073a03da2f2040eb4fda4cb07504ede5b`，相同 |
| libLLVMSupport.a | 179 | PASS | `6f19ce053b5626554b3e843e46def5968632c0e1e8f4eefb64397aacbd706f1d`，相同 |
| libarcher_static.a | 1 | PASS | `8b62ad19c1d6ed134baa37706a6aa6cbb8e320c71ca774c5179d5a62cdebabbc`，相同 |
| libclangSema.a | 86 | PASS | `709c7865aee2f5cfd1dbb93e18d22c7406cf50673830e6b02591160a9dcf70b7`，相同 |
| libLLVMAnalysis.a | 131 | PASS | `7ed41555e1659b9895efadaaed835f13df2a367665901583397087a0d33ad0dc`，相同 |

共 498 成员，488 转换、10 原样保留；第一遍 converter wall **191.763777 s**，
单成员 wait4 最大 RSS **559,800 KiB**。强符号缺失 0；允许缺失的 W 合计 295
（Analysis 82、Support 30、archer 1、CodeGen 76、Sema 106）。这些是五档统计，不能冒充全库汇总。
证据：`E/five-regression-results.json`、`five-run-1/summary.json`、逐成员 `symbols.json`。
第一遍使用本轮候选的相同选项/符号/归档策略；随后仅修正取消诊断传播，尚未以最终 Source 完成两遍实跑。

第二遍在独占冲突后主动中止，**DETERMINISM_NOT_COMPLETED**，不以“第一遍与历史相同”替代“两遍相同”的要求。
最终 scope wall 224.155125s 包含比较及部分第二遍，不是完整两遍的耗时。
该 scope 中止后未取得最终 cgroup MemoryPeak，记 UNKNOWN；进程采样和退出原因保存在 `five-regression-scope/`。

### 2.4 实跑负例

| 注入 | 已观察结果 | 当前门禁状态 |
| --- | --- | --- |
| `-mllvm -foo` | exit1，点名 `-mllvm` | PASS |
| `-gdwarf-5` | exit1，点名最后 DWARF 项 | PASS |
| `-fno-unroll-loops` | exit1，点名未分类 token | PASS |
| `llvm.type.test` | exit1，点名类型 intrinsic | PASS |
| thin archive | exit1，点名 thin archive | PASS |
| 实际删除 must_preserve 强符号 | exit1，点名 strong defined symbols missing | PASS，额外独立负例；不擅自替代用户指定 hidden 负例 |
| 中途复制抛错 | exit1，INSTALL_FAILED，点名 injected mid-copy failure | PASS |
| 挂起、忽略 TERM 的假编译器 | 首次 603.313s 后 exit1；子命令在600s超时、3s后KILL | 原顶层诊断不合格；已修复，但600s实跑复验被中止，未完成 |
| 转换追加 `-fvisibility=hidden` | 见§3.1，无符号丢失 | 原负例预期不成立，待用户裁决 |

第一次负例原始输出在 `E/negative-real/`、`negative-real-results.json`；
修正诊断后第二批的已完成七项在 `negative-real-final/`、`negative-real-final-results.json`。
首次超时的逐命令 JSON 已写具体 timeout，但主线程先观察取消状态，把顶层原因覆盖为 cancelled after command failure。
现由 Commands 保存首个失败原因，check 传播该原因；短超时、信号及后代回收单元测试通过。
复验不是一次成功的600秒门禁：因为独占中止，没有等待到时限，不能填 PASS。

## 3. 需要澄清的两条验收前提

### 3.1 hidden 不等于符号消失

用同一个合法 bitcode 探针和本版转换参数，只在后一条命令追加 `-fvisibility=hidden`，实测两者：

```text
SHA256 40ca0b5ac7e6d4e000c96f852fbbb5a4b1098404f9616117bf817bb200678e6d
llvm-nm: 0000000000000000 T must_preserve
readelf: FUNC GLOBAL DEFAULT ... must_preserve
```

证据：`E/visibility-semantics.json`、`visibility-probe/*-{compile,nm,readelf}.json`及文本输出。
两边文件字节相同，所以本探针连“可见性变化”也没有发生。
docs/28 §1.1 已说明 IR GlobalValue 带可见性，前端 `-fvisibility` 参数不是删除已存在 IR 定义的开关。
不能伪造该负例非零退出；建议保留这个实测结论，用真正删除强符号的负例认证 I。
已询问用户，收尾时尚未收到决定，不把建议当批准。

### 3.2 独立安装根的 -bi 不等于转换器二次运行

试验 spec 的 `%install` 从构建树安装，而本方案只改安装根归档、保持构建树 bitcode 不变。
因此独立 buildroot 的真实 `rpmbuild -bi --short-circuit` 会重新装入 bitcode，必须再次转换，
不能凭空满足“该次打印 SKIP”；这是流程判断，**本轮未执行 -bi**。
依据：S/packaging/llvm.spec 的 `%install` 安装命令、Source:589/730 的输入边界。
建议把验收拆为：独立 buildroot 真正完成安装/转换并验收，然后再次直接调用 Source 对同一安装树要求 SKIP。
已询问用户，尚未收到决定；不修改构建树归档来制造 SKIP。

## 4. 完整构建与新 RPM 验收：全部 NOT RUN

| 用户要求 | 本次状态/原因 |
| --- | --- |
| >=16GiB 准入，5分钟轮询、最长6小时 | 未启动等待；先决的独占与离线门禁未通过 |
| 6/6/2、18GiB、swap0、debug-j4 的一次 LLVM 构建 | 0 次；未证明6/6/2内存可行性，也未降低并发 |
| CMake 门禁、总wall/峰值、安装转换段/清理后磁盘峰值 | NOT RUN/UNKNOWN |
| 22 RPM inventory、新解包 | 没有新RPM；未创建新验收内容 |
| 225档机器码、DWARF、全符号索引/次序/函数分段及全库符号缺失统计 | NOT RUN；只有§2的五档/普查证据 |
| compiler-rt 45档与基线 | NOT RUN，不挪用docs/30结果作为v2验收 |
| brp链、格式错误0、NATIVE段完整、大文件删除 | 新构建实测 NOT RUN；Source小探针/单测不替代此项 |
| 新旧逐文件差异与libarcher双归属 | 新RPM比较 NOT RUN；历史双归属见docs/30 §3.1及spec `%files static-devel`/`%files -n libomp-devel` |
| 七项宿主消费者 | NOT RUN |
| Tizen bfd/lld 各一次、精确BuildRequires、whole-archive诊断 | 0 次；未新增这两次构建结果 |
| 独立buildroot短路幂等 | 0 次；另有§3.2前提待裁决 |
| clang-22/lld/llvm-ar 新旧SHA | 无新产物，NOT RUN |

部署与转换范围不变：x86_64 host 可经 accel 交叉构建 ARM 包；accel 取工具不取 static-devel，
x86_64 static-devel 的消费者是 x86_64 目标程序。候选只实现 x86_64 的显式认证后端策略，不是通用选项重放；
ARM/AArch64 转换另行认证。所有安装根内含 bitcode 的归档（包括 libomp-devel 与 llvm-static-devel 双归属的 libarcher_static.a）均纳入。
最终归档仍交标准 GNU strip 去 DWARF；本轮未用新 RPM 实证这一最终状态。

## 5. 候选身份、补丁状态与恢复条件

| 文件 | SHA256 |
| --- | --- |
| v2候选Source（tools与S同字节） | `6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557` |
| v2候选spec（6/6/2） | `6a91a0bf3d8d2044473662b65ed3d32d4696a697ccd52200d983ce4334aeafdf` |
| v2候选完整diff（相对f111162e，非format-patch） | `751a629228ed49fb013d95d8d8a451dc341e841c142db67198c7624d36f1ccdb` |
| docs/31 v1 format-patch（保留未覆盖） | `0c40c91cb6b896fd93f2712b669eec6771d219268dff7d290539fbb98d0bea58` |
| docs/31 v1 Source（保留未覆盖） | `2476c5efa061499d7963e0f0976f0c9c86944b688f5bcc48ea40911574af399e` |

候选完整 diff：
`/home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-v2-20260929/archive-native-conversion-v2.diff`。
在新建的干净 f111162e 临时工作树 `temp/llvm-archivefix-v2-apply-check` 上，`git apply --check` 退出0。
这仅证明能应用，**不能提交发货**。没有向 W 应用补丁、没有生成v2 LLVM提交或推Gerrit。

等独占恢复并解决§3两项后，须先补完最终Source的两遍五档/600s负例实跑，再按本任务协议进行一次完整构建及全部新RPM验收。
不得把当前 INCOMPLETE 改名为 PASS 绕过未完成项；若届时6/6/2内存失败，仍停止等用户决定。
合格后才生成v2 format-patch：作者 FatTank <hao.lin@samsung.com>、
保留 `Change-Id: Id4eb147e7ec4764d58a81110cf7bf57d21b64ac8`，提交说明登记真正使用的并发与实测结果。
当前没有这些新结果，因此没有提前写“验证通过”的提交说明。

## 附录 A：相对分支 HEAD 的 spec diff

```diff
diff --git a/packaging/llvm.spec b/packaging/llvm.spec
index 54a07ce84218..ad3840f5299b 100644
--- a/packaging/llvm.spec
+++ b/packaging/llvm.spec
@@ -44,6 +44,11 @@ Source1001: llvm.manifest
 Source1002: mlgo_arm_model.tar.gz
 Source1003: mlgo_aarch_model.tar.gz
 Source1004: mlgo_x86_model.tar.gz
+Source1005: llvm-static-archives-native.py
+
+%ifarch x86_64
+BuildRequires: util-linux
+%endif
 
 %{!?mlgo_build_jobs: %define mlgo_build_jobs 6}
 %{!?mlgo_verify_configure_only: %define mlgo_verify_configure_only 0}
@@ -396,6 +401,20 @@ rm -rf %{buildroot}%{_libdir}/debug/*
 rm -rf %{buildroot}/usr/lib/libear/*
 rm -rf %{buildroot}/usr/lib/libscanbuild/*
 
+%ifarch x86_64
+# Run after compilation has finished; these workers do not overlap build jobs.
+# Preserve the standard RPM post-processing, including archive strip -g.
+rm -rf "%{_builddir}/%{buildsubdir}/build/native-archive-conversion"
+python3 %{SOURCE1005} --root "%{buildroot}" \
+    --build "%{_builddir}/%{buildsubdir}/build" \
+    --evidence "%{_builddir}/%{buildsubdir}/build/native-archive-conversion" \
+    --arch x86_64 \
+    --compiler "%{_builddir}/%{buildsubdir}/build/bin/clang-22" \
+    --disassembler "%{_builddir}/%{buildsubdir}/build/bin/llvm-dis" \
+    --nm "%{_builddir}/%{buildsubdir}/build/bin/llvm-nm" \
+    --jobs 4 --address-space-bytes 4294967296 || exit 1
+%endif
+
 %post -n clang -p /sbin/ldconfig
 %postun -n clang -p /sbin/ldconfig
 
```

## 附录 B：相对 docs/30 已验证 Source 的完整修订 diff

下面保留完整修改供评审；可直接读取本提交的 [候选 Source](../tools/llvm_static_archives_source.py)。
注意 `patches/archive-index-fix/llvm-static-archives-native.py` 仍是 v1，二者当前刻意不同，不能混用。

```diff
--- /home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-v2-20260929/before-llvm-static-archives-native.py	2026-09-29 10:17:13.014160727 +0800
+++ /home/linhao/Toolchain/development/llvm-optimize/tools/llvm_static_archives_source.py	2026-09-29 10:50:29.485692580 +0800
@@ -1,20 +1,31 @@
 #!/usr/bin/env python3
-# Standalone RPM Source; docs/28 conversion policy, wait4 resource accounting.
-# Embedded inspect_llvm_archives.py SHA256 81008a4859172318da880f224e53c5136958c29ebc9e12194e8f729fbd2d9ae0
-#!/usr/bin/env python3
-"""Read GNU/BSD ar metadata without executing members; retain duplicate identities.
+"""Convert installed ThinLTO archive members using a certified backend policy.
 
-GNU 32/64-bit symbol tables are decoded by member header offset, then normalized
-into (symbol, ordinal, name, occurrence). No ranlib repairs are performed.
-Thin members are never followed. Unsupported index layouts fail explicitly.
+Requires Python >= 3.9 on Linux and LLVM major 22. Custom ar/ELF parsing retains
+header-offset identities for duplicate member names, and verifies full indexes.
+Text IR metadata/attribute parsing depends on LLVM 22 llvm-dis output syntax.
+Four architecture-specific policy points are deliberately explicit: backend
+options, recorded-command classification, relocation rules, and triple allowlist.
+Failing closed when parameters change is intentional; recertify before use.
 """
 import argparse
 from collections import Counter
+from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
 import hashlib
 import json
 import mmap
+import os
 from pathlib import Path
+import re
+import shlex
+import shutil
+import signal
+import stat
 import struct
+import subprocess
+import tempfile
+import threading
+import time
 
 
 def cstring(data, offset):
@@ -158,71 +169,131 @@
                     machine_symbol_entries=len(native_map))
 
 
-def mapping_equal(left, right):
-    """Offsets/mtime may change; ordered identities and every index pair may not."""
-    identities = lambda x: [(m['name'],m['occurrence']) for m in x['members']]
-    return identities(left)==identities(right) and left['index']==right['index']
-
-
-# Embedded convert_static_archives.py SHA256 26089402335e36f93a04086e8ad77db799a71e87f5b462e58ec97932807ceffa
-#!/usr/bin/env python3
-"""Convert bitcode archive members to native objects, without changing inputs.
-
-Use inside a separately bounded cgroup. Four workers, 4 GiB AS per tool;
-the first failure cancels work and terminates outstanding child processes.
-Outputs and evidence require a new directory. GNU ar preserves member order
-and duplicate names by taking each input from a separate ordinal directory.
-"""
-import argparse
-from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
-import hashlib
-import json
-import os
-from pathlib import Path
-import re
-import signal
-import shlex
-import struct
-import subprocess
-import threading
-import time
-
-
-# Verified against the saved real-TU command and LLVM 22 source. These options
-# must be supplied to native code generation; they are not recovered merely by
-# loading IR. Debug metadata, CPU/features and linkage remain in the input IR.
-BACKEND_FLAGS = ['-O3', '-ffunction-sections', '-fdata-sections',
-                 '-funique-section-names', '-faddrsig', '-g', '-gdwarf-4',
-                 '-ffp-contract=on']
+CERTIFIED_LLVM_MAJOR = 22
+CERTIFIED_OPTIMIZATION = {'x86_64': '-O3'}
+CERTIFIED_TRIPLES = {'x86_64': {'x86_64-tizen-linux-gnu'}}
+BACKEND_FLAGS = ['-ffunction-sections', '-fdata-sections',
+                 '-funique-section-names', '-faddrsig', '-g', '-gdwarf-4']
+# LLVM 22 clang/Driver/ToolChains/Clang.cpp:2797, 6228, 7992-7999.
+DEFAULTS = {'unique-section-names': True, 'addrsig': True, 'fp-contract': 'on'}
 
 
 def sha(path):
+    digest = hashlib.sha256()
     with Path(path).open('rb') as stream:
-        return hashlib.file_digest(stream, 'sha256').hexdigest()
-
-
-def ir_settings(lines, require_recorded_options=False):
-    """Read relocation flags and retained function attributes, never edit IR."""
-    retained = []
-    triple = None
-    levels = {}
-    cpus, features = set(), set()
-    command_id, recorded_command = None, None
+        for block in iter(lambda: stream.read(1024 * 1024), b''):
+            digest.update(block)
+    return digest.hexdigest()
+
+
+def classify_options(argv, arch='x86_64'):
+    """Certified policy, not arbitrary compiler-option replay; consume operands."""
+    if arch not in CERTIFIED_OPTIMIZATION:
+        raise ValueError('uncertified architecture: '+arch)
+    rows, optimizations, dwarfs, contractions = [], [], [], []
+    switches = {key: [] for key in ('function-sections', 'data-sections',
+                                  'unique-section-names', 'addrsig')}
+    operand_options = {'-D', '-I', '-isystem', '-resource-dir', '-o', '-MT', '-MF', '-x'}
+    exact_ir = {'-fomit-frame-pointer', '-fno-omit-frame-pointer', '-fexceptions',
+                '-fno-exceptions', '-fasynchronous-unwind-tables', '-funwind-tables',
+                '-fno-asynchronous-unwind-tables', '-fno-unwind-tables', '-fno-common',
+                '-ftrapping-math', '-m64', '-fPIC', '-fPIE', '-fpic', '-fpie',
+                '-fno-pic', '-fno-pie', '-fno-semantic-interposition'}
+    exact_ir.update({'-fvisibility-inlines-hidden', '-fno-visibility-inlines-hidden'})
+    index = 0
+    while index < len(argv):
+        token = argv[index]
+        category, reason = None, None
+        if index == 0 and re.fullmatch(r'clang(?:\+\+)?(?:-22)?', Path(token).name):
+            category, reason = 'irrelevant', 'original driver path'
+        elif token in operand_options:
+            if index+1 == len(argv) or argv[index+1].startswith('-'):
+                raise ValueError('missing operand for '+token)
+            category, reason = 'irrelevant', 'preprocessing, driver resource, output or language operand'
+            rows.append(dict(index=index, token=token, category=category, reason=reason))
+            index += 1
+            rows.append(dict(index=index, token=argv[index], category=category, reason='operand of '+token))
+            index += 1
+            continue
+        elif re.fullmatch(r'-O(?:[0-3szg]|fast)', token):
+            category, reason = 'ir', 'original IR pipeline; certified last optimization is also replayed'
+            optimizations.append(token)
+        elif re.fullmatch(r'-gdwarf-\d+', token):
+            category, reason = 'restore', 'debug emission version'
+            dwarfs.append(token)
+        elif token.startswith('-ffp-contract='):
+            category, reason = 'restore', 'backend FP fusion policy'
+            contractions.append(token.split('=', 1)[1])
+        elif any(token in ('-f'+key, '-fno-'+key) for key in switches):
+            category, reason = 'restore', 'backend section/symbol emission policy'
+            for key in switches:
+                if token in ('-f'+key, '-fno-'+key):
+                    switches[key].append(token == '-f'+key)
+        elif (token in exact_ir or re.fullmatch(r'-fvisibility=(?:default|hidden|protected)', token)
+              or re.fullmatch(r'-g(?:[0-3]|line-tables-only|line-directives-only)?', token)
+              or re.fullmatch(r'-march=[A-Za-z0-9_.+-]+', token)
+              or re.fullmatch(r'-m(?:sse|avx)[A-Za-z0-9_.-]*', token)
+              or re.fullmatch(r'-mfpmath=(?:sse|387|sse,387|387,sse)', token)
+              or token in ('-frecord-command-line', '-frecord-gcc-switches')
+              or token.startswith('-std=')):
+            category, reason = 'ir', 'function/module attributes, metadata or frontend semantics'
+        elif token == '-flto=thin':
+            category, reason = 'irrelevant', 'pre-link bitcode format already materialized; never replay LTO'
+        elif (token.startswith(('-W', '-D', '-I', '--target=', '-fmessage-length=',
+                               '-fdiagnostics-color=')) or token in
+              ('-fdiagnostics-color', '-fcolor-diagnostics', '-fno-color-diagnostics',
+               '-pedantic', '-pipe', '-c', '-MD', '--driver-mode=g++')):
+            category, reason = 'irrelevant', 'diagnostics, preprocessing or driver action'
+        elif not token.startswith('-') and re.search(r'\.(?:c|cc|cpp|cxx|C|ii|i|bc|ll|o|obj|s|S)$', token):
+            category, reason = 'irrelevant', 'input/output path'
+        if category is None:
+            raise ValueError('unclassified original command token: '+token)
+        rows.append(dict(index=index, token=token, category=category, reason=reason))
+        index += 1
+    if not optimizations or optimizations[-1] != CERTIFIED_OPTIMIZATION[arch]:
+        raise ValueError('uncertified last optimization: '+str(optimizations[-1:] or 'missing'))
+    if not dwarfs or dwarfs[-1] != '-gdwarf-4':
+        raise ValueError('uncertified last DWARF option: '+str(dwarfs[-1:] or 'missing'))
+    effective = {}
+    for key, values in switches.items():
+        effective[key] = values[-1] if values else DEFAULTS.get(key, False)
+        if not effective[key]:
+            raise ValueError('original command does not enable '+key)
+    contraction = contractions[-1] if contractions else DEFAULTS['fp-contract']
+    if contraction not in ('on', 'off', 'fast'):
+        raise ValueError('uncertified FP contraction value: '+contraction)
+    return dict(tokens=rows, optimization=optimizations[-1], dwarf=dwarfs[-1],
+                switches=effective, fp_contract=contraction,
+                fp_contract_source='last explicit option' if contractions else 'LLVM 22 non-CUDA/HIP default on')
+
+
+def ir_settings(lines, require_recorded_options=True, arch='x86_64'):
+    """Read LLVM 22 textual metadata/attributes without modifying input IR."""
+    retained, metadata = [], {}
+    triple, command_id = None, None
+    levels, cpus, features = {}, set(), set()
     for line in lines:
+        # Intrinsic references, not string literals in LLVM's own implementation.
+        for intrinsic in ('llvm.type.test', 'llvm.public.type.test'):
+            if re.search(r'@'+re.escape(intrinsic)+r'(?:\.|\s*\()', line):
+                raise ValueError('unsupported type metadata/intrinsic: '+intrinsic)
+        if re.search(r'!vcall_visibility\b', line):
+            raise ValueError('unsupported type metadata: !vcall_visibility')
+        if re.search(r'!"EnableSplitLTOUnit"\s*,\s*i32\s+1\b', line):
+            raise ValueError('unsupported type metadata: EnableSplitLTOUnit=1')
         if line.startswith('!llvm.commandline = '):
             match = re.fullmatch(r'!llvm.commandline = !\{!(\d+)\}\s*', line)
-            if not match:
+            if not match or command_id is not None:
                 raise ValueError('exactly one recorded command is required')
             command_id = match[1]
-        if command_id is not None and line.startswith('!'+command_id+' = '):
-            match = re.fullmatch(r'!\d+ = !\{!"(.*)"\}\s*', line)
-            if not match:
-                raise ValueError('invalid recorded command metadata')
-            recorded_command = shlex.split(re.sub(r'\\([0-9A-Fa-f]{2})',
-                lambda m: chr(int(m[1], 16)), match[1]))
+        match = re.fullmatch(r'!(\d+) = !\{!"(.*)"\}\s*', line)
+        if match:
+            metadata[match[1]] = match[2]
         if line.startswith('target triple = '):
-            triple = line.split('"')[1]
-            retained.append(line.rstrip())
+            value = line.split('"')[1]
+            if triple is not None:
+                raise ValueError('multiple IR triples')
+            triple = value; retained.append(line.rstrip())
         if line.startswith('attributes #'):
             retained.append(line.rstrip())
             cpus.update(re.findall(r'"target-cpu"="([^"]+)"', line))
@@ -236,32 +307,25 @@
             if key in levels and levels[key] != int(value):
                 raise ValueError('conflicting relocation flags')
             levels[key] = int(value)
-    if not triple or not triple.startswith('x86_64-'):
-        raise ValueError('only an explicit x86_64 IR target is certified')
+    if triple not in CERTIFIED_TRIPLES.get(arch, set()):
+        raise ValueError('uncertified '+arch+' IR triple: '+str(triple))
     pic, pie = levels.get('PIC Level', 0), levels.get('PIE Level', 0)
     if pic not in (0, 1, 2) or pie not in (0, 1, 2) or (pie and pie != pic):
         raise ValueError('unsupported PIC/PIE flags')
     if 'Code Model' in levels:
         raise ValueError('explicit code model requires separate certification')
-    if require_recorded_options:
-        if not recorded_command:
-            raise ValueError('missing original command: backend policy cannot be certified')
-        optimizations = [x for x in recorded_command if re.fullmatch(r'-O(?:[0-3szg]|fast)', x)]
-        if not optimizations or optimizations[-1] != '-O3':
-            raise ValueError('original optimization level is not O3')
-        for option in ('function-sections', 'data-sections'):
-            settings = [x for x in recorded_command if x in ('-f'+option, '-fno-'+option)]
-            if not settings or settings[-1] != '-f'+option:
-                raise ValueError('original command lacks enabled '+option)
-        if '-gdwarf-4' not in recorded_command:
-            raise ValueError('original DWARF setting not certified')
-    # Function-level CPU/features remain in the IR; do not override with -march.
-    flags = ['--no-default-config', '--target='+triple, '-x', 'ir', *BACKEND_FLAGS, '-c']
+    if command_id not in metadata:
+        raise ValueError('missing original command: backend policy cannot be certified')
+    recorded_command = shlex.split(re.sub(r'\\([0-9A-Fa-f]{2})',
+        lambda match: chr(int(match[1], 16)), metadata[command_id]))
+    policy = classify_options(recorded_command, arch)
+    flags = ['--no-default-config', '--target='+triple, '-x', 'ir', policy['optimization'],
+             *BACKEND_FLAGS, '-ffp-contract='+policy['fp_contract'], '-c']
     flags += ([{1: '-fpie', 2: '-fPIE'}[pie]] if pie else
               [{1: '-fpic', 2: '-fPIC'}[pic]] if pic else ['-fno-pic', '-fno-pie'])
     return dict(triple=triple, pic_level=pic, pie_level=pie, target_cpu=sorted(cpus),
                 target_features=sorted(features), flags=flags, evidence=retained,
-                recorded_command=recorded_command)
+                recorded_command=recorded_command, policy=policy)
 
 
 def pic_relocations(data):
@@ -298,83 +362,257 @@
     return dict(checked=checked, forbidden=forbidden)
 
 
+
+def atomic_json(path, value):
+    path = Path(path)
+    fd, name = tempfile.mkstemp(prefix='.'+path.name+'.', dir=path.parent)
+    try:
+        with os.fdopen(fd, 'w') as stream:
+            json.dump(value, stream, indent=2)
+            stream.write('\n')
+        os.replace(name, path)
+    finally:
+        if os.path.exists(name):
+            os.unlink(name)
+
+
 class Commands:
-    def __init__(self):
+    def __init__(self, address_space_bytes=4*1024**3, timeout=600):
         self.stop = threading.Event()
         self.lock = threading.Lock()
         self.children = set()
+        self.address_space_bytes = address_space_bytes
+        self.timeout = timeout
+        self.signal_received = None
+        self.cancelled_at = None
+        self.failure_reason = None
+
+    def interrupted(self, sig, frame):
+        # Python handlers run in the main thread: never acquire a worker lock here.
+        self.signal_received = sig
 
-    def cancel(self):
-        self.stop.set()
+    def cancel(self, reason=None):
         with self.lock:
+            if reason is not None and self.failure_reason is None:
+                self.failure_reason = reason
+            if self.cancelled_at is None:
+                self.cancelled_at = time.monotonic()
+            self.stop.set()
             for child in self.children:
                 try:
                     os.killpg(child.pid, signal.SIGTERM)
                 except ProcessLookupError:
                     pass
 
+    def check(self):
+        if self.signal_received is not None:
+            self.cancel()
+            raise RuntimeError('cancelled by signal '+str(self.signal_received))
+        if self.stop.is_set():
+            raise RuntimeError('cancelled after: '+self.failure_reason if self.failure_reason else 'cancelled after command failure')
+
     def run(self, argv, prefix, stdout=None):
+        self.check()
         prefix = Path(prefix)
-        timing = prefix.with_suffix('.time')
-        log = prefix.with_suffix('.log')
-        # GNU time is absent from the pinned Tizen buildroot. Keep limits in
-        # prlimit (util-linux); wait4 returns per-child, not process-global usage.
-        command = ['/usr/bin/prlimit', '--as=4294967296', '--core=0', '--', *map(str, argv)]
+        timing, log = prefix.with_suffix('.time'), prefix.with_suffix('.log')
+        command = ['/usr/bin/prlimit', '--as='+str(self.address_space_bytes), '--core=0',
+                   '--', *map(str, argv)]
         start = time.monotonic()
+        reason, status, usage, reaped = None, None, None, False
         with log.open('wb') as err:
             with self.lock:
-                if self.stop.is_set():
-                    raise RuntimeError('cancelled after first failure')
+                if self.stop.is_set() or self.signal_received is not None:
+                    raise RuntimeError('cancelled before process launch')
                 child = subprocess.Popen(command, stdout=stdout if stdout is not None else err,
                                          stderr=err, start_new_session=True)
                 self.children.add(child)
             try:
-                _, status, usage = os.wait4(child.pid, 0)
-                rc = os.waitstatus_to_exitcode(status)
-                child.returncode = rc
+                while True:
+                    now = time.monotonic()
+                    if self.signal_received is not None:
+                        reason = 'signal '+str(self.signal_received)
+                        self.cancel(reason)
+                    if now-start >= self.timeout and not reaped:
+                        reason = 'command timeout after '+str(self.timeout)+' s'
+                        self.cancel(reason)
+                    if self.stop.is_set():
+                        reason = reason or 'cancelled after command failure'
+                        if now-self.cancelled_at >= 3:
+                            try:
+                                os.killpg(child.pid, signal.SIGKILL)
+                            except ProcessLookupError:
+                                pass
+                    if not reaped:
+                        pid, child_status, child_usage = os.wait4(child.pid, os.WNOHANG)
+                        if pid:
+                            status, usage, reaped = child_status, child_usage, True
+                            child.returncode = os.waitstatus_to_exitcode(status)
+                            if child.returncode:
+                                reason = reason or 'command failed'
+                                self.cancel(reason)  # Includes descendants after the leader exits.
+                    if reaped and (not self.stop.is_set() or now-self.cancelled_at >= 3):
+                        break
+                    time.sleep(0.05)
             finally:
+                if not reaped:
+                    self.cancel()
+                    remaining = 3-(time.monotonic()-self.cancelled_at)
+                    if remaining > 0:
+                        time.sleep(remaining)
+                    try:
+                        os.killpg(child.pid, signal.SIGKILL)
+                    except ProcessLookupError:
+                        pass
+                    _, status, usage = os.wait4(child.pid, 0)
+                    child.returncode = os.waitstatus_to_exitcode(status)
                 with self.lock:
                     self.children.discard(child)
-        elapsed = time.monotonic()-start
-        record = dict(argv=list(map(str, argv)), bounded_argv=command,
+        elapsed, rc = time.monotonic()-start, child.returncode
+        record = dict(argv=list(map(str, argv)), bounded_argv=command, pid=child.pid,
                       elapsed_seconds=elapsed, exit=rc, wall=elapsed,
                       user=usage.ru_utime, sys=usage.ru_stime, max_rss_kib=usage.ru_maxrss,
-                      accounting='os.wait4; Linux ru_maxrss is KiB')
+                      accounting='os.wait4(WNOHANG); Linux ru_maxrss is KiB',
+                      timeout_seconds=self.timeout, failure_reason=reason,
+                      stderr=log.read_text(errors='replace'))
         record['time_raw'] = f"{elapsed:.9f} {usage.ru_utime:.9f} {usage.ru_stime:.9f} {usage.ru_maxrss} {rc}\n"
         timing.write_text(record['time_raw'])
-        prefix.with_suffix('.json').write_text(json.dumps(record, indent=2)+'\n')
-        if rc:
+        atomic_json(prefix.with_suffix('.json'), record)
+        if rc or reason:
             self.cancel()
-            raise RuntimeError(f'command failed ({rc}): {argv}; see {log}')
+            raise RuntimeError(f'{reason or "command failed"} ({rc}): {argv}; see {log}')
+        self.check()
         return record
 
 
-def convert(root, output, clang, disassembler, loader=None, library_path=None):
-    output.mkdir(parents=True, exist_ok=False)
-    command = Commands()
-    prefix = ([str(loader), '--library-path', library_path] if loader else [])
+def parse_nm(text):
+    result = []
+    for line in text.splitlines():
+        if not line.strip():
+            continue
+        match = re.fullmatch(r'\s*(?:[0-9A-Fa-f-]+\s+)?([A-Za-z?])\s+(.+)', line)
+        if not match:
+            raise ValueError('unrecognized llvm-nm output: '+line)
+        result.append((match[1], match[2]))
+    return result
+
+
+def compare_symbols(before, after):
+    native_names = {name for kind, name in after}
+    missing = [(kind, name) for kind, name in before if name not in native_names]
+    strong_missing = [(kind, name) for kind, name in missing
+                      if kind not in ('W', 'V', 'U', 'w', 'v', 'u') and not kind.islower()]
+    return dict(before_count=len(before), after_count=len(after),
+                missing_by_type=dict(Counter(kind for kind, name in missing)),
+                missing=missing, strong_missing=strong_missing)
+
+
+def check_symbols(nm, source, target, command):
+    rows = []
+    for label, path in [('bitcode', source), ('native', target)]:
+        output = source.parent/(label+'-symbols.txt')
+        with output.open('wb') as stream:
+            command.run([nm, '--defined-only', '--extern-only', str(path)],
+                        source.parent/(label+'-nm'), stdout=stream)
+        rows.append(parse_nm(output.read_text()))
+    result = compare_symbols(*rows)
+    atomic_json(source.parent/'symbols.json', dict(result, bitcode_symbols=rows[0], native_symbols=rows[1]))
+    if result['strong_missing']:
+        raise ValueError('strong defined symbols missing after conversion: '+repr(result['strong_missing']))
+    return result
+
+
+def validate_archive(archive):
+    if archive.is_symlink():
+        raise ValueError('archive symlink not certified: '+str(archive))
+    data = inspect(archive)
+    if data['thin']:
+        raise ValueError('thin archive is not supported: '+str(archive))
+    if data['other']:
+        raise ValueError('other-format archive members are not supported: '+str(archive))
+    return data
+
+
+def validate_tools(build, compiler, disassembler, nm, command, output):
+    if not (build/'CMakeCache.txt').is_file():
+        raise ValueError('missing CMakeCache.txt under --build: '+str(build))
+    for label, tool in [('compiler', compiler), ('disassembler', disassembler), ('nm', nm)]:
+        if not tool.is_file() or not os.access(tool, os.X_OK):
+            raise ValueError('missing or non-executable --'+label+': '+str(tool))
+    version = output/'compiler-version.txt'
+    with version.open('wb') as stream:
+        command.run([compiler, '--version'], output/'compiler-version-command', stdout=stream)
+    text = version.read_text()
+    match = re.search(r'clang version (\d+)\.', text)
+    if not match or int(match[1]) != CERTIFIED_LLVM_MAJOR:
+        raise ValueError('uncertified compiler major (required 22): '+text.strip())
+    return dict(compiler=str(compiler), version=text, compiler_sha256=sha(compiler),
+                disassembler=str(disassembler), nm=str(nm))
+
+
+def reset_evidence(root, output, build):
+    root, output, build = root.resolve(), output.resolve(), build.resolve()
+    if (root == Path('/') or not root.is_dir() or not build.is_dir() or
+            output == build or build.is_relative_to(output) or root.is_relative_to(output)
+            or output.is_relative_to(root)):
+        raise ValueError('unsafe or overlapping install/build/evidence directories')
+    if output.exists():
+        shutil.rmtree(output)
+    output.mkdir(parents=True)
+
+
+def atomic_install(candidate, destination, expected_sha):
+    mode = stat.S_IMODE(destination.stat().st_mode)
+    fd, name = tempfile.mkstemp(prefix='.'+destination.name+'.native-', dir=destination.parent)
+    os.close(fd)
+    try:
+        shutil.copyfile(candidate, name)
+        if sha(name) != expected_sha:
+            raise ValueError('temporary archive copy SHA mismatch: '+str(destination))
+        os.chmod(name, mode)
+        os.replace(name, destination)
+        if sha(destination) != expected_sha:
+            raise ValueError('installed archive SHA mismatch: '+str(destination))
+    finally:
+        if os.path.exists(name):
+            os.unlink(name)
+
+
+def cleanup_evidence(output):
+    archives = output/'archives'
+    if archives.exists():
+        shutil.rmtree(archives)
+    # Keep JSON audit records, not bitcode/ELF/text-IR/nm/command-log payloads.
+    for path in output.rglob('*'):
+        if path.is_file() and path.suffix != '.json':
+            path.unlink()
+
+def convert(root, output, compiler, disassembler, nm, build, arch='x86_64', jobs=4,
+            address_space_bytes=4*1024**3, command=None):
+    root, output, build = Path(root).resolve(), Path(output).resolve(), Path(build).resolve()
+    if arch not in CERTIFIED_OPTIMIZATION or jobs < 1 or address_space_bytes < 1:
+        raise ValueError('invalid architecture or resource parameters')
+    reset_evidence(root, output, build)
+    command = command or Commands(address_space_bytes)
     summary = dict(started=time.time(), input_root=str(root), output_root=str(output),
-                   workers=4, as_bytes=4*1024**3, archives=[], status='RUNNING')
+                   arch=arch, workers=jobs, as_bytes=address_space_bytes, archives=[],
+                   status='CONVERTING', missing_symbols_by_type={})
     def save():
-        (output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
+        atomic_json(output/'summary.json', summary)
     save()
-    def interrupted(sig, frame):
-        command.cancel()
-        raise KeyboardInterrupt(f'signal {sig}')
-    old_handlers = {sig: signal.signal(sig, interrupted) for sig in (signal.SIGTERM, signal.SIGINT)}
+    old_handlers = {sig: signal.signal(sig, command.interrupted) for sig in (signal.SIGTERM, signal.SIGINT)}
     try:
-        for archive in sorted(root.rglob('*.a')):
-            if archive.is_symlink():
-                raise ValueError('archive symlink not certified: '+str(archive))
-            before = inspect(archive)
+        summary['tools'] = validate_tools(build, Path(compiler), Path(disassembler), Path(nm), command, output)
+        archives = [(archive, validate_archive(archive)) for archive in sorted(root.rglob('*.a'))]
+        summary['scanned_archives'] = len(archives)
+        summary['native_archives_skipped'] = sum(not data['bitcode'] for archive, data in archives)
+        for archive, before in archives:
+            command.check()
             if not before['bitcode']:
-                continue  # compiler-rt and any other native archive are unchanged
-            if before['thin'] or before['other']:
-                raise ValueError('unsupported archive format: '+str(archive))
+                continue
             rel = archive.relative_to(root)
             work = output/'members'/rel
             work.mkdir(parents=True)
-            (work/'before.json').write_text(json.dumps(before, indent=2)+'\n')
+            atomic_json(work/'before.json', before)
             paths = []
             with archive.open('rb') as stream:
                 for member in before['members']:
@@ -394,35 +632,38 @@
                     paths.append((member, source, target))
             def process(item):
                 member, source, target = item
+                command.check()
                 if member['kind'] == 'machine':
                     if sha(target) != member['sha256']:
                         raise ValueError('native member changed')
                     relocs = pic_relocations(target.read_bytes())
-                    (source.parent/'relocations.json').write_text(json.dumps(relocs, indent=2)+'\n')
+                    atomic_json(source.parent/'relocations.json', relocs)
                     return dict(ordinal=member['ordinal'], name=member['name'], preserved=True,
                                 relocation_check=relocs)
                 text_ir = source.with_suffix('.ll')
                 with text_ir.open('wb') as out:
-                    command.run([*prefix, str(disassembler), str(source), '-o', '-'], source.parent/'disassemble', stdout=out)
+                    command.run([disassembler, str(source), '-o', '-'], source.parent/'disassemble', stdout=out)
                 with text_ir.open() as lines:
-                    settings = ir_settings(lines, require_recorded_options=True)
-                (source.parent/'ir-settings.json').write_text(json.dumps(settings, indent=2)+'\n')
+                    settings = ir_settings(lines, arch=arch)
+                atomic_json(source.parent/'ir-settings.json', settings)
                 text_ir.unlink()
-                record = command.run([*prefix, str(clang), *settings['flags'], str(source), '-o', str(target)], source.parent/'convert')
+                record = command.run([compiler, *settings['flags'], str(source), '-o', str(target)], source.parent/'convert')
                 data = target.read_bytes()
-                relocs = pic_relocations(data)  # also verifies x86_64 ET_REL
-                (source.parent/'relocations.json').write_text(json.dumps(relocs, indent=2)+'\n')
+                relocs = pic_relocations(data)
+                atomic_json(source.parent/'relocations.json', relocs)
                 if settings['pic_level'] and relocs['forbidden']:
                     raise ValueError('non-PIC relocation in '+str(target))
+                symbols = check_symbols(nm, source, target, command)
                 return dict(ordinal=member['ordinal'], name=member['name'], preserved=False,
-                            settings=settings, conversion=record, sha256=sha(target))
+                            settings=settings, conversion=record, symbols=symbols, sha256=sha(target))
             results = []
             iterator = iter(paths)
-            with ThreadPoolExecutor(max_workers=4) as pool:
-                pending = {pool.submit(process, item) for item in list(next(iterator, None) for _ in range(4)) if item is not None}
+            with ThreadPoolExecutor(max_workers=jobs) as pool:
+                pending = {pool.submit(process, item) for item in list(next(iterator, None) for _ in range(jobs)) if item is not None}
                 try:
                     while pending:
-                        done, pending = wait(pending, return_when=FIRST_COMPLETED)
+                        command.check()
+                        done, pending = wait(pending, timeout=0.05, return_when=FIRST_COMPLETED)
                         for future in done:
                             results.append(future.result())
                         for _ in done:
@@ -439,7 +680,7 @@
             command.run(['/usr/bin/ar', 'qcDS', str(target_archive), *[str(t) for _, _, t in paths]], work/'pack')
             command.run(['/usr/bin/ar', 'sD', str(target_archive)], work/'index')
             after = inspect(target_archive)
-            (work/'after.json').write_text(json.dumps(after, indent=2)+'\n')
+            atomic_json(work/'after.json', after)
             if [(m['name'], m['occurrence']) for m in before['members']] != [(m['name'], m['occurrence']) for m in after['members']]:
                 raise ValueError('member identity or order changed')
             if after['bitcode'] or after['other'] or not after['index_equals_machine_symbols']:
@@ -447,54 +688,101 @@
             for old, new in zip(before['members'], after['members']):
                 if old['kind'] == 'machine' and old['sha256'] != new['sha256']:
                     raise ValueError('native member not preserved in archive')
+            missing = Counter()
+            for result in results:
+                missing.update(result.get('symbols', {}).get('missing_by_type', {}))
             record = dict(path=str(rel), before_sha256=before['sha256'], after_sha256=after['sha256'],
                           before_bytes=before['bytes'], after_bytes=after['bytes'], members=before['member_count'],
                           converted=before['bitcode'], preserved=before['machine'], index_entries=after['index_entries'],
                           debug_members=sum(bool(m['debug_sections']) for m in after['members']),
-                          results=sorted(results, key=lambda x:x['ordinal']))
+                          missing_symbols_by_type=dict(missing), results=sorted(results, key=lambda x:x['ordinal']))
             summary['archives'].append(record)
+            total_missing = Counter(summary['missing_symbols_by_type']); total_missing.update(missing)
+            summary['missing_symbols_by_type'] = dict(total_missing)
             save()
             print(json.dumps({k:v for k,v in record.items() if k!='results'}), flush=True)
             for _, source, target in paths:
                 if source.exists():
                     source.unlink()
                 target.unlink()
-        summary['status'] = 'PASS'
+        command.check()
+        summary['status'] = 'CONVERTED'
         return summary
     except BaseException as error:
         command.cancel()
-        summary.update(status='FAIL', reason=str(error))
+        summary.update(status='FAILED', reason=str(error))
+        raise
+    finally:
+        try:
+            summary['elapsed_seconds'] = time.time()-summary['started']
+            cancelled = summary['status'] == 'CONVERTED' and command.signal_received is not None
+            if cancelled:
+                command.cancel()
+                summary.update(status='FAILED', reason='signal '+str(command.signal_received))
+            save()
+            if cancelled:
+                raise RuntimeError(summary['reason'])
+        finally:
+            for sig, handler in old_handlers.items():
+                signal.signal(sig, handler)
+
+
+def install(root, output, compiler, disassembler, nm, build, arch='x86_64', jobs=4,
+            address_space_bytes=4*1024**3):
+    root, output = Path(root).resolve(), Path(output).resolve()
+    command = Commands(address_space_bytes)
+    old_handlers = {sig: signal.signal(sig, command.interrupted) for sig in (signal.SIGTERM, signal.SIGINT)}
+    result = None
+    try:
+        print('NATIVE_ARCHIVES_BEGIN', time.time(), flush=True)
+        result = convert(root, output, compiler, disassembler, nm, build, arch, jobs, address_space_bytes, command)
+        command.check()
+        result['status'] = 'INSTALLING'
+        atomic_json(output/'summary.json', result)
+        for record in result['archives']:
+            command.check()
+            destination, candidate = root/record['path'], output/'archives'/record['path']
+            if sha(destination) != record['before_sha256'] or sha(candidate) != record['after_sha256']:
+                raise ValueError('archive identity changed before atomic installation')
+            atomic_install(candidate, destination, record['after_sha256'])
+            record['installed'] = True
+            atomic_json(output/'summary.json', result)
+            print('NATIVE_ARCHIVE_INSTALLED', json.dumps({k:v for k,v in record.items() if k!='results'}), flush=True)
+        command.check()
+        cleanup_evidence(output)
+        result.update(status='PASS', install_finished=time.time(), large_files_deleted=True)
+        atomic_json(output/'summary.json', result)
+        if not result['archives']:
+            print('NATIVE_ARCHIVES_SKIP all archives already native', flush=True)
+        command.check()
+        print('NATIVE_ARCHIVES_END', time.time(), 'PASS', len(result['archives']), flush=True)
+        return result
+    except BaseException as error:
+        command.cancel()
+        if result is not None:
+            result.update(status='INSTALL_FAILED', reason=str(error))
+            atomic_json(output/'summary.json', result)
         raise
     finally:
-        summary['elapsed_seconds'] = time.time()-summary['started']
-        save()
         for sig, handler in old_handlers.items():
             signal.signal(sig, handler)
 
 
-# Packaging entry: input install tree stays intact until every conversion passes.
 def install_main():
-    import shutil
-    parser = argparse.ArgumentParser(description="Convert installed x86_64 ThinLTO archives before unchanged RPM brp strip")
+    parser = argparse.ArgumentParser(description='Convert certified x86_64 ThinLTO archives before standard RPM stripping')
     parser.add_argument('--root', type=Path, required=True)
     parser.add_argument('--build', type=Path, required=True)
     parser.add_argument('--evidence', type=Path, required=True)
+    parser.add_argument('--arch', choices=['x86_64'], required=True)
+    parser.add_argument('--compiler', type=Path, required=True)
+    parser.add_argument('--disassembler', type=Path, required=True)
+    parser.add_argument('--nm', type=Path, required=True)
+    parser.add_argument('--jobs', type=int, default=4)
+    parser.add_argument('--address-space-bytes', type=int, default=4*1024**3)
     args = parser.parse_args()
-    root, build, output = args.root.resolve(), args.build.resolve(), args.evidence.resolve()
-    if root == Path('/') or output.is_relative_to(root):
-        parser.error('separate non-system install root and evidence directory required')
-    print('NATIVE_ARCHIVES_BEGIN', time.time(), flush=True)
-    result = convert(root, output, build/'bin/clang-22', build/'bin/llvm-dis')
-    for record in result['archives']:
-        destination = root/record['path']
-        candidate = output/'archives'/record['path']
-        if sha(destination) != record['before_sha256'] or sha(candidate) != record['after_sha256']:
-            raise RuntimeError('archive identity changed before install replacement')
-        shutil.copyfile(candidate, destination)
-        if sha(destination) != record['after_sha256']:
-            raise RuntimeError('archive copy identity mismatch')
-        print('NATIVE_ARCHIVE_INSTALLED', json.dumps({k:v for k,v in record.items() if k!='results'}), flush=True)
-    print('NATIVE_ARCHIVES_END', time.time(), 'PASS', len(result['archives']), flush=True)
+    install(args.root, args.evidence, args.compiler.resolve(), args.disassembler.resolve(),
+            args.nm.resolve(), args.build, args.arch, args.jobs, args.address_space_bytes)
+
 
 if __name__ == '__main__':
     install_main()
```

## 附录 C：命令与原始输出入口

所有原始文件位于上文 E 的绝对路径，temp 不上传：

- 身份与锁：precheck.json、rpm-identity.json、baseline-content-check.json、lock-acquired.json、lock-released.json、final-integrity.json。
- 选项：original-command-corpus.json、original-token-counts.json、final-policy-audit.json；原3853条命令出处逐行保留。
- 类型普查：census_type_metadata.py、type-metadata-census.json、type-census-scope/。
- 五档：five_regression.py、five-regression-results.json、five-run-1/summary.json、five-run-2/summary.json、five-regression-scope/。
- 负例：negative_cases.py、negative_cases_final.py、negative-real[-final]-results.json、对应逐成员命令JSON；不会删去首次错误诊断。
- hidden探针：visibility_probe.py、visibility-semantics.json、visibility-probe/。
- spec查询：buildsubdir-query.json、explicit-build-path-query-via-file.json；临时失败查询也保留。
- 单测：final-tests.log；早期 source/guard/unit 日志保留，最终68项PASS以 final-tests.log 为准。
- 中止：exclusivity-recheck.json、other-ninja-ps.txt、owned-stage-stop.json、各 scope/outcome.json。
- 候选：source-final.py、source-v1-v2.diff、spec-v1-v2.diff、archive-native-conversion-v2.diff、patch-apply-check-final.json。

`*-scope/` 的 build.log 带时间戳；plan.json/launch.json/commands.log 保存启动命令、cap与参数，
samples.jsonl/process-memory.jsonl 保存采样，outcome.json 保存回收状态；缺失的完整运行数据记 UNKNOWN。
本轮没有新构建、BOLT、profile、校准、Chromium或Gerrit动作。
