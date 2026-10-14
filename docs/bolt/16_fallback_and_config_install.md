# 16 历史工具候选与配置级安装核对

2026-10-14，周三续跑四。第一步重链输入核对PASS，后续门禁按本页逐步记录；本轮不再恢复、配置或在原树运行Ninja。

## 最新人工裁决（覆盖此前相应要求）

1. 上轮恢复方法没有先移开污染cache，以正确环境重跑又触发compiler变化/删cache，不是新的产品缺陷。
2. 两次失败配置已刷新llvm-config.h、Targets.def、config.h等生成头；本周放弃原树恢复/树内工具路线。原树只读供已有重链输入与普通clang/strip/resource使用，禁止任何cmake/ninja（包括-n）；周五后决定恢复或废弃。
3. 本周正式本地候选允许历史llvm-bolt SHA1da7bb735f7bc1afab9a863154260699b0b0f88c6fd05b99231dd21ef653fd5a；树内工具构建与安装清理交Quickbuild验证。匹配、note、strip-all、三目标、身份链、对象、双模式/清单与性能门禁不变。
4. Quickbuild用自己的源码，BOLT前clang不与本地输入逐字相同；周四不核对两边clang SHA相等，改核Quickbuild日志N/M/S/U/Q、R、S/N同量级且5%双门禁PASS，并对Quickbuild clang复核性能。

原RPM环境前导用于所有显式cmake/ninja/链接；逐次记录PATH/which。准备性错误每类一次修正；同类第二次或产品门禁失败停止。16GiB重scope/锁≤60分钟、4GiB轻scope、swap0/内存/磁盘底线、原归档证据/22RPM/ARM保护与Gerrit拒绝原文停沿用。

## 第一步：保留输入，不重放

13重链并LLVM strip-debug的输入仍在 /home/abuild/bolt-work/bolt-v4-20261014-relink-first/relinked-clang-22，226,738,888B，SHA158275040dbaa71999f60a4b62e4dd9a23a58b4d72e7ff85fb3c5f5ebff064e4，与relink-first-relink.json一致。不需要链接输入审计或重放，没有在原树调用cmake/ninja/链接。历史tool完整SHA、profile SHA d9b132f9…与普通clang SHA7df0ff90…均复核PASS。

新E=W/temp/bolt-v4-20261014-fallback；根内新/home/abuild/bolt-work/bolt-v4-20261014-fallback。第一步4GiB轻scope12.049s，不取共享锁；source元数据基线保存，无准备性修正。后续候选与配置级四项结果待登记；尚无推送资格。

## 第二步：正式后备候选PASS

本次重新rpmspec展开debug/release草案，均调用同一Source1201 pipeline，helper镜像SHA与源提交一致；正式OPTIONS为ext-tsp、cdsort、split-functions/all-cold/eh、dyno-stats、thread-count=1、stale-threshold=5，不含infer-stale。历史工具按这些参数完整重写保留输入，匹配 N=23592/M=144032/S=0/U=1/Q=383；R=0.004238545%、S/N=0.000000000%，5%双门禁PASS。

前BOLT标识节与完整ELF审计PASS；strip-all前及后各三目标微型对象字节门禁PASS。BOLT输出SHAf5e665fb2d2b77b512ce71b38d639ebcaa470369153b7a352a8246b13866c83d；最终完全strip候选SHA4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9；输入/profile/tool身份链见fallback-candidate.json，其中identity明确strip前BOLT节存在、前后SHA与strip工具SHA。候选留根内本轮工作目录clang.candidate，历史工具路线不冒充本树新工具。

草案会在rpmbuild stdout打印匹配统计：pipeline返回counts(N/M/S/U/Q/R/S_over_N)，main JSON打印整个result；BOLT原始详细日志存work/rewrite/bolt.log。无需修改草案；周四可从构建日志读JSON数值与双门禁结果（未通过会BOLT_GATE_FAILED且退出）。重阶段scope26.620s、kernel峰4.030GiB、最大采样VmHWM3850992 kB，原RPM入口PATH与which见JSON；共享锁/proc/scope已回收。第三步静态配置/安装核对尚待。

## 第三步：命令采集第二次准备错误STOP，快照只读诊断发现清理缺口

原始临时配置 rc0，但本任务错误使用根内Ninja不支持的 `compdb -a`。这不是产品门禁失败；使用一次 command-capture（记录中ninja-compdb-option）准备性修正，改为显式传入全部生成规则。首轮日志保留，临时目录已删除。修正轮重新配置及追加bolt均rc0、无删cache提示，前后build.ninja/全部cmake_install/Export与Targets/Exports文件保存；再次采集却发现Ninja compdb有意省略无输入的CUSTOM_COMMAND边，不能以该输出认证全部边。此范围假设是本任务第二次同类采集错误，按PM停止，不再换采集器或跑新的配置/产品实验。

修正轮入口四次记录：baseline cmake27.149s，before compdb0.241s，append cmake3.742s，after compdb0.243s；全部原RPM PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin，which=/bin/clang及/bin/clang++。4GiB轻scope首轮39.135s/峰0.706GiB，修正轮40.120s/峰0.487GiB。临时目录已删除，原源码前后元数据清单一致。停止后只读分析保存快照，不重试命令采集；其结果不冒充完整第1项PASS。

|核对项|结果与证据|
|---|---|
|1 全部非BOLT构建边/生成配置|完整边命令门禁未认证：before13421条有命令边，只采11405，漏2016条；after13675条只采11608，漏2067条。已采11405普通边命令逐字相同，无普通边丢失。86个普通配置产物（含全部include/llvm/Config与llvm-config .inc等）内容逐字相同；第87个compile_commands.json为聚合构建元数据，只因追加BOLT条目而变化。绝不以头文件相同或已采子集替代全部边认证。|
|2 安装规则|快照只读核对：非BOLT规则不变；667→684个安装脚本，新增17个全在tools/bolt。唯一已有脚本tools/cmake_install.cmake只多一个BOLT子目录include及其条件wrapper，删除整个BOLT block后原文相同。新增7个静态库及2个工具别名，见下表。|
|3 导出元数据|47→47个文件；LLVMExports/Targets及其他导出文件内容不变。额外检查安装LLVMConfig.cmake：仅其LLVM_AVAILABLE_LIBS与LLVMBUILD_LIB_DEPS追加7个BOLT库（本文件不在Exports/Targets通配名内，但对消费者重要，明确纳入）。没有新增导出文件，完整diff在JSON。|
|4 清理/恢复覆盖|**FAIL，有2项遗漏**。7个静态库由file(INSTALL)登记manifest，可按安装差集prune；LLVMConfig.cmake位于/usr/lib64/cmake/llvm，已有ordinary-exports完整backup/restore覆盖。但两个BOLT别名由LLVMInstallSymlink.cmake创建，脚本未追加CMAKE_INSTALL_MANIFEST_FILES；helper prune_install要求每个新增非目录都在manifest内，会报unregistered install addition。因此不能推sandbox。|

新增静态库均在/usr/lib64：libLLVMBOLTCore.a、libLLVMBOLTPasses.a、libLLVMBOLTProfile.a、libLLVMBOLTRewrite.a、libLLVMBOLTRuntimeLibs.a、libLLVMBOLTTargetX86.a、libLLVMBOLTUtils.a。新增/usr/bin/perf2bolt及/usr/bin/llvm-boltdiff均为create_symlink指向llvm-bolt；BOLT_BUILD_TOOLS=OFF时llvm-bolt实体本身不安装，两个安装symlink仍由无条件add_bolt_tool_symlink生成。完整规则与来源源码SHA在fallback-config-install.json，LLVMInstallSymlink.txt公开；配置级分析不声称执行了实际DESTDIR安装。

建议下轮草案清理逻辑覆盖这两个脚本生成且未登记manifest的别名：校验普通baseline无相应路径、当前是预期指向llvm-bolt的新增链接，再删除，并保留最终完整inventory严格相同门禁；或在配置方案中真正禁止这些安装规则。不能仅忽略它们或放宽“不得新增文件”。本轮不改spec/helper、不改源提交或封套。完整边采集下轮应覆盖无输入CUSTOM_COMMAND，先验证覆盖范围；本轮没有继续更换方案。

## 收尾保护审计与原缓存写入例外

普通clang与22RPM逐SHA/大小PASS，review49-independent-install元数据PASS，源码前后清单PASS；原树cache文件SHA17f7fbc7…、build.ninja c0068a3e…保持上轮STOP状态，本次没有在原树调用cmake/ninja（含-n），生成头未再修复/刷新。原树禁用规则与周五后决定恢复/废弃不变。

**临时配置的缓存路径准备没有满足原树仅作输入来源的意图。** 沿用15预置LLVM_THINLTO_CACHE_PATH指向原lto.cache，配置测试链接仍向原缓存写入：最后已知47626文件/96880098760B→本次47987/96881772832B，+361文件/+1674072B。虽然没有显式复制/清理cache，仍不能声称原树完全只读；发现后不再写/删这些自动生成项。后续临时配置应改用本会话专用缓存，不需复制原缓存。本次free59823763456B（55.72GiB），没有>10GiB写入。

候选保持SHA4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9；候选门禁PASS，不等于总体推送资格。第四步30/90对象、双模式、22RPM-DWARF预期清单与30×5性能均NOT RUN，几何平均比未知；第五步sandbox NOT ATTEMPTED，未查远端前后，没有Gerrit评审/tizen_base/BOLT源推送。源d6ddbff5父cb679968、spec/helper/patch/profile/manifest保持原样；没有新fixture PASS声明。

两份完整配置快照公开为fallback-config-before/after.tar.xz（约1.48MB各），包含build.ninja/rules、667/684安装脚本、全部导出与普通配置产物；缺失边清单、规则/导出差异、完整PATH/which/argv、资源与停止边界在fallback-config-install/stop.json。首轮采集错误、正式BOLT日志与候选身份链公开。全部scope回收，proc finally卸载；重候选单段锁已释放，其余均轻任务。周四按最新PM比较Quickbuild匹配统计同量级与5%门禁并复核性能，**不要求Quickbuild与本地clang SHA相等**。
