# 49 续五至续六：x86完整构建环境、准入与验证记录

**当前状态（续八）：授权的三处导出临时目录已清理，正常磁盘准入PASS，无需一次性放宽；第二轮完整构建准备启动，结果待后续章节。**

日期：2026-10-13；开场提交 `6e874fdbd0149a33167c9b83f8938d17df7c7ceb`。
**历史状态（续七）：STOP_DISK_ADMISSION_AFTER_APPROVED_EMPTY_ROOT_DELETE。获批中止导出目录已删除，实际为15个空目录/0文件，释放61,440B（60KiB）；删除后/var/tmp可用263.726074GiB，仍低于263.758319GiB，差33.018750MiB。第二轮GBS调用0次，未清理其他目录、未重试；验收1–7未执行，无BOLT交接。**

**历史状态（续六）：STOP_DISK_ADMISSION_AFTER_EXPORT_HELPER_ABORT。新Base/Unified仓库预检PASS；GBS首次启动在源码导出阶段因入口漏选spec而主动中止，未创建chroot、未编译。入口已修正，但重跑前可用263.725967GiB低于263.758319GiB，按规则停止；没有重跑、清理或放宽门槛，没有新RPM/BOLT交接。**

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

primary中没有名为lld的独立x86_64/noarch包。Rnew的/usr/bin/ld.lld由llvm-22.1.8-1.6.x86_64提供（E6/rnew-lld-owner.txt），新Base的llvm同NEVRA；新根实际文件/版本因未初始化未测。gbs由宿主运行，未作为根内同名包提供。Unified提供strace-6.6-0.x86_64，但Rnew未装；本轮不为记录工具改spec依赖。完整列表E6/package-comparison.json。

### 7.4 磁盘与验收4边界

19:15复查/var/tmp可用286,023,012,352B（266.379688GiB）；≥263.758319GiB且减219.798599GiB后≥30GiB，两项PASS。后续启动前再次核查、构建运行中持续监测30GiB底线；本轮未清理任何文件。

旧docs/13/35/38基线来自原固定Base环境，glibc/binutils/gcc/rpm-build等发行号与本次新Base不同。它们不能直接充当“同环境未打补丁”基线；验收4按用户新规则列待PM裁决，不自动把差异豁免为通过。具体同环境替代方案及预算待构建完成后的实测安装段给出；其余验收继续。

## 8. 续六构建入口与预注册保护

环境阶段提交`2b6bde9`已推送main。独立完整源码checkout位于E6/source，HEAD为候选PS2 `4c36e899dffee2869af9afd174346e3eb9a7d7ca`，git状态为空；spec SHA `e88ef4cb4cfc4010bceb62a94389f517aedff0b2c2df819ba64dd988d9910426`，Source为冻结`c43523c0…`。未改W/llvm或原候选树。

新增[专用入口](../tools/run_certified_x86_release_build.py)，逐个钉Source/spec/两个patch、两配置、repomd/buildconfig SHA、HEAD、干净状态、项目锁、新根路径；默认只核验，`--run`才允许唯一一次GBS。与普通完整构建的历史指纹/16GiB准入无关，本轮使用docs/49 §1明确的重阶段10GiB准入、最多60分钟每5分钟一次；共享flock最长2h。18GiB/swap0、6/6/2、debuginfo-j4、nice15/ionice3保持。

复用build_llvm_x86_64.py的CMake/2GiB主机保护/30s采样/线程回收，新增可选disk_floor_bytes：每2秒检查新根父文件系统、低于30GiB即沿原stop_build停止scope，不删除文件。默认调用不带此项，原容量门禁不变；30GiB恰好允许。CMake仍要求15分钟内通过静态Release/Thin/O3/lld/断言OFF等，另逐项核对目标、projects、编译器、RTTI、6/2并发。

门禁测试：原构建测试加磁盘正负例共15项PASS；专用入口2项PASS（精确身份、错误身份/脏状态/复用根拒绝、双磁盘边界）。证据E6/build-guard-tests.log、certified-driver-tests.log、certified-input-preflight.json。

构建命令将在E6/full-build-scope/commands.log执行前完整echo，核心为：

```sh
python3 tools/run_certified_x86_release_build.py --run
# 内层：gbs -c E6/gbs-build.conf build -A x86_64 \
#   -B /var/tmp/llvm-optimize-x86-archivefix-20261013 --threads 1 \
#   --include-all --define '_smp_mflags -j4' \
#   -D E6/repository-preflight/buildconfig.conf E6/source
```

本节为启动前登记；不等于构建或新RPM验收通过。

## 9. 续六实际入口、辅助脚本缺陷与停止

### 9.1 一次GBS启动：尚未编译

19:21:02取得共享锁后以§8注册命令启动，启动准入10GiB和磁盘双门槛通过。GBS2.1.0于19:21:07进入export。新的tizen_base源码同时有`packaging/llvm.spec`和`packaging/libcxx-runtimes.spec`；专用入口漏传`--spec llvm.spec`，复用的GBS默认枚举了两个spec。进程原文（来自scope/process-memory.jsonl）：

```text
gbs export .../latest-base/source -o /var/tmp/llvm-optimize-x86-archivefix-20261013/local/sources/tizen_unified_standard/libcxx-runtimes-22.1.8-1 --outdir-directly --spec libcxx-runtimes.spec --include-all --packaging-dir=packaging
```

这是本任务构建辅助入口的范围选择缺陷，责任在入口，不是新快照、LLVM配方或Source失败。发现后向本任务驱动发送SIGINT，原stop_build停止该scope，19:22:00退出。只读诊断：`local/BUILD-ROOTS`不存在；全部2秒进程记录中rpmbuild、ninja、clang、lld/build进程观察数0；GBS日志只有准备/导出。没有用额外包的产物充当LLVM结果。证据E6/driver-spec-selection-stop.json、driver-spec-selection-diagnosis.json及full-build-scope原始日志。

本任务仅GBS入口1次；LLVM完整rpmbuild启动0次、CMake0次、RPM0个。新路径只留下GBS的sources/order/repos准备目录，不能称为完整LLVM构建树。

### 9.2 限定修正与重跑前磁盘失败

按辅助脚本条款，只补显式spec选择；不改Source/spec/config、优化参数、cap或门禁，第一次修正后尚未重跑：

```diff
--- a/tools/build_llvm_x86_64.py
+++ b/tools/build_llvm_x86_64.py
@@ -450,6 +450,8 @@
         command = ["gbs", "-c", str(args.config), "build", "-A", "x86_64", "-B", str(args.buildroot),
                    "--threads", "1", "--include-all", "--define", "_smp_mflags -j4",
                    "-D", str(chosen), str(args.source)]
+        if getattr(args, 'spec', None):
+            command += ['--spec', args.spec]
         if plan.get('certify_fingerprint'):
             completion_file = audit.directory/'gbs.exit'
             release_file = audit.directory/'gbs.release'
--- a/tools/run_certified_x86_release_build.py
+++ b/tools/run_certified_x86_release_build.py
@@ -113,7 +113,7 @@
         audit.json('registered-plan.json',plan)
         with (E/'gbs-invoked.json').open('x') as f:
             json.dump(dict(time=guard.stamp(),root=str(ROOT),head=HEAD),f)
-        guard.build(audit,SimpleNamespace(buildroot=ROOT,source=SOURCE,config=E/'gbs-build.conf'),
+        guard.build(audit,SimpleNamespace(buildroot=ROOT,source=SOURCE,config=E/'gbs-build.conf',spec='llvm.spec'),
                     plan,E/'repository-preflight/buildconfig.conf','systemd')
     except BaseException as error:
         audit.json('stopped.json',dict(time=guard.stamp(),error=repr(error))); raise
```

构建guard测试仍15项全部PASS，实际线程/进程模拟从10种扩为12种，新增显式llvm.spec命令检查与低磁盘自动中止/采样回收。专用入口2项全部PASS。完整输出E6/build-guard-tests-final.log、certified-driver-tests-final.log。这些只执行无害模拟，不启动GBS或编译；不是构建重试。

19:22:36重跑前再次检查/var/tmp：

|项|实际字节|GiB/结果|
|---|---:|---|
|可用|283,173,601,280|263.725967|
|1.2倍准入|283,208,338,637|263.758319|
|缺口|34,737,357|33.128125MiB，FAIL|
|可用减219.798599GiB预算|47,166,652,416|43.927368GiB，30GiB底线PASS|

两条规则必须同时满足，不能以只差约33MiB为由放宽1.2倍门槛，也没有把已导出载荷从冻结预算中自行扣除。导出阶段的临时磁盘写入已发生，现有目录全部保留；未删除任何内容，没有等待空间波动重判，没有执行第二次GBS。最终状态为`STOP_DISK_ADMISSION_AFTER_EXPORT_HELPER_ABORT`，不是LLVM编译失败或OOM。未来恢复需明确新一轮入口/新根策略，当前专用入口仍保留“根已存在/调用标记已存在即拒绝”，未开放任意重试。

### 9.3 实测资源的适用范围

以下仅是这次57.529877秒的导出入口；不代表完整LLVM构建时间/峰值：

|项|结果|
|---|---|
|scope配置|MemoryMax18GiB、MemorySwapMax0；nice15/ionice3|
|采样|30秒资源采样2条、2秒进程观察；运行中每2秒检查30GiB底线|
|采样到的cgroup MemoryPeak最大值|1,887,956,992B（1.758297GiB），仅采样下界|
|完整scope最终峰值|UNKNOWN：主动中止后scope已卸载；未伪造最终累计峰值|
|宿主采样最低MemAvailable|13,766,848,512B（12.821377GiB）|
|采样最低/var/tmp可用|283,112,337,408B（263.668911GiB）|
|进程VmHWM最高观察|git762,588KiB（源码导出），非clang/lld|
|memory.events|两次样本max/oom/oom_kill均0；无OOM报错，不能替代缺失的最终计数|
|GNU time -v|随主动中止未写出完整记录；不用空文件宣称已取得峰值|
|编译/链接/%install转换/打包耗时与峰值|N/A，全部未进入|

证据full-build-scope/{launch.json,outcome.json,samples.jsonl,process-memory.jsonl,memory-summary.json,stopped.json}。磁盘最低采样是全文件系统观察，不宣称所有变化都由本任务独占产生。启动后原初始准入线不是运行中止线；当时未低于30GiB，主动中止原因是spec选择错误，之后新的准入检查才失败。

## 10. 验收1–7、基线边界与替代方案

|验收项|本轮结果|
|---|---|
|1 身份/依赖、实际转换|候选spec/Source/补丁/HEAD及仓库宏PASS；新根未初始化，安装包归属/实际转换NOT RUN，整项未通过|
|2 install-post/execve、逐档llvm-strip、其他brp|NOT RUN|
|3 225开发档、45 compiler-rt、libarcher双归属|NOT RUN|
|4 同配方无补丁非归档基线|待PM裁决；新环境与历史基线不可比，未执行比较|
|5 宿主/Tizen消费者及运行库探针|NOT RUN|
|6 独立真实%install与同树SKIP|NOT RUN|
|7 ≥10成员直接非LTO结构诊断|本次新构建NOT RUN；此前60对认证证据不冒充本次结果|

验收4来源核查：docs/35的N、docs/38的N38及docs/13历史产物属于旧配方/旧Base环境；docs/36复原的是20260912.061113缓存。Rnew已装gcc14.2.0-1.10、binutils2.43-1.9、glibc2.40-1.10、rpm-build4.14.1.1-1.4，本次Base提供相同主版本但不同release（见§7.3）。当前目标又是cb679968叠加新PS3/PS2，不是原f111162e配方。即便个别工具NEVRA相同，也不能预先认定整套构建环境相同。此项不阻塞其他验收或交接，但本轮其他验收因未构建同样未完成。

供PM裁决的方案（**未授权执行、未运行**）：新构建成功后、BOLT交接前，保存完整构建证据；在同一根/同一已装依赖和BUILD中，用cb679968无两补丁的spec副本执行独立buildroot的真实`rpmbuild -bi --short-circuit --noclean`，不重编，比较其非归档安装文件与候选结果；如要求RPM层面，再另行批准经该RPM版本支持机制仅打包该树。不能把任意RPM拼装树代替真实%install，也不预先承诺`-bb --short-circuit`受该版本支持。含bitcode归档的原缺陷不作本项比较对象；所有非归档差异仍需解释，不自动放行。

预算仅供审批，不是本轮实测：docs/35 §4独立-bi曾耗时2,925.713秒，其中转换BEGIN–END1,939.927秒；当前无转换基线预计较少工作，但新环境/负载未知，建议预留30–90分钟，不作性能结论。历史独立安装父目录46.316360GiB（本页§2.2）；历史22 RPM合计8,857,390,396B（8.249088GiB）。若同时保留独立安装与一套RPM，可按1.2×两者之和预留约65.479GiB新增空间，并在其外保留30GiB；这只是历史载荷预算，正式执行前须按新树重算，不能作为降低完整构建准入的理由。

## 11. 交接与后续状态

BOLT为**NOT_READY**：没有新BUILD、ThinLTO缓存、构建完成时间或新RPM验收；不得使用本次仅导出的目录冒充交接树。原定完整根仍为`/var/tmp/llvm-optimize-x86-archivefix-20261013`；快照/repomd与spec/Source/候选身份已在§7–§8登记，只有完整构建和验收1–3、5–7通过后才可交接并承诺不再写树。

两ARM全量/根内小试/64MiB负例、bash依赖清单、LLVM23探测均未执行；遵循先完成debug主线构建验收的顺序。发布模式60对认证PASS沿用；发布模式完整构建继续挂账。

## 12. 回收、保护与交付

19:22:00共享重任务锁释放；19:26:04终检本任务构建进程0、采样器已回收、临时挂载0、两项目锁0，共享锁可获取。14项保护文件SHA全部与开场一致（含两Source/Commands所在文件、比较器、配置、W spec、已上传及新候选补丁）。未访问/修改BOLT资产，未清理磁盘，未推Gerrit。证据E6/lock-released.json、cleanup-final.json、final-integrity.json、stop.json。此处“回收”仅进程/锁/线程，不删除证据目录。

本轮交付：本页、STATUS、build_llvm_x86_64.py及测试、专用run_certified_x86_release_build.py及测试；原始数据/专用配置/diff保存在E6。仓库变更不含用户的gbs_llvm.conf修改。报告小于50KB；全部结果以本节最终停止为准，§8是启动前登记。

## 13. 续七：授权范围、开场与删除前盘点

2026-10-13开场main=`9e7448d4a8f88331b730075cf78fbc21add8cf4e`。新证据E7=`temp/release-x86-full-build-20261013/round2`，第一轮E6原文、调用标记与结果全部保留。项目锁19:33:38取得；主仓库仅用户既有gbs_llvm.conf修改；冻结Source/Commands所在文件、比较器、W spec、候选/已上传补丁及E6专用配置/构建输入SHA全部一致。MemAvailable=13,744,197,632B，超过轻任务6GiB准入。原始核查E7/initial-integrity.json；本轮未修改任何代码或配置。

### 13.1 本轮人工裁决（运行前）

1. 仅批准删除`/var/tmp/llvm-optimize-x86-archivefix-20261013`整目录；须先登记清单/占用并核查没有BUILD-ROOTS、rpmbuild产物、19:21:00之前的文件和使用进程。授权不包括GBS可能使用的目录外临时文件或任何其他目录。
2. 通过磁盘双准入才用原修正入口显式`--spec llvm.spec`执行第二轮；第二轮独立证据与独立一次性调用标记，第一轮记录不动；第二轮失败不重试。
3. 验收4同环境基线已获有条件批准：其余验收通过后、BOLT交接前，cb679968原样spec独立buildroot执行真实`-bi --short-circuit --noclean`，不打RPM。执行前ninja-n无编译/链接待办、运行中出现clang/lld编译链接即中止；可用须≥1.2×46.316+30=85.5792GiB，不足则保持待PM并交接。逐文件记录差异，不自动放行；完成比较并存清单/SHA后删除该独立buildroot。验收4结果不阻塞BOLT交接。
4. 其余资源与保护沿用；本轮没有扩展删除范围、调整预算或修改Source。

### 13.2 实际目录内容

**实际没有大体积导出载荷：普通文件0、软链接/特殊文件0，只有包括根本身的15个空准备目录。** `du -sx -B1`为61,440B，逐inode的st_blocks×512合计同值；逻辑文件载荷0。完整绝对路径、mode/dev/inode/size/blocks/mtime_ns/mtime/type已保存在E7/aborted-root-full-inventory.json；不存在未登记的普通文件。

|相对批准根的路径|目录占用B|mtime（+08:00）|
|---|---:|---|
|`.`|4096|2026-10-13T19:21:06.983871+08:00|
|`local`|4096|2026-10-13T19:21:06.984270+08:00|
|`local/order`|4096|2026-10-13T19:21:06.983871+08:00|
|`local/repos`|4096|2026-10-13T19:21:06.984203+08:00|
|`local/repos/tizen_unified_standard`|4096|2026-10-13T19:21:06.984203+08:00|
|`local/repos/tizen_unified_standard/x86_64`|4096|2026-10-13T19:21:06.984346+08:00|
|`local/repos/tizen_unified_standard/x86_64/RPMS`|4096|2026-10-13T19:21:06.984270+08:00|
|`local/repos/tizen_unified_standard/x86_64/SRPMS`|4096|2026-10-13T19:21:06.984270+08:00|
|`local/repos/tizen_unified_standard/x86_64/logs`|4096|2026-10-13T19:21:06.984270+08:00|
|`local/repos/tizen_unified_standard/x86_64/logs/fail`|4096|2026-10-13T19:21:06.984203+08:00|
|`local/repos/tizen_unified_standard/x86_64/logs/success`|4096|2026-10-13T19:21:06.984203+08:00|
|`local/sources`|4096|2026-10-13T19:21:06.984270+08:00|
|`local/sources/tizen_unified_standard`|4096|2026-10-13T19:21:07.577871+08:00|
|`local/sources/tizen_unified_standard/cache`|4096|2026-10-13T19:21:06.984270+08:00|
|`local/sources/tizen_unified_standard/libcxx-runtimes-22.1.8-1`|4096|2026-10-13T19:21:07.576871+08:00|

没有BUILD-ROOTS或任何rpmbuild产物；最早mtime也晚于19:21:00。mountinfo没有根内挂载。对可见/proc进程的cwd/root/exe/fd及相关构建命令检查，没有发现本项目竞争进程或指向该根的引用。**可见性限制必须保留：其他身份进程有299组cwd/root/exe、298组fd字段无法读取，未提权；本轮不能声称对这些字段完成了全宿主无盲区验证。** 实际删除只用空目录rmdir，不递归删除载荷；目录若新出现内容即失败，不会把未登记文件一并删掉。证据E7/aborted-root-delete-precheck.json、mountinfo-before.txt、aborted-root-du.txt。

### 13.3 删除执行与空间复查

删除前再次核对完整清单及inode/dev；确认本次清单全是空目录后，按深度倒序`Path.rmdir()`，删除范围精确止于批准根。没有使用扩大的rm范围，未删任何其他目录或文件。

19:34:37完成，根已不存在：

|项|实际字节|GiB/结果|
|---|---:|---|
|删除前/var/tmp可用|283,173,654,528|263.726017|
|删除后/var/tmp可用|283,173,715,968|263.726074|
|实际变化|61,440|60KiB|
|已删除|0文件、15目录|仅获批根|
|1.2倍准入|283,208,338,637|263.758319|
|准入缺口|34,622,669|33.018750MiB，FAIL|
|减历史写入预算236,006,948,864B后|47,166,767,104|43.927475GiB，30GiB底线PASS|

获批根不含上一轮导出阶段观察到的大载荷，因此删除该根只释放60KiB，不能把整个文件系统此前约数GiB变化当作本次删除收益。本轮未追查、未删除目录外载荷，也没有把剩余缺口从冻结准入值中扣除。两条门槛须同时满足；1.2倍失败即停止，没有等待自然波动后再判。证据E7/delete-result.json、check_and_remove_aborted_root.py。

## 14. 续七停止、验收和后续状态

最终状态`STOP_DISK_ADMISSION_AFTER_APPROVED_EMPTY_ROOT_DELETE`。第二轮GBS没有启动，也没有创建新的调用标记；E7仅盘点/删除/完整性/停止证据，没有full-build-scope。第一轮E6/gbs-invoked.json仍保持19:21:02的记录，SHA/bytes/mtime随final-integrity.json留证，未修改或清空。修正后的原入口/候选/两仓库身份均未改；今后启动仍需独立注册第二轮调用标记与目录，不能复用第一轮标记绕过一次性限制。

|要求|本轮结果|
|---|---|
|第二轮完整构建|NOT RUN，调用0次，根在批准删除后不存在|
|CMake/编译/链接/%install转换/打包耗时|N/A，未启动|
|构建cgroup峰值/进程VmHWM/构建磁盘峰值|N/A，无构建scope；上述磁盘是盘点时读数|
|验收1 身份/安装依赖|冻结候选身份复核一致；新根安装/工具归属NOT RUN，整项未完成|
|验收2 完整install-post/逐档strip|NOT RUN|
|验收3 开发归档/运行库/libarcher|NOT RUN|
|验收4 同环境未打补丁安装基线|已获有条件批准，但未到其余验收通过的执行时点，NOT RUN；不是新基线比较失败|
|验收5 宿主/Tizen/运行库消费者|NOT RUN|
|验收6 独立真实安装与同树SKIP|NOT RUN|
|验收7 跨子系统直接编译结构诊断|本轮NOT RUN|
|BOLT交接|NOT_READY，无新BUILD/ThinLTO缓存/完成时间，未交接|
|两ARM全量、根内小试与64MiB负例|NOT RUN|
|bash依赖、LLVM23探测|NOT RUN|
|发布模式完整构建|仍挂账；既有60对发布认证PASS不变|

## 15. 续七回收与交付

项目锁已释放，19:35:53终检本任务进程0、临时挂载0、项目锁0；未取得共享重任务锁、未启动采样器，未干扰BOLT。完整性核对保留全部冻结文件和第一轮证据；新证据目录位于W/temp，未提交载荷。E7/{lock-acquired.json,lock-released.json,cleanup-final.json,final-integrity.json,stop.json}记录回收与边界。

本轮只提交本页与STATUS，没有修改Source、Commands、比较器、spec、配置、候选补丁或构建入口；未做编译/打包、未推Gerrit。报告与STATUS同提交推送GitHub main，报告不超过50KB。历史§1–§12保持原结果，当前结论以§13–§15为准。


## 16. 续八：导出临时目录定位、授权清理与第二轮准入

开场main=da4b69b6f66f14cc8a516d4807433f8d7d48969b；E8=`temp/release-x86-full-build-20261013/round2-launch`。14项冻结文件SHA与此前登记一致，用户gbs_llvm.conf修改未纳入提交；两项目锁19:44:58取得。仅盘点/清理本轮指定范围，旧E6/E7证据及第一轮调用标记保留。

### 16.1 盘点与归属

19:20以后mtime或ctime变化的顶层条目共4个，均属linhao。完整元数据E8/top-level-stat.json，删除前逐文件清单E8/delete-full-inventory.jsonl（184,853条），大小统计delete-inventory-summary.json；不跟随符号链接、不跨文件系统。

|/var/tmp顶层名|mtime=ctime（+08）|du字节|普通文件数|归属与处理|
|---|---|---:|---:|---|
|.gbs_export_3hy1gs20|19:21:14.563871|233717760|11|llvm.spec、Source及5个配方文件与本轮PS2 checkout逐字节相同；导出载荷，已删|
|.gbs_export_xyqf69nu|19:21:40.902833|12288|1|libcxx-runtimes.spec只有GBS追加VCS行，指向4c36e899…-dirty；去该行与本轮checkout相同，已删|
|gbp_qpdqpzal|19:21:41.188872|2607124480|169020|第一轮19:21:43 PID2024061的tar -C明确指向其dump_tree_cgrm8h2n；内容为LLVM源码树，已删|
|linhao-gbs|19:21:06.849912|233472|17|持久GBS配置目录，含多个其他任务配置；**保留**|

身份原文：E8/export-content-identity.json、first-export-process-paths.json。三个删除对象均满足19:21:00–19:22:10、属主、归属三条件；更早gbp/.gbs_export目录不触碰。挂载检查无后代挂载；可读/proc cwd/root/exe/fd无使用引用。保留可见性限制：其他身份的297组cwd/root/exe、296组fd目录与135个fd链接无法读取，未提权；不能声称全宿主无盲区。删除前对全部条目的inode/dev/size/mtime/ctime重核一致。证据mountinfo-before-delete.txt、process-reference-check.json、clean_aborted_export.py。

### 16.2 删除与磁盘

19:49:56–19:49:57只删除表中三项。/var/tmp可用从283075473408B（263.634579GiB）到285916327936B（266.280189GiB），增加2840854528B（2.645610GiB），与三目录du合计相同。证据deletion-result.json。未删linhao-gbs或其他目录。

运行前PM批准的一次性规则：正常263.758319GiB准入未通过时，仅第二轮可在短缺≤1GiB且可用减219.798599GiB≥40GiB的交集内放行；30GiB实时底线不变。本轮清理后正常准入已满足，**未动用放宽**。实际启动前仍在共享锁内复查内存/磁盘，结果写full-build-scope/disk-admission.json。

### 16.3 第二轮入口登记

仍使用§7–§8冻结配置/快照/PS3/PS2/Source/完整checkout；GBS显式`--spec llvm.spec`。辅助入口新增`--round 2`，仅改变本次session身份、证据目录和一次性标记（E8/gbs-invoked-round2.json），首轮E6不改；normal路径没有放宽。4项测试PASS：原身份/新根约束、正常磁盘界限、第二轮≤1GiB及40GiB双边界、两轮标记隔离。测试日志E8/driver-tests.log；本地冻结身份与准入预检E8/local-preflight.json。

资源继续18GiB/swap0、6/6/2、debuginfo-j4、nice15/ionice3、共享flock、每2秒30GiB磁盘底线、宿主可用<2GiB中止。重阶段内存准入按本系列§1的10GiB，5分钟检查/最多60分钟；并非更改普通完整构建入口。另以独立观察器每10秒登记本轮新建gbp/.gbs_export顶层临时目录路径/du，仅观察新条目，不改文件。验收4条件及不阻塞交接沿用§13.1；本节不宣称构建或验收已完成。
