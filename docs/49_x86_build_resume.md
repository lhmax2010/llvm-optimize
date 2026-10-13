# 49 续九：第二轮部分构建树续跑前核查

**最终状态：STOP_RESUME_PREFLIGHT；续跑调用0次。** 指定的`--define '_smp_mflags -j1'`不会把本配方的Ninja改成串行：根内展开后仍是`ninja -j 6`。此外，干跑894项超过本轮规定上限811，历史单链接峰值也超过当前可用内存减2GiB的预算。按“任一不满足则不启动”停止，没有改宏、spec或资源后重试。

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
