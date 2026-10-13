# 49 续三：调试无关性最终判据与后续执行

日期：2026-10-13；开场 Git `c38bc2ae25bc9ab530f80965479b1fb7f5757e44`。**最终状态：STOP_ARM32_ALLOC_CONTENT。41测试PASS；x86 20/20 PASS；ARM32前12对PASS，第13对Serialize.cpp内容/重定位/符号不符，立即停止。剩余7对及AArch64未判定，后续回归/补丁/构建/交接NOT RUN。** 本页承接[docs/49 §0–§19](49_round4_revision_and_x86_build.md)，旧停止记录原样保留；因主文接近50KB，§20起完整记录单列本文件，每个大步骤同时更新主文状态与STATUS。

宿主恢复命令：`sudo sysctl -w vm.mmap_min_addr=65536`，重启也会恢复。本任务不修改宿主配置；/proc只临时挂载并回收。不开Gerrit，不访问BOLT工作树/分支/证据，不清理磁盘，不改两份Source或Commands。

## 20. 完整性、用户裁决与执行边界

证据目录 H=`temp/release-contract-final-20261013`。`initial-integrity.json`核对当前两份Source、候选补丁、原LLVM spec与用户配置摘要PASS；工作树只存在用户的`gbs_llvm.conf`修改。两把项目锁由`hold_lock.py`持有。重阶段共用`/home/linhao/Toolchain/development/heavy-stage.lock`，flock排队最长2h；轻/重阶段准入6/10GiB，18GiB cap、swap0、nice15/ionice3、30s采样与宿主可用2GiB保护沿用docs/49 §1（H/initial-integrity.json、lock-acquired.json、run_stage.py）。

用户最新确认：Quickbuild当前在Tizen-Base-Toolchain构建LLVM，定义`_toolchain`，走debug分支；未来进入Tizen-Base时未定义该宏，走发布分支。本次认证因此是未来实际交付前提。发布模式完整构建仍挂账，优先级提高，待PM安排；不能以调试无关性夹具代替发布完整构建（本轮用户裁决）。

### 20.1 事前冻结的最终十项规则

1. ELF class、字节序、machine、e_flags相同。
2. SHF_ALLOC身份为节名、类型、COMDAT签名及SHF_LINK_ORDER目标的递归身份。按身份多重集合比较，逐身份比较flags/size/alignment/entsize/内容，NOBITS只比大小。
3. `.init_array/.fini_array/.preinit_array/.ctors/.dtors`及其点后缀、合法C标识符节名，分别按节名保持身份序列。
4. 同身份重复节保持内部顺序与内容。
5. 每一目标节内部重定位顺序相同，跨目标节/重定位节文件顺序不比较。比较offset/type/addend/规范符号身份；SECTION用节身份，LOCAL用名+所在节身份+值，其余用符号名。REL隐式addend由目标节原始字节相同比较覆盖，RELA显式比较。
6. 符号作为多重集合，比较全部非LOCAL及有名非`.L` LOCAL；排除SECTION/FILE、无名LOCAL、`.L` LOCAL、定义在.debug*的LOCAL以及仅由debug重定位引用的未定义符号。不豁免可加载节中的映射符号。
7. COMDAT组按签名/flags/有序成员身份多重集合，去掉debug及其重定位成员。
8. `.llvm_addrsig`的ULEB128索引解析成规范符号身份集合，排除第6项debug专用符号。
9. 发布产物无.debug*节。
10. 文件节顺序有变化时，用同一llvm-dis记录两路bitcode去调试信息后的函数/全局定义顺序；只诊断，不作门禁。直接非LTO对比也只诊断。

实现：`tools/check_release_debug_independence.py`。本轮没有另外增加豁免（用户本轮裁决；实现与测试）。

## 21. 比较器与夹具

原25项全部保留，新增16项，**41/41 PASS**；执行0.085s，scope peak 24,391,680 B，exit0（H/comparison-tests-scope/build.log、memory-summary.json）。本步骤无失败、未使用辅助缺陷重跑条款。

|新增固定ELF夹具|预期与实测|
|---|---|
|COMDAT节换序|PASS|
|普通非组节换序|PASS|
|同名.init_array两节换序|FAIL，被拒绝|
|同名C标识符节换序|FAIL，被拒绝|
|同身份重复节换序|FAIL，被拒绝|
|跨目标节重定位换序|PASS|
|同目标节内重定位换序|FAIL，被拒绝|
|SHF_LINK_ORDER目标不同|FAIL，被拒绝|
|e_flags不同|FAIL，被拒绝|
|debug内增加LOCAL映射符号|PASS|
|ALLOC中映射符号变化|FAIL，被拒绝|
|仅debug引用的未定义符号增加（含addrsig引用）|PASS|
|ALLOC引用的未定义符号变化|FAIL，被拒绝|
|addrsig集合变化|FAIL，被拒绝|
|addrsig仅索引/记录顺序变化|PASS|
|额外：LOCAL重定位目标值变化|FAIL，被拒绝|

旧夹具变化逐项：`test_alloc_order`由普通节反序FAIL改为PASS，落实第2项；`test_section_relocation_target_canonical_name`的预期由节名改为SECTION+完整身份，落实第5项；`test_comdat_debug_only_member_difference_passes`预期成员由节名改为完整身份，落实第7项。其余原测试语义保留；测试入口移到新增类之后保证命令行执行覆盖所有41项（H/tests-before.py与当前测试diff，H/comparison-tests-scope/build.log）。

## 22. 已有40对输入核对、逐项重判与顺序诊断

已有80个对象全部与上轮`archive-inspections.json`中的成员SHA和大小相符（H/forty-identities.json）。只读取已有对象，没有重新编译或转换。持共享锁执行，比较器为先行提交`78e58f5`中的版本。x86全部20对PASS；ARM32第13对失败即停止，剩余7对不继续；AArch64尚未启动。每项完整结果及规范语义JSON见H/physical-{x86_64,armv7l}/，身份摘要分别引用P与F的旧检查清单。

P=`temp/release-debug-independence-20261013`，F=`temp/release-contract-v2-20261013`。x86对象来自P/physical-x86_64/NN-comparison，ARM32对象来自F/physical-armv7l/NN-comparison（H/forty-identities.json）。

|序号（0起）|文件（相对LLVM源码根；首项为build生成源）|x86|ARM32|AArch64|
|---:|---|---|---|---|
|0|build/tools/clang/tools/extra/clangd/CompletionModel.cpp|PASS|PASS|NOT RUN|
|1|clang-tools-extra/clang-apply-replacements/lib/Tooling/ApplyReplacements.cpp|PASS|PASS|NOT RUN|
|2|clang-tools-extra/clang-change-namespace/ChangeNamespace.cpp|PASS|PASS|NOT RUN|
|3|clang-tools-extra/clang-doc/BitcodeReader.cpp|PASS|PASS|NOT RUN|
|4|clang-tools-extra/clang-doc/BitcodeWriter.cpp|PASS|PASS|NOT RUN|
|5|clang-tools-extra/clang-doc/ClangDoc.cpp|PASS|PASS|NOT RUN|
|6|clang-tools-extra/clang-doc/Generators.cpp|PASS|PASS|NOT RUN|
|7|clang-tools-extra/clang-doc/HTMLGenerator.cpp|PASS|PASS|NOT RUN|
|8|clang-tools-extra/clang-doc/JSONGenerator.cpp|PASS|PASS|NOT RUN|
|9|clang-tools-extra/clang-doc/MDGenerator.cpp|PASS|PASS|NOT RUN|
|10|clang-tools-extra/clang-doc/Mapper.cpp|PASS|PASS|NOT RUN|
|11|clang-tools-extra/clang-doc/Representation.cpp|PASS|PASS|NOT RUN|
|12|clang-tools-extra/clang-doc/Serialize.cpp|PASS|FAIL：内容/重定位/符号|NOT RUN|
|13|clang-tools-extra/clang-doc/YAMLGenerator.cpp|PASS|NOT RUN：前项停止|NOT RUN|
|14|clang-tools-extra/clang-doc/support/File.cpp|PASS|NOT RUN：前项停止|NOT RUN|
|15|clang-tools-extra/clang-include-fixer/FuzzySymbolIndex.cpp|PASS|NOT RUN：前项停止|NOT RUN|
|16|clang-tools-extra/clang-include-fixer/InMemorySymbolIndex.cpp|PASS|NOT RUN：前项停止|NOT RUN|
|17|clang-tools-extra/clang-include-fixer/IncludeFixer.cpp|PASS|NOT RUN：前项停止|NOT RUN|
|18|clang-tools-extra/clang-include-fixer/IncludeFixerContext.cpp|PASS|NOT RUN：前项停止|NOT RUN|
|19|clang-tools-extra/clang-include-fixer/SymbolIndexManager.cpp|PASS|NOT RUN：前项停止|NOT RUN|

### 22.1 存在先后变化的文件：ARM32 ChangeNamespace.cpp

本轮实际已判33对中，只有ARM32第02项的SHF_ALLOC身份序列变化。该项所有硬检查均PASS。x86所有20项和已判ARM32其余12项没有整体身份顺序变化（H/physical-*/comparisons.json）。

使用同一个`temp/arm-archive-standard-build-20261010/armv7l-tool-wrappers/llvm-dis`对两路原bitcode反汇编，命令、工具摘要、原bitcode SHA及输出分别归档；去掉调试元数据后提取定义先后。两路均853个定义（584个函数、269个全局），定义多重集合相同，18个定义的位置不同。**先后差异在转换之前已存在**；这只回答第10项诊断，不能证明任意代码差异无害（H/physical-armv7l/02-comparison/ir-order-diagnostic.json、debug.ll、release.ll、*-without-debug.ll）。

原bitcode身份：debug `4a30e0782bf78f144fd8ada443ab16e3fbabdde17eab7ee90447f0b78ce051c4`；release `79c1b6ad4d4e14b53c7c34e591a981a1e7195c7456fea4865df1c84a8cb1109f`，均对原转换before.json核对一致。36个ELF节移位的上轮观察保留于docs/49 §17，本轮按新合同重判此项PASS，不改写上轮FAIL。

### 22.2 与直接非LTO编译的对照：仅记录旧实测

未重新编译。沿用已保存直接对象比较记录：x8620项中10项结构摘要相同、10项不同；ARM32同为10/10。x86差异序号1/2/3/7/8/9/11/13/17/18；ARM32为1/2/3/6/7/8/9/11/12/13。此处“相同”是当时记录的节/符号/重定位类型统计相同，不是对象逐字节相同（P/physical-x86_64/direct-diagnostic.json、F/physical-armv7l/direct-diagnostic.json；docs/49 §17.3）。

标注：**预期差异：转换对已做链接前优化的bitcode再次完整优化**。这些诊断不能豁免本次debug/发布两份转换结果的内容差异。AArch64直接对照未执行。

## 23. 产品门禁停止：Serialize.cpp

第12号（第13个）`clang-tools-extra/clang-doc/Serialize.cpp`：两路各630个可加载节、2789条可加载节重定位、839个纳入比较的符号、276组、23个规范addrsig元素；发布侧无debug节。header、有序语义节、COMDAT、addrsig、无debug检查PASS；**alloc/relocations/symbols FAIL**（H/physical-armv7l/comparisons.json最后一项）。

同身份函数节：

```text
.text._ZN5clang3doc9serialize9serializeB5cxx11ERSt10unique_ptrINS0_4InfoESt14default_deleteIS3_EERNS_17DiagnosticsEngineE
```

|项目|debug转换对象|发布转换对象|
|---|---|---|
|节大小|720（0x2d0）|716（0x2cc）|
|节内容SHA256|e70591d0924e27c537ce79d521fb608d495ac6d12c16d014a63779ab31f7afce|be8669b2e9391b6aeec048b986514f7eb7f53a28fe97b869c1c2f7bb8d3ace67|
|全对象SHA256|b3d8e27c7874731d68626f273d0eb63bed128de9d8aa5aae73fd1a858fe5593a|cdee22b5eab6b97e64328f64c0ce386af817802e99ba93b7e9296c5df8a239f3|
|该节内重定位数|20|20（按位置比较20项全部不同）|
|GLOBAL函数符号size|720|716|
|该节的LOCAL映射符号value|$d=36、$t=46、$d=712|$d=32、$t=42、$d=708|

两路该函数符号均GLOBAL/FUNC/DEFAULT、value=1；不一致是size与节内容等实质门禁字段，并非符号表索引或debug专用符号（H/stop-readonly-retry/result.json与readelf输出）。

独立宿主`readelf -SW/-sW/-rW/-x <节名>`确认相同现象；全部argv和stdout/stderr见H/stop-readonly-retry/commands.json及同目录文本。节表原文：

```text
debug:
  [79] .text._ZN5clang3doc9serialize9serializeB5cxx11ERSt10unique_ptrINS0_4InfoESt14default_deleteIS3_EERNS_17DiagnosticsEngineE PROGBITS        00000000 000748 0002d0 00  AX  0   0  4
release:
  [79] .text._ZN5clang3doc9serialize9serializeB5cxx11ERSt10unique_ptrINS0_4InfoESt14default_deleteIS3_EERNS_17DiagnosticsEngineE PROGBITS        00000000 000748 0002cc 00  AX  0   0  4
```

**完整差异原文**：[alloc、逐目标节重定位、符号统一diff](49_arm32_serialize_debug_failure.diff)。H/arm32-12-{alloc,relocations,symbols}.diff为原始副本。没有将差异解释成通过，没有改Source、重编、转换或重新跑实物门禁；停止记录H/stop.json。

### 23.1 只读复核辅助脚本的一次修正

产品停止后只读readelf复核辅助脚本首次用子串筛节名，意外同时匹配`.ARM.extab.text.<函数>`，导致“恰一行”断言失败。原始输出明确有两行，但目标`.text.<函数>`行本身已显示720/716。按用户辅助缺陷条款，仅把匹配改为节表行的**完整节名**正则，并用新证据目录重跑只读复核一次；结果PASS。没有改比较器或任何门禁，也没有重跑已失败的对象比较（H/stop-readonly-scope/build.log、diagnose_stop-before.py、diagnostic-helper-fix.diff、stop-readonly-retry-scope/build.log）。完整修正diff：

```diff
--- before/diagnose_stop.py
+++ after/diagnose_stop.py
@@ -1,7 +1,7 @@
 from pathlib import Path
 import subprocess,json,hashlib,re,collections,difflib
 E=Path(__file__).resolve().parent;W=E.parent.parent;old=W/'temp/release-contract-v2-20261013/physical-armv7l/12-comparison'
-D=E/'stop-readonly';D.mkdir();commands=[];texts={};section='.text._ZN5clang3doc9serialize9serializeB5cxx11ERSt10unique_ptrINS0_4InfoESt14default_deleteIS3_EERNS_17DiagnosticsEngineE'
+D=E/'stop-readonly-retry';D.mkdir();commands=[];texts={};section='.text._ZN5clang3doc9serialize9serializeB5cxx11ERSt10unique_ptrINS0_4InfoESt14default_deleteIS3_EERNS_17DiagnosticsEngineE'
 for mode in ('debug','release'):
  p=old/(mode+'.o');texts[mode]={}
  for flag,label in [('-hW','header'),('-SW','sections'),('-sW','symbols'),('-rW','relocations'),('-x','payload')]:
@@ -9,7 +9,7 @@
   (D/(mode+'-'+label+'.txt')).write_text(r.stdout);(D/(mode+'-'+label+'.stderr')).write_text(r.stderr)
   commands.append(dict(argv=argv,exit=r.returncode));assert r.returncode==0;texts[mode][label]=r.stdout
 (D/'commands.json').write_text(json.dumps(commands,indent=2))
-lines={m:[l for l in texts[m]['sections'].splitlines() if section in l and '.rel.text.' not in l and '.ARM.exidx.' not in l] for m in texts}
+lines={m:[l for l in texts[m]['sections'].splitlines() if re.match(r'\s*\[\s*\d+\]\s+'+re.escape(section)+r'\s',l)] for m in texts}
 assert len(lines['debug'])==len(lines['release'])==1,lines
 assert re.search(r'\b0002d0\b',lines['debug'][0]) and re.search(r'\b0002cc\b',lines['release'][0]),lines
 for mode in texts:print(mode,lines[mode][0])
```

## 24. 资源、回收与后续边界

|阶段|准入实读GiB|wall秒|scope MemoryPeak字节|宿主最低可用GiB|结果|
|---|---:|---:|---:|---:|---|
|comparison-tests-scope|13.463959|2.117205|24391680|13.462036|exit 0|
|forty-rejudge-scope|13.429317|50.382718|311693312|13.426407|exit 1|
|stop-readonly-scope|13.436096|2.116972|41447424|13.435780|exit 1|
|stop-readonly-retry-scope|13.232105|2.166929|51253248|13.232105|exit 0|

均18GiB cap、MemorySwapMax=0、nice15/ionice3；memory.events的max/oom/oom_kill为0。本轮没有因资源不足中止。重判阶段共享锁等待/释放见H/forty-rejudge-scope/heavy-lock-{acquired,released}.json；各采样器与log reader均已回收（各scope/memory-summary.json）。

两把项目锁于2026-10-13T15:48:56+08:00释放，最终审计PASS：本任务残留进程0、根内挂载0、项目锁0，所有scope退出；本轮没有新挂载/proc。未操作BOLT目录（H/lock-released.json、cleanup-final.json、final-mountinfo.txt）。

|后续步骤|最终状态与原因|
|---|---|
|剩余ARM32 7对、AArch64 20对|NOT RUN，前项产品门禁失败|
|x86两次225档全量回归|NOT RUN，60对未全PASS；本轮x8620夹具PASS不代替全库|
|PS3/PS2再生成、顺序apply、整树检查|NOT RUN；候选仍docs/46旧版本|
|x86完整构建与验收1–7|全部NOT RUN，未创建新构建树|
|BOLT交接|**无新树可交接**，未写入虚假完成时间/缓存身份；不触碰其会话资产|
|两ARM全量、根内小试、64MiB负例|NOT RUN|
|bash债务清单、LLVM23探测|NOT RUN，严格依原顺序停止|
|升级手册与停止材料|本轮更新docs/48、docs/49与此续页、STATUS|
|发布模式完整构建|挂账，因未来Tizen-Base交付优先级提高，待PM安排|

## 25. 冻结身份与交付

两份Source和Commands没有修改，最终再次核对初始摘要一致（H/final-source-identity.json）：

|文件|SHA256|
|---|---|
|tools/llvm_static_archives_source.py|c43523c0ce04fc3310e670ff97823db8260c21250dc3172575a18db56500082e|
|tools/llvm_static_archives_arm_trial.py|1bac8db608554b35d16482711bf0667f1fbee8d60c6fc52f0f448d240ffaa9e4|
|tools/check_release_debug_independence.py|b857665a545bae399b5042e8e566629338226ba102c9b446065d297b9af02d77|
|tools/test_release_debug_independence.py|4e06246b00e367778931119864efd001102dac69a8ddc88c9eabe3cecfe28909|
|patches/archive-index-fix/ps3/0001-packaging-fix-llvm-static-devel-with-ThinLTO.patch|1293f6982c87cfbeefe91aa08e92a7d1b72a129f716417f8c8cee61693c463c6|
|patches/llvm-strip/ps2/0001-packaging-use-llvm-strip-for-x86_64-archives.patch|aab2cfd1ad3fb58bfe44cdbdda50bbe67d5343b29a6a6d598408d3bb96620e88|

比较器与41项夹具先行提交`78e58f5`并推送main；本收尾提交由`git log -- docs/49_release_contract_final.md`定位。所有原始脚本、命令/日志、对象语义JSON、差异、锁/资源/回收证据放H，不提交大文件。主docs/49旧§0–§19保持历史，续三§20链接到本页；两文均小于50,000字节。未推Gerrit。
