# 22 续跑十二：第二轮评审修复与真实树演练

当前状态：第一步证据PASS；新源提交未生成；sandbox本轮未推；第六步尚未执行。

基线b7e61fb92b34795868230e4f9cee8e3ec65496f6（父a1410e3d），历史候选4ec07159…、profile、BOLT参数与重链方式保持。新提交作者/提交者统一Hao Lin <hao.lin@samsung.com>，只用单次-c，不改全局配置。原树禁CMake/Ninja/-P；只写本轮E/根内专用目录及B，保护归档证据/22RPM/ARM根；资源/锁/磁盘与准备错误停规则沿用。overlay仅第六步按本次授权用于其他完整树的只读下层；不能扩大到原禁用树。

## 1a 历史格式与TF证据

定位E历史bolt-measurement-20260918/incremental-final/ninja-dry-run.log，SHA90fe8cc9e82ef82f1df2a60defd6a00cd9de2655af0e4df564e84c77440d9d84。原始128行，126进度任务从1连续到126、总数恒126；每行有采集器时间戳，另2行Running as unit与chroot包装器信息，原件无法分别恢复stdout/stderr来源。TF原文如下：

```text
2026-09-18T12:31:49+08:00 [1/126] Building C object lib64/tf_runtime/CMakeFiles/tf_xla_runtime.dir/tf_xla_runtime_dummy.c.o
2026-09-18T12:31:49+08:00 [5/126] Linking C static library lib64/libtf_xla_runtime.a
```

历史分类：BOLT CXX对象105、静态库8、可执行2、TF2、其他9。历史runtime ON/双后端/merge-fdata等选项不同，只证格式/TF，不能当本轮允许计划；原流时间戳和非进度行必须拒，去前缀派生126任务也有本轮之外任务，应在夹具中明确预期拒绝。

## 1b 极小工程：主理解成立，实际重新生成计数为0/1

在RPM根内新专用toy目录配置/构建静态C库，调用同版本/bin/cmake、/bin/ninja，原RPM环境前导后cd到toy目录。没有对原LLVM树运行CMake/Ninja。toy仅用空C_FLAGS与STATIC_LIBRARY try_compile隔离链接依赖，不改变LLVM参数。stdout/stderr分开且另存按读取顺序合并版，wrapper环境trace另存。所有命令rc0。

- 全部最新：stdout `ninja: no work to do.\n`，stderr空。
- touch CMakeLists后：stdout `[0/1] Re-running CMake...\n`，stderr空；只显示这一行，没有后续真实任务。核心“dry-run看不到后续任务”的PM理解成立，但不能写死例子中的1/1，门禁应按单行描述专门拒绝。
- 显式重配file(WRITE)后：生成源SHA不变、mtime刷新；stdout出现 `[1/2] Building C object CMakeFiles/probe.dir/anchor.c.o` 与 `[2/2] Linking C static library libprobe.a`，stderr空。

16GiB/swap0/nice15/ionice3、独立共享锁约4秒，已释放并卸载proc/回收scope；原文与版本、argv、PATH/which、CMake产物在first-evidence包。这里是极小机制实验，不是第六步真实树演练。

## 1c 普通RPM CMake审计

22RPM逐个SHA绑定、实际查询文件列表并与20保存包头相同，共47个.cmake：clang5、libomp-devel1、llvm-devel41，其他0。逐个提取内容SHA同包头。旧大写BOLT规则0命中，新大小写敏感LLVMBOLT/llvm-bolt/perf2bolt/llvm-boltdiff/merge-fdata规则0命中。本基准不能声称b7 post会误拒普通CMake；新定向规则仍按PM实现。完整清单/内容在review2-rpm-cmake-result与first-evidence。

查找记录：第一次rg默认受ignore影响未列历史temp，随后按docs/15定位目录使用--no-ignore；一次docs/35文件名误猜，已先rg定位真实35_archive_fix_v2_final.md。均为产品操作前查找更正，不计准备纠正次数。本轮产品准备错误0。

## 2–3 实现与夹具 PASS

202/202（原146方法全部保留，新增56），2.463秒；4GiB scope 3.526秒。独立review-tool-descriptions JSON核对白名单，不从生产常量造全集。真实历史流按时间戳/包装器和旧配置外任务预期拒绝；toy三个真实输出亦绑定断言。TF成对计划112任务，配置刷新2，BOLT102对象+7库+1可执行；真实构建复核允许警告与restat总数缩小，保持批准清单、连续f和TF归档SHA不变。描述、返回值与进度错误均有负例。

call改waitid WNOWAIT保持组长、killpg后10秒清组/1秒非阻塞回收、SIGCHLD恢复默认、proc namespace自检/枚举及读取失败关闭、Z/X多线程视为活；原错标签先于清理错，成功回收后读日志失败不杀组，KBI/SystemExit保持。测试在返回时立即判后代已退出，随后两个心跳周期不再更新。RELRO现编小程序字节移动/缩小/清零拒绝，dynsym五元组/原始shndx定义类别、版本提供者、DT_BIND_NOW/W+X与NOBITS等负例通过。post复用不算SHA的失败关闭遍历与定向串，根内链接正常、悬空/错误/特殊文件拒绝。@rsp立即拒绝。

旧断言改动逐项理由见review2-implementation-result.json，原有146方法无删减。debug/release各18段，BOLT关闭时均与cb679968展开逐字节相同；canonical mini与源spec追加片段逐字相同且位于install/files之后。此处尚不是第七步实际post脚本证据。rpmspec无--without选项，沿用已认证的rpmbuild实际宏值兼容方式。源与B镜像逐字相同；源尚未提交，第五步前待真实安全门禁。
