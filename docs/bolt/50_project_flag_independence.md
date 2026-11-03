# 50：x86_64 固定项目参数与 release 静态库转换

本轮停在轻量测试，没有启动 Toolchain 或 Base-Dev 的演练、完整构建。
固定参数实现已保存为新的 detached 提交，Toolchain 的独立 shell 冒烟输出与 QB 1215143 的三个参数字符串逐字节相同；但这不代表展开或产物验证通过。
显式 helper 的 378 项测试有 12 项因测试 PATH 缺少 cmake 报错，按“任一轻量检查不通过即停”的要求，未重跑或继续后续步骤。

## 1. 提交和隔离

- 新本地提交：`a379c766e17d12ba7738ff6079adb39645c0a740`；tree `37c8c6d3f249b5948db1517d84a79a4d53c9a112`。
- 父提交仍是 `5aff6c0c3ab663872cf997a13bb9242bac474092`，其父 hybrid `38477c9b6e1401e5e1fe01fafa282ab92cf53887` 未改。
- 新 Change-Id：`Ic76505ddb122f1e06271ff7462e24eceee4d400a`；作者、提交者和 Signed-off-by 均 Hao Lin <hao.lin@samsung.com>，使用单次 git -c 指定。
- 只改新提交的 `packaging/llvm.spec` 和 `packaging/llvm-static-archives-native.py`，helper/profile/OPTIONS/白名单没有改。工作区提交后干净，仍为 detached HEAD，没有新建分支。
- 源码位置 `W/temp/review-20261102/source`；本轮目录 `W/temp/final-20261103`。未触碰 PGO 的源码和试验目录；未在任何历史构建根运行 cmake/ninja，没有完整构建、挂载、目录删除、Gerrit/sandbox 推送或 QB 操作。
- **该提交未获得完整构建资格。** 新增夹具、转换器既有测试、导出、展开/解析及所有构建验证尚未完成，不能使用此提交直接启动今晚构建。

## 2. 用户补充裁决与参数处理

用户确认：既有规范化不计入 DROPPED；另打印 NORMALIZED。所有移除按完整 token 匹配，不能把 `-fstack-protector-strong` 变成 `-strong`。

实现将 x86_64 旧 sed 子串替换段替换成可独立运行的 POSIX sh 函数 `tizen_llvm_flags`；片段位于 `# BEGIN/END TIZEN_LLVM_FIXED_FLAGS`，其副本 `flags.sh` 只用于本轮轻量核对。spec 里的 printf 百分号按 RPM 语法写成双百分号。没有把本地资源规则写入发布代码。

| 分类 | 规则 |
|---|---|
| 固定行为参数 | 不从项目值拼接；采用下表 QB 已生效的固定序列，保留顺序、重复项和空白 |
| 架构 | 项目中的完整 `-m64`、`-march=*`、`-mtune=*`、`-msse*`、`-mfpmath=*` 保留，保持顺序 |
| 调试 | debug 保留输入的调试 token 顺序；release 沿用已有去调试逻辑，函数本身也不输出调试 token |
| NORMALIZED | 完整优化级别 token（-O0/-O1/-O2/-O3/-Os/-Oz/-Og/-Ofast）、三种 stack-protector、-momit-leaf-frame-pointer、-fno-omit-frame-pointer |
| DROPPED | 既非已规范化项、架构/调试项，也不是对应固定参数集内 token 的其余输入；尤其不接受 -fno-inline-functions、-feliminate-unused-debug-types、--param=ssp-buffer-size=4 |
| LDFLAGS | 固定 Toolchain 的两项链接参数；架构/模式选项单独保留；不继承任意项目链接参数 |

### 2.1 每项固定参数的来源

A-X 为 [49号](49_qb_1215143_1214821.md) 的 QB1215143 x86日志，原始参数在L391/393/395，生效参数在L426–429，CMake在L438。本地 full-20261030 配置命令、行号保存在 `local-configure.json`。

| 固定 token（顺序见全文证据） | QB 来源 | 本地配置对应 |
|---|---|---|
| -ffunction-sections、-fdata-sections | A-X:L426/428/438 | 本地 C/CXXFLAGS 字符串无这两项；显式链接 flags 有，详见下方差异 |
| -Wno-unused-command-line-argument（两次） | A-X:L426/428 | 同样两次 |
| -Wno-error=unused-but-set-variable | A-X:L426/428 | 相同 |
| -Wno-error=unused-command-line-argument | A-X:L426/428 | 相同 |
| -pipe、-Wall | A-X:L426/428 | 相同 |
| -Wp,-D_FORTIFY_SOURCE=2 | A-X:L426/428 | 相同 |
| -fexceptions | A-X:L426/428 | 相同 |
| -Wformat、-Wformat-security | A-X:L426/428 | 相同 |
| -fmessage-length=0 | A-X:L426/428 | 相同 |
| -frecord-gcc-switches | A-X:L426/428 | 相同 |
| -fdiagnostics-color=never | A-X:L426/428 | 相同 |
| -fasynchronous-unwind-tables | A-X:L426/428 | 相同 |
| -O3、-flto=thin、-fomit-frame-pointer | A-X:L426/428 | 相同 |
| LDFLAGS: -Wl,-z,relro,--as-needed、-Wl,--gc-sections | A-X:L395 | 采用QB完整字符串；原CMake显式linker flags不改 |

架构实例 `-m64 -march=nehalem -msse4.2 -mfpmath=sse`、调试实例 `-g2 -gdwarf-4 … -g` 取自项目，不归入固定行为列表。

两份来源**并非原始字符串完全一致**：QB 显式多了 `-ffunction-sections -fdata-sections`，本地开头为空白。最初来源审计错误地断言二者完全一致，得到 AssertionError；随后只读展开差异、保留两份原文，不再用这个错误前提。按任务明确的“与 QB 1215143 输出逐字节相同”采用 QB 为字符串 oracle。这不是可以宣称 full-20261030 产物必然不变的证据；需要后续身份链、RPM 和 90 TU 实测。

### 2.2 已完成的独立冒烟核对

`/bin/sh -n flags.sh` 返回0；将 QB Toolchain 原始 CFLAGS/CXXFLAGS/LDFLAGS 输入片段，三项结果分别与 A-X 的生效值逐字节比较，结果 `[True, True, True]`。原输出：

```text
TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] CXXFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] LDFLAGS=[]
TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[] CXXFLAGS=[] LDFLAGS=[]
```

这只验证 shell 副本的这一组输入，不替代 rpmspec 展开、Base-Dev/截断负例或完整单元测试。其他新增夹具尚未执行，不记 PASS。

## 3. Source1005 的实现范围

- `classify_options`：完全没有 `-g` 类选项时允许 `dwarf=None`；出现任意已接受的调试选项，继续要求最后一个 DWARF 选项是 `-gdwarf-4`。
- `ir_settings`：release 从 backend flags 中去掉 `-g` 和 `-gdwarf-4`；debug 路径的原 flags 保持。
- 转换后的 release ELF 再查 debug sections，如有则失败，不能仅凭没有传 -g 就假定输出无调试信息。
- 未添加任何未知 token 白名单；`-feliminate-unused-debug-types` 仍应拒绝。真实 Base-Dev flags 已存入 `flags-inputs.json`，该负例和 release 对象正例尚待测试。

完整发布改动见 [source-commit.diff](../../tools/bolt/results/final-20261103/source-commit.diff)。本轮没有改工具目录里的转换器镜像；之后须通过显式导入本提交的 Source1005 跑既有测试，避免测到旧副本。

## 4. 停止点：378 项既有 helper 测试未通过

命令与 PATH 见 `test-invocation.json`：

```sh
python3 -B tools/bolt/run_review_tests.py --helper /home/linhao/Toolchain/development/llvm-optimize/temp/review-20261102/source/packaging/clang-bolt-helper.py
```

执行结果：366/378 项通过，12 项 ERROR，退出码1；没有断言失败被隐藏或改成PASS。12项均为缺少 cmake 的 FileNotFoundError。完整 stdout/stderr 原文已保存。

```text
======================================================================
ERROR: test_fini_value_rejected (test_fifth_review.FrozenRunpathTests.test_fini_value_rejected)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/test_fifth_review.py", line 37, in test_fini_value_rejected
    def test_fini_value_rejected(self):self.corrupt(13)
                                       ^^^^^^^^^^^^^^^^
  File "/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/test_fifth_review.py", line 21, in corrupt
    self.setup_elf('$ORIGIN/../lib64:/build/lib64:')
  File "/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/test_runpath_improvements.py", line 18, in setup_elf
    subprocess.run(['cmake','-P',str(script)],check=True,capture_output=True)
  File "/usr/lib/python3.12/subprocess.py", line 548, in run
    with Popen(*popenargs, **kwargs) as process:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/subprocess.py", line 1026, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
  File "/usr/lib/python3.12/subprocess.py", line 1955, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
FileNotFoundError: [Errno 2] No such file or directory: 'cmake'

----------------------------------------------------------------------
Ran 378 tests in 12.257s

FAILED (errors=12)
```

责任与处置：48号 §13 已记录过使用临时 host-tools/cmake 的方式，本轮启动测试时未把该入口加入 PATH，导致重现准备环境错误；这不是新源码已经证实有12处产品缺陷。按本任务“任一轻量检查不通过即停止”的要求，没有更改 PATH 后重跑，也没有进入导出、演练或完整构建。

## 5. 检查/构建状态表

| 项 | 状态 | 证据或原因 |
|---|---|---|
| 起点HEAD/父提交、工作区 | PASS | 原5aff6c0c、父38477c9b，开始干净 |
| 新detached提交、前两个提交不变 | PASS | source-identity.json、source-chain.txt |
| 参数来源采集 | 完成，存在已说明差异 | flags-inputs.json、local-configure.json、configure-source-differences.json |
| POSIX语法/Toolchain独立副本冒烟 | PASS（限定范围） | prototype-smoke-transcript.txt |
| 378 helper测试 | **ERROR，停止** | 12项找不到cmake；未重跑 |
| 新参数/转换器夹具、转换器既有测试 | NOT RUN | 停止后不继续；新增夹具未补齐 |
| GBS export、双配置展开、ARM字节比较、Tizen RPM五项解析 | NOT RUN | 没有绕过轻量门禁 |
| T/D启动入口与真实演练 | NOT RUN | 未创建toolchain/basedev根；未启动systemd构建服务 |
| 保留两根的磁盘准入 | 未执行正式判定 | 仅采集df；不能宣称启动条件全部满足 |
| T完整构建/身份链/23包/90TU | NOT RUN | 未启动 |
| D完整构建/release/90TU/RPM清单 | NOT RUN | 未启动 |
| T/D分阶段资源 | UNKNOWN | 无本轮构建样本，不沿用历史数字 |
| 装包实测 | NOT RUN | 本任务原定不做；新产物身份尚无可比较对象 |

本轮早期 `/home` df 可用为211755806720B。43号历史整根采样峰值68252237824B只能用作后续规划依据，未把它冒充这次的实际峰值，也未开始两个根的空间准入和夜间监控。`monitor.log` 只含本轮停止结束行，没有正在后台构建的任务。

## 6. 交付和恢复位置

- 原始证据：[final-20261103](../../tools/bolt/results/final-20261103/)，含失败原文、输入/来源、完整diff、提交身份和SHA256SUMS。
- 本地现场 `W/temp/final-20261103/` 保留。之后需要先补齐测试环境与新增夹具，再从轻量检查恢复；不能直接启动 T/D。
- 只推 GitHub bolt-v4 的文档与证据；源码新提交未推 Gerrit/sandbox。

**总结论：轻量检查未通过，未进行启动演练或完整构建；两个构建没有“全部通过”的结论。**


## 7. 轻量检查与演练（续）

本次恢复后，378 项 helper 测试、35 项转换器/新增夹具、双配置展开、五项 Tizen RPM 解析和两套入口的最终演练均通过。共三次演练（D重试一次），均在 CMake 入口停止，没有执行 LLVM Ninja，没有运行完整构建。今晚入口已准备；以下结果不代表 23 包、身份链或 90 TU 已通过。

### 7.1 身份、测试环境与夹具

源码仍为 `a379c766e17d12ba7738ff6079adb39645c0a740`，tree `37c8c6d3f249b5948db1517d84a79a4d53c9a112`；父 `5aff6c0c`、祖父 `38477c9b` 均未改，工作区干净。本轮没有修改发布代码或 amend 提交。前文及上一轮失败证据原样保留。

沿用 48 号 §13 的 `W/temp/review-20261103/host-tools/cmake`：该入口以新配置根的 loader、库目录运行其 CMake，测试驱动在本轮目录执行，fixture 使用宿主临时目录；没有进入历史根运行 CMake/Ninja。完整 PATH、入口/实际 ELF/loader 的 SHA 和 argv 见 [test-invocation.json](../../tools/bolt/results/final-20261103/continue/test-invocation.json)。版本原文：

```text
cmake version 3.31.2

CMake suite maintained and supported by Kitware (kitware.com/cmake).
```

| 检查 | 结果 | 原文证据 |
|---|---|---|
| 显式 helper 的既有测试 | 378/378 PASS，`Ran 378 tests` / `OK` | [stderr](../../tools/bolt/results/final-20261103/continue/helper-tests.stderr)、[stdout](../../tools/bolt/results/final-20261103/continue/helper-tests.stdout) |
| 转换器既有测试 | 24/24 PASS | [fixtures.stderr](../../tools/bolt/results/final-20261103/continue/fixtures.stderr) |
| 新参数与 release 夹具 | 11/11 PASS；合计35项 `OK` | [测试脚本](../../tools/bolt/results/final-20261103/continue/test_continuation.py)、[逐输入输出](../../tools/bolt/results/final-20261103/continue/flags-observed.json) |

转换器通过 importlib 显式导入源码提交中的 `packaging/llvm-static-archives-native.py`，注入既有测试使用的模块名；没有导入工具目录里的旧实现。路径和 SHA 原文在 [fixtures.stdout](../../tools/bolt/results/final-20261103/continue/fixtures.stdout)。

新增覆盖：Toolchain CFLAGS/CXXFLAGS/LDFLAGS 与 A-X:L427/L429及L395精确字符串相等；Base-Dev 固定输出、架构、NORMALIZED/DROPPED；strong 完整 token；空输入；重复 token；混合空格/tab/换行。重复架构项按原顺序保留、固定项只按固定列表输出，审计列表保留重复输入。release 无 DWARF 通过、带 -g 时保留原 DWARF 规则、未知 token 拒绝、真实 QB 参数负例拒绝、转换路径中产生含 `.debug_info` ELF 时拒绝。

QB 1214821 日志保留的是原始/生效 CFLAGS，不是完整逐对象 Ninja 命令；负例将日志里的生效 CFLAGS 原文接到 `clang` 后送入分类器，命中 `-feliminate-unused-debug-types` 拒绝。未把重建的 argv 冒充日志中完整命令。[输入来源及行号](../../tools/bolt/results/final-20261103/flags-inputs.json)。

### 7.2 导出、完整展开与解析

GBS export 退出0，[命令/返回码](../../tools/bolt/results/final-20261103/continue/export.json)、[stdout](../../tools/bolt/results/final-20261103/continue/export.stdout)、[导出spec](../../tools/bolt/results/final-20261103/continue/exported.spec)、[文件大小与SHA](../../tools/bolt/results/final-20261103/continue/export-inventory.json)。

使用 Tizen RPM/RPM-build `4.14.1.1-1.7`，通过同一配置根的 loader 和库从宿主临时目录只读调用；没有依赖宿主 RPM 版本。`RPM_CONFIGDIR` 指向 Tizen 目录；去掉宿主/用户宏文件来源，再用 `/usr/lib/build/queryconfig` 从两份固定 build.conf 生成各架构 rawmacros 和 optflags/rpmrc。每次命令、rc、stdout/stderr 均在 [parse](../../tools/bolt/results/final-20261103/continue/parse/) 中保存。debug/release 用显式 `_toolchain` 定义/取消选择，只用于本轮模式矩阵；真实 D 演练不增加 `_toolchain`。

- Toolchain build.conf：`e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945`。
- Base-Dev build.conf：`8ace286a5f98f2e02a79be275a64c22a86ea2b0034174c1e293381e181ce3f6a`。

| 配置 | x86 debug / release | armv7l / aarch64 | BOLT OFF |
|---|---|---|---|
| Toolchain | PASS，唯一diff为参数块 | PASS，与5aff逐字节相同 | PASS，仅参数块变化 |
| Base-Dev | PASS，唯一diff为参数块 | PASS，与5aff逐字节相同 | PASS，仅参数块变化 |

[12组逐字节/限定区间比较](../../tools/bolt/results/final-20261103/continue/parse/expansion-summary.json)，原始全文未去空行。x86每份diff均为“旧sed规范化块→新完整token参数函数、固定参数、NORMALIZED/DROPPED输出”；检查脚本同时断言该块前后**所有字节**相同。48 §15 的 `bc0d58ff` 与5aff的spec blob都是 `7a51be894f830043acbf25e4d822fa1af51d4a06`，因此既有Source/空行/hybrid差异不变，[衔接证据](../../tools/bolt/results/final-20261103/continue/off-section15-baseline.json)。

导出spec的 x86 ON、OFF、一行回退、armv7l、aarch64 五项，`rpmbuild -bp --nodeps --nobuild` 与 `rpmspec -P` 均退出0，各含8个生成补丁声明：[five-summary.json](../../tools/bolt/results/final-20261103/continue/parse/five-summary.json)。这五项命令只做解析/校验，不执行%prep；后续另行执行的启动演练见7.3。

准备性处理：初版比较脚本把旧参数块起点错误定位到中间的 `export CFLAGS`，在执行展开前触发边界 AssertionError。保留 [初版脚本](../../tools/bolt/results/final-20261103/continue/parse_checks.attempt1.py) 和 [错误原文](../../tools/bolt/results/final-20261103/continue/parse.attempt1.stderr)，改为完整 `%ifarch x86_64` 块边界后通过；没有放宽比较。一次只读查找误用不存在的48号文档文件名，随后 `rg --files docs/bolt` 定位为 `48_review_fixes.md`；不影响产品操作。

### 7.3 两个真实启动演练

[入口](../../tools/bolt/final-launch-20261103/launch.sh) 和 [控制器](../../tools/bolt/final-launch-20261103/launcher.py) 复制自dca920a8布局，[完整差异](../../tools/bolt/results/final-20261103/continue/launcher-final.diff)。沿用physical gbs-root + gbs-driver的BUILD-ROOTS链接、先prep后正常GBS流程。仅本地选择source/config/root/service；D不套用T的固定profile/strip身份监视，发布helper门禁和BOLT失败/磁盘停止监视不变。固定profile键名保留以兼容driver sources目录；实际来源由URL和build.conf决定，不因此把Base-Dev当成Toolchain。

- T：`W/temp/final-20261103/toolchain-rehearsal`，快照 `tizen-base-toolchain_20261013.024319`。
- D：`W/temp/final-20261103/basedev-rehearsal/retry-02`（首轮保留），快照 `tizen-base-dev_20261030.061217`。
- 两者都只启用各自 packages/debug，完整配置副本在 [configs](../../tools/bolt/results/final-20261103/continue/configs/)。
- MemoryMax=24,482,979,840B（本机MemTotal−8GiB），MemorySwapMax=0，CPUQuota=1200%，nice10，ionice2/7。GBS `--threads=30`，三个宏为jobs8、_smp_mflags=-j8、_costomized_smp_mflags=-j20；spec的LLVM编译并行6、链接2不改。
- T首轮通过；D首轮到达CMake并正常停止，但增量日志漏掉%build开始行，使控制器断言失败。修复本地采集器后在全新retry-02重做并通过；没有执行Ninja。平台日志里的 `Terminated`/`failed build` 是主动停止的预期结果，控制器最终按停止原因和清理事实判定PASS，不把它当作完整构建成功。

#### Toolchain 原文与参数

日志 `rehearsals/toolchain/evidence/rpm-build-final.log`：

```text
L633: [  330s] TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] CXXFLAGS=[-Os -fstack-protector -momit-leaf-frame-pointer -fno-omit-frame-pointer] LDFLAGS=[]
L635: [  330s] TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[] CXXFLAGS=[] LDFLAGS=[]
```

CMake命令在L645，参数逐字保存如下（C与C++分别比较，并非只比较token集合）：

```text
CMAKE_C_FLAGS= -ffunction-sections -fdata-sections  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument   -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables  -g -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument
CMAKE_CXX_FLAGS= -ffunction-sections -fdata-sections  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument   -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables  -g -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument
CMAKE_EXE_LINKER_FLAGS=-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections
CMAKE_SHARED_LINKER_FLAGS=-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections
LDFLAGS=-Wl,-z,relro,--as-needed -Wl,--gc-sections
```

LDFLAGS来自CMake执行前导出的环境，不虚构为一个`-D`参数。完整CMake argv、原文行和精确比较：[审计JSON](../../tools/bolt/results/final-20261103/continue/toolchain-rehearsal-audit.json)。

清理原文：[final-audit.json](../../tools/bolt/results/final-20261103/continue/rehearsals/toolchain/evidence/final-audit.json)：`ActiveState=inactive`、`SubState=dead`，mounts stdout为空，`remaining_build_processes=[]`；普通umount命令与返回码单独保存。控制器结束行：

```text
FINAL_PROJECT_FLAGS 已结束 2026-11-03T12:03:50.720693+08:00 status=ok reason=rehearsal-complete-at-CMake
```

#### Base-Dev 原文与参数

日志 `rehearsals/basedev/retry-02/evidence/rpm-build-final.log`：

```text
L601: [  313s] TIZEN_LLVM_NORMALIZED_FLAGS CFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] CXXFLAGS=[-O2 -fstack-protector-strong -fno-omit-frame-pointer] LDFLAGS=[]
L603: [  313s] TIZEN_LLVM_DROPPED_FLAGS CFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] CXXFLAGS=[-fno-inline-functions -Wl,-z,relro,--as-needed -feliminate-unused-debug-types --param=ssp-buffer-size=4] LDFLAGS=[]
```

CMake命令在L613，参数逐字保存如下（C与C++分别比较，并非只比较token集合）：

```text
CMAKE_C_FLAGS= -ffunction-sections -fdata-sections  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument    -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables   -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument
CMAKE_CXX_FLAGS= -ffunction-sections -fdata-sections  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument    -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables   -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument
CMAKE_EXE_LINKER_FLAGS=-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections
CMAKE_SHARED_LINKER_FLAGS=-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections
LDFLAGS=-Wl,-z,relro,--as-needed -Wl,--gc-sections
```

LDFLAGS来自CMake执行前导出的环境，不虚构为一个`-D`参数。完整CMake argv、原文行和精确比较：[审计JSON](../../tools/bolt/results/final-20261103/continue/basedev-rehearsal-audit.json)。

清理原文：[final-audit.json](../../tools/bolt/results/final-20261103/continue/rehearsals/basedev/retry-02/evidence/final-audit.json)：`ActiveState=inactive`、`SubState=dead`，mounts stdout为空，`remaining_build_processes=[]`；普通umount命令与返回码单独保存。控制器结束行：

```text
FINAL_PROJECT_FLAGS 已结束 2026-11-03T12:26:03.880510+08:00 status=ok reason=rehearsal-complete-at-CMake
```

#### Base-Dev首轮采集失败与修复

GBS重写同一个`.build.log`后，旧增量采集器仍沿用prep时的偏移；原始文件有`Executing(%prep)`和`Executing(%build)`，拼接副本却缺少后者。第一轮控制器原文：

```text
assert 'Executing(%prep)' in log and 'Executing(%build)' in log
AssertionError
FINAL_PROJECT_FLAGS 已结束 2026-11-03T12:16:48.289526+08:00 status=failed reason=unexpected-controller-error
```

[原始根日志副本](../../tools/bolt/results/final-20261103/continue/basedev-attempt1-authoritative-build.log)、[失败控制器栈](../../tools/bolt/results/final-20261103/continue/rehearsals/basedev/evidence/failure.txt)、[首次清理](../../tools/bolt/results/final-20261103/continue/rehearsals/basedev/evidence/final-audit.json)保留；这不是发布门禁失败，也没有补写原来的FAIL为PASS。

仅改本地日志采集：核对上次读取尾部128字节来检测截断/重写，记录重置事件；停止后另存完整`rpm-build-final.log`，控制器验证这份权威副本。新增模拟“截断后增长超过旧偏移”的夹具通过；[修复diff](../../tools/bolt/results/final-20261103/continue/launcher-logging-fix.diff)、[夹具](../../tools/bolt/results/final-20261103/continue/test_log_restart.py)、[结果](../../tools/bolt/results/final-20261103/continue/log-restart-fixture.json)。最终源码仍a379，378项helper与35项参数/转换器测试不受本地采集修复影响。

### 7.4 磁盘与今晚命令（本轮未执行）

历史full-20261030整根实测峰值为68,252,237,824B（63.565GiB）。规划同时保留两根：2×68,252,237,824=136,504,475,648B。演练前先加20%保守余量，再保留20GiB运行空间，参考目标185,280,207,258B（172.56GiB），当时满足。额外保留D失败现场后，再用演练实测的根外导出/driver/cache占用替代百分比粗估：两根历史峰值＋两份较大根外实测占用＋20GiB保留。20%是本轮规划参考，不是用户规定的硬门槛，更不是发布门槛；没有把旧构建峰值冒充本轮实测。

演练前可用 209,536,942,080B；演练后 183,474,429,952B（170.874GiB），按最终分项估算需 161,230,995,456B（150.158GiB），另外还余 22,243,434,496B。原20%保守参考是否仍满足：False；明确保留该结果，不改写最初估算。根外实测见[outside-root-overhead.json](../../tools/bolt/results/final-20261103/continue/outside-root-overhead.json)；[前后空间记录](../../tools/bolt/results/final-20261103/continue/disk-budget-final.json)。T及D首轮、D重试根全部保留，full根toolchain/basedev尚不存在。启动当天仍按入口检查剩余空间，运行中低于20GiB停止，不删除任何历史目录。

先T，T验证通过后才D，不能并行。本轮只写好以下命令，没有执行：

```sh
/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/final-launch-20261103/launch.sh toolchain full
/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/final-launch-20261103/launch.sh basedev full
```

每次入口最后打印对应 `tail -f .../controller.stdout`；后台成功、失败、停止都打印带ISO时间、status、reason的“已结束”行。

### 7.5 今晚T的验证口径

| 对象 | 判定 |
|---|---|
| strip-all之后、RUNPATH之前 | SHA必须为 `13a07cb7f84bd1ceda4d851c8bd71bddf7ef0c2d4864892eba64cbbb9a0350b8` |
| RUNPATH之后、debuglink之前 | SHA必须为 `8c2429d870f421a29a9914458bc4d4ff2ce359a15e0bdd20f39bfb4580c40bdf` |
| 最终clang | SHA必须为 `4f08e12d499ebd492ce4951f74915ba435f57f2e380dc6f3520f24644996cb17` |
| ordinary未strip、clang-22.debug、静态归档成员 | 允许记录编译命令的节导致SHA变化，但须逐文件/成员证明差异只在`.GCC.command.line`等明确的命令记录节，其余字节相同 |

不能笼统忽略整个`.debug_info`、全部非LOAD节或整个归档成员。任何新增允许的“命令记录节”须给出其性质与逐字节范围证据；不能把无法解释的结构变化自动归入允许项。ar成员日期继续按成员顺序一致、成员内容SHA一致、全部差异仅date字段的三条件单列。23包对比按上述口径逐包给出内容/mtime/ar日期/命令记录差异，不把允许差异写成“完全相同”；源码包允许spec/helper/转换脚本的既定变化。90TU和其他原门禁仍必须执行。

**总结论：本轮轻量检查及两次演练全部通过，今晚可以启动；本轮未运行完整构建，产物验证尚未发生。**
