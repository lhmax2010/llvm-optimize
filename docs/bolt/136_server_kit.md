# 136 号：原生服务器验证套件

**PASS。** `server-kit` 已发布，远端提交为 `e1c890c74eae5bac8f0eb2a9ca9120ec08e813f0`。分支只有一个根提交。GitHub 浅克隆后，26 个文件逐项核对通过。实际从 Gerrit 只读获取 PS5，应用 8 个产品文件的补丁后，Git tree 与 R 完全一致。[套件](https://github.com/lhmax2010/llvm-optimize/tree/e1c890c74eae5bac8f0eb2a9ca9120ec08e813f0)

## 发布与重新克隆

- 源码基底 PS5 `7b05a13744d1cf81a5e9cff22a27eb037bf1b6a8`，Gerrit ref `refs/changes/95/361395/5`。R 为 `2b9031dd9ab46e3fb142da13e64624de3896e8be`。
- `git ls-remote --heads` 的 `refs/heads/server-kit` 在推送前无记录，推送后为 `e1c890c74eae5bac8f0eb2a9ca9120ec08e813f0`。用 `git clone --branch server-kit --depth 1` 从 GitHub 新克隆，HEAD 一致，Git 确认为浅克隆，历史只有一个提交。
- 重新克隆后，根清单 `sha256sum -c` 通过 25/25 项，加上清单文件自身后共核对 26 个文件。最大文件 15,945,848 字节，未分片，未使用 Git LFS。README 记录了分片逐件校验、按序合并并核对整文件 SHA256 的命令。[README](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/e1c890c74eae5bac8f0eb2a9ca9120ec08e813f0/README.md) · [SHA256SUMS](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/e1c890c74eae5bac8f0eb2a9ca9120ec08e813f0/SHA256SUMS)
- 重新克隆后执行了真实的 Gerrit `git fetch`，`FETCH_HEAD` 指向 PS5。LLVM 验证工作树用本机已有 Git 对象加速，并只展开改动所需目录。`git apply --check --index --unidiff-zero` 通过，实际应用后的完整索引 tree 为 `ef9c45fb4f6b01f7ac410271153ff7b08552985a`。`packaging/llvm.spec` 的补丁以零上下文生成，避免发布旧上下文的内部注释。其他文件保留常规上下文。只读使用 Gerrit。
- 从新克隆的套件解包，733 个清单条目全部通过，包括 23 个原始输入、693 个依赖头文件和 17 份许可证或声明材料。23 个输入逐项匹配技能训练清单的路径、字节数和 SHA256。用归档头文件和已安装 SDK 的 GCC 启动对象执行 A 样本的 `clang -M`，解析到的 339 个头文件及其 SHA256 与原环境逐项一致。GCC 启动对象由匹配的 Tizen SDK 提供，套件记录其身份和 SHA256。[许可证清单](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/e1c890c74eae5bac8f0eb2a9ca9120ec08e813f0/LICENSES.md) · [依赖与 SDK 清单](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/e1c890c74eae5bac8f0eb2a9ca9120ec08e813f0/DEPENDENCIES.json)
- `skill/` 的 17 个文件取自发布时的证据分支。该目录最后一次变更为 `04c3047f927e00ffda1227c5fdc328a4bd72daf3`，自 134 号以来无文件差异。技能 tar.gz 解出的 17 份文件与 `skill/` 对应内容逐字节一致。
- 用重克隆套件、应用补丁后的源码和解包训练输入运行 dry-run，验证 8 个阶段、63 条计划命令和训练文件身份。完整 profile 生成流程仍待实跑。

## 禁用词扫描

沿用 134 号正则，以 `re.compile(pattern, re.I)` 和 `rx.search(line)` 逐行检查全部 24 个 UTF-8 文本文件。推送前和重克隆后均为 0 命中。训练输入和依赖源码原样归档，按任务范围免扫。

~~~text
github|lhmax|llvm-optimize|bolt-v4|sandbox|(?<![A-Za-z0-9])task[ _-]*[0-9]{2,}|[0-9]+号|报告号|/home/[^/\s]+|/opt/nvme-home|codex|claude|chatgpt|openai|anthropic|(?:@|https?://)[^/\s]*review\.tizen\.org
~~~

## 补丁路径

- `compiler-rt/CMakeLists.txt`
- `openmp/CMakeLists.txt`
- `packaging/clang-bolt-helper.py`
- `packaging/clang-pgo.fdata.xz`
- `packaging/clang-pgo.profdata.xz`
- `packaging/llvm-profiles.manifest`
- `packaging/llvm-static-archives-native.py`
- `packaging/llvm.spec`

## 完整分支清单

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `DEPENDENCIES.json` | 348,360 | `5952d8f0348f90c09254558bf80275776f55e626b86c32ef917abda7ae3d507e` |
| `LICENSES.md` | 6,755 | `8995a82c86a3a0add2b2845fa117c51bd524b6f803364587357552a825f47417` |
| `README.md` | 7,863 | `b38f2c908761a49f1048a9e7fee80a75a7662fcec9c63814d6e74cb8e3f60dc3` |
| `SHA256SUMS` | 2,347 | `fcc67655e1ba9a2efd20b1beea06106956caa8264fcac424f434042b4f4f4bdd` |
| `config.server.template.json` | 5,233 | `7ba3bd1bf19bb20f5e1000cedb92b5e00664d8a48a8b03c3b7fb8492a00e1800` |
| `pgo-recipe.patch` | 26,091 | `f839010d747f79c93f61cd93d371999f327d5bd81934232c8cf8b8cc2c3723cd` |
| `skill/SKILL.md` | 11,741 | `93ad4a5a86448ba5b045ac2c17ac63cbdbf7d33e0d30d82b846f04a2538ab9f8` |
| `skill/config.example.json` | 4,872 | `4beaabbc17fc593e99e1d06e9cf78699c8116c46ca75fc0da8885ae5467ed736` |
| `skill/references/gates.md` | 2,228 | `e955062076b6887f874b371e0b657d6f2e62f4dbc252a1f041e22de5df26ee19` |
| `skill/references/manifest-schema.md` | 2,369 | `c09a35d4150cf491161a642ca366ea94084b56f9d2a9a840368ab83ad477cc87` |
| `skill/references/pgo-match-method.md` | 1,809 | `f2129d2daa5543be8e5560480f32000bcf23b089b7c517c19c52a1aed398c2e5` |
| `skill/references/resource-budget.md` | 3,211 | `bce709361d1ab0205e0925850710bd2553814e7e2e3a8695c5bb1b461d43cfb4` |
| `skill/references/training-set.json` | 18,569 | `7547e5b22afbc94c941062b9a2130079c735a6d19d29429747e49a9aac60ec78` |
| `skill/references/training-set.md` | 7,216 | `9c2fc250444d97afeefc0ce8ec8c0c8cb0bc5bb8b92947f3259caef4454856e0` |
| `skill/scripts/bolt_stale_gate.py` | 4,465 | `0ef2283a2d02024403d483170c8be2ea8ca983cba4b72e18b63b314ea6f9156b` |
| `skill/scripts/generate_synthetic.py` | 3,859 | `d77996302ace91192a3e658a69d8d9083551fa2f6be7d4083fb41ab764c9bd26` |
| `skill/scripts/manifest.py` | 6,288 | `64954b7fa111655cbea3eea7bb7c4e306685b415cf1dde4b626763a2e81293b5` |
| `skill/scripts/pgo_pair.py` | 29,726 | `7df0d289cf4b883ab517ebc0e740549a8ffabd3697edcabd762985bed6f1c6e2` |
| `skill/scripts/runtime_dep_check.py` | 3,591 | `9a83f9c2febfdbf12a1d20453adec390b8d531c8d6e66ac30bac9d8ed4ba0511` |
| `skill/tests/test_bolt_stale_gate.py` | 3,721 | `7b1970b56b9ca0a4f7160f598061a6d687f69ece551f886f57b2c3685be9aaaa` |
| `skill/tests/test_manifest.py` | 3,602 | `5c281470628350e9c7602620913e0bb8501393905cadcefe7433f1a8b110e921` |
| `skill/tests/test_pgo_pair.py` | 4,812 | `f29a6e27d181f577faab15db084af32b961aec485587a36440730cc636179b1d` |
| `skill/tests/test_runtime_dep_check.py` | 2,800 | `ccf755229acd30e31943d22c9a9bacfa18833320b8e2f8f206c3940576bcc74a` |
| `tizen-llvm-offline-profile.tar.gz` | 30,521 | `9ccfb1019850ec57e0cc7f93ab6566955203d3428bf04d5754f3889b3adfc40c` |
| `training-inputs.sha256` | 122,513 | `9b103428d83fa2777734e334841a175418339c5401cd7d408a0d5b5e5b322c81` |
| `training-inputs.tar.xz` | 15,945,848 | `8a12c724b43c98e0db6e6d66234d070769d85c91872aa623275032407eeb2962` |

## 执行记录

本地证据目录为 `/home/linhao/Toolchain/development/llvm-optimize/archive/server-kit-136`。`github-after.stdout`、`clone-identity.json`、`remote-verification/results.json` 和 `scan-results.json` 分别记录远端引用、克隆身份、复验和扫描结果。

README 生成包装的第一次调用报 `SyntaxError: Unexpected identifier 'git'`。修正引号后重跑成功，首次调用发生在写入之前。无 STOP。
