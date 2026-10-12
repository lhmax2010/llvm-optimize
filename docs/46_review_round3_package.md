# 46 第二轮评审修订与第三轮评审材料

日期：2026-10-12（Asia/Shanghai）。开场 HEAD 与 origin/main 均为 `cb1e34af0958de17155459f7406869a91cadbe00`。

**当前完成第零步：完整性核查 PASS。后续只读普查、Source 修订、测试、全量复验与新补丁尚未执行。本页会随阶段更新，当前不能作为新候选已通过的材料。**

## 0. 范围与上次停止记录

W=`/home/linhao/Toolchain/development/llvm-optimize`；本轮 E=`W/temp/review-round3-continue-20261012`。temp 证据只留本机。生产 Source 为 `6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557`，ARM 候选为 `e2c2ebfa7272c6549f9be977861985ff597d3564dd26caf72438155622e30e0d`，尚无新 SHA。

上次 cb1e34a 停于代理复制的历史 16 GiB 准入断言：MemAvailable=15,255,969,792 B（14.208229 GiB）；scope、llvm-dis、测试和转换均未启动，代码未改。这不是产品失败。本轮用户明确改为轻量阶段 ≥6 GiB、全量转换 ≥10 GiB；不足时每5分钟读一次，最长60分钟；运行中18 GiB cap、swap0、nice15/ionice3、30秒采样、宿主可用低于2 GiB中止。上一停止原始输出保留在 `temp/review-round3-20261012`，旧报告完整内容可读 cb1e34a 版本。（证据：旧 E/stop-result.json；本轮任务资源准入；E/run_stage.py。）

## 1. 本地完整性核查

| 核查 | 本轮结果 | 证据（相对 E） |
|---|---|---|
| 主仓库全量 `git status --porcelain=v1 --ignored` | 4,682,969 行；唯一受跟踪改动为用户 `gbs_llvm.conf`，没有额外未跟踪非忽略项 | integrity-retry/main-status-all.stdout |
| 提交 / 远端 | `66e3369..HEAD` 只有 cb1e34a；本地 HEAD、origin/main 与远端 main 均一致 | integrity-retry/main-log.stdout、main-head.stdout、remote-head.stdout |
| 基准时间后 reflog | c1ebb68（10-11 01:21:36）、66e3369（01:22:06）为上一任务文档收尾；cb1e34a（10-12 14:33:04）为准入停止记录 | integrity-retry/main-reflog.stdout；git-object-attribution.json |
| tools/*.py、patches 全部文件、docs/43–46 | 61 个受检查文件与 HEAD blob 全同，关键 Source、补丁与最终测试 SHA 全同 | integrity-retry/head-blob-check.json；input-integrity.jsonl |
| W/llvm | HEAD `f111162e94aa48ed367c9d2c039456c70e7160ae`，分支 `sandbox/fangyu.he/llvm_optmize`；仅 spec 三处既有 6→4、6→4、2→1；基准后 reflog 无记录 | integrity-retry/llvm-*.stdout |
| W/llvm spec / 用户配置 | spec `95887b2d060b38d5ef8f56936f7481a03d131f9d26432180a68e02ec95f0dda5`；配置 `28f1caf93cd39738a7da1e0da8d5f945f7372963bb9823a507f9157294272169` | input-integrity.jsonl；integrity-retry/llvm-diff.stdout |
| W 全树 find（包括源码与 temp） | 基准 2026-10-11 01:18:45+08 后 186 条；无法归因 0 | metadata-complete.json；metadata-attribution.json |
| 15 个权限盲目录 | 经免密 chroot 只读补扫元数据，exit0，新增修改记录0；未改权限/文件 | privileged-newer-command.json、privileged-newer.stdout/stderr |
| 输入与工具 | x86 225、ARM32 210、AArch64 212，共647归档全同；两根6个accel ELF及包装器、宿主readelf、保护文件共671项 SHA PASS | input-integrity-result.json、input-integrity.jsonl |

修改时间归因：本轮核查/锁/证据94条；前次准入停止23条；前次完整任务文档收尾10条；Git对象/索引/ref/log59条。Git新对象逐一核验属于 c1ebb68、66e3369、cb1e34a 或 Codex turn-diffs 自动树快照；后者只是已登记用户配置与上述文档状态，不是额外分支提交。**无法归因清单为空**。cutoff 比上轮报告正式提交早数分钟，因此没有把已登记收尾提交误判为外来修改。（证据：metadata-attribution.json、git-object-attribution.json。）

本轮唯一一次第零步辅助脚本修正：初版 Python 字符串把 find `-printf` 中的 `\0` 解码为 NUL，Popen 在执行 find 前报 ValueError。只将字符串改为 raw 字符串，范围、时间及判据均未变；改后完整扫描完成。15个权限盲目录的追加只读补扫补齐覆盖。原失败和差异保留，不当作产品失败或降低核查门禁。（证据：integrity-helper-diagnosis.json、integrity-helper-fix.diff、integrity-scope、integrity-retry-scope。）

## 2. 只读普查与后续修订状态

第一步七项尚未运行。A1–A5、B1–B7、C/D 均尚未实施；B3/B5 须依据完整普查决定。Commands、W/llvm、spec、两份旧补丁没有改动；新候选补丁尚未生成。后续测试与两次 x86、两 ARM 全量复验尚未执行，不引用历史 PASS 代替。（证据：本轮 integrity-result.json。）

## 3. 本轮资源记录

| 阶段 | 准入 GiB | 启动可用 GiB | scope 峰值 GiB | 结果 |
|---|---:|---:|---:|---|
| integrity-scope | 6 | 16.121895 | 2.951160 | exit 1；采样器已回收 |
| integrity-retry-scope | 6 | 15.857098 | 4.945427 | exit 0；采样器已回收 |
| integrity-inputs-scope | 6 | 15.716362 | 1.474655 | exit 0；采样器已回收 |

全部阶段 MemoryMax=19,327,352,832 B、MemorySwapMax=0，未触发 OOM 或2 GiB宿主保护线。Git/find 的 scope 峰值包含文件缓存和内核 slab，不等于应用匿名内存。（证据：各 scope/plan.json、memory-summary.json。）

## 4. 不采纳项及理由（PM 已裁决）

下列为用户明确规定的设计边界，不是本轮实验新结论：

| 项目 | 不采纳理由 / 后续位置 |
|---|---|
| 重定位偏移加写入宽度检查 | 门禁不读目标字节；宽度随类型变化，统一 4 字节会误拒节末 1/2 字节重定位 |
| 内存看门狗 | 事后反应式，不等价于 RLIMIT_AS，且需改共用 Commands 循环 |
| `/emul` 原生 prlimit | 需改 qemu-accel 打包，超出 LLVM 包范围；保留为长期方案 |
| Python 解析 ARM 属性替代 readelf | 待第二段实测 qemu 调用开销再决定 |
| spec 改 `%{?buildsubdir}`、删除 `rm -rf`、补 binutils 依赖 | 非缺陷，不对总部评审中的 spec 做无功能收益改动 |
| 安装失败时另打印已安装清单 | summary 已记录，不为日志改共用安装函数 |
| 合并两个 change | Gerrit 依赖链保证顺序 |
| 把诊断数字写进 Commands 注释 | 证据放文档，不改 Commands |

出处：本轮任务第五步“不采纳项及理由”清单。

## 5. 第三轮与生产集成挂账

1. 完成七项只读普查，实施 A–D，宿主/根内测试与 B7 探针；依序完成 x86 两次和两 ARM 全量离线复验。
2. 生成第三轮评审的 PS3/PS2 候选与全量 diff；当前未生成。
3. 下一轮评审后做 x86 完整构建：cb679968 叠两个新补丁，扩大原编译与转换产物结构对照样本。本轮不做 RPM 构建。
4. ARM 第二段：根内 readelf 版本/输出/耗时、GNU ar 根内与宿主一致性、32位Python峰值、每命令600秒余量、/proc、磁盘、架构BuildRequires、/emul原生工具及显式AS确认、并发、最终RPM索引/符号/PIC/消费者验收。
5. 地址空间长期方案：原生限制器及交付边界；显式确认不等于限制已生效。

历史证据入口：[docs/44](44_arm_source_review_round1.md)、[docs/45](45_gerrit_patches_review_package.md)。不推 Gerrit、不清理磁盘；项目锁在后续阶段继续持有。
