# BOLT clang 维护与故障处置

适用于 packaging/llvm.spec 的 x86_64 clang_bolt 路径；生产内的简要说明随 packaging/clang-bolt-helper.py 文件头交付。本组内文档补充重训方法、证据保留和上线核对。BOLT 生成参数及 profile 在本轮不改，不重生成现有候选。

## 失败分流

|失败|核对内容|处置与复验|
|---|---|---|
|工具版本实际行不等于 CERTIFIED.bolt_version|工具来源、源码版本、bin/llvm-bolt SHA、版本完整原文|remedy: 有计划升级时更新认证常量并重新认证；否则用 --without clang_bolt，或将 x86_64 bcond_without 改成 bcond_with。不要用子串版本匹配。|
|profile SHA 实际值不符|Source1200 是否对应正确的二进制 Source、xz 完整性、未压缩 SHA|remedy: 先核对 Source 身份；SHA 不同不等于 profile 已过期。找回正确 Source 或另行重训、审核、重新认证。|
|计划含未批准任务或不完整|完整 dry-run、CMake 配置、dirty 来源、规则与依赖图、是否仅见 Re-running CMake...|remedy: 查明普通任务或新增任务来源；必要时离线重生成描述集合并重新认证。禁止运行时自动扩白名单，也不在看不到真实计划时继续。|
|匹配 R 或 S/N 超过5%|普通ELF/重链ELF、编译/链接配方、工具与profile身份、N/M/S/U/Q原文|remedy: 核对输入身份后重训 profile 或关闭 BOLT。禁止提高阈值、启用 infer-stale 或忽略失败。|

其他门禁（安全属性、tiny、compare-root、post身份、TF归档SHA、磁盘/环境）失败均停止。错误保留实际值、期望值、日志路径与英文 remedy，不把准备错误或来源变化称作新的产品缺陷。

## 运行前提与资源

- Python >=3.9，且具有 os.waitid、waitstatus_to_exitcode、P_PID、WEXITED、WNOHANG、WNOWAIT、CLD_EXITED。先运行 helper preflight 和 certified，保存原文。
- /proc 必须与执行命令的 PID 命名空间一致，进程组清理才有保证。BOLT_PROC_OK/MISSING 只作诊断，不是构建准入门禁；缺少匹配 /proc 时不能声称子孙进程清理已保证。
- buildroot 的绝对路径不得包含 debug（不区分大小写）。这是 find-debuginfo 路径选择器的实测前提，须在任何 BOLT 动作前检查，不通过改平台宏或权限绕过。
- disk-preflight 检查声明的写入上界、额外预留和写后剩余空间。单次计划写入 >10GiB，写后至少30GiB；<=10GiB，写后至少1GiB。16GiB默认BOLT阶段预算来自本地热缓存估计，不能当作冷缓存增长上限。必须把缓存增长和临时文件计入预算。
- ninja -j1 只限制Ninja同时调度的任务数，不限制链接器内部并行或内存。当前本地重阶段16GiB/swap0，nice15/ionice3，入口MemAvailable>=12GiB，运行<3GiB终止；共享锁每段<=60分钟、等锁<=2小时。轻阶段4GiB，nice19/ionice3，入口>=6GiB。
- cmake/ninja/链接须保留原RPM环境前导（PATH及全部CFLAGS/CXXFLAGS/LDFLAGS等）。记录 PATH 和 which clang/clang++，避免 /bin 与 /usr/bin 路径拼写变化触发CMake删缓存。已禁用的原树不能用任何CMake/Ninja命令重新探测。

## 升级 LLVM 与重新认证

1. 保留新基线、编译器身份、完整配置与原 clang 链接边；保留追加 bolt 前后的 build.ninja、rules.ninja、普通配置产物。使用专用测试树和缓存；不得污染仍供其他会话使用的树。正式交接树允许原地使用缓存。
2. 更新 helper 的 CERTIFIED.llvm_version、bolt_version、profile_sha256、bolt_task_count、tf_refresh_task_count；PROFILE_SHA 是 profile_sha256 的别名。审核 OPTIONS、目标三元组、精确描述集合与 TF 两条任务的证明，而不是盲改计数。
3. 在 llvm-optimize bolt-v4 证据仓库离线运行：

```sh
python3 tools/bolt/results/review-closure-v3.py \
  --before "$BOLT_BEFORE/build.ninja" \
  --after "$BOLT_AFTER/build.ninja" \
  --rules "$BOLT_AFTER/CMakeFiles/rules.ninja" \
  --expect-tasks "$BOLT_REVIEWED_TASK_COUNT" > "$BOLT_EVIDENCE/closure.json"
```

路径变量是维护者核定的新快照目录。训练脚本输出须在其WORKSPACE/temp下使用新目录，不直接运行硬编码旧现场的phase入口。--old-result 仅用于应完全保持分类的同一已认证图复核；升级新增合法边需要逐项人工审查，不把旧分类不同自动放行。脚本遇到未知 include/subninja、路径转义、未展开变量失败关闭。保存确切argv、输入SHA和描述展开所需rules子集；据此更新独立描述JSON与helper精确集合，并证明二者一致。

该结论只覆盖保存的静态Ninja图，不加载.ninja_deps/depfile、不做完整dirty判定。Quickbuild现场 tool-plan 与真实构建 tool-verify 仍是最终门禁，未知真实任务失败关闭。

4. 重跑全部夹具及负例；验证 Python/磁盘、链接命令/rsp、安全属性、进程组清理、干跑与真实构建日志完整性。dry-run只允许指定warning诊断；真实构建成功标记须唯一且在最后，合法restat缩减允许。TF归档前后SHA必须相同，普通构建任务不得出现。
5. 重跑 ON/OFF 两模式展开；OFF与新基线逐字一致；ON必须 snapshot < compare-root < native archive conversion < candidate install，转换一次。采集新基线/候选×debug/release四份真正生成的post脚本，平台段逐字相同、BOLT尾检最后；不要用rpmspec --eval代替捕获。
6. 重跑输入重链身份、匹配双门禁、BOLT note/strip SHA链、安全属性、三目标tiny、30历史+90资产完整对象比较（同一实体路径，不删.GCC.command.line）、双模式小RPM及完整普通载荷反向检查、RPM/DWARF预期差异、三目标性能与留出组。普通RPM必须先核对来源、字节和SHA，不能把历史包称为新基线构建物。
7. Quickbuild首次实际构建再核对tool-plan、TF SHA、tool-verify、compare-root、匹配统计、post身份、安全和tiny、最终RPM/accel身份、包清单及性能。正式发布模式仍需完整构建验证。

## profile v2 的训练来源与重训方法

历史文档的“ARM13+AArch6410”指23份profile：13个ARM工作负载（生成器A/B/C三项加10个真实源），加10个AArch64真实源。不是23个不同的LLVM文件；两目标真实训练选相同的10个LLVM源，目标预处理输入不同。资格实验的30行另包括10个留出源，共20个不同源。

|真实训练输入|ARM与AArch64均选用的源路径|
|---|---|
|llvm_sema_SemaStmt|clang/lib/Sema/SemaStmt.cpp|
|llvm_sema_SemaExprCXX|clang/lib/Sema/SemaExprCXX.cpp|
|llvm_codegen_SelectionDAG|llvm/lib/CodeGen/SelectionDAG/SelectionDAG.cpp|
|llvm_codegen_MachinePipeliner|llvm/lib/CodeGen/MachinePipeliner.cpp|
|llvm_transforms_Attributor|llvm/lib/Transforms/IPO/Attributor.cpp|
|llvm_transforms_WholeProgramDevirt|llvm/lib/Transforms/IPO/WholeProgramDevirt.cpp|
|llvm_arm_ARMISelLowering|llvm/lib/Target/ARM/ARMISelLowering.cpp|
|llvm_arm_ARMTargetTransformInfo|llvm/lib/Target/ARM/ARMTargetTransformInfo.cpp|
|llvm_mc_MasmParser|llvm/lib/MC/MCParser/MasmParser.cpp|
|llvm_mc_AsmParser|llvm/lib/MC/MCParser/AsmParser.cpp|

原始ARM侧在 tools/bench_inputs/real_tu/，AArch64侧在 real_tu_aarch64/；逐项.flags.json钉住原编译命令、预处理命令、目标和.ii SHA，大于公开大小上限的.ii按sidecar路径保存在本地。生成器为tools/bench_inputs/generate_synthetic.py，历史seed73419，A/B/C scale=1/2/2，-std=c++17 -O2；实际源TU参数逐项沿用sidecar，不能统一改成生成器参数。ARM目标armv7l-tizen-linux-gnueabi，AArch64目标aarch64-tizen-linux-gnu，均显式同一resource-dir和只读sysroot。

历史命令、资源与完整原文来源：W/docs/16_bolt_final.md §5–6、W/docs/20_spec_integration_v2.md附录D、tools/collect_bolt_profile.py、tools/extend_bolt_profile_aarch64.py、tools/finish_bolt_final.py。历史成功插桩使用22GiB和一个BOLT线程，18GiB曾OOM；不能在当前16GiB约束下照搬并声称已可执行，重训需另行核定资源。本轮没有重训授权或执行。

重训步骤（以下为维护模板，不会在包构建中执行；变量指新的独占实验目录和已核定工具）：

1. 准备相同身份的普通clang及带--emit-relocs重链、llvm-strip --strip-debug后的输入；保留两者。工具、runtime、loader、library-path必须同源并记录SHA。使用独立空profile目录与唯一PID前缀，对普通输入插桩，不能把插桩ELF作为优化重写输入。

```sh
"$BOLT_LOADER" --library-path "$BOLT_LIBRARY_PATH" \
  "$BOLT_TOOL" "$BOLT_INPUT" -instrument --thread-count=1 \
  -runtime-instrumentation-lib="$BOLT_RUNTIME_ARCHIVE" \
  -instrumentation-file="$BOLT_PROFILE_DIR/clang" \
  -instrumentation-file-append-pid \
  -instrumentation-binpath="$BOLT_INSTRUMENTED/bin/clang-22" \
  -o "$BOLT_INSTRUMENTED/bin/clang-22"
```

2. 建立与基线同名的clang++调用方式；ARM脚本按argv[0]选择g++模式，AArch64扩展显式加--driver-mode=g++。核对正式基线protocol_hash和全部输入SHA/flags、sysroot/resource-dir。ARM采集命令：

```sh
python3 tools/collect_bolt_profile.py \
  --compiler "$BOLT_INSTRUMENTED/bin/clang++" --baseline "$BOLT_ORDINARY/bin/clang++" \
  --baseline-result "$BOLT_FORMAL_BASELINE" --loader "$BOLT_LOADER" \
  --library-path "$BOLT_LIBRARY_PATH" --merge-fdata "$BOLT_MERGE_FDATA" \
  --sysroot "$BOLT_ARM_SYSROOT" --resource-dir "$BOLT_RESOURCE_DIR" \
  --profile-dir "$BOLT_PROFILE_DIR" --output "$BOLT_ARM_COLLECTION" --cpu 2
```

脚本要求新输出目录与空profile目录，生成A/B/C并逐项比对基线，先普通后插桩各一次，验证ARM ELF对象；运行器保持固定CPU2、ASLR off、4GiB编译进程AS上限。保存每个PID fdata的SHA/大小、源/flags与完整argv。只合并这13份，不能混入并发写入或历史重试文件。

3. 在同一插桩ELF内嵌前缀目录继续采集AArch64十项；扩展脚本要求原13份全部存在且逐项SHA不变，每项新增恰好一份非空PID fdata：

```sh
python3 tools/extend_bolt_profile_aarch64.py \
  --compiler "$BOLT_INSTRUMENTED/bin/clang++" --baseline "$BOLT_ORDINARY/bin/clang++" \
  --loader "$BOLT_LOADER" --library-path "$BOLT_LIBRARY_PATH" \
  --sysroot "$BOLT_AARCH64_SYSROOT" --resource-dir "$BOLT_RESOURCE_DIR" \
  --inputs tools/bench_inputs/real_tu_aarch64 --profile-dir "$BOLT_PROFILE_DIR" \
  --merge-fdata "$BOLT_MERGE_FDATA" --output "$BOLT_AARCH64_COLLECTION" --cpu 2
```

它从result.json明确列出的13+10路径构造merge-fdata argv，将stdout保存为merged-v2.fdata。等价原理为 `merge-fdata <明确13个ARM路径> <明确10个AArch64路径> > merged-v2.fdata`，不使用会混入未知文件的宽泛通配符。保存raw/commands.json及两目标result.json；留出组不得参与训练。

4. 新profile经xz压缩为二进制Source1200，记录压缩/未压缩SHA和大小，更新CERTIFIED.profile_sha256；保留23份原始fdata、清单、源SHA、flags和工具身份。当前v2未压缩171,232,190字节，SHA d9b132f9430dfed32e080c65b4422bd76eba4a9c2101a2b18a7f66c94133b326；xz 9,735,212字节，SHA 52fd8522b8cceadebfb6bfc0a19f721f1072cff95c682b12b2c4dd5b0cc1e27f。
压缩和登记命令示例（新profile的SHA必须重新登记，不能沿用旧值）：

```sh
xz -9e -c "$BOLT_AARCH64_COLLECTION/merged-v2.fdata" > "$BOLT_STAGE/clang-bolt-v2.fdata.xz"
sha256sum "$BOLT_AARCH64_COLLECTION/merged-v2.fdata" "$BOLT_STAGE/clang-bolt-v2.fdata.xz"
```

记录xz版本/参数及输出大小，发布前重新检查单文件大小约束。

5. 对去debug的重链输入执行正式OPTIONS（ext-tsp、cdsort、split-functions、split-all-cold、split-eh、dyno-stats、thread-count=1、stale-threshold=5），禁infer-stale；读取N/M/S/U/Q，R=(S+U)/(N+U)<=5%、S/N<=5%。不能仅凭SHA正确认为profile适配；当前N/M仅约16%。随后重新认证上述对象、包、安全、性能、留出组及Quickbuild实物门禁，不把插桩开销当优化收益。

## 日志锚点与身份链

|锚点/产物|含义|
|---|---|
|BOLT_BUILDROOT_OK|BOLT动作前路径检查通过|
|preflight/certified JSON|Python接口与认证版本、profile SHA、111+2集合计数|
|BOLT_PROC_OK / BOLT_PROC_MISSING|/proc诊断；不保证命名空间匹配|
|BOLT_TOOL_DRY_RUN_BEGIN/END|原始干跑日志边界；tool-plan.json保存诊断与真实类别计数|
|BOLT_NINJA_EXIT_0|ninja成功后追加的唯一末行；tool-verify据此认证真实构建日志完整性|
|tool-build-verification.json|planned/executed计数、构建前后工具SHA、实际任务和TF前后SHA|
|BOLT_STRIP_IDENTITY|strip-all前BOLT note存在与前后SHA；最终ELF不保留BOLT note|
|BOLT_PIPELINE_PASS|重链/重写、匹配、安全与三目标tiny成功|
|BOLT_COMPARE_ROOT_PASS|普通安装snapshot至候选替换前，buildroot未变化；静态库转换等后续改写须在此之后|
|BOLT_POST_GATE_PASS|单次原平台post链后，最终路径SHA/别名/安全/tiny/反向检查通过|
|BOLT_GATE_FAILED|任何helper门禁失败；保存原文及日志，不自动降级|

## 上线保留、崩溃定位与回退

每次构建保留：源码父/提交/Change-Id、完整spec/helper/profile Source SHA、普通clang、带relocs且strip-debug的BOLT输入、strip-all前BOLT ELF及其Build-ID、最终clang SHA和Build-ID、llvm-bolt/llvm-strip身份与构建环境、identity.json/rewrite-result.json/安装state、匹配计数与全部原文、工具计划/真实构建/TF SHA、RPM/DWARF清单、最终RPM SHA、accel包SHA及worker真正加载的clang实体SHA/Build-ID。存储预剥离ELF与profile需要访问控制和足够容量；不能只保存短SHA或日志截屏。

定位崩溃时先核对worker实际实体和最终RPM/accel SHA/Build-ID，不能凭包名推测候选身份。保留故障映射及ASLR加载偏移，把地址归一到对应ELF；用匹配的pre-strip BOLT ELF做符号级地址定位（如llvm-symbolizer），再通过保留的rewrite/地址映射、普通ELF及其DWARF映射到原源码。第一版BOLT输入已strip-debug，BOLT ELF自身不含可直接使用的源码级调试信息；没有保存足够的地址映射时不能宣称能从任意BOLT地址无损还原普通clang源码行。必要时按记录的原配方重现输入和重写，先核对中间/最终SHA再分析；单凭profile或N/M相似不能替代身份。

区分四件事：同一次构建中的SHA身份链；固定输入/工具/参数的重写可重现性；整个LLVM构建可重现性；两个环境的性能可比性。它们互不等价，不能要求不同Quickbuild配方和本地clang的SHA相同。Quickbuild核对匹配统计同量级且双门禁PASS，并对自己的clang做性能复核。

回退是提交x86_64的一行 bcond_without clang_bolt → bcond_with clang_bolt；关闭时Source1200/1201和BOLT相关BuildRequires同时失效，ON/OFF展开须重新对新基线证明。回退还需撤换accel/worker实际实体并同步恢复仓库快照/包版本，核对部署后的SHA与Build-ID；只改spec而继续使用旧accel或旧快照不能视作已回退。
