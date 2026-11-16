# 109：先行开关设计

设计先于产品编辑保存。输入为a061f4e4、61ef5d31及原Part1的spec差异，两份PS5评审原文。

## Part1完整spec范围

1. x86_64的LLVM_LINK_LLVM_DYLIB由OFF改ON；CLANG_LINK_CLANG_DYLIB由OFF改ON。
2. 新增TIZEN_HYBRID_LINK=ON、BUILD_SHARED_LIBS=OFF、LLVM_TOOL_LLVM_DRIVER_BUILD=OFF。
3. 构建后8个驱动的readelf NEEDED断言；3个必须存在，其余保留可跳过约定。
4. BuildRequires附近增加readelf说明注释；没有增加Part1的Source、%files、%install或静态库转换变更。
父提交确实没有第2项三参数；关闭Part1时省略这三项，不人为加入OFF参数。LLVM_BUILD_LLVM_DYLIB/CLANG_BUILD_CLANG_DYLIB原本为ON，保持原样。

## 宏与组合

新增%bcond_without llvm_speedup和%bcond_without hybrid_link；保留clang_bolt原架构默认值。
只在两处有效宏组合总开关：
llvm_hybrid_enabled = with llvm_speedup AND with hybrid_link；
llvm_bolt_enabled = with llvm_speedup AND with clang_bolt。
后续单项条件只读有效宏，不重复总开关表达式。x86_64之外不启用Part1/2。

| 总开关 | hybrid_link | clang_bolt | 结果 |
|---|---|---|---|
| 开 | 开 | 开 | 默认保持a061f4e4原展开 |
| 关 | 任意 | 任意 | Part1/2都关，恢复父链接参数和普通clang |
| 开 | 关 | 开 | 父链接方式、BOLT仍开 |
| 开 | 开 | 关 | 混合链接、普通clang |
| 开 | 关 | 关 | 父链接方式、普通clang |

“BOLT开、混合链接关”在现有源码接入上成立：
父提交x86_64同样把clang静态链接到LLVM组件；BOLT本身对组件链接显式DISABLE_LLVM_LINK_LLVM_DYLIB。
helper不要求TIZEN_HYBRID_LINK或全局LLVM_LINK_LLVM_DYLIB=ON；
门禁比较同一次构建的ordinary安装和clang，再检查BOLT改写，而非要求其他工具采用混合链接。
因此不强行耦合两个单项开关。组合展开及全部helper回归在本任务验证；实际产物仍待102夜间验证，不冒称已构建。

关闭Part1时跳过专属readelf断言。CMake源码保持不动；AddLLVM.cmake/AddClang.cmake安装文本仍不同，
未设置TIZEN_HYBRID_LINK时不触发新增接口逻辑。Part3固定参数和Part4安全检查完全保留。
总开关不承诺整个tree、全部包或编译参数恢复到父提交，只恢复Part1/2链接方式及普通clang。

## R1及范围

成功leader保持未reap状态，wait_group_exit(pid,10)确认组无存活成员；
超时转为指定COMMAND_ERROR并进入现有kill/wait/reap。
/proc等其他错误保留原诊断。成功路径先清_ACTIVE_GROUP再reap。
H1–H5/N1不改；仅补spawn不变量注释与回归。
R2嵌套信号问题、SystemExit/KeyboardInterrupt重抛前记录cleanup错误延后。

## 门禁

默认三架构rpmspec展开逐字节相同；总开关关闭的主cmake argv与父逐项相同
（Part3改变环境旗标值，但argv仍引用同样CFLAGS/CXXFLAGS）。
五项原解析与新组合；567既有项+R1+评审回归。任何产品FAIL停止，不自行改断言。
