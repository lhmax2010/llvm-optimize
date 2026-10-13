# 11 单一重链、磁盘底线与周三续跑

本轮（2026-10-13）只做轻任务，不取共享重锁，不跑重链/BOLT/对象实验；历史 R1 实测用于裁决与估算。最新人工裁决覆盖 06、07 以及 STATUS 的旧双路/复制新树 cache 方案，历史失败记录保留。

## 草案与夹具

生产路径只有 emit-relocs 重链 → 同树 LLVM strip-debug → BOLT 与匹配度/三目标 → LLVM strip-all → 三目标 → 安装与单次原 post 尾检。删除链接时 strip-debug、双路严格比较、回退函数/命令/夹具；没有自动降普通包。R、S/N 整数 5% 双门禁、禁止 infer-stale、前 BOLT note/前后 SHA、最终安装 SHA、ELF/存活/三目标/相对 alias、install 差集以及本地双模式清单策略均保留。

交接树默认原地使用原 ThinLTO cache，重放只改 output 与 depfile，再追加 emit-relocs；其余逐字不动。replay/pipeline 的 --cache-dir 是可选显式覆盖，仅供 R1 等受保护旧树由调用者预先准备完整校验副本；cache-copy/cache-unchanged 工具仍在。默认 pipeline 不复制、不审计冻结原 cache，允许 LLD 写入/prune。今夜没有引用任何新构建根。

95/95 fixtures PASS，含两路径逐字不变、显式第三路径、磁盘 >10 GiB/30 GiB 边界、额外 reserve、原 98,248,402,280B 危险复制在写入前被拒绝、磁盘失败不调用 linker、单一路径顺序、匹配/strip 前后微型失败终止；既有身份/清单/别名负例保留。轻 scope 4 GiB、swap0、nice19、ionice3，入口 ≥6 GiB；0.408s 测试 / 1.528s scope。完整 patch 和文本+Source 封套均静态 apply/tree PASS。

源草案提交 d6ddbff5ba74bfb420b357b5b6ba9ed300971bb4，父 cb67996861d070d68fec2b4c623eed7d20ba2e23；完整 patch 留 W/temp/bolt-v4-20261014-simplify，公开文本 patch、未变 profile 与 manifest 能重建同一完整树；未推 Gerrit。

## 磁盘准入

任何一次预计写入 >10×1024³ B 的操作，必须满足 free_before − planned_write − reserve ≥30×1024³ B，否则 SKIP_DISK，停止该项并记录。等于 10 GiB 不触发这条大写入底线，但仍必须有预算空间。按目标路径实际 st_dev/所在文件系统核算，不能拿 /home 的余量代替 /var/tmp，不能把预计会发生的缓存清理当可用空间。

helper 提供 disk-preflight 目录 字节数 [--reserve-bytes 字节数]；cache-copy 使用精确原 cache 字节加 4 GiB reserve。ELF 安装与 strip-all 副本按源实际大小预检，rewrite 按 4×输入暂估。spec 在 BOLT 开始、llvm-bolt 构建和额外 install 前分别用 16 GiB 保守阶段预算检查；pipeline 用 max(16 GiB,4×普通 ELF 大小)，可用 --planned-write-bytes 提高。16 GiB 是 R1 温缓存估计，不是未知新树/冷缓存写入的可靠上界：周三必须据交接树计划核算临时产物和新增缓存，预算不明即停止该项，不允许为了通过而下调。额外 buildroot 写入在 buildroot 文件系统单独预检。准入不抵消其他会话并发写盘，长阶段前必须再核算。

## Quickbuild 时间与内存估算

已有 0.5 秒采样中 ld.lld 可见跨度 612.645s、LLVM strip-debug 18.276s；BOLT 重写可见跨度31.717s，strip-all 可见0.501s（短命进程采样只能估计），原三目标约2s。完整 BOLT scope 66.333s 包括 profile 解压、SHA、重写、strip-all/微型门禁。新路径按约12–15分钟估算（参考重链+strip约10.5分钟，加BOLT/门禁约1分钟、SHA和新增strip前门禁余量）；不含同树新建 llvm-bolt、正常 LLVM 编译、安装/RPM post 或30/90对象。

reference scope 峰6.039 GiB，ld.lld 最大采样 VmHWM5,277,208kB；BOLT scope峰3.960 GiB、BOLT VmHWM3,855,356kB。pipeline 暂按峰约6.04 GiB，周三仍用16GiB cap。旧 reference 总676.945s含已删除的严格比较与原cache审核，加BOLT66.333s=743.278s可作旧测保守参考，不能当新代码的精确实测。旧copy41分钟及dual-link220秒不再计入新树流程。硬件、树、缓存、工具来源可能改变实耗。机器可读采样来源SHA与估算见 single-path-estimate.json。

## R1 副本清理与周三计划

仅删已核对旧 cache-copy.json 来源的 /home/abuild/bolt-work/bolt-v4-20261014/lto-cache；原cache与其他证据未变，设计附录在步骤3更新。

步骤2清理完成：仅删除授权副本 lto-cache 残余目录；前2,365文件/4,671,566,600B（实际占块4,676,378,624B），后0文件/0B/目录不存在；同文件系统free从79,338,237,952B（73.89GiB）到84,019,998,720B（78.25GiB），观测增4,681,760,768B。共享磁盘并发写入会影响free差量，不将其等同精确释放字节。原cache47,770文件/98,248,402,280B完整清单mtime/34跨度SHA前后及上轮基线一致，其他459条BOLT证据元数据清单一致。4GiB轻scope16.063s（工作15.095s），没有flock/chroot/mount；r1-cache-cleanup.json记录路径来源和审计哈希。步骤1 GitHub提交55a2e06已推送。
