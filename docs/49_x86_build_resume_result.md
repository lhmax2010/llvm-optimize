# 续十一：串行续跑结果与新 RPM 验收

状态：**构建成功，续跑前后 8/8 输出逐字节 PASS；RPM 内容、归档与后处理 PASS；消费者等验收进行中，BOLT 尚未交接**。

本页承接 [续跑记录 §15–§16](49_x86_build_resume.md)，旧记录保留。2026-10-14 消息流断开后恢复核查，没有再次调用 rpmbuild。时间均为北京时间。

证据 E11=`temp/release-x86-full-build-20261013/round2-eight-output-proof`（本机目录，不上传大文件）。R=`/var/tmp/llvm-optimize-x86-archivefix-20261013/local/BUILD-ROOTS/scratch.x86_64.0`；B=`R/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build`。

## 1. 唯一一次续跑成功

构建经一次续跑完成（`-ba --noprep`、`mlgo_build_jobs=1`、Ninja 串行），第二轮已完成部分保留。仅额外覆盖 mlgo_build_jobs，`_smp_mflags=-j4`、CMake 6/6/2 池参数、Source/spec/补丁/配置不变；完整 argv、启动门禁见前页 §16。

|阶段|日志界限|wall|
|---|---|---:|
|%build，Ninja 902/902 完成|10-13 22:43:03 → 10-14 05:48:16|25,513 s|
|安装主体至第一个后处理|05:48:16 → 06:24:22|2,166 s|
|其中 Source BEGIN–END（含回写、清理）|05:52:53.0819569 → 06:24:22.3160992|1,889.234142 s|
|后处理至 Processing files|06:24:22 → 06:35:39|677 s|
|文件处理/打包至 %clean|06:35:39 → 06:49:08|809 s|
|整个续跑守护 wall|22:43:03 → 06:49:10|29,166.743332 s|

除 Source 时间戳与守护 wall 外，分段为秒级日志界限，不是独立计时器。Source summary 的转换计算段为 1,496.817557 s，不能与含回写的 BEGIN–END 混用。退出码 0、CMake 门禁 PASS、守护 problems 为空、采样器和日志读取器已回收。

|资源|实测|
|---|---:|
|scope MemoryPeak / MemoryMax|19,327,352,832 B / 18 GiB|
|MemorySwapMax|0|
|memory.events max / oom / oom_kill|41,222 / 0 / 0|
|最大链接进程 VmHWM（clang-22）|11,025,645,568 B|
|宿主最低 MemAvailable|17,628,061,696 B|
|/var/tmp 最低可用|59,213,987,840 B|
|2 秒宿主/磁盘采样数|14,580|

scope 峰值紧贴 cap，包含文件缓存，不能当作进程自然峰值；没有 OOM。宿主 2 GiB 与磁盘 30 GiB 底线均未触发。转换段逐进程采样最大 clang VmHWM=879,394,816 B、Python=818,315,264 B，属于采样下界。不拿本机 wall 作性能结论。

只读 `du -sx` 观察器在 06:27:31 后的一次调用超出 50 s 退出；它不承担保护功能，独立 2 秒 statvfs 底线守护持续到正常结束。du 还有三处权限盲区，故其占用记录仅为下界，不冒充完整根磁盘峰值。stderr 与已有样本保留，未改权限或重跑构建。

证据：`resume-result.json`、`resume-scope/{outcome.json,build.log,scope-after-rpm.json,process-memory.jsonl,linker-memory-observations.jsonl}`、`resume-resource-summary.json`、`resume-host-disk-2s.jsonl`、`root-space-samples.jsonl`。


大链接观测值（完整列表见 resume-resource-summary.json）：

|目标|VmHWM B|GiB|
|---|---:|---:|
|`bin/clang-22`|11025645568|10.268433|
|`bin/clang-repl`|6790569984|6.324211|
|`lib64/libclang-cpp.so.22.1`|6694825984|6.235043|
|`lib64/LLVMgold.so`|6192971776|5.767654|
|`bin/clang-tidy`|5604909056|5.219978|
|`bin/llvm-lto`|5200330752|4.843185|
|`bin/clang-import-test`|4830081024|4.498363|
|`bin/clang-refactor`|4464476160|4.157867|
|`bin/pp-trace`|4179681280|3.892632|
|`bin/lld`|4156665856|3.871197|
|`bin/tool-template`|4124962816|3.841671|
|`bin/clangd-fuzzer`|3984105472|3.710487|
|`bin/clangd`|3888377856|3.621334|
|`bin/clang-check`|3812683776|3.550838|
|`lib64/libclang.so.22.1.8`|3586367488|3.340065|
|`bin/clangd-indexer`|3501154304|3.260704|
|`lib64/SampleAnalyzerPlugin.so`|3283845120|3.058319|
|`bin/lldb-instr`|3190628352|2.971504|
|`lib64/CheckerDependencyHandlingAnalyzerPlugin.so`|3086241792|2.874287|
|`lib64/CheckerOptionHandlingAnalyzerPlugin.so`|3067547648|2.856876|

## 2. 八项输出与 Ninja 历史

定向重建前快照、定向重建后、整个 rpmbuild 后三者全部相同。BuildVariables.inc 与六个占位源文件也保持 7/7 同字节。

原 Ninja 日志 7,614 行含 8 条旧重复记录；正常日志压缩后，全部 7,606 条原最新完成记录的五字段原样保留。续跑新增 1,085 条日志记录（构建边多输出，记录数不等于 902 个任务），允许集合外 0、未获准重复 0。重复项仅为获准的 8 个输出与必执行的 LLDB 头暂存操作；未完成的输出已重新执行。

证据：`snapshot-manifest.json`、`directed-byte-comparison.json`、`post-resume-byte-comparison.json`、`ninja-history-proof.json`、`before-rpmbuild.ninja_log`、`after-rpmbuild.ninja_log`。多输出和日志压缩辅助检查的 5 项正负例见前页 §16.7。


|输出（相对 B）|字节|三次 SHA256|
|---|---:|---|
|`lib64/tf_runtime/CMakeFiles/tf_xla_runtime.dir/tf_xla_runtime_dummy.c.o`|4660|`2ac3bc66e414248cd6e6777e42f95e127589f187bd8d47b424632a213f8f99fc`|
|`projects/compiler-rt/lib/ubsan/CMakeFiles/RTUbsan_dynamic_version_script_dummy.x86_64.dir/dummy.cpp.o`|3144|`9a48fc753b9b94d94e64610b6c40565957b86477cfc8e0a26cae74d97487994f`|
|`projects/compiler-rt/lib/asan/CMakeFiles/RTAsan_dynamic_version_script_dummy.x86_64.dir/dummy.cpp.o`|3184|`fb8ec35b2502ef50408a6e53876202af146d9a9bd5d7441c7db96afed4205d09`|
|`projects/compiler-rt/lib/hwasan/CMakeFiles/RTHwasan_dynamic_version_script_dummy.x86_64.dir/dummy.cpp.o`|3224|`d59aac784416ad5c13fe2e3acf09548215099996d179f3ec02bb05c02ebf3f90`|
|`projects/compiler-rt/lib/nsan/CMakeFiles/RTNsan_dynamic_version_script_dummy.x86_64.dir/dummy.cpp.o`|3128|`18243b5b76578cd0e5a878e8c5e62bb500a754027379500d3640c7a10b8e866b`|
|`projects/compiler-rt/lib/memprof/CMakeFiles/RTMemprof_dynamic_version_script_dummy.x86_64.dir/dummy.cpp.o`|3296|`248803087f975d8fe73149e7b911240b267d469f78e21fbb938e6bed36e83789`|
|`tools/llvm-config/CMakeFiles/llvm-config.dir/llvm-config.cpp.o`|868400|`96c89523a891441d7e9dec67973a11ce9de408bef1dbad02dadab732846f4c6c`|
|`lib64/libtf_xla_runtime.a`|22484724|`f15c565d30a981c22c71cbcf823030302cf51d19a381f4cc82e44626688be1ed`|

## 3. RPM 验收进度

22 个二进制 RPM 与一个 SRPM 已由同次 rpmbuild 写出，正在建立 inventory、解包及验收。最终结果随后续写，暂不认定归档、消费者或 BOLT 交接通过。


### 3.1 RPM inventory

以下 22 包总计 8856385928 B，均为 x86_64 22.1.8-1；`rpm -qp --requires` 中 ShortCircuited 依赖均为 0。路径前缀 `R/home/abuild/rpmbuild/RPMS/x86_64/`，SRPM 在同级 SRPMS。摘要不代替文件与消费者验收。

|文件|字节|SHA256|
|---|---:|---|
|`clang-22.1.8-1.x86_64.rpm`|310005746|`d1e5cac296eb0744ac2722d904f4cfd415e58b505ba002f98bb6fa67fe1b66ed`|
|`clang-debuginfo-22.1.8-1.x86_64.rpm`|2928268018|`dfb0f2b487c77cb1aea3a41d203c2bb0ce193e8634e6e962f0bf3a547994a71e`|
|`clang-devel-22.1.8-1.x86_64.rpm`|4098954|`f15b23c5457f417d0cee1d62248d45dba4e12805609919921336c769a9aad62e`|
|`clang-devel-debuginfo-22.1.8-1.x86_64.rpm`|5730302|`b99cb48cfadbb409ea0e276db4ac492b68ae2af0261e39ff9ac7418f96278f07`|
|`compiler-rt-22.1.8-1.x86_64.rpm`|3786278|`1566ea95539a15ca5fe866fe4afac8dc1f25c06986cbbbcad05022b4cb07807e`|
|`compiler-rt-debuginfo-22.1.8-1.x86_64.rpm`|1288074|`7be800c5b1c5c569467575749634c7d23369e54df8af5372ceedf029df47fe68`|
|`libllvm-22.1.8-1.x86_64.rpm`|23651318|`5ecb4b77600fbe83aad8686efa8c6e42511388beefa3fdcab48c1a43b010e039`|
|`libllvm-debuginfo-22.1.8-1.x86_64.rpm`|198054338|`71a91ec71aa253e9db2e1fc8a5a460b5f3b088e838afdd321b4143b110ee8a8c`|
|`libomp-22.1.8-1.x86_64.rpm`|373658|`28a59e1aa728346ce92870a4261621339e2c604e6208136b57316c2e418b3f03`|
|`libomp-debuginfo-22.1.8-1.x86_64.rpm`|1142626|`9f9543d833a53c7db38f06a5a7465a10a05cc3e78fdc56db1e9f7b3c515d9213`|
|`libomp-devel-22.1.8-1.x86_64.rpm`|25470|`b4f4624e8f732e0615b3aa460406f458ed9ecda314bbbba89fa4824cfc817a16`|
|`lldb-22.1.8-1.x86_64.rpm`|30772842|`804fd63f9d1421d5f853f2c0a3c0d8e3f17cfdcd124239fe2c643ab5fb353cbf`|
|`lldb-debuginfo-22.1.8-1.x86_64.rpm`|332831986|`ce810b31e49eb24ef68e3661362f8cdebc8873e9f52916bcde08288f2e20c6df`|
|`lldb-devel-22.1.8-1.x86_64.rpm`|30517826|`6fede95403aa1ce02251fdb6b33fb40cb92fd5c77f503fbe2de2eadb014c3e38`|
|`lldb-devel-debuginfo-22.1.8-1.x86_64.rpm`|279572642|`26766352a6f85dfb70ec82821314d2f251d7be4875c7125a4ca205b9b2accad1`|
|`llvm-22.1.8-1.x86_64.rpm`|410603834|`4f3e419210909517c9665da8e59d0abbef7341008d8597442b6a179cd0692fe0`|
|`llvm-debuginfo-22.1.8-1.x86_64.rpm`|3842582214|`adc25a671c4f383be0cfe947a790618765bc40cd6de20736dcf5a7a8d26000e4`|
|`llvm-debugsource-22.1.8-1.x86_64.rpm`|43652310|`72ac2533efb5bae4d1c4f67446d540f4645168678e569b6e4b2e063dcbb12374`|
|`llvm-devel-22.1.8-1.x86_64.rpm`|41191590|`ccc57f0a314ca8744d326404aa4b64f66221671bde96d285c6bdd86db75f2af9`|
|`llvm-devel-debuginfo-22.1.8-1.x86_64.rpm`|308615178|`b1ef1fda0081a0f0f777e2ac970807121df2fc03eb78c91c1b553ea6ffe06d6d`|
|`llvm-static-devel-22.1.8-1.x86_64.rpm`|59584342|`b7c88d43127e7ca4135d411cbf9ec9b3981910d16a1c81497d4427666b9628e3`|
|`python-clang-22.1.8-1.x86_64.rpm`|36382|`f4f665175a081bfeca3d65c1f199c6a92f37e736ddf39b4e0458d865e59b9bbc`|
|`llvm-22.1.8-1.src.rpm`|427904813|`796f3b1a3c6399ddf44e33ecc5ddeab9d4f3b088174970b1cafed77621287890`|

## 4. 验收辅助脚本问题记录

首次 inventory 查询误用 RPM 的 32 位 SIZE 标签。两个大 debuginfo 包返回 `(none)`，Python 整数解析失败；当时未创建解包目录、未修改任何包。只读逐包查询证明 LONGSIZE 有效：clang-debuginfo=17,290,867,296 B、llvm-debuginfo=21,534,166,920 B，其余 20 包两标签数值相同。

仅将查询改为 LONGSIZE，保留所有 SHA、元数据、磁盘预算与 ShortCircuited 门禁，按辅助脚本条款重跑一次；不是重建或放宽验收。证据 `rpm-size-tag-diagnosis.json`、`inventory_extract.before-longsize.py.txt`、`rpm-size-tag-helper-fix.diff`、两个 rpm-extract scope。重跑成功：22 RPM、17,689 路径全部通过，wall 811.288139 s；解包摘要/类型/软链接目标均匹配 RPM 元数据。

### 4.1 归档辅助检查的比较器选用错误

首轮归档检查在首档 libLLVMAArch64AsmParser.a 的函数段抽查报 `addrsig missing symbol table`。该档成员身份、无 bitcode/DWARF、完整索引已通过；错误来自辅助脚本调用了面向未 strip 的 debug/release 比较器。readelf 只读诊断显示，新 RPM 与 docs/38 已验收 RPM 的 `.llvm_addrsig` 均为 SHF_EXCLUDE、sh_link=0；实际符号表仍完整存在。lld 源码 `llvm/lld/ELF/InputFiles.cpp:791–805` 明确忽略这种经过 objcopy/重排符号后失效的 addrsig 表。

docs/47 §9.1.3 的本项合同是可加载内容、符号属性、重定位和完整索引，函数段抽查也不应依赖有效的非加载 addrsig。改为 E11 内专用只读 ELF 解析器：保留全部合同字段，addrsig 仅登记；发布模式比较器、两 Source 与 Commands 均未改。6 个正负例 PASS（自身及已失效 addrsig、可加载载荷改变、flags 改变、符号值改变、重定位偏移改变、残留调试节）；只重跑一次全量归档检查，225 开发档与 45 运行库全部 PASS。

证据：`archive-acceptance-first-failure.json`、`archive-check-diagnosis/` 三份对象及 readelf 原文、`archive-check-helper-diagnosis.json`、`archive-check-helper-fix.diff`、`packaged_elf_evidence.py`、`test_packaged_elf_evidence.py`、`packaged-elf-tests.log`。新旧辅助输出分别保存在 archive-checks 与 archive-checks-retry，不覆盖失败证据。

## 5. 已完成的后处理验收

执行证据与完整展开脚本一致：Source 先 BEGIN–END PASS 225，再进入 find-debuginfo/brp；brp-strip-static-archive 使用 `/usr/bin/llvm-strip`。exec/exit 追踪中 270 个包内归档恰好各调用一次，全部 exit 0；另一次 `--version` 探针独立计数。格式错误/strip 错误行 0。brp-compress、brp-python-hardlink、find-docs、find-debuginfo 各 1 次，debug 配置下 brp-strip 为 0，与原宏链行为一致。Source summary 为 PASS，大载荷已按 Source 原逻辑删除，只留 JSON 证据。

证据：`postprocessing-result.json`、`native-archives-install.log`、`rpm-exec-exit.trace`、`generated-rpm-scripts/`。27 项受保护身份复核一致（Source、spec、配置、宏、补丁等）；获准构建生成文件单列不与旧检查点强行等 SHA，见 `post-build-protected-identities.json`。

## 6. 新 RPM 归档全检 PASS

|检查|结果|
|---|---|
|225 开发归档、3,864 有序成员|身份/次序相同；全部 x86_64 ELF ET_REL；bitcode=0、other=0、非 thin；无调试节|
|完整符号→成员索引|逐档等于全部成员的外部定义符号多重集合；保留同名成员序号|
|转换强符号|缺失 0；允许的弱 W 缺失合计 1,920，逐成员原始记录保留|
|每函数一段|10 个成员抽查通过；跨子系统直接编译结构诊断另行执行|
|45 compiler-rt 归档、1,964 成员|与本次构建树比较：成员身份/次序、全部可加载内容、符号属性、相关重定位、完整索引相同；无调试节|
|libarcher_static.a|llvm-static-devel 与 libomp-devel 双归属、RPM 元数据及文件内容一致|

这里运行库对照为**本次新快照环境自己的构建原件**，不能混同旧快照的全文件字节比较。非加载节的 strip 结构变化保留诊断，未据其放宽可加载内容或符号/重定位检查。原件始终只读。

证据：`archive-acceptance.json`、`archive-checks-retry/`、`ba-conversion-summary.json`、`archive-check-corrected-once-scope/`。本次独立检查 wall 16 秒量级、scope峰 6,049,361,920 B；最终 wall 以 outcome.json 为准。

宿主消费者正在执行；Tizen、独立-bi/SKIP、同环境非归档基线与结构诊断尚未完成。BOLT NOT_READY。

## 7. 宿主消费者 PASS，Tizen 测试启动

七项宿主测试全部 PASS：A 的 bfd/lld 输出与本次新 RPM opt -O2 一致；B 的 bfd/lld 进程内链接生成物均退出 37；共享库以 -shared -z defs -z text 链接并 dlopen 执行正确；GC 版本输出一致；原 bitcode 归档在无插件 GNU ld 下按预期失败。A 普通版本 47,389,584 B，GC 版本 28,380,432 B。消费者不依赖 LLVM 共享库，完整 argv/驱动展开与资源日志保留。scope wall 24.273742 s，峰 983,031,808 B。

环境：LLVM 头文件/静态库/clang/opt 都来自本次 N=`temp/toolchain-release-x86-20261013`；C++ 与 libc 头文件、运行时 glibc/libstdc++ 来自宿主（编译 -v 和 loader --list 原文）；显式宿主 loader `/lib64/ld-linux-x86-64.so.2`，独立 Tizen libxml2 路径 `temp/toolchain-runtime-baseline/libxml2/usr/lib64`。编译 4 GiB AS，链接不设 AS、由 cgroup 控制；GNU ld 无 LTO/插件。参数名 baseline 在脚本中实际指向 N，不是旧 RPM。

compiler-rt 宿主 10 项（两链接器 × ASan 坏/好、UBSan、profile、builtins）全部 PASS：坏程序确实报告 heap-buffer-overflow，正常程序 0；UBSan 报有符号溢出；profraw 与 merge 成功；__divti3 调用及结果正确。资源目录显式指向 N/usr/lib64/clang/22。

证据：`new-rpm-consumers/`、`runtime-host/`、两个同名 scope。22 新 RPM 在同文件系统硬链接到 `/var/tmp/llvm-optimize-x86-archivefix-20261013-new-rpm-repo`，inode 一致，没有再复制 8.86GB。createrepo_c 成功，清单在 `new-rpm-identity.json`。Tizen bfd 于11:58:46启动，6GiB/swap0/≥8GiB准入、与原构建相同的冻结 Base/Unified 配置；根放在 `/home` 的新路径，后续 lld 串行，尚无结果。

### 7.1 Tizen bfd PASS

11:58:46→12:06:39，wall 473.178732 s。构建与 %check PASS，根内 270 归档 + 5 工具 SHA 与新 RPM 全同，A 输出逐字相同、B 生成物退出 37；ASan/UBSan/profile/builtins 均通过。scope MemoryPeak=6442450944 B（6GiB cap，含文件缓存）；memory.events 原文：`low 0; high 0; max 142; oom 0; oom_kill 0; oom_group_kill 0`。whole-archive 仅诊断，原文在 check-outputs/，不作门禁。证据 tizen-bfd/{result.json,installed-identities.json,build.log,scope-after-rpm.json,check-outputs/}。

第二个独立 lld 测试包于12:07:43开始，使用同一冻结配置、6GiB/swap0/8GiB准入，串行执行，尚无结论。

### 7.2 Tizen lld PASS；独立安装启动

12:07:43→12:11:41，wall 237.756389 s；scope峰 6028075008 B，memory.events=`low 0; high 0; max 0; oom 0; oom_kill 0; oom_group_kill 0`。构建/%check、A/B、全部运行库探针 PASS；12:13:03 完成根内 270 归档 + 5 工具 SHA 全同复核，A 输出与根内 opt 完全一致。证据 tizen-lld/{result.json,installed-identities.json,build.log,scope-after-rpm.json,check-outputs/}。因此验收5（七宿主、Tizen两包及运行库）PASS。

独立真实-bi已按原同宏入口启动准备，使用 `R/home/abuild/review49-independent-install/install-root`，不覆盖原-ba安装树；Source原-ba证据先备份到E11/ba-install-conversion-evidence。启动前/var/tmp可用112,110,084,096B，满足1.2×46.316GiB+30GiB；此步仍需等待实际转换与逐档检查，不能提前认定幂等PASS。
