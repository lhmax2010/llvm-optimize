# 142 361624 修正方案快速验证

**U PASS，V1 STOP，V2 STOP。** 本地分支 `fix-361624` 的最终 tree 与 C1 逐文件一致。
V1 停在 GBS 准备阶段，产出验证未执行。V2 是非 LTO 快速验证。

## U · 本地提交

在 PS1 `da885208aeb52f55c448ff46873d242346727522` 的索引分别重放 C1 补丁的 CMake 子集和全量，生成的最终 tree 为 `40c20b2b29f7f579c2bafcb48c5c63bc773b27b6`，对 C1 提交的内容 diff 为空。提交 1 验证 A2 变量恢复 18 处，提交 2 仅含 v3 两份 spec 和 A5。提交说明及新增行零命中，标题均不超过 50 字符。

|序|提交|tree|diffstat|原文|
|---|---|---|---|---|
|1|`4e5adcd58008a6340ba9005b7c8a1ae28efd46e2`|`88466faf20a95cfa24576c0449742c2b249420b1`|19 files changed, 31 insertions(+), 4 deletions(-)|[说明](../../tools/bolt/results/task142/1-message.txt) · [逐文件统计](../../tools/bolt/results/task142/1-diffstat.txt) · [补丁](../../tools/bolt/results/task142/1.patch)|
|2|`7a53f583607e02de469158d111790170694b4781`|`40c20b2b29f7f579c2bafcb48c5c63bc773b27b6`|2 files changed, 70 insertions(+), 41 deletions(-)|[说明](../../tools/bolt/results/task142/2-message.txt) · [逐文件统计](../../tools/bolt/results/task142/2-diffstat.txt) · [补丁](../../tools/bolt/results/task142/2.patch)|

未发现匹配本项目的 141 编排或子单元，也未发现 141 留下的结果目录。142 没有停止 141 相关进程。

## V1 · Standalone GBS（STOP）

x86_64，2 个 Ninja jobs，5,500 MiB 服务内存上限，swap 0。使用 Toolchain 冻结仓库 `tizen-base-toolchain_20261030.120529` 的 packages 和 debug，GBS 构建配置取自已经保留的同一项目配置。公开目录核对了 llvm、llvm-devel、llvm-static-devel、libllvm、libomp、clang、compiler-rt 的 `22.1.8-4.1` x86_64 RPM。[冻结仓库头](../../tools/bolt/results/task142/V1-frozen-header-probes.json) · [实际装入构建根的五项 EVR](../../tools/bolt/results/task142/V1-provider-nevra.txt)

|核对项|结果|
|---|---|
|冻结构建依赖|五项已装入并核实 `22.1.8-4.1`。|
|GBS 构建成功、spec 自身 provider consistency gate|STOP，准备阶段退出，spec gate 未运行。|
|7 个工具及 2 个归档、Requires|未运行。|
|所有可执行文件 GNU_RELRO、和 debug 文件的 build-id 配对|未运行。|
|llvm-bolt --version 的 x86-64 和 aarch64|未运行。|
|x86_64 和 AArch64 relocation mode 重写、x86_64 退出码|未运行。|
|CMakeCache dylib、镜像编译和 runtime flags|未运行。|

第一次 `--noinit` 缺少 GBS 放在构建根内的发行配置。准备修正按 `.guessed_dist` 补齐 `build.conf`，文件 SHA 与源配置一致。第二次进入 depanneur 后按发行名 `build` 查找源码，预置位置却是 `tizen_base_toolchain_standard`，返回失败。按一次准备修正上限停止。

```text
build root broken caused by missing build conf. Please build without --noinit first
error: <gbs>some packages failed to be built
```

```text
[    0s] /usr/bin/build: line 1215: cd: /home/linhao/Toolchain/development/llvm-optimize/archive/task142/V1-a1/gbs-driver/local/sources/build/llvm-tools-subpkgs-22.1.8-1: No such file or directory
[    0s] llvm-tools-subpkgs.spec is empty.  This should not happen...
```

[首次 GBS 原文](../../tools/bolt/results/task142/V1-first-gbs.txt) · [修正后的 GBS 原文](../../tools/bolt/results/task142/V1-gbs.txt) · [底层 build 原文](../../tools/bolt/results/task142/V1-rpmbuild.txt)

## V2 · In-tree

候选 I `a4d024f0f35630a743653af1542cb02e539fced6`。沿用 133-D N3 (iii) 的源码与项目组合，另用 `-DLLVM_ENABLE_LTO=OFF`，同时去掉原 CMake C/C++/ASM 和 exe/shared 链接参数里显式的 `-flto=thin`；保留其余选项。服务 6 GiB，swap 0，Nice 19，I/O idle。[实际配置参数](../../tools/bolt/results/task142/V2-original-configure-argv.json) · [N3 (ii) 原文](../../tools/bolt/results/task142/N3-raw-error.txt)

|核对项|结果|
|---|---|
|三目标成功完成最终链接|STOP / 未完成，`llvm-bolt`、`merge-fdata`、`llvm-bat-dump`。|
|静态 X86 组件、镜像源|PASS。lib64/libLLVMX86CodeGen.a, lib64/libLLVMX86AsmParser.a, lib64/libLLVMX86Desc.a, lib64/libLLVMX86Disassembler.a, lib64/libLLVMX86Info.a。镜像源未进入编译图。|
|成品 NEEDED|未运行（无最终二进制）。|
|llvm-bolt --version|未运行（无最终二进制）。|
|静态 x86_64 relocation mode 冒烟|未运行（无最终二进制）。|
|N3 (ii) 对照组|历史原样 PS1 配置报 `Found erroneous configuration for source file X86BoltMnemonicTables.cpp`。|

[三目标 Ninja 日志](../../tools/bolt/results/task142/V2-original-ninja.txt) · [链接命令](../../tools/bolt/results/task142/V2-original-link-line.txt) · [结果 JSON](../../tools/bolt/results/task142/V2-result.json)

首轮 Ninja 在 `bolt_rt` 的 C 编译器可执行探针失败。修正仅在验证单元的 `COMPILER_PATH` 中加入调用原 Tizen GNU ld 的脚本，用 sysroot 的 loader 和库启动 ld。最小同版 clang 链接探针通过，随后复用已完成的 Ninja 输出。源码和 CMake 配置未改。

```text
ld: error while loading shared libraries: libbfd-2.43.so: cannot open shared object file: No such file or directory
clang: error: unable to execute command: No such file or directory
clang: error: linker command failed due to signal (use -v to see invocation)
ninja: build stopped: subcommand failed.
```

[首轮 Ninja 原文](../../tools/bolt/results/task142/V2-attempt1-ninja.txt) · [首轮 STOP](../../tools/bolt/results/task142/V2-attempt1-STOP.txt) · [环境修正核对](../../tools/bolt/results/task142/V2-linker-provenance.json)

续跑的 GNU ld 探针切换成功并进入 `bolt_rt` 编译。嵌套 CMake 未获得主构建 C/C++ argv 中的 `-resource-dir`，而私有 clang 的默认资源目录没有头文件。两份 runtime 源均报 `stddef.h` 缺失。依一次准备修正的上限停止，未修改 I、未绕过 `bolt_rt`，未生成三个最终目标。

```text
/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/lib64/gcc/x86_64-tizen-linux-gnu/14.2.0/../../../gcc/x86_64-tizen-linux-gnu/14.2.0/include/c++/cstddef:50:10: fatal error: 'stddef.h' file not found
ninja: build stopped: subcommand failed.
```

V2 原始非零阶段情况如下。
```text
exit=1, expected=0, log=/home/linhao/Toolchain/development/llvm-optimize/archive/task142/V2-a2/ninja.txt
```
[原始 STOP](../../tools/bolt/results/task142/V2-original-STOP.txt)

## 用时及保护线

U 从任务现场创建到启动 V2 用了不到 3 分钟。V1 第一次 5 分 25 秒，准备修正后的 GBS 尝试 0 分 1 秒。V2 配置 8 分 56 秒，续跑服务 0 分 46 秒，首轮服务总计 16 分 38 秒。截至汇总 22 分 20 秒。
MemAvailable 低于 2 GiB 的看门狗事件 0 次。[看门狗原文](../../tools/bolt/results/task142/watchdog.jsonl) · [超限本地材料索引](../../tools/bolt/results/task142/large-local-artifacts.json)

读取了 C1、PS5、I、N3 配置、两份 GBS 准备日志、冻结仓库的公开元数据和本轮 V2 生成图、编译日志。V1 没有生成本轮 RPM，V2 没有生成三目标的完整产物。历史评审和 74 的夹具预检不计入本轮结果。证据只推 bolt-v4。
