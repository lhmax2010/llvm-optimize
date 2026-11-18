# 131 号 D：PGO 匹配计数方法

**UNKNOWN。** 58 号留存 profile 已用 Tizen LLVM 22.1.8 读取并证实为 IR 类型，完整计数方法与真值夹具尚未通过。

## 已确认的类型

58 号 prepare.py 第 12 行显式传入 LLVM_BUILD_INSTRUMENTED=IR。Tizen llvm-profdata 22.1.8 的实际输出为：

~~~text
Instrumentation level: IR  entry_first = 0  instrument_loop_entries = 0
Total functions: 176654
~~~

LLVM 22.1.8 初始 CMake 配置的 LLVM_BUILD_INSTRUMENTED 默认 OFF。LLVM_BUILD_INSTRUMENTED=IR 与 CSIR 显式分支分别使用 -fprofile-generate 与 -fcs-profile-generate，单独设置为 ON 落在 -fprofile-instr-generate 的 Frontend 分支。历史实验使用 IR。

| 方法 | 三类计数与分母 |
|---|---|
| -mllvm -pgo-warn-missing-function 及 mismatch 诊断 | 只有错误消息，没有 matched 或总体分母。COMDAT/weak 默认可能抑制对应警告。实测 -pgo-warn-mismatch 正写法在 22.1.8 不支持，提示 -no-pgo-warn-mismatch。 |
| -mllvm -stats | LLVM 源码提供 NumOfPGOFunc、NumOfPGOMismatch、NumOfPGOMissing。优化构建需要确认统计是否编入。聚合数字还需证明是否覆盖每条查询、各编译单元与 ThinLTO 阶段，不能用来区分局部函数和不同 hash 的 ODR 定义。本次未取得实测计数。 |
| profile-use 前 IR 查询点或带补丁的 opt 重放 | 选作下一步验证方法。在同一插桩 pass 的候选筛选、函数名/hash 计算和 profile 查询处发出逐实例记录，再按模块和名称/hash 聚合。要验证捕获 IR 的阶段及 pipeline 与构建一致，同时核对查询错误类别。单纯加载插件或数 IR 函数不够。 |
| llvm-profdata show | 记录 profile 的条目与计数，不能知道构建实际查询了哪些条目，也不提供同一统计域的分母。 |

使用 Tizen loader 运行 clang 22.1.8 时，驱动再调用 cc1 的 argv 被当成 loader 入参。一次修正加 -fintegrated-cc1 后仍出现同一错误并停止 D。两次原文保留如下。

~~~text
-cc1: error while loading shared libraries: -cc1: cannot open shared object file
clang-22: error: unable to execute command: No such file or directory
STOP: could not link fixture with the Tizen toolchain
~~~

全匹配、完全缺失、部分 hash 不匹配、仅 COMDAT 不匹配、跨单元重复、执行次数零、同名局部函数、同名 ODR 定义 hash 不同、匹配后被删除及克隆等真值夹具均未完成。产物门禁记录 UNKNOWN。[首次命令和完整回执](../../tools/bolt/results/task131/match-probes.json)。[一次修正后的回执](../../tools/bolt/results/task131/match-probes-retry.json)。
