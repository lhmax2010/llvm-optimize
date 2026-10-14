# 48 LLVM / GCC 升级后的归档转换重新认证

日期：2026-10-14。本手册是执行顺序与停止条件，不代表新版本已通过认证。当前实测进度见 [docs/50后续评审与升级探测](50_archive_followup_review.md)（完整构建锚点仍为[docs/49续十一结果](49_x86_build_resume_result.md)）；现有输入来自 LLVM 22.1.8。生产入口为 `tools/llvm_static_archives_source.py`，ARM 评审候选为 `tools/llvm_static_archives_arm_trial.py`，ARM RPM 集成仍未完成。

## 1. 哪些变化会触发检查

| 变化 | 现有检查与失败点 | 必须补的证据 |
|---|---|---|
| LLVM 主版本改变 | `validate_tools` 要求 `CERTIFIED_LLVM_MAJOR=22`；clang/llvm-dis/llvm-nm 的完整版本必须一致 | 新版本三工具路径、实际 ELF、版本、SHA；生产者/读取器兼容试验；完整重新认证 |
| LLVM 22 小版本改变 | 不再把 ARM 固定为 22.1.8；三工具仍须同版，ARM 每个函数的 target-cpu/target-features/tune-cpu 仍精确匹配 | docs/44 §2 同口径函数属性与命令全集普查；差异出现即停止，不因主版本相同放行 |
| 编译选项或 CMake 配方改变 | 未分类 token、未认证末项优化、关闭分段/符号选项、未认证 DWARF/FP contraction、错误 triple 都拒绝 | 实际 bitcode 内 llvm.commandline 全集；clang 源码依据；debug/发布参数一致与产物差异归因门禁，直接非LTO对照只诊断 |
| 调试/发布模式切换 | 无调试参数分支禁止 IR 的 `!llvm.dbg.cu`；有调试参数分支仍要求末项 `-gdwarf-4` | 三架构静态分类和真实源文件夹具；完整发布模式构建仍独立挂账 |
| IR 文本格式变化 | 依赖 LLVM 22 文本 IR 的单行定义、属性组、命令元数据与模块标志语法；已识别记录的重复/缺失拒绝；LLVM23多行module asm存在未识别且不报错的例外（见§6） | 新 llvm-dis 输出与现解析函数逐项比对，不能只看反汇编退出码 |
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
6. **运行两种模式实物夹具与根内限制。** 每架构至少20个跨子系统源文件，以原记录debug命令和spec精确sed后的发布命令各产bitcode，再交同一Source转换。2026-10-13 PM续三最终十项判据见[docs/49续三 §20.1](49_release_contract_final.md)：ELF头相同；SHF_ALLOC按名称/类型/COMDAT签名/link-order目标递归身份分组比较属性与全部内容，保留同身份重复节内部顺序；有序语义节（init/fini/preinit数组、ctors/dtors及点后缀、C标识符节名）按节名保留身份序列；只比较每目标节内部重定位顺序，规范SECTION/LOCAL引用；符号多重集合排除明确限定的debug专用符号；COMDAT比较有序成员身份并排除debug成员；addrsig比较规范符号身份集合；发布对象无.debug*。REL隐式addend由目标字节覆盖。节顺序变化时反汇编两路原bitcode、去掉debug信息记录定义顺序，仅诊断。比较器先通过正负夹具。2026-10-13续四裁决保留它作为比较工具，认证改为参数一致与差异归因：规范化输入/输出路径后只可缺少Source实际debug集合（当前固定为-g、-gdwarf-4），其他参数及顺序、clang实体SHA、cwd与环境集合相同；产物不同必须用同版opt --strip-debug和llvm-diff证明相关函数IR差异已存在于输入，或将去debug后的debug输入按原发布命令再转换，相关函数节/重定位/函数及映射符号与发布产物相同。差异只限被归因函数的节、重定位、映射符号、函数size；其余仍满足十项规则。未归因差异或参数失败使发布认证FAIL，不阻塞debug主线自身的独立验证，不允许自行扩充归因范围。每个差异函数保留反汇编原文，见独立辅助tools/check_release_attribution.py与[续四报告](49_release_attribution.md)。直接非LTO对照只记录“预期差异：转换对已做链接前优化的bitcode再次完整优化”。旧停止记录不回判。根内Python使用实际`/emul`工具与sh、临时`/proc`，监测clang软硬AS并做64MiB失败且不产`.o`负例，退出卸载。
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

- 续四三架构60对参数门禁全部PASS；53对产物相同、7个文件/架构组合的20个函数实例由后端路径(b)归因PASS（指定函数llvm-diff均exit0，去debug后再转换对应函数相同），发布夹具认证完成。Source/Commands及原十项比较器不变。此结论不是任意输入debug/nondebug代码一致性的证明，也不代替完整发布构建（docs/49_release_attribution.md §3–§4）。
- 原续三Serialize.cpp停止结论按当时判据成立并保留；本轮依据新裁决重新归因，而非改写历史记录。当前独立辅助16测试PASS；十项比较器此前41测试PASS。

- 续四两次x86全量回归与候选apply/tree PASS。续十一debug完整构建经一次-ba --noprep串行续跑完成；22RPM、归档/运行库、宿主及Tizen消费者、独立-bi与SKIP均通过，BOLT已交接。验收4同环境非归档比较因58.154GiB<85.5792GiB跳过，仍待PM，不宣称完整对照通过。详见docs/49_x86_build_resume_result.md §11。
- 两ARM宿主全量210/212档after SHA与docs/40 §12全同，原消费者和strip证据按合同沿用。ARM32根内小试在临时/proc挂载前Exec format error；只读核查宿主无qemu/ARM binfmt条目，Source未执行。按规则停止，AArch64根内小试、两根64MiB负例在该轮NOT RUN，按续十二决定暂停至下周；bash清单和LLVM23探测现已由docs/50完成。宿主原生工具4GiB生效不能替代根内原生sh启动器的实际进程limits证据（结果续页§12–§15）。
- 发布模式完整构建尚需独立执行；静态分类和局部夹具不能替代它。用户确认当前Quickbuild Tizen-Base-Toolchain定义`_toolchain`走debug，未来Tizen-Base未定义该宏走发布；此项优先级提高，待PM安排。
- ARM 第二段 spec 集成、完整 `%install`/RPM 与消费者验收仍需完成。
- 仓库验证驱动bash清单已完成：14文件登记（10个辅助驱动/脚本、4个测试/夹具），尚未迁移，不改驱动；原生bash/dash/sh专项6/6 PASS。LLVM源码自身bash检查仍留待总部替换dash时另做（docs/50 §6）。

下一次根内认证先只读检查实际binfmt条目和ARM ELF执行能力；宿主重启后的环境不能由历史根内PASS推定仍有效。当前mmap_min_addr=65536，本轮未更改。注册/初始化操作仍按用户当次授权执行，失败不自行改宿主配置。

## 6. 2026-10-14 LLVM23前向读取探测发现

官方LLVM23.1.3读取现有LLVM22.1.8 bitcode，x86_64/armv7l/aarch64各200个、共600样本均成功；当前未改解析器无异常，但返回字段并非全部正确。包含全部8个module asm成员；LLVM23把`module asm "..."`改为`module asm`与下一行字符串，现单行前缀解析漏读8个声明，ARM32的2项asm节跟踪也丢失。此事实要求升级时新增多行语法认证与固定正负夹具，不能只改CERTIFIED_LLVM_MAJOR。生产入口仍拒绝非22，不因本次只调用解析函数的探测而允许23进入%install。

600样本的转换flags、policy、原命令、triple/PIC/CPU/features相同；保留属性/元数据文本在x86182、ARM32179、AArch64186项不同，不能推出23代码生成等价。完整差异、工具/输入SHA及抽样规则见[docs/50 §7](50_archive_followup_review.md#7-llvm23前向读取探测方法与工具)与[600项解析差异JSON](50_llvm23_probe_results.json)。本次没有用LLVM23生成机器码、没有新版本完整构建；仍需按§2全流程重新认证。
