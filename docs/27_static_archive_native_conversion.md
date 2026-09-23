# 27 静态库 bitcode 转机器码：离线转换通过，消费者入口失败后停止

日期：2026-09-24（+08:00）；起点提交 `773543edff23541e2489e403f66cfa0b436f9fac`。
本报告自包含；docs/25、docs/26 原文不改。

**225 个含 bitcode 的归档全部完成离线转换：3,853 个 bitcode 成员转成 x86_64 ELF ET_REL，11 个既有机器码成员逐字节保留。**
成员数量、次序、同名成员身份及完整索引检查均通过，生成的索引共 318,543 条。
但第一项程序 A 消费者验证因**本次测试入口实现错误**失败，实际尚未进入 GNU ld 链接。
按用户“第一段任一项失败即停止”收尾：**没有重试、没有修改 spec、没有认证入口变更、完整构建 0 次**。

因此：离线格式/索引转换 **PASS**；GNU ld 无 LTO/无插件消费者兼容性 **未验证**；完整方案及 RPM 发货资格 **尚未通过**。
本次失败不证明转换后的库不能被 GNU ld 链接，也不能将未执行的链接/共享库验收记为通过。

## 0. 方案变更、独占与路径

用户本轮明确将兼容 GNU ld（不启用 LTO、不带插件）作为硬条件。
单纯保留 bitcode 索引不满足这个要求；此前“重定义 __strip_install_post、只 strip 纯机器码归档”方案作废。
新方向是在 `%install` 尾部将 bitcode 成员转为机器码、确定性重新归档，然后**保留原 RPM 宏和 brp-strip-static-archive**。
libarcher_static.a 一并纳入；compiler-rt 的 45 个纯机器码归档不转换。工具原有构建/链接保持不变。
本轮只执行了这一方案的离线部分，未将设计方向冒充已应用的 spec 修复。

| 别名 | 路径 |
| --- | --- |
| W | `/home/linhao/Toolchain/development/llvm-optimize` |
| E | `W/temp/static-native-conversion-20260924`，本次全部新证据 |
| P26 | `W/temp/archive-index-fix-rpm-20260923` |
| H | `P26/baseline-rpm-extract`，本轮复核后使用的唯一 RPM 基线内容 |
| C | `E/conversion`；转换归档在 `C/archives/usr/lib64/` |
| RT | `W/temp/toolchain-runtime-baseline/libxml2/usr/lib64`，独立 libxml2 运行库 |
| R0 | `W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0` |
| S | `W/temp/llvm-archivefix-trial`，分支 archive-fix-trial |
| Rnew | `W/temp/gbs-root-x86_64-archivefix`，未初始化 GBS |

进入时主仓库 status 为空，无其他 rpmbuild/gbs/ninja/lld/ld.lld/llvm-bolt 进程。
S 的 HEAD=`f111162e94aa48ed367c9d2c039456c70e7160ae`，分支与要求一致；
spec SHA=`95887b2d060b38d5ef8f56936f7481a03d131f9d26432180a68e02ec95f0dda5`，
相对 HEAD 的完整 diff 与 docs/26 记录相同，仅三处 4/4/1 并发改动。
证据：`E/precheck.json`（含 diff、受保护文件 SHA）。

Rnew 以 O_EXCL 建锁，session=`archivefix-rpm-1a80f7b3a2b64913aaa8ee19056fbb99`、PID=1581635，
开始 `2026-09-24T00:47:19.657922+08:00`。实验、核查及报告期间持有，收尾删除并回收进程。
生命周期见 `E/lock-acquired.json`、`lock-released.json`、`final-cleanup.json`。

R0 本轮仅访问指定 RPMS 文件；未读取 BUILD、SOURCES 或 rpmdb。宏链不变，沿用 docs/26 §3 的只读取证。
不访问已隔离混合根，不使用旧全静态 BUILD，不修改 W/llvm、其 spec 或 S 的 spec。

## 1. RPM 与解包基线复核：PASS

`E/rpm-identity.json`：按 docs/26 §1 的预期 SHA 重新读取 R0 指定目录中的 22 个 RPM，**22/22 匹配**。
随后对 H 的每个包内路径，根据 `P26/baseline-file-owners.json` / 逐包 file-metadata.tsv 核对：
普通文件 SHA256、文件类型与模式、软链接目标。**17,689 个唯一包内路径，差异 0**。
证据：`E/baseline-content-check.json`、`baseline-check.log`、`check_baseline.py`。
因此复用 H，无需重新解包；基线只读，未执行 ranlib/strip/内容替换。

输入归档集合由 docs/26 普查及本轮实际 ar 解析确定：llvm-static-devel 的 225 个含 bitcode 归档，
其中 libarcher_static.a 同时属于 libomp-devel。compiler-rt 45 个没有 bitcode，转换器按实际成员扫描后跳过，输出目录中没有这 45 个归档。
归档前后身份、成员映射见 `C/members/usr/lib64/<归档>/before.json` 与 `after.json`；汇总 `E/conversion-summary.json`。

转换器为 H/usr/bin/clang-22，SHA256=`3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c`，`--version` 为 `clang version 22.1.8`。
反汇编使用同一 RPM 解包中的 llvm-dis 22.1.8。版本/哈希/命令原始输出：`E/converter-identities.json`。
显式 loader=`/lib64/ld-linux-x86-64.so.2`，运行库通过 `--library-path RT` 传入，无宿主安装或 ELF 修改。
libxml2.so.16.1.1 内容 SHA=`0d70127304264bd46387484ed7e566fc5fec96fb9c77de8c06fe0a9e9a0a8034`；来源见 docs/13 §8。

## 2. 转换规则、命令与依据

### 2.1 原优化与重定位信息

工作区 `llvm/packaging/llvm.spec:189–206` 清理原优化 flags 后追加 -O3、ThinLTO 和 omit-frame-pointer；
x86_64 Release 分支在同文件 239–242；已实测 CMAKE_CXX_FLAGS（含 -O3、-march=nehalem）见 docs/13 §7。
本轮只对已生成 IR 做常规 O3 目标文件生成，**不执行跨模块 ThinLTO 链接优化，不改工具二进制**。
同为 O3 不表示与原 ThinLTO 链接后的代码逐字节相同；本任务的库兼容性仍须消费者验收。

全部 3,853 个 bitcode 成员经过 llvm-dis 只读解析，实际值：

| 项目 | 实测 |
| --- | --- |
| target triple | 全部 x86_64-tizen-linux-gnu |
| PIC Level / PIE Level | 全部 2 / 0 |
| 有 CPU 属性的模块 | 3,826 个，均 nehalem；features 原文逐模块保留 |
| 无 CPU 属性的模块 | 27 个；另行反汇编核对，**全部没有函数定义** |
| Code Model | 没有显式标志；转换器对未认证的显式模型拒绝处理 |

原文证据：每成员目录 `ir-settings.json` 的 evidence 行；无 CPU 属性核查为
`E/cpu-attribute-check/results.json`，由 `E/check_empty_modules.py` 在受限 scope 中执行，无再次转换。
已保留的函数属性含 SSE/SSSE3/SSE4.1/SSE4.2、popcnt 等；具体集合不由宿主 CPU 推导。

源码依据（均为 W 下只读源码）：

- `llvm/clang/lib/CodeGen/CodeGenModule.cpp:1469–1474`：将 PIC/PIE 等级写入模块。
- `llvm/clang/lib/CodeGen/BackendUtil.cpp:618–631`：后端目标机器使用命令行 relocation model 与 OptimizationLevel，故转换显式传 -O3/-fPIC。
- `llvm/llvm/lib/Target/X86/X86TargetMachine.cpp:216–231`：函数自己的 target-cpu/target-features 优先于默认目标值；本轮不改写 IR 属性。

### 2.2 实际转换与归档命令

每个成员放入以归档路径、原 ordinal 命名的独立目录，原始同名成员不共用文件路径。
按 before.json 的偏移读取原 payload 并核 SHA；原机器码成员直接复制，bitcode 才运行：

```bash
/usr/bin/time -f '%e %U %S %M %x' -o <成员>/convert.time \
  prlimit --as=4294967296 --core=0 -- \
  /lib64/ld-linux-x86-64.so.2 --library-path <RT> \
  <H>/usr/bin/clang-22 --no-default-config \
  --target=x86_64-tizen-linux-gnu -x ir -O3 -c -fPIC \
  <成员>/input.bc -o <成员>/<原成员名>
```

无 -flto；`--no-default-config` 避免读取 RPM 中绝对资源路径配置；IR 输入不依赖头文件或 sysroot。
每次 llvm-dis、clang、ar 调用的完整 argv、退出码、wall/user/sys/max RSS 在对应 json/time/log 中。
本轮转换 3,853 次全部退出 0，无跳过失败或重试。

按原成员顺序传入 GNU ar（不同 ordinal 目录可包含同名文件）：

```bash
/usr/bin/ar qcDS <新归档> <成员0路径> <成员1路径> ...
/usr/bin/ar sD <新归档>
```

q 保留重复成员；D 使用确定性头部；先 S 不建索引，再 sD 对全机器码成员建完整 GNU 索引。
输出独立存放在 C/archives，绝不覆盖 H。
[转换器](../tools/convert_static_archives.py)、[资源入口](../tools/run_static_archive_conversion.py) 随本提交。
[7 项测试](../tools/test_convert_static_archives.py) 全过，包括 GNU ar 真正打包同名成员两次字节一致、
成员次序/索引身份，以及 PIC/PIE/错误目标与绝对重定位正负例。测试不构建 LLVM；原始输出 `E/conversion-tests.log`。

### 2.3 PIC 检查的精确边界

逐个输出对象验证 ELF64 little endian、e_type=ET_REL、e_machine=62。
重定位扫描只看 SHF_ALLOC 目标节，排除调试节：拒绝指向非 SHN_ABS 符号的 R_X86_64_32/32S；
拒绝只读已分配节中的绝对 R_X86_64_64。可合法用于隐藏符号/eh_frame 的 PC-relative 重定位不一概禁止。
原 11 个机器码成员也经过扫描；本轮共检查 **3,540,132** 条重定位，命中上述禁止项 **0**。
证据：每成员 `relocations.json`、`E/conversion-summary.json`；实现 `tools/convert_static_archives.py:pic_relocations()`。

**该静态筛查不替代 GNU ld -shared/-z text/-z defs 的最终 PIC 消费者验证。**
共享库项因更早的消费者入口失败而未执行，因此本轮不能宣称共享库 PIC 验收已通过。

## 3. 离线转换实测与逐归档检查

| 指标 | 实测 |
| --- | --- |
| 转换归档数 | 225/225 |
| bitcode→机器码 | 3,853/3,853 |
| 原机器码保留 | 11/11，成员 SHA 不变 |
| 转换后总成员 | 3,864，全部 x86_64 ELF ET_REL；bitcode=0 |
| 成员数量/次序/名称/同名出现次数 | 225 个归档全部匹配 |
| 索引 | 每归档恰为已定义外部 global/weak/GNU-unique 符号→成员多重集合；共 318,543 条 |
| 转换前/后总字节 | 5449996190 / 6547786320，均为未做本轮打包 strip 的大小 |
| 带调试节的成员 | 3849；这里只记录，未模拟 brp strip |
| 转换程序总 wall | 722.644133 s |
| 含 scope 启停/统计握手 wall | 724.971965 s |
| 3,853 次 clang wall 累加 / CPU 累加 | 1381.44 / 1358.80 s；前者不是并行总 wall |
| 单次转换最大 RSS | 1037536 KiB = 0.989471 GiB |
| 最大 RSS 对象 | libclangDynamicASTMatchers.a / Registry.cpp.o；wall 14.82 s |
| cgroup MemoryPeak | 7013978112 B = 6.532276 GiB，含文件缓存 |
| 宿主最低采样 MemAvailable | 15356956672 B = 14.302280 GiB |
| memory.events | max=0，oom=0，oom_kill=0 |
| scope/采样器回收 | 两组 scope 最终 inactive/dead；sampler_reaped/log_reader_reaped=true |

最大 RSS 对应的原成员名以 `C/members/usr/lib64/libclangDynamicASTMatchers.a/before.json` 为准，
完整命令/资源为该成员目录 convert.json；所有归档大小表见附录 A。
索引检查使用 `tools/inspect_llvm_archives.py`，按成员 header offset 规范化到 ordinal/name/occurrence，保留重复符号与成员身份。
本轮对象比对是转换后的索引对其自身机器码定义，不再拿旧损坏 RPM 的空索引作为正确预期。

### 3.1 限流与启动政策

转换启动时 MemAvailable=17,046,933,504 B；nproc=20；磁盘可用约 524 GiB。
离线阶段选择 `min(18, floor(MemAvailable/GiB)-4)=11 GiB`，预留至少 4 GiB，
**不调用/不修改完整 LLVM 构建容量认证或其 18 GiB 门禁**。
并发 4，每个工具进程 AS=4 GiB，MemorySwapMax=0，nice 15，ionice -c3。
沿用现有采样器：每 30 秒 free/loadavg/进程树 RSS，每 2 秒进程 VmHWM；MemAvailable<2 GiB 自动停止。
最后 shell 等待统计握手，保存 memory.events/peak 后退出；所有退出路径回收采样线程。
资源入口只导入 run_bolt_stage 的统计函数，没有运行 llvm-bolt 或 BOLT 阶段。

完整 scope 启动命令在 `E/scope/launch.json`、`stage.sh`、`offline-plan.json`，前置原始 nproc/free/df 在 `conversion-driver.log`。
实测未触发内存上限，峰值是观察到的峰值而非 OOM 截断值；这不构成未来所有归档/配置的容量上界保证。

## 4. 消费者验证：入口错误，第一项失败即停止

### 4.1 预定测试和实际执行范围

实现 [verify_native_archive_consumers.py](../tools/verify_native_archive_consumers.py) 保留了本次**失败原入口**，
用于复现证据；它不是已通过验收的发布脚本。程序 A/B 完整源码在该脚本常量及 E/consumers/a.cpp、b.cpp。

| 项目 | 设计 | 本次结果 |
| --- | --- | --- |
| A：GNU ld | parseAssemblyString→verifyModule→打印 archive_probe_fn，期待单行输出 | **FAIL，尚未生成 A.o/进入 ld** |
| A：lld | 相同逻辑与输出对照 | NOT RUN |
| B：GNU ld / lld | lldCommon+lldELF，调用 lldMain 及 elf::link 的公开接口 | NOT RUN |
| A 共享库 | GNU ld -shared -z text -z defs，PIC 对象 | NOT RUN |
| 未转换归档反例 | 相同 GNU ld 无 LTO/无插件命令，改库路径，应失败 | NOT RUN |

每次 link 前保存 `-###`；A 的预定链接器是 `/usr/bin/ld.bfd`，argv 无 -flto、-plugin 或 --plugin。
**这里只能证明拟执行 argv，不能证明该链接已实际执行或成功。**

### 4.2 llvm-config 的定位处理

通过显式 loader 运行 llvm-config 时，首次查询的 --prefix 错指 `/usr/lib`，导致组件库缺失查询失败。
查询阶段修正为：在 E/consumers/prefix/bin 放宿主 loader 的同字节副本，并将 prefix/include、prefix/lib64 分别指向 H 的头文件与 C 的机器码归档。
该方式不改 llvm-config，不安装到宿主；随后 `--link-static` 取得 cxxflags/ldflags/组件库列表全部成功。
完整输出为 `E/llvm-config-queries.json`、`llvm-config-relocated-queries.json` 及 consumers/query-*.json、*.txt。

系统依赖为 -lrt -ldl -lm -lz -lxml2；libxml2 显式指向 RT/libxml2.so.16，避免误用宿主不同版本。
无 LLVM 共享库被加入消费者链接命令。通用 lld --version 返回“请选择驱动”的状态 1，
查询加 `-flavor gnu --version` 后正常输出 LLD 22.1.8；这是查询语法，不是链接实验重试。

### 4.3 实际错误及原因

A 首次命令把编译与链接放在一个 clang 驱动调用中。退出 1，wall=0.01 s，max RSS=45,908 KiB。
原始 `E/consumers/link-a-bfd.log`：

```text
-cc1: error while loading shared libraries: -cc1: cannot open shared object file
clang-22: error: unable to execute command: No such file or directory
clang-22: error: clang frontend command failed due to signal (use -v to see invocation)
InstalledDir: /usr/lib/x86_64-linux-gnu
```

`E/consumers/a-bfd-driver.txt` 的错误前端 executable：

```text
"/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2" "-cc1" ... "-x" "c++" ".../a.cpp"
```

源码证据：

- `llvm/clang/tools/driver/driver.cpp:63–77`：canonical executable 查询会调用 getMainExecutable。
- `llvm/llvm/lib/Support/Unix/Path.inc:256–279`：Linux 查询 `/proc/self/exe`，显式 loader 下得到 loader 路径。
- `llvm/clang/lib/Driver/Driver.cpp:5355–5359`：多于一个 job 时关闭 integrated cc1。
- `llvm/clang/lib/Driver/Job.cpp:408–414`：非进程内 cc1 回落为子进程执行。

离线 IR→.o 的单个 -c job 没有触发这次“编译＋链接”入口问题；它们均成功退出并通过对象/索引检查。
消费者失败发生在库被链接之前，故**不能归因于 GNU ld 不接受转换归档，也不能声称兼容性已证实**。
责任在本次测试入口未处理 loader 下的 cc1 子进程路径，不是用户方案被本次实验证伪。

严格遵守失败后不重试：未改 flags/换编译器重跑，未继续 B/共享库/反例，未进入第二段。
后续可修正的方向（**未执行**）：先单独 -c 生成对象，再仅用对象调用链接器，分开核对两个 argv；
保持原 API 负载、库集合、无 LTO/无插件条件不变。再次消费者验收通过前不进入 spec。

资源证据：`E/consumer-scope/outcome.json` command_exit_code=1；2.133406 s，MemoryPeak=22,425,600 B，OOM=0。
systemd scope Result=success 仅是 scope 状态；**不覆盖子命令退出 1**，本任务仍判 FAIL。
两 scope 的最终状态和采样器回收见 `E/scope-cleanup.json`、两组 outcome.json。

## 5. ARM/AArch64 只读调查与建议

实际存在：`/home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0` 与 `scratch.aarch64.0`。
只查询这两个根的 RPM 元数据、usr/emul 工具与配置，不构建、不改根。
第一次宿主 rpm 查询误用默认 ~/.rpmdb，记录后改为已枚举到的 `/var/lib/rpm`、bdb_ro 只读后端，查询成功。

| 项目 | ARM 根 | AArch64 根 |
| --- | --- | --- |
| 已安装 clang/llvm | 22.1.8-1.6 armv7l | 22.1.8-19.1 aarch64 |
| 已安装 clang-accel | 0.4-1.1 armv7l | 0.4-1.4 aarch64 |
| llvm-static-devel | 未安装 | 未安装 |
| 根外同 GBS local/cache 的 static-devel RPM | 未找到 | 未找到 |
| static-devel 是否 bitcode | **UNKNOWN：没有可检查的归档** | 同左 |
| emul/usr/bin/clang-22 版本 | 实际 --version=22.1.8；ELF x86_64 | 同左 |
| accel 注册目标 | 实际 --print-targets 含 ARM/AArch64/X86/BPF | 同左 |
| usr/bin/clang.cfg | armv7l-tizen-linux-gnueabi | aarch64-tizen-linux-gnu |
| 对这两个架构的实际待转换 IR 可读性 | **UNKNOWN：没有实际输入** | 同左 |

证据：E/other-arch-discovery.json、other-arch-packages.json、other-arch-runtime-layout.json、
other-arch-accel-versions.json、other-arch-accel-targets.json、other-arch-cached-static-devel.json。
不能因版本号相同，就把“能读未来实际 bitcode”记为已验证。

建议（未实施）：在 x86_64 构建分支使用本次自编 x86_64 clang；ARM/AArch64 若在 x86_64 GBS worker 上构建，
先核查系统 clang→accel 的实际路由与输入 IR 兼容性，再选择经 accel 执行的系统转换器。
不能假设构建树内新的 ARM ELF 路径会自动得到同样的 accel 路由。
工作区 spec:240–253 的 armv7l 为 MinSizeRel，aarch64 为 Release；这两个分支还须提取实际优化 flags、PIC/PIE 与函数属性，
**不要直接照搬本轮 x86_64 的 -O3 命令**。

耗时证据仅覆盖本轮 x86_64：3,853 个成员、并发4，总722.644133 s（约12分钟），转换CPU累加1,358.80 s。
若将来在同类 x86_64 accel 上执行类似规模 IR，这是规划参考点，**不是 ARM/AArch64 已测或保证的耗时**。
两个架构的成员规模、IR复杂度及是否经真实仿真尚未确定，绝对耗时量级为 UNKNOWN；
需对应 static-devel/原 IR 与 executor 的实际路由才能给可靠预算。未为了填数做其他架构编译。

## 6. 第二段、可提交补丁与结论

| 第二段要求 | 状态 |
| --- | --- |
| S/spec 的 %install 转换、新增 Source；原宏不改 | NOT RUN，第一段消费者失败 |
| 最小修法 diff / git apply --check / 补丁 SHA | **没有 spec 修法补丁；路径/ SHA 不适用** |
| archive-fix-trial 精确认证入口与正负测试 | NOT RUN，build_llvm_x86_64.py 与 HEAD 相同 |
| 18 GiB/swap0/4-4-1/debuginfo4 完整构建及 CMake 门禁 | 未启动，**0 次**；不以离线11GiB政策放行完整构建 |
| 22 个新 RPM inventory、解包 toolchain-archivefix | 无新 RPM |
| 新包全机器码/索引/成员次序 | NOT RUN；离线 PASS 不替代最终 brp 后 RPM 验收 |
| compiler-rt 内容/索引对照 | 新包验收 NOT RUN；离线输入未修改、未转换 |
| brp-strip-static-archive 与其他后处理日志 | NOT RUN；没有实际打包日志 |
| 新旧解包逐文件完整差异分类 | NOT RUN |
| 新 RPM 的 A/B/共享库消费者及 GNU ld 兼容性 | NOT RUN |
| 新 clang/lld/llvm-ar SHA 可复现性 | NOT RUN；转换没有生成或替换工具二进制 |

**可否据本轮提交 spec 修法：否。** 当前有可复用、已实际运行的离线转换与检查代码，
但消费者兼容性和完整 RPM 验收都未闭合。归档修复仍第一优先级，设计 v4/BOLT 暂缓；旧改宏方案作废。
转换结果及逐归档 SHA 已保留，后续入口修正后应先核其身份，再决定是否复用，而不是把本次 FAIL 改判为 PASS。

## 7. 自检与证据目录

| 自检 | 结果 |
| --- | --- |
| 22 RPM 与解包元数据复核 | PASS，22/22 与17,689/17,689 |
| 转换失败是否跳过、是否重试 | 否；转换全PASS；消费者第一次失败后停止 |
| 是否不带 LTO 转换、原机器码不变 | 是，实际 argv 与11成员SHA有记录 |
| 完整 PIC/消费者门禁是否通过 | 否；静态重定位扫描通过，共享库/实际链接未验 |
| 是否改原 W/llvm、spec、试验spec、RPM宏 | 否，保护检查见 E/preservation-check.json |
| docs/25、docs/26 是否保持不动 | 是，SHA与任务起点匹配 |
| 是否运行完整构建/BOLT/校准/Chromium/Gerrit | 否 |
| 独占锁、scope、采样器是否回收 | 是，E/lock-released.json、final-cleanup.json、scope-cleanup.json |
| STATUS是否同commit更新方案及失败范围 | 是，本提交可由 git log -1 -- docs/27_static_archive_native_conversion.md 定位 |

原始证据均在 E（绝对前缀见 §0）：

- precheck.json、rpm-identity.json、baseline-content-check.json、baseline-check.log、check_baseline.py。
- converter-identities.json、executed-tools-sha256.json、conversion-tests.log。
- conversion/summary.json、conversion/members/ 下每归档 before/after、每成员 IR/settings/命令/time/relocations；conversion-summary.json。
- scope/launch.json、build.log、samples.jsonl、process-memory.jsonl、time-v.txt、scope-after-rpm.json、outcome.json。
- consumers/ 下源码、查询输出、a-bfd-driver.txt、link-a-bfd.log/json/time、result.json；consumer-scope/ 同类资源记录。
- cpu-attribute-check/results.json、check_empty_modules.py；other-arch-*.json。
- preservation-check.json、lock-acquired.json、lock-released.json、final-cleanup.json、scope-cleanup.json。

完整成员机器码中间文件在归档核对后删除，转换后的 .a 保留；没有把大文件或原始日志提交到 GitHub。

## 附录 A：225 个转换归档的完整结果

本表是离线结果，尚未运行 brp-strip-static-archive；“顺序/索引 PASS”不表示消费者或 RPM 门禁通过。
全部新旧归档 SHA 与逐成员细节在 E/conversion-summary.json 和 before/after.json。

| 归档（H/usr/lib64/） | 成员 | BC→ELF | 原 ELF 保留 | 转换前 B | 转换后 B | 索引条目 | 有调试节成员 | 顺序/索引 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `libLLVMAArch64AsmParser.a` | 1 | 1 | 0 | 4874780 | 6746546 | 62 | 1 | PASS |
| `libLLVMAArch64CodeGen.a` | 63 | 63 | 0 | 93637138 | 120839248 | 4339 | 63 | PASS |
| `libLLVMAArch64Desc.a` | 12 | 12 | 0 | 8790320 | 11877922 | 658 | 12 | PASS |
| `libLLVMAArch64Disassembler.a` | 2 | 2 | 0 | 2002576 | 2799578 | 24 | 2 | PASS |
| `libLLVMAArch64Info.a` | 1 | 1 | 0 | 95582 | 106698 | 10 | 1 | PASS |
| `libLLVMAArch64Utils.a` | 1 | 1 | 0 | 1022860 | 1250832 | 62 | 1 | PASS |
| `libLLVMABI.a` | 1 | 1 | 0 | 27172 | 27106 | 1 | 1 | PASS |
| `libLLVMARMAsmParser.a` | 1 | 1 | 0 | 4114928 | 5197304 | 76 | 1 | PASS |
| `libLLVMARMCodeGen.a` | 49 | 49 | 0 | 59210366 | 74182814 | 3410 | 49 | PASS |
| `libLLVMARMDesc.a` | 13 | 13 | 0 | 5966318 | 7855052 | 434 | 13 | PASS |
| `libLLVMARMDisassembler.a` | 1 | 1 | 0 | 2257304 | 3738232 | 8 | 1 | PASS |
| `libLLVMARMInfo.a` | 1 | 1 | 0 | 93594 | 105178 | 10 | 1 | PASS |
| `libLLVMARMUtils.a` | 1 | 1 | 0 | 139416 | 153320 | 10 | 1 | PASS |
| `libLLVMAggressiveInstCombine.a` | 2 | 2 | 0 | 3290774 | 4125442 | 110 | 2 | PASS |
| `libLLVMAnalysis.a` | 131 | 125 | 6 | 134030922 | 166065124 | 9363 | 124 | PASS |
| `libLLVMAsmParser.a` | 4 | 4 | 0 | 10663380 | 13484390 | 658 | 4 | PASS |
| `libLLVMAsmPrinter.a` | 27 | 27 | 0 | 30774180 | 36857114 | 1956 | 27 | PASS |
| `libLLVMBPFAsmParser.a` | 1 | 1 | 0 | 490640 | 611494 | 28 | 1 | PASS |
| `libLLVMBPFCodeGen.a` | 26 | 26 | 0 | 19082078 | 22523750 | 1688 | 26 | PASS |
| `libLLVMBPFDesc.a` | 5 | 5 | 0 | 839732 | 968040 | 110 | 5 | PASS |
| `libLLVMBPFDisassembler.a` | 1 | 1 | 0 | 291164 | 294212 | 4 | 1 | PASS |
| `libLLVMBPFInfo.a` | 1 | 1 | 0 | 91270 | 99776 | 7 | 1 | PASS |
| `libLLVMBinaryFormat.a` | 14 | 14 | 0 | 2994558 | 3578336 | 247 | 14 | PASS |
| `libLLVMBitReader.a` | 5 | 5 | 0 | 11509418 | 14266316 | 506 | 5 | PASS |
| `libLLVMBitWriter.a` | 4 | 4 | 0 | 8448570 | 12239418 | 243 | 4 | PASS |
| `libLLVMBitstreamReader.a` | 1 | 1 | 0 | 672008 | 864026 | 48 | 1 | PASS |
| `libLLVMCAS.a` | 15 | 15 | 0 | 7837688 | 9271560 | 427 | 15 | PASS |
| `libLLVMCFGuard.a` | 1 | 1 | 0 | 750524 | 882346 | 18 | 1 | PASS |
| `libLLVMCFIVerify.a` | 2 | 2 | 0 | 2147476 | 2526068 | 151 | 2 | PASS |
| `libLLVMCGData.a` | 7 | 7 | 0 | 4890264 | 6011642 | 296 | 7 | PASS |
| `libLLVMCodeGen.a` | 238 | 237 | 1 | 250523280 | 307136582 | 14191 | 237 | PASS |
| `libLLVMCodeGenTypes.a` | 1 | 1 | 0 | 94620 | 117298 | 6 | 1 | PASS |
| `libLLVMCore.a` | 80 | 80 | 0 | 84203524 | 107364516 | 7628 | 80 | PASS |
| `libLLVMCoroutines.a` | 11 | 11 | 0 | 12862536 | 15373664 | 339 | 11 | PASS |
| `libLLVMCoverage.a` | 3 | 3 | 0 | 7331182 | 8958230 | 214 | 3 | PASS |
| `libLLVMDTLTO.a` | 1 | 1 | 0 | 485968 | 544288 | 35 | 1 | PASS |
| `libLLVMDWARFCFIChecker.a` | 4 | 4 | 0 | 1573624 | 1775882 | 122 | 4 | PASS |
| `libLLVMDWARFLinker.a` | 2 | 2 | 0 | 120604 | 126920 | 3 | 2 | PASS |
| `libLLVMDWARFLinkerClassic.a` | 4 | 4 | 0 | 6648528 | 7833816 | 416 | 4 | PASS |
| `libLLVMDWARFLinkerParallel.a` | 11 | 11 | 0 | 15430734 | 18091902 | 819 | 11 | PASS |
| `libLLVMDWP.a` | 2 | 2 | 0 | 1423520 | 1730668 | 68 | 2 | PASS |
| `libLLVMDebugInfoBTF.a` | 2 | 2 | 0 | 1232706 | 1590224 | 65 | 2 | PASS |
| `libLLVMDebugInfoCodeView.a` | 40 | 40 | 0 | 15137966 | 19302658 | 1772 | 40 | PASS |
| `libLLVMDebugInfoDWARF.a` | 29 | 29 | 0 | 24375292 | 28868864 | 1908 | 29 | PASS |
| `libLLVMDebugInfoDWARFLowLevel.a` | 3 | 3 | 0 | 1094162 | 1352980 | 60 | 3 | PASS |
| `libLLVMDebugInfoGSYM.a` | 14 | 14 | 0 | 8206230 | 10458982 | 504 | 14 | PASS |
| `libLLVMDebugInfoLogicalView.a` | 19 | 19 | 0 | 25733758 | 31125182 | 2322 | 19 | PASS |
| `libLLVMDebugInfoMSF.a` | 4 | 4 | 0 | 1725236 | 2196610 | 173 | 4 | PASS |
| `libLLVMDebugInfoPDB.a` | 93 | 93 | 0 | 29948434 | 36164928 | 3174 | 93 | PASS |
| `libLLVMDebuginfod.a` | 4 | 4 | 0 | 2117992 | 2564174 | 197 | 4 | PASS |
| `libLLVMDemangle.a` | 6 | 6 | 0 | 2421668 | 3555530 | 767 | 6 | PASS |
| `libLLVMDiff.a` | 3 | 3 | 0 | 1349944 | 1697496 | 82 | 3 | PASS |
| `libLLVMDlltoolDriver.a` | 1 | 1 | 0 | 675070 | 802180 | 15 | 1 | PASS |
| `libLLVMExecutionEngine.a` | 5 | 5 | 0 | 3144502 | 3881628 | 265 | 5 | PASS |
| `libLLVMExegesis.a` | 25 | 25 | 0 | 15890110 | 18766866 | 822 | 25 | PASS |
| `libLLVMExegesisAArch64.a` | 1 | 1 | 0 | 1076316 | 1350680 | 37 | 1 | PASS |
| `libLLVMExegesisX86.a` | 2 | 2 | 0 | 2441458 | 3173572 | 73 | 2 | PASS |
| `libLLVMExtensions.a` | 1 | 1 | 0 | 27942 | 28098 | 2 | 1 | PASS |
| `libLLVMFileCheck.a` | 1 | 1 | 0 | 2707708 | 3422302 | 239 | 1 | PASS |
| `libLLVMFrontendAtomic.a` | 1 | 1 | 0 | 557552 | 687864 | 22 | 1 | PASS |
| `libLLVMFrontendDirective.a` | 1 | 1 | 0 | 52380 | 58132 | 1 | 1 | PASS |
| `libLLVMFrontendDriver.a` | 1 | 1 | 0 | 101978 | 105498 | 4 | 1 | PASS |
| `libLLVMFrontendHLSL.a` | 6 | 6 | 0 | 2050758 | 2516402 | 129 | 6 | PASS |
| `libLLVMFrontendOffloading.a` | 3 | 3 | 0 | 3435454 | 3920466 | 106 | 3 | PASS |
| `libLLVMFrontendOpenACC.a` | 1 | 1 | 0 | 193824 | 238102 | 11 | 1 | PASS |
| `libLLVMFrontendOpenMP.a` | 4 | 4 | 0 | 10101866 | 13025852 | 571 | 4 | PASS |
| `libLLVMFuzzMutate.a` | 4 | 4 | 0 | 4457938 | 5313542 | 210 | 4 | PASS |
| `libLLVMFuzzerCLI.a` | 1 | 1 | 0 | 368288 | 453082 | 8 | 1 | PASS |
| `libLLVMGlobalISel.a` | 30 | 30 | 0 | 30399224 | 38244618 | 2127 | 30 | PASS |
| `libLLVMHipStdPar.a` | 1 | 1 | 0 | 1078348 | 1290852 | 18 | 1 | PASS |
| `libLLVMIRPrinter.a` | 1 | 1 | 0 | 194296 | 213210 | 12 | 1 | PASS |
| `libLLVMIRReader.a` | 1 | 1 | 0 | 510364 | 621504 | 13 | 1 | PASS |
| `libLLVMInstCombine.a` | 15 | 15 | 0 | 38363862 | 48767114 | 2421 | 15 | PASS |
| `libLLVMInstrumentation.a` | 28 | 28 | 0 | 48745550 | 60148850 | 2005 | 28 | PASS |
| `libLLVMInterfaceStub.a` | 3 | 3 | 0 | 2707424 | 3354526 | 116 | 3 | PASS |
| `libLLVMInterpreter.a` | 3 | 3 | 0 | 2729236 | 3975152 | 166 | 3 | PASS |
| `libLLVMJITLink.a` | 35 | 35 | 0 | 43854792 | 52126098 | 2507 | 35 | PASS |
| `libLLVMLTO.a` | 6 | 6 | 0 | 19886408 | 22422100 | 893 | 6 | PASS |
| `libLLVMLibDriver.a` | 1 | 1 | 0 | 969160 | 1175454 | 25 | 1 | PASS |
| `libLLVMLineEditor.a` | 1 | 1 | 0 | 262042 | 305598 | 26 | 1 | PASS |
| `libLLVMLinker.a` | 2 | 2 | 0 | 3566984 | 4102184 | 109 | 2 | PASS |
| `libLLVMMC.a` | 70 | 70 | 0 | 26865518 | 32324096 | 2012 | 70 | PASS |
| `libLLVMMCA.a` | 24 | 24 | 0 | 5719358 | 6718546 | 516 | 24 | PASS |
| `libLLVMMCDisassembler.a` | 5 | 5 | 0 | 755262 | 850968 | 59 | 5 | PASS |
| `libLLVMMCJIT.a` | 1 | 1 | 0 | 1133612 | 1352396 | 83 | 1 | PASS |
| `libLLVMMCParser.a` | 13 | 13 | 0 | 8974300 | 11805514 | 305 | 13 | PASS |
| `libLLVMMIRParser.a` | 3 | 3 | 0 | 6391244 | 8217414 | 315 | 3 | PASS |
| `libLLVMObjCARCOpts.a` | 8 | 8 | 0 | 5573878 | 6551370 | 144 | 8 | PASS |
| `libLLVMObjCopy.a` | 26 | 26 | 0 | 18755368 | 22303578 | 1124 | 26 | PASS |
| `libLLVMObject.a` | 36 | 36 | 0 | 36229380 | 42459714 | 2665 | 36 | PASS |
| `libLLVMObjectYAML.a` | 29 | 29 | 0 | 44639128 | 58573832 | 3619 | 29 | PASS |
| `libLLVMOptDriver.a` | 2 | 2 | 0 | 6892208 | 8029412 | 572 | 2 | PASS |
| `libLLVMOption.a` | 4 | 4 | 0 | 1766016 | 2308470 | 128 | 4 | PASS |
| `libLLVMOrcDebugging.a` | 7 | 7 | 0 | 7483054 | 8565922 | 410 | 7 | PASS |
| `libLLVMOrcJIT.a` | 57 | 57 | 0 | 86983258 | 101578816 | 5160 | 57 | PASS |
| `libLLVMOrcShared.a` | 7 | 7 | 0 | 1100678 | 1271264 | 160 | 7 | PASS |
| `libLLVMOrcTargetProcess.a` | 15 | 15 | 0 | 9955228 | 11881370 | 551 | 15 | PASS |
| `libLLVMPasses.a` | 6 | 6 | 0 | 45016450 | 55792266 | 9766 | 6 | PASS |
| `libLLVMPlugins.a` | 1 | 1 | 0 | 146814 | 160022 | 2 | 1 | PASS |
| `libLLVMProfileData.a` | 21 | 21 | 0 | 33022822 | 44324150 | 2560 | 21 | PASS |
| `libLLVMRemarks.a` | 11 | 11 | 0 | 5117214 | 6173158 | 419 | 11 | PASS |
| `libLLVMRuntimeDyld.a` | 8 | 8 | 0 | 9462968 | 11167478 | 921 | 8 | PASS |
| `libLLVMSandboxIR.a` | 15 | 15 | 0 | 9963148 | 11540908 | 1674 | 15 | PASS |
| `libLLVMScalarOpts.a` | 81 | 81 | 0 | 125040642 | 151965980 | 4116 | 81 | PASS |
| `libLLVMSelectionDAG.a` | 26 | 26 | 0 | 55822938 | 77324016 | 3756 | 26 | PASS |
| `libLLVMSupport.a` | 179 | 175 | 4 | 44309346 | 56358002 | 4993 | 172 | PASS |
| `libLLVMSupportLSP.a` | 3 | 3 | 0 | 2793464 | 3687430 | 251 | 3 | PASS |
| `libLLVMSymbolize.a` | 5 | 5 | 0 | 4829590 | 6013796 | 332 | 5 | PASS |
| `libLLVMTableGen.a` | 14 | 14 | 0 | 11789056 | 14979374 | 1073 | 14 | PASS |
| `libLLVMTableGenBasic.a` | 13 | 13 | 0 | 9411646 | 12104264 | 361 | 13 | PASS |
| `libLLVMTableGenCommon.a` | 23 | 23 | 0 | 28135432 | 36069072 | 1686 | 23 | PASS |
| `libLLVMTarget.a` | 5 | 5 | 0 | 1580756 | 1786818 | 189 | 5 | PASS |
| `libLLVMTargetParser.a` | 15 | 15 | 0 | 5674402 | 7669946 | 364 | 15 | PASS |
| `libLLVMTelemetry.a` | 1 | 1 | 0 | 235708 | 291910 | 17 | 1 | PASS |
| `libLLVMTextAPI.a` | 15 | 15 | 0 | 10020890 | 12869794 | 509 | 15 | PASS |
| `libLLVMTextAPIBinaryReader.a` | 1 | 1 | 0 | 1414020 | 1715230 | 52 | 1 | PASS |
| `libLLVMTransformUtils.a` | 94 | 94 | 0 | 96853102 | 116976114 | 3562 | 94 | PASS |
| `libLLVMVectorize.a` | 33 | 33 | 0 | 86713910 | 109270266 | 4812 | 33 | PASS |
| `libLLVMWindowsDriver.a` | 1 | 1 | 0 | 321640 | 443006 | 14 | 1 | PASS |
| `libLLVMWindowsManifest.a` | 1 | 1 | 0 | 402650 | 454396 | 27 | 1 | PASS |
| `libLLVMX86AsmParser.a` | 1 | 1 | 0 | 3512772 | 4391370 | 80 | 1 | PASS |
| `libLLVMX86CodeGen.a` | 66 | 66 | 0 | 115303032 | 154205120 | 4564 | 66 | PASS |
| `libLLVMX86Desc.a` | 16 | 16 | 0 | 11916092 | 16818334 | 2278 | 16 | PASS |
| `libLLVMX86Disassembler.a` | 1 | 1 | 0 | 1553368 | 4340348 | 4 | 1 | PASS |
| `libLLVMX86Info.a` | 1 | 1 | 0 | 89482 | 97332 | 6 | 1 | PASS |
| `libLLVMX86TargetMCA.a` | 1 | 1 | 0 | 137814 | 160890 | 14 | 1 | PASS |
| `libLLVMXRay.a` | 14 | 14 | 0 | 5172708 | 6154126 | 438 | 14 | PASS |
| `libLLVMipo.a` | 45 | 45 | 0 | 115556998 | 142761252 | 5246 | 45 | PASS |
| `libarcher_static.a` | 1 | 1 | 0 | 709448 | 888830 | 9 | 1 | PASS |
| `libclangAPINotes.a` | 5 | 5 | 0 | 9659868 | 13177722 | 440 | 5 | PASS |
| `libclangAST.a` | 114 | 114 | 0 | 230364922 | 304171844 | 26686 | 114 | PASS |
| `libclangASTMatchers.a` | 3 | 3 | 0 | 17098112 | 19386326 | 494 | 3 | PASS |
| `libclangAnalysis.a` | 31 | 31 | 0 | 48744872 | 53731104 | 2344 | 31 | PASS |
| `libclangAnalysisFlowSensitive.a` | 18 | 18 | 0 | 21959454 | 22680174 | 885 | 18 | PASS |
| `libclangAnalysisFlowSensitiveModels.a` | 3 | 3 | 0 | 13934446 | 16468636 | 1246 | 3 | PASS |
| `libclangAnalysisLifetimeSafety.a` | 10 | 10 | 0 | 11088326 | 13009828 | 307 | 10 | PASS |
| `libclangAnalysisScalable.a` | 4 | 4 | 0 | 874110 | 1070700 | 40 | 4 | PASS |
| `libclangApplyReplacements.a` | 1 | 1 | 0 | 1716482 | 2248968 | 117 | 1 | PASS |
| `libclangBasic.a` | 73 | 73 | 0 | 48594198 | 52856698 | 6167 | 73 | PASS |
| `libclangChangeNamespace.a` | 1 | 1 | 0 | 6155072 | 7366754 | 605 | 1 | PASS |
| `libclangCodeGen.a` | 101 | 101 | 0 | 219606070 | 255840746 | 7734 | 101 | PASS |
| `libclangCrossTU.a` | 1 | 1 | 0 | 1852100 | 2093810 | 106 | 1 | PASS |
| `libclangDaemon.a` | 82 | 82 | 0 | 177215514 | 208673100 | 7271 | 82 | PASS |
| `libclangDaemonTweaks.a` | 20 | 20 | 0 | 39566066 | 44938864 | 512 | 20 | PASS |
| `libclangDependencyScanning.a` | 7 | 7 | 0 | 7917672 | 9744968 | 446 | 7 | PASS |
| `libclangDirectoryWatcher.a` | 2 | 2 | 0 | 716314 | 843604 | 32 | 2 | PASS |
| `libclangDoc.a` | 11 | 11 | 0 | 24918148 | 33505172 | 1972 | 11 | PASS |
| `libclangDocSupport.a` | 2 | 2 | 0 | 379852 | 464626 | 10 | 2 | PASS |
| `libclangDriver.a` | 76 | 76 | 0 | 76126900 | 102081562 | 5935 | 76 | PASS |
| `libclangDynamicASTMatchers.a` | 5 | 5 | 0 | 51442378 | 66236372 | 6495 | 5 | PASS |
| `libclangEdit.a` | 3 | 3 | 0 | 1616232 | 1947948 | 75 | 3 | PASS |
| `libclangExtractAPI.a` | 6 | 6 | 0 | 16909170 | 22844064 | 1241 | 6 | PASS |
| `libclangFormat.a` | 23 | 23 | 0 | 19479866 | 25440968 | 1168 | 23 | PASS |
| `libclangFrontend.a` | 32 | 32 | 0 | 56621002 | 74311274 | 2631 | 32 | PASS |
| `libclangFrontendTool.a` | 1 | 1 | 0 | 1099362 | 1183800 | 14 | 1 | PASS |
| `libclangHandleCXX.a` | 1 | 1 | 0 | 514850 | 611156 | 36 | 1 | PASS |
| `libclangHandleLLVM.a` | 1 | 1 | 0 | 1510004 | 1643302 | 27 | 1 | PASS |
| `libclangIncludeCleaner.a` | 8 | 8 | 0 | 10889168 | 12833314 | 282 | 8 | PASS |
| `libclangIncludeFixer.a` | 6 | 6 | 0 | 3831196 | 4568400 | 164 | 6 | PASS |
| `libclangIncludeFixerPlugin.a` | 1 | 1 | 0 | 891206 | 956564 | 128 | 1 | PASS |
| `libclangIndex.a` | 9 | 9 | 0 | 15628096 | 18154706 | 265 | 9 | PASS |
| `libclangIndexSerialization.a` | 1 | 1 | 0 | 341666 | 405262 | 15 | 1 | PASS |
| `libclangInstallAPI.a` | 8 | 8 | 0 | 9276748 | 11159910 | 710 | 8 | PASS |
| `libclangInterpreter.a` | 10 | 10 | 0 | 11054336 | 11950810 | 478 | 10 | PASS |
| `libclangLex.a` | 25 | 25 | 0 | 24823768 | 30833686 | 1497 | 25 | PASS |
| `libclangMove.a` | 2 | 2 | 0 | 6544622 | 7651364 | 380 | 2 | PASS |
| `libclangOptions.a` | 2 | 2 | 0 | 1158292 | 1429702 | 24 | 2 | PASS |
| `libclangParse.a` | 18 | 18 | 0 | 32397796 | 38820346 | 1358 | 18 | PASS |
| `libclangQuery.a` | 2 | 2 | 0 | 6203984 | 6740656 | 325 | 2 | PASS |
| `libclangReorderFields.a` | 2 | 2 | 0 | 3663994 | 4426880 | 155 | 2 | PASS |
| `libclangRewrite.a` | 3 | 3 | 0 | 1512124 | 1785134 | 79 | 3 | PASS |
| `libclangRewriteFrontend.a` | 8 | 8 | 0 | 3424270 | 3751514 | 241 | 8 | PASS |
| `libclangSema.a` | 86 | 86 | 0 | 347385702 | 394836062 | 10187 | 86 | PASS |
| `libclangSerialization.a` | 17 | 17 | 0 | 57396436 | 72550674 | 3164 | 17 | PASS |
| `libclangStaticAnalyzerCheckers.a` | 134 | 134 | 0 | 184402564 | 201891082 | 6526 | 134 | PASS |
| `libclangStaticAnalyzerCore.a` | 49 | 49 | 0 | 63939322 | 76256906 | 3639 | 49 | PASS |
| `libclangStaticAnalyzerFrontend.a` | 7 | 7 | 0 | 7620978 | 7463084 | 225 | 7 | PASS |
| `libclangSupport.a` | 1 | 1 | 0 | 750028 | 966592 | 47 | 1 | PASS |
| `libclangTidy.a` | 9 | 9 | 0 | 14027276 | 16866676 | 650 | 9 | PASS |
| `libclangTidyAbseilModule.a` | 22 | 22 | 0 | 49671914 | 54884238 | 2993 | 22 | PASS |
| `libclangTidyAlteraModule.a` | 6 | 6 | 0 | 11507890 | 12553168 | 485 | 6 | PASS |
| `libclangTidyAndroidModule.a` | 17 | 17 | 0 | 27905792 | 29942360 | 1148 | 17 | PASS |
| `libclangTidyBoostModule.a` | 3 | 3 | 0 | 5481838 | 5971168 | 171 | 3 | PASS |
| `libclangTidyBugproneModule.a` | 105 | 105 | 0 | 261792300 | 291003090 | 15809 | 105 | PASS |
| `libclangTidyCERTModule.a` | 1 | 1 | 0 | 2618622 | 2830194 | 135 | 1 | PASS |
| `libclangTidyConcurrencyModule.a` | 3 | 3 | 0 | 4800888 | 5137614 | 113 | 3 | PASS |
| `libclangTidyCppCoreGuidelinesModule.a` | 32 | 32 | 0 | 68425502 | 75386646 | 3977 | 32 | PASS |
| `libclangTidyCustomModule.a` | 2 | 2 | 0 | 3385102 | 3704240 | 43 | 2 | PASS |
| `libclangTidyDarwinModule.a` | 3 | 3 | 0 | 4586320 | 4913574 | 110 | 3 | PASS |
| `libclangTidyFuchsiaModule.a` | 8 | 8 | 0 | 12816724 | 13658092 | 355 | 8 | PASS |
| `libclangTidyGoogleModule.a` | 16 | 16 | 0 | 29916542 | 32491032 | 1304 | 16 | PASS |
| `libclangTidyHICPPModule.a` | 6 | 6 | 0 | 11395730 | 12364250 | 522 | 6 | PASS |
| `libclangTidyLLVMLibcModule.a` | 5 | 5 | 0 | 8165866 | 8622256 | 205 | 5 | PASS |
| `libclangTidyLLVMModule.a` | 9 | 9 | 0 | 18048700 | 19615784 | 795 | 9 | PASS |
| `libclangTidyLinuxKernelModule.a` | 2 | 2 | 0 | 3172032 | 3406948 | 72 | 2 | PASS |
| `libclangTidyMPIModule.a` | 3 | 3 | 0 | 4970726 | 5358194 | 64 | 3 | PASS |
| `libclangTidyMain.a` | 1 | 1 | 0 | 1384694 | 1810004 | 109 | 1 | PASS |
| `libclangTidyMiscModule.a` | 28 | 28 | 0 | 66384070 | 73311544 | 3325 | 28 | PASS |
| `libclangTidyModernizeModule.a` | 50 | 50 | 0 | 157657284 | 181705204 | 10328 | 50 | PASS |
| `libclangTidyObjCModule.a` | 10 | 10 | 0 | 16878450 | 18248112 | 606 | 10 | PASS |
| `libclangTidyOpenMPModule.a` | 3 | 3 | 0 | 4897156 | 5257830 | 120 | 3 | PASS |
| `libclangTidyPerformanceModule.a` | 21 | 21 | 0 | 47561864 | 52505408 | 3052 | 21 | PASS |
| `libclangTidyPlugin.a` | 1 | 1 | 0 | 860756 | 985822 | 31 | 1 | PASS |
| `libclangTidyPortabilityModule.a` | 6 | 6 | 0 | 10491864 | 11256780 | 410 | 6 | PASS |
| `libclangTidyReadabilityModule.a` | 59 | 59 | 0 | 153356446 | 169188424 | 7593 | 59 | PASS |
| `libclangTidyUtils.a` | 23 | 23 | 0 | 35972392 | 39693176 | 1224 | 23 | PASS |
| `libclangTidyZirconModule.a` | 1 | 1 | 0 | 1421768 | 1500986 | 7 | 1 | PASS |
| `libclangTooling.a` | 17 | 17 | 0 | 12731232 | 15373260 | 731 | 17 | PASS |
| `libclangToolingASTDiff.a` | 1 | 1 | 0 | 6122252 | 6764430 | 84 | 1 | PASS |
| `libclangToolingCore.a` | 2 | 2 | 0 | 1585990 | 1984182 | 103 | 2 | PASS |
| `libclangToolingInclusions.a` | 3 | 3 | 0 | 1411784 | 1641528 | 55 | 3 | PASS |
| `libclangToolingInclusionsStdlib.a` | 1 | 1 | 0 | 1169404 | 1606092 | 30 | 1 | PASS |
| `libclangToolingRefactoring.a` | 12 | 12 | 0 | 32120646 | 38313944 | 383 | 12 | PASS |
| `libclangToolingSyntax.a` | 8 | 8 | 0 | 10389626 | 13099836 | 304 | 8 | PASS |
| `libclangTransformer.a` | 7 | 7 | 0 | 12336640 | 13621244 | 266 | 7 | PASS |
| `libclangdMain.a` | 2 | 2 | 0 | 6948846 | 8256580 | 676 | 2 | PASS |
| `libclangdRemoteIndex.a` | 1 | 1 | 0 | 100048 | 103902 | 2 | 1 | PASS |
| `libclangdSupport.a` | 16 | 16 | 0 | 4838814 | 5782274 | 405 | 16 | PASS |
| `libfindAllSymbols.a` | 8 | 8 | 0 | 8067408 | 8903028 | 493 | 8 | PASS |
| `liblldCOFF.a` | 18 | 18 | 0 | 26049746 | 33800804 | 1792 | 18 | PASS |
| `liblldCommon.a` | 13 | 13 | 0 | 4521058 | 5845100 | 341 | 13 | PASS |
| `liblldELF.a` | 41 | 41 | 0 | 70073250 | 89616434 | 4021 | 41 | PASS |
| `liblldMachO.a` | 30 | 30 | 0 | 29987584 | 37537950 | 2217 | 30 | PASS |
| `liblldMinGW.a` | 1 | 1 | 0 | 789500 | 1045104 | 13 | 1 | PASS |
| `liblldWasm.a` | 14 | 14 | 0 | 13501042 | 16591592 | 1246 | 14 | PASS |
