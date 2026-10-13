# 49 续九、续十：第二轮部分构建树续跑前核查

**续十最新：STOP_RECONFIGURE_PENDING_OUTPUTS；实际配置成功、命令不变，干跑新增8个已完成输出越界；rpmbuild调用0次。见§8–§14。**

**续九历史最终状态：STOP_RESUME_PREFLIGHT；续跑调用0次。** 指定的`--define '_smp_mflags -j1'`不会把本配方的Ninja改成串行：根内展开后仍是`ninja -j 6`。此外，干跑894项超过本轮规定上限811，历史单链接峰值也超过当前可用内存减2GiB的预算。按“任一不满足则不启动”停止，没有改宏、spec或资源后重试。

日期：2026-10-13，北京时间。开场main=`aa1da3578640db812030a6792f5d703d21322b70`。承接[第二轮停止报告](49_x86_build_round2_result.md)和[构建环境记录](49_x86_build_continuation.md)；旧报告保留。本页与STATUS同提交推送GitHub，不推Gerrit。

## 1. 裁决、现场和证据

PM本轮判断：第二轮两个大链接与编译任务并发撞峰，造成宿主可用内存降至1.99GiB；与补丁、环境、磁盘无关。这是本轮人工裁决前提，原始观测及其口径仍保留于前页。新授权为一次分段续跑：`-bc --short-circuit`用_smp_mflags=-j1，`-bi --short-circuit`恢复-j4，然后打包；不得从头重建或自行换入口。

W=`/home/linhao/Toolchain/development/llvm-optimize`。

```text
E9 = W/temp/release-x86-full-build-20261013/round2-resume
E8 = W/temp/release-x86-full-build-20261013/round2-launch
R  = /var/tmp/llvm-optimize-x86-archivefix-20261013/local/BUILD-ROOTS/scratch.x86_64.0
B  = R/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build
```

E9是本轮新证据目录，原始文件只存本机。开场主库仅用户既有gbs_llvm.conf修改，没有竞争构建进程；两项目锁21:00:50取得。14项Source/配置/比较器/补丁保护摘要与上轮相同，B的CMakeCache.txt、build.ninja、.ninja_log与E8停止副本相同，共17项开场检查PASS。结尾另核专用配置/buildconfig/仓库/候选身份，共26项检查PASS（含重复核对），没有编辑保护文件。证据initial-integrity.json、final-integrity.json。

|根内输入|SHA256|
|---|---|
|SOURCES/llvm.spec|822f22fe7a5a7d9cbebfdcae202d5d43cf428f05693070a60e4369517e8f3cd9|
|SOURCES/llvm-static-archives-native.py|c43523c0ce04fc3310e670ff97823db8260c21250dc3172575a18db56500082e|
|home/abuild/.rpmmacros|9b49f3dd05542ffe0ad772444207b856a3f23591872aa8af12e61ec8de4e61ec|
|usr/lib/rpm/macros|f2f13c69904e872a8196011d0f8e3dcc6feee4edf53380418c78ea737b44593a|

根内spec包括GBS唯一VCS行，故不等于checkout spec e88ef4cb…的整文件SHA；其导出身份沿用E8/round2-export-identity.json，没有重新导出。候选仍PS3=3731eda7…、PS2=4c36e899…，专用配置仍d1ff39ac…，Base/Unified快照及repomd均不变，完整身份见前页§2。

本轮只做轻量只读核查，未取得共享重任务锁、未启动构建scope。没有访问BOLT的工作树、分支和证据目录；没有清理磁盘、修改宿主配置或修改任何Source/Commands/比较器。

## 2. 当前根内只读核查方法

用同一专用配置进入既有R，以abuild登录shell执行。根内身份实读uid/gid=1000(abuild)，rpm与rpm-build均4.14.1.1-1.6.x86_64，rpmbuild版本输出4.14.1。没有调用rpmbuild构建阶段。

```sh
gbs -c "$W/temp/release-x86-full-build-20261013/latest-base/gbs-build.conf" \
  chroot --root "$R"
# 在上述入口内，以 su -s /bin/bash -c '<以下命令>' - abuild 执行：
cd /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build
ninja -n
rpmspec --parse --target=x86_64 --define '_smp_mflags -j1' \
  --define '_srcdefattr (-,root,root)' --define '_build_create_debug 1' \
  /home/abuild/rpmbuild/SOURCES/llvm.spec
# 第二份展开仅将上一条的 -j1 改为 -j4
```

完整shell输入root-preflight-input.sh、外层argv/时间/退出码root-preflight-result.json、输出root-preflight.log。21:01:51–21:01:52完成，GBS exit0且内部显式`@@ROOT_PREFLIGHT_EXIT=0`，不依赖GBS单独的返回码。没有运行CMake；干跑前后三个构建状态文件SHA完全相同，见after-dry-run-identities.json。

## 3. 门禁(a)：待办数量

|项|实测|
|---|---:|
|此前总数/最后完成数|7634 / 6829|
|用户给定剩余基数|805|
|中止时仍运行的Ninja任务|6：两个clang++链接驱动、四个clang++编译驱动|
|本轮准许上限|805+6=811|
|本次唯一ninja -n待办|894|
|超过上限|83，FAIL|

六个驱动PID为2078690、2079537、2079568、2079610、2079611、2079618，来源E8/scope-journal.log中中止时的进程列表。两个ld.lld是对应clang++驱动的子进程，不重复算作独立Ninja任务。

894项按输出动词分类：483 Building、223 Linking、88 LLDB、62 Generating、30 Copying、7 Creating、1 Running。Linking包括静态归档，不能全部当成ELF重链接。完整清单ninja-dry-run.log、分类dry-run-operation-counts.json。

只读比对与E8/ninja-progress.json的操作文本多重集合：重合89项，恰为88次`LLDB headers: stage LLDB headers in include directory`及一次`Running utility command for liblldb-header-staging`。894=805+89。没有其他操作文本重合，Cache/构建图/日志SHA也未变；因此**不能把894直接解释成配置重生成造成的大面积重编**。这只是诊断，并未从门禁总数中扣除89项，也未重新执行干跑寻求通过。证据dry-run-prior-operation-overlap.json、after-dry-run-identities.json。

## 4. 门禁(b)：CMake参数不变，但指定宏不能实现串行

当前根内spec原文：

```spec
# R/home/abuild/rpmbuild/SOURCES/llvm.spec:63
%{!?mlgo_build_jobs: %define mlgo_build_jobs 6}
# 同文件:403
ninja -j %{mlgo_build_jobs}
```

checkout spec对应为62、402行，差一行GBS追加VCS。%build没有引用_smp_mflags。当前根内`usr/lib/rpm/macros:182–184`把`%{?_smp_mflags}`传给find-debuginfo；同文件1099行的make_build也引用它，但此处构建使用直接Ninja命令。原文与行号保存macro-source-excerpts.json。

|检查|结果|
|---|---|
|传_smp_mflags=-j1后展开%build|`ninja -j 6`|
|传_smp_mflags=-j4后展开%build|`ninja -j 6`|
|两份完整展开spec|逐字节相同，SHA bb99b71d0f400ed1fbcad3bc156622563aeeabf1d045cf7e8122f50a011e4a0f|
|两份%build以及原第二轮%build|逐字节相同，SHA 8841d6101457a190ffd34617fb3afc9583701e882a06360d758b3a02a26cb935|
|CMake参数静态展开|与原第二轮相同，build-vs-round2.diff为空|
|实际重新configure及其后Cache对照|NOT RUN，尚未通过续跑前门禁|
|“同一时间只运行一个Ninja任务”|FAIL，指定方式仍为-j6|

展开文件expanded-j{1,4}.spec、build-j{1,4}.sh和build-macro-diff.txt均保存。第二轮Cache的Release/Thin/O3、静态工具开关、6/2 pool原值未改。不能以CMake参数相同代替串行门禁通过。

从spec条件默认定义可知，若以后另行裁决，可以评估在命令行设置`mlgo_build_jobs=1`来控制该Ninja调用；它与本次明确指定的_smp_mflags不是同一宏。本轮**没有添加这个覆盖，也没有改spec或用其他工具限并发**，不把它作为已经获准的新续跑方式。

## 5. 门禁(c)(d)：历史最大链接与宿主预算

只读逐行扫描docs/34的完整构建及恢复段linker-memory-observations.jsonl，每PID/目标取VmHWM最高观测值，完整输入摘要与前20项保存historical-link-peaks.json。扫描耗时202.065s，流式读取，不重新运行链接。

|历史输入|JSONL行数|SHA256|
|---|---:|---|
|temp/archive-fix-v2-build-20260929/full-build/linker-memory-observations.jsonl|67339|73b3ba7447a9c52a2c0abe24ac6f33896c938802ac348259e70b0d019dc06a13|
|同目录resume-20261008/build/linker-memory-observations.jsonl|9725|b15d6ec91f669e3577a649a418c56805aaed87758154ba47ee16e934f3b6af6d|

|阶段/目标|PID|原JSONL行|VmHWM B|GiB|
|---|---:|---:|---:|---:|
|首段liblldb.so.22.1.8，全部历史最大|59585|287|13989494784|13.028732|
|首段clang-import-test|132594|63176|12181155840|11.344585|
|首段clang-repl|134333|63902|11751677952|10.944603|
|首段libLLVM.so.22.1|130184|62510|11738476544|10.932308|
|首段lld|131809|62756|11453452288|10.666859|
|首段clang-22|64423|813|11440594944|10.654884|
|首段bugpoint|63027|713|11396227072|10.613564|
|首段libLTO.so.22.1|63174|646|11090485248|10.328819|
|恢复段clang-repl，恢复段最大|84196|1827|11036512256|10.278553|

这些是18GiB scope环境中的进程VmHWM采样值，不是无约束自然峰值，也不相加。按用户本轮规则直接与宿主预算比较，不因为已完成某个较大链接就擅自缩小历史门槛；即便只看尚需完成的clang-22，其历史值也高于下表预算。

|宿主读数|21:01:05开场|21:06:36门禁记录|
|---|---:|---:|
|MemTotal B|33072914432|33072914432|
|MemAvailable B|11934527488|11838124032|
|MemAvailable GiB|11.114895|11.025112|
|当前可用减2GiB B|9787043840|9690640384|
|当前可用减2GiB GiB|9.114895|9.025112|

固定10GiB重阶段准入单项满足，但历史最大13.028732GiB、clang-22 10.654884GiB均超过9.025112GiB单链接预算，因此门禁(c)FAIL。不等待自然波动后重新判定，也没有启动重阶段；此读数是续跑前参考，不是假称已完成启动准入。MemTotal、完整/proc/meminfo、两次RSS前10进程和/var/tmp可用空间分别保存在host-before.json、host-admission-reference.json、meminfo-*.txt。进程表只记录PID/PPID/名称/RSS，不干预其他项目。

## 6. 分段RPM机制与本轮未执行项

当前rpmbuild --help原文：`--short-circuit skip straight to specified stage (only for c,i)`。本轮没有调用-bc/-bi/-bb，只进行rpmspec文本展开。docs/34 §3.3采用的是正常`-ba --noprep`，不是本轮指定的分段short-circuit；没有擅自退回旧方式。

打包方式仍未实证：docs/13 §4记录该系列RPM的`-bb --short-circuit`跳过安装并增加rpmlib(ShortCircuited)依赖，不能冒称普通正式RPM等价路径。本轮在前置门禁已经停止，没有以这条历史记录断言新根实际打包成功或失败，也没有采用另外的打包手段。后续若重新安排续跑，需同时明确最终打包路径。

|本轮步骤/验收|状态|
|---|---|
|续跑前现场、输入、干跑前后构建文件身份|PASS|
|干跑任务上限(a)|FAIL：894>811，额外LLDB暂存操作另列诊断|
|参数静态一致性(b)|PASS；实际重配后Cache对照NOT RUN|
|串行执行条件(b)|FAIL：_smp_mflags=-j1仍展开ninja-j6|
|单链接宿主内存预算(c)|FAIL：13.028732>9.025112GiB；clang-22亦超预算|
|宿主内存及前10进程记录(d)|已完成|
|续跑%build、%install、打包|NOT RUN，调用均0，耗时/资源峰值N/A|
|新RPM清单/SHA|无新增RPM；上轮RPMS/SRPMS为空的记录保留|
|验收1 身份/环境|已有冻结身份与静态展开核查PASS；“经一次续跑完成”条件未成立|
|验收2 后处理|NOT RUN|
|验收3 开发归档/运行库|NOT RUN|
|验收4 同环境独立安装基线|NOT RUN，未到其他验收通过的执行时点；条件授权及不阻塞交接规则保留|
|验收5 宿主/Tizen/运行库消费者|NOT RUN|
|验收6 独立真实安装与同树SKIP|NOT RUN|
|验收7 直接非LTO结构诊断|NOT RUN|
|两ARM全量/根内小试/64MiB负例|NOT RUN|
|bash依赖清单/LLVM23探测|NOT RUN|

**BOLT交接NOT_READY。** B及其lto.cache保留，仍是第二轮部分构建现场；没有新增构建完成时间，不能标注“经一次续跑完成”。发布模式完整构建继续挂账，既有60对发布认证结果不变。停止结论stop.json明确resume_invocations=0。

## 7. 回收和提交

21:07:18两项目锁释放；21:07:38终检本任务进程0、挂载0、项目锁0。本轮未取得共享重任务锁、未新建scope或资源采样器，历史采样汇总进程正常退出。没有启动重编/转换、没有使用辅助脚本修正重跑例外。证据lock-released.json、cleanup-final.json。

只提交本页与STATUS。工作树保留用户原有gbs_llvm.conf改动，不将其提交。Source、spec、候选补丁、专用配置与部分构建树原件不变，旧停止记录不重写。GitHub提交后以本页及STATUS的同一提交为本轮交付；原始E9证据不上传大文件。


## 8. 续十：新裁决、输入与唯一配置预检

**2026-10-13最终状态：STOP_RECONFIGURE_PENDING_OUTPUTS，rpmbuild续跑调用0次。** 实际CMake重新配置成功，全部展开命令保持同字节，但干跑由894变为902：新增8个此前已经完成的输出操作，既不是中止时的未完成操作，也不是授权的两类LLDB头暂存。按“出现其他任何操作则停止”执行，没有改规则、重跑配置、启动-ba、回滚生成文件或修改spec。本轮内存参考读数充足；停止不归因于内存不足。§1–§7为续九原始停止记录，保留不变。

开场main=5b61c584c3d0d3098d1dc858ebde01596a5e37fa。新证据目录：

```text
E10 = W/temp/release-x86-full-build-20261013/round2-resume-serial
R = /var/tmp/llvm-optimize-x86-archivefix-20261013/local/BUILD-ROOTS/scratch.x86_64.0
B = R/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build
G = R/home/abuild/review49-resume-serial
```

本轮PM将续九分段short-circuit方式替换为docs/34验证过的正常`-ba --noprep`，只追加mlgo_build_jobs=1，保持_smp_mflags=-j4；编译/链接pool仍6/2，全局Ninja串行。干跑判据改为未完成输出与中止输出的并集，另允许两类LLDB操作；内存L只取待完成链接在docs/34的历史峰值，需可用≥L+2GiB，不足每5分钟最多60分钟。任一前置失败不启动。验收4有条件执行及不阻塞BOLT的裁决保持，后续不得把部分构建树标为已交接。

22:11:39两项目锁取得。开场28条输入/状态检查全部一致，主仓库仍只有用户既有gbs_llvm.conf修改，无本项目竞争进程。两Source、Commands、比较器、原工作区spec、根内spec、候选与已上传补丁、专用配置全部未改。Base仍20261010.120615，Unified仍20260814.092727，repomd摘要沿用前页§7。根内spec仍822f22fe…、Source仍c43523c0…；结束27条受保护身份核对PASS。（E10/initial-integrity.json、final-protected-identities.json。）

第二轮日志原始调用位于E8/full-build-scope/build.log:459；真实进程argv另存E8/actual-rpmbuild-argv.json，PID2057128：

```sh
rpmbuild --define '_smp_mflags -j4' \
  --define '_srcdefattr (-,root,root)' --nosignature --target=x86_64 \
  --define '_build_create_debug 1' -ba \
  /home/abuild/rpmbuild/SOURCES/llvm.spec
```

本轮准备但**未执行**的唯一续跑形式如下，不含--short-circuit：

```sh
rpmbuild --define '_smp_mflags -j4' \
  --define '_srcdefattr (-,root,root)' --nosignature --target=x86_64 \
  --define '_build_create_debug 1' -ba --noprep \
  --define 'mlgo_build_jobs 1' /home/abuild/rpmbuild/SOURCES/llvm.spec
```

根内同宏rpmspec展开证明%build只差`ninja -j 6`→`ninja -j 1`，CMake前导和命令其余逐字相同。证据expanded-serial.spec、expanded-build-serial.diff。不是修改根内spec，也没有以_smp_mflags覆盖Ninja。

## 9. 实际重配：命令不变，生成文件有变

### 9.1 原环境与执行证据

E8日志:476记录真实%build入口`/bin/sh -e /var/tmp/rpm-tmp.TKKl0B`。该原始脚本仍在R内，本轮复制为E10/original-rpm-build.sh，保留RPM生成的环境前导（含原始CFLAGS/CXXFLAGS、LDFLAGS、RPM变量）、工作目录与CMake命令，仅在最终Ninja前截断生成G/configure.sh。避免只用spec的%build片段而遗漏RPM注入的optflags。执行仍为专用配置GBS chroot、abuild登录shell、`/bin/sh -e`；原脚本与提取版均存证。

```sh
gbs -c "$W/temp/release-x86-full-build-20261013/latest-base/gbs-build.conf" \
  chroot --root "$R"
# 上述入口内：su -s /bin/bash -c '<E10/configure-input.sh所载命令>' - abuild
# 配置前后分别保存：
ninja -t commands
ninja -t compdb
ninja -n -v
# 唯一实际配置：
/bin/sh -e /home/abuild/review49-resume-serial/configure.sh
# 配置后另存可读描述：
ninja -n
```

配置与干跑持heavy-stage flock；scope18GiB/swap0、nice15/ionice3、2秒宿主2GiB及磁盘30GiB保护、30秒资源采样。没有执行Ninja编译任务；`-t`工具与`-n`为图读取/干跑。外层GBS exit0且根内完成标记exit0；scope未记录OOM。共享锁已释放，未占用BOLT资产。（configure_once.py、configure-input.sh、configure-scope/*、configure-shared-lock*.json。）

### 9.2 比对结果

|检查|结果|
|---|---|
|ninja -t commands完整文本|逐字节一致，SHA c4d4f9c28f04803686b3642e3908db1e884cf3d4cfb0b22f42e23c95b21b4c9e|
|ninja -t compdb全部21,987条记录|逐条及整体字节相同；SHA 7fecb60159dbe6934e9d3273886fec40c9a0e4321a90dc96f6f04ca402688ec5|
|CMakeFiles/rules.ninja|逐字节相同|
|Release/Thin、C/CXX/ASM各flags、link flags、6/2 pools、dylib开关|值全部相同|
|Cache四项工具变量|见下表；类型/路径写法变化，实际展开命令未变|
|build.ninja|字节不同；PDB辅助变量及RERUN_CMAKE/phony依赖列表变化，完整diff存证|
|.ninja_log|逐字节相同，证明本轮没有执行构建图任务|

|Cache键|重配前|重配后|
|---|---|---|
|CMAKE_C_COMPILER|STRING=/bin/clang|UNINITIALIZED=clang|
|CMAKE_CXX_COMPILER|STRING=/bin/clang++|UNINITIALIZED=clang++|
|CMAKE_AR|FILEPATH=/usr/bin/llvm-ar|UNINITIALIZED=/usr/bin/llvm-ar|
|CMAKE_RANLIB|FILEPATH=/usr/bin/llvm-ranlib|UNINITIALIZED=/usr/bin/llvm-ranlib|

这四项由相同无显式类型的-D参数重新写入Cache；不把整个Cache SHA不同直接等同于编译选项变化。编译/链接命令的完整比对为PASS；也不以此掩盖下一节的额外待办FAIL。configure-comparison.json的初始汇总状态REQUIRES_DIFFERENCE_CHECK表示需对生成文件差异逐项解释，最终判定在本节及§10。

|文件|重配前SHA256|重配后SHA256|
|---|---|---|
|CMakeCache.txt|8140b1d3ac4c9e3520c9bdb13ec3cb67c1740469e4be734e952275456bb641a4|f7e93b874c5aefdbe4515e6bedb8318ee7c207a95442162e460480545cceb59f|
|build.ninja|273ab43bc9acd82bd94e2eee9994c93c961ea048f979c3f7f532bfec795a17a2|9fcc86836b133cff1968f7393e608969341f2775cfbbd11d2e3a00199b36f551|
|.ninja_log|2a85260f032e210430855173f023b26c47f6c37205eba0c7d1206b216b1525cf|2a85260f032e210430855173f023b26c47f6c37205eba0c7d1206b216b1525cf|
|CMakeFiles/rules.ninja|0fa4d9e87d82294fb64468e03fa2f6b7c1045c3f80b5053083579651e29743fe|0fa4d9e87d82294fb64468e03fa2f6b7c1045c3f80b5053083579651e29743fe|

本轮不回滚CMake正常生成的文件；后续恢复应以new-build-checkpoint.json为新检查点，不再要求本轮生成图等于E8旧摘要。部分对象、归档及ThinLTO缓存保留。

## 10. 干跑门禁：按输出匹配的8项越界

用每条`ninja -n -v`实际命令精确查`ninja -t compdb`输出键：配置前894条、配置后902条均一对一匹配，未匹配0、歧义0；不靠文本描述猜输出。配置前894条中，805个输出不在完成日志，89个已记录输出恰为88个LLDB头暂存及1个liblldb-header-staging。配置后保留这894条，新增下表8条；它们全部在配置前.ninja_log中有完成行，也在E8完成进度中，且配置前不在待办集合内。（before/after-pending-outputs.json、before-pending-already-logged.json、added-pending-outputs.json、operation-repeat-check.json。）

|新增输出（相对B）|原完成记录|本轮干跑|
|---|---|---|
|`lib64/tf_runtime/CMakeFiles/tf_xla_runtime.dir/tf_xla_runtime_dummy.c.o`|存在；原结束84437ms|新增|
|`projects/compiler-rt/lib/ubsan/CMakeFiles/RTUbsan_dynamic_version_script_dummy.x86_64.dir/dummy.cpp.o`|存在；原结束1987777ms|新增|
|`projects/compiler-rt/lib/asan/CMakeFiles/RTAsan_dynamic_version_script_dummy.x86_64.dir/dummy.cpp.o`|存在；原结束1990068ms|新增|
|`projects/compiler-rt/lib/hwasan/CMakeFiles/RTHwasan_dynamic_version_script_dummy.x86_64.dir/dummy.cpp.o`|存在；原结束1992099ms|新增|
|`projects/compiler-rt/lib/nsan/CMakeFiles/RTNsan_dynamic_version_script_dummy.x86_64.dir/dummy.cpp.o`|存在；原结束2002694ms|新增|
|`projects/compiler-rt/lib/memprof/CMakeFiles/RTMemprof_dynamic_version_script_dummy.x86_64.dir/dummy.cpp.o`|存在；原结束2011688ms|新增|
|`tools/llvm-config/CMakeFiles/llvm-config.dir/llvm-config.cpp.o`|存在；原结束2017403ms|新增|
|`lib64/libtf_xla_runtime.a`|存在；原结束91563ms|新增|

新增为7次编译与1次静态归档；不是额外大型ELF链接。仍然违反本轮限定集合，**门禁(b)FAIL**。未擅自把它们解释成允许重做的“正常操作”；没有第二次CMake或修改mtime、spec、Ninja图求通过。

原中止6个驱动中，2秒采样覆盖5个输出：bugpoint、libLTO、llvm-profdata.cpp.o、CheckerDependencyHandling.cpp.o、CheckerOptionHandling.cpp.o；PID2079618只在停止journal中出现，没有进入最后一轮进程采样，输出路径标UNKNOWN，不编造。上述8项在重配前干跑集合外且早已完成，已足以判越界，不依赖猜测这个缺失PID。（interrupted-output-paths.json、interrupted-unsampled-pids.json。）

只读原因线索：MLGO资产`mlgo_sysroot/xla_aot_runtime_src/CMakeLists.txt:6`在configure时file(WRITE)重写tf_xla_runtime_dummy.c；compiler-rt各runtime的CMakeLists也file(WRITE)空dummy.cpp；这些输入的mtime晚于对应旧对象。llvm-config.cpp.o显式依赖由configure_file生成的BuildVariables.inc（llvm/tools/llvm-config/CMakeLists.txt:88、100–101），本轮该文件mtime也晚于旧对象。未保存这些生成输入的重配前内容，因此不冒称其前后字节全同，也不把线索提升为放行结论。（added-input-output-stat.json、生成源码原文。）

纯证据汇总辅助修正一处：初版finalize_preflight.py误要求6个journal PID都被2秒采样捕获；只读核查证明2079618未采到。修正为显式记录缺失PID，输出UNKNOWN，没有改构建/门禁脚本或重跑配置。旧版与summary-helper.diff保留。越界8项的判断在此前已成立。

## 11. 待完成链接预算与资源

### 11.1 历史匹配与宿主参考

干跑中159个clang驱动ELF链接输出（排除静态归档）；docs/34两段历史采样按目标路径匹配139个，20个未采到，记UNKNOWN，不以0代替。全清单见§14及E10/pending-link-historical-peaks.tsv和pending-link-historical-peaks.json。L按匹配到的历史最大VmHWM为clang-import-test的12,181,155,840B（11.344585GiB）；对应L+2=14,328,639,488B（13.344585GiB）。历史liblldb的13.028732GiB已不在待完成集合，按本轮裁决不纳入L。未采样目标仍缺独立峰值事实，不能宣称159项均有实测上界。

历史输入与§5相同，重新流式扫描67,339+9,725行，SHA逐字一致；耗时72.250秒，不运行任何链接。下表为停止后的宿主参考读数，**不是一次已执行续跑的启动记录**；干跑已失败，未进入等待或启动阶段。

|项目|字节|GiB|
|---|---:|---:|
|MemTotal|33072922624|30.801559|
|MemAvailable|24788119552|23.085735|
|SwapTotal|4294963200|3.999996|
|SwapFree|4294963200|3.999996|
|/var/tmp可用|266105122816|247.829708|

22:17:02参考MemAvailable高于L+2，也高于10GiB。没有因为内存不足停止；没有必要按5分钟等待。宿主Swap实有4GiB，但本任务scope始终MemorySwapMax=0。（host-preflight-end.json、meminfo-preflight-end.txt。）

前10占用进程（RSS单位KiB，不干预）：

```text
    PID    PPID COMMAND           RSS
   4631    4315 code            1487640
   4839    4318 code            770104
   4573    4094 chrome          494896
   4075    2563 chrome          413752
   5625    4094 chrome          411764
   2438       1 epp-client-daem 389464
   4837    4763 codex           317616
   4838    4764 codex           313556
   2978    2563 gnome-shell     300172
   4481    4318 code            297392
```

### 11.2 本轮唯一配置scope

- wall **8.176532s**；scope MemoryPeak **962985984B（0.896851GiB）**；MemoryMax18GiB，swap0，memory.events的max/oom/oom_kill均0。
- 30秒采样仅1点：宿主MemAvailable 24.135578GiB，/var/tmp可用 247.896679GiB；不把它们称为连续真实最低值。2秒保护线程全程无告警。
- %build补完、%install转换、后处理、打包均未执行，耗时与大链接VmHWM为N/A；没有新RPM，ShortCircuited依赖检查NOT RUN，不以“计划不用short-circuit”代替产物检查。
- scope资源/日志线程已join回收；configure-scope/outcome.json与scope-after-rpm.json保存内层exit与内核峰值，历史扫描进程正常退出。未新增重任务持续驻留。

## 12. 验收与交接状态

|步骤|本轮状态|
|---|---|
|门禁(a)同环境实际重配、命令对照|PASS：命令/compdb/rules相同；Cache及生成图差异已单列|
|门禁(b)输出路径允许集合|FAIL：8个此前已完成输出被重新排入|
|门禁(c)待链接历史预算|139/159有观测，L=11.344585GiB；参考内存满足L+2；未执行启动准入|
|门禁(d)宿主及前10进程|已记录；无实际rpmbuild启动时点|
|唯一-ba --noprep续跑|NOT RUN，调用0次|
|验收1 构建身份、依赖/日志|输入身份PASS；完整构建未完成，不能注明“经一次续跑完成”|
|验收2 后处理链|NOT RUN|
|验收3 开发归档、compiler-rt|NOT RUN|
|验收4 同环境非归档基线|NOT RUN；未达到其他验收通过的执行时点；有条件授权及不阻塞交接规则保留|
|验收5 七宿主/Tizen/运行库消费者|NOT RUN|
|验收6 独立真实安装及同树SKIP|NOT RUN|
|验收7 非LTO结构诊断|NOT RUN|
|RPM清单及ShortCircuited|无新RPM，检查NOT RUN|
|BOLT交接|NOT_READY；禁止把部分BUILD/cache当作验收完成的新树|
|两ARM全量、根内小试、64MiB负例|NOT RUN|
|bash依赖与LLVM23探测|NOT RUN|

B与B/lto.cache继续保留；没有“构建完成时间”，不作交接后只读承诺来误示已交付。已通过的60对发布认证、两条x86回归与候选补丁身份不变；发布模式完整构建继续挂账。本轮仅执行获准的实际配置一次，未调用rpmbuild，不修改任何Source/Commands/比较器/spec/补丁/配置，不进入BOLT工作树或证据目录。

## 13. 本轮收尾

22:14:15共享锁已释放；22:22:56两项目锁释放，最终核查本任务进程0、挂载0、项目锁0，scope为inactive/dead，采样器与日志线程已回收。证据E10/cleanup-final.json、lock-released.json。E10内原始数据保留本机；提交仅本页和STATUS，用户gbs_llvm.conf改动不入提交。没有删除目录、恢复CMake旧生成文件、安装软件或推Gerrit。

## 14. 待完成ELF链接历史峰值全表

单位GiB，VmHWM为docs/34两个阶段采样最大值；UNKNOWN=历史无匹配采样，不是零。每项原JSONL文件与行号见E10/pending-link-historical-peaks.tsv。此表为干跑结果和历史记录，不是本轮链接性能数据。

|目标（相对B）|历史VmHWM GiB|
|---|---:|
|`bin/FileCheck`|UNKNOWN|
|`bin/UnicodeNameMappingGenerator`|0.184940|
|`bin/bugpoint`|10.613564|
|`bin/clang-22`|10.654884|
|`bin/clang-apply-replacements`|0.431107|
|`bin/clang-change-namespace`|4.010555|
|`bin/clang-check`|9.066990|
|`bin/clang-diff`|9.465027|
|`bin/clang-doc`|3.900959|
|`bin/clang-extdef-mapping`|2.823982|
|`bin/clang-format`|1.282127|
|`bin/clang-fuzzer-dictionary`|0.255280|
|`bin/clang-import-test`|11.344585|
|`bin/clang-include-cleaner`|3.767097|
|`bin/clang-include-fixer`|3.902695|
|`bin/clang-installapi`|9.723938|
|`bin/clang-linker-wrapper`|10.167030|
|`bin/clang-move`|3.651012|
|`bin/clang-nvlink-wrapper`|9.830620|
|`bin/clang-offload-bundler`|1.763054|
|`bin/clang-query`|4.443367|
|`bin/clang-refactor`|7.977531|
|`bin/clang-reorder-fields`|4.144451|
|`bin/clang-repl`|10.944603|
|`bin/clang-scan-deps`|9.643044|
|`bin/clang-sycl-linker`|8.418072|
|`bin/clang-tidy`|8.293484|
|`bin/clangd`|7.859879|
|`bin/clangd-fuzzer`|7.926006|
|`bin/clangd-indexer`|7.303036|
|`bin/count`|UNKNOWN|
|`bin/dexp`|1.622589|
|`bin/diagtool`|4.457760|
|`bin/dsymutil`|4.912613|
|`bin/find-all-symbols`|3.919140|
|`bin/llc`|5.822006|
|`bin/lld`|10.666859|
|`bin/lldb`|0.177299|
|`bin/lldb-dap`|0.259491|
|`bin/lldb-instr`|7.189709|
|`bin/lldb-mcp`|0.368011|
|`bin/lldb-server`|2.252598|
|`bin/lli`|3.670044|
|`bin/lli-child-target`|0.320377|
|`bin/llvm-PerfectShuffle`|0.041843|
|`bin/llvm-ar`|2.146713|
|`bin/llvm-as`|0.659878|
|`bin/llvm-bcanalyzer`|0.158962|
|`bin/llvm-c-test`|3.228886|
|`bin/llvm-cas`|0.137901|
|`bin/llvm-cat`|0.556179|
|`bin/llvm-cfi-verify`|0.595680|
|`bin/llvm-cgdata`|0.658638|
|`bin/llvm-config`|0.236595|
|`bin/llvm-cov`|0.527241|
|`bin/llvm-ctxprof-util`|1.221840|
|`bin/llvm-cvtres`|0.336372|
|`bin/llvm-cxxdump`|0.456093|
|`bin/llvm-cxxfilt`|0.134434|
|`bin/llvm-cxxmap`|0.208633|
|`bin/llvm-debuginfo-analyzer`|0.517952|
|`bin/llvm-debuginfod`|0.469727|
|`bin/llvm-debuginfod-find`|0.310261|
|`bin/llvm-diff`|0.386272|
|`bin/llvm-dis`|0.376850|
|`bin/llvm-dlang-demangle-fuzzer`|0.127838|
|`bin/llvm-dwarfdump`|1.873581|
|`bin/llvm-dwarfutil`|4.897694|
|`bin/llvm-dwp`|4.625004|
|`bin/llvm-exegesis`|2.700298|
|`bin/llvm-extract`|1.516609|
|`bin/llvm-gsymutil`|2.195671|
|`bin/llvm-ifs`|0.395267|
|`bin/llvm-ir2vec`|4.714802|
|`bin/llvm-isel-fuzzer`|4.606049|
|`bin/llvm-itanium-demangle-fuzzer`|0.094585|
|`bin/llvm-jitlink`|1.327393|
|`bin/llvm-jitlink-executor`|0.230843|
|`bin/llvm-libtool-darwin`|0.651279|
|`bin/llvm-link`|0.688869|
|`bin/llvm-lipo`|0.587315|
|`bin/llvm-lto`|9.988052|
|`bin/llvm-lto2`|5.536057|
|`bin/llvm-mc`|0.355293|
|`bin/llvm-mca`|0.360516|
|`bin/llvm-microsoft-demangle-fuzzer`|UNKNOWN|
|`bin/llvm-ml`|1.839462|
|`bin/llvm-modextract`|0.661301|
|`bin/llvm-mt`|0.121689|
|`bin/llvm-nm`|0.576504|
|`bin/llvm-objcopy`|1.777069|
|`bin/llvm-objdump`|2.235855|
|`bin/llvm-offload-binary`|1.742210|
|`bin/llvm-offload-wrapper`|0.996979|
|`bin/llvm-opt-fuzzer`|5.344788|
|`bin/llvm-opt-report`|0.150833|
|`bin/llvm-pdbutil`|0.534737|
|`bin/llvm-profdata`|2.163986|
|`bin/llvm-profgen`|0.817406|
|`bin/llvm-rc`|0.042309|
|`bin/llvm-readobj`|2.320473|
|`bin/llvm-readtapi`|0.407524|
|`bin/llvm-reduce`|5.384403|
|`bin/llvm-remarkutil`|0.161404|
|`bin/llvm-rtdyld`|0.490406|
|`bin/llvm-rust-demangle-fuzzer`|UNKNOWN|
|`bin/llvm-sim`|0.429821|
|`bin/llvm-size`|0.380836|
|`bin/llvm-special-case-list-fuzzer`|0.127895|
|`bin/llvm-split`|2.916988|
|`bin/llvm-stress`|0.359959|
|`bin/llvm-strings`|0.158188|
|`bin/llvm-symbolizer`|1.728775|
|`bin/llvm-test-mustache-spec`|UNKNOWN|
|`bin/llvm-tli-checker`|0.524197|
|`bin/llvm-undname`|0.145813|
|`bin/llvm-xray`|0.454868|
|`bin/llvm-yaml-numeric-parser-fuzzer`|0.103470|
|`bin/llvm-yaml-parser-fuzzer`|0.127178|
|`bin/modularize`|3.955006|
|`bin/not`|UNKNOWN|
|`bin/obj2yaml`|0.559128|
|`bin/offload-arch`|0.237766|
|`bin/opt`|5.869381|
|`bin/pp-trace`|3.832802|
|`bin/reduce-chunk-list`|UNKNOWN|
|`bin/sancov`|0.509724|
|`bin/sanstats`|0.434467|
|`bin/split-file`|0.216248|
|`bin/tool-template`|2.275394|
|`bin/verify-uselistorder`|0.537666|
|`bin/yaml-bench`|UNKNOWN|
|`bin/yaml2macho-core`|0.152420|
|`bin/yaml2obj`|0.738049|
|`lib64/BugpointPasses.so`|UNKNOWN|
|`lib64/CheckerDependencyHandlingAnalyzerPlugin.so`|4.787960|
|`lib64/CheckerOptionHandlingAnalyzerPlugin.so`|4.802734|
|`lib64/LLVMgold.so`|7.979385|
|`lib64/SampleAnalyzerPlugin.so`|6.030426|
|`lib64/clang/22/lib/linux/libclang_rt.asan-x86_64.so`|0.055634|
|`lib64/clang/22/lib/linux/libclang_rt.dyndd-x86_64.so`|UNKNOWN|
|`lib64/clang/22/lib/linux/libclang_rt.hwasan-x86_64.so`|0.042450|
|`lib64/clang/22/lib/linux/libclang_rt.hwasan_aliases-x86_64.so`|0.042305|
|`lib64/clang/22/lib/linux/libclang_rt.memprof-x86_64.so`|UNKNOWN|
|`lib64/clang/22/lib/linux/libclang_rt.nsan-x86_64.so`|UNKNOWN|
|`lib64/clang/22/lib/linux/libclang_rt.scudo_standalone-x86_64.so`|UNKNOWN|
|`lib64/clang/22/lib/linux/libclang_rt.tsan-x86_64.so`|UNKNOWN|
|`lib64/clang/22/lib/linux/libclang_rt.ubsan_minimal-x86_64.so`|UNKNOWN|
|`lib64/clang/22/lib/linux/libclang_rt.ubsan_standalone-x86_64.so`|UNKNOWN|
|`lib64/libLLVM.so.22.1`|10.932308|
|`lib64/libLTO.so.22.1`|10.328819|
|`lib64/libRemarks.so.22.1`|UNKNOWN|
|`lib64/libarcher.so`|UNKNOWN|
|`lib64/libclang-cpp.so.22.1`|9.473083|
|`lib64/libclang.so.22.1.8`|8.806843|
|`lib64/liblldbIntelFeatures.so.22.1`|0.379642|
|`lib64/libomp.so`|0.191963|
|`lib64/libompd.so`|UNKNOWN|
|`projects/openmp/libompd/gdb-plugin/python-module/ompd/ompdModule.so`|UNKNOWN|
