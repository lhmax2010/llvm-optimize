# 154 · PS6 分析器打包修正

**A 已完成。补丁 5 的九个资源路径各归一个包，模拟无文件增减。补丁 6 恢复已安装但被 spec 删除的 14 个文件。** 补丁 1–3 的提交保持不变。正文仅重建补丁 4 的第三段。完整构建尚待 151 与 153 完成并推送证据。

## 补丁系列

| 顺序 | 补丁 | 提交 | 改动 |
|---|---|---|---|
| 1 | [1](../../tools/bolt/results/task154/0001-suggestion-1.patch) | `09b187fa3d5061d1ae431e97d3756786ed7529b1` | 旧包名依赖元数据。 |
| 2 | [2](../../tools/bolt/results/task154/0002-suggestion-2.patch) | `de3bf8dc783bf54d142a448cc3673ecee3fecaef` | OpenMP 安装注释。 |
| 3 | [3](../../tools/bolt/results/task154/0003-suggestion-3.patch) | `42f363793d46fbc80c924f908a987e769f083d03` | X86 镜像宏清理。 |
| 4 | [5](../../tools/bolt/results/task154/0004-suggestion-5.patch) | `52df1328a4a4c2f5eeef9b4ea60fd47d377d9246` | 仅 llvm.spec 的 %files，+6/−0。 |
| 5 | [6](../../tools/bolt/results/task154/0005-suggestion-6.patch) | `2960ffa545a38ee71dbb38861af7831933033089` | llvm.spec +2/−2，停止删除模块并分入 clang。 |
| 6 | [4](../../tools/bolt/results/task154/0006-suggestion-4.patch) | `88d0990dc9eaf55f80da3d713d02dce28f167eac` | 仅正文，tree 与补丁 6 相同。 |

本地分支 `ps6-suggestions` 以 `06f3424c543a9645707f9afbbd9b5318280fffeb` 为基底。构建取补丁 6 的 tree `9122c185080347bc424ace896f8a17dcd64555d4`。只有证据提交推送到 bolt-v4。

## 5 · HTML 报告与查看器资产

在 152 登记的 22 个 B1 RPM 上重读 `rpm -qlp`，先套用 PS6 已有的四个命令从 llvm 到 clang 的移动，再套用本补丁。llvm-devel 的 share 通配符保留，三个目标使用 %exclude。Tizen RPM 4.14.1 在 x86_64、aarch64、armv7l 解析均通过，补丁 5 和 6 合计 6/6。

| 验证 | 结论 |
|---|---|
| (a) 唯一归属 | 9 个目标路径和该组入口、包装脚本各归一个包，0 个新重复。若把检查扩展到 B1 的所有无关文件，基线原有 304 个非目录路径重叠及 18 个共享目录。它们的归属均保持，例如 clang/ compiler-rt 的资源头文件和两个开发包的 libarcher_static.a。 |
| (b) 资源覆盖 | clang 收录 Perl scan-build、包装脚本、sorttable.js、scanview.css 和手册。llvm 收录 scan-view 与 4 个 data 文件，保持 clang 对 llvm 的版本绑定。外部解释器由运行环境提供。 |
| (c) 路径守恒 | 18,061 个不同路径在补丁 5 前后完全一致。llvm-devel → clang 4 路径，llvm-devel → llvm 5 路径，计入两目录本身。增加与丢失均为 0。 |

Perl scan-build 的 450–468 行从相对安装位置读取 JS/CSS，900 行生成报告时调用 CopyFiles。资源不可读则走 DieDiag，111–125 行打印诊断并退出。1909–1925 行定位两个 analyzer wrapper，找不到也走 DieDiag。scan-view 的 65–74 行先查相邻 `../share/scan-view`，缺目录时退回源码相对目录，然后在进入异常处理前导入 ScanView。两处均缺失时导入报错。121 行的参数解析先于 146 行的 run，`--help` 只验证入口能启动，资产加载由归属与源码核对证明。 [源码原文](../../tools/bolt/results/task154/source-excerpts.txt) · [全量模拟](../../tools/bolt/results/task154/static-package-simulation.json) · [RPM 解析](../../tools/bolt/results/task154/rpmspec-results.json)

## 6 · Python 模块

**已安装后被删除。** PS6 的 scan-build-py CMake 选项默认开启。CMakeLists.txt 第 93–95、111–113、127–129 行把模块、报告资源和 libear 文件装到前缀下固定的 `lib/`。B1 日志 12996–13009 行、N2 日志 12636–12649 行均记录相同的 14 次 Installing。之后分别在 24139–24140 和 16516–16517 行被显式删除。

移除两条删除命令，由 clang 收录 `%{_prefix}/lib/libscanbuild`、`%{_prefix}/lib/libear`，并递归包含各自内容。三个 Python 入口第 9–13 行从 `/usr/bin` 的父目录拼出 `/usr/lib`，不使用架构 lib64。intercept.py 第 30 行导入 libear。模拟预期新增 14 个文件及 3 个目录。clang 不新增显式 Python 3 Requires，维持与 llvm 一致的构建根策略。 [B1 原文](../../tools/bolt/results/task154/B1-module-install-and-delete.txt) · [N2 原文](../../tools/bolt/results/task154/N2-module-install-and-delete.txt)

## 4 · 说明复核

**8/8 与 diff 相符。** 只替换了第三段。新正文纯 ASCII，最长 70 列，禁用词零命中。标题、HQ 历史和 trailer 按要求排除在门禁之外。 [逐句核对表](../../tools/bolt/results/task154/message-sentence-audit.md) · [说明 diff](../../tools/bolt/results/task154/p4-message.diff)

## 构建排队

等待 151 和 153 的所有相关单元退出，并验证两个最终回执都是远端 bolt-v4 的祖先。构建用 144 B1 配方和第 82 号入口。磁盘线为 `302,154,457,695 B`，内存按 139-D。看门狗停自己的子单元后清理并重新准入，资源中断最多重试一次。功能测试用只请求新 llvm、libllvm、clang 和 Perl 的独立 Tizen chroot，另有基础运行环境和解析得到的依赖。验证禁止 llvm-devel，并检查实际安装的三个包的 VCS。Python 测试依实际环境，未做代替试验。截止 2026-11-27 20:00 PST。
