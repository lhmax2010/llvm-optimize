# 45：QB DOD 本地修复与固定快照比较

两份build.conf不只是少了`_toolchain`：还改变编译器选择、默认优化参数、段入口环境、调试包插入和基础依赖。LLVM会改走release分支，sed/xz的PGO、readline/toybox等包也有明确分支变化；全部251个QB实际仓库已找到匹配提交的spec，但NGBS最终是否合并项目配置仍没有日志证据。推荐保留Toolchain自己的完整编译配置、仅让RPM依赖来自Tizen-Base，先确认配置装配机制，不能只给LLVM补一个宏；debuglink完整构建按用户要求暂停。

## 1. 默认DOD命名及反例排查

输入克隆为 `temp/qb-meta-20261028/repo`，原master HEAD `dc7d0e3e962ff6b27da97dad00ac7d9286d18136`。扫描全库46份`project_meta`，全部XML解析成功；32个DOD path中，7个同名、23个Tools显式异名引用、2个Toolchain/Dev异名且无显式定义。完整逐项结果：[all-project-dod-audit.json](../../tools/bolt/results/qb-meta-fix-and-snapshot-20261028/all-project-dod-audit.json)。

- 1202084子日志的DOD定义和`dod create project cmd`均为`DOD:Tizen-Base-Toolchain`，地址为Toolchain/reference；1211018同样创建该名，地址已变Base/reference。摘录见 [1202084-naming.txt](../../tools/bolt/results/qb-meta-fix-and-snapshot-20261028/1202084-naming.txt)、[1211018-naming.txt](../../tools/bolt/results/qb-meta-fix-and-snapshot-20261028/1211018-naming.txt)。这里确认的是**没有显式自定义DOD的默认生成路径**，不是所有项目必须同名的普遍限制。
- Tools-devbase-tools引用openSUSE15.2/15.5和Ubuntu22.04/24.04/26.04；Tools-devbase-tools-legacy引用openSUSE42.3和Ubuntu18.04/20.04。每个异名都有对应`meta-dod-Targets-*.xml`，定义名与引用吻合。
- 按用户要求只读核对它们的已有QB概览：1210029的子构建1210031为SUCCESSFUL；1210157的子构建1210161为SUCCESSFUL。见 [1210029概览](../../tools/bolt/results/qb-meta-fix-and-snapshot-20261028/tools-1210029-overview.txt)、[1210157概览](../../tools/bolt/results/qb-meta-fix-and-snapshot-20261028/tools-1210157-overview.txt)，同名png截图留存。这些成功说明显式异名有效，不能把名称必须一致说成全局规则；它们没有推翻Toolchain实际创建名与引用名不一致的证据。仅GET读取，未点任何构建操作。
- 历史相近改动：`7b9cbf97`把Base-X快照临时指向Base-Dev，仅改snapshot_info；`16c83914`随后启用的仍是`DOD:Tizen-Base-X`，没有改名为Dev。后者又被`a98f9e8c`撤回，`823e1331`最终恢复Base-X快照路径。完整四份diff在证据目录。因该启用提交被撤回，**不把它当成已验证成功的先例**，它仅说明历史写法和两种概念的区分。

## 2. 两行本地修复

本地提交 **`fd60db96806a372404bd4f04e68d4ba586290147`**，作者/提交者Hao Lin <hao.lin@samsung.com>，由Gerrit下载的commit-msg hook生成Change-Id。没有推送Gerrit或任何sandbox。

[完整git format-patch](../../tools/bolt/results/qb-meta-fix-and-snapshot-20261028/0001-fix-dod-references.patch)；[工作diff](../../tools/bolt/results/qb-meta-fix-and-snapshot-20261028/meta-working.diff)；[XML及版本比较](../../tools/bolt/results/qb-meta-fix-and-snapshot-20261028/meta-validation.json)。仅：

```diff
TIZEN/Tizen/Tizen-Base-Toolchain/project_meta:
-    <path project="DOD:Tizen-Base" repository="standard" />
+    <path project="DOD:Tizen-Base-Toolchain" repository="standard" />
TIZEN/Tizen/Tizen-Base-Dev/project_meta:
-    <path project="DOD:Tizen-Base" repository="standard" />
+    <path project="DOD:Tizen-Base-Dev" repository="standard" />
```

两个project_meta均与`3c78318^`版本逐字相同；两个snapshot_info均与`3c78318`后版本逐字相同。提交说明保留临时使用Base RPM的意图，引用1211018 L5516创建命令和L5486仓库错误原文。Tools显式DOD配置、其他文件均不变。仅本地XML/文本认证，未重新运行QB验证。

## 3. 快照来源与完整包差异

从两个固定URL的`standard/packages/repodata/repomd.xml`读取primary元数据与build.conf，不使用当前reference代替历史快照：

- `https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261013.024319/repos/standard/packages/`
- `https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base/tizen-base_20261026.005418/repos/standard/packages/`

[下载URL、大小、SHA](../../tools/bolt/results/qb-meta-fix-and-snapshot-20261028/snapshots/provenance.json)。primary保留gzip原件，解析后只比较x86_64/noarch。旧656条、新649条RPM记录；以name+arch分组可能含多个EVR，**不能把组数误叫RPM数量**。636个name+arch联合组：新增9、缺少11、EVR集合变化503、EVR相同但RPM校验不同113、完全相同0。

全部版本变化、新增、缺少及同版本不同内容的包，逐项见 [package-differences.tsv](../../tools/bolt/results/qb-meta-fix-and-snapshot-20261028/snapshots/package-differences.tsv)；完整校验值、位置见 [JSON](../../tools/bolt/results/qb-meta-fix-and-snapshot-20261028/snapshots/package-differences.json)。RPM checksum变化可能包括重建/签名/头部变化，不单凭它断言每个程序机器码不同；但无法证明整个工具链逐字相同，且明确存在release及配置变化。

重点包（x86_64，version-release）：

| 包 | Toolchain20261013 | Base20261026 |
|---|---|---|
| binutils | 2.43-1.14 | 2.43-3.30 |
| binutils-devel | 2.43-1.14 | 2.43-3.30 |
| clang | 22.1.8-3.1 | 22.1.8-6.5 |
| clang-devel | 22.1.8-3.1 | 22.1.8-6.5 |
| cmake | 3.31.2-1.5 | 3.31.2-1.96 |
| elfutils | 0.189-1.13 | 0.189-1.106 |
| gcc | 14.2.0-1.13 | 14.2.0-4.31 |
| gcc-c++ | 14.2.0-1.13 | 14.2.0-4.31 |
| glibc | 2.40-2.4 | 2.40-16.8 |
| glibc-devel | 2.40-2.4 | 2.40-16.8 |
| libllvm | 22.1.8-3.1 | 22.1.8-6.5 |
| libxml2 | 2.15.1-1.10 | 2.15.1-2.30 |
| libxml2-devel | 2.15.1-1.10 | 2.15.1-2.30 |
| llvm | 22.1.8-3.1 | 22.1.8-6.5 |
| llvm-devel | 22.1.8-3.1 | 22.1.8-6.5 |
| ninja | 1.13.1-1.14 | 1.13.1-1.63 |
| patchelf | 0.16.1-1.13 | 0.16.1-2.26 |
| python3 | 3.14.2-1.9 | 3.14.2-5.35 |
| python3-devel | 3.14.2-1.9 | 3.14.2-5.31 |
| rpm | 4.14.1.1-1.7 | 4.14.1.1-7.3 |
| rpm-build | 4.14.1.1-1.7 | 4.14.1.1-7.3 |
| sed | 4.1c-1.13 | 4.1c-5.24 |
| util-linux | 2.41.2-1.7 | 2.41.2-2.20 |
| xz | 5.8.1-1.12 | 5.8.1-5.29 |
| zlib | 1.3.1-1.14 | 1.3.1-2.29 |
| zlib-devel | 1.3.1-1.14 | 1.3.1-2.29 |

`lld`不是单独包名：primary文件列表显示`/usr/bin/ld.lld`由`llvm`提供；新版是llvm22.1.8-6.5。`/usr/bin/eu-strip`由`elfutils-0.189-1.106.x86_64`提供（不是假定宿主工具可用）；此前第三件的本地草稿在x86_64+BOLT条件内显式BuildRequires elfutils；现在暂停，未作新构建认证。

### 3.1 spec每一条BuildRequires

以f308fe08的源spec原行号列出，覆盖所有条件分支，不把未启用分支当作当前必装。所有14条/拆分项都能找到provider；详细版本、校验值见 [buildrequires.json](../../tools/bolt/results/qb-meta-fix-and-snapshot-20261028/snapshots/buildrequires.json)。

| spec行 | 原要求 | 旧provider | 新provider |
|---|---|---|---|
| 59 | util-linux | util-linux 0:2.41.2-1.7 | util-linux 0:2.41.2-2.20 |
| 66 | cmake | cmake 0:3.31.2-1.5 | cmake 0:3.31.2-1.96 |
| 67 | python3 | python3 0:3.14.2-1.9 | python3 0:3.14.2-5.35 |
| 68 | python3-devel | python3-devel 0:3.14.2-1.9 | python3-devel 0:3.14.2-5.31 |
| 69 | patchelf | patchelf 0:0.16.1-1.13 | patchelf 0:0.16.1-2.26 |
| 70 | binutils-devel | binutils-devel 0:2.43-1.14 | binutils-devel 0:2.43-3.30 |
| 71 | libxml2-devel | libxml2-devel 0:2.15.1-1.10 | libxml2-devel 0:2.15.1-2.30 |
| 73 | sed | sed 0:4.1c-1.13 | sed 0:4.1c-5.24 |
| 75 | ninja | ninja 0:1.13.1-1.14 | ninja 0:1.13.1-1.63 |
| 78 | python3 >= 3.9 | python3 0:3.14.2-1.9 | python3 0:3.14.2-5.35 |
| 79 | xz | xz 0:5.8.1-1.12 | xz 0:5.8.1-5.29 |
| 85 | clang | clang 0:22.1.8-3.1 | clang 0:22.1.8-6.5 |
| 85 | llvm | llvm 0:22.1.8-3.1 | llvm 0:22.1.8-6.5 |
| 85 | libllvm | libllvm 0:22.1.8-3.1 | libllvm 0:22.1.8-6.5 |

## 4. build.conf逐行比较与构建模式冲突

旧build.conf SHA256与既有记录精确一致：
`e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945`。

新build.conf SHA256：
`840ef6de94c6d73e3fcced27dc777a399df435a0f2e4017347191a296f5f1975`。

[完整逐行diff](../../tools/bolt/results/qb-meta-fix-and-snapshot-20261028/snapshots/build.conf.diff)。主要差异：项目/发行版名称；Base没有Toolchain的Clang选择宏、`_toolchain`、AR/CC/CXX环境前导及debug_package展开前导；基础必装变成gcc/gcc-c++；optflags使用Base的-O2/-fno-inline-functions而非Toolchain的-Os Clang链；架构flags也不同。不能仅因上游工具版本号相同就沿用39号精确SHA口径。

44号两次子日志L314直接记录Base/reference解析为 **tizen-base_20261026.005418**，L336/339生成的packages/debug URL亦相同，足以确认那两轮当时的解析结果；不是查询现在reference后倒推历史。

**已收到用户裁决**：暂停第三件，不采用仅本地补`_toolchain`来继续构建。对两份build.conf直接替换而言，LLVM入口分支会改变；但NGBS还有项目配置生成步骤，不能把下载地址等同最终RPM宏。第6–10节补全项目级调查、逐包影响和推荐方案，取代此前等待单包宏授权的状态。

## 5. 验收口径与状态

工具链不同，后续不能继承39号精确clang SHA验收。第一件本地meta提交保留且不推送；第二件快照差异已确认。第三件本地草稿保留、完整构建暂停，未产生新RPM，不把函数级符号实验或配置下载称为打包验证通过。

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

名单有三个不同口径，不能混称：当前Toolchain `manifest.xml` **245个源码仓库**；1211018日志L136/278/417/5737的四份相同`build_pkg_list_dic`为**251个实际调度仓库**；两者并集252个，额外的tensorflow2只在当前manifest内、该次实际列表没有。旧固定Toolchain快照的source索引有**365份SRPM、256个源码包名**（同包可能多个release，且源码包名不一定等于仓库名）。

来源：[manifest原文](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/toolchain-manifest.xml)、[manifest解析](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/manifest-projects.json)、[QB实际名单及原日志行号](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/1211018-package-lists.json)、[快照source目录原HTML](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/source-index-1.html)、[完整365份列表](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/srpm-list.txt)。已顺序读取全部365份SRPM，保存其中所有spec，数量与RPM头的spec名单吻合、文件大小/SHA复核全PASS。[每份URL/大小/压缩方式/spec SHA](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/spec-acquisition.json)。这只提取spec，不运行包内脚本；为避免下载大量源码，在全部spec读完后终止流，**download_prefix_sha256不是完整SRPM SHA**。

快照优先；缺少对应包或快照VCS不是QB所用提交时，再只读取Gerrit `tizen_base`/日志提交的packaging归档。最终251个实际仓库都有与QB提交号匹配的spec证据，tensorflow2有快照spec；[逐仓库提交与spec覆盖](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/project-spec-coverage.json)、[分支获取](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/git-spec-provenance.json)、[按QB精确提交获取](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/git-qb-spec-provenance.json)。分支头查询与archive分开记录，不把branch查询SHA冒充服务端tar内置签名；最终实际名单的匹配不依赖这六个分支读取的时间窗口，另按明确提交号取得了spec。

全量逐行搜索包括31个变化宏、间接消费变量及段入口，保留注释标记和上下文：[spec-macro-usage.tsv](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/spec-macro-usage.tsv)、[JSON](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/spec-macro-usage.json)、[全部源码包版本影响表](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/package-impact.tsv)。下表按仓库逐项列出（同一仓库多份spec时全部合并），优先该次QB提交；原始快照的额外/旧包版本仍包含在上述全量表中。

影响代号是**直接替换build.conf的静态条件推导**，不是编译结果；A方案继承这些变化，B/C若恢复完整有效Toolchain配置则消除这些配置变化（仍有Base依赖包版本变化），D改回旧依赖来源：

- **H**：表中列出的prep/build/install入口不再有Toolchain的AR/RANLIB、CC/CXX export；install入口的debug_package插入也消失。是否最终产生debug子包还取决于平台与spec，不武断地说每个包都关debug。
- **F**：直接消费optflags或CFLAGS/CXXFLAGS/RPM_OPT_FLAGS，默认Clang -Os选项链变为Base GCC -O2链；包自行覆盖的最终值须另核对。
- **T**：直接使用__cc/__cxx/__ar/__ranlib宏，工具分派/拼写可能变化。
- **G**：指定_toolchain_override gcc；旧条件已经选GCC，Base也默认GCC，不是必然换编译器，仍需核对工具名/flags。
- **L**：直接消费build_ldflags，项目定义消失，须检查平台或包本身是否补定义，不能保证链接flags相同。
- **X**：有包专属_toolchain/toolchain_is分支，见下一张原文表及LLVM小节。
- **M**：MLGO宏有自身默认；不能把配置宏消失说成MLGO必然关闭。
- **E**：所有项目均面对Required/Support/预安装/依赖版本/发行版标识变化。即使只有noarch脚本或无直接命中，也不能据此证明RPM相同。

段入口列P/B/I分别为prep/build/install；“—”表示所查spec无该类直接命中。链接后的`L`是保留spec的原行号，所有命中全文在TSV/JSON。

| 包/源码仓库（来源） | 变化宏直接命中；间接消费 | 段入口 | 两配置下的影响 | spec原文/行号 |
|---|---|---|---|---|
| platform/core/security/default-ac-domains（QB） | —；— | B/I/P | E,H | [default-ac-domains.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/default-ac-domains-0.2-1.1/default-ac-domains.spec#L16) L16,19,26 |
| platform/core/system/app-rootstrap-checker（QB） | —；— | I/P | E,H | [app-rootstrap-checker.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/app-rootstrap-checker-1.0.0-1.1/app-rootstrap-checker.spec#L35) L35,39 |
| platform/core/system/libdbuspolicy-header（QB） | —；— | B/I/P | E,H | [libdbuspolicy-header.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libdbuspolicy-header-1.2.0-1.1/libdbuspolicy-header.spec#L36) L36,40,45 |
| platform/hal/backend/rootstrap-checker（QB） | —；— | I/P | E,H | [hal-rootstrap-checker.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/hal-rootstrap-checker-1.0.0-4.1/hal-rootstrap-checker.spec#L35) L35,39 |
| platform/upstream/abi-compliance-checker（QB） | —；— | B/I/P | E,H | [abi-compliance-checker.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__abi-compliance-checker/abi-compliance-checker.spec#L22) L22,26,29 |
| platform/upstream/abi-dumper（QB） | —；— | B/I/P | E,H | [abi-dumper.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__abi-dumper/abi-dumper.spec#L31) L31,37,40 |
| platform/upstream/abi-tracker（QB） | —；— | B/I/P | E,H | [abi-tracker.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__abi-tracker/abi-tracker.spec#L26) L26,32,35 |
| platform/upstream/abi-viewer（QB） | —；— | B/I/P | E,H | [abi-viewer.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__abi-viewer/abi-viewer.spec#L28) L28,32,36 |
| platform/upstream/abseil-cpp（QB） | —；— | B/I/P | E,H | [abseil-cpp.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/abseil-cpp-20250814.1-1.1/abseil-cpp.spec#L45) L45,50,56 |
| platform/upstream/acl（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [acl.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/acl-2.3.2-1.13/acl.spec#L39) L39,43,44,45,54 |
| platform/upstream/alsa-lib（QB） | —；— | B/I/P | E,H | [alsa-lib.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/alsa-lib-1.2.12-1.1/alsa-lib.spec#L39) L39,48,60 |
| platform/upstream/alsa-utils（QB） | —；CFLAGS | B/I/P | E,H,F | [alsa-utils.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/alsa-utils-1.2.12-3.1/alsa-utils.spec#L27) L27,34,35,47 |
| platform/upstream/attr（QB） | —；CFLAGS, LDFLAGS, RPM_OPT_FLAGS | B/I/P | E,H,F | [attr.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/attr-2.5.1-1.14/attr.spec#L44) L44,48,49,51,52,66 |
| platform/upstream/autoconf（QB） | —；— | B/I/P | E,H | [autoconf.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/autoconf-2.71-1.15/autoconf.spec#L33) L33,39,47,48 |
| platform/upstream/autoconf-archive（QB） | —；— | B/I/P | E,H | [autoconf-archive.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/autoconf-archive-2023.02.20-1.13/autoconf-archive.spec#L23) L23,30,34 |
| platform/upstream/autoconf213（QB） | —；— | B/I/P | E,H | [autoconf213.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/autoconf213-2.13-1.1/autoconf213.spec#L50) L50,82,87 |
| platform/upstream/automake（QB） | —；— | B/I/P | E,H | [automake.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/automake-1.16.5-1.15/automake.spec#L30) L30,38,43 |
| platform/upstream/bc（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [bc.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/bc-1.06-1.1/bc.spec#L43) L43,57,58,59,66 |
| platform/upstream/bcc（QB） | —；— | B/I/P | E,H | [bcc-tools.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/git-specs/platform__upstream__bcc/bcc-tools.spec#L55) L55,58,75 |
| platform/upstream/binutils（QB） | —；CFLAGS, CXXFLAGS, RPM_OPT_FLAGS | B/I/P | E,H,F | [binutils.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/binutils-2.43-1.14/binutils.spec#L117) L117,121,122,123,124,170；[binutils-aarch64.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/binutils-aarch64-2.43-1.1/binutils-aarch64.spec#L120) L120,124,125,126,127,173；[binutils-armv7hl.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/binutils-armv7hl-2.43-1.1/binutils-armv7hl.spec#L120) L120,124,125,126,127,173；[binutils-armv7l.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/binutils-armv7l-2.43-1.1/binutils-armv7l.spec#L120) L120,124,125,126,127,173；[binutils-riscv64.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/binutils-riscv64-2.43-1.1/binutils-riscv64.spec#L120) L120,124,125,126,127,173 |
| platform/upstream/bison（QB） | —；— | B/I/P | E,H | [bison.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/bison-3.0.5-1.14/bison.spec#L21) L21,29,36 |
| platform/upstream/boost（QB） | `__cc`；CC, CFLAGS, CXXFLAGS, LDFLAGS | B/I/P | E,H,F,T | [boost.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/boost-1.83.0-1.2/boost.spec#L435) L422,434,435,436,438,439,494,530,531,547 |
| platform/upstream/boost-jam（QB） | `__cc`；CC, CFLAGS | B/I/P | E,H,F,T | [boost-jam.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/boost-jam-201104-1.1/boost-jam.spec#L37) L25,36,37,38,40,50 |
| platform/upstream/bpftrace（QB） | —；— | B/I/P | E,H | [bpftrace.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/bpftrace-0.24.2-1.2/bpftrace.spec#L70) L70,87,98 |
| platform/upstream/build（QB） | —；— | B/I/P | E,H | [build.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/build-20120927-1.1/build.spec#L63) L63,77,79 |
| platform/upstream/build-compare（QB） | —；— | B/I/P | E,H | [build-compare.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/build-compare-2023.06.18-1.4/build-compare.spec#L42) L42,46,48 |
| platform/upstream/bzip2（QB） | `__ar`, `__cc`, `__ranlib`；AR, CC, CFLAGS, LDFLAGS, RANLIB | B/I/P | E,H,F,T | [bzip2.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/bzip2-1.0.8-1.13/bzip2.spec#L61) L45,56,58,59,61,62,65,68 |
| platform/upstream/c-ares（QB） | —；— | B/I/P | E,H | [c-ares.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/c-ares-1.21.0-1.1/c-ares.spec#L43) L43,50,56 |
| platform/upstream/ccache（QB） | —；CFLAGS, CXXFLAGS, LDFLAGS | B/I/P | E,H,F | [ccache.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/ccache-4.12.1-1.1/ccache.spec#L24) L24,30,31,32,33,46 |
| platform/upstream/cereal（QB） | —；debug_package | B/I/P | E,H | [cereal.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/cereal-1.3.2-1.1/cereal.spec#L1) L1,35,38,42 |
| platform/upstream/chrpath（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [chrpath.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/chrpath-0.16-1.1/chrpath.spec#L20) L20,29,30,31,39 |
| platform/upstream/cmake（QB） | —；CFLAGS, CXXFLAGS, RPM_OPT_FLAGS | B/I/P | E,H,F | [cmake.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/cmake-3.31.2-1.9/cmake.spec#L34) L34,38,39,40,57 |
| platform/upstream/ctags（QB） | —；CFLAGS, CXXFLAGS, LDFLAGS | B/I/P | E,H,F | [ctags.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__ctags/ctags.spec#L20) L20,24,26,27,28,41 |
| platform/upstream/curl（QB） | —；CFLAGS | B/I/P | E,H,F | [curl.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/curl-8.11.0-1.1/curl.spec#L56) L56,67,70,71,73,94 |
| platform/upstream/dash（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [dash.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/dash-0.5.13.4-1.1/dash.spec#L17) L17,21,22,23,28 |
| platform/upstream/db4（QB） | —；CFLAGS, CXX | B/I/P | E,H,F | [db4.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__db4/db4.spec#L62) L62,66,74,95,126,129 |
| platform/upstream/dejagnu（QB） | —；— | B/I/P | E,H | [dejagnu.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/dejagnu-1.6.2-1.1/dejagnu.spec#L24) L24,28,34 |
| platform/upstream/diffutils（QB） | —；CFLAGS | B/I/P | E,H,F | [diffutils.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/diffutils-3.10-1.1/diffutils.spec#L23) L23,31,32,36 |
| platform/upstream/docbook-xsl-stylesheets（QB） | —；— | B/I/P | E,H | [docbook-xsl-stylesheets.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/docbook-xsl-stylesheets-1.79.2-1.1/docbook-xsl-stylesheets.spec#L56) L56,85,120 |
| platform/upstream/docbook_4（QB） | —；— | B/I/P | E,H | [docbook_4.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/docbook_4-4.5-1.1/docbook_4.spec#L89) L89,115,277 |
| platform/upstream/dos2unix（QB） | `__cc`；CC, RPM_OPT_FLAGS | B/I/P | E,H,F,T | [dos2unix.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/dos2unix-7.5.1-1.1/dos2unix.spec#L32) L24,30,31,32,35 |
| platform/upstream/doxygen（QB） | —；CFLAGS, CXXFLAGS, LDFLAGS | B/I/P | E,H,F | [doxygen.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/doxygen-1.14.0-1.1/doxygen.spec#L34) L34,41,42,43,44,55 |
| platform/upstream/e2fsprogs（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [e2fsprogs.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/e2fsprogs-1.46.0-1.9/e2fsprogs.spec#L75) L75,83,85,86,100 |
| platform/upstream/ed（QB） | `__cc`；CC, CFLAGS, LDFLAGS | B/I/P | E,H,F,T | [ed.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/ed-1.22.3-1.1/ed.spec#L22) L15,19,20,21,22,23,28 |
| platform/upstream/elfutils（QB） | —；— | B/I/P | E,H | [elfutils.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/elfutils-0.189-1.14/elfutils.spec#L95) L95,105,118 |
| platform/upstream/expat（QB） | —；CFLAGS, CXXFLAGS, LDFLAGS | B/I/P | E,H,F | [expat.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/expat-2.7.3-1.13/expat.spec#L94) L94,99,100,101,102,111 |
| platform/upstream/expect（QB） | —；CFLAGS | B/I/P | E,H,F | [expect.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/expect-5.45.4-1.1/expect.spec#L37) L37,44,45,57 |
| platform/upstream/fdupes（QB） | —；CFLAGS, optflags | B/I/P | E,H,F | [fdupes.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/fdupes-2.4.0-1.15/fdupes.spec#L19) L19,23,26,28 |
| platform/upstream/file（QB） | —；CFLAGS, LDFLAGS, RPM_OPT_FLAGS | B/I/P | E,H,F | [file.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/file-5.46-1.13/file.spec#L58) L58,66,73,74,87,95 |
| platform/upstream/filesystem（QB） | —；debug_package | B/I/P | E,H | [filesystem.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/filesystem-3.1-1.1/filesystem.spec#L4) L4,26,29,32 |
| platform/upstream/flex（QB） | —；— | B/I/P | E,H | [flex.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/flex-2.6.4-1.14/flex.spec#L24) L24,32,39 |
| platform/upstream/fribidi（QB） | —；— | B/I/P | E,H | [fribidi.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/fribidi-1.0.10-1.1/fribidi.spec#L40) L40,48,56 |
| platform/upstream/gcc（QB） | —；CFLAGS, CXXFLAGS, RPM_OPT_FLAGS, _toolchain_override | B/I/P | E,H,F,G | [gcc.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/gcc-14.2.0-1.14/gcc.spec#L30) L30,334,350,354,358,359,360,361,364,365,367,373,374,375,379,380,381,386,388,395,402,403,432,517,519；[gcc-aarch64.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/gcc-aarch64-14.2.0-1.4/gcc-aarch64.spec#L33) L33,337,353,357,361,362,363,364,367,368,370,376,377,378,382,383,384,389,391,398,405,406,435,520,522；[gcc-armv7hl.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/gcc-armv7hl-14.2.0-1.4/gcc-armv7hl.spec#L33) L33,337,353,357,361,362,363,364,367,368,370,376,377,378,382,383,384,389,391,398,405,406,435,520,522；[gcc-armv7l.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/gcc-armv7l-14.2.0-1.4/gcc-armv7l.spec#L33) L33,337,353,357,361,362,363,364,367,368,370,376,377,378,382,383,384,389,391,398,405,406,435,520,522；[gcc-riscv64.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/gcc-riscv64-14.2.0-1.4/gcc-riscv64.spec#L33) L33,337,353,357,361,362,363,364,367,368,370,376,377,378,382,383,384,389,391,398,405,406,435,520,522 |
| platform/upstream/gcc-contrib（QB） | —；— | B/I/P | E,H | [gcc-contrib.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/gcc-contrib-14.2.0-1.1/gcc-contrib.spec#L565) L565,571,585 |
| platform/upstream/gdb（QB） | —；CFLAGS, CXXFLAGS, LDFLAGS | B/I/P | E,H,F | [gdb.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/gdb-16.3-1.1/gdb.spec#L85) L85,105,106,108,109,110,111,149 |
| platform/upstream/gettext（QB） | —；CFLAGS | B/I/P | E,H,F | [gettext.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/gettext-0.21.1-2.13/gettext.spec#L77) L77,84,85,109 |
| platform/upstream/giflib（QB） | —；— | B/I/P | E,H | [giflib.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/giflib-5.2.2-1.4/giflib.spec#L60) L60,68,71 |
| platform/upstream/glibc（QB） | `__cc`, `__cxx`；CC, CFLAGS, CXX, CXXFLAGS, LDFLAGS, _toolchain_override, optflags | B/I/P | E,H,F,T,G | [glibc.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__glibc/glibc.spec#L365) L36,314,318,329,364,365,413,414,452,453,454,462,470,486,487,488,496,504,519 |
| platform/upstream/gn（QB） | `__ar`, `__cc`, `__cxx`, `__ranlib`；AR, CC, CXX, RANLIB | B/I/P | E,H,T | [gn.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/gn-20210313-1.1/gn.spec#L42) L37,41,42,64 |
| platform/upstream/golang（QB） | —；debug_package | B/I/P | E,H | [golang.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/golang-1.25.3-1.1/golang.spec#L6) L6,231,254,256 |
| platform/upstream/groff（QB） | —；CFLAGS, CXXFLAGS, LDFLAGS | B/I/P | E,H,F | [groff.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/groff-1.23.0-1.1/groff.spec#L42) L42,48,50,51,52,56 |
| platform/upstream/gtk-doc（QB） | —；— | B/I/P | E,H | [gtk-doc.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/gtk-doc-1.35.1-1.1/gtk-doc.spec#L34) L34,39,44 |
| platform/upstream/help2man（QB） | —；— | B/I/P | E,H | [help2man.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/help2man-1.49.3-1.13/help2man.spec#L23) L23,27,31 |
| platform/upstream/hostname（QB） | —；— | B/I/P | E,H | [hostname.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/hostname-3.23-1.1/hostname.spec#L19) L19,27,30 |
| platform/upstream/icecream（QB） | —；CFLAGS, CXXFLAGS, RPM_OPT_FLAGS | B/I/P | E,H,F | [icecream.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/icecream-0.9.7-1.1/icecream.spec#L52) L52,55,56,57,61 |
| platform/upstream/icu（QB） | —；CFLAGS, CXXFLAGS | B/I/P | E,H,F | [icu.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/icu-78.1-1.4/icu.spec#L63) L63,75,76,77,99 |
| platform/upstream/iniparser（QB） | —；— | B/I/P | E,H | [iniparser.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/iniparser-4.2.6-1.1/iniparser.spec#L29) L29,35,47 |
| platform/upstream/intltool（QB） | —；— | B/I/P | E,H | [intltool.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/intltool-0.51.0-1.12/intltool.spec#L26) L26,31,38 |
| platform/upstream/iproute2（QB） | `__ar`, `__cc`；AR, CC | B/I/P | E,H,T | [iproute2.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/iproute2-5.5.0-1.1/iproute2.spec#L69) L53,64,69,71 |
| platform/upstream/iptables（QB） | `_toolchain`, `toolchain_is`；CFLAGS, LDFLAGS | B/I/P | E,H,F,X | [iptables.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/iptables-1.6.1-2.1/iptables.spec#L80) L47,78,79,80,81,82,85,97 |
| platform/upstream/iso_ent（QB） | —；— | B/I/P | E,H | [iso_ent.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/iso_ent-2000.11.03-1.1/iso_ent.spec#L30) L30,34,36 |
| platform/upstream/itstool（QB） | —；— | B/I/P | E,H | [itstool.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/itstool-2.0.7-1.1/itstool.spec#L41) L41,45,49 |
| platform/upstream/jsoncpp（QB） | —；— | B/I/P | E,H | [jsoncpp.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/jsoncpp-1.9.6-1.13/jsoncpp.spec#L34) L34,40,57 |
| platform/upstream/keyutils（QB） | `__cc`；CC, CFLAGS, LDFLAGS, RPM_OPT_FLAGS | B/I/P | E,H,F,T | [keyutils.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/keyutils-1.6.3-1.3/keyutils.spec#L39) L34,38,39,41 |
| platform/upstream/kmod（QB） | `_toolchain`, `toolchain_is`；CFLAGS, LDFLAGS | B/I/P | E,H,F,X | [kmod.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/kmod-34.2-2.1/kmod.spec#L102) L82,90,102,103,104,107,112 |
| platform/upstream/krb5（QB） | —；CC, CFLAGS, LDFLAGS, RPM_OPT_FLAGS | B/I/P | E,H,F | [krb5.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/krb5-1.22.1-1.1/krb5.spec#L61) L61,67,72,73,74,96,101 |
| platform/upstream/less（QB） | —；CFLAGS, CXXFLAGS, LDFLAGS | B/I/P | E,H,F | [less.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/less-685-1.1/less.spec#L23) L23,27,28,29,30,31,35 |
| platform/upstream/libabigail（QB） | —；CFLAGS | B/I/P | E,H,F | [libabigail.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__libabigail/libabigail.spec#L31) L31,34,36,57 |
| platform/upstream/libarchive（QB） | —；CFLAGS, CXXFLAGS, LDFLAGS, optflags | B/I/P | E,H,F | [libarchive.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libarchive-3.8.1-2.4/libarchive.spec#L57) L57,63,64,65,66,67,72 |
| platform/upstream/libbpf（QB） | —；— | B/I/P | E,H | [libbpf.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libbpf-1.6.2-1.1/libbpf.spec#L46) L46,51,62 |
| platform/upstream/libcap（QB） | `__ar`, `__cc`, `__ranlib`；AR, CC, RANLIB | B/I/P | E,H,T | [libcap.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libcap-2.73-1.16/libcap.spec#L57) L49,55,57,60 |
| platform/upstream/libdrm（QB） | —；CFLAGS | B/I/P | E,H,F | [libdrm.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libdrm-2.4.131-2.1/libdrm.spec#L92) L92,106,107,128 |
| platform/upstream/libelf0（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [libelf0.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libelf0-0.8.13-1.1/libelf0.spec#L46) L46,54,55,56,69 |
| platform/upstream/libev（QB） | —；— | B/I/P | E,H | [libev.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libev-4.33-1.1/libev.spec#L29) L29,33,37 |
| platform/upstream/libevent（QB） | —；— | B/I/P | E,H | [libevent.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libevent-2.1.12-1.1/libevent.spec#L36) L36,42,47 |
| platform/upstream/libffi（QB） | —；LDFLAGS | B/I/P | E,H | [libffi.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libffi-3.4.7-1.15/libffi.spec#L64) L64,69,72,76 |
| platform/upstream/libgcrypt（QB） | —；CFLAGS | B/I/P | E,H,F | [libgcrypt.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libgcrypt-1.11.0-1.1/libgcrypt.spec#L35) L35,39,50,51,71 |
| platform/upstream/libgpg-error（QB） | —；— | B/I/P | E,H | [libgpg-error.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libgpg-error-1.51-1.1/libgpg-error.spec#L33) L33,41,47 |
| platform/upstream/libjpeg-turbo（QB） | —；CFLAGS | B/I/P | E,H,F | [libjpeg-turbo.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libjpeg-turbo-3.0.4-1.3/libjpeg-turbo.spec#L56) L56,64,67,76 |
| platform/upstream/libmd（QB） | —；— | B/I/P | E,H | [libmd.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libmd-1.1.0-1.1/libmd.spec#L49) L49,53,60 |
| platform/upstream/libnl2（QB） | —；— | B/I/P | E,H | [libnl2.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libnl2-2.0-2.1/libnl2.spec#L30) L30,35,41 |
| platform/upstream/libnl3（QB） | —；— | B/I/P | E,H | [libnl3.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libnl3-3.2.22-1.1/libnl3.spec#L44) L44,57,64 |
| platform/upstream/libogg（QB） | —；— | B/I/P | E,H | [libogg.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libogg-1.3.2-1.1/libogg.spec#L34) L34,42,54 |
| platform/upstream/libpciaccess（QB） | —；CFLAGS | B/I/P | E,H,F | [libpciaccess.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libpciaccess-0.13.2-1.1/libpciaccess.spec#L43) L43,52,55,56,61 |
| platform/upstream/libpsl（QB） | —；— | B/I/P | E,H | [libpsl.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libpsl-0.21.0-1.1/libpsl.spec#L34) L34,39,45 |
| platform/upstream/libsigc++（QB） | —；— | B/I/P | E,H | [libsigc++.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/git-specs/platform__upstream__libsigc%2B%2B/libsigc%2B%2B.spec#L35) L35,39,51 |
| platform/upstream/libsndfile（QB） | —；CFLAGS, LDFLAGS, optflags | B/I/P | E,H,F | [libsndfile.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libsndfile-1.2.2-1.1/libsndfile.spec#L42) L42,50,53,54,55,56,67 |
| platform/upstream/libtirpc（QB） | —；— | B/I/P | E,H | [libtirpc.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libtirpc-1.3.3-1.1/libtirpc.spec#L34) L34,38,42 |
| platform/upstream/libtool（QB） | —；CFLAGS, RPM_OPT_FLAGS | B/I/P | E,H,F | [libtool.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__libtool/libtool.spec#L42) L42,47,52,59 |
| platform/upstream/libunistring（QB） | —；— | B/I/P | E,H | [libunistring.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libunistring-1.4-1.13/libunistring.spec#L42) L42,46,53 |
| platform/upstream/libunwind（QB） | —；CFLAGS | B/I/P | E,H,F | [libunwind.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libunwind-1.6.2-1.1/libunwind.spec#L41) L41,47,48,60 |
| platform/upstream/libvorbis（QB） | —；— | B/I/P | E,H | [libvorbis.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libvorbis-1.3.7-1.1/libvorbis.spec#L66) L66,73,83 |
| platform/upstream/libwebp（QB） | —；CFLAGS | B/I/P | E,H,F | [libwebp.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libwebp-1.4.0-1.1/libwebp.spec#L47) L47,51,52,56 |
| platform/upstream/libxcrypt（QB） | —；CFLAGS | B/I/P | E,H,F | [libxcrypt.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libxcrypt-4.4.36-1.15/libxcrypt.spec#L62) L62,74,76,89 |
| platform/upstream/libxml2（QB） | —；CFLAGS, CXXFLAGS | B/I/P | E,H,F | [libxml2.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libxml2-2.15.1-1.13/libxml2.spec#L56) L56,61,62,63,74 |
| platform/upstream/libxslt（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [libxslt.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libxslt-1.1.43-1.1/libxslt.spec#L64) L64,71,72,73,81 |
| platform/upstream/libzio（QB） | `__ar`, `__cc`, `__ranlib`；AR, CC, RANLIB | B/I/P | E,H,T | [libzio.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/libzio-1.09-1.12/libzio.spec#L39) L12,31,37,39,68 |
| platform/upstream/linux-glibc-devel（QB） | —；— | B/I/P | E,H | [linux-glibc-devel.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/linux-glibc-devel-6.6-1.14/linux-glibc-devel.spec#L30) L30,34,85 |
| platform/upstream/llvm（QB） | `__cc`, `__cxx`, `_toolchain`, `mlgo_build_jobs`, `mlgo_verify_configure_only`；CFLAGS, CXXFLAGS, _toolchain_override, debug_package | B/I/P | E,H,F,T,X,M | [llvm-f308fe08.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/llvm-f308fe08.spec#L18) L18,19,33,63,64,83,86,183,198,201,202,203,204,218,227,236,237,257,258,263,264,265,266,304,344,414,416,419,422,484 |
| platform/upstream/lttng-ust（QB） | —；optflags | B/I/P | E,H,F | [lttng-ust.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/lttng-ust-2.14.0-1.1/lttng-ust.spec#L33) L33,39,42,57 |
| platform/upstream/lua（QB） | `__cc`；CC, CFLAGS, LDFLAGS | B/I/P | E,H,F,T | [lua.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/lua-5.1.5-1.12/lua.spec#L100) L82,91,92,93,100,105 |
| platform/upstream/m4（QB） | —；CFLAGS, CXXFLAGS, LDFLAGS | B/I/P | E,H,F | [m4.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/m4-1.4.20-1.1/m4.spec#L14) L14,18,19,20,21,35 |
| platform/upstream/make（QB） | —；CFLAGS, optflags | B/I/P | E,H,F | [make.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/make-4.4.1-1.13/make.spec#L21) L21,27,29,36 |
| platform/upstream/meson（QB） | —；— | B/I/P | E,H | [meson.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/meson-1.9.1-1.3/meson.spec#L58) L58,63,65 |
| platform/upstream/mm-common（QB） | —；— | B/I/P | E,H | [mm-common.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/mm-common-1.0.7-1.1/mm-common.spec#L31) L31,39,45 |
| platform/upstream/mtdev（QB） | —；— | B/I/P | E,H | [mtdev.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/mtdev-1.1.6-1.1/mtdev.spec#L37) L37,45,49 |
| platform/upstream/ncurses（QB） | —；CFLAGS, CXXFLAGS, LDFLAGS | B/I/P | E,H,F | [ncurses.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__ncurses/ncurses.spec#L188) L188,197,201,204,207,208,221,490 |
| platform/upstream/net-tools（QB） | —；CFLAGS, LDFLAGS, RPM_OPT_FLAGS | B/I/P | E,H,F | [net-tools.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/net-tools-2.0_20121208git-1.9/net-tools.spec#L29) L29,48,49,50,54 |
| platform/upstream/nghttp2（QB） | —；— | B/I/P | E,H | [nghttp2.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/nghttp2-1.51.0-1.1/nghttp2.spec#L51) L51,62,75 |
| platform/upstream/ninja（QB） | —；CFLAGS | B/I/P | E,H,F | [ninja.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/ninja-1.13.1-1.14/ninja.spec#L24) L24,30,32,36 |
| platform/upstream/nspr（QB） | —；CFLAGS, LDFLAGS, optflags | B/I/P | E,H,F | [nspr.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/nspr-4.36-2.2/nspr.spec#L36) L36,42,48,49,50,90 |
| platform/upstream/nss（QB） | —；CFLAGS, CXXFLAGS, LDFLAGS, RPM_OPT_FLAGS | B/I/P | E,H,F | [nss.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/nss-3.109-1.4/nss.spec#L126) L126,132,133,134,135,139,195 |
| platform/upstream/openfst（QB） | —；CXXFLAGS | B/I/P | E,H,F | [openfst.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/openfst-1.8.4-1.1/openfst.spec#L46) L46,52,53,58 |
| platform/upstream/openssl1.1（QB） | —；RPM_OPT_FLAGS | B/I/P | E,H,F | [openssl1.1.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/openssl1.1-1.1.1w-1.13/openssl1.1.spec#L57) L57,65,82,83,84,85,93,99 |
| platform/upstream/openssl3（QB） | —；RPM_OPT_FLAGS | B/I/P | E,H,F | [openssl3.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__openssl3/openssl3.spec#L53) L53,57,74,88,94 |
| platform/upstream/opus（QB） | —；— | B/I/P | E,H | [opus.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/opus-1.3.1-2.1/opus.spec#L27) L27,31,35 |
| platform/upstream/pam（QB） | —；— | B/I/P | E,H | [pam.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__pam/pam.spec#L73) L73,77,98 |
| platform/upstream/patch（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [patch.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/patch-2.8-1.12/patch.spec#L22) L22,25,27,28,34 |
| platform/upstream/patchelf（QB） | —；CFLAGS, CXXFLAGS, LDFLAGS, RPM_OPT_FLAGS | B/I/P | E,H,F | [patchelf.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/patchelf-0.16.1-1.13/patchelf.spec#L20) L20,24,25,26,27,28,38 |
| platform/upstream/pbzip2（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [pbzip2.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/pbzip2-1.1.13-1.1/pbzip2.spec#L25) L25,35,38,57 |
| platform/upstream/pcre（QB） | —；CFLAGS | B/I/P | E,H,F | [pcre.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/pcre-8.45-1.14/pcre.spec#L95) L95,100,101,122 |
| platform/upstream/pcre2（QB） | —；CFLAGS, CXXFLAGS, LDFLAGS | B/I/P | E,H,F | [pcre2.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/pcre2-10.47-1.1/pcre2.spec#L105) L105,115,117,118,119,163 |
| platform/upstream/perl（QB） | —；CFLAGS, CXXFLAGS, RPM_OPT_FLAGS, debug_package | B/I/P | E,H,F | [perl.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/perl-5.42.0-1.14/perl.spec#L23) L23,94,100,101,107,108,109,132,154 |
| platform/upstream/perl-Devel-Symdump（QB） | —；CFLAGS, optflags | B/I/P | E,H,F | [perl-Devel-Symdump.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/perl-Devel-Symdump-2.18-1.1/perl-Devel-Symdump.spec#L41) L41,46,47,53 |
| platform/upstream/perl-HTML-Parser（QB） | —；— | B/I/P | E,H | [perl-HTML-Parser.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/perl-HTML-Parser-3.83-1.1/perl-HTML-Parser.spec#L20) L20,24,28 |
| platform/upstream/perl-HTML-Tagset（QB） | —；— | B/I/P | E,H | [perl-HTML-Tagset.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/perl-HTML-Tagset-3.24-1.1/perl-HTML-Tagset.spec#L17) L17,21,25 |
| platform/upstream/perl-Module-Build（QB） | —；— | B/I/P | E,H | [perl-Module-Build.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/perl-Module-Build-0.4234-1.1/perl-Module-Build.spec#L59) L59,63,67 |
| platform/upstream/perl-PerlIO-gzip（QB） | —；— | B/I/P | E,H | [perl-PerlIO-gzip.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/perl-PerlIO-gzip-0.20-1.1/perl-PerlIO-gzip.spec#L20) L20,23,27 |
| platform/upstream/perl-Pod-Coverage（QB） | —；— | B/I/P | E,H | [perl-Pod-Coverage.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/perl-Pod-Coverage-0.23-1.1/perl-Pod-Coverage.spec#L46) L46,51,58 |
| platform/upstream/perl-Software-License（QB） | —；— | B/I/P | E,H | [perl-Software-License.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/perl-Software-License-0.104006-1.1/perl-Software-License.spec#L27) L27,31,35 |
| platform/upstream/perl-Test-Pod（QB） | —；— | B/I/P | E,H | [perl-Test-Pod.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/perl-Test-Pod-1.52-1.1/perl-Test-Pod.spec#L29) L29,34,41 |
| platform/upstream/perl-Test-Pod-Coverage（QB） | —；— | B/I/P | E,H | [perl-Test-Pod-Coverage.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/perl-Test-Pod-Coverage-1.10-1.1/perl-Test-Pod-Coverage.spec#L24) L24,29,36 |
| platform/upstream/perl-TimeDate（QB） | —；— | B/I/P | E,H | [perl-TimeDate.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/perl-TimeDate-2.33-2.1/perl-TimeDate.spec#L23) L23,27,34 |
| platform/upstream/perl-URI（QB） | —；— | B/I/P | E,H | [perl-URI.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/perl-URI-5.34-1.1/perl-URI.spec#L21) L21,25,29 |
| platform/upstream/perl-XML-Parser（QB） | —；CFLAGS, RPM_OPT_FLAGS | B/I/P | E,H,F | [perl-XML-Parser.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/perl-XML-Parser-2.47-1.12/perl-XML-Parser.spec#L41) L41,46,47,53 |
| platform/upstream/perl-gettext（QB） | —；optflags | B/I/P | E,H,F | [perl-gettext.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/perl-gettext-1.07-1.13/perl-gettext.spec#L33) L33,38,39,45 |
| platform/upstream/perl-inc-latest（QB） | —；— | B/I/P | E,H | [perl-inc-latest.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/perl-inc-latest-0.500-1.1/perl-inc-latest.spec#L79) L79,83,87 |
| platform/upstream/perl-json（QB） | —；— | B/I/P | E,H | [perl-json.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/perl-json-4.10-1.1/perl-json.spec#L34) L34,41,45 |
| platform/upstream/perl-libwww-perl（QB） | —；— | B/I/P | E,H | [perl-libwww-perl.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/perl-libwww-perl-6.81-1.1/perl-libwww-perl.spec#L25) L25,29,33 |
| platform/upstream/pkg-config（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [pkg-config.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/pkg-config-0.29.2-1.14/pkg-config.spec#L23) L23,29,30,31,41 |
| platform/upstream/popt（QB） | —；— | B/I/P | E,H | [popt.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/popt-1.16-1.12/popt.spec#L48) L48,51,55 |
| platform/upstream/procps-ng（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [procps-ng.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/procps-ng-4.0.5-1.1/procps-ng.spec#L56) L56,64,65,66,84 |
| platform/upstream/python（QB） | —；CFLAGS, LDFLAGS, RPM_OPT_FLAGS | B/I/P | E,H,F | [python.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-2.7.18-1.13/python.spec#L106) L106,137,139,140,141,158,165 |
| platform/upstream/python-MarkupSafe（QB） | —；CFLAGS, optflags | B/I/P | E,H,F | [python-MarkupSafe.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-MarkupSafe-1.0-1.1/python-MarkupSafe.spec#L39) L39,42,44,47 |
| platform/upstream/python-appdirs（QB） | —；— | B/I/P | E,H | [python-appdirs.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-appdirs-1.4.0-1.1/python-appdirs.spec#L46) L46,51,55 |
| platform/upstream/python-argparse（QB） | —；— | B/I/P | E,H | [python-argparse.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-argparse-1.4.0-1.1/python-argparse.spec#L60) L60,69,73 |
| platform/upstream/python-funcsigs（QB） | —；debug_package | B/I/P | E,H | [python-funcsigs.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-funcsigs-1.0.2-1.1/python-funcsigs.spec#L18) L18,42,45,49 |
| platform/upstream/python-libxml2（QB） | —；CFLAGS, optflags | B/I/P | E,H,F | [python-libxml2.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-libxml2-2.15.1-1.1/python-libxml2.spec#L33) L33,39,40,56 |
| platform/upstream/python-linecache2（QB） | —；— | B/I/P | E,H | [python-linecache2.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-linecache2-1.0.0-1.1/python-linecache2.spec#L45) L45,50,54 |
| platform/upstream/python-lxml（QB） | —；CFLAGS | B/I/P | E,H,F | [python-lxml.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-lxml-4.6.2-1.1/python-lxml.spec#L26) L26,34,35,38 |
| platform/upstream/python-magic（QB） | —；— | B/I/P | E,H | [python-magic.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-magic-5.41-1.1/python-magic.spec#L23) L23,27,32 |
| platform/upstream/python-mako（QB） | —；debug_package | B/I/P | E,H | [python-mako.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-mako-1.0.6-1.1/python-mako.spec#L24) L24,59,62,66 |
| platform/upstream/python-markdown（QB） | —；— | B/I/P | E,H | [python-markdown.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-markdown-3.1.1-1.1/python-markdown.spec#L29) L29,37,42 |
| platform/upstream/python-mock（QB） | —；— | B/I/P | E,H | [python-mock.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-mock-3.0.5-1.1/python-mock.spec#L48) L48,54,58 |
| platform/upstream/python-nose（QB） | —；— | B/I/P | E,H | [python-nose.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-nose-1.2.1-1.1/python-nose.spec#L35) L35,40,46；[python3-nose.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-nose-1.2.1-1.1/python3-nose.spec#L34) L34,39,45 |
| platform/upstream/python-packaging（QB） | —；debug_package | B/I/P | E,H | [python-packaging.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-packaging-20.8-1.1/python-packaging.spec#L23) L23,52,55,59 |
| platform/upstream/python-pbr（QB） | —；— | B/I/P | E,H | [python-pbr.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-pbr-5.5.1-1.1/python-pbr.spec#L54) L54,59,63 |
| platform/upstream/python-ply（QB） | —；— | B/I/P | E,H | [python-ply.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-ply-3.11-1.1/python-ply.spec#L28) L28,41,44 |
| platform/upstream/python-pygments（QB） | —；— | B/I/P | E,H | [python-pygments.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-pygments-2.7.3-1.1/python-pygments.spec#L27) L27,31,37 |
| platform/upstream/python-pyparsing（QB） | —；— | B/I/P | E,H | [python-pyparsing.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-pyparsing-2.2.0-1.1/python-pyparsing.spec#L43) L43,46,52 |
| platform/upstream/python-setuptools（QB） | —；— | B/I/P | E,H | [python-setuptools.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-setuptools-44.1.1-1.3/python-setuptools.spec#L53) L53,68,73 |
| platform/upstream/python-six（QB） | —；— | B/I/P | E,H | [python-six.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-six-1.15.0-1.1/python-six.spec#L40) L40,43,49 |
| platform/upstream/python-traceback2（QB） | —；— | B/I/P | E,H | [python-traceback2.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-traceback2-1.4.0-1.1/python-traceback2.spec#L43) L43,48,52 |
| platform/upstream/python-unittest2（QB） | —；— | B/I/P | E,H | [python-unittest2.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python-unittest2-1.1.0-1.1/python-unittest2.spec#L49) L49,52,56 |
| platform/upstream/python3（QB） | —；CFLAGS, CXXFLAGS, optflags | B/I/P | E,H,F | [python3.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-3.14.2-1.9/python3.spec#L155) L155,192,195,196,249,252；[python3-base.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-base-3.14.2-1.9/python3-base.spec#L237) L237,274,275,276,279,352,356 |
| platform/upstream/python3-MarkupSafe（QB） | —；— | B/I/P | E,H | [python3-MarkupSafe.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-MarkupSafe-3.0.3-1.3/python3-MarkupSafe.spec#L28) L28,34,37 |
| platform/upstream/python3-appdirs（QB） | —；— | B/I/P | E,H | [python3-appdirs.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-appdirs-1.4.4-1.1/python3-appdirs.spec#L45) L45,48,52 |
| platform/upstream/python3-build（QB） | —；— | B/I/P | E,H | [python3-build.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-build-1.0.3-1.1/python3-build.spec#L25) L25,30,34 |
| platform/upstream/python3-calver（QB） | —；— | B/I/P | E,H | [python3-calver.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-calver-2025.10.20-1.3/python3-calver.spec#L25) L25,31,34 |
| platform/upstream/python3-cython（QB） | —；— | B/I/P | E,H | [python3-cython.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-cython-3.2.4-1.3/python3-cython.spec#L42) L42,48,51 |
| platform/upstream/python3-editables（QB） | —；— | B/I/P | E,H | [python3-editables.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-editables-0.5-1.3/python3-editables.spec#L27) L27,30,34 |
| platform/upstream/python3-flit_core（QB） | —；— | B/I/P | E,H | [python3-flit_core.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-flit_core-3.12.0-1.1/python3-flit_core.spec#L19) L19,22,26 |
| platform/upstream/python3-hatchling（QB） | —；— | B/I/P | E,H | [python3-hatchling.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-hatchling-1.28.0-1.3/python3-hatchling.spec#L34) L34,40,43 |
| platform/upstream/python3-libxml2（QB） | —；CFLAGS, optflags | B/I/P | E,H,F | [python3-libxml2.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-libxml2-2.15.1-1.1/python3-libxml2.spec#L30) L30,34,35,51 |
| platform/upstream/python3-lxml（QB） | —；CFLAGS | B/I/P | E,H,F | [python3-lxml.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-lxml-6.0.2-1.3/python3-lxml.spec#L33) L33,41,42,45 |
| platform/upstream/python3-magic（QB） | —；— | B/I/P | E,H | [python3-magic.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-magic-5.46-1.1/python3-magic.spec#L23) L23,27,32 |
| platform/upstream/python3-mako（QB） | —；— | B/I/P | E,H | [python3-mako.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-mako-1.3.10-1.3/python3-mako.spec#L41) L41,47,50 |
| platform/upstream/python3-markdown（QB） | —；— | B/I/P | E,H | [python3-markdown.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-markdown-3.10.0-1.4/python3-markdown.spec#L27) L27,32,36 |
| platform/upstream/python3-packaging（QB） | —；— | B/I/P | E,H | [python3-packaging.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-packaging-25.0-1.9/python3-packaging.spec#L29) L29,33,35 |
| platform/upstream/python3-pathspec（QB） | —；— | B/I/P | E,H | [python3-pathspec.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-pathspec-1.0.1-1.4/python3-pathspec.spec#L24) L24,28,31 |
| platform/upstream/python3-pbr（QB） | —；— | B/I/P | E,H | [python3-pbr.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-pbr-7.0.3-1.1/python3-pbr.spec#L26) L26,33,36 |
| platform/upstream/python3-pip（QB） | —；— | B/I/P | E,H | [python3-pip.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-pip-25.3-1.1/python3-pip.spec#L25) L25,32,38 |
| platform/upstream/python3-pluggy（QB） | —；— | B/I/P | E,H | [python3-pluggy.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-pluggy-1.6.0-1.3/python3-pluggy.spec#L27) L27,33,36 |
| platform/upstream/python3-ply（QB） | —；— | B/I/P | E,H | [python3-ply.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-ply-3.11-1.1/python3-ply.spec#L28) L28,41,44 |
| platform/upstream/python3-pygments（QB） | —；— | B/I/P | E,H | [python3-pygments.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-pygments-2.19.2-1.3/python3-pygments.spec#L28) L28,34,37 |
| platform/upstream/python3-pyparsing（QB） | —；— | B/I/P | E,H | [python3-pyparsing.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-pyparsing-3.3.1-1.8/python3-pyparsing.spec#L32) L32,38,41 |
| platform/upstream/python3-pyproject_hooks（QB） | —；— | B/I/P | E,H | [python3-pyproject_hooks.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-pyproject_hooks-1.2.0-1.7/python3-pyproject_hooks.spec#L30) L30,34,37 |
| platform/upstream/python3-setuptools（QB） | —；— | B/I/P | E,H | [python3-setuptools.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-setuptools-80.9.0-1.3/python3-setuptools.spec#L30) L30,46,49 |
| platform/upstream/python3-setuptools_scm（QB） | —；— | B/I/P | E,H | [python3-setuptools_scm.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-setuptools_scm-9.2.2-1.3/python3-setuptools_scm.spec#L28) L28,32,34 |
| platform/upstream/python3-six（QB） | —；— | B/I/P | E,H | [python3-six.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-six-1.17.0-1.1/python3-six.spec#L24) L24,28,31 |
| platform/upstream/python3-trove_classifiers（QB） | —；— | B/I/P | E,H | [python3-trove_classifiers.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-trove_classifiers-2025.12.1.14-1.3/python3-trove_classifiers.spec#L23) L23,27,30 |
| platform/upstream/python3-typing_extensions（QB） | —；— | B/I/P | E,H | [python3-typing_extensions.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-typing_extensions-4.15.0-1.3/python3-typing_extensions.spec#L45) L45,49,52 |
| platform/upstream/python3-wheel（QB） | —；— | B/I/P | E,H | [python3-wheel.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/python3-wheel-0.46.1-1.1/python3-wheel.spec#L31) L31,36,44 |
| platform/upstream/qemu（QB） | —；— | B/I/P | E,H | [qemu-linux-user.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/qemu-linux-user-9.2.3.1-3.4/qemu-linux-user.spec#L52) L52,58,62 |
| platform/upstream/qemu-accel（QB） | —；— | B/I/P | E,H | [qemu-accel-aarch64.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__qemu-accel/qemu-accel-aarch64.spec#L124) L124,126,131；[qemu-accel-armv7l.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__qemu-accel/qemu-accel-armv7l.spec#L124) L124,126,131；[qemu-accel-riscv64.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__qemu-accel/qemu-accel-riscv64.spec#L124) L124,126,131 |
| platform/upstream/readline（QB） | `__cc`, `_toolchain`, `toolchain_is`；CFLAGS, LDFLAGS | B/I/P | E,H,F,T,X | [readline.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/readline-5.2-1.14/readline.spec#L118) L69,115,118,126,127,128,129,130,133,135,150 |
| platform/upstream/rfcdiff（QB） | —；— | I/P | E,H | [rfcdiff.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__rfcdiff/rfcdiff.spec#L25) L25,30 |
| platform/upstream/rpm（QB） | —；CFLAGS, LDFLAGS, optflags | B/I/P | E,H,F | [rpm.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__rpm/rpm.spec#L142) L142,166,169,170,172,201 |
| platform/upstream/setup（QB） | —；— | B/I/P | E,H | [setup.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/setup-0.9-2.6/setup.spec#L35) L35,41,47 |
| platform/upstream/sgml-skel（QB） | —；— | B/I/P | E,H | [sgml-skel.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/sgml-skel-0.7.2-1.1/sgml-skel.spec#L34) L34,44,50 |
| platform/upstream/shadow-utils（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [shadow-utils.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__shadow-utils/shadow-utils.spec#L35) L35,38,39,40,47 |
| platform/upstream/smack（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [smack.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/smack-1.3.1-1.12/smack.spec#L37) L37,43,44,45,50 |
| platform/upstream/sqlite（QB） | —；CFLAGS, optflags | B/I/P | E,H,F | [sqlite.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/sqlite-3.51.0-1.14/sqlite.spec#L78) L78,86,87,88,89,91,111 |
| platform/upstream/taglib（QB） | —；— | B/I/P | E,H | [taglib.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/taglib-1.13.1-1.1/taglib.spec#L28) L28,36,42 |
| platform/upstream/tcl（QB） | —；— | B/I/P | E,H | [tcl.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/tcl-8.6.17-1.1/tcl.spec#L45) L45,50,63 |
| platform/upstream/tensorflow2（仅manifest） | —；CC, CFLAGS, CXX, CXXFLAGS | B/I/P | E,H,F | [tensorflow2.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/tensorflow2-2.18.0-1.1/tensorflow2.spec#L123) L123,159,170,171,204,205,206,245,246,262 |
| platform/upstream/texinfo（QB） | —；CFLAGS, CXXFLAGS, LDFLAGS | B/I/P | E,H,F | [texinfo.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/texinfo-7.2-1.14/texinfo.spec#L57) L57,61,63,64,65,80 |
| platform/upstream/tiff（QB） | —；— | B/I/P | E,H | [tiff.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/tiff-4.7.0-1.1/tiff.spec#L46) L46,50,54 |
| platform/upstream/tinyxml2（QB） | —；CFLAGS | B/I/P | E,H,F | [tinyxml2.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/tinyxml2-11.0.0-1.1/tinyxml2.spec#L35) L35,41,42,47 |
| platform/upstream/toybox（QB） | `_toolchain`；CC, CFLAGS | B/I/P | E,H,F,X | [toybox.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__toybox/toybox.spec#L133) L121,130,133,134,137,139 |
| platform/upstream/tzdata（QB） | `__cc`；CC, CFLAGS, LDFLAGS, RPM_OPT_FLAGS | B/I/P | E,H,F,T | [tzdata.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__tzdata/tzdata.spec#L35) L23,29,35,36,37,41 |
| platform/upstream/unzip（QB） | `__cc`；CC, LDFLAGS | B/I/P | E,H,T | [unzip.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/unzip-610c25-1.4/unzip.spec#L47) L30,44,45,47,49 |
| platform/upstream/update-alternatives（QB） | —；CFLAGS, CXXFLAGS, LDFLAGS | B/I/P | E,H,F | [update-alternatives.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/update-alternatives-1.22.21-1.1/update-alternatives.spec#L46) L46,50,51,52,53,62 |
| platform/upstream/userspace-rcu（QB） | —；— | B/I/P | E,H | [userspace-rcu.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/userspace-rcu-0.13.2-2.1/userspace-rcu.spec#L34) L34,38,46 |
| platform/upstream/uthash（QB） | —；— | B/I/P | E,H | [uthash.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/uthash-2.3.0-1.12/uthash.spec#L27) L27,33,36 |
| platform/upstream/util-linux（QB） | `__cc`；CFLAGS, LDFLAGS, optflags | B/I/P | E,H,F,T | [util-linux.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/util-linux-2.41.2-1.7/util-linux.spec#L224) L185,196,199,200,201,224,226 |
| platform/upstream/util-macros（QB） | —；— | B/I/P | E,H | [util-macros.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/util-macros-1.19.0-1.1/util-macros.spec#L16) L16,20,24 |
| platform/upstream/v4l-utils（QB） | —；CFLAGS, optflags | B/I/P | E,H,F | [v4l-utils.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/v4l-utils-1.6.0-7.1/v4l-utils.spec#L65) L65,84,85,89 |
| platform/upstream/vim（QB） | —；CFLAGS, LDFLAGS, optflags | B/I/P | E,H,F | [vim.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/vim-9.1.1918-1.1/vim.spec#L80) L80,95,96,97,98,134 |
| platform/upstream/vtable-dumper（QB） | —；CC | B/I/P | E,H | [vtable-dumper.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/platform__upstream__vtable-dumper/vtable-dumper.spec#L18) L18,22,23,25 |
| platform/upstream/xdgmime（QB） | —；CFLAGS | B/I/P | E,H,F | [xdgmime.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/xdgmime-0.0.20-2.1/xdgmime.spec#L23) L23,27,28,35 |
| platform/upstream/xmlcharent（QB） | —；— | B/I/P | E,H | [xmlcharent.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/xmlcharent-0.3-405.1/xmlcharent.spec#L45) L45,54,86 |
| platform/upstream/xmlsec1（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [xmlsec1.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/xmlsec1-1.3.9-1.1/xmlsec1.spec#L71) L71,78,91,93 |
| platform/upstream/xmlstarlet（QB） | `_toolchain`, `toolchain_is`；CFLAGS, LDFLAGS | B/I/P | E,H,F,X | [xmlstarlet.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/xmlstarlet-1.6.1-1.1/xmlstarlet.spec#L29) L22,27,28,29,30,31,35,37,42 |
| platform/upstream/xxhash（QB） | `build_ldflags`；CFLAGS, CXXFLAGS, LDFLAGS, optflags | B/I/P | E,H,F,L | [xxhash.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/xxhash-0.8.3-1.1/xxhash.spec#L44) L37,41,42,43,44,47,48,49,50 |
| platform/upstream/xz（QB） | `_toolchain`, `toolchain_is`；CFLAGS, optflags | B/I/P | E,H,F,X | [xz.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/xz-5.8.1-1.13/xz.spec#L18) L18,19,80,88,92,97,102,103,104,107,110,114,117,127 |
| platform/upstream/yasm（QB） | —；CFLAGS, CXXFLAGS, LDFLAGS | B/I/P | E,H,F | [yasm.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/yasm-1.3.0-1.4/yasm.spec#L20) L20,26,27,28,29,35 |
| platform/upstream/zip（QB） | `__cc`；CC, CFLAGS | B/I/P | E,H,F,T | [zip.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/zip-3.0-1.1/zip.spec#L46) L25,43,44,46,48 |
| platform/upstream/zlib（QB） | —；CFLAGS, LDFLAGS, optflags | B/I/P | E,H,F | [zlib.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/zlib-1.3.1-1.14/zlib.spec#L71) L71,77,78,80,92 |
| platform/upstream/zstd（QB） | —；CFLAGS, CXXFLAGS, LDFLAGS | B/I/P | E,H,F | [zstd.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/zstd-1.5.7-1.13/zstd.spec#L67) L67,72,73,74,75,82 |
| product/upstream/bash（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [bash.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/bash-3.2.57-1.14/bash.spec#L33) L33,40,41,42,61 |
| product/upstream/coreutils（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [coreutils.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/product__upstream__coreutils/coreutils.spec#L48) L48,51,54,55,71 |
| product/upstream/cpio（QB） | —；— | B/I/P | E,H | [cpio.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/cpio-2.8-1.1/cpio.spec#L33) L33,46,53 |
| product/upstream/findutils（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [findutils.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/product__upstream__findutils/findutils.spec#L37) L37,41,54,55,65 |
| product/upstream/gawk（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [gawk.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/gawk-3.1.5-1.1/gawk.spec#L41) L41,60,61,62,76 |
| product/upstream/gdbm（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [gdbm.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/gdbm-1.8.3-1.15/gdbm.spec#L47) L47,63,64,65,76 |
| product/upstream/gmp（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [gmp.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/gmp-4.2.1-1.13/gmp.spec#L47) L47,55,56,57,65 |
| product/upstream/grep（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [grep.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/product__upstream__grep/grep.spec#L27) L27,31,32,33,45 |
| product/upstream/gzip（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [gzip.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/gzip-1.3.12-1.13/gzip.spec#L23) L23,29,30,31,39 |
| product/upstream/sed（QB） | `_toolchain`, `toolchain_is`；CFLAGS, LDFLAGS, optflags | B/I/P | E,H,F,X | [sed.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/specs/sed-4.1c-1.13/sed.spec#L16) L16,17,29,37,39,40,48,49,50,51,68,74 |
| product/upstream/tar（QB） | —；CFLAGS, LDFLAGS | B/I/P | E,H,F | [tar.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/product__upstream__tar/tar.spec#L28) L28,32,42,43,44,55,56 |
| product/upstream/which（QB） | —；CFLAGS | B/I/P | E,H,F | [which.spec](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/qb-specs/product__upstream__which/which.spec#L18) L18,22,23,28 |


直接分支原文与后果（[完整上下文摘录](../../tools/bolt/results/qb-fail-20261028/meta/buildconf/critical-spec-excerpts.txt)，每段注明具体spec文件）：

| 包 | 原文和行号 | 直接使用Base配置后的差异 |
|---|---|---|
| iptables | L80–84 `%{?_toolchain:` / `%if %{toolchain_is clang}` / sed删除`-Wno-stringop-truncation` | 外层变假，跳过Clang参数清理；不是宏解析失败 |
| kmod | L102–106 `%{?_toolchain:` / `%if !%{toolchain_is clang}` / `CFLAGS+=" -Wno-maybe-uninitialized"` | 旧默认Clang与新Base都不加这项；若旧选GCC override则分支有差异。编译器选择仍有变化 |
| readline | L128–133 `defined _toolchain` / `toolchain_is gcc` / else加`-ftree-loop-linear` | 默认Clang分支原不加；无_toolchain的Base分支加GCC选项 |
| sed | L16–20条件BuildRequires compiler-rt；L50–63 Clang运行`llvm-profdata merge`，else用普通反馈宏 | compiler-rt不再由此条件引入；do_profiling启用时切换反馈数据/命令；有外层保护 |
| xz | L18–22条件compiler-rt；L103–115 Clang的LLVM_PROFILE_FILE/llvm-profdata与else反馈目录 | 同样改变依赖和启用PGO时的工作流；有外层保护 |
| xmlstarlet | L29–33 `_toolchain`保护下加`-Wno-error=incompatible-function-pointer-types` | 新配置跳过Clang专用警告参数；不直接解析失败 |
| toybox | L100–102 `%{?!_toolchain:` / `export CC="gcc"` | 最小动态toybox显式选择GCC，不再继承原Clang环境 |
| GCC原生/交叉、glibc | gcc L30 / glibc L36 `_toolchain_override gcc` | 原来也选择GCC；不能断言这些包因Base配置改成不同编译器家族。需比较宏工具拼写/选项 |
| LLVM | f308 L18–37、198–207 | release开关、debug子包、去-g和debug目录清理定义发生变化，详见7.1 |

LLVM L13–16已经在三架构使用`%bcond_without mlgo`，L63–64自备jobs=6与verify=0默认值。因此配置删除三项MLGO宏，**不等于该LLVM spec必定关闭MLGO或改jobs**；但旧配置 `_with_mlgo`还参与全局Clang选项选择，完整链仍需核验。

31个变化宏的覆盖统计（数量是spec记录/版本而非唯一项目；0表示无直接语法引用，不表示没有宏内部或平台间接依赖）：

| 宏 | 命中spec记录数（包含注释外的段入口） |
|---|---|
| `___optflags_toolchain_clang` | 0 |
| `___optflags_toolchain_gcc` | 0 |
| `__ar` | 8 |
| `__ar_clang` | 0 |
| `__ar_gcc` | 0 |
| `__cc` | 30 |
| `__cc_clang` | 0 |
| `__cc_gcc` | 0 |
| `__cxx` | 5 |
| `__cxx_clang` | 0 |
| `__cxx_gcc` | 0 |
| `__global_cflags` | 0 |
| `__optflags` | 0 |
| `__optflags_toolchain` | 0 |
| `__optflags_toolchain_clang` | 0 |
| `__optflags_toolchain_gcc` | 0 |
| `__ranlib` | 7 |
| `__ranlib_clang` | 0 |
| `__ranlib_gcc` | 0 |
| `_ldflags_arch_extra` | 0 |
| `_project` | 0 |
| `_toolchain` | 15 |
| `_with_mlgo` | 0 |
| `build` | 398 |
| `build_ldflags` | 1 |
| `distribution` | 0 |
| `install` | 403 |
| `mlgo_build_jobs` | 2 |
| `mlgo_verify_configure_only` | 2 |
| `prep` | 403 |
| `toolchain_is` | 10 |


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

第一件本地meta提交fd60db96806a372404bd4f04e68d4ba586290147原样保留，未推送；只修DOD名称，不包含新的build.conf方案。第二件结论不变：两个快照构建LLVM用到的工具链**不完全相同**。第三件依用户回复暂停，没有启动新的gbs export、构建根环境准备或完整构建。

回复到达前已独立完成debuglink的本地实现草稿、346项测试、39号旧产物副本上的轻量符号/布局检查，并生成本地detached提交569d734d0ccb2959e3f33494593c5cd46a01c347（tree e3fff52ab97b479bf3e1fd5bc5b90f842756c346，父6e9d4f2）；未推任何远端、没有新RPM，不能标为正式打包认证。相关工作树和未完成证据保留，本次GitHub提交只包含本调查文档/证据/STATUS，不携带暂停的源码或测试改动。后台日志按约定记录status=stopped及用户暂停原因。

查找阶段有两处路径更正：Tools目录实际位于`TIZEN/Tools/`；POSIX sh不展开`{base,toolchain}`，改为显式两个路径。均在只读查找中纠正，没有执行包构建或改配置。spec获取用HTTPS顺序流式解包，只保存spec与来源/大小/SHA；读取到全部spec后停止下载，记录的download_prefix_sha256明确不是完整SRPM SHA。未执行来自spec的脚本。对未知加载器行为、历史实际生效配置和包级最终二进制影响，均保留“未确认/静态推导”边界。
