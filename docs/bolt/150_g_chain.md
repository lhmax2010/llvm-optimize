# 150 · PGO/BOLT profile 生成

**仅配置预演两轮完成，最终 0 条违规。** 最终配方为本地 pgo-dev 提交 750d7a83475a3c3c6fecf545ea74ba110fc845f5。G4 仍须通过磁盘和内存准入，N2 已在 149-run 通过。

| 预演 | Ninja 记录 | 违规 | 核对结果 |
|---|---:|---:|---|
| 1 | 21,983 | 5 | 三个 clang-tidy OpenMP 检查对象误归运行时。两个 Clang 链接命令后附 CMake -E，所以链接分类误报。没有缺失、错误或多余 PGO 参数的主编译边。 |
| 2 | 25,940 | 0 | 5,357 条主 C/C++ 编译边使用正确 profile，879 条运行时 C/C++ 编译边没有 PGO 选项。 |

第二轮补齐了 compdb 省略的 3,957 个非 phony 输出。compdb -x 展开响应文件。有命令的遗漏输出通过 Ninja 查询原命令，未经执行。[Ninja 的 compdb 实现](https://github.com/ninja-build/ninja/blob/v1.13.1/src/ninja.cc#L969-L1024)

两轮均在独立新根使用同一配方配置，第二轮通过门禁后按预演标记立即退出。没有运行 Ninja 产品编译。root 所有的残留只登记。预演与完整运行都复用通过哈希核对的 G3 profdata，原 IR 输入提交与新配方单独记账。

- 最终门禁 8/8、技能 59/59、编排 6/6 通过。
- 19:36 PST 的日志证明用户执行了 149-run 的 sudo 脚本。三个目录仍以原 inode 存在，未保存脚本逐条输出，因此各项成功、拒绝和释放字节数无法确认。
- G4 的保守磁盘准入为 312,154,457,695 B。磁盘或内存不够时按 10 分钟间隔重测，最长等待 60 分钟。

[最终配方补丁](../../tools/bolt/results/task150/pgo-recipe-final.patch) · [门禁分类修正](../../tools/bolt/results/task150/preview-1/gate-correction.diff) · [预演一](../../tools/bolt/results/task150/preview-1/ninja-gate.json) · [预演二](../../tools/bolt/results/task150/preview-2/ninja-gate.json) · [单测](../../tools/bolt/results/task150/gate-tests-final.txt) · [清理复测](../../tools/bolt/results/task150/sudo-recheck.json)
