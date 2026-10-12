# 47 第三轮评审修订与第四轮材料

日期：2026-10-12（Asia/Shanghai）。开场提交 `bda33ec60e694aeb92e71ac0444901350567a8ba`。

**收尾状态：STOP_HELPER_RETRY_EXHAUSTED。第零至第五步、四次全量复验均完成；第六步ARM32根内小试的辅助采样检查第二次失败，按用户规则停止。只读诊断见§7.2：两个原生clang实际均受4GiB软/硬AS限制，三档产物与离线结果相同，但本轮根内整体验收不记PASS。AArch64根内小试、两根64MiB负例与第七步补丁再生成未执行；第八步停止材料已完成。**

## 0. 范围、证据与资源规则

W=`/home/linhao/Toolchain/development/llvm-optimize`；本轮 E=`W/temp/review-round4-20261012`，下述 temp 证据仅在本机。依用户裁决：轻量阶段准入6 GiB，全量转换10 GiB；不足每5分钟复查、最多60分钟。运行中scope 18 GiB、swap0、nice15/ionice3、30秒采样，宿主可用低于2 GiB即中止。Commands、356627 spec、W/llvm与配置不改；不做完整RPM构建、不推Gerrit。本轮只做四种小spec组合；另依辅助脚本条款对夹具修正重跑一次，实际调用数见§5。

宿主 `mmap_min_addr` 沿用先前GBS设置；需要恢复时用户执行 `sudo sysctl -w vm.mmap_min_addr=65536`，重启也会恢复。本轮仅按各阶段需要临时挂载/proc，并在finally卸载。

本报告路径定义：

- R32=`/var/tmp/llvm-optimize-arm-c1-20261010/gbs-libraries-armv7l/local/BUILD-ROOTS/scratch.armv7l.0`。
- R64=`/var/tmp/llvm-optimize-arm-tls-aarch64-20261010/gbs-aarch64/local/BUILD-ROOTS/scratch.aarch64.0`。
- Rnew=`W/temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0`；各根B=`R/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build`。
- E5=`W/temp/arm-archive-stage1-20261010`，x86输入在`E5/x86-input`；ARM32输入为`W/temp/arm-archive-standard-build-20261010/armv7l-input`，AArch64输入为`W/temp/arm-archive-tls-thumb-20261010/aarch64-input`。
- 宿主ARM转换使用对应输入证据目录中的已登记`*-tool-wrappers/{clang-22,llvm-dis,llvm-nm}`；根内小试使用`/emul/usr/bin/{clang-22,llvm-dis,llvm-nm}`及`/emul/usr/bin/bash`，不经包装脚本。

## 1. 第零步完整性

| 项目 | 结果 | E内证据 |
|---|---|---|
| 截止点 | reflog 2026-10-12 19:35:32+08；本地HEAD/origin/main/远端main均bda33ec，无新提交 | integrity/main-*.stdout、remote-head.stdout |
| 主仓库全量status | 4,995,871行；非忽略差异只有用户gbs_llvm.conf | integrity/main-status-all.stdout |
| W/llvm | HEAD f111162e94aa48ed367c9d2c039456c70e7160ae；sandbox/fangyu.he/llvm_optmize；仅原三处并发改动 | integrity/llvm-*.stdout |
| 保护文件 | 69个HEAD blob全同；spec SHA95887b2d…、配置28f1caf9…均相符 | integrity/head-blob-check.json、input-integrity.jsonl |
| 修改时间全集 | 104条全部归因，未知0；15个权限盲目录免密只读补扫，新增0 | metadata-attribution.json、privileged-newer-command.json |
| 输入内容 | x86 225+ARM32 210+AArch64 212=647档；工具/代码/补丁等合计672项SHA PASS | input-integrity-result.json、input-integrity.jsonl |

归因类别：本轮锁/证据52、Git目录元数据15、上一收尾提交对象13、Codex自动树/refs15、上一提交/推送元数据9。自动树与HEAD的唯一差异是已登记配置，其blob SHA28f1caf9…一致。没有回滚或修复任何历史文件。本阶段未动用辅助脚本重试条款。原始find exit1仅来自15个权限盲目录，已补扫补齐；不把不完整扫描本身记为PASS。（证据：metadata-gate.json、git-object-attribution.json、codex-ref-attribution.json。）

## 2. 本轮实际资源

| 阶段（E下scope目录） | 准入GiB | 启动可用GiB | scope峰GiB | scope wall秒 | exit |
|---|---:|---:|---:|---:|---:|
| aarch64-scope | 10 | 14.278065 | 10.016487 | 1649.035 | 0 |
| armv7l-root-small-retry-scope | 6 | 14.302948 | 0.714195 | 10.220 | 1 |
| armv7l-root-small-scope | 6 | 14.264698 | 0.707218 | 10.229 | 1 |
| armv7l-scope | 10 | 14.282635 | 7.209900 | 1854.712 | 0 |
| facts-scope | 6 | 14.179691 | 0.664886 | 38.379 | 0 |
| final-integrity-scope | 6 | 14.341805 | 0.024136 | 2.117 | 0 |
| host-tests-scope | 6 | 14.063240 | 0.517220 | 56.525 | 0 |
| input-integrity-scope | 6 | 13.937710 | 1.200821 | 153.068 | 0 |
| integrity-scope | 6 | 9.839542 | 5.730644 | 1042.682 | 0 |
| metadata-completion-scope | 6 | 10.701515 | 0.016010 | 2.166 | 0 |
| root-tests-scope | 6 | 14.068626 | 0.306477 | 40.482 | 0 |
| small-spec-retry-scope | 6 | 14.059113 | 0.040215 | 2.116 | 0 |
| small-spec-scope | 6 | 14.133301 | 0.135212 | 6.118 | 1 |
| x86-candidate-scope | 10 | 14.267361 | 3.712425 | 1804.212 | 0 |
| x86-production-scope | 10 | 14.097652 | 2.642155 | 1853.821 | 0 |

15个阶段均一次满足准入，无等待；所有memory.events的max/oom/oom_kill均0，未触发宿主2GiB保护。scope峰包含文件缓存，scope wall包含驱动、校验和退出回收，不能与Source转换wall混同。全部采样器与日志线程已回收；三次exit1分别是小spec夹具一次和根内辅助检查两次，原因见§4、§7.2。证据：E/completed-stage-resources.json及每个scope的admission.json、samples.jsonl、memory-summary.json、time-v.txt。

## 3. 第一步事实核查

### 3.1 发布模式与当前认证边界

三根展开`%{defined _toolchain}|%{_toolchain}`均为`1|clang`。W/gbs_llvm.conf:6,9,12只列仓库，不直接定义宏；GBS取得的E9=`temp/arm-archive-stage1-c-newrepo-20261010/buildconfig-from-W.conf`:161原文为`%_toolchain %{?_toolchain_override}%{!?_toolchain_override:clang}`，SHA1e7610b6…；其来源链已由docs/13§3、docs/40§9核查为Unified配置。根内`home/abuild/.rpmmacros`对应行为x86:63、ARM32/A64:65。目标cb679968 spec:11–16因此进入`llvm_release_build=0`分支；178–186的移除调试选项sed不执行。（本轮facts-result.json/macro_files；三份*-toolchain-macro.stdout；target-spec.stdout。）

历史x86构建采用此带调试分支，docs/13及docs/35的日志同时有带`-gdwarf-4`的CMake调用、find-debuginfo与9个debuginfo RPM写出；docs/30/34/38沿用同配方、22包结果及debug分支记录，不把它们说成发布模式认证。两ARM只执行-bc，日志CMake flags保留`-g2 -gdwarf-4`；没有运行%install或生成debuginfo RPM，不能由“未产包”推断发布模式。具体日志路径、逐行摘录与SHA见facts-result.json/historical_logs；历史打包记录见docs/13§8、docs/30、docs/34–38。

静态模拟使用cb679968:180原样CFLAGS sed表达式，经`/usr/bin/sed`作用于每条完整记录命令，再由本轮开场分类函数分类；不转换任何成员。结果：

| 架构 | 全部记录命令 | PASS | FAIL | 唯一失败原因 |
|---|---:|---:|---:|---|
| x86_64 | 3853 | 0 | 3853 | `uncertified last DWARF option: missing` |
| armv7l | 3683 | 0 | 3683 | `uncertified last DWARF option: missing` |
| aarch64 | 3699 | 0 | 3699 | `uncertified last DWARF option: missing` |

**发布模式未被当前认证策略覆盖。** 删除调试参数后缺少强制的-gdwarf-4；这是纯文本模拟结论，不是本轮构建失败。按PM约束只记录，不改Source策略，后续如何支持发布模式待PM裁决。（证据：三份*-release-input.txt/output.txt/simulation.json；facts.py；target-spec.stdout。）

### 3.2 原生读取与工具身份

两根都执行用户给定命令：目标`/usr/bin/prlimit --as=4294967296 -- /emul/usr/bin/bash --noprofile --norc -p -c ...`，使用bash内建read/printf读取/proc/self/limits。原始读回均为：

```text
Max address space         unlimited            unlimited            bytes
```

exit均0。这证实此路径的4GiB限制没有传到原生bash，不能把旧失效归因于“只读到了错误的模拟cat”。本轮探针只读，不修改Commands或限制策略。（证据：armv7l-native-readback.stdout、aarch64-native-readback.stdout、facts-commands.json。）

| 根 | bash SHA256 | RPM归属 | ELF/解释器 |
|---|---|---|---|
| armv7l | `a0f9c3ac42deef107e32940003fb7373ab3d697dcfccb49734286e562cbc9000` | `qemu-accel-x86_64-armv7l-0.4-1.1.armv7l` | ELF64小端machine62；`/emul/usr/lib64/ld-linux-x86-64.so.2` |
| aarch64 | `4cfa54c74219fb7294ed8ce1d91909b36c52e6def59798d12d61ea3a736a5780` | `qemu-accel-x86_64-aarch64-0.4-1.1.aarch64` | ELF64小端machine62；`/emul/usr/lib64/ld-linux-x86-64.so.2` |

两根`home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/CMakeCache.txt`均存在；第六步根内小试不因缺构建目录而跳过。R32/R64沿用docs/46§0路径；完整绝对路径/Cache SHA在facts-result.json。/proc分别临时挂载并finally卸载，前/中/后mountinfo全部保存。（证据：*-facts-mount-*.txt，*-bash-{file,elf-header,elf-program,owner}.stdout，facts-result.json。）

## 4. Source与测试修订

X1合并汇编选项拒绝消息；X2/X4补主版本与module asm检查注释；X3将ELF表级边界检查移出条目循环。ARM A1–A7增加组合式原生bash限制启动器、严格读回探针、关键字专用传参、原生工具machine62验证/显式包装脚本许可、保留多重错误原因、统一x86成员结果结构、要求target存在且一致。Commands两份与开场逐字相同，Python3.9语法检查通过；本轮两环境测试与固定输入四次全量复验结果见§5、§7。这里的语法检查不等于已在Python3.9解释器运行全套测试。（E/source-revision-static.json、final-integrity.json。）

- `llvm_static_archives_source.py` SHA `7c83e822c333f05ddfce998918e79c542926203d26cf58750291f492d6e9dcaf`；完整diff：[docs/47_x86_source_round4.diff](47_x86_source_round4.diff)。
- `llvm_static_archives_arm_trial.py` SHA `3cdaecebf45ab213d92d212a874ef978a825bfc3f171183963599fe9bd4f5bb3`；完整diff：[docs/47_arm_source_round4.diff](47_arm_source_round4.diff)。

新增`tools/test_archive_review_round4.py`覆盖本轮X1/X3/A1–A7；旧ARM测试只更新被新政策取代的预期（旧AS放行删除、wrapper显式许可、target强制、install签名AST排除与实际调用补验）。原测试保留；宿主134/134 PASS（55.282秒）；ARM32根内134项中130 PASS、3项环境不适用、1项已知QEMU AS发现，无新增失败。

小spec首次发现夹具未显式展开`%debug_package`，标为on的组合实际未启用debug；根内宏`usr/lib/rpm/macros:229–235`与`home/abuild/.rpmmacros:124–129`说明启用需要宏展开/后端注入。只在临时spec增加`%debug_package`，off组合仍定义nil；原实际命令判据完全不变。本步骤动用一次辅助脚本修正重跑授权；原三组合日志与失败保留，修正全文E/small-spec-helper-fix.diff、诊断E/small-spec-helper-diagnosis.json。重跑四组合全部exit0；删除行版本debug开启不执行brp-strip、关闭执行/bin/strip，归档均以/usr/bin/llvm-strip单独命令执行，两个判据PASS。保留行版本实际行为同样符合此分派，仅作为观察结果。证据E/small-spec-retry/small-spec-results.json与四份stdout/stderr；没有推断保留行必然失败。

小spec修正的完整diff与根内监测唯一一次修正的完整diff一并外置：[docs/47_auxiliary_drivers.diff](47_auxiliary_drivers.diff)。前者重跑PASS；后者重跑仍FAIL，已停止而未再修改。Source没有因这两个辅助缺陷更改。

## 5. 本轮测试与小spec实测

宿主测试134项全部PASS，相对上一轮116项增加18项；0失败/错误/跳过。ARM32根内同样134项：130 PASS，以下4项按PM原裁决单列，其他均通过：

| 测试 | 根内分类 | 原因 |
|---|---|---|
| test_actual_limits_and_monitor_cleanup | 环境不适用 | 实验辅助模块需要/usr/bin/time |
| test_failure_stops_following_commands | 环境不适用 | 同上 |
| test_sections_symbols_visibility_and_relocations | 环境不适用 | x86 as --64夹具 |
| test_limits_accounting_and_no_external_time | 已知环境发现 | 未修改的Commands经QEMU设置AS后读回unlimited |

新启动器自身的读回/失败125/超时SIGKILL回收测试在两环境都PASS；没有把原Commands的已知限制问题改成PASS。根内解释器：`3.14.2 (main, Oct  1 2026, 21:46:23) [Clang 22.1.8 ]`。证据E/host-tests-result.json、root-suite-raw.json、root-suite-classified.json及root-commands.json；/proc已卸载。

| 小spec | debug | exit | 归档strip参数 | 普通brp-strip | 判定 |
|---|---|---:|---|---|---|
| 保留宏内注释 | on | 0 | /usr/bin/llvm-strip | 未执行 | 仅观察 |
| 保留宏内注释 | off | 0 | /usr/bin/llvm-strip | /bin/strip | 仅观察 |
| 删除宏内注释 | on | 0 | /usr/bin/llvm-strip | 未执行 | PASS |
| 删除宏内注释 | off | 0 | /usr/bin/llvm-strip | /bin/strip | PASS |

on两例均实际产出debuginfo/debugsource RPM，均执行find-debuginfo；不是仅设置一个测试布尔值。完整临时spec和set-x原文在E/small-spec-retry；本轮没有LLVM完整RPM构建。首次辅助夹具漏启debug及唯一一次修正见§4，不覆盖失败原始记录。总计7次小spec rpmbuild调用：首次3次后停止，修正后4次；没有LLVM构建。

## 6. 修订理由、来源与不采纳项

来源统一为本任务PM对Claude Code、Codex、Kimi Code第三轮意见的合并裁决；任务未提供每条意见与单一评审方的映射，本报告不补造该映射。下表的编号对应原裁决；实现全文见§4两份diff，行为证据见134项测试逐项结果。

| 编号 | 处理与理由 |
|---|---|
| X1 | `-Wa,`/`-Xassembler`同分支、同一固定拒绝消息；不增加可接受选项 |
| X2 | 注明x86只锁LLVM主版本；ARM有字面量特征串才锁完整版本 |
| X3 | 节表/stride/link/info/entsize在遍历条目前一次验证，错误带x86_64；循环内保留符号索引越界检查；合法输入不改PIC策略 |
| X4 | 明示x86 nm名称检查与ARM严格ELF符号检查的不同认证范围，不声称x86已获得ARM强度 |
| A1 | 组合包装Commands，仅三工具与探针经原生bash；软/硬AS、core及读回均失败关闭；记录payload与bash SHA |
| A2 | 两种探针均要求soft=hard=requested；无确认放行参数、无unlimited旁路 |
| A3 | 删除全局安装上下文；install/convert关键字专用参数逐层传递；x86拒绝ARM选项且内部不传ARM关键字 |
| A4 | 原生ELF须ELF64小端machine62；包装脚本仅显式许可并记录SHA/前4KiB；与启动器互斥 |
| A5 | 工具缺失等原始原因保留，再附完整版本不符说明，避免错误被覆盖 |
| A6 | x86结果的module_asm_symbol置于成员层，与生产Source一致 |
| A7 | --target必须存在、所有值相同且已认证；不新增目标 |
| C | 小spec已验证删除宏体停用注释的debug开/关行为；最终补丁未再生成，移除该行、定义上方来源说明和提交说明同步维护/全部静态子包范围仍挂账，不冒充已改候选补丁 |

未采纳项及依据：

1. “原生clang本已受限，旧探针读错路径”：本轮目标prlimit→原生bash也读回unlimited（§3.2），与既有QEMU9.2.3实现/实测一致；不接受该推断。
2. 双链交叉验证探针：由启动器内原生读取代替，设置、读取与exec工具发生在同一原生进程路径；宿主实际捕获两个运行中clang的4GiB软/硬限制，整步辅助门禁仍因第二次脚本失败停止，见§7.2。
3. 把上一提交说明116宿主测试改成112+3+1：不采纳；前者是宿主116全PASS，后者是另一次ARM根内分类。新轮为宿主134全PASS、根内130+3+1（§5）。
4. 新增`BuildRequires: /usr/bin/llvm-strip`：不采纳；LLVM自身依赖可能形成依赖环或提供方选择问题。保留安装期工具检查，验证时记录提供包；本轮不改356627 spec。
5. spec加入`rpm -qf`：只在证据中记录，不进入提交配方。
6. 启动器默认关闭并保留确认放行：不采纳；探针始终强制，删除旁路。宿主明确允许包装脚本仍须限制读回正确，不是允许未受限运行。

## 7. 全量与根内复验，以及停止边界

### 7.1 四次全量复验：PASS

| 本轮路径 | 状态 | 逐项结果 | Source转换wall秒 | 含前置核对总wall秒 |
|---|---|---|---:|---:|
| x86生产Source | PASS | 225档/3864有序成员/完整索引/3853组flags全部与docs/35一致；3处module asm检查通过 | 1783.727 | 1850.353 |
| ARM候选的x86路径 | PASS | 同上，第二次独立执行；3处module asm检查通过 | 1734.587 | 1800.684 |
| armv7l宿主离线 | PASS | 210档/3690成员（3683转换、7原机器码）；全部after SHA与docs/40 §12相同；3683 Thumb门禁PASS，属性差异0 | 1799.965 | 1852.836 |
| aarch64宿主离线 | PASS | 212档/3706成员（3699转换、7原机器码）；全部after SHA与docs/40 §12相同 | 1598.510 | 1646.645 |

两ARM使用已登记包装脚本并显式`--allow-wrapper-tools`，未启用原生启动器；两次探针软/硬AS均精确为4294967296。全库强符号缺失0；允许缺失的W类分别为x86两路径各1920、ARM32 2953、AArch64 1698，其他允许缺失类型未出现。ARM module asm检查分别2/3个成员PASS；不是忽略模块汇编。逐档字节全同符合用户的沿用条件，故本轮没有重跑三套消费者或两种strip，其证据沿用docs/40 §12与docs/44/46。（E/{x86-production,x86-candidate,armv7l,aarch64}-result.json；对应*-conversion/summary.json、逐档after.json和scope采样。）

### 7.2 ARM32根内小试：Source完成，辅助检查第二次失败，整步STOP

输入按含bitcode且原体积最小选择，复制到独立目录；原构建树及离线输入不改。首次目录为R32/home/abuild/review-round4-small-20261012；唯一一次重跑为同级review-round4-small-retry-20261012。两次均使用根内Python3.14.2、三工具直接指向`/emul/usr/bin/{clang-22,llvm-dis,llvm-nm}`，`--native-limit-bash /emul/usr/bin/bash --jobs 4 --address-space-bytes 4294967296`；--build指向本报告§0的B32，输出/evidence与输入都在各自独立目录。完整argv在E/root-small-retry/armv7l-root-small-source-argv.json；命令JSON保留payload及bash SHA。

| 辅助尝试 | 只读定因与处理 | 门禁结果 |
|---|---|---|
| 首次 | 监测器只遍历`/proc/<leader>/task/<leader>/children`，遗漏ThreadPoolExecutor工作线程启动的编译子进程；源程序转换成功，但未捕获运行中clang。`proc_tid_children(5)`第14–25行说明该列表属于指定task；Source转换并发使用工作线程。仅将监测器改为进程PPid树快照，保留5ms采样、原生ELF/`-c`识别及所有数值判据，输出改用新目录 | exit1；按辅助缺陷条款只重跑一次 |
| 唯一重跑 | 捕获两个原生clang；原有断言正则以`bytes$`结束，而内核limits行实际末尾有5个空格，故仍assert失败。软/硬值确实都是4294967296。只读诊断未改Source、Commands或正则 | exit1；同一步第二次失败，停止，未再修正/重跑 |

这两次失败是本任务编写的辅助检查缺陷，不是Source实际返回失败。用户规则仍要求第二次失败结束后续步骤；因此不把只读诊断数据改判为根内整体验收PASS。首次缺陷证据：E/root-helper-readonly-diagnosis.json、proc_tid_children-man.txt、armv7l-root-process-peaks.json；唯一修正全文：E/root-small-helper-fix.diff及[外置附件](47_auxiliary_drivers.diff)。第二次原始FAIL：E/root-small-retry/armv7l-root-small-result.json及armv7l-root-small-retry-scope日志；停止定性：E/stop-diagnosis.json。

重跑时宿主实际读取的两个进程为PID1605460（转换）与1605465（Thumb参考对象），exe均为R32/emul/usr/bin/clang-22，含`-c`。两条原始行均如下（右引号前的空格保留）：

```text
'Max address space         4294967296           4294967296           bytes     '
```

启动器探针也读回soft=hard=4294967296、core软/硬均0。Source CLI exit0、summary PASS；只读补齐比对表如下，证明这三档在本次根内GNU ar/readelf条件下产物字节不变，但不能替代未执行负例及AArch64根内认证。（E/stop-diagnosis.json；root-small-retry/armv7l-root-process-limits.json与保存的summary。）

| 归档（usr/lib/） | 输入字节 | 根内after SHA256（与本轮离线相同） |
|---|---:|---|
| libLLVMABI.a | 25442 | `b42d54db2684fd0d6b5b1ed954bffe33df7c77a4c2b82a1af12b905a236e6f5c` |
| libLLVMExtensions.a | 26526 | `152c6e4b1be5db9d9f1a33ff670af3ac1dd70d4eb1489023bf117f3c14b99108` |
| libLLVMFrontendDirective.a | 51068 | `254ed15ba174a63796c3d786d624ec6a303403d8e195005d64dd7ea090ba4e77` |

根内CLI wall **5.633643秒**；宿主监测Python进程VmHWM **50148 KiB**，根内getrusage自身读数49592 KiB，二者独立列出。scope wall10.220182秒、峰值0.714195GiB；含挂载、身份检查和辅助监测，不作为转换器性能结论。根内readelf实际路径`/usr/bin/readelf`，版本GNU Binutils 2.43，SHA256 `225473b13aca7d036663309478d78e72455aae709aeb6e664a1a4f69676c49d3`；它仍由原Commands运行，未纳入三原生工具包装。（root-small-retry/armv7l-small-readelf-version.stdout、armv7l-root-small-result.json、armv7l-root-process-peaks.json、stop-diagnosis.json。）

| 命令类别（含预检/版本查询） | 次数 | 平均wall秒 | 最大wall秒 |
|---|---:|---:|---:|
| native-probe | 1 | 0.054141 | 0.054141 |
| llvm-nm | 7 | 0.054287 | 0.054549 |
| llvm-dis | 4 | 0.055832 | 0.058128 |
| readelf | 7 | 0.054475 | 0.054912 |
| clang-22 | 7 | 0.055332 | 0.058300 |
| ar | 6 | 0.054559 | 0.055367 |

这些wall含Commands每50ms轮询的计时粒度，不能把约0.05秒直接解释成工具自身或qemu耗时。证据为该次保存的各命令JSON，由E/stop_diagnosis.py只读汇总。未用小样本推断全库qemu总耗时。

### 7.3 未执行项与补丁身份

ARM32的64MiB启动器负例、AArch64根内三小档+libarcher小试及64MiB负例全部**NOT RUN**。两根Cache均存在，未执行原因是上述停止规则，不是环境缺失或两小时超时。没有为通过检查再修辅助正则，没有放宽AS断言。

第七步候选补丁再生成也**NOT RUN**，不存在包含本轮Source的新PS3/PS2及对应apply/tree认证。仓库现有两份候选仍是docs/46版本，以下SHA只用于防止误用，不能作为本轮新增补丁交付：

| 旧候选（保持未改） | SHA256 |
|---|---|
| patches/archive-index-fix/ps3/0001-packaging-fix-llvm-static-devel-with-ThinLTO.patch | `1293f6982c87cfbeefe91aa08e92a7d1b72a129f716417f8c8cee61693c463c6` |
| patches/llvm-strip/ps2/0001-packaging-use-llvm-strip-for-x86_64-archives.patch | `aab2cfd1ad3fb58bfe44cdbdda50bbe67d5343b29a6a6d598408d3bb96620e88` |

PS3目录中的Source也仍是上一轮014fd32f版本，不是本轮tools中的7c83e822。原已上传的两份补丁与生产6bd0546a附件均未变。完整内容仍可从原仓库路径读取；本轮只外置两份Source diff和辅助驱动修正，不生成假的新补丁全文。（E/final-integrity.json；开场及结束SHA；git diff bda33ec -- patches为空。）

## 8. docs/46两条x86路径耗时差异的可证范围

来源：`temp/review-round3-continue-20261012/{x86-production,x86-candidate}-scope/{admission.json,samples.jsonl,memory-summary.json}`；本轮只读汇总E/previous-x86-timing-evidence.json。

| 上轮路径 | 转换wall秒 | 含前置核对总wall秒 | load1最小/中位/最大 | load1>10样本 | 最低宿主可用GiB | cgroup CPU秒 |
|---|---:|---:|---|---:|---:|---:|
| 生产Source | 2792.146 | 3035.233 | 3.90 / 5.865 / 25.50 | 21/100 | 12.139492 | 2766.600333 |
| ARM候选x86路径 | 4673.640 | 5164.360 | 3.39 / 9.13 / 49.98 | 80/169 | 7.212654 | 2772.715127 |

两次准入均一次满足10GiB，无等待；分别于15:42:36、16:33:33启动，采样窗口不同。第二次更长wall伴随更高宿主负载和更低可用内存，cgroup CPU累计接近；这些是观测，不足以把差异定量归因到负载、I/O或Source开销。本轮没有受控性能实验，不据此声称候选路径变慢，也不把准入等待算作转换耗时。

## 9. 后续完整构建验收清单（本轮未执行）

### 9.1 x86完整构建

1. 先补齐停止项并生成最终PS3/PS2；在干净cb679968顺序应用这两个最终候选，钉Source/工具/补丁SHA；确认util-linux依赖解析与llvm-strip版本、RPM归属。
2. 确认%install实际转换而非SKIP。从**完整spec**生成install-post并保存execve追踪：转换在前；每档brp归档strip实用llvm-strip且exit0；debug开启时brp-strip不执行；find-debuginfo与其余后处理照常。
3. 225开发档全检：成员身份/次序、无bitcode、无DWARF、完整符号→成员索引与强符号；45 compiler-rt档逐成员核对可加载节内容、符号属性、重定位和索引。libarcher在llvm-static-devel/libomp-devel双归属内容一致。
4. 非归档文件与**同配方无补丁**基线比较，不用不同配方历史SHA自动豁免；工具二进制不变逐个核查。
5. 宿主七项消费者与Tizen bfd/lld两测试包、ASan/UBSan/profile/builtins运行库探针重跑；GNU ld组无LTO/插件。
6. 独立安装根真实%install重新转换成功；同树再次直接调用Source为SKIP，分开证明，不混淆两种续跑。
7. 至少10个跨子系统成员，用原参数去LTO的直接编译与转换产物比较节区结构、符号绑定/可见性、重定位；不能仅以归档SHA或少量消费者替代。
8. 发布模式模拟缺DWARF已FAIL（§3.1）；PM须先决定认证范围/策略，不能将本轮带调试分支离线结果宣称为发布模式PASS。

### 9.2 ARM第二段打包

1. spec三工具必须指向/emul原生ELF，启用原生限制启动器；根内bash身份、完整工具版本与探针PASS是实施前置。Source目前为评审候选，本轮不改ARM spec、不打包。
2. 两架构都执行真实打包入口，尤其AArch64不得用离线转换代替%install。当前候选预期ARM32 210档、AArch64 212档；共同204档；ARM32另有LLVMARM的AsmParser/CodeGen/Desc/Disassembler/Info/Utils六档，AArch64对应六档再加LLVMExegesisAArch64与libarcher_static.a（E/arm-expected-inventory-difference.json，取自§12原始summary）。仍须按实际安装清单核对及libarcher归属，不能直接套x86225档。
3. 根内GNU ar/readelf、32位Python、临时/proc、超时、磁盘、宏后处理和标准strip均记录；本轮ARM32三小档只有诊断数据（§7.2），AArch64尚未实测；补齐根内门禁后再作为下一阶段预算基线。
4. 若readelf开销不可接受，可另行设计Python解析.ARM.attributes；须逐成员与GNU readelf做A/B属性/Thumb门禁对照，含缺省、畸形、重复属性及正负夹具，认证后才能替换，不能本轮跳过。
5. 根据本轮每类命令均值/最大值、总wall与Python峰值估算全库qemu编排预算，给总量与余量；小样本推算只能用于计划，完整%install实测才闭合。
6. 根内GCC/libstdc++变化时重核module asm白名单、符号状态和生产者选项；不得仅见clang主版本相同就沿用。
7. 两种strip后各自重做索引与消费者，检查TLS动态重定位/运行路径；新RPM上GNU ld无LTO、lld、共享库无TEXTREL、dlopen及GC全部验证。
8. ARM扩展不能改变x86已认证路径；最终Source新SHA须再次全量x86不变性及测试通过。发布模式问题独立待裁决。

## 10. 当前挂账

1. 第六步根内验收停止：当前Source与四次全量回归可供第四轮评审，但ARM32辅助检查第二次失败后不再重跑。后续若另获授权，须补ARM32根内完整门禁、两根64MiB负例及AArch64根内小试，不能据本轮部分数据跳过。
2. 356627 PS3 / 356639 PS2再生成及C项最终注释/提交说明更新未做，旧候选保留；新的apply/tree验证未做。
3. 发布模式全部模拟拒绝，待PM裁决；本轮不改发布认证策略。
4. 第四轮外部评审、最终候选叠加的x86完整构建、ARM第二段实际打包均未完成。只读保护核对见§11；不把小spec或离线测试称为完整LLVM构建验收。

## 11. 保护核对、回收与交付边界

结束只读核对PASS：W/llvm仍f111162e、spec仍95887b2d…，gbs_llvm.conf仍用户登记的28f1caf9…；两原上传补丁与6bd0546a附件未变，docs/25–46未改，现有PS3/PS2及其Source附件仍与开场bda33ec逐字相同。两份Source与本轮测试时记录SHA相同，两份Commands与开场逐字相同。（E/final-integrity.json，final-integrity-scope exit0。）

2026-10-12 23:53:55+08释放两个项目锁，持锁进程exit0；23:54:16核对15个scope均非active、采样器/日志线程已回收，本任务残留进程0，R32/R64/Rnew下挂载0，锁文件0。所有小试均使用副本，未清理历史载荷；Source按自身既有流程删除独立输出中的中间大文件不属于磁盘清理。未重建LLVM、未运行GBS完整打包、未改宿主配置或推Gerrit。（E/lock-released.json、cleanup-final.json、final-mountinfo.txt。）

本轮开场bda33ec后的阶段提交依次为4186e94、5aa1416、3cfb2bc、8a7c8ad、07c058d、074ef62、fb833a4、1ddb25a，均已推送。停止报告与STATUS同一个收尾提交；本提交号由`git log -1 -- docs/47_review_round4_package.md`定位，完成回复提供钉提交号链接。未执行项按§7.3/§10保留，不宣称整个任务PASS。
