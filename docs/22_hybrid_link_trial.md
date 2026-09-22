# 22 混合链接本机认证试构建（正确性）

执行日期：2026-09-22。修订先提交并推送 `8facdfad82e3e05eb8a848ccfaa997472a83f421`，
之后才创建独立源码工作树并启动试构建。本报告不包含BOLT、profile或性能校准。

**结论：一次全新混合试构建成功，22个二进制RPM，30/30 TU完整.o逐字节PASS；仍有两项发货/范围BLOCKER。**
一是五个额外工具仍静态链接LLVM；二是开发归档索引被GNU strip破坏，普通ranlib只补齐缺失索引，
不会更新已经存在但残缺的索引。本轮不修改补丁重试，未进入OBS/Gerrit，未做任何性能认证。

docs/21的先推修订保持不动；本报告记录其七文件提案的实际结果，以及新发现的方案边界。

## 1. 身份、授权与源码隔离

W=/home/linhao/Toolchain/development/llvm-optimize；E=W/temp/hybrid-trial-20260922。
源码试验工作树W/temp/llvm-hybrid-trial，分支hybrid-link-trial，HEAD=f111162e94aa48ed367c9d2c039456c70e7160ae。
原W/llvm仍在sandbox/fangyu.he/llvm_optmize，原spec与源文件不动。
试验工作树先继承原spec的三处4/4/1并发差异，再应用docs/21附录A七文件补丁；
保留static-devel、compiler-rt、libarcher，没有加入BOLT、keeprsp或归档修复spec改动。

GBS使用--include-all导出dirty工作树；实际SOURCES/llvm.spec自动添加VCS与历史/dirty补丁段，
全文差异E/exported-spec.diff。实际BUILD中的六个CMake源文件SHA均与获批内容相同；
spec由SOURCES提供，不在BUILD/packaging中。不能将这个文件布局差异误记为源码丢失。


获批应用后的文件摘要（与E/applied-source-sha256.json交叉核对）：

| 文件 | SHA256 |
| --- | --- |
| `clang/cmake/modules/AddClang.cmake` | `cc505b09c2856008843c430269fb989648090bdcfd1048ab1c2ca16d2c499480` |
| `clang/tools/driver/CMakeLists.txt` | `e3957b3fed9db504f032d1c3271b23d369c1d65afe4bd54f119f6b343978aad5` |
| `lld/cmake/modules/AddLLD.cmake` | `d43aa8961e5f3a4fd77a2a4b2051e39bea50c643b5a60d403af7c8db68c6a72f` |
| `lld/tools/lld/CMakeLists.txt` | `ebb6c00e06c799ad8b09969b11b2710e5f5928363fbc03dd98c220dd44ae7656` |
| `llvm/cmake/modules/AddLLVM.cmake` | `a06c1d55d9866328d3230752efe9c31db6393fc2ef9fc788b4c911ed23d25f89` |
| `llvm/tools/llvm-ar/CMakeLists.txt` | `5c44903dc53de9e25dea766fa69110068e4367b79d2511ca943e6a29bfe3866f` |
| `packaging/llvm.spec` | `c24ca6163ad6092b52d7bb448bd51690703dfef246d2bbc76c10acacadf71393` |

完整diff SHA256：`7c3b62fbe32d1667af6a5367ebbd2e83529f6e956cd902db1a2872a4da9eb2af`。

## 2. 预检和唯一认证入口

运行入口：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/build_llvm_x86_64.py --run \
  --certify-fingerprint hybrid-trial --source temp/llvm-hybrid-trial \
  --buildroot temp/gbs-root-x86_64-hybrid-trial \
  --log-dir temp/hybrid-trial-20260922/run
```

普通准入仍拒绝此新指纹，只有显式hybrid-trial入口可接受钉住的HEAD、分支、七文件SHA、完整diff SHA、
spec/配置/build.conf/repomd摘要和4/4/1、GBS线程1、debuginfo4。未知试验、任一差异拒绝；
固定工作树/新构建根，禁止自动改变源码。tools/llvm_hybrid_trial_fingerprint.json记录完整指纹与授权，
不是先验“容量已认证”凭据。14项构建门禁测试通过（新增响应文件目标关联测试后复核），包含串扰负例和采样器退出路径模拟。

预检：nproc20；启动available=18.362865GiB、磁盘664.620895GiB；门槛16GiB/60GiB通过。
两固定repo返回200；queryconfig+rpm展开_toolchain为1|clang；systemd用户scope探测成功。
完整命令执行前写E/run/launch.json、commands.log；nice15、ionice-c3、18GiB、MemorySwapMax=0，
读回MemoryMax=19327352832。每30秒free/load/RSS/磁盘，每2秒各进程VmHWM；低于2GiB自动中止。
子进程退出后短暂保留scope以读取累计peak/events，再回收采样器。原18GiB普通门禁未放宽。

## 3. CMake门禁

302.1053676910087秒通过，E/run/cache-gate.json的errors为空。实际关键值：

```text
CMAKE_BUILD_TYPE=Release
LLVM_LINK_LLVM_DYLIB=ON
CLANG_LINK_CLANG_DYLIB=ON
TIZEN_HYBRID_LINK=ON
LLVM_TOOL_LLVM_DRIVER_BUILD=OFF
BUILD_SHARED_LIBS=OFF
LLVM_ENABLE_LTO=Thin
LLVM_ENABLE_ASSERTIONS=No
LLVM_PARALLEL_COMPILE_JOBS=4
LLVM_PARALLEL_LINK_JOBS=1
LLVM_USE_LINKER=lld
LLVM_TARGETS_TO_BUILD=X86;ARM;AArch64;BPF
LLVM_EXPORT_SYMBOLS_FOR_PLUGINS=OFF
CMAKE_CXX_FLAGS=  -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument   -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables  -g -O3 -flto=thin -fomit-frame-pointer
```

LLVM_EXPORT_SYMBOLS_FOR_PLUGINS=OFF，因此本次没有触发该选项ON时的插件导出依赖遍历分支；
不能将configure成功推广成所有配置都支持拟议生成表达式。Ninja生成7633任务。
只读导出的三个最终链接命令：clang-22有113个归档token、lld90个、llvm-ar34个，
没有libLLVM/libclang-cpp.so token；这是生成图证据，仍须最终NEEDED验证。

## 4. 构建终态与资源实测

唯一一次`gbs build -A x86_64`从2026-09-22 20:30:11启动，21:54:11结束。
7633个编译/链接任务全部完成；没有configure/链接失败、重试或续跑。
实际命令行中的底层build工具仍有其自动生成的`--jobs 40`，但spec的ninja/compile/link为4/4/1，
显式`_smp_mflags -j4`覆盖打包宏；日志21:40:09原样执行`find-debuginfo.sh -j4`。
不能把底层默认参数误报为本次实际ninja或debuginfo并发。证据E/run/build.log、build-milestones.txt。

终态原始摘录：

```text
{
  "exit_code": 0,
  "elapsed_seconds": 5040.295107446,
  "command_exit_code": 0,
  "cache_passed": true,
  "problems": [],
  "sampler_reaped": true,
  "log_reader_reaped": true,
  "interrupted": null
}
Result=success
MemoryPeak=19327352832
CPUUsageNSec=25826592876000
MemoryMax=19327352832
MemorySwapMax=0
/usr/bin/time -v:
User time (seconds): 25035.33
System time (seconds): 790.09
Elapsed (wall clock) time (h:mm:ss or m:ss): 1:24:00
Maximum resident set size (kbytes): 15914848
Swaps: 0
Exit status: 0
```

| 项目 | 实测与含义 |
| --- | --- |
| scope累计峰值 | 18 GiB，恰好等于cap；这是受限运行的实际记账峰值，不能当作无上限自然内存需求 |
| memory.events | max=6369，oom=0，oom_kill=0，oom_group_kill=0；触发回收，没有OOM |
| 宿主最低MemAvailable（30秒采样） | 12151705600 B / 11.317158 GiB；未触发2GiB中止 |
| 外层time最大单进程RSS | 15.177582 GiB；不是进程RSS之和，亦不是scope总内存 |
| 采样器/日志线程 | outcome均reaped=true；结束后systemctl is-active为inactive（exit4），不是后台残留 |
| 磁盘（同文件系统，运行采样） | 启动664.620861 GiB，末次604.574287 GiB；差值60.046574 GiB含整个文件系统同期活动，不冒称纯构建大小 |
| du -sh | 新GBS根47G、源码工作树2.5G；du对根内root、ldconfig、upgrade三个受限目录报Permission denied，因此47G是可读范围值 |
| load1最大采样 | 23.61；本轮是正确性/容量试验，不是性能测量，无校准PASS声明 |

构建后`df -h`可用614G（此时已开始独立解包，时间边界不同）；原始输出E/disk-after.txt。
宿主`free -g`可见历史swap占用，不等于本次scope使用swap；本次MemorySwapMax=0、time Swaps=0。

关键链接及已观测Top 10：

| 链接目标 | lld采样VmHWM GiB | Ninja链接边wall秒 | 构建树ELF字节（未strip） |
| --- | ---: | ---: | ---: |
| `bin/clang-22` | 15.177582 | 443.526 | 1793477112 |
| `lib64/libclang-cpp.so.22.1` | 12.133747 | 211.504 | 929195504 |
| `lib64/libLLVM.so.22.1` | 11.292168 | 129.854 | 1181500120 |
| `bin/lld` | 11.057663 | 166.075 | 1079522520 |
| `lib64/libclang.so.22.1.8` | 9.137413 | 64.889 | 526301896 |
| `bin/llvm-exegesis` | 7.251167 | 120.792 | 598155432 |
| `bin/clangd-fuzzer` | 4.643539 | 16.292 | 363899536 |
| `bin/clang-tidy` | 3.145954 | 31.929 | 285653664 |
| `lib64/liblldb.so.22.1.8` | 2.664310 | 34.5 | 328050912 |
| `bin/clangd` | 2.629246 | 9.7 | 387244712 |

VmHWM来自2秒采样的进程累计高水位；可能漏掉最后不足2秒区间。Ninja边wall包括驱动/链接命令，
不等于采样首尾的进程存活跨度。clang采样高水位与外层time-v的15914848KiB吻合。
libLLVM.so与clang分别129.854秒/11.292168GiB、443.526秒/15.177582GiB。
全新根没有继承旧ThinLTO缓存，但不宣称宿主文件缓存冷态；不将该耗时用于吞吐比较。

启动时采样器只从lld直接argv取`-o`；libclang-cpp、clang等使用response文件时，完整process-memory仍记录PID和VmHWM。
本轮另用实际`/proc/PID/status`的PPid及父驱动`-o`建立E/link-target-map.json，关联原2秒记录，未伪造缺失样本。
交付脚本已补同一路径，直接argv/response/UNKNOWN/截断参数四种测试通过。
没有新增常驻采样进程，也没有改变正在运行的构建参数。关联与汇总保留E/summarize_resources.py。

**容量结论：这个精确七文件指纹的一次完整构建在18GiB/4/4/1/debuginfo4下成功。**
普通基线准入规则保持原样；显式hybrid-trial是该获批试验入口，不通用放行未知配置或BOLT/PGO。
完成容量试验不表示下述范围、归档或发货门禁已通过。

## 5. 产物、归档、别名与活性

### 5.1 RPM与LLVM共享库依赖

22个二进制RPM位于R=`W/temp/gbs-root-x86_64-hybrid-trial/local/BUILD-ROOTS/scratch.x86_64.0`的
`home/abuild/rpmbuild/RPMS/x86_64/`，另有一个SRPM；各RPM用rpm2cpio与cpio解包到
`W/temp/toolchain-hybrid-trial/`（H），没有安装到宿主，没有覆盖TC=`W/temp/toolchain-baseline/`。
逐条保留管道两端退出码，完整清单/文件列表/RPM SHA见E/products/rpm-inventory.json和commands.json。

| 工具 | 剥离后字节 | LLVM相关NEEDED | 该工具预期 |
| --- | ---: | --- | --- |
| clang-22 | 139929528 | 无 | PASS |
| lld | 83539400 | 无 | PASS |
| llvm-ar | 14825632 | 无 | PASS |
| opt | 231080 | libLLVM.so.22.1 | PASS |
| llc | 160792 | libLLVM.so.22.1 | PASS |
| llvm-objcopy | 208496 | libLLVM.so.22.1 | PASS |
| llvm-nm | 140448 | libLLVM.so.22.1 | PASS |
| llvm-strip | 208496 | libLLVM.so.22.1 | PASS |
| clang-tidy | 11075992 | libclang-cpp.so.22.1, libLLVM.so.22.1 | PASS |
| clangd | 17233016 | libclang-cpp.so.22.1, libLLVM.so.22.1 | PASS |
| lldb | 167240 | libclang-cpp.so.22.1, libLLVM.so.22.1 | PASS |

clang/clang++共享实体；lld与llvm-ar所有列出的别名NEEDED相同。
“静态”只指LLVM/Clang库，libc/libstdc++等仍是动态依赖。
lld还依赖libxml2.so.16；版本/活性检查使用独立旧快照解包库
`W/temp/toolchain-runtime-baseline/libxml2/usr/lib64`和显式loader，没有修改ELF。
LLDB的`H/usr/bin/lldb`是指向`/home/owner/share/tmp/sdk_tools/lldb/bin/lldb`的绝对软链接。
在解包目录外直接exists会误判不存在；本次按RPM逻辑根映射到H下真实ELF读取，未访问宿主同名路径。
它直接NEEDED含liblldb、libclang-cpp、libLLVM。E/products/tools-initial.json保留初查误判，tools.json为修正结果。

关键SHA256：

| 工具 | SHA256 |
| --- | --- |
| clang-22 | `eeb3495775e42948998f4ba31f8c0856efd3c5df421e5ed984fdf586025b4369` |
| lld | `b2c464aeaf9cf2f7610c587d765281bf1487bb93ebc483a47f181eacf4fc1f3d` |
| llvm-ar | `cad420e2daeb125b051a5d3f81b038b037c15fd30921ce880d4cc087d624313f` |
| opt | `3b5803e30dcd23bf86d7ba5d841b3781384886a67195e2764c48931d00fd7f0a` |
| llc | `997de5e998ba0b85ba406322c3c160f8481ada2b920d3b4d28ac33d93f34e4e7` |
| llvm-objcopy | `941a8168d1a03aff3362e697714691181b18b421f482ec14df8dce243ffdd0b9` |
| llvm-nm | `7fa487bb61292e4d07d328b869add941dc86017990bb89b01740049db3bbe06d` |
| clang-tidy | `0d8fad5f535726c0b6ce20f5429b1bcf7388e79bb4761b0a404747d98cc439fa` |
| clangd | `fddec8cd5d91d3ec7c167e84d7df7a00dcda5a5a0e4748a86af0e86a9b987649` |
| lldb | `d6c0fa78772669a6b8b13c4f9b27861494eb995c841c3a71885c5a11726f669e` |

**BLOCKER：其余工具全部走libLLVM.so的范围尚未满足。** `/usr/bin`全扫描另发现：

| 额外静态工具 | 字节 | 源码依据 |
| --- | ---: | --- |
| llvm-config | 325504 | llvm/llvm/tools/llvm-config/CMakeLists.txt:1、17 |
| llvm-exegesis | 47724712 | llvm/llvm/tools/llvm-exegesis/CMakeLists.txt:4、22 |
| llvm-tblgen | 4836176 | llvm/llvm/utils/TableGen/CMakeLists.txt:26；TableGen.cmake:186 |
| clang-tblgen | 2382816 | llvm/clang/utils/TableGen/CMakeLists.txt:1；TableGen.cmake:186 |
| lldb-tblgen | 973120 | llvm/lldb/utils/TableGen/CMakeLists.txt:8；TableGen.cmake:186 |

TableGen.cmake完整路径为`llvm/llvm/cmake/modules/TableGen.cmake`；这些路径显式静态链接LLVM组件。
这是现有上游例外未被七文件补丁覆盖，不是八个抽查工具失败。证据E/remaining-static-source-evidence.txt、products/tools.json。
本轮不擅改补丁修复，也不把这五项默认豁免；后续须修订方案或由用户明确例外。

### 5.2 常规包零LLVM.a、开发归档与单次ranlib

对**每一个**二进制RPM执行`rpm -qpl`，按`\.a$`过滤。

- `compiler-rt`：45个.a（COMPILER_RT_RUNTIME_EXCEPTION）。
- `libomp-devel`：1个.a（DEVEL）。
- `llvm-static-devel`：225个.a（DEVEL）。

其余19个二进制RPM的.a列表均空，包括全部常规LLVM/Clang包。
compiler-rt的45个运行库是用户明确保留项，不能同时声称“字面上所有非devel RPM都无.a”；
常规包零**LLVM开发归档**通过。libarcher_static.a继续归libomp-devel，未改其源码/打包范围。

开发归档共226个（static-devel225+libomp-devel1），用本次llvm-nm逐一`--print-armap`，
以Archive map段至少一个条目判非空，普通符号输出不计。源码格式依据`llvm/llvm/tools/llvm-nm/llvm-nm.cpp:2071–2076`。

| 状态 | 初始RPM解包 | 仅对独立副本各ranlib一次后 |
| --- | ---: | ---: |
| 无索引（Archive map缺失） | 223 | 0 |
| 非空索引 | 3 | 226 |
| 已实证残缺索引 | 3 | **仍有3** |

前三项“非空”实际也残缺：

| 归档 | 构建树索引条目 | RPM索引条目 | 一次ranlib后 |
| --- | ---: | ---: | ---: |
| libLLVMAnalysis.a | 9445 | 82 | 82 |
| libLLVMCodeGen.a | 14276 | 1 | 1 |
| libLLVMSupport.a | 5023 | 22 | 22 |

原因有直接源码依据：`llvm/llvm/tools/llvm-ar/llvm-ar.cpp:1084–1093`的createSymbolTable对已有GNU符号表直接return。
因此**单纯“armap非空＋普通llvm-ranlib”不足以保障归档索引完整**。本轮各副本仅执行一次ranlib，没有第二种参数组合或重建。
223个空索引补为非空，但不能把全226非空提升成所有索引/消费者已认证。
修复副本位于`E/archives/repaired/`；原解包归档及RPM摘要保持原样。
E/archives/results.json逐个记录前后SHA、字节数、条目数、命令退出码；summary-initial.json保留初次非空检查结果，
summary.json登记残缺索引复核，不能将早期“非空PASS”当最终发货PASS。

已知坏liblldCOFF.a（docs/13）负对照：nm退出0、普通成员符号非空，但Archive map=0，索引门禁正确拒绝。
SHA=`9e8915f4a853a8a97285f34c2b51eb2bc16eb3fb3de943fdabf43f1b3e252617`。

**发货BLOCKER未解除。** docs/21方案B“strip后普通ranlib”对残缺表不足，需下一方案修订；
方案A让brp不处理.a仍待试包，不能据本轮推断已认证。未修改spec、不追加修复命令。
本轮是本机试验，不发货；bfd/lld组件消费者与坏归档消费者对照没有执行，仍是发货前硬条件。
本轮完成的是逐归档查询、一次允许修复及复查；不以30 TU门禁替代静态开发包消费者验收。

### 5.3 别名、身份与活性

| 条目 | 实际链接类型/目标 |
| --- | --- |
| clang | 软链接→clang-22 |
| clang++ / clang-cl / clang-cpp | 软链接→clang→clang-22，最终实体一致，无待同步硬链接 |
| llvm-ranlib / llvm-lib / llvm-dlltool | 软链接→llvm-ar |
| ld.lld / ld64.lld / lld-link / wasm-ld | 软链接→lld |

E/products/tools.json保存lstat、link target、inode与nlink；clang与ar实体nlink均1。
身份脚本对clang-22退出0、`NEEDED_LLVM_SHARED=NO`；对llvm-objcopy退出0、`NEEDED_LLVM_SHARED=YES`。
只读检查使用`--no-exec --expect-bolt absent`，RPM归属为信息项，不因解包文件无宿主RPM归属而失败。

活性脚本对clang和lld分别PASS，使用`--host-arch x86_64`；lld新增`--tool-kind lld --compiler <clang-22>`，
查询GNU flavor版本并将最小ARM.o链接为relocatable ELF。所有功能命令限单核、4GiB AS、30秒、nice15/ionice-c3、禁core。
原ELF摘要前后相同；完整结果E/liveness-clang/result.json、E/liveness-lld/result.json。
对应源码/测试随本提交交付；测试覆盖clang默认/正确override一致、错误override拒绝、strip损坏负例与lld正例。

## 6. 与全静态基线的正确性及profile适用性

### 6.1 ELF差异

| RPM clang-22 | 字节 | SHA256 | .dynsym条目 |
| --- | ---: | --- | ---: |
| 全静态TC | 139929464 | `3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c` | 65241 |
| 混合H | 139929528 | `eeb3495775e42948998f4ba31f8c0856efd3c5df421e5ed984fdf586025b4369` | 65241 |

两者均无.symtab（已剥离）；符号数这里特指.dynsym，不将其冒充完整静态符号数。
完整节区大小表（readelf -SW原始输出在E/clang-comparison/）：

| 节区 | TC字节 | H字节 |
| --- | ---: | ---: |
| `NULL` | 0 | 0 |
| `.interp` | 28 | 28 |
| `.note.ABI-tag` | 32 | 32 |
| `.dynsym` | 1565784 | 1565784 |
| `.gnu.version` | 130482 | 130482 |
| `.gnu.version_r` | 784 | 784 |
| `.gnu.hash` | 455256 | 455256 |
| `.dynstr` | 4917447 | 4917499 |
| `.rela.dyn` | 5725704 | 5725704 |
| `.rela.plt` | 8112 | 8112 |
| `.rodata` | 19674176 | 19674176 |
| `.gcc_except_table` | 214 | 214 |
| `.eh_frame_hdr` | 1154852 | 1154852 |
| `.eh_frame` | 7824880 | 7824880 |
| `.text` | 95419023 | 95419023 |
| `.init` | 23 | 23 |
| `.fini` | 9 | 9 |
| `.plt` | 5424 | 5424 |
| `.tdata` | 4 | 4 |
| `.tbss` | 57 | 57 |
| `.fini_array` | 8 | 8 |
| `.init_array` | 3872 | 3872 |
| `.data.rel.ro` | 2998152 | 2998152 |
| `.dynamic` | 544 | 544 |
| `.got` | 1552 | 1552 |
| `.relro_padding` | 3496 | 3432 |
| `.data` | 37160 | 37160 |
| `.tm_clone_table` | 0 | 0 |
| `.got.plt` | 2728 | 2728 |
| `.bss` | 549978 | 549978 |
| `.gnu_debuglink` | 20 | 20 |
| `.shstrtab` | 305 | 305 |

只有.dynstr大小增加52B、.relro_padding减少64B，文件总大小增加64B；不能据此断言代码布局/性能相同。
本轮没有性能测量，也没有将节区大小相等当成图等价证明。

### 6.2 30 TU逐字节门禁

两边均以`clang-22 --driver-mode=g++`调用；显式同一R/usr/lib64 loader/runtime、
同一TC/usr/lib64/clang/22资源目录、同一目标sysroot、同一sidecar flags、同一cwd和输出文件名。
沿用tools/verify_compiler_outputs.py；CPU2、4GiB AS、ASLR off、tmpfs，实际比较完整.o的cmp退出码。
不删除-frecord-gcc-switches，不跳过.GCC.command.line或其他节区。临时输出工作目录已清理，证据.o另存E。

| 集合 | target / sysroot | 数量 | 结果 | 编译最大RSS KiB |
| --- | --- | ---: | --- | ---: |
| ARM训练 | armv7l-tizen-linux-gnueabi / scratch.armv7l.0 | 10 | **10/10 PASS** | 691640 |
| ARM留出 | armv7l-tizen-linux-gnueabi / scratch.armv7l.0 | 10 | **10/10 PASS** | 723544 |
| AArch64训练 | aarch64-tizen-linux-gnu / scratch.aarch64.0 | 10 | **10/10 PASS** | 694728 |

sysroot父路径为`/home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/`。
完整argv、input SHA、两边.o SHA、cmp原始输出与退出码分别保留E/correctness-{arm-training,arm-holdout,aarch64}/。
这是正确性运行，JSON中的计时仅是执行记录，未据此给出性能比值。

| 源文件标签 | ARM训练 | ARM留出 | AArch64 |
| --- | --- | --- | --- |
| arm_ARMISelLowering | PASS | — | PASS |
| arm_ARMTargetTransformInfo | PASS | — | PASS |
| codegen_MachinePipeliner | PASS | — | PASS |
| codegen_SelectionDAG | PASS | — | PASS |
| mc_AsmParser | PASS | — | PASS |
| mc_MasmParser | PASS | — | PASS |
| sema_SemaExprCXX | PASS | — | PASS |
| sema_SemaStmt | PASS | — | PASS |
| transforms_Attributor | PASS | — | PASS |
| transforms_WholeProgramDevirt | PASS | — | PASS |
| aarch64_AArch64InstructionSelector | — | PASS | — |
| analysis_ScalarEvolution | — | PASS | — |
| ast_ParentMapContext | — | PASS | — |
| driver_Driver | — | PASS | — |
| frontend_codegen_CoverageMappingGen | — | PASS | — |
| ir_Metadata | — | PASS | — |
| object_ELF | — | PASS | — |
| parse_ParseDecl | — | PASS | — |
| profiledata_InstrProfReader | — | PASS | — |
| x86_X86ISelDAGToDAG | — | PASS | — |

输入仍来自tools/bench_inputs/real_tu、holdout_tu、real_tu_aarch64原有sidecar，无新预处理、profile或基准校准。

### 6.3 profile v2适用性

H与TC的RPM ELF SHA不同，不能走“相同身份直接沿用”的判断。
更严格地，v2 profile实际绑定的是旧Q/stripped输入SHA
`eccfb075bc3b2a6ca2bda5a2a6e68f6a29ba48b5586cb603f4b46080f656013e`，而不是TC的RPM SHA。
本轮未为H生成新的relocs/stripped输入，因此新profile输入身份和代码图适配均**未认证**。
后续须走docs/21 §3.2第二级图重认证（提取器尚未认证）或重新训练；本轮不执行两者。
30 TU相同证明这些输入的代码生成一致，不能推出clang自身代码图/布局一致，也不能认证旧profile可直接用于H。

## 7. 自检与后续处置

| 自检 | 回答 |
| --- | --- |
| 修订是否先提交推送再构建 | 是，8facdfa先推送，随后才建worktree/启动GBS |
| 原分支、原spec及历史协议文件是否保持 | 是，E/protected-after.json全部SHA相同；原分支仍sandbox/fangyu.he/llvm_optmize，原4/4/1差异未动 |
| 是否只应用批准补丁 | 是，隔离hybrid-link-trial七文件；没有修补失败后重试，没有额外spec优化改动 |
| 18GiB/4-4-1/debuginfo4/采样回收 | 全部实现并有原始证据；完整构建成功，scope最终inactive，未向其他指纹开放 |
| 产物链接与包范围是否全部满足 | 三个实体/别名和八个抽查共享工具通过；五个额外静态工具未满足范围 |
| static-devel索引是否可发货 | 否；原包223空索引+3残缺索引；一次普通ranlib仅补空，三残缺仍在；消费者验收未做 |
| 30 TU是否完整逐字节相同 | 是，30/30 PASS；编译峰值小于4GiB AS限制；没有排除节区 |
| profile/BOLT/性能校准/Chromium/OBS/Gerrit | 均未执行 |
| 是否完成提交推送与STATUS同commit | 本报告、构建/活性脚本及测试、指纹、STATUS同一结果提交；提交身份从Git定位 |

后续需要评审的具体问题：①五个强制静态例外如何满足范围；②归档修法改为避免GNU strip处理.a，
或另设计能强制重建**残缺**表的方法，并执行bfd/lld组件消费者及坏例；③混合输入profile重认证。
当前结果只许可表述“本机一次构建与30TU正确性通过”，不发货、不进OBS，不隐含第二次试构建授权。

## 8. 原始证据索引

原始输出全部保留在`/home/linhao/Toolchain/development/llvm-optimize/temp/hybrid-trial-20260922/`，不上传：

| 路径（相对E） | 内容 |
| --- | --- |
| revision/ | 第一个提交的原件SHA、原三处并发diff、获批补丁与功能/规则测试 |
| applied-source.diff、applied-source-sha256.json | 隔离分支应用后的完整源码差异、摘要 |
| preflight/、preflight-console.log | 资源、仓库、宏与机制预检全部命令/输出 |
| run/launch.json、run/commands.log | 执行前完整命令与预检原始输出 |
| run/resource-plan.json、run/source-fingerprint.json | 实际资源计划和完整配置/源码身份 |
| run/build.log、run-console.log | 带时间戳GBS输出、外层门禁状态 |
| run/CMakeCache.txt、run/cache-gate.json、cache-key-lines.txt | 完整配置及302.105秒门禁结果 |
| exported.spec、exported-spec.diff、exported-source-check.json | GBS导出差异与构建根获批源文件摘要 |
| ninja-commands.txt、link-command-summary.json | 只读生成图与三个静态工具链接命令 |
| run/samples.jsonl、run/process-memory.jsonl、run/linker-memory-observations.jsonl | 30秒宿主/scope采样、2秒进程高水位与链接目标 |
| resource-summary.json | 原始采样汇总；累计VmHWM仍有采样遗漏界限 |
| build-gates-final-tests.log、liveness-tools-tests.log、liveness-tools-test/ | 14项构建准入/回收/响应文件测试及clang/lld活性功能检查 |
| link-target-map.json、scope-reaped.json、protected-after.json | response链接PID关联、scope退出、原件未变 |
| products/、five-tools.json、identity-*.log、liveness-{clang,lld}/ | RPM/ELF/别名/身份/活性全部命令与输出 |
| archives/ | 每个开发归档、一次修复副本、残缺表复核及已知坏例 |
| clang-comparison/、correctness-*/、correctness-summary.json | ELF节区/符号表与30TU完整cmp证据 |
| remaining-static-source-evidence.txt、build-milestones.txt | 静态例外、ranlib源码与构建阶段摘录 |
| known-bad-armap.txt | 已知坏liblldCOFF.a的非空普通符号输出，但缺失Archive map负例 |

## 附录 A：试验工作树相对HEAD的完整diff

包括原先已有的三处并发4/4/1变更及获批七文件混合补丁：

```diff
diff --git a/clang/cmake/modules/AddClang.cmake b/clang/cmake/modules/AddClang.cmake
index 4059fc3e986c..8583bbcaf4d1 100644
--- a/clang/cmake/modules/AddClang.cmake
+++ b/clang/cmake/modules/AddClang.cmake
@@ -107,6 +107,7 @@ macro(add_clang_library name)
     set_property(GLOBAL APPEND PROPERTY CLANG_STATIC_LIBS ${name})
   endif()
   llvm_add_library(${name} ${LIBTYPE} ${ARG_UNPARSED_ARGUMENTS} ${srcs})
+  tizen_hybrid_llvm_interface(${name} ${ARGN})

   if(MSVC AND NOT CLANG_LINK_CLANG_DYLIB)
     # Make sure all consumers also turn off visibility macros so they're not
diff --git a/clang/tools/driver/CMakeLists.txt b/clang/tools/driver/CMakeLists.txt
index 002aaef00525..b7f70845f695 100644
--- a/clang/tools/driver/CMakeLists.txt
+++ b/clang/tools/driver/CMakeLists.txt
@@ -39,7 +39,18 @@ if (CLANG_BOLT AND NOT LLVM_BUILD_INSTRUMENTED)
   endif()
 endif()

+set(tizen_static_link)
+if(TIZEN_HYBRID_LINK)
+  if(BUILD_SHARED_LIBS OR LLVM_TOOL_LLVM_DRIVER_BUILD)
+    message(FATAL_ERROR "Tizen hybrid requires component archives and separate drivers")
+  endif()
+  set(tizen_static_link DISABLE_LLVM_LINK_LLVM_DYLIB)
+  set(USE_SHARED "")
+  set(CLANG_LINK_CLANG_DYLIB OFF) # Directory-local; other clang tools keep ON.
+endif()
+
 add_clang_tool(clang
+  ${tizen_static_link}
   driver.cpp
   cc1_main.cpp
   cc1as_main.cpp
@@ -54,6 +65,10 @@ add_clang_tool(clang
   GENERATE_DRIVER
   )

+if(TIZEN_HYBRID_LINK)
+  set_property(TARGET clang PROPERTY TIZEN_STATIC_LLVM ON)
+endif()
+
 setup_host_tool(clang CLANG clang_exe clang_target)

 clang_target_link_libraries(clang
diff --git a/lld/cmake/modules/AddLLD.cmake b/lld/cmake/modules/AddLLD.cmake
index 37f73afa915f..6866e7fc87fc 100644
--- a/lld/cmake/modules/AddLLD.cmake
+++ b/lld/cmake/modules/AddLLD.cmake
@@ -11,6 +11,7 @@ macro(add_lld_library name)
     set(ARG_ENABLE_SHARED SHARED)
   endif()
   llvm_add_library(${name} ${ARG_ENABLE_SHARED} ${ARG_UNPARSED_ARGUMENTS})
+  tizen_hybrid_llvm_interface(${name} ${ARGN})

   if (NOT LLVM_INSTALL_TOOLCHAIN_ONLY)
     get_target_export_arg(${name} LLD export_to_lldtargets UMBRELLA lld-libraries)
diff --git a/lld/tools/lld/CMakeLists.txt b/lld/tools/lld/CMakeLists.txt
index 8498a91597a9..10e89babffa1 100644
--- a/lld/tools/lld/CMakeLists.txt
+++ b/lld/tools/lld/CMakeLists.txt
@@ -3,12 +3,26 @@ set(LLVM_LINK_COMPONENTS
   TargetParser
   )

+set(tizen_static_link)
+if(TIZEN_HYBRID_LINK)
+  if(BUILD_SHARED_LIBS OR LLVM_TOOL_LLVM_DRIVER_BUILD)
+    message(FATAL_ERROR "Tizen hybrid requires component archives and separate drivers")
+  endif()
+  set(tizen_static_link DISABLE_LLVM_LINK_LLVM_DYLIB)
+  set(USE_SHARED "")
+endif()
+
 add_lld_tool(lld
+  ${tizen_static_link}
   lld.cpp

   SUPPORT_PLUGINS
   GENERATE_DRIVER
   )
+if(TIZEN_HYBRID_LINK)
+  set_property(TARGET lld PROPERTY TIZEN_STATIC_LLVM ON)
+endif()
+
 export_executable_symbols_for_plugins(lld)

 function(lld_target_link_libraries target type)
diff --git a/llvm/cmake/modules/AddLLVM.cmake b/llvm/cmake/modules/AddLLVM.cmake
index d938214f9d0d..b00748adb4fb 100644
--- a/llvm/cmake/modules/AddLLVM.cmake
+++ b/llvm/cmake/modules/AddLLVM.cmake
@@ -1030,6 +1030,40 @@ macro(generate_llvm_objects name)
   endif()
 endmacro()

+# Proposed Tizen hybrid linkage: keep the default shared interface, but
+# provide component dependencies to an explicitly opted-in final consumer.
+function(tizen_hybrid_llvm_interface name)
+  if(NOT TIZEN_HYBRID_LINK OR NOT LLVM_LINK_LLVM_DYLIB OR NOT TARGET ${name})
+    return()
+  endif()
+  get_target_property(kind ${name} TYPE)
+  if(NOT kind STREQUAL "STATIC_LIBRARY")
+    return()
+  endif()
+  get_target_property(iface ${name} INTERFACE_LINK_LIBRARIES)
+  if(NOT "LLVM" IN_LIST iface)
+    # Some components explicitly disable the dylib already (e.g. clangSupport).
+    return()
+  endif()
+  cmake_parse_arguments(H "" ""
+    "LINK_COMPONENTS;LINK_LIBS;DEPENDS;OBJLIBS;ADDITIONAL_HEADERS" ${ARGN})
+  llvm_map_components_to_libnames(components ${H_LINK_COMPONENTS} ${LLVM_LINK_COMPONENTS})
+  set(static_consumer "$<BOOL:$<TARGET_PROPERTY:TIZEN_STATIC_LLVM>>")
+  set(replacement "$<$<NOT:${static_consumer}>:LLVM>")
+  foreach(component IN LISTS components)
+    list(APPEND replacement "$<${static_consumer}:${component}>")
+  endforeach()
+  set(result)
+  foreach(dep IN LISTS iface)
+    if(dep STREQUAL "LLVM")
+      list(APPEND result ${replacement})
+    else()
+      list(APPEND result "${dep}")
+    endif()
+  endforeach()
+  set_property(TARGET ${name} PROPERTY INTERFACE_LINK_LIBRARIES "${result}")
+endfunction()
+
 macro(add_llvm_executable name)
   cmake_parse_arguments(ARG
     "DISABLE_LLVM_LINK_LLVM_DYLIB;IGNORE_EXTERNALIZE_DEBUGINFO;NO_INSTALL_RPATH;SUPPORT_PLUGINS;EXPORT_SYMBOLS"
diff --git a/llvm/tools/llvm-ar/CMakeLists.txt b/llvm/tools/llvm-ar/CMakeLists.txt
index 4d0718f8cefe..2bb0025a0033 100644
--- a/llvm/tools/llvm-ar/CMakeLists.txt
+++ b/llvm/tools/llvm-ar/CMakeLists.txt
@@ -11,7 +11,17 @@ set(LLVM_LINK_COMPONENTS
   TargetParser
   )

+set(tizen_static_link)
+if(TIZEN_HYBRID_LINK)
+  if(BUILD_SHARED_LIBS OR LLVM_TOOL_LLVM_DRIVER_BUILD)
+    message(FATAL_ERROR "Tizen hybrid requires component archives and separate drivers")
+  endif()
+  set(tizen_static_link DISABLE_LLVM_LINK_LLVM_DYLIB)
+  set(USE_SHARED "")
+endif()
+
 add_llvm_tool(llvm-ar
+  ${tizen_static_link}
   llvm-ar.cpp

   DEPENDS
@@ -19,6 +29,10 @@ add_llvm_tool(llvm-ar
   GENERATE_DRIVER
   )

+if(TIZEN_HYBRID_LINK)
+  set_property(TARGET llvm-ar PROPERTY TIZEN_STATIC_LLVM ON)
+endif()
+
 add_llvm_tool_symlink(llvm-ranlib llvm-ar)
 add_llvm_tool_symlink(llvm-lib llvm-ar)
 add_llvm_tool_symlink(llvm-dlltool llvm-ar)
diff --git a/packaging/llvm.spec b/packaging/llvm.spec
index 54a07ce84218..d7c8e74eb843 100644
--- a/packaging/llvm.spec
+++ b/packaging/llvm.spec
@@ -45,7 +45,7 @@ Source1002: mlgo_arm_model.tar.gz
 Source1003: mlgo_aarch_model.tar.gz
 Source1004: mlgo_x86_model.tar.gz

-%{!?mlgo_build_jobs: %define mlgo_build_jobs 6}
+%{!?mlgo_build_jobs: %define mlgo_build_jobs 4}
 %{!?mlgo_verify_configure_only: %define mlgo_verify_configure_only 0}

 BuildRequires: cmake
@@ -256,6 +256,13 @@ cmake \
 %endif
     -DCLANG_ENABLE_ARCMT=OFF \
     -DLLVM_BUILD_LLVM_DYLIB=ON \
+    -DLLVM_LINK_LLVM_DYLIB=ON \
+    -DCLANG_LINK_CLANG_DYLIB=ON \
+    -DBUILD_SHARED_LIBS=OFF \
+    -DLLVM_TOOL_LLVM_DRIVER_BUILD=OFF \
+%ifarch x86_64
+    -DTIZEN_HYBRID_LINK=ON \
+%endif
     -DCLANG_BUILD_CLANG_DYLIB=ON \
     -DLLVM_ENABLE_PROJECTS="clang;lldb;clang-tools-extra;lld;compiler-rt;openmp" \
     -DLLVM_ENABLE_PER_TARGET_RUNTIME_DIR=OFF \
@@ -271,8 +278,8 @@ cmake \
     -DLLVM_LIBDIR_SUFFIX=`echo %{_lib} | sed s/lib//g` \
     -DCLANG_RESOURCE_DIR="../%{_lib}/clang/%{llvm_version}" \
     -DLLVM_BINUTILS_INCDIR=/usr/include \
-    -DLLVM_PARALLEL_COMPILE_JOBS=6 \
-    -DLLVM_PARALLEL_LINK_JOBS=2 \
+    -DLLVM_PARALLEL_COMPILE_JOBS=4 \
+    -DLLVM_PARALLEL_LINK_JOBS=1 \
 %if %{with mlgo}
 %ifarch armv7l aarch64 x86_64
     -DTENSORFLOW_AOT_PATH="${MLGO_AOT_DIR}/mlgo_sysroot" \
```
