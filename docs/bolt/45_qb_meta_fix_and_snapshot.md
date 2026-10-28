# 45：QB DOD 本地修复与固定快照比较

本地已把Toolchain和Dev的DOD引用各改回自己实际创建的名字，保留改用Tizen-Base快照的意图；其他不同名引用的Tools项目有显式DOD定义，不构成默认生成路径的反例。两个快照的工具链并不完全相同，不能沿用39号的精确clang SHA验收。后续本地依赖来源改为固定Tizen-Base `20261026.005418`；但其build.conf不定义`_toolchain`，与要求debug包的构建模式存在冲突，已请求用户裁决，完整构建尚未启动。

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

`lld`不是单独包名：primary文件列表显示`/usr/bin/ld.lld`由`llvm`提供；新版是llvm22.1.8-6.5。`/usr/bin/eu-strip`由`elfutils-0.189-1.106.x86_64`提供（不是假定宿主工具可用）；第三件将在x86_64+BOLT条件内显式BuildRequires elfutils。

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

**需裁决的冲突**：f308 spec L18–23在入口检查`_toolchain`，未定义则`llvm_release_build=1`；L31–37关闭debug_package并设置后处理删除`/usr/lib/debug`和`/usr/src/debug`。spec L83以后再定义_toolchain无法逆转先前分支。因此严格使用新build.conf和原给定三个宏，不能满足本任务clang-debuginfo、22二进制RPM及调试文件post SHA要求。已请求仅本地增加`--define "_toolchain clang"`的明确授权；未自行改变基线后处理或默默添加宏。此项与DOD两行修复无关。

## 5. 验收口径与状态

工具链不同：第三件采用R≤5%、S/N≤5%、90TU对象一致，以及列全23包差异并解释的口径；不要求clang SHA等于39号。配置修复仅本地提交、未送总部评审；快照盘点已完成。debuglink实现/完整构建进度另见43号报告，不能把这里的配置和下载检查说成完整构建通过。
