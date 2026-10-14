# 15 原 RPM 环境临时验证与续跑记录

2026-10-14。第一步临时配置 **PASS**；后续原树恢复与候选尚未执行。当前生产草案不改，源码提交仍 d6ddbff5ba74bfb420b357b5b6ba9ed300971bb4，父 cb67996861d070d68fec2b4c623eed7d20ba2e23。

## 人工裁决与执行边界

删缓存原因为本地入口 PATH 先搜 /usr/bin，原 RPM 环境先搜 /bin，相对编译器名解析为不同路径拼写；撤回 spec 缺陷判断。所有 cmake/ninja 均复用归档续十 original-rpm-build.sh 的原环境前导，逐次记录 PATH、which clang/clang++、完整 argv 与编译/链接环境。临时配置直接引用原源码，不复制源码。准备性错误每类允许纠正一次；同类第二次错误或任何产品门禁失败即停止。共享锁、16/4 GiB cap、swap0、nice/ionice、内存准入与磁盘底线沿用；归档证据与22RPM保护不变。

## 第一步：临时配置验证

原 RPM PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin；四次调用（temp-baseline cmake、temp-link-before ninja、temp-append cmake、temp-link-after ninja）均 which clang=/bin/clang、which clang++=/bin/clang++。完整 CFLAGS/CXXFLAGS/LDFLAGS/CC/CXX/AR/RANLIB 等保存在 rpm-env-temporary.json 的 calls 中及公开日志。环境前导保留原 flags/MLGO 路径；不执行与配置无关的 config.guess 补丁及 manifest 复制；MAKEFLAGS+= 在测试副本中改为 POSIX 等值赋值，原脚本未改。

临时 -S 为 /home/abuild/rpmbuild/BUILD/llvm-22.1.8/llvm，-B 为本会话新 BOLT 工作目录的 temp-build。预置唯一 LLVM_THINLTO_CACHE_PATH 为原树缓存路径，防止默认值随 -B 改变；只配置，不构建 LLVM 目标，不复制或清理缓存；CMake 的测试链接可能按原参数访问缓存。原参数配置后执行 rpmspec 展开的原草案追加命令；debug/release 命令此前已证明相同。无删缓存提示，编译器/flags/ThinLTO/MLGO 等非 BOLT 配置未变。

缓存差异13键：12个 BOLT/项目列表键及一个派生目录计数 CMAKE_NUMBER_OF_MAKEFILES 667→684。逐项实证新增17个 cmake_install.cmake 目录全部在 tools/bolt 下，无删除，严格对应计数差值。初版检查器仅按键名识别 BOLT，误报此派生计数；本次使用一次 cache-delta-classifier 准备性修正，要求新增目录集合/数量完全证明 BOLT 来源才接受，不豁免其他键。首轮日志与误报保留。修正轮两次配置 rc0；clang 链接边前后及原树已保存边逐字相同，SHA352a6f57fdc617c20f3e616a0f49ad113d1d5f057e44dcad0afa88c63a9a68cf。

原源码树（排除原 build）的完整路径/类型/大小/mtime 前后清单一致，无新增或修改；临时目录 finally 删除。4GiB轻scope两轮均40.635s，完整峰值/VmHWM/内存与回收证据在 JSON；没有共享锁，proc finally 已卸载。

后续恢复、干跑、候选、对象、双模式/清单、性能及 sandbox 结果将在本页追加；本次第一步 PASS 不代表后续门禁通过。

## 第二步：原始命令恢复未通过关键项门禁，STOP

保存失败配置开始时间以来的923个改写文件清单（以共享锁取得1791966147.7645748为界，紧接失败配置启动，清单是时间筛选候选而非逐文件因果断言）。其后只执行一次原始完整 cmake 命令，原 RPM 前导及 PATH 与第一步完全一致，which 仍 /bin/clang、/bin/clang++，真实 argv/环境均在 rpm-env-restoration.json 与 rpm-env-restore-configure.txt。没有省略原始 -D 参数。

调用返回0，但已有污染cache仍保存先前 /usr/bin compiler 记录；本次改回 /bin 又触发 CMAKE_C_COMPILER/CMAKE_CXX_COMPILER 变化及相同“require your cache to be deleted”提示。日志首轮启用clang/ThinLTO/原projects，自动删cache后第二轮变为默认配置。与失败前快照对比，50个显式命令/核心身份项中41项不一致；完整cache有664键差异。例如 LLVM_ENABLE_LTO Thin→OFF，LLVM_ENABLE_PROJECTS 原六项目→空，LLVM_TARGETS_TO_BUILD 四目标→all，CMAKE_INSTALL_PREFIX /usr→/usr/local，链接flags/MLGO/clang配置丢失。本次恢复 **FAIL**，不能将cmake rc0当恢复成功。

这是第二步明确的产品门禁“恢复后关键项必须一致”失败，按最新PM规则立即停止，不将它重命名为准备性错误重试。一次准备性修正仅用于第一步派生目录计数检查器；恢复命令未重试。ninja查询/干跑/分类与-j1补完未执行，>50条件没有评估，因此没有选择历史工具后备路线；本次无候选最终SHA、正式匹配、strip-all/微型门禁、DESTDIR、30/90对象、双模式、预期RPM/DWARF差异或30×5性能数据，sandbox未尝试、未查远端前后。此前早期匹配PASS仍仅历史资格结果，不能冒充本次候选。

当前原树仍未恢复：CMakeCache SHA17f7fbc72b14f6b1a5116aa17622e0af244fe84f2e72ef1e32bba61d3ca32876；build.ninja SHAc0068a3e42ae3b4303357000ddb6f30a0f72d46da704128277a052953ead4d42。完整before/本次after缓存、59,160,293B ninja文本差异及SHA留本次E，公开JSON含关键项/全部缓存差异、差异大小/SHA；不把覆盖两个快照当完整恢复方案。后续需获授权的污染缓存恢复步骤后才能继续；本轮不再尝试。

## 耗时、资源与保护审计

|阶段|scope秒|kernel峰GiB|最大采样VmHWM kB|
|---|---:|---:|---:|
|环境/输入准备|10.043|0.433|201148|
|首轮临时配置及分类器误报|40.633|0.712|307016|
|一次准备性修正后临时验证PASS|40.635|0.405|310256|
|原树恢复门禁FAIL|35.128|0.567|328556|

修正轮 baseline cmake28.166s、ninja边查询0.110s、append cmake3.894s、ninja边查询0.103s；恢复 cmake32.714s。完整各进程样本/宿主最低MemAvailable/轻4GiB swap0与scope回收在JSON；宿主最低仍≥16.66GiB。没有获取共享锁或运行重阶段，proc在配置各段finally卸载，没有宿主bind/ns。停止审计轻scope40.104s，kernel峰4.000GiB（含文件页缓存，受4GiB cap约束），保护原件逐SHA/大小与归档元数据均PASS。

普通clang仍7df0ff90…，22普通RPM全部不变，review49-independent-install元数据一致；源码树清单与任务前一致，W tracked仅既有gbs_llvm.conf改动、没有写W/llvm或进入ARM根。原地cache最终47,626文件/96,880,098,760B，比开工多519文件/2,288,400B；本轮配置可能执行测试链接，未复制cache，原地LLD写入/清理按交接授权允许，不声称cache冻结。文件系统free60,543,275,008B（56.39GiB）。没有任何>10GiB写入操作。

生产spec/helper、源提交d6ddbff5、文本patch/profile/manifest均未改；此次不需产品夹具变更，没有重新运行旧95fixtures。第一步认证仅证明原RPM环境追加配置无删cache、BOLT差异及clang链接边保持，完整Quickbuild/发布完整构建仍未认证。若tizen_base合入归档补丁，周五变基与spec冲突处理仍挂账。GitHub逐阶段提交与全部raw索引随本次收尾更新，不把GitHub证据提交当Gerrit源码提交。
