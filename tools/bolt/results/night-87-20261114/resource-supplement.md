# 87号资源草案补充：适用限制与定向诊断（未执行）

86 step5.py本次只改argv起点5→4，其他逻辑/文字保持原样；生成的resource-proposal.md仍含86号时代的“未核对开关”等说明，以本补充的源码核对为准。原输出结束行保留86步骤5字样，不冒充86当时已经完成。

## D report-stale
原脚本草案现在成功生成，input/tool/loader/profile均存在且已计算SHA。D llvm-bolt当前SHA与74 rewrite记录完全相同。完整命令见report-stale-plan.json和resource-proposal.md；未创建其输出根、未执行任何BOLT。本次只申请，不是授权执行。
资源建议：单进程约10GB来自83；cgroup申请16GiB含文件缓存、swap0，CPU400%、nice19、idle，仅串行1个。16GiB不是实测峰值。时长UNKNOWN，60分钟是建议硬停止线；磁盘暂申请5GiB，/home<30GiB、目录新增>5GiB、OOM或超时均停止、不重试。停止信号处理方式要随新执行任务授权。

## 2804条逐条明细
源码RewriteInstance.cpp L2911–2918在analyzeRelocation返回false时计数；L2479–2480唯一false路径为Relocation::isSupported失败。仅经过L2829–2903筛选的静态重定位会到达这里，2804不等于全部ELF重定位，也不是所有重定位值都被错误修改。
逐条输出L2913–2916有offset和type-name；L2830–2845有重定位节/目标节上下文。DEBUG_TYPE在L69为bolt，因此启用LLVM_DEBUG的工具可用-debug-only=bolt。逐条失败发生在SymbolName赋值前，日志本身不保证符号名；后处理需按原ELF的offset/type对应符号和节。
**74的T/D工具编译参数均有-DNDEBUG**（*-exact-bolt-flags.txt）；Debug.h的NDEBUG分支把LLVM_DEBUG去掉。-v=1仅控制其他输出，不能恢复该日志。不能承诺用现有工具增加开关即可得到明细，也不应提交注定无明细的运行申请。

条件命令（只用于说明，当前不可执行）：
    
    /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/lib64/ld-linux-x86-64.so.2 --library-path /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64:/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/lib64:/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64 /home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-bolt /home/linhao/Toolchain/development/llvm-optimize/temp/local-full-r6-20261111-materials/basedev/reference-relocs-clang-22 -o /home/linhao/Toolchain/development/llvm-optimize/temp/report-stale-proposal-20261116/clang.bolt -data=/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261111-r6/basedev/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt/profile.fdata -reorder-blocks=ext-tsp -reorder-functions=cdsort -split-functions -split-all-cold -split-eh -dyno-stats --thread-count=1 -stale-threshold=5 -use-old-text -report-stale -debug-only=bolt

该argv中的现有工具路径只有在另外获批、换为同源非NDEBUG诊断工具并记录新SHA后才有意义；不能覆盖74工具。本任务不构建、也不提出把新工具悄悄当作74工具。PM可选择另批诊断工具准备，或另批只读ELF枚举器复刻上述筛选并验证2804计数；后者不等同于BOLT实跑明细。

合并风险：若具备可输出LLVM_DEBUG的诊断工具，-report-stale与-debug-only=bolt可以放在一次正式参数运行中，保留-stale-threshold=5；但工具身份改变，须先确认2804和profile计数复现。大量debug日志可能超过5GiB或60分钟而不及完成report-stale；单进程内存及缓存开销UNKNOWN。建议仍申请16GiB但不保证足够，OOM就UNKNOWN，不自动提额重试。

## 采集改动草案
见collection-draft.diff.txt（语义伪diff，不能直接应用）。实际读过两侧launcher.py的stage/materialize/worker和resource_report.py的report。只改本地入口，不能修改发布helper。精确子步骤起止如无法无侵入采集，继续UNKNOWN，不将采样观察时间包装成实际执行时间。
CPU/内存/磁盘报备需另计比较解包副本、采集开销。本轮不实施采集、不清理。
