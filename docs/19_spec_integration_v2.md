# 19 BOLT 集成设计修订：固定快照生效门禁阻塞

日期：2026-09-21。**BLOCKER：当前固定 Base 快照的 accel clang 仍动态依赖
libLLVM/libclang-cpp，与本项目已做 BOLT 的静态 LLVM 形态不同。自研 spec 尚未进入该快照。**

本文件取代 [docs/18](18_spec_integration.md) 作为后续工作的**决策、准入条件与当前状态**入口；
docs/18 原文保留不动。按本轮明确指令：

> 若是动态形态，说明自研 spec 尚未进入该快照，写明并停下报告。

已触发该条件，故本轮止于只读调查和报告。**没有继续完整集成设计定稿、身份脚本修订、
新增测试或两个低成本实验。** 本文件是自包含的门禁阻塞版本，不冒充已完成的可实施 v2。
已确认的 PM 决策与 22 项处置逐项登记在第 4、5 节，恢复后按此继续。

对外统一表述：**筛选层多轮测量方向一致，BOLT 对 LLVM 自身源码编译负载有稳定正向影响，
量级待构建服务器验收。** 这里不对外给收益百分比，也不延续“五轮独立”的说法。

## 1. 生效路径与停止依据

### 1.1 已知流水线与实际调查对象

直接采用用户确认的事实，不重新论证：

```text
自研 x86_64 LLVM spec
  → OBS 构建 x86_64 LLVM RPM
  → qemu-accel 消费其中的二进制
  → 新 Base 镜像/固定快照
  → Quickbuild worker 的 /emul/usr/bin/clang-22
  → Chromium 平台 clang 路由（_use_gbs_clang=1）
```

Quickbuild 已确认使用平台 clang，不是 bundled clang 18；验收仍须保存
`ninja -t commands` 的实际 cc/cxx，并在非计时诊断中确认最终 exec ELF。
**部署闭环已知成立，不等于目前钉住的旧快照已包含自研 spec。**

本轮从 `gbs_llvm.conf:9` 实际固定的 URL 调查，没有修改配置或另选快照：

```text
https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/
  tizen-base-toolchain_20260912.061113/repos/standard/packages/
```

上面换行为展示；真实 URL 中没有空白。Unified 固定快照仍为
`tizen-unified-toolchain_20260814.092727`（gbs_llvm.conf:12），本次两个对照 RPM
均来自同一个 Base 快照。

### 1.2 实测结论

从该快照重新下载两份 RPM，用原归档 primary.xml 中的 SHA256 校验通过，再仅解包
各自的 clang-22 文件，执行 `file`、`readelf -hW/-dW/-SW/-lW/-nW`、SHA256 和 cmp。
**没有执行这两个快照编译器，也没有触发 binfmt/accel 分派。**

| 对象 | 文件字节数 | 是否直接依赖 libLLVM/libclang-cpp | LLVM 链接形态 |
| --- | ---: | --- | --- |
| 快照 x86_64 clang RPM 内 `/usr/bin/clang-22` | 120,608 | 两者均依赖 | 动态 LLVM |
| 同快照 accel RPM 内 `/emul/usr/bin/clang-22` | 131,592 | 两者均依赖 | 动态 LLVM |
| 工作区 RPM 基线 `TC/bin/clang-22` | 139,929,464 | 均不依赖 | 静态链接 LLVM 库 |
| 已做 BOLT 的实际输入 `Q/stripped/bin/clang-22` | 226,730,672 | 均不依赖 | 静态链接 LLVM 库 |

这里“静态”仅指 LLVM/clang 库链接方式，并不表示不依赖 libc 等运行库。
证据：`A/binary-inspection.json`、`A/binary-investigation.txt` 与各对象的 `*-dynamic.txt`。

**明确回答：当前快照 accel 是动态形态，与被 BOLT 的形态不一致。**
快照 clang 的 RPM VCS 是 `8dfebafe1a477b3dcc678ee4cb18a3a4306d5a7c`，工作区自研
源码提交为 `f111162e94aa48ed367c9d2c039456c70e7160ae`。包身份、实际 NEEDED 与大小共同
支持“当前快照尚未包含本次自研静态 LLVM spec”的结论，未单凭提交号或大小推断。

这个发现不推翻已经完成的静态 clang BOLT 筛选结果，也不否认 OBS→accel→Quickbuild
流水线；它阻止我们把该快照的动态薄壳当成已测静态输入继续认证。

### 1.3 每个转换环节的身份追踪要求

调查已证明 qemu-accel 会修改 ELF，故不能要求整条流水线一个 SHA 不变。后续应记录
**带转换关系的多份哈希清单**：

| 环节 | 必须记录 | 当前状态 |
| --- | --- | --- |
| LLVM OBS 构建 | source/spec/patch/config 身份、宏、Release、RPM SHA、RPM 内 clang SHA、BOLT/profile 状态 | 当前快照是旧动态形态；自研新构建未在该快照出现 |
| qemu-accel 输入 | 安装的 x86_64 clang/llvm NEVRA、RPM SHA、复制前 clang SHA | spec 显示消费已安装文件；完整原始依赖清单 UNKNOWN |
| qemu-accel 输出 | qemu VCS、patchelf 等处理器版本/命令、输入→输出 SHA、输出 NEEDED/节区、accel RPM SHA | 当前两份 ELF 及 RPM SHA 已实测；所有转换版本/隐式后处理尚未完全还原 |
| Base 快照 | 固定 URL、repodata/checksum 与 accel RPM SHA | 已从固定快照下载并校验 |
| Quickbuild worker | `CC_EMUL=/emul/usr/bin/clang-22` 的实际 SHA、NEEDED、BOLT 特征、RPM 归属和 exec trace | 必须在未来验收现场检查；不能用本机解包路径替代 worker |

发布清单应把上游输入 hash 与 accel 处理后 hash 都列出，并验证 BOLT 节区在每次处理后
的实际保留情况。最终身份以 Quickbuild worker 上执行的 ELF 为准。

## 2. 调查一：qemu-accel 如何消费 x86_64 LLVM

### 2.1 原始材料、来源与限制

本机路径记号：

```text
W  = /home/linhao/Toolchain/development/llvm-optimize
A  = W/temp/spec-review-20260921
TC = W/temp/toolchain-baseline/usr
Q  = W/temp/bolt-measurement-20260918/run
QS = A/source-rpm/qemu-accel-aarch64.spec
```

从快照 source 索引实际找到并下载：
[固定快照 qemu-accel SRPM](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260912.061113/repos/standard/source/qemu-accel-0.4-1.1.src.rpm)。
HTTP 200，13,706 字节，SHA256：

```text
1a78b7b192b2151cc1e0b12cf92ba1b1bc179ccfb8aec3090a68f365b623ff0b
```

`rpm -qpl` 实际只列出 **qemu-accel-aarch64.spec**；源码包中没有独立 Source tarball、
armv7l 生成 spec 或 baselibs_body。不能把它命名成不存在的 qemu-accel.spec。
QS:1–2 设定 cross=aarch64；QS:38 的 VCS 是
`platform/upstream/qemu-accel#e01aa7250a1a73aa8f88ba9ac4a05cbc954d1c9f`，与本次
armv7l accel RPM 的 VCS 相同（A/rpm-metadata.txt）。

下列结论明确来自**该固定 VCS 的已下载 aarch64 生成 spec 中的通用处理主体**。
对 armv7l 分支无法仅凭这个源包还原的部分标 UNKNOWN；随后用实际 armv7l ELF 验证
解释器变化、RUNPATH 和字节差异，没有把 aarch64 条件分支冒称 armv7l 实际执行日志。

尝试获取该 VCS 的完整源码以补 armv7l/baselibs：
`review.tizen.org/gerrit/...` 需要凭据，`review.tizen.org/git/...` HTTP 403，
`git.tizen.org/cgit/...` TLS 失败。未改变认证/系统配置；这些缺口保留为 UNKNOWN。
原始记录见 A/qemu-git-remote.txt、qemu-git-public.txt、downloads.jsonl。

### 2.2 消费与转换过程

| 步骤 | QS 的 file:line | 结论 |
| --- | --- | --- |
| 安装构建依赖 | QS:72 `BuildRequires: clang`；QS:82 `BuildRequires: llvm-devel`；QS:89 `ExclusiveArch: x86_64` | 消费 x86_64 构建环境已安装的工具/库；不是在本段逐个执行 rpm2cpio 解包 LLVM RPM |
| build 阶段 | QS:126–131 | prep 空；build 仅 sanitizer 条件下恢复 flags；这里没有重新编译/链接 clang |
| 生成 clang 文件清单 | QS:305–331；QS:337–347 | 从 `/usr/bin/clang-*`、clang++、llvm-*、lld、ld.lld 等开始；用 ldd 收集库、readlink -f 补真实路径 |
| 原件复制 | QS:366–385 | `patch_binary` 中 `cp -aL $binary $outfile`，目标位于 buildroot/emul 下；先跟随源软链接复制实体 |
| 改解释器 | QS:389–392 | `patchelf --print-interpreter` 成功时执行 `--set-interpreter %{emul_path}$rtld`，**会改 ELF** |
| 改 RUNPATH | QS:394–400 | 仅当已有 RUNPATH 非空且以 `/` 开头，改为 `/emul/%{_libdir}`；相对 `$ORIGIN` 路径不走此分支 |
| 执行 patch | QS:404–409 | 对收集的文件逐个后台调用 patch_binary 后 wait |
| 恢复 clang 别名 | QS:619–645 | 用 cmp 识别与 clang-major 相同的副本，删除该副本并创建软链接；另加 clang 与 target-triple 别名 |
| accel 包转架构 | QS:587–617 | 生成基于 cross 的 baselibs.conf prologue，并拼接 baselibs_body；后者缺失，完整实际转包动作 UNKNOWN |
| 其他后处理 | QS:682 `%fdupes`；QS:694–705 `%files` | 有去重宏与 RPM 后处理接口；宏展开/完整 OBS 打包日志没有包含在该 SRPM 中，不能凭此排除 ELF 后续变更 |

`rpm2cpio`、`eu-strip`、`objcopy`、`strip` 等名字也出现在 QS 的**被复制工具清单**中；
不能把这些列表项当作它们已经对 clang 执行的命令。通用 patch_binary 没有 clang 重新链接、
objcopy 或 prelink 调用。QS:29–32 的 `_rpm_strip_disable=1` 只在 armv7hl 宏条件内，
**不能推出 armv7l 的 strip 被关闭**。隐式 brp/转包动作仍需对应 OBS 日志/宏与完整源码证明。

### 2.3 对 BOLT 节区的影响与身份后果

- patchelf 修改 PT_INTERP，特定条件下修改 RUNPATH，足以使整个 ELF SHA 改变。
  本次两个 ELF 的解释器实测差异支持该转换确实发生；没有声称全部字节差异仅由这一项解释。
- `.note.bolt_info`、`.bolt.org.*`、`.text.cold` 在本次两个快照文件中均未观察到。
  因输入没有这些节区，**本次调查不能实证 patchelf/brp 会保留未来 BOLT 标记**。
- patchelf 或后续 strip 是否移动、保留、删除各 BOLT 节区必须在未来试包中逐段检查，
  不能用“修改解释器不改变源程序语义”替代节区保留和最终执行正确性验证。
- `%fdupes` 与重建别名使 link 类型也须重新枚举；仅替换一个文件名不保证所有硬链接别名
  随之更新。当前没有执行任何二进制改写来试验这个问题。

因此，qemu-accel 不能视作“原样复制所以 hash 不变”的透明封装；原始 RPM hash、
RPM 内 ELF hash、accel 输出 ELF hash 都要分别认证。

## 3. 调查二：当前快照 accel 的实际形态与字节比较

### 3.1 下载与 RPM 身份

两个下载均 HTTP 200，SHA256 与
`W/temp/snapshot-archive/tizen-base-toolchain_20260912.061113/primary.xml` 匹配。
A/package-metadata.json 保存命中条目；A/downloaded-rpms.json、downloads.jsonl 保存 URL、
HTTP headers、文件大小与校验结果。

| RPM | 包字节数 | RPM SHA256 | VCS |
| --- | ---: | --- | --- |
| clang-22.1.8-1.6.x86_64.rpm | 29,048,537 | `574c6bdcf0dd272dcbb7445133b11674d67391f1089df20eb832c1dffb81dd36` | llvm#8dfebafe1a477b3dcc678ee4cb18a3a4306d5a7c |
| clang-accel-x86_64-armv7l-0.4-1.1.armv7l.rpm | 54,806,369 | `919fa8d921b8432f2d2fbe7d9bed344acff18bda2f49fd25f5e45cc8712b0a3e` | qemu-accel#e01aa7250a1a73aa8f88ba9ac4a05cbc954d1c9f |

分别来自同一 packages URL 下的 `x86_64/` 和 `armv7l/`。accel RPM 标签的架构是 armv7l，
**里面的 clang 是 x86_64 ELF**；不得拿 RPM 架构标签代替 ELF Machine。

解包实际命令以 clang RPM 为例（完整绝对路径、cwd、退出码见 A/*-extract.txt）：

```bash
rpm2cpio clang-22.1.8-1.6.x86_64.rpm \
  | cpio -idm --no-absolute-filenames ./usr/bin/clang-22
```

accel 对应 `./emul/usr/bin/clang-22`。两条都在 A/unpacked/ 下独立目录执行，未安装到宿主。

### 3.2 ELF 哈希与实际动态段

| ELF | SHA256 |
| --- | --- |
| 快照 x86_64 clang | `df5778e25058bb2746512c772483f7f40e42fe27c7e4077c1f1f03a6be6cac5c` |
| 快照 armv7l accel 内 x86_64 clang | `590fa22e2859a15c3d05c46aca08958949bb0cc7ab5abf293ae8ea2f338daa1b` |
| 工作区静态 LLVM RPM 基线 | `3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c` |
| 实际 BOLT 剥离输入 | `eccfb075bc3b2a6ca2bda5a2a6e68f6a29ba48b5586cb603f4b46080f656013e` |

快照 accel 的 `readelf -dW` NEEDED/RUNPATH 原始摘录：

```text
 0x000000000000001d (RUNPATH)            Library runpath: [$ORIGIN/../lib64]
 0x0000000000000001 (NEEDED)             Shared library: [libclang-cpp.so.22.1]
 0x0000000000000001 (NEEDED)             Shared library: [libLLVM.so.22.1]
 0x0000000000000001 (NEEDED)             Shared library: [libstdc++.so.6]
 0x0000000000000001 (NEEDED)             Shared library: [libm.so.6]
 0x0000000000000001 (NEEDED)             Shared library: [libgcc_s.so.1]
 0x0000000000000001 (NEEDED)             Shared library: [libc.so.6]
```

两个快照文件的这些 NEEDED 与 RUNPATH 相同；主体 LLVM 代码在共享库中。
工作区 RPM 基线与 BOLT 输入的 NEEDED 列表中没有 libLLVM/libclang-cpp。
证据：A/snapshot-clang-dynamic.txt、snapshot-accel-dynamic.txt、workspace-clang-dynamic.txt、
bolt-input-dynamic.txt。这里没有把动态薄壳自身未见 BOLT 标记等同于检查过其所有共享库。

两个 ELF 的 `readelf -lW` 原始摘录：

```text
# snapshot-clang
      [Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]
# snapshot-accel
      [Requesting program interpreter: /emul/usr/lib64/ld-linux-x86-64.so.2]
```

逐字节比较结果：**不相同**，cmp 退出 1：

```text
/home/linhao/Toolchain/development/llvm-optimize/temp/spec-review-20260921/unpacked/snapshot-clang/usr/bin/clang-22 /home/linhao/Toolchain/development/llvm-optimize/temp/spec-review-20260921/unpacked/snapshot-accel/emul/usr/bin/clang-22 differ: byte 57, line 1
```

这是**同一个固定快照的两个包**之间的实测；完整最初依赖包清单未取到，不能仅凭包版本
相同就进一步声称已证明 accel 构建恰好消费了该 RPM 的每一字节、且只做了一种转换。

### 3.3 门禁结果与恢复条件

`SNAPSHOT_LLVM_SHAPE_MATCH=NO`，`STATUS=BLOCKED_BY_DYNAMIC_ACCEL`。
按用户要求停止后续工作。原脚本的 ARCH_MISMATCH/NEEDED 等风险仍存在，**本轮没有把
旧脚本用于检查或执行这些快照二进制**；使用独立的只读 readelf 命令获得上述证据。

恢复前须有明确的下一步决定。若继续以固定快照作为生效准入条件，需要包含自研静态
LLVM 的 OBS 构建、重新生成的 qemu-accel/Base 快照，并验证：

1. x86_64 LLVM RPM 和 accel 的源配方确认为自研 source/spec/patch，最终 NEEDED 均不含
   libLLVM/libclang-cpp；在平台上允许的其他动态运行库不算这项失败。
2. qemu-accel 输入、转换过程、输出分别有可追踪哈希，不要求跨 patchelf 的 SHA 相同。
3. worker 上实际 `/emul/usr/bin/clang-22` 与新 accel 发布清单匹配，并完成必做 exec trace。

本轮没有把 spec 提交到 OBS、没有改快照 URL，也没有替换工具链；不能代用户自行越过
“动态形态即停下”的决定。若决定在新快照到位前先完成离线设计/脚本，需要明确解除或
缩小这个停止条件，不能把耗时经过视为授权。

## 4. 已采纳的 PM 决策与后续设计约束

以下是修订依据登记，**不是已实施/已验证的方案**：

- **保留 reloc 只走单 clang 重链重放。** 在原 `%build` 主 ninja 成功后，从
  `ninja -t commands clang` 取得最终链接命令，保留 rsp/cwd/ThinLTO 参数，只追加
  `-Wl,--emit-relocs` 并改独立输出。重链放入可失败隔离阶段；失败产普通包。
  不再使用全局 CMAKE_EXE_LINKER_FLAGS 路径。`_toolchain` 未定义时，build 开始即跳过
  BOLT 并记录 manifest。此前热缓存实测 227.656 秒、lld VmHWM 9.760868 GiB 仅作参考，
  不是新的配置容量认证。
- **第一版不改 CLANG_VENDOR、不改 LLVM_VERSION_SUFFIX。** 身份使用独立 Release、
  可信多阶段 hash 清单、BOLT 节区、实际 worker 路径，保留普通/BOLT 对照的同一版本标识。
- **profile 优先独立 noarch RPM。** 不放 Source0，不波及全架构；入队预检选择有/无 BOLT
  的条件依赖集合。首次没有可用 profile 时预期为 `FALLBACK_NO_PROFILE` 普通包。
  生产 profile 的机器、cap、具体插桩输入、训练负载、责任人和更新流程尚未定稿。
  新输入 SHA 必须重新认证；stale 上限与有效覆盖率下限须设可达数值及来源，**不沿用 stale=0**。
- **manifest 不依赖 `%check` 才存在。** 后续放在 `%install` 末尾，或用审定的 `%ghost`
  方式；`%check` 只校验。打包后最终 hash 放外部可信发布清单；不得把 install 时的 SHA
  冒充 brp/patchelf 后的 SHA。跨阶段状态格式、固定路径、候选提升和别名硬链接更新仍待定稿。
- **容量指纹必须重新登记。** 新集成配置不能直接按旧“同构”指纹放行；须一次受限实测后认证。
  原完整 LLVM 的 18 GiB 门禁本轮不动。
- **22 GiB 是一次有界容量试验临时放宽的启动政策。** 先前规则按可用减 4 应为 21 GiB，
  且“低于 24 GiB 拒绝”当时改成了“记录、不拒绝”。不把这次例外当成常规容量规则。
  已测生产用途的纯重写自身为 3.481499 GiB、21.83 秒，不依赖 22 GiB 的插桩试验政策。
- **PGO 的口径更正：** 因开发机容量暂缓；原依据的加法模型已作废；待服务器容量评估后
  重估。PGO 与 BOLT 可叠加，不再把“PGO=NO”作为永久既定决策传递。本轮仍不做 PGO。
- **正确性口径：** 训练 10 + 留出 10，共 20 个 TU 的 BOLT 产物对照全部逐字节相同。
  这不自动覆盖未来 RPM/brp/accel 转换后的新 ELF，仍要重做最终产物门禁。
- **数据口径：** 历史收益数字若再引用，必须写“耗时降低”，逐行标明 RPM 基线或剥离版分母、
  含重链剥离还是纯 BOLT、正式/诊断、训练/留出和噪声门禁状态。本轮不重新整理未完成的
  实验比值，不给外部百分比。139,929,464 与 215,899,856 字节只是剥离方式不同的现存
  文件之差，不能直接当成 RPM 或并发内存需报备的增长。
- **服务器验收要求冻结在测量之前。** A 必须为同 source/spec/patch 的
  `without_clang_bolt`；至少 A1 B1 B2 A2 A3 B3，另有一对 A/A 零对照。冻结配对/停止规则/
  区间算法，明确 build、tee、异步 job 非零时终止该轮；纳入 cpu.stat 的 user+sys 第二口径。
  `CC_EMUL` 必查、首次编译后的非计时 exec trace 必做；编译内存及下游运行资源的数值门槛和
  误差处理还未确定，不能写成已验收。
- **发货硬条件：** docs/13 已知 llvm-static-devel 的 GNU strip 符号索引问题，必须做消费者
  链接验收；不通过则修复后再发货，或从发货集明确剔除该开发包。不能随 BOLT 性能包悄悄带出。

## 5. 22 项评审处置（按严重度）

用户未附原评审的逐条编号；下列 R01–R22 是对本消息要求的合并追踪编号，覆盖全部要求，
不声称与任何一家评审的原编号相同。

**采纳**表示决定/约束已记录；不表示代码已实现。**部分采纳**表示原则接受，但所要求的
定稿、修订、试包或实验被本轮停止门禁暂停。没有否决评审意见；不能把暂停伪装成完成。

| 严重度 | 编号 | 意见 | 处置与理由 |
| --- | --- | --- | --- |
| 阻塞 | R01 | 调查 OBS→qemu-accel→快照→Quickbuild；实测形态与哈希链 | **采纳**：两份同快照 RPM 实测动态，触发停止；patchelf 与 SHA 变化已证；缺 armv7l 完整生成材料明确 UNKNOWN |
| 高 | R02 | 单 clang 重链替代全局 flags；build 位置、_toolchain 前置、隔离失败降级 | **采纳**：第 4 节登记固定方向；未执行重链或修改 spec |
| 高 | R03 | 首版不改 vendor/suffix，多层身份 | **采纳**：第 4 节更正；旧版本字符串不改，后续以 Release/多阶段 hash/节区/worker 识别 |
| 高 | R04 | profile 自举、SHA 绑定/重认证、责任人、可达 stale/覆盖率阈值 | **部分采纳**：不用 stale=0 已采纳；生产输入尚未进入快照，机器/责任人/数值阈值未定稿 |
| 高 | R05 | profile 独立 noarch RPM，入队选择条件依赖 | **采纳**：第 4 节取代 Source0 建议；首次无 profile 产普通包 |
| 高 | R06 | manifest 在 install 生成或 ghost；固定跨阶段状态格式/路径 | **部分采纳**：不依赖 check 生成已采纳；状态文件、实现与跳过 check 负对照暂停 |
| 高 | R07 | 软/硬链接枚举和一并替换；brp 对 BOLT 节区影响试包实测 | **部分采纳**：qemu 的 cp -aL、恢复软链接、fdupes 已记录；新 BOLT 试包检查暂停 |
| 高 | R08 | 集成新容量指纹实测登记；22 GiB 例外准确归档 | **采纳**：第 4 节更正政策；原 18 GiB 门禁字节未改，未擅自放行新配置 |
| 高 | R10 | 收益口径、20 TU、现存文件体积差；逐轮类型与分母 | **采纳**：第 4 节修正，本文不对外给收益百分比；旧报告保留历史，不再当作当前口径 |
| 高 | R11 | A/B 定义、6 轮+AA、停止/区间/CPU口径、CC_EMUL/trace、量化资源红线 | **部分采纳**：固定要求已登记；完整模板、阈值与执行均因形态门禁暂停 |
| 高 | R12 | llvm-static-devel 符号索引缺陷纳入发货硬门禁 | **采纳**：消费者链接通过或剔除开发包，未进行本机链接实验 |
| 高 | R13 | 脚本 ELF Machine 对比 uname，ARCH_MISMATCH 自动禁止执行 | **部分采纳**：接受；脚本未修订；本轮以只读 readelf 替代运行旧脚本，未触发 binfmt |
| 高 | R14 | 脚本 readelf -dW / NEEDED_LLVM_SHARED 正负判定 | **部分采纳**：同等只读调查已做并发现 BLOCKER；尚未合入脚本 |
| 高 | R15 | --expect-bolt present/partial/absent 失配非零 | **部分采纳**：接口与测试待门禁解除，不声称旧脚本已支持 |
| 高 | R16 | RPM 归属仅信息；区分 wrapper 与检查失败 | **部分采纳**：接受；usage/退出码/WRAPPER 分支修订暂停 |
| 高 | R17 | awk/stat 等辅助命令失败传播为 UNKNOWN/exit 2 | **部分采纳**：接受；实现及失败注入测试暂停 |
| 高 | R18 | 输入文件 -x 检查 | **部分采纳**：接受；实现及测试暂停 |
| 高 | R20 | 推送测试代码，覆盖架构和 NEEDED 的正负对照 | **部分采纳**：接受；本轮未新增/提交测试，不能复用旧 15 项测试宣称覆盖新增要求 |
| 中 | R09 | PGO 暂缓原因与可叠加口径 | **采纳**：废除加法模型依据，待服务器容量评估重估；非永久 NO |
| 中 | R19 | usage 注明 timeout 可选 | **部分采纳**：接受；本轮停止前没有修改脚本 |
| 中 | R21 | 同 RPM 基线两名字的完整 A/A 零对照 | **部分采纳**：实验授权接受；因动态形态门禁 **NOT RUN**，没有新噪声值 |
| 中 | R22 | RPM/relocs-only/stripped 同轮交错，4 GiB AS 限制与诊断标注 | **部分采纳**：实验授权接受；因门禁 **NOT RUN**，未尝试未剥离 ELF 的 AS 容量 |

合计：采纳 8 项、部分采纳 14 项、未采纳 0 项。部分采纳不是拒绝原则，原因均是本轮
更高优先级的“动态形态停下报告”。

## 6. 实验附录与未完成项

| 实验 | 实际状态 | 3% 门禁 | 新 JSON |
| --- | --- | --- | --- |
| A/A 零对照 | NOT RUN_STOP_GATE | 未测，不写 PASS/FAIL | 无 |
| relocs-only / RPM / stripped 交错 | NOT RUN_STOP_GATE | 未测，不写 PASS/FAIL | 无 |

本轮没有创建伪空基准结果，`temp/bench_results/` 没有本任务新实验数据。
也没有通过当前动态 accel 的样本替代静态基准台对象。身份脚本仍是上一轮版本：

```text
tools/verify_toolchain_identity.sh
SHA256 4016af69657f81aa12c4f5fb44f2f3b67c02f133b5b06124d1e015fe4bdc8b4a
```

所以 `/emul/usr` 的**未来修订版**用法应为
`verify_toolchain_identity.sh /emul/usr --expect-bolt present`，但旧版尚不支持
`--expect-bolt`，不得复制此命令当成当前可执行验收流程。本轮没有满足第三部分脚本交付，
没有把未执行的新增测试标 PASS。

## 7. 原始输出、保护文件与提交自检

原始材料统一在：
`/home/linhao/Toolchain/development/llvm-optimize/temp/spec-review-20260921/`。

| 文件 | 内容 |
| --- | --- |
| downloads.jsonl、snapshot-index.html、repos-index.html、standard-index.html、source-index.html | URL、HTTP 状态、索引、下载 hash、失败原因 |
| package-metadata.json、downloaded-rpms.json、rpm-metadata.txt | 固定快照 primary 条目、两份下载匹配、VCS/NEVRA |
| rpms/、source-rpm/、unpacked/ | 原始 RPM/SRPM、实际生成 spec、两个独立 ELF 解包目录；不提交 |
| source-rpm-list.txt、source-rpm-extract.txt、qemu-spec.txt、qemu-processing.txt | SRPM 文件清单、全部 spec 行号及关键摘录 |
| qemu-git-remote.txt、qemu-git-public.txt | 获取同 VCS 全源码失败的原始输出；cgit TLS 失败在 downloads.jsonl |
| binary-inspection.json、binary-investigation.txt | 四份已存在/下载 ELF 的完整只读检查结果 |
| snapshot-clang-*、snapshot-accel-*、workspace-clang-*、bolt-input-* | 各自 file/header/dynamic/sections/segments/notes 原始输出 |
| snapshot-byte-compare.txt | cmp 原始输出与退出 1 |
| commands.jsonl、audit.py、fetch_packages.py、inspect_rpms.py | 本轮调查命令及仅用于本次审计的脚本，不是交付的身份脚本 |
| initial-state.txt、preservation.json | 起始状态与保护文件未改证明 |
| publication.log、publication-verification.json | GitHub push、远端提交号与 raw 内容校验；提交后写入 temp |

自检：

1. **停止条件是否触发并遵守？是。** 动态 LLVM NEEDED 实测后停止设计定稿、脚本和实验。
2. **是否修改 docs/18？否。** SHA256 保持
   `6ddf174ba42133b4a877fe1355030c66371e0a6961f2472e198d288c040639dd`。
3. **是否修改 spec、LLVM 源码、GBS URL 或完整构建容量门禁？否。**
   A/preservation.json 逐项 hash 与起始相同；源码树仍只有此前三处并发差异。
4. **是否执行 LLVM/Chromium 构建、PGO、BOLT、基准实验？否。** 只下载、解包、查询与读文件。
5. **是否向 Gerrit 推送？否。** 仅尝试公共源码只读访问；本轮报告只推 GitHub main。
6. **是否把源码调查缺口和未完成工作写清？是。** armv7l 完整生成材料/隐式后处理 UNKNOWN；
   脚本和两项实验 NOT RUN；本报告不冒充已完成的完整集成设计。
7. **本轮实际交付是什么？** 仅本报告；完成回复给本文件 raw 与固定提交链接。
