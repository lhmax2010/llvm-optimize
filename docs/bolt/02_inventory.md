# 02 BOLT v4 只读盘点

日期：2026-10-12（Asia/Shanghai）。开场主仓库与origin/main为fb833a4c8ee1ece09027a0d5d04e254ea9899a5f；LLVM HEAD为f111162e94aa48ed367c9d2c039456c70e7160ae。证据E=`/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013`。本文所有“现存”均为本轮只读实际检查；不表示新cb679968产物已经认证。

## 1. 开场输入封存

必读docs/README、STATUS、12–21、46和两候选补丁已复制到E/inventory/opening-*；逐字SHA登记在opening-inputs.json。主工作区已有归档会话的docs/47与gbs配置修改，未写入。用户规定中文提交覆盖docs/README的英文提交惯例。

| 文件 | 字节 | 开场SHA256 |
|---|---:|---|
| `/home/linhao/Toolchain/development/llvm-optimize/docs/46_review_round3_package.md` | 27441 | `942eae8deaa9ffe15e1b56eaca99b3a1f99b0c85cc7843fc08e06f85c7fa605c` |
| `/home/linhao/Toolchain/development/llvm-optimize/llvm/packaging/llvm.spec` | 20665 | `95887b2d060b38d5ef8f56936f7481a03d131f9d26432180a68e02ec95f0dda5` |
| `/home/linhao/Toolchain/development/llvm-optimize/patches/archive-index-fix/ps3/0001-packaging-fix-llvm-static-devel-with-ThinLTO.patch` | 50284 | `1293f6982c87cfbeefe91aa08e92a7d1b72a129f716417f8c8cee61693c463c6` |
| `/home/linhao/Toolchain/development/llvm-optimize/patches/archive-index-fix/ps3/llvm-static-archives-native.py` | 43799 | `014fd32f309bc0be80471eebf8a4a3cf50a5656ce3a2584e4bbdfb9a05a9affd` |
| `/home/linhao/Toolchain/development/llvm-optimize/patches/llvm-strip/ps2/0001-packaging-use-llvm-strip-for-x86_64-archives.patch` | 2803 | `aab2cfd1ad3fb58bfe44cdbdda50bbe67d5343b29a6a6d598408d3bb96620e88` |

356627 PS3候选format-patch提交f0e9777011a6ff5dbdd416899848d69edb70db27：新增Source1005与安装阶段原生归档转换，只作用x86，工具构建/链接不变。356639 PS2候选提交db23b26079776684d09c620ae614a59cd40007a0：复制Tizen __strip_install_post，仅归档参数改为/usr/bin/llvm-strip，brp-strip仍用默认/bin/strip。两者是开场本地候选身份，不冒充已上传Gerrit patchset。后续更新不得自动替换本次基线。

## 2. 现存产物逐项登记

R1=`W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0`；W为主工作区。历史clang/profile均来自f111162e配方，BOLT工具是docs/15在R1增量启用bolt项目的实验构建产物。RPM基线是docs/13最终RPM解包的clang，不是旧公开动态快照。历史带relocs ELF来自docs/14单clang重链；去debug输入来自docs/15。v1来自docs/16；v2来自docs/20附录D。

| 名称 | 实际绝对路径 | 字节 | SHA256 | 现存 |
|---|---|---:|---|---|
| profile-v2 | `/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-aarch64-v2-20260921/profile-work/merged-v2.fdata` | 171232190 | `d9b132f9430dfed32e080c65b4422bd76eba4a9c2101a2b18a7f66c94133b326` | 是 |
| clang-v2 | `/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-aarch64-v2-20260921/optimized-v2/bin/clang-22` | 218881120 | `f26b65625897189bd38ae02eb8b4cf5854ada84c08be9be3943f241dea647637` | 是 |
| clang-v1 | `/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-final-20260918/optimized/bin/clang-22` | 215899856 | `d6538b5ee1fdc429008b4481b651f994e354eabd55853666a0a9f0da03692e63` | 是 |
| clang-relocs | `/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/bolt-relocs-6a5e8e81bccb/clang-22` | 3560474952 | `6bfc85a8cce9952c4bcbea1a4ea169fb6199c379c18527df7d349f375e52caaf` | 是 |
| clang-stripped-input | `/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-measurement-20260918/run/stripped/bin/clang-22` | 226730672 | `eccfb075bc3b2a6ca2bda5a2a6e68f6a29ba48b5586cb603f4b46080f656013e` | 是 |
| clang-rpm-baseline | `/home/linhao/Toolchain/development/llvm-optimize/temp/toolchain-baseline/usr/bin/clang-22` | 139929464 | `3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c` | 是 |
| llvm-bolt | `/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-bolt` | 648678768 | `1da7bb735f7bc1afab9a863154260699b0b0f88c6fd05b99231dd21ef653fd5a` | 是 |
| perf2bolt | `/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/perf2bolt` | 648678768 | `1da7bb735f7bc1afab9a863154260699b0b0f88c6fd05b99231dd21ef653fd5a` | 是 |
| merge-fdata | `/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/merge-fdata` | 11891568 | `9a725e368f39cc9fbaaf32fe8698ea3e1d120fee7de565373e376e3fc759a6a7` | 是 |
| llvm-strip | `/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-strip` | 98946648 | `64503737dd079f750cfea7b427582682657df2c6a4cff2f394be46336a0d89aa` | 是 |
| GNU-strip | `/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0/usr/bin/strip` | 167536 | `ee80ec36060dc467f57a3c7ae7155affbfcd39cec254892cffa45096a9f5e7ec` | 是 |
| eu-strip | `/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0/usr/bin/eu-strip` | 347328 | `96b2656d473cbac24283c950fa55d842c21dcdae9b6d49cd18f4c89054a86738` | 是 |
| objcopy | `/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0/usr/bin/objcopy` | 167528 | `88f57a67278e0031ed2ce91569955d0d3d618af43821997b095fac2c80ab7bbf` | 是 |
| host-strip | `/usr/bin/strip` | 166568 | `0d980587ada7ab12193f39271f060d5663aa2f289b0e80d2a0274ce7306e4e42` | 是 |
| host-objcopy | `/usr/bin/objcopy` | 166536 | `9276e918e3c26d3aa7ef9dd2232cd8ac692f03d3c1f270bfa5144a2b5492b713` | 是 |

perf2bolt是指向llvm-bolt的相对软链接，不是独立Ninja目标。merge-fdata独立目标；生产使用现成profile不需要运行perf2bolt/merge-fdata。llvm-bolt自报22.1.8、BOLT revision unknown（历史docs/15）；因此以工具文件SHA与构建来源钉身份。

## 3. spec差异与profile适配判定

E/inventory/target-spec.txt取git对象cb67996861d070d68fec2b4c623eed7d20ba2e23；workspace-head-spec.txt取f111162e；spec.diff完整保存。开场工作区spec的6→4/6→4/2→1既有并发差异单独封存，不能冒充HEAD原文。

| 项 | cb679968 | f111162e | 对重链/profile的含义 |
|---|---|---|---|
| LLVM/clang库 | x86显式LLVM_LINK_LLVM_DYLIB=OFF、CLANG_LINK_CLANG_DYLIB=OFF；仍构建共享库 | 未显式设置这两个链接选项；历史cache/ELF实测OFF、静态组件 | 同为LLVM库静态形态，不能仅凭spec文字认定二进制相同 |
| 编译器 | x86明确clang/clang++，未定义_toolchain时添加BR并定义clang | %__cc/%__cxx，未定义_toolchain没有前置BR块 | 实际driver、安装包与宏环境可能不同 |
| 优化flags | 强制O3/ThinLTO只在x86；先删除更长stack-protector选项；删除-fno-inline-functions；加-Wno-unused-command-line-argument | 所有arch；先删短stack-protector选项；保留-fno-inline-functions；无该末尾诊断flag | 顺序会影响含长选项的字符串；必须检查实际展开flags，不能直接假定语义一致 |
| 链接 | toolchain定义时lld、ThinLTO、function/data sections、gc-sections、热cache | 对应设置相同 | 实际对象、driver、flags、cache及rsp须登记 |
| 项目 | clang;lldb;clang-tools-extra;lld;compiler-rt;openmp | 同左 | 均不启用bolt项目，spec正常构建不会提供llvm-bolt |
| 子包 | static-devel保持发布 | 同左 | 不撤包、不改归档方案 |

两提交差异另含libcxx/libcxxabi与独立runtime配方（14文件，556增/14删），LLVM/clang/bolt源目录没有差异；这缩小风险，仍不能取代实机profile门禁。现有profile v2可读、171232190B、ARM13+AArch6410，且历史输入匹配通过；**能否直接用于cb679968产物：UNKNOWN，尚无该配方完成构建的对应ELF，周三必须实测≤5%失配。** 不要求今晚重训，也不认定一定不可用。

## 4. 只读构建树登记

没有chroot、cd进根、ninja查询或任何构建。只从宿主绝对路径读取cache/图/ELF；缺spec位置如实记缺，不能据此断定整个根无spec。

| 根（相对W/temp） | cache / Ninja图 | build/bin/clang-22 | 来源/续跑资格 |
|---|---|---|---|
| gbs-root-x86_64-debuginfo-j4-v2 | 存在；cache 23848f0d…，图133b142f… | 1793477048B，d25e9960… | f111162e历史完整树，已增量加bolt；仅用来读历史工具，不能代cb679968 |
| gbs-root-x86_64-archivefix-v2 | 存在；cache d9970d73…，图81216d3d… | 同历史clang SHA | f111162e归档修复旧完整树，项目列表无bolt；归档会话持有锁，不续跑 |
| gbs-root-x86_64-archivefix | 存在；cache26b69aa3…，图d832ff11… | 指定位置缺失 | 旧/不完整现场，不选 |
| gbs-root-x86_64-debuginfo-j4 | 指定位置缺失 | 缺失 | 不选 |

完整SHA与绝对路径：E/inventory/build-trees.json；cache副本同目录。**周三应使用归档会话周二夜新产出的cb679968+指定PS3/PS2完整x86树，当前路径UNKNOWN。** 必须先取得实际树、源码/补丁/spec/cache/宏/driver/rsp与成功完整构建日志，锁移交后才续跑；不能套用上述旧根。

## 5. RPM后处理实际脚本

R1内rpm-build历史版本4.14.1.1-1.4.x86_64。find-debuginfo、macros、Tizen宏、brp脚本已逐字复制到E/inventory/rpm-*，供后续同SHA认证。docs/46在archivefix-v2根核查相同宏；本轮读取R1版本，周三新根须重新核查。

- Tizen __spec_install_post依次：有__debug_package才调__debug_install_post → check-buildroot → __os_install_post → ISU/可选检查。
- __os_install_post：brp-compress → 没有_rpm_strip_disable时__strip_install_post → brp-python-hardlink → find-docs。brp-strip条件为没有__debug_package，传%__strip（默认/bin/strip）；实际操作strip -g，即--strip-debug。静态归档处理独立，不影响clang；comment-note行被注释。
- find-debuginfo先按objdump节区筛选：debuglink跳过；debug存在才选；只有gnu.version则提示already stripped并跳过。-p和-l只分配输出文件列表，不排除处理对象。
- 被选中的文件先debugedit -i（可能重算build-id），后eu-strip --remove-comment -f DEBUGFILE ELF；默认STRIP_DEFAULT_PACKAGE不是binutils。-g只在相应MIME为EXE/DSO时加-g；-r对应--reloc-debug-sections；--strip-option全局生效。binutils分支是cp→strip --remove-section=.comment→objcopy --add-gnu-debuglink。-m会另外注入.gnu_debugdata。不能将debugedit或其他objcopy写入视为天然安全。
- 历史完整构建实际调用：find-debuginfo.sh -j4 --build-id-seed 22.1.8-1 --unique-debug-src-base llvm-22.1.8-1.x86_64 -S debugsourcefiles.list BUILD。今晚保持串行-j1，其余一致；新宏环境另冻结。spec原release分支去掉-g并覆盖debug_install_post，但x86前置_toolchain定义的时序须看实际rpm展开，不凭布尔名称推断。
- 无按clang路径排除的原生选项。_rpm_strip_disable/--strip-disable是全包级，STRIP_KEEP_SYMTAB仅Kconfig分支；不能用于只保护clang。可验证“预先去debug→BOLT后无debug→选择器跳过”，但这不是文件排除API，还须防护brp-strip并做完整RPM验证。

## 6. 锁与资源协作

开场归档会话使用W/temp/review-round4-20261012/hold_lock.py，O_CREAT|O_EXCL同时占用W/temp/.llvm-optimize-exclusive.lock和W/temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock；记录pid/session/start；只有拥有者记录匹配才删除。锁记录与脚本只读复制到inventory/archive-*。以后任何重任务须由归档会话明确释放/移交、只读确认进程及根身份后再按该机制取得两锁；禁止删除“看似过时”锁。本轮未获取、等待、释放或发信号干扰这些锁。

只读盘点也在独立2GiB/swap0 scope、nice19/ionice3执行。inventory-fixed-scope实测88.7s、peak835477504B、OOM0，回收inactive/dead。初次辅助入口因相对脚本路径在证据cwd解析错误退出2；实际盘点未启动，scope已回收。仅改为绝对路径，门禁不变；失败日志保留inventory-scope。没有实验OOM或宿主低内存事件被掩盖。
