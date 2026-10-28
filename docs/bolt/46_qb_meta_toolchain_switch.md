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
