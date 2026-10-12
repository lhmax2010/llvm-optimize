# 03 BOLT v4 strip策略轻实验

日期：2026-10-12（Asia/Shanghai）。证据目录E=`/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013`；原始日志/副本/脚本只在E内。**推荐llvm-strip --strip-debug处理BOLT clang，以clang固定路径组包装实际brp；无DWARF的clang必须确认find-debuginfo跳过。没有完整RPM验收，也没有新的BOLT重写。**

## 1. 输入与执行环境

BOLT v2原件218881120B，SHA f26b65625897189bd38ae02eb8b4cf5854ada84c08be9be3943f241dea647637；relocs原件3560474952B，SHA6bfc85a8cce9952c4bcbea1a4ea169fb6199c379c18527df7d349f375e52caaf；RPM clang基线139929464B，SHA3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c。完整绝对路径/SHA见02_inventory；所有操作都是真正复制后的文件，不硬链接原件。

使用历史R1的GNU strip/objcopy2.43、eu-strip0.189和LLVM22.1.8 llvm-strip；工具SHA见盘点。本轮版本实查保存在strip/v2-safe-rpm-chain/tool-version-*.stdout，不用宿主不同版本冒充Tizen处理器。根内工具只通过宿主绝对路径和显式loader/library-path读取并执行于E，没有chroot、进入根执行、挂载或根内写入。clang两边均用宿主/lib64/ld-linux-x86-64.so.2和相同历史libxml2目录；没有直接运行ARM ELF或触发binfmt。

每项独立systemd user scope，MemoryMax2147483648B、MemorySwapMax0、nice19/ionice3；串行，启动MemAvailable≥8GiB，采样0.5s，观察低于3GiB就杀本项全部进程。预注册的唯一重写预算6GiB/准入10GiB因前置失败没有启用。父控制器记录unit/argv/真实rc与memory.current/peak/events；结果PASS指**记录流程完成**，不代表副本产品通过，产品看下表version/对象结果。

微型C固定为：

```c
unsigned bolt_probe(unsigned x, unsigned y) { return (x * 33u) ^ (y + (x >> 3)); }
int bolt_branch(int x) { return x < 0 ? -x : x * 7 + 1; }
```

依次--target=armv7l-tizen-linux-gnueabi、aarch64-tizen-linux-gnu、x86_64-tizen-linux-gnu，均-c -O2；无headers。所有变体同一个源/cwd/输出路径，再保存对象。基线三对象SHA分别0ddbf6866ac0bf4a472f5c4092765d50a50cef0c8db461cea1c8bed7feb335ca（832B）、ffd324721c939a3d06825482154fdaf2c5f23aa342bdcf807cf49c78b8dd6407（1128B）、2382019e2ccb1e240af2d93e23f6d4e2b37ffd11cededba033cb16559fb3fefe（1048B）。未做性能测量，不执行生成对象。

## 2. 完整结果矩阵

LOAD标志顺序：普通4段为R/RX/RW/RW；BOLT5段为R/RX/RW/RW/RX。表中“全”指原有.bolt.org.*、.text.cold与.note.bolt_info名称仍在；“部分”指note丢失。节区名称在不等于可执行，故必须查版本及三目标对象。失败编译没有可比较对象，列为失败而不是字节不同。OOM项结构与大小未认证，不把遗留未处理副本大小写成处理结果。

| 输入与处理 | 处理rc | 能运行（version rc） | LOAD数/标志 | BOLT节区 | ARM/A64/x86完整.o | 字节 |
|---|---:|---|---|---|---|---:|
| RPM基线 | 0 | 是（0） | 4/R/RX/RW/RW | 无（非BOLT） | PASS/PASS/PASS | 139929464 |
| v2未经处理 | 0 | 是（0） | 5/R/RX/RW/RW/RX | 全 | PASS/PASS/PASS | 218881120 |
| v2 GNU strip默认 | 0 | 否（SIGSEGV/-11） | 5/R/RX/RW/RW/RX | 全 | 失败/失败/失败 | 187256328 |
| v2 GNU strip --strip-debug | 0 | 否（SIGSEGV/-11） | 5/R/RX/RW/RW/RX | 全 | 失败/失败/失败 | 218297104 |
| v2 eu-strip --remove-comment -f debugfile | 0 | 否（127） | 0/— | 全 | 失败/失败/失败 | 183223936 |
| v2 llvm-strip --strip-debug | 0 | 是（0） | 5/R/RX/RW/RW/RX | 全 | PASS/PASS/PASS | 218879608 |
| v2 llvm-strip --strip-all | 0 | 是（0） | 5/R/RX/RW/RW/RX | 部分，note丢失 | PASS/PASS/PASS | 183223048 |
| v2 GNU objcopy --strip-debug | 0 | 否（SIGSEGV/-11） | 5/R/RX/RW/RW/RX | 全 | 失败/失败/失败 | 218297104 |
| v2 实际find-debuginfo（正常路径） | 0 | 是（0） | 5/R/RX/RW/RW/RX | 全 | PASS/PASS/PASS | 218881120 |
| v2 LLVM debug-strip→find-debuginfo→clang专用brp | 0 | 是（0） | 5/R/RX/RW/RW/RX | 全 | PASS/PASS/PASS | 218879608 |
| relocs GNU strip默认 | 0 | 是（0） | 4/R/RX/RW/RW | 无（非BOLT） | PASS/PASS/PASS | 144543960 |
| relocs GNU strip --strip-debug | 0 | 是（0） | 4/R/RX/RW/RW | 无（非BOLT） | PASS/PASS/PASS | 226730408 |
| relocs eu-strip --remove-comment -f debugfile | OOM | OOM，未测 | UNKNOWN/— | UNKNOWN | 未测 | UNKNOWN |
| relocs llvm-strip --strip-debug | OOM | OOM，未测 | UNKNOWN/— | UNKNOWN | 未测 | UNKNOWN |
| relocs llvm-strip --strip-all | OOM | OOM，未测 | UNKNOWN/— | UNKNOWN | 未测 | UNKNOWN |
| relocs GNU objcopy --strip-debug | 0 | 是（0） | 4/R/RX/RW/RW | 无（非BOLT） | PASS/PASS/PASS | 226730408 |

独立副本逐项证据：E/strip/<表中name>/result.json、commands.jsonl、segments/sections/dynamic.stdout、version/compile-*.stdout/stderr及对象；汇总strip-results.json。完整LOAD偏移/地址/flags保存在segments.stdout，不能只靠段数量相同断言结构完整。

结论限定于本输入和工具：GNU两种strip及GNU objcopy处理BOLT后均SIGSEGV，虽有5LOAD和note；eu-strip实际RPM参数返回0却LOAD0，loader退出127。对普通relocs GNU对应路径可运行且三目标一致，证明风险与BOLT布局相关，不能全局宣称GNU strip不可用。LLVM debug-strip保留note、219MB上下；LLVM all-strip能运行且183MB，但note丢失，不是首选。

## 3. find-debuginfo实际处理与误选反例

供应商脚本按原文复制，SHA与R1一致；它自身是既有Bash脚本，未改写或声称改成POSIX。我们新写的wrapper均#!/bin/sh，并以dash语法检查。辅助debugedit及PATH工具wrapper通过原根loader调用，行为/参数不改；不设置全包strip-disable。

实际参数沿用历史完整RPM日志：--build-id-seed 22.1.8-1 --unique-debug-src-base llvm-22.1.8-1.x86_64 -S debugsourcefiles.list；今晚为串行改-j1（历史-j4）。RPM_BUILD_ROOT/BUILD_DIR与TMPDIR都在E，STRIP_DEFAULT_PACKAGE=elfutils。eu-strip候选参数据脚本strip_to_debug为--remove-comment -f debugfile，未添加未启用的-g/-r/-m。

没有按文件路径排除的原生API：-p/-l分配输出列表，不是exclude；_rpm_strip_disable/--strip-disable全包级。实际可利用的是**无debug节区时选择器跳过**，不把它叫作路径排除API。

首次试验路径包含“v2-find-debuginfo”：objdump -h会先输出绝对文件名，正则(debug[.a-z_]*|gnu.version)连路径中的debug也匹配，误选无DWARF clang→debugedit/eu-strip→LOAD0。处理rc0、version127，183223936B。失败现场strip/v2-find-debuginfo完整保留；原v2 sections证明没有.debug_*；fd-path-diagnosis.json记录根因。

复验目标置于strip/rpm-case-v2-fd-pathfixed/usr/bin/clang-22，不含debug字符串：原脚本提示“/usr/bin/clang-22 is already stripped!”、elfbins.list为空、SHA逐字不变、三个目标PASS。LLVM预debug-strip后同样运行实际find-debuginfo和brp-strip的组合也PASS；strip/v2-safe-rpm-chain/result.json记录fd跳过、SHA不变和post_brp结构/对象。完整RPM仍未打包验证，新根宏也未取到，不能用这个副本实验宣布RPM生产链闭合。

## 4. clang包装器与别名实验

safe-rpm-chain用原brp-strip脚本，仅精确clang路径透传至llvm-strip（实际-g），其他路径仍默认GNU；没有改PS2静态归档处理。

进一步路线/alias试验v2-wrapper-audit增加一个硬链接clang-hard、软链接clang++和普通去debug relocs clang。首次按运行时inode识别组：主clang经llvm-strip替换inode，clang-hard随后被误路由GNU；hardlink_same_inode=false，断言失败（scope rc1）。这是**产品alias缺陷证据**，不是通过。主clang和普通对照三目标都PASS仍不能掩盖失败组；原routes.log/result保留。

修正候选v2-wrapper-audit-fixed：预先冻结clang-22与clang-hard路径，两者都走LLVM，ordinary-clang仍GNU；逐个处理后先比较两clang文件SHA一致，再重建硬链接。路线日志实际为LLVM/GNU/LLVM，三个目标的主clang及普通对照全部PASS，group_content_identical=true、hardlink_same_inode=true，scope rc0。此轻实验说明实现必须预登记路径组或先规范软别名，不能处理后动态按主inode发现旧alias；生产escape/路径组manifest和所有实际triple别名仍待补丁验证。

## 5. OOM与跳过项

| 项 | 结果/证据 | 后续处理 |
|---|---|---|
| relocs llvm-strip --strip-debug | 2GiB cap达到；systemd Result=oom-kill，外层rc-15；未形成认证剥离输入 | 不提高cap、不重试该输入；e主链缺前提 |
| relocs eu-strip RPM参数 | 2GiB scope OOM，Result=oom-kill，rc-15 | 保留副本/日志，不做虚假结构存活结论 |
| relocs llvm-strip --strip-all | 同上 | 保留副本/日志 |
| e：LLVM预剥离后唯一BOLT重写 | SKIP_PRESTRIP_OOM | **今晚实际llvm-bolt调用0次**，不拿其他预剥离方式替换既定实验 |
| e输出的a–d及实际find-debuginfo | 随e跳过七种处理 | 没有e输出，不能用历史v2替代宣称通过 |
| f：原生按文件排除API | 未发现，因此无此API可验证 | 已验证选择器跳过及clang专用brp方案，原生exclude仍不存在 |

OOM不是宿主MemAvailable<3GiB中止；准入全部≥8GiB，没有等5分钟的需要。memory.peak包含页缓存，达到2GiB只说明当前scope预算不足，不证明llvm-strip匿名RSS下界=2GiB；OOM前末次0.5s采样可能仍显示oom0，直接systemd Result提供终止事实。没有越过cap或把OOM当成功。所有scope结束后cgroup为空/消失，失败unit保留Result，不reset-failed抹掉证据；不向归档任务/锁进程发信号。

## 6. 原始证据索引与可复核边界

| 位置（相对E） | 内容 |
|---|---|
| run_scope.py / scope_child.py | 独立cgroup、准入、nice/ionice、0.5s采样、紧急终止、回收逻辑 |
| strip_stage.py / *-stage.py / run_strip.py / run_relocs.py | 精确处理/副本/三目标验证脚本与串行计划 |
| strip-plan.json / strip-driver.log / relocs-driver.log / strip-results.json | 预注册主矩阵、串行真实退出与汇总 |
| *-scope/command.json、child-env.json、admission.jsonl、samples.jsonl、result.json | 精确scope argv、实际nice19/ionice idle、入口与memory指标 |
| relocs-llvm-debug-scope/result.json、其他OOM unit-exit.txt | systemd OOM事实与回收 |
| strip/*/result.json、commands.jsonl及readelf/version/compile文件 | 每副本结构、SHA、三对象与实际退出码 |
| fd-path-diagnosis.json；strip/v2-find-debuginfo与v2-fd-pathfixed | 错误路径/修正路径两个真实行为 |
| strip/v2-wrapper-audit及v2-wrapper-audit-fixed | alias失败与修正验证，GNU普通对照 |
| original-preservation.json / posix-syntax-check.json | 收尾原件SHA复核及新shell的dash -n结果 |

所有中间ELF/profile/对象不提交Git；报告没有性能测量与“其他RPM已不退化”声明。推荐方案仍须周三新树上预剥离/重写和周四完整RPM/90对/accel验证，门禁不通过则不发BOLT试验包。
