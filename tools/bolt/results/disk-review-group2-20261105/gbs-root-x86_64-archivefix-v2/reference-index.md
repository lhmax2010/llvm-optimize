# 引用逐条索引：gbs-root-x86_64-archivefix-v2

本页逐条列工具脚本及55–63号文档引用。其他用途来源的完整命中在main-docs/bolt-docs-references-v3.txt.gz。路径命中不等于当前执行依赖；历史render/报告脚本仍按原文列出。

## main-scripts

- `/home/linhao/Toolchain/development/llvm-optimize/tools/test_certified_x86_release_build.py:48`
  ```text
                           'temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock'):
  ```
- `/home/linhao/Toolchain/development/llvm-optimize/tools/run_certified_x86_release_build.py:55`
  ```text
                W/'temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock'):
  ```
- `/home/linhao/Toolchain/development/llvm-optimize/tools/test_archive_fix_trial.py:89`
  ```text
              root=Path(tmp)/'temp/gbs-root-x86_64-archivefix-v2';root.mkdir(parents=True)
  ```
- `/home/linhao/Toolchain/development/llvm-optimize/tools/build_llvm_x86_64.py:166`
  ```text
      if root.resolve() != (WORKSPACE/'temp/gbs-root-x86_64-archivefix-v2').resolve():
  ```

## bolt-scripts

- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/test_archive_fix_trial.py:89`
  ```text
              root=Path(tmp)/'temp/gbs-root-x86_64-archivefix-v2';root.mkdir(parents=True)
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/build_llvm_x86_64.py:166`
  ```text
      if root.resolve() != (WORKSPACE/'temp/gbs-root-x86_64-archivefix-v2').resolve():
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/root-inventory-20261022/make_report.py:122`
  ```text
  T/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/root-inventory-20261022/make_report.py:137`
  ```text
  | docs35/38旧Rnew、docs25 overlay的lower | `T/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0` | 原始下层只读，含旧普通工具及docs38包；main hybrid52也复用工具；本轮没有直接执行树内工具 |
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/source-order-20261016/attempt-version-display/root_parse.py:3`
  ```text
  E=Path(__file__).resolve().parent;W=E.parents[1];L=W/'temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0';M=E/'merged';G=1024**3
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/source-order-20261016/attempt-version-display/root_parse.py:61`
  ```text
   project=W/'temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock'
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/install-rehearsal-20261015/finalize-first.py:30`
  ```text
  save('final-recovery.json',{'own_mounts':mounts,'cgroup_exists':cg.exists(),'project_lock_exists':(E.parents[1]/'temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock').exists(),'abuild_survivors':read('supervisor-exit.json')['remaining_abuild_pids'],'lower_unchanged':True,'source_unchanged':True})
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/install-rehearsal-20261015/finalize-first.py:34`
  ```text
  s+='''## B：发现问题（本地演练时限中止，未完成）\n\n停止步骤：只带 emit-relocs 的 clang 重链。宿主监护按55分钟计算截止主动SIGKILL abuild进程，预留卸载/审计时间，原文：\n\n```text\nshared lock 3300-second deadline, leaving 300 seconds for cleanup/audit\n```\n\n没有观测到源代码产品门禁失败。rpmbuild退出码-9来自上述资源时限终止，不是匹配度、strip、安全属性或post失败；这些步骤尚未运行。本地结果不能据此断言QB会失败。本根初始缓存仅61文件/14,977,512B，与历史温缓存预演条件不同；不把耗时差异作为QB必败证据。\n\n## 执行范围与结果\n\n下层：W/temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0；这是docs38历史构建树，不称作67619ec8新构建物。仅将506dc25的spec/helper/profile/converter作为演练输入，不改源码。upper/work/merged均为本会话新目录、同一文件系统，所有写入在overlay；未在下层或坏配置的/var/tmp树运行cmake/ninja/-P。\n\n成功认证的一次sudo -A调用包办overlay、/proc、临时/dev及必要节点、chroot abuild、卸载。原RPM入口PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin，clang/clang++解析/bin/clang和/bin/clang++；宏_toolchain=clang，debug模式，_smp_mflags=-j4。完整argv、实际生成install/post脚本和原始日志均保存。\n\n| 项目 | 结果 | 事实 |\n| --- | --- | --- |\n| 普通CMake安装 | PASS | install-before.json为5,429路径；仅执行一次普通安装 |\n| preflight/certified | PASS | Python3.14.2，LLVM22.1.8，认证111 BOLT+2 TF；profile未压缩SHA d9b132f9… |\n| 路径与proc | PASS | BOLT_BUILDROOT_OK、BOLT_PROC_OK；没有MISSING |\n| 真实dry-run/tool-plan | PASS | 总113：102对象、7静态库、1可执行、1生成，另TF刷新2；ninja_diagnostics=[] |\n| 实际-j1构建/tool-verify | PASS | BOLT_NINJA_EXIT_0；planned=executed=113；工具此前不存在、本次产出true |\n| TF归档 | PASS | 前后及预构建归档均f15c565d30a981c22c71cbcf823030302cf51d19a381f4cc82e44626688be1ed |\n| clang emit-relocs重链 | INTERRUPTED | 计算截止时仍未结束，不能视作合格BOLT输入 |\n| strip-debug/BOLT匹配/标识/strip-all/安全/两次tiny | NOT RUN | N/M/S/U/Q、R、S/N与候选SHA均未知；没有BOLT_PIPELINE_PASS |\n| compare-root | NOT RUN | 无BOLT_COMPARE_ROOT_PASS |\n| 静态归档转换及候选install | NOT RUN | 未执行；保全的构建目录summary是历史docs38记录，与旧摘要相同，不能冒作新输出 |\n| 平台后处理及post尾检 | NOT RUN | find-debuginfo实际执行0次；无BOLT_POST_GATE_PASS；post路径/cmake计数未知 |\n| 最终ninja no-work | NOT RUN | 按停止规则未在中止后继续产品步骤；不伪造no-work原文 |\n| 卸载/进程/锁/下层审计 | PASS | 见下节；全部成功回收，未延长持锁上限 |\n\n'''
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/install-rehearsal-20261015/root_wrapper.py:3`
  ```text
  E=Path(__file__).resolve().parent;W=E.parents[1];L=W/'temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0';M=E/'merged';P=Path('home/abuild/rpmbuild/BUILD/llvm-22.1.8');G=1024**3
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/install-rehearsal-20261015/prepare.py:3`
  ```text
  E=Path(__file__).resolve().parent;W=E.parents[1];S=W/'temp/bolt-v4-20261013/v41/llvm-source';L=W/'temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0';P=L/'home/abuild/rpmbuild/BUILD/llvm-22.1.8';G=1024**3
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/source-order-20261016/root_parse.py:3`
  ```text
  E=Path(__file__).resolve().parent;W=E.parents[1];L=W/'temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0';M=E/'merged-certified';G=1024**3
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/source-order-20261016/root_parse.py:61`
  ```text
   project=W/'temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock'
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/root-inventory-20261022/annotate.py:12`
  ```text
  put('gbs-root-x86_64-archivefix-v2','f111162e + docs35/38 配方','Rnew；docs38 llvm-strip 根','main/docs/38_llvm_strip_x86_64.md:27; main/docs/52_hybrid_link_tizen_base.md:49','是，Rnew/B','D25 upper 的历史 lower；main hybrid52 工具环境；删后旧 overlay 无法重挂，hybrid 复验失去工具','保留','同时被 BOLT 演练与 main hybrid 引用','原始普通 clang、strip、资源目录；R/RPMS 是 docs38 包，非 docs35')
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/install-rehearsal-20261015/launch.py:4`
  ```text
  lock=W/'temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock';record=None;fd=None
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/install-rehearsal-20261015/finalize.py:30`
  ```text
  save('final-recovery.json',{'own_mounts':mounts,'cgroup_exists':cg.exists(),'project_lock_exists':(E.parents[1]/'temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock').exists(),'abuild_survivors':read('supervisor-exit.json')['remaining_abuild_pids'],'lower_unchanged':True,'source_unchanged':True})
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/install-rehearsal-20261015/finalize.py:34`
  ```text
  s+='''## B：发现问题（本地演练时限中止，未完成）\n\n停止步骤：只带 emit-relocs 的 clang 重链。宿主监护按55分钟计算截止主动SIGKILL abuild进程，预留卸载/审计时间，原文：\n\n```text\nshared lock 3300-second deadline, leaving 300 seconds for cleanup/audit\n```\n\n没有观测到源代码产品门禁失败。rpmbuild退出码-9来自上述资源时限终止，不是匹配度、strip、安全属性或post失败；这些步骤尚未运行。本地结果不能据此断言QB会失败。本根初始缓存仅61文件/14,977,512B，与历史温缓存预演条件不同；不把耗时差异作为QB必败证据。\n\n## 执行范围与结果\n\n下层：W/temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0；这是docs38历史构建树，不称作67619ec8新构建物。仅将506dc25的spec/helper/profile/converter作为演练输入，不改源码。upper/work/merged均为本会话新目录、同一文件系统，所有写入在overlay；未在下层或坏配置的/var/tmp树运行cmake/ninja/-P。\n\n成功认证的一次sudo -A调用包办overlay、/proc、临时/dev及必要节点、chroot abuild、卸载。原RPM入口PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin，clang/clang++解析/bin/clang和/bin/clang++；宏_toolchain=clang，debug模式，_smp_mflags=-j4。完整argv、实际生成install/post脚本和原始日志均保存。\n\n| 项目 | 结果 | 事实 |\n| --- | --- | --- |\n| 普通CMake安装 | PASS | install-before.json为5,429路径；仅执行一次普通安装 |\n| preflight/certified | PASS | Python3.14.2，LLVM22.1.8，认证111 BOLT+2 TF；profile未压缩SHA d9b132f9… |\n| 路径与proc | PASS | BOLT_BUILDROOT_OK、BOLT_PROC_OK；没有MISSING |\n| 真实dry-run/tool-plan | PASS | 总113：102对象、7静态库、1可执行、1生成，另TF刷新2；ninja_diagnostics=[] |\n| 实际-j1构建/tool-verify | PASS | BOLT_NINJA_EXIT_0；planned=executed=113；工具此前不存在、本次产出true |\n| TF归档 | PASS | 前后及预构建归档均f15c565d30a981c22c71cbcf823030302cf51d19a381f4cc82e44626688be1ed |\n| clang emit-relocs重链 | INTERRUPTED | 计算截止时仍未结束，不能视作合格BOLT输入 |\n| strip-debug/BOLT匹配/标识/strip-all/安全/两次tiny | NOT RUN | N/M/S/U/Q、R、S/N与候选SHA均未知；没有BOLT_PIPELINE_PASS |\n| compare-root | NOT RUN | 无BOLT_COMPARE_ROOT_PASS |\n| 静态归档转换及候选install | NOT RUN | 未执行；保全的构建目录summary是历史docs38记录，与旧摘要相同，不能冒作新输出 |\n| 平台后处理及post尾检 | NOT RUN | find-debuginfo实际执行0次；无BOLT_POST_GATE_PASS；post路径/cmake计数未知 |\n| 最终ninja no-work | NOT RUN | 按停止规则未在中止后继续产品步骤；不伪造no-work原文 |\n| 卸载/进程/锁/下层审计 | PASS | 见下节；全部成功回收，未延长持锁上限 |\n\n'''
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/source-order-20261016/attempt-prep-count/root_parse.py:3`
  ```text
  E=Path(__file__).resolve().parent;W=E.parents[1];L=W/'temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0';M=E/'merged-parse';G=1024**3
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/source-order-20261016/attempt-prep-count/root_parse.py:61`
  ```text
   project=W/'temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock'
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/narrow-disk-20261019/root_wrapper.py:4`
  ```text
  E=Path(__file__).resolve().parent;W=E.parents[1];L=W/'temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0';M=E/'merged-rpm';G=1024**3
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/narrow-disk-20261019/root_wrapper.py:70`
  ```text
   project=W/'temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock'
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/narrow-disk-20261019/close_results.py:15`
  ```text
  project=W/'temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock'
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/second-review-20261104/sandbox-direct-20261103/classify.py:22`
  ```text
  'gbs-root-x86_64-archivefix-v2':('建议保留','24、31、38','静态库修复历史根和受保护原始 RPM 组；不把后来的包冒充新基线。'),
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/source-order-20261016/attempt-rpmspec-without/root_parse.py:3`
  ```text
  E=Path(__file__).resolve().parent;W=E.parents[1];L=W/'temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0';M=E/'merged-final';G=1024**3
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/source-order-20261016/attempt-rpmspec-without/root_parse.py:61`
  ```text
   project=W/'temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock'
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/disk-diagnostics-20261019/root_wrapper.py:4`
  ```text
  E=Path(__file__).resolve().parent;W=E.parents[1];L=W/'temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0';M=E/'merged-rpm';G=1024**3
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/disk-diagnostics-20261019/root_wrapper.py:66`
  ```text
   project=W/'temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock'
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/temp-cleanup-20261026/report.py:77`
  ```text
  restore={str(T/'toolchain-archivefix-v2-final'):'docs35原22RPM：T/archive-fix-v2-final-20261009/rpms-docs35；原件保留',str(T/'toolchain-llvm-strip'):'docs38的22RPM仍在gbs-root-x86_64-archivefix-v2/.../rpmbuild/RPMS/x86_64；不把它们说成67619ec8新构建',str(T/'toolchain-release-x86-20261013'):'docs49交接树/var/tmp/llvm-optimize-x86-archivefix-20261013/.../rpmbuild/RPMS/x86_64；该树仅删缓存，RPM保留',str(T/'bolt-v4-20261016-source-order/upper-parse'):'docs26解析实验已结束；upper-parse不是原始输入，报告/脚本/导出留在父目录；原下层保留','/var/tmp/llvm-optimize-archivefix-v2-final-20261009/independent-install':'docs35独立安装载荷；原RPM及外部验收报告保留；重跑需重建DESTDIR'}
  ```

## main-config

无。

## bolt-config

无。

## recent-docs

无。
