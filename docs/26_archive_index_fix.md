# 26 llvm-static-devel 归档索引修复：RPM 基线普查与运行库格式门禁

日期：2026-09-23（+08:00）。起点提交：`c12c0e1a966ceac9b400035777e47882e4628471`。
归档索引修复仍是当前第一任务，设计 v4/BOLT 暂缓。本报告自包含；docs/25 保留原文。

**本轮完成 22/22 RPM 身份核查、全新解包、270 个唯一归档的普查和 RPM 宏链取证；在第一步第 4 项停止。**
停止原因：`libarcher_static.a` 的唯一成员 `ompt-tsan.cpp.o` 是 LLVM bitcode，头部 `42 43 c0 de`，当前索引为空。
它同时属于 `libomp-devel` 与 `llvm-static-devel`。用户规定运行库 libarcher 含 bitcode/其他格式即停，
所以未扩大修法范围、未修改试验 spec、未修改构建认证入口，也未启动完整构建（**0 次**）。
**尚无可提交的归档修复补丁，无新 RPM，无新包验收通过结论。**

这次停止是实际成员格式触发，**不是旧 build.ninja 身份问题**。按用户更正，旧全静态构建树在 docs/15 的 configure 是已登记合法变更；
本轮不再读取/校验它。旧混合构建根继续隔离，未读写。

## 0. 独占、输入与访问范围

| 别名 | 本机路径 |
| --- | --- |
| W | `/home/linhao/Toolchain/development/llvm-optimize` |
| E | `/home/linhao/Toolchain/development/llvm-optimize/temp/archive-index-fix-rpm-20260923` |
| R0 | `W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0` |
| J | `W/temp/baseline-resume-20260917`，docs/13 的 inventory/证据 |
| H | `E/baseline-rpm-extract`，本任务唯一基线内容 |
| S | `W/temp/llvm-archivefix-trial`，`archive-fix-trial` |
| Rnew | `W/temp/gbs-root-x86_64-archivefix`，尚未 GBS 初始化 |

进入时主仓库 `git status --porcelain` 为空；扫描 `/proc`，未发现其他 rpmbuild/gbs/ninja/lld/ld.lld/llvm-bolt 进程。
证据 `E/exclusive-precheck.json`。复用 S 的检查全部通过（`E/source-precheck.json`）：

```text
HEAD=f111162e94aa48ed367c9d2c039456c70e7160ae
branch=archive-fix-trial
spec SHA256=95887b2d060b38d5ef8f56936f7481a03d131f9d26432180a68e02ec95f0dda5
status= M packaging/llvm.spec
```

相对 HEAD 的 diff 与 docs/25 保存的三处 4/4/1 并发 diff 完全相同，无其他源码修改。
原 W/llvm spec 未改，S 的 spec 到停止时也未改；docs/25 SHA 未变，见 `E/preservation-check.json`。

在 Rnew 以 O_EXCL 重新取得 `.llvm-optimize-exclusive.lock`：

```text
session=archivefix-rpm-55507c4264ff48f088600c623840f969
pid=1566499
started=2026-09-23T22:47:47.456340+08:00
```

核查/解包/普查/报告期间持续持锁，收尾核对归属后删除并回收持有进程。
`E/lock-acquired.json`、`lock-released.json`、`final-cleanup.json` 留存生命周期。
没有构建 scope/构建采样器启动，不能将其资源数据记为已测。

**R0 仅读取 `home/abuild/rpmbuild/RPMS/x86_64/` 的这 22 个 RPM，以及 `usr/lib/rpm/` 的宏/脚本。**
未读取 R0/BUILD、rpmdb、旧 SOURCES、旧安装树；未使用 `temp/toolchain-baseline`。
为确定宏内容对应的 NEVRA，另取固定快照的 rpm/rpm-build 包元数据，方法和边界见 §3.2。

## 1. RPM 基准核对与新解包：PASS

参考 `J/rpm-inventory.json`，逐个对原路径 RPM 计算 SHA256，**22/22 全匹配**。
完整路径和预期/实际 SHA 在 `E/rpm-baseline-check.json`；下表 SHA 同时是预期和实测值。
所有包名均加后缀 `-22.1.8-1.x86_64.rpm`，位于 R0 指定 RPMS 目录。

| 包名 | RPM 字节 | 预期 = 实测 SHA256 | 结果 |
| --- | ---: | --- | --- |
| `clang` | 310023082 | `f126062d8ef1f2e95e5a3bdfba3ba02470ad1bfac14b15728a8d334997d5f8cc` | PASS |
| `clang-debuginfo` | 2928319534 | `c5db7fb7369741db11694e51626bbfc313adb49753b022fb3e80cef3e62791ac` | PASS |
| `clang-devel` | 4098834 | `ff37c18ed4bbfc2b9761137655b5795b6d5e977aee3a92c8d3371cdd9c043e12` | PASS |
| `clang-devel-debuginfo` | 5729298 | `b6975ac7b700114f00d8e47f84ad98066d6ad0e434a6bb54e0c692300c48d672` | PASS |
| `compiler-rt` | 3722242 | `c2e17444ddcf24771100d998fa1df4732771adf63c3a33241dff6a487129d1c4` | PASS |
| `compiler-rt-debuginfo` | 1288278 | `db37405aaacdee0d715854ef74e6f4be53d8769021e56df861c18650034d91e6` | PASS |
| `libllvm` | 23650574 | `73e2b20c3f561743bf71e8b3a585a822cfc6c6ceb9b154c0db00546b05625698` | PASS |
| `libllvm-debuginfo` | 198056846 | `91f0047418db40d27d8b53a324414d8165f2b75dafc86b0bd016df2c8c27d0ca` | PASS |
| `libomp` | 373374 | `50d087870ccdf36108fe8bfec395122a213e25d7b833345166c291faab1639a3` | PASS |
| `libomp-debuginfo` | 1142190 | `071d85c7e5a3adbdb11057acd05de6469b57093fa71187fec57c4b605c1bff31` | PASS |
| `libomp-devel` | 250126 | `0e9a9dc76426e6242a04f5d396ff2c6ce632e0414b3872e310d767f6cce4c47a` | PASS |
| `lldb` | 30763794 | `309834e1808a413e9415f74d555d2240cd15882451fb20748839b8ab2d1ef441` | PASS |
| `lldb-debuginfo` | 332845250 | `227ebf7b0808daf206dd2489b419ed7c212bf3bf1d09ab964c83437021cb195c` | PASS |
| `lldb-devel` | 30520458 | `a7c25e7724760f9fd25b1f011fe6ff808a91662b79f4fde1cc1c6341082ecc0e` | PASS |
| `lldb-devel-debuginfo` | 279580570 | `a202aa6de6043347dab2c5bc0159e23b4a4c440f9c661069792344931411c205` | PASS |
| `llvm` | 410629530 | `cd798dbcf13cd59c2be6859df2666370044f51c8cd3282ab266924e297514ee1` | PASS |
| `llvm-debuginfo` | 3842661714 | `e9fd72d62145ca047dcf50bd6150e86a987f8995706dcde666b43773e5827f76` | PASS |
| `llvm-debugsource` | 43651146 | `2f0bae899b69620c09a23d3e963ff8329ee0a7607e987451bd7a50fa24ad1a3c` | PASS |
| `llvm-devel` | 41191450 | `cf3250150bcae5b99c3fafbf18a1f37fff434f5edc27239ef55eb6cdf86fb211` | PASS |
| `llvm-devel-debuginfo` | 308603238 | `477c41cb90a5403781952cd69ae9015860fc8cd3b7bb6ac2092002dfb5992109` | PASS |
| `llvm-static-devel` | 1375822930 | `a39a17cfffea1c5fd4ce84231bb563115bc0d7dca3f54774eb2d1b8c88894b02` | PASS |
| `python-clang` | 36322 | `0244071cd46fb03ab0a856d6e13166922f3a81f19901645f54ec63ce67c49c22` | PASS |

全部通过后才创建 H，逐包执行 `rpm2cpio` → `cpio -idmu --no-absolute-filenames --no-preserve-owner`，
检查管道两端退出码，**22 对均为 0**。未安装到宿主。
每包 `rpm -qp` 文件清单及 mode/digest/link 元数据写入 `E/<包名>-file-metadata.tsv`；
重叠路径的这些属性逐项一致才允许合并解包。所属包映射为 `E/baseline-file-owners.json`。
全过程日志为 `E/baseline-extract.log`、`baseline-extraction-status.json`；解包入口源码 `E/extract_baseline.py`。

指定坏归档 H/usr/lib64/liblldCOFF.a 核对 PASS：

```text
SHA256=9e8915f4a853a8a97285f34c2b51eb2bc16eb3fb3de943fdabf43f1b3e252617
```

证据 `E/bad-archive-identity.json`；它仍保留原始坏索引状态，没有执行 ranlib/strip 或其他修复。

## 2. 归档普查：完成，运行库格式门禁 FAIL

### 2.1 方法与证据边界

命令（完整 argv 和退出码为 `E/census-command.json`）：

```bash
nice -n 15 ionice -c3 taskset -c 2 \
  prlimit --as=4294967296 --core=0 -- \
  python3 tools/census_llvm_archives.py \
  --root temp/archive-index-fix-rpm-20260923/baseline-rpm-extract \
  --owners temp/archive-index-fix-rpm-20260923/baseline-file-owners.json \
  --output temp/archive-index-fix-rpm-20260923/census
```

串行、CPU 2、4 GiB AS、nice 15、ionice idle。没有执行归档成员，也没有生成或修复索引。
运行输出 `E/census.log`；最终摘要 `E/census/census.json`、`E/census-summary.json`；退出码 **2** 表示 `FAIL_RUNTIME_FORMAT`。

[inspect_llvm_archives.py](../tools/inspect_llvm_archives.py) 按 ar 文件头识别普通/thin，按成员数据实际 magic 识别 raw/wrapped bitcode；
本次机器码成员均是 ELF ET_REL，依据 ELF class、endianness 和 e_type 判别。其他格式单列，thin 不跟随外部文件。
GNU 32/64 位索引的成员偏移解析为 **序号、成员名、同名出现次数**；保存每条符号映射的原始次序。
不支持的索引格式或损坏格式显式报错，本轮未遇到这类解析错误。
每个成员记录字节数、SHA、ar mtime 和前四字节，完整 JSON 在 `E/census/archives/<归档相对路径>.json`。

“索引是否恰为机器码成员符号”通过 ELF `.symtab` 中已定义的外部 global/weak/GNU-unique 符号与 ar 索引多重集合比较，
包含成员序号及同名次数，保留重复项。**此列为 YES 不等于 bitcode 归档索引完整**：纯 bitcode 归档的机器码符号集合为空，坏索引也可能为空。
最终包对本次构建树的顺序映射验收工具入口已有 `--compare`，但本轮未执行这一新产物验收。

检查器及普查停止规则的 10 项测试通过，含 5 个运行库/开发库格式门禁子例。
覆盖 native/bitcode/unknown、混合归档、重复成员、错指成员、索引次序、64 位索引、GNU 长名称、thin 不跟随、损坏输入。
原始输出 `E/archive-parser-tests.log`；测试 [test_inspect_llvm_archives.py](../tools/test_inspect_llvm_archives.py) 使用合成字节夹具，没有编译 LLVM 或小程序。

### 2.2 汇总与包内重复归属

| 口径 | 归档数 | 成员数 | bitcode | 机器码 | 其他格式 | thin | 空索引数 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| compiler-rt | 45 | 1964 | 0 | 1964 | 0 | 0 | 3 |
| llvm-static-devel（包含 libarcher） | 225 | 3864 | 3853 | 11 | 0 | 0 | 222 |
| libomp-devel 中 libarcher_static.a | 1 | 1 | 1 | 0 | 0 | 0 | 1 |

**唯一归档路径 270，按包归属计 271 条。** `libarcher_static.a` 同时出现在 llvm-static-devel 和 libomp-devel，
包元数据的 SHA/mode/link 一致，是同一路径同内容；上表后两行不能直接当作互不相交的文件集合。
若单列 libarcher，剩余 static-devel 独有归档是 224。
证据：两个包的 file-metadata.tsv、`E/baseline-file-owners.json` 和 `E/census-summary.json`。

compiler-rt **45/45 全部成员为原生 ELF ET_REL**，本轮未发现 bitcode/其他/thin。
45 个索引均恰好包含各自机器码成员的可索引外部定义，未发现这批 RPM 的索引遗漏。
其中 asan-preinit、hwasan-preinit、memprof-preinit 三个 x86_64 归档各只有一个机器码成员，无上述外部定义，所以索引为空；
不能套用“非空才通过”的错误判据，也不由此宣称其其他内容经过消费者验证。

static-devel 的三个混合归档当前索引如下，其他 222 个包内归档索引为空：

| 归档 | 成员 | bitcode | 机器码 | 索引条目 | 是否恰为机器码符号 |
| --- | ---: | ---: | ---: | ---: | --- |
| libLLVMAnalysis.a | 131 | 125 | 6 | 82 | YES |
| libLLVMCodeGen.a | 238 | 237 | 1 | 1 | YES |
| libLLVMSupport.a | 179 | 175 | 4 | 22 | YES |

这组数量是 **docs/13 全静态 RPM 基线**的新普查；不替换 docs/22 混合产物的历史 226/223 等计数。
没有使用旧构建树补造“构建前索引”列。

### 2.3 明确停止项：libarcher_static.a

```text
路径：H/usr/lib64/libarcher_static.a
归属：libomp-devel、llvm-static-devel
归档字节数：709448
归档 SHA256：6266af6cbc5e283a417119b0fdab0c488c9a0bbced1d9bc5d4deab89ffaee38c
成员：ompt-tsan.cpp.o（第 1 个、同名第 1 次）
成员字节数：709380
成员 SHA256：ff1da15491c7e7ee91e8894bda5a6b3bb41767440e96746e6a0a86e7ef0b6e85
数据偏移：68
前四字节：42 43 c0 de
格式：LLVM bitcode
索引条目数：0
thin：NO
```

原始只读交叉确认（`E/runtime-blocker-raw.json`，两命令退出 0）：

```text
$ /usr/bin/ar t H/usr/lib64/libarcher_static.a
ompt-tsan.cpp.o
$ od -An -tx1 -j 68 -N 4 H/usr/lib64/libarcher_static.a
 42 43 c0 de
```

用户第一步第 4 项要求 compiler-rt **或 libarcher** 含 bitcode/其他格式即停。故本轮在普查完成后停止，
不因为它同时在 static-devel 中就自行视为已获范围豁免。
需要用户明确该运行库现有 bitcode 索引缺陷是否纳入后续修复/验收范围；本轮不自动改判或扩大范围。

## 3. RPM 宏链与 `_rpm_strip_disable`：只读取证

宏链取证在解包期间并行完成，没有读取 R0/BUILD。原文及编号副本为 `E/rpm-macros/`；
R0 内的 `usr/lib/rpm/tizen/macros` 实为 `../tizen_macros` 软链接，两种写法指向同一宏体。

### 3.1 调用链与不适用的全局开关

| R0 内路径:行 | 实际行为 |
| --- | --- |
| `usr/lib/rpm/macros:83` | `%__strip /bin/strip` |
| `usr/lib/rpm/tizen/macros:34–38` | `__strip_install_post` 定义；第 36 行为通用归档 strip |
| `usr/lib/rpm/tizen/macros:40–45` | `__os_install_post`：compress、受 `_rpm_strip_disable` 控制的 strip、python-hardlink、find-docs |
| `usr/lib/rpm/tizen/macros:53–60` | `__spec_install_post`：debug、arch、os、isu、可选 rootstrap 检查 |
| `usr/lib/rpm/brp-strip-static-archive:15–20` | 逐个筛出普通 ar 归档，第 19 行 `$STRIP -g "$f"` |
| `usr/lib/rpm/macros:178` | 定义 `_rpm_strip_disable` 会给 find-debuginfo 增加 `--strip-disable` |
| `usr/lib/rpm/macros:182–199` | debug hook 传入 `_smp_mflags` 与上述 find-debuginfo 选项 |
| `usr/lib/rpm/find-debuginfo.sh:147–148,254–256,492–494` | 处理 `--strip-disable`，令 strip_to_debug 提前退出，另清空 strip_option |
| `usr/lib/rpm/brp-strip:14–20` | 普通 ELF strip 路径，亦受上层全局开关影响 |

原宏体（tizen/macros:34–38）：

```rpm
%__strip_install_post    \
    %{!?__debug_package:%{_rpmconfigdir}/brp-strip %{__strip}} \
    %{_rpmconfigdir}/brp-strip-static-archive %{__strip} \
#    %{_rpmconfigdir}/brp-strip-comment-note %{__strip} %{__objdump} \
%{nil}
```

因此 `_rpm_strip_disable` **不能作为只修归档索引的局部开关**：它除了跳过通用归档 strip，
还影响普通 strip hook 和 debuginfo 提取/strip 行为，不满足“其余后处理不变”。
这来自实际宏/脚本内容，不按上游惯例推断。

### 3.2 宏文件 SHA 与匹配的包 NEVRA

为遵守 R0 的读取白名单，**未读取 R0 rpmdb，也未执行 `rpm --root R0 -q`**。
从固定 Base 快照取 rpm/rpm-build RPM，核对归档 primary.xml 的包 SHA；
用宿主 `rpm -qp` 查询 NEVRA 和逐文件摘要，与 R0 实际宏/脚本内容核对：

| 匹配包 NEVRA | RPM SHA256 |
| --- | --- |
| `rpm-0:4.14.1.1-1.4.x86_64` | `ba3a470c8c560dc9ea5a01145a2c51a40db458c807c5d4606f8f87d78207d996` |
| `rpm-build-0:4.14.1.1-1.4.x86_64` | `722f24fe7d100628cc31918f9860f7f74b1cf70ec17868f51edcfefd57d5d2b2` |

两个请求均 HTTP 200。URL、qf 原始结果、dump、比较值为 `E/macro-package-identity.json`、`rpm-dump.txt`、`rpm-build-dump.txt`。
这是**当前宏内容匹配这些包**的证明，不冒充本轮直接读取的安装数据库 NEVRA。
`macros`、`tizen_macros` 归 rpm；所列 brp/find/check 脚本归 rpm-build。
软链接自身的 RPM digest 为零，按 link target 与目标文件摘要核对，未把零摘要当内容不符。

| R0 内文件 | 实际内容 SHA256 | 类型 |
| --- | --- | --- |
| `usr/lib/rpm/macros` | `f2f13c69904e872a8196011d0f8e3dcc6feee4edf53380418c78ea737b44593a` | 普通文件 |
| `usr/lib/rpm/tizen/macros` | `f0f991bd97f44b7bf906ac4a7a45cd34b7444c1acce2358261e4a95b3e68ebc8` | → ../tizen_macros |
| `usr/lib/rpm/brp-strip-static-archive` | `d40b7c625bf8e1e685f9130c7dbe3e2b9e8a144d2c3a4b52ab4a3c39afee712b` | 普通文件 |
| `usr/lib/rpm/brp-strip` | `2f5edd0a45c8a52329d0be66a1ccca92ad58fffd8e92f6ef7a607b62c06764f0` | 普通文件 |
| `usr/lib/rpm/brp-compress` | `b1e27e6ee93f0116add358dbafdf04913f1f4c6778bc657971d0d08a83bd1385` | 普通文件 |
| `usr/lib/rpm/brp-python-hardlink` | `c56be31851c0f853730d31522b5f94da73bfcf3d106eb72f777431db40e76e35` | 普通文件 |
| `usr/lib/rpm/tizen/find-docs.sh` | `7b5f42406b2913fc4416323f0d8d85b09b6bf4b5f4295835b4dcf2469a6333e7` | 普通文件 |
| `usr/lib/rpm/find-debuginfo.sh` | `bca9df3cb1e55423ff066f07df6121f5af9e211fe596b602dc4ec5829a501ec3` | 普通文件 |
| `usr/lib/rpm/check-buildroot` | `238b0fa185a2b15b488c5e3d9348886d08a40c5293261840167d7a68f7e8b0d2` | 普通文件 |
| `usr/lib/rpm/tizen/find-isufiles.sh` | `96827dd3187b8475b1074219cdb35a38d63ae4920e02b1e753b4e315610a35ca` | 普通文件 |
| `usr/lib/rpm/tizen_macros` | `f0f991bd97f44b7bf906ac4a7a45cd34b7444c1acce2358261e4a95b3e68ebc8` | 普通文件 |

若后续进入完整构建，仍须对新根重核这些文件 SHA/软链接形态；**本轮没有新根宏一致性通过结果**。

## 4. 修法、完整构建与新 RPM 验收：未执行

| 阶段 | 状态与原因 |
| --- | --- |
| spec 重定义 __strip_install_post，仅删除 brp-strip-static-archive | NOT RUN；运行库格式停止条件先触发，原宏未修改，没有“新宏已生效”结论 |
| `%install` 尾段按实际成员格式选择 `/bin/strip -g` 并打印日志 | NOT RUN；不自动将 bitcode libarcher 纳入修复 |
| 相对工作区 spec 的修法 diff、git apply --check | NOT RUN；无归档修法补丁 |
| archive-fix-trial 精确指纹入口及正负测试 | NOT RUN；构建脚本未改，原容量/CMake 门禁不变 |
| 18 GiB、swap 0、4/4/1、debuginfo -j4 的一次完整构建 | 未启动，**0 次**；未占用一次失败构建试验 |
| 新根宏 SHA 与 R0 一致性 | NOT RUN |
| 构建 wall/峰值/磁盘、新 22 RPM inventory、toolchain-archivefix | 不适用；没有新构建产物 |
| 新开发归档完整有序符号→成员映射对本次构建树 | NOT RUN；普查保存的基线索引不代替新包验收 |
| 纯机器码归档无调试节、成员内容对基线、索引完整 | 新包验收 NOT RUN；本轮仅有基线成员/索引普查 |
| 新构建各 brp/find-debuginfo 执行、归档 strip 0 次/格式错误 0 行、安装判别日志一致 | NOT RUN；不能用未启动构建的“零次”当成功 |
| 新/旧解包清单与 SHA 差异完整分类 | NOT RUN |
| core/support、含 lld 组件两组，GNU ld/lld 四次消费者链接/运行 | NOT RUN |
| 替换坏 liblldCOFF.a 后链接失败与映射门禁拒绝 | NOT RUN；本轮只核对坏归档身份，未进行链接负例 |
| 新 clang-22/lld/llvm-ar 的 SHA 可复现性比较 | NOT RUN |

可提交的归档修复补丁路径：**无**；修法补丁 SHA：**不适用**；能否以本轮完整构建验收为依据提交：**否，尚未实现/验证**。
本轮交付的是基线普查、局部修法边界证据和可复用只读检查器，不是已经验证的 spec 修复。

## 5. 下一步与约束自检

当前第一任务保持归档修复，设计 v4/BOLT 暂缓。下一步需要用户明确 **libarcher bitcode 归档的处理范围**；
不能继续沿用“compiler-rt 与 libarcher 都是纯机器码”的假设。
S、Rnew 保留；S 仍只有原有三处并发改动，Rnew 尚未初始化。后续执行前须重新取得独占锁。

| 自检 | 结果 |
| --- | --- |
| 先读 STATUS/docs/25，主仓库起点干净，独占检查通过 | 是 |
| R0 只读 RPMS 与 usr/lib/rpm；不读 BUILD/rpmdb，不用旧 TC，不碰旧混合根 | 是 |
| 22 RPM SHA、坏 liblldCOFF.a SHA、完整普查 | PASS；格式门禁因 libarcher bitcode FAIL |
| 是否修改工作区 W/llvm、原 spec、试验 spec 或 docs/25 | 否 |
| 是否启动完整构建、BOLT、性能校准、Chromium 或推 Gerrit | 否 |
| 是否失败后修改修法重试 | 否；尚无修法 |
| 是否把运行库格式失败当作全局根污染 | 否；本轮 RPM 身份全部匹配 |
| 锁是否回收、文档与 STATUS 是否同提交 | 是；锁/保护证据见 final-cleanup.json，本提交定位用 git log |

## 附录 A：全部 270 个唯一归档的普查表

路径相对 H；所属 RPM 可重复。BC=bitcode，ELF=机器码，Other=其他格式；最后一列只比较**机器码外部定义集合**，不宣称 bitcode 索引完整。
每个归档的完整成员 SHA/序号/同名次数/有序索引 JSON 均在 E/census/archives 下，本文不复制大量符号名。

| 路径 | 所属 RPM | 成员 | BC | ELF | Other | thin | 索引条目 | 恰为 ELF 符号 |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: | --- |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.asan-preinit-x86_64.a` | compiler-rt | 1 | 0 | 1 | 0 | NO | 0 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.asan-x86_64.a` | compiler-rt | 125 | 0 | 125 | 0 | NO | 5450 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.asan_cxx-x86_64.a` | compiler-rt | 1 | 0 | 1 | 0 | NO | 21 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.asan_static-x86_64.a` | compiler-rt | 2 | 0 | 2 | 0 | NO | 140 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.builtins-x86_64.a` | compiler-rt | 173 | 0 | 173 | 0 | NO | 195 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.cfi-x86_64.a` | compiler-rt | 58 | 0 | 58 | 0 | NO | 1122 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.cfi_diag-x86_64.a` | compiler-rt | 90 | 0 | 90 | 0 | NO | 1502 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.ctx_profile-x86_64.a` | compiler-rt | 76 | 0 | 76 | 0 | NO | 1406 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.dd-x86_64.a` | compiler-rt | 59 | 0 | 59 | 0 | NO | 1239 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.dfsan-x86_64.a` | compiler-rt | 86 | 0 | 86 | 0 | NO | 1737 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.fuzzer-x86_64.a` | compiler-rt | 25 | 0 | 25 | 0 | NO | 459 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.fuzzer_interceptors-x86_64.a` | compiler-rt | 1 | 0 | 1 | 0 | NO | 18 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.fuzzer_no_main-x86_64.a` | compiler-rt | 24 | 0 | 24 | 0 | NO | 458 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.gwp_asan-x86_64.a` | compiler-rt | 8 | 0 | 8 | 0 | NO | 60 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.hwasan-preinit-x86_64.a` | compiler-rt | 1 | 0 | 1 | 0 | NO | 0 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.hwasan-x86_64.a` | compiler-rt | 111 | 0 | 111 | 0 | NO | 2659 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.hwasan_aliases-x86_64.a` | compiler-rt | 111 | 0 | 111 | 0 | NO | 2659 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.hwasan_aliases_cxx-x86_64.a` | compiler-rt | 1 | 0 | 1 | 0 | NO | 22 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.hwasan_cxx-x86_64.a` | compiler-rt | 1 | 0 | 1 | 0 | NO | 22 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.lsan-x86_64.a` | compiler-rt | 97 | 0 | 97 | 0 | NO | 1752 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.memprof-preinit-x86_64.a` | compiler-rt | 1 | 0 | 1 | 0 | NO | 0 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.memprof-x86_64.a` | compiler-rt | 99 | 0 | 99 | 0 | NO | 4753 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.memprof_cxx-x86_64.a` | compiler-rt | 1 | 0 | 1 | 0 | NO | 20 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.msan-x86_64.a` | compiler-rt | 98 | 0 | 98 | 0 | NO | 5758 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.msan_cxx-x86_64.a` | compiler-rt | 1 | 0 | 1 | 0 | NO | 20 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.nsan-x86_64.a` | compiler-rt | 99 | 0 | 99 | 0 | NO | 1785 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.profile-x86_64.a` | compiler-rt | 19 | 0 | 19 | 0 | NO | 140 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.rtsan-x86_64.a` | compiler-rt | 91 | 0 | 91 | 0 | NO | 2234 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.safestack-x86_64.a` | compiler-rt | 6 | 0 | 6 | 0 | NO | 16 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.scudo_standalone-x86_64.a` | compiler-rt | 28 | 0 | 28 | 0 | NO | 277 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.scudo_standalone_cxx-x86_64.a` | compiler-rt | 1 | 0 | 1 | 0 | NO | 74 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.stats-x86_64.a` | compiler-rt | 75 | 0 | 75 | 0 | NO | 1336 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.stats_client-x86_64.a` | compiler-rt | 1 | 0 | 1 | 0 | NO | 2 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.tsan-x86_64.a` | compiler-rt | 120 | 0 | 120 | 0 | NO | 5748 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.tsan_cxx-x86_64.a` | compiler-rt | 1 | 0 | 1 | 0 | NO | 21 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.tysan-x86_64.a` | compiler-rt | 91 | 0 | 91 | 0 | NO | 1555 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.ubsan_minimal-x86_64.a` | compiler-rt | 1 | 0 | 1 | 0 | NO | 76 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.ubsan_standalone-x86_64.a` | compiler-rt | 93 | 0 | 93 | 0 | NO | 1484 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.ubsan_standalone_cxx-x86_64.a` | compiler-rt | 4 | 0 | 4 | 0 | NO | 8 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.xray-basic-x86_64.a` | compiler-rt | 2 | 0 | 2 | 0 | NO | 21 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.xray-dso-x86_64.a` | compiler-rt | 2 | 0 | 2 | 0 | NO | 6 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.xray-fdr-x86_64.a` | compiler-rt | 2 | 0 | 2 | 0 | NO | 36 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.xray-profiling-x86_64.a` | compiler-rt | 3 | 0 | 3 | 0 | NO | 61 | YES |
| `/usr/lib64/clang/22/lib/linux/libclang_rt.xray-x86_64.a` | compiler-rt | 60 | 0 | 60 | 0 | NO | 1199 | YES |
| `/usr/lib64/clang/22/lib/linux/liborc_rt-x86_64.a` | compiler-rt | 14 | 0 | 14 | 0 | NO | 143 | YES |
| `/usr/lib64/libLLVMAArch64AsmParser.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMAArch64CodeGen.a` | llvm-static-devel | 63 | 63 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMAArch64Desc.a` | llvm-static-devel | 12 | 12 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMAArch64Disassembler.a` | llvm-static-devel | 2 | 2 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMAArch64Info.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMAArch64Utils.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMABI.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMARMAsmParser.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMARMCodeGen.a` | llvm-static-devel | 49 | 49 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMARMDesc.a` | llvm-static-devel | 13 | 13 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMARMDisassembler.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMARMInfo.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMARMUtils.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMAggressiveInstCombine.a` | llvm-static-devel | 2 | 2 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMAnalysis.a` | llvm-static-devel | 131 | 125 | 6 | 0 | NO | 82 | YES |
| `/usr/lib64/libLLVMAsmParser.a` | llvm-static-devel | 4 | 4 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMAsmPrinter.a` | llvm-static-devel | 27 | 27 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMBPFAsmParser.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMBPFCodeGen.a` | llvm-static-devel | 26 | 26 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMBPFDesc.a` | llvm-static-devel | 5 | 5 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMBPFDisassembler.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMBPFInfo.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMBinaryFormat.a` | llvm-static-devel | 14 | 14 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMBitReader.a` | llvm-static-devel | 5 | 5 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMBitWriter.a` | llvm-static-devel | 4 | 4 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMBitstreamReader.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMCAS.a` | llvm-static-devel | 15 | 15 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMCFGuard.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMCFIVerify.a` | llvm-static-devel | 2 | 2 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMCGData.a` | llvm-static-devel | 7 | 7 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMCodeGen.a` | llvm-static-devel | 238 | 237 | 1 | 0 | NO | 1 | YES |
| `/usr/lib64/libLLVMCodeGenTypes.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMCore.a` | llvm-static-devel | 80 | 80 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMCoroutines.a` | llvm-static-devel | 11 | 11 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMCoverage.a` | llvm-static-devel | 3 | 3 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMDTLTO.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMDWARFCFIChecker.a` | llvm-static-devel | 4 | 4 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMDWARFLinker.a` | llvm-static-devel | 2 | 2 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMDWARFLinkerClassic.a` | llvm-static-devel | 4 | 4 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMDWARFLinkerParallel.a` | llvm-static-devel | 11 | 11 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMDWP.a` | llvm-static-devel | 2 | 2 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMDebugInfoBTF.a` | llvm-static-devel | 2 | 2 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMDebugInfoCodeView.a` | llvm-static-devel | 40 | 40 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMDebugInfoDWARF.a` | llvm-static-devel | 29 | 29 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMDebugInfoDWARFLowLevel.a` | llvm-static-devel | 3 | 3 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMDebugInfoGSYM.a` | llvm-static-devel | 14 | 14 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMDebugInfoLogicalView.a` | llvm-static-devel | 19 | 19 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMDebugInfoMSF.a` | llvm-static-devel | 4 | 4 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMDebugInfoPDB.a` | llvm-static-devel | 93 | 93 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMDebuginfod.a` | llvm-static-devel | 4 | 4 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMDemangle.a` | llvm-static-devel | 6 | 6 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMDiff.a` | llvm-static-devel | 3 | 3 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMDlltoolDriver.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMExecutionEngine.a` | llvm-static-devel | 5 | 5 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMExegesis.a` | llvm-static-devel | 25 | 25 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMExegesisAArch64.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMExegesisX86.a` | llvm-static-devel | 2 | 2 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMExtensions.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMFileCheck.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMFrontendAtomic.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMFrontendDirective.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMFrontendDriver.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMFrontendHLSL.a` | llvm-static-devel | 6 | 6 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMFrontendOffloading.a` | llvm-static-devel | 3 | 3 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMFrontendOpenACC.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMFrontendOpenMP.a` | llvm-static-devel | 4 | 4 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMFuzzMutate.a` | llvm-static-devel | 4 | 4 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMFuzzerCLI.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMGlobalISel.a` | llvm-static-devel | 30 | 30 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMHipStdPar.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMIRPrinter.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMIRReader.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMInstCombine.a` | llvm-static-devel | 15 | 15 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMInstrumentation.a` | llvm-static-devel | 28 | 28 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMInterfaceStub.a` | llvm-static-devel | 3 | 3 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMInterpreter.a` | llvm-static-devel | 3 | 3 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMJITLink.a` | llvm-static-devel | 35 | 35 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMLTO.a` | llvm-static-devel | 6 | 6 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMLibDriver.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMLineEditor.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMLinker.a` | llvm-static-devel | 2 | 2 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMMC.a` | llvm-static-devel | 70 | 70 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMMCA.a` | llvm-static-devel | 24 | 24 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMMCDisassembler.a` | llvm-static-devel | 5 | 5 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMMCJIT.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMMCParser.a` | llvm-static-devel | 13 | 13 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMMIRParser.a` | llvm-static-devel | 3 | 3 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMObjCARCOpts.a` | llvm-static-devel | 8 | 8 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMObjCopy.a` | llvm-static-devel | 26 | 26 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMObject.a` | llvm-static-devel | 36 | 36 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMObjectYAML.a` | llvm-static-devel | 29 | 29 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMOptDriver.a` | llvm-static-devel | 2 | 2 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMOption.a` | llvm-static-devel | 4 | 4 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMOrcDebugging.a` | llvm-static-devel | 7 | 7 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMOrcJIT.a` | llvm-static-devel | 57 | 57 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMOrcShared.a` | llvm-static-devel | 7 | 7 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMOrcTargetProcess.a` | llvm-static-devel | 15 | 15 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMPasses.a` | llvm-static-devel | 6 | 6 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMPlugins.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMProfileData.a` | llvm-static-devel | 21 | 21 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMRemarks.a` | llvm-static-devel | 11 | 11 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMRuntimeDyld.a` | llvm-static-devel | 8 | 8 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMSandboxIR.a` | llvm-static-devel | 15 | 15 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMScalarOpts.a` | llvm-static-devel | 81 | 81 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMSelectionDAG.a` | llvm-static-devel | 26 | 26 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMSupport.a` | llvm-static-devel | 179 | 175 | 4 | 0 | NO | 22 | YES |
| `/usr/lib64/libLLVMSupportLSP.a` | llvm-static-devel | 3 | 3 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMSymbolize.a` | llvm-static-devel | 5 | 5 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMTableGen.a` | llvm-static-devel | 14 | 14 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMTableGenBasic.a` | llvm-static-devel | 13 | 13 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMTableGenCommon.a` | llvm-static-devel | 23 | 23 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMTarget.a` | llvm-static-devel | 5 | 5 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMTargetParser.a` | llvm-static-devel | 15 | 15 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMTelemetry.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMTextAPI.a` | llvm-static-devel | 15 | 15 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMTextAPIBinaryReader.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMTransformUtils.a` | llvm-static-devel | 94 | 94 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMVectorize.a` | llvm-static-devel | 33 | 33 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMWindowsDriver.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMWindowsManifest.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMX86AsmParser.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMX86CodeGen.a` | llvm-static-devel | 66 | 66 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMX86Desc.a` | llvm-static-devel | 16 | 16 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMX86Disassembler.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMX86Info.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMX86TargetMCA.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMXRay.a` | llvm-static-devel | 14 | 14 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libLLVMipo.a` | llvm-static-devel | 45 | 45 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libarcher_static.a` | libomp-devel, llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangAPINotes.a` | llvm-static-devel | 5 | 5 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangAST.a` | llvm-static-devel | 114 | 114 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangASTMatchers.a` | llvm-static-devel | 3 | 3 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangAnalysis.a` | llvm-static-devel | 31 | 31 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangAnalysisFlowSensitive.a` | llvm-static-devel | 18 | 18 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangAnalysisFlowSensitiveModels.a` | llvm-static-devel | 3 | 3 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangAnalysisLifetimeSafety.a` | llvm-static-devel | 10 | 10 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangAnalysisScalable.a` | llvm-static-devel | 4 | 4 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangApplyReplacements.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangBasic.a` | llvm-static-devel | 73 | 73 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangChangeNamespace.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangCodeGen.a` | llvm-static-devel | 101 | 101 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangCrossTU.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangDaemon.a` | llvm-static-devel | 82 | 82 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangDaemonTweaks.a` | llvm-static-devel | 20 | 20 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangDependencyScanning.a` | llvm-static-devel | 7 | 7 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangDirectoryWatcher.a` | llvm-static-devel | 2 | 2 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangDoc.a` | llvm-static-devel | 11 | 11 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangDocSupport.a` | llvm-static-devel | 2 | 2 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangDriver.a` | llvm-static-devel | 76 | 76 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangDynamicASTMatchers.a` | llvm-static-devel | 5 | 5 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangEdit.a` | llvm-static-devel | 3 | 3 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangExtractAPI.a` | llvm-static-devel | 6 | 6 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangFormat.a` | llvm-static-devel | 23 | 23 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangFrontend.a` | llvm-static-devel | 32 | 32 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangFrontendTool.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangHandleCXX.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangHandleLLVM.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangIncludeCleaner.a` | llvm-static-devel | 8 | 8 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangIncludeFixer.a` | llvm-static-devel | 6 | 6 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangIncludeFixerPlugin.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangIndex.a` | llvm-static-devel | 9 | 9 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangIndexSerialization.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangInstallAPI.a` | llvm-static-devel | 8 | 8 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangInterpreter.a` | llvm-static-devel | 10 | 10 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangLex.a` | llvm-static-devel | 25 | 25 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangMove.a` | llvm-static-devel | 2 | 2 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangOptions.a` | llvm-static-devel | 2 | 2 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangParse.a` | llvm-static-devel | 18 | 18 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangQuery.a` | llvm-static-devel | 2 | 2 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangReorderFields.a` | llvm-static-devel | 2 | 2 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangRewrite.a` | llvm-static-devel | 3 | 3 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangRewriteFrontend.a` | llvm-static-devel | 8 | 8 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangSema.a` | llvm-static-devel | 86 | 86 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangSerialization.a` | llvm-static-devel | 17 | 17 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangStaticAnalyzerCheckers.a` | llvm-static-devel | 134 | 134 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangStaticAnalyzerCore.a` | llvm-static-devel | 49 | 49 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangStaticAnalyzerFrontend.a` | llvm-static-devel | 7 | 7 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangSupport.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidy.a` | llvm-static-devel | 9 | 9 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyAbseilModule.a` | llvm-static-devel | 22 | 22 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyAlteraModule.a` | llvm-static-devel | 6 | 6 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyAndroidModule.a` | llvm-static-devel | 17 | 17 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyBoostModule.a` | llvm-static-devel | 3 | 3 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyBugproneModule.a` | llvm-static-devel | 105 | 105 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyCERTModule.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyConcurrencyModule.a` | llvm-static-devel | 3 | 3 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyCppCoreGuidelinesModule.a` | llvm-static-devel | 32 | 32 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyCustomModule.a` | llvm-static-devel | 2 | 2 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyDarwinModule.a` | llvm-static-devel | 3 | 3 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyFuchsiaModule.a` | llvm-static-devel | 8 | 8 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyGoogleModule.a` | llvm-static-devel | 16 | 16 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyHICPPModule.a` | llvm-static-devel | 6 | 6 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyLLVMLibcModule.a` | llvm-static-devel | 5 | 5 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyLLVMModule.a` | llvm-static-devel | 9 | 9 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyLinuxKernelModule.a` | llvm-static-devel | 2 | 2 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyMPIModule.a` | llvm-static-devel | 3 | 3 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyMain.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyMiscModule.a` | llvm-static-devel | 28 | 28 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyModernizeModule.a` | llvm-static-devel | 50 | 50 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyObjCModule.a` | llvm-static-devel | 10 | 10 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyOpenMPModule.a` | llvm-static-devel | 3 | 3 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyPerformanceModule.a` | llvm-static-devel | 21 | 21 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyPlugin.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyPortabilityModule.a` | llvm-static-devel | 6 | 6 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyReadabilityModule.a` | llvm-static-devel | 59 | 59 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyUtils.a` | llvm-static-devel | 23 | 23 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTidyZirconModule.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTooling.a` | llvm-static-devel | 17 | 17 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangToolingASTDiff.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangToolingCore.a` | llvm-static-devel | 2 | 2 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangToolingInclusions.a` | llvm-static-devel | 3 | 3 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangToolingInclusionsStdlib.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangToolingRefactoring.a` | llvm-static-devel | 12 | 12 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangToolingSyntax.a` | llvm-static-devel | 8 | 8 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangTransformer.a` | llvm-static-devel | 7 | 7 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangdMain.a` | llvm-static-devel | 2 | 2 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangdRemoteIndex.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libclangdSupport.a` | llvm-static-devel | 16 | 16 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/libfindAllSymbols.a` | llvm-static-devel | 8 | 8 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/liblldCOFF.a` | llvm-static-devel | 18 | 18 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/liblldCommon.a` | llvm-static-devel | 13 | 13 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/liblldELF.a` | llvm-static-devel | 41 | 41 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/liblldMachO.a` | llvm-static-devel | 30 | 30 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/liblldMinGW.a` | llvm-static-devel | 1 | 1 | 0 | 0 | NO | 0 | YES |
| `/usr/lib64/liblldWasm.a` | llvm-static-devel | 14 | 14 | 0 | 0 | NO | 0 | YES |

## 附录 B：原始证据索引

E 下包括：

- `exclusive-precheck.json`、`source-precheck.json`、`lock-acquired.json`、`lock-released.json`、`preservation-check.json`、`final-cleanup.json`。
- `rpm-baseline-check.json`、`baseline-extract.log`、`baseline-extraction-status.json`、`baseline-file-owners.json`、22 份 `*-file-metadata.tsv`、`bad-archive-identity.json`。
- `census-command.json`、`census.log`、`census/census.json`、`census/archives/`、`census-summary.json`、`runtime-blocker-raw.json`。
- `rpm-macros/`、`rpm-macro-manifest.json`、`macro-package-identity.json`、`rpm-provider-candidates.json`、两份 RPM dump 与下载 RPM。
- `archive-parser-tests.log`，检查器/普查脚本的源码在 tools/ 随本次提交；只读解包/下载入口留在 `extract_baseline.py`、`identify_rpm_macros.py`。

所有大文件/原始输出均在 temp/，没有将解包内容或 RPM 上传仓库。
