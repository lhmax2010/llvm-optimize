# 49 续四：发布模式参数认证与差异归因

日期：2026-10-13；开场HEAD `df729697426dff67a3871bfa850754ee8be7d376`。**最终状态：STOP_DISK_ADMISSION；补充裁决复查SKIP_FULL_BUILD_DISK_FLOOR（§9）。发布认证60/60 PASS（53相同、7对/20函数由(b)归因）；两次x86全量回归PASS；新PS3/PS2 apply/tree PASS。完整构建与后续步骤未执行，无BOLT新树交接。** 旧docs/49及续三保留，十项ELF比较器和两份Source/Commands不修改。本页不超过50KB。

## 1. 用户裁决、完整性与执行边界

本轮PM判断：Serialize.cpp debug版多4字节属于LLVM自身debug/nondebug代码生成差异，非转换逻辑引入；本任务将该判断登记为人工裁决，并用opt去调试信息、llvm-diff与必要的后端再转换验证归因，不把裁决冒充新实测。发布模式改为“参数一致+差异归因”，不再要求所有产物字节相同；归因FAIL仅停止发布认证线，debug主线仍按原顺序继续（本轮用户指令）。

参数硬门禁：规范化明确的输入/输出路径后，debug命令只允许少`-g`、`-gdwarf-4`；其他token及顺序必须一致，clang实体SHA、cwd、环境集合相同。调试集合来自生产Source的BACKEND_FLAGS及ir_settings无调试分支、ARM对应分支（tools/llvm_static_archives_source.py:176、360；tools/llvm_static_archives_arm_trial.py:945）。不通配忽略其他-g开关。

十项产物比较保持原样。差异必须仅在被归因函数的节、节内重定位、映射符号、函数size；其余仍完全通过十项规则。优先(a)：同版opt --strip-debug后llvm-diff证实相关函数IR已不同；否则(b)：去debug后的debug bitcode用原发布命令再转换，被归因函数必须与发布产物一致。两者不成立则FAIL。逐差异函数保存objdump第一处指令差异周围原文，最多40行（本轮用户指令；tools/check_release_attribution.py）。

证据目录 E=`temp/release-attribution-20261013`。初始Source/补丁/spec/config与上轮冻结SHA一致，十项比较器与测试均同HEAD；工作树仅既有用户gbs_llvm.conf修改（E/initial-integrity.json）。双项目锁覆盖任务；重阶段共享heavy-stage.lock以flock排队最长2h。沿用docs/49 §1：轻/重准入6/10GiB，等待5min最长60min；18GiB cap、swap0、nice15/ionice3、30s采样、宿主可用<2GiB中止。不访问BOLT资产，不清理磁盘，不推Gerrit。

宿主恢复命令仍为`sudo sysctl -w vm.mmap_min_addr=65536`，重启也会恢复；本任务不恢复，/proc仅按需临时挂载并卸载。

## 2. 独立辅助与测试

新增`tools/check_release_attribution.py`、`tools/test_release_attribution.py`；16/16 PASS（E/attribution-tests-scope/build.log，0.004s）。原十项比较器不改。

|夹具|预期/实测|
|---|---|
|只差两调试token|PASS|
|增加非debug token|FAIL，拒绝|
|删除非debug token|FAIL，拒绝|
|改变非debug token|FAIL，拒绝|
|非debug换序|FAIL，拒绝|
|clang实体SHA不同|FAIL，拒绝|
|环境身份不同|FAIL，拒绝|
|cwd不同|FAIL，拒绝|
|额外-gline-tables-only|FAIL，拒绝|
|输入阶段(a)|已归因PASS|
|后端阶段(b)|已归因PASS|
|函数外差异|FAIL，拒绝|
|(a)(b)均不成立|FAIL，拒绝|
|函数binding变化|FAIL，拒绝|
|其他节映射符号变化|FAIL，拒绝|
|llvm-diff函数标题、异常/缺函数|只接受指定函数有效差异，错误拒绝|

## 3. 实物执行

### 3.1 已有33对与Serialize.cpp

参数33/33 PASS：x86 20、ARM32 13。32对十项产物比较PASS；Serialize.cpp为已归因PASS(b)。两路仅差`-g -gdwarf-4`，其余参数及次序一致，clang实体SHA一致。历史转换未逐次快照环境值；cwd/环境相同的依据是同一父进程中两次转换继承同一环境、驱动与Source未修改cwd/环境，而非事后虚构历史环境快照（E/first33-retry/*/*/parameters.json）。

Serialize.cpp去调试信息后的指定函数llvm-diff exit=0、输出为空，不能认定(a)。去debug后的debug bitcode按原发布命令（仅换输入/输出）再转换exit0，0.504372s、VmHWM 91,276KiB；与发布产物对应函数节、节内重定位、函数及映射符号完全一致。除该函数的节/重定位/映射符号/函数size外，十项规则全部PASS。原函数debug720B、release716B，本轮实测支持“调试信息进入后端引起差异”，没有修改两Source、Commands或十项比较器（E/first33-result.json，E/first33-retry/armv7l/12/*）。

第一处指令差异周围原文（两路合计36行；完整反汇编与diff在同目录）：


debug：
```text
00000000 <_ZN5clang3doc9serialize9serializeB5cxx11ERSt10unique_ptrINS0_4InfoESt14default_deleteIS3_EERNS_17DiagnosticsEngineE>:
       0: e92d 41f0    	push.w	{r4, r5, r6, r7, r8, lr}
       4: f6ad 1d18    	subw	sp, sp, #0x918
       8: 4604         	mov	r4, r0
       a: 48af         	ldr	r0, [pc, #0x2bc]        @ 0x2c8 <_ZN5clang3doc9serialize9serializeB5cxx11ERSt10unique_ptrINS0_4InfoESt14default_deleteIS3_EERNS_17DiagnosticsEngineE+0x2c8>
       c: 4478         	add	r0, pc
       e: 6800         	ldr	r0, [r0]
      10: 6800         	ldr	r0, [r0]
      12: f8cd 0914    	str.w	r0, [sp, #0x914]
      16: 680d         	ldr	r5, [r1]
      18: f8d5 04dc    	ldr.w	r0, [r5, #0x4dc]
      1c: f20f 0104    	adr.w	r1, #4
      20: e8df f000    	tbb	[pc, r0]
      24: 05 f2 c4 3a  	.word	0x3ac4f205
      28: 68 05 0c 96  	.word	0x960c0568
      2c: 05 00        	.short	0x0005
      2e: 2000         	movs	r0, #0x0
      30: 4621         	mov	r1, r4
```

release：
```text
00000000 <_ZN5clang3doc9serialize9serializeB5cxx11ERSt10unique_ptrINS0_4InfoESt14default_deleteIS3_EERNS_17DiagnosticsEngineE>:
       0: e92d 41f0    	push.w	{r4, r5, r6, r7, r8, lr}
       4: f6ad 1d18    	subw	sp, sp, #0x918
       8: 4604         	mov	r4, r0
       a: 48ae         	ldr	r0, [pc, #0x2b8]        @ 0x2c4 <_ZN5clang3doc9serialize9serializeB5cxx11ERSt10unique_ptrINS0_4InfoESt14default_deleteIS3_EERNS_17DiagnosticsEngineE+0x2c4>
       c: 4478         	add	r0, pc
       e: 6800         	ldr	r0, [r0]
      10: 6800         	ldr	r0, [r0]
      12: f8cd 0914    	str.w	r0, [sp, #0x914]
      16: 680d         	ldr	r5, [r1]
      18: f8d5 04dc    	ldr.w	r0, [r5, #0x4dc]
      1c: e8df f000    	tbb	[pc, r0]
      20: 05 f2 c4 3a  	.word	0x3ac4f205
      24: 68 05 0c 96  	.word	0x960c0568
      28: 05 00        	.short	0x0005
      2a: 2000         	movs	r0, #0x0
      2c: 4621         	mov	r1, r4
      2e: f801 0f08    	strb	r0, [r1, #8]!
```

### 3.2 一次辅助路径修正

首次实物驱动在opt执行前失败：引用了Source完成转换后已删除的临时`members/fixture.a/00012/input.bc`。只读核查发现原始输入副本仍在`physical-armv7l/{debug,release}-input/members/12.o`，SHA与before.json完全一致（debug `e3f1f129fa94f8d9ed8cbed5d1cf1b1618ebf0075a16d09aa3efda83a267bfac`，release `160f7682ca2dd05f402c51a1ce4e7a875837e3901fa39668a1d12559adf4bc81`）。按授权只修输入定位，门禁与参数不改；本步骤唯一一次重跑PASS。证据E/input-path-fix-proof.json、input-path-helper-fix.diff；首次和重跑日志均保留。第一次共享锁等待约752s，重跑scope峰662,466,560B，swap0/18GiB上限，无OOM（E/first33-scope、first33-retry-scope）。

ARM32余7对全部相同PASS；AArch64结果见§4。


## 4. 三架构60对发布模式认证

本轮发布认证 **PASS**：参数60/60 PASS；状态计数`{'PASS_ATTRIBUTED': 7, 'PASS_IDENTICAL': 53}`。该结论只覆盖选定60成员的参数及差异归因，不等于发布模式完整构建认证。Source与Commands不变（E/release-status.json）。

|序号|源文件|x86|ARM32|AArch64|
|---:|---|---|---|---|
|0|`build/tools/clang/tools/extra/clangd/CompletionModel.cpp`|相同PASS|相同PASS|相同PASS|
|1|`clang-tools-extra/clang-apply-replacements/lib/Tooling/ApplyReplacements.cpp`|相同PASS|相同PASS|已归因PASS(b)|
|2|`clang-tools-extra/clang-change-namespace/ChangeNamespace.cpp`|相同PASS|相同PASS|已归因PASS(b)|
|3|`clang-tools-extra/clang-doc/BitcodeReader.cpp`|相同PASS|相同PASS|已归因PASS(b)|
|4|`clang-tools-extra/clang-doc/BitcodeWriter.cpp`|相同PASS|相同PASS|相同PASS|
|5|`clang-tools-extra/clang-doc/ClangDoc.cpp`|相同PASS|相同PASS|相同PASS|
|6|`clang-tools-extra/clang-doc/Generators.cpp`|相同PASS|相同PASS|相同PASS|
|7|`clang-tools-extra/clang-doc/HTMLGenerator.cpp`|相同PASS|相同PASS|相同PASS|
|8|`clang-tools-extra/clang-doc/JSONGenerator.cpp`|相同PASS|相同PASS|相同PASS|
|9|`clang-tools-extra/clang-doc/MDGenerator.cpp`|相同PASS|相同PASS|相同PASS|
|10|`clang-tools-extra/clang-doc/Mapper.cpp`|相同PASS|相同PASS|相同PASS|
|11|`clang-tools-extra/clang-doc/Representation.cpp`|相同PASS|相同PASS|已归因PASS(b)|
|12|`clang-tools-extra/clang-doc/Serialize.cpp`|相同PASS|已归因PASS(b)|已归因PASS(b)|
|13|`clang-tools-extra/clang-doc/YAMLGenerator.cpp`|相同PASS|相同PASS|相同PASS|
|14|`clang-tools-extra/clang-doc/support/File.cpp`|相同PASS|相同PASS|相同PASS|
|15|`clang-tools-extra/clang-include-fixer/FuzzySymbolIndex.cpp`|相同PASS|相同PASS|相同PASS|
|16|`clang-tools-extra/clang-include-fixer/InMemorySymbolIndex.cpp`|相同PASS|相同PASS|相同PASS|
|17|`clang-tools-extra/clang-include-fixer/IncludeFixer.cpp`|相同PASS|相同PASS|已归因PASS(b)|
|18|`clang-tools-extra/clang-include-fixer/IncludeFixerContext.cpp`|相同PASS|相同PASS|相同PASS|
|19|`clang-tools-extra/clang-include-fixer/SymbolIndexManager.cpp`|相同PASS|相同PASS|相同PASS|

所有参数仅去掉固定集合`-g`、`-gdwarf-4`，其余参数顺序保持不变。x86与ARM32历史两路在同一父进程循环中继承cwd/环境（代码与SHA证据，未声称持有历史环境原始快照）；新AArch64两次转换另记录cwd与完整环境键值集合的SHA，未把敏感环境值写入报告（E/physical-aarch64/conversion-contexts.json）。

### 4.1 工具身份

以下工具全部22.1.8；仅用于opt去debug、llvm-diff及反汇编，未替换原架构转换编译器（E/diagnostic-tools-retry/identity.json）。

|工具|绝对路径|SHA256|
|---|---|---|
|opt|`/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/opt`|`c842412e6854a534898139eb24b2769b00284502f900a3af13f2f21d02848322`|
|llvm-diff|`/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-diff`|`227c137b0ae007eb4be57c5a788f0e7ad34ea6f6a3415af4cf9cc164460bda05`|
|llvm-objdump|`/home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-objdump`|`a9448cb80dd2464ee55762f2d741459f39138c84a4b68d5f328ae71df2568daa`|

### 4.2 AArch64过程与顺序诊断

R64以原编译命令分别生成debug/release/native共60对象；两路bitcode均保持ThinLTO，native仅去掉ThinLTO、只作诊断。两路各20成员转换与完整索引PASS，发布路无debug节；临时proc挂载及卸载均exit0（E/physical-aarch64/commands.json，根内generation.json，archive-inspections.json）。
节顺序变化清单（不据此豁免内容差异）：
- armv7l `clang-tools-extra/clang-change-namespace/ChangeNamespace.cpp`；沿用同SHA输入的H/physical-armv7l/02-comparison/ir-order-diagnostic.json：853定义、584函数、269全局，18个定义位置变化，变化已存在于转换前（docs/49_release_contract_final.md §22.1）。

### 4.3 直接非LTO对照（仅诊断）

“预期差异：转换对已做链接前优化的bitcode再次完整优化”。以下统计使用既有同一describe/differences方法；不要求字节相同、不作通过门禁。

|架构|结构记录相同|有结构差异|证据|
|---|---:|---:|---|
|x86_64|10|10|`temp/release-debug-independence-20261013/physical-x86_64/direct-diagnostic.json`|
|armv7l|10|10|`temp/release-contract-v2-20261013/physical-armv7l/direct-diagnostic.json`|
|aarch64|9|11|`temp/release-attribution-20261013/physical-aarch64/direct-diagnostic.json`|


### 4.4 AArch64差异逐函数归因与反汇编

AArch64有6文件、19函数出现内容差异。19次指定函数llvm-diff均exit0、输出为空；各文件去debug后的debug bitcode用原发布命令再转换，对应函数十项规则全部相同，均由后端路径(b)归因。所有函数外差异门禁PASS。以下每函数两路合计不超过16行；原文完整命令、stderr、反汇编、差异和重转对象在E/aarch64-evaluation/NN/。没有据经验放行任何额外差异。

#### 1 ApplyReplacements.cpp

llvm-diff（每个下列函数）：exit=0，stdout/stderr为空；归因(b) PASS。后端重转wall 0.4023422930040397秒、RSS 481252KiB。

函数`_ZN4llvm12handleErrorsIJZNS_12consumeErrorENS_5ErrorEEUlRKNS_13ErrorInfoBaseEE_EEES1_S1_DpOT_`：
debug：
```text
     128: d63f0100     	blr	x8
     12c: 36000160     	tbz	w0, #0x0, 0x158 <_ZN4llvm12handleErrorsIJZNS_12consumeErrorENS_5ErrorEEUlRKNS_13ErrorInfoBaseEE_EEES1_S1_DpOT_+0x158>
     130: f9400288     	ldr	x8, [x20]
     134: aa1403e0     	mov	x0, x20
     138: f900027f     	str	xzr, [x19]
     13c: f9400501     	ldr	x1, [x8, #0x8]
     140: a9454ff4     	ldp	x20, x19, [sp, #0x50]
     144: a94457f6     	ldp	x22, x21, [sp, #0x40]
```
release：
```text
     128: d63f0100     	blr	x8
     12c: 36000160     	tbz	w0, #0x0, 0x158 <_ZN4llvm12handleErrorsIJZNS_12consumeErrorENS_5ErrorEEUlRKNS_13ErrorInfoBaseEE_EEES1_S1_DpOT_+0x158>
     130: f9400288     	ldr	x8, [x20]
     134: aa1403e0     	mov	x0, x20
     138: f9400501     	ldr	x1, [x8, #0x8]
     13c: f900027f     	str	xzr, [x19]
     140: a9454ff4     	ldp	x20, x19, [sp, #0x50]
     144: a94457f6     	ldp	x22, x21, [sp, #0x40]
```
#### 2 ChangeNamespace.cpp

llvm-diff（每个下列函数）：exit=0，stdout/stderr为空；归因(b) PASS。后端重转wall 0.9031715210294351秒、RSS 481252KiB。

函数`_ZN4llvm12handleErrorsIJZNS_12consumeErrorENS_5ErrorEEUlRKNS_13ErrorInfoBaseEE_EEES1_S1_DpOT_`：
debug：
```text
     128: d63f0100     	blr	x8
     12c: 36000160     	tbz	w0, #0x0, 0x158 <_ZN4llvm12handleErrorsIJZNS_12consumeErrorENS_5ErrorEEUlRKNS_13ErrorInfoBaseEE_EEES1_S1_DpOT_+0x158>
     130: f9400288     	ldr	x8, [x20]
     134: aa1403e0     	mov	x0, x20
     138: f900027f     	str	xzr, [x19]
     13c: f9400501     	ldr	x1, [x8, #0x8]
     140: a9454ff4     	ldp	x20, x19, [sp, #0x50]
     144: a94457f6     	ldp	x22, x21, [sp, #0x40]
```
release：
```text
     128: d63f0100     	blr	x8
     12c: 36000160     	tbz	w0, #0x0, 0x158 <_ZN4llvm12handleErrorsIJZNS_12consumeErrorENS_5ErrorEEUlRKNS_13ErrorInfoBaseEE_EEES1_S1_DpOT_+0x158>
     130: f9400288     	ldr	x8, [x20]
     134: aa1403e0     	mov	x0, x20
     138: f9400501     	ldr	x1, [x8, #0x8]
     13c: f900027f     	str	xzr, [x19]
     140: a9454ff4     	ldp	x20, x19, [sp, #0x50]
     144: a94457f6     	ldp	x22, x21, [sp, #0x40]
```
#### 3 BitcodeReader.cpp

llvm-diff（每个下列函数）：exit=0，stdout/stderr为空；归因(b) PASS。后端重转wall 1.7568218999658711秒、RSS 481252KiB。

函数`_ZN4llvm15SmallVectorImplIN5clang3doc13EnumValueInfoEE12emplace_backIJS3_EEERS3_DpOT_`：
debug：
```text
      c4: b9400a68     	ldr	w8, [x19, #0x8]
      c8: f9400269     	ldr	x9, [x19]
      cc: 11000508     	add	w8, w8, #0x1
      d0: 9baa2509     	umaddl	x9, w8, w10, x9
      d4: b9000a68     	str	w8, [x19, #0x8]
      d8: d1024120     	sub	x0, x9, #0x90
      dc: a9434ff4     	ldp	x20, x19, [sp, #0x30]
      e0: f94013f5     	ldr	x21, [sp, #0x20]
```
release：
```text
      c4: b9400a68     	ldr	w8, [x19, #0x8]
      c8: f9400269     	ldr	x9, [x19]
      cc: 11000508     	add	w8, w8, #0x1
      d0: 9baa2509     	umaddl	x9, w8, w10, x9
      d4: d1024120     	sub	x0, x9, #0x90
      d8: b9000a68     	str	w8, [x19, #0x8]
      dc: a9434ff4     	ldp	x20, x19, [sp, #0x30]
      e0: f94013f5     	ldr	x21, [sp, #0x20]
```

函数`_ZN4llvm15SmallVectorImplIN5clang3doc8LocationEE12emplace_backIJiiRNS_9StringRefEbEEERS3_DpOT_`：
debug：
```text
      b4: 39010299     	strb	w25, [x20, #0x40]
      b8: 11000529     	add	w9, w9, #0x1
      bc: f9000688     	str	x8, [x20, #0x8]
      c0: 9bab292a     	umaddl	x10, w9, w11, x10
      c4: b9000a69     	str	w9, [x19, #0x8]
      c8: d1012140     	sub	x0, x10, #0x48
      cc: a9444ff4     	ldp	x20, x19, [sp, #0x40]
      d0: a94357f6     	ldp	x22, x21, [sp, #0x30]
```
release：
```text
      b4: 39010299     	strb	w25, [x20, #0x40]
      b8: 11000529     	add	w9, w9, #0x1
      bc: f9000688     	str	x8, [x20, #0x8]
      c0: 9bab292a     	umaddl	x10, w9, w11, x10
      c4: d1012140     	sub	x0, x10, #0x48
      c8: b9000a69     	str	w9, [x19, #0x8]
      cc: a9444ff4     	ldp	x20, x19, [sp, #0x40]
      d0: a94357f6     	ldp	x22, x21, [sp, #0x30]
```

函数`_ZN4llvm15SmallVectorImplIN5clang3doc9ReferenceEE12emplace_backIJS3_EEERS3_DpOT_`：
debug：
```text
      e8: 5280250a     	mov	w10, #0x128             // =296
      ec: f9400269     	ldr	x9, [x19]
      f0: 11000508     	add	w8, w8, #0x1
      f4: 9baa2509     	umaddl	x9, w8, w10, x9
      f8: b9000a68     	str	w8, [x19, #0x8]
      fc: d104a120     	sub	x0, x9, #0x128
     100: a9434ff4     	ldp	x20, x19, [sp, #0x30]
     104: f94013f5     	ldr	x21, [sp, #0x20]
```
release：
```text
      e8: 5280250a     	mov	w10, #0x128             // =296
      ec: f9400269     	ldr	x9, [x19]
      f0: 11000508     	add	w8, w8, #0x1
      f4: 9baa2509     	umaddl	x9, w8, w10, x9
      f8: d104a120     	sub	x0, x9, #0x128
      fc: b9000a68     	str	w8, [x19, #0x8]
     100: a9434ff4     	ldp	x20, x19, [sp, #0x30]
     104: f94013f5     	ldr	x21, [sp, #0x20]
```

函数`_ZN4llvm23SmallVectorTemplateBaseIN5clang3doc13EnumValueInfoELb0EE18growAndEmplaceBackIJS3_EEERS3_DpOT_`：
debug：
```text
      f8: 52801209     	mov	w9, #0x90               // =144
      fc: f9000274     	str	x20, [x19]
     100: 11000508     	add	w8, w8, #0x1
     104: 9ba95109     	umaddl	x9, w8, w9, x20
     108: 29015668     	stp	w8, w21, [x19, #0x8]
     10c: d1024120     	sub	x0, x9, #0x90
     110: a9444ff4     	ldp	x20, x19, [sp, #0x40]
     114: a94357f6     	ldp	x22, x21, [sp, #0x30]
```
release：
```text
      f8: 52801209     	mov	w9, #0x90               // =144
      fc: f9000274     	str	x20, [x19]
     100: 11000508     	add	w8, w8, #0x1
     104: 9ba95109     	umaddl	x9, w8, w9, x20
     108: d1024120     	sub	x0, x9, #0x90
     10c: 29015668     	stp	w8, w21, [x19, #0x8]
     110: a9444ff4     	ldp	x20, x19, [sp, #0x40]
     114: a94357f6     	ldp	x22, x21, [sp, #0x30]
```

函数`_ZN4llvm23SmallVectorTemplateBaseIN5clang3doc13FieldTypeInfoELb0EE18growAndEmplaceBackIJS3_EEERS3_DpOT_`：
debug：
```text
      c0: b9400a68     	ldr	w8, [x19, #0x8]
      c4: f9000274     	str	x20, [x19]
      c8: 11000508     	add	w8, w8, #0x1
      cc: 9bb65109     	umaddl	x9, w8, w22, x20
      d0: 29015668     	stp	w8, w21, [x19, #0x8]
      d4: d1060120     	sub	x0, x9, #0x180
      d8: a9444ff4     	ldp	x20, x19, [sp, #0x40]
      dc: a94357f6     	ldp	x22, x21, [sp, #0x30]
```
release：
```text
      c0: b9400a68     	ldr	w8, [x19, #0x8]
      c4: f9000274     	str	x20, [x19]
      c8: 11000508     	add	w8, w8, #0x1
      cc: 9bb65109     	umaddl	x9, w8, w22, x20
      d0: d1060120     	sub	x0, x9, #0x180
      d4: 29015668     	stp	w8, w21, [x19, #0x8]
      d8: a9444ff4     	ldp	x20, x19, [sp, #0x40]
      dc: a94357f6     	ldp	x22, x21, [sp, #0x30]
```

函数`_ZN4llvm23SmallVectorTemplateBaseIN5clang3doc14MemberTypeInfoELb0EE18growAndEmplaceBackIJS3_EEERS3_DpOT_`：
debug：
```text
     120: 52803409     	mov	w9, #0x1a0              // =416
     124: f9000274     	str	x20, [x19]
     128: 11000508     	add	w8, w8, #0x1
     12c: 9ba95109     	umaddl	x9, w8, w9, x20
     130: 29015a68     	stp	w8, w22, [x19, #0x8]
     134: d1068120     	sub	x0, x9, #0x1a0
     138: a9444ff4     	ldp	x20, x19, [sp, #0x40]
     13c: a94357f6     	ldp	x22, x21, [sp, #0x30]
```
release：
```text
     120: 52803409     	mov	w9, #0x1a0              // =416
     124: f9000274     	str	x20, [x19]
     128: 11000508     	add	w8, w8, #0x1
     12c: 9ba95109     	umaddl	x9, w8, w9, x20
     130: d1068120     	sub	x0, x9, #0x1a0
     134: 29015a68     	stp	w8, w22, [x19, #0x8]
     138: a9444ff4     	ldp	x20, x19, [sp, #0x40]
     13c: a94357f6     	ldp	x22, x21, [sp, #0x30]
```

函数`_ZN4llvm23SmallVectorTemplateBaseIN5clang3doc8LocationELb0EE18growAndEmplaceBackIJiiRNS_9StringRefEbEEERS3_DpOT_`：
debug：
```text
     1a0: 52800909     	mov	w9, #0x48               // =72
     1a4: f9000274     	str	x20, [x19]
     1a8: 11000508     	add	w8, w8, #0x1
     1ac: 9ba95109     	umaddl	x9, w8, w9, x20
     1b0: 29015a68     	stp	w8, w22, [x19, #0x8]
     1b4: d1012120     	sub	x0, x9, #0x48
     1b8: a9474ff4     	ldp	x20, x19, [sp, #0x70]
     1bc: a94657f6     	ldp	x22, x21, [sp, #0x60]
```
release：
```text
     1a0: 52800909     	mov	w9, #0x48               // =72
     1a4: f9000274     	str	x20, [x19]
     1a8: 11000508     	add	w8, w8, #0x1
     1ac: 9ba95109     	umaddl	x9, w8, w9, x20
     1b0: d1012120     	sub	x0, x9, #0x48
     1b4: 29015a68     	stp	w8, w22, [x19, #0x8]
     1b8: a9474ff4     	ldp	x20, x19, [sp, #0x70]
     1bc: a94657f6     	ldp	x22, x21, [sp, #0x60]
```

函数`_ZN4llvm23SmallVectorTemplateBaseIN5clang3doc9ReferenceELb0EE18growAndEmplaceBackIJS3_EEERS3_DpOT_`：
debug：
```text
     11c: 52802509     	mov	w9, #0x128              // =296
     120: f9000274     	str	x20, [x19]
     124: 11000508     	add	w8, w8, #0x1
     128: 9ba95109     	umaddl	x9, w8, w9, x20
     12c: 29015668     	stp	w8, w21, [x19, #0x8]
     130: d104a120     	sub	x0, x9, #0x128
     134: a9444ff4     	ldp	x20, x19, [sp, #0x40]
     138: a94357f6     	ldp	x22, x21, [sp, #0x30]
```
release：
```text
     11c: 52802509     	mov	w9, #0x128              // =296
     120: f9000274     	str	x20, [x19]
     124: 11000508     	add	w8, w8, #0x1
     128: 9ba95109     	umaddl	x9, w8, w9, x20
     12c: d104a120     	sub	x0, x9, #0x128
     130: 29015668     	stp	w8, w21, [x19, #0x8]
     134: a9444ff4     	ldp	x20, x19, [sp, #0x40]
     138: a94357f6     	ldp	x22, x21, [sp, #0x30]
```

函数`_ZN5clang3docL11addTypeInfoIPNS0_11TypedefInfoENS0_8TypeInfoEEEN4llvm5ErrorET_OT0_`：
debug：
```text
      50: 913c6280     	add	x0, x20, #0xf18
      54: 91040261     	add	x1, x19, #0x100
      58: 94000000     	bl	0x58 <_ZN5clang3docL11addTypeInfoIPNS0_11TypedefInfoENS0_8TypeInfoEEEN4llvm5ErrorET_OT0_+0x58>
      5c: 79425268     	ldrh	w8, [x19, #0x128]
      60: f90002bf     	str	xzr, [x21]
      64: 791e8288     	strh	w8, [x20, #0xf40]
      68: a9424ff4     	ldp	x20, x19, [sp, #0x20]
      6c: f9400bf5     	ldr	x21, [sp, #0x10]
```
release：
```text
      50: 913c6280     	add	x0, x20, #0xf18
      54: 91040261     	add	x1, x19, #0x100
      58: 94000000     	bl	0x58 <_ZN5clang3docL11addTypeInfoIPNS0_11TypedefInfoENS0_8TypeInfoEEEN4llvm5ErrorET_OT0_+0x58>
      5c: 79425268     	ldrh	w8, [x19, #0x128]
      60: 791e8288     	strh	w8, [x20, #0xf40]
      64: f90002bf     	str	xzr, [x21]
      68: a9424ff4     	ldp	x20, x19, [sp, #0x20]
      6c: f9400bf5     	ldr	x21, [sp, #0x10]
```

函数`_ZN5clang3docL11addTypeInfoIPNS0_12FunctionInfoENS0_8TypeInfoEEEN4llvm5ErrorET_OT0_`：
debug：
```text
      50: 91040261     	add	x1, x19, #0x100
      54: 8b080280     	add	x0, x20, x8
      58: 94000000     	bl	0x58 <_ZN5clang3docL11addTypeInfoIPNS0_12FunctionInfoENS0_8TypeInfoEEEN4llvm5ErrorET_OT0_+0x58>
      5c: 79425268     	ldrh	w8, [x19, #0x128]
      60: f90002bf     	str	xzr, [x21]
      64: 7920d288     	strh	w8, [x20, #0x1068]
      68: a9424ff4     	ldp	x20, x19, [sp, #0x20]
      6c: f9400bf5     	ldr	x21, [sp, #0x10]
```
release：
```text
      50: 91040261     	add	x1, x19, #0x100
      54: 8b080280     	add	x0, x20, x8
      58: 94000000     	bl	0x58 <_ZN5clang3docL11addTypeInfoIPNS0_12FunctionInfoENS0_8TypeInfoEEEN4llvm5ErrorET_OT0_+0x58>
      5c: 79425268     	ldrh	w8, [x19, #0x128]
      60: 7920d288     	strh	w8, [x20, #0x1068]
      64: f90002bf     	str	xzr, [x21]
      68: a9424ff4     	ldp	x20, x19, [sp, #0x20]
      6c: f9400bf5     	ldr	x21, [sp, #0x10]
```

函数`_ZN5clang3docL11addTypeInfoIPNS0_7VarInfoENS0_8TypeInfoEEEN4llvm5ErrorET_OT0_`：
debug：
```text
      50: 913c6280     	add	x0, x20, #0xf18
      54: 91040261     	add	x1, x19, #0x100
      58: 94000000     	bl	0x58 <_ZN5clang3docL11addTypeInfoIPNS0_7VarInfoENS0_8TypeInfoEEEN4llvm5ErrorET_OT0_+0x58>
      5c: 79425268     	ldrh	w8, [x19, #0x128]
      60: f90002bf     	str	xzr, [x21]
      64: 791e8288     	strh	w8, [x20, #0xf40]
      68: a9424ff4     	ldp	x20, x19, [sp, #0x20]
      6c: f9400bf5     	ldr	x21, [sp, #0x10]
```
release：
```text
      50: 913c6280     	add	x0, x20, #0xf18
      54: 91040261     	add	x1, x19, #0x100
      58: 94000000     	bl	0x58 <_ZN5clang3docL11addTypeInfoIPNS0_7VarInfoENS0_8TypeInfoEEEN4llvm5ErrorET_OT0_+0x58>
      5c: 79425268     	ldrh	w8, [x19, #0x128]
      60: 791e8288     	strh	w8, [x20, #0xf40]
      64: f90002bf     	str	xzr, [x21]
      68: a9424ff4     	ldp	x20, x19, [sp, #0x20]
      6c: f9400bf5     	ldr	x21, [sp, #0x10]
```
#### 11 Representation.cpp

llvm-diff（每个下列函数）：exit=0，stdout/stderr为空；归因(b) PASS。后端重转wall 0.7531663629924878秒、RSS 481252KiB。

函数`_ZSt21__unguarded_partitionIN9__gnu_cxx17__normal_iteratorIPN5clang3doc11CommentInfoESt6vectorIS4_SaIS4_EEEENS0_5__ops15_Iter_less_iterEET_SC_SC_SC_T0_`：
debug：
```text
      e4: a94327ea     	ldp	x10, x9, [sp, #0x30]
      e8: a908a7ea     	stp	x10, x9, [sp, #0x88]
      ec: a94427ea     	ldp	x10, x9, [sp, #0x40]
      f0: a909a7ea     	stp	x10, x9, [sp, #0x98]
      f4: a9452beb     	ldp	x11, x10, [sp, #0x50]
      f8: f94033e9     	ldr	x9, [sp, #0x60]
      fc: a90aabeb     	stp	x11, x10, [sp, #0xa8]
     100: b940013a     	ldr	w26, [x9]
```
release：
```text
      e4: a94327ea     	ldp	x10, x9, [sp, #0x30]
      e8: a908a7ea     	stp	x10, x9, [sp, #0x88]
      ec: a94427ea     	ldp	x10, x9, [sp, #0x40]
      f0: a909a7ea     	stp	x10, x9, [sp, #0x98]
      f4: f94033e9     	ldr	x9, [sp, #0x60]
      f8: a9452beb     	ldp	x11, x10, [sp, #0x50]
      fc: b940013a     	ldr	w26, [x9]
     100: a90aabeb     	stp	x11, x10, [sp, #0xa8]
```
#### 12 Serialize.cpp

llvm-diff（每个下列函数）：exit=0，stdout/stderr为空；归因(b) PASS。后端重转wall 0.7529030889854766秒、RSS 481252KiB。

函数`_ZN4llvm23SmallVectorTemplateBaseIN5clang3doc13EnumValueInfoELb0EE18growAndEmplaceBackIJNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEENS_9StringRefERSB_EEERS3_DpOT_`：
debug：
```text
      80: b9400a68     	ldr	w8, [x19, #0x8]
      84: f9000274     	str	x20, [x19]
      88: 11000508     	add	w8, w8, #0x1
      8c: 9bb85109     	umaddl	x9, w8, w24, x20
      90: 29015668     	stp	w8, w21, [x19, #0x8]
      94: d1024120     	sub	x0, x9, #0x90
      98: a9444ff4     	ldp	x20, x19, [sp, #0x40]
      9c: a94357f6     	ldp	x22, x21, [sp, #0x30]
```
release：
```text
      80: b9400a68     	ldr	w8, [x19, #0x8]
      84: f9000274     	str	x20, [x19]
      88: 11000508     	add	w8, w8, #0x1
      8c: 9bb85109     	umaddl	x9, w8, w24, x20
      90: d1024120     	sub	x0, x9, #0x90
      94: 29015668     	stp	w8, w21, [x19, #0x8]
      98: a9444ff4     	ldp	x20, x19, [sp, #0x40]
      9c: a94357f6     	ldp	x22, x21, [sp, #0x30]
```

函数`_ZN4llvm23SmallVectorTemplateBaseIN5clang3doc13FieldTypeInfoELb0EE18growAndEmplaceBackIJNS2_8TypeInfoENSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEEERS3_DpOT_`：
debug：
```text
      d0: b9400a68     	ldr	w8, [x19, #0x8]
      d4: f9000274     	str	x20, [x19]
      d8: 11000508     	add	w8, w8, #0x1
      dc: 9bb65109     	umaddl	x9, w8, w22, x20
      e0: 29015668     	stp	w8, w21, [x19, #0x8]
      e4: d1060120     	sub	x0, x9, #0x180
      e8: a9444ff4     	ldp	x20, x19, [sp, #0x40]
      ec: a94357f6     	ldp	x22, x21, [sp, #0x30]
```
release：
```text
      d0: b9400a68     	ldr	w8, [x19, #0x8]
      d4: f9000274     	str	x20, [x19]
      d8: 11000508     	add	w8, w8, #0x1
      dc: 9bb65109     	umaddl	x9, w8, w22, x20
      e0: d1060120     	sub	x0, x9, #0x180
      e4: 29015668     	stp	w8, w21, [x19, #0x8]
      e8: a9444ff4     	ldp	x20, x19, [sp, #0x40]
      ec: a94357f6     	ldp	x22, x21, [sp, #0x30]
```

函数`_ZN4llvm23SmallVectorTemplateBaseIN5clang3doc14MemberTypeInfoELb0EE18growAndEmplaceBackIJNS2_8TypeInfoENSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEENS1_15AccessSpecifierERbEEERS3_DpOT_`：
debug：
```text
     130: 52803409     	mov	w9, #0x1a0              // =416
     134: f9000274     	str	x20, [x19]
     138: 11000508     	add	w8, w8, #0x1
     13c: 9ba95109     	umaddl	x9, w8, w9, x20
     140: 29015a68     	stp	w8, w22, [x19, #0x8]
     144: d1068120     	sub	x0, x9, #0x1a0
     148: a9454ff4     	ldp	x20, x19, [sp, #0x50]
     14c: a94457f6     	ldp	x22, x21, [sp, #0x40]
```
release：
```text
     130: 52803409     	mov	w9, #0x1a0              // =416
     134: f9000274     	str	x20, [x19]
     138: 11000508     	add	w8, w8, #0x1
     13c: 9ba95109     	umaddl	x9, w8, w9, x20
     140: d1068120     	sub	x0, x9, #0x1a0
     144: 29015a68     	stp	w8, w22, [x19, #0x8]
     148: a9454ff4     	ldp	x20, x19, [sp, #0x50]
     14c: a94457f6     	ldp	x22, x21, [sp, #0x40]
```

函数`_ZN4llvm23SmallVectorTemplateBaseIN5clang3doc8LocationELb0EE18growAndEmplaceBackIJRS3_EEES6_DpOT_`：
debug：
```text
     150: 52800909     	mov	w9, #0x48               // =72
     154: f9000274     	str	x20, [x19]
     158: 11000508     	add	w8, w8, #0x1
     15c: 9ba95109     	umaddl	x9, w8, w9, x20
     160: 29015a68     	stp	w8, w22, [x19, #0x8]
     164: d1012120     	sub	x0, x9, #0x48
     168: a9454ff4     	ldp	x20, x19, [sp, #0x50]
     16c: a94457f6     	ldp	x22, x21, [sp, #0x40]
```
release：
```text
     150: 52800909     	mov	w9, #0x48               // =72
     154: f9000274     	str	x20, [x19]
     158: 11000508     	add	w8, w8, #0x1
     15c: 9ba95109     	umaddl	x9, w8, w9, x20
     160: d1012120     	sub	x0, x9, #0x48
     164: 29015a68     	stp	w8, w22, [x19, #0x8]
     168: a9454ff4     	ldp	x20, x19, [sp, #0x50]
     16c: a94457f6     	ldp	x22, x21, [sp, #0x40]
```
#### 17 IncludeFixer.cpp

llvm-diff（每个下列函数）：exit=0，stdout/stderr为空；归因(b) PASS。后端重转wall 0.2517894949996844秒、RSS 481252KiB。

函数`_ZN4llvm12handleErrorsIJZNS_12consumeErrorENS_5ErrorEEUlRKNS_13ErrorInfoBaseEE_EEES1_S1_DpOT_`：
debug：
```text
     128: d63f0100     	blr	x8
     12c: 36000160     	tbz	w0, #0x0, 0x158 <_ZN4llvm12handleErrorsIJZNS_12consumeErrorENS_5ErrorEEUlRKNS_13ErrorInfoBaseEE_EEES1_S1_DpOT_+0x158>
     130: f9400288     	ldr	x8, [x20]
     134: aa1403e0     	mov	x0, x20
     138: f900027f     	str	xzr, [x19]
     13c: f9400501     	ldr	x1, [x8, #0x8]
     140: a9454ff4     	ldp	x20, x19, [sp, #0x50]
     144: a94457f6     	ldp	x22, x21, [sp, #0x40]
```
release：
```text
     128: d63f0100     	blr	x8
     12c: 36000160     	tbz	w0, #0x0, 0x158 <_ZN4llvm12handleErrorsIJZNS_12consumeErrorENS_5ErrorEEUlRKNS_13ErrorInfoBaseEE_EEES1_S1_DpOT_+0x158>
     130: f9400288     	ldr	x8, [x20]
     134: aa1403e0     	mov	x0, x20
     138: f9400501     	ldr	x1, [x8, #0x8]
     13c: f900027f     	str	xzr, [x19]
     140: a9454ff4     	ldp	x20, x19, [sp, #0x50]
     144: a94457f6     	ldp	x22, x21, [sp, #0x40]
```



## 5. debug主线：两次x86全量不变性回归

输入E5/x86-input的225档全部before SHA先核对docs/35锚点；各工具SHA先核对。新生产Source与ARM候选的x86路径分别独立全量转换，未覆盖输入或历史输出。完整比较归档after SHA、成员ordinal/name/occurrence/SHA、完整符号→成员索引与3853后端flags；三份同asm成员的`_ZSt21ios_base_library_initv`均保持唯一U。结果如下（E/x86-*-result.json与progress.json）：

|路径|Source SHA256|归档/成员/flags|结果|转换wall秒|scope峰GiB|
|---|---|---|---|---:|---:|
|production|`c43523c0ce04fc3310e670ff97823db8260c21250dc3172575a18db56500082e`|225 / 3864 / 3853|全部逐字节/完整映射相同 PASS|1787.577|3.711048|
|candidate|`1bac8db608554b35d16482711bf0667f1fbee8d60c6fc52f0f448d240ffaa9e4`|225 / 3864 / 3853|全部逐字节/完整映射相同 PASS|1733.075|5.264145|

production允许缺失符号（按原策略）：`{'W': 1920}`；强符号缺失0。
candidate允许缺失符号（按原策略）：`{'W': 1920}`；强符号缺失0。

本轮两Source未修改，因此Source本体147宿主测试/ARM根143PASS+3环境不适用+1AS既有发现沿用docs/49 §3的同SHA证据；本轮新增辅助16测试独立执行。上述全量转换是本轮新实测，不以旧回归代替。

`build/bin/clang`为软链接`clang-22`，samefile=true且可执行，clang实体SHA `d25e99607c9ea23bf2e50da5075c21f0145f6da24a39a4228d2fd8026ead70cf`。候选spec可按已裁决使用无版本号别名（E/clang-alias.json）。

后续已完成候选重生成与apply/tree核对（§6），随后磁盘门禁停止（§7）。没有新构建树交接给BOLT。


## 6. PS3 / PS2候选重生成与整树核对

基准`cb67996861d070d68fec2b4c623eed7d20ba2e23`。本地候选PS3提交`3731eda7e1b81bd313849a61d60fbac4970a99b1`；PS2提交`4c36e899dffee2869af9afd174346e3eb9a7d7ca`，父子顺序正确。作者FatTank <hao.lin@samsung.com>；Change-Id分别保持Id4eb147e7ec4764d58a81110cf7bf57d21b64ac8与Iac085555112855d60cc7591931e91466691db6b2。干净基准上逐个apply --check/实际apply均PASS，两个阶段git write-tree均与提交tree相同（E/patch-result.json、patch-commands.json）。

PS3 spec相对已上传PS2只将转换器入口由build/bin/clang-22改成clang；Source换成已测试生产版c43523c0…，原W/llvm及其spec未改。PS2删除宏体中的停用注释行，改在宏上方标出tizen_macros:37停用状态，并保留平台宏来源34–38/rpm-build-4.14.1.1-1.4与未来同步要求；只替换archive strip，普通brp-strip仍用平台__strip，不全局覆盖__strip。提交说明明确覆盖本buildroot全部静态归档（含compiler-rt）；完整构建待补、发布模式完整打包尚未认证。未推Gerrit。

|产物|字节|SHA256|
|---|---:|---|
|[patches/archive-index-fix/ps3/0001-packaging-fix-llvm-static-devel-with-ThinLTO.patch](../patches/archive-index-fix/ps3/0001-packaging-fix-llvm-static-devel-with-ThinLTO.patch)|52698|`0d777afbf7b1a7b86afc5c1da5f7bef6b622315efc1316be0cac2b6e782d94e7`|
|[patches/archive-index-fix/ps3/llvm-static-archives-native.py](../patches/archive-index-fix/ps3/llvm-static-archives-native.py)|45786|`c43523c0ce04fc3310e670ff97823db8260c21250dc3172575a18db56500082e`|
|[patches/llvm-strip/ps2/0001-packaging-use-llvm-strip-for-x86_64-archives.patch](../patches/llvm-strip/ps2/0001-packaging-use-llvm-strip-for-x86_64-archives.patch)|3147|`c679f342a72d52de92914cd2d0007c981e0d6d22a6b378f811ca8ee8e12da9ff`|
|[docs/49_356627_ps3.diff](../docs/49_356627_ps3.diff)|52698|`0d777afbf7b1a7b86afc5c1da5f7bef6b622315efc1316be0cac2b6e782d94e7`|
|[docs/49_356639_ps2.diff](../docs/49_356639_ps2.diff)|3147|`c679f342a72d52de92914cd2d0007c981e0d6d22a6b378f811ca8ee8e12da9ff`|

本轮替换的是ps3/ps2候选子目录，不是两份已上传补丁。旧候选摘要保留：PS3 patch `1293f6982c87cfbeefe91aa08e92a7d1b72a129f716417f8c8cee61693c463c6`；PS3 Source `014fd32f309bc0be80471eebf8a4a3cf50a5656ce3a2584e4bbdfb9a05a9affd`；PS2 patch `aab2cfd1ad3fb58bfe44cdbdda50bbe67d5343b29a6a6d598408d3bb96620e88`（E/initial-integrity.json、final-integrity.json；旧版本仍在Git历史）。


## 7. 完整构建磁盘准入：STOP_DISK_ADMISSION

完整构建尚未启动；本轮没有执行gbs/rpmbuild、没有生成RPM，未执行额外磁盘清理（Source自身中间文件生命周期不变）。两Source、Commands、十项比较器、W/llvm/spec、配置和两份已上传补丁均保持原身份。

### 7.1 历史口径与本次计算

最后一次完整x86构建是docs/34（含批准的恢复段）；docs/35、38为增量，不用其增量占用冒充完整构建需求。采用历史文件系统可用空间高水位，并补回那次为完成构建而清理的20GiB ThinLTO缓存：本轮禁止清理，不能把回收带来的空闲当作无需预留。

- 入口可用：220,941,500,416B（docs/34 E/full-build/resource-plan.json）。
- 恢复段最低采样可用：6,409,388,032B（E34/resume-20261008/combined-build-resources.json）。
- 当时释放缓存的已分配空间：21,474,836,480B（同目录cache-reclaim-result.json）。
- 无清理预算口径：入口−最低采样+已回收=236,006,948,864B（219.798599GiB）。另核对清理前读数，取较大值；不是把各组件不同时刻的峰值相加。
- 既定1.2倍准入：ceil(上述值×1.2)=283,208,338,637B，即 **263.758319GiB**。

口径边界：这是历史文件系统整体空间变化（构建树、cache、安装树、转换证据、RPM等），不是隔离根的独占du峰值；历史日志不能分离同时期其他写入者，故不能宣称LLVM自身精确需要这些字节。这里用该已记录的空间预算执行准入，不以清理后的最终树大小缩减预算。若要求独立根峰值，现有记录不足以据此宣称准入已满足。docs/30另一次完整构建的入口−最低采样为235,383,414,784B，其1.2倍为282,460,097,741B（263.061465GiB），本次两个位置也均低于该交叉参照；不是用增量空间估完整构建（docs/30 §2，E/disk-admission.json）。

|检查位置|可用B|可用GiB|准入|
|---|---:|---:|---|
|`/home/linhao/Toolchain/development/llvm-optimize/temp`|79,377,338,368|73.925907|FAIL|
|`/var/tmp`|265,096,077,312|246.889961|FAIL|

采样时间2026-10-13T18:15:02.939479+08:00；同时记录df原文，/home与/var/tmp是两个文件系统，空间不相加。没有清理、拆分构建目录、调低门槛或启动后重试（E/disk-admission.json、disk-df.txt）。

### 7.2 后续步骤与BOLT交接

|原任务步骤|本轮状态|
|---|---|
|新x86完整-ba构建、CMake/依赖指纹|NOT RUN：磁盘准入FAIL后停止|
|验收1：身份、依赖、实际转换非SKIP|NOT RUN|
|验收2：install-post/execve、逐档llvm-strip与其余brp|NOT RUN|
|验收3：225归档、45 compiler-rt、libarcher双归属|NOT RUN（离线x86回归不代替RPM验收）|
|验收4：同配方无补丁基线的非归档比较|NOT RUN|
|验收5：七宿主与Tizen bfd/lld、运行库消费者|NOT RUN|
|验收6：独立真实安装与同树SKIP|NOT RUN|
|验收7：新构建≥10成员直接非LTO结构记录|NOT RUN；§4的60对夹具诊断另存，不冒称新构建记录|
|BOLT交接|NOT READY，无新build目录、完成时间、ThinLTO缓存或经验证配置可交接|
|两ARM全量、根内小试、64MiB负例|NOT RUN：按原顺序位于完整构建之后|
|bash依赖清单、LLVM23探测|NOT RUN：停止后不越过执行顺序|
|发布模式完整构建、ARM第二段打包|继续挂账；发布路径将来用于Tizen-Base，优先级提高|

PS3/PS2是评审候选，提交说明仍保留完整构建待补；未生成伪称全验收通过的commit-message-final.txt。没有发出“BOLT可在新树续跑”的交接承诺，现有Rnew只作为本轮只读工具/输入。新补丁身份见§6，但这些身份不是新RPM或新构建树的身份（E/stop.json、patch-result.json）。

## 8. 资源、回收、证据与提交

所有实际执行scope为18GiB/swap0、nice15/ionice3；重阶段有共享flock，clang/诊断工具命令4GiB AS。下表wall为scope过程时长，不是性能对比；峰值含页缓存。

|阶段|入场可用GiB / 门槛|wall秒|scope峰GiB|宿主最低GiB|exit|
|---|---|---:|---:|---:|---:|
|attribution-tests|12.992691 / 6|2.121|0.016949|12.992382|0|
|first33|13.402748 / 10|12.181|1.055183|13.402702|1|
|first33-retry|11.749428 / 10|84.593|0.616970|11.501190|0|
|remaining7|13.447994 / 10|2.122|0.114418|13.447994|0|
|aarch64-physical|13.433128 / 10|296.170|1.159843|11.183235|0|
|x86-production|13.454914 / 10|1885.153|3.711048|12.247395|0|
|x86-candidate|13.492382 / 10|1800.622|5.264145|11.958115|0|
|patch-generation|13.572456 / 6|10.172|0.558895|13.572575|0|

first33首次exit1是§3.2的辅助路径错误，唯一一次授权修正重跑PASS，不隐去失败。全部scope无OOM；首次first33共享锁等待约752秒，第二轮x86等待270.006秒。资源包装器日志统一写BUILD COMMAND，该标签不代表执行过本轮LLVM完整构建。

最终核查14项SHA PASS；旧候选Source的014fd32f…另从开场Git提交读取核对，受保护两份已上传补丁与6bd0546a Source副本均未改。项目锁已在18:16:47释放，8个scope均退出、采样器及日志线程回收；任务相关进程0、临时挂载0、项目锁0，各重阶段的共享锁均按finally释放。没有读取BOLT工作树/证据或操作其他会话进程（E/final-integrity.json、cleanup-final.json、final-mountinfo.txt、各heavy-lock-released.json）。

阶段提交均已推GitHub main：辅助与16测试c5b7e41；33对与Serialize归因70117de；60对认证aeea5f8；生产x86回归/升级手册0b6f5d8；双x86回归d1ccc5d；候选补丁a454bbc。此停止报告与STATUS同提交；最终钉提交号链接在回复中给出。未推Gerrit。

全部原始输出在E（本机，不上传）：参数逐token与上下文证明、60对比较/归因、opt/llvm-diff/objdump完整命令与原文、后端再转换、各Source转换summary/逐成员检查、apply/tree日志、资源采样、磁盘门禁、收尾核查。评审文档、辅助与测试、候选补丁和外置diff在本仓库。


## 9. 续四执行中补充裁决：30GiB底线与/var/tmp构建根

2026-10-13用户新增两条要求，本提交登记生效，§7的历史停止数据不改判：

1. 任何一次写入超过10GiB的操作，写完后所在文件系统可用空间必须仍不少于30GiB；不满足就跳过该项并报告，不清理任何现有目录。适用于完整构建、解包、转换、缓存复制等大写入，不把一次操作拆成小份规避；后续执行前按目的文件系统核查写入预算与剩余空间，执行后记录实测值。用户提到BOLT会话复制缓存曾使工作区只剩约5.6GB，这是人工告知，不是本会话实测；本会话未进入其目录核查或修改。
2. 新x86完整构建根固定为 `/var/tmp/llvm-optimize-x86-archivefix-20261013`；准入只按`/var/tmp`所在文件系统计算，不再以`/home`不足替代该根的判定，也不合并两个文件系统空间。实际构建验收通过后才在STATUS登记完整build/cache路径和BOLT可续跑交接；当前只是计划根路径，尚未创建、不能作为交接。

本补充没有取消原任务“历史实测占用×1.2”准入；两项分别检查。即使只考虑新增30GiB底线，下述预算检查也未通过。

### 9.1 复查证据与决定

基准为上一收尾提交`183eb20725f1ad0bc6fe8d31504219c672bce8d4`。14项Source/spec/config/比较器/补丁SHA复核全部PASS；工作树仍只有既有用户`gbs_llvm.conf`修改。双项目锁覆盖这次记录更新；没有启动重阶段，不占用BOLT共享重任务锁。

证据目录 D=`temp/release-attribution-20261013/disk-supplement-20261013`；D/admission.json、df.txt、findmnt.txt、git-status.txt。读数时间：2026-10-13T18:33:59.237786+08:00。

|项目|字节|GiB/结果|
|---|---:|---|
|`/var/tmp`当前可用|265,082,286,080|246.877117|
|§7登记的历史无清理写入预算|236,006,948,864|219.798599|
|按上述预算写完预计剩余|29,075,337,216|27.078518|
|用户新增剩余底线|32,212,254,720|30|
|底线预算缺口|3,136,917,504|2.921482|
|原1.2倍准入|283,208,338,637|263.758319，FAIL|

**决定：SKIP_FULL_BUILD_DISK_FLOOR。** 原1.2倍准入仍FAIL；按当前可用减历史预算，预计剩余不足30GiB，新增底线也FAIL。历史预算的范围与局限沿用§7：这是整个文件系统可用空间变化，不能分离其他写入者，不是LLVM独占du或未来用量保证；没有把估计剩余冒充新构建实测，也没有改用更小的事后树大小放行。

因此本次没有创建新构建根，没有GBS/rpmbuild、超过10GiB的写入、磁盘清理或新RPM；两Source、Commands、比较器、两份已上传补丁、W/llvm与配置均未修改。后续顺序仍停在完整构建前；§7.2的验收/ARM/LLVM23等NOT RUN状态不变。BOLT交接仍NOT_READY；STATUS记录计划根而不宣称可续跑。此前60对认证、两次x86回归与候选apply/tree PASS仍有效，不重跑。

本次仅文档与状态更新；没有启动构建、采样器或挂载。双项目锁在记录完成后释放，回收证据见D/lock-released.json、cleanup.json。报告与STATUS同提交推送GitHub main，不推Gerrit。
