# 夜间串行入口（仅本地）

白天只运行 `launch.sh SOURCE_SHA rehearsal toolchain|basedev`。完整构建必须由用户另行启动：

```sh
/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/night-launch-20261103/launch.sh 9e39fa8a61392652bb28b75fc26216675bcad1d5 night
```

源码 SHA 必填，HEAD 不同、已跟踪文件不干净、配置或模板 SHA 不符、目标根已存在均拒绝。
未跟踪文件不阻断。入口使用 final-launch 的 GBS driver 布局；不修改源码和发布参数。

`night.py` 等待 T 的构建、验证、正常卸载和审计结束，再启动 D。T 一般构建或验证失败仍运行 D；
磁盘停止、OOM、残留进程/挂载或无法确认清理时停止整个流程。D 没有 T 候选时不能声称 D/T 90 TU 通过。
每项和整个流程都有带时区的“已结束”状态。认证装包不自动运行，留待次日。

主要文件：

|文件|用途|
|---|---|
|launch.sh / night.py|POSIX 入口、串行协调器、进度日志|
|launcher.py / provenance.json|模板 SHA、导出/准备/构建服务、新根、清理审计|
|validate.py|T 身份/23 包/90 TU；D 验证调度|
|checks.py|命令记录逐字节证明、ar 日期三条件、debuglink CRC、参数日志|
|release_checks.py|转换成员 debug 节、真实 C-2、MODULE 命令和 dlopen、包差异|
|rpm_io.py / rpm_extract.py|RPM 载荷清单与新目录提取，解析 cpio 硬链接|
|resource_report.py|每根资源表、临界停止分类；缺失数据 UNKNOWN|
|test_checks.py / test_startup.py / test_integration.py|白天夹具（部分需要新 scratch 目录）|
|audit_rehearsal.py|与51号实测字符串逐字节对照；不调用 CMake/Ninja|

所有验证输出写到新根的 `validation/`，构建和资源证据写到 `evidence/`。
写入已有验证目录会拒绝。所有生产门禁不变。命令记录例外逐个记录差异字节，节外、头表、大小均严格比较；
缺少必要中间文件时拒绝证明，不能凭最终 SHA 猜测。

资源：MemoryMax=MemTotal−8GiB，swap=0，CPUQuota=1200%，nice10，ionice2/7；
构建根 du 约60秒，cgroup/df约2秒，llvm-bolt进程约10ms。整次 `memory.peak` 包括文件缓存；
分阶段内存是 `memory.current` 的采样最大值，不冒充独立阶段 `memory.peak`。

详细结果与尚待真实 release 数据的项目见 docs/bolt/53_night_validation_prep.md。

## 55 号修订：保留产物重新验证

`revalidate.py` 不构建、不挂载、不调用 sudo。它要求两根的 `validation-02/`
尚不存在，再在独立的 16 GiB、swap=0 的 systemd 用户服务里先 T 后 D。
本轮额外限制 CPUQuota=200%，nice10、ionice2/7。普通比较失败会如实保留并继续
独立项；MemoryError 或验证服务 OOM 停止队列，不再启动 D。

日志只读 `gbs-driver/local/repos/*/x86_64/logs/success/llvm-*/log.txt`，超过
1 GiB 拒绝，逐行筛选，不读取累计 `evidence/rpm-build.log`。RPM 也只在
`gbs-driver/local/repos` 查找；认证基线的 `products` 是显式选择，不作回退。
`log_support.py` 按原始 `[NNNNs]` 锚点划阶段，以开头的 UTC 开始行映射原始采样。

`section_compare.py` 实现用户批准的三个记录节例外，逐个记录内容与结构变化。
`.comment` 只接受编译器/链接器标识；`.GCC.command.line` 比较字符串计数。
`.symtab`、`.strtab` 和代码等非记录节仍严格比较。`checks.debuglink_proof`
仅在符号文件的严格比较通过后允许 CRC 四字节变化；不能因为可符号化就放行。
历史 53 号的“节大小必须相同”判据由 55 号批准的记录节规则取代。

`test_revalidation.py` 保留全部夹具，`NIGHT_TEST_ROOT` 可指定一个不存在的新目录。
禁止原地执行有固定历史输出路径的 `test_integration.py`；本轮使用新夹具目录。
详细执行结果见 `docs/bolt/55_night_revalidation.md`，不能把入口修复等同于产物认证通过。

真实包验证补充：ELF 允许重名节，比较器按有序实例核对；不额外要求名称唯一。
不同 RPM 共用同名普通文件时，仅在 SHA 完全相同的情况下复用提取副本，
不同内容或符号链接均失败；不覆盖已有副本。补检入口保留首次失败结果，
`correct_duplicate_sections.py` 只重算误拒输入，`resume_release_checks.py` 只补 release 项。
