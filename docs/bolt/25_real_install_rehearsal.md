# 25 sandbox 收拢与真实树安装演练

日期：2026-10-15 至 2026-10-16，Asia/Shanghai。源提交 `506dc25c86e4e2154150796d10b77b71d71ad6bb`，父 `67619ec8bbbac7238a6cfc33a481ccfbcd12206f`。未修改源码，未推 refs/for 或 tizen_base。

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

## B：发现问题（本地演练时限中止，未完成）

停止步骤：只带 emit-relocs 的 clang 重链。宿主监护按55分钟计算截止主动SIGKILL abuild进程，预留卸载/审计时间，原文：

```text
shared lock 3300-second deadline, leaving 300 seconds for cleanup/audit
```

没有观测到源代码产品门禁失败。rpmbuild退出码-9来自上述资源时限终止，不是匹配度、strip、安全属性或post失败；这些步骤尚未运行。本地结果不能据此断言QB会失败。本根初始缓存仅61文件/14,977,512B，与历史温缓存预演条件不同；不把耗时差异作为QB必败证据。

## 执行范围与结果

下层：W/temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0；这是docs38历史构建树，不称作67619ec8新构建物。仅将506dc25的spec/helper/profile/converter作为演练输入，不改源码。upper/work/merged均为本会话新目录、同一文件系统，所有写入在overlay；未在下层或坏配置的/var/tmp树运行cmake/ninja/-P。

成功认证的一次sudo -A调用包办overlay、/proc、临时/dev及必要节点、chroot abuild、卸载。原RPM入口PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin，clang/clang++解析/bin/clang和/bin/clang++；宏_toolchain=clang，debug模式，_smp_mflags=-j4。完整argv、实际生成install/post脚本和原始日志均保存。

| 项目 | 结果 | 事实 |
| --- | --- | --- |
| 普通CMake安装 | PASS | install-before.json为5,429路径；仅执行一次普通安装 |
| preflight/certified | PASS | Python3.14.2，LLVM22.1.8，认证111 BOLT+2 TF；profile未压缩SHA d9b132f9… |
| 路径与proc | PASS | BOLT_BUILDROOT_OK、BOLT_PROC_OK；没有MISSING |
| 真实dry-run/tool-plan | PASS | 总113：102对象、7静态库、1可执行、1生成，另TF刷新2；ninja_diagnostics=[] |
| 实际-j1构建/tool-verify | PASS | BOLT_NINJA_EXIT_0；planned=executed=113；工具此前不存在、本次产出true |
| TF归档 | PASS | 前后及预构建归档均f15c565d30a981c22c71cbcf823030302cf51d19a381f4cc82e44626688be1ed |
| clang emit-relocs重链 | INTERRUPTED | 计算截止时仍未结束，不能视作合格BOLT输入 |
| strip-debug/BOLT匹配/标识/strip-all/安全/两次tiny | NOT RUN | N/M/S/U/Q、R、S/N与候选SHA均未知；没有BOLT_PIPELINE_PASS |
| compare-root | NOT RUN | 无BOLT_COMPARE_ROOT_PASS |
| 静态归档转换及候选install | NOT RUN | 未执行；保全的构建目录summary是历史docs38记录，与旧摘要相同，不能冒作新输出 |
| 平台后处理及post尾检 | NOT RUN | find-debuginfo实际执行0次；无BOLT_POST_GATE_PASS；post路径/cmake计数未知 |
| 最终ninja no-work | NOT RUN | 按停止规则未在中止后继续产品步骤；不伪造no-work原文 |
| 卸载/进程/锁/下层审计 | PASS | 见下节；全部成功回收，未延长持锁上限 |

树内工具SHA `34686c3362e736763cf0a1a6a44bb54b4d2e5cc34e58322477f2fa63696259fc`。实际版本原文：

```text
LLVM (http://llvm.org/):
  LLVM version 22.1.8
  Optimized build.
BOLT revision <unknown>

  Registered Targets:
    x86    - 32-bit X86: Pentium-Pro and above
    x86-64 - 64-bit X86: EM64T and AMD64
```

历史候选4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9未重新生成或修改；本次没有新候选，故无法作SHA或匹配统计对照。

## 资源与耗时

上限沿用docs38：18GiB（19,327,352,832B）、swap0、nice15/ionice3，BOLT-j1，后处理预定-j4。准入沿用任务MemAvailable≥12GiB，运行<3GiB即停；重锁等待≤2h，本次立即取得。预算274,432,007,480B，写前free318,858,526,720B，投影44,426,519,240B≥30GiB；包含普通安装、额外完整debuginfo、归档转换、110GiB缓存和24GiB BOLT工作。运行时继续守30GiB底线。

| 阶段 | 观测区间秒 | cgroup current采样最大GiB | 最大观测进程VmHWM GiB |
| --- | ---: | ---: | ---: |
| ordinary-install | 823.129 | 6.805 | 0.121 |
| snapshot | 401.241 | 6.709 | 0.151 |
| bolt-configure | 34.760 | 6.429 | 0.285 |
| tool-dry-run | 1.217 | 6.272 | 0.121 |
| tool-build | 341.865 | 8.318 | 5.805 |
| pipeline | 1622.401 | 11.091 | 10.410 |

每0.5秒请求采样，阶段间隔及短进程可能漏采；阶段current最大值为观测峰，不冒称逐阶段重置的内核峰。memory.peak为累计内核峰，原文与实际时间戳均保留。

全scope内核峰11920756736B（11.102GiB）；最大观测VmHWM 10915560KiB（10.410GiB）。宿主最低可用5.581GiB；文件系统最低free236.253GiB、可用量下降高水位60.707GiB（共享文件系统观测，不等于上层独占精确写量）。memory.events全0，没有OOM或低内存/低磁盘中止。

本次rpmbuild/%install尝试总耗时3228.039秒（53.801分钟），未到完整post结束；本次持锁3374.417秒（56.240分钟）<60分钟，首次askpass未启动的独立锁尝试0.556秒。

## 清理与保全

卸载失败0；最终mountinfo中无本会话挂载，scope/cgroup已消失，abuild存活成员0。项目O_EXCL锁按拥有者匹配删除，flock释放。下层BUILD共240,718路径的类型/大小/mtime/链接目标清单前后完全一致，压缩清单SHA同为ee0e3adffe0c54a048236af45bebb4af1b2166edf16f5947371dbee00c856c19；CMakeCache/build.ninja/.ninja_log/.ninja_deps/clang-22/TF归档六个SHA逐项相同。

上层完整保留至周五2026-10-16待用户处置，未删除任何载荷；计量见upper-retained.json。归档证据与22RPM均只读，未进入ARM树，S源工作树仍干净且HEAD=506dc25。没有Gerrit评审/tizen_base推送或QB操作。

## 准备纠正与边界

1. 下层旧BUILDROOT为空，产品步骤前发现零安装量估算不可用，改用已认证完整22包合并载荷取整，并另计完整debuginfo一次；此类修正1次，原始暂算保留。
2. 首次askpass受Snap GTK/GIO环境污染，zenity在显示密码框前发生GLIBC_PRIVATE链接错误，没有接收密码、提权、挂载或产品操作。环境类修正1次：仅askpass清理六个库/GTK/GIO变量；非特权zenity --version=4.0.1后，一次实际图形输入成功。首次失败sudo及日志完整保留；不是用户取消/输错后重试。所有挂载、运行、卸载都在同一次成功sudo调用内。
3. 补充同UID宿主进程监护，覆盖helper另开session的后代；截止时SIGKILL六个abuild进程，存活0，保留root包装器清理。没有改变产品参数、候选生成路径或门禁。
4. 首次只读Git输入SHA/空间测量用了nice19/ionice3，但未加4GiB cgroup；这是准备资源设置偏差，不能隐去。复算预算及最终压缩/整理在4GiB/swap0轻scope，实际演练18GiB/swap0；原文保存。已有文件查找先rg--files，W/temp默认忽略时改用find定位，没有产品用错输入或环境。

5. 收尾报告的Python百分号格式化将%install误当作格式控制，提交前修正1次并保留原始stderr；未影响产品结果。

## 输入SHA

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

前四项来自506dc25 Git对象，合并根复核相同；其余Source复用下层同名原件。完整raw见10_raw_links_part7起的续表，包含分支版与钉提交版。
