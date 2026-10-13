# 49 续四：发布模式参数认证与差异归因

日期：2026-10-13；开场HEAD `df729697426dff67a3871bfa850754ee8be7d376`。**进行中：60对参数PASS；发布模式参数与归因认证PASS；生产Source的x86全量回归PASS，ARM候选的x86回归待执行。** 旧docs/49及续三保留，十项ELF比较器和两份Source/Commands不修改。本页不超过50KB。

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

## 5. debug主线：x86回归进度

生产Source第一轮PASS：225档after SHA、3864有序成员、完整索引、3853组后端flags与docs/35完全一致；三份同asm成员U符号门禁PASS，强符号缺失0，允许缺失W=1920。转换1787.577秒，总1882.794秒，scope峰3,984,707,584B，无OOM。第二轮ARM候选x86路径随后执行（E/x86-production-result.json、x86-production-scope/memory-summary.json）。
