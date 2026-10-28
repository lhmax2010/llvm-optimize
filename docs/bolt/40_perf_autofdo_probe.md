# 40：perf与AutoFDO本机能力探测（2026-10-28）

硬件和内核暴露LBR能力，但当前普通用户权限下没有采到分支记录。默认perf入口缺当前内核工具，已安装的perf 7.0.14能列事件，但带/不带-b的cycles:u采样都因perf_event_paranoid=4被拒绝。llvm-profgen存在且能运行，但没有有效perf.data，故本轮未能验证AutoFDO转换。

**状态：部分完成。** 硬件/权限/工具盘点和两种采样尝试完成；采样成功路径、分支栈前20行与profgen转换未完成，原因是工具匹配和权限限制。没有安装软件、提权、改sysctl或重新构建。

## 1. 硬件、内核与访问限制

- GenuineIntel，Intel Core Ultra 7 265，20逻辑CPU；CPUID family6/model198/stepping2。微架构相关的内核PMU实现名为`lunarlake_hybrid`（cpu_core和cpu_atom相同）；这是内核PMU标识，不把它直接等同于产品营销代号。
- 内核`6.17.0-1033-oem`；lscpu原文flags含`arch_lbr`、`bts`、`intel_pt`。
- cpu_core与cpu_atom的caps/branches均32，branch_counter_nr=4、branch_counter_width=2、max_precise=3。AMD BRS/LbrExtV2不适用于本机Intel CPU。
- perf_event_paranoid=4，kptr_restrict=1；dmesg读取返回`Operation not permitted`，未尝试sudo。sysfs可读证据不依赖dmesg。

完整原文：[lscpu.stdout](../../tools/bolt/results/perf-probe-20261028/lscpu.stdout)、[uname.stdout](../../tools/bolt/results/perf-probe-20261028/uname.stdout)、[hardware.json](../../tools/bolt/results/perf-probe-20261028/hardware.json)、dmesg.stderr。

## 2. perf工具及一次单文件采样尝试

`/usr/bin/perf`是包装入口，返回当前内核缺工具警告：

```text
WARNING: perf not found for kernel 6.17.0-1033

  You may need to install the following packages for this specific kernel:
    linux-tools-6.17.0-1033-oem
    linux-cloud-tools-6.17.0-1033-oem

  You may also want to install one of the following packages to keep up to date:
    linux-tools-oem
    linux-cloud-tools-oem
```

只读发现已有`/usr/lib/linux-hwe-7.0-tools-7.0.0-38/perf`，版本7.0.14；没有安装替代包。该用户态工具与运行内核版本不同，不能把本次列事件成功视为完整兼容认证。perf list成功，branch/BR_INST_RETIRED/BR_MISP_RETIRED等事件摘录见[perf-list-branch-excerpts.txt](../../tools/bolt/results/perf-probe-20261028/perf-list-branch-excerpts.txt)，完整输出为perf-list.stdout。

用34号C++ -O2的00-SemaStmt、x86_64目标，输入SHA核对，通过宿主loader、本轮运行库/resource-dir、固定CPU2、setarch -R构造单次编译命令。先尝试`perf record -e cycles:u -b`；失败后只重试用户指定的`perf record -e cycles:u`，两者退出码均255，发生在打开事件阶段，未产生single.o，不宣称编译被实际采样。完整argv和输入在compile-input.json、record-branches.json、record-cycles.json。

带-b原文：

```text
Missing support for build id in kernel mmap events.
Disable this warning with --no-buildid-mmap
Error:
Failure to open event 'cpu_atom/cycles/u' on PMU 'cpu_atom' which will be removed.
Access to performance monitoring and observability operations is limited.
Consider adjusting /proc/sys/kernel/perf_event_paranoid setting to open
access to performance monitoring and observability operations for processes
without CAP_PERFMON, CAP_SYS_PTRACE or CAP_SYS_ADMIN Linux capability.
More information can be found at 'Perf events and tool security' document:
https://www.kernel.org/doc/html/latest/admin-guide/perf-security.html
perf_event_paranoid setting is 4:
  -1: Allow use of (almost) all events by all users
      Ignore mlock limit after perf_event_mlock_kb without CAP_IPC_LOCK
>= 0: Disallow raw and ftrace function tracepoint access
>= 1: Disallow CPU event access
>= 2: Disallow kernel profiling
To make the adjusted perf_event_paranoid setting permanent preserve it
in /etc/sysctl.conf (e.g. kernel.perf_event_paranoid = <setting>)
Error:
Failure to open event 'cpu_core/cycles/u' on PMU 'cpu_core' which will be removed.
Access to performance monitoring and observability operations is limited.
Consider adjusting /proc/sys/kernel/perf_event_paranoid setting to open
access to performance monitoring and observability operations for processes
without CAP_PERFMON, CAP_SYS_PTRACE or CAP_SYS_ADMIN Linux capability.
More information can be found at 'Perf events and tool security' document:
https://www.kernel.org/doc/html/latest/admin-guide/perf-security.html
perf_event_paranoid setting is 4:
  -1: Allow use of (almost) all events by all users
      Ignore mlock limit after perf_event_mlock_kb without CAP_IPC_LOCK
>= 0: Disallow raw and ftrace function tracepoint access
>= 1: Disallow CPU event access
>= 2: Disallow kernel profiling
To make the adjusted perf_event_paranoid setting permanent preserve it
in /etc/sysctl.conf (e.g. kernel.perf_event_paranoid = <setting>)
Error:
Failure to open event 'dummy:u' on PMU 'software' which will be removed.
Access to performance monitoring and observability operations is limited.
Consider adjusting /proc/sys/kernel/perf_event_paranoid setting to open
access to performance monitoring and observability operations for processes
without CAP_PERFMON, CAP_SYS_PTRACE or CAP_SYS_ADMIN Linux capability.
More information can be found at 'Perf events and tool security' document:
https://www.kernel.org/doc/html/latest/admin-guide/perf-security.html
perf_event_paranoid setting is 4:
  -1: Allow use of (almost) all events by all users
      Ignore mlock limit after perf_event_mlock_kb without CAP_IPC_LOCK
>= 0: Disallow raw and ftrace function tracepoint access
>= 1: Disallow CPU event access
>= 2: Disallow kernel profiling
To make the adjusted perf_event_paranoid setting permanent preserve it
in /etc/sysctl.conf (e.g. kernel.perf_event_paranoid = <setting>)
Error:
Failure to open any events for recording.
```

不带-b也打印相同权限拒绝，见[record-cycles.stderr](../../tools/bolt/results/perf-probe-20261028/record-cycles.stderr)。错误中的“Missing support for build id in kernel mmap events”也原样保留，可能涉及用户态/内核版本组合，未改参数消除警告。明确阻断采样的证据是访问权限拒绝，不推断为硬件不支持LBR。

成功样本数为0；无有效分支栈，因此perf script前20行**未测**，不能用空输出证明“硬件没有分支记录”。临时数据文件（若perf预创建）不能当作有效采样文件。

## 3. LLVM工具

所有工具来自39号本轮build/bin，使用相同loader/lib路径，仅调用--version/--help，没有构建任何目标。

| 工具 | 存在 | --version返回 | 说明 |
|---|---|---:|---|
| llvm-profgen | True | 0 | 普通文件；路径见llvm-tools.json |
| perf2bolt | True | 0 | llvm-bolt；路径见llvm-tools.json |
| llvm-bolt | True | 0 | 普通文件；路径见llvm-tools.json |
| llvm-profdata | True | 0 | 普通文件；路径见llvm-tools.json |

四个工具版本均为LLVM 22.1.8，BOLT revision打印<unknown>；版本原文保留在各工具-version.stdout。llvm-profgen帮助列出--perfdata、--binary、--output；llvm-bolt/perf2bolt帮助保留perf输入相关选项。这只证明入口存在，不证明转换可用。

因为没有带分支栈的有效perf.data，`llvm-profgen --perfdata=... --binary=ordinary-clang-22 --output=...` **NOT RUN**，无profile输出大小。见[conversion.json](../../tools/bolt/results/perf-probe-20261028/conversion.json)。不从工具存在推断AutoFDO链路通过。

## 4. 探测期间负载

起止附近load average为`9.64 8.93 5.63 12/2138 197937`；三秒/proc CPU增量样本中，PID2407 epp-client-daem约0.536核, PID15572 code-insiders约0.162核。按0.5核短样本阈值epp-client-daem命中；未观察到编译/链接进程命中该阈值，不代表整个机器始终空闲。ps的累计PCpu与三秒增量分开保存；不能据短采样给某个Codex会话作完整负载归因。探测本身只持续约4.4秒，采样命令在开始编译前被拒绝，没有性能结论。

证据：load.json、processes.stdout、processes-after.stdout。systemd service CPUQuota100%、MemoryMax2GiB、swap0、nice19、idle I/O；未改系统设置。

## 5. 后续设计前提（仅建议）

后续若要验证LBR→AutoFDO，需要用户/管理员另外提供允许perf_event_open的环境，并使用与内核适配的perf工具；本轮未执行任何授权或系统调整。拿到真实分支栈后再验证profgen对ordinary二进制的地址映射和输出，不能用权限失败数据生成profile。perf版BOLT同样需要实际perf数据再验证，现有perf2bolt版本/帮助不是profile质量证据。
