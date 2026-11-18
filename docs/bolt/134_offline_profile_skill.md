# 134 号离线 PGO/BOLT 生成技能

**交付验证 PASS。** 技能共 17 个文件。Agent Skills 格式校验通过，单元测试 39/39，PS5 原版边界夹具 15/15。示例和本机 dry-run 各产生 8 个阶段、63 条计划命令，未启动构建进程或创建目标输出目录。完整流水线仍待实跑验证。

技能目录为 `tools/skills/tizen-llvm-offline-profile/`。依据为 131 号编排与预算、设计 v10、131 作用域和匹配方法记录、58/59 号历史测量、PS5 中的 `match_counts` 及 15 项原有边界夹具。本次未进行 GBS、编译训练、LLVM/BOLT 重写、RPM 打包或完整发布验收。

## 文件清单
- `SKILL.md`
- `config.example.json`
- `references/gates.md`
- `references/manifest-schema.md`
- `references/pgo-match-method.md`
- `references/resource-budget.md`
- `references/training-set.json`
- `references/training-set.md`
- `scripts/bolt_stale_gate.py`
- `scripts/generate_synthetic.py`
- `scripts/manifest.py`
- `scripts/pgo_pair.py`
- `scripts/runtime_dep_check.py`
- `tests/test_bolt_stale_gate.py`
- `tests/test_manifest.py`
- `tests/test_pgo_pair.py`
- `tests/test_runtime_dep_check.py`

## 测试与兼容性

- 清单测试 9 项，覆盖两种 BOLT 模式、PGO 关闭回退、草案状态、占位资产、自相矛盾的 SHA、缺失或重复映射与路径越界。
- BOLT 测试 18 项，其中 15 项与 PS5 原边界夹具一致。比较实际源码确认独立脚本的 `match_counts` 与 PS5 逐字相同。同一测试类用两种实现运行，均 15/15。文件入口增加完整行、log SHA、准确阈值和额外畸形行的检查。
- 运行时门禁测试 5 项，以 ELF/readelf 夹具模拟正常和异常输出；含归档、薄归档、符号、节及动态依赖。此处不代替真实发货载荷验证。
- dry-run/编排测试 7 项，含零 subprocess、阶段选择、缩减档实参、checkpoint 文件身份、Ninja 范围及合成输入哈希。三个合成输入从固定 seed 和 scale 生成后，大小与历史 SHA 均匹配。

## Dry-run 对照

| 新阶段 | 131 号对应阶段 | 差异 |
|---|---|---|
| instrumented-build | instrumented-build | 输出 GBS argv、cwd 与独立构建根。资源由配置中的档位和协作锁管理。 |
| ir-train | ir-train | 仍按完整原顺序训练 23 次。各次以独立目录检查恰好一份非空 profraw。 |
| merge-profdata | merge-profdata | 计划用文件模式标注，实跑先列出每份 profraw 再作为 argv 传给 llvm-profdata。 |
| pgo-build | pgo-build | 增加离线 Source 暂存、主构建及运行库 Ninja 参数检查与发货载荷门禁。 |
| bolt-tools-relink | bolt-tools、relink-strip-debug | 合为一个阶段，显式展示原始 link edge、replay、strip-debug 以及节核对。 |
| bolt-instrument-train-merge | bolt-instrument、bolt-train、merge-fdata | 合为一个阶段，保留采集参数、23 条训练命令和 fdata 合并。 |
| bolt-match | 新增显式门禁 | 用发布参数进行同一输入重写，执行原 PS5 计数判定。引用历史成功改写的 44.984 秒与 8,712,601,600 B cgroup 峰值。 |
| write-manifest | write-manifest | 输出两份 xz 与未认证清单，写入 BOLT 结果、PGO UNKNOWN、源码及工具证据。 |

131 的 10 个历史子步骤与各自耗时、内存数据一一对应。旧已知时间小计为 11328.532 秒，增加显式 BOLT 匹配阶段的历史数据后，仍有未知阶段。保留 21,703,991,296 B 历史 cgroup 峰值、91,275,411,456 B 两个根的边界观测值和含保留空间的 125.626 GiB 规划下界。两次 dry-run 展示配置中的正常档和缩减档。

本机 dry-run 的 23 条有序目标参数、大小和输入 SHA 与 131 原始计划一致。20 个真实输入路径可见；A/B/C 原工作路径已不在，生成器单测重现其 SHA。两次计划共 8 阶段、63 条命令，并分别保存在本地 `/home/linhao/Toolchain/development/llvm-optimize/temp/task134-offline-profile/example-dry-run.json` 和 `/home/linhao/Toolchain/development/llvm-optimize/temp/task134-offline-profile/local-dry-run.json`。本机配置和计划含现场路径，仅保留在本地。

## 可共享性扫描

以 Python 正则大小写不敏感地扫描技能目录的所有 UTF-8 文件，每条命中附文件和行号。命令等价于以下已执行扫描。结果为 **17 个文件，0 命中**。

~~~sh
/usr/bin/python3 -B -c 'import pathlib,re,sys; pattern=re.compile("github|lhmax|llvm-optimize|bolt-v4|sandbox|(?<![A-Za-z0-9])task[ _-]*[0-9]{2,}|[0-9]+号|报告号|/home/[^/\\s]+|/opt/nvme-home|codex|claude|chatgpt|openai|anthropic|(?:@|https?://)[^/\\s]*review\\.tizen\\.org",re.I); root=pathlib.Path(sys.argv[1]); print([(str(f.relative_to(root)),i,line) for f in root.rglob("*") if f.is_file() for i,line in enumerate(f.read_text(encoding="utf-8").splitlines(),1) if pattern.search(line)])' /path/to/tizen-llvm-offline-profile
~~~

## 本地交付包及验证边界

- 包为 `/home/linhao/Toolchain/development/llvm-optimize/temp/task134-offline-profile/tizen-llvm-offline-profile.tar.gz`，30,521 B，SHA256 `9ccfb1019850ec57e0cc7f93ab6566955203d3428bf04d5754f3889b3adfc40c`。回读归档核对 17 个文件逐字节一致。包仅留在本地。
- GBS 配方适配、构建根和工具运行时路径、真实 Ninja/ELF 载荷门禁、端到端断点续跑和资源监督、BOLT 新 profile 重写、发布验收和 PGO 匹配计数尚未经完整运行验证。预处理输入和 SDK 由操作者从获准来源取得或重建。SKILL.md 末尾保留指定状态原文。
- 证据采集时一次内联脚本因反引号转义解析失败，修正后继续。提交前校验发现训练文档末尾有一个多余空行，修正文档并重新扫描、打包和回读验证。无未恢复的 STOP。

~~~text
SyntaxError: Unexpected identifier 'INPUT'
~~~
