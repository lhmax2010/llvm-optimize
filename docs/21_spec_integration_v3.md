# 21 BOLT 集成设计 v3：混合链接、后处理活性与服务器验收

日期：2026-09-22。本文完整取代 docs/20 的后续实施设计；docs/20 原文、历史校准与判定保持不动。
先读并核对了 [STATUS.md](STATUS.md)，起点为 `312a358`。本轮只有源码/元数据调查、
已有 ELF 副本的 strip 实验、脚本及测试；**未应用补丁，未 configure/build LLVM，未构建混合版，
未采 profile、未运行 BOLT、未做性能校准或 Chromium 构建、未推 Gerrit**。

用户裁决：下游运行 wall/CPU 容差 2%、内存 3%，编译期内存容差 5%；
本机性能校准结束，后续本机只做功能/稳定性验证；目标改为混合链接。
量化容差是用户接受的工程政策，不是从这几轮实验估计出的自然误差。

路径：`W=/home/linhao/Toolchain/development/llvm-optimize`；`E=W/temp/spec-v3-20260922`；
`TC=W/temp/toolchain-baseline/usr`；`Q=W/temp/bolt-measurement-20260918/run`；
`E16=W/temp/bolt-final-20260918`；`E2=W/temp/bolt-aarch64-v2-20260921`；
`R1=W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0`；
`S=W/llvm/packaging/llvm.spec`；`QS=W/temp/spec-review-20260921/source-rpm/qemu-accel-aarch64.spec`。
源码基点 `f111162e94aa48ed367c9d2c039456c70e7160ae`，已有 spec 并发差异保留。
原始资料只保存在 temp，不在 GitHub；本轮索引见附录 F。

## 0. 混合形态与实施前置

目标：clang/clang++、llvm-ar、lld/ld.lld **静态链接 LLVM/Clang 组件库**，其他工具维持共享库路径；
不指 libc 全静态。clang++ 是 clang 别名，lld/ld.lld 是同一实体家族；llvm-ranlib/lib/dlltool
也是 llvm-ar 别名，不能同一个实体一面静态、一面动态。别名均继承实体链接形态。
静态组件仍须存在于 build tree 供链接；取消的是 llvm-static-devel 发布，不是禁止构建 .a。

**源码机制结论：有条件可行，尚未构建验证。** executable 的 per-target 开关存在，
clang driver 可用目录局部 CLANG_LINK_CLANG_DYLIB=OFF；但 clang/lld 的静态组件接口
会把 `LLVM` 共享库传递给最终链接。仅给三个工具添加 DISABLE 开关不足以证明无共享依赖。
附录 A 给三个 CMakeLists、spec 以及必要的 AddLLVM/AddClang/AddLLD 接口修补拟议 diff，
共七文件；`git apply --check` 只验证上下文，不是配置/链接验证。没有改工作区源码。

另有已存在的上游强制静态例外（llvm-config、llvm-exegesis、部分 tablegen/support）：
不能把“全局 ON”写成“其余每个 ELF 都必然动态”。精确静态实体/别名和这些例外须纳入审批清单；
如要求消除所有例外，须另审这些目标的附加补丁，不在本轮悄悄扩范围。见附录 A.1。

四项前置全部关闭前，不进入 BOLT spec 实施：

| 前置 | 当前状态 | 完成判据 |
| --- | --- | --- |
| 混合补丁批准 | 待用户批准 | 审定七文件提案、别名/上游例外、归档移除范围与 CMake 开发接口处理 |
| 反向依赖审计 | 本机快照运行依赖查询完成；OBS BuildRequires UNKNOWN | 在目标 OBS 项目取得 buildinfo、反向依赖及文件级消费者证据；禁止把 0 个 Requires 当成无构建消费者 |
| 混合构建实测 | NOT RUN | 只在获批后执行；验证 CMake、最终 NEEDED、图摘要、profile rebind、资源/磁盘/inode 新指纹 |
| accel 试包 | NOT RUN | 补完整源码/宏日志，验证字节转换、别名、节区、活性、最终 worker 身份与正确性 |

### 0.1 静态库移除的范围风险

S:83–89 定义 llvm-static-devel；S:529–532 用 `%{_libdir}/lib*.a` 收文件。
实际基线此包含 **225 个 .a**，其中 libarcher_static.a 同时在 libomp-devel；
compiler-rt 子包另有 **45 个 .a**。S:609–624 的 runtime/OpenMP 列表与主开发包不同。
因此“撤下 llvm-static-devel”和“所有子包零 .a”不是同一操作。
本轮已单独向用户确认 runtime 范围，未收到确认前不把运行库删除当成授权的实施步骤。
附录 A 的最小提案只删除顶层开发归档、保留 libarcher_static.a 和 compiler-rt，**属于待批准提案**。
若用户坚持全 RPM 零 .a，附录 A 列出替代 diff 和下游运行库阻塞；不能静默保留或静默删除。

移除 .a 还可能使 llvm/clang/lld 的已安装 CMake export 引用不存在的 archive。
S:514–526、578–582 发布这些 cmake 目录；AddClang.cmake:123–146 与 AddLLD.cmake:15–30
注册组件导出。试包必须用干净消费者执行 find_package/共享库链接，必要时生成共享库专用
export 集并更新依赖；本轮未构建，具体 export 结果 UNKNOWN，不宣称提案已是可发货补丁。

## 1. 生效路径、accel 体积与身份

### 1.1 部署链与当前快照

用户确认链路：工作区混合 spec/source/patch/MLGO → OBS x86_64 LLVM RPM → qemu-accel
消费并转换 → 新 Base 固定快照 → Quickbuild worker `/emul/usr/bin/clang-22` →
Chromium 平台 clang（`_use_gbs_clang=1`）。最终 OBS 项目/新快照待用户提供。
旧公开 Base `tizen-base-toolchain_20260912.061113` 的 x86_64 clang/accel 均为旧动态形态，
只能作调查样本，不能冒充混合候选。原证据：[docs/19 §1.2、§3](19_spec_integration_v2.md)。

### 1.2 转换与体积

QS:305–347 从 clang-*、clang++、opt/lli/llc、llvm-*、lld/ld.lld、libLTO/LLVMgold 收集文件和 ldd 库；
QS:366–400 先 cp -aL，再改 PT_INTERP，非空绝对 RUNPATH 才改到 emul 库目录；
QS:619–645 用 cmp 将 clang 家族相同副本恢复为软链接；QS:682 为 fdupes。
现 SRPM 仅含 aarch64 生成 spec，armv7l baselibs_body/隐式 brp 仍未取得。
不能把上述通用主体当成完整 armv7l 执行日志。证据：docs/19 §2.1–2.2。

试包必须：对同一输入、相同 patchelf 二进制/环境/参数独立处理两次并比较输出 SHA；
记录解释器/RUNPATH、LOAD/节区和后处理步骤；不一致即停止，不能用“patchelf 会改 SHA”掩盖不确定性。
本轮未重做 patchelf；旧单次副本实测保留 BOLT 特征及 3 TU PASS（docs/20 附录 C），
**双次确定性仍待试包**。最终 accel 别名逐项记录 lstat 类型、目标、inode、内容 SHA；
静态/动态不同实体必须不同 SHA，cmp 只能合并内容完全相同且批准的别名组。

本轮解包旧 accel RPM 的全部文件作清单（E/accel-inventory.json），再按路径替换模型：
共享库和非选中工具取旧 accel 的实测字节数；选中实体取 TC；BOLT clang 取 E16/E2。
旧 RPM 为 **54,806,369 B**（约 55 MB），xz 参数 `5T`；解包 /emul 常规文件总量 **239,582,376 B**。
这不是内存量；别名/目录/包头不计入常规文件总量。

| 模型（后 clang 别名恢复） | 未压缩常规文件 B | 压缩体积代理 B | 相对旧包体积代理 |
| --- | ---: | ---: | ---: |
| 旧动态快照实物 | 239582376 | 54806369（实际 RPM） | 1.000 |
| 混合、普通 clang | 592536712 | 135547473 | 2.473 |
| 混合、BOLT v1 clang | 668507104 | 152926303 | 2.790 |
| 混合、BOLT v2 clang | 671488368 | 153608291 | 2.803 |
| 全静态工具模型、普通 clang | 2687050440 | 614684103 | 11.216 |
| 全静态工具模型、BOLT v1 clang | 2763020832 | 632062933 | 11.533 |

压缩代理严格按 `新常规文件总量 × (54806369/239582376)`，只是旧包压缩比的线性外推；
**未实际压缩候选、不是预测区间或容量保证**，新代码重复率/包布局/压缩参数可改变结果。
全静态模型替换旧清单里所有 usr/bin 实体为本机相应静态产物，仍保留旧库集合作同口径比较；
未来 ldd 闭包可能增删共享库，实包大小 UNKNOWN。所有逐文件源路径与算式在 E/size-model.json。

关键原始体积：TC clang-22=139929464 B，E16 BOLT=215899856 B，E2 BOLT=218881120 B；
TC lld=83539336 B，llvm-ar=14825632 B。clang++ 不另计一份最终实体；
旧 accel lld/ld.lld 各一常规文件，llvm-ar/ranlib/lib/dlltool 各一份，模型保留这种实际重复。
它们分别取同一静态家族体积，不把 llvm-ranlib 假标成动态。旧 libLLVM=83596248 B、
libclang-cpp=62750008 B 因其他动态工具仍须保留，不能从混合估算中减掉。
cp -aL 到 clang 别名恢复前还会临时多出 clang-cl、clang-cpp、clang++ 三份实体：
混合普通额外 419788392 B，BOLT v1 额外 647699568 B；这部分计入 staging 磁盘，不能拿最终包量替代。
QS 的 cmp 循环不比较 llvm-ar 与 lld，也不比较任意动态工具；它们不会仅因链接形态或同版本误合并。
未来 fdupes 的具体宏行为仍需枚举实包验证。

### 1.3 身份与 worker

第一版不改 CLANG_VENDOR/LLVM_VERSION_SUFFIX。Release 与外部可信清单绑定，节区只是交叉证据。

| 层级 | 必须留存 | 判据 |
| --- | --- | --- |
| OBS 原始 LLVM RPM | NEVRA/RPM SHA、spec/source/patch/MLGO、普通/候选 ELF SHA、profile SHA、pre/post_brp manifest | 混合形态与实际包一致，所有必需测试通过 |
| accel 输出 | 消费的输入 SHA、qemu VCS、patchelf 版本/参数、输出 SHA、别名/节区/NEEDED/活性记录 | 跨 patchelf 不要求 SHA 相同，要求授权确定性转换与语义一致 |
| Quickbuild worker | accel 可信输出清单 SHA、现场 ELF SHA、BOLT 节区、活性、实际 exec trace | 最终 `/emul/usr/bin/clang-22` 匹配；不能只查 `/usr/bin/clang` ARM 壳 |

LLVM 包的 `/usr/share/llvm/clang-bolt/manifest.json` **不在 QS 的 /emul 收集列表**，worker 不依赖它。
worker 从可信发布资产取得 accel 输出清单（不能现场自算 expected SHA），验证示例：

```bash
CC_EMUL=/emul/usr/bin/clang-22
EXPECTED_SHA=发布清单中已核验的实际SHA
./verify_toolchain_identity.sh --expected-sha256 "$EXPECTED_SHA" --expect-bolt present "$CC_EMUL"
./check_bolt_liveness.sh "$CC_EMUL" --output "$EVIDENCE/liveness"
```

A 组要求 expect-bolt absent；两组都记录脚本 SHA/完整输出/退出码。binfmt UNKNOWN 不准绕过，
foreign ELF 自动只读，NAME_ONLY 仅提示；test-only registry override 不准用于生产验收。
先 `ninja -t commands` 保存 cc/cxx，再在首次编译后做一次非计时 exec trace，确认最终 ELF。
固定署名部署和 exec trace 解决时序身份；脚本前后 stat 检查不是原子快照，见帮助的 TOCTOU 提示。

## 2. 普通路径改动、重链与资源

### 2.1 三种入口与无条件 keeprsp

普通路径显式改动清单：混合链接补丁/取消开发静态包；**所有 A/B/seed 普通 ninja 都无条件
`-d keeprsp`**，与 `%{with clang_bolt}` 无关。同一 source/spec/patch/CMake 的 A/B 普通
ninja argv、环境、cwd、shell 逐字节一致；只有主构建完成后的候选处理不同。
启动普通 ninja 前运行同一冻结 ninja 的 `-d list` 并保存 stdout/rc；不支持 keeprsp 则写
`FALLBACK_UNSUPPORTED_CONFIG`，BOLT 不启动，普通构建用双方一致的普通路径；不能让 A/B 只有一边加开关。
keep-rsp 的磁盘、文件数/inode 增量计入新容量指纹，不套用旧 18 GiB 同构凭证。

| 入队模式 | bcond | 依赖/行为 |
| --- | --- | --- |
| ordinary A | without clang_bolt、without clang_bolt_seed | 普通混合构建依赖，不依赖 profile/重写工具 |
| candidate B | with clang_bolt、without clang_bolt_seed | 普通依赖 + 已认证 BOLT 工具/runtime/独立 noarch profile 包 + 外部隔离执行器 |
| seed export | with clang_bolt_seed、without clang_bolt | 普通依赖 + relink/strip/封装能力，不依赖现成 profile；同 job 额外输出 seed 子包 |

同时 with seed 与 with bolt 立即拒绝。`%build` 开头展开 `_toolchain`：未定义→
`FALLBACK_TOOLCHAIN_UNDEFINED`；非 clang、非 x86_64、未知 CMake/driver 形态→
`FALLBACK_UNSUPPORTED_CONFIG`，普通构建继续，写状态。原 x86_64 MLGO/O3/ThinLTO 参数不降低。

BOLT job **依赖解析失败**发生在 spec 执行前，spec 无法捕捉：由入队控制器标
`SUPERSEDED_BY_ORDINARY`，记录失败 job ID 并立即提交 ordinary job；发布门禁仅看这个
ordinary job 的最终成功状态和产物，不能把未运行的 BOLT job 算成功。
平台不支持这种替代提交时，采用普通依赖集合 + 受信 `%{?_bolt_profile_path}` 只读资产路径；
路径缺失/签名/SHA 不符分别按 no-profile/profile 降级。不得设置必装 profile 后再声称 spec 内可恢复。

### 2.2 链接重放契约

主 ninja 成功后 `ninja -t commands clang` 定位唯一最终链接命令。普通 ninja **启动前**冻结
shell ELF/版本、cwd、完整环境（含 PATH/LC/TZ/模型变量）、driver/linker ELF 和动态库身份；
重放使用同一个环境快照。敏感环境不公开，证据资产加访问控制，但不能漏掉影响链接的变量。

解析器处理已认证语法的 argv、环境赋值、重定向/串联与引号；**禁止 eval**、禁止把文本
简单 split 后当等价命令。`$ORIGIN` 按原 shell 的单/双引号展开语义保留，未知 shell 结构降级。
递归登记 @rsp 的原始字节、嵌套引用、所有对象/归档及成员顺序、链接脚本 INCLUDE、插件/模型对象的 SHA；
环/缺失/越界路径拒绝。最终 rsp 的 mtime 必须不早于 bin/clang-22；更老即 `FALLBACK_RELINK_INPUT`，
不通过 touch 伪造新鲜度。这个保守规则可能拒绝合法热构建，届时降级并留证，不事后取消。

只在已解析最终 argv 追加 `-Wl,--emit-relocs` 并替换主输出为独立候选；保留 cwd/rsp/ThinLTO
与全部普通 flags。枚举所有写出：候选 ELF、独立 depfile、登记 ThinLTO cache；
map/time-trace/save-temps/response 写回等若未登记，拒绝重放，不覆盖普通产物。

ThinLTO cache 必须非空、参数/版本一致且来源为此次普通构建；否则 FALLBACK_RELINK_INPUT。
16 GiB 是**热态阶段上限**，不是冷链接保证（已有冷链接 16.83 GiB、热链接 9.760868 GiB）。
第一次混合认证必须分别测试两种 cache 方案：只读快照；独立目录复制完整已热缓存。
只读模式写入失败即降级；独立副本禁止落回主 cache。记录 inode/体积和认证 linker 的命中/未命中统计；
工具不支持可审计统计则记 UNKNOWN、该模式不认证为热态。两种都测试不等于本轮重新链接；均待批准后进行。

### 2.3 隔离与容量

实施前在**目标 OBS executor** 跑最小 job，证明 cgroup v2 子组委派可用、读回 max/swap/events、
验证 PID 属于预期父子组、注入子组 OOM 后控制器和普通产物存活并能回收。
不允许 RPM chroot 另开绕过父组的 systemd 兄弟 scope。缺委派→FALLBACK_NO_ISOLATION。
原完整构建上限 18 GiB、并发 4/4/1、debuginfo -j4 不变；混合+BOLT 为新指纹，须另行认证。

| 串行可选阶段 | MemoryMax | wall 超时 | 最小可用磁盘 | 说明 |
| --- | ---: | ---: | ---: | --- |
| 单 clang 热重链 | 16 GiB | 20 min | **12 GiB** | 不足 FALLBACK_NO_DISK；含缓存副本、rsp/inode预算 |
| strip-debug 副本 | 6 GiB | 5 min | 2 GiB | 只 llvm-objcopy --strip-debug；保留 relocs/symtab，禁止换成 GNU/eu-strip |
| 纯 BOLT rewrite | 6 GiB | 5 min | 2 GiB | v2 已测自身 3.678791 GiB/24.43 s；非 DWARF 更新保证 |
| 每个正确性编译 | **独立子 cgroup 4 GiB** | 180 s | 1 GiB | 串行；同时 RLIMIT_AS=4 GiB，禁 swap/core |

磁盘阈值为启动政策，不是测量下界；另按已登记文件数检查可用 inode。每阶段启动前读父组
`memory.max/current`，剩余额度不得小于本阶段上限及已登记控制器预算；宿主还须留 ≥2 GiB。
无法核验或不足→FALLBACK_NO_HEADROOM。不相加各阶段峰值，不抬父组上限。
每30秒 free/load/tree RSS、每秒目标 VmHWM、time -v、cgroup peak/events；nice15/ionice-c3；
宿主 available<2 GiB 紧急中止。所有退出路径杀净子组并回收日志/采样器，确认无 PID。

可选阶段非零/OOM/超时保留失败现场并产 ordinary；主构建/install 自身失败是真失败。
只有候选通过 post_brp、事务 COMMITTED 且提升成功才删除本 job 的 relocs/stripped 中间件；
失败路径不删，immutable seed/profile 资产不在清理范围。最终候选、日志、哈希和必要普通回滚证据保留。
22 GiB 仅为一次有界 profile 插桩政策，MemorySwapMax=0，不外溢到 18 GiB 完整构建或 6 GiB 纯重写。

## 3. profile 自举、图绑定与有效性

### 3.1 同 job seed 子包

首个生产输入用 **`--with clang_bolt_seed --without clang_bolt`**，代替 v2 独立 seed job 提案。
先照 ordinary 路径生成包内容，受限重放后 strip-debug，额外产 `llvm-bolt-seed` 子包：
stripped ELF（现有参照 226730672 B，未来实际记录）、relocs/stripped SHA、链接 argv/递归 rsp、
对象清单/图摘要、CMake/source/spec/MLGO 身份和工具/环境清单。不把 3.56 GB relocs ELF 装进正常 clang 包。
seed 是独立子包/资产，不进 accel 收集列表。

**ordinary 与 seed 模式的普通 RPM 逐包字节相同**为强门禁，而非只比较 ELF/payload。
为此预先固定 SOURCE_DATE_EPOCH、实际 RPM 支持的 buildtime/buildhost/mtime 规范、排序、
压缩和签名策略；两个模式的非 seed 包必须 cmp。若目标 RPM 不支持复现、或额外子包改变 debuginfo
分组导致差异，记 SEED_REPRODUCIBILITY_BLOCKER，不以去签名/仅 payload 相同冒充通过。
目标根支持哪些 reproducibility 宏要在试包前查清；本轮未试包，不保证此要求已实现。

维护者 lhmax2010 批准输入/图与 profile 发布。下载 OBS seed 后，在本机按单次有界
22 GiB、1线程、SwapMax=0、nice/ionice/采样/低于2 GiB中止入口插桩；保留 runtime archive、
instrumentation-binpath、PID 后缀等 docs/16 原参数。**本轮不执行插桩**。
未来授权的 OBS 新输入不是当前本机 Q 输入，不得混用 SHA。
训练采用 v2：ARM 13（seed73419，scale1/2/2，A/B/C+训练10）+ AArch64 10；各自 target/sysroot，
同版本资源目录；冻结23条输入/flags/SHA，每组 fdata 明确列出，不用通配符混入留出。
合并 profile + manifest 优先独立 noarch RPM；首次无 profile 的 ordinary 是 FALLBACK_NO_PROFILE，符合预期。

### 3.2 两级 rebind 与混合首次输入

manifest version=3，至少包括 owner/reviewer、source/spec/patch/MLGO、BOLT/runtime/loader SHA、
relocs_input_sha、stripped_input_sha、graph_digest_schema/hash、profile_sha、双目标 corpus、
参数/警告基线、认证正确性、debug policy 和签名。build/input/profile 三者不可只靠版本号关联。

1. stripped 输入 SHA 与认证输入一致：直接绑定，仍执行 §3.3/正确性/活性门禁。
2. SHA 不同但**已认证同版本图提取器**给出的图摘要相同，且 §3.3 全通过：允许自动 rebind，
   state/manifest 写 `input_rebind_auto=true`、原/新 relocs/stripped SHA、图/工具/schema/判据；不得改原 manifest。
3. 图不同、摘要缺失、解析含歧义或 schema/tool 改变：重新训练并认证；不自动推断“应该差不多”。

source/spec/patch/MLGO 变化先触发重新认证；图相同可按第2级复用，图变必须重训。
混合首次构建也走同一规则，不能因沿用源码 f111162e 就默认 v2 profile 可用。

图摘要方案（待混合试验认证，本轮不生成候选图）：固定架构/端序/ABI；以唯一符号ID+重名消歧
记录函数边界/大小、规范化指令与操作数、基本块/CFG边、间接跳转表、重定位类型/加数/符号目标、
代码引用的数据段内容与 EH/unwind 关联；将仅地址布局变化的地址规范为符号+偏移。
排序后 canonical JSON 哈希，并保存原始 readelf/objdump、构建对象/归档成员/链接命令摘要供交叉核对。
不能只哈函数名/数目或 .text 大小；不能忽略有语义的数据/relocs/模型对象。
提取器无法完整覆盖或碰到未知 relocation/ICF别名/缺函数边界时失败并重训，不能以弱摘要自动 rebind。
先用原件、只改 debug/build-id 的副本、改指令/跳转表的负对照认证提取器后才开放自动路径。

全静态与混合 clang 是否同输入 **UNKNOWN**：源组件可相同、基线 PIC=ON，但共享接口、
LLVM_BUILD_STATIC/可见性、归档顺序、ThinLTO 导入、链接器/缓存/环境、模型对象、build-id/debug
路径和新重放都可能改变最终 SHA/图。基线证据为 R1 CMakeCache 的 PIC=ON、BUILD_SHARED_LIBS=OFF、
LLVM_TOOL_LLVM_DRIVER_BUILD=OFF 及 docs/14 最终链接命令；新图须实际取得，不能先断言一样。

**A/B LLVM 各构建一次**（同混合补丁、不同 clang_bolt bcond）；下文八轮均是 **Chromium 构建**，
不是反复重建 LLVM，也不是在各轮重新训练/rewrite profile。

### 3.3 stale、覆盖率与警告门禁

固定命令为 docs/16 的 ext-tsp/cdsort/split-functions/split-all-cold/split-eh/dyno-stats、
thread-count=1，并加 `-stale-threshold=5`。命令行含 `-infer-stale-profile`（包括显式赋值形式）
即 FALLBACK_PROFILE；不允许从日志缺行推断已关闭该功能。

认证解析器取以下**数量**，拒绝缺行/重复行/负数/不合理分母：

- N、M：`BOLT-INFO: N out of M functions in the binary (...) have non-empty execution profile`。
- S：`BOLT-WARNING:` 或 `BOLT-ERROR: S (...) function[s] have invalid (possibly stale) profile`。
- 覆盖率 **(N−S)/M ≥10%**；stale 函数占比 **S/N ≤5%**，不是 samples 比例。
- S 行不存在，只有在工具版本/完整成功日志格式均已认证、argv 不含 infer-stale 时允许 S=0；
  non-simple 行独立记录，不能再次从 N 减掉。

源码：`llvm/bolt/lib/Passes/BinaryPasses.cpp:1487–1502,1524–1564` 定义数量/比例/严格大于阈值退出；
`llvm/bolt/lib/Profile/StaleProfileMatching.cpp:51–53` 默认关闭 infer-stale。
当前 v2 N=23592、M=144032、S=0；383 non-simple 已被排除于 regular profile 统计之外。
5%/10% 是工程准入政策，不是性能保证。

manifest 加 `rewrite_warning_baseline`，当前已认证 v2 实验日志的三类计数：
`split_function=1`（条数），`failed_relocations=2804`（警告里的 relocation 数，不是1条），
`jump_past_end=6`（条数）。证据 E2/rewrite-scope/build.log:9–17；所有警告保留原文。
state 写三类观测与基线；任一计数 > baseline×1.20（整数精确比较）、基线0出现>0、或新警告类别，
即 FALLBACK_PROFILE。已知 stale 警告仍受新类别政策，stale≤5% 不豁免 warning gate；首次认证
如需接纳新的警告类型，须离线评审更新 baseline，不能运行时自动扩白名单。错误行无条件失败。

## 4. 安装事务、打包后处理与发货

### 4.1 固定状态文件

`%{_builddir}/llvm-%{version}/clang-bolt/state.json` 固定路径；%build 原子写（临时文件、fsync、rename），
%install 校验版本/终态/SHA 后读，%check 只读；不能让 --nocheck 导致清单缺失。

```json
{
  "schema": 3,
  "input_sha256": "64hex",
  "candidate_sha256": null,
  "profile_sha256": null,
  "relocs_sha256": null,
  "graph_digest": null,
  "input_rebind_auto": false,
  "status": "FALLBACK_NO_PROFILE",
  "failure_reason": "profile asset absent",
  "rewrite_warning_counts": {"split_function": 0, "failed_relocations": 0, "jump_past_end": 0},
  "rewrite_warning_baseline": {"split_function": 1, "failed_relocations": 2804, "jump_past_end": 6},
  "started_at": "UTC ISO8601",
  "finished_at": "UTC ISO8601"
}
```

终态枚举冻结：ORDINARY、BOLT_READY、BOLT_INSTALLED、FALLBACK_NO_PROFILE、FALLBACK_PROFILE、
FALLBACK_TOOLCHAIN_UNDEFINED、FALLBACK_UNSUPPORTED_CONFIG、FALLBACK_RELINK_INPUT、
FALLBACK_NO_ISOLATION、FALLBACK_NO_HEADROOM、**FALLBACK_NO_DISK**、FALLBACK_OOM、FALLBACK_TIMEOUT、
FALLBACK_STRIP、FALLBACK_REWRITE、FALLBACK_CORRECTNESS、FALLBACK_STATE。
RUNNING 不是可安装终态。依赖入队的 SUPERSEDED_BY_ORDINARY 在队列 manifest，另连 ordinary job ID。
失败原因必须非空并存日志路径/rc，不能仅改状态字符串掩盖失败。

### 4.2 实体/别名事务和 pre/post_brp

普通实体**完整复制**到 build tree 的 `clang-bolt/ordinary/`，不是硬链接，不在 strip 会扫描的
BUILDROOT 里保存回滚副本。登记每个别名的软/硬链接类型、目标、inode；拒绝循环/逃逸链接。
预制新主文件和全部硬链接临时名（同一候选 inode），为软链接也预制临时链接；写 fsync 的 PREPARED
事务日志后逐项 rename。整组核验后写 COMMITTED，全部别名切换成功才允许删普通事务副本。
任一异常先恢复**整组**并复核普通 SHA/链接类型；恢复不完整则 %install 非零，不能 fall-open。
再入发现 PREPARED/未提交日志，先恢复完成再尝试新事务，不继续半安装状态。

%install 末尾生成 pre_brp 清单（候选状态、实体/alias SHA/类型、节区/活性），加入 %files。
`__debug_install_post` **执行前**再次检查 alias manifest。保持原 install-post 链次序，
在原链末尾**无条件**追加 finalizer，生成 post_brp 清单；%check 只校验 post_brp，--nocheck 不跳过 finalizer。
实施时用目标 RPM 的宏展开记录确认插入位置，捕获原宏体再包装，禁止递归定义/替换掉原链。
部署 finalizer 要在普通和 BOLT 包都安装执行；输出放 `%{buildroot}%{_datadir}/llvm/clang-bolt/manifest.json`，
包含 pre_brp/post_brp 独立 SHA、debug policy 和实际 fallback 状态。不能自称其中有最终 RPM 的自引用 SHA，
最终 RPM/accel SHA 由包外可信发布清单给出。

**每层后处理后强制活性检查**：strip/objcopy、BOLT 候选、RPM brp、accel patchelf/fdupes/转包、
worker。记录 LOAD 个数、entry 位于可执行 LOAD、version rc、最小 TU rc；与该层认证结构比较。
任一失败阻止该产物发货。后处理已毁损时，不能把 `%check` 跳过或静默恢复一个未走完整链的文件后照发；
保留现场，另走普通终态/重新试包。未知处理层也不能只用 BOLT note 尚在作为成功依据。

### 4.3 debuginfo

首版 Quickbuild 评估包使用 llvm-objcopy --strip-debug 输入，无旧 DWARF，
`debug_policy=stripped-evaluation`；不假配普通 clang 的 debuglink/build-id/DWARF。
其他工具原 debuginfo 流程保留 -j4。实施时必须用**目标 OBS 根** find-debuginfo.sh、RPM宏与 brp
重新核对，不把本机 R1:389–399 的跳过行为推广为未来所有根。
本轮 GNU strip/eu-strip **退出0但破坏 BOLT 活性**已复现（附录 C）；这些后处理必须条件跳过、
替换为已认证安全路径，或使 BOLT 降级/试包停止；不能只在末尾隐藏错误。
若要求 clang 源码级调试，另行认证 `--update-debug-sections` 的容量、时间、符号化/源码行/内联栈与
RPM debuglink/build-id 一致性；目前 UNKNOWN，不能引用 3.7 GiB 作为该模式的预算。

### 4.4 静态开发包门禁与功能红线

不发布 llvm-static-devel 后，原“修复归档索引再发货”改为：**检查拟发货包中禁止的 .a 为零，
反向依赖审计通过**；不是宣布既有索引缺陷已修复。若要求整个 RPM 集零 .a，必须同时处理 §0.1
的 compiler-rt/libomp 运行库兼容性；未定范围/审计不通过不发货。附录 A 分开列清两种范围。
CMake 导出、llvm-config 和使用共享库的消费者仍要验收，不能只删除 %files 条目留下失效开发接口。
若将来恢复发布：**全归档 armap** 检查 + lld 组件消费者实际链接/运行 + 删除索引的负对照为硬条件。

BOLT 前后对最终混合/RPM/accel 形态重做 ARM训练10+ARM留出10+AArch64训练10，共30 TU 完整 .o cmp；
两边同 clang-22 --driver-mode=g++、保留 -frecord-gcc-switches，不过滤节区。任何差异 BLOCKER。
已有全静态30 TU PASS只证明旧输入，不能代替此试包。

必须注入验证：无profile/错SHA、_toolchain未定义、rsp缺失/陈旧/未知写出、冷cache、磁盘/父组余额不足、
隔离缺失、OOM/超时、stale/警告增加、state损坏、事务中途退出/回滚失败、硬链接/逃逸软链接、
--nocheck、strip活性失败、worker身份漂移。各分支须有终态与非零/降级证据，不能仅由设计表代替测试。

## 5. 证据口径

| 观测 | 正确限定 |
| --- | --- |
| docs/16 GM 0.846042 | ARM13训练、前置校准PASS1.595225%、正式、分母同轮RPM，含重链/剥离/BOLT |
| 最终 AArch64 GM 0.848116 / 0.852074 | 10训练TU、校准PASS0.835047%、一次正式、v2/RPM与v1/RPM，含重链/剥离/BOLT；第二顺位、已经暖机 |
| 最终 ARM GM 0.854402 等 | 训练/诊断，校准FAIL4.272374%，无正式轮；不能作认证收益 |
| docs/20 附录 B | 中间三方两轮通过校准1.986133%，GM重链/剥离中间效应接近1，非纯BOLT新正式轮 |

**armv7l 在筛选层无合格认证**：只有 docs/16 一次通过校准的训练集正式轮，留出/最后确认未通过；
不能把这句话改成“从未有过一次PASS”。AArch64 有一次通过的正式轮，但次序/暖机与目标混淆，
不是已证明比 ARM 更稳定，也不是 Quickbuild 认证。

本机噪声参照：docs/20 附录 A 编译 GM 的同轮 A/A 配对为1.002369、0.998587（约±0.24%），
同名跨轮1.013230、1.009407（约1%）。**这是GM层描述，不是每个TU都在±0.24%**；原整体FAIL保留。
v2/v1约0.5%的点值不能作为选择v2的增益证据；不高于会话间约1%的噪声参照，逐目标/次序也有混淆。
v2的理由是训练代表性覆盖 ARM+AArch64，非宣称其微小增量已确证；v1仅ARM训练也在AArch64上有正向观测。

禁止单独引用：**0.846042、0.848116、0.852074、0.854402**（以及任何同类数字）。
每次引用必须同时带四项限定：①分母/同轮关系；②含重链剥离还是纯BOLT；
③训练/留出及正式/诊断；④噪声门禁状态与次序条件。不称“五轮独立”，不写等幅“吞吐提升”。
对外只说：**筛选层多轮测量方向一致，BOLT 对 LLVM 自身源码编译负载有稳定正向影响，量级待构建服务器验收。**
再补：**候选含重链与剥离；docs/20 附录 B 已实测这些中间处理的几何平均影响接近1.000，不等于严格零影响。**

## 6. Quickbuild 验收协议（实施前冻结）

### 6.1 工具链、身份与数据

A/B 混合 LLVM 各构建一次；A=`without_clang_bolt`，B=`with_clang_bolt`，同 source/spec/patch/
MLGO、普通 ninja argv、CMake、资源头/运行库、target/sysroot。若B降级普通，不能算BOLT验收候选。
普通模式、seed模式复现门禁与这里 A/B Chromium 八轮是不同试验。
冻结 worker/并发/cgroup/缓存策略、source/GN args/flag/图边与任务数量、profile/ELF SHA、脚本和统计版本。
保存 args.gn、完整 commands、.ninja_log（重试不丢弃）、总wall、cpu.stat前后、peak/events、实际cc/cxx路径及SHA。

身份调用必须落盘 rc，不能用 tee 的成功冒充检查通过。以下仅模板，不在本轮运行：

```bash
set -u -o pipefail
: "${CC_EMUL:?}" "${EXPECTED_SHA:?}" "${EXPECTED_BOLT:?}" "${EVIDENCE:?}"
set +e
./verify_toolchain_identity.sh --expected-sha256 "$EXPECTED_SHA" \
  --expect-bolt "$EXPECTED_BOLT" "$CC_EMUL" > "$EVIDENCE/identity-emul.txt" 2>&1
identity_rc=$?
set -e
printf '%s\n' "$identity_rc" > "$EVIDENCE/identity-emul.rc"
python3 - "$identity_rc" "$EVIDENCE/identity-emul.txt" <<'PYIDENTITY'
from pathlib import Path
import sys
rc=int(sys.argv[1]);body=Path(sys.argv[2]).read_text();lines=set(body.splitlines())
assert rc == 0
assert {'EXPECTED_SHA256=PASS','EXPECTED_BOLT=PASS','IDENTITY_STABILITY=PASS','EXECUTABLE=YES',
        'VERSION_EXIT=0','ARCH_MISMATCH=NO','BINFMT_REGISTRY_OVERRIDDEN=NO'} <= lines
assert {'BINFMT_DISPATCH_POSSIBLE=NO','BINFMT_DISPATCH_POSSIBLE=NAME_ONLY'} & lines
PYIDENTITY
```

身份/活性/首次编译后非计时 exec trace 必做，CC_EMUL必须指向实际/emul ELF。

### 6.2 顺序、失败传播与 A/A 中止

固定 **A0a A0b A1 B1 B2 A2 A3 B3**，配对A1/B1、A2/B2、A3/B3，共八轮Chromium构建。
执行前冻结 all_metrics 全集：build_wall、unit_compile、build_cpu、compile_memory，
以及下游独立同顺序八轮的 runtime_wall/runtime_cpu/runtime_memory/runtime_rss。
下游独立试验的A/A和后六轮也服从同一停止/资源规则，不把两个试验不同指标混成一个时间序列；
下方代码输入须由各自试验完整采集，同一指标的八值不跨试验拼接。
在尚无下游轮数据时先独立取得其A/A，完整 preflight 才可继续相关后六轮；不要用伪0或默认值占位。

对**全部指标**计算A/A d；任一**时间/CPU指标**d>0.10，中止整个验收、不启动A1；
内存也计算d，但由资源噪声门禁处理。查明环境后另建ID从头八轮，不自动等待/追加/替换坏轮。
本条替代 v2“任何指标>0.10”的表述。任一身份、功能、job、cgroup、日志完整性失败都停止。

构建适配器须等远程job最终状态，不以“成功提交请求”返回0；支持取消并确认终态。
下面检查 build/time、tee、后台wait和真实job，不吞失败：

```bash
set -u -o pipefail
: "${BUILD_ADAPTER:?}" "${ROUND:?}" "${EVIDENCE:?}" "${JOB_CGROUP:?}"
cp "$JOB_CGROUP/cpu.stat" "$EVIDENCE/cpu.before" || exit 1
set +e
/usr/bin/time -v -o "$EVIDENCE/time.txt" \
  "$BUILD_ADAPTER" --round "$ROUND" --wait --evidence "$EVIDENCE" 2>&1 | tee "$EVIDENCE/build.log"
rc=("${PIPESTATUS[@]}")
set -e
(( rc[0] == 0 && rc[1] == 0 )) || exit 1
cp "$JOB_CGROUP/cpu.stat" "$EVIDENCE/cpu.after"
cp "$JOB_CGROUP/memory.peak" "$EVIDENCE/memory.peak"
cp "$JOB_CGROUP/memory.events" "$EVIDENCE/memory.events"
python3 - "$EVIDENCE" <<'PYJOB'
import json,sys
from pathlib import Path
p=Path(sys.argv[1]);s=json.loads((p/'job-status.json').read_text())
assert s['terminal'] is True and s['state']=='SUCCEEDED' and s['exit_code']==0
for name in ['.ninja_log','args.gn','ninja-commands.txt','identity-emul.txt','identity-emul.rc']:
    assert (p/name).is_file() and (p/name).stat().st_size>0
assert int((p/'identity-emul.rc').read_text())==0
PYJOB
# 若将这整个受检作业另放后台，启动方还必须 wait "$job_pid" || exit 1。
```

每轮用新cgroup；cpu.stat第二口径取user+sys增量并覆盖accel子进程。远程worker数据而非客户端数据。
失败时适配器保留job ID并取消，取完cgroup证据再回收；取消无法确认则停止排队并报告。

### 6.3 公式、分辨力与工程容差

每指标最终 `d=max(d_AA, max(|Ai/Aj−1|，i≠j，i,j∈{1,2,3}))`。
所有有序A对都取，等价于最大A/最小A−1；只取max，不能选较小者。此公式先冻结再运行。
A/A阶段还没有A1–A3，只能用d_AA作事前检查；结束后必须再纳入A间漂移，不能提前假定为0后不复核。

入队前冻结最小可辨收益δ：建议 unit_compile=0.10、build_cpu=0.10，用户可在入队前改；
用户给出的 build_wall=0.03 建议值与 `margin=max(0.03,2d)`、`margin≥δ` 拒绝条件存在
**确定性死区**：即使d=0也拒绝。本文不私自改成别的数。
若坚持δ_wall=0.03，则结果必为 INSUFFICIENT_RESOLUTION，不能启动A/B；要开展总wall收益验收，
用户须在试验入队前明确批准 δ_wall>0.03（例如0.06）。这是待定参数，不是在运行后调门槛。
`aa_preflight.dead_zone` 明确给每个冲突指标的margin/δ。

收益规则：各自三对B/A都严格小于`1-margin`才成立，GM不盖过失败对；
总wall另分为 **成立 / 未确证 / 噪声超过可检测效应**（最终margin>0.06时第三类优先）。
最终A间漂移令margin≥δ也记分辨力不足。时间/CPU三项均成立才能称整体收益；仅编译项成立只能报告编译阶段。

资源规则：tol为已接受容差（编译peak .05；下游wall/CPU .02；下游peak/RSS .03）。
`2d>tol` → INCONCLUSIVE_NOISE；否则 `max(r)≤1+tol` **且** `GM(r)≤1.00` 才非退化。
不是“允许平均变慢2%”；内存上限也不是从ELF体积推算。INCONCLUSIVE_NOISE同样不发货，原因记环境噪声。
所有轮无OOM/新增swap、无功能失败是独立硬条件。

精确代码如下；all_metrics每项形如 `{"values":[A0a,A0b,A1,B1,B2,A2,A3,B3],"delta":0.10}`，
资源项不用delta。A/A阶段values为两项；任何指标缺失都拒绝。代码由测试直接从本文提取执行：

```python
import math
from decimal import Decimal

# Freeze these names, kinds, tolerances and each benefit delta before queuing A0a.
BENEFIT = ('build_wall', 'unit_compile', 'build_cpu')
TOL = {'compile_memory': .05, 'runtime_wall': .02, 'runtime_cpu': .02,
       'runtime_memory': .03, 'runtime_rss': .03}
TIME = set(BENEFIT) | {'runtime_wall', 'runtime_cpu'}
REQUIRED = set(BENEFIT) | set(TOL)
D = lambda value: Decimal(str(value))

def _validate(all_metrics):
    if set(all_metrics) != REQUIRED:
        raise ValueError('missing/extra metric: freeze the complete inventory')
    for name, item in all_metrics.items():
        values = item['values']
        if len(values) not in (2, 8) or any(type(v) not in (int, float) or not math.isfinite(v) or v <= 0 for v in values):
            raise ValueError('incomplete/nonpositive measurement')
        if name in BENEFIT:
            delta = item['delta']
            if type(delta) not in (int,float) or not math.isfinite(delta) or not 0 < delta < 1:
                raise ValueError('freeze a delta in (0,1) for each benefit metric')

def aa_preflight(all_metrics):
    _validate(all_metrics)
    drift = {n: abs(D(v['values'][1])/D(v['values'][0])-1) for n,v in all_metrics.items()}
    dead = {n: {'margin': float(max(D(.03),2*drift[n])), 'delta': all_metrics[n]['delta']}
            for n in BENEFIT if max(D(.03),2*drift[n]) >= D(all_metrics[n]['delta'])}
    noisy_resource = [n for n,tol in TOL.items() if 2*drift[n] > D(tol)]
    status = ('ABORT_ENVIRONMENT' if any(drift[n] > D(.10) for n in TIME)
              else 'INSUFFICIENT_RESOLUTION' if dead
              else 'INCONCLUSIVE_NOISE' if noisy_resource else 'CONTINUE')
    return {'status':status, 'd':{n:float(d) for n,d in drift.items()},
            'dead_zone':dead, 'noisy_resources':noisy_resource, 'established':False}

def _paired(all_metrics, name):
    values=all_metrics[name]['values']
    if len(values)!=8: raise ValueError('all eight rounds are required')
    a0a,a0b,a1,b1,b2,a2,a3,b3=map(D, values)
    aa=abs(a0b/a0a-1)
    baseline=[a1,a2,a3]
    between=max(abs(a/b-1) for a in baseline for b in baseline)
    d=max(aa,between)  # Never replace a large drift with the smaller one.
    ratios=[b1/a1,b2/a2,b3/a3]
    return d,ratios,math.prod(map(float,ratios))**(1/3)

def paired_gate(all_metrics, metric_name):
    pre=aa_preflight(all_metrics)  # All metrics, not only the selected one.
    if pre['status']!='CONTINUE': return pre
    if metric_name not in BENEFIT: raise ValueError('use resource_gate for resources')
    d,ratios,gm=_paired(all_metrics,metric_name)
    margin=max(D(.03),2*d)
    if metric_name=='build_wall' and margin>D(.06):
        status='NOISE_EXCEEDS_DETECTABLE_EFFECT'
    elif margin>=D(all_metrics[metric_name]['delta']): status='INSUFFICIENT_RESOLUTION'
    elif all(r < 1-margin for r in ratios): status='ESTABLISHED'
    else: status='NOT_ESTABLISHED'
    return {'status':status,'established':status=='ESTABLISHED','d':float(d),
            'margin':float(margin),'threshold':float(1-margin),
            'ratios':list(map(float,ratios)),'geomean':gm,'dead_zone':pre['dead_zone']}

def resource_gate(all_metrics, metric_name):
    pre=aa_preflight(all_metrics)
    if pre['status']!='CONTINUE': return pre
    if metric_name not in TOL: raise ValueError('unknown resource metric')
    d,ratios,gm=_paired(all_metrics,metric_name)
    tol=D(TOL[metric_name])
    if 2*d>tol: status='INCONCLUSIVE_NOISE'
    elif max(ratios)<=1+tol and math.prod(ratios)<=1: status='NONREGRESSION'
    else: status='REGRESSION_OR_NOT_CONFIRMED'
    return {'status':status,'established':status=='NONREGRESSION','d':float(d),
            'tolerance':float(tol),'ratios':list(map(float,ratios)),'geomean':gm}

def validate_identity(rc, text):
    required={'EXPECTED_SHA256=PASS','EXPECTED_BOLT=PASS','IDENTITY_STABILITY=PASS',
              'EXECUTABLE=YES','VERSION_EXIT=0','ARCH_MISMATCH=NO','BINFMT_REGISTRY_OVERRIDDEN=NO'}
    lines=set(text.splitlines())
    if rc!=0 or not required<=lines or not ({'BINFMT_DISPATCH_POSSIBLE=NO','BINFMT_DISPATCH_POSSIBLE=NAME_ONLY'} & lines):
        raise ValueError('identity query failed/incomplete/non-native')
```

## 7. 本机校准关闭与脚本协议修订

不再做本机性能校准，基准台保留用于功能/稳定性；本轮只运行单元/接口测试和最小TU活性检查。
`final_bolt_calibration_plan.json` 与启动器保持原字节，已执行预注册不改；历史FAIL/PASS均保留。

对最后一次原始JSON作只读重算（E/noise-reanalysis.json）：**ARM 39/39 编译组合跨轮负偏**，
不是评审摘要的38/39；run1最大CV5.114231%、run2为0.928355%。
v2/RPM同轮GM从0.854402到0.854986，其跨轮变化0.068292%（约0.07%）；
v1/RPM对应−0.105068%。0.07%只指前者GM的稳定度，不是所有行或所有配对误差上界。
与“会话暖机/时变性能共同漂移，配对比值相对稳定”的解释一致；没有独立频率/温度干预证据，
不能写成已经唯一证明的物理根因。loadavg>10解释**不适用于这次**（样本0，最高4.28）。
ARM先跑、AArch64后跑，FAIL/PASS与执行次序混淆，不得解释成目标本身稳定性不同。

拆分的准确表述是：**逐行判据未变，决策规则由联合判定改为各自判定**，
不是总体假阳性/通过概率都不变。它已事前提交ea7d120；结果80bc93a归档，不能倒改预注册。

本提交将 `CALIBRATION_POLICY` 升为 **compile-only-v3**，仅约束未来记录/测试，不重判旧JSON：

- 编译项决定noise_floor和timing/CV门禁，lld/ar timing/CV仍诊断；
  **任意行 retained suspect>0，整体FAIL**，含lld/ar。新增`suspect_any_row`、`suspect_diagnostic_only`布尔字段，
  后者表示诊断行存在suspect（即使编译行也有），不是“只有诊断行有”。
- 校准前检查完成状态、schema、实际协议摘要、夹具摘要、工具链集合、协议声明的负载全集、
  每项N个样本、iteration/首样本丢弃、有限合法指标，并从原始samples重新算完整summary比对。
- 对称删项、伪hash、少样本、FAILED、缺summary/伪summary一律拒绝，不能两边一起坏就PASS。
  内部一致性hash不证明真实性，外部冻结manifest仍须独立校验。
- 任务只给了“Codex补丁B”的功能清单，未附原始diff；按列出的完整性要求实现并测试，
  不声称逐字应用了未取得的补丁。

身份脚本v3：注册表错误在已知foreign架构时仍禁止执行，但不额外记exit2；
NAME_ONLY不禁原生执行；magic/mask/offset和extension实际匹配才YES；无两者为错误；
不可执行文件EXECUTABLE=NO并只读完成；SECTION_DETAIL_MATCHES为真实计数；
测试覆盖TOCTOU提示、RISC-V头、缺extra-dir/不可读目录/override、真实静态/动态/ARM/BOLT。
`--binfmt-registry-dir`仅测试，强制no-exec和OVERRIDDEN=YES；不能用于生产绕过真实注册表。

## 8. 待定、审批与恢复条件

| 项目 | 当前状态/下一步 |
| --- | --- |
| 混合补丁 | 附录A只读拟议；批准前不应用、不configure、不构建；传递接口、上游静态例外和别名要一起审 |
| .a 范围及开发接口 | runtime范围待确认；OBS反向BuildRequires/文件级消费者待审，CMake导出必须可用；无审计不发货 |
| 混合构建实测 | 新容量/磁盘/inode指纹、NEEDED、图摘要与profile自动rebind未测，不沿用全静态认证 |
| accel试包 | 完整qemu源码/armv7l生成材料/宏日志、patchelf双次确定性、去重/alias、strip防护与逐层活性待验 |
| OBS项目/快照 | 待用户给自研spec所在项目；新快照钉校验和，当前旧公开快照不替代 |
| Quickbuild参数 | δ_wall=.03与预注册floor产生死区；用户须决定是否接受不入队，或在入队前批准>.03；不得执行后调整 |
| Quickbuild资源/执行器 | 取得实际CPU/内存/并发/cgroup数据，先做最小委派job；据此触发PGO容量重估，PGO可与BOLT叠加 |
| 全平台lld/ar占比 | 待全平台日志：`.ninja_log`链接+归档边`Σ(end−start)`占**全部边时间总和**比例，与总wall另列；不把并行累计时间直接除总wall当占比 |
| 第二阶段工具 | 5%/10%为首版工程阈值；>10%考虑真实规模链接基准/lld专用profile/BOLT lld/产物字节门禁；<5%及5%–10%（含边界）默认搁置并记录 |
| 源码级调试 | update-debug-sections成本/正确性UNKNOWN，生产需求明确后单独认证，不用旧DWARF |
| 三家评审 | 本v3及本轮脚本/实验交评审；采纳设计不等于已试包/已发货，不能掩盖本表前置 |

## 附录 A：混合链接源码调查与拟议补丁（未应用）

### A.1 CMake 证据

以下行号均为未修改的工作区源码；带行号全文归档 E/source-evidence.txt。

| 文件:行号 | 只读结论 |
| --- | --- |
| llvm/llvm/cmake/modules/AddLLVM.cmake:1033–1039,1106–1112,1142–1144 | add_llvm_executable解析DISABLE_LLVM_LINK_LLVM_DYLIB；ON且未禁用才USE_SHARED；禁用时定义LLVM_BUILD_STATIC |
| 同文件:1467–1482,1514–1516 | add_llvm_tool→llvm_add_tool→add_llvm_executable转发；必须关闭统一llvm-driver形态才是独立实体 |
| 同文件:742–765 | 非component静态库用PUBLIC链接依赖，全局ON会把LLVM传播给消费者；可执行局部禁用不能删除这层 |
| llvm/clang/cmake/modules/AddClang.cmake:87–109,218–233 | Clang组件静态/对象库与shared不同；clang_target_link_libraries按CLANG_LINK_CLANG_DYLIB选择clang-cpp，没有现成的per-call禁用参数 |
| llvm/clang/tools/driver/CMakeLists.txt:42–70 | driver声明及clangBasic/CodeGen/Driver/Frontend/FrontendTool/Options/Serialization；局部普通变量OFF可覆盖仅本目录，不改全局cache |
| llvm/lld/tools/lld/CMakeLists.txt:1–37 | lld直接LLVM组件Support/TargetParser，另经lldCommon/COFF/ELF/MachO/MinGW/Wasm传递更多LLVM依赖 |
| llvm/lld/cmake/modules/AddLLD.cmake:4–13,35–55 | lld库和工具包装沿用AddLLVM；库层也必须处理传递边 |
| llvm/llvm/tools/llvm-ar/CMakeLists.txt:1–24 | ar使用LLVM组件；ranlib/lib/dlltool是同实体别名 |
| llvm/clang/tools/clang-shlib/CMakeLists.txt:6–40,51–58 | clang-cpp从组件对象与LINK_LIBRARIES收集依赖；拟议补丁保留库自身LINK_LIBRARIES的LLVM，仅按最终消费者选择接口 |
| llvm/llvm/tools/llvm-config/CMakeLists.txt:17；llvm/llvm/tools/llvm-exegesis/CMakeLists.txt:22及lib/* | 上游显式DISABLE例外；其余工具全动态不是全局开关能无条件保证的事实 |
| llvm/llvm/cmake/modules/AddLLVM.cmake:1550–1555；llvm/clang/lib/Support/CMakeLists.txt:28 | utility/support另有强制静态路径，需区分发布工具与构建工具 |

拟议补丁用最终consumer的TIZEN_STATIC_LLVM属性选择LLVM组件接口，同时保留其他consumer共享路径。
CMake官方说明单参数TARGET_PROPERTY在使用需求中按消费目标求值，接口参与传递链接；
这支持方案机制，**不替代目标版本CMake生成图/链接实测**。
来源：[CMake生成表达式](https://cmake.org/cmake/help/latest/manual/cmake-generator-expressions.7.html#target-properties)、
[INTERFACE_LINK_LIBRARIES](https://cmake.org/cmake/help/latest/prop_tgt/INTERFACE_LINK_LIBRARIES.html)。

为什么七文件：三目标局部开关 + spec默认共享；再加一个公共接口选择函数及Clang/LLD库包装两个调用。
省掉后三处会漏PUBLIC LLVM依赖。生成后必须核验完整链接命令、插件符号导出列表和NEEDED；
AddLLVM的配置期export_executable_symbols遍历对生成表达式的处理也需专项验证，不能只看顶层开关。
若当前CMake/目标无法安全按consumer区分，替代是独立静态build目录只产三个实体、动态目录产其余；
代价是重复组件构建、磁盘/缓存/身份复杂度和新容量认证，不能作为本轮偷偷构建的绕路。

### A.2 最小开发库范围提案

以下diff基于当前含三处并发数的S与f111162e源码生成，E/proposed-hybrid.patch；
仅执行 `git -C llvm apply --check ../temp/spec-v3-20260922/proposed-hybrid.patch`，未应用。
它不包含BOLT集成代码，后者必须等§0四项前置完成。archive删除范围仍待用户确认；
CMake导出缺archive的消费者问题是必须补齐的试包前置，不把此文本当已验证可发货补丁。

```diff
--- a/llvm/cmake/modules/AddLLVM.cmake
+++ b/llvm/cmake/modules/AddLLVM.cmake
@@ -1030,6 +1030,40 @@
   endif()
 endmacro()

+# Proposed Tizen hybrid linkage: keep the default shared interface, but
+# provide component dependencies to an explicitly opted-in final consumer.
+function(tizen_hybrid_llvm_interface name)
+  if(NOT TIZEN_HYBRID_LINK OR NOT LLVM_LINK_LLVM_DYLIB OR NOT TARGET ${name})
+    return()
+  endif()
+  get_target_property(kind ${name} TYPE)
+  if(NOT kind STREQUAL "STATIC_LIBRARY")
+    return()
+  endif()
+  get_target_property(iface ${name} INTERFACE_LINK_LIBRARIES)
+  if(NOT "LLVM" IN_LIST iface)
+    # Some components explicitly disable the dylib already (e.g. clangSupport).
+    return()
+  endif()
+  cmake_parse_arguments(H "" ""
+    "LINK_COMPONENTS;LINK_LIBS;DEPENDS;OBJLIBS;ADDITIONAL_HEADERS" ${ARGN})
+  llvm_map_components_to_libnames(components ${H_LINK_COMPONENTS} ${LLVM_LINK_COMPONENTS})
+  set(static_consumer "$<BOOL:$<TARGET_PROPERTY:TIZEN_STATIC_LLVM>>")
+  set(replacement "$<$<NOT:${static_consumer}>:LLVM>")
+  foreach(component IN LISTS components)
+    list(APPEND replacement "$<${static_consumer}:${component}>")
+  endforeach()
+  set(result)
+  foreach(dep IN LISTS iface)
+    if(dep STREQUAL "LLVM")
+      list(APPEND result ${replacement})
+    else()
+      list(APPEND result "${dep}")
+    endif()
+  endforeach()
+  set_property(TARGET ${name} PROPERTY INTERFACE_LINK_LIBRARIES "${result}")
+endfunction()
+
 macro(add_llvm_executable name)
   cmake_parse_arguments(ARG
     "DISABLE_LLVM_LINK_LLVM_DYLIB;IGNORE_EXTERNALIZE_DEBUGINFO;NO_INSTALL_RPATH;SUPPORT_PLUGINS;EXPORT_SYMBOLS"
--- a/clang/cmake/modules/AddClang.cmake
+++ b/clang/cmake/modules/AddClang.cmake
@@ -107,6 +107,7 @@
     set_property(GLOBAL APPEND PROPERTY CLANG_STATIC_LIBS ${name})
   endif()
   llvm_add_library(${name} ${LIBTYPE} ${ARG_UNPARSED_ARGUMENTS} ${srcs})
+  tizen_hybrid_llvm_interface(${name} ${ARGN})

   if(MSVC AND NOT CLANG_LINK_CLANG_DYLIB)
     # Make sure all consumers also turn off visibility macros so they're not
--- a/lld/cmake/modules/AddLLD.cmake
+++ b/lld/cmake/modules/AddLLD.cmake
@@ -11,6 +11,7 @@
     set(ARG_ENABLE_SHARED SHARED)
   endif()
   llvm_add_library(${name} ${ARG_ENABLE_SHARED} ${ARG_UNPARSED_ARGUMENTS})
+  tizen_hybrid_llvm_interface(${name} ${ARGN})

   if (NOT LLVM_INSTALL_TOOLCHAIN_ONLY)
     get_target_export_arg(${name} LLD export_to_lldtargets UMBRELLA lld-libraries)
--- a/clang/tools/driver/CMakeLists.txt
+++ b/clang/tools/driver/CMakeLists.txt
@@ -39,7 +39,18 @@
   endif()
 endif()

+set(tizen_static_link)
+if(TIZEN_HYBRID_LINK)
+  if(BUILD_SHARED_LIBS OR LLVM_TOOL_LLVM_DRIVER_BUILD)
+    message(FATAL_ERROR "Tizen hybrid requires component archives and separate drivers")
+  endif()
+  set(tizen_static_link DISABLE_LLVM_LINK_LLVM_DYLIB)
+  set(USE_SHARED "")
+  set(CLANG_LINK_CLANG_DYLIB OFF) # Directory-local; other clang tools keep ON.
+endif()
+
 add_clang_tool(clang
+  ${tizen_static_link}
   driver.cpp
   cc1_main.cpp
   cc1as_main.cpp
@@ -53,6 +64,10 @@
   ${CLANG_BOLT_DEPS}
   GENERATE_DRIVER
   )
+
+if(TIZEN_HYBRID_LINK)
+  set_property(TARGET clang PROPERTY TIZEN_STATIC_LLVM ON)
+endif()

 setup_host_tool(clang CLANG clang_exe clang_target)

--- a/lld/tools/lld/CMakeLists.txt
+++ b/lld/tools/lld/CMakeLists.txt
@@ -3,12 +3,26 @@
   TargetParser
   )

+set(tizen_static_link)
+if(TIZEN_HYBRID_LINK)
+  if(BUILD_SHARED_LIBS OR LLVM_TOOL_LLVM_DRIVER_BUILD)
+    message(FATAL_ERROR "Tizen hybrid requires component archives and separate drivers")
+  endif()
+  set(tizen_static_link DISABLE_LLVM_LINK_LLVM_DYLIB)
+  set(USE_SHARED "")
+endif()
+
 add_lld_tool(lld
+  ${tizen_static_link}
   lld.cpp

   SUPPORT_PLUGINS
   GENERATE_DRIVER
   )
+if(TIZEN_HYBRID_LINK)
+  set_property(TARGET lld PROPERTY TIZEN_STATIC_LLVM ON)
+endif()
+
 export_executable_symbols_for_plugins(lld)

 function(lld_target_link_libraries target type)
--- a/llvm/tools/llvm-ar/CMakeLists.txt
+++ b/llvm/tools/llvm-ar/CMakeLists.txt
@@ -11,13 +11,27 @@
   TargetParser
   )

+set(tizen_static_link)
+if(TIZEN_HYBRID_LINK)
+  if(BUILD_SHARED_LIBS OR LLVM_TOOL_LLVM_DRIVER_BUILD)
+    message(FATAL_ERROR "Tizen hybrid requires component archives and separate drivers")
+  endif()
+  set(tizen_static_link DISABLE_LLVM_LINK_LLVM_DYLIB)
+  set(USE_SHARED "")
+endif()
+
 add_llvm_tool(llvm-ar
+  ${tizen_static_link}
   llvm-ar.cpp

   DEPENDS
   intrinsics_gen
   GENERATE_DRIVER
   )
+
+if(TIZEN_HYBRID_LINK)
+  set_property(TARGET llvm-ar PROPERTY TIZEN_STATIC_LLVM ON)
+endif()

 add_llvm_tool_symlink(llvm-ranlib llvm-ar)
 add_llvm_tool_symlink(llvm-lib llvm-ar)
--- a/packaging/llvm.spec
+++ b/packaging/llvm.spec
@@ -79,14 +79,6 @@
 %description devel
 This package contains library and header files needed to develop
 new native programs that use the LLVM infrastructure.
-
-%package static-devel
-Summary: Static libraries for LLVM
-Requires: %{name} = %{version}
-
-%description static-devel
-This package contains static libraries needed to develop new
-native programs that use the LLVM infrastructure.

 %package -n libllvm
 Summary: LLVM shared libraries
@@ -256,6 +248,13 @@
 %endif
     -DCLANG_ENABLE_ARCMT=OFF \
     -DLLVM_BUILD_LLVM_DYLIB=ON \
+    -DLLVM_LINK_LLVM_DYLIB=ON \
+    -DCLANG_LINK_CLANG_DYLIB=ON \
+    -DBUILD_SHARED_LIBS=OFF \
+    -DLLVM_TOOL_LLVM_DRIVER_BUILD=OFF \
+%ifarch x86_64
+    -DTIZEN_HYBRID_LINK=ON \
+%endif
     -DCLANG_BUILD_CLANG_DYLIB=ON \
     -DLLVM_ENABLE_PROJECTS="clang;lldb;clang-tools-extra;lld;compiler-rt;openmp" \
     -DLLVM_ENABLE_PER_TARGET_RUNTIME_DIR=OFF \
@@ -391,6 +390,11 @@
 # Install the clang python bits
 mkdir -p %{buildroot}%{python3_sitelib}
 cp -a ../clang/bindings/python/clang %{buildroot}%{python3_sitelib}/
+
+# Keep build-tree archives for the selected static tools; do not publish
+# component development archives. Runtime archives need a separate scope decision.
+find %{buildroot}%{_libdir} -maxdepth 1 -type f \
+  -name '*.a' ! -name 'libarcher_static.a' -delete

 rm -rf %{buildroot}%{_libdir}/debug/*
 rm -rf %{buildroot}/usr/lib/libear/*
@@ -526,11 +530,6 @@
 %{_prefix}/bin/amdgpu-arch
 %{_prefix}/bin/nvptx-arch

-%files static-devel
-%manifest %{name}.manifest
-%defattr(-,root,root,-)
-%{_libdir}/lib*.a
-
 %files -n libllvm
 %manifest %{name}.manifest
 %defattr(-,root,root,-)
```

若明确批准**全部子包零.a**，上述install删除段应改为下列替代，另删除libomp-devel的
`%{_libdir}/libarcher_static.a`文件项（不是把它留在未归属文件区）：

```diff
- find %{buildroot}%{_libdir} -maxdepth 1 -type f \
-   -name '*.a' ! -name 'libarcher_static.a' -delete
+ find %{buildroot}%{_prefix} -name '*.a' \( -type f -o -type l \) -delete
@@
 %files -n libomp-devel
-%ifnarch %arm
-%{_libdir}/libarcher_static.a
-%endif
 %{_libdir}/cmake/openmp/FindOpenMPTarget.cmake
```

该替代会删除45个compiler-rt归档，包含builtins/sanitizer与orc运行库；必须先确认生产driver
不需要这些库或有经批准的独立供应方案。未确认即运行库兼容性BLOCKER，不在本机实施。
主提案保留runtime也必须在最终报告/包清单声明，不能声称“所有RPM零.a”已满足。

## 附录 B：归档与反向依赖调查

实际spec路径S，不用旧安装包spec替代；源码范围见§0.1。文件清单来自当前22 RPM的
`rpm -qpl`：E/llvm-static-devel-files.txt、compiler-rt-files.txt、libomp-devel-files.txt。

| 已归档primary.xml | package数 | llvm-static-devel提供者 | Requires命中 |
| --- | ---: | --- | --- |
| Base tizen-base-toolchain_20260912.061113 | 1736 | x86_64 22.1.8-1.6；armv7l -1.7；aarch64 -1.9 | 0（包名/开发归档名） |
| Unified tizen-unified-toolchain_20260814.092727 | 9607 | 无 | 0（同查询范围） |

Base primary SHA=5cf28889b7f9706281c019898e4c54e93e04c23d5b813f8f42eca03d7da16138；
Unified SHA=beba1f62d83b1ab105ae1a114c8fa6277bc037615c090cef9547489e7e22d286。
输入来自temp/snapshot-archive各快照，按包名和225个开发归档的完整路径/文件名查询；
方法E/audit_reverse_dependencies.py，结果E/reverse-dependencies.json；不重新下载/猜快照。
二进制repodata的requires不含完整BuildRequires；已归档资料无完整源码spec/文件索引和OBS建图，
**构建反向依赖及未声明的.a链接消费者 UNKNOWN**。0不能升级为删除安全结论。

在有权限的OBS机器上执行（实际API/项目/仓库/架构先由用户指定；逐相关项目/架构查，不能只查Base）：

```bash
osc -A "$OBS_API" repos "$PROJECT"
osc -A "$OBS_API" whatdependson "$PROJECT" llvm "$REPOSITORY" "$ARCH"
osc -A "$OBS_API" api "/build/$PROJECT/$REPOSITORY/$ARCH/_builddepinfo?package=llvm&view=revpkgnames"
osc -A "$OBS_API" buildinfo "$PROJECT" "$CONSUMER" "$REPOSITORY" "$ARCH" > buildinfo.xml
# 针对每个consumer检查bdep中的llvm-static-devel及其提供者，再取源码spec/链接日志核实文件级依赖。
```

参数依据本机 `/usr/lib/python3/dist-packages/osc/commandline.py:5176–5242,5344–5351`、
`osc/core.py:5632–5646`；whatdependson按**源码包llvm**反查，不把子包名当源码项目包名。
其输出也不保证涵盖跨项目隐式文件使用；继续审计消费者buildinfo、spec及链接命令。
本机尝试`osc help whatdependson`因未配置凭据在提示处EOF，未创建.oscrc、未登录；
随后只读客户端源码核实语法，没有给用户编造OBS查询成功。

## 附录 C：GNU strip / eu-strip 活性实验

输入为E16/optimized/bin/clang-22副本，SHA d6538b5ee1fdc429008b4481b651f994e354eabd55853666a0a9f0da03692e63。
原件未修改；strip工具为R1/usr/bin/strip（GNU binutils2.43）和eu-strip（elfutils0.189），
通过R1/usr/lib64/ld-linux-x86-64.so.2和同根library-path运行。命令默认strip，无额外选项，
nice15/ionice-c3/单CPU/4GiB AS/禁core；具体argv在E/liveness/commands.json。

| 对象 | strip rc | LOAD数 | entry在可执行LOAD | version rc | 最小TU rc | 判定 |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| 原BOLT（正例） | 未处理 | 5 | True | 0 | 0 | PASS |
| GNU strip副本 | 0 | 5 | True | -11（SIGSEGV） | -11 | FAIL |
| eu-strip副本 | 0 | 0 | False | 127 | 127 | FAIL |

version/最小TU都用宿主显式loader，两边一致；表中负数是Python的信号退出码（shell常见139），
127为loader无法加载；不把它混成strip本身失败。结构存在也不足以证明活性，GNU结果就是反例。
程序头/readelf、stdout/stderr、版本、commands与result.json全部在E/liveness/。
`tools/check_bolt_liveness.sh`可独立运行，输出LOAD、entry、version/compile rc和输入不变SHA；
正负测试`tools/test_check_bolt_liveness.sh`直接用本轮副本，无重新strip或BOLT。

```bash
tools/check_bolt_liveness.sh "$ELF" --loader /lib64/ld-linux-x86-64.so.2 --output "$NEW_EVIDENCE"
# 每次output须新建，不能覆盖旧结果；新executor应验证其实际loader而非硬搬宿主路径。
tools/test_check_bolt_liveness.sh "$E16/optimized/bin/clang-22" "$E/liveness/strip-clang-22" "$NEW_TEST_EVIDENCE"
```

脚本是功能烟测，不是性能基准；小TU不依赖headers，target默认armv7l可显式指定。
每次子进程有30秒超时、4GiB AS、禁core、单核；退出失败保留原始输出。结构/最小TU通过仍不替代30 TU门禁。

## 附录 D：本轮评审落实索引

编号为本轮任务条目的追踪号，不冒充三家原始编号。设计落实不代表未来构建已完成。

| 编号 | 项目 | 本轮状态/位置 |
| --- | --- | --- |
| V01 | 三项用户决策与状态备案 | 采纳；§0/§5/§7及STATUS，同commit |
| V02 | per-target混合机制/最小补丁 | 调查+七文件拟议；附录A，未应用；仅三开关不足 |
| V03 | 静态开发库移除/反向依赖 | 本机Requires审计完成，OBS BuildRequires与runtime范围待定；§0.1/附录B |
| V04 | accel混合/全静态体积 | 文件级估算完成；§1.2，压缩值明确代理模型 |
| V05 | clang输入与图摘要 | §3.2设计完成，混合实物尚无，不能保证SHA相同 |
| V06 | GNU/eu-strip活性复现 | 完成，二者退出0但副本失活；附录C |
| V07 | 独立活性脚本/正负测试 | 完成；check_bolt_liveness.sh及test脚本 |
| V08 | worker不依赖/emul manifest | §1.3明确，可信accel清单+节区+活性+trace |
| V09 | patchelf双次确定性/alias | §1.2明确列为试包必测；本轮未试包 |
| V10 | keeprsp无条件/探测/容量 | §2.1完成设计；不支持降级，A/B一致 |
| V11 | 环境/递归rsp/mtime/写出/禁eval | §2.2完成契约，未知语法降级 |
| V12 | 热缓存/16GiB/两模式认证 | §2.2；两模式待获批混合认证，不伪称已测 |
| V13 | 磁盘12GiB/成功才清理 | §2.3、§4.1枚举同步 |
| V14 | 逐编译4GiB子cgroup/父余额 | §2.3；executor委派最小job前置 |
| V15 | BOLT依赖失败→ordinary | §2.1队列SUPERSEDED_BY_ORDINARY及路径资产替代 |
| V16 | 三bcond/同job seed/普通RPM字节相同 | §2.1/§3.1；复现强门禁未验证，不能用payload替代 |
| V17 | 两级rebind/混合首次认证 | §3.2；图提取器必须先认证，不使用弱摘要 |
| V18 | LLVM各一次/Chromium八轮 | §3.2/§6明确 |
| V19 | N/M/S覆盖率/禁infer-stale | §3.3，源码行号修正:51–53 |
| V20 | 三类warning>20%/新类别 | §3.3/state，当前基线1/2804/6 |
| V21 | 普通完整复制/安装事务/回滚 | §4.2，恢复失败非零，再入先恢复 |
| V22 | pre/post_brp/finalizer/nocheck | §4.2，debug hook前alias复查 |
| V23 | 每层活性/目标find-debuginfo | §4.2–4.3，实际strip负例支持必要性 |
| V24 | 不发布static-devel新门禁 | §4.4；runtime范围未决不伪报全RPM零.a |
| V25 | 噪声参照/数字引用限定 | §5完成；明确GM口径和第二顺位 |
| V26 | worker身份rc与PASS字段 | §6.1可执行模板与测试 |
| V27 | 全指标preflight/时间d>0.10 | §6.2/代码及测试 |
| V28 | max漂移/delta/dead_zone | §6.3代码及测试；δwall=.03死区明确挂账 |
| V29 | 总wall三分/resource_gate | §6.3；工程容差、噪声不发货，测试覆盖 |
| V30 | 暖机共模/判定规则变化 | §7；更正39/39，不唯一归因物理原因 |
| V31 | 本机不再校准/v2代表性 | §5/§7；本轮没有性能运行 |
| V32 | PGO触发/lld-ar口径 | §8；5–10%默认搁置 |
| V33 | identity注册表/NAME_ONLY/extension | 脚本与新增正负例完成 |
| V34 | non-exec/节名计数/TOCTOU/override | 脚本与测试完成；override强制不执行 |
| V35 | 校准完整性/compile-only-v3/suspect | 基准台与19项测试；旧判定不重算 |
| V36 | 验收规则/模板测试与冻结文件 | test_final_bolt_calibration.py；计划和启动器不改 |

## 附录 E：测试、保护与交付边界

身份测试67项PASS；基准台19项PASS；验收规则29项PASS（含冻结历史规则）；活性原件正例/strip副本负例PASS。
验收规则测试与文档代码/补丁检查的最终原始输出见E/final-tests.log和E/validation.json。
这些是功能/协议检查，不是新校准、混合构建或OBS验收。
本轮初次身份测试的预期计数错误也保留E/identity-tests.log（/usr/bin/true本身有gnu_debuglink，
不是0个明细）；修正测试并加真实1与mock0后为E/identity-tests-v2.log，未抹除失败日志。

冻结保护：docs/20、已执行plan/启动器、gbs配置、spec和相关LLVM源码前后SHA一致；
源树既有三处并发差异不动。改动仅docs/21、STATUS和本轮工具/测试；temp原始材料忽略不提交。
本机已经关闭的性能校准不会因新校准解析器重新开放。

## 附录 F：原始证据索引

全部相对E（完整路径定义在开头）：

| 文件/目录 | 内容 |
| --- | --- |
| protected-before.json、validation.json | 保护文件前后SHA、提交范围、文档/脚本检查 |
| source-state.txt、source-evidence.txt | LLVM HEAD/既有spec差异、带行号源文件 |
| make_proposal.py、proposed-hybrid.patch | 从未改源码生成的拟议diff；只check不apply |
| audit_reverse_dependencies.py、reverse-dependencies.json、*-files.txt、osc-source.txt | 两快照反依赖、三包归档清单、OBS客户端语法依据 |
| accel-full/、accel-inventory.json、accel-extract.log、accel-rpm-files.txt | 旧55MB RPM完整解包与实际文件/别名/大小 |
| size-model.json、rpm-compression.txt | 逐模型每文件来源/字节、代理压缩算式与旧RPM参数 |
| liveness/ | 两strip命令/版本/退出码、readelf、version/最小TU结果、正负测试 |
| warning-evidence.txt、noise-reanalysis.json | 历史日志/JSON只读摘录，不重新运行或改判 |
| identity-tests*.log、bench-tests.log、final-tests.log | 实际功能测试输出 |
