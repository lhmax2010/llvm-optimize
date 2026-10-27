# 37：RUNPATH 修复、工具并行、真实源码门禁与测量

RUNPATH 已在本轮完整构建中用 CMake `file(RPATH_CHANGE)` 修成 `$ORIGIN/../lib64`，安装及 post 门禁通过。工具构建由上次实测 337 秒降至 108 秒，三处 real 检查 24/24 对通过、合计 52.61 秒。RPM 严格内容比较随后发现 compiler-rt 的 45 个归档 SHA 不同（只读诊断证明仅 ar 内部时间戳不同），按停止条件结束，因此 old-text 大小/性能和运行时 RSS **未测量，不能给出结论**。

## 1. 范围与身份

本轮仅本地源码提交、GitHub `bolt-v4` 证据；不推 Gerrit/sandbox，不操作 QB。基线 `aa637c1b4a0f9ea9f6f0317cf035126eba85aeb7`，amend 后本地 detached HEAD 为 `ac112ebfd6e7983bdfd4c38dd156e6baba72731b`，tree `581bc4d92752ee7e2de9f7aa70d79cb174c3293b`，父提交仍为 `6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2`。作者、提交者及 Signed-off-by 为 Hao Lin <hao.lin@samsung.com>；Change-Id 不变。

相对 aa637c1 只改 spec/helper：[源码 diff](../../tools/bolt/results/runpath-fix-20261026/source.patch)、[spec](../../tools/bolt/results/runpath-fix-20261026/llvm.spec)、[helper](../../tools/bolt/results/runpath-fix-20261026/clang-bolt-helper.py)。Source1200、OPTIONS、111 条 BOLT 白名单和 2 条 TF 白名单保持不变，见 [常量 AST 核对](../../tools/bolt/results/runpath-fix-20261026/unchanged-production-constants.json)。提交说明同时修正旧的 serial/-j1 描述，避免与新并行行为矛盾。

## 2. 实现

- 普通 CMake 安装完成、snapshot 之前执行 `installed-baseline`，保存安装版 SHA、DT_RPATH/DT_RUNPATH 原值和完整安全属性。
- strip-all 后用构建环境 CMake 的 `file(RPATH_CHANGE)` 原地处理 candidate。用 ELF reader 和 readelf 独立核对两种路径标签。全部程序头/节头、文件大小、动态标签序列、代码节 SHA，以及 `.dynstr`/`.dynamic` 之外的全部文件字节必须保持；失败不安装。
- candidate 和安装基线比较所有安全属性；ordinary 对照只豁免两种路径标签。post 同样检查安装基线及其 SHA。identity 保存 strip-all SHA、RPATH-adjusted SHA 和经临时安装文件校验的 installed SHA；安装仍为临时文件校验后原子改名。
- llvm-bolt 使用 `%{mlgo_build_jobs}` 并行构建。计划/执行按任务集合比较，同时保留进度格式、唯一计数、完整任务数量和白名单检查；允许打印顺序变化。Ninja 的 restat 总数兼容性保持，但执行集合必须等于计划集合。
- 三处 real 门禁：BOLT 后、strip-all/RUNPATH 后、post。两侧使用同一编译器路径/inode、同一输出路径，比较完整对象 SHA，不移除 `.GCC.command.line`。

真实用例固定为 compiler-rt/lib/builtins/{bswapsi2.c,bswapdi2.c}（三个目标，-O2 -g）以及 llvm/lib/Support/{SmallVector.cpp,StringRef.cpp}（x86_64，-O2 -g -std=c++17）。C 额外用 `-ffreestanding -nostdinc` 和显式 resource include，避免跨目标系统头依赖。C++ 包含源码和生成头目录。每处 8 对。

## 3. 准备与轻量认证

新根先按同一固定快照完成 `%prep`；在该根的独立 `pretrial-include` 中只配置生成头、不构建 LLVM，再用保全的普通 clang（SHA d5090159915657b235b96f1202c058e1efd1647d6a2225ac8fdb2906aeaa501d）试编译。8 项通过，编译总耗时 1.293 秒；这只是选例准备，正式三处门禁使用本轮普通 clang 和本轮构建生成的头。见 [预试结果](../../tools/bolt/results/runpath-fix-20261026/pretrial-result.json)。

全部 **317 项测试 PASS**（原 300 + 新 17），见 [stdout](../../tools/bolt/results/runpath-fix-20261026/tests.stdout)、[stderr](../../tools/bolt/results/runpath-fix-20261026/tests.stderr)。既有 pipeline/post 夹具补安装基线和 real/RPATH 调用断言；历史“不变函数”断言只去掉本次明确授权改变的 security_compare、tool_plan、tool_verify，其余仍核对。

新提交 gbs export 通过，Tizen rpm/rpm-build 4.14.1.1-1.7 五项解析通过；关闭 BOLT 的源 spec 在 debug/release 两种宏下展开与 aa637c1 **逐字节相同，不做归一化**。采用源 spec 比较以避免 GBS 自动 VCS 行的无关差异。见 [五项矩阵](../../tools/bolt/results/runpath-fix-20261026/five-parse/matrix.json)、[OFF 比较](../../tools/bolt/results/runpath-fix-20261026/five-parse/off-comparison.json)。

准备问题与处理均保留在 [preparatory-corrections.json](../../tools/bolt/results/runpath-fix-20261026/preparatory-corrections.json)：主机默认 PATH 无 CMake，夹具改用已存在的 CMake；解析曾早于导出结束；解析目录遗漏 Source0，首次复制又遇到 rpmbuild 已创建的空 SOURCES；补齐后重新认证。正式构建尚未开始时，GBS 暂存父目录因 sudo 初始化而为 root 属主，改用用户属主的 `gbs-driver/local` 保存 sources/repos，BUILD-ROOTS 软链接回同一个新根；未改权限、未删除目录。没有修改产品门禁来通过这些准备检查。

## 4. 构建条件与过程

固定快照 `20261013.024319`，只启用 packages/debug；build.conf SHA 为 `e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945`。父日志三个宏和 threads=30 不变。MemoryMax=24,482,967,552 B（MemTotal−8 GiB），swap=0，nice=10，ionice=2/7；不设内存准入、不冻结。/home 可用低于20 GiB则停止；这些只在本地驱动，不进入发布代码。

物理根：`W/temp/runpath-fix-20261026/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0`；GBS 驱动通过 `gbs-driver/local/BUILD-ROOTS` 指向同一根。预试与正式构建复用该新根，历史根未执行 CMake/Ninja。每60秒 du，失败/超时样本保留。基线23个 RPM SHA 全部通过，见 [核对结果](../../tools/bolt/results/runpath-fix-20261026/baseline-rpm-sha.json)。

完整构建成功；全部构建内门禁通过。独立 RPM 内容比较失败后停止，90 TU、old-text 和 RSS 未运行，详见第 6–9 节。

## 5. 挂账

- `-use-old-text` 是否采用，由用户看测量数据后决定；本轮不改生产 OPTIONS。
- 完全 strip 交付的崩溃定位方案待用户决定；继续保全 ordinary、BOLT 前后 ELF、身份和重写记录。


## 6. 完整构建与门禁结果

本轮 GBS 外层耗时 **7515.61 秒**；包日志最后 `[7495s]` 报构建结束，GBS 返回 0。产出 **22 个二进制 RPM + 1 个源码 RPM**，已保全到 `W/temp/runpath-fix-20261026/products/`，逐个 SHA 核对并生成 SHA256SUMS；根和产物都保留。见 [build-result](../../tools/bolt/results/runpath-fix-20261026/build-result.json)、[保全清单](../../tools/bolt/results/runpath-fix-20261026/preserved-products.json)、[完整日志](../../tools/bolt/results/runpath-fix-20261026/rpm-build.log)、[锚点](../../tools/bolt/results/runpath-fix-20261026/excerpts.txt)。

| 检查 | 结果 |
|---|---|
| 本地夹具 | PASS，317 项（原 300 + 新 17） |
| gbs export / Tizen rpm 五项解析 | PASS，5/5 |
| BOLT OFF debug/release 与 aa637c1 展开 | PASS，逐字节相同 |
| tool-plan / tool-verify | PASS，113/113；111 BOLT + 2 TF；ninja diagnostics=0 |
| 匹配统计 | N=23592，M=144032，S=0，U=1，Q=383；R=0.0042385453%，S/N=0；与上次相同 |
| BOLT 标识、strip、两次 tiny、安全属性 | PASS |
| RUNPATH 与 installed-baseline / 布局门禁 | PASS，RUNPATH=`$ORIGIN/../lib64`，RPATH=null，无构建路径/空项 |
| compare-root | PASS |
| cache-release | removed，13162 文件，21622697984 B（20.138 GiB），13.05 秒 |
| Source1005 | PASS，225 个转换归档；45 个原生归档跳过转换 |
| post 身份、安全属性、别名、反向检查、tiny/real | PASS，`BOLT_POST_GATE_PASS` |
| RPM 完整内容比较 | **FAIL**：compiler-rt 的45个 `.a` 文件 SHA 不同；第7节 |
| 90 TU、old-text 正确性/性能、RSS | **NOT RUN**：上述门禁失败后停止 |

三个 real 检查点各 8 对，完整 `.o` 字节相同：

| 检查点 | 通过 | 耗时（含该检查点内准备/复制） |
|---|---:|---:|
| BOLT 重写后、strip 前 | 8/8 | 29.850 s |
| strip-all/RPATH 后 | 8/8 | 13.369 s |
| post 尾检 | 8/8 | 9.394 s |
| 合计 | 24/24 | **52.613 s** |

[资格复核](../../tools/bolt/results/runpath-fix-20261026/qualification.json)及 [bolt-work](../../tools/bolt/results/runpath-fix-20261026/bolt-work/) 保存全部 JSON 和编译日志。身份链：

- ordinary：`d5090159915657b235b96f1202c058e1efd1647d6a2225ac8fdb2906aeaa501d`，与 aa637c1 ordinary 相同。
- strip-all 后、改 RUNPATH 前：`8b799f18e2bc37269385db125c881609e8457de1dd179f5d9d0ff9f557b58d16`，与 aa637c1 candidate 相同。
- 改 RUNPATH 后 / 临时安装校验 / 最终安装：`963f1163fa983737a43ec5b4bd04fa142a4236829dee290b23feeda28abd1c9e`。
- installed-baseline：`db34590a532a05935df2996a9e47aad3253e5144745da9c44b9759271594a58e`。

流水线已验证本轮 strip-all 前后对应的布局与非路径字节约束；改 RUNPATH 前候选的完整 SHA 等于上次候选。因此已有身份链与布局证据支持“本轮 candidate 仅有允许的路径区域变化”。独立比较脚本末尾对两份 ELF 再做直接比较尚未执行：它在 compiler-rt 门禁失败处停止，不能声称该独立项已运行。

## 7. RPM 比较失败及停止处置

原23个 RPM 用前 SHA 全部匹配旧保全记录。比较按包名排序，文件清单、类型/权限/属主、大小、完整内容 SHA 严格核对；RPM 载荷条目的 mtime 单独记录，不参与内容相等判定。

| 已比较包 | 内容变化数 | 载荷 mtime 变化数 | 结果 |
|---|---:|---:|---|
| clang-22.1.8-1.x86_64.rpm | 1 | 66 | PASS |
| clang-debuginfo-22.1.8-1.x86_64.rpm | 0 | 27 | PASS |
| clang-devel-22.1.8-1.x86_64.rpm | 0 | 237 | PASS |
| clang-devel-debuginfo-22.1.8-1.x86_64.rpm | 0 | 4 | PASS |
| compiler-rt-22.1.8-1.x86_64.rpm | 45 | 105 | **FAIL** |

clang 主包唯一变化为 `usr/bin/clang-22`，另三个已比较 clang 包内容不变。**剩余17个二进制 RPM和源码 RPM未继续比较**，不宣称“其他21包全部一致”。完整逐文件结果和 mtime 清单见 [RPM summary](../../tools/bolt/results/runpath-fix-20261026/rpm-comparison/summary.json)、[compiler-rt 原始对照](../../tools/bolt/results/runpath-fix-20261026/rpm-comparison/compiler-rt-22.1.8-1.x86_64.rpm.json)、[断言 stderr](../../tools/bolt/results/runpath-fix-20261026/rpm-comparison.stderr)。

原文关键项：

```text
RPM compiler-rt-22.1.8-1.x86_64.rpm changed 45 timestamps 105 PASS False
AssertionError: ... 'PASS': False
```

只读诊断进一步拆解这45个 ar 文件：全部成员的内容 SHA 相同，除 ar header 的12字节 date 字段外的**全部字节相同**。例如 `libclang_rt.asan-preinit-x86_64.a` 的 `/` 和 `/0` 两个成员：

```text
old_date = '1792773555  '
new_date = '1793080900  '
old SHA = 123b8bd0b8f6f862025b6122a27390d911487b25c2e74bb100855cc9fed83c9e
new SHA = 44dabd25c8bb4f70d58e60ad4f7ffee6f013b75fd4250efa9b3df222ea1b89a7
```

[逐归档/逐成员诊断](../../tools/bolt/results/runpath-fix-20261026/rpm-comparison/compiler-rt-ar-diagnosis.json)保存45项全部结果。这里是文件**内部字节**变化，不是已经单列的 RPM 文件 mtime。本轮未把内部时间戳自动加入许可范围，未改比较代码、未修改任何归档或 RPM，严格 SHA 门禁仍为 FAIL。时间值与两轮平台 static-archive strip 时段相符；“由平台 strip 重写 ar 日期产生”是基于时序的**推测**，本轮未做额外复现实验。

用户规定任一门禁失败即停止，因此不执行后面的90 TU、old-text和RSS。用户若后续允许单独归类 ar 内部日期，需明确比较口径后再续跑；本轮不自行决定。构建根、candidate、ordinary、全部RPM均保留，没有推送Gerrit/sandbox。

## 8. 时间与磁盘

与33号原始日志比较，明确区分 `ninja` 本身与前置阶段。上次“约13分钟”实际对应 begin→tool-built（799秒），不是纯工具构建（337秒）。

| 时间段 | aa637c1 原日志 | 本轮 | 本轮减去上次 |
|---|---:|---:|---:|
| ninja llvm-bolt（上次-j1 / 本轮-j6） | 337 s | 108 s | -229 s |
| disk-report begin → tool-built | 799 s | 259 s | -540 s |
| disk-report begin → compare-root | 1201 s | 883 s | -318 s |

纯工具构建实测减少229秒（约68.0%）；不同日期、缓存/负载/磁盘条件的两次运行，不能把全部差值归因于并行。锚点与行号见 [时间对照](../../tools/bolt/results/runpath-fix-20261026/timing-comparison.json)、[基线原文](../../tools/bolt/results/runpath-fix-20261026/baseline-timings.json)。本轮重链期间观察到块设备等待与较高I/O压力、低内存压力，见 [只读观察](../../tools/bolt/results/runpath-fix-20261026/relink-io-observation.json)。没有修改参数来避开等待。

本轮构建 cgroup 峰值 **16105480192 B（14.999 GiB）**，memory.events 的 oom/oom_kill/max 全为0，swap峰值0。每60秒 du，共122个有效样本、4个缺失样本，缺失原文保留。观测构建根峰值 **72498270208 B（67.519 GiB）**，位于BOLT阶段；这是离散采样下界，不是连续精确峰值。构建前整个任务可用空间约538GiB；本轮不清理任何历史目录。

| 阶段 | 观测峰值 GiB |
|---|---:|
| ordinary-build | 46.823 |
| ordinary-install | 58.465 |
| BOLT | 67.519 |
| cache-release | 无完整落在该短阶段内的样本 |
| native-conversion-install | 53.337 |
| platform-post | 46.396 |
| packaging | 41.457 |

[原始 du](../../tools/bolt/results/runpath-fix-20261026/du-root.jsonl)、[资源采样](../../tools/bolt/results/runpath-fix-20261026/resources.jsonl)、[阶段统计](../../tools/bolt/results/runpath-fix-20261026/disk-comparison.json)。本轮带额外选例配置目录、较多证据文件，不把与33号64.055GiB的差值简单归因于发布代码。

## 9. 采集修正、未运行项与交付边界

构建结束后 GBS 将根内 `.build.log` 移到 `gbs-driver/local/repos/tizen_base_toolchain_standard/x86_64/logs/success/llvm-22.1.8-1/log.txt`。独立资格脚本首次在复制日志时 FileNotFoundError，尚未执行产品断言；定位实际日志后只修正采集路径，保留第一次错误输出于 [preparation-final-log-path](../../tools/bolt/results/runpath-fix-20261026/preparation-final-log-path/)，未重跑构建。之后资格复核PASS、保全完成；真正的停止点为第7节RPM门禁。其它准备修正见第3节及完整JSON。

- 未运行：最终 candidate 90 TU；old-text 重写/大小/匹配/内存/90 TU/三方耗时；普通与最终candidate的逐文件RSS。没有填充、估算或沿用历史测量冒充本轮数据。
- 未改：Source1200、生产OPTIONS、白名单；普通构建/安装/平台后处理执行方式；VS Code配置。
- 没有删除构建根，没有创建分支，没有推送Gerrit/sandbox，没有操作QB。
- 已保全完整构建与失败证据；本地源码为本文第1节SHA，不是已全部认证的交付版本。
- 后台日志末行固定为 `RUNPATH_FIX FINISHED ... status=stopped reason=rpm-content-gate-compiler-rt-45-ar-files`。

**挂账仍为：old-text是否采用、崩溃定位方案。** 因本轮停止，old-text没有新增测量可供采纳；另需用户裁决归档内部日期差异的验收口径，才能继续未执行的独立验证。
