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


## 133-D D 续做

**UNKNOWN。** 将平台 clang 和 lld 作为私有 ELF 直接运行。先探测了原 PT_INTERP 与平台 `LD_LIBRARY_PATH` 的组合，返回 SIGSEGV。仅在私有副本中改用匹配的 Tizen PT_INTERP，保留历史原件。Tizen clang 22.1.8 的 `--version` 和小程序编译、链接成功。

IR 对照在 `opt pgo-instr-gen` 提取 profile key 和 CFG hash，用 LLVM 22.1.8 读入手工限定的 IR profile，在 `opt pgo-instr-use` 的输入实例上对照诊断与 entry-count。已通过全匹配、无缺失的健康单元、完全缺失和部分 hash 不匹配。平台 `opt -stats` 接受该选项，但这几份运行未输出所需的全量计数。

初次 COMDAT 夹具在 systemd 传参时将 `$name` 展开成了空字符串。保留原始错误，修正一次后重跑。重跑中 LLVM 正确生成 `@__profn_a = linkonce_odr hidden constant [1 x i8] c"a"`，夹具只识别 `private constant`，因此第二次准备错误停止。本次没有通过 COMDAT、跨单元重复、零计数、同名局部、不同 hash 的 ODR、匹配后删除和克隆的真值门槛。没有给出生产 PGO 匹配率。

~~~text
error: expected top-level entity
 = comdat any
 ^
AssertionError
~~~

~~~text
KeyError: '@__profn_a'
~~~

[工具最初探测](../../tools/bolt/results/task133-d/tool-direct-probe.json)、[匹配加载器的工具校验](../../tools/bolt/results/task133-d/tool-direct-rebound.json)、[首次夹具命令与原文](../../tools/bolt/results/task133-d/D-commands.json)、[修正重跑命令与原文](../../tools/bolt/results/task133-d/D-commands-retry.json)、[已完成夹具的逐实例对照](../../tools/bolt/results/task133-d/D-fixtures-retry.json)。
