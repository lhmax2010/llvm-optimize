# 24 归档索引修法与混合 clang profile 适用性：完整性门禁停止报告

日期：2026-09-23，时区 +08:00。起点提交：`dab197cd9d2d5ec4c7f6bb70c70bed6d27466dad`。

**本轮在第零步停止：22 个 RPM 的 SHA256 全部不同于 docs/22 inventory，ThinLTO cache 的文件数与总字节也不同于已登记值。**
另查明 `R/home/abuild/rpmbuild/SOURCES/llvm.spec` 已不同于 docs/22 导出副本，差异全文见 §2.5。
按用户“任一项不符即停止并报告，不修复”的要求，没有恢复资产、替换参考值或启动后续实验。

因此，本轮**不能确认归档修法已满足独立修复提交 Gerrit 的验收条件，也不能确认 profile v2 可绑定混合 clang**。
这是前置资产不匹配导致未测，不能解读为修法或 profile 已被技术实验证伪。
没有执行 `%install`、重链、BOLT 或 30 TU；未进行任何实验重试。

本报告与 STATUS 同提交更新，docs/23 保留不动。另一会话的未提交成功声明不作为本轮证据。

## 0. 路径、参考基准与证据边界

| 别名 | 本机实际路径 |
| --- | --- |
| W | `/home/linhao/Toolchain/development/llvm-optimize` |
| R | `W/temp/gbs-root-x86_64-hybrid-trial/local/BUILD-ROOTS/scratch.x86_64.0` |
| B | `R/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build` |
| H | `W/temp/toolchain-hybrid-trial`，本轮未使用其内容进行验收 |
| H22 | `W/temp/hybrid-trial-20260922`，docs/22 所引原始记录 |
| E | `/home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-verification-20260923-173328`，本轮独立证据 |
| F | `/home/linhao/Toolchain/development/llvm-optimize/temp/foreign-artifacts/20260923-173328`，外来工作内容备份/隔离 |

`temp/` 仅在本机保留，不上传 GitHub。以下 E 中的实际测量由本会话重新执行；旧记录只提供比较基准：

- [docs/22 §4–§5](22_hybrid_link_trial.md)：构建 ELF 体积、RPM inventory、三归档索引基准；RPM 参考为 `H22/products/rpm-inventory.json`。
- SOURCES spec 参考为 `H22/exported.spec`，对应 docs/22 §1 的导出记录。
- cache 参考为**已提交的** `dab197c:docs/23` §2 所引 `temp/archive-profile-rebind-20260923/preflight.json`：12469 文件、20363360960 B。
- docs/22 **没有记录构建树 clang 的 SHA**；本轮读取的是已提交 `dab197c:docs/23` §0 所引 `temp/archive-profile-rebind-20260923/protected-before.json` 中的该项 SHA。不能把 docs/22 的剥离后 RPM clang SHA 当构建树 SHA。
- 进入时工作区 docs/23、STATUS 和一个脚本已有未提交修改。先保存完整副本与 diff，再核对 Git 已提交版本；没有采用外来未提交报告作为验收证据。具体见 §3。

## 1. 独占核查与锁：PASS，已回收

在 `/proc` 检查相关进程的命令行、cwd、root、exe，筛查 rpmbuild、gbs、ninja、lld/ld.lld、llvm-bolt 及编译器，并检查 `R/home/abuild` 已有锁。
`E/exclusivity-before.json` 原始结果：

```json
{"processes": [], "blocking": [], "existing_locks": []}
```

本会话以 `O_CREAT|O_EXCL` 原子创建 `R/home/abuild/.llvm-optimize-exclusive.lock`（0600），未覆盖他人锁。
`E/lock-acquired.json` 记录：

```text
session=archive-fix-verification-3acf2ceecd3a468f9b526745e822b84a
pid=1529248
started=2026-09-23T17:34:14.238518+08:00
proc_start_ticks=18073315
```

资产检查期间持有该锁。停止后，锁持有进程在 finally 中核对归属再删除；进程退出 0，已回收。
`E/lock-released.json` 原始结果：

```json
{"removed": true, "pid": 1529248, "ended": "2026-09-23T17:39:03.689150+08:00"}
```

这里证明的是本次扫描与锁生命周期，不宣称已从操作系统层面禁止所有不遵守锁的外部写入。
未启动构建/实验 scope 或采样器，因此没有此类后台进程需要回收。

## 2. 共享资产逐项核查：FAIL

实际测量窗口为 `2026-09-23T17:36:42.814835+08:00` 至 `17:37:05.224168+08:00`。
`E/check_assets.py` 串行读取资产；SHA 用 `hashlib.file_digest(..., 'sha256')`，体积用 stat，cache 逐文件枚举并累计字节。
完整结果为 `E/assets.json`，控制台为 `E/assets-console.log`。完成第零步这批只读差异取证后停止，未进入依赖它的 Ninja dry-run 或实验。

### 2.1 构建树 clang：体积与可获得的历史 SHA 均匹配

```text
B/bin/clang-22
bytes: 1793477112
SHA256: e88efed89d7cf67b55fe1bdfd067eea5384869f8ed65882f86386f7f3fc42455
```

体积匹配 docs/22；SHA 匹配已提交 docs/23 所引保护记录。docs/22 缺该 SHA 的限制如 §0，不补造证据。
来源：`E/assets.json` 的 `checks.clang`。这一个 ELF 匹配不能覆盖其他资产失败。

### 2.2 原路径上的 22 个 RPM：0/22 匹配

包文件均位于 `R/home/abuild/rpmbuild/RPMS/x86_64/`，文件名为下表包名加 `-22.1.8-1.x86_64.rpm`。
预期值来自 docs/22 inventory，当前值由本会话对 inventory 记录的原路径直接读取；全部路径、当前字节数与 SHA 见 `E/assets.json` 的 `checks.rpms`。

| 包名 | docs/22 SHA256 | 当前 SHA256 | 结果 |
| --- | --- | --- | --- |
| `clang` | `a4f72546583a562f8e9b25aa1965d91ac7fa7958ac3f0939cbd5b0382abb016d` | `1e29bc9c34b5c194774a594cb48cd7447d3cdf685ef0a593333bd28207ac76bb` | FAIL |
| `clang-debuginfo` | `bab3c5911ee0b01d978a217fd03f6f18008ef0bc7cbcd501282c242c0fe9afc6` | `d2dc58a66772ff865e1acd54b0afa222c338fbfa0f3b152babb8f4788c006866` | FAIL |
| `clang-devel` | `2ed9382b5cc12a56c623d654806a1b5b78f7dd3dfbac45d5e3f74a9ef0b3d895` | `19fa5f9e824c082b80147fe3441c8eb6f2280b1393f80f4eb54837edae62d595` | FAIL |
| `clang-devel-debuginfo` | `a585746381e7e9536020065107652db684532371148d9abaaf1cb37ec65d02e3` | `d4b3092f624d3996bb73e4705783aec6d7dc1fcff3fb0fac0e44c6ebffb0a326` | FAIL |
| `compiler-rt` | `ae4098d95e67d1b71db49017e88029b162aad020aaec3e668604736e7277dd2d` | `ebd2dfe093b469d431fc0ce04dad2eb2cb005778863f059252e39810a722742d` | FAIL |
| `compiler-rt-debuginfo` | `9efae376b2c18ffbe1533673e0f51a98d87f3a27dc1d1976b38874074d22c63c` | `3465e4fa4ed9ea633dadcc6fd0510187d71d8f95061edc266e681d8d64dd57a7` | FAIL |
| `libllvm` | `fc2d62109cfec9f221b87a44ba7d74902efda37db2a0f5b1a568e1cd2374e98e` | `12a715098ab5e87bfc55544cb9a0e379d13e974821cff0469a5a367b50aa4332` | FAIL |
| `libllvm-debuginfo` | `1ee5300bf1deb2ad27ee0bedc21c68538f3d8d3ced515679a7cacfd755344f1d` | `de3e7f9b6df304fa10d4575fffa9e2e8d5f770d525adc45513b56cfea6f9396a` | FAIL |
| `libomp` | `8db0f5481637fe912cdd0bf36b28828f20f960f4cfc231afafe34a1f394397d8` | `df057d633a9925409aba0a06a168d1e10f9d32d71e10ed79b66ad3a835665ccb` | FAIL |
| `libomp-debuginfo` | `2b299a4a9481ea6d611583d9e3f65981176341fb21454709c23a38beba950086` | `b1796cb63043da1e79bc5d6aaedad86e4b4ca9e0db948c11167cf17d845cb561` | FAIL |
| `libomp-devel` | `79d6c5501378cda844da1824a80a02a98ad450862cd871a46d8e753fc9123bc8` | `b26edca894c09fc6d640a4df07a1bf8b0703a7b409e9d2d49ce77a70c2ee0959` | FAIL |
| `lldb` | `85383eedf017e444544e003d26c5649a6c33514f23a971ba4ad2044fe9c98217` | `fb31022d6e6b6dc009e95d13bd20d174fccc166c3104b34d0c5ae57c9cf316a5` | FAIL |
| `lldb-debuginfo` | `519f33767805d69ee526c3a7a5bea0a41b0d83aae19a271c96d8c952adbb66f2` | `813fed42892c291e3a54a3174414baedbf030d90ed4c231d5a4cf5bec798622e` | FAIL |
| `lldb-devel` | `c04ab145c72d3350c980acad5c37587683b5a9159c1d5e19827a9ce33a3e37e4` | `5237461ea1c019116a42cf66045ac1be9779525f39fc7d41e9558195b7a25908` | FAIL |
| `lldb-devel-debuginfo` | `0bccfac8387d50d8fbb387640545cd9a9cddfea041d1144881e4368a506089d1` | `fd628af2af30867a185f7845db7f9cb6bb774cfcf8a0f9068dab608cbe012bc7` | FAIL |
| `llvm` | `4baff036cac23ecef9f18c71b7b959a4ff27b46cd47049209368465e1657f8f8` | `b0dd5421b39846cc6f4bc8374a2c0ab27caee2afeb8b3252240ec1a47ce051c9` | FAIL |
| `llvm-debuginfo` | `28359d0974110a595d06c5965f23a9ef086fb48b2677fc72554ec6167f9abbf6` | `626c5aefc3170b84e813aeda17780608632b589bb78bb04ab377d22244f6702b` | FAIL |
| `llvm-debugsource` | `ee24857baba026105cc5717f96b5b4f9139df634a27ec69e1cc5ddfe79f31076` | `f036fafbf8acb7dfe26cb2c90760a2041a47ed38d37c2bb078f5c1b67e6cbaca` | FAIL |
| `llvm-devel` | `5cc932473b75536d69afc76661f80c16379ce721976a6846241ab33a22944174` | `6d9dc3df1ed6cf13a0b01c8d5045612bacc0c77c0c984704b1e9ed3d938fe896` | FAIL |
| `llvm-devel-debuginfo` | `18bb318c7facc0c33ad999c9c6d79e1dc899458ba34c7ae23a0b56e975f2e46c` | `939b25fb847d4190357e16ec2ebeab1db9eca77ac2a64e3a7482db65d3acb290` | FAIL |
| `llvm-static-devel` | `710a691623e710019913d1049131c288a8edff3ad2f0c0799c4c30eb5969957d` | `78dd1e8fc757fb6676555793939046f68f82d990a81d2bf782c183b38d433eee` | FAIL |
| `python-clang` | `d63669137a32938d492a33cc85735198a502d0a996189e99382c555975253e74` | `3a754fcdf271c0af3c68d49733a3d7007abd038fe5ad6b30aa38ab142b9131c1` | FAIL |

**这里只证明 RPM 文件字节身份不符。** RPM 头部变化也会改变 SHA；本轮未重新解包比较 payload，不能据此声称 22 包的内容全部被改坏，也不能猜测谁在何时改写。
没有切换到其他会话的 RPM 备份，未恢复或覆盖这些文件。

### 2.3 三个关键开发归档的 Archive map 条目数：PASS

| B/lib64 下的归档 | 预期条目数 | 实测条目数 | llvm-nm 退出码 | 结果 |
| --- | ---: | ---: | ---: | --- |
| `libLLVMAnalysis.a` | 9445 | 9445 | 0 | PASS |
| `libLLVMCodeGen.a` | 14276 | 14276 | 0 | PASS |
| `libLLVMSupport.a` | 5023 | 5023 | 0 | PASS |

实际命令模板（展开后的三条完整 argv 见 `E/asset-commands.json`）：

```bash
nice -n 15 ionice -c3 taskset -c 2 \
  prlimit --as=4294967296 --core=0 -- \
  /lib64/ld-linux-x86-64.so.2 \
  "$W/temp/toolchain-baseline/usr/bin/llvm-nm" --print-armap \
  "$B/lib64/libLLVMAnalysis.a"
```

另两条只换归档名，逐条 180 秒超时。只统计输出的 `Archive map` 段，不混入成员符号列表。
原始 stdout/stderr 保存在 `E/libLLVM{Analysis,CodeGen,Support}.a-armap.{stdout,stderr}`。
这只是用户第零步要求的三项计数核查，**不是 226 个开发归档普查，也不是完整符号→成员映射相等的证明**。

### 2.4 ThinLTO cache：FAIL

| 项目 | 已登记值 | 本轮实测 | 差值 |
| --- | ---: | ---: | ---: |
| 文件数 | 12469 | 12471 | +2 |
| 总字节 | 20363360960 | 20363368128 | +7168 |

来源：`E/assets.json` 的 `checks.cache`；本轮完整文件路径、字节和 mtime_ns 清单为 `E/cache-files.json`。
没有清理、裁剪或改写 cache，也没有修改 cache 参数。仅凭总量差不能推出具体哪次操作造成变化。

### 2.5 SOURCES/llvm.spec：不同，未恢复、未执行

```text
docs/22 导出参考 SHA256:
685e569071c13541e9025c3dc03627b4176bea98653fb44c0dd8e0a0ee10ec1e
当前 R/home/abuild/rpmbuild/SOURCES/llvm.spec SHA256:
d31ffae18a0b8804972a92e5817de2fcff58832d880186e34f7369c52469c261
```

`E/sources-spec.current` 是当前文件只读快照，`E/sources-spec.diff` 完整差异如下。
该 diff 是**现场已有变化的证据，不是本轮实施的补丁，也不是本轮认证后的修法**：

```diff
--- docs22/exported.spec
+++ R/SOURCES/llvm.spec-current
@@ -55,6 +55,16 @@
 
 %{!?mlgo_build_jobs: %define mlgo_build_jobs 4}
 %{!?mlgo_verify_configure_only: %define mlgo_verify_configure_only 0}
+# brp-strip-static-archive (tizen_macros:36 -> brp script :19 `strip -g`)
+# rewrites ThinLTO bitcode archive symbol tables with only the native
+# members it can read, dropping every bitcode symbol from the index.
+# Redefine __strip_install_post (tizen_macros:34-38) minus that line;
+# _rpm_strip_disable is NOT usable (macros:178 would pass --strip-disable
+# to find-debuginfo and change every ELF).
+%define __strip_install_post \
+    %{!?__debug_package:%{_rpmconfigdir}/brp-strip %{__strip}} \
+%{nil}
+
 
 BuildRequires: cmake
 BuildRequires: python3
```

可确认当前文件比 docs/22 多出局部重定义 `__strip_install_post` 的内容；不能据此确认操作者或执行时间。
没有恢复它，也没有用它执行任何 rpmbuild。本轮另有 RPM 与 cache 两项明确的完整性阻塞，是否仅将此项作为报告项不影响停止结论。

### 2.6 Ninja“无待办”：NOT RUN

按完整性先决条件失败即停止，本轮没有在 B 执行 Ninja dry-run。
**B 是否存在待编译/待链接任务为 UNKNOWN**，不能沿用另一会话的结果补 PASS。

## 3. 工作树与外来文件处理

`E/initial-state.json` 记录进入时 `git status --short`：

```text
 M docs/23_archive_fix_and_profile_rebind.md
 M docs/STATUS.md
 M tools/relink_clang_for_bolt.py
?? tools/repack_static_archive_fix.py
```

按用户要求，未跟踪脚本记录 SHA 后移至 `F/tools/repack_static_archive_fix.py`：

```text
bytes=8747
SHA256=e180da20bcb995e748f331de664e458cae495b5a2f595e24932856d7cd2464bd
```

未执行、未提交该脚本。已有跟踪文件修改完整保存至 `F/tracked-working-copies/`，初始 binary diff 保存至 `F/initial-working.diff`；E/initial 下另有备份。
工作区 docs/23 与 `tools/relink_clang_for_bolt.py` **原样保留，不纳入本次提交**。进入时 SHA 为：

| 文件 | 进入时 SHA256（收尾复核必须相同） |
| --- | --- |
| docs/23_archive_fix_and_profile_rebind.md | `aa44933696d679759a098d1e9dbfcaf730759190ca92c0df40a999cf266d2028` |
| tools/relink_clang_for_bolt.py | `683e88c98a05d75edc6b3d1cc517b181f4b8e837c05c6f9c09c4766723f4acc6` |

原 STATUS 工作副本也先保存，SHA 为 `967201443e839a853304625b34324c2c32189e5a37f6e8b0099df76b88f5f458`。
本次 STATUS 更新以 **Git 已提交 `dab197c` 版本**加本会话实测为基础，不把外来未提交的成功声明变成本次验证结论。
这不删除其取证副本。详见 `E/foreign-artifacts.json`、`E/committed/docs/` 和收尾的 `E/preservation-check.json`。

本次只提交 docs/24 与 STATUS。因此提交后工作树仍会显示上述 docs/23/重链脚本的外来修改，不宣称工作树干净。

## 4. 第一、二部分状态：未执行，修法未认证

| 要求 | 本轮状态与原因 |
| --- | --- |
| 226 开发归档及 45 compiler-rt 的逐成员/逐索引普查 | NOT RUN；第零步失败。compiler-rt 是否全原生 ELF、当前索引是否完整均不在本轮确认范围 |
| 按 compiler-rt 普查结果选择修法、生成 P/llvm-archive-fix.spec | NOT RUN；没有普查结果，未选择两种修法之一；未生成 spec 副本或“显式 strip 归档清单” |
| 同根同宏链小 spec 正负对照 | NOT RUN；无本轮 brp 调用数、格式错误行数或探针索引结果 |
| 真实 `%install`，独立 buildroot，18 GiB/SwapMax=0 | NOT RUN；未执行 `rpmbuild -bi`、`-bb` 或其他打包命令，未触碰共享 BUILDROOT |
| 226 个完整符号→成员映射相等 | NOT RUN；§2.3 三计数不能替代此验收 |
| compiler-rt 45 个成员 SHA/索引与 H 相等 | NOT RUN；没有成员 mtime 差异结论 |
| 非 .a 内容与原 22 RPM 逐文件相等 | NOT RUN；原 RPM 身份不匹配，未自动改用当前 RPM 作基准 |
| LLVMContext/Module + lld 组件，bfd/lld 双消费者及坏 liblldCOFF.a 负例 | NOT RUN；不能借用另一会话结果 |
| 保留 compress/strip/python-hardlink/find-docs 等 brp 步骤的实际日志 | NOT RUN；本轮没有 `%install` 执行日志 |

**结论：尚不具备以本轮“完整验证通过”为依据提交独立归档修复的条件。**
docs/23 已提交的根因证据仍是历史记录，本轮没有重做或推翻它；缺失的是本任务要求的全面修法验收。

## 5. 第三部分状态：未执行，profile 绑定未认证

第二部分失败可以不影响第三部分，但用户明确规定**第零步完整性失败时第三部分也不执行**。
因此下列各步均 NOT RUN：

1. 16 GiB / 20 分钟的 emit-relocs 单 clang 重链。没有新 ELF、链接 wall/VmHWM 或重链后 cache 统计。
2. `llvm-objcopy --strip-debug` 与 `check_bolt_elf.py`。
3. merged-v2 的 6 GiB、单线程纯 BOLT 重写（含 `-stale-threshold=5`）。没有新 dyno-stats、stale/invalid 或三类警告计数。
4. 对照 23592/144032 与 1/2804/6 的图等价实证。
5. BOLT/未 BOLT 混合 clang 的 30 TU 完整 `.o` 逐字节比较与 `--host-arch x86_64` 活性检查。

**profile v2 能否绑定混合 clang：本轮未确证。** 不能用未执行的检查宣布图等价，也不能据此宣布必须重训。

## 6. 恢复工作的必要条件与约束自检

恢复前需要用户明确用于比较的可信资产版本，以及如何处理当前与 docs/22/docs/23 不同的 RPM、cache、SOURCES spec。
本轮只保留差异，不擅自恢复共享目录，不将现值登记成新的预期值，不用另一会话报告替代实测。
之后若获继续授权，应重新取得独占锁并完整重跑第零步；包括本轮未做的 Ninja dry-run。

| 自检 | 答案 |
| --- | --- |
| 是否独占核查并创建/回收本会话锁？ | 是，§1；锁进程退出 0，锁已删除 |
| 是否保留 docs/23 与外来工作痕迹？ | 是，§3；docs/23 未改，外来脚本隔离，跟踪文件副本/diff 保存 |
| 是否把另一会话成功声明作为本次证据？ | 否 |
| 是否修改工作树 spec/源码、SOURCES spec、共享 BUILDROOT 或 cache？ | 否；只读检查，唯一 R 内写操作是本会话锁的建立/删除 |
| 是否执行真实 `%install`、重链、BOLT、完整重建或实验重试？ | 否，第一到第三部分都未启动 |
| 是否性能校准、采新 profile、构建 Chromium、推 Gerrit？ | 否 |
| 是否完整验证修法/profile？ | 否；第零步 FAIL，停止原因与未执行项逐项列明 |

## 附录：本轮证据索引

| E 下文件 | 内容 |
| --- | --- |
| `initial-state.json`、`initial-working.diff`、`initial/`、`committed/` | 起点提交、脏工作树、完整备份、已提交参考文本 |
| `hold_lock.py`、`exclusivity-before.json`、`lock-acquired.json`、`lock-released.json` | 本轮锁/进程扫描实现及原始生命周期 |
| `check_assets.py`、`assets-console.log`、`assets.json` | 本轮只读核查实现、实际输出与汇总 |
| `asset-commands.json`、`libLLVM*.a-armap.stdout` / `.stderr` | 三归档完整命令、退出码与原始输出 |
| `cache-files.json` | cache 本轮逐文件枚举 |
| `sources-spec.current`、`sources-spec.diff` | 当前 SOURCES spec 副本及全文差异 |
| `foreign-artifacts.json`、`preservation-check.json` | 隔离/备份位置与收尾保护检查 |
| `preparation-shell.stderr` | 锁脚本准备阶段的一次 shell 引号错误；实际锁/资产核查前发生 |

准备阶段 shell 输出 `unexpected EOF while looking for matching` 引号错误，未执行到锁脚本；改用直接启动后才取得 §1 的锁。
这不是 rpmbuild/BOLT 实验失败或重试；所有实验均为零次。
