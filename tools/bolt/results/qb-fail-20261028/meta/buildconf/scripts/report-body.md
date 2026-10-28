
## 6. 用户暂停第三件后的全量 build.conf 调查

本节覆盖前文“只增加一个本地 `_toolchain` 宏”的待裁决建议：**用户未批准该建议，已明确暂停第三件**。不能用LLVM自己的一个宏掩盖Toolchain整个项目的配置变化。以下均为只读调查和静态推导，未构建、未修改任何配置，也未推送Gerrit。

### 6.1 比较范围及完整差异

旧配置精确SHA `e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945`；新Base配置精确SHA `840ef6de94c6d73e3fcced27dc777a399df435a0f2e4017347191a296f5f1975`。两者是固定快照的完整build.conf，非手工摘取宏片段。

[完整逐行diff](../../tools/bolt/results/qb-meta-fix-and-snapshot-20261028/snapshots/build.conf.diff)；[带条件和原行号的逐项分类TSV](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/config-classification.tsv)；[机器可读分类](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/config-classification.json)。分类器保留Macros多行定义和`%ifarch`上下文；没有把六个架构的宏混为一个最终值。另用本机`/usr/lib/build/queryconfig`只读解析两份原件，三个目标×rawmacros/optflags/repotype/target共24项退出0；[完整argv/退出码](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/query-results.json)，同目录`query-*.txt`是输出。它们证明配置可读和分支内容，**不是已完成Tizen RPM环境中的全部spec展开或构建**。

| 分类 | Toolchain → Base 的实际变化 | 原文位置/边界 |
|---|---|---|
| `%define` | `_project`改名；删除`__optflags`，新增`__global_cflags` | 旧L1、354；新L1、281 |
| Macros身份 | `_project`、`distribution`从Toolchain改Base | 两份L5、14–15；其余vendor/version/repository定义不变 |
| 编译器选择 | 删除`_toolchain`、`toolchain_is`、Clang/GCC的`__ar/__ranlib/__cc/__cxx`分派及两套flags | 旧L123–162；Base没有这些项目定义，可能回到RPM平台默认，不能说这些内建宏必定完全未定义 |
| MLGO | 删除ARM/AArch64的`_with_mlgo=1`、`mlgo_build_jobs=6`、`mlgo_verify_configure_only=0` | 旧L115–121；有些spec自带默认值，不能一律说MLGO关闭或并行度改变 |
| 段入口宏 | 删除`%prep/%build/%install`包装；不再由这些包装export AR/RANLIB/CC/CXX，取消该`%install`中的debug_package插入 | 旧L164–177；GBS/平台还可能有其他debug插入机制，需分别检查 |
| Optflags，共六架构 | 默认Clang `-Os`链变为Base `-O2 -fno-inline-functions -fstack-protector-strong`链；GCC专用选项进入Base公共/架构参数 | 旧L354–361；新L281–288。二者仍有`-g2 -gdwarf-4`，不能说新build.conf本身全局删了`-g` |
| 架构参数 | ARM新增`-Wa,-mimplicit-it=thumb`、GCC `--param`；AArch64调优从cortex-a53改为cortex-a57.cortex-a53，并新增GCC去未用debug type选项；x86/i686/RISC-V亦有对应GCC选项 | 六行Optflags全文见diff，不仅看x86 |
| 链接flags | 删除`_ldflags_arch_extra`、`build_ldflags`的项目定义；Base把`-Wl,-z,relro,--as-needed`放入公共编译flags，ARM/i686各自补链接flags | 旧L363–376；新L281–288。不等于所有硬化标志都丢失，但传递位置和宏接口改变 |
| Required/Support | gcc从Support变Required，gcc-c++单独Required；删除Support clang llvm-devel | 旧L300–303；新L228–229；binutils/glibc/rpm-build/libtool仍必需 |
| Preinstall/RunScripts | ARMv7l/v7hl/AArch64/RISC-V的clang-accel预安装及脚本运行条目删除 | 旧L223–224、231–232、239–240、247–248；qemu-accel仍在，不能说仿真完全关闭 |
| Keep | 删除Keep clang llvm libllvm llvm-devel，替换为cpp（已有其他cpp条目） | 旧L338、新L265；影响依赖环境保留，不直接等于特定包一定装/不装 |
| Prefer | 无差异 | 完整条目一致 |
| Ignore | 两份均无`Ignore:`指令 | `_skip_check_packages`是宏列表，且两份相同，不能混称Ignore规则 |
| Substitute | 无差异 | clang-accel四个替换条目仍在；预安装条目删除不代表这些替换也删除 |
| VMinstall | 无差异 | perl/libmount/libblkid等列表一致 |
| Repotype | 两份均未显式声明`Repotype:` | `Patterntype: rpm-md comps`相同；queryconfig repotype为空，不伪造值 |
| 其他 | Release、BuildFlags genmetaalgo、Hostarch、Target、ExportFilter、跨架构qemu设置、RPM压缩格式、check跳过列表相同 | 条件块删除只围绕已删宏；新增注释无执行意义；Order/Constraint/ExpandFlags未新增 |

31个发生增删/改值的宏名（含段入口）及其每个spec的命中/未命中清单，见[macro-coverage.json](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/macro-coverage.json)。同时搜索`_toolchain_override`、`optflags`、CFLAGS/CXXFLAGS/LDFLAGS和工具环境变量，覆盖“宏本身没改名、但消费链改变”的情况。

### 6.2 一个必须分清的边界：快照配置不等于已证实的QB最终配置

`3c78318b`只改两个`project_meta`和两个`snapshot_info`，**没有改Toolchain的`project_config`**。其父、该提交和本地HEAD中的Toolchain `project_config`逐字相同，[SHA对比](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/project-config-identity.json)。当前[完整project_config](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/toolchain-project_config) L135仍有`%_toolchain ...`，L119–160仍有编译器选择与段入口宏。

因此可证实的是：两份下载的build.conf不同，若用Base原件直接替代Toolchain配置会产生下文的影响；**不能仅凭`get_build_conf_text`取了Base地址，就声称NGBS最终传给RPM的全部宏已经确认变成Base**。1211018在仓库可用性检查处就失败，没有可供读取的LLVM包编译入口/最终.rpmmacros。QB还有`create_meta_for_ngbs`路径，是否又应用项目自己的project_config，本轮可见日志没有打印最终合成结果。

此外“维持原Toolchain条件”有两个时间基准，不能混用：10月13日快照e5187fd7与3c78318之前最新project_config并非完全相同。10月26日`8739131f`把section GC限制到Clang链接；此前还加了ARM max-page-size等。[完整近期历史diff](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/toolchain-config-diffs.txt)、[快照与当前配置diff](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/snapshot-vs-current-project-config.diff)。若保留总部此次切仓库前的编译条件，应以**3c78318父提交的项目配置**为基准，不能无说明退回10月13日全部配置。

## 7. Toolchain全部包的spec盘点和影响

<!-- PACKAGE_INVENTORY -->

以上逐包表给出源码/宏命中的证据，不宣称已实际重编每个包。所谓“宏链改变”，是两份build.conf直接替换时的静态影响；包内重新定义CC/CFLAGS或平台宏还可能覆盖。尤其不把“没有直接出现_toolchain”的包说成不受影响：它们仍消费段入口export、optflags、依赖包和编译器默认值。

### 7.1 LLVM的可确定分支变化

[QB请求的f308fe08 spec全文](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/llvm-f308fe08.spec)：

- L18–23：入口`%if %{defined _toolchain}`真时`llvm_release_build=0`，无该宏则为1。
- L31–37：release分支`%define debug_package %{nil}`，并把`__debug_install_post`定义成find-debuginfo后`rm -rf "%{buildroot}/usr/lib/debug"`、`rm -rf "%{buildroot}/usr/src/debug"`。**宏定义不等于该链必然执行**：平台链是否调用仍取决于debug_package机制；但它明确不承诺保留人工安装的debug文件。
- L198–207：release分支用sed从CFLAGS/CXXFLAGS/FFLAGS去掉`-g`类选项，之后x86自己的-O3+ThinLTO整理仍照常执行。不是新build.conf把所有包的-g都去掉，而是LLVM spec根据宏走了这个分支。
- L83–88：x86后续会补`_toolchain=clang`，并增加clang/llvm/libllvm BuildRequires，但**不能逆转前面已经决定的llvm_release_build**。因此不能仅看后面的`defined _toolchain`就断言仍是debug构建。
- L253–258：x86编译器仍显式clang/clang++；ARM/AArch64用`%__cc/%__cxx`，会落回Base/RPM工具宏。L266–273与L304–307的ThinLTO/lld/LLVM工具及非x86动态链接条件，也必须按各架构不同的宏状态判断。
- 结果：直接使用Base原件，不能维持本次“22个二进制RPM、clang-debuginfo含符号文件”的验收前提；不能用只给LLVM补一个宏替代项目级修复。原任务完整构建已暂停。

## 8. QB选择build.conf的可见机制和局限

[1202084配置流原文](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/1202084-config-flow.txt)、[1211018配置流原文](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/1211018-config-flow.txt)（每行前缀为原始完整日志行号）：

| 环节 | 1202084 | 1211018 |
|---|---|---|
| `__update_gbs_conf` L312–316 | base来自Toolchain/reference，解析为20261013.024319 | base来自Base/reference，解析为20261026.005418 |
| 生成profile L324、330–339 | 同名Toolchain profile，`buildconf=./build.conf`；Toolchain packages/debug | 同名Toolchain profile，`buildconf=./build.conf`；Base packages/debug |
| `get_build_conf_text` L347–348 | `repo_url`为Toolchain/reference/repos/standard | `repo_url`为Base/reference/repos/standard |
| NGBS入口（1211018） | 不把GBS profile等同最终RPM宏 | L400 `USE_NGBS=yes`；L432从Toolchain元目录生成build_meta；L434 DOD下载父地址为Base/reference；L441起还从Base取参考NGBS根；L509实际执行exec_ngbs_build.py |

这支持“默认GBS配置生成的仓库和build.conf取址都跟随snapshot_info.base”，但日志**没有记录build.conf最终字节/SHA，也没有打印NGBS最终合成_config**。下载固定快照用于比较的SHA不是从QB机器上取回的文件SHA，两者须区分。

全库46个项目目录均有`project_config`、`project_meta`、`project_env`、`snapshot_info`、`manifest.xml`和`candidate_snapshot`。另有4个`meta-dod.xml`、9组按DOD名拆分的meta/config文件、1个aggregate_list；没有独立命名为build.conf的受跟踪文件。[全部路径](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/repository-file-inventory.txt)、[文件类型统计](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/repository-file-types.json)。

存在**配置与下载URL分开存放的实例**：Tools-devbase-tools的[meta-dod-Targets-Ubuntu-24.04.xml](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/tools-example-meta-dod-Targets-Ubuntu-24.04.xml)声明Ubuntu下载URL；[project_config_dod-Targets-Ubuntu-24.04](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/tools-example-project_config_dod-Targets-Ubuntu-24.04)独立声明Repotype/Preinstall/宏等；主project_meta引用该DOD。前文已有该项目成功QB概览，说明显式异名DOD体系有可运行实例。历史`391390ff`已包含这些文件，[历史原文](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/tools-explicit-config-history.txt)。

**尚不能证明的部分**：看不到默认Toolchain路径是否支持单独的“build.conf URL”设置，不能凭文件名推断添加某个新XML属性/环境变量就有效。scm/meta/qb本身没有get_build_conf_text或create_meta_for_ngbs的实现；日志L391指向另一份QB-Scripts仓库，当前调查没有其代码。可见git历史不是shallow，但root为2026-09-08“latest snapshot”；更早配置实现历史不在这份仓库。没有读取QB后台设置或执行任何QB变更。

## 9. 修复候选和推荐

| 方案 | 具体文件/建议改法 | 能否同时保留Base包与Toolchain条件 | 风险和验证 |
|---|---|---|---|
| A. 只修DOD，接受配置改变 | 保留本地fd60db9两个project_meta单行修复；snapshot_info继续指Base；其他不改 | 若最终确实使用Base build.conf，则**不能**保留Toolchain条件；是项目行为迁移，不是纯名字修复 | LLVM发行模式/调试包改变；其余包见逐包表。需按新的项目标准重做全包三架构验证，不能用LLVM单包PASS替代 |
| B. Base包、Toolchain配置独立选择（推荐） | Toolchain project_meta引用自己的DOD；snapshot_info.base继续Base；Toolchain project_config保持3c78318父提交的完整内容。先确认create_meta_for_ngbs如何写入项目_config；若已经读取该文件，修名后应先核验最终合成配置；若默认路径忽略它，需修QB-Scripts配置装配，而不是随便在meta新增未知字段 | **设计上可以**，Tools分离文件是参考；但本轮证据不足以认证默认Toolchain的实现机制已经支持 | 不自行宣称只改meta两行已解决。索取/只读比对build_meta配置、NGBS最终_config和RPM宏；随后本地依赖解析/宏展开与基准一致，再安排完整项目验证。包版本更新仍会改变二进制，即便编译条件相同 |
| C. 在配置层补齐差异 | 仅在Toolchain专属配置装配结果补齐第6节31个差异宏及Preinstall/RunScripts/Required/Support/Keep/Optflags等；相应文件是`TIZEN/Tizen/Tizen-Base-Toolchain/project_config`，**它已包含这些机制，当前不应重复追加**。若加载链不使用它，仍须修读取/合并流程 | 完整补齐并验证合并优先级才可能；只补_toolchain远远不够 | 不改`TIZEN/Tizen/Tizen-Base/project_config`或Base公共快照build.conf，否则波及Base以及其他消费者。也不向Dev无条件灌Toolchain宏。追加顺序可能留下Base GCC flags和Toolchain Clang flags并存，须验证最终值而非“文本里有宏” |
| D. 临时恢复全部Toolchain来源 | 两个相关project_meta恢复正确DOD；Toolchain snapshot_info.base恢复Toolchain固定快照/来源，其他项目单独决定 | 保留旧来源和旧条件，但**不满足总部希望使用Base包的意图** | 只作为等待加载器确认时的临时退路；不能冒充推荐终态或未经用户授权实施 |

推荐B。首先保留现有两行DOD修复但不提交总部；请维护者确认`get_build_conf_text`与NGBS项目配置的最终装配机制，并以3c78318父提交Toolchain project_config为条件基准。**没有证据时，不推荐仅接受Base原件，也不推荐只给LLVM补_toolchain，更不修改Base全局配置来照顾Toolchain。**

只读/本地验证清单（本轮未执行构建）：

1. 固定两个来源：Base RPM仓库URL与SHA清单；Toolchain配置来源提交和SHA。记录GBS与NGBS最终输入，不仅记录中间profile。
2. 对三个架构比较最终rawmacros、CC/CXX/AR/RANLIB、optflags、build_ldflags、debug_package/段入口宏、依赖解析和clang-accel选择；不得以“成功展开一份LLVM spec”代替全项目覆盖。
3. 按逐包表对所有实际spec做条件展开，优先LLVM、GCC系列、glibc、iptables及任何覆盖工具宏的包。纯noarch包也核对包清单/debug机制，不能一概跳过。
4. 核验Base包仓库不再broken，NGBS引用与生成DOD同名；在无需触发QB的本地配置装配测试中先证明旧条件不变。完整项目构建需要用户后续授权，本轮不做。

## 10. 状态、边界与准备性更正

第一件本地meta提交fd60db96806a372404bd4f04e68d4ba586290147原样保留，未推送；只修DOD名称，不包含新的build.conf方案。第二件结论不变：两个快照构建LLVM用到的工具链**不完全相同**。第三件依用户回复暂停，没有启动gbs export、环境准备或完整构建。

回复到达前已独立完成debuglink的本地实现草稿、346项测试、39号旧产物副本上的轻量符号/布局检查，并生成本地detached提交569d734d0ccb2959e3f33494593c5cd46a01c347（tree e3fff52ab97b479bf3e1fd5bc5b90f842756c346，父6e9d4f2）；未推任何远端、没有新RPM，不能标为正式打包认证。相关工作树和未完成证据保留，本次GitHub提交只包含本调查文档/证据/STATUS，不携带暂停的源码或测试改动。后台日志按约定记录status=stopped及用户暂停原因。

查找阶段有两处路径更正：Tools目录实际位于`TIZEN/Tools/`；POSIX sh不展开`{base,toolchain}`，改为显式两个路径。均在只读查找中纠正，没有执行包构建或改配置。spec获取用HTTPS顺序流式解包，只保存spec与来源/大小/SHA；读取到全部spec后停止下载，记录的download_prefix_sha256明确不是完整SRPM SHA。未执行来自spec的脚本。对未知加载器行为、历史实际生效配置和包级最终二进制影响，均保留“未确认/静态推导”边界。
