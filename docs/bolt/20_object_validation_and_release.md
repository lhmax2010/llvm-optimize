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

## 固定核性能复核 PASS

30份x86_64资产条目，三组各10按既定权重（不把cohort重复条目去重），每侧5次/总300次编译。固定CPU 2，Intel(R) Core(TM) Ultra 7 265，无SMT同胞；intel_pstate/powersave，策略范围800–5300MHz，实测频率/负载每次前后保留，未修改策略。并行度1、共享重锁、16GiB/swap0/nice15/ionice3；准入该核busy约4%，load1约1.03。角色先后逐轮交替，拷贝/SHA/前导/chroot不计时，计taskset+clang subprocess wall_s，不删异常样本。

|cohort/源条目|普通中位秒|候选中位秒|候选/普通|
|---|---:|---:|---:|
| arm-training/00-SemaStmt | 5.924246 | 5.020201 | 0.847399 |
| arm-training/01-SemaExprCXX | 6.181000 | 5.169195 | 0.836304 |
| arm-training/02-SelectionDAG | 7.183144 | 6.210044 | 0.864530 |
| arm-training/03-MachinePipeliner | 6.345171 | 5.447421 | 0.858515 |
| arm-training/04-Attributor | 6.564803 | 5.624523 | 0.856770 |
| arm-training/05-WholeProgramDevirt | 5.941800 | 5.093702 | 0.857266 |
| arm-training/06-ARMISelLowering | 8.524114 | 7.381667 | 0.865975 |
| arm-training/07-ARMTargetTransformInfo | 5.063993 | 4.241886 | 0.837656 |
| arm-training/08-MasmParser | 3.384084 | 2.922770 | 0.863681 |
| arm-training/09-AsmParser | 2.736224 | 2.321193 | 0.848320 |
| arm-holdout/00-ParentMapContext | 5.920512 | 5.041770 | 0.851577 |
| arm-holdout/01-ParseDecl | 5.030503 | 4.227525 | 0.840378 |
| arm-holdout/02-Driver | 5.267358 | 4.606841 | 0.874602 |
| arm-holdout/03-CoverageMappingGen | 5.696608 | 4.675234 | 0.820705 |
| arm-holdout/04-Metadata | 5.550470 | 4.755958 | 0.856857 |
| arm-holdout/05-ScalarEvolution | 9.854125 | 8.643751 | 0.877171 |
| arm-holdout/06-AArch64InstructionSelector | 5.816990 | 4.987474 | 0.857398 |
| arm-holdout/07-X86ISelDAGToDAG | 5.202233 | 4.501135 | 0.865231 |
| arm-holdout/08-ELF | 5.744014 | 5.139962 | 0.894838 |
| arm-holdout/09-InstrProfReader | 4.498176 | 3.833669 | 0.852272 |
| aarch64-training/00-SemaStmt | 5.927614 | 4.994018 | 0.842500 |
| aarch64-training/01-SemaExprCXX | 6.179533 | 5.178743 | 0.838048 |
| aarch64-training/02-SelectionDAG | 7.179609 | 6.223661 | 0.866852 |
| aarch64-training/03-MachinePipeliner | 6.325929 | 5.456417 | 0.862548 |
| aarch64-training/04-Attributor | 6.574663 | 5.619978 | 0.854793 |
| aarch64-training/05-WholeProgramDevirt | 5.925185 | 5.080818 | 0.857495 |
| aarch64-training/06-ARMISelLowering | 8.521611 | 7.380459 | 0.866087 |
| aarch64-training/07-ARMTargetTransformInfo | 5.066534 | 4.256032 | 0.840028 |
| aarch64-training/08-MasmParser | 3.400408 | 2.936897 | 0.863690 |
| aarch64-training/09-AsmParser | 2.716850 | 2.338638 | 0.860790 |

几何平均比 0.855890085，按(1-ratio)耗时降低14.411%，阈值严格<0.98：PASS。load1范围1.37–2.54/中位1.93（含被测单进程），完整5次原样本/环境/cpu频率在validation-performance.json。scope 1704.017s/峰4.343GiB/VmHWM最高725344kB，锁持1704.056s；proc/scope/锁已回收，无低内存/OOM。不是Quickbuild性能；周四实物仍须复核。

## Sandbox推送与收尾 PASS

全部前四步门禁通过且保护审计PASS后，直接推授权源提交 a1410e3d14b8836e3f9be5a1b4380f914dc2e705（父cb67996861d070d68fec2b4c623eed7d20ba2e23）到 sandbox/lhmax2025/bolt_pgo；远端before cb67996861d070d68fec2b4c623eed7d20ba2e23，after a1410e3d14b8836e3f9be5a1b4380f914dc2e705。Git返回0，无force、无refs/for、无tizen_base，没有archive补丁/变基；source tree33b4e9f84cec3336878501d55fe243b41c092c80。完整stdout/stderr及远端前后查询公开validation-sandbox-*，元数据validation-sandbox-push.json。

|源提交文件|操作|字节|SHA256|
|---|---|---:|---|
| packaging/clang-bolt-helper.py | A | 33098 | 7614228b5da020fd1ae08eaef0ebaf096c317f21a370e249285ee632711888e7 |
| packaging/clang-bolt-v2.fdata.xz | A | 9735212 | 52fd8522b8cceadebfb6bfc0a19f721f1072cff95c682b12b2c4dd5b0cc1e27f |
| packaging/llvm.spec | M | 24322 | 14d17a60369a2c05661037583740b410f0fd710aef2c0c78de08175a57bb6c0c |

本地候选最终SHA4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9，路线历史工具后备。周四必须核Quickbuild匹配统计同量级/双5%、现场tool-plan、compare-root、Quickbuild自身性能、debugsource逐项清单；不要求两边clang SHA相同。若tizen_base之后合归档install补丁，周五在新基线上变基处理spec冲突；本次不做。发布完整普通/BOLT构建及消费者仍挂账，双模式mini只证明机制。

保护审计PASS：22RPM/普通clang等指纹、归档独立证据/原源码元数据、坏cache/ninja SHA保持；120原输入再次逐SHA不变。原cache47987/96881772832B，无新CMake/Ninja/原cache写入；无ARM根访问/完整LLVM构建/W tracked或W/llvm修改。所有18次重锁单次≤60m、proc/scope回收；最终审计scope30.592s，sandbox轻scope22.592s。原根free53753024512B/E free426093473792B。

本轮查找更正0：均先rg --files/find定位。产品准备性修正三类各一次：(1)报告误要求debug也调用brp-strip，根据08及同一trace改为debug0/release1，未重跑RPM、未改产物；(2)旧scope CLI打印FAIL却返回rc0导致一次Git缺少未生成report的pathspec错误，未提交；本会话CLI改为正确传播状态，后续操作失败即退出。(3)收尾报告正文百分号格式转义错误，修正生成器一次，不重跑产品或推送。失败report原文与三项理由公开，非产品门禁豁免。性能进度消息曾236误计为206已即时纠正，原300样本未受影响。

任务第一至第五步完成，最终PASS；证据分步GitHub提交0009452、dc5163f、bcbdd1a、b2e18dd，sandbox已更新。所有数据/每file5次中位数CSV/完整来源和原包头/execve/资源与约束在本20及validation-*；原大.o/.ii/ELF/RPM和cgroup/mountinfo留E/根内专用目录。GitHub收尾与raw索引随后推送并逐URL校验。

收尾报告修正补充：正文百分号格式错误修正一次；另一次stdin报告辅助命令从W导入E的metrics模块失败，实际未执行任何报告动作，rg定位后去掉不需要的导入，以标准库复制/更新资料。两类各修正一次；连同先前post链计数/scope CLI共四类各一次，实验和sandbox推送均未重跑/改变。两收尾失败原文和完整四项记录公开。查找已有文件均先搜索，本次无产品查找路径更正；模块搜索路径属于报告命令准备错误，不计为产品结果FAIL。

原始artifact格式：CSV保留标准CRLF，git whitespace以cr-at-eol识别；Gerrit captured stderr原样保留尾空格，仅该路径排除whitespace lint。其余提交文件diff-check PASS，文件大小/HTTP/SHA检查不排除任何文件，不改原样本数字或网络原文。
