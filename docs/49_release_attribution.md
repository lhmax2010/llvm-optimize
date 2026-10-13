# 49 续四：发布模式参数认证与差异归因

日期：2026-10-13；开场HEAD `df729697426dff67a3871bfa850754ee8be7d376`。**进行中：独立辅助16项测试PASS，实物参数门禁与归因待执行。** 旧docs/49及续三保留，十项ELF比较器和两份Source/Commands不修改。本页不超过50KB。

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

待执行。已有33对先检查；ARM32剩7对及AArch6420对随后执行。发布结论独立于debug主线。

## 4. debug主线与挂账

待执行：x86两次全量回归→PS3/PS2候选重生成与顺序apply/tree→新根完整构建/验收1–7→冻结BOLT交接→ARM全量/根内小试/64MiB负例→bash债务/LLVM23探测。主线自身失败仍停止；没有新交接树。发布模式完整构建仍挂账，未来Tizen-Base未定义_toolchain的实际交付提高其优先级，待PM安排。
