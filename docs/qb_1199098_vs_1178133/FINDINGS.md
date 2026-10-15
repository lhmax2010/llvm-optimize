# Quickbuild 1199098 与 1178133：事实与证据

用途：供 Claude review。本文仅记录采集结果与确定的算术差值，不判断变慢原因。

范围：两个 Quickbuild ID 都是 `Tizen-Unified-Toolchain/standard/armv7l`。用户补充的 Base 快照分别为 `tizen-base-toolchain_20261015.022255` 和 `tizen-base-toolchain_20260914.073422`，与 Unified 日志中的依赖地址一致。Base 快照的构建日志、RPM 是**关联依赖证据**，不是这些 Unified ID 的产物。证据：[raw/1199098_html_index.html:31–35](raw/1199098_html_index.html#L31)；[raw/1178133_html_index.html:31–35](raw/1178133_html_index.html#L31)；[raw/1199098_quickbuild.txt:131](raw/1199098_quickbuild.txt#L131)；[raw/1178133_quickbuild.txt:135](raw/1178133_quickbuild.txt#L135)。

原始 HTTP 响应不改写，URL、获取时间、字节数、SHA-256 和 HTTP 状态记录在 [raw/fetch_manifest.jsonl](raw/fetch_manifest.jsonl)。`.pretty.json` 仅将对应原始 JSON 缩进，已验证解析后相等；网页 `.txt` 为 HTML 文本提取。CSV 的 `evidence` 列给出 raw 文件及从一开始的行号。`duration_ratio_optimized_over_baseline` 为优化/基线，`exact_ratio` 保留精确分数；显示小数是该分数的格式化值。没有独立等待/调度字段时写“未获取”，不以总时长减包时长代替。

## 总耗时

| 构建 | Quickbuild 起始（页面原文） | 结束（起始+页面总耗时） | Quickbuild 总耗时 | 证据 |
| --- | --- | --- | --- | --- |
| 1199098 | 2026-10-15 03:21:59 | 2026-10-15 08:27:46 | 5 hours 5 minutes 47 seconds = 18347 秒 | [raw/1199098_overview.html:839–841](raw/1199098_overview.html#L839) |
| 1178133 | 2026-09-17 13:24:24 | 2026-09-17 18:22:28 | 4 hours 58 minutes 4 seconds = 17884 秒 | [raw/1178133_overview.html:839–841](raw/1178133_overview.html#L839) |

优化侧 Quickbuild 总时长比基线多 **463 秒**；精确比值为 `18347/17884`。[raw/analysis_summary.jsonl:4](raw/analysis_summary.jsonl#L4)。

| 构建 | Profiling 起始（原文） | Profiling 结束（原文） | Profiling RunTime/1000（秒） | 证据 |
| --- | --- | --- | --- | --- |
| 1199098 | 2026-10-15 12:26:09 | 2026-10-15 17:20:59 | 17690 | [raw/1199098_result_meta.json:1](raw/1199098_result_meta.json#L1) |
| 1178133 | 2026-09-17 22:27:47 | 2026-09-18 03:15:43 | 17276 | [raw/1178133_result_meta.json:1](raw/1178133_result_meta.json#L1) |

Profiling 时间跨度多 **414 秒**。它与 Quickbuild 总时长是不同字段，未混合使用。[raw/analysis_summary.jsonl:5](raw/analysis_summary.jsonl#L5)。

页面起止字符串未声明时区，本文保留原文。Rust 优化侧 Profiling 起始为 `2026-10-15 12:26:09`，完整包日志起始为 `2026-10-15 03:26:09 UTC`；基线分别为 `2026-09-17 22:27:47` 与 `2026-09-17 13:27:47 UTC`。这些时钟表示未统一，未用它们交叉计算等待时间。[raw/1199098_buildtime.pretty.json:5312–5321](raw/1199098_buildtime.pretty.json#L5312)；[raw/1199098_buildtime.json:1](raw/1199098_buildtime.json#L1) key=rust；[raw/1199098_armv7l_rust-1.90.0-1.txt:6](raw/1199098_armv7l_rust-1.90.0-1.txt#L6)；[raw/1178133_buildtime.pretty.json:5312–5321](raw/1178133_buildtime.pretty.json#L5312)；[raw/1178133_buildtime.json:1](raw/1178133_buildtime.json#L1) key=rust；[raw/1178133_armv7l_rust-1.90.0-1.txt:6](raw/1178133_armv7l_rust-1.90.0-1.txt#L6)。

两侧各自按实际耗时降序的前 30 个包见 [top30.csv](top30.csv)，每行保留原始来源；全表见 [per_package.csv](per_package.csv)，共同包对比见 [compare.csv](compare.csv)。Profiling duration 是包从开始到结束的日志/打包跨度，包含 buildroot 准备与 RPM 处理；不是单独编译 CPU 时间。Rust 日志边界可核对这一口径：[raw/1199098_armv7l_rust-1.90.0-1.txt:6](raw/1199098_armv7l_rust-1.90.0-1.txt#L6)、[raw/1199098_armv7l_rust-1.90.0-1.txt:416–435](raw/1199098_armv7l_rust-1.90.0-1.txt#L416)、[raw/1199098_armv7l_rust-1.90.0-1.txt:656](raw/1199098_armv7l_rust-1.90.0-1.txt#L656)。

已获取的仓库/架构整体窗口仅为上表的 Unified/standard/armv7l。Unified 的 x86_64、aarch64 两组对应构建未获取，原因是给定 ID 只覆盖 armv7l。关联 Base 快照虽列出架构，但没有整体开始/结束字段；其 Profiling 路径返回 HTTP 404，整体时间及等待/调度时间均未获取，未把单个 LLVM 包的时间当成整个 Base 构建。[raw/1199098_base_build.xml:3–18](raw/1199098_base_build.xml#L3)；[raw/1178133_base_build.xml:3–18](raw/1178133_base_build.xml#L3)；[raw/1199098_base_builddata_profiling_reports_:1–10](raw/1199098_base_builddata_profiling_reports_#L1)；[raw/1178133_base_builddata_profiling_reports_:1–10](raw/1178133_base_builddata_profiling_reports_#L1)。

## llvm 包（来源分支与修复）

两个 Unified 包列表均没有 llvm，因此这两个 Unified ID 中未重新构建 llvm。关联 Base 快照各架构有完整 LLVM 构建日志，版本与 UTC 起止如下。耗时取日志文本 `finished-start` 的精确秒差；行首终值另保留于 [llvm_builds.csv](llvm_builds.csv)。[raw/1199098_buildtime.json:1](raw/1199098_buildtime.json#L1)；[raw/1178133_buildtime.json:1](raw/1178133_buildtime.json#L1)。

| 关联 Unified ID | Base 架构 | 版本-release | 开始 UTC | 结束 UTC | 秒 | 证据 |
| --- | --- | --- | --- | --- | --- | --- |
| 1199098 | x86_64 | 22.1.8-3.1 | 2026-10-14T07:04:31Z | 2026-10-14T15:22:15Z | 29864 | [raw/1199098_base_x86_64_llvm.txt:6](raw/1199098_base_x86_64_llvm.txt#L6)；[raw/1199098_base_x86_64_llvm.txt:17839](raw/1199098_base_x86_64_llvm.txt#L17839)；[raw/1199098_base_x86_64_llvm.txt:17359](raw/1199098_base_x86_64_llvm.txt#L17359) |
| 1199098 | armv7l | 22.1.8-3.1 | 2026-10-14T07:04:31Z | 2026-10-14T08:17:53Z | 4402 | [raw/1199098_base_armv7l_llvm.txt:6](raw/1199098_base_armv7l_llvm.txt#L6)；[raw/1199098_base_armv7l_llvm.txt:19703](raw/1199098_base_armv7l_llvm.txt#L19703)；[raw/1199098_base_armv7l_llvm.txt:19241](raw/1199098_base_armv7l_llvm.txt#L19241) |
| 1199098 | aarch64 | 22.1.8-3.1 | 2026-10-14T07:04:31Z | 2026-10-14T08:34:05Z | 5374 | [raw/1199098_base_aarch64_llvm.txt:6](raw/1199098_base_aarch64_llvm.txt#L6)；[raw/1199098_base_aarch64_llvm.txt:20614](raw/1199098_base_aarch64_llvm.txt#L20614)；[raw/1199098_base_aarch64_llvm.txt:20142](raw/1199098_base_aarch64_llvm.txt#L20142) |
| 1178133 | x86_64 | 22.1.8-1.6 | 2026-09-12T16:12:04Z | 2026-09-12T17:46:50Z | 5686 | [raw/1178133_base_x86_64_llvm.txt:6](raw/1178133_base_x86_64_llvm.txt#L6)；[raw/1178133_base_x86_64_llvm.txt:17356](raw/1178133_base_x86_64_llvm.txt#L17356)；[raw/1178133_base_x86_64_llvm.txt:16876](raw/1178133_base_x86_64_llvm.txt#L16876) |
| 1178133 | armv7l | 22.1.8-1.7 | 2026-09-12T18:02:00Z | 2026-09-12T19:32:58Z | 5458 | [raw/1178133_base_armv7l_llvm.txt:6](raw/1178133_base_armv7l_llvm.txt#L6)；[raw/1178133_base_armv7l_llvm.txt:15997](raw/1178133_base_armv7l_llvm.txt#L15997)；[raw/1178133_base_armv7l_llvm.txt:15535](raw/1178133_base_armv7l_llvm.txt#L15535) |
| 1178133 | aarch64 | 22.1.8-1.9 | 2026-09-12T22:03:11Z | 2026-09-12T23:21:10Z | 4679 | [raw/1178133_base_aarch64_llvm.txt:6](raw/1178133_base_aarch64_llvm.txt#L6)；[raw/1178133_base_aarch64_llvm.txt:16894](raw/1178133_base_aarch64_llvm.txt#L16894)；[raw/1178133_base_aarch64_llvm.txt:16422](raw/1178133_base_aarch64_llvm.txt#L16422) |

基线 armv7l 的 `started` 行首为 `[1s]`、`finished` 行首为 `[5459s]`，明确 UTC 时间差为 `5458` 秒；CSV 同时保存两种原始表示，未把行首终值直接当作 UTC 差值。[raw/1178133_base_armv7l_llvm.txt:6](raw/1178133_base_armv7l_llvm.txt#L6)；[raw/1178133_base_armv7l_llvm.txt:15997](raw/1178133_base_armv7l_llvm.txt#L15997)。

优化 Base manifest 的 LLVM revision 是 `67619ec8bbbac7238a6cfc33a481ccfbcd12206f`；基线是 `8dfebafe1a477b3dcc678ee4cb18a3a4306d5a7c`。[raw/1199098_base_manifest.xml:108](raw/1199098_base_manifest.xml#L108)；[raw/1178133_base_manifest.xml:109](raw/1178133_base_manifest.xml#L109)。优化提交的官方 Git 页面标注分支 `tizen_base`，提交标题为 `packaging: fix llvm-static-devel with ThinLTO`。[raw/llvm_67619ec8_commit.cgit.html:175–178](raw/llvm_67619ec8_commit.cgit.html#L175)。**构建时 checkout 的分支参数未获取**：当前已获取的 snapshot manifest 给的是 revision，LLVM 包日志给的是 srcmd5，不能用 Git 页面当前分支标记替代构建命令中的分支参数。[raw/1199098_base_x86_64_llvm.txt:8](raw/1199098_base_x86_64_llvm.txt#L8)。

该精确提交包含 x86_64 静态归档修复：spec 声明 `Source1005: llvm-static-archives-native.py`，并在 `%ifarch x86_64` 条件内调用 `python3 %{SOURCE1005}`、`--arch x86_64`。[raw/llvm_67619ec8_llvm_spec.cgit.txt:47](raw/llvm_67619ec8_llvm_spec.cgit.txt#L47)；[raw/llvm_67619ec8_llvm_spec.cgit.txt:429–441](raw/llvm_67619ec8_llvm_spec.cgit.txt#L429)。对应构建日志实际执行了该脚本，并输出 `NATIVE_ARCHIVES_BEGIN` 与逐档转换结果。[raw/1199098_base_x86_64_llvm.txt:16309–16313](raw/1199098_base_x86_64_llvm.txt#L16309)。原始提交补丁保存在 [raw/llvm_67619ec8_fix.patch](raw/llvm_67619ec8_fix.patch)，原始 spec 保存在 raw，脚本新增正文在该完整补丁中；独立脚本源码接口本次返回 HTTP 502，响应体也已保留，未当成源码（[raw/fetch_manifest.jsonl:96](raw/fetch_manifest.jsonl#L96)）。没有在本机执行该补丁或脚本。该 spec 的转换调用条件只列 x86_64。

qemu-accel 同样不在两个 Unified 构建的包列表中。优化关联 Base 快照有新的 `qemu-accel-armv7l` / `qemu-accel-aarch64` 构建记录；基线记录一并列出。这里的构建架构是 x86_64，目标架构由 spec 名区分；详细版本输出见 [qemu_builds.csv](qemu_builds.csv)。

| 关联 ID | 目标架构 | 开始 UTC | 结束 UTC | 秒 | 证据 |
| --- | --- | --- | --- | --- | --- |
| 1199098 | armv7l | 2026-10-14T17:18:03Z | 2026-10-14T17:35:22Z | 1039 | [raw/1199098_base_x86_64_qemu-accel-armv7l.txt:6](raw/1199098_base_x86_64_qemu-accel-armv7l.txt#L6)；[raw/1199098_base_x86_64_qemu-accel-armv7l.txt:3128](raw/1199098_base_x86_64_qemu-accel-armv7l.txt#L3128)；[raw/1199098_base_x86_64_qemu-accel-armv7l.txt:2726](raw/1199098_base_x86_64_qemu-accel-armv7l.txt#L2726)；[raw/1199098_base_x86_64_qemu-accel-armv7l.txt:2899](raw/1199098_base_x86_64_qemu-accel-armv7l.txt#L2899) |
| 1199098 | aarch64 | 2026-10-14T17:18:03Z | 2026-10-14T17:35:26Z | 1043 | [raw/1199098_base_x86_64_qemu-accel-aarch64.txt:6](raw/1199098_base_x86_64_qemu-accel-aarch64.txt#L6)；[raw/1199098_base_x86_64_qemu-accel-aarch64.txt:3125](raw/1199098_base_x86_64_qemu-accel-aarch64.txt#L3125)；[raw/1199098_base_x86_64_qemu-accel-aarch64.txt:2723](raw/1199098_base_x86_64_qemu-accel-aarch64.txt#L2723)；[raw/1199098_base_x86_64_qemu-accel-aarch64.txt:2896](raw/1199098_base_x86_64_qemu-accel-aarch64.txt#L2896) |
| 1178133 | armv7l | 2026-09-12T18:57:25Z | 2026-09-12T19:01:35Z | 250 | [raw/1178133_base_x86_64_qemu-accel-armv7l.txt:6](raw/1178133_base_x86_64_qemu-accel-armv7l.txt#L6)；[raw/1178133_base_x86_64_qemu-accel-armv7l.txt:3151](raw/1178133_base_x86_64_qemu-accel-armv7l.txt#L3151)；[raw/1178133_base_x86_64_qemu-accel-armv7l.txt:2747](raw/1178133_base_x86_64_qemu-accel-armv7l.txt#L2747)；[raw/1178133_base_x86_64_qemu-accel-armv7l.txt:2920](raw/1178133_base_x86_64_qemu-accel-armv7l.txt#L2920) |
| 1178133 | aarch64 | 2026-09-12T18:58:49Z | 2026-09-12T19:02:25Z | 216 | [raw/1178133_base_x86_64_qemu-accel-aarch64.txt:6](raw/1178133_base_x86_64_qemu-accel-aarch64.txt#L6)；[raw/1178133_base_x86_64_qemu-accel-aarch64.txt:3147](raw/1178133_base_x86_64_qemu-accel-aarch64.txt#L3147)；[raw/1178133_base_x86_64_qemu-accel-aarch64.txt:2743](raw/1178133_base_x86_64_qemu-accel-aarch64.txt#L2743)；[raw/1178133_base_x86_64_qemu-accel-aarch64.txt:2916](raw/1178133_base_x86_64_qemu-accel-aarch64.txt#L2916) |

## 下游实际使用的编译器与链接器

安装/keeping 列表、版本、编译器行和链接器行见 [downstream_toolchains.csv](downstream_toolchains.csv)。`keeping` 表示日志保留的已装包，不是此次新安装。`lldb` 与 `lld` 按不同名称处理；样本的完整安装列表未列独立 `lld-*` RPM，所以其独立安装版本写“未获取”，也不据此判断 buildroot 中是否存在 lld 可执行文件。

| 关联 ID / 来源 | 架构 / 样本 | LLVM / clang 安装版本 | qemu-accel | 编译器与链接器记录 | 证据 |
| --- | --- | --- | --- | --- | --- |
| 1199098 / Unified | armv7l / libinput | llvm-22.1.8-3.1 / clang-22.1.8-3.1 | qemu-accel-x86_64-armv7l-0.4-2.2 | [   35s] C compiler for the host machine: armv7l-tizen-linux-gnueabi-clang (clang 22.1.8 "clang version 22.1.8")；ld.bfd | [raw/1199098_armv7l_libinput-1.31.3-0.txt:178](raw/1199098_armv7l_libinput-1.31.3-0.txt#L178)；[raw/1199098_armv7l_libinput-1.31.3-0.txt:180](raw/1199098_armv7l_libinput-1.31.3-0.txt#L180)；[raw/1199098_armv7l_libinput-1.31.3-0.txt:152](raw/1199098_armv7l_libinput-1.31.3-0.txt#L152)；[raw/1199098_armv7l_libinput-1.31.3-0.txt:291](raw/1199098_armv7l_libinput-1.31.3-0.txt#L291)；[raw/1199098_armv7l_libinput-1.31.3-0.txt:292](raw/1199098_armv7l_libinput-1.31.3-0.txt#L292)；[raw/1199098_armv7l_libinput-1.31.3-0.txt:294](raw/1199098_armv7l_libinput-1.31.3-0.txt#L294) |
| 1199098 / Base snapshot | x86_64 / libdrm | llvm-22.1.8-2.3 / clang-22.1.8-2.3 | 未获取 | [  134s] C compiler for the host machine: x86_64-tizen-linux-gnu-clang (clang 22.1.8 "clang version 22.1.8")；ld.bfd | [raw/1199098_base_x86_64_libdrm.txt:164](raw/1199098_base_x86_64_libdrm.txt#L164)；[raw/1199098_base_x86_64_libdrm.txt:169](raw/1199098_base_x86_64_libdrm.txt#L169)；[raw/1199098_base_x86_64_libdrm.txt:1–941](raw/1199098_base_x86_64_libdrm.txt#L1)（完整包列表未列出该独立包名）；[raw/1199098_base_x86_64_libdrm.txt:387](raw/1199098_base_x86_64_libdrm.txt#L387)；[raw/1199098_base_x86_64_libdrm.txt:388](raw/1199098_base_x86_64_libdrm.txt#L388) |
| 1199098 / Base snapshot | armv7l / libdrm | llvm-22.1.8-2.3 / clang-22.1.8-2.3 | qemu-accel-x86_64-armv7l-0.4-1.1 | [  228s] C compiler for the host machine: armv7l-tizen-linux-gnueabi-clang (clang 22.1.8 "clang version 22.1.8")；ld.bfd | [raw/1199098_base_armv7l_libdrm.txt:188](raw/1199098_base_armv7l_libdrm.txt#L188)；[raw/1199098_base_armv7l_libdrm.txt:190](raw/1199098_base_armv7l_libdrm.txt#L190)；[raw/1199098_base_armv7l_libdrm.txt:168](raw/1199098_base_armv7l_libdrm.txt#L168)；[raw/1199098_base_armv7l_libdrm.txt:410](raw/1199098_base_armv7l_libdrm.txt#L410)；[raw/1199098_base_armv7l_libdrm.txt:411](raw/1199098_base_armv7l_libdrm.txt#L411) |
| 1199098 / Base snapshot | aarch64 / libdrm | llvm-22.1.8-2.3 / clang-22.1.8-2.3 | qemu-accel-x86_64-aarch64-0.4-1.1 | [  129s] C compiler for the host machine: aarch64-tizen-linux-gnu-clang (clang 22.1.8 "clang version 22.1.8")；ld.bfd | [raw/1199098_base_aarch64_libdrm.txt:191](raw/1199098_base_aarch64_libdrm.txt#L191)；[raw/1199098_base_aarch64_libdrm.txt:194](raw/1199098_base_aarch64_libdrm.txt#L194)；[raw/1199098_base_aarch64_libdrm.txt:179](raw/1199098_base_aarch64_libdrm.txt#L179)；[raw/1199098_base_aarch64_libdrm.txt:413](raw/1199098_base_aarch64_libdrm.txt#L413)；[raw/1199098_base_aarch64_libdrm.txt:414](raw/1199098_base_aarch64_libdrm.txt#L414) |
| 1178133 / Unified | armv7l / libinput | llvm-22.1.8-1.7 / clang-22.1.8-1.7 | qemu-accel-x86_64-armv7l-0.4-1.1 | [   41s] C compiler for the host machine: armv7l-tizen-linux-gnueabi-clang (clang 22.1.8 "clang version 22.1.8")；ld.bfd | [raw/1178133_armv7l_libinput-1.31.3-0.txt:196](raw/1178133_armv7l_libinput-1.31.3-0.txt#L196)；[raw/1178133_armv7l_libinput-1.31.3-0.txt:198](raw/1178133_armv7l_libinput-1.31.3-0.txt#L198)；[raw/1178133_armv7l_libinput-1.31.3-0.txt:170](raw/1178133_armv7l_libinput-1.31.3-0.txt#L170)；[raw/1178133_armv7l_libinput-1.31.3-0.txt:309](raw/1178133_armv7l_libinput-1.31.3-0.txt#L309)；[raw/1178133_armv7l_libinput-1.31.3-0.txt:310](raw/1178133_armv7l_libinput-1.31.3-0.txt#L310)；[raw/1178133_armv7l_libinput-1.31.3-0.txt:312](raw/1178133_armv7l_libinput-1.31.3-0.txt#L312) |
| 1178133 / Base snapshot | x86_64 / libdrm | llvm-22.1.8-1.6 / clang-22.1.8-1.6 | 未获取 | [  111s] C compiler for the host machine: x86_64-tizen-linux-gnu-clang (clang 22.1.8 "clang version 22.1.8")；ld.bfd | [raw/1178133_base_x86_64_libdrm.txt:179](raw/1178133_base_x86_64_libdrm.txt#L179)；[raw/1178133_base_x86_64_libdrm.txt:182](raw/1178133_base_x86_64_libdrm.txt#L182)；[raw/1178133_base_x86_64_libdrm.txt:1–938](raw/1178133_base_x86_64_libdrm.txt#L1)（完整包列表未列出该独立包名）；[raw/1178133_base_x86_64_libdrm.txt:398](raw/1178133_base_x86_64_libdrm.txt#L398)；[raw/1178133_base_x86_64_libdrm.txt:399](raw/1178133_base_x86_64_libdrm.txt#L399) |
| 1178133 / Base snapshot | armv7l / libdrm | llvm-22.1.8-1.7 / clang-22.1.8-1.7 | qemu-accel-x86_64-armv7l-0.4-1.1 | [   65s] C compiler for the host machine: armv7l-tizen-linux-gnueabi-clang (clang 22.1.8 "clang version 22.1.8")；ld.bfd | [raw/1178133_base_armv7l_libdrm.txt:192](raw/1178133_base_armv7l_libdrm.txt#L192)；[raw/1178133_base_armv7l_libdrm.txt:194](raw/1178133_base_armv7l_libdrm.txt#L194)；[raw/1178133_base_armv7l_libdrm.txt:172](raw/1178133_base_armv7l_libdrm.txt#L172)；[raw/1178133_base_armv7l_libdrm.txt:417](raw/1178133_base_armv7l_libdrm.txt#L417)；[raw/1178133_base_armv7l_libdrm.txt:418](raw/1178133_base_armv7l_libdrm.txt#L418) |
| 1178133 / Base snapshot | aarch64 / libdrm | llvm-22.1.8-1.9 / clang-22.1.8-1.9 | qemu-accel-x86_64-aarch64-0.4-1.1 | [   93s] C compiler for the host machine: aarch64-tizen-linux-gnu-clang (clang 22.1.8 "clang version 22.1.8")；ld.bfd | [raw/1178133_base_aarch64_libdrm.txt:195](raw/1178133_base_aarch64_libdrm.txt#L195)；[raw/1178133_base_aarch64_libdrm.txt:198](raw/1178133_base_aarch64_libdrm.txt#L198)；[raw/1178133_base_aarch64_libdrm.txt:183](raw/1178133_base_aarch64_libdrm.txt#L183)；[raw/1178133_base_aarch64_libdrm.txt:420](raw/1178133_base_aarch64_libdrm.txt#L420)；[raw/1178133_base_aarch64_libdrm.txt:421](raw/1178133_base_aarch64_libdrm.txt#L421) |

当前 Unified/armv7l 的 libinput 两边都明确记录 `ld.bfd 2.43`，并有 `Linking target` 行。[raw/1199098_armv7l_libinput-1.31.3-0.txt:291–294](raw/1199098_armv7l_libinput-1.31.3-0.txt#L291)；[raw/1178133_armv7l_libinput-1.31.3-0.txt:309–312](raw/1178133_armv7l_libinput-1.31.3-0.txt#L309)。表中的 Base/libdrm 日志只证明其自身构建环境：优化快照内 x86_64 日志始于 `2026-09-24 20:19:41 UTC`，安装 LLVM `22.1.8-2.3`，并非快照中 LLVM RPM 的 `22.1.8-3.1`。[raw/1199098_base_x86_64_libdrm.txt:6](raw/1199098_base_x86_64_libdrm.txt#L6)；[raw/1199098_base_x86_64_libdrm.txt:164](raw/1199098_base_x86_64_libdrm.txt#L164)；[raw/1199098_base_packages_x86_64.html:365](raw/1199098_base_packages_x86_64.html#L365)。其余样本也各自保留日志起始时间，未把快照发布时间当成每个包的构建时间。

为补充使用新 LLVM 的实际安装记录，各架构 Base/zlib 完整日志也已保存。优化侧 zlib 的安装清单列出 LLVM/clang `22.1.8-3.1`；它们仅明确探测 `/usr/bin/ld` 为 GNU ld，未给出可直接归档为 ld.bfd/lld 的实际可执行名称，因此 CSV 保留“未获取”及原探测行。

- x86_64：llvm-22.1.8-3.1 / clang-22.1.8-3.1；[raw/1199098_base_x86_64_zlib.txt:159](raw/1199098_base_x86_64_zlib.txt#L159)；[raw/1199098_base_x86_64_zlib.txt:162](raw/1199098_base_x86_64_zlib.txt#L162)；[raw/1199098_base_x86_64_zlib.txt:460](raw/1199098_base_x86_64_zlib.txt#L460)。
- armv7l：llvm-22.1.8-3.1 / clang-22.1.8-3.1；[raw/1199098_base_armv7l_zlib.txt:178](raw/1199098_base_armv7l_zlib.txt#L178)；[raw/1199098_base_armv7l_zlib.txt:180](raw/1199098_base_armv7l_zlib.txt#L180)；[raw/1199098_base_armv7l_zlib.txt:481](raw/1199098_base_armv7l_zlib.txt#L481)。
- aarch64：llvm-22.1.8-3.1 / clang-22.1.8-3.1；[raw/1199098_base_aarch64_zlib.txt:182](raw/1199098_base_aarch64_zlib.txt#L182)；[raw/1199098_base_aarch64_zlib.txt:185](raw/1199098_base_aarch64_zlib.txt#L185)；[raw/1199098_base_aarch64_zlib.txt:486](raw/1199098_base_aarch64_zlib.txt#L486)。

## rust 两边对比

armv7l 两侧均为 `rust-1.90.0-1`，Profiling 实际耗时分别 **1650 秒、792 秒**，差 **858 秒**，精确比值 **25/12**（显示为 `2.08333333333`）。[raw/1199098_buildtime.pretty.json:5312–5321](raw/1199098_buildtime.pretty.json#L5312)；[raw/1199098_buildtime.json:1](raw/1199098_buildtime.json#L1) key=rust；[raw/1178133_buildtime.pretty.json:5312–5321](raw/1178133_buildtime.pretty.json#L5312)；[raw/1178133_buildtime.json:1](raw/1178133_buildtime.json#L1) key=rust。完整日志分别为 [优化侧](raw/1199098_armv7l_rust-1.90.0-1.txt) 和 [基线](raw/1178133_armv7l_rust-1.90.0-1.txt)。

| 检查项 | 优化侧 armv7l | 基线 armv7l | 证据 |
| --- | --- | --- | --- |
| llvm-devel / libllvm 安装版本 | 22.1.8-3.1 / 22.1.8-3.1 | 22.1.8-1.7 / 22.1.8-1.7 | [raw/1199098_armv7l_rust-1.90.0-1.txt:262](raw/1199098_armv7l_rust-1.90.0-1.txt#L262)；[raw/1199098_armv7l_rust-1.90.0-1.txt:298](raw/1199098_armv7l_rust-1.90.0-1.txt#L298)；[raw/1178133_armv7l_rust-1.90.0-1.txt:262](raw/1178133_armv7l_rust-1.90.0-1.txt#L262)；[raw/1178133_armv7l_rust-1.90.0-1.txt:298](raw/1178133_armv7l_rust-1.90.0-1.txt#L298) |
| llvm-static-devel | 未获取：完整安装清单未列此独立包名 | 同左 | [raw/rust_log_queries.jsonl:1](raw/rust_log_queries.jsonl#L1)；[raw/rust_log_queries.jsonl:6](raw/rust_log_queries.jsonl#L6) |
| 系统或自带 LLVM | 未获取：没有构建 rustc 的 LLVM 配置 | 同左 | [raw/rust_log_queries.jsonl:2](raw/rust_log_queries.jsonl#L2)；[raw/rust_log_queries.jsonl:7](raw/rust_log_queries.jsonl#L7) |
| LLVM 静态/动态链接 | 未获取：没有 link-shared / llvm-config 调用 | 同左 | [raw/rust_log_queries.jsonl:2](raw/rust_log_queries.jsonl#L2)；[raw/rust_log_queries.jsonl:7](raw/rust_log_queries.jsonl#L7) |
| 链接 rustc 的链接器 | 未获取：未见 rustc 链接命令 | 同左 | [raw/rust_log_queries.jsonl:4](raw/rust_log_queries.jsonl#L4)；[raw/rust_log_queries.jsonl:9](raw/rust_log_queries.jsonl#L9) |
| bootstrap 各阶段耗时 | 未获取：未见 bootstrap 阶段行 | 同左 | [raw/rust_log_queries.jsonl:3](raw/rust_log_queries.jsonl#L3)；[raw/rust_log_queries.jsonl:8](raw/rust_log_queries.jsonl#L8) |

两边 `%build` 记录设置环境变量后 `exit 0`，`%install` 则解包 `rust-1.90.0-arm-unknown-linux-gnueabi.tar.xz` 并执行 `./install.sh --components=rustc,rust-std-arm-unknown-linux-gnueabi,cargo,clippy-preview`。本次日志记录的是这些预编译组件的安装，未提供这些组件最初生成时的 LLVM 配置或 rustc 链接命令。[raw/1199098_armv7l_rust-1.90.0-1.txt:435–485](raw/1199098_armv7l_rust-1.90.0-1.txt#L435)；[raw/1178133_armv7l_rust-1.90.0-1.txt:435–485](raw/1178133_armv7l_rust-1.90.0-1.txt#L435)。`rust-lld` / `ld.lld` 的打包文件警告不是链接 rustc 时选择该链接器的证据。[raw/1199098_armv7l_rust-1.90.0-1.txt:552–556](raw/1199098_armv7l_rust-1.90.0-1.txt#L552)。

每侧相邻日志行时间戳差最大的 15 处完整列于 [rust_timestamp_gaps.csv](rust_timestamp_gaps.csv)：行号、前后秒数、精确差值和两行原文都保留。严格比较相邻物理行，要求两行都以 `[ NNNs ]` 开头；按间隔降序、前行号升序排序；没有把时间差归因到某个动作。每侧最大的三处如下。

| 构建 | 差值秒 | 前行原文 | 后行原文 | 证据 |
| --- | --- | --- | --- | --- |
| 1199098 | 351 | `[  725s] build-compare-2023.06.18-1.4          ########################################` | `[ 1076s] clang-accel-x86_64-armv7l-0.4-2.2     ########################################` | [raw/1199098_armv7l_rust-1.90.0-1.txt:385–386](raw/1199098_armv7l_rust-1.90.0-1.txt#L385) |
| 1199098 | 316 | `[  210s] [30/46] preinstalling clang-accel-x86_64-armv7l...` | `[  526s] [31/46] preinstalling qemu-accel-x86_64-armv7l...` | [raw/1199098_armv7l_rust-1.90.0-1.txt:161–162](raw/1199098_armv7l_rust-1.90.0-1.txt#L161) |
| 1199098 | 167 | `[    5s] [12/108] downloading http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261015.022255/repos/standard/packages/armv7l/clang-accel-x86_64-armv7l-0.4-2.2.armv7l.rpm ... ` | `[  172s] [13/108] downloading http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261015.022255/repos/standard/packages/armv7l/coreutils-6.9-14.2.armv7l.rpm ... ` | [raw/1199098_armv7l_rust-1.90.0-1.txt:32–33](raw/1199098_armv7l_rust-1.90.0-1.txt#L32) |
| 1178133 | 108 | `[  413s] Checking for unpackaged file(s): /usr/lib/rpm/check-files /home/abuild/rpmbuild/BUILDROOT/rust-1.90.0-1.arm` | `[  521s] Wrote: /home/abuild/rpmbuild/SRPMS/rust-1.90.0-1.src.rpm` | [raw/1178133_armv7l_rust-1.90.0-1.txt:639–640](raw/1178133_armv7l_rust-1.90.0-1.txt#L639) |
| 1178133 | 85 | `[  521s] Wrote: /home/abuild/rpmbuild/SRPMS/rust-1.90.0-1.src.rpm` | `[  606s] Wrote: /home/abuild/rpmbuild/RPMS/armv7l/rust-1.90.0-1.armv7l.rpm` | [raw/1178133_armv7l_rust-1.90.0-1.txt:640–641](raw/1178133_armv7l_rust-1.90.0-1.txt#L640) |
| 1178133 | 78 | `[  624s] Wrote: /home/abuild/rpmbuild/RPMS/armv7l/rust-std-shared-1.90.0-1.armv7l.rpm` | `[  702s] Wrote: /home/abuild/rpmbuild/RPMS/armv7l/rust-devel-1.90.0-1.armv7l.rpm` | [raw/1178133_armv7l_rust-1.90.0-1.txt:642–643](raw/1178133_armv7l_rust-1.90.0-1.txt#L642) |

[RPM 阶段边界表](rust_phase_boundaries.csv) 只保存 `%prep/%build/%install/%clean` 的时间戳，不将这些称为 bootstrap 耗时。两个构建的 x86_64、aarch64 Rust 日志、版本、耗时及链接配置均**未获取**：给定 Unified ID 只构建 armv7l，补充的是 Base 快照，没有同组其他架构的 Unified 构建 ID。逐项状态见 [rust_review.csv](rust_review.csv)。

## 静态库扫描

下载来源是 Unified 日志实际引用、用户随后确认的两个 Base 快照。CSV 的 `build` 是关联 Unified ID，不表示 RPM 由该 Unified 构建产出。三种架构的 RPM 链接及大小原文在对应 `raw/*_base_packages_<arch>.html`，下载 SHA 与 URL 在 `raw/fetch_manifest.jsonl`，RPM 包头身份在 [raw/rpm_metadata.txt](raw/rpm_metadata.txt)。RPM 和解包后的 `.a` 仅存于仓库 `temp/qb_1199098_vs_1178133/`，没有提交。

| 关联 ID | 架构 | .a 数量 | bitcode 成员 | ELF 成员 | 其他成员 | 扫描证据 |
| --- | --- | --- | --- | --- | --- | --- |
| 1199098 | x86_64 | 225 | 0 | 3864 | 0 | [raw/static_archive_scan.csv:2–226](raw/static_archive_scan.csv#L2) |
| 1199098 | armv7l | 210 | 3683 | 7 | 0 | [raw/static_archive_scan.csv:227–436](raw/static_archive_scan.csv#L227) |
| 1199098 | aarch64 | 212 | 3699 | 7 | 0 | [raw/static_archive_scan.csv:437–648](raw/static_archive_scan.csv#L437) |
| 1178133 | x86_64 | 225 | 0 | 3864 | 0 | [raw/static_archive_scan.csv:649–873](raw/static_archive_scan.csv#L649) |
| 1178133 | armv7l | 210 | 0 | 3690 | 0 | [raw/static_archive_scan.csv:874–1083](raw/static_archive_scan.csv#L874) |
| 1178133 | aarch64 | 212 | 0 | 3706 | 0 | [raw/static_archive_scan.csv:1084–1295](raw/static_archive_scan.csv#L1084) |

逐 `.a` 统计见 [raw/static_archive_scan.csv](raw/static_archive_scan.csv)。每个成员的原始前四字节、成员名、次序及分类见 [raw/static_archive_members.jsonl](raw/static_archive_members.jsonl)，每行扫描结果引用其成员记录行范围。识别规则：`42 43 c0 de` 或 `de c0 17 0b` 为 LLVM bitcode；`7f 45 4c 46` 为 ELF；ar 符号表和长文件名表不计为成员。保留重复成员名，以序号分别计数；没有编译或转换归档。所有 ELF 成员还单独读取了 ELF e_type，均为 ET_REL；逐档检查记录见 [raw/static_elf_type_check.jsonl](raw/static_elf_type_check.jsonl)。统计与完整性检查见 [raw/validation.json](raw/validation.json)，方法见 [raw/scan_method.txt](raw/scan_method.txt)。

## 两次构建是否同条件

以下仅列相同项与不同项，不将差异解释为因果。

- 两侧 Profiling JSON 各有 **1029** 个条目，HTML 成功列表及 metadata 各报 **1030** 个包。共同缺项是 `rust-value-bag`。[raw/analysis_summary.jsonl:1–2](raw/analysis_summary.jsonl#L1)。已从完整包日志补上此包：优化侧 UTC `finished-start=30` 秒，基线 `39` 秒；CSV 明确标记为日志回填，未伪称页面有这行。[raw/1199098_armv7l_rust-value-bag-1.0.0_9-1.txt:6](raw/1199098_armv7l_rust-value-bag-1.0.0_9-1.txt#L6)；[raw/1199098_armv7l_rust-value-bag-1.0.0_9-1.txt:347](raw/1199098_armv7l_rust-value-bag-1.0.0_9-1.txt#L347)；[raw/1178133_armv7l_rust-value-bag-1.0.0_9-1.txt:6](raw/1178133_armv7l_rust-value-bag-1.0.0_9-1.txt#L6)；[raw/1178133_armv7l_rust-value-bag-1.0.0_9-1.txt:332](raw/1178133_armv7l_rust-value-bag-1.0.0_9-1.txt#L332)。覆盖明细见 [profiling_coverage.csv](profiling_coverage.csv)。
- 按仓库、架构、包名配对，**1030** 个共同包，版本-release 不同的包 **0** 个，仅一边出现的包 **0** 个；后两份 CSV 保留表头、没有数据行。[raw/analysis_summary.jsonl:3](raw/analysis_summary.jsonl#L3)；[version_differences.csv](version_differences.csv)；[only_in_one.csv](only_in_one.csv)。版本字符串相同不代表所有构建输入相同。
- Quickbuild `build_pkg_list_dic` 的项目到提交映射相同，逐条见 [source_revisions.csv](source_revisions.csv)。[raw/1199098_quickbuild.txt:130](raw/1199098_quickbuild.txt#L130)；[raw/1178133_quickbuild.txt:134](raw/1178133_quickbuild.txt#L134)；[raw/analysis_summary.jsonl:6](raw/analysis_summary.jsonl#L6)。
- Base 输入分别是 `20261015.022255` 与 `20260914.073422`；Unified 参考仓库分别是 `20260917.132101` 与 `20260814.092727`。[raw/1199098_quickbuild.txt:338–347](raw/1199098_quickbuild.txt#L338)；[raw/1178133_quickbuild.txt:338–347](raw/1178133_quickbuild.txt#L338)。
- 两侧都设置 `--threads=30`、`jobs 8`、`_smp_mflags -j8`、`_costomized_smp_mflags -j20`；外层 timeout 分别为 `8h` 和 `6h`。Profiling/reorder 参考地址不同。[raw/1199098_quickbuild.txt:431–432](raw/1199098_quickbuild.txt#L431)；[raw/1178133_quickbuild.txt:430–431](raw/1178133_quickbuild.txt#L430)。
- Worker 名不同：优化侧 Rust 为 `ip-192-168-56-28:5`，基线为 `ip-192-168-56-144:5`，各包 worker 在 per_package.csv 中保留；未取得两台机器相同硬件、负载、缓存状态或调度等待的证据。[raw/1199098_buildtime.pretty.json:5312–5321](raw/1199098_buildtime.pretty.json#L5312)；[raw/1199098_buildtime.json:1](raw/1199098_buildtime.json#L1) key=rust；[raw/1178133_buildtime.pretty.json:5312–5321](raw/1178133_buildtime.pretty.json#L5312)；[raw/1178133_buildtime.json:1](raw/1178133_buildtime.json#L1) key=rust。
- 下游实际安装的 LLVM、clang、qemu-accel 版本存在差异，详见上节；Base 快照包含早于快照发布日的下游构建日志，不能把同一快照内所有日志视作同一次全量重建。

未获取项均保留原因；没有用估计值补齐。此次只下载、解包、读取文件头和做文本统计；没有修改产品源码、spec 或补丁，没有编译、运行归档转换脚本或向 Gerrit 提交。
