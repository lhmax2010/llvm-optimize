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

## 22RPM逐包预期差异清单 PASS（debug基准）

22个只读普通RPM头和完整SHA绑定；实际只读解包main clang与9个debug包，每个提取regular ELF的大小/SHA与RPM头相同。全部133调试ELF的--show-sources返回0/无诊断；普通clang自身1个，其他132个的完整来源清单绑定SHA。主包GNU debuglink名称及CRC32与clang-22.debug精确相符，明确调试文件所有者。普通clang映射到已包装debugsource的5106个来源，仅5个未被其他任何debug ELF引用。

|包|变化|删除|其他要求|
|---|---|---|---|
| clang | 7 | 0 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| clang-debuginfo | 0 | 1 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| clang-devel | 0 | 0 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| clang-devel-debuginfo | 0 | 0 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| compiler-rt | 0 | 0 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| compiler-rt-debuginfo | 0 | 0 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| libllvm | 0 | 0 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| libllvm-debuginfo | 0 | 0 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| libomp | 0 | 0 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| libomp-debuginfo | 0 | 0 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| libomp-devel | 0 | 0 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| lldb | 0 | 0 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| lldb-debuginfo | 0 | 0 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| lldb-devel | 0 | 0 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| lldb-devel-debuginfo | 0 | 0 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| llvm | 0 | 0 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| llvm-debuginfo | 0 | 0 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| llvm-debugsource | 0 | 5 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| llvm-devel | 0 | 0 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| llvm-devel-debuginfo | 0 | 0 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| llvm-static-devel | 0 | 0 | 全部其他路径/type/mode/size/SHA/link target保留基线 |
| python-clang | 0 | 0 | 全部其他路径/type/mode/size/SHA/link target保留基线 |

clang包允许实体内容/大小变化与6个别名target规范化；7个family aliases中clang原已指clang-22而不变。clang-debuginfo仅删除自身/usr/lib/debug/usr/bin/clang-22.debug；本基线没有对应build-id链接，删除列表0项，不凭习惯编造。llvm-debugsource仅允许以下5个已逐项证明的源文件缺失：

- /usr/src/debug/llvm-22.1.8-1.x86_64/build/tools/clang/tools/driver/clang-driver.cpp
- /usr/src/debug/llvm-22.1.8-1.x86_64/clang/tools/driver/cc1_main.cpp
- /usr/src/debug/llvm-22.1.8-1.x86_64/clang/tools/driver/cc1as_main.cpp
- /usr/src/debug/llvm-22.1.8-1.x86_64/clang/tools/driver/cc1gen_reproducer_main.cpp
- /usr/src/debug/llvm-22.1.8-1.x86_64/clang/tools/driver/driver.cpp

各项绑定普通debug SHA/来源dump SHA/全部其他debug manifest SHA/原源文件SHA，owner/独占证据在validation-expected-proof.json，完整其他来源与原22包header manifest以xz公开，raw source dumps+stderr在tar.xz。严格helper package-compare对预期debug差集PASS；发布模式只(a)的规则模拟PASS，但没有真实发布全构建，debug基准不能证明发布payload字节。发布普通/BOLT完整构建仍在进Tizen-Base前挂账。

不允许新增任何路径，不允许非clang内容变更，不允许llvm-bolt/perf2bolt/llvm-boltdiff/libLLVMBOLT*.a/new BOLT exports或debugsource。包含5源的父目录条目仍要求保持基线；源文件独占证据不自动放行目录删除，周四明确核对。没有实际完整BOLT RPM产出，本步为预期差异及证据，不冒充实物逐包比对。Quickbuild候选实体必须对自己的strip-all日志SHA；本地4ec/文件大小只是候选占位，不要求两边clang SHA一致。其他payload逐字节基准不放宽。

|解包/来源阶段|写入预估GiB|scope秒|峰GiB|锁持秒|剩余空间GiB|
|---|---:|---:|---:|---:|---:|
| clang | 1.230 | 15.056 | 1.596 | 15.089 | 439.006 |
| clang-debuginfo | 16.103 | 333.280 | 8.741 | 333.319 | 422.896 |
| clang-devel-debuginfo | 0.032 | 1.527 | 0.093 | 1.564 | 422.858 |
| compiler-rt-debuginfo | 0.010 | 1.025 | 0.049 | 1.058 | 422.847 |
| libllvm-debuginfo | 1.015 | 12.051 | 1.786 | 12.082 | 421.831 |
| libomp-debuginfo | 0.005 | 1.027 | 0.042 | 1.058 | 421.825 |
| lldb-debuginfo | 1.783 | 22.338 | 2.928 | 22.375 | 420.041 |
| lldb-devel-debuginfo | 1.487 | 18.726 | 2.545 | 18.762 | 418.553 |
| llvm-debuginfo | 20.055 | 412.960 | 9.069 | 412.993 | 398.488 |
| llvm-devel-debuginfo | 1.574 | 18.562 | 2.344 | 18.593 | 396.903 |

各重段16GiB/swap0/nice15/ionice3、单锁≤60m；16.103/20.055GiB两次写入预检与写后free≥30GiB通过，原件只读，无原cache变动。全部锁/proc/scope已回收。原RPM与约43GiB解包证据留E，不上传大ELF。

## 周四实物核对步骤

1. 绑定Quickbuild版本/宏模式与候选identity日志；匹配统计同量级且双5%、tool-plan、compare-root必须PASS。
2. 解开所有RPM，以本基准逐包枚举路径/类型/权限/大小/SHA/链接target；只允许清单中clang与alias变更及已证明debug缺失，任何新增/非clang变更失败；clang用QB自己的candidate SHA。
3. 对debugsource完整文件清单与上快照比较，除5源外其他文件及目录不自动放行；现存所有CMake导出SHA须等普通值，排除BOLT库/工具/工具alias/新源。
4. 核实包内clang存活/三目标/aliases，再对Quickbuild clang性能复核；不比较local/QB clang SHA。周五若tizen_base合归档静态库补丁再变基/解spec冲突，本步不做。
