# 361624：105续三部分评审（STOP）

结论：**NEEDS-FIX；试合并的树内 CMake 配置失败，未修复、未重试。**
361624 未并入已推送的 PS5 候选。本文件不是完整评审通过证明。

## 已读取与试合并

- revision da885208aeb52f55c448ff46873d242346727522，父61ef5d31ca91025c414c748477bef0c64ddfa67c。
- 完整提交/补丁：361624-full.diff；父提交：361624-parent.txt。
- HQ “在合入后改接”的原文来自361395 PS4评论，而非361624提交说明，见hq-later-rebase-comment.json：
  “NOTE: a follow-up change, 361624 (split tool subpackages into llvm-tools-subpkgs.spec; also touches bolt/ CMake), will be rebased onto this change after it merges.”
- 在独立游离工作树把361624 cherry-pick --no-commit 到PS5候选；唯一未合并文件packaging/llvm.spec，冲突原文trial-unmerged.diff。保持冲突、不解决、不提交；其他暂存变更见trial-staged.diff。
- 原候选a061f4e4工作树干净；其llvm/bolt/cmake/third-party与PS4相同，见candidate-final-identity.json。

## 已观察的影响（与完成验证区分）

| 位置 | 观察 | 当前证据边界 |
|---|---|---|
| bolt/lib、tools、unittests 的 CMake | 多处删除DISABLE_LLVM_LINK_LLVM_DYLIB，未限制在standalone分支 | 源码显示树内链接策略也受影响；叠加配置失败，未取得最终链接命令 |
| 新X86BoltMnemonicTables.cpp | 只在BOLT_BUILT_STANDALONE时列入目标，未登记LLVM_OPTIONAL_SOURCES | 树内配置实测拒绝，见下节 |
| 新llvm-tools-subpkgs.spec | standalone BOLT、LLVM_LINK_LLVM_DYLIB=ON；新增libllvm依赖；armv7l关闭BOLT runtime，LLVM_LIBDIR_SUFFIX=64写死 | 只读spec观察，未做该spec的ARM构建/解析，不能声称兼容 |
| llvm.spec | 新增--build-id=sha1；armv7l targets增加AArch64/X86；删除libgomp/libiomp别名；调整安装命令和部分%files顺序 | 需要保留候选的BOLT安装/后处理/显式debugfiles.list接入；实际冲突未解决 |
| clang/lld/llvm-ar、llvm-static-devel | 本补丁未直接改变这些工具的安装路径/所属文件条目，未直接修改转换器或static-devel清单 | 补丁文本观察，不代替包级验证；链接和安装布局的间接影响仍需核对 |
| BOLT runtime | ExternalProject参数新增空CMAKE_C_FLAGS/CXX_FLAGS，非standalone专属 | 与现有旗标策略的相互影响未做构建验证 |

## 配置与停止

两份配置都只启用LLVM+bolt、X86，LLVM_LINK_LLVM_DYLIB=ON、LLVM_BUILD_LLVM_DYLIB=ON、
TIZEN_HYBRID_LINK=ON；关闭BOLT runtime及非必要依赖。这是用于隔离链接策略的配置探针，
不是完整产品配置。工具来自74号Toolchain根，经自身loader运行。
只执行CMake配置（含其探针）及成功侧的ninja查询，没有编译LLVM产品目标。

未叠加侧：CMake rc=0；ninja -t commands -s bin/llvm-bolt rc=0、1条最终命令，
不含libLLVM.so。见candidate-cmake-command.json、candidate-cmake.log、candidate-llvm-bolt-link.txt。

叠加侧：CMake rc=1，不能进入ninja命令核对。完整原文with-361624-cmake.log；
源码对应361624-config-failure-source.txt。X86 CMake第27–29行仅在standalone追加新cpp，
LLVMProcessSources第105–113行会拒绝既非可选也未列入目标的cpp。
最小修正方向是将standalone专用cpp登记为可选源文件；本次**没有应用**该改动。

```text
CMake Error at cmake/modules/LLVMProcessSources.cmake:113 (message):
  Found erroneous configuration for source file X86BoltMnemonicTables.cpp

  LLVM's build system enforces that all source files are added to a build
  target, that exactly one build target exists in each directory, and that
  this target lists all files in that directory.  If you want multiple
  targets in the same directory, add PARTIAL_SOURCES_INTENDED to the target
  specification, though it is discouraged.

  Please update
  /home/linhao/Toolchain/development/llvm-optimize/temp/hq-review-105-20261116/trial-361624/bolt/lib/Target/X86/CMakeLists.txt


Call Stack (most recent call first):
  cmake/modules/LLVMProcessSources.cmake:59 (llvm_check_source_file_list)
  cmake/modules/AddLLVM.cmake:519 (llvm_process_sources)
  cmake/modules/AddLLVM.cmake:925 (llvm_add_library)
  /home/linhao/Toolchain/development/llvm-optimize/temp/hq-review-105-20261116/trial-361624/bolt/lib/Target/X86/CMakeLists.txt:31 (add_llvm_library)


```

同一日志另有平台CMake子进程装载OPENSSL_3.2.0失败的原文；
未把它掩去，也未在源码门禁失败后修改环境重试。即使消除该环境诊断，
上述新cpp与source-list检查的冲突仍有独立源码证据。

tool-plan只核对Ninja任务描述白名单，不直接检查链接命令或DT_NEEDED；
源码不允许新增的libLLVM共享库链接任务。若需要重建libLLVM则会触及该白名单；
若libLLVM已是最新，不能仅凭新增依赖断言门禁必然拒绝。
本次没有得到叠加侧任务图，**是否在真实Part2流程拒绝仍未验证**。

## 未运行

- 叠加侧ninja -t commands、实际tool-plan探针；
- find-debuginfo/build-id与post identity的详细源码对照；
- RPM中libLLVM.so的nm -D符号导出核实，不能据此确认复制表是否必要；
- ARM打包验证、实际构建/链接/安装、QB、Gerrit回复；
- 107：用户表示材料尚未准备，等待通知。

英文部分草稿361624-review-for-user.partial.md只覆盖已证明的配置问题，未发布。
