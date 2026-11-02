# Stripped ordinary clang 尺寸口径

本轮仅对 `W/temp/review-20261102/size-baseline/` 内的副本执行 strip；没有在构建根内运行命令或写入，没有修改原 ordinary 文件。W 为 `/home/linhao/Toolchain/development/llvm-optimize`。

## 本次实测

| 项目 | 值 |
|---|---|
| 输入 | `/home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028/full-20261030/products/binaries/ordinary-clang-22` |
| 输入字节 | 1,793,485,376（含 DWARF） |
| 输入 SHA256 | `d5090159915657b235b96f1202c058e1efd1647d6a2225ac8fdb2906aeaa501d` |
| 输出 | `/home/linhao/Toolchain/development/llvm-optimize/temp/review-20261102/size-baseline/ordinary-clang-22.stripped` |
| strip 后字节 | **139,929,432** |
| strip 后 SHA256 | `eab52018354b9bdd3bdd34b21cfb7731c28883b509fe371566b246c3a5e391cc` |
| 工具 | `/home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028/full-20261030/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-strip` |
| 工具实际实体 | `/home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028/full-20261030/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-objcopy` |
| 工具 SHA256 | `d5699b8f418931119d49ea82848c708e3252fea4e820f8d7373e5230e515d79d` |
| 参数 | `--strip-all <新副本>`，与 helper 的 strip_all() 相同 |
| strip 退出码/耗时 | 0 / 3.110396s |

发布 helper 的 `strip_all()`（本包 `files/packaging/clang-bolt-helper.py:1624–1634`）先复制再执行 `[tool, '--strip-all', after]`。工具 SHA 与 full-20261030 的 identity 中 strip_tool_sha256 一致。由于在宿主的试验目录执行 Tizen 工具，本次显式用该根 loader 和运行库启动，未使用 chroot 或进入构建根。

实际完整 argv（原始数组另见 `evidence/argv.json`）：

```sh
/home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028/full-20261030/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/lib64/ld-linux-x86-64.so.2 --library-path /home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028/full-20261030/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64:/home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028/full-20261030/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr/lib64:/home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028/full-20261030/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/lib64 /home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028/full-20261030/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-strip --strip-all /home/linhao/Toolchain/development/llvm-optimize/temp/review-20261102/size-baseline/ordinary-clang-22.stripped
```

原候选的执行记录见 `evidence/historical-candidate-strip-argv.json`；本次 stdout/stderr 见 `evidence/strip.stdout`、`evidence/strip.stderr`。输出没有 `.symtab` 或 `.debug_info`；原件执行后重新计算SHA仍相同，见 `evidence/original-after.json`。二进制副本仅留本地，不放进本评审包。

## N、P

```text
最终打包 clang = 152,532,400 B
本次 stripped ordinary = 139,929,432 B
N = 152,532,400 - 139,929,432 = 12,602,968 B
P = 12,602,968 / 139,929,432 × 100
  = 9.006659871241384% → 9.0%（一位小数）
.gnu_debuglink 贡献 = 152,532,400 - 152,532,296 = 104 B
```

这比较的是 clang 实体，不是 RPM 压缩包大小；不把去掉 ordinary 的 DWARF 带来的差额当作 BOLT 收益。

## 历史数值核对

`139,930,576 = 183,224,160 − 43,293,584` 是本次提示中的算式，**不能确认它是同一 ordinary 按同样 strip 处理的历史实测**。在 docs/bolt 和结果目录的未压缩文本中，没有找到这个尺寸的独立产物记录；完整搜索命中保留在 `evidence/historical-size-hits.txt`（压缩日志未作穷举解压）。可直接查到以下来源：

- `docs/bolt/01_bolt_v4_design.md:43,190`：历史 RPM ordinary 为 **139,929,464B**，SHA `3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c`；当时 BOLT strip-all 为 **183,223,048B**，差额 **43,293,584B**（约31.0%）。
- `docs/bolt/02_inventory.md:30` 与 `docs/bolt/03_strip_experiments.md:7,28,34` 同时记录这个旧输入、大小及 strip 结果。结果中的 `tools/bolt/results/validation-expected-differences.json:5481` 也记录旧 RPM 基线139929464B。
- `docs/bolt/37_runpath_and_improvements.md:158,198`：**183,224,160B** 是后来的 hybrid+BOLT候选；不是上述183223048B旧候选。将后者沿用的43,293,584差额从这个新尺寸中扣除，得到的139,930,576不是已查证的ordinary产物。

本次139,929,432比该算式少 **1,144B**，比历史RPM ordinary少 **32B**。可以确定历史比较使用了不同SHA的普通RPM基线，而且混用了两个年代的BOLT候选尺寸；这32B的具体ELF字节成因本轮没有进一步实测，不能归因到某个节或参数。因此按用户裁决采用**本次同工具/同参数的实测值**，不沿用算式。

上述文档固定版本可从以下前缀读取：
`https://raw.githubusercontent.com/lhmax2010/llvm-optimize/0dc274528111434f03854b17f6c24109e68e80fe/`
