# BOLT 留出集（2026-09-20）

本目录只用于 docs/17 的留出评估，**没有参与 BOLT profile 训练**。
训练集仍为 `../real_tu/`，本目录不得并入训练目录。使用基准台时显式传
`--real-tu-dir tools/bench_inputs/holdout_tu --seed 20260920 --scales 1 2 2`。

`selection.json` 在任何候选收益测量之前锁定：AST、Parse、Driver、前端
CodeGen（排除 TargetBuiltins）、IR、Analysis、AArch64、X86、Object、ProfileData
各一个。使用已有 `.ninja_log` 中每目标最后一次记录，在 2–12 秒范围内选最接近
6 秒者，以对象路径打破同值；训练源码全部排除。没有按 BOLT 收益选择或替换。
选择器是 `tools/select_llvm_holdout.py`；完整候选池、原始日志和命令保存在
`temp/bolt-holdout-20260920/selection/`。

这十个 TU 来自 LLVM `f111162e94aa48ed367c9d2c039456c70e7160ae` 构建树，
均由 RPM 基线 clang 22，以 `--target=armv7l-tizen-linux-gnueabi`、现有 ARM
GBS sysroot、同一个 clang 22 资源目录实际预处理。格式与
[训练集格式规范](../real_tu/README.md) 相同；每个 `.flags.json` 包含目标、
SHA256、语义 flags、原始编译命令与实际预处理命令。没有更改源码或生成配置头。

七个不超过 10 MB 的 `.ii` 与 sidecar 一同提交；另三个的 sidecar `input`
引用下列工作区绝对目录中的文件：

`/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-holdout-20260920/collection/`

| 不入 Git 的输入 | 字节 |
| --- | ---: |
| llvm_frontend_codegen_CoverageMappingGen.ii | 10722459 |
| llvm_aarch64_AArch64InstructionSelector.ii | 18902822 |
| llvm_x86_X86ISelDAGToDAG.ii | 19611787 |

迁移机器时需复制这三个原始输入，并更新绝对 `input` 路径，内容 SHA256 不得改变。
也可用 `collect_llvm_real_tu.py` 和本清单重新采集，之后必须核对全部输入身份。
详细复现命令、时序、校准与三方结果见 [docs/17](../../../docs/17_bolt_holdout.md)。

合成 A/B/C 在运行时生成，不存于此目录。历史生成器的 A 不消耗随机数；本次扩展
仅对非默认 seed 使用另一条独立随机流选择不同模板 ID，数量和模板结构不变。
默认 73419 的历史输出逐字节保留，新 seed 20260920 使三类都成为新输入。
