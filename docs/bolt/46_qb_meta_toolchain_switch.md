# 46：Toolchain 切换主项目来源的上传前检查（2026-10-28）

**两个评审都没有上传**：Base 命中缺包的实际 BuildRequires；Unified 的第二层 DOD 创建方式尚未证明，且现有源码清单有17个仓库不在新来源中。Base 三架构各少11个包，Unified 与 Base 合并后仍少115/115/114个包名，不能判为“缺少但不影响”；部分只是别名/配置变体，不把包名差异全部当作编译失败。**QB是否真正使用Toolchain自己的project_config，仍待修复合入后的第一次QB确认**，本轮没有触发或修改QB。

## 1. 范围、身份和停止状态

用户已确认总部意图：使用对应主项目的代码和RPM依赖，保留Toolchain自身的project_config。开始前读取STATUS及44/45号；本轮只有公开元数据/spec/日志读取、临时RPM解包和4次最小C编译，没有软件包构建、系统安装、配置修改或Gerrit写入。

只读fetch后的master为`7b2f2ae2d0e0cdc42307454c73c10be23b6d0ef5`，四个相关项目相对上次master没有变化。原本地两行修复`fd60db96806a372404bd4f04e68d4ba586290147`保留；没有执行rebase，因为上传前门禁已不满足。第二个评审没有生成提交或猜测一份可用的两层DOD配置。两个评审互相独立，均无change编号/URL；没有执行任何`git push ... refs/for/master`。

| 检查 | Base-Toolchain / Dev | Unified-Toolchain |
|---|---|---|
| 项目原件、当前master | 已保存；仅旧本地两行diff | 两目录全部6个文件原样保存，project_config SHA不变 |
| 缺包与依赖 | **FAIL**：gcc-armv7hl依赖binutils-armv7hl | 元数据初查有缺包/旧RPM依赖风险；因更早停止条件，不做全1046仓库spec认证 |
| 三架构project_config | 必装/运行脚本/Support等有提供者；Keep/条件Substitute有历史缺项，严格“所有点名项齐全”不成立 | own配置Substitute的pkgconfig(gl)无提供者；继承配置未认证 |
| MLGO最小编译 | **PASS 4/4**：旧/新clang × ARMv7/AArch64 | own project_config无该参数，条件项不适用；所需Base层clang已在左侧实测 |
| 源码清单完整性 | 复用45号251实际仓库spec证据 | **FAIL**：1046 → 固定来源1030；缺17、增1、267个共同仓库revision变化 |
| DOD机制 | 默认命名依据1211018保留 | **STOP**：需要Base层，但未证实如何同时生成第二个DOD |
| XML/提交/上传 | 已有两行diff；未rebase、未上传 | 原XML合法；未生成修改diff/新提交、未上传 |

本报告的后续表格是停止前已取得的只读检查和诊断记录，不把未执行的完整依赖认证标成PASS。用户规定“命中缺包依赖或配置缺失则不上传”，没有自行豁免或改目标包清单。

## 2. Base：三架构缺包、spec与provides

旧固定快照为`Tizen-Base-Toolchain/tizen-base-toolchain_20261013.024319`；新固定快照为`Tizen-Base/tizen-base_20261026.005418`。45号保存的原始primary包含所有架构，本轮重新解析armv7l/aarch64/x86_64，各自合并noarch，未将上一轮仅x86的JSON误当成全仓库。完整primary来源/SHA仍见45号snapshots/provenance.json；本轮解析结果在`repos/toolchain/packages-all.json`和`repos/base/packages-all.json`，含provides、requires的比较操作符/epoch/version/release。

| Base中缺少的包名 | x86_64 / armv7l / aarch64 | 251个实际仓库spec的静态命中/影响 |
|---|---|---|
| binutils-armv7hl | 三者均缺 | gcc-armv7hl.spec L1/L101：BuildRequires binutils-armv7hl，无替代provider，触发停止 |
| coreutils-su | 三者均缺 | 未见直接或已展开简单宏的BuildRequires/Requires命中；不等同全条件求解PASS |
| gcc-armv7hl | 三者均缺 | 未见直接或已展开简单宏的BuildRequires/Requires命中；不等同全条件求解PASS |
| libtensorflow2-aot-runtime | 三者均缺 | 未见直接或已展开简单宏的BuildRequires/Requires命中；不等同全条件求解PASS |
| tensorflow2-aot-devel | 三者均缺 | 未见直接或已展开简单宏的BuildRequires/Requires命中；不等同全条件求解PASS |
| tensorflow2-lite-devel | 三者均缺 | 未见直接或已展开简单宏的BuildRequires/Requires命中；不等同全条件求解PASS |
| tensorflow2-lite-flatbuf-schema | 三者均缺 | 未见直接或已展开简单宏的BuildRequires/Requires命中；不等同全条件求解PASS |
| tensorflow2-lite-util | 三者均缺 | 未见直接或已展开简单宏的BuildRequires/Requires命中；不等同全条件求解PASS |
| toybox-full | 三者均缺 | 未见直接或已展开简单宏的BuildRequires/Requires命中；不等同全条件求解PASS |
| toybox-symlinks-full | 三者均缺 | 未见直接或已展开简单宏的BuildRequires/Requires命中；不等同全条件求解PASS |
| toybox-symlinks-nslookup | 三者均缺 | 未见直接或已展开简单宏的BuildRequires/Requires命中；不等同全条件求解PASS |

明确命中的原文（[完整上下文](../../tools/bolt/results/qb-meta-switch-20261028/base-dependency-stop.txt)）：

```spec
# packaging/gcc-armv7hl.spec（快照保留文件的原行号）
1: %define cross armv7hl
101: %{?cross:BuildRequires: binutils-%{cross}}
```

`cross`已定义为armv7hl，因此条件内容是`BuildRequires: binutils-armv7hl`，没有版本限定。旧仓库有此provider，新三个架构及noarch均无；也没有其他包通过Provides提供该名字。该spec的VCS与QB 251个实际仓库中的`platform/upstream/gcc`提交匹配，来源和匹配证据沿用45号`project-spec-coverage.json`。即使同一项目也可能从源码再产出binutils交叉包，本轮没有验证调度闭包，且用户门禁明确“命中即停”，不能以这种可能性豁免。

检查不是只grep11个包名：从缺包收集全部Provides和primary中的文件能力名，再检查BuildRequires/Requires原文、简单宏展开和条件上下文；同时检查旧二进制RPM的Requires，包括版本限定。[全部spec命中/未展开行及二进制依赖](../../tools/bolt/results/qb-meta-switch-20261028/base-missing-dependencies.json)。3条旧二进制依赖均属于也被移除的包自身：tensorflow2-aot-devel和tensorflow2-lite-flatbuf-schema都要求tensorflow2-lite-devel = 2.18.0-1.1；toybox-symlinks-full要求toybox-full = 0.6.0-1.4。它们不是证明251仓库里另有三个消费者。

边界：这不是完整RPM条件/版本求解器；未解析完的宏行原样列出，替代provider按能力名列出但不擅自认证版本范围。初次扫描只识别行首BuildRequires，随后发现GCC的条件宏包装，在出结论前补为识别宏内部依赖并重跑；原始spec没有改动。最终有确定的阻断，不以“其他未命中”宣称全项目依赖安全。

### 2.1 project_config点名包

使用本机libbuild的`Build::read_config_dist`分别解析三架构，展开`%{build_hostarch}=x86_64`及架构条件；只读取配置，不执行spec。[每个点名项、原行号、provider及旧仓库对照](../../tools/bolt/results/qb-meta-switch-20261028/base-config-providers.tsv)；[JSON](../../tools/bolt/results/qb-meta-switch-20261028/base-config-providers.json)。

- Preinstall、Runscripts、Required、Support、VMinstall：本轮三个目标上都找到了提供者，包括ARM/AArch64所需的clang-accel-x86_64-*；不能误报这些预安装包已从Base删除。
- Keep以下11个名字三架构均无同名或Provides：`glib2, libada, libcloog, libmpc, libmpfr, libppl, libppl_c, nss-softokn-freebl, perl-libs, tizen-rpm-config, xz-lzma-compat`；它们在旧固定仓库也无provider。Keep并不是强制安装要求，不能据此断言这次换仓库新增11个编译失败，但也不能把用户要求的“每个点名项都有提供者”标为PASS。
- Substitute左侧是触发名，不要求它本身有RPM；右侧逐项检查。32bit RHS、armv7hl accel RHS无provider；其他架构的accel在它们自己的目标仓库中有provider，在当前目标上没有。替换规则是否触发需结合实际依赖，未将这些全部当作每个架构的必装缺失。完整触发名和跨架构provider见表。
- 上述历史/条件项不扩大第一评审的两行修改范围；本轮未修改project_config，也没有自行清理其遗留配置。

### 2.2 MLGO：新旧RPM实际单文件编译

下载并验primary SHA的clang RPM及执行所需glibc/libgcc/libstdc++/zlib x86_64 RPM，解到本轮临时目录；未运行RPM脚本、未安装到系统。用各自glibc loader与library-path调用该clang，`--list`记录确认运行库来源；这是ELF运行依赖闭包，不是安装完整RPM事务（没有为普通包脚本的系统工具要求做系统安装）。C源码无头文件、只编译不链接，使用`--no-default-config`避免宿主默认配置干扰。

```text
--target=<armv7l-tizen-linux-gnueabi 或 aarch64-tizen-linux-gnu>
-O2 -mllvm=-regalloc-enable-advisor=release
-mllvm=-enable-ml-inliner=release -c mlgo.c -o <本轮临时对象>
```

本地限额仅用于探测：nice19、ionice idle、地址空间4GiB、禁core；没有写入任何发布配置。stdout/stderr、完整argv、耗时、对象大小/SHA及ELF机器类型均留证。

| RPM版本 | ARMv7 rc | AArch64 rc | 结果 |
|---|---:|---:|---|
| Toolchain clang 22.1.8-3.1 | 0 | 0 | 非空ARM/AArch64 ET_REL对象；stderr空 |
| Base clang 22.1.8-6.5 | 0 | 0 | 非空ARM/AArch64 ET_REL对象；stderr空 |

[测试记录](../../tools/bolt/results/qb-meta-switch-20261028/mlgo/tests.json)；[下载URL、大小、SHA](../../tools/bolt/results/qb-meta-switch-20261028/mlgo/downloads.json)；[clang实体身份](../../tools/bolt/results/qb-meta-switch-20261028/mlgo/clang-identities.json)。这说明两套二进制接受并能执行这两个advisor选项，不证明所有训练模型、全量性能或整个Toolchain构建都已认证。project_config L112–117本身还有i686/x86_64条件，L94–100定义ARM/AArch64的_with_mlgo；实测按用户要求显式传这两个选项，没有将复杂宏条件简化成所有架构必然自动使用。

### 2.3 第一评审的diff及状态

原本地提交未改写，[两行完整diff](../../tools/bolt/results/qb-meta-switch-20261028/base-existing.diff)：

```diff
TIZEN/Tizen/Tizen-Base-Toolchain/project_meta:
-    <path project="DOD:Tizen-Base" repository="standard" />
+    <path project="DOD:Tizen-Base-Toolchain" repository="standard" />
TIZEN/Tizen/Tizen-Base-Dev/project_meta:
-    <path project="DOD:Tizen-Base" repository="standard" />
+    <path project="DOD:Tizen-Base-Dev" repository="standard" />
```

没有rebase、没有上传、没有添加reviewer。Base-Dev没有被额外改造；它与Toolchain打包在同一个两行评审中，整个评审受上述失败门禁阻断。

## 3. Unified：现状、快照和依赖层

[项目全文件及SHA来源](../../tools/bolt/results/qb-meta-switch-20261028/metadata-provenance.json)；[结构化拓扑](../../tools/bolt/results/qb-meta-switch-20261028/unified-topology.json)。两个目录都只有project_meta、snapshot_info、project_config、project_env、manifest.xml、candidate_snapshot这6个文件，没有meta-dod或project_config_dod。两个project_meta都没有显式path；**0个静态DOD引用不等于运行时无需DOD**。

| 项目 | 自身latest/reference | 基础来源 | 架构 |
|---|---|---|---|
| Unified-Toolchain | latest 20261027.063617 / reference 20261016.052151 | snapshot_info为Base-Toolchain 20261013.140248；最近QB实际选择20261026.051209 | standard: armv7l,aarch64,x86_64 |
| Unified | latest/reference 20261027.231956 | Base 20261026.005418 | standard三架构；另外standard_gcov仅armv7l、emulator仅x86_64 |

standard架构列表相同；完整仓库/架构集合不相同，不能把额外emulator源混成standard验收。公开`reference/build.xml`确认当前reference确为`tizen-unified_20261027.231956`，固定快照build.xml中base_id明确为`tizen-base_20261026.005418`。三架构packages子目录均HTTP200；debug采用平铺文件布局，debug根目录HTTP200且明确列出三架构RPM，不能用不存在的debug/<arch>/目录判断仓库缺失。primary中也有三个架构和noarch。[公开访问与SHA](../../tools/bolt/results/qb-meta-switch-20261028/repo-download-provenance.json)；[debug根目录检查](../../tools/bolt/results/qb-meta-switch-20261028/debug-discovery.json)；[debug平铺布局/架构计数](../../tools/bolt/results/qb-meta-switch-20261028/debug-layout.json)；[reference build.xml](../../tools/bolt/results/qb-meta-switch-20261028/unified-reference-build.xml)；[源码manifest来源](../../tools/bolt/results/qb-meta-switch-20261028/unified-source-provenance.json)。

Unified的packages里没有clang、gcc、glibc、bash、llvm、coreutils，并不是包含Base全部包的聚合仓库。它实际需要“Unified + Base”两层。把Unified-Toolchain的latest/reference/base全改为Unified，只能给默认来源一个地址；两个项目目录没有现成的显式第二层DOD定义可照搬。本轮**不能确认QB会据build.xml递归创建Base DOD**，也不能把Tools项目的自定义DOD先例直接当作Unified默认加载器已支持多层的证据。

### 3.1 最近的已有QB 1209720

已由用户在headed Chromium中手动登录，只读取概览和Save日志下载链接。[概览](../../tools/bolt/results/qb-meta-switch-20261028/qb/1209720-overview.txt)；[截图](../../tools/bolt/results/qb-meta-switch-20261028/qb/1209720-overview.png)；[日志来源/SHA](../../tools/bolt/results/qb-meta-switch-20261028/qb/provenance.json)。1209720为Successful，开始2026-10-27 06:36:18，耗时5:53:55；ARMv7/AArch64/x86子构建1209725/1209726/1209727均成功。

x86子日志原文：

```text
1209727 L316: repo_url : standard http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261026.051209/repos/standard
1209727 L333: buildconf=./build.conf
1209727 L334: repos = repo.base_0,repo.base_debug_0
1209727 L350: ----start get_build_conf_text-----------------------------------
1209727 L351: repo_url : standard http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261026.051209/repos/standard
1209727 L432: timeout 8h gbs build --threads=30 --define "jobs 8" --define "_smp_mflags -j8" --define "_costomized_smp_mflags -j20" --baselibs --clean-once --style=tar
```

这是GBS，不是1211018的NGBS；四份完整日志中`dod create project`出现次数为0。必须报告“没有DOD创建命令”，不能编造该轮创建了DOD:Unified或DOD:Base。[计数及行号](../../tools/bolt/results/qb-meta-switch-20261028/qb/mechanism-summary.json)。三子日志实际构建清单都是1046仓库，名字集合与当前Unified-Toolchain manifest相同；具体revision保存在每份packages.json，不能仅凭名称相同声称提交相同。

因此第二评审在“证明第二层DOD会被创建”处停止。没有编造project_meta path、meta-dod文件名/机制，也没有新建一个未经认证的本地提交。以下是已经取得的只读可行性初查，完整spec依赖认证没有继续。

## 4. Unified：源码和二进制缺失初查

### 4.1 源码清单

当前Toolchain manifest和最近QB均1046个仓库；新固定快照standard manifest为1030个。缺17、增加1（platform/upstream/fluoride），共同仓库267个revision变化。[完整新增/缺少/revision变更TSV](../../tools/bolt/results/qb-meta-switch-20261028/unified-repository-changes.tsv)；[与QB清单的比较](../../tools/bolt/results/qb-meta-switch-20261028/unified-fixed-source-comparison.json)。

元仓库当前Unified manifest另有两个emulator仓库，所以它是1032而非standard固定快照的1030；[两个项目manifest直接比较](../../tools/bolt/results/qb-meta-switch-20261028/unified-manifest-diff.json)保留这个区别，不拿元目录列表替代实际快照。

| 新standard来源缺少的现有仓库 | 判定 |
|---|---|
| platform/core/api/wifi | 未满足“现有包均有对应源码”要求；未授权删除/替换该目标 |
| platform/core/connectivity/bluetooth-tools | 未满足“现有包均有对应源码”要求；未授权删除/替换该目标 |
| platform/core/uifw/ise-default | 未满足“现有包均有对应源码”要求；未授权删除/替换该目标 |
| platform/core/uifw/ise-default-nui | 未满足“现有包均有对应源码”要求；未授权删除/替换该目标 |
| platform/core/uifw/libscl-ui-nui | 未满足“现有包均有对应源码”要求；未授权删除/替换该目标 |
| platform/upstream/clat | 未满足“现有包均有对应源码”要求；未授权删除/替换该目标 |
| platform/upstream/ctags | 未满足“现有包均有对应源码”要求；未授权删除/替换该目标 |
| profile/iot/apps/dotnet/oobe-ui | 未满足“现有包均有对应源码”要求；未授权删除/替换该目标 |
| profile/iot/apps/dotnet/setting-autofill | 未满足“现有包均有对应源码”要求；未授权删除/替换该目标 |
| profile/iot/apps/dotnet/setting-inputmethod | 未满足“现有包均有对应源码”要求；未授权删除/替换该目标 |
| profile/iot/apps/dotnet/settings | 未满足“现有包均有对应源码”要求；未授权删除/替换该目标 |
| profile/mobile/platform/core/uifw/autofill-config | 未满足“现有包均有对应源码”要求；未授权删除/替换该目标 |
| profile/mobile/platform/core/uifw/e-tizen-data | 未满足“现有包均有对应源码”要求；未授权删除/替换该目标 |
| profile/mobile/platform/core/uifw/isf-config | 未满足“现有包均有对应源码”要求；未授权删除/替换该目标 |
| profile/tv/platform/core/uifw/autofill-config | 未满足“现有包均有对应源码”要求；未授权删除/替换该目标 |
| profile/tv/platform/core/uifw/e-tizen-data | 未满足“现有包均有对应源码”要求；未授权删除/替换该目标 |
| profile/tv/platform/core/uifw/isf-config | 未满足“现有包均有对应源码”要求；未授权删除/替换该目标 |

### 4.2 二进制包（含noarch）

旧对照是Unified-Toolchain reference `20261016.052151`的standard仓库；新为Unified `20261027.231956`，并额外计算“假如Base第二层可用”的乐观联合结果。**联合计算不表示第二层DOD配置已经实现**。此处不把旧Base层的包重复算进Unified自己的仓库差异。

| 架构 | 新Unified单层少的包名数 | 新Unified+Base联合仍少的包名数 | 旧RPM Requires命中行数 |
|---|---:|---:|---:|
| x86_64 | 116 | 115 | 60 |
| armv7l | 116 | 115 | 62 |
| aarch64 | 115 | 114 | 61 |

[完整缺包/版本限定Requires/替代provider](../../tools/bolt/results/qb-meta-switch-20261028/unified-missing-dependencies.json)；[逐包三架构TSV](../../tools/bolt/results/qb-meta-switch-20261028/unified-missing-packages.tsv)。例如旧`app-rootstrap-native-data-internal`要求`lightweight-web-engine-profile_mobile`，新联合仓库无该能力provider；building-blocks相关包还引用autofill-config-mobile等。它们是旧RPM的实际requires证据，不是已证明新spec仍保留同样依赖；完整1046仓库spec检查因前置停止条件未执行，标为NOT RUN。

缺包名逐项如下；若有另名包提供旧名字，仅列出候选，未宣称满足所有版本限定和文件能力：

| 缺少包名 | x86 / ARMv7 / AArch64 | 新联合仓库提供旧名字的其他包 |
|---|---|---|
| autofill-config-mobile | 缺/缺/缺 | 无 |
| autofill-config-tv | 缺/缺/缺 | 无 |
| bluetooth-frwk-extension-TM1 | 非缺项/缺/非缺项 | 无 |
| bluetooth-frwk-profile_ivi | 缺/缺/缺 | 无 |
| bluetooth-frwk-profile_mobile | 缺/缺/缺 | 无 |
| bluetooth-frwk-profile_tv | 缺/缺/缺 | 无 |
| bluetooth-frwk-profile_wearable | 缺/缺/缺 | 无 |
| bluetooth-tools | 缺/缺/缺 | 无 |
| bluetooth-tools-no-firmware | 缺/缺/缺 | 无 |
| bluetooth-tools-profile_common | 缺/缺/缺 | 无 |
| bluetooth-tools-profile_ivi | 缺/缺/缺 | 无 |
| bluetooth-tools-profile_mobile | 缺/缺/缺 | 无 |
| bluetooth-tools-profile_wearable | 缺/缺/缺 | 无 |
| capi-network-wifi | 缺/缺/缺 | 无 |
| capi-network-wifi-devel | 缺/缺/缺 | 无 |
| capi-system-media-key-tcore | 缺/缺/缺 | 无 |
| chromium-efl-browser | 缺/非缺项/非缺项 | chromium-efl-browser |
| chromium-efl-upgrade-tpk | 缺/缺/缺 | 无 |
| clat | 缺/缺/缺 | 无 |
| com.samsung.dali-demo-resources_mobile | 缺/缺/缺 | com.samsung.dali-demo-resources_720x1280 |
| com.samsung.dali-demo-resources_rpi | 缺/缺/缺 | com.samsung.dali-demo-resources_1920x1080_rpi |
| dali2-adaptor-profile_common | 缺/缺/缺 | dali2-adaptor |
| dali2-adaptor-profile_mobile | 缺/缺/缺 | dali2-adaptor |
| dali2-adaptor-profile_tv | 缺/缺/缺 | dali2-adaptor |
| dali2-csharp-binder-profile_common | 缺/缺/缺 | dali2-csharp-binder |
| dali2-csharp-binder-profile_mobile | 缺/缺/缺 | dali2-csharp-binder |
| dali2-csharp-binder-profile_tv | 缺/缺/缺 | dali2-csharp-binder |
| dali2-toolkit-resources_360x360 | 缺/缺/缺 | 无 |
| e-tizen-data-profile_mobile | 缺/缺/缺 | 无 |
| e-tizen-data-profile_tv | 缺/缺/缺 | 无 |
| e20-test-harness | 缺/缺/缺 | 无 |
| efl-misc-profile_ivi | 缺/缺/缺 | 无 |
| efl-misc-profile_mobile | 缺/缺/缺 | 无 |
| efl-misc-profile_tv | 缺/缺/缺 | 无 |
| efl-misc-profile_wearable | 缺/缺/缺 | 无 |
| efl-modules-profile_ivi | 缺/缺/缺 | 无 |
| efl-modules-profile_mobile | 缺/缺/缺 | 无 |
| ise-default | 缺/缺/缺 | 无 |
| ise-default-config | 缺/缺/缺 | 无 |
| ise-default-profile_common | 缺/缺/缺 | 无 |
| ise-default-profile_ivi | 缺/缺/缺 | 无 |
| ise-default-profile_mobile | 缺/缺/缺 | 无 |
| ise-default-profile_tv | 缺/缺/缺 | 无 |
| isf-config-mobile | 缺/缺/缺 | 无 |
| isf-config-tv | 缺/缺/缺 | 无 |
| libds-tizen-blender | 缺/缺/缺 | 无 |
| libds-tizen-blender-devel | 缺/缺/缺 | 无 |
| libds-tizen-blur | 缺/缺/缺 | 无 |
| libds-tizen-blur-devel | 缺/缺/缺 | 无 |
| libds-tizen-clipboard | 缺/缺/缺 | 无 |
| libds-tizen-clipboard-devel | 缺/缺/缺 | 无 |
| libds-tizen-display-policy | 缺/缺/缺 | 无 |
| libds-tizen-display-policy-devel | 缺/缺/缺 | 无 |
| libds-tizen-dpms | 缺/缺/缺 | 无 |
| libds-tizen-dpms-devel | 缺/缺/缺 | 无 |
| libds-tizen-embedded-compositor | 缺/缺/缺 | 无 |
| libds-tizen-embedded-compositor-devel | 缺/缺/缺 | 无 |
| libds-tizen-explicit-sync | 缺/缺/缺 | 无 |
| libds-tizen-explicit-sync-devel | 缺/缺/缺 | 无 |
| libds-tizen-gbm-server | 缺/缺/缺 | 无 |
| libds-tizen-gbm-server-devel | 缺/缺/缺 | 无 |
| libds-tizen-hwc | 缺/缺/缺 | 无 |
| libds-tizen-hwc-devel | 缺/缺/缺 | 无 |
| libds-tizen-indicator | 缺/缺/缺 | 无 |
| libds-tizen-indicator-devel | 缺/缺/缺 | 无 |
| libds-tizen-input-devicemgr | 缺/缺/缺 | 无 |
| libds-tizen-input-devicemgr-devel | 缺/缺/缺 | 无 |
| libds-tizen-input-method | 缺/缺/缺 | 无 |
| libds-tizen-input-method-devel | 缺/缺/缺 | 无 |
| libds-tizen-keyrouter | 缺/缺/缺 | 无 |
| libds-tizen-keyrouter-devel | 缺/缺/缺 | 无 |
| libds-tizen-launch | 缺/缺/缺 | 无 |
| libds-tizen-launch-devel | 缺/缺/缺 | 无 |
| libds-tizen-memory-flusher | 缺/缺/缺 | 无 |
| libds-tizen-memory-flusher-devel | 缺/缺/缺 | 无 |
| libds-tizen-policy | 缺/缺/缺 | 无 |
| libds-tizen-policy-devel | 缺/缺/缺 | 无 |
| libds-tizen-remote-surface | 缺/缺/缺 | 无 |
| libds-tizen-remote-surface-devel | 缺/缺/缺 | 无 |
| libds-tizen-renderer | 缺/缺/缺 | 无 |
| libds-tizen-renderer-devel | 缺/缺/缺 | 无 |
| libds-tizen-scaler | 缺/缺/缺 | 无 |
| libds-tizen-scaler-devel | 缺/缺/缺 | 无 |
| libds-tizen-screen | 缺/缺/缺 | 无 |
| libds-tizen-screen-devel | 缺/缺/缺 | 无 |
| libds-tizen-screen-rotation | 缺/缺/缺 | 无 |
| libds-tizen-screen-rotation-devel | 缺/缺/缺 | 无 |
| libds-tizen-screenshooter | 缺/缺/缺 | 无 |
| libds-tizen-screenshooter-devel | 缺/缺/缺 | 无 |
| libds-tizen-surface-exporter | 缺/缺/缺 | 无 |
| libds-tizen-surface-exporter-devel | 缺/缺/缺 | 无 |
| libds-tizen-tbm-server | 缺/缺/缺 | 无 |
| libds-tizen-tbm-server-devel | 缺/缺/缺 | 无 |
| libds-tizen-text-input | 缺/缺/缺 | 无 |
| libds-tizen-text-input-devel | 缺/缺/缺 | 无 |
| libds-tizen-video | 缺/缺/缺 | 无 |
| libds-tizen-video-devel | 缺/缺/缺 | 无 |
| libscl-ui-nui | 缺/缺/缺 | 无 |
| libscl-ui-nui-devel | 缺/缺/缺 | 无 |
| lightweight-web-engine-profile_mobile | 缺/缺/缺 | 无 |
| lightweight-web-engine-profile_wearable | 缺/缺/缺 | 无 |
| org.tizen.cssetting-autofill | 缺/缺/缺 | 无 |
| org.tizen.cssetting-inputmethod | 缺/缺/缺 | 无 |
| org.tizen.cssettings | 缺/缺/缺 | 无 |
| org.tizen.inputdelegator-profile_common | 缺/缺/缺 | 无 |
| org.tizen.ise-default-nui | 缺/缺/缺 | 无 |
| org.tizen.oobe | 缺/缺/缺 | 无 |
| security-config-profile_iot_headed | 缺/缺/缺 | 无 |
| security-config-profile_iot_headless | 缺/缺/缺 | 无 |
| security-config-profile_mobile | 缺/缺/缺 | 无 |
| security-config-profile_wearable | 缺/缺/缺 | 无 |
| security-privilege-manager-extension-iot | 缺/缺/缺 | 无 |
| security-privilege-manager-extension-mobile | 缺/缺/缺 | 无 |
| security-privilege-manager-extension-wearable | 缺/缺/缺 | 无 |
| svi-data-profile_mobile | 缺/缺/缺 | 无 |
| svi-data-profile_wearable | 缺/缺/缺 | 无 |

### 4.3 Unified自身project_config

`project_config`原文SHA为`a5abe9c7a6dcf2909799e6bbc6cca6349c2fe94d9cf74132db74eebc30f34086`，一个字未改。它自身没有regalloc-enable-advisor/enable-ml-inliner参数，故条件性的Unified单独MLGO测试不适用；如果继承Base-Toolchain的宏，最终宏装配仍要首次QB核实，新Base clang已通过第2.2节显式参数测试。

临时解析输入仅在本轮结果脚本工作区加`_repository=standard`前导，让条件分支按标准仓库展开，没有修改原project_config。该文件自身点名项主要是Substitute；[所有provider结果](../../tools/bolt/results/qb-meta-switch-20261028/unified-config-providers.tsv)显示`Substitute: pkgconfig(gles11) pkgconfig(egl) pkgconfig(glesv1) pkgconfig(gl)`（L52）的最后一项在三架构新联合仓库均无provider，其他RHS有。该替换只有触发gles11依赖时才生效，不等于每个包必然失败；但本轮不能满足“每个点名项都有provider”的严格上传检查。

## 5. 后续需要用户/总部决定的事项

1. Base：明确gcc-armv7hl是否继续在Toolchain目标中、binutils-armv7hl从哪里提供；不能仅修DOD后忽略这个命中。历史Keep/未触发Substitute项是否允许例外，需要明确裁决，本轮没有改动它们。
2. Unified：先说明17个源码目标的保留/替代策略，以及Unified+Base两层依赖如何被QB真正创建。当前两个项目自己的配置没有可照搬的第二层显式DOD定义；需要加载器实现或已有两层项目的实际生成日志，不能猜。
3. 缺包分类和目标范围明确后，再对新来源实际spec做完整BuildRequires/Requires与版本/Provides求解；不能用旧二进制requires或小C编译替代。
4. 条件全部满足后，两个提交应分别基于当时最新master；仅推各自refs/for/master、不加reviewer。本轮没有获得通过状态，所以没有执行这些步骤。
5. 合入后首次QB必须保留最终project_config/_config/.rpmmacros及编译器/flags原文，确认使用Toolchain自己的条件；总部意图已经确认，实际加载结果仍挂账。

## 6. 证据完整性和执行边界

[证据SHA256SUMS](../../tools/bolt/results/qb-meta-switch-20261028/SHA256SUMS)覆盖本目录材料；公开RPM体积较大，仅在本轮temp保留，GitHub保存其下载URL、原始大小/校验值、运行输出。父/子QB完整日志用gzip保存；浏览器只保存登录后的概览文本/截图和下载日志，没有保存cookie、认证头或登录表单。

查找更正：QB下载入口标题是Save而非Download，按页面实际链接纠正后只读下载；依赖扫描补上宏包装内BuildRequires；debug/<arch>/初探404后检查父目录，确认实际采用平铺RPM布局，未将该404误报为快照缺少debug。全部原始输入/发布代码/项目配置未改，未删除目录，未运行cmake/ninja或软件包构建，未推Gerrit、master或sandbox。第一本地修复仍是fd60db96；两个评审均STOP/未上传。


## 7. 用户裁决后的处理（2026-10-28）

**两个评审本轮仍未上传，但停止依据已收窄。** Base 的 gcc-armv7hl 确实进入了 QB 调度和依赖计算，不能按“只编 gcc.spec”豁免；Keep/Substitute 的历史缺项则全部解除阻断。Unified 的依赖仓库和 build.conf 实际来自 Base-Toolchain，但日志不足以排除代码清单来自 meta/manifest.xml，因此按“看不出来就停”的裁决，不修改 snapshot_info、不上传。

本节追加于原第1–6节之后；前文是上一轮的历史结论，未改写。本轮 Unified 的目标已变为“Unified 代码 + 原 Base-Toolchain 依赖”；上一轮两层 DOD 和二进制缺包检查不再作为此方案的阻断。17个仓库的删除也不直接判失败；只有通过来源机制检查后，才进入剩余1030仓库的 BuildRequires 认证。

### 7.1 Base：不是只选 gcc.spec / binutils.spec

对两份完整子日志重新逐行检索，并与45号的实际仓库清单核对：

| 仓库 | 1202084 与 1211018 实际 revision | 对应实际源码包/spec |
|---|---|---|
| platform/upstream/gcc | `49c5060508ce8a6ed6beca375233688a6bdd9140` | gcc、gcc-aarch64、gcc-armv7l、gcc-armv7hl、gcc-riscv64；各有同名.spec |
| platform/upstream/binutils | `518d2e0089ccf79dd8de973276207d3aa638df11` | binutils、binutils-aarch64、binutils-armv7l、binutils-armv7hl、binutils-riscv64；各有同名.spec |

原始仓库映射：两份日志的 L136/L278/L417；1211018 另有 L5737。见本节证据目录的 `1202084-repo-entries.json` 和 `1211018-repo-entries.json`。251是源码仓库数量，**不是spec或源码包数量**；一个仓库可以导出多份spec。

1211018 原文（`1211018-cross-spec.txt`保留每一组完整上下文）：

```text
L888: 05:22:37,293 INFO  - check package binutils-armv7hl
L889: 05:22:37,293 INFO  - <package name="binutils-armv7hl" project="Tizen-Base-Toolchain" />
L893: 05:22:37,293 INFO  - {'name': 'binutils-armv7hl.spec', 'md5': '', 'status': 'A'}
L985: 05:22:46,750 INFO  - check package gcc
L994: 05:22:46,750 INFO  - {'name': 'gcc.spec', 'md5': '', 'status': 'A'}
L4884: 05:24:25,723 INFO  - check package gcc-armv7hl
L4885: 05:24:25,723 INFO  - <package name="gcc-armv7hl" project="Tizen-Base-Toolchain" />
L4889: 05:24:25,723 INFO  - {'name': 'gcc-armv7hl.spec', 'md5': '', 'status': 'A'}
```

这里不能把“包目录里有一个spec”单独当成运行证据。决定性的补充是1202084 **实际调度器**的状态与依赖原文：

```text
L1106: 07:29:38,438 INFO  - check package gcc-armv7hl
L1107: 07:29:38,438 INFO  - info: gcc-armv7hl No files were changed.
L1345: 08:00:20,359 INFO  - 	 binutils-armv7hl blocked
L1425: 08:00:20,360 INFO  - 	 gcc-armv7hl blocked
L1426: 08:00:20,360 INFO  - 		bison, flex, makeinfo, gcc-c++, zlib-devel, xz-devel, perl, binutils-armv7hl, binutils, glibc, ...
```

日志没有给出完整的 `rpmbuild ... gcc-armv7hl.spec` 命令，也不能声称它已成功编完；但它明确是 **纳入构建并计算了 binutils-armv7hl 依赖的目标**，而非被忽略的附带文件。45号已保存的 `gcc-armv7hl.spec` L1 `%define cross armv7hl`、L101 `%{?cross:BuildRequires: binutils-%{cross}}` 与上述调度结果互证。因此本轮命中“QB会编它”的停止条件，**不rebase、不上传Base评审**。没有擅自用“项目内也计划构建binutils-armv7hl”放宽用户规定的缺包门禁。

旧快照 `tizen-base-toolchain_20261013.024319` 的 x86_64 primary 元数据原始 release 核对：

| 包 | version-release | source RPM |
|---|---|---|
| gcc | 14.2.0-1.13 | gcc-14.2.0-1.13.src.rpm |
| gcc-armv7hl | 14.2.0-1.3 | gcc-armv7hl-14.2.0-1.3.src.rpm |
| binutils | 2.43-1.14 | binutils-2.43-1.14.src.rpm |
| binutils-armv7hl | 2.43-1.1 | binutils-armv7hl-2.43-1.1.src.rpm |

用户给出的cross release号与二进制仓库一致；45号提取的 `gcc-armv7hl-14.2.0-1.4/` 是 source 索引中另一份保留SRPM，不能用目录名代替本表的二进制release，也不能凭release较老推断QB不编它。`old-release-comparison.json`另列三架构的location、source、VCS和包校验值。

### 7.2 Base：历史 Keep / Substitute 缺项豁免

从原始primary解析结果重新计算提供者，按目标架构+noarch匹配包名、Provides和文件提供；没有只复述上一轮的结论。合计 **56个“架构×指令×名字”缺项，旧仓库提供者也是空，新增退化0项**：Keep为11名字×3架构=33项，Substitute为23项。本次全部按用户裁决豁免，不再阻断。每项的配置行号及旧/新提供者 `[]` 见 `provider-waivers.tsv/json`；输入primary解析文件的SHA和可复跑脚本也一并保存。

| 指令 | 名字 | 缺失的目标架构 | 旧提供者 | 新提供者 | 裁决 |
|---|---|---|---|---|---|
| keep | `glib2` | x86_64, armv7l, aarch64 | 无 | 无 | 原有缺项，豁免 |
| keep | `libada` | x86_64, armv7l, aarch64 | 无 | 无 | 原有缺项，豁免 |
| keep | `libcloog` | x86_64, armv7l, aarch64 | 无 | 无 | 原有缺项，豁免 |
| keep | `libmpc` | x86_64, armv7l, aarch64 | 无 | 无 | 原有缺项，豁免 |
| keep | `libmpfr` | x86_64, armv7l, aarch64 | 无 | 无 | 原有缺项，豁免 |
| keep | `libppl` | x86_64, armv7l, aarch64 | 无 | 无 | 原有缺项，豁免 |
| keep | `libppl_c` | x86_64, armv7l, aarch64 | 无 | 无 | 原有缺项，豁免 |
| keep | `nss-softokn-freebl` | x86_64, armv7l, aarch64 | 无 | 无 | 原有缺项，豁免 |
| keep | `perl-libs` | x86_64, armv7l, aarch64 | 无 | 无 | 原有缺项，豁免 |
| keep | `tizen-rpm-config` | x86_64, armv7l, aarch64 | 无 | 无 | 原有缺项，豁免 |
| keep | `xz-lzma-compat` | x86_64, armv7l, aarch64 | 无 | 无 | 原有缺项，豁免 |
| substitute | `clang-accel-x86_64-aarch64` | x86_64, armv7l | 无 | 无 | 原有缺项，豁免 |
| substitute | `clang-accel-x86_64-armv7hl` | x86_64, armv7l, aarch64 | 无 | 无 | 原有缺项，豁免 |
| substitute | `clang-accel-x86_64-armv7l` | x86_64, aarch64 | 无 | 无 | 原有缺项，豁免 |
| substitute | `clang-accel-x86_64-riscv64` | x86_64, armv7l, aarch64 | 无 | 无 | 原有缺项，豁免 |
| substitute | `glibc-32bit` | x86_64 | 无 | 无 | 原有缺项，豁免 |
| substitute | `glibc-devel-32bit` | x86_64 | 无 | 无 | 原有缺项，豁免 |
| substitute | `libgcc-32bit` | x86_64 | 无 | 无 | 原有缺项，豁免 |
| substitute | `python-accel-x86_64-aarch64` | x86_64, armv7l | 无 | 无 | 原有缺项，豁免 |
| substitute | `python-accel-x86_64-armv7hl` | x86_64, armv7l, aarch64 | 无 | 无 | 原有缺项，豁免 |
| substitute | `python-accel-x86_64-armv7l` | x86_64, aarch64 | 无 | 无 | 原有缺项，豁免 |
| substitute | `python-accel-x86_64-riscv64` | x86_64, armv7l, aarch64 | 无 | 无 | 原有缺项，豁免 |

这些“无”严格按同架构/noarch判断。例如带目标名的accel包在另一架构仓库存在，不意味着在x86_64仓库也有provider；旧、新按同一规则比较。其余Preinstall、Runscripts、Required、Support、VMinstall检查沿用第2节的通过结果；MLGO旧/新clang两目标4/4通过也保持不变。

### 7.3 Unified：机制实证与不能跨过的证据缺口

读取1209720父日志、1209725/26/27三个子日志和1211018完整日志，没有重新登录或操作QB。

| 项目 | 1209720 / x86子构建1209727 | 1211018 |
|---|---|---|
| 构建方式 | 子L432 `timeout 8h gbs build --threads=30 ...` | L400 `USE_NGBS=yes`；L509 NGBS入口 |
| 代码参考标记 | 父L1162–1164 `BUILD_REFERENCE: Ref. Snapshot`；L3915 snapshot_num_url=Unified-Toolchain/20261016.052151 | L130/L314 snapshot_num_url=Base/20261026.005418 |
| 已解析清单 | 父L1290 MANIFEST_ORIG、L2339 MANIFEST_REF；L3921 build_pkg_list_dic共1046仓库；父L3932 `do_src_sync` | L136等四处共251仓库，已解析完成 |
| 依赖URL | 子L317 base_path_url=Base-Toolchain/20261026.051209/repos/standard；L334启用repo.base_0、repo.base_debug_0；L339/L342分别packages/debug | L314 base_path_url=Base/20261026.005418；L331启用base两仓库，L336/L339为packages/debug |
| build.conf来源 | 子L350–352 `get_build_conf_text`读取上述Base-Toolchain的`packages/repodata/`；L333 `buildconf=./build.conf` | L347–350同函数取Base/reference，解析为20261026.005418 |
| 项目自身project_config | 父L3424打印PROJECT_CONFIG，L3427标题为Unified-Toolchain，L3434 FileProvides、L3435 Prefer、L3439 _with_tizen等 | L432从Toolchain元目录生成NGBS build_meta；没有最终宏文本 |

关键原文（保存为 `1209727-mechanism.txt`）：

```text
L317: 06:47:51,954 INFO  - After converting, snapshot_num_url : http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20261016.052151, base_path_url : standard http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261026.051209/repos/standard, unified_path_url : , common_path_url :
L333: 06:47:51,954 INFO  - buildconf=./build.conf
L334: 06:47:51,954 INFO  - repos = repo.base_0,repo.base_debug_0
L350: 06:47:51,954 INFO  - ----start get_build_conf_text-----------------------------------
L351: 06:47:51,954 INFO  - repo_url : standard http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261026.051209/repos/standard
L352: 06:47:51,954 INFO  - repodata_url inside get_build_conf_text: http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261026.051209/repos/standard/packages/repodata/
```

**已证实**：本次GBS的依赖和get_build_conf_text输入均使用base_path_url，实际是Base-Toolchain；code snapshot_num_url与base_path_url分开。自身PROJECT_CONFIG确实已经传入父任务变量，但**没有看到它被拼接到最终build.conf的命令、大小或最终展开文本**，所以不能把变量存在写成已应用。当前metadata的base固定号为20261013.140248，本次QB实际为20261026.051209；这里记录实值，不把当前XML冒充历史执行值。

**来源歧义的逐项复核**（`manifest-ambiguity.json`）：

- 父日志 MANIFEST_ORIG、MANIFEST_REF 都有1046个仓库/revision，均与固定参考快照standard.xml完全一致。
- 父日志最终build_pkg_list_dic与参考快照一致1045项；唯一差异linux-rpi正是L1156用户显式替换的revision。
- 但是，scm/meta/qb 的 `Tizen-Unified-Toolchain/manifest.xml` 也给出**完全相同的1046个仓库/revision**；对最终build_pkg_list_dic也是相同1045项+同一用户替换。
- 父日志L6280–6281明确打印 `Manifest_URL` / `Not Defined (Manifest_URL)`。这不代表QB没有读取manifest，只说明该日志字段没有提供URL。
- 全文没有snapshot_info加载记录或manifest下载URL；`MANIFEST_ORIG/REF`已经是解析后的值，未显示从snapshot XML还是meta/manifest.xml取值。检索式、命中行和输入SHA保存在 `mechanism-search.json`、`input-sha256.json`。

因此，“代码从reference取、只改snapshot_info就会切换全部代码”**与现有日志相容，但仍只是推断，不能排除meta/manifest.xml的来源**。这两份manifest恰好相同，无法用内容匹配消除歧义。按用户明示“看不出来就不要改、停下报告”，Unified在机制检查处停止；没有进入1030仓库BuildRequires认证，也没有修改latest/reference/base或任何其他项目文件。

下一步所缺的是QB在解析 `MANIFEST_REF/ORIG` 之前的读取日志或对应加载器代码，能明确给出来源URL/文件及字段映射；以及最终build.conf合并证据。未自行获取内部脚本、改变QB设置或触发构建来补证。17少1增的清单、267个共同仓库revision变化仍保留在第3节及原证据中，本轮没有把“未检查剩余依赖”写成通过。

### 7.4 最终diff、上传状态与边界

| 评审 | 本轮判定 | 本地改动 / 最终diff | Gerrit |
|---|---|---|---|
| Base-Toolchain / Base-Dev | STOP：cross GCC的依赖真实进入调度 | fd60db96806a372404bd4f04e68d4ba586290147原样保留，原两行DOD修复见第1节和`base-existing.diff`；本轮新增diff为空，未rebase | 未上传，无change URL |
| Unified-Toolchain | STOP：无法确认manifest源选择机制 | 新增diff为空；snapshot_info、project_meta/config、manifest、candidate_snapshot、project_env均未改；未创建提交 | 未上传，无change URL |

两项检查均未满足上传条件，因此没有执行fetch/rebase/commit/push到Gerrit，也没有访问QB做状态操作。scm/meta/qb工作区仍干净，HEAD仍fd60db96；提交说明及Change-Id保持不变。本轮只提交证据与本文/STATUS到GitHub bolt-v4。合入后首次QB核实最终编译配置的挂账继续保留。

新增证据索引：

- [可复跑离线审计脚本](../../tools/bolt/results/qb-meta-switch-20261028/user-ruling/audit.py)
- [1202084 cross目标及依赖原文](../../tools/bolt/results/qb-meta-switch-20261028/user-ruling/1202084-cross-spec.txt)
- [1211018全部GCC/binutils源码包导入原文](../../tools/bolt/results/qb-meta-switch-20261028/user-ruling/1211018-cross-spec.txt)
- [56项旧/新provider逐项豁免](../../tools/bolt/results/qb-meta-switch-20261028/user-ruling/provider-waivers.tsv)
- [旧包release与VCS](../../tools/bolt/results/qb-meta-switch-20261028/user-ruling/old-release-comparison.json)
- [Unified父日志机制原文](../../tools/bolt/results/qb-meta-switch-20261028/user-ruling/1209720-mechanism.txt)、[GBS子日志](../../tools/bolt/results/qb-meta-switch-20261028/user-ruling/1209727-mechanism.txt)、[NGBS对照](../../tools/bolt/results/qb-meta-switch-20261028/user-ruling/1211018-mechanism.txt)
- [manifest内容歧义检查](../../tools/bolt/results/qb-meta-switch-20261028/user-ruling/manifest-ambiguity.json)、[全文检索](../../tools/bolt/results/qb-meta-switch-20261028/user-ruling/mechanism-search.json)
- [输入SHA](../../tools/bolt/results/qb-meta-switch-20261028/user-ruling/input-sha256.json)、[输出SHA](../../tools/bolt/results/qb-meta-switch-20261028/user-ruling/SHA256SUMS)


## 8. 第二次裁决后的处理（2026-10-28任务续跑）

**两个评审均已上传，未推master、未加reviewer。** Base缺失的binutils-armv7hl可由本项目同revision的binutils仓库自产，按新裁决不再阻断。Unified已确认代码来自快照而不是meta manifest；全部1030仓库的依赖检查通过，改动仅为latest/reference两行，建议等Base-Toolchain的新快照和相应依赖引用更新就绪后再合入。

| 评审 | 提交 | Gerrit | 判定 |
|---|---|---|---|
| Base-Toolchain / Base-Dev DOD | `ffba0ca45811e6ee70f95f527ae47b958431c20d` | [359363](https://review.tizen.org/gerrit/c/scm/meta/qb/+/359363) | PASS，已上传 |
| Unified-Toolchain代码来源 | `12f22a9c3cd1262f91a798d8f6439f6e3835ad31` | [359364](https://review.tizen.org/gerrit/c/scm/meta/qb/+/359364) | PASS，已上传 |

两提交都独立基于当时最新master `7b2f2ae2d0e0cdc42307454c73c10be23b6d0ef5`。前第1–7节未改；本节取代第7节两个停止判定。project_config是否最终附加到构建宏链的实物核对仍待合入后首次QB，不能把本次静态审查写成QB已验证。

### 8.1 Base：依赖仓库或项目自产包均可满足

用户裁决：不能以“QB会编gcc-armv7hl”直接停止，应该检查它的依赖有没有提供者。第7节已经保存的证据现在按这个标准解释：

```text
1211018 L888: 05:22:37,293 INFO  - check package binutils-armv7hl
1211018 L889: 05:22:37,293 INFO  - <package name="binutils-armv7hl" project="Tizen-Base-Toolchain" />
1211018 L893: 05:22:37,293 INFO  - {'name': 'binutils-armv7hl.spec', 'md5': '', 'status': 'A'}
1202084 L650: 07:29:04,101 INFO  - check package binutils-armv7hl
1202084 L651: 07:29:04,101 INFO  - info: binutils-armv7hl No files were changed.
1202084 L1345: 08:00:20,359 INFO  - 	 binutils-armv7hl blocked
1202084 L1426: 08:00:20,360 INFO  - 		bison, flex, makeinfo, gcc-c++, zlib-devel, xz-devel, perl, binutils-armv7hl, binutils, glibc, ...
```

两份实际仓库清单的binutils revision均为`518d2e0089ccf79dd8de973276207d3aa638df11`，新清单导入了`binutils-armv7hl.spec`。所以gcc-armv7hl的依赖有**项目内的自产提供者**；不能把依赖仓库里没这个RPM等同于闭包缺失，也没有声称被blocked的包当时已经编完。

其余10个包沿用第2节对251实际仓库spec的检查，没有命中待构建spec的依赖：

| Base中缺少的包 | 本次处理 |
|---|---|
| `gcc-armv7hl` | 已有spec检查无命中，不阻断 |
| `libtensorflow2-aot-runtime` | 已有spec检查无命中，不阻断 |
| `tensorflow2-aot-devel` | 已有spec检查无命中，不阻断 |
| `tensorflow2-lite-devel` | 已有spec检查无命中，不阻断 |
| `tensorflow2-lite-flatbuf-schema` | 已有spec检查无命中，不阻断 |
| `tensorflow2-lite-util` | 已有spec检查无命中，不阻断 |
| `toybox-full` | 已有spec检查无命中，不阻断 |
| `toybox-symlinks-full` | 已有spec检查无命中，不阻断 |
| `toybox-symlinks-nslookup` | 已有spec检查无命中，不阻断 |
| `coreutils-su` | 已有spec检查无命中，不阻断 |

原始二进制Requires中移除包彼此的依赖，不等于当前251源码仓库会编spec的BuildRequires；本轮没有把它们混用。Keep/Substitute共56个旧有缺项继续按第7.2节豁免，MLGO四项小编译既有PASS结果沿用。

fd60db96 rebase到master时无冲突。机器核对：提交说明逐字节不变，父提交为master，提交diff与原来的两行diff逐字节相同；两个XML合法。作者和提交者为Hao Lin，Change-Id仍为`Ib11994fc5745de18f0feefb4c83e6fab64d9633e`。最终diff：

```diff
diff --git a/TIZEN/Tizen/Tizen-Base-Dev/project_meta b/TIZEN/Tizen/Tizen-Base-Dev/project_meta
index 12d2f34..774c1b3 100644
--- a/TIZEN/Tizen/Tizen-Base-Dev/project_meta
+++ b/TIZEN/Tizen/Tizen-Base-Dev/project_meta
@@ -3,7 +3,7 @@
     <enable/>
   </debuginfo>
   <repository name="standard">
-    <path project="DOD:Tizen-Base" repository="standard" />
+    <path project="DOD:Tizen-Base-Dev" repository="standard" />
     <arch name="armv7l"/>
     <arch name="aarch64"/>
     <arch name="x86_64"/>
diff --git a/TIZEN/Tizen/Tizen-Base-Toolchain/project_meta b/TIZEN/Tizen/Tizen-Base-Toolchain/project_meta
index 7fed9ad..2dcffed 100644
--- a/TIZEN/Tizen/Tizen-Base-Toolchain/project_meta
+++ b/TIZEN/Tizen/Tizen-Base-Toolchain/project_meta
@@ -3,7 +3,7 @@
     <enable/>
   </debuginfo>
   <repository name="standard">
-    <path project="DOD:Tizen-Base" repository="standard" />
+    <path project="DOD:Tizen-Base-Toolchain" repository="standard" />
     <arch name="armv7l"/>
     <arch name="aarch64"/>
     <arch name="x86_64"/>
```

推送命令：

```sh
git push origin ffba0ca45811e6ee70f95f527ae47b958431c20d:refs/for/master
```

[完整推送输出](../../tools/bolt/results/qb-meta-switch-20261028/second-ruling/base-push.txt)保留原文；Gerrit返回SUCCESS及359363链接，并提示`warning: subject >50 characters; use shorter first paragraph`。按用户要求保留原提交说明，没有为了消除警告修改标题。只读Gerrit query复核状态NEW、分支master、patch set为上述SHA，见[查询原文](../../tools/bolt/results/qb-meta-switch-20261028/second-ruling/base-gerrit-query.jsonl)。

### 8.2 Unified：用Base实例区分manifest来源

`3c78318b`完整diff只涉及Base-Toolchain和Base-Dev各自的project_meta、snapshot_info，共4文件；没有修改Base-Toolchain的manifest.xml。[原文diff](../../tools/bolt/results/qb-meta-switch-20261028/second-ruling/3c78318b.diff)。该manifest前后均245仓库：

| 版本 | SHA256 | Git blob OID |
|---|---|---|
| 3c78318b^ | `9effc3e3d218eeca78d9a97acd3593a4bfd73753a6ffd50e8364438288eb273f` | `75a9167862c127f584e51811e74373237c9e5418` |
| 3c78318b | `9effc3e3d218eeca78d9a97acd3593a4bfd73753a6ffd50e8364438288eb273f` | `75a9167862c127f584e51811e74373237c9e5418` |

1211018 L136/L278/L417/L5737实际清单均251仓库；和meta相比，新增7、移除tensorflow2这1项、共同仓库revision变化18。逐项证据见[source-mechanism.json](../../tools/bolt/results/qb-meta-switch-20261028/second-ruling/source-mechanism.json)：

| 类型 | 仓库 | 与Base快照比较 |
|---|---|---|
| 新增 | `platform/upstream/abi-compliance-checker` | revision完全一致 |
| 新增 | `platform/upstream/abi-dumper` | revision完全一致 |
| 新增 | `platform/upstream/abi-tracker` | revision完全一致 |
| 新增 | `platform/upstream/abi-viewer` | revision完全一致 |
| 新增 | `platform/upstream/ctags` | revision完全一致 |
| 新增 | `platform/upstream/rfcdiff` | revision完全一致 |
| 新增 | `platform/upstream/vtable-dumper` | revision完全一致 |
| revision变化 | `platform/upstream/db4` | 一致 |
| revision变化 | `platform/upstream/glibc` | 一致 |
| revision变化 | `platform/upstream/libabigail` | 一致 |
| revision变化 | `platform/upstream/libtool` | 一致 |
| revision变化 | `platform/upstream/llvm` | 用户显式覆盖LLVM；不是快照revision |
| revision变化 | `platform/upstream/ncurses` | 一致 |
| revision变化 | `platform/upstream/openssl3` | 一致 |
| revision变化 | `platform/upstream/pam` | 一致 |
| revision变化 | `platform/upstream/qemu-accel` | 一致 |
| revision变化 | `platform/upstream/rpm` | 一致 |
| revision变化 | `platform/upstream/shadow-utils` | 一致 |
| revision变化 | `platform/upstream/toybox` | 一致 |
| revision变化 | `platform/upstream/tzdata` | 一致 |
| revision变化 | `product/upstream/coreutils` | 一致 |
| revision变化 | `product/upstream/findutils` | 一致 |
| revision变化 | `product/upstream/grep` | 一致 |
| revision变化 | `product/upstream/tar` | 一致 |
| revision变化 | `product/upstream/which` | 一致 |

不能把18个revision全写成快照版本：其中17个与Base快照相同，LLVM为用户指定的f308fe08，父1211014 L209/L363明确打印`platform/upstream/llvm@f308fe08eeaad4e219f8505449b88bd5f644ea8c`。最终251项目集合和Base快照完全一致，250个revision相同，唯一差异是这个显式覆盖；这是对用户给定结论的精确计数补充。[LLVM覆盖原文](../../tools/bolt/results/qb-meta-switch-20261028/second-ruling/1211014-llvm-override.txt)。

区别于第7节“两份manifest恰好相同”，这个实例的meta manifest与实际输入确实不同，排除了代码只来自meta manifest的解释。结合1209720/1209727的原文：

```text
1209720 L1164: 06:36:26,366 INFO  - Ref. Snapshot
1209720 L3915: 06:36:29,141 INFO  -                snapshot_num_url: http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20261016.052151
1209727 L317: 06:47:51,954 INFO  - After converting, snapshot_num_url : http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20261016.052151, base_path_url : standard http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261026.051209/repos/standard, unified_path_url : , common_path_url :
1209727 L334: 06:47:51,954 INFO  - repos = repo.base_0,repo.base_debug_0
1209727 L350: 06:47:51,954 INFO  - ----start get_build_conf_text-----------------------------------
1209727 L352: 06:47:51,954 INFO  - repodata_url inside get_build_conf_text: http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261026.051209/repos/standard/packages/repodata/
```

结论按用户本轮裁决执行：reference的snapshot_num_url选择代码清单；base_path_url选择依赖及基础build.conf。项目自身project_config保持不变；日志打印它作为变量存在，但最终拼接动作仍未直接读到，不据此宣称运行时宏装配已认证。

固定新快照`Tizen-Unified/tizen-unified_20261027.231956`的standard manifest本轮重新HTTP GET成功，HTTP 200、URL、大小、SHA见[snapshot-url-provenance.json](../../tools/bolt/results/qb-meta-switch-20261028/second-ruling/snapshot-url-provenance.json)。未用会变化的reference别名替代固定输入。

### 8.3 1030仓库BuildRequires闭包

从新固定manifest的**每个精确revision**以只读`git archive --remote=ssh://review.tizen.org:29418/<repo> <revision> packaging`取得spec，不执行包内脚本、不构建。4个并发网络读取，nice19/ionice3，工作归档只放本任务temp。覆盖结果：

| 检查 | 结果 |
|---|---|
| manifest仓库 / 成功获取 | 1030 / 1030 |
| spec文件 | 1034 |
| BuildRequires记录 | 9487 |
| 移除仓库 / 其包名、Provides和文件能力并集 | 17 / 134 |
| 对上述能力的BuildRequires命中 | 0 |
| 未展开依赖宏、外部include、动态BuildRequires入口 | 均0 |
| 只能由移除仓库满足的依赖 | 0，PASS |

保留条件分支（不因某个架构/开关关闭而漏扫），处理续行、BuildRequires标签及限定形式、spec内define/global和Name/Version/Release常量。也检查了整个spec中的能力名出现和外部include/动态依赖入口。全文件文本另有2处e-tizen-data命中，分别是仍保留的common仓库中的alias定义和Provides声明，均不是BuildRequires；原文另存removed-capability-text-hits.json。此为针对**17个移除仓库产出的静态依赖闭包检查**，不是宣称全部1030包在新旧工具链上都已编译成功。

提供者输入包括旧Unified-Toolchain包的VCS→仓库映射、包名/Provides/文件能力；可替代来源只包括新1030仓库自产包，以及当前snapshot_info实际指向的Base-Toolchain **20261013.140248**（三架构+noarch）。没有把旧分析用的20261013.024319冒充当前配置。由于最终对134能力的BuildRequires命中为0，没有需要靠忽略版本限定或猜测替代者放行的条目。

| 不再编的仓库 | 旧快照产出的包名 | 能力数 | BR命中 |
|---|---|---:|---:|
| `platform/core/api/wifi` | `capi-network-wifi`, `capi-network-wifi-devel` | 12 | 0 |
| `platform/core/connectivity/bluetooth-tools` | `bluetooth-tools`, `bluetooth-tools-no-firmware`, `bluetooth-tools-profile_common`, `bluetooth-tools-profile_ivi`, `bluetooth-tools-profile_mobile`, `bluetooth-tools-profile_wearable` | 26 | 0 |
| `platform/core/uifw/ise-default` | `ise-default`, `ise-default-config`, `ise-default-profile_common`, `ise-default-profile_ivi`, `ise-default-profile_mobile`, `ise-default-profile_tv` | 31 | 0 |
| `platform/core/uifw/ise-default-nui` | `org.tizen.ise-default-nui` | 4 | 0 |
| `platform/core/uifw/libscl-ui-nui` | `libscl-ui-nui`, `libscl-ui-nui-devel` | 14 | 0 |
| `platform/upstream/clat` | `clat` | 7 | 0 |
| `platform/upstream/ctags` | `ctags` | 7 | 0 |
| `profile/iot/apps/dotnet/oobe-ui` | `org.tizen.oobe` | 4 | 0 |
| `profile/iot/apps/dotnet/setting-autofill` | `org.tizen.cssetting-autofill` | 4 | 0 |
| `profile/iot/apps/dotnet/setting-inputmethod` | `org.tizen.cssetting-inputmethod` | 4 | 0 |
| `profile/iot/apps/dotnet/settings` | `org.tizen.cssettings` | 4 | 0 |
| `profile/mobile/platform/core/uifw/autofill-config` | `autofill-config-mobile` | 2 | 0 |
| `profile/mobile/platform/core/uifw/e-tizen-data` | `e-tizen-data-profile_mobile` | 8 | 0 |
| `profile/mobile/platform/core/uifw/isf-config` | `isf-config-mobile` | 3 | 0 |
| `profile/tv/platform/core/uifw/autofill-config` | `autofill-config-tv` | 2 | 0 |
| `profile/tv/platform/core/uifw/e-tizen-data` | `e-tizen-data-profile_tv` | 8 | 0 |
| `profile/tv/platform/core/uifw/isf-config` | `isf-config-tv` | 3 | 0 |

这17个仓库是固定Unified标准manifest已不包含的目标；新增1个为`platform/upstream/fluoride`。不将所有17个都泛称为profile仓库（其中也有wifi、clat、ctags等），也不把1030范围外的旧RPM当成新项目自产提供者。

逐仓库revision/spec来源与SHA见[spec-acquisition.json](../../tools/bolt/results/qb-meta-switch-20261028/second-ruling/spec-acquisition.json)，spec全文位于同目录specs/；[全部BR记录](../../tools/bolt/results/qb-meta-switch-20261028/second-ruling/buildrequires-lines.json)、[命中表](../../tools/bolt/results/qb-meta-switch-20261028/second-ruling/buildrequires-hits.json)、[移除仓库→产出→能力](../../tools/bolt/results/qb-meta-switch-20261028/second-ruling/removed-repository-providers.json)、[汇总](../../tools/bolt/results/qb-meta-switch-20261028/second-ruling/closure-summary.json)。Base当前仓库的原始repomd/primary与SHA验证在[base-current/provenance.json](../../tools/bolt/results/qb-meta-switch-20261028/second-ruling/base-current/provenance.json)。分析脚本存入本结果目录，便于复核。

### 8.4 Unified最终改动及上传

再次fetch后master仍为`7b2f2ae2d0e0cdc42307454c73c10be23b6d0ef5`。从这个master单独detached提交，没有叠加359363。XML合法，git diff仅1文件、2行删除/2行增加；base子树和其余项目文件逐字节不变。不新增DOD、不改project_meta/config、manifest、candidate_snapshot或project_env。

```diff
diff --git a/TIZEN/Tizen/Tizen-Unified-Toolchain/snapshot_info b/TIZEN/Tizen/Tizen-Unified-Toolchain/snapshot_info
index e70cfb8..14bc58f 100644
--- a/TIZEN/Tizen/Tizen-Unified-Toolchain/snapshot_info
+++ b/TIZEN/Tizen/Tizen-Unified-Toolchain/snapshot_info
@@ -1,7 +1,7 @@
 <?xml version="1.0" encoding="UTF-8"?>
 <snapshotinfo>
-  <latest target="tizen-unified-toolchain_20261027.063617" url="http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/"/>
-  <reference target="tizen-unified-toolchain_20261016.052151" url="http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/"/>
+  <latest target="tizen-unified_20261027.231956" url="http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified/"/>
+  <reference target="tizen-unified_20261027.231956" url="http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified/"/>
   <base target="tizen-base-toolchain_20261013.140248" url="http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/">
     <repository name="standard">
       <type name="standard"/>
```

提交说明包含代码来源证据、17个移除仓库、全量BR检查结果和合入时机，由原commit-msg hook生成Change-Id；作者、提交者和Signed-off-by都是Hao Lin。完整说明见[unified-final-commit.txt](../../tools/bolt/results/qb-meta-switch-20261028/second-ruling/unified-final-commit.txt)，结构验证见[unified-validation.json](../../tools/bolt/results/qb-meta-switch-20261028/second-ruling/unified-validation.json)。

```sh
git push origin 12f22a9c3cd1262f91a798d8f6439f6e3835ad31:refs/for/master
```

[推送原文](../../tools/bolt/results/qb-meta-switch-20261028/second-ruling/unified-push.txt)返回SUCCESS及上述change URL。**合入建议**：先让Base-Toolchain按Base代码产出新快照，再配合正常的依赖快照引用更新合入。本补丁的base仍是固定20261013.140248，单纯“等到新快照发布”不会让固定URL自动更新；总部合入时应确认正常配置更新已推进该引用。本轮没有越权改base，也没有宣称旧依赖能满足新代码的全部版本需求。

### 8.5 执行边界和交付核对

只上传上述两个`refs/for/master`，没有推master、sandbox或其他分支，没有添加reviewer。没有构建软件包、修改QB状态、修改LLVM源码/历史构建根、删除目录或修改VS Code配置。scm/meta/qb中只产生两个独立提交；GitHub仅追加本节、STATUS和审查证据。前文逐字节保留检查和证据索引见本目录`delivery-validation.json`与`SHA256SUMS`。
