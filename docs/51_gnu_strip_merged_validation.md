# 51 仅合入 356627、归档仍用 GNU strip：证据核查与补充实测

日期：2026-10-14，Asia/Shanghai。起点 `6972188df206f96bb3c081191aa8eb2582376ae1`。

**结论：机器码、归档索引和普通消费者兼容性已有实测支持，本轮补查也通过；但 `.llvm_addrsig` 在 GNU strip 后失效。**
该失效没有破坏实际符号表、代码或重定位：lld 22 保守忽略它，普通链接/运行通过；`--icf=safe` 会警告，加 `--fatal-warnings` 则链接失败。
**docs/38 的 llvm-strip 版 RPM 也有同一失效并在同一条件下失败，因此不能把合入 356949 当作本问题已验证的修复。**
16:27:24 下载站 HTTP 200，最新仍为 `tizen-base-toolchain_20261013.140248`，没有合入后的快照；官方 RPM 对照挂账，不等待。

本轮不改 Source、spec、补丁或配置，不构建 LLVM，不推 Gerrit；未进入 BOLT 资产及已交接的新 x86 构建树。
只在新证据目录处理副本，历史资料保持原样。机器可读完整摘要：[51_gnu_strip_validation.json](51_gnu_strip_validation.json)。

## 0. 路径与证据口径

`W=/home/linhao/Toolchain/development/llvm-optimize`。以下相对路径以 W 为根。

| 别名 | 路径及用途 |
| --- | --- |
| E | `temp/gnu-strip-merged-check-20261014`，本次新证据/副本 |
| C35 | `temp/archive-fix-v2-final-20261009/continue-20261009`，历史 GNU strip 构建、验收 |
| E36 | `temp/archive-fix-tizen-consumers-20261009`，历史 Tizen 消费者、提交身份 |
| E38 | `temp/llvm-strip-x86_64-20261009/continue-20261009`，历史 llvm-strip RPM 验收 |
| N | `temp/toolchain-archivefix-v2-final`，docs/35 GNU strip RPM 解包 |
| N38 | `temp/toolchain-llvm-strip`，docs/38 llvm-strip RPM 解包 |
| H | `temp/archive-index-fix-rpm-20260923/baseline-rpm-extract`，旧基线工具/头文件与反例 |
| U | `temp/release-attribution-20261013/x86-production-conversion/archives`，保留的未 strip 开发归档；本次不转换 |
| B旧 | `temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build`，只读 compiler-rt 原件 |
| R0 | `temp/gbs-root-x86_64-debuginfo-j4-v2/local/BUILD-ROOTS/scratch.x86_64.0`，只读 GNU strip、loader/库和 brp 脚本 |

B旧是 docs/34–38 的历史树，**不是**后来交接给 BOLT 的 `/var/tmp/llvm-optimize-x86-archivefix-20261013/...` 树。
完整逐成员 JSON、原始日志与脚本在本机 E；GitHub JSON 提供输入/输出逐档 SHA、命令、汇总与历史证据摘要，未上传二进制载荷。

## 1. 历史证据核查：有功能证据，但不是精确提交配方的完整重建

### 1.1 356627 PS2 身份

docs/50 已核验 tizen_base 合入提交 `67619ec8bbbac7238a6cfc33a481ccfbcd12206f`，父 `cb67996861d070d68fec2b4c623eed7d20ba2e23`，与上传的 PS2 内容相同。
本轮重新读取保存的合入文件并算 SHA：

| 文件/状态 | SHA256 |
| --- | --- |
| 合入/PS2 `packaging/llvm.spec` | `d93a549206434c4512c60d5a96bfeb133b7aaf6ea13b8cd0302e06c1cb99b1c9` |
| 合入/PS2 Source | `6bd0546a63bd50151296a366ce0e7c688d774e91a36015ba194227e4ca092557` |
| docs/35 实际试验 spec | `6a91a0bf3d8d2044473662b65ed3d32d4696a697ccd52200d983ce4334aeafdf` |
| docs/35 实际 Source | 同上 `6bd0546a…` |
| docs/35 GBS 导出 spec（另有 VCS/Patch 字段） | `91f684691eb35af52b1a9f2a2cba478f88dbfd8a48b4c2281dac6144d71d3bd0` |

证据：`temp/archive-followup-review-20261014/{merge-check.json,merged-llvm.spec,merged-llvm-static-archives-native.py}`；
`C35/precheck.json`；`E36/submission-verification.json`。本轮对应文件存在性、大小与 SHA 清单为 `E/historical-evidence.json`。

### 1.2 docs/22–38 的证据链

| 报告 | 实际覆盖 | 能否作为本组合的精确完整构建证据 |
| --- | --- | --- |
| docs/22–26 | bitcode 索引缺陷、旧宏修法及停止记录 | 否；尚非 bitcode→机器码修法 |
| docs/27–28 | 离线转换和消费者阶段，分别因入口/资源规则停止 | 否；旧转换器或非完整验收 |
| docs/29 | GNU strip 离线模拟和七消费者通过；完整构建入口未启动 | 否 |
| docs/30–31 | 一次完整构建，GNU strip，225/45、宿主/Tizen 通过 | 较早修法的支持证据；Source 是 `2476c5efa061499d7963e0f0976f0c9c86944b688f5bcc48ea40911574af399e`，不是 PS2 |
| docs/32 | v2 离线阶段停止，未完整构建 | 否 |
| docs/33 | 未转换 bitcode + llvm-strip 失败的对照调查 | 不能混同转换后机器码 |
| docs/34 | Source 6bd 的完整构建，额外加了 llvm-strip 宏 | 否；strip 配置不同 |
| **docs/35** | 恢复 GNU strip，`-ba --noprep` 增量构建/RPM；225 开发档、45 compiler-rt、七宿主、独立安装与 SKIP 通过 | **直接支持 Source 6bd + GNU strip 的组合；不是 d93a 配方从零完整构建** |
| **docs/36** | docs/35 同一 RPM 的 Tizen bfd/lld 消费者通过，生成 d93a 提交配方 | 补齐 Tizen 证据；明确没有重建刷新后的整个 tizen_base 配方 |
| docs/37 | 两基准配方宏展开、3,853 条历史命令策略覆盖 | 编译参数认证支持；不等同完整构建 |
| docs/38 | 在 docs/35 基础上改 llvm-strip，增量构建和运行库消费者通过 | 用作本次 strip 方案对照，不能充当 GNU strip 构建 |

因此，严格回答“有没有一次**精确 d93a spec + 6bd Source、只合入 356627 的完整构建并完成所有指定检查**”：**未找到。**
但也不能说“GNU strip 组合从未验证”：docs/35–36 对同一 Source 和新增转换块完成了实际 RPM 与消费者验证。
E36 的 `target-vs-validated-base.diff` 记录基准配方差异；其 diff 方向是目标 cb679968 → 本机 f111162e，不能反读。
差异包括诊断参数、编译器别名、显式 dylib 开关、条件化 flags 等；docs/37 的 `policy-result.json` 为 225 档/3,853 命令、未分类 0，明确未做新编译。

### 1.3 历史直接检查及缺口

docs/35 §3–§5 原始记录：

- `C35/build/build.log:8690`：`+ /usr/lib/rpm/brp-strip-static-archive /bin/strip`；格式错误 0。
- `new-archives-result.json`、`new-archive-checks/`：225 档、3,864 成员全机器码/无 DWARF；318,543 条完整索引，以符号和成员序号/同名序号核对。
- `install-conversion-summary.json`：转换前后强符号缺失 0、允许弱 W 消失 1,920；这是**转换**符号检查，不是 strip 前后全部符号属性比较。
- 45 compiler-rt 的 1,964 成员 ELF 与 H 相同、完整索引相同；`runtime-ar-header-differences.json` 将 ar mtime 差异单列。
- `new-rpm-consumers/result.json` 七项 PASS；E36 `tizen-summary.json`、`tizen-{bfd,lld}/` 是实际 Tizen A/B 链接与运行证据。

历史转换的 PIC/重定位扫描及共享库 `-z text` 消费者存在，但没有找到 strip 前后全库 `.llvm_addrsig`、全部符号属性/规范化重定位的完整检查。
**本轮按任务第 2 项补齐，未倒填或改判旧报告。**

## 2. GNU strip 补充实验

### 2.1 输入身份与方法

U 的 225 个归档实际 SHA 全部等于自身 summary 的 after SHA，且逐档等于 **C35/ba-install-conversion-evidence/summary.json** 的 after SHA。
U 虽由后续 Source 回归保存，但本次输入是与 PS2 实测转换结果**逐档同字节**的机器码副本，未重新转换、未用新构建树替代旧证据。
45 个 compiler-rt 从 B旧 `lib64/clang/22/lib/linux/*.a` 复制；输入路径/字节/SHA 全量登记为 `E/input-inventory.json`。

按原成员序号/名称/同名出现序号核对；`tools/inspect_llvm_archives.py` 解析索引 header offset。
补充只读 ELF 检查器为 `E/check_strip.py`：比较 ELF 头、SHF_ALLOC 的类型/flags/大小/对齐/内容、符号名称/类型/绑定/可见性/所在节/值/大小、规范化的非调试重定位及去除调试成员的 COMDAT。
不将被正常删除的 FILE、SECTION 和调试节符号当作外部符号损坏。RELA 显式 addend 一并比较。
`sh_entsize` 单列结构差异，核心可加载检查沿用 docs/38 §3.2 的 type/flags/bytes/content 规则；没有用 `.llvm_addrsig` 的坏索引去解释实际 `.symtab`。
原有归档解析/strip 检查 12 项测试全通过（`validator-tests.log`）。

实际命令（完整绝对 argv 在 JSON）：

```sh
R0/lib64/ld-linux-x86-64.so.2 \
  --library-path R0/usr/lib64:R0/lib64 \
  R0/usr/bin/strip -g E/strip-output/<归档相对路径>
```

`R0/usr/lib/rpm/brp-strip-static-archive:19` 正是 `$STRIP -g "$f"`，脚本 SHA
`d40b7c625bf8e1e685f9130c7dbe3e2b9e8a144d2c3a4b52ab4a3c39afee712b`。
实测 `GNU strip (GNU Binutils) 2.43`，工具 SHA
`ee80ec36060dc467f57a3c7ae7155affbfcd39cec254892cffa45096a9f5e7ec`；loader SHA
`e5f09939e3bb271e04524de3eb82d9d26bb528d3fe10cb9c6e7ebbaa069f466a`。见 `strip-tool.json`。

### 2.2 全库结果

| 项目 | 开发归档 | compiler-rt |
| --- | ---: | ---: |
| 归档数 | 225 | 45 |
| 成员数 | 3,864 | 1,964 |
| 完整符号→成员索引条目 | 318,543 | 47,694 |
| strip 前字节 | 6,615,100,896 | 68,423,806 |
| strip 后字节 | 520,479,520 | 37,842,410 |
| exit 0 / stderr 非空 | 225 / 0 | 45 / 0 |
| 机器码、身份/次序、无调试节、完整索引 | PASS | PASS |
| 可加载内容、符号属性、非调试重定位、COMDAT | PASS | PASS |
| strip 后成员与 docs/35 N 逐字节一致 | 全部 | 全部 |

全体 5,828 个成员均 x86_64 ELF ET_REL，bitcode/other/thin 为 0；每个索引恰为已定义外部符号多重集合，且 strip 前后完整映射相同。
原先保留的 11 个机器码成员也纳入上述检查，未跳过。

695 个成员的 697 个数组节 `sh_entsize` 从 0 变为 8，其他可加载字段均相同：
`.init_array` 671、`.preinit_array` 19、`.init_array.65537` 1、`.init_array.90` 1、`.init_array.0` 3、`.fini_array.100` 1、`.fini_array.0` 1。
这是完整记录的结构差异，不能宣称 strip 前后 ELF 全文件相同。它与 docs/34、38 已记录的数组节 entry-size 差异属于同类；本次字节内容/大小/类型/flags/对齐均无差异。
`strip-result.json` 的原始 `SEMANTIC_DIFFERENCES` 标签保留了包含 entsize 的较严字段比较；`validation-summary.json` 显式分出上述结构差异与核心门禁，未覆盖原数据。

### 2.3 `.llvm_addrsig`：确定存在元数据失效

| 统计 | 开发归档 | compiler-rt | 合计 |
| --- | ---: | ---: | ---: |
| 带 `.llvm_addrsig` 的成员 | 3,853 | 1,946 | 5,799 |
| 其中空表 | 77 | 1,242 | 1,319 |
| payload 字节合计 | 184,863 | 23,729 | 208,592 |
| GNU strip 后 `sh_link=0` | 3,853 | 1,946 | 5,799 |

270 个归档均有受影响成员。5,799 个表的 payload SHA 全部未变，符号表已重新编号；按唯一 `.symtab` **仅作诊断地**解释旧编号，有 4,480 个表对应的符号身份改变，3,820 个表出现编号越界。
这不表示 lld 真的使用了那些坏编号；`sh_link=0` 就是告诉它不可使用该表。空表也失去有效链接，但不称其“非空内容损坏”。

代表原文（`libLLVMAArch64AsmParser.a` 的成员 0 `AArch64AsmParser.cpp.o`）：

```text
before [1003] .llvm_addrsig ... 000039 00 E 1004 0 1
before [1004] .symtab       ...
after  [ 992] .llvm_addrsig ... 000039 00 E    0 0 1
after  [ 993] .symtab       ...
```

独立 `readelf -SW/-sW/-rW/-x.llvm_addrsig` 原文在 `E/example-{before,after}-*.txt`，未修改对象。

## 3. 消费者复验与条件性失败

### 3.1 普通消费者：7/7 PASS

本次全部正例使用 E/strip-output 中的 GNU strip 结果。`tools/verify_native_archive_consumers.py` 的原有协议不变：
H 的 clang/LLVM 头/资源、宿主 GCC13 C++头及 libstdc++/glibc/crt/GNU ld；Tizen libxml2 仅经独立 library-path 使用，不安装宿主。
编译与链接分开，编译 4 GiB AS，链接无 AS 上限；GNU ld 不带 LTO/插件，driver argv 经原检查器验证。

| 检查 | 结果 |
| --- | --- |
| A：GNU ld / lld | 均通过，LLVM IR 解析+PassBuilder O2 输出与基线 opt -O2 完全一致 |
| B：GNU ld / lld | 均通过，进程内 lld 链出的程序退出 37 |
| 共享库 / dlopen | `-shared -z defs -z text`，运行输出正确 |
| GNU ld `--gc-sections` | 运行正确；47,387,472 → 28,378,320 B，仅功能记录 |
| 未转换 bitcode 反例 | 无插件 GNU ld 失败，符合预期 |

完整编译、链接、运行 argv、stdout、时间/RSS/VmPeak：`E/consumers/`；判据 `consumers/result.json`。
不把普通消费者通过外推到所有链接选项。

### 3.2 lld `--icf=safe` 的额外针对性诊断

从本次成功的 A-lld 完整 argv 派生，只增加表中选项及独立输出路径。LLVM 对照只把归档搜索目录换成 N38。

| 归档 | 附加选项 | 结果 |
| --- | --- | --- |
| 本次 GNU strip 副本 | `--icf=safe` | exit 0，1,057 条 addrsig 警告；运行输出仍与 opt 相同 |
| 同上 | `--icf=safe --fatal-warnings` | exit 1；20 条 addrsig 错误后触发默认错误数量上限 |
| docs/38 llvm-strip RPM | `--icf=safe --fatal-warnings` | **同样 exit 1**；20 条同类错误后停止 |

示例：

```text
lld: warning: ...libLLVMDemangle.a(DLangDemangle.cpp.o): --icf=safe conservatively ignores SHT_LLVM_ADDRSIG [index 16] with sh_link=0 (likely created using objcopy or ld -r)
lld: error: ...toolchain-llvm-strip/usr/lib64/libLLVMDemangle.a(DLangDemangle.cpp.o): --icf=safe conservatively ignores SHT_LLVM_ADDRSIG [index 17] with sh_link=0 (likely created using objcopy or ld -r)
```

第三条原作为预期成功的对照，实测失败；`icf-scope/outcome.json` 保留非零，没有修改预期后重跑或修产物。
随后只读盘点 N38：270 个归档 SHA 全部匹配 E38 当年的逐文件记录；不是拿到被改过的对照。
其同一 5,799 个表也全部 `sh_link=0`，旧编号解释的符号身份改变同为 4,480 个。
`llvm-strip-addrsig-control.json` 保留 `FAIL`（有效表保持假设不成立）；`docs38-identity.json` 是 270 档身份 PASS。
两种 strip 的普通消费者历史都通过，不与这里特定选项的失败矛盾。

### 3.3 源码解释及严重程度

本机 LLVM 22 源码只读依据（路径相对 W，HEAD `f111162e94aa48ed367c9d2c039456c70e7160ae`）：

- `llvm/lld/ELF/InputFiles.cpp:791–804`：`SHT_LLVM_ADDRSIG` 的 sh_link 非 0 才保存；为 0 且 `--icf=safe` 时警告并忽略。
- `llvm/lld/ELF/Driver.cpp:2587–2611`：没有可用 addrsig 时，保守地把所有符号视作地址显著；不会按失效编号进行不安全折叠。
- `llvm/llvm/lib/ObjCopy/ELF/ELFObjcopy.cpp:384`：strip-debug 删除 FILE 符号；
  `ELFObject.cpp:1133–1153` 清开一般节的 symtab 链接，`:2591–2595` 只有符号索引未改变才恢复链接。这解释了为什么不能假设 llvm-strip 必然维护 addrsig。

逐行摘录、源码 SHA 在 E 的 `*.source.txt`、`source-provenance.json`；实测链接结果优先于推断。

**影响判定：条件性兼容性问题，不是“356627 修完后索引仍损坏”或已证实运行错误。**
GNU ld、普通 lld 和指定运行测试正常；安全 ICF 会保守降级并产生警告，启用 `--fatal-warnings` 的消费者确定被阻塞。
compiler-rt 的成员与 docs/13 基线同字节，故其中的失效也存在于旧基线，不能全部归因为 356627。
本轮不估算体积/性能损失，也没有穷举所有链接器版本。
**不能以此问题为理由声称必须紧急合入 356949 即可修好：已验 llvm-strip 方案同样触发。**
356949 的发布模式/加固/平台 strip 一致性价值另行评审；若总部的实际消费者使用上述两选项组合，需要把 addrsig 保持问题单独登记处理。此任务不改 Source、spec 或任何补丁。

## 4. 官方快照：尚无合入后的产物

2026-10-14 16:27:24+08 读取[官方目录](https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/)，HTTP 200。
目录原文 `E/snapshot-list.html`，SHA
`93dd5db3a111998f83f2e5c668018788c0d91fdb3dca55e63fb840d34d8d0281`。

列出的具体快照：20260914.073422、20260924.094908、20261010.120615、20261013.024319、**20261013.140248**。
356627 合入时间为 2026-10-14 14:48:39+08（docs/50 Gerrit 原始查询）。没有日期晚于该时间的快照。
所以本轮**没有下载或比较官方 LLVM RPM**，没有拿本地 RPM 代替官方快照；也不能从目录未更新推断 OBS 构建成功或失败。

待新快照出现后：先验证包的 VCS/构建身份确实包含 356627，再与 `20261013.140248` 的 x86_64 LLVM 系列 RPM 比较；
静态库查 native/完整索引，其他文件逐字节、差异逐项列出，并登记 glibc/gcc/binutils/clang/llvm 等环境变化。
该任务已进入 STATUS，未等待、未自行改换比较基线。

## 5. 资源、产出与收尾

仅副本 strip、只读检查和小消费者编译/链接。重阶段持共享 flock；准入 10 GiB、18 GiB scope、swap0、nice15/ionice3、宿主 2 GiB/磁盘 30 GiB 保护。
未复制超过 10 GiB 的载荷；270 个原始归档总计 6,683,524,702 B，strip 后 558,321,930 B。

| 阶段 | wall | scope MemoryPeak | 结果 |
| --- | ---: | ---: | --- |
| GNU strip/全库检查 | scope 181.464 s；检查器 180.370 s | 7,254,478,848 B（含页缓存） | 核心 PASS，addrsig 失效单列 |
| 七项宿主消费者 | 32.423 s | 1,204,367,360 B | 7 PASS |
| ICF 诊断 | 原始各链接记录见 JSON | 222,150,656 B | 两个 fatal-warnings 链接失败，未重试 |
| N38 只读 addrsig 盘点 | 原始 scope 记录见 JSON | 3,069,169,664 B | 与历史 SHA 相符；有效表假设 FAIL |

四 scope 的 memory.events 均无 OOM；采样器/日志线程回收。锁释放与保护文件复核见 `E/final-audit.json`。
W/gbs_llvm.conf 原有用户修改保留、不提交；两份 Source SHA 未变。未挂载 chroot，未进入已交接树，未推 Gerrit。

主要复核入口：`E/{check_strip.py,summarize_checks.py,icf_diagnostic.py,read_llvm_control.py}`；
原始结果 `input-inventory.json`、`checks/**/*.json`、`strip-result.json`、`validation-summary.json`、`icf/*.log`、`consumers/`、`snapshots.json`。
这些脚本不写任何输入文件；失败的对照没有重跑。公开摘要中记录脚本 SHA 和完整消费者 argv。
