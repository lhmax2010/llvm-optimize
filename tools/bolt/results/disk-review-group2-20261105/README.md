# 65号只读盘点证据

被分析对象没有删除、移动或修改。所有生成文件只写到本结果目录及65号/STATUS文档。

- `targets.json`：13个精确分析目录。
- `previous-finished.txt`：64号结束记录；`started.json`、`df.txt`、`mounts.txt`、`services.txt`：开始状态。
- 各目录 `inventory.json`、`files.jsonl.gz`：du原文、完整可读文件元数据、权限/超时；不遍历.git内部。
- `*-references-v3.txt.gz` 与 `reference-index.md`：最终脚本/文档引用；v1/v2中间结果保留，不用来声称覆盖完整。
- `git-review.json`、Git原文gzip：原要求的branches/tags、detached HEAD、stash、tracked status。
- `git-remote-followup-v2.json`：最终Gerrit可达性结论。v1 stdin排除写法错误，保留中间结果；v2逐行加`^`后排除已有的远端commit对象，不fetch、不修改refs。
- `rpm.tsv`、`rpm-catalog.json`：全部RPM路径、大小、实测SHA及同SHA位置；未完成哈希记UNKNOWN，不使用旧摘要替代。
- `assets.tsv`：工具/profile/products和probe产物的大小、SHA、已核对副本。
- `small-evidence.json`：顶层小报告/脚本与Git跟踪文件的同名同SHA比较；未查到不代表全局唯一。
- `archive-copy-comparison.json`：四组归档逐个实测SHA。每组480秒；超时后只把已核对相同的文件列为候选，其余保留。
- `recommendation.json`、`retain-files.tsv.gz`、`suggested-files.tsv.gz`：精确保留/建议瘦身边界，不是执行脚本；所有RPM、profiles和未发布Git内容均保留。
- `profile-correspondence.json`、`profile-semantic-comparison.json`：23原始fdata与旧清单、Source1200的核对。merge-fdata输出顺序非固定，完整行多重集相同不等于新重合并SHA相同。
- `handoff-assets.json`：内网源码完整归档和5分片当前SHA，与保留清单6/6一致。
- `usage.json`：普通用户/proc检查，有权限盲区，不能当成未来删除的无占用授权。

所有du/sha256sum使用`nice -n 19 ionice -c3`并带timeout。各Python采集脚本保存了命令参数和返回值；没有运行cmake/ninja/gbs，没有sudo，没有QB/Gerrit写操作。副本检索仅覆盖记录范围，不推断旧自构建RPM一定能在下载站重新取得。

`merge-fdata-ordering.raw.txt.gz`保留带行号源码摘录原文；`.txt`阅读版仅清掉空白行行号后面的行尾空格。
