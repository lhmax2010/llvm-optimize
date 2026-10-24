# BOLT 叠加 hybrid：本地完整构建与验证

**本地验证全部 PASS**：22 个二进制 RPM、1 个源码 RPM，BOLT 全部门禁与 90/90 完整对象比较通过。profile R=0.004238545%，与全静态参考 0.0042385% 一致。完整根已观测峰值 **64.055 GiB**，比 hybrid 66.696 GiB 低 2.641 GiB，比全静态+BOLT 224.718 GiB 低 160.663 GiB；离散采样和历史构建差异见第 6 节。

## 1. 合并与输入

hybrid `6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2` 上 cherry-pick BOLT `3d3b4bf564fd8edec793e49e6de75b5fa7007d16`。本地 detached HEAD 提交 **`aa637c1b4a0f9ea9f6f0317cf035126eba85aeb7`**；父提交为 hybrid，tree `1c52e7922a5ae112b96dc18c297ed2dff58aa218`。作者/提交者 Hao Lin <hao.lin@samsung.com>，Change-Id `Ic98eab90cc017f127a66e1729b44fab8b8e8fb41`。

自动合并无冲突，因此没有人工冲突解法。hybrid 的 CMake 配置、源码与补丁全部保留；BOLT Source、代码块与 post 链保留，helper/profile 与 3d3b4bf 逐字节相同。只在本地提交，没有新建分支或推送 Gerrit。

使用 GBS 2.1.0 与固定 QB1202084 配置，只启用 Base `20261013.024319` 的 packages/debug。build.conf SHA256 `e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945`；配置 SHA256 `ce60cb95bad10e8e7ed20f3eb69094c4f91efacb8d89725967a6a4deb2a3d388`。宏为 `jobs 8`、`_smp_mflags -j8`、`_costomized_smp_mflags -j20`，外层 `--threads=30`。实际 ordinary ninja 为 `-d keeprsp -j6`（编译池6/链接池2），与 docs/53 相同。文件名的20261024为用户指定标签，真实时间见日志。

GBS export 成功，8 个导出补丁与 hybrid 导出逐字节相同。Tizen rpm 4.14.1.1 的 x86 BOLT ON、OFF、一行回退、armv7l、aarch64 五项均 PASS（每项8个补丁）。仅在专用解析目录运行 rpm；不在任何历史根运行 cmake/ninja。

证据：[local-source.patch](../../tools/bolt/results/bolt-on-hybrid-20261024/local-source.patch), [five-parse/matrix.json](../../tools/bolt/results/bolt-on-hybrid-20261024/five-parse/matrix.json), [hybrid-export-patches-unchanged.json](../../tools/bolt/results/bolt-on-hybrid-20261024/hybrid-export-patches-unchanged.json), [build-command.json](../../tools/bolt/results/bolt-on-hybrid-20261024/build-command.json)。

## 2. 链接预检查与真实白名单

预检查从 docs/53 保存的 build.ninja 和对应 rules.ninja 复制到本次 graph-copy，仅在复制图上执行 ninja -t commands。clang 链接命令具有唯一绝对 `--thinlto-cache-dir=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache`，通过原 helper replay_script；本次新根的实际重链随后也通过。

llvm-bolt driver 及 BOLT 库显式指定 `DISABLE_LLVM_LINK_LLVM_DYLIB`，hybrid 没有把 llvm-bolt 改为 LLVM 动态链接。实际 llvm-bolt 的 NEEDED 不含 libLLVM/libclang-cpp。**白名单未修改、无分类差异**：102对象、7静态库、1 executable、1 generated，共111个 BOLT任务，加2个TF刷新任务。真实 planned=executed=113，ninja_diagnostics=0，BOLT_NINJA_EXIT_0、本次新产出和TF归档复核均 PASS。

本树 llvm-bolt SHA256 `0ecdff6172f7fffb08d30f3865976ca15dc8708c3a1ef9fe0d2a543059996f75`。[link-precheck.json](../../tools/bolt/results/bolt-on-hybrid-20261024/link-precheck.json), [linkage-source-excerpts.txt](../../tools/bolt/results/bolt-on-hybrid-20261024/linkage-source-excerpts.txt), [bolt-work/tool-plan.json](../../tools/bolt/results/bolt-on-hybrid-20261024/bolt-work/tool-plan.json), [bolt-work/tool-build.txt](../../tools/bolt/results/bolt-on-hybrid-20261024/bolt-work/tool-build.txt), [bolt-work/tool-build-verification.json](../../tools/bolt/results/bolt-on-hybrid-20261024/bolt-work/tool-build-verification.json), [built-llvm-bolt-needed.txt](../../tools/bolt/results/bolt-on-hybrid-20261024/built-llvm-bolt-needed.txt)。

## 3. 构建、资源和时间线

GBS 退出0；开始 2026-10-23T22:12:17.026361+08:00，结束 2026-10-24T00:44:52.596856+08:00，耗时 9155.6 秒。独立根 `/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-on-hybrid-20261024/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0` 保留。

MemoryMax=MemTotal−8GiB=24482983936 B，MemorySwapMax=0，nice10、ionice2:7。独占共享锁贯穿本轮，无内存准入、冻结或分段；/home低于20GiB正常停止规则保留。cgroup memory.peak=24146620416 B，memory.events 原文：

```text
low 0
high 0
max 0
oom 0
oom_kill 0
oom_group_kill 0
```

每60秒尝试 chroot 内 `du -sx -B1 /`，50秒扫描超时记缺失。[du-root.jsonl](../../tools/bolt/results/bolt-on-hybrid-20261024/du-root.jsonl)、[resources.jsonl](../../tools/bolt/results/bolt-on-hybrid-20261024/resources.jsonl)、[build-result.json](../../tools/bolt/results/bolt-on-hybrid-20261024/build-result.json)。

| 阶段锚点 | 日志行 | elapsed s |
|---|---:|---:|
| prep | 448 | 284 |
| build | 515 | 303 |
| build-end | 10857 | 4660 |
| install | 10858 | 4660 |
| disk-begin | 16436 | 5131 |
| disk-tool-built | 23644 | 5933 |
| pipeline-pass | 23650 | 6227 |
| disk-pipeline | 23651 | 6227 |
| compare-root | 23656 | 6335 |
| cache-release | 23658 | 6373 |
| native-start | 23678 | 6374 |
| native-end | 24129 | 8469 |
| find-debuginfo | 24132 | 8474 |
| post-pass | 24720 | 8869 |
| disk-post | 24721 | 8869 |
| packaging | 24723 | 8871 |
| finished | 25202 | 9141 |

完整锚点及原文：[timeline.tsv](../../tools/bolt/results/bolt-on-hybrid-20261024/timeline.tsv)、[excerpts.txt](../../tools/bolt/results/bolt-on-hybrid-20261024/excerpts.txt)。普通链接期出现可观察的 I/O 等待，CPU/日志继续推进，无OOM；读数见 ordinary-link-*。不把I/O等待认定为死锁。

## 4. BOLT、缓存与 post 门禁

| N | M | S | U | Q | R | S/N |
|---:|---:|---:|---:|---:|---:|---:|
| 23592 | 144032 | 0 | 1 | 383 | 0.004238545% | 0.000000000% |

双5%门禁 PASS、禁用 infer-stale；BOLT标识节、strip-all SHA链、安全属性和两次tiny均 PASS。compare-root确认5429条目完全不变；Source1005转换225归档PASS；post反向检查、别名与安装SHA尾检PASS。所有统计来自本次树内新建llvm-bolt，没有使用历史工具代替。

ordinary SHA256 `d5090159915657b235b96f1202c058e1efd1647d6a2225ac8fdb2906aeaa501d`；candidate SHA256 **`8b799f18e2bc37269385db125c881609e8457de1dd179f5d9d0ff9f557b58d16`**。BOLT前标识节与strip前后链见 [bolt-work/pipeline-result.json](../../tools/bolt/results/bolt-on-hybrid-20261024/bolt-work/pipeline-result.json)。

缓存释放日志原文：

```text
[ 6373s] BOLT_CACHE_RELEASE removed path=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache files=13162 allocated_bytes=21622669312 seconds=36.8142408599997
```

实际释放 21622669312 B（20.138 GiB）、13162 文件，用时36.814秒。随后转换、安装、平台后处理与RPM打包全部继续通过。

## 5. 对象、链接与产物保全

docs/22同一批30 TU × armv7l/aarch64/x86_64，90份输入逐一核对SHA。使用本次 ordinary 副本与 candidate，在本次根内同一 compiler 路径和同一 inode 上依次编译，同一输入/输出路径、--no-default-config，比较完整 `.o`，不剥离 .GCC.command.line：**90/90 PASS**。三个目标各30/30。测试参数、每条输出SHA与命令均保留。验证总用时1092.4秒（含保全和链接检查），验证cgroup观测峰值13011689472B、swap=0、OOM=0，见 [validation-resource-summary.json](../../tools/bolt/results/bolt-on-hybrid-20261024/validation-resource-summary.json)。

clang、clang++/clang-cl/clang-cpp、lld及其别名、llvm-ar/llvm-ranlib均无 libLLVM.so 或 libclang-cpp.so 依赖；candidate 与 ordinary 的 NEEDED 列表相同。[objects-result.json](../../tools/bolt/results/bolt-on-hybrid-20261024/objects-result.json)、[linkage.json](../../tools/bolt/results/bolt-on-hybrid-20261024/linkage.json)。

保全目录：`/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-on-hybrid-20261024/products/`。candidate、ordinary、llvm-bolt、identity.json、四次disk-report、cache-release.json、全部22二进制RPM和1源码RPM均复制后复核SHA。根不删除；[preserved-products.json](../../tools/bolt/results/bolt-on-hybrid-20261024/preserved-products.json) 给出完整路径/大小/SHA，供后续性能测量。

## 6. 磁盘测量与基线对照

完整成功扫描 120 次、缺失/不完整 33 次。整轮已观测峰值 68778053632 B（64.055 GiB），采样起点 2026-10-23T23:54:17.016531+08:00。这是离散观测下界；未补造超时读数，跨阶段扫描不强行归类，全盘df变化不冒充本根占用。

| 阶段 | 本次GiB | hybrid GiB | 全静态+BOLT GiB | 本次完整样本 |
|---|---:|---:|---:|---:|
| ordinary-build | 43.687 | 34.636 | 161.026 | 44 |
| ordinary-install | 58.054 | 58.522 | 205.561 | 8 |
| BOLT | 64.055 | — | 218.040 | 20 |
| cache-release | 59.491 | — | — | 1 |
| native-conversion-install | 50.951 | 66.696 | 224.718 | 35 |
| platform-post | 44.229 | 60.834 | 217.610 | 6 |
| packaging | 39.256 | 56.773 | 219.843 | 5 |

| disk-report时点 | BOLT自有GiB（含缓存正增量） | 缓存正增量GiB | 全盘可用GiB |
|---|---:|---:|---:|
| begin | 0.000 | 0.000 | 27.580 |
| tool-built | 3.783 | 1.148 | 23.792 |
| pipeline | 4.367 | 1.148 | 23.208 |
| post | 3.220 | 0.000 | 48.266 |

post自有占用降低包含缓存正增量在删除后归零，不能说工具或候选被清理。与hybrid的整轮峰值差受BOLT增量与cache-release共同影响；全静态基线另有2.065GiB中断链接临时残留、不同资源限制和续跑历史。不能把全部差值归因于单一优化，亦不能把20GiB缓存释放直接等同于整轮峰值降幅。[disk-comparison.json](../../tools/bolt/results/bolt-on-hybrid-20261024/disk-comparison.json)。

## 7. RPM 大小（字节）

| RPM | hybrid | hybrid+BOLT | 差值 |
|---|---:|---:|---:|
| clang-22.1.8-1.x86_64.rpm | 65571169 | 78633217 | +13062048 |
| clang-debuginfo-22.1.8-1.x86_64.rpm | 617939805 | 326909681 | -291030124 |
| clang-devel-22.1.8-1.x86_64.rpm | 4098705 | 4099169 | +464 |
| clang-devel-debuginfo-22.1.8-1.x86_64.rpm | 5727969 | 5728097 | +128 |
| compiler-rt-22.1.8-1.x86_64.rpm | 3722589 | 3720689 | -1900 |
| compiler-rt-debuginfo-22.1.8-1.x86_64.rpm | 1288441 | 1288421 | -20 |
| libllvm-22.1.8-1.x86_64.rpm | 23651157 | 23651713 | +556 |
| libllvm-debuginfo-22.1.8-1.x86_64.rpm | 198054017 | 198054137 | +120 |
| libomp-22.1.8-1.x86_64.rpm | 373521 | 373397 | -124 |
| libomp-debuginfo-22.1.8-1.x86_64.rpm | 1141925 | 1142353 | +428 |
| libomp-devel-22.1.8-1.x86_64.rpm | 25501 | 25489 | -12 |
| lldb-22.1.8-1.x86_64.rpm | 5453089 | 5453261 | +172 |
| lldb-debuginfo-22.1.8-1.x86_64.rpm | 70085437 | 70084113 | -1324 |
| lldb-devel-22.1.8-1.x86_64.rpm | 5603465 | 5602649 | -816 |
| lldb-devel-debuginfo-22.1.8-1.x86_64.rpm | 54165477 | 54166301 | +824 |
| llvm-22.1.8-1.x86_64.rpm | 41689293 | 41694641 | +5348 |
| llvm-debuginfo-22.1.8-1.x86_64.rpm | 347383729 | 347380421 | -3308 |
| llvm-debugsource-22.1.8-1.x86_64.rpm | 43664945 | 43651577 | -13368 |
| llvm-devel-22.1.8-1.x86_64.rpm | 5326957 | 5326953 | -4 |
| llvm-devel-debuginfo-22.1.8-1.x86_64.rpm | 421021 | 421013 | -8 |
| llvm-static-devel-22.1.8-1.x86_64.rpm | 60440909 | 60450105 | +9196 |
| python-clang-22.1.8-1.x86_64.rpm | 36301 | 36301 | +0 |
| llvm-22.1.8-1.src.rpm | 340927600 | 350697433 | +9769833 |

这是压缩包大小比较，不等于逐文件一致性认证；BOLT会改变clang实体、debug信息包及源码包，本任务未要求两次RPM字节一致。[rpm-size-comparison.json](../../tools/bolt/results/bolt-on-hybrid-20261024/rpm-size-comparison.json)、[rpm-identities.json](../../tools/bolt/results/bolt-on-hybrid-20261024/rpm-identities.json)。

## 8. 准备处理、范围与复核

1. 宿主PATH无ninja：复制现有Tizen ninja到本次目录，仅查询复制的图。
2. 首轮解析引用旧7补丁SOURCES，缺hybrid Patch7：原失败证据保留，改用本次完整导出专用SOURCES，五项重跑PASS。
3. 证据脚本相对Path.parent曾算错输出目录；在产品操作前改为绝对路径。验证控制器目录计算也在运行前静态核对纠正。
4. 大量Source1005文本证据采用tar.gz归档，保留完整命令、日志和时间文件，避免仓库散落数万个小文件。

没有改变源码门禁、profile、白名单、基线安装或后处理；没有在历史根执行cmake/ninja，没有删除历史目录，没有推Gerrit或创建sandbox。构建与验证均无失败重试。完整证据 [final-audit.json](../../tools/bolt/results/bolt-on-hybrid-20261024/final-audit.json)、[validation-controller.json](../../tools/bolt/results/bolt-on-hybrid-20261024/validation-controller.json)；本报告及证据仅提交GitHub bolt-v4。

## 9. 记录边界与平台提示

- 最长两次成功du采样起点之间相隔 1620.0 秒（约27.0分钟），位于普通链接期；所以本次64.055GiB是已观测值，不是连续上界。/home全盘最低可用 21758730240 B（20.264GiB），没有低于20GiB。详见 [sampling-limitations.json](../../tools/bolt/results/bolt-on-hybrid-20261024/sampling-limitations.json)。
- 平台有普通工具缺少build-id的warning；app-rootstrap-checker还打印了多spec路径的 `error: query of specfile ... libcxx-runtimes.spec` / `llvm.spec failed, can't parse`，随后 `SUCCESS: app-rootstrap-checker done`。docs/53 hybrid基线存在相同原文。本次GBS退出0，五项独立Tizen解析和全部BOLT门禁PASS；不把这些平台文本当作不存在，也没有修改检查器。双边行号/原文见 [platform-checker-messages.json](../../tools/bolt/results/bolt-on-hybrid-20261024/platform-checker-messages.json)，完整日志见 [rpm-build.log](../../tools/bolt/results/bolt-on-hybrid-20261024/rpm-build.log)。
- GBS默认 `%clean` 清理了本轮BUILDROOT；保留了整个新chroot、BUILD、RPM及products。没有手动删除任何历史根、目录或保全资产。构建结束时本根无残余挂载。磁盘构建采样结束后才复制products、执行对象验证，这些后续写入不计入整轮构建峰值。
- 最终RPM的 `/usr/bin/clang-22` 文件摘要与candidate SHA相同，见 [packaged-clang-identity.json](../../tools/bolt/results/bolt-on-hybrid-20261024/packaged-clang-identity.json)。post原始JSON见 [post-result.json](../../tools/bolt/results/bolt-on-hybrid-20261024/post-result.json)。
- 本轮不做性能测量；candidate与本次ordinary已保全，后续由用户安排。验证使用本树ordinary副本，不把它与docs/53的另一轮普通clang做跨构建SHA相等要求。


## 10. 2026-10-24：授权更新统一 sandbox 分支

用户明确授权将已验证的 hybrid+BOLT 合并提交推到唯一的 BOLT sandbox 分支。本节更新此前“未推 Gerrit”的历史状态；不修改源码、不重做构建或解析、不操作 QB。

### 10.1 推送前核对

| 核对项 | 实际值 / 结果 |
|---|---|
| 源工作区 HEAD | `aa637c1b4a0f9ea9f6f0317cf035126eba85aeb7`，tracked/untracked 均干净 |
| tree | `1c52e7922a5ae112b96dc18c297ed2dff58aa218` |
| 父提交 hybrid | `6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2` |
| 再上一层 | `67619ec8bbbac7238a6cfc33a481ccfbcd12206f` |
| BOLT 作者和提交者 | 均为 `Hao Lin <hao.lin@samsung.com>` |
| BOLT Change-Id | `Ic98eab90cc017f127a66e1729b44fab8b8e8fb41` |
| hybrid Change-Id | `I28171720d5bbbf9eaf491cdafc0aee0b43f9cd06`，原提交对象保持不变 |
| 推送前远端 | `3d3b4bf564fd8edec793e49e6de75b5fa7007d16`，符合精确租约 |
| 既有认证 | export-result.json 的 --commit 为 aa637c1，退出 0；five-parse/matrix.json 五项均 PASS，rpmbuild/rpmspec 均退出 0 |

上述认证沿用本报告第 1–9 节的同一提交结果，没有重新运行。原始核对与提交对象见 [precheck.json](../../tools/bolt/results/bolt-on-hybrid-20261024/sandbox-push-20261024/precheck.json)、[BOLT commit](../../tools/bolt/results/bolt-on-hybrid-20261024/sandbox-push-20261024/aa637c1b.commit.txt)、[hybrid commit](../../tools/bolt/results/bolt-on-hybrid-20261024/sandbox-push-20261024/6e9d4f2b.commit.txt)。

### 10.2 推送与远端复核

源工作区 origin 为 `ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm`。执行命令：

```sh
git push --force-with-lease=refs/heads/sandbox/lhmax2025/bolt_pgo:3d3b4bf564fd8edec793e49e6de75b5fa7007d16 origin aa637c1b4a0f9ea9f6f0317cf035126eba85aeb7:refs/heads/sandbox/lhmax2025/bolt_pgo
```

退出码 0，合并 stdout/stderr 原文如下（进度回车在 Markdown 中显示为换行；原始字节保存在链接文件）：

```text
remote: 
remote: Processing changes: refs: 1        
remote: Processing changes: refs: 1, done            
To ssh://review.tizen.org:29418/platform/upstream/llvm
 + 3d3b4bf564fd...aa637c1b4a0f aa637c1b4a0f9ea9f6f0317cf035126eba85aeb7 -> sandbox/lhmax2025/bolt_pgo (forced update)
```

推送前 `git ls-remote origin refs/heads/sandbox/lhmax2025/bolt_pgo`：

```text
3d3b4bf564fd8edec793e49e6de75b5fa7007d16	refs/heads/sandbox/lhmax2025/bolt_pgo
```

推送后同一查询：

```text
aa637c1b4a0f9ea9f6f0317cf035126eba85aeb7	refs/heads/sandbox/lhmax2025/bolt_pgo
```

`git log --reverse --format='%H %s' 67619ec8bbbac7238a6cfc33a481ccfbcd12206f..aa637c1b4a0f9ea9f6f0317cf035126eba85aeb7` 列出恰好两个提交：

```text
6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2 cmake: use hybrid LLVM linkage on x86_64
aa637c1b4a0f9ea9f6f0317cf035126eba85aeb7 packaging: optimize x86_64 clang with BOLT
```

推送无警告、无拒绝；没有推 refs/for、创建分支或删除构建根。原始 [命令](../../tools/bolt/results/bolt-on-hybrid-20261024/sandbox-push-20261024/command.txt)、[输出](../../tools/bolt/results/bolt-on-hybrid-20261024/sandbox-push-20261024/push-output.txt)、[退出码](../../tools/bolt/results/bolt-on-hybrid-20261024/sandbox-push-20261024/push-result.json)、[远端结果](../../tools/bolt/results/bolt-on-hybrid-20261024/sandbox-push-20261024/remote-after.txt)已保全。

供用户启动 QB 的软件包写法：`platform/upstream/llvm@aa637c1b4a0f9ea9f6f0317cf035126eba85aeb7`。本轮到此停止，QB 由用户启动。
