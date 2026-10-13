# 49 续五至续六：x86完整构建环境、准入与验证记录

日期：2026-10-13；开场提交 `6e874fdbd0149a33167c9b83f8938d17df7c7ceb`。
**当前状态（续六）：新固定Base仓库预检PASS；磁盘两项准入PASS，正在准备唯一一次x86完整构建。尚无新RPM验收或BOLT交接。**

历史续五状态：STOP_BASE_REPOSITORY_404；下文§1–§6保留原记录。

本页承接[发布模式认证与续四](49_release_attribution.md)，保留旧停止判定。发布模式60对认证、两条x86全量回归与PS3/PS2顺序apply/tree PASS沿用同SHA证据，不冒称新RPM认证。原始输出位于 E=`/home/linhao/Toolchain/development/llvm-optimize/temp/release-x86-full-build-20261013`，只存本机。

## 1. 授权、身份与路径

用户明确批准只删除两ARM构建树的ThinLTO缓存目录内容，以满足新x86完整构建准入；缓存目录本身、BUILD原件、GBS缓存、证据/日志保留。理由为剩余ARM转换与限制负例不重新链接；以后若在两树重链须按冷缓存处理。本授权是对此前“不清理”的严格限域例外，不扩展到其他目录、BOLT资产或任何其他项目。

|别名|完整路径|
|---|---|
|W|`/home/linhao/Toolchain/development/llvm-optimize`|
|R32|`/var/tmp/llvm-optimize-arm-c1-20261010/gbs-libraries-armv7l/local/BUILD-ROOTS/scratch.armv7l.0`|
|R64|`/var/tmp/llvm-optimize-arm-tls-aarch64-20261010/gbs-aarch64/local/BUILD-ROOTS/scratch.aarch64.0`|
|B32/B64|分别为R32/R64下的`home/abuild/rpmbuild/BUILD/llvm-22.1.8/build`|
|计划新x86根|`/var/tmp/llvm-optimize-x86-archivefix-20261013`（未创建）|

14项Source/spec/config/比较器/两份已上传补丁/新候选与续四冻结值全部一致。工作树只存在既有用户`gbs_llvm.conf`修改，未归入本提交。两把项目锁取得后执行盘点/删除，重构建未启动、没有占用BOLT共享重任务锁；BOLT工作树/分支/证据未进入或修改。证据：E/initial-integrity.json、lock-acquired.json、post-cleanup-integrity.json。

宿主mmap配置未改；历史恢复命令仍为`sudo sysctl -w vm.mmap_min_addr=65536`，重启也会恢复。本轮没有/proc挂载。

## 2. 缓存路径确认与只读盘点

两根`CMakeCache.txt`中的原文均为：

```text
LLVM_THINLTO_CACHE_PATH:STRING=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache
```

这是chroot内绝对路径；映射到对应R32/R64后，两个删除范围精确为：

- `/var/tmp/llvm-optimize-arm-c1-20261010/gbs-libraries-armv7l/local/BUILD-ROOTS/scratch.armv7l.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache`
- `/var/tmp/llvm-optimize-arm-tls-aarch64-20261010/gbs-aarch64/local/BUILD-ROOTS/scratch.aarch64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache`

|架构|CMakeCache行号|Ninja clang目标/链接flags行号|已记录的链接参数|
|---|---:|---|---|
|armv7l|1732|build.ninja:90089 / 90092|`-Wl,--thinlto-cache-dir=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache`|
|aarch64|1741|build.ninja:96747 / 96750|`-Wl,--thinlto-cache-dir=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache`|

原始片段及完整clang目标块：E/*-cache-path-lines.txt、*-clang-link-block.txt；两个配置文件与构建图SHA见cache-inventory.json。路径resolve后仍在本根BUILD中，无软链接、跨设备或缓存内挂载；删除前逐文件inode/size/mtime再次核对。补充尝试从宿主`ninja -t commands`导出链接命令时，宿主PATH没有ninja，未执行任何目标；最终依据直接采用已有build.ninja的clang链接块和CMakeCache原文，不重建命令、不修改生成文件。

### 2.1 删除前缓存文件

|架构|普通文件数|逻辑字节|实际可回收文件块字节|GiB|
|---|---:|---:|---:|---:|
|armv7l|9,132|7,535,910,568|7,554,351,104|7.035538|
|aarch64|8,726|13,380,418,992|13,398,233,088|12.478077|

共17,858文件；无子目录、软链接、特殊文件或范围外硬链接。回收估计使用唯一inode的st_blocks×512，而不是用逻辑字节冒充实际空间；缓存目录占用不计入回收，因为目录保留。清单含每个文件的路径/dev/inode/size/blocks/nlink/mtime/mode，分别存E/armv7l-cache-manifest.jsonl、aarch64-cache-manifest.jsonl。

### 2.2 /var/tmp顶层目录（删除前，只读du）

命令形式：`timeout 120 du -sx -B1 <顶层目录>`；根内排名使用`timeout 180 du -x -B1 <R32或R64>`。`-x`不跨文件系统。下表“部分”是不可读条目导致du exit1的可读下界，不能声称全量精确统计；完整stderr与退出码见E/du-inventory.json、*-du.stderr。另尝试免密只读`sudo -n du`，两根均返回“a password is required”，没有输入密码或变更权限。缓存自身全部可读，缓存计数/回收与准入不受这些其他目录盲区影响。

|/var/tmp下目录|可读占用GiB|状态|
|---|---:|---|
|`/var/tmp/llvm-optimize-arm-tls-aarch64-20261010`|50.734028|部分，exit 1|
|`/var/tmp/llvm-optimize-archivefix-v2-final-20261009`|46.316360|完整|
|`/var/tmp/llvm-optimize-arm-c1-20261010`|41.166027|部分，exit 1|
|`/var/tmp/llvm-optimize-llvm-strip-tizen-20261009`|8.928097|部分，exit 1|
|`/var/tmp/llvm-optimize-arm-stage1-20261010`|8.927795|部分，exit 1|
|`/var/tmp/llvm-optimize-archivefix-v2-tizen-20261009`|8.922398|部分，exit 1|
|`/var/tmp/gbp_n8i9xq9v`|1.070770|完整|
|`/var/tmp/.gbs_export_78i7dgrb`|0.092278|完整|
|`/var/tmp/linhao-gbs`|0.000217|完整|
|`/var/tmp/.gbs_export_emue9l22`|0.000050|完整|
|`/var/tmp/epp-client`|0.000004|部分，exit 1|
|`/var/tmp/systemd-private-2033de4e268049c0952137c313232414-ModemManager.service-ZyzUOu`|0.000004|部分，exit 1|
|`/var/tmp/systemd-private-2033de4e268049c0952137c313232414-colord.service-bKkunB`|0.000004|部分，exit 1|
|`/var/tmp/systemd-private-2033de4e268049c0952137c313232414-fwupd.service-k4FB1N`|0.000004|部分，exit 1|
|`/var/tmp/systemd-private-2033de4e268049c0952137c313232414-polkit.service-km5LPj`|0.000004|部分，exit 1|
|`/var/tmp/systemd-private-2033de4e268049c0952137c313232414-power-profiles-daemon.service-iCmn1w`|0.000004|部分，exit 1|
|`/var/tmp/systemd-private-2033de4e268049c0952137c313232414-switcheroo-control.service-XjzQfm`|0.000004|部分，exit 1|
|`/var/tmp/systemd-private-2033de4e268049c0952137c313232414-systemd-logind.service-ihMsp6`|0.000004|部分，exit 1|
|`/var/tmp/systemd-private-2033de4e268049c0952137c313232414-systemd-oomd.service-AY5BaE`|0.000004|部分，exit 1|
|`/var/tmp/systemd-private-2033de4e268049c0952137c313232414-systemd-resolved.service-39fa3c`|0.000004|部分，exit 1|
|`/var/tmp/systemd-private-2033de4e268049c0952137c313232414-systemd-timesyncd.service-oOPRey`|0.000004|部分，exit 1|
|`/var/tmp/systemd-private-2033de4e268049c0952137c313232414-upower.service-PNvVQV`|0.000004|部分，exit 1|

### 2.3 两根最大的10个可读子目录（删除前）

包含父子层级，各行不可相加；不是10个互斥载荷。路径相对于R32/R64；根本身不入排名。

|根|子目录|可读占用GiB|
|---|---|---:|
|armv7l|`home`|36.768959|
|armv7l|`home/abuild`|36.768955|
|armv7l|`home/abuild/rpmbuild`|24.064240|
|armv7l|`home/abuild/rpmbuild/BUILD`|23.661324|
|armv7l|`home/abuild/rpmbuild/BUILD/llvm-22.1.8`|23.661320|
|armv7l|`home/abuild/rpmbuild/BUILD/llvm-22.1.8/build`|20.998829|
|armv7l|`home/abuild/arm-tls-consumers-20261010`|11.769718|
|armv7l|`home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib`|8.512562|
|armv7l|`home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache`|7.036304|
|armv7l|`home/abuild/arm-tls-consumers-20261010/native-rerun`|6.784847|
|aarch64|`home`|45.980225|
|aarch64|`home/abuild`|45.980221|
|aarch64|`home/abuild/rpmbuild`|32.920086|
|aarch64|`home/abuild/rpmbuild/BUILD`|32.517170|
|aarch64|`home/abuild/rpmbuild/BUILD/llvm-22.1.8`|32.517166|
|aarch64|`home/abuild/rpmbuild/BUILD/llvm-22.1.8/build`|29.836418|
|aarch64|`home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache`|12.478767|
|aarch64|`home/abuild/aarch64-tls-consumers-20261010`|12.100582|
|aarch64|`home/abuild/aarch64-tls-consumers-20261010/native`|10.578014|
|aarch64|`home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64`|8.388477|

## 3. 预判、限域删除与磁盘复查

历史无清理写入预算236,006,948,864B（219.798599GiB）、1.2倍准入283,208,338,637B（263.758319GiB）沿用续四§7；其“文件系统空间变化、非隔离LLVM独占du”的边界不变。新增底线为单次>10GiB写入完成后仍≥30GiB；两门槛同时生效。

|时点|/var/tmp可用B|可用GiB|减219.798599GiB后的预算剩余|
|---|---:|---:|---:|
|盘点预判前|265,081,331,712|246.876228|27.077629GiB|
|删除后预期|286,033,915,904|266.389843|46.591244GiB|
|实际删除前|265,081,311,232|246.876209|27.077610GiB|
|实际删除后|286,033,895,424|266.389824|46.591225GiB|

预判两项PASS后才执行删除，18:57:31完成；实际释放20,952,584,192B（19.513615GiB），与可回收文件块估计完全相同。删除后可用266.389824GiB ≥263.758319；预算剩余46.591225GiB ≥30，**复查PASS**。这不是新构建实测峰值；如果后续构建获准启动，仍须持续采样并在可用<30GiB时中止。

实际删除使用打开的目录fd和`os.unlink(relative, dir_fd=fd)`，路径只能来自两份经核对清单；所有前置检查完成后才开始；没有使用扩大的rm范围。两缓存目录保留，各自0文件/0载荷字节。没有删除源码、归档、ELF、构建图、RPM、GBS缓存或证据；post-cleanup-integrity确认两根CMakeCache/build.ninja SHA不变。证据E/cache-delete-preflight.json、delete-safety.json、deleted-files.jsonl、cache-deletion-result.json；辅助原文inventory.py、delete_approved_caches.py保留于E。

## 4. 构建前仓库门禁：Base 404

磁盘通过后，调用已有`tools/build_llvm_x86_64.py`的`repositories(Audit, W/gbs_llvm.conf)`做标准只读预检，没有调用其build/main构建入口。配置SHA仍为`28f1caf93cd39738a7da1e0da8d5f945f7372963bb9823a507f9157294272169`。HTTP查询各一次，不换源、不重试。

|仓库|repomd结果|SHA256|
|---|---|---|
|Base：tizen-base-toolchain_20261001.092726|2026-10-13 18:58:06+08 HTTP 404|无成功响应体，不伪造摘要|
|Unified：tizen-unified-toolchain_20260814.092727|18:58:07 HTTP 200，4476B|`e7af3f222f0ce958678d964589f2d156e8b47ba463ac0b3b0b96c74663382200`|

Base失败URL（保持配置原值）：
`https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261001.092726/repos/standard/packages/repodata/repomd.xml`

Unified URL：
`https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260814.092727/repos/standard/packages/repodata/repomd.xml`

Unified primary/build.conf下载与repomd checksum一致；`queryconfig --dist <下载的buildconfig.conf> --archpath x86_64 rawmacros`及RPM宏求值仍得到`1|clang`，但这不能代替缺失的Base仓库。完整请求/宏/输出在E/repository-preflight/commands.log，文件与repositories.json/result.json同目录。

失败原文：

```text
REPOSITORY BLOCKER repo.base-standard: HTTP Error 404: Not Found
RuntimeError: preflight blocked: repo.base-standard: HTTP Error 404: Not Found
```

按失败停止规则，本轮到此结束；没有自行改用新快照、复原本地仓库或再次执行预检。现有GBS缓存仍保留，未把它们未经核对就当成本次新根的完整依赖仓库。

## 5. 完整构建、验收与后续状态

|步骤|结果|
|---|---|
|x86新根-ba完整构建、CMake配置门禁|NOT RUN；GBS/rpmbuild未启动、无新根/新RPM|
|验收1：身份/依赖、实际转换非SKIP|NOT RUN|
|验收2：完整install-post与execve/逐档strip退出码|NOT RUN|
|验收3：225开发档、45运行库、libarcher双归属|NOT RUN|
|验收4：同配方无补丁基线非归档比较|NOT RUN|
|验收5：七宿主/Tizen两包及运行库消费者|NOT RUN|
|验收6：独立真实安装与同树SKIP|NOT RUN|
|验收7：新构建≥10成员直接非LTO结构记录|NOT RUN，仅诊断的既有60对数据另见续四|
|构建时长、构建/转换/链接内存峰值、构建磁盘峰值|N/A，没有构建；不以盘点耗时冒充构建耗时|
|BOLT交接|NOT_READY；没有新树、build/cache路径或完成时间可交接|
|两ARM全量、根内小试、64MiB负例|NOT RUN，按原顺序停在完整构建之前|
|bash依赖清单、LLVM23探测|NOT RUN|
|发布模式完整构建|继续挂账；60对发布模式认证已PASS不变|

预定使用的PS3 SHA `0d777afbf7b1a7b86afc5c1da5f7bef6b622315efc1316be0cac2b6e782d94e7`、PS2 SHA `c679f342a72d52de92914cd2d0007c981e0d6d22a6b378f811ca8ee8e12da9ff`；生产Source `c43523c0ce04fc3310e670ff97823db8260c21250dc3172575a18db56500082e`、ARM候选 `1bac8db608554b35d16482711bf0667f1fbee8d60c6fc52f0f448d240ffaa9e4`，均未修改。候选提交说明“完整构建待补”保留，没有伪造final提交说明。

## 6. 收尾与证据边界

本轮仅指定缓存删除及只读预检，未执行LLVM/Chromium构建、BOLT、性能校准或Gerrit推送，没有修改GBS配置、Source/Commands、比较器或W/llvm。临时/proc挂载0、构建scope/采样器0；项目锁释放与本任务进程回收见E/lock-released.json、cleanup-final.json。后续任何ARM重链均按冷缓存估算，本轮原件与既有转换/消费者证据仍保留。

报告与STATUS同提交推送GitHub main；旧docs/49及续四原文保留，新增链接指向本页。报告小于50KB。原始JSON/日志/临时辅助脚本在E，不上传大文件；仓库产出只有本页、续四入口链接与STATUS更新。

## 7. 续六：具体Base快照选择与环境预检

开场main为`fe48ba0913c5a48938c8665b1cf3ac5d56118a43`；新证据E6=`temp/release-x86-full-build-20261013/latest-base`。14项冻结身份一致；只存在用户既有gbs_llvm.conf修改，两项目锁取得。用户授权新Base具体快照，原因是更接近周四Quickbuild的Toolchain环境；不复原旧缓存仓库、不改W配置、不改Source/Commands/比较器/候选补丁；失败不另换快照。

### 7.1 目录索引与固定选择

2026-10-13 19:14:13+08读取[Base目录索引](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/)，HTTP200，874字节，SHA `1a6f2b43da23a55380bbceaa6f48b059dffcedcecbe47b3251f250a5557bef16`。实际href包含以下三个具体目录，按日期时间排序选最大值，没有使用reference/latest：

- `tizen-base-toolchain_20260914.073422`
- `tizen-base-toolchain_20260924.094908`
- `tizen-base-toolchain_20261010.120615`

选中`tizen-base-toolchain_20261010.120615`。原文E6/base-index.html、请求与排序证据snapshot-selection.json。

### 7.2 两仓库与配置

调用已有`tools/build_llvm_x86_64.py.repositories(Audit, E6/gbs-build.conf)`，19:14:23–19:14:31完成只读预检PASS；下载的primary/build.conf均验证repomd checksum，宏求值`1|clang`。

|仓库|repomd HTTP|repomd SHA256|
|---|---|---|
|Base 20261010.120615|200|`2a99108e748092148d1161f4ef5e50fbaa57d98132460db6ad02852fea4a39a5`|
|Unified 20260814.092727|200|`e7af3f222f0ce958678d964589f2d156e8b47ba463ac0b3b0b96c74663382200`|

原配置SHA `28f1caf93cd39738a7da1e0da8d5f945f7372963bb9823a507f9157294272169`；专用配置SHA `d1ff39acbaffd03f3c626e9fa8c4a397ea902066e722fd305539cb298de7ab34`。完整diff（只有一处Base URL替换）：

```diff
--- W/gbs_llvm.conf
+++ E/gbs-build.conf
@@ -6,7 +6,7 @@
 repos = repo.base-standard, repo.unified-standard
 
 [repo.base-standard]
-url=https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261001.092726/repos/standard/packages/
+url=https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261010.120615/repos/standard/packages/
 
 [repo.unified-standard]
 url=https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20260814.092727/repos/standard/packages/
```

仓库原始元数据、完整命令、宏和结果见E6/repository-preflight。此处是仓库预检，尚非GBS完整依赖解析或CMake验收。

### 7.3 环境包版本对照（参考，不作门禁）

Rnew为§1历史x86根；只读`rpm --root Rnew --dbpath /var/lib/rpm -qa`，全部列表E6/rnew-rpm-qa.tsv。首次未显式dbpath的宿主rpm查询尝试了/home/linhao/.rpmdb并失败；只读诊断后指定Tizen实际/var/lib/rpm成功。无构建重试、无根内容修改。新版本取Base primary，不能混称尚未创建的新根实际安装版本。版本格式version-release.arch，epoch均0。

|包|Rnew已装|新Base提供|
|---|---|---|
|bash|3.2.57-1.8.x86_64|3.2.57-1.4.x86_64|
|binutils|2.43-1.9.x86_64|2.43-1.6.x86_64|
|binutils-devel|2.43-1.9.x86_64|2.43-1.6.x86_64|
|build|20120927-1.1.noarch|20120927-1.1.noarch|
|clang|22.1.8-1.6.x86_64|22.1.8-1.6.x86_64|
|cmake|3.31.2-1.2.x86_64|3.31.2-1.6.x86_64|
|coreutils|6.9-14.2.x86_64|6.9-14.1.x86_64|
|elfutils|0.189-1.10.x86_64|0.189-1.6.x86_64|
|gcc|14.2.0-1.10.x86_64|14.2.0-1.6.x86_64|
|gcc-c++|14.2.0-1.10.x86_64|14.2.0-1.6.x86_64|
|glibc|2.40-1.10.x86_64|2.40-1.7.x86_64|
|glibc-devel|2.40-1.10.x86_64|2.40-1.7.x86_64|
|libgcc|14.2.0-1.10.x86_64|14.2.0-1.6.x86_64|
|libllvm|22.1.8-1.6.x86_64|22.1.8-1.6.x86_64|
|libstdc++|14.2.0-1.10.x86_64|14.2.0-1.6.x86_64|
|llvm|22.1.8-1.6.x86_64|22.1.8-1.6.x86_64|
|ninja|1.13.1-1.9.x86_64|1.13.1-1.5.x86_64|
|patchelf|0.16.1-1.8.x86_64|0.16.1-1.5.x86_64|
|python3|3.14.2-1.6.x86_64|3.14.2-1.6.x86_64|
|python3-devel|3.14.2-1.6.x86_64|3.14.2-1.6.x86_64|
|qemu-accel|未安装|0.4-1.1.x86_64|
|rpm|4.14.1.1-1.4.x86_64|4.14.1.1-1.6.x86_64|
|rpm-build|4.14.1.1-1.4.x86_64|4.14.1.1-1.6.x86_64|
|util-linux|2.41.2-1.4.x86_64|2.41.2-1.6.x86_64|

primary中没有名为lld的独立x86_64/noarch包；不得据此声称lld工具不存在，工具归属以新根实际文件/RPM查询确认。gbs由宿主运行，未作为根内同名包提供。Unified提供strace-6.6-0.x86_64，但Rnew未装；本轮不为记录工具改spec依赖。完整列表E6/package-comparison.json。

### 7.4 磁盘与验收4边界

19:15复查/var/tmp可用286,023,012,352B（266.379688GiB）；≥263.758319GiB且减219.798599GiB后≥30GiB，两项PASS。后续启动前再次核查、构建运行中持续监测30GiB底线；本轮未清理任何文件。

旧docs/13/35/38基线来自原固定Base环境，glibc/binutils/gcc/rpm-build等发行号与本次新Base不同。它们不能直接充当“同环境未打补丁”基线；验收4按用户新规则列待PM裁决，不自动把差异豁免为通过。具体同环境替代方案及预算待构建完成后的实测安装段给出；其余验收继续。
