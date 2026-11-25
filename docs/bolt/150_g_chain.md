# 150 · PGO/BOLT profile 生成

**门禁修正与单测已完成，仅配置预演进行中。** 配方提交为 32005e1006fb849545a8e8cdf73a1a6a41f988d6，位于本地 pgo-dev。

- 配方与技能同步识别 Clang 资源目录、clang_rt. 和 libclang_rt. 产物，以及 compiler-rt 和 OpenMP 子构建。运行时边不允许 PGO 选项。主 C/C++ 编译边要求一个正确的 profile-use 参数，链接边允许该参数重复一次。
- Ninja 使用 compdb -x 展开响应文件。报告给出扫描边数、违规总数以及每条违规的输出、选项、类别和命令。
- 新增门禁测试 5/5、离线技能测试 59/59、编排测试 6/6 通过。保留 149-run 两次误拒原文作为回归输入。
- 19:36 PST 的 sudo 日志证明用户执行了清理脚本。三个登记路径仍以原 inode 存在，逐项输出未归档，因此成功、拒绝和释放字节数为 UNKNOWN。全机 df 变化不等于脚本释放空间。
- 只配置预演用新构建根，运行同一配方的 %build 到 Ninja 门禁后退出。G4 在预演通过且磁盘、内存都满足准入后启动。N2 已在 149-run 通过，本次没有 N2 阶段。

[配方补丁](../../tools/bolt/results/task150/pgo-recipe.patch) · [技能 diff](../../tools/bolt/results/task150/skill-gate.diff) · [门禁测试日志](../../tools/bolt/results/task150/gate-tests.txt) · [清理复测](../../tools/bolt/results/task150/sudo-recheck.json)
