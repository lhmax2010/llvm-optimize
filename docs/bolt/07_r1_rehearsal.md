# 07 R1 流水线预演：完全 strip

本轮只代表 f111162e 配方二进制；历史 llvm-bolt SHA1da7bb73…只作资格实验，不代表同源生产工具已构建。没有完整 LLVM 构建，没有 standalone，也没有进入归档根。

## 缓存、挂载与资源

完整复制 47,770 文件、98,248,402,280B；复制前可用103,902,519,296B，另留4GiB两路径重链瞬时空间。count/bytes/mtime/34个确定性跨度SHA样本核对通过。原cache复制前后、两次重链之后、独立最终审计均一致。副本后来被正常 LLD cache pruning 清理，原件不变；宿主空间已恢复约95GB，未手工删除缓存。

每段独立共享flock；cache为4GiB/nice19/ionice3，其余实际LLVM阶段16GiB/nice15/ionice3，swap0；入口与低于3GiB监控均启用。全部已结束scope消失，已完成段持锁均<60min；没有删锁或动归档锁/进程。只用普通chroot挂proc，以1000:1000执行，finally卸载；before/during/after mountinfo保存并校验after无R1/proc。未使用unshare、自绑定、宿主bind或overlay。

| 阶段 | scope wall(s) | cgroup峰GiB | 最大采样VmHWM(kB) | 结果 |
| --- | ---: | ---: | ---: | --- |
| bolt | 66.333 | 3.96 | 3855356 | PASS |
| cache | 2480.49 | 2.172 | 143032 | PASS |
| control | 3.032 | 0.054 | 18292 | PASS |
| dual | 220.237 | 5.406 | 4261760 | PASS |
| objects | 23.087 | 0.571 | 615984 | FAIL |
| reference | 676.945 | 6.039 | 5277208 | PASS |

VmHWM来自/proc逐进程0.5秒采样，JSON保留PID/名称各自最大值，不把cgroup峰值冒充VmHWM；短命进程可能未采到。耗时包括该scope内SHA/原cache审核，replay单独执行wall为dual214.123s、reference671.564s（reference包括strip-debug及严格比较）。BOLT阶段净60.308s，scope66.333s；单独rewrite等每项log/argv另留E。

## 严格一致性：FAIL，不放宽

非debug ALLOC全部内容/属性一致；2,581,569条重定位完整语义记录一致。符号表350,654对348,310，不一致；多出的2,344条全部STT_FILE，包括abi-note.c/init.c/crtstuff.c等。即使只差STT_FILE也不豁免。因此dual-flags快路径没有合格。按上一轮PM已经明确的“不一致退回预剥离”裁决，采用仅emit-relocs后llvm-strip --strip-debug的reference输入；SHA eccfb075bc3b2a6ca2bda5a2a6e68f6a29ba48b5586cb603f4b46080f656013e。

## BOLT、身份链与三目标

新实测 N=23592、M=144032、S=0、U=1、Q=383；R=1/23593≈0.004238545%，S/N=0%，整数5%双门禁PASS，infer-stale禁用。不是拿历史计数替代本次执行。

strip前SHA4f95c348c6eaa123959c7e90fd89d652f2d2c2453721fd3fc9b2487f234a360a，检查.note.bolt_info及其他BOLT标识节存在；同树llvm-strip --strip-all后SHA575fc9db9a18c28ad7d8ae12c999ca52b01bc3662fa13b68cedebe89a0b01965，无.symtab、debug/gdb_index、BOLT note。保持5个LOAD和合法entry；armv7l/aarch64/x86_64微型对象与同树普通clang全部完整字节一致，版本存活PASS。

## 历史30对象：初轮路径差异FAIL；公平重测30/30 PASS

30份历史.ii均存在且输入SHA可核验。初轮第1份ARM训练ARMISelLowering普通/候选.o不同，立即停后29份未跑；只读ELF诊断证实唯一不同节.GCC.command.line，完整记录了两个不同编译器路径，其他节（含代码、DWARF、重定位）相同，producer均clang22.1.8。没有删除录命令参数/过滤节或改判据。

源码复核发现GCC记录使用canonical实际ELF路径，只改argv[0]不足。因此验证器已准备在新的工作目录同一实体路径分两批复制普通/候选（各一次），复制前后SHA证明来源；输入、全部参数、cwd、输出一致，仍比较完整.o，原实体不改。公平重测第一次未满足12GiB入口所以SKIP_ADMISSION，第二次共享锁被占用；暂挂自己的未取锁等待以完成不依赖重锁的后续轻任务，未向归档进程发信号。公平重测随后实际等锁363.056s取得共享锁；入口合格，按16GiB/swap0/nice15/ionice3完成全部30对，完整字节相同。采用同一实体路径的两批复制，普通与候选只各复制一次，来源SHA在JSON；没有改编译参数、删除frecord或过滤任何节。初轮失败及准入/挂等待记录仍保留。

## 原始证据与边界

E=/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261014；R1新工作=/home/abuild/bolt-work/bolt-v4-20261014。cache-admission/cache-copy、各*-session mountinfo/锁时间、*-scope采样/峰值、link.original/两replay、rewrite/identity/tiny、objects初轮、symbol/object-difference/original-cache-final均保存；大原始日志留E，不进Git。公开tools/bolt/results/r1-rehearsal.json给参数、身份和资源。真实RPM完整清单与cb新树匹配度未认证。

## 最终重测与收尾

公平30对净350秒以内（精确每段字段见JSON），scope wall351.600s、cgroup峰4.572GiB、最大采样clang VmHWM722544kB，持锁351.706s；30完整.o全部PASS，未因首轮差异忽略.GCC.command.line。所有普通/候选调用的实际实体路径、input/cwd/argv/output均相同，每批实际来源与复制SHA分别验证，普通原文件SHA d25e9960…前后不变。

**预演可闭合的路径为reference重链→LLVM strip-debug→BOLT→LLVM strip-all**。dual-flags严格符号表一致性仍FAIL，2,344个STT_FILE不豁免。新cb树重新认证；本轮不能称dual-flags快路径PASS或Gerrit/Quickbuild已就绪。

最终独立缓存审核在公平重测后再次PASS；原47,770文件/98,248,402,280B的文件清单、mtime与34抽样SHA全部不变。最终审计确认R1无proc/root绑定残留、各已结束scope消失、源草案干净/公开helper与源内helper相同、Python3.9语法及设计50KB限制PASS。公开resource-metrics.json记录每个scope、所有失败、锁及挂载info摘要，不隐藏测量代码错误。

## 磁盘险情备案（2026-10-13，最新 PM 裁决）

今天复制 98,248,402,280B 后，工作区可用空间一度只有约5.6GB（入场 free 103,902,519,296B 减复制量，约5,654,117,016B / 5.27GiB）；直到 LLD 正常 cache pruning 自动删除副本的大部分内容才恢复。这是磁盘险情：此前只留4GiB重链 reserve，没有30GiB安全底线；checksum/count审核PASS不代表空间安全，不能依赖自动清理救场。

对策已裁决：周三正式交接新树后原地使用原cache，允许LLD写入/prune，不再复制；任何预计单次写入>10GiB，写完仍须≥30GiB free（reserve另计），不足跳过并报告。原大cache复制在新helper准入中会被拒绝。新完整x86树放/var/tmp，准确路径仅从归档会话 origin/main STATUS 正式交接取得，交接前不碰。快路径因2344 STT_FILE被永久删除，新草案只留reference+LLVM strip-debug，不在新树重复双路比较。完全strip SHA575fc9db…与历史v2完全strip一致。今晚仅轻任务，无共享锁/重实验；本会话副本残余将单独按授权删除并记录前后空间，其他原始证据保留。

本次残余清理完成：仅删除授权副本 lto-cache 残余目录；前2,365文件/4,671,566,600B（实际占块4,676,378,624B），后0文件/0B/目录不存在；同文件系统free从79,338,237,952B（73.89GiB）到84,019,998,720B（78.25GiB），观测增4,681,760,768B。共享磁盘并发写入会影响free差量，不将其等同精确释放字节。原cache47,770文件/98,248,402,280B完整清单mtime/34跨度SHA前后及上轮基线一致，其他459条BOLT证据元数据清单一致。4GiB轻scope16.063s（工作15.095s），没有flock/chroot/mount；r1-cache-cleanup.json记录路径来源和审计哈希。步骤1 GitHub提交55a2e06已推送。
