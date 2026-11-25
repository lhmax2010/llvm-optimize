# 158 · QB manifest、编译基准和 154-B 核对

## 第 0 步 · 157 manifest 状态

**集成保留 UNQUALIFIED，生产打包仍要求 READY。** A 和 B 的 QB 专用测试提交只在选择打包 manifest 时显式传入 `allow_unqualified=True`。B 原样使用 G8 的 manifest。测试提交说明注明临时例外。SHA256、大小、项目及开关映射、重复映射、重复 JSON 字段及占位拒绝均沿用现有打包代码。

候选推送前，157 会调用集成提交的打包脚本，核对它对同一份 UNQUALIFIED manifest 以状态检查失败。测试提交的打包脚本须能解包并通过原有身份校验。另逐字核对集成脚本与配方、测试脚本与三处预期变更。A、B 的原准入继续生效。

[脚本 diff](../../tools/bolt/results/task158/157-manifest-status.diff) · [单测日志](../../tools/bolt/results/task158/157-manifest-tests.txt)

10/10 单测通过。初跑夹具误用会主动拒绝占位内容的打包器，并把命令行项目参数的错误码误期望为 1。修正两处夹具后重跑。157 等待单元于 04:14 PST 恢复，继续等待 G4。
