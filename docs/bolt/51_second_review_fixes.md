# 第二轮外部评审修复与轻量复核

三个提交的修复、轻量检查和两次 CMake 入口演练全部通过，可以送审；本轮没有运行完整构建。未知项目参数按用户裁决丢弃并提示人工评审，Toolchain 和 Base-Dev 的真实参数均没有产生 warning。评审包已刷新，三个源码提交仅保留在本地，新产物的一致性仍需后续完整构建验证。

## 1. 范围、提交与裁决

源码独立树：`W/temp/review-20261102/source`，detached HEAD。W 为 `/home/linhao/Toolchain/development/llvm-optimize`。不改 PGO 工作区或 debuglink 历史源码树；未推 Gerrit/sandbox、未创建任务分支、未删除历史目录。

| 所属提交 | 上轮提交 | 本轮提交 | Change-Id |
|---|---|---|---|
| 混合链接 | 38477c9b | d4d6ca16b55a9afcb64a30ebf634f340f968267b | I28171720d5bbbf9eaf491cdafc0aee0b43f9cd06 |
| BOLT | 5aff6c0c | f2553114b05cbb022ff3ac062dbac284e1029df4 | Ic98eab90cc017f127a66e1729b44fab8b8e8fb41 |
| 固定参数/转换器 | a379c766 | 9e39fa8a61392652bb28b75fc26216675bcad1d5 | Ic76505ddb122f1e06271ff7462e24eceee4d400a |

父链从 `67619ec8` 起恰为三层，作者与提交者均为 Hao Lin <hao.lin@samsung.com>，保留各自 Signed-off-by。完整身份见 [commits.json](../../tools/bolt/results/second-review-20261104/commits.json)。发布 profile、OPTIONS、工具白名单及其余大写生产常量均未变化：[unchanged-constants.json](../../tools/bolt/results/second-review-20261104/unchanged-constants.json)。

采纳来源以用户提供的第二轮评审条目为准；未提供评审者署名的条目不猜具体作者。转换器八项夹具由用户补充确认为 Claude Code 第三部分 C-2。用户随后覆盖原第 8、9 条：未知项目参数与非认证 debug 序列只 warning；非法 release 值、`-march=native`、`-mtune=native` 仍失败。

## 2. 逐项修复与轻量结果

| 问题/来源 | 实现与边界 | 测试/证据 |
|---|---|---|
| 混合链接 NEEDED 误放行；评审第 1 条 | readelf、grep 均 LC_ALL=C；grep 从 here-document 读取；0 拒绝共享 LLVM，1 通过，其余失败；readelf 失败带 FAILED 标记 | grep 2/127、readelf 非零均拒绝，无 OK 标记 |
| 五个上游静态工具未检查；第 2 条 | 存在则执行同一门禁，不存在逐个 SKIP；三个发布驱动仍必须存在 | llvm-config 引入 libLLVM 拒绝；五个缺失工具逐个 SKIP |
| readelf BuildRequires 说明；第 3 条 | 注释放在同一依赖声明组已有空行，明确 binutils-devel 还供应 readelf | 避免新增空行改变 ARM 展开；两架构逐字节比较 |
| 取消信号在纯 Python/尾部被吞；第 4 条 | digest、inventory、解压循环检查；main 返回前检查；run_step 写成功标记前检查；不在 install 的三个 rename 之间插检查 | 纯 Python 真 SIGTERM、尾部取消无成功标记、循环负例 |
| SIGINT/第二信号；第 4 条 | SIGINT 与 TERM/HUP 共用处理；第一信号清理组，第二信号先 kill 活跃组再恢复默认处理并向自身发信号；组回收后清除 PGID | SIGINT 创建后/清理中两代进程退出；双 TERM 返回 -15，无活后代 |
| 取消被诊断成磁盘；第 4 条 | CANCELLED/TIMEOUT/COMMAND_ERROR 分开；CANCELLED 跳过 disk-diagnose | 前缀与跳过诊断夹具；48§5 六探针期望更新 |
| 维护注释；第 5 条 | 14400 秒依据：本地工具 108–157 秒、QB 包 13792 秒；LC_ALL 仅 ninja；rpath_layout 前置最多一个路径标签 | 注释不扩大发布参数/门禁 |
| IFS/shell 状态；第 6 条 | 保存 IFS 是否存在和原值，unset 后分词，准确恢复；恢复原 glob 选项 | sh/dash × 默认/未设/冒号/换行；同时验证初始 set -f 与 `$-` |
| release 值；第 7 条 | 仅 0/1，其他 FAILED，三次调用均 `|| exit 1` | 空、2、yes 均失败 |
| 项目参数门禁；第 8 条及用户覆盖 | 四个 expected dropped 仅审计；其他未知 token 丢弃，三组汇总 warning 在 stdout/stderr 各一次；native CPU 仍失败 | fcf-protection、z,now、mno-avx、gsplit、空允许清单：rc=0、丢弃且警告；native 两项失败 |
| debug 序列；第 9 条及用户覆盖 | 认证序列 `-g2 -gdwarf-4 -g`；非认证序列 debug 模式 warning 后继续，release 不检查 | C/CXX 缺末尾 g 和 DWARF5 用例；正常 T/D 无 warning |
| Source1005 模式契约；Claude C-2 | 必填 --debug-info yes/no；每个转换成员 recorded command 与模式一致；未知 token 仍拒绝；只对转换后的 release 成员断言无调试节 | §3 census 与八项夹具 |
| 原生成员；第 10 条 | 原样保留，不按 release 模式检查原有调试节；summary 统计 native_members_preserved | 含调试节原生成员 release 下保留、字节不变 |
| 链接参数说明；第 11–13 条 | LDFLAGS 影响 MODULE 初始化；EXE/SHARED 仍 spec 显式给出；提交说明解释原加固取向和历史 SHA 证据边界 | JSON 标注 LDFLAGS “日志中只有一次赋值，按原值推定” |

显式 helper 全套：**393 项 = 原 378 + 新 15，全部通过**。原测试中两处 COMMAND_FAILED 断言改为 COMMAND_ERROR 前缀；六个取消探针改用 CANCELLED 期望，清理期用命令错误先触发清理，再发送首个取消信号；二次信号独立测试，避免把“首个取消”和“立即终止”混为一谈。

原文：[helper-certified.stderr](../../tools/bolt/results/second-review-20261104/helper-certified.stderr)、[helper-certified.stdout](../../tools/bolt/results/second-review-20261104/helper-certified.stdout)。执行入口显式指向 source/packaging/clang-bolt-helper.py；CMake 为 48 号记录的 host-tools 包装器，只在宿主临时测试目录运行小配置。PATH、版本、SHA 见 [test-invocation-certified.json](../../tools/bolt/results/second-review-20261104/test-invocation-certified.json)。

参数/转换器测试 **42 项 = 原转换器 24 + 新 18，全部通过**；单个测试内部覆盖 sh/dash 与多组参数矩阵，不把 subTest 数虚报成独立测试数。[policy-delivery.stderr](../../tools/bolt/results/second-review-20261104/policy-delivery.stderr)、[逐次输入/输出](../../tools/bolt/results/second-review-20261104/policy-observed.json)、[显式导入路径与SHA](../../tools/bolt/results/second-review-20261104/policy-delivery.stdout)。另有 §3 两个真实工具合成 bitcode 案例。

## 3. full-20261030 census 与 Claude C-2

只读遍历 `build/native-archive-conversion/members/**/ir-settings.json`，逐个记录路径、SHA 与 recorded_command 中的 `-g` token：**3853/3853 带调试参数，0 个不带**。据此实施 --debug-info 检查。逐成员清单：[debug-census.json](../../tools/bolt/results/second-review-20261104/debug-census.json)。

| C-2 | 输入与判据 | 结果 |
|---|---|---|
| 1 | 选用该 census 的真实 recorded command，yes；后端含 -g/-gdwarf-4 | PASS |
| 2 | 同一命令去除全部 -g token，yes；expected debug, found release | PASS |
| 3 | 无 -g 命令，no；后端不含 -g | PASS |
| 4 | 有 -g 命令，no；expected release, found debug | PASS |
| 5 | 本轮演练根 clang + Base-Dev 固定 release 参数，合成小 bitcode；真实转换后调试节为空 | PASS，合成真实工具实测 |
| 6 | 合成模块保留 !llvm.dbg.cu，但 recorded command 声明 release；转换输出带 debug 时拒绝 | PASS，合成真实工具实测 |
| 7 | QB1214821 原失败参数含 -feliminate-unused-debug-types | PASS，仍拒绝 |
| 8 | 缺 --debug-info | PASS，argparse rc=2 |

1、2 原文：[real-recorded-command.json](../../tools/bolt/results/second-review-20261104/real-recorded-command.json)。第 5、6 条是用户授权的合成夹具，不是完整 Base-Dev release 包产物；完整构建后仍须用真实成员再补测。原始 QB 日志只给出 CFLAGS，不声称它是一条完整 per-object Ninja 命令。

合成实测原文：`CLAUDE_C2_SYNTHETIC_RELEASE_PASS 2/2`，正例 `debug_members: 0`；反例 `release conversion unexpectedly emitted debug sections`。见 [实测结果](../../tools/bolt/results/second-review-20261104/synthetic-retry04/real-release-fixture.json)、[stdout](../../tools/bolt/results/second-review-20261104/real-release-fixture-retry04.stdout)。

直接 loader 启动会让 clang 根据 `/proc/self/exe` 把 loader 写进 recorded command，`--argv0` 也未消除它；转换器按原白名单拒绝。最终只对新临时工具副本设置 PT_INTERP 指向本轮 loader，并用局部 LD_LIBRARY_PATH 启动；复制前后 `.text` SHA 完全相同（[证据](../../tools/bolt/results/second-review-20261104/synthetic-retry04/private-tool-text-identity.json)），原工具未改。宿主没有 patchelf，另一次准备失败也保留；最终使用本轮新根里的 patchelf。所有记录、输入、输出保留在 synthetic-release* 新目录，没有为通过测试登记 loader 或新的未知 token。

warning 仅改变项目参数处理的决策，不放宽 Source1005 的后续认证：有调试参数的成员仍要求最后一个 DWARF 参数为 -gdwarf-4。非认证 debug 序列能继续经过参数函数，不代表后续任一门禁都必然通过。

## 4. 展开、导出、常量

最终提交 gbs export 成功；上游至本次仍生成 Patch0–7。两种 build.conf 保留固定 SHA（Toolchain e5187fd7…；Base-Dev 8ace286a…）。每种配置 x86 debug/release 各 ON/OFF，加 armv7l/aarch64，共 12 个完整展开比较；ARM 全文与 `5aff6c0c` 字节相同。x86 差异限定在参数函数、混合链接断言、两处 ninja-only 注释及显式 --debug-info 参数；逐条 diff 保留，未忽略一般空行。

原文：`EXPANSIONS_PASS 12 FIVE_PARSE_PASS 5`，见 [parse-ruling.stdout](../../tools/bolt/results/second-review-20261104/parse-ruling.stdout)。[展开汇总](../../tools/bolt/results/second-review-20261104/parse-ruling/expansion-summary.json)、[五项解析](../../tools/bolt/results/second-review-20261104/parse-ruling/five-summary.json)；完整展开、diff、argv、stderr 位于相同目录。Tizen RPM 4.14.1.1 的 ON/OFF/一行回退/armv7l/aarch64 全通过。没有运行 `%prep` 或包构建来冒充解析；五项使用 `rpmbuild -bp --nodeps --nobuild`。

## 5. 两个新根启动演练

入口沿用 dca920a8 的 gbs-driver 布局及 docs50 已修好的日志重写检测，复制到 `tools/bolt/second-review-launch-20261104/`，只使用本轮源码与新根。该入口只允许 rehearsal/rehearsal-02，禁止 full。根为 `W/temp/second-review-20261104/{toolchain,basedev}-rehearsal`。配置与上轮完全相同：固定 Toolchain/ Base-Dev 快照、jobs8 / _smp_mflags-j8 / _costomized_smp_mflags-j20，外层 threads30。

systemd MemoryMax=MemTotal−8GiB，swap=0，CPUQuota=1200%，nice10，ionice2/7；这些设置仅在本地入口，不进发布代码。监测到实际 `+ cmake -G Ninja` 即正常停止，禁止运行 Ninja。两次串行；保留全部根和日志。

两个入口均一次演练通过。实际命令（在证据仓库执行）：

```sh
/bin/sh tools/bolt/second-review-launch-20261104/launch.sh toolchain rehearsal
/bin/sh tools/bolt/second-review-launch-20261104/launch.sh basedev rehearsal
```

| 项目 | CMake 入口日志秒数 | 整轮演练耗时，含导出/准备/清理 | 结果 |
|---|---:|---:|---|
| Toolchain | 377 | 599.910 秒 | PASS；DROPPED 空，warning 0 |
| Base-Dev | 372 | 943.582 秒 | PASS；DROPPED 恰为四个预期 token，warning 0 |

实际参数原文（去掉日志时间前缀后内容不变）：

**Toolchain**（原始日志行号见审计 JSON）

```text
[  377s] TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] CXXFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] LDFLAGS=[]
[  377s] TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[] CXXFLAGS=[] LDFLAGS=[]
CMAKE_C_FLAGS=[ -ffunction-sections -fdata-sections  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument   -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables  -g -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument]
CMAKE_CXX_FLAGS=[ -ffunction-sections -fdata-sections  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument   -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables  -g -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument]
CMAKE_EXE_LINKER_FLAGS=[-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections]
CMAKE_SHARED_LINKER_FLAGS=[-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections]
LDFLAGS=[-Wl,-z,relro,--as-needed -Wl,--gc-sections]
```

**Base-Dev**（原始日志行号见审计 JSON）

```text
[  372s] TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] CXXFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] LDFLAGS=[]
[  372s] TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] CXXFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] LDFLAGS=[]
CMAKE_C_FLAGS=[ -ffunction-sections -fdata-sections  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument    -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables   -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument]
CMAKE_CXX_FLAGS=[ -ffunction-sections -fdata-sections  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument    -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables   -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument]
CMAKE_EXE_LINKER_FLAGS=[-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections]
CMAKE_SHARED_LINKER_FLAGS=[-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections]
LDFLAGS=[-Wl,-z,relro,--as-needed -Wl,--gc-sections]
```

Toolchain C/CXX/LDFLAGS 与 QB1215143 认证字符串逐字相同；Base-Dev C/CXX 使用固定 release 参数及其架构参数，LDFLAGS 为固定值。EXE/SHARED 的显式链接参数未变。演练没有执行 Ninja，没有生成新的 LLVM 包。

完整 argv 和行号：[T 审计](../../tools/bolt/results/second-review-20261104/toolchain-rehearsal-audit.json)、[D 审计](../../tools/bolt/results/second-review-20261104/basedev-rehearsal-audit.json)。原始日志和控制器输出：[T evidence](../../tools/bolt/results/second-review-20261104/rehearsals/toolchain/evidence/)、[D evidence](../../tools/bolt/results/second-review-20261104/rehearsals/basedev/evidence/)。控制器结束行均为 `FINAL_PROJECT_FLAGS 已结束 ... status=ok reason=rehearsal-complete-at-CMake`。

正常卸载本次根的 proc/devpts/shm，未使用强制/懒卸载；源码仍 clean detached。两套 controller/prep/build 服务全部 inactive/dead、Result=success；根内残留进程和挂载均为空：[T final-audit](../../tools/bolt/results/second-review-20261104/rehearsals/toolchain/evidence/final-audit.json)、[D final-audit](../../tools/bolt/results/second-review-20261104/rehearsals/basedev/evidence/final-audit.json)、[最终服务检查](../../tools/bolt/results/second-review-20261104/rehearsals-final-summary.json)。

演练后 /home 可用 158,030,852,096 字节（147.178 GiB），只是现场记录，不据此宣布两轮完整构建有足够空间；本轮没有授权完整构建，之后启动仍须重新核对空间。两个新根全部保留。


## 6. 不采纳/仍挂账

| 评审建议/缺口 | 本轮处理与理由 |
|---|---|
| debugfiles 路径由 spec 传入 | 不采纳；维持已认证的平台路径约定，当前任务不改此接口；已有存在性和内容门禁。平台约定若改变需另行修复认证 |
| release 原样保留成员必须无调试节 | 不采纳；这些成员不是本转换器新生成，检查会误拒绝原有原生归档；只记录数量并保持内容 |
| 关闭 BOLT 的完整构建 | 本轮不做；用户限定轻量/演练。完整展开逐字比较不能替代完整构建，保留此验证缺口 |
| 67619ec8 基线缺口 | 不用来源不同的 RPM 冒充该提交新构建；保持旧证据来源和缺口，需后续独立认证 |
| release 真实成员复测 | 合成 C-2 #5/#6 仅验证机制；Base-Dev 完整构建后应替换为真实成员再测 |

## 7. 过程修正与证据保全

- 初次 amend 未 stage 工作文件，随后的 cherry-pick 被 Git 拒绝，未覆盖文件；随后将各自文件 stage/amend。临时 checkpoint 只用于把后续取消修正归回 BOLT 父提交；最终链只有三个提交，未建立新分支。
- 首轮取消测试保留原文：清理期信号最初仍带 COMMAND_ERROR，已改为 CANCELLED；旧 rc7 断言随前缀规范调整。探针的空心跳就绪竞态改为等待两级非空心跳，再触发清理。
- 注释条件块导致展开多三个空行，初次检查拒绝；注释最终占用依赖声明组原有空行，保留 ARM 字节身份。曾用独立临时 spec 验证尾行注释不可用，RPM 报 Dependency tokens 错误，未用于发布版本。
- 有一次解析先于异步 export 完成，文件尚不存在；保留错误原文，等待导出完成后重跑最终矩阵。没有因此放宽产品门禁。
- 用户中途补充 C-2 原文及参数 warning 裁决；旧的 FAIL 策略测试输出保留为历史迭代，最终以 ruling 命名输出和最终提交为准。

本轮所有原始证据在 [second-review-20261104](../../tools/bolt/results/second-review-20261104/)，评审包见 [README](../../patches/review-20261104/README.md)。

## 8. 交付核对

- 三个 format-patch 独立顺序应用到 67619ec8 的临时 Git index，得到 tree `cbc33271f8a9a7a5bd4de3c806bed6182c268e98`，与最终源码相同：[review-apply.json](../../tools/bolt/results/second-review-20261104/review-apply.json)。
- 材料含完整补丁、BOLT 纯文本 diff（仅排除 profile 二进制）、三个完整提交说明、相对 a379c766 的增量、spec/helper/转换器/六个 CMake 文件以及 SHA256SUMS。旧包未改。
- 大型 GBS 源码/模型归档保留在本地；发布最终导出 spec、文件 SHA 清单和全部检查输出，不重复上传多套源码归档。演练超过 1 MiB 的文本压缩为 gzip；复制清单记录原文 SHA 与发布文件 SHA。
- 只提交并推送证据仓库 GitHub bolt-v4；三个源码提交未推送 Gerrit/sandbox，未操作 QB，未触碰 PGO 现场。

最终结论：**可以送审**。轻量检查和两个启动演练全部通过；完整构建、RPM/90TU 新产物认证仍未运行。


## 9. sandbox 更新与磁盘清单（2026-11-03，推送前停止）

本次用户已授权把三个提交推送到 Gerrit 的 sandbox/lhmax2025/bolt_pgo，但指定源码克隆的 origin 实际指向本机另一份源码仓库。按“任一推送前核对不符即停止”执行：**未运行 push，未修改 remote 配置，未继续磁盘盘点**。前述轻量验证结论不变。

### 9.1 只读核对

| 项目 | 结果 |
|---|---|
| `git status --porcelain=v1 --untracked-files=all` | rc=0，输出为空；工作区干净 |
| HEAD | 9e39fa8a61392652bb28b75fc26216675bcad1d5，PASS |
| 三层父链 | 9e39fa8a → f2553114 → d4d6ca16 → 67619ec8，PASS |
| 三个作者、提交者、Signed-off-by | 均 Hao Lin <hao.lin@samsung.com>，PASS |
| 三个 Change-Id | 与本文第1节逐个相同，PASS |
| origin 目标 | 本地路径，不是 Gerrit，停止 |
| origin 的指定 sandbox 引用 | ls-remote rc=0，输出为空，无法满足预期3ee2d847 |

`git remote -v` 原文：

```text
origin	/home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-tb20261026/source (fetch)
origin	/home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-tb20261026/source (push)
```

执行的查询：

```sh
git ls-remote origin refs/heads/sandbox/lhmax2025/bolt_pgo
```

stdout、stderr 均为空，退出码0。这里查到的是 **origin 所指的本地仓库**，不能据此说 Gerrit 分支不存在或 SHA 已变化。本轮未直接查询 Gerrit，Gerrit 当前 SHA 标为 UNKNOWN，也没有“推后 SHA”。43号§14记录的是另一份源码工作区的 Gerrit origin，不适用于当前这个独立克隆。

指定 push 命令未执行，因此没有伪造的推送返回原文。没有向本地旧源码仓库写引用，没有改任何源码或 Git remote 配置，也没有改用其他推送方式。

### 9.2 磁盘清单状态

磁盘盘点、三组目录总量、两轮完整构建所需空间及缺口均 **NOT RUN**：本任务要求推送前任一项不符合即停止。未使用旧盘点数字冒充当前值，未删除或移动文件。需先明确当前克隆的 Gerrit origin 设置后，才可按同一指定租约命令续跑，并继续本次只读盘点。

全部原始核对记录：[preflight.json](../../tools/bolt/results/second-review-20261104/sandbox-update-20261103/preflight.json)，同目录包含工作区、三份提交身份、remote 与 ls-remote 的 stdout/stderr。

本轮结论：**推送前目标核对未通过，sandbox 未更新，磁盘盘点未执行；仅发布停止记录。**
