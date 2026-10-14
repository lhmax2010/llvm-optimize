# 17 单次普通安装草案与严格文本门禁停止

2026-10-14，周三续跑五。已完成草案编辑、103夹具与新源提交/封套；为完成第一步后续读取审核，提前执行依赖的第二步全量文本比对，结果FAIL。随后停止产品实验，未执行修正草案的两模式rpmspec展开、30/90对象、双模式小spec、RPM/DWARF预期清单、性能或sandbox。不是全部第一步认证PASS。

## 最新人工裁决

追加bolt后的第二次完整安装必然带入7个BOLT静态库、两个未登记manifest的工具别名和改写的LLVMConfig.cmake；prune拒绝未登记别名。采用删除第二次安装，不给prune加特例。普通安装已完成，由原候选install子命令单独替换clang-22；改用更严格的构建根清单不变门禁。前轮原cache新增361文件1674072B由PM接受为交接cache正常变动；以后若临时配置，用专用cache。本轮只读现有快照，不执行新配置；原树禁cmake/ninja（含-n/-P安装）不变。文本分类覆盖所有build/rule及无输入CUSTOM_COMMAND，不用compdb。产品失败即停、每类准备性错误最多一次修正与资源/保护规则沿用。

## 草案修正及夹具

删除ordinary-exports目录/备份/恢复、第二次安装及其写预算、prune调用；原普通CMake安装仍仅一次。保留旧prune函数/CLI供原有历史夹具与审计，生产不调用；不是增加别名特例。新增compare-root子命令：重新取构建根清单，保存install-after-pipeline.json，逐路径检查新增、删除、类型、权限、大小、SHA、软链接目标，以及目录/链接权限与根目录权限；报错指明第一个不同的相对路径。snapshot CLI新增完整权限metadata，原inventory文件形状保持，避免改变旧RPM清单协议。

门禁位于pipeline之后、原普通安装整理之前；候选安装仍在原%install末尾，以避免之后的原ln命令覆盖已规范化别名。该门禁证明BOLT配置/构建/pipeline未改变普通CMake安装；门禁之后原有普通安装整理与末尾candidate install保持原顺序。没有把平台正常整理的变化当BOLT副作用。其余生产重链/重写参数、匹配/note/strip-all/微型/单次原post尾检不变。

103/103夹具PASS：原95不变，新增8（不变通过；新增文件/软链接、删除文件、内容/文件权限/链接目标/目录权限变化均失败，错误包含路径）。Python3.9 parse及helper镜像一致。fixtures净0.581s/轻scope1.527s。当前草案只有静态源码检查确认一个-P安装、无ordinary-exports/prune及有compare-root；**本次debug/release rpmspec展开未执行**，不能拿16的旧草案展开顶替。

新源提交a1410e3d14b8836e3f9be5a1b4380f914dc2e705，父cb67996861d070d68fec2b4c623eed7d20ba2e23，tree33b4e9f84cec3336878501d55fe243b41c092c80；spec SHA14d17a60369a2c05661037583740b410f0fd710aef2c0c78de08175a57bb6c0c，helper SHA7614228b5da020fd1ae08eaef0ebaf096c317f21a370e249285ee632711888e7。完整binary patch留E；公开review.patch+不变profile.xz封套静态apply/整树PASS。新源码尚未具备推sandbox资格。no-reinstall-draft-change.diff给相对d6ddbff5的全部改动；manifest给源码身份与封套哈希。

## 全量文本分类：严格FAIL

范围为16保存的两份build.ninja、CMakeFiles/rules.ninja，原件SHA与压缩快照一致；未重新生成、不执行Ninja/compdb。块定义为SequenceMatcher非equal opcode（零上下文）；混合块只计一次。完整原文在build.diff/rules.diff，逐块坐标与分类在JSON，首版全部记录压缩为edge-details.json.xz（77MB原JSON保留E，公开xz约1MB）。只读归类识别安装聚合CUSTOM_COMMAND与新BOLT依赖别名，没有改动门禁或重跑配置。

|分类|文本块数|判定|
|---|---:|---|
|BOLT目录构建边/依赖别名|9|允许；共472条新增build语句|
|BOLT规则|1|允许；24条新增rule|
|聚合目标新增BOLT依赖|5|允许；6条聚合语句（含两个安装聚合CUSTOM_COMMAND）|
|BOLT构建与聚合依赖混合|1|允许；一个块中两类变更|
|普通PDB变量删除/改变|7421|**FAIL**；6255个对象边、583个链接边，共6838条普通边|
|CMake普通依赖移除及BOLT新增|2|**FAIL**；新增20个BOLT依赖，同时删88个普通检测/benchmark依赖|
|总计|7439|严格产品门禁FAIL|

每类原文示例（完整上下文见raw diff与JSON）：

```ninja
# 新BOLT构建（对应tools/bolt/lib/Core）
# 完整build行在JSON；以下是新增边的原OBJECT_DIR绑定
  OBJECT_DIR = tools/bolt/lib/Core/CMakeFiles/LLVMBOLTCore.dir
# 新BOLT rule
rule CXX_COMPILER__LLVMBOLTCore_Release
# 聚合依赖新增条目（install-llvm-libraries等）
# 行过长，完整原文保存在JSON statement_examples/aggregate_BOLT_dependencies
```

普通边失败原文，以clang对象与链接为例：

```diff
-  TARGET_COMPILE_PDB = tools/clang/tools/driver/CMakeFiles/clang.dir/
-  TARGET_PDB = bin/clang.pdb
# 对象边删除以上两个绑定；链接边删除COMPILE_PDB并改PDB为：
-  TARGET_PDB = bin/clang.pdb
+  TARGET_PDB = clang.dbg
```

CMake重跑依赖移除原文示例：

```text
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/third-party/benchmark/cmake/gnu_posix_regex.cpp
/usr/share/cmake/Modules/CMakeCCompilerABI.c
```

CMake依赖增添原文示例：

```text
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/CMakeLists.txt
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/cmake/modules/AddBOLT.cmake
```

PDB差异在此前已采普通编译/链接命令中未体现；保存的Linux rules没有$TARGET_PDB引用。但PM允许类别不含这些普通变量变化，也不含删除普通CMake依赖，所以不能自行视为无害豁免。两份快照只能证明变化存在；是否来自BOLT或首次/缓存配置阶段区别，没有本轮对照配置，不能武断归因。runtime tool-plan仅查普通Building/Linking计划，本轮不运行；严格文本FAIL不允许推断Quickbuild该门禁PASS或据此推送。正常Quickbuild仍保留ninja -n llvm-bolt/tool-plan现场门禁。

## BOLT段之后的构建目录读取审核

|位置/命令|实际路径/依赖|本次判断|
|---|---|---|
|原%install的ln/cat/mkdir/mv/cp -P/rm|均为buildroot里的clang配置/别名、LLDB SDK搬移/库与普通清理|不读取重新配置的build产物；保持原步骤|
|cp -a ../clang/bindings/python/clang|PROJECT/clang源目录，位于build之外|16/本次源清单不变；不会读改写的CMake导出|
|候选install helper|build/clang-bolt/clang.candidate、identity.json及identity.before_path的BOLT输出|主动BOLT资产，helper验证SHA/note/ELF；不是普通配置产物读取|
|%files/%manifest|安装树、PROJECT的llvm.manifest及平台debug manifest|不再从build复制重配置的LLVMConfig/Exports；无%check段|
|原debug post/find-debuginfo|PROJECT及DWARF引用的build生成头/其他源，宏传%_builddir/%buildsubdir|存在间接build读取。86配置产物相同是部分证据，完整边门禁已FAIL，完整DWARF逐文件证明未跑；不认证完全不受影响|
|原arch/os/isu等post|安装树strip/compress/python等|没有新build导出读取；没有第二次CMake安装|
|新增BOLT post helper|build/clang-bolt/install-state.json、ordinary-clang-22、post-gate；buildroot/lib64/clang/22|读取自己的状态/普通compiler副本及安装资源，要求SHA/三目标/别名；不读普通PDB绑定|

平台宏与find-debuginfo源码只读定位，路径和判断在no-reinstall-stop.json。读取审核仅资料部分完成，没有把间接DWARF读取的未知项视为PASS；第一步第4/5项因此未完整认证。

## 收尾与未完成项目

debug/release当前草案展开NOT RUN；30历史+90对象、双模式小spec、22RPM逐项预期/DWARF清单、30×5性能全部NOT RUN，几何平均未知。新方案应保持普通安装清单，最终只允许clang实体/别名变化及既定debug专属缺失例外，不允许任何BOLT产物，但本轮未用实际包认证。sandbox未尝试，远端前后未查；源a1410e3d…仅本地草案，Gerrit评审/tizen_base无推送。

本地候选仍SHA4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9，来自历史工具后备，未重新重写。周四核Quickbuild日志N/M/S/U/Q、R、S/N同量级且双5%PASS，并复核Quickbuild clang性能，不要求两边SHA相等。

保护审计PASS：22RPM/普通clang等完整SHA大小、归档独立install证据元数据、原源码清单一致；原树坏cache/ninja配置保持17f7fbc7…/c0068a3e…，未恢复/写入。原ThinLTO cache仍47987/96881772832B，本轮0新增，前轮增量按PM接受。没有任何cmake/ninja/链接、新配置、chroot/proc mount或共享锁；全是4GiB/swap0/nice19/ionice3轻scope，全部回收；不进入ARM根、不改W tracked/llvm。对比scope151.782s/峰0.549GiB/VmHWM387212kB，fixture1.527s/峰0.055GiB，freeze18.570s/峰0.482GiB，审计16.060s/峰0.974GiB。没有>10GiB写入；原根free59147931648B。

本轮未动用准备性错误重试。严格产品失败后仅归档、只读细分类、Git封套验证与报告/发布；不会依据“Linux未使用PDB变量”放宽准入。GitHub源修订材料abc3e19已推；完整停止材料与raw索引随后分步推送。

## 各类附加原文摘录

ordinary_PDB_metadata_change 原文示例：

```ninja
  TARGET_PDB = lib64/libtf_xla_runtime.pdb
```

BOLT_build_edges 原文示例：

```ninja
build tools/bolt/list_install_components: phony
```

BOLT_build_edges+aggregate_BOLT_dependencies 原文示例：

```ninja
build tools/bolt/lib/Core/all: phony lib64/libLLVMBOLTCore.a
```

BOLT_rules 原文示例：

```ninja
rule CXX_EXECUTABLE_LINKER__llvm-bolt_Release
```
