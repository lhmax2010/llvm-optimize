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
