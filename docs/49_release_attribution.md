# 49 续四：发布模式参数认证与差异归因

日期：2026-10-13；开场HEAD `df729697426dff67a3871bfa850754ee8be7d376`。**进行中：独立辅助16项测试PASS；前33对参数PASS，Serialize.cpp按后端路径(b)已归因PASS。** 旧docs/49及续三保留，十项ELF比较器和两份Source/Commands不修改。本页不超过50KB。

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


## 4. debug主线与挂账

待执行：x86两次全量回归→PS3/PS2候选重生成与顺序apply/tree→新根完整构建/验收1–7→冻结BOLT交接→ARM全量/根内小试/64MiB负例→bash债务/LLVM23探测。主线自身失败仍停止；没有新交接树。发布模式完整构建仍挂账，未来Tizen-Base未定义_toolchain的实际交付提高其优先级，待PM安排。

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

ARM32余7对、AArch6420对尚待执行。
