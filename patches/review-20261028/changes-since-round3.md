# 第三轮外部评审之后的BOLT变更

评审基点是24号文档最终十四B的506dc25（父67619ec8），不是该文前半段停止快照。下面按实际交付演进顺序列出用户指定的六个版本；这些版本多次amend/rebase，不是一条可依次cherry-pick的Git链。当前两个补丁只对应67619ec8→6e9d4f2→f308fe08。纯提交说明折行（e2463165）不改变tree，列为备注而非产品改动。

0002是f308fe08相对hybrid父提交的累计BOLT补丁，helper为整文件新增，因此下表的位置是当前0002中的行号/函数锚点，不是历史增量hunk。

| 顺序/版本 | 改了什么 | 为什么 | 验证文档 | 0002大致位置 |
|---|---|---|---|---|
| 1 `af82efed1a688ba0877a4b4ca723922abbc96d20` | Source1200/1201移到Source1005之后并无条件声明；BOLT BuildRequires及执行仍受x86_64+开关保护 | GBS把生成的Patch声明插到最后Source之后，原条件块隐藏ARM和OFF模式的Patch0，造成No patch number 0 | 26号：旧版本复现、新版本五项导出spec解析；e246仅说明折行、tree相同 | L1733–1734，Source1200/1201 |
| 2 `9e5675f57d122549997caffa39b655dfefc46fee` | 取消全部发布磁盘门槛；四次disk-report；失败disk/not-disk/unknown诊断及按实际文件推算；atomic保存/候选原子替换；只包装BOLT专用命令 | 固定预留阈值阻断QB且会随产物失效；磁盘写满必须失败且不安装半成品。撤回e971对普通构建和平台链的包装，恢复基线执行方式 | 27号收窄修订：注入ENOSPC/非磁盘/诊断异常/unknown、结构比对、五解析 | L852 install_candidate；L1218 disk_report；L1385 disk_diagnose；spec BOLT函数/四报告段 |
| 3 `3d3b4bf564fd8edec793e49e6de75b5fa7007d16` | compare-root后释放唯一经核验的build/lto.cache；跳过异常路径，不影响构建；外层except Exception覆盖IndexError | 缓存最后在重链中用到，后续安装/转换/post不使用其内容；减少后处理占用，清理失败不能变为产品失败 | 30生命周期分析、32双轮完整构建和§15的300测试/解析/异常修复 | L1115 cache_release；spec BOLT_COMPARE_ROOT_PASS后cache-release |
| 4 `aa637c1b4a0f9ea9f6f0317cf035126eba85aeb7` | BOLT改动叠到不变的hybrid6e9d4f2之上 | 合并链接方式与BOLT验证；保留clang/lld/llvm-ar静态组件，其它工具走共享库 | 33：完整22+1 RPM、113白名单、profile匹配、90/90对象；保全产物 | 父提交改变不产生独立0002 hunk；hybrid代码在0001，0002的spec BOLT块沿用 |
| 5 `ac112ebfd6e7983bdfd4c38dd156e6baba72731b` | 用CMake RPATH_CHANGE将candidate RUNPATH对齐普通安装基线；llvm-bolt并行构建且核对真实任务集合；三处real对象检查 | 修复重链产物带构建路径/空项；降低工具构建耗时；用真实源码补充tiny门禁 | 37：317测试、完整构建、§10按用户批准ar日期口径完成23RPM/90TU/old-text和RSS；初始停止未掩盖 | L653 adjust_rpath；L715 real_gate；L971 tool_plan及tool_verify；L1480/L1485 pipeline；L1833 ninja -j宏 |
| 6 `f308fe08eeaad4e219f8505449b88bd5f644ea8c` | OPTIONS末尾仅追加-use-old-text，其余顺序/值、profile、白名单不变 | 37实验clang减少30,691,864B（16.75%），生成对象不变；用户决定采用 | 39：318测试、五解析/OFF一致、完整22+1、精确13a→8c身份、23RPM、90TU、1200RSS | L195 OPTIONS末项；提交说明L83；不新增其它生产函数变化 |

额外说明：26的提交说明重排与39重启后的本地资源调整不改变发布代码。41号崩溃定位是只读探测，尚未采用任何新方案：符号表版离线可解析24/24，objcopy --only-keep-debug失败；不把探测副本混入0002或files/。

验证链接：

- [24号 raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/24_rebase_recertification.md)
- [26号 raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/26_source_order_parse_fix.md)
- [27号 raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/27_disk_diagnostics.md)
- [30号 raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/30_cache_lifetime.md)
- [32号 raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/32_cache_release.md)
- [33号 raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/33_bolt_on_hybrid.md)
- [37号 raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/37_runpath_and_improvements.md)
- [39号 raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/39_use_old_text_final.md)
- [41号 raw](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/41_crash_localization_probe.md)
