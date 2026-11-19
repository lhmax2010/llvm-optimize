# 138-D：清理、插桩编译器启动和逐阶段准入

**PASS。** 选定使用保留 G1 构建根的匹配加载器加 `--library-path` 执行原插桩 clang，第一项训练得到一份非空 profraw。新编排按阶段一次性计算 MemoryMax。实物 dry-run 核对 G1 编译器、profdata 工具和原始构建日志后，计划直接进入 G2。51 项单测与技能校验通过，21 个文件的禁用词扫描为零。原 G1 clang 和 BUILD 树保持原处。

## 清理

133-N 原调用在 `buildsteps.before-g1-recovery.py` 的 `delete_intermediate()`。`pgosteps.py` 的 G1 收尾和使用完 G4 BUILD 的后续阶段均经该函数清理，原 `pgo_pair.py` 只调用配置里的构建适配器。现场命令在 G1 的 Tizen chroot 里执行 `/usr/bin/rm`，即构建根内 `/usr/bin/toybox` 的 rm applet，版本 **0.8.14**。该 applet 拒绝 `--one-file-system`。宿主机的 GNU rm 没有参与这次清理。

技能和新版编排共用 `scripts/build_cleanup.py`。删除前验证目标是指定项目目录的严格子目录，确认路径规范且没有通过路径分量穿越符号链接。用目录文件描述符逐层预扫，遇到挂载点或不同 `st_dev` 直接报错，预扫阶段零删除。删除阶段按同样的边界逐层处理，并只解绑树中符号链接本身。编排保留构建根路径和大小记录，并在调用前检查宿主挂载。技能可用 `build_tree_cleanup` 配置一次性中间树，清理前要确认后续 checkpoint 需要的产物已外置并哈希。测试覆盖普通树、外指和悬空链接、跨设备目录、同设备挂载模拟及路径越界。本任务只删除了测试夹具。[编排补丁](../../tools/bolt/results/task138-d/orchestration.patch)

## 启动诊断

原插桩 clang 为 1,466,952,360 B，SHA256 `381789a9f576f9e6e7affe25ee568e303da6816ba28e64c86135d29c55ea06a7`。ELF 解释器 `/lib64/ld-linux-x86-64.so.2`，构建根匹配加载器为 `/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64/ld-linux-x86-64.so.2`。RUNPATH 为 `$ORIGIN/../lib64:/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64:`。NEEDED 和匹配库路径如下。

- `librt.so.1` → `/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64/librt.so.1, /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64/librt.so.1`
- `libdl.so.2` → `/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64/libdl.so.2, /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64/libdl.so.2`
- `libm.so.6` → `/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64/libm.so.6, /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64/libm.so.6`
- `libz.so.1` → `/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64/libz.so.1.3.1, /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64/libz.so.1.3.1`
- `libstdc++.so.6` → `/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64/libstdc++.so.6.0.33, /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64/libstdc++.so.6.0.33`
- `libgcc_s.so.1` → `/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64/libgcc_s.so.1, /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64/libgcc_s.so.1`
- `libc.so.6` → `/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64/libc.so.6, /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64/libc.so.6`
- `ld-linux-x86-64.so.2` → `/home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64/ld-linux-x86-64.so.2, /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64/ld-linux-x86-64.so.2`

| 方式 | `--version` | 第一个训练输入 |
|---|---|---|
| A：匹配的构建根加载器 | clang version 22.1.8 | 一份 profraw，32,385,336 B，wall_s=15.93，max_rss_kib=1069916 |
| B：直接执行加目标 LD_LIBRARY_PATH | SIGSEGV，退出 139 | 停止该方式，未编译 |
| C：私有副本更换 ELF 解释器 | clang version 22.1.8 | 一份 profraw，32,385,320 B，wall_s=12.43，max_rss_kib=1064228 |

两种成功方式都使用 A 项的完整参数，加 `-c` 和 `-fintegrated-cc1`，各自写入独立的 `LLVM_PROFILE_FILE`。方法 A 沿用 118 C 成功的匹配加载器方式。集成 cc1 避免驱动以加载器路径重执行。方法 C 仅修改一个私有副本的 `PT_INTERP`，它证明匹配的加载器和运行库组合可用。选用 A，无须维护改写副本。方法 B 的 GDB 显示 `__libc_start_main` 来自 Tizen 根的 `libc.so.6`，该 ELF 指定的宿主解释器与目标 libc 混用即复现崩溃。[118 C](118_plugin_load.md) · [原始命令、计时、内存和回溯](../../tools/bolt/results/task138-d/diagnosis-verified.json)

### STOP 与准备修正原文

133-N 清理 STOP 原文：

~~~text
rm: Unknown option 'one-file-system' (see "rm --help")
~~~

138-D 第一轮轻量计时把目标库路径传给了宿主计时器，GDB 的启动 shell 也继承了目标库。第一次 GDB 启动报告如下。一次准备修正把目标库路径只传给被测程序，并在 GDB 中禁用启动 shell，分别补测 B、C。C 通过，B 的被测程序发生以下真实崩溃。

~~~text
During startup program terminated with signal SIGSEGV, Segmentation fault.
No stack.
Program received signal SIGSEGV, Segmentation fault.
#0  0x0000731266c4dc96 in __libc_start_main () from /home/linhao/Toolchain/development/llvm-optimize/archive/task133-n-20261118/G1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64/libc.so.6
~~~

## 一次性内存准入演算

取 133-N 结束阶段约 22.6 GiB 的 MemAvailable 作统一输入。按 `min(MemAvailable − 6 GiB, 标准上限)` 得到各步上限，低于下限即跳过。下表只算单步资源准入，G6 若跳过，依赖它的 G7 和 G8 随后跳过。

| 阶段 | 标准上限 GiB | 下限 GiB | 算出 MemoryMax GiB | 并行度 | 单步结果 |
|---|---:|---:|---:|---:|---|
| N2 全量构建 | 24.00 | 15.00 | 16.60 | 4 | 可准入 |
| G1 插桩构建 | 8.08 | 8.08 | 8.08 | 2 | 可准入 |
| G2 IR 训练 | 1.66 | 1.66 | 1.66 | 1 | 可准入 |
| G3 profdata 合并 | 2.04 | 2.04 | 2.04 | 1 | 可准入 |
| G4 PGO 构建 | 24.26 | 15.00 | 16.60 | 4 | 可准入 |
| G5 BOLT 工具与重链 | 24.26 | 15.00 | 16.60 | 4 | 可准入 |
| G6 BOLT 插桩、训练、合并 | 19.08 | 19.08 | 16.60 | 1 | SKIPPED |
| G7 BOLT 匹配 | 9.74 | 9.74 | 9.74 | 1 | 可准入 |
| G8 压缩与清单 | 24.26 | 1.00 | 16.60 | 1 | 可准入 |
| N4 全量构建 | 24.00 | 15.00 | 16.60 | 4 | 可准入 |

完整构建标准上限 24 GiB。完整构建、G4 和 G5 使用 15 GiB 链接下限，与历史 ld.lld 单进程约 13.3e9 B 对应。G 各实测阶段的上限取 131 dry-run 所引用历史峰值的 1.2 倍，向上对齐到内存页。G1、G2、G3、G6、G7 用对应上限作为下限。G5 和 G8 缺独立实测，预算上限用已测阶段最高峰值的 1.2 倍，G8 的 1 GiB 下限是压缩阶段规划值。试验中的 stage cap/Floor 细节见下方 JSON。

编排把同一次启动测量传给技能，子单元里的技能核对实际 cgroup MemoryMax。完整构建用 `--define 'mlgo_build_jobs N'`，其中 `N=max(2, floor(6 × MemoryMax / 24 GiB))`。改动只控制构建并行度，产品源码、编译参数和产物定义保持原样。138-D 未做完整重建和产物对比。看门狗保持 MemAvailable < 6 GiB 或 /home < 15 GiB 时只停止当前子单元。[内存演算 JSON](../../tools/bolt/results/task138-d/admission-22.6.json)

## 断点与交付

用 133-N 原记录生成恢复收据。执行 `--resume --recover-instrumented RECEIPT --stages ir-train --dry-run` 后，实际回读校验原 G1 clang 和 profdata 工具 SHA、原日志 SHA 和成功标记、R 提交、构建配置及配方身份。输出 `VERIFIED_FOR_REUSE`，唯一所选阶段为 G2，规划 23 条匹配加载器训练命令，未创建输出目录和 checkpoint。单测以夹具验证实际执行路径建立 G1 checkpoint 并且只调用 G2。此次仅对首个真实训练项做了 A、C 诊断。[dry-run](../../tools/bolt/results/task138-d/resume-dry-run.json) · [收据](../../tools/bolt/results/task138-d/recovery-receipt.json)

新编排工作副本在 `/home/linhao/Toolchain/development/llvm-optimize/archive/task138-d/orchestration`，证据分支包含相对 133-N 的补丁。原 133-N 现场的 BUILD 树仍在。技能单测 51/51 通过，格式验证通过，禁用词扫描 21 份文件零命中。[单测](../../tools/bolt/results/task138-d/unittest.txt) · [扫描](../../tools/bolt/results/task138-d/scan-results.json)

`server-kit` 等待单独同步。需要复制 `skill/SKILL.md`、`skill/config.example.json`、`skill/references/compiler-launch.md`、`skill/references/resource-budget.md`、`skill/scripts/pgo_pair.py`、`skill/scripts/build_cleanup.py`、`skill/scripts/stage_resources.py`、`skill/tests/test_pgo_pair.py`、`skill/tests/test_build_cleanup.py`。同步时重打技能归档，并更新根目录的配置示例与 SHA256 清单。
