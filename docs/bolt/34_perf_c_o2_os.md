# 34. BOLT 编译耗时：C、C++、-O2 与 -Os

## 1. HQ 汇总

比值为优化后/优化前；小于 1 表示更快。每格 20 个独立文件，每侧 5 次，先取逐文件中位数，再对比值取几何平均。比值均为组内比较，不是跨组绝对速度，也不是整个软件包构建的加速。HQ 表采用主矩阵的 C++ 与独立无警告 C 实验。C 样本仅覆盖本机 Tizen zlib/minizip，不能代表所有 Tizen C 应用。

| 语言 | 选项 | 架构 | 静态 BOLT/普通 | 节省 | hybrid+BOLT/普通 | 节省 |
|---|---|---|---:|---:|---:|---:|
| C | -O2 | x86_64 | 0.879375 | 12.06% | 0.870528 | 12.95% |
| C | -O2 | armv7l | 0.865229 | 13.48% | 0.863484 | 13.65% |
| C | -O2 | aarch64 | 0.866771 | 13.32% | 0.860887 | 13.91% |
| C | -Os | x86_64 | 0.873339 | 12.67% | 0.868617 | 13.14% |
| C | -Os | armv7l | 0.855503 | 14.45% | 0.857937 | 14.21% |
| C | -Os | aarch64 | 0.858588 | 14.14% | 0.858662 | 14.13% |
| C++ | -O2 | x86_64 | 0.850856 | 14.91% | 0.849071 | 15.09% |
| C++ | -O2 | armv7l | 0.847117 | 15.29% | 0.845817 | 15.42% |
| C++ | -O2 | aarch64 | 0.846093 | 15.39% | 0.845622 | 15.44% |
| C++ | -Os | x86_64 | 0.844838 | 15.52% | 0.841477 | 15.85% |
| C++ | -Os | armv7l | 0.838284 | 16.17% | 0.837191 | 16.28% |
| C++ | -Os | aarch64 | 0.839133 | 16.09% | 0.836491 | 16.35% |
| C++ | -O3 | x86_64 | 0.851867 | 14.81% | 0.849507 | 15.05% |
| C++ | -O3 | armv7l | 0.848437 | 15.16% | 0.846686 | 15.33% |
| C++ | -O3 | aarch64 | 0.848559 | 15.14% | 0.847295 | 15.27% |

本批 C 样本也有收益：-O2 节省 12.06%–13.91%，-Os 节省 12.67%–14.45%。C++ -O2 节省 14.91%–15.44%，-Os 节省 15.52%–16.35%；hybrid 和静态组的 BOLT 收益接近，不能据这次小差距宣称某种链接方式更快。

C++ -O3 是复测，不与 -O2/-Os 混合。旧 x86 结果以 30 条目（含重复训练样本）统计为 0.855890（约 14.4%）；从旧原始数据按 20 独立源重算为 0.856515。新测同时保留等权 20 文件与旧 30 条目权重，见后表。

完整数值：[hq-summary.csv](../../tools/bolt/results/perf-c-o2-os-20261025/hq-summary.csv)、[600 行逐文件中位数](../../tools/bolt/results/perf-c-o2-os-20261025/per-file-medians.csv)。

## 2. 编译器和样本身份

| 组 | 角色 | SHA256 | 大小（B） |
|---|---|---|---:|
| static | ordinary | `06c940726269210ce3655e17366820a080bfe236a3adc24622958e6a6709e309` | 1793485312 |
| static | candidate | `4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9` | 183224160 |
| hybrid | ordinary | `d5090159915657b235b96f1202c058e1efd1647d6a2225ac8fdb2906aeaa501d` | 1793485376 |
| hybrid | candidate | `8b799f18e2bc37269385db125c881609e8457de1dd179f5d9d0ff9f557b58d16` | 183224160 |

第二组启用依据：33号报告的周六 hybrid+BOLT 本地完整构建和验证 PASS。保全产品只读，未重生成候选。编译器路径/完整身份见 [compiler-identities.json](../../tools/bolt/results/perf-c-o2-os-20261025/compiler-identities.json)。

C：本机 `/home/linhao/Toolchain/libtool/codes/zlib` 的 15 个顶层库源文件，另选 minizip 的 ioapi、mztools、unzip、zip、minizip，共 20 个。覆盖压缩、解压、校验和、gzip I/O、ZIP 归档；没有下载源码。没有把 zlib/minizip 的结果泛化为 sqlite、OpenSSL、glib 或 busybox 的结果。来源提交、源文件大小与 SHA 见 [c-source-selection.json](../../tools/bolt/results/perf-c-o2-os-20261025/c-source-selection.json)。

C 为三个目标分别在 -O2/-Os 下预处理（共 120 份），保留优化级别相关的预定义宏差异。使用既有 Tizen 构建根的 sysroot；当前 `sudo -n` 需要密码，未进入 chroot、未提权或挂载，而是在宿主通过 Tizen loader/运行库执行并显式指定只读 sysroot。此处是与“在构建根内预处理”的执行位置差异。预处理原始 argv、stdout/stderr、退出码均保存；[C 预处理输入归档](../../tools/bolt/results/perf-c-o2-os-20261025/c-preprocessed-inputs.tar.gz)。

C++：沿用 docs/53 保存且 docs/33 核验的 90 条 .ii 资产，按原始文件去重为每目标 20 个；不重新预处理。三个优化级别各使用同一 .ii，原先预处理时的 -O3 宏保持不变，故这里衡量同一预处理输入的优化/代码生成耗时。两个原有 -O3 参数均替换成所测级别；其余参数除编译器槽位、sysroot/resource-dir、输入/输出路径及 --no-default-config 外保留。输入 SHA 和完整编译命令见 [cases.json](../../tools/bolt/results/perf-c-o2-os-20261025/cases.json)。

目标为 `x86_64-tizen-linux-gnu`、`armv7l-tizen-linux-gnueabi`、`aarch64-tizen-linux-gnu`。既有资产编译参数中没有显式 -mcpu/-march 等 CPU 参数，因此未自行添加。每个目标两侧使用同一 sysroot，全部编译器共用本次 hybrid 构建树的 clang/22 resource-dir。

## 3. 测量方法和环境

测量开始 2026-10-24T23:22:36.541163+08:00，结束 2026-10-25T04:30:37.431959+08:00。固定 CPU 2，并行编译数 1；角色按轮交替：第 0/2/4 轮 ordinary→candidate，第 1/3 轮 candidate→ordinary，主矩阵每个角色按同一顺序运行全部 300 个用例，独立 C 补测每个角色为 120 个用例。与旧脚本一致采用逐轮角色切换，而不是每个文件重新复制 1.8GB 编译器。

每个实验内部用同一路径/同一 inode 覆盖两侧编译器（复制与 SHA 核验在计时外），相同 cwd、输出路径和输入。主矩阵和无警告 C 实验各有自己的专用槽位；两组编译器在同一实验共用该槽位，resource-dir、sysroot、CPU 和计时方式相同。计时覆盖 taskset + setarch + Tizen loader + clang 的 subprocess 墙钟耗时，只做 `-c`。每次编译之前删除本次输出，防止把旧对象当成新对象。没有包构建或源码修改。

ASLR：每次命令使用 `setarch x86_64 -R`，探针 `/proc/self/personality` 为 `00040000`。运行中编译进程 affinity 已实读为 [2]；读取其 /proc/PID/personality 被权限策略拒绝，保留原始失败记录，不冒充直接读到。旧保存的 target-perf-driver.py 中未见 setarch，不能声称旧测已经关闭 ASLR；本轮明确关闭。Tizen loader 直接运行，避免向历史根写入；与旧 chroot 调用的位置不同。两侧完全同条件，但跨轮旧/新比值仍受运行环境和负载影响。

CPU Intel Core Ultra 7 265；governor `powersave`，driver `intel_pstate`，同胞列表 `2`，未修改调频策略。每次前后负载（1分钟）min/median/max=1.15/1.85/2.94；边界频率 min/median/max=800000/5131962.0/5221311 kHz，边界采样不等于编译期间平均频率。

开测前周六构建已结束。未按背景负载等待，不剔除异常样本；负载不能单独证明另一个重任务的存在。进程快照、conditions.json 与 samples.jsonl.gz 保存事实；开场与结束快照没有发现并行的包构建，主要后台进程为 VS Code/桌面，不能据两个快照排除期间短暂负载。C 小文件耗时包括编译器启动，启动成本可能掩盖优化阶段收益；只有 5 次样本，不给不存在的置信精度。资源使用 systemd 用户服务、MemoryMax=MemTotal−8GiB、swap0、nice10、ionice2/7，仅本地执行，不进入发布代码。

## 4. 对象一致性与完整性

主矩阵 6000 次，加无警告 C 补测 2400 次，共 8400 次编译，全部数据均保留。HQ 表使用 C++ 主矩阵 3600 次和无警告 C 的 2400 次，共 6000 次；600 个组×用例分别以第一轮 ordinary 为参考，对后续 5400 份输出做完整字节比较；不删除 .GCC.command.line 或任何节。不同输出共 0 份。全部输入收尾 SHA 核验不变。

包含辅助 C 实验在内共 7560 份非参考输出做过完整字节比较；全部 8400 次编译的退出码和对象校验结果在 summary.json 中独立列出。不同对象完整列表见 [summary.json](../../tools/bolt/results/perf-c-o2-os-20261025/summary.json) 的 unequal_outputs；为空才表示全部一致。每次输出 SHA、字节数、返回码和 byte_equal 在原始样本中。性能快慢不作为本任务的停止门禁，也不会为满足某个比值重跑或挑选样本。

C++ 原有参数会对部分 LLVM 输入产生警告（例如 GenVT.inc 的 -Wconstant-logical-operand）；保留原样，计时包含诊断产生与日志输出，两侧同条件。没有把该时间宣称为纯优化器内部时间。

## 5. C++ -O3 与历史口径

| 组 | 架构 | 本次等权20源 | 本次按旧30条目权重 | 留出10源 |
|---|---|---:|---:|---:|
| static | x86_64 | 0.851867 | 0.851159 | 0.853994 |
| static | armv7l | 0.848437 | 0.847451 | 0.851401 |
| static | aarch64 | 0.848559 | 0.847386 | 0.852087 |
| hybrid | x86_64 | 0.849507 | 0.848587 | 0.852275 |
| hybrid | armv7l | 0.846686 | 0.845715 | 0.849608 |
| hybrid | aarch64 | 0.847295 | 0.845775 | 0.851873 |

新“30权重”将训练组 10 源各重复计权两次、留出 10 源各一次；这是本次 5 次样本的重新加权，不伪装成另做了 30×5 次实验。历史独立源结果由旧记录合并同一源的 5/10 个样本后取中位数，细节见 summarize.py。

## 6. 原始材料和范围

C 参数修正：主矩阵的 -c .i 命令沿用预处理时两条 -I，每次产生两条 unused-command-line-argument 警告。该准备疏漏可能影响很短的 C 用例；没有删除其 2400 条完整样本，而是在主矩阵结束后以同一批 .i 补测两侧各 5 次，仅删除无效 -I 并使用独立输出槽位。预处理仍保留 -I。HQ 表采用 clean-c/ 的无警告结果，旧 C 结果保留于 warning-inclusive-c-summary.csv 与 main-matrix-summary.json。C 补测另在计时外 fsync 编译器副本，避免大副本的后台写回干扰短任务；耗时记录在 clean-c/compiler-switches.jsonl。两套实验执行时间、槽位、刷盘处理和前序热身负载不同，不把两套比值之差简单解释为警告的独立因果效应。

准备修正：最初使用带 timeout 的 subprocess.run，发现其 wait 轮询可能使短 C 编译计时量化；在 BOLT 对照开始前停止该单侧试运行，保留全部 149 条原始样本于 preparation-timer-pilot/，改为 Popen 阻塞 wait + 独立超时看护后从头完成两侧各 5 轮。试运行不是按结果筛选出的异常样本，未混入配对统计；原因和处置见 preparatory-correction.json。

原始目录：`tools/bolt/results/perf-c-o2-os-20261025/`。包含 prepare.py、measure.py、summarize.py、report.py、编译器身份、300 个用例、120 份预处理命令记录、C 输入归档、主矩阵 6000 条及 clean-c/ 补测 2400 条逐次采样（含完整 argv、前后负载/频率、SHA 和计时）、逐次编译日志归档 compile-logs.tar.gz（成员路径与样本 log 字段对应）、条件和资源记录、逐文件 CSV 与汇总 JSON。JSONL 无损 gzip；归档前后 SHA/解压验证见 archive-manifest.json，原始未压缩文件仍保存在本次 temp 的 raw-uncompressed/ 中。目录日期按用户指定 20261025，实际开始日期以 conditions.json 为准。

未修改 LLVM/helper/spec，未构建软件包，未联网取源码，未推 Gerrit，未删除历史根或保全产品，未运行历史根的 cmake/ninja。新测量槽位与输出只位于本次 temp/perf-c-o2-os-20261025；编译器与输入本体保持只读。完成后停止。
