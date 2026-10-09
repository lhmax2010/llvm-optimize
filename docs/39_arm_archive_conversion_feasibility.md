# 39 armv7l / aarch64 静态库转换可行性调查

日期：2026-10-09。本轮只调查并做小文件实验，没有构建 LLVM、运行归档全量转换、修改 spec/Source/补丁或推送 Gerrit。
docs/25–38 保留原文。用户确认 356627（转换）与 356639（llvm-strip）已上传；ARM 若通过后续认证，分别更新这两个 change 的 patchset，不另开 review。

**结论：实现具有条件可行性，但现有 x86_64 Source 不能直接用于 ARM。** 两个现有根的 x86_64 accel clang/llvm-dis/llvm-nm/llvm-ar/llvm-strip 均为 22.1.8；小文件跨目标编译、ThinLTO bitcode 读取及机器码输出成功。
cb679968 的 ARM32 是 **MinSizeRel / 末项 -Os**，AArch64 是 **Release / 预计末项 -O3**；两者保留 `-fstack-protector`，并非 x86_64 flags 的复制。
ARM32 的实际 IR triple 是 `thumbv7-tizen-linux-gnueabi`，不能只认证 driver 的 `armv7l-…` 拼写。
仍需真实 ARM 归档的全命令普查、PIC/ABI 与消费者认证，才能交付 ARM patchset。当前本机完整构建不准入：磁盘仅 40.93 GiB；ARM 自动 binfmt 路由尚未恢复，完整构建资源需求也未认证。

## 0. 对象、方法与证据边界

| 别名 | 实际路径 / 身份 |
| --- | --- |
| W | `/home/linhao/Toolchain/development/llvm-optimize` |
| E | `W/temp/arm-archive-feasibility-20261009`，本轮命令与原始输出，仅在本机 |
| RA | `/home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0` |
| R64 | `/home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.aarch64.0` |
| RX | `W/temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0`，仅查询已装宏/CMake，不执行构建 |
| T | `cb67996861d070d68fec2b4c623eed7d20ba2e23:packaging/llvm.spec`；只从 Git blob 导出到 `E/target.spec` |
| L | `W/llvm`；下文 Clang/LLVM/lld 源码路径相对 L |
| E35 | `W/temp/archive-fix-v2-final-20261009/continue-20261009` |

开场主仓库 `08e08899d66d4e73d3ddefd4c48a4466dbdcf381`、status 为空。
W/llvm 仍为 f111162e 的工作区；对 f111162e 与 cb679968 的 `clang/ llvm/ lld/` 做 Git diff 为空，故下文这些源码行可用于目标配方分析。
证据：E/`head.stdout`、`status.stdout`、`local-source-identity.stdout`、`source-sha.json`。
没有读取隔离的旧混合构建根。W 原 spec、转换 Source、patches/ 和历史报告的收尾 SHA 检查见 E/`protected-final.json`。

**查询入口的实际偏差：** 两次 `gbs chroot` 未到达查询哨兵，内部 ARM `su` 报 `Exec format error`，GBS 外层却返回 0。
随后检查宿主实现，发现 `/usr/lib/python3/dist-packages/gitbuildsys/cmd_chroot.py:60–62` 在进入前会复制宿主 `resolv.conf` 到根内；本次调用也走过该包装器。
因此不能声称两个历史根的所有文件均零写入。未保存这两个 resolver 文件的查询前摘要，没有猜测性恢复；spec、源码、宏和工具没有主动改写。
后续全部改用显式 QEMU/loader 或只执行查询的 `sudo -n chroot`，不再调用 GBS 包装器，不修改 binfmt/sysctl。
证据：E/`*-gbs-query.{stdout,stderr}`、`host-gbs-chroot-source.stdout`、`root-query-wrapper-caveat.json`、`*-root-resolv-metadata.stdout`。

## 1. ThinLTO、宏展开与编译参数

### 1.1 展开的对象及限制

在每个 ARM 根内选取**该架构的 `/usr/bin/rpmspec`**，通过该根的静态 QEMU 和显式原生 loader 运行；没有用宿主 rpm 代替其解析器。
根外执行需要把 RPM_CONFIGDIR、rpmrc、宏搜索路径重定位到对应根，显式加载该根 `home/abuild/.rpmrc` 与 `.rpmmacros`，不读取宿主用户宏。
R64 的 `/lib/ld-linux-aarch64.so.1` 是指向 `/lib64/…` 的绝对软链接，直接 `qemu -L` 首次查询打不开它；使用根内实际 loader 后查询成功，没有改软链接。

共同定义与 docs/35 相同，只有目标架构不同：

```text
--define '_smp_mflags -j4'
--define '_srcdefattr (-,root,root)'
--nosignature --target=armv7l    # 另一份为 aarch64
--define '_build_create_debug 1'
--define '_topdir /home/abuild/rpmbuild'
```

`rpmspec --parse` 输出完整 spec，取 `%build`；只执行变量赋值与用 `printf` 替代的 CMake 参数输出，**没有运行 CMake**。
方法、完整 argv、原始展开：E/`expand.py`、`commands.jsonl`、`{armv7l,aarch64}-{parsed,exact-showrc,cmake-argv}.stdout`、`*-cmake.json`、`*-macro-files.json`。
x86_64 对照使用 docs/37 同一 T 的已验证展开：`temp/target-recipe-policy-check-20261009/target-cmake.json`；三者汇总 E/`cmake-comparison.json`。

这是 **T + 当前各根 buildconfig/宏** 的展开，不冒称未来 OBS 项目的宏已钉定。
两根 `.rpmmacros:54–56,65,70–72` 选择 clang 与 `%optflags`；`.rpmrc:1,3,5` 分别提供 AArch64、ARM32、x86_64 的架构项。
两根 `_toolchain=clang`，T:11–16 因而选非 release_build 分支，T:245–252 的 ThinLTO 生效。

### 1.2 三架构对照

| 项 | x86_64 | armv7l | aarch64 | 依据 |
| --- | --- | --- | --- | --- |
| CMAKE_C_COMPILER | clang | armv7l-tizen-linux-gnueabi-clang | aarch64-tizen-linux-gnu-clang | T:232–238；各 cmake.json |
| CMAKE_CXX_COMPILER | clang++ | armv7l-tizen-linux-gnueabi-clang++ | aarch64-tizen-linux-gnu-clang++ | 同上 |
| CMAKE_BUILD_TYPE | Release | MinSizeRel | Release | T:255–268 |
| LLVM_ENABLE_LTO / LLVM_USE_LINKER | Thin / lld | Thin / lld | Thin / lld | T:245–252 |
| CMAKE_C/CXX/ASM_FLAGS | 附录 A 的 X | 附录 A 的 A32，等于本根 optflags | 附录 A 的 A64，等于本根 optflags | T:242–244；原始展开 |
| 公共 flags 强制改写 | 去原优化/stack protector/frame-pointer，再加 O3、ThinLTO、omit-frame-pointer | **不执行** x86_64 条件块 | **不执行** x86_64 条件块 | T:196–219 |
| CMake 配置后追加的优化级 | -O3 -DNDEBUG | -Os -DNDEBUG | -O3 -DNDEBUG（覆盖公共 -Os） | RX `usr/share/cmake/Modules/Compiler/GNU.cmake:58–63`、同目录 `Clang.cmake:27–28`；E/cmake-{gnu,clang}-defaults.stdout |
| 实际转换应认证的末项优化级 | 已认证 -O3 | 候选 -Os | 候选 -O3 | 前两行；真实 ARM 全量命令尚待采集 |
| LLVM_LINK_LLVM_DYLIB / CLANG_LINK_CLANG_DYLIB | OFF / OFF | ON / ON | ON / ON | T:276–284 |
| LLVM_TARGETS_TO_BUILD | X86;ARM;AArch64;BPF | ARM;BPF | AArch64;BPF | T:255–268 |
| LLVM_TARGET_ARCH | 未显式设置 | ARM | AArch64 | 同上 |
| LLVM_PARALLEL_COMPILE_JOBS / LINK_JOBS | 6 / 2 | 6 / 2 | 6 / 2 | T:299–300；不是本轮容量放行 |
| MLGO 编译并发 | 6 | 6 | 6 | T:48；根 .rpmmacros；完整展开 |

**末项优化级的证据强度是配置推导。** 两个现有 ARM 根未安装 cmake/ninja，也不是 LLVM 的完整构建根；这里引用已验证 RX 的 cmake 3.31.2-1.2 默认值，不声称读到了未来 ARM CMakeCache。
未来若 CMake 版本/默认 flags 改变，必须以真实记录命令重新认证。原始包清单为 E/`*-packages.stdout`；x86 CMake NEVRA 为 `x86-cmake-qf.stdout`。

LLVM 自身追加项不能遗漏：`llvm/cmake/modules/HandleLLVMOptions.cmake:433–459` 的 PIC/semantic-interposition，`:1147–1157` 的 function/data sections，`:1303–1313` 的 `-flto=thin`；`llvm/CMakeLists.txt:670` 默认 PIC=ON。
`LLVM_ENABLE_LTO` 向 C/CXX 追加 ThinLTO，不等于 CMAKE_ASM_FLAGS 也追加；原生汇编成员仍须原字节保留。
警告、可用性探针、目标局部 define/include/异常选项等，以 docs/28 §1.1 的方法对**新的 ARM 记录命令全集**普查；当前没有 ARM build.ninja，不能列造一份“已实测完整对象命令”。

### 1.3 ARM 专有项及补回策略草案

下列“写入 IR”不表示可忽略跨目标 driver/ABI 一致性；转换仍必须核对 triple、ELF Machine、端序和 ABI。
所有行均为设计分类，本轮未加入 Source 白名单。

| 参数 | 分类与转换要求 | 源码 / 本轮证据 |
| --- | --- | --- |
| ARM `-march=armv7-a` | 写入 IR：规范化 triple、target-cpu/features；认证该精确值 | `clang/lib/Driver/ToolChains/Arch/ARM.cpp:275–353,540–573`；`CodeGenModule.cpp:2929–2992`；E/armv7l.ll |
| `-mthumb` | 写入 IR：**thumbv7** triple、+thumb-mode；转换须保持 Thumb，不硬改回 armv7l triple | 同上 ARM.cpp:298–353；E/armv7l.ll:4 和函数属性 |
| `-marm` / `-mcpu=` | 本次原 flags **未出现**，不顺手放入认证；今后出现须重认证。ARM 模式会改变 triple/features | ARM.cpp:298–353,656–658 |
| `-mfpu=neon` | 写入 IR 的 FPU/features；候选按精确值认证并与 attrs 对照 | ARM.cpp:664–679；E/armv7l.ll 的 +neon/+vfp… |
| `-mfloat-abi=softfp` | 同时涉及 IR 调用约定与后端 FloatABI，**不能当纯前端项丢弃**；候选显式重放 softfp，核对 EABI/属性 | `clang/lib/Driver/ToolChains/Clang.cpp:1475–1491`；`CodeGen/BackendUtil.cpp:383–391`；ARM driver plan 的 aapcs-linux、cc1 `-mfloat-abi soft` |
| `-mlittle-endian` | 端序进入 IR triple/datalayout；driver还有独立处理，候选显式重放并核验 little endian，不当诊断项丢弃 | ARM.cpp:34–45,275–282；E/armv7l.ll / readelf |
| ARM `-mtune=cortex-a8` | 本版本与机器码无关：源码明确暂不实现、只抑制未使用警告；不得声称写入 tune-cpu | ARM.cpp:660–662；小样本 IR 无 tune-cpu |
| `-Wp,-D__SOFTFP__`、`-D_FILE_OFFSET_BITS=64` | 与 IR→机器码阶段无关：预处理已经完成；保留在原命令审计，不重复预处理 | `clang/lib/Frontend/CompilerInvocation.cpp:3438–3462,4816–4865`；E/armv7l-driver-plan.stderr |
| AArch64 `-march=armv8-a+fp+simd+crc+crypto` | 写入 IR：+v8a/+fp-armv8/+neon/+crc/+crypto… | `Arch/AArch64.cpp:200–266`；E/aarch64.ll |
| AArch64 `-mtune=cortex-a53` | 写入 IR 的 `tune-cpu=cortex-a53`，与 ARM32 的忽略行为不同 | AArch64.cpp:233–238；CodeGenModule.cpp:2983–2984；E/aarch64.ll |
| ARM 两架构 `-fstack-protector` | 写入 IR：ssp 属性、buffer-size 等；x86 spec 会删它，ARM 保留。应显式分类、核验 IR | CodeGenModule.cpp:2729–2740；两个 .ll 的 ssp/buffer-size |
| `-Os` / `-O3` | IR 已优化；转换后端仍取原命令末项，ARM32 候选 -Os / AArch64 -O3；不传 -flto | docs/28 §1.1；BackendUtil.cpp:618–631,1131–1140；§1.2 |

其余共同项沿用 docs/28 §1.1 的分类依据：visibility/exceptions/unwind/frame-pointer、PIC、调试元数据写入 IR；`-W*`、`-D*`/include、pipe、依赖输出属于前端/driver。
后端仍补回 function/data sections、unique-section-names、addrsig、末项 DWARF4 和 fp-contract；依据 BackendUtil.cpp:393–405,453–466 与 docs/28 §1.1，不能只传优化级。
ARM 的 EHABI/unwind、float ABI、`.ARM.attributes` 还要加入未来对照，不以相同 triple 替代 ABI 验收。

本轮纯文本调用现有 `classify_options`，不转换文件、不改函数：`-mtune`、`-mlittle-endian`、`-mfpu`、`-mfloat-abi`、`-mthumb`、`-fstack-protector` 均被拒绝；末项 -Os 也拒绝。
`-march=…` 能归类，但不意味着架构已认证：Source 的 arch/triple/ELF 门禁仍只接受 x86_64。
证据：E/`current-policy-token-probes.json`；`tools/llvm_static_archives_source.py:173–175,189–267,310–327,331–363`。

## 2. 转换器、实际路由与小文件实验

### 2.1 两套工具，而非一份混合身份

RA 的 `/emul/usr/bin` 有 214 个可读条目，R64 有 210 个（含软链接，不等同实体工具数量）。完整路径、链接目标、字节数和 SHA 为 E/`*-tools.json`。

| 根内路径 | RA 字节 | R64 字节 | 身份 / 查询 |
| --- | ---: | ---: | --- |
| /emul/usr/bin/clang-22 | 131592 | 131592 | x86_64 ELF，22.1.8 |
| /emul/usr/bin/llvm-dis | 43480 | 43480 | 22.1.8 |
| /emul/usr/bin/llvm-nm | 147800 | 147800 | 22.1.8 |
| /emul/usr/bin/llvm-ar | 81232 | 81232 | 22.1.8 |
| /emul/usr/bin/ar | 64248 | 64248 | 存在；设计选择 llvm-ar，不假设 GNU ar 能读 bitcode |
| /emul/usr/bin/llvm-strip | 208352 | 208352 | 22.1.8；来自 clang-accel 包 |
| /usr/bin/clang-22 | 75956 | 120136 | 分别 ARM ELF32 / AArch64 ELF64，均 22.1.8 |
| /usr/bin/llvm-strip | → llvm-objcopy | → llvm-objcopy | 分别 ARM / AArch64 ELF，来自 llvm 包 |

accel clang SHA：

```text
RA   44552dc6d42c7602056d50360205d62fdf6ebd9c6760ac90bf91f7b3f31b9c65
R64  49703995e9314b2944cce04d7399d7e4589279c34df30aee1f87cd999b5bc74a
```

同版本、同体积不等于同 SHA。两个 accel `--print-targets` 都有 ARM、AArch64、X86、BPF；实际枚举见 E/`*-accel-targets.stdout`。
根内包清单：RA clang/llvm `22.1.8-1.6.armv7l`、clang-accel `0.4-1.1.armv7l`；R64 clang/llvm `22.1.8-19.1.aarch64`、clang-accel `0.4-1.4.aarch64`。
工具头/依赖、版本及归属见 `*-elf.stdout`、`*-accel-*-version.stdout`、`*-dispatcher-rpm-package-query.stdout`，不是根据包名猜 ELF 架构。

### 2.2 自动分派和显式分派的区别

当前 `/proc/sys/fs/binfmt_misc` 只有 jar/python 注册，没有 ARM/AArch64；`gbs chroot` 因 su 的 Exec format error 失败，不能宣称当前普通 shell 已自动加速。
已有 `/usr/bin/qemu-{arm,aarch64}` 是宿主 x86_64 静态程序；`qemu-*-binfmt` 的 dispatcher 也存在。
本轮**不注册 binfmt、不安装工具**，直接在 chroot 调用 dispatcher 的保留 argv[0] 协议：

```sh
sudo -n chroot "$R" /usr/bin/qemu-binfmt \
  /usr/bin/clang /usr/bin/clang --version
```

两个根均成功。`/usr/bin/<triple>-clang` 别名也成功；输出分别含目标 triple 与 `Configuration file: /usr/bin/clang.cfg`。
额外用根内 QEMU 执行 env，设置 `LD_DEBUG=files` 后调用同一 dispatcher；原始输出明确加载 `/emul/usr/lib64/ld-linux-x86-64.so.2`、`libLLVM.so.22.1` 和 `libclang-cpp.so.22.1`。
因此本轮实证的是：**显式调用既有 dispatcher 时，系统 clang 路径进入 x86_64 accel**。内核自动注册的端到端构建仍未验证。
证据：E/`binfmt.json`、`*-dispatcher-{correct-version,target-alias,compiler-plan,loader-trace}.*`。
首次漏传保留 argv[0] 得到 no input files，已保留；sudo strace 查询无免密授权而未执行，没有输入密码或修改权限。

dispatcher 的本地反汇编 E/`qemu-binfmt-main.stdout` 显示：main 先 realpath，构造 `/emul/%s` 并检查 X_OK，存在则 execve；否则去掉自身 `-binfmt` 后缀进入 QEMU。
对应地址 0x401739–0x40177d、0x40181e–0x40182a、0x40179a–0x4017f7；字符串证据为 `*-qemu-binfmt-strings.stdout`。
**新构建树 clang 不会仅因叫 clang-22 就自动映射到系统 accel**：需要 `/emul/<该完整 realpath>` 对应物。本轮未构建新 ARM clang；对新路径走 QEMU 的判断为该分派逻辑的推导，不能冒充已测新产物。

### 2.3 小规模实验（已结束）

197 字节 C 文件含 float 运算、外部全局地址和栈数组，没有 LLVM 源码编译。四次正常 `-c` 各一次；另各一次 ThinLTO 发射、llvm-dis、IR→机器码、llvm-strip -g。
完整实验脚本 E/`probe.py`，6.507 秒完成，小于 30 分钟；后续版本/路由查询只用了秒级时间。没有校准和性能结论。

宿主显式执行 accel 的方法：

```sh
"$R/emul/lib64/ld-linux-x86-64.so.2" \
  --library-path "$R/emul/lib64:$R/emul/usr/lib64" \
  "$R/emul/usr/bin/clang-22" --no-default-config -fintegrated-cc1 \
  --target=armv7l-tizen-linux-gnueabi --sysroot="$R" \
  <该架构 optflags> <配置末项优化级> -DNDEBUG \
  -fPIC -ffunction-sections -fdata-sections -c "$E/probe.c" -o "$E/armv7l-accel.o"
```

AArch64 改 triple/sysroot 和末项 -O3。显式 QEMU 路径用根内 QEMU→根内 ARM loader→`R/usr/bin/clang-22`，相同 flags、相同输入；不是把 x86 ELF 当作 ARM ELF。
显式 loader 会影响记录命令中的 executable 路径，所以这些探针**不是可直接交给现有白名单的生产命令样本**。

| 目标 | 路径 | wall 秒（含启动） | max RSS KiB | exit / readelf |
| --- | --- | ---: | ---: | --- |
| armv7l | x86_64 accel | 1.344708 | 79728 | 0，ARM ELF32 little-endian ET_REL |
| armv7l | ARM clang 经 QEMU | 0.754935 | 133964 | 0，同架构 ET_REL |
| aarch64 | x86_64 accel | 0.768019 | 82348 | 0，AArch64 ELF64 little-endian ET_REL |
| aarch64 | AArch64 clang 经 QEMU | 1.203709 | 167596 | 0，同架构 ET_REL |

证据：`small-experiment-summary.json`、`*-time.txt`、`*-object.stdout`、`commands.jsonl`。
顺序固定、无预热，I/O/缓存不同；ARM32 这一次模拟路径更快**不构成性能比较**，不得据此估整套 LLVM 的倍率。
两个 accel 22.1.8 均能读自身生成的 bitcode 并产生正确 Machine 的目标文件；IR 记录 PIC Level=2、DWARF4、EnableSplitLTOUnit=0。
ARM32 triple 为 thumbv7、无 tune-cpu；AArch64 有 tune-cpu=cortex-a53。两次 strip exit0、去除探针 DWARF；仅小对象测试，尚未验收 ARM 归档索引。

资源入口为一次 `systemd-run --user`，MemoryMax=6G、swap0、RuntimeMaxSec=1800、nice15/idle I/O；accel 编译另加 4GiB AS。QEMU 地址空间包含 guest reservation，不套该 AS，仍走此实验服务入口。
**容量证据限制：** 服务完成打印的 memory peak 768 KiB 明显小于子进程 RSS，退出后 transient unit 已回收、MemoryPeak 不可读，因此不把该字段作为有效进程树峰值或 cap 覆盖证明。表中只采用 GNU time 的单命令 RSS；未来构建必须重新核对子进程 cgroup 归属和持续采样。
记录：E/`experiment-launch.json`、`experiment-start.json`、`experiment-end.json`、`scope-query.stdout`。

## 3. bitcode 生产者与转换器一致性

T 的 CMAKE_C_COMPILER/CXX_COMPILER 展开为对应根的 triple-clang/clang++，它们解析到 `/usr/bin/clang-22`；显式 dispatcher 实证进入 accel 22.1.8。
**若后续正常构建启用同一分派配置，bitcode 生产者应是这个 x86_64 accel clang**，不是新生成的 ARM clang。
依据：§1.2、E/`*-cfg-links.stdout`、`*-dispatcher-target-alias.stdout`、`*-dispatcher-loader-trace.stderr`。

建议 ARM 转换优先显式选取**同一构建环境、同一身份清单中的 accel clang/llvm-dis/llvm-nm/llvm-ar**，加目标 triple、ABI 与记录 flags；不以新 ARM build/bin/clang 作为默认转换器。
新 ARM clang 可作交叉验证参照；强制执行它会进入模拟路径，也受 32-bit guest VA 等不同约束，不能复用 x86 单进程 4GiB AS 的解释。
`/emul` 中缺工具或版本/输入身份不符时硬失败，不悄悄回退到另一个版本。

现有根的 native 与 accel 都自报 22.1.8；不同 RPM Release/不同 SHA 不等于同 revision 已认证。
未来 OBS 若更换生产者，即使主版本仍 22，也需记录生产者、disassembler、converter、nm 的完整版本/来源/哈希并执行真实 bitcode 读取与代码生成对照。
本轮没有 T 构建出来的 ARM `.a`：两个根 `rpm -q llvm-static-devel` 均未安装，RPMS 无 llvm 包，BUILD 分别仅有 rpi4-linux-kernel 与 e-tizen-data-profile_common。
因而“目标配方预期有 bitcode”来自 LLVM_ENABLE_LTO 与小样本，**不是对未来 RPM 做了归档普查**。

兼容性方向：`llvm/docs/DeveloperPolicy.rst:774–796` 说明较新 LLVM 对旧 bitcode 的读取兼容，文本 IR 无稳定兼容承诺；不能倒推旧工具能读新 bitcode。
docs/33 §4 已实测 lld18 读取 LLVM22 BinaryFormat 报 Unknown attribute kind，机器码版本可读。
公开说明参见 [LLVM IR backwards compatibility](https://llvm.org/docs/DeveloperPolicy.html#ir-backwards-compatibility)；此处以本地 22 源码为版本依据。
本轮仅证明小样本 22→22 成功，没有批准跨版本转换。

## 4. PIC 与重定位认证草案（未改 Source）

现有 `tools/llvm_static_archives_source.py:331–363` 只接受 EM_X86_64/ELF64 little-endian；其规则还区分 SHN_ABS 与目标节写权限，不能机械替换枚举号。
ARM 实现须先按 ELF class 解码：ARM32 `r_sym=r_info>>8`、type低8位；AArch64 为 >>32/低32位；支持 REL/RELA、扩展节数与符号索引，保留成员 ordinal/header-offset/同名 occurrence。
检查的是重定位**所作用的节**（sh_info），不是 `.rel.*` 自身 flags；忽略非 SHF_ALLOC 调试节。

### 4.1 禁止集合候选

对非 SHN_ABS 符号，以下绝对地址重定位出现在 `SHF_ALLOC && !SHF_WRITE` 的节时拒绝；SHN_ABS 常量例外须保留。该表是保守认证设计，尚未跑 ARM 全档普查。

| 架构 | 拒绝 / 特殊处理集合 | 依据 |
| --- | --- | --- |
| ARM | R_ARM_ABS32、ABS32_NOI、ABS16、ABS8、ABS12、THM_ABS5；MOVW_ABS_NC、MOVT_ABS、THM_MOVW_ABS_NC、THM_MOVT_ABS；THM_ALU_ABS_G0_NC/G1_NC/G2_NC/G3 | `llvm/include/llvm/BinaryFormat/ELFRelocs/ARM.def:9–15,50–55,62`；`lld/ELF/Arch/ARM.cpp:105–114`；AAELF32 表的 S+A 类 |
| ARM | TARGET1 默认按绝对地址检查，只有明确 target1-rel 时按相对；TARGET2 必须有平台策略记录，否则拒绝未认证状态。BASE_ABS 也不默认放行 | ARM.cpp:139–149；ARM.def:38,45,48；AAELF32 TARGET1/2 平台选择规则 |
| AArch64 | ABS16/32/64、MOVW_UABS_G0/G0_NC/G1/G1_NC/G2/G2_NC/G3、MOVW_SABS_G0/G1/G2；AUTH_ABS64、FUNCINIT64 作为额外绝对地址类拒绝/另认证 | `llvm/include/llvm/BinaryFormat/ELFRelocs/AArch64.def:10–26,65`；`lld/ELF/Arch/AArch64.cpp:143–171` |

ARM 的小宽度绝对地址和 AArch64 ABS16/32 即使目标节可写也不能自动通过：动态链接器可表达范围/重定位支持需另查，初版可保守拒绝非 SHN_ABS 的这些窄地址重定位。
未知 relocation、未知 TLS 模型/目标选项不自动归入安全集合，输出归档、成员身份、目标节、符号、type 后停止认证。

### 4.2 不能按名字含 ABS 一刀切

AArch64 `ADD_ABS_LO12_NC`、`LDST{8,16,32,64,128}_ABS_LO12_NC` 可与 ADRP 的 page-relative 部分组成正常 PIC 序列；只承载页内低位，不能把 lld 的所有 R_ABS 表项都直接当违规。
ARM 的 PREL31（含 .ARM.exidx）、REL32、PREL MOVW/MOVT、GOT/PLT 相对项也不能全禁。
依据：`lld/ELF/Arch/AArch64.cpp:147–152` 与 [AAELF64](https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst) 的 ADRP/LO12 说明；[AAELF32](https://github.com/ARM-software/abi-aa/blob/main/aaelf32/aaelf32.rst) relocation 表；`ARM.cpp:118–136`。
已归档 ABI 文本 E/`aaelf{32,64}.stdout`，SHA 分别 `45b1c691a16eb0c4186562e5c49f05f6767bddcd865fa14ea6a5cc6839e6c170`、`7432d7d35022d00db30cd8d53ca32a39a958e4acedbb90ffa2c6d572a35ef02f`。

**静态扫描不是共享链接证明。** 最终仍需两架构各用 GNU ld 与 lld 做真实 `-shared -z defs -z text` 链接，核对无 TEXTREL，并运行 dlopen/API 消费者；同时核对 ARM attributes、softfp 参数传递与 Thumb interworking。
正负夹具包含：只读绝对地址负例、SHN_ABS 常量、GOT/PLT/PREL31 正例、AArch64 ADRP+LO12 正例、ABI/triple 不匹配负例。
本轮小对象 readelf 已保存，其成功不替代以上门禁。

## 5. 本机完整 ARM 构建的可行性与成本

**当前结论：不在本机启动完整 ARM LLVM 构建。** 这不是宣称硬件永远做不到；现有路由、磁盘和容量证据不足以认证两种新构建配置。

| 项 | 已有实测 / 本轮观测 | 对 ARM 可作的判断 |
| --- | --- | --- |
| CPU / RAM | nproc20；MemTotal 33,072,914,432 B；22:52 MemAvailable 22,490,279,936 B | 内存达到旧16GiB入口；不证明新的 ARM ThinLTO 链接能在18GiB完成 |
| 当前磁盘 | /home free 43,949,535,232 B = 40.93 GiB | 小于60GiB旧入口，当前直接不准入；本轮未清理任何历史载荷 |
| x86 初始编译链接 | docs/13：7634任务，2:33:40；clang 单链接 VmHWM16.83GiB | 仅 x86 静态配置参考；ARM 链共享 libLLVM、目标子集不同，不能用同构门禁放行 |
| x86 一次完整转换配方构建 | docs/30 §2：16,011.555s；18GiB cap；磁盘入口546,240,655,360→最低310,857,240,576 B | 主机空闲空间减少约219.22GiB，含 cache/证据/RPM且非独占磁盘计量；60GiB只是入口，不是全过程容量估计 |
| x86 转换 | docs/28：225档/3853成员，782.346s；docs/35 真实install有完整逐成员记录 | 能给数百秒至千秒级的历史 x86参考，不能按架构名乘倍率预测 ARM |
| 本机 ARM LLVM 历史日志 | 现有两根BUILD不是LLVM；RPMS无llvm；检索根内已有log未找到LLVM完整构建 | 完整 wall、自然RSS峰值、磁盘峰值 **UNKNOWN** |
| 本轮 tiny C | §2.3，单次0.75–1.35s，RSS约78–164MiB | 只证明能执行/发射目标；不外推到 LLVM 最大TU或ThinLTO链接 |

证据：E/`resources.stdout`、`capacity-now.json`、`*-build-root-top.stdout`、`*-project-rpm-files.stdout`、`*-existing-build-logs.stdout`；docs/30 §2 表。
时间判断仅到“参考 x86 是多小时级，ARM 的可信区间/上界不能估出”；不给无证据的 ARM 小时数或内存倍数。
未来完整构建应在已配置 accel 的 OBS/Quickbuild 执行，单架构串行，先记录硬件/宏/工具身份，再记录 compile/link/install/debuginfo 分阶段峰值与磁盘；不预先保证18GiB、6/6/2足够。
本机先做有限 TU 的 O-level/ABI/PIC/符号认证，采样中等与最大真实归档成员后才可估转换阶段时间；需要目标原归档与构建日志供给。本轮不安排完整构建。

## 6. 公开快照消费者现状

沿用 docs/33 §5 的固定公开 Base `tizen-base-toolchain_20260912.061113` 与 Unified `tizen-unified-toolchain_20260814.092727` 调查；不是重新声称旧 Base URL 仍在线。
元数据361/1061源码条目、源包摘要、补丁后 CMake 和构建日志均已归档；本轮只核对已有证据。

| 架构 | 直接 BuildRequires llvm-static-devel | 实际 LLVM 链接形态 | 证据 |
| --- | --- | --- | --- |
| armv7l | bcc-tools、bpftrace | 两者可见发布构建均使用共享 LLVM/clang | E33/sources/bcc-tools-0.35.0-1.1/bcc-tools.spec:272–275、sources/bpftrace-0.24.2-1.1/bpftrace.spec:93；E33/downloads/base/logs/armv7l/succeeded/bcc-tools.buildlog.txt:2701、bpftrace.buildlog.txt:3578,3594 |
| aarch64 | bcc-tools、bpftrace | 同上 | aarch64/succeeded/bcc-tools.buildlog.txt:2684、bpftrace.buildlog.txt:3583,3599 |

E33=`W/temp/llvm-strip-alternative-20260929`；精确源文件定位见 docs/33 §5.2–§5.3。
bcc 的 ENABLE_LLVM_SHARED=ON，bpftrace 的 STATIC_LINKING=OFF；BR 含 static-devel 不能当实际消费 `.a` 的证据。
**在该限定公开数据内未确认 ARM 静态 LLVM 消费者；不能推出 SR 私有项目或整个平台没有消费者。**
llvm-devel 的参照名单不含归档证据；不把这个名单扩大为 static-devel 受影响包数。最终 GNU ld/lld 的 exec 未完整保存的项仍保持 docs/33 的 UNKNOWN。

## 7. 保持 x86_64 不变的 Source 设计与验证

### 7.1 结构草案

保持现有 x86_64 策略入口、默认参数、flags 顺序、clang 路径、IR 断言、PIC规则及确定性归档行为原样；ARM 走独立 policy 分派，不把 ARM 参数塞进全局宽泛白名单。
候选结构（只设计）：

```text
policy_for_arch(arch)
  x86_64 -> 原 classifier / 原 ir_settings / 原 pic_relocations / 原 argv 构造
  armv7l -> 精确 ARM32 token策略、末项Os、thumbv7、softfp、ELF32 REL/RELA
  aarch64 -> 精确 AArch64 token策略、末项O3、tune-cpu、ELF64 RELA
```

共有层只管理归档 header-offset 身份/次序、取消/超时、原子回写、强符号与幂等状态；所有新增分支在选择 x86_64 时不可达。
ARM 版本/default差异写入该架构表，未知token/type metadata/版本仍硬失败；不能因为某参数“上游支持”就放行。
CLI 将来新增两个 arch choices；spec 原 x86 条件与命令逐字保留，ARM 条件增加独立命令，编译器/disassembler/nm 选择绑定该根 accel 清单。
不改工具本身构建/链接参数，不把转换步骤并发叠加在 LLVM 编译期。

### 7.2 全量 x86 回归契约

基准 Source SHA：`6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557`。
docs/35 strip 前转换记录仍在：

```text
E35/ba-install-conversion-evidence/summary.json
SHA256 4d824c4f2c9fae5b1064e76b1eb8b328248bdbbfca2beb98b32759592529fcd6
status=PASS, archives=225, members=3864（3853转换 + 11原机器码）
```

本轮已核对该记录结构和摘要，见 E/`x86-regression-anchor.json`；记录包括每档 before_sha256/after_sha256 与 results 中每个 ordinal/name/sha256。
**未来验证方法，不在本轮执行：**

1. 只读复制 docs/35 的构建树原件；因 RX 后来被 docs/38续跑过，必须先逐档核对 `before_sha256`，再核对原成员身份。输入不同即停止，不能用新输入给“不变”背书。
2. 同版本/同哈希转换工具、相同 flags 顺序、cwd/路径语义、4 worker/AS与 Source defaults，在新输出目录跑改后 Source 的225档。
3. 每档完整归档 SHA 必须等于记录的 `after_sha256`；每个成员按 ordinal+name+occurrence 比 SHA，全部3864个相同；原11机器码成员仍与输入相同。不能拿已经strip的 RPM `.a` 作 strip 前基准。
4. 旧/新 Source 的 x86 CLI、白名单正负、末项规则、metadata、超时取消、强符号、安装失败、SKIP等全套测试重跑；逐条 x86 argv 与既有记录一致。
5. 标准 strip 后再验索引、GNU ld无LTO消费者和compiler-rt；356639 rebase 后另跑 llvm-strip 规则。x86 RPM 结果变化必须解释并停止“不变性”认证，不能自动豁免。

原实现文本 IR parsing 对 LLVM22 的依赖、四类架构变化点见 Source头注释及 docs/32。ARM 初版只扩大显式架构表，不进行附带重构。

## 8. ARM 的 llvm-strip 与宏链

两根 `/usr/bin/llvm-strip -> llvm-objcopy` 是目标架构 ELF；对应 `/emul/usr/bin/llvm-strip` 为 x86_64 ELF，实测22.1.8。
包归属查询：

```text
RA:  llvm-22.1.8-1.6.armv7l
     clang-accel-x86_64-armv7l-0.4-1.1.armv7l
R64: llvm-22.1.8-19.1.aarch64
     clang-accel-x86_64-aarch64-0.4-1.4.aarch64
```

实际 dispatcher 会先 realpath：llvm-strip 的原生软链接解析成 llvm-objcopy，因此分派可能进入 **/emul/usr/bin/llvm-objcopy**，但 argv[0] 仍 llvm-strip，选择 strip 模式；不误写成只看文本路径就确定实体文件。
E/`*-dispatcher-correct-strip.stdout` 已证明此入口可运行；完整工具清单与反汇编支撑路径解释。最终 OBS 必须再用执行记录留存 ELF身份。

| 两个根内文件:行 | 宏链行为 | 与 x86_64 对照 |
| --- | --- | --- |
| usr/lib/rpm/macros:83 | `%__strip /bin/strip` | 默认相同；ARM尚未应用356639扩展 |
| usr/lib/rpm/tizen/macros:34–38 | brp-strip 仅在未定义debug包时；static-archive总接 `%__strip`；comment-note注释 | 相同条件结构 |
| tizen/macros:40–46,53–60 | 原后处理与debug阶段衔接 | 与docs/38 §1同结构 |
| brp-strip-static-archive:7,15–20 | 取首参，逐档 `$STRIP -g` | 相同调用方式，不用总rpmbuild成功代替逐档exit证据 |
| find-debuginfo.sh:269,275,277–280 | 默认eu-strip；不读 `%__strip` | 相同，须保留当前debug条件 |

证据：E/`*-usr_lib_rpm_*.stdout`、`*-strip-macro-uses.stdout`、`*-strip-macro-hashes.json`；docs/38 §1。
本轮 `--eval` 未解析spec时打印了未定义 `__debug_package` 的 brp-strip 分支，不能把该查询当成未来开debuginfo时确实执行了brp-strip；上表按宏条件明确区分。

ARM 转换完成后应全为目标机器码；本轮仅证明两个 accel llvm-strip 能处理对应的小对象并去掉调试段。
不能直接把 docs/38 的 x86 compiler-rt 结构差异集合认证给 ARM：未来需分别比较所有 SHF_ALLOC 类型/flags/大小/内容、索引、成员身份/次序、ARM属性与运行库消费者；新结构类别必须登记评审。
不能让 llvm-strip 接原 bitcode 并靠失败不改文件来“保索引”（docs/33 §1已有反例）。

## 9. 供 PM 决定的实施步骤与 patchset 更新

1. **补齐输入与环境。** 选择将构建 T/356627 的 ARM OBS 项目、固定 buildconfig/包源；确认 binfmt/accel 的真实 exec、各工具SHA、CMake版本、root宏。取得代表真实 TU/原bitcode及原argv；本机不替用户改系统配置。
2. **小规模认证。** 按§1.3分别做直接去LTO编译与ThinLTO→转换对照：节区/符号绑定可见性、ABI、Thumb/ARM模式、EHABI/unwind、PIC及shared链接；参数先按实际命令全集建立白名单，再加正负样本。两种架构不共享“猜测默认值”。
3. **实现356627增量并守住x86。** 采用§7分派结构，x86代码/命令保持；在隔离工作树跑225档/3864成员的全量SHA门禁。此步预算可参考docs/28离线782s和docs/35逐成员数据，但完整重测仍以新记录为准。
4. **ARM完整试包在服务器。** 两架构各一次完整构建和静态库/运行库/非归档/宏链验收。static-devel实际归档数以各架构inventory为准，不硬套x86的225/45；GNU ld无LTO、lld、共享库、GC-sections、API/内嵌lld消费者以及幂等两步全部重做。记录生产者与转换器一致性。
5. **更新356627。** 用户上传前只读fetch最新 `refs/changes/27/356627/<PS>`；以其确切父分支为基准，在隔离工作树修改/amend，保留作者 FatTank `<hao.lin@samsung.com>` 与 Change-Id `Id4eb147e7ec4764d58a81110cf7bf57d21b64ac8`。补丁含ARM支持，不夹带llvm-strip宏；生成format-patch、干净base apply --check及x86回归报告。用户向 `refs/for/tizen_base` 上传后应更新原356627。
6. **更新356639并重挂依赖。** fetch `refs/changes/39/356639/<PS>`，将该独立change rebase/cherry-pick到新356627提交；保留其 Change-Id `Iac085555112855d60cc7591931e91466691db6b2`（docs/38生成记录；执行时核对Gerrit最新提交），仅在ARM转换已通过后扩展strip架构条件。新的父提交必须是新356627，不留在旧67619ec8上；重做ARM strip/运行库消费者与x86不变性后由用户更新原356639。

以上是方案，不是已执行的实现、全量转换、构建或Gerrit操作；不新开review，不改现有两份patch。

### 待补齐 / UNKNOWN

| 项 | 已尝试与缺口 | 需要的条件 |
| --- | --- | --- |
| 自动accel端到端构建 | 普通GBS chroot失败；显式dispatcher与/emul加载已成功 | 维护方确认有效binfmt注册与worker执行trace |
| T实际ARM归档与完整原argv | 两现有根无static-devel/LLVM BUILD；本轮只发射小C bitcode | OBS/Quickbuild原构建树或未转换归档+compdb/记录命令 |
| CMake追加flags最终值 | T/rpmspec完整展开；用已验证CMake3.31.2推导优化末项 | ARM实际CMake版本/Cache/build.ninja核对 |
| ARM完整构建成本 | 无本机对应日志，磁盘低于入口；tiny C不是代表负载 | 服务器分阶段采样、归档/转换规模普查 |
| 新ARM clang的执行/兼容性 | 只有已装ARM clang的QEMU小实验；未生成新工具 | 新产物身份与显式模拟对照，或采用同生产者accel认证 |
| 真实静态消费者范围 | 固定公开数据两直接BR包实际共享 | 私有项目依赖与实际链接日志，不能凭BR补名单 |
| ARM归档PIC/符号/运行库完整认证 | 仅本轮小对象正确架构、IR/strip成功 | §4与§9完整矩阵，不能借x86的PASS代替 |

## 附录 A. 完整公共 flags 与 CMake 参数清单

下面的 flags 由原始输出生成；连续空格保留。每架构 CMAKE_C_FLAGS、CMAKE_CXX_FLAGS、CMAKE_ASM_FLAGS 在这次展开中相同。
`optflags` 与后续 CMake 参数是两个层次；特别是 AArch64 的公共 -Os 并不覆盖 Release 后追加的 -O3。

### X：x86_64

`%optflags`：

```text
-Os -fstack-protector -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument -momit-leaf-frame-pointer  -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables -fno-omit-frame-pointer -g
```

`CMAKE_C_FLAGS = CMAKE_CXX_FLAGS = CMAKE_ASM_FLAGS`：

```text
  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument   -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables  -g -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument
```


### A32：armv7l

`%optflags`：

```text
-Os -fstack-protector -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument  -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -march=armv7-a -mtune=cortex-a8 -mlittle-endian -mfpu=neon -mfloat-abi=softfp -mthumb -Wp,-D__SOFTFP__ -D_FILE_OFFSET_BITS=64 -g
```

`CMAKE_C_FLAGS = CMAKE_CXX_FLAGS = CMAKE_ASM_FLAGS`：

```text
-Os -fstack-protector -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument  -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -march=armv7-a -mtune=cortex-a8 -mlittle-endian -mfpu=neon -mfloat-abi=softfp -mthumb -Wp,-D__SOFTFP__ -D_FILE_OFFSET_BITS=64 -g
```


### A64：aarch64

`%optflags`：

```text
-Os -fstack-protector -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument  -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -march=armv8-a+fp+simd+crc+crypto -mtune=cortex-a53 -g
```

`CMAKE_C_FLAGS = CMAKE_CXX_FLAGS = CMAKE_ASM_FLAGS`：

```text
-Os -fstack-protector -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument  -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -march=armv8-a+fp+simd+crc+crypto -mtune=cortex-a53 -g
```


### 其余 CMake 定义逐项对照

下表来自三份展开的参数字典；`—` 表示该架构 spec 未显式传此项，不等于实际 CMake 默认为空。生成器三者均为 Ninja；末尾源码参数均为 `../llvm`。

| 参数 | x86_64 | armv7l | aarch64 |
| --- | --- | --- | --- |
| `CLANG_BUILD_CLANG_DYLIB` | `ON` | `ON` | `ON` |
| `CLANG_ENABLE_ARCMT` | `OFF` | `OFF` | `OFF` |
| `CLANG_LINK_CLANG_DYLIB` | `OFF` | `ON` | `ON` |
| `CLANG_RESOURCE_DIR` | `../lib64/clang/22` | `../lib/clang/22` | `../lib64/clang/22` |
| `CMAKE_AR` | `/usr/bin/llvm-ar` | `/usr/bin/llvm-ar` | `/usr/bin/llvm-ar` |
| `CMAKE_BUILD_TYPE` | `Release` | `MinSizeRel` | `Release` |
| `CMAKE_CXX_COMPILER` | `clang++` | `armv7l-tizen-linux-gnueabi-clang++` | `aarch64-tizen-linux-gnu-clang++` |
| `CMAKE_C_COMPILER` | `clang` | `armv7l-tizen-linux-gnueabi-clang` | `aarch64-tizen-linux-gnu-clang` |
| `CMAKE_EXE_LINKER_FLAGS` | `-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections` | `-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections` | `-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections` |
| `CMAKE_INSTALL_PREFIX` | `/usr` | `/usr` | `/usr` |
| `CMAKE_RANLIB` | `/usr/bin/llvm-ranlib` | `/usr/bin/llvm-ranlib` | `/usr/bin/llvm-ranlib` |
| `CMAKE_SHARED_LINKER_FLAGS` | `-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections` | `-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections` | `-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections` |
| `LLVM_BINUTILS_INCDIR` | `/usr/include` | `/usr/include` | `/usr/include` |
| `LLVM_BUILD_DOCS` | `OFF` | `OFF` | `OFF` |
| `LLVM_BUILD_EXAMPLES` | `OFF` | `OFF` | `OFF` |
| `LLVM_BUILD_LLVM_DYLIB` | `ON` | `ON` | `ON` |
| `LLVM_BUILD_TESTS` | `OFF` | `OFF` | `OFF` |
| `LLVM_DEFAULT_TARGET_TRIPLE` | `x86_64-tizen-linux-gnu` | `armv7l-tizen-linux-gnueabi` | `aarch64-tizen-linux-gnu` |
| `LLVM_ENABLE_ASSERTIONS` | `No` | `No` | `No` |
| `LLVM_ENABLE_DOXYGEN` | `OFF` | `OFF` | `OFF` |
| `LLVM_ENABLE_LTO` | `Thin` | `Thin` | `Thin` |
| `LLVM_ENABLE_PER_TARGET_RUNTIME_DIR` | `OFF` | `OFF` | `OFF` |
| `LLVM_ENABLE_PROJECTS` | `clang;lldb;clang-tools-extra;lld;compiler-rt;openmp` | `clang;lldb;clang-tools-extra;lld;compiler-rt;openmp` | `clang;lldb;clang-tools-extra;lld;compiler-rt;openmp` |
| `LLVM_ENABLE_RTTI` | `ON` | `ON` | `ON` |
| `LLVM_HOST_TRIPLE` | `x86_64-tizen-linux-gnu` | `armv7l-tizen-linux-gnueabi` | `aarch64-tizen-linux-gnu` |
| `LLVM_INCLUDE_DOCS` | `OFF` | `OFF` | `OFF` |
| `LLVM_INCLUDE_EXAMPLES` | `OFF` | `OFF` | `OFF` |
| `LLVM_INCLUDE_TESTS` | `OFF` | `OFF` | `OFF` |
| `LLVM_LIBDIR_SUFFIX` | `64` | `` | `64` |
| `LLVM_LINK_LLVM_DYLIB` | `OFF` | `ON` | `ON` |
| `LLVM_MLGO_EMBED_TF_XLA_RUNTIME_OBJECTS` | `/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/xla_compiled_cpu_function.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/cpu_function_runtime.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/custom_call_status.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/executable_run_options.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/runtime_single_threaded_matmul_f32.cc.o` | `/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/xla_compiled_cpu_function.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/cpu_function_runtime.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/custom_call_status.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/executable_run_options.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/runtime_single_threaded_matmul_f32.cc.o` | `/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/xla_compiled_cpu_function.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/cpu_function_runtime.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/custom_call_status.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/executable_run_options.cc.o;/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/xla_runtime_objects/runtime_single_threaded_matmul_f32.cc.o` |
| `LLVM_MLGO_EXPORT_TF_XLA_RUNTIME` | `OFF` | `OFF` | `OFF` |
| `LLVM_OPTIMIZED_TABLEGEN` | `ON` | `ON` | `ON` |
| `LLVM_OVERRIDE_MODEL_HEADER_INLINERSIZEMODEL` | `/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/InlinerSizeModel.h` | `/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/InlinerSizeModel.h` | `/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/InlinerSizeModel.h` |
| `LLVM_OVERRIDE_MODEL_HEADER_REGALLOCEVICTMODEL` | `/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/RegAllocEvictModel.h` | `/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/RegAllocEvictModel.h` | `/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/RegAllocEvictModel.h` |
| `LLVM_OVERRIDE_MODEL_OBJECT_INLINERSIZEMODEL` | `/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/InlinerSizeModel.o` | `/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/InlinerSizeModel.o` | `/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/InlinerSizeModel.o` |
| `LLVM_OVERRIDE_MODEL_OBJECT_REGALLOCEVICTMODEL` | `/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/RegAllocEvictModel.o` | `/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/RegAllocEvictModel.o` | `/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/RegAllocEvictModel.o` |
| `LLVM_PARALLEL_COMPILE_JOBS` | `6` | `6` | `6` |
| `LLVM_PARALLEL_LINK_JOBS` | `2` | `2` | `2` |
| `LLVM_TARGETS_TO_BUILD` | `X86;ARM;AArch64;BPF` | `ARM;BPF` | `AArch64;BPF` |
| `LLVM_TARGET_ARCH` | `—` | `ARM` | `AArch64` |
| `LLVM_TARGET_TRIPLE_ENV` | `x86_64-tizen-linux-gnu` | `armv7l-tizen-linux-gnueabi` | `aarch64-tizen-linux-gnu` |
| `LLVM_USE_LINKER` | `lld` | `lld` | `lld` |
| `TENSORFLOW_AOT_PATH` | `/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/mlgo_sysroot` | `/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/mlgo_sysroot` | `/home/abuild/rpmbuild/BUILD/llvm-22.1.8/mlgo_verify_assets/mlgo_sysroot` |
| `TIZEN` | `1` | `1` | `1` |

## 附录 B. 原始输出、命令与提交自检

所有正文 E 路径位于 `W/temp/arm-archive-feasibility-20261009`，不上传大文件；`commands.jsonl` 记录主查询/实验的argv、环境差异、exit、wall及stdout/stderr文件。
`audit.py`、`expand.py`、`probe.py` 是本轮证据生成入口，只放temp，不是生产转换实现。
完整工具清单、原生/accel ELF输出、root宏原文、rpmspec展开、ABI文本、CMake比较、probe .bc/.ll/.o、逐次错误输出均保留；失败查询没有删掉。
本轮会话另有只读定位/search命令，其关键结果已归入上述带行号摘录；不声称 commands.jsonl 包含交互定位时每条 grep/ls。

- 未构建 LLVM/Chromium、未运行GBS build/rpmbuild、未全量转换归档；小实验6.507秒，另有秒级查询，未超过30分钟。
- spec、Source、两份提交补丁、W/llvm与历史报告未改；最终hash核对见 protected-final.json。GBS查询包装器的resolver副作用已在§0明确登记，不掩盖为绝对零写入。
- 不推Gerrit；只提交本报告与STATUS到GitHub。未改变现有x86认证指纹或资源门槛。
- 本轮结论是**可实施的认证方案与局部可执行性证据**，不是ARM修复交付或性能收益认证。
