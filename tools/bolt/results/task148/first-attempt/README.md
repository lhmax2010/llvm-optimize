# 148 首次执行与修正

N2 关闭开关预检通过。N2 和 G4 的源码导出、构建根准备均成功，GBS 在编译前拒绝 noinit。第一轮 G4 已核对 G1–G3 的产物。N2/G4 使用独立新目录各重跑一次。按 144 B1 的成功命令使用 GBS 正常初始化，并配置独立 tmpdir，配方、快照、开关和门禁保持原值。

    error: build root broken caused by missing build conf. Please build without --noinit first
    error: <gbs>some packages failed to be built

第一次推送在 git diff --cached --check 遇到报告文件末尾空行，已修正渲染器。原始 ANSI 日志及 Git 交付输出见同目录。
