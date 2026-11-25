# 157 · QB PGO 候选

**等待 G4 的正式回执。** 预检已通过。候选与 sandbox 写操作未开始。

配方 `750d7a83475a3c3c6fecf545ea74ba110fc845f5`，tree `0ab6abcd20184eeab988d139b28d2ef164707dcf`，直接父提交 `e42a56bd17f2870e184e48f7d0b8769f7b505d85`。
PS5 `7b05a13744d1cf81a5e9cff22a27eb037bf1b6a8` 经祖先检查通过。PS5 至配方的 14 条新增提交说明通过 ASCII、STATUS 禁用词和扩展禁用词检查。

预检用 Tizen RPM 4.14.1 展开开关片段，x86_64 的 PGO 路径与混合链接生效，BOLT 无活动步骤，ARM 两架构与默认展开逐字节相同。CMake 脚本模式执行上游 profile-use 条件，在 C/C++ 标志中生成 `-fprofile-instr-use`。RPM 调用通过 `LLVM_PROFDATA_FILE` 传递路径。没有配置或编译 LLVM。正式展开和两个 manifest 校验将在 G4 PASS 后针对候选提交执行。

等待单元 `llvm-opt-task157-qb-candidates.service`。A 只使用 Toolchain T 的映射。G3 预期 `52,530,416 B`，SHA256 `39171c4a5fcb6166ac86d6d47ad16c7890527a73e66c26f035fb910288f496aa`。B 等待 G6、G7、G8 PASS。当前技能生成器写 `UNQUALIFIED`，打包端需要 `READY`。B 使用实际生成的原件核对这一门禁。

新建引用使用普通 Git push。pre-push 检查远端通告的旧 SHA 全零，并检查完整 sandbox 目标。预检模拟通过新建、拒绝已有引用、拒绝 refs/for 和拒绝多引用四种情况。QB 由用户触发。

[预检原文](../../tools/bolt/results/task157/preflight/) · [等待单元](../../tools/bolt/results/task157/watch.py)
