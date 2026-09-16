# 00 工作区初始化记录

日期：2026-09-16（Asia/Shanghai）。

工作区：`/home/linhao/Toolchain/development/llvm-optimize`。
远端：<https://github.com/lhmax2010/llvm-optimize.git>，分支：`main`。

本次仅初始化 Git 仓库、目录和产出规范。未调查 LLVM 工具链，未修改源码，
未构建任何东西，未向 Gerrit 推送任何内容。

## 1. 初始化前的工作区现状

以下为执行 `git init` 前的顶层目录原始输出：

```text
$ ls -la
total 16
drwxrwxr-x  3 linhao linhao 4096 Sep 16 14:33 .
drwxrwxr-x 21 linhao linhao 4096 Sep 16 14:33 ..
-rw-rw-r--  1 linhao linhao 1059 Sep 16 14:33 gbs_llvm.conf
drwxrwxr-x 32 linhao linhao 4096 Sep 16 14:29 llvm
```

| 路径 | 初始大小 | 说明 |
| --- | --- | --- |
| `llvm/` | `6.9G`（`du -sh`） | 已有 LLVM 源码树，不提交 |
| `gbs_llvm.conf` | 1,059 字节（`ls -la`） | 已有 GBS 配置，原样提交 |
| 工作区整体 | `6.9G`（单独执行 `du -sh .`） | 初始化前测量 |

源码树实际路径经 `readlink -f llvm` 确认为：

```text
/home/linhao/Toolchain/development/llvm-optimize/llvm
```

初始化前检查 `.git` 不存在（同时检查普通路径和符号链接），
`git rev-parse --show-toplevel` 也确认此目录不属于上层 Git 仓库。
因此没有覆盖既有仓库。`git ls-remote --symref` 检查指定 GitHub 远端，
返回码为 0、输出为空，远端当时没有任何引用。

## 2. 执行顺序与忽略规则

严格按以下顺序执行：

1. 查看顶层目录、确认源码树实际路径与体积、检查是否已有 Git 仓库。
2. 先写 `.gitignore`，使用实测目录名 `/llvm/`。
3. 执行 `git init -b main`，立即检查状态数量与源码树排除规则。
4. 建立 `docs/`、`tools/`、`temp/`，写入产出规范和目录占位文件。
5. 验证状态数量、排除规则和待提交文件大小后，才执行第一次 `git add`。
6. 首次提交并推送；根据实际输出撰写本报告，再单独提交推送本报告。

首次 `git add` 使用明确的文件清单：

```bash
git add -- .gitignore docs/README.md gbs_llvm.conf temp/.gitkeep tools/.gitkeep
```

`.gitignore` 完整内容如下：

```gitignore
# Existing LLVM source tree (verified workspace directory).
/llvm/

# Intermediate files, raw logs, and large files; keep the directory.
temp/*
!temp/.gitkeep

# Build directories and compiled outputs.
build/
build-*/
cmake-build-*/
out/
CMakeFiles/
CMakeCache.txt
compile_commands.json
*.o
*.obj
*.so
*.so.*
*.a
*.lo
*.la
*.dylib
*.dll
*.exe
*.rpm
*.deb
*.d
*.bc
*.pch
*.gch
*.gcda
*.gcno
*.profraw
*.profdata

# GBS build roots, package outputs, and caches.
GBS-ROOT*/
gbs-root*/
gbs_root*/
.gbs/
.osc/
.ccache/
BUILD/
BUILDROOT/
RPMS/
SRPMS/

# Archives belong in temp/.
*.tar
*.tar.*
*.tgz
*.tbz2
*.txz
*.zip
*.7z

# Editor and tool temporary files.
.idea/
.vscode/
.cache/
.gstack/
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
.DS_Store
Thumbs.db
*.swp
*.swo
*~
*.tmp
*.temp
*.bak
*.log
```

GBS 配置中的构建根为
`/home/linhao/Toolchain/development/llvm-optimize/temp/GBS-ROOT-TIZEN-UNIFIED-LLVM-CODES`，
被 `temp/*` 和 GBS 构建根规则覆盖。此处仅核对路径是否排除，没有执行 GBS。

## 3. 状态数量与源码树排除验证

写入 `.gitignore`、初始化 Git 后，首次执行的实际结果为：

```text
$ git status --porcelain | wc -l
2
$ git status --porcelain
?? .gitignore
?? gbs_llvm.conf
```

目录和规范文档建立后、第一次 `git add` 前，数量为 **5**：

```text
$ git status --porcelain | wc -l
5
$ git status --porcelain
?? .gitignore
?? docs/
?? gbs_llvm.conf
?? temp/
?? tools/
```

第一次暂存后数量仍为 **5**，暂存状态原始输出为：

```text
$ git status --porcelain
A  .gitignore
A  docs/README.md
A  gbs_llvm.conf
A  temp/.gitkeep
A  tools/.gitkeep
```

数量均在几十个以内，没有出现成千上万条记录。源码树排除验证：

```text
$ git check-ignore -v llvm/
.gitignore:2:/llvm/	llvm/
```

```text
$ git status --short --ignored -- llvm/
!! llvm/
```

`git ls-files -- llvm/` 无输出，确认索引中没有 LLVM 源码。
`temp/` 中仅 `.gitkeep` 被跟踪：

```text
$ git ls-files -- temp/
temp/.gitkeep
```

另外检查了 `build/`、`out/`、`GBS-ROOT/`、对象文件、库、RPM 和编辑器目录，
全部匹配忽略规则。`git check-ignore -q temp/.gitkeep` 返回 1，确认占位文件
未被忽略。完整检查输出保存在
`/home/linhao/Toolchain/development/llvm-optimize/temp/01_precommit_checks.txt`，不提交。

首次暂存的 5 个文件均不超过 10 MB：`.gitignore` 811 字节、
`docs/README.md` 1,684 字节、`gbs_llvm.conf` 1,059 字节，两个 `.gitkeep`
均为 0 字节。对暂存对象再次检查大小，且 `git diff --cached --check` 通过。
本报告也在其提交前检查大小。

## 4. 目录结构与产出规范

```text
llvm-optimize/
├── .gitignore
├── gbs_llvm.conf
├── docs/
│   ├── README.md
│   └── 00_workspace_setup.md
├── tools/
│   └── .gitkeep
├── temp/
│   ├── .gitkeep
│   └── ...（原始日志和中间产物，不提交）
└── llvm/（已有 6.9G 源码树，不提交）
```

- `docs/`：上传需要评审的报告、方案和设计文档，使用编号前缀排序。
- `tools/`：上传分析脚本、基准测试脚本；当前用 `.gitkeep` 保留空目录。
- `temp/`：存放中间产物、原始日志和大文件，仅上传 `.gitkeep`。
- 超过 10 MB 的文件放 `temp/`，在相关文档中记录工作区绝对路径。
- 每个任务完成后提交并推送至 GitHub；英文提交信息说明具体产出。
- 不向 Gerrit 推送任何内容；代码改动须等所有评审通过后才进入 Gerrit 流程。

完整规范见 [README.md](README.md)。`.gitignore` 不具备按文件大小过滤的能力，
因此每次提交前仍需检查暂存文件大小。

## 5. 首次提交与推送的原始输出

以下输出均来自实际成功执行的命令，返回码均为 0。
本报告在首次推送完成后形成，并通过随后的一次文档提交推送保存，
以便记录已发生的结果。此节及文末日志反映首次推送完成时的状态；
包含本报告的后续提交及最终推送结果在任务完成回执中列出。

```text
$ git commit -m "chore: initialize workspace and output guidelines"
[main (root-commit) 2c6e496] chore: initialize workspace and output guidelines
 5 files changed, 121 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 docs/README.md
 create mode 100644 gbs_llvm.conf
 create mode 100644 temp/.gitkeep
 create mode 100644 tools/.gitkeep
```

```text
$ git push -u origin main
To https://github.com/lhmax2010/llvm-optimize.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

```text
$ git log --oneline
2c6e496 chore: initialize workspace and output guidelines
```

```text
$ git remote -v
origin	https://github.com/lhmax2010/llvm-optimize.git (fetch)
origin	https://github.com/lhmax2010/llvm-optimize.git (push)
```

首次推送后，工作区状态条目数为 0：

```text
$ git status --porcelain | wc -l
0
```

原始日志位于 `/home/linhao/Toolchain/development/llvm-optimize/temp/`，例如
`10_initial_commit.txt`、`11_initial_push.txt`、`12_initial_log.txt`、
`13_initial_remote.txt`；只将必要原始输出嵌入本报告，日志文件不提交。

## 6. 提交前自检

以下自检在提交本报告前完成，推送证据取自已完成的首次推送。

1. **`.gitignore` 是否在第一次 `git add` 之前就已就位？**

   是。写入 `.gitignore` 后才执行 `git init`，完成状态和排除规则验证后
   才执行第一次 `git add`。

2. **`git status --porcelain | wc -l` 的实际数字是多少？LLVM 源码树是否被正确排除？**

   初始化后为 **2**；目录和规范文档就绪后为 **5**；首次暂存后仍为 **5**；
   首次提交推送后为 **0**。LLVM 源码树被正确排除：`git check-ignore -v llvm/`
   命中 `.gitignore:2:/llvm/`，忽略状态为 `!! llvm/`，
   `git ls-files -- llvm/` 无输出。没有源码进入索引。

3. **仓库总大小是多少？（`du -sh .git`）**

   首次推送后、本报告暂存前为 **240K**（不含被排除的 6.9G 源码树）。
   首次提交前测量为 156K。以下为首次推送后的实际输出；后续提交报告
   会使 Git 元数据略有增长。

```text
$ du -sh .git
240K	.git
```

4. **是否向 Gerrit 推送了任何内容？**

   否。唯一远端为指定的 GitHub `origin`，仅执行了 `git push -u origin main`。

5. **是否构建了任何东西？**

   否。没有执行 GBS、CMake、Ninja、Make 或其他构建命令。

6. **推送是否成功？贴出 git log 与 remote 的原始输出。**

   是。首次推送返回码为 0，创建远端 `main` 并建立跟踪关系。
   随后执行的原始输出如下：

```text
$ git log --oneline
2c6e496 chore: initialize workspace and output guidelines
```

```text
$ git remote -v
origin	https://github.com/lhmax2010/llvm-optimize.git (fetch)
origin	https://github.com/lhmax2010/llvm-optimize.git (push)
```
