# 续十一：串行续跑结果与新 RPM 验收

状态：**构建成功，续跑前后 8/8 输出逐字节 PASS；新 RPM 验收进行中，BOLT 尚未交接**。

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

## 4. 验收辅助脚本问题记录

首次 inventory 查询误用 RPM 的 32 位 SIZE 标签。两个大 debuginfo 包返回 `(none)`，Python 整数解析失败；当时未创建解包目录、未修改任何包。只读逐包查询证明 LONGSIZE 有效：clang-debuginfo=17,290,867,296 B、llvm-debuginfo=21,534,166,920 B，其余 20 包两标签数值相同。

仅将查询改为 LONGSIZE，保留所有 SHA、元数据、磁盘预算与 ShortCircuited 门禁，按辅助脚本条款重跑一次；不是重建或放宽验收。证据 `rpm-size-tag-diagnosis.json`、`inventory_extract.before-longsize.py.txt`、`rpm-size-tag-helper-fix.diff`、两个 rpm-extract scope。重跑结果随后登记。
