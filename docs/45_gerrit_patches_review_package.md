# 45 两个 Gerrit 补丁的外部评审材料包

日期：2026-10-10。本文只汇集既有证据，不新增构建、转换或运行测试。评审对象为 **x86_64 生产补丁**；ARM 候选与本轮修订属于另一个待认证版本，不能替代这两份补丁。既有材料链接钉在已发布 Git 提交 `ddc73105dbd46348c650414e7e48bfd95c5309e9`；本轮docs/44最终报告内容钉在续二小修/测试停止提交 `b547f987739d068f267d62f9cd67981c46b0f56b`，均不随main漂移；也可由[本提交的docs/44](44_arm_source_review_round1.md)读取同字节版本。`temp/` 是本机证据，不在 GitHub；W=`/home/linhao/Toolchain/development/llvm-optimize`。（出处：docs/36 §3、docs/38 §6、docs/43 §1。）

## 1. 身份与依赖顺序

| 项目 | 356627 patchset 2 | 356639 patchset 1 |
|---|---|---|
| 内容 | ThinLTO 静态归档转机器码 | LLVM 包的 x86_64 静态归档改用 llvm-strip |
| Gerrit 地址（标识，不作为本文证据链接） | `https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/356627` | `https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/356639` |
| 已上传标题（用户本轮确认） | `packaging: fix llvm-static-devel with ThinLTO` | `packaging: use llvm-strip for x86_64 archives` |
| 已上传提交 | `67619ec8bbbac7238a6cfc33a481ccfbcd12206f` | `b0465d099164a8f8c1ddd406e6f74c2ada8f9f9f`（本轮只读ls-remote核验） |
| 父提交 | `cb67996861d070d68fec2b4c623eed7d20ba2e23`，tizen_base | `67619ec8bbbac7238a6cfc33a481ccfbcd12206f` |
| Change-Id | `Id4eb147e7ec4764d58a81110cf7bf57d21b64ac8` | `Iac085555112855d60cc7591931e91466691db6b2` |
| 作者 | FatTank `<hao.lin@samsung.com>` | 同左 |
| 仓库 format-patch 的提交封套 | `2d773cb6191e07610627a544af908b4c19da6abc` | `f86dc69a7461a9708c2280fe49961c9730dd9beb` |
| format-patch SHA256 | `ddef2221db9ba1c044b0087b9fcde2a93202fdf28c518b4d0dcd1c4653119ac6` | `49c5618226a8d281d9aed9427eb651391684e17a4e75bf68673d5cf2bf8761a5` |

**封套提交号与上传提交号不同，不可混写。** 用户确认上传时仅修改标题、其余内容一致；356627 PS2 的完整提交及父提交还经 docs/38 的 fetch 独立核验。356639 PS1本轮经无交互`git ls-remote refs/changes/39/356639/1`取得完整号，不把本地候选f86dc69a当成已上传提交；仅查询，不修改/推送Gerrit。原始输出见docs/44 §11、`temp/arm-source-review-continue-20261010/gerrit-356639-ls-remote.txt`（exit0，stderr空）。（出处：docs/36 §3.1–3.3；docs/38 §6；用户本轮任务“第五步”。）

356627 的新增 `packaging/llvm-static-archives-native.py` 与仓库 `tools/llvm_static_archives_source.py`、`patches/archive-index-fix/llvm-static-archives-native.py` 同字节，SHA256 **`6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557`**。不能拿 ARM 候选 `1620a8da…` 替换本次评审附件。（出处：docs/36 §3.2、docs/43 §1。）

直接入口：[356627完整补丁](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/patches/archive-index-fix/0001-Fix-llvm-static-devel-usability-with-ThinLTO.patch)；[356639完整补丁](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/patches/llvm-strip/0001-Use-llvm-strip-for-x86_64-archive-packaging.patch)；[生产Source](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/tools/llvm_static_archives_source.py)。

## 2. 356627 设计与 spec 全部改动

**问题。** ThinLTO 使组件 `.a` 含 LLVM bitcode。原 GNU `strip -g` 不识别这些成员，仍可能返回成功并重写出丢失/残缺索引；即使恢复索引，GNU ld 无 LTO/LLVM 插件仍不能读取 bitcode。因此只修 armap 或只换 strip 不能满足本项目的 GNU ld 消费者要求。（出处：docs/26 §1、docs/27 方案变更、docs/33 §2–§3；[生产Source](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/tools/llvm_static_archives_source.py) 的头注释。）

**流程。** 编译链接结束后，x86_64 `%install` 末尾扫描安装根所有 `.a`（包括 libarcher）；拒绝 thin/未知成员格式，纯机器码整档跳过。含 bitcode 时按“归档路径 + 成员序号/名称/同名出现序号”读取，不用 basename 覆盖提取；机器码成员保持原字节，bitcode 经本构建树 clang 转成 ELF ET_REL。按原序确定性 `ar qcDS`、`ar sD` 重建 GNU 归档；检查全部成员、完整符号→成员索引后再回写。标准 RPM 后处理完全保留，最终 strip 去除 DWARF。（出处：[生产Source](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/tools/llvm_static_archives_source.py):589–714、730–769；docs/35 §2–§3。）

**编译策略。** 从 `llvm.commandline` 逐 token 归入已进 IR / 与本次机器码生成无关 / 后端补回三类；未知 token 即失败。末项优化必须 `-O3`、DWARF 必须 4，function/data sections、unique section names、addrsig 必须启用；FP contraction 取末项，缺省为 LLVM 22 的 `on`。不传 `-flto`。另验 x86 triple、PIC/PIE、类型元数据；明确认证的后端策略，并非通用命令重放。（出处：[生产Source](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/tools/llvm_static_archives_source.py):173–178、189–329；docs/32 §1、docs/37 §3。）

**门禁与事务。** PIC 重定位扫描；转换前后 `llvm-nm --defined-only --extern-only` 按名称检查强符号不丢失，弱符号允许缺失并汇总；归档索引独立要求精确外部定义符号多重集合。摘要以临时文件+replace 更新，状态 CONVERTED→INSTALLING→PASS；每档同目录临时文件核 SHA/权限后 `os.replace`。失败非零，安装阶段写 INSTALL_FAILED；无待转换归档打印 NATIVE_ARCHIVES_SKIP。每档原子，不承诺整库回滚。（出处：[生产Source](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/tools/llvm_static_archives_source.py):331–378、487–587、589–769；docs/35 §3–§4。）

**资源。** 默认 4 workers；转换编译子进程地址空间 4 GiB；每命令 600 秒超时；取消先 SIGTERM，3 秒后 SIGKILL 进程组，信号不能变成成功退出。构建整体的 cgroup cap 是外层验证措施，Source 自身不创建 cgroup。（出处：[生产Source](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/tools/llvm_static_archives_source.py) 的 Commands、convert、install_main；docs/32 §1、docs/35 §2.2。）

spec 只有下列两处插入，完整 diff 原样引自评审补丁；Source 声明无架构条件，BR 与实际执行仅 x86_64：

```diff
diff --git a/packaging/llvm.spec b/packaging/llvm.spec
index 64705188b67c..8240282641a3 100644
--- a/packaging/llvm.spec
+++ b/packaging/llvm.spec
@@ -44,6 +44,11 @@ Source1001: llvm.manifest
 Source1002: mlgo_arm_model.tar.gz
 Source1003: mlgo_aarch_model.tar.gz
 Source1004: mlgo_x86_model.tar.gz
+Source1005: llvm-static-archives-native.py
+
+%ifarch x86_64
+BuildRequires: util-linux
+%endif
 
 %{!?mlgo_build_jobs: %define mlgo_build_jobs 6}
 %{!?mlgo_verify_configure_only: %define mlgo_verify_configure_only 0}
@@ -421,6 +426,20 @@ rm -rf %{buildroot}%{_libdir}/debug/*
 rm -rf %{buildroot}/usr/lib/libear/*
 rm -rf %{buildroot}/usr/lib/libscanbuild/*
 
+%ifarch x86_64
+# Run after compilation has finished; these workers do not overlap build jobs.
+# Preserve the standard RPM post-processing, including archive strip -g.
+rm -rf "%{_builddir}/%{buildsubdir}/build/native-archive-conversion"
+python3 %{SOURCE1005} --root "%{buildroot}" \
+    --build "%{_builddir}/%{buildsubdir}/build" \
+    --evidence "%{_builddir}/%{buildsubdir}/build/native-archive-conversion" \
+    --arch x86_64 \
+    --compiler "%{_builddir}/%{buildsubdir}/build/bin/clang-22" \
+    --disassembler "%{_builddir}/%{buildsubdir}/build/bin/llvm-dis" \
+    --nm "%{_builddir}/%{buildsubdir}/build/bin/llvm-nm" \
+    --jobs 4 --address-space-bytes 4294967296 || exit 1
+%endif
+
 %post -n clang -p /sbin/ldconfig
 %postun -n clang -p /sbin/ldconfig
 

```

`%{buildsubdir}` 在已验构建中为 `llvm-22.1.8`；使用明确 build 路径，不依赖 `%install` 的 `$PWD`。转换工人不与编译任务叠加；没有更改 strip 宏、并发或任何优化配方。（出处：docs/32 §1、docs/36 §3.2；[356627完整补丁](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/patches/archive-index-fix/0001-Fix-llvm-static-devel-usability-with-ThinLTO.patch)。）

## 3. 356627 既有验证证据

下表区分历史 v1、最终 v2 和纯文本策略核查，不能合并成“干净 tizen_base 已完整验收”。

| 检查 | 已有结果与范围 | 证据 |
|---|---|---|
| 历史一次完整构建 | docs/30 v1 Source `2476c5ef…`；22 RPM，16,011.555025 s，4/4/1、18 GiB/swap0；不是本次6bd Source | docs/30 §2–§4 |
| v2 完整构建与最终续跑 | docs/34 v2完整构建成功，试验strip导致运行库逐字节门禁停止；docs/35恢复提交配置，唯一-ba --noprep续跑5,381.375232 s，6/6/2、18 GiB/swap0，22 RPM；最终验收以下均指docs/35+36 | docs/34 §3–§4；docs/35 §1–§3 |
| 开发归档 | 225唯一路径、3,864成员：3,853 bitcode转机器码、11原机器码保留；全部ET_REL、无bitcode/调试节；原成员顺序/同名身份一致，完整索引等于定义外部符号多重集合；10成员分段抽查通过 | docs/35 §2.2、§3.1 |
| 强/弱符号 | 强符号缺失0；允许缺失的W类1,920，其他类别0 | docs/35 §2.2 |
| compiler-rt | 45归档、1,964成员ELF与docs/13基线逐字节一致；完整索引一致、无调试节；ar成员mtime差异单列 | docs/35 §3.1 |
| 非归档文件 | 17,689路径核清单/模式/类型/软链接/摘要，差异仅225开发库与45运行库归档；其他文件0差异 | docs/35 §3.3 |
| 标准brp链 | find-debuginfo、compress、archive-strip、python-hardlink、find-docs照常；GNU strip格式错误0；转换BEGIN/END完整，大载荷已删 | docs/35 §3.2 |
| 独立安装 | 独立buildroot真实-bi从构建原件再次转换225档并验收PASS；随后同树直接调用Source打印SKIP，225档SHA不变。前者不是SKIP | docs/35 §4.1–4.2 |
| 宿主七项 | A-bfd/A-lld：解析IR+PassBuilder O2结果同opt；B-bfd/B-lld：进程内lld生成物exit37；共享库-z defs/-z text+dlopen；GC运行与大小记录；原bitcode/GNU ld反例 | docs/35 §5.1 |
| Tizen bfd/lld两包 | docs/35因旧Base404未编译；docs/36从107个原缓存RPM复原，两个新根各113包NEVRA同docs/30，BR精确22.1.8-1；225归档+4工具身份相同，两包A同根内opt -O2、B生成物exit37全部PASS；实际命令无-flto/-plugin | docs/36 §1–§2 |
| 新目标参数策略 | cb679968对f111162e公共flags多一个已存在的-Wno-unused-command-line-argument；3,853派生原命令分类全部PASS，未分类0，末项相同；只读文本核查，没有新IR/完整构建/%install | docs/37 §1–§4 |
| 目标补丁应用 | 干净cb679968 git apply --check --index与完整tree核对PASS；剔除两插入块后spec等于目标原件，Source同6bd | docs/36 §3.2 |

归档中 `libarcher_static.a` 属于 llvm-static-devel 与 libomp-devel 双归属，225按唯一路径计数；不是compiler-rt的45个运行库之一。（出处：docs/35 §3.1；docs/38 §3.1。）

宿主消费者使用宿主GCC 13 C++头/libstdc++/glibc，Tizen libxml2通过独立目录和显式loader提供；Tizen两包则是完整Tizen根，gcc14.2.0、glibc2.40、binutils2.43。两环境不能混称一个纯Tizen宿主测试。（出处：docs/35 §5.1；docs/36 §2.1–2.3。）

## 4. 356639：仅 LLVM 包 x86_64 静态库后处理

在父补丁已使静态库全为机器码后，跟随平台LLVM编译环境，把本包 `%__strip` 指向 llvm-strip；不改归档转换、不改其他包、不改变 find-debuginfo 工具。**影响面结论限当前开debuginfo的Tizen宏链**。（出处：docs/38 §1、§6；[356639完整补丁](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/patches/llvm-strip/0001-Use-llvm-strip-for-x86_64-archive-packaging.patch)。）

完整新增内容为4行：

```diff
+%ifarch x86_64
+# With debuginfo, __strip handles static archives; find-debuginfo uses eu-strip.
+%define __strip %{_bindir}/llvm-strip
+%endif
```

### 4.1 宏链实际使用点

R为docs/38的试验构建根。行号来自其存档宏文件，不能直接套到另一个RPM版本。（出处：docs/38 §1，`temp/llvm-strip-x86_64-20261009/*numbered.txt`、`macro-inputs.json`。）

| R内路径:行 | 当前实际行为 |
|---|---|
| `usr/lib/rpm/macros:83` | 默认__strip=/bin/strip，被试验spec覆盖 |
| `usr/lib/rpm/platform/x86_64-linux/macros:72–74` | 默认三调用，随后被Tizen宏重定义 |
| `usr/lib/rpm/tizen/macros:34–38` | 生效的strip-install-post，文件链接到../tizen_macros |
| 同文件`:35` | brp-strip仅在无debug包时执行；本次不执行 |
| 同文件`:36` | brp-strip-static-archive传入%__strip，当前唯一实际使用点 |
| 同文件`:37` | brp-strip-comment-note已注释 |
| 同文件`:40–46、53–60` | compress、strip链、python-hardlink、find-docs；debug步骤独立且在前 |
| `usr/lib/rpm/macros:182–196` | find-debuginfo接_smp_mflags，不接%__strip |
| `usr/lib/rpm/find-debuginfo.sh:269、275、277–280` | STRIP_DEFAULT_PACKAGE未设置，选择eu-strip；后备分支也不读%__strip |
| `usr/lib/rpm/brp-strip-static-archive:7、15–20` | 取首参为STRIP，对ar执行-g；不聚合逐档失败，所以必须单独追踪退出码 |

根内 eu-strip 来自 `elfutils-0.189-1.10.x86_64`；llvm-strip来自已安装 `llvm-22.1.8-1.6.x86_64`，后处理脚本来自 `rpm-build-4.14.1.1-1.4.x86_64`。本次追踪的是构建环境 `/usr/bin/llvm-strip`，不是假定调用刚产出的build/bin版本。（出处：docs/38 §1。）

### 4.2 实测证据

| 检查 | 结果 | 证据 |
|---|---|---|
| 一次增量产包 | -ba --noprep，6,318.154842 s，18 GiB/swap0、6/6/2、debuginfo4，22 RPM；无完整重建 | docs/38 §2 |
| 225开发归档 | 全机器码、无DWARF、顺序/重名身份、完整索引全部PASS；强符号缺失0 | docs/38 §3.1 |
| compiler-rt 45/1,964 | 每成员全部SHF_ALLOC的类型/flags/大小/内容SHA相同，NOBITS按大小/类型；完整符号→成员映射一致，无调试节 | docs/38 §3.2 |
| 结构变化 | 全1,964成员ELF字节不同：字符串表合并、空表处理、节区/符号索引重编号、偏移等；64成员66个共同节sh_entsize变化（init/preinit数组为主）；全部成员SHA同docs/34旧overlay，未出现新类别 | docs/38 §3.2 |
| 非静态库 | 17,689路径只有270个.a不同，非静态库0差异；clang-22/lld/llvm-ar与GNU-strip版本及基线SHA相同 | docs/38 §3.3 |
| strip逐次退出 | execve/exit_group追踪270个唯一归档路径，全部llvm-strip -g exit0；格式/诊断错误0行；不是仅用rpmbuild总退出码 | docs/38 §3.4；`continue-20261009/rpm-exec-exit.trace` |
| 后处理完整 | find-debuginfo 1、compress 1、archive-strip 1、python-hardlink 1、find-docs 1；独立brp-strip 0符合debug条件；NATIVE段完整、大文件删除 | docs/38 §3.4 |
| 七宿主消费者 | 同§3的A/B/共享库/GC/反例，7/7 PASS | docs/38 §4.1 |
| 宿主运行库 | bfd/lld各测ASan堆越界（非零且heap-buffer-overflow）、ASan正常exit0、UBSan有符号溢出报告、profraw可merge、builtins 128位除法正确；10/10 PASS | docs/38 §4.2 |
| Tizen运行库与API | bfd/lld两新包A/B及上述运行库探针全部PASS，profraw 224B→合并profile640B；两个根114包，仅比docs/36增compiler-rt；实际编译/链接无-flto/-plugin | docs/38 §5 |
| 提交应用 | 干净67619ec8父提交git apply --check与tree相同；Source6bd不变；仅spec四行 | docs/38 §6 |

可加载内容一致不等于ELF逐字节相同，也不是对所有sanitizer功能的穷举保证。docs/38的Tizen bfd测试包scope峰值触及6 GiB且memory.events的max=294、OOM=0；该峰是cap约束下数据，不当作自然内存需求或性能结果。（出处：docs/38 §3.2、§5.3。）

## 5. 已知边界与评审重点

1. **仅x86_64。** 当前Source choices、triple与PIC规则都只认证x86_64。356627拟议PS3才加入ARM；356639将rebase并扩架构，仍需后续spec/RPM验收。ARM Source不是本包附件的替代品。（出处：docs/36 §3.2；docs/43 §1、§5；本轮用户决定。）
2. **版本闸门只核clang主版本22。** dis/nm仅查存在/可执行，现spec三工具都来自同一构建树；脚本未独立要求完整版本相同。ARM新工具预检不自动改变x86共用代码。（出处：[生产Source](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/tools/llvm_static_archives_source.py):535–549；spec显式三路径；本轮docs/44 §8–§10。）
3. **强符号对照只比名称。** 不以该门禁证明符号类型、可见性、大小及全部语义一致；索引的精确多重集合是另一个检查。允许弱符号丢失也不是任意ABI变化的许可。（出处：[生产Source](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/tools/llvm_static_archives_source.py):499–521；docs/35 §2.2、§3.1。）
4. **逐档原子≠整库事务回滚。** 安装途中失败可能已有部分归档替换，状态INSTALL_FAILED、%install失败；本设计不恢复已写归档。重新真实%install与同树幂等已有分别验收。（出处：[生产Source](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/tools/llvm_static_archives_source.py):563–577、730–769；docs/35 §4。）
5. **纯机器码归档整档跳过。** 先拒thin/other，再按bitcode数决定跳过；不重做该档的转换/PIC/强符号检查，也不把SKIP等同全新生产环境认证。独立运行库验收补足当前固定输入的证据。（出处：[生产Source](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/tools/llvm_static_archives_source.py):524–549、611–619；docs/35 §3.1、§4.2。）
6. **目标配方未完整构建。** cb679968/67619ec8的源码配方在本轮未从干净目标重建；docs/37是现有3,853命令替换公共flags后的纯文本策略核查。未来新增token、宏默认或LLVM主版本变化会按设计失败，需重新分类和认证。（出处：docs/36 §3.1；docs/37 §4；docs/38 §6。）
7. **llvm-strip结构差异允许但有边界。** 只放行既有分类，核全部SHF_ALLOC与完整索引并补真实运行；不是关闭debuginfo或把compiler-rt字节变化忽略。全库归档可能因标准strip工具版本变化而变，需要重新核验。（出处：docs/38 §3.2、§4–§5。）
8. **当前默认选项不是通用接口。** -O3、DWARF4、分段开启、x86 triple与PIC等策略从认证语料确定；未启用ThinLTO且全native时为no-op，但工具/构建目录预检仍先执行。Python最低3.9，util-linux BR用于prlimit，摘要分块读取。（出处：SOURCE头注释、validate_tools/convert；docs/32 §1、docs/36 §3.2。）
9. **ARM评审仍独立。** docs/43为1620候选历史认证，docs/44 §7–§12为5608修订停止历史；本轮§13–§17诊断600例支持取消测试时序问题，授权小修后候选为`e2c2ebfa7272c6549f9be977861985ff597d3564dd26caf72438155622e30e0d`。宿主99/99 PASS；ARM32 Python3.14.2为94 PASS、2 FAIL、3环境ERROR，仍未通过全套门禁。x86与两ARM全量回归未启动，不把旧after SHA或消费者证据绑定到新候选。（出处：docs/44 §13–§17；E3/stop-result.json。）

10. **x86 Source不检查module asm；本轮只读核查仍NOT RUN。** 生产6bd的ir_settings不解析该语句，check_symbols仅比较定义外部符号，不能证明.globl引入的UND引用存在。任务原定在docs/35最终产物定位含该声明的真实成员并报告`_ZSt21ios_base_library_initv`绑定/节索引；因第三步根内测试失败而停止，未执行此项，实际成员清单与符号状态UNKNOWN。不能以ARM原声明、源码路径或旧消费者通过推断x86最终符号。此处是证据缺口，不声称x86符号已丢失。（出处：生产Source:275–329、499–521；docs/44 §16；E3/stop-result.json。）

11. **生产Commands取消不保证返回时后代已消失。** 父进程已被wait4回收时，发送进程组SIGKILL的同一轮可break，不另等后代消失。对同字节Commands的预注册诊断（普通300次+4CPU负载300次）：两组各4次首读R，8次均SigPnd=0、ShdPnd=0x100；600例全在3秒内消失/Z，最长5.430058ms，两组p99为5.312265/5.287699ms（5ms轮询观测上界）。按该场景判据支持测试时序问题，不能外推为同步回收保证。测试现先验不存在/Z/待处理SIGKILL，再要求3秒内终止；Commands未修改。诊断辅助脚本曾把X(dead)误作存活，仅修一次后完整重跑，原失败证据保留。（出处：生产Source:437–453；docs/44 §13；`temp/arm-source-cancel-diagnosis-20261010/diagnostic-retry/observations.jsonl`。）

12. **ARM根共用测试仍有边界。** 根内缺/usr/bin/time导致2 ERROR，宿主as --64夹具退出1；另有RLIMIT_AS期望4GiB而读回-1、timeout探针期望SIGKILL却收到SIGTERM这2 FAIL。根内/proc不可见，返回ok的后代测试不能独立证明根内状态可见性。未改测试断言/Commands或重试，两个FAIL原因未进一步实证；生产x86历史认证不因此自动作废，也不能替代新ARM环境验收。（出处：docs/44 §15；E3/unit-tests-armv7l.log、armv7l-environment.json。这里E3完整路径见docs/44 §13。）

## 6. 外部评审读取清单

全部为固定提交raw文本；补丁自身含完整Source，独立Source供阅读无需从diff还原。`temp/`原日志大于文档范围，本机路径从对应报告展开。

- [356627补丁全文](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/patches/archive-index-fix/0001-Fix-llvm-static-devel-usability-with-ThinLTO.patch)
- [356639补丁全文](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/patches/llvm-strip/0001-Use-llvm-strip-for-x86_64-archive-packaging.patch)
- [x86生产Source6bd](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/tools/llvm_static_archives_source.py)
- [补丁旁Source同字节副本](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/patches/archive-index-fix/llvm-static-archives-native.py)
- [docs/30 §2–§4：历史完整构建](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/docs/30_archive_fix_full_build.md)
- [docs/34：v2完整构建及停止边界](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/docs/34_archive_fix_v2_build.md)
- [docs/35 §2–§5：最终提交配置与幂等](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/docs/35_archive_fix_v2_final.md)
- [docs/36 §1–§3：两Tizen包与补丁](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/docs/36_archive_fix_tizen_consumers.md)
- [docs/37：新配方策略覆盖](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/docs/37_target_recipe_policy_check.md)
- [docs/38 §1、§3–§6：strip宏链和运行库](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/docs/38_llvm_strip_x86_64.md)
- [docs/43：历史ARM候选与测试](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/docs/43_arm_conversion_review_package.md)
- [历史ARM候选1620（非生产Source）](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/ddc73105dbd46348c650414e7e48bfd95c5309e9/tools/llvm_static_archives_arm_trial.py)

- [docs/44：首轮历史与续二诊断、小修、根内测试停止最终报告](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/b547f987739d068f267d62f9cd67981c46b0f56b/docs/44_arm_source_review_round1.md)

本文不提出合入结论；请分别审查两个change，并区分“代码设计”“现有固定输入验收”“目标流水线尚未发生的验证”。（证据边界：docs/36 §3.1；docs/37 §4；docs/38 §6。）
