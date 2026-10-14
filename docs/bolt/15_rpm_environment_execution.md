# 15 原 RPM 环境临时验证与续跑记录

2026-10-14。第一步临时配置 **PASS**；后续原树恢复与候选尚未执行。当前生产草案不改，源码提交仍 d6ddbff5ba74bfb420b357b5b6ba9ed300971bb4，父 cb67996861d070d68fec2b4c623eed7d20ba2e23。

## 人工裁决与执行边界

删缓存原因为本地入口 PATH 先搜 /usr/bin，原 RPM 环境先搜 /bin，相对编译器名解析为不同路径拼写；撤回 spec 缺陷判断。所有 cmake/ninja 均复用归档续十 original-rpm-build.sh 的原环境前导，逐次记录 PATH、which clang/clang++、完整 argv 与编译/链接环境。临时配置直接引用原源码，不复制源码。准备性错误每类允许纠正一次；同类第二次错误或任何产品门禁失败即停止。共享锁、16/4 GiB cap、swap0、nice/ionice、内存准入与磁盘底线沿用；归档证据与22RPM保护不变。

## 第一步：临时配置验证

原 RPM PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin；四次调用（temp-baseline cmake、temp-link-before ninja、temp-append cmake、temp-link-after ninja）均 which clang=/bin/clang、which clang++=/bin/clang++。完整 CFLAGS/CXXFLAGS/LDFLAGS/CC/CXX/AR/RANLIB 等保存在 rpm-env-temporary.json 的 calls 中及公开日志。环境前导保留原 flags/MLGO 路径；不执行与配置无关的 config.guess 补丁及 manifest 复制；MAKEFLAGS+= 在测试副本中改为 POSIX 等值赋值，原脚本未改。

临时 -S 为 /home/abuild/rpmbuild/BUILD/llvm-22.1.8/llvm，-B 为本会话新 BOLT 工作目录的 temp-build。预置唯一 LLVM_THINLTO_CACHE_PATH 为原树缓存路径，防止默认值随 -B 改变；仅配置，不读写或复制缓存。原参数配置后执行 rpmspec 展开的原草案追加命令；debug/release 命令此前已证明相同。无删缓存提示，编译器/flags/ThinLTO/MLGO 等非 BOLT 配置未变。

缓存差异13键：12个 BOLT/项目列表键及一个派生目录计数 CMAKE_NUMBER_OF_MAKEFILES 667→684。逐项实证新增17个 cmake_install.cmake 目录全部在 tools/bolt 下，无删除，严格对应计数差值。初版检查器仅按键名识别 BOLT，误报此派生计数；本次使用一次 cache-delta-classifier 准备性修正，要求新增目录集合/数量完全证明 BOLT 来源才接受，不豁免其他键。首轮日志与误报保留。修正轮两次配置 rc0；clang 链接边前后及原树已保存边逐字相同，SHA352a6f57fdc617c20f3e616a0f49ad113d1d5f057e44dcad0afa88c63a9a68cf。

原源码树（排除原 build）的完整路径/类型/大小/mtime 前后清单一致，无新增或修改；临时目录 finally 删除。4GiB轻scope两轮均40.635s，完整峰值/VmHWM/内存与回收证据在 JSON；没有共享锁，proc finally 已卸载。

后续恢复、干跑、候选、对象、双模式/清单、性能及 sandbox 结果将在本页追加；本次第一步 PASS 不代表后续门禁通过。
