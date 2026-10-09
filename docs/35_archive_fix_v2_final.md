# 35 归档修复 v2：提交配置恢复、增量续跑与验收

日期：2026-10-09（Asia/Shanghai）。本轮起点 `f49a56159e6a144e7aa413b67641f87e4b403bca`；
docs/25–34保持不动。本报告与STATUS同一提交更新，原始证据仅保存在本机。

**结果：增量续跑、新RPM前四项、独立安装幂等两步与七项宿主消费者全部PASS；在Tizen bfd测试包的依赖解析阶段STOP。**
固定Base快照的repomd在本轮只读核查中返回HTTP404；测试根没有创建，编译/链接/%check均未执行。
按“任一步失败即停，不改后重试”，没有启动lld测试包，没有生成或覆盖v2最终format-patch。
这不是归档消费者链接失败，也不是OOM；Tizen原生消费者兼容性在本轮仍未确证。

## 0. 范围、前次停止与本轮清理

本轮使用标准GNU strip的提交配置，Source和6/6/2并发不变；只执行原构建根的一次
`rpmbuild -ba --noprep`，不进行完整重建。不改W/llvm与其spec，不访问隔离旧混合根。

### 0.1 路径

| 别名 | 路径 |
| --- | --- |
| W | `/home/linhao/Toolchain/development/llvm-optimize` |
| E35 | `W/temp/archive-fix-v2-final-20261009`，f49a561停止现场保留 |
| C | `E35/continue-20261009`，本轮新证据；以下未加前缀的证据路径均相对C |
| E34 | `W/temp/archive-fix-v2-build-20260929`；U34=`E34/resume-20261008` |
| S | `W/temp/llvm-archivefix-trial`，分支`archive-fix-trial` |
| Rnew | `W/temp/gbs-root-x86_64-archivefix-v2` |
| R | `Rnew/local/BUILD-ROOTS/scratch.x86_64.0` |
| B | `R/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build` |
| H | `W/temp/archive-index-fix-rpm-20260923/baseline-rpm-extract`，docs/13基线 |
| N | `W/temp/toolchain-archivefix-v2-final`，本轮22个新RPM解包 |

### 0.2 f49a561的停止历史

前次已恢复提交配置，但未启动构建：磁盘只有18.761GiB，允许清理的缓存全部删除后理论上仍只有54.724GiB，
低于原60GiB门槛。当时未删除缓存或其他目录，也未做RPM验收。原报告副本为`C/docs35-at-f49a561.md`，
原准入记录为`E35/resource-admission.json`等文件。旧FAIL/STOP不追溯改判。
本轮用户随后单独授权下述三项清理，才重新进入原门槛；没有降低门槛。

### 0.3 授权清理清单

| 对象 | 删前记录 | 实际处理 |
| --- | --- | --- |
| `W/temp/toolchain-archivefix-v2`作废解包 | 17,723路径；16,397常规文件、39软链接、1,287目录；逻辑49,626,144,207 B，独占分配49,667,145,728 B | 整个指定目录删除 |
| R内上一轮22个二进制RPM及1个SRPM | 22个RPM逐一与E34 inventory SHA相同；23个文件共9,197,486,454 B | 仅登记文件删除 |
| `B/lto.cache/llvmcache-*` | 20,872文件；逻辑38,572,354,832 B，分配38,614,765,568 B；均为单硬链接 | 清单与前次E35登记完全相符，每个文件按inode/大小/mtime再次核验后删除 |

SRPM为`llvm-22.1.8-1.src.rpm`，340,919,286 B。docs/34附录A没有它的历史SHA，
因此本轮只记录实际SHA `3a1ce127291a52fd5551dcb2d9aa4a331f4631ab0f1fdb887a4ebc6fb8ed65ca`及来源，**不声称SRPM通过了不存在的历史SHA对照**；用户明确授权删除该SRPM。
清理脚本仅处理上表对象，完整路径、SHA和逐文件删除日志见
`cleanup.py`、`cleanup-plan.json`、`obsolete-extraction-manifest.json`、`obsolete-extraction-size.json`、
`obsolete-rpms-before-delete.json`、`cache-before-delete.json`、`cache-checkpoint-comparison.json`、`deletion-journal.jsonl`。

清理前可用20,130,463,744 B（18.747955GiB），清理后117,599,830,016 B（109.523376GiB），
原60GiB门槛PASS。原始df见`resources-before.log`、`resources-after.log`；结果`cleanup-result.json`。
后续正常RPM `%clean` 清理其本次BUILDROOT属于已授权正常-ba流程，不是另行删除历史目录。
基线根/H、docs/30根及RPM、隔离旧混合根、docs/25–35历史证据均未清理。

## 1. 独占、输入身份与准入

13:20:48取得本项目锁，session=`archivefix-rpm-fbf469cd44db4432bf9957e5f14f21ed`，holder PID214174。
未发现本项目竞争构建进程。开场主仓库为f49a561且status为空；当前修改均为本任务产生。
`lock-acquired.json`、`precheck.log`、`precheck.json`保存原始检查。

S的HEAD为`f111162e94aa48ed367c9d2c039456c70e7160ae`。

| 输入 | SHA256 |
| --- | --- |
| S/packaging/llvm.spec | `6a91a0bf3d8d2044473662b65ed3d32d4696a697ccd52200d983ce4334aeafdf` |
| S/packaging/llvm-static-archives-native.py | `6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557` |
| 相对f111162e的完整候选diff | `751a629228ed49fb013d95d8d8a451dc341e841c142db67198c7624d36f1ccdb` |
| R/home/abuild/rpmbuild/SOURCES/llvm.spec | `91f684691eb35af52b1a9f2a2cba478f88dbfd8a48b4c2281dac6144d71d3bd0` |
| W/llvm原件spec（保持原4/4/1本地设置） | `95887b2d060b38d5ef8f56936f7481a03d131f9d26432180a68e02ec95f0dda5` |

S spec与docs/32候选逐字节一致；Source不变，沿用docs/34最终离线PASS证据。
root内SOURCES spec保留原GBS增加的VCS/Patch字段，故其SHA与S不同；恢复证明、完整diff及两者关系见
`E35/configuration-restoration.json`、`E35/archive-native-conversion-v2.diff`及`precheck.json`。
认证配置逐项匹配，9项入口正负测试PASS（`fingerprint-tests.log`）。

本轮CMakeCache、build.ninja、两份Ninja状态文件、四个关键ELF、S spec/Source和root spec，
共11项完整SHA全部匹配f49a561登记的`E35/resume-input-manifest.json`。
这补齐了本轮继续前的完整身份检查；docs/34缺少重配后图完整SHA的历史证据边界仍不追溯消除。
前次B/native-archive-conversion证据另备份到`previous-install-conversion-evidence`，未覆盖历史报告证据。

续跑前只读`ninja -n`为87项：86个LLDB头文件stage、1个utility，没有编译/链接待办。
命令、cwd和原始输出见`dry_run.py`、`dry-run.log`、`dry-run.json`。

## 2. 唯一一次增量续跑

完整命令由`resume_once.py`生成并存入`abuild-resume.sh`、`chroot-input.sh`、`build/launch.json`，
通过gbs chroot进入R，abuild运行：

```sh
rpmbuild --define '_smp_mflags -j4' --define '_srcdefattr (-,root,root)' \
  --nosignature --target=x86_64 --define '_build_create_debug 1' \
  -ba --noprep /home/abuild/rpmbuild/SOURCES/llvm.spec
```

准入MemAvailable≥16GiB，首次22,930,866,176 B满足，无等待；磁盘117,051,248,640 B满足60GiB。
全程systemd user scope `MemoryMax=18G`、`MemorySwapMax=0`、nice15/ionice3；Ninja/compile/link=6/6/2，
debuginfo-j4，转换独立4workers，每个转换编译进程4GiB AS。链接不设AS限制。
宿主MemAvailable<2GiB中止、30秒资源采样、2秒进程观察及回收机制沿用；未改变准入或运行政策。

### 2.1 CMake与实际Ninja任务

CMake门禁PASS，完整关键参数见`build/cache-gate.json`；主要项：

```text
CMAKE_BUILD_TYPE:STRING=Release
LLVM_ENABLE_LTO:STRING=Thin
LLVM_LINK_LLVM_DYLIB:BOOL=OFF
CLANG_LINK_CLANG_DYLIB:BOOL=OFF
LLVM_USE_LINKER:UNINITIALIZED=lld
LLVM_ENABLE_ASSERTIONS:BOOL=No
LLVM_PARALLEL_COMPILE_JOBS:STRING=6
LLVM_PARALLEL_LINK_JOBS:STRING=2
LLVM_TARGETS_TO_BUILD:STRING=X86;ARM;AArch64;BPF
CMAKE_CXX_FLAGS: ... -g -O3 -flto=thin -fomit-frame-pointer
```

%build按原spec重新configure后实际执行102项：86头文件stage、1utility、7编译、8链接/归档。
增量任务全文见`ninja-actual-tasks.json`，并非声称Ninja完全空转。
6个compiler-rt DSO、llvm-config发生重链，libtf_xla_runtime.a重新归档；clang-22、lld、llvm-ar没有重链。
配置生成的version-script/dummy等导致新增少量任务；没有更改配置消除它们。

### 2.2 实测资源和转换

| 项 | 实测 |
| --- | --- |
| 起止 | 13:26:11–14:55:52 |
| 总wall | 5,381.375232 s；`time -v`为1:29:41 |
| time -v最高RSS | 3,471,928 KiB；不等同整个scope的峰值 |
| scope MemoryPeak | 17,618,108,416 B（16.408142GiB），低于18GiB |
| memory.events | low/high/max/oom/oom_kill/oom_group_kill均0 |
| scope CPU | 17,082.842137 CPU秒；仅过程记录，不作性能结论 |
| 宿主最低MemAvailable | 16,695,009,280 B（30秒采样） |
| 进程树RSS采样最大 | 6,495,817,728 B；不等同scope内存峰值 |
| 构建期间最低可用磁盘 | 54,686,830,592 B（30秒采样） |
| NATIVE_ARCHIVES_BEGIN/END | 13:38:32–14:12:20；2,028.120725 s，含检查/回写 |
| Source转换核心wall | 1,494.861776 s |
| 单次转换编译最高RSS | 1,045,536 KiB |
| 转换阶段scope current采样最大 | 12,758,884,352 B；不是单编译进程RSS |
| 扫描/转换/跳过 | 270归档，225含bitcode转换，45纯机器码跳过 |
| 成员 | 3,853 bitcode转机器码；11原机器码保留；总3,864 |
| 符号缺失 | 强符号0；允许消失的W类1,920，其余类型0 |
| 清理 | Source回写PASS后archives/members大文件全部删除，仅JSON证据保留 |
| 回收 | sampler_reaped=true；log_reader_reaped=true；构建exit=0 |

证据：`build-resource-summary.json`、`install-conversion-summary.json`、`conversion-early-summary.json`、
`build/outcome.json`、`build/scope-after-rpm.json`、`build/samples.jsonl`、`native-archives-install.log`。
%install结束后正常执行find-debuginfo-j4；最终写出22二进制RPM和1个SRPM。

## 3. 新RPM验收

### 3.1 归档与compiler-rt

22个RPM先逐包记录路径/大小/SHA，再用`rpm2cpio | cpio -idmu --no-absolute-filenames --no-preserve-owner`
解包到新目录N。两端退出码均0，重复包归属的文件元数据一致；详见`rpm-inventory.json`、
`rpm-extract.log`、`rpm-extraction-status.json`、`rpm-file-owners.json`。

225开发归档全部PASS：无bitcode/other/thin、全部x86_64 ELF ET_REL、无调试节，
318,543条索引恰为成员外部定义符号多重集合；与本次B逐成员ordinal/名称/同名出现序号一致。
抽查10个成员确认每函数分段。libarcher_static.a仍为libomp-devel与llvm-static-devel双归属，不遗漏。
45个compiler-rt全部PASS：1,964个成员ELF SHA与H逐字节相同，完整索引映射相同、无调试节；
1,964个成员ar时间戳变化单列，未把ELF变化当成容器变化。
原始逐档/逐成员结果：`verify_new_archives.py`、`new-archives-result.json`、`new-archive-checks/*.json`。

### 3.2 标准后处理

| 步骤 | 本轮次数 | docs/13基线次数 |
| --- | ---: | ---: |
| brp-compress | 1 | 1 |
| 独立brp-strip | 0 | 0 |
| brp-strip-static-archive /bin/strip | 1 | 1 |
| brp-python-hardlink | 1 | 1 |
| find-docs | 1 | 1 |
| find-debuginfo | 1 | 1 |

GNU strip格式错误0行，BEGIN/END各1次、END为PASS225，大文件清理检查PASS。
独立brp-strip在基线宏链也没有执行，不能填成已执行1次。
`build/build.log:8690`原文为：

```text
2026-10-09T14:34:31+08:00 + /usr/lib/rpm/brp-strip-static-archive /bin/strip
```

完整步骤行号和原始输出见`postprocessing-result.json`；构建警告与验收差异分开记录，不将构建exit0视作逐文件一致。

### 3.3 逐文件比对与工具SHA

实际读取N与H的17,689个唯一路径，比较清单、模式、类型、链接目标和内容SHA；各解包树与其对应RPM头部元数据核对全部匹配。新旧内容差异如下。
差异仅225个开发归档（已转换并通过§3.1）及45个compiler-rt归档；**其他文件差异0**。
45个运行库只将各ar header的12字节mtime字段归一化后，整档逐字节相同；包括索引等特殊header，没有豁免其他字节变化。
完整逐文件清单、新旧SHA与分类见`rpm-file-comparison.json`；逐档ar字段归因见
`runtime-ar-header-differences.json`；审查结果为`file-differences-reviewed.json`（PASS）。
这是本次产物的实测，不声称RPM头部或所有未来构建可复现。

clang-22、lld、llvm-ar三者大小和SHA与H全部相同（`three-tools-sha.json`）：

| 工具 | 字节 | SHA256（本轮=基线） |
| --- | ---: | --- |
| clang-22 | 139,929,464 | `3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c` |
| lld | 83,539,336 | `7ebba1bbc8a46e086c4470373315dd31730dab8fe554987894e6689e45e071fc` |
| llvm-ar | 14,825,632 | `cad420e2daeb125b051a5d3f81b038b037c15fd30921ce880d4cc087d624313f` |

## 4. 独立安装幂等：两步PASS

按用户补充，**在新RPM验收前四项全部通过后**执行，早于宿主与Tizen消费者。
为保留所有历史目录，独立安装树置于系统SSD的全新路径：
`/var/tmp/llvm-optimize-archivefix-v2-final-20261009/independent-install/install-root`。
此存储位置是实施选择，不是放宽资源政策；SSD准入时可用450,968,928,256 B（约420GiB）。
只将其父目录临时bind到R内新建的`/home/abuild/archivefix-v2-final-ssd`；
install-pre的rm-rf只作用于`install-root`子目录，不作用于挂载点，也不覆盖正常-ba的安装树或N。
标准-ba的完整转换证据先复制到`ba-install-conversion-evidence`，再允许真实%install重建B内证据目录。

### 4.1 真实-bi重新转换

在原R中、同一类受限scope与abuild身份，唯一一次调用：

```sh
rpmbuild --define '_smp_mflags -j4' --define '_srcdefattr (-,root,root)' \
  --nosignature --target=x86_64 --define '_build_create_debug 1' \
  -bi --short-circuit --noclean \
  --buildroot /home/abuild/archivefix-v2-final-ssd/install-root \
  /home/abuild/rpmbuild/SOURCES/llvm.spec
```

16GiB准入、18GiB/swap0、6/6/2/debuginfo4、nice15/ionice3及采样保护不变。
15:24:14启动，入口wall=2,925.712776 s，exit0；scope峰值17,748,463,616 B，所有memory.events为0。
宿主采样最低可用19,205,808,128 B；采样器、日志线程均回收；临时bind挂载在finally中卸载。
源文件按原%install从B安装，**不是从RPM拼装树**。

```text
2026-10-09T15:34:41+08:00 NATIVE_ARCHIVES_BEGIN 1791531281.9523861
2026-10-09T16:07:01+08:00 NATIVE_ARCHIVES_END 1791533221.879673 PASS 225
2026-10-09T16:11:43+08:00 + /usr/lib/rpm/brp-strip-static-archive /bin/strip
```

重新转换225档、3,853 bitcode，保留11原机器码成员；转换核心1,495.330294 s，
BEGIN至END为1,939.927287 s；单个转换编译最高RSS1,042,800 KiB。
强符号缺失0，允许W类缺失1,920；证据大文件已删除。
后处理后在这棵独立安装树重做第1项：225档的成员顺序/同名身份、全部机器码、无调试节和完整索引全部PASS，
10个成员的每函数分段抽查PASS。
证据：`independent-bi/{abuild.sh,commands.log,build.log,outcome.json,scope-after-rpm.json,storage.json,storage-final.json}`、
`independent-install-summary.json`、`independent-archives-result.json`、`independent-archive-checks/`。

### 4.2 对同一安装树直接调用Source

重新挂载同一SSD父目录，直接运行同一个Source，未再次运行rpmbuild：

```sh
python3 /home/abuild/rpmbuild/SOURCES/llvm-static-archives-native.py \
  --root /home/abuild/archivefix-v2-final-ssd/install-root \
  --build /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build \
  --evidence /home/abuild/archivefix-v2-final-skip-evidence --arch x86_64 \
  --compiler /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/clang-22 \
  --disassembler /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-dis \
  --nm /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-nm \
  --jobs 4 --address-space-bytes 4294967296
```

原始输出：

```text
2026-10-09T16:14:57+08:00 NATIVE_ARCHIVES_SKIP all archives already native
2026-10-09T16:14:57+08:00 NATIVE_ARCHIVES_END 1791533697.00144 PASS 0
```

exit0，入口26.378315 s；扫描270档全部native，转换0档，225个开发归档前后SHA逐个完全相同。
scope峰值1,804,120,064 B，无内存事件；采样器、日志线程回收，挂载再次卸载。
证据：`independent-skip/`、`independent-skip-verification.json`。
这里才是SKIP测试；没有错误要求“真实-bi重装原件后也应SKIP”。

## 5. 消费者与本轮停止点

### 5.1 七项宿主消费者：7/7 PASS

全部正例归档来自N/usr/lib64；H的编译器、头文件、llvm-config、opt与N已经逐字节证明相同，用作同协议夹具。
旧H归档仅用于失败反例。用`tools/verify_native_archive_consumers.py`，编译与链接分开；
编译4GiB AS，链接不设AS上限；外围按docs/29的可用内存减4GiB、最高18GiB策略，本次cap18GiB/swap0。
GNU ld的实际driver展开不含-flto或任何插件，也没有误将-cc1交给loader。

| 环境部分 | 实际来源及证据 |
| --- | --- |
| LLVM工具、LLVM/lld头文件、资源目录 | H解包，已与N同字节；resource-dir=H/usr/lib64/clang/22 |
| 被验静态库 | N/usr/lib64；llvm-config --link-static临时prefix将lib64指向N |
| C++头、libstdc++、glibc、crt、libgcc、GNU ld | 宿主；compile-a.log确认GCC13搜索路径，a-bfd-runtime.txt保存loader实际解析 |
| libxml2.so.16 | `W/temp/toolchain-runtime-baseline/libxml2/usr/lib64`的Tizen库，经显式library-path；未安装到宿主 |
| loader | 宿主`/lib64/ld-linux-x86-64.so.2` |

| 项目 | 结果 |
| --- | --- |
| A-bfd / A-lld | 均PASS；固定IR经过PassBuilder O2后输出与H的opt -O2完整一致 |
| B-bfd / B-lld | 均PASS；进程内调用lld ELF入口，生成物运行exit37；两者生成物SHA均为`3609167ac2889072dcca787a8cf2cbcdb762c280e55350b797ef02e6842ce789` |
| 共享库与dlopen | PASS；GNU ld使用-shared -z defs -z text，加载后输出一致 |
| --gc-sections | PASS；47,387,472→28,378,320 B；GC版运行正确，不作为性能结论 |
| 原bitcode归档反例 | PASS；相同无LTO/无插件GNU ld命令失败，保留完整错误；这不是隔离了索引因素的实验 |

scope wall28.402079 s，峰值1,217,548,288 B，无内存事件，采样器和日志线程回收。
全部编译/链接/运行argv、时间、RSS/VmPeak和driver输出在`new-rpm-consumers/`，
总判据`new-rpm-consumers/result.json`，scope证据`new-consumers-scope/`。

### 5.2 Tizen bfd：依赖解析失败，未进入编译

只在上述门禁通过后才启动；新根为
`/var/tmp/llvm-optimize-archivefix-v2-final-20261009/gbs-root-archive-consumer-v2-final-bfd`。
SSD位置与独立安装一样用于保留/home历史材料，不修改仓库来源或测试协议。
两个小测试源码repo均已准备，只有bfd调用了GBS；lld源码准备不等于已执行测试。
本地附加库`C/new-rpm-repo`由本轮22 RPM硬链接生成，逐个确认device/inode相同，
`createrepo_c --workers 2`成功；配置gbs_llvm.conf SHA仍为`a3fea7732532db26c11b88407464e0274a6d8b4277623364fe16b6980181b03f`。

实际命令（各路径按§0.1展开；完整argv为`tizen-bfd/attempt.json`）：

```text
gbs -c W/gbs_llvm.conf build -A x86_64
  -B /var/tmp/llvm-optimize-archivefix-v2-final-20261009/gbs-root-archive-consumer-v2-final-bfd
  --threads 1 --include-all --define '_smp_mflags -j4'
  -D E34/full-build/buildconfig.conf -R C/new-rpm-repo C/test-package-bfd
```

BR精确钉llvm-static-devel/llvm-devel/llvm/clang=22.1.8-1；测试包含A、B及%check，
另预备whole-archive共享链接只记录，不作为门禁。由于本次根本没有进入构建，这些检查均未执行。
准入24,855,044,096 B≥8GiB，等待0次；MemoryMax6GiB、MemorySwapMax0、nice15/ionice3及宿主2GiB保护。
16:16:21–16:16:33，wall12.177772 s，GBS exit1；scope峰值147,640,320 B，所有memory.events为0，
sampler_reaped/log_reader_reaped均true。没有scratch根实例，未执行rpmbuild、编译器、链接器或%check。

`tizen-bfd/build.log`关键原文：

```text
2026-10-09T16:16:32+08:00 === the following packages failed to build due to missing build dependencies (1) ===
2026-10-09T16:16:32+08:00 archive-native-consumer-bfd:
2026-10-09T16:16:32+08:00   nothing provides ld-linux-x86-64.so.2()(64bit) needed by llvm-devel
2026-10-09T16:16:32+08:00   nothing provides glibc
2026-10-09T16:16:32+08:00   nothing provides bash
2026-10-09T16:16:32+08:00   nothing provides rpm-build
2026-10-09T16:16:32+08:00 error: <gbs>some packages failed to be built
```

总计189条`nothing provides`，完整条目和行号为`failure-diagnosis/summary.json`。
GBS调用本身FAIL，**GNU ld消费者兼容性在此轮未测试，不记作链接失败**。
错误包装中的cache_passed不涉及LLVM CMake门禁：此小测试包没有该门禁，outcome为null。

### 5.3 只读原因核查与停止边界

停止后仅各读取一次固定仓库repomd，无重试构建、无切换URL：

| 固定仓库 | 16:19只读查询 | SHA/含义 |
| --- | --- | --- |
| Base `tizen-base-toolchain_20260912.061113` | HTTP404，155 B错误页 | `acb74ed94d31dd207b22ae4b7a9209eb830148782acfa6276bd558982f7762fb`；该固定端点当前不可读，不猜测服务端删除原因 |
| Unified `tizen-unified-toolchain_20260814.092727` | HTTP200，4,476 B | `e7af3f222f0ce958678d964589f2d156e8b47ba463ac0b3b0b96c74663382200`，与原指纹相同 |

Base原始状态行：`HTTP/1.1 404 Not Found`；URL为
`https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20260912.061113/repos/standard/packages/repodata/repomd.xml`。
`failure-diagnosis/repo-http.json`保存完整curl argv、状态、最终URL、SHA；同目录保存完整headers/body。

本机GBS源码`/usr/lib/python3/dist-packages/gitbuildsys/cmd_build.py:141–159`显示-R是追加仓库，
本次未带--skip-conf-repos。`utils.py:362–380`将PageNotFound转为无法识别标准repo；
`utils.py:463–496`只加入识别成功的远端，未识别也可能不立即报fatal；
`utils.py:515–536`仍可返回本地附加repo。
因此**本地22包可见并不证明Base可用**；本轮实际缺失基础依赖，且Base固定端点404，阻塞为仓库可用性，
不能归因为SSD、内存上限或新归档链接能力。源码副本和SHA也在`failure-diagnosis/`。

要继续，需先恢复同一Base快照的可用仓库/具有对应版本与摘要的缓存镜像，再按新授权补齐两个Tizen包。
本轮没有自行换快照、补仓库、重试bfd或启动lld；没有执行whole-archive诊断。
完整失败现场及新RPM均保留。原根增量构建不需要重新执行来解释这个依赖解析失败。

## 6. 补丁状态、结论与收尾

**本轮停止，v2最终提交补丁未生成。** 已闭合的是：标准提交配置的一次增量产包、225开发/45运行库验收、
17,689路径非归档零差异、独立-bi真重装与同树SKIP、七项宿主消费者。
未闭合的是本轮Tizen bfd/lld包内验收；不能用docs/30历史结果代替，不能声称全部验收或发货PASS。

| 项目 | 结果 |
| --- | --- |
| 清理三项/原60GiB门槛 | PASS；没有额外清理历史目录 |
| CMake/一次-ba --noprep | PASS；无完整重建，未改6/6/2或18GiB |
| 新RPM第1–4项、工具SHA | PASS |
| 独立-bi及同树SKIP | 两步PASS；使用独立buildroot，未覆盖N |
| 七宿主消费者 | PASS 7/7 |
| Tizen bfd包 | FAIL于依赖解析；尚未编译/链接/%check |
| Tizen lld包、whole-archive | NOT_RUN，按规则停止 |
| 重试 | 0 |
| v2 format-patch / tizen_base刷新 | NOT_RUN，未进入第三步 |
| Gerrit | 未推送 |

目标基准仍记录docs/34的本地tizen_base `2d23367d74afbf2bb1e9e4013fce072b3a154109`；
本轮没有fetch或新建提交工作树，不能声称已经生成基于该HEAD的v2补丁。
实测试验diff仍为`E35/archive-native-conversion-v2.diff`，SHA
`751a629228ed49fb013d95d8d8a451dc341e841c142db67198c7624d36f1ccdb`，**它不是本轮最终Gerrit提交包**。

`patches/archive-index-fix/`的v1保持不动：

- 补丁`0001-Fix-llvm-static-devel-usability-with-ThinLTO.patch`：SHA `0c40c91cb6b896fd93f2712b669eec6771d219268dff7d290539fbb98d0bea58`。
- Source `llvm-static-archives-native.py`：SHA `2476c5efa061499d7963e0f0976f0c9c86944b688f5bcc48ea40911574af399e`。

收尾核对W原件、S输入、docs/25–34和v1资产；所有本轮scope及采样器均已退出，临时bind均已卸载。
项目锁持有至收尾检查结束并由原持有者释放；记录`final-integrity.json`、`final-process-check.json`、`lock-released.json`。
本报告、STATUS与认证文件的执行状态同一commit提交GitHub；没有改gbs配置、spec/Source、LLVM源码，
没有做完整LLVM重建、性能校准、Chromium构建或Gerrit推送。
秒数和内存仅为运行记录，不作性能结论。总结果为`final-outcome.json`。

## 附录A：本轮二进制RPM inventory

所有路径位于`R/home/abuild/rpmbuild/RPMS/x86_64/`。

| 文件 | 字节 | SHA256 |
| --- | ---: | --- |
| clang-22.1.8-1.x86_64.rpm | 310019538 | `82970941d586e91861ebe5afe7d0c99db98e6142bd77e5c2b9d6aaf44c2e2604` |
| clang-debuginfo-22.1.8-1.x86_64.rpm | 2928315838 | `1a4dfce12b39e2c4f667b995dbedf0098eb17afc955c76f38b02f00c30e13266` |
| clang-devel-22.1.8-1.x86_64.rpm | 4099162 | `17974fc8ca91902fe2e567003d051bbfd66f98001ea33ad6da3bfbabd951e59c` |
| clang-devel-debuginfo-22.1.8-1.x86_64.rpm | 5728882 | `f8724e453f170815bca1e85db3776bc88d59756cb13b1765ad4898b9cb885e01` |
| compiler-rt-22.1.8-1.x86_64.rpm | 3721870 | `4264edddd7f29f7bd3f00570569ac86107f56189113208590d41e9598bd689e7` |
| compiler-rt-debuginfo-22.1.8-1.x86_64.rpm | 1289498 | `b473f81452b0de80b726f4f910654b24370d447b92d2c71279d29631f9a314ed` |
| libllvm-22.1.8-1.x86_64.rpm | 23649450 | `3382c1eb11516f54e62d933c77193c188a11c792ff906dbc3792806c86772d05` |
| libllvm-debuginfo-22.1.8-1.x86_64.rpm | 198056974 | `f2fb22953807c2f386ebd5980e9a12133979ff4b740b946d6a20d58f81fee3fc` |
| libomp-22.1.8-1.x86_64.rpm | 373462 | `88a057dd1d70cd92eaedeb60daaca00d674d70d1c2f3268bff4f53cfe86cbeb5` |
| libomp-debuginfo-22.1.8-1.x86_64.rpm | 1142202 | `874e533d8059bcc084c8d2d76f1a2530b72f1f129f350505ead52fc26832b6cd` |
| libomp-devel-22.1.8-1.x86_64.rpm | 25522 | `89f4dfced1682786e607cc27feaf4a501d09c112edf8ca84a12a30ca70dbfce8` |
| lldb-22.1.8-1.x86_64.rpm | 30767594 | `221a36caaf8a200970b70268a0031418043b11821f724a4b2ee56a545cba8d99` |
| lldb-debuginfo-22.1.8-1.x86_64.rpm | 332844394 | `d96b6e91b766e27bbc662684f13cc7d58f9d5950aaca3a3c5dce5837145f27dd` |
| lldb-devel-22.1.8-1.x86_64.rpm | 30525214 | `4ee2c13f43c48c5139822959ca5d7966206df6d9531f0c80eab5d11782646b0e` |
| lldb-devel-debuginfo-22.1.8-1.x86_64.rpm | 279580554 | `7364d0d3a3289c848180d4601c4b5cd8f603c466b0507d6ce8ae3d69d8a62645` |
| llvm-22.1.8-1.x86_64.rpm | 410661042 | `476ee724108ab0420014b098f94551ea7b34224bd60a20bff91039f5b604e88e` |
| llvm-debuginfo-22.1.8-1.x86_64.rpm | 3842665274 | `b52898d90215ae0eb116c3438bb65333adf70fa391a78e8dd6f732f5187f94c7` |
| llvm-debugsource-22.1.8-1.x86_64.rpm | 43654074 | `c3934936973840ec76de6c1933cf5da90458d823456ef513d3c48b4a92c3cab5` |
| llvm-devel-22.1.8-1.x86_64.rpm | 41190542 | `f9a6cc22e5cde49373f277b8b8b641bde4171b1f543fbe3b7bd2dab4a7889d62` |
| llvm-devel-debuginfo-22.1.8-1.x86_64.rpm | 308603382 | `a0a5ea2e037f87bfc55657bc575287f42e083e309df5ccab42eabd7f655944ef` |
| llvm-static-devel-22.1.8-1.x86_64.rpm | 60439606 | `4c0c72613ac6772730475fddf642257da5f28adf3a026b60d5888c4abbfb3c06` |
| python-clang-22.1.8-1.x86_64.rpm | 36322 | `3e9ffa2c6e85ae6242956b3ddec511a8efb24822e6c4f127db66cbf6cb80ad99` |
