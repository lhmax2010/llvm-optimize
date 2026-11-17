# 118 E：交付打包 STOP

A STOP、B PASS（内部 BOLT 告警明细不可见）、C PASS、D STOP。未生成 H3，未查询或推送 sandbox。

第一次准备错误为报告编排的 JavaScript SyntaxError，修正为独立 Python 脚本后，四份报告和 STATUS 已写入。第二次准备错误：预计日志分析的 gzip 可以小于 10MB，实际压缩后为 30,478,003 B，大小断言失败。停止打包，不拆分、不重压缩、不重跑。原 JSON 和 gzip 均保留本地，路径、SHA 见 delivery-local-only.json；不将其加入 Git。

本次仅收尾保存已有报告、STOP 和符合大小限制的现有文本/压缩日志证据。私有 RPM 解包目录、生成的二进制夹具、scratch、缓存以及超限日志分析文件不入库。没有完成原计划的全量交付索引/哈希清单；不得把本次称为完整打包 PASS。

~~~text
COMPRESSED 30478003
Traceback (most recent call last):
  File "<stdin>", line 8, in <module>
AssertionError
Finished with result: exit-code
Main processes terminated with: code=exited/status=1
~~~

报告 raw 链接：

- [A 磁盘](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/118_disk_audit.md)
- [B QB](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/118_qb_1231417_1231418.md)
- [C 插件](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/118_plugin_load.md)
- [D helper](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/118_helper_fixes.md)
- [A STOP](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/tools/bolt/results/disk-118/classification-STOP.txt)
- [D 首次 STOP](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/tools/bolt/results/ps5-helper-118/first-test-stop.txt)
- [D 最终 STOP](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/tools/bolt/results/ps5-helper-118/retry1/STOP.txt)
- [E 首次错误](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/tools/bolt/results/ps5-helper-118/delivery-preparation-error.txt)
- [E 最终 STOP](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/tools/bolt/results/ps5-helper-118/delivery-second-STOP.txt)

E 已结束 2026-11-17T00:03:58.361869-08:00 status=STOP
