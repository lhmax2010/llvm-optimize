# 18 文本差异补充认证：甲类通过，CMake phony 输出块超出乙类

2026-10-14，周三续跑六。本次产品门禁仍 FAIL：7,439 块中 7,438 块通过，1 块不在允许范围，状态 STOP_CMAKE_PHONY_OUTPUTS_OUTSIDE_ALLOWED_CLASSES。失败后没有执行对照配置、当前草案两模式展开、30/90 对象、双模式小 spec、RPM/DWARF 预期差异、性能或 sandbox 推送。不能把此次认证记为完成。

## 人工裁决与执行范围

PM采用 a1410e3d14b8836e3f9be5a1b4380f914dc2e705（父 cb679968）的删除第二次安装/compare-root 草案，确认上轮 103 个夹具通过。本轮不改 source/spec/helper/profile/patch；上轮夹具及静态封套 PASS 沿用，并非新增测试。

甲类只允许同一构建语句的变量绑定变化，变量不得被两文件中的任何 rule 字段以 $NAME 或 ${NAME} 引用，输出/输入/隐式依赖/order-only/rule/其他变量全部不变。乙类只允许 RERUN_CMAKE 的 build build.ninja 语句依赖清单变化。本轮严格按这两个条件认证，不把规则关联性扩充为许可。

PM对 debug 间接源读取的三项覆盖接受：86普通配置产物字节相同；Quickbuild 现场 tool-plan 保证不重编普通对象；安装的 clang-22 完全 strip，不把 BOLT 源带入 debugsource。因此该读取不再单独阻塞本地认证，但不撤销本次文本门禁失败。周四增加实物 debugsource 文件清单对比。

原树禁 CMake/Ninja（含 -n、-P 安装）不变；唯一准许的新配置是认证通过后的临时无 BOLT 对照，必须专用 ThinLTO 缓存。本次认证失败，故对照 NOT RUN，原缓存没有新写入。共享锁/资源/磁盘/准备性一次修正/保护规则均沿用。

## 甲类逐块 PASS

复用17保存的非equal SequenceMatcher opcode坐标，不重新生成 Ninja，也不使用 compdb。读取16的 config-before/config-after 两份 build.ninja、CMakeFiles/rules.ninja，逐文件 SHA 与17原始记录一致；每块按坐标切片与17保存原文再次逐字相等。

所有改动变量仅两个：TARGET_COMPILE_PDB、TARGET_PDB。7,421 个甲类文本块全部只含这两个变量的绑定删除或改值，每块所属构建语句均被完整认证。共6,838条普通语句：6,255对象、583链接。头行逐字相同，因而输出、输入、隐式/order-only依赖、rule名相同；删去实际改动的变量绑定后，剩余完整语句逐字相同，其他变量值亦逐项相同。每条证明的头行/剩余字节SHA与每块坐标在 text-proof-certification.json。

搜索方法：解析两文件中所有顶层 rule 定义，遍历其完整字段（不限 command，同时包括 description、depfile、rspfile、rspfile_content 等），两快照均搜索。build.ninja 中两次均0条 rule；rules.ninja before1,215条、after1,239条，共2,454条定义。每个变量分别按以下正则搜索，精确匹配裸变量及花括号变量；为保守起见不排除 $$ 字面转义：

```text
\$(?:TARGET_COMPILE_PDB(?![A-Za-z0-9_])|\{TARGET_COMPILE_PDB\})
\$(?:TARGET_PDB(?![A-Za-z0-9_])|\{TARGET_PDB\})
```

两变量分别0命中。完整搜索结果、逐块/逐语句证据、四文件SHA见JSON；原认证脚本 text-proof-certify.py 公开。并未只搜索 Linux command 字段或只搜索 $TARGET_PDB。

## 乙类：一块 PASS，一块 FAIL

真正的 RERUN_CMAKE 块为第7,437块，build build.ninja 头的输出和rule均保持，绑定不变，只改隐式依赖列表：删88、增20，满足乙类。

第7,438块则是 CMake 输入文件的多输出 phony 回退语句，其形状为：

```ninja
build <全部 CMake 输入文件清单>: phony
```

它位于“缺失CMake输入不是错误”的回退规则处，rule是phony；不是RERUN_CMAKE，也不是build build.ninja。该块删除相同88路径、增加相同20路径，但改动位于冒号左侧的**输出**，没有变量绑定变化，也没有依赖变化。甲类要求输出不变，乙类要求指定的重跑语句，聚合许可只允许新增BOLT依赖，故三者均不能覆盖。两个清单的对应关系证明与CMake依赖相关，但不满足本轮准许条件。

完整两条原文与差异独立公开：text-proof-phony-failure-before.ninja.txt、after.ninja.txt、diff.txt；不是将长输出头截断后判断。完整块坐标和88/20对应性在JSON。以下清单既是第7,437块的依赖删除/增加，也是第7,438块的输出删除/增加：

### 删除的88项（完整路径）

```text
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/third-party/benchmark/cmake/gnu_posix_regex.cpp
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/third-party/benchmark/cmake/posix_regex.cpp
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/third-party/benchmark/cmake/pthread_affinity.cpp
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/third-party/benchmark/cmake/steady_clock.cpp
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/third-party/benchmark/cmake/thread_safety_attributes.cpp
/usr/share/cmake/Modules/CMakeASMCompiler.cmake.in
/usr/share/cmake/Modules/CMakeCCompiler.cmake.in
/usr/share/cmake/Modules/CMakeCCompilerABI.c
/usr/share/cmake/Modules/CMakeCXXCompiler.cmake.in
/usr/share/cmake/Modules/CMakeCXXCompilerABI.cpp
/usr/share/cmake/Modules/CMakeCompilerIdDetection.cmake
/usr/share/cmake/Modules/CMakeDetermineASMCompiler.cmake
/usr/share/cmake/Modules/CMakeDetermineCCompiler.cmake
/usr/share/cmake/Modules/CMakeDetermineCXXCompiler.cmake
/usr/share/cmake/Modules/CMakeDetermineCompiler.cmake
/usr/share/cmake/Modules/CMakeDetermineCompilerABI.cmake
/usr/share/cmake/Modules/CMakeDetermineCompilerId.cmake
/usr/share/cmake/Modules/CMakeDetermineCompilerSupport.cmake
/usr/share/cmake/Modules/CMakeDetermineSystem.cmake
/usr/share/cmake/Modules/CMakeFindBinUtils.cmake
/usr/share/cmake/Modules/CMakeNinjaFindMake.cmake
/usr/share/cmake/Modules/CMakeParseImplicitIncludeInfo.cmake
/usr/share/cmake/Modules/CMakeParseImplicitLinkInfo.cmake
/usr/share/cmake/Modules/CMakeParseLibraryArchitecture.cmake
/usr/share/cmake/Modules/CMakeSystem.cmake.in
/usr/share/cmake/Modules/CMakeTestASMCompiler.cmake
/usr/share/cmake/Modules/CMakeTestCCompiler.cmake
/usr/share/cmake/Modules/CMakeTestCXXCompiler.cmake
/usr/share/cmake/Modules/CMakeTestCompilerCommon.cmake
/usr/share/cmake/Modules/Compiler/ADSP-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/ARMCC-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/ARMClang-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/AppleClang-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/Borland-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/Bruce-C-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/Clang-CXX-CXXImportStd.cmake
/usr/share/cmake/Modules/Compiler/Clang-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/Clang-DetermineCompilerInternal.cmake
/usr/share/cmake/Modules/Compiler/Clang-FindBinUtils.cmake
/usr/share/cmake/Modules/Compiler/Compaq-C-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/Compaq-CXX-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/Cray-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/CrayClang-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/Embarcadero-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/Fujitsu-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/FujitsuClang-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/GHS-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/GNU-C-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/GNU-CXX-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/HP-C-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/HP-CXX-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/IAR-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/IBMCPP-C-DetermineVersionInternal.cmake
/usr/share/cmake/Modules/Compiler/IBMCPP-CXX-DetermineVersionInternal.cmake
/usr/share/cmake/Modules/Compiler/IBMClang-C-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/IBMClang-CXX-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/Intel-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/IntelLLVM-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/LCC-C-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/LCC-CXX-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/MSVC-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/NVHPC-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/NVIDIA-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/OpenWatcom-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/OrangeC-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/PGI-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/PathScale-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/SCO-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/SDCC-C-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/SunPro-C-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/SunPro-CXX-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/TI-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/TIClang-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/Tasking-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/TinyCC-C-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/VisualAge-C-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/VisualAge-CXX-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/Watcom-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/XL-C-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/XL-CXX-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/XLClang-C-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/XLClang-CXX-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/zOS-C-DetermineCompiler.cmake
/usr/share/cmake/Modules/Compiler/zOS-CXX-DetermineCompiler.cmake
/usr/share/cmake/Modules/Internal/CMakeDetermineLinkerId.cmake
/usr/share/cmake/Modules/Internal/FeatureTesting.cmake
/usr/share/cmake/Modules/Platform/Linux-Determine-CXX.cmake
CMakeFiles/simple.cc
```

### 新增的20项（完整路径）

```text
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/CMakeLists.txt
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/cmake/modules/AddBOLT.cmake
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/include/bolt/Core/TargetConfig.def.in
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/include/bolt/RuntimeLibs/RuntimeLibraryVariables.inc.in
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/lib/CMakeLists.txt
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/lib/Core/CMakeLists.txt
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/lib/Passes/CMakeLists.txt
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/lib/Profile/CMakeLists.txt
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/lib/Rewrite/CMakeLists.txt
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/lib/RuntimeLibs/CMakeLists.txt
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/lib/Target/CMakeLists.txt
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/lib/Target/X86/CMakeLists.txt
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/lib/Utils/CMakeLists.txt
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/tools/CMakeLists.txt
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/tools/bat-dump/CMakeLists.txt
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/tools/binary-analysis/CMakeLists.txt
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/tools/driver/CMakeLists.txt
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/tools/heatmap/CMakeLists.txt
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/tools/llvm-bolt-fuzzer/CMakeLists.txt
/home/abuild/rpmbuild/BUILD/llvm-22.1.8/bolt/tools/merge-fdata/CMakeLists.txt
```

## 全部7,439块的最终分类

|类别|块数|判定|
|---|---:|---|
|BOLT构建边|9|PASS|
|BOLT规则|1|PASS|
|聚合目标新增BOLT依赖|5|PASS|
|BOLT构建/聚合混合|1|PASS|
|甲：未被rule引用的变量|7,421|PASS|
|乙：RERUN_CMAKE依赖列表|1|PASS|
|CMake输入phony输出清单|1|FAIL，超出允许范围|
|合计|7,439|7,438 PASS / 1 FAIL|

旧四类16块的分类保留17证明，没有重新调用配置器。6838普通语句的编译/链接字段相同，支持普通命令不变的静态预期；但整体文本门禁未通过，不能宣称本地整体认证或Quickbuild现场tool-plan PASS。Quickbuild仍须实际执行 ninja -n llvm-bolt，确认无普通任务。

## 未执行与候选身份

无BOLT对照配置 NOT RUN：产品认证已失败，不用来源实验豁免门禁；因此没有PATH/which调用记录，也不能给出“不加bolt同样发生”的结论。两模式rpmspec展开 NOT RUN，未沿用旧草案展开顶替；30/90对象、当前草案双模式小spec、22RPM/DWARF逐项预期差异、30×5性能全部 NOT RUN；几何平均未知。预期差异政策仍只允许clang实体/别名以及有证据的debug专属缺失，不得有BOLT产物，但本次未生成/认证实际预期清单。

本地候选保留16认证的历史工具后备产物，SHA4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9；此前N23592/M144032/S0/U1/Q383、R0.004238545%、S/N0%及note/strip-all/三目标/身份链PASS，本轮未重写或重新冒充完整资格。源提交仍a1410e3d14b8836e3f9be5a1b4380f914dc2e705，父cb67996861d070d68fec2b4c623eed7d20ba2e23。

sandbox NOT ATTEMPTED，远端前后未查，推送前提不满足；没有Gerrit评审/tizen_base推送。规定外情况已按要求停止，不自行添加phony许可或修改草案。若要续跑，须PM明确是否额外允许这个多输出phony清单块及证明条件；本次不请求无人值守确认。

周四核对六项：Quickbuild匹配统计同量级且双5% PASS；tool-plan PASS；compare-root PASS；Quickbuild clang性能复核；实际debugsource包清单与上一快照对比；不比较local/Quickbuild clang SHA。

## 运行记录

只有4GiB/swap0/nice19/ionice3只读轻scope；未获取共享锁，未有CMake/Ninja/链接或chroot/proc挂载，未进入ARM根。每类准备性修正一次规则下，动用一次文档路径修正：猜测17文件名错误，rg --files定位正确17_no_reinstall_and_text_gate.md后读取；不涉及产品判定，未重试失败门禁。新E为W/temp/bolt-v4-20261014-text-proof。最终保护审计与资源见text-proof-stop.json。
