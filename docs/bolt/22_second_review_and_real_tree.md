# 22 续跑十二：第二轮评审修复与真实树演练

STOP；新本地源 d08b54da276102c2b607fbddd07966111f5147cd；sandbox 未推；第六步未实际执行（overlay 权限不足）。第七步捕获入口同类第二次准备失败后停止。

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

## 4 真实产物 PASS；5 本地源提交 PASS

普通7df与候选4ec SHA绑定，新安全属性全部相同。RELRO flags4/vaddr136891248/filesz3004136/memsz3007632；DT_BIND_NOW均false、W_X_LOAD均false；dynsym和版本绑定各65241条、verneed43条，全部原文以security-properties xz公开。tiny三目标完整对象一致；20小RPM根的副本分别通过新post反向、compare-root及完整post（SHA/alias/security/tiny），故意加入llvm-bolt被拒。构造110任务通过，编号一致的111任务含普通Support被拒。没有重新生成候选。

源提交d08b54da276102c2b607fbddd07966111f5147cd，父b7e61fb92b34795868230e4f9cee8e3ec65496f6，tree 40a569a2e001dcf11f5cf5e9239211001be9d7a3；作者/提交者均Hao Lin。spec/helper/profile的SHA和字节、0003补丁、完整索引apply/tree一致证明见draft-manifest。该内容锁定用于第六步，尚未推sandbox。

## 6 真实树演练 NOT RUN：overlay 权限

先独占共享锁，在本轮E内四个空目录上做overlay权限探针，没有访问docs/35下层树。命令是sudo -n /bin/mount -t overlay overlay -o lowerdir=<own empty>,upperdir=<own>,workdir=<own> <own scratch.overlay-probe>。rc1原文：

```text
sudo: a password is required
```

按PM专门许可将第六步记NOT RUN，其余继续；没有复制树或从零构建依赖闭包，没有私有namespace或host bind。overlay未挂成功，无卸载遗留；锁释放，own探针目录保留。没有实际进入/挂载下层，因此下层CMake配置资格、全BUILD前后清单及SHA、普通最新状态、真实工具dry-run/build、树内工具/候选、匹配统计、完整安装/后处理及实物反向检查全NOT RUN，不能以早期历史快照或小根替代。没有上层真实构建数据可保留。原文argv/mountinfo/lock与资源见overlay JSON和stop-evidence。

## 7 实际post脚本采集准备失败，STOP

使用根内rpmbuild -bi --short-circuit，所有topdir/builddir/buildroot/tmp均为本轮专用位置；原RPM前导保持PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin，which clang=/bin/clang、clang++=/bin/clang++。没有使用rpmspec --eval取得post。三次采集准备过程原文不覆盖：

1. Source0未备，rpmbuild在启动脚本前报告 `llvm-22.1.8.tar.gz: No such file or directory`。一次“漏备Source输入”修正：链接原SOURCES的已有文件，helper/profile使用本轮相同内容。只读原件，链接清单公开。
2. 初次捕获入口只定义__spec_install_shell，实际__spec_install_cmd却引用___build_cmd。该定义只改shebang，/bin/sh仍执行；仅在本轮空目录运行rm/mkdir前导，随后cd llvm-22.1.8失败，没有执行cmake/ninja/安装/post。一次捕获入口修正：根据根内macros原文改为覆盖__spec_install_cmd，保留___build_args实际-e。
3. 修正后wrapper确实保存了基线debug完整生成脚本、未执行脚本体并返回0；rpmbuild仍进入包文件校验，因未安装普通文件返回1。采集驱动先要求整个rpmbuild返回0，未接受已保存的partial脚本。同属捕获入口/返回契约准备的第二次失败，立即停止，不再换判据或重跑。

最终错误原文含：

```text
File not found: .../post-capture-final/BUILDROOT/usr/bin/llvm-objcopy
File not found: .../post-capture-final/BUILDROOT/usr/bin/llvm-strip
```

这是脚本采集工具准备失败，不是已证明helper/spec产品门禁失败。partial baseline脚本只作失败诊断，不认证debug/release追加链逐字相同。新源debug脚本和release两脚本均未取得；第七步认证NOT RUN、采集流程FAIL。第二步canonical片段与OFF展开PASS仍有效，但不替代该项；第六步实际debug执行证明亦缺失。未来需在捕获脚本时停止包处理，不能把缺失实物假称安装成功。本轮不再试。

## 最终逐项表

|项目|状态|证据路径（仓库内）|
|---|---|---|
|1a 历史dry-run格式/TF|PASS|tools/bolt/results/review2-historical-dry-run.txt、review2-historical-format.json|
|1b 根内极小工程|PASS|review2-toy-result.json、review2-toy-*.stdout/stderr/combined.txt、first-evidence包|
|1c 22RPM/47 CMake|PASS|review2-rpm-cmake-result.json、first-evidence包|
|2 helper/spec修复、OFF展开|PASS|bolt_helper.py、review2-draft.spec、review2-macro-result.json|
|3 原146保留+新增56|PASS|test_second_review.py、review2-tests.txt、review2-implementation-result.json|
|4 ordinary/candidate新安全/tiny/双根post|PASS|review2-real-security.json、review2-security-properties.json.xz、review2-real-gates.json|
|5 本地提交/0003/apply/tree/镜像|PASS|patches/bolt/draft-manifest.json、0003-clang-bolt-second-review.patch|
|6 真实树overlay演练|NOT RUN|review2-overlay.json、stop-evidence包；无权限，没有复制替代|
|7 脚本采集流程|FAIL|review2-post-scripts.json、post-baseline-debug-partial.sh及三次原文在stop-evidence包|
|7 两模式实际post链认证|NOT RUN|仅partial基线脚本，未完成逐字对照|
|8 文档/保护/raw发布|PASS|本22、STATUS、21补充、review2-protection.json及raw索引|
|sandbox推送|NOT RUN|前提未全部PASS，未尝试推送；只读远端仍b7e61fb|

真实dry-run的范围：历史原流128行、126任务（105对象/8库/2可执行/TF2/其他9），stderr来源不可从采集器合并原件还原，另2条wrapper行；本次构造的当前计划110 BOLT=102/7/1，另可TF0或2，均夹具认证。第六步真实110/112任务、是否stderr、构建后最新原文均NOT RUN，不能当作实际证据。1b stderr三种case均空。

历史4ec匹配统计见fallback-candidate.json，本轮未重写；第六步新树统计、耗时、工具/候选SHA与历史对照均NOT RUN。没有把“同量级”变成既成结果。

## 资源、保护与纠正记录

下表wall为scope墙时；VmHWM仅列采样到的最大进程高水位，不等于完整进程全集的绝对峰。memory.peak为cgroup实际累计峰。全部scope swap0、nice/ionice按4/16GiB类别；入口与运行MemAvailable逐样本在raw，scope均回收。

|阶段|状态|wall s|cgroup峰 B|采样最大VmHWM KiB|
|---|---|---:|---:|---:|
|review2-history|PASS|1.525|13545472|16284|
|review2-toy|PASS|4.030|306286592|21668|
|review2-rpm-cmake|PASS|21.057|988975104|37320|
|review2-tests|PASS|3.526|86982656|45632|
|review2-macros|PASS|1.519|39698432|22512|
|review2-real-security|PASS|3.524|324136960|319944|
|review2-real-gates|PASS|8.058|876138496|109804|
|review2-overlay-admission|PASS|1.023|14536704|12644|
|review2-post-scripts|FAIL|1.024|30298112|12608|
|review2-post-scripts-corrected|FAIL|1.023|31268864|12632|
|review2-post-scripts-final|FAIL|1.026|31305728|12624|
|review2-protection|PASS|16.542|1074638848|96984|

第六步各真实构建段资源/磁盘高水位均NOT RUN；探针磁盘可用424225906688 B。最终原根可用50448162816 B、E可用424224243712 B，没有>10GiB单次写入；原缓存47987文件/96881772832 B不变，禁止树cache/ninja SHA与源码元数据、22RPM全SHA/大小及归档证据元数据均PASS。原clang与历史4ec保持。W tracked仍仅原gbs_llvm.conf改动，未写W/llvm。源新提交tracked clean，镜像相同；全局git配置未改。

查找更正5项及一次范围过宽rg中断详见review2-corrections.json。该广域发现未执行ARM命令或写ARM，但不能以未出现ARM路径的输出证明没有遍历别的目录。之后只查本会话目录。产品准备：漏备Source一次修正；捕获入口修正一次后第二次失败STOP。没有第三次捕获纠正，没有门禁豁免。

sandbox仅只读查询，实际仍b7e61fb92b34795868230e4f9cee8e3ec65496f6。没有推refs/for或tizen_base；新d08源尚未供Quickbuild，不能用本轮不完整认证宣称可交付。所有新提交author/committer与Signed-off-by为Hao Lin <hao.lin@samsung.com>。
