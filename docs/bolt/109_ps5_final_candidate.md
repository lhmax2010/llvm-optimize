# 109：PS5 最终候选准备（STOP，未推送）

**结论：STOP。默认x86_64展开失败，未推sandbox、未生成新的LLVM提交。**
sandbox只读核对仍为a061f4e415a895412516ffe076084f407f2d70a8。
本次新增有效宏采用了平台RPM不支持的expr宏；这是产品spec兼容性失败，
不按准备脚本错误处理，没有改代码后重跑。

| 项目 | 结果 |
|---|---|
| 基底身份 | a061f4e4，tree 8d08d49a1c70ebb06118d8d84734c695e24e6d32，父61ef5d31；原工作树干净 |
| 先行开关设计 | 已保存，再在新独立游离工作树实施 |
| 代码 | 仅llvm.spec开关、helper R1及注释；未提交、未验证通过 |
| 默认x86_64展开 | FAIL：RPM无法解析新增有效宏；基底的展开及nobuild解析rc=0 |
| armv7l/aarch64、总开关关闭、单项组合 | NOT RUN |
| 原567项、R1、评审回归 | NOT RUN，总数/通过数不冒称567；本轮unittest运行0项 |
| 提交说明、sandbox推送、回复更新 | NOT RUN；原FINAL文件不动 |
| 交付 | 保存设计、diff、解析命令与错误、资源及现场；提交bolt-v4 |

## 1. 开关设计与读取范围

[先行设计](../../tools/bolt/results/ps5-final-109-20261116/switch-design.md)在产品编辑之前保存。
读取a061f4e4及父提交61ef5d31的完整llvm.spec、原Part1的spec差异，
[Codex评审](../../tools/bolt/results/review-ps5/codex-review.md)及
[Claude Code评审](../../tools/bolt/results/review-ps5/claude-code-review.md)，
以及helper进程组管理、原测试驱动和已通过的RPM解析工具配置。

Part1全部spec改动：LLVM_LINK_LLVM_DYLIB和CLANG_LINK_CLANG_DYLIB由OFF改ON；
新增TIZEN_HYBRID_LINK=ON、BUILD_SHARED_LIBS=OFF、LLVM_TOOL_LLVM_DRIVER_BUILD=OFF；
构建后驱动NEEDED断言、readelf用途注释。没有Part1的%files或%install清单变化。
父提交没有后三参数，设计关闭时省略它们，保留父提交的两个OFF；
原有LLVM_BUILD_LLVM_DYLIB和CLANG_BUILD_CLANG_DYLIB仍ON。

设计的总开关llvm_speedup和单项hybrid_link均默认开；clang_bolt沿用架构默认。
总开关关时两个有效宏都关，Part3/4不受影响；单独关hybrid_link时BOLT仍开。
依据：父链接方式也让clang静态链接组件，BOLT自身仍强制组件链接，
helper没有要求混合链接开启；这只是源码接入判断，实际组合和产物尚未验证。
安装的AddLLVM.cmake/AddClang.cmake文本仍不同，不声称关闭开关能恢复整个父tree或全部包。

## 2. 未提交实现与R1

[完整diff](../../tools/bolt/results/ps5-final-109-20261116/implementation.diff)仅包含两文件。
新工作树：/home/linhao/Toolchain/development/llvm-optimize/temp/ps5-final-109-20261116/source，
HEAD仍a061f4e4，保留未提交的两文件修改；原105工作树不动。

R1草案在rc==0后调用wait_group_exit(pid,10)，超时存活组错误转换为指定
COMMAND_ERROR并走原kill/wait/reap；其他/proc错误继续保留原诊断。
成功确认后先清_ACTIVE_GROUP再reap。只新增要求的spawn不变量英文注释，
未改H1–H5/N1或转换器。因更早的展开门禁失败，R1没有运行测试，不能称修复已完成。

## 3. 展开失败原文及只读原因核对

```text
error: parse error in expression
error: /home/linhao/Toolchain/development/llvm-optimize/temp/ps5-final-109-20261116/source/packaging/llvm.spec:81: bad %if condition
```

[失败条件](../../tools/bolt/results/ps5-final-109-20261116/failed-condition.txt)：
新增llvm_hybrid_enabled/llvm_bolt_enabled通过expr宏合成；第81行使用后者作为%if。
平台工具为既有Tizen根中通过自身loader运行的RPM 4.14.1。
只读能力核对输出如下（没有重跑产品门禁）：

```text
RPM version 4.14.1
--eval '%{expr:1 && 1}' 的输出仍是：
%{expr:1 && 1}
```

即该RPM未展开expr宏，导致%if接收到非法表达式。
[工具与参数原文](../../tools/bolt/results/ps5-final-109-20261116/rpm-capability-readonly.json)、
[解析脚本](../../tools/bolt/results/ps5-final-109-20261116/parse_switches.py)、
[STOP](../../tools/bolt/results/ps5-final-109-20261116/STOP.txt)。
脚本在第一份候选展开时立即退出，后续五项/组合比较均未执行。
没有使用准备错误修正机会来放宽或重跑这个产品失败。

## 4. 回归材料与延后清单

用户提供的两个探针目录均存在，已只读确认及阅读说明，尚未复制、适配或运行：
- /tmp/claude-1000/-home-linhao-Toolchain-development-llvm-optimize/5e8aa240-5caa-4416-a0c4-218f8c1eb336/scratchpad/r13/probe/
- /tmp/codex-review-ps5-05g9bu2m/

按PM D3延后且未改：嵌套信号R2；SystemExit/KeyboardInterrupt重新抛出前记录cleanup错误。
567既有项不能沿用为本轮通过，R1四类场景、信号发布窗口、Popen失败、
SIGCHLD四类状态和评审探针均待运行。未创建累计候选提交、未改提交说明或Q6/H1/H2最终回复。
没有访问QB/Gerrit评论API，没有构建RPM或LLVM目标，没有推refs/for或sandbox。
仅只读ls-remote证明sandbox仍a061f4e4。

## 5. 资源与交付

串行systemd用户服务4GiB、swap0、CPU200%、Nice19、IO idle，
MemAvailable低于6GiB停止自身的看门狗已启用，现场未触发；没有OOM。
[资源原文](../../tools/bolt/results/ps5-final-109-20261116/resources.json)、
[结束行](../../tools/bolt/results/ps5-final-109-20261116/ended.txt)、
[全部证据索引](../../tools/bolt/results/ps5-final-109-20261116/RAW_LINKS.md)。

本次只读核对失败原因后停止，没有修正产品、没有重跑。

## 6. 109号续：RPM兼容块已替换，第二次准备错误STOP

PM授权把expr定义替换为明确的0/1派生宏块；已逐字采用，其余产品位置不改。
[授权替换diff](../../tools/bolt/results/ps5-final-109-20261116/resume/rpm414-authorized-fix.diff)、
[八处使用点的x86_64条件核对](../../tools/bolt/results/ps5-final-109-20261116/resume/effective-macro-guards.json)。
设计不变：总开关、两个独立单项，Part3/4不受影响。

默认x86_64候选已能被RPM解析，首次比较仅显示开头新增12个空行，
对应2个bcond与10行派生宏块。原比较脚本未实现PM授权的宏块例外，因此使用本次一次准备修正：
仅拟匹配12个新增前导换行，之后仍逐字节比较；不做全局空白归一化。
原错误与修正diff均保存，新结果写parse-rerun，没有覆盖parse中的首轮结果。

但修正脚本把换行写成了字面反斜杠+n，第二次比较再次误报相同的12个空行。
这是我的第二次准备错误，不是新产品差异。按PM规则立即STOP，未修正、未重跑。
[错误代码与原文](../../tools/bolt/results/ps5-final-109-20261116/resume/second-preparation-STOP.txt)、
[准备修正diff](../../tools/bolt/results/ps5-final-109-20261116/resume/preparation-fix.diff)。

当前状态：默认展开比较未完成；ARM、关闭总开关与父cmake参数比较、单项组合、五项解析、
567项+R1+评审回归均未完成/未运行（本续跑unittest 0项）。未生成新LLVM提交，
原a061f4e4工作树未改，新独立工作树保留未提交修改；未推sandbox，未更新回复文件。
只读远端结果见sandbox-readonly.stdout，仍a061f4e415a895412516ffe076084f407f2d70a8。
没有Gerrit写入、构建、QB访问或对另一项目的操作。只保全现场和交付停止报告。
