# 20 续跑八：对象验证、本地认证与性能

2026-10-15 续跑八：从对象继续（进行中）

PM确认7439文本/两模式展开/120输入准备已经结束，不重做；只按要求复核保存输入SHA。查询已有脚本/证据/配置必须先rg --files或find；产品操作前改正的查找路径不计准备错误但逐项报告；产品用错输入/env/参数仍每类修正一次，第二次或产品门禁失败即停。a1410e3d父cb和历史后备候选4ec07159…不改。本轮禁止新CMake，原树cmake/ninja/-P仍禁。

120输入SHA复核PASS，共901204757B；新E=bolt-v4-20261015-validation，根内同名专用目录。六段单锁16GiB/swap0/nice15/ionice3/单编译进程，普通与候选同一实体路径及inode、相同argv/cwd/input/output，完整.o不删.GCC.command.line。随后双模式小spec、22RPM/DWARF预期清单、30×5性能geom<0.98才推sandbox。路径查找更正/准备性修正目前0；既有输入不再复制。

后续结果逐项登记；此前文本/展开PASS沿用19。

## 30/90对象全部PASS

120/120输入各完成普通与候选编译，共240次；所有完整.o逐字节相同，包括.GCC.command.line，没有过滤或删节。同一compiler路径/同一inode、相同argv/input/cwd/output，原RPM前导PATH/which记录在每次call与日志。19输入复核SHA全部相同，旧输入只读。结果与完整参数见validation-objects.json。

|段|对数|scope秒|峰GiB|最大采样VmHWM kB|锁持秒|
|---|---:|---:|---:|---:|---:|
| historical-arm-training | 10 | 114.361 | 2.829 | 690332 | 114.405 |
| historical-arm-holdout | 10 | 124.779 | 2.428 | 723088 | 124.811 |
| historical-aarch64 | 10 | 120.878 | 2.453 | 694784 | 120.913 |
| assets-armv7l | 30 | 338.521 | 2.694 | 723672 | 338.555 |
| assets-aarch64 | 30 | 341.742 | 2.612 | 728772 | 341.777 |
| assets-x86_64 | 30 | 339.852 | 2.803 | 724084 | 339.887 |

合计scope 1380.133s，最大cgroup峰2.829GiB；每段16GiB/swap0/nice15/ionice3、单编译进程、锁≤60分钟，全部锁/proc/scope回收，无低内存或OOM。没有CMake/Ninja/原cache写入。全.o/ii/原始calls留E与根内专用目录，非公开大二进制。双模式/预期清单/性能仍待，不推sandbox。

## 双模式小spec PASS

使用a1410e3d helper，普通clang/control先安装→snapshot/compare-root→候选install→原平台post一次→BOLT post尾检。没有第二次CMake安装或新配置。debug/release各一次rpmbuild-bb，execve证明helper post各1次、find-debuginfo仅debug1次、brp-strip脚本debug0次/release1次（原debug宏跳过该脚本）；debug control由eu-strip处理、release control由GNU strip处理，候选两边均未被strip/eu-strip处理。两RPM解包候选SHA保持4ec07159…，每边包装前尾检和包装后三目标对象全部PASS，clang家族链接归一clang-22。

- debug: scope 32.628s，峰3.245GiB；file原文 `/home/abuild/bolt-work/bolt-v4-20261015-validation/clang.candidate: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, stripped`。
- release: scope 34.612s，峰3.166GiB；file原文 `/home/abuild/bolt-work/bolt-v4-20261015-validation/clang.candidate: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, stripped`。

完整spec/日志/execve/逐调用环境见validation-smoke-*及validation-dual-mode.json；控制ELF小链接单锁16GiB，RPM两段4GiB轻scope，无共享锁，proc/scope均回收。不是完整LLVM RPM后处理认证，逐包预期/DWARF清单下一步。
