# 36 归档修复 v2：缓存复原 Base、Tizen 消费者验收与提交补丁

日期：2026-10-09（Asia/Shanghai）。起点 `9f27fbcc01d9c25b8adc7962548813cc3fc28f45`。
**PASS：固定 Base 的107个基础RPM全部从历史缓存复原；bfd/lld各一次串行构建与包内A/B验收通过，
两根113包NEVRA与docs/30完全相同。v2单提交format-patch已在刷新后的tizen_base上通过应用检查，供用户上传评审。**
本轮没有重建LLVM，没有修改W/llvm或gbs_llvm.conf，没有推送Gerrit。docs/25–35保持原样；
docs/35中的历史STOP保留，本报告闭合其Tizen消费者与提交材料挂账，不重判旧结果。

## 0. 范围与现场

| 别名 | 实际路径 |
| --- | --- |
| W | `/home/linhao/Toolchain/development/llvm-optimize` |
| E | `W/temp/archive-fix-tizen-consumers-20261009`；本报告未加前缀的原始证据路径均相对E |
| E30 | `W/temp/archive-fix-full-build-20260927` |
| C | `W/temp/archive-fix-v2-final-20261009/continue-20261009` |
| N | `W/temp/toolchain-archivefix-v2-final`，docs/35新RPM解包 |
| 历史缓存根 | `W/temp/gbs-root-archive-consumer-bfd`、`W/temp/gbs-root-archive-consumer-lld`，只读 |
| 新测试根父目录 | `/var/tmp/llvm-optimize-archivefix-v2-tizen-20261009`；两个新根后缀分别为`gbs-root-archive-consumer-v2-cached-bfd`和`-lld` |
| 提交工作树P | `W/temp/llvm-archivefix-submission-v2-20261009`，独立共享对象克隆、稀疏检出packaging；不移动W原分支 |

开场主仓库status为空，未发现本项目gbs/rpmbuild/ninja/lld/llvm-bolt竞争进程。
16:49:54取得项目独占锁：`W/temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock`，
holder PID334938，session=`tizen-consumer-c7433e3ca6534fd5b7ec1aca77110895`。
证据：`start.json`、`lock-acquired.json`。其他项目不在本锁范围内。

逐个读取docs/35的22个原RPM和C/new-rpm-repo中的22个副本/硬链接，SHA和大小全部匹配docs/35附录A；
没有重新打包它们。`new-rpm-identity.json`保存两套路径、NEVRA和SHA。
gbs_llvm.conf SHA仍为`a3fea7732532db26c11b88407464e0274a6d8b4277623364fe16b6980181b03f`。
W/llvm原HEAD仍为`f111162e94aa48ed367c9d2c039456c70e7160ae`，原spec SHA
`95887b2d060b38d5ef8f56936f7481a03d131f9d26432180a68e02ec95f0dda5`，本地三处并发改动未动。
保护清单为`protected-start.json`；收尾对照`final-integrity.json`。

## 1. 从历史缓存重建本地 Base

### 1.1 安装清单与缓存身份

两历史根实际缓存均在：

```text
local/cache/6472de3503e3aaf43e4695c51bdf18ee/*.rpm
```

各有107个RPM，共214条缓存路径。两份同NEVRA副本SHA逐一相同。
安装清单取自`E30/tizen-bfd/build.log`及`E30/tizen-lld/build.log`的113条`cumulate`记录，
再与紧随其后的实际RPM安装进度逐项核对；架构由对应RPM头部查询，未从文件名猜测。
例如bfd日志:196–308为完整113项，:312起执行安装；同日志:39–145记录107条原始下载URL，均来自：

```text
https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260912.061113/repos/standard/packages/
```

原清单按“包名属于本项目22包且Release恰为1”排除六个实际已安装自产包：
`clang`、`llvm`、`llvm-devel`、`llvm-static-devel`、`libllvm`、`lldb`，均为22.1.8-1.x86_64。
没有按模糊版本前缀误排除基础包；另外16个项目RPM不在旧测试根的113包安装清单内。
其余107个基础包全部在缓存找到，没有缺失，没有从Unified补包，也没有触发最新Base备用方案。

历史缓存还保留原repomd和primary：

| 项目 | SHA256 |
| --- | --- |
| 原Base repomd.xml | `68b93454b4800a462e228260b11926a63ad8bba0589cc3f1a7dc4f0525bc2a74` |
| 原压缩primary.xml.gz | `abe32fe31df569c59946b57b9ac651af4ffe0ba3e57a661d9c06480c9bc5dbb6` |

先核primary压缩文件摘要等于原repomd登记，再把107个RPM的SHA逐项与primary的package checksum对照，全部PASS。
这是**原快照缓存字节一致性**核对，不只是同NVR推断。没有把重建repo的元数据摘要声称为原repo摘要。
证据：`cache-inventory.json`（全部214路径）、`historical-{bfd,lld}-installed.json`（逐行来源及排除理由）、
`historical-repodata/`、`historical-metadata-verification.json`（107个checksum和实际安装行）、`reconstruction-plan.json`。

### 1.2 新仓库

复制107个匹配文件到全新`E/base-local-repo/`，共97,776,140 B；历史缓存root拥有，使用普通复制，
没有修改历史RPM或其权限。每个新副本再次核SHA。生成命令：

```sh
createrepo_c --workers 2 /home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-tizen-consumers-20261009/base-local-repo
```

exit0，新repomd SHA `a6c0ab57cce474f3d7943e3f7213a0719d39bcd4c59a109bb27f35cff9fecf00`。完整命令/输出为`createrepo.log`、`local-base-repository.json`；
附录A列出107包NEVRA与SHA，该JSON另含历史URL、两份缓存路径和新副本路径。
这是该测试环境所需的Base子集，不声称完整镜像整个快照。

## 2. 两个 Tizen 测试包

### 2.1 输入、协议与资源

原样使用docs/35 §5.2的`C/test-package-bfd`与`C/test-package-lld`，未改测试spec/源文件。
`test-source-identities.json`记录各Git HEAD和所有非.git文件SHA。
BuildRequires精确钉`llvm-static-devel/llvm-devel/llvm/clang = 22.1.8-1`，另含libxml2-devel、zlib-devel、util-linux。
使用docs/35同一buildconfig；只增加本地Base的第二个-R，仍保留原配置和Unified，无`--skip-conf-repos`。

两次完整GBS argv见`tizen-bfd/attempt.json`及`tizen-lld/attempt.json`，结构如下：

```sh
W=/home/linhao/Toolchain/development/llvm-optimize
C="$W/temp/archive-fix-v2-final-20261009/continue-20261009"
E="$W/temp/archive-fix-tizen-consumers-20261009"
# flavor先bfd，全部门禁通过后才lld；每个只执行一次。
gbs -c "$W/gbs_llvm.conf" build -A x86_64 \
  -B "/var/tmp/llvm-optimize-archivefix-v2-tizen-20261009/gbs-root-archive-consumer-v2-cached-$flavor" \
  --threads 1 --include-all --define '_smp_mflags -j4' \
  -D "$W/temp/archive-fix-v2-build-20260929/full-build/buildconfig.conf" \
  -R "$C/new-rpm-repo" -R "$E/base-local-repo" "$C/test-package-$flavor"
```

原资源包装`tools/build_llvm_x86_64.py:436`沿用，任务入口`E/run_tizen_consumer.py`：
准入MemAvailable≥8GiB，`systemd-run --user --scope -p MemoryMax=6G -p MemorySwapMax=0`，
`nice -n 15 ionice -c3`，30秒采样、宿主可用<2GiB中止、采样器及日志线程回收；串行。
编译`prlimit --as=4294967296 --core=0`；链接不设地址空间上限。
两次可用内存均立即满足，等待0次；根放新SSD路径以保留所有既有证据，磁盘准入仍≥60GiB。

### 2.2 依赖来源与环境复现

| 项 | bfd | lld |
| --- | ---: | ---: |
| 实际安装包 | 113 | 113 |
| 来自重建Base | 107 | 107 |
| 来自docs/35新RPM库 | 6 | 6 |
| 与docs/30的NEVRA差异 | 0 | 0 |
| 根内225归档+4工具SHA匹配N | PASS | PASS |

GBS保留的合并`local/order/.repo.cache`中，每个已安装NEVRA均唯一对应到上述两个本地repo之一；
逐包核对应RPM摘要，再核`installed-pkg/*`实际标记与日志实际安装行。
两份`environment-verification.json`记录**每一个基础包的实际选中来源**，并保存完整合并记录
`resolved-repository-cache.txt`。不是根据-R存在就假定使用了本地库。
lld运行中另存`transient-rpmlist.txt`；bfd临时`.init_b_cache/rpmlist`在正常GBS收尾时被删除，
故使用保留下来的唯一F记录和安装证据交叉核对，没有重跑测试来补文件。

每个构建日志:28的init_buildsystem命令包含本地新RPM库、本地Base库和原Unified URL；
原不可读Base由GBS识别阶段省略，gbs_llvm.conf没有修改。实际安装不需要从Unified取基础包。

关键环境全部与docs/30相同：glibc2.40-1.10、GCC/libstdc++14.2.0-1.10、binutils2.43-1.9、
rpm/rpm-build4.14.1.1-1.4、libxml2 2.15.1-1.7、zlib1.3.1-1.9。
编译/链接/运行均在Tizen x86_64根内；clang配置`/usr/bin/clang++.cfg`，target=`x86_64-tizen-linux-gnu`，
头文件、C++标准库、glibc/crt、libxml2均来自该根，不使用宿主头/运行库。
编译器版本22.1.8；六个项目包NEVRA与历史相同但内容明确取本轮v2 RPM，已逐文件核验身份。

### 2.3 编译、链接、%check

先编译a.cpp/b.cpp/minimal.s为.o，再链接。`llvm-config --link-static`取库列表；
A运行PassBuilder O2，B调用lld ELF公开入口。完整展开argv在各`compiler-linker-commands.json`及build.log，
`check-outputs/a.driver`和`b.driver`保存`-###`输出。
GNU ld组实际`/usr/bin/ld.bfd`，lld组实际`/usr/bin/ld.lld`；两组driver输出均无-flto、-plugin、--plugin或-cc1。
例如bfd的展开以以下行开始，后续全部参数留在原始文件：

```text
clang version 22.1.8
Target: x86_64-tizen-linux-gnu
Configuration file: /usr/bin/clang++.cfg
 "/usr/bin/ld.bfd" "--hash-style=gnu" "--eh-frame-hdr" "-m" "elf_x86_64" "-pie" ...
```

两包均执行并通过：

```sh
opt -S -O2 input.ll -o expected.ll
./a input.ll > actual.ll
cmp expected.ll actual.ll
./b minimal.o generated > b.output
grep -x lld-in-process-link-ok b.output
if ./generated; then code=0; else code=$?; fi
test "$code" = 37
```

```text
2026-10-09T16:54:23+08:00 [   76s] TIZEN_CONSUMER_CHECK_PASS bfd A_IR_IDENTICAL B_GENERATED_EXIT_37
2026-10-09T16:56:12+08:00 [   44s] TIZEN_CONSUMER_CHECK_PASS lld A_IR_IDENTICAL B_GENERATED_EXIT_37
```

GBS、scope command和%check均exit0；随后重新读取expected/actual核相同，验证根内225归档及
clang-22/opt/llvm-config/lld四工具SHA与N相同。结果`installed-identities.json`、`check-outputs/`。
`--whole-archive -shared`仅诊断：两组链接exit0，未定义符号原始输出分别508/507行，
包含动态运行库引用；没有加-zdefs或将清单非空当门禁失败，也不据此认证任意全集组合的消费者语义。
完整stderr/stdout/undefined列表均保留。

### 2.4 实测记录

| 项目 | bfd | lld |
| --- | ---: | ---: |
| 启动 | 2026-10-09T16:52:56+08:00 | 2026-10-09T16:55:17+08:00 |
| 结束 | 2026-10-09T16:54:25+08:00 | 2026-10-09T16:56:15+08:00 |
| 入口wall（秒） | 88.644845 | 58.435464 |
| scope MemoryPeak（B） | 6230188032 | 5762170880 |
| 宿主最低可用（B，30秒采样） | 23389982720 | 23413002240 |
| 准入MemAvailable（B） | 23650430976 | 23758667776 |
| GBS/%check | PASS / PASS | PASS / PASS |
| 等待/重试次数 | 0 / 0 | 0 / 0 |
| sampler/log-reader回收 | true / true | true / true |

两组memory.events全部0，无OOM；完整time-v、scope内存和cpu.stat在`tizen-summary.json`及各scope目录。
这里是功能验收的执行记录，不是性能比较；scope峰值含页缓存，不当作链接器自身RSS。
原采样/日志线程均回收，完整退场状态见各outcome.json与`final-integrity.json`。

## 3. 提交补丁

### 3.1 目标基准刷新与证据边界

两包及安装身份验收通过后，仅做一次无凭据交互fetch：

```text
git fetch --no-tags origin refs/heads/tizen_base:refs/remotes/origin/tizen_base
GIT_TERMINAL_PROMPT=0
GIT_SSH_COMMAND=ssh -o BatchMode=yes -o ConnectTimeout=10 -o ConnectionAttempts=1
exit=0
2d23367d74afbf2bb1e9e4013fce072b3a154109 -> cb67996861d070d68fec2b4c623eed7d20ba2e23
```

`target-fetch.json`保存原始输出。新目标已含x86_64 -O3/ThinLTO配方；相对原目标的两次上游提交和spec全文差异
为`target-ref-refresh.diff`，与此前验证基准f111162e的差异为`target-vs-validated-base.diff`。
目标spec快照`target-base.spec`，SHA `9ee73e37f1297a261b835bcd9c7fa2fbff72e271816950991cbe95be0945edda`。

**本轮没有构建刷新后的整个tizen_base配方。** 提交基于用户要求的最新可取得HEAD；
验证证明的是：本次Source及两处新增spec块与已验内容完全相同，除此之外保持新基准逐字节不动；
不能把它写成“新目标完整配方已经重建通过”。新增配方的原命令超出认证策略时，Source会按设计失败并要求重新认证。
本地已有O3/ThinLTO基线的完整构建、增量新RPM与本轮消费者是本补丁的实测证据；将来目标流水线仍需正常构建评审。

### 3.2 内容、应用检查与SHA

[format-patch](../patches/archive-index-fix/0001-Fix-llvm-static-devel-usability-with-ThinLTO.patch)
与[便于直接阅读的Source](../patches/archive-index-fix/llvm-static-archives-native.py)均在`patches/archive-index-fix/`。
补丁内已含Source，不需要重复手动拷贝。只有2个文件：

1. packaging/llvm.spec两处插入：无架构条件的Source1005及x86_64 util-linux BR；%install末尾x86_64转换调用。
2. packaging/llvm-static-archives-native.py，SHA严格为已验`6bd0546a…`。

没有加入__strip定义、并发改动、优化开关或其他配方差异；x86_64以外不新增转换路径。
精确spec diff：

```diff
diff --git a/packaging/llvm.spec b/packaging/llvm.spec
index 64705188b67c..8240282641a3 100644
--- a/packaging/llvm.spec
+++ b/packaging/llvm.spec
@@ -44,6 +44,11 @@ Source1001: llvm.manifest
 Source1002: mlgo_arm_model.tar.gz
 Source1003: mlgo_aarch_model.tar.gz
 Source1004: mlgo_x86_model.tar.gz
+Source1005: llvm-static-archives-native.py
+
+%ifarch x86_64
+BuildRequires: util-linux
+%endif

 %{!?mlgo_build_jobs: %define mlgo_build_jobs 6}
 %{!?mlgo_verify_configure_only: %define mlgo_verify_configure_only 0}
@@ -421,6 +426,20 @@ rm -rf %{buildroot}%{_libdir}/debug/*
 rm -rf %{buildroot}/usr/lib/libear/*
 rm -rf %{buildroot}/usr/lib/libscanbuild/*

+%ifarch x86_64
+# Run after compilation has finished; these workers do not overlap build jobs.
+# Preserve the standard RPM post-processing, including archive strip -g.
+rm -rf "%{_builddir}/%{buildsubdir}/build/native-archive-conversion"
+python3 %{SOURCE1005} --root "%{buildroot}" \
+    --build "%{_builddir}/%{buildsubdir}/build" \
+    --evidence "%{_builddir}/%{buildsubdir}/build/native-archive-conversion" \
+    --arch x86_64 \
+    --compiler "%{_builddir}/%{buildsubdir}/build/bin/clang-22" \
+    --disassembler "%{_builddir}/%{buildsubdir}/build/bin/llvm-dis" \
+    --nm "%{_builddir}/%{buildsubdir}/build/bin/llvm-nm" \
+    --jobs 4 --address-space-bytes 4294967296 || exit 1
+%endif
+
 %post -n clang -p /sbin/ldconfig
 %postun -n clang -p /sbin/ldconfig

```

把两处新增块从提交spec移除后，字节恰等于目标base spec；新增块与S实测spec的新增块逐字节相同。
最终format-patch本身在干净base执行：

```text
git apply --check --index <最终format-patch>   # exit0，空stdout/stderr
git apply --index <最终format-patch>          # exit0
git diff --cached --check                    # exit0
git write-tree
7b49745738b5512fbbed890e67e6a3861e1e39a5
```

应用后的完整tree与单提交tree一致，父提交为cb67996861d070d68fec2b4c623eed7d20ba2e23。
完整命令、cwd、退出码、stdout/stderr为`submission-commands.jsonl`，断言结果为`submission-verification.json`。

| 项目 | 值 |
| --- | --- |
| 目标base | `cb67996861d070d68fec2b4c623eed7d20ba2e23` |
| 补丁内单提交 | `2d773cb6191e07610627a544af908b4c19da6abc` |
| format-patch字节 | 46381 |
| format-patch SHA256 | `ddef2221db9ba1c044b0087b9fcde2a93202fdf28c518b4d0dcd1c4653119ac6` |
| Source SHA256 | `6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557` |
| 新spec SHA256 | `d93a549206434c4512c60d5a96bfeb133b7aaf6ea13b8cd0302e06c1cb99b1c9` |
| 作者 | FatTank <hao.lin@samsung.com> |
| Change-Id | `Id4eb147e7ec4764d58a81110cf7bf57d21b64ac8` |

被替换的v1保留于Git历史docs/31与E/v1-backup/，不销毁旧证据：
旧patch SHA `0c40c91cb6b896fd93f2712b669eec6771d219268dff7d290539fbb98d0bea58`；
旧Source SHA `2476c5efa061499d7963e0f0976f0c9c86944b688f5bcc48ea40911574af399e`。

### 3.3 提交说明全文

```text
packaging: fix llvm-static-devel usability with ThinLTO

ThinLTO leaves LLVM bitcode in the static archives. The GNU strip invoked
by brp-strip-static-archive does not understand these members but can
return success while dropping or truncating the archive symbol index.
Even with an intact index, GNU ld without LTO or an LLVM plugin cannot
link bitcode members.

At the end of %install, convert bitcode members to native objects using
an explicitly certified backend policy, then rebuild deterministic GNU
archives and their indexes. Preserve existing native members, original
member order and duplicate member names. Leave the standard RPM
post-processing unchanged; the final archives contain no DWARF after
standard strip processing.

Apply the conversion only on x86_64, to all installed archives containing
bitcode, including libarcher_static.a from libomp-devel (also owned by
llvm-static-devel). Leave armv7l and aarch64 for separate certification.
Tool compilation and linkage are unchanged.

The x86_64 host tools also cross-compile ARM packages through accel,
which extracts tools rather than static archives. Consumers of the
x86_64 static-devel archives build x86_64 targets.

Fail closed on unclassified original compiler options, an uncertified
LLVM major version or incompatible IR metadata. Such changes require
option-policy review and recertification; this is not generic option
replay.

This fix targets LLVM recipes using -O3 and ThinLTO. A recipe without
ThinLTO is a no-op (NATIVE_ARCHIVES_SKIP) when its installed archives are
already native. When ThinLTO is enabled, the original compiler options
must match the certified policy or %install fails pending recertification.

Validation used the certified LLVM 22 x86_64 recipe: one full build plus
incremental continuation, with build/compile/link concurrency 6/6/2 and
debuginfo -j4. All 225 development archives contain native objects and
complete symbol indexes. All 45 compiler-rt archives retain identical
member ELF bytes and index mappings; only ar header timestamps differ.
Non-archive files, including clang, lld and llvm-ar, are byte-identical
to the pre-fix baseline. A fresh independent %install reconverts and
passes; rerunning the converter on that same tree reports SKIP.

Host and Tizen consumer tests pass with plugin-free GNU ld without LTO
and with lld. They exercise LLVM IR parsing and the O2 pass pipeline,
in-process lld ELF linking, and, on the host, shared-library loading and
section garbage collection. Tizen tests use the same 113 installed
package versions as the earlier validated environment; 107 Base RPMs
were recovered from its cache and checked against archived repository
checksums.

Change-Id: Id4eb147e7ec4764d58a81110cf7bf57d21b64ac8
Signed-off-by: FatTank <hao.lin@samsung.com>
```

## 4. 结论与收尾

**可以提交评审：v2的Tizen GNU ld（无LTO/插件）和lld消费者门禁均PASS，补丁已基于当前可取得tizen_base生成并通过apply检查。**
本轮仅2次小测试包构建、均一次成功；没有重建LLVM、没有重试测试包、没有改W原件或gbs配置。
没有触发“最新Base”备用分支，没有新增profile、运行优化重写或构建Chromium，没有推送Gerrit。
本机原固定Base远端缺失仍是客观历史事实，但这两个测试环境已通过缓存复原，不再阻塞归档修复提交材料。

证据边界：225开发归档/45compiler-rt、非归档零差异、独立-bi/SKIP和七宿主消费者沿用docs/35；
本轮新实测闭合Tizen包内验收。compiler-rt“逐字节相同”指成员ELF及索引，不掩盖ar header时间戳差异。
未覆盖armv7l/aarch64的静态库转换，也不将whole-archive诊断当成任意下游包已通过。

保护核查、进程/挂载和采样器退出为`final-integrity.json`；项目锁由原持有者释放，`lock-released.json`存证。
完整任务状态`final-outcome.json`。本报告与STATUS和两个补丁文件同一commit推送GitHub，用户自行安排Gerrit。

辅助取证说明：一次只读元数据探测早于仓库JSON生成，另一次读取遇到已正常清理的临时rpmlist；
均未触发构建/消费者失败或重跑，后者改读保留的唯一仓库记录及安装标记。原记录在`orchestration-note.txt`。
只读路径枚举遇到挂载proc权限后不再递归该树；未改宿主权限或历史根。

## 附录 A：复原的107个Base RPM

全部来自上述固定Base缓存，两历史根SHA相同且与历史primary相符；每行均在两根实际安装。

| NEVRA | SHA256 |
| --- | --- |
| app-rootstrap-checker-1.0.0-1.1.x86_64 | `0310b58fc02e3fbe2dd630d267c08899ca480e31a2db502fa52d2affb3625d4d` |
| autoconf-2.71-1.11.noarch | `3b4aa5f4e753255961cb21b46d30fe9a80b6102068f760e2e01ebf56f1e03588` |
| automake-1.16.5-1.11.noarch | `f821e5acdd7e64795cbf613b5176eb869787893012d32bd5325e861209f6f824` |
| bash-3.2.57-1.8.x86_64 | `f889dd58f9a974fe25b7224298fc96d1ed20df7e3382e1307e36e8f33c035c1f` |
| binutils-2.43-1.9.x86_64 | `f73aedfc84da56c55a24d3e9e48d12aa7c4363663eef77c82a5ca316df3ffaa3` |
| binutils-libs-2.43-1.9.x86_64 | `3b5f89a2f44c2568498d7a3ea5d2670c1cb97326fe0c0da9d8b0ce0b62a6ff30` |
| build-20120927-1.1.noarch | `2a10cbeb369dc93963aaf3ff4cbb12a392a46a7dd4f90e13ce50df666d3700fb` |
| build-compare-2023.06.18-1.2.noarch | `5138c884d8bb2623d0239cf7caed14936f5e91de7c7a7eeb2d8fec0b262b26f8` |
| build-mkbaselibs-20120927-1.1.noarch | `e7747c2557c440a18fb44e3f8e0f51621fc310afb4e4d3a1562016edbd764bf7` |
| bzip2-1.0.8-1.8.x86_64 | `5c3fe93e6b334aa0610133321ae96bb408e1d3bfa9ef793f0521738647e30ca6` |
| coreutils-6.9-14.2.x86_64 | `d17e6f8fe1949d5ebb1931dfb3f3d7cc0e1ff63459e9b2b0ca15633aa0d903fe` |
| cpio-2.8-1.1.x86_64 | `b4c60bf6c23ef694c293b0ee6a770dac2c5dba9c61441291a21337637e073693` |
| cpp-14.2.0-1.10.x86_64 | `5ba89de5eb12bd1a534e9cff0d57d7f598444935a458c671482f923dac96a7ef` |
| diffutils-3.10-1.1.x86_64 | `594990fcab906eb0f0b641e8323f0921c9b8e3c9ea022683839c30b768d07c24` |
| elfutils-0.189-1.10.x86_64 | `befdc2fede466c760186fc28fdea22d9854bb7304ed6286cb1e498f40e49715b` |
| file-5.46-1.8.x86_64 | `f978142f67cee9b6e1ff755086681d172f40c24e319a44893630cc1930276d32` |
| filesystem-3.1-1.1.x86_64 | `1e89548f8d59b094cb196401336bff45955d3d20520693d2ea5578623f43fc57` |
| findutils-4.3.8-1.8.x86_64 | `72a652c5d096d61c08d0b3bfa8f5a13331b204a60b4efdfe1a180a2c0c71e657` |
| gawk-3.1.5-1.1.x86_64 | `156c3317a2f03e186563729020a0f80da3768bed00cfcaf8a3a8c582d8b8f4dc` |
| gcc-14.2.0-1.10.x86_64 | `5baeca35dd8fa497fbbec0d143c55c366a439e375a5688aafcd25dca0ea71c01` |
| gcc-c++-14.2.0-1.10.x86_64 | `a251991c6895af61f672cc820f65125adf7f0c4097a47ac0fd7dac78778ce4ab` |
| gdbm-1.8.3-1.10.x86_64 | `4d196992f97c6a11f5909c901af521b6ea316809f9abfefedbc982ed73c160c0` |
| glibc-2.40-1.10.x86_64 | `fd56378927086f81a506513a1075fe169ccb63917f7629ee6c3f37c410423818` |
| glibc-devel-2.40-1.10.x86_64 | `7cc9e71ce4d8f372a1d697f5a8c78cf35acfaa22783ab6a6b37c56a43021e23c` |
| glibc-locale-2.40-1.10.x86_64 | `9cd0aeb09529049a7df9ffdee57676656f4cf39bbda1c5fcedf76306a25733b9` |
| grep-2.5.2-1.10.x86_64 | `3772982bb63f346aa89f5e29667eec510c492e509b718040801ebe4580d9611b` |
| gzip-1.3.12-1.8.x86_64 | `41859f885b6b76c756f50fd9fe60393d070f85220f733009f3c7cf0c14d3e2f4` |
| hal-rootstrap-checker-1.0.0-4.1.x86_64 | `68ea1ac2f20d0e5d9c01e67c0410bcdbcfa57fa803be16a7dc5a614fb0d2a8be` |
| hostname-3.23-1.1.x86_64 | `b598385d7f2547545557a4fd6f0b7bb7edc98a69b44b7805790e7870c105e7a8` |
| less-685-1.1.x86_64 | `326ce166c3b21044401c8d8841ba1dc19c7ac2068b7f102a3a116694a531aa2e` |
| libacl-2.3.2-1.8.x86_64 | `6f63420b4768baf0803237f8959e1cee5aee0be7c0c308d5035da72796827e06` |
| libarchive-3.8.1-1.4.x86_64 | `1c26ede1fb4220fd1fff0d6f9eb22271cb21163675fff209aba6880392831ec0` |
| libarchive-tools-3.8.1-1.4.x86_64 | `92b0165cefca65bbbad1676ce2e8023c942b29133c658df1590f59ccd1dc57ad` |
| libasm-0.189-1.10.x86_64 | `354f70e606e454df44cab49b8a3d40cca638dcdbf920c0471137bd173d289656` |
| libatomic-14.2.0-1.10.x86_64 | `cb31c8137bf05b4ea886466b40d60c78b6ba8c44d858f448260a402948116588` |
| libattr-2.5.1-1.9.x86_64 | `0e58b2ff0c7217f7cf38c8d354e3cb564a1ab40ddb3a23cddd38b3b0cf192e9d` |
| libblkid-2.41.2-1.4.x86_64 | `de177037af099ac5beb3e3c585ebb6382c001a2c726c691503d4f3f6c9b1a9cb` |
| libbz2-1.0.8-1.8.x86_64 | `22f3e7e5589da540ce050a24209efee20f8e73641b3f712c519dcdc8cafc29c8` |
| libcap-2.73-1.10.x86_64 | `489919f5aa44103e6408a4d32a4e262629a230a8eb441cc01c98c389b5f6c536` |
| libcc1-14.2.0-1.10.x86_64 | `8804377be5278a4f5f4904aeb9ab1734e6cfcce880d40a95ea5ef74b00817a90` |
| libdw-0.189-1.10.x86_64 | `b8f607b53fd572b6162671b576697c9bef7a9a26765f17570d0d48e7048e64e4` |
| libelf-0.189-1.10.x86_64 | `1ebf4d95722924a58ea3f261bac96b0d1f7f77dc078a9374407cf89000f6569d` |
| libfdisk-2.41.2-1.4.x86_64 | `5b6c4f639cfe6162a6c2b37b992972ce07ead91715de607f9e2dcdf82d26b3de` |
| libfreebl3-3.109-1.1.x86_64 | `63c0a1000e059601bd27a49a1c4295704051414353573ec40df4887684ab49dc` |
| libgcc-14.2.0-1.10.x86_64 | `87960899eae6c67d7cc3700f06620704234a22f4616b91b491ba5e7330a8c8aa` |
| libgfortran-14.2.0-1.10.x86_64 | `6c61ef1caf4261d3bd763e1c697b0ccaf7ea719b5fac4b9c64b272ee3fa8c2f4` |
| libgomp-14.2.0-1.10.x86_64 | `7ff593718a8d79645ee0dfad381b392e635a670949400f102e8b46586032ea3b` |
| libitm-14.2.0-1.10.x86_64 | `93ca916f325e6cb104dcc159be2348278d327b0256d6323335b0449827a60961` |
| liblastlog2-2.41.2-1.4.x86_64 | `d5cb581e24371004acba41d824f16c009ad64684c2fe906449a16ce8c14ee8ab` |
| libltdl-2.5.4-1.10.x86_64 | `235cd0def0f008efb8828b898336969e817a259238928800a5cf49dbcc7aad78` |
| liblua-5.1.5-1.7.x86_64 | `e2d9152a5c0942d4ac8e55a8346029cd20b9de6f8f82d91b2c984e5268c1b59d` |
| liblzma-5.8.1-1.9.x86_64 | `18a0ca9c02fe6431a8177c74e4ffc19d1f7187c501952ecb1a0ca6cf8e4be19e` |
| libmagic-5.46-1.8.x86_64 | `60ba6a8d6c7606bfce1ae8cdd7ef5794fd0ca3c1100d823c231759421b57a312` |
| libmagic-data-5.46-1.8.x86_64 | `019725f69790b76767ba549353766b3b3f8e37e2a0e02c248c47da18e9c5f1de` |
| libmount-2.41.2-1.4.x86_64 | `4c419ed0918750bbd47a8ba3111cec43a84ce34572209f1cd3a9191cabebb51b` |
| libncurses-6.6-1.3.x86_64 | `a8e5c2b9a1d9b7413b0fcc29b913f1f10dabf76df06e556a25caf53f3c1aacfb` |
| libncurses5-6.6-1.3.x86_64 | `cfd6a867a06ad269d09f2e80da9392eb852a5177ce13a92406880649fa969a8b` |
| libncurses6-6.6-1.3.x86_64 | `c42e6590589fe7ac111e7442b53b7e5ca8ec75aeb941451317b24b6a9aa73a0f` |
| libopenssl3-3.5.5-1.8.x86_64 | `620771daf1dde3147db06650e37edb534baebb0d902410698818cf3914a8faff` |
| libpcre-8.45-1.9.x86_64 | `e0d862fb2db95344c1829f9fd351d8f1252c7d9c2a198b53f0b445e0a710a7c4` |
| libpopt-1.16-1.8.x86_64 | `dc0eadc4271b2add924f0d76fd0ff2212e788a7c812d0d935688a1def6f7ec9b` |
| libpython3_141_0-3.14.2-1.6.x86_64 | `aff3de47eb6d437f99ec0e5cb6db39cc41a2e84237d44a8011d584fa4d1b4379` |
| libquadmath-14.2.0-1.10.x86_64 | `613758e8363bc24ed0eac7eac3bac9b79524b185ffee4e2d0fbfacda2f376125` |
| libreadline-5.2-1.8.x86_64 | `c6f741271dfb355cbe5723ef5b89f6bfb049681c8806e9e40cd1a550fddcb568` |
| libsmack-1.3.1-1.7.x86_64 | `7b532b612323e66960652a8ca005815e1913240a90db0e97884498d2f2f369b8` |
| libsmartcols-2.41.2-1.4.x86_64 | `ca56429befa99db0b21c093093659823b3872b6b56b3b717be379bcbdac07826` |
| libsoftokn3-3.109-1.1.x86_64 | `3feeb6ac53a50a49daba636f1daf539e0734570fbc150909c96969478ea02b48` |
| libsqlite-3.51.0-1.9.x86_64 | `58cd8bcd2605f4beb20e3a45b80ed7ccd56b6e4aabf2b9cb18308ab608c07848` |
| libstdc++-14.2.0-1.10.x86_64 | `bfb8c0909595dfcff03856f2f218b32f06f17fd2150224b27c9c5813b22d084b` |
| libstdc++-devel-14.2.0-1.10.x86_64 | `37dd64484c6233db76e54b243a7543fb0928d21f588d9ea638e3615880538f4a` |
| libtool-2.5.4-1.10.x86_64 | `e16587b250a9c991c714619d00abe927fedc12f8cc2b4b96410596e04ae582f8` |
| libuuid-2.41.2-1.4.x86_64 | `06c0bc0ff9d6f0c03f3953e27ae3d8566dc41767c66c74b1e5ca2e9409da4e5b` |
| libxcrypt-4.4.36-1.10.x86_64 | `e9024ca20ad42a5c87e6d8051ff369776620363b954e3e49c5e7fbad47a8f932` |
| libxcrypt-devel-4.4.36-1.10.x86_64 | `7861cd7d42080202ac7174489a1f1e9758c2e90eef44c22d7e74700d1c6fdb4a` |
| libxml2-2.15.1-1.7.x86_64 | `a168b0e23b3a51132e63a6d518270b1f6375627317af7cf6341c29afdacb2dcf` |
| libxml2-devel-2.15.1-1.7.x86_64 | `884098777a739254a132f26b779d775af0ec31be574bb824698f08e2b8a2307b` |
| libxml2-tools-2.15.1-1.7.x86_64 | `a2b4ce7c5e2b2d63dd75fb4f1b4e45d27fa40f9cd4de08800a9006c620d87aec` |
| libzstd1-1.5.7-1.8.x86_64 | `5be348b937ca4314319c8061ccdd6d634303f5a4a864c61e88b313594b79c2b5` |
| linux-glibc-devel-6.6-1.9.x86_64 | `5e6e0a1230776fdbefcae5f56f8ffcdf64971fc23ca5d6b28fa765b6f89af4a8` |
| m4-1.4.20-1.1.x86_64 | `c76de1549cb2fbf8307c8fe44d0e0dd45b6f09cbe2bbea204b1df8012f891354` |
| make-4.4.1-1.8.x86_64 | `cf3dc90e95b9f8822fee11ea1fb8661ea7e008a7784e1b27075f5faff62e04a5` |
| ncurses-devel-6.6-1.3.x86_64 | `4b08ba36c807220f4530b28e288cd75aec0fc570a2343d058027a86117d1730d` |
| net-tools-2.0_20121208git-1.3.x86_64 | `57761bf7f5f39d11faab66f3713e8f65f59bb08ec3fa7c268e48bb27d974e843` |
| nspr-4.36-1.1.x86_64 | `fbc19311adb0d985666b665fa0bc9d4c0f3438bd143b3d1f4041cb1474e40119` |
| nss-3.109-1.1.x86_64 | `7b3b4e4df3e52f47c49fefb466ea85e2fb031b6b77d57f45f1676427dd38dd74` |
| nss-certs-3.109-1.1.x86_64 | `619841e41d103e581eb5be85fc90c54772fe76a7b514e0a474f40853dadffa3e` |
| pam-1.1.6-1.4.x86_64 | `8e722cf4ad81c4ed66b2eb9a9b1b5ad14f190b65e955af6c3680088d48685463` |
| patch-2.8-1.8.x86_64 | `617fa83e6fa37f3e27b3aa6e19d79857d0d820411d68481a9bbeab381ce8d50a` |
| perl-5.42.0-1.8.x86_64 | `7007d2050f27da1b5e104ff694d1600ba0b37bcae4deb036978acc3bf4995206` |
| pkg-config-0.29.2-1.8.x86_64 | `c9921fd52a1efc333bb1ec70dce4d5c3c90580a9487cc8aa97256c232eb3ae7d` |
| readline-devel-5.2-1.8.x86_64 | `763449fa6431cddc1c6865089e2362756b58407988f1cf6dbda600b773a2313a` |
| rpm-4.14.1.1-1.4.x86_64 | `ba3a470c8c560dc9ea5a01145a2c51a40db458c807c5d4606f8f87d78207d996` |
| rpm-build-4.14.1.1-1.4.x86_64 | `722f24fe7d100628cc31918f9860f7f74b1cf70ec17868f51edcfefd57d5d2b2` |
| sed-4.1c-1.9.x86_64 | `47a8fbbcb02d09286ab50a39f991814c5f41a1c5a5b932b9500c47b7073270dc` |
| setup-0.9-1.11.noarch | `e9af6371a1340a794babb48e1b014fdcfa6897b09e233e51a4cbd721fc46401b` |
| smack-1.3.1-1.7.x86_64 | `3213d0b894629d9a8964fd97d9ae66844a67894bf2fbaa8920acd01556366db3` |
| tar-1.17-1.1.x86_64 | `ec204e74b5c75595f329c02f644a0cfa9b1bf9f1dd38c0b9319385f1fa14bab2` |
| terminfo-base-full-6.6-1.3.x86_64 | `229249e0bfcbe821ca02ef1c27917428ce5ed13c903fb96e2c2d0a298a01cfd5` |
| tzdata-2025b-1.1.x86_64 | `2e23f7a27d82df76f72d19c7a68d429e2461a67926a29b3cf5bd3c077df8300e` |
| update-alternatives-1.22.21-1.1.x86_64 | `57a3a23bfabd32301e359c729a178ac930558154ca6cfebf0ca0c1812454773e` |
| util-linux-2.41.2-1.4.x86_64 | `34711dcc98cb9ef38f57ed3d8ee06b3c37090d91d42d0dec9072e82fb54a7edb` |
| util-linux-su-2.41.2-1.4.x86_64 | `4ccbb3f85ca2df34a8b16bf1d40a0384cdd4eec5d37045895dc661f7870f33f2` |
| which-2.17-1.1.x86_64 | `4be03efecaf353a16395430d371544902f91aa116208eab77db4f6a8170aecb0` |
| xz-5.8.1-1.9.x86_64 | `ccad2bccc55ef4874060d3cf1b6d8a10fa27500857a0a0b8a8df4252007af9b5` |
| xz-devel-5.8.1-1.9.x86_64 | `e2d17088491ce71ed01d02e17991fad39e86fe9382261cec6f5461e3415a8827` |
| zlib-1.3.1-1.9.x86_64 | `2498efc4856de5f0a82cc5c2a340727ecac400f9015b820369f10080609a2cb7` |
| zlib-devel-1.3.1-1.9.x86_64 | `a0f9cb8f741a1a5815dc5886816067dc700481758227b6ca383975379f6b3328` |

## 附录 B：证据入口

所有原始文件在E（§0绝对路径），temp不上传：

- `prepare_repo.py`、`verify_historical_metadata.py`及生成JSON：缓存、清单、摘要、仓库创建。
- `run_tizen_consumer.py`、`verify_tizen_installed.py`、`verify_environment.py`：限流入口及只读核查。
- `tizen-{bfd,lld}/{attempt,launch,result,outcome,scope-after-rpm,environment-verification,installed-identities}.json`。
- `tizen-{bfd,lld}/build.log`、`compiler-linker-commands.json`、`check-outputs/`：完整argv和原始输出。
- `tizen-summary.json`、`samples.jsonl`、`time-v.txt`（后两者在各tizen目录）：资源与回收。
- `make_submission.py`、`submission-commands.jsonl`、`submission-verification.json`、`commit-message.txt`及目标diff。
- `protected-start.json`、`final-integrity.json`、`lock-released.json`、`final-outcome.json`：现场和结束状态。
