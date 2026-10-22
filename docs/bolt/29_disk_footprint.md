# 29：BOLT 磁盘占用盘点与同条件补测准入

更新：2026-10-22，Asia/Shanghai。状态：**第一步完成历史盘点与输入准备；完整补测未启动，清理及其验证未执行。**

目前还不能给出开启 BOLT 比关闭开关多出的完整构建峰值。已有一次未跑完的安装演练，当前保留的 BOLT 工具、工作目录和缓存上层条目共约 11.41 GiB；它不是完整流水线峰值，也不能直接当作 BOLT 的净增量。本轮没有改代码、没有删除中间产物，减少量未测，现有 clang 未改，也没有生成新的 clang。内存释放后已满足准入，但工作盘空间不足以覆盖历史无 BOLT 构建的已观测下界和本地保留量，因而尚未启动用户要求的同条件完整构建。

证据统一位于 [disk-footprint-20261021](../../tools/bolt/results/disk-footprint-20261021/)。目录沿用用户指定日期；下载和本轮盘点实际在 10 月 22 日执行。

## 1. 本轮做了什么，缺什么

| 项目 | 状态 | 结果或边界 |
| --- | --- | --- |
| 固定 Base 快照及 build.conf 获取 | PASS | HTTP 200，压缩前后 SHA 与 repomd.xml 一致；没有取 reference 或 20261001 |
| 独立 GBS 配置 | READY | gbs_llvm_qb1202084.conf；仅启用指定 base packages/debug 两个仓库 |
| 历史无 BOLT 根占用 | 有下界 | 582 份历史 du 采样，最高 236,149,145,600 B；存在权限盲区及收尾采样缺失 |
| 历史开启 BOLT 根占用 | 不足 | 只有未完成的 %install 演练上层终点与文件系统 free 采样，不是完整构建根峰值 |
| 9e5675f、指定快照完整 ON 构建及 60 秒 du | NOT RUN | 本地磁盘容量准入参考不足；没有生成新的采样冒充实测 |
| 同条件 OFF 构建 | NOT RUN | 尚未启动 ON；若后续确需 OFF，先报告预计耗时再开始 |
| 清理 | NOT RUN | 尚不能认定 BOLT 完整净增峰值大小，不越过用户给的条件 |
| 清理后完整构建、clang/RPM 比较、白名单 | NOT RUN | 没有清理提交或新构建物 |
| 新提交 gbs export、五项解析 | NOT RUN | 没有新源提交；不沿用旧认证冒作本轮 PASS |
| Gerrit / QB 操作 | 无 | 没有推送、改配置、触发或控制 QB |

## 2. 固定输入与 QB / 本地差异

子构建原始日志记作 C，父日志记作 P。C 是 28 号文档已归档的 [1202084-full-log.txt.gz](../../tools/bolt/results/qb-timeout-20261021/child/1202084-full-log.txt.gz)，P 是该目录上一层的 full-log.txt.gz。行号均为解压后从 1 开始的原始行号。

C:L130、316、324–348 明确指定 `tizen-base-toolchain_20261013.024319`；C:L331 仅启用 `repo.base_0,repo.base_debug_0`，L332 的 standard 仓库列表是注释，未加入本地启用列表。C:L523 是 `export JOBS_N=12;export WORKER_N=28` 的 NGBS 启动命令。[摘录](../../tools/bolt/results/disk-footprint-20261021/qb-config-excerpts.txt)保留原文。

下载 URL：

```text
http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261013.024319/repos/standard/packages/repodata/f96236003d723509db9150df3987263ea7836b89fd1a3a1d2cde3e9f6cc52544-build.conf.gz
```

| 文件 | 大小 B | SHA256 |
| --- | ---: | --- |
| build.conf.gz | 3,559 | f96236003d723509db9150df3987263ea7836b89fd1a3a1d2cde3e9f6cc52544 |
| 解压 build.conf | 11,171 | e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945 |

[下载来源](../../tools/bolt/results/disk-footprint-20261021/input-provenance.json)、[仓库元数据](../../tools/bolt/results/disk-footprint-20261021/repomd.xml)、[校验结果](../../tools/bolt/results/disk-footprint-20261021/build-conf-verification.json)均保存。核对包含 repomd 的 checksum/open-checksum、gzip 解压内容、临时目录副本完全相同。这里验证的是用户指定固定快照提供的 build.conf；没有取得 QB 当时写入磁盘的 build.conf 原件，不能声称已经比对过那个原件的 SHA。

本地专用配置：

```text
/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261021-disk-footprint/gbs_llvm_qb1202084.conf
```

配置副本见 [gbs_llvm_qb1202084.conf](../../tools/bolt/results/disk-footprint-20261021/gbs_llvm_qb1202084.conf)。原 W/gbs_llvm.conf 的既有修改保留，SHA 仍为 `28f1caf93cd39738a7da1e0da8d5f945f7372963bb9823a507f9157294272169`，未写入。

| 条件 | QB 1202084 | 本地已准备 / 尚待实测 |
| --- | --- | --- |
| llvm 源码 | C 源码映射含 9e5675f57d122549997caffa39b655dfefc46fee；缺包 checkout 日志 | 干净的同一提交；spec/helper SHA 见 source-preservation.json |
| Base | 20261013.024319 | 同一固定快照 packages 和 debug URL |
| build.conf | 从当时 reference 读取；用户已确认其指向上述快照 | 固定快照下载；解压 SHA e5187fd7…；没有改用当前 reference |
| 构建引擎 | NGBS；预置 .NGBS-ROOT，三架构同机 | GBS 2.1.0，计划新建独立 x86_64 根；无 ARM 并发 |
| 并行 | JOBS_N=12、WORKER_N=28；LLVM 实际 ninja -j 缺日志 | 用户指定 jobs 8、_smp_mflags -j8、_costomized_smp_mflags -j20；未运行，不能写成实测 ninja -j8 或 -j20 |
| LLVM 自身并行 | 缺包日志，不能从 NGBS 变量推定 | 9e spec L63 默认 mlgo_build_jobs=6；L411 用该宏。最终展开和实际 argv 待启动后记录 |
| shelve | C 只给请求的源码映射；额外处理清单未取得 | 计划直接使用干净 9e，额外 shelve 清单为空；不叠加后续代码 |
| 外层命令 | P:L1511 有 timeout 8h gbs build --threads=30 及上述宏；C 实际使用 NGBS | 只采用用户明确认可的本地 GBS 与宏差异；尚未执行完整构建命令 |
| 本地资源 | 不以本机规则推定 QB 限额 | 重段 16 GiB/swap0、nice15/ionice3、共享锁及本地磁盘规则，仅约束本地测量 |

P 的完整命令另存 [parent-build-command-excerpt.txt](../../tools/bolt/results/disk-footprint-20261021/parent-build-command-excerpt.txt)。父命令和实际 NGBS 调度不能混为一次实际 GBS 执行。

## 3. 历史无 BOLT 构建：能证实的峰值下界

来源 W/temp/release-x86-full-build-20261013/round2-eight-output-proof/root-space-samples.jsonl。原文件无改写，逐字节 gzip 副本为 [historical-off-root-space-samples.jsonl.gz](../../tools/bolt/results/disk-footprint-20261021/historical-off-root-space-samples.jsonl.gz)，582 行；[TSV](../../tools/bolt/results/disk-footprint-20261021/historical-off-samples.tsv)给每行加阶段，采样器原文也已保全。

最高样本为第 **579 行**，时间 **2026-10-14 06:24:16.293693+08:00**，du 原始 stdout：

```text
236149145600	/var/tmp/llvm-optimize-x86-archivefix-20261013
```

即 **219.931 GiB**。当时普通构建已于 05:48:16 结束，静态库转换及安装尚未结束，平台后处理在 06:24:22 才开始。额外的独立安装验收在当天 12:13 左右才准备，因此最高样本没有包含那套额外完整安装目录。阶段依据 [main/docs49](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/main/docs/49_x86_build_resume_result.md) §1、§7.2；该文档的当前版本链接会随 main 变化，原始时间及本地源路径同时保存在 [summary](../../tools/bolt/results/disk-footprint-20261021/historical-off-summary.json)。

限制必须保留：

- 这是 **历史无 BOLT 构建**，不是在本次 9e5675f 上关闭回退开关的构建。它使用 Base 20261010.120615、Unified 20260814.092727，源码 cb679968 加归档修复。
- du 目标是 `…/llvm-optimize-x86-archivefix-20261013` 整个 GBS 根，包含 local 下的基础环境、构建等；不是只测 scratch chroot，更不是单测 build/。
- 582 行 du 均 exit 1，有 `/var/cache/ldconfig`、`/usr/share/upgrade`、`/root` 三处权限盲区。未改权限或提权重新测旧树。
- 最后样本 06:27:31，下一次 du 超过 50 秒后观察器于 06:29:07 结束。普通构建直到 06:49:10 才完成打包。未覆盖的时段与短命文件可能更高，因此只能报 **至少 236,149,145,600 B 的已观测根占用**，不能称为精确完整峰值。

由此仍无法计算同条件 ON−OFF；不能拿旧根当前 du 或整个文件系统 free 的下降代替完整峰值。

## 4. 历史 BOLT 演练：当前保留终点，不是峰值

25 号演练使用 506dc25 的 spec/helper，复用 docs38 的历史下层树，仅跑 %install；在 relink 期间被本地 55 分钟计算截止终止。没有走到 strip、BOLT 改写、compare-root、候选安装、转换或 post。初始 ThinLTO cache 仅 61 文件 / 14,977,512 B，和完整普通构建后的温缓存不同。

本轮只读 du 的对象是该演练的 retained **upper**，不会写下层。原始 argv、stdout、stderr、时间都在 [historical-rehearsal-current-du.json](../../tools/bolt/results/disk-footprint-20261021/historical-rehearsal-current-du.json)。

| 范围 | 当前分配占用 B | GiB | 解释 |
| --- | ---: | ---: | --- |
| tools/bolt 对象及生成文件 | 146,677,760 | 0.137 | 只含上层新增部分 |
| bin/llvm-bolt | 566,829,056 | 0.528 | 当次构建的工具 |
| 7 个 lib64/libLLVMBOLT*.a 合计 | 146,661,376 | 0.137 | 每个库的 du 原文在 JSON |
| **以上工具合计** | 860,168,192 | 0.801 | 三行互不包含 |
| clang-bolt 工作目录 | 5,381,619,712 | 5.012 | 含 ordinary 副本、未完成链接临时文件、profile 及文本 |
| lto.cache 上层条目 | 6,005,907,456 | 5.593 | 不是相同完整构建的 ON−OFF 缓存增量；含新增/可能 copy-up |
| **工具 + 工作 + 上层 cache** | 12,247,695,360 | 11.407 | 仅现存选定路径和，未到后续阶段 |
| 整个 build/ 上层 | 12,337,217,536 | 11.490 | 包含上述子项，不可再相加；还含配置等普通路径变化 |
| 普通 BUILDROOT 上层 | 52,646,158,336 | 49.031 | 普通 CMake 安装，不属于 BOLT 新增目录 |

工具库数值以逐个 du 的精确和为准。演练保全记录的整个 upper 分配量 **64,993,333,248 B**，逻辑字节 **65,114,238,933 B**；它包含普通 BUILDROOT，绝不能写成“BOLT 多用了 65 GB”。资源采样中整个共享文件系统 free 下降高水位 **65,183,444,992 B** 也不能归因给 BOLT。

工作目录当前主要文件：ordinary-clang-22 逻辑 **1,793,477,048 B**，profile.fdata **171,232,190 B**，未完成 `reference-relocs-clang-22.tmpc53946f` 逻辑 **3,560,474,952 B**、分配 **3,414,781,952 B**。未完成文件不是有效 relink 输入。清单见 [historical-rehearsal-endpoint.json](../../tools/bolt/results/disk-footprint-20261021/historical-rehearsal-endpoint.json)；mtime 不等于创建、最后使用或删除时刻，ordinary 的 cp -p 更会保留旧 mtime。

另一份 13 号温缓存重链实测，重链输出在 strip-debug 前逻辑 **3,560,483,168 B**，之后 **226,738,888 B**，当时缓存 **47,107 文件 / 96,877,810,360 B**。这些是文件端点，不是磁盘峰值，也不是 BOLT 新增 96.9 GB：大缓存在普通构建后已存在。[原始摘要](../../tools/bolt/results/disk-footprint-20261021/historical-relink-summary.json)。

四次 BOLT_DISK_REPORT 属于 9e 实现，旧 25 号演练早于这项实现。现有 QB 1202084 只拿到总控/调度日志，没有 x86 LLVM 包日志，因此没有四阶段原始磁盘报告可用于此次完整峰值计算。测试夹具里小文件的 BOLT_DISK_REPORT 不作为真实完整构建用量。

## 5. 用户要求的逐项峰值与生命周期表

“未知”表示没有连续覆盖的同条件测量，不用某个预算或终点填成峰值。下列最后使用关系是 **9e 代码静态读取关系**；具体时间需要补测的阶段日志和 60 秒 du，尚未取得。[源文带行号摘录](../../tools/bolt/results/disk-footprint-20261021/source-lifetime-excerpts.txt)。

| 项目 / 实际路径 | 完整峰值 | 产生阶段 | 最后使用阶段 / 时间 | 已知删除时机 |
| --- | --- | --- | --- | --- |
| 普通 LLVM：BUILD/llvm-22.1.8/build（不含另列 cache/BOLT/转换） | 未知 | %build | %install 及后处理的工具/元数据读取；具体时刻未知 | 本轮未删除；9e 没有为 BOLT 删除普通 build/ |
| BOLT 工具：同一 build/tools/bolt、lib64/libLLVMBOLT*.a、bin/llvm-bolt | 未知；旧中止演练终点 0.801 GiB | BOLT 重新配置、-j1 工具构建 | pipeline 重写；完整实测时间未知 | 9e 中未主动删除；旧演练仍保留 |
| 重链输出、link.d、重放脚本：build/clang-bolt/reference-relocs* | 未知；旧演练留有未完成临时文件 | pipeline relink | rewrite 读取已 strip-debug 输入后；具体时刻未知 | 9e 中未主动删除 |
| ordinary-clang-22 副本 | 未知；旧演练文件逻辑 1.793 GB | ordinary-copy | post 仍做安全属性与 tiny 对照，不能在 pipeline 完成时删除 | 9e 中未主动删除 |
| clang.bolt / clang.candidate | 未知 | rewrite / strip-all | install 的 validate_identity 还读取 strip-all 前 clang.bolt；candidate 供安装 | 9e 中未主动删除 |
| profile.fdata / Source1200 | 未知；旧展开 profile 171,232,190 B | unpack / SOURCES | rewrite；Source 压缩文件是构建输入 | 9e 中未主动删除；不得将共享 SOURCES 当中间文件删掉 |
| ThinLTO cache 的实际新增量 | 未知；旧温 cache 是普通构建既有约 96.9 GB | 普通链接及 BOLT 重链 | 链接器可能复用、写入和清理 | LLD 自身策略；本轮未删 cache |
| compare-root | 未知；**只有 install-before.json 和 install-after-pipeline.json，不存在第二个完整根** | snapshot / compare-root | compare-root 比较前后清单 | 9e 保留 JSON；本轮无删除 |
| candidate 安装目录 | 不单独计算；**复用唯一 BUILDROOT** | helper install | 先临时文件、fsync、核 SHA，再 rename；post 继续读安装后的 clang | 临时文件失败清理；没有第二份完整安装目录 |
| native-archive-conversion 临时载荷 | 未知 | compare-root 之后，clang 替换之前，Source1005 | 静态库转换逐档完成 | 转换器有逐档/收尾清理；本轮未运行，精确峰值与时间未知 |
| BUILDROOT（含 debug） | 未知；旧演练普通安装终点分配 49.031 GiB | 普通 CMake install，早于 BOLT | 平台后处理、RPM 文件处理和打包 | 本轮未运行，没有 %clean 时刻 |
| 最终 RPMS / SRPMS | 未知 | 文件处理 / 打包 | 打包及后续核验 | 本轮未生成或删除 |
| debuginfo | 未知；属于 BUILDROOT/usr/lib/debug，非另一个可相加完整安装根 | find-debuginfo | debuginfo RPM 打包 | 本轮未运行，没有删除时刻 |

特别需要澄清：工具构建使用的是普通 LLVM 的同一个 build 目录。若将“删掉 BOLT 工具整个构建目录”解释成删整个 build/，会破坏普通工具、库及后处理输入。只能在测量证明需要清理后，对真正 BOLT 自有的子目录/文件设计删除；本轮没有执行这一步。

## 6. 为什么内存已释放，仍未开始完整构建

[local-admission.json](../../tools/bolt/results/disk-footprint-20261021/local-admission.json)记录本轮准入时刻。MemAvailable **25,716,416,512 B（23.95 GiB）**，高于重任务 12 GiB 准入；不是内存继续阻塞。

目的文件系统为 /home 的 /dev/sda1，st_dev=2049。所有下列数值来自本轮 statvfs 的 `f_bavail × f_frsize`，是当前用户可用量；不把 root 保留块算作可供写入的空间。

| 本地准入参考 | 字节 B | GiB |
| --- | ---: | ---: |
| 目的盘可用 | 229,464,346,624 | 213.705 |
| 本地要求保留 | 32,212,254,720 | 30.000 |
| 可用于新增写入 | 197,252,091,904 | 183.705 |
| 历史 OFF 已观测下界 | 236,149,145,600 | 219.931 |
| 该下界 + 本地保留量 | 268,361,400,320 | 249.931 |
| **相对此参考仍缺** | **38,897,053,696** | **36.226** |

这是保守的 **本地准入参考**，不是声称新快照一定恰好需要这些字节。它还没有包括新源码导出、仓库下载、BOLT 的额外占用及短命峰值，因此释放这 36.2 GiB 也不等于已证明预算足够。旧样本根的环境不同，尚不能推导出可靠的完整新构建总需求；不能利用这种未知假装有空间，也不应随意写死更大的新门槛。

/var/tmp 所在另一文件系统也只剩 49,982,820,352 B，保留 30 GiB 后只有 17,770,565,632 B；不能作为可直接容纳全新完整根的替代目的盘。两个文件系统 free 不可直接相加来证明某一个根放得下。

按用户继续沿用的本地“单次大写入后仍保留 30 GiB”规则，本轮不以一个已不满足历史下界参考的目的盘启动完整构建，也没有擅自清掉保全证据、受保护旧根或普通 ThinLTO cache 以腾空间。共享重锁未取得，未启动任何编译/链接进程。完整构建预计还会长于一小时，后续启动前也必须落实可恢复分段，不能突破单次持锁 60 分钟。

这些准入与资源限制只用于本地；本轮没有把任何门槛写进 helper、spec 或发布代码。

## 7. 后续测量方法与接受条件（未执行）

保持已固定的 build.conf/Base、干净 9e、上述三个本地宏；使用专用新根，记录完整 GBS/rpmbuild argv、实际宏和所有输入 SHA。每 60 秒记录一次原始 du stdout/stderr、开始/结束时间、exit，同时记录文件系统可用量。整个根的同步采样用于峰值，子目录分项用于解释；父子目录不可相加。短于采样间隔的峰值仍可能漏采，报告必须标作采样下界。

build/ 内单列 BOLT、cache、转换临时目录；ordinary 子项扣除这些包含项。debug 目录属于 BUILDROOT，候选安装也属于同一 BUILDROOT。工具并非独立 build tree，compare-root 只是 JSON；没有的目录明确填“不适用”，不得造出两份安装目录。

阶段日志给产生和最后使用锚点；删除时间只能取实际 unlink/rmtree 事件，不能用文件 mtime 猜。ThinLTO 缓存新增量必须从 BOLT 开始时的清单与运行后差集核算，不将普通构建缓存整体算入 BOLT。

先取得 ON 完整采样，再判断历史 OFF 是否足以对照；若仍需新 OFF 完整构建，按用户要求先说明预计耗时再启动。没有同条件 ON/OFF 或可信差分证据前，不作“BOLT 很大/很小”的结论，不进入第二步删除。

只有清理前后使用相同输入、profile、工具与参数的候选、全部 RPM 文件清单/哈希、工具任务白名单均通过，才可报告清理安全。历史 4ec07159… 来自 cb679968 旧树及历史 BOLT；新快照输入不同，不能预先承诺 SHA 相同，更不能把未取得的 QB 506dc25 candidate 当作已核实的 4ec。

## 8. 修改范围、错误修正与交付

源树仍是 **9e5675f57d122549997caffa39b655dfefc46fee**，tree **941fc226aeb6b32ea6c78b03d78b5af2b87561a5**，工作副本干净，没有新源提交。spec SHA **0f9bd9333c614129fd5951ed8a1c062793c7cef74b83dbe9e52b03fffedf6a8d**，helper SHA **28f61031cb5ff60eaa46ebdc6a07014e4019ce1046f3ccee07794b6c173d1f23**。[保全记录](../../tools/bolt/results/disk-footprint-20261021/source-preservation.json)。没有新建分支，没有 Gerrit 推送，也没有 QB 操作。

只新增证据、专用本地配置与本文，更新 STATUS/raw 索引；未在受保护根执行 cmake/ninja，未修改 W 的受跟踪文件或旧下层目录。历史 upper 只读 du，保全文件不删除。

准备性修正一次：组装源码摘录时行号范围超过 spec 的实际 790 行，触发 IndexError；尚未进行任何产品操作。以 wc/tail 定位真实尾段，按实际长度取最后 15 行，并在写入前断言范围合法，修正后成功。该错误不影响已有采样或源文件。[逐条记录](../../tools/bolt/results/disk-footprint-20261021/preparatory-corrections.json)。

交付目录中的 `collect_historical.py` 是本地只读盘点脚本，不属于发布 helper，也没有运行任何新构建。原始历史 du 已保全压缩副本；本轮没有新的 60 秒构建采样可交付。源代码提交 SHA 无新增；证据提交 SHA 以本文所在 GitHub bolt-v4 提交为准。
