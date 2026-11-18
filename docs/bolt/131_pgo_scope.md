# 131 号 C：PGO 作用范围盘点

**已证实旧实验把 PGO 标志传给运行库。全量逐命令覆盖为 UNKNOWN。** 58 号 D 的 Ninja 进度识别 6,229 个编译对象，其中 4,160 个可由进程采样直接确认带 profile-use。

| 分类 | 日志对象 | 日志目标 | 实际采到参数的对象 | 实际采到参数的目标 |
|---|---:|---:|---:|---:|
| LLVM/Clang/LLD | 3,684 | 304 | 2,611 | 252 |
| runtime | 896 | 87 | 157 | 37 |
| other | 1,649 | 195 | 1,392 | 183 |

按 Ninja 对象输出去重，按 CMake 目标目录和名称识别。主类含 LLVM、Clang、LLD 库和工具。clang-tools-extra、LLDB、benchmark、TensorFlow 归入其他。运行库目录包括 compiler-rt 和 openmp。进程采样另有 93 个带标志的输出路径未关联到进度对象，单列于同一证据。

58 号 D 的构建日志第 395 行记录 `-DLLVM_PROFDATA_FILE=/home/abuild/pgo-resource/clang.profdata`。进程采样第 7737 行直接确认 compiler-rt 的 RTSanitizerCommon 使用该 profile。59 号使用了上一次 D 的产物采集 BOLT profile。

原 D 构建根和登记的归档目录均无 build.ninja。Ninja 进度是所见对象清单，采样会遗漏进程。两者不能替代全图的命令导出。[对象与目标 TSV](../../tools/bolt/results/task131/historical-scope-units.tsv)。[逐个采样命中、参数与原始日志行号](../../tools/bolt/results/task131/historical-scope-sampled.json)。[源路径和进度汇总](../../tools/bolt/results/task131/historical-scope.json)。

## 实现定位

LLVM 22.1.8 的 HandleLLVMOptions.cmake 1262–1276 行在主配置追加 LLVM_PROFDATA_FILE 选项。PS5 将 compiler-rt 和 openmp 列在 LLVM_ENABLE_PROJECTS，两者会继承主配置的 C/C++ 和链接参数。第二批候选在这两个 CMake 子目录内移除该开关，并将本地 LLVM_PROFDATA_FILE 置空，外层仍保留主构建配置。

候选用 Ninja compdb 检查实际命令，根据上述运行库目录及链接输出分组。主构建 C/C++ 编译命令在 PGO 开启时必须使用认证文件。运行库和关闭 PGO 时的命令不得出现 PGO 标志。运行库有独立 Ninja 图时还须把独立图纳入 132 号验证，现有夹具只验证平面主图规则。
