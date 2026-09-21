# 20 BOLT spec 集成设计 v2、身份校验与本机诊断实验

日期：2026-09-21。本文件**完整取代 docs/18 的设计建议**；docs/18、docs/19 原文保留。
用户已解除 docs/19 的停止条件：公开快照陈旧是调查结论，不是禁止面向工作区静态 spec
设计和实验的理由。本文的设计已经展开；**本轮没有修改 spec，也没有部署到 OBS**。
只有最终验收使用的 OBS 项目及其新 Base 快照仍须用户指定，不能用旧快照冒充新构建。

对外统一表述：**筛选层多轮测量方向一致，BOLT 对 LLVM 自身源码编译负载有稳定正向影响，
量级待构建服务器验收。** 本文的本机诊断结果不作为 Chromium 或全平台收益承诺。

## 1. 生效路径与多级身份清单

### 1.1 目标、已知流水线与当前快照

直接采用用户确认的部署事实：

```text
工作区静态 LLVM spec + source/patch/MLGO
  → OBS x86_64 LLVM RPM（普通 / BOLT 两种构建）
  → qemu-accel 消费 x86_64 RPM 中安装的 ELF，并转换
  → 新 Base 镜像 / 固定快照
  → Quickbuild worker /emul/usr/bin/clang-22
  → Chromium 平台 clang 路由（_use_gbs_clang=1）
```

设计目标是工作区 `llvm/packaging/llvm.spec` 的 x86_64 静态 LLVM 形态。
`gbs_llvm.conf:9` 的公开 Base 快照 `tizen-base-toolchain_20260912.061113`
仍是旧 spec：x86_64 clang 和 accel clang 都依赖 `libLLVM.so.22.1`、
`libclang-cpp.so.22.1`，VCS 为 `8dfebafe…`，不是工作区 `f111162e…`。
这是 [docs/19 §1.2、§3](19_spec_integration_v2.md) 的实测，**只说明快照陈旧**。
新验证快照在用户确认 OBS 项目后按 repomd/primary 校验和固定，不修改当前 URL 猜测项目。

旧快照的独立调查结果保留如下，不能作为未来静态包的身份清单：

| ELF | 字节数 | SHA256 | 直接 LLVM 共享库依赖 |
| --- | ---: | --- | --- |
| 旧快照 x86_64 clang RPM | 120608 | `df5778e25058bb2746512c772483f7f40e42fe27c7e4077c1f1f03a6be6cac5c` | YES |
| 同快照 accel `/emul/usr/bin/clang-22` | 131592 | `590fa22e2859a15c3d05c46aca08958949bb0cc7ab5abf293ae8ea2f338daa1b` | YES |
| 本机静态 RPM 基线 | 139929464 | `3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c` | NO |

证据：`temp/spec-review-20260921/binary-inspection.json`、`rpm-metadata.txt`、
`*-dynamic.txt`；完整绝对路径定义见附录。这里“静态”只指 LLVM/clang 库，不指 libc 静态。

### 1.2 qemu-accel 是会改 ELF 的转换环节

沿用 [docs/19 §2.2](19_spec_integration_v2.md) 的行号证据。
`QS = temp/spec-review-20260921/source-rpm/qemu-accel-aarch64.spec`；源包的通用处理主体
与实际 armv7l accel RPM 同 VCS，完整 armv7l 生成材料及隐式 brp 展开仍未取得。

| 实际源码动作 | 证据 | 集成含义 |
| --- | --- | --- |
| 从已安装 clang/llvm 构建依赖收集二进制及 ldd 库 | QS:72、82、305–347 | 记录消费的精确 NEVRA 和文件哈希；不只记 qemu 包版本 |
| `cp -aL $binary $outfile` | QS:366–385 | 跟随软链接复制实体，别名暂时成为副本 |
| `patchelf --set-interpreter %{emul_path}$rtld` | QS:389–392 | 改 PT_INTERP；ELF SHA 可以变化 |
| 非空且以 `/` 开头的 RUNPATH 改为 emul 库目录 | QS:394–400 | `$ORIGIN/../lib64` 不走该条件；绝对 RUNPATH 必须另外留证 |
| `cmp` 识别 clang-major 相同副本，删除副本、重建软链接 | QS:619–645 | clang/clang++/triple 别名最终指向 clang-22，支持仅优化这一个实体 |
| `%fdupes`，以及 RPM/baselibs 后处理入口 | QS:587–617、682、694–705 | 必须检查最终链接类型及最终 ELF，不能假定宏不改内容 |

单 clang 方案必须在 LLVM RPM 中先保证所有 clang 别名指向或具有同一个已认证实体。
这样 accel 的复制、cmp 与软链接恢复才不会把旧副本混入新包。别名处理不是可省的清理项。
本轮 patchelf 实验见附录 C；它只验证这一个显式转换，**不替代 OBS brp/fdupes/转包试验**。

### 1.3 身份：三份 ELF 哈希、可信发布清单、worker 实际调用

第一版不改 `CLANG_VENDOR`、不改 `LLVM_VERSION_SUFFIX`，版本字符串和整数版本宏维持原值。
不引入新的 configure/版本解析兼容变量；docs/18 的 branding 建议失效。

每次发布用不同 RPM Release 区分 A/B，版本号仍为同一个 LLVM 版本。Release 只能标记
配方和请求状态，**实际是否应用 BOLT 由 manifest 和最终 ELF 决定**，不能把 BOLT 请求
降级后的包标为已应用。Release 的普通/BOLT 请求标记在所有相互精确依赖的子包保持一致，
记录 OBS 最终生成的 NEVRA，不只记录入队请求值。发布流水线在包签名权限下维护只读、版本化、签名的清单：

| 阶段 | 清单必填字段 | 检查关系 |
| --- | --- | --- |
| OBS LLVM RPM | source/spec/patch/MLGO 配置 SHA、宏、Release/NEVRA、RPM SHA、解包 ELF SHA、BOLT 工具/profile SHA、实际状态 | 先验证包签名与可信 RPM SHA，再解包核对最终 ELF；不能用 install 时的临时 SHA 代替 |
| qemu-accel | 输入 RPM/ELF SHA、qemu VCS、patchelf 版本/SHA/参数、输入输出节区摘要、输出 ELF SHA、accel RPM SHA | 跨 patchelf **不要求 SHA 相同**；要求授权转换、BOLT 关键节区保留、NEEDED 合规、语义一致 |
| Base 快照 | 固定快照 ID、repodata SHA、上述 accel RPM SHA | 禁止只记滚动 reference |
| Quickbuild worker | 快照 ID、RPM 归属、`/emul/usr/bin/clang-22` 解析路径/实际 SHA、动态段/节区、exec trace | SHA 必须等于**accel 输出**清单，不是等于原 OBS ELF；最终身份以 worker ELF 为准 |

可信清单从经认证的发布存储获取，不能取“待验证二进制旁任意文本”自证。
BOLT 节区可被复制或删除，因此不是签名；RPM 归属也不能证明文件未被替换。
`__clang_version__` 和 `--version` 在 A/B 相同是本版预期，不足以区别二者。

本轮交付脚本可脱离工作区运行，Quickbuild worker 示例：

```bash
CC_EMUL=/emul/usr/bin/clang-22
# EXPECTED_SHA 必须从可信 accel 输出发布清单取得，而非现场自算再传回。
bash verify_toolchain_identity.sh --expected-sha256 "$EXPECTED_SHA" \
  --expect-bolt present "$CC_EMUL"
bash verify_toolchain_identity.sh --expect-bolt present /emul/usr
# A 组普通包：改为 --expect-bolt absent，并使用 A 的可信 SHA。
# 只读收集外国 ELF，脚本也会自动禁止执行：
bash verify_toolchain_identity.sh --no-exec /path/to/arm/clang-22
```

脚本输出版本、SHA、Machine、`ARCH_MISMATCH`、完整 `readelf -dW`、
`NEEDED_LLVM_SHARED`、BOLT 节区/notes、RPM 查询输出/退出码。
`present` 指观察到 `.note.bolt_info`；`partial` 指只有 `.bolt.org.*`；
`absent` 指二者皆无。`.text.cold` 单独存在不能作为 BOLT 证明。
这是特征检查，不是来源或性能认证；直接 NEEDED=NO 也不递归证明所有间接依赖。

返回码：0 检查完成，1 SHA/BOLT 期望不符，2 输入/辅助工具/解析/版本查询不完整，
3 识别到 shebang wrapper（无其他错误/期望失配时）。`WRAPPER=YES` 时不执行 wrapper；须另用 trace 查最终 ELF。
RPM 无归属、查询错误或缺 rpm 均仅信息项；`--no-exec`、已知架构不匹配本身不使检查失败。
未知架构返回 2；架构不匹配即使指定 loader 也自动跳过执行，防止 binfmt/accel 混入另一文件。
依赖 Bash 4+、coreutils、awk、readelf；rpm、timeout 可选。timeout 存在时版本查询限 15 秒。

GN 已知使用平台 clang，验收仍保存 `ninja -C "$OUT" -t commands > commands.txt`，
从具体编译边提取 cc/cxx/launcher，解析 wrapper/软链接，再做 §6 的必做 exec trace。
不能仅凭 args.gn、toolchain.ninja 中变量名或第一层 ARM clang 路径认定最终执行的是哪个 ELF。

## 2. spec 的集成位置与隔离降级

本节是**后续 spec 实施契约**，不是声称本轮已有可运行的 RPM 集成补丁。
原 spec、LLVM 源码及容量脚本均未修改。下列命令和状态行为在实施时须逐项测试。
首版只改 x86_64 clang-22 实体及别名；不重写 lld、ar 或共享库。

### 2.1 条件、两套入队依赖与 build 开头断言

新增 `%bcond_with clang_bolt`，默认普通构建；`--with clang_bolt` 仅由入队预检在
profile/工具/容量认证齐备时选择。A 组显式 `--without clang_bolt`。
BOLT 工具为单独 builder 包（设计名 `llvm-bolt-tools`，版本和 SHA 固定），包含 llvm-bolt、
llvm-objcopy 和必要运行库；不在 LLVM 本次 `%build` 里临时 configure 新项目。
profile 包采用 §3 的独立 noarch 包。新包名是拟实施接口，不声称当前快照已有这些包。

入队预检先校验仓库元数据、工具/profile 包签名和 SHA：

- 普通集合：当前 spec 原有 BuildRequires（包括 spec:52 已有的 Python 3），无 profile/BOLT 依赖。
- BOLT 集合：普通集合 + 固定版本 builder tools/正确性测试资产 + 精确 profile NEVRA，仅 x86_64 且
  `_toolchain=clang` 且集成容量指纹已登记时启用。
- 缺 profile 或工具时，入队器选择普通集合，附只允许枚举值的 skip 原因。
  不让 OBS 因不存在的无条件 BuildRequires 在 `%build` 前失败。首次无 profile 产
  `FALLBACK_NO_PROFILE` 普通包，这是预期。显式 A 则记 `DISABLED_BY_REQUEST`。
- 仓库在预检后失去依赖，BOLT 排队解析失败时由入队器另起一次普通构建，保留失败 job ID
  与降级原因；绝不把未产 RPM 的 failed job 伪装成功。

在 `%build` 开头（现 `llvm/packaging/llvm.spec:170`）初始化 §4 状态，实施宏级断言：

```spec
%if ! %{defined _toolchain}
# 普通 ninja 构建继续；BOLT 请求转 FALLBACK_TOOLCHAIN_UNDEFINED。
%else
# 还必须验证展开值为 clang、目标为 x86_64，才允许 BOLT 阶段。
%endif
```

这项“硬断言”约束 BOLT 准入，不杀死普通 LLVM 构建。
证据：spec:229–236 只有 `_toolchain` 定义时才显式启用 lld/ThinLTO；x86_64 Release/targets
在 spec:239–242，docs/10 §2.2 解释分支。仍检查实际 CMakeCache 与静态 NEEDED，不能仅看宏。

### 2.2 单 clang 链接重放、strip、rewrite、替换

在原 `%build` 的 `ninja -j %{mlgo_build_jobs}` 成功之后（spec:362–363），进入**可失败的
独立阶段**。普通构建失败仍令整个任务失败；只有新增 BOLT 阶段失败才降级。
先保存 build/bin/clang-22 与 CMakeCache/build.ninja SHA；全流程不覆盖这个普通候选。

1. 从 build 目录执行 `ninja -t commands clang`，保留全文，并精确选取输出为
   `bin/clang-22` 的最终链接边；本项目已验证的精确查询为
   `ninja -t commands -s bin/clang-22`（`tools/relink_clang_for_bolt.py:68` 起）。
   断言恰好一个链接命令，输出/depfile 参数各一个，不接受陌生 framing。
   保存 cwd、环境、linker/driver SHA、rsp 原始内容/SHA、ThinLTO cache 路径/参数。
   改 ELF 输出为 `build/clang-bolt/relocs/clang-22`，depfile 改入该目录；仅追加
   `-Wl,--emit-relocs`，其他优化/ThinLTO 参数与 shell 引号（尤其 `$ORIGIN`）原样保留。
   不向 `CMAKE_EXE_LINKER_FLAGS` 全局追加 emit-relocs，不触发其他目标。
   若使用 rsp，原正常 ninja 加 `-d keeprsp` 保留响应文件（只改变保留行为，不改编译参数）；
   已完成构建缺 rsp 时 **FALLBACK_RELINK_INPUT**，不猜 rsp、也不重编整棵树。
   输入路径/响应文件内容的哈希写入 link manifest；命令解析不符也降级。
2. 将 relocs ELF 只读归档；`llvm-objcopy --strip-debug relocs/clang-22 stripped/clang-22`。
   比对全部 allocated 节区 payload 和非 debug 重定位，要求 `.rela.text`、`.symtab` 非空，
   `.rela.*` 中针对代码/数据的项保留；只允许随 debug 目标删除其 debug 重定位。
   使用 `tools/check_bolt_elf.py` 的检查规则，失败 `FALLBACK_STRIP`。
3. 校验 profile manifest 与本次输入/配置认证绑定，执行：

   ```bash
   llvm-bolt stripped/clang-22 -data "$PROFILE/merged.fdata" \
     -reorder-blocks=ext-tsp -reorder-functions=cdsort \
     -split-functions -split-all-cold -split-eh -dyno-stats \
     --thread-count=1 -stale-threshold=5 -o candidate/clang-22
   ```

   排序/拆分/dyno-stats 六项来自工作区 `llvm/bolt/README.md:212`，
   `--thread-count=1` 保持 docs/16 实测线程设置；
   `-stale-threshold=5` 是新集成的拒绝门槛（不改变排序算法），依据见 §3.3。
   保存退出码、完整 stderr/dyno-stats、候选 SHA、profile 指标。任何解析缺项、退出非零、
   超时或 OOM 均不提升候选。不在生产包构建中插桩或训练。
4. 对普通 clang 与候选编译训练 10 + 留出 10 个 ARM TU，固定资源目录/sysroot、flags、
   cwd、输出路径和 `clang-22 --driver-mode=g++`，保留 `-frecord-gcc-switches`。
   对 20 对 `.o` 逐字节 `cmp`；任一差异 `FALLBACK_CORRECTNESS` 并阻止 BOLT 版发货。
   快速身份/节区/NEEDED 校验也须通过。至此写 `APPLIED` 状态，但只在 `%install` 替换。

本项目当前训练 10 + 留出 10，共 **20 个 TU 的 BOLT 产物对照全部逐字节相同**；
这不是未来任意输入/版本正确性的形式证明，新的集成候选仍执行上述门禁。
正确性测试 corpus 作为独立固定版本 builder 测试资产依赖，包含 20 个 .ii、sidecar、
ARM sysroot/资源目录身份和训练/留出标识，不混进 profile 训练集合。
缺测试资产则 `FALLBACK_CORRECTNESS_ASSETS`，不能跳过门禁提升候选。

### 2.3 资源隔离与失败判据

原完整 LLVM 构建的 **18 GiB、4/4/1、debuginfo -j4** 门禁保持不变。
新增 relink/BOLT/工具依赖产生**新的集成指纹**；先用一次独立、明确登记为认证试验的
受限构建取得实测，再登记该指纹，不能套用旧同构放行条目。
指纹至少包含 source/spec/patch/MLGO/CMake/宏、并发、BOLT工具、profile、stage caps、
debug策略与链接命令结构。普通和集成的指纹分别保存。

生产执行器要求 cgroup v2 委派，新增阶段放在完整构建 cgroup 的**子 cgroup**，
`memory.swap.max=0`、`memory.oom.group=1`。外部控制器和普通 clang 副本在子组外。
不能在 RPM chroot 随手调用 user systemd scope：新 scope 可能成为兄弟组，绕过构建上限。
执行器先验证 `/proc/<pid>/cgroup` 的父子关系和实际 memory.max；无法证明隔离则
`FALLBACK_NO_ISOLATION`。只在开发机独立试验入口使用已验证的 user scope。

集成首轮认证试验采用以下**启动政策值**，不是声称自然峰值或保证不失败：

| 子阶段 | 子组 MemoryMax | wall timeout | 理由与失败行为 |
| --- | ---: | ---: | --- |
| 单 clang relink | 16 GiB | 20 min | 热缓存已测 9.76 GiB；给 18 GiB 父组留控制器空间。冷缓存 16.83 GiB 可能被拒绝/杀掉，允许普通包降级，不偷偷扩 cap |
| strip-debug | 6 GiB | 5 min | 已测自身约 4.30 GiB；独立运行，不与 relink/rewrite 叠加 |
| 纯 BOLT rewrite | 6 GiB | 5 min | 已测自身 3.481499 GiB；不携带 debug 更新，不做插桩 |
| 每个正确性编译 | RLIMIT_AS 4 GiB，串行 | 180 s | 复用现有 TU 协议；父组内执行 |

每 30 秒保存 free/loadavg/进程树 RSS；BOLT/linker 进程再每秒记录 VmHWM，保存
cgroup memory.peak/events 和 `/usr/bin/time -v`。宿主 MemAvailable <2 GiB 中止可选阶段；
以 trap/finally 回收整个子组和采样器、确认无残留 PID，再做普通打包。`nice -n15`、
`ionice -c3` 沿用。阶段退出非零/超时/OOM/校验不符，候选留在证据区且永不替换正常 ELF。
子组 OOM 记 `FALLBACK_OOM`；普通构建或 install 自身失败仍返回非零，不属于 BOLT 降级。

22 GiB 是 docs/16 **一次有界容量试验临时放宽的启动政策**：当时按“可用减 4”应是
21 GiB，且“低于 24 拒绝”改成“记录、不拒绝”。本设计仅在 §3 首个生产 profile 的
单次有界插桩中复用已验证入口政策，单独授权/记录，不改变完整构建门禁。
生产纯重写不依赖 22 GiB。PGO **因开发机容量暂缓**；原加法峰值模型已作废，
待服务器容量评估后重估；PGO 与 BOLT 可叠加，不再传递永久“PGO=NO”。

### 2.4 已有成本证据（不能相加为同时峰值）

| 阶段 | 已测时间 | 已测内存 | 证据及适用边界 |
| --- | --- | --- | --- |
| emit-relocs 单 clang 热缓存重链 | 227.656 s | lld VmHWM 9.760868 GiB；scope 10.451344 GiB | docs/14 重链；完整首轮冷 clang 链接曾达 16.83 GiB，不能拿热值担保冷构建 |
| strip-debug | tool wall 2.31 s；阶段 4.166983 s | MaxRSS 4507492 KiB，即 4.298679 GiB | docs/15、Q/strip/tool-time-v.txt；3.56 GB 原件变 226730672 B |
| 插桩 | tool wall 66.00 s | VmHWM 19.722076 GiB，非截断 | docs/16；只发生在 profile 自举，不是每次 RPM rewrite |
| 纯优化重写 | tool wall 21.83 s；阶段 22.271900 s | VmHWM 3.481499 GiB | docs/16；剥离输入、已有 profile；不是 update-debug 上界 |
| BOLT 工具增量准备 | configure 26.426 s；126 项 545.525 s | scope 分别 627392512 / 4907880448 B | docs/15；本设计预置 tools 包，不把该时间计为每包必付重写成本 |

这些是现有具体阶段的总成本，**相对同条件未做该阶段的“增量内存”未测**；不能从 scope
峰值减进程 VmHWM 得出可复用开销，也不能把独立阶段自然峰值相加作拒绝依据。

## 3. profile 自举、绑定、存放与重认证

### 3.1 首个生产 profile 的闭环

责任分工固定为：**项目维护者 lhmax2010** 批准 source/spec/profile 发布与重认证；
OBS 作业生成输入/包证据；本机采集执行器按冻结命令训练，失败不自动改 cap/参数。
人员交接必须更新 manifest 的 owner/reviewer，不能留下匿名 profile。

1. OBS 首次普通静态构建，不存在已认证 profile，状态 `FALLBACK_NO_PROFILE`。
   普通 job 结束但回收 build tree 前，由入队器安排独立的 `PROFILE_SEED_EXPORT` 作业，
   使用已完成的原对象/缓存按 §2 隔离重放单 clang 链接；它不要求已有 profile，也不改普通 RPM。
   该 seed-export 路径单独做容量准入，失败不重编普通包，保留 build tree 供有资源时继续。
   上传 relocs ELF、链接命令/rsp/CMake/源身份到访问受控的只读资产存储。
   这样解除“没有 profile 就无法得到首个 relocs 输入”的循环依赖。
2. 在**本开发机**下载、核对 relocs SHA，复制并 `--strip-debug`；分别保存 relocs SHA、
   stripped SHA 和代码/重定位节区摘要。不能直接把 strip 前 SHA 当实际插桩输入 SHA。
3. 独立单次插桩，MemoryMax=22 GiB、MemorySwapMax=0、thread-count=1，沿用
   docs/16 的 2 GiB 紧急中止、nice/ionice、采样/回收。运行前记录 MemAvailable 字节数
   和主要进程，低于 24 GiB记录但不自动拒绝；并非无限重试或完整构建豁免。
   输入换为此次 OBS 静态图，输出/profile 前缀为新的独占目录：

   ```bash
   systemd-run --user --scope -p MemoryMax=22G -p MemorySwapMax=0 \
     nice -n 15 ionice -c3 /usr/bin/time -v -o "$RUN/instrument-time.txt" \
     llvm-bolt "$STRIPPED" -instrument --thread-count=1 \
     -runtime-instrumentation-lib="$BOLT_RUNTIME/libbolt_rt_instr.a" \
     -instrumentation-file="$RUN/profiles/clang" \
     -instrumentation-file-append-pid \
     -instrumentation-binpath="$RUN/instrumented/clang-22" \
     -o "$RUN/instrumented/clang-22"
   ```

   这个本机 scope 命令置于 §2.3 规定的外部采样/紧急中止/回收控制器内。
   `llvm-bolt` 从已核验的工具环境解析；如需显式 loader/library-path，保留原 stage.json
   的完整前缀，只使用独立解包运行库，不向宿主安装。
   使用与已验证 BOLT tools 同构的工具/runtime archive，全部 SHA 入 manifest；各参数
   以 `temp/bolt-final-20260918/instrument/stage.json` 原 argv 为基准核对，不能仅复制选项名
   而漏 runtime/binpath/PID 后缀。插桩失败保留现场，普通包继续可用；追加资源须另评估。
4. 用现有训练 13 组：A/B/C，seed=73419、scale=1/2/2；real_tu 训练 10 个 ARM .ii。
   固定 ARM triple/sysroot/资源目录与 sidecar flags，每组一次，保存输入/flags SHA、
   运行时间、退出码、每 PID fdata；不把留出 10 个加入训练。
   `merge-fdata -o "$RUN/merged.fdata" "$RUN"/profiles/*`，每个输入须存在、非空、退出 0。
   新 OBS clang 的资源目录不能冒用本机旧 headers；为该版本冻结新的 corpus manifest。
5. 在该 stripped 输入试纯重写，满足 §3.3 和 20 TU 正确性；将 profile + manifest 打成
   独立 noarch RPM。下一次同图/已重认证构建即可应用，不能为了自举在首次 OBS 构建里循环训练。

本轮**没有执行上述新插桩或重写**。已有训练 profile 是 153887224 B，SHA
`d8b6c9146822fbe19ce0c3646d57d17e797d865100a7b0193562db6ea371c24d`；仅作为设计成本/格式样本，
不自动授权新 OBS SHA 使用。

### 3.2 分发与版本

首选独立 `noarch` RPM，例如 `llvm-bolt-profile-clang22-<profile-id>`，路径
`/usr/share/llvm-bolt-profiles/<profile-id>/{merged.fdata,manifest.json}`；包 ID 永不复用，
NEVRA、RPM SHA、解包 profile SHA 都固定。profile 不进 Source0，不扩大非 x86_64 构建依赖。
无 BOLT 分支不解析 profile/tools 包；精确依赖在入队时决定，见 §2.1。

其他方案仍有明确边界：独立有条件 SourceN 可离线归档，但约 154 MB 分发成本及源文件
缺失可能在 `%prep` 前阻断，要用两套入队配置；固定服务器路径只适合试验，必须只读、
固定内容哈希并备份，可移植性低，不作为首版生产分发。均不使用滚动 latest。

manifest 版本 `profile_schema=1`：保存 source/spec/patch SHA、MLGO 参数及模型 SHA、
CMake/宏/目标架构、relocs SHA、stripped SHA、代码/重定位摘要、BOLT tool/runtime SHA、
训练 corpus/flags/资源目录/sysroot SHA、profile SHA/bytes、命令、时间、owner/reviewer、
认证输入列表、profile 统计及正确性结果。不同构建图生成新 profile-id，不覆盖旧文件。

**任一 source/spec/patch/MLGO 配置变化触发重训申请与重新认证**。
即便只有重建时间路径导致新 ELF SHA，也必须重新认证，不能自动沿用 allowlist：
先比较代码/重定位/符号图，核对新构建身份；在独立受限试验中测旧 profile 的匹配率、
20 TU 正确性和筛选方向，维护者签署新输入 SHA 认证记录后才能复用。
若配置变化实质改变图，重新走 13 组训练。待认证期间自动普通包降级。

### 3.3 stale 与覆盖率的可达门槛

首版冻结为以下**工程准入政策**，不是上游保证或从吞吐拟合出的统计界限：

- stale 函数占比 **≤5%**：分母为有非空 profile 的 regular functions，分子为无效（含
  inferred-stale）profile functions；保持默认不启用 infer-stale，传 `-stale-threshold=5`。
- 有效 profile 函数覆盖率 **≥10%**：`valid_profile_functions / total_regular_functions`；
  用数量计算，禁止把输出四舍五入后的 15.1 当原始数据。统计缺失/分母为 0 均拒绝提升。
- 另记录 stale sample 占比与 non-simple 数，不把 non-simple 混成 stale；出现新解析警告
  类别、无法映射的输入图或工具版本漂移，要求离线重认证，不用“退出 0”替代认证。

依据：docs/16 rewrite 原始日志是 **21802 / 144032** 有 profile，约 15.137%；
另有 **378 non-simple profiled functions** 未优化。源码
`llvm/bolt/lib/Passes/BinaryPasses.cpp:1466–1469、1487–1502、1524–1564`
显示 non-simple 单列，stale 会从有效集合排除，超 stale-threshold 才失败；
默认阈值在同文件:211 起是 100%，不能依赖默认退出码约束陈旧 profile；
`llvm/bolt/lib/Profile/StaleProfileMatching.cpp:50–53` 的 infer-stale 默认关闭。
10% 给当前约 15.1% 覆盖留明确余量，5% 容许少量图变化但拒绝大面积失配。
**这两个数是首次试包门槛，尚未证明它们能保证性能**；后续变更须评审并更新 policy version。
不能把 378 当作 378 个 stale 再扣一次。parser 保留全部日志并从相应数量行交叉计算；
无 invalid 行只有在已认证工具日志格式、完整成功输出齐备时可认定 stale=0。

## 4. 跨阶段状态、别名、打包与 debuginfo

### 4.1 固定状态与事务规则

固定路径：`%{_builddir}/llvm-%{version}/build/clang-bolt/state.json`；本版本展开为
`.../BUILD/llvm-22.1.8/build/clang-bolt/state.json`。同目录下 `ordinary/`、`relocs/`、
`stripped/`、`candidate/`、`logs/` 各自独立。所有路径由 spec 展开传入，禁止扫描“最新目录”。

```json
{
  "schema": 1,
  "policy": "clang-bolt-v2",
  "requested": true,
  "status": "FALLBACK_NO_PROFILE",
  "reason": "exact profile package unavailable at queue preflight",
  "input_sha256": null,
  "ordinary_sha256": "<64 lowercase hex>",
  "candidate_sha256": null,
  "profile_sha256": null,
  "relocs_sha256": null,
  "source_spec_config_sha256": "<64 lowercase hex>",
  "profile_id": null,
  "tool_sha256": null,
  "checks": {"elf": false, "profile": false, "tu_byte_equal": false},
  "timestamp_utc": "2026-09-21T00:00:00Z"
}
```

`input_sha256` 专指实际给 BOLT 的 stripped 输入；relocs 单列，不能混用。
尖括号字段仅表示 schema 中要求的 hash，不是本轮新构建数据。
终态枚举固定为 `APPLIED`、`DISABLED_BY_REQUEST`、`FALLBACK_NO_PROFILE`、
`FALLBACK_TOOLCHAIN_UNDEFINED`、`FALLBACK_UNSUPPORTED_CONFIG`、`FALLBACK_NO_TOOLS`、
`FALLBACK_UNCERTIFIED_INPUT`、`FALLBACK_NO_ISOLATION`、`FALLBACK_RELINK_INPUT`、
`FALLBACK_RELINK`、`FALLBACK_STRIP`、`FALLBACK_PROFILE`、`FALLBACK_REWRITE`、
`FALLBACK_OOM`、`FALLBACK_TIMEOUT`、`FALLBACK_CORRECTNESS_ASSETS`、`FALLBACK_CORRECTNESS`。
内部临时态 `RUNNING` 不允许安装候选。

`%build` 初始化，再按阶段写新 JSON 临时文件，flush/fsync 后同目录原子 rename；
最后 APPLIED 只在所有门禁通过后写入。原因写结构化短字符串、原始退出/信号另存日志。
`%install` **只读验证此状态文件**：schema/字段/配置身份、候选路径不逃逸、SHA、checks。
缺失/损坏/RUNNING/未知状态一律选择已校验的普通实体，在安装清单记
`INSTALL_FALLBACK_INVALID_STATE`；不能因为状态没写完就使用目录里碰巧存在的候选。
普通实体本身丢失或 hash 改变是基础构建错误，必须非零，不伪装降级成功。

### 4.2 install 提升、别名与 check

现 `%install` 在 spec:365 起，cmake install 在:367，别名在:368–377。
先按现有逻辑安装普通构建；状态 APPLIED 才原子替换 buildroot 的 clang-22。
替换前保存普通安装实体，枚举 `%{buildroot}%{_bindir}`：

- `lstat` 区分软链接/普通文件；软链接按 **buildroot 内**解释绝对链接并检测循环/逃逸，
  不直接 `readlink -f` 跟到宿主 `/usr/bin`。保存所有最终指向 clang-22 的链接文本。
- 用 `stat` 的 device+inode 找 clang-22 的硬链接别名，记录完整集合和 nlink；
  枚举数与 nlink 不符意味着还有未定位链接，拒绝候选提升，选择普通文件。
- 先 `install -m755 candidate clang-22.new`，核对 SHA 后 rename 到 clang-22；
  原硬链接别名逐个用 `ln` 指向新 inode，软链接保留类型/文本。
  无法一次完成时回滚普通实体及整组别名；不能留下新旧 ELF 混用。
- 后验每个别名在 buildroot 内解析到同一 SHA，预期软/硬类型一致；保存 alias manifest。
  qemu 侧 `%fdupes`/cmp 后再枚举一次，预期 clang++ 等为指向 clang-22 的软链接。

**身份清单在 `%install` 最后必定创建**：
`%{buildroot}%{_datadir}/llvm/clang-bolt/manifest.json`，加入 clang 子包 `%files`。
普通/降级包也有该文件。包含原 state 的副本、安装选择、install 前后 SHA、alias清单、
所有检查状态和原因；不伪装它是 brp 后最终 hash，也不自包含循环的 RPM hash。
`%check` 只读校验清单、安装实体与别名，不生成任何 `%files` 依赖文件。
实施测试必须同时覆盖正常 check 与 `--nocheck`，两者都能产出清单完整的包。

RPM 后处理之后，由发布步骤从最终 RPM 解包生成 §1.3 外部可信 hash 清单。
brp-strip、find-debuginfo、fdupes、accel 转换后逐层保存 `readelf -SW/-nW/-dW`，
要求实际观测到 `.note.bolt_info`、输入中已有 `.bolt.org.*` 与 `.text.cold` 保留，
或按试包实测形成经过评审的允许变化规则。**现阶段不预先批准删除标记**；
试包出现任何缺失先阻止 BOLT 发货，可发布普通包，查明后再固定该转换的判据。
未来最终 worker 还执行 20 TU 等价性，不止在 build tree 里检查一次。

### 4.3 调试信息政策

首版为 **Quickbuild 验收用 BOLT 包**，走 strip-debug 输入；clang 本体无旧 DWARF，
不得将普通 clang 的 debuginfo/debuglink/build-id 对应文件假配给它。
BOLT 后地址改变，旧 DWARF 不能用于可靠源码行/变量/内联栈定位；符号表尚可辅助函数级
归因，但不等于完整崩溃分析。该限制必须写进 manifest `debug_policy=stripped-evaluation`。
普通包及其他未 BOLT 工具沿用原 debuginfo 流程，debuginfo 并发仍为 -j4。
当前 `R1/usr/lib/rpm/find-debuginfo.sh:389–399` 按 objdump 节区名筛选：有 debuglink 跳过；有 debug 才处理；
无 debug 而有 gnu.version 则输出 already stripped 并跳过。它不以 file 的 stripped 标签判定。
现有 BOLT ELF 虽因保留 symtab 被 file 报为 not stripped，但无 DWARF、有 gnu.version，
会落入这条跳过分支（只读证据 E/debuginfo-read-only.txt）。这不代表全包不生成 debuginfo，
也不代表后面的其他 brp 步骤会跳过 clang。

若生产发货要求 clang 源码级调试，首版 BOLT 不能无条件替代普通包：
先做独立 `--update-debug-sections` 试包，成功认证后改用保留 DWARF 的输入、更新调试段
再交 find-debuginfo。**该模式的自身峰值/时间为 UNKNOWN**；3.481499 GiB/21.83 s
只属于剥离输入，不能外推。所需实验固定为：相同 relocs ELF/profile/tools/排序参数，
仅增加 update-debug 并保留 DWARF；受限运行、记录 VmHWM/wall/cgroup，再对已知崩溃位置
做符号化、源码行/内联栈与 ordinary 对照，最终 RPM debuglink/build-id 一致性检查。
失败保留普通包，不关闭全包 debuginfo，不交付地址错配的调试包。
证据：`llvm/bolt/README.md:215`、`llvm/bolt/lib/Rewrite/RewriteInstance.cpp:2207、4833`，docs/18 §2.4。

### 4.4 范围与发货硬条件

首版只 BOLT clang，因为现有 profile/20 TU 正确性/筛选证据都针对它。
不把 Chromium 链接只占 0.2% 外推到普通 RPM 包，也不因此永久排除 lld/llvm-ar。
后续每个工具须独立 workload/profile/正确性/容量与包调用面认证。
139929464 B 的 RPM clang 与 215899856 B 的现有 BOLT 文件来自**不同剥离方式**，
只是现存文件之差，不能报告为发布包或并发 RAM 增长；真实并发内存按 §6 测量。

发货前还必须处理 docs/13 已知 `llvm-static-devel` GNU strip 删除 archive 符号索引问题：
在干净消费者根仅安装最终开发包，使用该包 llvm-config 的 flags 和静态组件，
编译一个调用 LLVM API 的小消费者并链接/运行，保存命令/退出码；例如 Core/Support 的
LLVMContext、Module 构造与析构。执行前用 `llvm-ar t`、`llvm-nm --print-armap` 检查索引。
最小消费者示例在已安装最终包的原生 x86_64 验收根中执行，不在本轮宿主执行：

```bash
set -euo pipefail
cat > consumer.cpp <<'CPP'
#include <llvm/IR/LLVMContext.h>
#include <llvm/IR/Module.h>
int main() { llvm::LLVMContext c; llvm::Module m("consumer", c); return m.empty() ? 0 : 1; }
CPP
# llvm-config 输出来自已核验的最终包；这里故意按其参数列表展开。
for linker in bfd lld; do
  /usr/bin/clang++ consumer.cpp -o "consumer-$linker" -fuse-ld="$linker" \
    $(/usr/bin/llvm-config --cxxflags --ldflags --link-static --libs core support --system-libs)
  "./consumer-$linker"
done
```

GNU ld/BFD 与 lld 都检查，避免某个 linker 的容忍行为掩盖索引问题。
禁止消费构建树库或临时 ranlib 后才声称包通过。失败则修复包后重新验收，或在发布清单
明确剔除 llvm-static-devel；它是硬条件，不能随 BOLT 性能包悄悄带出。

### 4.5 实施时必须通过的集成负对照

以下是后续 spec 补丁的验收用例，不冒充本轮已跑的测试：

| 注入条件 | 必须观察到的结果 |
| --- | --- |
| `_toolchain` 未定义、非 clang 或非 x86_64 | 普通构建继续；无 relink/rewrite；对应终态清单存在 |
| profile 包/文件缺失、SHA 不符、认证输入不符 | 前者队列选普通依赖或 FALLBACK_NO_PROFILE；后两者 FALLBACK_PROFILE/UNCERTIFIED_INPUT，不提升 |
| rsp 缺失、链接命令结构不同 | FALLBACK_RELINK_INPUT；不重建对象、不修改原 ninja |
| relink/strip/rewrite 退出非零、超时、子 cgroup OOM | 外部控制器存证并回收全部子进程/采样器，普通 ELF SHA 不变，产普通 RPM |
| parser 缺数、stale>5%、有效覆盖<10%、TU 任一字节不同 | 候选不可提升，按 profile/correctness 原因降级；失败证据不删除 |
| state 丢失/损坏/RUNNING、候选 SHA 改变 | install 选择已校验普通 ELF并记录安装降级；普通 ELF 自身坏则真正失败 |
| 一个硬链接别名、多级软链接、逃逸/循环链接 | 前两者正确同组替换；后两者拒绝提升，不跟随宿主文件 |
| `%check` 跳过 | 清单照常由 install 生成，RPM `%files` 完整 |
| 未认证集成指纹、22 GiB 插桩入口误传到完整构建 | 拒绝该构建启动；普通 18 GiB 路径和 cap 字节保持不变 |
| brp/accel 后缺关键节区、最终 worker hash 不符 | BOLT 发货失败；不以 install 中间 hash/“版本一致”掩盖 |

## 5. 证据口径与本轮身份脚本测试

历史数字只留作内部追踪，统一比值为**候选 wall / 表中指定分母 wall**：

| 轮次 | 负载/用途 | 分母与变量 | 噪声门禁 | 可得结论 |
| --- | --- | --- | --- | --- |
| docs/16 calibration-run1 | 训练；校准 | 同轮 RPM；含重链+剥离+BOLT | 与 run2 合计 PASS 1.595225% | 校准之一，不单列“独立正式实验” |
| docs/16 calibration-run2 | 训练；校准 | 同轮 RPM；含重链+剥离+BOLT | 同上 | 同一校准对 |
| docs/16 formal | 训练；正式 | RPM；含重链+剥离+BOLT | 前置校准 PASS | 13 编译项几何平均 0.846042；**耗时降低**15.3958%（分母 RPM，包含重链/剥离/BOLT） |
| docs/17 attempt1 run1 | 留出；诊断 | 同轮 RPM 与 stripped 分开列 | 校准对 FAIL 4.345326% | 不作验收收益 |
| docs/17 attempt1 run2 | 留出；诊断 | 同上 | 同上 | 不能当独立正式轮 |
| docs/17 attempt2 run1 | 留出；诊断 | 同轮 RPM 与 stripped 分开列 | 校准对 FAIL 6.609160% | 不作验收收益 |
| docs/17 attempt2 run2 | 留出；诊断 | 同上 | 同上 | 无后续正式轮 |

本轮补齐的 A/A 与 relocs-only 是诊断实验，详见附录，不重新训练、不重写 BOLT。
文中保留的百分比只用于内部噪声/阈值/历史口径说明；对外收益表述采用本文开头的定性句。

本轮身份脚本测试：`tools/test_verify_toolchain_identity.sh` 已入交付范围，覆盖 42 项。
真实正负对照为：现有 ARM 根 clang、docs/19 动态快照 x86_64 clang、静态 RPM clang、
现有 BOLT clang。ARM 正例不执行，recording-loader 验证没有被调用。
其余用私有 PATH mock 注入 awk/stat/readelf/uname/RPM 错误及 partial 特征；不改真实 ELF。
测试可传 `--static/--dynamic/--arm/--bolt/--loader` 指定异机 fixture，缺 fixture 明确失败。
原始输出 `E/identity-tests.log`，实测 **42/42 PASS**。完整分支与命令就在提交的测试脚本里。

## 6. Quickbuild 验收：预先冻结的操作与判据

### 6.1 A/B、身份与准备

A **写死为同 source/spec/patch/MLGO 的 `without_clang_bolt` 构建**；B 是同一配置仅开启
经认证 BOLT 集成，且 manifest=APPLIED。禁止拿旧动态快照、bundled clang18 或历史绝对
wall 当 A。两组走同一 OBS→accel→Base 流水线，各固定快照及全部 hash。
新 snapshot/OBS project 未指定是部署输入缺口，不是本设计协议缺口。
A/B 验收 builder 使用同一依赖包集合及版本（普通 A 也预置 B 的额外工具/profile，只是不调用），
固定构建路径与 SOURCE_DATE_EPOCH，并核对 CMakeCache 的非 BOLT 配置相同。
两份 Base 的差集只允许已批准的 LLVM/accel 包与身份清单；其他运行依赖必须相同。
非 clang 工具另核对代码/动态段身份；若发生未授权差异，整轮不可作为单变量验收。

构建服务器维护者在执行前提交 acceptance manifest：两组快照/包/ELF/源码/GN args/flags、
构建图 hash、构建任务分类器版本、worker 型号/内核/CPU策略、并发/内存/磁盘、缓存政策、
以下轮次顺序/统计公式/停止规则、运行测试程序与输入。入队即冻结，结果出来不改阈值。
所有轮在专用 worker 同资源配额、同 source 和 GN 图上执行；禁用 ccache/sccache，
每轮全新 output 目录保证重编：用各自干净根/容器，根内规范路径保持一致，外部归档目录
再按 round 区分；禁止 A/B flags 中混入不同的编译绝对路径。路径由 manifest 固定。
固定依赖缓存预热策略；不能交替
冷/热文件缓存并解释成编译器收益。保存宿主内存/主要进程、温度/频率/负载、cgroup limits。

必须记录：总 wall、完整构建日志、`.ninja_log`、args.gn、toolchain.ninja、
`ninja -t commands`、编译器/链接器/资源目录/flags SHA、实际编译/链接任务数量及图身份、
cgroup `cpu.stat` 和 `memory.peak/events`。ARM wrapper 与 x86_64 accel ELF分别留证：

```bash
CC_EMUL=/emul/usr/bin/clang-22
export CC_EMUL
bash verify_toolchain_identity.sh "$CC_EMUL" \
  --expected-sha256 "$EXPECTED_ACCEL_SHA" --expect-bolt "$EXPECTED_BOLT" \
  > "$EVIDENCE/identity-emul.txt" 2>&1 || exit 1
ninja -C "$OUT" -t commands > "$EVIDENCE/ninja-commands.txt" || exit 1
cp -- "$OUT/args.gn" "$EVIDENCE/args.gn" || exit 1
```

准备阶段先成功编译一条真实编译边；这次首次编译完成后，从 commands 中选该边，
在相同 cwd/env 重放一次，
输出到独立诊断目录，用 `strace -f -e trace=execve,execveat -s4096 -o exec.trace -- …`。
这是**必做的非计时实验**；完成后清理准备输出，再启动 A/A 和六轮正式构建，
不在计时构建途中插入 trace。核对最终 ELF 为清单中的
`/emul/usr/bin/clang-22`。若 trace 环境只记录 binfmt 初始 exec 不能看到替换，额外采集
编译子进程 `/proc/<pid>/exe`、maps 和 hash，必须观察到最终 x86_64 ELF，不能仅见 ARM
launcher 就签字。缺 trace 权限/证据则验收未完成；不申请本机 capability 或修改 sysctl。

### 6.2 轮次、失败传播与停止

固定先做 **A0a、A0b 一对 A/A**，再 **A1 B1 B2 A2 A3 B3**，共八次完整服务器构建。
配对固定 A1/B1、A2/B2、A3/B3；不用按快慢重排。若 AA 不稳，后六轮不启动，查明环境后
新建试验 ID 重做全部协议。六轮中任一失败终止整个验收，保留已完成轮为诊断数据。

执行模板的 `BUILD` 必须是**等待 Quickbuild job 终态的适配器**；数组参数和其脚本 SHA
冻结入 manifest，不是“提交请求成功就返回 0”的命令。适配器必须保存 job ID、每次查询、
最终状态，只有明确成功且构建产物和 `.ninja_log` 齐备返回 0；取消/超时/失败/未知均非零。
适配器收到 SIGINT/SIGTERM、日志写入失败或超时时，必须请求取消 job，并等待确认终态；
只杀本地轮询器不算终止远端构建。取消不能确认时返回非零并停止整个验收，保留 job ID。
不编造当前未取得的 Quickbuild CLI 子命令。下面的外层 shell 为可执行失败传播模板，
在实际 worker 内运行或由适配器采回对应 worker 数据，不能把提交客户端的 cpu.stat 当 job CPU：

```bash
#!/usr/bin/env bash
set -u -o pipefail
# 环境指定已审定的等待适配器、轮次参数及新建 evidence 目录；缺少任一值即失败。
: "${BUILD_ADAPTER:?}" "${ROUND:?}" "${EVIDENCE:?}" "${JOB_CGROUP:?}"
mkdir -p "$EVIDENCE" || exit 1
cp "$JOB_CGROUP/cpu.stat" "$EVIDENCE/cpu.before" || exit 1
# JOB_CGROUP 必须是这一轮新建并纳入全部 job 子进程的 cgroup，不能复用累计 memory.peak。
set +e
/usr/bin/time -v -o "$EVIDENCE/time.txt" \
  "$BUILD_ADAPTER" --round "$ROUND" --wait --evidence "$EVIDENCE" \
  2>&1 | tee "$EVIDENCE/build.log"
rc=("${PIPESTATUS[@]}")
set -e
cp "$JOB_CGROUP/cpu.stat" "$EVIDENCE/cpu.after"
cp "$JOB_CGROUP/memory.peak" "$EVIDENCE/memory.peak"
cp "$JOB_CGROUP/memory.events" "$EVIDENCE/memory.events"
(( rc[0] == 0 && rc[1] == 0 )) || exit 1
# job-status.json 由适配器按终态生成；还需拒绝遗漏产物的假成功。
python3 - "$EVIDENCE" <<'PY'
import json,pathlib,sys
p=pathlib.Path(sys.argv[1]);s=json.loads((p/'job-status.json').read_text())
if not (s['terminal'] is True and s['state']=='SUCCEEDED' and s['exit_code']==0):
    raise SystemExit('Quickbuild job did not succeed')
for name in ['.ninja_log','args.gn','ninja-commands.txt','identity-emul.txt']:
    if not ((p/name).is_file() and (p/name).stat().st_size>0):
        raise SystemExit('Missing acceptance evidence: '+name)
PY
```

若外层另放后台，必须 `wait "$job_pid"` 检查真实状态，不能只查 `tee` 或 `kill -0`。
适配器协调保存 cgroup 数据后才允许作业 cgroup 回收；这里的 time 总 wall 是端到端等待，
另外从服务器 job 记录真实 build-start/end，**排队时间不计为构建收益**。
内存 OOM、身份变化、输入图/任务数不等、缓存协议不符、缺失日志或 correctness 差异都停止。
无关系统服务入侵资源隔离也终止并标环境无效；不挑某个快样本重跑替换。

### 6.3 指标、区间、量化资源红线

主指标同时报告端到端有效 build wall 和单位编译成本：从完整 `.ninja_log` 按冻结的
编译边清单求 `Σ(end-start)/编译任务数`，保持并行度/任务集合一致。这是任务 wall
均值，不等于 CPU time；所有重试/重复边必须计入并单列，不能仅取最后一条掩盖失败。
`.ninja_log` 单位毫秒、不同阶段分类由实际 commands 固定，不凭文件后缀混入归档/链接。
第二口径为同一新 cgroup 的
`Δcpu.stat(user_usec + system_usec)`，覆盖真实 accel 子进程，另报每任务 CPU 成本。
跨机器/跨输入图/跨缓存策略绝对值不可比；本机训练/留出数字不能代替这些服务器指标。

AA 环境门槛冻结为：对 build wall、单位编译成本、CPU总成本、memory.peak，
`abs(A0b/A0a-1) ≤ 3%`，否则本次验收停止。3%沿用项目筛选层噪声容忍目标，
不是声称一次AA能估计完整置信分布；后续统计还保留实测 AA 误差带。

三个配对各算 `r_i=B_i/A_i`、`x_i=ln(r_i)`；点估计 `exp(mean(x))`，
95%区间 `exp(mean(x) ± 4.302653*sd(x,ddof=1)/sqrt(3))`（df=2）。
额外以同指标 AA 漂移 `d=abs(ln(A0b/A0a))` 向两端各扩 d，作为保守环境误差带。
这是预定小样本估计；若配对波动/趋势破坏解释，标“不确定”，不得缩小区间或追加最快轮。
本次只看一次冻结的全部数据；不按中间结果提前宣称成功，不以不断加轮直到显著作停止规则。

收益成立必须**同时**满足：

| 指标 | 预定门槛（B/A，分母为同轮配对 A） | 来源与误差处理 |
| --- | --- | --- |
| 单位编译 wall | 加 AA 误差的区间上界 <1.00 | 对目标任务的方向性收益；不是预先指定收益百分比 |
| cgroup user+sys CPU成本 | 加 AA 误差的区间上界 <1.00 | 独立 CPU 口径防止仅受墙钟环境影响 |
| 完整 build wall | 加 AA 误差的区间上界 <1.00 | Quickbuild 最终吞吐目标；若只单位成本通过而总 wall 未通过，仅能称编译阶段成立、整包仍不确定 |
| 编译构建期 memory.peak | 加 AA 误差的区间上界 ≤1.05，且任何轮无 OOM/新增swap | **+5% 是工程非退化容忍上限**，不是文件体积推算；大于此值不批准推广 |
| 下游产物运行 wall/CPU | 固定工作负载的配对区间上界 ≤1.02 | **+2% 工程回归预算**，不是已有实测；需独立运行验收 |
| 下游产物运行峰值内存 | 配对区间上界 ≤1.03，且每次无 OOM/新增swap | **+3% 工程回归预算**；RSS与cgroup分别报告，不互相替代 |

阈值依据是首版工程风险预算：编译器布局变化允许有限 resident working set 变化，
故编译内存设 5%；生成代码预期不变，下游运行设置更紧的 2% 时间/CPU、3% 内存上限。
服务器数据尚未取得，不能把这些政策数写成实测推导值；实测误差按上述 AA 扩区间处理，
不因误差大就放宽预算。

下游运行验收固定使用现有平台回归套件的确定输入/命令清单（以 manifest 的文件 SHA 冻结），
涵盖 Chromium 启动、既定页面加载/交互与退出，禁止测试中更换网页内容/网络负载。
先独立 AA 20 对、再 A/B 20 对，顺序交替 AB/BA；每对同机/缓存/隔离条件，
测运行 wall、CPU、cgrouppeak/RSS、功能测试退出状态；点估计按 logratio，
95% t 区间 df=19 临界 2.093024，再以 AA 的 logratio 区间最大绝对端点扩误差。
未能压下测量误差使上界跨阈值时结论是**不确定，不能放行**，不把噪声从观察回归中扣掉。
任一功能不正确立即失败。数据未取得前不给“下游资源不退化”的承诺。
20 对是固定执行量，2/3/5% 是本版明确工程容忍值；项目负责人在执行前批准 manifest 后
才成为发布门禁，执行后不得为结果好看改变这些数。

服务器发货批准还要求：§4.4 静态开发包门禁、最终 RPM/accel/worker 20 TU 字节门禁、
正确 debug 策略、无未认证后处理。上述本轮仅设计，**没有在本机构建 Chromium**。

## 附录 A：本轮实验协议与 A/A 零对照

以下路径全部以实际本机路径为准，原始大文件不提交：

```text
W   = /home/linhao/Toolchain/development/llvm-optimize
E   = W/temp/spec-integration-v2-20260921
D   = W/temp/bench_results/spec-integration-v2-20260921
TC  = W/temp/toolchain-baseline/usr
R1  = W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0
S   = /home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0
Q   = W/temp/bolt-measurement-20260918/run
E16 = W/temp/bolt-final-20260918
```

实验在现有开发机环境运行，非专用空载服务器；轻量文档工作与身份测试期间基准仍运行，
身份测试显式绑 CPU 0，基准绑 CPU 2。三项基准/编译实验本身串行，不与另一重负载重叠；
后台进程见 host-before 原始记录，不能据此假定整轮环境零干扰。

两个实验均直接使用未修改的 `tools/bench_toolchain.py`，`--calibrate` 各跑两次完整
同轮交错测量。真实输入为原训练 10 个 .ii，合成 seed=73419、scale=1/2/2；没有采新
profile，也没有把留出集混入训练目录。CPU 2、ASLR off、N=5 丢首次、loadavg 阈值 10、
ARM triple、同一 S sysroot、同一 `TC/lib64/clang/22` 资源目录，逐编译进程 4 GiB AS。
夹具由每个实验的第一个工具链（RPM 基线）生成，64 objects，三者共用；lld 每样本
4096 次、ar 1024 次，报告按单调用归一化，不能把这两类短调用与编译时间直接混加。
loader 均为 `/lib64/ld-linux-x86-64.so.2`，libxml2 独立库目录
`W/temp/toolchain-runtime-baseline/libxml2/usr/lib64`，没有安装到宿主。

以 A/A 命令为例，完整绝对 argv 在 `D/aa/launch.json`：

```bash
nice -n 15 ionice -c3 python3 tools/bench_toolchain.py \
  --toolchain "rpm-a=$E/toolchains/rpm-a" \
  --loader rpm-a=/lib64/ld-linux-x86-64.so.2 \
  --library-path "rpm-a=$W/temp/toolchain-runtime-baseline/libxml2/usr/lib64" \
  --toolchain "rpm-b=$E/toolchains/rpm-b" \
  --loader rpm-b=/lib64/ld-linux-x86-64.so.2 \
  --library-path "rpm-b=$W/temp/toolchain-runtime-baseline/libxml2/usr/lib64" \
  --sysroot "$S" --resource-dir "$TC/lib64/clang/22" \
  --real-tu-dir "$W/tools/bench_inputs/real_tu" --runs 5 --seed 73419 --scales 1 2 2 \
  --cpus 2 --aslr off --load-threshold 10 --shards 64 \
  --link-repeats 4096 --archive-repeats 1024 --work-dir /dev/shm \
  --output "$D/aa/calibration" --calibrate
```

A/A 两个名字的 clang SHA 都是 `3283505c…`；两套 lld/ar 也指向同一套基线文件。
本轮不追着噪声门禁重跑，不因失败改协议；原有门禁为各工具/负载跨轮 wall 中位数差
≤3%、每轮 CV≤3%、无保留的高负载可疑样本，见 `tools/bench_toolchain.py:454–473`。

**实测状态：完整执行，校准 FAIL；仅诊断数据。** 最大跨轮噪声底 **3.846399%**，
分母为同工具链同项目 run1 的 wall 中位数。两轮均无高负载保留样本；失败项是
`rpm-a/ld.lld` 跨轮 +3.170433%、`rpm-a/llvm-ar` run2 CV=3.291540%、
`rpm-b/llvm-ar` 跨轮 +3.846399% 且 run2 CV=3.374567%。
**26 个编译组合全部满足原门禁，但整体不能标 PASS。** 没有追加正式轮或改参数重跑。

运行于 2026-09-21 17:13:33–17:46:40 +08:00，总 wall 1987.139 s。
启动时 nproc=20，MemAvailable=23163789312 B（free -b），swap used=0；
完整 `/proc/meminfo` 和主要进程 RSS 在 `D/aa/host-before.txt`。

| 轮 | 完整轮耗时 s | 13编译项 GM(rpm-b/rpm-a) | 最大CV | 全命令峰值RSS KiB | 临时产物回收 |
| --- | ---: | ---: | ---: | ---: | --- |
| 1 | 981.731 | 1.002369 | 2.235681% | 1188744 | 是 |
| 2 | 996.614 | 0.998587 | 3.374567% | 1188744 | 是 |

两名称同轮比较接近 1；同一名称跨轮的 13 编译项几何平均 run2/run1 则分别为
**rpm-a 1.013230、rpm-b 1.009407**。
这说明同轮配对和跨轮漂移是两种量，不能拿其中一个替代另一个；A/A 没有任何真实优化收益。

| 项目 | run1 rpm-b/rpm-a | run2 rpm-b/rpm-a |
| --- | ---: | ---: |
| A | 1.013396 | 1.005883 |
| B | 1.004104 | 1.003839 |
| C | 0.991012 | 0.997686 |
| real_llvm_arm_ARMISelLowering | 1.000628 | 1.003596 |
| real_llvm_arm_ARMTargetTransformInfo | 1.006684 | 0.994017 |
| real_llvm_codegen_MachinePipeliner | 1.003341 | 1.005261 |
| real_llvm_codegen_SelectionDAG | 1.012504 | 0.996152 |
| real_llvm_mc_AsmParser | 0.993482 | 0.996033 |
| real_llvm_mc_MasmParser | 1.001812 | 0.994571 |
| real_llvm_sema_SemaExprCXX | 1.004000 | 0.994150 |
| real_llvm_sema_SemaStmt | 0.997019 | 0.999978 |
| real_llvm_transforms_Attributor | 0.998928 | 0.996680 |
| real_llvm_transforms_WholeProgramDevirt | 1.004138 | 0.993906 |
| ld.lld | 1.018203 | 0.998483 |
| llvm-ar | 0.989662 | 1.014436 |

两轮协议 SHA 相同：`ee895ba89baab38bc03d421ef8dc6f10836f40db763e230949b3aa7eb255a2a9`；
共享夹具 SHA 相同：`30acab6c36503bcf53f5ad6467d17a58ede7f0205f95f68dedd1125494a9096a`。
每样本 wall/user/sys/RSS、前后 loadavg、弃用标志、全部命令在原始 JSON/raw 中；
这里不将短工具的归一化时间混入 13 编译项几何均值。

## 附录 B：RPM / relocs-only / stripped 同轮交错

三者顺序固定为 `rpm-baseline`、`relocs-only`、`stripped`；只改变 clang ELF，lld/ar
仍全部用相同基线，资源目录、输入、夹具和协议与附录 A 相同。

| 标签 | 实际 ELF | 字节数 | SHA256 |
| --- | --- | ---: | --- |
| rpm-baseline | TC/bin/clang-22 | 139929464 | `3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c` |
| relocs-only | R1/home/abuild/bolt-relocs-6a5e8e81bccb/clang-22 | 3560474952 | `6bfc85a8cce9952c4bcbea1a4ea169fb6199c379c18527df7d349f375e52caaf` |
| stripped | Q/stripped/bin/clang-22 | 226730672 | `eccfb075bc3b2a6ca2bda5a2a6e68f6a29ba48b5586cb603f4b46080f656013e` |

`E/run_measurement.py relocs` 保存了 `D/relocs/launch.json` 的完整三个工具链 argv。
本次只是运行已存在的文件，没有重链、strip 或 BOLT。原 3.56 GB relocs 文件不放进 Git。

**因果边界：** stripped/relocs-only 对照同一次重链产物经过 `objcopy --strip-debug`
这一步的影响；relocs-only/RPM 还包含重定位保留、debug 是否保留和 RPM 后处理差异，
不能称为完全纯净的“重链单变量”。stripped/RPM 则是此前 BOLT 对照链条里的中间影响。
本轮没有再引入未经打包的 ordinary-build ELF，所以不虚称完全分离了每一种后处理。
这些比值都不包含 BOLT 重写本身，不能用来直接宣布新的 BOLT 净收益。

**实测：两轮完整执行；原 3% 校准门禁 PASS，最大跨轮差 1.986133%。**
分母为同工具链同项目的 run1 wall 中位数。结果按诊断实验记录；没有追加正式轮或改协议重试。
总阶段 wall 2959.254 s，开始 2026-09-21T17:47:14.631918+08:00，结束 2026-09-21T18:36:33.907802+08:00。
未剥离 ELF 的全部 13 个编译项在 4 GiB AS 下完成；未触发容量失败，未放宽限制。

| 轮 | 完整轮 wall s | 全命令峰值RSS KiB | 最大CV | 可疑保留样本 | 夹具/产物回收 |
| --- | ---: | ---: | ---: | ---: | --- |
| 1 | 1487.877 | 1188744 | 2.409033% | 0 | 是 |
| 2 | 1466.421 | 1527232 | 2.207152% | 0 | 是 |

全部组合通过既定门禁；本轮仍只回答中间处理对照，不把它当作新的 BOLT/Chromium 验收。

**第 1 轮**；P=RPM、R=未剥离 relocs、S=stripped。所有时间为保留样本 wall 中位数，单位秒。

| 项目 | P s | R s | S s | R/P | S/R | S/P |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 8.709521 | 8.685715 | 8.710959 | 0.997267 | 1.002906 | 1.000165 |
| B | 2.247708 | 2.246714 | 2.249905 | 0.999558 | 1.001420 | 1.000978 |
| C | 6.102872 | 6.109335 | 6.099358 | 1.001059 | 0.998367 | 0.999424 |
| real_llvm_arm_ARMISelLowering | 8.448699 | 8.451076 | 8.470505 | 1.000281 | 1.002299 | 1.002581 |
| real_llvm_arm_ARMTargetTransformInfo | 4.856711 | 4.864947 | 4.873088 | 1.001696 | 1.001673 | 1.003372 |
| real_llvm_codegen_MachinePipeliner | 6.280749 | 6.238403 | 6.258385 | 0.993258 | 1.003203 | 0.996439 |
| real_llvm_codegen_SelectionDAG | 6.863933 | 6.905758 | 6.904412 | 1.006093 | 0.999805 | 1.005897 |
| real_llvm_mc_AsmParser | 2.707115 | 2.703586 | 2.709994 | 0.998696 | 1.002370 | 1.001064 |
| real_llvm_mc_MasmParser | 3.377119 | 3.378903 | 3.361269 | 1.000529 | 0.994781 | 0.995307 |
| real_llvm_sema_SemaExprCXX | 6.186734 | 6.199682 | 6.180177 | 1.002093 | 0.996854 | 0.998940 |
| real_llvm_sema_SemaStmt | 5.927204 | 5.933599 | 5.933912 | 1.001079 | 1.000053 | 1.001132 |
| real_llvm_transforms_Attributor | 6.382931 | 6.358013 | 6.390334 | 0.996096 | 1.005083 | 1.001160 |
| real_llvm_transforms_WholeProgramDevirt | 5.824647 | 5.813721 | 5.844023 | 0.998124 | 1.005212 | 1.003326 |
| ld.lld | 0.004912 | 0.004897 | 0.004892 | 0.996794 | 0.999070 | 0.995867 |
| llvm-ar | 0.002418 | 0.002400 | 0.002412 | 0.992554 | 1.004706 | 0.997225 |
| **13编译项几何平均** | — | — | — | **0.999675** | **1.001075** | **1.000749** |

**第 2 轮**；P=RPM、R=未剥离 relocs、S=stripped。所有时间为保留样本 wall 中位数，单位秒。

| 项目 | P s | R s | S s | R/P | S/R | S/P |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 8.647239 | 8.513205 | 8.548472 | 0.984500 | 1.004143 | 0.988578 |
| B | 2.228717 | 2.228773 | 2.237813 | 1.000025 | 1.004056 | 1.004082 |
| C | 5.993873 | 5.996947 | 6.000816 | 1.000513 | 1.000645 | 1.001158 |
| real_llvm_arm_ARMISelLowering | 8.373060 | 8.379551 | 8.354411 | 1.000775 | 0.997000 | 0.997773 |
| real_llvm_arm_ARMTargetTransformInfo | 4.802115 | 4.815698 | 4.798379 | 1.002829 | 0.996404 | 0.999222 |
| real_llvm_codegen_MachinePipeliner | 6.220325 | 6.210082 | 6.207114 | 0.998353 | 0.999522 | 0.997876 |
| real_llvm_codegen_SelectionDAG | 6.912292 | 6.885806 | 6.880226 | 0.996168 | 0.999190 | 0.995361 |
| real_llvm_mc_AsmParser | 2.714915 | 2.678459 | 2.698820 | 0.986572 | 1.007602 | 0.994071 |
| real_llvm_mc_MasmParser | 3.349645 | 3.343741 | 3.344618 | 0.998237 | 1.000262 | 0.998499 |
| real_llvm_sema_SemaExprCXX | 6.064812 | 6.085821 | 6.069399 | 1.003464 | 0.997302 | 1.000756 |
| real_llvm_sema_SemaStmt | 5.865169 | 5.840841 | 5.868172 | 0.995852 | 1.004679 | 1.000512 |
| real_llvm_transforms_Attributor | 6.308579 | 6.310785 | 6.303953 | 1.000350 | 0.998917 | 0.999267 |
| real_llvm_transforms_WholeProgramDevirt | 5.786698 | 5.761700 | 5.767640 | 0.995680 | 1.001031 | 0.996707 |
| ld.lld | 0.004840 | 0.004830 | 0.004838 | 0.997995 | 1.001611 | 0.999604 |
| llvm-ar | 0.002393 | 0.002371 | 0.002368 | 0.990821 | 0.998466 | 0.989300 |
| **13编译项几何平均** | — | — | — | **0.997163** | **1.000822** | **0.997983** |

两轮夹具 SHA：`30acab6c36503bcf53f5ad6467d17a58ede7f0205f95f68dedd1125494a9096a`；协议 SHA：`15597c454b95b54397ea03ef54c09f8f8194a8ab0ad6a61bf9a77752d0da597a`。
两轮各项 user/sys/RSS/最小值/标准差及所有 sample 详见 D/relocs 的 JSON，未用历史测量当分母。

两轮的 13 编译项几何平均都接近 1，未观察到可稳定分辨的大幅中间处理效应。
这不等于证明精确零影响；也不能用本轮 S/P 去除历史 docs/16 的 B/P，跨轮反算所谓
纯 BOLT 收益。A/A 的失败与本三方校准的通过都保留，分别属于各自时段和协议标签。
对外仍使用本文开头的定性口径，最终量级由服务器验收。

## 附录 C：patchelf 对已有 BOLT ELF 副本的影响

宿主 PATH 没有 patchelf，但实际存在 `R1/usr/bin/patchelf`，通过宿主 loader 查询为
**patchelf 0.16.1**。使用该现有工具，没有安装软件或修改原 BOLT 文件。
输入是 `E16/optimized/bin/clang-22` 的复制件 `E/patchelf/bin/clang-22`。
仅执行与 QS:389–392 对应的解释器转换，命令如下（绝对 argv、退出码及 time-v 输出见
`E/patchelf/commands.json`、`patch.txt`）：

```bash
nice -n 15 ionice -c3 taskset -c 2 prlimit --as=4294967296 -- /usr/bin/time -v \
  /lib64/ld-linux-x86-64.so.2 "$R1/usr/bin/patchelf" \
  --set-interpreter /emul/usr/lib64/ld-linux-x86-64.so.2 \
  "$E/patchelf/bin/clang-22"
```

处理前后分别保留完整 `readelf -SW/-nW/-lW`、每节 type/flags/address/size/payload SHA、
整个 ELF SHA。关键节区保留判据为 name/type/flags/size/payload SHA 一致；地址等元数据
变化另行列出，不把合法搬移 note 地址冒充 payload 损坏。

三个 TU 固定选 ARMISelLowering、SemaExprCXX、Attributor，分别覆盖 ARM 后端、clang
语义分析、LLVM Transforms。使用 `tools/verify_compiler_outputs.py`，两边都以
`clang-22 --driver-mode=g++`、同资源目录/sysroot/sidecar/cwd/output 编译，完整 `.o` cmp，
不跳过 `.GCC.command.line`。

本机编译对照显式用**同一宿主 loader**运行原版及 patched 副本，绕过被改的 PT_INTERP；
因此它证明节区保留及该运行环境下 codegen 一致，**不证明目标 `/emul` loader/库实际部署
正确**。后者仍须在 worker 的必做 exec trace 与最终 TU 门禁验证。相对 RUNPATH 未走
QS 的绝对路径改写分支；该实验也不覆盖隐式 brp-strip/fdupes/baselibs。

**节区门禁 PASS；三个 TU 的完整 .o 逐字节 PASS。**

| 项目 | 处理前 | 处理后 |
| --- | --- | --- |
| ELF 字节数 | 215899856 | 217466016 |
| SHA256 | `d6538b5ee1fdc429008b4481b651f994e354eabd55853666a0a9f0da03692e63` | `494d73054c61a237c49a5d8100e6398f363270c7ae2ae141800c51f48d97deff` |
| PT_INTERP | `/lib64/ld-linux-x86-64.so.2` | `/emul/usr/lib64/ld-linux-x86-64.so.2` |

patchelf 自身 `/usr/bin/time -v`：wall **0:00.64**，MaxRSS **427940 KiB**，退出 0。

| BOLT 关键节区 | 字节数 | type/flags/size/payload SHA | address 等元数据也相同 |
| --- | ---: | --- | --- |
| `.bolt.org.rodata` | 19674176 | PASS | 是 |
| `.bolt.org.eh_frame` | 7824880 | PASS | 是 |
| `.bolt.org.eh_frame_hdr` | 1154852 | PASS | 是 |
| `.bolt.org.text` | 95419023 | PASS | 是 |
| `.text.cold` | 12449809 | PASS | 是 |
| `.note.bolt_info` | 672 | PASS | 是 |

完整 readelf -nW 输出（含命令行）逐字节相同：**否，仅两个 note 的显示顺序改变**：
ABI-tag 从 BOLT note 之前移到之后；两个 note 的 payload SHA 均未改变。
ABI-tag 的地址确有移动，BOLT note 地址/内容不变。完整 diff 在 `E/patchelf/notes.diff`。
节区摘要中发生 payload/元数据变化的项：`.interp`, `.note.ABI-tag`, `.dynsym`, `.dynamic`, `.symtab`。
程序头/节区表位置等完整差异见 before/after 原始输出；不能把整体 SHA 改变误判为编译语义改变。

| TU | 两边共同的 .o SHA256（cmp 另已执行） | 结果 |
| --- | --- | --- |
| real_llvm_arm_ARMISelLowering | `8fda7bed1e354d2d30c03aadd34edd826d442d57d32a96ea8886fc70869adaac` | PASS |
| real_llvm_sema_SemaExprCXX | `f2322722b4eb22bdb1892829101a3ee8993e43f21975c711c83954b5daff8e5e` | PASS |
| real_llvm_transforms_Attributor | `466f9d4333819496d55a1e6012d534aaf95417ecf7d33e7104c58b110979a490` | PASS |

三个输入及 flags 的 hash、6 次编译的 wall/user/sys/RSS、两份 .o 和 cmp 退出码在
`E/patchelf-equality/result.json` 与 raw/；汇总另存 `D/patchelf.json`。
本实验没有性能/噪声门禁：它检验转换与字节一致性，**3% 门禁不适用**。

## 附录 D：R01–R22 最终处置与证据

编号沿用 docs/19 的合并追踪编号，不声称等于三家原始评审编号。“采纳”区分设计契约、
本轮代码/实验与未来试包验收；所有请求的本轮实现完成后才标完成，不把未来 OBS 验收
说成已完成。

| 严重度 | 编号 | 最终处置 | 本文/交付依据 |
| --- | --- | --- | --- |
| 阻塞 | R01 | 采纳；停止门禁已按用户最新指令解除 | §1 完整流水线、陈旧快照、多级 hash；最终新快照待 OBS 项目确定 |
| 高 | R02 | 采纳；完整设计 | §2 单 clang 重放、rsp/cwd、_toolchain 准入、隔离失败降级 |
| 高 | R03 | 采纳；首版不改 branding | §1.3 Release+可信清单+节区+worker 实际路径 |
| 高 | R04 | 采纳；自举与认证流程已定 | §3 本机有界 22 GiB、13 训练组、维护者责任、5% stale/10% coverage、双输入 SHA |
| 高 | R05 | 采纳；独立 noarch RPM | §2.1、§3.2 两套入队依赖、无 profile 预期普通包 |
| 高 | R06 | 采纳；固定状态/安装清单 | §4.1–4.2 原子 JSON、build 写/install 读/check 只读；缺损 fail-open |
| 高 | R07 | 采纳；别名事务与转换门禁 | §1.2、§4.2 软硬链接与 brp；附录 C 实测 patchelf；完整试包仍是发货条件 |
| 高 | R08 | 采纳；容量指纹与例外隔离 | §2.3 新指纹先认证；22 GiB 不泄漏完整 18 GiB 构建门禁 |
| 高 | R10 | 采纳；口径已统一 | §5 逐轮正式/诊断、训练/留出、分母；20 TU 与文件体积差边界 |
| 高 | R11 | 采纳；完整验收模板 | §6 固定八轮、配对/区间/停止、CPU第二口径、exec trace、5/2/3%资源预算 |
| 高 | R12 | 采纳；发货硬条件 | §4.4 消费者静态链接验收或剔除 llvm-static-devel，未冒称已修复 |
| 高 | R13 | 采纳；脚本/实机测试完成 | Machine/uname、真实 ARM 正例、自动 no-exec |
| 高 | R14 | 采纳；脚本/实机测试完成 | 完整动态段与 NEEDED，动态快照 YES/静态基线 NO |
| 高 | R15 | 采纳；脚本/测试完成 | expect-bolt 三态及失配非零 |
| 高 | R16 | 采纳；脚本/测试完成 | RPM 仅信息、WRAPPER=YES/exit3，不执行 wrapper |
| 高 | R17 | 采纳；脚本/故障注入完成 | awk/stat/readelf/uname 错误 UNKNOWN/exit2 |
| 高 | R18 | 采纳；脚本/测试完成 | -x 检查，不可执行输入退出2 |
| 高 | R20 | 采纳；测试代码随本轮推送 | 42/42 PASS，真实正负 ELF 与私有 PATH 故障注入 |
| 中 | R09 | 采纳；PGO 口径修正 | §2.3 废弃加法模型，开发机暂缓，待服务器重估，可与 BOLT 叠加 |
| 中 | R19 | 采纳；usage/测试完成 | timeout 可选，缺失时原生版本查询也通过 |
| 中 | R21 | 采纳；完整 A/A 实验 | 附录 A；按实际门禁标记，失败数据亦保留，不追噪声 |
| 中 | R22 | 采纳；三方交错实验 | 附录 B；固定4GiB AS，无放宽，完整比值及混杂边界 |

## 附录 E：原始记录、检查与发布

| 本机文件/目录 | 内容 |
| --- | --- |
| E/protected-before.json、protected-after.json | docs18/19、spec、GBS配置、完整构建脚本/容量指纹、基准脚本、三个现有 ELF/profile 的保护哈希 |
| E/identity-tests.log、identity-tests.json、identity-{arm,dynamic,static,bolt}.txt | 42 项测试与四类实际身份输出 |
| E/debuginfo-read-only.txt | 当前 find-debuginfo 的节区筛选源码及 BOLT ELF 的 file/objdump 输出；只读检查 |
| E/document-checks.json、acceptance-validator-checks.json | 文档 shell/JSON 语法及终态/缺失/空证据拒绝测试 |
| D/aa/、D/relocs/ | launch/host-before/completion、两轮 JSON/Markdown、calibration JSON、raw 命令/输出；所有失败照实保留 |
| E/run_measurement.py、continue_experiments.py、experiment-controller.log | 本次串行实验执行器；两个重实验不并行 |
| E/experiment-summary.json、summarize_experiments.py | 逐项比值、几何均值、原始 JSON 派生公式；未重写原结果 |
| E/patchelf/、E/patchelf-equality/、D/patchelf.json | patchelf 前后完整节区/notes/segments、时间/命令、三个 TU 原始 .o 与 cmp |
| E/run_patchelf.py | 本轮副本转换及比较执行记录脚本；未成为通用部署工具 |
| E/publication.log、publication-verification.json | 提交、push、远端 HEAD、main/固定提交 raw 内容 SHA 核对，发布后写入 |

文档中的 E/D 等均已在附录 A 展开为固定绝对路径；大 ELF、profile、实验 JSON 和原始日志
按 README 留在 temp，不上传。可复用的身份脚本及测试提交 tools，本次专用编排器留 temp。

自检：不改 spec/LLVM 源码、不做 PGO/完整重建/新 BOLT 重写、不构建 Chromium、不推 Gerrit；
仅编译已授权基准输入并修改已有 BOLT 文件的副本。docs18/19 保留；完整构建 18 GiB 门禁
保持字节不变。最终 GitHub 提交包含本文、身份脚本、测试脚本三项；发布验证记录另存 temp。

最终保护检查：**11 项保护文件全部同 SHA，另加 3.56 GB relocs ELF 前后 SHA 相同**；
LLVM 源码树仍只有任务开始前的 `packaging/llvm.spec` 三处并发差异，spec 本身 hash 未变。
四个完整基准轮都报告 scratch_removed=true；串行实验控制器、patchelf 与 cmp 均已退出。
身份测试 **42/42 PASS**；A/A **FAIL 3.846399%**，三方 **PASS 1.986133%**，
patchelf **6 个 BOLT 节区保留、3 个 TU 字节 PASS**。GitHub 发布仅使用 origin/main，
提交号和 raw 校验由 E/publication-verification.json 记录，并在完成回复给固定提交链接。
