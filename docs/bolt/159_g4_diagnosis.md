# 159 · G4 归档转换失败诊断

**归类为 (c) 单进程地址空间不足。** G4 已完成 CMake、Ninja 编译和链接，进入 `%install` 后，归档转换器用构建出的 Clang 22.1.8 将 `usr/lib64/libclangAST.a` 的第 52 号成员（从 0 开始）`Disasm.cpp.o` 从 ThinLTO IR 转为 native ELF。后端的 `Assignment Tracking Analysis` 在 `clang::interp::Function::dump` 上分配失败。子进程受 `RLIMIT_AS=4 GiB` 约束，cgroup 没有 OOM 事件。

## 首个实际错误

成员 stderr 从第一行开始就是：

~~~text
LLVM ERROR: out of memory
Allocation failed
~~~

`llvm-dis` 的退出码为 0。随后 `clang-22 -x ir -O3 -g -gdwarf-4` 在代码生成中报错。Clang 记录 frontend 退出码 134，驱动退出码为 1，整个调用墙钟 49.08 秒，未达 600 秒命令上限。成员峰值 RSS 为 4,123,208 KiB（3.93 GiB）。`prlimit --as=4294967296 --core=0` 原样保存在成员命令回执中。4 GiB 限制加上近上限的 RSS 和 LLVM 分配失败，支持地址空间耗尽的判断。RSS 与虚拟地址空间是不同计量，现有记录未采到失败瞬间的 VmSize。

RPM 总日志 L17538 的最后一个已完成归档为 `libclangAPINotes.a`。L17539 开始打印 traceback，L17559 为 `RuntimeError: cancelled after: command failed`，L17561 是 RPM 对 `%install` 的退出状态。转换器把子进程 stderr 写到成员日志，子进程失败后设置取消标记，主线程只把取消状态写到了 RPM 总日志。

[成员 stderr 原文](../../tools/bolt/results/task159/disasm-member-stderr.txt) · [成员命令与计量](../../tools/bolt/results/task159/disasm-member-command.json) · [IR 参数分类](../../tools/bolt/results/task159/disasm-member-ir-settings.json) · [总日志原文片段](../../tools/bolt/results/task159/g4-failure-context.txt)

## 分类依据

| 候选 | 判断与依据 |
|---|---|
| (a) 配方或 PGO 门禁、助手 | Ninja 门禁扫描 25,940 条边，5,357 条编译边使用 profile，879 条属于运行时，违规 0。构建进入 `%install` 并开始转换。配方中的 4 GiB 单进程上限是本次资源约束。转换器的取消日志掩盖了具体子命令失败。 |
| (b) profile-use 编译或 hash 匹配 | 总日志与成员 stderr 无 profile 不匹配诊断。成员的历史编译命令记录了 profile-use，转换实际 argv 只有 `-x ir` 等重放选项，已按现有规则去掉 profile 文件参数。实际失败栈是调试信息赋值追踪中的内存分配。仅凭现有记录无法量化 PGO 对这一个 IR 成员内存需求的影响。 |
| (c) 资源 | **符合。** cgroup 峰值 14,270,107,648 B，上限 16,009,859,072 B。G4 的 434 次采样中 /home 最低可用 233,490,501,632 B，MemAvailable 最低 14,091,681,792 B。无磁盘耗尽、超时或看门狗触发证据。 |
| (d) 与 PGO 无关的既有问题 | 149-run N2 同一 `%install` 转换阶段通过。N2 将 `libclangAST.a` 的 114 个成员全部转为 native 并安装，结束记录为 `NATIVE_ARCHIVES_END … PASS 225`，随后处理了 `llvm-static-devel` 并完成 RPM 构建。N2 与 G4 的该归档输入 SHA 不同，该对照能确认 N2 通过同一阶段，不能单独判定 G4 的具体 IR 为何需要更多内存。 |

`memory.events` 原文：

~~~text
low 0
high 0
max 0
oom 0
oom_kill 0
oom_group_kill 0
sock_throttled 0
~~~

[阶段标记](../../tools/bolt/results/task159/g4-stage-markers.txt) · [cgroup 记录](../../tools/bolt/results/task159/g4-cgroup-stop.json) · [N2 同阶段原文](../../tools/bolt/results/task159/n2-comparison.txt)

## 最小修复方案与重跑时长

1. 在下一轮获准后，先以同一份 bitcode、同一套转换参数和调试信息做隔离验证。只提高该次转换的 `--address-space-bytes`，建议单 worker 在 6 GiB 试验，若仍为地址空间耗尽再验证 8 GiB。先确认 G4 的 cgroup 和主机余量。现场保留了成员命令、参数与 stderr，清理后成员原始 `input.bc` 和 Clang 诊断提到的副本在已核查路径均已不存在，需要从同配方重建恢复该成员。
2. 在 G4 的 PGO 归档转换路径采用验证过的最小上限，对高内存成员限制并发。可将该成员的有界重跑安排在其余转换 worker 排空之后。保留第一次失败的归档名、成员名、退出码和 stderr 头部，避免下一次只留下取消信息。该方案保持 profile、编译参数、调试信息和打包门禁的语义，预计影响转换占用和耗时。实际产物与门禁结果须由重跑核对。
3. 同档位 4/4/1、从头重跑预计 **约 5.5–6.5 小时**，准入等待另计。实测 G4 在开始归档转换前约 3 小时 15 分，失败时累计 13,063 秒（3 小时 37 分 43 秒）。同档位 N2 归档转换至安装完成约 40 分钟，从归档完成至 RPM 构建结束约 1 小时 45 分。用后两段估算 G4 的未完成工作，中心值约 5 小时 40 分。若整个转换阶段降为单 worker，需重新估算。

## 154-B 与主机状态

2026-11-25 05:37:56 PST，`llvm-opt-task154-after-153.service` 从 04:15:21 PST 起已运行 **1 小时 22 分 35 秒**，正在等待构建磁盘准入。两次编号的完整构建子单元均为 inactive，构建阶段尚未开始，实际构建运行时长为 0。最近一次准入内存已通过，磁盘线为 302,154,457,695 B。

| 项目 | 字节 |
|---|---:|
| /home 可用 | 274,024,816,640 |
| 距 154-B 磁盘线尚差 | 28,129,641,055 |
| MemAvailable | 21,293,047,808 |

[状态快照与最后准入记录](../../tools/bolt/results/task159/154-status.json)

## G4 总日志原文

以下为指定 `log.txt` 的 L17499–L17568，含第一条 traceback 前 40 行，以及后续直至文件结束。日志在第一条 traceback 后只剩 29 行，在 RuntimeError 后只剩 9 行。原文件 SHA256 为 `0507d3b9edc5f9d7f723a8e5f146ff49a7d2d74b5fa96c1bfab41a87046d6f47`。

~~~text
[10316s] {"path": "usr/lib64/libLLVMObjectYAML.a", "before_sha256": "1e47d5ac0df98b901daaf7465633fea8a14f7eba31bf5a29e76141bf738ac158", "after_sha256": "b337d59630c5bd997607fb1214312effbcbcc11c81c9850fd9a3cc49d73ccb4f", "before_bytes": 44603630, "after_bytes": 56051634, "members": 29, "converted": 29, "preserved": 0, "index_entries": 4325, "debug_members": 29, "missing_symbols_by_type": {"W": 3}}
[10319s] {"path": "usr/lib64/libLLVMOptDriver.a", "before_sha256": "3c94fc1c5586610fc06050779e02fb2db74ea2b83d0094031e74f99884f09f35", "after_sha256": "dfdad45f57fa539f0db241d58e20a239fba95e1fbbfd73a4f7d972a8940fd969", "before_bytes": 7001126, "after_bytes": 8101246, "members": 2, "converted": 2, "preserved": 0, "index_entries": 606, "debug_members": 2, "missing_symbols_by_type": {}}
[10321s] {"path": "usr/lib64/libLLVMOption.a", "before_sha256": "dce2177e664964b38797e33c4a59bf116e7faa11461bc4ea84d32bf6b91f5f7c", "after_sha256": "454558868eddbccbe49bcee66022b966cf1b044af863474fcf7df186f6022c38", "before_bytes": 1763630, "after_bytes": 2314408, "members": 4, "converted": 4, "preserved": 0, "index_entries": 156, "debug_members": 4, "missing_symbols_by_type": {"W": 3}}
[10324s] {"path": "usr/lib64/libLLVMOrcDebugging.a", "before_sha256": "fcec3f8a452bb92b09afdb06df015162f5217e8ef8cde6ef682e278298ef967c", "after_sha256": "770723485d8967042304227c563ac0636fac361b6a451b84a5482da30e93a2e2", "before_bytes": 7709602, "after_bytes": 8565812, "members": 7, "converted": 7, "preserved": 0, "index_entries": 437, "debug_members": 7, "missing_symbols_by_type": {"W": 5}}
[10345s] {"path": "usr/lib64/libLLVMOrcJIT.a", "before_sha256": "af9c8b8eda1efe74994ffb7b60ab3987cd2a09dfe2f7b69f71094a27c3409066", "after_sha256": "77861cb0a27d2405942ec2a9c8dcb15072c368da1cabd88fc03f8fee5a649445", "before_bytes": 91009380, "after_bytes": 99970270, "members": 57, "converted": 57, "preserved": 0, "index_entries": 5088, "debug_members": 57, "missing_symbols_by_type": {"W": 20}}
[10348s] {"path": "usr/lib64/libLLVMOrcShared.a", "before_sha256": "16ec577388b3444f68226d0a17133bfe90160f9e039bbe5b41f8a4297512b2fe", "after_sha256": "a5910bd10dd3dc038bfdc0b477425da8a1cee180f54d0e25478d6ef04647a5c6", "before_bytes": 1126844, "after_bytes": 1293700, "members": 7, "converted": 7, "preserved": 0, "index_entries": 173, "debug_members": 7, "missing_symbols_by_type": {}}
[10351s] {"path": "usr/lib64/libLLVMOrcTargetProcess.a", "before_sha256": "dc1dc66b68cd5df9a9cc835798ddf25841803e75447161b33398d643517f6007", "after_sha256": "84eed99fc03cf93ce292a8dde418260957e8f4b229e370f1445380e7862831af", "before_bytes": 10221056, "after_bytes": 12032896, "members": 15, "converted": 15, "preserved": 0, "index_entries": 579, "debug_members": 15, "missing_symbols_by_type": {}}
[10375s] {"path": "usr/lib64/libLLVMPasses.a", "before_sha256": "91438e6f8ec2173c8359d91a6103d4d8720a9c0511805f22ba550634ca7abcaa", "after_sha256": "d8616a22c1600d65147afdc732c4cdb66dbd1ca7af412ef84c88b420b27cf303", "before_bytes": 46738864, "after_bytes": 54147030, "members": 6, "converted": 6, "preserved": 0, "index_entries": 10159, "debug_members": 6, "missing_symbols_by_type": {"W": 20}}
[10377s] {"path": "usr/lib64/libLLVMPlugins.a", "before_sha256": "405e3088fa82683c8caf2daba9ff7c458f633c02e1d381648c94c88fd117e200", "after_sha256": "90061bd8ec9d1dce3dd5f7efca85a17e65d2fa63d6a0f756f400deb25b9716a8", "before_bytes": 150060, "after_bytes": 163640, "members": 1, "converted": 1, "preserved": 0, "index_entries": 3, "debug_members": 1, "missing_symbols_by_type": {}}
[10388s] {"path": "usr/lib64/libLLVMProfileData.a", "before_sha256": "0771dd7f495ed7784b6109500f65f8c80d06feaa72ef96527ff1589dea81aa74", "after_sha256": "3c79d2fd8a6c93ec0ee7d59074e03003b9e00a0883112232a8e530d50ab57edf", "before_bytes": 32137052, "after_bytes": 40751044, "members": 21, "converted": 21, "preserved": 0, "index_entries": 3281, "debug_members": 21, "missing_symbols_by_type": {"W": 8}}
[10392s] {"path": "usr/lib64/libLLVMRemarks.a", "before_sha256": "2904e0872d21626cf644cae72f004be5b7845dbf30568ac74d8c6c448f004f59", "after_sha256": "a5d07d919248f7af9439caacdac4ccbb25917c5434f4a2d7a86add4564cbb671", "before_bytes": 5085568, "after_bytes": 5904264, "members": 11, "converted": 11, "preserved": 0, "index_entries": 526, "debug_members": 11, "missing_symbols_by_type": {"W": 1}}
[10397s] {"path": "usr/lib64/libLLVMRuntimeDyld.a", "before_sha256": "bd26de18b416e2ba691a888c9a6512f58b246dd648a9fd0c8b84e3876b6981b3", "after_sha256": "67a0c5afc7af39f44ad9a3c3ff1e608439f18e5bd63c3b9448bb5dbfba301f04", "before_bytes": 9643094, "after_bytes": 11121218, "members": 8, "converted": 8, "preserved": 0, "index_entries": 987, "debug_members": 8, "missing_symbols_by_type": {"W": 1}}
[10401s] {"path": "usr/lib64/libLLVMSandboxIR.a", "before_sha256": "21d86430f69119b49748c87e1ff91fb920bd61a2cb5c7499c660a651cf5dad2b", "after_sha256": "78256d9e90eb3df8268cec69ea57df23f54c086870a363ffaaf9ab67419ae364", "before_bytes": 9982294, "after_bytes": 11176626, "members": 15, "converted": 15, "preserved": 0, "index_entries": 1815, "debug_members": 15, "missing_symbols_by_type": {}}
[10438s] {"path": "usr/lib64/libLLVMScalarOpts.a", "before_sha256": "726b2bafe4722fa40a54e453b6a7f331eecd456f31a908450aa360ebaec0840d", "after_sha256": "1257e214ec030bb85e830b57f2cea233bd67fb6f926bf9f6e84f8f465c546796", "before_bytes": 128040758, "after_bytes": 157777356, "members": 81, "converted": 81, "preserved": 0, "index_entries": 5186, "debug_members": 81, "missing_symbols_by_type": {"W": 88}}
[10463s] {"path": "usr/lib64/libLLVMSelectionDAG.a", "before_sha256": "f09224247c7565a153ba2473b796ae26290e87a71b14397db4eeeba3840dc16a", "after_sha256": "1b74c4cea93b62087e58455c7f77f26d3a1255b0741cb44027b42c27529a257e", "before_bytes": 59256720, "after_bytes": 82794292, "members": 26, "converted": 26, "preserved": 0, "index_entries": 4093, "debug_members": 26, "missing_symbols_by_type": {"W": 7}}
[10484s] {"path": "usr/lib64/libLLVMSupport.a", "before_sha256": "afa1b6f4f4963553fe4a8d0b2fe8be93509821dfd580564d46a1180d6256c7dc", "after_sha256": "15506ab188ad151e0d6ebccd2b69490039e94aa9ac526c46163d4abdb416d3cb", "before_bytes": 44532638, "after_bytes": 56047134, "members": 179, "converted": 175, "preserved": 4, "index_entries": 5841, "debug_members": 176, "missing_symbols_by_type": {"W": 4}}
[10487s] {"path": "usr/lib64/libLLVMSupportLSP.a", "before_sha256": "78c06d463af8c71637471dfdd4c0cefe2a866cdc2cf573e81b9b81ea7f61c377", "after_sha256": "b0fed6ec77f59a1fdbbe3ae596ed170955c4a82f7128b1bc51718b18771c55e5", "before_bytes": 2795572, "after_bytes": 3572112, "members": 3, "converted": 3, "preserved": 0, "index_entries": 269, "debug_members": 3, "missing_symbols_by_type": {"W": 7}}
[10491s] {"path": "usr/lib64/libLLVMSymbolize.a", "before_sha256": "f3cc0c731eeb697c324af347c5d1a4a0e88fc41dacdccc0373334604f7a3cb43", "after_sha256": "66c76240d6baf803100b4b35a62ce56a8d4f8fcb124d39489931faa2f50a2a84", "before_bytes": 4914490, "after_bytes": 6120050, "members": 5, "converted": 5, "preserved": 0, "index_entries": 356, "debug_members": 5, "missing_symbols_by_type": {}}
[10496s] {"path": "usr/lib64/libLLVMTableGen.a", "before_sha256": "1e0bbf314c0e0a5ab1c0efd5651980c56a2cfd26424af12a8b09086348ba7ade", "after_sha256": "5273473283500143c992402407465d3838d9837db528766c9f50771ae633f386", "before_bytes": 12191018, "after_bytes": 15538468, "members": 14, "converted": 14, "preserved": 0, "index_entries": 1055, "debug_members": 14, "missing_symbols_by_type": {"W": 2}}
[10502s] {"path": "usr/lib64/libLLVMTableGenBasic.a", "before_sha256": "139bd190e8d232622cb7f4da13e21cfcde7407cca8325834f44f6aa1c5aa81ed", "after_sha256": "995fbbeb1e9fde63515cb4de3511384a3069daaf11aaf16fb711e70325936edb", "before_bytes": 9732058, "after_bytes": 12314558, "members": 13, "converted": 13, "preserved": 0, "index_entries": 368, "debug_members": 13, "missing_symbols_by_type": {}}
[10513s] {"path": "usr/lib64/libLLVMTableGenCommon.a", "before_sha256": "0ef98b255d1a0006a7f78c6e22eef4f2e3eb59605413fe3da960a6dbb3fb1c74", "after_sha256": "b3d0b5ede4a019a16246b4e419e75913698eefb5183ca7cb24a0d961c0e4235b", "before_bytes": 28674530, "after_bytes": 36336996, "members": 23, "converted": 23, "preserved": 0, "index_entries": 1615, "debug_members": 23, "missing_symbols_by_type": {"W": 2}}
[10516s] {"path": "usr/lib64/libLLVMTarget.a", "before_sha256": "73018b78c4387945c5bc44b46099ffaac2da1136e99687d9391584ddec73de84", "after_sha256": "b264910108cb48ec7b276085c46e5be9c79c47819a1e9a9bc5392d5b814fd53b", "before_bytes": 1612664, "after_bytes": 1840280, "members": 5, "converted": 5, "preserved": 0, "index_entries": 191, "debug_members": 5, "missing_symbols_by_type": {}}
[10519s] {"path": "usr/lib64/libLLVMTargetParser.a", "before_sha256": "05578b9bd22c29d1006d261ad445ee1dcdb700f77d6f3550d0169f5f6ff1de7d", "after_sha256": "19d68c26d7f28d86703f8caebcfb9da3202d5274738bfe029f7e51e19bdd9524", "before_bytes": 5660786, "after_bytes": 7437170, "members": 15, "converted": 15, "preserved": 0, "index_entries": 465, "debug_members": 15, "missing_symbols_by_type": {"W": 2}}
[10521s] {"path": "usr/lib64/libLLVMTelemetry.a", "before_sha256": "3f04ca7a4c67b6a8d2f92d27c6c0033c30b0c9dfb3079b5558b30ec07448bedd", "after_sha256": "e1a538b4e6222abd78683cabf982c6300d13a263e05294f45402892f0abfb8fc", "before_bytes": 241746, "after_bytes": 287114, "members": 1, "converted": 1, "preserved": 0, "index_entries": 23, "debug_members": 1, "missing_symbols_by_type": {}}
[10527s] {"path": "usr/lib64/libLLVMTextAPI.a", "before_sha256": "7ea7395af2ae8979b10bcfaad9ebbb9d062b41b7661cba6a80f4715831567bfe", "after_sha256": "de44ea3e8713bf882767eef9530f410f0263eec04ff2b9951d6c59375190872f", "before_bytes": 9737826, "after_bytes": 11966650, "members": 15, "converted": 15, "preserved": 0, "index_entries": 754, "debug_members": 15, "missing_symbols_by_type": {}}
[10530s] {"path": "usr/lib64/libLLVMTextAPIBinaryReader.a", "before_sha256": "2191dff7d8c5ba236e977bd5d93360245e5aaa81ac1f6bf0a29b09857a605d7d", "after_sha256": "22ee4c3ad4bc262b33df1013b1ffc2d24b27384eef5da21bea6a24d2f765c8df", "before_bytes": 1453082, "after_bytes": 1688402, "members": 1, "converted": 1, "preserved": 0, "index_entries": 50, "debug_members": 1, "missing_symbols_by_type": {}}
[10559s] {"path": "usr/lib64/libLLVMTransformUtils.a", "before_sha256": "519f2979ab81e10f4f5cbb12fbbb18e0e46b30a3d3f75f281eb2c9de8926a514", "after_sha256": "08b019df3a58f617d71d78ac83a8de2a19d1926b5ba43855d32d2a091a1118d5", "before_bytes": 99337750, "after_bytes": 122247764, "members": 94, "converted": 94, "preserved": 0, "index_entries": 4346, "debug_members": 94, "missing_symbols_by_type": {"W": 72}}
[10595s] {"path": "usr/lib64/libLLVMVectorize.a", "before_sha256": "210a990946f3f795d85c203cafe86800311abed7cf3a4940cbd2eaa3a18a1764", "after_sha256": "52559a3d5f1204c747c68e6ee13cc5206728b6a0524894c9737b0fec7f2efb5f", "before_bytes": 87985522, "after_bytes": 114074986, "members": 33, "converted": 33, "preserved": 0, "index_entries": 5740, "debug_members": 33, "missing_symbols_by_type": {"W": 25}}
[10597s] {"path": "usr/lib64/libLLVMWindowsDriver.a", "before_sha256": "c82e6eb40dcc3be5668edefc3ee8658cb02f2efcb8c7248b3c937b556a4fa7e9", "after_sha256": "ab0b3d083b740317afe366084ed426fcad3757b9411a2708cd74d28db3fe57f6", "before_bytes": 288076, "after_bytes": 335996, "members": 1, "converted": 1, "preserved": 0, "index_entries": 20, "debug_members": 1, "missing_symbols_by_type": {}}
[10599s] {"path": "usr/lib64/libLLVMWindowsManifest.a", "before_sha256": "835dd21c276665c54ee66c49f8d035d489454cb9573eeb41cf71eee3fbf23a93", "after_sha256": "0a12a2e5c5f300070e8ec9967524067b2c3af16dff1be6cb4eb804741dc4be54", "before_bytes": 411968, "after_bytes": 444900, "members": 1, "converted": 1, "preserved": 0, "index_entries": 27, "debug_members": 1, "missing_symbols_by_type": {}}
[10603s] {"path": "usr/lib64/libLLVMX86AsmParser.a", "before_sha256": "afda2f0f5b83dfc14b055c7ca710ecba18c13abdb82f1da5344dfb47352e7f40", "after_sha256": "525e9050799fbc8337266c1aadfb583fbd4e6054c5307c294a1f271032e6b1ab", "before_bytes": 3506410, "after_bytes": 4123710, "members": 1, "converted": 1, "preserved": 0, "index_entries": 116, "debug_members": 1, "missing_symbols_by_type": {}}
[10634s] {"path": "usr/lib64/libLLVMX86CodeGen.a", "before_sha256": "a29c4361291ec90eecaa1df8580192174d7fddb38c2c049bf5046c2e062dd9de", "after_sha256": "e78ebadb7be991297081981f2503c6e89672c0661e357578dd99ee055f5a7aff", "before_bytes": 114657450, "after_bytes": 150462572, "members": 66, "converted": 66, "preserved": 0, "index_entries": 5339, "debug_members": 66, "missing_symbols_by_type": {"W": 8}}
[10639s] {"path": "usr/lib64/libLLVMX86Desc.a", "before_sha256": "7bfb1d81031c51d4b21560b03dc64d2fedc8308d41429dac058f7a6cb1af0e20", "after_sha256": "071c989e2c7e19c702c31446f4bce84d278334ddef95f0ce69ccd1680ec603a5", "before_bytes": 11962220, "after_bytes": 16969644, "members": 16, "converted": 16, "preserved": 0, "index_entries": 2311, "debug_members": 16, "missing_symbols_by_type": {}}
[10642s] {"path": "usr/lib64/libLLVMX86Disassembler.a", "before_sha256": "91f1cf212613b551dde9e7b3bf4fd79a4577396f1615f375e1637b82c117da29", "after_sha256": "a2e46eefe53b40fc932044ad10f7d498175dc7dd650f7336802099359bc723e5", "before_bytes": 1927768, "after_bytes": 5386132, "members": 1, "converted": 1, "preserved": 0, "index_entries": 4, "debug_members": 1, "missing_symbols_by_type": {}}
[10643s] {"path": "usr/lib64/libLLVMX86Info.a", "before_sha256": "2ed487e15a0690e0118a235b4c64f55f859d836c859b9ba0657b8984ff040592", "after_sha256": "90cd27eb564e326e9d7057ee690ec904f7a0b53afc900877ab47ff8eade20bc5", "before_bytes": 91096, "after_bytes": 98708, "members": 1, "converted": 1, "preserved": 0, "index_entries": 6, "debug_members": 1, "missing_symbols_by_type": {}}
[10645s] {"path": "usr/lib64/libLLVMX86TargetMCA.a", "before_sha256": "ad82b142b50e014a2bcbda0ece8f6ca4a5a67dfbc0459a490b3cb0a032813d37", "after_sha256": "f64f56f608da7bbca967d9cfae2197bfcb72a2a94467c7b6505283f04cc97bff", "before_bytes": 141158, "after_bytes": 159178, "members": 1, "converted": 1, "preserved": 0, "index_entries": 14, "debug_members": 1, "missing_symbols_by_type": {}}
[10648s] {"path": "usr/lib64/libLLVMXRay.a", "before_sha256": "ff2d18c49970b0e661159c6f1f847af74ac8c3e3f96e700e2565650bee8a4cad", "after_sha256": "813c91a1f9cb78246d14bf81585155254d83a9b33aa5644693a2bd098584f35d", "before_bytes": 5407476, "after_bytes": 6347916, "members": 14, "converted": 14, "preserved": 0, "index_entries": 471, "debug_members": 14, "missing_symbols_by_type": {}}
[10690s] {"path": "usr/lib64/libLLVMipo.a", "before_sha256": "78c0bfce92eae9f2658fc7e7cc74de5baa752db583feead14ccad4b57fb65427", "after_sha256": "3b7fff9765caaafb437d1941a083491861feae18dbc9059cb032cd2a444acde7", "before_bytes": 112166646, "after_bytes": 136625616, "members": 45, "converted": 45, "preserved": 0, "index_entries": 7354, "debug_members": 45, "missing_symbols_by_type": {"W": 18}}
[10695s] {"path": "usr/lib64/libarcher_static.a", "before_sha256": "311ef698f7c85fb6a3b0040b8073824234283cf0b05595b706e1662c139237da", "after_sha256": "87778fe43fa1a7478f35877e36d9a85ecb8f5b54b660bc57483aa5c5c100dfec", "before_bytes": 710566, "after_bytes": 902310, "members": 1, "converted": 1, "preserved": 0, "index_entries": 9, "debug_members": 1, "missing_symbols_by_type": {"W": 1}}
[10701s] {"path": "usr/lib64/libclangAPINotes.a", "before_sha256": "799db59c0897cde3118c7d2f607ab9a1dbf2d18fed023293690d6918a9542bfb", "after_sha256": "aeadfee6f6af8157a2e130339a007d3f5c72924da7075f1176a5bcf996f98ac8", "before_bytes": 9431532, "after_bytes": 12810324, "members": 5, "converted": 5, "preserved": 0, "index_entries": 671, "debug_members": 5, "missing_symbols_by_type": {}}
[10786s] Traceback (most recent call last):
[10786s]   File "/home/abuild/rpmbuild/SOURCES/llvm-static-archives-native.py", line 1095, in <module>
[10786s]     raise SystemExit(install_main())
[10786s]                      ~~~~~~~~~~~~^^
[10786s]   File "/home/abuild/rpmbuild/SOURCES/llvm-static-archives-native.py", line 1088, in install_main
[10786s]     return _install_main()
[10786s]   File "/home/abuild/rpmbuild/SOURCES/llvm-static-archives-native.py", line 1075, in _install_main
[10786s]     raise failure[1].with_traceback(failure[2])
[10786s]   File "/home/abuild/rpmbuild/SOURCES/llvm-static-archives-native.py", line 1061, in _install_main
[10786s]     install(args.root, args.evidence, args.compiler.resolve(), args.disassembler.resolve(),
[10786s]     ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[10786s]             args.nm.resolve(), args.build, args.arch, args.jobs, args.address_space_bytes, args.debug_info)
[10786s]             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[10786s]   File "/home/abuild/rpmbuild/SOURCES/llvm-static-archives-native.py", line 972, in install
[10786s]     result = convert(root, output, compiler, disassembler, nm, build, arch, jobs, address_space_bytes, command, debug_info)
[10786s]   File "/home/abuild/rpmbuild/SOURCES/llvm-static-archives-native.py", line 896, in convert
[10786s]     command.check()
[10786s]     ~~~~~~~~~~~~~^^
[10786s]   File "/home/abuild/rpmbuild/SOURCES/llvm-static-archives-native.py", line 602, in check
[10786s]     raise RuntimeError('cancelled after: '+self.failure_reason if self.failure_reason else 'cancelled after command failure')
[10786s] RuntimeError: cancelled after: command failed
[10787s] + exit 1
[10788s] error: Bad exit status from /var/tmp/rpm-tmp.IYOE67 (%install)
[10788s] 
[10788s] 
[10788s] RPM build errors:
[10788s]     Bad exit status from /var/tmp/rpm-tmp.IYOE67 (%install)
[10789s] 
[10789s] linhao-linux failed "build llvm.spec" at Wed Nov 25 12:25:53 UTC 2026.
[10789s] 
~~~
