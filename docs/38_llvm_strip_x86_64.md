# 38 LLVM x86_64 打包改用 llvm-strip：磁盘准入停止记录

日期：2026-10-09（Asia/Shanghai）。起点主仓库 `25e2b1894903c40af9aeaa3e4c158c4e95674dc2`。
已先读 STATUS、docs/34、docs/35、docs/36；docs/25–37 保留不动。

**本轮在第零步磁盘准入停止，没有启动增量构建。**
原构建根所在 `/home` 可用 50.800056 GiB；
即使清空全部允许的本根 LTO cache，上界也只有 50.816586 GiB，
仍比原 60 GiB 门槛少 9.183414 GiB。
允许删除的独立安装树位于另一个 SSD 文件系统，删除它不能增加 `/home` 可用空间。
没有降低门槛、迁移构建根、删除其他产物，或在不足的空间上尝试构建。

**已完成的本轮证据：** docs/35 的 22 RPM SHA/大小全部匹配；
N 的 17,689 个包内路径类型、模式、大小、SHA/软链接目标全部匹配 docs/35，额外非目录文件 0；
宏链只读核查支持“当前开 debuginfo 的 LLVM 包中，改变 `%__strip` 只影响静态归档后处理”。
后者不是本轮新 RPM 及运行库消费者的动态验收。

**未完成：** 新 spec 三行未应用，原 S/root spec 均保持原值；增量构建、新 RPM、225/45 归档验收、
七项宿主消费者、sanitizer/profile/builtins 消费者、Tizen 测试包、叠加提交补丁均 **NOT RUN**。
未以 docs/34 的旧结果代替本轮新增消费者证据，也未生成可提交的 llvm-strip change。

## 0. 范围、身份和独占

用户确认归档修复已上传 Gerrit **356627 patchset 2**，提交前缀 `67619ec8bbba`，
父提交 `cb67996861d0`；本轮原计划生成其后的独立 x86_64 change。
这是用户提供的已知状态；由于本轮在前置门禁停止，**没有执行第三步 fetch，未冒称独立核验了远端 patchset 身份**。
平台已全量转 LLVM 编译作为用户前提使用，不重新论证。

| 别名 | 路径 |
| --- | --- |
| W | `/home/linhao/Toolchain/development/llvm-optimize` |
| E | `W/temp/llvm-strip-x86_64-20261009`，本轮原始证据；以下未加前缀的文件名均相对 E |
| C | `W/temp/archive-fix-v2-final-20261009/continue-20261009`，docs/35 证据 |
| S | `W/temp/llvm-archivefix-trial`，隔离试验分支 |
| Rnew | `W/temp/gbs-root-x86_64-archivefix-v2` |
| R | `Rnew/local/BUILD-ROOTS/scratch.x86_64.0` |
| B | `R/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build` |
| N | `W/temp/toolchain-archivefix-v2-final`，本轮要求的非静态库对照，未改 |
| 允许清理的独立安装树 | `/var/tmp/llvm-optimize-archivefix-v2-final-20261009/independent-install` |

开场 `git status --porcelain` 为空；项目竞争进程清单为空。
独占锁：`Rnew/.llvm-optimize-exclusive.lock`，以 O_EXCL 取得；
session=`tizen-consumer-8bfba4d3e58a406b8df7df7a05debdc6`，PID=475398，开始 `2026-10-09T18:34:19.331085+08:00`。
沿用历史锁工具，因此 session 字符串的前缀仍是 tizen-consumer，不代表启动了消费者任务。
证据：`processes-start.json`、`lock-acquired.json`；结束时释放锁，见 `lock-released.json`。

| 输入 | 核查值 |
| --- | --- |
| S HEAD | `f111162e94aa48ed367c9d2c039456c70e7160ae` |
| S 分支 | `archive-fix-trial` |
| S/packaging/llvm.spec SHA | `6a91a0bf3d8d2044473662b65ed3d32d4696a697ccd52200d983ce4334aeafdf` |
| S Source SHA | `6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557` |
| R/.../SOURCES/llvm.spec SHA | `91f684691eb35af52b1a9f2a2cba478f88dbfd8a48b4c2281dac6144d71d3bd0` |

S spec 仍是 docs/35 登记的 `6a91a0bf…`，Source 未变。
本轮没有把以下拟议三行写入 S 或 R，故**不存在已应用的新 spec SHA 或新实测 spec diff**：

```spec
%ifarch x86_64
%define __strip %{_bindir}/llvm-strip
%endif
```

磁盘门禁在编辑前即确认不能满足；本轮也没有改 W/llvm、gbs_llvm.conf、Source 或既有认证指纹。
保护文件摘要：`protected-start.json`、`final-integrity.json`。

### 0.1 22 RPM 与 N 复核

逐个读取 R 内 22 个 RPM，比较 `C/rpm-inventory.json` 中 SHA256 和字节数：22/22 PASS，见附录 A。
对 N 逐路径读取内容并与 `C/rpm-file-comparison.json` 的 `new` 元数据比较：

```text
RPM_IDENTITY_PASS 22
N_IDENTITY_PASS 17689
mismatches = 0
extra_non_directory_paths = []
```

包括 225 开发静态库、45 compiler-rt 和全部非静态库文件，没有只抽查三工具。
完整记录 `rpm-identity.json`、`N-files.json`、`N-identity.json`、`identity-result.json`、`precheck.log`。
只读核查工具在 RPM 摘要阶段曾中断，以补齐元数据比较器的目录/软链接 size 字段，再完成核查；
初版脚本/日志保留为 `precheck-initial.py`、`precheck-initial.log`。没有发生真实产物身份门禁失败或构建重试。

## 1. `%__strip` 作用范围：只读核查

### 1.1 全部宏引用及有效调用链

递归检索 R 的 `/usr/lib/rpm`、`/etc/rpm`、`/home/abuild/.rpmmacros`，
`all-strip-macro-references.stdout` 保留 201 行 `__strip` 相关原文，包括所有架构的未生效定义。
其中 65 个 platform 文件各有三个 strip 调用行，共 195 行；不能把其他架构文件当成当前有效宏。
当前 x86_64 宏使用点如下（路径相对 R）：

| 文件:行 | 内容/作用 | 开 debuginfo 时 |
| --- | --- | --- |
| `usr/lib/rpm/macros:83` | `%__strip /bin/strip` 默认值 | 当前仍为此值，本轮未改 |
| `usr/lib/rpm/platform/x86_64-linux/macros:72–74` | 默认 os-install-post 中 brp-strip / static-archive / comment-note 各传 `%__strip` | 后续 Tizen 宏重定义该链，不能直接按这三行判实际执行 |
| `usr/lib/rpm/tizen/macros:34–38` | 重定义 strip-install-post | 此处是有效 strip 链；该文件是 `../tizen_macros` 的软链接 |
| `usr/lib/rpm/tizen/macros:35` | brp-strip 受 `!__debug_package` 条件约束 | 条件不成立，不运行 |
| `usr/lib/rpm/tizen/macros:36` | brp-strip-static-archive 传 `%__strip` | **唯一实际使用 `%__strip` 的 strip 调用** |
| `usr/lib/rpm/tizen/macros:37` | brp-strip-comment-note 传 `%__strip` | 行首 #，不运行 |
| `usr/lib/rpm/tizen/macros:40–46` | compress、未禁用时 strip 链、python-hardlink、find-docs | 除 strip 链外不读 `%__strip` |
| `usr/lib/rpm/tizen/macros:53–60` | 有 debug-package 时先 debug-install-post，再 arch/os/isu/检查器链 | debug-install-post 与 `%__strip` 的静态库调用独立 |

根内只读查询以 abuild 执行；用于展开后处理宏的 `__debug_package=1` 显式模拟已确认的 debuginfo 状态，
不是向 spec 写入新定义或运行安装脚本。docs/35 §3.2 的真实日志亦证明独立 brp-strip 为 0 次、
static-archive 为 1 次。查询原文：

```text
STRIP=/bin/strip
STRIP_POST=

    /usr/lib/rpm/brp-strip-static-archive /bin/strip
#    /usr/lib/rpm/brp-strip-comment-note /bin/strip /bin/objdump
```

完整 argv/输入：`macro-query-input.sh`、`commands.jsonl`；stdout 为 `macro-query.stdout`。
`brp-strip-static-archive:7` 从第一个参数取 STRIP，:15–20 扫描排除 debug 目录的普通 ar 并执行 `$STRIP -g "$f"`。
所以未来三行覆盖对该链的预期变化是参数从 `/bin/strip` 换成 `/usr/bin/llvm-strip`；
此次没有构建，**没有新的“270 档全部 exit0”执行证据**。
该脚本没有逐档退出码聚合，后续验收也不能仅凭脚本或 RPM 总退出码 0 声称 270 次均成功。

### 1.2 find-debuginfo 的工具与来源

`usr/lib/rpm/macros:182–196` 的 debug-install-post 调用 find-debuginfo，并传 `_smp_mflags`；没有传 `%__strip`。
`usr/lib/rpm/find-debuginfo.sh:248–285` 中，普通 ELF 在 `STRIP_DEFAULT_PACKAGE != binutils` 时执行：

```sh
eu-strip --remove-comment $g $strip_option -f "$1" "$2" || exit
```

该调用在 :275。:269 是内核模块分支的 eu-strip；:277–280 是显式选择 binutils 时的
strip/objcopy 后备分支，它同样不读取 RPM 的 `%__strip` 宏。
本根 abuild 查询 `STRIP_DEFAULT_PACKAGE=UNSET`，本 spec 不改该变量；因此本配置选择 eu-strip。
来源为根内 `rpm -qf` 实际输出：

```text
/usr/bin/eu-strip                         elfutils-0.189-1.10.x86_64
/usr/bin/llvm-strip                       llvm-22.1.8-1.6.x86_64
/usr/lib/rpm/find-debuginfo.sh             rpm-build-4.14.1.1-1.4.x86_64
/usr/lib/rpm/brp-strip-static-archive      rpm-build-4.14.1.1-1.4.x86_64
```

原输出、所有所读宏/脚本/工具 SHA 在 `macro-query.stdout`、`macro-inputs.json`，带行号全文在 `*.numbered.txt`。
**作用范围结论限本 LLVM spec 开 debuginfo、当前宏链与环境**；不是平台所有 RPM 或关闭 debuginfo 时的普遍结论。

## 2. 磁盘门禁与授权清理上界

资源读取时间 `2026-10-09T18:37:01.759341+08:00`。内存准入通过：MemAvailable=22,951,632,896 B
（21.375374 GiB ≥16 GiB）。磁盘是本轮唯一已发现的准入阻塞。

| 项目 | 实测 |
| --- | ---: |
| 原门槛 | 64,424,509,440 B = 60 GiB |
| B 所在 `/home` 可用 | 54,546,145,280 B = 50.800056 GiB |
| cache 逻辑字节 | 14,973,928 B |
| cache 条目数 | 60 |
| cache 完整分配空间回收乐观上界（含目录） | 17,747,968 B |
| 假定全部 cache 都释放后的 `/home` 可用上界 | 54,563,893,248 B = 50.816586 GiB |
| 即使清空 cache 仍短缺 | 9,860,616,192 B = 9.183414 GiB |
| SSD 独立安装树分配字节 | 49,713,315,840 B |
| 独立安装树常规文件/目录/软链接 | 16397 / 1290 / 39 |

`df -B1` 原始输出（与随后 disk_usage 读数相差 28,672 B，属于两个连续采样时点）：

```text
Filesystem         1B-blocks          Used    Available Use% Mounted on
/dev/sda1      1967844950016 1813262163968  54546173952  98% /home
/dev/nvme0n1p1  501809635328   85490352128 390753480704  18% /
```

B 的 st_dev=2049（/dev/sda1），独立安装树 st_dev=66305（/dev/nvme0n1p1），
两者不同；没有把根 SSD 的 364 GiB 可用空间算进 `/home`。
既然两项授权清理都不能使原构建根达到 60 GiB，**没有做无助于准入的删除**，两项均完整保留。
没有删除 N、基线 H、任何历史 RPM 或证据；没有自行把 Rnew 迁到 SSD，也没有在达到门槛前启动 `-ba --noprep`。

`cache-inventory.json` 记录每个缓存条目的路径、inode、设备、nlink、大小、分配块数、mtime。
上界连硬链接等可能不能实际回收的块也计入，仍不够，故这是有利于准入的乐观上界而非低估。
`resource-admission.json`、`df-*.log`、`free-bytes.log` 是完整判据。
需要在**同一文件系统**额外取得至少上述约 9.184 GiB（这是已假设清空 cache 的下界），并重新检查实际可用≥60 GiB，
或由用户另行决定存储方案，才能继续；本轮没有自行扩大清理范围。

## 3. 后续步骤状态

| 用户要求 | 本轮状态 |
| --- | --- |
| 项目锁、无竞争进程、22 RPM/N 身份 | PASS |
| `%__strip` 全部使用点、eu-strip 来源 | 已完成只读核查，见 §1 |
| 试验 spec 仅增加三行，记录新 SHA/diff | NOT APPLIED；磁盘门禁先停止，原 spec 保持 docs/35 配置 |
| 一次 -ba --noprep，16/18 GiB、swap0、6/6/2、debuginfo4 | NOT RUN；0 次入口，没有启动 scope/Ninja/转换/后处理 |
| 新 22 RPM inventory 与 temp/toolchain-llvm-strip | NOT CREATED；该目录未创建 |
| 225 开发归档格式/索引/次序/分段 | NOT RUN；现有 N 身份 PASS 不代替新产物验收 |
| 45 compiler-rt SHF_ALLOC 类型/flags/size/content、索引、无调试节、结构类别 | NOT RUN；docs/34 §1.3 为历史记录，不重判为本轮 PASS |
| 非静态库逐字节同 N；270 次 llvm-strip exit0 | NOT RUN |
| 七项宿主消费者 | NOT RUN |
| 宿主/Tizen × bfd/lld 的 ASan 坏/好、UBSan、profile merge、builtins | NOT RUN；运行库被真实消费是否正常，本轮 UNKNOWN |
| docs/36 同类 Tizen 静态库消费者 bfd/lld | NOT RUN |
| fetch 356627/2，单提交 format-patch、apply --check | NOT RUN；无新 Change-Id，无 patches/llvm-strip 补丁 |

不对 llvm-strip 方案给出本轮验收通过结论，也不称 compiler-rt 消费者失败；它们根本没有运行。
项目锁已回收，无构建或采样器遗留；只读身份核查全部结束，收尾见 `final-integrity.json` 和 `lock-released.json`。

## 附录 A：作为本轮对照的 22 RPM 身份

下表是 **docs/35 的既有 RPM 本轮复核**，不是本轮新产物。
原文件均在 `R/home/abuild/rpmbuild/RPMS/x86_64/`；完整路径在 `rpm-identity.json`。

| 文件 | 字节 | SHA256 | 对照 docs/35 |
| --- | ---: | --- | --- |
| `clang-22.1.8-1.x86_64.rpm` | 310,019,538 | `82970941d586e91861ebe5afe7d0c99db98e6142bd77e5c2b9d6aaf44c2e2604` | PASS |
| `clang-debuginfo-22.1.8-1.x86_64.rpm` | 2,928,315,838 | `1a4dfce12b39e2c4f667b995dbedf0098eb17afc955c76f38b02f00c30e13266` | PASS |
| `clang-devel-22.1.8-1.x86_64.rpm` | 4,099,162 | `17974fc8ca91902fe2e567003d051bbfd66f98001ea33ad6da3bfbabd951e59c` | PASS |
| `clang-devel-debuginfo-22.1.8-1.x86_64.rpm` | 5,728,882 | `f8724e453f170815bca1e85db3776bc88d59756cb13b1765ad4898b9cb885e01` | PASS |
| `compiler-rt-22.1.8-1.x86_64.rpm` | 3,721,870 | `4264edddd7f29f7bd3f00570569ac86107f56189113208590d41e9598bd689e7` | PASS |
| `compiler-rt-debuginfo-22.1.8-1.x86_64.rpm` | 1,289,498 | `b473f81452b0de80b726f4f910654b24370d447b92d2c71279d29631f9a314ed` | PASS |
| `libllvm-22.1.8-1.x86_64.rpm` | 23,649,450 | `3382c1eb11516f54e62d933c77193c188a11c792ff906dbc3792806c86772d05` | PASS |
| `libllvm-debuginfo-22.1.8-1.x86_64.rpm` | 198,056,974 | `f2fb22953807c2f386ebd5980e9a12133979ff4b740b946d6a20d58f81fee3fc` | PASS |
| `libomp-22.1.8-1.x86_64.rpm` | 373,462 | `88a057dd1d70cd92eaedeb60daaca00d674d70d1c2f3268bff4f53cfe86cbeb5` | PASS |
| `libomp-debuginfo-22.1.8-1.x86_64.rpm` | 1,142,202 | `874e533d8059bcc084c8d2d76f1a2530b72f1f129f350505ead52fc26832b6cd` | PASS |
| `libomp-devel-22.1.8-1.x86_64.rpm` | 25,522 | `89f4dfced1682786e607cc27feaf4a501d09c112edf8ca84a12a30ca70dbfce8` | PASS |
| `lldb-22.1.8-1.x86_64.rpm` | 30,767,594 | `221a36caaf8a200970b70268a0031418043b11821f724a4b2ee56a545cba8d99` | PASS |
| `lldb-debuginfo-22.1.8-1.x86_64.rpm` | 332,844,394 | `d96b6e91b766e27bbc662684f13cc7d58f9d5950aaca3a3c5dce5837145f27dd` | PASS |
| `lldb-devel-22.1.8-1.x86_64.rpm` | 30,525,214 | `4ee2c13f43c48c5139822959ca5d7966206df6d9531f0c80eab5d11782646b0e` | PASS |
| `lldb-devel-debuginfo-22.1.8-1.x86_64.rpm` | 279,580,554 | `7364d0d3a3289c848180d4601c4b5cd8f603c466b0507d6ce8ae3d69d8a62645` | PASS |
| `llvm-22.1.8-1.x86_64.rpm` | 410,661,042 | `476ee724108ab0420014b098f94551ea7b34224bd60a20bff91039f5b604e88e` | PASS |
| `llvm-debuginfo-22.1.8-1.x86_64.rpm` | 3,842,665,274 | `b52898d90215ae0eb116c3438bb65333adf70fa391a78e8dd6f732f5187f94c7` | PASS |
| `llvm-debugsource-22.1.8-1.x86_64.rpm` | 43,654,074 | `c3934936973840ec76de6c1933cf5da90458d823456ef513d3c48b4a92c3cab5` | PASS |
| `llvm-devel-22.1.8-1.x86_64.rpm` | 41,190,542 | `f9a6cc22e5cde49373f277b8b8b641bde4171b1f543fbe3b7bd2dab4a7889d62` | PASS |
| `llvm-devel-debuginfo-22.1.8-1.x86_64.rpm` | 308,603,382 | `a0a5ea2e037f87bfc55657bc575287f42e083e309df5ccab42eabd7f655944ef` | PASS |
| `llvm-static-devel-22.1.8-1.x86_64.rpm` | 60,439,606 | `4c0c72613ac6772730475fddf642257da5f28adf3a026b60d5888c4abbfb3c06` | PASS |
| `python-clang-22.1.8-1.x86_64.rpm` | 36,322 | `3e9ffa2c6e85ae6242956b3ddec511a8efb24822e6c4f127db66cbf6cb80ad99` | PASS |

## 附录 B：证据和自检

证据目录绝对路径：`/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-strip-x86_64-20261009`。
原始文件保存在 temp，不上传；本报告与 STATUS 同 commit 推送 GitHub。

- `precheck.py`、`precheck.log`、`rpm-identity.json`、`N-files.json`：原产物完整只读身份核查。
- `macro_audit.py`、`commands.jsonl`、`all-strip-macro-references.stdout`、`macro-query.stdout`、`macro-inputs.json`：宏链与工具来源。
- `resource-admission.json`、`cache-inventory.json`、`df-*.log`、`free-bytes.log`：磁盘不足及允许清理无助于准入的依据。
- `protected-start.json`、`final-integrity.json`、`lock-acquired.json`、`lock-released.json`：现场和回收。

自检：增量/完整构建均 0 次；测试包 0 次；spec/Source/配置/认证指纹改动 0；
删除文件 0；未访问隔离旧混合根；未推 Gerrit；未生成未经验证的 llvm-strip 提交补丁。
