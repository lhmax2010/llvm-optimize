# 04 新基线、sandbox与Quickbuild环境

日期：2026-10-13（Asia/Shanghai）。本轮E=`/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41`，B=`/home/linhao/Toolchain/development/llvm-optimize-bolt`。所有克隆/快照在E；W/llvm和归档根未改。最新输入以本轮取到的Git对象/配置为准，不把旧快照当新Quickbuild执行日志。

## 1. Gerrit建分支

git ls-remote确认tizen_base最新HEAD为 `cb67996861d070d68fec2b4c623eed7d20ba2e23`，与原计划cb679968完全相同；不同于采集配方 `f111162e94aa48ed367c9d2c039456c70e7160ae`。确认目标refs/heads/sandbox/lhmax2025/bolt_pgo不存在后，仅推原始HEAD，无新提交、无force。推送返回0，复查sandbox也指向同一cb。证据E/gerrit-opening.json、gerrit-branch-result.json。

```sh
git push ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm \
  cb67996861d070d68fec2b4c623eed7d20ba2e23:refs/heads/sandbox/lhmax2025/bolt_pgo
```

此命令本轮已执行一次；后续不要重建已存在分支。只读源副本E/llvm-source来自W/llvm的共享对象克隆并checkout该HEAD，源工作树开场干净；之后补丁仅在此副本实现。BOLT提交本任务不推Gerrit。

## 2. 基线差异及预演迁移边界

与f111162e相比：14文件556增/14删，源码差异仅libcxx/libcxxabi及独立runtime配方；LLVM/clang/bolt源目录无差异。spec x86显式clang/clang++；_toolchain未定义时后补clang与BR；显式LLVM_LINK_LLVM_DYLIB=OFF、CLANG_LINK_CLANG_DYLIB=OFF；强制O3/ThinLTO只在x86；优化清理删除-fno-inline-functions、先删长stack-protector选项，并加诊断flag。旧树实际cache与源码HEAD是f111162e，x86工具也静态。完整diff保留source-spec.diff/source-diff-stat.txt。

**clang不预期逐字节等同历史采集ELF**：源码热点相同是profile适用的有利条件，但实际driver/宏/flags与构建元数据可能改变。profile v2兼容性仍以新ELF的R与S/N≤5%为准，当前UNKNOWN。旧树能验证链接解析、双链接flags、BOLT工具/数据格式、匹配parser、别名和RPM脚本机制、同旧基线的对象一致性；不能证明新配方匹配、新项目宏、完整新RPM、Quickbuild性能或最终90对通过。

## 3. project_config原文与路由

元数据仓库ssh://lhmax2025@review.tizen.org:29418/scm/meta/qb；本轮HEAD `4937b4163c76b4051fe8522f04ffdc68fb6fd77b`。独立浅克隆E/qb-meta；全文在克隆，精确行号与SHA在qb-scan.json。

TIZEN/Tizen/Tizen-Base-Toolchain/project_config:134：

```rpm
%_toolchain %{?_toolchain_override}%{!?_toolchain_override:clang}
```

同文件152–156：

```rpm
%install %{?_enable_debug_packages:%{?buildsubdir:%{debug_package}}}\
%%install\
export AR=%{__ar} RANLIB=%{__ranlib};\
export CC=%{__cc} CXX=%{__cxx};\
%{nil}
```

Toolchain/project_meta:2–4是debuginfo enable，standard包含x86_64；Toolchain/manifest.xml:109明确platform/upstream/llvm（快照revision7e4dc62d…，不能冒充本轮sandbox HEAD）。Tizen-Base也在manifest:109包含llvm且standard有x86，但其project_config无_toolchain定义，project_meta同样enable debuginfo。Unified-Toolchain的本地config无_toolchain，其manifest未列llvm；不能据此断言它直接构建llvm或推断隐式继承宏。

(a) **分项目结论**：在Toolchain配置先加载、_enable_debug_packages有效的情况下，_toolchain定义使llvm.spec:11–16选择llvm_release_build=0；install宏启用debug_package，首版BOLT debug条件可满足。在Base配置且没有其他外来_toolchain宏的情况下，spec先选llvm_release_build=1，24–30禁用debug_package；60–67稍后补定义clang不会重算已选值，仍是发布分支。实际Quickbuild sandbox请求选哪个项目/合并宏未得到，不能把条件推导冒充实际job日志。

(b) **BOLT含义**：本周只支持__debug_package定义；Toolchain候选可进入，Base上述发布路径必须清楚失败，不能默默关BOLT或全包禁strip。需对实际RPM展开验证定义时序，不能在尚未展开install宏的位置误判。待用户给实际Quickbuild项目/请求路由，不在本轮提问。

供归档修复会话独立引用：**Quickbuild并非一律debug。qb元数据4937b416…的Tizen-Base-Toolchain/project_config:134提前定义_toolchain=clang，llvm.spec据此选debug分支，项目meta开启debuginfo；Tizen-Base本地config无此宏，spec先选发布分支并禁debug_package，稍后的clang fallback不重算release值。两项目manifest:109均含llvm/x86候选；实际sandbox job项目与最终宏尚未知，归档修复应分别验证发布/debug展开，不能用“project_meta enable”单独证明spec走debug。**

llvm/x86候选全集（据manifest与project_meta）：

| 项目 | _toolchain本地定义 | llvm manifest位置 | x86 |
|---|---|---|---|
| Tizen-Base | 无/需合并宏核查 | 109 | 是 |
| Tizen-Base-ASAN | 无/需合并宏核查 | 101 | 是 |
| Tizen-Base-Dev | 无/需合并宏核查 | 109 | 是 |
| Tizen-Base-RISCV | 无/需合并宏核查 | 101 | 是 |
| Tizen-Base-SC | 无/需合并宏核查 | 109 | 是 |
| Tizen-Base-Toolchain | 有 | 109 | 是 |
| Tizen-Base-X | 无/需合并宏核查 | 109 | 是 |
| Tizen-Base-X-ASAN | 无/需合并宏核查 | 103 | 是 |

## 4. 磁盘与续跑预算

本轮W/B所在/dev/sda1余106519019520B（99.20GiB）；/var/tmp所在根文件系统余266072498176B（247.80GiB）。不清理、不借用归档根。历史续跑以60GiB可用空间为准入，22个二进制RPM约8.86GB，另有buildroot/debug树、SRPM、转换临时文件与cache；BOLT relocs/候选/profile及90资产另需数GiB。建议明天保留至少历史60GiB再加BOLT临时量，实际tree/buildroot/RPM旧文件及archive任务占用需重算。本轮当前空间可支持轻任务和有限预演，**不是明晚够用的保证**；每次阶段开始再查。不够则停该阶段报告，未经授权不清理。

## 5. profile失配应急（仅估算，未执行）

新基线R或S/N>5%时先失败停止试包，记录N/S/U/argv/输入/工具SHA。若用户另行批准重新训练：用新clang relocs输入单线程插桩→同ARM13+AArch6410冻结负载分别编译并留PID fdata→明确清单merge→同v2参数重写→重新正确性/压缩/Source/hash与补丁评审→Quickbuild重建。禁止复用旧插桩ELF训练新二进制。

历史插桩cap22GiB，自身峰19.72GiB、66.72s；ARM13采集含基线/merge366.80s；新增A6410含审计/merge296.02s；热重链227.66s，重写26.32s。净步骤约16.4分钟仅为历史相加参考，**不含新预处理、90对验证、重新打包、排队及Quickbuild全构建**。实际端到端预计至少另留数小时且未知；周四一轮评审/周五交付会有明显延期风险。当前16GiB重阶段政策不能容纳历史插桩22GiB需求，必须另有资源裁决，今天不插桩/不采profile。

## 2026-10-14 用户确认（覆盖此前实际 job UNKNOWN）

当前 Quickbuild 在 Tizen-Base-Toolchain 项目构建 llvm，定义 _toolchain，spec 走 debug 分支；以后进入 Tizen-Base 时不定义 _toolchain，spec 走发布分支，不跑 find-debuginfo，由 GNU brp-strip 处理 not stripped 可执行文件。此为用户人工裁决前提，不再等待项目信息；完全 strip 的 BOLT 交付须支持两模式。
