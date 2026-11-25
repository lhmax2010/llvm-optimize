# 158 · QB manifest、编译基准和 154-B 核对

**核对通过。** 157 的 manifest 例外限于 QB 测试提交。154-B 的 RPM 检查已进入等待单元使用的脚本。V0/V1 五个原始对象逐字节相同。留出集共 177 个 TU、9 个软件包，训练集来源文件和输入 SHA256 均无交集。

## 第 0 步 · 157 manifest 状态

**集成保留 UNQUALIFIED，生产打包仍要求 READY。** A 和 B 的 QB 专用测试提交只在选择打包 manifest 时显式传入 `allow_unqualified=True`。B 原样使用 G8 的 manifest。测试提交说明注明临时例外。SHA256、大小、项目及开关映射、重复映射、重复 JSON 字段及占位拒绝均沿用现有打包代码。

候选推送前，157 会调用集成提交的打包脚本，核对它对同一份 UNQUALIFIED manifest 以状态检查失败。测试提交的打包脚本须能解包并通过原有身份校验。另逐字核对集成脚本与配方、测试脚本与三处预期变更。A、B 的原准入继续生效。

[脚本 diff](../../tools/bolt/results/task158/157-manifest-status.diff) · [单测日志](../../tools/bolt/results/task158/157-manifest-tests.txt)

10/10 单测通过。初跑夹具误用会主动拒绝占位内容的打包器，并把命令行项目参数的错误码误期望为 1。修正两处夹具后重跑。157 等待单元于 04:14 PST 恢复，继续等待 G4。

## 第 1 步 · 154-B RPM 核对

- B1 的基线 clang RPM 为 `clang-22.1.8-1.x86_64.rpm`，69,200,093 B，SHA256 `5cfec198849eb1042f11dd2036b1e4df5956cba14c67aea595922f67d35fa1ad`。脚本在查询前重核身份，保存两份 `rpm -qp --requires` 的原文和差集。新增 Python 相关依赖即 FAIL。
- 脚本列出 clang 的 `/usr/lib/libscanbuild` 和 `/usr/lib/libear` 文件。若存在字节码，每个 Python 源文件须有对应字节码，额外的孤立缓存也会失败。字节码全部缺席允许通过。RPM 日志中的 `Installed (but unpackaged) file(s)` 仍会导致失败。
- `analyze-build --help`、`intercept-build --help`、`scan-build-py --help` 各保留结果与输出。运行环境缺失时按工具分别登记原因。
- 7/7 测试通过。首跑发现缓存名识别把优化级别误当作模块名的一部分，修正识别后复测。实际 RPM 与功能测试结果由 154-B 构建产出。

[154-B 核对 diff](../../tools/bolt/results/task158/154-build-checks.diff) · [单测](../../tools/bolt/results/task158/154-audit-tests.txt)

## 第 2 步 · 基准工具

每批次切换同一私有根路径和同一个普通文件形式的加载器。第一轮仅切换符号链接，Clang 从 `/proc/self/exe` 得到解析后的原加载器路径，五个原始对象均不同，移除 `.GCC.command.line` 的诊断比较均相同。加载器改用固定的普通文件路径后，五个原始对象均相同，包含 3 个 C TU、2 个 C++ TU。

每个变体完成一轮不计分预热。主指标使用 user+sys，墙钟为辅助指标。墙钟超过 CPU 的 1.5 倍且绝对差超过 1 秒的样本，在同轮末尾重跑一次，保留两个记录。重复仍异常的样本所在批次退出总时间统计。安静和有干扰组按轮首尾采集的构建进程名划分，双方均记录 loadavg。通用进程名无法确认项目归属，另一项目字段留为 UNKNOWN。

复测使用 CPU 19、单 worker、1 个测量轮，归入有干扰组，仅用于工具与正确性验证。12/12 单测通过。

[首次复测 JSON](../../tools/bolt/results/task158/five-tu-symlink-only.json) · [固定加载器复测](../../tools/bolt/results/task158/five-tu-results.md) · [基准工具单测](../../tools/bolt/results/task158/bench-tests.txt)

## 第 3 步 · 留出语料

从 Base-Dev 固定快照 `tizen-base-dev_20261030.061217` 获取源码 RPM，先运行 `rpmbuild -bp` 应用打包补丁。CMake 编译数据库、配置后的 `make -n` 命令和 tinyxml2 的 Meson 目标提供逐 TU 参数。配置只运行编译器探针和依赖探测，实际语料用匹配的 Tizen Clang、sysroot 和 `-E` 生成。常规参数取自快照构建配置，去掉两个 GCC 专用参数。所有语料统一 `-O2`。记录完整配置命令、实际预处理命令、编译输入参数和本地文件路径。CMake 可用的可选库以留存 sysroot 为准。

对照 server-kit 与实际训练清单的 23 项身份，并复核训练输入的字节和 SHA256。从预处理文件第一条源标记提取原始文件身份，合成输入使用原始源码路径。对保留与新生成的每个 TU 同时比较规范化来源文件、保守的源文件 basename 和输入 SHA256。177/177 个输入重核通过，训练重叠 0，项目内重复来源 0。

| 类别 | 数量 |
|---|---:|
| 全部 TU | 177 |
| 本次新增 TU | 147 |
| C / C++ | 87 / 90 |
| 小于 256 KiB / 至少 256 KiB 且小于 8 MiB / 至少 8 MiB | 75 / 97 / 5 |
| 语料占用 | 229,749,282 B |

| 软件包 | TU |
|---|---:|
| bzip2 | 7 |
| expat | 4 |
| icu | 76 |
| jsoncpp | 3 |
| libwebp | 55 |
| llvm | 10 |
| sqlite | 1 |
| tinyxml2 | 1 |
| zlib | 20 |

最小 36,652 B，最大 19,739,071 B。30 个旧 TU 沿用 156 的恢复收据。新增输入来自七个 Base-Dev 源码包。Expat 的 dry-run 在后续目标上退出 2，已输出的四条编译命令可独立复核，四个预处理均成功。所有新增数据保留在本地 `archive/task158/corpus/`，逐项字节和 SHA256 在清单中。

[语料与逐项身份清单](../../tools/bolt/results/task158/corpus-config.json) · [训练源身份](../../tools/bolt/results/task158/corpus-training-identity.json) · [预处理命令](../../tools/bolt/results/task158/corpus-preprocessing.json) · [固定快照源包索引](http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Dev/tizen-base-dev_20261030.061217/repos/standard/source/)

## 第 4 步 · 调度

154-B 仍先等 151、153 都退出且各自最终证据已推送，同时要求 158 语料收据进入终态且无语料包构建运行。04:25:43 PST 写出 PASS 收据。本次语料工作只需配置、依赖探测和预处理，未排队任何包构建，也未使用 3 小时构建预算。154-B 磁盘及内存准入保留，最终截止为 2026-11-27 20:00 PST。157 保持独立，仅按原有 G 链状态触发。

[等待脚本 diff](../../tools/bolt/results/task158/154-corpus-schedule.diff) · [语料交接收据](../../tools/bolt/results/task158/corpus-state.json)
