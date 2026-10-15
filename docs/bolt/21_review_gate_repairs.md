# 21 续跑九：外部评审门禁修复

## 人工裁决与边界

Quickbuild 旧 tool-plan 会误拒绝 BOLT 静态库；用户取消该轮。本轮不推任何 Gerrit 分支，只更新 GitHub bolt-v4。候选生成命令及参数不改，历史后备候选 SHA256 4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9 必须保持。新源提交以 a1410e3d 为父，周五再整理。

Quickbuild 参数及项目配置不可改，x86_64 保持 `%bcond_without clang_bolt` 默认开启；本地 `--without clang_bolt` 用于零影响核对。Quickbuild 回退须提交 spec 新提交，将 x86_64 改为 `%bcond_with clang_bolt`，正式提交说明必须包含该方式。

沿用锁/资源/磁盘/保护规则；不在原树运行 cmake/ninja/-P，不进行新配置，不进入 ARM 树。查找先 rg/find；产品准备错误每类只准修正一次；产品门禁失败立即停止。

## 第一步 tool-plan

保存的配置快照离线递归遍历 llvm-bolt 全部显式、隐式与 order-only 依赖，展开 rule/edge 的 description 变量，没有运行 Ninja。闭包 1911 条边：普通 1792（含有 command 的 1715）；新增 BOLT phony 9；新增实际任务 110。普通边在 Quickbuild 应已最新，出现在 dry-run 一律拒绝。

描述全集：102 个 `Building CXX object tools/bolt/...`；7 个 `Linking CXX static library lib64/libLLVMBOLT{Core,Passes,Profile,Rewrite,RuntimeLibs,TargetX86,Utils}.a`；1 个 `Linking CXX executable bin/llvm-bolt`。逐条原文与边见 review-tool-descriptions.json 和 review-closure.json.xz。

helper 用全集的精确字符串白名单。每行必须完整匹配 `[f/t] 描述`，计数有效，不允许噪声、未知 Generating/Creating、普通任务或伪造包含 bin/llvm-bolt 的字符串；计划非空且包含最终链接。返回对象/静态库/可执行文件真实计数。spec 固定 `LC_ALL=C NINJA_STATUS='[%%f/%%t] ' ninja -n llvm-bolt`。

夹具 109/109 PASS（原103+新增6个测试方法，全集110项逐条subTest）；包含全部负例。根因由旧 helper 对静态库的拒绝及新全集夹具确认。

准备记录：执行编辑脚本时 cwd 指向 tools/bolt，误用了相对的 E 路径；改成已定位的绝对路径一次。该次未编辑 helper，随后新回归夹具对旧 helper 报错；修正入口后109项通过。属本轮一次命令工作目录准备修正，不隐藏失败记录。

后续步骤尚待，源提交与文本补丁暂不生成最终版。

## 第二步：部分实现，停止认证

已编辑但未认证：call 使用 Popen/start_new_session、异常/超时 killpg(SIGKILL)+wait 并附日志；tiny 每次删除旧输出、要求非空普通非链接文件、双方禁默认配置；inventory 验证根并对 walk 错误失败；ELF 类型/版本/头大小/节范围/字符串表/LOAD范围及filesz入口检查；clang-cl/cpp 异常别名；版本行精确校验；post 禁工具/静态库/所有CMake文件内BOLT；spec把debug路径检查移到BOLT动作前；生产prune函数/CLI删除，其三个历史夹具单独保存不随Source发布。候选生成参数未改。

rsp检查：保存的 link.original SHA256 `352a6f57fdc617c20f3e616a0f49ad113d1d5f057e44dcad0afa88c63a9a68cf`，4890字符；shlex分词后没有任何以 `@` 开头的参数。完整命令在 review-rsp-evidence.json，按裁决不增加rsp代码。

新增35个测试方法（tool-plan6、健壮性29），连同原103共138。第一次全套执行有夹具字段/异常契约及进程观察错误；各项一次修正后，最终 **137/138 PASS、1 FAIL**。其中ELF文件范围、入口、字符串、目录访问错误、tiny无输出/空/链接、别名、版本、反向检查的夹具通过；不能称全部夹具PASS。

失败项 `ProcessGroupTests.test_timeout_kills_descendants_and_heartbeat`：第一次 exists/read 的 `/proc` 竞态已修正；第二次在 helper 返回后，读取后代1199507状态为 `R`，不是消失或Z。未完成后代全部退出与心跳停止的证明，立即停止，不再修正/重跑。killpg已发送不等于已证明整个进程组退出；仅等待直接子进程不足以提供此证据。以后应先明确后代退出/回收的等待契约，再修复并重测，不在本轮追加尝试。后续只读审计该PID已不存在，两个失败scope均已回收。

历史prune三项只移位未删除证据；生产Source只有helper/spec/profile，不包含历史测试。新helper/spec仅为未完成工作副本，**没有生成新源提交**。未完成差异及SHA单独置 review-repairs-incomplete.patch/manifest，旧a141文本补丁/manifest未冒充本轮资格。

## 停止后状态

安全属性对比（ELF类型、INTERP、RELRO、STACK、PROPERTY/notes、动态flags/needed、dynsym、版本集合）全部 **NOT RUN**，不声称保持；因此安全属性门禁尚未实现。宏链逐字证据、debug/release开关OFF与cb基线比对全部NOT RUN。ARM/AArch64 30条各5次、20独立源与留出组性能全部NOT RUN，几何平均比未知。真实候选上的新tiny/security/post/compare-root及构造dry-run联合认证NOT RUN。旧20的x86性能不代替本轮目标性能。

候选仍 `4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9`；普通clang与禁用原树cache/ninja SHA未变。22RPM全SHA/大小、归档证据元数据、原源码元数据比对PASS，原ThinLTO仍47987文件/96881772832B；本轮无CMake/Ninja/链接/候选重写/原cache写入/共享锁/proc挂载/ARM根/LLVM构建。全部实验4GiB/swap0/nice19/ionice3 scope已回收；初次109项短单测直接执行，未纳入cgroup，该资源执行偏差如实登记。无>10GiB写入。

新源提交：**未生成**；源HEAD仍a1410e3d，修复在工作副本保留。本轮Gerrit任何分支均未查询或推送。GitHub阶段提交3e7141f已发布tool-plan；停止记录与未认证修复另提交bolt-v4。

准备修正与查找更正逐条见review-corrections.json；两份完整失败日志均公开。初次编辑脚本cwd错误后测试了旧helper，作为旧行为回归复现而非新实现认证；后续109项才是正确实现PASS。停止时没有继续产品步骤。

## 续跑十：PM裁决及进程组约定

上轮不是单纯测试竞态：killpg后只等待直接子进程，不能证明lld等后代已停止写缓存。call异常/超时先killpg(SIGKILL)，回收直接子进程，随后扫描/proc/*/stat，取最后一个右括号之后的state与pgrp；相同pgrp且非Z/X视为存活，每20ms复查，10秒仍存活则GateError列PID/状态。原超时/异常和日志路径保留。/proc消失视为已退出，无法读取/格式错误则失败关闭。

真实shell→子→孙，孙每30ms写心跳；按同样10秒约定观察所有后代退出/僵尸后，再等待150ms（超过两个周期）确认心跳不增。持续存活mock负例报告424242:R、原错误和日志。全套140/140 PASS，新增2方法（累计比原103新增37），reviewfinish-process-tests给原文/资源；4GiB/swap0/nice19/ionice3 scope回收。本轮尚无准备修正。

rsp不加代码、tool-plan闭包及白名单不重做；全套单测包含原有tool-plan回归。候选生成步骤/参数不改；源父a141，本轮不推sandbox或任何Gerrit分支。后续按安全属性→宏链→真实门禁顺序，任一产品失败即停。

## 续跑十安全属性：全部保持

SHA绑定普通7df0ff90…与候选4ec07159…；readelf完整原文（含全部动态符号/版本）以xz公开，security-probe完整结构与生产helper再次提取相同。未改变生成参数或重新生成候选。

|属性|普通|候选|判定|
|---|---|---|---|
|ELF类型|DYN/PIE(3)|DYN/PIE(3)|相同|
|PT_INTERP|/lib64/ld-linux-x86-64.so.2|同左|相同|
|GNU_RELRO flags/vaddr/filesz/memsz|R(4)/0x828cb70/0x2dd6e8/0x2de490|同左|续跑十二新门禁逐值相同；续跑十仅readelf范围记录|
|GNU_STACK|RW(6)|RW(6)|相同，无执行权限|
|PT_GNU_PROPERTY/.note.gnu.property|均无|均无|相同；不声称有IBT/SHSTK|
|DT_FLAGS|无|无|相同|
|DT_FLAGS_1|PIE/0x08000000|同左|相同|
|DT_NEEDED|librt,libdl,libm,libz,libstdc++,libgcc_s,libc,ld-linux-x86-64（完整SONAME见原文）|同序列|相同|
|.dynsym名称/绑定/类型/可见性/定义类别|65241条|65241条|续跑十二五元组逐条相同；原续跑十仅名称/绑定/可见性|
|.gnu.version|65241个五元组与(提供文件,版本名)/hidden绑定|同左|续跑十二逐条相同|
|.gnu.version_r|43条需求|同左|相同|

helper新增security_properties/security_compare与security CLI，流水线strip-all之后及post启用，属性不符报具体类别；续跑十当时未比较地址/大小。续跑十二新增RELRO flags/vaddr/filesz/memsz及范围检查；dynsym保留原始st_shndx，以名称/绑定/类型/可见性/定义类别比较，忽略符号地址/大小/所在代码节名；版本含提供文件名与hidden，另比DT_BIND_NOW存在和W+X LOAD。更新表格采用22真实复测，不追溯声称旧helper已比较新增字段。原始节/段范围及动态/字符串/版本表边界均失败关闭。返回属性与重符号数据的条数/SHA避免巨大构建日志。

新增6个安全夹具（保持、删除GNU property、改栈权限、删除导出、改绑定、改可见性）全部PASS。全套146/146；比本轮开工138新增8，比原103累计新增43。一次旧post夹具输入修正：placeholder文件名fixture改为其identity已生成的真实before ELF，未mock掉新门禁；首次失败原文保留，修正后通过。本轮产品准备修正目前仅此一类一次。所有4GiB scopes已回收。

## 续跑十宏链：PASS（当前小spec原文证明）

历史20小spec把路径直接代入override，属于结构复用，原文并非逐字相同。本轮用源spec的同一完整片段生成两模式canonical小spec，位于%install和%files之后；逐字相等SHA256为61626efeef3dcaf1989b8ae00466578f733c0d4e638c127f54681d6bd826f180。两边完整原文见macro-evidence包内post-fragment.spec、macro-mini-debug/release.spec；小spec本轮只rpmspec展开，没有冒充新的rpmbuild执行。

```spec
%global __bolt_original_spec_install_post %{__spec_install_post}
%define __spec_install_post \
    %{__bolt_original_spec_install_post} \
    python3 %{SOURCE1201} post "%{buildroot}" "%{_builddir}/%{buildsubdir}/build/clang-bolt/install-state.json" "%{_builddir}/%{buildsubdir}/build/clang-bolt/ordinary-clang-22" "%{_builddir}/%{buildsubdir}/build/clang-bolt/post-gate" --resource-dir "%{buildroot}%{_libdir}/clang/%{llvm_version}" || exit 1
```

静态审查把BOLT新增空白移入条件块，避免关闭时多空行；不改生成命令/参数。debug/release各完成ON、OFF、cb679968基线展开，OFF的prep/build/install/check/clean（如存在）及post/pre/files等相关段逐字节相同，完整列表及SHA在reviewfinish-macros.json，未过滤空白或规范化路径。

根内rpmspec不支持--without：第一次采集参数错误修正一次，改用rpmbuild实际设置的_without_clang_bolt定义。单独rpmbuild --without clang_bolt --eval证明其实际值为字符串--without-clang_bolt；最初报告误期待整数1，属另一类报告判据错误，修正一次。安装macros中bcond_without只检查该变量是否存在；rpmspec传实际同一字符串。两类原文均保存，未将不支持的CLI冒充成功，最终展开PASS。本轮累计准备修正三类各一次：旧post夹具输入、rpmspec选项兼容、宏值报告判据；无同类第二次。

所有调用在原RPM前导，PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin，which clang=/bin/clang、clang++=/bin/clang++；argv/环境与mount前中后原文保存。轻scope已回收/proc已卸载，不取重锁，无CMake/Ninja。真实产物门禁下一步。

## 续跑十真实产物及源提交：PASS，停在推送前

不重新生成候选。ordinary7df与candidate4ec执行新的tiny（两边--no-default-config、每次清理输出、非空非链接）三目标完整.o相同，安全属性比较再次PASS。只复制20已解包的debug/release小RPM根到本轮专用目录：各执行post反向检查、故意加入llvm-bolt被拒并移除、compare-root文件/类型/权限/大小/SHA/链接逐项保持、完整post的SHA/alias/ELF/security/三目标全部PASS。原20证据不改。110任务全集构造dry-run返回102对象/7静态库/1可执行任务，加入普通lib/Support任务明确被拒。

新本地源提交 **97c060a10bf0d19cea4b163853ceb873ed431478**，父 **a1410e3d14b8836e3f9be5a1b4380f914dc2e705**，tree ea70ea066dd16430b23c238d9654e1667479b960；仅修改packaging/llvm.spec与clang-bolt-helper.py，profile保持。源tracked工作副本干净。文本补丁0002对父提交静态apply与整树write-tree相同，manifest已更新，旧a141 manifest单独保存。不推任何Gerrit分支，也不查询远端；不是已更新sandbox的声明。

|文件|字节|SHA256|
|---|---:|---|
|llvm.spec|24571|df1198d1567af520b12064fca6fe8342ab55c8859eebaec011d2e5ac3dd90620|
|clang-bolt-helper.py|52707|4590b337247749e76962801167a96a10f61ef5cbe9c993fba25ef462d87b9970|
|profile.xz（不变）|9735212|52fd8522b8cceadebfb6bfc0a19f721f1072cff95c682b12b2c4dd5b0cc1e27f|

OPTIONS与PROFILE_SHA常量和父提交相同；候选最终SHA仍4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9。source提交说明写明QB参数/项目不可改，x86默认开启；回退提交把bcond_without改bcond_with。

收尾保护审计PASS：22RPM完整SHA/大小、归档证据元数据、原源码元数据、禁用cache/ninja SHA不变，原ThinLTO仍47987/96881772832B。本轮没有原树CMake/Ninja/-P、链接/重写、重锁、ARM树或完整LLVM构建；所有实验4GiB/swap0/nice19/ionice3且scope回收，proc挂载仅本轮临时proc并在finally卸载，无宿主bind/namespace。没有单次>10GiB写入。详细资源、原文、三类各一次准备修正见reviewfinish-resources/corrections/final-result。

本轮只完成提示要求的本地修复/安全/宏链/真实门禁认证，停止在推送前。历史20性能与对象证据不因本轮而重测；前轮尚缺ARM/AArch64性能不冒充已补。Quickbuild仍须现场tool-plan/compare-root/security/post、自身clang性能及debugsource实物核对；不要求local/QB clang SHA相等。

## 续跑十一B：目标性能方法与输入

20性能方法原样用于ARM/AArch64：固定CPU2，单并行，编译器在本轮专用槽位覆盖且inode不变；round0/2/4 ordinary→candidate，round1/3 candidate→ordinary；每侧5次，不删异常样本。只计taskset+clang子进程墙钟，拷贝/SHA/环境前导/chroot在计时外；记录每次前后负载/频率，保留原RPM PATH和which输出。频率策略不修改。

普通SHA7df0ff90…、候选4ec07159…，60份既有.ii SHA及大小逐项相同。三元组严格取资产armv7l-tizen-linux-gnueabi/aarch64-tizen-linux-gnu，所有参数逐字保留，仅换本轮统一编译器槽位与输出。输入仍在此前专用目录，不重新预处理或进入ARM树。完整预检/原记录SHA在target-perf-preflight，实验driver公开。

每目标30条=arm-training10、arm-holdout10、aarch64-training10；两个训练cohort是同10源且输入SHA相同，共20独立源。主判据仍30条每侧5次的中位比几何平均严格<0.98；独立20按源汇总全部5/10样本再中位/比值/等权几何平均，留出组10另算。额外保存按entry中位数比值先在源内几何平均再等权20的结果，明确不同口径，不用去重删除任何原样本。

两目标分开重锁与16GiB/swap0/nice15/ionice3，单锁≤60m，MemAvailable准入12G/运行底线3G。磁盘16GiB预检预计剩36,421,627,904B，≥30GiB。准备性错误目前0；未改LLVM源码、未操作Gerrit。结果待。

### 续跑十一B：ARM目标 PASS

30条目、每侧5次/共300次全部保留，几何平均比 **0.856351167** <0.98；独立20源（池化全样本）0.858165628，留出10为0.868458776。独立20按entry中位比先源内平均的备用口径0.859362152，不混用。x86_64历史0.855890085，ARM相近。

CPU2 / Intel(R) Core(TM) Ultra 7 265，intel_pstate/powersave，策略800000–5300000kHz；准入busy3.000%。运行load1 min/median/max=1.59/2.86/4.68；600个编译前后频率样本kHz min/median/max=800000/1572406.0/5200000，属于边界采样而非编译期间平均频率。单并行、同一slot/inode10次覆盖全部核实。scope1723.033s/峰4.585GiB，锁1723.072s；proc/锁/scope回收。

|条目|普通中位s|候选中位s|比值|
|---|---:|---:|---:|
|arm-training/00-SemaStmt|6.306962|5.249152|0.832279|
|arm-training/01-SemaExprCXX|6.451667|5.391396|0.835659|
|arm-training/02-SelectionDAG|7.172717|6.102068|0.850733|
|arm-training/03-MachinePipeliner|6.515881|5.621568|0.862749|
|arm-training/04-Attributor|6.645996|5.643808|0.849204|
|arm-training/05-WholeProgramDevirt|5.935641|5.178307|0.872409|
|arm-training/06-ARMISelLowering|8.697455|7.628552|0.877102|
|arm-training/07-ARMTargetTransformInfo|4.920030|4.256021|0.865040|
|arm-training/08-MasmParser|3.429316|3.003495|0.875829|
|arm-training/09-AsmParser|2.800406|2.400299|0.857125|
|arm-holdout/00-ParentMapContext|6.000011|5.132233|0.855371|
|arm-holdout/01-ParseDecl|5.015590|4.365531|0.870392|
|arm-holdout/02-Driver|5.336522|4.718423|0.884176|
|arm-holdout/03-CoverageMappingGen|5.760749|4.821350|0.836931|
|arm-holdout/04-Metadata|5.499623|4.860948|0.883869|
|arm-holdout/05-ScalarEvolution|9.804958|8.751684|0.892577|
|arm-holdout/06-AArch64InstructionSelector|5.751231|4.925337|0.856397|
|arm-holdout/07-X86ISelDAGToDAG|5.056611|4.309699|0.852290|
|arm-holdout/08-ELF|5.761812|5.196722|0.901925|
|arm-holdout/09-InstrProfReader|4.655609|3.971036|0.852957|
|aarch64-training/00-SemaStmt|6.200113|5.130725|0.827521|
|aarch64-training/01-SemaExprCXX|6.471503|5.347725|0.826350|
|aarch64-training/02-SelectionDAG|7.279690|6.107221|0.838940|
|aarch64-training/03-MachinePipeliner|6.589895|5.513919|0.836723|
|aarch64-training/04-Attributor|6.535015|5.558852|0.850626|
|aarch64-training/05-WholeProgramDevirt|6.011069|5.083873|0.845752|
|aarch64-training/06-ARMISelLowering|8.805394|7.494910|0.851173|
|aarch64-training/07-ARMTargetTransformInfo|5.051683|4.205777|0.832550|
|aarch64-training/08-MasmParser|3.484781|3.042993|0.873224|
|aarch64-training/09-AsmParser|2.804367|2.381503|0.849212|

完整5次样本/argv/条件见target-perf-armv7l.json；逐条与独立20 CSV、原始logs与scope/session raw归档公开。没有删样、重跑或准备错误。AArch64尚待。

### 续跑十一B：AArch64目标 PASS

30条目、每侧5次/共300次全部保留，几何平均比 **0.847699213**；阈值严格<0.98。独立20源（池化全样本）0.847858623，留出10为0.847902567；备用entry中位数口径独立20为0.847750047。

CPU2 / Intel(R) Core(TM) Ultra 7 265，intel_pstate/powersave，策略800000–5300000kHz；准入busy1.980%。运行load1 min/median/max=0.58/1.55/3.48；600个边界频率样本kHz min/median/max=800000/1324176.0/5144592。单并行/同slot-inode/角色交替。scope1702.921s/峰2.814GiB，锁1702.955s；proc/锁/scope回收。

|条目|普通中位s|候选中位s|比值|
|---|---:|---:|---:|
|arm-training/00-SemaStmt|5.852411|4.917169|0.840196|
|arm-training/01-SemaExprCXX|6.106148|5.095319|0.834457|
|arm-training/02-SelectionDAG|7.317092|6.206304|0.848193|
|arm-training/03-MachinePipeliner|6.360688|5.430820|0.853810|
|arm-training/04-Attributor|6.599587|5.618496|0.851341|
|arm-training/05-WholeProgramDevirt|5.942862|5.009327|0.842915|
|arm-training/06-ARMISelLowering|8.559531|7.467597|0.872431|
|arm-training/07-ARMTargetTransformInfo|5.025584|4.190340|0.833802|
|arm-training/08-MasmParser|3.421826|3.017507|0.881841|
|arm-training/09-AsmParser|2.816296|2.404688|0.853847|
|arm-holdout/00-ParentMapContext|6.089231|5.187010|0.851833|
|arm-holdout/01-ParseDecl|5.156298|4.335147|0.840748|
|arm-holdout/02-Driver|5.499464|4.791426|0.871253|
|arm-holdout/03-CoverageMappingGen|5.787300|4.759894|0.822472|
|arm-holdout/04-Metadata|5.687852|4.866279|0.855557|
|arm-holdout/05-ScalarEvolution|10.167534|8.721117|0.857742|
|arm-holdout/06-AArch64InstructionSelector|5.859820|4.876201|0.832142|
|arm-holdout/07-X86ISelDAGToDAG|5.267725|4.422101|0.839471|
|arm-holdout/08-ELF|6.047000|5.317907|0.879429|
|arm-holdout/09-InstrProfReader|4.638627|3.850826|0.830165|
|aarch64-training/00-SemaStmt|6.012758|4.923279|0.818806|
|aarch64-training/01-SemaExprCXX|6.281204|5.057829|0.805232|
|aarch64-training/02-SelectionDAG|7.359765|6.183350|0.840156|
|aarch64-training/03-MachinePipeliner|6.457493|5.440901|0.842572|
|aarch64-training/04-Attributor|6.542446|5.590771|0.854538|
|aarch64-training/05-WholeProgramDevirt|5.904664|5.037710|0.853175|
|aarch64-training/06-ARMISelLowering|8.560491|7.459861|0.871429|
|aarch64-training/07-ARMTargetTransformInfo|4.947170|4.126177|0.834048|
|aarch64-training/08-MasmParser|3.405693|2.953881|0.867336|
|aarch64-training/09-AsmParser|2.755815|2.357781|0.855566|

完整原样本/argv/频率负载、逐条目和独立20 CSV与raw归档为target-perf-aarch64系列。

### 续跑十一B最终结论：两目标全部PASS

|目标|30条目几何平均比|独立20源|留出10|耗时降低|
|---|---:|---:|---:|---:|
|armv7l|0.856351167|0.858165628|0.868458776|14.365%|
|aarch64|0.847699213|0.847858623|0.847902567|15.230%|
|x86_64（20历史）|0.855890085|未在本轮重新测量|未在本轮重新测量|14.411%|

两目标各300次、共600次原样本，无删样或重跑；主判据均严格<0.98。ARM与x86_64相近，AArch64的候选/普通比更低。20独立源的两训练cohort重复输入合并全部10样本，留出每侧5样本；原30条目统计保持三组各10的权重，不混用口径。两目标分时测量，CPU/策略/方法与20相同，完整边界频率和负载原文均保存。

收尾：60输入SHA再次相同；普通clang/4ec候选、22RPM全SHA/大小、归档证据及原源码元数据、禁用cache/ninja SHA不变，原缓存47987文件/96881772832B。源HEAD仍b7e61fb92b34795868230e4f9cee8e3ec65496f6、spec/helper SHA不变且tracked clean。没有LLVM源码修改、Gerrit查询/推送、原树CMake/Ninja/-P、链接/重写、ARM树访问或全构建。两段锁分别约28.7/28.4分钟，全部释放，proc/scope回收；资源详情在target-perf-resources，磁盘底线通过。没有产品准备错误；公开driver仅修正EOF空白格式告警，未改运行脚本/参数或重测。

## 续跑十二：表述修正与变基上传验收补充

续跑十二d08b54da276102c2b607fbddd07966111f5147cd父b7e61fb；作者、提交者、Signed-off-by均Hao Lin <hao.lin@samsung.com>，全局配置未改。202项及历史候选新安全/tiny/post通过，overlay无权限NOT RUN，第七步采集入口第二次准备失败STOP；没有推sandbox。详情22，不以小根测试冒充完整树演练。

取消的首次/暖配置对照实验没有补做：已认证的是文本门禁证明相关变化的技术影响为零，内容与首次/暖配置差异一致；不是差异来源因果归因已经实证。历史PM判断和技术证明应区分记录。

以下为周五变基及上传的验收补充；本轮没有执行的内容一律待验证，不能以已有材料名称代替实物认证：

- 记录变基父提交、树、源码/spec/helper/profile/工具/候选各身份及author/committer/Signed-off-by；若tizen_base合入归档修复，处理spec冲突后重证受影响项。
- 保存现场完整dry-run、tool-plan/真实构建复核JSON、工具版本、原RPM PATH/which和执行顺序日志；TF成对出现时保存归档前后SHA与预编译输入证据。第六步本次缺失，仍待验证。
- 解开全套Quickbuild RPM，逐包复查实体/别名/缺失debug与debugsource的既定例外、无BOLT产物及导出残留；普通后处理一次、尾检最后执行。比较debugsource上一快照，本轮只有22普通RPM的CMake内容审计，非新全包认证。
- 实测新增各阶段wall、cgroup峰、进程VmHWM、磁盘高水位，并测下游并发编译的总内存；本轮小门禁资源不能代替Quickbuild或下游并发。
- 对accel实际抽取、patchelf、重打包链取证，确认worker实际执行文件路径/最终SHA、默认配置与clang/clang++/clang-cl/clang-cpp及三元组driver入口，避免测试了另一实体。
- 建立最终SHA到BOLT前/后符号资料映射，保留pre-strip身份链和日志，做一次函数级崩溃定位演练；完全strip实体不声称有源码级调试能力。此端到端调试演练仍待验证。
- 发布模式完整LLVM构建、新树/Quickbuild目标性能与可重现性均待验证；历史十一B ARM/AArch64性能已有，但不替代变基/Quickbuild实物重测。发布mini仅证明后处理机制，不替代全构建。
- 变基若改变链接输入、profile、BOLT参数/工具、候选安全字段或后处理链，重新认证对应匹配、安全、对象、性能和RPM清单/post证据；本轮stop后的缺项不能被“文本没冲突”自动关闭。
