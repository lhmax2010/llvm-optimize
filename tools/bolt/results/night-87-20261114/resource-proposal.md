# 资源报备草案（未批准、未执行）

## D report-stale
目的只取得74号D的失配名单；保持旧profile、正式优化参数与5%门槛。不是新构建、不把输出作为新发货候选。
输入/工具/loader/profile当前身份见report-stale-plan.json；平台工具由自身根loader读取。源提交fea0fe46，输入D SHA bf15cf062439714651809cd3b5ca82619407081adca64ceb65699e6ccae50501。运行前应复核全部SHA和输出目录不存在；任一输入不存在则先PM指定保全副本，不从网络获取。
命令（只写不执行）：

    /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/lib64/ld-linux-x86-64.so.2 --library-path /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64:/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/lib64:/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64 /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-bolt /home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22 -o /home/linhao/Toolchain/development/llvm-optimize/temp/report-stale-proposal-20261116/clang.bolt -data=/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt/profile.fdata -reorder-blocks=ext-tsp -reorder-functions=cdsort -split-functions -split-all-cold -split-eh -dyno-stats --thread-count=1 -stale-threshold=5 -use-old-text -report-stale

计划输出目录为W/temp/report-stale-proposal-20261116；只在获批后创建。stdout/stderr、command.json、退出码、资源记录和一次输出ELF全部保留。
资源申请草案：单进程约10GB（83依据）；建议MemoryMax=16GiB包含文件缓存、swap0、CPUQuota=400%、nice19、idle IO、单任务。16GiB是待批准余量，不是实测需求。本任务仍4GiB，未运行llvm-bolt。
时长UNKNOWN；排期预留60分钟，拟硬停止线60分钟，不把它当实测预测。磁盘新占用暂申请5GiB（输入读取不复制、输出/日志/采样），精确上限UNKNOWN；stdout/stderr各1GiB监测告警，/home低于30GiB或目录新增超过5GiB即按获批的正常取消流程停。OOM不重试、不抬限制。信号/正常停止方式需要资源报备同时授权，本任务没有执行。
还应单列诊断-v或print开关的输出膨胀风险；本次未完成对应源码开关核对，不能把建议-v=1当作保证提供relocation明细的已验证命令。

## 下一次计划内完整构建采集
不修改当前入口。先审阅以下伪diff，再独立实现/测试，按新输出目录部署；产品源码/spec/helper不变。
1. launcher的service_stage及controller：记录monotonic_ns与wall time、项目/step/argv/service/PID、rc/signal。两类时钟分开，禁止采样器观察时间替代命令实际起止。
2. 已有driver监视器：每2秒保存memory.current/peak/events及memory.stat的anon/file；服务结束前保全最终计数，cgroup删除后不可恢复；文件缓存与进程RSS不相加。
3. 进程记账：捕获子进程创建/退出、cmdline和wait4 rusage；所有后代不能只靠controller的RUSAGE_CHILDREN。对gbs/chroot边界需要授权的进程事件采集或可审计wrapper，否则最大单进程继续UNKNOWN；/proc VmHWM轮询不能保证捕获短进程。
4. cmake/ninja大链接/BOLT各门禁/归档/打包：优先已有原始日志和.ninja_log的真实起止；但BOLT工具内部子步骤若无起止记录，仅外部采样无法精确拆分。要精确计时需另批透明exec事件采集方案；不得暗改产品helper，不凭日志相邻行推算。
5. 文件系统已用量/可用量10秒；分层du每5分钟（BUILD、BUILDROOT、SOURCES、RPM、BOLT工件、profile），每次50秒上限，记录timeout/rc/权限盲区；一次仅一个du，父子不相加。也需另批终止超时子进程。
6. resource_report按真实阶段窗口对齐采样；缺命令起止、anon/file、rusage或层级du就UNKNOWN。memory.events max>0则峰值写≥限额，时长标回收影响；不把成功du最大值当保证峰值。
7. 新测试：时钟回拨、短进程、子孙进程、cgroup消失、du超时/权限失败、prep交接、截断峰值，所有采集开销记录，不能改发布产物参数。

预计需要修改文件：toolchain/launcher.py、basedev/launcher.py的生成监控片段，两个resource_report.py；新增本地collector及tests；run-night只增加采集开关传递；README/provenance/SHA256SUMS更新。完整构建资源设置不自动改变。本草案不修复本次步骤2授权不足的问题。

## 磁盘
按85已有du列表引用原采样时间，本次只重新df、不重新du。历史最低预算2×70,485,561,344B+20GiB；目标加20%根余量。差额见resource-budget.json。新增采集、比较解包、PGO根和report-stale分别预算，不能当已有余量覆盖。
清理候选见cleanup-candidates.json，体积是85的du，不保证可实际释放量（可能有链接/共享块及同期变化），只提供PM审核清单。不可把已发布摘要视为大型输入已上传。优先审计可重解的比较副本；PGO原始profile、74 BOLT输入、恢复的TU输入、当前QB基线、源码保护备份和有效构建根不列为低风险删除项。
