# 48 LLVM / GCC 升级后的归档转换重新认证

日期：2026-10-13。本手册是执行顺序与停止条件，不代表新版本已通过认证。当前实测进度见 [docs/49](49_round4_revision_and_x86_build.md)；现有输入来自 LLVM 22.1.8。生产入口为 `tools/llvm_static_archives_source.py`，ARM 评审候选为 `tools/llvm_static_archives_arm_trial.py`，ARM RPM 集成仍未完成。

## 1. 哪些变化会触发检查

| 变化 | 现有检查与失败点 | 必须补的证据 |
|---|---|---|
| LLVM 主版本改变 | `validate_tools` 要求 `CERTIFIED_LLVM_MAJOR=22`；clang/llvm-dis/llvm-nm 的完整版本必须一致 | 新版本三工具路径、实际 ELF、版本、SHA；生产者/读取器兼容试验；完整重新认证 |
| LLVM 22 小版本改变 | 不再把 ARM 固定为 22.1.8；三工具仍须同版，ARM 每个函数的 target-cpu/target-features/tune-cpu 仍精确匹配 | docs/44 §2 同口径函数属性与命令全集普查；差异出现即停止，不因主版本相同放行 |
| 编译选项或 CMake 配方改变 | 未分类 token、未认证末项优化、关闭分段/符号选项、未认证 DWARF/FP contraction、错误 triple 都拒绝 | 实际 bitcode 内 llvm.commandline 全集；clang 源码依据；debug/发布转换产物调试无关性门禁，直接非LTO对照只诊断 |
| 调试/发布模式切换 | 无调试参数分支禁止 IR 的 `!llvm.dbg.cu`；有调试参数分支仍要求末项 `-gdwarf-4` | 三架构静态分类和真实源文件夹具；完整发布模式构建仍独立挂账 |
| IR 文本格式变化 | 依赖 LLVM 22 文本 IR 的单行定义、属性组、命令元数据与模块标志语法；重复、缺失或不识别的记录拒绝 | 新 llvm-dis 输出与现解析函数逐项比对，不能只看反汇编退出码 |
| GCC / libstdc++ 头文件改变 | module asm 白名单目前只有 `.globl _ZSt21ios_base_library_initv`；输出符号状态必须满足各架构门禁 | 新头文件路径/包版本/SHA、全部 module asm 普查、逐成员符号与消费者证据 |
| ELF/重定位变化 | ARM 未认证重定位硬失败，LE 禁止，IE 等待裁决；x86 和 ARM 各有 ELF 边界与 PIC 检查 | 新类型的 ABI 与 LLVM/lld 源码依据、可写/只读/非 ALLOC 分布、正负夹具和共享库运行验证 |
| 原生 shell 或工具路由改变 | shell/三工具必须是可执行 x86_64 ELF；AS/core 设置和读回不符失败；原生限制设置失败 exit125 | `/emul/usr/bin/sh` 实际指向与 SHA、实际执行 clang 的 `/proc/<pid>/limits`、64 MiB 负例 |

这些门禁不是对任意 LLVM 命令的通用重放支持；不以“只增加一个开关”代替认证。具体实现入口为两份 Source 的 `classify_options`、`ir_settings`、`validate_tools`，以及 ARM 的 `arm_classify_options`、`arm_function_targets`、`arm_pic_relocations`、`ARMNativeLimitCommands`。历史方法与已知边界见 docs/28 §1、docs/44 §2、docs/47 §9。

## 2. 固定执行顺序

1. **冻结旧锚点。** 保存 Source/补丁/源码提交、spec 展开、CMakeCache、三工具和 shell 的版本/SHA、输入归档及完整有序成员/索引、转换后 SHA、消费者输出。保留 x86 225 档以及两 ARM 输入与 JSON；不得覆盖旧证据。
2. **先做读取兼容性和语法普查。** 明确谁生产 bitcode、谁反汇编、谁转换。新版本 `llvm-dis` 读取旧输入的样本结果，只说明该方向；不能推出旧工具可读新 bitcode。记录命令全集、IR triple、PIC/PIE/Code Model、调试元数据、函数属性、module asm、CFI/type 标记、成员格式、重定位全集。
3. **写逐项差异依据。** 为新增/变更 token 查 clang 源码中的 frontend/IR 属性或后端选项处理；为重定位查目标 ABI 与实际 lld 实现。库头文件变化另查新的 module asm 意图与输出符号。未确定的项目保留 STOP，禁止扩大通配符绕过。
4. **先写固定字面量正负测试，再更新策略。** 依次更新版本门槛与文本解析假设、每架构 triple/优化策略及 token 分类、需补回的后端选项、ARM 函数属性认证表、module asm 白名单/输出门禁、重定位集合。只有实证变化的表才修改；不修改 Commands 来掩盖策略问题。
5. **验证旧行为与新行为两条线。** 用旧工具和旧输入运行新 Source，确认仍在承诺范围内的旧 x86 路线逐档/逐成员 SHA、完整索引和后端 flags 不变。再用新工具与新输入做全量转换、完整索引/强符号/PIC/Thumb 检查。新编译器可能改变代码生成；有差异须分析并建立经批准的新锚点，不能把新工具输出直接宣称为旧 SHA 不变。
6. **运行两种模式实物夹具与根内限制。** 每架构至少20个跨子系统源文件，以原记录debug命令和spec精确sed后的发布命令各产bitcode，再交同一Source转换。硬门禁为：全部SHF_ALLOC节名称/标志/大小/内容逐字节相同，作用于这些节的重定位偏移/类型/符号名/addend逐条相同；排除FILE及调试节的SECTION符号后，符号名称/类型/绑定/可见性/所在节名/值/大小逐项相同；发布对象不得含.debug。REL隐式addend须连同目标节原始字节验证；RELA显式addend直接比较。任一不符停止。直接非LTO编译与转换对象的结构差异只记录，不作通过判据；标注“预期差异：转换对已做链接前优化的 bitcode 再次完整优化”。这是2026-10-13用户事前裁决，旧停止记录保留。根内 Python 下使用实际 `/emul` 工具与 sh，临时 `/proc`，监测真实 clang 的软硬 AS，做64 MiB失败且不产 `.o` 的负例；退出卸载。
7. **完整打包与消费。** 运行真实 `%install` 和标准后处理，归档成员/索引/调试节全检，compiler-rt、libarcher 归属、非归档文件、七项宿主消费者、Tizen GNU ld 无 LTO/无插件及 lld 消费者、运行库探针、独立安装与同树 SKIP 均重新验收。ARM 根内 AS 和 accel 路由不能用宿主离线结果替代。
8. **冻结最终版本后生成补丁。** 候选 Source SHA、补丁顺序、完整构建指纹与日志保持一致；提交说明只写实际通过项。新大版本、小版本或新配方若未完成上述验证，标为候选而非已发布认证。

## 3. ARM accel 落后于正在构建的包时

ARM 的候选转换器选用构建环境中 `/emul` 的原生 x86_64 三工具，未假定刚生成的 ARM clang 会原生执行。bitcode 生产者由实际 CMake 编译器及其 accel 路由决定，包名版本不能替代生产者实测版本。（依据：docs/39 §2–§3、docs/40 §11–§12、docs/47 §9.2。）

升级时先登记 **bitcode 生产者、转换器、反汇编器、nm** 四项版本与 ELF 路径。若新生产者先于 accel 升级，不允许让旧 llvm-dis/clang 静默处理未知新 IR，也不允许在 `%install` 失败后 SKIP 掉含 bitcode 的归档。

可执行的过渡顺序是：在隔离环境准备同版的原生三工具，先证明其能读取新输入并完成重新认证；再更新构建环境的 accel 工具供给和入口；最后开展 ARM 完整打包验收。若无法提供经认证的同版三工具，先停止 ARM 发货并挂账。是否保留旧生产者完成某阶段由配方负责人决定，本手册不擅改编译器或关闭门禁。不要把“新读取器能读旧 bitcode”当成“旧读取器能读新 bitcode”的依据。

## 4. sh 从 bash 切换到 dash

入口保持 `/emul/usr/bin/sh`，但每次解析实际指向、名称、x86_64 ELF 身份与 SHA。脚本只用共同支持的 POSIX 写法：`ulimit -v`/`ulimit -c` 同时设置软硬值，再用 `-S`、`-H` 分别读回；探针由 shell 内置 `while read` 读取 `/proc/self/limits`；执行路径是 `exec "$@"`。

启动前用 argv 形式的 `/usr/bin/env -u BASH_ENV -u ENV` 清除环境脚本入口；不依赖 bash 的 `--noprofile/--norc/-p`。shell 缺失、架构错误、ulimit 不支持或读回不符均失败，不提供未生效放行选项。单元测试覆盖宿主 bash/dash/sh 的读回、exit125、参数空格/引号/美元符号、环境脚本不执行和超时 SIGKILL；真实根内仍须另做进程 limits 与负例，不能由单元测试推定。（实现与本轮结果：docs/49 §3。）

## 5. 当前挂账

- LLVM 23 官方工具的样本探测结果以 docs/49 为准；未完成时写 NOT RUN/SKIP，不宣称兼容。
- 发布模式完整构建尚需独立执行；静态分类和局部夹具不能替代它。
- ARM 第二段 spec 集成、完整 `%install`/RPM 与消费者验收仍需完成。
- 仓库验证驱动的 bash 依赖清单见 docs/49；本轮不改这些驱动。LLVM 源码自身的 bash 检查留待总部替换 dash 时另做，不在此手册中假定其已兼容。
