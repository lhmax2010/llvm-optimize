# 引用逐条索引：bolt-v4-20261022-cache-release

本页逐条列工具脚本及55–63号文档引用。其他用途来源的完整命中在main-docs/bolt-docs-references-v3.txt.gz。路径命中不等于当前执行依赖；历史render/报告脚本仍按原文列出。

## main-scripts

无。

## bolt-scripts

- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/perf-c-o2-os-20261025/prepare.py:17`
  ```text
  for group,prefix in [('static','bolt-v4-20261022-cache-release/baseline-products'),('hybrid','bolt-on-hybrid-20261024/products')]:
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/second-review-20261104/sandbox-direct-20261103/classify.py:10`
  ```text
  'bolt-v4-20261022-cache-release':('建议保留','32、34、38','baseline/revised-products、preserved-before-delete 是已认证静态版本原件；根已清理不代表剩余 products 可删。'),
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/cache-release-20261022/baseline-cache-space-recovery.py:5`
  ```text
  assert D==Path('/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261022-cache-release')
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/cache-release-20261022/launch.py:3`
  ```text
  W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=W/'temp/bolt-v4-20261022-cache-release';E=D/'baseline-segment1';E.mkdir(exist_ok=False)
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/cache-release-20261022/launch-prepared.py:3`
  ```text
  W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=W/'temp/bolt-v4-20261022-cache-release';E=D/'baseline-segment2';E.mkdir(exist_ok=False)
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/cache-release-fix-20261023/parse.py:3`
  ```text
  D=Path(__file__).resolve().parent;R=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261022-cache-release/baseline-root/local/BUILD-ROOTS/scratch.x86_64.0');E=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/cache-release-fix-20261023/five-parse');E.mkdir(exist_ok=True)
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/bolt-on-hybrid-20261024/parse.py:3`
  ```text
  D=Path(__file__).resolve().parent;R=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261022-cache-release/baseline-root/local/BUILD-ROOTS/scratch.x86_64.0');E=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/bolt-on-hybrid-20261024/five-parse');E.mkdir(exist_ok=True)
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/temp-cleanup-20261026/report.py:17`
  ```text
   'bolt-v4-20261022-cache-release':('BOLT/cache-release','9e5675f、d20e873；双轮完整构建与比较已完成','bolt/docs/bolt/32_cache_release.md:232; bolt/docs/bolt/32_cache_release.md:244'),
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/temp-cleanup-20261026/report.py:40`
  ```text
   if name in ['bolt-v4-20261022-cache-release','hybrid-local-20261023','bolt-on-hybrid-20261024']:
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/temp-cleanup-20261026/report.py:88`
  ```text
  lines+=['', '深入build/、lto.cache、RPMS、SRPMS和BUILDROOT的独立du全部在 subunits.json。它们是解释父目录组成的重叠数据，不能累加成“清理收益”。','', '## 5. 必须保留、需要先保全的小资产','', '- `T/runpath-fix-20261026/`：当前不存在；一旦创建整目录保留，不推断其任务已结束。', '- `T/bolt-on-hybrid-20261024/products/`（3.886GiB）、`T/bolt-v4-20261022-cache-release/{baseline-products,revised-products}/`（各11.248GiB）：整体保留，RUNPATH/RPM比较仍要用。', '- `T/bolt-v4-20261021-disk-footprint/` 的gbs_llvm_qb1202084.conf和build.conf整体保留。固定快照配置及build.conf实际SHA见catalog；build.conf预期e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945。', '- 90份TU：`T/hybrid-local-20261023/tu-inputs/`，以及旧validation/bench_results资产；34号C输入`T/perf-c-o2-os-20261025/inputs/`和C++ .ii原件全部保留。perf父目录本次整体保留，包括测量脚本所用槽位/对象；不因报告已发布自动删除原始数据。', '- profile/Source1200原件、`W/tools/collect_bolt_profile.py`、`extend_bolt_profile_aarch64.py`、final_bolt_calibration_plan.json及训练/留出清单保留；bench_results整体保留。所有*.fdata及clang-bolt-v2.fdata.xz的本轮SHA见catalog。源码仓库中的同名Source也不会删除。', '- **新增保全前提**：34号通过hybrid+BOLT根的Tizen loader/运行库和build/lib64/clang/22运行。删除该gbs-root前，先保全 runtime-preservation.json 的8个运行库路径/符号链接布局及整个resource-dir，并在将来重测时显式重定向路径；本轮未复制、未改脚本。旧R1、ARM32/64 sysroot仍保留。', '', '### 5.1 已有同SHA副本与需要补存的清单','', '完整逐文件表：[asset-catalog.tsv](../../tools/bolt/results/temp-cleanup-20261026/asset-catalog.tsv)（路径、大小、SHA、同SHA其它路径）；本次删除范围对应的动作与保全预算：[preserve-before-delete.json](../../tools/bolt/results/temp-cleanup-20261026/preserve-before-delete.json)。副本判断不只比文件名；同inode复用SHA时也核对size/mtime，来源记录在asset-hashes-inode-aliases.json。仅列少量关键二进制如下：','', '| 保留文件 | 字节数 | SHA256 | 副本/结论 |','|---|---:|---|---|']
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/temp-cleanup-20261026/hash-assets.py:5`
  ```text
  new=['bolt-v4-20261022-cache-release','hybrid-local-20261023','bolt-on-hybrid-20261024']
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/temp-cleanup-20261026/hash-assets.py:19`
  ```text
   for p in (W/'temp/bolt-v4-20261022-cache-release'/parent/'binaries').glob('*'):
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/temp-cleanup-20261026/plan.py:9`
  ```text
  conservative=[str(T/'bolt-v4-20261022-cache-release/baseline-root'),str(T/'bolt-v4-20261022-cache-release/revised-root'),str(T/'hybrid-local-20261023/gbs-root'),str(T/'bolt-on-hybrid-20261024/gbs-root'),'/var/tmp/llvm-optimize-x86-archivefix-20261013/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache']
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/temp-cleanup-20261026/revised-root-followup/cleanup.py:7`
  ```text
  ROOT=W/'temp/bolt-v4-20261022-cache-release/revised-root'
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/temp-cleanup-20261026/revised-root-followup/attempt-2/cleanup.py:7`
  ```text
  ROOT=W/'temp/bolt-v4-20261022-cache-release/revised-root'
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/temp-cleanup-20261026/execution/preserve.py:11`
  ```text
   T/'bolt-v4-20261022-cache-release/baseline-root',
  ```
- `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/temp-cleanup-20261026/execution/preserve.py:12`
  ```text
   T/'bolt-v4-20261022-cache-release/revised-root',
  ```

## main-config

无。

## bolt-config

无。

## recent-docs

无。
