# 自研优化版 x86_64 LLVM：固定快照、限流构建与基线

更新时间：2026-09-17T11:21:28+08:00。

## 1. 状态与范围

**BLOCKED：编译和链接完成，但 RPM debuginfo 阶段触发 18 GiB cgroup OOM，未产出 RPM。** 当前唯一源码基线是工作区 LLVM
`f111162e94aa48ed367c9d2c039456c70e7160ae`。没有回退到已安装 RPM 的构建配方。
使用原生 x86_64 GBS 构建，保留 spec 的 -O3、ThinLTO、-fomit-frame-pointer、
静态链接 LLVM 库及 MLGO 设置。源码侧只允许三处并发数字变化。

本次已将 Base 和 Unified 分别固定为其 reference 当前实际指向的快照，
完整预检通过，随后真实执行 `tools/build_llvm_x86_64.sh --run`。
资源守护、配置门禁和日志机制沿用已有脚本，未改动 tools/ 中的实现。
不构建 Chromium，不向 Gerrit 推送。

验证体系分两层：本机基准台用于分钟级筛选 LLVM 变体；最终验收是专用构建服务器
的 Chromium 全量构建耗时。本机不做后一层。本次 clang 22 与新增真实 TU 输入集
必须重新校准，不能沿用 docs/12 的 clang 18 噪声结果。

路径约定（均是本机真实路径）：

| 符号 | 路径 |
| --- | --- |
| W | `/home/linhao/Toolchain/development/llvm-optimize` |
| S | `W/llvm/packaging/llvm.spec` |
| Q | `W/temp/snapshot-resolution-20260917` |
| A | `W/temp/snapshot-archive` |
| P | `W/temp/baseline-preflight-20260917` |
| L | `W/temp/baseline-build-20260917` |
| B | `W/temp/gbs-root-x86_64-baseline` |
| U | `A/tizen-unified-toolchain_20260814.092727/build.conf` |

## 2. reference 解析与固定快照

先取得两个项目的目录索引和 reference 目录索引，沿索引中的 `build.xml` 链接读取
根元素下的 `<id>`，再请求同名快照的 `repos/standard/packages/repodata/repomd.xml`。
**reference 和固定快照的 repomd.xml 按完整字节比较相等**；归档后再次获取 reference
并比较，确认解析期间没有发生切换。日期来自 XML 的 id，没有根据修改日期推断。

原始 XML 摘录（Q/*-reference-build.xml，全文亦在 Q/resolution.log）：

```xml
<id>tizen-base-toolchain_20260912.061113</id>
<base_id url="http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/">reference</base_id>

<id>tizen-unified-toolchain_20260814.092727</id>
<base_id url="http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/">tizen-base-toolchain_20260813.050338</base_id>
```

Unified 的 `base_id` 是它原始构建时的 Base 身份，不能误当成 Unified 自己的快照 id。
本任务按决策固定两个 reference 各自当前的目标，不擅自改选该历史 base_id。

| 项目 | 已解析快照 | reference / 快照 HTTP | repomd.xml SHA256（双方相同） |
| --- | --- | --- | --- |
| Tizen-Base-Toolchain | `tizen-base-toolchain_20260912.061113` | 200 / 200；二次复核仍一致 | `68b93454b4800a462e228260b11926a63ad8bba0589cc3f1a7dc4f0525bc2a74` |
| Tizen-Unified-Toolchain | `tizen-unified-toolchain_20260814.092727` | 200 / 200；二次复核仍一致 | `e7af3f222f0ce958678d964589f2d156e8b47ba463ac0b3b0b96c74663382200` |

完整 GET URL、时间、HTTP 状态、字节数、SHA256、XML 原文和 RESOLVED 记录在
Q/resolution.log；解析脚本保存在 Q/resolve.py。以下为实际包源：

- https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260912.061113/repos/standard/packages/
- https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260814.092727/repos/standard/packages/

### 配置变更

改前 SHA256：`6696073dc5a459c5b90ed51d1a5d9c90eb1505d3989615ea729f993e046deb50`
改后 SHA256：`a3fea7732532db26c11b88407464e0274a6d8b4277623364fe16b6980181b03f`

改动仅涉及 URL 行：删除失效的重复 URL 与历史 URL 注释，每节保留一个固定快照 URL。
未改变 profile、repo 顺序或 general.buildroot；命令行 `-B` 指定本次全新构建根。
改前/改后原文件分别保存在 Q/gbs_llvm.conf.before 和 Q/gbs_llvm.conf.after。
完整 diff（Q/config.diff）：

```diff
--- a/gbs_llvm.conf
+++ b/gbs_llvm.conf
@@ -6,11 +6,7 @@
 repos = repo.base-standard, repo.unified-standard

 [repo.base-standard]
-url=https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/reference/repos/standard/packages/
-#url=http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260722.045200/repos/standard/packages/
-url=http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260804.124315/repos/standard/packages/
+url=https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260912.061113/repos/standard/packages/

 [repo.unified-standard]
-url=https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/reference/repos/standard/packages/
-#url=http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260725.003315/repos/standard/packages/
-#url=https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260804.223836/repos/standard/packages/
+url=https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260814.092727/repos/standard/packages/
```

### 元数据归档

每个目录存放 repomd.xml、解压后的 primary.xml、下载到的原始压缩文件、build.conf、
reference-build.xml、比较用的两份 reference repomd，以及包含 URL/摘要的 manifest.json。
下载内容与 repomd.xml 声明的 checksum 逐项相符。元数据用于日后核对，**不是全部 RPM
包的离线镜像**；不会承诺仅凭这些 XML 就能在远端包被清理后重建。

| 归档目录（相对 W） | primary.xml 字节数 | 解压后 primary.xml SHA256 | build.conf SHA256 |
| --- | ---: | --- | --- |
| `temp/snapshot-archive/tizen-base-toolchain_20260912.061113/` | 4079780 | `5cf28889b7f9706281c019898e4c54e93e04c23d5b813f8f42eca03d7da16138` | `b8a19c32e5e153a745e3012da6dca3e3077e6a37b2b76cbf773743b6d8c9ff3c` |
| `temp/snapshot-archive/tizen-unified-toolchain_20260814.092727/` | 21165478 | `beba1f62d83b1ab105ae1a114c8fa6277bc037615c090cef9547489e7e22d286` | `1e7610b6a922d27b80eb59c1c78bdf716f7de2e8e24700e0ee7c62522739ed52` |

这些文件都在被 Git 忽略的 temp/。Unified primary.xml 超过 10 MB，未进入 Git。

## 3. 完整预检结果与 `_toolchain`

实际执行（未带 `--run`），退出码 0：

```sh
tools/build_llvm_x86_64.sh --log-dir temp/baseline-preflight-20260917
```

原始尾部关键输出（Q/preflight-console.log）：

```text
1|clang
[exit=0]
MEMORY MECHANISM systemd
PREFLIGHT PASS; no spec edit and no build. Use --run to proceed.
```

本报告中的上述四行去除了时间前缀；完整原始输出保存在 P/commands.log。
P/repositories.json 记录两个固定源的 HTTP 200、x86_64 包清单及 build.conf 摘要。

### 包与 BuildRequires

先用本机 GBS 后端 Build::read_config("x86_64", U) 和 Build::Rpm::parse 解析 S，
保留 GBS 的 `opensuse_bs=0` 定义；这只是读取 spec，不运行构建。
结果见 Q/spec-build-requires.json。随后从归档 primary.xml 的 x86_64/noarch 包名及
RPM provides 中解析直接 BuildRequires，原始匹配输出在 Q/dependencies.log/json。
后续整个依赖闭包由真正 GBS 的依赖展开和安装检查。

| Base 必须存在的 x86_64 包 | 实际版本-Release | 结果 |
| --- | --- | --- |
| clang | 22.1.8-1.6 | PASS |
| llvm | 22.1.8-1.6 | PASS |
| cmake | 3.31.2-1.2 | PASS |
| ninja | 1.13.1-1.9 | PASS |
| glibc | 2.40-1.10 | PASS |
| rpm-build | 4.14.1.1-1.4 | PASS |
| binutils | 2.43-1.9 | PASS |

| spec 实际 BuildRequires | 提供包（均来自固定 Base） | 版本-Release |
| --- | --- | --- |
| cmake | cmake.x86_64 | 3.31.2-1.2 |
| python3 | python3.x86_64 | 3.14.2-1.6 |
| python3-devel | python3-devel.x86_64 | 3.14.2-1.6 |
| patchelf | patchelf.x86_64 | 0.16.1-1.8 |
| binutils-devel | binutils-devel.x86_64 | 2.43-1.9 |
| libxml2-devel | libxml2-devel.x86_64 | 2.15.1-1.7 |
| ninja | ninja.x86_64 | 1.13.1-1.9 |

S:51–60 的 sed 在 `llvm_release_build=1` 分支，本次分支为 0，故不是本次实际
BuildRequires。所有实际 7 项均通过，没有用“按惯例存在”填空。

### 宏来源

GBS 按 gbs_llvm.conf:6 的 repo 顺序读取 repomd 中的 build 元数据，最后的 Unified
配置生效。实现依据：`/usr/lib/python3/dist-packages/gitbuildsys/utils.py:430–447,463–496`。
本次重新下载的 U:146–184 是非架构专属的 Macros 段，其中：

```text
150 %__cc_clang %{_host}-clang
151 %__cxx_clang %{_host}-clang++
161 %_toolchain %{?_toolchain_override}%{!?_toolchain_override:clang}
166 %__cc %{expand:%%{__cc_%{_toolchain}}}
167 %__cxx %{expand:%%{__cxx_%{_toolchain}}}
```

用 `/usr/lib/build/queryconfig --dist U --archpath x86_64 rawmacros` 得到宏文件，
再用 `rpm --macros /usr/lib/rpm/macros:<生成文件> --eval '%{defined _toolchain}|%{_toolchain}'`
实际得到 `1|clang`。P 与 L 的 commands.log 都记录了本次复核。
因此 S:11–16 取真分支，`_toolchain_override=clang`、`llvm_release_build=0`，
S:229–236 的 lld/ThinLTO/llvm-ar/llvm-ranlib 参数应生效。
没有增加 `--define _toolchain`。

U:121–127 的 mlgo_build_jobs=6 只在 armv7l/aarch64 分支，x86_64 不被其覆盖。
S:7–8 自己默认启用 x86_64 MLGO；S:48 的默认任务数可按允许范围调整。

## 4. 资源、并发、实际启动命令

构建前原始资源输出（L/commands.log，实际启动前又重新检查精确值）：

```text
2026-09-17T08:43:32+08:00 $ nproc
2026-09-17T08:43:32+08:00 20
[exit=0]
2026-09-17T08:43:32+08:00 $ free -g
2026-09-17T08:43:32+08:00                total        used        free      shared  buff/cache   available
Mem:              30           7           9           0          14          22
Swap:              3           0           3
[exit=0]
2026-09-17T08:43:32+08:00 $ df -h /home/linhao/Toolchain/development/llvm-optimize/temp
2026-09-17T08:43:32+08:00 Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       1.8T  672G  1.1T  39% /home
[exit=0]
2026-09-17T08:43:32+08:00 $ nproc
2026-09-17T08:43:32+08:00 20
[exit=0]
2026-09-17T08:43:32+08:00
```

精确资源值：MemAvailable = 24485412864 B = 22.803818 GiB；
可用磁盘 = 1146346184704 B = 1067.618080 GiB。
均通过 16 GiB / 60 GiB 门槛，见 L/resource-plan.json。

| 限制 | 实际设置 | 依据 |
| --- | --- | --- |
| systemd MemoryMax | 18 GiB | floor(可用 GiB) - 4，预留至少 4 GiB |
| MemorySwapMax | 0 | 不让构建 scope 通过 swap 扩张内存 |
| GBS 包并发 | 1 | --threads 1 |
| Ninja 总任务数 | 4 | S:48 |
| LLVM compile/link 池 | 4 / 1 | S:274–275 |
| 链接内存预算 | 1 × 8 GiB < 13.682291 GiB | 严格小于可用内存的 60% |
| 其余预算 | 编译 4 × 2 GiB + 开销 2 GiB | 与链接合计 18 GiB；编译 2 GiB 是预算假设，不是实测 |
| CPU / I/O 调度 | nice 15 / ionice idle（-c3） | L/runtime-scope-check.log、L/priority-check.log 实测 |

本次仅修改的 spec diff（L/spec-concurrency.diff）：

```diff
diff --git a/packaging/llvm.spec b/packaging/llvm.spec
index 54a07ce84218..6e159c542234 100644
--- a/packaging/llvm.spec
+++ b/packaging/llvm.spec
@@ -45,7 +45,7 @@ Source1002: mlgo_arm_model.tar.gz
 Source1003: mlgo_aarch_model.tar.gz
 Source1004: mlgo_x86_model.tar.gz

-%{!?mlgo_build_jobs: %define mlgo_build_jobs 6}
+%{!?mlgo_build_jobs: %define mlgo_build_jobs 4}
 %{!?mlgo_verify_configure_only: %define mlgo_verify_configure_only 0}

 BuildRequires: cmake
@@ -271,8 +271,8 @@ cmake \
     -DLLVM_LIBDIR_SUFFIX=`echo %{_lib} | sed s/lib//g` \
     -DCLANG_RESOURCE_DIR="../%{_lib}/clang/%{llvm_version}" \
     -DLLVM_BINUTILS_INCDIR=/usr/include \
-    -DLLVM_PARALLEL_COMPILE_JOBS=6 \
-    -DLLVM_PARALLEL_LINK_JOBS=2 \
+    -DLLVM_PARALLEL_COMPILE_JOBS=4 \
+    -DLLVM_PARALLEL_LINK_JOBS=1 \
 %if %{with mlgo}
 %ifarch armv7l aarch64 x86_64
     -DTENSORFLOW_AOT_PATH="${MLGO_AOT_DIR}/mlgo_sysroot" \
```

真实执行入口：

```sh
tools/build_llvm_x86_64.sh --run --log-dir temp/baseline-build-20260917
```

脚本在执行前输出的完整底层命令（L/launch.json、commands.log）：

```sh
/usr/bin/time -v -o /home/linhao/Toolchain/development/llvm-optimize/temp/baseline-build-20260917/time-v.txt systemd-run --user --scope --unit=llvm-baseline-ce682bfbada047fcb575eaeebd4993ba.scope -p MemoryMax=18G -p MemorySwapMax=0 nice -n 15 ionice -c3 gbs -c /home/linhao/Toolchain/development/llvm-optimize/gbs_llvm.conf build -A x86_64 -B /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-baseline --threads 1 --include-all -D /home/linhao/Toolchain/development/llvm-optimize/temp/baseline-build-20260917/buildconfig.conf /home/linhao/Toolchain/development/llvm-optimize/llvm
```

`-D` 指向已下载并复核的原始 build.conf，内容没有增删宏；`--include-all` 让三处
并发修改进入源码导出。源工作树在启动前经过检查，其他源码/spec 内容没有改变。
GBS scope 实际名为 `llvm-baseline-ce682bfbada047fcb575eaeebd4993ba.scope`。

### 守护与实测内存

脚本后台线程每 30 秒落盘 free -m 原文、loadavg、进程树 RSS 总和、PID 清单及 cgroup
内存属性；每 2 秒检查 MemAvailable，小于 2 GiB 立即中止并保留现场。
正常退出、失败及可捕获中断均在 finally 中 join 采样线程；结果写 outcome.json。
本机 systemd 用户 scope 可用，实际使用 cgroup 聚合内存上限，没有走 prlimit 后备。

截至本次报告生成：采样 306 次，可用内存最低 7.997826 GiB；
进程树 RSS 求和最大 18427691008 B（17.162125 GiB）；从有效 scope 采样读到的
MemoryPeak 最大 19327352832 B（18.000000 GiB），与结束后的 systemd 属性一致。RSS 求和
重复计共享页，cgroup 用量还包括文件缓存，两者不能混用。306 次记录是离散采样，
不能把采样极值当成连续监测的精确 RSS 极值。采样器未触发 MemAvailable < 2 GiB；
此次停止由 cgroup 的 18 GiB 上限先触发。

实际退出记录：

```json
{
  "exit_code": 143,
  "elapsed_seconds": 9222.385007260134,
  "cache_passed": true,
  "problems": [],
  "sampler_reaped": true,
  "log_reader_reaped": true,
  "interrupted": null
}
```

外层 time -v 原文：

```text
Command terminated by signal 15
	Command being timed: "systemd-run --user --scope --unit=llvm-baseline-ce682bfbada047fcb575eaeebd4993ba.scope -p MemoryMax=18G -p MemorySwapMax=0 nice -n 15 ionice -c3 gbs -c /home/linhao/Toolchain/development/llvm-optimize/gbs_llvm.conf build -A x86_64 -B /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-baseline --threads 1 --include-all -D /home/linhao/Toolchain/development/llvm-optimize/temp/baseline-build-20260917/buildconfig.conf /home/linhao/Toolchain/development/llvm-optimize/llvm"
	User time (seconds): 0.14
	System time (seconds): 0.06
	Percent of CPU this job got: 0%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 2:33:40
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 102148
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 10
	Minor (reclaiming a frame) page faults: 22099
	Voluntary context switches: 2042
	Involuntary context switches: 7
	Swaps: 0
	File system inputs: 14752
	File system outputs: 4008
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
```

### 构建结束与失败原因

| 阶段 | 本地时间（2026-09-17，UTC+08:00） | 结果与证据 |
| --- | --- | --- |
| 启动 GBS | 08:43:40 | L/launch.json、commands.log |
| CMake 门禁 | 启动后 297.775 秒 | PASS，L/cache-gate.json |
| 全部 Ninja 任务完成 | 11:02:35 | `[7634/7634]`，L/build.log:10854 |
| RPM `%install` | 11:02:36 | L/build.log:10856 |
| debuginfo 提取开始 | 11:12:39 | `find-debuginfo.sh -j40`，L/build.log:16442 |
| cgroup OOM | 11:17:20 | L/kernel-oom.log、scope-journal.log |
| 控制脚本结束 | 11:17:22 | 外层构建返回 143；脚本返回 2，L/stopped.json |

整个流程外层 `/usr/bin/time -v` 的 wall 是 **2:33:40**；控制器连同收尾是
**9222.385 秒**。其 `Maximum resident set size = 102148 KiB`、user/sys = 0.14/0.06 秒
只反映这次被信号终止的外层进程所取得的资源统计，**不是 LLVM 构建的峰值和 CPU
消耗**。完整构建范围采用 systemd MemoryPeak = **18 GiB**、CPUUsageNSec =
68291713114000；另报告 30 秒采样的 RSS 求和峰值 **17.162125 GiB**。
time 输出同时含 `Command terminated by signal 15` 和 `Exit status: 0`，不得将末行
解释为构建成功；控制脚本的实际退出记录是 143/2，scope 结果是 `oom-kill`。

结束后的 systemd 原始属性（L/scope-final.log）：

```text
Result=oom-kill
OOMPolicy=stop
ControlGroup=
MemoryPeak=19327352832
MemorySwapPeak=0
CPUUsageNSec=68291713114000
ActiveState=failed
SubState=failed
```

内核原始关键行（L/kernel-oom.log）：

```text
Sep 17 11:17:20 linhao-linux kernel: eu-strip invoked oom-killer: gfp_mask=0x101cca(GFP_HIGHUSER_MOVABLE|__GFP_WRITE), order=3, oom_score_adj=100
Sep 17 11:17:20 linhao-linux kernel: memory: usage 18874368kB, limit 18874368kB, failcnt 85551
Sep 17 11:17:20 linhao-linux kernel: swap: usage 0kB, limit 0kB, failcnt 0
Sep 17 11:17:20 linhao-linux kernel: oom-kill:constraint=CONSTRAINT_MEMCG,nodemask=(null),cpuset=/,mems_allowed=0,oom_memcg=/user.slice/user-1000.slice/user@1000.service/app.slice/llvm-baseline-ce682bfbada047fcb575eaeebd4993ba.scope,task_memcg=/user.slice/user-1000.slice/user@1000.service/app.slice/llvm-baseline-ce682bfbada047fcb575eaeebd4993ba.scope,task=debugedit,pid=2125699,uid=1000
Sep 17 11:17:20 linhao-linux kernel: Memory cgroup out of memory: Killed process 2125699 (debugedit) total-vm:1597988kB, anon-rss:1438880kB, file-rss:60kB, shmem-rss:0kB, UID:1000 pgtables:2884kB oom_score_adj:100
```

内核明确给出 `CONSTRAINT_MEMCG` 和本次 scope 路径：这是构建 cgroup 达到上限，
不是根据 SIGTERM 猜测 OOM。首先被杀的是 debugedit PID 2125699；L/debuginfo-processes.json
保存了其完整 argv，处理对象为暂存目录 `usr/bin/clang-22`。OOM 时内核记录匿名内存
18986385408 B、文件缓存 44343296 B（同一 kernel-oom.log），已不能只靠回收缓存完成分配。
随后 systemd 以 OOMPolicy=stop 停止整个 scope。`No build ID note found` 警告在此之前
出现，但最终中止的证据是 cgroup OOM，不能把这些警告当成已证明的退出原因。

### 已实现限额与本次暴露的缺口

- **聚合内存上限确实生效**：18 GiB、swap 0，OOM 后构建终止。最后一次 30 秒采样
  尚是 oom=0（11:17:10），OOM 发生在 11:17:20；这说明必须结合结束后的 journal，
  不能用最后一次采样的零值否认 OOM。
- **编译/链接并发池生效，但未覆盖 RPM debuginfo 并发**：构建根
  `home/abuild/.rpmmacros:133` 是 `%_smp_mflags -j40`；根内 `usr/lib/rpm/macros:183–184`
  将它传给 find-debuginfo。GBS 的 `--threads 1` 只控制同时构建的包数，
  本机 `gbs build --help` 明确如此说明（L/gbs-build-help.txt:141–142）。
  因此不能声称整个 RPM 流程最多只有 4 个工作进程。
- **8 GiB 单次链接估值偏低**：L/linker-memory-observations.jsonl 中，链接 `bin/clang-22`
  的 lld PID 2099398 已观测 VmHWM=17648684 KiB（16.831 GiB）。这是采到的进程高水位，
  不是完整逐链接内存追踪。它高于 8 GiB 预算，也高于启动可用内存 60% 的 13.682 GiB；
  规划公式按要求的估值通过，**不能据此声称实测也满足该比例**。本次单链接并发已是 1，
  未提高内存上限或改变任何优化参数。之后重跑需要重新审视该预算。
- **CPU/I/O 优先级持续继承**：真实 ld.lld 的 NI=15、ionice=idle
  （L/linker-priority-check.log）；RPM debugedit 也为 NI=15、idle，且 cgroup 路径相同
  （L/packaging-resource-proof.log）。没有因进入 chroot 或打包阶段丢失这些限制。

### 收尾与现场

L/outcome.json 中 sampler_reaped=true、log_reader_reaped=true。结束后遍历 `/proc/*/cgroup`
未发现本 scope 的残留进程，scope 目录已消失（L/cleanup-verification.json）。
systemd 日志曾记录对部分进程发送信号时的 `Operation not permitted`；最终残留检查为空，
所以回收结论依据终态检查，而非忽略该警告。

构建根、源导出、原 build.ninja/.ninja_log、CMakeCache、未剥离的构建树二进制，以及
部分 debuginfo 暂存文件均保留，未清理、未覆盖、未重试。输出位置 `B/local/repos` 与
根内 `home/abuild/rpmbuild/RPMS` 均没有 RPM（L/rpm-output-inventory.json）；缓存里的
依赖 RPM 不是本次 LLVM 产物。结束后磁盘仍有 859G 可用，见 L/final-workspace-checks.log。

## 5. CMake 预期与配置阶段门禁

本次 x86_64 预期参数如下，出处为 S；G 表示根内展开的 `_host`，PFX 表示 `_prefix`，
LIB 表示 `_lib`，此节表中的 A 表示源码目录的 `mlgo_verify_assets`（与归档路径缩写无关）。
不能把宿主 RPM 的 `_host` 当成 Tizen 根的实测 triple。

| 参数 | x86_64 预期 | spec 行号或来源 |
| --- | --- | --- |
| Generator / source | Ninja / `../llvm` | S:219,293 |
| `TIZEN` | 1 | S:220 |
| `CMAKE_C_COMPILER` | `%__cc`，按 U 展开为 `G-clang` | S:221；U:150,161,166 |
| `CMAKE_CXX_COMPILER` | `%__cxx`，按 U 展开为 `G-clang++` | S:222；U:151,161,167 |
| `LLVM_HOST_TRIPLE` | G | S:223 |
| `LLVM_DEFAULT_TARGET_TRIPLE` | G | S:224 |
| `LLVM_TARGET_TRIPLE_ENV` | G | S:225 |
| `CMAKE_ASM_FLAGS` | 清理原 flags 后追加 `-O3 -flto=thin -fomit-frame-pointer` 的 CFLAGS | S:189–206,226 |
| `CMAKE_C_FLAGS` | 同 CFLAGS | S:227 |
| `CMAKE_CXX_FLAGS` | 清理原 flags 后追加 `-O3 -flto=thin -fomit-frame-pointer` 的 CXXFLAGS；必须无 `-Os` | S:197–206,228 |
| `CMAKE_SHARED_LINKER_FLAGS` | `-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections` | S:229–230 |
| `CMAKE_EXE_LINKER_FLAGS` | 同上一行 | S:231 |
| `LLVM_USE_LINKER` | lld | S:232 |
| `LLVM_ENABLE_LTO` | Thin | S:233 |
| `CMAKE_RANLIB` | `%{_bindir}/llvm-ranlib` | S:234 |
| `CMAKE_AR` | `%{_bindir}/llvm-ar` | S:235 |
| `LLVM_ENABLE_ASSERTIONS` | No，即布尔 OFF | S:237 |
| `LLVM_ENABLE_RTTI` | ON | S:238 |
| `CMAKE_BUILD_TYPE` | Release | S:239–240 |
| `LLVM_TARGETS_TO_BUILD` | `X86;ARM;AArch64;BPF` | S:241 |
| `CLANG_ENABLE_ARCMT` | OFF | S:257 |
| `LLVM_BUILD_LLVM_DYLIB` | ON | S:258 |
| `CLANG_BUILD_CLANG_DYLIB` | ON | S:259 |
| `LLVM_ENABLE_PROJECTS` | `clang;lldb;clang-tools-extra;lld;compiler-rt;openmp` | S:260 |
| `LLVM_ENABLE_PER_TARGET_RUNTIME_DIR` | OFF | S:261 |
| `LLVM_BUILD_EXAMPLES` / `LLVM_INCLUDE_EXAMPLES` | OFF / OFF | S:262–263 |
| `LLVM_BUILD_TESTS` / `LLVM_INCLUDE_TESTS` | OFF / OFF | S:264–265 |
| `LLVM_ENABLE_DOXYGEN` | OFF | S:266 |
| `LLVM_BUILD_DOCS` / `LLVM_INCLUDE_DOCS` | OFF / OFF | S:267–268 |
| `LLVM_OPTIMIZED_TABLEGEN` | ON | S:269 |
| `CMAKE_INSTALL_PREFIX` | PFX | S:270 |
| `LLVM_LIBDIR_SUFFIX` | LIB 去掉 `lib` | S:271 |
| `CLANG_RESOURCE_DIR` | `../LIB/clang/22` | S:18,272 |
| `LLVM_BINUTILS_INCDIR` | `/usr/include` | S:273 |
| `LLVM_PARALLEL_COMPILE_JOBS` | 4（本次资源计划已应用） | S:274 |
| `LLVM_PARALLEL_LINK_JOBS` | 1（本次资源计划已应用） | S:275 |
| `TENSORFLOW_AOT_PATH` | `A/mlgo_sysroot` | S:278 |
| `LLVM_MLGO_EXPORT_TF_XLA_RUNTIME` | OFF | S:279 |
| `LLVM_MLGO_EMBED_TF_XLA_RUNTIME_OBJECTS` | A 下的 5 个 XLA runtime objects，见下文 | S:212,280 |
| `LLVM_OVERRIDE_MODEL_HEADER_INLINERSIZEMODEL` | `A/InlinerSizeModel.h` | S:281 |
| `LLVM_OVERRIDE_MODEL_OBJECT_INLINERSIZEMODEL` | `A/InlinerSizeModel.o` | S:282 |
| `LLVM_OVERRIDE_MODEL_HEADER_REGALLOCEVICTMODEL` | `A/RegAllocEvictModel.h` | S:283 |
| `LLVM_OVERRIDE_MODEL_OBJECT_REGALLOCEVICTMODEL` | `A/RegAllocEvictModel.o` | S:284 |
| `LLVM_LINK_LLVM_DYLIB` | 未传，源码默认 OFF | `llvm/llvm/CMakeLists.txt:912` |
| `CLANG_LINK_CLANG_DYLIB` | 未传，默认继承前者，即 OFF | `llvm/clang/CMakeLists.txt:309` |

5 个 runtime object 均位于 `A/xla_runtime_objects/`：
`xla_compiled_cpu_function.cc.o`、`cpu_function_runtime.cc.o`、
`custom_call_status.cc.o`、`executable_run_options.cc.o`、
`runtime_single_threaded_matmul_f32.cc.o`（S:212）。

MLGO 为 x86_64 默认开启（S:7–8），采用 S:165–166 的 x86 模型资产；
因此 S:286–287、290–291 的两个 `MODEL_PATH=none` 分支不在本次预期清单。
`LLVM_TARGET_ARCH` 只出现在其他架构分支；x86_64 未传。
没有擅自增加其他 CMake 参数，也没有使用 configure-only 宏。

两个 LINK_DYLIB 开关的默认 OFF 分别来自 `llvm/llvm/CMakeLists.txt:912` 和
`llvm/clang/CMakeLists.txt:309`。BUILD_DYLIB=ON 仍会构建共享库，不代表工具链接这些库。
最终仍须通过工具 NEEDED 验证。断言的 No 与 OFF 在 CMake 中等价。

### 实际配置门禁

脚本自 GBS 启动起 900 秒内必须发现并校验主构建目录的 CMakeCache；任何必需字段
缺失或不符均中止，两个并发池也必须与计划一致。

门禁用时：297.775 秒；原 Cache：`/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-baseline/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/CMakeCache.txt`；结果：PASS。

CMakeCache 原始关键行（完整副本 L/CMakeCache.txt）：

```text
CLANG_LINK_CLANG_DYLIB:BOOL=OFF
CMAKE_BUILD_TYPE:STRING=Release
CMAKE_CXX_FLAGS:STRING=  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument   -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables  -g -O3 -flto=thin -fomit-frame-pointer
LLVM_ENABLE_ASSERTIONS:BOOL=No
LLVM_ENABLE_LTO:STRING=Thin
LLVM_LINK_LLVM_DYLIB:BOOL=OFF
LLVM_PARALLEL_COMPILE_JOBS:STRING=4
LLVM_PARALLEL_LINK_JOBS:STRING=1
LLVM_TARGETS_TO_BUILD:STRING=X86;ARM;AArch64;BPF
LLVM_USE_LINKER:UNINITIALIZED=lld
```

## 6. 产物验证、真实 TU 和吞吐基线

### 构建树初检；RPM 验收未完成

由于 RPM 打包失败，未执行 rpm2cpio | cpio，也未创建 `temp/toolchain-baseline/`。
为核对已完成的链接结果，使用未修改的 tools/verify_toolchain.sh 对原 build/ 目录
进行了只读验证。这不代表 RPM 验收通过，不能将它当成最终基线交付。

验证根是 `B/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build`。
五个工具均为原生 x86_64 ELF，NEEDED 没有 libLLVM/libclang-cpp；版本查询使用本次构建根
的原生 ELF loader 和其 usr/lib64，不经 accel，不安装到宿主。
完整 ls/file/readelf/版本命令及原始输出在 L/build-tree-verification.log，结构化结果为
L/build-tree-verification.json。旧 accel 本次重新查询的原始结果在 L/accel-reference.log/json；
其共享库依赖使验证脚本返回 BLOCKER 是旧工具的预期特征，不是新链接失败。

| 工具 | 新 build/ ELF 字节数 | 新 LLVM NEEDED | 新版本 | 旧 accel 字节数 | 旧 LLVM NEEDED | 旧版本 |
| --- | ---: | --- | --- | ---: | --- | --- |
| clang | 1793477048 | 无 | 22.1.8 | 131592 | libclang-cpp.so.22.1, libLLVM.so.22.1 | 22.1.8 |
| clang++ | 1793477048 | 无 | 22.1.8 | 131592 | libclang-cpp.so.22.1, libLLVM.so.22.1 | 22.1.8 |
| ld.lld | 1079523024 | 无 | 22.1.8 | 6449904 | libLLVM.so.22.1 | 22.1.8 |
| llvm-ar | 121868264 | 无 | 22.1.8 | 81232 | libLLVM.so.22.1 | 22.1.8 |
| llvm-ranlib | 121868264 | 无 | 22.1.8 | 81232 | libLLVM.so.22.1 | 22.1.8 |

新文件带 debug_info、尚未剥离；旧 accel 是已安装产物。上述大小不能作为同处理阶段的
受控比较，也不能把差额全部归因于静态链接。最终 RPM 大小和 NEEDED 仍为 UNKNOWN。
本表只证明构建树中的五个工具确实没有直接依赖 LLVM/Clang C++ 共享库。

| 新构建树工具 | SHA256 |
| --- | --- |
| clang | `d25e99607c9ea23bf2e50da5075c21f0145f6da24a39a4228d2fd8026ead70cf` |
| clang++ | `d25e99607c9ea23bf2e50da5075c21f0145f6da24a39a4228d2fd8026ead70cf` |
| ld.lld | `9895d67f7020ac1ca573ac7d40b1cda93ace9aa504c17cfed358211bd1554f47` |
| llvm-ar | `3d8ed30f0cfb0ce3bf1dc096b7b3cb840291ff0e49f3aaa26975ad3a2a681d8f` |
| llvm-ranlib | `3d8ed30f0cfb0ce3bf1dc096b7b3cb840291ff0e49f3aaa26975ad3a2a681d8f` |

| 工具 | 完整 NEEDED |
| --- | --- |
| clang | librt.so.1, libdl.so.2, libm.so.6, libz.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so.6, ld-linux-x86-64.so.2 |
| clang++ | librt.so.1, libdl.so.2, libm.so.6, libz.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so.6, ld-linux-x86-64.so.2 |
| ld.lld | libxml2.so.16, librt.so.1, libdl.so.2, libm.so.6, libz.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so.6, ld-linux-x86-64.so.2 |
| llvm-ar | librt.so.1, libdl.so.2, libm.so.6, libz.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so.6, ld-linux-x86-64.so.2 |
| llvm-ranlib | librt.so.1, libdl.so.2, libm.so.6, libz.so.1, libstdc++.so.6, libgcc_s.so.1, libc.so.6, ld-linux-x86-64.so.2 |

clang --version 的关键原始输出：

```text
clang version 22.1.8
Target: x86_64-tizen-linux-gnu
Thread model: posix
```

```text
LLD 22.1.8 (compatible with GNU linkers)
LLVM (http://llvm.org/):
  LLVM version 22.1.8
  Optimized build.
```

补充限制：新 lld 在宿主直接运行时缺少 libxml2.so.16（L/built-lld-preliminary.log）；
用本次构建根的 loader/library-path 查询版本成功。对应依赖是固定快照缓存中的
`B/local/cache/6472de3503e3aaf43e4695c51bdf18ee/libxml2-2.15.1-1.7.x86_64.rpm`。
后续提取最终工具链时要解决该运行时依赖，不能通过安装到宿主或修改工具二进制掩盖它。
本轮没有执行该提取步骤。

### 真实 TU：已选候选，尚未生成 .ii

以下 10 项来自本次真实 build.ninja 和 .ninja_log：每个要求的子目录选两项，
在已完成、单次 1–30 秒的 .cpp.o 中选择最接近 6 秒的项。这个耗时是本次 x86_64/ThinLTO
构建日志用于选样的任务 wall，**不是后续 ARM 基准的耗时**。不把 MC 的 2–3 秒改写成 5 秒。

| 子系统 | 源文件（相对导出的 llvm-22.1.8/） | 原任务 wall 秒 | .ii 状态 |
| --- | --- | ---: | --- |
| sema | `clang/lib/Sema/SemaStmt.cpp` | 6.033 | NOT_COLLECTED |
| sema | `clang/lib/Sema/SemaExprCXX.cpp` | 6.098 | NOT_COLLECTED |
| codegen | `llvm/lib/CodeGen/SelectionDAG/SelectionDAG.cpp` | 6.010 | NOT_COLLECTED |
| codegen | `llvm/lib/CodeGen/MachinePipeliner.cpp` | 6.040 | NOT_COLLECTED |
| transforms | `llvm/lib/Transforms/IPO/Attributor.cpp` | 5.930 | NOT_COLLECTED |
| transforms | `llvm/lib/Transforms/IPO/WholeProgramDevirt.cpp` | 5.888 | NOT_COLLECTED |
| arm | `llvm/lib/Target/ARM/ARMISelLowering.cpp` | 6.935 | NOT_COLLECTED |
| arm | `llvm/lib/Target/ARM/ARMTargetTransformInfo.cpp` | 4.747 | NOT_COLLECTED |
| mc | `llvm/lib/MC/MCParser/MasmParser.cpp` | 2.887 | NOT_COLLECTED |
| mc | `llvm/lib/MC/MCParser/AsmParser.cpp` | 2.395 | NOT_COLLECTED |

实际 Ninja 查询使用本次根内原生 ninja 的 `-t compdb-targets`，不触发构建。
完整查询 argv 在 L/tu-query-command.json，完整输出在 L/tu-compdb.json；每个候选的
完整命令、路径、目标文件、原 wall 保存在 L/tu-candidates.json；选样脚本为
L/select-tu-candidates.py。没有运行预处理、没有写入 .ii 或 sidecar。

构建期间已发现一个后续输入兼容性问题：原始命令包含 -fPIC、-fno-semantic-interposition、
-fvisibility-inlines-hidden、-fno-common、-gdwarf-4、-frecord-gcc-switches，当前基准台
白名单不接受这些选项（tools/bench_toolchain.py:150–157）。real_tu/README.md 要求保留
语义选项、审查扩充白名单，不能静默删除。仅增加六个精确匹配项的两行补丁存放在
L/proposed-real-tu-flags.diff；已提请确认，**尚未获准、未应用**。本轮 tools/ 实现未改动。
RPM 构建失败是当前首要阻塞；该白名单问题不能被当成已有 TU 或校准结果。

### 重新校准与正式数据：NOT RUN

| 要求 | 本轮结果 | 原因 / 下一步所需条件 |
| --- | --- | --- |
| 新 clang 22 两轮完整噪声校准，门槛 3% | UNKNOWN / NOT RUN | 先完成受限 RPM 打包、解包验证和真实 TU 输入集 |
| A/B/C + 真实 TU + lld + ar 基线表 | UNKNOWN / NOT RUN | 必须先通过新工具链完整校准 |
| `temp/bench_results/baseline-*/` JSON | 未生成 | 不用构建树临时代替最终 RPM 工具链 |
| bundled clang 18 独立参考轮 | NOT RUN | 在新基线具备条件后单独运行 |

不能将 docs/12 的历史 0.220% 噪声值归给这次 clang 22，也不能用未测量的数据填表。
bundled clang 18 后续使用自己的资源目录，报告必须标注：
**资源目录不同，不是受控对照，仅供量级参考。**

当前需要解决的是 RPM 的 -j40 并发及重新审视链接内存预算；本轮仅允许 URL 和 spec
三处既有并发数字变更，未获准增加第四处 RPM 宏、改变调试/优化配置或扩大内存上限，
因此没有自行绕过失败重跑。构建根原样保留，恢复方式也应先确认，不能删除重来或承诺
现有包装脚本能原地续跑（它当前要求不存在的新根）。

## 7. 复现与证据索引

```sh
# 当前固定配置下只做预检；新的 --log-dir 必须不存在。
tools/build_llvm_x86_64.sh --log-dir temp/下一次预检目录 --buildroot temp/尚不存在的检查根
# 当前 B 已使用，脚本会拒绝覆盖；不要对现有构建根再次 --run。
tools/build_llvm_x86_64.sh --help
tools/verify_toolchain.sh --help
```

| 证据路径 | 内容 |
| --- | --- |
| Q/index-requests.log、Q/*-index.html、Q/*-reference.html | 原始目录索引、HTTP 状态 |
| Q/resolution.log、Q/resolve.py、Q/resolved.json | XML id 解析、双向 repomd 比较、归档摘要 |
| A/两个快照目录/ | repomd、primary、build.conf、压缩原件、manifest |
| Q/config-checksums.json、Q/config.diff、Q/gbs_llvm.conf.before/after | 完整配置前后证据 |
| Q/spec-build-requires.json、Q/check_dependencies.py、Q/dependencies.log/json | GBS 后端解析和包/provides 匹配 |
| P/commands.log、resource-plan.json、repositories.json、x86_64.rpmmacros | 不带 --run 的真实完整预检 |
| L/launch.json、commands.log、build.log | 真实启动 argv、命令原始输出、逐行时间戳构建日志 |
| L/resource-plan.json、spec-concurrency.diff | 启动前资源重算、仅三处数字的 spec diff |
| L/runtime-scope-check.log、priority-check.log、samples.jsonl | 真实 scope 属性、nice/ionice、后台采样 |
| L/cache-gate.json、CMakeCache.txt | 门禁结果和实际 Cache 原件 |
| L/outcome.json、time-v.txt | 退出码、线程回收、外层时间/RSS |
| L/scope-final.log、scope-journal.log、kernel-oom.log | 18 GiB cgroup OOM 的终态和内核证据 |
| L/cleanup-verification.json、packaging-resource-proof.log、debuginfo-processes.json | 回收检查、-j40 来源、真实进程 argv 和优先级 |
| L/linker-memory-observations.jsonl、linker-priority-check.log | 链接进程 RSS 高水位及调度优先级 |
| L/rpm-output-inventory.json、final-workspace-checks.log | 无输出 RPM，源码/配置最终状态 |
| L/build-tree-verification.log/json、accel-reference.log/json | 构建树五工具与旧 accel 的只读对照 |
| L/tu-candidates.json、tu-compdb.json、tu-query-command.json | 十个候选的来源和完整原命令；非已采集 .ii |
| L/proposed-real-tu-flags.diff | 未应用的最小白名单补丁 |
| Q/resolution-attempt1.log | 最初解析匹配到 Unified 的 id/base_id 后拒绝，随后改为根 id 精确解析 |

工具脚本与保护逻辑测试沿用提交 179196d，本轮没有调整限流或放宽任何门禁。
所有大文件及原始输出留在 temp，不纳入提交。

## 8. 提交前自检

1. **内存机制、峰值、回收**：systemd 用户 scope，MemoryMax=18 GiB、MemorySwapMax=0。
   连续 cgroup 峰值 18 GiB；30 秒采样 RSS 求和峰值 17.162125 GiB。RPM debuginfo -j40
   触发 cgroup OOM，不能宣称构建资源配置已全面合格。采样器和日志线程均回收，
   最终无 scope 残留进程。原始 time -v 的 102148 KiB 不能当成构建峰值，详见第 4 节。
2. **`_toolchain` 是否定义**：是，clang。固定 Unified build.conf 的 U:161、宏查询 `1|clang`、
   实际根 .rpmmacros:63 和 CMakeCache 均有证据。没有增加 `_toolchain` 的 --define。
3. **CMakeCache 是否全通过**：是，297.775 秒通过，早于 900 秒门槛。Release、Thin、
   两个 LINK_DYLIB=OFF、lld、assertions=No/OFF、CXX_FLAGS 含 -O3 不含 -Os、X86/ARM
   均确认；原始关键行见第 5 节。配置通过不等于 RPM 构建成功。
4. **产物 NEEDED 是否还有 LLVM 共享库**：构建树中的五个工具均无，见第 6 节完整表和原始
   readelf 输出；最终 RPM 工具链为 UNKNOWN，因为 RPM 打包失败，没有解包产物。
5. **重新校准噪声底**：UNKNOWN / NOT RUN。RPM、真实 TU 和校准前置条件未完成，未沿用
   clang 18 的旧值，没有生成或声称存在正式基线 JSON。
6. **是否修改 spec 并发数以外内容**：否，源码工作树仍只有三处并发数 diff；配置只有获准 URL
   变更，前后 SHA256 见第 2 节。工具实现未修改，提议的白名单补丁仍在 temp/ 未应用。
7. **是否构建 Chromium 或推送 Gerrit**：否。仅运行本次 LLVM GBS 构建和只读查询，推送目标
   是 GitHub 的 lhmax2010/llvm-optimize。
8. **是否列全部 raw 链接**：门禁后的中间回复已列报告、配置及四个相关工具文件；最终回复同样
   列出。本轮未生成新的真实 TU/sidecar，也不把 temp/ 原始证据误列为 GitHub 文件。
