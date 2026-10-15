# 25 sandbox 收拢与真实树安装演练

日期：2026-10-15，Asia/Shanghai。源提交 `506dc25c86e4e2154150796d10b77b71d71ad6bb`，父 `67619ec8bbbac7238a6cfc33a481ccfbcd12206f`。未修改源码，未推 refs/for 或 tizen_base。

## A：分支收拢

PASS。明确租约 `ad8a2606ec3c9e53b657f3f8261be9f7d63b23c8` 的 force-with-lease 推送后，bolt_pgo 已等于最终源提交；v2 删除后查询不存在。GitHub 首阶段提交 `905b14f`。

长期人工裁决：BOLT 只使用 sandbox/lhmax2025/bolt_pgo。后续不新建 sandbox 分支；变基更新只允许该分支以当前完整远端 SHA 为租约强推，其他分支一律不强推。

其他分支只读登记如下，均未删除或更新：

| 分支后缀 | SHA | 提交标题 |
| --- | --- | --- |
| libcxx-ehabi-backport | 5c169afc97945bfb88786d9f38477f6973fe5285 | Build static libc++ and libc++abi archives for clang toolchains |
| libcxx-migration | 2d23367d74afbf2bb1e9e4013fce072b3a154109 | packaging: select Clang explicitly for libc++ runtimes |
| lld | 120afe9cd158e5de9fe26d4282785c5d59c657bc | clang: use lld as the default linker |
| llvm_only_clang | f8277158cf44f872e2b2d62a2e839cb33bd0afea | jenkins: fail fast when the CTMark preflight fails |
| mlgo | 08ffd8cd7c72f5dd6e612d8395362def96d84029 | test: close PR-3 fallback IR extraction gaps |
| mlgo_aot | 88ff57cadcff52ab50ca6865db7faed7388358fe | packaging: pin EIGEN_NEON_GEBP_NR=4 for the aarch64 XLA AOT runtime |

## B：真实树演练

执行中。下层为 W/temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0，真实树自身宏包含 _toolchain。上层/工作/合并目录均在 W/temp/bolt-v4-20261015-install-rehearsal，项目 O_EXCL 锁与共享 flock 双锁。单次完整包装器负责挂载、chroot abuild、卸载；未在下层运行 cmake/ninja/-P。

资源上限沿用 docs/38：18 GiB（19,327,352,832B）、swap0、nice15/ionice3，find-debuginfo -j4，BOLT -j1。沿用本任务准入 MemAvailable≥12 GiB，运行<3 GiB 即停止；共享锁3500秒安全截止。空间预算274,432,007,480B，入口318,858,526,720B，预算后44,426,519,240B≥30GiB，运行时低于30GiB终止。原缓存61文件/14,977,512B；预算包括110GiB缓存写入。

准备修正：下层旧BUILDROOT为空，预产品阶段改用已认证完整22包合并载荷估算并按全载荷另计一次debuginfo；首次sudo的askpass因Snap GTK/GIO库冲突未启动密码框、未接收密码、未提权或挂载，保留原文并按环境错误一次修正，只清理askpass的六个图形/库变量，非特权zenity --version=4.0.1。修正后一次图形输入认证成功，所有挂载与卸载在同一次成功sudo调用中。首次准备读SHA/测量仅nice19/ionice3、未加cgroup cap；复算预算在4GiB/swap0轻scope，实际演练全在18GiB scope。此准备资源偏差不隐去。

完整执行结果与raw索引收尾补齐。

## B1/B3 身份与输入

下层 BUILD 全清单240,718路径；关键六SHA已保存，原clang-22为d25e99607c9ea23bf2e50da5075c21f0145f6da24a39a4228d2fd8026ead70cf（该历史根自己的构建产物，不冒称7df本树）。实际编译器解析/bin/clang、/bin/clang++；PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin。未复用坏配置的/var/tmp树。

| 输入 | 字节 | SHA256 |
| --- | ---: | --- |
| llvm.spec | 26530 | 5fb99b761b1de26aebdf6c7d47f303acbdb91acd38dab76c2b9da934f5070e92 |
| clang-bolt-helper.py | 67624 | ff138400be3f10c2c71acd88c17fc8a221ecf9872bff1578460976de981d4158 |
| clang-bolt-v2.fdata.xz | 9735212 | 52fd8522b8cceadebfb6bfc0a19f721f1072cff95c682b12b2c4dd5b0cc1e27f |
| llvm-static-archives-native.py | 40749 | 6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557 |
| llvm-22.1.8.tar.gz | 258009434 | 1f5fe8da0a18255a63cde36f1570c88265bb8ffc6458deae06d04e77abc6f7d2 |
| llvm.manifest | 189 | 55449a170ea90537532d2fd52a2e2f7c9a53dbcb6b1894c8a321c53a8685524d |
| mlgo_arm_model.tar.gz | 28477748 | dd468cce897c7f578b38668e9d869c6785f3fdbcf97879fd7775b430bd0a3a9a |
| mlgo_aarch_model.tar.gz | 30461764 | 76f896dfdce3fa19d0ed467554ed3a643f062f52b4a4db81f576d04c469014a1 |
| mlgo_x86_model.tar.gz | 28652731 | 6c221a08aa63f80c3d82713ba968125797f16351c258a174fc0eec6fdffdbf43 |

前四项直接来自506dc25的Git对象；其余Source复用下层同名原件，经合并根读取再次校验。未解包或修改源码。

## B4 首个真实门禁：PASS

普通安装、preflight/certified、BOLT_BUILDROOT_OK/BOLT_PROC_OK均成功。安装根快照5,429路径。真实dry-run恰113条：BOLT对象102、静态库7、可执行1、生成任务1，另TF刷新2；ninja_diagnostics为空、计数0。tool-plan PASS，没有其他任务。工具构建前bin/llvm-bolt不存在；TF归档f15c565d30a981c22c71cbcf823030302cf51d19a381f4cc82e44626688be1ed与预构建归档相同。正在执行真正-j1构建，尚不能宣称tool-verify或pipeline通过。

实际rpmbuild生成的完整install/post脚本已捕获。额外同UID宿主监护覆盖helper独立session，资源中止时清理abuild进程而保留root包装器做卸载审计；55分钟停止计算任务，为单次60分钟持锁保留5分钟清理时间。它不改变产品命令或门禁。
