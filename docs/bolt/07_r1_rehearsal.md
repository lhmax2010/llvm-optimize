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

## 历史30对象：初轮FAIL，完整门禁尚未通过

30份历史.ii均存在且输入SHA可核验。初轮第1份ARM训练ARMISelLowering普通/候选.o不同，立即停后29份未跑；只读ELF诊断证实唯一不同节.GCC.command.line，完整记录了两个不同编译器路径，其他节（含代码、DWARF、重定位）相同，producer均clang22.1.8。没有删除录命令参数/过滤节或改判据。

源码复核发现GCC记录使用canonical实际ELF路径，只改argv[0]不足。因此验证器已准备在新的工作目录同一实体路径分两批复制普通/候选（各一次），复制前后SHA证明来源；输入、全部参数、cwd、输出一致，仍比较完整.o，原实体不改。公平重测第一次未满足12GiB入口所以SKIP_ADMISSION，第二次共享锁被占用；暂挂自己的未取锁等待以完成不依赖重锁的后续轻任务，未向归档进程发信号。后续在2小时预算内继续等，最终状态会更新本文。

## 原始证据与边界

E=/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261014；R1新工作=/home/abuild/bolt-work/bolt-v4-20261014。cache-admission/cache-copy、各*-session mountinfo/锁时间、*-scope采样/峰值、link.original/两replay、rewrite/identity/tiny、objects初轮、symbol/object-difference/original-cache-final均保存；大原始日志留E，不进Git。公开tools/bolt/results/r1-rehearsal.json给参数、身份和资源。真实RPM完整清单与cb新树匹配度未认证。
