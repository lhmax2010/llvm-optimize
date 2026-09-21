# 20 BOLT spec 集成设计 v2、双目标 profile 与验收协议

修订日期：2026-09-22（§7.1 为预注册最终尝试；附录 A–D 为历史实验）。本文件**完整取代 docs/18 的设计建议**；docs/18、docs/19 原文保留。
用户已解除 docs/19 的停止条件：公开快照陈旧是调查结论，不是禁止面向工作区静态 spec
设计和实验的理由。本文的设计已经展开；**本轮没有修改 spec，也没有部署到 OBS**。
最终验收使用的 OBS 项目及其新 Base 快照仍须用户指定，不能用旧快照冒充新构建。
本版落实编译项校准门禁、八轮简单验收规则、armv7l+aarch64 profile v2。
附录 A–C 保留上一版实验事实；历史 FAIL 不按新门禁重判。新增实验见附录 D。

提交 795a5c4 的实测：profile v2 与一次 6 GiB cap 纯重写完成，30 TU 全部逐字节 PASS；
双目标三方两轮校准 **FAIL，编译项噪声底 3.334074%**。未执行正式轮，
ARM 不劣于 v1 及 AArch64 增量收益均未确证；逐轮诊断比值和失败项见附录 D。
本版补充服务器 A/A 事前中止规则，并完成 §7.1 已预注册的最后一次本机拆分校准：
**ARM FAIL（噪声底4.272374%），未运行正式轮；AArch64 PASS（0.835047%），完成正式轮。**
本机校准线结束，不再重试；后续转三家评审与Quickbuild，不能把局部PASS当成双目标认证通过。

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
上一版 patchelf 实验见附录 C；它只验证这一个显式转换，**不替代 OBS brp/fdupes/转包试验**。

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

脚本输出版本、SHA、Machine、`ARCH_MISMATCH`、`BINFMT_DISPATCH_POSSIBLE`、完整 `readelf -dW`、
`NEEDED_LLVM_SHARED`、BOLT 节区/notes、RPM 查询输出/退出码。
`present` 指观察到 `.note.bolt_info`；`partial` 指只有 `.bolt.org.*`；
`absent` 指二者皆无。`.text.cold` 单独存在不能作为 BOLT 证明。
这是特征检查，不是来源或性能认证；直接 NEEDED=NO 也不递归证明所有间接依赖。

返回码：0 检查完成，1 SHA/BOLT 期望不符，2 输入/辅助工具/解析/版本查询不完整，
3 识别到 shebang wrapper（无其他错误/期望失配时）。`WRAPPER=YES` 时不执行 wrapper；须另用 trace 查最终 ELF。
RPM 无归属、查询错误或缺 rpm 均仅信息项；`--no-exec`、已知架构不匹配本身不使检查失败。
未知架构返回 2；架构不匹配即使指定 loader 也自动跳过执行。
另外只读扫描 `/proc/sys/fs/binfmt_misc/`：已注册条目的 magic/mask/offset 匹配当前 ELF，
或存在 ARM/aarch64 名称/解释器注册，输出 `BINFMT_DISPATCH_POSSIBLE=YES`，自动禁执行。
**即使 ARM chroot 中 `uname -m=armv7l` 且 Machine=ARM，也不绕过这道门禁**。
这是保守的“可能分派”判断：disabled 注册也拦截，不声称内核一定会分派。
注册目录缺失/不可读/格式错误则 UNKNOWN、禁执行、exit 2；可读空目录为 NO，仍保留架构门禁。
NO 只说明当前可见注册未匹配，不能替代 worker 的实际 exec trace。
`--binfmt-extra-dir DIR` 仅增加扫描目录供 mock/另一个 proc mount 使用，不能替代真实 proc 目录。
本机当前只有 jar/python3.12 注册，与 ELF 不匹配；测试用 masked magic+非零 offset、
ARM 注册+模拟同架构 uname 正例和空/不匹配目录负例验证；不修改 binfmt 注册。
版本查询被跳过时，以只读 ELF 身份及实际 worker exec trace 完成核验，不强行执行壳。
依赖 Bash 4+、coreutils、awk、readelf；rpm、timeout 可选。timeout 存在时版本查询限 15 秒。

GN 已知使用平台 clang，验收仍保存 `ninja -C "$OUT" -t commands > commands.txt`，
从具体编译边提取 cc/cxx/launcher，解析 wrapper/软链接，再做 §6 的必做 exec trace。
不能仅凭 args.gn、toolchain.ninja 中变量名或第一层 ARM clang 路径认定最终执行的是哪个 ELF。

## 2. spec 的集成位置与隔离降级

本节是**后续 spec 实施契约**，不是声称本轮已有可运行的 RPM 集成补丁。
原 spec、LLVM 源码及完整构建容量脚本均未修改。下列命令和状态行为在实施时须逐项测试。
首版只改 x86_64 clang-22 实体及别名；不重写 lld、ar 或共享库。

**对普通构建路径的改动清单（后续实施，不是本轮 spec diff）：**

- 仅一项：普通 `ninja -j %{mlgo_build_jobs}` 增加 `-d keeprsp`，保留链接 rsp 供单 clang 重放。
  不改变源、CMake 优化参数或调度并发；缺 rsp 时降级，不自行重建。

新增可选 BOLT 阶段的宏、依赖与 manifest 契约在下文独立定义。`-d keeprsp` 虽不改代码生成，
仍须进入集成指纹；不得用“仅保留文件”绕过首次集成容量认证。

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
   llvm-bolt stripped/clang-22 -data "$PROFILE/merged-v2.fdata" \
     -reorder-blocks=ext-tsp -reorder-functions=cdsort \
     -split-functions -split-all-cold -split-eh -dyno-stats \
     --thread-count=1 -stale-threshold=5 -o candidate/clang-22
   ```

   排序/拆分/dyno-stats 六项来自工作区 `llvm/bolt/README.md:212`，
   `--thread-count=1` 保持 docs/16 实测线程设置；
   `-stale-threshold=5` 是新集成的拒绝门槛（不改变排序算法），依据见 §3.3。
   保存退出码、完整 stderr/dyno-stats、候选 SHA、profile 指标。任何解析缺项、退出非零、
   超时或 OOM 均不提升候选。不在生产包构建中插桩或训练。
4. 对普通 clang 与候选编译 ARM 训练 10 + ARM 留出 10 + aarch64 训练 10 个 TU，固定各目标的资源目录/sysroot、flags、
   cwd、输出路径和 `clang-22 --driver-mode=g++`，保留 `-frecord-gcc-switches`。
   对 30 对 `.o` 逐字节 `cmp`；任一差异 `FALLBACK_CORRECTNESS` 并阻止 BOLT 版发货。
   快速身份/节区/NEEDED 校验也须通过。至此写 `APPLIED` 状态，但只在 `%install` 替换。

本项目 v1 已验证训练 10 + 留出 10，共 **20 个 TU 的 BOLT 产物对照全部逐字节相同**；
这不是未来任意输入/版本正确性的形式证明，新的双目标集成候选执行上述 **30 TU** 门禁。
正确性测试 corpus 作为独立固定版本 builder 测试资产依赖，包含 30 个 .ii、sidecar、
ARM/aarch64 sysroot 与共同资源目录身份和训练/留出标识，不混进 profile 训练集合。
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
4. **profile v2 训练 23 组**：armv7l 13（A/B/C seed=73419、scale=1/2/2 + 原训练 10 .ii），
   再加同 10 个 LLVM 源文件用 RPM 基线重新预处理的 aarch64 10 .ii。
   ARM triple 为 `armv7l-tizen-linux-gnueabi`；aarch64 为 `aarch64-tizen-linux-gnu`。
   各用对应 GBS sysroot，资源头同属该版 clang 22；宏检查须有 `__aarch64__`、无 `__arm__`。
   输入/flags/目标/sysroot/资源目录 SHA 均入 corpus manifest；aarch64 目录独立为
   `tools/bench_inputs/real_tu_aarch64/`，不重标 ARM/x86 的 .ii，也不把 ARM 留出 10 个用于训练。
   每组一次，保存运行时间、退出码和一份 PID fdata。按已冻结的 23 文件清单执行
   `merge-fdata <13 arm fdata> <10 aarch64 fdata> > merged-v2.fdata`，不扫描通配符混入额外负载。
   新 OBS clang 的资源目录不能冒用本机旧 headers；为该版本冻结新的 corpus manifest。
5. 在该 stripped 输入试纯重写，满足 §3.3 和 30 TU 正确性；将 profile + manifest 打成
   独立 noarch RPM。下一次同图/已重认证构建即可应用，不能为了自举在首次 OBS 构建里循环训练。

本轮**不重新插桩**，复用 Q/instrumented 原件，只采新增 aarch64 10 组，合并后在
6 GiB cap 下允许一次纯优化重写；实测及门禁见附录 D。旧 v1 profile 为 153887224 B，SHA
`d8b6c9146822fbe19ce0c3646d57d17e797d865100a7b0193562db6ea371c24d`，保持不变。
本机 v2 与未来首个生产 OBS profile 是两个认证对象；本机实测不自动授权新的 OBS 输入 SHA。

### 3.2 分发与版本

首选独立 `noarch` RPM，例如 `llvm-bolt-profile-clang22-<profile-id>`，路径
`/usr/share/llvm-bolt-profiles/<profile-id>/{merged-v2.fdata,manifest.json}`；包 ID 永不复用，
NEVRA、RPM SHA、解包 profile SHA 都固定。profile 不进 Source0，不扩大非 x86_64 构建依赖。
无 BOLT 分支不解析 profile/tools 包；精确依赖在入队时决定，见 §2.1。

其他方案仍有明确边界：独立有条件 SourceN 可离线归档，但本次 v2 为 171232190 B
（v1为153887224 B）的分发成本及源文件
缺失可能在 `%prep` 前阻断，要用两套入队配置；固定服务器路径只适合试验，必须只读、
固定内容哈希并备份，可移植性低，不作为首版生产分发。均不使用滚动 latest。

manifest 版本 `profile_schema=2`、`profile_version=v2`：保存 source/spec/patch SHA、MLGO 参数及模型 SHA、
CMake/宏/目标架构、relocs SHA、stripped SHA、代码/重定位摘要、BOLT tool/runtime SHA、
分目标的 corpus（armv7l 13 / aarch64 10）、每个输入/flags/资源目录/sysroot SHA、profile SHA/bytes、命令、时间、owner/reviewer、
认证输入列表、profile 统计及正确性结果。不同构建图生成新 profile-id，不覆盖旧文件。
目标 corpus 的强制字段如下（尖括号为必须填入的摘要，不是允许的运行时缺省值）：

```json
{
  "profile_schema": 2,
  "profile_version": "v2",
  "corpora": [
    {"target": "armv7l-tizen-linux-gnueabi", "count": 13,
     "synthetic": {"seed": 73419, "scales": [1, 2, 2]}, "real_tu_count": 10,
     "inputs_flags_manifest_sha256": "<SHA256>", "sysroot_headers_sha256": "<SHA256>"},
    {"target": "aarch64-tizen-linux-gnu", "count": 10, "real_tu_count": 10,
     "inputs_flags_manifest_sha256": "<SHA256>", "sysroot_headers_sha256": "<SHA256>"}
  ],
  "resource_headers_sha256": "<shared clang 22 resource SHA256>",
  "relocs_sha256": "<SHA256>", "stripped_sha256": "<SHA256>",
  "profile_sha256": "<SHA256>", "candidate_sha256": "<SHA256>"
}
```

实际每个输入的路径、SHA、flags 与 target 均在所引用的 manifest 展开，不仅记数量。
两目标 sysroot 的头文件摘要分别计算；生成的 .ii 本身再以 SHA 固定，后续测量不重新 -E。

**任一 source/spec/patch/MLGO 配置变化触发重训申请与重新认证**。
即便只有重建时间路径导致新 ELF SHA，也必须重新认证，不能自动沿用 allowlist：
先比较代码/重定位/符号图，核对新构建身份；在独立受限试验中测旧 profile 的匹配率、
30 TU 正确性和筛选方向，维护者签署新输入 SHA 认证记录后才能复用。
若配置变化实质改变图，重新走 23 组训练。待认证期间自动普通包降级。

### 3.3 stale 与覆盖率的可达门槛

首版冻结为以下**工程准入政策**，不是上游保证或从吞吐拟合出的统计界限：

- stale **函数数量**占比 **≤5%**，不是样本权重占比。源码变量对应为
  `100 * NumAllStaleFunctions / (ProfiledFunctions.size() + NumStaleProfileFunctions)`；
  分母是参与该统计的有效+无效 profile 函数，不含提前跳过的 non-simple 函数。
  分子含 invalid 和 inferred-stale，保持默认不启用 infer-stale，传 `-stale-threshold=5`。
  严格 `>` 才错误退出，因此 5% 本身可通过，不用日志中四舍五入的百分比复算门禁。
- 有效 profile 函数覆盖率 **≥10%**：`valid_profile_functions / total_regular_functions`；
  用数量计算，禁止把输出四舍五入后的 15.1 当原始数据。统计缺失/分母为 0 均拒绝提升。
- 另记录 stale sample 占比与 non-simple 数，不把 non-simple 混成 stale；出现新解析警告
  类别、无法映射的输入图或工具版本漂移，要求离线重认证，不用“退出 0”替代认证。

依据：docs/16 rewrite 原始日志是 **21802 / 144032** 有 profile，约 15.137%；
另有 **378 non-simple profiled functions** 未优化。源码
`llvm/bolt/lib/Passes/BinaryPasses.cpp:1466–1469、1487–1502、1524–1564`
显示 non-simple 单列、分母在 :1524–1525、函数比例在 :1536–1538、
阈值判断/错误退出在 :1561–1564。:1551–1559 的 stale **samples** 比例仅另行打印，
不是 `-stale-threshold` 的判据；源码无需修改。stale 会从有效集合排除；
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
未来最终 worker 还执行双目标 30 TU 等价性，不止在 build tree 里检查一次。

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

首版只 BOLT clang，因为历史 profile/20 TU 与本次双目标 profile/30 TU 的正确性、筛选证据均针对它。
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

上一版补齐的 A/A 与 relocs-only 是诊断实验，详见附录 A/B；当时不训练、不重写 BOLT。
795a5c4 的双目标 profile/一次重写单列附录 D，不回填旧试验。
文中保留的百分比只用于内部噪声/阈值/历史口径说明；对外收益表述采用本文开头的定性句。

795a5c4 身份脚本测试：`tools/test_verify_toolchain_identity.sh` 已入库，共 49 项。
真实正负对照为：现有 ARM 根 clang、docs/19 动态快照 x86_64 clang、静态 RPM clang、
现有 BOLT clang。ARM 正例不执行，recording-loader 验证没有被调用。
其余用私有 PATH mock 注入 awk/stat/readelf/uname/RPM 错误及 partial 特征；不改真实 ELF。
测试可传 `--static/--dynamic/--arm/--bolt/--loader` 指定异机 fixture，缺 fixture 明确失败。
上一版 `E/identity-tests.log` 为 42/42 PASS；新增 binfmt 后原始输出
`E2/identity-tests.log`，实测 **49/49 PASS**。完整分支与命令就在提交的测试脚本里。

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
配对固定 A1/B1、A2/B2、A3/B3；不用按快慢重排。A/A 用于给 §6.3 的阈值提供 d，
A0b 完成后，对每一指标计算 `d = |A0b/A0a − 1|`，包括时间、CPU 第二口径和资源指标。
**任一指标 d > 0.10，则判服务器环境不稳，中止验收、不启动 A1**；保留两轮原始证据。
查明环境后另建试验 ID，从 A0a 重做全部八轮，不能沿用此次 A/A 或部分 A/B。
全部 d ≤ 0.10 才继续后六轮，并按 §6.3 的 `max(0.03, 2d)` 判据判断收益。
这是事前环境中止条件，不改通过判据，也不恢复 AA≤3% 条件；0.10 边界允许继续。
下游运行的独立八轮同样在自身 A/A 后执行此检查。任何指标缺失/非有限/非正数均拒绝启动 A1。
任一轮构建/身份/资源执行失败仍终止整个验收；已完成轮保留为诊断数据，不追加轮次。

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

### 6.3 冻结配对、简单判定与量化资源红线

主指标同时报告有效完整 build wall、单位编译 wall（冻结编译边中所有尝试的
`Σ(end-start)/编译任务数`）；第二口径为同一新 cgroup 的
`Δcpu.stat(user_usec + system_usec)`，必须纳入实际 accel 子进程。
从 `.ninja_log` 毫秒与 commands 分类，重试/重复边计入且单列，不仅保留最后一次。
排队时间、跨机器/任务图/缓存策略的绝对耗时不可比较，历史本机轮不能作为服务器 A 组。

冻结顺序 **A0a A0b A1 B1 B2 A2 A3 B3**，A 为同 source/spec/patch 的
`without_clang_bolt` 构建。固定配对 A1/B1、A2/B2、A3/B3，禁止重排或追加轮。
对每一指标分别计算 `d = abs(A0b/A0a - 1)`。A/A 不是置信区间估计，
而是这一组执行的噪声参照；先执行 §6.2 的任一 d > 0.10 中止检查，
通过后 d 进入下面的统一阈值，不叠加旧的 AA≤3% 准入规则。

对三个时间/CPU 指标各自用自己的 d：

```text
margin = max(0.03, 2*d)
limit = 1 - margin
r1 = B1/A1; r2 = B2/A2; r3 = B3/A3
成立 = (r1 < limit and r2 < limit and r3 < limit)
```

必须**三对全部严格小于**阈值；等于也不成立。任一对不满足标 **未确证**，不加轮。
各项 `GM = (r1*r2*r3)^(1/3)` 只描述结果，不能用平均收益盖过某一对失败。
不计算 t 区间，不靠选择轮次或无限加样本把结论改成成立。完整 build wall、单位编译 wall、
CPU 第二口径须全部成立才批准整体收益；仅编译指标通过则只能报告编译阶段观察，
Quickbuild 整体收益仍未确证。执行失败/缺证据/输入变化仍按 §6.2 立即停止。

调度器必须在 A0b 完成后，先将所有指标的两次值传给 `aa_preflight()`；只有 CONTINUE
才入队 A1。`paired_gate()` 再做防御检查，不能靠八轮结束后检查来替代事前中止。
以下代码给出精确规则（数值须有限且 >0；后六轮来自同一试验 ID）：

```python
import math
from decimal import Decimal

def aa_preflight(metrics):
    # Called immediately after A0b, before scheduling ANY A1.
    if not metrics:
        raise ValueError("missing A/A metrics")
    drift = {}
    for name, pair in metrics.items():
        a0a, a0b = pair
        if not all(math.isfinite(x) and x > 0 for x in pair):
            raise ValueError("invalid or missing A/A measurement")
        # Decimal keeps the exact 0.10 boundary from failing due to float rounding.
        drift[name] = abs(Decimal(str(a0b))/Decimal(str(a0a)) - 1)
    abort = any(d > Decimal("0.10") for d in drift.values())
    return {"status": "ABORT_ENVIRONMENT" if abort else "CONTINUE",
            "drift": {name: float(d) for name, d in drift.items()}}

def paired_gate(values):
    preflight = aa_preflight({"metric": values[:2]})
    if preflight["status"] == "ABORT_ENVIRONMENT":
        return {**preflight, "established": False}  # No later measurements required.
    a0a, a0b, a1, b1, b2, a2, a3, b3 = values
    if not all(math.isfinite(x) and x > 0 for x in values):
        raise ValueError("invalid or missing measurement")
    d = abs(Decimal(str(a0b))/Decimal(str(a0a)) - 1)
    ratios = [Decimal(str(b))/Decimal(str(a)) for a,b in [(a1,b1),(a2,b2),(a3,b3)]]
    threshold = 1 - max(Decimal("0.03"), 2*d)
    return {"status": "EVALUATED", "d": float(d), "threshold": float(threshold),
            "ratios": list(map(float, ratios)),
            "established": all(r < threshold for r in ratios),
            "geomean": math.prod(map(float, ratios))**(1/3)}
```

资源阈值维持工程预算；为了不用统计区间又不把误差当收益，采用**各对最大比值 + 2d**
的保守上界，d 取该资源指标自己的 A/A 值。大误差不能放宽预算：

| 指标 | 非退化门槛（B/A，分母为配对 A） | 依据与误差处理 |
| --- | --- | --- |
| 编译期 cgroup memory.peak | `max(r1,r2,r3)+2d ≤1.05`，所有轮无 OOM/新增swap | +5% 工程预算；按峰值实测，不从文件体积推算 |
| 下游运行 wall 与 CPU（分别） | `max(r1,r2,r3)+2d ≤1.02` | +2% 工程预算，生成代码预期不变，需独立执行验收 |
| 下游运行 cgroup peak/RSS（分别） | `max(r1,r2,r3)+2d ≤1.03`，每轮无 OOM/新增swap | +3% 工程预算；RSS/cgroup不可互替 |

下游运行单独用冻结的启动/页面加载/交互/退出套件，以资产和命令 SHA 固定输入，
同机/隔离/缓存策略，独立 A/A 一对和 A/B 交错三对，顺序同上，不在运行中更换网页/网络内容。
任一功能失败立即终止；上述保守上界越线即**未确证/不放行**，不加轮。
5/2/3% 是首版风险预算，2d 是预先冻结的误差余量政策，均不冒称自然方差估计或已有实测。
服务器尚未执行，不能给“下游资源不退化”的承诺。

发货还要求 §4.4 静态开发包门禁、最终 RPM/accel/worker **30 TU** 字节门禁、正确 debug
策略、无未认证后处理。本轮不运行 Quickbuild 或 Chromium，仅交付模板与本机附录数据。

## 7. 基准台协议变更记录

**生效日期 2026-09-21，自提交 `795a5c4` 引入的 `compile-only-v2` 协议起，只适用于此后运行。**
附录 D 使用该提交的脚本 SHA；本次目标筛选会再次改变脚本/协议 hash，不追溯旧 JSON。
`ld.lld`/`llvm-ar` 的 66 个小对象负载主要测约 4.5 ms 的启动成本，不在编译几何平均内。
两项仍完整测量、写 rows 和原始统计，`diagnostic_only=true`；row.pass 仅表示其数值是否
在阈值内，**不影响整体 PASS 或 noise_floor_pct**。报告显式列 Diagnostic only，避免误读。
只对编译项应用中位数跨轮差≤3%、每轮 CV≤3%、无保留可疑样本；噪声底取编译项最大差。
协议包含 `calibration_policy=compile-only-v2`、脚本 SHA、各目标输入及 sysroot 头文件 hash，
因此 protocol hash 必变；新旧 hash 不可混成一对校准，也不能按新规则重判旧失败。
`calibration()` 还会拒绝缺少新 policy 字段的旧 JSON，防止误用 API 追溯重判。

历史判定固定保留：docs/17 两对 **FAIL 4.345326% / FAIL 6.609160%**，本文件附录 A
**FAIL 3.846399%**。三次虽由 lld/ar 触发，但仍是当时协议的 FAIL。附录 B 的原 PASS 同样保留。
测试覆盖“编译 4% 仍 FAIL”和“lld/ar 20%/CV超限/可疑，但编译全过则整体 PASS”，以及
AArch64 target/对象 Machine 正反例。新增目标仅对明确传入的 corpus 生效；ARM夹具由首个
工具链生成，23 编译项与 lld/ar 在同一轮按负载/轮次交错，不拼接不同轮的历史数据。

### 7.1 本机校准最终尝试（预注册已执行，本机不再重试）

预注册 ID：`FINAL-SPLIT-20260921`。这是本机**最后一次**校准尝试；无论结果如何，
随后转三家评审与 Quickbuild 验收，不再安排本机重试。采用用户已定的失败解释：
795a5c4 附录 D 在 20:00–20:01 宿主 loadavg 超过10，出现 suspect 与 CV 超限，
同时69个编译组合取最大偏差会增加撞线概率；不把这次 FAIL 归因于基准台实现缺陷。
历史 FAIL、全部原始样本与附录 D 保持原判，不能用本次结果覆盖。

**预注册提交证据：** `ea7d1207a2894e9f2267ec1f3aa92a0a8b4e2e1f`，提交信息为
`Preregister final split BOLT calibration`，Git committer时间 **2026-09-21 22:28:42 +08:00**。
文档、脚本和机器可读计划先提交并推送；用户后续确认“开始”，才在2026-09-22启动。
启动器核对干净HEAD与origin/main都等于该SHA，将提交号、Git时间、计划SHA写入
`attempt.json` 和 `preregistration-git.txt`。本版是结果归档，不能用本版提交时间替代预注册。
以下冻结条件在运行后没有调整。可只读查看原预注册提交：

```bash
git log -1 --format=fuller --grep='^Preregister final split BOLT calibration$'
```

冻结条件（机器可读版：`tools/final_bolt_calibration_plan.json`）：

| 项目 | 事前约定 |
| --- | --- |
| 执行顺序 | A=armv7l 13项×3工具链，两轮完整校准；若PASS则紧接A正式轮。然后B=aarch64 10项×3工具链，两轮完整校准；若PASS则紧接B正式轮。串行执行，不交叠 |
| 工具链顺序 | rpm-baseline、bolt-v1、bolt-v2；每个目标内同轮交错，沿用奇偶轮反转；RPM始终生成共同夹具 |
| 独立门禁 | A的39个、B的30个编译组合分别取最大偏差；每项跨轮中位数差≤3%、每轮CV≤3%、无保留suspect。lld/ar仍完整测量、仅诊断 |
| 启动窗口 | 用户确认夜间关闭桌面应用后才允许启动；入口记录loadavg原文、前20进程RSS、/proc/meminfo及MemAvailable字节数。入口1分钟loadavg>3直接拒绝，不等待、不自动重试；等于3允许 |
| 运行环境 | CPU2、ASLR off、N=5丢首次、编译进程4GiB AS、tmpfs；load suspect阈值10；保留可疑样本，不筛掉 |
| 负载 | ARM A/B/C seed73419、scale1/2/2 + 原ARM训练10；AArch64为原v2的10个.ii。留出10不进入性能表；输入/flags/SHA冻结，不重新预处理 |
| 资源目录/sysroot | 同TC/lib64/clang/22；ARM与AArch64分别用附录D的固定根，头文件hash须与795a5c4一致 |
| 链接/归档 | 两目标都保留附录D的共同66个ARM对象夹具；lld4096/ar1024次归一化。B中生成A/B/C仅供夹具，不计入B的10个计时编译项 |
| 采样 | 从本次运行开始到结束，每30秒记录loadavg，另记起止；保存采样最大值、>10的样本时间与相邻界限，不能冒称连续最大值/精确越线时刻 |
| 失败/通过 | 目标校准FAIL不跑该目标正式轮、不重试；一个目标FAIL仍执行另一目标。执行错误、身份/输入变化、采样失败则停止，不把错误当完整校准FAIL。PASS仅允许该目标一次正式轮 |
| 正式轮 | 参数/工具/夹具须与该目标校准完全相同；同轮v2/v1、v2/RPM、v1/RPM逐项比值与编译GM；注明分母、正式/诊断、全部为训练集 |
| 一次性 | 固定新目录拒绝复用；拒绝启动也保存记录，不自动换ID、改阈值、换负载或重试。结果不支持再安排本机校准 |

拆分是把69个组合的“取最大”改为39和30两个较小集合各自取最大，降低多重比较下
撞线概率；**判据本身不放宽**，不声称修正了统计置信水平。A/B结果分开发布，不能只报
通过者，也不把两目标重新合成一个校准PASS。这个改变在运行前进入Git，不能事后选集合。
“启动 load≤3”只用于本次入口启动；运行中仍使用原load>10 suspect规则，采样仅留证，
不动态暂停或改变协议。Quickbuild的A/A d>0.10规则不替代本机3%校准规则。

以下为冻结的执行入口；本次已执行完毕，**不得再次启动本机校准**。默认仍只打印计划：

```bash
# 默认仅打印冻结命令，不执行任何 clang：
python3 tools/run_final_bolt_calibration.py
# 本次已执行的命令模板（归档，勿重跑）；PREREG_COMMIT为上述预注册完整SHA：
python3 tools/run_final_bolt_calibration.py --run --quiet-window-confirmed \
  --preregistered-commit "$PREREG_COMMIT"
```

启动器只允许测量，不含采profile/BOLT/重建入口。冻结文件保存旧输入hash、三个二进制
及运行库身份、精确原命令和夹具hash；目标筛选是唯一负载选择变化。子进程退出/信号
路径都会回收采样线程，异常终止测量进程组并保留现场。相关测试使用mock，不启动clang。

固定原始输出目录：
`/home/linhao/Toolchain/development/llvm-optimize/temp/bench_results/bolt-final-split-20260921/`。
保存顶层环境、attempt、loadavg与Git证据，以及 `armv7l/`、`aarch64/` 各自
`calibration-run1/2.json`、`calibration.json`、逐项Markdown与原始命令；通过者另有formal。
阶段起止时间供分别归属load样本。以下已列全部逐项表、各自noise_floor、正式轮
（通过者）与环境最大load/>10时段；失败诊断表同样保留，没有以历史轮作对照。

| 当前执行状态 | ARM校准 | AArch64校准 | 正式轮 | 启动环境 |
| --- | --- | --- | --- | --- |
| **COMPLETE_NO_MORE_LOCAL_ATTEMPTS** | FAIL 4.272374% | PASS 0.835047% | 仅AArch64完成一轮 | load1=1.59，MemAvailable=24503046144 B |

两次均未通过时结论固定为：**“v2 性能认证本机未确证，转 Quickbuild”**。仅一个通过时，
只报告该目标正式结果，另一个未确证；两个通过仍只是训练集筛选结果，不能外推全平台。
任何结果后都结束本机校准，转评审与Quickbuild；不因点值接近门槛再加轮。

#### 7.1.1 预注册执行记录与最终结论

本次预注册提交为 **`ea7d1207a2894e9f2267ec1f3aa92a0a8b4e2e1f`**，Git committer时间
**2026-09-21 22:28:42 +08:00**，已先push。用户在后续消息中确认“开始”，才执行冻结入口；
实际启动 **2026-09-22T00:21:32.562370+08:00**，结束 **2026-09-22T02:03:03.060858+08:00**。未改参数/样本/输入/工具，不追加轮次。
启动记录：`loadavg_raw=1.59 1.32 1.26 3/1429 762552`，1分钟值 **1.59≤3**；
MemAvailable **24503046144 B**（22.820240 GiB）。
这是实际读数，不据用户确认推断所有桌面/后台进程消失。前20进程RSS原始输出（KiB）：

```text
    PID COMMAND           RSS
   9122 code            1405320
   9116 code            730436
 302824 xdg-desktop-por 578748
   4625 code            421180
   4366 code            396772
   4496 code            380624
  10516 claude          378824
   9095 code            363736
   4358 code            320152
   2871 gnome-shell     307832
   4248 code            273024
  10549 code            265404
  14419 claude          243116
  14329 claude          240032
   5070 claude          236756
   9159 codex           230308
   4660 code            229896
   2331 epp-client-daem 227196
  15501 nautilus        222612
   4789 codex           219448
```

30秒采样最高1分钟loadavg **4.28**；超过10的样本 **0**。
采样器回收 **True**，错误 **None**。该最大值是离散采样最大值，不是连续峰值。
未观察到>10时段；逐测量前后的load仍按基准台原规则判suspect，不以30秒采样替代。

| 目标 | 实际开始 | 实际结束（含正式轮若有） | 目标期间采样max load1 | >10样本 |
| --- | --- | --- | ---: | ---: |
| armv7l | 2026-09-22T00:21:36.050415+08:00 | 2026-09-22T01:06:35.311988+08:00 | 4.28 | 0 |
| aarch64 | 2026-09-22T01:06:35.335654+08:00 | 2026-09-22T02:03:03.060027+08:00 | 2.16 | 0 |

| 目标 | 校准判定 | noise_floor % | 未通过编译组合 | 正式轮 |
| --- | --- | ---: | ---: | --- |
| armv7l | **FAIL** | 4.272374 | 8 | 未执行（校准FAIL） |
| aarch64 | **PASS** | 0.835047 | 0 | 已执行 |

armv7l 编译组合 39 项：跨轮差>3%有 5 项，
任一轮CV>3%有 5 项，
保留suspect的组合有 0 项（各类可重叠，不相加冒充失败总数）。

aarch64 编译组合 30 项：跨轮差>3%有 0 项，
任一轮CV>3%有 0 项，
保留suspect的组合有 0 项（各类可重叠，不相加冒充失败总数）。

仅对通过校准的目标报告正式轮；另一目标未确证，不能把局部PASS表述为双目标认证通过。
**本机校准线到此结束，无论上述结果如何都不再重试；后续转三家评审和Quickbuild。**

| 目标/轮次 | 性质 | GM(v2/v1) | GM(v2/RPM) | GM(v1/RPM) |
| --- | --- | ---: | ---: | ---: |
| armv7l/calibration-run1 | 校准诊断/训练集 | 1.002496 | 0.854402 | 0.852275 |
| armv7l/calibration-run2 | 校准诊断/训练集 | 1.004235 | 0.854986 | 0.851380 |
| aarch64/calibration-run1 | 校准诊断/训练集 | 0.995011 | 0.847232 | 0.851480 |
| aarch64/calibration-run2 | 校准诊断/训练集 | 0.995636 | 0.848649 | 0.852368 |
| aarch64/formal | 正式/训练集 | 0.995354 | 0.848116 | 0.852074 |

比值均为同轮wall中位数之比，分母如列名；<1表示耗时降低，>1表示耗时增加。GM仅含编译项，
lld/ar仍诊断。v2/v1比较双目标与ARM-only profile的布局；v2/RPM、v1/RPM包含原重链/剥离/BOLT，
不是纯BOLT拆分收益。全为训练输入（ARM13/AArch6410），不含留出集；不外推Chromium或全平台。
相近比值不构成独立统计非退化证明；未通过的轮不得用于正式收益表述。

#### 7.1.2 armv7l 逐项校准与测量

校准protocol hash：`81dfe4ad6f089a29eeed0422ca9586a73a75221b2c0de46e823e9c5801ae8909`。以下保留所有编译与诊断行，门禁不省略失败项。

| 工具链/项 | 跨轮差 % | CV1 % | CV2 % | 保留suspect | row.pass | diagnostic_only |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| rpm-baseline/A | -1.424359 | 3.588765 | 0.758672 | 0 | False | False |
| rpm-baseline/B | -2.431687 | 1.601369 | 0.210240 | 0 | True | False |
| rpm-baseline/C | -4.064013 | 3.035621 | 0.132084 | 0 | False | False |
| rpm-baseline/real_llvm_arm_ARMISelLowering | -2.908033 | 1.889254 | 0.211200 | 0 | True | False |
| rpm-baseline/real_llvm_arm_ARMTargetTransformInfo | -1.694742 | 0.877711 | 0.279759 | 0 | True | False |
| rpm-baseline/real_llvm_codegen_MachinePipeliner | -2.200946 | 1.756354 | 0.201027 | 0 | True | False |
| rpm-baseline/real_llvm_codegen_SelectionDAG | -2.843868 | 1.931653 | 0.611955 | 0 | True | False |
| rpm-baseline/real_llvm_mc_AsmParser | -1.943643 | 2.186278 | 0.767030 | 0 | True | False |
| rpm-baseline/real_llvm_mc_MasmParser | -0.582451 | 0.767090 | 0.307267 | 0 | True | False |
| rpm-baseline/real_llvm_sema_SemaExprCXX | -1.348434 | 1.031340 | 0.258786 | 0 | True | False |
| rpm-baseline/real_llvm_sema_SemaStmt | -0.919048 | 0.825021 | 0.546815 | 0 | True | False |
| rpm-baseline/real_llvm_transforms_Attributor | -0.233868 | 1.249805 | 0.165086 | 0 | True | False |
| rpm-baseline/real_llvm_transforms_WholeProgramDevirt | -0.729688 | 1.512003 | 0.376977 | 0 | True | False |
| rpm-baseline/ld.lld | -0.528980 | 1.439831 | 0.153962 | 0 | True | True |
| rpm-baseline/llvm-ar | 0.333478 | 1.528938 | 1.731928 | 0 | True | True |
| bolt-v1/A | -2.171142 | 4.038165 | 0.687272 | 0 | False | False |
| bolt-v1/B | -3.469343 | 2.423387 | 0.241181 | 0 | False | False |
| bolt-v1/C | -4.060246 | 2.547546 | 0.067667 | 0 | False | False |
| bolt-v1/real_llvm_arm_ARMISelLowering | -2.061388 | 1.760182 | 0.280377 | 0 | True | False |
| bolt-v1/real_llvm_arm_ARMTargetTransformInfo | -1.740006 | 2.439992 | 0.780794 | 0 | True | False |
| bolt-v1/real_llvm_codegen_MachinePipeliner | -2.707122 | 1.985106 | 0.209705 | 0 | True | False |
| bolt-v1/real_llvm_codegen_SelectionDAG | -2.827440 | 2.004090 | 0.521254 | 0 | True | False |
| bolt-v1/real_llvm_mc_AsmParser | -1.928699 | 2.230354 | 0.928355 | 0 | True | False |
| bolt-v1/real_llvm_mc_MasmParser | -0.532458 | 0.994394 | 0.501219 | 0 | True | False |
| bolt-v1/real_llvm_sema_SemaExprCXX | -0.874321 | 1.281035 | 0.439464 | 0 | True | False |
| bolt-v1/real_llvm_sema_SemaStmt | -0.728321 | 1.383903 | 0.294391 | 0 | True | False |
| bolt-v1/real_llvm_transforms_Attributor | -0.864781 | 1.675499 | 0.460367 | 0 | True | False |
| bolt-v1/real_llvm_transforms_WholeProgramDevirt | -0.693833 | 1.663092 | 0.677677 | 0 | True | False |
| bolt-v1/ld.lld | -0.512144 | 1.829785 | 0.247299 | 0 | True | True |
| bolt-v1/llvm-ar | -0.057702 | 1.340329 | 0.529614 | 0 | True | True |
| bolt-v2/A | -3.559196 | 5.114231 | 0.315029 | 0 | False | False |
| bolt-v2/B | -2.711827 | 1.845060 | 0.199088 | 0 | True | False |
| bolt-v2/C | -4.272374 | 2.885736 | 0.167753 | 0 | False | False |
| bolt-v2/real_llvm_arm_ARMISelLowering | -1.938776 | 2.285265 | 0.239557 | 0 | True | False |
| bolt-v2/real_llvm_arm_ARMTargetTransformInfo | -1.510268 | 1.689536 | 0.536444 | 0 | True | False |
| bolt-v2/real_llvm_codegen_MachinePipeliner | -2.511864 | 1.839802 | 0.411654 | 0 | True | False |
| bolt-v2/real_llvm_codegen_SelectionDAG | -2.502345 | 1.321945 | 0.326350 | 0 | True | False |
| bolt-v2/real_llvm_mc_AsmParser | -1.059964 | 3.099178 | 0.213358 | 0 | False | False |
| bolt-v2/real_llvm_mc_MasmParser | -0.125677 | 0.675790 | 0.509944 | 0 | True | False |
| bolt-v2/real_llvm_sema_SemaExprCXX | -0.629934 | 1.158342 | 0.785904 | 0 | True | False |
| bolt-v2/real_llvm_sema_SemaStmt | -0.206784 | 1.156258 | 0.037252 | 0 | True | False |
| bolt-v2/real_llvm_transforms_Attributor | -0.714533 | 1.045505 | 0.639277 | 0 | True | False |
| bolt-v2/real_llvm_transforms_WholeProgramDevirt | -0.676008 | 1.145060 | 0.018938 | 0 | True | False |
| bolt-v2/ld.lld | -0.752494 | 1.229141 | 0.296364 | 0 | True | True |
| bolt-v2/llvm-ar | -0.586268 | 2.557062 | 0.610607 | 0 | True | True |

**calibration-run1（校准/诊断，训练集）**

| 项 | RPM s | v1 s | v2 s | v2/v1 | v2/RPM | v1/RPM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 8.373248 | 7.523491 | 7.641795 | 1.015725 | 0.912644 | 0.898515 |
| B | 2.253722 | 1.745383 | 1.752934 | 1.004326 | 0.777795 | 0.774444 |
| C | 6.137816 | 5.911611 | 5.919143 | 1.001274 | 0.964373 | 0.963146 |
| real_llvm_arm_ARMISelLowering | 8.424065 | 7.192691 | 7.198215 | 1.000768 | 0.854482 | 0.853827 |
| real_llvm_arm_ARMTargetTransformInfo | 4.783723 | 3.970509 | 3.993565 | 1.005807 | 0.834823 | 0.830004 |
| real_llvm_codegen_MachinePipeliner | 6.200499 | 5.304762 | 5.310785 | 1.001135 | 0.856509 | 0.855538 |
| real_llvm_codegen_SelectionDAG | 6.895490 | 5.881840 | 5.895137 | 1.002261 | 0.854927 | 0.852998 |
| real_llvm_mc_AsmParser | 2.652189 | 2.254123 | 2.251040 | 0.998633 | 0.848748 | 0.849910 |
| real_llvm_mc_MasmParser | 3.275470 | 2.814595 | 2.800679 | 0.995056 | 0.855046 | 0.859295 |
| real_llvm_sema_SemaExprCXX | 6.043758 | 4.980607 | 4.988178 | 1.001520 | 0.825344 | 0.824091 |
| real_llvm_sema_SemaStmt | 5.773037 | 4.811499 | 4.806012 | 0.998860 | 0.832493 | 0.833443 |
| real_llvm_transforms_Attributor | 6.201319 | 5.274070 | 5.288861 | 1.002805 | 0.852861 | 0.850475 |
| real_llvm_transforms_WholeProgramDevirt | 5.696764 | 4.822742 | 4.844031 | 1.004414 | 0.850313 | 0.846576 |
| ld.lld | 0.004716 | 0.004706 | 0.004730 | 1.004990 | 1.002956 | 0.997976 |
| llvm-ar | 0.002317 | 0.002313 | 0.002326 | 1.005770 | 1.003970 | 0.998210 |

整轮wall 1364.721989s，所有命令最大RSS 1188744KiB，scratch_removed=True，状态 MEASURED。
该轮编译项最大CV 5.114231%，保留suspect样本 0；均如实披露，不调整样本或追加重试。
fixture hash：`30acab6c36503bcf53f5ad6467d17a58ede7f0205f95f68dedd1125494a9096a`。


**calibration-run2（校准/诊断，训练集）**

| 项 | RPM s | v1 s | v2 s | v2/v1 | v2/RPM | v1/RPM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 8.253983 | 7.360145 | 7.369809 | 1.001313 | 0.892879 | 0.891708 |
| B | 2.198919 | 1.684829 | 1.705397 | 1.012208 | 0.775562 | 0.766208 |
| C | 5.888374 | 5.671585 | 5.666255 | 0.999060 | 0.962278 | 0.963183 |
| real_llvm_arm_ARMISelLowering | 8.179091 | 7.044422 | 7.058658 | 1.002021 | 0.863013 | 0.861272 |
| real_llvm_arm_ARMTargetTransformInfo | 4.702652 | 3.901422 | 3.933251 | 1.008158 | 0.836390 | 0.829622 |
| real_llvm_codegen_MachinePipeliner | 6.064030 | 5.161155 | 5.177385 | 1.003145 | 0.853786 | 0.851110 |
| real_llvm_codegen_SelectionDAG | 6.699391 | 5.715535 | 5.747621 | 1.005614 | 0.857932 | 0.853142 |
| real_llvm_mc_AsmParser | 2.600640 | 2.210647 | 2.227180 | 1.007479 | 0.856397 | 0.850040 |
| real_llvm_mc_MasmParser | 3.256392 | 2.799609 | 2.797160 | 0.999125 | 0.858975 | 0.859727 |
| real_llvm_sema_SemaExprCXX | 5.962262 | 4.937060 | 4.956756 | 1.003989 | 0.831355 | 0.828052 |
| real_llvm_sema_SemaStmt | 5.719980 | 4.776456 | 4.796074 | 1.004107 | 0.838477 | 0.835048 |
| real_llvm_transforms_Attributor | 6.186816 | 5.228461 | 5.251071 | 1.004324 | 0.848752 | 0.845097 |
| real_llvm_transforms_WholeProgramDevirt | 5.655196 | 4.789280 | 4.811285 | 1.004595 | 0.850772 | 0.846881 |
| ld.lld | 0.004691 | 0.004682 | 0.004694 | 1.002562 | 1.000702 | 0.998145 |
| llvm-ar | 0.002324 | 0.002311 | 0.002312 | 1.000451 | 0.994767 | 0.994318 |

整轮wall 1328.928985s，所有命令最大RSS 1519804KiB，scratch_removed=True，状态 MEASURED。
该轮编译项最大CV 0.928355%，保留suspect样本 0；均如实披露，不调整样本或追加重试。
fixture hash：`30acab6c36503bcf53f5ad6467d17a58ede7f0205f95f68dedd1125494a9096a`。

#### 7.1.3 aarch64 逐项校准与测量

校准protocol hash：`fa1d35ecf70c9d9fd26e63189d2656c0c6fc2baa6fa4fa2e62dec33fbb03c46e`。以下保留所有编译与诊断行，门禁不省略失败项。

| 工具链/项 | 跨轮差 % | CV1 % | CV2 % | 保留suspect | row.pass | diagnostic_only |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| rpm-baseline/real_aarch64_llvm_arm_ARMISelLowering | 0.281619 | 0.629295 | 0.734378 | 0 | True | False |
| rpm-baseline/real_aarch64_llvm_arm_ARMTargetTransformInfo | -0.089501 | 0.423491 | 0.476917 | 0 | True | False |
| rpm-baseline/real_aarch64_llvm_codegen_MachinePipeliner | 0.835047 | 0.636036 | 0.123870 | 0 | True | False |
| rpm-baseline/real_aarch64_llvm_codegen_SelectionDAG | -0.252605 | 0.227075 | 0.292179 | 0 | True | False |
| rpm-baseline/real_aarch64_llvm_mc_AsmParser | -0.191430 | 0.953444 | 0.556109 | 0 | True | False |
| rpm-baseline/real_aarch64_llvm_mc_MasmParser | 0.216152 | 0.318950 | 0.770228 | 0 | True | False |
| rpm-baseline/real_aarch64_llvm_sema_SemaExprCXX | -0.472055 | 0.370793 | 0.343866 | 0 | True | False |
| rpm-baseline/real_aarch64_llvm_sema_SemaStmt | -0.305709 | 0.414494 | 0.238158 | 0 | True | False |
| rpm-baseline/real_aarch64_llvm_transforms_Attributor | 0.026673 | 0.204417 | 0.081231 | 0 | True | False |
| rpm-baseline/real_aarch64_llvm_transforms_WholeProgramDevirt | -0.200537 | 0.486206 | 0.196995 | 0 | True | False |
| rpm-baseline/ld.lld | 0.638875 | 0.190587 | 0.589032 | 0 | True | True |
| rpm-baseline/llvm-ar | 0.704295 | 1.464781 | 0.992420 | 0 | True | True |
| bolt-v1/real_aarch64_llvm_arm_ARMISelLowering | 0.346391 | 0.614194 | 0.751905 | 0 | True | False |
| bolt-v1/real_aarch64_llvm_arm_ARMTargetTransformInfo | 0.439985 | 0.665146 | 0.134914 | 0 | True | False |
| bolt-v1/real_aarch64_llvm_codegen_MachinePipeliner | 0.140554 | 0.390658 | 0.447697 | 0 | True | False |
| bolt-v1/real_aarch64_llvm_codegen_SelectionDAG | 0.390312 | 0.303942 | 0.341410 | 0 | True | False |
| bolt-v1/real_aarch64_llvm_mc_AsmParser | -0.053468 | 0.538298 | 1.598745 | 0 | True | False |
| bolt-v1/real_aarch64_llvm_mc_MasmParser | -0.104021 | 1.030457 | 0.771949 | 0 | True | False |
| bolt-v1/real_aarch64_llvm_sema_SemaExprCXX | -0.380244 | 0.213222 | 0.633519 | 0 | True | False |
| bolt-v1/real_aarch64_llvm_sema_SemaStmt | 0.135857 | 0.225666 | 0.432807 | 0 | True | False |
| bolt-v1/real_aarch64_llvm_transforms_Attributor | 0.022062 | 0.439523 | 0.470640 | 0 | True | False |
| bolt-v1/real_aarch64_llvm_transforms_WholeProgramDevirt | -0.050258 | 0.167084 | 0.645826 | 0 | True | False |
| bolt-v1/ld.lld | 0.642924 | 0.247376 | 0.244317 | 0 | True | True |
| bolt-v1/llvm-ar | -1.114600 | 0.733965 | 0.901693 | 0 | True | True |
| bolt-v2/real_aarch64_llvm_arm_ARMISelLowering | 0.283497 | 0.933249 | 0.155919 | 0 | True | False |
| bolt-v2/real_aarch64_llvm_arm_ARMTargetTransformInfo | 0.557292 | 0.785272 | 0.518716 | 0 | True | False |
| bolt-v2/real_aarch64_llvm_codegen_MachinePipeliner | -0.150978 | 0.457015 | 0.251340 | 0 | True | False |
| bolt-v2/real_aarch64_llvm_codegen_SelectionDAG | -0.014764 | 0.554240 | 0.346329 | 0 | True | False |
| bolt-v2/real_aarch64_llvm_mc_AsmParser | 0.002433 | 1.023271 | 0.477694 | 0 | True | False |
| bolt-v2/real_aarch64_llvm_mc_MasmParser | 0.552435 | 0.648475 | 0.956656 | 0 | True | False |
| bolt-v2/real_aarch64_llvm_sema_SemaExprCXX | -0.094490 | 0.133135 | 0.616542 | 0 | True | False |
| bolt-v2/real_aarch64_llvm_sema_SemaStmt | -0.009036 | 0.521876 | 0.080645 | 0 | True | False |
| bolt-v2/real_aarch64_llvm_transforms_Attributor | 0.405849 | 0.691989 | 0.426171 | 0 | True | False |
| bolt-v2/real_aarch64_llvm_transforms_WholeProgramDevirt | -0.015794 | 0.483442 | 0.093885 | 0 | True | False |
| bolt-v2/ld.lld | 0.308035 | 0.182101 | 0.300958 | 0 | True | True |
| bolt-v2/llvm-ar | 0.147793 | 1.077926 | 1.196564 | 0 | True | True |

**calibration-run1（校准/诊断，训练集）**

| 项 | RPM s | v1 s | v2 s | v2/v1 | v2/RPM | v1/RPM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| real_aarch64_llvm_arm_ARMISelLowering | 8.447398 | 7.309997 | 7.272809 | 0.994913 | 0.860953 | 0.865355 |
| real_aarch64_llvm_arm_ARMTargetTransformInfo | 4.853891 | 4.039466 | 4.014194 | 0.993744 | 0.827005 | 0.832212 |
| real_aarch64_llvm_codegen_MachinePipeliner | 6.194106 | 5.360762 | 5.348587 | 0.997729 | 0.863496 | 0.865462 |
| real_aarch64_llvm_codegen_SelectionDAG | 7.109806 | 6.117153 | 6.080513 | 0.994010 | 0.855229 | 0.860383 |
| real_aarch64_llvm_mc_AsmParser | 2.715539 | 2.311817 | 2.309708 | 0.999088 | 0.850552 | 0.851329 |
| real_aarch64_llvm_mc_MasmParser | 3.381791 | 2.917337 | 2.893394 | 0.991793 | 0.855580 | 0.862660 |
| real_aarch64_llvm_sema_SemaExprCXX | 5.981713 | 4.987438 | 4.961806 | 0.994861 | 0.829496 | 0.833781 |
| real_aarch64_llvm_sema_SemaStmt | 5.724266 | 4.805534 | 4.788584 | 0.996473 | 0.836541 | 0.839502 |
| real_aarch64_llvm_transforms_Attributor | 6.459480 | 5.510092 | 5.464382 | 0.991704 | 0.845948 | 0.853024 |
| real_aarch64_llvm_transforms_WholeProgramDevirt | 5.822379 | 4.960278 | 4.939562 | 0.995824 | 0.848375 | 0.851933 |
| ld.lld | 0.004676 | 0.004667 | 0.004682 | 1.003324 | 1.001423 | 0.998105 |
| llvm-ar | 0.002317 | 0.002309 | 0.002318 | 1.003902 | 1.000502 | 0.996614 |

整轮wall 1123.299497s，所有命令最大RSS 1187680KiB，scratch_removed=True，状态 MEASURED。
该轮编译项最大CV 1.030457%，保留suspect样本 0；均如实披露，不调整样本或追加重试。
fixture hash：`30acab6c36503bcf53f5ad6467d17a58ede7f0205f95f68dedd1125494a9096a`。


**calibration-run2（校准/诊断，训练集）**

| 项 | RPM s | v1 s | v2 s | v2/v1 | v2/RPM | v1/RPM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| real_aarch64_llvm_arm_ARMISelLowering | 8.471188 | 7.335318 | 7.293427 | 0.994289 | 0.860969 | 0.865914 |
| real_aarch64_llvm_arm_ARMTargetTransformInfo | 4.849547 | 4.057239 | 4.036565 | 0.994904 | 0.832359 | 0.836622 |
| real_aarch64_llvm_codegen_MachinePipeliner | 6.245829 | 5.368297 | 5.340512 | 0.994824 | 0.855052 | 0.859501 |
| real_aarch64_llvm_codegen_SelectionDAG | 7.091846 | 6.141029 | 6.079616 | 0.989999 | 0.857268 | 0.865928 |
| real_aarch64_llvm_mc_AsmParser | 2.710341 | 2.310581 | 2.309764 | 0.999646 | 0.852204 | 0.852506 |
| real_aarch64_llvm_mc_MasmParser | 3.389101 | 2.914302 | 2.909379 | 0.998310 | 0.858451 | 0.859904 |
| real_aarch64_llvm_sema_SemaExprCXX | 5.953476 | 4.968474 | 4.957117 | 0.997714 | 0.832643 | 0.834550 |
| real_aarch64_llvm_sema_SemaStmt | 5.706767 | 4.812062 | 4.788151 | 0.995031 | 0.839030 | 0.843220 |
| real_aarch64_llvm_transforms_Attributor | 6.461203 | 5.511308 | 5.486559 | 0.995510 | 0.849155 | 0.852985 |
| real_aarch64_llvm_transforms_WholeProgramDevirt | 5.810703 | 4.957785 | 4.938782 | 0.996167 | 0.849946 | 0.853216 |
| ld.lld | 0.004706 | 0.004697 | 0.004697 | 0.999986 | 0.998131 | 0.998146 |
| llvm-ar | 0.002333 | 0.002283 | 0.002321 | 1.016718 | 0.994973 | 0.978613 |

整轮wall 1124.793698s，所有命令最大RSS 1519796KiB，scratch_removed=True，状态 MEASURED。
该轮编译项最大CV 1.598745%，保留suspect样本 0；均如实披露，不调整样本或追加重试。
fixture hash：`30acab6c36503bcf53f5ad6467d17a58ede7f0205f95f68dedd1125494a9096a`。


**formal（正式，训练集）**

| 项 | RPM s | v1 s | v2 s | v2/v1 | v2/RPM | v1/RPM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| real_aarch64_llvm_arm_ARMISelLowering | 8.438910 | 7.343373 | 7.278924 | 0.991224 | 0.862543 | 0.870180 |
| real_aarch64_llvm_arm_ARMTargetTransformInfo | 4.855412 | 4.065625 | 4.031945 | 0.991716 | 0.830402 | 0.837339 |
| real_aarch64_llvm_codegen_MachinePipeliner | 6.263552 | 5.319307 | 5.330985 | 1.002195 | 0.851112 | 0.849248 |
| real_aarch64_llvm_codegen_SelectionDAG | 7.093354 | 6.139232 | 6.089964 | 0.991975 | 0.858545 | 0.865491 |
| real_aarch64_llvm_mc_AsmParser | 2.720540 | 2.322423 | 2.313845 | 0.996306 | 0.850509 | 0.853662 |
| real_aarch64_llvm_mc_MasmParser | 3.363032 | 2.907811 | 2.916760 | 1.003077 | 0.867301 | 0.864640 |
| real_aarch64_llvm_sema_SemaExprCXX | 5.966504 | 4.987024 | 4.968548 | 0.996295 | 0.832740 | 0.835837 |
| real_aarch64_llvm_sema_SemaStmt | 5.743241 | 4.803865 | 4.760811 | 0.991038 | 0.828942 | 0.836438 |
| real_aarch64_llvm_transforms_Attributor | 6.463722 | 5.536046 | 5.493079 | 0.992239 | 0.849832 | 0.856480 |
| real_aarch64_llvm_transforms_WholeProgramDevirt | 5.816193 | 4.956923 | 4.944872 | 0.997569 | 0.850191 | 0.852263 |
| ld.lld | 0.004701 | 0.004697 | 0.004703 | 1.001281 | 1.000573 | 0.999292 |
| llvm-ar | 0.002319 | 0.002324 | 0.002308 | 0.992983 | 0.995457 | 1.002492 |

整轮wall 1125.553400s，所有命令最大RSS 1187680KiB，scratch_removed=True，状态 MEASURED。
该轮编译项最大CV 1.390181%，保留suspect样本 0；均如实披露，不调整样本或追加重试。
fixture hash：`30acab6c36503bcf53f5ad6467d17a58ede7f0205f95f68dedd1125494a9096a`。

#### 7.1.4 原始记录与自检

全部原始输出在本节冻结的 `temp/bench_results/bolt-final-split-20260921/`：
`host-before.json`、`preregistration-git.txt`、`attempt.json`、`loadavg.jsonl`、`loadavg-summary.json`，
以及两目标目录中的命令、日志、每样本JSON/Markdown；逐项派生摘要在
`temp/final-calibration-prereg-20260921/final-results-summary.json`。所有JSON/大日志留temp不提交。
只运行已有三个clang的基准测量；无新profile、无BOLT重写、无LLVM/Chromium构建、无spec/源码修改、无Gerrit推送。
启动前执行已push的预注册SHA核验；运行中脚本与计划未改，历史FAIL未重判；无追加尝试。

正式训练集结果的解读：AArch64 `GM(v2/v1)=0.995354`，`GM(v2/RPM)=0.848116`，
`GM(v1/RPM)=0.852074`。v2/v1点值接近1，本轮没有另设显著性或非退化检验，
不能据此宣称v2对v1的微小增量收益已经确证。ARM的两轮诊断v2/v1为1.002496、1.004235，
校准FAIL，仍不能确证ARM非退化；不重试。所有收益的最终量级和是否成立交由Quickbuild验收。

本结果更新的Git提交/push原文与main/固定提交raw校验，归档至
`temp/final-calibration-prereg-20260921/results-publication.log`、`results-publication-verification.json`。
冻结脚本、计划、历史文档、spec及ELF核验见同目录 `results-validation.json`。

## 8. 待定事项（本轮不执行）

- 最终 OBS 项目与验收 Base 快照：待用户确认自研静态 spec 已进入哪个项目后固定，当前公开快照陈旧。
- lld / llvm-ar 在全平台构建中的时间占比：待用户提供 Quickbuild 全平台日志后按实际调用分析。
  链接+归档占比 **>10%** 才启动第二阶段：真实规模链接基准、lld 专用 profile、BOLT lld、
  链接产物逐字节门禁；**<5%** 则搁置。5%–10%（含边界）继续待决，不擅自启动。
  不能从 Chromium 的 0.2% 或当前小夹具推断全平台占比；本轮不训练/重写 lld。

## 附录 A：上一版实验协议与 A/A 零对照（历史原判）

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

两个历史实验均直接使用当时未修改的 `tools/bench_toolchain.py`，`--calibrate` 各跑两次完整
同轮交错测量。真实输入为原训练 10 个 .ii，合成 seed=73419、scale=1/2/2；没有采新
profile，也没有把留出集混入训练目录。CPU 2、ASLR off、N=5 丢首次、loadavg 阈值 10、
ARM triple、同一 S sysroot、同一 `TC/lib64/clang/22` 资源目录，逐编译进程 4 GiB AS。
夹具由每个实验的第一个工具链（RPM 基线）生成，64 shards 加 A/C 共66 objects，三者共用；lld 每样本
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
该历史实验不追着噪声门禁重跑，不因失败改协议；原有门禁为各工具/负载跨轮 wall 中位数差
≤3%、每轮 CV≤3%、无保留的高负载可疑样本，见历史提交 `16aa9370e995ba543ee2189454d08b8ca13508d0` 的 `tools/bench_toolchain.py:454–473`。

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
该历史实验没有再引入未经打包的 ordinary-build ELF，所以不虚称完全分离了每一种后处理。
这些比值都不包含 BOLT 重写本身，不能用来直接宣布新的 BOLT 净收益。

**实测：两轮完整执行；原 3% 校准门禁 PASS，最大跨轮差 1.986133%。**
分母为同工具链同项目的 run1 wall 中位数。结果按诊断实验记录；没有追加正式轮或改协议重试。
总阶段 wall 2959.254 s，开始 2026-09-21T17:47:14.631918+08:00，结束 2026-09-21T18:36:33.907802+08:00。
未剥离 ELF 的全部 13 个编译项在 4 GiB AS 下完成；未触发容量失败，未放宽限制。

| 轮 | 完整轮 wall s | 全命令峰值RSS KiB | 最大CV | 可疑保留样本 | 夹具/产物回收 |
| --- | ---: | ---: | ---: | ---: | --- |
| 1 | 1487.877 | 1188744 | 2.409033% | 0 | 是 |
| 2 | 1466.421 | 1527232 | 2.207152% | 0 | 是 |

全部组合通过既定门禁；该历史实验仍只回答中间处理对照，不把它当作新的 BOLT/Chromium 验收。

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
这不等于证明精确零影响；也不能用该历史实验 S/P 去除历史 docs/16 的 B/P，跨轮反算所谓
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

## 附录 D：aarch64 profile v2 实验（795a5c4 实测归档）

### D.1 固定路径、资源与输入来源

```text
W  = /home/linhao/Toolchain/development/llvm-optimize
E2 = W/temp/bolt-aarch64-v2-20260921
D2 = W/temp/bench_results/bolt-aarch64-v2-20260921
S64 = /home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.aarch64.0
TC = W/temp/toolchain-baseline/usr
Q = W/temp/bolt-measurement-20260918/run
E16 = W/temp/bolt-final-20260918
```

枚举 6 个现存 aarch64 根，见 E2/aarch64-roots.json；选与 ARM 根同系列的 S64，
有 usr/include/stdlib.h，根内 clang 的只读 ELF header 为 Machine=AArch64。未运行该异架构 clang。
实际预处理/编译均用原生 x86_64 RPM clang，显式 AArch64 triple 与 S64。证据：
E2/aarch64-sysroot-inspection.txt、preprocess/commands.log、collection.json。
启动 nproc=20，free -g available=21 GiB，磁盘 available=673 GiB；E2/preflight.log 保留主要进程。
重写/采集均采用 6 GiB MemoryMax、MemorySwapMax=0、nice15/ionice-c3，沿用 2秒进程/30秒宿主采样、
低于2GiB紧急中止与 finally 回收。编译逐个 CPU2、ASLR off、4GiB RLIMIT_AS；测量前另存 D2/*-host-before.txt。

同原训练 selection.json 的 10 个源文件，重新 -E，而非改写旧 .ii 的 target 字段。预定义宏原文摘录：

```text
#define __aarch64__ 1
__arm__ : ABSENT
__x86_64__ : ABSENT
```

首行为 target-predefined-macros.txt 原行；ABSENT 为对完整输出检索的结果。所有 sidecar 包含
target、SHA、完整原命令和 -E 命令，输出另经 ELF64/EM_AARCH64 对象格式检查。

| 文件（同名 .flags.json 配套） | 原 LLVM 源文件 | .ii 字节 | .ii SHA256 |
| --- | --- | ---: | --- |
| llvm_sema_SemaStmt | clang/lib/Sema/SemaStmt.cpp | 9088683 | `b6573be55442a2e3cb6d164a8a3c429eb31ad5c2f26fb22032747567c05f62e6` |
| llvm_sema_SemaExprCXX | clang/lib/Sema/SemaExprCXX.cpp | 10178219 | `b0e3072b0ba360c94c13fc444aedfa34b42a09f8906e243c74483ac1387b7eac` |
| llvm_codegen_SelectionDAG | llvm/lib/CodeGen/SelectionDAG/SelectionDAG.cpp | 6639918 | `9a6284c2a607318eb15d5f6eac2045dea17ee8a0337af3afc8a6ddeb2d8e8ef9` |
| llvm_codegen_MachinePipeliner | llvm/lib/CodeGen/MachinePipeliner.cpp | 6554330 | `c527c1fdba6d5fbda4c9d5f05977eeab72f57f08ecbf0dc03a88dc5283bac97e` |
| llvm_transforms_Attributor | llvm/lib/Transforms/IPO/Attributor.cpp | 5483967 | `5d8197c27f485685feb34e725618d6ac8fba2ba96905f425be84dabdef2f4e85` |
| llvm_transforms_WholeProgramDevirt | llvm/lib/Transforms/IPO/WholeProgramDevirt.cpp | 5700401 | `c683df3c5dc31263fafc6a6bdd8605e476d01ea8c79948e013417e5015218ee5` |
| llvm_arm_ARMISelLowering | llvm/lib/Target/ARM/ARMISelLowering.cpp | 8218513 | `607cdc02caa0d60e609ef484009eec36934f8571e1bd3f716b65a7cf54d0d880` |
| llvm_arm_ARMTargetTransformInfo | llvm/lib/Target/ARM/ARMTargetTransformInfo.cpp | 7606360 | `6e24b90e3d215d66afe40777370412789f2c510860cb89cf9fae140aceda9414` |
| llvm_mc_MasmParser | llvm/lib/MC/MCParser/MasmParser.cpp | 3887337 | `8fecbaf28238e7f1fc994c4b15f1963ee856b83362ad6bd5172fc1df082f50ac` |
| llvm_mc_AsmParser | llvm/lib/MC/MCParser/AsmParser.cpp | 4011311 | `065b0315c147b477df749c30774a2c56db37aeba4a61450e0c51e0205ccf4cd4` |

目录为 tools/bench_inputs/real_tu_aarch64/。仅 SemaExprCXX 大于 10,000,000 B，留在
`/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-aarch64-v2-20260921/preprocess/llvm_sema_SemaExprCXX.ii`，
sidecar 以绝对 input 引用；其余9个 .ii与10个 sidecar提交。ARM训练/留出目录未修改。

### D.2 复用插桩 ELF、10+13 合并与采集成本

复用 Q/instrumented/bin/clang-22，SHA `685b2f3706a427c674d633602cc6309c5d45aad2c31723ca6d0cdaaac74d2ea1`，**未重新插桩**。
该 ELF 内嵌 Q/profiles/clang 的 PID 前缀；每个新增 TU 产生恰好一份新 fdata，按前后文件集差登记。
原13文件前后 SHA 全相同。新增10个与原13个按明确清单 merge，不混入其他 profile。
v2 合并文件 `E2/profile-work/merged-v2.fdata` 为 **171232190 B**，
SHA `d9b132f9430dfed32e080c65b4422bd76eba4a9c2101a2b18a7f66c94133b326`。profile-v2-manifest.json记录两目标 corpus、stripped/候选/profile SHA；
profile-work/result.json记录每个 fdata路径/SHA/体积与原13文件 SHA。现有v1 merged.fdata未覆盖。

新增10组插桩编译 wall 合计 **231.662382 s**，配套一次基线合计 **58.209330 s**，
总量比 3.979815（插桩/RPM，仅采集开销诊断，非优化性能结论）。
采集含基线/审计 wall 290.375087 s，含merge总wall 296.019211 s；
10份新fdata总计 1314447043 B。原始命令与wait4数据在 profile-work/raw/。

| aarch64 TU | 基线一次 wall s | 插桩一次 wall s | 插桩/RPM | 新 fdata B |
| --- | ---: | ---: | ---: | ---: |
| real_llvm_arm_ARMISelLowering | 8.595597 | 33.754477 | 3.926950 | 141111179 |
| real_llvm_arm_ARMTargetTransformInfo | 4.868052 | 20.411787 | 4.193009 | 132294136 |
| real_llvm_codegen_MachinePipeliner | 6.270901 | 24.465758 | 3.901474 | 133466102 |
| real_llvm_codegen_SelectionDAG | 7.299528 | 28.582778 | 3.915702 | 138810522 |
| real_llvm_mc_AsmParser | 2.784819 | 13.345525 | 4.792241 | 125865652 |
| real_llvm_mc_MasmParser | 3.528278 | 14.898041 | 4.222469 | 125802060 |
| real_llvm_sema_SemaExprCXX | 6.185450 | 24.438823 | 3.951018 | 128687762 |
| real_llvm_sema_SemaStmt | 5.951124 | 23.573498 | 3.961184 | 126246302 |
| real_llvm_transforms_Attributor | 6.689295 | 25.570952 | 3.822668 | 129079440 |
| real_llvm_transforms_WholeProgramDevirt | 6.036286 | 22.620743 | 3.747460 | 133083888 |

### D.3 唯一一次纯重写：6 GiB cap

输入仍为 Q/stripped/bin/clang-22（226730672 B，SHA eccfb075…，完整值在 §3/manifest）；
与 docs/16 v1 保持相同排序/拆分选项和单线程，增加 -stale-threshold=5 准入检查：

```bash
llvm-bolt "$Q/stripped/bin/clang-22" -o "$E2/optimized-v2/bin/clang-22" \
  -data="$E2/profile-work/merged-v2.fdata" \
  -reorder-blocks=ext-tsp -reorder-functions=cdsort \
  -split-functions -split-all-cold -split-eh -dyno-stats \
  --thread-count=1 -stale-threshold=5
```

完整实际命令含 `/lib64/ld-linux-x86-64.so.2 --library-path <独立libxml2>`，
由 `tools/run_bolt_stage.py --memory-max-gib 6` 执行；精确 argv 在 E2/rewrite-scope/stage.json。

| 指标 | 实测 | 原始记录 |
| --- | --- | --- |
| llvm-bolt 自身 wall | 24.43 s | rewrite-scope/tool-time-v.txt |
| 自身 VmHWM / MaxRSS | 3857492 KiB = 3.678791 GiB | process-memory.jsonl + tool-time-v.txt，一致 |
| scope wall | 26.324582 s | outcome.json |
| scope MemoryPeak / MemoryMax | 3886170112 / 6442450944 B | scope-after-rpm.json |
| memory.events | max=0、oom=0、oom_kill=0、oom_group_kill=0 | scope-after-rpm.json |
| 宿主采样最低 MemAvailable | 22352379904 B；阶段不足30秒，仅1个宿主样本，不冒称连续最低值 | samples.jsonl |
| 回收 | sampler_reaped=true、log_reader_reaped=true；退出0 | outcome.json |
| bolt-v2 ELF | 218881120 B；SHA `f26b65625897189bd38ae02eb8b4cf5854ada84c08be9be3943f241dea647637` | profile-v2-manifest.json |

峰值未贴 cap且events无压力/OOM，**不是截断值**。此实测支持本输入/不更新debug的纯重写可在6GiB中完成，
不能推广成带debug更新/其他源码版本的内存保证。完整LLVM构建18GiB门禁不变。

完整 dyno-stats 在 rewrite-scope/build.log；关键原行（统计来自合并profile，不是benchmark收益）：

```text
BOLT-INFO: 23592 out of 144032 functions in the binary (16.4%) have non-empty execution profile
BOLT-INFO: 383 functions with profile could not be optimized
         17422124951 : all function calls
        815741765614 : executed instructions
        194456200794 : executed load instructions
         17422124951 : all function calls (=)
        803493495029 : executed instructions (-1.5%)
        194456200794 : executed load instructions (=)
```

非空profile 23592/144032，原v1为21802/144032；383 non-simple不能优化，不能算作stale。
本次成功日志无invalid/stale警告，未开启infer-stale；按已核验源码计stale=0，5%门禁通过。

### D.4 30 TU 字节正确性门禁

ARM训练10 + ARM留出10 + aarch64训练10，**30/30逐字节PASS**。每对都用
`clang-22 --driver-mode=g++`，同cwd/输出路径/资源头/目标sysroot，保留 -frecord-gcc-switches；
实际 cmp 比较完整 .o，不排除 .GCC.command.line。证据 correctness-30.json 和三个 equality-*/result.json、
raw/commands.json；完整对象留temp。候选先通过全部30项才启动测量。

### D.5 三工具链、23编译项同轮交错

顺序固定 rpm-baseline（TC，第一个生成共同夹具）、bolt-v1（E16/optimized）、bolt-v2（E2/optimized-v2）。
性能负载正是v2训练的23组；ARM留出10只做正确性验证，未加入本轮性能表。
因此即便校准通过，aarch64收益也仍是训练集筛选观察，需要后续服务器/独立负载验收泛化。
ARM13 + aarch6410，N=5丢首次，CPU2、ASLR off、loadavg阈值10、同clang22资源目录、
对应目标sysroot、共同66对象夹具、4GiB AS、tmpfs、lld4096/ar1024次归一化，两个完整校准轮后只在PASS时跑正式轮。
测量期间未启动其他重实验，宿主仍有桌面/开发服务；20:00–20:01 loadavg 曾超过10，随后回落。
E2/host-during-200004.txt、host-during-200129.txt保存环境切片；不能据此断言某个进程是噪声根因。
高负载样本按原协议保留，任何门禁失败均照实报告。
没有拿docs/13或16历史轮当对照。v2/v1只有profile训练覆盖与布局变化（stale参数只作准入检查）；
v1/RPM、v2/RPM仍包含先前重链/剥离/BOLT，不能全部称纯BOLT。输入和分析口径在测量前由 E2/analysis-policy.json 冻结。

新协议校准 **FAIL**，编译项噪声底 **3.334074%**；69个编译组合参与门禁，6个lld/ar组合仅诊断。
protocol hash `872c7c39219bb89c638affef7a810fe7ef92d895e6b716a9bbfa47571a8b5694`。
未通过项如下。按门禁不执行正式轮，不追加尝试、不更换负载或放宽阈值；下面两轮仅作诊断。

| 工具链/项 | 跨轮差% | CV1% | CV2% | 可疑样本 |
| --- | ---: | ---: | ---: | ---: |
| rpm-baseline/A | 1.572374 | 1.997279 | 4.288191 | 0 |
| rpm-baseline/real_llvm_mc_AsmParser | -1.507503 | 2.260966 | 3.364373 | 0 |
| rpm-baseline/real_llvm_sema_SemaExprCXX | -0.937216 | 2.390141 | 3.127391 | 0 |
| rpm-baseline/real_llvm_sema_SemaStmt | 0.758636 | 2.145240 | 2.692341 | 1 |
| rpm-baseline/real_llvm_transforms_Attributor | 0.481416 | 2.489548 | 2.476116 | 1 |
| rpm-baseline/real_llvm_transforms_WholeProgramDevirt | 0.253103 | 2.916396 | 2.764534 | 1 |
| rpm-baseline/real_aarch64_llvm_arm_ARMISelLowering | -0.735394 | 4.383652 | 2.330624 | 1 |
| rpm-baseline/real_aarch64_llvm_arm_ARMTargetTransformInfo | 1.663413 | 1.614572 | 2.395570 | 1 |
| rpm-baseline/real_aarch64_llvm_codegen_MachinePipeliner | 1.048930 | 1.534585 | 1.897657 | 1 |
| rpm-baseline/real_aarch64_llvm_transforms_Attributor | 3.334074 | 0.247380 | 1.844160 | 0 |
| bolt-v1/A | 1.506848 | 1.532678 | 3.916657 | 0 |
| bolt-v1/real_llvm_mc_AsmParser | -0.530714 | 2.511967 | 3.837387 | 0 |
| bolt-v1/real_llvm_sema_SemaExprCXX | -1.379070 | 3.503220 | 2.866641 | 0 |
| bolt-v1/real_llvm_sema_SemaStmt | 0.532391 | 2.833085 | 2.920411 | 1 |
| bolt-v1/real_llvm_transforms_Attributor | 0.830446 | 2.284438 | 3.195697 | 1 |
| bolt-v1/real_llvm_transforms_WholeProgramDevirt | 0.353536 | 4.483450 | 2.843538 | 1 |
| bolt-v1/real_aarch64_llvm_arm_ARMISelLowering | 0.460457 | 3.211396 | 2.129063 | 1 |
| bolt-v1/real_aarch64_llvm_arm_ARMTargetTransformInfo | 1.872777 | 3.418220 | 3.395321 | 1 |
| bolt-v1/real_aarch64_llvm_mc_AsmParser | -0.913987 | 2.627485 | 3.095729 | 0 |
| bolt-v1/real_aarch64_llvm_mc_MasmParser | 0.319571 | 3.259768 | 2.749543 | 0 |
| bolt-v1/real_aarch64_llvm_transforms_Attributor | 3.080342 | 0.248965 | 1.720630 | 0 |
| bolt-v1/real_aarch64_llvm_transforms_WholeProgramDevirt | 3.247547 | 0.569306 | 2.352958 | 0 |
| bolt-v2/A | 0.579580 | 1.497007 | 4.149575 | 0 |
| bolt-v2/real_llvm_sema_SemaStmt | -0.716481 | 1.902002 | 2.517028 | 1 |
| bolt-v2/real_llvm_transforms_Attributor | 0.820916 | 2.740070 | 2.505753 | 1 |
| bolt-v2/real_llvm_transforms_WholeProgramDevirt | 1.110782 | 2.330116 | 2.627556 | 1 |
| bolt-v2/real_aarch64_llvm_arm_ARMISelLowering | -1.142517 | 2.976791 | 2.450835 | 1 |
| bolt-v2/real_aarch64_llvm_arm_ARMTargetTransformInfo | 1.132051 | 3.267331 | 2.342504 | 1 |

| 轮次 | 目标/项数 | GM(v2/v1) | GM(v2/RPM) | GM(v1/RPM) |
| --- | --- | ---: | ---: | ---: |
| calibration-run1 | armv7l / 13 | 1.004010 | 0.855496 | 0.852079 |
| calibration-run1 | aarch64 / 10 | 0.996174 | 0.849719 | 0.852982 |
| calibration-run2 | armv7l / 13 | 1.000433 | 0.855538 | 0.855168 |
| calibration-run2 | aarch64 / 10 | 0.990335 | 0.847250 | 0.855518 |

所有比值分母如列名，均为同轮wall中位数之比，GM不含lld/ar。<1为耗时降低，>1为耗时增加。
两目标分别报告，不能用aarch64收益掩盖ARM退化；也不能把训练负载结果外推到Chromium/全平台。

**对本轮两个性能问题的回答：均未确证。** ARM 的 v2/v1 几何平均依轮次为 1.004010 / 1.000433；这些点值不足以证明 v2 不劣于 v1。
AArch64 的 v2/v1 依轮次为 0.996174 / 0.990335，v2/RPM 为 0.849719 / 0.847250；仅为未通过校准的数据描述。
两轮不能合并包装成正式收益，也不能从相近点值宣称等效。没有生成正式轮 JSON；
profile v2、纯重写容量和 30 TU 正确性已完成，但性能认证及生产发布授权均未获得。

**calibration-run1逐项表**（校准/诊断；单位s）：

| 目标/项 | RPM | v1 | v2 | v2/v1 | v2/RPM | v1/RPM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| armv7l/A | 8.591445 | 7.660944 | 7.736480 | 1.009860 | 0.900486 | 0.891695 |
| armv7l/B | 2.235561 | 1.724092 | 1.744825 | 1.012025 | 0.780486 | 0.771212 |
| armv7l/C | 6.113277 | 5.842214 | 5.838570 | 0.999376 | 0.955064 | 0.955660 |
| armv7l/real_llvm_arm_ARMISelLowering | 8.422611 | 7.245890 | 7.334838 | 1.012276 | 0.870851 | 0.860290 |
| armv7l/real_llvm_arm_ARMTargetTransformInfo | 4.873971 | 4.037495 | 4.053651 | 1.004001 | 0.831694 | 0.828379 |
| armv7l/real_llvm_codegen_MachinePipeliner | 6.290165 | 5.373172 | 5.434182 | 1.011355 | 0.863917 | 0.854218 |
| armv7l/real_llvm_codegen_SelectionDAG | 6.961876 | 5.948444 | 5.962165 | 1.002307 | 0.856402 | 0.854431 |
| armv7l/real_llvm_mc_AsmParser | 2.736538 | 2.304279 | 2.303134 | 0.999503 | 0.841623 | 0.842042 |
| armv7l/real_llvm_mc_MasmParser | 3.375285 | 2.896913 | 2.899271 | 1.000814 | 0.858971 | 0.858272 |
| armv7l/real_llvm_sema_SemaExprCXX | 6.162586 | 5.130145 | 5.151505 | 1.004164 | 0.835932 | 0.832466 |
| armv7l/real_llvm_sema_SemaStmt | 5.951580 | 4.995422 | 4.977908 | 0.996494 | 0.836401 | 0.839344 |
| armv7l/real_llvm_transforms_Attributor | 6.433878 | 5.456119 | 5.478992 | 1.004192 | 0.851585 | 0.848030 |
| armv7l/real_llvm_transforms_WholeProgramDevirt | 5.889523 | 5.021477 | 5.001167 | 0.995955 | 0.849163 | 0.852612 |
| aarch64/real_aarch64_llvm_arm_ARMISelLowering | 8.814108 | 7.573215 | 7.601347 | 1.003715 | 0.862407 | 0.859215 |
| aarch64/real_aarch64_llvm_arm_ARMTargetTransformInfo | 5.015915 | 4.210423 | 4.165679 | 0.989373 | 0.830492 | 0.839413 |
| aarch64/real_aarch64_llvm_codegen_MachinePipeliner | 6.406448 | 5.518888 | 5.488370 | 0.994470 | 0.856695 | 0.861458 |
| aarch64/real_aarch64_llvm_codegen_SelectionDAG | 7.284095 | 6.337867 | 6.297278 | 0.993596 | 0.864524 | 0.870097 |
| aarch64/real_aarch64_llvm_mc_AsmParser | 2.818656 | 2.416732 | 2.404029 | 0.994744 | 0.852899 | 0.857406 |
| aarch64/real_aarch64_llvm_mc_MasmParser | 3.511478 | 3.015368 | 3.006068 | 0.996916 | 0.856069 | 0.858718 |
| aarch64/real_aarch64_llvm_sema_SemaExprCXX | 6.190147 | 5.194066 | 5.138089 | 0.989223 | 0.830043 | 0.839086 |
| aarch64/real_aarch64_llvm_sema_SemaStmt | 5.911178 | 4.937040 | 4.936168 | 0.999823 | 0.835057 | 0.835204 |
| aarch64/real_aarch64_llvm_transforms_Attributor | 6.609706 | 5.676388 | 5.640950 | 0.993757 | 0.853434 | 0.858796 |
| aarch64/real_aarch64_llvm_transforms_WholeProgramDevirt | 5.969032 | 5.080426 | 5.112245 | 1.006263 | 0.856461 | 0.851131 |
| diagnostic/ld.lld | 0.004818 | 0.004834 | 0.004837 | 1.000804 | 1.004098 | 1.003292 |
| diagnostic/llvm-ar | 0.002386 | 0.002382 | 0.002397 | 1.006550 | 1.004702 | 0.998164 |

整轮wall 2168.861700s；全命令最大RSS 1188744KiB；scratch_removed=True。

**calibration-run2逐项表**（校准/诊断；单位s）：

| 目标/项 | RPM | v1 | v2 | v2/v1 | v2/RPM | v1/RPM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| armv7l/A | 8.726534 | 7.776383 | 7.781319 | 1.000635 | 0.891685 | 0.891119 |
| armv7l/B | 2.251514 | 1.750785 | 1.742668 | 0.995364 | 0.773999 | 0.777604 |
| armv7l/C | 6.093533 | 5.912437 | 5.908077 | 0.999263 | 0.969565 | 0.970281 |
| armv7l/real_llvm_arm_ARMISelLowering | 8.445427 | 7.325937 | 7.330997 | 1.000691 | 0.868043 | 0.867444 |
| armv7l/real_llvm_arm_ARMTargetTransformInfo | 4.823415 | 4.024875 | 4.041794 | 1.004204 | 0.837953 | 0.834445 |
| armv7l/real_llvm_codegen_MachinePipeliner | 6.234453 | 5.316471 | 5.331122 | 1.002756 | 0.855107 | 0.852757 |
| armv7l/real_llvm_codegen_SelectionDAG | 6.936735 | 5.906305 | 5.906131 | 0.999970 | 0.851428 | 0.851453 |
| armv7l/real_llvm_mc_AsmParser | 2.695284 | 2.292050 | 2.303448 | 1.004973 | 0.854622 | 0.850393 |
| armv7l/real_llvm_mc_MasmParser | 3.356611 | 2.898945 | 2.898228 | 0.999753 | 0.863439 | 0.863652 |
| armv7l/real_llvm_sema_SemaExprCXX | 6.104830 | 5.059397 | 5.092465 | 1.006536 | 0.834170 | 0.828753 |
| armv7l/real_llvm_sema_SemaStmt | 5.996731 | 5.022017 | 4.942242 | 0.984115 | 0.824156 | 0.837459 |
| armv7l/real_llvm_transforms_Attributor | 6.464851 | 5.501429 | 5.523970 | 1.004097 | 0.854462 | 0.850975 |
| armv7l/real_llvm_transforms_WholeProgramDevirt | 5.904430 | 5.039230 | 5.056719 | 1.003471 | 0.856428 | 0.853466 |
| aarch64/real_aarch64_llvm_arm_ARMISelLowering | 8.749290 | 7.608087 | 7.514500 | 0.987699 | 0.858870 | 0.869566 |
| aarch64/real_aarch64_llvm_arm_ARMTargetTransformInfo | 5.099351 | 4.289274 | 4.212837 | 0.982179 | 0.826152 | 0.841141 |
| aarch64/real_aarch64_llvm_codegen_MachinePipeliner | 6.473647 | 5.589639 | 5.621427 | 1.005687 | 0.868355 | 0.863445 |
| aarch64/real_aarch64_llvm_codegen_SelectionDAG | 7.344153 | 6.368397 | 6.345431 | 0.996394 | 0.864011 | 0.867138 |
| aarch64/real_aarch64_llvm_mc_AsmParser | 2.796975 | 2.394643 | 2.379178 | 0.993542 | 0.850625 | 0.856155 |
| aarch64/real_aarch64_llvm_mc_MasmParser | 3.480802 | 3.025005 | 3.004935 | 0.993365 | 0.863288 | 0.869054 |
| aarch64/real_aarch64_llvm_sema_SemaExprCXX | 6.242838 | 5.243241 | 5.106426 | 0.973906 | 0.817965 | 0.839881 |
| aarch64/real_aarch64_llvm_sema_SemaStmt | 6.053091 | 5.077425 | 4.992610 | 0.983296 | 0.824803 | 0.838815 |
| aarch64/real_aarch64_llvm_transforms_Attributor | 6.830079 | 5.851240 | 5.797482 | 0.990813 | 0.848816 | 0.856687 |
| aarch64/real_aarch64_llvm_transforms_WholeProgramDevirt | 6.141708 | 5.245415 | 5.228845 | 0.996841 | 0.851367 | 0.854064 |
| diagnostic/ld.lld | 0.005060 | 0.005057 | 0.004991 | 0.987004 | 0.986381 | 0.999369 |
| diagnostic/llvm-ar | 0.002417 | 0.002437 | 0.002459 | 1.009207 | 1.017720 | 1.008435 |

整轮wall 2192.502768s；全命令最大RSS 1519832KiB；scratch_removed=True。

### D.6 复现入口与证据索引

交付 `collect_llvm_real_tu.py --target aarch64-tizen-linux-gnu`、
`extend_bolt_profile_aarch64.py`、`measure_bolt_aarch64.py`（rewrite/verify/calibrate/measure四阶段）。
各脚本 --help 给参数；每阶段拒绝覆盖旧证据，profile采集入口要求恰好13个原fdata，
本实验已完成后不应直接再次采集进该目录。现有二进制的profile前缀不可通过CLI随意更换；
新实验需独占、认证过的输入/证据，不能为重试删除既有现场。

| E2/D2 路径 | 内容 |
| --- | --- |
| E2/preflight.log、aarch64-roots.json、aarch64-sysroot-inspection.txt | 实际资源/根枚举与架构 |
| E2/preprocess/ | 全部-E命令、宏、10个输入与sidecar计划 |
| E2/profile-work/result.json、raw/ | 10次baseline+instrumented编译、23文件合并与哈希 |
| E2/collect-scope/、rewrite-scope/ | cap/命令/time/VmHWM/cgroup/采样/回收，完整dyno-stats |
| E2/profile-v2-manifest.json、correctness-30.json、equality-*/ | 输入/候选/profile身份、30个完整对象cmp |
| E2/analysis-policy.json、pipeline.json、experiment-summary.json | 前置分析规则、阶段退出/时间、派生比值 |
| D2/*-launch.json、*-host-before.txt、*.json、*-raw/；E2/host-during-*.txt | 精确同轮三方命令、宿主状态、每样本wall/user/sys/RSS/load与校准 |
| E2/binfmt-registry.txt、identity-tests.log、identity-v2.txt | 宿主真实注册、49项正负测试、v2只读ELF身份 |
| E2/harness-tests.log、all-tool-tests.log、acceptance-rule-tests.json | 编译门禁16项、工具原回归35项、八轮简单规则6项 |
| E2/protected-before.json、protected-after.json、publication-verification.json | 原有资产保护与最终GitHub发布核验 |

## 附录 E：R01–R22 处置与本版延续

编号沿用 docs/19 的合并追踪编号，不声称等于三家原始评审编号。“采纳”区分设计契约、
本轮代码/实验与未来试包验收；所有请求的本轮实现完成后才标完成，不把未来 OBS 验收
说成已完成。

| 严重度 | 编号 | 最终处置 | 本文/交付依据 |
| --- | --- | --- | --- |
| 阻塞 | R01 | 采纳；停止门禁已按用户最新指令解除 | §1 完整流水线、陈旧快照、多级 hash；最终新快照待 OBS 项目确定 |
| 高 | R02 | 采纳；完整设计 | §2 单 clang 重放、rsp/cwd、_toolchain 准入、隔离失败降级 |
| 高 | R03 | 采纳；首版不改 branding | §1.3 Release+可信清单+节区+worker 实际路径 |
| 高 | R04 | 采纳；自举与认证流程已定 | §3 本机有界 22 GiB、双目标 23 训练组、维护者责任、5% stale/10% coverage、双输入 SHA |
| 高 | R05 | 采纳；独立 noarch RPM | §2.1、§3.2 两套入队依赖、无 profile 预期普通包 |
| 高 | R06 | 采纳；固定状态/安装清单 | §4.1–4.2 原子 JSON、build 写/install 读/check 只读；缺损 fail-open |
| 高 | R07 | 采纳；别名事务与转换门禁 | §1.2、§4.2 软硬链接与 brp；附录 C 实测 patchelf；完整试包仍是发货条件 |
| 高 | R08 | 采纳；容量指纹与例外隔离 | §2.3 新指纹先认证；22 GiB 不泄漏完整 18 GiB 构建门禁 |
| 高 | R10 | 采纳；口径已统一 | §5 逐轮正式/诊断、训练/留出、分母；20 TU 与文件体积差边界 |
| 高 | R11 | 采纳；完整验收模板 | §6 固定八轮、简单配对规则/停止、CPU第二口径、exec trace、5/2/3%资源预算 |
| 高 | R12 | 采纳；发货硬条件 | §4.4 消费者静态链接验收或剔除 llvm-static-devel，未冒称已修复 |
| 高 | R13 | 采纳；脚本/实机测试完成 | Machine/uname + binfmt、真实 ARM 正例、自动 no-exec |
| 高 | R14 | 采纳；脚本/实机测试完成 | 完整动态段与 NEEDED，动态快照 YES/静态基线 NO |
| 高 | R15 | 采纳；脚本/测试完成 | expect-bolt 三态及失配非零 |
| 高 | R16 | 采纳；脚本/测试完成 | RPM 仅信息、WRAPPER=YES/exit3，不执行 wrapper |
| 高 | R17 | 采纳；脚本/故障注入完成 | awk/stat/readelf/uname 错误 UNKNOWN/exit2 |
| 高 | R18 | 采纳；脚本/测试完成 | -x 检查，不可执行输入退出2 |
| 高 | R20 | 采纳；测试代码随本轮推送 | 49/49 PASS，含 binfmt mock、真实正负 ELF 与故障注入 |
| 中 | R09 | 采纳；PGO 口径修正 | §2.3 废弃加法模型，开发机暂缓，待服务器重估，可与 BOLT 叠加 |
| 中 | R19 | 采纳；usage/测试完成 | timeout 可选，缺失时原生版本查询也通过 |
| 中 | R21 | 采纳；完整 A/A 实验 | 附录 A；按实际门禁标记，失败数据亦保留，不追噪声 |
| 中 | R22 | 采纳；三方交错实验 | 附录 B；固定4GiB AS，无放宽，完整比值及混杂边界 |

## 附录 F：上一版原始记录与本版检查/发布

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

上述 E/D 表是上一版历史归档，原文件不重算、不覆盖。该版的 A/A FAIL、relocs PASS、
patchelf PASS 仍保持原判。795a5c4 的双目标实验与该版检查存附录 D 的 E2/D2；本次预注册不覆盖这些记录。

795a5c4 自检（历史）：不改 spec/LLVM 源码、不做 PGO/完整重建、不重新插桩、不构建 Chromium、不推 Gerrit。
只使用已批准的预处理、已有插桩 clang 训练、一次 6 GiB 纯 BOLT 重写与基准测量。
完整构建 18 GiB 门禁保持文件 hash 不变。原始 profile/旧候选均只读保护，新增 fdata 因现有
插桩二进制内嵌 PID 输出前缀而在原 profiles 目录新增文件，并逐个登记，不覆盖旧 13 文件。
提交只包含本次文档、工具与≤10 MB的配套输入；日志、profile、ELF、JSON 保留 temp。
GitHub push 与 main/固定提交 raw 校验的结果见 E2/publication-verification.json（发布后生成）。

ea7d120预注册阶段自检（历史）：该提交时未启动校准或正式测量，等待用户确认；未执行clang编译、profile采集或BOLT。
未改 spec/LLVM源码/完整构建18GiB门禁，不构建Chromium、不推Gerrit。
`tools/test_final_bolt_calibration.py` **16项PASS**（直接执行§6.3文档公式，含d=0.11中止、
d=0.09继续、d=0.10边界、严格小于、启动load正负例、独立目标/不重试、回收、冻结身份）；
`tools/test_bench_toolchain.py` **17项PASS**（包括13/10目标筛选及原门禁/资源检查）。
测试记录、只读检查及发布证据：
`/home/linhao/Toolchain/development/llvm-optimize/temp/final-calibration-prereg-20260921/`。
同目录的preregistration.json记录预注册SHA与Git时间；其NOT_RUN是预注册当时状态，当前执行记录以§7.1及D-final/attempt.json为准。
其中D-final为`temp/bench_results/bolt-final-split-20260921`。

本次执行自检：预注册之后获用户确认才启动；启动load≤3；按目标独立完成两轮；
ARM失败跳过正式轮，AArch64通过后只跑一轮正式测量；全程无参数调整或重试。
采样器已回收，五轮scratch_removed均为true；不改spec/LLVM源码、不采profile、不跑BOLT，
不构建LLVM工程或Chromium、不向Gerrit推送。本机校准结束，转三家评审与Quickbuild。
