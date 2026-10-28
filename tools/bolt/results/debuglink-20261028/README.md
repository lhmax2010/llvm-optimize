# debuglink 20261028 前置认证证据

总状态 STOP，详见 result.json 和 [43号报告](../../../../docs/bolt/43_debuginfo_symbols.md)。

348 tests PASS；GBS export PASS；新根仅完成依赖安装和 %prep；五项 Tizen RPM 解析 PASS。
BOLT-off debug 全文比较多一个空行，未归一化，按门禁停止；release 比较及完整构建未运行。
initial-tests.* 保留环境/fixture 修正前原始输出；tests.* 为最后通过结果。
source/ 是本地69807d06完整spec/helper，不代表源码已推送Gerrit。
scripts/ 仅保存本次实际执行的测试、准备、解析脚本；未执行的后续验证草稿不纳入本次提交。
