# ThinLTO 缓存释放与双轮本地测量（2026-10-22）

状态：实现与单元测试、五项解析 PASS；未改 9e5675f 的基线完整构建正在运行。尚不能回答实际 BOLT 增量、峰值降幅或候选/RPM 是否相同，不能用历史 97 GB 缓存替代本次测量。

## 1. 源码与边界

本地源提交 `d20e873b2c7dfac10fab9235e2b781dad08dc4c7`，父 `67619ec8bbbac7238a6cfc33a481ccfbcd12206f`，在 `9e5675f57d122549997caffa39b655dfefc46fee` 上 amend。保留 Change-Id `Ic98eab90cc017f127a66e1729b44fab8b8e8fb41`；作者、提交者和 Signed-off-by 为 Hao Lin。不改全局配置、不访问 Gerrit。

源码仓库原为 detached HEAD，没有名为 bolt_pgo 的本地分支；沿用此前 detached amend 做法，不新建分支。这里的本地提交没有推送到远端 bolt_pgo。

spec 仅在 `echo BOLT_COMPARE_ROOT_PASS` 后新增以下三行，移除这三行后与 9e5675f 全文逐字节相同：

```spec
# No subsequent step consumes this ThinLTO cache.
# Release it only inside the enabled x86_64 BOLT block.
python3 -B %{SOURCE1201} cache-release "$PWD" "$BOLT_WORK"
```

普通构建、基线安装、Source1005、平台 post 链、四次 disk-report 均未改。源码全文 diff、完整 helper/spec、结构检查见本页证据目录。

## 2. helper 行为

新命令先调用 `replay_script` 验证 link.original 的完整格式及唯一绝对缓存路径规则；再要求 realpath 与 build/lto.cache 相同、路径为实际目录且不是软链接。否则输出 skipped 并返回 0。删除前 disk_entries 统计普通文件数和实际 allocated bytes（含目录）；rmtree 成功输出 removed、耗时，并原子保存 cache-release.json。部分删除失败输出 partial 和可读剩余文件数（统计失败时为 unknown）。记录文件写入失败仅报告 record-unavailable，不改变成功退出约定；参数用法错误由 argparse 返回 2。

disk-report / disk-diagnose 未修改：缓存缺失时 disk_entries 返回空集合，正增量为 0，净变化允许为负数。原因仍取自失败 errno/日志，缺失缓存本身不是磁盘失败。新增测试验证了释放后的非磁盘诊断和真正 ENOSPC 诊断。

## 3. 已完成认证

- 全部 299 测试 PASS：既有 289 + 新增 10。原始 stdout/stderr 已保存。
- 新增覆盖：正常删除、外部路径跳过、软链接跳过、目录缺失跳过、中途删除出错、重复缓存参数跳过、link.original 缺失、JSON 写满、参数错误、释放后报告与诊断。
- 新提交 gbs export PASS；Tizen rpm/rpm-build 4.14.1.1-1.7 五项解析全部 PASS，每项保留七个 Patch。
- profile 和 Source1005 与 9e5675f 字节相同。生产 helper 与测试镜像相同。

## 4. 构建条件与采样口径

固定 Base `20261013.024319`，仅 packages/debug 两仓库；build.conf SHA256 `e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945`。使用既有 `gbs_llvm_qb1202084.conf`，命令行 -B 指向本次新根，不改旧配置。

本地 GBS 2.1.0，与 QB NGBS 有差异。外层 --threads=30，三个宏为 `jobs 8`、`_smp_mflags -j8`、`_costomized_smp_mflags -j20`；固定 build.conf 和 spec 的 mlgo_build_jobs=6 保持。没有额外 shelve。GBS 包构建入口实际 argv 也存入日志。

仅在本次新根执行构建，历史根完全不动。每段共享 heavy-stage.lock 独占最多 3400 秒，加退出清理仍小于 60 分钟；16 GiB / swap0 / nice15 / ionice3，开始 MemAvailable >=12 GiB，低于3 GiB停止。本地磁盘准入参考为历史219.931 GiB下界+15 GiB BOLT估计+20 GiB导出保留+30 GiB底线，非精确峰值，也不是发布代码门槛。采样每60秒，资源每5秒。

同时记录外层 GBS 根与独立 chroot 根：普通用户外层 du 对 usr/share/upgrade、var/cache/ldconfig、root 有权限盲区，错误原样保留；补充以既有 sudo chroot 权限在本次新 chroot 内执行 du -sx -B1 /，完整根读数单独存档，不把盲区读数称为完整值。三个盲区初次各12,288字节。普通 sudo du 未授权，没有绕过或改权限。

修订 spec 的解析使用新基线根中的 RPM，专用 /home/abuild/cache-release-parse 仅存两份小 spec；不执行其安装或构建，不影响基线源码。此验证小目录占用须在最终测量中列明。

## 5. 准备性修正

第一次启动遗漏 tar 模式的预导出，8.323秒即失败，未进入 %prep：

```text
/usr/bin/build: line 1215: cd: .../baseline-root/local/sources/tizen_base_toolchain_standard/llvm-22.1.8-1: No such file or directory
llvm.spec is empty.  This should not happen...
```

补齐 gbs export 并明确 --spec llvm.spec，第二次启动成功进入 %prep/%build。该准备类修正一次；原始失败日志保留。只读定位 RPM 临时脚本时按实际日志确认目录为 /var/tmp，采集器补入该目录，不修改任何产品输入。du 权限盲区按第4节另列完整 chroot 读数。

## 6. 双轮结果

待完整构建完成后更新：阶段时间、四次报告、峰值、cache-release 原文、候选SHA、逐RPM文件和SHA差异、tool-plan/compare-root/post。当前不得宣称这些门禁已通过。

## 7. 原始证据

目录：[`tools/bolt/results/cache-release-20261022/`](../../tools/bolt/results/cache-release-20261022/)。源码、测试、解析为已完成材料；构建运行记录最终补齐。没有删除历史目录或任何缓存。
