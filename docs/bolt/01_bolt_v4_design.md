# 01 Tizen LLVM BOLT 集成设计 v4.1：Quickbuild sandbox 第一版

修订：2026-10-14（Asia/Shanghai）。**最新裁决与执行记录在附录末尾，旧v4保留为历史设计。** 原地重链/早期匹配已PASS；同树配置失败后，原因诊断发现RPM与本地PATH不一致。本轮临时baseline因源布局准备错误STOP，尚未认证spec、恢复原树或生成正式候选；见14。

原v4日期：2026-10-12（Asia/Shanghai）。目标周五2026-10-16前交付Quickbuild试验材料，周四只对补丁做一轮外部评审；本轮不构建LLVM、不打RPM、不上传Gerrit。本文为自包含实施与验收设计，尚无生产集成补丁或新RPM。今晚实测和未测项分别标明，不能以历史PASS替代新配方认证。

W=`/home/linhao/Toolchain/development/llvm-optimize`；B=`/home/linhao/Toolchain/development/llvm-optimize-bolt`，分支bolt-v4；E=`W/temp/bolt-v4-20261013`（目录名按用户指定，实际开场日期为10-12）。完整路径/SHA盘点见[02_inventory.md](02_inventory.md)，实验矩阵见[03_strip_experiments.md](03_strip_experiments.md)。这些链接为补充，本设计的关键决策、步骤、证据和门禁均在正文。

## 1. 冻结目标、范围与v3变更

人工裁决2026-10-12共九项，不擅自改变：

1. 周五10-16前交付BOLT补丁用于Quickbuild试验；试验不上Gerrit。
2. 第一版仅x86_64构建分支、仅clang；lld/llvm-ar以后再做。保持现有工具静态链接LLVM库，不引入混合链接；llvm-static-devel照常发布。静态LLVM库不等于静态libc。
3. 直接使用现成profile v2，作为spec的Source提交，不单独打profile RPM；构建内不匹配函数比例≤5%，超过则构建失败。
4. 首版不要求BOLT clang源码级DWARF，但经过完整RPM后处理（find-debuginfo、strip等）后必须能运行。
5. 补丁基线为tizen_base cb67996861d070d68fec2b4c623eed7d20ba2e23叠356627 PS3、356639 PS2候选，同时干净应用到裸cb679968。
6. 不得引起其他LLVM消费者RPM编译错误、运行时性能下降或运行内存升高；BOLT前后完整.o逐字节相同。LLVM自身构建内存显著增加须报告。
7. 新写shell全部POSIX sh，适应总部bash→dash；不复用旧Bash身份/活性脚本作为新生产入口。
8. 周四仅对补丁做一轮外部评审。
9. 周三晚使用归档会话完成的x86完整树续跑：只重链clang、BOLT、打包；周四验证与评审，周五交付。不能自动替换成历史树。

| docs/21 v3设计项 | v4处置 | 原因 |
|---|---|---|
| 混合链接及七文件源码补丁 | 不进入首版 | 本周静态配方、最小clang范围已冻结 |
| 独立noarch profile RPM、同job seed、自举和图rebind系统 | profile v2 Source+不可变manifest；不采集/不重训 | 本周使用已得数据，避免新增发布链 |
| BOLT失败自动产普通RPM | 显式BOLT试验任何硬门禁失败即失败 | 用户要求≤5%匹配及正确性，不能把降级产物标为BOLT成功 |
| 外部builder工具RPM | 必须在spec可复现地提供工具；推荐同源私有工具子构建 | 当前spec没有bolt项目，历史工具只是本地实验产物 |
| strip存活仅风险登记 | 选择llvm-strip --strip-debug，clang专用包装器；完整后处理门禁 | 本轮GNU/eu-strip退出0而失活；LLVM路径已有轻量证据 |
| 保留身份/alias/逐层存活要求 | 保留，改成POSIX入口 | qemu-accel修改ELF，版本字符串不区分A/B |

历史事实：profile v2训练为ARM13+AArch6410；旧BOLT v2对30个真实源文件（ARM训练10、ARM留出10、AArch6410）完整.o逐字节相同。AArch64最终筛选校准通过，训练口径耗时降低约15%；ARM最终噪声校准FAIL，未证明不退化。对外只说“方向一致的正向影响，量级待服务器验收”。不把微型C烟测或训练收益解释成其他RPM运行性能保证。

## 2. 输入、补丁身份与profile适用性

| 固定输入 | 身份 / 内容 |
|---|---|
| LLVM源码目标 | cb67996861d070d68fec2b4c623eed7d20ba2e23 |
| 历史profile来源配方 | f111162e94aa48ed367c9d2c039456c70e7160ae；O3/ThinLTO/LLVM库静态；含x86 MLGO |
| v2 profile | W/temp/bolt-aarch64-v2-20260921/profile-work/merged-v2.fdata；171232190B；SHA256 d9b132f9430dfed32e080c65b4422bd76eba4a9c2101a2b18a7f66c94133b326 |
| 历史去debug带relocs输入 | W/temp/bolt-measurement-20260918/run/stripped/bin/clang-22；226730672B；eccfb075bc3b2a6ca2bda5a2a6e68f6a29ba48b5586cb603f4b46080f656013e |
| 历史BOLT v2 | W/temp/bolt-aarch64-v2-20260921/optimized-v2/bin/clang-22；218881120B；f26b65625897189bd38ae02eb8b4cf5854ada84c08be9be3943f241dea647637 |
| 历史RPM基线 | W/temp/toolchain-baseline/usr/bin/clang-22；139929464B；3283505cdfebae8a211b0d5fb7befbe5295812787554eb1199ee52e3cfc4a61c |

开场PS3/PS2候选SHA以02_inventory封存表为准；spec Source1005已由归档修复占用。BOLT拟用Source1006（profile）、1007（manifest）和1008（集成帮助脚本包）；实施前对裸基线与叠补丁基线检查编号冲突。profile超过仓库10MB限制，不提交到此GitHub证据仓库；实际Tizen/OBS Source上传作为独立文件或固定内容压缩归档，解压后核对上述SHA。压缩大小UNKNOWN；不能把大文件拆片或把本机绝对路径写进spec来规避Source供应链。

两spec都未启用bolt。cb679968的x86分支显式LLVM_LINK_LLVM_DYLIB=OFF、CLANG_LINK_CLANG_DYLIB=OFF；f111162e的历史cache/ELF也实测静态。两提交LLVM/clang/bolt源目录无差异，但cb679968改了x86编译器选择、_toolchain前置定义及优化flags处理；其余源码差异在libcxx/libcxxabi与独立runtime配方。现profile**可作为候选直接读取，适配新clang仍UNKNOWN**。周三实际匹配门禁决定是否可用，不凭同主版本或源目录相同放行。

manifest钉source/spec/两patch/MLGO资产、CMakeCache关键参数、构建driver/linker/工具SHA、profile SHA、历史输入SHA、训练清单与flags及新输入SHA；文件名相同不能证明来源相同。旧profile不修改；新配方SHA不同是明确资格验证，不能伪造旧输入SHA。若匹配失败，本周BOLT试验构建失败并交PM，不能自动重训或改链接形态。

## 3. llvm-bolt来源与构建方案

当前spec项目列表：clang;lldb;clang-tools-extra;lld;compiler-rt;openmp；没有bolt。现成llvm-bolt位于历史R1/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-bolt，R1为W/temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0；648678768B，SHA256 1da7bb735f7bc1afab9a863154260699b0b0f88c6fd05b99231dd21ef653fd5a。自报LLVM22.1.8、BOLT revision unknown，必须用SHA/源构建记录定位，不能把unknown当版本证明。perf2bolt是llvm-bolt软链接；merge-fdata独立；首版都不调用后二者。

推荐生产spec在x86普通LLVM成功构建后，以同Source0的bolt/为源做**私有standalone BOLT子构建**，指向刚产出的LLVM CMake exports与静态组件，仅构建llvm-bolt目标，不执行私有子树install。源码bolt/CMakeLists.txt支持standalone find_package(LLVM)，BOLT工具不是从宿主PATH随意取得。主LLVM项目列表无需加入bolt，避免把LLVMBOLT*.a、BOLT工具和symlink规则意外收入static-devel/主RPM。示意命令仅为周三计划，今晚未执行：

```sh
# 在新认证树的build内；LLVM_CMAKE_DIR必须指向实际生成的LLVMConfig.cmake。
: "${LLVM_CMAKE_DIR:?}" "${BOLT_SOURCE_DIR:?}" "${BOLT_TOOL_DIR:?}"
test -f "$LLVM_CMAKE_DIR/LLVMConfig.cmake" || exit 1
cmake -S "$BOLT_SOURCE_DIR" -B "$BOLT_TOOL_DIR" -G Ninja \
  -DLLVM_DIR="$LLVM_CMAKE_DIR" -DCMAKE_BUILD_TYPE=Release \
  -DBOLT_TARGETS_TO_BUILD=X86 -DBOLT_ENABLE_RUNTIME=OFF \
  -DBOLT_INCLUDE_TESTS=OFF -DBOLT_BUILD_TOOLS=ON || exit 1
ninja -C "$BOLT_TOOL_DIR" -j 1 llvm-bolt || exit 1
```

实际子构建必须传同源RTTI/assertion/编译器/平台与必要MLGO链接配置，保存完整CMake argv/cache。纯优化重写不需要BOLT插桩runtime；不构建merge-fdata、不把perf2bolt名称当独立Ninja目标。**standalone与本Tizen/MLGO exports是否完整兼容、只构建llvm-bolt的时间/峰值均UNKNOWN，需先干跑图审查与限定构建验证。** 这不是声称今晚已认证的生产方案。

已实证备选是docs/15在原树项目列表追加;bolt，再ninja llvm-bolt merge-fdata：configure26.426s/peak627392512B，126任务545.525s/peak4907880448B（4.57GiB）。这个9分钟数包含merge-fdata、runtime及少量MLGO依赖，不能直接冒充standalone llvm-bolt单目标成本。在主树启用bolt会增加工具/库install规则，未经逐项排除与非clang产物比对不能使用。BOLT_BUILD_TOOLS=OFF只限制工具默认ALL，不能据此保证所有BOLT库/别名不安装。

周三“只重链/BOLT/打包”入口若新树没有llvm-bolt，可先使用**明确复制、验证SHA且单独登记的既有22.1.8历史工具**做资格实验（源码bolt在两提交间相同），不把它冒充生产spec自构建工具。可复现Source构建工具与同版本静态运行依赖必须在周四补丁定稿前闭合；否则只得到本地资格实验，不能声称补丁能独立构建。这项工具准备不能悄悄变成整棵LLVM重建。

## 4. spec集成流水线（仅x86_64）

新增opt-in `%bcond_with clang_bolt`，只在`%ifarch x86_64`声明BOLT Sources并运行阶段；ARM/AArch64/i686普通配方不改。请求BOLT而_toolchain/实际架构/静态库形态不符则失败，不能静默降级。普通A组不请求BOLT；既有static-devel转换/strip宏原样保留。首版不改CLANG_VENDOR、版本宏或clang版本字符串。

### 4.1 正常构建与唯一clang链接边

正常ninja仍走原O3/ThinLTO/MLGO/并发。为响应文件保留，A/B都使用同一支持`-d keeprsp`的ninja；改动不改变编译参数，但要登记容量/文件数。周三已完成树没有rsp时检查是否实际使用rsp；缺必需rsp立即失败，不猜写、不重编对象。

主构建结束保存普通build/bin/clang-22的完整副本与SHA。执行**图工具查询而不是build**，保存唯一最终链接命令：

```sh
set -eu
: "${BOLT_WORK:?}"
mkdir -p "$BOLT_WORK/ordinary" "$BOLT_WORK/relocs"
cp -p bin/clang-22 "$BOLT_WORK/ordinary/clang-22"
ninja -t commands -s bin/clang-22 > "$BOLT_WORK/link.original" || exit 1
```

历史命令是`: && /bin/x86_64-tizen-linux-gnu-clang++ ... -o bin/clang-22 ... && :`。解析器只接受认证结构、恰好一个最终命令/输出/depfile；保持原shell引号特别是`\$ORIGIN`，不使用eval、不做简单空白split后重组。只改输出与依赖文件为BOLT工作目录，尾部追加-Wl,--emit-relocs；不向全局CMAKE_EXE_LINKER_FLAGS添加，不重链其他工具。

完整登记对象/归档（含顺序）、响应文件递归内容/SHA、链接脚本、driver/linker、cwd/env与MLGO对象。保存同一原始shell环境；未知额外map/save-temps写出、缺文件或cache身份不符失败。正常热ThinLTO cache保留；周三锁移交后的专用树才可复用其cache，记录命中与写入，不与归档会话并发。若要复制独立cache，必须是完整同版本热cache，不从冷目录套用历史热链接峰值。

未来实施的重链脚本应生成经审查的POSIX `link.replay.sh`，在同cwd/env以`sh`执行；输出`relocs/clang-22`及独立`clang-link.d`。现有tools/relink_clang_for_bolt.py硬编码旧基线/cap与Bash入口，不能直接拿来处理新cb树，需实现限定解析而非直接运行历史脚本。

### 4.2 去DWARF与唯一重写

relocs副本先llvm-strip --strip-debug，保留.symtab、.rela.text和非debug重定位；比较非debug ALLOC payload与重定位记录。不使用--strip-all作为BOLT输入。今晚3.56GB完整debug输入在2GiB cap预剥离OOM；该新剥离输入及重写串联未完成，因此周三须先测合适的串行预剥离预算，不能当成本≤2GiB。

```sh
: "${LLVM_STRIP:?}" "${LLVM_BOLT:?}" "${PROFILE:?}" "${BOLT_WORK:?}"
cp -p "$BOLT_WORK/relocs/clang-22" "$BOLT_WORK/clang.input"
"$LLVM_STRIP" --strip-debug "$BOLT_WORK/clang.input" || exit 1
"$LLVM_BOLT" "$BOLT_WORK/clang.input" \
  -data="$PROFILE" -o "$BOLT_WORK/clang.candidate" \
  -reorder-blocks=ext-tsp -reorder-functions=cdsort \
  -split-functions -split-all-cold -split-eh -dyno-stats \
  --thread-count=1 -stale-threshold=5 \
  > "$BOLT_WORK/bolt.log" 2>&1 || exit 1
"$LLVM_STRIP" --strip-debug "$BOLT_WORK/clang.candidate" || exit 1
```

参数保持docs/20 v2，不加instrument、infer-stale-profile、update-debug-sections。后剥离选LLVM以保留BOLT note并使后处理判定稳定；不能用GNU strip/objcopy/eu-strip再写BOLT候选。记录各层输入输出SHA、LOAD、入口、节区payload与工具SHA。profile解析门禁和第5节三目标门禁在安装前执行，失败即整个BOLT构建失败。

### 4.3 安装实体与别名

原install完成后，只替换安装根usr/bin/clang-22；先枚举软链接链和原实体的全部硬链接/路径，在安装根内解析，逃逸/循环或未知复制体失败。clang、clang++、triple-clang等同一家族都必须路由到新实体，不能留旧普通副本；lld/llvm-ar和其他工具不改。

建议在替换前将登记的clang硬链接别名规范为到clang-22的相对软链接，记录这项家族内链接类型变化；以临时文件install/move原子替换实体。若必须保留硬链接类型，就用**预先冻结的路径组**路由后处理，不能处理完主实体后动态按inode重新发现：llvm-strip可能原子换inode，硬别名会脱离原组。后处理结束先比较各路径内容，再重建硬链接或规范为软链接；任一别名仍为旧SHA即失败。路径组保护必须覆盖实际被brp处理的每个家族实体。

### 4.4 find-debuginfo与brp-strip策略

R1实际rpm-build4.14.1.1-1.4：find-debuginfo先objdump -h筛选，debuglink跳过、debug存在才处理、只有gnu.version则already stripped跳过。被选中时debugedit -i→eu-strip --remove-comment -f debugfile ELF；默认后者会破坏BOLT。Tizen brp-strip在无__debug_package时用%__strip -g；PS2只改静态归档strip参数，仍须保护clang。

今晚证据：无debug的v2 ELF在正常路径被find-debuginfo跳过且SHA不变；预先llvm-strip --strip-debug后再执行真实find-debuginfo与真实brp-strip（clang专用LLVM包装器），5个LOAD/BOLT note保留、版本和三个目标逐字节门禁通过。**这只是脚本对副本，不是完整RPM已验收。**

主方案：候选完全无旧DWARF；find-debuginfo照常运行并核查clang未被提取/修改；对brp仅将**登记的BOLT clang路径组**转发至构建树llvm-strip，其他文件透传原/bin/strip，归档仍由PS2的/usr/bin/llvm-strip处理。不要全局把%__strip换成LLVM后连其他可执行文件也改变。包装器必须接受真实brp的单文件-g调用，未知参数/多文件形态失败；路径分组与escape检查由安装manifest提供。

已有脚本的输入正则还会匹配objdump输出中的**绝对文件路径**：路径包含debug可把无DWARF ELF误选中。初次副本放在find-debuginfo命名目录时已实证失活；移到不含debug的路径后跳过。生产执行前对实际绝对buildroot路径与objdump选择结果作硬断言；若会被选中，不能依靠“本来没有DWARF”放行。绝不能注入虚假的.gnu_debuglink骗选择器。

备选：用clang专用包装在find-debuginfo调用前把登记家族实体临时移到**buildroot外**，调用原脚本、恢复，保留其余工具debug处理；持久事务状态/信号恢复/软硬别名都须另验，今晚未测，不自动启用。另一个备选llvm-strip --strip-all轻量能运行、减小文件但删除.note.bolt_info，不作为首选；即使用它也须保留可信manifest并重做全部后处理认证。禁止全包_rpm_strip_disable/--strip-disable，禁止配旧DWARF。

post_brp强制门禁必须接在**完整原__spec_install_post的末尾**（所有debug/arch/os/ISU步骤之后、RPM写出之前），保存现有宏展开再追加finalizer；不能覆盖成简化宏导致其他步骤丢失。%check不承担唯一门禁，以免--nocheck绕过。所有工具/活性/三目标编译检查真实返回码，brp内部`|| :`不能吞掉最终门禁。RPM写出后再独立解包检查最终实体/别名/可信manifest，不能把buildroot临时SHA直接称为RPM内SHA。

## 5. 构建内硬门禁与匹配度定义

同一新构建的普通clang、relocs重链clang、BOLT候选和post_brp clang依次验证。今晚以旧RPM对历史BOLT检查仅证明该输入，不替代未来基线。

profile匹配至少钉N（非空profile函数）、S（invalid/stale函数）、U（未消费的profile函数对象）、Q（non-simple有profile但不能优化），工具与日志格式固定。源码BinaryPasses.cpp输出S/N与-stale-threshold拒绝，但DataReader.cpp另外统计NamesToBranches中unused对象；**仅加-stale-threshold=5不足以覆盖完全没匹配的profile函数**，不能用S/二进制全部函数M当分母。

第一版采用保守可审计的操作口径：`R=(S+U)/(N+U)`，以及BOLT自身`S/N`均≤5%；N>0。U来自当前fdata reader未消费记录；N不包含Q，省去Q的分母使R更保守。Q只登记“不被优化”，不冒充stale。非空覆盖N/M作为诊断保存，不把v3的10%覆盖门槛悄悄加成本次用户裁决。S/U缺行只在**已认证工具SHA/格式、完整成功日志、禁infer-stale**条件下可判0；截断、缺N、重复矛盾行、解析错误、N≤0均失败。用整数`100*(S+U) <= 5*(N+U)`比较，恰好5%允许、超过失败，不用显示四舍五入后的百分比裁决。实施时对别名/LTO聚合的reader消费语义与日志计数作夹具认证，不能把未知objects计数生硬当函数率；无法证明口径就失败并报UNKNOWN。

历史v2 N=23592、M=144032、S=0、Q=383；历史完整日志另有profile for 1 objects was ignored，即U=1，保守R=1/23593约0.00424%；不由N推断U。新cb输出暂无，profile适用性UNKNOWN。资格实验不打开infer-stale来“修好”门禁。

固定微型C源不依赖headers/sysroot，编译器显式使用同资源目录、源/cwd/输出文件名和flags。最少三个目标：armv7l-tizen-linux-gnueabi、aarch64-tizen-linux-gnu、x86_64-tizen-linux-gnu；各`-c -O2`。可实现为下面POSIX片段（同输出路径，保存后逐字节cmp）：

```sh
set -eu
: "${CC_ORDINARY:?}" "${CC_CANDIDATE:?}" "${GATE_DIR:?}" "${RESOURCE_DIR:?}"
mkdir -p "$GATE_DIR"
cd "$GATE_DIR"
cat > tiny.c <<'C'
unsigned bolt_probe(unsigned x, unsigned y) { return (x * 33u) ^ (y + (x >> 3)); }
int bolt_branch(int x) { return x < 0 ? -x : x * 7 + 1; }
C
"$CC_ORDINARY" --version > ordinary-version.txt 2>&1 || exit 1
"$CC_CANDIDATE" --version > candidate-version.txt 2>&1 || exit 1
for triple in armv7l-tizen-linux-gnueabi aarch64-tizen-linux-gnu x86_64-tizen-linux-gnu
do
  "$CC_ORDINARY" --target="$triple" -resource-dir "$RESOURCE_DIR" \
    -c -O2 tiny.c -o same.o || exit 1
  cp same.o "$triple.ordinary.o" || exit 1
  "$CC_CANDIDATE" --target="$triple" -resource-dir "$RESOURCE_DIR" \
    -c -O2 tiny.c -o same.o || exit 1
  cmp "$triple.ordinary.o" same.o || exit 1
done
```

native buildroot可直接运行；宿主外测必须对两clang用同显式loader/library-path，不能混入ARM binfmt。另检查Machine=x86_64、无libLLVM/libclang-cpp直接NEEDED、新LOAD覆盖入口且可执行、BOLT note/ALLOC节区完整。每个命令失败、任何.o差异、失配>5%、post_brp失活都构建失败并保留证据，停止试包，不自动发普通RPM。

负对照预注册：profile缺失/坏SHA/错格式、5%边界/刚超边界、缺N/S/U计数、infer-stale误入、strip退出0但失活、别名留旧内容、--nocheck跳过、工具缺失、OOM/超时。每个应在RPM写出前失败；不是只测试脚本字面存在。

## 6. 时间、内存与体积

| 阶段 | 已测历史数据 | 新配方边界 |
|---|---|---|
| 单clang emit-relocs热重链（docs/14） | 227.656s；lld VmHWM9.760868GiB；scope peak10.451344GiB | 约4分钟参考；冷链接曾16.83GiB，新cb可能不同；不相加到普通构建峰值 |
| LLVM BOLT工具增量（docs/15） | configure26.426s；126任务545.525s；scope峰4.57GiB | 含额外目标；standalone/仅llvm-bolt成本UNKNOWN |
| 历史GNU objcopy去debug（docs/18引用docs/15） | time MaxRSS4.298679GiB；scope峰2921844736B | 不代表LLVM工具或新输入成本 |
| 今晚llvm-strip处理3.56GB debug重链输入 | 2GiB cap OOM，未产生认证输入 | 明确容量风险；不抬今晚cap，周三独立测实际高水位 |
| v2纯重写（docs/20附录D） | 自身24.43s/3.678791GiB；scope26.3246s/3886170112B；6GiB cap、OOM0 | 约25秒参考；不含DWARF更新，不保证新cb输入 |
| 完整debuginfo（docs/13） | -j4约14:51，clang eu-strip VmHWM约3.21GiB | BOLT完整RPM链增量UNKNOWN，须重验 |

本轮轻实验2GiB，BOLT重写许可6GiB；准入MemAvailable8/10GiB、运行观察低于3GiB立即终止，nice19/ionice3，swap0，串行。今晚因预剥离OOM未实际运行新的llvm-bolt重写，不把历史6GiB记录写成今夜PASS。

周三预算建议：继续归档会话已批准的完整父cgroup上限，不擅自提高；热重链独立串行阶段预留至少历史scope10.45GiB余量，建议16GiB阶段上限；预剥离可建议6GiB但需**新任务资源裁决**；纯重写6GiB参考。父剩余预算、控制器和宿主headroom同时核验，不能在chroot内另开绕过父预算的兄弟scope。记录memory.peak/events、进程VmHWM、time-v、宿主采样和并发；显著新增峰值如实报PM，不用插桩19.7GiB峰值冒充优化阶段。

历史RPM clang139929464B→BOLT v2218881120B（+78951656B，约56.4%）；本轮LLVM debug-strip候选218879608B，只少1512B；LLVM strip-all183223048B（比旧RPM+43293584B，约31.0%），但失去BOLT note。clang++软链接不重复算实体。cb候选、RPM压缩/SRPM/profile压缩与最终accel包变化全为UNKNOWN，周三打包实测；不拿docs/21混合体积模型当全静态首版实包预测。

## 7. accel链路及已验/未验

实际ARM包构建执行的是x86_64 clang：x86 LLVM RPM→qemu-accel提取→Base快照→worker /emul/usr/bin/clang-22→交叉生成ARM/AArch64。BOLT只作用于x86_64包，别对ARM ELF做BOLT。

已取得qemu-accel SRPM通用aarch64 spec的动作：从安装的clang/LLVM依赖取文件；cp -aL跟随别名；patchelf --set-interpreter到/emul解释器；只有非空绝对RUNPATH改为emul库路径（$ORIGIN/../lib64不触发）；cmp恢复clang-major相同副本的软链接；fdupes及RPM/baselibs后处理。完整armv7l生成spec/隐式宏仍UNKNOWN。

历史docs/20附录C：BOLT v1副本用patchelf0.16.1改解释器，BOLT节区payload保留，三真实ARM TU完整.o一致；整体SHA变、两note显示顺序变。只证明那个显式转换；**没有认证v2+新strip组合、双次确定性、最终accel RPM或worker**。

发布清单必须有三层ELF SHA（LLVM RPM内、accel RPM内、worker实物），跨patchelf不强求同SHA，要求授权转换+节区/语义门禁；worker应等于accel输出SHA。版本字符串不变、BOLT note存在或RPM归属单项都不是来源证明。非计时诊断保存ninja编译边和execve/execveat trace，确认最终x86 /emul clang，不仅看到ARM wrapper。直接替换worker文件并不建立可交付链路，本轮不部署。

## 8. 周三续跑、周四验证预注册

### 8.1 周三10-14晚：输入移交与增量资格实验

现存历史完整树只有debuginfo-j4-v2、archivefix-v2，均f111162e；不能用于验收cb679968。归档会话周二夜的新cb+PS3/PS2完整x86树**路径UNKNOWN，待其完成后登记**。核验新树源码/补丁SHA是否仍为本次开场候选；如已更新，先报告基线变化，不混用未授权候选。需要release-lock由拥有者释放项目与根双O_EXCL锁，独立确认无重任务，再按移交规则获取；本轮从未获取/等待/删除其锁。

未来续跑顺序：冻结已完成构建的spec/cache/图/driver/普通clang/RPM身份→查询唯一链接边→原环境只重链clang→去debug→profile v2唯一优化→三目标硬门禁→正常install（含既有归档转换）→替换实体/别名→完整原RPM后处理→post_brp硬门禁→打包→独立解包验证。正常install可能重新转换归档，不能人为跳过这两个归档修复；如用户要求时间范围无法容纳该标准步骤，须报告，不私自删除宏。

命令层接口预注册：原新树授权执行器进入内层build后运行第4.1节ninja查询和经过限定解析的`sh link.replay.sh`，再第4.2节命令，日志逐阶段独立存档。打包采用docs/35、38已实证的正常-ba --noprep路径，未来在已移交的新根内以abuild运行，不能在今晚或历史根执行：

```sh
: "${SPEC:?}"
rpmbuild --define '_smp_mflags -j4' \
  --define '_srcdefattr (-,root,root)' \
  --define '_build_create_debug 1' \
  --with clang_bolt -ba --noprep "$SPEC" > rpm-resume.log 2>&1 || exit 1
```

SPEC是新的BOLT集成spec：%build内的候选处理与%install替换/完整post宏均已实施才可调用。启动前做完整ninja干跑/配置指纹核查，普通LLVM边不允许新增任何编译/链接任务；如正常增量路径会重编普通工具，周三“只重链clang”条件不满足即停止，不擅自改ninja图。正常%build重执行配置/无工作ninja的时间另记；standalone工具准备是否另需编译必须提前闭合第3节条件。不要用-short-circuit拼装正式RPM或自行跳过归档转换。GBS/init/chroot的外层具体argv由新树移交时提供并冻结，本文不编造新的GBS stage语法，不复用旧Bash硬编码驱动。帮助脚本接口和最终argv须在补丁评审材料中给齐。

预计普通热重链约4分钟、纯BOLT约25秒；预剥离/工具准备/归档转换/debuginfo/RPM压缩另计。每步保存真实退出码、wall/CPU/cgroup peak/events/进程RSS；任一失败停止后续BOLT试包，保留普通副本及全部日志。

### 8.2 周四10-15：最终RPM、alias、正确性及patchelf

1. 对最终clang RPM与全部LLVM子包记录NEVRA/VCS/SHA，独立解包；检查最终clang实体与所有别名、LOAD/入口、BOLT节区/manifest、NEEDED及--version；禁止把install前候选当最终包。对A/B所有非clang文件记录差异，只有批准的manifest/发行标记允许差异；静态归档结果应保持归档会话认证值。
2. 最终RPM内clang对**同新构建普通clang**运行固定三目标微型门禁。实际默认PT_INTERP路径运行与显式loader诊断均记录；不能只用loader绕过坏解释器而签发。
3. 按用户“30源文件在三个目标”作**30×3=90对**完整.o比较；旧证据只有ARM10+ARM留出10+AArch6410=30对，不冒充90对。旧预处理.ii带固定target，不能盲目跨三个target重用。须从对应30真实源文件在冻结的三个sysroot/resource头/flags重新预处理，保持共同cwd/输出路径、driver-mode=g++与-frecord-gcc-switches；源/头/flags/SHA归档。新预处理是周四验证计划，今晚不采集、不编译大TU。有文件/源依赖缺失则90对验收未完成，不用同一个微型C复制30次代替。
4. 对最终BOLT ELF做与实际qemu动作相同的cp -aL/patchelf副本；同输入独立处理两次比较输出SHA，记录真实工具版本/SHA/解释器/RUNPATH、LOAD和每个BOLT关键节区payload；在可运行对应解释器环境再做三目标微型及同90对.o检查，不能仅显式loader存活而遗漏/emul实际运行。遇到绝对RUNPATH分支按实际新输入追加认证；完整fdupes/alias/accel RPM链取得后另查。
5. 预注册源码级DWARF为“不要求”，不生成旧clang debuglink假配；其他工具/子包debuginfo照常。检查两种__debug_package展开（开/关）及真实post_brp位置、--nocheck仍有门禁；保护wrapper路径范围和原归档strip参数不变。
6. 补丁在两个隔离源副本进行`git apply --check`：裸cb与cb叠指定PS3/PS2；实际顺序apply后比较spec预期tree/宏，证明不覆盖Source1005或PS2。不在W/llvm checkout/apply。完整构建只用叠补丁基线，裸基线干净应用不等于已跑另一全构建。
7. 一轮外部补丁评审材料包括完整spec/helper diff、Source与hash清单、所有失败/跳过、真实命令与最终RPM证据。评审失败修订后是否再评审由用户裁决，不自行增加轮数。

硬约束6最终还要Quickbuild确认：同源码/依赖/flags/资源/caches的A/B完整RPM构建，无编译失败；消费者生成对象一致、下游运行测试与运行内存不增；使用平台认可分辨力的事前阈值，不能以“测不出”解释任何已测退化。LLVM自身构建新增内存另报。A/A、轮序、容差/死区/worker资源由内部团队冻结；本设计不恢复v3已取消的默认容差。此次没有性能测量，也不承诺其他所有RPM已不退化。

## 9. Quickbuild交付物、风险与待答清单

最终交付物：在裸cb及叠PS3/PS2都能应用的spec+POSIX/Python helpers补丁、profile Source文件（171MB未压缩）与manifest SHA、本机构建/完整后处理认证RPM、供Quickbuild使用的输入/输出/工具/accel/worker身份清单和验收记录。当前只交付盘点、轻实验、设计与状态，尚无上述生产补丁/新RPM。

| 交付途径（均待用户确认） | 需要的具体输入/操作 | 是否自动生效 |
|---|---|---|
| 自定义RPM仓库 | repo地址/签名权限与KEY、A/B精确NEVRA及依赖、Quickbuild/accel如何从该repo取工具；重建对应accel或冻结可认可的工具注入路径 | 安装原生LLVM RPM不自动更新已有/emul clang |
| OBS新Base快照 | OBS项目/仓库/架构、上传Source/patch权限、x86 LLVM和qemu-accel构建、生成并固定新Base及repodata、worker选择该快照 | 完整链可生效，需时间/依赖及宏验证 |
| 直接用补丁构建 | Quickbuild实际支持的Source/patch输入接口、执行器/构建配方/源码版本、profile上传位置、怎样把新x86工具放入accel/worker，并保留独立A/B | 只对消费者源码打LLVM补丁不会替换构建器工具 |

| 风险 | 现有证据 | 处理/后备 |
|---|---|---|
| profile新配方失配 | spec参数差异、cb ELF尚无 | ≤5%门禁失败即停止；旧普通包可留作A/回退，但不能冒充B |
| debug预剥离内存 | 今晚2GiB OOM | 周三资源裁决后测高水位；不提高今晚cap，不自动走新profile |
| GNU/eu-strip误判成功 | v2实际崩溃/LOAD0、工具rc0 | LLVM clang路径包装+post_brp硬门禁 |
| find-debuginfo误选 | 文件路径debug文字即可触发 | 对实际选择结果/路径冻结，默认要求跳过；备选显式暂存需另验 |
| 硬alias脱离 | llvm-strip可替换inode | 预先记录全组，规范软链接或按固定路径处理后重建；不动态inode漏组 |
| standalone工具供应 | 源码支持，Tizen/MLGO组合未实测 | 限定干跑/只构建llvm-bolt验证，失效不整树重建；生产来源未闭合则不发可复现声明 |
| RPM/accel变化 | 仅脚本副本和v1单次patchelf旧证据 | 最终RPM/90对/新patchelf双次/worker实物门禁 |
| 其他RPM功能/资源 | 历史30对不是全平台证明 | Quickbuild同条件A/B与下游运行资源验收；发现退化停试验 |
| 构建树/候选变更 | 归档会话正在更新材料 | 开场SHA封存，新树/补丁身份不符先报PM |

待用户回答（按无人值守规则仅列出，不在本轮提问或等待）：选哪种Quickbuild交付路线及项目/仓库/输入接口？周三新cb完整树路径、准确候选SHA和锁移交何时提供？是否允许周三预剥离6GiB参考预算及工具限定子构建、实际父cgroup/并发是多少？何处上传171MB profile Source（压缩格式/限制）？完整qemu-accel armv7l生成材料/宏日志从何取得？三个目标的30真实源文件/sysroot与Quickbuild性能/运行内存协议由谁冻结？

不再把“要不要混合链接、是否撤static-devel、是否单独profile RPM、是否要求首版完整DWARF”当待裁决问题，这些已由九项决策闭合。


## 附录 v4.1 最新修订：单一重链、原地缓存、磁盘底线（2026-10-13晚）

本附录覆盖原正文和上一版 v4.1 的冲突方案。06、07、08及 STATUS 旧段落保留历史状态；本次不重跑它们的实验。今晚只轻任务，不获取共享锁、构建LLVM、运行重链或BOLT，不进归档构建根。正式新树交接后才按周三预注册推进。

### V4.1-1 人工前提与交付身份

Quickbuild当前Tizen-Base-Toolchain定义_toolchain，走debug；未来Tizen-Base未定义_toolchain，走发布，不跑find-debuginfo，GNU brp-strip处理file判为not stripped的可执行文件。x86_64默认%bcond_without clang_bolt；其他架构原流程。两模式交付同一完全strip的BOLT候选，不用brp包装器、不改平台宏或权限。Source/base仍cb679968；不叠356627/356639到sandbox源码，不推本次BOLT提交到Gerrit，周五前不做standalone子构建。

唯一生产路径：仅追加-Wl,--emit-relocs重链→同树llvm-strip --strip-debug→BOLT→匹配度及三目标微型门禁→同树llvm-strip --strip-all→三目标确认→安装clang-22与单次原平台post尾检。删除链接时--strip-debug快路径、双路严格比较及回退，失败构建失败，不能自动降普通包。

依据R1实测：两路非debug ALLOC/全部重定位相同，但符号表相差2,344个STT_FILE；LLVM strip-debug删除它们，链接器strip-debug不删，快路径不合格。reference输入SHAeccfb075…，final strip-all SHA575fc9db9a18c28ad7d8ae12c999ca52b01bc3662fa13b68cedebe89a0b01965，与历史BOLT v2完全strip后SHA相同。旧FAIL仍在07，不以删除比较器抹掉失败。

strip-all前保留候选、检查.note.bolt_info、无debug/gdb_index、合法native ELF/entry/LOAD，记录SHA与BOLT节。strip-all后无.symtab/debug/gdb_index/BOLT note，记录SHA及同树strip工具SHA；前后身份链JSON写构建日志。最终安装clang-22 SHA必须等于strip-all后候选；不要求最终保留BOLT note。普通历史RPM clang无.symtab且file为stripped，与fully stripped BOLT在符号表有无上一致（06）；不是新cb RPM对照证据。

原__spec_install_post完整原链只执行一次，末尾追加安装SHA、ELF/存活、三目标、相对alias终检。候选替换在正常%install尾部，别名从普通实体inode/解析/同内容来源确认并改相对clang-22软链；循环/逃逸/旧内容失败。不在构建内做第二次普通post或完整普通RPM清单对照。

### V4.1-2 同树工具、缓存与重放

普通LLVM先按原不含bolt项目列表完成，保存真实install清单/exports。仅开启BOLT的x86_64追加bolt，BOLT_BUILD_TOOLS=OFF、BOLT_ENABLE_RUNTIME=OFF、BOLT_INCLUDE_TESTS=OFF、BOLT_TARGETS_TO_BUILD=X86，ninja -n llvm-bolt必须没有普通LLVM对象/链接任务，然后ninja -j1 llvm-bolt。再次install后恢复普通exports，按实际manifest差集删除全部新增BOLT产物及空目录；未知新增、普通文件消失或改变失败。完整in-tree工具图/install仍待新树认证；历史llvm-bolt SHA1da7bb73…只作R1资格工具。

**新树不复制ThinLTO缓存。** 归档会话在origin/main docs/STATUS.md正式交接后，该树归本会话使用；clang重链与新增llvm-bolt链接直接引用原缓存，LLD写入或prune均可接受，不再要求原cache前后不变。记录使用的原cache路径/策略便于复现；交接前不得碰新树或以目录存在当交接。

冻结唯一Ninja clang链接边、rsp/环境与输入，默认重放只改output和dependency路径、追加emit-relocs；原cache参数及其余字串逐字保持，保留转义$ORIGIN。helper的--cache-dir保留为可选第三项改写，仅供R1等受保护非交接树：由调用者先准备完整副本，count/bytes/mtime/跨度SHA核对，并在任务前后冻结原cache。不把这个保护策略施加到已交接新树，不在新树重跑副本复制。

profile v2压缩Source9,735,212B、SHA52fd8522b8cceadebfb6bfc0a19f721f1072cff95c682b12b2c4dd5b0cc1e27f；解压171232190B、SHAd9b132f9430dfed32e080c65b4422bd76eba4a9c2101a2b18a7f66c94133b326。BOLT固定ext-tsp/cdsort/split-functions/split-all-cold/split-eh/dyno-stats、thread-count1、stale-threshold5；禁infer-stale/instrument/update-debug。完整成功、认证工具日志提取N/M/S/U/Q；R=(S+U)/(N+U)≤5%且S/N≤5%整数比较，缺失/异常/截断/重复失败，不静默重训。

### V4.1-3 磁盘准入与险情

任何预计单次写入>10GiB：同文件系统free_before−planned_write−reserve必须≥30GiB，不满足即SKIP_DISK，跳过并报告。必须计入临时产物、ELF复制、独立strip输出、新增cache及打包空间；不能预支预计prune释放。按目标实际st_dev核算，/home和/var/tmp分别查可用空间。无法确定预算则停止该项，不用最乐观估计通关。

helper disk-preflight接受路径、声明字节数和可选reserve；大写入30GiB边界与精确10GiB边界有正负夹具。cache-copy按精确原cache字节加4GiBreserve，因此旧危险复制会被拒绝。spec在BOLT开始、工具构建、额外install前分别预检16GiB阶段预算；pipeline用max(16GiB,4×普通ELF大小)，--planned-write-bytes可提高；安装/strip-all副本按实际源大小，rewrite按4×输入估计。16GiB只是温cache R1估计，周三必须核实是否足以包含新树新增cache与临时文件，必要时提高，不能当冷cache上界。各写入阶段开始前重新核算，监控并发归档写盘，准入不是磁盘配额保证。

今天旧任务复制98,248,402,280B后workspace free一度约5.6GB；直到LLD自动prune副本才恢复。此前仅留4GiB重链reserve且复制巨大cache，缺少30GiB底线，属于险情而非安全PASS。对策：正式交接新树原地用cache，以及上述大写入底线。已在STATUS与07备案；今晚只删除旧R1自建copy残余2,365文件/4,671,566,600B，原cache及其他证据不变，详情11/r1-cache-cleanup.json。

### V4.1-4 本地RPM与DWARF对照（双模式）

对照来自正式交接cb679968构建的同模式、不开BOLT的RPM，源/spec/宏/参数/归档修复必须与本地BOLT资格树相同；不能用旧f111162e包冒充。逐包解到新目录，形成main/debuginfo/debugsource限定路径，保存类型、权限、软链目标、每个常规文件SHA；相同大小不够。先证明普通clang家族alias来源。不得新增文件，其他内容逐字节相同，只允许：

- (a) 主包usr/bin/clang-22实体内容变化，及已证明clang家族alias的链接类型变化；最终相对指向clang-22。
- (b) 仅debug：debuginfo缺clang-22自身.debug及其准确.build-id链接。用普通实体build-id/debuglink、debug文件SHA和链接实际目标逐一证明，路径名字不是证明。
- (c) 仅debug：debugsource缺只由clang-22 DWARF引用的源。解析普通clang全部DWARF路径并核对RPM映射，同时扫描所有其他普通ELF/debug输入排除共有引用，逐项保存反向引用集、来源SHA、DWARF dump SHA、全部其他debug输入manifest SHA和缺失项基线。未扫描完整、映射不明或无法证明一律FAIL。

发布只允许(a)，任何(b)(c)差异失败。目录也在当前snapshot，空目录缺失不自动豁免。package-compare是严格清单策略检查器，接受人工审核的真实provenance，不会把调用者随手填写SHA当自动DWARF证明；新树须实际生成/审核。文件清单对照只在本地验证，不加入构建流程；夹具不代替真实RPM。

### V4.1-5 公平30/90对象验证与历史证据

90资产已90/90 .ii完成，缺源/缺头0，30历史selection（ARM训练10、ARM留出10、A64训练10）对应20独立源路径×三目标，完整argv与源/.ii/逐头SHA见09/assets90-manifest.json，677,747,108B输入留旧E。90实际对象尚未做；不能把历史30 PASS当90 PASS。历史30可用.ii在R1公平复测30/30完整对象一致，见07。

Tizen编译参数使.GCC.command.line记录实际编译器路径，不能只改argv[0]。在新的专用目录固定一个常规文件实体路径：先复制普通clang一次，验证SHA、编全部普通对象；再复制BOLT候选到同一实体路径一次，验证SHA、编全部候选对象。输入/.ii、完整argv（保留frecord）、cwd、resource-dir、输出路径均相同，逐个完整.o比较，不过滤任何节或DWARF。30与90两个集合都适用；保存来源SHA和每批槽位SHA，原普通/候选文件不改。每个对象的输出使用同一路径，再分别保存两批输出。新增复制的磁盘预算也受V4.1-3约束。

R1旧双模式小spec实际原post各一次，两模式clang均被选择器跳过；普通控制在debug被FD/eu-strip、release被GNU strip -g处理，RPM clang SHA575fc9db…及三目标PASS（08）。这只证明R1宏机制，不替代生产helper尾检、完整Tizen-Base宏或新树资格。完整execve原日志留旧E，公开JSON给实际成功strip调用及两模式判据。

### V4.1-6 周三10-14续跑顺序与开始条件

开始必须同时满足：归档会话在origin/main docs/STATUS.md明确写READY并正式交接cb679968完整x86树和普通RPM（基线、叠加补丁、source/spec/宏/普通ELF/tool/cache身份、构建验收结果与输出路径）；共享heavy-stage.lock空闲并按约定取得；内存及磁盘预算准入。新树将放/var/tmp，**准确build根与cache路径只取交接STATUS，计划不写死W/temp或猜测目录**。今晚只读Git对象：origin/main=6e874fdbd0149a33167c9b83f8938d17df7c7ceb仍明确BOLT交接NOT READY，无新根/cache/完成指纹；没有进入根。即使随后main更新，必须重新核实正式交接。

1. 接手后先冻结普通身份和同模式RPM，持共享锁先查询普通新clang对v2的匹配度R/S/N；无emit-relocs时只作资格检查。超5%或日志不可信即停，不继承R1历史数值、不自动重训。历史工具结果明确标资格，生产结果仍须同树认证工具。
2. 核实实际磁盘预算后原地用原cache；配置in-tree llvm-bolt并验证dry-run普通任务0，再只构建llvm-bolt。记录新工具版本/SHA/图、全部输入身份。交接树的原cache可正常变动，包括工具链接prune，无需副本或前后冻结审计。
3. 唯一emit-relocs重链→LLVM strip-debug→同树BOLT→整数匹配/前note/三目标→strip-all SHA链→三目标→install差集/exports恢复→末尾安装和alias→单次正常原post→最终SHA/存活/三目标/alias。任一gate失败即停止并报告，不重走快路径。重链没有双路比较，资格只属于交接树配方。
4. 对历史30和新90 .ii按V4.1-5同一实体路径做完整对象对照；可分段持锁，但不能改变flags、丢记录节、复用旧PASS或改目标字段代替真实目标输入。记录耗时/kernel峰/进程VmHWM，失败保留原样。
5. 正常debug打包后在本地逐包对照交接普通RPM，按(a)(b)(c)严格核查全部路径/SHA，并为每个clang debug/build-id与独占source缺失生成、审核普通DWARF/全部其他debug的证据；不得新增，非clang文件逐字节相同。保留不明差异，不扩例外。再做子包/SDK/CMake消费者等尚缺完整验证，更新STATUS。
6. 审核源草案真实适用性：本地资格树可能叠归档修复，sandbox源提交仍以已审核tizen_base基线为准，不把局部本地验收冒充不同recipe的Quickbuild认证。新树匹配、同树工具/安装/post/完整包/30与90/输入与宏一致性、外部评审、Source尺寸与Quickbuild处理检查全部通过，才有条件执行下列未来推送；当前任务仍禁止推BOLT到Gerrit。

后续重阶段独立flock /home/linhao/Toolchain/development/heavy-stage.lock，等≤2h、持≤60min、结束即释；超时跳过并报告，不拿归档项目锁。重cap16GiB/swap0/nice15/ionice3、入口MemAvailable≥12GiB、运行<3GiB立即终止；轻cap4GiB/nice19/ionice3、入口≥6GiB，串行，记录wall/kernel peak/VmHWM。如正式交接树需普通chroot/proc，沿已实证普通chroot mount -n -tproc none /proc、--userspec=1000:1000执行、finally umount/proc并记录三份mountinfo；不使用unshare/私有空间/selfbind/overlay/宿主bind。R1及R32/R64其他原文件只读；原cache只读约束仅对未交接旧树，不对新树。

### V4.1-7 发布分支挂账与未来sandbox推送

进入Tizen-Base前仍须真实未定义_toolchain的完整x86普通/BOLT同配方构建对照：宏/全部post（GNU brp-strip选择）、同树工具与匹配、最终SHA/存活/三目标/30与90完整对象/alias、只允许(a)的逐文件字节与类型对照、其他子包/SDK/CMake消费者、资源与磁盘准入、失败不降普通包。08小spec仅支持完全strip选择器会跳过clang的机制判断，不能替代完整发布构建。本项继续挂账，不在今晚做。

仅在上述真实对应模式资格和外部评审等全部条件通过后，核对远端基线与sandbox，不force；AUDITED_COMMIT为完整已审源码提交，不是本证据仓库HEAD或文本patch：

```sh
git ls-remote ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm refs/heads/tizen_base refs/heads/sandbox/lhmax2025/bolt_pgo
git push ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm AUDITED_COMMIT:refs/heads/sandbox/lhmax2025/bolt_pgo
```

远端基线已变化则停止报告，不能自动重基/review豁免。本轮只推GitHub bolt-v4，sandbox此前仅原样创建基线。Source当前唯一重链版本和静态整树身份在patches/bolt/draft-manifest.json；95fixtures通过，完整新树/真实RPM认证仍未完成。温cache Quickbuild pipeline暂估12–15min/峰约6.04GiB，不含新llvm-bolt编译或正常post，精确边界和R1采样依据见11/single-path-estimate.json。

### V4.1-8 周三执行记录与恢复边界（最新2026-10-14）

历次完整记录分别见12（普通无relocs误探测）、13（修正顺序/重链和早期匹配PASS、同树配置非bolt变化STOP）、14（原因诊断/临时源布局错误STOP），原v4正文与V4.1-1至7不改，旧执行附录已完整保存在GitHub0d78c75。最新授权覆盖旧“先普通匹配”与“不推BOLT”：先emit-relocs/strip-debug再匹配；全部规定门禁及性能geom<0.98后，父cb679968直接sandbox，Gerrit拒绝原文停、不拆profile。

现有重链输入15827504…/226738888B；历史早期N23592/M144032/S0/U1/Q383、R0.004238545%、S/N0% PASS，产物已删。重链scope17.571s/峰13.071GiB、早期scope26.075s/峰3.809GiB，不能沿用旧峰估6.04GiB。正式工具/候选仍无，后续30/90、双模式、DWARF预期清单与性能未做。

新增只读原因：相对compiler缓存，在原RPM登录PATH先/bin，失败本地入口先/usr/bin，导致同一实体的compiler路径拼写变；CMake提示CMAKE_C_COMPILER/CMAKE_CXX_COMPILER变化、自动删cache重配。本地与两宏spec追加命令参数相同，但环境不同；先前“spec缺陷”初判已撤回，尚不能宣称Quickbuild认证PASS。

最新恢复任务要求临时先原配置再追加bolt（不删cache/仅bolt键/链接逐字）PASS，然后原始RPM前导/命令恢复一次、dry-run扣除8触碰和LLDB暂存后≤50编链才-j1补，>50允许历史工具后备。两路线必须候选门禁、30/90、双模式/DWARF、30×5性能合格才推；后备Quickbuild SHA交叉核对条件只在实际生成合格候选后成立。

此次临时baseline因只准备llvm链接、漏同级cmake目录失败而按规则STOP，尚未append；临时目录清理，原树cache/ninja仍上一失败bd8ad3aa…/a37efa6a…未恢复。没有重试/恢复/构建/后备候选/推送。正式草案仍d6ddbff5…父cb679968，未改源码封套；22RPM/归档证据保护通过、proc/scope回收，未取重锁/进ARM。未来tizen_base合归档修复时周五再变基解spec冲突。不能直接在当前失配配置上ninja，原快照在13对应E。


### v4.1-12至14 历史记录

15临时配置PASS但原树恢复FAIL；16历史后备候选4ec07159…门禁PASS，安装遗漏STOP；17修成单次安装/compare-root，103夹具及封套PASS，文本门禁STOP。详见15–17，原树禁CMake/Ninja；未来临时配置专用cache。

### v4.1-15/16 文本补充与续跑七（最新2026-10-15）

18仅RERUN_CMAKE获许可而phony STOP；最新PM扩展为簿记语句对，phony无依赖/变量且输出88删/20增与RERUN完全配对，7439文本块全PASS。来源按PM首次检测/缓存重配判定，对照取消，禁止新CMake配置。Quickbuild tool-plan仍现场把关。

19当前a1410e3d草案debug/release展开PASS，同BOLT段/一次安装/无exports-prune/compare-root次序正确；120输入SHA准备PASS但未编译。同类辅助脚本路径错误第二次触发准备STOP，30/90对象、双模式、RPM-DWARF、性能、sandbox均未做。原树/cache未写，保护审计PASS；候选仍历史后备4ec07159…，源父cb不变。

周四核统计同量级/双5%、tool-plan、compare-root、Quickbuild性能、debugsource实际清单；不比较双方SHA。86配置/tool-plan/完全strip覆盖debug间接读取。细节见18/19/STATUS。
