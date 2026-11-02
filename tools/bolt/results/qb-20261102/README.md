# QB 1215143 / 1214821 只读证据

分析：[49号报告](../../../../docs/bolt/49_qb_1215143_1214821.md)。采集日期2026-11-02；没有构建、QB写入、源码修改或Gerrit推送。

- `1215143/`、`1214821/`：父概览/完整日志、各三架构LLVM包完整日志、RBS manifest、包仓库目录及编号摘录。
- `1215145/`、`1214824/`：实际执行子构建完整日志与配置/调度摘录。profiling和gbs_reports入口返回概览，不能当成取得了profiling表。
- `1215143/clang-*.rpm.json`：完整下载的两个RPM的URL、大小、SHA；`*-query.txt`及`*-files.txt`为VCS和完整文件列表。二进制保留在本地W/temp/qb-20261102/rpms，不重复提交。
- `1215143/rpm-identity-comparison.json`：实际QB clang与本地full-20261030 SHA/大小；QB不含debuglink/clang-22.debug。
- `1215143/tool-dry-run.txt`：113条真实任务；`tool-and-pipeline.json`、`json-line-23525.json`、`profile-summary.json`：原日志JSON与派生匹配摘要。
- `1215143/json-line-16322.json.gz`、`json-line-16324.json.gz`：普通安装基线和snapshot的大JSON，原文同时在完整包日志中；没有重新运行helper。
- `timeline.tsv`、各架构`*-timeline-excerpts.txt`：阶段锚点原文。`*-silent-gaps.json`：相邻有秒数日志行的前10个间隔，单位秒，含原始行号和文本；间隔不等于进程卡死。
- `1214821/first-error-context.txt`：Source1005失败完整traceback和前后安装上下文。
- `configs/`：两个固定快照的build.conf原件/压缩件、repodata目录和全文diff。SHA是固定快照文件，不冒充worker最终配置SHA。
- `source/`：独立裸克隆的只读git查询、原始提交/spec/转换器、差异和编号摘录。9b8d74af与67619ec8 diff文件0，tree相同。
- `current-toolchain/`：latest与reference分别查证；SRPM VCS均不等于67619ec8，因此没有下载static-devel或执行归档比较。`*-srpm-header.json`的SHA仅针对HTTP Range头部前缀。
- `failed-packages.json`：全部三架构失败目录枚举。B仅x86_64 llvm，A无失败。
- `provenance.jsonl`：追加式采集记录，URL、原始/存储大小和SHA；`url=null`为本地查询或派生结果。部分派生摘要后续补充，以`file-manifest.json`/`SHA256SUMS`为最终文件身份；`compression.json`记录大JSON压缩对应关系。
- `limits.txt`：访问失败/无法确认范围；不将缺失日志作为通过证明。

## 复核方法

```sh
sha256sum -c SHA256SUMS
gzip -dc 1214821/x86_64-llvm.log.gz | nl -ba | sed -n '16311,16350p'
gzip -dc 1215143/x86_64-llvm.log.gz | nl -ba | sed -n '23727,23728p'
```

行号一律按解压后的完整原文。没有导出浏览器cookie、登录表单或认证头。所有超过1MiB的文本均已gzip，完整文件校验清单见SHA256SUMS。
