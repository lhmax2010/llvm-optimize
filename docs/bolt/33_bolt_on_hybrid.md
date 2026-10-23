# BOLT 叠加 hybrid：本地完整构建与验证

状态：准备与五项解析 PASS，完整构建进行中；尚不能宣称 profile 匹配或产物通过。文件路径沿用用户指定的 20261024 标签，实际启动时间以原始记录中的时间戳为准（Asia/Shanghai）。

## 1. 合并与输入

hybrid `6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2` 上 cherry-pick BOLT `3d3b4bf564fd8edec793e49e6de75b5fa7007d16`，detached HEAD 本地提交 `aa637c1b4a0f9ea9f6f0317cf035126eba85aeb7`，tree `1c52e7922a5ae112b96dc18c297ed2dff58aa218`，作者/提交者 Hao Lin。保留 BOLT Change-Id `Ic98eab90cc017f127a66e1729b44fab8b8e8fb41`。自动合并成功，无冲突；hybrid CMake 源码/配置完整保留，BOLT helper/profile 与输入相同。源码未推送远端，没有新建分支。

固定 QB1202084 配置与 Base `20261013.024319`，只启用 packages/debug；build.conf SHA256 `e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945`。宏 `jobs 8`、`_smp_mflags -j8`、`_costomized_smp_mflags -j20`；外层 `--threads=30`。GBS export 成功，Tizen rpm 4.14.1.1 五项（x86 ON/OFF/一行回退、armv7l、aarch64）均 PASS，全部包含 8 个补丁。

## 2. 链接预检查

从 docs/53 的 build.ninja 与同一次 hybrid 构建的 rules.ninja 复制到本次 `graph-copy`，仅在复制目录执行 ninja -t commands（不在历史根内执行）。clang 唯一链接边满足原 helper replay_script：单个绝对 ThinLTO 路径 `/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache`，emit-relocs 重放生成成功。

llvm-bolt driver 和 BOLT 库 CMakeLists 均显式带 `DISABLE_LLVM_LINK_LLVM_DYLIB`，预期仍静态链接 LLVM。白名单保持 111 BOLT + 2 TF，不修改；最终由新根实际 tool-plan/tool-verify 门禁验证。[源文件与行号](../../tools/bolt/results/bolt-on-hybrid-20261024/link-precheck.json)。

## 3. 本地构建与测量

独立根 `temp/bolt-on-hybrid-20261024/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0`。MemoryMax=MemTotal−8GiB=24482983936 B，swap0、nice10、ionice2:7；无内存准入/冻结/分段，独占共享锁至本轮退出。每60秒尝试完整根 du，50秒超时记录缺失，不补造；/home低于20GiB正常停止，OOM、构建失败或BOLT门禁失败不重试、不绕过。

尚在运行；峰值、匹配统计、RPM、90对象验证与产品保全待完成。基准为 hybrid 66.696GiB、全静态+BOLT224.718GiB，比较按离散采样口径，并注明缺失范围。

## 4. 准备过程处理

1. 宿主 PATH 无 ninja；复制已有 Tizen ninja 到本次新目录，对复制的构建图查询，不触碰历史构建。
2. 五项解析第一轮引用旧7补丁SOURCES，报告缺少hybrid第8补丁；原输出保留到 five-parse-missing-patch-attempt，改指本次专用目录中完整导出输入后重跑，五项全部PASS。没有修改产品门禁或源码来规避错误。

证据：[原始目录](../../tools/bolt/results/bolt-on-hybrid-20261024/)，含合并输出、spec差异、完整文本补丁、配置/输入SHA、导出、五项解析、链接预检查和本地控制器。最终结论待更新。
