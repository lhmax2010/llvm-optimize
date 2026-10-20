# llvm_optimize 内网源码包：本地 upstream 续做停止记录

状态（2026-10-20）：**STOP_PATCH_BYTES_DIFFER**。第 2 步 spec 逐字节相同，8 个生成补丁均不相同，因此整体 FAIL；Release/tag 未创建；整包未生成、0 片；第 6 步 GitHub 回下及再导出未执行。**本页是停止报告，尚无可粘贴的下载脚本或已发布资产。**

上一轮 `7bab0df9193cab894c6efa3a84c7eda7e84a1b98` 的 native 回退停止记录保留在 [历史报告](https://github.com/lhmax2010/llvm-optimize/blob/7bab0df9193cab894c6efa3a84c7eda7e84a1b98/docs/llvm_optimize_intranet_fetch.md)。本次按用户新裁决，只调整浅克隆的本地 upstream 引用，使用原导出命令重验一次；没有加深历史、修改导出规则或把摘要差异自行豁免。

## 1. 本地引用修正与身份

W=`/home/linhao/Toolchain/development/llvm-optimize`；E=`W/temp/llvm-optimize-intranet-20261020`；S=`E/llvm`。沿用上轮浅克隆与全部历史证据，新导出写到 `E/export-tag-upstream`。

实际命令（`update-ref` 带旧值，防止误删其他引用）：

```bash
git -C "$S" update-ref -d refs/remotes/origin/upstream aadaa00de76ed0c4987b97450dd638f63a385bed
git -C "$S" -c user.name='Hao Lin' -c user.email='hao.lin@samsung.com' \
  branch upstream 'refs/tags/upstream/22.1.8^{commit}'
git -C "$S" rev-parse refs/heads/upstream
git -C "$S" merge-base HEAD upstream
```

后两条均输出 `ca7933e47d3a3451d81e72ac174dcb5aa28b59d1`。没有 fetch、Gerrit push 或远端建分支。

| 核对项 | 实际结果 |
| --- | --- |
| HEAD | `6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2`，PASS |
| tree | `80a6fd231c4564a3b762f4ec288cf2c41f9d2e20`，PASS |
| parent | `67619ec8bbbac7238a6cfc33a481ccfbcd12206f` |
| 当前本地分支 | `llvm_optimize` |
| origin URL | `ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm`，不变 |
| local upstream / merge-base | 均为 `ca7933e47d3a3451d81e72ac174dcb5aa28b59d1`，PASS |
| refs/remotes/origin/upstream | 已按授权删除；只是本地跟踪引用 |
| 工作区 | 干净；未改源码、spec、补丁 |
| W/gbs_llvm.conf | SHA `28f1caf93cd39738a7da1e0da8d5f945f7372963bb9823a507f9157294272169`，用户原有修改保留 |

**此仓库的本地 `upstream` 是为满足 GBS 检查而指向上游标签提交的辅助分支，不是 Gerrit upstream 分支的跟踪副本。不要用 `git fetch` 覆盖它；以后更新代码时只拉 sandbox 分支。** 现有 remote fetch refspec 本来就只覆盖 `sandbox/lhmax2025/llvm_optimize`。未来重新下载或打包成功后仍需核对本地 upstream 与 merge-base，并打印 `UPSTREAM OK`；本次未进行回下验证，不能宣称该项已交付。

证据：`E/resume-upstream-identity.json`（逐命令 argv、输出、退出码）；`E/clone-identity.json` 是上一轮身份记录，其中旧 origin/upstream 状态仅作历史。

## 2. 一次标准 GBS 导出与失败原文

除新输出目录外，与上轮的配置、spec、commit、outdir-directly、仓库路径完全相同；外层 scope 同样设置 TMPDIR、GIT_TERMINAL_PROMPT=0、LC_ALL=C。

```bash
TMPDIR="$E/tmp" gbs \
  -c /home/linhao/Toolchain/development/llvm-optimize/gbs_llvm.conf export \
  --spec llvm.spec \
  --commit 6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2 \
  --outdir-directly --outdir "$E/export-tag-upstream" "$E/llvm"
```

运行 20:22:53.885–20:24:03.925（UTC+08），GBS exit 0。日志原文：

```text
info: Generating patches from git (upstream/22.1.8..6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2)
info: llvm-22.1.8.tar.gz does not exist, creating from 'upstream/22.1.8'
info: Generating patches from git (upstream/22.1.8..6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2)
info: package files have been exported to:
     /home/linhao/Toolchain/development/llvm-optimize/temp/llvm-optimize-intranet-20261020/export-tag-upstream
```

全文不含 `native`，本轮已解决上轮的祖先检查回退；但内容门禁仍失败。比较器原始失败：

```text
AssertionError: export differs; do not package
```

它在检查完 spec 和全部 8 个 patch、保存 FAIL JSON 后退出 1。GBS 自身没有报错；失败的是用户要求的逐字节 / SHA 门禁。

| 文件 | reference-export.json 的 SHA256 | 本轮 SHA256 | 逐字节 |
| --- | --- | --- | --- |
| `llvm.spec` | `1da77fe8dfe45134bf7ae558ef366da2cfda6eccd917740449b85557b00e7f07` | `1da77fe8dfe45134bf7ae558ef366da2cfda6eccd917740449b85557b00e7f07` | PASS |
| `0001-Add-support-for-Tizen-toolchain-vendor.patch` | `a71a7503e851f4ebe1c192326d832c28f79a81ff1c9db43696d0487c118d587c` | `47e3915b6b5f6ecbc382b1ee37808cddb1817d5dc17b72f15af28d5b2d7bdb07` | FAIL |
| `0002-Link-libclang_rt.asan.so-against-libatomic-when-nece.patch` | `cefb73ec25a64f8c70cc0e585dfc688a23eb44b740093755ffaf8ee86f7e716e` | `cb71bb6cdfb7f13cbb38c085a0df1b58cdb02c62c4c30f5b67ef5317444d744d` | FAIL |
| `0003-Fix-armv7l-build-when-compiler-is-clang.patch` | `9ce436eb2f73e01b112cfeb10d6108e33c719b1db54a8fc404abdc10c367102b` | `2db35bd6292ffc9cf2e95037864851e36210349a1e78e8e91803cd967746f9ca` | FAIL |
| `0004-clang-add-support-for-LLVM-gold-plugin-in-case-of-ac.patch` | `45d68e84754f93ebe10ba80725e6cbb28826890e344f0ae910e061690105e944` | `a19fb1127c82382aaf27f5b0eb42900537f74a30835e4f43d5322c31836073d1` | FAIL |
| `0005-Merge-MLGO-AOT-compilation-support-and-optimization-.patch` | `da2cacae22ef8ececf808596b14ff53b6741db23e3f34d7fc5e07a75fa3543c2` | `6006e5191bbe2b275303f5a172a816a7fd7bd1131f3dcd8500063ff2e139b449` | FAIL |
| `0006-libcxxabi-declare-__gnu_unwind_frame-in-cxa_personal.patch` | `f52129a2f008603a3cf74fc1bf448d984b0f1827a48a9597f346223d87b98062` | `11871a7f2e6d84e53bdcf36220a9926db84b4558db61bb8053af2a02182445e1` | FAIL |
| `0007-libcxx-backport-EH-ABI-forced-unwind-handling.patch` | `b2d657339c18c5c1416bc9b3890afd39394b9ce46af061c1db809315ad4746d3` | `8d8026105ae3b75d53160db3888736e317706810ff358401640eb4f139a3703e` | FAIL |
| `0008-cmake-use-hybrid-LLVM-linkage-on-x86_64.patch` | `5bce5e43b16cf6fc8494ae4db489adf77e19489af8375144c524a8d70732c67e` | `60994d247eaed66645d623fe8521b2a86233f3b1df8f281ce1e44e50a827cfc2` | FAIL |

参考文件来自 `W/temp/hybrid-sandbox-20261019/patch-export`，与上轮 `E/reference-export.json` 再核 SHA 一致；参考 spec 同时与仓库内 `docs/52_hybrid_sandbox_evidence/exported-llvm.spec.txt` 一致。本轮生成 8 个 patch，缺失 0，匹配 0/8；spec 匹配。

证据：`E/tag-export-command.json`、`tag-export.log`、`tag-export-comparison.json`、`resume-export-gate.json`；完整差异 `E/tag-export-full.diff`。

## 3. 只读差异定位：Git 对象 ID 的缩写长度

8 个补丁共 **29 行 `index`** 不同：参考导出对象 ID 是 12 位，浅克隆导出是 9 位；9 位均为对应 12 位的前缀。每行两端各少 3 字符，共少 174 字节。去掉这些 `index` 行之后，8 个文件的其余字节分别完全相同。各 patch 的不同 `index` 行数为 **6、1、1、3、2、1、9、6**。

第一个差异原文：

```diff
-index 00c352b458c3..0e7107a1964e 100644
+index 00c352b45..0e7107a19 100644
```

对两个仓库只读执行：

| 命令 | 本次浅克隆 S | 上轮完整克隆 |
| --- | --- | --- |
| `git config --show-origin --get-all core.abbrev` | exit 1，无值 | exit 1，无值 |
| `git rev-parse --short HEAD` | `6e9d4f2bc`（9 位） | `6e9d4f2bc77e`（12 位） |

这些证据把本次字节差异定位到 Git 的对象名缩写；**不等于本轮门禁 PASS**。没有改 core.abbrev、没有重写生成 patch、没有重新 export，也没有通过加深历史碰运气。若后续允许显式固定导出对象 ID 的长度，可作为下一轮待验证选项；本轮不执行。

证据：`E/tag-export-difference-analysis.json`、`resume-export-gate.json`、`tag-export-full.diff`。该诊断不涉及编译产物或功能正确性。

## 4. 按失败分支要求：完整克隆只读历史测量

只读对象库：`W/temp/hybrid-sandbox-20261019/remote-check`。它不是 BOLT 工作树，也不是交接的 x86 构建树；未 fetch、checkout、repack 或修改任何引用。

输入重核：HEAD=`6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2`，origin/upstream=`aadaa00de76ed0c4987b97450dd638f63a385bed`，merge-base=`f2ccf80136a01ca69f766becafb329db6c54c0c8`，非浅仓库。

每个范围执行：

```bash
git -C "$FULL" rev-list --count "$BASE..HEAD"
git -C "$FULL" rev-list --objects --no-object-names "$BASE..HEAD" > objects.txt
git -C "$FULL" cat-file \
  --batch-check='%(objectname) %(objecttype) %(objectsize) %(objectsize:disk)' \
  < objects.txt > sizes.txt
# 将 HEAD 换成 origin/upstream，再做同样的只读测量。
```

`FULL` 与 `BASE` 为上面记录的完整路径和完整提交号。实际两套命令、对象清单和尺寸输出均已保存，不是估算。

| 范围（BASE=f2ccf801…） | 提交数 | 对象数 | 解压逻辑大小（B） | 当前对象存储大小合计（B） |
| --- | ---: | ---: | ---: | ---: |
| `f2ccf801..HEAD` | 59,531 | 842,118 | 25,291,906,027 | 1,084,457,989 |
| `f2ccf801..origin/upstream` | 401 | 4,520 | 132,138,933 | 4,713,417 |
| 两范围对象去重并集 | — | 845,575 | 25,391,302,393 | 1,087,995,218 |

| tip | 对象类型 | 数量 | 逻辑大小（B） | 当前存储大小（B） |
| --- | --- | ---: | ---: | ---: |
| `HEAD` | commit | 59,531 | 73,643,052 | 52,875,255 |
| `HEAD` | tree | 484,916 | 2,505,687,530 | 134,203,896 |
| `HEAD` | blob | 297,671 | 22,712,575,445 | 897,378,838 |
| `origin/upstream` | commit | 401 | 317,172 | 212,634 |
| `origin/upstream` | tree | 2,859 | 19,237,552 | 1,332,321 |
| `origin/upstream` | blob | 1,260 | 112,584,209 | 3,168,462 |

口径：`base..tip` 对象集合是 tip 可达、base 不可达的对象。`objectsize` 是未压缩逻辑大小；`objectsize:disk` 是现有完整克隆中每个对象当前表示的大小，可能使用 pack delta，不含 pack/index 开销及必要 delta 基对象闭包。**两列都不是网络下载量、加深所需新增量或可独立打包体积**；两范围还有交集，不能直接相加。没有实际加深浅克隆或生成测量包，不能从这些数值承诺最终压缩大小。

证据：`E/full-history-measurement.json`、`full-history-{head,upstream}-objects.txt`、`full-history-{head,upstream}-sizes.txt`、`object-measure-command.json`。测量运行 20:25:29.565–20:25:53.574，exit 0。

## 5. 交付状态、资源与回收

| 步骤 | 结果 |
| --- | --- |
| 本地 upstream / merge-base / HEAD / tree / origin / 干净状态 | PASS |
| GBS 不回退 native | PASS |
| spec SHA / 字节 | PASS |
| 8 个 patch SHA / 字节 | FAIL，0/8；仅 29 行缩写长度不同 |
| 完整克隆两个范围的只读提交数与对象体积 | 完成，见 §4 |
| repack、只打包 .git、split | NOT RUN；整包未生成，0 片，无整包/各片 SHA |
| GitHub Release/tag `src-llvm-optimize-6e9d4f2` | NOT RUN；本轮查询 release not found，未调用 create/upload |
| 固定 URL/大小/SHA 的内网脚本 | 未交付；不编造不存在的资产 |
| GitHub 实际回下 / HEAD OK / TREE OK / UPSTREAM OK / 再次 export | NOT RUN |
| GitHub main | 本报告与 STATUS 同一提交，原始证据只留 temp，无大文件入分支 |

轻任务沿用 6 GiB 准入、18 GiB cap、swap0、nice19/ionice3；每 2 秒检查宿主可用内存 2 GiB 与目标文件系统可用空间 30 GiB 底线。本轮 export 与只读对象测量共 47 个样本，最低宿主可用 **7202426880 B**、最低 /home 可用 **235623944192 B**，无保护中止。scope 退出后 MemoryPeak 已不可读，未编造峰值；没有构建、转换或重任务。

两个本轮 scope 均 inactive，项目锁在收尾释放；未创建挂载，无本轮导出进程或采样器残留。证据 `E/resume-resource-summary.json`、`resume-lock-released.json`、`resume-final-audit.json`。未改全局 Git 配置、W/gbs_llvm.conf、源码/spec/原补丁；未进入 BOLT 资产和交接树，未推 Gerrit。用户原有 gbs_llvm.conf 未提交修改保留。
