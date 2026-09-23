# 归档索引修法试验与混合 clang profile 适用性：停止报告

日期：2026-09-23。起点：`559879a8bac5f46b4eec82df110777c47ae984c1`。
背景沿用 [docs/22](22_hybrid_link_trial.md)，不重判历史构建、正确性或性能结果。

**结论：归档索引根因已直接复现；修法尚未通过打包验收；profile v2 对混合 clang 的适用性未测。**
唯一一次重打包因试验入口遗漏 Tizen install-pre 清理行为而失败，属于本次执行方案错误，
不是归档修复补丁被证伪。按用户“每步失败即停不重试”以及短路失败时仅交根因与提案的约束，
停止后续实验。未重链、未剥离、未 BOLT、未编译本轮 30 TU；不能据此宣称需要重训或允许直接绑定。

## 0. 路径、范围和保护

下列别名均为本机路径；`temp/` 原始证据不上传 GitHub：

| 别名 | 路径 |
| --- | --- |
| W | `/home/linhao/Toolchain/development/llvm-optimize` |
| E | `W/temp/archive-profile-rebind-20260923` |
| R | `W/temp/gbs-root-x86_64-hybrid-trial/local/BUILD-ROOTS/scratch.x86_64.0` |
| B | `R/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build` |
| H | `W/temp/toolchain-hybrid-trial`，原混合 RPM 解包目录 |
| P | `R/home/abuild/archive-fix-20260923`，本轮独立试验目录 |
| E2 | `W/temp/bolt-aarch64-v2-20260921` |

读前已读 STATUS；本报告与 STATUS 同提交更新。未修改工作树 LLVM spec/源码或历史认证文件。
工作树 LLVM 子仓库已有的 `packaging/llvm.spec` 修改保留，没有复原或覆盖用户修改。
`E/protected-before.json`、`protected-after.json`、`preservation-check.json` 核实七项 SHA 全相同：
工作树 spec、R/SOURCES/llvm.spec、B/bin/clang-22、build.ninja、CMakeCache.txt、H 的 clang-22、v2 profile。
原 22 个 RPM 对 docs/22 inventory 的 SHA 核对见 `E/original-rpm-preservation.json`。

现场与任务背景有一处差异：本轮开始时原 `R/home/abuild/rpmbuild/BUILDROOT` 为空，
不是可直接复用的完整安装树。`E/preflight.json` 记录空目录；旧
`W/temp/hybrid-trial-20260922/run/build.log:21343–21348` 记录 2026-09-22 21:53:54 的 `%clean`
删除原安装树。构建树 B 和 22 个 RPM 仍在。本轮未重新完整构建。

## 1. 归档根因与修法

### 1.1 根因确认：PASS

工具采用 H 中 LLVM 22 的 `llvm-ar`、`llvm-nm`，用 R 的加载器及库运行；GNU strip 为
R 的 `/usr/bin/strip`，版本 **GNU Binutils 2.43**（`E/strip-version.txt`）。
命令记录 `E/root-cause/commands.json`；原始 ar/nm/xxd/stdout/stderr 全保留。
逐命令 nice 15、ionice idle、CPU 2、地址空间 4 GiB、core=0、180 秒超时；串行执行。

| 输入 | `llvm-ar t` 成员数 | bitcode 成员 | ELF 成员 | Archive map 条目 |
| --- | ---: | ---: | ---: | ---: |
| `B/lib64/libLLVMAnalysis.a` | 131 | 125 | 6 | 9445 |
| `H/usr/lib64/libLLVMAnalysis.a`，原 RPM 解包 | 131 | 125 | 6 | 82 |
| 构建归档独立副本，经一次 `R/usr/bin/strip -g` | 131 | 125 | 6 | 82 |

两份原始归档的成员名称及次序一致；125 个 bitcode 成员的内容 SHA 全一致。
除了五项抽样，还解析了所有归档成员，并与实际 `llvm-ar t` 输出核对。
抽样实际执行 `llvm-ar p archive member`，完整输出保存后用 `xxd -l 4` 读取前四字节，
避免 `head` 提前关闭管道产生 SIGPIPE；与任务要求的前四字节检查等价：

| 成员名 | 构建树前四字节 | RPM 前四字节 | 类型 |
| --- | --- | --- | --- |
| AliasAnalysis.cpp.o | `42 43 c0 de` | `42 43 c0 de` | LLVM bitcode |
| AliasAnalysisEvaluator.cpp.o | `42 43 c0 de` | `42 43 c0 de` | LLVM bitcode |
| AliasSetTracker.cpp.o | `42 43 c0 de` | `42 43 c0 de` | LLVM bitcode |
| Analysis.cpp.o | `42 43 c0 de` | `42 43 c0 de` | LLVM bitcode |
| InlinerSizeModel.o | `7f 45 4c 46` | `7f 45 4c 46` | ELF |

RPM 的 82 条索引按其对应成员分组如下；**恰好覆盖全部六个 ELF 成员，没有 bitcode 成员**：

| 成员名 | 索引条目 |
| --- | ---: |
| InlinerSizeModel.o | 1 |
| xla_compiled_cpu_function.cc.o | 20 |
| cpu_function_runtime.cc.o | 3 |
| custom_call_status.cc.o | 3 |
| executable_run_options.cc.o | 28 |
| runtime_single_threaded_matmul_f32.cc.o | 27 |
| 合计 | 82 |

逐符号到成员的完整映射见 `E/root-cause/rpm-armap.stdout` 的 Archive map 段及
`result.json` 的 `rpm.index`；构建对照为 `build-armap.stdout`。
GNU strip 对副本只执行一次，退出 **0**，stderr 对 bitcode 报
`Unable to recognise the format of file: file format not recognized`；
索引 **9445 → 82**，与原 RPM 的 82 条映射逐项相等。
副本在 `E/root-cause/libLLVMAnalysis.strip-copy.a`，没有在原归档上运行 strip 或 ranlib。

**“ThinLTO bitcode 成员 + 本根 GNU strip 重写符号表”成立。**
直接证据是成员仍在、bitcode 内容未变、索引仅剩 native ELF 符号，以及同工具同参数独立复现。
这证明本根工具/输入组合的行为，不推广为所有 GNU strip/plugin 配置都如此。

调用链位置（路径相对 R）：

| 文件:行 | 行为 |
| --- | --- |
| `usr/lib/rpm/tizen/macros:34–38` | `__strip_install_post`，第 36 行调用 `brp-strip-static-archive %{__strip}` |
| `usr/lib/rpm/tizen/macros:40–45` | `__os_install_post`，第 42 行调用上述宏；保留 compress、python-hardlink、find-docs |
| `usr/lib/rpm/tizen/macros:53–60` | install-post 依次执行 debug、arch、os、isu、rootstrap 检查 |
| `usr/lib/rpm/brp-strip-static-archive:15–20` | 寻找非 debug 目录的 `current ar archive`，第 19 行逐文件 `$STRIP -g "$f"` |

### 1.2 方案 A：提案存在，唯一重打包尝试 FAIL

#### 最小生产 spec diff

只在本 spec 内重定义嵌套的 `__strip_install_post`，从当前 R 宏体中去掉归档 strip。
不修改系统 rpm 宏，也不整体替换 `__os_install_post`：

```diff
--- a/packaging/llvm.spec
+++ b/packaging/llvm.spec
@@ -1 +1,6 @@
+# Preserve LLVM ThinLTO archive symbol indexes; keep other BRP processing.
+%define __strip_install_post \
+    %{!?__debug_package:%{_rpmconfigdir}/brp-strip %{__strip}} \
+%{nil}
+
 %define keepstatic 1
```

独立副本为 `P/llvm-archive-fix.spec`，diff 原件 `E/archive-index-fix.spec.diff`。
工作树 spec 和 R/SOURCES/llvm.spec 均未应用补丁。

副作用：本 LLVM spec 的所有 `.a` 都不再经过该 GNU strip 步骤，包含 static-devel、
libomp 的归档和 compiler-rt 运行库归档；native 成员可能保留更多调试信息、增加包大小。
其他 ELF strip 条件及 os-post 链保留；本宏定义不会持久改变其他独立 RPM 构建的宏。
这些是作用域/机制分析，**不是 22 包非 `.a` 等价性实测**。目标 OBS 宏如有变化，必须重新核对。

#### 实际执行入口与失败原因

R 的 RPM 为 **4.14.1**，`E/rpm-version.stdout`、`rpmbuild-help.stdout:44–54`：
`--noprep` 跳过 prep，`--noclean` 跳过 clean，`--nobuild` 不执行任何构建阶段，
`--short-circuit` 的本机帮助文本仅列 `c,i`；未把其他版本的 `-bb --short-circuit` 行为当成本机保证。
本轮没有把 `--nobuild` 误用为“仅跳过编译”。

原安装树不存在，先从原 22 个 RPM 恢复到 `P/BUILDROOT`，再把构建树对应的 226 个开发归档放回。
226 是 **llvm-static-devel 225 + libomp-devel 1**，不是 static-devel 自身 226。
22 次解包与 226 次恢复成功；证据 `E/repack-preparation/extraction.json`、`restored-archives.json`。

独立 `P/llvm-repack-trial.spec` 另有以下**仅试验入口**改动，不属于上面的生产补丁：
将 `%build`、`%install` 主体换成 `:`，复用已处理的 debug payload/list，
设置 `__debug_install_post %{nil}`，保留 arch/os/isu/rootstrap 后处理。
完整差异 `E/repack-harness-only.diff`。本轮原本拟验证归档后处理和重打包，不重复 find-debuginfo。

唯一一次打包命令，在 R 内以 abuild 执行：

```sh
rpmbuild --define '_smp_mflags -j4' \
  --define '_srcdefattr (-,root,root)' --nosignature --target=x86_64 \
  --define '_build_create_debug 1' \
  --define '_rpmdir /home/abuild/archive-fix-20260923/RPMS' \
  --buildroot /home/abuild/archive-fix-20260923/BUILDROOT \
  -bb --noprep --noclean /home/abuild/archive-fix-20260923/llvm-repack-trial.spec
```

**入口错误：漏查 Tizen 的 install-pre 覆盖。**
`R/usr/lib/rpm/tizen/macros:234–239` 在 `%install` 主体执行前 `rm -rf "$RPM_BUILD_ROOT"` 并重建空目录。
因此预先恢复的独立 payload 被清空；空 `%install` 没有恢复它，后处理扫描的是空树。
`E/repack-scope/build.log:41–60` 记录删除与后处理，`:130` 起报告 File not found。
该日志中没有执行 `brp-strip-static-archive`，只能证明宏链移除了此命令，不能证明归档经链处理后完好。

前置只读 `rpmspec -P` 首次错误地带了其不支持的 `--buildroot`（保留错误输出）；
去掉该参数后解析成功，展开的 `%build/%install` 主体确为 no-op。
**只看 `rpmspec -P` 主体没有验证隐式 stage preamble，未防住此次错误。**
这两次是只读参数检查，不是重复打包；实际 rpmbuild 仅上述一次。

此外，rootstrap 检查日志出现 SOURCES 多个 spec 被作为单个参数解析的错误及 `/dev/fd` 错误，
不能凭它们输出 SUCCESS 判定该层通过。见 `build.log:61–129`。本轮未修改或重跑这些钩子。

| 指标 | 实测 |
| --- | --- |
| 执行时间 | 2026-09-23 13:30:03–13:30:16，+08:00 |
| guard wall | 12.271 秒 |
| 内存/调度保护 | 18 GiB cgroup、swap=0、nice 15、idle IO，2 秒进程采样/30 秒系统采样 |
| rpmbuild 实际退出码 | **1** |
| gbs 外层退出码 | 0；guard 通过内层 command.exit 检出失败，整体脚本退出 2 |
| scope memory.peak | 48,472,064 B；OOM/oom_kill 均 0 |
| 新 RPM 数 | **0** |
| 后台采样/日志线程 | 已回收；scope 状态另留证 |

证据：`E/repack-scope/{outcome.json,memory-summary.json,stopped.json,build.log}`。
错误是本次试验入口实现问题，**不能写成“RPM 4.14.1 不支持短路重打包”**。
后续如获新任务授权，可在 `%install` 主体内从独立、不会被清理的 staging 恢复 payload，
让 install-pre 先正常执行；应先验证完整宏展开、清理边界与 rootstrap 输入。
这是未执行的候选修正，本轮没有改入口重试。

#### 要求的验收状态与后续测试

| 验收项 | 本轮结果 |
| --- | --- |
| 新包 226 归档逐一与构建树 Archive map 对照 | NOT RUN；没有新 RPM |
| Analysis/CodeGen/Support 恢复到 9445/14276/5023 | NOT VERIFIED；§1.1 仅实测 Analysis 根因 |
| 22 包文件清单及非 `.a` SHA 不变 | NOT RUN；不能用原包自比冒充修复前后对比 |
| 新 static-devel core/support 消费者，bfd/lld 链接并运行 | NOT RUN |
| docs/21 §4.4 lldCOFF 消费者，bfd + 同版 LLVMgold / lld，运行且无 LLVM 动态 NEEDED | NOT RUN |
| 已知坏 liblldCOFF.a 索引负例及实际链接结果 | NOT RUN；保留 docs/21 的既有 SHA，未冒充本轮负例结果 |

修法进入 spec 前仍需上述全部测试，Archive map 应比较完整映射或至少逐归档精确计数，
不能继续采用“非空即完整”。包范围覆盖 compiler-rt；检查宏关闭后增加的 `.a` 大小和 native DWARF。
须补“安装前清空根”的入口测试，确保 payload 在清空之后恢复，且只清理本次独立目录。

### 1.3 当前全静态产物的既有缺陷

这是**当前全静态 spec 所产出的 llvm-static-devel 的既有缺陷，与混合/BOLT 无关**。
历史证据为 [docs/13“GNU strip 对 ThinLTO 静态归档的处理”](13_baseline_build.md#gnu-strip-对-thinlto-静态归档的处理)：
全静态构建树、BUILDROOT、最终 RPM 的 liblldCOFF.a 对照已记录索引丢失；
坏归档 SHA 为 `9e8915f4a853a8a97285f34c2b51eb2bc16eb3fb3de943fdabf43f1b3e252617`。
本轮新增的是混合 Analysis 的直接复现，不是把旧包问题归因于混合链接。
“既有产物缺陷”不代表本轮另行证明了所有线上快照的具体文件状态。

修复建议同 §1.2 的最小 spec diff，**待用户批准后进 Gerrit**；
当前还欠重打包与消费者验收，不能以补丁提案替代修复完成。本轮未推 Gerrit。

## 2. profile v2 对混合 clang 的适用性

### 2.1 重链：仅完成只读预检，NOT RUN

`E/ninja-command.stdout` 保存对 B 执行 `ninja -t commands -s bin/clang-22` 的最终边，
命令长约 5000 字符，没有 `@rsp`；保留原 cwd、shell 引号和 `$ORIGIN`，
候选重放命令仅改独立输出/依赖文件并追加 `-Wl,--emit-relocs`，见 `E/relink-command.txt`。
该候选没有执行，不能宣称完成原构建环境等价性认证。

`E/preflight.json`：`B/lto.cache` 有 12,469 个文件、20,363,360,960 B，是本次混合构建留下的非空缓存。
计划使用热缓存 16 GiB cap、1200 秒 timeout；未触发空缓存 18 GiB 分支。
**lld VmHWM、wall、实际 cache 命中均 UNKNOWN/NOT RUN**；非空文件不等于命中率实测。

### 2.2 剥离与纯重写：NOT RUN

选定的 profile 为 `E2/profile-work/merged-v2.fdata`，SHA
`d9b132f9430dfed32e080c65b4422bd76eba4a9c2101a2b18a7f66c94133b326`，前后未变。
H 原始 clang SHA `eeb3495775e42948998f4ba31f8c0856efd3c5df421e5ed984fdf586025b4369`，前后未变。

未产生 relocs-H、stripped-H 或 BOLT-H；未调用 llvm-objcopy、check_bolt_elf.py 或 llvm-bolt。
因此没有本轮 dyno-stats 全文、invalid/stale 行、警告计数或 stale-threshold 退出结果。
历史 `E2/rewrite-scope/build.log:9–20` 的 **23592/144032、1/2804/6** 仅是预定比较基线，
不是 H 的测量值。不能把历史日志复制为本轮实测。

判定：**适用性未知，未达到 §3.2 第二级图等价的实证条件**。
没有证据要求重训，也没有证据允许直接绑定；旧 profile 的旧输入绑定维持原状。

### 2.3 正确性与活性：NOT RUN

BOLT-H 未产生，ARM 训练 10 + ARM 留出 10 + AArch64 10 的本轮 H/BOLT-H 比较未执行；
`check_bolt_liveness.sh --host-arch x86_64` 对 BOLT-H 也未执行。
docs/22 的 H/全静态 TC 30 TU PASS 仍有效，但不能替代本轮缺失的 H/BOLT-H 对照。

## 3. 最终裁决与证据入口

- **归档修法能否进 spec：尚不能作为已验收修复进入。** 根因成立，最小补丁可供评审；
  需新的授权任务修正试验入口并完成 226 归档、22 包等价和消费者/负例验收。
- **profile v2 能否直接绑定混合 clang：本轮未证明，保持未认证。**
  重链、剥离、重写、30 TU、活性均未启动；没有补跑，没有采新 profile 或做性能校准。
- 没有构建 Chromium、没有完整重建、没有改工作树 LLVM spec/源码、没有推 Gerrit。
  本轮仅向 GitHub 提交本报告和 STATUS；失败状态与缺失实验明确保留。

主要原始证据目录：`E/root-cause/`、`E/repack-preparation/`、`E/prepare-scope/`、`E/repack-scope/`。
完整命令在 `root-cause/commands.json`、`repack.sh`、`repack-scope/stage.json`；
前后保护在 `protected-{before,after}.json`、`preservation-check.json`、`original-rpm-preservation.json`。
原 22 RPM SHA 均相同；prepare/repack 两个 scope 最终均为 inactive/dead，记录在 E 的对应 `.scope.state` 文件。
